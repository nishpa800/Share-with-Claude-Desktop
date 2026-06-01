# QUANTITATIVE RESEARCH SYSTEM — WORK BREAKDOWN STRUCTURE
## Consulting-Style Project Plan · Every Task = A Skill · Five Pillars Applied to Each

**Project:** Autonomous Quantitative Research & Indicator Optimization System
**Client:** Anish Patel
**Governing Doctrine:** Five Pillars Operating System v1.0
**Date:** 2026-05-26
**Status:** Phase 0 — Reconnaissance (in progress)

---

## WBS NUMBERING CONVENTION

- **X.0** = Phase statement (what this phase achieves)
- **X.Y** = Skill (distinct unit of work, gets its own skill folder + Five Pillars treatment)
- **X.Y.Z** = Sub-skill (component within a skill, documented inside parent skill)
- **[SKILL]** = Requires dedicated skill file in /quant-brain/skills/
- **[ROUTINE]** = Requires recurring scheduled execution
- **[ARTIFACT]** = Produces a deliverable document or dataset
- **[HANDOFF]** = Defines interface between skills (inputs/outputs contract)

Each **[SKILL]** must contain:
1. Five Pillars compliance proof (all 5 pillars addressed with evidence)
2. Problem statement (formal, with equation of knowns/unknowns)
3. System definition (parts, inputs, outputs, processing, communication)
4. Reference ranges (what good/bad/critical looks like for every parameter)
5. Inversion analysis (how this skill fails)
6. Pre-mortem (assuming failure, trace back to causes)
7. Acceptance criteria (how to prove this skill achieved its goal)
8. Handoff spec (what it receives from upstream, what it delivers downstream)
9. Monitoring/observability (how to tell if something is wrong — 2σ, 3σ thresholds)
10. Pearls and pitfalls (hard-won lessons, gotchas, edge cases)

---

## PHASE 0: RECONNAISSANCE & INVENTORY
### 0.0 Phase Statement
Achieve complete knowledge of every data source, every field, every delivery method, every client library, every piece of documentation, every tutorial, every blog post, every use case, every API status, every product subscription, every hardware resource, and every indicator in the suite. No code. Only knowledge. The output is a verified inventory that Anish can review and say "yes, that's everything" or "you missed X."

**WHY THIS IS FIRST:** Per Pillar I (Problem Crystallization), you cannot define variables, equations, knowns/unknowns, or solve for anything if you haven't inventoried what exists. Per Pillar II (Leverage Points), Level 7 — Information Flows — is the highest-leverage intervention. Anish cannot see what he has. This phase makes it visible.

### 0.1 — Massive.com Stocks Data Inventory [SKILL] [ARTIFACT]
- **What:** Complete schema documentation of all stocks-related endpoints, fields, types, parameters
- **Covers:** Aggregates (bars), trades, quotes, snapshots, ticker details, conditions, exchanges, OHLCV, extended hours vs regular hours, pre/post market
- **Delivery methods:** REST endpoints, WebSocket feeds, S3 flat files
- **Must document:** Every column name, data type, example value, whether nullable, timestamp precision (nanosecond), normalization rules
- **Must answer:** Do we get extended hours? Regular only? Both? How are they flagged? What's the historical depth? What resolution (tick, second, minute, hour, day)? Can we reconstitute from ticks?
- **Five Pillars required:** Full treatment
- **Depends on:** Nothing (entry point)
- **Feeds:** 1.1, 2.1, 3.1

### 0.2 — Massive.com Options Data Inventory [SKILL] [ARTIFACT]
- **What:** Complete schema documentation of all options-related endpoints
- **Covers:** Options contracts, chains, trades, quotes, snapshots, open interest, Greeks (if provided), expirations, strikes, underlying mapping
- **Delivery methods:** REST endpoints, WebSocket feeds, S3 flat files
- **Must document:** Every field, type, example value. Contract symbology. How Greeks are calculated (Black-Scholes? Which model?). Whether they provide implied volatility. Historical depth for options chains.
- **Must answer:** What Greeks are provided vs what we calculate ourselves? How are expirations organized? What's the latency on options quotes? Are we getting OPRA feed or consolidated?
- **Five Pillars required:** Full treatment
- **Depends on:** Nothing
- **Feeds:** 1.2, 2.2, 3.2

### 0.3 — Massive.com Benzinga News Inventory [SKILL] [ARTIFACT]
- **What:** Complete schema documentation of Benzinga News feed
- **Covers:** Articles, topics/categories, tickers mentioned, sentiment scores (if any), timestamps, authors, sources, content types
- **Delivery methods:** REST, WebSocket (if available for real-time news)
- **Must document:** Every field. How articles are categorized. How ticker associations work. Whether sentiment is pre-computed or we compute it. Historical depth. Update frequency.
- **Must answer:** Is there real-time streaming for breaking news? How are tickers extracted/tagged? What's the taxonomy of news categories? Is the full article text available or just headlines?
- **Five Pillars required:** Full treatment
- **Depends on:** Nothing
- **Feeds:** 1.3, 2.3

### 0.4 — Massive.com Benzinga Earnings Inventory [SKILL] [ARTIFACT]
- **What:** Complete schema documentation of Benzinga Earnings feed
- **Covers:** Earnings estimates, actuals, surprises, EPS, revenue, calendar dates, reporting times (BMO/AMC), fiscal periods, analyst counts, revision history
- **Delivery methods:** REST, flat files
- **Must document:** Every field. Point-in-time nature (are estimates as-of a date, or revised?). How surprises are calculated. Historical depth. Whether we get revision history or just latest.
- **Must answer:** Is this point-in-time data (critical for backtesting — no lookahead bias)? How far in advance do we get earnings dates? Do we get whisper numbers? Conference call data?
- **Five Pillars required:** Full treatment
- **Depends on:** Nothing
- **Feeds:** 1.4, 2.4

### 0.5 — Massive.com ETF Subscription 1 Inventory [SKILL] [ARTIFACT]
- **What:** Complete schema of first ETF data subscription
- **Covers:** Holdings, weights, sector allocation, flows (inflows/outflows), AUM, NAV, premium/discount, creation/redemption, rebalance dates
- **Must document:** Every field. Frequency of holdings updates. Whether flows are daily/weekly. Historical depth.
- **Must answer:** Which ETFs are covered? Is it all US ETFs or a subset? How current are holdings (T+1? T+30?)? Do we get creation/redemption basket data?
- **Five Pillars required:** Full treatment
- **Depends on:** Nothing
- **Feeds:** 1.5, 2.5

