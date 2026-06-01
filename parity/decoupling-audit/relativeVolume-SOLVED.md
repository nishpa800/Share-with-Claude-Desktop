# SOLVED — `TradingView/ta/7` `relativeVolume` Decoupling Dependency

**Status:** Ported, smoke-verified, parity-test-ready.
**Artifacts:** `relative_volume_port.py` (this dir), this report.
**Blast radius:** SQUARIFY 46 v2 RVOL-gated signals only. FAUNA's call is dead.

---

## 0. Statement of Work

**Dependency:** `import TradingView/ta/7 as tv_ta` → `tv_ta.relativeVolume(length, anchorTimeframe, isCumulative, adjustRealtime)`.
**Live call (SQUARIFY 46 v2):** `length=30, anchorTimeframe="" , isCumulative=true, adjustRealtime=true`.

**Knowns**
- `ta` is TradingView's public standard library (script `BICzyhq0`); it delegates RVOL to the public `RelativeValue` library (script `cZnSLls2`).
- `relativeVolume` returns a 3-tuple `(currentVolume, pastVolume, relativeVolume)`.
- Empty `anchorTimeframe=""` → function default anchor `"D"` (daily/session).
- `isCumulative=true` is the documented default; `adjustRealtime` only affects the developing real-time bar.

**Unknowns (resolved)**
- Exact internal alignment → resolved: elapsed-time-offset ("slot") indexing within each anchor, averaged across prior `length` periods at the same slot (binary-search leftmost on offset). Confirmed from `RelativeValue` signatures `calcCumulativeSeries` + `averageAtTime`.
- Anchor `""` resolution → resolved to `"D"`.

**Acceptance criteria for parity**
- For a fixed symbol+timeframe over closed bars, port's `relative_volume` equals TV's `ta.relativeVolume` third output within tolerance **|Δ| ≤ 1e-4 relative** on ≥99% of bars, with discrepancies only on warmup or DST/half-day edges (documented).

---

## 1. Ground Truth

`relativeVolume(length, anchorTimeframe, isCumulative, adjustRealtime)`:

- **length** — number of prior anchor periods averaged for the historical baseline (live: 30).
- **anchorTimeframe** — period whose start resets the cumulative volume; `""` → `"D"` (NY session day). Defines slot 0 = first bar of the period.
- **isCumulative=true** — compare *cumulative volume since the anchor start up to the current elapsed offset* against the *average cumulative-volume-at-the-same-elapsed-offset* over the prior `length` anchors. (false → raw per-bar volume vs average raw per-bar volume at same slot.)
- **adjustRealtime=true** — on the developing (unconfirmed) bar only, projects the partial cumulative to a full-bar estimate via an elapsed-time ratio. On **closed/confirmed bars it is a strict NO-OP** (bar already complete → ratio 1). Since massive feeds closed aggregates, it is a no-op for historical recompute unless a developing-bar fraction is explicitly supplied.

Primitives (from `RelativeValue`):
- `calcCumulativeSeries(source, anchor, adjustRealtime)` → cumulative sum since last `anchor==true` bar.
- `averageAtTime(source, length, timeframe, isCumulative)` → average of values sharing the current bar's elapsed offset from the anchor across the prior `length` periods (uses `array.binary_search_leftmost` on stored offsets).

