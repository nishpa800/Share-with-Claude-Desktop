# GitHub & Massive Repo Inventory — Phase 0 Recon

**Generated:** 2026-05-26
**Source:** Live scan of `/Users/anishpatel/code/massive-com/`, `gh repo list nishpa800`, and skill source-of-truth files.

---

## PART 1: ~/code/massive-com/ — Full Inventory (38 repos)

### TIER 1 — CRITICAL: Client SDKs + MCP + Community

| Repo | Lang | Last Commit | Summary | Relevance |
|---|---|---|---|---|
| **client-python** | Python | 2026-04-10 | Official Massive Python SDK. 76 REST methods (14 domain mixins: aggs, trades, quotes, snapshots, indicators, reference, summaries, financials, benzinga, etf-global, futures, economy, tmx, experimental). 7 WS methods. Auth via `MASSIVE_API_KEY` env. Auto-pagination via `next_url`. Retry: urllib3 status_forcelist `[413,429,499,500,502,503,504]`. | **PRIMARY** — main SDK for our pipeline |
| **client-go** | Go | 2026-04-27 | Official Massive Go SDK. 145 REST methods (oapi-codegen from OpenAPI). WS: gorilla/websocket + cenkalti/backoff + tomb.v2. Three-goroutine arch (read/write/process) with 100k-buffered Output() channel. 18 feed hosts, 10 markets, 36 topics, 19 WS model structs. | **HIGH** — best for high-throughput WS capture (1M+ msgs/sec) |
| **client-js** | TypeScript | 2026-04-27 | Official Massive JS SDK. 145 async REST methods on flat `DefaultApi` (OpenAPI-generated, 49.5k LOC `api.ts`). 487 interfaces, 252 enums. v8.0 breaking change: single `requestParameters` object. 6 WS factories. | **MEDIUM** — useful for web dashboards; canonical OpenAPI schema at `src/openapi.json` |
| **client-jvm** | Kotlin | 2026-02-05 | Official Massive JVM SDK. REST: OpenAPI-generated `DefaultApi` (18,261 LOC, ~100 methods, OkHttp+Moshi). WS: hand-written ktor + kotlinx.serialization + coroutines. 17 feed hosts, 14 markets, 361 model data classes. | **REFERENCE** — 361 model classes = most complete schema reference across all SDKs |
| **mcp_massive** | Python | 2026-04-17 | Massive MCP Server (v0.9.1). 3 tools: `search_endpoints` (BM25 FTS5 over llms-full.txt), `call_api` (REST proxy + pagination + store_as), `query_data` (SQLite over stored DataFrames). 14 apply= functions (6 BS Greeks + 5 returns + 2 technicals). Already installed via `uv tool install`. | **PRIMARY** — our LLM-data bridge |
| **community** | Mixed | 2026-04-23 | Official examples repo. 13 REST + 4 WebSocket examples. Contains the confirmed NOI subscription pattern, dark-pool scanner, LULD monitor, options premium scanner, filings demo, ETF/Benzinga/TMX dashboards, and more. | **PRIMARY** — patterns and reference implementations |

### TIER 2 — HIGH VALUE: AI Rules, Plugins, Infra

