---
name: parity-decoupling
description: >
  USE BEFORE porting ANY TradingView Pine indicator to Anish's local candle factory,
  or when asked to check whether an indicator's detection plots can be reproduced from
  Massive.com OHLCV WITHOUT a TradingView dependency. Audits each indicator study,
  classifies every detection plot (PURE_OHLCV / NEEDS_USER_INPUT / BARSTATE_LIVE /
  EXTERNAL_DEPENDENCY), flags any "TV." / request.* / library import, resolves each
  dependency to a Massive substitute, and produces per-indicator parity tables. The
  whole point is to decouple from TradingView and use it ONLY as a visual layer.
  Trigger phrases: "parity", "decouple from TradingView", "port indicator", "can we
  reproduce this plot", "audit the indicator studies", "candle factory", "TV dot
  dependency", "is there a proprietary dependency", "deconstruct the indicator".
metadata:
  type: project
  owner: anish
  created: 2026-05-31
---

# SKILL: Pine → Candle-Factory Parity Decoupling

## 0. WHO / WHAT / WHEN / WHERE / WHY (routing)

**WHY this exists.** Anish authored ~7 indicator suites (150+ detection plots) in
TradingView Pine over 4 years. The goal is to run those detections on a LOCAL candle
factory fed by Massive.com real-time + historical OHLCV, so TradingView becomes ONLY a
visual layer — no calculation dependency. Before any port, we must PROVE each detection
plot is reproducible and FLAG anything that secretly depends on TradingView internals.

**WHEN to invoke (inclusion criteria):**
- Anish attaches one or more `.txt` Pine indicator studies and asks to audit / port them.
- Anyone asks "can we reproduce this plot without TradingView?" / "is there a TV
  dependency?" / "decouple X from TradingView".
- Before the parity-verifier agent runs bar-for-bar tests (this skill is the PRE-step:
  it decides WHAT is reproducible; parity-verifier proves the Python matches).
- Codex/anyone has built or is building the candle factory and needs the detection spec.

**WHEN NOT to invoke:**
- Bar-for-bar numeric parity testing of an already-ported indicator → that is the
  `parity-verifier` agent / `pine-to-python-conversion` skill, not this one.
- Pure data-ingestion questions → `massive-data-truth` / `vendor-recon`.

**WHERE outputs live:**
- Per-indicator audit tables → `/Users/anishpatel/quant-brain/parity/audit/<name>.md`
- Consolidated verdict → `/Users/anishpatel/quant-brain/parity/audit/CONSOLIDATED.md`
- Recovered/pinned Pine source → `/Users/anishpatel/quant-brain/parity/<NAME>.pine`

**WHO does the work:** the orchestrator (you) spawns ONE auditor agent per indicator,
in parallel. If an auditor finds a genuine external dependency, IT spawns a research
sub-agent. See §3 and §4.

---

## 1. PROBLEM DEFINITION (Seven-Pillar mise en place)

> Anish demanded this be explicit before any grunt work. Reproduce this block per run.

### 1.0 Statement of Work
Prove, for each attached indicator, that every detection plot can be recomputed on a
local candle factory (Massive OHLCV → reconstructed candles → N timeframes) with NO
runtime dependency on TradingView, OR flag and resolve each dependency that exists.

### 1.1 Variables (knowns)
- **Inputs:** Massive.com minute aggregates → candle factory builds 5 timeframes,
  6000 bars/stock (5000-bar max lookback + buffer). Pine source `.txt` files.
- **Pine built-ins are pure OHLCV functions:** `ta.*`, `math.*` = deterministic
  functions of O/H/L/C/V. Fully reproducible in Python.
- **Bar metadata** (`time`, `syminfo.mintick`, `barstate.isconfirmed`) is mappable
  from Massive timestamps + a tick-size table.
- **TradingView MCP** is connected and can read live indicator values for validation
  (`mcp__tradingview__data_get_study_values`, `data_get_pine_*`).

### 1.2 Unknowns (and how each is resolved)
| Unknown | Resolution method |
|---|---|
| Does any plot use `request.*` / `security` / `syminfo` price / `vwap` / fundamentals? | grep + full read by auditor agent (§3) |
| Does any plot use a `import TradingView/...` library? | grep `import ` + classify (open-source math vs feed) |
| Exact TV recursive-seeding (ema/atr/rma)? | replicate TV convention; validate vs MCP study values |
| Session-anchor convention for RVOL? | reimplement + compare to live chart RVOL |
| From-genesis running-state alignment? | genesis-aligned replay or documented drift |

