# Parity Audit — Ultra Combo v57

**File audited:** `/tmp/IND_ULTRA.txt` (1149 lines, read in full — lines 1–943 + 944–1149)
**Auditor goal:** Determine, plot-by-plot, whether every detection marker can be rebuilt EXACTLY from Massive minute-aggregate OHLCV(+volume) candles, or whether any plot needs data TradingView supplies that local candles do not.

---

## 1. Declaration & Header Facts

| Property | Value | Line |
|---|---|---|
| `@version` | **6** | 1 |
| Declaration | `indicator("Ultra Combo v57", shorttitle="ULTRA v57", overlay=true, max_labels_count=500, max_bars_back=2000)` | 12 |
| `overlay` | **true** | 12 |
| `max_bars_back` | **2000** | 12 |
| `max_labels_count` | 500 | 12 |
| External imports | **`import TradingView/ta/7 as tv_ta`** (line 349) — ONE external library | 349 |

**CRITICAL find #1 (grep-missed external):** line 349 imports the official TradingView `ta/7` library and line 350 calls `tv_ta.relativeVolume(30, "", false, true)`. This is NOT `request.security`, but it IS code that does not live in this file. It must be re-derived, not assumed. Analyzed in §5.

**CRITICAL find #2 (the 5000-bar question, line 773):** `isHV = volume[1] == ta.highest(volume, 5000)[1] or ... 252 ... or ... 63`. The 5000-bar lookback directly collides with Anish's "~6000 bars" plan and `max_bars_back=2000`. Analyzed in §5.

**No `request.security`, `request.financial`, `request.dividends`, `request.splits`, `request.economic`, `request.quandl`, `syminfo.*` price feeds, or `[1]`-on-another-symbol calls exist anywhere in the file.** Confirmed line-by-line. The only non-OHLCV inputs touched are `volume`, `time()`, `dayofmonth`, `bar_index`, `syminfo.mintick`, `syminfo.timezone` (implicit via session), `timeframe.in_seconds`/`.period`, and `barstate.*`. All reproducible from Massive candles + a known timeframe + a known exchange-tz.

---

## 2. STATUS TABLE — Every Detection Plot / Alert

Plots are at lines 1018–1068; alerts 1073–1128; alertconditions 1133–1147. Combo booleans (lines 828–920) gate them and roll up sub-signals (MB/RE/TA core 99–106, F2/E3/FC 124–299, RVOL/HW 304–364, PBJ/PB 369–519, PUP/PPD 524–579, TB/Foster 584–642, ROC/DISP/FAUNA/Super 647–759, GZ1/HV 764–823). Status of each visible marker = worst status among its inputs.