| Repo | Lang | Last Commit | Summary | Relevance |
|---|---|---|---|---|
| **claude-code-plugin** | Markdown/skills | 2026-04-24 | Massive Claude Code Plugin. 5 slash commands (`/massive:scaffold`, `discover`, `debug`, `options`, `dashboard`). 24 KB CLAUDE.md auto-loads every session with SDK patterns, ticker formats, plan tiers, failure modes. | **INSTALLED** — already active in our sessions |
| **codex-plugin** | Markdown/skills | 2026-04-27 | Massive Codex Plugin (OpenAI). Same 5 skills as Claude plugin + bundled MCP via `.mcp.json` + `uvx`. Patterns worth porting to our workflow. | LOW — reference only |
| **massive-ai-rules** | Markdown | 2026-04-23 | AI instruction files for all coding assistants (Claude, Codex, Cursor, Copilot, Windsurf, Gemini). Same 22KB core knowledge replicated per tool. | LOW — already consumed via claude-code-plugin |
| **indicator** | Go | 2025-11-06 | Fork of `cinar/indicator`. ~50 textbook TA indicators (SMA, EMA, RSI, MACD, Bollinger, ATR, OBV, MFI, VWAP, Stochastic, etc.) with backtesting framework. | **MEDIUM** — useful Go TA library; NONE of Anish's custom Pine indicators are here |
| **tradingview-adapter** | JS | 2020-02-14 | JS adapter for feeding Massive data into TradingView Charting Library (JS widget). **NOT compatible with TradingView Desktop** — only works with the embeddable JS widget. | **NOT COMPATIBLE** — Anish uses TV Desktop |
| **optimize** | Go | 2025-07-24 | Fork of `pa-m/optimize`. Numerical optimization: Brent, Golden Section, Powell, CMA-ES. Pure math optimization — NOT a financial backtester. | LOW — potential use in parameter optimization |

### TIER 3 — DATA INFRASTRUCTURE (Apache Arrow / DataFusion ecosystem)

| Repo | Lang | Last Commit | Summary | Relevance |
|---|---|---|---|---|
| **arrow-datafusion** | Rust | 2025-08-25 | Apache DataFusion SQL query engine. Massive's internal query engine for their flat-file and analytical workloads. | **HIGH-POTENTIAL** — SQL engine for querying our Parquet flat files |
| **datafusion-materialized-views** | Rust | 2025-11-05 | Incremental view maintenance + query rewriting for materialized views in DataFusion. Hive-partitioned files in object storage. | **HIGH-POTENTIAL** — incremental materialized views over our S3 flat files |
| **datafusion-objectstore-s3** | Rust | 2023-03-11 | S3 ObjectStore implementation for DataFusion. Enables querying Parquet files directly from S3. | **HIGH-POTENTIAL** — query Massive flat files on S3 without download |
| **datafusion-postgres** | Rust | 2025-09-05 | Postgres wire protocol frontend for DataFusion. Lets any Postgres client (DBeaver, psql, JDBC) query DataFusion. | **HIGH-POTENTIAL** — expose our data warehouse via standard SQL |
| **pg_catalog** | Rust | 2025-08-26 | Postgres system catalog compatibility layer for DataFusion. Enables BI tools expecting pg_catalog schema. | MEDIUM — companion to datafusion-postgres |
| **corr-subq-udf-rs** | Rust | 2025-08-26 | Correlated subquery-to-UDF rewriter for DataFusion. | LOW — niche query optimization |
| **vortex** | Rust/Python | 2026-04-22 | Next-gen columnar file format (Linux Foundation). 100x faster random access vs Parquet. Rust + Python + JVM bindings. | **HIGH-POTENTIAL** — future replacement for Parquet in our pipeline |
| **arrow-rs** | Rust | 2024-03-11 | Official Rust implementation of Apache Arrow. | MEDIUM — dependency of DataFusion stack |
| **arrow-rs-object-store** | Rust | 2025-06-30 | Rust object_store crate (S3/GCS/Azure/local FS). | MEDIUM — dependency of DataFusion + S3 |
| **arrow** | C++/Multi | N/A (no git log) | Apache Arrow multi-language toolbox. | LOW — old fork, no local history |
| **parquet-go** | Go | 2023-03-09 | High-performance Go Parquet reader/writer (segmentio). | MEDIUM — potential for Go-based flat-file processing |

### TIER 4 — INTERNAL INFRA & MISCELLANEOUS

