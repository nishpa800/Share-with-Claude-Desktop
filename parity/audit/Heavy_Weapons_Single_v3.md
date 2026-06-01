# Parity Audit — Heavy Weapons Single v3

**File:** `/tmp/IND_HW.txt` (1138 lines, read in full)
**Indicator:** `Heavy Weapons Single v3` (shorttitle `HW Single v3`)
**Auditor goal:** Determine whether every detection plot / signal can be reproduced EXACTLY from Massive minute-aggregate OHLCV(+volume) candles alone, or whether any plot requires data TradingView supplies that local candles do not.

---

## 1. Declaration & Environment

| Field | Value | Line |
|---|---|---|
| `@version` | **5** (Pine v5, NOT v6) | 1 |
| `indicator()` | `"Heavy Weapons Single v3"`, `shorttitle="HW Single v3"` | 2 |
| `overlay` | **true** | 2 |
| `max_bars_back` | **5000** | 2 |
| Library import | `import TradingView/ta/7 as tv_ta` | 4 |

**v5-specific semantics confirmed:** uses `barstate.isconfirmed` (`conf`, line 276), `var` series state (sequence/streak/maxVol accumulators), `nz()` warmup guards. No v6-only constructs. No `request.*`, no `syminfo.*`, no `timeframe.change`, no `time`/session/`dayofweek` usage. `timeframe.in_seconds()` (149) and `timeframe.period` (1082) are pure metadata — they select hardcoded threshold ladders by bar duration, fully reproducible from knowing the bar TF.

**THE ONE EXTERNAL DEPENDENCY:** `tv_ta.relativeVolume()` from the official `TradingView/ta/7` library (lines 288, 298, 299). This is a *library call*, not raw OHLCV math — its internals are NOT in this file. It is the single biggest parity risk and is analyzed in full in §4.

---

## 2. STATUS TABLE — Every Detection Plot / Signal / Decision Cell

### A. plotshape detection signals (45 plotshape calls)

