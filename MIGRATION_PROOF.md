# quant-brain → one-system consolidation — MIGRATION PROOF
Date: 2026-05-31 (Sun) ~22:30 CDT
Operator: Claude Code (Opus 4.8). Anish executes the deletion himself.

## What "one system" means now
- CODE  → GitHub `nishpa800/trading-data-system`, under `quant-brain/`
- DATA  → this OWC archive: `/Volumes/OWC Envoy Ultra/quant-brain-archive-20260531/`
- LEDGER→ local git repo initialized in quant-brain (commit 924fbef)

## Three lockstep moves (Claude ↔ Codex)
1. git init quant-brain — first version-controlled snapshot. Commit `924fbef`.
2. AGENTS.md → CLAUDE.md symlink in quant-brain — Codex now boots from the
   SAME 15 KB project brief as Claude (zero drift; one file, two names).
3. Reconciled global files: fixed persona contradiction in
   `~/.codex/AGENTS.md` ("non-technical founder" → "MD / domain expert,
   not a software engineer") to match `~/.claude/CLAUDE.md`, and added an
   explicit anti-drift sibling clause.

## Preservation proof
SOURCE (excl .venv) at snapshot: 23,688 files / 15,250,835,832 bytes (14.20 GB)
OWC MIRROR:                       23,692 files / 15,250,856,544 bytes
- Mirror ≥ source because live processes added files during/after copy.
- Byte-identity verified with `rsync -anc` (checksum) dry-run.
- ALL 21 residual diffs are files BORN AFTER the snapshot by live writers
  (rnd/* autoresearch output, *.pyc bytecode, capturer status heartbeats).
  NONE are modifications or deletions of already-captured data. No loss.

Data composition (14 GB):
- data/realtime/ = 13 GB  IRREPLACEABLE (websocket-only: trades 12G, NOI 65M,
  minute_aggs 561M, status 24M). Last market data: 2026-05-29 (Fri).
- data/historical/ = 1.4 GB  re-fetchable from Massive S3.

## Code merge
- Repo: nishpa800/trading-data-system
- Branch: merge/quant-brain-consolidation   Commit: 5fe9c06   PR: #1
- Path: quant-brain/  (1048 files / 45 MB)
- Excluded (junk/regenerable, also present in this mirror): .DS_Store,
  __pycache__/*.pyc, one external gstack .ts (recoverable from gstack origin).

## DELETION BLOCKER (must clear before `rm`)
Live processes writing INTO quant-brain at proof time:
- PID 50499  capture-ws.py (NOI/WebSocket capturer) — IDLE (weekend) but alive.
- PID 59819  rnd/autoresearch.py --workers 4 --max-exps 25 — another agent's
  "100-experiment proof run."
Note: trading-data-system has its OWN NOI pipeline at
`OWC/TradingDataSystem/massive-realtime/noi` — quant-brain's capturer is the
legacy duplicate. Going forward, live NOI capture = TDS's job.

## SAFE DELETION RUNBOOK (Anish runs)
1. Stop the two writers:
     pkill -f capture-ws.py
     pkill -f 'rnd/autoresearch.py'
2. Final delta re-sync (sweeps in post-snapshot files):
     rsync -a --exclude='.venv/' /Users/anishpatel/quant-brain/ \
       "/Volumes/OWC Envoy Ultra/quant-brain-archive-20260531/"
3. Re-verify (expect 0 real diffs):
     rsync -anc --exclude='.venv/' /Users/anishpatel/quant-brain/ \
       "/Volumes/OWC Envoy Ultra/quant-brain-archive-20260531/" | grep -v '/$'
4. Delete ONLY after steps 1-3 are clean:
     rm -rf /Users/anishpatel/quant-brain
5. Monday before 08:30 CDT open: confirm TDS's NOI capturer is the live one.

## Recovery
- Code:  git clone https://github.com/nishpa800/trading-data-system (quant-brain/)
- Data:  this OWC archive directory (full mirror)
