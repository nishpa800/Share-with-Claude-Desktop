# Permutation Priority Map — What to Test First Overnight

## The Problem

~150 detection plots × 13 timeframes × 807 tickers × ~250 historical days = 
billions of possible combinations. We can't test everything in one night.
This map prioritizes which permutations the autoresearch loop tests FIRST.

## Priority Tiers

### P1 — Test TONIGHT (highest expected information gain)

**1. E+A signals inside FORTRESS+ VOB → 5-day return**
- The 7 home-run E+A signals (GRAIL, SD!, UC NAG, NPM+UC+PBJ, CO, S18, GOLF)
- Only when Tensile ≥ 18 (FORTRESS or IMMUTABLE)
- Outcome: 5-day forward return
- Why first: This is the thesis. If E+A + FORTRESS predicts big moves, everything else is optimization.

**2. CIR × top detection plots → 3-5 day return**
- CIR_LONG events from closing NOI
- Cross with: T3 Buy (any tier), PUP, FLOOR, Napalm, GOLF
- Outcome: did the reversal happen? How much?
- Why second: CIR is our best-documented signal (13.2 bps/day). Adding detection plots should improve it.

**3. OIA × Alpha Strike × OD → 20-minute return**
- OIA events from opening NOI
- Cross with: Alpha Strike (#9), OD (#12), PUP, FAUNA
- Outcome: 5/10/15/20 minute returns after 9:35 ET entry
- Why third: OIA is a 20-min trade — quick feedback, many samples per day.

### P2 — Test THIS WEEK

**4. Tensile threshold optimization**
- Vary the tier weights (w_A through w_F) in the tensile equation
- Test: does weighting A at 10 instead of 6 produce better separation?
- Test: does excluding F entirely improve signal quality?

**5. Single detection plot → 1-day return (all 150 plots)**
- Baseline: each plot individually, what's its standalone predictive power?
- This tells us which plots are genuinely useful vs decorative
- Rank all 150 by standalone PPV and Sensitivity

**6. RVOL tier thresholds per timeframe**
- SAAB/1x/GrandSlam thresholds are currently hardcoded per timeframe
- Test: small variations in thresholds → does signal quality improve?

### P3 — Test THIS MONTH

**7. Pairwise plot combinations (top 30 × top 30)**
- After P2 identifies the top 30 standalone plots, test all pairwise combos
- 30 × 29 / 2 = 435 pairs. Each pair tested on 250 days. Manageable.

**8. Multi-timeframe confirmation**
- Does a signal on 15m + 1h simultaneously beat either alone?
- Test all 13 timeframes pairwise for the top 10 signals

**9. Sector-conditional performance**
- Do signals perform differently by sector?
- Test top 10 signals × 11 sectors = 110 permutations

### P4 — Test QUARTERLY

**10. Full combinatorial sweep (top 10 × top 10 × top 10)**
- Triple combinations of the top 10 signals
- 10 × 9 × 8 / 6 = 120 triples. Expensive but comprehensive.

**11. Input parameter sensitivity sweep**
- For each indicator's top 3 most sensitive parameters
- Test ±10%, ±20%, ±50% variations
- ~7 indicators × 3 params × 5 variations = 105 experiments

## Time Budget Per Night

With local Python + numpy on Mac:
- One permutation (generate signals → compute returns → score Northstar): ~2 seconds
- In 8 hours: 14,400 permutations

**P1 experiments (tonight): ~50 permutations. Done in 2 minutes.**
The remaining 8 hours test P2 experiments in the background.

## Experiment Format

Each experiment logged to results.tsv:
```
timestamp  experiment_id  description  northstar  ppv  sensitivity  mcc  n_signals  avg_return  status
```

## What NOT to Test

- Combinations involving I (Independent) category plots — they don't relate to VOB
- Plots that fire < 5 times in 250 days — insufficient sample size
- Parameter changes > ±50% from defaults — too far from calibrated region
- Any combination that produces > 1000 signals per day — too noisy, likely garbage

### Links
- [[vob-embedding-map]] — E+A classification for P1
- [[tensile-strength-model]] — threshold optimization for P2
- [[confluence-scoring]] — weight optimization