| Detection Plot / Cell | Fires on (1-line math) | Inputs | Status | Parity Risk | Mitigation |
|---|---|---|---|---|---|
| **SAAB +LONG** (864) | `bb_normalizedPrice ∈ [th_saab, th_1x)` & close>open & posDiff>smaDiff & anyLong | OHLC, vol, SMA30, SMA20 | GREEN | none | sma+abs+nz, warmup `bb_avgLength`+`bb_smaLength` |
| **Kratos +SHORT** (865) | same range, close<open & anyShort | OHLC, vol | GREEN | none | same |
| **Bull RVOL 1x +LONG** (866) | `normPrice ∈ [th_1x, th_gs)` & bull & anyLong | OHLC, vol | GREEN | none | same |
| **Bear RVOL 1x +SHORT** (867) | same range, bear & anyShort | OHLC, vol | GREEN | none | same |
| **Grand Slam +LONG** (868) | `normPrice ≥ th_gs_moab` & bull & anyLong | OHLC, vol | GREEN | none | same |
| **MOAB +SHORT** (869) | `normPrice ≥ th_gs_moab` & bear & anyShort | OHLC, vol | GREEN | none | same |
| **WTC +L/+S** (870) | `relVolRatio ∈ (th_wtc, th_hiro]` & anyMom | **tv_ta.relativeVolume** | **YELLOW** | library RVOL semantics | §4 — replicate anchored RVOL |
| **Hiroshima +L/+S** (871) | `relVolRatio > th_hiro` & anyMom | **tv_ta.relativeVolume** | **YELLOW** | same | §4 |
| **Nagasaki +L/+S** (872) | bar vol > all prior bars' max vol ever | vol, `var maxVol` | YELLOW | needs full series history from bar 0 | §5 — seed maxVol over entire 6000-bar load; converges trivially |
| **UU/UUU/UUUU +disp** (877-879) | N consec bull bars, sum normPrice ≥ th_saab, ≥1-2 disp in streak | OHLC, vol, stdev | GREEN | streak state | `var` accumulators; stdev warmup `i_std_len`=100 |
| **DD/DDD/DDDD +disp** (880-882) | mirror bearish | OHLC, vol, stdev | GREEN | same | same |
| **2x SAAB / 2x Kratos** (887-888) | sig[1] & sig[0] & (HV150 or disp) | OHLC, vol, highest150, stdev | GREEN | none | std `ta.highest` + `[1]` |
| **2x Bull1x / 2x Bear1x** (889-890) | sigRVOL1x[1] & [0] & gate | OHLC, vol | GREEN | none | same |
| **B2B Mid Bull / Bear** (891-892) | mixed-tier consecutive & gate | OHLC, vol | GREEN | none | same |
| **FAUNA Bull +disp+LONG** (897) | bullText≠"" & disp_cur_seq & anyLong | OHLC, vol, ATR14, SMAs | GREEN | ATR warmup | RMA/ATR seeding §5; all pure ta.* |
| **FAUNA Bear +disp+SHORT** (898) | bearText≠"" & disp_cur_seq & anyShort | OHLC, vol, ATR | GREEN | same | same |
| **Disp Bull / Bear** (903-904) | range[1] > stdev[1]×7.5 & FVG pattern | OHLC, stdev100 | GREEN | none | offset=−1 is display only |
| **Consec Disp Bull/Bear 2+** (905-906) | range[1]>stdev×5.0 & FVG & streak≥2 | OHLC, stdev | GREEN | none | `var` streak |
| **Consec Disp Bull/Bear 3+** (907-908) | range[1]>stdev×3.0 & FVG & streak≥3 | OHLC, stdev | GREEN | none | same |
| **LONG 1-5** (913,915,917-919) | `hybRegRatio>regEff` & `hybCumRatio>cumEff` & bodyRat≥bodyEff & bull & tier-exclusive | OHLC, **tv_ta.relativeVolume ×2** | **YELLOW** | library RVOL (Reg + Cum) | §4 — these are the momentum gate; RVOL parity is load-bearing |
| **SHORT 1-2** (914,916) | mirror bearish, `hybMom1/2` | OHLC, **tv_ta.relativeVolume ×2** | **YELLOW** | same | §4 |
| **HV 1000 +LONG[1]** (924) | `vol[1]==highest(vol,1000)[1]` & anyLong[1] | vol, highest1000 | YELLOW | 1000-bar lookback warmup | §5 — needs ≥1000 prior bars; ok at 6000 |
| **HV 500 +LONG[1]** (925) | highest500, NOT HV1000, anyLong[1] | vol | YELLOW | 500-bar warmup | §5 |
| **HV 350 / 250 / 150** (926-928) | exclusive highest350/250/150 tier & anyLong[1] | vol | GREEN | ≤350-bar warmup, trivially met | std ta.highest |
| **HCT Bull +Singles** (933) | hctMasterBull (10 combos OR) & anySinglesRaw | OHLC, vol, **tv_ta.relativeVolume**, stdev | **YELLOW** | depends on Pentagon/WTC/Hiro = RVOL | §4 (inherits RVOL risk) |
| **HCT Bear +Singles** (934) | hctMasterBear & anySinglesRaw | same | **YELLOW** | same | §4 |
| **Pent+HV1K** (939) | sigPentagon & vol==highest(vol,1000) | **tv_ta.relativeVolume**, vol | **YELLOW** | RVOL (Pentagon) + 1000 warmup | §4 + §5 |
| **Pent+HV500+Disp** (940) | sigPentagon & highest500 & range>stdev×5 | **tv_ta.relativeVolume**, vol, stdev | **YELLOW** | same | §4 + §5 |

### B. Named boolean signals feeding the plots (intermediate, must be parity-exact)

`sigSAAB, sigKratos, sigBullRVOL1x, sigBearRVOL1x, sigGrandSlam, sigMOAB` (278-283, GREEN);
`sigWTC, sigHiroshima, sigPentagon` (291-293, **YELLOW** — RVOL);
`sigAddLong1-5, sigAddShort1-2` (312-335, **YELLOW** — RVOL Reg+Cum);
`sigNagasaki` (351, YELLOW — full-history);
`hct_dispBull/Bear/noDisp` (374-376, GREEN — FVG+stdev);
`groupA_Bull/Bear, groupB` (381-383, inherit RVOL YELLOW);
15 HCT combos + 20 fire booleans (392-435, inherit);
`sigDispBull/Bear`, `sigCDisp*`, `sig_bull/bear_*` sequences, `sig_B2B_*` (all GREEN);
`pentDisp5, sigPentHV1K, sigPentHV500D` (449-451, YELLOW-RVOL).

### C. Alert (1 aggregated `alert()` call, line 1054)

