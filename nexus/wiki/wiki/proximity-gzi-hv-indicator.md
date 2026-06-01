# Proximity GZI HV — Fair Value Gap Zone Intersection + High Volume FVG (v1)

Source: nishpa800/indicators · proximity-gzi-hv/versions/PROXIMITY_GZI_HV_v1.pine
Lines: 232 · Pine Script v5 · Overlay indicator

## What It Does

Detects Fair Value Gaps (FVGs) and produces two signal types on top of them:
GZI (Gap Zone Intersection) when same-polarity FVGs overlap in price within
a temporal proximity window, and HV (High Volume FVG) when an FVG forms on
a bar with milestone volume (highest in 63, 252, or 5000 bars). Draws FVG
zones as boxes, tracks mitigation, and plots unmitigated levels. This is the
STRUCTURAL GAP indicator — it maps where the market left unfilled gaps that
act as magnets or barriers.

## How It Works (the physical measurement)

### FVG Detection

A Fair Value Gap requires three bars:
- **Bullish FVG:** bar[0] low > bar[2] high AND bar[1] close > bar[2] high
  AND gap size exceeds threshold. Gap zone = [bar[2] high, bar[0] low].
- **Bearish FVG:** bar[0] high < bar[2] low AND bar[1] close < bar[2] low
  AND gap size exceeds threshold. Gap zone = [bar[0] high, bar[2] low].

Threshold modes:
- **Auto (default):** Cumulative average of (high-low)/low across all bars.
  This adapts to the ticker's historical volatility.
- **Manual:** Fixed percentage (default 1%).

Multi-timeframe: FVGs can be detected on a configurable timeframe (default =
chart timeframe) via request.security().

### GZI — Gap Zone Intersection (Signal 1)

Fires when a NEW FVG overlaps in PRICE with an EXISTING same-polarity FVG
that is within the temporal proximity window (Max Bar Distance).

Two overlap modes:
1. **Standard overlap:** The new FVG and existing FVG share price range
   (overlap_bottom < overlap_top)
2. **Adjacent HV:** Both the new AND existing FVGs have HV status, and they
   are merely touching (overlap_bottom <= overlap_top) — relaxed from strict
   overlap because two HV FVGs touching is significant enough

GZI detects FVG CLUSTERING — when the market produces multiple gaps in the
same direction at the same price in quick succession, it signals strong
one-directional pressure. The gaps reinforce each other.

### HV — High Volume FVG (Signal 2)

Fires when a new FVG forms and the formation bar (bar[1]) had milestone volume:
- Volume equals the highest in 5000 bars (all-time on most charts), OR
- Volume equals the highest in 252 bars (annual), OR
- Volume equals the highest in 63 bars (quarterly)

HV FVGs are structurally more important because the volume behind them makes
them harder to mitigate.

### Zone Lifecycle

1. **Creation:** FVG detected → box drawn from bar[0]-2 to bar[0]+480
2. **Tracking:** Stored in fvg_records array with max/min/polarity/bar index/HV status
3. **Mitigation:** Bullish FVG mitigated when close < zone min; bearish when
   close > zone max. Zone removed and optionally draws mitigation dashed line.
4. **Unmitigated levels:** Last N unmitigated zones draw horizontal lines at
   their key level (bullish = lower boundary, bearish = upper boundary)

## Detection Plots (4 total)

| Plot | Name | Condition | Offset | Visual | What It Detects |
|------|------|-----------|--------|--------|-----------------|
| 1 | Bullish GZI | New bullish FVG overlaps existing bullish FVG within proximity + price overlap | -1 | Green flag, top | Bullish gap clustering — multiple FVGs stacking in same price zone |
| 2 | Bearish GZI | New bearish FVG overlaps existing bearish FVG within proximity + price overlap | -1 | Red flag, top | Bearish gap clustering |
| 3 | Bullish HV | New bullish FVG on a bar with milestone volume (63/252/5000 highest) | -1 | Cyan flag, below bar | High-volume bullish gap — strong structural support |
| 4 | Bearish HV | New bearish FVG on a bar with milestone volume | -1 | Orange flag, below bar | High-volume bearish gap — strong structural resistance |

### Alert Conditions (10 total)

