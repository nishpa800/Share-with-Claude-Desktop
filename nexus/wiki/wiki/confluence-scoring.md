# Confluence Scoring System — The Orchestra Score

## The Equation

```
Confluence(ticker, t) = Σ(plot_weight × plot_fired) × Tensile_multiplier × NOI_multiplier × Sector_multiplier

Where:
  Detection_score = Σ w_i × fired_i   for each detection plot i that fired on this bar

  Plot weights (by VOB embedding category):
    E+A (Embedded + Amplifier) = 5  (GRAIL, SD!, UC NAGASAKI, etc.)
    E   (Embedded)             = 3  (Napalm, TNT, PBJ approach, etc.)
    A   (Amplifier)            = 2  (Nagasaki, HV+D, WBUSH, etc.)
    C   (Coincident)           = 1  (UU, FAUNA, RVOL, etc.)
    I   (Independent)          = 0  (Omega-A — excluded from scoring)

  Tensile_multiplier:
    NONE (0-3)      → 0.25 (nearly zeroes out the score — no zone = no play)
    WEAK (3-7)      → 0.50
    MODERATE (7-12) → 0.75
    STRONG (12-18)  → 1.00
    FORTRESS (18-25)→ 1.50
    IMMUTABLE (25+) → 2.00

  NOI_multiplier:
    No NOI data        → 1.00 (neutral — ticker may not be NYSE-listed)
    CIR_LONG aligns    → 1.30 (institutional flow confirms bullish zone)
    CIR_SHORT aligns   → 1.30 (institutional flow confirms bearish zone)
    CIR contradicts    → 0.50 (institutional flow fights the zone — caution)
    OIA confirms today → 1.15 (opening momentum aligns)
    HomeRun config     → 1.50 (CIR + OIA + VIX + Friday all align)

  Sector_multiplier:
    Sector inflowing (30-day positive ETF flow) → 1.10
    Sector neutral                              → 1.00
    Sector outflowing (30-day negative ETF flow)→ 0.80
```

## Confluence Score Classification

| Score | Level | Description | Action |
|-------|-------|-------------|--------|
| 0-5 | **NOISE** | Few weak signals, no zone structure | Ignore |
| 5-15 | **WATCH** | Some signals firing, moderate zone | Add to watchlist, do not trade |
| 15-30 | **SETUP** | Multiple signals, strong zone, some confirmation | Prepare position, wait for entry trigger |
| 30-50 | **TRADE** | Strong confluence, fortress zone, NOI alignment | Enter position with standard size |
| 50-80 | **CONVICTION** | Heavy confluence, immutable zone, full NOI + sector alignment | Enter with increased size |
| 80+ | **HOME RUN** | Maximum possible confluence — this is the play Anish describes | Maximum conviction position |

## Example Scenarios

### Scenario A: Noise (score ~3)
- 2 coincident plots firing (FAUNA bull + RVOL 1x) → 1+1 = 2
- No VOB stacking → Tensile NONE → ×0.25
- No NOI signal → ×1.0
- Score: 2 × 0.25 × 1.0 = 0.5 → NOISE
- Action: Nothing. Random candle patterns without structure.

### Scenario B: Setup (score ~22)
- T3b Buy fires (E, weight 3) + PUP (C, weight 1) + SAAB (C, weight 1) = 5
- VOB stacking: 3 tiers near price → Tensile STRONG → ×1.0
- CIR_LONG from yesterday → ×1.30
- Sector inflowing → ×1.10
- Score: 5 × 1.0 × 1.30 × 1.10 = 7.15 → WATCH (borderline SETUP)

### Scenario C: Home Run (score ~95)
- GRAIL fires (E+A, weight 5) + SD! (E+A, weight 5) + NPM+UC+PBJ (E+A, weight 5) + 
  T3a Buy (E, weight 3) + Nagasaki (A, weight 2) + FAUNA (C, weight 1) = 21
- VOB: 5 tiers stacking, full bull ladder → Tensile IMMUTABLE → ×2.0
- CIR_LONG + OIA confirms + High VIX + Friday → HomeRun config → ×1.50
- Sector inflowing → ×1.10
- Score: 21 × 2.0 × 1.50 × 1.10 = 69.3 → CONVICTION (approaching HOME RUN)

### Scenario D: The Absolute Peak
All 7 E+A signals fire + T3a + Nagasaki inside a 6-tier ladder VOB with
HomeRun NOI config in an inflowing sector:
- Detection: 7×5 + 3 + 2 = 40
- Tensile: ×2.0
- NOI: ×1.50
- Sector: ×1.10
- Score: 40 × 2.0 × 1.50 × 1.10 = 132 → **ABSOLUTE HOME RUN**
- This may fire once a quarter across all 807 watchlist tickers.

## What the Autoresearch Loop Optimizes

The overnight permutation engine tests WHICH plot_weight assignments produce
the best Northstar scores out of sample. The default weights above are
theoretical — the autoresearch loop calibrates them empirically:

1. Run the scoring model on 30 days of historical data
2. For each signal event, compute: confluence score at signal time → actual return over 1/3/5 days
3. Optimize weights to maximize: high scores → big wins, low scores → correctly skipped
4. The Northstar metric ensures both PPV (precision) and Sensitivity (recall) are balanced

## Daily Workflow

### Pre-Market (7:00 AM CT)
1. Load yesterday's closing NOI signals → CIR scores
2. Load yesterday's VOB state per ticker → Tensile scores
3. Load ETF sector flows → Sector multipliers
4. Compute Confluence for every watchlist ticker
5. Rank by Confluence score descending
6. Morning report: top 10 TRADE+ tickers with full breakdown

### Opening (8:25-8:35 AM CT)
1. OIA signals fire → update NOI_multiplier
2. Detection plots fire on opening bars → update Detection_score
3. Recompute Confluence in real-time
4. If any ticker jumps to CONVICTION+ → alert

### Post-Market (3:15 PM CT)
1. Score all closing NOI for tomorrow
2. Run forward Confluence projection: "If tomorrow's detection plots fire like
   today's, what will tomorrow's top signals be?"
3. Generate pre-computed watchlist for tomorrow's open

### Links
- [[vob-embedding-map]] — plot weight categories
- [[tensile-strength-model]] — Tensile multiplier source
- [[noi-cross-reference]] — NOI multiplier source
- [[noi-thresholds]] — CIR/OIA definitions
