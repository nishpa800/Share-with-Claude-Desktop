# Decoupling Audit — Jumbo CIA ★ FIRST BAR ONLY FAUNA FIXED★ (shorttitle "1st PUP FAUNA")

**File:** `/Users/anishpatel/Desktop/Indicator studies/"Jumbo CIA ★ FIRST BAR ONLY FAUNA FIXED★", shorttitle="1st PUP FAUNA".txt` (1747 lines, Pine v5)
**Audited:** 2026-05-31 · **Scope:** TradingView-decoupling risk for massive.com OHLCV → local Python candle factory.

---

## 1. Verdict

This indicator is **fully recomputable from massive.com aggregate OHLCV alone — there are NO Class-D blockers.** It uses `import TradingView/ta/7 as tv_ta` (line 4) with exactly one call site, `tv_ta.relativeVolume(...)` at line 337 — and the single value it produces (`relVolRatio`, line 338) is **dead/orphaned**: it feeds no detection plot, no signal, no alert (confirmed by full-file grep — `relVolRatio` appears once, is never read again; the inline comment on line 336 even states "WTC signal removed... kept for potential future use"). So the only Class-C dependency in the script can be **dropped entirely with zero behavioral impact**, or ported later at leisure. Every actual detection plot is built from `open/high/low/close/volume` plus `ta.*` math builtins (Class A) and session/calendar/mintick/barstate plumbing (Class B). The real parity work is not TradingView coupling; it is **warmup depth and session semantics**: `ta.highest(volume, 5000)` (lines 212, 475) demands >5000 closed bars of history before HV/Nagasaki/GZ1-HV milestones are correct, which is exactly why the 6000-bar candle factory target exists; and the entire "FIRST BAR ONLY" / Katana / Opening-Drive / FAUNA+ chain logic hinges on `ta.change(time("D"))` new-day detection (line 731), which must be reproduced with correct exchange-local (America/New_York) calendar + DST handling in Python. Bottom line: **decoupling-safe. Port the new-day clock and the 5000-bar volume warmup carefully; delete or trivially port relativeVolume.**

---

## 2. Detection-plot / signal-output table

One row per distinct plotted shape, label, or alert-bearing signal output. Combo signals are listed once (their bull/bear pair grouped). "Series/inputs" lists the upstream primitives; all of them resolve to OHLCV + ta.* unless noted.

