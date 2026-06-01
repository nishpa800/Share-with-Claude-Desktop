# Detection Plot × NOI Cross-Reference

## The Question

When CIR (Closing Imbalance Reversal) fires, which detection plots tend to also
be firing? When OIA (Opening Imbalance Acceleration) fires, which detection
plots are present? This cross-reference connects Anish's indicator suite to the
NOI signal system.

## Theoretical Mapping

### CIR LONG (closing sell imbalance → buy reversal over 3-5 days)

**Why certain detection plots should correlate with CIR:**
CIR fires when institutions dump shares at the close (uninformed MOC flow).
The 3-5 day reversal represents price returning to fair value. Detection plots
that detect accumulation, support testing, or buying pressure should fire at the
START of the reversal — confirming that the CIR signal is producing the expected
price action.

| Detection Plot | Expected CIR Correlation | Mechanism |
|---------------|-------------------------|-----------|
| T3 Buy (any tier) | **HIGH** | T3 fires when price is inside a dominant bullish zone — exactly where price returns during CIR reversal |
| PUP / B2B PUP | **HIGH** | Pocket pivots detect buying volume exceeding red volume — accumulation during reversal |
| FLOOR / 2F | **HIGH** | Structural support (Ping Pong) — CIR reversal often bounces at these levels |
| Napalm (bull) | **MEDIUM** | Zone displacement — may fire as price accelerates through the reversal |
| UU/UUU/UUUU | **MEDIUM** | Multi-qualifier streaks — accumulation patterns during multi-day reversal |
| FAUNA (bull) | **MEDIUM** | Candle anatomy — momentum/range expansion bars during reversal |
| RVOL (bull) | **MEDIUM** | Relative volume spikes during reversal buying |
| Alpha Strike | **LOW** | First-signal-of-session — may fire on the morning after CIR signal |
| OD (Opening Drive) | **LOW** | Opening displacement — may fire on gap-up morning after CIR |
| GOLF | **LOW** | 3-bar waterfall — too short for multi-day CIR horizon |

### CIR SHORT (closing buy imbalance → sell reversal)

Mirror of above: detection plots that detect distribution, resistance, selling
pressure should correlate. PPD, MOAB, bear FAUNA, bear Napalm, bearish T3.

### OIA LONG (opening buy acceleration → 20-min momentum)

**Why certain detection plots should correlate with OIA:**
OIA fires on opening auction buy-side acceleration. This represents aggressive
pre-open buying. Detection plots that detect the SAME buying pressure in the
first 5-20 minutes of trading should confirm the OIA signal.

| Detection Plot | Expected OIA Correlation | Mechanism |
|---------------|-------------------------|-----------|
| OD (Opening Drive) | **VERY HIGH** | This IS the opening drive detector — directly measures same phenomenon |
| Alpha Strike | **VERY HIGH** | First-signal-of-session — fires at open when OIA momentum carries through |
| PUP | **HIGH** | Pocket pivot on first bar — volume exceeding red confirms OIA direction |
| FAUNA (bull) | **HIGH** | Momentum Bar / Range Expansion on opening bar |
| GG (Gap & Go) | **HIGH** | Gap that continues — OIA often produces gaps |
| HW (Heavy Weapon) | **MEDIUM** | 5x displacement + PBJ — may fire if opening move is extreme |
| Nagasaki | **MEDIUM** | All-time-high volume — opening bars can produce extreme volume |
| TNT | **LOW** | Zone confluence — independent of opening dynamics |

## Cross-Signal Reinforcement Rules

### Rule 1: CIR + T3 = Maximum Reversal Confidence
When CIR_LONG fires (closing sell imbalance) AND the next day T3 Buy fires
(price inside dominant bullish zone), the reversal is being CONFIRMED by the
zone structure. Both the institutional flow (NOI) and the market structure (VOB)
agree — this is the highest-conviction reversal.

### Rule 2: OIA + Alpha Strike + OD = Opening Drive Home Run
When OIA fires (opening buy acceleration) AND Alpha Strike fires (first signal
of session at structural support with RVOL) AND OD fires (Opening Drive
displacement), all three are detecting the same phenomenon from different
angles. Enter at 9:35 ET, ride 20 minutes.

### Rule 3: CIR + VOB Tensile ≥ 18 + E+A Detection Plots = The Play
This is Anish's thesis fully realized:
1. CIR_LONG fires → institutional flow predicts reversal
2. VOB Tensile ≥ 18 (FORTRESS) → the floor is structurally sound
3. 3+ E+A detection plots firing → multiple independent confirmations
4. Result: buy at the bottom of an unbreakable VOB with institutional flow + 
   detection plot confluence all agreeing → the 10x move

## Empirical Validation Plan

As the autoresearch loop accumulates data, compute:
- For each CIR event: which detection plots fired within ±2 bars?
- For each OIA event: which detection plots fired within ±2 bars?
- Correlation matrix: CIR × each detection plot → did the reversal actually happen?
- OIA × each detection plot → did the 20-min momentum carry?

After 30+ trading days, this map will be populated with REAL correlations,
not theoretical ones.

### Links
- [[vob-indicator]] — zone data for T3 correlation
- [[vob-embedding-map]] — E+A classification
- [[tensile-strength-model]] — FORTRESS threshold
- [[noi-thresholds]] — CIR and OIA definitions
