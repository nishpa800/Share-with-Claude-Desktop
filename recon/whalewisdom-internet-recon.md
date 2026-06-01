# WhaleWisdom.com -- Exhaustive Internet-Wide Reconnaissance

**Date:** 2026-05-26
**Author:** Claude Opus 4.7 (autonomous recon agent)
**Scope:** Everything knowable about WhaleWisdom from every corner of the internet

---

## Table of Contents

1. [Company Overview](#1-company-overview)
2. [Product & Features](#2-product--features)
3. [Subscription Tiers & Pricing](#3-subscription-tiers--pricing)
4. [API Documentation (Complete)](#4-api-documentation-complete)
5. [Data Coverage & Update Frequency](#5-data-coverage--update-frequency)
6. [WhaleWisdom Alpha Blog (Strategy Research)](#6-whalewisdom-alpha-blog-strategy-research)
7. [Competitor Comparison](#7-competitor-comparison)
8. [Reddit / Community Intelligence](#8-reddit--community-intelligence)
9. [YouTube & Tutorial Resources](#9-youtube--tutorial-resources)
10. [Academic Papers on 13F Alpha](#10-academic-papers-on-13f-alpha)
11. [GitHub / Open-Source Ecosystem](#11-github--open-source-ecosystem)
12. [SEC EDGAR Direct Access (Backup/Comparison)](#12-sec-edgar-direct-access-backupcomparison)
13. [Trading Strategies Using 13F Data](#13-trading-strategies-using-13f-data)
14. [Data Limitations & Gotchas](#14-data-limitations--gotchas)
15. [Combining 13F With Other Data Sources](#15-combining-13f-with-other-data-sources)
16. [Python/PyPI Packages](#16-pythonpypi-packages)
17. [Apify Scrapers](#17-apify-scrapers)
18. [N-PORT as Complementary Data](#18-n-port-as-complementary-data)
19. [13F-Based ETFs (Real-World Validation)](#19-13f-based-etfs-real-world-validation)
20. [Relevance to Anish's Quant Stack](#20-relevance-to-anishs-quant-stack)

---

## 1. Company Overview

| Field | Value |
|---|---|
| **Name** | WhaleWisdom LLC |
| **URL** | https://whalewisdom.com |
| **Founded** | 2008 |
| **Founders** | Daniel Collins (president, software engineer), Brent Plunkett |
| **HQ** | Scottsdale, AZ |
| **Funding** | $1.42M total (3 rounds, 1 investor) |
| **Mission** | Track institutional 13F/13D/Form 4 filings, make hedge fund intelligence accessible to retail investors |
| **Blog** | https://whalewisdomalpha.com (strategy research blog, separate domain) |

**Source:** [About WhaleWisdom](https://whalewisdom.com/info/about), [Tracxn Profile](https://tracxn.com/d/companies/whale-wisdom/__YEOXd0W_NKgVDXl_bhDWQd6ofwEf4EuDMc43P42SQtg), [LinkedIn - Daniel Collins](https://www.linkedin.com/in/daniel-collins-414086135/)

---

## 2. Product & Features

### 2.1 Core Data Types

| Filing Type | Description | Update Speed |
|---|---|---|
| **13F-HR** | Quarterly institutional holdings (long only, US equities/options/ADRs, >$100M AUM) | Within minutes of SEC release; checks EDGAR every few minutes |
| **Schedule 13D** | Activist investor >5% stake (must file within 10 days of crossing threshold) | Near real-time |
| **Schedule 13G** | Passive investor >5% stake | Near real-time |
| **Form 4** | Insider transactions (officer/director buys/sells, must file within 2 business days) | Near real-time |
| **8-K** | Material events | Near real-time |

### 2.2 Tools & Reports

| Tool | Description | Tier Required |
|---|---|---|
| **13F Backtester** | Build theoretical portfolios from fund 13F filings; control # of holdings (up to 50), filter by sector/market cap/performance, customize rebalancing, weight restrictions. Default: top 10 holdings equal-weight, rebalances 46 days after quarter-end. Prices include dividends/spinoffs (total return). | Free (limited), Standard+ (full) |
| **WhaleScore** | Proprietary fund scoring: risk-adjusted 13F returns over 3 years, updated quarterly, averaged over 4 quarters. Predicts future alpha via regression. Filters: 5-750 holdings, 3+ years history, >20% concentration in top 10. Excludes banks/insurance/pensions. | Standard+ |
| **WhaleIndex 20** | Consensus picks of top WhaleScore funds. Performance: **20.74% annualized since 2006**. Updated quarterly. | Standard+ |
| **WhaleIndex 100** | Broader version: 100 most commonly held stocks among 13F filers. More than doubled S&P 500 over 1/3/5 year periods. | Standard+ |
| **Duplicator** | Clone/replicate any fund's portfolio. Auto-updates with new filings. | Free (limited) |
| **13F Heat Map** | 100 hottest stocks based on latest 13F data. Metrics: # filers increasing/starting position, # decreasing/exiting, inverse change in average ranking. Only stocks held by 5%+ of sampled portfolios qualify. | Free |
| **Consensus Picks** | Select group of funds, see common holdings across all. | Free (5 funds), Standard (10), Pro (50) |
| **Double Down Report** | Identifies underperforming stocks where funds increased holdings (contrarian conviction). | Free |
| **13F Stock Screener** | Filter stocks by: # of 13F holders, % increasing position, avg weight within holding funds, sector, market cap. | Free |
| **Combined Holdings Report** | Merge multiple funds' 13F into single portfolio view. | Pro+ |
| **Fund Performance Search** | Search/filter all 4,200+ funds by performance metrics. | Free |
| **Filer Groups** | Create custom fund groups (e.g., "All Stars"), up to 50 members (Pro). Use for backtesting, consensus, combined holdings. | Standard (10), Pro (50) |
| **Insider Backtester** | Backtest strategies based on Form 4 insider buying signals. Filter by insider type, purchase size, stock price, market cap. | Pro+ |
| **Insider Dashboard** | Real-time Form 4 insider transaction monitoring. | Free |
| **13D/13G Search** | Track activist/passive 5%+ positions. View filing history and average post-filing performance per filer. | Free |
| **Email Alerts** | Per-stock or basket-based alerts for 13F, 13D/G, Insider, 8-K filings. Real-time or daily digest. Configurable triggers (e.g., only when shares sold, % change threshold). | Free (unlimited) |
| **CSV Export Module** | Download all 13F data for a filer across all time periods. Customize columns and quarters. Auto-compressed to ZIP. | Standard+ |
| **Excel Add-in** | Pull 13F/13D/13G data directly into Excel without API knowledge. Available in Microsoft Office Marketplace. | Standard+ |
| **Portfolio Tracker** | Compare personal portfolio against hedge fund benchmarks. | Free |

**Sources:** [WhaleWisdom Features](https://whalewisdom.com/info/features), [DayTradeReview](https://daytradereview.com/whalewisdom-review/), [BullishBears Review 2026](https://bullishbears.com/whalewisdom-review/), [Getting Started](https://whalewisdom.com/info/getting_started), [Whale University](https://whalewisdom.com/help/whale_university)

---

## 3. Subscription Tiers & Pricing

| Tier | Cost | Fund Limit | API Quota | Key Features |
|---|---|---|---|---|
| **Free** | $0 | 5 funds at a time | No API | Last 9 quarters (2 years) of 13F data. Most reporting/backtesting tools. Unlimited email alerts. |
| **Standard** | $90/quarter or $300/year | 10 funds | 50 filers + 50 stocks per quarter | 13F data back to 2001. WhaleIndex. WhaleScore. CSV export. Excel add-in. |
| **Pro** | $150/quarter or $500/year | 50 funds | 200 filers + 200 stocks per 90 days | Combined holdings report. Full Insider Backtester. Advanced backtesting. Up to 50 members per filer group. |
| **Enterprise** | Custom (several thousand/year) | Unlimited | Unlimited API calls | Everything in Pro + `filing_data_feed` + `condensed_data_feed` live API commands. Nightly FTP file delivery (13F + 13D/G). Bulk Schedule 13D/G data. |

**Anish's tier:** Pro ($500/yr, 3-month renewals, active since 2026-05-18). Gets 200 stocks/filers historical 13F data every 90 days.

**Source:** [Subscription Info](https://whalewisdom.com/info/subscription_info), [Enterprise White Paper](https://s3.amazonaws.com/whalewisdom/whitepaper/EnterpriseWhitePaper.pdf)

---

## 4. API Documentation (Complete)

### 4.1 Authentication

| Parameter | Description |
|---|---|
| **Base URL** | `https://whalewisdom.com/shell/command.json` |
| **Method** | GET |
| **Auth scheme** | HMAC-SHA1 |
| **`args`** | JSON object containing command + parameters |
| **`api_shared_key`** | Your shared key (env: `WHALEWISDOM_SHARED_KEY`) |
| **`api_sig`** | HMAC-SHA1 digest of the `args` string, base64-encoded, using your secret key |
| **`timestamp`** | ISO 8601 UTC (some implementations include this in the args) |

**Request format:**
```
GET https://whalewisdom.com/shell/command.json?args={JSON}&api_shared_key={KEY}&api_sig={SIG}
```

**Output formats:** `.json`, `.csv`, `.html` (append to `command` in URL)

**Rate limit:** 20 requests per minute

### 4.2 Known API Commands

#### `quarters`
- **Purpose:** List all 13F filing quarters in the database and which ones your account can access
- **Parameters:** `{"command":"quarters"}`
- **Output:** Quarter IDs, dates, availability flags
- **Required for:** Most other commands use quarter IDs

#### `filer_lookup`
- **Purpose:** Find a 13F filer's ID by partial name or CIK
- **Parameters:** `{"command":"filer_lookup","name":"Berkshire"}` or `{"command":"filer_lookup","cik":"1067983"}`
- **Response:** Filer ID, name, CIK
- **Max records:** 1,000

#### `stock_lookup`
- **Purpose:** Find a stock's ID by ticker symbol or name
- **Parameters:** `{"command":"stock_lookup","symbol":"GOOGL"}`
- **Response:** Stock ID, name, symbol, status (active/delisted)

#### `holdings`
- **Purpose:** Get all holdings for one or more filers (from 13F filings)
- **Parameters:** `{"command":"holdings","filer_ids":[349,2182],"include_13d":1}`
- **Key params:** `filer_ids` (array), `include_13d` (0/1), quarter_id (optional)
- **Tier limits:** 50 filers/quarter (Standard), 200/90 days (Pro), unlimited (Enterprise)

#### `holders`
- **Purpose:** Get all 13F holders of a stock or group of stocks
- **Parameters:** `{"command":"holders","stock_ids":[195,411],"include_13d":1}`
- **Key params:** `stock_ids` (array), `include_13d` (0/1)
- **Tier limits:** 50 stocks/quarter (Standard), 200/90 days (Pro)

#### `stock_comparison`
- **Purpose:** Quarterly comparison of 13F holders of a specific stock
- **Parameters:** `{"command":"stock_comparison","stockid":3598,"q1id":39,"q2id":40}`
- **Key params:** `stockid`, `q1id`, `q2id` (quarter IDs from `quarters` command)

#### `holdings_comparison`
- **Purpose:** Quarterly comparison of a filer's 13F holdings between two quarters
- **Parameters:** `{"command":"holdings_comparison","filerid":349,"q1id":39,"q2id":40}`
- **Key params:** `filerid`, `q1id`, `q2id`, `order`, `dir`, `filter` (e.g., CALL/PUT)

#### `export`
- **Purpose:** Export entire 13F holdings history for a single filer
- **Parameters:** `{"command":"export","quarters":[40,41,42],"columns":[16,17,18],"filer_id":349,"output":1,"email":"test@test.com"}`
- **Key params:** `filer_id`, `quarters` (array), `columns` (array of column IDs), `output`, `email`

#### `filing_data_feed` (Enterprise only)
- **Purpose:** Live data feed of new 13F filings as they're processed
- **Tier:** Enterprise only
- **Notes:** Not available to Standard/Pro subscribers

#### `condensed_data_feed` (Enterprise only)
- **Purpose:** Condensed version of filing data feed
- **Tier:** Enterprise only

### 4.3 Credentials (Anish's env)

```
WHALEWISDOM_SHARED_KEY    -- api_shared_key parameter
WHALEWISDOM_SECRET_KEY    -- HMAC-SHA1 signing key
WHALEWISDOM_BASE_URL      -- https://whalewisdom.com/shell/command.json
```

**Sources:** [API Help](https://whalewisdom.com/shell/api_help), [API Documentation](https://whalewisdom.com/help/api), [Alteryx Community](https://community.alteryx.com/t5/Alteryx-Designer-Desktop-Discussions/API-Connections-to-Whale-Wisdom-Encrypting-using-HMAC-SHA1-and/td-p/150176), [npd-whale-wisdom PyPI](https://pypi.org/project/npd-whale-wisdom/)

---

## 5. Data Coverage & Update Frequency

| Metric | Value |
|---|---|
| **Historical depth** | March 31, 2001 quarter (free: last 9 quarters only) |
| **Filer count** | 4,200+ funds (as of backtester documentation) |
| **Update cadence** | Checks SEC EDGAR every few minutes; new filings imported within minutes |
| **Filing deadline** | 45 days after quarter-end (if weekend, next Monday) |
| **Heat Map/WhaleIndex/Statistics** | Updated 1-2 days AFTER the 13F deadline |
| **Data source** | SEC EDGAR, entirely automated parsing (in-house, no human intervention) |
| **Data quality** | Automated; margin for error acknowledged; links to original SEC filings provided for verification |
| **Filing formats parsed** | Pre-Q3 2013: fixed-width TXT; Post-Q3 2013: XML |
| **Confidential treatment** | Some managers request delayed disclosure (3-12 months) to hide positions being accumulated/unwound |

**Key deadlines for 2026:**
- Q1 2026 (ends 3/31): 13F due by May 15, 2026
- Q2 2026 (ends 6/30): 13F due by August 14, 2026
- Q3 2026 (ends 9/30): 13F due by November 14, 2026
- Q4 2026 (ends 12/31): 13F due by February 14, 2027

**Source:** [WhaleWisdom FAQ](https://whalewisdom.com/faq), [SEC 13F FAQ](https://www.sec.gov/rules-regulations/staff-guidance/division-investment-management-frequently-asked-questions/frequently-asked-questions-about-form-13f)

---

## 6. WhaleWisdom Alpha Blog (Strategy Research)

WhaleWisdom maintains a separate blog at https://whalewisdomalpha.com with detailed strategy research. Key articles:

### 6.1 Biotech Insider Strategy
- **Finding:** Biotech/medtech insiders are the "smartest of the smart money"
- **Backtest:** Buying when C-level/directors/10% owners disclose >$100K purchases within 3 days, buying on close one day after Form 4 filing, stocks >$1/share, market cap <$20B
- **Result:** 7,196% return (47.3% annualized) since beginning of 2008
- **Source:** [WhaleWisdom Alpha - Biotech Insiders](https://whalewisdomalpha.com/biotech-insiders-the-smartest-of-the-smart-money/)

### 6.2 Activist 13F Strategy (26.3% Annual)
- **Finding:** Following all activist managers' 13F filings (not 13D) produces better returns
- **Method:** Hold 10 stocks = activists' highest conviction positions, rebalance quarterly
- **Result:** 26.3% annualized since 2009 (690%+ cumulative through April 2018)
- **Key insight:** Entries on 13F filing dates avoid the volatility spike of 13D filings
- **Extended backtest:** 21.6% annualized, 2,705% cumulative since 2001
- **Source:** [WhaleWisdom Alpha - Activist Strategy](https://whalewisdom.com/articles/this-strategy-returned-26-3-a-year-since-2009-finding-hidden-opportunities-in-activists-13f-filings/)

### 6.3 13D/13G Profit Strategies
- **Finding:** 13D/G filings more timely than 13F (10-day filing requirement vs 45-day)
- **Caution:** Don't buy immediately after 13D -- stock often already advanced by filing date
- **Best approach:** Use WhaleWisdom's performance data per filer to identify which activist filers have best post-filing track records
- **Source:** [WhaleWisdom Alpha - 13D/13G Smart Money](https://whalewisdomalpha.com/13d-13g-filings-profit-from-the-smart-money/)

### 6.4 Insider Trades vs Analyst Recommendations
- **Finding:** Insiders with "skin in the game" produce better signals than sell-side analysts
- **Source:** [WhaleWisdom Alpha - Insider vs Analyst](https://whalewisdomalpha.com/insider-trades-and-analyst-recommendations/)

---

## 7. Competitor Comparison

### 7.1 Direct Competitors

| Platform | Strengths | Weaknesses | Pricing | Best For |
|---|---|---|---|---|
| **WhaleWisdom** | WhaleScore, backtester, heatmap, 13D/G + insider, API, Excel add-in, data since 2001 | Automated parsing (margin for error), 45-day lag | $0-500/yr | Clone investing, backtesting, comprehensive 13F analysis |
| **Fintel** | Institutional ownership depth, Fund Sentiment Score, 13D/G integration, global reach, fast EDGAR updates | More expensive, less backtesting capability | $24.99-99.99/mo | Institutional ownership deep dives, short interest |
| **DataRoma** | Curated elite investors only (Buffett, Ackman, Pabrai), manually verified against EDGAR | Small fund universe, no API, limited customization | Free | Tracking legendary long-term value investors |
| **GuruFocus** | Deep fundamental analysis (DCF, Graham Number), valuation models, predictability rank | More fundamental than institutional flow focused | $449/yr+ | Value investing research combined with guru tracking |
| **HedgeFollow** | 10,000+ institutional investors tracked, clean interface | Less analytical depth | Free (mostly) | Quick hedge fund portfolio lookups |
| **Unusual Whales** | Congressional trading (STOCK Act), 13F, dark pool, options flow, crypto, news all in one | Expensive for full access, less 13F-specific depth | $19.99-49.99/mo | Multi-signal traders wanting options + institutional flow |
| **13F.info** | Clean viewing interface for SEC filings, open source | Limited analytics | Free | Simple 13F viewing |
| **TIKR** | 7 best free tracking tools comparison, clean UI | Free tier limitations | Freemium | Portfolio monitoring |
| **SEC-API.io** | 18M+ filings since 1993, 300ms indexing, full-text search, streaming, PDF rendering | API-only (no GUI analysis tools), requires dev skills | $49-199/mo | Developers building custom 13F pipelines |

### 7.2 Institutional-Grade Platforms
- **Bloomberg Terminal / FactSet / Refinitiv:** Real-time institutional holdings, no filing lag, short interest data. Cost: $24K+/year
- **Dakota Marketplace:** 13F filings + SEC-API integration + live calls + IC notes. Cost: $16,500/user/year
- **Novus:** Hedge fund analytics platform, public ownership indices

**Sources:** [Dakota Comparison](https://www.dakota.com/resources/blog/whalewisdom-opportunity-hunter-sec-api-which-is-right-for-you), [FindMyMoat Fintel vs WW](https://www.findmymoat.com/vs/fintel-vs-whalewisdom), [RhinoInvestory Alternatives](https://rhinoinvestory.com/dataroma-alternatives), [TIKR Blog](https://www.tikr.com/blog/7-best-free-websites-to-track-hedge-fund-portfolios)

---

## 8. Reddit / Community Intelligence

### 8.1 Common Use Cases (aggregated from r/investing, r/algotrading, r/SecurityAnalysis, Quora)

- **Clone investing:** Most popular use -- replicate Buffett, Ackman, Druckenmiller quarterly
- **Idea generation:** "Ideas often surface on WhaleWisdom before financial social media picks them up"
- **Consensus filtering:** When 3+ respected managers independently buy the same stock, it's a high-conviction signal
- **Contrarian screening:** WhaleWisdom's Double Down report finds stocks where funds are buying into weakness

### 8.2 Community Sentiment
- **Positive:** Best free 13F tool, WhaleScore is genuinely useful for fund selection, backtester is unique among free/cheap tools
- **Neutral:** Data lag is inherent to 13F, not WhaleWisdom's fault
- **Negative:** Occasional parsing errors in automated system; Pro tier required for serious analysis; no short position visibility

### 8.3 Community Strategy Ideas
- Track "crowded trades" (too many funds in same name) as risk signal
- Monitor de-crowding phases (funds quietly trimming) as leading indicator
- Combine 13F positioning with price/volume for phase identification:
  - Both rising = healthy accumulation
  - Price up + ownership down = distribution
  - Price down + ownership up = contrarian accumulation
  - Both falling = capitulation

**Sources:** [Quora - 13F Aggregators](https://www.quora.com/Is-there-a-good-website-that-aggregates-13F-filings-to-track-hedge-fund-managers)

---

## 9. YouTube & Tutorial Resources

### 9.1 WhaleWisdom Official
- **Tutorial Videos:** Available at https://whalewisdom.com/help/tutorial_videos
- **Whale University:** https://whalewisdom.com/help/whale_university
- **Topics covered:** Stock lookup, filer lookup, account creation, premium features, backtesting

### 9.2 Third-Party YouTube Content
- **"Stock Market Whales - Hedge Funds & Institutional Activity"** - YouTube video covering WhaleWisdom fundamentals
- Multiple channels cover 13F analysis using WhaleWisdom alongside EDGAR directly

### 9.3 Whitepapers
- **Backtesting Whitepaper:** [CloudFront PDF](http://cloudfront.whalewisdomcdn.com/whitepaper/WhaleWisdom_Backtesting.pdf) (TLS issues, also at [whalewisdom.com/whitepapers/backtesting](https://whalewisdom.com/whitepapers/backtesting))
- **Enterprise White Paper:** [S3 PDF](https://s3.amazonaws.com/whalewisdom/whitepaper/EnterpriseWhitePaper.pdf)
- **13Fs Explained:** [CloudFront PDF](http://cloudfront.whalewisdomcdn.com/whitepaper/WhaleWisdom.com+13Fs+Explained.pdf)

**Source:** [Tutorial Videos](https://whalewisdom.com/help/tutorial_videos), [YouTube](https://www.youtube.com/watch?v=jTfYHIhS-Hs)

---

## 10. Academic Papers on 13F Alpha

### 10.1 Seminal Papers

#### "Best Ideas" -- Cohen, Polk, Silli (LSE/Harvard)
- **Finding:** Stocks where active managers display most conviction outperform market by **2.8-4.5% per year** depending on benchmark
- **Key insight:** The vast majority of other stocks managers hold do NOT exhibit significant outperformance -- only the highest-conviction "best ideas" generate alpha
- **Implication:** Concentrated portfolios > diversified portfolios for alpha
- **URL:** [LSE Paper](https://personal.lse.ac.uk/polk/research/bestideas.pdf), [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1364827)

#### "Systematic 13F Hedge Fund Alpha" -- Angelini, Iqbal, Jivraj (Lancaster/Imperial, 2019)
- **Finding:** Must select managers with longer-term views (qualitative fund classification)
- **Strategy:** Combines conviction + consensus of such managers
- **Performance:** Outperforms S&P 500 by **3.80% average**, Sharpe ratio of **0.75**, Q1 2004 - Q2 2019
- **Key innovation:** First in academic literature to use qualitative fund classifications to separate long-term vs short-term managers
- **URL:** [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3459526), [Lancaster PDF](https://wp.lancs.ac.uk/fofi2020/files/2020/04/FoFI-2020-090-Farouk-Jivraj.pdf)

#### "Alpha Cloning -- Following 13F Fillings" -- Quantpedia
- **Performance:** Indicative annual return **20.21%**, monthly alpha **1.26%** (geometrically annualized)
- **Method:** Invest in securities with broadest managerial consensus, 10-100 stocks, rebalance quarterly
- **Backtest period:** 1991-2005
- **Recent extension (Schroeder, 2023):** Top-quartile cloned portfolios exceeded S&P 500 by **24.3% annualized risk-adjusted**
- **URL:** [Quantpedia](https://quantpedia.com/strategies/alpha-cloning-following-13f-fillings)

### 10.2 Machine Learning on 13F Data

#### Deep Reinforcement Learning -- Fleiss et al. (Rebellion Research)
- **Method:** Deep RL on SEC 13F holdings data, feature extraction for portfolio construction
- **Performance:** **21% annualized return**, Sharpe ratio **1.8**
- **URL:** [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3958478), [Rebellion Research](https://www.rebellionresearch.com/constructing-alpha-generating-equity-portfolios-from-sec-data-using-deep-reinforcement-learning-feature-extraction)

#### ML Portfolio Construction -- Fleiss, Cui, DiPietro
- **Method:** Feature extraction from 13F data to predict stock price movements
- **Performance:** 15.0% and 19.8% annualized (vs 9.5% S&P 500)
- **URL:** [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4173243)

#### ML for Investment Manager Performance -- Chen, Song, Qian, Fleiss
- **Method:** ML applied to predict investment manager performance by analyzing holdings across sectors
- **URL:** [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4352145)

### 10.3 Alpha Decay Research

#### "Why Do Institutions Delay Reporting Their Shareholdings?" -- Musto et al. (Wharton)
- **Finding:** If managers intend to trade in same direction next quarter, they delay reporting to prevent front-running
- **Implication:** Delayed 13F filings are themselves an information signal
- **URL:** [Wharton PDF](https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2014/04/13-15.musto_.pdf)

#### "Why Do Hedge Funds Avoid Disclosure?" -- Confidential 13F Analysis
- **Finding:** Hedge funds request confidential treatment to hide profitable ideas; delayed positions outperform non-delayed ones
- **URL:** [ResearchGate](https://www.researchgate.net/publication/228963032_Why_Do_Hedge_Funds_Avoid_Disclosure_Evidence_from_Confidential_13F_Filings)

#### "13F Blind Spot" -- Exponential Tech
- **Finding:** The REAL lag is not 45 days -- it's up to **135 days** (quarter-end snapshot + 45-day filing deadline = data describes positions from 45-135 days ago)
- **URL:** [Exponential Tech](https://www.exponential-tech.ai/post/13f-blind-spot)

### 10.4 Insider Trading Research

#### Lakonishok and Lee (2002) -- Review of Financial Studies
- **Finding:** Stocks with heavy insider buying outperformed market by **4.8% over 12 months**

#### Cohen, Malloy, Pomorski (2012) -- Journal of Finance
- **Finding:** Distinguished "routine" insider trades (calendar-based, predictable) from "opportunistic" (irregular, precedes news). Opportunistic trades are the signal.

#### SEC Form 13F-HR Statistical Investigation (2022)
- **Finding:** Statistical analysis of trading imbalances and profitability around 13F filings
- **URL:** [arXiv](https://arxiv.org/pdf/2209.08825)

**Effective 13F strategy benchmarks (academic consensus):**
- Sharpe ratio > 0.6
- Information ratio > 0.4
- Alpha persistence across market regimes

---

## 11. GitHub / Open-Source Ecosystem

### 11.1 SEC EDGAR 13F Tools

| Repo | Stars | Language | Purpose |
|---|---|---|---|
| **[edgartools](https://github.com/dgunning/edgartools)** | High | Python | **Best-in-class.** MIT-licensed. 13F, 10-K, 8-K, XBRL, Form 3/4/5, ADV. `filing.obj()` gives structured Python objects. `compare_holdings()`, `holding_history(periods=4)`. Handles both TXT (pre-2013) and XML formats. Free, no API key needed. |
| **[sec-api-python](https://github.com/janlukasschroeder/sec-api-python)** | Medium | Python | SDK for sec-api.io. 20M+ filings, insider trades, 13F holdings, XBRL-to-JSON, real-time streaming. Requires paid API key. |
| **[hedge-fund-tracker](https://github.com/dokson/hedge-fund-tracker)** | Low | - | 13F + 13D/G + Form 4 combined. LLM-based "Promise Scores." |
| **[sec-13f-filings](https://github.com/toddwschneider/sec-13f-filings)** | Medium | - | Cleaner viewing of SEC 13F data, period comparison, holding history. |
| **[13F-Rebalancing-Portfolio](https://github.com/samsonq/13F-Rebalancing-Portfolio)** | Low | Python | ML-based portfolio rebalancing using 13F data. |
| **[EDGAR-Parsing](https://elsaifym.github.io/EDGAR-Parsing/)** | Low | Python | Open-source 13F parsing from EDGAR, 1999-2020 coverage. |
| **[Stock-Analyser-M](https://github.com/beccadsouza/Stock-Analyser-M)** | Low | Java | Jersey REST API serving investment insights from WhaleWisdom data. |
| **[fundholdings](https://github.com/cpackard/fundholdings)** | Low | Python | Web crawler for 13F-HR holdings from SEC EDGAR. |
| **[Edgar_Scraper](https://github.com/codeLovingYogi/Edgar_Scraper)** | Low | Python | XML and ASCII text parser for EDGAR 13F filings. |
| **[sec-web-scraper-13f](https://github.com/CodeWritingCow/sec-web-scraper-13f)** | Low | Python | Parsing 13F mutual fund holdings from SEC. |
| **[SEC-13F](https://github.com/girishji/SEC-13F)** | Low | Python | Scrape Form 13F-HR to track trading patterns. |

### 11.2 WhaleWisdom-Specific Tools

- **No official WhaleWisdom GitHub repository found.** WhaleWisdom does not appear to have any open-source code.
- PyPI packages exist (see Section 16).

### 11.3 Key Recommendation: EdgarTools

EdgarTools is the strongest option for building a direct-from-EDGAR pipeline as a backup/comparison to WhaleWisdom:
- Free, MIT-licensed, actively maintained
- `pip install edgartools`
- Structured Python objects with properties and DataFrames
- Quarter-over-quarter comparison built in
- Multi-quarter trend analysis
- Handles both legacy TXT and modern XML formats
- No API key or subscription required

**Source:** [EdgarTools Docs](https://edgartools.readthedocs.io/en/stable/13f-filings/), [EdgarTools GitHub](https://github.com/dgunning/edgartools)

---

## 12. SEC EDGAR Direct Access (Backup/Comparison)

### 12.1 Official SEC 13F Data Sets

The SEC provides quarterly bulk download data sets at:
- **URL:** https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets
- **Format:** XML-extracted, flattened tabular data
- **Coverage:** May 2013 to present (XML submissions only)
- **Update cadence:** Quarterly (run after February, May, August, November)
- **Documentation:** [Form 13F Readme PDF](https://www.sec.gov/files/form_13f_readme.pdf)

### 12.2 Data Structure

The SEC 13F data set contains up to 7 files per quarter:
- **SUBMISSION:** Primary key = ACCESSION_NUMBER; includes filer/report metadata
- **COVERPAGE:** Cover page details (manager info, CIK, CRD, report type)
- **INFOTABLE:** The actual holdings data (CUSIP, value, shares, put/call)

### 12.3 Filing Format History
- **Pre-Q3 2013:** Fixed-width TXT format (harder to parse)
- **Post-Q3 2013:** XML format (required by SEC)
- **Container:** SGML wrapper with SEC-specific tags; `.txt` files contain complete submission

### 12.4 EDGAR APIs

| API | Purpose | Latency |
|---|---|---|
| **EDGAR Full-Text Search** | Search all filings since 2001 by content | < 60 seconds after filing |
| **EFTS (EDGAR Filing Text Search)** | Free full-text search | Near real-time |
| **sec-api.io** | Commercial API, 18M+ filings since 1993 | **300 milliseconds** after filing |

### 12.5 13F Securities List
The SEC maintains an official list of securities that must be reported on 13F:
- Published quarterly
- Available at: https://www.sec.gov/divisions/investment/13flists.htm
- ~15,000 securities typically

**Source:** [SEC 13F Data Sets](https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets), [EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)

---

## 13. Trading Strategies Using 13F Data

### 13.1 Clone Investing / Coattail Investing

**Method:** Replicate top holdings of proven outperformers.

**Best practices:**
- Focus on managers with **long-term horizons** (5+ year holding periods) -- 45-day lag matters less
- Use WhaleScore to identify consistently outperforming managers
- Equal-weight top 10 holdings, rebalance 46 days after quarter-end
- WhaleWisdom backtester default: top 10 by % weight, equal-weight, rebalance day after filing
- Example: Copying Coatue Management's top 10 over 10 years = 300%+ return (3x S&P 500)

**Key academic backing:**
- Cohen/Polk/Silli: Best ideas outperform by 2.8-4.5%/year
- Angelini/Iqbal/Jivraj: Sharpe 0.75, 3.8% over S&P
- Quantpedia: 20.21% annualized indicative return

### 13.2 Whale Convergence (Multi-Manager Consensus)

**Method:** Buy when 3+ uncoordinated top-tier managers buy the same stock in the same quarter.

**Signal strength:** Three or more funds converging independently is "the single most differentiating concept in 13F analysis."

**Implementation:** Use WhaleWisdom Consensus Picks tool with curated filer group.

### 13.3 Crowded Trade Detection / De-Crowding

**Method:** Monitor institutional concentration; high crowding = liquidation risk.

**Signals:**
- Rising: Many funds accumulating = structural bid (bullish when calm, risky in stress)
- De-crowding: Funds quietly trimming = leading indicator of weakness
- 2021 meme stock events demonstrated violent crowded position unwinding

**Implementation:** Use WhaleWisdom holders command to count institutional holders per stock; track quarter-over-quarter changes.

### 13.4 New Position Detection vs. Conviction Signals

**Signal hierarchy (strongest to weakest):**
1. **Cluster insider buying** (3+ insiders within 10 days) -- strongest
2. **New position from high-WhaleScore manager** in undervalued stock
3. **Significant position increase** (>50% increase in shares) by respected manager
4. **Whale convergence** (3+ managers independently buying)
5. **Existing large position maintained** (no change = thesis intact but stale)
6. **Decreased position** -- liquidation signal
7. **Sold out entirely** -- strongest sell signal

### 13.5 Activist 13F Strategy

**Method:** Follow activist managers' 13F filings (NOT 13D filings).

**Why 13F > 13D for entries:**
- 13D filings create volatility spike (stock often already up)
- 13F entries are quieter, better entry prices
- 26.3% annualized since 2009 following this approach

### 13.6 Form 4 Insider Buying Strategy

**Key filters for high-conviction insider signals:**
- C-level executives, directors, or 10%+ owners
- Purchase size > $100K
- Stock price > $1
- Market cap: $500M-$20B sweet spot (academic research shows strongest signal here)
- Cluster buying (3+ insiders within 10 days)
- **Distinguish "routine" from "opportunistic"** trades (Cohen/Malloy/Pomorski 2012)

**Backtest results:**
- Lakonishok/Lee: Insider buying stocks outperform by 4.8% over 12 months
- WhaleWisdom Insider Backtester biotech strategy: 47.3% annualized since 2008

### 13.7 Phase Detection Overlay

**Combine 13F ownership trend with price action:**

| Price Trend | Ownership Trend | Phase | Action |
|---|---|---|---|
| Up | Up | Healthy accumulation | Hold/Add |
| Up | Down | Distribution | Trim/Hedge |
| Down | Up | Contrarian accumulation | Watch for reversal |
| Down | Down | Capitulation | Avoid |

### 13.8 Sector Rotation via 13F

**Method:** Aggregate institutional flows by sector to detect capital rotation waves.
- Persistent positive flows precede sector outperformance
- Aligns with macro narratives (monetary policy, inflation, geopolitics)

---

## 14. Data Limitations & Gotchas

### 14.1 What 13F Does NOT Include

| Excluded | Why It Matters |
|---|---|
| **Short positions** | Only see long side of pair trades; complete picture missing |
| **Cash positions** | Can't assess cash-to-equity ratio / risk posture |
| **Foreign securities** | International holdings invisible; misleading for global macro funds |
| **Commodities** | No exposure visibility |
| **Open-end mutual fund shares** | Not 13F securities |
| **Cryptocurrency** | Not reportable |
| **Most derivatives** | Unless options on 13F securities |
| **Fixed income** | Bonds/treasuries not included |
| **Private investments** | PE/VC not visible |

### 14.2 Timing Gotchas

| Issue | Detail |
|---|---|
| **45-day delay** | Filing deadline is 45 days after quarter-end |
| **135-day effective lag** | Quarter-end snapshot + 45-day deadline = data describes positions 45-135 days old |
| **Intra-quarter trading invisible** | Fund could have bought and sold within the quarter |
| **No trade timing** | Unknown when positions were opened/closed |
| **Confidential treatment** | Some positions delayed 3-12 months via SEC confidential treatment requests |
| **Strategic delay** | Funds delay filing when they plan to continue trading in same direction |
| **Weekend rule** | If deadline falls on weekend, filings due next Monday |

### 14.3 Data Quality

| Issue | Detail |
|---|---|
| **Automated parsing** | WhaleWisdom acknowledges margin for error |
| **Filing errors** | Filers themselves make mistakes |
| **CUSIP mapping** | CUSIPs can change (corporate actions) |
| **Manager changes** | Mergers, name changes distort continuity |
| **AUM threshold** | Only managers with >$100M in qualifying securities must file |
| **Small positions** | Some managers only report positions >10,000 shares or >$200K |

### 14.4 Alternative: N-PORT for Mutual Funds/ETFs

N-PORT filings are **monthly** (vs quarterly 13F), filed within **30 days** (vs 60), and disclose **complete portfolio** including cash, shorts, foreign, treasuries. However, only covers registered investment companies (mutual funds/ETFs), not hedge funds.

---

## 15. Combining 13F With Other Data Sources

### 15.1 Data Source Synergies for Anish's Stack

| Data Source | What It Adds | Available To Anish? |
|---|---|---|
| **NYSE Order Imbalances (NOI)** | Real-time buy/sell pressure; confirms whether institutional accumulation/distribution is happening NOW | Yes -- Massive $49/mo add-on |
| **Options Flow** | Leading indicator of institutional direction; large OTM call/put sweeps signal conviction | Via Massive options data |
| **Dark Pool Prints** | Large off-exchange institutional block trades; hidden positioning | Via Massive |
| **Benzinga News** | Catalyst identification; correlate filings with corporate events | Yes -- Massive subscription |
| **13D/13G Filings** | Activist positions (more timely than 13F, 10-day requirement) | Yes -- WhaleWisdom |
| **Form 4 Insider** | Insider buying clusters; 2-day filing requirement = near real-time | Yes -- WhaleWisdom |
| **SEC EDGAR Direct** | Backup data source; verification of WhaleWisdom parsing | Free, via EdgarTools |
| **Price/Volume (Massive)** | Phase detection overlay (price trend + ownership trend) | Yes |

### 15.2 Multi-Signal Confluence Framework

**Strongest setup (maximum confluence):**
1. WhaleWisdom shows 3+ high-WhaleScore funds adding NEW positions in same stock (whale convergence)
2. Insider buying cluster in same stock (Form 4, 3+ insiders within 10 days)
3. NOI data shows persistent buy-side imbalances
4. Options flow shows large OTM call sweeps
5. Dark pool prints confirm large block buys
6. Price holding support / in accumulation phase
7. Benzinga news shows positive catalyst approaching

**This is the 13F version of Anish's Holy Grail confluence approach.**

---

## 16. Python/PyPI Packages

### 16.1 WhaleWisdom-Specific

| Package | Version | Status | Notes |
|---|---|---|---|
| **[npd-whale-wisdom](https://pypi.org/project/npd-whale-wisdom/)** | 0.2.4 (Jan 2022) | Inactive | `call_api()` function, uses `WW_SHARED_KEY` + `WW_SECRET_KEY` env vars. MIT license. Author: Max Leonard. Hosted on Azure DevOps. |
| **[whalewisdom-holdings](https://pypi.org/project/whalewisdom-holdings/)** | Unknown | **Inactive** (no updates in 12 months, security vulnerability in indirect dependency) | 65 downloads/week. Retrieving holdings from WhaleWisdom API. |

### 16.2 SEC EDGAR General

| Package | Notes |
|---|---|
| **[edgartools](https://pypi.org/project/edgartools/)** | **Recommended.** Active, MIT, 13F parsing with structured Python objects. `pip install edgartools` |
| **[sec-api](https://pypi.org/project/sec-api/)** | Commercial API wrapper for sec-api.io |

---

## 17. Apify Scrapers

Multiple WhaleWisdom scrapers available on Apify marketplace:

| Scraper | What It Does |
|---|---|
| **[tropical_quince/whalewisdom-13f-scraper](https://apify.com/tropical_quince/whalewisdom-13f-scraper)** | Scrape hedge fund 13F holdings, positions, shares, performance |
| **[fortuitous_pirate/whalewisdom-13f-scraper](https://apify.com/fortuitous_pirate/whalewisdom-13f-scraper)** | Alternative scraper with scheduling support |
| **[consummate_mandala/whalewisdom-13f-scraper](https://apify.com/consummate_mandala/whalewisdom-13f-scraper/api/openapi)** | OpenAPI definition available |

**Output formats:** JSON, CSV, Excel
**Integrations:** Google Sheets, Zapier, Make (Integromat), n8n
**Scheduling:** Apify Schedules for automated recurring runs

**Note:** These bypass the WhaleWisdom API and scrape the website directly. Anish has API access, so the official API is preferred.

---

## 18. N-PORT as Complementary Data

| Attribute | 13F | N-PORT |
|---|---|---|
| **Who files** | Investment managers with >$100M equity AUM | Registered investment companies (mutual funds, ETFs) |
| **Frequency** | Quarterly | Monthly |
| **Filing deadline** | 45 days after quarter-end | 30 days after month-end |
| **Coverage** | Long equity only | **Complete portfolio** (cash, shorts, foreign, treasuries, derivatives) |
| **Public availability** | All filings public | Only quarterly N-PORT made public |
| **SEC data sets** | https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets | https://www.sec.gov/data-research/sec-markets-data/form-n-port-data-sets |

**2026 Update:** SEC proposed amendments requiring monthly filing (instead of quarterly) with 30-day deadline (instead of 60). This makes N-PORT increasingly valuable as a complement to 13F.

---

## 19. 13F-Based ETFs (Real-World Validation)

These ETFs prove that 13F-based strategies work at scale:

| ETF | Ticker | AUM | Strategy | Performance |
|---|---|---|---|---|
| **Goldman Sachs Hedge Industry VIP ETF** | GVIP | $103M | Tracks stocks most popular among hedge fund 13F filings | Varies |
| **Global X Guru Index ETF** | GURU | $55M | 13F-based index, rebalanced quarterly | **11%+ annualized since 2012 launch** |
| **AlphaClone Alternative Alpha ETF** | ALFA | $22M | World's first 13F-based ETF | Varies |
| **Direxion iBillionaire Index ETF** | (closed) | - | Tracked billionaire investors' 13F | Closed |

**Key insight:** These ETFs face the same 45-day lag constraint but still produce market-competitive returns, validating the fundamental approach.

**Limitation:** "What is keeping these funds from achieving top-notch performance is actually what enables them to exist in the first place: the 13F filings" -- the inherent lag caps alpha potential.

**Source:** [Citywire](https://citywireusa.com/registered-investment-advisor/news/hedge-fund-etfs-holdings-gold-or-time-to-fold/a1182619), [Seeking Alpha](https://seekingalpha.com/article/4077250-beat-market-guru-etfs)

---

## 20. Relevance to Anish's Quant Stack

### 20.1 What Anish Has

- **WhaleWisdom Pro** ($500/yr, active since 2026-05-18)
- 200 stocks/filers per 90 days via API
- Full Insider Backtester (Form 4)
- Up to 50 members per filer group
- Combined holdings report
- HMAC-SHA1 API keys in env

### 20.2 How 13F Data Fits Anish's System

Anish's core stack is built around **multi-timeframe confluence detection** with custom Pine indicators (B2B PUP, TNT OD, SQUARIFY, VOB, HVD-PBJ-PPD). The 13F data adds a **structural layer** that these tick-level indicators cannot see:

| Anish's Layer | What It Provides | 13F Enhancement |
|---|---|---|
| **Pine Indicators** | Tick-level price/volume signals | 13F confirms institutional conviction behind those moves |
| **NOI (Order Imbalances)** | Real-time buy/sell pressure | 13F reveals WHO is behind the imbalance (compare NOI stocks vs 13F new positions) |
| **VOB (Volume Order Blocks)** | Holy Grail / Nightmare confluence | 13F ownership trend validates whether a VOB is accumulation or distribution |
| **Options Flow** | Institutional direction via derivatives | Cross-reference: is the fund that just filed 13F also showing up in options flow? |
| **Benzinga News** | Catalyst identification | Combine with insider buying clusters around catalysts |

### 20.3 Strategy Ideas to Test

1. **13F-Confirmed VOB:** When a Volume Order Block forms AND 3+ high-WhaleScore funds added the stock in latest 13F = higher probability Holy Grail setup

2. **Insider Cluster + NOI Confluence:** Insider buying cluster (Form 4) + persistent buy-side NOI = institutional accumulation in progress. Enter on Pine indicator confirmation.

3. **De-Crowding Short Signal:** When crowded institutional names (>100 13F holders) show decreasing ownership for 2+ quarters AND price enters distribution phase on Pine indicators = short setup

4. **Quarterly Rebalancing Calendar Trade:** Around 13F deadline dates (46 days after quarter-end), watch for increased volume as clone funds rebalance. NOI data should show imbalances. Trade the rebalancing flow.

5. **Activist Contrarian:** WhaleWisdom Double Down Report (funds buying into weakness) + Price at key support level on Pine indicators = contrarian accumulation entry

### 20.4 Implementation Priority

1. **First:** Get `quarters`, `filer_lookup`, `stock_lookup` working via API to establish data pipeline
2. **Second:** Build filer group of 20-30 high-WhaleScore managers; pull `holdings` quarterly
3. **Third:** Set up email alerts for insider buying in watchlist stocks
4. **Fourth:** Cross-reference 13F holdings changes with NOI data for confluence detection
5. **Fifth:** Backtest 13F-confirmed setups against raw indicator signals to measure lift

### 20.5 Key Constraints

- API rate limit: 20 requests/minute
- Pro tier: 200 stocks/filers per 90 days -- must be selective
- Data is quarterly (structural, not tactical) -- use for position sizing and conviction, not entry timing
- Always cross-reference WhaleWisdom data with EDGAR original filings for verification

---

## Appendix A: All WhaleWisdom URLs Discovered

```
https://whalewisdom.com/                                    -- Homepage
https://whalewisdom.com/help/api                            -- API documentation
https://whalewisdom.com/shell/api_help                      -- API authentication help
https://whalewisdom.com/info/subscription_info              -- Subscription tiers
https://whalewisdom.com/info/features                       -- Features list
https://whalewisdom.com/info/getting_started                -- Getting started guide
https://whalewisdom.com/info/about                          -- About page
https://whalewisdom.com/info/email_alert                    -- Email alerts setup
https://whalewisdom.com/info/excel_add_in                   -- Excel add-in
https://whalewisdom.com/info/whalescores                    -- WhaleScore methodology
https://whalewisdom.com/info/faq                            -- FAQ
https://whalewisdom.com/info/investing_13f                  -- 13F investing guide
https://whalewisdom.com/faq                                 -- FAQ (alternate)
https://whalewisdom.com/help/whale_university               -- Whale University
https://whalewisdom.com/help/getting_started                -- Common uses
https://whalewisdom.com/help/tutorial_videos                -- Tutorial videos
https://whalewisdom.com/help/backtesting_whitepaper         -- Backtesting whitepaper
https://whalewisdom.com/help/how_can_whalewisdom_help       -- Help overview
https://whalewisdom.com/whitepapers/backtesting             -- Backtesting whitepaper
https://whalewisdom.com/whitepapers/whalewisdom             -- General whitepaper
https://whalewisdom.com/whaleindex                          -- WhaleIndex 100
https://whalewisdom.com/whaleindex/index_1_0                -- WhaleIndex v1.0
https://whalewisdom.com/whaleindex/portfolio_2_0            -- WhaleIndex v2.0
https://whalewisdom.com/report/heat_map                     -- Heat Map 2.0
https://whalewisdom.com/HeatMap                             -- Heat Map (legacy)
https://whalewisdom.com/schedule13d                         -- 13D/13G filings
https://whalewisdom.com/ownership                           -- Form 4 insider trading
https://whalewisdom.com/filing/latest_filings               -- Latest 13F filings
https://whalewisdom.com/statistics/quarterly_stats          -- Quarterly statistics
https://whalewisdom.com/ExcelAddIn                          -- Excel add-in download
https://whalewisdom.com/about                               -- About WhaleWisdom
https://whalewisdom.com/dashboard2/insider_backtester       -- Insider Backtester
https://whalewisdom.com/dashboard2/insider_dashboard        -- Insider Dashboard
https://whalewisdom.com/dashboard2/analytics/backtester     -- 13F Backtester
https://whalewisdom.com/dashboard2/analytics/consensus      -- Consensus Report
https://whalewisdom.com/dashboard2/analytics/double_down    -- Double Down Report
https://whalewisdom.com/dashboard2/search/stock_screener    -- Stock Screener
https://whalewisdom.com/dashboard2/search/fund_performance_search -- Fund Performance
https://whalewisdom.com/dashboard2/other/schedule13         -- 13D/G Search
https://whalewisdom.com/dashboard2/email_alerts             -- Email Alerts

-- Blog (WhaleWisdom Alpha)
https://whalewisdomalpha.com/                               -- Blog home
https://whalewisdomalpha.com/about-us/                      -- About blog
https://whalewisdomalpha.com/category/biotech-insiders-13f-strategies/ -- Biotech category
https://whalewisdomalpha.com/category/13f-filings/          -- 13F category

-- Whitepapers (CDN)
https://s3.amazonaws.com/whalewisdom/whitepaper/EnterpriseWhitePaper.pdf
http://cloudfront.whalewisdomcdn.com/whitepaper/WhaleWisdom_Backtesting.pdf
http://cloudfront.whalewisdomcdn.com/whitepaper/WhaleWisdom.com+13Fs+Explained.pdf
```

## Appendix B: All Academic Paper URLs

```
https://personal.lse.ac.uk/polk/research/bestideas.pdf                    -- Best Ideas (Cohen/Polk/Silli)
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1364827               -- Best Ideas (SSRN)
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3459526               -- Systematic 13F Alpha
https://wp.lancs.ac.uk/fofi2020/files/2020/04/FoFI-2020-090-Farouk-Jivraj.pdf -- Systematic 13F Alpha (PDF)
https://quantpedia.com/strategies/alpha-cloning-following-13f-fillings     -- Quantpedia Alpha Cloning
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3958478               -- Deep RL Portfolio (Fleiss)
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4173243               -- ML 13F Portfolios (Fleiss/Cui)
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4352145               -- ML Manager Performance
https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2014/04/13-15.musto_.pdf -- Delay Research
https://arxiv.org/pdf/2209.08825                                          -- 13F Trading Imbalances
https://arxiv.org/pdf/2602.06198                                          -- Insider Purchase ML Detection
```

---

**END OF RECON**

This document contains everything discoverable across the public internet about WhaleWisdom.com, 13F filing analysis, and institutional holdings strategies as of 2026-05-26. It covers the company, product, API, academic research, competitive landscape, open-source tools, and concrete strategy ideas mapped to Anish's existing quant stack.
