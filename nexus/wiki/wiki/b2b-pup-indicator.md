# B2B PUP — Back-to-Back Pocket Pivot Combined (v4.32)

Source: nishpa800/indicators · b2b-pup/versions/B2B_PUP_Combined_v4.32_2026-05-04.pine
Lines: 1,259 · Pine Script v5 · Overlay indicator

## What It Does

Detects back-to-back Pocket Pivot Up Days (PUP) — consecutive bars where price
rises significantly with volume exceeding the highest red-bar volume in the lookback
period. This is a multi-engine indicator that combines PUP with FAUNA, Displacement,
PBJ, RVOL, HV+D, TNT/Napalm, and Combo Sets to produce 20 numbered detection plots.

## Seven Engines

### Engine A — PUP / PPD (Offset: 0)
- **PUP (Pocket Pivot Up):** Close > Open by >3% AND volume > highest red volume in 10 days
- **PPD (Pocket Pivot Down):** Open > Close by >3% AND volume > highest green volume in 10 days
- Input params: % Change (3.0), Lookback Days (10)

### Engine B — FAUNA (Offset: 0)
Seven candle anatomy classifiers, all hardcoded ON:
- **MB (Momentum Bar):** body > 1.6× ATR14, body ratio > 70%, volume > 1.8× avg
- **RE (Range Expansion):** range > 2.2× ATR14, small wick (<15%), volume > 1.8× avg
- **GG (Gap & Go):** gap > 0.9× ATR14, gap direction matches candle, volume > 1.8× avg
- **TA (Trend Acceleration):** trend-aligned, close change > 1.6× avg delta, volume > 1.8× avg
- **TR (Trap Reversal):** weak prior bar + current MB/RE/TA
- **ES (Engulfing Surge):** strong opposite prior bar + current MB/RE/TA
- **GDR (Gap Direction Reversal):** prior bar opposite direction + gap

### Engine C — Displacement (Offset: -1)
- Bar[1] range exceeds StdDev × 5.0 threshold AND FVG (Fair Value Gap) confirmed on bar[0]
- Measures extreme single-bar moves with gap continuation

### Engine D — PBJ (Offset: 0)
- VWMA + ATR Supertrend trailing stop system
- PB (Price Break): supertrend crossover after zone approach
- PBJ (PB & Jelly): PB + price at HH/LL extreme with volume confirmation
- Full level/approach/reacceleration engine with 30 zones tracked

### Engine E — RVOL Tiers (Offset: 0)
Relative volume classification with timeframe-adjusted thresholds:
- **SAAB:** RVOL ≥ saab_threshold, < 1x threshold (mild)
- **Kratos:** Bearish SAAB equivalent
- **RVOL 1x Bull/Bear:** RVOL ≥ 1x threshold, < Grand Slam
- **Grand Slam:** RVOL ≥ grand slam threshold (extreme bull)
- **MOAB:** Extreme bear RVOL
- **Pentagon:** Relative volume ratio ≥ 1x, ≤ WTC
- **WTC:** Relative volume ratio > WTC threshold, ≤ Hiroshima
- **Hiroshima:** Relative volume ratio > Hiroshima threshold
- **Nagasaki:** ALL-TIME HIGH volume for this ticker/timeframe

### Engine F — HV+D (Offset: -1)
- High Volume + Displacement: volume is highest in 50/100/200/500/1000 bars AND
  displacement + FVG confirmed
- **HVD+PBJ:** HV+D + PBJ on aligned bar
- **B2B HVD:** Back-to-back HV+D (consecutive bars)
- **B2B HVD+PBJ:** B2B HV+D + PBJ aligned