### 0.6 — Massive.com ETF Subscription 2 Inventory [SKILL] [ARTIFACT]
- **What:** Complete schema of second ETF data subscription (likely ETF Global or similar)
- **Covers:** May differ from 0.5 — could be analytics, ratings, or different data provider
- **Must document:** Everything. How it differs from subscription 1. Whether there's overlap or complementary data.
- **Five Pillars required:** Full treatment
- **Depends on:** 0.5 (to compare/contrast)
- **Feeds:** 1.6, 2.6

### 0.7 — Massive.com NYSE Order Imbalance (NOI) Inventory [SKILL] [ARTIFACT]
- **What:** Complete schema of NYSE Order Imbalance data
- **Covers:** Regulatory imbalance messages, informational imbalances, paired quantity, imbalance quantity, reference price, far price, near price, current price, imbalance side, auction type (open, close, halt, IPO)
- **Delivery methods:** REST (historical), WebSocket (real-time), flat files
- **Must document:** Every field. Timing of messages (when during the day are imbalances published?). How the WebSocket feed works. Message frequency. Symbol coverage.
- **Must answer:** Do we get both opening and closing auction imbalances? How early before open/close do imbalances start publishing? What's the message rate at peak? How does the WebSocket NOI tracker work (per Massive's recent blog post)?
- **Five Pillars required:** Full treatment
- **Depends on:** Nothing
- **Feeds:** 1.7, 2.7, 9.5

### 0.8 — Massive.com WebSocket Architecture Inventory [SKILL] [ARTIFACT]
- **What:** Complete documentation of ALL WebSocket feeds across all data types
- **Covers:** All feed hosts, all topics, all markets, connection protocol, authentication, heartbeat, reconnection, message format, throughput
- **Must document:** Every WebSocket topic. Message schemas. How to subscribe/unsubscribe. Backfill behavior on reconnect. All 18 feed hosts × 10 markets (per Go SDK docs).
- **Must answer:** What's the full list of real-time feeds? Stocks trades, stocks quotes, stocks aggregates, options trades, options quotes, NOI — what else? How do we handle connection drops? What's the message throughput at peak? Buffer requirements?
- **Five Pillars required:** Full treatment
- **Depends on:** 0.1, 0.2, 0.7
- **Feeds:** 1.8, 6.5

### 0.9 — Massive.com REST API Architecture Inventory [SKILL] [ARTIFACT]
- **What:** Complete documentation of REST API structure, authentication, pagination, rate limits, error handling
- **Covers:** Base URL, auth (Bearer token), pagination (next_url cursor), rate limits (per plan), response formats (JSON), error codes, retry strategy
- **Must document:** Rate limit thresholds. Pagination pattern. How to handle 429s. Backoff strategy. Request timeout best practices.
- **Five Pillars required:** Full treatment
- **Depends on:** Nothing
- **Feeds:** All Phase 1 REST skills

### 0.10 — Massive.com S3/Flat Files Architecture Inventory [SKILL] [ARTIFACT]
- **What:** Complete documentation of flat file access via S3
- **Covers:** S3 endpoint, bucket structure, file format (CSV? Parquet? Both?), partitioning scheme (by date? by ticker?), file naming convention, access credentials, download tooling
- **Must document:** Exact bucket paths for each data type. File sizes. Compression. Whether files are daily snapshots or rolling. How to determine what's new since last download.
- **Must answer:** Can we use aws s3 sync for incremental downloads? What's the total data size per product? Is it Parquet (preferred) or CSV? Are there manifest files listing available data?
- **Five Pillars required:** Full treatment
- **Depends on:** Nothing
- **Feeds:** All Phase 1 flat file skills

### 0.11 — Massive.com Client Libraries Inventory [SKILL] [ARTIFACT]
- **What:** Comparative documentation of all four client SDKs
- **Covers:** Python, JavaScript, Go, Java/Kotlin
- **Must document per library:**
  - All available methods (every function/method name)
  - Authentication pattern
  - Pagination handling
  - Error handling / retry logic
  - WebSocket support
  - Async support
  - Latest version and breaking changes
  - Installation and setup
- **Must answer:** Which library is best for our use case (Python for data science, Go for performance)? Are they auto-generated from OpenAPI spec? Are there known bugs or limitations?
- **Five Pillars required:** Full treatment
- **Depends on:** Nothing
- **Feeds:** Phase 1 implementation decisions

### 0.12 — Massive.com Tutorials, Examples & Use Cases Inventory [SKILL] [ARTIFACT]
- **What:** Every tutorial, example, blog post, and use case from Massive
- **Covers:**
  - Community repo examples (13 REST + 4 WebSocket confirmed)
  - Blog post tutorials (NYSE OI tracker, dark pool scanner, etc.)
  - Knowledge base articles
  - Getting started guides
  - The confirmed NOI WebSocket pattern
  - New /stocks/filings and /consumer-spending/eu surfaces
  - 2026-02-23 schema-breaking decimal-size change
- **Must document:** Each example with: what it does, what API endpoints it uses, what data it consumes, what patterns it demonstrates, how we adapt it
- **Five Pillars required:** Abbreviated (Pillars I, II only)
- **Depends on:** Nothing
- **Feeds:** All skills (reference material)

### 0.13 — Massive.com API Status & Infrastructure Inventory [SKILL] [ARTIFACT]
- **What:** Current API health, infrastructure architecture, data quality guarantees
- **Covers:**
  - Current API status page
  - Two fully isolated networks for redundancy
  - HA streaming messaging system
  - Nanosecond-precision proprietary database
  - Data normalization methodology
  - Multi-layer redundancy and backup
  - SQL interface status (not yet available — tracking for when it launches)
- **Must document:** How they ensure uptime. What happens during outages. SLA if available. How to monitor for degradation.
- **Five Pillars required:** Abbreviated (Pillars I, II only)
- **Depends on:** Nothing
- **Feeds:** 8.6

