# HVD ↔ PBJ v1 — BULLISH (38) — Pine→Python Parity Audit

**Source file:** `/Users/anishpatel/Desktop/Indicator studies/"BASE HV+D ↔ PBJ v1 — BULLISH (38)", shorttitle="HVD PBJ BULL".txt`
**Internal header:** `BASE HV+D ↔ PBJ ↔ PPD v1 — BULLISH SPLIT` (bull half of a bull/bear split; 38 bull plotshapes, 0 labels)
**Decoded working copy:** `/Users/anishpatel/quant-brain/parity/HVD_PBJ_BULL.pine` (Pine Script v5, 1312 lines, `overlay=true`)
**Audited:** 2026-05-31 — all 1312 lines read from source; emit calls and every leg traced to OHLCV.

---

## VERDICT (one paragraph)

The BULLISH side is **reproducible from Massive.com OHLCV aggregates alone — NO EXTERNAL DATA DEPENDENCY.** Static scan confirms zero market-data-fetch calls: `request.* = 0`, `security( = 0`, `vwap = 0`, `fundamental = 0`. Every one of the 44 `plotshape` calls and 17 `alert()` calls resolves to booleans built from `open/high/low/close/volume` plus bar timing. **The "+D" (Delta) term is NOT order-flow / bid-ask / tick delta** — it is a *displacement + Fair-Value-Gap* construct: a bar whose prior range exceeds `stdev(range,100)×5` AND forms a bullish FVG (`low > high[2] and close[1] > open[1]`); fully OHLCV-derived (see *Delta derivation*). The headline `hvd_fire_bull` = a rolling/all-time **High-Volume** bar (`volume[1]` ties `ta.highest(volume,N)` for N∈{50…1000} or a running max) co-occurring with that displacement+FVG. The 38 detections are this HV+D core combined with five OHLCV engines (RVOL, FAUNA candle-anatomy, USE-displacement streaks, GZ1/HV-FVG arrays, PUP/PPD volume, PBJ SuperTrend landing-zones, ping-pong S/R, Boom-Hunter Ehlers oscillator). **Three caveats, none blocking:** (1) it imports `TradingView/ta/7` and calls `tv_ta.relativeVolume(...)` — a *public open-source library*, not proprietary data; its math (current-vs-past cumulative/rolling volume) must be ported, not fetched. (2) Every signal is gated on `barstate.isconfirmed` — historically exact on closed bars (which is what a Python backtest consumes). (3) Heavy reliance on session/timeframe primitives (`timeframe.in_seconds`, `time("D")`, `session.isfirstbar`, `syminfo.mintick`) that must be mapped to bar metadata, not fetched. **Conclusion: NO EXTERNAL DEPENDENCY — fully reproducible from OHLCV + bar metadata.**

---

## SUMMARY COUNT TABLE

| Metric | Value |
|---|---|
| `plotshape` calls | 44 (38 are the named bull detections; rest are toggle-split variants) |
| `alert()` calls | 17 |
| `alertcondition` | 0 |
| `bgcolor` / `barcolor` / `plotchar` / `plotarrow` | 0 |
| `line.new` (S/R + landing-zone drawing) | 4 (presentation only) |
| Distinct `ta.*` functions | 19 |
| `math.*` | abs, max, min, avg, exp, cos, sin, asin, sum (pure numeric) |
| `barstate.*` | `isconfirmed` (gates every signal via `conf`) |
| Imported library | `TradingView/ta/7` → `tv_ta.relativeVolume` (open-source, port the math) |
| **EXTERNAL DATA DEPENDENCY** | **0** |
| **BLOCKED** | **0** |
| PURE_OHLCV detections | 38 / 38 (one library-math port: relativeVolume) |
| Parity status | REPRODUCIBLE_WITH_WARMUP (large warmups: up to 1000-bar volume highs; recursive Ehlers/EMA seeding) |

---

## THE 38 BULL DETECTIONS (enumerated, stable-named)

Naming convention for the port: `hvd_bull.<key>`. Source line of the `plotshape` in brackets.

**HV+D core + co-occurrence (5):**
1. `hvd` — HV+D standalone [1111] = `hvd_fire_bull` = `base_hv_hit and d1_bull`
2. `hvd_pb` — HV+D + PB landing [1112] = `hvd_fire_bull and sigBullPB[1]`
3. `hvd_pbj` — HV+D + PBJ reclaim [1113] = `hvd_fire_bull and sigBullPBJ[1]`
4. `co_pbj` — Pipeline-D triple: HV+D+PBJ+USE [1154] = `hvd_fire_bull and sigBullPBJ[1] and use_any_bull[1]`
5. `co_pb` — HV+D+PB+USE [1155]

