# NOI SIGNAL SYSTEM — Five Pillars Treatment
## The Two Pareto Leverage Points from NYSE Order Imbalance

**Created:** 2026-05-26
**Governing Doctrine:** Five Pillars Operating System v1.0
**Data Source:** Massive.com WebSocket NOI feed (live capture running)
**Status:** ACTIVE — signals can be generated from today's data

---

## PILLAR I — PROBLEM CRYSTALLIZATION

### Problem Statement

Identify the two most outsized, aggressive trading signals derivable from NYSE
Order Imbalance data, formalize them as equations with measurable variables,
and score them across 13 timeframes (1m, 3m, 5m, 10m, 15m, 30m, 1h, 2h, 3h,
1d, 2d, 3d, 1w).

### Equation Triangulation

**E1 — Information Theory (Mutual Information):**
```
I(NOI_signal ; Future_returns) = H(Future_returns) - H(Future_returns | NOI_signal)
```
The NOI signal reduces uncertainty about future returns. The two signals below
maximize this mutual information — they tell us the MOST about what price will
do next. Uninformed flow (index funds, ETF rebalancing) creates a predictable
dislocation that informed traders can exploit.

**E2 — Physics (Mean Reversion as Damped Harmonic Oscillator):**
```
x(t) = A × e^(-γt) × cos(ωt + φ)
```
The closing imbalance creates a price dislocation (amplitude A). The market
acts as a restoring force (spring constant). The dislocation decays
exponentially with damping coefficient γ. 83% reversal in 3-5 days gives
us γ ≈ 0.35/day. The half-life of the dislocation is ln(2)/γ ≈ 2 days.

**E3 — Game Theory (Market Maker Inventory Risk Premium):**
```
Premium = f(Inventory × Volatility × Holding_period)
```
Market makers forced to absorb sell imbalances demand compensation proportional
to: (a) inventory size, (b) overnight volatility (VIX), (c) holding period
(weekend > weekday). This is NOT anomaly — it's a rational equilibrium price
for bearing inventory risk. It persists because someone MUST hold overnight.

### Where equations AGREE
All three say: the closing auction is the primary signal source. The opening
auction has information but it's been arbed by HFTs for intraday scalping.
The closing signal survives because it requires overnight holding, which is
beyond HFT horizons.

---

## THE TWO SIGNALS

---

### SIGNAL 1: CLOSING IMBALANCE REVERSAL (CIR)
**The Passive Fund Liquidity Premium**

#### What it detects
Passive index funds, ETF rebalancing, and pension fund flows create massive
uninformed MOC (Market on Close) orders. These temporarily dislocate the
closing price. 83% of this dislocation reverses within 3-5 days.

#### The Equation

```
CIR_score(ticker, t) = -sign(NOI_close) × |NOI_ratio| × VIX_scale × Calendar_boost

Where:
  NOI_close     = final closing imbalance quantity (positive = buy, negative = sell)
  sign()        = direction (+1 for buy, -1 for sell)
  NOI_ratio     = |imbalance_quantity| / paired_quantity  (strength of imbalance)
  VIX_scale     = VIX / 20  (normalized; >1 when fear is elevated)
  Calendar_boost = 1.0 normally
                 = 1.44 on Fridays (weekend premium: 44.4 bps per Hendershott)
                 = 2.0 on index rebalance dates (forced uninformed flow)
                 = 2.5 on Friday + rebalance (all premiums stack)

  The NEGATIVE sign is critical: we trade OPPOSITE the imbalance.
  Large sell imbalance → CIR_score is POSITIVE (buy signal)
  Large buy imbalance  → CIR_score is NEGATIVE (sell signal)
```

#### Entry Rules
1. At 3:55 PM ET, compute `NOI_ratio` from the latest imbalance message
2. Filter: `NOI_ratio >= 0.10` (10% imbalance-to-paired minimum)
3. Filter: Market cap $2B-$50B (mid-cap sweet spot, excludes mega-caps with too much liquidity)
4. Filter: Average daily volume > 500K shares (tradeable)
5. Rank all qualifying tickers by `|CIR_score|` descending
6. Take top 10 long (highest positive CIR) and top 10 short (most negative CIR)
7. Enter at MOC (Market on Close) or in last 2 minutes of trading

#### Exit Rules (Multi-Timeframe)
| Timeframe | Action | Expected Return |
|-----------|--------|-----------------|
| Overnight (next open) | Sell 50% of position | ~7-12 bps (inventory premium) |
| 1 day | Evaluate: if >50% of expected move captured, tighten stop | ~13 bps |
| 2 days | Half-life of dislocation reached | ~20 bps |
| 3 days | Evaluate for full exit | ~26 bps |
| 5 days | Hard exit — beyond this, signal decays | ~32 bps (full reversal) |