### 0.14 — Massive.com Reference Data Inventory [SKILL] [ARTIFACT]
- **What:** All reference/metadata endpoints
- **Covers:** Ticker details, market status, exchanges, conditions, ticker types, splits, dividends, financials, market holidays, ticker news, related companies
- **Must document:** Every field. How reference data links to market data (foreign keys). Update frequency.
- **Five Pillars required:** Full treatment
- **Depends on:** Nothing
- **Feeds:** 2.9 (symbol normalization), 2.10 (corporate actions)

### 0.15 — WhaleWisdom API Inventory [SKILL] [ARTIFACT]
- **What:** Complete schema documentation of WhaleWisdom API
- **Covers:** 13F filings, Schedule 13F holdings, insider trading (Form 4), fund managers, AUM, filer groups, Insider Backtester, ownership changes
- **Delivery methods:** REST API (command.json endpoint with shared_key + secret_key)
- **Must document:** Every API command. Every field returned. Authentication pattern. Rate limits. Historical depth. Filing dates and delay (13F filings are 45 days delayed by regulation).
- **Must answer:** What's the complete command set? How do we get holdings changes quarter-over-quarter? Can we track specific funds? What's the insider transaction taxonomy?
- **Five Pillars required:** Full treatment
- **Depends on:** Nothing
- **Feeds:** 1.13, 1.14, 2.7

### 0.16 — TradingView Pine Indicator Suite Inventory [SKILL] [ARTIFACT]
- **What:** Complete documentation of every Pine indicator Anish uses
- **Covers:** Every indicator by name and S-number:
  - B2B PUP
  - TNT OD
  - SQUARIFY
  - HVD-PBJ-PPD
  - VOB (Volume Order Block)
  - Heavy Combo Toggles (HCT)
  - Proximity GZI HV
  - Napalm (NPM)
  - SUPER
  - SDUPER
  - UC
  - GOLF
  - WBUSH
  - WMD
  - Alpha Strike
  - (and any others discovered via TradingView MCP)
- **Must document per indicator:**
  - Full name and S-number
  - Pine Script version
  - Every input parameter (name, type, default value, valid range)
  - Every output signal/plot (name, type, what it represents)
  - What data it consumes (OHLCV? volume? other indicators?)
  - Visual elements (lines, labels, boxes, tables, colors)
  - Dependencies on other indicators
  - The trading logic it implements (what setup does it detect?)
- **Must answer:** What is the complete indicator dependency graph? Which indicators feed into others? What's the canonical version of each? Which are deprecated?
- **Five Pillars required:** Full treatment (especially Pillar III — cryptanalytic pattern extraction of what each indicator is detecting)
- **Depends on:** TradingView MCP connection
- **Feeds:** Phase 4 (translation), Phase 5 (parity), Phase 9 (pattern detection)

### 0.17 — Hardware & Storage Inventory [SKILL] [ARTIFACT]
- **What:** Complete inventory of all storage and compute resources
- **Covers:**
  - Mac specifications (CPU, RAM, OS version)
  - OWC 8-bay enclosure (~180 TB) — mount point, partitions, free space, RAID config
  - 4 TB external drive — mount point, current usage, free space
  - Google Cloud storage (ultra plan) — capacity, sync settings, what's stored there
  - Local SSD — capacity, free space
- **Must document:** Where each type of data should go. Read/write speeds. Sync behavior (Google Drive sync — the danger of crashing if we dump data into a synced folder). Backup strategy.
- **Must answer:** Where does DuckDB live? Where do raw flat files go? Where do experiment results go? What's the total ingest budget in TB? What's the Google Drive sync risk?
- **Five Pillars required:** Abbreviated (Pillars I, II)
- **Depends on:** Nothing
- **Feeds:** 3.7 (storage management skill)

### 0.18 — GitHub Repository Inventory [SKILL] [ARTIFACT]
- **What:** Complete inventory of all repos Anish has forked/cloned
- **Covers:**
  - All repos in ~/code/massive-com/ (35+ repos)
  - All repos on nishpa800 GitHub
  - All repos in ~/code/anish/ (quant-brain and other projects)
- **Must document:** For each repo: what it is, language, last updated, relevance to our system, useful code patterns
- **Five Pillars required:** Abbreviated (Pillar I only — inventory)
- **Depends on:** Nothing
- **Feeds:** Phase 1 implementation decisions

### 0.19 — Massive.com Product Subscription Verification [SKILL] [ARTIFACT]
- **What:** Verify exactly which subscriptions are active, what tier, what's included
- **Covers:** Cross-reference account access against product pages. Confirm which endpoints return data vs 403/401. Identify any subscriptions we DON'T have that we should.
- **Five Pillars required:** Abbreviated (Pillar I)
- **Depends on:** 0.1 through 0.14
- **Feeds:** All downstream phases

---

## PHASE 1: DATA INGESTION
### 1.0 Phase Statement
Build per-source ingestion jobs that pull raw data exactly as-is into local staging storage. No transformation. Preserve everything. Schema validation on every run. Each source gets its own independent ingestion skill because each source has different endpoints, schemas, delivery methods, rate limits, and failure modes.

### 1.1 — Stocks REST API Ingestion [SKILL] [ROUTINE]
- **What:** Automated ingestion of all stocks data via REST API
- **Sub-skills:**
  - 1.1.1 Historical aggregates (bars) backfill — all symbols, all resolutions, full history
  - 1.1.2 Daily incremental aggregates update
  - 1.1.3 Trades data ingestion (tick-level)
  - 1.1.4 Quotes data ingestion (NBBO)
  - 1.1.5 Snapshots ingestion (current state)
  - 1.1.6 Ticker details / reference data sync
- **Output:** Raw Parquet files in staging, organized by date/symbol
- **Monitoring:** Row counts vs expected, schema validation, latency tracking
- **Routine:** Daily at 7:30 AM CT (1 hour before market open)
- **Five Pillars required:** Full treatment

### 1.2 — Stocks S3/Flat File Ingestion [SKILL] [ROUTINE]
- **What:** Bulk download of historical stocks data from S3 flat files
- **Why separate from 1.1:** Flat files are the most efficient way to backfill large historical datasets. REST is for incremental updates. Different skill, different tooling, different failure modes.
- **Output:** Raw files in local staging
- **Routine:** Weekly full sync, daily incremental check