| Cell | Verdict | Status |
|---|---|---|
| `alert(msg + metrics, freq_once_per_bar_close)` | Concatenates all fired detection names + REG/CUM/BODY metrics | DETECTION (mirrors plots). Reproducible — it is a string assembly of signals already classified above. No new dependency. The `freq_once_per_bar_close` confirms bar-close (confirmed) execution. |

No `alertcondition()` calls exist (only the newer `alert()` function). No `label.new` calls (FAUNA text is carried via `plotshape` text + alert string).

### D. INFO PANEL TABLE (41 table.* calls, lines 1073-1137) — COSMETIC vs DETECTION

The entire table is wrapped in `if show_InfoPanel and barstate.islast` (1074). **`barstate.islast` confirms the table renders only on the most recent bar — it is a live dashboard, NOT a per-bar detection.** Classification of every populated cell:

| Cell(s) | Content | Verdict |
|---|---|---|
| (0,0) title (1082) | TF + Hiroshima threshold + R/C/B pct | **COSMETIC** — displays config; threshold itself is GREEN-derived |
| (0,1)-(4,1) header row (1085-89) | "Tier/Side/Reg/Cum/Body" labels | **COSMETIC** |
| `fireBg1-5` (1091-95) | bg color = lime if sigAddLong/Short fired | **COSMETIC** (color only; the underlying `sigAddLong*` boolean IS detection-YELLOW, but the *cell* is display) |
| (0..4, 2-6) M1-M5 rows (1097-1125) | `hybReg/Cum/BodyEff` threshold VALUES via str.tostring | **COSMETIC** — displays the derived threshold ladder (which is GREEN-computable), not a verdict |
| (0,7) (1127) | live `hybRegRatio/hybCumRatio/hybBodyRat` readout | **COSMETIC** display, but values are YELLOW (RVOL-derived) |
| (0,8) (1130) | DISP StdDev multiplier config echo | **COSMETIC** |
| (0,9) (1133) | SAAB/Krat threshold echo | **COSMETIC** |
| (0,10) (1136) | static GATES legend text | **COSMETIC** |

**No table cell carries a standalone detection verdict that is not already emitted by a plotshape or the alert.** The table is 100% dashboard. Parity not required for any cell. (Note: title says "HW SINGLES v2" at line 1082 — a stale label string inside a v3 file; cosmetic, ignore.)

---

## 3. Tally

- **Distinct detection plots/signals classified:** ~30 plot families (45 plotshape calls due to tier-splits) + 1 alert + 41 table cells.
- **GREEN (pure OHLCV/volume + standard ta.*):** ~21 plot families — all RVOL-0.56 (SAAB/Kratos/RVOL1x/GS/MOAB), all sequences (UU…DDDD), all displacement (Disp/CDisp2/CDisp3), all B2B, FAUNA, HV150/250/350, HCT displacement engine.
- **YELLOW (reproducible with care):** ~9 plot families — **WTC, Hiroshima, Pentagon, LONG1-5, SHORT1-2, all HCT combos, Pent+HV1K, Pent+HV500D** (all via `tv_ta.relativeVolume`), plus **Nagasaki** (full-history max) and **HV500/HV1000** (warmup lookback).
- **RED (needs data TV supplies that Massive does not):** **0.** Confirmed line-by-line — no `request.security/financial/dividends/splits/economic`, no sub-candle tick dependency, no external feed. Everything is volume + OHLC.
- **COSMETIC (no parity needed):** all 41 table cells; offset=−1 display shifts; all colors/text/size/bgcolor args.

---

## 4. THE RVOL BASELINE — `tv_ta.relativeVolume` (the biggest parity risk)

### Verbatim source

```pine
// line 288 — Reg@Time RVOL (WTC / Hiroshima / Pentagon)
[currentVolume_reg, pastVolume_reg, _] =
    tv_ta.relativeVolume(reg_length, reg_anchorTimeframe, reg_calculationMode == "Cumulative", reg_adjustRealtime)
relVolRatio = currentVolume_reg / pastVolume_reg          // line 289

// lines 298-299 — Hybrid Momentum (LONG/SHORT 1-5)
[hybRegCur, hybRegPast, _hr] = tv_ta.relativeVolume(reg_length, reg_anchorTimeframe, false, reg_adjustRealtime)  // Regular
[hybCumCur, hybCumPast, _hc] = tv_ta.relativeVolume(reg_length, reg_anchorTimeframe, true,  reg_adjustRealtime)  // Cumulative
hybRegRatio = hybRegCur / hybRegPast   // 301
hybCumRatio = hybCumCur / hybCumPast   // 302
```

