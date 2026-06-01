# WhaleWisdom API Access Proof -- Recon Report

**Date:** 2026-05-26
**Status:** BLOCKED -- Server unreachable from this network
**Source:** API docs retrieved from Wayback Machine (cached 2025-01-03)

---

## CRITICAL FINDING: Server Unreachable

whalewisdom.com (IP: 174.129.12.150, AWS EC2 us-east-1) is **completely unreachable** from this network.
Every connection attempt -- HTTPS (443), HTTP (80), ICMP ping -- times out at the TCP level.
Traceroute dies after hop 5 (AT&T backbone at 32.130.19.159). Packets never reach AWS.

This is NOT an authentication issue -- the TCP handshake never completes.

### Diagnostics Performed

| Test | Result |
|------|--------|
| `curl -v https://whalewisdom.com` (port 443) | Timeout after 15s, no TCP connect |
| `curl -v http://whalewisdom.com` (port 80) | Timeout after 10s, no TCP connect |
| `ping -c 3 whalewisdom.com` | 100% packet loss |
| `traceroute whalewisdom.com` | Dies at hop 5 (AT&T backbone) |
| DNS resolution (Google 8.8.8.8, Cloudflare 1.1.1.1) | Resolves correctly to 174.129.12.150 |
| WebFetch (alternate network path) | Timeout after 60s |
| UpDownRadar + web search | Site reportedly UP for other users |

**Root cause:** Likely AT&T residential network blocking or routing issue to this specific EC2 IP.
The CloudFront CDN at d27mjrcvcy56qq.cloudfront.net (used for static assets) connects fine.

---

## CRITICAL FINDING: Authentication Method Mismatch

The credentials format provided:
```
shared_key=XXX&secret_key=XXX&command=COMMAND
```

**does NOT match** the actual WhaleWisdom API authentication spec. The API requires **HMAC-SHA1 signed requests**:

```
https://whalewisdom.com/shell/command.json?args=URL_ENCODED_JSON&api_shared_key=SHARED_KEY&api_sig=BASE64_HMAC_SHA1&timestamp=ISO8601
```

The secret key is NEVER sent as a query parameter. It is used locally to compute the HMAC-SHA1 signature.

### Correct Authentication Flow

1. Build a JSON `args` string: `{"command":"stock_lookup","symbol":"AAPL"}`
2. Get current UTC timestamp in ISO 8601: `2026-05-26T11:00:39Z`
3. Concatenate: `args + "\n" + timestamp`
4. Compute: `HMAC-SHA1(secret_key, args + "\n" + timestamp)`
5. Base64-encode the digest to get `api_sig`
6. URL-encode `args` and build the URL:
   ```
   https://whalewisdom.com/shell/command.json?args=URL_ENCODED_ARGS&api_shared_key=SHARED_KEY&api_sig=SIG&timestamp=TIMESTAMP
   ```

### Python3 Reference Implementation (from WhaleWisdom's own sample)

```python
import hashlib, hmac, time, base64
from urllib.parse import quote_plus

json_args = '{"command":"quarters"}'
secret_key = 'YOUR_SECRET_KEY'
shared_key = 'YOUR_SHARED_KEY'

formatted_args = quote_plus(json_args)
timenow = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

raw_args = json_args + '\n' + timenow
hmac_hash = hmac.new(secret_key.encode(), raw_args.encode(), hashlib.sha1).digest()
sig = base64.b64encode(hmac_hash).rstrip()

url = (f'https://whalewisdom.com/shell/command.json?'
       f'args={formatted_args}'
       f'&api_shared_key={shared_key}'
       f'&api_sig={sig.decode()}'
       f'&timestamp={timenow}')
```

### Three Authentication Methods (from docs)

1. **Session cookie** -- log in via browser, let cookie authenticate
2. **HMAC-SHA1 digital signature** -- the programmatic method (described above)
3. **Interactive Testing Shell** -- browser-based at `https://whalewisdom.com/shell/index`

---

## Complete API Command Reference

Source: Wayback Machine snapshot of `https://whalewisdom.com/shell/api_help` (2025-01-03)

The API has **8 documented commands** (2 more commented out / deprecated):

### 1. `quarters`

Lists all 13F filing dates in the database and their availability for your account.

| Key | Value | Type | Required | Description |
|-----|-------|------|----------|-------------|
| (none) | | | | No parameters needed |

**Output formats:** html, json, csv
**Example args:** `{"command":"quarters"}`
**Rate limit:** 20 requests/minute (global)

---

### 2. `stock_lookup`

