# Options Data Primer — For the Options Department Lead Agent

**Author:** Claude (data/architecture)  **Date:** 2026-05-31  **Status:** authoritative briefing
**Audience:** the LLM agent owning the options edge-research department
**Source of truth:** live Massive.com API pulls (this doc), `recon/massive-api-endpoints.md`, `recon/s3-flatfiles-access-proof.md`

---

## 1. Your mission, stated in our terms

We do not trade options for premium decay, spreads, or theta farming. Options exist in this system for **one** reason: they are **X-ray vision into the transference of energy**. Our North Star is a 2×2:

| Underlying signal | It is **POTENTIAL** energy (stored, about to reverse) | It is **KINETIC** energy (releasing, continuing) |
|---|---|---|
| **Bearish** signal | bearish exhaustion → fuel for a **bullish** launch | bearish move accelerating **down** |
| **Bullish** signal | bullish coiling → fuel for a continued **bullish** launch | bullish move accelerating **up** |

Price alone cannot tell you which quadrant you are in at the moment it matters — the **transference period**, the "chemical reaction" between stored and released energy. That is precisely where the options tape carries information the underlying does not: **who is positioning, at what strike, with what urgency, and how dealers are forced to hedge.** A bearish print on the tape with calls being accumulated and put IV collapsing is potential energy for a reversal. The same bearish print with put volume surging, IV expanding, and OI migrating to lower strikes is kinetic continuation. **Your job is to build the detectors that separate those two cases.** This document tells you exactly what raw material you have to do it with.

---

## 2. The 1,000-contract cap — the problem, the constraint, the capability

There is exactly **one hard quota wall** in our entire Massive subscription, and it is yours: the **options WebSocket allows 1,000 simultaneous contract subscriptions per connection**, and we get **one connection per asset class** by default `[recon/massive-website-crawl.md:113-114]`. Stocks are uncapped (one wildcard `T.*` streams the whole market); options are not — OPRA lists **~1.5 million live contracts**, so a live wildcard would be 1,500× over the cap. Full-market options **streaming is impossible by design**.

**This constraint applies to LIVE streaming only.** It does **not** apply to REST or to the S3 flat-file archive. That distinction is the most important thing in this document, so be precise about it:

- **LIVE (WebSocket):** you choose ≤1,000 contracts and stream their trades/quotes/second-bars in real time. This is your *real-time sensor*, and it is rationed. You spend those 1,000 slots on the contracts where the transference is happening **right now** — your active VOB candidates × near-the-money strikes × the front 1–2 expiries. Re-pick the roster every pre-market as spot moves.
- **REST (on-demand):** **unlimited** request rate on Options Advanced `[recon/massive-api-endpoints.md:17]`. You can pull a full option-chain snapshot (every strike, every expiry, with greeks/IV/OI) for any underlying, any time, with no 1,000 cap. The chain snapshot is your *whole-market scan*; the WebSocket is your *zoom lens*.
- **FLAT FILES (S3 archive):** **the entire OPRA history of every contract that has ever traded.** No cap, no rationing. This is your *historical laboratory*.

So the mental model you must hold: **the 1,000 cap is a real-time attention budget, not a data-availability limit.** Historically and on-demand you can see everything. Live, you must aim.

---

## 3. The granular tree → the forest (what you can actually get)

Think of it as a resolution ladder. For **every** option contract you can obtain, at both live and historical scope:

| Resolution | What it is | Live channel | Historical source | Depth |
|---|---|---|---|---|
| **TICK — trades** | every individual execution: price, size, exchange, condition | `T.<contract>` (WS) | `/v3/trades` (REST) + S3 `trades_v1/` | **2014 → present** |
| **TICK — quotes (NBBO)** | every best bid/ask change | `Q.<contract>` (WS) | `/v3/quotes` (REST) + S3 `quotes_v1/` | **2022 → present** |
| **PER-SECOND agg** | 1-second OHLCV | `AS.<contract>` (WS) | **WS-only — no flat file** (rebuild from ticks) | forward-capture only |
| **PER-MINUTE agg** | 1-minute OHLCV+vwap+trade-count | `A.<contract>` (WS) | `/v2/aggs` (REST) + S3 `minute_aggs_v1/` | **2014 → present** |
| **DAILY agg** | 1-day OHLCV (the "forest") | — | `/v2/aggs` (REST) + S3 `day_aggs_v1/` | **2014 → present** |
| **CHAIN SNAPSHOT** | greeks, IV, OI, day-stats, NBBO, last trade — **the analytical layer** | — | `/v3/snapshot/options/{underlying}` (REST, current only) | live snapshot |

