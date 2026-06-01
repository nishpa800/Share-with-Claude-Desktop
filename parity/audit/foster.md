# Pine→Python Parity Audit — "Anish TB Foster Fix"

**Source file (canonical):** `/Users/anishpatel/Desktop/Indicator studies/"Anish TB Foster Fix",.txt`
*(Note: the on-disk filename literally begins with a double-quote character: `"Anish TB Foster Fix",.txt`. The macOS Desktop folder blocks `os.listdir`/`ls` via TCC even with the sandbox disabled, so the file was located via Spotlight `mdfind` and read from the byte-identical mirror at `/Users/anishpatel/code/anish/indicators/imports/20260531T103840_indicator_studies/originals/anish_tb_foster_fix.txt`.)*

**Pine version:** v6 — `indicator("Anish TB Foster Fix", overlay=true, max_bars_back=2000)`
**Actual file length:** **221 lines** (not 2253; the "~2253 lines / 6 barstate / 116 ta.* / ~150 drawing calls" recon profile does NOT match this file — those numbers belong to a different/aggregate indicator. This file has 7 `ta.*` call-sites across 3 distinct functions, 0 barstate, 28 drawing/alert outputs.)
**Audit date:** 2026-05-31

---

## VERDICT (one paragraph)

**NO EXTERNAL DEPENDENCY — fully reproducible from the OHLCV candle factory.** "Anish TB Foster Fix" is a self-contained Stage-Analysis + Pocket-Pivot confluence indicator. It computes three EMAs (50/150/200) and 52-week high/low channels to define "Anish Bull" (Stage-2 uptrend) and "Anish Bear" (Stage-4 downtrend) gates, a volume-based Pocket Pivot (PUP/PPD), gap detection, and a set of stateful sequence detectors (TB/Foster window logic, Back-to-Back, and 1st-Pass-from-neutral). Every input dereferences to open/high/low/close/volume plus exactly three `ta.*` primitives: `ta.ema`, `ta.highest`, `ta.lowest`. Verified counts on the real source: **0** `request.*`, **0** `syminfo.*`, **0** `security()`, **0** `barstate.*`, **0** `timenow`/`dividends`/`earnings`/`splits`, **0** `vwap`, **0** `timeframe`, **0** `math.*`. There are 14 `plotshape` outputs and 14 `alertcondition` outputs (28 total signal surfaces, all firing on booleans). Every output is **REPRODUCIBLE_WITH_WARMUP** — the only parity caveat is recursive EMA seeding (`ta.ema` 50/150/200) and a 252-bar `ta.highest`/`ta.lowest` channel that need adequate history, plus several Pine `var` state machines that must be replicated bar-by-bar from a deterministic start.

---

## SUMMARY COUNT TABLE

| Metric | Count |
|---|---|
| Total distinct plot/signal outputs | 28 (14 plotshape + 14 alertcondition; the alerts mirror the plots → 14 unique signal series) |
| Unique signal series | 14 |
| PURE_OHLCV (data dependency) | 14 / 14 |
| NEEDS_USER_INPUT_ONLY (params only, no data dep) | all also take user inputs (barSize, ppLookback, gap flags, minAnishBars, followUpBars, neutralBarsRequired) |
| REPRODUCIBLE (no warmup concern) | 0 strictly — all transitively touch EMA200[21] / 252-bar channel |
| REPRODUCIBLE_WITH_WARMUP | 14 / 14 |
| BARSTATE_LIVE_ONLY | 0 |
| BLOCKED / EXTERNAL_DEPENDENCY | 0 |

Data-dependency class for every signal = **PURE_OHLCV**. Parity status for every signal = **REPRODUCIBLE_WITH_WARMUP**.

---

## FOUNDATION SERIES (intermediates feeding all signals) — all PURE_OHLCV

| Series | Line | Equation |
|---|---|---|
| `ema50/ema150/ema200` | 19 | `ta.ema(close, 50/150/200)` |
| `ema200_1m` | 20 | `ema200[21]` (EMA200 value 21 bars ago — approximates "1 month ago" slope reference) |
| `w52Hi / w52Lo` | 21 | `ta.highest(high, 252)` / `ta.lowest(low, 252)` |
| `bullPass` (Anish Bull) | 24 | `close>ema50 ∧ close≥ema150 ∧ close≥ema200 ∧ ema50>ema150 ∧ ema50>ema200 ∧ ema150≥ema200 ∧ ema200>ema200_1m ∧ close>1.30·w52Lo ∧ close≥0.75·w52Hi` |
| `bearPass` (Anish Bear) | 27 | mirror with `<`/`≤`: `… ∧ ema200<ema200_1m ∧ close<0.70·w52Hi ∧ close≤1.25·w52Lo` |
| `redVol/greenVol` | 30–31 | `close<open ? volume : 0` / `close>open ? volume : 0` |
| `hiRedVol/hiGreenVol` | 32–33 | `ta.highest(redVol[1], ppLookback)` / `ta.highest(greenVol[1], ppLookback)` (prior-bar offset) |
| `priceUp/priceDn` | 35–36 | `((close−open)/open)·100 > barSize` / `((open−close)/open)·100 > barSize` |
| `volBull/volBear` | 37–38 | `volume > hiRedVol` / `volume > hiGreenVol` |
| `sPPBull/sPPBear` | 40–41 | `priceUp ∧ volBull` / `priceDn ∧ volBear` |
| `gapUp/gapDn` | 44–45 | `open > close[1]·(1+gapValue/100)` / `open < close[1]·(1−gapValue/100)` |

