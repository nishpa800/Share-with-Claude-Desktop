# NYSE Order Imbalance (NOI) Alpha Research
## Exhaustive Signal Analysis for Outsized Returns

**Research Date:** 2026-05-26
**Objective:** Identify the TWO most leveraged signals from NYSE order imbalance data -- the Pareto 20% that produce 80% of returns.

---

## EXECUTIVE SUMMARY: THE TWO HOME-RUN SIGNALS

### HOME RUN #1: Closing Auction Imbalance Reversal (The Passive Fund Liquidity Premium)

**The Signal:** When a stock has an extreme MOC (Market-on-Close) order imbalance at 3:50 PM -- driven by passive fund rebalancing -- the price is temporarily dislocated. Go OPPOSITE the imbalance (provide liquidity) and hold 3-5 days for the reversal.

**The Numbers:**
- **13.2 basis points per DAY** risk-adjusted return (Wu, 2019 -- SSRN 3440239)
- **32 bps spread** between top and bottom imbalance deciles at the close (Jegadeesh & Wu)
- **83% of the closing price dislocation reverses within 3-5 days** (Nasduck Substack; Wu 2019)
- **14% of the closing auction return systematically reverses overnight** (Bender, Clapham, Schwemmlein 2024 -- SSRN 4757345)
- For the most extreme stocks (largest auction volumes), **up to 24% of the auction return reverses**

**Why It Works:** Passive funds (ETFs, index funds) use MOC orders to minimize tracking error. This creates massive, predictable, UNINFORMED order flow. Market-on-close volume has grown to >10% of total daily volume. These flows are NOT information-driven -- they are mechanical. The price impact is transitory and reverses as the temporary supply/demand pressure dissipates.

**The Strategy (Long/Short):**
1. At 3:50 PM, observe NYSE closing auction imbalance data
2. Sort stocks by imbalance magnitude (normalized by average daily volume)
3. SHORT stocks with the largest BUY imbalances
4. LONG stocks with the largest SELL imbalances
5. Hold 3-5 days for full reversal
6. The Significant Imbalance flag (>30% of 20-day avg closing size for S&P 500 names) identifies the most extreme opportunities

**Statistical Confidence:**
- Yanbin Wu (2019): Published in Journal of Financial Economics pipeline, t-stats significant
- Effect driven by passive fund growth -- structural, not a fluke
- Slippage compression of 2.4 bps (-25%) after NYSE Significant Imbalance flag change (Oct 2024)
- Validated across NYSE, NASDAQ, and European markets (Bender et al. 2024)

**Decay Rate:** The alpha is persistent because it is STRUCTURAL -- passive fund assets continue to grow. The reversal window is 3-5 days. The signal regenerates daily because passive funds trade MOC every single day.

**Who This Hurts:** Traders who JOIN the imbalance (trade in the same direction as the passive flow) systematically LOSE money. NYSE's own research shows imbalance-joining orders have NEGATIVE VWAC (loss per share).

---

### HOME RUN #2: Overnight Drift from Closing Imbalance (The Inventory Risk Premium)

**The Signal:** When there is a large SELL imbalance at the close, market makers are forced to absorb inventory (become net buyers). They require compensation for holding this overnight risk. The result: stocks with large sell imbalances at the close BOUNCE overnight as market makers offload inventory to Asian/European participants.

**The Numbers:**
- **7.6% annualized overnight return** during Asian hours after negative (sell) closing imbalances (Boyarchenko, Larsen, Whelan -- NY Fed Staff Report 917)
- **12.4% annualized overnight return** during European hours after negative closing imbalances
- Total overnight bounce after sell imbalances: approximately **20% annualized**
- The asymmetry is the key: positive (buy) imbalances show WEAK overnight reversal (-1.5% Asian, -5.1% European)
- S&P 500 futures overnight session generates **2.6% annualized** (>half of total 4.3% close-to-close return) -- concentrated in the 2-3 AM ET window when European markets open

