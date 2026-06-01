"""
Parity-grade Python port of TradingView/ta/7 ``relativeVolume()``.

Source of truth: TradingView's public ``ta`` standard library (script BICzyhq0)
which delegates to the ``RelativeValue`` library (script cZnSLls2). The
relevant primitives are:

    calcCumulativeSeries(source, anchor, adjustRealtime)
        -> cumulative sum of `source` since the last bar where `anchor` was
           true. `adjustRealtime` estimates a projected close value on the
           developing (unconfirmed) bar from a value-to-time ratio.

    averageAtTime(source, length, timeframe, isCumulative)
        -> for the CURRENT bar's elapsed-time-offset from its anchor start,
           gather the value at the SAME elapsed offset in each of the prior
           `length` anchor periods and average them (binary-search by elapsed
           offset, leftmost match).

    relativeVolume(length, anchorTimeframe, isCumulative, adjustRealtime)
        currentVolume = calcCumulativeSeries(volume, anchor, adjustRealtime)   (cumulative mode)
                      = volume                                                  (non-cumulative)
        pastVolume    = averageAtTime(<that series>, length, anchorTimeframe, isCumulative)
        return (currentVolume, pastVolume, currentVolume / pastVolume)

SQUARIFY 46 v2 live config: length=30, anchorTimeframe="" (auto -> "D" daily/
session anchor), isCumulative=true, adjustRealtime=true.

EQUATION (cumulative mode, the live config)
-------------------------------------------
Let bars within an anchor period p be indexed by elapsed offset k = 0,1,2,...
(k = number of completed bars of that timeframe since the anchor's start;
equivalently the slot index of the bar inside the session day).

    cumVol[p, k]   = sum_{j=0..k} volume[p, j]              (cumulative volume to slot k of period p)
    currentVolume  = cumVol[p_now, k_now]
    pastVolume     = (1/N) * sum over the N most-recent prior periods q (N<=length)
                            that HAVE a bar at slot k_now, of cumVol[q, k_now]
    rvol           = currentVolume / pastVolume

Non-cumulative mode replaces cumVol[p,k] with the raw volume[p,k] in both
currentVolume and pastVolume.

adjustRealtime: on the last (developing) bar of a real-time feed, currentVolume
is scaled up to a projected full-bar value via elapsed-time ratio. On CLOSED /
confirmed bars it is a strict NO-OP (the bar is already complete, ratio == 1).
Because we port from massive.com aggregates where every fed bar is a closed
aggregate, adjustRealtime is a no-op here unless the caller explicitly marks a
developing bar via `developing_bar_fraction`.

Author: decoupling-audit
"""

from __future__ import annotations

import numpy as np
import pandas as pd

NY_TZ = "America/New_York"


def _ensure_ny_index(df: pd.DataFrame, timestamp_col: str) -> pd.DataFrame:
    """Return a copy with a tz-aware America/New_York DatetimeIndex.

    Massive/Polygon timestamps are UTC (epoch ms or tz-aware). We convert to
    New_York so the *session day* anchor and DST handling are correct.
    """
    out = df.copy()
    ts = out[timestamp_col]
    if np.issubdtype(ts.dtype, np.integer) or np.issubdtype(ts.dtype, np.floating):
        # epoch milliseconds (Polygon flat-file / aggregate convention)
        ts = pd.to_datetime(ts, unit="ms", utc=True)
    else:
        ts = pd.to_datetime(ts, utc=True)
    out = out.assign(_ts=ts.dt.tz_convert(NY_TZ)).set_index("_ts")
    return out.sort_index()


def _anchor_keys(idx: pd.DatetimeIndex, anchor: str) -> np.ndarray:
    """Map each bar to its anchor-period id.

    anchor="" or "D" -> the New_York calendar (session) day. This matches
    TradingView's default "D" anchor: cumulative volume resets at each new
    trading day. Other anchors ("W","M") supported for completeness.
    """
    if anchor in ("", "D"):
        return idx.normalize().view("int64")  # midnight-NY of each day
    if anchor == "W":
        return (idx.isocalendar().year.values * 100 + idx.isocalendar().week.values)
    if anchor == "M":
        return idx.year.values * 100 + idx.month.values
    raise ValueError(f"Unsupported anchorTimeframe: {anchor!r}")


