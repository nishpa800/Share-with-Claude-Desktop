# CONSOLIDATED PARITY VERDICT — Batch 2 (2026-05-31)

Indicators: **TNT Opening Drive OD v3**, **Ultra Combo v57**, **VOB Asym T3 ×6 + MutEx v10**, **Heavy Weapons Single v3**.
Goal: prove each detection plot is reproducible on a Massive-OHLCV candle factory (5 TFs, ~6000 bars) so TradingView becomes a **visual layer only**.

---

## TL;DR — Can we decouple? **YES. Zero blockers. Zero un-substitutable TradingView feeds.**

| Indicator | @ver | max_bars_back | Plots audited | RED | YELLOW | GREEN | The one "TV." dep | Hardest parity risk |
|---|---|---|---|---|---|---|---|---|
| TNT OD v3 | v5 | **1500** | 21 families / 42 shapes | 0 | 20 | 1 | `tv_ta.relativeVolume` (L738) | ET session-open anchoring (opening-drive) |
| Ultra Combo v57 | v6 | **2000** | 53 | 0 | 53 | 0 | `tv_ta.relativeVolume` (L350) | `highest(volume,5000)` vs mbb=2000 conflict |
| VOB Asym T3 v10 | v6 | **5000** | ~40 | 0 | ~40 | 0 | **none** (pure `ta.ema`) | EMA(2513) seed convergence > 6000 bars |
| HW Single v3 | v5 | **5000** | ~30 + 41 cosmetic | 0 | ~9 | ~21 | `tv_ta.relativeVolume` ×4 | session-bucketed RVOL needs ≥35 sessions |

**The only TradingView coupling in the entire batch = `import TradingView/ta/7 → tv_ta.relativeVolume(...)`.**
This is NOT a proprietary feed and NOT `request.security`. It is TradingView's **open-source** Pine library — readable, portable math. It is the same dependency Batch 1 found in B2B PUP. **VOB (the flagship) has zero library imports at all** — it is 100% native `ta.*` on OHLCV.

Confirmed line-by-line across all four: **0** `request.security`, **0** `request.financial/dividends/splits/economic`, **0** other-symbol series, **0** sub-candle/tick requirement, **0** literal `TV.` tokens. Anish's specific "TV dot" fear does not exist in these files.

---

## THE TWO REAL DEPENDENCIES (both resolved)

### A. `tv_ta.relativeVolume()` — present in TNT, Ultra, HW (NOT VOB)
Signature observed: `relativeVolume(length, anchorTimeframe, isCumulative, adjustRealtime)`.
- TNT L738: `relativeVolume(30, "", true, true)` — cumulative, realtime-adjusted.
- Ultra L350: `relativeVolume(30, "", false, true)` — non-cumulative.
- HW L288/298/299: `relativeVolume(reg_length, reg_anchorTimeframe, …)` — user-exposed anchor.

**Resolution — REPRODUCIBLE_WITH_WARMUP.** It is session-anchored relative volume:
`RVOL_t = cumVol_session(t) / mean_{k=1..M} cumVol_session_k(same time-of-session offset)`.
Port the open-source library source verbatim. **CRITICAL parity trap:** it is NOT `volume / sma(volume,30)`. With `anchor=""` it buckets by minute-of-session over the prior 30 daily sessions. A naive SMA port silently corrupts every directional signal that rides it (WTC / Hiroshima / Pentagon / WMD / WBUSH / LONG-SHORT gate / HCT combos).
**Warmup:** 30 sessions × 390 RTH minutes ≈ **11,700 1-minute bars** → the planned 6000-bar window is **INSUFFICIENT at 1m**. Pull ≥35 trading days of 1m warmup. At 5m/15m/1h the 6000-bar window is fine.
**Validate once** against TradingView live (`data_get_study_values` / table readout) on 2–3 high-volume tickers to ≤0.5%.

### B. EMA seed convergence on huge lengths — VOB flagship only
VOB's name is a **misnomer**: "T3 ×6" = Anish's *Tier-3 super signal*, **not** a Tillson T3 moving average. The engine is `ta.ema(close, sens)` vs `ta.ema(close, sens+13)` per tier, sens A=2513 … F=1013.
TradingView seeds EMA with the raw first close; residual seed weight after k bars = `(1-α)^k`, `α=2/(L+1)`. Bars-to-parity @ τ=0.1%:
**F(1013)≈3500 · E≈4360 · D≈5230 · C≈6950 · B≈7820 · A(2513)≈8680 bars.**
With `max_bars_back=5000` and a 6000-bar window, **tiers A/B/C will NOT match TV** — and because the two EMAs differ by only 13 in length, a 0.1% level error can flip a crossover → cascade into wrong zones/VLB/MZ on the *strongest* tiers (the highest-conviction VOB signals — non-droppable).
**Resolution — REPRODUCIBLE_WITH_WARMUP, fund more bars:** ≥10,000-bar burn-in for VOB; use pandas `ewm(adjust=False)` (NOT adjust=True); feed the same leading history TV had; validate vs `data_get_pine_lines` on ≥5 symbols.