**Why It Works:** This is the market maker inventory risk premium. When selling pressure creates end-of-day order imbalances, market makers become net buyers involuntarily. They hold overnight risk and require compensation. As new participants arrive overnight (Asia open, Europe open), market makers offload inventory at higher prices.

**The Strategy:**
1. At 3:50-4:00 PM, identify stocks with extreme SELL imbalances in the closing auction
2. BUY these stocks at/near the close
3. Hold overnight
4. SELL at the next morning's open (or within first 30 minutes)
5. The effect is STRONGEST after market selloffs (high VIX days)

**Critical Asymmetry:** This only works reliably on the SELL imbalance side. Buy imbalances do NOT produce a symmetric negative overnight drift. This asymmetry arises from time-varying risk aversion -- market participants demand MORE compensation for holding long positions acquired during selloffs.

**Statistical Confidence:**
- NY Fed Staff Report 917 (Boyarchenko, Larsen, Whelan 2021)
- Natural experiment: Japan does not observe daylight savings time, so the Tokyo open shifts one hour exogenously between seasons -- the overnight drift shifts with it, confirming it is driven by liquidity arrival timing
- Hendershott & Seasholes: High-inventory minus low-inventory portfolio returns 10 bps in 1 day, 33 bps in 5 days
- Weekend effect amplifies: 44.4 bps return on high-vs-low inventory portfolio when formed Friday close to next Friday close

**Decay Rate:** This alpha is semi-permanent because it compensates for a real economic risk (overnight inventory holding). As long as market makers exist and require compensation for bearing overnight risk, this premium persists.

---

## DETAILED RESEARCH FINDINGS

### Section 1: Academic Foundation

#### Chordia, Roll, and Subrahmanyam (2002) -- "Order Imbalance, Liquidity, and Market Returns"
- **Source:** Journal of Financial Economics, Vol. 65
- **URL:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=282759
- **Key Finding:** Aggregate daily order imbalance on the NYSE is strongly positively autocorrelated (persists at least 5 daily lags), but market returns show near-zero autocorrelation
- **Signal:** Lagged imbalances bear a positive predictive relation to current-day returns (momentum), which reverses sign after controlling for contemporary imbalance
- **Implication:** The market takes IMMEDIATE account of the forecastable portion of imbalance persistence -- the tradeable signal is in the UNEXPECTED component

#### Chordia and Subrahmanyam (2004) -- "Order Imbalance and Individual Stock Returns"
- **Source:** Journal of Financial Economics, published version of UCLA working paper 36-00
- **URL:** https://www.anderson.ucla.edu/documents/areas/fac/finance/36-00.pdf
- **Key Finding:** Order imbalance predicts next-day individual stock returns
- **Signal Details:**
  - Lagged imbalance positively predicts current-day returns (continuation from autocorrelated imbalance)
  - Contemporaneous imbalance positively relates to returns
  - The strategy of trading on extreme imbalances (>2 standard deviations from zero) for SMALL firms yields the highest average return of **0.55% per day**
  - One standard deviation increase in order imbalance causes 0.07% stock return on NYSE/AMEX, 0.08% on NASDAQ
- **Cross-Sectional:** Effect is STRONGER for illiquid stocks, small-cap stocks
- **Statistical Significance:** p < 0.05 across multiple specifications
- **Decay:** Strongest at 1-day horizon, diminishing at longer lags

#### Hendershott and Seasholes -- "Market Maker Inventories and Stock Prices"
- **Source:** SSRN 890860
- **URL:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=890860
- **Key Findings:**
  - Portfolio based on day-0 inventory: stock declines ~7 bps/day for 3 days prior, drops 30 bps on formation day (total ~50 bps decline), then REVERSES by 10 bps
  - Long high-inventory / Short low-inventory portfolio: **10 bps at 1 day, 33 bps at 5 days**
  - **Weekend amplification: 44.4 bps** on high-vs-low inventory portfolio (Friday close to next Friday close)
  - Inventory effects are COMPLEMENTARY to order imbalance -- both predict reversals independently

