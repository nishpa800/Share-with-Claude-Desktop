# Heavy Combo Toggles — HCT (v1)

Source: nishpa800/indicators · heavy-combo-toggles/versions/HEAVY_COMBO_TOGGLES_v1.pine
Lines: 292 · Pine Script v5 · Overlay indicator

## What It Does

Aggregates 15 Heavy Combo sub-signals into 3 master detection plots: Bull,
Bear, and Neutral. Each master plot is an OR-gate across 5 Heavy Combo
families, with 15 individual eligibility checkboxes controlling which families
contribute. The underlying RVOL, Nagasaki, and displacement engines are lifted
verbatim from HEAVY PENTAGON. This is the VOLUME ANOMALY CLASSIFIER — it
answers "is this bar experiencing an extreme volume event, and in which
direction?"

## How It Works (the physical measurement)

### Three Pipelines (unchanged from HEAVY PENTAGON)

#### Pipeline 1: RVOL Bull/Bear (Standard — Normalized Price Spike)

Measures price spike relative to recent average, normalized by volume:
1. `normalizedPrice = |close - open| / SMA(|close - open|, 30)[1]`
2. `normalizedVolume = volume / SMA(volume, 30)[1]`
3. `diff = normalizedPrice - normalizedVolume`
4. Base bullish: close > open AND positive diff > SMA(positive diff, 20)
5. Base bearish: close < open AND same condition

Tiered classification by normalizedPrice thresholds (timeframe-adjusted):

| Tier | Direction | Condition |
|------|-----------|-----------|
| SAAB | Bullish | normalizedPrice in [saab_threshold, 1x_threshold) |
| Kratos | Bearish | Same range, bearish base |
| Bull RVOL 1x | Bullish | normalizedPrice in [1x_threshold, gs_threshold) |
| Bear RVOL 1x | Bearish | Same range, bearish base |
| Grand Slam | Bullish | normalizedPrice >= gs_threshold |
| MOAB | Bearish | normalizedPrice >= gs_threshold, bearish base |

Thresholds scale by timeframe (e.g., 1x = 38.0 at 10sec, 20.0 at 1min,
8.4 at 15min, 5.9 at 1hr, 1.8 at 1day).

#### Pipeline 2: RVOL Reg @ Time (Time-Regularized Volume Ratio)

Uses TradingView's `tv_ta.relativeVolume()` to compute current volume vs
historical average at the same time of day:

| Tier | Condition |
|------|-----------|
| Pentagon | relVolRatio in [1x_threshold, wtc_threshold] |
| WTC | relVolRatio in (wtc_threshold, hiroshima_threshold] |
| Hiroshima | relVolRatio > hiroshima_threshold |

Where: `wtc_threshold = 1x * 2.0`, `hiroshima_threshold = gs_threshold` (approx).

#### Pipeline 3: Nagasaki (All-Time High Volume)

Simple running maximum:
- If current confirmed bar volume > all prior maximum volume ever seen on
  this ticker/timeframe, Nagasaki = true
- Running max updates on every bar

### Displacement Engine (Building Block)

Not a standalone pipeline — used as a direction classifier for all combos:
1. bar[1] range must exceed `strength (6.0) * stdev(bar ranges, lookback 100)`
2. bar[0] must confirm with FVG (bullish: low > high[2]; bearish: high < low[2])
3. `dispBull` = displacement candle was bullish (close[1] > open[1]) + bullish FVG
4. `dispBear` = displacement candle was bearish + bearish FVG
5. `noDisp` = neither dispBull nor dispBear (used for Neutral classification)

### The 15 Sub-Signals (5 Families x 3 Directions)

Two classification groups feed the combo logic:

- **Group A (Pipeline 1, directional):** Bull RVOL 1x OR Grand Slam (bull side);
  Bear RVOL 1x OR MOAB (bear side). Excludes SAAB/Kratos.
- **Group B (Pipeline 2, neutral heavy):** Pentagon OR WTC OR Hiroshima.

| Family | Base Condition | What It Requires |
|--------|---------------|-----------------|
| Heavy Yin-Yang | Group A (either side) AND Group B | Directional price spike + time-regularized volume spike |
| Heavy Nagasaki | Nagasaki AND Group A (either side) | All-time volume + directional price spike |
| Heavy Nagasaki Vol | Nagasaki AND Group B | All-time volume + time-regularized volume spike |
| Heavy Trident | Nagasaki AND Group A AND Group B | All three pipelines firing — rarest, strongest |
| Neutral Heavy x2 | Two or more Group B signals simultaneously | Multiple time-regularized volume tiers (e.g., Pentagon + WTC) |