| Repo | Lang | Last Commit | Summary | Relevance |
|---|---|---|---|---|
| **errands-server** | Go | 2025-11-06 | HTTP-based job queue with SSE. Persistent storage via Badger (SSD). Concurrency-safe multi-worker. | LOW — internal Massive infra |
| **errands-go** | Go | 2022-06-30 | Go client for Errands API. | LOW |
| **errands-js** | JS | 2025-11-06 | JS client for Errands API. | LOW |
| **go-app-ticker-wall** | Go | 2025-11-06 | Cross-platform scrolling ticker tape display. Leader-GUI architecture, gRPC. | LOW — office display tool |
| **go-multicast-dump** | Go | 2025-11-06 | CLI tool to dump UDP multicast traffic in hex. | LOW — network debug utility |
| **xbrl-parser** | Go | 2025-11-06 | Go XBRL document parser (facts, contexts, units). SEC filing parsing. | MEDIUM — useful for parsing raw XBRL filings |
| **simple-binary-encoding** | Java/C++ | 2023-01-19 | SBE (FIX Trading Community) — OSI layer 6 binary encoding for low-latency financial apps. | LOW — Massive's internal wire format |
| **kin-openapi** | Go | 2021-06-07 | OpenAPI 3.0 file handler for Go. Used by oapi-codegen for client-go generation. | LOW — build dependency |
| **nanovgo** | Go | 2025-11-06 | NanoVG OpenGL rendering library (Go port). | NONE — graphics library |
| **drone** | Go | 2021-03-31 | CI/CD pipeline tool. | NONE — Massive's old CI |
| **puppet-k8s** | Ruby | 2025-08-13 | Puppet module for K8s deployment. | NONE — Massive's infrastructure automation |
| **sftp** | Go | 2019-04-11 | Go SFTP package (SSH file transfer). | NONE |
| **ceph** | Unknown | N/A | Distributed storage (no local git history). | NONE |
| **aws-sdk-go-v2** | Unknown | N/A | AWS SDK for Go (no local git history). | NONE — use the real AWS SDK |
| **contentful-markdown-plugin** | JS | 2022-02-09 | Contentful CMS markdown editor extension. | NONE — CMS plugin |

---

## PART 2: Critical SDK Deep-Dive

### client-python (76 REST + 7 WS methods)

**Source:** `/Users/anishpatel/code/massive-com/client-python/`
**Skill:** `/Users/anishpatel/.claude/skills/massive-python-sdk`
**Deep doc:** `/Users/anishpatel/code/anish/trading-data-system/sources/massive/community_learnings/client-python.md`

**Auth:** `MASSIVE_API_KEY` env var or `api_key=` kwarg. Sent as `Authorization: Bearer <key>`.
**Pagination:** `next_url`-based generator. `pagination=True` (default) auto-follows all pages. `pagination=False` returns one page.
**Retry:** urllib3 `Retry(total=3, status_forcelist=[413,429,499,500,502,503,504], backoff_factor=0.1)`.
**Import:** `from massive import RESTClient, WebSocketClient`

#### REST Method Inventory (76 total)