### Section 2: The Closing Auction Ecosystem

#### NYSE Closing Auction Mechanics
- **MOC/LOC order deadline:** 3:50 PM ET
- **Imbalance data dissemination:** Starting at 3:50 PM, updates every 1 second
- **Significant Imbalance flag** (new as of Oct 28, 2024):
  - S&P 500 stocks: 30% of 20-day Average Closing Size AND notional >= $200,000
  - S&P 400 stocks: 50% threshold
  - All other stocks: 70% threshold
  - When flagged, additional MOC/LOC orders allowed until 4:00 PM on OPPOSITE side only
- **Average closing auction:** >$18 billion/day notional (2022 data)
- **D-Orders:** 51% of total D-Order insert volume arrives in the last 3 minutes before close
- **Over 60% of NYSE D-Orders** arrive after 3:55 PM

#### Yanbin Wu (2019) -- "Closing Auction, Passive Investing, and Stock Prices"
- **Source:** SSRN 3440239
- **URL:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3440239
- **THE definitive paper on Signal #1**
- **Key Findings:**
  - Passive investing leads to greater MOC order usage (minimizes tracking error)
  - MOC order volume has grown to >10% of entire day's trading volume
  - Price impact from large MOC imbalances is ECONOMICALLY LARGE and TRANSITORY
  - Long/short strategy exploiting reversal: **13.2 bps per day risk-adjusted return**
  - Full reversal takes 3-5 trading days
  - Both passive AND informed traders use MOC orders
  - Informed traders' MOC orders have LASTING price impact (no reversal)
  - Uninformed/passive flow creates the REVERSIBLE component

#### Jegadeesh and Wu -- "Closing Auctions: Nasdaq Versus NYSE"
- **Source:** SSRN 3732955
- **Key Finding:** To-close return spread between top and bottom imbalance deciles: **32 basis points**
- 83% of this spread reverses within 3-5 days
- NASDAQ shows similar patterns

#### Bender, Clapham, and Schwemmlein (2024) -- "Shifting Volumes to the Close"
- **Source:** SSRN 4757345
- **Key Findings (European markets):**
  - Closing auctions account for >1/3 of daily volume in major European markets
  - **14% of closing auction return systematically reverses overnight**
  - For stocks with largest closing auctions: **up to 24% reversal**
  - Main drivers: increasing closing auction volumes, index rebalancing days, high intraday returns

#### NYSE Data Insights -- "Closing Auction: Immediate Market Impact"
- **Source:** https://www.nyse.com/data-insights/closing-auction-immediate-market-impact-price-drift-and-transaction-cost-of-trading
- **Key Numbers:**
  - Russell 1000 stocks: closing auction orders averaging 2.4% of CADV produce immediate price moves of **0.34x the daily average spread**
  - Price drift from order arrival to auction execution: **0.6x-1.7x daily average spread** (R1000)
  - Orders exceeding 0.47% of CADV between 15:57-15:58 trigger **large and persistent market impact**
  - Impact intensifies closer to close: 0.3x spread at 15:55 vs 0.4x spread at 15:59

#### NYSE Data Insights -- Transaction Cost Analysis
- **Source:** NYSE Closing Auction Part 2
- **Imbalance-OFFSETTING orders (contrarian):** VWAC of $0.0075-$0.014 per share GAIN for S&P 1500 stocks
- **Imbalance-JOINING orders:** NEGATIVE VWAC (net loss)
- **Conclusion:** Providing liquidity against the imbalance is systematically profitable; joining the imbalance is systematically unprofitable

### Section 3: The Overnight Drift