### 1.3 — Options REST API Ingestion [SKILL] [ROUTINE]
- **What:** Automated ingestion of all options data
- **Sub-skills:**
  - 1.3.1 Options contracts reference data
  - 1.3.2 Options chain snapshots (per underlying, per expiry)
  - 1.3.3 Options trades (tick-level)
  - 1.3.4 Options quotes (NBBO)
  - 1.3.5 Open interest historical
  - 1.3.6 Options aggregates (bars)
- **Output:** Raw Parquet files
- **Routine:** Daily

### 1.4 — Options S3/Flat File Ingestion [SKILL] [ROUTINE]
- **What:** Bulk historical options data from flat files
- **Routine:** Weekly full sync

### 1.5 — Benzinga News Ingestion [SKILL] [ROUTINE]
- **What:** Automated ingestion of news articles
- **Sub-skills:**
  - 1.5.1 Historical news backfill
  - 1.5.2 Real-time news polling (or WebSocket if available)
  - 1.5.3 Topic/category mapping
  - 1.5.4 Ticker-article association mapping
- **Output:** Raw JSON → Parquet
- **Routine:** Every 15 minutes during market hours, hourly off-hours

### 1.6 — Benzinga Earnings Ingestion [SKILL] [ROUTINE]
- **What:** Automated ingestion of earnings data (point-in-time)
- **Sub-skills:**
  - 1.6.1 Earnings calendar ingestion
  - 1.6.2 Earnings estimates (as-of date preservation for PIT)
  - 1.6.3 Earnings actuals and surprises
  - 1.6.4 Historical estimates revision chain
- **Critical:** Point-in-time preservation — must store what was KNOWN at each date, not just latest
- **Output:** Raw Parquet with as-of timestamps
- **Routine:** Daily, with intraday updates during earnings season

### 1.7 — ETF Data Ingestion (Sub 1) [SKILL] [ROUTINE]
- **What:** Automated ingestion of first ETF subscription
- **Sub-skills depend on 0.5 inventory results**
- **Routine:** Daily

### 1.8 — ETF Data Ingestion (Sub 2) [SKILL] [ROUTINE]
- **What:** Automated ingestion of second ETF subscription
- **Routine:** Daily

### 1.9 — NYSE Order Imbalance REST Ingestion [SKILL] [ROUTINE]
- **What:** Historical NOI data via REST
- **Output:** Raw Parquet
- **Routine:** Daily after close

### 1.10 — NYSE Order Imbalance WebSocket Ingestion [SKILL] [ROUTINE]
- **What:** Real-time NOI streaming via WebSocket
- **Sub-skills:**
  - 1.10.1 WebSocket connection management (auth, heartbeat, reconnection)
  - 1.10.2 Message parsing and local buffering
  - 1.10.3 Append-only storage (no overwriting — every message preserved)
  - 1.10.4 Connection health monitoring
- **Critical:** Must run continuously during market hours. Must handle disconnections gracefully. Must not lose messages.
- **Output:** Append-only Parquet partitioned by date
- **Routine:** Always-on during market hours (9:00 AM - 4:00 PM ET, with pre-open starting 8:00 AM ET)

### 1.11 — Real-Time WebSocket Streaming Infrastructure [SKILL]
- **What:** Shared infrastructure for all WebSocket connections
- **Covers:** Connection pooling, authentication, heartbeat management, automatic reconnection with exponential backoff, message routing, backpressure handling, logging
- **Why separate skill:** This is the plumbing that 1.10 and any other real-time feed sits on top of. Different unit of work from the per-source ingestion.
- **Five Pillars required:** Full treatment (especially Pillar V — game theory of connection management under adversarial network conditions)

### 1.12 — Dark Pool Data Ingestion [SKILL] [ROUTINE]
- **What:** Ingestion of dark pool / off-exchange trade data
- **Depends on:** 0.1 to determine if dark pool data is a separate endpoint or filtered from trades
- **Routine:** Daily or real-time depending on delivery method

### 1.13 — WhaleWisdom 13F Ingestion [SKILL] [ROUTINE]
- **What:** Automated ingestion of 13F institutional holdings
- **Sub-skills:**
  - 1.13.1 Filing list retrieval (new filings since last check)
  - 1.13.2 Holdings detail retrieval per filing
  - 1.13.3 Quarter-over-quarter change calculation
  - 1.13.4 Fund manager metadata
- **Output:** Raw JSON → Parquet
- **Routine:** Daily check for new filings (filings arrive on rolling basis, 45 days after quarter end)

### 1.14 — WhaleWisdom Insider/Form 4 Ingestion [SKILL] [ROUTINE]
- **What:** Automated ingestion of insider transactions
- **Sub-skills:**
  - 1.14.1 Insider transaction feed
  - 1.14.2 Insider Backtester data (if API supports)
- **Output:** Raw Parquet
- **Routine:** Daily

### 1.15 — Schema Validation & Drift Detection [SKILL] [ROUTINE]
- **What:** Automated validation that every ingestion run matches expected schema
- **Covers:** Column names, data types, nullable/non-nullable, value ranges, timestamp precision
- **How it detects drift:** Compare today's schema hash against stored baseline. Alert on any mismatch. Log the specific diff.
- **Reference ranges:** For each field type: expected row count range (mean ± 3σ from last 7 days), expected null rate, expected value distribution
- **Output:** Validation report per ingestion run; alert on drift
- **Routine:** Runs as part of every ingestion job (post-hook)

### 1.16 — Ingestion Monitoring & Alerting [SKILL] [ROUTINE]
- **What:** Heartbeat and health monitoring for all ingestion jobs
- **Covers:**
  - Did each job run on schedule?
  - Did it complete successfully?
  - Row counts: within expected range (mean ± 2σ, flag at ± 3σ)?
  - Latency: is data arriving when expected?
  - Completeness: are all expected symbols present?
- **Thresholds:**
  - WARNING: > 2σ deviation from 7-day mean
  - CRITICAL: > 3σ deviation, or job failed, or no data for > 1 hour during market hours
