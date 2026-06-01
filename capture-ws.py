#!/usr/bin/env python3
"""
Real-time WebSocket capturer for Massive.com (Polygon.io)
Captures: Trades, Quotes, Minute Aggs, NOI (Order Imbalances) for watchlist tickers
Stores: Append-only Parquet files partitioned by date and channel

Usage:
    source /Users/anishpatel/quant-brain/.venv/bin/activate
    python capture-ws.py
"""

import json
import os
import sys
import time
import signal
import threading
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

import websocket
import pyarrow as pa
import pyarrow.parquet as pq

API_KEY = "YoNn293OnaeaeLNGxADx2kL46nvtsCXB"
WS_URL = "wss://socket.massive.com/stocks"
DATA_DIR = Path("/Users/anishpatel/quant-brain/data/realtime")
WATCHLIST_FILE = Path("/Users/anishpatel/quant-brain/watchlist.txt")
FLUSH_INTERVAL = 60  # flush to parquet every 60 seconds
MAX_BUFFER = 50000   # flush if buffer exceeds this many messages

# Channel subscriptions
# T = trades, Q = quotes, AM = minute aggs, NOI = order imbalances
CHANNELS = ["T", "AM", "NOI"]  # Q is very high volume, start without it

buffers = defaultdict(list)
msg_count = 0
last_flush = time.time()
running = True


def load_watchlist():
    if WATCHLIST_FILE.exists():
        tickers = [t.strip() for t in WATCHLIST_FILE.read_text().splitlines() if t.strip()]
        print(f"Loaded {len(tickers)} tickers from watchlist")
        return tickers
    print("WARNING: No watchlist file found, subscribing to all tickers (*)")
    return ["*"]


def build_subscriptions(tickers):
    subs = []
    for channel in CHANNELS:
        if channel == "NOI":
            subs.append("NOI.*")
        elif len(tickers) > 500:
            subs.append(f"{channel}.*")
        else:
            for t in tickers:
                subs.append(f"{channel}.{t}")
    return subs


def flush_buffers():
    global last_flush
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")

    for channel, messages in buffers.items():
        if not messages:
            continue

        outdir = DATA_DIR / channel / date_str
        outdir.mkdir(parents=True, exist_ok=True)

        timestamp = now.strftime("%H%M%S")
        outpath = outdir / f"{channel}_{date_str}_{timestamp}.parquet"

        try:
            table = pa.Table.from_pylist(messages)
            pq.write_table(table, str(outpath), compression="snappy")
            count = len(messages)
            print(f"  FLUSHED {channel}: {count} msgs -> {outpath.name}")
        except Exception as e:
            # fallback: save as JSON if parquet fails
            json_path = outdir / f"{channel}_{date_str}_{timestamp}.json"
            with open(json_path, "w") as f:
                json.dump(messages, f)
            print(f"  FLUSHED {channel}: {len(messages)} msgs -> {json_path.name} (JSON fallback: {e})")

    buffers.clear()
    last_flush = time.time()


def on_message(ws, message):
    global msg_count

    try:
        data = json.loads(message)
    except json.JSONDecodeError:
        return

    if isinstance(data, list):
        for item in data:
            process_item(item)
    elif isinstance(data, dict):
        if data.get("ev") == "status":
            status = data.get("status", "")
            msg = data.get("message", "")
            print(f"  STATUS: {status} — {msg}")
            return
        process_item(data)


def process_item(item):
    global msg_count

    ev = item.get("ev", "unknown")
    item["_captured_at"] = int(time.time() * 1000)

    if ev == "T":
        buffers["trades"].append(item)
    elif ev == "Q":
        buffers["quotes"].append(item)
    elif ev == "AM":
        buffers["minute_aggs"].append(item)
    elif ev == "NOI":
        buffers["noi"].append(item)
    else:
        buffers[ev].append(item)

    msg_count += 1

    total_buffered = sum(len(v) for v in buffers.values())
    elapsed = time.time() - last_flush

    if total_buffered >= MAX_BUFFER or elapsed >= FLUSH_INTERVAL:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Total msgs: {msg_count} | Flushing {total_buffered} buffered...")
        flush_buffers()


def on_error(ws, error):
    print(f"WS ERROR: {error}")


def on_close(ws, close_status_code, close_msg):
    print(f"WS CLOSED: {close_status_code} — {close_msg}")
    flush_buffers()


def on_open(ws):
    print("WS CONNECTED — authenticating...")

    ws.send(json.dumps({"action": "auth", "params": API_KEY}))
    time.sleep(1)

    tickers = load_watchlist()
    subs = build_subscriptions(tickers)

    # Subscribe in batches (websocket has message size limits)
    batch_size = 100
    for i in range(0, len(subs), batch_size):
        batch = ",".join(subs[i:i + batch_size])
        ws.send(json.dumps({"action": "subscribe", "params": batch}))
        print(f"  Subscribed batch {i // batch_size + 1}: {len(subs[i:i+batch_size])} channels")
        time.sleep(0.2)

    total = len(subs)
    print(f"\nSUBSCRIBED to {total} channels across {len(CHANNELS)} types")
    print(f"Channels: {', '.join(CHANNELS)}")
    print(f"Data dir: {DATA_DIR}")
    print(f"Flush every {FLUSH_INTERVAL}s or {MAX_BUFFER} msgs")
    print(f"Capturing... (Ctrl+C to stop)\n")


def signal_handler(sig, frame):
    global running
    print("\n\nSIGNAL received — flushing and shutting down...")
    running = False
    flush_buffers()
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("  MASSIVE.COM REAL-TIME WEBSOCKET CAPTURER")
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Channels: {', '.join(CHANNELS)}")
    print(f"  Data dir: {DATA_DIR}")
    print("=" * 60)

    while running:
        try:
            ws = websocket.WebSocketApp(
                WS_URL,
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close,
            )
            ws.run_forever(
                ping_interval=30,
                ping_timeout=10,
                reconnect=5,
            )
        except Exception as e:
            print(f"Connection error: {e}")

        if running:
            print("Reconnecting in 5 seconds...")
            time.sleep(5)


if __name__ == "__main__":
    main()
