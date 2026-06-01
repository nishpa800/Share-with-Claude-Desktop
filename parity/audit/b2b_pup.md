# Parity Audit — B2B PUP Combined 5.4 (`shorttitle="B2B PUP 5.4*"`)

Source (exact — note the **leading `"` is part of the filename**):
`/Users/anishpatel/Desktop/Indicator studies/"B2B PUP Combined 5.4.439am", shorttitle="B2B PUP 5.4*".txt`
Indicator title: `B2B PUP Combined 5.4.439am`. Internal header self-labels v4.31. **1248 lines, ~77 KB, CRLF.**
Auditor: Pine→Python parity auditor. Date: 2026-05-31.

> Access: `~/Desktop` blocks `listdir`/`glob` via macOS TCC, and the filename starts with a literal `"`. Resolve via Spotlight (`mdfind -name 'B2B PUP'` → the `.txt` line) then `open()` the exact path in Python.

---

## VERDICT

The **brief's pre-verified recon is wrong for this file.** This script is **not pure-OHLCV.** It contains `import TradingView/ta/7 as tv_ta` (line 31) and **three** `tv_ta.relativeVolume(30,...)` calls (lines 279, 774, 775) — the genuine **EXTERNAL_DEPENDENCY**. `ta.relativeVolume` internally uses `request.security_lower_tf` to build a session-anchored, multi-day cumulative-volume baseline. It also uses `syminfo.mintick` (line 176), `timeframe.in_seconds()` (lines 44, drives the whole RVOL threshold ladder), `time`/`time("D")`/`session.isfirstbar` (session anchoring), and `barstate.isconfirmed` (`conf`, gates nearly everything). The **20 plotted S-signals are NOT independent** — they are a combination layer over **9 engines** (PUP/PPD, FAUNA, Displacement, PBJ, RVOL+Pentagon, HV+D, TNT/Napalm/Charge/Cont, GZI/ComboSets, UU-streaks). The `tv_ta.relativeVolume` dependency propagates into **S5, S8, S9, S10, S11, S12, S19, S20** (everything touching RVOL det_* — SAAB/Kratos/RVOL1x/GrandSlam/MOAB/Pentagon/WTC/Hiroshima, Long1/Short1, ComboSets, UU). **Bottom line: this indicator is fully reproducible from Massive OHLCV, but ONLY after re-implementing `ta.relativeVolume` from intraday session-cumulative volume (Massive minute aggregates supply this).** It is not a TradingView-proprietary *data* feed — it is a computable transform of OHLCV+timestamp. So: **NO un-substitutable external dependency, but it is NOT free OHLCV either — the RVOL session-cumulative baseline must be rebuilt.**

---

## SUMMARY COUNT TABLE

| Category | Count |
|---|---|
| Plotted detections (plotshape) | **36** (S1–S6,S8–S18 ×2 + S19 ×2 + S20 ×2) |
| Distinct S-mappings | **20** (S1–S20; **S7 does not exist** — numbering skips 7) |
| Runtime `alert()` calls | 4 distinct templates (aggregate bull/bear + per-signal bull/bear), `freq_once_per_bar_close` |
| `alertcondition()` | **0** (none in this build) |
| `bgcolor` | **0** | 
| `label.new` / `box.new` / `line.new` / `table.*` | **0** (overlay plotshapes + alerts only) |
| sigCount / charge-tier ladder | **0** (does NOT exist in this build) |
| Internal engines | 9 |
| `tv_ta.relativeVolume` call sites | **3** (lines 279, 774, 775) |
| Plotted signals free of RVOL dependency | S1,S2,S3,S4,S6,S13,S14,S15,S16,S17,S18 (11) — PURE_OHLCV |
| Plotted signals carrying RVOL (`tv_ta`) dependency | S5,S8,S9,S10,S11,S12,S19,S20 (8) | 
| EXTERNAL_DEPENDENCY (un-substitutable) | **0** (relativeVolume is reconstructable) |
| Parity REPRODUCIBLE_WITH_WARMUP | all 20 (8 also require RVOL reconstruction) |
| Parity BLOCKED | 0 |