### 1.3 Governing relationships (equations)
- Detection plot = boolean/numeric series `f(O,H,L,C,V, user_inputs)`. Reproducible ⇔
  `f` is expressible in `ta.*`/`math.*` primitives with no external fetch.
- Parity-safe region: a series using `ta.highest(x,N)` is valid only for bars where
  `bar_index ≥ N`. With 6000 bars and N=5000, valid tail = last 1000 bars.
- RVOL: `RVOL_t = cumVol_session(t) / mean_{k=1..M} cumVol_session_k(sameOffset)`.

### 1.4 Current state → Ideal state → GAP
- **Current:** indicators run only inside TradingView; calculation is coupled to TV.
- **Ideal:** indicators run in Python on the candle factory; TV is display-only.
- **Gap:** (a) confirm zero un-substitutable deps [DONE 2026-05-31: zero found];
  (b) reimplement the one open-source RVOL library function;
  (c) replicate TV recursive seeding + from-genesis state;
  (d) build the candle factory + Python detection layer; (e) bar-for-bar parity.

### 1.5 Inversion (how this fools us)
- A plot looks pure but secretly calls a library with `request.security_lower_tf`
  (B2B PUP `tv_ta.relativeVolume` did exactly this). → ALWAYS grep `import ` and
  expand library calls.
- Float `volume == highest(volume)` after Massive's 2026-02-23 decimal change. → ε-compare.
- Windowed slice ≠ TradingView's from-genesis state. → genesis-aligned replay.
- Phantom/duplicate source files (Desktop TCC + multiple copies). → pin a SHA-256.

### 1.6 Acceptance criteria
Per indicator: a written table with EVERY detection plot classified + parity status,
every dependency resolved to a Massive substitute or marked BLOCKED, and a one-line
verdict. Consolidated doc with cross-cutting risks. Zero un-resolved BLOCKED items, or
each BLOCKED item has a documented research ticket.

---

## 2. INPUT → PROCESSING → OUTPUT contract

- **INPUT:** Pine `.txt` files (paths from Anish) + Massive minute aggregates + recon
  doc `recon/massive-api-endpoints.md`.
- **PROCESSING:** per-indicator full read → enumerate plots → dereference equations to
  OHLCV primitives → classify dependency → assign parity status → resolve deps.
- **OUTPUT:** `parity/audit/<name>.md` tables + `CONSOLIDATED.md` + pinned `.pine`.

---

## 3. EXACT WORKFLOW (painstaking, numbered, with IF-THEN agent spawning)

### Phase 0 — Mise en place
- **0.1** List the indicator files Anish attached. Record exact paths (they contain
  quotes/commas/em-dashes/↔ — keep them verbatim).
- **0.2** Reproduce the §1 problem-definition block for this run.
- **0.3** Create output dirs:
  `mkdir -p /Users/anishpatel/quant-brain/parity/audit`

### Phase 1 — Reconnaissance grep (cheap, before spawning)
- **1.1** Read each file's dependency profile WITHOUT a full read. The Desktop folder
  is TCC-sandboxed: `ls`/Read may fail with "Operation not permitted". **Python
  `open()` works; ALWAYS pipe bash stdout through `| cat` (this shell swallows stdout).**
  Use `/Users/anishpatel/quant-brain/skills/parity-decoupling/scan.py` (see §6) or:
  ```
  python3 scan.py 2>&1 | cat
  ```
- **1.2** For each file record counts of: `request.`, `syminfo.`, `timeframe.`,
  `\bTV\.`, `import `, `\bta\.`, `\bmath\.`, `barstate.`, `vwap`,
  `(dividends|earnings|splits)\.`, `security`, drawing calls.
- **1.3** IF `ls`/Read/`open()` all fail (TCC) → recover the file via `mdfind` /
  AppleScript Full-Disk-Access → base64 → local decode into `parity/<NAME>.pine`.
  Note: multiple copies often exist under `~/code/anish/indicators/...` — prefer a copy
  you can hash, and pin its SHA-256.