#### Boyarchenko, Larsen, and Whelan (2021) -- "The Overnight Drift"
- **Source:** NY Fed Staff Report 917
- **URL:** https://libertystreeteconomics.newyorkfed.org/2021/05/the-overnight-drift-in-us-equity-returns/
- **THE definitive paper on Signal #2**
- **Key Findings:**
  - S&P 500 futures: overnight session (4:15 PM to 9:30 AM) generates **2.6% annualized** (>50% of total 4.3% close-to-close)
  - 2-3 AM ET window (European open): **3.6% annualized**
  - After NEGATIVE (sell) closing imbalances:
    - Asian hours overnight return: **7.6% annualized**
    - European hours overnight return: **12.4% annualized**
    - Total overnight bounce: ~20% annualized
  - After POSITIVE (buy) closing imbalances:
    - Asian hours: **-1.5% annualized** (weak)
    - European hours: **-5.1% annualized** (no meaningful reversal)
  - **CRITICAL ASYMMETRY:** The overnight drift is driven almost entirely by SELL imbalance days
  - Mechanism: Market maker inventory risk premium
  - VIX at 90th percentile: response is **6.1 basis points** per abnormal imbalance event
  - Natural experiment validation: Japan DST shift confirms timing-driven mechanism

#### NY Fed -- "Intraday Market Making with Overnight Inventory Costs"
- **Source:** Staff Report 799
- **Key Insight:** Market makers have limited risk tolerance. When order flows strain equilibrium inventory levels, the market maker adjusts quotes, generating transitory return patterns that reverse as inventory is unwound.

### Section 4: Cross-Sectional Signal Strength

#### Which Stocks Show the Strongest Imbalance Signals?

| Stock Characteristic | Signal Strength | Evidence |
|---------------------|----------------|----------|
| **Small-cap** | STRONGEST absolute returns | 0.55% daily return on extreme imbalance strategy (Chordia & Subrahmanyam) |
| **Illiquid stocks** | STRONGEST predictive power | Order imbalance has strongest predictive power for illiquid stocks |
| **Large-cap (S&P 500)** | MOST STATISTICALLY RELIABLE | Significant alpha concentrated in large-cap despite smaller absolute returns |
| **High closing auction volume** | Strongest reversal effect | Up to 24% of auction return reverses for largest auction stocks |
| **Index constituents** | HIGHEST systematic flow | Passive fund MOC orders concentrate in index members |
| **Rebalance additions/deletions** | EXTREME imbalances | Russell reconstitution: NYSE traded $275B in closing auction alone |

#### Cross-Impact Effects
- **Source:** Cross-Impact of Order Flow Imbalance (arXiv 2112.13213)
- Multi-asset OFI provides additional explanatory power for FUTURE returns (1-min horizon)
- Sector structure matters: Utilities and Real Estate show strongest cross-sector spillover
- ETF order imbalance predicts underlying constituent returns
- Effect decays rapidly -- primarily useful at high-frequency horizons

### Section 5: Opening Auction Signals

#### Opening Imbalance Momentum
- NYSE opens: Imbalance data disseminated every 1 second starting at 8:00 AM ET
- NASDAQ NOII: disseminated starting at 9:28 AM, updated every 5 seconds
- Average NYSE opening auction: **44 million shares, $2.4 billion/day**
- **Opening Cross Momentum Strategy:** Buy stocks with largest buy imbalances at open, short stocks with largest sell imbalances
- First 30 minutes show momentum continuation
- Intraday periodicity: returns in a given 30-minute interval predict returns in the SAME interval the next day
- HOWEVER: Opening imbalance signal is WEAKER than closing because:
  1. Less passive fund flow (MOC dominates LOC)
  2. More information-driven (overnight news)
  3. Higher noise-to-signal ratio

### Section 6: Option Volume Imbalance (Amplifier Signal)

