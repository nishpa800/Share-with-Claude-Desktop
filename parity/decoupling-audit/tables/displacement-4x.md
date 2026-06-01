# Decoupling Audit — Displacement 4x ("DISP 4x")

Source file: `/Users/anishpatel/Desktop/Indicator studies/"Displacement 4x", shorttitle="DISP 4x".txt`
Audited: 2026-05-31 · Lines audited: 1–120

## Verdict

**Fully decouplable. Zero blockers (no Class D).** This indicator is four structurally identical "displacement + FVG" engines (D1–D4) differing only by std-dev multiplier (6.5 / 6.0 / 5.5 / 5.0), shape, and plot location. Every detection plot is computed purely from raw OHLCV via `math.abs`, subtraction, comparison, and a single `ta.stdev` call — all Class A. The only non-pure-math touch is `barstate.isconfirmed` (line 23), a Class B realtime-vs-confirmed gate that is trivial in Python because the candle factory only emits closed bars (so `conf` is always true on reconstructed history; it merely suppresses the live forming bar in TV). There is no `request.security`, no `tv_ta`, no session/time/calendar logic, no `syminfo.mintick`, no external feed. Massive OHLCV (5 TFs, 6000 bars) is sufficient for 1:1 recreation of all 8 signal outputs. Overall recreate risk: **Low**.

## Detection Plot Table

| Detection Plot | Line refs | What it detects | Series/inputs used | TV namespaces touched | Class | Massive OHLCV sufficient? | Recreate risk | Notes / mitigation |
|---|---|---|---|---|---|---|---|---|
| D1 Bull | 35–42, 44 | Prior bar was a bullish displacement (range[1] > stdev×6.5) followed by a confirmed bullish FVG | open, close, high, low; `d1_rng`=abs(open−close) or high−low; `ta.stdev(rng,100)`×6.5; `low>high[2] and close[1]>open[1]`; `barstate.isconfirmed` | `ta.stdev`, `math.abs`, `barstate.isconfirmed`, `plotshape` | A (B for conf gate) | Y | stdev sample/pop convention must match TV (see gotchas); offset=-1 is a visual shift only |
| D1 Bear | 35–40, 43, 45 | Prior bullish-magnitude displacement followed by confirmed bearish FVG (`high<low[2] and close[1]<open[1]`) | same as D1 Bull, bear FVG | same | A (B) | Y | mirror of D1 Bull |
| D2 Bull | 59–65, 68 | Same engine, mult 6.0, plotted bottom | OHLC; `ta.stdev(rng,100)`×6.0; bull FVG; conf | `ta.stdev`, `math.abs`, `barstate.isconfirmed`, `plotshape` | A (B) | Y | identical logic to D1, different multiplier/location |
| D2 Bear | 59–64, 66, 69 | Mult 6.0, bear FVG, bottom | OHLC; ×6.0; bear FVG; conf | same | A (B) | Y | — |
| D3 Bull | 83–89, 92 | Mult 5.5, xcross, top | OHLC; `ta.stdev(rng,100)`×5.5; bull FVG; conf | same | A (B) | Y | — |
| D3 Bear | 83–88, 90, 93 | Mult 5.5, bear FVG, top | OHLC; ×5.5; bear FVG; conf | same | A (B) | Y | — |
| D4 Bull | 107–113, 116 | Mult 5.0, cross, bottom | OHLC; `ta.stdev(rng,100)`×5.0; bull FVG; conf | same | A (B) | Y | — |
| D4 Bear | 107–112, 114, 117 | Mult 5.0, bear FVG, bottom | OHLC; ×5.0; bear FVG; conf | same | A (B) | Y | — |
| alertcondition D1–D4 Bull/Bear | 46–47, 70–71, 94–95, 118–119 | Alert triggers mirroring the 8 boolean signals | same booleans `dN_bull`/`dN_bear` | `alertcondition` | A (B) | Y | not visual plots; same booleans, no extra compute. Recreate as event emits |

## Flagged Dependencies (Class C / D)

**None.** No Class C (`tv_ta.*`) and no Class D (external/proprietary/seed/`request.security`) dependencies exist in this file. The only non-Class-A item is the `barstate.isconfirmed` gate (Class B, line 23), detailed below — it is not a blocker.

### Class B note — `barstate.isconfirmed` (line 23, blast radius = all 8 plots + 8 alerts)
- **What it needs:** the gate ensures a signal only fires on a *closed* bar, not on the live forming bar.
- **Recreate avenue:** The Python candle factory builds from completed massive aggregate bars, so every reconstructed bar is already "confirmed." Set `conf = True` for all historical/closed bars. For any live/forming bar in a real-time path, set `conf = False` (or only emit on bar close) to match TV exactly.
- **Equation sketch:** `conf := bar_is_closed`. In batch recompute over the 6000-bar history, `conf ≡ True`, so the gate is a no-op for parity testing.

## Parity Gotchas

1. **`ta.stdev` is POPULATION stdev (divides by N), not sample (N−1).** TV's `ta.stdev` uses the biased/population formula. Use `numpy.std(x, ddof=0)` or pandas `.std(ddof=0)` over the rolling 100-bar window — NOT the default pandas `.std()` (ddof=1). This is the single highest-risk parity item: getting ddof wrong shifts every threshold and flips edge-case signals. (Lines 36, 60, 84, 108.)
2. **Rolling-window warmup.** `ta.stdev(rng, 100)` needs 100 prior values of `rng`; `d1_prevDisp` reads `[1]` and FVG reads `[2]`. The first valid signal can only occur at bar index ≥ 101. With 6000 bars this is negligible, but per-timeframe the first ~101 bars must be discarded for parity. TV begins outputting `na` until the window fills — replicate by emitting no signal until ≥100 `rng` samples exist.
3. **`offset=-1` is a pure visual shift.** The signal boolean is computed on bar[0] (FVG confirmation bar) but plotted under bar[1] (the displacement candle). For data parity, store the signal on the confirmation bar timestamp and apply −1 shift only at the visual layer. Do NOT bake the −1 into the boolean — the header comment (lines 7–10) explicitly says combo systems must compare against bar[1] (the plotted candle), so be deliberate about which bar your downstream join keys on.
4. **`rng` definition branches on input.** Default `"Open to Close"` → `abs(open−close)`; alt `"High to Low"` → `high−low` (lines 35/59/83/107). Parity requires reading the actual input state per engine, not assuming the default. All four default to Open-to-Close.
5. **Continuous multiplier, no bucketing.** Header (lines 13–16) stresses the threshold is `stdev × mult` with no rounding. Use full float precision; do not round threshold or `rng` to mintick. There is NO `syminfo.mintick` in this file, so no tick-rounding parity concern — keep raw floats.
6. **FVG `[2]` gap definition.** Bull FVG: `low > high[2] and close[1] > open[1]`. The gap is measured current-low vs high two bars back, with the middle bar[1] required to be the displacement candle of the correct color. Index alignment of `[1]`/`[2]` must match exactly; off-by-one here silently breaks every signal.
7. **Realtime repaint:** because of `barstate.isconfirmed`, TV does not repaint these — they lock on close. The Python side must likewise only finalize on bar close to be bar-for-bar identical; an intrabar recompute would show a signal TV never plotted.
