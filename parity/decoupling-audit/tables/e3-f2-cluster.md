# Decoupling Audit — `e3 f2 cluster THIS bull bear 58% reduction THIS` (shorttitle `f2 e3 58%`)

Source: `/Users/anishpatel/Desktop/Indicator studies/"e3 f2 cluster THIS bull bear 58% reduction THIS".txt` (387 lines, Pine v5, `overlay=true`).

## Verdict

**FULLY DECOUPLABLE. Zero blockers (no Class D), zero TV-library ports (no Class C).** Every one of the 8 detection plots is computable from Massive/Polygon OHLCV bars alone. The only non-pure-OHLCV machinery is (a) NY-session masking via `time(timeframe.period,"0930-1600","America/New_York")` (line 64), (b) calendar new-day detection via `ta.change(dayofmonth)` (lines 78, 100, 201), and (c) `barstate.isconfirmed` gating on the two FC-Cluster plots (lines 127, 138, 228, 239). All three are Class B — recreatable-with-effort using a tz-aware bar timestamp index and a closed-bar convention; none require any data Polygon doesn't provide. The `ta.*` surface is just `ta.atr(14)`, `ta.sma(...)`, and `ta.change(...)` (Class A math). `syminfo.ticker` (line 346) is cosmetic (alert string prefix only). The real parity risk is **not** data availability — it is **bar-for-bar reproduction of stateful path-dependent logic**: persistent counters (`sessBar`, `b1_s1/s2/s3`, run-length accumulators) and the rolling 20-bar overlap arrays (lines 140–177, 241–278). These must be replayed in strict chronological order with TV's exact session/DST and closed-bar semantics or the FC-Cluster outputs will diverge.

## Detection Plot Table

| Detection Plot | Line refs | What it detects | Series / inputs used | TV namespaces touched | Class | OHLCV sufficient? | Recreate risk | Notes / mitigation |
|---|---|---|---|---|---|---|---|---|
| **Bull FC Cluster** (`CLUSTER`, plotshape) | def 90–177, plot 300; deps: events 67–69, sessBar 76–88, sub-inds 93–114, overlap 116–177 | "2-of-3" bull cluster (MB-run, MBRETA-run, MB+RE session-run) **AND** a price-range overlap between a high-rVol "threshold" bar and a multi-bar bull "sequence" bar within a rolling 20-bar window | OHLC, volume; `atr14`, `avgVol20`, `avgDelta`, `trendMA`; `inSession`; `dayofmonth`; rolling `ta.sma` of body-spike & volume; arrays of bar_index/high/low | `ta.atr/sma/change`, `math.abs`, `time(timeframe.period,...)`, `dayofmonth`, `bar_index`, `barstate.isconfirmed`, `array.*`, `nz/na` | **B** | **Y** | **High** (stateful) | Path-dependent: persistent counters + two rolling 20-bar arrays + overlap geometry (`loA<=hiB and loB<=hiA`, line 159). Must replay bars in order with TV closed-bar + session semantics. See Flagged #1. |
| **Bull E3** (`E3`, plotshape) | def 180–183, plot 301 | 3rd in-session bar where bars 1,2,3 each fired a bull event (MB/RE/TA) | `sessBar`, `b2_ev`(=`bull_MB or bull_RE or bull_TA`) at `[0],[1],[2]` | `ta.*`, `math.abs`, session/`dayofmonth` (via sessBar), `inSession` | **B** | **Y** | Med | Depends on `sessBar==3`, so correct NY-session start + new-day reset required. Otherwise pure OHLCV. |
| **Bull First Two** (`F2`, plotshape) | def 186–188, plot 302 | 2nd in-session bar where bar 1 and bar 2 are both bull Marubozu (MB) | `sessBar`, `bull_MB` at `[0],[1]` | same as above | **B** | **Y** | Med | Same session-counter dependency as E3. |
| **Bear FC Cluster** (`BEAR CLUSTER`, plotshape) | def 191–278, plot 303; deps events 72–74 | Bear mirror of Bull FC Cluster; note bear sequence threshold `b4_sum >= 0.5` (line 239) vs bull `>= 0.1` (line 138), and bear base requires `bodyDn` in the diff filter (line 224) | OHLC, volume; same indicator set, bear-signed; arrays | same as Bull FC | **B** | **Y** | **High** (stateful) | Same as Bull FC; mind the asymmetric thresholds (0.5 vs 0.1) and the `bodyDn`-gated `b4_neg`. See Flagged #2. |
| **Bear E3** (`Bear E3`, plotshape) | def 281–284, plot 304 | 3rd in-session bar with bear event on bars 1,2,3 | `sessBar`, `b5_ev`(bear MB/RE/TA) `[0],[1],[2]` | `ta.*`, session/`dayofmonth` | **B** | **Y** | Med | Mirror of Bull E3. |
| **Bear First Two** (`Bear F2`, plotshape) | def 287–289, plot 305 | 2nd in-session bar, bars 1&2 both bear MB | `sessBar`, `bear_MB`[0],[1] | same | **B** | **Y** | Med | Mirror of Bull F2. |
| **Any Bull** (`ANY BULL`, plotshape) | def 294, plot 306 | OR of Bull FC/E3/F2 | `sBullFC or sBullE3 or sBullF2` | inherits | **B** | **Y** | High (inherits FC) | Pure boolean OR of the three above; risk inherited from Bull FC. |
| **Any Bear** (`ANY BEAR`, plotshape) | def 295, plot 307 | OR of Bear FC/E3/F2 | `sBearFC or sBearE3 or sBearF2` | inherits | **B** | **Y** | High (inherits FC) | Pure boolean OR; risk inherited from Bear FC. |