| Domain | Count | Methods |
|---|---|---|
| **Aggregates** | 5 | `list_aggs`, `get_aggs`, `get_grouped_daily_aggs`, `get_daily_open_close_agg`, `get_previous_close_agg` |
| **Trades** | 3 | `list_trades`, `get_last_trade`, `get_last_crypto_trade` |
| **Quotes** | 4 | `list_quotes`, `get_last_quote`, `get_last_forex_quote`, `get_real_time_currency_conversion` |
| **Snapshots** | 8 | `list_universal_snapshots`, `get_snapshot_all`, `get_snapshot_direction`, `get_snapshot_ticker`, `get_snapshot_option`, `list_snapshot_options_chain`, `get_snapshot_crypto_book`, `get_snapshot_indices` |
| **Indicators** | 4 | `get_sma`, `get_ema`, `get_rsi`, `get_macd` |
| **Reference** | 23 | `get_market_holidays`, `get_market_status`, `list_tickers`, `get_ticker_details`, `get_ticker_events`, `list_ticker_news`, `get_ticker_types`, `get_related_companies`, `list_splits`, `list_dividends`, `list_conditions`, `get_exchanges`, `get_options_contract`, `list_options_contracts`, `list_short_interest`, `list_short_volume`, `list_stocks_splits`, `list_stocks_dividends`, `list_stocks_filings_risk_factors`, `list_stocks_taxonomies_risk_factors`, `list_stocks_filings_10k_sections`, `list_stocks_filings_8k_text`, `list_stocks_filings_index` |
| **Summaries** | 1 | `get_summaries` |
| **Financials** | 5 | `list_financials_balance_sheets`, `list_financials_cash_flow_statements`, `list_financials_income_statements`, `list_financials_ratios`, `list_stocks_floats` |
| **Benzinga** | 10 | `list_benzinga_analyst_insights`, `list_benzinga_analysts`, `list_benzinga_consensus_ratings`, `list_benzinga_earnings`, `list_benzinga_firms`, `list_benzinga_guidance`, `list_benzinga_news`, `list_benzinga_news_v2`, `list_benzinga_ratings`, `list_benzinga_bulls_bears_say` |
| **ETF Global** | 5 | `get_etf_global_analytics`, `get_etf_global_constituents`, `get_etf_global_fund_flows`, `get_etf_global_profiles`, `get_etf_global_taxonomies` |
| **Futures** | 9 | `list_futures_aggregates`, `list_futures_contracts`, `list_futures_products`, `list_futures_quotes`, `list_futures_trades`, `list_futures_schedules`, `list_futures_market_statuses`, `get_futures_snapshot`, `list_futures_exchanges` |
| **Economy/Fed** | 6 | `list_treasury_yields`, `list_inflation`, `list_inflation_expectations`, `list_labor_market_indicators`, `list_eu_merchant_aggregates`, `list_eu_merchant_hierarchy` |
| **TMX** | 1 | `list_tmx_corporate_events` |
| **Experimental** | 2 | `vx.list_stock_financials`, `vx.list_ipos` |

#### WebSocket Channels

| Market | Channels |
|---|---|
| Stocks | `T` trades, `Q` quotes, `A` per-sec agg, `AM` per-min agg, `LULD` limit-up/down, `NOI` imbalance, `FMV` fair-market-value, `LV` launchpad value |
| Options | `T`, `Q`, `A`, `AM`, `FMV`, `LV` |
| Indices | `A`, `AM`, `V` (index value) |
| Crypto | `XT` trades, `XQ` quotes, `XA`/`XAS` aggs, `XL2` L2 book, `AM`, `FMV`, `LV` |
| Forex | `C` quotes, `CA`/`CAS` aggs, `AM`, `FMV`, `LV` |
| Futures | `T`, `Q`, `A`, `AM` |

#### What is NOT in the Python SDK

- No async REST client (sync urllib3 only; WS is async)
- No token-bucket rate limiter (only blind retry on 429)
- No S3 flat-file client (use boto3 against `s3://flatfiles/`)
- No response caching
- No Greeks calculator (use MCP `apply=` or snapshot endpoints)
- No account/usage/billing endpoints
- No retry observability

### client-go (145 REST + 36 WS topics)

**Source:** `/Users/anishpatel/code/massive-com/client-go/`
**Deep doc:** `/Users/anishpatel/code/anish/trading-data-system/sources/massive/community_learnings/client-go.md`

**Auth:** `MASSIVE_API_KEY` env or constructor arg. Bearer header. Panics if empty.
**Pagination:** `rest.WithPagination(true)` (default). `NewIteratorFromResponse()` auto-follows `next_url`.
**HTTP Timeout:** 60s hardcoded.

**When to use Go over Python:** High-throughput WS capture. The three-goroutine architecture with 100k-buffered Output() channel handles 1M+ msgs/sec on a Mac. Python's asyncio can't match this for full-firehose tick capture.