> The brief's "S1–S20 plus Napalm, Charge ladders, combos" maps to: Napalm = internal TNT engine (feeds S13/S16); Charge = internal TNT charge-level array (feeds Cont→S14); combos = GZI ComboSets / UU streaks / UC2 / FMU (feed S8,S9,S11,S19,S20). There is **no separate sigCount charge1/2/3/Max background tier** in this version.

---

## ENGINE INVENTORY (every S-signal is built from these)

| Engine | Lines | Key outputs | Data dependency |
|---|---|---|---|
| A — PUP/PPD (Pocket Pivot) | 63–69 | det_PUP, det_PPD | PURE_OHLCV (highest red/green vol, lookback 10) |
| B — FAUNA (MB/RE/GG/TA + TR/ES/GDR excl, 7 hardcoded ON) | 75–104 | det_FAUNABull/Bear | PURE_OHLCV (atr14, sma20/50) |
| C — Displacement | 109–118 | det_DISPBull/Bear | PURE_OHLCV (stdev(rng,100)·mult + FVG) |
| D — PBJ (VWMA/EMA/SMA/WMA/HMA base + ATR supertrend + level arrays) | 124–253 | det_PBJBull/Bear, det_PBBull/Bear | PURE_OHLCV + **syminfo.mintick** (zone-width floor, L176) |
| E — RVOL + Pentagon | 258–291 | det_SAAB,Kratos,RVOL1xB/R,GrandSlam,MOAB (RVOL-ladder) **+ Pentagon,WTC,Hiroshima (tv_ta.relativeVolume, L279)** + Nagasaki | RVOL spike/vol part PURE; **Pentagon/WTC/Hiroshima = EXTERNAL (relativeVolume)**; ladder keyed on `timeframe.in_seconds()` |
| F — HV+D | 296–321 | det_HVDBull/Bear, B2BHVD*, HVDPBJ* | PURE_OHLCV (highest vol rank to 1000 + displacement FVG) |
| G — TNT / Napalm / Charge / Cont | 333–686 | det_bullTNT(+raw/2/super), det_bullNapalm, det_bullCharge, det_contBull, det_retBullTNT, det_b2bBullNapalm (+bear) | PURE_OHLCV (EMA-cross zones, swing pivots, atr200, rsi14, median, zone/charge arrays) |
| H — GZI ComboSets / Long1 / UU | 692–939 | gz_bullGZI/HV, comboSet1–4, det_CS1/CS2/Unified, **det_Long1/Short1 (tv_ta L774/775)**, det_UC2Bull/Bear, det_FMUBull/Bear, det_UU/UUU/UUUU | GZI PURE; **ComboSet1–4 pull RVOL det_*; Long1/Short1 = EXTERNAL (relativeVolume)**; UU uses RVOL rv_normPrice (PURE) + time |
| Combination layer | 945–1029 | det_S1..S20 + fire_* | inherits dependencies of sourced engines |

---

## FULL PER-PLOT TABLE (the 20 plotted S-signals; each has bull+bear plotshape)

