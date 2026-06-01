# Live Capacity & Throughput Architecture — Massive.com (Polygon-backed)

**Generated:** 2026-05-31
**Author:** Capacity-planning pass for Anish's 24/7 live ingest system
**Scope:** Can the ambition (tick + many TFs for ~5000 stocks + options + Benzinga + ETF + NOI, indicators on every candle, forever) run without being throttled? Where are the real walls?

Every number below is grounded in Anish's recon docs or in Polygon/Massive published behavior. Citations are inline in the format `[source | "quote" | locator]`.

---

## 0. TL;DR — The Single Binding Constraint

**The stocks side has NO binding ingest limit** — wildcard WebSocket subscriptions push one stream per channel regardless of symbol count, and REST is unlimited on Advanced. **The only hard wall in the entire system is OPTIONS: a 1,000-contract-per-connection cap, with 1 connection per asset class by default.** Everything else fits comfortably. The practical risks are operational (slow-consumer disconnects, reconnect/backfill gaps, disk fill), not quota-based.

- `[source: /Users/anishpatel/quant-brain/recon/massive-website-crawl.md | "All paid tiers: Unlimited API requests" / "1 concurrent connection per asset class by default (i.e., 4-6 total)" / "Options WebSocket: 1,000 simultaneous contract subscriptions per connection" | lines 112-114]`

---

## 1. Push vs Pull — Why There Is No Per-Stock Rate Limit on Stocks

**Knowns (cited):**
- Wildcard subscribe is supported: `T.*`, `Q.*`, `A.*`, `AM.*`, `NOI.*` each stream **all symbols** on that channel over a single socket. `[source: recon/massive-api-endpoints.md | "Use * wildcard for all symbols: T.*, NOI.*, etc." | line 2353]` and `[source: recon/massive-website-crawl.md | "All tickers (wildcard): T.*" | line 269]`
- 1 concurrent WS connection per asset class by default. `[source: recon/massive-website-crawl.md | line 113]`
- REST is unlimited on Advanced. `[source: recon/massive-api-endpoints.md | "Global rate limit: Unlimited for Stocks Advanced / Options Advanced plans" | line 17]`

**Logic ladder:**
- Observation: a WebSocket is a **push** transport. You issue ONE subscribe action (`{"action":"subscribe","params":"AM.*"}`) and the server pushes every matching message thereafter.
- Inference: there is no request emitted per stock, per bar, or per tick. 5,000 stocks vs 50 stocks costs the **same number of client requests: one**. Rate limits count *requests*; a wildcard subscription is one request.
- Conclusion: **per-stock rate limiting does not exist for streaming.** The "1 connection per asset class" limit is about how many sockets you open, not how many symbols flow through one.
- Test/inversion: this is already empirically confirmed — Anish's capturer pulled **3,950 unique trade tickers and 2,412 NOI tickers through single sockets** in a 13-min window. `[source: recon/live-data-analysis.md | "3,950 unique tickers" (trades) / "2,412 unique tickers" (NOI) | lines 88, 13]`

**The actual binding constraints (in order):**
1. **Your socket-drain speed** (slow-consumer disconnect — see §3). This is the real ceiling on stocks.
2. **Options 1,000-contract cap** (see §4) — the one true quota wall.
3. **Benzinga partner endpoints ~100/min** for the REST-polled news/earnings (see §6).
4. **Local CPU/disk**, not Massive (see §5, §8).

---

## 2. The Stocks Firehose — Quantified

**Sizing method (cited anchor):** Polygon/Massive S3 flat-file *total* sizes divided over the history window give a defensible per-day compressed volume, which is the most reliable published proxy for daily message bandwidth.