- **Output:** Dashboard + alerting
- **Routine:** Continuous monitoring, alert immediately on CRITICAL

---

## PHASE 2: DATA CLEANING & NORMALIZATION
### 2.0 Phase Statement
Transform raw ingested data into clean, typed, deduplicated, timezone-normalized data. Each source has its own cleaning rules because each source has different data quality issues, formats, and semantics. Cleaning is SEPARATE from harmonization (Phase 3) — here we fix each source's individual problems; in Phase 3 we align them with each other.

### 2.1 — Stocks Data Cleaning [SKILL]
- **Input:** Raw stocks Parquet from Phase 1
- **Operations:** Type casting, timezone normalization (all to UTC with market-hours flag), deduplication, gap detection (missing bars), outlier flagging (not removal — flag for review), split/dividend adjustment awareness
- **Output:** Clean stocks Parquet
- **Reference ranges:** Expected OHLCV distributions per symbol; flag >5σ moves for review

### 2.2 — Options Data Cleaning [SKILL]
- **Input:** Raw options Parquet
- **Operations:** Contract symbol normalization (OCC format), expiry validation, strike sanity checks, Greek bounds checking, deduplication, timezone
- **Output:** Clean options Parquet

### 2.3 — Benzinga News Text Normalization [SKILL]
- **Input:** Raw news JSON/Parquet
- **Operations:** HTML stripping, encoding normalization (UTF-8), ticker extraction validation, category mapping, deduplication (same article from multiple feeds), timestamp normalization
- **Output:** Clean news Parquet
- **Note:** This is TEXT data — completely different cleaning rules from numeric OHLCV data. Different skill, different expertise.

### 2.4 — Benzinga Earnings Normalization [SKILL]
- **Input:** Raw earnings Parquet
- **Operations:** Point-in-time validation (no future data leaking into past records), EPS/revenue unit normalization, fiscal period alignment, surprise calculation validation
- **Output:** Clean earnings Parquet with verified PIT integrity
- **Critical:** Any PIT violation makes backtesting meaningless. This skill must PROVE no lookahead bias.

### 2.5 — ETF Data Normalization [SKILL]
- **Input:** Raw ETF Parquet (both subscriptions)
- **Operations:** Holdings weight normalization (sum to 100%?), ticker standardization, flow sign convention, NAV/price alignment, date normalization
- **Output:** Clean ETF Parquet

### 2.6 — NYSE Order Imbalance Normalization [SKILL]
- **Input:** Raw NOI Parquet
- **Operations:** Message type classification, imbalance side normalization, price field validation, auction type categorization, duplicate message handling
- **Output:** Clean NOI Parquet

### 2.7 — WhaleWisdom Data Normalization [SKILL]
- **Input:** Raw WhaleWisdom Parquet
- **Operations:** Filing date validation (45-day delay rule), CUSIP/ticker mapping, share count normalization, value calculation validation, position change classification (new/increased/decreased/sold)
- **Output:** Clean WhaleWisdom Parquet

### 2.8 — Timestamp Normalization [SKILL]
- **What:** Universal timestamp handling across all sources
- **Covers:** Nanosecond precision preservation, UTC conversion, market-hours flagging (pre-market, regular, post-market, closed), timezone-aware storage
- **Why separate skill:** Timestamp handling is a cross-cutting concern that affects every source. Getting it wrong corrupts everything downstream. The rules are the same but the source formats differ.

### 2.9 — Symbol/Ticker Normalization [SKILL]
- **What:** Universal ticker standardization
- **Covers:** Map all ticker representations to a canonical form. Handle class shares (BRK.A vs BRK-A vs BRKA). Handle name changes. Handle delistings. Handle options symbols (OCC symbology).
- **Must use:** Massive reference data (from 0.14) as the authoritative source

### 2.10 — Corporate Actions Adjustment [SKILL]
- **What:** Split and dividend adjustment for historical data
- **Covers:** Stock splits (forward/reverse), special dividends, spin-offs, mergers
- **Why separate skill:** Getting this wrong makes all historical analysis meaningless. It requires reference data (splits, dividends) cross-referenced with price history. Different unit of work from cleaning.

### 2.11 — Data Quality Scoring [SKILL] [ROUTINE]
- **What:** Assign a quality score to every dataset after cleaning
- **Covers:** Completeness (% of expected records present), accuracy (% passing validation rules), timeliness (delay from source to local), consistency (cross-source agreement)
- **Output:** Quality scorecard per dataset per day
- **Reference ranges:** Define "good" (>95% completeness, <1s latency), "acceptable" (>90%, <5s), "degraded" (<90%, >5s), "failed" (<80% or missing)
- **Routine:** Runs after every cleaning job

---

## PHASE 3: UNIFIED ANALYTICAL LAYER (DuckDB + Polars + PyArrow)
### 3.0 Phase Statement
Load clean data into DuckDB with a schema designed for the queries we need to run. Cross-source foreign keys. Materialized views. Partitioning. Query-ready for experiments. This is where all sources become queryable together.

### 3.1 — DuckDB Schema Design [SKILL] [ARTIFACT]
- **What:** Design the complete database schema
- **Must define:** Every table, every column, every type, every index, every constraint, every foreign key
- **Must justify:** Why each table is structured the way it is. What queries it optimizes for. What tradeoffs were made.
- **Five Pillars required:** Full treatment (especially Pillar I — the schema IS the formal representation of the problem)

### 3.2 — Polars/PyArrow Integration [SKILL]
- **What:** Define how data moves between DuckDB, Polars DataFrames, and PyArrow tables
- **Covers:** Zero-copy interop where possible. Memory management. Lazy vs eager evaluation. When to use which tool.

### 3.3 — Cross-Source Foreign Key Mapping [SKILL]
- **What:** Define how data from different sources links together
- **Covers:** Ticker as the primary join key. Timestamp alignment (different sources have different latencies). How to join earnings dates with price data. How to join 13F filings with price data (accounting for 45-day delay). How to join NOI with price action.

### 3.4 — Materialized Views Design [SKILL]
- **What:** Pre-computed views for common analysis patterns
- **Covers:** Daily OHLCV with earnings flags. Options chain snapshots with Greeks. NOI summary by symbol/date. Holdings changes quarter-over-quarter.