| Detection Plot | Line refs | What it detects | Series/inputs used | TV namespaces touched | Class | OHLCV sufficient? | Recreate risk | Notes / mitigation |
|---|---|---|---|---|---|---|---|---|
| **Grand Slam** (plot+alert+alertcond) | 327, 1106, 1215–1231, 1719 | Bull body-vs-vol spike ≥ MOAB threshold | bb_normalizedPrice (=|close-open|/sma; lines 313–321), th_gs_moab(tfSec) | ta.sma, timeframe.in_seconds, barstate.isconfirmed | A/B | Y | Low | Threshold is a hardcoded tf-second lookup (296–308). Reproduce `timeframe.in_seconds` from bar interval. |
| **MOAB** | 328, 1107, 1233–1249, 1720 | Bear mirror of Grand Slam | same as Grand Slam, bearish | ta.sma, timeframe.* | A/B | Y | Low | Mirror of above. |
| **RVOL 1x Bull/Bear** (internal, feeds combos/extras) | 325–326, 774–775 | Body-vs-vol spike in [th_1x, th_gs_moab) | bb_normalizedPrice, th_1x(tfSec) | ta.sma, timeframe.* | A/B | Y | Low | Not plotted directly; consumed by Super/Full Stack/Typhoon/Katana/Nagasaki extras. |
| **SAAB / Kratos** (internal) | 331–334, 799–800 | Lower-tier RVOL band (0.56×th_1x) | bb_normalizedPrice | ta.sma, timeframe.* | A/B | Y | Low | Internal; feeds SAAB²/KRATOS²/Gripen/Whale extras. |
| **FAUNA Bull/Bear** | 343–388 | Momentum candle (MB/RE/TA) minus excluded reversal patterns | atr(14), sma(vol,20), sma(body,20), sma(range,20), sma(|Δclose|,10), sma(close,50), body/range ratios | ta.atr, ta.sma, barstate.isconfirmed | A/B | Y | Low | Pure candle geometry + vol multiples. Core of the whole script. |
| **Displacement Bull/Bear** | 393–410, 771–772 | StdDev-multiple range bar + FVG | stdev(range,100)×mult, FVG (low>high[2] etc.) | ta.stdev, barstate.isconfirmed | A/B | Y | Low | Two thresholds: std×i_std_mult and std×2 (PUP variant). |
| **GZ1 HV FVG: bullHV / bearHV** | 211–255, 780–781, 905–906 | FVG bar that is also a volume milestone (HV) | volume[1], highest(vol,5000)[1], highest(vol,252)[1], FVG geometry, cum range threshold | ta.highest, ta.cum, time (dedupe) | A/B | Y | **Med (warmup)** | `highest(volume,5000)[1]` needs >5000 prior closed bars. `time != gz_lastT` dedupe (B). |
| **GZ1 GZI: bullGZI / bearGZI** | 221–255, 782–783 | Overlapping/stacked FVGs within gz1_dist bars | gz_fvg array of FVG boxes, bar_index distance | ta.highest, ta.cum, time | A/B | Y | Med | Stateful array of FVG objects; deterministic from OHLCV. Replay must rebuild array in-order. |
| **GZ1 mitigation lines** (visual only) | 257–266 | Draws line when FVG mitigated | array state, close vs box | line.new, xloc.bar_time | B | Y | Low | Pure drawing; default off (gz1_mitLvl=false). Visual layer — recompute level, draw in TV only. |
| **HV standalone (sigHV)** | 475–477 | Current bar = highest vol in 5000 or 252 | highest(vol,5000), highest(vol,252) | ta.highest | A | Y | **Med (warmup)** | 5000-bar warmup. Feeds Katana yesterday-state + PUP+ANY/PPD+ANY extras. |
| **Nagasaki (HEV) Bull/Bear** | 482–489, 1083–1084, 1126–1127, 1548–1589, 1743–1744 | Highest-ever volume bar + any directional signal | running max(volume) since bar 0, nag_dir_bull/bear aggregate | barstate.isconfirmed | A | Y | **Med (warmup)** | "Ever" = since first bar in series → result depends on how deep history loads. Anchor to a fixed epoch in Python for stability. |
| **Pocket Pivot PUP/PPD (sigPUP/PPD)** | 494–503 | Up/down bar w/ vol > highest opposite-color vol in lookback | redVol/greenVol, highest(...,pp_lookback), % bar move | ta.highest | A | Y | Low | pp_barSize % and lookback are inputs. |
| **Anish Pass Bull/Bear (sigAnishBull/Bear)** (internal) | 508–516 | Stage-2/Stage-4 trend template | ema50/150/200, ema200[21], highest/lowest(252) | ta.ema, ta.highest, ta.lowest | A | Y | Low | Computed but NOT consumed by any plot/alert in this file (orphaned like relVol — note for cleanup). 252-bar + 21-offset warmup. |
| **Whale+PUP / Whale+PPD** | 521–552, 725–726, 1110–1111, 1252–1276, 1721–1722 | Pivot reclaim + HV milestone + PUP/PPD + PBJ | sma(close,len), sma(vol,50), highest(vol,252/63), max-vol-ever, dn/up vol arrays, PBJ engine | ta.sma, ta.highest, arrays | A | Y | Med (warmup) | maxVolEver = running max (history-depth sensitive). Requires PBJ engine (also Class A/B). |
| **PB&J engine: sigBullPBJ/PB, sigBearPBJ/PB** | 559–714 | Supertrend cross + level-approach (PB) / breakout-pullback (PBJ) | f_ma (VWMA/EMA/SMA/WMA/HMA), atr, supertrend, ema, lowest/highest, lvl arrays | ta.ema/sma/wma/hma/vwma/atr, ta.crossover/under, syminfo.mintick (618), barstate.isconfirmed | A/B | Y | Med | `syminfo.mintick` (618) gates level creation — must source per-symbol tick size. Stateful arrays; order-dependent replay. |
| **Yin Yang swing high/low + breakout/breakdown/rejection** | 415–470, 801–802 | ATR-filtered pivots, level cross events | pivothigh/low(75,1), atr(50)×3.5, sr array | ta.pivothigh/low, ta.atr, arrays, barstate.isconfirmed | A | Y | Low | pivothigh(75,1) → needs 75 bars left context. Feeds Gripen/Typhoon. |
| **Double Disp Bull/Bear** | 813–814, 1165–1166, 1355–1384, 1733–1734 | B2B Disp+FAUNA + PUP/PBJ | sigDISP, sigFAUNA, al_PUP, al_anyPBJ | (derived) | A/B | Y | Low | Pure composition of A/B signals. |
| **PUP Combo / PPD Combo (PUP²/PPD²)** | 817–818, 1168–1169, 1387–1413, 1735–1736 | B2B Disp(pup)+FAUNA+PUP | sigDISP_pup, sigFAUNA, al_PUP | (derived) | A/B | Y | Low | Composition. |
| **Full Stack Bull/Bear** | 821–822, 1171–1172, 1416–1442, 1737–1738 | RVOL+FAUNA+Disp+PBJ | al_anyRVOL, al_FAUNA, sigDISP, al_anyPBJ | (derived) | A/B | Y | Low | Composition. |
| **FVG Stack Bull/Bear** | 825–826, 1174–1175, 1445–1465, 1739–1740 | RVOL+FAUNA+Disp+HV+GZI | + gz_bullHV, gz_bullGZI | (derived) | A/B | Y | Low | Composition. |
| **Super Combo Bull/Bear (PBJ/PB)** | 829–834, 1103, 1178–1188, 1467–1498, 1741–1742 | Disp+PBJ/PB+FAUNA+RVOL | (derived) | (derived) | A/B | Y | Low | Composition. |
| **Musashi Bull/Bear** | 837–838, 1160–1162, 1500–1523, 1731–1732 | (GZI or HV)+PUP+Whale+PBJ | gz_*, al_PUP, al_Whale, al_anyPBJ | (derived) | A/B | Y | Low | Composition. |
| **Gripen Bull/Bear** (internal, no plot) | 841–842 | Swing+1stBar+RVOL/SAAB+FAUNA+PB/PBJ | yy_validLow/High, is_new_sess, derived | (derived) | A/B | Y | Low | Computed but no plot/alert; dead like Anish Pass — flag for cleanup. |
| **SAAB² / KRATOS²** | 844–857, 1113–1115, 1278–1303, 1725–1726 | B2B RVOL band + qual + PUP/PBJ | sigSAAB, sigRVOL1x, sigGrandSlam, gz_*, derived | (derived) | A/B | Y | Low | Composition; saab2_reqConfirm toggles qual gate. |
| **Typhoon Bull/Bear** | 859–863, 1117–1119, 1305–1330, 1727–1728 | Swing+1stBar+FAUNA+(PUP or Whale+PBJ) | yy_valid*, is_new_sess[yy_rightBars], derived | (derived) | A/B | Y | Low | Uses yy_rightBars offset (B — bar-offset alignment). |
| **Tomcat Bull/Bear** | 865–869, 1121–1123, 1332–1353, 1723–1724 | 1stBar+FAUNA+Disp+≥2 of {PUP/PPD,Whale,PBJ} | is_new_sess, derived counts | (derived) | A/B | Y | Low | Composition + new-day gate. |
| **PAF PUP/PPD B2B** | 871–873, 1129–1131, 1591–1622, 1745–1746 | B2B PUP+FAUNA (no disp) | sigPUP, sigFAUNA | (derived) | A | Y | Low | Composition. |
| **FAUNA+ Alpha/Bravo/Charlie/Delta/Echo** | 878–1004, 1135–1146, 1624–1663, 1747 | Density of Disp-FVG hits ≥req within window, optional FAUNA/PUP/HVGZ requirements | f_fp_disp (stdev(range,100)×mult + FVG), f_fp_count, chain/grace state vs is_new_sess | ta.stdev, barstate.isconfirmed, new-day | A/B | Y | Low | Stateful chain reset on new session (B). Each set = same math, diff params. |
| **FAUNA+ Foxtrot (4-in-4)** | 1006–1008 | 4 consecutive FAUNA bars | sigFAUNABull[0..3] | (derived) | A | Y | Low | Composition. |
| **FAUNA+ Golf (PUP²/PPD²)** | 1010–1015, 1148–1150 | B2B any-density + FAUNA + PUP | fp_any_raw, fp_al_fauna, fp_al_PUP | (derived) | A | Y | Low | Composition. |
| **FAUNA+ Opening Drive Bull/Bear** | 1017–1026, 1152–1154 | ≤od_max bars into session + FVG + disp + PUP/PPD vol | sessionBarCount, od FVG/disp, pp_priceUp/volBull | ta.stdev, new-day session counter | A/B | Y | **Med** | Depends on `sessionBarCount` (735–742) which depends on new-day clock. Session-relative — port NY calendar. |
| **Katana Bull/Bear (A/B/E)** | 1032–1073, 1156–1158, 1525–1546, 1729–1730 | Yesterday-state + today GZI/HV/FAUNA + dir + PUP/PBJ | persisted prior-session vars captured on is_new_sess, kat_dir | new-day, barstate | A/B | Y | **Med** | Cross-session carry of "yesterday" flags — exact new-day boundary must match TV. |
| **Super plotshape ("S")** | 1103 | Visual square for any Super | sigAnySuperBull/Bear, fbm | plotshape | A/B | Y | Low | Visual; logic already covered by Super Combo. |
| **FAUNA+ combined Bull/Bear plot + letter labels** | 1135–1146 | Aggregate A–F shape + which-letter label | anyAFBull/Bear | plotshape, label.new | A/B | Y | Low | Visual aggregation. |
| **PUP+ANY / PPD+ANY alert** | 1665–1716 | PUP/PPD on 1st bar + enumerated co-signals | sigPUP/PPD + all derived | (derived) | A/B | Y | Low | Alert-only enrichment; no new detection math. |

