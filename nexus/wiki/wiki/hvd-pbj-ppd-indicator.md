# HVD-PBJ-PPD — High Volume Displacement + PBJ + USE Alarm (v4.26)

Source: nishpa800/indicators · hvd-pbj-ppd/versions/HVDPBJPPD_4.26.1244am_PPD_UC_RVOL_1x_2026-05-05.pine
Lines: 1,940 · Pine Script v5 · Overlay indicator

## What It Does

Detects co-occurrence of three independent measurement systems: high-volume
displacement candles (HV+D), PBJ supertrend reversals, and USE Alarm detection
engine signals. The core principle is the DECOUPLED PIPELINE ARCHITECTURE —
four completely isolated pipelines that produce terminal booleans, combined
only at the final AND gate. No pipeline ever reaches inside another. Each is
a black box.

This is the STRUCTURAL VALIDATION indicator — it answers "did a high-volume
displacement event coincide with a supertrend reversal AND an independent
pattern detection?"

## How It Works (the 4 Decoupled Pipelines)

### Pipeline A: HV+D (High Volume + Displacement)

**Inputs:** Volume rank + standard deviation candle range + FVG ONLY.
**Must NEVER reference:** PBJ, Zoo, Supertrend, FAUNA, RVOL, Ping Pong,
Combo Sets, or any USE engine variable.

Measures whether bar[1] had:
1. Extreme volume rank (highest volume in N-bar lookback, N = 50 to 1000, or all-time HEV)
2. Displacement: bar[1] range exceeds stdev(100) x multiplier
3. FVG confirmation: bar[0] gaps above/below bar[2] in the displacement direction

Three displacement tiers with independent stdev multipliers:
- **Base (d1):** 5.0x stdev — applies to all timeframes
- **HTF1 (d2):** 4.0x stdev — activates when chart TF is between configured From/To
- **HTF2 (d3):** 2.5x stdev — activates for higher timeframes

HV rank lookback windows: 50, 75, 100, 150, 200, 250, 300, 350, 400, 450,
500, 550, 600, 650, 700, 750, 1000 bars, plus All-Time High Volume (HEV).
Each has an individual enable checkbox.

**Terminal outputs:** `hvd_fire_bull`, `hvd_fire_bear` (fires bar N, describes bar N-1, offset=-1).

### Pipeline B: PBJ (Supertrend Entry)

**Inputs:** Zoo MA (VWMA len 5), ATR Supertrend (period 10, mult 2.0), PB&J filter ONLY.
**Must NEVER reference:** HV rank, displacement stdev, FVG, or any Pipeline A variable.

PBJ engine:
1. VWMA(5) with ATR(10) x 2.0 Supertrend trailing stop
2. Crossover/crossunder of price through Supertrend = PB (Price Break)
3. PBJ = PB at HH/LL extreme (25-bar) with volume confirmation (vol > 0.1x avg)
4. Reacceleration: Supertrend resumes movement after flat period
5. Up to 30 level zones tracked for approach detection

**Terminal outputs:** `sigBullPBJ`, `sigBullPB`, `sigBearPBJ`, `sigBearPB` (fires bar N, describes bar N, offset=0).

### Pipeline C: USE Alarm (45+ detections)

**Inputs:** USE's own engines (RVOL, FAUNA, Displacement, PBJ, Ping Pong, etc.)
**Must NEVER reference:** Any Pipeline A variable.

Pipeline C contains its OWN independent instances of PBJ and displacement —
these are NOT the same as Pipeline A or Pipeline B.

Engines within Pipeline C:
1. **RVOL (Engine 1):** Normalized price spike tiers (SAAB, Kratos, RVOL 1x Bull/Bear, Grand Slam, MOAB, Pentagon, WTC, Hiroshima, Nagasaki)
2. **FAUNA (Engine 2):** Candle anatomy (MB, RE, TA, GG, TR, ES, GDR)
3. **USE Displacement (Engine 3):** Three-tier displacement with configurable stdev multipliers (6.0/5.0/4.0) and FVG gating
4. **GZ1/HV FVG (Engine 4):** Gap Zone Intersection + High Volume FVG detection
5. **PUP/PPD (Engine 5):** Pocket Pivot Up/Down (>3% price move + volume exceeding lookback)
6. **PBJ (Engine 6 = Pipeline B):** Shared output
7. **Ping Pong SR (Engine 7):** Support/resistance with swing pivot, flat level, breakout/bounce/reject detection
8. **UU/UUU/UUUU (Engine 8):** Consecutive RVOL streak with path qualification (A-F pathways)
9. **Session/Alpha Strike (Engine 9):** First-of-day detection + multi-axis alpha signals
10. **Long/Short (Engine 11):** Relative volume ratio (regular and cumulative) x body ratio

