# Parity Audit — VOB Asym T3 ×6 + MutEx Lines + Claude v10

**File audited:** `/tmp/IND_VOB.txt` (1590 lines, Pine v6, read in full — no sampling)
**Indicator title:** `"VOB Asym T3 ×6 + MutEx Lines + Claude v10"` (line 2)
**Auditor goal:** Determine whether every detection plot / line / signal can be reproduced EXACTLY from Massive.com minute-aggregate OHLCV(+volume) rebuilt locally on 5 timeframes (1m/5m/15m/1h/D), ~6000-bar window, with NO TradingView feed dependency.
**Verdict headline:** ZERO RED. Every output is pure OHLCV/volume + standard `ta.*` math + array state. The dominant — and severe — parity risk is **EMA warmup convergence**, NOT a T3. **There is no Tillson T3 in this file.** Details in §4.

---

## 1. Declaration / Header Facts

| Property | Value | Line |
|---|---|---|
| `@version` | 6 | 1 |
| Declaration | `indicator(..., overlay = true)` | 2 |
| `max_lines_count` | 500 | 3 |
| `max_labels_count` | 500 | 3 |
| **`max_bars_back`** | **5000** | 3 |
| Overlay | true (draws on price) | 2 |

**Critical structural fact:** Despite the name "**T3** ×6", there is **no T3 / Tillson smoother / `ta.tema` / cascaded-EMA chain anywhere in the file.** The "T3" label is Anish's *signal name* (Tier-3 super signal), not the Tillson T3 moving average. Every moving average in this script is a **single `ta.ema(close, length)`** (lines 295–306 for slopes; lines 530–531 inside `f_vob`). The brief's premise of "6 cascaded EMAs / longest warmup of any MA" does **not** apply. The real warmup problem is different and arguably worse — see §4.

### Full `ta.*` inventory (every call, line-referenced)
| `ta.*` call | Where | Purpose | Pure OHLCV? |
|---|---|---|---|
| `ta.atr(200)` wrapped in `ta.highest(..,200)` | 263 | `atr_base` → proximity/adjust thresholds | Yes (H,L,C) |
| `ta.rsi(close,14)` | 275 | emission context only (not signal logic) | Yes |
| `ta.change(time("D"))` | 282 | session-rollover detector | Yes (time) ⚠ TZ |
| `ta.percentrank(volume,200)` | 290 | `vol_rank` emission context | Yes (vol) |
| `ta.ema(close, sens_*)` ×6 | 295,297,299,301,303,305 | slope context (`slope_ema_*`) | Yes |
| `ta.ema(close, len1)` / `ta.ema(close, len2)` | 530–531 | **core crossover engine** (per tier) | Yes |
| `ta.crossover` / `ta.crossunder` | 532–533 | zone-trigger events | Yes |
| `ta.lowest(len2)` / `ta.highest(len2)` | 534–535 | swing-origin price for zone | Yes |

No `request.security`, `request.financial`, `request.dividends`, `request.splits`, `request.economic`, `request.quandl`, no `[tick]`/sub-candle, no external feed. Coarse grep's "ZERO RED" is **confirmed line-by-line.**

---

## 2. STATUS TABLE — every detection plot / line / signal

Plot budget per header (lines 71–74): 31 plotshapes + 7 alertconditions. Below: all plotshapes, the MutEx `line.new` family, labels, alertconditions, and the named booleans that drive decisions.

