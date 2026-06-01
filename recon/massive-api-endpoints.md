# Massive.com API — Complete Endpoint Reconnaissance

**Generated:** 2026-05-26
**Source of truth:** Live MCP `search_endpoints` (detail=verbose) + `call_api` sample calls + `KNOWN_SUBSCRIPTIONS.md`
**Anish's subscriptions:** Stocks Advanced ($199/m), Options Advanced ($199/m), Benzinga News ($99/m), Benzinga Earnings ($99/m), ETF Global Fund Flows ($99/m), ETF Global Constituents ($99/m), Order Imbalances ($49/m), Currencies Basic (free), Futures Basic (free), Indices Basic (free)

---

## Access Modes

| Mode | Base URL | Auth | Use |
|---|---|---|---|
| **REST** | `https://api.massive.com` | `Authorization: Bearer $MASSIVE_API_KEY` | On-demand queries, snapshots, fundamentals |
| **WebSocket** | `wss://socket.massive.com/{market}` | bearer in `auth` action message | Live streaming: NOI, FMV, AS, T, Q, A |
| **S3 flat files** | `https://files.massive.com` (S3 protocol) | AWS-style with `MASSIVE_S3_*` keys | Bulk historical (Parquet) |

**Global rate limit:** Unlimited for Stocks Advanced / Options Advanced plans (no published cap per request; throttle at 429 if hit). Partner endpoints may have lower caps (Benzinga ~100/min observed).
**Global pagination:** cursor-based via `next_url` field in response. Follow the URL with the `cursor` param to get next page.

---

## TABLE OF CONTENTS

