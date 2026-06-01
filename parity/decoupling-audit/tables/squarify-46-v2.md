# Decoupling Audit — SQUARIFY 46 v2 (`shorttitle="SQ46 v2"`)

**File audited:** `/Users/anishpatel/Desktop/Indicator studies/"SQUARIFY 46 v2", shorttitle="SQ46 v2".txt` (2622 lines)
**Audit date:** 2026-05-31
**Mission:** prove every detection plot is recomputable from Massive (Polygon) aggregate OHLCV alone in a Python candle factory (5 TFs × 6000 bars); flag anything that is not.

---

## 1. Verdict

**SQUARIFY 46 v2 is 100% recomputable from OHLCV alone. ZERO blockers (no CLASS D).** Every one of the 46 named plots plus the two extra Tier-1/Tier-2 confluence plots is a pure deterministic function of the four-or-five OHLCV series (`open, high, low, close, volume`) plus `time` and the resolution period. The script has **zero `request.security`**, **zero external/alternative-data feeds**, **zero fundamentals, options, NOI, news, or 13F dependencies**. The only non-`ta.*`/`math.*` library call is `tv_ta.relativeVolume` (line 449, 1228, 1229), an **open-source TradingView library** whose entire algorithm is OHLCV volume bucketed by intra-period elapsed time — fully portable (CLASS C, the single flagged item). Everything else is CLASS A (pure OHLCV + `ta.*` + `math.*`) or CLASS B (CLASS A wrapped in session/new-day/`mintick`/`barstate` gating). The dominant parity risks are **not** data-availability risks; they are **arithmetic-fidelity** risks: (a) faithfully porting `tv_ta.relativeVolume` including its `adjustRealtime` behavior and anchor semantics; (b) reproducing TradingView's exact `ta.*` recursion/seed conventions (EMA/RMA/ATR/stdev/pivot/linreg) bar-for-bar; (c) reproducing the deep stateful `var` arrays (TNT zones, Ping Pong S/R, GZ FVG, charge ladders, Boom Hunter IIR filters) which are path-dependent and demand a warmup of ≥1500 bars (`max_bars_back=1500`) and an all-time-high accumulator (`maxVolEver`, `maxVol`, HEV) that is technically unbounded. With 6000-bar history these are satisfiable. **Decoupling is GREEN. Build the candle factory; the only library you must hand-port is `relativeVolume`.**

---

## 2. Detection-plot dependency table

Class legend: **A** = pure OHLCV + `ta.*`/`math.*`; **B** = A + session/calendar/`mintick`/`barstate`/new-day; **C** = `tv_ta.*` library port; **D** = external/proprietary data (none found).

> Note: every plot multiplies in `tv_ta.relativeVolume` *transitively* because the RVOL engine (WTC/Hiroshima/Pentagon, lines 449–453) and the Long/Short engine (lines 1228–1235) feed dozens of downstream signals. Plots whose direct local logic also references those engines are marked **C (via RVOL)**; otherwise the transitive dependency is noted in Notes. All such plots remain fully recomputable — RVOL itself is OHLCV-derived.

