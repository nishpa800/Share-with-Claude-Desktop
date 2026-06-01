# Massive.com S3 Flat Files -- Access Proof & Inventory

**Date tested:** 2026-05-26
**Endpoint:** `https://files.massive.com`
**Bucket:** `flatfiles`
**Auth:** S3-compatible (Access Key ID + Secret Access Key)
**AWS CLI command pattern:**
```bash
AWS_ACCESS_KEY_ID=fb3928e4-bcee-445a-8e08-6c258055801d \
AWS_SECRET_ACCESS_KEY=YoNn293OnaeaeLNGxADx2kL46nvtsCXB \
aws s3 ls s3://flatfiles/ --endpoint-url https://files.massive.com
```

---

## SUBSCRIPTION BOUNDARIES (Critical Finding)

| Prefix | List (browse) | Download (GET) | Status |
|--------|:---:|:---:|--------|
| `us_stocks_sip/` | OK | OK | **FULL ACCESS** |
| `us_options_opra/` | OK | OK | **FULL ACCESS** |
| `global_crypto/` | OK | 403 Forbidden | List-only |
| `global_forex/` | OK | 403 Forbidden | List-only |
| `us_futures_cbot/` | OK | 403 Forbidden | List-only |
| `us_futures_cme/` | OK | 403 Forbidden | List-only |
| `us_futures_comex/` | OK | 403 Forbidden | List-only |
| `us_futures_nymex/` | OK | 403 Forbidden | List-only |
| `us_indices/` | OK | 403 Forbidden | List-only |

**Bottom line:** You can download from `us_stocks_sip` and `us_options_opra` only. All other prefixes return 403 on GET/HEAD even though you can list their contents.

---

## TOP-LEVEL PREFIXES (9 total)

```
flatfiles/
  global_crypto/
  global_forex/
  us_futures_cbot/
  us_futures_cme/
  us_futures_comex/
  us_futures_nymex/
  us_indices/
  us_options_opra/
  us_stocks_sip/
```

---

## FILE FORMAT & NAMING CONVENTION

- **Format:** Gzip-compressed CSV (`.csv.gz`)
- **Organization:** `{prefix}/{data_type}/YYYY/MM/YYYY-MM-DD.csv.gz`
- **One file per trading day** across all tickers in that asset class
- **Sorted alphabetically by ticker** within each file
- **Timestamps:** Nanosecond Unix epoch (int64) in all timestamp columns

---

## DETAILED INVENTORY BY PREFIX

### 1. `us_stocks_sip/` -- FULL ACCESS

| Data Type | Date Range | Typical Daily Size (compressed) | Typical Daily Size (uncompressed) |
|-----------|-----------|--------------------------------|-----------------------------------|
| `day_aggs_v1/` | 2003 -- 2026 | ~300 KB | ~967 KB |
| `minute_aggs_v1/` | 2003 -- 2026 | ~27-30 MB | ~137 MB |
| `trades_v1/` | 2003 -- 2026 | ~3.0-3.7 GB | est. 15-20 GB |
| `quotes_v1/` | 2003 -- 2026 | ~6.1-10.5 GB | est. 30-60 GB |

**Schemas:**

**day_aggs_v1** (12,093 rows/day = all tickers):
```
ticker,volume,open,close,high,low,window_start,transactions
A,2036584.149027,115.030000,114.960000,116.360000,113.675000,1779422400000000000,34455
```

**minute_aggs_v1** (1,826,498 rows/day):
```
ticker,volume,open,close,high,low,window_start,transactions
A,28038.875816,115.030000,114.910000,115.030000,114.760000,1779456600000000000,125
```