| # | Detection Plot / Line | Fires on / level computed from | Inputs | Status | Parity Risk | Mitigation |
|---|---|---|---|---|---|---|
| 1–6 | **T3a–T3f Buy** circles (L800–805) | `t3_buy_*` (L642): `bc==1 and sp>0 and db_vol>sp*super_mult and pat_bull`. Zone arrays from EMA crossover engine | close, EMA crossover, accumulated volume, array state | **YELLOW** | EMA warmup (§4) + array-state lookback dependence | Warm up ≥ `sens+13` bars before trusting; deterministic given same bar history |
| 7–12 | **T3a–T3f Sell** circles (L807–812) | `t3_sell_*` (L643) mirror of buy | same | **YELLOW** | same | same |
| 13 | **Nagasaki** diamond (L814) | `isNagasaki` (L718): `volume[1] > maxVolEver` (all-time-high running max) | volume only | **YELLOW** | `maxVolEver` is `var` seeded 0.0; depends on full history from bar 0. On a 6000-bar window the "all-time" max is window-relative, not true ATH | Anchor the running-max scan to the SAME first bar TV had, or document that ATH = max-within-loaded-window. Otherwise GREEN math |
| 14–19 | **ZoneBull A–F** markers `zA..zF` (L956–961) | `fire_zb_*` (L864–875): array grew this bar (`nzb_*`, L666–671) + enable + cooldown | EMA crossover, `ta.lowest`, volume accum | **YELLOW** | EMA warmup + cooldown uses `bar_index` (history-length-dependent) | §4; cooldown = bars-since, deterministic if bar 0 aligned |
| 20–25 | **ZoneBear A–F** markers `zA..zF` (L963–968) | `fire_zs_*` mirror | same | **YELLOW** | same | same |
| 26 | **VLB Bull** triangleup (L1454) | `plot_vlb_bull` (L1444): strict F→E→D→C→B→A chronological ladder complete, `barstate.isconfirmed`, cooldown. Price rule `new.upper>=prior.lower` (L1223 etc.) | zone formation order + zone hi/lo | **YELLOW** | Depends on exact zone-formation sequence → depends on EMA warmup (§4); `barstate.isconfirmed` execution model | Replicate bar-close-only evaluation; align warmup |
| 27 | **VLB Bear** triangledown (L1455) | `plot_vlb_bear` (L1445) mirror, `new.lower<=prior.upper` (L1348 etc.) | same | **YELLOW** | same | same |
| 28 | **Multi-Zone Bull 2** square (L1537) | `plot_mz_b2` (L1520): `mz_bull_cnt==2` (count of `fire_zb_*`, L1516) + confirmed + cooldown | zone-formation booleans | **YELLOW** | Downstream of zone formation (EMA warmup) | §4 |
| 29 | **Multi-Zone Bull 3+** flag (L1538) | `plot_mz_b3` (L1521): `mz_bull_cnt>=3` | same | **YELLOW** | same | §4 |
| 30 | **Multi-Zone Bear 2** square (L1539) | `plot_mz_s2` (L1522): `mz_bear_cnt==2` | same | **YELLOW** | same | §4 |
| 31 | **Multi-Zone Bear 3+** flag (L1540) | `plot_mz_s3` (L1523): `mz_bear_cnt>=3` | same | **YELLOW** | same | §4 |
| L1 | **MutEx zone lines** — top/bottom/mid + fill, priority 0 (L1001–1008) | Price levels = `l.upper` / `l.lower` / `l.mid` from `level` UDT, computed at zone formation (see §4 level math). Priority from `f_count_overlaps` (L993) | zone hi/lo/mid, overlap count | **YELLOW** | Levels derived from `ta.lowest/highest` swing + `atr_adjust` clamp; redrawn every bar (full clear+rebuild L977–984) | Reproduce level formula exactly (L544–559); `syminfo.mintick` NOT used here so no rounding gap |
| L2 | **MutEx degraded midlines** priority 1/2/3 (L1010–1017) | Same `l.mid`; style downgraded by overlap priority | overlap engine | **YELLOW** | Overlap priority is order-dependent on array iteration (A→F, L1029–1040) | Preserve processing order A,B,C,D,E,F bull then bear |
| E1 | **Zone-formation labels** (L1053, `label.new`) | On `nzb_*/nzs_*`, text only (mid price y-pos) | emission metrics | YELLOW (cosmetic) | Not a signal; metadata only | Drop if not needed downstream |
| AC1 | `alertcondition` **Any T3 / Nagasaki** (L821) | `any_t3` OR of all `plot_t3_*` + nagasaki | — | YELLOW | mirrors signals above | — |
| AC2 | `alertcondition` **Any Zone Formation** (L1074) | `any_zone` OR of all `fire_z*` | — | YELLOW | mirrors zone markers | — |
| AC3 | `alertcondition` **VLB Strict Ladder** (L1458) | `plot_vlb_bull or plot_vlb_bear` | — | YELLOW | mirrors VLB | — |
| AC4–7 | `alertcondition` **MZ Bull2/Bull3/Bear2/Bear3** (L1543–1546) | `plot_mz_*` | — | YELLOW | mirrors MZ | — |
| — | `alert()` Bloomberg strings (L830–858, 1077–1102, 1479–1490, 1568–1590) | String payloads only; carry `syminfo.ticker/prefix`, `timeframe.period` | metadata | YELLOW (metadata) | `syminfo.prefix` (exchange) + `syminfo.ticker` must be supplied externally | Inject ticker/exchange/TF as constants from Massive ingestion context |