| # | Plot (title) | Equation (dereferenced) | Source engines | Dependency | Parity | Notes |
|---|---|---|---|---|---|---|
| S1 | B2B Bull/Bear (◆) | `det_b2bPUP = det_PUP and det_PUP[1]`; PUP=`conf & (close-open)/open·100>3 & vol>highest(redVol[1],10)` | A | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | offset 0. conf-gated. |
| S2 | B2B+FAU (◆) | `det_b2bPUP and FAUNABull and FAUNABull[1]` | A,B | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | atr/sma warmup. |
| S3 | B2B+DISP (◆,off −1) | `PUP[1]&PUP[2] & (DISP or HVD) on [0]&[1]` | A,C,F | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | stdev(100)+HV-rank warmup. |
| S4 | B2B+F+D (label,off −1) | S3 + `FAUNABull[1]&[2]` | A,B,C,F | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | — |
| S5 | B2B+SAAB (◆) | `det_b2bPUP and (RVOL-dir confluence over [0]/[1])`; dir=`SAAB or RVOL1xB or GrandSlam`, neut=`WTC or Hiroshima` | A,**E** | **tv_ta (via neut=WTC/Hiroshima)** + RVOL | REPRODUCIBLE_WITH_WARMUP | dir set is PURE; **neut set pulls relativeVolume** → carries external dep. See resolution. |
| S6 | B2B+PBJ (label,off −1) | `anyB2B & (PBJBull or PBJBull[1] or HVDPBJBull)` (+S3/S4 variants) | A,D,F | PURE_OHLCV (+syminfo.mintick) | REPRODUCIBLE_WITH_WARMUP | mintick scalar from Massive ref. |
| S8 | UC+B2B (label,off −1) | `det_b2bPUP and det_UnifiedBull` (+S3 variant); Unified=`CS1[0] & CS2[1]` | A,**H** | **tv_ta** (ComboSets use RVOL det_*) | REPRODUCIBLE_WITH_WARMUP | depends on Pentagon/RVOL via comboSet. |
| S9 | Uni+B2B (flag,off −1) | `det_b2bPUP and (det_UC2Bull or det_FMUBull ...)` | A,**H** | **tv_ta** (UC2/FMU ← ComboSets ← RVOL) | REPRODUCIBLE_WITH_WARMUP | rewired from S19 OR S20. |
| S10 | L1B2B (flag) | `det_Long1 & det_Long1[1] & (b2bPUP or [1])`; Long1=`conf & regRatio>7 & cumRatio>3.5 & up & bodyRat≥0.6` | A,**H** | **tv_ta (relativeVolume L774/775 — DIRECT)** | REPRODUCIBLE_WITH_WARMUP | regRatio/cumRatio ARE the two relativeVolume outputs. Must reconstruct. |
| S11 | FVG/L1 (label,off −1) | `det_b2bPUP and (det_CS1Bull or det_Long1 or [1])` | A,**H** | **tv_ta** | REPRODUCIBLE_WITH_WARMUP | CS1 + Long1 both RVOL-bearing. |
| S12 | UU+B2B (label) | `det_b2bPUP and (anyUU or anyUU[1])`; UU/UUU/UUUU streak logic | A,**H** | **tv_ta**-light (uses rv_normPrice PURE + th_saab/th_1x from tfSec) | REPRODUCIBLE_WITH_WARMUP | UU uses RVOL *spike* (PURE), NOT relativeVolume; effectively PURE_OHLCV+timeframe. |
| S13 | B2BNPM (label) | `det_b2bPUP and (det_b2bBullNapalm or [1])`; Napalm = TNT displacement vs active opposing TNT zone | A,G | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | heavy TNT state. |
| S14 | CONT (circle) | `det_b2bPUP and (det_contBull or [1])`; Cont = Charge/TNT/Return proximity (≤3 bars) | A,G | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | Charge ladder + Return-to-TNT. |
| S15 | TNT+B2B (label,huge) | `det_b2bPUP and (det_bullTNT or [1])`; TNT=raw∪2.0∪super | A,G | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | ema100/113, atr200, rsi14, zones. |
| S16 | NPM (◆,off −1) | `det_b2bPUP and (det_bullNapCons or [1])`; NapCons=Napalm∪Charge | A,G | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | — |
| S17 | HVD+B2B (flag,off −1) | `det_b2bPUP and (det_B2BHVDBull or [1])`; B2BHVD=HVD & HVD[1] | A,F | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | highest(vol,1000) warmup. |
| S18 | HVDPBJ (flag,huge,off −1) | `det_b2bPUP and (det_B2BHVDPBJBull or [1])` | A,F,D | PURE_OHLCV (+mintick) | REPRODUCIBLE_WITH_WARMUP | — |
| S19 | UC×2 (◆,off −1) | `fire_UC2 = det_UC2Bull`; UC2 counts ≥2 bars in 2-bar window where CS1(FVG-combo) AND CS2(matrix-combo) both fired | **H** | **tv_ta** (ComboSets ← RVOL/Pentagon) | REPRODUCIBLE_WITH_WARMUP | standalone plot. |
| S20 | FMU×2 (◆,off −1) | `fire_FMU = det_FMUBull`; FMU counts ≥2 bars where CS1 OR CS2 fired | **H** | **tv_ta** | REPRODUCIBLE_WITH_WARMUP | standalone plot. |

