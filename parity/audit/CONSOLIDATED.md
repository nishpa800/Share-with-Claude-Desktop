# Pine → Candle-Factory Parity Audit — CONSOLIDATED VERDICT

**Date:** 2026-05-31
**Scope:** 4 indicator studies attached by Anish, audited by 4 parallel agents.
**Question answered:** *"If we deconstruct these indicators and apply them to our own
candle factory fed by Massive.com OHLCV, can we reproduce every detection plot —
or is there a TradingView proprietary dependency that decouples us from TradingView?"*

---

## TL;DR — THE ANSWER

**YES. All four indicators are reproducible from a Massive.com OHLCV candle factory.
There are ZERO blocked plots and ZERO un-substitutable TradingView data feeds.**

The "TV dot" dependency Anish flagged is **one open-source library import**:
`import TradingView/ta/7` → `tv_ta.relativeVolume(...)`. This is **published Pine
source code** (session-anchored Relative Volume), **not** a proprietary data feed.
It is reimplemented from Massive minute aggregates. It appears in **B2B PUP**,
**HVD-PBJ BULL**, and **HVD-PBJ BEAR**.

Everything else is `ta.*` / `math.*` built-ins (pure functions of OHLCV) + bar
metadata (`time`, `syminfo.mintick`, `barstate.isconfirmed`).

---

## PER-INDICATOR STATUS

| Indicator | Lines / Pine | Detection plots | PURE_OHLCV | TV-lib (RVOL) | BLOCKED | Verdict |
|---|---|---|---|---|---|---|
| Anish TB Foster Fix | 221 / v6 | 14 signals (28 surfaces) | 14 | 0 | 0 | ✅ Fully reproducible, warmup only |
| B2B PUP Combined 5.4 | 1248 / v5 (hdr v4.31) | 20 S-maps / 36 plotshapes | 11 | 8 (S5,S8–S12,S19,S20) | 0 | ✅ Reproducible; rebuild RVOL baseline |
| HVD-PBJ BEAR (36) | 1302 / v5 | 36 plotshapes | 36 | uses lib but bear plots clean | 0 | ✅ Fully reproducible |
| HVD-PBJ BULL (38) | 1312 / v5 | 38 (44 plotshapes) | ~36 | lib import present | 0 | ✅ Reproducible, large warmup |

Full per-plot tables (every equation, input, dependency, parity status) are in:
- `parity/audit/foster.md`
- `parity/audit/b2b_pup.md`
- `parity/audit/hvd_pbj_bear.md`
- `parity/audit/hvd_pbj_bull.md`

---

## THE ONE "TV." DEPENDENCY — RESOLVED

**What it is:** `tv_ta.relativeVolume(length, anchorTimeframe, ...)` from the
open-source `TradingView/ta/7` standard library. Internally it uses
`request.security_lower_tf` to pull the symbol's OWN lower-timeframe volume and
build a session-anchored cumulative RVOL baseline. It is **the same symbol's
volume** — NOT external data, NOT another symbol, NOT a TradingView-only feed.

**7-Pillar resolution:**
- *Problem:* one function pulls intraday volume to compute session RVOL.
- *Knowns:* formula is open-source; Massive has minute aggregates on disk
  (`/data/historical/minute/`, 30 days) + REST/S3 for deeper history.
- *Unknowns:* exact session-anchor convention (RTH vs ETH), warmup length.
- *Equation:* `RVOL_t = cum_volume_in_session_to_t / avg(cum_volume_to_same_offset over prior N sessions)`.
- *Resolution:* reimplement in Python from Massive minute bars; ≥30-session warmup;
  validate against TradingView `data_get_study_values` via MCP on the live chart.
- *Blast radius:* affects 8 of B2B PUP's plotted signals + RVOL inputs in HVD-PBJ.
  If skipped, those signals mis-fire; if rebuilt, full parity.

---

## CROSS-CUTTING PARITY RISKS (apply to ALL ports)

1. **Recursive-function seeding.** TradingView seeds `ta.ema` with an SMA, `ta.atr`/
   `ta.rma` with Wilder's method. A naive Python EMA diverges for ~3×length bars.
   → Replicate TV's exact seeding; discard warmup region from parity comparison.

2. **Warmup budget vs. the 6000-bar plan.** Largest lookback is GZ1 `ta.highest(...,5000)`
   and `ta.highest(volume,1000)`. With EXACTLY 6000 bars and a 5000-bar lookback,
   **only the last ~1000 bars are fully warmed.** Parity tests must compare the
   warmed tail, not the head. For these specific engines, more history = safer.

3. **From-genesis running state.** `maxVolEver`, HEV/Nagasaki maxima, SuperTrend
   `curr_long/short/st_dir`, `ta.cum`, and all `var` streak/array counters depend on
   EVERY bar since the symbol's first bar. A windowed slice starting at a different
   bar than TradingView started **will not match.** → Genesis-aligned replay, or
   accept drift and document it.

4. **Volume exact-equality fragility.** Dozens of `volume == ta.highest(volume,N)`
   gates. Massive made size/volume columns DECIMALS on 2026-02-23. Float `==` is
   fragile. → Use `volume >= max - ε` or match TV's rounding.

5. **`syminfo.mintick`.** Used as an SR-dedup epsilon (B2B PUP, HVD-PBJ). Not market
   data. → Supply a per-symbol tick-size table.

6. **Centered pivots.** `ta.pivothigh/pivotlow` look right; need a right-offset in the
   Python port to avoid lookahead bias.

7. **Canonical source pinning.** Multiple copies of these files exist on disk
   (`~/code/anish/indicators/...`) and the Desktop TCC sandbox blocks `ls`/Read
   (python `open()` and `mdfind` work). **Pin a SHA-256 of the exact source** before
   porting so the Python version is traceable to one Pine revision.

8. **`barstate.isconfirmed` gating.** Nearly all signals fire only on closed bars →
   historically exact; live/realtime bars are intentionally excluded. Good for parity.

---

## DUCKDB / THROUGHPUT / CHOKE-POINT CONCERNS

- **Candle factory (3 stocks × 5 TF × 6000 bars):** trivial — sub-second in DuckDB.
- **Real choke = parity at scale.** From-genesis state (risk #3) means you cannot
  parity-test on a 6000-bar slice for the running-max / SuperTrend / cum engines;
  those need full history per symbol. Budget for full-history pulls on the watchlist.
- **RVOL rebuild** needs minute data per session → 30-session minimum per symbol.
  On-disk minute data is only 30 days; deeper RVOL history needs Massive REST/S3.
- **Fallback plans:** (a) if minute history is thin, compute RVOL from daily-volume
  proxy and flag reduced fidelity; (b) if from-genesis replay is too costly for 807
  tickers, restrict full-state engines to the active candidate shortlist and run the
  cheap PURE_OHLCV engines across the full universe.
