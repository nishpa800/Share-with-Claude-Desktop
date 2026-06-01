# VOB — Volume Order Block Indicator (v9.1)

Source: nishpa800/indicators · vob/versions/VOB_Asym_T3x6_MutEx_Claude_v9_2026-05-12.pine
Lines: 1,722 · Pine Script v6 · Overlay indicator

## What It Does

Detects Volume Order Blocks — price zones where significant volume accumulated
during an EMA crossover event. These zones act as support (bullish) or resistance
(bearish). When price returns to a zone, it tends to bounce or reject. This is
the CENTRAL indicator in Anish's thesis — everything else orbits this.

## How It Works (the physical measurement)

1. Two EMAs computed per sensitivity tier: fast = sensitivity value, slow = sensitivity + 13
2. Bullish crossover (fast > slow) → find lowest bar in lookback → create BULLISH zone
   around that low with accumulated volume from low bar to crossover bar
3. Bearish crossunder (fast < slow) → find highest bar → create BEARISH zone around
   that high with accumulated volume
4. Zones persist until INVALIDATED: bullish zone dies when price closes BELOW lower boundary;
   bearish zone dies when price closes ABOVE upper boundary
5. Zones within 3× ATR(200) are deduplicated — newer replaces older

## Six Sensitivity Tiers

| Tier | Default Sensitivity | Character |
|------|-------------------|-----------|
| A | 850 | Highest — fewest zones, strongest, slowest to trigger |
| B | 750 | Second highest |
| C | 650 | Middle-high |
| D | 550 | Middle-low |
| E | 450 | Second lowest |
| F | 350 | Lowest — most zones, weakest, fastest to trigger |

Each tier runs its OWN independent VOB engine. Zones from different tiers can
OVERLAP at the same price — this is "stacking" and represents extreme confluence.
**Stacking is the key to tensile strength — more tiers stacking = harder to break.**

### Optimization Targets
The 6 sensitivity values (850, 750, 650, 550, 450, 350) are the PRIMARY parameters
for autoresearch optimization per timeframe. These control zone formation frequency
and strength.

## Detection Plots (25 total)

### Layer 1 — T3 Super Signals (13 plots)

T3 fires when: exactly ONE zone exists in the dominant direction, that zone's
volume exceeds the opposing pool × super_mult (default 1.0), and current price
is INSIDE that zone. This is the highest-conviction signal.

| Plot | Condition | Visual |
|------|-----------|--------|
| T3a Buy | 1 bull zone, vol > bear pool × mult, price inside zone (tier A) | Green circle, top |
| T3a Sell | 1 bear zone, vol > bull pool × mult, price inside zone (tier A) | Red X-cross, top |
| T3b Buy | Same logic, tier B | Cyan circle, above bar |
| T3b Sell | Same logic, tier B | Pink X-cross, above bar |
| T3c Buy | Tier C | Blue circle, below bar |
| T3c Sell | Tier C | Purple X-cross, below bar |
| T3d Buy | Tier D | Yellow circle, bottom |
| T3d Sell | Tier D | Orange X-cross, bottom |
| T3e Buy | Tier E | Orange arrow down, above bar, HUGE |
| T3e Sell | Tier E | Dark red cross, above bar |
| T3f Buy | Tier F | Gold arrow up, below bar, HUGE |
| T3f Sell | Tier F | Dark red cross, below bar |
| Nagasaki | bar[1] volume > ALL prior volume ever seen on this ticker/TF | Purple diamond, offset -1 |

### Layer 2 — Zone Creation Markers (12 plots)

Fire when a new zone is created at any tier. Cooldown-gated.
- 6 bullish zone creation markers (one per tier A-F)
- 6 bearish zone creation markers (one per tier A-F)

### Layer 3 — New Detection Plots v9 (7 plots)

| Plot | Condition | What It Detects |
|------|-----------|-----------------|
| Bull Ladder (L↑) | All 6 tiers F→A active, wick lows ascending (within tolerance) | Full-tier structural bullish staircase — extremely rare, extremely strong |
| Bear Ladder (L↓) | All 6 tiers F→A active, wick highs descending | Full-tier structural bearish staircase |
| Bull Ladder+Gap (LG↑) | Bull ladder + current bar gaps up ≥ 0.5% | Ladder breakout confirmation |
| Bear Ladder+Gap (LG↓) | Bear ladder + current bar gaps down ≥ 0.5% | Ladder breakdown reversal precursor |
| Adjacent (ADJ) | Same-tier bull AND bear zone formed within 25 bars | Rapid formation of opposing zones at same sensitivity — market indecision/transition |
| Wrong-Way 3 Bull (WW↓) | 3 consecutive tiers with bull zones DESCENDING (violating expected ascent) | Structural degradation — bull zones losing height, bearish signal |
| Wrong-Way 3 Bear (WW↑) | 3 consecutive tiers with bear zones ASCENDING (violating expected descent) | Structural degradation — bear zones losing depth, bullish signal |

