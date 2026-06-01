"""
prepare.py — FIXED. DO NOT MODIFY.

Data loading, evaluation metrics (Northstar), and lookback window builder.
This is the ground truth evaluation. The autoresearch agent cannot touch this.
"""

import math
import pyarrow.parquet as pq
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

DATA_DIR = Path("/Users/anishpatel/quant-brain/data")
HIST_DAILY = DATA_DIR / "historical" / "daily"
HIST_MINUTE = DATA_DIR / "historical" / "minute"
REALTIME = DATA_DIR / "realtime"


# ─────────────────────────────────────────────────────────────────
# Data Loading (historical + real-time)
# ─────────────────────────────────────────────────────────────────

def load_daily_bars(start_date: str, end_date: str) -> pd.DataFrame:
    """Load daily bars from S3 flat files for date range."""
    all_dfs = []
    for year_dir in sorted(HIST_DAILY.iterdir()):
        if not year_dir.is_dir():
            continue
        for month_dir in sorted(year_dir.iterdir()):
            if not month_dir.is_dir():
                continue
            for f in sorted(month_dir.glob("*.csv.gz")):
                date_str = f.stem.replace(".csv", "")
                if start_date <= date_str <= end_date:
                    try:
                        df = pd.read_csv(f, compression="gzip")
                        df["date"] = date_str
                        all_dfs.append(df)
                    except Exception:
                        pass
    if not all_dfs:
        return pd.DataFrame()
    return pd.concat(all_dfs, ignore_index=True)


def load_noi(date: str) -> pd.DataFrame:
    """Load NOI messages for a single date from WebSocket capture."""
    noi_dir = REALTIME / "noi" / date
    if not noi_dir.exists():
        return pd.DataFrame()
    dfs = []
    for f in sorted(noi_dir.glob("*.parquet")):
        try:
            dfs.append(pq.read_table(f).to_pandas())
        except Exception:
            pass
    if not dfs:
        return pd.DataFrame()
    return pd.concat(dfs, ignore_index=True)


def load_minute_bars_realtime(date: str) -> pd.DataFrame:
    """Load minute bars from WebSocket capture for a single date."""
    agg_dir = REALTIME / "minute_aggs" / date
    if not agg_dir.exists():
        return pd.DataFrame()
    dfs = []
    for f in sorted(agg_dir.glob("*.parquet")):
        try:
            dfs.append(pq.read_table(f).to_pandas())
        except Exception:
            pass
    if not dfs:
        return pd.DataFrame()
    return pd.concat(dfs, ignore_index=True)


def get_trading_days(n_days: int, end_date: str = None) -> list[str]:
    """Get the last n trading days from available data."""
    dates = set()
    for year_dir in HIST_DAILY.iterdir():
        if not year_dir.is_dir():
            continue
        for month_dir in year_dir.iterdir():
            if not month_dir.is_dir():
                continue
            for f in month_dir.glob("*.csv.gz"):
                d = f.stem.replace(".csv", "")
                if end_date is None or d <= end_date:
                    dates.add(d)

    noi_dir = REALTIME / "noi"
    if noi_dir.exists():
        for d in noi_dir.iterdir():
            if d.is_dir() and (end_date is None or d.name <= end_date):
                dates.add(d.name)

    return sorted(dates)[-n_days:]


# ─────────────────────────────────────────────────────────────────
# Evaluation Metrics — THE NORTHSTAR (do not modify)
# ─────────────────────────────────────────────────────────────────

