# SKILL: WhaleWisdom Data Ingestion
## Five Pillars Compliance: MANDATORY — All 5 Pillars Applied

**Skill ID:** WW-INGEST-001
**Status:** Phase 0 — Reconnaissance (in progress)
**Owner:** Autonomous agent (no human decisions required for execution)
**Governing Doctrine:** Five Pillars Operating System v1.0
**Created:** 2026-05-26
**Last Updated:** 2026-05-26

---

## LESSONS LEARNED (from Massive.com — applied here FIRST)

Before any work on this skill, we document what went wrong during the Massive.com
data ingestion effort and how this skill prevents repeating those failures.

### What went wrong with Massive.com (honest accounting)

1. **No problem statement was written.** I jumped to describing phases and architecture
   without formally defining what we were solving for, what the knowns and unknowns were,
   or what equations governed the problem. Reporter-mode, not analyst-mode.

2. **No inventory was done before building.** For two months, no one documented what
   endpoints existed, what fields they returned, what the access boundaries were, or
   what the data looked like. Code was attempted before knowledge existed.

3. **No skills were created.** A WBS was written as a project plan, but zero actual
   skill files were produced. The WBS was a table of contents with no book behind it.
   Each distinct unit of work requires its own skill with full Five Pillars treatment.

4. **Clarifying questions were used as a substitute for autonomous work.** Every
   technical decision was pushed back to Anish instead of being resolved by the agent.
   Anish has ADHD and executive dysfunction — every question drains his energy.
   The agent must BE the executive function.

5. **Band-aid fragments were built.** Pieces of systems were coded without connecting
   them. No handoffs were defined. Nothing worked end-to-end.

6. **The Five Pillars were summarized, not executed.** The document was read but its
   protocols were not run. Equations were not written. Inversion was not done.
   Pre-mortem was not done. It was described in abstract, not applied in concrete.

### How this skill prevents those failures

- Problem statement is written FIRST (below) with formal variables, equations, knowns/unknowns
- Inventory/recon is completed before any code
- This IS the skill file — it exists, it has the Five Pillars, it proves compliance
- No clarifying questions — all decisions are made autonomously and documented
- The full pipeline is specified end-to-end with handoff contracts
- Every pillar is EXECUTED, not described

---

## PILLAR I — PROBLEM-SOLVING (Problem Crystallization)

### 1.1 Problem Statement (formal, one sentence, no hedging)

Ingest all available data from WhaleWisdom's API — 13F institutional holdings,
insider transactions (Form 4), fund manager metadata, and filer group data —
for all filers across the most recent 8 quarters, into local Parquet staging files
organized by filer and quarter, with schema validation, rate-limit compliance,
incremental update capability, and full audit trail.

### 1.2 Decision Variable

What to optimize: **completeness × speed** — maximize the fraction of available
WhaleWisdom data captured per unit of wall-clock time, subject to rate-limit
constraints and API terms of service.

### 1.3 State Variables

| Variable | Type | Current Value | Desired Value |
|----------|------|---------------|---------------|
| 13F filings ingested | count | 0 | ALL filings for 8 quarters |
| Insider transactions ingested | count | 0 | ALL Form 4 transactions available |
| Fund manager profiles ingested | count | 0 | ALL filer profiles |
| Data freshness | timestamp | never | < 24 hours from latest SEC filing |
| Schema documentation | % complete | 0% | 100% (every field known) |
| Pipeline automation | boolean | false | true (runs on schedule) |

### 1.4 Constraints

- **Rate limits:** WhaleWisdom API rate limits unknown (UNKNOWN — must discover)
- **45-day delay:** 13F filings are reported 45 days after quarter end (regulatory)
- **API authentication:** shared_key + secret_key (already have credentials)
- **Storage:** Must fit on available drives (estimate size: UNKNOWN — must calculate)
- **No code yet:** This skill must be fully specified before implementation begins
- **Single operator:** System must run autonomously without Anish's intervention

### 1.5 Objective Function