def relative_volume(
    df: pd.DataFrame,
    length: int = 30,
    anchor_timeframe: str = "",
    is_cumulative: bool = True,
    adjust_realtime: bool = True,
    volume_col: str = "volume",
    timestamp_col: str = "timestamp",
    developing_bar_fraction: float | None = None,
) -> pd.DataFrame:
    """Reproduce TradingView ``ta.relativeVolume`` bar-for-bar.

    Parameters
    ----------
    df : intraday OHLCV bars, one row per bar, ascending time. Must contain
         `volume_col` and `timestamp_col`.
    length : number of PRIOR anchor periods averaged (live: 30).
    anchor_timeframe : "" (auto -> daily/session), "D", "W", or "M".
    is_cumulative : cumulative-since-anchor mode (live: True).
    adjust_realtime : project the developing bar to a full bar (no-op on
        closed bars; live: True). Only takes effect on the FINAL row and only
        if `developing_bar_fraction` in (0,1] is supplied.
    developing_bar_fraction : fraction of the developing bar's time already
        elapsed (0<f<=1). None => treat every bar as closed (no-op).

    Returns
    -------
    DataFrame indexed like the input order with columns:
        current_volume, past_volume, relative_volume, slot, anchor_id
    `past_volume`/`relative_volume` are NaN during warmup (fewer than 1 prior
    period available at that slot).
    """
    if length < 1:
        raise ValueError("length must be >= 1")

    work = _ensure_ny_index(df, timestamp_col)
    vol = work[volume_col].astype(float).to_numpy()
    n = len(work)
    if n == 0:
        return pd.DataFrame(
            columns=["current_volume", "past_volume", "relative_volume", "slot", "anchor_id"]
        )

    anchor_ids = _anchor_keys(work.index, anchor_timeframe)

    # slot = elapsed-offset index of the bar within its anchor period (0-based).
    # Computed as a running counter that resets when the anchor id changes.
    slot = np.empty(n, dtype=np.int64)
    new_period = np.empty(n, dtype=bool)
    counter = -1
    prev_anchor = None
    for i in range(n):
        if anchor_ids[i] != prev_anchor:
            counter = 0
            new_period[i] = True
            prev_anchor = anchor_ids[i]
        else:
            counter += 1
            new_period[i] = False
        slot[i] = counter

    # current_volume series
    if is_cumulative:
        current = np.empty(n, dtype=float)
        running = 0.0
        for i in range(n):
            running = vol[i] if new_period[i] else running + vol[i]
            current[i] = running
    else:
        current = vol.copy()

    # past_volume = average of the SAME series at the SAME slot across the
    # prior `length` anchor periods that contain that slot.
    # Build, per slot, the ordered history of period-values as we stream.
    slot_history: dict[int, list[float]] = {}
    past = np.full(n, np.nan, dtype=float)
    for i in range(n):
        s = int(slot[i])
        hist = slot_history.get(s)
        if hist:  # average over up to `length` most-recent prior periods
            window = hist[-length:]
            past[i] = float(np.mean(window))
        # append THIS period's value at this slot for future bars
        if hist is None:
            slot_history[s] = [current[i]]
        else:
            hist.append(current[i])

    # adjust_realtime: only the final, developing bar, only in cumulative mode.
    if adjust_realtime and is_cumulative and developing_bar_fraction:
        f = float(developing_bar_fraction)
        if 0.0 < f < 1.0:
            current[-1] = current[-1] / f  # project to full-bar value

    ratio = np.divide(
        current, past, out=np.full(n, np.nan), where=(past > 0) & ~np.isnan(past)
    )

    return pd.DataFrame(
        {
            "current_volume": current,
            "past_volume": past,
            "relative_volume": ratio,
            "slot": slot,
            "anchor_id": anchor_ids,
        },
        index=range(n),
    )


if __name__ == "__main__":
    # tiny smoke test: 3 days, 2 bars/day, constant daily pattern
    ts = pd.to_datetime(
        [
            "2026-01-02 09:30", "2026-01-02 09:31",
            "2026-01-05 09:30", "2026-01-05 09:31",
            "2026-01-06 09:30", "2026-01-06 09:31",
        ]
    ).tz_localize(NY_TZ).tz_convert("UTC")
    # epoch milliseconds (Polygon/massive convention)
    epoch_ms = (ts.astype("datetime64[ns, UTC]").astype("int64") // 1_000_000).astype("int64")
    demo = pd.DataFrame(
        {"timestamp": epoch_ms, "volume": [100, 50, 200, 60, 300, 70]}
    )
    out = relative_volume(demo, length=30, is_cumulative=True, adjust_realtime=True)
    print(out)
    # day3 slot0 current=300, past=avg(100,200)=150 -> rvol=2.0
    # day3 slot1 current=370, past=avg(150,260)=205 -> rvol~1.805
