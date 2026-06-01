# Live Data Capture Analysis — 2026-05-26

**Capture window (initial):** 08:56 - 09:09 ET (pre-open auction, ~13 minutes)
**Analysis timestamp:** 2026-05-26 ~09:10 ET

---

## 1. NYSE Order Imbalance (NOI)

### Volume
- **44,006 messages** across 13 parquet files (flushed every ~60s)
- **2,412 unique tickers** on NYSE
- ~56 messages/sec throughput
- Rows per file: 1,616 - 7,291 (avg 3,385)

### Schema (Polygon NOI WebSocket)
| Field | Meaning | Type |
|-------|---------|------|
| `ev` | Event type (always "NOI") | str |
| `T` | Ticker symbol | str |
| `t` | SIP timestamp (nanoseconds) | int64 |
| `at` | Auction time (sec from midnight; 930 = 9:30 AM ET) | int64 |
| `i` | Sequence / imbalance indicator | int64 |
| `a` | Auction type: M=Open, C=Close, H=Halt | str |
| `x` | Exchange ID (10 = NYSE) | int64 |
| `o` | Order imbalance qty (+ = buy side, - = sell side) | int64 |
| `p` | Paired quantity (matched shares) | int64 |
| `b` | Book clearing price (indicative match price) | float64 |
| `r` | Reference price (last sale / prior close) | float64 |
| `_captured_at` | Our capture timestamp (ms) | int64 |

### Imbalance Side Distribution
| Side | Count | Pct |
|------|-------|-----|
| BUY | 24,171 | 54.9% |
| SELL | 18,511 | 42.1% |
| NEUTRAL | 1,324 | 3.0% |

Net market bias: **+12.8% skew toward buy side** in this pre-open window.

### Top 10 Largest Imbalances (by absolute share quantity)
| Ticker | Max Imbalance | Side | Avg Imbalance | Avg Paired | Msgs |
|--------|--------------|------|---------------|------------|------|
| RDW | 1,191,038 | BUY | +1,128,093 | 277,187 | 467 |
| NOK | 1,146,108 | BUY | +1,017,465 | 239,371 | 562 |
| BB | 836,857 | BUY | +716,337 | 113,331 | 237 |
| F | 461,793 | SELL | -432,795 | 195,833 | 136 |
| TE | 240,450 | BUY | +222,147 | 91,021 | 123 |
| SPCE | 237,007 | BUY | +219,655 | 80,295 | 111 |
| KOS | 219,758 | SELL | -208,217 | 17,465 | 25 |
| UAMY | 215,986 | BUY | +202,305 | 34,516 | 36 |
| LYG | 198,962 | BUY | +170,673 | 45,841 | 101 |
| SMR | 191,348 | BUY | +177,873 | 116,007 | 186 |

### Top 10 Notional Imbalances (price x quantity)
| Ticker | Notional $ | Qty | Price |
|--------|-----------|-----|-------|
| TSM | $80,978,796 | 191,290 | $423.33 |
| VRT | $41,222,625 | 109,927 | $375.00 |
| APH | $27,559,754 | 176,326 | $156.30 |
| RDW | $24,892,694 | 1,191,038 | $20.90 |
| NOK | $22,922,160 | 1,146,108 | $20.00 |
| IBM | $20,127,450 | 76,676 | $262.20 |
| SGOV | $18,358,346 | 182,416 | $100.64 |
| GLW | $15,738,903 | 78,303 | $201.00 |
| NOW | $15,691,336 | 146,648 | $106.00 |
| SNOW | $14,378,299 | 103,441 | $159.00 |

### Auction Types
- **M (Market Open):** 44,005 (100.0%) — pre-open auction imbalances
- **H (Halt):** 1 (0.0%)
- No Close (C) yet — market hasn't closed

### Persistent Imbalance Patterns