### 3.5 — Partitioning Strategy [SKILL]
- **What:** How data is physically organized on disk
- **Covers:** Partition by date for fast range scans. Partition by symbol for single-stock analysis. Hybrid partitioning for common query patterns.

### 3.6 — Query Optimization [SKILL]
- **What:** Ensure common queries run fast enough for interactive analysis and batch experiments
- **Covers:** Index selection. Statistics maintenance. Query plan analysis. Memory budgeting.

### 3.7 — Storage Management [SKILL]
- **What:** Where each type of data physically lives and why
- **Covers:**
  - Raw staging → 4TB external or OWC (bulk, write-once)
  - Clean data → OWC (frequently read)
  - DuckDB database file → local SSD (fast random access)
  - Experiment results → local SSD or OWC
  - Google Cloud → ONLY for backups, NOT for active data (sync risk)
- **Must address:** The Google Drive sync danger Anish identified. Never put actively-written data in a synced folder.

---

## PHASE 4: PINE SCRIPT TRANSLATION
### 4.0 Phase Statement
Translate every Pine indicator from Pine Script v5 to Python. This is TRANSLATION (different languages, same meaning), not replication. The translator must understand both languages deeply.

### 4.1 — Pine Script → Python Translation Methodology [SKILL] [ARTIFACT]
- **What:** Define the systematic approach for translating Pine Script to Python
- **Covers:**
  - Pine Script v5 syntax → Python equivalents
  - Pine's bar-by-bar execution model vs Python's vectorized model
  - Pine's built-in functions (ta.sma, ta.ema, ta.rsi, etc.) → Python implementations
  - Pine's series type → Pandas/Polars series
  - Pine's security() / request.security() → multi-timeframe in Python
  - Pine's plot/label/line/box/table → Python output format
  - How to handle Pine's na values
  - How to handle Pine's history referencing (close[1], close[2])
- **Five Pillars required:** Full treatment (especially Pillar III — the translation IS a decoding problem)

### 4.2 — Per-Indicator Translation Skills [SKILL per indicator]
Each indicator gets its own skill file:
- 4.2.1 B2B PUP translation [SKILL]
- 4.2.2 TNT OD translation [SKILL]
- 4.2.3 SQUARIFY translation [SKILL]
- 4.2.4 HVD-PBJ-PPD translation [SKILL]
- 4.2.5 VOB (Volume Order Block) translation [SKILL]
- 4.2.6 Heavy Combo Toggles (HCT) translation [SKILL]
- 4.2.7 Proximity GZI HV translation [SKILL]
- 4.2.8 Napalm (NPM) translation [SKILL]
- 4.2.9 SUPER translation [SKILL]
- 4.2.10 SDUPER translation [SKILL]
- 4.2.11 UC translation [SKILL]
- 4.2.12 GOLF translation [SKILL]
- 4.2.13 WBUSH translation [SKILL]
- 4.2.14 WMD translation [SKILL]
- 4.2.15 Alpha Strike translation [SKILL]
- (additional indicators discovered in 0.16)

Each translation skill must document:
- The Pine source (exact version, line count, complexity assessment)
- The Python output (vectorized implementation)
- Every input parameter mapped
- Every output signal mapped
- Edge cases and Pine-specific behavior that requires special handling

---

## PHASE 5: BAR-FOR-BAR PARITY VERIFICATION
### 5.0 Phase Statement
Prove that every translated Python indicator produces IDENTICAL output to the Pine Script original on the same input data. This is a completely different skill from translation — translation is about understanding two languages; parity is about measurement and proof.

### 5.1 — Parity Testing Methodology [SKILL] [ARTIFACT]
- **What:** Define how we prove bar-for-bar parity
- **Covers:**
  - How to extract ground truth from TradingView MCP (data_get_study_values, data_get_pine_lines, data_get_pine_labels, data_get_pine_tables, data_get_pine_boxes)
  - Tolerance definition (what counts as "identical" — exact match? < 0.01% error?)
  - Test data selection (which symbols, which date ranges, which market conditions)
  - Visual comparison methodology (overlay plots)
  - Statistical comparison (correlation, RMSE, max deviation)
  - Edge case coverage (market open, market close, gaps, halts, splits)
- **Five Pillars required:** Full treatment

### 5.2 — TradingView MCP Ground Truth Extraction [SKILL]
- **What:** Extract indicator values from TradingView for comparison
- **Covers:** Using chart_get_state, data_get_study_values, data_get_pine_lines/labels/tables/boxes with study_filter to get exact indicator outputs from the live chart
- **Why separate skill:** Extracting ground truth is its own technical challenge. The MCP has specific behaviors, limitations, and gotchas (indicators must be visible, some return 200KB+).

### 5.3 — Visual Parity Comparison [SKILL]
- **What:** Visual overlay of Pine output vs Python output
- **Covers:** Plot both on same chart. Flag bars where they diverge. Color-code by deviation magnitude.
- **Why separate skill:** Visual comparison catches things numerical comparison misses (plot timing, level placement, color/style meaning)

### 5.4 — Per-Indicator Parity Test Skills [SKILL per indicator]
- 5.4.1 through 5.4.15+ (one per indicator, matching 4.2.X numbering)
- Each must: extract TV values, run Python version on same data, compare, report full parity metrics

### 5.5 — Parity Regression Testing [SKILL] [ROUTINE]
- **What:** Automated re-verification after any change to translated Python code
- **Routine:** On every code change (CI-style)

---

## PHASE 6: EXPERIMENT ENGINE
### 6.0 Phase Statement
Build the always-on autonomous system that runs parameter optimization experiments 24/7 without human intervention. This is the system that does the actual work of finding better indicator configurations.

### 6.1 — Hypothesis Definition Framework [SKILL] [ARTIFACT]
- **What:** Formal structure for defining what an experiment tests
- **Covers:** PICO-equivalent for quant finance: Population (which symbols/timeframes), Intervention (which parameter change), Control (current/default parameters), Outcome (which Northstar metrics)
- **Five Pillars required:** Full treatment (especially Pillar IV — this IS the statistical modeling protocol)