| # | Detection Plot | Line refs | What it detects | Series / inputs used | TV namespaces touched | Class | Massive OHLCV sufficient? | Recreate risk | Notes / mitigation |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **SD! (Super Duper)** | 2227; def 1689 | UC (csNew3) + consolidated Napalm + PUP, same visual bar, offset −1 | csNew3_Bull, det_bullNapalmCons, sigPUP[1] | ta.ema/atr/stdev/crossover; tv_ta.relativeVolume (transitive) | C (via RVOL) | Y | Med | Depends on TNT engine + combo sets + PUP. All OHLCV. Port RVOL once. |
| 2 | **SUPER** | 2228; def 1687 | UC + consolidated Napalm, same bar, offset −1 | csNew3_Bull, det_bullNapalmCons | as above | C (via RVOL) | Y | Med | Same chain minus PUP. |
| 3 | **HW (Heavy Weapon)** | 2229; def 1357 | Green + 5σ disp (no FVG) + PBJ + (GS/WTC/Hiro/dirNag) + Platform | disp5_bull, sigBullPBJ, RVOL tiers, bull_pp | ta.stdev/ema/atr/crossover/pivot; tv_ta RVOL (WTC/Hiro) | C (via RVOL) | Y | Med | WTC/Hiroshima come from `relVolRatio` (line 451-452). |
| 4 | **FLOOR** | 2230; def 2156 | Ping Pong bull support + PBJ + dir RVOL + checkbox Set1 | bull_pp, sigBullPBJ, bull_hw_slot, cb1_pass_floor | ta.pivothigh/low/atr/ema; mintick (Ping Pong tol) | C (via RVOL) | Y | Med | Ping Pong S/R is stateful `var` arrays + `syminfo.mintick` (line 763) → CLASS B element folded in. mintick from Massive tick size table. |
| 5 | **2F (2nd Floor)** | 2231; def 2157 | Ping Pong bull + PB (not PBJ) + dir RVOL + checkbox Set1 | anyBull2nd, oneOfThese, cb1_pass | same as #4 | C (via RVOL) | Y | Med | Mirror of FLOOR with PB instead of PBJ. |
| 6 | **UUUU** | 2232; def 913-968 | 4+ consecutive qualified U bars, paths A–G | u_bull_streak, bb_normalizedPrice, PBJ/DISP/FAUNA/SAAB/RVOL1x/GS, is_new_day | ta.sma; time("D") new-day; tv_ta RVOL | C (via RVOL) | Y | Med | `pA` uses new-day (CLASS B). SUB-2MIN gate uses tfSec. |
| 7 | **UUU** | 2233; def 971-1023 | 3 consecutive qualified U bars | as #6 | as #6 | C (via RVOL) | Y | Med | Same. |
| 8 | **UU** | 2234; def 1026-1078, gate 2158 | 2 consecutive qualified U bars + oneOfThese_forUU | as #6 | as #6 | C (via RVOL) | Y | Med | Same. |
| 9 | **A★ (Alpha Strike)** | 2235; def 2150 | First-of-day + Ping Pong bull + (GS or RVOL1x) + PBJ + expanded FAUNA | firstOfDay, bull_pp, sigBullPBJ, as_fauna_expanded | ta.pivot/atr/sma; new-day (firstOfDay via is_new_day) | C (via RVOL) | Y | Med | firstOfDay reset on `is_new_day` (line 1220) → CLASS B. |
| 10 | **ΩA (Omega-A)** | 2236; def 1774 | Boom Hunter omega event + high-conf cosignal, not MOAB/bear-disp | bh_anyOmega, omega_cosignal_A | ta.ema/sma/rsi/linreg/pivot/crossover/barssince; math.exp/cos/asin | C (via RVOL) | Y | **High** | Boom Hunter = Ehlers IIR high-pass + super-smoother filters (lines 1694-1764). Heavily recursive; needs exact `ta.ema` seed + long warmup. Cosignal pulls RVOL. |
| 11 | **FOX (Foxtrot)** | 2237; def 2159 | 4 consecutive FAUNA-confirmed bull bars, gated | sigFoxtrotBull (1224), hvd_pbj_bull/oneOfThese | ta.atr/sma | C (via RVOL) | Y | Med | FAUNA pure OHLCV; gate touches RVOL transitively. |
| 12 | **OD (Opening Drive)** | 2238; def 1268 | Session bar ≤ max + FVG combo + disp + PUP[1] + PBJ[1], offset −1 | sessionBarCount, od_fvg_bull, disp_prevDisp, sigPUP[1], sigBullPBJ[1] | new-day session counter; ta.stdev | C (via RVOL) | Y | Med | `sessionBarCount` from `is_new_day` (CLASS B). od_fvg pulls combo sets (RVOL). |
| 13 | **GOLF** | 2239; def 1276 | 3-bar: bar[2]=FAUNA+PUP, bar[1]=FAUNA+PUP+DISP, bar[0]=DISP, offset −1 | sigDISPBull, sigFAUNABull[1,2], sigPUP[1,2] | ta.stdev/sma/atr | A | Y | Low | Pure OHLCV; no RVOL, no session. CLASS A. |
| 14 | **PBJ+F2/E3** | 2242; def 2002 | PBJ + Foster Pair or Exhaustion Triple | sigBullPBJ, sBullF2, sBullE3 | u57 session (time NY tz), ta.ema/atr/sma | B | Y | Med | F2/E3 use u57 session counter w/ `time(..,"0930-1600","America/New_York")` (line 1847) → NY tz/DST CLASS B. |
| 15 | **PBJ+CL** | 2243; def 2003 | PBJ + full FAUNA Cluster | sigBullPBJ, sBullFC | u57 session; arrays; ta.sma | B | Y | Med | Cluster (sBullFC, line 1924) uses u57 session + overlap arrays. |
| 16 | **F2CL→E3** | 2244; def 2004 | Sequential Foster Pair + Cluster then Exhaustion Triple | sBullF2[1], sBullFC[1], sBullE3 | as #14/#15 | B | Y | Med | Same session dependency. |
| 17 | **E3⅔PP** | 2245; def 2010 | Exhaustion Triple w/ 2 of 3 bars PUP | sBullE3, pupCntE3 | u57 session; PUP | B | Y | Med | |
| 18 | **F2×2D** | 2246; def 1998 | Foster Pair on consecutive sessions | sBullF2, f_hadYesterday | dayofmonth lookback (≤500 bars) | B | Y | Med | `f_hadYesterday` (line 1988) scans up to 500 bars using `dayofmonth` calendar. CLASS B. |
| 19 | **E3×2D** | 2247; def 1999 | Exhaustion Triple on consecutive sessions | sBullE3, f_hadYesterday | dayofmonth lookback | B | Y | Med | |
| 20 | **F2E3seq** | 2248; def 2000 | Foster Pair one session, Exhaustion Triple next | sBullE3, f_hadYesterday(sBullF2) | dayofmonth lookback | B | Y | Med | |
| 21 | **CL×2D** | 2249; def 2001 | FAUNA Cluster on consecutive sessions | sBullFC, f_hadYesterday | dayofmonth lookback | B | Y | Med | |
| 22 | **NPM+** | 2252; def 2173 | Napalm + ((PBJ+(UC/HW/WBUSH)) OR WBUSH), offset −1 | det_bullNapalmCons, sigBullPBJ[1], csNew3_Bull, hwBull[1], sigWMD[1] | TNT engine (ta.ema/atr/stdev/highest/median/rsi); RVOL | C (via RVOL) | Y | Med | Napalm from TNT propulsion engine, OHLCV-only. WBUSH pulls RVOL. |
| 23 | **NPM12** | 2253; def 2162 | Napalm + checkbox Set1 OR Set2, offset −1 | det_bullNapalmCons, cb1_pass_npm, cb2_pass_npm | TNT; RVOL (via d9/combo in checkbox) | C (via RVOL) | Y | Med | |
| 24 | **NPM3** | 2254; def 2163 | Napalm + checkbox Set3 (only when NPM12 off), offset −1 | det_bullNapalmCons, cb3_pass_npm | as #23 | C (via RVOL) | Y | Med | |
| 25 | **B2BNPM** | 2255; def 1663 | Back-to-back consolidated Napalm | det_bullNapalmCons[0,1] | TNT engine | A | Y | Med | TNT engine is pure OHLCV (no RVOL). CLASS A but deeply stateful. |
| 26 | **NPM+TNT** | 2256; def 1665 | Napalm + TNT same candle | raw_napalmBull, raw_bullTNT[1] | TNT engine | A | Y | Med | Pure OHLCV; stateful zones. |
| 27 | **CO** | 2259; def 1827 | HV+D + PBJ + (UC OR FVG combo set), offset −1 | hvd_fire_bull, sigBullPBJ[1], co_uc_or_fvg_bull | HV+D (volume highest), combo sets (RVOL) | C (via RVOL) | Y | Med | hvd_fire_bull = volume-rank + displacement, pure OHLCV; combo sets pull RVOL. |
| 28 | **HVD+PBJ** | 2260; def 1810 | HV+D + PBJ same candle (sub-3min needs checkbox), offset −1 | hvd_pbj_bull, tfSec, cb1_pass_npm | ta.highest(volume); tfSec | C (via RVOL) | Y | Med | tfSec gate (CLASS B). Checkbox pulls RVOL. |
| 29 | **B2BHVD+PBJ** | 2261; def 1836 | Consecutive HV+D + PBJ on either bar, offset −1 | b2b_bull_raw, sigBullPBJ[1,2] | ta.highest(volume), ta.stdev | A | Y | Low | HV+D + PBJ are OHLCV-only. CLASS A. |
| 30 | **B2BHVD** | 2262; def 1840 | Consecutive HV+D without PBJ, offset −1 | b2b_bull_nopb | ta.highest(volume), ta.stdev | A | Y | Low | CLASS A. |
| 31 | **UU+UC** | 2263; def 2209 | Any UU family + Unified Combo same candle, offset −1 | uu_any, csNew3_Bull | UU streak; combo sets (RVOL) | C (via RVOL) | Y | Med | |
| 32 | **GRAIL** | 2266; def 2176 | Napalm + PBJ + PUP + UC all same bar, offset −1 | det_bullNapalmCons, sigBullPBJ[1], sigPUP[1], csNew3_Bull | TNT; RVOL (combo) | C (via RVOL) | Y | Med | The Holy Grail confluence. |
| 33 | **FLR+NPM** | 2267; def 2179 | Floor + Napalm same candle, offset −1 | anyBullFloor[1], det_bullNapalmCons | Ping Pong + TNT; RVOL | C (via RVOL) | Y | Med | |
| 34 | **NPM+PBJ+PUP** | 2268; def 2182 | Napalm + PBJ + PUP without UC, offset −1 | det_bullNapalmCons, sigBullPBJ[1], sigPUP[1] | TNT | A | Y | Med | No RVOL, no session. Stateful TNT. CLASS A. |
| 35 | **NAG+** | 2269; def 2185 | Nagasaki + any bull signal | sigNagasaki, RVOL1x/GS/FAUNA/DISP/PBJ/PUP/GZ | maxVol all-time accumulator; RVOL | C (via RVOL) | Y | Med | Nagasaki = all-time-high volume (`maxVol`, line 455-462). Unbounded accumulator — see gotchas. |
| 36 | **UU+HVD** | 2270; def 2188 | UU[1] + HV+D + PBJ, offset −1 | sigUU*[1], hvd_pbj_bull | UU streak; HV+D | C (via RVOL) | Y | Med | |
| 37 | **UU+NPM** | 2271; def 2191 | UU[1] + Napalm, offset −1 | sigUU*[1], det_bullNapalmCons | UU; TNT | C (via RVOL) | Y | Med | |
| 38 | **FLR+UU** | 2272; def 2194 | Floor or 2F + any UU family | anyBullFloor/anyBull2nd, uu_any | Ping Pong; UU; RVOL | C (via RVOL) | Y | Med | |
| 39 | **FOS+PUP+1x** | 2273; def 2197 | Foster + PUP + (RVOL1x or Napalm) | fosterPBJSignal, sigPUP, sigBullRVOL1x/Napalm | u57 session (Foster); RVOL | C (via RVOL) | Y | Med | Foster window uses u57 session. |
| 40 | **NPM+UC** | 2276; def 2203 | Napalm + UC without PBJ, offset −1 | det_bullNapalmCons, csNew3_Bull | TNT; RVOL (combo) | C (via RVOL) | Y | Med | |
| 41 | **WBUSH+ANY Bull** | 2279; def 2067 | Any of 5 Heavy Combos firing bull (Yin-Yang/Nag/NagVol/Trident/NHx2) | hp_* bases (RVOL tiers, Pentagon, WTC, Hiro, Nagasaki) + sigDISPBull | tv_ta RVOL (Pentagon/WTC/Hiro = relVolRatio); maxVol (Nag) | **C** | Y | Med | **Direct** RVOL consumer: Pentagon/WTC/Hiroshima all from `relVolRatio` (lines 451-453). |
| 42 | **WBUSH+ANY Bear** | 2280; def 2068 | Mirror of 41, bear | as #41 | as #41 | **C** | Y | Med | |
| 43 | **WBUSH Neutral** | 2281; def 2069 | Any of 5 Heavy Combos, no FVG-disp either way | hp_* bases + hp_noDisp | as #41 | **C** | Y | Med | |
| 44 | **NPM+UC+PBJ** | 2284; def 2206 | Napalm + UC + PBJ, offset −1 | det_bullNapalmCons, csNew3_Bull, sigBullPBJ[1] | TNT; RVOL | C (via RVOL) | Y | Med | |
| 45 | **UC NAGASAKI Bull** | 2287; def 2076 | Unified Combo + Nagasaki same visual bar, offset −1 | csNew3_Bull, sigNagasaki[1] | combo sets (RVOL); maxVol | C (via RVOL) | Y | Med | |
| 46 | **UC NAGASAKI Bear** | 2288; def 2077 | Mirror of 45, bear | csNew3_Bear, sigNagasaki[1] | as #45 | C (via RVOL) | Y | Med | |
| — | **T1 Opening Confluence** (extra plot) | 2486; def 2479 | First session bar + disp ≥8σ + UC + HV+D + RVOL1x | stats_sessBar, disp_rng/disp_std, csNew3_Bull, hvd_fire_bull, sigBullRVOL1x | new-day session; ta.stdev; RVOL1x (bb_normalizedPrice) | C (via RVOL) | Y | Med | Not in the "46" but emits a plotshape + alert. CRWV recipe. RVOL1x is from bb engine, not tv_ta. |
| — | **T2 Opening Confluence** (extra plot) | 2514; def 2508 | First 2 session bars + B2B PUP + UU family | stats_sessBar, det_b2bPUP, uu_any | new-day session; PUP; UU; RVOL (UU) | C (via RVOL) | Y | Med | Not in the "46". |

