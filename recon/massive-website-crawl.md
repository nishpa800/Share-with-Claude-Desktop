# Massive.com (formerly Polygon.io) -- Exhaustive Website Crawl

**Crawl Date:** 2026-05-26
**Crawl Agent:** Claude Opus 4.7 (1M context)
**Purpose:** Phase 0 reconnaissance for quantitative trading research system

---

## TABLE OF CONTENTS

1. [Company Overview & Rebrand](#1-company-overview--rebrand)
2. [Subscription Tiers & Pricing](#2-subscription-tiers--pricing)
3. [REST API Documentation](#3-rest-api-documentation)
4. [WebSocket API Documentation](#4-websocket-api-documentation)
5. [Flat Files / S3 Documentation](#5-flat-files--s3-documentation)
6. [SQL Interface](#6-sql-interface)
7. [Client Libraries / SDKs](#7-client-libraries--sdks)
8. [MCP Server (AI Integration)](#8-mcp-server-ai-integration)
9. [Partner Data Products](#9-partner-data-products)
10. [Data Infrastructure & Architecture](#10-data-infrastructure--architecture)
11. [Knowledge Base Articles](#11-knowledge-base-articles)
12. [Blog Posts & Tutorials](#12-blog-posts--tutorials)
13. [Changelog & Release Notes](#13-changelog--release-notes)
14. [API Status & Incidents](#14-api-status--incidents)
15. [Community Examples & Sample Apps](#15-community-examples--sample-apps)
16. [Relevance to Our System](#16-relevance-to-our-system)

---

## 1. COMPANY OVERVIEW & REBRAND

### Source URLs
- https://massive.com/blog/polygon-is-now-massive
- https://massive.com/about
- https://www.crunchbase.com/organization/polygon-io

### Key Facts

- **Founded:** January 2016 (incorporated January 2017) by Quinton Pike in Atlanta, GA
- **CEO/Founder:** Quinton Pike (previously at Google and CNN, background in web design/interactive media)
- **Rebrand Date:** October 30, 2025, 4 PM ET -- Polygon.io officially became Massive.com
- **Rebrand Rationale:** Reflects focus on scale, reliability, and comprehensive market data coverage
- **Funding:** $6.4M total raised. Series A: $6M on October 14, 2020, led by e.ventures (now Headline) with participation from Green Visor Capital
- **Headquarters:** Atlanta, GA (data centers in NJ and Chicago)
- **Employee count:** ~50-100 (estimated from Crunchbase/LinkedIn data)

### Migration Details
- **API base URL changed:** api.polygon.io -> api.massive.com (polygon.io remains supported for extended period)
- **WebSocket URL changed:** socket.polygon.io -> socket.massive.com
- **S3 endpoint:** https://files.polygon.io (still active) / https://files.massive.com
- **SDK package names changed:** polygon -> massive (Python), @polygon.io/client-js -> @massive.com/client-js
- **No breaking changes to API functionality** -- keys, accounts, integrations all continue working
- **GitHub orgs:** polygon-io/* repos redirected/mirrored to massive-com/*

---

## 2. SUBSCRIPTION TIERS & PRICING

### Source URLs
- https://massive.com/pricing
- https://massive.com/knowledge-base/article/what-are-the-different-polygon-subscriptions-i-can-use

### Products (Asset Classes)

Four independent product lines, each with its own tiers:

1. **Stocks** (US Equities)
2. **Options** (US OPRA)
3. **Indices** (US Indices)
4. **Currencies** (Forex + Crypto combined)
5. **Futures** (CME Group -- CBOT, CME, COMEX, NYMEX) -- available as separate product

### Tier Structure (per product)

| Tier | Recency | Rate Limit | Flat Files | Price Range |
|------|---------|------------|------------|-------------|
| **Basic** | 15-min delayed | 5 req/min | Yes (2yr history) | Free |
| **Starter** | 15-min delayed | Unlimited | Yes (full history) | ~$29/mo |
| **Developer** | 15-min delayed | Unlimited | Yes (full history) | ~$79/mo |
| **Advanced** | Real-time | Unlimited | Yes (full history) | ~$199/mo |
| **Business** | Real-time | Unlimited | Yes (full history) | Custom |

### Known Pricing (from KNOWN_SUBSCRIPTIONS.md + web sources)

| Product | Price | Notes |
|---------|-------|-------|
| Stocks Advanced | $199/mo | Real-time equities, full SIP tape |
| Options Advanced | $199/mo | Real-time OPRA, all 17 exchanges |
| Currencies Basic | Free | Forex aggregates + reference data |
| Futures Basic | Free | CME/CBOT/COMEX/NYMEX aggregates |
| Indices Basic | Free | Index values (SPX, NDX, RUT, VIX, etc.) |

### Expansion Packs (Add-ons, priced per-seat)

| Add-on | Price | What It Unlocks |
|--------|-------|-----------------|
| **Order Imbalances** | $49/mo | NYSE/Nasdaq NOI -- WebSocket only |
| **Benzinga News** | $99/mo | Real-time news headlines + body + tickers |
| **Benzinga Earnings** | $99/mo | Earnings calendar + actuals + estimates |
| **Benzinga Analyst Ratings** | $99/mo | Upgrades, downgrades, price targets |
| **Benzinga Analyst Insights** | $99/mo | Commentary behind analyst ratings |
| **Benzinga Guidance** | $99/mo | Company guidance on future earnings/revenue |
| **ETF Global Fund Flows** | $99/mo | Daily ETF inflow/outflow |
| **ETF Global Constituents** | $99/mo | ETF holdings + weights |
| **ETF Global Analytics** | Unknown | Advanced ETF analytics |
| **ETF Global Profiles** | Unknown | ETF profile/metadata |
| **ETF Global Taxonomies** | Unknown | ETF classification system |
| **TMX Corporate Events** | Unknown | Wall Street Horizon calendar (earnings, dividends, conferences) |

### Rate Limits
- **Free tier:** 5 API requests per minute
- **All paid tiers:** Unlimited API requests
- **WebSocket:** 1 concurrent connection per asset class by default (i.e., 4-6 total: stocks, options, forex, crypto, indices, futures)
- **Options WebSocket:** 1,000 simultaneous contract subscriptions per connection

### Anish's Active Subscriptions (per KNOWN_SUBSCRIPTIONS.md, verified 2026-05-18)
Total: ~$891/month. Stocks Advanced ($199), Options Advanced ($199), Order Imbalances ($49), Benzinga News ($99), Benzinga Earnings ($99), ETF Global Fund Flows ($99), ETF Global Constituents ($99), Currencies Basic (free), Futures Basic (free), Indices Basic (free).

---

## 3. REST API DOCUMENTATION

### Source URLs
- https://massive.com/docs (main docs hub)
- https://massive.com/docs/llms.txt (AI-agent index)
- https://massive.com/docs/llms-full.txt (comprehensive AI docs)
- https://massive.com/docs/rest/quickstart
- https://massive.com/docs/rest/stocks/overview
- https://massive.com/docs/rest/options/overview

### Authentication
- **Method:** Bearer token in Authorization header
- **Header:** `Authorization: Bearer YOUR_API_KEY`
- **Environment variable:** `MASSIVE_API_KEY`

### Base URL
- **Primary:** `https://api.massive.com`
- **Legacy (still works):** `https://api.polygon.io`

### Pagination
- **Cursor-based:** Responses include `next_url` for next page
- **`limit` parameter:** Controls page size, NOT total results (default varies by endpoint, max typically 50,000)
- **`pagination=True`** (default in SDKs): Automatically fetches all pages
- **Query filter extensions:** `.gt`, `.gte`, `.lt`, `.lte`, `.any_of` for powerful filtering
- **Sort:** Comma-separated columns with `.asc`/`.desc` suffixes

### Stocks REST Endpoints

#### Market Data
| Endpoint | Path Pattern | Description |
|----------|-------------|-------------|
| Aggregates (Custom Bars) | `GET /v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from}/{to}` | OHLCV bars at custom intervals |
| Daily Summary | `GET /v2/aggs/ticker/{ticker}/prev` | Previous day OHLCV |
| Grouped Daily | `GET /v2/aggs/grouped/locale/us/market/stocks/{date}` | All tickers for a date |
| Trades | `GET /v3/trades/{ticker}` | Tick-level trade data with nanosecond timestamps |
| Last Trade | `GET /v2/last/trade/{ticker}` | Most recent trade |
| Quotes (NBBO) | `GET /v3/quotes/{ticker}` | Top-of-book quotes |
| Last Quote | `GET /v2/last/nbbo/{ticker}` | Most recent NBBO |
| Snapshot - All Tickers | `GET /v2/snapshot/locale/us/market/stocks/tickers` | Current minute/day/prev agg + last trade/quote for all |
| Snapshot - Single | `GET /v2/snapshot/locale/us/market/stocks/tickers/{ticker}` | Same for one ticker |
| Snapshot - Gainers/Losers | `GET /v2/snapshot/locale/us/market/stocks/{direction}` | Top movers |
| Unified Snapshot | `GET /v3/snapshot` | Multi-asset snapshot in single request |

#### Technical Indicators
| Endpoint | Path Pattern | Description |
|----------|-------------|-------------|
| SMA | `GET /v1/indicators/sma/{ticker}` | Simple Moving Average |
| EMA | `GET /v1/indicators/ema/{ticker}` | Exponential Moving Average |
| MACD | `GET /v1/indicators/macd/{ticker}` | Moving Average Convergence Divergence |
| RSI | `GET /v1/indicators/rsi/{ticker}` | Relative Strength Index |

#### Reference Data
| Endpoint | Path Pattern | Description |
|----------|-------------|-------------|
| All Tickers | `GET /v3/reference/tickers` | List all supported tickers |
| Ticker Details | `GET /v3/reference/tickers/{ticker}` | Company info, market cap, FIGI, CIK |
| Related Tickers | `GET /v1/related-companies/{ticker}` | Related/peer companies |
| Ticker Types | `GET /v3/reference/tickers/types` | CS, ETF, ADRC, etc. |
| Exchanges | `GET /v3/reference/exchanges` | All known exchanges with IDs |
| Conditions | `GET /v3/reference/conditions` | Trade and quote conditions from CTA/UTP/OPRA/FINRA |
| Market Holidays | `GET /v1/marketstatus/upcoming` | Upcoming holidays with open/close times |
| Market Status | `GET /v1/marketstatus/now` | Current market open/close state |

#### Fundamentals
| Endpoint | Path Pattern | Description |
|----------|-------------|-------------|
| Financials | `GET /vX/reference/financials` | Balance sheet, income stmt, cash flow from SEC filings |
| Financial Ratios | `GET /stocks/financials/v1/ratios` | 40+ ratios (P/E, P/B, ROE, etc.) using TTM + daily price |
| Short Interest | `GET /stocks/v1/short-interest` | Bi-weekly FINRA data, days-to-cover |
| Short Volume | `GET /stocks/v1/short-volume` | Daily short sale volume from ATS/off-exchange |
| Float | `GET /stocks/v1/float` | Free float shares available for trading |

#### Corporate Actions
| Endpoint | Path Pattern | Description |
|----------|-------------|-------------|
| Dividends | `GET /stocks/v1/dividends` | Historical cash dividends, ex-date, pay-date, split-adjusted |
| Splits | `GET /stocks/v1/splits` | Stock splits with ratio and adjustment factor (history from 1978) |
| Ticker Events | `GET /vX/reference/tickers/{ticker}/events` | IPOs, name changes, delistings |

#### SEC Filings (Beta -- free during early access)
| Endpoint | Path Pattern | Description |
|----------|-------------|-------------|
| SEC EDGAR Index | `GET /stocks/filings/vX/index` | Master index of all EDGAR filings (10-K, 10-Q, 8-K, 13-F, Form 3/4, S-1) |
| 10-K Sections | `GET /stocks/filings/vX/10k/sections` | Raw text sections (business, risk factors) |
| 8-K Items | `GET /stocks/filings/vX/8k` | Parsed content at item level |
| 13-F Holdings | `GET /stocks/filings/vX/13f` | Institutional holdings |
| Form 3/4 | `GET /stocks/filings/vX/form3`, `form4` | Beneficial ownership / insider transactions |
| Risk Factors | `GET /stocks/filings/vX/risk-factors` | Extracted risk factors |

### Options REST Endpoints
| Endpoint | Description |
|----------|-------------|
| Options Contracts | Reference data for specific options contracts (type, exercise style, expiration, strike, shares per contract) |
| Options Chain Snapshot | All contracts for an underlying: last quote, last trade, OI, day bar, Greeks (delta/gamma/theta/vega), IV, break-even |
| Options Trades | Historical tick-level options trades |
| Options Quotes | Historical options quotes |
| Options Aggregates | OHLCV bars for options contracts |

### Indices REST Endpoints
- 11,400+ indices including S&P 500 (I:SPX), Nasdaq-100 (I:NDX), DJIA (I:DJI), VIX (I:VIX)
- Ticker format: `I:XXX`
- Values, aggregates, snapshots
- Historical data from early March 2023

### Forex REST Endpoints
- 1,100+ FX pairs
- Real-time quotes, OHLCV, indicators
- Historical quotes and OHLCV back to 2009

### Crypto REST Endpoints
- 166 cryptocurrency tickers from 4 exchanges (Coinbase, Kraken, etc.)
- Trades, quotes, aggregates, snapshots

### Futures REST Endpoints
- CME Group exchanges: CME, CBOT, COMEX, NYMEX
- Tick-by-tick trades, Level 1 quotes, contract details, product specs, trading schedules
- 10+ years historical data
- Data sourced from direct CME Globex feeds via Equinix co-location

### Economy REST Endpoints
| Endpoint | Description |
|----------|-------------|
| Treasury Yields | US Treasury yield curve data |

---

## 4. WEBSOCKET API DOCUMENTATION

### Source URLs
- https://massive.com/docs/websocket/quickstart
- https://massive.com/docs/websocket/stocks/overview
- https://massive.com/docs/websocket/stocks/trades
- https://massive.com/docs/websocket/stocks/imbalances
- https://massive.com/docs/websocket/stocks/luld
- https://massive.com/docs/websocket/stocks/fair-market-value
- https://massive.com/docs/websocket/options/overview
- https://massive.com/docs/websocket/forex/overview
- https://massive.com/docs/websocket/crypto/overview

### Connection Details
- **Base URL:** `wss://socket.massive.com` (legacy: `wss://socket.polygon.io`)
- **Authentication:** After connecting, send auth message with API key before subscribing
- **Connections:** 1 concurrent connection per asset class (stocks, options, forex, crypto, indices, futures)
- **Reconnection:** SDKs handle automatic reconnection with subscription resubscription

### Subscription Syntax
- **Single ticker:** `T.AAPL`
- **Multiple tickers:** `T.AAPL,T.MSFT,T.GOOGL`
- **All tickers (wildcard):** `T.*`

### Stocks WebSocket Channels

| Channel Prefix | Event Type | Description | Access Tier |
|---------------|------------|-------------|-------------|
| `T` | Trades | Every executed trade: price, size, exchange, conditions, SIP/participant timestamps | Starter+ |
| `Q` | Quotes (NBBO) | Bid/ask prices and sizes as they update | Starter+ |
| `A` | Aggregates (Per Minute) | Minute OHLCV bars from qualifying trades | Starter+ |
| `AM` | Aggregates (Per Second) | Second-level OHLCV bars | Advanced+ |
| `LULD` | Limit Up/Limit Down | Price band breach events, halts, resumptions | Advanced+ |
| `NOI` | Net Order Imbalance | NYSE/Nasdaq auction imbalances (open/close/intraday) | Imbalances add-on |
| `FMV` | Fair Market Value | Algorithmically derived real-time fair price estimate | Business only |

#### Trades Channel (`T`) -- Full Field Spec
| Field | Type | Description |
|-------|------|-------------|
| `ev` | enum | Event type: "T" |
| `sym` | string | Ticker symbol |
| `x` | integer | Exchange ID |
| `i` | string | Trade ID |
| `z` | integer | Tape: 1=NYSE, 2=AMEX, 3=Nasdaq |
| `p` | number | Trade price |
| `s` | integer | Trade size (whole shares) |
| `ds` | string | Trade size including fractional shares |
| `c` | array[int] | Trade conditions |
| `t` | integer | SIP timestamp (Unix ms) |
| `pt` | integer | Participant/exchange timestamp (Unix ms) |
| `q` | integer | Sequence number (increasing, non-sequential) |
| `trfi` | integer | Trade Reporting Facility ID |
| `trft` | integer | TRF timestamp (Unix ms) |

**Dark pool identification:** If `x` = 4 (exchange ID 4) AND `trfi` is present, the trade came from a dark pool.

#### NOI Channel -- Full Field Spec
| Field | Type | Description |
|-------|------|-------------|
| `ev` | enum | "NOI" |
| `T` | string | Ticker symbol |
| `t` | integer | Timestamp (Unix nanoseconds) |
| `at` | integer | Auction time in EST (HHMM, e.g., 930 = 9:30 AM) |
| `a` | string | Auction type code: O=Open, M=Market Close, H=Halt, C=Close, P=Price Variation, R=Regulatory Imbalance |
| `i` | integer | Symbol sequence number |
| `x` | integer | Exchange ID |
| `o` | integer | Imbalance quantity |
| `p` | integer | Paired quantity |
| `b` | number | Book clearing price |

**Timing:** Primarily at market open (9:30 AM ET) and close (4:00 PM ET), plus during halts and mini-auctions. Some auction types are NYSE-specific.

**Access:** Requires Imbalances expansion pack ($49/mo) with real-time recency.

#### LULD Channel -- Full Field Spec
| Field | Type | Description |
|-------|------|-------------|
| `ev` | enum | "LULD" |
| `T` | string | Ticker symbol |
| `h` | number | High price limit |
| `l` | number | Low price limit |
| `i` | array[int] | Indicator codes (halts/resumptions -- Nasdaq only for codes 17/18) |
| `z` | integer | Tape: 1=NYSE, 2=AMEX, 3=Nasdaq |
| `t` | integer | Unix millisecond timestamp |
| `q` | integer | Sequence number |

**Supported exchanges:** NYSE, Nasdaq, Cboe BZX, NYSE Arca, NYSE American.

#### FMV Channel -- Full Field Spec (Business plan only)
| Field | Type | Description |
|-------|------|-------------|
| `ev` | enum | "FMV" |
| `fmv` | number | Fair market valuation metric |
| `sym` | string | Ticker symbol |
| `t` | integer | Nanosecond timestamp |

**Coverage:** Pre-market, regular, and after-hours sessions. Available for stocks, options, crypto, forex.

### Options WebSocket Channels
| Channel | Description | Limit |
|---------|-------------|-------|
| Trades | Options trade executions | 1,000 contracts per connection |
| Quotes | Options bid/ask | 1,000 contracts per connection |
| Aggregates (Per Minute) | Minute OHLCV for options | 1,000 contracts per connection |
| Aggregates (Per Second) | Second OHLCV | 1,000 contracts per connection |
| FMV | Fair market value for options | Business only |

### Forex WebSocket Channels
- Quotes
- Aggregates (Per Minute)
- Aggregates (Per Second)
- Fair Market Value (Business only)

### Crypto WebSocket Channels
- Trades
- Quotes
- Aggregates (Per Minute)
- Aggregates (Per Second)
- Fair Market Value (Business only)

### Indices WebSocket Channels
- Values
- Aggregates

### Futures WebSocket Channels
- Trades
- Quotes

---

## 5. FLAT FILES / S3 DOCUMENTATION

### Source URLs
- https://massive.com/docs/flat-files/quickstart
- https://massive.com/docs/flat-files/stocks/overview
- https://massive.com/knowledge-base/article/how-to-get-started-with-s3
- https://massive.com/blog/flat-files

### S3 Access Configuration

| Setting | Value |
|---------|-------|
| **Endpoint** | `https://files.polygon.io` (also `https://files.massive.com`) |
| **Bucket** | `flatfiles` |
| **Authentication** | Access Key ID + Secret Access Key (from Massive Dashboard) |
| **Protocol** | S3-compatible (not AWS S3 directly) |

### Supported S3 Clients

1. **AWS CLI:** `aws s3 ls --endpoint-url https://files.polygon.io s3://flatfiles/`
2. **Rclone:** `rclone config create s3polygon s3 env_auth=false access_key_id=KEY secret_access_key=SECRET endpoint=https://files.polygon.io`
3. **MinIO:** MinIO client configuration with endpoint/bucket
4. **Boto3 (Python):** `session.client('s3', endpoint_url='https://files.polygon.io')` with bucket='flatfiles'

### Available Flat File Datasets

| Asset Class | S3 Prefix | Datasets |
|------------|-----------|----------|
| **US Stocks (SIP)** | `us_stocks_sip/` | trades, quotes, minute_aggs, day_aggs |
| **US Options (OPRA)** | `us_options_opra/` | trades, quotes, minute_aggs, day_aggs |
| **US Indices** | `us_indices/` | values_v1, minute_aggs, day_aggs |
| **US Futures (CME)** | `us_futures_cme/` | trades, quotes, minute_aggs, session_aggs |
| **US Futures (CBOT)** | `us_futures_cbot/` | trades, quotes, minute_aggs, session_aggs |
| **US Futures (COMEX)** | `us_futures_comex/` | trades, quotes, minute_aggs, session_aggs |
| **US Futures (NYMEX)** | `us_futures_nymex/` | trades, quotes, minute_aggs, session_aggs |
| **Global Forex** | `global_forex/` | quotes, minute_aggs, day_aggs |
| **Global Crypto** | `global_crypto/` | trades, quotes, minute_aggs, day_aggs |

### File Format
- **Format:** Compressed CSV (gzip)
- **Header row:** First row identifies columns
- **Partitioning:** By date (one file per dataset per day per ticker or per day for full market)
- **Minute aggregate columns (example):** ticker, volume, open, close, high, low, window_start, transactions

### Data Sources for Stocks
- All 19 major U.S. stock exchanges (NYSE, Nasdaq, CBOE, etc.)
- FINRA Trade Reporting Facilities (NYSE TRF, Nasdaq TRF)
- Dark pools

### Historical Depth
- **Basic tier:** 2 years
- **Starter+ tiers:** Full history (stocks: 20+ years, varies by dataset)
- **Included in all paid plans** at no additional charge (announced March 6, 2024)

---

## 6. SQL INTERFACE

### Source URL
- https://massive.com/sql

### Status
- **Available** (not beta, fully launched)
- Query over 2 PB of market data instantly with SQL
- Access through Massive.com platform

### Capabilities
- SQL query interface for historical and real-time market data
- Covers stocks, options, indices, forex, crypto, futures
- Part of Massive's multi-access delivery model (REST + WebSocket + S3 + SQL)

### Note on MCP Server SQL
The MCP server (mcp_massive) provides a **separate** in-memory SQLite query capability:
- `store_as` parameter on `call_api` saves results to in-memory SQLite table
- `query_data` tool runs SQL against stored tables
- Supports: `SHOW TABLES`, `DESCRIBE`, `DROP TABLE`, CTEs, window functions
- This is CLIENT-SIDE in the MCP process, NOT the same as Massive's hosted SQL interface

---

## 7. CLIENT LIBRARIES / SDKS

### Source URLs
- https://github.com/massive-com/client-python
- https://github.com/massive-com/client-go
- https://github.com/massive-com/client-js (also polygon-io/client-js)
- https://github.com/massive-com/client-jvm (also polygon-io/client-jvm)
- https://deepwiki.com/massive-com/client-python

### Python SDK (client-python)

| Property | Value |
|----------|-------|
| **PyPI package** | `massive` (formerly `polygon-api-client`) |
| **Python version** | 3.9+ required |
| **Latest release** | v2.8.0 (May 26, 2026) |
| **GitHub stars** | ~1,400 |
| **License** | MIT |

**Architecture:**
- `RESTClient` -- Synchronous HTTP access to all REST endpoints
- `WebSocketClient` -- Asynchronous real-time streaming
- Dependencies: `urllib3` (HTTP with connection pooling, retry on 413/429/499/500-504), `websockets` (async WS), `certifi` (SSL)

**Key REST methods:**
- `list_aggs()` -- Aggregate bars with multiplier/timespan
- `get_last_trade()` / `list_trades()` -- Trade data
- `get_last_quote()` / `list_quotes()` -- Quote data
- `list_snapshot_options_chain()` -- Options chain snapshot
- `list_stocks_filings_index()` -- SEC EDGAR index (beta)
- `list_stocks_filings_10k_sections()` -- 10-K raw text (beta)
- Pattern: `list_*()` returns paginating iterator, `get_*()` returns single object

**Pagination:** Automatic by default (`pagination=True`). `limit` controls page size, client fetches all pages via `next_url`.

**Filter operators:** `_gt`, `_gte`, `_lt`, `_lte` in parameter names are rewritten to `.gt`, `.gte`, `.lt`, `.lte` by the SDK.

**WebSocket usage:**
```python
from massive import WebSocketClient
ws = WebSocketClient(api_key="KEY", subscriptions=["T.AAPL"])
ws.run(handle_msg=lambda msgs: [print(m) for m in msgs])
```

**Debug mode:** `RESTClient(trace=True, verbose=True)`

**Versioning:** Endpoint prefixes `/v1/` (legacy), `/v2/` (core stable), `/v3/` (enhanced), `/vX/` (experimental, may change).

### Go SDK (client-go)

| Property | Value |
|----------|-------|
| **Module** | `github.com/massive-com/client-go/v3` |
| **Go version** | 1.18+ (uses generics) |
| **Latest release** | v3.3.0 (April 2026) |
| **License** | MIT |

**Architecture:**
- REST: `rest.NewWithOptions()` with OpenAPI-generated `*WithResponse` methods
- WebSocket: `massivews.New()` with gorilla/websocket + cenkalti/backoff + tomb.v2
  - Three goroutines: read, write, process
  - 100k-buffer `Output()` channel
  - Automatic reconnection with subscription resubscription

**REST example:**
```go
c := rest.NewWithOptions("API_KEY", rest.WithPagination(true))
resp, _ := c.GetStocksAggregatesWithResponse(ctx, "AAPL", 1, "day", "2026-02-16", "2026-02-20", params)
```

**WebSocket example:**
```go
c, _ := massivews.New(massivews.Config{APIKey: "KEY", Feed: massivews.RealTime, Market: massivews.Stocks})
c.Connect()
c.Subscribe(massivews.StocksTrades, "TSLA", "GME")
for out := range c.Output() { /* process */ }
```

**100+ example code snippets** in the repository.

### JavaScript/TypeScript SDK (client-js)

| Property | Value |
|----------|-------|
| **npm package** | `@massive.com/client-js` (formerly `@polygon.io/client-js`) |
| **Breaking change (v8.0):** | All methods now take a single `requestParameters` object (June 2025) |
| **Generated from:** | OpenAPI spec (auto-syncs with API) |

**Key stats:**
- 145 REST methods (auto-generated from OpenAPI)
- 487 interfaces
- 252 enums

**Breaking changes in v8:**
- Default base URL: api.polygon.io -> api.massive.com
- Default WS URL: socket.polygon.io -> socket.massive.com
- Package/import: polygon -> massive
- Core functionality unchanged

### JVM SDK (Kotlin/Java) (client-jvm)

| Property | Value |
|----------|-------|
| **Language** | Kotlin (usable from any JVM language, Android SDK 21+) |
| **REST** | OpenAPI-generated god-class (~18,261 LOC, ~100 methods, OkHttp+Moshi) |
| **WebSocket** | Hand-written with ktor + kotlinx.serialization + coroutines |
| **API flavors** | 3: suspend / blocking / async (for Java interop) |
| **WS topics** | 36 across 18 feed hosts x 10 markets |
| **Model classes** | 361 (most complete schema reference of any SDK) |

### SDK Comparison Summary

| Feature | Python | Go | JS/TS | JVM |
|---------|--------|-----|-------|-----|
| REST methods | ~76 | ~145 (generated) | 145 (generated) | ~100 (generated) |
| WS methods | 7 | 36 topics | Full | 36 topics x 3 flavors |
| Auto-pagination | Yes | Yes | Yes | Yes |
| Auto-reconnect WS | Yes | Yes | Yes | Yes |
| OpenAPI generated | Partial | Yes | Yes | Yes (REST) |
| Model classes | ~25+ | 19 structs | 487 interfaces | 361 classes |

---

## 8. MCP SERVER (AI INTEGRATION)

### Source URLs
- https://github.com/massive-com/mcp_massive
- https://massive.com/blog/querying-financial-markets-with-the-polgon-io-mcp-server-claude-4-and-pydantic-ai
- https://massive.com/blog/creating-stock-market-reports-using-open-ais-gpt-5-and-agent-sdk-with-the-polygon-io-mcp-server-in-under-200-lines-of-code

### Overview
An MCP (Model Context Protocol) server providing LLM-friendly access to the entire Massive.com API surface. Rather than one tool per endpoint, it provides 3 composable tools that cover everything.

### Requirements
- Python 3.12+
- Massive.com API key
- Astral UV v0.4.0+

### Installation (Claude Code)
```bash
uv tool install "mcp_massive @ git+https://github.com/massive-com/mcp_massive@v0.10.0"
claude mcp add massive -e MASSIVE_API_KEY=your_key -- mcp_massive
```

### Three Core Tools

#### 1. `search_endpoints`
- Discovers API endpoints via natural language queries
- Uses BM25 routing (not embeddings)
- Dynamically indexes all endpoints at startup from llms.txt
- Parameters: `detail` ("more" for params, "verbose" for full docs), `max_results`, `scope` ("functions" for built-in functions)

#### 2. `call_api`
- Invokes any Massive.com REST API endpoint
- `store_as` parameter saves results as in-memory SQLite table
- `apply` parameter for post-processing with built-in functions
- Handles paginated responses with next-page hints

#### 3. `query_data`
- Executes SQL against stored SQLite database
- Supports: SHOW TABLES, DESCRIBE, DROP TABLE, CTEs, window functions
- `apply` parameter for post-processing

### Built-in Functions (14 total, computed CLIENT-SIDE via numpy)

**Black-Scholes Greeks (6):**
- `bs_price`, `bs_delta`, `bs_gamma`, `bs_theta`, `bs_vega`, `bs_rho`

**Returns Calculations (5):**
- `simple_return`, `log_return`, `cumulative_return`, `sharpe_ratio`, `sortino_ratio`

**Technical Analysis (2):**
- `sma` (simple moving average), `ema` (exponential moving average)

**Note:** These are calculated in the MCP process locally, NOT on Massive's servers.

### Configuration Environment Variables

| Variable | Required | Default |
|----------|----------|---------|
| MASSIVE_API_KEY | Yes | -- |
| MCP_TRANSPORT | No | stdio |
| MASSIVE_API_BASE_URL | No | https://api.massive.com |
| MASSIVE_MAX_TABLES | No | 50 |
| MASSIVE_MAX_ROWS | No | 50,000 |

### AI Agent Documentation
- **llms.txt:** Standard AI-agent index of all endpoints (~22KB)
- **llms-full.txt:** Comprehensive docs with full field specs
- **Convention files:** Same content replicated across CLAUDE.md, AGENTS.md, GEMINI.md, .windsurfrules, .github/copilot-instructions.md
- **Cursor:** Uses 5 scoped .mdc rules (different approach)

---

## 9. PARTNER DATA PRODUCTS

### Source URLs
- https://massive.com/partners/benzinga
- https://massive.com/partners/etf-global
- https://massive.com/partners/business-tmx
- https://massive.com/alternative/consumer-spending

### Benzinga (News + Earnings + Ratings)

**Partnership announced:** June 2025

**Available data products:**
1. **Benzinga News** ($99/mo) -- Market-moving headlines with full articles, structured by tickers
2. **Benzinga Earnings** ($99/mo) -- Earnings calendar, estimates, actuals, surprises
3. **Benzinga Analyst Ratings** ($99/mo) -- Upgrades, downgrades, price targets, aggregated ratings
4. **Benzinga Analyst Insights** ($99/mo) -- Commentary behind analyst ratings
5. **Benzinga Guidance** ($99/mo) -- Company guidance on future earnings/revenue

**Delivery:** REST API endpoints

### ETF Global (Fund Flows + Constituents + Analytics)

**Partnership announced:** February 2026

**Available data products:**
1. **ETF Global Fund Flows** ($99/mo)
   - Endpoint: `GET /etf-global/v1/fund-flows`
   - Tracks daily ETF capital movements (inflows/outflows)
   - Fields: composite_ticker, effective_date, processed_date, fund_flow, nav, shares_outstanding
   - Updated daily, history from April 3, 2017
   - Limit: max 5,000 per request

2. **ETF Global Constituents** ($99/mo)
   - Top holdings, position weights, concentration analysis
   
3. **ETF Global Analytics** (separate add-on)
4. **ETF Global Profiles** (separate add-on)
5. **ETF Global Taxonomies** (separate add-on)

### TMX Wall Street Horizon (Corporate Events)

**Partnership announced:** November 14, 2025 (Massive closed the market at TSX to celebrate)

**Endpoint:** `GET /tmx/v1/corporate-events`

**Event types (20+ categories):**
- Earnings announcement dates, earnings results
- Dividend dates, stock splits
- Investor conferences, analyst days
- Business updates, shareholder meetings
- And 14+ additional types

**Key features:**
- Status tracking: approved, confirmed, canceled, pending, postponed, unconfirmed, historical
- Updated every 2 hours
- Historical data from January 1, 2018
- Filtering by ticker, ISIN, form type, date range, status

### Fable Data (European Consumer Spending)

**Product:** Alternative data -- daily consumer spending totals by merchant
- 250+ US public companies tracked across 6 European countries
- Transaction data since 2016
- Endpoint: `GET /alternative/v1/consumer-spending/eu`
- Powered by Fable Data (UK-based, IMF-endorsed data quality)

### Nasdaq Basic (Business add-on)
- NBBO alternative to consolidated SIP data
- Available as Stocks Business add-on
- All U.S. equities price, reference, and fundamental data

---

## 10. DATA INFRASTRUCTURE & ARCHITECTURE

### Source URLs
- https://massive.com/blog/were-moving-datacenters
- https://polygon.io/knowledge-base/categories/infrastructure
- https://polygon.io/knowledge-base/article/which-timestamps-are-returned-for-polygons-stock-trades-and-nbbo-quotes

### Data Center Locations

| Location | Facility | Purpose |
|----------|----------|---------|
| **Secaucus, NJ** | Equinix NY2 + NY5 | Primary -- co-located with NYSE, Nasdaq, CBOE, Bats |
| **Chicago, IL** | Equinix ORD11 | Full redundancy -- co-located with CME Group |

### Co-location Benefits
- **Direct physical connections** to exchanges (minimizes latency, maximizes integrity)
- Same facilities as NYSE, Nasdaq, Bats, CBOE
- CME Globex feeds sourced via dedicated Chicago connections
- OPRA co-location for options data

### Data Coverage
- **Scale:** 2+ PB of historical market data
- **Historical depth:** 20+ years of tick-level trade and quote data
- **Exchanges:** All 19 U.S. stock exchanges + FINRA TRFs + dark pools
- **Options:** All 17 U.S. options exchanges (OPRA)
- **Futures:** CME, CBOT, COMEX, NYMEX (CME Group)
- **Forex:** 1,100+ currency pairs
- **Crypto:** 166 tickers from 4 exchanges
- **Indices:** 11,400+ indices

### Timestamp Handling
- **Resolution:** Nanosecond precision
- **Trade timestamps returned:**
  - SIP timestamp (`t`) -- when the SIP received the trade
  - Participant timestamp (`pt`) -- when the exchange/TRF generated the trade
  - TRF timestamp (`trft`) -- when the TRF received the trade
- **Format:** Unix epoch in nanoseconds (trades) or milliseconds (some WS channels)
- **Data sources for stocks:** CTA (NYSE-listed + regional), UTP (Nasdaq-listed)
- **Data sources for options:** OPRA

### Data Normalization
- Historical dividends are NOT adjusted for splits (noted in KB)
- Splits have `historical_adjustment_factor` for price normalization
- Bid_size/ask_size reported in shares (not round lots) since November 3, 2025 per SEC MDI rules
- Backfilled history for consistency with new share-based reporting

### Real-time vs Historical Normalization
- Real-time: SIP/OPRA feed, sub-millisecond from exchange to client
- Historical: Same data, archived in flat files and queryable via REST
- Consistency maintained across delivery methods (REST = WS = flat files for same data point)

---

## 11. KNOWLEDGE BASE ARTICLES

### Source URLs
- https://massive.com/knowledge-base
- https://massive.com/knowledge-base/categories/*

### Known Categories

| Category | URL | Key Articles |
|----------|-----|--------------|
| **FAQ** | /categories/faq | General platform questions |
| **Support** | /categories/support | Technical assistance |
| **How-To** | /categories/how-to | Step-by-step guides |
| **WebSockets** | /categories/websockets | WS connection, topics, limits |
| **REST** | /categories/rest | REST endpoints, rate limits |
| **Timestamps** | /categories/timestamps | Timestamp formats, SIP vs participant |
| **Infrastructure** | /categories/infrastructure | Data center, architecture |
| **Data Coverage** | /categories/data-coverage | What data is available |
| **Sources** | /categories/sources | Where data comes from |
| **Financials** | /categories/financials | Fundamentals data |
| **Reference Data** | /categories/reference-data | Tickers, exchanges, conditions |
| **Flat Files** | (within docs) | S3 access, file formats |

### Key KB Articles Identified

| Article | URL (massive.com path) | Summary |
|---------|----------------------|---------|
| What are the different subscriptions? | /knowledge-base/article/what-are-the-different-polygon-subscriptions-i-can-use | Plans and tiers |
| Does Massive offer dark pool data? | /knowledge-base/article/does-polygon-offer-dark-pool-data | Yes: exchange=4 + trfi field |
| How many WebSocket connections? | /knowledge-base/article/how-many-polygon-websocket-connections-can-i-use-at-one-time | 1 per asset class |
| How many tickers per WS connection? | /knowledge-base/article/how-many-tickers-can-you-subscribe-to-on-a-single-massive-websocket-connection | Varies by asset class |
| Which timestamps are returned? | /knowledge-base/article/which-timestamps-are-returned-for-polygons-stock-trades-and-nbbo-quotes | SIP, participant, TRF timestamps |
| REST API request limits? | /knowledge-base/article/what-is-the-request-limit-for-massives-restful-apis | Free: 5/min, Paid: unlimited |
| Does Massive have a status page? | /knowledge-base/article/does-massive-have-a-market-holiday-or-status-page | Yes: massive-status.com |
| How to get started with S3? | /knowledge-base/article/how-to-get-started-with-s3 | AWS CLI, Rclone, MinIO, Boto3 setup |
| When does Massive scrape EDGAR? | /knowledge-base/article/when-does-polygon-scrape-edgar-company-filings-for-financial-reports | Daily |
| Does Massive adjust dividends for splits? | /knowledge-base/article/does-polygon-adjust-historic-dividends-for-splits | No |

---

## 12. BLOG POSTS & TUTORIALS

### Source URLs
- https://massive.com/blog
- https://massive.com/blog/tag/tutorial
- https://massive.com/blog/tag/announcement
- https://massive.com/blog/tag/release-notes
- https://massive.com/blog/tag/new
- https://massive.com/blog/tag/update
- https://massive.com/blog/tag/options

### Key Blog Posts Catalogued

#### Tutorials

| Title | URL | Date | Summary |
|-------|-----|------|---------|
| Build a NYSE Order Imbalance Tracker with Massive's WebSocket API | /blog/build-a-nyse-order-imbalance-tracker-with-massives-websocket-api | 2025 | Python WebSocket NOI subscriber with real-time display |
| Build a Real-Time Dark Pool Scanner with Massive's WebSocket API | /blog/dark-pool-scanner-with-massive | 2025 | Terminal dark pool scanner in <150 lines Python |
| Build an Iron Condor Screener with Massive | /blog/build-an-iron-condor-screener-with-massive | Dec 9, 2025 | Python utility screening iron condors on SPY using options API |
| Build a 0-DTE Covered Call Screener for SPY | /blog/build-a-0-dte-covered-call-screener-for-spy-with-polygon-io | 2025 | Same-day expiration covered call selection |
| Pattern for Non-Blocking WebSocket and REST Calls in Python | /blog/pattern-for-non-blocking-websocket-and-rest-calls-in-python | 2025 | Async patterns for combining WS + REST |
| Massive + Python: Unlocking Real-Time and Historical Stock Market Data | /blog/polygon-io-with-python-for-stock-market-data | 2025 | Python SDK getting started |
| Massive + Go: Unlocking Real-Time and Historical Stock Market Data | /blog/go-stock-market-data | 2025 | Go SDK getting started |
| Massive + Kotlin: Unlocking Real-Time and Historical Stock Market Data | /blog/jvm-stock-market-data | 2025 | JVM SDK getting started |
| Analyzing Market Sentiment with Short Volume and Short Interest APIs | /blog/short-volume-short-interest-tutorial | 2025 | Short squeeze detection |
| Build a Corporate Events Calendar using Massive + TMX | /blog/build-a-corporate-events-calendar-using-massive-tmx-wall-street-horizon | 2025 | TMX integration tutorial |
| Deep Dive into Trade-Level Data with Flat Files | /blog/insights-from-trade-level-data | 2024+ | Analyzing tick data from flat files |
| Querying Financial Markets with MCP Server + Claude 4 | /blog/querying-financial-markets-with-the-polgon-io-mcp-server-claude-4-and-pydantic-ai | 2026 | MCP server + Claude + Pydantic AI |
| Creating Stock Market Reports with GPT-5 + Agent SDK + MCP | /blog/creating-stock-market-reports-using-open-ais-gpt-5-and-agent-sdk-with-the-polygon-io-mcp-server-in-under-200-lines-of-code | 2026 | OpenAI GPT-5 + MCP in <200 lines |

#### Announcements

| Title | URL | Date | Summary |
|-------|-----|------|---------|
| Polygon.io is Now Massive | /blog/polygon-is-now-massive | Oct 30, 2025 | Rebrand announcement |
| Massive + ETF Global Partnership | /blog/announcing-massive-etf-global-partnership-constituents-fund-flows-analytics-profiles-and-taxonomies-2 | Feb 2026 | ETF data partnership |
| Balance Sheets, Cash Flow, Income Statements | /blog/announcing-polygon-io-financials-balance-sheets-cash-flow-income-statements-and-ratios | Oct 22, 2025 | Fundamentals API launch |
| Options Chain Snapshot API | /blog/announcing-options-chain-snapshot-api | 2024 | Options snapshot endpoint |
| V2 Tick API | /blog/v2-tick-api | 2024 | Enhanced tick data |
| Client Library Updates | /blog/client-library-updates | 2025 | SDK modernization |
| New Pagination Patterns (Cursors + Filter Extensions) | /blog/api-pagination-patterns | 2024 | Cursor-based pagination |
| Historical File Downloads Included in All Paid Plans | /blog/flat-files | Mar 2024 | Free flat files for paid users |
| Indices Data Has Arrived | /blog/indices-data-has-arrived | 2023 | 11,400+ indices launched |
| Massive Integrates Nasdaq Basic | /blog/polygon-integrates-nasdaq-basic-to-deliver-market-data-to-leading-applications-and-websites | 2023 | Nasdaq Basic integration |
| Simplifying Data Access with CSV Support | /blog/simplifying-data-access-with-csv-support | 2023 | CSV flat files launch |
| New Stock Financials API | /blog/new-stock-financials-api | 2023 | Financials from EDGAR |
| Series A Funding | /blog/series-a-funding | Oct 2020 | $6M raise |
| We Have a Blog! | /blog/we-have-a-blog | earliest | First blog post |

#### ClickHouse Integration (External)
- **Build a real-time market data app with ClickHouse and Massive** -- https://clickhouse.com/blog/build-a-real-time-market-data-app-with-clickhouse-and-polygonio

---

## 13. CHANGELOG & RELEASE NOTES

### Source URLs
- https://massive.com/changelog
- https://massive.com/blog/tag/release-notes
- https://massive.com/blog/release-notes-june-2025
- https://massive.com/blog/release-notes-september-2024
- https://massive.com/blog/release-notes-april-2024

### Key Changes (reverse chronological)

#### 2026
- **May 2026:** Custom Bars API 504 errors on minute/hourly for select tickers (resolved May 21)
- **Feb 2026:** ETF Global partnership announced (Constituents, Fund Flows, Analytics, Profiles, Taxonomies)
- **Feb 23, 2026:** Schema-breaking decimal-size change in community examples
- **Jan-May 2026:** Continued MCP server development, blog posts on AI agent integration

#### 2025
- **Nov 3, 2025:** bid_size/ask_size now reported in shares (not round lots) across Stocks Quotes REST, WebSocket, and Flat Files per SEC MDI rules. History backfilled.
- **Oct 30, 2025:** Polygon.io rebranded as Massive.com
- **Nov 14, 2025:** TMX Wall Street Horizon partnership announced (closed the market at TSX)
- **Oct 22, 2025:** Financials API launched (balance sheets, cash flow, income statements, ratios)
- **Aug 11, 2025:** Level 2 Crypto WebSocket sunset
- **June 2025:** Benzinga partnership (news, earnings, analyst ratings, guidance)
- **June 2025:** JS/TS SDK major version update (v8.0 -- code-gen from OpenAPI, breaking changes)
- **June 2025:** JVM SDK beta branch (code-gen from OpenAPI)
- **2025:** New APIs for short interest, short volume, treasury yields
- **2025:** NYSE NOI WebSocket generally available
- **2025:** SEC EDGAR filings API (beta, free during early access)
- **2025:** Financial ratios API (40+ metrics, TTM + daily price)

#### 2024
- **Sep 2024:** New data center operations, advanced API functionalities
- **Apr 2024:** Daily historical flat files included at no additional charge for all paid plans
- **2024:** Options Chain Snapshot API launched
- **2024:** V2 Tick API announced
- **2024:** New cursor-based pagination with query filter extensions

#### 2023
- **2023:** Indices data launched (11,400+ indices)
- **2023:** Nasdaq Basic integration
- **2023:** CSV flat files support
- **2023:** New Stock Financials API

---

## 14. API STATUS & INCIDENTS

### Source URLs
- https://massive-status.com/ (redirected from polygonstatus.com)
- https://polygonio.statuspage.io/uptime

### Current Status (as of 2026-05-26)
**All Systems Operational**

### 90-Day Uptime (as of 2026-05-26)

| Service | Uptime |
|---------|--------|
| Stocks | 99.99% |
| Options | 99.97% |
| Indices | 99.99% |
| Forex | 99.99% |
| Crypto | 99.92% |
| Futures (Beta) | 100% |

Each service includes: Market Data REST, Reference Data REST, WebSocket, Flat Files -- all 99.84%+ uptime individually.

### Recent Incidents

| Date | Incident | Status |
|------|----------|--------|
| May 21, 2026 | Custom Bars API 504 errors on minute/hourly requests for select stock tickers | Resolved (fix deployed, monitoring completed 14:58 EDT) |
| May 18-19, 2026 | Scheduled infrastructure upgrade + Crypto delays (upstream Coinbase outage) | Resolved May 18, 09:11 EDT |
| May 15-18, 2026 | Options reference/snapshot data degradation for newly created contracts (upstream provider) | Resolved May 18, 08:47 EDT |

---

## 15. COMMUNITY EXAMPLES & SAMPLE APPS

### Source URLs
- https://github.com/polygon-io/community
- https://polygon.io/sample-applications
- https://github.com/massive-com/community

### Official Community Repository

**Repository:** `github.com/polygon-io/community` (also `massive-com/community`)

**Structure:**
```
examples/
  rest/           -- REST API demonstrations
    options-iron-condor/  -- Iron condor screening in Python
    ...
  websocket/      -- WebSocket API demonstrations
  integrations/   -- Database, charting, analytics platform integrations
```

**Requirements:** `MASSIVE_API_KEY` environment variable

**Known examples (17 total per massive-community-examples skill):**
- 13 REST examples
- 4 WebSocket examples
- Including: NOI WebSocket subscription pattern, new /stocks/filings and /consumer-spending/eu surfaces

### Third-Party Examples
- **timkpaine/polygon-io-examples** -- Dashboards, scripts, notebooks, utilities
- **bobtabor/PolygonDownloadAmazonS3FlatFile** -- Flat file download utility
- **shinathan/polygon.io-stock-database** -- 1-min, 5-min, daily database builder

### YouTube Tutorials
- Screen for Iron Condors using Python and Massive (official)
- Demo: Getting Started with Polygon.io + Indices Data (S&P 500)

---

## 16. RELEVANCE TO OUR SYSTEM

### What Anish Has Access To (per KNOWN_SUBSCRIPTIONS.md)

| Product | Status | Monthly Cost |
|---------|--------|------|
| Stocks Advanced (real-time SIP) | ACTIVE | $199 |
| Options Advanced (real-time OPRA) | ACTIVE | $199 |
| Order Imbalances (NOI WebSocket) | ACTIVE | $49 |
| Benzinga News | ACTIVE | $99 |
| Benzinga Earnings | ACTIVE | $99 |
| ETF Global Fund Flows | ACTIVE | $99 |
| ETF Global Constituents | ACTIVE | $99 |
| Currencies Basic | ACTIVE | Free |
| Futures Basic | ACTIVE | Free |
| Indices Basic | ACTIVE | Free |

**NOT subscribed (verified 403):** Benzinga Ratings, Benzinga Analyst Insights, Benzinga Guidance, TMX Corporate Events, ETF Global Taxonomies/Profiles/Analytics.

### Critical Data Delivery Paths for Our Stack

1. **S3 Flat Files** (bulk historical) -- us_stocks_sip, us_options_opra, us_indices, us_futures_*, global_forex, global_crypto
   - Endpoint: https://files.massive.com (or files.polygon.io)
   - Bucket: flatfiles
   - Keys: In env as MASSIVE_S3_ACCESS_KEY_ID / MASSIVE_S3_SECRET_ACCESS_KEY

2. **REST API** (on-demand queries, fundamentals, reference data, filings) -- api.massive.com
   - Key: MASSIVE_API_KEY (Bearer auth)
   - Unlimited requests on paid plan
   - Cursor-based pagination with next_url

3. **WebSocket API** (real-time streaming) -- socket.massive.com
   - Stocks: T.*, Q.*, A.*, AM.*, LULD.*, NOI.*
   - Options: trades, quotes, aggs
   - 1 connection per asset class

4. **MCP Server** (AI-powered queries in Claude Code sessions)
   - search_endpoints -> call_api -> query_data pipeline
   - In-memory SQLite + 14 apply= functions

### Key Technical Facts for System Design

- **Timestamps:** Nanosecond precision. SIP timestamp (`t`), participant timestamp (`pt`), TRF timestamp (`trft`).
- **Dark pool detection:** exchange=4 + trfi field present
- **NOI is WebSocket-only** -- no REST endpoint for order imbalances
- **FMV is Business-only** -- Anish has Advanced, not Business
- **Bid/ask sizes in shares** (not round lots) since Nov 3, 2025
- **SEC filings endpoints are beta** (free, may change plans later)
- **Financial ratios use TTM** + most recent daily stock price
- **Short interest updates bi-weekly** (FINRA cadence)
- **Flat files included in all paid plans** at no extra charge
- **Options WS limit:** 1,000 simultaneous contract subscriptions per connection
- **Historical adjustment factor** available for splits but dividends are NOT split-adjusted

### Gaps / Not Available from Massive

- **Level 2 / order book data:** Not available (L2 Crypto was sunset Aug 2025)
- **Real-time order flow analytics:** Not built-in (must be constructed from trades)
- **Intraday VWAP:** Must be calculated from tick data
- **Custom Pine Script indicators:** Not related (Massive is data, TV is charting)
- **Form 13D/G, Form ADV, Form D, Mutual Fund N-CEN:** Not in Massive (go to SEC EDGAR direct)

---

## APPENDIX: ALL URLS CRAWLED

### Documentation
- https://massive.com/docs
- https://massive.com/docs/llms.txt
- https://massive.com/docs/llms-full.txt
- https://massive.com/docs/rest/quickstart
- https://massive.com/docs/rest/stocks/overview
- https://massive.com/docs/rest/options/overview
- https://massive.com/docs/rest/stocks/fundamentals/ratios
- https://massive.com/docs/rest/stocks/fundamentals/short-interest
- https://massive.com/docs/rest/stocks/corporate-actions/dividends
- https://massive.com/docs/rest/stocks/corporate-actions/splits
- https://massive.com/docs/rest/stocks/filings/index
- https://massive.com/docs/rest/partners/tmx/corporate-events
- https://massive.com/docs/rest/partners/etf-global/fundflows
- https://massive.com/docs/websocket/quickstart
- https://massive.com/docs/websocket/stocks/overview
- https://massive.com/docs/websocket/stocks/trades
- https://massive.com/docs/websocket/stocks/imbalances
- https://massive.com/docs/websocket/stocks/luld
- https://massive.com/docs/websocket/stocks/fair-market-value
- https://massive.com/docs/websocket/options/overview
- https://massive.com/docs/websocket/forex/overview
- https://massive.com/docs/websocket/crypto/overview
- https://massive.com/docs/flat-files/quickstart
- https://massive.com/docs/flat-files/stocks/overview

### Product Pages
- https://massive.com/pricing
- https://massive.com/futures
- https://massive.com/currencies
- https://massive.com/options (polygon.io/options)
- https://massive.com/sql
- https://massive.com/alternative/consumer-spending
- https://massive.com/partners/benzinga
- https://massive.com/partners/etf-global
- https://massive.com/partners/business-tmx
- https://massive.com/about

### Knowledge Base
- https://massive.com/knowledge-base
- https://massive.com/knowledge-base/categories/faq
- https://massive.com/knowledge-base/categories/support
- https://massive.com/knowledge-base/categories/websockets
- https://massive.com/knowledge-base/categories/rest
- https://massive.com/knowledge-base/categories/timestamps
- https://massive.com/knowledge-base/categories/infrastructure
- https://massive.com/knowledge-base/categories/data-coverage
- https://massive.com/knowledge-base/categories/sources
- https://massive.com/knowledge-base/categories/financials
- https://massive.com/knowledge-base/categories/reference-data
- https://massive.com/knowledge-base/article/what-are-the-different-polygon-subscriptions-i-can-use
- https://massive.com/knowledge-base/article/does-polygon-offer-dark-pool-data
- https://massive.com/knowledge-base/article/how-many-polygon-websocket-connections-can-i-use-at-one-time
- https://massive.com/knowledge-base/article/which-timestamps-are-returned-for-polygons-stock-trades-and-nbbo-quotes
- https://massive.com/knowledge-base/article/what-is-the-request-limit-for-massives-restful-apis
- https://massive.com/knowledge-base/article/does-massive-have-a-market-holiday-or-status-page
- https://massive.com/knowledge-base/article/how-to-get-started-with-s3
- https://massive.com/knowledge-base/article/when-does-polygon-scrape-edgar-company-filings-for-financial-reports
- https://massive.com/knowledge-base/article/does-polygon-adjust-historic-dividends-for-splits

### Blog Posts
- https://massive.com/blog
- https://massive.com/blog/polygon-is-now-massive
- https://massive.com/blog/build-a-nyse-order-imbalance-tracker-with-massives-websocket-api
- https://massive.com/blog/dark-pool-scanner-with-massive
- https://massive.com/blog/build-an-iron-condor-screener-with-massive
- https://massive.com/blog/build-a-0-dte-covered-call-screener-for-spy-with-polygon-io
- https://massive.com/blog/pattern-for-non-blocking-websocket-and-rest-calls-in-python
- https://massive.com/blog/polygon-io-with-python-for-stock-market-data
- https://massive.com/blog/go-stock-market-data
- https://massive.com/blog/jvm-stock-market-data
- https://massive.com/blog/short-volume-short-interest-tutorial
- https://massive.com/blog/build-a-corporate-events-calendar-using-massive-tmx-wall-street-horizon
- https://massive.com/blog/insights-from-trade-level-data
- https://massive.com/blog/querying-financial-markets-with-the-polgon-io-mcp-server-claude-4-and-pydantic-ai
- https://massive.com/blog/creating-stock-market-reports-using-open-ais-gpt-5-and-agent-sdk-with-the-polygon-io-mcp-server-in-under-200-lines-of-code
- https://massive.com/blog/announcing-massive-etf-global-partnership-constituents-fund-flows-analytics-profiles-and-taxonomies-2
- https://massive.com/blog/announcing-polygon-io-financials-balance-sheets-cash-flow-income-statements-and-ratios
- https://massive.com/blog/announcing-options-chain-snapshot-api
- https://massive.com/blog/v2-tick-api
- https://massive.com/blog/client-library-updates
- https://massive.com/blog/api-pagination-patterns
- https://massive.com/blog/flat-files
- https://massive.com/blog/indices-data-has-arrived
- https://massive.com/blog/polygon-integrates-nasdaq-basic-to-deliver-market-data-to-leading-applications-and-websites
- https://massive.com/blog/simplifying-data-access-with-csv-support
- https://massive.com/blog/new-stock-financials-api
- https://massive.com/blog/series-a-funding
- https://massive.com/blog/were-moving-datacenters
- https://massive.com/blog/release-notes-june-2025
- https://massive.com/blog/release-notes-september-2024
- https://massive.com/blog/release-notes-april-2024

### Changelog & Status
- https://massive.com/changelog
- https://massive-status.com/
- https://polygonio.statuspage.io/uptime

### GitHub Repositories
- https://github.com/massive-com/client-python (v2.8.0, ~1,400 stars)
- https://github.com/massive-com/client-go (v3.3.0)
- https://github.com/massive-com/client-js
- https://github.com/massive-com/client-jvm
- https://github.com/massive-com/mcp_massive (v0.10.0)
- https://github.com/polygon-io/community (official examples)

### External Resources
- https://clickhouse.com/blog/build-a-real-time-market-data-app-with-clickhouse-and-polygonio
- https://deepwiki.com/massive-com/client-python
- https://pkg.go.dev/github.com/polygon-io/client-go/websocket
- https://www.crunchbase.com/organization/polygon-io

---

*End of crawl. This document contains all findings from 60+ web searches and 40+ page fetches conducted on 2026-05-26.*