| # | Detection Plot (line) | Fires on (1-line math) | Inputs | Status | Parity Risk | Mitigation |
|---|---|---|---|---|---|---|
| 1 | PBJ+F2 (1018) | PBJ buy/sell cross + F2 (2 consec MB at sessBar==2) | OHLCV, EMA20, ATR14, VWMA5, ATR10 supertrend, session counter, mintick | YELLOW | RMA-seeded ATR warmup; mintick (424); session (95); isconfirmed (96) | seed RMA per §4; pass mintick+tz as candle metadata |
| 2 | PBJ+E3 (1019) | PBJ cross + E3 (3 consec MB/RE/TA at sessBar==3) | same + sessBar | YELLOW | session counter + ATR warmup | §4 |
| 3 | PBJ+Cluster (1020) | PBJ cross + FC cluster overlap (rvol arrays) | OHLCV, sma30 of |body| & vol, overlap arrays, mintick | YELLOW | array state path-dependent on history start; ATR/sma warmup | §4 + fixed warmup bar offset |
| 4 | PB+F2 (1021) | PB (level-approach) cross + F2 | same as #1 | YELLOW | mintick (423), level arrays, session | §4 |
| 5 | PB+E3 (1022) | PB cross + E3 | same | YELLOW | as above | §4 |
| 6 | PB+Cluster (1023) | PB cross + FC cluster | same | YELLOW | as above | §4 |
| 7 | F2CL→E3 (1025) | F2[1] & FC[1] & E3 | OHLCV+ATR+sma+session | YELLOW | session + warmup | §4 |
| 8 | F2CL+B2B (1026) | F2 & FC & b2bPUP | + PUP (priceUp + vol>highest(redVol,10)) | YELLOW | session + warmup | §4 |
| 9 | B2B+F2 (1027) | b2bPUP/PPD & F2 | OHLCV+vol | YELLOW | session + warmup | §4 |
| 10 | E3⅔PP (1028) | E3 & ≥2 PUP in 3 bars | OHLCV+vol+session | YELLOW | session | §4 |
| 11 | F2×2D (1030) | F2 today & F2 in prior ~2 days (barsPerDay loop) | OHLCV+vol+barsPerDay (tf-derived) | YELLOW | `barsPerDay` from `timeframe.in_seconds`; RTH-bar assumption (390min) | must pass true RTH bar count; Massive includes ext-hours — filter to RTH first |
| 12 | E3×2D (1031) | E3 today & E3 prior day | same | YELLOW | barsPerDay + session | as #11 |
| 13 | F2E3seq (1032) | F2/E3 cross-day pairing | same | YELLOW | barsPerDay + session | as #11 |
| 14 | CL×2D (1033) | FC today & FC prior day | + arrays | YELLOW | barsPerDay + array warmup | as #11 + §4 |
| 15 | HW+Bull (1035) | anyBullHW & sAnyBull | RVOL thresholds (tf-keyed), tv_ta.relativeVolume, Nagasaki cum-max, super combos | YELLOW | tv_ta.relativeVolume (349-352); Nagasaki cum-max history-dependent (357-364) | re-derive relativeVolume per §5; Nagasaki needs full-history max → §5 |
| 16 | HW+Bear (1036) | anyBearHW & sAnyBear | same | YELLOW | same | §5 |
| 17 | GZ/HV+Bull (1040) | (bullGZI or bullHV) & sAnyBull, offset −1 | FVG geometry, isHV (highest vol 5000/252/63), cum range avg | YELLOW | **isHV 5000-bar lookback (773)** vs 6000 bars/max_bars_back=2000; plot offset −1 | §5 — set max_bars_back≥5001 OR cap lookback to available history; render offset −1 in plot layer |
| 18 | GZ/HV+Bear (1041) | bear equivalent | same | YELLOW | same | §5 |
| 19 | HV+GZI+ (1043) | sessBar==2 & bullHV[1] & bullHV & bullGZI, offset −1 | isHV + GZI + session | YELLOW | isHV 5000 (773) + session | §5 |
| 20 | HV+GZI− (1044) | bear equivalent | same | YELLOW | same | §5 |
| 21 | GZ/HV MEGA+ (1048) | gz1MegaBull or hvMegaBull (GZI/HV & superBull & PUP & FAUNA & DISP), offset −1 | full stack incl isHV, stdev100, relativeVolume | YELLOW | isHV 5000 + relativeVolume + stdev100 warmup | §5 |
| 22 | GZ/HV MEGA− (1049) | bear | same | YELLOW | same | §5 |
| 23 | GZ1+HV MEGA+ (1050) | gz1hvMegaBull (both GZI & HV) | full stack | YELLOW | isHV 5000 + relativeVolume | §5 |
| 24 | GZ1+HV MEGA− (1051) | bear | same | YELLOW | same | §5 |
| 25 | OPENER+ (1053) | sessBar==1 & (GZI|HV) & (HW|PBJ|ROC|1stPUP+S-PUP) | session + isHV + HW + EMA50/150/200 stack + ROC/LazyDinosaur EMAs | YELLOW | session anchor (sessBar==1 = first RTH bar); EMA200 + ema200[21] warmup; isHV | RTH-filter candles; long EMA warmup → §4 |
| 26 | OPENER− (1054) | bear | same | YELLOW | same | §4/§5 |
| 27 | 3BAR+ (1056) | PBJ-in-3 & (B2BPUP-in-3 or ≥2 PUP) | OHLCV+vol+PBJ | YELLOW | ATR/EMA warmup | §4 |
| 28 | 3BAR− (1057) | bear | same | YELLOW | same | §4 |
| 29 | FOS+HVY (1059) | anyFoster & (ROC|HW|Super) | bullPass EMA stack (50/150/200/200[21]), 52wk hi/lo(252), window state | YELLOW | EMA200 + 252-bar 52wk window + window var state; isconfirmed | §4 — long warmup + deterministic var init |
| 30 | TB+HVY (1060) | anyTB & (ROC|HW|Super) | same | YELLOW | same | §4 |
| 31 | GZ/HV+HVY+ (1062) | (GZI|HV) & (HW|Super|ROC), offset −1 | isHV + HW stack | YELLOW | isHV 5000 + relativeVolume | §5 |
| 32 | GZ/HV+HVY− (1063) | bear | same | YELLOW | same | §5 |
| 33 | SUPER×2D+ (1065) | anySuperBull & had-super-yesterday | super stack + barsPerDay loop | YELLOW | barsPerDay + isHV/relativeVolume in super stack | §5 + #11 |
| 34 | SUPER×2D− (1066) | bear | same | YELLOW | same | §5 |
| 35 | NAGA (1068) | sigNagasaki = new all-time max volume since bar 0 | volume, running max from bar_index==0 (357-364) | **YELLOW (history-critical)** | Value depends ENTIRELY on where the series starts; "new max vs first 6000 bars" ≠ "new max vs full TV history" | §5 — define explicit anchor: running-max from first loaded candle; document that NAGA is start-of-window relative |
| 36 | NAGA alert (1073-74) | sigNagasaki | volume cum-max | YELLOW | as #35 | §5 |
| 37 | Scan Trigger alert (1076-78) | superBull/Bear PBJ/PB or GS or MOAB | super stack + RVOL thresholds | YELLOW | relativeVolume + warmup | §5 |
| 38 | Opener alert (1080-88) | openerBull/Bear | as #25/26 | YELLOW | session + warmup | §4 |
| 39 | 3Bar alert (1090-96) | threeBar_Bull/Bear | as #27/28 | YELLOW | warmup | §4 |
| 40 | GZ1/HV/HV+GZI/Foster/TB/SuperB2B alerts (1098-1128) | mirror plots 21-34 | full stack | YELLOW | isHV + relativeVolume + barsPerDay | §5 |
| 41 | alertcondition Nagasaki (1133) | sigNagasaki | volume cum-max | YELLOW | as #35 | §5 |
| 42-47 | alertcondition Mega/Opener/3Bar/Foster-TB/GZHV-Heavy/SuperB2B (1134-1140) | mirror combos | full stack | YELLOW | isHV + relativeVolume | §5 |
| 48-53 | alertcondition Scan/PBJ-F2/PBJ-E3/PBJ-CL/HW-Any/GZHV-Any/HV-GZI (1141-1147) | mirror combos | full stack | YELLOW | warmup + isHV/relativeVolume | §4/§5 |

