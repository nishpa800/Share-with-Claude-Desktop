"""
Nexus Data Preparation Layer
Transforms raw captured WebSocket data (trades, minute aggs, NOI) into
structured context windows for the Nexus agent pipeline.
"""

import pyarrow.parquet as pq
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import json

DATA_DIR = Path("/Users/anishpatel/quant-brain/data/realtime")
NEXUS_DATA = Path("/Users/anishpatel/quant-brain/nexus/data")


def load_day(channel: str, date: str) -> pd.DataFrame:
    day_dir = DATA_DIR / channel / date
    if not day_dir.exists():
        return pd.DataFrame()
    files = sorted(day_dir.glob("*.parquet"))
    if not files:
        return pd.DataFrame()
    dfs = []
    for f in files:
        try:
            dfs.append(pq.read_table(f).to_pandas())
        except Exception:
            pass
    if not dfs:
        return pd.DataFrame()
    return pd.concat(dfs, ignore_index=True)


def build_minute_bars(date: str, ticker: str) -> pd.DataFrame:
    aggs = load_day("minute_aggs", date)
    if aggs.empty:
        return aggs
    tick_col = "T" if "T" in aggs.columns else "sym"
    bars = aggs[aggs[tick_col] == ticker].copy()
    if bars.empty:
        return bars
    bars["dt"] = pd.to_datetime(bars["s"] if "s" in bars.columns else bars["t"], unit="ms")
    bars = bars.sort_values("dt")
    return bars


def build_noi_profile(date: str, ticker: str) -> dict:
    noi = load_day("noi", date)
    if noi.empty:
        return {"has_noi": False}

    t_noi = noi[noi["T"] == ticker].copy()
    if t_noi.empty:
        return {"has_noi": False, "ticker": ticker}

    t_noi = t_noi.sort_values("t")
    open_msgs = t_noi[t_noi["a"] == "M"]
    close_msgs = t_noi[t_noi["a"] == "C"]

    profile = {
        "has_noi": True,
        "ticker": ticker,
        "total_messages": len(t_noi),
        "open_messages": len(open_msgs),
        "close_messages": len(close_msgs),
    }

    if len(open_msgs) > 0:
        last_open = open_msgs.iloc[-1]
        profile["open_final_imbalance"] = int(last_open["o"])
        profile["open_final_paired"] = int(last_open["p"])
        profile["open_book_price"] = float(last_open["b"])
        profile["open_direction"] = "BUY" if last_open["o"] > 0 else ("SELL" if last_open["o"] < 0 else "NEUTRAL")

        imb_values = open_msgs["o"].values
        consec = 1
        max_consec = 1
        for j in range(1, len(imb_values)):
            if (imb_values[j] > 0 and imb_values[j - 1] > 0) or (imb_values[j] < 0 and imb_values[j - 1] < 0):
                consec += 1
                max_consec = max(max_consec, consec)
            else:
                consec = 1
        profile["open_max_consecutive"] = max_consec
        profile["open_acceleration"] = max_consec >= 4

    if len(close_msgs) > 0:
        last_close = close_msgs.iloc[-1]
        profile["close_final_imbalance"] = int(last_close["o"])
        profile["close_final_paired"] = int(last_close["p"])
        profile["close_book_price"] = float(last_close["b"])
        profile["close_direction"] = "BUY" if last_close["o"] > 0 else ("SELL" if last_close["o"] < 0 else "NEUTRAL")
        paired = last_close["p"] if last_close["p"] != 0 else 1
        profile["close_imbalance_ratio"] = abs(float(last_close["o"])) / float(paired)

    return profile


def build_context_window(ticker: str, dates: list[str]) -> dict:
    """
    Build the structured historical context H_{1:τ} for a ticker.
    This is what the Historical Context Agent produces.

    For each date: OHLCV summary + NOI profile + key metrics.
    """
    context = {
        "ticker": ticker,
        "dates": dates,
        "history": [],
    }

    for date in dates:
        bars = build_minute_bars(date, ticker)
        noi = build_noi_profile(date, ticker)

        day_entry = {
            "date": date,
            "noi": noi,
        }

        if not bars.empty:
            day_entry["open"] = float(bars.iloc[0]["o"]) if "o" in bars.columns else None
            day_entry["high"] = float(bars["h"].max()) if "h" in bars.columns else None
            day_entry["low"] = float(bars["l"].min()) if "l" in bars.columns else None
            day_entry["close"] = float(bars.iloc[-1]["c"]) if "c" in bars.columns else None
            day_entry["volume"] = int(bars["v"].sum()) if "v" in bars.columns else None
            day_entry["vwap"] = float(bars["vw"].mean()) if "vw" in bars.columns else None
            day_entry["bar_count"] = len(bars)

            if day_entry["open"] and day_entry["open"] != 0:
                day_entry["return_pct"] = round(
                    (day_entry["close"] - day_entry["open"]) / day_entry["open"] * 100, 3
                )
        else:
            day_entry["no_data"] = True

        context["history"].append(day_entry)

    return context


def build_multi_timeframe_bars(date: str, ticker: str) -> dict:
    """
    Build bars at all 13 timeframes from 1-minute data.
    Returns dict of timeframe -> DataFrame.
    """
    bars_1m = build_minute_bars(date, ticker)
    if bars_1m.empty:
        return {}

    bars_1m = bars_1m.set_index("dt")
    result = {"1m": bars_1m}

    timeframes = {
        "3m": "3min", "5m": "5min", "10m": "10min", "15m": "15min",
        "30m": "30min", "1h": "1h", "2h": "2h", "3h": "3h",
    }

    for label, freq in timeframes.items():
        try:
            resampled = bars_1m.resample(freq).agg({
                "o": "first", "h": "max", "l": "min", "c": "last",
                "v": "sum", "vw": "mean",
            }).dropna()
            result[label] = resampled
        except Exception:
            pass

    return result


def get_available_dates() -> list[str]:
    noi_dir = DATA_DIR / "noi"
    if not noi_dir.exists():
        return []
    return sorted([d.name for d in noi_dir.iterdir() if d.is_dir()])


def get_tickers_with_noi(date: str) -> list[str]:
    noi = load_day("noi", date)
    if noi.empty:
        return []
    return sorted(noi["T"].unique().tolist())