**Key model structs (19):** EquityAgg, CurrencyAgg, EquityTrade, CryptoTrade, EquityQuote, ForexQuote, CryptoQuote, Imbalance, LimitUpLimitDown, Level2Book, IndexValue, LaunchpadValue, FairMarketValue, FuturesTrade, FuturesQuote, FuturesAggregate, ControlMessage, EventType, Action.

**Gotchas:**
- `LaunchpadValue`/`FairMarketValue` timestamps are nanoseconds (everything else ms)
- `FuturesAggregate` flattens `ev` as a plain string (not embedded struct)
- L2 book is crypto-only
- Iterator loses types (returns `map[string]any`)
- `User-Agent: massive-go-test` hardcoded (leftover)

### client-js (145 REST + 6 WS factories)

**Source:** `/Users/anishpatel/code/massive-com/client-js/`
**Deep doc:** `/Users/anishpatel/code/anish/trading-data-system/sources/massive/community_learnings/client-js.md`

**Auth:** API key via `Configuration.apiKey`. Leaks as query string on pagination follow-ups.
**Pagination:** Opt-in via `globalFetchOptions.pagination = true`. Recursive axios interceptor.

**Key facts:**
- v8.0 (June 2025) BREAKING: every method takes single `requestParameters` object
- `src/openapi.json` is the canonical schema source — pull fresh via `npm run pull-spec`
- 108 REST example files under `examples/rest/`
- Pagination interceptor has probable bug: reads `nextResults.results` instead of `nextResults.data.results`

### client-jvm (~100 REST methods + coroutine WS)

**Source:** `/Users/anishpatel/code/massive-com/client-jvm/`
**Deep doc:** `/Users/anishpatel/code/anish/trading-data-system/sources/massive/community_learnings/client-jvm.md`

**Key value:** 361 model data classes — the most complete schema reference across all SDKs. 17 named feed hosts, 14 market modes.

**Three API flavors per method:** `fooBar()` (suspend), `fooBarBlocking()`, `fooBarAsync(callback)` — designed for Java interop.

---

## PART 3: Community Examples (17 total)

**Source:** `/Users/anishpatel/code/massive-com/community/examples/`

### WebSocket Examples (4) — HIGHEST VALUE

| Example | What It Does | Channel/Endpoint | Key Pattern |
|---|---|---|---|
| **noi-imbalance-monitor** | NYSE NOI event streaming with convergence tracking. Open/Close/Halt auction types. | WS `NOI.*` (Market.Stocks) | `client.subscribe("NOI.*")` — THE confirmed NOI subscription pattern. Fields: `imbalance_quantity`, `paired_quantity`, `book_clearing_price`, `auction_type` (M/C/H). |
| **dark-pool-scanner** | Filters TRF prints by notional >= $100k. Maps TRF IDs (201=FINRA/NYSE, 202=FINRA/NASDAQ Carteret, 203=FINRA/NASDAQ Chicago). | WS `T.*` (Market.Stocks) | `exchange == 4 && trf_id in {201,202,203}` = dark pool. Multi-ticker: `[f"T.{t}" for t in tickers]`. |
| **luld-monitor** | Mag-7 LULD bands + market-wide halt/resumption. Indicators 15/16 (band), 17 (halt), 18 (resume). | WS `LULD.*` | Indicator 17 = halt, 18 = resume. NASDAQ-listed only for halt/resume indicators. |
| **options-premium-scanner** | Large options prints by premium. OSI symbol parsing. | WS `T.*` (Market.Options) | Options trade filtering by size/premium. |

### REST Examples (13)