def compute_confusion_matrix(signals: list[dict], outcomes: list[dict]) -> dict:
    """
    Compute full confusion matrix from signal/outcome pairs.

    Each signal: {"ticker": str, "date": str, "signal": str, "confidence": float}
    Each outcome: {"ticker": str, "date": str, "actual_return": float, "direction_correct": bool}
    """
    tp = fp = tn = fn = 0
    brier_sum = 0.0
    n_scored = 0

    for sig, out in zip(signals, outcomes):
        predicted_positive = sig["signal"] not in ("NEUTRAL", None, "")
        actual_positive = out.get("direction_correct", False)

        if predicted_positive and actual_positive:
            tp += 1
        elif predicted_positive and not actual_positive:
            fp += 1
        elif not predicted_positive and not actual_positive:
            tn += 1
        elif not predicted_positive and actual_positive:
            fn += 1

        if predicted_positive:
            actual_binary = 1.0 if actual_positive else 0.0
            brier_sum += (sig["confidence"] - actual_binary) ** 2
            n_scored += 1

    total = tp + fp + tn + fn
    if total == 0:
        return {"error": "no scored signals"}

    sensitivity = tp / max(tp + fn, 1)
    specificity = tn / max(tn + fp, 1)
    ppv = tp / max(tp + fp, 1)
    npv = tn / max(tn + fn, 1)
    accuracy = (tp + tn) / total
    balanced_accuracy = (sensitivity + specificity) / 2

    if (tp + fp) > 0 and (tp + fn) > 0 and (tn + fp) > 0 and (tn + fn) > 0:
        mcc_num = (tp * tn) - (fp * fn)
        mcc_den = math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
        mcc = mcc_num / mcc_den if mcc_den > 0 else 0.0
    else:
        mcc = 0.0

    brier = brier_sum / max(n_scored, 1)

    f1 = 2 * ppv * sensitivity / max(ppv + sensitivity, 1e-9)

    return {
        "tp": tp, "fp": fp, "tn": tn, "fn": fn,
        "sensitivity": round(sensitivity, 4),
        "specificity": round(specificity, 4),
        "ppv": round(ppv, 4),
        "npv": round(npv, 4),
        "accuracy": round(accuracy, 4),
        "balanced_accuracy": round(balanced_accuracy, 4),
        "f1": round(f1, 4),
        "mcc": round(mcc, 4),
        "brier": round(brier, 4),
        "total_signals": total,
        "n_positive_signals": tp + fp,
    }


def compute_northstar(metrics: dict) -> float:
    """
    Compute the composite Northstar score from confusion matrix metrics.
    This is THE metric the autoresearch loop optimizes.
    Higher is better. Range: 0.0 to 1.0.
    """
    from nexus.signal import (
        NORTHSTAR_PPV_WEIGHT,
        NORTHSTAR_SENSITIVITY_WEIGHT,
        NORTHSTAR_MCC_WEIGHT,
        NORTHSTAR_BRIER_WEIGHT,
    )

    ppv = metrics.get("ppv", 0)
    sensitivity = metrics.get("sensitivity", 0)
    mcc = (metrics.get("mcc", 0) + 1) / 2  # normalize MCC from [-1,1] to [0,1]
    brier_complement = 1.0 - metrics.get("brier", 1.0)  # lower brier is better

    northstar = (
        NORTHSTAR_PPV_WEIGHT * ppv
        + NORTHSTAR_SENSITIVITY_WEIGHT * sensitivity
        + NORTHSTAR_MCC_WEIGHT * mcc
        + NORTHSTAR_BRIER_WEIGHT * brier_complement
    )
    return round(northstar, 6)


def evaluate_signals_against_outcomes(
    signals: list[dict],
    daily_bars: pd.DataFrame,
    hold_days: int = 5,
) -> tuple[list[dict], dict, float]:
    """
    Full evaluation pipeline:
    1. Match signals to actual price outcomes
    2. Compute confusion matrix
    3. Compute Northstar score

    Returns: (outcomes, metrics, northstar)
    """
    tick_col = "ticker" if "ticker" in daily_bars.columns else "T"
    outcomes = []

    for sig in signals:
        ticker = sig["ticker"]
        sig_date = sig["date"]
        sig_type = sig["signal"]

        t_bars = daily_bars[daily_bars[tick_col] == ticker].copy()
        if t_bars.empty:
            outcomes.append({
                "ticker": ticker, "date": sig_date,
                "actual_return": 0.0, "direction_correct": False,
                "reason": "no price data",
            })
            continue

        t_bars = t_bars.sort_values("date")
        future_bars = t_bars[t_bars["date"] > sig_date].head(hold_days)

        if future_bars.empty:
            outcomes.append({
                "ticker": ticker, "date": sig_date,
                "actual_return": 0.0, "direction_correct": False,
                "reason": "no future bars",
            })
            continue

        entry_bar = t_bars[t_bars["date"] == sig_date]
        if entry_bar.empty:
            entry_price = future_bars.iloc[0]["open"]
        else:
            entry_price = float(entry_bar.iloc[0]["close"])

        exit_price = float(future_bars.iloc[-1]["close"])
        actual_return = (exit_price - entry_price) / entry_price if entry_price > 0 else 0.0

        if sig_type in ("CIR_LONG", "OIA_LONG"):
            direction_correct = actual_return > 0
        elif sig_type in ("CIR_SHORT", "OIA_SHORT"):
            direction_correct = actual_return < 0
        else:
            direction_correct = False

        outcomes.append({
            "ticker": ticker,
            "date": sig_date,
            "actual_return": round(actual_return, 6),
            "direction_correct": direction_correct,
            "entry_price": entry_price,
            "exit_price": exit_price,
        })

    metrics = compute_confusion_matrix(signals, outcomes)
    northstar = compute_northstar(metrics)

    return outcomes, metrics, northstar