Returns stocks matching a ticker symbol or name. Returns: stock id, name, symbol, status (active/delisted).

| Key | Value | Type | Required | Description |
|-----|-------|------|----------|-------------|
| name | NAME | string | name OR symbol required | Partial or complete name to search for |
| symbol | SYMBOL | string | name OR symbol required | Stock ticker symbol to search for |

**Output formats:** html, json, csv
**Example args:**
- `{"command":"stock_lookup", "name":"Apple Comp"}`
- `{"command":"stock_lookup", "symbol":"aapl"}`

**Response fields (expected):** stock_id, name, symbol, status

---

### 3. `filer_lookup`

Returns 13F filers matching search criteria. Max 1,000 records.

| Key | Value | Type | Required | Description |
|-----|-------|------|----------|-------------|
| name | NAME | string | at least one required | Partial or complete name |
| cik | CIK | string | at least one required | Central Index Key |
| id | ID | number | at least one required | Database ID of the filer |
| city | CITY | string | at least one required | City provided by filer |
| state | STATE | string | at least one required | State filer resides in |
| state_incorporation | STATE | string | at least one required | State of incorporation |
| business_phone | PHONE | string | at least one required | Business phone |
| irs_number | IRS# | string | at least one required | IRS number |
| offset | OFFSET | string | optional | Offset for pagination (>1000 records) |

**Output formats:** html, json, csv
**Example args:**
- `{"command":"filer_lookup", "name":"berkshire"}`
- `{"command":"filer_lookup", "cik":"0001067983"}`

**Response fields (expected):** filer_id, name, cik

---

### 4. `stock_comparison`

Quarterly comparison of 13F holders of a specific stock between two quarters.

| Key | Value | Type | Required | Description |
|-----|-------|------|----------|-------------|
| stockid | STOCK ID | numeric | required | ID of the stock (from stock_lookup) |
| q1id | QUARTER 1 ID | numeric | required | ID of first 13F filing quarter |
| q2id | QUARTER 2 ID | numeric | required | ID of second 13F filing quarter |
| order | ORDER BY | string | optional | filer_name, q1_shares, q2_shares, or percent_change |
| dir | DIRECTION | string | optional | ASC or DESC |

**Output formats:** html, json, csv
**Example args:**
- `{"command":"stock_comparison","stockid":3598,"q1id":39,"q2id":40}`
- `{"command":"stock_comparison","stockid":3598,"q1id":39,"q2id":40,"order":"q2_shares","dir":"DESC"}`

---

### 5. `holdings_comparison`

Compare a filer's 13F holdings between two quarters.

| Key | Value | Type | Required | Description |
|-----|-------|------|----------|-------------|
| filerid | FILER ID | numeric | required | ID of the filer |
| q1id | QUARTER 1 ID | numeric | required | First quarter to compare |
| q2id | QUARTER 2 ID | numeric | required | Second quarter to compare |
| order | ORDER BY | string | optional | stock, q2_market_value, q1_percent_of_portfolio, q2_percent_of_portfolio, q2_shares, q1_shares, q1_market_value, percent_change, absolute_change |
| dir | DIRECTION | string | optional | ASC or DESC |
| filter | FILTER | array of strings | optional | SHARES, CALL, PUT, or PRN |
| stockid | STOCK ID | numeric | optional | Restrict results to specific stock |

**Output formats:** html, json, csv
**Example args:**
- `{"command":"holdings_comparison","filerid":163,"q1id":39,"q2id":40}`
- `{"command":"holdings_comparison","filerid":163,"q1id":39,"q2id":40,"order":"q2_shares","dir":"DESC"}`
- `{"command":"holdings_comparison","filerid":163,"q1id":39,"q2id":40,"order":"q2_shares","filter":["CALL","PUT"]}`

---

### 6. `export`

Export entire 13F holdings history for a single filer. Standard subscribers limited to 50 filers/quarter.

| Key | Value | Type | Required | Description |
|-----|-------|------|----------|-------------|
| filer_id | FILER ID | numeric | required | ID of filer to export |
| quarters | [QUARTER_IDs] | array of numbers | required | Quarter IDs to export |
| output | OUTPUT ID | numeric | required | 1 = single CSV, 2 = separate CSVs per quarter |
| columns | [COLUMN_IDs] | array of numbers | required | See column list below |
| email | EMAIL | string | required | Email address to send export to |