---

## PER-SIGNAL TABLE

| # | Signal (Pine title) | Line | Equation (dereferenced to OHLCV + ta) | Inputs (O/H/L/C/V + ta + user) | Dependency | Parity Status | Notes |
|---|---|---|---|---|---|---|---|
| 1 | Pocket Pivot Bull (PUP) | 186 | `sPPBull = priceUp ∧ volume>highest(redVol[1],ppLookback)` | C,O,V; ta.highest; barSize, ppLookback | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | needs ppLookback+1 bars. triangleup, text "PUP". |
| 2 | Pocket Pivot Bear (PPD) | 187 | `sPPBear = priceDn ∧ volume>highest(greenVol[1],ppLookback)` | C,O,V; ta.highest; barSize, ppLookback | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | triangledown, "PPD". |
| 3 | Anish Bull | 188 | `bullPass` (see foundation) | C,H,L; 3×ta.ema, ta.highest(252), ta.lowest(252) | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | needs ≥273 bars (252 channel + 21-bar EMA offset) and EMA warmup. diamond. |
| 4 | Anish Bear | 189 | `bearPass` | same as #3 | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | diamond. |
| 5 | All Three Bull | 190 | `sAllBull = sPPBull ∧ gapUpSig ∧ bullPass`; `gapUpSig = gapUpEnabled ∧ gapUp` | #1 ∧ #3 ∧ gap; gapUpEnabled, gapValue | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | circle. Default gapUpEnabled=false ⇒ never fires unless user enables. |
| 6 | All Three Bear | 191 | `sAllBear = sPPBear ∧ gapDnSig ∧ bearPass` | #2 ∧ #4 ∧ gap | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | circle. gapDownEnabled default false. |
| 7 | Super Pup (S-PUP) | 194 | `superPup = sPPBull ∧ bullPass` | #1 ∧ #3 | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | labelup, "S-PUP". |
| 8 | Super PPD (S-PPD) | 195 | `superPPD = sPPBear ∧ bearPass` | #2 ∧ #4 | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | labeldown, "S-PPD". |
| 9 | Foster Buy | 196 | Stateful: open window when a bearPass run ≥ minAnishBars ends; within followUpBars bars, fire if `sPPBull`; cancel if bearPass returns or window expires | #2,#4 history; minAnishBars, followUpBars | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | `var fosterWindowOpen/Count`, `var consecAnishBear`. Replicate state machine exactly (lines 95–131). labelup, "FOSTER". |
| 10 | TB Sell | 197 | Mirror: open window when a bullPass run ≥ minAnishBars ends; within followUpBars, fire if `sPPBear`; cancel on bullPass/expiry | #1,#3 history; minAnishBars, followUpBars | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | `var tbWindowOpen/Count`, `var consecAnishBull` (lines 57–93). labeldown, "TB". |
| 11 | B2B PUP | 200 | `b2bPUP = sPPBull ∧ sPPBull[1]` | #1 and its 1-bar lag | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | labelup, "B2B PUP". |
| 12 | B2B PPD | 201 | `b2bPPD = sPPBear ∧ sPPBear[1]` | #2 and lag | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | labeldown, "B2B PPD". |
| 13 | 1st PUP Pass | 202 | Stateful: count neutral bars (`¬bullPass ∧ ¬bearPass`); after ≥ neutralBarsRequired set neutralPhaseComplete; arm on `sPPBull`; disarm on bearPass; fire `pupArmed ∧ bullPass ∧ ¬bullPass[1]`; reset after fire | #1,#3,#4 history; neutralBarsRequired | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | `var neutralBarCount/neutralPhaseComplete/pupArmed` (lines 137–164). labelup, "1st PUP". |
| 14 | 1st PPD Pass | 203 | Mirror: arm `ppdArmed` on `sPPBear` after neutral phase; disarm on bullPass; fire `ppdArmed ∧ bearPass ∧ ¬bearPass[1]`; reset | #2,#3,#4 history; neutralBarsRequired | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | `var ppdArmed` (lines 166–183). labeldown, "1st PPD". |

