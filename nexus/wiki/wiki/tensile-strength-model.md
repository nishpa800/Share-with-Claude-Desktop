# Tensile Strength Model — What Makes a VOB Unbreakable

## The Equation

```
Tensile(ticker, t) = Σ(tier_weights × tier_active) × Vol_dominance × Ladder_bonus × Anti_fragility

Where:
  Tier_score = Σ w_i × active_i   for i ∈ {A, B, C, D, E, F}
    w_A = 6 (highest weight — slowest EMA, fewest zones, strongest)
    w_B = 5
    w_C = 4
    w_D = 3
    w_E = 2
    w_F = 1 (lowest weight — fastest EMA, most zones, weakest)
    active_i = 1 if tier i has an active zone within stacking_threshold of price, else 0

  Maximum tier_score = 6+5+4+3+2+1 = 21 (all tiers stacking)

  Vol_dominance = bull_pool / (bull_pool + bear_pool)
    Range: 0.0 (all bearish) to 1.0 (all bullish)
    For bullish VOB, want > 0.6. For T3 condition, dominant pool > opposing × super_mult.

  Ladder_bonus = 
    1.0  if no ladder detected
    1.5  if 3+ consecutive tiers form a ladder (ascending lows or descending highs)
    2.0  if full 6-tier ladder detected (Bull Ladder or Bear Ladder)
    2.5  if full ladder + gap (Ladder+Gap detection)

  Anti_fragility = 1.0 - Wrong_Way_penalty
    Wrong_Way_penalty = 0.3 if Wrong-Way 3 detected (structural degradation)
    Adjacent_penalty  = 0.15 if Adjacent Bull/Bear detected (indecision)
    Anti_fragility range: 0.55 (worst) to 1.0 (clean structure)

  Final Tensile range: 0 to ~52.5 (theoretical max with all tiers + ladder + no degradation)
```

## Tensile Strength Classification

| Score | Classification | Description | Action |
|-------|---------------|-------------|--------|
| 0-3 | **NONE** | No meaningful VOB support/resistance | Do not trade based on zone |
| 3-7 | **WEAK** | 1-2 low tiers stacking, low volume dominance | Caution — zone may break |
| 7-12 | **MODERATE** | 2-3 tiers stacking, decent volume dominance | Tradeable with other confirmation |
| 12-18 | **STRONG** | 3-4 tiers including at least one A/B, good volume | High confidence — zone likely holds |
| 18-25 | **FORTRESS** | 4+ tiers stacking with volume dominance + ladder forming | Very high confidence — add on dips to zone |
| 25+ | **IMMUTABLE** | 5-6 tiers, full ladder, massive volume dominance, no wrong-way | Maximum conviction — the home run setup |

## Components Explained

### Tier Stacking (the foundation)

The VOB indicator runs 6 independent engines at different EMA lengths. When
multiple tiers create zones at the same price level, it means the EMA crossover
signal is occurring across MULTIPLE timeframe-equivalent sensitivities simultaneously.

**Why stacking matters:** A single-tier zone can form from random noise in the
EMA crossover. Three tiers forming at the same price requires a genuine structural
shift across multiple measurement scales. The probability of 3+ tiers randomly
stacking decreases exponentially — it's real signal, not noise.

**The stk_bull metric** from the VOB indicator counts how many tiers have active
bullish zones within stacking_threshold_pct (default 2%) of current price.
stk_bull ≥ 3 = STRONG, stk_bull ≥ 5 = IMMUTABLE.

### Volume Dominance (the energy)

```
Vol_dominance = bull_pool / (bull_pool + bear_pool)
```

The bull_pool is the total accumulated volume across all active bullish zones.
The bear_pool is the same for bearish zones. When bull_pool >> bear_pool, it
means significantly more volume accumulated during bullish EMA crossover events
than bearish ones. The buyers were more aggressive than the sellers.

**T3 condition requires:** dominant zone volume > opposing pool × super_mult.
This ensures the single remaining zone has MORE buying power than all opposing
zones combined. It's a volume supremacy test.

### Ladder Formation (structural integrity)

A ladder means all 6 tiers' zones are forming in a staircase pattern:
- **Bull ladder:** Each tier F→A has ascending lows (higher floors)
- **Bear ladder:** Each tier F→A has descending highs (lower ceilings)

This represents structural momentum across all measurement scales. It's the
physical equivalent of multiple independent measurements all agreeing on the
same trend direction. In Anish's framework, a full bull ladder is the strongest
possible structural confirmation that the floor is rising.

### Anti-Fragility (coherence)

**Wrong-Way 3** means 3 consecutive tiers are violating the expected sequence —
bull zones descending when they should ascend (or vice versa). This indicates
structural incoherence — the zone system is fighting itself.

**Adjacent** means a same-tier bull AND bear zone formed within 25 bars. This
indicates the market is rapidly switching direction at that sensitivity level —
indecision, not conviction.

Both reduce tensile strength because they indicate the VOB structure is not
cleanly directional.

## Multi-Timeframe Tensile

The tensile strength score should be computed at MULTIPLE timeframes and
compared:

| Timeframe | What It Tells You |
|-----------|-------------------|
| 5-minute | Intraday zone strength (scalp-level) |
| 15-minute | Short-term structural support |
| 1-hour | Institutional timeframe zone strength |
| 4-hour | Swing trade zone durability |
| Daily | Position-level structural support |

**Confluence rule:** When tensile is STRONG or higher on 15m + 1h + daily
simultaneously at the same price level = the highest-conviction setup.

## Integration with NOI and Detection Plots

The Tensile Strength score feeds into the Maestro Score (Task 14):

```
Maestro = f(Tensile, NOI_signal, Detection_confluence, Sector_rotation)
```

When Tensile ≥ 18 (FORTRESS) AND CIR_LONG fires AND 3+ E+A detection plots
fire on the same bar = maximum conviction. This is Anish's "it's going up
like 30%" scenario.

### Links
- [[vob-indicator]] — the zone data that feeds this model
- [[vob-embedding-map]] — which detection plots are zone-embedded
- [[noi-thresholds]] — NOI signals that confirm/amplify
