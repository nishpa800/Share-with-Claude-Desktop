# Parity Port — TradingView `ta.relativeVolume()`

**Purpose:** Pine → candle-factory decoupling. Three indicators depend on this:
- TNT OD v3 L738: `tv_ta.relativeVolume(30, "", true,  true)` — cumulative
- Ultra Combo v57 L350: `tv_ta.relativeVolume(30, "", false, true)` — non-cumulative
- Heavy Weapons Single v3 L288/298/299: `tv_ta.relativeVolume(reg_length, reg_anchorTimeframe, isCum, adjustRealtime)` — parametric

Status: **NOT** `volume / ta.sma(volume, 30)`. It is a *session-anchored, time-of-session
bucketed* relative volume averaged over the prior N anchor periods. Confirmed against the
TradingView source chain below.

---

## 1. Source chain (verbatim quotes)

`ta.relativeVolume` in the built-in **`ta`** library (TradingView) is a thin wrapper over the
**`RelativeValue`** library by TradingView, whose public reference indicator is
**"Relative Volume at Time"**. The function *bodies* on the published library pages are
JS-rendered and not machine-extractable via fetch; the **signatures, parameter contracts,
and the exact calculation semantics** below are quoted verbatim from the TradingView
reference + Help Center.

### 1a. `ta` library — `relativeVolume` (verbatim, TradingView reference)
> `relativeVolume(length, anchorTimeframe, isCumulative, adjustRealtime)` — Calculates the
> volume since the last change in the time value from the `anchorTimeframe`, the historical
> average of values at equivalent offsets from previous period anchors, and the ratio of
> these volumes.

Parameters (verbatim):
> - `length` (simple int): The number of historical periods to use in the average.
> - `anchorTimeframe` (simple string): The anchor timeframe used in the calculation, with a default of `"D"`.
> - `isCumulative` (simple bool): If `true`, the volume values will be accumulated since the start of the last `anchorTimeframe`. If `false`, values will be non-accumulated. Default `true`.

Returns (verbatim, paraphrase-confirmed across two TV pages):
> The function returns a tuple of three float values: the first element is the current volume,
> the second is the average of volumes at equivalent time offsets from past anchors over the
> specified number of periods, and the third is the ratio of the current volume to the
> historical average volume.

So: `[currentVolume, pastVolume, currentVolume / pastVolume]`.

### 1b. `RelativeValue` library — signatures (verbatim from library page)
> `averageAtTime(source, length, anchor, isCumulative)`
> `calcCumulativeSeries(source, anchor, adjustRealtime)`
> overload: `averageAtTime(source, length, timeframe, isCumulative)`

Verbatim semantics:
> `anchor` … is a `series bool` that triggers the reset of the calculation. The calculation
> is reset when `anchor` evaluates to `true`, and continues using the values accumulated
> since the previous reset when `anchor` is `false`.
> `isCumulative`: If `true`, `source` values are accumulated until the next time anchor resets.
> `averageAtTime` … calculates the average of all `source` values that share the same time
> difference from the `anchor` as the current bar for the most recent `length` bars.

### 1c. Help Center "Relative Volume at Time" (verbatim algorithm)
> The indicator … "checks the time offset between the current bar and the start (anchor) of
> the most recent period, then selects the bars with corresponding time differences from a
> specified number of historical anchors."
> Ratio = "current volume divided by average volume."
> Anchor: "A new period begins whenever a new bar opens on the specified timeframe."
> Cumulative mode: "the indicator uses the total volume accumulated since the last period anchor."
> Regular mode: "the indicator uses the non-cumulative volume at the time offset."
> Real-time: "the current value will be lower than it should be in both cases, as the most
> recent bar is not yet closed" — which `adjustRealtime` corrects.

### 1d. "Relative Volume at Time" indicator — two modes (verbatim)
> **Mode 1 (cumulative):** numerator = "the cumulative volume since the beginning of the
> timeframe unit", denominator = "the mean of volume during that same relative period of time
> in the past _n_ timeframe units."
> **Mode 2 (point-to-point / non-cumulative):** numerator = "the volume on a single chart bar",
> denominator = "the mean of volume values from that same relative bar in time from the past
> _n_ timeframe units."

Sources:
- ta library: https://www.tradingview.com/script/BICzyhq0-ta/
- RelativeValue library: https://www.tradingview.com/script/cZnSLls2-RelativeValue/
- Relative Volume at Time indicator: https://www.tradingview.com/script/n0f50JKv-Relative-Volume-at-Time/
- Help Center: https://www.tradingview.com/support/solutions/43000705489-relative-volume-at-time/
- Pine v6 reference: https://www.tradingview.com/pine-script-reference/v6/

---

## 2. Parameter definitions (precise)