### Phase 2 — Spawn ONE auditor agent per indicator (PARALLEL)
- **2.1** Spawn N `general-purpose` agents in a SINGLE message (parallel). **Do NOT
  put any other tool call (especially a Bash `ls` on Desktop) in the same message — a
  TCC error there cancels the whole parallel batch.** (Learned 2026-05-31.)
- **2.2** Each agent prompt MUST contain: exact file path; the `open() | cat` read
  recipe + chunked-read fallback; the pre-verified recon counts ("trust then verify");
  the 5 audit tasks; the dependency + parity taxonomies; the IF-EXTERNAL escalation
  (§4); and the exact output path `parity/audit/<name>.md`.
- **2.3** Audit taxonomy each agent applies per plot:
  - DEPENDENCY ∈ {PURE_OHLCV, NEEDS_USER_INPUT_ONLY, BARSTATE_LIVE_ONLY, EXTERNAL_DEPENDENCY}
  - PARITY ∈ {REPRODUCIBLE, REPRODUCIBLE_WITH_WARMUP(+bars), LIVE_ONLY, BLOCKED}
- **2.4** Each agent writes the per-plot table (`# | Plot | Equation | Inputs |
  Dependency | Parity | Notes`), a ta.*+warmup list, and a one-line verdict.

### Phase 3 — IF-THEN dependency escalation (inside each auditor)
- **3.1 IF** a plot is classified `EXTERNAL_DEPENDENCY` (real `request.*`, `security`,
  `vwap`, fundamental, OR a `import TradingView/...` library call), **THEN** the auditor
  applies 7-pillar problem solving on that single dependency:
  - define it; list knowns/unknowns; write the governing equation;
  - **3.2** search `recon/massive-api-endpoints.md` for a Massive endpoint that supplies
    the same quantity (trades, quotes, minute aggs, short volume, etc.);
  - **3.3** IF the library is open-source (e.g. `TradingView/ta`), fetch its source and
    confirm it is MATH not a FEED → reclassify as REPRODUCIBLE_WITH_WARMUP + write the
    reimplementation formula;
  - **3.4** IF no Massive substitute exists → keep BLOCKED, open a research ticket in
    the audit file ("DEPENDENCY RESOLUTION: BLOCKED — needs <source>"), and **spawn a
    research sub-agent** to scan the web + other vendors for a substitute.
  - **3.5** ELSE write "DEPENDENCY RESOLUTION" with the Massive substitute + warmup.

### Phase 4 — Consolidate
- **4.1** Read the 4 audit files; build `CONSOLIDATED.md`: TL;DR answer, per-indicator
  status table, the resolved "TV." dependency, cross-cutting parity risks, DuckDB/
  throughput/choke-point notes + fallbacks.
- **4.2** Report to Anish with `file:///` URLs to every artifact.

### Phase 5 — Handoff to the porting layer (next skill, not this one)
- **5.1** Pin SHA-256 of each canonical source.
- **5.2** Hand the tables to `pine-to-python-conversion` → then `parity-verifier`.

---

## 4. IF-THEN AGENT-SPAWNING RULES (decision ladder)

```
IF #indicators attached ≥ 1:
    spawn 1 auditor agent PER indicator, in parallel, alone in the message.
IF an auditor finds EXTERNAL_DEPENDENCY:
    IF dependency is an open-source library (import TradingView/... or similar):
        fetch source -> confirm math-not-feed -> reclassify REPRODUCIBLE_WITH_WARMUP.
    ELSE IF Massive endpoint supplies the quantity:
        write DEPENDENCY RESOLUTION with the endpoint + warmup.
    ELSE:
        keep BLOCKED + spawn a research sub-agent (web + vendor scan) + open ticket.
IF Desktop file unreadable (TCC "Operation not permitted"):
    recover via mdfind/AppleScript-FDA -> base64 -> local .pine ; pin SHA-256.
IF multiple source copies exist:
    pin the hashable copy ; warn Anish which revision was audited.
```

---

## 5. DIAGNOSTICS & TROUBLESHOOTING

