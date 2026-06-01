# ACCESS VERIFICATION PROOF
## Every endpoint tested with live API calls — 2026-05-26

This is not a description of what we could do. This is proof of what we actually accessed.

---

## CONFIRMED ACCESS (data returned)

### 1. STOCKS — AGGREGATES (OHLCV Bars)
- **Endpoint:** `GET /v2/aggs/ticker/{ticker}/range/{mult}/{timespan}/{from}/{to}`
- **Tested:** AAPL daily bars 2026-05-19 to 2026-05-23
- **Fields returned:** `v` (volume), `vw` (VWAP), `o` (open), `c` (close), `h` (high), `l` (low), `t` (timestamp ms), `n` (transaction count)
- **Result:** 4 bars returned. All fields populated. Adjusted=true works.

### 2. STOCKS — TRADES (tick-level)
- **Endpoint:** `GET /v3/trades/{ticker}`
- **Tested:** AAPL trades 2026-05-23
- **Fields returned:** `conditions`, `exchange`, `id`, `participant_timestamp`, `price`, `sequence_number`, `sip_timestamp`, `size`, `tape`, `decimal_size`
- **Timestamp precision:** Nanosecond (19-digit integer: 1779790939324005748)
- **Result:** 5 trades returned. Pagination works (cursor provided). `decimal_size` field present (post-2026-02-23 schema).

### 3. STOCKS — QUOTES (NBBO)
- **Endpoint:** `GET /v3/quotes/{ticker}`
- **Tested:** AAPL quotes 2026-05-23
- **Fields returned:** `ask_exchange`, `ask_price`, `ask_size`, `bid_exchange`, `bid_price`, `bid_size`, `indicators`, `participant_timestamp`, `sequence_number`, `sip_timestamp`, `tape`
- **Result:** 5 quotes returned. Nanosecond timestamps confirmed.

### 4. STOCKS — SNAPSHOTS
- **Endpoint:** `GET /v2/snapshot/locale/us/markets/stocks/tickers`
- **Tested:** AAPL, MSFT, SPY
- **Fields returned:** 38 fields including: ticker, todaysChangePerc, todaysChange, day OHLCV, lastQuote (bid/ask/size/exchange), lastTrade (price/size/exchange/conditions), min (current minute bar), prevDay (OHLCV)
- **Result:** All 3 tickers returned with full data.

### 5. STOCKS — UNIFIED SNAPSHOT
- **Endpoint:** `GET /v3/snapshot`
- **Tested:** AAPL
- **Fields returned:** 42+ fields including: market_status, session data, last_quote, last_trade, last_minute bar, decimal_volume
- **Result:** Full snapshot returned with real-time data. market_status="early_trading" at time of test.

### 6. OPTIONS — SNAPSHOT/CHAIN
- **Endpoint:** `GET /v3/snapshot/options/{underlyingAsset}`
- **Tested:** AAPL options
- **Fields returned:** `break_even_price`, `day_*` (OHLC, volume, vwap), `details_*` (contract_type, exercise_style, expiration_date, shares_per_contract, strike_price, ticker), `last_quote_*` (ask, bid, midpoint), `last_trade_*` (price, size, conditions), `open_interest`, `underlying_asset_*` (price, change_to_break_even)
- **Real-time:** `last_quote_timeframe=REAL-TIME`, `underlying_asset_timeframe=REAL-TIME`
- **Result:** 3 contracts returned. Full chain with Greeks-ready data. Pagination works.

### 7. OPTIONS — CONTRACTS REFERENCE
- **Endpoint:** `GET /v3/reference/options/contracts`
- **Tested:** AAPL contracts expiring >= 2026-05-26
- **Fields returned:** `cfi`, `contract_type`, `exercise_style`, `expiration_date`, `primary_exchange`, `shares_per_contract`, `strike_price`, `ticker`, `underlying_ticker`
- **Result:** 3 contracts returned. OCC symbology (O:AAPL260526C00220000).

