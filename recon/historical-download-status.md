# Historical Data Download Status

**Date:** 2026-05-27
**Source:** Massive.com S3 flat files (`s3://flatfiles` via `https://files.massive.com`)
**Subscription:** Stocks Advanced ($199/mo) + Options Advanced ($199/mo) — confirmed via KNOWN_SUBSCRIPTIONS.md
**Purpose:** Historical context for Nexus forecasting system

---

## Download Summary

| Dataset | Files | Size (compressed) | Date Range | Status |
|---|---|---|---|---|
| **Daily Aggregates (2025)** | 250 | 53 MB | 2025-01-02 to 2025-12-31 | COMPLETE |
| **Daily Aggregates (2026)** | 99 | 27 MB | 2026-01-02 to 2026-05-26 | COMPLETE |
| **Minute Aggregates (30d)** | 30 | 809 MB | 2026-04-14 to 2026-05-26 | COMPLETE |
| **Options Daily Aggs (6mo)** | 140 | 501 MB | 2025-11-03 to 2026-05-26 | COMPLETE |
| **TOTAL** | **519** | **1.4 GB** | — | **ALL COMPLETE** |

---

## File Locations

```
/Users/anishpatel/quant-brain/data/historical/
  daily/
    2025/  (250 files, 53 MB)  — 01/ through 12/
    2026/  (99 files, 27 MB)   — 01/ through 05/
  minute/
    (30 files, 809 MB) — flat directory, 2026-04-14.csv.gz through 2026-05-26.csv.gz
  options_daily/
    2025/  (11/, 12/)
    2026/  (01/ through 05/)
    (140 files total, 501 MB)
```

---

## Schema (verified from sample files)

### Daily Aggregates (`day_aggs_v1`)
```
ticker, volume, open, close, high, low, window_start, transactions
```
- window_start is nanosecond Unix timestamp
- ~10,870 tickers per day
- ~210 KB compressed per file

### Minute Aggregates (`minute_aggs_v1`)
```
ticker, volume, open, close, high, low, window_start, transactions
```
- Same schema as daily
- ~1.94M rows per day (all tickers x all minutes)
- ~27 MB compressed per file

### Options Daily Aggregates (`us_options_opra/day_aggs_v1`)
```
ticker, volume, open, close, high, low, window_start, transactions
```
- Ticker format: `O:<underlying><expiry><C|P><strike>` (e.g., `O:A260618C00080000`)
- ~370,450 option contracts per day
- ~3.6 MB compressed per file

---

## S3 Path Convention

```
s3://flatfiles/us_stocks_sip/day_aggs_v1/YYYY/MM/YYYY-MM-DD.csv.gz
s3://flatfiles/us_stocks_sip/minute_aggs_v1/YYYY/MM/YYYY-MM-DD.csv.gz
s3://flatfiles/us_options_opra/day_aggs_v1/YYYY/MM/YYYY-MM-DD.csv.gz
```

---

## Notes

- Initial parallel download hit 429 (Too Many Requests) rate limits from Massive S3. Resolved by running syncs sequentially.
- All files are gzip-compressed CSV. Use `gzcat` or `pandas.read_csv(path, compression='gzip')` to read.
- Daily aggs cover 349 trading days (250 in 2025 + 99 in 2026 YTD) = full 1-year lookback from 2025-01-02.
- Minute aggs cover exactly 30 trading days (2026-04-14 through 2026-05-26).
- Options daily aggs cover ~7 months (2025-11-03 through 2026-05-26).