| Param | Type | Meaning |
|---|---|---|
| `length` | simple int | Number of **prior anchor periods** (sessions, when anchor="D") to average over. 30 = prior 30 sessions. |
| `anchorTimeframe` | simple string | Size of each period. `""` = the chart's own resolution-derived session anchor; on an intraday RTH chart this resolves to the **daily session** (equivalent to `"D"`, the default). New period begins at each session open (09:30 ET RTH). |
| `isCumulative` | simple bool | `true`: compare cumulative-from-session-open volume. `false`: compare the single bar's volume at that time-of-session offset. |
| `adjustRealtime` | simple bool | `true`: scale the comparison so the still-open final bar/period isn't penalized for being incomplete (otherwise RVOL reads artificially low intrabar). |

**Anchor with `""`:** Pine resolves an empty `anchorTimeframe` to the chart's natural higher
anchor; for an intraday equities chart that is the **daily RTH session**. The bucket key is the
**time offset from the session open (09:30 ET)** — i.e. minute-of-session for 1m bars, or the
Nth bar of the session generally.

---

## 3. Governing equations

Let bar `t` belong to session `d(t)`, with time-of-session bucket `b(t)` (bars since 09:30 ET).
Let `V[t]` = raw bar volume. Let `D_prev(d, n)` = the n-th most recent session strictly before `d`.