#### Reference Ranges
| Metric | Normal | Strong | Extreme |
|--------|--------|--------|---------|
| NOI_ratio | 0.05-0.10 | 0.10-0.30 | > 0.30 |
| Notional imbalance | < $5M | $5-$20M | > $20M |
| CIR_score magnitude | 0.1-0.5 | 0.5-1.5 | > 1.5 |
| Expected 5-day return (long side) | 15-25 bps | 25-40 bps | > 40 bps |

#### NYSE Significant Imbalance Thresholds
- **S&P 500 stocks:** 30% of 20-day average closing auction size
- **Mid/small cap:** 50% of 20-day average closing auction size
- When NYSE publishes a "Significant Imbalance" it's a STRONG signal

#### Academic Evidence
- Yanbin Wu (SSRN 3440239): 13.2 bps/day risk-adjusted return
- Management Science publication: NYSE floor brokers amplify this effect
- NY Fed Staff Report 917: overnight drift from inventory risk
- 83% reversal rate within 3-5 days (multiple sources)

#### Inversion (how this signal FAILS)
1. The imbalance is INFORMED, not mechanical (e.g., ahead of M&A announcement)
2. A regime change means the "noise" was actually "signal" (the sell-off continues)
3. Concentrated in one sector = macro event, not random fund flow
4. VIX is spiking because of a systemic crisis (correlations go to 1, diversification fails)

**Mitigation:** Cross-reference against Benzinga news for any breaking headlines
on the ticker. If there's material news, skip that ticker — the imbalance is
informed, not mechanical.

---

### SIGNAL 2: OPENING IMBALANCE ACCELERATION (OIA)
**The Pre-Open Momentum Signal**

#### What it detects
During the opening auction window (9:00-9:30 AM ET), NOI messages arrive every
~15 seconds showing the evolving imbalance. When the imbalance ACCELERATES in
one direction (4+ consecutive messages growing), it indicates aggressive
directional order flow that will push the opening price and continue for the
first 20-25 minutes of trading.

#### The Equation

```
OIA_score(ticker, t) = sign(NOI_925) × Accel_factor × Size_factor

Where:
  NOI_925       = imbalance_quantity from 9:25 AM ET onward (last 5 min before open)
  sign()        = direction of imbalance

  Accel_factor  = Consecutive_same_direction / 4
                  (number of consecutive messages where imbalance grew in same direction,
                   divided by minimum threshold of 4; Accel_factor >= 1.0 to trigger)

  Size_factor   = |imbalance_quantity| / σ_imbalance
                  (current imbalance divided by its 20-day standard deviation;
                   Size_factor >= 1.0 means at least 1σ move)

  Trigger: OIA fires ONLY when Accel_factor >= 1.0 AND Size_factor >= 1.0
```

#### Entry Rules
1. Monitor NOI messages from 9:25 AM ET onward
2. For each ticker, track consecutive same-direction imbalance growth
3. Filter: 4+ consecutive accelerating messages (Accel_factor >= 1.0)
4. Filter: Imbalance magnitude >= 1σ of 20-day trailing average (Size_factor >= 1.0)
5. **DO NOT enter at the open** — wait for the 5-minute mark (9:35 AM ET)
6. Enter at 9:35 in the DIRECTION of the imbalance (unlike Signal 1, this is WITH the flow)
7. The 5-minute delay avoids the opening volatility whipsaw

#### Exit Rules (Multi-Timeframe)
| Timeframe | Action | Expected Return |
|-----------|--------|-----------------|
| 5 min (9:40 AM) | First check — is it working? If not, cut | ~0.3% |
| 10 min (9:45 AM) | Trail stop at breakeven if profitable | ~0.5% |
| 15 min (9:50 AM) | Tighten stop to 50% of max gain | ~0.6% |
| 20 min (9:55 AM) | **PRIMARY EXIT — take profit** | ~0.8% (1σ event) |
| 25 min (10:00 AM) | **HARD EXIT — signal expires** | decaying |
| 30 min+ | Signal is DEAD beyond this point | noise |

**This is a 20-25 minute trade.** It does NOT carry overnight. It does NOT
work as a swing trade. The alpha window is 9:35-9:55 AM ET.

#### Reference Ranges
| Metric | Weak | Moderate | Strong | Extreme |
|--------|------|----------|--------|---------|
| Consecutive accel messages | 2-3 | 4-5 | 6-8 | 9+ |
| Size_factor (σ) | 0.5-1.0 | 1.0-1.5 | 1.5-2.5 | > 2.5 |
| Expected 20-min return | 0.2% | 0.5% | 0.8% | > 1.2% |
| Win rate (estimated) | ~50% | ~58% | ~65% | ~72% |