**100% BUY side (all messages):**
NOK (562 msgs), RDW (467), STM (432), SAP (379), RIO (361), HSBC (359), QBTS (327), IONQ (319), OKLO (282), TSM (266), VRT (262), NOW (253), GSK (243), BB (237), ING (234)

**100% SELL side (all messages):**
AON (568 msgs), BP (477), EQNR (393), NVS (325), E (244), COF (191), RACE (157), XOM (154), PFE (151), JPM (150), BRK.B (148), HE (141), UBER (138)

---

## 2. Trades

### Volume
- **393,570 trades** across 13 parquet files
- **3,950 unique tickers**
- ~502 trades/sec throughput
- Time range: 12:56-13:09 UTC (08:56-09:09 ET)

### Schema (Polygon Trades WebSocket)
| Field | Meaning | Type |
|-------|---------|------|
| `ev` | Event type ("T" = trade) | str |
| `sym` | Ticker symbol | str |
| `i` | Trade ID | str |
| `x` | Exchange ID | int64 |
| `p` | Price | float64 |
| `s` | Size (shares) | int64 |
| `c` | Conditions (array of int codes) | object |
| `t` | SIP timestamp (ms) | int64 |
| `pt` | Participant timestamp | float64 |
| `q` | Sequence number | int64 |
| `z` | Tape (1=A, 2=B, 3=C) | int64 |
| `trfi` | TRF ID | float64 |
| `trft` | TRF timestamp | float64 |
| `ds` | Data source | str |
| `_captured_at` | Our capture timestamp (ms) | int64 |

### Top Traded Tickers
| Ticker | Trades |
|--------|--------|
| YMAT | 41,818 |
| NCRA | 25,190 |
| CODX | 17,200 |
| SOXL | 10,124 |
| OTLK | 9,529 |
| MU | 8,120 |
| RGTI | 8,117 |
| IONQ | 7,813 |
| UFG | 7,743 |
| UZX | 7,434 |
| NVDA | 5,887 |

- Price range: $0.0092 - $8,475.00
- Size range: 0 - 1,500,000 shares (avg 199)

---

## 3. Minute Aggregates

### Volume
- **8,248 bars** across 13 parquet files
- **2,145 unique tickers**
- Time range: 12:56-13:08 UTC (08:56-09:08 ET)
- 0 duplicate (ticker, time) rows

### Schema (Polygon Minute Aggs WebSocket)
| Field | Meaning | Type |
|-------|---------|------|
| `ev` | Event type ("AM" = aggregate minute) | str |
| `sym` | Ticker symbol | str |
| `v` | Volume (shares in bar) | int64 |
| `av` | Accumulated volume (session total) | int64 |
| `vw` | VWAP for bar | float64 |
| `o` | Open | float64 |
| `c` | Close | float64 |
| `h` | High | float64 |
| `l` | Low | float64 |
| `a` | Day VWAP (accumulated) | float64 |
| `z` | Tape | int64 |
| `s` | Bar start timestamp (ms) | int64 |
| `e` | Bar end timestamp (ms) | int64 |
| `dv` | Dollar volume | str |
| `dav` | Accumulated dollar volume | str |
| `otc` | OTC flag | object |

### Coverage
- Max bars per ticker: 13 (full coverage for ~13 minutes of data)
- Tickers with full 13-bar coverage include: SLV, NIO, NCRA, NFLX, TQQQ, VRT, IONQ

---

## 4. Data Health Summary

| Stream | Messages | Tickers | Throughput | Files |
|--------|----------|---------|------------|-------|
| NOI | 44,006 | 2,412 | 56/sec | 13 |
| Trades | 393,570 | 3,950 | 502/sec | 13 |
| Minute Aggs | 8,248 | 2,145 | ~10/sec | 13 |

**Total messages captured: 445,824**

All three WebSocket streams are flowing correctly. Parquet files are flushing on a ~60-second cadence. No gaps detected in the timestamp sequence.

---

## 5. Follow-up Analysis (T+5 min)

*Will be appended after 5 minutes of additional accumulation.*