| Example | What It Does | Endpoint(s) | Key Pattern |
|---|---|---|---|
| **amazon-eu-spending** | Decade of European card spend at Amazon. 200k+ rows daily card-transaction data across 5+ countries. | `/consumer-spending/eu/v1/merchant-hierarchy`, `/consumer-spending/eu/v1/merchant-aggregates` | Month-fan-out concurrency: `asyncio.Semaphore(20)` + `httpx.AsyncClient`. Values are signed negative (card debits). |
| **filings-disclosures-demo** | EDGAR index, 10-K/8-K text, risk-factor taxonomy. **BETA endpoints.** | `/stocks/filings/v1/index`, `10-K/v1/sections`, `8-K/v1/text`, `v1/risk-factors`, `taxonomies/v1/risk-factors` | Pre-classified risk-factor diffs across filings. SDK >= 2.4.0 required. |
| **fractional-share-precision** | Decimal-size fields across WS/REST/flat files. Documents the 2026-02-23 schema breaking change. | WS `ds`/`dv`/`dav`; REST `decimal_size`/`decimal_volume`; flatfiles `trades_v1` | **BREAKING:** `size`/`volume` columns are now decimals in flat files. Use `decimal.Decimal`. S3 partial download: range request `bytes=0-524287`. |
| **go-getting-started** | Aggregates + snapshot demo via client-go v3. | `/v2/aggs/...`, `/v3/snapshot/...` | `rest.NewWithOptions(apiKey, rest.WithPagination(true))` |
| **gpt5-openai-agents-sdk-massive-mcp** | Agentic CLI using OpenAI Agents SDK + mcp_massive over stdio. | MCP server | Agent-loop pattern with Massive MCP. |
| **market-parser-massive-mcp** | Claude 4 + PydanticAI + Massive MCP integration. | MCP server | Anthropic agent pattern. |
| **options-0-dte-covered-call** | 0-DTE SPY covered-call screener with Greeks/IV. | Options chain snapshot + last-trade | Options screening with computed Greeks. |
| **options-advanced-covered-call** | Multi-expiry covered-call optimizer with 7 metrics. | Options chain snapshot, close | Multi-metric options optimization. |
| **options-iron-condor** | Iron condor screener with earnings warning. | `list_options_contracts`, `list_snapshot_options_chain`, `list_benzinga_earnings` | Cross-endpoint join (options + earnings). |
| **partner-benzinga** | Streamlit news + analyst + earnings dashboard. | `/benzinga/v2/news`, `/benzinga/v1/{ratings,analyst-insights,...}` | Benzinga v2 News (new); v1 for everything else. |
| **partner-etf-global** | Streamlit ETF health pulse + HHI + fund-flow z-scores. | `/etf-global/v1/{constituents,fund-flows,analytics,profiles,taxonomies}` | 1-2 business day processing delay on holdings. |
| **partner-tmx** | Streamlit corporate events calendar. 22 event types. | `/tmx/v1/corporate-events` | Low-level `client._get()` with `any_of` modifiers. Historical data starts 2018-01-01. |
| **splits-dividends-demo** | New splits/dividends endpoints + `historical_adjustment_factor`. | `/stocks/v1/splits`, `/stocks/v1/dividends` | Replaces deprecated `/v3/reference/{splits,dividends}`. |

### Critical Gotchas from Community Examples

1. **Flat-file `size`/`volume` are NOW decimals** (2026-02-23). Pipelines casting to int will truncate.
2. **Decimal fields are strings** — use `decimal.Decimal`, not float.
3. **NOI coverage is NYSE-listed only** — no NASDAQ names. Windows: 9:00-9:30 ET (open), 15:50-16:00 ET (close).
4. **LULD indicators 17/18 are NASDAQ-listed only**.
5. **Consumer-spending values are signed negative** (card debits).
6. **`next_url` strips the API key** — re-inject on every paginated request.
7. **Filings endpoints are BETA** — not all companies have parsed text.
8. **ETF holdings have 1-2 business day processing delay**.
9. **TMX historical data starts 2018-01-01**.
10. **Benzinga news is v2; all other Benzinga endpoints are v1**.

---

## PART 4: MCP Server (`mcp_massive`)

**Source:** `/Users/anishpatel/code/massive-com/mcp_massive/`
**Deep doc:** `/Users/anishpatel/code/anish/trading-data-system/sources/massive/community_learnings/mcp_massive.md`

### 3 Tools (read-only)