#### Inversion (how this signal FAILS)
1. The acceleration reverses in the last 1-2 minutes (imbalance FLIP = cancel signal)
2. The opening print is a gap that already priced in the imbalance (signal is stale)
3. Major macro news at 9:30 AM (FOMC, jobs report) overwhelms the imbalance signal
4. Low-liquidity stocks: imbalance looks large but there's no volume to trade against

**Mitigation:** If the imbalance FLIPS direction in the last 2 minutes before
open, CANCEL the signal entirely. If there's a scheduled macro release at
9:30 AM, skip this signal for the day.

---

## COMBINED EQUATION — THE INSANE HOME RUN

When BOTH signals align with maximum conditions:

```
HomeRun_score = CIR_score × OIA_carryover × Regime_multiplier

Where:
  CIR_score        = from Signal 1 (closing imbalance from PREVIOUS day)
  OIA_carryover    = 1.0 if today's opening imbalance CONFIRMS yesterday's close direction
                     0.5 if neutral
                     0.0 if contradicts (CANCEL — the reversal isn't happening)

  Regime_multiplier = VIX_scale × Calendar_boost × Sector_concentration

  The "insane home run" fires when:
    1. Yesterday: large sell imbalance at close (CIR long signal)
    2. Overnight: stock drifts higher (inventory premium captured)
    3. Today's open: buy-side imbalance accelerating (OIA confirms reversal)
    4. VIX > 25 (fear premium elevated)
    5. Friday or index rebalance date (calendar premium)

  All five conditions = maximum signal strength.
  Expected combined return: 1-3% over 3-5 days.
```

---

## MULTI-TIMEFRAME SCORING MATRIX

For every signal generated, score the outcome across all 13 timeframes:

```
Timeframe grid:
  T1  = 1 min    (immediate reaction)
  T2  = 3 min    (early confirmation)
  T3  = 5 min    (first real signal — OIA entry point)
  T4  = 10 min   (short-term follow-through)
  T5  = 15 min   (quarter-hour trend)
  T6  = 30 min   (half-hour conviction)
  T7  = 1 hour   (institutional response)
  T8  = 2 hours  (mid-session trend)
  T9  = 3 hours  (half-day move)
  T10 = 1 day    (full session — CIR partial exit)
  T11 = 2 days   (CIR half-life reached)
  T12 = 3 days   (CIR 75% reversal expected)
  T13 = 1 week   (CIR full reversal window)

For each signal event, compute:
  Return(Ti) = (Price(t + Ti) - Price(t_entry)) / Price(t_entry)

Store: signal_id, ticker, date, signal_type (CIR/OIA/HomeRun), entry_price,
       score, VIX, calendar_flag, sector, market_cap,
       return_1m, return_3m, return_5m, return_10m, return_15m, return_30m,
       return_1h, return_2h, return_3h, return_1d, return_2d, return_3d, return_1w
```

This matrix lets us find EXACTLY which timeframes have the best risk-adjusted
returns for each signal type, and calibrate entry/exit timing.

---

## PILLAR II — CRITICAL THINKING

### Leverage Points (Meadows)
1. **Level 7 (Information):** NOI data tells us what institutions are doing
   BEFORE the price reflects it. This is an information asymmetry — the data
   is public but most retail traders don't use it.
2. **Level 6 (Positive feedback):** Imbalance acceleration IS a positive
   feedback loop — more orders in one direction attract more orders.
   Signal 2 (OIA) exploits this directly.

### Inversion — How to guarantee these signals FAIL
1. Trade WITH the closing imbalance instead of against it (reversal becomes a loss)
2. Enter at the open instead of waiting 5 minutes (get whipsawed by opening volatility)
3. Hold the OIA trade past 10:00 AM (signal expires, becomes noise)
4. Ignore VIX context (low-vol regime = small dislocations = not worth the spread)
5. Don't filter for news (informed imbalance = NOT mechanical = don't fade it)
6. Use on NASDAQ-listed stocks (NOI only covers NYSE-listed names)

### Pre-Mortem
Six months from now, the signal system failed because:
1. We didn't cross-reference against Benzinga news and faded an informed imbalance
   (merger announcement). One big loss wiped weeks of small gains.
2. We applied the closing reversal to mega-caps (AAPL, MSFT) where there's too
   much liquidity for 32 bps to materialize.
3. We ran the OIA signal during a major FOMC announcement day and got destroyed
   by the macro event overpowering the imbalance.

---