| Alert | Condition |
|-------|-----------|
| Bullish FVG | Any new bullish FVG detected |
| Bearish FVG | Any new bearish FVG detected |
| Bullish FVG Mitigation | Bullish FVG zone mitigated (price closed below) |
| Bearish FVG Mitigation | Bearish FVG zone mitigated (price closed above) |
| Bullish GZI | GZI signal fires bullish |
| Bearish GZI | GZI signal fires bearish |
| Any GZI | Either GZI direction |
| Bullish HV FVG | HV signal fires bullish |
| Bearish HV FVG | HV signal fires bearish |
| Any HV FVG | Either HV direction |

## Input Parameters

### FVG Detection

| Parameter | Default | What It Controls |
|-----------|---------|-----------------|
| Threshold % | 1.0 | Manual minimum gap size as % of price |
| Auto | true | Auto-calculate threshold from cumulative average range |
| Unmitigated Levels | 15 | How many unmitigated zones draw horizontal lines |
| Mitigation Levels | false | Draw dashed lines where mitigated zones were |
| Timeframe | (chart) | Multi-timeframe FVG detection |

### Style

| Parameter | Default | What It Controls |
|-----------|---------|-----------------|
| Bullish FVG | green (70% transparent) | Box color for bullish FVG zones |
| Bearish FVG | red (70% transparent) | Box color for bearish FVG zones |

### GZI Signal Settings

| Parameter | Default | What It Controls |
|-----------|---------|-----------------|
| Show GZI Signals | true | Enable/disable GZI detection |
| Max Bar Distance | 6 | Maximum bars between overlapping FVGs for GZI to fire |
| Bullish GZI Color | #00ff88 | Plot color |
| Bearish GZI Color | #ff0055 | Plot color |

### HV Signal Settings

| Parameter | Default | What It Controls |
|-----------|---------|-----------------|
| Show HV Signals | true | Enable/disable HV detection |
| Bullish HV Color | #00bfff | Plot color |
| Bearish HV Color | #ff6600 | Plot color |

### Hardcoded

| Parameter | Value | What It Controls |
|-----------|-------|-----------------|
| Box Extend | 480 bars | How far forward FVG boxes extend on chart |

## How FVGs Relate to VOB Zones

FVGs and VOBs measure different structural phenomena that reinforce each other:

- **VOB zones** form at EMA crossover events with accumulated volume — they
  represent PRICE MEMORY backed by volume consensus.
- **FVGs** form when price moves so fast that a three-bar gap appears — they
  represent PRICE INEFFICIENCY that the market wants to revisit.

When a GZI or HV signal fires AT THE SAME PRICE as an active VOB zone, it
means:
1. The VOB zone already has volume consensus
2. The FVG clustering (GZI) or extreme volume (HV) adds gap-based structural
   evidence
3. The zone becomes doubly reinforced — both volume memory AND gap inefficiency
   point to the same price

This is why the HVD-PBJ-PPD indicator's Engine 4 (GZ1/HV FVG) uses the same
FVG detection logic — it feeds GZI/HV signals into combo sets that combine
with displacement and RVOL.

### Specific VOB Interactions

- **Bullish GZI at VOB support:** Multiple bullish FVGs clustering at the VOB's
  lower boundary = strong upward pressure zone
- **HV FVG at VOB creation bar:** If the VOB zone was created on a bar that
  also triggered an HV FVG, the zone has double volume backing
- **Bearish GZI above stacked VOB:** Bearish gap clustering immediately above
  a bullish VOB stack = potential breakdown warning
- **Unmitigated FVG inside VOB zone:** An unfilled gap sitting inside a VOB
  zone acts as a price magnet, increasing the probability of revisit

## Relationship to VOB Thesis

Proximity GZI HV provides the STRUCTURAL GAP layer. VOBs are the volume
consensus layer, TNT is the momentum detection layer, and FVGs are the
inefficiency layer. When all three agree at the same price — a stacked VOB
zone contains unmitigated FVGs with GZI clustering, and TNT OD fires an
event — the zone has three independent reasons to hold.

### Links
- [[vob-indicator]] — VOB zones that FVGs reinforce when overlapping
- [[hvd-pbj-ppd-indicator]] — Pipeline C Engine 4 uses identical FVG/GZI logic
- [[b2b-pup-indicator]] — Engine C (Displacement) references FVG confirmation
- [[tnt-od-indicator]] — CS1 (FVG Combo) and CATALYST use FVG-based signals
- [[squarify-indicator]] — shares FVG detection patterns