### Underlying engine source-classes (these feed the plots above)

| Engine / building block | Lines | Class | OHLCV sufficient? | Notes |
|---|---|---|---|---|
| HV+D Pipeline A (volume rank + displacement FVG) | 60-308 | A | Y | `ta.highest(volume,N)`, `ta.stdev`. HEV = unbounded all-time accumulator (line 274). TF-activation uses tfSec (B). |
| RVOL bb engine (SAAB/Kratos/GS/MOAB/RVOL1x) | 426-447 | A | Y | `ta.sma(close-open)`, `ta.sma(volume)` — NOT tv_ta. Pure OHLCV. |
| **tv_ta.relativeVolume (WTC/Hiroshima/Pentagon)** | 449-453 | **C** | Y | **The one flagged port.** See §3. |
| Nagasaki (all-time-high volume) | 455-462 | A | Y | Unbounded `maxVol` accumulator. |
| FAUNA (MB/RE/TA/GG candle anatomy) | 474-506 | A | Y | `ta.atr/sma`. Pure OHLCV candle morphology. |
| USE Displacement 1/2/3 + streaks | 508-555 | A | Y | `ta.stdev`. |
| GZ1 / HV FVG (gap-zone intersection arrays) | 557-612 | A | Y | `ta.highest(volume,5000/252/63)`, `ta.cum`. Stateful array. 5000-bar lookback. |
| PUP/PPD | 614-619 | A | Y | `ta.highest` over signed volume. |
| PBJ / Zoo Supertrend (Pipeline B) | 621-745 | B | Y | `ta.ema/atr/vwma/hma/wma`, `syminfo.mintick` (line 668). CLASS B for mintick. |
| Ping Pong S/R (Pipeline C) | 747-882 | B | Y | `ta.pivothigh/low/atr`, `syminfo.mintick`×buffer (line 763). Stateful `var` line arrays. |
| UU/UUU/UUUU streak engine | 884-1212 | C (via RVOL) | Y | Uses bb_normalizedPrice + RVOL signals + new-day. |
| Matrix Number (Neo/Trinity) | 1214-1216 | A | Y | `ta.highest(volume,neo_len)`. |
| Foxtrot / first-of-day | 1218-1225 | B | Y | new-day reset. |
| Long/Short engine (uses tv_ta RVOL ×2) | 1227-1238 | **C** | Y | **Direct tv_ta.relativeVolume** calls (lines 1228-1229). |
| Combo Sets 1-4 + csNew1/2/3 (Unified Combo) | 1240-1257 | C (via RVOL) | Y | Pulls RVOL tiers + GZ + matrix. |
| Combo Chain / LS Chain | 1281-1342 | C (via RVOL) | Y | |
| TNT Propulsion + Napalm + Charge engine | 1360-1665 | A | Y | `ta.ema/atr/highest/lowest/median/rsi/stdev`. Pure OHLCV, deeply stateful zones/ladders. |
| Boom Hunter (Ehlers IIR) + Omega | 1692-1774 | A | Y | `math.exp/cos/sin/asin`, `ta.ema/sma/rsi/linreg/pivot/barssince/crossover`. Recursive filters. |
| Ultra-57 FAUNA combos (F2/E3/Cluster/Foster) | 1844-2024 | B | Y | `time(...,"0930-1600","America/New_York")` session + dayofmonth. |
| Heavy Pentagon → WBUSH | 2026-2072 | C (via RVOL) | Y | Pentagon/WTC/Hiro from RVOL. |
| Stats engine (percentrank, fwd returns, geometry) | 2401-2621 | B | Y | `ta.percentrank/rsi/sma`; `time(...,"0930-1000",NY)`; output-only (log.info). |