### Pipeline D: Triple Co-Occurrence (AND Gate)

**Consumes ONLY:** Terminal booleans from A, B, and C.
**Must NEVER:** Re-evaluate internals of any pipeline, check if PBJ has high volume,
check if USE detections have HV+D displacement, or reach into any engine.

Offset alignment:
- `hvd_fire_bull` (bar N, describes N-1)
- `sigBullPBJ[1]` (bar N-1, describes N-1)
- `use_any_bull[1]` (bar N-1, describes N-1)
- All three align to bar N-1. Plot offset = -1.

## Detection Plots (51+ plotshapes + labels)

### Pipeline A Standalone — HV+D (6 plots)

| Plot | Name | Condition | Offset | What It Detects |
|------|------|-----------|--------|-----------------|
| A1 | HV+D Bull | hvd_fire_bull (volume rank hit + displacement + FVG, bullish) | -1 | High-volume displacement candle with FVG continuation |
| A2 | HV+D Bear | hvd_fire_bear | -1 | Bearish high-volume displacement |
| A3 | HV+D+PB Bull | hvd_fire_bull AND sigBullPB[1] | -1 | HV displacement + supertrend Price Break |
| A4 | HV+D+PBJ Bull | hvd_fire_bull AND sigBullPBJ[1] | -1 | HV displacement + full PBJ (PB at HH/LL extreme) |
| A5 | HV+D+PB Bear | hvd_fire_bear AND sigBearPB[1] | -1 | Bearish HV displacement + Price Break |
| A6 | HV+D+PBJ Bear | hvd_fire_bear AND sigBearPBJ[1] | -1 | Bearish HV displacement + full PBJ |

### Pipeline A — Back-to-Back HV+D (6 plots)

| Plot | Name | Condition | Offset | What It Detects |
|------|------|-----------|--------|-----------------|
| B1 | B2B HV+D Bull | hvd_fire_bull AND hvd_fire_bull[1] (consecutive) | -1 | Two consecutive HV displacement candles — extreme |
| B2 | B2B HV+D+PBJ Bull | B2B HV+D AND PBJ on either bar | -1 | Consecutive HV displacement + supertrend reversal |
| B3 | B2B HV+D+PB Bull | B2B HV+D AND PB on either bar (not PBJ) | -1 | Consecutive HV displacement + Price Break |
| B4 | B2B HV+D Bear | Mirror of B1, bearish | -1 | Bearish consecutive HV displacement |
| B5 | B2B HV+D+PBJ Bear | Mirror of B2, bearish | -1 | Bearish consecutive + PBJ |
| B6 | B2B HV+D+PB Bear | Mirror of B3, bearish | -1 | Bearish consecutive + PB |

### Pipeline A — HV+D Momentum Co-Occurrence (labels, not plotshapes)

These use labels to preserve the 64-plotshape budget.
Mutual exclusivity cascade: 3of3 > 2of3 > individual PBJ > non-PBJ.

| Label | Name | Condition | What It Detects |
|-------|------|-----------|-----------------|
| M1 | HVD+PUP | hvd_fire_bull + PUP[1], no PBJ | HV displacement + pocket pivot |
| M2 | HVD+PBJ+PUP | hvd_fire_bull + PBJ[1] + PUP[1] | HV displacement + supertrend + pocket pivot |
| M3 | HVD+RVOL | hvd_fire_bull + (RVOL1x or GrandSlam)[1], no PBJ | HV displacement + strong RVOL |
| M4 | HVD+PBJ+RVOL | hvd_fire_bull + PBJ[1] + RVOL[1] | HV displacement + supertrend + RVOL |
| M5 | HVD+CMB | hvd_fire_bull + Unified Combo, no PBJ | HV displacement + combo set |
| M6 | HVD+PBJ+CMB | hvd_fire_bull + PBJ[1] + Unified Combo | HV displacement + supertrend + combo |
| M7 | HVD+PBJ 2of3 | hvd_fire_bull + PBJ + 2 of {PUP, RVOL, CMB} | Double momentum confirmation |
| M8 | HVD+PBJ 3of3 | hvd_fire_bull + PBJ + PUP + RVOL + CMB | Maximum triple momentum |
| M9-M16 | Bear mirrors | Same logic, bearish (PPD instead of PUP) | Bearish momentum co-occurrence |

### Pipeline C — USE Alarm Detections (43 plots)

#### Priority Tier (4 plots)

