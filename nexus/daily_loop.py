#!/usr/bin/env python3
"""
daily_loop.py — The autonomous daily loop.
Karpathy AutoResearch + Nexus + LLM Wiki.

Runs phases based on time of day:
  --phase premarket   (7:00 AM CT)  Score yesterday, calibrate, generate signals
  --phase open        (8:25 AM CT)  Monitor opening imbalance acceleration
  --phase postmarket  (3:15 PM CT)  Capture closing imbalances, generate tomorrow's signals
  --phase experiment  (8:00 PM CT)  AutoResearch loop — modify signal.py, backtest, keep/revert
  --phase full                      Run all phases sequentially
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

NEXUS_DIR = Path("/Users/anishpatel/quant-brain/nexus")
WIKI_DIR = NEXUS_DIR / "wiki"
OUTPUTS_DIR = NEXUS_DIR / "outputs"
RESULTS_TSV = NEXUS_DIR / "results.tsv"
VENV_PYTHON = "/Users/anishpatel/quant-brain/.venv/bin/python"


def premarket():
    """Score yesterday's signals, run calibration, generate today's report."""
    print("=" * 60)
    print("  PRE-MARKET PHASE — 7:00 AM CT")
    print("=" * 60)

    # 1. Score yesterday's signals
    print("\n[1/4] Scoring yesterday's signals against actual outcomes...")
    result = subprocess.run(
        [VENV_PYTHON, "nexus/backtest.py", "--days", "25", "--holdout", "1"],
        capture_output=True, text=True, cwd="/Users/anishpatel/quant-brain",
    )
    print(result.stdout[-500:] if result.stdout else "No output")
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr[-300:]}")

    # 2. Update wiki with results
    print("\n[2/4] Updating wiki with yesterday's results...")
    today = datetime.now().strftime("%Y-%m-%d")
    results_file = WIKI_DIR / "wiki" / "daily-results" / f"{today}.md"
    results_file.parent.mkdir(parents=True, exist_ok=True)
    results_file.write_text(f"# Daily Results — {today}\n\n{result.stdout}\n")
    print(f"  Written to {results_file}")

    # 3. Generate today's signal scan
    print("\n[3/4] Generating today's NOI signal scan...")
    scan_result = subprocess.run(
        [VENV_PYTHON, "nexus/pipeline.py", "--scan", "--top", "30", "--horizon", "5"],
        capture_output=True, text=True, cwd="/Users/anishpatel/quant-brain",
    )
    print(scan_result.stdout[-1000:] if scan_result.stdout else "No output")

    # 4. Generate morning report
    print("\n[4/4] Generating morning report...")
    report = f"""# Morning Report — {today}

## Yesterday's Score
{result.stdout if result.stdout else 'No backtest results available'}

## Today's Signals
{scan_result.stdout if scan_result.stdout else 'No signals generated'}

## Wiki Status
Pages: {len(list((WIKI_DIR / 'wiki').glob('*.md')))} entity pages
"""
    report_file = OUTPUTS_DIR / f"morning_report_{today}.md"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(report)
    print(f"  Morning report: {report_file}")


def opening():
    """Monitor opening imbalance acceleration signals."""
    print("=" * 60)
    print("  OPENING PHASE — 8:25 AM CT")
    print("=" * 60)
    print("  WebSocket capturer is running and capturing NOI messages.")
    print("  OIA signals will be scored post-hoc from captured data.")
    print("  (Real-time OIA alerting requires a separate streaming process)")


def postmarket():
    """Capture closing imbalances, generate tomorrow's signals."""
    print("=" * 60)
    print("  POST-MARKET PHASE — 3:15 PM CT")
    print("=" * 60)

    today = datetime.now().strftime("%Y-%m-%d")

    # Generate tomorrow's signals from today's closing NOI
    print("\n[1/2] Scanning today's closing imbalances...")
    result = subprocess.run(
        [VENV_PYTHON, "nexus/pipeline.py", "--scan", "--top", "30", "--horizon", "5"],
        capture_output=True, text=True, cwd="/Users/anishpatel/quant-brain",
    )
    print(result.stdout[-1000:] if result.stdout else "No output")

    # Update wiki
    print("\n[2/2] Updating wiki...")
    update_wiki_index()


def experiment():
    """AutoResearch loop — modify signal.py, backtest, keep/revert."""
    print("=" * 60)
    print("  EXPERIMENT PHASE — AutoResearch Loop")
    print("  Modifying signal.py, backtesting, keeping improvements")
    print("=" * 60)

    # Run baseline first
    print("\n[Baseline] Running current signal.py parameters...")
    result = subprocess.run(
        [VENV_PYTHON, "nexus/backtest.py", "--days", "20", "--holdout", "5"],
        capture_output=True, text=True, cwd="/Users/anishpatel/quant-brain",
    )
    print(result.stdout[-500:] if result.stdout else "No output")

    # Log baseline to results.tsv
    if not RESULTS_TSV.exists():
        RESULTS_TSV.write_text("timestamp\tnorthstar\tppv\tsensitivity\tmcc\tstatus\tdescription\n")

    now = datetime.now().isoformat()
    # Parse northstar from output
    for line in (result.stdout or "").split("\n"):
        if "NORTHSTAR SCORE:" in line:
            score = line.split(":")[-1].strip()
            with open(RESULTS_TSV, "a") as f:
                f.write(f"{now}\t{score}\t\t\t\tbaseline\tcurrent signal.py parameters\n")
            print(f"  Baseline Northstar: {score}")
            break

    print("\n  Experiment loop would continue here autonomously.")
    print("  (Full autonomous loop requires launching as a persistent agent)")


def update_wiki_index():
    """Rebuild wiki/index.md from all entity pages."""
    wiki_dir = WIKI_DIR / "wiki"
    wiki_dir.mkdir(parents=True, exist_ok=True)

    pages = sorted(wiki_dir.glob("*.md"))
    index_lines = ["# NOI Signal Research Wiki — Index\n"]
    index_lines.append(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    index_lines.append(f"Total pages: {len(pages)}\n")

    for p in pages:
        if p.name == "index.md":
            continue
        first_line = p.read_text().split("\n")[0].replace("#", "").strip()
        index_lines.append(f"- [[{p.stem}]] — {first_line}")

    (wiki_dir / "index.md").write_text("\n".join(index_lines))
    print(f"  Wiki index updated: {len(pages)} pages")


def main():
    parser = argparse.ArgumentParser(description="Nexus Daily Autonomous Loop")
    parser.add_argument("--phase", required=True,
                        choices=["premarket", "open", "postmarket", "experiment", "full"])
    args = parser.parse_args()

    if args.phase == "premarket":
        premarket()
    elif args.phase == "open":
        opening()
    elif args.phase == "postmarket":
        postmarket()
    elif args.phase == "experiment":
        experiment()
    elif args.phase == "full":
        premarket()
        opening()
        postmarket()
        experiment()


if __name__ == "__main__":
    main()