### 6.2 — Parameter Sweep Methodology [SKILL]
- **What:** How parameters are systematically varied
- **Covers:**
  - Grid search (exhaustive, for small parameter spaces)
  - Bayesian optimization (for expensive-to-evaluate spaces)
  - Evolutionary/genetic algorithms (for complex multi-parameter interactions)
  - Random search (as a baseline)
  - Choosing which method for which indicator
- **Must define:** Stopping criteria (when have we searched enough — the logistic carrying capacity from E3)

### 6.3 — Walk-Forward Evaluation [SKILL]
- **What:** Time-series-aware validation that prevents lookahead bias
- **Covers:** Anchored walk-forward, rolling walk-forward, expanding window, purged k-fold for time series
- **Must prevent:** Any form of future information leaking into training/optimization

### 6.4 — Regime Detection & Stratification [SKILL]
- **What:** Identify market regimes and evaluate separately within each
- **Covers:** Bull, bear, choppy/range-bound, crisis/vol-spike, trending vs mean-reverting
- **Why separate skill:** An indicator that works in bull markets but fails in bear markets is a trap if you don't test regime-stratified. This is a specialized statistical/ML problem.

### 6.5 — Experiment Daemon (Always-On) [SKILL] [ROUTINE]
- **What:** The actual process that runs 24/7
- **Covers:**
  - Process management (Hermes cron, launchd, systemd — whichever is most reliable on macOS)
  - Experiment queue (pick next experiment to run)
  - Resource management (don't saturate CPU/disk)
  - Crash recovery (resume from where it left off)
  - Results persistence (every experiment result saved immediately)
  - Heartbeat (prove the daemon is alive)
- **Must survive:** Reboots, sleep/wake, network drops, disk full
- **Routine:** Always-on, 24/7

### 6.6 — Experiment Results Storage [SKILL]
- **What:** How experiment results are stored and queryable
- **Covers:** Every run: timestamp, indicator, parameters tested, data window, regime, all Northstar metrics, execution time, errors
- **Must support:** "Show me the top 10 parameter sets for VOB on SPY in bull regime" type queries

### 6.7 — Experiment Queue Management [SKILL]
- **What:** How experiments are prioritized and scheduled
- **Covers:** Priority based on expected information gain. Deduplication (don't re-run identical experiments). Dependency ordering. Load balancing.

---

## PHASE 7: SCORING & EVALUATION
### 7.0 Phase Statement
Evaluate every experiment against the full Northstar confusion-matrix surface. No single-metric shortcuts. Calibration mandatory. Out-of-sample only.

### 7.1 — Northstar Confusion Matrix Scoring [SKILL]
- **What:** Compute all Northstar metrics for any indicator output
- **Covers:** Sensitivity, Specificity, PPV, NPV, Accuracy, Balanced Accuracy, F1, Fβ, MCC, Cohen's Kappa, AUC-ROC, AUC-PR, Brier Score, Log Loss, ECE
- **Must report:** All metrics with confidence intervals (bootstrap). Never just one metric.

### 7.2 — Calibration-by-Intersection Protocol [SKILL]
- **What:** The Nexus-validated calibration protocol from §11.5.3 of Five Pillars
- **Covers:** n sequential backtest splits, per-fold critique rules, intersection across folds, held-out validation, acceptance threshold (≥5% improvement)
- **Five Pillars required:** Full treatment (this IS Pillar IV's Calibration Gauntlet made operational)

### 7.3 — Regime-Stratified Evaluation [SKILL]
- **What:** Evaluate performance separately per market regime
- **Depends on:** 6.4 (regime detection)
- **Must report:** Per-regime Northstar metrics. Flag any regime where performance < 2σ below overall.

### 7.4 — Out-of-Sample Validation [SKILL]
- **What:** Guarantee no data leakage in any evaluation
- **Covers:** Strict temporal separation. Purging. Embargo periods. Knowledge-cutoff-strict testing.

### 7.5 — Overfitting Detection [SKILL]
- **What:** Detect when optimization has found noise instead of signal
- **Covers:** Train/test gap analysis. Deflated Sharpe ratio (accounting for multiple comparisons). Combinatorial purged cross-validation.

### 7.6 — Reference Range Definition [SKILL] [ARTIFACT]
- **What:** Define what "good" looks like for each metric in each context
- **Covers:** Expected ranges for each Northstar metric by: indicator type, asset class, timeframe, regime. What's achievable vs what's fantasy.
- **Must produce:** A reference table that any other skill can query: "Is Sensitivity of 0.74 on this indicator in this regime good, acceptable, or degraded?"

---

## PHASE 8: MONITORING & OBSERVABILITY
### 8.0 Phase Statement
Know at all times whether every system is healthy. Detect problems before they corrupt data or waste experiments.

### 8.1 — Data Pipeline Health Monitoring [SKILL] [ROUTINE]
- **What:** Real-time health dashboard for all ingestion and cleaning jobs
- **Routine:** Continuous, with checks every 15 minutes during market hours

### 8.2 — Anomaly Detection for Data Quality [SKILL] [ROUTINE]
- **What:** Statistical anomaly detection on incoming data
- **Covers:** Compare today's data to trailing 7-day distribution. Flag at 2σ, alert at 3σ.
- **Routine:** Per ingestion run

### 8.3 — Dashboard Design [SKILL] [ARTIFACT]
- **What:** Visual dashboard Anish can review
- **Covers:** Pipeline status, data quality scores, experiment progress, top results

### 8.4 — Alerting [SKILL]
- **What:** How alerts are delivered and escalated
- **Covers:** What triggers an alert, how it's delivered (terminal notification? push?), escalation rules

### 8.5 — Massive.com Website Change Monitoring [SKILL] [ROUTINE]
- **What:** Daily automated check of Massive website for any changes
- **Covers:**
  - New blog posts
  - New tutorials or use cases
  - Documentation updates
  - API changelog entries
  - New product announcements
  - Schema changes
  - New endpoints
  - Client library updates (new versions)
  - Knowledge base updates
  - API status changes
- **Routine:** Daily at 7:00 AM CT (before market open)
- **Output:** Change report. If anything material changed, flag for review and update relevant skills.

### 8.6 — API Status & Health Monitoring [SKILL] [ROUTINE]
- **What:** Monitor Massive and WhaleWisdom API health
- **Routine:** Every 4 hours during market days, once on weekends

---

## PHASE 9: PATTERN DETECTION (Pillar III Application)
### 9.0 Phase Statement
Apply cryptanalytic pattern extraction to find hidden structure in the data that the indicators should detect.

### 9.1 — Cryptanalytic Pattern Extraction Framework [SKILL]
- **What:** Systematic application of Pillar III to market data
- **Five Pillars required:** Full treatment (this IS Pillar III)

### 9.2 — Volume Order Block Detection [SKILL]
- **What:** Detect the highest tensile volume order blocks that won't be broken
- **Relates to:** Anish's play — finding the VOB where price sits at the lowest point on the highest tensile VOB, with bearish structure transferring potential energy to bullish structure

### 9.3 — Structure Transfer Detection [SKILL]
- **What:** Detect when bearish structure is stuck on top of a VOB and transferring energy to bullish
- **Relates to:** The exponential/logarithmic energy play

### 9.4 — Dark Pool Signal Detection [SKILL]
- **What:** Extract signals from dark pool / off-exchange data
- **Depends on:** 1.12 (dark pool ingestion)

### 9.5 — Order Imbalance Signal Detection [SKILL]
- **What:** Extract predictive signals from NYSE order imbalance data
- **Depends on:** 1.9, 1.10 (NOI ingestion)

---

## PHASE 10: PLAYBOOK DEFINITION
### 10.0 Phase Statement
Formalize Anish's trading plays into structured, testable playbook entries.

### 10.1 — Trade Setup Taxonomy [SKILL] [ARTIFACT]
- **What:** Bloomberg-style taxonomy of all setup types
- **Covers:** Classification hierarchy: asset class → setup type → trigger → confirmation → entry → stop → target

### 10.2 — Playbook Formalization [SKILL] [ARTIFACT]
- **What:** Each play defined formally with Five Pillars treatment
- **The VOB play:** Price at lowest point on highest tensile VOB → bearish structure stuck on top → energy transfer → bullish breakout with exponential energy
- **Each play gets:** Variables, equations, measurable conditions, testable predictions

### 10.3 — Signal Confluence Detection [SKILL]
- **What:** Detect when multiple indicators/signals align (the "Holy Grail" VOB confluence)
- **Five Pillars required:** Full treatment (especially Pillar V — the Lollapalooza scan)

### 10.4 — Entry/Exit Criteria Formalization [SKILL]
- **What:** Precise, quantifiable entry and exit rules for each play

---

## CROSS-CUTTING SKILLS

### C.1 — Handoff Protocol [SKILL] [ARTIFACT]
- **What:** Standard interface contract between skills
- **Covers:** What each skill receives as input, what it produces as output, data format, validation checks at handoff points, error propagation

### C.2 — Routine Scheduling [SKILL]
- **What:** How recurring jobs are scheduled and managed
- **Covers:** Hermes cron, macOS launchd, or custom scheduler. Timezone handling (all times CT primary). Dependencies between routines. Failure recovery.

### C.3 — Hardware/Storage Allocation [SKILL]
- **What:** Rules for where data goes based on access pattern and size
- **Depends on:** 0.17

### C.4 — Google Cloud Integration (with sync safety) [SKILL]
- **What:** How to safely use Google Cloud storage without triggering destructive sync
- **Critical:** Google Drive sync can crash the system if large datasets are written to a synced folder. Must define safe zones.

### C.5 — GitHub Repository Management [SKILL]
- **What:** How code, configs, and artifacts are version controlled
- **Covers:** Repo structure, branching, commit conventions, what goes in git vs what doesn't (data files)

### C.6 — CLAUDE.md & Documentation Management [SKILL] [ROUTINE]
- **What:** Keep all documentation, wiki, CLAUDE.md files up to date
- **Routine:** Updated whenever any skill is created or modified

### C.7 — Five Pillars Compliance Verification [SKILL]
- **What:** Audit every skill to verify it properly addresses all Five Pillars
- **Covers:** Checklist per skill: Problem statement? Equations? Critical thinking? Inversion? Pre-mortem? Cryptanalytic analysis? Statistical modeling? Game theory? Northstar metrics?
- **Routine:** Run on every new or modified skill

---

## SKILL COUNT SUMMARY

| Phase | Skills | Routines |
|-------|--------|----------|
| 0: Reconnaissance | 19 | 0 |
| 1: Ingestion | 16 | 12 |
| 2: Cleaning | 11 | 1 |
| 3: Analytical Layer | 7 | 0 |
| 4: Translation | 16+ | 0 |
| 5: Parity | 5 + 15+ per indicator | 1 |
| 6: Experiments | 7 | 1 |
| 7: Scoring | 6 | 0 |
| 8: Monitoring | 6 | 5 |
| 9: Pattern Detection | 5 | 0 |
| 10: Playbook | 4 | 0 |
| Cross-cutting | 7 | 2 |
| **TOTAL** | **~109+ base + per-indicator** | **~22** |

---

## DEPENDENCY GRAPH (Phase Level)

```
Phase 0 (Recon)
    │
    ├──► Phase 1 (Ingestion) ──► Phase 2 (Cleaning) ──► Phase 3 (DuckDB Layer)
    │                                                          │
    │                                                          ├──► Phase 6 (Experiments)
    │                                                          │        │
    └──► Phase 4 (Translation) ──► Phase 5 (Parity) ──────────┘        │
                                                                        ▼
                                                               Phase 7 (Scoring)
                                                                        │
    Phase 8 (Monitoring) ◄────── runs alongside ALL phases ────────────►│
                                                                        │
    Phase 9 (Pattern Detection) ◄── requires Phase 3 + Phase 5 ────────┘
                                                                        │
                                                               Phase 10 (Playbook)
```

---

## NEXT IMMEDIATE ACTIONS

1. **Phase 0 recon agents are running NOW** — inventorying Massive API endpoints, crawling website, inventorying GitHub forks
2. **Next:** Write the first skill file (0.1 — Massive Stocks Data Inventory) with FULL Five Pillars treatment as the gold standard template
3. **Then:** Proceed through each 0.X skill, filling in actual data from recon agents
4. **Anish reviews:** Each completed recon skill before Phase 1 begins
