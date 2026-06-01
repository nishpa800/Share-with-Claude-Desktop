#!/usr/bin/env python3
"""
Nexus Pipeline Orchestrator
Runs the full 5-agent pipeline: Context → Macro/Micro → Synthesize → Calibrate
Adapted from arXiv 2605.14389v1 for NOI + stock forecasting.

Usage:
    source /Users/anishpatel/quant-brain/.venv/bin/activate
    python nexus/pipeline.py --ticker AA --horizon 5 --date 2026-05-26
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from nexus.data_prep import (
    build_context_window,
    build_noi_profile,
    build_minute_bars,
    build_multi_timeframe_bars,
    get_available_dates,
    get_tickers_with_noi,
)
from nexus.agents import (
    HISTORICAL_CONTEXT_AGENT,
    MACRO_REASONING_AGENT,
    MICRO_REASONING_AGENT,
    FORECAST_SYNTHESIZER_AGENT,
    CALIBRATION_AGENT,
)

OUTPUT_DIR = Path("/Users/anishpatel/quant-brain/nexus/outputs")
GUIDELINES_DIR = Path("/Users/anishpatel/quant-brain/nexus/guidelines")


def format_context_for_agents(context: dict) -> str:
    lines = [f"# {context['ticker']} — Historical Context"]
    for day in context["history"]:
        lines.append(f"\n## {day['date']}")
        if day.get("no_data"):
            lines.append("  No trading data available.")
            continue
        lines.append(f"  Open: ${day.get('open', 'N/A')} | High: ${day.get('high', 'N/A')} | Low: ${day.get('low', 'N/A')} | Close: ${day.get('close', 'N/A')}")
        lines.append(f"  Volume: {day.get('volume', 'N/A'):,} | VWAP: ${day.get('vwap', 'N/A')}")
        lines.append(f"  Return: {day.get('return_pct', 'N/A')}%")

        noi = day.get("noi", {})
        if noi.get("has_noi"):
            lines.append(f"  NOI Messages: {noi.get('total_messages', 0)} (Open: {noi.get('open_messages', 0)}, Close: {noi.get('close_messages', 0)})")
            if "open_direction" in noi:
                lines.append(f"  Opening Imbalance: {noi['open_direction']} | Final: {noi.get('open_final_imbalance', 'N/A')} | Paired: {noi.get('open_final_paired', 'N/A')} | Acceleration: {noi.get('open_max_consecutive', 'N/A')} consecutive")
            if "close_direction" in noi:
                lines.append(f"  Closing Imbalance: {noi['close_direction']} | Final: {noi.get('close_final_imbalance', 'N/A')} | Paired: {noi.get('close_final_paired', 'N/A')} | Ratio: {noi.get('close_imbalance_ratio', 'N/A'):.2f}")
        else:
            lines.append("  NOI: Not available for this ticker (may not be NYSE-listed)")

    return "\n".join(lines)


def format_noi_summary(context: dict) -> str:
    lines = ["# NOI Pattern Summary"]
    buy_days = 0
    sell_days = 0
    accel_days = 0

    for day in context["history"]:
        noi = day.get("noi", {})
        if noi.get("close_direction") == "BUY":
            buy_days += 1
        elif noi.get("close_direction") == "SELL":
            sell_days += 1
        if noi.get("open_acceleration"):
            accel_days += 1

    total = len(context["history"])
    lines.append(f"Days analyzed: {total}")
    lines.append(f"Closing BUY imbalance days: {buy_days} ({100*buy_days/max(total,1):.0f}%)")
    lines.append(f"Closing SELL imbalance days: {sell_days} ({100*sell_days/max(total,1):.0f}%)")
    lines.append(f"Opening acceleration days: {accel_days}")

    last_day = context["history"][-1] if context["history"] else {}
    last_noi = last_day.get("noi", {})
    lines.append(f"\nMost Recent Day ({last_day.get('date', 'N/A')}):")
    if last_noi.get("has_noi"):
        lines.append(f"  Closing: {last_noi.get('close_direction', 'N/A')} | Imbalance: {last_noi.get('close_final_imbalance', 'N/A')} | Ratio: {last_noi.get('close_imbalance_ratio', 0):.2f}")
        lines.append(f"  Opening: {last_noi.get('open_direction', 'N/A')} | Acceleration: {last_noi.get('open_acceleration', False)}")

        # CIR Signal
        if last_noi.get("close_imbalance_ratio", 0) >= 0.10:
            if last_noi.get("close_direction") == "SELL":
                lines.append(f"\n  >>> CIR SIGNAL: LONG (trade opposite sell imbalance, expect 3-5 day reversal)")
            elif last_noi.get("close_direction") == "BUY":
                lines.append(f"\n  >>> CIR SIGNAL: SHORT (trade opposite buy imbalance, expect 3-5 day reversal)")
    else:
        lines.append("  No NOI data (not NYSE-listed)")

    return "\n".join(lines)


def load_guidelines(ticker: str) -> str:
    gfile = GUIDELINES_DIR / f"{ticker}_guidelines.json"
    if gfile.exists():
        data = json.loads(gfile.read_text())
        return data.get("guidelines", "No calibration guidelines available yet. This is the first run.")
    return "No calibration guidelines available yet. This is the first run. Apply the NOI signal framework:\n- Closing sell imbalance with ratio >= 0.10 → expect BUY reversal over 3-5 days (CIR signal)\n- Closing buy imbalance with ratio >= 0.10 → expect SELL reversal\n- Opening acceleration (4+ consecutive) → expect continuation for 20-25 minutes after open\n- The bigger the notional imbalance, the stronger the signal\n- Mid-caps ($2B-$10B) have strongest signals\n- Friday + sell imbalance = strongest setup (weekend inventory premium)"


def parse_tag(text: str, tag: str) -> str:
    pattern = f"<{tag}>(.*?)</{tag}>"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""


def run_pipeline(ticker: str, horizon: int, dates: list[str]) -> dict:
    """
    Run the full Nexus pipeline for a single ticker.
    Returns the complete pipeline output.

    NOTE: This version prepares all prompts and data. In production,
    each agent prompt would be sent to Claude API. For now, we prepare
    everything and output the prompts for manual/automated execution.
    """
    print(f"\n{'='*60}")
    print(f"  NEXUS PIPELINE — {ticker} | Horizon: {horizon} sessions")
    print(f"  Dates: {dates[0]} to {dates[-1]}")
    print(f"{'='*60}")

    # STAGE 0: Build context window
    print("\n[Stage 0] Building context window...")
    context = build_context_window(ticker, dates)
    structured_context = format_context_for_agents(context)
    noi_summary = format_noi_summary(context)
    guidelines = load_guidelines(ticker)

    print(f"  Context: {len(context['history'])} days, {sum(1 for d in context['history'] if d.get('noi', {}).get('has_noi'))} with NOI data")

    # STAGE 1: Historical Context Agent
    print("\n[Stage 1] Historical Context Agent — structuring timeline...")
    ctx_prompt = HISTORICAL_CONTEXT_AGENT.format(
        ticker=ticker,
        raw_data=structured_context,
    )

    # STAGE 2a: Macro-Reasoning Agent
    print("[Stage 2a] Macro-Reasoning Agent — broad trajectory analysis...")
    macro_prompt = MACRO_REASONING_AGENT.format(
        ticker=ticker,
        horizon=horizon,
        structured_context=structured_context,
        noi_summary=noi_summary,
    )

    # STAGE 2b: Micro-Reasoning Agent (parallel with 2a)
    print("[Stage 2b] Micro-Reasoning Agent — step-by-step analysis...")
    micro_prompt = MICRO_REASONING_AGENT.format(
        ticker=ticker,
        horizon=horizon,
        structured_context=structured_context,
        noi_detail=noi_summary,
    )

    # STAGE 3: Forecast Synthesizer
    print("[Stage 3] Forecast Synthesizer — merging perspectives...")
    synth_prompt = FORECAST_SYNTHESIZER_AGENT.format(
        ticker=ticker,
        horizon=horizon,
        structured_context=structured_context,
        macro_output="[Will be filled by macro agent output]",
        micro_output="[Will be filled by micro agent output]",
        guidelines=guidelines,
    )

    # Package everything
    pipeline_output = {
        "ticker": ticker,
        "horizon": horizon,
        "dates": dates,
        "run_timestamp": datetime.now().isoformat(),
        "context_summary": {
            "days_analyzed": len(context["history"]),
            "days_with_noi": sum(1 for d in context["history"] if d.get("noi", {}).get("has_noi")),
            "last_close_direction": context["history"][-1].get("noi", {}).get("close_direction", "N/A") if context["history"] else "N/A",
            "last_close_ratio": context["history"][-1].get("noi", {}).get("close_imbalance_ratio", 0) if context["history"] else 0,
            "last_open_acceleration": context["history"][-1].get("noi", {}).get("open_acceleration", False) if context["history"] else False,
        },
        "noi_signal_summary": noi_summary,
        "prompts": {
            "context_agent": ctx_prompt,
            "macro_agent": macro_prompt,
            "micro_agent": micro_prompt,
            "synthesizer_agent": synth_prompt,
        },
        "guidelines_applied": guidelines,
    }

    # Generate the NOI-derived signal independently (rule-based, not LLM)
    last_noi = context["history"][-1].get("noi", {}) if context["history"] else {}
    signal = generate_noi_signal(last_noi, ticker)
    pipeline_output["noi_rule_signal"] = signal

    return pipeline_output


def generate_noi_signal(noi: dict, ticker: str) -> dict:
    """
    Pure rule-based NOI signal generation (no LLM needed).
    Based on the two Pareto signals from our research.
    """
    signal = {
        "ticker": ticker,
        "signal_type": "NEUTRAL",
        "confidence": 0.0,
        "reasoning": "",
    }

    if not noi.get("has_noi"):
        signal["reasoning"] = "No NOI data — ticker may not be NYSE-listed"
        return signal

    # Signal 1: CIR (Closing Imbalance Reversal)
    close_ratio = noi.get("close_imbalance_ratio", 0)
    close_dir = noi.get("close_direction", "NEUTRAL")
    close_imb = noi.get("close_final_imbalance", 0)

    if close_ratio >= 0.10:
        if close_dir == "SELL":
            signal["signal_type"] = "CIR_LONG"
            signal["confidence"] = min(0.5 + close_ratio * 0.5, 0.85)
            signal["reasoning"] = (
                f"CIR LONG: Large sell-side closing imbalance (ratio={close_ratio:.2f}, "
                f"imbalance={close_imb:,}). Per Yanbin Wu (SSRN 3440239), 83% of "
                f"uninformed closing dislocations reverse within 3-5 days. "
                f"Expected return: ~32 bps over 5 days."
            )
        elif close_dir == "BUY":
            signal["signal_type"] = "CIR_SHORT"
            signal["confidence"] = min(0.5 + close_ratio * 0.5, 0.85)
            signal["reasoning"] = (
                f"CIR SHORT: Large buy-side closing imbalance (ratio={close_ratio:.2f}, "
                f"imbalance={close_imb:,}). Expect reversal per CIR framework."
            )

    # Signal 2: OIA (Opening Imbalance Acceleration) — for tomorrow's open
    if noi.get("open_acceleration"):
        open_dir = noi.get("open_direction", "NEUTRAL")
        consec = noi.get("open_max_consecutive", 0)
        if consec >= 4:
            oia_signal = f"OIA_{open_dir}" if open_dir != "NEUTRAL" else "NEUTRAL"
            # If OIA confirms CIR direction, boost confidence
            if (signal["signal_type"] == "CIR_LONG" and open_dir == "BUY") or \
               (signal["signal_type"] == "CIR_SHORT" and open_dir == "SELL"):
                signal["confidence"] = min(signal["confidence"] + 0.1, 0.90)
                signal["reasoning"] += (
                    f" OIA CONFIRMS: Opening acceleration ({consec} consecutive "
                    f"{open_dir}) aligns with CIR direction. Boosted confidence."
                )

    # Calendar boost (check day of week)
    today = datetime.now()
    if today.weekday() == 4:  # Friday
        if signal["signal_type"] in ("CIR_LONG", "CIR_SHORT"):
            signal["confidence"] = min(signal["confidence"] + 0.05, 0.90)
            signal["reasoning"] += " FRIDAY PREMIUM: Weekend inventory premium adds ~44 bps."

    return signal


def run_for_watchlist(dates: list[str], horizon: int, top_n: int = 20) -> list[dict]:
    """
    Run pipeline for the top N most interesting tickers based on NOI signals.
    """
    if not dates:
        print("No dates available.")
        return []

    latest_date = dates[-1]
    print(f"\nScanning NOI signals for {latest_date}...")
    tickers = get_tickers_with_noi(latest_date)
    print(f"Found {len(tickers)} tickers with NOI data")

    # Score all tickers by NOI signal strength
    scored = []
    for ticker in tickers:
        noi = build_noi_profile(latest_date, ticker)
        signal = generate_noi_signal(noi, ticker)
        if signal["signal_type"] != "NEUTRAL":
            scored.append({
                "ticker": ticker,
                "signal": signal["signal_type"],
                "confidence": signal["confidence"],
                "reasoning": signal["reasoning"],
                "close_ratio": noi.get("close_imbalance_ratio", 0),
                "close_imbalance": noi.get("close_final_imbalance", 0),
            })

    scored.sort(key=lambda x: x["confidence"], reverse=True)
    top = scored[:top_n]

    print(f"\nTop {len(top)} signals:")
    print(f"{'Ticker':<8} {'Signal':<12} {'Conf':>6} {'Ratio':>8} {'Imbalance':>12}")
    print("-" * 50)
    for s in top:
        print(f"{s['ticker']:<8} {s['signal']:<12} {s['confidence']:>6.2f} {s['close_ratio']:>8.2f} {s['close_imbalance']:>12,}")

    # Run full pipeline for each
    results = []
    for s in top:
        result = run_pipeline(s["ticker"], horizon, dates)
        results.append(result)

    return results


def main():
    parser = argparse.ArgumentParser(description="Nexus Pipeline Orchestrator")
    parser.add_argument("--ticker", type=str, help="Single ticker to analyze")
    parser.add_argument("--horizon", type=int, default=5, help="Forecast horizon in trading sessions")
    parser.add_argument("--date", type=str, help="Date to analyze (YYYY-MM-DD)")
    parser.add_argument("--scan", action="store_true", help="Scan all tickers and rank by signal strength")
    parser.add_argument("--top", type=int, default=20, help="Number of top signals to analyze (with --scan)")
    args = parser.parse_args()

    dates = get_available_dates()
    if args.date:
        dates = [d for d in dates if d <= args.date]

    if not dates:
        print("No captured data found. Is the WebSocket capturer running?")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    GUIDELINES_DIR.mkdir(parents=True, exist_ok=True)

    if args.scan:
        results = run_for_watchlist(dates, args.horizon, args.top)
        outfile = OUTPUT_DIR / f"scan_{dates[-1]}_{datetime.now().strftime('%H%M%S')}.json"
        with open(outfile, "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\nResults saved to {outfile}")

    elif args.ticker:
        result = run_pipeline(args.ticker, args.horizon, dates)
        outfile = OUTPUT_DIR / f"{args.ticker}_{dates[-1]}_{datetime.now().strftime('%H%M%S')}.json"
        with open(outfile, "w") as f:
            json.dump(result, f, indent=2, default=str)
        print(f"\nResult saved to {outfile}")
        print(f"\nNOI Signal: {result['noi_rule_signal']['signal_type']}")
        print(f"Confidence: {result['noi_rule_signal']['confidence']:.2f}")
        print(f"Reasoning: {result['noi_rule_signal']['reasoning']}")

    else:
        print("Usage:")
        print("  python nexus/pipeline.py --ticker AA --horizon 5")
        print("  python nexus/pipeline.py --scan --top 20 --horizon 5")


if __name__ == "__main__":
    main()
