# SKILL: Nexus Daily Autonomous Loop
## Self-Teaching, Self-Improving, Persistent Research System
## Karpathy AutoResearch + LLM Wiki + Nexus Framework + Five Pillars

**Skill ID:** NEXUS-LOOP-001
**Status:** ACTIVE — runs autonomously every trading day
**Governing Doctrine:** Five Pillars Operating System v1.0
**Architecture:** Karpathy AutoResearch loop + LLM Wiki persistence + Nexus 5-agent pipeline
**Created:** 2026-05-27

---

## WHY THIS SKILL EXISTS

Anish should NEVER have to tell the system what to do each day. The system
must teach itself, improve itself, and compound knowledge — exactly like
Karpathy's AutoResearch ran 700 experiments in 2 days with zero human input.

The system failed because:
1. No persistent memory — each session started from scratch
2. No self-evaluation — signals were generated but never scored against outcomes
3. No improvement loop — the same mistakes repeated daily
4. No compounding knowledge — insights were lost between sessions

This skill fixes all four.

---

## ARCHITECTURE: THREE SYSTEMS MERGED

### System 1: Karpathy AutoResearch Loop (the engine)

```
┌──────────────────────────────────────────────────┐
│              DAILY AUTORESEARCH LOOP              │
│                                                    │
│  1. READ yesterday's results + wiki knowledge     │
│  2. HYPOTHESIZE what to change (strategy params,  │
│     signal thresholds, new patterns)              │
│  3. MODIFY the signal generation code             │
│  4. RUN the modified system against today's data  │
│  5. EVALUATE against actual price outcomes        │
│  6. COMMIT if improved, REVERT if not             │
│  7. UPDATE the wiki with what was learned         │
│  8. REPEAT tomorrow                              │
│                                                    │
│  Target: 5-10 experiments per day                 │
│  Budget: 5 minutes per experiment (backtesting)   │
│  Decision: commit/revert based on Northstar       │
└──────────────────────────────────────────────────┘
```