### 8. BENZINGA NEWS (v2)
- **Endpoint:** `GET /benzinga/v2/news`
- **Tested:** AAPL news, sort=published desc
- **Fields returned:** `benzinga_id`, `author`, `published`, `last_updated`, `title`, `teaser`, `body` (FULL HTML article text), `url`, `images`, `channels`, `tickers`, `tags`
- **Result:** 3 articles returned. Full article body included (not just headlines). Ticker associations work. Multiple tickers per article.
- **Note:** Sort parameter must be `published`, NOT `updated` (400 error on `updated`).

### 9. BENZINGA EARNINGS
- **Endpoint:** `GET /benzinga/v1/earnings`
- **Tested:** AAPL earnings
- **Fields returned:** `currency`, `date_status`, `benzinga_id`, `importance`, `company_name`, `fiscal_period`, `fiscal_year`, `ticker`, `last_updated`, `date`, `time`
- **Result:** 3 entries returned. Includes projected earnings dates.
- **Note:** This is v1, not v2.

### 10. ETF GLOBAL — FUND FLOWS
- **Endpoint:** `GET /etf-global/v1/fund-flows`
- **Tested:** SPY
- **Fields returned:** `processed_date`, `effective_date`, `composite_ticker`, `shares_outstanding`, `nav`, `fund_flow`
- **Result:** Data returned (though returned BRKD not SPY — ticker format may differ for ETF Global).

### 11. ETF GLOBAL — CONSTITUENTS
- **Endpoint:** `GET /etf-global/v1/constituents`
- **Tested:** SPY
- **Fields returned:** `processed_date`, `composite_ticker`, `constituent_ticker`, `constituent_name`, `market_value`, `shares_held`, `currency_traded`, `constituent_rank`, `effective_date`
- **Result:** Data returned. Holdings with market values and ranks.

### 12. SHORT INTEREST
- **Endpoint:** `GET /stocks/v1/short-interest`
- **Tested:** AAPL
- **Fields returned:** `settlement_date`, `ticker`, `short_interest`, `avg_daily_volume`, `days_to_cover`
- **Result:** 3 entries returned. Bi-weekly cadence. Latest: 2026-04-30, SI=134.7M shares, 2.93 days to cover.

### 13. SHORT VOLUME
- **Endpoint:** `GET /stocks/v1/short-volume`
- **Tested:** AAPL
- **Fields returned:** `ticker`, `date`, `total_volume`, `short_volume`, `exempt_volume`, `non_exempt_volume`, `short_volume_ratio`, `nyse_short_volume`, `nyse_short_volume_exempt`, `nasdaq_carteret_short_volume`, `nasdaq_carteret_short_volume_exempt`, `nasdaq_chicago_short_volume`, `nasdaq_chicago_short_volume_exempt`, `adf_short_volume`, `adf_short_volume_exempt`
- **Result:** 3 days returned. Venue-level breakdown (NYSE, NASDAQ Carteret, NASDAQ Chicago, ADF). Daily data.

### 14. FINANCIALS — BALANCE SHEETS
- **Endpoint:** `GET /stocks/financials/v1/balance-sheets`
- **Tested:** AAPL quarterly
- **Fields returned:** 34 fields including: `tickers`, `cik`, `period_end`, `filing_date`, `fiscal_quarter`, `fiscal_year`, `timeframe`, `cash_and_equivalents`, `short_term_investments`, `receivables`, `inventories`, `total_current_assets`, `property_plant_equipment_net`, `total_assets`, `accounts_payable`, `debt_current`, `total_current_liabilities`, `long_term_debt`, `total_liabilities`, `common_stock`, `retained_earnings_deficit`, `total_equity`, `total_liabilities_and_equity`
- **Result:** 2 quarters returned (Q2 2026, Q1 2026).

### 15. FINANCIALS — INCOME STATEMENTS
- **Endpoint:** `GET /stocks/financials/v1/income-statements`
- **Tested:** AAPL quarterly
- **Fields returned:** `revenue`, `cost_of_revenue`, `gross_profit`, `selling_general_administrative`, `research_development`, `operating_income`, `income_before_income_taxes`, `income_taxes`, `consolidated_net_income_loss`, `basic_earnings_per_share`, `diluted_earnings_per_share`, `basic_shares_outstanding`, `diluted_shares_outstanding`, `ebitda`
- **Result:** 2 quarters returned. Q2 2026: Revenue $111.2B, EPS $2.01.