**No `plot()` numeric series and no `table.*` survive in v10** — header L73 and L246 confirm all three visual tables were removed; `data_get_study_values` plots referenced in comments (L64) are not present as live `plot()` calls in the body. `log.info` (L1110) is emission-only, no decision role.

---

## 3. Tally

- **Total decision outputs classified:** 31 plotshapes + 7 alertconditions + MutEx line family (2 visual classes) + labels = **~40 outputs.**
- **GREEN (zero-risk):** 0 outright — every signal inherits EMA-warmup sensitivity.
- **YELLOW (reproducible with care):** **ALL** outputs. Drivers: (a) EMA warmup convergence on enormous lengths (§4) — dominant; (b) `var`/array persistent zone state with history-length dependence; (c) `barstate.isconfirmed` bar-close execution model; (d) `time("D")` session/timezone via `syminfo.timezone`; (e) `maxVolEver` all-time running max anchored to bar 0; (f) `bar_index`-based cooldown.
- **RED (needs non-OHLCV TV data):** **0.** Confirmed line-by-line.
- **Non-droppable core:** MutEx zone lines, T3 signals, VLB ladder, Multi-Zone — these ARE the thesis output. None can be dropped.

---

## 4. Warmup-Convergence + Persistent-State Deep-Dive (THE flagship risk)

### 4a. There is no Tillson T3 — the real engine is single-EMA crossover
The brief expected "6 cascaded EMAs". **Reality (verbatim, L529–535):**
```
int   len2    = len1 + 13
float ema1    = ta.ema(close, len1)
float ema2    = ta.ema(close, len2)
bool  cup     = ta.crossover(ema1, ema2)  and barstate.isconfirmed
bool  cdn     = ta.crossunder(ema1, ema2) and barstate.isconfirmed
float lowest  = ta.lowest(len2)
float highest = ta.highest(len2)
```
Each tier compares a fast `ema(close, sens)` against a slow `ema(close, sens+13)`. Tiers: A=2500/2513, B=2250/2263, C=2000/2013, D=1500/1513, E=1250/1263, F=1000/1013 (L114–119, +13 at L529).

### 4b. The convergence problem is SEVERE — and it is about EMA *seeding*, not cascade depth
Pine `ta.ema` uses (confirmed via TradingView/TradingCode docs):
```
alpha = 2 / (length + 1)
ema := na(ema[1]) ? src : alpha*src + (1-alpha)*nz(ema[1])
```
**Pine seeds the EMA with the first available `close` (sma_seed = false by default), NOT an SMA.** The recursive weight retained from the seed after *k* bars is `(1-alpha)^k`. For length L, `1-alpha = (L-1)/(L+1)`.

Convergence to within tolerance τ requires `(1-alpha)^k <= τ`, i.e. `k >= ln(τ)/ln(1-alpha)`.

For the **slowest tier (A, L=2513):** `1-alpha = 2512/2514 = 0.999204`. To reach τ=1% residual seed weight: `k = ln(0.01)/ln(0.999204) ≈ 4.605/0.000796 ≈ 5786 bars`. To reach τ=0.1%: `k ≈ 8679 bars`. To reach τ=0.01% (~tick-tight parity): `k ≈ 11,570 bars`.

**This is the killer finding:** with `max_bars_back = 5000` and a planned **~6000-bar window**, tier A's EMA has only shed ~`(1-0.000796)^6000 ≈ e^(-4.78) ≈ 0.0084` → **still ~0.8% seed contamination at the most recent bar.** Tiers A/B/C (L≥2000) will **NOT** be byte-identical to TV unless the local rebuild starts from the *same first bar* TV used. The crossover of two near-equal slow EMAs (separation only 13 in length) is acutely sensitive to this residual — a 0.1% level difference can flip a `crossover` bar, which cascades into different zone arrays, different VLB ladders, everything.