---

## 3. Flagged dependencies

### 3.1 CLASS C — `tv_ta.relativeVolume` (the ONLY library port). DEEPEST TREATMENT.

**Import:** line 37 `import TradingView/ta/7 as tv_ta`.
**Call sites:**
- Line 449 (RVOL engine): `[currentVolume_reg,pastVolume_reg,_unused]=tv_ta.relativeVolume(reg_length, reg_anchorTimeframe, reg_calculationMode=="Cumulative", reg_adjustRealtime)`
- Line 1228 (Long/Short, **non-cumulative**): `tv_ta.relativeVolume(reg_length, reg_anchorTimeframe, false, reg_adjustRealtime)`
- Line 1229 (Long/Short, **cumulative**): `tv_ta.relativeVolume(reg_length, reg_anchorTimeframe, true, reg_adjustRealtime)`

**Hardcoded arguments (line 320):** `reg_anchorTimeframe = ""`, `reg_length = 30`, `reg_calculationMode = "Cumulative"`, `reg_adjustRealtime = true`. So in production: **length=30, anchor="" (auto), cumulative=true, adjustRealtime=true** for line 449; and BOTH cumulative=false (line 1228) and cumulative=true (line 1229) are computed for the L/S engine.

**Signature (TradingView/ta/7):**
`relativeVolume(float length, string anchorTimeframe = "", bool isCumulative = true, bool adjustRealtime = false) → [float currentVolume, float averageVolume, bool isFilled]`

