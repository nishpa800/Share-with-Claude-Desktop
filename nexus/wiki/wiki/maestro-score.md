# Maestro Score — The Final GO/NO-GO Signal

## What This Is

The Maestro Score is the single composite number that combines everything:
VOB tensile strength, detection plot confluence, NOI signals, sector rotation,
and multi-timeframe alignment into one GO/NO-GO decision.

This is the conductor directing the orchestra. Each instrument (indicator)
plays its part. The Maestro listens to all of them and decides: is this a
symphony or cacophony?

## The Equation

```
Maestro(ticker, t) = Confluence(ticker, t) × MTF_alignment × Freshness_decay

Where:
  Confluence = from [[confluence-scoring]] (incorporates Tensile, NOI, Sector, Detection plots)

  MTF_alignment = Multi-timeframe agreement multiplier
    All checked timeframes agree on direction:
      3 timeframes agree → 1.20
      4 timeframes agree → 1.40
      5+ timeframes agree → 1.60
    Any timeframe contradicts:
      1 contradicts → 0.90
      2+ contradict → 0.70

  Freshness_decay = how recent the signals are
    Fired this bar                → 1.00
    Fired 1-3 bars ago            → 0.90
    Fired 4-10 bars ago           → 0.70
    Fired 11-25 bars ago          → 0.50
    Fired 26+ bars ago            → 0.30 (stale — signal is dying)

  Final Maestro range: 0 to ~200+ (theoretical max with everything aligned)
```

## Decision Matrix

| Maestro Score | Decision | Position Size | Hold Period | Stop Logic |
|---------------|----------|--------------|-------------|------------|
| 0-10 | **NO TRADE** | 0% | — | — |
| 10-25 | **WATCH** | 0% | — | Add to watchlist |
| 25-40 | **STARTER** | 25% of max | 1-3 days | Below VOB zone lower boundary |
| 40-60 | **STANDARD** | 50% of max | 3-5 days | Below nearest bull zone mid |
| 60-80 | **CONVICTION** | 75% of max | 5-10 days | Below stacked zone cluster |
| 80+ | **HOME RUN** | 100% of max | Hold until VOB invalidates | Only if zone breaks on daily close |

## What a HOME RUN Looks Like in Practice

```
TICKER: XYZ
MAESTRO SCORE: 94.7

VOB STATE:
  Tier A: Bullish zone at $45.20 (active, vol=12M)
  Tier B: Bullish zone at $45.35 (active, vol=8M)
  Tier C: Bullish zone at $44.90 (active, vol=15M)
  Tier D: Bullish zone at $45.10 (active, vol=6M)
  Tier E: Bullish zone at $45.50 (active, vol=4M)
  Stacking: 5 tiers within 2% of price ← IMMUTABLE
  Tensile: 28.5
  Bull Ladder: YES (ascending lows F→A)
  Volume Dominance: 0.85 (bull pool dominates)

DETECTION PLOTS FIRING:
  GRAIL (#32): ✅ (Napalm + PBJ + PUP + UC) — weight 5
  SD! (#1): ✅ (UC + Napalm + PUP) — weight 5
  T3a Buy: ✅ (price inside dominant A-tier zone) — weight 3
  Nagasaki: ✅ (all-time-high volume) — weight 2
  FAUNA Bull: ✅ (Momentum Bar) — weight 1
  Detection Score: 16

NOI:
  Yesterday CIR: LONG (sell imbalance -$18M notional)
  Today OIA: BUY acceleration (8 consecutive, 2σ)
  VIX: 28 (elevated)
  Day: Friday
  NOI Config: HOME RUN (CIR + OIA + VIX + Friday)
  NOI Multiplier: 1.50

SECTOR:
  XLK (Technology): +$454M 30-day inflow
  Sector Multiplier: 1.10

MULTI-TIMEFRAME:
  15m: Bullish VOB ← agrees
  1h: Bullish VOB ← agrees
  4h: Bullish VOB ← agrees
  Daily: Bullish VOB ← agrees
  MTF Alignment: 1.40

CALCULATION:
  Detection: 16
  Tensile: ×2.00 (IMMUTABLE)
  NOI: ×1.50 (HOME RUN)
  Sector: ×1.10
  = Confluence: 16 × 2.0 × 1.5 × 1.1 = 52.8
  MTF: ×1.40
  Freshness: ×1.00 (all fired this bar)
  = MAESTRO: 52.8 × 1.40 × 1.00 = 73.9

DECISION: CONVICTION — 75% position, hold 5-10 days
  Entry: $45.30 (current price, inside stacked VOB zone)
  Stop: $44.50 (below lowest zone in stack — zone cluster invalidation)
  Target: None — hold until VOB invalidates or 10 days
  Risk/Reward: $0.80 risk for potentially 10-30% move (Anish's thesis)
```

## What the Autoresearch Loop Calibrates

The Maestro Score has several tunable components:

1. **Plot weights** (E+A=5, E=3, A=2, C=1) → optimize via overnight permutations
2. **Tensile multipliers** (NONE=0.25 to IMMUTABLE=2.0) → calibrate against outcomes
3. **NOI multipliers** (CIR=1.3, HomeRun=1.5) → calibrate against actual reversal rates
4. **MTF alignment multipliers** (3 agree=1.2 to 5+=1.6) → calibrate against actual win rates
5. **Decision thresholds** (WATCH=10, STARTER=25, etc.) → calibrate against actual returns
6. **Freshness decay curve** (1.0 to 0.3) → measure how quickly signals lose predictive power

Each of these is a parameter in signal.py that the autoresearch loop can modify,
backtest, and commit/revert based on Northstar improvement.

## Daily Report Format

The morning report presents the top 10 tickers by Maestro Score:

```
═══════════════════════════════════════════════════════════
  MAESTRO SCORE REPORT — 2026-05-28 Pre-Market
═══════════════════════════════════════════════════════════

#   Ticker  Maestro  Decision    Tensile  Detection  NOI        Sector
1   AA      84.2     HOME RUN    IMMUT    GRAIL+SD!  CIR_LONG   XLB ↑
2   TSM     67.3     CONVICTION  FORTR    T3a+NPM    CIR_LONG   SMH ↑
3   GEV     52.1     STANDARD    STRONG   GOLF+PUP   CIR_LONG   XLI ↑
4   NOW     48.7     STANDARD    STRONG   S18+FAUNA  CIR_LONG   XLK ↑
5   CRWD    41.2     STANDARD    MODRT    T3c+SAAB   OIA_LONG   XLK ↑
...
```

This is what Anish sees when he wakes up. No questions. No decisions to make
about methodology. Just: here are the top signals, ranked, with full breakdown.

## The Meta-Insight

The Maestro Score encodes Anish's entire thesis into a number:

1. **VOB tensile strength** = "is the floor unbreakable?"
2. **Detection plots** = "are my indicators screaming?"
3. **NOI** = "are institutions confirming?"
4. **Sector** = "is the tide rising?"
5. **Multi-timeframe** = "does every scale agree?"

When ALL five align: the stock is sitting at the bottom of an immutable
structural floor, smart money is piling in, the sector is inflowing, and every
timeframe confirms the same direction. That's not a 2:1 trade. That's the play
where you size up and hold for the big move.

### Links
- [[confluence-scoring]] — the detection + tensile + NOI composite
- [[tensile-strength-model]] — VOB structural integrity math
- [[vob-embedding-map]] — which detection plots matter most
- [[noi-cross-reference]] — NOI signal alignment
- [[permutation-priority]] — what the autoresearch optimizes
- [[parameter-sensitivity]] — tunable parameters in this equation