**Namespace tally across all rows:** `ta.*` (sma, ema, wma, hma, vwma, atr, stdev, highest, lowest, cum, change, crossover, crossunder, pivothigh, pivotlow), `math.*`, `barstate.isconfirmed`, `timeframe.in_seconds`/`timeframe.period`, `time`/`time("D")`, `syminfo.mintick`, `input.source(close)`, plus drawing namespaces (`plotshape`, `label.new`, `line.new`) which are visual-only. **`request.security`: none. `tv_ta.*`: exactly one, orphaned.**

---

## 3. Flagged dependencies

### 3.1 `tv_ta.relativeVolume` — Class C (the ONLY library coupling) — and it is DEAD

**Call site (line 337):**
```pine
[currentVolume_reg, pastVolume_reg, _] = tv_ta.relativeVolume(reg_length, reg_anchorTimeframe, reg_calculationMode == "Cumulative", reg_adjustRealtime)
relVolRatio = currentVolume_reg / pastVolume_reg          // line 338
```
Inputs (lines 76–80): `reg_anchorTimeframe = input.timeframe("")`, `reg_length = 30`, `reg_calculationMode ∈ {Cumulative, Regular}` (default Regular), `reg_adjustRealtime = true`.

**Blast radius: ZERO.** Full-file search confirms `relVolRatio`, `currentVolume_reg`, and `pastVolume_reg` are **never referenced again** after line 338. The author's own comment (lines 271, 336) says "WTC REMOVED" / "kept for potential future use, WTC signal removed." **No plot, no signal, no alert consumes it.** Therefore for parity you may simply **omit this line** and the import on line 4, and the output is byte-identical. This is the single most important finding: the only TV-library coupling in a 1747-line script is inert.

