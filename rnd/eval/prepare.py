"""
R&D AutoResearch — prepare.py   [SACRED — do not let an experiment edit this]
=============================================================================
This is the `prepare.py` equivalent of Karpathy autoresearch: fixed data prep
and the ground-truth LABEL. Changing this file changes the QUESTION, so it is
read-only to the experiment loop. Only a human (with the charter open) edits it.

WHAT IT DOES
------------
Loads local daily bars (free, on-disk), restricts to the watchlist population,
and for every (ticker, day) builds:
  • FEATURES  — measurable shadows of VOB structure / potential & kinetic energy
                (momentum, volume surge, range, gap, where-in-range, distance to
                 recent floor/ceiling, volatility, streak, avg trade size).
  • LABEL     — the 2x2 resolution, BULL branch:  does a bullish trigger become a
                TRUE LAUNCH (sustained +TGT move) or a TRAP (rolls over to -STP)?

The label encodes Anish's exact question: "when is a bullish detection plot VERY
bullish vs a bullish-looking plot that turns price into a bearish leg." TGT=0.10
ties to the 10%x6 mantra.

The result is cached ONCE to cache/events.parquet. The autoresearch loop then runs
thousands of experiments against the cache for free — the expensive load happens
a single time. That is the token/compute economics: Python = free muscle.

PROVENANCE
----------
Source: /data/historical/daily/{2025,2026}/MM/YYYY-MM-DD.csv.gz
Schema: ticker, volume, open, close, high, low, window_start(ns), transactions
"""
from __future__ import annotations
import glob
import os
import sys
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DAILY_GLOB = os.path.join(ROOT, "data", "historical", "daily", "*", "*", "*.csv.gz")
WATCHLIST = os.path.join(ROOT, "watchlist.txt")
CACHE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cache", "events.parquet")

# ---- LABEL CONSTANTS (SACRED — these define the question, not a tunable) -------
TGT = 0.10      # +10% = a real launch (the 10%x6 thesis)
STP = 0.05      # -5% drawdown first = a trap / bearish leg
HORIZON = 5     # trading days to resolve
LOOKBACK = 20   # rolling window for structure features


def _load_watchlist() -> set[str]:
    with open(WATCHLIST) as f:
        return {ln.strip().upper() for ln in f if ln.strip()}


def _load_daily(watch: set[str]) -> pd.DataFrame:
    files = sorted(glob.glob(DAILY_GLOB))
    if not files:
        raise FileNotFoundError(f"no daily bars matched {DAILY_GLOB}")
    frames = []
    for fp in files:
        try:
            df = pd.read_csv(fp, compression="gzip",
                             usecols=["ticker", "volume", "open", "close",
                                      "high", "low", "window_start", "transactions"])
        except Exception as e:                       # never let one bad file kill prep
            print(f"  warn: skip {os.path.basename(fp)}: {e}", file=sys.stderr)
            continue
        df = df[df["ticker"].str.upper().isin(watch)]
        frames.append(df)
    out = pd.concat(frames, ignore_index=True)
    out["ticker"] = out["ticker"].str.upper()
    out["date"] = pd.to_datetime(out["window_start"], unit="ns").dt.normalize()
    out = out.sort_values(["ticker", "date"]).reset_index(drop=True)
    return out


def _features_and_label(g: pd.DataFrame) -> pd.DataFrame:
    """Per-ticker. All features use info up to & including day t (no lookahead).
    Label looks FORWARD HORIZON days — that is the outcome we are predicting."""
    g = g.sort_values("date").reset_index(drop=True)
    c, h, l, o, v = g["close"], g["high"], g["low"], g["open"], g["volume"]
    tx = g["transactions"].replace(0, np.nan)
    prev_c = c.shift(1)

    g["ret1"] = c / prev_c - 1.0
    g["ret5"] = c / c.shift(5) - 1.0
    g["ret20"] = c / c.shift(20) - 1.0
    vol_ma = v.rolling(LOOKBACK).mean()
    g["vol_ratio"] = v / vol_ma
    g["range_pct"] = (h - l) / c
    g["gap"] = o / prev_c - 1.0
    rng = (h - l).replace(0, np.nan)
    g["close_pos"] = (c - l) / rng                       # 1=closed on high (kinetic up)
    g["dist_hi20"] = c / h.rolling(LOOKBACK).max() - 1.0  # proximity to ceiling
    g["dist_lo20"] = c / l.rolling(LOOKBACK).min() - 1.0  # proximity to floor/VOB
    g["vol20"] = g["ret1"].rolling(LOOKBACK).std()
    up = (g["ret1"] > 0).astype(int)
    g["up_streak"] = up * (up.groupby((up != up.shift()).cumsum()).cumcount() + 1)
    g["avg_trade_size"] = v / tx
    tx_ma = tx.rolling(LOOKBACK).mean()
    g["tx_ratio"] = tx / tx_ma

    # ---- forward LABEL (path-aware-lite): launched without first getting stopped ----
    hv, lv, cv = h.values, l.values, c.values
    n = len(g)
    fwd_max = np.full(n, np.nan)
    fwd_min = np.full(n, np.nan)
    for i in range(n):
        j = min(i + 1 + HORIZON, n)
        if i + 1 < j:
            fwd_max[i] = hv[i + 1:j].max()
            fwd_min[i] = lv[i + 1:j].min()
    p = cv
    launched = fwd_max >= p * (1 + TGT)
    stopped = fwd_min <= p * (1 - STP)
    label = np.where(np.isnan(fwd_max), np.nan,
                     np.where(launched & ~stopped, 1.0, 0.0))
    g["label"] = label
    return g


FEATURE_COLS = ["ret1", "ret5", "ret20", "vol_ratio", "range_pct", "gap",
                "close_pos", "dist_hi20", "dist_lo20", "vol20", "up_streak",
                "avg_trade_size", "tx_ratio"]


def build_events(force: bool = False) -> str:
    if os.path.exists(CACHE) and not force:
        print(f"cache exists: {CACHE} (use force=True to rebuild)")
        return CACHE
    watch = _load_watchlist()
    print(f"watchlist: {len(watch)} tickers")
    daily = _load_daily(watch)
    print(f"daily rows (watchlist): {len(daily):,} across {daily['ticker'].nunique()} tickers")
    parts = []
    for tk, g in daily.groupby("ticker", sort=False):
        gg = _features_and_label(g.copy())
        gg["ticker"] = tk
        parts.append(gg)
    ev = pd.concat(parts, ignore_index=True)
    ev = ev.dropna(subset=["label"]).reset_index(drop=True)
    keep = ["ticker", "date", "close", "label"] + FEATURE_COLS
    ev = ev[keep]
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    ev.to_parquet(CACHE, index=False)
    pos = ev["label"].mean()
    print(f"events: {len(ev):,} rows | base-rate(launch)={pos:.3f} | saved -> {CACHE}")
    return CACHE


def load_events() -> pd.DataFrame:
    if not os.path.exists(CACHE):
        build_events()
    return pd.read_parquet(CACHE)


if __name__ == "__main__":
    build_events(force="--force" in sys.argv)