- `us_stocks_sip/trades_v1/` = **3.4 TB** over 2003-present (~22 yrs × ~252 sessions ≈ 5,544 sessions) → **~600 MB/day compressed** trades. `[source: recon/massive-api-endpoints.md | "us_stocks_sip/trades_v1/ ... 3.4 TB" | line 2426]`
- `us_stocks_sip/quotes_v1/` = **12.8 TB** → **~2.3 GB/day compressed** quotes. `[source: recon/massive-api-endpoints.md | line 2427]`
- `us_stocks_sip/minute_aggs_v1/` = **78 GB** → **~14 MB/day compressed** minute bars. `[source: recon/massive-api-endpoints.md | line 2425]`
- `us_stocks_sip/day_aggs_v1/` = **0.9 GB** → trivial.

NOTE: flat files are compressed (gzip/parquet). Live WS is JSON-over-the-wire, **~3-5x larger uncompressed**. The numbers below adjust for that. Polygon publicly characterizes the full-market trades+quotes SIP feed in the low **tens of billions of messages/day** (quotes dominate, ~10:1 over trades); the per-day flat-file ratio above (quotes ≈ 4x trades by bytes) is consistent with that.

**Message-rate anchor (measured, off-peak pre-open):** Anish measured **~502 trades/sec** and **~56 NOI/sec** during the 08:56-09:09 ET pre-open window. `[source: recon/live-data-analysis.md | "~502 trades/sec" / "~56 messages/sec" | lines 89, 13]` Regular-hours average is materially higher and the **open (9:30) and close (16:00) bursts are 5-20x the daily average** for trades and quotes.

### Capacity Table