**Exact signature** (`TradingView/ta/7`, open source):
```
relativeVolume(simple int length, simple string anchorTimeframe, simple bool isCumulative, simple bool adjustRealtime) =>
    [currentVolume, averageVolume, relativeVolume]
```
Returns a 3-tuple: current (possibly cumulative) volume, the trailing average of that quantity over `length` prior anchor periods, and their ratio.

**Parameter meanings:**
- **`anchorTimeframe`** — the reset boundary. `""` means "use the chart's own timeframe as anchor" (i.e., no higher-TF anchoring; each bar is its own period). A value like `"D"` would reset the cumulative accumulator at each new day. With the default `""`, Regular mode degenerates to "this bar's volume vs the average of the last `length` bars' volume."
- **`isCumulative`** (`reg_calculationMode=="Cumulative"`, default **false/Regular**) — Regular: compare per-bar volume to the average per-bar volume at the same position; Cumulative: accumulate volume from the anchor open and compare to the average cumulative-volume-at-same-elapsed-time across the prior `length` anchor periods.
- **`adjustRealtime`** (`reg_adjustRealtime=true`) — on the still-forming (unconfirmed) bar/period, project/scale the partial volume so RVOL isn't artificially low intraday. Only affects the live bar; **closed bars are unaffected**. Since this script gates virtually everything behind `barstate.isconfirmed` and the consumer is dead, the realtime adjustment is irrelevant here.

