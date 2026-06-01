"""
signal.py — THE FILE THE AUTORESEARCH LOOP MODIFIES

This contains all signal parameters, thresholds, filters, and scoring logic.
The autoresearch agent experiments by changing values here, backtesting,
and keeping changes that improve the Northstar score.

DO NOT put data loading or evaluation metrics here.
Those live in prepare.py (fixed, do not modify).
"""

# ─────────────────────────────────────────────────────────────────
# CIR (Closing Imbalance Reversal) Parameters
# ─────────────────────────────────────────────────────────────────

CIR_MIN_RATIO = 0.10           # minimum imbalance/paired ratio to trigger
CIR_MAX_RATIO = 5.0            # above this = suspicious, likely bad data
CIR_MIN_NOTIONAL = 500_000     # minimum dollar imbalance to be meaningful
CIR_MIN_PAIRED = 100           # minimum paired quantity (filter illiquid auctions)
CIR_HOLD_DAYS = 5              # expected reversal window
CIR_EXIT_PARTIAL_DAY = 1       # sell 50% at this day (overnight premium capture)

CIR_CONFIDENCE_BASE = 0.50
CIR_CONFIDENCE_RATIO_WEIGHT = 0.5   # how much ratio adds to confidence
CIR_CONFIDENCE_CAP = 0.85

CIR_FRIDAY_BOOST = 0.05        # weekend inventory premium
CIR_VIX_THRESHOLD = 20         # above this, VIX scale kicks in
CIR_VIX_WEIGHT = 0.05          # added confidence when VIX > threshold

# Sector filter: only CIR_LONG in sectors with positive 30-day flows
CIR_USE_SECTOR_FILTER = True

# Earnings filter: skip tickers reporting within N days (informed flow risk)
CIR_EARNINGS_EXCLUSION_DAYS = 3

# Market cap filter (in billions)
CIR_MIN_MCAP = 2.0
CIR_MAX_MCAP = 500.0


# ─────────────────────────────────────────────────────────────────
# OIA (Opening Imbalance Acceleration) Parameters
# ─────────────────────────────────────────────────────────────────

OIA_MIN_CONSECUTIVE = 4         # minimum consecutive same-direction messages
OIA_MIN_SIGMA = 1.0             # minimum standard deviations from 20-day mean
OIA_ENTRY_DELAY_MINUTES = 5     # wait this many minutes after open to enter
OIA_EXIT_MINUTES = 20           # close position this many minutes after entry
OIA_HARD_EXIT_MINUTES = 25      # absolute max hold time

OIA_MIN_NOTIONAL = 100_000
OIA_FLIP_CANCEL = True          # cancel signal if imbalance flips in last 2 min

OIA_CONFIDENCE_BASE = 0.45
OIA_CONFIDENCE_CONSEC_WEIGHT = 0.05  # per consecutive message above minimum
OIA_CONFIDENCE_CAP = 0.80


# ─────────────────────────────────────────────────────────────────
# Combined / HomeRun Parameters
# ─────────────────────────────────────────────────────────────────

HOMERUN_REQUIRE_CIR_AND_OIA = True   # both must align for HomeRun signal
HOMERUN_CONFIDENCE_BOOST = 0.10


# ─────────────────────────────────────────────────────────────────
# Scoring Weights (Northstar composite)
# ─────────────────────────────────────────────────────────────────

NORTHSTAR_PPV_WEIGHT = 0.30
NORTHSTAR_SENSITIVITY_WEIGHT = 0.30
NORTHSTAR_MCC_WEIGHT = 0.20
NORTHSTAR_BRIER_WEIGHT = 0.20


# ─────────────────────────────────────────────────────────────────
# Signal Generation Functions
# ─────────────────────────────────────────────────────────────────