**USE-engine Tier-1 plotshapes (21) [1116–1139]:**
6. `uuuu` (P21 streak ≥4) · 7. `uuu` (==3) · 8. `uu` (==2, gated) · 9. `alpha_strike` · 10. `foxtrot` (FAUNA 4-bar streak) · 11. `omega_a` (Boom-Hunter Ω) · 12. `od` (Opening-Drive) · 13. `disp_cons2` (displacement streak ≥2 + FAUNA) · 14. `disp_cons3` (≥3) · 15. `golf` · 16. `paf` (PUP+FAUNA B2B) · 17. `cs1_fvg` (combo-set FVG) · 18. `cs2_mat` (combo-set Matrix) · 19. `cs3_combo` (unified combo) · 20. `cc` (combo chain) · 21. `lsc` (long/short chain) · 22. `floor` · 23. `floor2` (2nd floor) · 24. `hw` (Heavy-Weapons stack) · 25. `super` · 26. `sduper` (SUPER DUPER) · plus 27. `nag_plus` (Nagasaki+) [1139]

**B2B HV+D (3) [1170–1172]:**
28. `b2b` (no-PB) · 29. `b2b_pbj` · 30. `b2b_pb`

**HV+D MOMENTUM CO-OCC (8) [1206–1213]:**
31. `hvdm_pup` · 32. `hvdm_rvol` · 33. `hvdm_cmb` · 34. `hvdm_pbj_pup` · 35. `hvdm_pbj_rvol` · 36. `hvdm_pbj_cmb` · 37. `hvdm_2of3` · 38. `hvdm_3of3`

(Total 44 plotshape calls = these 38 + the 3 Pipeline-D/B2B duplicates already counted + 3 toggle-split rows. The 17 `alert()` calls are 1:1 with the gated detections plus the aggregator and Nagasaki-direction alerts.)

---

## PER-DETECTION / PER-LEG TABLE

| # | Name | Equation (dereferenced to OHLCV + ta.*) | Inputs | Dependency | Parity |
|---|---|---|---|---|---|
| L1 | `base_hv_hit` (HV core) | `volume[1] == ta.highest(volume,N)[1]` for any enabled N∈{50,75,…,1000} (17 toggles) **OR** running all-time max (`isHEV`/`maxVolEver`) | volume; 17 bool toggles, useHEV | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP (≤1000-bar) |
| L2 | `d1_bull` (the "+D") | `conf and (range[1] > ta.stdev(range,100)[1]*5.0) and (low>high[2] and close[1]>open[1])`, `range = |open−close|` (or H−L) | OHLC; d1_len=100, d1_mult=5 | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP (100) |
| 1 | `hvd_fire_bull` | `base_hv_hit and d1_bull` | L1,L2 | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP |
| 2 | `hvd_pb` | `hvd_fire_bull and sigBullPB[1]` | L1,L2,PBJ-engine | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP |
| 3 | `hvd_pbj` | `hvd_fire_bull and sigBullPBJ[1]` | L1,L2,PBJ-engine | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP |
| E-RVOL | `sigSAAB/sigGrandSlam/sigBullRVOL1x/sigWTC/sigHiroshima/sigPentagon` | normalized price-spike `|close−open|/sma(|c−o|,30)[1]` and **`relVolRatio = tv_ta.relativeVolume(30,…)`** vs timeframe-scaled thresholds | OHLCV, tfSec | PURE_OHLCV + **library math port** | REPRODUCIBLE_WITH_WARMUP |
| E-FAUNA | `sigFAUNABull` | candle anatomy: body/range vs `ta.atr(14)`, `volume>1.8*ta.sma(volume,20)`, trend `ta.sma(close,50)` rising, with weak/strong-bear exclusions | OHLCV | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP (50) |
| E-DISP | `sigDISPBull, disp5_bull, sigDispConsBull2/3` | range vs `ta.stdev(range,100)*mult` + bullish FVG + consecutive-streak counters + FAUNA history | OHLC | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP (100) |
| E-GZ1 | `gz_bullGZI, gz_bullHV` | bullish FVG (`low>high[2] and close[1]>high[2]`, gap% > `ta.cum((h−l)/l)/bar_index`), HV via `ta.highest(volume,{63,252,5000})`; intersection over array of recent FVGs | OHLCV | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP (≤5000) |
| E-PUP/PPD | `sigPUP` | `((close−open)/open)*100 > 3.0 and volume > ta.highest(redVol[1],10)` | OHLCV | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP (10) |
| E-PBJ | `sigBullPBJ, sigBullPB` | SuperTrend on `ta.vwma/ema(close)` ± `mult*ta.atr` → cross + landing-zone array approach; PBJ = `low<ema(close,20)*(1−atr-thresh) and low==ta.lowest(low,25) and volume>sma(vol,20)*0.1` | OHLCV | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP (25) |
| E-SR | `bull_pp` (floor gravity) | ping-pong S/R from `ta.pivothigh/pivotlow(5,1)` + body-flat levels + `ta.atr` bounce logic; needs `syminfo.mintick` for tolerance | OHLC, mintick | PURE_OHLCV (+tick size) | REPRODUCIBLE_WITH_WARMUP |
| E-BH | `bh_anyOmega` (Omega) | Ehlers Boom-Hunter: high-pass + super-smoother recursive filters on `close`, TCI/MF/RSI tradition, pivots/crossovers | close, volume | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP (recursive seed) |
| E-MATRIX | `sigNeoBull/sigTrinityBull` | `volume == ta.highest(volume,67)` + FAUNA / body | OHLCV | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP (67) |
| 6–38 | USE/B2B/MOMENTUM plotshapes | boolean compositions of the engines above + `show_*` toggles + `masterGate` (first-bar-of-day gate) | engines + user toggles + session | PURE_OHLCV (toggles = NEEDS_USER_INPUT_ONLY) | REPRODUCIBLE_WITH_WARMUP |

