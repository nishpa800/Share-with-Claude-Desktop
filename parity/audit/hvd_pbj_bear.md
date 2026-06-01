# Parity Audit — `BASE HV+D ↔ PBJ v1 — BEARISH (36)` (shorttitle `HVD PBJ BEAR`)

- **Source file:** `/Users/anishpatel/Desktop/Indicator studies/"BASE HV+D ↔ PBJ v1 — BEARISH (36)", shorttitle="HVD PBJ BEAR".txt`
- **Lines:** 1,302 · **Bytes:** 75,721 · **MD5:** `e608ce87620a1584df5663140ff595cb`
- **Pine version:** v5, `overlay=true`
- **Audit date:** 2026-05-31

> NOTE on the filename: the file on disk literally begins with a `"` double-quote character (`"BASE HV+D ↔ PBJ v1 — BEARISH (36)", shorttitle="HVD PBJ BEAR".txt`). The path given in the task brief omitted that leading quote, which is why `open()` initially failed. The directory itself is TCC-sandbox-blocked for `ls`/`listdir`; the file was located with Spotlight (`mdfind`) and opened by exact path.

---

## VERDICT (one paragraph)

**NO EXTERNAL DEPENDENCY — fully reproducible from Massive.com OHLCV aggregates alone.** Every one of the 36 bear detection plotshapes (plus the 3 HV+D-standalone plotshapes that share the budget, totalling the 36 permanent series the header advertises) resolves to deterministic functions of `open/high/low/close/volume`, `ta.*` rolling primitives, `math.*` scalar ops, `bar_index`, and session boundaries derived from `time`/`time("D")`. There is **zero** `request.*`, `request.security`, `syminfo.*` price/fundamental fetch, external symbol, tick feed, bid/ask, or `ta.vwap` anchored intrabar dependency. The **"+D" (Displacement / "Distribution") term is NOT order-flow delta** — it is pure candle-geometry displacement: `|open−close|` (or `high−low`) measured in standard deviations, combined with a 2-bar Fair-Value-Gap geometry and directional `close<open`. The single non-built-in import (`TradingView/ta/7 → relativeVolume`) is a published open-source library whose math (cumulative session volume ÷ trailing average) is trivially reproducible from OHLCV + session anchoring; it is NOT proprietary or hidden. Two parity caveats only: (1) `volume == ta.highest(volume, N)` exact-equality HV-rank tests require **bit-exact volume** — the 2026-02-23 Massive decimal-size change means the local builder must match TradingView's volume rounding/aggregation or the equality flips; (2) the large lookbacks (1000-bar HV, `max_bars_back=1100`, all-time `maxVolEver`/`maxVol`/`isHEV`/`isNagasaki` running maxima) need long warmup and a stable from-genesis history to be identical. Everything is REPRODUCIBLE or REPRODUCIBLE_WITH_WARMUP. Nothing is BLOCKED. A handful of booleans are `barstate.isconfirmed`-gated (non-repaint on close) and a few `var` running-state accumulators are seeded at `bar_index==0` (recursive-seed risk noted below).

---

## SUMMARY COUNT TABLE

| Category | Count |
|---|---|
| Detection plotshapes (permanent series) | **36** (see note) |
| — HV+D standalone block | 3 (HV+D, PB, PBJ) |
| — USE bear plotshapes | 20 |
| — Pipeline D triple co-occurrence | 2 |
| — Back-to-Back HV+D | 3 |
| — HV+D Momentum co-occurrence | 8 |
| `alert()` calls (1:1 + aggregator + nagasaki) | 17 lines |
| `label.new` detections | **0** (header guarantee; all moved to plotshapes) |
| `box.new` detections | 0 (only `line.new` for internal SR bookkeeping, non-detection) |
| `bgcolor()` detections | 0 |
| Dependency = PURE_OHLCV | all engines |
| Dependency = NEEDS_USER_INPUT_ONLY (toggles/thresholds) | gating only |
| Dependency = BARSTATE_LIVE_ONLY | 0 (all use `isconfirmed` = close, not live) |
| Dependency = EXTERNAL_DEPENDENCY | **0** |
| Parity = REPRODUCIBLE | majority |
| Parity = REPRODUCIBLE_WITH_WARMUP | HV-rank / all-time-max / long-lookback engines |
| Parity = LIVE_ONLY / BLOCKED | 0 |