**The tree (most granular):** an individual option trade, nanosecond-timestamped, with exchange and condition code — e.g. a single 3-lot print of `O:NVDA260601C00155000` at \$60.92 at `1780078288334000000` ns. **The forest (least granular):** one row per contract per day — 364,438 rows covering *every* contract that traded that session, ~4 MB compressed. You can hold the entire forest for years on the OWC drive; you sample the tree where it matters.

**What you can download — the absolute maximum** `[recon/s3-flatfiles-access-proof.md:105-145]`:

| S3 prefix (`us_options_opra/`) | Range | Compressed/day | Total archive |
|---|---|---|---|
| `day_aggs_v1/` | 2014→ | ~4 MB | ~5.5 GB |
| `minute_aggs_v1/` | 2014→ | ~24–29 MB | ~33 GB |
| `trades_v1/` | 2014→ | ~62–78 MB | ~74 GB |
| `quotes_v1/` | 2022→ | ~106–172 GB | **~98 TB** |

**Recommendation, concrete:** pull `day_aggs` (5.5 GB) and `minute_aggs` (33 GB) **in full, now** — that is twelve years of every contract's OHLCV for under 40 GB, and it is enough to build OI/volume/IV-history features for the entire market. Pull `trades_v1` (74 GB) in full too; tick-level option trades for all history fit comfortably. **Do not bulk-download `quotes_v1`** — 98 TB will not fit and you do not need every NBBO change for every dead contract. Pull option quotes selectively (per underlying, per event window) from REST or targeted S3 date ranges. Download S3 **sequentially**, not in parallel — parallel pulls trip a 429 `[recon/historical-download-status.md:79]`.

---

## 4. Where the edge lives — assessment, mapped to the 2×2

You are the subject-matter expert and you will form your own hypotheses, but here is the starting map of which variables illuminate which quadrant. This is a hypothesis menu, not dogma.

**Stored potential energy (pre-transference) is visible in standing positioning:**
- **Open interest distribution across strikes** — where is the crowd parked? OI building at strikes *above* a falling price = potential bullish energy (someone is positioning for the reversal, not the continuation).
- **IV term structure & skew** — put-skew steepening into a selloff is fear *pricing in* (kinetic); put-skew flattening while price falls is fear *exhausting* (potential reversal). The skew is the chemistry of the transference.
- **Greeks aggregates** — net dealer gamma. Near a large positive-gamma strike, dealers hedge *against* the move (suppressive, potential coiling); negative-gamma regimes *amplify* the move (kinetic). The **gamma flip level** is the single most important transference marker options give you.

**Released kinetic energy is visible in flow urgency (the tick footprint):**
- **Trade-size & aggressor side** — large prints lifting the ask vs hitting the bid. The option tick tape *is* an order-flow footprint; bucket trades by price-vs-NBBO to infer buy/sell aggression (the quote ticks give you the NBBO to classify against).
- **Volume-to-OI ratio** — volume ≫ OI means *new* positioning today (kinetic initiation); volume ≪ OI means existing holders, quiet (potential still stored).
- **IV expansion rate** — IV ripping higher intrabar = energy releasing; IV crushing while price moves = the move is *over*, energy spent.
- **Put/call volume & premium ratios** — directional conviction and its acceleration.

**The transference period itself** — the 2×2's ambiguous middle — is where you combine standing structure (OI/greeks/skew) with flow urgency (tick footprint/IV velocity) on the **same contracts**, second by second, during the window your VOB/footprint detectors flag on the underlying. That cross-product — *standing structure changing under flow pressure* — is the chemical reaction. It is why you need both the snapshot layer (structure) and the tick layer (flow), and why your 1,000 live slots must sit on exactly the contracts where the underlying is at a VOB decision point.

---

## 5. Storage — Parquet + DuckDB + Polars (decided)

Do not invent a new stack. Use ours:

- **Archive format: Parquet**, partitioned `asset=options/underlying=<SYM>/date=<YYYY-MM-DD>/`. S3 ships CSV.gz; land it, convert to Parquet once. Parquet is columnar → you scan only the columns a feature needs, with predicate pushdown on date/strike.
- **Query engine: DuckDB.** SQL directly over the Parquet tree, zero-copy, handles the full multi-TB archive on a single Mac, no server. This is where you build feature tables and run cross-sectional scans.
- **In-memory feature engineering: Polars** (Arrow-backed, lazy, far faster than pandas). DuckDB ↔ Polars share Arrow buffers with no serialization cost — query in DuckDB, hand the frame to Polars, compute greeks-derived features, write back to the Parquet feature store.
- **Pipeline:** `S3 CSV.gz → Parquet (partitioned) → DuckDB views → Polars transforms → Parquet feature store → detectors.` The Massive MCP (`call_api … store_as` + `query_data`) is fine for interactive exploration and prototyping; the production archive path is the Parquet/DuckDB pipeline above.