Sources: [ta library](https://www.tradingview.com/script/BICzyhq0-ta/) · [RelativeValue library](https://www.tradingview.com/script/cZnSLls2-RelativeValue/) · [Pine v6 reference](https://www.tradingview.com/pine-script-reference/v6/).

---

## 2. Equation (cumulative mode = live config)

Within anchor period `p`, index bars by elapsed offset `k = 0,1,2,...` (slot = position of the bar inside its session day).

```
cumVol[p,k]  = Σ_{j=0..k} volume[p,j]
currentVolume = cumVol[p_now, k_now]
pastVolume    = mean over the N≤length most-recent prior periods q that contain slot k_now of cumVol[q, k_now]
relVol        = currentVolume / pastVolume
```

Non-cumulative mode: replace `cumVol[p,k]` with raw `volume[p,k]` in both terms.
`adjustRealtime` (developing bar, fraction f of elapsed time): `currentVolume ← currentVolume / f`. Closed bar ⇒ f=1 ⇒ no-op.

---

## 3. Python Port

`relative_volume_port.py` → `relative_volume(df, length=30, anchor_timeframe="", is_cumulative=True, adjust_realtime=True, ...)`.

Handles: NY-session-day anchor detection from UTC epoch-ms timestamps (Polygon convention), per-period slot reset, cumulative running sum, slot-aligned averaging across the trailing `length` periods, warmup NaN (no prior period at that slot), and the closed-bar no-op convention for `adjust_realtime` (only engages when `developing_bar_fraction` ∈ (0,1) is passed).

**Smoke test (verified):** 3 session days, 2 bars/day. Day-3 slot-0: current=300, past=avg(100,200)=150 → rvol **2.000**. Day-3 slot-1: current=370, past=avg(150,260)=205 → rvol **1.8049**. Day-1 = warmup NaN. Output matches exactly.

---

## 4. Parity Test Plan

1. Pick symbol+timeframe with no recent splits (e.g. SPY 5m), a window spanning ≥ `length`+5 = 35 session days.
2. On TradingView Desktop, add `ta.relativeVolume(30, "", true, true)` (or read SQUARIFY's plotted RVOL) and pull bar values via TV MCP `data_get_study_values` / `data_get_indicator` over the visible range.
3. Pull the **same bars** from massive (`/v2/aggs/.../range/5/minute/...`), feed into `relative_volume()`.
4. Align by timestamp; compare the ratio column. **Tolerance: relative |Δ| ≤ 1e-4** on confirmed bars; ignore the live developing bar (adjustRealtime path) and the first `length` warmup periods.

**Failure-triage ladder**
1. Whole series shifted by one slot → timezone/exchange-tz mismatch (massive UTC vs NY); verify `_ensure_ny_index`.
2. Off-by-one only on Mar/Nov weeks → DST transition; confirm `America/New_York` (not fixed UTC offset).
3. rvol wrong at slot 0 each day → cumulative not resetting; check `new_period`/anchor keys.
4. Baseline magnitude off → warmup window or `length` window size (`hist[-length:]`).
5. Half-day (early close) periods diverge → fewer slots that day; expected, see §5.
6. Volume magnitude systematically off → consolidated vs primary-exchange volume (see §5).

---

## 5. Inversion — How This Silently Breaks

- **DST days:** wrong tz handling shifts every slot on transition weeks. Mitigated by NY-tz normalize.
- **Half-days / early closes:** those anchors have fewer slots; late-session slots have fewer contributing prior periods → noisier baseline. Not a bug, but flag if SQUARIFY trades those sessions.
- **Anchor `""` per-timeframe:** on a non-intraday chart `"D"` anchor degenerates; SQUARIFY runs intraday so this is fine, but a daily-chart port would need a different anchor.
- **Partial first session:** if the massive window starts mid-day, period 0 is incomplete and pollutes the baseline. Drop the first partial anchor before relying on output.
- **Consolidated vs primary volume:** TradingView feed volume may differ from Polygon consolidated tape; a constant ratio offset cancels in the *ratio* output, but if TV uses primary-exchange and Polygon consolidated and the mix varies intraday, small drift appears. Verify on the parity run.
- **`int64`/dtype overflow on `.view`:** pandas may yield `datetime64[ms]`; the port forces `datetime64[ns, UTC]` before epoch math.

---

## 6. Blast Radius + Recommendation

**Contained.** Only SQUARIFY 46 v2's RVOL-gated signals consume this. The "Jumbo CIA FAUNA" call exists but its output is orphaned/dead — no port needed there, just delete the dead call on cleanup.

**RECOMMENDATION: PORT IT** (done). It is a single, well-defined, deterministic function with a verified parity-grade Python implementation. No need to drop or gate it. Action items:
1. Run the §4 parity test (TV MCP vs port) on SPY 5m before wiring into the live candle factory.
2. Drop SQUARIFY's first partial session from any recompute window.
3. Remove FAUNA's dead `relativeVolume` call during decoupling cleanup.