Source: [Karpathy AutoResearch](https://www.marktechpost.com/2026/03/08/andrej-karpathy-open-sources-autoresearch-a-630-line-python-tool-letting-ai-agents-run-autonomous-ml-experiments-on-single-gpus/)

### System 2: Karpathy LLM Wiki (the memory)

```
nexus/wiki/
├── raw/                     # Immutable source material
│   ├── nexus-paper.md       # The Nexus framework paper
│   ├── noi-alpha-research.md
│   ├── noi-practical-strategies.md
│   ├── five-pillars.md
│   └── daily-results/       # Each day's signal results
│       ├── 2026-05-26.md
│       ├── 2026-05-27.md
│       └── ...
│
├── wiki/                    # LLM-maintained entity pages
│   ├── index.md             # Master index of all concepts
│   ├── log.md               # Compilation history
│   ├── cir-signal.md        # Closing Imbalance Reversal - everything known
│   ├── oia-signal.md        # Opening Imbalance Acceleration
│   ├── sector-rotation.md   # ETF rotation patterns
│   ├── noi-thresholds.md    # Calibrated thresholds (updated daily)
│   ├── ticker-profiles.md   # Per-ticker NOI behavior patterns
│   ├── failures.md          # What went wrong and why
│   ├── improvements.md      # What worked and should be repeated
│   ├── calendar-effects.md  # Day-of-week, month-end, rebalance patterns
│   ├── regime-detection.md  # VIX regimes, bull/bear/chop
│   └── ...                  # New pages created as knowledge grows
```

Source: [Karpathy LLM Wiki](https://datasciencedojo.com/blog/llm-wiki-tutorial/)

At 10 pages it answers basic questions.
At 50 pages it synthesizes across ideas you never explicitly connected.
At 100+ pages it becomes a self-improving research brain.

### System 3: Nexus 5-Agent Pipeline (the forecaster)

```
Historical Context (REST/S3 lookback + WebSocket real-time + Wiki knowledge)
    ├──► Macro-Reasoning Agent (broad trajectory + sector rotation)
    └──► Micro-Reasoning Agent (per-session catalysts + NOI signals)
         ↓
Forecast Synthesizer (merges perspectives + calibration guidelines)
         ↓
Calibration Agent (scores against outcomes, generates improvement rules)
         ↓
Wiki Update (new knowledge committed to persistent memory)
```

---

## THE DAILY LOOP — WHAT RUNS EVERY DAY WITHOUT HUMAN INPUT

### Pre-Market Phase (7:00 AM CT — 1.5 hours before open)

```
STEP 1: LOAD CONTEXT
  ├── Read wiki/index.md (what do we know?)
  ├── Read wiki/noi-thresholds.md (current calibrated thresholds)
  ├── Read wiki/failures.md (what to avoid)
  ├── Read wiki/improvements.md (what to repeat)
  ├── Load yesterday's signal results + actual outcomes
  └── Load historical lookback from S3/REST data

STEP 2: SCORE YESTERDAY
  ├── For each CIR signal generated yesterday:
  │   ├── Pull actual price at T+1 open, T+1 close, T+2, T+3
  │   ├── Compute return at each timeframe
  │   ├── Score: did the reversal happen? By how much?
  │   └── Tag: WIN / LOSS / PENDING (if < 5 days old)
  ├── For each OIA signal from yesterday morning:
  │   ├── Pull actual 5m, 10m, 15m, 20m returns after entry
  │   └── Score: did the acceleration predict direction?
  └── Save results to raw/daily-results/YYYY-MM-DD.md

STEP 3: CALIBRATE (Nexus Calibration Agent)
  ├── Compare predicted signals vs actual outcomes
  ├── Generate critique: where were we wrong?
  ├── Generate guidelines: what to adjust?
  ├── Intersect with guidelines from previous days
  │   (only keep rules that generalize across 5+ days)
  └── Update wiki/noi-thresholds.md with calibrated values

STEP 4: RESEARCH (AutoResearch loop)
  ├── Read latest from Massive.com blog (any new tutorials?)
  ├── Check if any data schemas changed
  ├── Look for new patterns in accumulated data
  │   ├── Are certain tickers consistently better CIR signals?
  │   ├── Are certain sectors showing persistent imbalance?
  │   ├── Is there a time-of-day pattern in NOI accuracy?
  │   └── Any new cross-signal patterns (NOI + volume + sector)?
  └── If pattern found: create new wiki page, add to index

STEP 5: GENERATE TODAY'S SIGNALS
  ├── Load yesterday's closing NOI for CIR signals
  ├── Apply calibrated thresholds (from wiki, not defaults)
  ├── Cross-reference with sector rotation (ETF flows)
  ├── Cross-reference with earnings calendar (Benzinga)
  ├── Filter against wiki/failures.md (avoid known bad patterns)
  ├── Rank by confidence (Nexus Synthesizer)
  └── Output: today's signal report
```

### Market Hours Phase (8:25 AM CT — opening auction)

```
STEP 6: OPENING IMBALANCE MONITORING
  ├── WebSocket NOI feed is live (already running)
  ├── At 8:25-8:30 CT: monitor acceleration signals
  ├── Apply OIA thresholds from wiki/noi-thresholds.md
  ├── If signal fires: log to daily-results with entry price
  └── At 8:55 CT: log 20-min outcome for OIA signals
```

### Post-Market Phase (3:15 PM CT — after close)

```
STEP 7: CLOSING IMBALANCE CAPTURE
  ├── WebSocket captured closing auction NOI
  ├── Score all closing imbalances
  ├── Generate tomorrow's CIR signals
  ├── Cross-reference with sector rotation
  └── Output: next-day signal report

STEP 8: WIKI UPDATE (Karpathy pattern)
  ├── Add today's results to raw/daily-results/
  ├── Run compilation: update wiki pages with new knowledge
  │   ├── Update noi-thresholds.md if calibration changed values
  │   ├── Update ticker-profiles.md with new per-ticker patterns
  │   ├── Update failures.md if a signal type failed
  │   ├── Update improvements.md if something worked well
  │   └── Create new pages for any newly discovered patterns
  ├── Run linting pass (every 20 new data points):
  │   ├── Check for contradictions between wiki pages
  │   ├── Resolve stale information
  │   └── Ensure index.md is current
  └── Commit updated wiki to git

STEP 9: EXPERIMENT (AutoResearch pattern)
  ├── Pick ONE hypothesis to test (from wiki/improvements.md or new idea)
  ├── Modify signal parameters (threshold, timeframe, filter)
  ├── Backtest on last 30 days of data
  ├── Compare Northstar metrics: better or worse?
  ├── If better by ≥5%: COMMIT the change, update thresholds
  ├── If worse: REVERT, log in wiki/failures.md WHY it didn't work
  └── Log experiment in autoresearch/log/YYYY-MM-DD.md
```

---

## WHAT COMPOUNDS OVER TIME

### Week 1 (days 1-5):
- Basic CIR/OIA signals with default thresholds
- Raw win/loss tracking
- Wiki has ~10 pages

### Week 2 (days 6-10):
- First calibration cycle complete (5+ days of data)
- Thresholds adjusted based on actual performance
- Per-ticker patterns emerging
- Wiki has ~25 pages, starting to cross-reference

### Month 1 (days 11-22):
- Calibration-by-intersection active (generalized rules)
- Sector rotation patterns integrated
- Day-of-week effects quantified
- VIX regime-dependent thresholds
- Wiki has ~50 pages, synthesizing connections
- AutoResearch has run 50+ experiments, ~10 committed improvements

### Month 3 (days 45-66):
- Full quarter of data
- Seasonal patterns emerging
- Ticker-specific models (some tickers are better CIR candidates)
- Cross-signal confluence patterns validated
- Wiki has ~100 pages, approaching Karpathy-scale knowledge base
- System is materially better than day 1

### Month 6+:
- The system knows more about NOI signals on these tickers than any human
- Calibrated thresholds are evidence-based, not guesswork
- New patterns discovered that weren't in the academic literature
- The wiki IS the institutional knowledge of this trading operation

---

## IMPLEMENTATION: THE DAILY CRON JOB

This runs as a Hermes cron job OR a launchd plist on macOS:

```
# Pre-market: 7:00 AM CT
0 7 * * 1-5  cd /Users/anishpatel/quant-brain && .venv/bin/python nexus/daily_loop.py --phase premarket

# Opening auction: 8:25 AM CT  
25 8 * * 1-5  cd /Users/anishpatel/quant-brain && .venv/bin/python nexus/daily_loop.py --phase open

# Post-market: 3:15 PM CT
15 15 * * 1-5  cd /Users/anishpatel/quant-brain && .venv/bin/python nexus/daily_loop.py --phase postmarket

# Nightly experiment: 8:00 PM CT
0 20 * * 1-5  cd /Users/anishpatel/quant-brain && .venv/bin/python nexus/daily_loop.py --phase experiment
```

---

## FIVE PILLARS COMPLIANCE

### Pillar I — Problem-Solving
The daily loop IS the equation: `Knowledge(day_n) = Knowledge(day_{n-1}) + Learnings(day_n) - Pruned_stale_info`
This is a compounding function. The growth rate r depends on the quality of
the calibration agent and the thoroughness of the wiki updates.

### Pillar II — Critical Thinking
Every day the system asks: "What did I get wrong yesterday and WHY?"
The wiki/failures.md page is the inversion analysis made persistent.
The calibration-by-intersection ensures only generalizable rules survive.

### Pillar III — Cryptography
Each day adds more data to the pattern detection engine. Patterns that
were invisible in 5 days of data become visible in 30 days. The system
is decoding the market's hidden structure one day at a time.

### Pillar IV — Statistical Modeling
The Northstar metrics are computed daily. Calibration error is tracked.
Reference ranges are updated. Overfitting is detected by the intersection
protocol (a rule that works on one fold but not five is noise, not signal).

### Pillar V — Game Theory
The system understands WHY its edge exists (structural equilibrium, not anomaly)
and monitors whether the game is changing (are more participants fading the
closing imbalance? is the reversal rate declining from 83%?).

---

## HOW THIS PREVENTS ANISH FROM HAVING TO TELL ME WHAT TO DO

| What Anish used to have to do | What the system does instead |
|-------------------------------|------------------------------|
| "Download the data" | S3 sync runs automatically daily |
| "Score yesterday's signals" | Pre-market phase scores everything |
| "What signals are there today?" | Signal report auto-generated by 7:30 AM CT |
| "Update the thresholds" | Calibration agent adjusts thresholds after 5+ days |
| "Check the ETF rotation" | Sector rotation analysis runs automatically |
| "What went wrong?" | wiki/failures.md updated every post-market |
| "Try something new" | AutoResearch experiment runs every night |
| "Remember what we learned" | Wiki persists and compounds across sessions |
| "Don't make the same mistake" | Failures page is checked before every signal |

Anish reviews the morning report, makes trading decisions, and gives feedback
if something is wrong. The system does everything else.

---

## SOURCES

- [Karpathy AutoResearch](https://www.marktechpost.com/2026/03/08/andrej-karpathy-open-sources-autoresearch-a-630-line-python-tool-letting-ai-agents-run-autonomous-ml-experiments-on-single-gpus/)
- [Karpathy LLM Wiki Tutorial](https://datasciencedojo.com/blog/llm-wiki-tutorial/)
- [Karpathy on the Loopy Era of AI](https://www.nextbigfuture.com/2026/03/andrej-karpathy-on-code-agents-autoresearch-and-the-self-improvement-loopy-era-of-ai.html)
- [Nexus: Agentic Framework for Time Series Forecasting (arXiv 2605.14389v1)](https://arxiv.org/html/2605.14389v1)
- Five Pillars Operating System v1.0 (Anish Patel)