```
Maximize: Completeness(filers, quarters) × Freshness(last_update)
Subject to: RateLimit(requests/sec) ≤ API_max
            Storage(total_GB) ≤ Available_disk
            Latency(ingestion_time) ≤ Acceptable_window
```

### 1.6 Cynefin Classification

**Complicated** — The API has knowable structure. The data has knowable schema.
The relationships between filings, filers, and holdings are deterministic.
Requires expertise to map but is not inherently unpredictable.
Approach: analyze → plan → execute (not probe-sense-respond).

### 1.7 Equation Triangulation (3 disciplines, per R3)

**E1 — Information Theory (Shannon): Channel Capacity**
```
C = B × log₂(1 + S/N)
```
The WhaleWisdom API is a channel. Bandwidth B = requests/second allowed.
Signal S = useful data per response. Noise N = overhead (pagination, errors, retries).
Channel capacity is maximized by: (a) maximizing payload per request (batch queries
if available), (b) minimizing retries (respect rate limits proactively, don't hit 429s),
(c) parallelizing where allowed. The 45-day filing delay is NOT noise — it's latency
in the channel. The signal is still high-quality once it arrives.

**E2 — Queueing Theory (Little's Law): Throughput**
```
L = λ × W
```
L = number of requests in flight. λ = arrival rate (requests/sec we send).
W = average service time per request (API response latency).
If API response time W = 0.5s, and we can have L = 1 concurrent request,
then λ = L/W = 2 requests/sec maximum throughput.
For 8 quarters × ~5,000 filers × 2 requests each (filing list + holdings detail) =
80,000 requests. At 2 req/s = 40,000 seconds = ~11 hours minimum.

**CRITICAL UNKNOWN:** We don't know the actual rate limit, the actual number of
filers, or the actual response time. These are unknowns that must be measured
in Phase 0 before any download estimate is reliable.

**E3 — Logistics / Supply Chain (Throughput Accounting): Bottleneck Identification**
```
System_throughput = min(Stage_1_throughput, Stage_2_throughput, ..., Stage_n_throughput)
```
The pipeline has stages: API call → JSON parse → validate → transform → write Parquet.
The bottleneck determines total throughput. If the API is the bottleneck (likely —
it's the slowest stage due to network latency and rate limits), then optimizing
downstream stages (parsing, validation) has zero effect on total throughput.
Focus optimization effort on the bottleneck: batch requests if possible,
minimize wasted calls, cache responses.

### 1.8 Where the equations AGREE

All three say: **measure the API constraints first before estimating anything.**
Without knowing the rate limit, filer count, response size, and latency, all
download time estimates are fabricated. The first task is empirical measurement.

### 1.9 Where the equations DISAGREE

E1 says maximize signal per request (batch). E2 says throughput is constrained by
concurrency. E3 says find the bottleneck and optimize only that. Resolution:
if the API is the bottleneck (likely), then E1 and E3 agree — maximize useful
data per API call. E2 just tells us what the theoretical maximum throughput is.

### 1.10 Knowns

| Known | Value | Source |
|-------|-------|--------|
| API base URL | https://whalewisdom.com/shell/command.json | Credentials file |
| Shared key | 1WCfcW0xi4tykIAwxuUw | Claude settings |
| Secret key | nWn4SZ25ngk4xqvGL1gGUmMUy651lsbYJixXc3px | Claude settings |
| Auth method | GET params (shared_key + secret_key) | API docs |
| 13F filing delay | 45 days after quarter end | SEC regulation |
| Quarter end dates | 03-31, 06-30, 09-30, 12-31 | Standard fiscal |
| 8 quarter range | Q3 2024 through Q2 2026 | User requirement |
| Data format | JSON responses | API docs |
| Storage target | Parquet files | Architecture decision |
| Output location | OWC 8-bay or local SSD (TBD by storage skill) | Hardware inventory |

### 1.11 Unknowns (MUST RESOLVE BEFORE IMPLEMENTATION)

| Unknown | Why It Matters | How to Resolve |
|---------|---------------|----------------|
| API rate limit (req/sec or req/min) | Determines download time and retry strategy | Empirical test: send requests and measure when throttling occurs |
| Total number of 13F filers per quarter | Determines total request count | API call: search all filers, count results |
| Number of holdings per filer per quarter | Determines total data volume | Sample 10 large filers, measure |
| Response size per request (KB) | Determines storage and bandwidth needs | Sample calls, measure response sizes |
| Available API commands (full list) | Determines what data we can get | Test every command mentioned in docs + probe for undocumented ones |
| Pagination behavior | Determines how to handle large result sets | Test with large queries |
| Historical depth | How far back does WhaleWisdom data go? | API test with old dates |
| Insider transaction coverage | Which companies/insiders are covered? | API test |
| Error handling / retry semantics | How does the API signal errors? | Observe error responses |
| Data update frequency | How often is new filing data added? | Compare filing dates to WhaleWisdom availability |
| Does WhaleWisdom have a GitHub? | Could provide SDKs, tools, examples | Web search |
| Does WhaleWisdom provide flat files? | Could bypass API for bulk download | Check website/docs |
| Competitor data sources for 13F | Backup if WhaleWisdom has gaps | Web search (SEC EDGAR direct, Fintel, etc.) |

### 1.12 Falsification Design (Pillar I, Stage 4)

**What data would confirm our model is correct?**
- API calls return structured JSON with consistent schema across quarters
- Rate limits are stable and predictable (not dynamic/adaptive)
- 8 quarters of data is downloadable within our estimated time window
- Downloaded data matches what WhaleWisdom shows on their website for the same filer

**What data would falsify it?**
- API returns different schema per quarter (would require per-quarter cleaning rules)
- Rate limits are extremely restrictive (e.g., 1 req/min would make bulk download take weeks)
- Some quarters have no data or missing filers (coverage gap)
- API authentication expires or rotates (credential management needed)

**Smallest experiment to meaningfully update our estimates:**
1. Call `filer_search` with no filter to count total filers (~5 minutes)
2. Call `holdings` for 3 different filers (small, medium, large) to measure response sizes (~2 minutes)
3. Send 10 requests in rapid succession to measure rate limit response (~1 minute)
Total: ~8 minutes of API calls tells us whether this is an 11-hour job or a 5-day job.

---

## PILLAR II — CRITICAL THINKING (System Map, Leverage, Inversion)

### 2.1 System Map

```
                    ┌─────────────────────┐
                    │    SEC EDGAR         │
                    │  (raw 13F filings)   │
                    └─────────┬───────────┘
                              │ parsed by WhaleWisdom
                              ▼
                    ┌─────────────────────┐
                    │  WhaleWisdom DB      │
                    │  (structured data)   │
                    └─────────┬───────────┘
                              │ exposed via API
                              ▼
┌──────────────┐    ┌─────────────────────┐    ┌──────────────────┐
│ Rate Limiter │◄──►│  WhaleWisdom API     │◄──►│ Our Ingestion    │
│ (unknown)    │    │  (REST/JSON)         │    │ Pipeline         │
└──────────────┘    └─────────────────────┘    └────────┬─────────┘
                                                        │
                                               ┌────────▼─────────┐
                                               │ Raw JSON staging  │
                                               └────────┬─────────┘
                                                        │ validate + transform
                                               ┌────────▼─────────┐
                                               │ Clean Parquet     │
                                               │ (partitioned by   │
                                               │  filer + quarter) │
                                               └────────┬─────────┘
                                                        │ load
                                               ┌────────▼─────────┐
                                               │ DuckDB            │
                                               │ (queryable)       │
                                               └──────────────────┘
```

### 2.2 Stocks and Flows

- **Stock:** WhaleWisdom's database (accumulates as SEC filings are parsed)
- **Flow in:** SEC EDGAR filings → WhaleWisdom parsing (we don't control this)
- **Stock:** Our local data store (accumulates as we ingest)
- **Flow in:** API calls → our pipeline (we control this)
- **Flow out:** Queries from experiment engine (downstream consumer)

### 2.3 Feedback Loops

**Balancing (B1 — Rate Limiting):** As we increase request rate → API throttles →
effective throughput decreases → we must slow down. Equilibrium: send at exactly
the rate limit, no faster.

**Reinforcing (R1 — Data compounds):** More quarters ingested → richer
quarter-over-quarter change analysis → more signals → more experiment hypotheses
→ more demand for data → motivation to ingest more.

### 2.4 Leverage Points (Meadows)

| Rank | Level | Leverage Point | Action |
|------|-------|---------------|--------|
| 1 | **7 — Information** | We don't know what commands the API supports or what its limits are | Resolve ALL unknowns (§1.11) before downloading |
| 2 | **4 — Delays** | 45-day filing delay is regulatory and cannot be reduced | Design around it: schedule ingestion ~50 days after quarter end; don't check daily when no new filings exist |
| 3 | **8 — Rules** | Define batch vs sequential download rules | Batch by quarter (all filers for Q1, then Q2, etc.) to enable checkpointing |
| 4 | **1 — Parameters** | Request rate, batch size, retry backoff | Tune after measuring rate limits |

### 2.5 Inversion — How to GUARANTEE this fails

1. Start downloading without knowing the rate limit → get IP banned or key revoked
2. Don't validate responses → silently ingest corrupted or incomplete data
3. Don't checkpoint progress → crash at 90% and start over from zero
4. Assume all filers have the same schema → miss edge cases (small filers, international, etc.)
5. Don't compare downloaded data against the website → no ground truth validation
6. Don't account for the 45-day delay → check for Q2 2026 data on June 30 and panic when it's not there (it won't arrive until ~August 14)
7. Download everything sequentially with no parallelism → take 5x longer than necessary
8. Don't store raw JSON → lose the ability to re-process if schema understanding changes
9. Don't handle API errors gracefully → one 500 error kills the entire pipeline
10. Don't document what was downloaded → no way to verify completeness

### 2.6 Pre-Mortem — It's 6 months from now and WhaleWisdom ingestion failed

**Cause 1 (most probable):** API credentials expired or were rotated. Nobody noticed.
Pipeline kept running but getting 401s. Months of data were missed.
→ *Earliest signal:* Health check that verifies auth on every run. Alert on non-200.

**Cause 2:** WhaleWisdom changed their API response schema (added/removed fields).
Pipeline kept running but writing garbage to Parquet. Downstream queries returned
wrong results. Experiments based on this data produced misleading conclusions.
→ *Earliest signal:* Schema hash validation on every ingestion run. Compare response
fields against stored baseline. Alert on ANY mismatch.

**Cause 3:** We downloaded 8 quarters but missed 200 small filers because our
filer list was incomplete. We didn't know they were missing because we never
verified completeness against an independent source (SEC EDGAR filing count).
→ *Earliest signal:* Cross-reference our filer count per quarter against SEC EDGAR
FULL-INDEX filing count. Flag if our count < 95% of EDGAR count.

### 2.7 Lollapalooza Scan

**Forces FOR us:**
- WhaleWisdom already did the hard work of parsing SEC EDGAR XML into structured data
- 13F data is public (no legal risk in downloading)
- The 45-day delay is known and constant (predictable, not random)
- We already have API credentials (no onboarding friction)

**Forces AGAINST us:**
- Unknown rate limits could make bulk download impractical
- 45-day delay means the data is ALWAYS stale — alpha decay is real
- WhaleWisdom could change their API without notice (no SLA for our tier)
- We have no backup data source if WhaleWisdom goes down

**Net assessment:** Favorable, but the rate limit unknown is the single biggest risk.
Resolve it first.

---

## PILLAR III — CRYPTOGRAPHY (Hidden Structure Extraction)

### 3.1 Adversarial Framing

WhaleWisdom's data is NOT raw SEC filings — it's WhaleWisdom's INTERPRETATION of
those filings. The encoding is: SEC XML → WhaleWisdom parsing → structured JSON.
We are trusting WhaleWisdom's parser. The hidden assumption: their parser is correct.

**How to test this assumption:** For a sample of filers, compare WhaleWisdom API
output against raw SEC EDGAR filings. If they diverge, WhaleWisdom's parser has bugs
and we need to decide whether to trust their data or build our own parser.

### 3.2 Hidden Structure in 13F Data

The surface data is "Fund X holds Y shares of Stock Z." The hidden structure:
- **Position changes** across quarters reveal strategy (accumulating, trimming, liquidating)
- **Crowding** — when many funds converge on the same position, it's a crowded trade
  (high risk of correlated liquidation)
- **New positions** — a fund's first entry into a stock is a stronger signal than
  increasing an existing position
- **Timing vs filing** — the filing is 45 days stale. The REAL question is: does the
  fund still hold this position NOW? (requires combining with other data: options flow,
  dark pool, insider transactions)
- **Size relative to AUM** — a $10M position in a $100B fund (0.01% of AUM) is noise.
  A $10M position in a $50M fund (20% of AUM) is a high-conviction bet.

### 3.3 Side-Channel Analysis

The most valuable signal from 13F data is NOT the holdings themselves — it's the
**changes and the patterns of changes across funds**. This requires:
- Quarter-over-quarter diff calculation (new positions, increased, decreased, sold)
- Cross-fund correlation (are multiple smart-money funds making the same move?)
- Size-weighted conviction scoring (position size / AUM = conviction level)
- Timing clustering (did 5 funds all initiate the same position in the same quarter?)

These are computations we perform AFTER ingestion, but they determine HOW we
structure the data during ingestion (we need filer AUM, position values, and
quarter-over-quarter comparability).

---

## PILLAR IV — STATISTICAL MODELING (Estimation and Calibration)

### 4.1 Download Time Estimation (to be calibrated after Phase 0)

**Preliminary model (full of unknowns — will be updated):**

```
T_total = N_filers × N_quarters × R_per_filer × (1/λ_max + W_overhead)

Where:
  N_filers    = total 13F filers per quarter (~5,000? UNKNOWN)
  N_quarters  = 8
  R_per_filer = requests needed per filer per quarter (2-3: list + holdings + detail)
  λ_max       = max allowed request rate (req/sec) (UNKNOWN)
  W_overhead  = per-request overhead (parsing, writing) (~0.05s)
```

**Scenario analysis (until unknowns are resolved):**

| Scenario | N_filers | R_per_filer | λ_max | Total requests | Time |
|----------|----------|-------------|-------|---------------|------|
| Optimistic | 3,000 | 2 | 5/sec | 48,000 | 2.7 hours |
| Base case | 5,000 | 3 | 2/sec | 120,000 | 16.7 hours |
| Pessimistic | 8,000 | 4 | 1/sec | 256,000 | 71 hours (3 days) |
| Worst case | 8,000 | 4 | 0.5/sec | 256,000 | 142 hours (6 days) |

**These numbers are NOT reliable until we measure.** The 8-minute experiment
described in §1.12 will collapse these scenarios to a single calibrated estimate.

### 4.2 Storage Estimation

**Per-filer per-quarter data:**
- Filing metadata: ~1 KB
- Holdings list (assuming avg 200 positions): ~50-100 KB JSON, ~20-40 KB Parquet
- Insider transactions: variable, ~5-50 KB

**Total estimate (base case):**
```
5,000 filers × 8 quarters × 60 KB/filer/quarter = 2.4 GB raw JSON
Parquet compression ~3:1 → ~800 MB Parquet
```

This is small. Storage is NOT the bottleneck. Time is.

### 4.3 Reference Ranges (what good/bad/critical looks like)

| Metric | Good | Acceptable | Degraded | Critical |
|--------|------|------------|----------|----------|
| Completeness (% of filers captured) | > 99% | > 95% | > 90% | < 90% |
| Schema consistency (fields matching baseline) | 100% | 100% | < 100% → ALERT | N/A |
| Ingestion success rate (% of requests 200 OK) | > 99% | > 95% | > 90% | < 90% → STOP |
| Freshness (days since last new filing ingested) | < 2 | < 7 | < 14 | > 14 → investigate |
| API response time (seconds) | < 1 | < 3 | < 10 | > 10 → investigate |

---

## PILLAR V — GAME THEORY (Multi-Agent, Adversarial)

### 5.1 Players

1. **Us** — want all data, as fast as possible, continuously updated
2. **WhaleWisdom** — want to provide data but not be overwhelmed (rate limits exist for a reason)
3. **SEC** — provides the raw data; has no stake in our ingestion
4. **Other WhaleWisdom API users** — share the same rate-limited resource
5. **Future Anish** — will query this data for experiments; needs it queryable and correct

### 5.2 Best Response Analysis

If we send requests too fast → WhaleWisdom throttles or bans us → we get zero data.
If we send requests too slow → we waste time → Anish waits longer → frustration.
Nash equilibrium: send at exactly the sustainable rate, with exponential backoff on 429s.

### 5.3 Mechanism Design

We should design our ingestion to be a **good citizen**:
- Respect rate limits proactively (don't trigger 429s)
- Send User-Agent identifying ourselves
- Use conditional requests (If-Modified-Since) if supported to reduce unnecessary load
- Schedule bulk downloads during off-peak hours (late night / weekends)

This is not altruism — it's self-interest. A banned API key is worse than a slow download.

---

## WORK BREAKDOWN STRUCTURE (within this skill)

### WW-0.0 Phase Statement: Reconnaissance & Measurement
Resolve ALL unknowns from §1.11 before downloading any data.

### WW-0.1 — API Command Discovery [TASK]
- **What:** Test every known and suspected API command
- **Commands to test:** stock_lookup, filer_search, filer, holdings, insider_transactions,
  insider_summary, filing_details, filer_group, and any others discovered
- **For each:** Document full parameter set, response schema, every field
- **Status:** WhaleWisdom access test agent running (results pending)

### WW-0.2 — Rate Limit Measurement [TASK]
- **What:** Empirically determine the API rate limit
- **Method:** Send increasing burst of requests, measure when throttling occurs
- **Output:** Confirmed requests/second or requests/minute limit
- **Duration:** ~5 minutes

### WW-0.3 — Filer Count Measurement [TASK]
- **What:** Determine total number of 13F filers per quarter
- **Method:** filer_search with broad filter, paginate through all results, count
- **Output:** Exact filer count for most recent quarter
- **Duration:** ~10 minutes (depends on rate limit)

### WW-0.4 — Holdings Size Sampling [TASK]
- **What:** Measure response size for small, medium, and large filers
- **Method:** Pick 3 filers (e.g., small fund, mid-size, Berkshire Hathaway), get holdings
- **Output:** Average response size in KB, average holdings count per filer
- **Duration:** ~2 minutes

### WW-0.5 — Download Time Calibration [TASK]
- **What:** Plug measured values into §4.1 model, produce calibrated time estimate
- **Depends on:** WW-0.2, WW-0.3, WW-0.4
- **Output:** "Downloading 8 quarters of 13F data will take approximately X hours"

### WW-0.6 — Internet-Wide Recon [TASK]
- **What:** Search everywhere (not just WhaleWisdom website) for strategies, gotchas,
  academic papers, Reddit/YouTube/Seeking Alpha discussions, GitHub repos,
  competitor comparisons, SEC EDGAR backup paths
- **Status:** Agent running in background
- **Output:** /quant-brain/recon/whalewisdom-internet-recon.md

### WW-0.7 — SEC EDGAR Cross-Reference Setup [TASK]
- **What:** Set up independent verification source
- **Method:** Download SEC EDGAR FULL-INDEX for the 8 target quarters, count 13-F filings
- **Purpose:** Ground truth to verify WhaleWisdom completeness
- **Output:** Per-quarter filing count from EDGAR

---

### WW-1.0 Phase Statement: Bulk Historical Download
Download all 13F data for 8 quarters. Checkpoint after every quarter.

### WW-1.1 — Filer List Download (per quarter) [TASK]
- **What:** Get complete list of all filers for each quarter
- **Output:** filer_id, name, AUM, filing_date for every filer per quarter
- **Checkpoint:** Save filer list to Parquet after each quarter completes

### WW-1.2 — Holdings Download (per filer per quarter) [TASK]
- **What:** For each filer in each quarter, download full holdings
- **Output:** filer_id, quarter, stock, shares, value, share_change, pct_of_portfolio
- **Checkpoint:** Save per-filer per-quarter. If pipeline crashes at 60%, resume from 60%.
- **Progress tracking:** Log file showing filer_id, quarter, status (pending/done/error)

### WW-1.3 — Insider Transactions Download [TASK]
- **What:** Download all insider transactions (Form 4) for covered companies
- **Output:** insider_name, company, transaction_type, shares, price, date, form_type
- **Checkpoint:** By company or by date range

### WW-1.4 — Fund Manager Metadata Download [TASK]
- **What:** Download all fund manager profile data
- **Output:** filer_id, name, AUM, style, top_holdings, performance metrics (if available)

### WW-1.5 — Raw JSON Preservation [TASK]
- **What:** Store every raw API response as-is before any transformation
- **Why:** If our schema understanding changes, we can re-process without re-downloading
- **Output:** Raw JSON files organized by command/filer/quarter

---

### WW-2.0 Phase Statement: Cleaning & Transformation
Transform raw JSON into clean, validated Parquet files.

### WW-2.1 — Schema Validation [TASK]
- **What:** Validate every response against expected schema
- **Method:** Compare field names and types against baseline from WW-0.1
- **Alert:** On ANY schema deviation

### WW-2.2 — Data Type Casting [TASK]
- **What:** Convert JSON types to proper Parquet types
- **Covers:** dates → date type, shares → int64, values → decimal, percentages → float64

### WW-2.3 — Quarter-over-Quarter Diff Calculation [TASK]
- **What:** Compute position changes between consecutive quarters
- **Output:** For each filer × stock: change_type (new/increased/decreased/sold),
  share_change, value_change, conviction_score (position_value / AUM)

### WW-2.4 — Cross-Fund Crowding Analysis [TASK]
- **What:** For each stock, count how many 13F filers hold it, weighted by AUM
- **Output:** crowding_score per stock per quarter

### WW-2.5 — EDGAR Cross-Reference Validation [TASK]
- **What:** Compare our filer count and filing dates against SEC EDGAR FULL-INDEX
- **Output:** Completeness report: % of EDGAR filings captured, any missing filers
- **Acceptance:** ≥ 95% completeness or investigate gaps

---

### WW-3.0 Phase Statement: DuckDB Integration
Load clean Parquet into the unified analytical layer.

### WW-3.1 — DuckDB Table Design [TASK]
- Tables: ww_filers, ww_holdings, ww_insider_transactions, ww_position_changes
- Foreign keys: filer_id links to filer profile, ticker links to Massive reference data

### WW-3.2 — Materialized Views [TASK]
- top_new_positions_this_quarter
- most_crowded_stocks
- largest_position_increases
- insider_buying_signals

---

### WW-4.0 Phase Statement: Automation & Monitoring

### WW-4.1 — Scheduled Incremental Update [ROUTINE]
- **When:** Daily check for new filings (most activity ~50 days after quarter end)
- **What:** Check for new/amended filings since last run, ingest only new data
- **Routine:** Daily at 6:00 AM CT

### WW-4.2 — Health Monitoring [ROUTINE]
- **What:** Verify API auth is valid, responses are healthy, no schema drift
- **Routine:** Every run (pre-check before any data download)

### WW-4.3 — Completeness Audit [ROUTINE]
- **When:** 60 days after each quarter end (when most 13F filings should be in)
- **What:** Compare our filing count against SEC EDGAR, flag gaps
- **Routine:** Quarterly

---

## HANDOFF SPECIFICATIONS

### Upstream (what this skill receives)
- **From:** Nothing (entry point — WhaleWisdom API is the source)
- **Credentials:** shared_key, secret_key from environment/settings
- **Schedule trigger:** Daily cron or Hermes routine

### Downstream (what this skill delivers)
- **To:** DuckDB unified analytical layer (Phase 3 of main WBS)
- **Format:** Clean Parquet files partitioned by quarter/filer
- **Schema:** Documented in WW-0.1 (after API discovery completes)
- **Freshness guarantee:** Data available in DuckDB within 24 hours of WhaleWisdom update
- **Quality guarantee:** ≥ 95% completeness verified against SEC EDGAR

### Handoff to Experiment Engine
- **What experiments use this data:**
  - Clone investing: replicate top fund positions
  - Crowding detection: identify crowded trades before liquidation
  - New position signals: fund's first entry into a stock
  - Insider buying confluence: 13F + Form 4 alignment
  - Combine with Massive data: 13F holdings changes → predict volume/price impact

---

## MONITORING & OBSERVABILITY

### How to tell if something is wrong

| Signal | Normal | Warning (2σ) | Critical (3σ) |
|--------|--------|--------------|----------------|
| API response time | < 1s | 1-5s | > 5s |
| Error rate per run | < 1% | 1-5% | > 5% |
| Filer count per quarter | ~5,000 ± 500 | < 4,000 or > 6,000 | < 3,000 |
| Holdings per filer | ~200 ± 150 | < 10 or > 1,000 | 0 (empty response) |
| Schema fields | matches baseline | N/A | ANY deviation |
| Auth status | 200 OK | N/A | 401/403 |

### Dashboard metrics
- Last successful ingestion timestamp
- Filers ingested this quarter vs expected
- API error rate (trailing 7 days)
- Storage used
- Next scheduled run

---

## FIVE PILLARS COMPLIANCE PROOF

| Pillar | Section | Evidence |
|--------|---------|----------|
| I. Problem-Solving | §1.1-1.12 | Formal problem statement, 3 equations from 3 disciplines (info theory, queueing theory, logistics), knowns/unknowns table, falsification design |
| II. Critical Thinking | §2.1-2.7 | System map, stocks/flows, feedback loops, Meadows leverage points, 10-point inversion, 3-cause pre-mortem, Lollapalooza scan |
| III. Cryptography | §3.1-3.3 | Adversarial framing (WhaleWisdom as encoder), hidden structure in 13F data, side-channel analysis (cross-fund patterns) |
| IV. Statistical Modeling | §4.1-4.3 | Download time model with 4 scenarios, storage estimation, reference ranges with 4-tier severity |
| V. Game Theory | §5.1-5.3 | 5 players identified, best response analysis (rate limit equilibrium), mechanism design (good citizen strategy) |

---

## PEARLS AND PITFALLS

### Pearls (what to do right)
- **Always store raw JSON** — you will misunderstand the schema the first time. Raw data lets you re-process.
- **Checkpoint after every quarter** — a 6-hour download that crashes at hour 5 and has to restart is devastating.
- **Use SEC EDGAR as ground truth** — WhaleWisdom is a secondary source. EDGAR is the primary source. Always verify against primary.
- **Position size relative to AUM is more informative than absolute position size** — a $100M position in a $500B fund is noise. A $100M position in a $200M fund is the fund's thesis.
- **New positions are stronger signals than increased positions** — a first entry represents a new conviction; an increase might be mechanical rebalancing.

### Pitfalls (what will go wrong if you're not careful)
- **The 45-day delay is REAL** — do not expect Q2 2026 data before mid-August 2026.
- **Amended filings** — some filers submit amendments (13F/A). These REPLACE the original. You must handle amendments or you'll have stale data.
- **Confidential treatment** — some holdings are filed confidentially and appear later. Your Q1 filing might be incomplete even after 45 days.
- **Small filers** — filers with < $100M AUM are not required to file 13F. Your universe is biased toward large institutions.
- **Non-equity holdings** — 13F covers "Section 13(f) securities" which includes some options, warrants, and convertible bonds. Not just stocks.
- **Name changes and ticker changes** — a filer might change their name; a stock might change its ticker. Both require normalization.