| Tool | Purpose | Key Details |
|---|---|---|
| `search_endpoints` | Natural language endpoint discovery | BM25 FTS5 over `llms-full.txt`. Column weights: title=10, description=1, path_info=0.5, attrs=0.1, market=5. Market keywords get 2x boost. Synonym expansion via `constants.ALIASES`. |
| `call_api` | Generic REST proxy | Auto `next_url` pagination. Path allowlist from indexed endpoints. `store_as` saves to in-memory SQLite. 50 MB response cap. 30s httpx timeout. |
| `query_data` | SQL over stored data | SQLite `:memory:`. sqlglot AST validation (SELECT-only). FTS5 auto-enabled on TEXT columns. 30s timeout. TTL 3600s. Max 50 tables, 50k rows/table. |

### 14 apply= Functions (client-side numpy, NOT on Massive servers)

| Category | Functions |
|---|---|
| **Greeks** | `bs_price`, `bs_delta`, `bs_gamma`, `bs_theta` (daily), `bs_vega` (per 1%), `bs_rho` (per 1%) |
| **Returns** | `simple_return`, `log_return`, `cumulative_return`, `sharpe_ratio` (rolling, ddof=1), `sortino_ratio` (downside-only) |
| **Technical** | `sma` (rolling mean), `ema` (EWM, alpha=2/(span+1)) |

### Architecture

- **Endpoint index:** Fetches `https://massive.com/docs/rest/llms-full.txt` at first call. Parses into FTS5 virtual table. Porter tokenizer. Dedup by title (4x over-fetch).
- **Path allowlist:** Regex-escaped `path_prefix` strings. Blocks `..`, `\`, `?`, `#`, double-encoding.
- **Store:** SQLite `:memory:`. sqlglot validates AST. Authorizer denies non-SELECT. Function allowlist (~50 names). TTL = 1 hr.
- **Pipeline cap:** 20 apply= steps max. Closed registry — no arbitrary code execution.

### Configuration

```
MASSIVE_API_KEY          — already set
MASSIVE_MAX_TABLES=50    — default; bump for multi-asset scans
MASSIVE_MAX_ROWS=50000   — default; bump to 200k+ for tick reconstruction
MASSIVE_LLMS_TXT_URL     — leave unset to track latest
```

---

## PART 5: GitHub — nishpa800 Repos (30 repos)

### Anish's Own Repos

| Repo | Visibility | Last Push | Purpose |
|---|---|---|---|
| **trading-data-system** | private | 2026-05-26 | Core pipeline: Massive S3/REST puller -> OWC Envoy Ultra. Agent plist configs. KNOWN_SUBSCRIPTIONS.md. Skill source-of-truth files. |
| **indicators** | public | 2026-05-26 | Pine indicator suite: B2B PUP, TNT OD, SQUARIFY, HVD-PBJ-PPD, VOB, Heavy Combo Toggles, Proximity GZI HV. Per-indicator versioning + CHANGELOG. |
| **realtime-indicators** | private | 2026-05-20 | Pine -> Python real-time engine fed by Massive WebSocket. Companion to indicators repo. |
| **anish-instructions** | private | 2026-05-25 | (Personal instructions/config) |
| **Google-Studio** | private | 2026-05-22 | Volume Order Flow research. |
| **alphaomega1** | public | 2026-05-21 | (Working title project) |
| **setup-library** | private | 2026-05-06 | Setup playbooks. |

### Forked Repos on nishpa800