| Symptom | Cause | Fix |
|---|---|---|
| `ls`/Read on Desktop → "Operation not permitted" | macOS TCC blocks Desktop folder | use python `open()`; or mdfind/AppleScript FDA recover |
| Bash command returns NOTHING | this shell swallows stdout on some cmds | append `2>&1 \| cat` |
| Parallel agent batch all "Cancelled" | a sibling tool in the same message errored (TCC) | spawn agents ALONE; no Bash sibling |
| Recon line-count ≠ agent's line-count | phantom/duplicate file; wrong copy | recover canonical copy; pin SHA-256; trust agent's full read |
| Python EMA/ATR diverges from TV for first bars | TV SMA/Wilder seeding | replicate TV seeding; drop warmup from parity window |
| `volume == highest(volume)` never matches | 2026-02-23 Massive decimal volume | use `>= max - ε` |
| Running-max / SuperTrend / cum mismatch | windowed slice ≠ from-genesis state | genesis-aligned replay |
| RVOL signals (S5,S8–S12,S19,S20) mis-fire | session RVOL baseline not rebuilt | reimplement tv_ta.relativeVolume from minute aggs, ≥30-session warmup |
| Pivots fire too early | centered pivot lookahead | add right-offset in Python port |
| Recon grep says "0 TV deps" but agent finds one | dep hidden in `import TradingView/ta/7 as tv_ta` + `tv_ta.` alias, not `ta.`/`TV.`/`request.` | grep `^import ` AND the import alias; never trust the `ta.`-only grep |
| RVOL port off by a lot | used `volume/sma(volume,len)`; real one is session-minute-bucketed over N sessions | port library source verbatim; bucket by minute-of-session; ≥35-session warmup; 6000 bars too few at 1m |
| Big-length EMA tiers (e.g. EMA 2513) never match TV | seed contamination `(1-α)^k` still ~0.8% at 6000 bars | burn-in ≥10k bars; `ewm(adjust=False)`; feed same leading history |
| `highest(x,5000)` but max_bars_back<5000 | Pine is internally inconsistent | replicate effective (clamped) lookback OR honor literal 5000; validate vs MCP |

---

## 6. SUB-SKILL: the auditor agent procedure (`scan.py` + prompt template)

**`scan.py`** (Phase-1 recon; lives beside this file):
```python
import os, re, glob
d = "/Users/anishpatel/Desktop/Indicator studies/"   # or any dir of .txt Pine
targets = [f for f in glob.glob(d+"*.txt")]
pats = {'request.':r'request\.','syminfo.':r'syminfo\.','timeframe.':r'timeframe\.',
 'TV.':r'\bTV\.','import':r'^import ','ta.':r'\bta\.','math.':r'\bmath\.',
 'barstate.':r'barstate\.','vwap':r'vwap','div/earn/split':r'(dividends|earnings|splits)\.',
 'security':r'security','draw.new':r'(label|line|box|table)\.new','plotshape':r'plotshape'}
for t in sorted(targets):
    txt = open(t, encoding='utf-8', errors='replace').read()
    print("="*70); print(os.path.basename(t), "lines:", txt.count(chr(10))+1)
    for n,p in pats.items():
        c = len(re.findall(p, txt, re.M))
        if c: print(f"   {n:14s}{c}")
# run: python3 scan.py 2>&1 | cat
```

**Auditor agent prompt template** (fill `<<...>>`):
```
You are a TradingView Pine->Python parity auditor. Goal: prove every DETECTION PLOT in
<<FILE>> is reproducible from Massive OHLCV alone, or flag+resolve each dependency.
READ: the Desktop folder is TCC-blocked for ls/Read; python open() works; ALWAYS pipe
bash through cat. Read the WHOLE file (chunk with split(chr(10))[a:b] if long):
  python3 -c "print(open('<<FILE>>',encoding='utf-8',errors='replace').read())" | cat
PRE-VERIFIED RECON (trust then verify): <<counts>>.
TASKS: (1) enumerate every plotshape/plotchar/label/box/bgcolor/alert-gated boolean +
named signal series; (2) per plot give EQUATION (dereferenced to OHLCV+ta.* primitives),
INPUTS, PROCESSING, OUTPUT; (3) DEPENDENCY in {PURE_OHLCV|NEEDS_USER_INPUT_ONLY|
BARSTATE_LIVE_ONLY|EXTERNAL_DEPENDENCY}; (4) PARITY in {REPRODUCIBLE|
REPRODUCIBLE_WITH_WARMUP(+bars)|LIVE_ONLY|BLOCKED}; (5) list distinct ta.* + flag
recursive-seed risks (rma/ema/rsi/atr/sma/highest/lowest/barssince/valuewhen/crossover).
IF EXTERNAL_DEPENDENCY: 7-pillar resolve -> grep recon/massive-api-endpoints.md ->
if open-source library, fetch source & confirm math-not-feed -> propose Massive
substitute in a "DEPENDENCY RESOLUTION" section; else keep BLOCKED + say so.
OUTPUT: write markdown to parity/audit/<<name>>.md (verdict; count table; full per-plot
table; ta.*+warmup list; cross-cutting notes). Exhaustive, no truncation. Return a
short verdict+counts summary.
```

