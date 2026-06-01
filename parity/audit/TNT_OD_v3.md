# Parity Audit — TNT Opening Drive (OD) v3

**Auditor goal:** Determine whether every detection plot can be reproduced EXACTLY from
local OHLCV(+volume) candles rebuilt from Massive minute-aggregates, or whether any plot
depends on data TradingView supplies that Massive/local candles do not.

---

## 1. Header

| Field | Value | Line |
|---|---|---|
| Indicator name | `TNT Opening Drive OD v3` (short `TNT OD v3`) | 190 |
| Pine version | `//@version=5` (NOTE: declared v5, but file is described as "Pine v6" in the task; the `@version` annotation says **5**) | 189 |
| Declaration | `indicator("TNT Opening Drive OD v3", "TNT OD v3", overlay = true, max_lines_count = 500, max_labels_count = 500, max_boxes_count = 500, max_bars_back=1500)` | 190–191 |
| overlay | `true` | 190 |
| **max_bars_back** | **1500** | 191 |
| Library import | `import TradingView/ta/7 as tv_ta` | 193 |
| Visible detection plots (`plotshape`) | **42** plotshapes (21 bull/bear pairs) | 1728–1797 |
| Alert-only detections | NAGASAKI standalone alert (no plotshape) | 2143–2146 |
| Distinct named signals plotted | 21 plot families (see table) | — |

**CRITICAL HEADER FINDING:** `max_bars_back=1500` is set. The candle factory targets **~6000 bars**.
Two of this indicator's lookbacks (`ta.highest(volume, 5000)` line 905, `ta.highest(volume, 1000)`
lines 753/793-cluster) request more history than `max_bars_back` guarantees AND the all-time-high
Nagasaki accumulator (lines 743–749) is unbounded from bar 0. This is the #2 parity risk after the
library import. See §4 and §5.

---

## 2. STATUS TABLE — one row per detection plot

All plots are built from OHLCV+volume and a long chain of derived booleans. The chain reduces to a
small set of **shared parity-critical primitives**; every plot inherits the worst status of the
primitives it depends on. Primitives flagged below:

- **P-LIB** `tv_ta.relativeVolume(30,"",true,true)` (line 738) → feeds `u5_relVolRatio` → WTC / Hiroshima / Pentagon / WMD, HCT group-B, all enrichment paths. **Library black box.**
- **P-NAG** `u5_Nagasaki` running all-time-high volume from bar 0 (743–749). **Unbounded path-dependent.**
- **P-HV** `ta.highest(volume, 5000)` (905), `ta.highest(volume,1000)` (753), `[1]`-offset. **Deep lookback vs max_bars_back=1500.**
- **P-SESS** `session.isfirstbar` (323), `time("D")` (701), `timeframe.in_seconds` (327). **Session/TZ anchoring.**
- **P-STDEV** `ta.stdev(disp_range, N)` warmup seeding (580, 785, 961, 1098, 1153). **Converges; low risk.**
- **P-MINTICK** `syminfo.mintick` (825). **Symbol metadata.**
- **P-CONF** `barstate.isconfirmed` (everywhere). **Bar-close execution model.**