**Port algorithm from massive intraday bars (if ever revived):**
- *Regular mode, anchor=="":* `currentVolume = volume[t]`; `averageVolume = mean(volume[t-length .. t-1])`; `rvol = currentVolume/averageVolume`. Trivial rolling mean.
- *Cumulative-anchored (anchor="D"):* For each bar, compute `elapsed` = bars since the session anchor (or seconds-into-session). `currentVolume = Σ volume from anchor-open through t`. `averageVolume = mean over the prior `length` sessions of (cumulative volume at the same elapsed position)`. `rvol = currentVolume / averageVolume`. Implementation: bucket each session's volume by intraday slot index, keep a deque of the last `length` sessions' cumulative-by-slot curves, average element-wise.
- *Realtime adjustment:* on the open bar of the live period only, scale partial cumulative volume by `(period_length / elapsed)` (or by historical same-slot completion fraction) to estimate the full-period figure. Compute only on the live bar; never on closed bars. For backtest/parity you compute on closed bars only → adjustment is a no-op → no parity risk.

**Recommendation:** Drop it. If revived, it is a ~20-line Python function. Class C, but de-facto Class A given it is unused.

### 3.2 Volume-milestone warmup — `ta.highest(volume, 5000)` (Class A, but parity-critical)

Lines **212** (`ta.highest(volume,5000)[1]`) and **475** (`ta.highest(volume,5000)`) plus the `[1]` shift, `ta.highest(volume,252)` (213, 476, 524), `ta.highest(volume,63)` (525). These drive **HV, GZ1-HV, Whale, Nagasaki**. Math is trivial (rolling max) but **the answer is wrong until ≥5000 closed bars of true history are loaded**. This is precisely the 6000-bar candle-factory parity requirement: load ≥5001 bars (ideally 6000) before trusting any HV-milestone plot. Note `script max_bars_back=1000` (line 2) — Pine still evaluates `highest(...,5000)` because it's a series op, but your Python engine must hold the full 5000-deep volume window.

### 3.3 `syminfo.mintick` (Class B)

Line **618**: `if math.abs(up - lo) >= syminfo.mintick` gates whether a PB&J level box is created (degenerate near-zero-height levels are rejected). Per-symbol tick size must be sourced from Massive reference data (ticker details) or inferred from price scale per symbol. Wrong mintick → spurious or missing PB&J levels → cascades into PB/PBJ-dependent combos (Whale, Super, Full Stack, Musashi, Katana, Tomcat, Typhoon). Med importance. Also `str.tostring(close, format.mintick)` (1212) is display-only.

### 3.4 New-day / session boundary (Class B — the structural backbone)

Line **731**: `is_new_day = ta.change(time("D")) != 0` → `is_new_sess` (732) drives: FIRST-BAR-ONLY gates (`fb0/fbs/fbm`, 744–788), `sessionBarCount` (735–742, → Opening Drive), FAUNA+ chain/grace reset (912–1004), Katana yesterday-state carry (1044–1073), Typhoon/Gripen/Tomcat 1st-bar gates. `time("D")` is **exchange-local day** with DST. Python must reproduce day bucketing in **America/New_York** with correct DST transitions and the exchange session calendar (RTH vs ETH must match how the chart was set). This is the highest-leverage Class-B port — get it wrong and every "first bar" and every cross-session signal misaligns by one bar.