---

## 6. Bottom line for you

- The 1,000-cap is a **live attention budget**. Spend it on VOB-candidate underlyings × NTM strikes × front expiries, rotated pre-market.
- **Everything else is unlimited:** REST chain snapshots (whole-market structure scan, with greeks/IV/OI), and the full OPRA history in S3 (day/minute/trades since 2014; quotes since 2022).
- **Download now:** option `day_aggs` + `minute_aggs` + `trades_v1` in full (~110 GB total, sequential). Leave the 98 TB `quotes_v1` for targeted pulls.
- **Your edge target:** build detectors that read standing structure (OI/greeks/skew) against flow urgency (tick footprint/IV velocity) to classify each underlying signal into the 2×2 — potential vs kinetic, bullish vs bearish — during the transference window.

The full field-by-field anatomy, with real rows pulled live from Massive today, is in the P.S.

---

## P.S. — Full anatomy & physiology of the options data (real samples, pulled live 2026-05-31)

### A. The contract identifier (OCC symbol) — decode it first

`O:NVDA260601C00155000`

| Segment | Value | Meaning |
|---|---|---|
| `O:` | — | options namespace prefix (Massive/Polygon convention) |
| `NVDA` | NVDA | underlying root |
| `260601` | 2026-06-01 | expiration `YYMMDD` |
| `C` | Call | `C`=call, `P`=put |
| `00155000` | 155.000 | strike × 1000, zero-padded to 8 digits → divide by 1000 |

Every endpoint and every flat file keys on this string. It is your join key across all resolutions.

### B. TICK — trades  (`/v3/trades/{contract}`, WS `T.<contract>`)
Real rows (NVDA C155, descending time):
```
conditions,exchange,id,participant_timestamp,price,sequence_number,sip_timestamp,size,decimal_size
[233],302,,1780078288334000000,60.92,0,1780078288334000000,1,1.0
[233],302,,1780078085353000000,60.64,0,1780078085353000000,1,1.0
```
| Field | Type | Meaning |
|---|---|---|
| `conditions` | int array (REST) / single int (S3) | trade condition codes (e.g. 233, 209, 227) — determines whether a print is "regular", late, or a special-settlement; **for tick-bar / footprint purposes this is the filter that decides which prints count** |
| `exchange` | int | OPRA participant exchange ID (300-range, e.g. 302) |
| `price` | float | execution price (per share; ×100 = per contract) |
| `size` / `decimal_size` | int / float | contracts traded; post-2026-02-23 `decimal_size` is the precise float |
| `sip_timestamp` | int64 ns | consolidated tape timestamp, **nanoseconds** |
| `id`, `participant_timestamp`, `sequence_number` | often empty for options | present/rich for stocks; sparse here |

### C. TICK — quotes / NBBO  (`/v3/quotes/{contract}`, WS `Q.<contract>`)
Real rows:
```
ask_exchange,ask_price,ask_size,bid_exchange,bid_price,bid_size,sequence_number,sip_timestamp
315,61,1,322,52.3,1,1284995807,1780084799152806850
312,60.75,1,322,52.3,2,1284871096,1780084798803220311
```
| Field | Meaning |
|---|---|
| `bid_price`/`ask_price` | best bid/offer at that instant |
| `bid_size`/`ask_size` | size at the BBO (in contracts) |
| `bid_exchange`/`ask_exchange` | which OPRA venue holds the BBO |
| `sequence_number` | ordering within the feed |
| `sip_timestamp` | ns timestamp |
Use the quote stream to classify each trade as buy/sell-aggressor (trade price vs prevailing NBBO) — this is how you turn the raw option tape into an **order-flow footprint**.