---

## CROSS-CUTTING PARITY RISKS (apply to the porting layer)

1. **`max_bars_back` is per-indicator and SMALLER than people assume** (TNT 1500, Ultra 2000, VOB 5000, HW 5000). Several scripts call `ta.highest(volume,5000)` while `max_bars_back` is only 1500–2000 → **internal inconsistency in the Pine itself**. Decide per signal: replicate the *effective* TV lookback (clamped by mbb) OR honor the literal 5000 (the 6000-bar rebuild allows it). Then validate. **Correction to the working assumption: history length DOES matter** for any recursive/cumulative/session-bucketed series — "same settings ⇒ same output regardless of bar count" is FALSE for EMA seeding, `ta.cum`, from-genesis running maxima, and RVOL.
2. **Session / timezone anchoring** — TNT (opening-drive) is the highest-stakes: `session.isfirstbar` (L323), `time("D")` (L701), and first-bar gating drive FUSE/DENSITY/B2B/UU-streak/ALL alerts. Ultra uses `time(tf,"0930-1600","America/New_York")` (L95). Factory MUST timestamp in **America/New_York**, apply **DST-aware RTH (390-min) filtering**, and locate the 09:30 ET session-open bar via an exchange trading calendar. VOB uses `syminfo.timezone` for daily session reset (L282/414).
3. **`barstate.isconfirmed`** (all four) is **parity-SAFE offline** — every Massive candle is closed, so it's always true → no repaint. Compute on closed bars only. `barstate.islast` gates only cosmetic table/last-bar drawing (HW's 41 table cells are 100% cosmetic — no verdict not already emitted by a plotshape/alert).
4. **From-genesis running state**: Nagasaki cum-max (TNT L743, Ultra L357, VOB L716 "maxVolEver"), `ta.cum`, and VOB's `var array<level>` 15-zone state are path-dependent → genesis-aligned replay or a pinned anchor bar; document residual drift.
5. **Float volume after Massive 2026-02-23 decimal change**: `volume == highest(volume)` comparisons (Ultra L773 isHV) must use `>= max − ε`.
6. **`syminfo.mintick` rounding**: TNT/Ultra round to mintick; VOB MutEx line levels are **raw floats, no rounding** (L544–559) → no tick-gap there.

---

## COMPUTE / THROUGHPUT (DuckDB) NOTES + FALLBACKS

- **DuckDB builds candles + rolling/vectorizable features** (EMA via `ewm`, ATR, stdev, highest/lowest, cumsum). **State machines do NOT belong in SQL** — zones/charge/supertrend/density/15-zone dedup run as a row-by-row Python pass per ticker/TF.
- Embarrassingly parallel per (ticker, timeframe). Only per-bar inner loops to watch: Ultra `f_hadSignalYesterday` (~1000-iter, L853) and VOB per-crossover volume scan (L542) → vectorize as rolling windows / cumsum lookups.
- **Choke point:** 1m RVOL warmup (≥11,700 bars) × full watchlist (807 tickers) × 5 TFs. **Fallback:** stage RVOL warmup once into a parquet baseline table (minute-of-session × ticker), refresh daily; don't recompute per run.
- **Choke point:** VOB ≥10k-bar burn-in × 807 tickers. **Fallback:** burn-in only the watchlist subset actually charted; cache converged EMA state.

---

## BOTTOM LINE
All four reproducible from Massive OHLCV alone. **Front-load exactly two engineering tasks** before parity testing: (1) port `tv_ta.relativeVolume` as session-bucketed RVOL with ≥35-session warmup + parquet baseline; (2) fund VOB's ≥10k-bar EMA burn-in. Everything else is standard recursive-seed replication + ET session anchoring + row-by-row state-machine porting. Then hand to `pine-to-python-conversion` → `parity-verifier` for bar-for-bar proof.

Per-indicator detail: `TNT_OD_v3.md`, `Ultra_Combo_v57.md`, `VOB_Asym_T3_v10.md`, `Heavy_Weapons_Single_v3.md` (this dir).