**Sub-signal coverage note:** every named boolean (bull_MB/RE/TA, bear_*, b1_*/b4_* cluster machinery, sigBullRVOL1x/GrandSlam/MOAB/WTC/Hiroshima/Nagasaki, sigBullPB/PBJ + bear, PUP/PPD/superPup/firstPUPPass, fosterSignal/tbSignal families, sigROC/DISP/FAUNA, bullGZI/HV) is consumed by at least one plot/alert above and is therefore classified transitively. None is GREEN-only because every plot ultimately rolls into the YELLOW warmup/session/isHV/library cluster — but the underlying MATH of each is pure OHLCV (see §4 ta inventory). No sub-signal references an external symbol or HTF series.

---

## 3. Tally

- **GREEN: 0** plots are *unconditionally* green. (Every visible plot inherits at least one YELLOW dependency: RMA/EMA warmup, session anchoring, `barsPerDay`, `tv_ta.relativeVolume`, the `isHV` 5000-bar lookback, or the Nagasaki cumulative max.)
- **YELLOW: 53 (all detection plots/alerts)** — reproducible from OHLCV but require the specific mitigations in §4/§5 to match TV bit-for-bit.
- **RED: 0** — nothing requires `request.security`, `request.financial`, dividends/splits, sub-candle tick data, or an external feed. The one external `import` (`tv_ta.relativeVolume`) is a pure-volume math helper, fully re-derivable (§5). Confirmed line-by-line; grep's "zero RED" holds.

