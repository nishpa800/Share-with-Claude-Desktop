# Failures — What Went Wrong and Why

## 2026-05-26 (Day 0)
- Built system with zero historical lookback. Nexus needs historical context. Fixed.
- Generated signals from 1 day of data with no calibration. Baseline only.
- Top CIR signals included illiquid preferred shares (paired=0). Fixed with CIR_MIN_PAIRED filter.
- OIA signals: AA was a home run (+1.4% in 20 min), TDG was a loss (-0.9%). Need to filter by notional size — bigger notional = stronger signal.