def score_cir(imbalance: int, paired: int, book_price: float,
              is_friday: bool = False, vix: float = 15.0,
              sector_inflowing: bool = True, days_to_earnings: int = 999) -> dict:
    """Score a single ticker's CIR signal from closing auction data."""

    if paired < CIR_MIN_PAIRED:
        return {"signal": "NEUTRAL", "confidence": 0.0, "reason": "paired < minimum"}

    ratio = abs(imbalance) / max(paired, 1)
    notional = abs(imbalance * book_price)

    if ratio < CIR_MIN_RATIO:
        return {"signal": "NEUTRAL", "confidence": 0.0, "reason": f"ratio {ratio:.3f} < {CIR_MIN_RATIO}"}
    if ratio > CIR_MAX_RATIO:
        return {"signal": "NEUTRAL", "confidence": 0.0, "reason": f"ratio {ratio:.3f} > max (suspicious)"}
    if notional < CIR_MIN_NOTIONAL:
        return {"signal": "NEUTRAL", "confidence": 0.0, "reason": f"notional ${notional:,.0f} < ${CIR_MIN_NOTIONAL:,.0f}"}

    if CIR_USE_SECTOR_FILTER and not sector_inflowing:
        return {"signal": "NEUTRAL", "confidence": 0.0, "reason": "sector outflowing"}

    if days_to_earnings < CIR_EARNINGS_EXCLUSION_DAYS:
        return {"signal": "NEUTRAL", "confidence": 0.0, "reason": f"earnings in {days_to_earnings} days"}

    direction = "CIR_LONG" if imbalance < 0 else "CIR_SHORT"
    confidence = CIR_CONFIDENCE_BASE + min(ratio, 0.7) * CIR_CONFIDENCE_RATIO_WEIGHT

    if is_friday:
        confidence += CIR_FRIDAY_BOOST
    if vix > CIR_VIX_THRESHOLD:
        confidence += CIR_VIX_WEIGHT

    confidence = min(confidence, CIR_CONFIDENCE_CAP)

    return {
        "signal": direction,
        "confidence": round(confidence, 3),
        "ratio": round(ratio, 4),
        "notional": round(notional, 2),
        "hold_days": CIR_HOLD_DAYS,
        "partial_exit_day": CIR_EXIT_PARTIAL_DAY,
    }


def score_oia(consecutive: int, final_imbalance: int, book_price: float,
              sigma_score: float = 1.0, flipped: bool = False) -> dict:
    """Score a single ticker's OIA signal from opening auction data."""

    if consecutive < OIA_MIN_CONSECUTIVE:
        return {"signal": "NEUTRAL", "confidence": 0.0, "reason": f"consecutive {consecutive} < {OIA_MIN_CONSECUTIVE}"}

    if sigma_score < OIA_MIN_SIGMA:
        return {"signal": "NEUTRAL", "confidence": 0.0, "reason": f"sigma {sigma_score:.2f} < {OIA_MIN_SIGMA}"}

    notional = abs(final_imbalance * book_price)
    if notional < OIA_MIN_NOTIONAL:
        return {"signal": "NEUTRAL", "confidence": 0.0, "reason": f"notional ${notional:,.0f} < ${OIA_MIN_NOTIONAL:,.0f}"}

    if OIA_FLIP_CANCEL and flipped:
        return {"signal": "NEUTRAL", "confidence": 0.0, "reason": "imbalance flipped in last 2 min"}

    direction = "OIA_LONG" if final_imbalance > 0 else "OIA_SHORT"
    extra_consec = max(0, consecutive - OIA_MIN_CONSECUTIVE)
    confidence = OIA_CONFIDENCE_BASE + extra_consec * OIA_CONFIDENCE_CONSEC_WEIGHT
    confidence = min(confidence, OIA_CONFIDENCE_CAP)

    return {
        "signal": direction,
        "confidence": round(confidence, 3),
        "consecutive": consecutive,
        "notional": round(notional, 2),
        "entry_delay_min": OIA_ENTRY_DELAY_MINUTES,
        "exit_min": OIA_EXIT_MINUTES,
        "hard_exit_min": OIA_HARD_EXIT_MINUTES,
    }