**Non-plot outputs (no shapes, completeness):** `sigMux` (313–322) MUX selector, `f_getAny()` (324–339) name picker, and `alert(...)` calls (346–386) are all functions of the 8 booleans above plus `syminfo.ticker` (cosmetic string). No new data dependency; not detection plots.

## Flagged dependencies (Class C / D)

**None.** No `tv_ta.*`, no `request.security`, no external/alt-data, no proprietary feeds. Class D blockers: **0**. Class C ports: **0**.

The items below are **Class B** — listed because they are the only places parity can silently break. They are not blockers, but they must be implemented deliberately.

### B-1 — NY session mask `inSession` (line 64)
- **Needs:** `time(timeframe.period, "0930-1600", "America/New_York")` returns non-`na` only for bars whose start time falls in 09:30–16:00 ET. Drives `inSession`, `sessBar`, and `b1_ev3/b4_ev3`.
- **Recreate avenue:** tz-aware timestamp per bar (Polygon agg `t` is ms epoch UTC → convert to `America/New_York` with a DST-correct tz library, e.g. `zoneinfo`). Mask `09:30 <= local_time < 16:00`. **DST is automatic in IANA tz** — do not hardcode a UTC offset.
- **Blast radius:** every plot except none — E3/F2 fully depend on it via `sessBar`; FC depends partially via `b1_ev3`. Wrong session edges shift the session-bar count and break E3/F2 directly.
- **Algorithm sketch:** `local = utc_from_ms(t).astimezone(NY); in_session = (local.time() >= 09:30) and (local.time() < 16:00)`. Match TV's bar-start-time convention (TV stamps a bar by its open time).