### Engine G — TNT / Napalm / Continuous
- **TNT:** Three-engine confluence (VOB-like EMA crossover + ANISH swing structure + FLUX)
- **Napalm (NPM):** Displacement through an active opposing TNT zone (scans ALL active zones, up to 30)
- **Charge:** Opposing zone displacement that pushes a new level
- **Return-to-TNT:** Price retraces back into a TNT zone after breakout
- **Continuous (CONT):** Rapid-fire events within N bars (sudden change proximity)
- **TNT 2.0 (Super):** TNT raw + opposing Charge simultaneously
- **B2B Napalm:** Consecutive Napalm/Charge fires
- **Napalm Consolidated:** Napalm OR Charge (equivalent signals per Anish's framework)

## The 20 Detection Plots (S-Numbered)

| # | Name | Condition | Offset | What It Detects |
|---|------|-----------|--------|-----------------|
| S1 | B2B PUP | PUP on bar[0] AND PUP on bar[1] | 0 | Consecutive pocket pivots — strong buying |
| S2 | B2B PUP+FAUNA | S1 + FAUNA on both candles | 0 | Pocket pivots with candle anatomy confirmation |
| S3 | B2B PUP+DISP | S1 + Displacement/HV+D on both | -1 | Pocket pivots with extreme move + FVG |
| S4 | B2B PUP+FAUNA+DISP | S1 + FAUNA + Displacement on both | -1 | Triple confirmation: PUP + anatomy + displacement |
| S5 | B2B PUP+SAAB | S1 + directional RVOL on both candles | 0 | Pocket pivots with relative volume confirmation |
| S6 | Any B2B+PBJ | Any B2B PUP + PBJ on either candle | -1 | Pocket pivots at supertrend level approach |
| S8 | UC+B2B PUP | Unified Combo + B2B PUP | -1 | Combo set confluence with pocket pivots |
| S9 | Uni Combo+B2B PUP | (S19 OR S20) + B2B PUP | -1 | Broadest combo + PUP gate |
| S10 | L1 B2B+B2B PUP | Long 1 back-to-back + B2B PUP | 0 | Long/short ratio extreme + pocket pivots |
| S11 | (FVG/L1)+B2B PUP | FVG Combo or Long 1 + B2B PUP | -1 | FVG or ratio + pocket pivots |
| S12 | UU+B2B PUP | UU/UUU/UUUU + B2B PUP | 0 | Multi-qualifier streak + pocket pivots |
| S13 | B2B NPM+B2B PUP | Back-to-back Napalm + B2B PUP | 0 | Consecutive TNT zone displacements + pocket pivots |
| S14 | CONT+B2B PUP | Continuous + B2B PUP | 0 | Rapid-fire events + pocket pivots |
| S15 | TNT+B2B PUP | TNT Raw + B2B PUP | 0 | Three-engine confluence + pocket pivots |
| S16 | NPM+B2B PUP | Napalm Raw + B2B PUP | -1 | Zone displacement + pocket pivots |
| S17 | B2B HVD+B2B PUP | Back-to-back HV+D + B2B PUP | -1 | Consecutive high-volume displacement + pocket pivots |
| S18 | B2B HVDPBJ+B2B PUP | B2B HV+D+PBJ + B2B PUP | -1 | Maximum triple: HV+D + PBJ + pocket pivots |
| S19 | Unified Combo ×2 | Back-to-back Unified Combo (standalone) | -1 | Consecutive FVG+Matrix combos — standalone signal |
| S20 | FVG/MAT/Uni Combo ×2 | Any combo ×N (standalone) | -1 | Broadest combo repetition — standalone signal |

## Key Input Parameters

| Parameter | Default | Engine | What It Controls |
|-----------|---------|--------|-----------------|
| % Change | 3.0 | PUP/PPD | Minimum price move to qualify as pocket pivot |
| Lookback Days | 10 | PUP/PPD | Window for highest red/green volume comparison |
| Std Dev Length | 100 | Displacement | Lookback for displacement threshold calculation |
| Std Dev Multiplier | 5.0 | Displacement | How many σ constitutes "displacement" |
| Sensitivity | 100 | TNT | EMA length for TNT zone formation |
| Swing Length | 10 | TNT | Bars for swing high/low detection |
| Sudden Change Max Bars | 3 | CONT | Max bars between events for "continuous" |
| Max TNT Zones | 30 | Napalm | How many zones Napalm scans for displacement |

## Relationship to VOB Thesis

B2B PUP detection plots are the signals that fire INSIDE VOB zones. When a VOB
is forming (detected by the VOB indicator's zone creation) and B2B PUP fires
simultaneously, it confirms that the VOB has real buying/selling power behind it.

**Highest-conviction VOB-embedded B2B PUP signals:**
- S4 (B2B PUP+FAUNA+DISP) — triple confirmation
- S13 (B2B NPM+B2B PUP) — Napalm means displacement through a TNT zone + pocket pivots
- S17 (B2B HVD+B2B PUP) — high volume displacement + pocket pivots
- S18 (B2B HVDPBJ+B2B PUP) — maximum confluence

### Links
- [[vob-indicator]] — the VOB zones these signals fire inside
- [[squarify-indicator]] — shares engines (FAUNA, RVOL, Displacement, TNT)
- [[tnt-od-indicator]] — TNT engine is shared
