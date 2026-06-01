# TNT OD — TNT Opening Drive (v3)

Source: nishpa800/indicators · tnt-od/versions/TNT_Opening_Drive_OD_v3_2026-05-04.pine
Lines: 1,803 · Pine Script v5 · Overlay indicator

## What It Does

Detects extreme anomaly events built on the TNT engine — a three-engine
confluence system (VOB + ANISH swing structure + FLUX order blocks) — and
combines them with displacement, Napalm zone-piercing, PBJ supertrend
reversals, RVOL streaks, density clustering, and WBUSH Heavy Combo
classifications. Designed for Opening Drive scenarios where the first bars
of a session produce cascade-style signals. This is the PRIMARY alert
indicator — it fires when multiple independent systems agree that
something significant is happening right now.

## How It Works (the physical measurement)

### Three-Engine Confluence (TNT 1.0)

1. **Engine 1 — VOB:** EMA crossover (fast = Sensitivity, slow = Sensitivity + 13)
   identifies structural zones. Bullish crossover finds lowest bar in lookback,
   bearish crossunder finds highest bar. Zone defined by origin bar range.
2. **Engine 2 — ANISH:** Swing high/low detection (pivot length = Swing Length).
   When price crosses a swing point, the last opposing-color candle before the
   swing becomes the order block. Consecutive overlapping OBs confirm structure.
3. **Engine 3 — FLUX:** Independent swing detection using candle body extremes.
   OB must fit within ATR(200) x 3.5 bounds. Pullback into FLUX OB = FLUX signal.

TNT fires when: all three engines confirm within a temporal window (2 x EMA_SLOW
bars), the VOB and ANISH zones overlap in price, volume exceeds median threshold,
EMA slope aligns with direction, and RSI is not extreme.

### Zone Management

- TNT zones persist until invalidated (price closes beyond boundary)
- Up to 30 zones tracked for Napalm/Charge/Return scanning
- Charge levels track displacement through opposing zones
- Super TNT (2.0) fires when 2+ consecutive events accumulate

### Signal Taxonomy

Signals are organized into a strict tier system:

- **Tier 1:** Multi-axis confluence already built in. Fires as-is.
- **Tier 2:** Hard-gated — NEVER fires without a USE V5 enrichment co-signal
  (RVOL1x, GrandSlam, PUP, CS1, FAUNA, WMD, HV1000, or DYNAMITE).
- **Density:** Rolling temporal window — X visual events within Y bars.
- **UU/UUU/UUUU + TNT ANY:** Consecutive RVOL streak with path qualification
  overlapping any TNT OD detection within the streak window.
- **WBUSH:** Heavy Combo state (from Heavy Combo Toggles / HEAVY PENTAGON)
  combined with any TNT OD detection.

### Offset Rules (Verification Protocol v3.2)

- **Offset -1:** Any signal whose detection chain touches displacement+FVG
  (Napalm, CATALYST, DYNAMITE, Density, UU+TNT). Visual anchors to bar[1].
- **Offset 0:** Signals without displacement+FVG in chain (TNT raw, CONT,
  FUSE, PBJ+TNT, IGNITE TNT+CONT).

## Detection Plots (42 total)

### Tier 1 — Multi-Axis Confluence (18 plots)