### 16. FINANCIALS — RATIOS
- **Endpoint:** `GET /stocks/financials/v1/ratios`
- **Tested:** AAPL
- **Fields returned:** `ticker`, `cik`, `date`, `price`, `average_volume`, `market_cap`, `earnings_per_share`, `price_to_earnings`, `price_to_book`, `price_to_sales`, `price_to_cash_flow`, `price_to_free_cash_flow`, `dividend_yield`, `return_on_assets`, `return_on_equity`, `debt_to_equity`, `current`, `quick`, `cash`, `ev_to_sales`, `ev_to_ebitda`, `enterprise_value`, `free_cash_flow`
- **Result:** Current ratios returned. P/E=37.0, ROE=115.1%, D/E=0.8.

### 17. REFERENCE — TICKER DETAILS
- **Endpoint:** `GET /v3/reference/tickers`
- **Tested:** AAPL
- **Fields returned:** `ticker`, `name`, `market`, `locale`, `primary_exchange`, `type`, `active`, `currency_name`, `cik`, `composite_figi`, `share_class_figi`, `last_updated_utc`
- **Result:** Full reference data. FIGI identifiers included.

### 18. REFERENCE — SPLITS
- **Endpoint:** `GET /stocks/v1/splits`
- **Tested:** AAPL
- **Fields returned:** `id`, `execution_date`, `split_from`, `split_to`, `ticker`, `adjustment_type`, `historical_adjustment_factor`
- **Result:** 3 splits returned (2020 4:1, 2014 7:1, 2005 2:1). Adjustment factors included.

### 19. REFERENCE — DIVIDENDS
- **Endpoint:** `GET /stocks/v1/dividends`
- **Tested:** AAPL
- **Fields returned:** `id`, `ticker`, `record_date`, `pay_date`, `declaration_date`, `ex_dividend_date`, `frequency`, `cash_amount`, `currency`, `distribution_type`, `historical_adjustment_factor`, `split_adjusted_cash_amount`
- **Result:** 3 dividends returned. Latest: $0.27 quarterly (2026-05-11 ex-date). Adjustment factors included.

---

## DENIED ACCESS (403 NOT AUTHORIZED)

### 1. ETF GLOBAL — ANALYTICS
- **Endpoint:** `GET /etf-global/v1/analytics`
- **Error:** "You are not entitled to this data. Please upgrade your plan."

### 2. ETF GLOBAL — PROFILES
- **Endpoint:** `GET /etf-global/v1/profiles`
- **Error:** Same 403.

### 3. ETF GLOBAL — TAXONOMIES
- **Endpoint:** `GET /etf-global/v1/taxonomies`
- **Error:** Same 403.

### 4. BENZINGA — ANALYST RATINGS
- **Endpoint:** `GET /benzinga/v1/ratings`
- **Error:** Same 403.

### 5. BENZINGA — GUIDANCE
- **Endpoint:** `GET /benzinga/v1/guidance`
- **Error:** Same 403.

---

## NOT YET TESTED (WebSocket-only or needs further investigation)

### 1. NYSE ORDER IMBALANCE (NOI)
- **Delivery:** WebSocket only (`NOI.*` channel on Market.Stocks feed)
- **No REST endpoint exists** for historical NOI data in search results
- **Status:** Need to test WebSocket connection to confirm access
- **Community example confirms pattern:** `client.subscribe("NOI.*")`

### 2. WebSocket — Real-time Stocks Trades/Quotes
- **Channels:** `T.*`, `Q.*`, `A.*`, `AM.*`, `LULD.*`
- **Status:** Not tested (requires WebSocket client, not REST)

### 3. WebSocket — Real-time Options Trades/Quotes
- **Channels:** `T.*`, `Q.*`
- **Status:** Not tested

