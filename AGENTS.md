# /Volumes/OWC Envoy Ultra/TradingDataSystem/ — HOT data drive

**Drive:** OWC Envoy Ultra 4 TB (HOT — live trading data only). Archive copy lives on the 208 TB OWC ThunderBay 8-bay.

## Before doing anything

Read in this order:
1. **`/Users/anishpatel/.claude/projects/-Users-anishpatel/memory/ANISH_HAS.md`** — master registry
2. **`/Users/anishpatel/code/anish/trading-data-system/KNOWN_SUBSCRIPTIONS.md`** — what feeds we pay for
3. **`/Users/anishpatel/code/anish/trading-data-system/CLAUDE.md`** — pipeline guide

## Layout

```
TradingDataSystem/
├── massive-flatfiles/   # S3 mirror of files.massive.com/flatfiles
├── massive-rest/        # REST-API pulls (snapshots, references, OHLCV)
├── massive-realtime/    # WebSocket capture (trades, quotes, aggs, NOI, etc.)
├── whalewisdom/         # 13F + Form 4 JSON, polled every 90d
└── logs/                # poller + WS-client logs
```

## Hard rules

- **NEVER write to `~/data/` or any boot-drive path.** This volume is the canonical hot store. If this drive is unmounted, the answer is "mount it" — never silently fall back.
- **Verify mount before any write:** `ls /Volumes/ | grep "OWC Envoy Ultra"` must return a result.
- **24/7 collectors** = launchd plists, not nohup. See the `persistent-collection` skill.
- **File naming:** `<source>/<asset_class>/<symbol>/<date>.<ext>` — e.g., `massive-realtime/stocks/NVDA/2026-05-19.parquet`

## Code that writes here

All pipeline code lives at `/Users/anishpatel/code/anish/trading-data-system/`. Don't edit code on the volume — it has no git.