| Plot | Name | Condition | Offset | What It Detects |
|------|------|-----------|--------|-----------------|
| 1 | B2B Napalm Bull | Napalm on bar[0] AND Napalm on bar[1] (consecutive displacement through opposing TNT zones) | -1 | Serial displacement through TNT zones — two-bar confirmation |
| 2 | B2B Napalm Bear | Mirror of above, bearish | -1 | Serial bearish displacement |
| 3 | RC NPM+TNT Bull | Napalm AND TNT fire on same visual bar | -1 | Displacement event coincides with structural confluence — rare |
| 4 | RC NPM+TNT Bear | Mirror, bearish | -1 | Bearish displacement + structural confluence |
| 5 | FUSE Bull | Sequential NPM -> TNT -> CONT within proximity window | 0 | Escalating event cascade in tight temporal cluster |
| 6 | FUSE Bear | Mirror, bearish | 0 | Bearish cascade |
| 7 | CATALYST Bull | Napalm + CS1 (FVG Combo) on same visual bar | -1 | Displacement backed by FVG clustering or HV-FVG structure |
| 8 | CATALYST Bear | Mirror, bearish | -1 | Bearish displacement + FVG structure |
| 9 | PBJ+NPM Bull | PBJ supertrend reversal + Napalm on same visual bar | -1 | Supertrend reversal coincides with zone displacement |
| 10 | PBJ+NPM Bear | Mirror, bearish | -1 | Bearish reversal + displacement |
| 11 | PBJ+TNT Bull | PBJ supertrend reversal + TNT on same visual bar | 0 | Supertrend reversal coincides with structural breakout |
| 12 | PBJ+TNT Bear | Mirror, bearish | 0 | Bearish reversal + breakout |
| 13 | IGNITE TNT+CONT Bull | TNT + Continuous on same visual bar | 0 | Structural breakout that is also part of rapid-fire cluster |
| 14 | IGNITE TNT+CONT Bear | Mirror, bearish | 0 | Bearish breakout + cluster |
| 15 | IGNITE NPM+CONT Bull | Napalm + Continuous on same visual bar | -1 | Displacement event within rapid-fire cluster |
| 16 | IGNITE NPM+CONT Bear | Mirror, bearish | -1 | Bearish displacement + cluster |
| 17 | DYNAMITE Bull | B2B displacement (bar[1]+bar[2] both exceed stdev range, same bullish direction) + FAUNA on both + bar[0] confirms bullish FVG | -1 | Consecutive extreme-range bars with candle anatomy confirmation |
| 18 | DYNAMITE Bear | Mirror, bearish | -1 | Bearish consecutive displacement |

### Tier 2 — Enrichment-Gated (12 plots)

| Plot | Name | Condition | Offset | What It Detects |
|------|------|-----------|--------|-----------------|
| 19 | TNT Enriched Bull | Raw TNT + enrichment co-signal on same bar | 0 | Structural breakout with volume/pattern confirmation |
| 20 | TNT Enriched Bear | Mirror, bearish | 0 | Bearish breakout + enrichment |
| 21 | NPM Enriched Bull | Raw Napalm + enrichment on visual bar[1] | -1 | Zone displacement with volume/pattern confirmation |
| 22 | NPM Enriched Bear | Mirror, bearish | -1 | Bearish displacement + enrichment |
| 23 | CONT Enriched Bull | Raw Continuous + enrichment on same bar | 0 | Rapid-fire cluster with confirmation |
| 24 | CONT Enriched Bear | Mirror, bearish | 0 | Bearish cluster + enrichment |
| 25 | RC TNT+RET Enriched Bull | TNT + Return-to-TNT + enrichment on same bar | 0 | Breakout + zone retest + confirmation |
| 26 | RC TNT+RET Enriched Bear | Mirror, bearish | 0 | Bearish breakout + retest |
| 27 | RC RET+NPM Enriched Bull | Return + Napalm on same visual bar + enrichment | -1 | Zone retest + displacement + confirmation |
| 28 | RC RET+NPM Enriched Bear | Mirror, bearish | -1 | Bearish retest + displacement |
| 29 | PBJ+RET Enriched Bull | PBJ + Return-to-TNT + enrichment on same bar | 0 | Supertrend reversal at zone retest + confirmation |
| 30 | PBJ+RET Enriched Bear | Mirror, bearish | 0 | Bearish reversal + retest |

### Density Signals (6 plots)

| Plot | Name | Condition | Offset | What It Detects |
|------|------|-----------|--------|-----------------|
| 31 | Density 1 Bull | 2 visual bull events within 2 bars (default) | -1 | Tight clustering of bullish events |
| 32 | Density 1 Bear | Mirror, bearish | -1 | Tight bearish clustering |
| 33 | Density 2 Bull | 3 visual bull events within 3 bars (default) | -1 | Stricter temporal density |
| 34 | Density 2 Bear | Mirror, bearish | -1 | Stricter bearish density |
| 35 | Density 3 Bull | 2 visual bull events within 6 bars (default) | -1 | Sparse but temporally clustered events |
| 36 | Density 3 Bear | Mirror, bearish | -1 | Sparse bearish clustering |

### UU/UUU/UUUU + TNT ANY (6 plots)