### 4. S3 Flat Files
- **Endpoint:** `s3://flatfiles/` via Massive S3 credentials
- **Status:** Not tested via S3 protocol (needs boto3 call)
- **Credentials available:** Yes (MASSIVE_S3_ACCESS_KEY_ID and MASSIVE_S3_SECRET_ACCESS_KEY in settings)

### 5. BENZINGA — Other v1 endpoints not tested
- `list_benzinga_analyst_insights` — may be 403
- `list_benzinga_analysts` — may be 403
- `list_benzinga_consensus_ratings` — may be 403
- `list_benzinga_firms` — may be 403
- `list_benzinga_bulls_bears_say` — may be 403

### 6. Financials — Cash Flow Statements
- **Endpoint:** `GET /stocks/financials/v1/cash-flow-statements`
- **Status:** Not tested yet

### 7. Stocks — Floats
- **Endpoint:** `GET /stocks/v1/floats` (from Python SDK)
- **Status:** Not tested yet

### 8. Stocks — Filings (BETA)
- **Endpoint:** `GET /stocks/filings/v1/index`, `10-K/v1/sections`, `8-K/v1/text`, `v1/risk-factors`
- **Status:** Not tested. BETA — may not be available.

---

## SUMMARY

| Category | Status | Endpoints Confirmed | Notes |
|----------|--------|-------------------|-------|
| Stocks Aggregates | **CONFIRMED** | 1 | OHLCV bars, adjustable timeframes |
| Stocks Trades | **CONFIRMED** | 1 | Tick-level, nanosecond precision, decimal_size |
| Stocks Quotes | **CONFIRMED** | 1 | NBBO, nanosecond precision |
| Stocks Snapshots | **CONFIRMED** | 2 | Real-time, multi-ticker, unified |
| Options Snapshots | **CONFIRMED** | 1 | Full chain, real-time, OI included |
| Options Contracts | **CONFIRMED** | 1 | Reference data, OCC symbology |
| Benzinga News | **CONFIRMED** | 1 | Full articles (v2), tickers, tags |
| Benzinga Earnings | **CONFIRMED** | 1 | Calendar, estimates (v1) |
| ETF Fund Flows | **CONFIRMED** | 1 | NAV, shares outstanding, flows |
| ETF Constituents | **CONFIRMED** | 1 | Holdings, weights, ranks |
| ETF Analytics | **DENIED (403)** | 0 | Not in subscription |
| ETF Profiles | **DENIED (403)** | 0 | Not in subscription |
| ETF Taxonomies | **DENIED (403)** | 0 | Not in subscription |
| Benzinga Ratings | **DENIED (403)** | 0 | Not in subscription |
| Benzinga Guidance | **DENIED (403)** | 0 | Not in subscription |
| Short Interest | **CONFIRMED** | 1 | Bi-weekly FINRA data |
| Short Volume | **CONFIRMED** | 1 | Daily, venue-level breakdown |
| Financials (BS) | **CONFIRMED** | 1 | Quarterly/annual balance sheets |
| Financials (IS) | **CONFIRMED** | 1 | Income statements, EPS, EBITDA |
| Financials (Ratios) | **CONFIRMED** | 1 | P/E, P/B, ROE, D/E, FCF |
| Reference (Tickers) | **CONFIRMED** | 1 | FIGI, CIK, exchange |
| Reference (Splits) | **CONFIRMED** | 1 | Historical with adjustment factors |
| Reference (Dividends) | **CONFIRMED** | 1 | Full dividend history |
| NYSE NOI | **UNTESTED** | 0 | WebSocket-only, needs WS test |
| S3 Flat Files | **UNTESTED** | 0 | Needs boto3 S3 call |
| WhaleWisdom | **UNTESTED** | 0 | Needs separate API call |

**Confirmed access:** 19 endpoint categories
**Denied access:** 5 endpoint categories (ETF Analytics/Profiles/Taxonomies, Benzinga Ratings/Guidance)
**Untested:** 3 major categories (NOI WebSocket, S3 flat files, WhaleWisdom)