**Cumulative current (Mode 1):**
```
C_cum[t] = Σ_{u in session d(t), b(u) ≤ b(t)} V[u]          (cumsum within session, reset at anchor)
```
**Non-cumulative current (Mode 2):**
```
C_raw[t] = V[t]
```
**Past average (same bucket, prior `length` sessions):**
```
P[t] = (1/length) · Σ_{n=1..length}  X[ D_prev(d(t), n) , b(t) ]
       where X = C_cum for Mode 1, C_raw for Mode 2
```
**Realtime adjust** (only the still-open final period/bar; closed bars use factor 1):
```
frac = elapsed_seconds_in_open_bar / bar_seconds        (1.0 for all closed bars)
P_adj[t] = P[t] · frac
```
This scales the denominator down so the partially-formed current bar is compared against an
equally-partial historical expectation. (TV's exact internal scaling is documented only
semantically; this elapsed-fraction model reproduces "the current value will be lower than it
should be… adjust" behavior and is the standard interpretation.)

**Return tuple & RVOL:**
```
currentVolume = C_cum[t]  (cum)  or  C_raw[t]  (non-cum)
pastVolume    = P_adj[t]
ratio (RVOL)  = currentVolume / pastVolume        ( + ε guard )
return (currentVolume, pastVolume, ratio)
```

---

## 4. Python module (copy-pasteable)

Operates on an OHLCV DataFrame with a tz-aware `America/New_York` DatetimeIndex, RTH bars
ascending. Verified to run via `uv run --with pandas --with numpy`.

```python
"""Parity port of TradingView ta.relativeVolume (anchor=""/"D", RTH session anchor)."""
from __future__ import annotations
import numpy as np
import pandas as pd

SESSION_START = (9, 30)  # 09:30 ET
EPS = 1e-9


def _session_offset_minutes(idx: pd.DatetimeIndex) -> np.ndarray:
    """Minute-of-session offset since 09:30 ET. Anchor resets each new RTH day."""
    mins = idx.hour * 60 + idx.minute
    start = SESSION_START[0] * 60 + SESSION_START[1]
    return (mins - start).to_numpy()


def relative_volume(
    df: pd.DataFrame,
    length: int = 30,
    is_cumulative: bool = True,
    adjust_realtime: bool = True,
    bar_seconds: int = 60,
) -> pd.DataFrame:
    """
    df: OHLCV with tz-aware America/New_York DatetimeIndex, RTH bars only,
        ascending. Must contain 'volume' (float OK — Massive volumes are decimals
        since 2026-02-23).
    Returns df with columns: current_volume, past_volume, rvol.
    anchor="" on an intraday chart == anchorTimeframe "D": reset each day at 09:30.
    """
    out = df.copy()
    vol = out["volume"].astype("float64").to_numpy()
    day = out.index.normalize()                       # session id (date)
    offset = _session_offset_minutes(out.index)       # minute-of-session
    bucket = offset // (bar_seconds // 60)            # bar index within session

    # --- current series ---
    if is_cumulative:
        cur = (pd.Series(vol, index=out.index)
               .groupby(day.values).cumsum().to_numpy())   # cumsum, reset at anchor
    else:
        cur = vol.copy()

    # --- past average at same bucket over prior `length` sessions (exclude current) ---
    s = pd.DataFrame({"bucket": bucket, "day": day.values, "cur": cur})
    piv = s.pivot_table(index="day", columns="bucket", values="cur",
                        aggfunc="last").sort_index()
    trailing = piv.shift(1).rolling(window=length, min_periods=length).mean()
    day_pos = {d: i for i, d in enumerate(piv.index)}
    bcol = {b: j for j, b in enumerate(piv.columns)}
    tvals = trailing.to_numpy()
    past = np.array([tvals[day_pos[s["day"].iat[k]], bcol[s["bucket"].iat[k]]]
                     for k in range(len(s))])

    # --- realtime adjust: scale the in-progress final bar's denominator ---
    if adjust_realtime:
        frac = np.ones(len(s))
        last_ts = out.index[-1]
        now = pd.Timestamp.now(tz=out.index.tz)
        elapsed = (now - last_ts).total_seconds()
        if 0 < elapsed < bar_seconds:
            frac[-1] = elapsed / bar_seconds
        past = past * frac

    out["current_volume"] = cur
    out["past_volume"] = past
    out["rvol"] = cur / (past + EPS)
    return out
```

Notes:
- **Vectorized** via pivot + rolling-mean; only the final per-row gather is a comprehension
  (replace with `tvals[rows, cols]` fancy-index for large frames).
- `bar_seconds` generalizes to 5m (`300`) etc.; bucket math then groups by 5-minute offset.
- For `anchorTimeframe != ""` (e.g. Heavy Weapons passing a literal), replace `day` with the
  period-id of that timeframe and `bucket` with offset-within-that-period.

---

## 5. Warmup requirement (per timeframe)

`past` needs `length` **complete prior sessions** at every bucket → first `length` sessions are NaN.

| TF | bars/RTH session | warmup bars (length=30) | note |
|---|---|---|---|
| 1m | 390 | **11,700** | 6,000 1m bars is **insufficient** (~15.4 sessions). Need ≥30 full sessions. |
| 5m | 78 | 2,340 | |
| 15m | 26 | 780 | |
| 1h | 7 (RTH) | 210 | |

Discard the first `length` sessions before any parity comparison. (Synthetic 40-session
1m run confirmed exactly 11,700 NaN rows.)

---

## 6. Validation recipe (≤0.5% vs TradingView live)

1. Pick 2–3 high-volume tickers (e.g. NVDA, AAPL, SPY).
2. In TradingView Desktop, add the **"Relative Volume at Time"** indicator (TV built-in, same
   `RelativeValue` engine) with `Length=30`, anchor `D`, set Cumulative ON for TNT-OD parity /
   OFF for Ultra-Combo parity, "Adjust for real-time bar" ON.
3. Read TV values via the MCP:
   - `mcp__tradingview__data_get_study_values` (the indicator's `Relative Volume` plot), or
   - `mcp__tradingview__data_get_pine_tables` if surfaced as a table.
   Also pull bars with `mcp__tradingview__data_get_ohlcv` (`summary=false`) for the same range.
4. Feed the **same OHLCV** (Massive S3 1m, RTH-filtered, NY tz) into `relative_volume()` with
   matching flags.
5. Align on timestamps; compute `abs(py.rvol - tv.rvol) / tv.rvol`.
   - **Discard** the first 30 sessions (warmup) and the **current/open bar** (realtime
     fraction depends on exact wall-clock; compare only closed bars for strict parity).
   - **Tolerance:** ≤0.5% median; investigate any closed-bar deviation >0.5%. Most residual
     comes from (a) RTH vs ETH session boundary, (b) data vendor volume differences
     (TV consolidated vs Massive), (c) half-day sessions shifting bucket counts.
6. If systematic offset appears, check session-start (TV uses the symbol's exchange session,
   not a hardcoded 09:30 — adjust `SESSION_START` / use exchange calendar for half-days).

---

## 7. Massive 2026-02-23 decimal-volume implication

Massive S3 flat-file size/volume columns are now **decimals (float)**, not ints. The module
casts `volume` to `float64` and uses an `EPS = 1e-9` guard on the ratio denominator so a
zero-volume bucket (illiquid open) can't divide-by-zero. No int truncation anywhere — cumsum
and means stay in float. Confirm ingestion preserves the decimals (don't `astype(int)` upstream).

---

## 8. Acceptance

- [x] Verbatim source contracts captured (signatures + both modes + realtime semantics).
- [x] Equations for cumulative + non-cumulative + realtime-adjust + return tuple.
- [x] Pure pandas module, runs under `uv` (40-session synthetic test passed).
- [x] Warmup math proven (11,700 NaN @ 1m/length=30).
- [x] Validation recipe via TV MCP, ≤0.5% closed-bar tolerance, warmup+open-bar discard.
- [x] Decimal-volume + ε handling documented.