| Plot | Name | Condition | Offset | What It Detects |
|------|------|-----------|--------|-----------------|
| P1 | SUPER Bull | PBJ + disp + (FAUNA or L1) + volume + (combo+PUP or platform) | -1 | Maximum multi-engine confluence |
| P2 | SUPER Bear | Mirror, bearish | -1 | Maximum bearish confluence |
| P3 | SD Bull | Platform + PBJ + volume + combo + PUP + disp + (FAUNA or L1) | -1 | Super Duper — all axes firing simultaneously |
| P4 | SD Bear | Mirror, bearish | -1 | Maximum bearish all-axis |

#### Tier 1 Detections (22 plots)

| Plot | Name | Condition | Offset | What It Detects |
|------|------|-----------|--------|-----------------|
| T1 | Bull UUUU | 4+ consecutive bullish RVOL bars, path qualified (A-F) | -1 | Extended bullish RVOL streak |
| T2 | Bull UUU | 3 consecutive, path qualified | -1 | Medium bullish streak |
| T3 | Bull UU | 2 consecutive, path qualified + oneOfThese gate | -1 | Short bullish streak with co-signal |
| T4 | Alpha Strike Bull | First detection of session + PP bull + (GS or RVOL1x) + PBJ + expanded FAUNA | -1 | First-bar alpha signal |
| T5 | Foxtrot Bull | 4 consecutive FAUNA-confirmed bullish bars | 0 | Sustained candle anatomy streak |
| T6 | Omega-A | Boom Hunter omega + high-confidence co-detection | 0 | Cycle-based alpha |
| T7 | OD Bull | Opening Drive — session bar count <= max + FVG combo + disp + PUP + PBJ | -1 | Opening drive first-bar combo |
| T8 | D2+ Bull | 2+ consecutive displacement bars + FAUNA on each | -1 | Serial displacement |
| T9 | D3+ Bull | 3+ consecutive displacement bars + FAUNA on each | -1 | Extended serial displacement |
| T10 | Golf Bull | 3-bar confirmed sequence: displacement + FAUNA + PUP | -1 | Triple-bar anatomy + displacement + pocket pivot |
| T11 | PAF PUP B2B | Back-to-back PUP + FAUNA bull | 0 | Consecutive pocket pivots with anatomy |
| T12-T22 | Bear mirrors + Combo Sets | CS1 FVG, CS2 MAT, Unified Combo, CC (Combo Chain), LSC (Long/Short Chain) | various | Pattern-specific detections |

#### Tier 2 — Structure (4 plots)

| Plot | Name | Condition | Offset | What It Detects |
|------|------|-----------|--------|-----------------|
| S1 | Floor | PP bull + PBJ + (RVOL1x or GS or WTC or Hiro or directional Nagasaki) | 0 | Support platform with volume |
| S2 | 2nd Floor | PP bull + PB + volume (gated) | 0 | Secondary support platform |
| S3 | Rooftop | PP bear + PBJ + volume | 0 | Resistance ceiling |
| S4 | Penthouse | PP bear + PB + volume | 0 | Secondary resistance ceiling |

#### Tier 3 — HW (2 plots)

| Plot | Name | Condition | Offset | What It Detects |
|------|------|-----------|--------|-----------------|
| HW1 | HW Bull | Green + 5x disp + PBJ + HW volume + platform | 0 | Highway — extreme displacement with structure |
| HW2 | HW Bear | Mirror, bearish | 0 | Bearish highway |

#### Special — Nagasaki Plus (1 plot, checkbox bypasser)

| Plot | Name | Condition | Offset | What It Detects |
|------|------|-----------|--------|-----------------|
| NAG | NAG+ Bull | Nagasaki + any directional bull co-signal | 0 | All-time-high volume with directional confirmation |

### Pipeline D — Triple Co-Occurrence (4 plots)

| Plot | Name | Condition | Offset | What It Detects |
|------|------|-----------|--------|-----------------|
| CO1 | CO HV+D+PBJ+USE Bull | hvd_fire_bull AND sigBullPBJ[1] AND use_any_bull[1] | -1 | All three pipelines agree: bullish + full PBJ |
| CO2 | CO HV+D+PB+USE Bull | hvd_fire_bull AND sigBullPB[1] AND use_any_bull[1] | -1 | All three agree: bullish + Price Break |
| CO3 | CO HV+D+PBJ+USE Bear | hvd_fire_bear AND sigBearPBJ[1] AND use_any_bear[1] | -1 | All three agree: bearish + full PBJ |
| CO4 | CO HV+D+PB+USE Bear | hvd_fire_bear AND sigBearPB[1] AND use_any_bear[1] | -1 | All three agree: bearish + Price Break |