| # | Detection Plot | What it fires on (1-line math) | Inputs | Status | Parity Risk | Mitigation |
|---|---|---|---|---|---|---|
| 1 | **B2B NAPALM** Bull/Bear (1728–1729) | Napalm on bar[1] AND bar[0]; Napalm = displacement+FVG through an opposing active TNT zone (590–601); gated by `gate_bull[1]` | OHLC, vol, ta.ema/stdev/atr, zones, P-SESS, P-CONF; gate pulls P-LIB+P-NAG+P-HV via `gate_bull` | YELLOW | Inherits gate → P-LIB / P-NAG via `hct_bull`,`nagAny`,`uc`; stdev warmup | Reproduce gate atoms (see §5). Without `tv_ta.relativeVolume` re-derivation, WTC/Hiro/Pentagon legs of gate diverge. |
| 2 | **RC NPM+TNT** Bull/Bear (1730–1731) | Napalm AND TNT on same visual bar; `gate_*[1]` (1175–1176) | OHLC, vol, ta.ema/rsi/median/stdev/atr, P-SESS, P-CONF, gate | YELLOW | Gate (P-LIB/P-NAG); TNT synergy uses rsi(14)+ema warmup | Re-derive gate atoms; seed RSI/EMA with ≥ slow-EMA warmup (SENS+13 default 113). |
| 3 | **FUSE** Bull/Bear (1733–1734) | Sequential NPM→TNT→CONT within `SUDDEN_PROX` bars, `>= sessionFirstBarIdx` (1198–1199) | OHLC, vol, ta.*, P-SESS (session-bounded), P-CONF | YELLOW | Session anchoring: FUSE requires NPM `>= sessionFirstBarIdx` → wrong session boundary breaks it | Anchor candle factory sessions to exchange TZ; see §4. No library dep. |
| 4 | **CATALYST** Bull/Bear (1736–1737) | Napalm AND CS1 (FVG-combo) same bar; `gate_*[1]` (1211, 1253) | OHLC, vol, ta.highest(vol,5000/252/63), ta.cum, P-LIB(via gate), P-NAG | YELLOW | CS1 uses P-HV (`highest(volume,5000)` 905) + gate (P-LIB/P-NAG) | Warm up ≥5000 bars OR accept CS1 HV-leg divergence; re-derive gate. |
| 5 | **PBJ+NPM** Bull/Bear (1739–1740) | PBJ supertrend reversal + Napalm same visual bar; `pnGate`+`gate_*[1]` (1182, 1249) | OHLC, vol, ta.vwma(5), ta.atr(10/14), ta.ema(20), P-LIB(via gate) | YELLOW | PBJ supertrend is recursive (`var u5_st_dir`, 800–809) — path-dependent but self-converging; gate P-LIB | Seed supertrend over ≥50 bars; re-derive gate. |
| 6 | **PBJ+TNT** Bull/Bear (1742–1743) | PBJ reversal + TNT same bar; `ptGate` (1184, 1250) — NOT new-gated | OHLC, vol, ta.vwma/atr/ema/rsi/median, P-CONF | YELLOW | `ptGate` sub-minute leg uses `u5_WMD` (P-LIB). On ≥1m TF `ptGate` passes trivially (`not isSubMinute`) | On 1m+ TFs `isSubMinute` false → gate trivially true; pure OHLCV. On sub-minute (not in factory's 5 TFs) it needs P-LIB. **Safe for 1m/5m/15m/1h/D.** |
| 7 | **IGNITE T+C** Bull/Bear (1745–1746) | TNT + Continuous same bar (1202) | OHLC, vol, ta.*, P-CONF | YELLOW | TNT synergy warmup only | Standard warmup. No library/session-critical dep. |
| 8 | **IGNITE N+C** Bull/Bear (1747–1748) | Napalm + Continuous(bar[1]) (1204) | OHLC, vol, ta.*, zones, P-CONF | YELLOW | Zone-array + stdev warmup | Standard warmup; offset-1. |
| 9 | **DYNAMITE** Bull/Bear (1750–1751) | bar[1]&bar[2] both exceed `dynStdMult·stdev(100)` + same color + FAUNA on both + bar[0] FVG (960–975) | OHLC, vol, ta.stdev(100), ta.sma(20/50/10), ta.atr(14), P-CONF | **GREEN** | Pure OHLCV+vol + standard ta.*. FAUNA = candle anatomy. No library, no session, no deep HV. | None needed beyond 100-bar stdev + 50-bar SMA warmup. **Fully reproducible.** |
| 10 | **TNT ENRICHED** Bull/Bear (1754–1755) | Raw TNT + `enrichBull_N` co-signal + `gate_*` (1260–1261) | OHLC, vol, P-LIB (WMD in enrich), P-HV (HV1000), P-NAG (via gate) | **RED-leaning YELLOW** | `enrichBull_N` includes `u5_WMD` (P-LIB) and `u5_HV1000` (P-HV); gate adds P-LIB/P-NAG | Enrichment has OR-redundant legs (RVOL1x/PUP/CS1/FAUNA are OHLCV); fires can still occur w/o the library legs, but **exact** match needs P-LIB re-derivation. See §5. |
| 11 | **NPM ENRICHED** Bull/Bear (1757–1758) | Raw Napalm + `enrichBull_N1` + `gate_*[1]` (1262–1263) | OHLC, vol, P-LIB, P-NAG, P-HV | YELLOW | enrich_N1 includes Pentagon/WTC/Hiro (P-LIB), Nagasaki (P-NAG), HV1000 (P-HV) | Same as #10. |
| 12 | **CONT ENRICHED** Bull/Bear (1760–1761) | Raw Continuous + `enrichBull_N` + `gate_*` (1264–1265) | OHLC, vol, P-LIB, P-NAG | YELLOW | enrich_N (`u5_WMD`) + gate | Same as #10. |
| 13 | **RC TNT+RET ENR** Bull/Bear (1763–1764) | TNT+Return same bar + enrich_N + gate (1266) | OHLC, vol, P-LIB, P-NAG | YELLOW | enrich + gate | Same as #10. |
| 14 | **RC RET+NPM ENR** Bull/Bear (1766–1767) | Return+Napalm + enrich_N1 + gate[1] (1267) | OHLC, vol, P-LIB, P-NAG, P-HV | YELLOW | enrich_N1 + gate | Same as #10. |
| 15 | **PBJ+RET ENR** Bull/Bear (1769–1770) | PBJ+Return + enrich_N + gate (1268) | OHLC, vol, P-LIB, P-NAG | YELLOW | enrich + gate | Same as #10. |
| 16 | **DENSITY 1/2/3** Bull/Bear (1773–1778) | X visual events in Y bars; visual pool = TNT/Napalm/Cont/RC/PBJ events (1276–1338), session-bounded by `sessionFirstBarIdx` | OHLC, vol, ta.*, P-SESS, P-CONF | YELLOW | Density count resets/bounds on `sessionFirstBarIdx` (1290,1298…) → wrong session anchor mis-counts. Pool itself OHLCV. | Anchor sessions exactly (§4). No library dep in the density pool (events are TNT/Napalm = OHLCV). |
| 17 | **UU/UUU/UUUU+TNT ANY** Bull/Bear (1781–1786) | RVOL streak ≥2/3/4 (`u5_bb_normPrice≥0.5`) + path qual + any TNTOD signal in window (1573–1578) | OHLC, vol, ta.sma, P-SESS (`hasDay1` via `time("D")`), P-CONF | YELLOW | Streak `hasDay1` flag uses `ta.change(time("D"))` (701) → day-boundary detection = P-SESS. RVOL leg is OHLCV (spike/vol SMA). | Anchor day boundary in exchange TZ (§4). The "TNT ANY" pool can include CATALYST/B2B → indirectly P-LIB via gate, but UU itself OHLCV. |
| 18 | **WBUSH+TNTOD ANY** Bull/Bear (1789–1790) | Heavy Pentagon state (15 sub-combos) AND any TNTOD plot (1687–1688) | OHLC, vol, **P-LIB** (groupB=Pentagon/WTC/Hiro from `u5_relVolRatio`), P-NAG | **RED-leaning YELLOW** | Heavy Pentagon group-B (994) is **entirely** `tv_ta.relativeVolume`-derived. Direction classifier `u5_DISPBull/Bear` is OHLCV. | Without re-deriving `relativeVolume`, group-B legs cannot match → WBUSH Yin-Yang/Trident/NHx2 diverge. See §5. |
| 19 | **WBUSH Neutral** (1791) | Heavy Pentagon neutral state, standalone (1689, no TNTOD pairing) | OHLC, vol, **P-LIB**, P-NAG | **RED-leaning YELLOW** | Same P-LIB dependency as #18; fires standalone so divergence is visible | Re-derive `relativeVolume`; see §5. |
| 20 | **T1 RELAY** Bull/Bear (1794–1795) | Any Tier1 visual on bar[2] AND on bar[1], same dir (1668–1669); pool = 11 Tier1 incl HCT, UC (1662–1665) | Union of plots 1–9 + `hct_bull`(P-LIB) + `uc_bull` | YELLOW | Pool includes HCT (P-LIB group-B) and UC (uses u5_WMD=P-LIB). Most pool members GREEN/YELLOW. | Reproducible to the extent its component plots are; P-LIB legs (HCT, UC-WMD) are the only gaps. |
| 21 | **T1 STACK** Bull/Bear (1796–1797) | ≥2 distinct Tier1 visuals on bar[1] (1672–1675) | Same pool as #20 | YELLOW | Same as #20 | Same as #20. |
| A1 | **NAGASAKI** standalone alert (2143–2146) | `u5_Nagasaki` all-time-high volume from bar 0; checkbox default OFF | volume only, **P-NAG**, P-SESS (first-bar gap text) | YELLOW | All-time-high since bar 0 → **strictly path-dependent on history start**. Default OFF. | Anchor the accumulator start consistently (see §5 P-NAG). Volume-only otherwise. |

---

## 3. Tally

- **GREEN: 1** (DYNAMITE — plot #9, the only plot with zero library/session/deep-HV dependency)
- **YELLOW: 20** (everything else — reproducible with care; mitigations stated)
- **RED: 0** (no `request.security` / `request.financial` / `request.dividends` / external-symbol / tick-finer-than-candle dependency exists anywhere in the file — coarse grep confirmed line-by-line)

**Two YELLOWs are "hard-YELLOW / RED-leaning"** because they depend materially on the
`tv_ta.relativeVolume` library call whose internals are not standard `ta.*`: **WBUSH bull/bear
(#18) and WBUSH Neutral (#19)**, plus the library leg embedded in all Tier-2 enrichment plots
(#10–#15) and HCT/UC group-B. These are reproducible but require re-implementing the library
function (§5), not just calling a standard indicator.

---

## 4. SESSION / TIMEZONE DEEP-DIVE (the #1 opening-drive parity risk)

This is an **opening-drive** indicator. Three constructs anchor everything to the session, and the
candle factory MUST reproduce their timestamps exactly or plots fire on the wrong bars.

**Verbatim session/TZ lines:**

```pine
323  bool isFirstBar = session.isfirstbar
324  var int sessionFirstBarIdx = na
325  if isFirstBar
326      sessionFirstBarIdx := bar_index
327  int u5_tfSec = timeframe.in_seconds(timeframe.period)
328  bool isSubMinute = u5_tfSec <= 60
```

```pine
701  bool u5_is_new_day = ta.change(time("D")) != 0
702  var int u5_sessionBarCount = 0, var int u5_lastCountedBar = -1
703  if u5_is_new_day and bar_index != u5_lastCountedBar
704      u5_sessionBarCount := 1, u5_lastCountedBar := bar_index
705  else if bar_index != u5_lastCountedBar
706      u5_sessionBarCount += 1, u5_lastCountedBar := bar_index
```

```pine
1700 bool isF_N = isFirstBar
1701 bool isF_N1 = not na(sessionFirstBarIdx) and (bar_index - 1) == sessionFirstBarIdx
```

**Where session anchoring gates real plots:**

- **FUSE** (1198–1199): `lastBullNPMVis >= nz(sessionFirstBarIdx, 0)` — the cascade must start within the current session. Wrong session boundary → FUSE fires across sessions or never.
- **DENSITY 1/2/3** (1290, 1298, 1306, 1314, 1322, 1330): every density count requires `(bar_index-1-i) >= nz(sessionFirstBarIdx,0)` and resets on `isFirstBar` (1283–1286). Mis-anchored session = wrong event counts.
- **B2B NAPALM** (1247–1248): `(bar_index - 2) >= sessionFirstBarIdx` — both Napalm bars must be in-session.
- **UU/UUU/UUUU** (1350, 1354): `hasDay1` is set from `u5_is_new_day` (`ta.change(time("D"))`) — the streak's "saw a day-1 bar" qualifier (path pA).
- **ALERT GATING** (1700–1719): `masterFirstBar` ON requires `isF_N`/`isF_N1` (first bar of session) AND HV-rank. The entire "FIRST !!! / FIRST XXX / NOT !!!" status string (1706, 1711) is session-derived.

**Two distinct anchors are in play — and they are NOT the same:**

1. **`session.isfirstbar`** = first bar of the symbol's *regular session* per the chart's session
   spec / exchange calendar. TradingView resolves this from `syminfo` exchange + session string
   ("0930-1600" for US equities) in the exchange timezone (America/New_York).
2. **`time("D")` change** = a *calendar-day* boundary in the **exchange timezone** (`syminfo.timezone`),
   used for `u5_is_new_day` and `hasDay1`. This is a day rollover, not the session open.

**HOW THE LOCAL CANDLE FACTORY MUST ANCHOR BARS (exact spec):**

- Massive minute aggregates are stamped in **UTC epoch (nanoseconds/ms)**. Convert to
  **America/New_York** (handles EST/EDT DST automatically — do NOT hardcode -5/-4).
- **Regular session = 09:30–16:00 ET.** Anish's CLAUDE.md notes he thinks in CT (08:30–15:00 CT);
  that is the same instants as 09:30–16:00 ET. Anchor to **ET / exchange TZ**, because that is what
  TradingView uses for `session.isfirstbar` and `syminfo.timezone` for US equities.
- **`session.isfirstbar` equivalent:** the first bar whose ET timestamp ≥ 09:30:00 on each trading
  day, using an **exchange trading-calendar** (skip weekends + NYSE holidays + half-days). If the
  factory blindly takes "first bar after midnight" it will mis-fire every opening-drive plot.
- **`time("D")` equivalent:** ET calendar-date change. A bar at 09:30 ET starts a new "D" only if its
  ET date differs from the prior bar's ET date. (For intraday US-equity bars this coincides with the
  session start, so in practice anchor #1 and #2 align — but only if you use ET, not UTC.)
- **Decide the data window first:** if the factory feeds only RTH (regular-hours) bars, the first RTH
  bar of the day IS `session.isfirstbar`. If it feeds 24h/extended-hours bars, you must apply the
  09:30 ET session filter to identify the first-bar — otherwise `isFirstBar` lands on the 04:00 ET
  pre-market bar and the "Opening Drive" thesis collapses.

**Acceptance test for session parity:** for a known symbol/day, the local factory's `isFirstBar`
bar index must equal the bar TradingView marks (verify via `data_get_ohlcv` / chart timestamps).
`u5_sessionBarCount==1` must land on the 09:30 ET bar.

---

## 5. Hard-dependency deep problem-solve (P-LIB, P-NAG, P-HV)

### 5.1 P-LIB — `tv_ta.relativeVolume(30, "", true, true)` (line 738) — the single biggest parity risk

**Define the dependency.** Line 738:
```pine
[u5_currentVol_reg, u5_pastVol_reg, _u5_unused] = tv_ta.relativeVolume(30, "", true, true)
float u5_relVolRatio = u5_currentVol_reg / u5_pastVol_reg
```
`u5_relVolRatio` drives **Pentagon / WTC / Hiroshima** (740–742), which feed `u5_WMD` (750),
Heavy-Pentagon group-B (994 → all of WBUSH #18/#19), HCT group-B (1107 → `hct_bull/bear` → the new
gate), Tier-2 enrichment legs (1228–1237), and UC's `u5_WMD` leg (1132–1133). It is the most
load-bearing non-OHLCV-trivial primitive in the file.

**Knowns.** It is from the official `TradingView/ta/7` library, version-pinned. Signature
`relativeVolume(length, anchor, isCumulative, isAdjusted)` (positional here: `30`, `""`, `true`,
`true`). It computes current vs. historical volume at the equivalent intraday point, **anchored**
(the `""`/cumulative/adjusted args control session-relative accumulation and time-of-day matching).
It is computed entirely from **volume + bar time** — it does NOT pull an external feed, another
symbol, or `request.security`. Therefore it is **reproducible from local candles** — it is just not
a one-liner `ta.*`.

**Unknowns (resolve before claiming exact parity).** The exact accumulation window, how `anchor=""`
defaults (session vs none), whether `isAdjusted` applies a time-of-day normalization, and the exact
"past volume" reference set. These are not visible in this file.

**Governing relationship (inferred).** `relVol ≈ cumVol_session_to_now / avg(cumVol_session_to_same_time_of_day over N prior sessions)`, with `isAdjusted` normalizing for partial-bar/time-of-day. The thresholds (`f_u5_wtc`, `f_u5_hiro`, etc., 722–728) are applied to this ratio.

**Concrete avenue from Massive data.** Massive provides full **1-minute aggregates with volume +
exact bar start time** (the candle factory's own source) and **tick trades** if finer is needed.
Reproduce by: (1) **read the library source** via TradingView MCP (`pine_open` /
`pine_get_source` on `TradingView/ta/7`, or `mcp__tradingview__data_get_study_values` to capture
live `relativeVolume` outputs and reverse-engineer), then port the exact accumulation logic; or
(2) **calibrate empirically** — capture `u5_relVolRatio` from the live chart via the TV MCP
(`data_get_study_values` after exposing it as a plot) across many bars and fit the local
reimplementation until WTC/Hiro/Pentagon boundaries match. Recommended: do (1) first since it's a
published, readable library — this converts the unknown into a deterministic port.

**Blast radius if dropped.** Dropping the `relativeVolume` leg would **break WBUSH #18/#19
entirely** (group-B is 100% relVol) and **weaken** Tier-2 enrichment, HCT, and UC (they have
OR-redundant OHLCV legs — RVOL1x/PUP/CS1/FAUNA/Nagasaki — so they would still fire, just not
identically). WBUSH is a high-conviction confluence plot; do NOT drop it. Port the library.

### 5.2 P-NAG — `u5_Nagasaki` unbounded all-time-high (lines 743–749)

```pine
743  var float u5_maxVol = 0.0
745  if bar_index == 0
746      u5_maxVol := volume
747  else if volume > u5_maxVol
748      u5_isNag := true, u5_maxVol := volume
```
**Dependency:** "highest volume since the script's first bar." It is **strictly path-dependent on
where history starts.** With `max_bars_back=1500` and a 6000-bar factory, TradingView and the local
engine will disagree on `u5_maxVol` unless both start the accumulator at the **same bar**.
**Mitigation:** define a fixed anchor (e.g., first bar of the loaded 6000-bar window, or first bar
of available Massive history per symbol) and start the accumulator there in BOTH systems. Document
the anchor in the parity contract. Nagasaki feeds the gate (`nagAny`), Heavy-Pentagon, HCT
base-combos, and the (default-OFF) standalone alert. Volume-only otherwise → easy to reproduce once
the anchor is pinned.

### 5.3 P-HV — deep volume lookbacks vs `max_bars_back=1500`

- `ta.highest(volume, 5000)[1]` (line 905, CS1) — needs 5001 bars of history to be exact.
- `ta.highest(volume, 1000)[1]` (line 753, HV1000) and `ta.highest(volume, 252/63)` (905).
- `max_bars_back=1500` (191) is **smaller than 5000** → TradingView itself will not look back the
  full 5000 bars; it caps at the available/declared history. **The candle factory must replicate
  the same effective cap.** If the factory feeds 6000 bars but TV only saw 1500, the `highest(.,5000)`
  values differ.

**Mitigation:** (a) match the effective lookback — either raise TV's `max_bars_back` to ≥5001 AND
feed ≥5001 bars in both systems, or (b) cap the local `highest()` to the same window TV actually
used. Easiest exact-parity path: feed both systems the SAME bar count (≥6000) and set
`max_bars_back=5000`+ in the ported Pine reference used for cross-check. For the production Python
engine, compute `highest(volume, min(N, bars_available_since_anchor))`.

### 5.4 Other YELLOW primitives (low risk, standard mitigation)

- **P-STDEV / RMA-EMA warmup:** `ta.stdev` (580/785/961/1098/1153), `ta.ema`/`ta.rsi`/`ta.atr`
  (320, 379, 522, 798, 813). EMA/RMA/RSI/ATR are exponentially-weighted and **converge** after
  ~5×length bars; they are mildly path-dependent on history length but converge to the same value
  given identical seeding. Mitigation: feed ≥ max(5×slowest-length) warmup bars before the first
  evaluated bar; seed EMA with SMA of first `length` bars (Pine's convention) — `ta.ema` seeds with
  the first source value, `ta.rma`/`ta.atr`/`ta.rsi` seed with SMA. Match Pine's seeding exactly in
  Python (this is the classic RMA-seed gotcha). Slowest length here: `ta.atr(200)` (320),
  `ta.ema(SENS+13)` (default 113), `ta.highest(.,5000)`. Warm up ≥1000 bars minimum, ideally the
  full 6000.
- **P-MINTICK:** `syminfo.mintick` (825), used only as a minimum-width filter when pushing a PBJ
  level. Mitigation: store per-symbol tick size from Massive reference (`/v3/reference/tickers` —
  available) and apply identically. Negligible effect on whether a plot fires (it filters
  degenerate zero-width levels).
- **P-CONF:** `barstate.isconfirmed` everywhere — means every signal is evaluated **on bar close**.
  Mitigation: the candle factory operates on completed bars only, so this maps cleanly (evaluate
  each plot on the closed bar). No realtime-flicker concern in a batch backtest. There is **no**
  `barstate.isrealtime` / `barstate.islast` branching that would change historical values.

---

## 6. ta.* FUNCTION INVENTORY (confirm each is standard/reproducible)

| Function | Lines (examples) | Standard? | Notes |
|---|---|---|---|
| `ta.atr` | 320 (200), 321, 798 (10), 813 (14) | ✓ | RMA-based; seed with SMA(length). Reproducible. |
| `ta.ema` | 379 (fast/slow), 813 (20) | ✓ | Seeds with first value. Reproducible. |
| `ta.sma` | 711, 713, 717, 756, 757, 813 | ✓ | Simple mean. Reproducible. |
| `ta.stdev` | 580, 785, 961, 1098, 1153 | ✓ | Population stdev (Pine default biased). Match `ddof=0`. |
| `ta.rsi` | 522 (14) | ✓ | RMA-based; seed carefully. Reproducible. |
| `ta.highest` | 384, 753, 793, 816, 905, 1714, 1715 | ✓ | Rolling max. **But see P-HV (5000-bar vs max_bars_back).** |
| `ta.lowest` | 413, 815 | ✓ | Rolling min. Reproducible. |
| `ta.vwma` | 798 (5) | ✓ | Volume-weighted MA. Reproducible from OHLCV. |
| `ta.median` | 522 (volume, EMA_SLOW) | ✓ | Rolling median. Reproducible. |
| `ta.cum` | 907, 1094 | ✓ | Cumulative sum from bar 0 → **path-dependent on history start** (like P-NAG, but a running mean of range/low). Anchor consistently. |
| `ta.change` | 701 | ✓ | Used on `time("D")` → P-SESS (day boundary), not a price diff. |
| `ta.crossover` / `ta.crossunder` | 380, 381, 810 | ✓ | Reproducible. |
| **`tv_ta.relativeVolume`** | 738 | **✗ (library)** | **NOT a standard ta.* — see §5.1 P-LIB. The one function requiring a port, not a call.** |

All standard `ta.*` are reproducible. The **only** non-standard math primitive is
`tv_ta.relativeVolume` from the imported library.

---

## 7. DuckDB / compute concerns at scale (~6000 bars × 5 TFs × N symbols)

1. **Stateful recursion is NOT a SQL/DuckDB operation.** Large parts of this indicator are
   imperative and path-dependent: the zone arrays (`tnt_zones`, `super_zones`, `charge_levels`,
   `u5_bull_lvls`), the supertrend `var u5_st_dir` (800–809), `var u5_maxVol`, the density
   ring-state (`d1br/d1ba…`), and the FUSE/streak `var int last…` trackers. DuckDB is the right
   tool for **bar construction** (resample 1m → 5m/15m/1h/D via `time_bucket`, aligned to the
   09:30 ET session anchor) and for the **windowed ta.*** primitives (EMA/SMA/stdev/highest as
   window functions), but the zone/charge/supertrend/density state machines must run in **Python
   row-by-row** (or a Numba/vectorized state pass). Plan: DuckDB produces the candle table + cheap
   rolling features; Python computes the stateful detections.
2. **Lookback window vs storage.** `highest(volume,5000)` means you need ≥5000 prior bars of warmup
   PER (symbol, timeframe) before the first valid bar. For 1m bars that's ~13 trading days of RTH
   (390 bars/day) just for warmup; for the daily TF, 5000 bars is ~20 years — likely unattainable
   and TV-capped at `max_bars_back=1500` anyway. **Resolve the effective lookback per TF** (see
   §5.3) and store it in the parity contract; don't silently let DuckDB compute a "true" 5000 when
   TV used 1500.
3. **Session alignment is the join key.** Bucketing must be done in **America/New_York** with a
   trading-calendar mask. DuckDB `time_bucket` on naive UTC will straddle the 09:30 boundary and
   silently desync `isFirstBar`. Build a `session_id` / `is_first_bar` column once, in ET, and carry
   it through every TF.
4. **`ta.cum` / `var u5_maxVol` anchoring** (P-NAG, line 907 `u5_gz_thresh`): cumulative-from-bar-0
   values depend on the window start. Pin the anchor bar per symbol and store it so reruns are
   deterministic.
5. **EMA/RMA seeding** must match Pine's convention exactly or every gated plot drifts on early
   bars — assert parity on a golden symbol/day against TV MCP `data_get_study_values` before
   trusting the batch.
6. **Float determinism:** Pine uses f64; use float64 in Python/DuckDB and replicate Pine's operation
   order where thresholds are razor-thin (the displacement `> stdev*mult` comparisons).

---

## 8. BOTTOM LINE

**Can the whole indicator be reproduced locally? → YES, WITH CAVEATS.**

There is **zero RED** dependency: no `request.security`, no `request.financial/dividends/splits`, no
external symbol, no tick-finer-than-the-candle requirement. Every input is OHLCV+volume+bar-time,
all of which Massive supplies. Coarse grep's "zero externals" finding is **confirmed line-by-line.**

**Caveats (all YELLOW, all mitigable):**

1. **`tv_ta.relativeVolume` (line 738) must be ported, not called.** It is the one non-standard
   primitive and it is load-bearing for WBUSH (#18/#19) and a leg of every Tier-2 enrichment plot,
   HCT, and UC. Port it from the published `TradingView/ta/7` source (readable via TV MCP) or
   calibrate against live `data_get_study_values`. This is the single biggest parity risk.
2. **Session/timezone anchoring is the #1 structural risk for this opening-drive indicator.** The
   candle factory MUST timestamp in **America/New_York**, identify the **09:30 ET session-open bar**
   with an exchange trading calendar, and reproduce both `session.isfirstbar` and `time("D")`
   day-boundary. Get this wrong and FUSE, DENSITY, B2B, UU-streak, and ALL alert gating fire on the
   wrong bars.
3. **Deep volume lookbacks (`highest(volume,5000)`) collide with `max_bars_back=1500`.** Match the
   *effective* lookback in both systems; don't let the local engine see more history than TV did.
4. **`u5_Nagasaki` and `ta.cum` are unbounded path-dependent from bar 0.** Pin a fixed anchor bar
   in both systems.
5. **EMA/RMA/RSI/ATR warmup seeding** must replicate Pine's seeding convention; warm up ≥1000 bars
   (ideally the full 6000) before the first evaluated bar.
6. Only **DYNAMITE (#9)** is GREEN with no caveats — pure OHLCV + standard ta.*.

**Recommendation:** Proceed with local reproduction. Front-load two tasks: (a) port
`tv_ta.relativeVolume` exactly and validate against TV MCP, and (b) build the ET-anchored session
column. With those two solved, the remaining 19 YELLOW plots reduce to standard warmup + state-machine
porting and should reach bar-for-bar parity. Validate on a golden (symbol, day) using TradingView
MCP `data_get_study_values` / `data_get_pine_labels` before trusting the batch over 6000 bars.