Inputs (lines 74-77): `reg_anchorTimeframe = input.timeframe("")` (**blank = chart timeframe**), `reg_length = 30`, `reg_calculationMode = "Cumulative"`, `reg_adjustRealtime = true`.

### Governing equation (from TradingView `ta/7` library semantics, confirmed via docs)

`relativeVolume(length, anchorTF, isCumulative, adjustRealtime)` returns `[currentVolume, averagePastVolume, ratio]` where:

- An **anchor period** is one bar of `anchorTF` (blank → chart TF). The library detects an anchor rollover when the anchored time value changes.
- **`isCumulative=true` (Cumulative mode):** `currentVolume` = volume accumulated since the start of the current anchor period (session-to-date). `pastVolume` = average, over the last `length` anchor periods, of the cumulative volume **at the same intra-period offset** (same number of bars into the period). → **time-of-day / intra-session bucketed RVOL.**
- **`isCumulative=false` (Regular mode):** `currentVolume` = this bar's volume. `pastVolume` = average of the volume **at the equivalent offset position** within the prior `length` anchor periods. → still **positionally/time-bucketed**, NOT a rolling SMA of raw volume.
- **`adjustRealtime=true`:** scales the unconfirmed current bar's partial volume for fair comparison — irrelevant for historical replay (only the live forming bar). On confirmed bars it is a no-op.

> **CRITICAL PARITY INSIGHT:** This is NOT `volume / ta.sma(volume, 30)`. It is **intraday-session-offset-bucketed** relative volume. With blank anchorTF on an intraday chart, the anchor defaults to **"D"** (daily) — so the baseline is "average volume at this same minute-of-session over the prior 30 sessions." A naive `volume/SMA(volume,N)` Python reimplementation will produce DIFFERENT numbers and silently break WTC/Hiroshima/Pentagon AND the entire LONG/SHORT momentum gate — which in turn is the master gate for SAAB/RVOL1x/GS and the HCT combos. **This is the highest-leverage parity item in the whole indicator.**

### Convergence analysis (6000-bar window)

- The Cumulative/Regular average needs `reg_length = 30` prior anchor periods.
- If anchor = "D" and chart = 1m: a US session ≈ 390 min. 30 sessions × 390 ≈ **11,700 bars needed** for the baseline to be fully populated. **6000 1-minute bars ≈ 15 trading days — does NOT cover 30 sessions.** → Baseline under-fills; early ratios computed against <30 sessions. TradingView itself averages over *available* periods until 30 accumulate, so values stabilize only after 30 sessions of warmup.
- On **5m**: session ≈ 78 bars → 30 sessions ≈ 2,340 bars (fits in 6000). **15m:** ≈ 26/session → 780 bars (fits). **1h:** ≈ 7/session → 210 bars (fits easily). **Daily:** anchor likely "M"/"W"; 30 daily-of-month buckets need ~30 months — but `reg_length` semantics on a D chart with blank anchor make anchor=D itself, collapsing Regular mode to ~per-bar — re-derive empirically per TF.
- **Mitigation (EXACT):**
  1. **Reimplement the anchored RVOL faithfully**, not as an SMA. Port `TradingView/ta/7 relativeVolume` logic: track anchor rollover (calendar day boundary for "D"), maintain a within-period bar counter (offset), accumulate session-to-date volume (Cumulative) or take per-bar volume (Regular), and average that quantity across the last 30 same-offset slots.
  2. **Fetch ≥ 30 anchor-periods of warmup before the audit window.** For 1m/5m intraday with daily anchor, pull **≥ 35 trading days** of minute aggregates from Massive (`/v2/aggs` minute bars) so the 30-session bucket fully fills before the first scored bar. 6000 bars alone is INSUFFICIENT at 1m — extend the load.
  3. **Validate by cross-check:** run TradingView `data_get_study_values` on WTC/Hiroshima/Pentagon and the M1-M5 Reg/Cum readouts (table row 7, line 1127) for a sample symbol/TF, and assert the Python `relVolRatio`, `hybRegRatio`, `hybCumRatio` match to ≤0.5% before trusting any downstream LONG/SHORT/HCT signal.
  4. **Pin the anchor:** confirm with Anish whether charts run blank-anchor (→ "D"). If he ever sets `reg_anchorTimeframe` explicitly, the Python port must read that same value.

### Execution model (barstate)