## Key Input Parameters

### Pipeline A — HV+D

| Parameter | Default | What It Controls |
|-----------|---------|-----------------|
| Base Displacement Range Type | Open to Close | Body vs full range for stdev |
| Base Std Dev Length | 100 | Lookback for range stdev |
| Base Std Dev Multiplier | 5.0 | How many sigma for base displacement |
| HTF1 Std Dev Multiplier | 4.0 | Lower threshold for mid-timeframes |
| HTF2 Std Dev Multiplier | 2.5 | Lowest threshold for high timeframes |
| HTF1 From/To TF | 15 Min / 2 Hour | When HTF1 profile activates |
| HTF2 From/To TF | 2 Hour / 3 Month | When HTF2 profile activates |
| 50-Bar through 1000-Bar | all true | Which HV rank lookbacks to check |
| All-Time High Volume (HEV) | true | Include all-time volume check |

### Pipeline B — PBJ (hardcoded)

| Parameter | Value | What It Controls |
|-----------|-------|-----------------|
| Zoo MA Type | VWMA | Moving average type for signal line base |
| Zoo MA Length | 5 | MA period |
| Supertrend Period | 10 | ATR period for trailing stop |
| Supertrend Mult | 2.0 | ATR multiplier |
| PBJ HH/LL Lookback | 25 | Bars for extreme high/low check |
| PBJ Volume Mult | 0.1 | Minimum volume ratio for PBJ qualification |

### Pipeline C — USE Alarm

| Parameter | Default | What It Controls |
|-----------|---------|-----------------|
| Disp Min Mult | 6.0 | USE displacement minimum sigma |
| Disp Max Mult | 100.0 | Upper cap |
| GZ1 Max Bar Distance | 12 | Proximity for FVG overlap detection |
| Hotspot Lookback | 150 | HV check for GZ1/HV engine |
| Matrix Number Lookback | 67 | Neo lookback for highest volume detection |
| Opening Drive Max Bars | 2 | How many bars into session for OD signals |
| PBJ Proximity (bars) | 1 | UU/UUU streak PBJ distance requirement |
| Pivot Left/Right Bars | 5 / 1 | Swing pivot detection parameters |

### Master Controls

| Parameter | Default | What It Controls |
|-----------|---------|-----------------|
| First Candle of Day Required | false | Requires first bar + any HV rank |
| Aggregate Alerts | true | Combine all USE detections into one alert |

## The Black-Box Principle

The architecture enforces strict isolation:

1. Pipeline A knows NOTHING about PBJ, FAUNA, RVOL, or any USE engine
2. Pipeline B knows NOTHING about volume rank or HV+D displacement
3. Pipeline C knows NOTHING about Pipeline A's volume rank calculations
4. Pipeline D sees ONLY terminal booleans from A, B, and C — NEVER internals
5. Pipeline C has its OWN PBJ and displacement — they are NOT Pipeline A or B

**Why this matters:** When Pipeline D's CO signal fires, you KNOW that three
completely independent measurement systems — each blind to the others —
simultaneously detected the same event. This eliminates the false confidence
of correlated signals sharing code paths.

**How to add future detections:** Create Pipeline E with its OWN isolated
variables, produce a single terminal boolean, add it to Pipeline D's AND gate.
NEVER nest HV/displacement/PBJ checks inside the new pipeline.

## Relationship to VOB Thesis

HVD-PBJ-PPD validates VOB zones through independent structural measurement.
When a VOB zone forms (detected by the VOB indicator) and HVD-PBJ-PPD's
Pipeline D co-occurrence fires at the same price level, it confirms:

1. **Volume conviction** (Pipeline A) — the displacement candle had historically
   extreme volume relative to its own lookback
2. **Structural alignment** (Pipeline B) — the supertrend system agrees this
   is a reversal point
3. **Pattern confirmation** (Pipeline C) — one of 43+ independent detections
   corroborates the event

The Pipeline D CO signal inside a stacked VOB zone is one of the highest-conviction
setups in the entire indicator suite.

### Links
- [[vob-indicator]] — the zones these signals validate
- [[b2b-pup-indicator]] — shares Engine F (HV+D), Engine D (PBJ), Engine E (RVOL)
- [[tnt-od-indicator]] — shares displacement engine, PBJ, RVOL tiers
- [[squarify-indicator]] — shares UU/UUU/UUUU paths, FAUNA, RVOL, Combo Sets
- [[proximity-gzi-hv-indicator]] — Pipeline C Engine 4 (GZ1/HV FVG) uses same FVG logic
- [[heavy-combo-toggles-indicator]] — volume ratio classifications shared