| Plot | Name | Condition | Offset | What It Detects |
|------|------|-----------|--------|-----------------|
| 37 | UU+TNT ANY Bull | 2-bar RVOL streak (qualified via paths pA-pG) + any TNTOD bull detection in window | -1 | Short consecutive RVOL streak overlapping structural event |
| 38 | UU+TNT ANY Bear | Mirror, bearish | -1 | Short bearish streak + event |
| 39 | UUU+TNT ANY Bull | 3-bar RVOL streak (pG requires 3+ distinct qualifiers) + any TNTOD bull detection | -1 | Medium streak + structural event |
| 40 | UUU+TNT ANY Bear | Mirror, bearish | -1 | Medium bearish streak + event |
| 41 | UUUU+TNT ANY Bull | 4+ bar RVOL streak (pG requires 4+ qualifiers) + any TNTOD bull detection | -1 | Extended streak + structural event |
| 42 | UUUU+TNT ANY Bear | Mirror, bearish | -1 | Extended bearish streak + event |

### WBUSH (3 plots — v2 addition)

These are NOT counted in the 42 plotshapes above; they use the same plotshape mechanism.

| Plot | Name | Condition | Offset | What It Detects |
|------|------|-----------|--------|-----------------|
| W1 | WBUSH+TNTOD ANY Bull | Any of 5 Heavy Combo Bull classifications AND any TNTOD bull plot fired | 0 | Heavy volume combo confluence with TNT OD bull signal |
| W2 | WBUSH+TNTOD ANY Bear | Any of 5 Heavy Combo Bear classifications AND any TNTOD bear plot fired | 0 | Heavy volume combo confluence with TNT OD bear signal |
| W3 | WBUSH Neutral | Any of 5 Heavy Combo Neutral classifications (standalone, no TNTOD pairing required) | 0 | Extreme volume event without directional displacement |

## Enrichment Co-Signals (Tier 2 gate)

Tier 2 signals require at least ONE of these to be present on the plot bar:

| Co-Signal | Description |
|-----------|-------------|
| RVOL 1x | Normalized price spike in 1x-to-GrandSlam range |
| Grand Slam | Normalized price spike above Grand Slam threshold |
| PUP | Pocket Pivot Up (>3% price rise + volume > highest red volume) |
| CS1 | FVG Combo (consecutive or HV-backed fair value gaps) |
| FAUNA | Candle anatomy qualifier (Momentum Bar, Range Expansion, etc.) |
| WMD | Any volume ratio rank (Pentagon, WTC, Hiroshima, Nagasaki) |
| HV1000 | Volume is highest in 1000-bar lookback |
| DYNAMITE | B2B displacement + FAUNA on both bars |

## UU Path Qualification System

U-streaks qualify through one of seven paths (OR logic):

| Path | Requirement |
|------|-------------|
| pA | First bar of day present in streak + PBJ on at least one bar |
| pB | ALL bars in streak have displacement |
| pC | ALL bars have SAAB/RVOL + displacement or FAUNA |
| pD | (Intentionally skipped — TNT OD has no HV+D engine) |
| pE | Displacement/FAUNA on one bar without PBJ AND PBJ on another without disp/fauna |
| pF | UUUU only — (FAUNA or displacement) + PBJ present anywhere |
| pG | (v2 new) Count distinct qualifier types {PBJ, DISP, FAUNA, SAAB, RVOL1x, GrandSlam} in streak; need k >= streak size (UU=2, UUU=3, UUUU=4) |

## WBUSH Integration

WBUSH ports the 5 Heavy Combo families from [[heavy-combo-toggles-indicator]]:

| Heavy Combo Family | Base Condition |
|-------------------|----------------|
| Heavy Yin-Yang | Group A (RVOL1x or GrandSlam) + Group B (Pentagon or WTC or Hiroshima) |
| Heavy Nagasaki | Nagasaki + Group A |
| Heavy Nagasaki Vol | Nagasaki + Group B |
| Heavy Trident | Nagasaki + Group A + Group B |
| Neutral Heavy x2 | Two or more Group B signals simultaneously |

Each family produces Bull/Bear/Neutral based on displacement direction.
WBUSH-bull or WBUSH-bear = any of 5 families in that direction.

## Input Parameters

### Master Controls

| Parameter | Default | What It Controls |
|-----------|---------|-----------------|
| First Bar Only Alerts | true | Requires first bar of session + any HV rank on plot bar |
| Aggregate Alerts | true | ON: one combined alert per bar; OFF: individual alerts |

### Engine Parameters

