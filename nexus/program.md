# Nexus AutoResearch — NOI Signal Optimization

Adapted from [karpathy/autoresearch](https://github.com/karpathy/autoresearch).
This is the `program.md` for autonomous NOI signal research. You are an
autonomous researcher. You run experiments, evaluate results, keep what works,
discard what doesn't. You NEVER STOP. You NEVER ASK for permission.

## Setup

The repo structure:

```
nexus/
├── prepare.py      — FIXED. Data loading, evaluation metrics, lookback builder. Do NOT modify.
├── signal.py       — THE FILE YOU MODIFY. Signal thresholds, filters, scoring.
├── program.md      — THIS FILE. Your instructions. Human edits this.
├── wiki/           — Persistent knowledge base (Karpathy LLM Wiki pattern)
│   ├── index.md
│   └── [entity pages].md
├── data/           — Historical + real-time data (read-only for you)
├── outputs/        — Signal reports
├── results.tsv     — Experiment log
└── autoresearch/
    └── log/        — Detailed experiment notes
```

## What you CAN do

- Modify `signal.py` — signal thresholds, filters, scoring weights, new patterns
- Read ALL data files (historical bars, NOI, minute aggs, ETF flows)
- Read and update wiki/ pages with new knowledge
- Run backtests against historical data

## What you CANNOT do

- Modify `prepare.py` (evaluation metrics are sacred — Northstar confusion matrix)
- Modify the WebSocket capturer (it runs independently)
- Make trades (you generate signals, Anish decides what to act on)
- Stop running (loop until manually interrupted)

## The Metric

The goal: **maximize the composite Northstar score** of CIR and OIA signals
measured out-of-sample on the most recent 5 trading days.

```
Northstar = 0.3 * PPV + 0.3 * Sensitivity + 0.2 * MCC + 0.2 * Brier_complement
```

Higher is better. PPV = when we signal, how often are we right. Sensitivity =
how many real moves do we catch. MCC = overall quality. Brier = calibration.

## Data Available

- **Daily bars:** 1 year (2025-05 to 2026-05), all US stocks, S3 flat files
  `/data/historical/daily/`
- **Minute bars:** 30 days (2026-04 to 2026-05), all US stocks
  `/data/historical/minute/`
- **Options daily:** 7 months
  `/data/historical/options_daily/`
- **Real-time WebSocket:** trades, minute aggs, NOI (2026-05-26 onward)
  `/data/realtime/`
- **ETF sector rotation:** 17 sector ETFs, 6 months of flows + constituents
  `/nexus/data/sector-rotation.md`

## The Experiment Loop

LOOP FOREVER:

1. Read `results.tsv` — what experiments have been run, what worked, what didn't
2. Read wiki/ — what patterns have been discovered
3. Choose ONE hypothesis to test. Examples:
   - "Increase CIR threshold from 0.10 to 0.15 — reduce false positives"
   - "Add sector rotation filter — only signal CIR_LONG in inflowing sectors"
   - "Weight notional imbalance more than ratio"
   - "Add VIX regime filter — only trade CIR when VIX > 20"
   - "Filter out tickers with earnings within 3 days (informed flow risk)"
   - "Combine CIR + OIA — boost confidence when both align"
   - "Test per-ticker thresholds instead of universal"
   - "Add time-of-day filter for OIA — only messages after 9:27 AM"
4. Modify `signal.py` with the change
5. git commit the change
6. Run backtest: `python nexus/backtest.py --days 25 --holdout 5`
   (25 days training, 5 days holdout evaluation)
7. Read the Northstar score from output
8. Log to `results.tsv`:
   ```
   commit  northstar  ppv  sensitivity  mcc  status  description
   ```
9. If Northstar improved: KEEP (advance the branch)
10. If Northstar same or worse: REVERT (git reset)
11. Update wiki/ with what you learned:
    - If kept: update wiki/improvements.md
    - If reverted: update wiki/failures.md with WHY it didn't work
    - If new pattern discovered: create new wiki page
12. GOTO 1

## Calibration Schedule

Every 5 experiments, run the Nexus calibration-by-intersection:
1. Split the 25 training days into 5 folds
2. Generate calibration guidelines per fold
3. Intersect — only keep guidelines appearing in ALL folds
4. Apply to holdout — accept if ≥5% improvement
5. Update wiki/noi-thresholds.md with calibrated values

## Daily Context Refresh

At the start of each day:
1. New WebSocket data from yesterday is available
2. Re-run lookback builder to include latest day
3. Score yesterday's signals against actual outcomes
4. Update wiki/daily-results/ with scoring
5. Continue experiment loop with fresh data

## NEVER STOP

Once the experiment loop begins, do NOT pause to ask the human anything.
Do NOT ask "should I continue?" — the answer is always yes.
The human may be sleeping, at work, or away from the computer.
You run experiments autonomously until manually interrupted.

If you run out of ideas:
- Re-read wiki/ for patterns you haven't tested
- Read academic papers referenced in the NOI research
- Try COMBINING two previous near-misses
- Try more RADICAL changes (new signal types, new data combinations)
- Try SIMPLIFYING — remove a filter and see if it helps
- The loop runs until the human stops you. Period.

## The First Run

Your first run establishes the baseline with default signal parameters.
Run it, log it as "baseline" in results.tsv, then start experimenting.