Each base condition is classified into Bull/Bear/Neutral by displacement:

| Direction | Classifier |
|-----------|------------|
| Bull | Base condition AND dispBull (bullish displacement + FVG) |
| Bear | Base condition AND dispBear (bearish displacement + FVG) |
| Neutral | Base condition AND noDisp (no displacement either direction) |

This produces 15 booleans (5 families x 3 directions).

### The 3 Master Plots (OR-Gates)

| Master Plot | Logic |
|-------------|-------|
| S1: Heavy Combo Bull | OR of all 5 Bull sub-signals (gated by eligibility checkboxes) |
| S2: Heavy Combo Bear | OR of all 5 Bear sub-signals (gated by eligibility checkboxes) |
| S3: Heavy Combo Neutral | OR of all 5 Neutral sub-signals (gated by eligibility checkboxes) |

## Detection Plots (3 total)

| Plot | Name | Condition | Offset | Visual | What It Detects |
|------|------|-----------|--------|--------|-----------------|
| S1 | Heavy Combo Bull | Any eligible bull combo family fires (displacement + FVG confirmed bullish) | -1 | Lime circle, bottom, text "HC triangle-up" | Bullish volume anomaly with displacement confirmation |
| S2 | Heavy Combo Bear | Any eligible bear combo family fires (displacement + FVG confirmed bearish) | -1 | Red circle, top, text "HC triangle-down" | Bearish volume anomaly with displacement confirmation |
| S3 | Heavy Combo Neutral | Any eligible neutral combo family fires (volume anomaly WITHOUT displacement) | 0 | White circle, top, text "HC dash" | Extreme volume event with no directional displacement |

### Offset Rules

- **Bull and Bear (S1, S2):** AND-gate with dispBull/dispBear, which has
  displacement+FVG in chain. Per Verification Protocol Rule 2, offset = -1.
  Visual anchors on bar[1] (the displacement candle).
- **Neutral (S3):** AND-gate with noDisp (absence of displacement). No
  displacement candle to mark. Constituent signals fire on bar[0]. Offset = 0.

## The 15 Sub-Signals Detail

### Heavy Yin-Yang (Pipeline 1 + Pipeline 2)

| Sub-Signal | Condition |
|------------|-----------|
| Heavy Yin-Yang Bull | (Bull RVOL 1x OR Grand Slam OR Bear RVOL 1x OR MOAB) AND (Pentagon OR WTC OR Hiroshima) AND dispBull |
| Heavy Yin-Yang Bear | Same base AND dispBear |
| Heavy Yin-Yang Neutral | Same base AND noDisp |

### Heavy Nagasaki (Pipeline 3 + Pipeline 1)

| Sub-Signal | Condition |
|------------|-----------|
| Heavy Nagasaki Bull | Nagasaki AND (Bull RVOL 1x OR Grand Slam OR Bear RVOL 1x OR MOAB) AND dispBull |
| Heavy Nagasaki Bear | Same base AND dispBear |
| Heavy Nagasaki Neutral | Same base AND noDisp |

### Heavy Nagasaki Vol (Pipeline 3 + Pipeline 2)

| Sub-Signal | Condition |
|------------|-----------|
| Heavy Nagasaki Vol Bull | Nagasaki AND (Pentagon OR WTC OR Hiroshima) AND dispBull |
| Heavy Nagasaki Vol Bear | Same base AND dispBear |
| Heavy Nagasaki Vol Neutral | Same base AND noDisp |

### Heavy Trident (Pipeline 1 + Pipeline 2 + Pipeline 3)

| Sub-Signal | Condition |
|------------|-----------|
| Heavy Trident Bull | Nagasaki AND (Group A) AND (Group B) AND dispBull |
| Heavy Trident Bear | Same base AND dispBear |
| Heavy Trident Neutral | Same base AND noDisp |

### Neutral Heavy x2 (Pipeline 2 x 2)

| Sub-Signal | Condition |
|------------|-----------|
| Neutral Heavy x2 Bull | (Pentagon AND WTC) OR (Pentagon AND Hiroshima) OR (WTC AND Hiroshima) AND dispBull |
| Neutral Heavy x2 Bear | Same base AND dispBear |
| Neutral Heavy x2 Neutral | Same base AND noDisp |

## Input Parameters

### Heavy Combo Eligibility (15 checkboxes)