Returns a tuple: `[currentVolume, averageVolume, isFilled]`. The script computes `relVolRatio = currentVolume / averageVolume`. The third element is discarded (`_unused`, `_r2`, `_c2`).

**Semantics — what it actually computes (OHLCV-only):**
1. **Anchor timeframe** (`anchorTimeframe`): defines the period over which "cumulative" volume accrues and against which the historical average is bucketed. **Empty string `""` = AUTO**: TradingView picks an anchor coarser than the chart resolution by its standard auto rule (intraday chart → daily anchor; daily chart → yearly; etc.). For Anish's intraday candle factory the auto-anchor on a 1m/5m/15m/1h chart resolves to the **trading day (session)**. So the "anchor reset" is **session-open** in RTH terms.
2. **`isCumulative = true`:** `currentVolume` = running **sum** of bar volume from the anchor reset (session open) up to and including the current bar. `averageVolume` = the average, across the last `length` (=30) prior anchor-periods, of the cumulative volume **at the same elapsed offset into the period**. I.e. it compares "volume accumulated so far today, at this minute-of-session" against "the typical volume accumulated by this same minute-of-session over the last 30 sessions." This is the classic intraday cumulative-RVOL curve.
3. **`isCumulative = false`** (line 1228): `currentVolume` = **this single bar's** volume; `averageVolume` = average of the volume at the **same intra-period slot** over the last 30 periods. Per-slot RVOL, not cumulative.
4. **`adjustRealtime = true`:** on the still-forming (last/realtime) bar, the partial elapsed fraction of the period is used to **pro-rate** the historical comparison so an incomplete bar isn't unfairly compared to full historical bars. On **closed/historical bars this is a no-op.** Since the candle factory recomputes on **closed bars only** (everything is gated by `barstate.isconfirmed` / `freq_once_per_bar_close`), `adjustRealtime` has **NO effect on parity** for backfilled history — it only matters for the live forming bar, which the parity harness should evaluate at close anyway.