**Note on the GREEN count:** the *signal math itself* is GREEN-grade (standard `ta.*`). The plots are graded YELLOW only because of execution-model/warmup/anchor/library wrappers, all of which have concrete, stated mitigations. There is no un-mitigable YELLOW and no RED.

---

## 4. Session / Execution-Model / Warmup Section

**Session anchoring (verbatim):**
- Line 95: `bool inSession = not na(time(timeframe.period, "0930-1600", "America/New_York"))`
- Lines 108–119: session bar counter — `if ta.change(dayofmonth) != 0 isNewDay := true` … `if isNewDay and inSession sessBar := 1` … `else if inSession and sessBar > 0 sessBar += 1` … `else if not inSession sessBar := 0`.
- `sessBar==1/2/3` gate OPENER, F2, E3, HV+GZI combos (lines 208-209, 295-296, 881-882, 891-892).

**Mitigation (session):** Massive minute aggregates carry UTC timestamps including pre/post-market. To match `time(..., "0930-1600", "America/New_York")`:
1. Convert each candle ts to America/New_York (DST-aware — use a tz library, not a fixed −5/−4 offset; TV uses exchange tz which observes US DST).
2. Mark a bar in-session iff its open time ∈ [09:30, 16:00) NY.
3. Derive `sessBar` by the same new-day (`dayofmonth` change in NY tz) + in-session increment logic.
4. **RTH-only candle factory:** `barsPerDay` (lines 17-23) assumes a 390-min RTH day. If the candle factory feeds 24h bars, `barsPerDay` and every `*×2D` / opener signal breaks. Decision: build the indicator series on RTH-filtered candles (matches TV's default regular-session chart), OR replicate TV's session model exactly. RTH-filter is the lower-risk path and matches how Anish charts.

**Execution model:**
- `conf = barstate.isconfirmed` (line 96) gates virtually every event (MB/RE/TA, RVOL, GZ1/HV pushes at 787/802, PB approach at 486). The header comment (line 7) states ALL signals use `isconfirmed` for non-repainting.
- **Mitigation:** trivially satisfied in a batch/local rebuild — every Massive candle is already closed/confirmed. Just evaluate signals on closed bars only. No realtime/intrabar ambiguity exists offline. This REMOVES the usual repaint risk entirely; it is the easiest YELLOW to clear.
- `barstate.islast`/`isrealtime`: not used. No look-ahead constructs. No `request.security(..., lookahead_on)`.

**`syminfo.mintick` (lines 423-424):** `f_add_lvl` rejects levels thinner than one mintick. **Mitigation:** supply the symbol's tick size as candle-factory metadata (Massive reference/tickers endpoint provides it). A wrong mintick only changes whether a near-degenerate PB/PBJ level is created — small blast radius, but pass the real value to be exact.

**Warmup / history-length convergence (the RMA question):**
- `ta.atr` (14/10/100), `ta.ema` (20/50/150/200/8/21/5), `ta.rma` (inside atr/rsi) are **recursive/IIR** — their value at bar *n* technically depends on all prior bars, converging exponentially. TV seeds ATR/RMA with an SMA of the first `length` bars then recurses; it does NOT depend on 5000 bars of history — convergence is effectively complete within ~5×length bars.
- **Mitigation:** (a) replicate TV's exact seeding — RMA/ATR first value = `sma(src,len)` at the len-th bar, then `rma = (prev*(len-1)+src)/len`; RSI same. (b) Discard the first ~250 bars of every series as warmup before trusting EMA200/ATR100/52wk(252) signals. With 6000 bars, losing 250 to warmup is acceptable. (c) `ta.stdev(...,100)` (line 693) and `ta.sma(...,100)` (line 649) need ≥100 valid bars — same discard rule covers them.
- **Convergence answer:** for all EMA/RMA/ATR/RSI here, value does NOT meaningfully depend on history beyond ~5×length; 6000 bars is far more than enough. The ONLY genuinely history-length-sensitive constructs are `isHV`'s `highest(volume,5000)` and Nagasaki's bar-0 cumulative max (§5).

**Array-state path dependence (cluster machinery, lines 159-205, 246-291, 779-823):** `var` arrays accumulate threshold/sequence boxes and prune by a 20-bar window (178, 183) or 7-bar window (795, 810) or size cap (497-500, 817-823). Because pruning windows are short (≤20 bars), the array state is NOT sensitive to where history starts beyond ~20-30 bars of warmup. **Mitigation:** same 250-bar warmup discard fully covers it. Deterministic `var` initialization in Python must mirror Pine (empty arrays, counters at 0, `st_dir=1` at line 391, `maxVol=0` seeded on first bar).

---

## 5. Deep Solve — The Three Hard-YELLOW Dependencies

### 5.1 `tv_ta.relativeVolume(30, "", false, true)` (lines 349-352) — external library

**Dependency:** `import TradingView/ta/7 as tv_ta`; `[currentVolume_reg, pastVolume_reg, _] = tv_ta.relativeVolume(30, "", false, true)`; `relVolRatio = currentVolume_reg / pastVolume_reg` (351). Feeds WTC (352) and Hiroshima (353) — the highest-tier "weapons" used across MEGA, Heavy, Super, Opener, Scan plots.

**Knowns:** Signature is `relativeVolume(length, anchorTimeframe, isCumulative, ...)`. Here length=30, **anchorTimeframe="" (empty)**, isCumulative=**false**, 4th arg true. Per TradingView's own `ta` library, the function returns (currentVolume, averagePastVolume, ratio) where the average is taken over `length` prior anchor-periods at the equivalent intra-period offset, using the RelativeValue library. With `isCumulative=false` the values are per-bar (not accumulated).

**Unknown → resolved:** What does `anchorTimeframe=""` mean? Empty anchor = no higher-timeframe anchor, so each bar is its own "period" and the offset machinery collapses. With a per-bar period and non-cumulative volume, `currentVolume_reg = volume[0]` and `pastVolume_reg = average of the last 30 bars' volume` → **`relVolRatio ≈ volume / sma(volume, 30)`** (with TV's specific exclusion of the current bar from the average, i.e. likely `sma(volume,30)[1]`-style, mirroring the file's own `bb_avgVolDenom = ta.sma(volume, bb_avgLength)[1]` pattern at line 330).

**Governing equation:** `relVolRatio = volume_t / mean(volume_{t-1 … t-30})`.

**Concrete reproduction from Massive:** Massive 1m aggregates give exact per-bar `volume`. Compute `sma(volume,30)` (offset by 1 bar) and divide. **Validation step (mandatory, do NOT assume):** before trusting the parity, run the indicator live in TradingView Desktop on 2-3 tickers via the TV MCP (`data_get_study_values`), capture `relVolRatio` on ~50 bars, and confirm the Python `volume/sma(volume,30)[1]` matches to ≤0.1%. If TV's helper excludes the current bar differently or weights differently, adjust the offset. This is a 30-minute empirical check that converts the one external dependency into a verified GREEN-grade formula. **Blast radius if dropped:** WTC + Hiroshima would be lost → degrades HW/MEGA/Heavy/Opener/Scan tiers but does NOT remove the PBJ/PB/F2/E3/FC/PUP/GZ1/HV core. Recommendation: re-derive (cheap, high confidence), do not drop.

### 5.2 `isHV` 5000-bar lookback (line 773) vs 6000-bar / max_bars_back=2000 plan

**Dependency:** `isHV = volume[1] == ta.highest(volume, 5000)[1] or volume[1] == ta.highest(volume, 252)[1] or volume[1] == ta.highest(volume, 63)[1]`. `isHV` drives bullHV/bearHV (790-791, 805) → every GZ/HV, HV+GZI, MEGA, Heavy, Super-B2B plot.

**Knowns/Unknowns:** `highest(volume,5000)` asks "is the prior bar the highest volume in the last 5000 bars?" Three nested horizons (5000 ≈ ~13 RTH days on 1m? no — 5000 1m RTH bars ≈ 12.8 trading days; 252 ≈ daily-year proxy; 63 ≈ quarter proxy — on a 1m chart these are intraday windows, the naming is daily-borrowed). The hard fact: **`max_bars_back=2000` (line 12) is LESS than the 5000 requested.** In TV, `highest(volume,5000)` with only 2000 bars of history available silently computes over whatever bars exist (≤2000), so the live indicator is ALREADY effectively `highest(volume, min(2000, available))`. This is a latent inconsistency in the Pine itself.

**Governing logic:** `isHV_t = (vol_{t-1} == max(vol over trailing min(N, history)))` for N∈{5000,252,63}.

**Reproduction from Massive:** Massive easily supplies ≥5000 1m bars per ticker (30 days minute data on disk already; S3 gives far more). Two parity options:
1. **Match the live TV behavior** (faithful to what Anish currently sees): cap the 5000 window at the same effective bound TV uses. Since `max_bars_back=2000`, replicate `highest(volume, min(2000, n))`. This reproduces the CURRENT chart exactly.
2. **Match the literal intent** (5000): raise `max_bars_back` in any re-port to ≥5001 and feed ≥5000 bars. This is "more correct" but will NOT match the current TV chart for tickers with <5000 bars loaded.
**Recommendation:** decide which is ground truth and lock it. Given Anish rebuilds 6000 bars, option 2 (literal 5000) is feasible and cleaner — but flag to Anish that signals will differ from his historical TV screenshots wherever TV was capped at 2000. **Blast radius:** isHV gates the entire HV/GZ family; a wrong window flips bullHV/bearHV → flips ~16 plots. High blast radius — must be validated against TV MCP `data_get_study_values` on a high-volume ticker.

### 5.3 Nagasaki cumulative max from bar 0 (lines 357-364)

**Dependency:** `var float maxVol = 0.0; if bar_index==0 maxVol:=volume else if volume>maxVol sigNagasaki:=true, maxVol:=volume`. NAGA plot (1068) + alerts (1073, 1133).

**Logic:** fires on every new running-maximum volume since the FIRST loaded bar. Value is intrinsically anchored to where the data window starts — there is no fixed lookback. On TV this is "since the leftmost loaded bar"; on a 6000-bar local rebuild it is "since the first of those 6000 bars." **These are different anchors** → NAGA will fire on different bars than a TV chart loaded with a different history depth.

**Mitigation (define the anchor explicitly — convert uncertainty to a rule):** declare the canonical NAGA anchor = first candle of the loaded 6000-bar window, and document that NAGA is a *window-relative* all-time-high-volume marker, not an absolute one. For stable cross-run behavior, anchor to a fixed calendar start (e.g. first bar of the rebuild window) and persist `maxVol` so re-runs over the same window reproduce identically. **Blast radius:** NAGA is one standalone flag (and contributes to anyBullHW/anyBearHW lines 870-871). Low-to-medium; easily reproduced once the anchor is fixed.

---

## 6. ta.* Inventory (every call confirmed reproducible)

| ta.* call | Lines | Reproducible? |
|---|---|---|
| `ta.atr(14/10/100)` | 82,375,387,412,703,ld_atr 653 | Yes — RMA-seeded; §4 warmup |
| `ta.sma(...)` | 83,84,85,147,149,153,234,236,240,328,330,334,413,649,656,705-708 | Yes |
| `ta.ema(...)` | 411,524-526,650,652,655 + f_ma EMA 379 | Yes — §4 warmup |
| `ta.wma/hma/vwma` (via f_ma) | 381-383, base_ma uses VWMA 386 | Yes — VWMA/WMA/HMA standard, OHLCV+vol |
| `ta.highest/lowest` | 416,417,528,529,536,537,773 | Yes — `highest(volume,5000)` is the §5.2 case |
| `ta.change(dayofmonth)` | 110,131,218 | Yes — from candle timestamps (NY tz) |
| `ta.crossover/crossunder` | 404,405,658,659,661,664,667,670 | Yes |
| `ta.stdev(...,100)` | 693 | Yes — §4 warmup |
| `ta.cum(...)` | 775 (gzThresh = cum((H-L)/L)/bar_index) | Yes — but **running mean from bar 0 → window-anchor-sensitive like NAGA**; document anchor (treat as §5.3-class) |
| `tv_ta.relativeVolume` | 350 | Yes after §5.1 re-derivation + TV validation |

No `ta.vwap` (session-anchored) is used — good, that would have added a session-reset parity wrinkle. `hlc3` (652-654) is pure OHLC.

---

## 7. DuckDB / Compute Scale

- Per ticker: 6000 bars × 5 timeframes. The indicator is single-pass O(bars) except the cluster array loops (lines 193-204, 280-289, 793-813) which are O(bars × window) with window ≤30 → still ~linear, trivial.
- `f_has` (673-679) loops `win-1` (win=1 here, lines 681-682) → O(1). `f_hadSignalYesterday` (853-859) loops `barsPerDay*2` (~975 on 1m) per bar → O(bars × ~1000) ≈ 6M ops/ticker/tf. Across a 807-ticker watchlist × 5 tf that is ~24B inner iterations — **vectorize** (`f_hadSignalYesterday` is just "did sig fire in the last 2 sessions" → a rolling `any()` window) rather than a naive per-bar Python loop. DuckDB window functions or numpy rolling handle it in seconds.
- No cross-row joins needed; the whole indicator is per-ticker per-timeframe independent → embarrassingly parallel.

---

## 8. Bottom Line

**Reproducible locally from Massive OHLCV candles? YES — with caveats, zero blockers.**

- **0 RED.** No `request.security`/financial/dividend/split/economic/tick dependency anywhere. The lone external `import TradingView/ta/7` is a pure-volume helper (`relativeVolume`) that reduces to `volume / sma(volume,30)` and must be empirically confirmed against TV once (§5.1).
- **All 53 detection plots/alerts are YELLOW**, every one with a concrete mitigation. The dominant YELLOW themes: (1) RMA/EMA/ATR warmup seeding — clear by discarding ~250 warmup bars and matching TV's SMA-seed; (2) NY-session/`barsPerDay` anchoring — clear by RTH-filtering candles with DST-aware tz; (3) `barstate.isconfirmed` — auto-satisfied offline (all candles closed); (4) `tv_ta.relativeVolume` — re-derive + validate; (5) `isHV` 5000-bar lookback colliding with `max_bars_back=2000` — must pick literal-5000 vs match-current-TV and validate.
- **Highest parity risk:** `isHV`'s `ta.highest(volume,5000)` vs the declared `max_bars_back=2000` (line 773 vs 12). It gates ~16 HV/GZ/MEGA/Heavy plots and the Pine itself is internally inconsistent (asks 5000, allows 2000). Second: the window-anchor-relative signals — Nagasaki cum-max (357-364) and `gzThresh` cum-mean (775) — which depend on where the loaded history starts and will diverge from TV unless the anchor is fixed.
- **Mandatory validation gate before trusting the port:** run Ultra Combo v57 live in TradingView Desktop (TV MCP `data_get_study_values`) on 2-3 high-volume tickers, capture `relVolRatio`, `isHV`-driven HV flags, and Nagasaki bars over ~100 bars, and reconcile against the Python rebuild to ≤0.1% / exact-boolean. This converts every remaining YELLOW into a measured GREEN.
