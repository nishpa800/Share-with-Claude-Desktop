# Input Parameter Sensitivity Map

## Purpose

Identify which input parameters have the HIGHEST sensitivity — meaning a small
change produces a big change in signal output. These are the parameters the
autoresearch loop should tweak FIRST for maximum impact.

## Sensitivity Classification

**HIGH SENSITIVITY (change ±10% → ≥20% change in signal frequency or quality):**
These are the levers that move the system. Tweak these first.

**MEDIUM SENSITIVITY (change ±10% → 5-20% change):**
Worth optimizing but lower priority.

**LOW SENSITIVITY (change ±10% → <5% change):**
Leave at defaults unless everything else is optimized.

## VOB Indicator Parameters

| Parameter | Default | Sensitivity | Why |
|-----------|---------|-------------|-----|
| **Sensitivity A** | 850 | **HIGH** | Controls the strongest tier — changes here shift which zones exist at the most important level |
| **Sensitivity B** | 750 | **HIGH** | Second-strongest tier — directly affects stacking count |
| Sensitivity C | 650 | MEDIUM | Mid-tier — moderate impact on stacking |
| Sensitivity D | 550 | MEDIUM | Mid-tier |
| Sensitivity E | 450 | LOW | Lower tier — many zones, individually weak |
| Sensitivity F | 350 | LOW | Lowest tier — most zones but least meaningful |
| **Super Mult** | 1.0 | **HIGH** | T3 threshold — changing from 1.0 to 1.5 dramatically reduces T3 signal frequency but may improve quality |
| Cooldown Bars | 100 | MEDIUM | Affects signal density — lower = more signals, higher = fewer but less redundant |
| Stacking Threshold % | 2.0 | MEDIUM | Defines what "near price" means — wider = more stacking reported |
| Ladder Tolerance % | 0.3 | LOW | Fine-tuning of ladder strictness |
| Adjacent Bar Window | 25 | LOW | Rarely changes outcome materially |

**Recommended autoresearch sweeps for VOB:**
1. Sensitivity A: test 600, 700, 750, 800, 850, 900, 1000, 1200
2. Super Mult: test 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0
3. Sensitivity B: test ±100 from default

## B2B PUP Parameters

| Parameter | Default | Sensitivity | Why |
|-----------|---------|-------------|-----|
| **% Change (PUP)** | 3.0 | **HIGH** | Minimum price move for PUP — lower catches more but weaker signals |
| Lookback Days (PUP) | 10 | MEDIUM | Window for volume comparison |
| **Std Dev Multiplier (Displacement)** | 5.0 | **HIGH** | What counts as "displacement" — lower = more signals |
| Std Dev Length | 100 | LOW | Lookback for std dev calculation |
| **TNT Sensitivity** | 100 | **HIGH** | EMA length for TNT zone formation — directly affects zone positions |
| Sudden Change Max Bars | 3 | MEDIUM | CONT trigger window |
| Max TNT Zones | 30 | LOW | Scan depth for Napalm — 30 is generous |
| PBJ ATR Multiplier | 3.0 | MEDIUM | How far from PBJ MA price must be for entry signal |

**Recommended sweeps for B2B PUP:**
1. % Change: test 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0
2. Std Dev Multiplier: test 3.0, 4.0, 5.0, 6.0, 7.0
3. TNT Sensitivity: test 50, 75, 100, 125, 150, 200

## SQUARIFY Parameters

SQUARIFY shares all engines with B2B PUP — same parameters apply.
The unique SQUARIFY parameters are the 46 en_* toggles (on/off per signal).

**The most impactful SQUARIFY optimization:**
- Turn OFF low-PPV signals (determined by P2 standalone testing)
- This reduces noise and concentrates alerts on high-quality signals

## HVD-PBJ-PPD Parameters

| Parameter | Default | Sensitivity | Why |
|-----------|---------|-------------|-----|
| **HV+D Std Dev Multiplier** | 5.0 | **HIGH** | What counts as "high volume displacement" |
| HV+D Std Dev Length | 100 | LOW | Lookback |
| PBJ MA Period | 20 | MEDIUM | Affects PBJ entry level positions |
| PBJ ATR Period | 14 | LOW | Standard ATR |
| PBJ ATR Multiplier | 3.0 | MEDIUM | How far from MA for PBJ signal |
| PBJ Volume Multiplier | 0.1 | LOW | Volume filter for PBJ (very permissive at 0.1) |

## Proximity GZI HV Parameters

| Parameter | Default | Sensitivity | Why |
|-----------|---------|-------------|-----|
| **Threshold %** | 1.0 | **HIGH** | Minimum FVG size — lower catches more FVGs |
| Show Last | 15 | LOW | Display parameter only |
| Max Bar Distance (GZI) | 6 | MEDIUM | How close FVGs must be for overlap |

## Cross-Indicator Sensitivity Summary

### Top 10 Parameters to Sweep First (Highest Impact)

| Rank | Parameter | Indicator | Default | Test Range |
|------|-----------|-----------|---------|------------|
| 1 | Super Mult | VOB | 1.0 | 0.5 - 3.0 |
| 2 | Sensitivity A | VOB | 850 | 600 - 1200 |
| 3 | % Change (PUP) | B2B PUP | 3.0 | 1.5 - 5.0 |
| 4 | Std Dev Mult (Displacement) | B2B PUP / HVD | 5.0 | 3.0 - 7.0 |
| 5 | TNT Sensitivity | B2B PUP | 100 | 50 - 200 |
| 6 | Sensitivity B | VOB | 750 | 550 - 950 |
| 7 | PBJ ATR Multiplier | B2B PUP / HVD | 3.0 | 1.5 - 5.0 |
| 8 | Cooldown Bars | VOB | 100 | 25 - 200 |
| 9 | Threshold % (FVG) | Proximity GZI | 1.0 | 0.3 - 3.0 |
| 10 | Stacking Threshold % | VOB | 2.0 | 1.0 - 5.0 |

These 10 parameters × 5-8 values each = 50-80 experiments. One night's work.

### Links
- [[permutation-priority]] — test schedule
- [[confluence-scoring]] — weight optimization is separate from parameter optimization
- [[tensile-strength-model]] — Sensitivity A/B directly affect tensile