### D. MINUTE / DAILY aggregates  (`/v2/aggs/...`, WS `A.`/`AM.`)
Real minute rows (NVDA C155, 2026-05-29):
```
v,vw,o,c,h,l,t,n
1,60.51,60.51,60.51,60.51,60.51,1780062480000,1
2,60.24,60.22,60.26,60.26,60.22,1780069800000,2
```
Real daily rows:
```
v,vw,o,c,h,l,t,n
62,61.2232,60.51,60.92,62.06,60.22,1780027200000,62
128,59.1549,60.08,58.96,60.08,58.57,1779940800000,128
```
| Field | Meaning |
|---|---|
| `v` | volume (contracts) |
| `vw` | volume-weighted average price (VWAP) |
| `o,c,h,l` | open/close/high/low |
| `t` | window start, **epoch milliseconds** (note: aggs are ms; ticks are ns) |
| `n` | number of trades in the bar |

### E. CHAIN SNAPSHOT — the analytical layer  (`/v3/snapshot/options/{underlying}`)
Real row (NVDA C212.5, at-the-money — greeks present):
```
details_strike_price=212.5  details_contract_type=call  details_expiration_date=2026-06-01
greeks_delta=0.5050  greeks_gamma=0.0749  greeks_theta=-1.2180  greeks_vega=0.0423
implied_volatility=0.5105  open_interest=4568  day_volume=14210  day_vwap=4.3814
last_quote_bid=2.02  last_quote_ask=2.30  last_trade_price=2.27
underlying_asset_price=212.4801  break_even_price=214.66
```
| Group | Fields | Meaning |
|---|---|---|
| `details_*` | contract_type, exercise_style, expiration_date, shares_per_contract (100), strike_price, ticker | static contract spec |
| `greeks_*` | delta, gamma, theta, vega | risk sensitivities — **gamma drives the dealer-hedging / transference logic** |
| `implied_volatility` | — | the IV the market is pricing; build skew & term structure from the chain |
| `open_interest` | — | standing positioning (stored potential energy) |
| `day_*` | open/close/high/low/volume/vwap/change | session stats per contract |
| `last_quote_*`, `last_trade_*` | NBBO + last print | current micro-state |
| `underlying_asset_*` | price, ticker, change_to_break_even | spot context for the whole chain |
**Note:** greeks/IV are **omitted for deep-ITM or untradeable contracts** (no solvable IV) — expect nulls there; they populate near and out of the money where you actually work.

### F. S3 flat-file schemas (CSV.gz, one file per UTC date, partition by date)
```
day_aggs_v1   : ticker,volume,open,close,high,low,window_start,transactions
minute_aggs_v1: ticker,volume,open,close,high,low,window_start,transactions
trades_v1     : ticker,conditions,correction,exchange,price,sip_timestamp,size
quotes_v1     : ticker,ask_exchange,ask_price,ask_size,bid_exchange,bid_price,bid_size,sequence_number,sip_timestamp
```
Flat-file `trades` differ from REST: a **single integer** `conditions` (not an array), a `correction` column, and **no** `id`/`participant_timestamp`/`sequence_number`/`tape`. `window_start` in aggs is **nanoseconds** in the flat files (REST aggs use ms) — normalize on ingest. **Schema break 2026-02-23:** `size`/`volume` are now decimals; new precision columns `decimal_size`, `dv`, `dav`, `decimal_volume` arrive as strings — cast explicitly.

### G. How to pull from Massive
- **REST:** `GET https://api.massive.com<path>`, header `Authorization: Bearer $MASSIVE_API_KEY`. Cursor pagination (`next_url`/`cursor`). Operators as `field.gte`/`field.lte` (e.g. `strike_price.gte=210`). Unlimited rate on Advanced.
- **WebSocket:** `wss://socket.massive.com/options` → `{"action":"auth","params":"$KEY"}` → `{"action":"subscribe","params":"A.O:NVDA260601C00212500,..."}` — ≤1,000 contracts per connection.
- **S3:** `aws s3 ... --endpoint-url https://files.massive.com` with `MASSIVE_S3_ACCESS_KEY_ID`/`SECRET`. Prefix `s3://flatfiles/us_options_opra/<type>_v1/YYYY/MM/YYYY-MM-DD.csv.gz`. **Sequential downloads only** (parallel → 429).

### H. Tagging / labeling convention for the archive
Land everything keyed by the OCC ticker; derive and store as columns: `underlying`, `expiration_date`, `contract_type`, `strike`, `dte` (days-to-expiry), `moneyness` (strike/spot). Partition Parquet by `underlying` + `date`. Tag each row's source resolution (`tick|sec|min|day|snapshot`) so detectors never mix resolutions accidentally. Timestamps: store everything in **nanosecond epoch UTC**, carry a derived `America/New_York` session column for RTH/auction logic.