**Note on S7:** there is no S7 (no `en_S7`, no `det_S7`, no `fire_S7`). The numbering jumps S6→S8. 20 *labels* S1–S20 exist but only 19 `fire_*` series (S1–S6, S8–S18, S19=UC2, S20=FMU) → **36 plotshapes** (each ×2 bull/bear, except all are ×2 = 18×2=36).

---

## DISTINCT `ta.*` / `tv_ta.*` + WARMUP / RECURSIVE-SEEDING RISK

| Func | ~Count | Used by | Type | Warmup / seeding risk |
|---|---|---|---|---|
| `ta.highest` | ~20 | PUP, HV ranks (50/100/200/500/1000), HV+D, swing, GZI(252/63), matrix(67) | windowed max | LOW per call; **highest(vol,1000)** ⇒ need ≥1000-bar warmup before HV-rank/HEV/Nagasaki valid. |
| `ta.sma` | ~10 | FAUNA, RVOL avg, PBJ vol-ma, MAT | windowed mean | LOW. |
| `ta.ema` | ~5 | PBJ MA, TNT ema(SENS=100)/ema(113), f_ma EMA option | recursive | MEDIUM — ema(113) longest; seed consistently. |
| `ta.atr` | ~4 | FAUNA atr14, PBJ supertrend, TNT atr200 | **rma** | HIGH — Wilder recursive seeding; atr200 long warmup. |
| `ta.rsi` | 1 | TNT gate rsi14 | **rma** | HIGH — recursive. |
| `ta.stdev` | ~3 | Displacement, HV+D, TNT disp | windowed | LOW (population stdev). |
| `ta.crossover`/`crossunder` | ~4 | PBJ, TNT cross | 2-bar | LOW. |
| `ta.lowest` | ~3 | PBJ, TNT swing | windowed min | LOW. |
| `ta.median` | 1 | TNT vol gate | windowed | LOW. |
| `ta.cum` | 2 | GZI threshold `cum((h-l)/l)/bar_index`, | cumulative | MEDIUM — path-cumulative from origin; anchor consistently. |
| `ta.vwma`/`ta.wma`/`ta.hma` | 1 each | PBJ MA options | windowed weighted | LOW (default is VWMA). |
| `ta.change` | 1 | is_new_day=change(time("D")) | diff | LOW — needs timestamp. |
| `tv_ta.relativeVolume` | **3** | Pentagon/WTC/Hiroshima (L279), Long1/Short1 (L774/775) | **request.security_lower_tf internally** | **EXTERNAL — must reconstruct from intraday session-cumulative volume.** |

**Recursive seeders to mirror exactly:** rma (atr×4, rsi×1), ema (×5 incl ema113). **Origin-anchored cumulative/path state:** HEV `hv_maxVolEver`, `rv_maxVol` (Nagasaki), `ta.cum` (GZI threshold), ALL TNT/Charge/Zone/FVG `var` arrays, UU streak counters. **No `ta.barssince`/`ta.valuewhen`** (state via `var int …Bar` + `bar_index`). **Forward-confirmation lag:** TNT swing uses `high[SWING_LEN]` (trailing 10-bar, not centered) — reproducible.

---

## NON-OHLCV PINE BUILTINS (parity treatment)