#### Michael, Cucuringu, and Howison -- "Option Volume Imbalance as a Predictor for Equity Returns"
- **Source:** arXiv 2201.09319, SSRN 4019647
- **Key Findings:**
  - Normalized imbalance between option volumes (bullish vs bearish) predicts OVERNIGHT excess market returns
  - **Most predictability stems from high-implied-volatility contracts**
  - **PUT option volumes contain MORE information than calls**
  - **Market-Maker option volumes are the strongest signal source**
  - Stocks with low put-call ratios outperform high put-call ratio stocks by **>40 bps next day** and **>1% over next week**
- **Implication for NOI:** Option volume imbalance can AMPLIFY the equity order imbalance signal. When BOTH equity closing imbalance AND option volume imbalance agree, the signal is much stronger.

### Section 7: Index Rebalance Days (The Extreme Case)

#### Russell Reconstitution -- The Annual Home Run
- **Source:** BMLL Tech, NYSE Data Insights, CME Group
- **Scale:** ~$11 trillion benchmarked to Russell indices
- June 2024 reconstitution: NYSE/NASDAQ traded **$275B / $103B** in closing auctions
- Normal day closing auction: ~$25 billion (7% of value)
- Rebalance day closing auction: **10x normal or more**
- Imbalances are MASSIVE and PREDICTABLE (additions get buy flow, deletions get sell flow)
- 51% of D-Order volume arrives in last 3 minutes
- These are the EXTREME version of Signal #1 -- the passive flow reversal is amplified enormously
- Quarterly rebalances show elevated auction activity 2-3 days before and after the event

### Section 8: Available Data Sources

#### Massive (Polygon) NOI WebSocket
- **Endpoint:** `WS /stocks/NOI`
- **Subscription:** Ticker-specific or `*` for all
- **Key Fields:**
  - `o` -- Imbalance quantity (the unmatched shares)
  - `p` -- Paired quantity (already-matched shares)
  - `b` -- Book clearing price
  - `at` -- Auction time (HHMM EST)
  - `a` -- Auction type: O (Opening), C (Closing), H (Halt), M (Market), P (Pricing), R (Regulatory)
  - `T` -- Ticker
  - `t` -- Unix nanosecond timestamp
- **Coverage:** NYSE-listed securities, real-time
- **Updates:** At market open (9:30 AM), close (4:00 PM), and during halts/mini-auctions
- **Blog Post:** https://massive.com/blog/build-a-nyse-order-imbalance-tracker-with-massives-websocket-api

#### Databento NYSE Imbalance Feeds
- **Cost:** Starting at $1,000/month
- **Datasets:** XNYS.PILLAR, ARCX.PILLAR, XASE.PILLAR
- **Extra Fields vs Massive:**
  - `ind_match_price` -- indicative match price (highest volume subject to collars)
  - `cont_book_clr_price` -- includes continuous book interest
  - `auct_interest_clr_price` -- auction orders only
  - `ssr_filling_price` -- short sale restriction price

#### NYSE Direct Data
- **Imbalance Reference Price:** NYSE Last Sale (adjusted for bid/offer bounds)
- **Paired Quantity:** Volume of better-priced and at-priced shares that can be paired
- **Imbalance Quantity:** Unmatched volume
- **Dissemination:** Every 1 second if changed (starting 3:50 PM for closing, 8:00 AM for opening)

### Section 9: Risk Factors and Implementation Notes

#### What Can Go Wrong
1. **Execution risk:** The alpha is NOT available at zero cost -- you must execute at/near the close, competing with HFTs
2. **Slippage:** Large orders moving against the imbalance will themselves be absorbed into the auction
3. **Informed vs. Uninformed flow:** Not all imbalances are passive/uninformed -- some reflect genuine information
4. **Cancellation risk:** Large imbalances can shrink dramatically in the final seconds as LOC orders offset
5. **Capacity constraints:** The strategy is capacity-limited -- too much capital chasing the reversal will eliminate the premium
6. **Short-selling constraints:** The short side of Signal #1 requires borrow availability