| Repo | Source | Last Push | Notes |
|---|---|---|---|
| **datafusion** | apache/datafusion | 2026-05-26 | Fork of Apache DataFusion — actively pushed TODAY |
| **client-python** | massive-com/client-python | 2026-05-26 | Fork — actively pushed TODAY |
| **client-go** | massive-com/client-go | 2026-05-26 | Fork — actively pushed TODAY |
| **community** | massive-com/community | 2026-05-20 | Fork |
| **client-js** | massive-com/client-js | 2026-05-08 | Fork |
| **mcp_massive** | massive-com/mcp_massive | 2026-05-05 | Fork |
| **vortex** | vortex-data/vortex | 2026-05-08 | Columnar file format (Linux Foundation) |
| **errands-server** | massive-com/errands-server | 2025-11-07 | HTTP job queue |
| **xbrl-parser** | massive-com/xbrl-parser | 2025-11-06 | XBRL document parser |
| **errands-js** | massive-com/errands-js | 2025-11-06 | Errands JS client |
| **go-multicast-dump** | massive-com/go-multicast-dump | 2025-11-06 | Multicast dump tool |
| **indicator** | cinar/indicator | 2025-11-06 | Go TA library |
| **go-app-ticker-wall** | massive-com/go-app-ticker-wall | 2025-11-06 | Ticker tape display |
| **nanovgo** | massive-com/nanovgo | 2025-11-06 | OpenGL rendering |
| **puppet-k8s** | voxpupuli/puppet-k8s | 2025-10-08 | K8s Puppet module |
| **arrow-rs-object-store** | apache/arrow-rs-object-store | 2025-09-22 | Rust object store |
| **datafusion-postgres** | massive-com/datafusion-postgres | 2025-09-08 | Postgres frontend for DataFusion |
| **pg_catalog** | massive-com/pg_catalog | 2025-08-26 | Postgres compat layer |
| **corr-subq-udf-rs** | ybrs/corr-subq-udf-rs | 2025-08-26 | Subquery-to-UDF rewriter |
| **arrow-rs** | apache/arrow-rs | 2024-03-11 | Rust Arrow |
| **aws-sdk-go-v2** | aws/aws-sdk-go-v2 | 2024-02-01 | AWS Go SDK |
| **arrow** | apache/arrow | 2023-04-13 | Multi-lang Arrow |
| **parquet-go** | segmentio/parquet-go | 2023-04-03 | Go Parquet lib |

---

## PART 6: Key Findings & Recommendations

### What We Have That Matters Most

1. **Complete Massive SDK coverage** in 4 languages (Python primary, Go for performance, JS for dashboards, JVM for schema reference)
2. **Working MCP bridge** (`mcp_massive`) with 3 tools + 14 apply= functions already installed
3. **Confirmed NOI pattern** — `client.subscribe("NOI.*")` on `Market.Stocks`, `Feed.RealTime`
4. **Dark-pool detection** — `exchange == 4 && trf_id in {201,202,203}`
5. **17 community examples** with battle-tested patterns for every major data surface
6. **DataFusion stack** (arrow-datafusion + S3 objectstore + postgres frontend + materialized views) — a complete analytical SQL engine for querying our flat files

### Schema Sources Ranked by Completeness

1. **client-jvm** — 361 model classes (most complete)
2. **client-js** — 487 interfaces + `openapi.json` (canonical spec)
3. **client-go** — 145 methods + 19 WS model structs
4. **client-python** — 76 methods + full data class inventory

### Gaps to Fill

- No async Python REST (need httpx wrapper or threadpool)
- No rate limiter (need token-bucket for 429-heavy paths)
- No S3 flat-file client in any SDK (need boto3)
- No response caching (need Redis/disk layer)
- No pipeline for fractional-share decimal migration (flat files broke 2026-02-23)
- Filings endpoints (BETA) need probing to confirm access
- Consumer-spending endpoints need probing to confirm access

### DataFusion Stack Potential

The `arrow-datafusion` + `datafusion-objectstore-s3` + `datafusion-postgres` + `datafusion-materialized-views` combination could serve as our analytical query layer:
- Query Massive S3 flat files (Parquet) directly without downloading
- Expose via Postgres wire protocol (any BI tool connects)
- Materialized views with incremental maintenance over Hive-partitioned data
- `pg_catalog` enables tool compatibility
- `vortex` (100x faster than Parquet) as future format upgrade path