**trades_v1** (hundreds of millions of rows/day):
```
ticker,conditions,correction,exchange,id,participant_timestamp,price,sequence_number,sip_timestamp,size,tape,trf_id,trf_timestamp
A,"12,37",0,4,52983525159748,1779427811494482943,114.790000,3478,1779436803799308985,4.000000,1,201,1779436803799271495
```
- `conditions`: comma-separated trade condition codes
- `exchange`: integer exchange ID
- `tape`: SIP tape (1=A, 2=B, 3=C)
- `trf_id` / `trf_timestamp`: Trade Reporting Facility fields
- `size`: fractional shares supported (decimal)

**quotes_v1** (NBBO, billions of rows/day):
```
ticker,ask_exchange,ask_price,ask_size,bid_exchange,bid_price,bid_size,conditions,indicators,participant_timestamp,sequence_number,sip_timestamp,tape,trf_timestamp
A,12,0.0,0,12,0.0,0,"1,81",,1779433493626456646,174,1779433493626915885,1,0
```
- S3 metadata tag: `entitlement-data-type: nbbo`
- `conditions`: comma-separated NBBO condition codes
- `indicators`: optional field

### 2. `us_options_opra/` -- FULL ACCESS

| Data Type | Date Range | Typical Daily Size (compressed) |
|-----------|-----------|--------------------------------|
| `day_aggs_v1/` | 2014 -- 2026 | ~3.9-4.3 MB |
| `minute_aggs_v1/` | 2014 -- 2026 | ~24-29 MB |
| `trades_v1/` | 2014 -- 2026 | ~62-78 MB |
| `quotes_v1/` | 2022 -- 2026 | **~106-172 GB** |

**Schemas:**

**day_aggs_v1** (364,438 rows/day = all option contracts):
```
ticker,volume,open,close,high,low,window_start,transactions
O:A260618C00100000,3,16.2,16.2,16.2,16.2,1779422400000000000,1
```
- Ticker format: `O:{underlying}{YYMMDD}{C|P}{strike*1000}` (OCC standard)
- Same columns as stocks day_aggs

**minute_aggs_v1:**
```
ticker,volume,open,close,high,low,window_start,transactions
O:A260618C00100000,3,16.2,16.2,16.2,16.2,1779458460000000000,1
```

**trades_v1** (simplified vs stocks -- fewer columns):
```
ticker,conditions,correction,exchange,price,sip_timestamp,size
O:A260618C00100000,227,0,309,16.2,1779458509681000000,3
```
- No `id`, no `participant_timestamp`, no `sequence_number`, no `tape`, no `trf_*`
- `exchange`: OPRA exchange IDs (300-range)
- `conditions`: single integer (not comma-separated like stocks)

**quotes_v1** (simplified vs stocks):
```
ticker,ask_exchange,ask_price,ask_size,bid_exchange,bid_price,bid_size,sequence_number,sip_timestamp
O:A260717C00060000,0,0,0,320,45.3,1,1446504,1779456601047390893
```
- No `conditions`, `indicators`, `participant_timestamp`, `tape`, `trf_timestamp`
- MASSIVE files: 106-172 GB compressed per day

### 3. `global_crypto/` -- LIST ONLY (403 on download)

| Data Type | Date Range | Typical Daily Size (compressed) |
|-----------|-----------|--------------------------------|
| `day_aggs_v1/` | 2010 -- 2026 | ~12 KB |
| `minute_aggs_v1/` | 2010 -- 2026 | ~2.1-2.4 MB |
| `trades_v1/` | 2010 -- 2026 | ~31-39 MB |

No `quotes_v1` for crypto. No `session_aggs_v1`.

### 4. `global_forex/` -- LIST ONLY (403 on download)

| Data Type | Date Range | Typical Daily Size (compressed) |
|-----------|-----------|--------------------------------|
| `day_aggs_v1/` | 2009 -- 2026 | ~29-34 KB |
| `minute_aggs_v1/` | 2009 -- 2026 | ~1.5-16 MB |
| `quotes_v1/` | 2009 -- 2026 | ~17-354 MB |

No `trades_v1` for forex. No `session_aggs_v1`.