**Exact port algorithm from Massive intraday bars (session-anchored, length=30):**
```
# Inputs: per-bar (ts, volume) at chart resolution. RTH session anchor.
# Build "slot" key = ordinal bar index within the session (0,1,2,... from session open),
#   OR elapsed-seconds-into-session bucketed to the bar resolution. Use ordinal slot
#   when bars are regular; use elapsed-seconds when bars can be missing.
for each session S:
    cum = 0
    for each bar b in S (in order):
        slot = b.index_within_session            # 0-based
        cum += b.volume
        # history of the SAME slot over the prior `length` sessions:
        hist_cum  = [cumvol_at_slot(s, slot)  for s in prior 30 sessions if slot exists]
        hist_perbar = [volume_at_slot(s, slot) for s in prior 30 sessions if slot exists]
        averageVolume_cum    = mean(hist_cum)      # isCumulative=true
        averageVolume_perbar = mean(hist_perbar)   # isCumulative=false
        currentVolume_cum    = cum
        currentVolume_perbar = b.volume
        relVolRatio_cum    = currentVolume_cum    / averageVolume_cum
        relVolRatio_perbar = currentVolume_perbar / averageVolume_perbar
# adjustRealtime: only for the live in-progress bar — pro-rate hist by elapsed fraction.
#   For closed-bar parity, skip it.
```
**Validation against TV:** lift `currentVolume`/`averageVolume` directly via `data_get_study_values` / `pine_get_console` (the stats engine already logs `RVOL_MULT`) and assert your port matches bar-for-bar on a handful of tickers/sessions before trusting downstream signals.