**Mitigation (exact):**
1. **Seed identically and start identically.** Reproduce Pine's recurrence exactly: `ema[0]=close[0]`, then `alpha*close + (1-alpha)*ema_prev`. Do **not** use pandas `ewm(adjust=True)` (that's an expanding-window formula and will diverge); use `ewm(adjust=False)` or hand-roll the recurrence.
2. **Match the warmup origin.** TV computes from the first bar it loaded (governed by `max_bars_back=5000` for *referenced* history, but EMA itself runs from chart bar 0). To get parity, the local candle factory must feed the **same leading history** TV had. Practically: load **≥ 12,000 bars** before the analysis window for tiers A/B (so τ<0.01% at the first analysis bar), then evaluate only the trailing ~6000. Burn-in of ~2× the longest length (≈5000 bars) gets τ≈e^-4≈1.8%; ~4× (≈10000 bars) gets τ≈0.03%. **Recommendation: ≥10,000-bar burn-in for daily/1h; verify per-tier.**
3. **Quantified parity-to-bar verdict (per tier, τ=0.1% seed residual):** F(1013)→~3500 bars, E(1263)→~4360, D(1513)→~5230, C(2013)→~6950, B(2263)→~7820, A(2513)→~8680. **On a flat 6000-bar window with no extra burn-in, only tiers D/E/F converge; A/B/C do not.** This must be designed around.
4. **`ta.lowest/highest(len2)`** (L534–535) over up to 2513 bars is a hard window — fully deterministic and GREEN given identical bars, but it ALSO needs the full `len2` of leading bars present or it silently shortens the window. Same ≥len2 burn-in requirement.
5. **`ta.atr(200)` then `ta.highest(,200)`** (L263): RMA-based ATR (Wilder) also seeds; needs ~1000-bar burn-in for <0.1% — trivially covered by the EMA burn-in above.