| Parameter | Default | What It Controls |
|-----------|---------|-----------------|
| Heavy Yin-Yang Bull | true | Include Heavy Yin-Yang in master Bull OR-gate |
| Heavy Yin-Yang Bear | true | Include in master Bear OR-gate |
| Heavy Yin-Yang Neutral | true | Include in master Neutral OR-gate |
| Heavy Nagasaki Bull | true | Include Heavy Nagasaki in Bull |
| Heavy Nagasaki Bear | true | Include in Bear |
| Heavy Nagasaki Neutral | true | Include in Neutral |
| Heavy Nagasaki Vol Bull | true | Include Heavy Nagasaki Vol in Bull |
| Heavy Nagasaki Vol Bear | true | Include in Bear |
| Heavy Nagasaki Vol Neutral | true | Include in Neutral |
| Heavy Trident Bull | true | Include Heavy Trident in Bull |
| Heavy Trident Bear | true | Include in Bear |
| Heavy Trident Neutral | true | Include in Neutral |
| Neutral Heavy x2 Bull | true | Include Neutral Heavy x2 in Bull |
| Neutral Heavy x2 Bear | true | Include in Bear |
| Neutral Heavy x2 Neutral | true | Include in Neutral |

### Pipeline 1 — RVOL Bull/Bear

| Parameter | Default | What It Controls |
|-----------|---------|-----------------|
| Lookback Length | 30 | SMA lookback for normalizing price/volume spikes |
| SMA Length | 20 | SMA of positive diff for threshold |

### Pipeline 2 — RVOL Reg @ Time

| Parameter | Default | What It Controls |
|-----------|---------|-----------------|
| Anchor Timeframe | (chart) | Timeframe for historical volume comparison |
| Length | 30 | Number of historical bars for average |
| Calculation Mode | Cumulative | Cumulative vs regular volume aggregation |
| Adjust Unconfirmed | true | Adjust for partially-filled current bar |

### Displacement Engine

| Parameter | Default | What It Controls |
|-----------|---------|-----------------|
| Strength (sigma multiplier) | 6.0 | Bar[1] range must exceed this many stdev |
| Lookback Length | 100 | Bars for bar-range stdev calculation |
| FVG Threshold % | 2.0 | Manual FVG minimum gap size |
| Auto FVG Threshold | true | Auto-calculate from cumulative average range |

## How WBUSH in Other Indicators References This

The WBUSH system in [[tnt-od-indicator]] and other indicators ports the exact
same 5 Heavy Combo families and 15 sub-signals defined here. They use their
own instances of the RVOL/Nagasaki/Displacement pipelines (not a cross-indicator
reference), but the classification logic is identical:

- **WBUSH-bull** = any of 5 Bull sub-signals fired
- **WBUSH-bear** = any of 5 Bear sub-signals fired
- **WBUSH-neutral** = any of 5 Neutral sub-signals fired

TNT OD then AND-gates WBUSH with its own detection plots:
- WBUSH+TNTOD ANY Bull = WBUSH-bull AND any TNTOD bull plot fired
- WBUSH+TNTOD ANY Bear = WBUSH-bear AND any TNTOD bear plot fired
- WBUSH Neutral = WBUSH-neutral (standalone, no TNTOD pairing)

This means Heavy Combo Toggles is the REFERENCE IMPLEMENTATION. When tuning
RVOL thresholds or displacement sensitivity, changes here should be mirrored
in all WBUSH ports.

## Relationship to VOB Thesis

Heavy Combo Toggles classifies volume anomalies into directional categories.
For the VOB thesis, the key insight is:

- **Heavy Combo Bull at VOB support:** Extreme volume anomaly with bullish
  displacement at a VOB zone = institutional buying is defending the zone
- **Heavy Trident (rarest):** All three pipelines firing simultaneously at a
  VOB zone = the strongest possible volume backing
- **Neutral signals at VOB zones:** Extreme volume WITHOUT displacement means
  the zone is absorbing pressure without breaking — this is what "unbreakable"
  looks like before the breakout happens
- **Nagasaki volume at VOB creation:** If a VOB zone was created on a Nagasaki
  bar (all-time high volume), the zone has maximum volume conviction

### Links
- [[vob-indicator]] — VOB zones where Heavy Combo volume classifications add conviction
- [[tnt-od-indicator]] — WBUSH system ports these 15 sub-signals for TNT OD confluence
- [[b2b-pup-indicator]] — Engine E (RVOL Tiers) uses same normalized price spike classification
- [[hvd-pbj-ppd-indicator]] — Pipeline C shares RVOL, FAUNA, and Nagasaki detection
- [[squarify-indicator]] — shares RVOL tier definitions