| Builtin | Lines | Purpose | Massive-OHLCV treatment |
|---|---|---|---|
| `barstate.isconfirmed` (`conf`) | 37 | gates nearly every det_* + the alert block | True for all closed historical bars → REPRODUCIBLE offline; only suppresses live forming bar. Port = "fire on bar close." |
| `session.isfirstbar` + `var sessionFirstBarIdx` | 38–42 | first-bar gate (only active if `en_firstBarOnly=true`; default false ⇒ masterGate=true) | Derive from bar timestamp (first intraday bar of a new session-date). Inert by default. |
| `timeframe.in_seconds()` (`tfSec`) | 44 | keys RVOL threshold ladder (th_1x/gs/saab/wtc/hiro) + UU `_ok` gate (`tfSec>120`) | Supply chosen bar resolution in seconds as a config constant. NEEDS_USER_INPUT_ONLY. |
| `time`, `time("D")`, `ta.change(time("D"))` | 45,707,720,841 | `is_new_day`; GZI dedupe `time!=gz_lastT` | From bar UTC timestamp (calendar/session-day change). PURE from timestamp. |
| `syminfo.mintick` | 176 | min zone width in PBJ lander (affects S6/S7→S6,S18) | Per-symbol tick from Massive reference (`/v3/reference/tickers` price increment) or infer from price decimals. One scalar per symbol. |

None is a TradingView-proprietary *data feed*; all derive from timestamp / chosen timeframe / static tick size.

---

## DEPENDENCY RESOLUTION (Seven-Pillar) — `tv_ta.relativeVolume`

**Problem-Solving.** The only non-OHLCV-derivable construct is `import TradingView/ta/7` + 3× `tv_ta.relativeVolume(30,"",cumulative,daily)` (L279,774,775). Its outputs `[currentVolume, requestedAverage, isLastBarOfTf]` drive `rv_relVolRatio` (Pentagon/WTC/Hiroshima) and `ls_regRatio`/`ls_cumRatio` (Long1/Short1). These propagate to plotted **S5, S8, S9, S10, S11, S19, S20** (and partly S12).

**Critical Thinking / Inversion.** Trap: treating relativeVolume as an external *data subscription*. It is not — it is `request.security_lower_tf`-based **aggregation of the symbol's own volume**, anchored to the session. No second symbol, no fundamentals, no NBBO. Therefore it is fully reconstructable from Massive intraday OHLCV; the failure mode is *getting the session anchor and the cumulative-vs-regular distinction wrong*, not *missing data*.

**Cryptography (decode the signature).** `ta.relativeVolume(length=30, anchor="", isCumulative, useDailyMode)`:
- `(30,"",false,true)` → **regular** RVOL: current bar volume vs avg of same intraday-time-slot volume over the last 30 sessions. (`ls_regRatio`)
- `(30,"",true,true)` → **cumulative** RVOL: today's volume accumulated since session open vs avg cumulative-to-this-time over 30 sessions. (`ls_cumRatio`, and the Pentagon path `rv_relVolRatio`)
Rosetta key = **elapsed-time-within-session** + **session-day boundary**.

**Advanced Computer Modeling — Massive substitute.** From Massive minute aggregates (on disk: `/data/historical/minute`; REST: `/v2/aggs/ticker/{t}/range/1/minute/...`):
1. Bucket volume by (session_date, elapsed_seconds_from_RTH_open).
2. `current_regular` = this bar's volume; `avg_regular` = mean over the prior 30 sessions' same time-slot → regRatio.
3. `current_cum` = Σ volume from session open to this bar; `avg_cum` = mean of prior-30-sessions cumulative at the same elapsed offset → cumRatio.
4. `isLastBarOfTf` = bar is the last sub-bar of its parent timeframe (derivable from timestamps).

**Statistical Modeling.** 30-session baseline ⇒ need ≥30 prior trading days of intraday bars per symbol before regRatio/cumRatio are defined. On-disk minute history = 30 days (the exact floor); pull more via REST for stability. Combined with EMA200-class warmup and highest(1000), prepend a generous warmup.