## Input Parameters (optimization targets)

| Parameter | Default | Range | What It Controls |
|-----------|---------|-------|-----------------|
| Sensitivity A | 850 | 1+ | EMA length for tier A zones |
| Sensitivity B | 750 | 1+ | EMA length for tier B zones |
| Sensitivity C | 650 | 1+ | EMA length for tier C zones |
| Sensitivity D | 550 | 1+ | EMA length for tier D zones |
| Sensitivity E | 450 | 1+ | EMA length for tier E zones |
| Sensitivity F | 350 | 1+ | EMA length for tier F zones |
| Super Mult | 1.0 | 0.1+ | T3 signal threshold — dominant vol must exceed opposing × this |
| Cooldown Bars | 100 | 0+ | Suppress same signal for N bars after firing |
| Ladder Tolerance % | 0.3 | 0+ | Per-tier price slack for ladder detection |
| Ladder Gap Threshold % | 0.5 | 0+ | Minimum gap size for Ladder+Gap |
| Adjacent Bar Window | 25 | 1+ | Max bars between same-tier opposing zones for Adjacent |
| Stacking Threshold % | 2.0 | 0.1+ | Zones within this % of price count as "stacked" |

## Emission Layer (37 numeric plots for Claude Code MCP)

The indicator emits through ALL 6 channels Claude Code can read:
1. plot() → data_get_study_values: 37 time series per bar
2. label.new() → data_get_pine_labels: metadata at zone formation
3. table.new() → data_get_pine_tables: comprehensive snapshot
4. log.info() → pine_get_console: per-bar streaming data
5. alert() → Bloomberg-format pipe-delimited strings
6. line.new() → data_get_pine_lines: zone boundary prices

Emission metrics computed per tier:
- Active zone count (bull/bear)
- Nearest zone distance % from price
- Stacking count (zones within threshold of price)
- Bull/bear gap % (distance to nearest opposing zone)
- EMA slope (momentum direction per tier)
- Nearest zone volume

## Bloomberg-Format Alert Schema

```
T3_SIGNAL|TICKER:AAPL|EXCHANGE:NASDAQ|TF:15|SIGNAL:T3_SUPER_BUY|TIER:A|
SENS:850|DIR:BULL|CLOSE:310.77|VOL:43670|VOLRANK:85|RSI:62.3|SESS:12|
BULLPOOL:1234567|BEARPOOL:789012|BULLZONES:4|BEARZONES:2|
BULLSTACK:3|BEARSTACK:0|BULLGAP:5.2|BEARGAP:1.3|
NRBULLDIST:0.5|NRBEARDIST:3.1|SLOPE:0.0023
```

## Relationship to Thesis

VOB IS the thesis. The "unbreakable floor" Anish describes is:
- Multiple tiers (A+B+C or more) stacking at the same price level
- Each tier's zone volume exceeding the opposing pool
- The ladder pattern (F→A ascending lows) confirming structural bullish staircase
- When price sits at the bottom of this stacked zone AND detection plots from
  other indicators fire inside it = the home run setup

### What Makes a VOB "Unbreakable" (tensile strength indicators)

1. **Tier stacking (stk_bull ≥ 3):** 3+ tiers with zones near current price
2. **Volume dominance:** Bull pool >> Bear pool (T3 condition)
3. **Ladder formation:** All 6 tiers ascending = maximum structural integrity
4. **No Wrong-Way:** Absence of WW signals = structure is coherent
5. **Adjacent NOT firing:** No rapid opposing zone formation = clean trend
6. **Nagasaki volume on formation bar:** All-time-high volume when zone was created

### Links to Other Indicators

- [[b2b-pup-indicator]] — detection plots that fire inside VOB zones
- [[squarify-indicator]] — 46 signals, many VOB-aware
- [[tnt-od-indicator]] — TNT zones interact with VOB zones
- [[noi-thresholds]] — NOI signals confirm/amplify VOB setups