- `conf = barstate.isconfirmed` (276) gates **every** signal. Massive minute aggregates are already closed/confirmed bars → on historical replay, `conf` is always true. Parity-safe: compute on closed bars only. The live forming bar must be excluded (matches `freq_once_per_bar_close` alert, line 1054).
- `barstate.islast` (1074) gates ONLY the info table → **cosmetic, confirmed**. No detection depends on it.
- No `barstate.isrealtime`/`isnew` detection logic. Clean.

---

## 5. Other YELLOW mitigations (warmup / full-history)

- **Nagasaki (341-351):** `var maxVol` accumulates the all-time max volume from `bar_index==0`. Parity requires the Python series to start from the **same first bar** as TradingView's loaded history. If Massive load starts at a different first bar than TV's chart, "all-time max" diverges. **Mitigation:** anchor both to the same inception bar, or define Nagasaki as "max over loaded window" and document the window. Converges trivially after warmup; the only risk is a different bar-0 origin.
- **ATR/RMA seeding (FAUNA, lines 664, 681, 685, 690):** `ta.atr(14)` uses RMA which is recursively seeded; first value = SMA of first 14 TR, then Wilder smoothing. Python must replicate Wilder's RMA seeding exactly, not pandas `.ewm`. Converges to <0.01% within ~5×period (~70 bars) — trivially met in 6000.
- **stdev warmup (lines 371, 460):** `ta.stdev(high-low, 100)` and `ta.stdev(range, i_std_len=100)` are population stdev (TV uses population, ddof=0), need 100 bars. Fully met.
- **HV500/HV1000 (846-847):** need 500/1000 prior bars. Met at 6000, but the first 1000 bars of any window cannot fire HV1000 — exclude them from scoring or extend warmup.
- **`hct_thresh` auto (367):** `ta.cum((high-low)/low)/bar_index` is a running mean of relative range from inception → same bar-0-origin sensitivity as Nagasaki. Anchor inception bar consistently.

---

## 6. DuckDB / Compute Scale

- Per symbol per TF: ~6000 bars × ~30 signal families. Trivial in DuckDB/pandas. The only non-vectorizable pieces are the stateful `var` accumulators (sequence streaks, maxVol, displacement streaks) — implement as ordered single-pass scans (Python loop or DuckDB window with running aggregates).
- **The expensive correctness cost is data volume, not compute:** to fill the 30-session RVOL bucket at 1m you must ingest ~35+ trading days of minute bars *per symbol* as warmup before the scored window. Across the 807-ticker watchlist that is ~35 days × 390 min × 807 ≈ **11M warmup rows minimum** just to seed RVOL — plan the Massive minute-aggregate pull and DuckDB partitioning (by ticker, by day) accordingly.
- `ta.highest(volume, 1000)` over 6000 bars × 807 tickers is fine as a DuckDB windowed MAX.

---

## 7. Bottom Line

**Heavy Weapons Single v3 has ZERO RED dependencies** — confirmed line-by-line, no `request.*`, no tick/quote/financial/corporate-action data. Everything is OHLC + volume. **It is reproducible from Massive candles alone.**

The audit is dominated by **one load-bearing YELLOW: `tv_ta.relativeVolume` (lines 288, 298, 299).** It is NOT a simple volume SMA — it is **intraday-session-offset-bucketed relative volume anchored to the (blank→daily) timeframe**. It drives WTC/Hiroshima/Pentagon directly AND the LONG/SHORT 1-5 momentum gate, which is itself the master gate for the RVOL-0.56 family and all HCT combos. A naive SMA reimplementation will silently corrupt the majority of the indicator's directional signals. **Reimplement the anchored RVOL faithfully and pull ≥30 anchor-sessions of warmup (≈35+ trading days of 1m bars — more than the planned 6000-bar window) before scoring.** Validate Python `relVolRatio/hybRegRatio/hybCumRatio` against TradingView's live table readout to ≤0.5% before trusting downstream signals.

Secondary YELLOWs (Nagasaki, HV500/1000, hct_thresh-auto) all reduce to **anchoring the Python series to the same inception bar** and providing adequate lookback warmup — mechanical, not blocking.

The 41-cell info table and the single `alert()` are **cosmetic / signal-mirroring** respectively; no table cell needs parity. `barstate.islast` (table) and `barstate.isconfirmed` (all signals) are handled by computing on closed bars only.

Sources: [ta — Library by TradingView](https://www.tradingview.com/script/BICzyhq0-ta/), [Pine Script Reference](https://www.tradingview.com/pine-script-reference/v6/)