Every `show_*`, `en_*`, length, mult, and `i_req_fvg` input is **NEEDS_USER_INPUT_ONLY** — pin to the chart defaults to reproduce.

---

## DISTINCT `ta.*` FUNCTIONS (19) + WARMUP / RECURSIVE-SEEDING RISK

| ta.* | Warmup | Recursive (path-dependent) | Note |
|---|---|---|---|
| `ta.highest` / `ta.lowest` | YES — **up to 1000-bar** (and 5000 in GZ1) | no | dominant warmup driver; needs ≥1000 bars history |
| `ta.stdev` | YES (100) | no | displacement thresholds |
| `ta.sma` | YES | no | volume/body/trend baselines |
| `ta.ema` | YES | **YES** | PBJ MA, SuperTrend base, Boom-Hunter; seed = SMA of first len |
| `ta.atr` | YES | **YES** (rma) | FAUNA/PBJ/SR distance gates |
| `ta.vwma` / `ta.wma` / `ta.hma` | YES | partial | selectable PBJ MA type |
| `ta.linreg` | YES | no | Boom-Hunter wt3 |
| `ta.rsi` | YES | **YES** (rma) | Boom-Hunter tradition |
| `ta.cum` | from bar 0 | **YES** | GZ1 auto-threshold; start at first bar |
| `ta.change` | 1 | no | day-change `time("D")`, deltas |
| `ta.barssince` | needs event in window | quasi-state | Boom-Hunter entry windows |
| `ta.crossover` / `ta.crossunder` | 1 | no | SuperTrend + oscillator edges |
| `ta.pivothigh` / `ta.pivotlow` | **centered (left+right confirm lag)** | no | SR(5,1) → 1-bar right lag; Boom-Hunter(1,1)/(5,5) |
| `tv_ta.relativeVolume` (library) | YES (30) | YES (cumulative mode) | **port the library math, do not fetch** |

**HIGH-priority parity risks:**
- **Large lookbacks:** `ta.highest(volume, 1000)` and GZ1's `ta.highest(volume,5000)` require ≥1000 (ideally ≥5000) contiguous bars of warmup before signals are valid. `max_bars_back=1100` is set in the script.
- **Recursive seeding:** `ta.ema/atr/rsi/cum`, the Boom-Hunter Ehlers high-pass/super-smoother filters (`bh_HP`, `bh_Filt`, `bh_Peak`…), SuperTrend (`curr_long/short`, `st_dir`), and all `var`-state counters (streaks, `maxVolEver`, FVG/SR arrays) are path-dependent. Feed full contiguous Massive history from the first available bar.
- **Pivot lag:** `ta.pivotlow/pivothigh` are centered — apply identical right-offset to avoid lookahead.
- **`tv_ta.relativeVolume`:** sourced from the open `TradingView/ta` library (v7). It returns `[currentVolume, pastVolume]` (rolling or cumulative-by-session). Reimplement from OHLCV+session, not as an external call.

---

## DELTA / ACCUMULATION ("+D") DERIVATION — VERIFIED FROM SOURCE (highest parity-risk)