---

## 7. PROVENANCE / RUN LOG

- **2026-05-31:** First run on 4 studies (Foster Fix, B2B PUP 5.4, HVD-PBJ BEAR/BULL).
  Verdict: 0 BLOCKED, 0 un-substitutable feeds. Only "TV." dep = open-source
  `tv_ta.relativeVolume` (reproducible). See `CONSOLIDATED.md`. Learnings folded into
  §5 diagnostics (TCC, stdout-swallow, parallel-cancel, decimal-volume, genesis-state).
- **2026-05-31 (batch 2):** TNT OD v3, Ultra Combo v57, VOB Asym T3 v10, HW Single v3.
  Verdict: again 0 BLOCKED, 0 RED, same single "TV." dep (`tv_ta.relativeVolume`); VOB
  has NO import at all (pure `ta.ema`). See `CONSOLIDATED_BATCH2.md`. NEW learnings:
  (a) coarse grep for `request.`/`TV.`/`ta.` MISSES the dependency — it hides in an
  `import TradingView/ta/7 as tv_ta` line, so **ALWAYS grep `^import ` AND the alias
  (`tv_ta.`)**, not just `ta.`. (b) `relativeVolume(len,anchor,isCumulative,adjustRT)`
  with `anchor=""` is **session-minute-bucketed, NOT `volume/sma(volume,len)`** — needs
  ≥30 *sessions* warmup (≈11,700 bars at 1m → 6000-bar window INSUFFICIENT at 1m; fine
  at 5m+). (c) `max_bars_back` is per-indicator and often < internal `highest(_,5000)`
  calls → the Pine is internally inconsistent; replicate effective (clamped) lookback or
  honor literal, then validate. (d) Huge-length EMA seed convergence: EMA(2513) needs
  ≈8680 bars to reach 0.1% of TV's value → fund ≥10k-bar burn-in for VOB tiers A/B/C or
  they WON'T match. (e) A name can lie — VOB "T3" is a Tier-3 signal, not a Tillson T3 MA.
- **2026-05-31 (batch 3):** Displacement 4x, e3 f2 cluster, Jumbo CIA FAUNA (1st PUP),
  SQUARIFY 46 v2. Verdict: **0 BLOCKED, 0 Class-D**, all GREEN. Outputs written to a NEW
  dir `parity/decoupling-audit/` (tables/, 00-MASTER-REPORT.md) — note: earlier batches
  used `parity/audit/`; consolidate dirs on next run. Used an A/B/C/D rubric this batch
  (A=PURE_OHLCV, B=NEEDS_USER_INPUT/BARSTATE/session, C=tv_ta library, D=external feed) —
  same conclusions as the 4-class taxonomy. NEW deliverable this run: the single live
  Class-C dep `tv_ta.relativeVolume` (SQUARIFY; length=30, anchor=""→session, cumulative,
  adjustRealtime) was **fully PORTED and parity-smoke-verified**, not just described:
  `parity/decoupling-audit/relative_volume_port.py` + `relativeVolume-SOLVED.md`. Key
  facts confirmed: `adjustRealtime` is a strict **no-op on closed bars** (zero historical-
  parity risk); FAUNA's `tv_ta.relativeVolume` output (`relVolRatio`) + `sigAnish*`/
  `sigGripen*` are **dead code** (written-once-never-read) → delete during port, don't
  port. Reusable port function is the canonical RVOL implementation for all future ports.