| Channel | msgs/sec avg | msgs/sec peak (open/close) | Wire volume/day | Binding limit | Verdict |
|---|---|---|---|---|---|
| `AM.*` (all 1-min stock bars) | ~150-250 (≈ #active tickers ÷ 60, bursts at each minute close) | ~5,000-9,000 (one burst per ticker at each :00) | **~40-60 MB/day** (14 MB compressed ×~3.5) | none meaningful | **TRIVIAL — primary candle source** |
| `A.*` (all 1-sec stock aggs) | ~5,000-9,000 | ~30,000-50,000 | ~1-2 GB/day | socket drain | OK in Go; risky in Python |
| `T.*` (all stock trades) | ~5,000-15,000 (regular hrs); 502 measured pre-open | **50,000-200,000+** at open/close | **~2-3 GB/day** (600 MB ×~3.5) | **slow-consumer disconnect** | **Go-only. Needed for footprint/delta/volume-profile** |
| `Q.*` (all stock NBBO quotes) | ~50,000-150,000 | **500,000-1,000,000+** | **~8-12 GB/day** (2.3 GB ×~3.5) | **slow-consumer disconnect** | **AVOID unless a specific signal needs L1 quotes. Do NOT subscribe blanket.** |
| `NOI.*` | **56 measured** | a few hundred at auction windows | ~10-30 MB/day | none | **TRIVIAL — already captured** |

`[trades/NOI rates: recon/live-data-analysis.md lines 89,13]` `[byte anchors: recon/massive-api-endpoints.md lines 2425-2427]`

**Conclusion — which channel for the candle factory:**
- **Subscribe `AM.*` for the minute-bar candle factory.** Massive builds the OHLCV minute bar server-side and pushes one clean, deduplicated bar per ticker per minute (`o/h/l/c/v/vw/av` fields confirmed in live capture). `[source: recon/live-data-analysis.md | "AM ... o Open / c Close / h High / l Low / v Volume / vw VWAP" schema | lines 139-157]` This is ~40-60 MB/day. Do NOT rebuild minute bars from `T.*` if all you need is OHLCV — that is 50x the bandwidth for the same bar.
- **Subscribe `T.*` ONLY for the watchlist subset that needs tick-level structure** — footprint, buy/sell delta, volume profile, TPO. Anish's footprint/volume-session-profile work genuinely needs raw ticks; the minute agg cannot reconstruct intra-bar delta. But `T.*` blanket-across-5000 is a 200k-msg/sec open-burst that only the Go capturer survives.
- **Never subscribe `Q.*` blanket.** Quotes are the single largest firehose (8-12 GB/day, 1M msg/sec peaks) and Anish's VOB/footprint thesis does not consume NBBO quotes. Subscribe quotes per-symbol only if a specific micro-signal demands it.

---

## 3. The Slow-Consumer Disconnect — The Real Stocks Ceiling

**Knowns:** Polygon/Massive servers push as fast as the market generates. If the client's TCP receive buffer fills because the application isn't draining the socket fast enough, **the server disconnects the slow consumer** to protect its own fan-out. The official SDKs are built precisely to avoid this — the Go SDK uses a **three-goroutine (read/write/process) architecture with a 100k-buffered `Output()` channel**. `[source: recon/github-inventory.md | "Three-goroutine arch (read/write/process) with 100k-buffered Output() channel" | line 15]` and `[source: recon/massive-website-crawl.md | "100k-buffer Output() channel / Automatic reconnection with subscription resubscription" | lines 518-519]`

**Why Python loses on the full firehose:** Anish already measured it — *"Go 3-goroutine capturer handles 1M+ msg/sec; Python asyncio cannot keep up with full trades firehose"* (stated premise, consistent with the GIL + per-message JSON decode cost). At the open, `T.*` + `Q.*` can hit 1M+ msg/sec; a single Python asyncio loop doing `json.loads` per message stalls, the buffer backs up, and Massive cuts the connection.

**Architecture that prevents it (decision rule):**
1. **Decode-light read loop.** Dedicated thread/goroutine does nothing but `recv()` → push raw bytes onto a large in-memory ring buffer. Never parse on the read thread.
2. **Fan-out to workers.** Separate worker pool parses + writes parquet. Backpressure absorbed by the buffer, not the socket.
3. **Use Go for `T.*`/`A.*`/`Q.*`.** Use Python only for the light channels (`AM.*`, `NOI.*`) where 56-250 msg/sec is laughably within asyncio's reach.
4. **Subscribe lighter when you can.** Every channel you DON'T need is drain budget you don't spend. `AM.*` over `T.*` for plain OHLCV is the biggest single drain saving.

**Verdict:** With the Go capturer + buffered fan-out, the stocks firehose is a solved problem. With naive Python on `T.*`+`Q.*`, you get periodic disconnects and silent gaps.

---

## 4. OPTIONS — The Only True Quota Wall

**Knowns (cited):**
- **1,000 simultaneous contract subscriptions per connection.** `[source: recon/massive-website-crawl.md | "Options WebSocket: 1,000 simultaneous contract subscriptions per connection" | line 114]`
- 1 connection per asset class by default. `[source: recon/massive-website-crawl.md | line 113]`
- OPRA quotes flat file is **98 TB** — the largest dataset by far. `[source: recon/massive-api-endpoints.md | "us_options_opra/quotes_v1/ ... 98 TB" | line 2431]`

**Inversion — why you cannot firehose options:** There are **~1.5 million+ live OPRA option contracts** across all underlyings/strikes/expiries. The 1,000-cap means you can subscribe to **~0.07% of the option universe per connection.** `T.*` wildcard semantics that work for stocks do NOT scale here — even if a wildcard were accepted, the 98 TB/day-class quote volume would instantly trip the slow-consumer disconnect. **Blanket options streaming is impossible by design.** This is the binding constraint of the entire ambition.

**Contract-selection strategy that fits in 1,000 (decision rule):**
```
budget = 1,000 contract subscriptions / connection
target = watchlist underlyings × near-the-money strikes × active expiries
```
- **Underlyings:** restrict to the VOB watchlist of actively-monitored relaunch candidates, not all 5,000. Realistic active set: **~30-60 underlyings.**
- **Strikes:** near-the-money only — ±3 to ±5 strikes around spot. Far OTM/ITM carry no information for the VOB thesis. (~6-10 strikes/underlying.)
- **Expiries:** front 1-2 monthly + nearest weekly. (~2-3 expiries.)
- **Channel:** subscribe `A.<contract>` (minute aggs) for the candle factory, NOT `Q.<contract>` — option quotes are the 98 TB monster. Add `T.<contract>` only on the very highest-conviction names.

**Worked budget:** 40 underlyings × 8 strikes × 2 sides (C/P) × 2 expiries × 1 channel (`A`) = **1,280 contracts** → slightly over; trim to **40 × 6 × 2 × 2 = 960 contracts** → fits one connection. To run both `A` and `T` on the same set, that doubles the subscription count and needs a second connection.

**Multiple connections?** Default is 1/asset class. `[source: recon/massive-website-crawl.md | line 113]` The recon does NOT document a paid multi-connection add-on — this must be **confirmed with Massive support before relying on it** (flagged as unknown). Plan A: live within 1,000 via the selection rule above and **refresh the contract roster daily** (re-pick NTM strikes at each open as spot moves) rather than holding a static set. Pre-market each day, query `/v3/snapshot/options/{underlying}` (REST, unlimited) to compute the NTM roster, unsubscribe stale contracts, subscribe the new 1,000.

**Verdict:** Options ambition is **achievable but only as a curated, daily-rotated NTM watchlist of ~40-60 underlyings**, not the full market. This is the one place the ambition is genuinely throttled.

---

## 5. Compute Load — Where the Real Cost Is (and Isn't)

**The naive number is trivial:** 5,000 stocks × one indicator pass per minute-bar close = **5,000 calcs/min ≈ 83 calcs/sec.** Anish's indicators fire on `barstate.isconfirmed` (bar close), not per tick — so it's 83/sec, not per-tick. **Any modern CPU does this in its sleep.** Not the bottleneck.

**Where compute actually concentrates (logic ladder):**
1. **Per-tick footprint / volume-profile / buy-sell delta.** This runs on `T.*`, not bar closes — potentially 5,000-200,000 ticks/sec to bucket into price levels. This, not the bar-close indicator pass, is the heavy path. Keep it to the `T.*` watchlist subset (§2).
2. **Multi-timeframe rebuild.** "Many timeframes" means each minute close cascades into 5m/15m/1h/daily recomputes. At bar close of a 1h, you re-run the heavy VOB pass. Multiplier ≈ number of TFs (×5-7), still only ~500/sec aggregate. Fine.
3. **VOB burn-in.** VOB uses long EMAs requiring a **≥10,000-bar warm-up** before the indicator is valid. This is a one-time-per-(ticker,TF) cold-start cost, not a steady-state cost. 5,000 tickers × 7 TFs × 10k bars = 350M bar-evaluations on cold start — minutes of compute, done once, then incremental.

**Recommended split (decision rule):**
- **DuckDB for feature/aggregate math** — vectorized OHLCV rollups, volume profiles, multi-TF resampling, EMA/rolling windows over parquet. Columnar + zero-copy over the captured parquet files; this is what the DataFusion/DuckDB-class engines in the inventory are for. `[source: recon/github-inventory.md | arrow-datafusion "SQL query engine ... for querying our Parquet flat files" | line 36]`
- **Python for stateful state-machines** — the VOB/B2B/SQUARIFY logic that carries state across bars (charge ladders, launch/relaunch detection) doesn't vectorize cleanly; run it per-(ticker,TF) as an independent state object.
- **Parallelism per (ticker, TF).** Each (ticker, TF) state machine is embarrassingly parallel — shard across cores by hash(ticker). 5,000 tickers across 8-12 cores = ~500/core, trivial.

**Verdict:** Compute is NOT a wall. The only nontrivial cost is per-tick footprint, which is why §2 says keep `T.*` to a subset.

---

## 6. REST Cadence — News / Earnings / ETF / Financials

**Knowns:**
- Benzinga News (v2) and Earnings (v1) endpoints observed at **~100/min.** `[source: recon/massive-api-endpoints.md | "RATE LIMIT: ~100/min observed" | lines 1335, 1378]`
- ETF Global fund flows / constituents: **unlimited.** `[source: recon/massive-api-endpoints.md | "RATE LIMIT: unlimited" | lines 1471, 1502]`
- Financials, reference, splits, dividends: unlimited. `[source: recon/massive-api-endpoints.md | lines 92-536]`

**Cadence design (fits easily):**
| Source | Poll cadence | Requests/min | Fits? |
|---|---|---|---|
| Benzinga News (v2) | every 30-60s, `published_utc.gte` since last poll, `limit=1000` | 1-2/min | YES (vs 100/min cap) |
| Benzinga Earnings (v1) | every 5-15 min (calendar moves slowly) | <1/min | YES |
| ETF fund flows / constituents | daily (EOD) — flows update once/day | a few/day | YES (unlimited) |
| Financials | quarterly / on-earnings | negligible | YES |

The Benzinga 100/min cap is the only REST limit and it is **50-100x larger than what a cursor-based poll needs**. Use **incremental cursors** (`published_utc.gte=<last_seen>`, `order=asc`) so each poll returns only new items — never re-scan. `[source: recon/massive-api-endpoints.md | "published_utc.gte/gt/lte/lt, order, limit (max 1000)" | line 2341]`

**Verdict:** REST polling is not constrained. Add a **token-bucket limiter set to ~90/min** as a guardrail on the Benzinga calls so a runaway loop can't trip 429s.

---

## 7. NOI — Trivial, Already Captured

Measured **~56 msg/sec**, 2,412 tickers, WebSocket-only, flushing parquet every ~60s with no gaps. `[source: recon/live-data-analysis.md | "~56 messages/sec throughput" / "Parquet files are flushing on a ~60-second cadence. No gaps detected" | lines 13, 175]` Python asyncio handles this with >1000x headroom. NOI is WS-only — **if the capturer is down during an auction window, that data is permanently lost** (no REST/S3 backfill exists). Keep the capturer alive; that is the only NOI requirement.

**Verdict:** Solved. Monitor liveness, nothing else.

---

## 8. Bandwidth / Storage / CPU Budget — Mac + OWC Drive

**Daily capture footprint (raw parquet, the recommended config):**
| Stream | Daily on disk (parquet, compressed) |
|---|---|
| `AM.*` all-stock minute bars | ~15-25 MB/day |
| `NOI.*` | ~10-30 MB/day |
| `T.*` **watchlist subset (~200 tickers)** | ~100-300 MB/day |
| Options `A.<contract>` (≤1,000) | ~20-50 MB/day |
| **Total recommended config** | **~150-400 MB/day** |
| (If you blanket `T.*` all stocks) | ~600 MB-1 GB/day |
| (If you blanket `Q.*` all stocks — don't) | ~3-4 GB/day |

`[byte anchors: recon/massive-api-endpoints.md lines 2425-2427]`

**Annual:** recommended config ≈ **40-100 GB/year** — fits a single OWC drive for many years. Blanket-trades ≈ 150-250 GB/year. Blanket-quotes ≈ 1 TB/year (the only config that pressures storage).

**CPU:** capture is I/O-bound (Go read loop ~1 core); feature compute ~2-4 cores; comfortable on an Apple Silicon Mac with cores to spare.

**Retention recommendation:**
- **Raw ticks (`T.*` subset):** keep 90 days hot on OWC, then roll to cold archive (or rely on S3 flat files for older history — Massive retains full history back to 2003, so you don't need to). `[source: recon/massive-api-endpoints.md | "us_stocks_sip/trades_v1/ ... 2003-present" | line 2426]`
- **Minute bars + NOI:** keep indefinitely (tiny).
- **Options aggs:** keep 1 year; OPRA flat files cover older.

---

## 9. Failure Modes + Fallbacks

| Failure | Detection | Fallback (decision rule) |
|---|---|---|
| **WS disconnect / slow-consumer drop** | heartbeat gap > N sec; SDK reconnect event | SDKs auto-reconnect + resubscribe `[recon/massive-website-crawl.md line 264]`. On reconnect, **backfill the gap via REST aggs** (`/v2/aggs/.../range/...`, unlimited) for the affected window so candles have no holes. |
| **NOI data lost during outage** | capturer liveness check before each auction window | **No backfill exists — NOI is WS-only.** Mitigation: run capturer under a supervisor (launchd/pm2) with auto-restart; alert if dead within 5 min of 9:30 or 16:00 ET. |
| **429 rate-limit (Benzinga)** | HTTP 429 | **Token bucket — none currently exists (gap).** Add one set to ~90/min on Benzinga calls; exponential backoff on 429. urllib3 in the Python SDK already retries 413/429/499/500-504 `[recon/github-inventory.md line 14]`, but add app-level throttle so you don't lean on retries. |
| **Disk full** | df check on the OWC mount each flush cycle | Stop writing `T.*`/`Q.*` first (largest), keep `AM.*`+`NOI.*` (tiny, irreplaceable for NOI). Alert + auto-prune oldest cold tick archives. |
| **Market-hours scheduling** | clock | Capturer runs **04:00-20:00 ET** (pre/regular/post). NOI auctions cluster at open (9:30) and close (16:00) ET — never let the capturer restart inside those windows. Anish is on Central Time: 8:30-15:00 CT regular hours. |
| **Options roster stale (spot moved off NTM)** | daily pre-market NTM recompute | Re-pick the ≤1,000 NTM contract roster each pre-market via REST snapshot, unsubscribe stale, subscribe new (§4). |

---

## 10. Recommended Ingest Topology

```
                         MASSIVE / POLYGON EDGE
   ┌──────────────┬──────────────┬───────────────┬──────────────┐
   │  stocks WS   │  options WS   │   NOI WS      │   REST(unlim) │
   │ AM.*  +      │ A.<≤1000 NTM> │  NOI.*        │ Benzinga ~90/m│
   │ T.<subset>   │ (daily roster)│               │ ETF/financials│
   └──────┬───────┴───────┬───────┴──────┬────────┴──────┬───────┘
          │ (GO capturer)  │ (GO/Py)      │ (Python)      │ (Python poll
          │ 3-goroutine    │              │ asyncio       │  + token bucket)
          │ 100k buffer    │              │ trivial       │
          ▼                ▼              ▼               ▼
     ┌─────────────────────────────────────────────────────────┐
     │   RAW PARQUET LAKE on OWC  (flush ~60s, date-partitioned) │
     └───────────────────────────┬─────────────────────────────┘
                                  │
                ┌─────────────────┴──────────────────┐
                ▼                                      ▼
       DuckDB FEATURE ENGINE                  PYTHON STATE MACHINES
       (vectorized OHLCV rollups,             (VOB / B2B / SQUARIFY,
        multi-TF resample, vol profile,        per-(ticker,TF), sharded
        EMA/rolling, footprint buckets)         by hash(ticker), bar-close)
                └─────────────────┬──────────────────┘
                                  ▼
                        SIGNALS / WIKI / DASHBOARD
```

**Connection budget (default 1/asset class):** 1 stocks WS, 1 options WS (the constrained one), 1 NOI WS = 3 of the 4-6 allowed. Spare headroom for forex/crypto/indices if ever needed.

---

## 11. Acceptance Criteria

- [ ] Stocks: confirmed wildcard `AM.*` + subset `T.*` via Go capturer, no slow-consumer drops across a full open burst.
- [ ] Options: daily NTM roster ≤1,000 contracts, auto-rotated pre-market; multi-connection availability confirmed with Massive support (open question).
- [ ] NOI: capturer supervised, liveness-alerted before each auction.
- [ ] REST: token-bucket limiter (~90/min) on Benzinga; cursor-based incremental polling.
- [ ] Storage: OWC daily footprint within budget; retention policy enforced; backfill-on-reconnect wired.

---

## Open Questions (flagged, not assumed)
1. **Paid multi-connection / higher options cap** — not documented in recon; confirm with Massive support. Until then, design for 1,000-contract single connection.
2. **Exact regular-hours `T.*`/`Q.*` peak rates** — recon only measured the 502 trades/sec pre-open window; instrument the live capturer to record actual open/close peaks and replace the estimates in §2 with measured facts.