**Blast radius — which of the 46 consume RVOL (directly or transitively):**
- **Direct** (`relVolRatio` from line 449): WTC, Hiroshima, Pentagon (lines 451-453) → these feed **WBUSH 41/42/43** (Heavy Pentagon), **HW 3**, **Floor 4 / 2F 5** (bull_hw_slot), **Combo Set 2/4**, **Omega cosignal (ΩA 10)**, **NAG+ 35**, **UC NAGASAKI 45/46** (via combo sets), **UU* family 6/7/8** (bsaab path).
- **Direct** (lines 1228-1229, L/S engine `ls_regRatio`/`ls_cumRatio`): **Long1/Long2** → **Combo Chain (sigCCBull) 27-feeders**, **LS Chain 38-feeders**, **Matrix-aligned combos**, **Omega cosignal**, **UU pD/pE paths**, **T1 confluence indirectly**.
- **Transitive (via combo sets csNew1/2/3 = Unified Combo):** **SD! 1, SUPER 2, CO 27, UU+UC 31, GRAIL 32, NPM+UC 40, NPM+UC+PBJ 44, UC NAGASAKI 45/46, T1 27** and any "UC" plot.
- **NOT touching RVOL at all (CLASS A, safe even if RVOL port were wrong):** **GOLF 13, B2BHVD+PBJ 29, B2BHVD 30, NPM+PBJ+PUP 34, B2BNPM 25, NPM+TNT 26** (TNT/FAUNA/PUP/HV-D/PBJ only). Use these as your **RVOL-independent parity control group**.

**Realtime-adjustment parity risk:** LOW for backfill (closed bars), because every signal is `conf`-gated. The ONLY parity divergence from `adjustRealtime` would occur if the Python factory evaluates a *partial* forming bar differently than TV's live bar. Mitigation: **only emit signals on closed bars** (which the script already does), and `adjustRealtime` becomes irrelevant. Note line 449 passes `true` but lines 1228-1229 also pass `true`; keep them consistent in the port and disable the realtime pro-rate in the offline/backfill path.

### 3.2 CLASS D — BLOCKERS
**NONE.** As expected. No `request.security`, no fundamentals, options, NOI/imbalance, news, 13F, ETF flows, or any non-OHLCV feed anywhere in 2622 lines. `syminfo.ticker` (lines 2495, 2523, 2551) is cosmetic string interpolation in alert/log payloads only — zero effect on signal logic or parity.

---

## 4. Parity gotchas (bar-for-bar fidelity vs TradingView)