**Export columns:**
| Col ID | Field |
|--------|-------|
| 1 | Filer Name |
| 2 | Stock Name |
| 3 | Stock Ticker |
| 4 | Quarter Date |
| 5 | Type of Security |
| 6 | Current Shares Held |
| 7 | Current Market Value |
| 8 | Previous Shares Held |
| 9 | Previous Market Value |
| 10 | Current % of Portfolio |
| 11 | Previous % of Portfolio |
| 12 | Current Rank |
| 13 | Previous Rank |
| 14 | Change in Shares |
| 15 | Type of Change |
| 16 | Sector |
| 17 | stock_id |
| 18 | source |

**Output formats:** html, json, csv
**Example args:**
```json
{"command":"export","quarters":[40,41,42],"columns":[1,2,3,4,5,6,7,8],"filer_id":349,"output":1,"email":"testemail@test.com"}
```

---

### 7. `holdings`

Output all holdings for a filer or list of filers. Data from 13F filings, optionally augmented with 13D/G.

| Key | Value | Type | Required | Description |
|-----|-------|------|----------|-------------|
| filer_ids | [FILER_IDs] | numeric array | required | IDs of filers to include |
| quarter_ids | [QUARTER_IDs] | numeric array | optional | Leave blank for most recent |
| stock_ids | [STOCK_IDs] | numeric array | optional | Restrict to specific stocks |
| all_quarters | 1 or 0 | number | optional | 1 = retrieve all available quarters |
| sort | ORDER BY | string | optional | Column to sort by |
| dir | DIRECTION | string | optional | ASC or DESC |
| limit | LIMIT | number | optional | Limit number of results |
| include_13d | 1 or 0 | number | optional | 1 = augment with 13D/G filings |
| columns | [COLUMN_IDs] | array of numbers | optional | Leave blank for all |

**Holdings/Holders columns (shared):**
| Col ID | Field |
|--------|-------|
| 0 | filer_id |
| 1 | filer_name |
| 2 | stock_id |
| 3 | stock_name |
| 4 | stock_ticker |
| 5 | security_type |
| 6 | shares_change |
| 7 | position_change_type |
| 8 | current_ranking |
| 9 | previous_ranking |
| 10 | current_percent_of_portfolio |
| 11 | previous_percent_of_portfolio |
| 12 | current_mv (market value) |
| 13 | previous_mv |
| 14 | current_shares |
| 15 | previous_shares |
| 16 | source_date |
| 17 | source |
| 18 | sector |
| 19 | industry |
| 20 | % Ownership |
| 21 | filer_street_address |
| 22 | filer_city |
| 23 | filer_state |
| 24 | filer_zip_code |
| 25 | avg_price |
| 26 | percent_change |
| 27 | quarter_id_owned (quarter first owned by filer) |

**Output formats:** json, csv (NOT html)
**Example args:**
```json
{"command":"holdings","filer_ids":[349,2182],"include_13d":1}
```
(Retrieves holdings of Berkshire Hathaway [349] and Paulson & Co [2182])

---

### 8. `holders`

Output all holders for a stock or group of stocks. Same column structure as `holdings`.

| Key | Value | Type | Required | Description |
|-----|-------|------|----------|-------------|
| stock_ids | [STOCK_IDs] | numeric array | required | IDs of stocks |
| filer_ids | [FILER_IDs] | numeric array | optional | Restrict to specific filers |
| quarter_ids | [QUARTER_IDs] | numeric array | optional | Leave blank for most recent |
| all_quarters | 1 or 0 | number | optional | 1 = retrieve all available quarters |
| sort | ORDER BY | string | optional | Column to sort by |
| dir | DIRECTION | string | optional | ASC or DESC |
| limit | LIMIT | number | optional | Limit results |
| include_13d | 1 or 0 | number | optional | 1 = augment with 13D/G |
| hedge_funds_only | 1 or 0 | number | optional | 1 = only hedge funds |
| columns | [COLUMN_IDs] | array of numbers | optional | Leave blank for all (same as holdings) |

**Output formats:** json, csv
**Example args:**
```json
{"command":"holders","stock_ids":[195,411],"include_13d":1}
```
(Retrieves all holders of Apple [195] and Halliburton [411])

---

### 9. `filer_metadata` (undocumented -- found in Wayback Machine CDX index)

Likely returns metadata about a specific filer. Discovered from cached API call URL:
```
command.json?args={"command":"filer_metadata","filer_id":349}
```

| Key | Value | Type | Required | Description |
|-----|-------|------|----------|-------------|
| filer_id | FILER ID | numeric | required | ID of the filer |

---

### Deprecated/Commented-Out Commands (visible in HTML source)