#### When the Signal Is STRONGEST
1. **High VIX / Market selloff days** -- the overnight inventory premium (Signal #2) is amplified
2. **Index rebalance dates** -- the passive flow reversal (Signal #1) is at maximum
3. **Quarter-end / Month-end** -- institutional rebalancing creates predictable flow
4. **Significant Imbalance flag days** -- the NYSE has pre-identified the extreme cases for you
5. **Small-cap / illiquid stocks** -- the price impact is larger, the reversal is more pronounced
6. **Late-arriving D-Orders** -- imbalance changes in last 3 minutes are the most informative

#### When the Signal FAILS
1. **True information events** -- earnings, M&A, guidance changes create imbalances that do NOT reverse
2. **Low-volatility, low-volume days** -- imbalances are small and noise dominates
3. **Crowded trade** -- if too many participants provide liquidity, the premium compresses
4. **Regulatory changes** -- changes to auction mechanics can alter signal properties

### Section 10: Implementation Roadmap

#### Phase 1: Data Capture (Week 1)
- Subscribe to Massive NOI WebSocket for all NYSE tickers (`*`)
- Capture every closing auction imbalance message from 3:45-4:00 PM daily
- Store: ticker, timestamp, imbalance_qty, paired_qty, book_clearing_price, auction_type
- Also capture OHLCV for each ticker (daily bars) for return calculation

#### Phase 2: Signal Construction (Week 2)
- For each ticker each day, compute:
  - `imbalance_ratio = imbalance_qty / (imbalance_qty + paired_qty)`
  - `normalized_imbalance = imbalance_qty / 20_day_avg_daily_volume`
  - `imbalance_direction = sign(imbalance_qty)` (positive = buy imbalance, negative = sell)
  - `imbalance_zscore = (imbalance_qty - 20_day_mean) / 20_day_std`
- Sort cross-section into deciles by normalized_imbalance
- Track whether the NYSE Significant Imbalance flag was triggered

#### Phase 3: Signal #1 Backtest -- Closing Reversal (Week 3)
- Long bottom decile (largest sell imbalances), Short top decile (largest buy imbalances)
- Entry: Close of day T
- Exit: Close of day T+5 (or T+3 for faster turnover)
- Measure: daily return, cumulative return, Sharpe ratio, max drawdown
- Compare: equal-weighted vs. value-weighted vs. imbalance-magnitude-weighted

#### Phase 4: Signal #2 Backtest -- Overnight Drift (Week 3)
- Screen for stocks with extreme SELL imbalances (bottom decile or >2 sigma)
- Entry: Close of day T
- Exit: Open of day T+1
- Measure: overnight return, hit rate, Sharpe ratio
- Stratify by: VIX level, market cap, day of week (Friday amplification)

#### Phase 5: Combined Signal (Week 4)
- When BOTH signals agree (extreme sell imbalance at close on high-VIX day):
  - Buy at close
  - Partial exit at open (capture overnight drift)
  - Remainder held 3-5 days (capture full reversal)
- This is the "insane home run" configuration

---

## BIBLIOGRAPHY

### Foundational Papers
1. Chordia, Roll, Subrahmanyam (2002) -- "Order Imbalance, Liquidity, and Market Returns" -- JFE
2. Chordia, Subrahmanyam (2004) -- "Order Imbalance and Individual Stock Returns" -- JFE
3. Hendershott, Seasholes -- "Market Maker Inventories and Stock Prices" -- SSRN 890860

### Signal #1 Core Papers
4. Wu (2019) -- "Closing Auction, Passive Investing, and Stock Prices" -- SSRN 3440239
5. Jegadeesh, Wu -- "Closing Auctions: Nasdaq Versus NYSE" -- SSRN 3732955
6. Bender, Clapham, Schwemmlein (2024) -- "Shifting Volumes to the Close" -- SSRN 4757345
7. Goyal, Jegadeesh, Wu -- "Price Impact: Continuous Trading, Closing Auctions, and Opening Auctions" -- SSRN 4300417

### Signal #2 Core Papers
8. Boyarchenko, Larsen, Whelan (2021) -- "The Overnight Drift" -- NY Fed Staff Report 917
9. NY Fed Staff Report 799 -- "Intraday Market Making with Overnight Inventory Costs"

### Amplifier Signals
10. Michael, Cucuringu, Howison (2022) -- "Option Volume Imbalance as a Predictor for Equity Returns" -- arXiv 2201.09319
11. Cross-Impact of Order Flow Imbalance in Equity Markets -- arXiv 2112.13213

### Market Microstructure
12. Cartea, Donnelly, Jaimungal (2015) -- "Enhancing Trading Strategies with Order Book Signals" -- Applied Mathematical Finance
13. Byrd et al. -- "The Importance of Low Latency to Order Book Imbalance Trading Strategies" -- arXiv 2006.08682
14. Baltussen, Da, Soebhag -- "End-of-Day Reversal" -- Working paper
15. Della Corte, Kosowski -- "Overnight-Intraday Reversal Everywhere"

### NYSE Data Sources
16. NYSE Opening and Closing Auctions Fact Sheet -- nyse.com
17. NYSE Significant Imbalance Flag -- nyse.com/data-insights
18. NYSE Closing Auction Market Impact Parts 1 & 2 -- nyse.com/data-insights
19. NYSE TAQ Order Imbalance Quick Reference -- nyse.com
20. Databento NYSE Imbalance Feeds -- databento.com/blog/NYSE-imbalance-feeds

### Strategy Resources
21. Nasduck Substack -- "Closing Auction Imbalance Trading" -- nasduck.substack.com
22. Massive Blog -- "Build a NYSE Order Imbalance Tracker" -- massive.com/blog
23. HFT Backtest -- "Market Making with Alpha: Order Book Imbalance" -- hftbacktest.readthedocs.io
24. QuestDB Glossary -- "Order Imbalance Strategies" -- questdb.com/glossary

---

## APPENDIX: Quick-Reference Signal Card

### SIGNAL #1: CLOSING REVERSAL
```
WHEN:   3:50 PM, NYSE Significant Imbalance flag triggers
        OR imbalance_zscore > 2.0 (either direction)
DO:     Trade OPPOSITE the imbalance
        (sell imbalance -> go long, buy imbalance -> go short)
HOLD:   3-5 trading days
TARGET: 13.2 bps/day risk-adjusted (Wu 2019)
        32 bps top-to-bottom decile spread
        83% reversal of price dislocation
BEST:   Index rebalance days, month/quarter end
        Small-cap, illiquid names, high-VIX days
WORST:  True information events (earnings, M&A)
```

### SIGNAL #2: OVERNIGHT DRIFT (SELL IMBALANCE ONLY)
```
WHEN:   3:50 PM, large SELL imbalance detected
        (bottom decile of cross-section, or zscore < -2.0)
DO:     BUY at close
HOLD:   Overnight (sell at next open)
TARGET: 7.6% annualized (Asian hours) + 12.4% (European hours)
        Amplified on high-VIX days (6.1 bps per event at VIX 90th pctile)
BEST:   Market selloff days, high VIX
        Friday close (weekend inventory premium = 44.4 bps)
WORST:  Low volatility regime, when genuine bad news drives the sell imbalance
NOTE:   ASYMMETRIC -- does NOT work reliably for buy imbalances
```

### COMBINED "INSANE HOME RUN" CONFIGURATION
```
WHEN:   High VIX day + Large SELL imbalance at close
        + Friday for bonus weekend premium
        + Index rebalance date for maximum passive flow
DO:     BUY at close
        SELL 50% at next open (capture overnight drift)
        HOLD 50% for 3-5 days (capture full reversal)
EXPECT: Overnight drift + multi-day reversal + weekend premium
        = potentially 50-100+ bps total capture on extreme events
```