1. **Warmup / lookback depth.** `max_bars_back=1500` (line 36). Hard lookbacks observed: `ta.highest(volume,1000)` (#260, 1273), `ta.highest(volume,5000)` (GZ HV, line 566), `ta.highest(volume,252)`/`63`, `ta.pivot*`, `ta.linreg(...,21)`, Boom Hunter IIR (needs ~hundreds of bars to settle), RVOL length=30 **sessions** (=30 days of intraday bars). **The 5000-bar HV lookback and 30-session RVOL anchor are the binding constraints.** 6000-bar history per TF satisfies the 5000-bar window; ensure intraday history spans ≥30 full RTH sessions for RVOL. Begin trusting signals only after bar 5000 (or after the longest window has fully populated). Pivots have a `rightBars` look-ahead — a pivot at bar i is only confirmed at bar i+rightBars; replicate this lag exactly.

2. **`syminfo.mintick` sourcing.** Used at line 668 (PBJ level dedup: `math.abs(up-lo)>=syminfo.mintick`) and line 763 (Ping Pong tolerance: `math.max(syminfo.mintick*pp_buffer_ticks, syminfo.mintick/10)`, `pp_buffer_ticks=10`). **Massive provides tick size via reference/ticker metadata; for US equities ≥ $1 it is $0.01, sub-$1 it is $0.0001.** Hardcode/lookup per symbol. A wrong mintick shifts Ping Pong level merging → can change FLOOR/2F/A★/FLR+* firing. Medium risk; validate on a low-priced name.

3. **Session / DST correctness.** Two NY-tz session masks: `time(timeframe.period,"0930-1600","America/New_York")` (u57, line 1847) and `time(timeframe.period,"0930-1000","America/New_York")` (stats window, line 2412). **Must use a DST-aware America/New_York calendar** (not a fixed UTC offset). Massive timestamps are epoch-UTC; convert to America/New_York with a tz database so 09:30-16:00 RTH tracks the EST/EDT shift correctly. Getting DST wrong shifts every Ultra-57 combo (#14-21, #39) and the stats window by an hour on the wrong days.

4. **New-day detection.** `ta.change(time("D"))!=0` (lines 56, 465, 2436) and `ta.change(dayofmonth)!=0` (lines 1849, 1871, 1931, 1987). `time("D")` rolls at the **exchange daily boundary** (session/calendar day), while `dayofmonth` rolls at the **bar's calendar date**. **These can differ around the session boundary and across DST** — replicate each exactly as written; do not unify them. New-day drives `is_new_day`, `sessionBarCount`, `u57_sessBar`, `firstOfDay`, UU `hasDay1`, and the F2/E3 "consecutive sessions" logic. The `f_hadYesterday` scan (line 1988) walks back up to 500 bars across `dayofmonth` changes — port the loop bound and early-break verbatim.

5. **`barstate.isconfirmed` semantics.** `conf` (line 41) gates almost every signal. In the offline factory, **every bar is "confirmed"** (no realtime). So `conf` ≡ true for all backfilled bars — fine. The subtlety: signals defined as e.g. `volume[1]==ta.highest(volume,N)[1]` describe **bar N-1** and plot with `offset=-1`. Preserve the [1]/[2] index shifts and the plot offsets exactly, or your fire-bar timestamps drift by one bar versus TV's visual.

6. **Stateful path-dependence (the real fidelity tax).** TNT zones (`tnt_z`), charge ladders (`cl_t`), Ping Pong `srLevels`, GZ `gz_fvgs`, Boom Hunter recursive `bh_HP/bh_Filt/bh_Peak`, and the `var` streak counters are all **order-dependent accumulators**. They must be computed by a **single forward pass** over the full 6000-bar history (no vectorized shortcut that ignores prior state), and the array prune bounds (`>30`, `>50`, `>100`, `maxZones_t=15`, `>500`) must match. Any divergence compounds forward.

7. **All-time-high accumulators are unbounded.** `maxVolEver` (line 274, HEV), `maxVol` (line 455, Nagasaki), `_hev_pending`. These reference the **entire visible history**, not a rolling window — so HEV/Nagasaki firing depends on **how far back your history starts.** TradingView's value depends on its loaded bars too; to match, **start both series from the same first bar** as the TV chart (or accept that HEV/Nagasaki/NAG+ #35, UC NAGASAKI #45/46 are sensitive to history origin and validate their first-fire bar explicitly).

8. **`ta.*` seed/recursion conventions.** EMA/RMA(ATR via `ta.atr`)/stdev/linreg/percentrank/median/pivot must replicate **TradingView's exact seeding** (e.g., `ta.ema` seeds with SMA of first `length` bars; `ta.atr` uses RMA, not SMA; `ta.stdev` is population, biased). Use a library that matches TV (or port the recurrences directly) rather than pandas defaults (which differ on ddof and EMA seeding). This is the most common silent parity break. Validate each primitive against `data_get_study_values` before composing signals.

9. **Output-only constructs (no parity impact).** `alert()` (lines 2389, 2398, 2495, 2523), `alertcondition` (2491, 2519), `log.info` (2621), all `plotshape` cosmetics, line/label/box drawings (Ping Pong/TNT visuals), and `str.format_time`/`syminfo.ticker` string building are **presentation/notification only**. They do not affect the boolean signal values and can be replaced wholesale by the candle-factory's own emit layer.