**Question:** does "+D" require bid/ask, tick, or order-flow delta? **Answer: NO.** There are zero quote/tick/`request` calls. The "+D" is a **displacement + bullish Fair-Value-Gap** construct (source lines 56–67, 121):

```
d1_rng      = (d1_type=="Open to Close") ? |open - close| : (high - low)
d1_std      = ta.stdev(d1_rng, 100)
d1_thresh   = d1_std * 5.0
d1_prevDisp = d1_rng[1] > d1_thresh[1]               // prior bar was an outsized "displacement" candle
d1_bullFVG  = low > high[2] and close[1] > open[1]    // 3-bar bullish Fair Value Gap
d1_bull     = barstate.isconfirmed and d1_prevDisp and d1_bullFVG
hvd_fire_bull = base_hv_hit and d1_bull              // HV + the "+D"
```

Interpretation: "+D" = *Displacement* — a statistically large-range bar (≥5σ of the 100-bar range distribution) immediately followed by an unfilled upward gap (current low above the high two bars ago, with a green middle bar). This is pure price geometry. Every input — O/H/L/C and `[1]`,`[2]` history — is in a Massive OHLCV aggregate. The `bar_range==0` cases reduce naturally (range 0 fails the `> threshold` test). → **PURE_OHLCV, REPRODUCIBLE_WITH_WARMUP** (warmup = 100 bars for the stdev). The related "PPD" engine (PUP/PPD, lines 432–436) is a separate volume-vs-direction proxy (`green/red volume` rolling highs), also pure OHLCV.

---

## CROSS-CUTTING NOTES

- **Architecture:** HV core (volume rolling/all-time highs) × "+D" (displacement+FVG) = `hvd_fire_bull`, fused with 9 OHLCV engines (RVOL, FAUNA, USE-Displacement, GZ1/HV-FVG, PUP/PPD, PBJ-SuperTrend, Ping-Pong S/R, Boom-Hunter Ω, Matrix-Number) into 38 gated bull detections. Mirror **BEARISH (36)** file inverts every sign.
- **`tv_ta.relativeVolume` (library import):** the ONLY non-builtin call. It is open-source TradingView library math (not a data feed). DEPENDENCY RESOLUTION below.
- **Session / timeframe primitives:** `timeframe.in_seconds(timeframe.period)` (RVOL threshold scaling), `time("D")`/`is_new_day`, `session.isfirstbar` (first-bar-of-day `masterGate`), `sessionBarCount` (Opening-Drive window), `syminfo.mintick` (S/R tolerance). These are **bar metadata**, reproducible from Massive bar timestamps + the instrument's tick size — not external fetches. Map them; do not treat as blockers.
- **barstate:** every signal carries `conf = barstate.isconfirmed`, so all detections are bar-close events → historically exact in a Python backtest. No LIVE_ONLY repaint dependency.
- **Drawing layer** (`line.new` ×4 for S/R) is cosmetic; the *boolean* SR state (`bull_pp`) is what feeds detections and is fully reproducible.

**DEPENDENCY RESOLUTION (for the one library call + session primitives):**
- *Seven-pillar:* **Problem** = `tv_ta.relativeVolume` and session/tick primitives are not OHLCV builtins. **Critical thinking** = a missed reimplementation silently shifts RVOL thresholds and the OD/first-bar gates → false signal counts. **Cryptography** = decode the library: `relativeVolume(len, anchorTF, isCumulative, adjustRealtime)` returns current vs trailing average volume (rolling sum of `len` bars, or session-cumulative when `isCumulative`). **Computer modeling** = port as `currentVol = sum(volume, len)` (rolling) or session-cumulative `volume`; `pastVol = sma(that, len)` trailing — reproduce from OHLCV + session boundaries. **Statistical** = validate ported `relVolRatio` against TV `data_get_study_values` on ≥3 symbols/timeframes before trusting. **Game theory** = no vendor lock-in; the library is open and the inputs are OHLCV. **Synthesis** = reimplement in Python from Massive bars + session calendar; tick size from Massive reference data.
- *Massive substitute:* none needed for a *data* feed — Massive OHLCV aggregates (`/data/historical/` daily & minute, already on disk) supply every input. `recon/massive-api-endpoints.md` Reference endpoints (tickers/splits) provide `mintick`/tick size; bar timestamps provide session/day boundaries.

**Bottom line: NO EXTERNAL DATA DEPENDENCY — fully reproducible from Massive OHLCV + bar metadata, given ≥1000–5000 bars of warmup and exact recursive-state seeding.**
