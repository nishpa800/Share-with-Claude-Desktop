#!/usr/bin/env python3
"""
backtest.py — Run backtests for the autoresearch loop.

Loads historical data, generates signals using current signal.py parameters,
evaluates against actual price outcomes, reports Northstar score.

Usage:
    python nexus/backtest.py --days 25 --holdout 5
    python nexus/backtest.py --days 25 --holdout 5 --signal-type CIR
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from nexus.prepare import (
    load_daily_bars,
    load_noi,
    get_trading_days,
    evaluate_signals_against_outcomes,
    compute_northstar,
)
from nexus.signal import score_cir, CIR_HOLD_DAYS


def generate_cir_signals_for_date(date: str) -> list[dict]:
    """Generate CIR signals from NOI closing auction data for a single date."""
    noi = load_noi(date)
    if noi.empty:
        return []

    close_noi = noi[noi["a"] == "C"].copy()
    if close_noi.empty:
        return []

    last_close = close_noi.sort_values("t").groupby("T").last().reset_index()
    signals = []

    for _, row in last_close.iterrows():
        result = score_cir(
            imbalance=int(row["o"]),
            paired=int(row["p"]),
            book_price=float(row["b"]) if row["b"] != 0 else 0.01,
        )
        if result["signal"] != "NEUTRAL":
            signals.append({
                "ticker": row["T"],
                "date": date,
                "signal": result["signal"],
                "confidence": result["confidence"],
                "ratio": result.get("ratio", 0),
                "notional": result.get("notional", 0),
            })

    return signals


def run_backtest(total_days: int = 25, holdout_days: int = 5, signal_type: str = "CIR") -> dict:
    """
    Run backtest over total_days, evaluate on last holdout_days.
    Returns: dict with metrics and northstar score.
    """
    all_dates = get_trading_days(total_days + holdout_days + CIR_HOLD_DAYS)

    if len(all_dates) < total_days + holdout_days:
        print(f"WARNING: Only {len(all_dates)} dates available, need {total_days + holdout_days}")
        if len(all_dates) < 2:
            return {"error": "insufficient data", "northstar": 0.0}

    holdout_dates = all_dates[-holdout_days:]
    train_dates = all_dates[:total_days]
    eval_end = all_dates[-1]

    print(f"Train period: {train_dates[0]} to {train_dates[-1]} ({len(train_dates)} days)")
    print(f"Holdout period: {holdout_dates[0]} to {holdout_dates[-1]} ({len(holdout_dates)} days)")

    # Generate signals on holdout dates
    all_signals = []
    for date in holdout_dates:
        if signal_type == "CIR":
            day_signals = generate_cir_signals_for_date(date)
        else:
            day_signals = generate_cir_signals_for_date(date)
        all_signals.extend(day_signals)

    if not all_signals:
        print("No signals generated in holdout period.")
        return {"error": "no signals", "northstar": 0.0, "n_signals": 0}

    print(f"Generated {len(all_signals)} signals across holdout period")

    # Load daily bars for evaluation
    daily_bars = load_daily_bars(holdout_dates[0], eval_end)
    if daily_bars.empty:
        print("No daily bar data for evaluation period.")
        return {"error": "no price data", "northstar": 0.0}

    # Evaluate
    outcomes, metrics, northstar = evaluate_signals_against_outcomes(
        all_signals, daily_bars, hold_days=CIR_HOLD_DAYS,
    )

    # Print results
    print(f"\n{'='*60}")
    print(f"  BACKTEST RESULTS — {signal_type}")
    print(f"{'='*60}")
    print(f"  Signals generated: {metrics.get('total_signals', 0)}")
    print(f"  Positive signals:  {metrics.get('n_positive_signals', 0)}")
    print(f"  TP: {metrics.get('tp', 0)} | FP: {metrics.get('fp', 0)} | TN: {metrics.get('tn', 0)} | FN: {metrics.get('fn', 0)}")
    print(f"  PPV (Precision):   {metrics.get('ppv', 0):.4f}")
    print(f"  Sensitivity:       {metrics.get('sensitivity', 0):.4f}")
    print(f"  Specificity:       {metrics.get('specificity', 0):.4f}")
    print(f"  MCC:               {metrics.get('mcc', 0):.4f}")
    print(f"  Brier:             {metrics.get('brier', 0):.4f}")
    print(f"  F1:                {metrics.get('f1', 0):.4f}")
    print(f"{'─'*60}")
    print(f"  NORTHSTAR SCORE:   {northstar:.6f}")
    print(f"{'='*60}")

    # Count wins/losses
    wins = sum(1 for o in outcomes if o.get("direction_correct"))
    losses = sum(1 for o in outcomes if not o.get("direction_correct") and o.get("actual_return") is not None)
    avg_return = sum(o.get("actual_return", 0) for o in outcomes) / max(len(outcomes), 1)

    print(f"  Wins: {wins} | Losses: {losses} | Win Rate: {wins/max(wins+losses,1)*100:.1f}%")
    print(f"  Average Return: {avg_return*100:.3f}%")

    return {
        "northstar": northstar,
        "metrics": metrics,
        "n_signals": len(all_signals),
        "wins": wins,
        "losses": losses,
        "avg_return": round(avg_return, 6),
        "train_dates": train_dates,
        "holdout_dates": holdout_dates,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nexus Backtest")
    parser.add_argument("--days", type=int, default=25, help="Training days")
    parser.add_argument("--holdout", type=int, default=5, help="Holdout days for evaluation")
    parser.add_argument("--signal-type", type=str, default="CIR", help="Signal type to backtest")
    args = parser.parse_args()

    result = run_backtest(args.days, args.holdout, args.signal_type)

    outfile = Path("/Users/anishpatel/quant-brain/nexus/outputs") / f"backtest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    outfile.parent.mkdir(parents=True, exist_ok=True)
    with open(outfile, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\nResults saved to {outfile}")