### 4c. Persistent var/array state and its lookback dependence
- **Zone arrays** `upper_*` / `lower_*` are `var array<level>` (L314–325), capped at 15 (`shift()` at L571–572, 585–586). State is fully **path-dependent**: which zones exist now depends on the entire crossover/invalidation history since bar 0. Two different start bars → different surviving zones → different `t3_*`, `fire_z*`, VLB, MZ. **Mitigation:** identical bar history + identical evaluation order; this is deterministic, just history-sensitive. Replicate the dedup rule (L567: `abs(mid-mid1)<atr_proximity` nulls the *previous* zone) and the invalidation rule (L569 bull: `close<l.lower`; L583 bear: `close>upper`) exactly.
- **`maxVolEver`** (L716, `var float … = 0.0`) — Nagasaki is window-anchored ATH (see table #13).
- **Cooldown stamps** `last_*` / `cd_*` (L331–357) store `bar_index`; `f_cd_ok` (L398–399) = `na or (bar_index-last)>cd`. `bar_index` is offset-dependent but the *difference* is invariant, so cooldown is parity-safe if the same first bar is used.
- **VLB state machine** `vlb_*_state` + per-step OHLCV snapshots (L1161–1183) — pure derived state from zone-formation booleans; deterministic.

### 4d. Level-price math (what the MutEx lines actually plot) — verbatim
Bull zone (L544–547):
```
float src = math.min(open[i], close[i])
src := (src - lowest) < atr_adj * 0.5 ? lowest + atr_adj * 0.5 : src
float mid = math.avg(src, lowest)
lo_lvl.push(level.new(index, src, lowest, mid, vol, open[i], high[i], low[i], close[i]))
```
Bear zone (L556–559): mirror using `math.max(open,close)` and `highest`, clamped by `atr_adj*0.5`. `atr_adj = ta.highest(ta.atr(200),200)*2` (L263–265). **All pure OHLCV.** No `syminfo.mintick` rounding is applied to line levels (mintick never appears in the file), so there is **no tick-rounding parity gap** to worry about — levels are raw floats. Reproduce `math.avg`, `math.min/max`, and the ATR clamp bit-for-bit.

---

## 5. RED / Hard-YELLOW Solve

**No RED.** The only hard-YELLOW is **4b EMA warmup on tiers A/B/C**, and it is solvable entirely from Massive data — it needs *more bars*, not different *kinds* of data:

- **Dependency:** parity of `ema(close, 2000..2513)` at the analysis bar.
- **Knowns:** Pine recurrence + seed rule (docs-confirmed); seed residual `(1-alpha)^k`; Massive `/v2/aggs` minute bars + daily flat files provide arbitrarily long lookback (17 months daily, 30 days minute on disk; REST/S3 for more).
- **Unknown:** the exact first bar TV loaded for a given chart/symbol (depends on plan + symbol listing date). **Resolve by test:** pull `data_get_study_values`/`data_get_pine_lines` from the live TV chart via the TradingView MCP for 5 reference symbols, compare local-rebuild zone levels, and tune burn-in length until line prices match to ≤0.1%.
- **Governing equation:** `k_required = ln(τ)/ln((L-1)/(L+1))`.
- **Avenue from Massive:** for daily TF, load full listed history (S3 daily flat files cover all US stocks); for 1m/5m/15m/1h, fetch ≥10,000 leading bars from `/v2/aggs` before the analysis window. Tiers A/B at 1m need ~8700 bars ≈ 22 RTH days of 1m — well within Massive limits.
- **Blast radius if ignored:** tiers A/B/C crossovers mistime by 1–several bars → wrong zones → wrong VLB/MZ/T3 on the *highest-conviction* (strongest, fewest-zone) tiers. **Non-droppable; must fund the burn-in.**

### DuckDB / compute scale
6 tiers × per-bar inner loops up to `len2` (L539–543 volume accumulation scans up to 2513 bars on every crossover) is O(bars × len) in the worst case. In Python/DuckDB, vectorize: precompute EMAs with `ewm(adjust=False)`, detect crossovers vectorized, and compute the swing-origin via rolling `idxmin/idxmax` over `len2`; the volume-accumulation `for k=0 to i` (L542–543) is a prefix-sum (`cumsum`) lookup, not a loop. ~6000 bars × 6 tiers × ~6000 symbols is trivial for DuckDB if EMAs are vectorized; the only trap is the per-crossover swing scan — replace with cumulative arrays. Keep the 15-zone cap + dedup as a small stateful pass (cannot be fully vectorized due to path-dependent invalidation).

---

## 6. Bottom Line

- **0 RED.** 100% reproducible from Massive OHLCV+volume; no `request.*`, no tick/sub-candle, no external feed — confirmed line-by-line across all 1590 lines.
- **The name lies:** there is **no Tillson T3**. Every MA is a single `ta.ema`. "T3" = Tier-3 signal name. The cascade-warmup premise does not apply.
- **The true flagship risk is EMA seed convergence on huge lengths (1000–2513).** With `max_bars_back=5000` and a 6000-bar window, **tiers A/B/C will NOT match TV** unless the local rebuild feeds the same long leading history. Required burn-in: **≥10,000 bars** (per `k=ln(τ)/ln((L-1)/(L+1))`) for ≤0.1% parity on tier A. Fund the burn-in or accept that the strongest tiers diverge.
- **Everything is path-dependent var/array state** — identical first bar + identical evaluation order (A→F, bull→bear) + exact recurrence (`ewm(adjust=False)`) + bar-close-only (`barstate.isconfirmed`) gives bit-parity. Skip any of these and zones drift.
- **Line levels are raw floats** (no `mintick` rounding) — reproduce `math.avg/min/max` + `atr_adjust*0.5` clamp exactly; that's the entire MutEx level formula (L544–559).
- **Validate empirically:** diff local zone lines vs `data_get_pine_lines` from live TV (TradingView MCP) on ≥5 symbols, tune burn-in until ≤0.1%.

Sources: [TradingCode — EMA in Pine](https://www.tradingcode.net/tradingview/exponential-moving-average/), [TradingView Pine v6 Reference](https://www.tradingview.com/pine-script-reference/v6/)