> Note on "36": the header comment (lines 4–15) states the bear side ships **36 plotshapes, 0 labels**. The plot region contains 3 (HV+D block) + 20 (USE) + 2 (Pipeline D) + 3 (B2B) + 8 (Momentum co-occ) = **36** `plotshape()` calls. Confirmed by full-file grep of `plotshape(`.

---

## DELTA / DISTRIBUTION DERIVATION (highest parity-risk subsection)

**Finding: there is no order-flow delta anywhere in this script.** The "+D" in "HV+D" stands for **Displacement** (the script's own group label is `── HV+D: DISP BASE ──`, line 56), realized purely from candle geometry. Three independent places confirm this:

1. **HV+D displacement engine (Pipeline A, lines 60–67):**
   - `d1_rng = (d1_type=="Open to Close") ? |open − close| : (high − low)` — body-size or full-range, user-selectable; default **Open-to-Close body**.
   - `d1_std = ta.stdev(d1_rng, 100)` ; `d1_thresh = d1_std * 5.0`.
   - `d1_prevDisp = d1_rng[1] > d1_thresh[1]` (previous bar's body exceeded 5σ of the trailing-100 body distribution).
   - Direction comes from a **2-bar Fair Value Gap** + prior-candle color: `d1_bearFVG = high < low[2] and close[1] < open[1]`.
   - So "Distribution/displacement bear" = *prior bar was a ≥5σ wide-range candle AND a bearish FVG formed AND the prior candle closed down*. **100% OHLCV.**

2. **USE Displacement engines 2+/3+ (lines 327–369):** identical pattern with min/max σ-multiplier bands (`disp_std * i_std_min … i_std_max`) and streak counters requiring N consecutive displacement bars co-occurring with FAUNA fires. Pure OHLCV.

3. **FAUNA "delta"-named variable (line 294):** `fauna_avgDelta = ta.sma(|close − close[1]|, 10)`. This is **close-to-close price change magnitude**, a momentum proxy — NOT buy/sell volume delta. Used in `TA_r = ... (close[1]−close) > 1.6*fauna_avgDelta ...`. Pure OHLCV.

**Direction / "buy vs sell pressure" proxy** everywhere in the script is the textbook OHLCV proxy: `close < open` (bearish body), `close > open` (bullish body), body ratio `|close−open|/(high−low)`, and wick position (`close−low`, `high−close`). No tick rule, no bid/ask, no uptick/downtick volume split, no `volume`-signed series. **Therefore no Massive trades/quotes tick feed is required.** (If Anish ever wants *true* signed delta for a future variant, Massive DOES expose trades + quotes — `recon/massive-api-endpoints.md` — but this indicator does not need it.)

---

## ta.* FUNCTION INVENTORY + WARMUP / RECURSIVE-SEED RISK

Distinct `ta.*` used: `ta.atr`, `ta.stdev`, `ta.highest`, `ta.lowest`, `ta.sma`, `ta.ema`, `ta.wma`, `ta.hma`, `ta.vwma`, `ta.cum`, `ta.change`, `ta.rsi`, `ta.crossover`, `ta.crossunder`, `ta.pivothigh`, `ta.pivotlow`, `ta.rma` (inside `ta.atr`), `math.sum` (via `math.sum`). Library: `tv_ta.relativeVolume` (TradingView/ta/7).
Distinct `math.*`: `math.abs`, `math.max`, `math.min`, `math.avg`, `math.sum`.

| Primitive | Where | Warmup | Recursive-seed risk |
|---|---|---|---|
| `ta.highest(volume, N)` N∈{50…1000,252,5000,63} | HV-rank, GZ HV, Neo, Super | up to **5000 bars** | None (windowed), but exact-equality compare to `volume`/`volume[1]` is fragile (see caveat) |
| `ta.atr(14)`, `ta.atr(pp_atr_len=100)`, `ta.atr(10)` | shared, swing, supertrend | 14–100 | `ta.atr` uses `ta.rma` → **recursive EMA-type seed**; first value seeded from SMA. Long, deterministic. |
| `ta.stdev(rng, 100)` | displacement engines | 100 | None (windowed) |
| `ta.ema`, `ta.hma`, `ta.wma`, `ta.vwma` (f_ma switch) | PBJ MA, pbj_ma, BoomHunter | len | `ta.ema`/`ta.hma` **recursive seed** from first value; deterministic but needs warmup from genesis |
| `ta.cum((high-low)/low)/bar_index` | GZ auto threshold (line 382) | **from genesis** | `ta.cum` is a running sum since bar 0 → must replay full history for parity |
| `ta.change(time("D"))` | new-day detection | 1 | None |
| `ta.pivothigh/low(_, 5, 1)` | swing SR | left+right=6, **confirms `right` bars late** | None, but pivots resolve with a lag = rightBars |
| `ta.rsi` (BoomHunter `bh_tradition`) | Boom helper (defined but `boom_bear=fox_bear`, RSI path unused in fire) | n3=3 | recursive (Wilder RMA) — but dead code for outputs |
| `tv_ta.relativeVolume(30, "", true, true)` | RVOL (WTC/Hiroshima/Pentagon) | session cumulative | cumulative-since-session-start; reproducible from OHLCV+session |
| `var maxVolEver / maxVol / st_dir / curr_long / curr_short / sig_line / *_streak / *_cnt` | running state | **from genesis** | **Recursive `var` accumulators** — `isHEV`/`isNagasaki`/supertrend line/streak counters all depend on full bar-0-forward replay. Highest warmup sensitivity. |

**Seeding note:** `curr_long`/`curr_short`/`sig_line` (PBJ supertrend, lines 454–466) are self-referential (`curr_long := f(nz(curr_long[1], seed))`). `st_dir` flips persist. These are classic recursive Pine series — Python parity must replay from the same first bar with the same `nz()` seed defaults or values diverge.

---

## FULL PER-PLOT TABLE

Engine boolean lines cited; `fire_*` = `show_* and <engine bool> and masterGate`. All gated by `conf = barstate.isconfirmed` somewhere upstream (close-confirmed, non-repaint). `offset=-1` on most = plotted on prior bar (cosmetic; parity uses the fire bar).

### A. HV+D standalone block (3) — plotshapes lines 1106–1108

| # | Plot Name | Equation (deref to OHLCV) | Inputs | Dependency | Parity | Notes |
|---|---|---|---|---|---|---|
| 1 | HV+D Bear | `hvd_fire_bear = base_hv_hit AND d1_bear`. `base_hv_hit = (useHEV AND isHEV) OR (base_enabled AND not isHEV)`. `isHEV = volume[1] > maxVolEver(running)`. `base_enabled = any(ub_N AND baseRank==N)`, `baseRank` = largest N where `volume[1]==ta.highest(volume,N)[1]`. `d1_bear = conf AND d1_rng[1]>5·stdev(d1_rng,100)[1] AND high<low[2] AND close[1]<open[1]` | volume, O/H/L/C; toggles ub50..ub1000, useHEV, d1_len=100, d1_mult=5 | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | 1000-bar highest + all-time `maxVolEver`; exact-eq volume caveat |
| 2 | PB Bear | `hvd_pb_bear = hvd_fire_bear AND (pb_bear OR pbj_bear)` (plot uses `en_hvd_pb_bear and hvd_pb_bear`) | + PBJ engine | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | depends on PBJ supertrend recursion |
| 3 | PBJ Bear | `hvd_pbj_bear = hvd_fire_bear AND pbj_bear`; `pbj_bear = sigBearPBJ = conf AND sell_cross AND wait_pbj_sell` | + PBJ engine | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | recursive supertrend/level arrays |

### B. USE bear plotshapes (20) — lines 1111–1130

| # | Plot Name | Equation (deref) | Inputs | Dependency | Parity | Notes |
|---|---|---|---|---|---|---|
| 4 | Bear UUUU (DDDD) | `uuuu_bear = use_bear_streak >= 4`; `use_bear` = OR of FAUNA/DISP/Neo/OD/Lantern/PPD/Foxtrot/Golf bear | many toggles | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | streak `var` from genesis |
| 5 | Bear UUU (DDD) | `use_bear_streak >= 3` | — | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | same streak |
| 6 | Bear UU (DD) | `use_bear_streak >= 2` (toggle default off) | — | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | same streak |
| 7 | Alpha Strike Bear (A★) | `as_bear = sigKratos AND sigPPD`. `sigKratos = conf AND bb_baseBearish AND bb_normPrice∈[saab,1x)`; `bb_baseBearish=(close<open) AND (posDiff>smaDiff)`; `bb_normPrice=|close-open|/sma(|close-open|,30)[1]` | bb_avgLength=30 | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | normalization uses [1] shifted SMA |
| 8 | Foxtrot Bear (FOX) | `fox_bear = sigMOAB OR sigBearRVOL1x`; `sigMOAB=conf AND bb_baseBearish AND bb_normPrice>=th_gs_moab(tfSec)` | tfSec thresholds | PURE_OHLCV | REPRODUCIBLE | tf-dependent constant ladder |
| 9 | OD Bear | `od_full_bear = od_bear = (sessionBarCount<=2) AND close<open AND volume>sma(volume,20)` | od_max_bars=2 | PURE_OHLCV | REPRODUCIBLE | needs session-bar counter from `time("D")` |
| 10 | Disp Bear 2+ (D2) | `sigDispConsBear2 = sigDISP2Bear AND disp2_bearStreak>=2 AND sigFAUNABear[1] AND sigFAUNABear[2]` | disp2 σ-band 5..100 | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | streak + lookback |
| 11 | Disp Bear 3+ (D3) | `sigDispConsBear3 = sigDISP3Bear AND disp3_bearStreak>=3 AND sigFAUNABear[1..3]` | disp3 σ-band 4..100 | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | streak |
| 12 | Golf Bear (G) | `golf_bear = fox_bear AND sigPPD AND neo_bear`; `neo_bear=volume>=highest(volume,67) AND close<open` | neo_len=67 | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | 67-bar highest exact-eq |
| 13 | PAF Bear (PAF-) | `paf_bear = sigPPD AND ls_lantern_bear`; lantern = reg/cum-volume multiples vs SMA + body ratio | mom floors | PURE_OHLCV | REPRODUCIBLE | math.sum(volume,3) cumvol |
| 14 | CS1 FVG Bear | `cs_cs1_bear = bearFVG AND bodyRatio>=0.74 AND close<open AND (not pentagonReq OR sigPentagon)` | cs_bodyPct_FVG | PURE_OHLCV | REPRODUCIBLE | (default toggle off) |
| 15 | CS2 MAT Bear | `cs_cs2_bear = neo_bear AND bodyRatio>=0.74 AND (pentagon opt)` | cs_bodyPct_MAT | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | neo 67-bar |
| 16 | Unified Combo Bear (COMBO) | `cs_cs3_bear = cs_cs1_bear OR cs_cs2_bear` | — | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | — |
| 17 | CC Bear | `cc_bear = cc_bear_cnt>=2 AND cc_hit_bear`; `cc_hit_bear=FAUNA/DISP/Neo/PPD bear`; counter resets on miss | cc_min_hits=2 | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | `var` counter from genesis |
| 18 | LSC Bear | `lsc_bear = lsc_bear_cnt>=2 AND ls_lantern_bear` | lsc_min_hits=2 | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | `var` counter (default off) |
| 19 | Rooftop | `bear_rooftop = high>=highest(high,20)[1] AND close<open AND volume>sma(volume,20)` | rt_lookback=20 | PURE_OHLCV | REPRODUCIBLE | (default off) |
| 20 | Penthouse | `bear_penthouse = bull_penthouse` (mirror placeholder, line 774) = `low<=lowest(low,20)[1] AND close>open AND volume>sma(vol,20)` | — | PURE_OHLCV | REPRODUCIBLE | **NOTE: code bug carried from combined — bear_penthouse aliases bull. Reproduce as-written for parity.** (default off) |
| 21 | HW Bear | `hw_bear = (high-low)>2·atr14 AND close<open AND volume>1.5·sma(vol,20)` | — | PURE_OHLCV | REPRODUCIBLE | atr14 recursive seed |
| 22 | SUPER Bear (S!) | `super_bear = volume>=highest(volume,100) AND close<open AND bodyRatio>=0.75` | — | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | 100-bar highest exact-eq (default off) |
| 23 | SDuper Bear (SD!) | `sduper_bear = super_bear AND sigPentagon` | — | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | + relativeVolume Pentagon band |

### C. Pipeline D — triple co-occurrence (2) — lines 1145–1146

| # | Plot Name | Equation (deref) | Inputs | Dependency | Parity | Notes |
|---|---|---|---|---|---|---|
| 24 | CO: HV+D+PBJ+USE Bear (CO\nPBJ) | `co_bear_pbj = hvd_fire_bear AND pbj_bear AND use_bear` | — | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | union of A×B×C engines |
| 25 | CO: HV+D+PB+USE Bear (CO\nPB) | `co_bear_pb = hvd_fire_bear AND pb_bear AND not pbj_bear AND use_bear` | — | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | — |

### D. Back-to-Back HV+D (3) — lines 1161–1163

| # | Plot Name | Equation (deref) | Inputs | Dependency | Parity | Notes |
|---|---|---|---|---|---|---|
| 26 | B2B HV+D Bear | `b2b_bear_nopb = hvd_fire_bear AND b2b_bear_cnt>=2` (consecutive HV+D-bear within window=5) | — | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | `var` consecutive counter |
| 27 | B2B HV+D+PBJ Bear | `b2b_bear_pbj = b2b_bear_nopb AND pbj_bear` | — | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | — |
| 28 | B2B HV+D+PB Bear | `b2b_bear_pb = b2b_bear_nopb AND pb_bear AND not pbj_bear` | — | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | — |

### E. HV+D Momentum co-occurrence (8) — lines 1197–1204

| # | Plot Name | Equation (deref) | Inputs | Dependency | Parity | Notes |
|---|---|---|---|---|---|---|
| 29 | HV+D+PPD Bear | `hvdm_ppd_nopbj_r = (hvd_fire_bear AND sigPPD) AND not pbj_bear`; `sigPPD=conf AND priceDn3% AND volume>highest(greenVol[1],10)` | pp_barSize=3, pp_lookback=10 | PURE_OHLCV | REPRODUCIBLE | greenVol/redVol = volume split by close vs open (geometry, not tick delta) |
| 30 | HV+D+RVOL Bear | `hvdm_rvol_nopbj_r = (hvd_fire_bear AND (sigWTC OR sigHiroshima OR sigPentagon)) AND not pbj_bear` | reg_length=30 | PURE_OHLCV (lib) | REPRODUCIBLE_WITH_WARMUP | uses `tv_ta.relativeVolume` (session cumulative; reproducible) |
| 31 | HV+D+CMB Bear | `hvdm_cmb_nopbj_r = (hvd_fire_bear AND (sigFAUNABear OR sigDISPBear)) AND not pbj_bear` | — | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | — |
| 32 | HV+D+PBJ+PPD Bear | `hvdm_vis_pbjppd_r = (hvd_fire_bear AND sigPPD) AND pbj_bear` | — | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | — |
| 33 | HV+D+PBJ+RVOL Bear | `hvdm_vis_pbjrvol_r = (hvd_fire_bear AND rvol) AND pbj_bear` | — | PURE_OHLCV (lib) | REPRODUCIBLE_WITH_WARMUP | — |
| 34 | HV+D+PBJ+CMB Bear | `hvdm_vis_pbjcmb_r = (hvd_fire_bear AND cmb) AND pbj_bear` | — | PURE_OHLCV | REPRODUCIBLE_WITH_WARMUP | — |
| 35 | HV+D+PBJ 2of3 Bear | `hvdm_2of3_r = hvd_fire_bear AND (Σ[PPD, RVOL, CMB] >= 2)` | — | PURE_OHLCV (lib) | REPRODUCIBLE_WITH_WARMUP | — |
| 36 | HV+D+PBJ 3of3 Bear | `hvdm_3of3_r = hvd_fire_bear AND (Σ[PPD, RVOL, CMB] >= 3)` | — | PURE_OHLCV (lib) | REPRODUCIBLE_WITH_WARMUP | — |

### Non-detection / alerts (informational)

- 17 `alert(...)` lines (1210–1302), all `alert.freq_once_per_bar_close` (close-confirmed). The aggregator `f_agg_bear()` and Nagasaki alert build dynamic strings; the dynamic 2of3/3of3 component list lives only in the alert payload, not in a plot. `Nagasaki = isNagasaki = volume > maxVol(running)` (all-time-high volume bar) — PURE_OHLCV, from-genesis running max.
- `line.new(...)` calls (lines 608–618) are **internal SR-level bookkeeping** for Engine 7 Ping-Pong (drawn transparent, `color.new(...,100)`), not detection outputs. They use `syminfo.mintick` only as a price-tolerance epsilon (`price_tolerance = max(mintick*10, mintick/10)`) — a per-symbol tick size that Massive exposes via reference data (or can be inferred from price precision). Not a price/data fetch.

---

## CROSS-CUTTING NOTES

1. **`barstate.isconfirmed` (`conf`) everywhere** → all engines evaluate on bar close. **No `barstate.isrealtime`/`islast`-gated detection** = nothing is LIVE_ONLY. Python parity should compute on closed bars only.
2. **`syminfo.mintick`** appears twice (lines 480, 574) as a tolerance epsilon for SR-level dedup and minimum level width. It is per-symbol tick size, available from Massive reference/tickers (or `round` precision). Not market data; not a parity blocker, but the Python builder must supply the correct tick size per symbol or SR-dedup boundaries shift slightly (affects only PB/PBJ level construction edge cases).
3. **`tfSec = timeframe.in_seconds(timeframe.period)`** drives the RVOL threshold ladders (`f_rvol_1x_threshold` etc.). In Python parity this is a known constant from the bar interval being processed (60 for 1m, 300 for 5m, …). Deterministic, no dependency.
4. **`time("D")` / `session.isfirstbar`** are session-boundary derivations. Reproducible from bar timestamps + exchange session calendar (RTH boundaries). The Python builder must know the symbol's session (NYSE 8:30–15:00 CT per project) to match `is_new_day`, `sessionBarCount`, `od_inWindow`, and `_FIRST`.
5. **Volume exact-equality HV-rank tests** (`volume == ta.highest(volume, N)`, dozens of them) are the single largest parity hazard. After the 2026-02-23 Massive decimal-size change, volume is a decimal; TradingView rounds/aggregates differently. Mitigation: (a) match TradingView's bar-volume rounding exactly, or (b) replace exact-eq with `volume >= ta.highest(volume,N) - ε`. Recommend documenting and standardizing in the Python translation layer.
6. **From-genesis running state** (`maxVolEver`, `maxVol`, supertrend `curr_long/curr_short/sig_line/st_dir`, all `*_streak`/`*_cnt`, `ta.cum`) requires replaying the full available history from the first bar TradingView would have. With Massive's 17-month daily / 30-day minute windows, intraday `maxVolEver`/HEV/Nagasaki will only match TradingView if both start from the same first bar. Flag as REPRODUCIBLE_WITH_WARMUP and note the genesis-alignment requirement.
7. **Carried-over code quirks to reproduce verbatim** for 1:1 parity: `bear_penthouse = bull_penthouse` (line 774, mirror placeholder); `uuuu_bull = f_uu_bull_scan(4) and show_BearUUUU == show_BearUUUU` (line 861, the `x==x` is always-true dead gating); BoomHunter `bh_tradition`/RSI defined but outputs reduced to `boom_bear = fox_bear` (RSI path is dead code). Do not "fix" these — match them.
8. **Library import `TradingView/ta/7` (`tv_ta.relativeVolume`)** is the only non-builtin. It is open-source, published, and computes session-cumulative volume ÷ trailing-average cumulative volume. Fully reproducible from OHLCV + session anchoring; not proprietary, not a data fetch. Implement once in the Python layer.

**DEPENDENCY RESOLUTION:** Not required — there is no genuine external dependency. (For completeness, `recon/massive-api-endpoints.md` confirms Massive provides trades + quotes if a *future* true-signed-delta variant is ever desired, but this BEARISH indicator derives all direction from OHLCV candle geometry and needs only the standard aggregate bars Anish already has.)