These were in the docs HTML but commented out:
- `backtester` -- run backtests
- `backtester_status` -- check backtest status
- `backtester_saved` -- list saved backtests
- `backtester_load` -- load a saved backtest
- `backtester_delete` -- delete a saved backtest

---

## Commands NOT in the API

The following were mentioned in the user's request but do **NOT** exist in the documented WhaleWisdom REST API:

| Suggested Command | Status | Notes |
|-------------------|--------|-------|
| `filer_search` | DOES NOT EXIST | Correct command is `filer_lookup` |
| `insider_transactions` | DOES NOT EXIST | No insider data via API. Available only via web UI at `/dashboard2/other/form4_search` |
| `insider_summary` | DOES NOT EXIST | Same -- web UI only |

The WhaleWisdom API is **strictly 13F-focused**. Insider (Form 4) data is available on the website but NOT exposed through the REST API.

---

## Known Filer IDs (from docs examples)

| Filer ID | Name |
|----------|------|
| 163 | Appaloosa Management |
| 349 | Berkshire Hathaway |
| 2182 | Paulson & Co |

## Known Stock IDs (from docs examples)

| Stock ID | Name |
|----------|------|
| 195 | Apple (AAPL) |
| 411 | Halliburton |
| 3598 | E*Trade |

## Known Quarter IDs (from docs examples)

| Quarter ID | Date |
|------------|------|
| 1 | 3/31/2001 |
| 39 | 9/30/2010 |
| 40 | 12/31/2010 |
| 41 | 3/31/2011 |
| 42 | 6/30/2011 |

---

## Subscription Tiers

- **Non-subscribers:** Access to last 8 quarters of data
- **Standard subscribers:** Full quarterly access, limited to 50 filer exports/quarter
- **Rate limit:** 20 requests per minute (all tiers)

---

## Test Results Summary

### API Calls Attempted

| # | Command | Args | Result |
|---|---------|------|--------|
| 1 | quarters | `{"command":"quarters"}` | TCP TIMEOUT -- server unreachable |
| 2 | stock_lookup (AAPL) | `{"command":"stock_lookup","symbol":"aapl"}` | TCP TIMEOUT -- server unreachable |
| 3 | filer_lookup (Berkshire) | `{"command":"filer_lookup","name":"berkshire"}` | TCP TIMEOUT -- server unreachable |

All calls were properly constructed with HMAC-SHA1 signatures. The failure is at the network level, not the API level.

### Correct curl Command (for when server is reachable)

```bash
# Step 1: Generate the signed URL using Python
python3 -c "
import hashlib, hmac, time, base64
from urllib.parse import quote_plus

args = '{\"command\":\"stock_lookup\",\"symbol\":\"aapl\"}'
secret = 'nWn4SZ25ngk4xqvGL1gGUmMUy651lsbYJixXc3px'
shared = '1WCfcW0xi4tykIAwxuUw'
t = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
sig = base64.b64encode(hmac.new(secret.encode(), (args+'\n'+t).encode(), hashlib.sha1).digest()).decode().rstrip()
print(f'https://whalewisdom.com/shell/command.json?args={quote_plus(args)}&api_shared_key={shared}&api_sig={quote_plus(sig)}&timestamp={quote_plus(t)}')
"

# Step 2: Use the generated URL with curl
curl -s "PASTE_URL_HERE"
```

---

## Action Items

1. **Network fix required:** whalewisdom.com is unreachable from this network (AT&T residential in Houston, TX area). Try from a different network, VPN, or cloud server.
2. **Authentication fix required:** The user-provided credential format (`shared_key`/`secret_key` as direct params) is wrong. Must use HMAC-SHA1 signed requests with `api_shared_key` and `api_sig`.
3. **No insider data via API:** The `insider_transactions` and `insider_summary` commands do not exist. Insider data (Form 4) is web-UI-only on WhaleWisdom.
4. **When the server becomes reachable,** re-run this test suite using the Python HMAC signing script above.

---

## Sources

- WhaleWisdom API docs: Wayback Machine snapshot of `https://whalewisdom.com/shell/api_help` (2025-01-03T18:26:49Z)
- Python3 API sample: Wayback Machine snapshot of `https://whalewisdom.com/python3_api_sample.txt`
- Wayback CDX index: `http://web.archive.org/cdx/search/cdx?url=whalewisdom.com/shell/command*`
- WhaleWisdom API overview: `https://whalewisdom.com/help/api`
- PyPI package: `https://pypi.org/project/npd-whale-wisdom/`