**Alerts (lines 206–219):** 14 `alertcondition` calls fire on exactly the 14 booleans above (PUP, PPD, Anish Bull, Anish Bear, All Three Bull/Bear, Super Pup/PPD, Foster, TB, B2B PUP/PPD, 1st PUP/PPD Pass). No new logic — same parity status as their source signal.

---

## DISTINCT `ta.*` FUNCTIONS + WARMUP-RISK FLAGS

| ta function | Call sites | Recursive? | Warmup-seeding parity risk | Mitigation |
|---|---|---|---|---|
| `ta.ema` | 3 (len 50,150,200) | YES (infinite-memory) | MEDIUM–HIGH | TV seeds EMA's first value with SMA(len) then `α=2/(len+1)`. Replicate that seed; with len=200 plus the `[21]` offset, discard ≥ ~221+ warmup bars (recommend ≥ 600 for ema200 to converge tightly). |
| `ta.highest` | 3 (len 252 on high; len ppLookback on redVol[1]/greenVol[1]) | No (windowed max) | LOW | Needs `len` bars in window; note the `[1]` prior-bar offset on the Pocket-Pivot volume channels — replicate exactly. |
| `ta.lowest` | 1 (len 252 on low) | No (windowed min) | LOW | Needs 252 bars. |

No `ta.rma / ta.rsi / ta.atr / ta.sma / ta.barssince / ta.valuewhen / ta.crossover / ta.crossunder` are used in this file. The classic recursive-seeding traps (RMA/RSI/ATR) are therefore ABSENT; the only recursive primitive is `ta.ema`.

**Pine `var` state machines to replicate bar-by-bar (not ta functions, but stateful → recursion-from-bar-0):**
- `consecAnishBull`, `consecAnishBear` (run-length counters)
- `tbWindowOpen/tbWindowCount`, `fosterWindowOpen/fosterWindowCount` (TB/Foster windows)
- `neutralBarCount`, `neutralPhaseComplete`, `pupArmed`, `ppdArmed` (1st-Pass arming)

These must be initialized identically (all 0/false) and driven on the same bar sequence; they are the highest-fidelity risk for parity because a single missed/extra bar shifts every downstream window. Unit-test them with golden sequences.

---

## TIMEFRAME-TOKEN RESOLUTION

`grep -ci timeframe` on the real source = **0**. There is no `timeframe` token in any form — no `request.security(..., timeframe.period, ...)`, no `input.timeframe`, no comment/string/variable using the word. **No multi-timeframe dependency exists.** Note: line 20 `ema200_1m` and line 13's tooltip mention "1 month"/"Window Bars" conceptually, but `ema200_1m = ema200[21]` is purely a 21-bar historical offset on the chart's own timeframe (21 trading days ≈ 1 month on a daily chart) — it is NOT a higher-timeframe request. The indicator runs entirely on the chart's native timeframe; reproduction needs only single-timeframe Massive OHLCV aggregates.

---

## CROSS-CUTTING PARITY NOTES

1. **Data inputs = O,H,L,C,V only.** All sourceable from Massive aggregates (e.g. `/v2/aggs/ticker/{t}/range/...`). Massive's 2026-02-23 decimal volume change is fine — volume enters only via comparisons and conditional sums (`redVol/greenVol`), so decimals are exact.
2. **No live-only constructs.** Zero `barstate.*`; nothing is LIVE_ONLY. Full historical backfill reproduces every signal; no repaint concern (no pivots, no security lookahead).
3. **Warmup budget:** the binding constraint is `ta.lowest/highest(252)` AND `ema200[21]` → first valid `bullPass/bearPass` needs ≥ 273 bars, and EMA200 needs additional warmup to converge. Discard ≥ 600 leading bars before scoring parity to be safe; below that, EMA divergence will flip Anish Bull/Bear gates.
4. **EMA seeding is the only recursive-ta risk.** Match TradingView's SMA-seed-then-EMA convention; an off-spec seed produces a slowly-decaying offset that can flip the boundary `≥`/`>` comparisons in #3/#4.
5. **Stateful sequence detectors (#9, #10, #13, #14) are deterministic but order-sensitive.** They depend on prior-bar booleans and `var` accumulators; port them as an explicit per-bar loop, not a vectorized expression, and verify with golden-bar fixtures. The `[1]` lags in #11/#12/#13/#14 (`sPPBull[1]`, `¬bullPass[1]`, `¬bearPass[1]`) must use the prior bar's value, not the current.
6. **Default-off gaps:** #5/#6 (All Three) require `gapUpEnabled`/`gapDownEnabled`, both default `false` → they never fire under default settings. The Python port must expose these as parameters to match user-enabled behavior.

**Conclusion:** NO EXTERNAL DEPENDENCY — fully reproducible from the candle factory. No DEPENDENCY RESOLUTION section required (no Massive substitute needed; no recon lookup necessary).
