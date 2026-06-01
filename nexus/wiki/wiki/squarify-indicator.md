# SQUARIFY — 46-Signal Detection Suite (v2)

Source: nishpa800/indicators · squarify/versions/SQUARIFY_46_v2_2026-05-04.pine
Lines: 2,622 · Pine Script v5 · Overlay indicator

## What It Does

The largest signal set in the indicator suite. 46 detection plots, each a buy/sell
trigger. Combines all engines from B2B PUP (FAUNA, RVOL, Displacement, PBJ, TNT,
Napalm, HV+D, Combo Sets) plus unique signals: SUPER, SDUPER, GOLF, WBUSH, UU/UUU/UUUU
qualification streaks, Alpha Strike, Opening Drive, and more.

## All 46 Detection Plots

### Tier S (Supreme — highest conviction)
| # | Name | Condition | Offset |
|---|------|-----------|--------|
| 1 | **SD! (SDUPER)** | Unified Combo + Napalm(consolidated) + PUP. All same bar. | -1 |
| 2 | **SUPER** | Unified Combo + Napalm(consolidated). All same bar. | -1 |
| 32 | **GRAIL** | Napalm + PBJ + PUP + Unified Combo ALL on same bar. | -1 |
| 44 | **NPM+UC+PBJ** | Napalm + Unified Combo + PBJ. | -1 |
| 45 | **UC NAGASAKI Bull** | Unified Combo + All-Time-High Volume on same bar. | -1 |
| 46 | **UC NAGASAKI Bear** | Bear mirror of #45. | -1 |

### Tier A (Alpha — multi-engine confluence)
| # | Name | Condition | Offset |
|---|------|-----------|--------|
| 3 | **HW (Heavy Weapon)** | Green bar + 5x displacement + PBJ + (GS/WTC/Hiro/dirNag) + Platform. ALL required. | 0 |
| 9 | **A★ (Alpha Strike)** | First signal of session + Ping Pong bull + (GS or RVOL1x) + PBJ + expanded FAUNA. | 0 |
| 12 | **OD (Opening Drive)** | Session bar ≤ max bars + FVG + displacement + PUP + PBJ. ALL required. | -1 |
| 13 | **GOLF** | 3-bar sequence: bar[2]=FAUNA+PUP, bar[1]=FAUNA+PUP+DISP, bar[0]=DISP confirmation. | -1 |
| 27 | **CO** | HV+D + PBJ + (Unified Combo OR FVG Combo Set). | -1 |

### Tier B (Battalion — strong multi-axis signals)
| # | Name | Condition | Offset |
|---|------|-----------|--------|
| 4 | **FLOOR** | Ping Pong bull + PBJ + directional RVOL + qualifier gate. | 0 |
| 5 | **2F (2nd Floor)** | Ping Pong bull + PB (not PBJ) + directional RVOL + qualifier gate. | 0 |
| 10 | **ΩA (Omega-A)** | Boom Hunter omega + high-confidence cosignal. NOT MOAB/bear disp. | 0 |
| 11 | **FOX (Foxtrot)** | 4 consecutive FAUNA-confirmed bullish bars + (HV+D+PBJ OR qualifier). | 0 |
| 22 | **NPM+** | Napalm + ((PBJ + (UC or HW or WBUSH)) OR WBUSH alone). | -1 |

### Tier U (Unified — streak-based qualification)
| # | Name | Condition | Offset |
|---|------|-----------|--------|
| 6 | **UUUU** | 4+ consecutive qualified U bars (≥4 distinct qualifiers from {PBJ,DISP,FAUNA,SAAB,RVOL1x,GS}). | 0 |
| 7 | **UUU** | 3 consecutive qualified U bars (≥3 distinct qualifiers). | 0 |
| 8 | **UU** | 2 consecutive qualified U bars (≥2 distinct qualifiers) + gate. | 0 |
| 31 | **UU+UC** | Any UU family + Unified Combo on same candle. | -1 |
| 36 | **UU+HVD** | Any UU family + HV+D + PBJ. | -1 |
| 37 | **UU+NPM** | Any UU family + Napalm on same window. | -1 |
| 38 | **FLR+UU** | Floor or 2F + any UU family. | 0 |

