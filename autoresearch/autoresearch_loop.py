#!/usr/bin/env python3
"""
autoresearch_loop.py  —  the entire auto-research engine, ~180 lines, zero dependencies.

The point of this file: the LOOP is not the hard part. Observe -> hypothesize -> test ->
log -> rank -> repeat is mechanical. The hard part is the two functions at the bottom
(load_events / load_labels). Everything between them is generic and done.

It RUNS as-is on synthetic data so you can see the loop work right now:
    python3 autoresearch_loop.py
Then swap `generate_synthetic_events()` for `load_real_events()` to point it at your
parity-reconstructed candles + 13F-anchored labels. Nothing else changes.

What it tests: for any signal (a detection plot firing, a cluster, anything boolean) and any
target outcome (e.g. "price advanced >= 1 unit within H bars" = bullish_KE_realized), is the
signal diagnostic? Output is a likelihood ratio with a confidence interval, gated exactly the
way ALPHA_SPEC.md requires (CI excludes 1, FDR-controlled across the whole search).
"""

from __future__ import annotations
import json, math, random, statistics
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

random.seed(7)  # reproducible

# ----------------------------------------------------------------------------------------
# 1. STATS — confusion matrix -> likelihood ratios with Wilson CIs (stdlib only)
# ----------------------------------------------------------------------------------------
def _wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for a proportion k/n. Returns (lo, hi)."""
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    s = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - s) / d, (c + s) / d)

def confusion_and_lr(tp: int, fp: int, fn: int, tn: int) -> dict:
    sens = tp / (tp + fn) if (tp + fn) else 0.0          # P(signal+ | state true)
    spec = tn / (tn + fp) if (tn + fp) else 0.0          # P(signal- | state false)
    ppv  = tp / (tp + fp) if (tp + fp) else 0.0
    npv  = tn / (tn + fn) if (tn + fn) else 0.0
    lr_plus  = sens / (1 - spec) if (1 - spec) > 0 else float("inf")
    lr_minus = (1 - sens) / spec if spec > 0 else float("inf")
    # CI on LR+ via Wilson on sens and spec (rough but honest; gate is "CI excludes 1")
    s_lo, s_hi = _wilson(tp, tp + fn)
    sp_lo, sp_hi = _wilson(tn, tn + fp)
    lr_plus_lo = s_lo / (1 - sp_lo) if (1 - sp_lo) > 0 else float("inf")
    lr_plus_hi = s_hi / (1 - sp_hi) if (1 - sp_hi) > 0 else float("inf")
    return dict(tp=tp, fp=fp, fn=fn, tn=tn, n=tp + fp + fn + tn,
                sens=round(sens, 3), spec=round(spec, 3), ppv=round(ppv, 3), npv=round(npv, 3),
                lr_plus=round(lr_plus, 2), lr_plus_ci=(round(lr_plus_lo, 2), round(lr_plus_hi, 2)),
                lr_minus=round(lr_minus, 3))

def benjamini_hochberg(pvals: list[float], q: float = 0.10) -> list[bool]:
    """FDR control. Returns a pass/fail mask aligned to pvals."""
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    passed = [False] * m
    crit = 0
    for rank, i in enumerate(order, start=1):
        if pvals[i] <= (rank / m) * q:
            crit = rank
    for rank, i in enumerate(order, start=1):
        if rank <= crit:
            passed[i] = True
    return passed

def approx_pvalue(tp, fp, fn, tn) -> float:
    """Two-sided z-test on the log-odds ratio (Haldane-Anscombe 0.5 correction)."""
    a, b, c, d = tp + 0.5, fp + 0.5, fn + 0.5, tn + 0.5
    lor = math.log((a * d) / (b * c))
    se = math.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
    z = abs(lor / se)
    return math.erfc(z / math.sqrt(2))  # two-sided

# ----------------------------------------------------------------------------------------
# 2. HYPOTHESIS — a signal condition + the target outcome it claims to predict
# ----------------------------------------------------------------------------------------
@dataclass
class Hypothesis:
    name: str
    target: str                       # outcome key on each event, e.g. "bullish_KE_realized"
    predicate: callable               # event -> bool : did the signal fire?
    rationale: str = ""

def test(hyp: Hypothesis, events: list[dict]) -> dict:
    tp = fp = fn = tn = 0
    for e in events:
        fired = bool(hyp.predicate(e))
        truth = bool(e[hyp.target])
        if fired and truth: tp += 1
        elif fired and not truth: fp += 1
        elif not fired and truth: fn += 1
        else: tn += 1
    m = confusion_and_lr(tp, fp, fn, tn)
    m["pvalue"] = approx_pvalue(tp, fp, fn, tn)
    m["name"], m["target"], m["rationale"] = hyp.name, hyp.target, hyp.rationale
    return m

# ----------------------------------------------------------------------------------------
# 3. PROPOSE — generate hypotheses. "Pick a random detection plot." "Bearish cluster -> up."
#    This is literally the scientific method, automated. Add generators here; that's the job.
# ----------------------------------------------------------------------------------------
DETECTION_PLOTS = ["PUP_b2b", "FAUNA_bull", "HVD_disp5", "UC", "RVOL1x_bull",
                   "PPD_b2b", "FAUNA_bear", "HVD_disp5_bear", "MOAB_bear", "RVOL1x_bear",
                   "noise_a", "noise_b", "noise_c", "noise_d", "noise_e"]  # noise = must fail

def propose_single_plot(target: str) -> Hypothesis:
    plot = random.choice(DETECTION_PLOTS)
    return Hypothesis(f"{plot}->{target}", target,
                      predicate=lambda e, p=plot: e["signals"].get(p, False),
                      rationale=f"does {plot} alone predict {target}?")

def propose_bearish_cluster(target: str = "bullish_KE_realized", k: int = 3) -> Hypothesis:
    """Your exact example: when a candle has a bunch of bearish signals, hypothesize it is
    bearish POTENTIAL energy -> price goes UP (opposite-polarity rule)."""
    bear = ["PPD_b2b", "FAUNA_bear", "HVD_disp5_bear", "MOAB_bear", "RVOL1x_bear"]
    return Hypothesis(f"bearish_cluster>={k}->{target}", target,
                      predicate=lambda e, b=bear, k=k: sum(e["signals"].get(s, False) for s in b) >= k,
                      rationale=f">= {k} bearish plots on a bar -> bearish PE -> bullish KE")

# ----------------------------------------------------------------------------------------
# 4. THE LOOP — propose, test, log to disk, FDR-control, rank, report.
# ----------------------------------------------------------------------------------------
def run_loop(events: list[dict], n_random: int = 60, out_dir: Path = Path(".")):
    results = []
    results.append(test(propose_bearish_cluster(), events))           # the named hypothesis
    for _ in range(n_random):                                         # the random search
        results.append(test(propose_single_plot("bullish_KE_realized"), events))

    passed_fdr = benjamini_hochberg([r["pvalue"] for r in results], q=0.10)
    for r, ok in zip(results, passed_fdr):
        r["fdr_pass"] = ok
        # ALPHA_SPEC gate: meaningful LR AND CI excludes 1 AND survives FDR
        r["ships"] = (r["lr_plus"] >= 2.0 and r["lr_plus_ci"][0] > 1.0 and ok)

    out = out_dir / f"results_{datetime.now():%Y%m%dT%H%M%S}.jsonl"
    with out.open("w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    shipped = sorted([r for r in results if r["ships"]], key=lambda r: r["lr_plus"], reverse=True)
    print(f"tested {len(results)} hypotheses | {sum(r['ships'] for r in results)} pass the gate "
          f"(LR+>=2, CI>1, FDR q=.10) | logged -> {out.name}\n")
    print(f"{'hypothesis':32} {'n':>5} {'LR+':>6} {'CI':>14} {'sens':>5} {'spec':>5} {'ships':>5}")
    for r in sorted(results, key=lambda r: r["lr_plus"], reverse=True)[:8]:
        print(f"{r['name'][:32]:32} {r['n']:>5} {r['lr_plus']:>6} "
              f"{str(r['lr_plus_ci']):>14} {r['sens']:>5} {r['spec']:>5} {str(r['ships']):>5}")
    return results

# ----------------------------------------------------------------------------------------
# 5. DATA  <-- THE ONLY HARD PART. Replace synthetic with real parity candles + labels.
# ----------------------------------------------------------------------------------------
def generate_synthetic_events(n: int = 4000) -> list[dict]:
    """Stand-in for real data so the loop runs. Bakes in a TRUE hidden relationship
    (bearish cluster -> up) plus a weak one (UC -> up) plus pure-noise signals, so the
    engine can actually DISCOVER the real edges and (correctly) reject the noise."""
    events = []
    for _ in range(n):
        sig = {p: random.random() < 0.12 for p in DETECTION_PLOTS}
        bear_count = sum(sig.get(s, False) for s in ["PPD_b2b", "FAUNA_bear", "HVD_disp5_bear", "MOAB_bear", "RVOL1x_bear"])
        # ground truth: bearish cluster strongly -> up; UC weakly -> up; else base rate
        p_up = 0.30
        if bear_count >= 3: p_up = 0.78
        if sig.get("UC"):   p_up = min(0.95, p_up + 0.18)
        events.append({"signals": sig, "bullish_KE_realized": random.random() < p_up})
    return events

def load_real_events() -> list[dict]:
    """TODO (this is the actual work, and it's what the rest of the repo exists to produce):
      - read parity-reconstructed candles (parity/, signals/) across the timeframe sweep
      - attach detection-plot booleans per bar (signals/)
      - attach the OUTCOME label per bar from the 13F-anchored retrospective
        (price advanced >= 1 unit within H bars, point-in-time, NO lookahead)
    Return the same shape as generate_synthetic_events(). Then delete the synthetic call below.
    """
    raise NotImplementedError("wire parity candles + labels here")

if __name__ == "__main__":
    events = generate_synthetic_events()          # <-- swap for load_real_events()
    run_loop(events, out_dir=Path(__file__).parent)