### 5. `us_futures_cbot/` -- LIST ONLY (403 on download)

| Data Type | Date Range | Typical Daily Size (compressed) |
|-----------|-----------|--------------------------------|
| `trades_v1/` | 2017 -- 2026 | ~13-16 MB |
| `quotes_v1/` | 2017 -- 2026 | ~698 MB |
| `minute_aggs_v1/` | 2017 -- 2026 | ~1.5 MB |
| `session_aggs_v1/` | 2017 -- 2026 | ~15-16 KB |

### 6. `us_futures_cme/` -- LIST ONLY (403 on download)

| Data Type | Date Range | Typical Daily Size (compressed) |
|-----------|-----------|--------------------------------|
| `trades_v1/` | 2017 -- 2026 | ~42-56 MB |
| `quotes_v1/` | 2017 -- 2026 | ~3.5-4.2 GB |
| `minute_aggs_v1/` | 2017 -- 2026 | ~1.5-1.7 MB |
| `session_aggs_v1/` | 2017 -- 2026 | ~22-23 KB |

### 7. `us_futures_comex/` -- LIST ONLY (403 on download)

| Data Type | Date Range | Typical Daily Size (compressed) |
|-----------|-----------|--------------------------------|
| `trades_v1/` | 2017 -- 2026 | ~5.9-7.2 MB |
| `quotes_v1/` | 2017 -- 2026 | ~193 MB |
| `minute_aggs_v1/` | 2017 -- 2026 | similar to CBOT |
| `session_aggs_v1/` | 2017 -- 2026 | similar to CBOT |

### 8. `us_futures_nymex/` -- LIST ONLY (403 on download)

| Data Type | Date Range | Typical Daily Size (compressed) |
|-----------|-----------|--------------------------------|
| `trades_v1/` | 2017 -- 2026 | ~14-18 MB |
| `quotes_v1/` | 2017 -- 2026 | ~1.4 GB |
| `minute_aggs_v1/` | 2017 -- 2026 | similar scale |
| `session_aggs_v1/` | 2017 -- 2026 | ~15-22 KB |

### 9. `us_indices/` -- LIST ONLY (403 on download)

| Data Type | Date Range | Typical Daily Size (compressed) |
|-----------|-----------|--------------------------------|
| `day_aggs_v1/` | 2023 -- 2026 | ~272-398 KB |
| `minute_aggs_v1/` | 2023 -- 2026 | ~101-149 MB |
| `values_v1/` | 2023 -- 2026 | ~2.1-2.8 GB |

Note: `us_indices` uses `values_v1` instead of `trades_v1`/`quotes_v1`.

---

## UNIQUE DATA TYPES BY ASSET CLASS

| Data Type | Stocks | Options | Crypto | Forex | Futures (all 4) | Indices |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|
| `day_aggs_v1` | X | X | X | X | -- | X |
| `minute_aggs_v1` | X | X | X | X | X | X |
| `trades_v1` | X | X | X | -- | X | -- |
| `quotes_v1` | X | X | -- | X | X | -- |
| `session_aggs_v1` | -- | -- | -- | -- | X | -- |
| `values_v1` | -- | -- | -- | -- | -- | X |

---

## S3 METADATA TAGS (from HEAD responses on accessible files)

| File | Metadata |
|------|----------|
| `us_stocks_sip/trades_v1` | `entitlement-data-type: trades` |
| `us_stocks_sip/quotes_v1` | `entitlement-data-type: nbbo` |
| `us_options_opra/trades_v1` | `compression-level: "9"` |
| `us_options_opra/quotes_v1` | `compression-level: "-1"` |
| `us_options_opra/minute_aggs_v1` | `compression-level: "9"` |

---

## STORAGE ESTIMATES (for downloadable data)

### us_stocks_sip (full history 2003-2026, ~24 years)

Assuming ~250 trading days/year:

| Data Type | Daily (compressed) | Annual | Full History |
|-----------|-------------------|--------|-------------|
| `day_aggs_v1` | ~310 KB | ~76 MB | ~1.8 GB |
| `minute_aggs_v1` | ~28 MB | ~6.9 GB | ~166 GB |
| `trades_v1` | ~3.4 GB | ~837 GB | ~20 TB |
| `quotes_v1` | ~8.0 GB | ~1.95 TB | ~47 TB |

### us_options_opra (2014-2026, ~13 years for most; quotes from 2022)

| Data Type | Daily (compressed) | Annual | Full History |
|-----------|-------------------|--------|-------------|
| `day_aggs_v1` | ~4 MB | ~980 MB | ~12.7 GB |
| `minute_aggs_v1` | ~27 MB | ~6.6 GB | ~86 GB |
| `trades_v1` | ~70 MB | ~17 GB | ~221 GB |
| `quotes_v1` | ~140 GB | ~34 TB | ~170 TB (from 2022) |

---

## DOWNLOAD COMMANDS (Ready to Use)

### Download one day of stock day aggs:
```bash
AWS_ACCESS_KEY_ID=fb3928e4-bcee-445a-8e08-6c258055801d \
AWS_SECRET_ACCESS_KEY=YoNn293OnaeaeLNGxADx2kL46nvtsCXB \
aws s3 cp s3://flatfiles/us_stocks_sip/day_aggs_v1/2026/05/2026-05-22.csv.gz \
  ./2026-05-22-day-aggs.csv.gz --endpoint-url https://files.massive.com
```

### Download a full month of stock minute aggs:
```bash
AWS_ACCESS_KEY_ID=fb3928e4-bcee-445a-8e08-6c258055801d \
AWS_SECRET_ACCESS_KEY=YoNn293OnaeaeLNGxADx2kL46nvtsCXB \
aws s3 cp s3://flatfiles/us_stocks_sip/minute_aggs_v1/2026/05/ \
  ./minute_aggs/2026/05/ --endpoint-url https://files.massive.com --recursive
```

### Sync all day aggs (all years):
```bash
AWS_ACCESS_KEY_ID=fb3928e4-bcee-445a-8e08-6c258055801d \
AWS_SECRET_ACCESS_KEY=YoNn293OnaeaeLNGxADx2kL46nvtsCXB \
aws s3 sync s3://flatfiles/us_stocks_sip/day_aggs_v1/ \
  ./day_aggs/ --endpoint-url https://files.massive.com
```

---

## SAMPLE DATA DOWNLOADED

File: `us_stocks_sip/day_aggs_v1/2026/05/2026-05-22.csv.gz`
- Compressed: 305.7 KB
- Uncompressed: 967 KB
- Rows: 12,093 (one per ticker)
- Successfully decompressed and read

---

## KEY OBSERVATIONS

1. **23 years of tick-level stock data** (2003-present) is available for download.
2. **13 years of options data** (2014-present) including trades and OHLCV.
3. **Options NBBO quotes** start from 2022 and are enormous (100+ GB/day compressed).
4. **All files are one-per-day across all tickers** -- not one-per-ticker. This means downloading a specific ticker requires downloading the entire day's file and filtering locally.
5. **Listing is universal** -- you can browse the entire bucket structure even for prefixes you cannot download from. This lets you see what would be available with a subscription upgrade.
6. **Volume column uses decimal precision** (fractional shares) -- `volume: 2036584.149027`, likely reflecting the 2026-02-23 schema change documented in community learnings.
7. **Nanosecond timestamps** throughout -- not milliseconds, not microseconds. Example: `1779422400000000000`.
8. **No Parquet files** -- everything is CSV + gzip. No columnar format available.
9. **Futures use `session_aggs_v1`** instead of `day_aggs_v1` -- reflecting futures session semantics.
10. **Indices use `values_v1`** instead of trades/quotes -- reflecting index calculation values rather than tradeable quotes.