### Tier N (Napalm — TNT zone displacement combos)
| # | Name | Condition | Offset |
|---|------|-----------|--------|
| 23 | **NPM12** | Napalm + qualifier Set 1 OR Set 2. | -1 |
| 24 | **NPM3** | Napalm + qualifier Set 3 (fires only when NPM12 does NOT). | -1 |
| 25 | **B2BNPM** | Back-to-back Napalm (consolidated). | -1 |
| 26 | **NPM+TNT** | Napalm + TNT on same candle. | -1 |
| 33 | **FLR+NPM** | Floor + Napalm on same candle. | -1 |
| 34 | **NPM+PBJ+PUP** | Napalm + PBJ + PUP without Unified Combo. | -1 |
| 40 | **NPM+UC** | Napalm + Unified Combo WITHOUT PBJ. | -1 |

### Tier H (HV+D — high volume displacement)
| # | Name | Condition | Offset |
|---|------|-----------|--------|
| 28 | **HVD+PBJ** | HV+D + PBJ on same candle. Excludes CO. | -1 |
| 29 | **B2BHVD+PBJ** | Consecutive HV+D + PBJ on either bar. | -1 |
| 30 | **B2BHVD** | Consecutive HV+D without PBJ. | -1 |
| 35 | **NAG+** | Nagasaki + any bullish signal. | 0 |

### Tier W (WBUSH — Heavy Pentagon classification)
| # | Name | Condition | Offset |
|---|------|-----------|--------|
| 41 | **WBUSH+ANY Bull** | Any of 5 Heavy Combos (Yin-Yang, Nagasaki, Nagasaki Vol, Trident, Neutral Heavy x2) firing bullish. | 0 |
| 42 | **WBUSH+ANY Bear** | Mirror — any of 5 Heavy Combos firing bearish. | 0 |
| 43 | **WBUSH Neutral** | Any of 5 Heavy Combos hitting neutral classification. | 0 |

### Tier F (Foster/Exhaustion — multi-bar candle patterns)
| # | Name | Condition | Offset |
|---|------|-----------|--------|
| 14 | **PBJ+F2/E3** | PBJ + Foster Pair or Exhaustion Triple. | 0 |
| 15 | **PBJ+CL** | PBJ + full FAUNA Cluster. | 0 |
| 16 | **F2CL→E3** | Sequential Foster Pair + Cluster then Exhaustion Triple. | 0 |
| 17 | **E3⅔PP** | Exhaustion Triple where 2 of 3 bars are PUP. | 0 |
| 18 | **F2×2D** | Foster Pair on consecutive trading sessions. | 0 |
| 19 | **E3×2D** | Exhaustion Triple on consecutive sessions. | 0 |
| 20 | **F2E3seq** | Foster Pair one session then Exhaustion Triple next. | 0 |
| 21 | **CL×2D** | FAUNA Cluster on consecutive sessions. | 0 |
| 39 | **FOS+PUP+1x** | Foster + PUP + (RVOL1x or Napalm consolidated). | 0 |

## Key Definitions

- **SUPER** = Unified Combo + Napalm consolidated
- **SDUPER (SD!)** = SUPER + PUP (the triple)
- **GOLF** = 3-bar displacement waterfall with FAUNA+PUP confirmation
- **WBUSH** = Heavy Pentagon's 5 Heavy Combo families OR'd into bull/bear/neutral
- **UU/UUU/UUUU** = Consecutive bars meeting ≥2/3/4 distinct qualifier types
- **GRAIL** = Maximum confluence: Napalm + PBJ + PUP + Unified Combo (the holy grail)

## VOB Relationship

SQUARIFY signals are the orchestra members. Each one detects a specific market
microstructure event. When multiple SQUARIFY signals fire simultaneously inside
a VOB zone, it's the confluence that produces the home run.

**The hierarchy for VOB-embedded signals:**
1. GRAIL (#32) — if this fires inside a stacked VOB, it's the absolute peak confluence
2. SD! (#1) / SUPER (#2) — Unified Combo + Napalm inside VOB
3. UC NAGASAKI (#45) — All-time-high volume + Unified Combo inside VOB
4. GOLF (#13) — 3-bar displacement waterfall inside VOB
5. Alpha Strike (#9) — First signal of session at VOB support

### Links
- [[vob-indicator]] — the zones these signals fire inside
- [[b2b-pup-indicator]] — shares engines, B2B PUP is a subset
- [[tnt-od-indicator]] — TNT/Napalm engine shared
- [[heavy-combo-toggles]] — WBUSH signals sourced from here