1. [STOCKS — Aggregates](#1-stocks--aggregates)
2. [STOCKS — Trades & Quotes (Tick)](#2-stocks--trades--quotes-tick)
3. [STOCKS — Snapshots](#3-stocks--snapshots)
4. [STOCKS — Last Trade / Last Quote](#4-stocks--last-trade--last-quote)
5. [STOCKS — Short Data](#5-stocks--short-data)
6. [STOCKS — Corporate Actions](#6-stocks--corporate-actions)
7. [STOCKS — Financials](#7-stocks--financials)
8. [STOCKS — SEC Filings](#8-stocks--sec-filings)
9. [STOCKS — Technical Indicators (server-side)](#9-stocks--technical-indicators-server-side)
10. [OPTIONS — Chain, Contracts, Trades, Quotes](#10-options--chain-contracts-trades-quotes)
11. [BENZINGA — News](#11-benzinga--news)
12. [BENZINGA — Earnings](#12-benzinga--earnings)
13. [BENZINGA — Other Partner Endpoints (403 unless subscribed)](#13-benzinga--other-partner-endpoints)
14. [ETF GLOBAL — Constituents](#14-etf-global--constituents)
15. [ETF GLOBAL — Fund Flows](#15-etf-global--fund-flows)
16. [ETF GLOBAL — Other (403 unless subscribed)](#16-etf-global--other-403-unless-subscribed)
17. [NYSE ORDER IMBALANCE (NOI)](#17-nyse-order-imbalance-noi)
18. [FUTURES](#18-futures)
19. [FOREX](#19-forex)
20. [CRYPTO](#20-crypto)
21. [INDICES](#21-indices)
22. [ECONOMY / MACRO](#22-economy--macro)
23. [ALTERNATIVE DATA — Consumer Spending (EU)](#23-alternative-data--consumer-spending-eu)
24. [TMX — Corporate Events](#24-tmx--corporate-events)
25. [REFERENCE DATA](#25-reference-data)
26. [WEBSOCKET CHANNELS (all markets)](#26-websocket-channels-all-markets)
27. [S3 FLAT FILES](#27-s3-flat-files)
28. [MCP apply= FUNCTIONS (client-side)](#28-mcp-apply-functions-client-side)

---

## 1. STOCKS — Aggregates

### 1.1 Custom Bars (OHLC)

```
ENDPOINT: GET /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to}
DESCRIPTION: Aggregated historical OHLCV bars at any resolution. Constructed from qualifying trades only.
DELIVERY: REST
FIELDS RETURNED:
  ticker        (string)  — exchange symbol
  adjusted      (boolean) — whether adjusted for splits
  queryCount    (integer) — number of base aggregates used
  request_id    (string)  — server request ID
  resultsCount  (integer) — total results
  status        (string)  — request status
  results[].c   (number)  — close price
  results[].h   (number)  — highest price
  results[].l   (number)  — lowest price
  results[].n   (integer) — number of transactions
  results[].o   (number)  — open price
  results[].otc (boolean) — whether OTC ticker (omitted if false)
  results[].t   (integer) — Unix ms timestamp for start of window
  results[].v   (number)  — trading volume
  results[].vw  (number)  — volume-weighted average price (VWAP)
  next_url      (string)  — cursor pagination URL
PARAMETERS:
  stocksTicker  (string, required) — case-sensitive ticker (e.g. AAPL)
  multiplier    (integer, required) — timespan multiplier (e.g. 5)
  timespan      (string, required)  — second|minute|hour|day|week|month|quarter|year
  from          (string, required)  — start date YYYY-MM-DD or ms timestamp
  to            (string, required)  — end date YYYY-MM-DD or ms timestamp
  adjusted      (boolean, optional) — adjust for splits (default true)
  sort          (string, optional)  — asc|desc by timestamp
  limit         (integer, optional) — max base aggregates queried (default 5000, max 50000)
HOURS: both (pre-market, regular, after-hours all included)
HISTORICAL DEPTH: 2003 to present (via S3 flat files for full history)
REAL-TIME: yes (real-time for Stocks Advanced)
RATE LIMIT: unlimited (Stocks Advanced tier)
PAGINATION: cursor-based via next_url
SAMPLE RESPONSE:
  {"adjusted":true,"results":[{"c":302.25,"h":302.8,"l":298.08,"n":653718,"o":298.18,"t":1779249600000,"v":38229843.71746,"vw":301.1324}],"status":"OK"}
```

### 1.2 Previous Day Bar (OHLC)

```
ENDPOINT: GET /v2/aggs/ticker/{stocksTicker}/prev
DESCRIPTION: Previous trading day OHLCV bar.
DELIVERY: REST
FIELDS RETURNED:
  ticker        (string)
  adjusted      (boolean)
  queryCount    (integer)
  request_id    (string)
  resultsCount  (integer)
  status        (string)
  results[].T   (string)  — ticker
  results[].c   (number)  — close
  results[].h   (number)  — high
  results[].l   (number)  — low
  results[].o   (number)  — open
  results[].t   (integer) — timestamp ms
  results[].v   (number)  — volume
  results[].vw  (number)  — VWAP
PARAMETERS:
  stocksTicker  (string, required)
  adjusted      (boolean, optional) — default true
HOURS: regular session (standard daily bar)
HISTORICAL DEPTH: previous day only
REAL-TIME: yes
RATE LIMIT: unlimited
PAGINATION: none (single result)
```

### 1.3 Daily Market Summary (Grouped)

```
ENDPOINT: GET /v2/aggs/grouped/locale/us/market/stocks/{date}
DESCRIPTION: All tickers' daily OHLCV bars for a single date (whole-market view).
DELIVERY: REST
FIELDS RETURNED:
  adjusted      (boolean)
  queryCount    (integer)
  request_id    (string)
  resultsCount  (integer)
  status        (string)
  results[].T   (string)  — ticker symbol
  results[].c   (number)  — close
  results[].h   (number)  — high
  results[].l   (number)  — low
  results[].n   (integer) — transactions
  results[].o   (number)  — open
  results[].t   (integer) — timestamp ms
  results[].v   (number)  — volume
  results[].vw  (number)  — VWAP
  results[].otc (boolean) — OTC flag
PARAMETERS:
  date          (string, required) — YYYY-MM-DD
  adjusted      (boolean, optional) — default true
  include_otc   (boolean, optional) — include OTC tickers
HOURS: regular session summary
HISTORICAL DEPTH: 2003+
REAL-TIME: delayed (available after market close)
RATE LIMIT: unlimited
PAGINATION: none (all tickers in one response)
```

### 1.4 Daily Ticker Summary (Open/Close)

```
ENDPOINT: GET /v1/open-close/{stocksTicker}/{date}
DESCRIPTION: Single-day OHLC with pre-market and after-hours prices.
DELIVERY: REST
FIELDS RETURNED:
  afterHours    (number) — after-hours close
  close         (number) — regular close
  from          (string) — date
  high          (number) — regular high
  low           (number) — regular low
  open          (number) — regular open
  preMarket     (number) — pre-market open
  status        (string) — response status
  symbol        (string) — ticker
  volume        (number) — regular volume
PARAMETERS:
  stocksTicker  (string, required)
  date          (string, required) — YYYY-MM-DD
  adjusted      (boolean, optional) — default true
HOURS: both (includes pre/post market prices separately)
HISTORICAL DEPTH: 2003+
REAL-TIME: yes
RATE LIMIT: unlimited
PAGINATION: none (single result)
```

---

## 2. STOCKS — Trades & Quotes (Tick)

### 2.1 Trades (Historical Tick)

```
ENDPOINT: GET /v3/trades/{stockTicker}
DESCRIPTION: Historical tick-level trades for a single ticker. Full SIP data.
DELIVERY: REST
FIELDS RETURNED:
  results[].conditions        (array[integer]) — condition code IDs
  results[].correction        (integer)        — trade correction indicator
  results[].exchange          (integer)        — exchange ID
  results[].id                (string)         — trade ID
  results[].participant_timestamp (integer)    — exchange timestamp (ns)
  results[].price             (number)         — trade price
  results[].sequence_number   (integer)        — sequence number
  results[].sip_timestamp     (integer)        — SIP timestamp (ns)
  results[].size              (number)         — trade size (shares)
  results[].tape              (integer)        — tape (1=A/NYSE, 2=B/NYSE-Arca/etc, 3=C/Nasdaq)
  results[].trf_id            (integer)        — TRF ID
  results[].trf_timestamp     (integer)        — TRF timestamp (ns)
  next_url                    (string)         — pagination cursor
  request_id                  (string)
  status                      (string)
PARAMETERS:
  stockTicker   (string, required)
  timestamp     (string, optional) — YYYY-MM-DD or ns timestamp
  timestamp.gte (string, optional)
  timestamp.gt  (string, optional)
  timestamp.lte (string, optional)
  timestamp.lt  (string, optional)
  order         (string, optional) — asc|desc
  limit         (integer, optional) — default 10, max 50000
  sort          (string, optional) — timestamp
HOURS: both (all sessions)
HISTORICAL DEPTH: 2003+ (via REST for recent; S3 for full)
REAL-TIME: yes (real-time SIP for Stocks Advanced)
RATE LIMIT: unlimited
PAGINATION: cursor-based via next_url
```

### 2.2 Quotes (Historical NBBO)

```
ENDPOINT: GET /v3/quotes/{stockTicker}
DESCRIPTION: Historical tick-level NBBO quotes for a single ticker.
DELIVERY: REST
FIELDS RETURNED:
  results[].ask_exchange      (integer)  — ask exchange ID
  results[].ask_price         (number)   — ask price
  results[].ask_size          (number)   — ask size (round lots)
  results[].bid_exchange      (integer)  — bid exchange ID
  results[].bid_price         (number)   — bid price
  results[].bid_size          (number)   — bid size (round lots)
  results[].conditions        (array[integer]) — condition code IDs
  results[].indicators        (array[integer]) — indicator IDs
  results[].participant_timestamp (integer) — exchange timestamp (ns)
  results[].sequence_number   (integer)
  results[].sip_timestamp     (integer)  — SIP timestamp (ns)
  results[].tape              (integer)
  results[].trf_timestamp     (integer)
  next_url                    (string)
  request_id                  (string)
  status                      (string)
PARAMETERS:
  stockTicker   (string, required)
  timestamp     (string, optional) — YYYY-MM-DD or ns timestamp
  timestamp.gte (string, optional)
  timestamp.gt  (string, optional)
  timestamp.lte (string, optional)
  timestamp.lt  (string, optional)
  order         (string, optional) — asc|desc
  limit         (integer, optional) — default 10, max 50000
  sort          (string, optional) — timestamp
HOURS: both (all sessions)
HISTORICAL DEPTH: 2003+ (REST recent; S3 for full 12.8 TB history)
REAL-TIME: yes
RATE LIMIT: unlimited
PAGINATION: cursor-based via next_url
```

---

## 3. STOCKS — Snapshots

### 3.1 Unified Snapshot (Cross-Asset)

```
ENDPOINT: GET /v3/snapshot
DESCRIPTION: Real-time snapshot across stocks, options, forex, crypto, indices in one request.
DELIVERY: REST
FIELDS RETURNED:
  results[].ticker                                 (string)
  results[].type                                   (enum: stocks|options|forex|crypto|indices)
  results[].name                                   (string)
  results[].market_status                          (string) — open|closed|early_trading|late_trading
  results[].last_updated                           (integer) — ns timestamp
  results[].fmv                                    (number) — Fair Market Value (if available)
  results[].fmv_last_updated                       (integer) — ns timestamp
  results[].session.change                         (number)
  results[].session.change_percent                 (number)
  results[].session.close                          (number)
  results[].session.high                           (number)
  results[].session.low                            (number)
  results[].session.open                           (number)
  results[].session.previous_close                 (number)
  results[].session.volume                         (number)
  results[].session.decimal_volume                 (string) — post 2026-02-23 decimal precision
  results[].session.vwap                           (number)
  results[].session.price                          (number)
  results[].session.last_updated                   (integer) — ns
  results[].session.early_trading_change           (number)
  results[].session.early_trading_change_percent   (number)
  results[].session.late_trading_change            (number)
  results[].session.late_trading_change_percent    (number)
  results[].session.regular_trading_change         (number)
  results[].session.regular_trading_change_percent (number)
  results[].last_trade.price                       (number)
  results[].last_trade.size                        (number)
  results[].last_trade.exchange                    (integer)
  results[].last_trade.conditions                  (array[integer])
  results[].last_trade.id                          (string)
  results[].last_trade.last_updated                (integer) — ns
  results[].last_trade.timeframe                   (string) — REAL-TIME|DELAYED
  results[].last_trade.decimal_size                (string)
  results[].last_quote.ask                         (number)
  results[].last_quote.ask_size                    (number)
  results[].last_quote.ask_exchange                (integer)
  results[].last_quote.bid                         (number)
  results[].last_quote.bid_size                    (number)
  results[].last_quote.bid_exchange                (integer)
  results[].last_quote.last_updated                (integer) — ns
  results[].last_quote.timeframe                   (string) — REAL-TIME|DELAYED
  results[].last_quote.midpoint                    (number) — options only
  results[].last_minute.close                      (number)
  results[].last_minute.high                       (number)
  results[].last_minute.low                        (number)
  results[].last_minute.open                       (number)
  results[].last_minute.volume                     (number)
  results[].last_minute.vwap                       (number)
  results[].last_minute.transactions               (integer)
  results[].last_minute.last_updated               (integer) — ns
  results[].last_minute.decimal_volume             (string)
  results[].value                                  (number) — index value (indices only)
  next_url       (string)
  request_id     (string)
  status         (string)
PARAMETERS:
  ticker.any_of  (string, optional) — comma-separated, max 250
  ticker         (string, optional) — lexicographic range
  ticker.gte     (string, optional)
  ticker.gt      (string, optional)
  ticker.lte     (string, optional)
  ticker.lt      (string, optional)
  type           (string, optional) — stocks|options|forex|crypto|indices
  order          (string, optional)
  limit          (integer, optional) — default 10, max 250
  sort           (string, optional)
HOURS: both (real-time during all sessions)
HISTORICAL DEPTH: current snapshot only
REAL-TIME: yes
RATE LIMIT: unlimited
PAGINATION: cursor-based via next_url
```

### 3.2 Single Ticker Snapshot

```
ENDPOINT: GET /v2/snapshot/locale/us/markets/stocks/tickers/{stocksTicker}
DESCRIPTION: Real-time snapshot for a single stock ticker.
DELIVERY: REST
FIELDS RETURNED: Same structure as Unified Snapshot results[] for stocks type.
PARAMETERS:
  stocksTicker   (string, required)
HOURS: both
HISTORICAL DEPTH: current only
REAL-TIME: yes
RATE LIMIT: unlimited
PAGINATION: none
```

### 3.3 Full Market Snapshot

```
ENDPOINT: GET /v2/snapshot/locale/us/markets/stocks/tickers
DESCRIPTION: Snapshot for ALL stock tickers (paginated).
DELIVERY: REST
FIELDS RETURNED: Same as Unified Snapshot results[] for stocks.
PARAMETERS:
  tickers        (string, optional) — comma-separated filter
  include_otc    (boolean, optional)
  order          (string, optional)
  limit          (integer, optional)
  sort           (string, optional)
HOURS: both
HISTORICAL DEPTH: current only
REAL-TIME: yes
RATE LIMIT: unlimited
PAGINATION: cursor-based
```

### 3.4 Top Market Movers

```
ENDPOINT: GET /v2/snapshot/locale/us/markets/stocks/{direction}
DESCRIPTION: Top gainers or losers for the day.
DELIVERY: REST
FIELDS RETURNED: Same as snapshot results[].
PARAMETERS:
  direction      (string, required) — gainers|losers
  include_otc    (boolean, optional)
HOURS: regular session
HISTORICAL DEPTH: current only
REAL-TIME: yes
RATE LIMIT: unlimited
PAGINATION: none
```

---

## 4. STOCKS — Last Trade / Last Quote

### 4.1 Last Trade

```
ENDPOINT: GET /v2/last/trade/{stocksTicker}
DESCRIPTION: Most recent trade for a ticker.
DELIVERY: REST
FIELDS RETURNED:
  results.T                  (string) — ticker
  results.c                  (array[integer]) — conditions
  results.f                  (integer) — TRF timestamp (ns)
  results.i                  (string)  — trade ID
  results.p                  (number)  — price
  results.q                  (integer) — sequence number
  results.r                  (integer) — TRF ID
  results.s                  (number)  — size
  results.t                  (integer) — SIP timestamp (ns)
  results.x                  (integer) — exchange ID
  results.y                  (integer) — participant timestamp (ns)
  results.z                  (integer) — tape
  request_id                 (string)
  status                     (string)
PARAMETERS:
  stocksTicker  (string, required)
HOURS: both
REAL-TIME: yes
```

### 4.2 Last NBBO Quote

```
ENDPOINT: GET /v2/last/nbbo/{stocksTicker}
DESCRIPTION: Most recent NBBO quote for a ticker.
DELIVERY: REST
FIELDS RETURNED:
  results.T                  (string) — ticker
  results.P                  (number) — ask price
  results.S                  (number) — ask size (lots)
  results.X                  (integer) — ask exchange
  results.c                  (array[integer]) — conditions
  results.f                  (integer) — TRF timestamp (ns)
  results.i                  (array[integer]) — indicators
  results.p                  (number) — bid price
  results.q                  (integer) — sequence number
  results.s                  (number) — bid size (lots)
  results.t                  (integer) — SIP timestamp (ns)
  results.x                  (integer) — bid exchange
  results.y                  (integer) — participant timestamp (ns)
  results.z                  (integer) — tape
  request_id                 (string)
  status                     (string)
PARAMETERS:
  stocksTicker  (string, required)
HOURS: both
REAL-TIME: yes
```

---

## 5. STOCKS — Short Data

### 5.1 Short Interest

```
ENDPOINT: GET /stocks/v1/short-interest
DESCRIPTION: FINRA biweekly short interest by ticker.
DELIVERY: REST
FIELDS RETURNED:
  results[].settlement_date   (string) — YYYY-MM-DD
  results[].ticker            (string)
  results[].short_interest    (number) — total short shares
  results[].avg_daily_volume  (number) — average daily volume
  results[].days_to_cover     (number) — short_interest / avg_daily_volume
PARAMETERS:
  ticker              (string, optional)
  ticker.any_of       (string, optional)
  ticker.gte/gt/lte/lt (string, optional)
  settlement_date     (string, optional) — YYYY-MM-DD
  settlement_date.gte/gt/lte/lt (string, optional)
  order               (string, optional)
  limit               (integer, optional) — default 100, max 50000
  sort                (string, optional)
HOURS: N/A (biweekly snapshot)
HISTORICAL DEPTH: 2017+
REAL-TIME: no (biweekly FINRA release)
RATE LIMIT: unlimited
PAGINATION: cursor-based
SAMPLE: {"settlement_date":"2017-12-29","ticker":"A","short_interest":4197300,"avg_daily_volume":1234014,"days_to_cover":3.4}
```

### 5.2 Short Volume

```
ENDPOINT: GET /stocks/v1/short-volume
DESCRIPTION: FINRA daily short volume broken down by exchange.
DELIVERY: REST
FIELDS RETURNED:
  results[].ticker                             (string)
  results[].date                               (string) — YYYY-MM-DD
  results[].total_volume                       (number)
  results[].short_volume                       (number)
  results[].exempt_volume                      (number)
  results[].non_exempt_volume                  (number)
  results[].short_volume_ratio                 (number) — percentage
  results[].nyse_short_volume                  (number)
  results[].nyse_short_volume_exempt           (number)
  results[].nasdaq_carteret_short_volume       (number)
  results[].nasdaq_carteret_short_volume_exempt(number)
  results[].nasdaq_chicago_short_volume        (number)
  results[].nasdaq_chicago_short_volume_exempt (number)
  results[].adf_short_volume                   (number)
  results[].adf_short_volume_exempt            (number)
PARAMETERS:
  ticker              (string, optional)
  ticker.any_of       (string, optional)
  date                (string, optional) — YYYY-MM-DD
  date.gte/gt/lte/lt  (string, optional)
  order               (string, optional)
  limit               (integer, optional) — default 100, max 50000
  sort                (string, optional)
HOURS: N/A (daily after close)
HISTORICAL DEPTH: 2024+ (observed in sample)
REAL-TIME: no (next-day)
RATE LIMIT: unlimited
PAGINATION: cursor-based
```

---

## 6. STOCKS — Corporate Actions

### 6.1 Splits

```
ENDPOINT: GET /stocks/v1/splits
DESCRIPTION: Stock splits with historical adjustment factor. REPLACES deprecated /v3/reference/splits.
DELIVERY: REST
FIELDS RETURNED:
  results[].execution_date              (string) — YYYY-MM-DD
  results[].split_from                  (number) — original shares
  results[].split_to                    (number) — new shares
  results[].ticker                      (string)
  results[].id                          (string)
  results[].historical_adjustment_factor (number) — multiply pre-split prices by this
PARAMETERS:
  ticker              (string, optional)
  ticker.any_of       (string, optional)
  execution_date      (string, optional)
  execution_date.gte/gt/lte/lt (string, optional)
  order               (string, optional)
  limit               (integer, optional) — default 10, max 1000
  sort                (string, optional)
  reverse_split       (boolean, optional)
HOURS: N/A
HISTORICAL DEPTH: comprehensive
REAL-TIME: no
PAGINATION: cursor-based
```

### 6.2 Dividends

```
ENDPOINT: GET /stocks/v1/dividends
DESCRIPTION: Dividend declarations with ex-dates. REPLACES deprecated /v3/reference/dividends.
DELIVERY: REST
FIELDS RETURNED:
  results[].cash_amount     (number)
  results[].currency        (string)
  results[].declaration_date (string)
  results[].dividend_type   (string) — CD (cash dividend), SC (special cash), LT (long-term capital gain), ST (short-term capital gain)
  results[].ex_dividend_date (string)
  results[].frequency       (integer) — 1=annual, 2=bi-annual, 4=quarterly, 12=monthly, 0=one-time
  results[].pay_date        (string)
  results[].record_date     (string)
  results[].ticker          (string)
PARAMETERS:
  ticker              (string, optional)
  ticker.any_of       (string, optional)
  ex_dividend_date    (string, optional)
  ex_dividend_date.gte/gt/lte/lt (string, optional)
  declaration_date    (string, optional)
  record_date         (string, optional)
  pay_date            (string, optional)
  cash_amount         (number, optional)
  dividend_type       (string, optional)
  frequency           (integer, optional)
  order               (string, optional)
  limit               (integer, optional) — default 10, max 1000
  sort                (string, optional)
HOURS: N/A
HISTORICAL DEPTH: comprehensive
REAL-TIME: no (event-driven)
PAGINATION: cursor-based
```

### 6.3 IPOs

```
ENDPOINT: GET /vX/reference/ipos
DESCRIPTION: Initial public offerings — upcoming and recent.
DELIVERY: REST
FIELDS RETURNED:
  results[].ticker                  (string)
  results[].last_updated            (string)
  results[].announced_date          (string)
  results[].issuer_name             (string)
  results[].currency_code           (string)
  results[].max_shares_offered      (number)
  results[].lowest_offer_price      (number)
  results[].highest_offer_price     (number)
  results[].total_offer_size        (number)
  results[].primary_exchange        (string)
  results[].shares_outstanding      (number)
  results[].security_type           (string) — CS, ET, etc.
  results[].lot_size                (integer)
  results[].security_description    (string)
  results[].ipo_status              (string) — pending|withdrawn|approved|listed
PARAMETERS:
  ticker              (string, optional)
  us_code             (string, optional)
  listing_date        (string, optional)
  listing_date.gte/gt/lte/lt (string, optional)
  ipo_status          (string, optional)
  order               (string, optional) — asc|desc
  limit               (integer, optional) — default 10, max 1000
  sort                (string, optional) — listing_date
HOURS: N/A
HISTORICAL DEPTH: recent IPOs
REAL-TIME: no
PAGINATION: cursor-based
SAMPLE: {"ticker":"RUIH","announced_date":"2026-05-22","issuer_name":"RUI Holdings Inc.","ipo_status":"pending"}
```

### 6.4 Float

```
ENDPOINT: GET /stocks/vX/float
DESCRIPTION: Free-float shares outstanding per ticker.
DELIVERY: REST
FIELDS RETURNED:
  results[].ticker            (string)
  results[].free_float        (number) — shares available for trading
  results[].effective_date    (string) — YYYY-MM-DD
  results[].free_float_percent (number) — percentage of total
PARAMETERS:
  ticker              (string, optional)
  ticker.any_of       (string, optional)
  effective_date      (string, optional)
  effective_date.gte/gt/lte/lt (string, optional)
  order               (string, optional)
  limit               (integer, optional)
  sort                (string, optional)
HOURS: N/A
HISTORICAL DEPTH: point-in-time
REAL-TIME: no
PAGINATION: cursor-based
SAMPLE: {"ticker":"A","free_float":282206675,"effective_date":"2026-04-17","free_float_percent":99.9}
```

---

## 7. STOCKS — Financials

### 7.1 Income Statements

```
ENDPOINT: GET /stocks/financials/v1/income-statements
DESCRIPTION: SEC income statements from 10-K/10-Q filings.
DELIVERY: REST
FIELDS RETURNED:
  results[].tickers                                     (array[string])
  results[].cik                                         (string)
  results[].period_end                                  (string) — YYYY-MM-DD
  results[].filing_date                                 (string) — YYYY-MM-DD
  results[].fiscal_quarter                              (integer) — 1-4
  results[].fiscal_year                                 (integer)
  results[].timeframe                                   (string) — quarterly|annual
  results[].revenue                                     (number)
  results[].cost_of_revenue                             (number)
  results[].gross_profit                                (number)
  results[].selling_general_administrative              (number)
  results[].research_development                        (number)
  results[].other_operating_expenses                    (number)
  results[].total_operating_expenses                    (number)
  results[].operating_income                            (number)
  results[].interest_expense                            (number)
  results[].interest_income                             (number)
  results[].other_income_expense                        (number)
  results[].total_other_income_expense                  (number)
  results[].income_before_income_taxes                  (number)
  results[].income_taxes                                (number)
  results[].consolidated_net_income_loss                (number)
  results[].net_income_loss_attributable_common_shareholders (number)
  results[].basic_earnings_per_share                    (number)
  results[].diluted_earnings_per_share                  (number)
  results[].basic_shares_outstanding                    (number)
  results[].diluted_shares_outstanding                  (number)
  results[].ebitda                                      (number)
PARAMETERS:
  ticker/cik/period_end/filing_date/fiscal_quarter/fiscal_year/timeframe — all with range operators
  order, limit, sort
HOURS: N/A
HISTORICAL DEPTH: 2009+
REAL-TIME: no (filing lag)
PAGINATION: cursor-based
```

### 7.2 Balance Sheets

```
ENDPOINT: GET /stocks/financials/v1/balance-sheets
DESCRIPTION: SEC balance sheets from 10-K/10-Q filings.
DELIVERY: REST
FIELDS RETURNED:
  results[].tickers                                     (array[string])
  results[].cik                                         (string)
  results[].period_end                                  (string)
  results[].filing_date                                 (string)
  results[].fiscal_quarter                              (integer)
  results[].fiscal_year                                 (integer)
  results[].timeframe                                   (string)
  results[].cash_and_equivalents                        (number)
  results[].receivables                                 (number)
  results[].inventories                                 (number)
  results[].other_current_assets                        (number)
  results[].total_current_assets                        (number)
  results[].property_plant_equipment_net                (number)
  results[].goodwill                                    (number)
  results[].other_assets                                (number)
  results[].total_assets                                (number)
  results[].accounts_payable                            (number)
  results[].debt_current                                (number)
  results[].accrued_and_other_current_liabilities       (number)
  results[].total_current_liabilities                   (number)
  results[].long_term_debt_and_capital_lease_obligations (number)
  results[].other_noncurrent_liabilities                (number)
  results[].total_liabilities                           (number)
  results[].commitments_and_contingencies               (number)
  results[].common_stock                                (number)
  results[].accumulated_other_comprehensive_income      (number)
  results[].retained_earnings_deficit                   (number)
  results[].other_equity                                (number)
  results[].total_equity_attributable_to_parent         (number)
  results[].noncontrolling_interest                     (number)
  results[].total_equity                                (number)
  results[].total_liabilities_and_equity                (number)
PARAMETERS: same as income statements
HOURS: N/A
HISTORICAL DEPTH: 2009+
PAGINATION: cursor-based
```

### 7.3 Cash Flow Statements

```
ENDPOINT: GET /stocks/financials/v1/cash-flow-statements
DESCRIPTION: SEC cash flow statements from 10-K/10-Q filings.
DELIVERY: REST
FIELDS RETURNED:
  results[].tickers                                     (array[string])
  results[].cik                                         (string)
  results[].period_end / filing_date / fiscal_quarter / fiscal_year / timeframe
  results[].net_income                                  (number)
  results[].depreciation_depletion_and_amortization     (number)
  results[].other_operating_activities                  (number)
  results[].change_in_other_operating_assets_and_liabilities_net (number)
  results[].cash_from_operating_activities_continuing_operations (number)
  results[].net_cash_from_operating_activities          (number)
  results[].purchase_of_property_plant_and_equipment    (number)
  results[].sale_of_property_plant_and_equipment        (number)
  results[].other_investing_activities                  (number)
  results[].net_cash_from_investing_activities_continuing_operations (number)
  results[].net_cash_from_investing_activities          (number)
  results[].short_term_debt_issuances_repayments        (number)
  results[].long_term_debt_issuances_repayments         (number)
  results[].dividends                                   (number)
  results[].other_financing_activities                  (number)
  results[].net_cash_from_financing_activities_continuing_operations (number)
  results[].net_cash_from_financing_activities          (number)
  results[].effect_of_currency_exchange_rate            (number)
  results[].change_in_cash_and_equivalents              (number)
PARAMETERS: same as income statements
HOURS: N/A
HISTORICAL DEPTH: 2009+
PAGINATION: cursor-based
```

### 7.4 Financial Ratios

```
ENDPOINT: GET /stocks/financials/v1/ratios
DESCRIPTION: Computed financial ratios per ticker per date.
DELIVERY: REST
FIELDS RETURNED:
  results[].ticker                  (string)
  results[].cik                     (string)
  results[].date                    (string)
  results[].price                   (number)
  results[].average_volume          (number)
  results[].market_cap              (number)
  results[].earnings_per_share      (number)
  results[].price_to_earnings       (number)
  results[].price_to_book           (number)
  results[].price_to_sales          (number)
  results[].price_to_cash_flow      (number)
  results[].price_to_free_cash_flow (number)
  results[].dividend_yield          (number)
  results[].return_on_assets        (number)
  results[].return_on_equity        (number)
  results[].debt_to_equity          (number)
  results[].current                 (number) — current ratio
  results[].quick                   (number) — quick ratio
  results[].cash                    (number) — cash ratio
  results[].ev_to_sales             (number)
  results[].ev_to_ebitda            (number)
  results[].enterprise_value        (number)
  results[].free_cash_flow          (number)
PARAMETERS:
  ticker, cik, date — with range operators
  order, limit, sort
HOURS: N/A
HISTORICAL DEPTH: derived from financials
PAGINATION: cursor-based
SAMPLE: {"ticker":"A","date":"2026-05-22","price":114.96,"market_cap":32487962362,"price_to_earnings":25.18,"debt_to_equity":0.49}
```

---

## 8. STOCKS — SEC Filings

### 8.1 Form 4 (Insider Transactions)

```
ENDPOINT: GET /stocks/filings/vX/form-4
DESCRIPTION: SEC Form 4 insider transaction filings.
DELIVERY: REST
FIELDS RETURNED:
  results[].tickers                         (array[string])
  results[].issuer_cik                      (string)
  results[].owner_cik                       (string)
  results[].accession_number                (string)
  results[].form_type                       (string) — "4"
  results[].filing_date                     (string)
  results[].period_of_report                (string)
  results[].issuer_name                     (string)
  results[].owner_name                      (string)
  results[].is_director                     (boolean)
  results[].is_officer                      (boolean)
  results[].is_ten_percent_owner            (boolean)
  results[].is_other                        (boolean)
  results[].officer_title                   (string)
  results[].security_type                   (string) — non_derivative|derivative
  results[].record_type                     (string) — holding|transaction
  results[].security_title                  (string)
  results[].transaction_timeliness          (string) — O (on time), L (late)
  results[].aff_10b5_one                    (boolean) — 10b5-1 plan
  results[].shares_owned_following_transaction (number)
  results[].direct_or_indirect              (string) — D|I
  results[].nature_of_ownership             (string)
  results[].filing_url                      (string)
PARAMETERS:
  tickers, issuer_cik, owner_cik, filing_date, period_of_report — with range ops
  form_type, is_director, is_officer, is_ten_percent_owner
  order, limit, sort
HOURS: N/A
HISTORICAL DEPTH: EDGAR history
PAGINATION: cursor-based
```

### 8.2 Form 3 (Initial Insider Ownership)

```
ENDPOINT: GET /stocks/filings/vX/form-3
DESCRIPTION: SEC Form 3 initial statement of beneficial ownership.
DELIVERY: REST
FIELDS RETURNED:
  results[].tickers                         (array[string])
  results[].issuer_cik                      (string)
  results[].owner_cik                       (string)
  results[].accession_number                (string)
  results[].form_type                       (string) — "3"
  results[].filing_date                     (string)
  results[].period_of_report                (string)
  results[].issuer_name                     (string)
  results[].owner_name                      (string)
  results[].is_director                     (boolean)
  results[].is_officer                      (boolean)
  results[].is_ten_percent_owner            (boolean)
  results[].is_other                        (boolean)
  results[].officer_title                   (string)
  results[].security_type                   (string)
  results[].security_title                  (string)
  results[].exercise_price                  (number)
  results[].underlying_security_title       (string)
  results[].underlying_security_shares      (number)
  results[].direct_or_indirect              (string)
  results[].footnotes                       (array[object])
  results[].filing_url                      (string)
PARAMETERS: same as Form 4
HOURS: N/A
PAGINATION: cursor-based
```

### 8.3 13-F Filings (Institutional Holdings)

```
ENDPOINT: GET /stocks/filings/vX/13-F
DESCRIPTION: Quarterly 13-F institutional holdings filings.
DELIVERY: REST
FIELDS RETURNED:
  results[].filer_cik                       (string)
  results[].accession_number                (string)
  results[].form_type                       (string) — 13F-HR|13F-HR/A
  results[].filing_date                     (string)
  results[].period                          (string) — quarter end YYYY-MM-DD
  results[].issuer_name                     (string)
  results[].title_of_class                  (string)
  results[].market_value                    (number) — in thousands
  results[].shares_or_principal_amount      (number)
  results[].shares_or_principal_type        (string) — SH|PRN
  results[].investment_discretion           (string) — SOLE|SHARED|DEFINED
  results[].voting_authority_sole           (number)
  results[].voting_authority_shared         (number)
  results[].voting_authority_none           (number)
  results[].cusip                           (string)
  results[].filing_url                      (string)
  results[].file_number                     (string)
  results[].film_number                     (string)
PARAMETERS:
  filer_cik, filing_date, period, cusip, form_type — with range operators
  order, limit, sort
HOURS: N/A
HISTORICAL DEPTH: EDGAR history
PAGINATION: cursor-based
```

### 8.4 Risk Factors (Pre-Classified)

```
ENDPOINT: GET /stocks/filings/vX/risk-factors
DESCRIPTION: Pre-classified risk factors from 10-K filings with 3-level taxonomy.
DELIVERY: REST
FIELDS RETURNED:
  results[].cik                  (string)
  results[].ticker               (string)
  results[].primary_category     (string) — e.g. strategic_and_competitive
  results[].secondary_category   (string) — e.g. market_position_and_competition
  results[].tertiary_category    (string) — e.g. competitive_pressure_and_market_share_loss
  results[].filing_date          (string)
  results[].supporting_text      (string) — full risk factor text
PARAMETERS:
  ticker, cik, primary_category, secondary_category, tertiary_category, filing_date — with range ops
  order, limit, sort
HOURS: N/A
HISTORICAL DEPTH: 10-K filings
PAGINATION: cursor-based
```

### 8.5 Risk Categories (Taxonomy)

```
ENDPOINT: GET /stocks/taxonomies/vX/risk-factors
DESCRIPTION: Reference taxonomy of risk factor categories (3 levels).
DELIVERY: REST
FIELDS RETURNED:
  results[].primary_category     (string)
  results[].secondary_category   (string)
  results[].tertiary_category    (string)
  results[].description          (string)
  results[].taxonomy             (number)
PARAMETERS:
  primary_category, secondary_category, tertiary_category — with range ops
  limit, sort
HOURS: N/A
PAGINATION: cursor-based
```

### 8.6 10-K Sections

```
ENDPOINT: GET /stocks/filings/10-K/vX/sections
DESCRIPTION: Parsed sections from 10-K annual reports.
DELIVERY: REST
FIELDS RETURNED: (504 timeout on sample call — endpoint exists but may be slow/heavy)
PARAMETERS:
  ticker, cik, filing_date, section — with range ops
  order, limit, sort
HOURS: N/A
PAGINATION: cursor-based
```

### 8.7 8-K Text

```
ENDPOINT: GET /stocks/filings/8-K/vX/text
DESCRIPTION: Full text of 8-K current report filings.
DELIVERY: REST
FIELDS RETURNED:
  results[].cik              (string)
  results[].ticker           (string)
  results[].accession_number (string)
  results[].form_type        (string)
  results[].filing_date      (string)
  results[].items_text       (string) — full 8-K text with item headers
  results[].filing_url       (string)
PARAMETERS:
  ticker, cik, filing_date, form_type — with range ops
  order, limit, sort
HOURS: N/A
PAGINATION: cursor-based
```

### 8.8 SEC EDGAR Index

```
ENDPOINT: GET /stocks/filings/vX/index
DESCRIPTION: EDGAR filing index (all form types).
DELIVERY: REST
FIELDS RETURNED:
  results[].cik              (string)
  results[].issuer_name      (string)
  results[].filing_url       (string)
  results[].accession_number (string)
PARAMETERS:
  cik, form_type, filing_date — with range ops
  order, limit, sort
HOURS: N/A
PAGINATION: cursor-based
```

---

## 9. STOCKS — Technical Indicators (Server-Side)

### 9.1 SMA (Simple Moving Average)

```
ENDPOINT: GET /v1/indicators/sma/{stockTicker}
DESCRIPTION: Server-computed SMA over any timespan/window.
DELIVERY: REST
FIELDS RETURNED:
  results.values[].timestamp  (integer) — ms
  results.values[].value      (number)
  results.underlying.url      (string) — URL of underlying aggs
  next_url, request_id, status
PARAMETERS:
  stockTicker        (string, required)
  timestamp          (string, optional) — YYYY-MM-DD or ms
  timestamp.gte/gt/lte/lt (string, optional)
  timespan           (string, optional) — minute|hour|day|week|month|quarter|year
  adjusted           (boolean, optional) — default true
  window             (integer, optional) — SMA period (e.g. 50)
  series_type        (string, optional) — close|open|high|low
  expand_underlying  (boolean, optional) — include aggs in response
  order              (string, optional) — asc|desc
  limit              (integer, optional) — default 10, max 5000
HOURS: N/A (computed from aggs)
HISTORICAL DEPTH: matches underlying aggs (2003+)
PAGINATION: cursor-based
```

### 9.2 EMA (Exponential Moving Average)

```
ENDPOINT: GET /v1/indicators/ema/{stockTicker}
DESCRIPTION: Server-computed EMA.
DELIVERY: REST
FIELDS/PARAMETERS: Same structure as SMA.
```

### 9.3 RSI (Relative Strength Index)

```
ENDPOINT: GET /v1/indicators/rsi/{stockTicker}
DESCRIPTION: Server-computed RSI.
DELIVERY: REST
FIELDS/PARAMETERS: Same structure as SMA. Window default 14.
```

### 9.4 MACD (Moving Average Convergence/Divergence)

```
ENDPOINT: GET /v1/indicators/macd/{stockTicker}
DESCRIPTION: Server-computed MACD with signal line and histogram.
DELIVERY: REST
FIELDS RETURNED:
  results.values[].timestamp   (integer) — ms
  results.values[].value       (number)  — MACD line
  results.values[].signal      (number)  — signal line
  results.values[].histogram   (number)  — MACD - signal
  results.underlying.url       (string)
PARAMETERS:
  Same as SMA plus:
  short_window   (integer, optional) — default 12
  long_window    (integer, optional) — default 26
  signal_window  (integer, optional) — default 9
PAGINATION: cursor-based
```

---

## 10. OPTIONS — Chain, Contracts, Trades, Quotes

### 10.1 Option Chain Snapshot

```
ENDPOINT: GET /v3/snapshot/options/{underlyingAsset}
DESCRIPTION: Full options chain with greeks, quotes, and trades for an underlying.
DELIVERY: REST
FIELDS RETURNED:
  results[].break_even_price                        (number)
  results[].day.change                              (number)
  results[].day.change_percent                      (number)
  results[].day.close                               (number)
  results[].day.high                                (number)
  results[].day.last_updated                        (integer) — ns
  results[].day.low                                 (number)
  results[].day.open                                (number)
  results[].day.previous_close                      (number)
  results[].day.volume                              (number)
  results[].day.vwap                                (number)
  results[].details.contract_type                   (string) — call|put
  results[].details.exercise_style                  (string) — american|european
  results[].details.expiration_date                 (string) — YYYY-MM-DD
  results[].details.shares_per_contract             (integer) — usually 100
  results[].details.strike_price                    (number)
  results[].details.ticker                          (string) — OCC option symbol
  results[].greeks.delta                            (number)
  results[].greeks.gamma                            (number)
  results[].greeks.theta                            (number)
  results[].greeks.vega                             (number)
  results[].implied_volatility                      (number)
  results[].last_quote.ask                          (number)
  results[].last_quote.ask_size                     (number)
  results[].last_quote.ask_exchange                 (integer)
  results[].last_quote.bid                          (number)
  results[].last_quote.bid_size                     (number)
  results[].last_quote.bid_exchange                 (integer)
  results[].last_quote.last_updated                 (integer) — ns
  results[].last_quote.midpoint                     (number)
  results[].last_quote.timeframe                    (string)
  results[].last_trade.sip_timestamp                (integer) — ns
  results[].last_trade.conditions                   (array[integer])
  results[].last_trade.price                        (number)
  results[].last_trade.size                         (integer)
  results[].last_trade.exchange                     (integer)
  results[].last_trade.timeframe                    (string)
  results[].open_interest                           (integer)
  results[].underlying_asset.change_to_break_even   (number)
  results[].underlying_asset.last_updated           (integer) — ns
  results[].underlying_asset.price                  (number)
  results[].underlying_asset.ticker                 (string)
  results[].underlying_asset.timeframe              (string)
PARAMETERS:
  underlyingAsset    (string, required) — e.g. AAPL
  strike_price       (number, optional) — with .gte/.gt/.lte/.lt
  expiration_date    (string, optional) — YYYY-MM-DD with range ops
  contract_type      (string, optional) — call|put
  order              (string, optional)
  limit              (integer, optional) — default 10, max 250
  sort               (string, optional)
HOURS: both
HISTORICAL DEPTH: current snapshot
REAL-TIME: yes
PAGINATION: cursor-based
```

### 10.2 Single Option Contract Snapshot

```
ENDPOINT: GET /v3/snapshot/options/{underlyingAsset}/{optionContract}
DESCRIPTION: Snapshot for a single option contract.
DELIVERY: REST
FIELDS RETURNED: Same as chain snapshot results[] for one contract.
PARAMETERS:
  underlyingAsset  (string, required)
  optionContract   (string, required) — OCC symbol
HOURS: both
REAL-TIME: yes
```

### 10.3 Options Trades (Historical Tick)

```
ENDPOINT: GET /v3/trades/{optionsTicker}
DESCRIPTION: Tick-level trades for an option contract.
DELIVERY: REST
FIELDS RETURNED: Same as stock trades.
PARAMETERS: Same as stock trades (with optionsTicker).
HOURS: both
HISTORICAL DEPTH: 2014+ (Options Advanced)
REAL-TIME: yes
PAGINATION: cursor-based
```

### 10.4 Options Quotes (Historical NBBO)

```
ENDPOINT: GET /v3/quotes/{optionsTicker}
DESCRIPTION: Tick-level NBBO quotes for an option contract.
DELIVERY: REST
FIELDS RETURNED: Same as stock quotes.
PARAMETERS: Same as stock quotes (with optionsTicker).
HOURS: both
HISTORICAL DEPTH: 2022+ (Options Advanced)
REAL-TIME: yes
PAGINATION: cursor-based
```

### 10.5 Options Custom Bars (OHLC)

```
ENDPOINT: GET /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}
DESCRIPTION: OHLCV bars for an option contract.
DELIVERY: REST
FIELDS/PARAMETERS: Same as stock aggs.
HOURS: both
HISTORICAL DEPTH: 2014+
```

### 10.6 Options Previous Day Bar

```
ENDPOINT: GET /v2/aggs/ticker/{optionsTicker}/prev
DESCRIPTION: Previous day OHLCV for an option contract.
DELIVERY: REST
FIELDS/PARAMETERS: Same as stock prev bar.
```

### 10.7 Options Daily Ticker Summary

```
ENDPOINT: GET /v1/open-close/{optionsTicker}/{date}
DESCRIPTION: Daily open/close for an option contract with pre/post market.
DELIVERY: REST
FIELDS/PARAMETERS: Same as stock daily summary.
```

### 10.8 Options Last Trade

```
ENDPOINT: GET /v2/last/trade/{optionsTicker}
DESCRIPTION: Most recent trade for an option contract.
DELIVERY: REST
FIELDS/PARAMETERS: Same as stock last trade.
```

### 10.9 All Option Contracts

```
ENDPOINT: GET /v3/reference/options/contracts
DESCRIPTION: Reference data for all option contracts (filterable by underlying).
DELIVERY: REST
FIELDS RETURNED:
  results[].cfi                    (string) — CFI code (e.g. OCASPS)
  results[].contract_type          (string) — call|put
  results[].exercise_style         (string) — american|european
  results[].expiration_date        (string) — YYYY-MM-DD
  results[].primary_exchange       (string) — MIC code
  results[].shares_per_contract    (integer)
  results[].strike_price           (number)
  results[].ticker                 (string) — OCC symbol
  results[].underlying_ticker      (string)
PARAMETERS:
  underlying_ticker  (string, optional)
  contract_type      (string, optional)
  expiration_date    (string, optional) — with range ops
  strike_price       (number, optional) — with range ops
  expired            (boolean, optional)
  order              (string, optional)
  limit              (integer, optional) — default 10, max 1000
  sort               (string, optional)
HOURS: N/A
PAGINATION: cursor-based
```

### 10.10 Single Contract Overview

```
ENDPOINT: GET /v3/reference/options/contracts/{options_ticker}
DESCRIPTION: Full metadata for a single option contract.
DELIVERY: REST
FIELDS RETURNED: Same as all contracts results[] for one contract, plus additional_underlyings.
PARAMETERS:
  options_ticker  (string, required)
  as_of           (string, optional) — point-in-time date
```

---

## 11. BENZINGA — News

```
ENDPOINT: GET /benzinga/v2/news
DESCRIPTION: Real-time Benzinga news articles with full body, tickers, tags.
DELIVERY: REST
SUBSCRIPTION: Benzinga News ($99/m) — VERIFIED 200
FIELDS RETURNED:
  results[].benzinga_id      (integer)
  results[].author           (string)
  results[].published        (string) — ISO 8601
  results[].last_updated     (string) — ISO 8601
  results[].title            (string)
  results[].teaser           (string) — short summary
  results[].body             (string) — full HTML body
  results[].url              (string) — Benzinga article URL
  results[].images           (array)  — image URLs
  results[].channels         (array[string]) — e.g. news, hot-stories
  results[].tickers          (array[string]) — mentioned tickers
  results[].tags             (array[string]) — topic tags
PARAMETERS:
  tickers         (string, optional) — comma-separated
  topics          (string, optional)
  channels        (string, optional)
  published.gte/gt/lte/lt (string, optional) — ISO date
  updated.gte/gt/lte/lt (string, optional)
  order           (string, optional) — asc|desc
  limit           (integer, optional) — default 10, max 100
  sort            (string, optional) — published|updated
HOURS: N/A (24/7 news)
HISTORICAL DEPTH: years of archive
REAL-TIME: yes (near real-time)
RATE LIMIT: ~100/min observed
PAGINATION: cursor-based
```

---

## 12. BENZINGA — Earnings

```
ENDPOINT: GET /benzinga/v1/earnings
DESCRIPTION: Earnings calendar with actuals, estimates, revenue data.
DELIVERY: REST
SUBSCRIPTION: Benzinga Earnings ($99/m) — VERIFIED 200
FIELDS RETURNED:
  results[].currency          (string) — USD
  results[].date_status       (string) — confirmed|unconfirmed
  results[].actual_eps        (number)
  results[].previous_eps      (number)
  results[].eps_method        (string) — gaap|non_gaap
  results[].benzinga_id       (string)
  results[].importance        (integer) — 0-5
  results[].company_name      (string)
  results[].fiscal_period     (string) — Q1/Q2/Q3/Q4/FY
  results[].fiscal_year       (integer)
  results[].actual_revenue    (number)
  results[].previous_revenue  (number)
  results[].revenue_method    (string) — gaap|non_gaap
  results[].ticker            (string)
  results[].last_updated      (string) — ISO 8601
  results[].date              (string) — YYYY-MM-DD (earnings date)
  results[].time              (string) — HH:MM:SS (earnings time)
PARAMETERS:
  tickers         (string, optional) — comma-separated
  date            (string, optional) — YYYY-MM-DD
  date.gte/gt/lte/lt (string, optional)
  date_status     (string, optional) — confirmed|unconfirmed
  importance      (integer, optional) — 0-5
  order           (string, optional)
  limit           (integer, optional) — default 10, max 100
  sort            (string, optional)
HOURS: N/A
HISTORICAL DEPTH: years of earnings data
REAL-TIME: yes (updated on report)
RATE LIMIT: ~100/min
PAGINATION: cursor-based
SAMPLE: {"currency":"USD","date_status":"confirmed","actual_eps":-0.04,"ticker":"SNT","date":"2026-05-26"}
```

---

## 13. BENZINGA — Other Partner Endpoints

### 13.1 Analyst Ratings (403 — NOT SUBSCRIBED)

```
ENDPOINT: GET /benzinga/v1/ratings
SUBSCRIPTION: Benzinga Ratings (separate bolt-on) — 403 for Anish
```

### 13.2 Consensus Ratings (403 — NOT SUBSCRIBED)

```
ENDPOINT: GET /benzinga/v1/consensus-ratings/{ticker}
SUBSCRIPTION: Benzinga Ratings (separate bolt-on) — 403 for Anish
```

### 13.3 Analyst Insights (403 — NOT SUBSCRIBED)

```
ENDPOINT: GET /benzinga/v1/analyst-insights
SUBSCRIPTION: Benzinga Analyst Insights — 403 for Anish
```

### 13.4 Corporate Guidance (403 — NOT SUBSCRIBED)

```
ENDPOINT: GET /benzinga/v1/guidance
SUBSCRIPTION: Benzinga Guidance — 403 for Anish
```

### 13.5 Analyst Details

```
ENDPOINT: GET /benzinga/v1/analysts
DESCRIPTION: Reference data for Benzinga-tracked analysts.
SUBSCRIPTION: may require Ratings — status TBD
```

### 13.6 Firm Details

```
ENDPOINT: GET /benzinga/v1/firms
DESCRIPTION: Reference data for analyst firms.
SUBSCRIPTION: may require Ratings — status TBD
```

### 13.7 Bulls Bears Say

```
ENDPOINT: GET /benzinga/v1/bulls-bears-say
DESCRIPTION: Bull/bear case summaries for tickers.
SUBSCRIPTION: may require Ratings — status TBD
```

---

## 14. ETF GLOBAL — Constituents

```
ENDPOINT: GET /etf-global/v1/constituents
DESCRIPTION: ETF holdings with constituent tickers, weights, market values.
DELIVERY: REST
SUBSCRIPTION: ETF Global Constituents ($99/m) — VERIFIED 200
FIELDS RETURNED:
  results[].processed_date       (string) — YYYY-MM-DD
  results[].composite_ticker     (string) — ETF identifier
  results[].constituent_ticker   (string) — holding ticker
  results[].constituent_name     (string) — holding name
  results[].market_value         (number) — USD value
  results[].shares_held          (number) — shares
  results[].currency_traded      (string) — USD
  results[].constituent_rank     (integer) — rank by weight
  results[].effective_date       (string) — YYYY-MM-DD
PARAMETERS:
  composite_ticker      (string, optional)
  composite_ticker.any_of (string, optional)
  constituent_ticker    (string, optional)
  constituent_ticker.any_of (string, optional)
  effective_date        (string, optional) — with range ops
  processed_date        (string, optional)
  order                 (string, optional)
  limit                 (integer, optional) — default 100, max 5000
  sort                  (string, optional)
HOURS: N/A (daily/weekly update)
HISTORICAL DEPTH: 2024+ (observed)
REAL-TIME: no (daily lag)
RATE LIMIT: unlimited
PAGINATION: cursor-based
```

---

## 15. ETF GLOBAL — Fund Flows

```
ENDPOINT: GET /etf-global/v1/fund-flows
DESCRIPTION: Daily ETF fund flow data (inflows/outflows, NAV, shares outstanding).
DELIVERY: REST
SUBSCRIPTION: ETF Global Fund Flows ($99/m) — VERIFIED 200
FIELDS RETURNED:
  results[].processed_date       (string)
  results[].effective_date       (string)
  results[].composite_ticker     (string) — ETF ticker
  results[].shares_outstanding   (number)
  results[].nav                  (number) — net asset value per share
  results[].fund_flow            (number) — daily flow (positive = inflow)
PARAMETERS:
  composite_ticker      (string, optional) — with range ops
  composite_ticker.any_of (string, optional)
  effective_date        (string, optional) — with range ops
  processed_date        (string, optional)
  order                 (string, optional)
  limit                 (integer, optional) — default 100, max 5000
  sort                  (string, optional)
HOURS: N/A (daily)
HISTORICAL DEPTH: 2024+ (observed)
REAL-TIME: no (T+1)
RATE LIMIT: unlimited
PAGINATION: cursor-based
SAMPLE: {"processed_date":"2024-12-12","composite_ticker":"BRKD","shares_outstanding":100001,"nav":25.22,"fund_flow":0.0}
```

---

## 16. ETF GLOBAL — Other (403 unless subscribed)

### 16.1 ETF Taxonomies (403)

```
ENDPOINT: GET /etf-global/v1/taxonomies
SUBSCRIPTION: ETF Global Taxonomies — 403 for Anish
```

### 16.2 ETF Profiles & Exposure (403)

```
ENDPOINT: GET /etf-global/v1/profiles
SUBSCRIPTION: ETF Global Profiles — 403 for Anish
```

### 16.3 ETF Analytics (403)

```
ENDPOINT: GET /etf-global/v1/analytics
SUBSCRIPTION: ETF Global Analytics — 403 for Anish
```

---

## 17. NYSE ORDER IMBALANCE (NOI)

```
ENDPOINT: WebSocket channel NOI.<symbol> on wss://socket.massive.com/stocks
DESCRIPTION: Net Order Imbalance data from NYSE/Nasdaq opening/closing auctions and halt auctions.
DELIVERY: WebSocket ONLY — no REST, no S3 historical. Forward-capture only.
SUBSCRIPTION: Order Imbalances ($49/m) — VERIFIED ACTIVE
FIELDS RETURNED (per WS message):
  ev                    (string)  — "NOI"
  sym                   (string)  — ticker symbol
  t                     (integer) — timestamp (ns)
  T                     (string)  — tape (A/B/C)
  imbalance_quantity    (number)  — net imbalance shares
  paired_quantity       (number)  — shares that can be paired at auction
  book_clearing_price   (number)  — price that would clear the book
  auction_type          (string)  — M (market open), C (market close), H (halt)
  reference_price       (number)  — reference price for the auction
  far_price             (number)  — far clearing price
  near_price            (number)  — near clearing price
  imbalance_side        (string)  — B (buy), S (sell), N (none)
CONNECTION:
  1. Connect: wss://socket.massive.com/stocks
  2. Auth: {"action":"auth","params":"<MASSIVE_API_KEY>"}
  3. Subscribe: {"action":"subscribe","params":"NOI.*"} (all symbols) or "NOI.AAPL" (single)
HOURS: fires during auction windows (9:28-9:30 ET open, 15:50-16:00 ET close, halt auctions)
HISTORICAL DEPTH: NONE — WebSocket-only, forward capture. Every minute offline = data lost forever.
REAL-TIME: yes
RATE LIMIT: N/A (streaming)
PAGINATION: N/A (streaming)
CRITICAL: Anish's launchd capturer (realtime/noi_capturer.py) MUST be running 24/7.
```

---

## 18. FUTURES

### 18.1 Futures Aggregate Bars

```
ENDPOINT: GET /futures/v1/aggs/{ticker}
DESCRIPTION: OHLCV bars for futures contracts. Timestamps in Central Time.
DELIVERY: REST
FIELDS RETURNED:
  results[].close              (number)
  results[].dollar_volume      (number)
  results[].high               (number)
  results[].low                (number)
  results[].open               (number)
  results[].session_end_date   (string) — YYYY-MM-DD (trading date)
  results[].settlement_price   (number)
  results[].ticker             (string)
  results[].transactions       (integer)
  results[].volume             (integer) — contracts
  results[].window_start       (integer) — nanosecond timestamp
PARAMETERS:
  ticker          (string, required) — e.g. ESZ4, GCJ5
  resolution      (string, optional) — e.g. 1sec, 5min, 1hour, 1session, 1week, 1month
  window_start    (string, optional) — YYYY-MM-DD or ns timestamp
  window_start.gte/gt/lte/lt (string, optional)
  limit           (integer, optional) — default 1000, max 50000
  sort            (string, optional)
HOURS: futures trading hours (nearly 24h Sun-Fri)
HISTORICAL DEPTH: CME history
REAL-TIME: yes (Futures Basic)
PAGINATION: cursor-based
```

### 18.2 Futures Snapshot

```
ENDPOINT: GET /futures/v1/snapshot
DESCRIPTION: Real-time snapshot for futures contracts.
DELIVERY: REST
FIELDS RETURNED:
  results[].ticker                   (string)
  results[].product_code             (string)
  results[].details.open_interest    (number)
  results[].details.settlement_date  (integer) — ns
  results[].last_minute.close/high/low/open/volume (number)
  results[].last_minute.last_updated (integer)
  results[].last_quote.ask/ask_size/ask_timestamp   (number/integer)
  results[].last_quote.bid/bid_size/bid_timestamp   (number/integer)
  results[].last_quote.last_updated  (integer)
  results[].last_trade.price/size/last_updated (number)
  results[].session.change/change_percent (number)
  results[].session.close/high/low/open/volume (number)
  results[].session.previous_settlement (number)
  results[].session.settlement_price    (number)
PARAMETERS:
  product_code     (string, optional) — with range ops and .any_of
  ticker           (string, optional) — with range ops and .any_of
  limit            (integer, optional) — default 100, max 50000
  sort             (string, optional)
HOURS: futures hours
REAL-TIME: yes
PAGINATION: cursor-based
```

### 18.3 Futures Trades

```
ENDPOINT: GET /futures/v1/trades/{ticker}
DESCRIPTION: Tick-level trade data for a futures contract.
DELIVERY: REST
FIELDS RETURNED:
  results[].channel          (integer) — CME multicast channel
  results[].price            (number)
  results[].report_sequence  (integer)
  results[].sequence_number  (integer)
  results[].session_end_date (string)
  results[].size             (integer) — contracts
  results[].ticker           (string)
  results[].timestamp        (integer) — nanoseconds
PARAMETERS:
  ticker           (string, required)
  timestamp        (string, optional) — ns or YYYY-MM-DD or ISO 8601
  timestamp.gte/gt/lte/lt
  session_end_date (string, optional)
  limit            (integer, optional) — default 10, max 49999
  sort             (string, optional)
HOURS: futures hours
PAGINATION: cursor-based
```

### 18.4 Futures Quotes

```
ENDPOINT: GET /futures/v1/quotes/{ticker}
DESCRIPTION: BBO quote data for a futures contract.
DELIVERY: REST
FIELDS RETURNED:
  results[].ask_price         (number)
  results[].ask_size          (integer) — contracts
  results[].ask_timestamp     (integer) — ns
  results[].bid_price         (number)
  results[].bid_size          (integer)
  results[].bid_timestamp     (integer) — ns
  results[].channel           (integer)
  results[].report_sequence   (integer)
  results[].sequence_number   (integer)
  results[].session_end_date  (string)
  results[].ticker            (string)
  results[].timestamp         (integer) — ns
PARAMETERS: Same as futures trades.
PAGINATION: cursor-based
```

### 18.5 Futures Contracts (Reference)

```
ENDPOINT: GET /futures/v1/contracts
DESCRIPTION: Contract specifications and index.
DELIVERY: REST
FIELDS RETURNED:
  results[].active              (boolean)
  results[].date                (string)
  results[].days_to_maturity    (integer)
  results[].first_trade_date    (string)
  results[].group_code          (string)
  results[].last_trade_date     (string)
  results[].max_order_quantity   (integer)
  results[].min_order_quantity   (integer)
  results[].name                (string)
  results[].product_code        (string)
  results[].settlement_date     (string)
  results[].settlement_tick_size (number)
  results[].spread_tick_size    (number)
  results[].ticker              (string)
  results[].trade_tick_size     (number)
  results[].trading_venue       (string) — MIC code
  results[].type                (string) — single|combo
PARAMETERS:
  date, product_code, ticker, active, type, first_trade_date, last_trade_date — all with range ops
  limit (max 1000), sort
PAGINATION: cursor-based
```

### 18.6 Futures Products (Reference)

```
ENDPOINT: GET /futures/v1/products
DESCRIPTION: Futures product specifications.
DELIVERY: REST
FIELDS RETURNED:
  results[].asset_class              (string) — commodity, equity, etc.
  results[].asset_sub_class          (string) — energy, metals, etc.
  results[].date                     (string)
  results[].last_updated             (string)
  results[].name                     (string)
  results[].price_quotation          (string)
  results[].product_code             (string)
  results[].sector                   (string)
  results[].settlement_currency_code (string)
  results[].settlement_method        (string) — financially_settled|deliverable
  results[].settlement_type          (string) — cash|physical
  results[].sub_sector               (string)
  results[].trade_currency_code      (string)
  results[].trading_venue            (string) — MIC
  results[].type                     (string) — single|combo
  results[].unit_of_measure          (string)
  results[].unit_of_measure_qty      (number)
PARAMETERS:
  name, product_code, date, trading_venue, sector, sub_sector, asset_class, asset_sub_class, type — with range and .any_of
  limit (max 50000), sort
PAGINATION: cursor-based
```

### 18.7 Futures Exchanges

```
ENDPOINT: GET /futures/v1/exchanges
DELIVERY: REST
FIELDS: results[].acronym, id, locale, mic, name, operating_mic, type, url
PARAMETERS: limit (max 999)
```

### 18.8 Futures Market Status

```
ENDPOINT: GET /futures/v1/market-status
DELIVERY: REST
FIELDS: results[].market_event, name, product_code, session_end_date, timestamp, trading_venue
PARAMETERS: product_code (with range ops), limit (max 99)
```

### 18.9 Futures Schedules

```
ENDPOINT: GET /futures/v1/schedules
DELIVERY: REST
FIELDS: results[].event, product_code, product_name, session_end_date, timestamp, trading_venue
PARAMETERS: product_code, session_end_date, trading_venue — with range ops; limit (max 1000), sort
```

---

## 19. FOREX

### 19.1 Forex Custom Bars

```
ENDPOINT: GET /v2/aggs/ticker/{forexTicker}/range/{multiplier}/{timespan}/{from}/{to}
FIELDS/PARAMETERS: Same as stocks aggs. Ticker format: C:EURUSD
```

### 19.2 Forex Previous Day Bar

```
ENDPOINT: GET /v2/aggs/ticker/{forexTicker}/prev
```

### 19.3 Forex Last Quote

```
ENDPOINT: GET /v1/last_quote/currencies/{from}/{to}
DESCRIPTION: Real-time last quote for a currency pair.
DELIVERY: REST
FIELDS: results.ask, bid, exchange, timestamp
PARAMETERS: from (string, required), to (string, required)
```

### 19.4 Forex Quotes (Historical)

```
ENDPOINT: GET /v3/quotes/{fxTicker}
FIELDS/PARAMETERS: Same as stock quotes. Ticker format: C:EURUSD
```

### 19.5 Forex Single Ticker Snapshot

```
ENDPOINT: GET /v2/snapshot/locale/global/markets/forex/tickers/{ticker}
```

### 19.6 Forex Full Market Snapshot

```
ENDPOINT: GET /v2/snapshot/locale/global/markets/forex/tickers
```

### 19.7 Forex Top Movers

```
ENDPOINT: GET /v2/snapshot/locale/global/markets/forex/{direction}
PARAMETERS: direction — gainers|losers
```

### 19.8 Forex Daily Market Summary

```
ENDPOINT: GET /v2/aggs/grouped/locale/global/market/fx/{date}
DESCRIPTION: All forex pairs daily bars for one date.
```

### 19.9 Currency Conversion

```
ENDPOINT: GET /v1/conversion/{from}/{to}
DESCRIPTION: Real-time currency conversion.
FIELDS: converted, from, initialAmount, last.ask, last.bid, last.exchange, last.timestamp, to
PARAMETERS: from (required), to (required), amount (optional), precision (optional)
```

### 19.10 Forex Technical Indicators

```
GET /v1/indicators/sma/{fxTicker}
GET /v1/indicators/ema/{fxTicker}
GET /v1/indicators/rsi/{fxTicker}
GET /v1/indicators/macd/{fxTicker}
Same structure as stocks.
```

---

## 20. CRYPTO

### 20.1 Crypto Custom Bars

```
ENDPOINT: GET /v2/aggs/ticker/{cryptoTicker}/range/{multiplier}/{timespan}/{from}/{to}
Ticker format: X:BTCUSD
```

### 20.2 Crypto Previous Day Bar

```
ENDPOINT: GET /v2/aggs/ticker/{cryptoTicker}/prev
```

### 20.3 Crypto Trades (Historical)

```
ENDPOINT: GET /v3/trades/{cryptoTicker}
```

### 20.4 Crypto Last Trade

```
ENDPOINT: GET /v1/last/crypto/{from}/{to}
FIELDS: last.price, size, exchange, conditions, timestamp
```

### 20.5 Crypto Daily Ticker Summary

```
ENDPOINT: GET /v1/open-close/crypto/{from}/{to}/{date}
```

### 20.6 Crypto Single Ticker Snapshot

```
ENDPOINT: GET /v2/snapshot/locale/global/markets/crypto/tickers/{ticker}
```

### 20.7 Crypto Full Market Snapshot

```
ENDPOINT: GET /v2/snapshot/locale/global/markets/crypto/tickers
```

### 20.8 Crypto Top Movers

```
ENDPOINT: GET /v2/snapshot/locale/global/markets/crypto/{direction}
```

### 20.9 Crypto Daily Market Summary

```
ENDPOINT: GET /v2/aggs/grouped/locale/global/market/crypto/{date}
```

### 20.10 Crypto Technical Indicators

```
GET /v1/indicators/sma/{cryptoTicker}
GET /v1/indicators/ema/{cryptoTicker}
GET /v1/indicators/rsi/{cryptoTicker}
GET /v1/indicators/macd/{cryptoTicker}
```

---

## 21. INDICES

### 21.1 Indices Custom Bars

```
ENDPOINT: GET /v2/aggs/ticker/{indicesTicker}/range/{multiplier}/{timespan}/{from}/{to}
Ticker format: I:SPX, I:NDX, I:DJI, I:RUT
```

### 21.2 Indices Previous Day Bar

```
ENDPOINT: GET /v2/aggs/ticker/{indicesTicker}/prev
```

### 21.3 Indices Snapshot

```
ENDPOINT: GET /v3/snapshot/indices
DESCRIPTION: Snapshot for one or more indices.
FIELDS RETURNED:
  results[].ticker           (string)
  results[].name             (string)
  results[].value            (number) — current index value
  results[].last_updated     (integer) — ns
  results[].market_status    (string)
  results[].type             (enum: indices)
  results[].timeframe        (string) — REAL-TIME|DELAYED
  results[].session.change   (number)
  results[].session.change_percent (number)
  results[].session.close    (number)
  results[].session.high     (number)
  results[].session.low      (number)
  results[].session.open     (number)
  results[].session.previous_close (number)
PARAMETERS:
  ticker.any_of (max 250), ticker range ops, order, limit (max 250), sort
```

### 21.4 Indices Daily Ticker Summary

```
ENDPOINT: GET /v1/open-close/{indicesTicker}/{date}
FIELDS: afterHours, close, from, high, low, open, preMarket, status, symbol
```

### 21.5 Indices Technical Indicators

```
GET /v1/indicators/sma/{indicesTicker}
GET /v1/indicators/ema/{indicesTicker}
GET /v1/indicators/rsi/{indicesTicker}
GET /v1/indicators/macd/{indicesTicker}
```

---

## 22. ECONOMY / MACRO

### 22.1 Treasury Yields

```
ENDPOINT: GET /fed/v1/treasury-yields
DESCRIPTION: Daily U.S. Treasury yields from 1-month to 30-year maturities.
DELIVERY: REST
FIELDS RETURNED:
  results[].date             (string) — YYYY-MM-DD
  results[].yield_1_month    (number)
  results[].yield_3_month    (number)
  results[].yield_6_month    (number)
  results[].yield_1_year     (number)
  results[].yield_2_year     (number)
  results[].yield_3_year     (number)
  results[].yield_5_year     (number)
  results[].yield_7_year     (number)
  results[].yield_10_year    (number)
  results[].yield_20_year    (number)
  results[].yield_30_year    (number)
PARAMETERS:
  date              (string, optional) — with range ops and .any_of
  limit             (integer, optional) — default 100, max 50000
  sort              (string, optional)
HOURS: N/A
HISTORICAL DEPTH: 1962 to present
REAL-TIME: no (daily)
PAGINATION: cursor-based
SAMPLE: {"date":"2026-05-21","yield_1_month":3.72,"yield_10_year":4.57,"yield_30_year":5.1}
```

### 22.2 Inflation

```
ENDPOINT: GET /fed/v1/inflation
DESCRIPTION: Realized inflation indicators (CPI, PCE).
DELIVERY: REST
FIELDS RETURNED:
  results[].date               (string)
  results[].cpi                (number) — CPI index value
  results[].cpi_core           (number) — CPI ex food & energy
  results[].cpi_year_over_year (number) — YoY % change
  results[].pce                (number) — PCE price index
  results[].pce_core           (number) — Core PCE (Fed's preferred)
  results[].pce_spending       (number) — nominal PCE in $B
PARAMETERS: date with range ops, limit (max 50000), sort
HISTORICAL DEPTH: decades
PAGINATION: cursor-based
```

### 22.3 Inflation Expectations

```
ENDPOINT: GET /fed/v1/inflation-expectations
DESCRIPTION: Market-based and model-based inflation expectations.
DELIVERY: REST
FIELDS RETURNED:
  results[].date                  (string)
  results[].market_5_year         (number) — 5yr breakeven rate
  results[].market_10_year        (number) — 10yr breakeven rate
  results[].forward_years_5_to_10 (number) — 5yr/5yr forward
  results[].model_1_year          (number) — Cleveland Fed 1yr
  results[].model_5_year          (number) — Cleveland Fed 5yr
  results[].model_10_year         (number) — Cleveland Fed 10yr
  results[].model_30_year         (number) — Cleveland Fed 30yr
PARAMETERS: date with range ops, limit (max 50000), sort
PAGINATION: cursor-based
```

### 22.4 Labor Market

```
ENDPOINT: GET /fed/v1/labor-market
DESCRIPTION: Key labor market indicators from the Federal Reserve.
DELIVERY: REST
FIELDS RETURNED:
  results[].date                            (string)
  results[].unemployment_rate               (number) — UNRATE
  results[].labor_force_participation_rate  (number) — CIVPART
  results[].avg_hourly_earnings             (number) — CES0500000003
  results[].job_openings                    (number) — JTSJOL (thousands)
PARAMETERS: date with range ops, limit (max 50000), sort
HISTORICAL DEPTH: decades (FRED sourced)
PAGINATION: cursor-based
```

---

## 23. ALTERNATIVE DATA — Consumer Spending (EU)

### 23.1 Merchant Aggregates

```
ENDPOINT: GET /consumer-spending/eu/v1/merchant-aggregates
DESCRIPTION: European consumer spending data (Fable Data). Daily card/banking transactions for ~250 US public companies across 6 EU countries.
DELIVERY: REST
SUBSCRIPTION: probe needed (may be 403 for Anish — listed in community examples but not in KNOWN_SUBSCRIPTIONS)
FIELDS RETURNED:
  results[].transaction_date                          (string)
  results[].name                                      (string) — merchant name (lowercase)
  results[].parent_name                               (string) — parent company
  results[].merchant_ticker                           (string) — Bloomberg ticker
  results[].merchant_industry                         (string) — GICS/BICS/ICB
  results[].mcc_group                                 (string) — merchant category
  results[].user_country                              (string) — UK|DE|FR|ES|IT|AT
  results[].channel                                   (string) — online|offline|bnpl
  results[].consumer_type                             (string) — consumer_credit|consumer_debit|open_banking
  results[].transaction_currency                      (string) — EUR|GBP
  results[].total_spend                               (number) — net (usually negative)
  results[].total_transactions                        (integer)
  results[].total_accounts                            (integer)
  results[].spend_out_spend                           (number) — purchases (negative)
  results[].spend_out_transaction_count               (integer)
  results[].spend_out_distinct_account_key_count      (integer)
  results[].spend_in_spend                            (number) — refunds (positive)
  results[].spend_in_transaction_count                (integer)
  results[].spend_in_distinct_account_key_count       (integer)
  results[].eight_day_rolling_category_accounts       (integer) — for normalization
  results[].eight_day_rolling_total_accounts          (integer)
  results[].twenty_eight_day_rolling_category_accounts (integer)
  results[].twenty_eight_day_rolling_total_accounts   (integer)
  results[].published_date                            (string) — ~7 days after transaction
  results[].type                                      (string) — merchant|payment_processor
PARAMETERS:
  transaction_date, name, user_country, channel, consumer_type, parent_name — with range ops and .any_of
  limit (max 5000), sort
HISTORICAL DEPTH: 2016+ (Spain 2019+)
PAGINATION: cursor-based
```

### 23.2 Merchant Hierarchy

```
ENDPOINT: GET /consumer-spending/eu/v1/merchant-hierarchy
DESCRIPTION: Reference mapping merchants to parent companies, tickers, sectors.
DELIVERY: REST
FIELDS RETURNED:
  results[].lookup_name              (string) — lowercase merchant tag
  results[].normalized_name          (string) — display name
  results[].ticker                   (string) — Bloomberg ticker
  results[].parent_name              (string)
  results[].parent_ticker            (string)
  results[].grandparent_name         (string)
  results[].grandparent_ticker       (string)
  results[].great_grandparent_name   (string)
  results[].great_grandparent_ticker (string)
  results[].category                 (string)
  results[].sector                   (string)
  results[].industry_group           (string)
  results[].industry                 (string)
  results[].sub_industry             (string)
  results[].listing_status           (string) — public|private
  results[].active_from              (string) — YYYY-MM-DD
  results[].active_to                (string) — YYYY-MM-DD (9999-12-31 = active)
PARAMETERS:
  lookup_name, ticker, listing_status, active_from, active_to — with range ops
  limit (max 50000), sort
PAGINATION: cursor-based
```

---

## 24. TMX — Corporate Events

```
ENDPOINT: GET /tmx/v1/corporate-events
DESCRIPTION: Wall Street Horizon corporate event calendar.
SUBSCRIPTION: TMX Corporate Events — 403 for Anish (NOT subscribed)
FIELDS RETURNED (from docs):
  results[].date                 (string)
  results[].type                 (string) — earnings_announcement_date|stock_split|dividend|conference|etc.
  results[].status               (string) — confirmed|pending|canceled
  results[].ticker               (string)
  results[].isin                 (string)
  results[].company_name         (string)
  results[].event_details        (string)
  results[].source_url           (string)
  results[].timestamp            (string)
PARAMETERS:
  date, type, ticker, isin, status — with range ops
  limit, sort
```

---

## 25. REFERENCE DATA

### 25.1 All Tickers

```
ENDPOINT: GET /v3/reference/tickers
DESCRIPTION: Ticker universe across all asset classes.
DELIVERY: REST
FIELDS RETURNED:
  results[].ticker                   (string)
  results[].name                     (string)
  results[].market                   (string) — stocks|crypto|fx|otc
  results[].locale                   (string) — us|global
  results[].primary_exchange         (string) — MIC code
  results[].type                     (string) — CS|ET|ADRC|FUND|...
  results[].active                   (boolean)
  results[].currency_name            (string)
  results[].currency_symbol          (string) — ISO 4217
  results[].base_currency_name       (string) — for FX/crypto
  results[].base_currency_symbol     (string)
  results[].cik                      (string)
  results[].composite_figi           (string)
  results[].share_class_figi         (string)
  results[].last_updated_utc         (string)
  results[].delisted_utc             (string)
PARAMETERS:
  ticker (with range ops), type, market, exchange, cusip, cik, date, search, active
  order, limit (max 1000), sort
PAGINATION: cursor-based
```

### 25.2 Ticker Overview (Single)

```
ENDPOINT: GET /v3/reference/tickers/{ticker}
DESCRIPTION: Comprehensive details for one ticker.
FIELDS RETURNED:
  results.ticker, name, market, locale, primary_exchange, type, active
  results.cik, composite_figi, share_class_figi
  results.currency_name, description, homepage_url
  results.address.address1, city, state, postal_code
  results.branding.logo_url, icon_url
  results.list_date, market_cap, phone_number
  results.round_lot, sic_code, sic_description
  results.share_class_shares_outstanding, weighted_shares_outstanding
  results.total_employees, ticker_root, ticker_suffix
  results.delisted_utc
PARAMETERS:
  ticker (required), date (optional — point-in-time)
```

### 25.3 Ticker Events

```
ENDPOINT: GET /vX/reference/tickers/{id}/events
DESCRIPTION: Corporate events for a ticker (name changes, splits, etc.).
FIELDS RETURNED:
  results[].name             (string) — company name at that time
  results[].composite_figi   (string)
  results[].cik              (string)
  results[].ticker_change_ticker (string)
  results[].type             (string) — ticker_change|split|etc.
  results[].date             (string) — YYYY-MM-DD
PARAMETERS:
  id (string, required) — ticker symbol
  types (string, optional) — filter by event type
```

### 25.4 Ticker Types

```
ENDPOINT: GET /v3/reference/tickers/types
FIELDS: results[].code, description, asset_class, locale
PARAMETERS: asset_class (optional), locale (optional)
```

### 25.5 Exchanges

```
ENDPOINT: GET /v3/reference/exchanges
FIELDS: results[].id, type, asset_class, locale, name, acronym, mic, operating_mic, participant_id, url
PARAMETERS: asset_class (optional), locale (optional)
```

### 25.6 Condition Codes

```
ENDPOINT: GET /v3/reference/conditions
DESCRIPTION: Mapping of condition code IDs to names and descriptions.
FIELDS RETURNED:
  results[].id              (integer) — condition ID
  results[].type            (string) — regular|buy_or_sell_side|etc.
  results[].name            (string) — condition name
  results[].asset_class     (string) — stocks|options|crypto
  results[].data_types      (array[string]) — trade|nbbo
  results[].description     (string)
PARAMETERS:
  asset_class, data_type, id, sip — with operators
  order, limit, sort
PAGINATION: cursor-based
SAMPLE: {"id":1,"type":"buy_or_sell_side","name":"Sell Side","asset_class":"crypto","data_types":["trade"]}
```

### 25.7 Market Status (Real-Time)

```
ENDPOINT: GET /v1/marketstatus/now
DESCRIPTION: Real-time status of all markets.
FIELDS RETURNED:
  afterHours                        (boolean)
  earlyHours                        (boolean)
  market                            (string) — extended-hours|open|closed
  serverTime                        (string) — RFC3339
  exchanges.nasdaq                  (string)
  exchanges.nyse                    (string)
  exchanges.otc                     (string)
  currencies.crypto                 (string)
  currencies.fx                     (string)
  indicesGroups.s_and_p             (string)
  indicesGroups.nasdaq              (string)
  indicesGroups.dow_jones           (string)
  indicesGroups.ftse_russell        (string)
  indicesGroups.msci                (string)
  indicesGroups.mstar               (string)
  indicesGroups.mstarc              (string)
  indicesGroups.cccy                (string)
  indicesGroups.cgi                 (string)
  indicesGroups.societe_generale    (string)
```

### 25.8 Market Holidays

```
ENDPOINT: GET /v1/marketstatus/upcoming
DESCRIPTION: Upcoming market holidays and closures (forward-looking only).
FIELDS RETURNED:
  [].date       (string)
  [].exchange   (string) — NYSE|NASDAQ|OTC
  [].name       (string) — holiday name
  [].status     (string) — closed|early-close
  [].open       (string) — open time (if early close)
  [].close      (string) — close time (if early close)
```

### 25.9 Related Tickers

```
ENDPOINT: GET /v1/related-companies/{ticker}
DESCRIPTION: Peer tickers identified by news co-occurrence and return correlation.
FIELDS RETURNED:
  results[].ticker  (string)
PARAMETERS:
  ticker (string, required)
SAMPLE: AAPL -> [MSFT, AMZN, GOOGL, GOOG, NVDA, TSLA, META, NFLX, DIS, BRK.B]
```

### 25.10 News (Reference)

```
ENDPOINT: GET /v2/reference/news
DESCRIPTION: Aggregated news with sentiment and insights from multiple publishers.
FIELDS RETURNED:
  results[].id                          (string) — hash ID
  results[].publisher.name              (string)
  results[].publisher.homepage_url      (string)
  results[].publisher.logo_url          (string)
  results[].publisher.favicon_url       (string)
  results[].title                       (string)
  results[].author                      (string)
  results[].published_utc               (string)
  results[].article_url                 (string)
  results[].tickers                     (array[string])
  results[].image_url                   (string)
  results[].description                 (string)
  results[].keywords                    (array[string])
  results[].insights                    (array[object])
  results[].insights[].ticker           (string)
  results[].insights[].sentiment        (string) — positive|negative|neutral
  results[].insights[].sentiment_reasoning (string)
PARAMETERS:
  ticker.any_of, published_utc.gte/gt/lte/lt, order, limit (max 1000), sort
NOTE: This is a different endpoint from /benzinga/v2/news. This aggregates from multiple publishers (GlobeNewswire, Business Wire, etc.) with AI-generated insights and sentiment.
PAGINATION: cursor-based
```

---

## 26. WEBSOCKET CHANNELS (All Markets)

Connect: `wss://socket.massive.com/<market>` where market = stocks|options|crypto|forex|indices|futures
Auth: `{"action":"auth","params":"<MASSIVE_API_KEY>"}`
Subscribe: `{"action":"subscribe","params":"<CHANNEL>.<symbol>"}`
Use `*` wildcard for all symbols: `T.*`, `NOI.*`, etc.

### Stocks (wss://socket.massive.com/stocks)

| Channel | Event | Description | Anish Subscribed |
|---|---|---|---|
| `T.<sym>` | Trade | Real-time tick trades | YES |
| `Q.<sym>` | Quote | Real-time NBBO quotes | YES |
| `A.<sym>` | Minute Agg | 1-minute OHLCV bars | YES |
| `AM.<sym>` | Minute Agg (alt) | Alias for A | YES |
| `AS.<sym>` | Per-Second Agg | **WS-only, no historical. Forward capture only.** | YES |
| `NOI.<sym>` | Net Order Imbalance | **Auction imbalances. WS-only. $49/m.** | YES |
| `FMV.<sym>` | Fair Market Value | **Continuous synthetic price. WS-only.** | YES |
| `LULD.<sym>` | Limit Up/Limit Down | Halt events | NO (separate bolt-on) |
| `LV.<sym>` | Launchpad Value | Synthetic launchpad | YES (likely) |

### Options (wss://socket.massive.com/options)

| Channel | Event | Description |
|---|---|---|
| `T.<contract>` | Trade | Option trade ticks |
| `Q.<contract>` | Quote | Option NBBO |
| `A.<contract>` | Minute Agg | 1-minute bars |
| `AS.<contract>` | Per-Second Agg | **WS-only** |
| `FMV.<contract>` | Fair Market Value | **WS-only** |

### Crypto (wss://socket.massive.com/crypto)

| Channel | Event | Description |
|---|---|---|
| `XT.<pair>` | Trade | Crypto trades |
| `XQ.<pair>` | Quote | Crypto BBO |
| `XA.<pair>` | Minute Agg | 1-minute bars |
| `XAS.<pair>` | Per-Second Agg | **WS-only** |
| `XL2.<pair>` | Level-2 Book | **Order book depth (crypto only)** |
| `XS.<pair>` | Single Quote | Consolidated snapshot |

### Forex (wss://socket.massive.com/forex)

| Channel | Event | Description |
|---|---|---|
| `C.<pair>` | Quote | FX quote |
| `CA.<pair>` | Minute Agg | 1-minute bars |
| `CAS.<pair>` | Per-Second Agg | **WS-only** |
| `FMV.<pair>` | Fair Market Value | **WS-only** |

### Indices (wss://socket.massive.com/indices)

| Channel | Event | Description |
|---|---|---|
| `V.<index>` | Value | Index value updates |
| `A.<index>` | Minute Agg | 1-minute bars |
| `AS.<index>` | Per-Second Agg | **WS-only** |

### Futures (wss://socket.massive.com/futures)

| Channel | Event | Description |
|---|---|---|
| `T.<contract>` | Trade | Futures trade ticks |
| `Q.<contract>` | Quote | Futures BBO |
| `A.<contract>` | Minute Agg | 1-minute bars |
| `AS.<contract>` | Per-Second Agg | **WS-only** |

---

## 27. S3 FLAT FILES

Base: `s3://flatfiles/` via `https://files.massive.com` with `MASSIVE_S3_*` AWS-style creds.

| Prefix | Coverage | Total Size | Anish Access |
|---|---|---|---|
| `us_stocks_sip/day_aggs_v1/` | 2003-present | 0.9 GB | YES (Stocks Advanced) |
| `us_stocks_sip/minute_aggs_v1/` | 2003-present | 78 GB | YES |
| `us_stocks_sip/trades_v1/` | 2003-present | **3.4 TB** | YES |
| `us_stocks_sip/quotes_v1/` | 2003-present | **12.8 TB** | YES |
| `us_options_opra/day_aggs_v1/` | ~2014-present | 5.5 GB | YES (Options Advanced) |
| `us_options_opra/minute_aggs_v1/` | ~2014-present | 33 GB | YES |
| `us_options_opra/trades_v1/` | ~2014-present | 74 GB | YES |
| `us_options_opra/quotes_v1/` | ~2022-present | **98 TB** | YES |
| `us_indices/` | varies | N/A | NO (Basic tier = 403 for S3) |
| `us_futures_cme/` | varies | N/A | NO (Basic tier = 403 for S3) |
| `us_futures_cbot/` | varies | N/A | NO (Basic tier = 403 for S3) |
| `us_futures_comex/` | varies | N/A | NO (Basic tier = 403 for S3) |
| `us_futures_nymex/` | varies | N/A | NO (Basic tier = 403 for S3) |
| `global_forex/` | varies | N/A | NO (Basic tier = 403 for S3) |
| `global_crypto/` | varies | N/A | NO (Basic tier = 403 for S3) |

**Schema note (CRITICAL):** Post 2026-02-23, `size`/`volume` columns are decimals. New fields: `decimal_size`, `ds`, `dv`, `dav`, `decimal_volume` — returned as strings for precision.

---

## 28. MCP apply= FUNCTIONS (Client-Side)

These run locally in the MCP process via numpy, NOT on Massive servers. Use with `call_api` or `query_data` `apply` parameter.

### Black-Scholes Greeks (6 functions)

| Function | Signature | Returns |
|---|---|---|
| `bs_price` | `bs_price(S, K, T, r, sigma, option_type?)` | Option price (Float64) |
| `bs_delta` | `bs_delta(S, K, T, r, sigma, option_type?)` | Delta: N(d1) for calls, N(d1)-1 for puts |
| `bs_gamma` | `bs_gamma(S, K, T, r, sigma)` | Gamma (same for calls/puts) |
| `bs_theta` | `bs_theta(S, K, T, r, sigma, option_type?)` | Daily theta (annual/365) |
| `bs_vega` | `bs_vega(S, K, T, r, sigma)` | Vega per 1% vol change |
| `bs_rho` | `bs_rho(S, K, T, r, sigma, option_type?)` | Rho per 1% rate change |

All take: S=spot, K=strike, T=years to expiry, r=risk-free rate, sigma=IV. option_type defaults to "call".

### Returns (5 functions)

| Function | Signature | Returns |
|---|---|---|
| `simple_return` | `simple_return(column)` | (p_t - p_{t-1}) / p_{t-1} |
| `log_return` | `log_return(column)` | log(p_t / p_{t-1}) |
| `cumulative_return` | `cumulative_return(column)` | (1+r).cumprod() - 1 |
| `sharpe_ratio` | `sharpe_ratio(column, window, rf?)` | Rolling Sharpe (mean-rf)/std |
| `sortino_ratio` | `sortino_ratio(column, window, rf?)` | Rolling Sortino (downside deviation) |

### Technical (2 functions)

| Function | Signature | Returns |
|---|---|---|
| `sma` | `sma(column, window)` | Simple moving average |
| `ema` | `ema(column, window)` | Exponential moving average (span=window) |

---

## COMPLETE ENDPOINT INDEX (De-Duplicated)

### Stocks (35 unique REST endpoints)

| # | Method | Path | Name |
|---|---|---|---|
| 1 | GET | `/v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Custom Bars |
| 2 | GET | `/v2/aggs/ticker/{stocksTicker}/prev` | Previous Day Bar |
| 3 | GET | `/v2/aggs/grouped/locale/us/market/stocks/{date}` | Daily Market Summary |
| 4 | GET | `/v1/open-close/{stocksTicker}/{date}` | Daily Ticker Summary |
| 5 | GET | `/v3/trades/{stockTicker}` | Trades |
| 6 | GET | `/v3/quotes/{stockTicker}` | Quotes |
| 7 | GET | `/v3/snapshot` | Unified Snapshot |
| 8 | GET | `/v2/snapshot/locale/us/markets/stocks/tickers/{stocksTicker}` | Single Ticker Snapshot |
| 9 | GET | `/v2/snapshot/locale/us/markets/stocks/tickers` | Full Market Snapshot |
| 10 | GET | `/v2/snapshot/locale/us/markets/stocks/{direction}` | Top Market Movers |
| 11 | GET | `/v2/last/trade/{stocksTicker}` | Last Trade |
| 12 | GET | `/v2/last/nbbo/{stocksTicker}` | Last Quote |
| 13 | GET | `/stocks/v1/short-interest` | Short Interest |
| 14 | GET | `/stocks/v1/short-volume` | Short Volume |
| 15 | GET | `/stocks/v1/splits` | Splits |
| 16 | GET | `/stocks/v1/dividends` | Dividends |
| 17 | GET | `/stocks/vX/float` | Float |
| 18 | GET | `/vX/reference/ipos` | IPOs |
| 19 | GET | `/stocks/financials/v1/income-statements` | Income Statements |
| 20 | GET | `/stocks/financials/v1/balance-sheets` | Balance Sheets |
| 21 | GET | `/stocks/financials/v1/cash-flow-statements` | Cash Flow Statements |
| 22 | GET | `/stocks/financials/v1/ratios` | Financial Ratios |
| 23 | GET | `/stocks/filings/vX/form-4` | Form 4 (Insider) |
| 24 | GET | `/stocks/filings/vX/form-3` | Form 3 (Initial Insider) |
| 25 | GET | `/stocks/filings/vX/13-F` | 13-F Filings |
| 26 | GET | `/stocks/filings/vX/risk-factors` | Risk Factors |
| 27 | GET | `/stocks/taxonomies/vX/risk-factors` | Risk Categories |
| 28 | GET | `/stocks/filings/10-K/vX/sections` | 10-K Sections |
| 29 | GET | `/stocks/filings/8-K/vX/text` | 8-K Text |
| 30 | GET | `/stocks/filings/vX/index` | SEC EDGAR Index |
| 31 | GET | `/v1/indicators/sma/{stockTicker}` | SMA |
| 32 | GET | `/v1/indicators/ema/{stockTicker}` | EMA |
| 33 | GET | `/v1/indicators/rsi/{stockTicker}` | RSI |
| 34 | GET | `/v1/indicators/macd/{stockTicker}` | MACD |
| 35 | GET | `/v1/related-companies/{ticker}` | Related Tickers |

### Options (10 unique REST endpoints)

| # | Method | Path | Name |
|---|---|---|---|
| 36 | GET | `/v3/snapshot/options/{underlyingAsset}` | Option Chain Snapshot |
| 37 | GET | `/v3/snapshot/options/{underlyingAsset}/{optionContract}` | Single Contract Snapshot |
| 38 | GET | `/v3/trades/{optionsTicker}` | Options Trades |
| 39 | GET | `/v3/quotes/{optionsTicker}` | Options Quotes |
| 40 | GET | `/v2/aggs/ticker/{optionsTicker}/range/...` | Options Bars |
| 41 | GET | `/v2/aggs/ticker/{optionsTicker}/prev` | Options Prev Bar |
| 42 | GET | `/v1/open-close/{optionsTicker}/{date}` | Options Daily Summary |
| 43 | GET | `/v2/last/trade/{optionsTicker}` | Options Last Trade |
| 44 | GET | `/v3/reference/options/contracts` | All Contracts |
| 45 | GET | `/v3/reference/options/contracts/{options_ticker}` | Contract Overview |

### Partners / Vendor (11 REST endpoints)

| # | Method | Path | Name | Anish Sub? |
|---|---|---|---|---|
| 46 | GET | `/benzinga/v2/news` | Benzinga News | YES |
| 47 | GET | `/benzinga/v1/earnings` | Benzinga Earnings | YES |
| 48 | GET | `/benzinga/v1/ratings` | Analyst Ratings | NO (403) |
| 49 | GET | `/benzinga/v1/consensus-ratings/{ticker}` | Consensus Ratings | NO (403) |
| 50 | GET | `/benzinga/v1/analyst-insights` | Analyst Insights | NO (403) |
| 51 | GET | `/benzinga/v1/guidance` | Corporate Guidance | NO (403) |
| 52 | GET | `/benzinga/v1/analysts` | Analyst Details | TBD |
| 53 | GET | `/benzinga/v1/firms` | Firm Details | TBD |
| 54 | GET | `/benzinga/v1/bulls-bears-say` | Bulls Bears Say | TBD |
| 55 | GET | `/etf-global/v1/constituents` | ETF Constituents | YES |
| 56 | GET | `/etf-global/v1/fund-flows` | ETF Fund Flows | YES |

### ETF Global (gated — not subscribed)

| # | Method | Path | Name | Anish Sub? |
|---|---|---|---|---|
| 57 | GET | `/etf-global/v1/taxonomies` | ETF Taxonomies | NO (403) |
| 58 | GET | `/etf-global/v1/profiles` | ETF Profiles | NO (403) |
| 59 | GET | `/etf-global/v1/analytics` | ETF Analytics | NO (403) |

### TMX (gated — not subscribed)

| # | Method | Path | Name | Anish Sub? |
|---|---|---|---|---|
| 60 | GET | `/tmx/v1/corporate-events` | Corporate Events | NO (403) |

### Futures (9 REST endpoints)

| # | Method | Path | Name |
|---|---|---|---|
| 61 | GET | `/futures/v1/aggs/{ticker}` | Futures Bars |
| 62 | GET | `/futures/v1/snapshot` | Futures Snapshot |
| 63 | GET | `/futures/v1/trades/{ticker}` | Futures Trades |
| 64 | GET | `/futures/v1/quotes/{ticker}` | Futures Quotes |
| 65 | GET | `/futures/v1/contracts` | Futures Contracts |
| 66 | GET | `/futures/v1/products` | Futures Products |
| 67 | GET | `/futures/v1/exchanges` | Futures Exchanges |
| 68 | GET | `/futures/v1/market-status` | Futures Market Status |
| 69 | GET | `/futures/v1/schedules` | Futures Schedules |

### Forex (10 REST endpoints)

| # | Method | Path | Name |
|---|---|---|---|
| 70 | GET | `/v2/aggs/ticker/{forexTicker}/range/...` | Forex Bars |
| 71 | GET | `/v2/aggs/ticker/{forexTicker}/prev` | Forex Prev Bar |
| 72 | GET | `/v2/aggs/grouped/locale/global/market/fx/{date}` | Forex Daily Summary |
| 73 | GET | `/v1/last_quote/currencies/{from}/{to}` | Forex Last Quote |
| 74 | GET | `/v3/quotes/{fxTicker}` | Forex Quotes |
| 75 | GET | `/v2/snapshot/locale/global/markets/forex/tickers/{ticker}` | Forex Single Snapshot |
| 76 | GET | `/v2/snapshot/locale/global/markets/forex/tickers` | Forex Full Snapshot |
| 77 | GET | `/v2/snapshot/locale/global/markets/forex/{direction}` | Forex Top Movers |
| 78 | GET | `/v1/conversion/{from}/{to}` | Currency Conversion |
| 79-82 | GET | `/v1/indicators/{sma,ema,rsi,macd}/{fxTicker}` | Forex Technicals |

### Crypto (10 REST endpoints)

| # | Method | Path | Name |
|---|---|---|---|
| 83 | GET | `/v2/aggs/ticker/{cryptoTicker}/range/...` | Crypto Bars |
| 84 | GET | `/v2/aggs/ticker/{cryptoTicker}/prev` | Crypto Prev Bar |
| 85 | GET | `/v2/aggs/grouped/locale/global/market/crypto/{date}` | Crypto Daily Summary |
| 86 | GET | `/v3/trades/{cryptoTicker}` | Crypto Trades |
| 87 | GET | `/v1/last/crypto/{from}/{to}` | Crypto Last Trade |
| 88 | GET | `/v1/open-close/crypto/{from}/{to}/{date}` | Crypto Daily Summary |
| 89 | GET | `/v2/snapshot/locale/global/markets/crypto/tickers/{ticker}` | Crypto Single Snapshot |
| 90 | GET | `/v2/snapshot/locale/global/markets/crypto/tickers` | Crypto Full Snapshot |
| 91 | GET | `/v2/snapshot/locale/global/markets/crypto/{direction}` | Crypto Top Movers |
| 92-95 | GET | `/v1/indicators/{sma,ema,rsi,macd}/{cryptoTicker}` | Crypto Technicals |

### Indices (6 REST endpoints + 4 indicators)

| # | Method | Path | Name |
|---|---|---|---|
| 96 | GET | `/v2/aggs/ticker/{indicesTicker}/range/...` | Indices Bars |
| 97 | GET | `/v2/aggs/ticker/{indicesTicker}/prev` | Indices Prev Bar |
| 98 | GET | `/v1/open-close/{indicesTicker}/{date}` | Indices Daily Summary |
| 99 | GET | `/v3/snapshot/indices` | Indices Snapshot |
| 100-103 | GET | `/v1/indicators/{sma,ema,rsi,macd}/{indicesTicker}` | Indices Technicals |

### Economy (4 REST endpoints)

| # | Method | Path | Name |
|---|---|---|---|
| 104 | GET | `/fed/v1/treasury-yields` | Treasury Yields |
| 105 | GET | `/fed/v1/inflation` | Inflation |
| 106 | GET | `/fed/v1/inflation-expectations` | Inflation Expectations |
| 107 | GET | `/fed/v1/labor-market` | Labor Market |

### Alternative Data (2 REST endpoints)

| # | Method | Path | Name |
|---|---|---|---|
| 108 | GET | `/consumer-spending/eu/v1/merchant-aggregates` | EU Consumer Spending |
| 109 | GET | `/consumer-spending/eu/v1/merchant-hierarchy` | Merchant Hierarchy |

### Reference (8 REST endpoints)

| # | Method | Path | Name |
|---|---|---|---|
| 110 | GET | `/v3/reference/tickers` | All Tickers |
| 111 | GET | `/v3/reference/tickers/{ticker}` | Ticker Overview |
| 112 | GET | `/vX/reference/tickers/{id}/events` | Ticker Events |
| 113 | GET | `/v3/reference/tickers/types` | Ticker Types |
| 114 | GET | `/v3/reference/exchanges` | Exchanges |
| 115 | GET | `/v3/reference/conditions` | Condition Codes |
| 116 | GET | `/v1/marketstatus/now` | Market Status |
| 117 | GET | `/v1/marketstatus/upcoming` | Market Holidays |
| 118 | GET | `/v2/reference/news` | News (with sentiment) |

---

## GRAND TOTAL

| Category | REST Endpoints | WebSocket Channels | S3 Prefixes | MCP Functions |
|---|---|---|---|---|
| Stocks | 35 | 9 | 4 | — |
| Options | 10 | 5 | 4 | — |
| Partners (Benzinga/ETF/TMX) | 14 | — | — | — |
| Futures | 9 | 4 | 4 (403) | — |
| Forex | 10 | 4 | 1 (403) | — |
| Crypto | 10 | 6 | 1 (403) | — |
| Indices | 6 | 3 | 1 (403) | — |
| Economy | 4 | — | — | — |
| Alternative | 2 | — | — | — |
| Reference | 9 | — | — | — |
| MCP Functions | — | — | — | 13 |
| **TOTAL** | **109** | **31** | **15** | **13** |

**Anish has active access to:** 109 REST endpoints (minus ~8 gated partner endpoints = ~101 working), 31 WebSocket channels (minus LULD = 30 working), 8 S3 prefixes (stocks + options), and 13 MCP apply functions.

---

## CRITICAL GOTCHAS (from KNOWN_ENDPOINTS.md)

1. **Decimal-size schema break 2026-02-23.** `size`/`volume` are decimals now (string fields for precision).
2. **Old `/v3/reference/{splits,dividends}` deprecated.** Use `/stocks/v1/{splits,dividends}`.
3. **NOI is WebSocket-only.** No REST/S3 historical. Every minute offline = unrecoverable.
4. **Per-second aggs (AS.*) are WebSocket-only.** Same forward-only constraint.
5. **LULD is NOT subscribed.** `LULD.*` subscribe will silently fail.
6. **Go SDK timestamps:** `LaunchpadValue` and `FairMarketValue` use NANOSECONDS; everything else uses milliseconds.
7. **`api.polygon.io` still works** post-Oct 2025 rebrand. Both `api.polygon.io` and `api.massive.com` resolve.

---

*End of reconnaissance. This file is the COMPLETE inventory of every discoverable Massive API endpoint as of 2026-05-26.*