### B-2 — New-day detection `ta.change(dayofmonth)` (lines 78, 100, 201)
- **Needs:** detects calendar day rollover **in exchange/chart tz** to reset `sessBar` and `b1_s2/b4_s2`.
- **Recreate avenue:** `is_new_day = local_date != prev_local_date` using the same NY-local date as B-1. `ta.change(dayofmonth)!=0` is just "day-of-month differs from prior bar"; use full local date to be safe across month boundaries (TV's `dayofmonth` change also fires at month rollover — equivalent).
- **Blast radius:** session counters and the MBRETA daily-reset counter; affects all 8 plots.
- **Algorithm sketch:** carry `prev_day`; on first bar of a new NY date set the new-day flag, then run the `sessBar` state machine (lines 80–88).

### B-3 — `barstate.isconfirmed` gating (lines 127, 138, 228, 239)
- **Needs:** FC-Cluster threshold/sequence events only register on a **closed (confirmed) bar**.
- **Recreate avenue:** in a batch/historical Python pipeline over completed bars, every bar is "confirmed," so this is a **no-op for historical parity**. It only matters for a live/last-forming bar: do not emit FC threshold/sequence events on the still-forming current bar — gate on bar-closed.
- **Blast radius:** Bull/Bear FC Cluster (and Any Bull/Bear via inheritance) on the realtime edge only. Historical backfill is unaffected.
- **Algorithm sketch:** treat only finalized bars as event-eligible; suppress FC array pushes for the open bar.

### B-4 — `syminfo.ticker` (line 346) — cosmetic
- **Needs:** ticker symbol string for alert prefix only. No effect on any boolean/plot. Supply the symbol you're processing. Not a parity concern.

## Parity gotchas

1. **Session / DST boundary correctness (B-1, B-2).** Use IANA `America/New_York` so DST transitions (Mar/Nov) are automatic. Polygon timestamps are UTC ms — convert per bar, do not apply a fixed -5/-4. A one-bar session-edge error directly mis-numbers `sessBar`, which **breaks E3 (`sessBar==3`) and F2 (`sessBar==2`) deterministically**, not just statistically. Also confirm TV stamps bars by **open time** (it does) and match that, or the 09:30 and 16:00 edges land on the wrong bar.

2. **`barstate.isconfirmed` historical vs realtime (B-3).** On historical bars `isconfirmed` is always true → ignore for backfill. On the live forming bar it is false until close → FC events must not latch intrabar. If the Python "candle factory" recomputes on partial bars, FC Cluster will fire early vs TV. Gate FC event registration to closed bars only to match.

3. **`ta.atr(14)` seeding (lines 51).** Pine's `ta.atr` uses **RMA (Wilder) smoothing** of True Range, *not* SMA. TR uses `max(high-low, |high-close[1]|, |low-close[1]|)` with `close[1]`; the **first bar** has no prior close so TR seeds from `high-low` and RMA warms up over ~14 bars. Reproduce RMA exactly (`rma = (prev*(n-1)+tr)/n` after an initial SMA seed) and feed it the **same 6000-bar history window** — a different warmup start shifts `atr14` for early bars and flips `wide`/MB thresholds. With 6000 bars of lookback the steady-state is fine; only the leading edge of the window is at risk.

4. **`ta.sma` warmup & `[1]` offsets (lines 52–54, 118–124, 219–225).** Several SMAs are read at `[1]` (e.g. `ta.sma(b1_spk,30)[1]`, line 118) — i.e. the prior bar's 30-bar average, explicitly excluding the current bar. Replicate the one-bar lag precisely. SMAs over `na`-containing series (`b1_pos`, `b4_neg` are `na` when the diff is non-positive — lines 123, 224) follow Pine's rule: `ta.sma` over a series with `na` skips `na`s within the window in v5? **No — Pine `ta.sma` returns `na` until the window is full of valid values and treats `na` as breaking; verify against TV** using `data_get_study_values`. This is the subtlest parity trap: the `na`-gated positive/negative spike SMA (`b1_smaP`/`b4_smaN`) feeds the `b1_base`/`b4_base` gate. Reproduce Pine's exact `na`-handling for these conditional series or FC will drift.

5. **Stateful counters must be replayed in order.** `sessBar` (80–88), `b1_s1/b4_s1` (94/195), `b1_s2/b4_s2` (99–106/200–207), `b1_s3/b4_s3` (110–112/211–213), and FC run-length accumulators `b1_len/b1_sum` (130–138) / `b4_len/b4_sum` (231–239) are persistent `var` state. Any vectorized recompute must emulate the sequential `:=` updates exactly. Note `b1_s2` reset logic (lines 100–106): resets to 0 on new day OR when `b1_ev2` is false, then increments — order matters.

6. **Rolling 20-bar overlap arrays (140–177 / 241–278).** Threshold bars and sequence bars are stored with `bar_index/high/low`, pruned when `bar_index - stored > 20` (lines 149, 154), and overlap is the interval test `loA<=hiB and loB<=hiA` (line 159). `b1_ovlp` is set when a new threshold bar overlaps any stored sequence bar **or** a new sequence bar overlaps any stored threshold bar. Reproduce the prune window (`>20`, strict) and the push-order (threshold push happens before sequence push within a bar; both can run on the same bar) exactly, or FC Cluster diverges.

7. **Asymmetric bull/bear thresholds.** Bear sequence requires `b4_sum >= 0.5` (line 239) vs bull `b1_sum >= 0.1` (line 138), and `b4_neg` is additionally gated on `bodyDn` (line 224) whereas `b1_pos` is not body-gated (line 123). Do not assume the bear path is a pure sign-flip of the bull path — it is not.

8. **`nz`/`na` defaults.** `nz(b1_avgSpk,1)`/`nz(b1_avgVolD,1)` (lines 119–121) default to 1 to avoid div-by-zero during warmup; `nz(b1_pos)`/`nz(b1_smaP)` default to 0 (lines 125). Match these defaults or warmup-bar comparisons differ.

## Class tally
- Class A: 0 plots stand purely on A, but all A-machinery (`ta.atr/sma/change`, `math.*`) is present and trivially portable.
- **Class B: 8 / 8 detection plots** (session/calendar/barstate/stateful logic).
- Class C: 0.
- Class D: 0.

**Massive OHLCV is sufficient for 100% of detection plots.** No TradingView compute dependency remains once session-tz, new-day, closed-bar, RMA-ATR, and the stateful counters/arrays are faithfully ported.