| Parameter | Default | What It Controls |
|-----------|---------|-----------------|
| Sensitivity | 100 | EMA length for VOB zone detection (fast EMA = this, slow = this + 13) |
| Swing Length | 10 | Bars for ANISH swing high/low pivot detection |
| Range Type | Open to Close | Whether displacement measures body range or full range |
| Disp Std Dev Length | 100 | Lookback for displacement standard deviation calculation |
| Disp Std Dev Mult | 5 | How many sigma constitutes displacement |
| Return to TNT % | 100.0 | How deep price must retrace into TNT zone for Return signal |
| Return to TNT 2.0 % | 50.0 | Return depth for Super zones |
| Sudden Change Max Bar Distance | 3 | Max bars between events for Continuous/FUSE signals |

### DYNAMITE Parameters

| Parameter | Default | What It Controls |
|-----------|---------|-----------------|
| Displacement Std Dev Multiplier | 5.0 | Both consecutive bars must exceed stdev(100) x this |

### Density Parameters

| Parameter | Default | What It Controls |
|-----------|---------|-----------------|
| Density 1 Events (X) | 2 | Events required in window |
| Density 1 Bars (Y) | 2 | Window size in visual bars |
| Density 2 Events (X) | 3 | Stricter event count |
| Density 2 Bars (Y) | 3 | Stricter window |
| Density 3 Events (X) | 2 | Sparse event count |
| Density 3 Bars (Y) | 6 | Wider window for sparse clustering |

### Zone Limits

| Parameter | Default | What It Controls |
|-----------|---------|-----------------|
| Max TNT 1.0 Zones | 30 | Active TNT zones tracked for Napalm/Charge/Return scans |
| Max TNT 2.0 Zones | 30 | Active Super zones tracked |

### Tier 1/2 Enable Checkboxes

All 18 Tier 1 plots have individual bull/bear enable toggles (all default true).
All 12 Tier 2 plots have individual bull/bear enable toggles (all default true).
All 6 Density plots have individual bull/bear enable toggles (all default true).
All 6 UU plots have individual bull/bear enable toggles (all default true).
All 3 WBUSH plots have individual enable toggles (all default true).

### Nagasaki Alert

| Parameter | Default | What It Controls |
|-----------|---------|-----------------|
| Fire NAGASAKI alert | false | Standalone alert for all-time-high volume bars (floods alerts when ON) |

## Alert Format

```
DIRECTION | FIRST_STATUS | NAME
```

- DIRECTION: BULL or BEAR
- FIRST_STATUS: FIRST !!! (first bar, gap <= bar range), FIRST XXX (first bar,
  gap > bar range), NOT !!! (not first bar of session)
- NAME: Signal name (B2B NAPALM, RC NPM+TNT, FUSE, CATALYST, etc.)

When Aggregate Alerts is ON, all signals on one bar are joined with " + ".

## Relationship to OIA (Opening Imbalance Acceleration)

TNT OD's Opening Drive signals (particularly when First Bar Only is enabled)
detect the same phenomenon that OIA measures from the NOI side. When the NYSE
Opening Imbalance Acceleration signal fires in our NOI system and TNT OD's
first-bar detections fire simultaneously, this represents the highest-conviction
opening setup: the institutional order flow (OIA) confirms the structural
price pattern (TNT OD).

## Relationship to VOB Thesis

TNT OD answers: "Is something happening RIGHT NOW at or near a VOB zone?" The
three-engine confluence ensures structural agreement, while displacement/Napalm
confirms that price is actively piercing or bouncing from zones. When TNT OD
fires inside a stacked VOB zone (from the VOB indicator), it validates the
zone's tensile strength in real time.

**Highest-conviction TNT OD signals for VOB validation:**
- B2B Napalm — consecutive displacement through zones = maximum force
- CATALYST — displacement + FVG structural confluence = VOB zone is generating gaps
- DYNAMITE — consecutive extreme-range bars = explosive breakout from zone
- WBUSH+TNTOD ANY — Heavy Combo volume anomaly + TNT structure = institutional participation

### Links
- [[vob-indicator]] — the zones TNT OD detects events within
- [[b2b-pup-indicator]] — shares TNT/Napalm engine, PBJ engine, RVOL tiers
- [[heavy-combo-toggles-indicator]] — source of WBUSH classifications
- [[squarify-indicator]] — shares UU/UUU/UUUU path system, FAUNA, RVOL
- [[hvd-pbj-ppd-indicator]] — shares displacement and PBJ engines
- [[noi-thresholds]] — OIA signal from NOI system confirms TNT OD opening drive