## PILLAR III — CRYPTOGRAPHY (Hidden Structure)

The surface: "There's a buy/sell imbalance at the auction."
The hidden structure: "The imbalance encodes WHO is trading."

- **Mechanical/uninformed flow** (index funds, ETF rebalancing, pension rebalancing)
  creates imbalances that WILL reverse. This is Signal 1.
- **Informed flow** (merger arb, event-driven hedge funds) creates imbalances
  that WILL NOT reverse. This is the trap.

The cryptanalytic task: distinguish mechanical from informed flow.
**Discriminating tests:**
- Is there Benzinga news on the ticker? → Informed. Skip.
- Is it an index rebalance date? → Mechanical. Strong signal.
- Is the imbalance concentrated in one sector? → Macro event. Reduced signal.
- Is the imbalance scattered across many unrelated tickers? → Mechanical. Strong signal.

---

## PILLAR IV — STATISTICAL MODELING

### Northstar Metrics (to be computed as data accumulates)

Every signal event will be scored after the fact on:
- **Sensitivity:** What % of large moves did we predict? (did we catch the home runs?)
- **Specificity:** What % of no-move days did we correctly skip? (did we avoid noise?)
- **PPV:** When we signaled, what % were actually profitable?
- **NPV:** When we didn't signal, what % were correctly quiet?
- **Brier Score:** Are our confidence scores calibrated?
- **MCC:** Overall quality accounting for all four quadrants

### Calibration Protocol
After 30 trading days of signals:
1. Compute actual returns for each signal at each timeframe
2. Compare predicted vs actual return distributions
3. Apply Calibration-by-Intersection: split into 5 folds, extract critique rules
   per fold, intersect → only keep rules that generalize across all folds
4. Update thresholds if calibration error > 5%

---

## PILLAR V — GAME THEORY

### Players
1. **Passive funds** — create the uninformed flow. They MUST trade at MOC. No choice.
2. **Market makers** — absorb imbalances. Demand overnight premium. Rational actors.
3. **HFTs** — have arbed the opening scalp. Cannot hold overnight. Leave the closing signal alone.
4. **Us** — exploit the structural premium that exists BETWEEN the HFT horizon (microseconds)
   and the passive fund horizon (quarterly). The 1-5 day sweet spot is ours.

### Why this edge persists
This is NOT an anomaly waiting to be arbed. It's a **structural equilibrium:**
- Passive funds MUST trade at MOC (index tracking mandate)
- Market makers MUST be compensated for inventory risk
- HFTs CANNOT hold overnight
- The premium is the price of liquidity provision. Someone must pay it. That someone is the passive fund investor. The premium flows to whoever provides the offsetting liquidity — which is us.

---

## WHAT TO DO TODAY

### Pre-Market (NOW — before 8:30 CT)
The WebSocket capturer is running. NOI data is flowing. Watch for:
- Opening imbalance acceleration signals from 8:25-8:30 CT (9:25-9:30 ET)
- Tickers from the watchlist with 4+ consecutive same-direction accelerating messages
- Size factor >= 1σ

### At 8:35 CT (9:35 ET) — 5 minutes after open
- If OIA signals fired, enter in direction of imbalance
- Set exit at 8:55 CT (9:55 ET) — 20 minute hold max

### At Close (2:50-3:00 CT / 3:50-4:00 ET)
- Monitor closing imbalances for CIR signals
- Rank by |CIR_score|
- Enter top signals at MOC
- Hold overnight minimum, 3-5 days maximum

### Tonight
- Score today's signals on all 13 timeframes as data comes in
- Begin building the historical backtest using S3 flat file data

---

## PEARLS AND PITFALLS

### Pearls
- **The 5-minute delay on OIA is non-negotiable.** Entering at the open gets whipsawed.
- **Mid-caps ($2B-$10B) are the sweet spot.** Enough liquidity to trade, not so much that the imbalance is meaningless.
- **Friday + sell imbalance is the best single day of the week.** Weekend inventory premium stacks on top of reversal.
- **Scattered multi-ticker sell imbalances = mechanical flow = strong CIR signal.** Concentrated in one sector = macro event = weak signal.
- **NOI is NYSE-listed only.** This does not work for NASDAQ-listed stocks.

### Pitfalls
- **Opening scalping is DEAD.** Don't try to capture pennies at the open — HFTs own that.
- **Imbalance ratio > 50% is a RED FLAG, not a bigger signal.** It may indicate a problematic auction or information event.
- **Don't fade informed flow.** Always check Benzinga news before trading against an imbalance.
- **Order flow autocorrelation is 100+ lags.** Today's closing imbalance direction is correlated with tomorrow's. Account for serial correlation in backtests.