**Game Theory.** Cheapest correct path: implement one shared `relative_volume(length, cumulative)` Massive helper and feed all three call sites. Do **not** drop S5/S8/S9/S10/S11/S19/S20 — unlike a stub-only build, here they ARE plotted, so omitting relativeVolume would silently break ~40% of the visible signal surface.

### Conclusion
**NO un-substitutable external dependency.** `tv_ta.relativeVolume` is the single non-trivial dependency and is fully reconstructable from Massive intraday OHLCV + session timestamps. Everything else is OHLCV + bar-timestamp + per-symbol tick size. **Reproducible — but NOT "free pure-OHLCV": the RVOL session-cumulative baseline must be rebuilt before S5/S8/S9/S10/S11/S19/S20 will match.**

---

## CROSS-CUTTING NOTES

1. **Brief recon was for a different / stub file.** Actual file: 1 TradingView import + 3 `tv_ta.relativeVolume`, 1 `syminfo.mintick`, 1 `timeframe.in_seconds()`, multiple `time`/`time("D")`, ~60 `ta.*`, **36 plotshapes + 4 alert templates, 0 bgcolor/label/box/alertcondition, 0 sigCount/charge-tier ladder.** There is **no S7**. Reconcile the canonical source before porting — pull from `nishpa800/indicators` (declared source of truth) or re-export from TradingView Desktop (MCP is **UP**: `tv_health_check` ok, chart `NASDAQ:OUST`). Other on-disk copies exist (e.g. `~/code/anish/indicators/imports/.../pine_v5/b2b_pup_combined_5_4_439am....pine`, `~/code/anish/indicators/b2b-pup/versions/`).
2. **Massive substitute search done** in `recon/massive-api-endpoints.md` context: standard aggregates + on-disk minute flat files cover all inputs (O/H/L/C/V + timestamp); the only reconstruction is relativeVolume (no special endpoint, no denied scope, no NOI/quotes/fundamentals needed).
3. **Massive 2026-02-23 decimal-size change:** HV-rank and RVOL logic compare raw volumes; ensure the Python loader uses the new decimal volume schema consistently across warmup + scoring (a mixed-schema join would corrupt highest()/RVOL).
4. **`conf` everywhere** → port must fire on bar close, not intrabar.
5. **Heavy stateful path-dependence (TNT/Charge/PBJ/GZI/zone+FVG arrays, UU streaks, HEV/Nagasaki maxima)** is the #1 parity risk — higher than the data dependency. Process bars strictly in order from a fixed origin; no windowed re-eval.
6. **HV ranks need ≥1000-bar warmup; rma (atr200/rsi) + ema113 need ≥5–10×period; relativeVolume needs ≥30 sessions.** Use the largest warmup of these before scoring.
7. **`offset=-1` plots** (S3,S4,S6,S8,S9,S11,S16,S17,S18,S19,S20) render one bar back — align on the *detection* bar (not the plotted bar) when diffing vs `data_get_study_values`.

---

## ACCEPTANCE CRITERIA (Python parity run)

- [ ] Pin canonical source + content hash (this Desktop file vs `nishpa800/indicators`).
- [ ] Implement shared Massive `relative_volume(length=30, cumulative=bool)` from minute aggregates; verify regRatio/cumRatio vs `data_get_study_values` on a known bar.
- [ ] Port 9 engines in bar-order with `var` state from a fixed origin; warmup ≥ max(1000 bars, 30 sessions, 10×atr200).
- [ ] Per-bar boolean match for S1–S6, S8–S20 (bull+bear) vs TV `data_get_study_values`/`data_get_pine_labels` for ≥3 symbols × ≥500 confirmed bars.
- [ ] Honor `offset=-1` alignment + `conf` bar-close semantics.
- [ ] Supply per-symbol `min_tick` and `timeframe_seconds` as config constants.
- [ ] Confirm there is no S7 and no charge-tier background in the port (match this build exactly).