### 3.5 `barstate.isconfirmed` (Class B)

`conf` (line 197) and direct `barstate.isconfirmed` gate nearly every signal and all stateful array mutations (PB&J 681, FAUNA+ chains, Yin-Yang 432/439/450). In a bar-replay Python engine, "confirmed" = closed bar. Process only closed bars; do not emit on the forming bar. The few unconfirmed-bar-sensitive pieces (`reg_adjustRealtime`) are dead. Map `barstate.isconfirmed → bar is closed` and parity holds.

### 3.6 Bar-offset alignment (`-moff`, `-yy_rightBars`, `f_align`) (Class B)

Lines 754–806: `moff = i_req_fvg ? 1 : 0` and `f_align(sig)=sig[moff]`; Typhoon plots at `-yy_rightBars` (=1). These are **plot-position offsets** (paint the marker N bars back so it lands on the originating bar). They do not change detection logic, only the bar index the marker is attached to. In a decoupled system, record the signal on its true originating bar and apply the offset only in the visual layer; do not let offsets shift the recomputed signal's timestamp.

---

## 4. Parity gotchas (checklist)

1. **5000-bar volume warmup.** `ta.highest(volume,5000)` (212, 475) → load ≥5001 (target 6000) closed bars before HV / GZ1-HV / Nagasaki / Whale are valid. Earlier bars produce false "milestone" hits because the max window is under-filled. `[1]` shift on line 212 means the milestone is evaluated against history *excluding the current bar* — replicate the lag exactly.
2. **"Ever" running maxes are history-depth-dependent.** `nag_maxVol` (482–489) and `wh_maxVolEver` (526–528) seed from `bar_index==0` / first loaded bar. Their truth depends on how far back history loads. Anchor to a fixed epoch (e.g., earliest available massive bar per symbol) so the running max is reproducible run-to-run.
3. **mintick per-symbol.** Source tick size per ticker (Massive reference/ticker-details), not a global constant. Drives PB&J level creation (618) → cascades to ~7 combo families.
4. **New-day clock + DST + session.** `ta.change(time("D"))` (731) must be reproduced in America/New_York with DST and the same session definition (RTH vs ETH) used on the chart. This is the single biggest behavioral risk: it governs every FIRST-BAR-ONLY gate, `sessionBarCount`, Opening Drive, FAUNA+ chain reset, and Katana cross-session carry.
5. **relativeVolume anchoring/realtime.** `tv_ta.relativeVolume(..., reg_anchorTimeframe="", "Regular", adjustRealtime=true)` (337) — anchor `""` = chart TF (no HTF reset); Regular = per-bar; realtime adjust = live-bar-only projection. **Currently dead (output unused).** Drop it, or port per §3.1. Zero parity impact today.
6. **barstate semantics.** `conf`/`isconfirmed` everywhere = process closed bars only; stateful arrays (PB&J, GZ1 FVG list, Yin-Yang SR list) must mutate **once per closed bar, in chronological order** — replay order matters or array contents diverge.
7. **`timeframe.in_seconds(timeframe.period)`** (273) feeds the RVOL threshold ladders (277–308). Reproduce from the bar interval (e.g., 60 for 1m). Wrong tf-seconds → wrong Grand Slam/MOAB/SAAB thresholds.
8. **Stateful array ordering & caps.** GZ1 FVG array (cap 50, line 267), Yin-Yang SR (cap 50, 469), PB&J bull/bear lvls (cap 30, 692–695) — caps and unshift/pop order must match Pine exactly for GZI/PB&J/breakout parity.
9. **Orphaned signals to drop in the Python port (not just relVol):** `relVolRatio` (338), `sigAnishBull/Bear` (515–516), `sigGripenBull/Bear` (841–842) are computed but never plotted/alerted in this file. Replicate only if you intend to surface them; otherwise omit for speed.

---

*Audit complete. Class distribution: ~95% Class A, remainder Class B (session/mintick/barstate/offset), exactly 1 Class C (dead), 0 Class D. Massive OHLCV is sufficient for 100% of live detection plots.*
