"""
R&D AutoResearch — autoresearch.py   [THE NEVER-STOP LOOP]
=============================================================================
Mantra: "R&D never stops. 24/7, no sleep."

Karpathy autoresearch loop, adapted to Anish's question. Each experiment:
  1. mutate the config (hill-climb from the global best)
  2. evaluate() on held-out sessions  -> RND_Northstar   (free Python heavy-lift)
  3. KEEP if it improved, REVERT if not                  (commit/discard)
  4. append to results.tsv + write an experiment note
This runs forever (--max-exps 0) under launchd, OR bounded for a proof run.

--workers K forks K independent hill-climbers that share the global best and the
results ledger via a file lock. On a 128 GB / multi-core machine this turns the
box into a swarm of cooperating searchers — the honest realization of "100 agents
running experiments", in free Python.
"""
from __future__ import annotations
import argparse
import contextlib
import fcntl
import json
import os
import random
import sys
import time
import multiprocessing as mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "eval"))

import evaluate as E          # noqa: E402
import model as M             # noqa: E402
from prepare import FEATURE_COLS, build_events  # noqa: E402

RESULTS = os.path.join(HERE, "results.tsv")
BEST = os.path.join(HERE, "cache", "best_config.json")
LOCK = os.path.join(HERE, "cache", ".lock")
EXP_DIR = os.path.join(HERE, "experiments")
HEADER = "ts\texp_id\tworker\tscore\tppv\tnpv\tspec\tmcc\tbrier\tn_test\tstatus\tdescription\n"


@contextlib.contextmanager
def filelock():
    os.makedirs(os.path.dirname(LOCK), exist_ok=True)
    f = open(LOCK, "w")
    try:
        fcntl.flock(f, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()


def read_global_best():
    with filelock():
        if os.path.exists(BEST):
            with open(BEST) as f:
                return json.load(f)
    return None


def write_global_best(cfg, score, exp_id):
    with filelock():
        cur = None
        if os.path.exists(BEST):
            with open(BEST) as f:
                cur = json.load(f)
        if cur is None or score > cur["score"]:
            with open(BEST, "w") as f:
                json.dump({"config": cfg, "score": score, "exp_id": exp_id}, f, indent=2)
            return True
    return False


def log_result(row: dict):
    with filelock():
        new = not os.path.exists(RESULTS)
        with open(RESULTS, "a") as f:
            if new:
                f.write(HEADER)
            f.write("\t".join(str(row[k]) for k in
                    ["ts", "exp_id", "worker", "score", "ppv", "npv", "spec",
                     "mcc", "brier", "n_test", "status", "description"]) + "\n")


def mutate(cfg: dict):
    """Return (neighbor_config, human_description)."""
    c = json.loads(json.dumps(cfg))
    kind = random.choice([
        "feat_drop", "feat_add", "vol_ratio", "close_pos", "require_up",
        "model", "depth", "lr", "iter", "l2", "min_leaf", "thr"])
    if kind == "feat_drop" and len(c["features"]) > 3:
        drop = random.choice(c["features"]); c["features"].remove(drop)
        return c, f"drop feature {drop}"
    if kind == "feat_add":
        missing = [f for f in FEATURE_COLS if f not in c["features"]]
        if missing:
            add = random.choice(missing); c["features"].append(add)
            return c, f"add feature {add}"
    if kind == "vol_ratio":
        c["min_vol_ratio"] = round(min(4.0, max(1.0, c["min_vol_ratio"] + random.choice([-.25, .25, .5]))), 2)
        return c, f"min_vol_ratio -> {c['min_vol_ratio']}"
    if kind == "close_pos":
        c["min_close_pos"] = round(min(0.9, max(0.0, c["min_close_pos"] + random.choice([-.1, .1]))), 2)
        return c, f"min_close_pos -> {c['min_close_pos']}"
    if kind == "require_up":
        c["require_up"] = not c["require_up"]
        return c, f"require_up -> {c['require_up']}"
    if kind == "model":
        c["model"] = "logreg" if c["model"] == "hgb" else "hgb"
        return c, f"model -> {c['model']}"
    if kind == "depth":
        c["max_depth"] = int(min(6, max(2, c["max_depth"] + random.choice([-1, 1]))))
        return c, f"max_depth -> {c['max_depth']}"
    if kind == "lr":
        c["learning_rate"] = round(min(0.30, max(0.01, c["learning_rate"] * random.choice([0.7, 1.4]))), 4)
        return c, f"learning_rate -> {c['learning_rate']}"
    if kind == "iter":
        c["max_iter"] = int(min(500, max(100, c["max_iter"] + random.choice([-50, 50, 100]))))
        return c, f"max_iter -> {c['max_iter']}"
    if kind == "l2":
        c["l2"] = round(min(1.0, max(0.0, c["l2"] + random.choice([-0.1, 0.1, 0.25]))), 3)
        return c, f"l2 -> {c['l2']}"
    if kind == "min_leaf":
        c["min_leaf"] = int(min(150, max(10, c["min_leaf"] + random.choice([-10, 10, 20]))))
        return c, f"min_leaf -> {c['min_leaf']}"
    if kind == "thr":
        c["decision_thr"] = round(min(0.75, max(0.30, c["decision_thr"] + random.choice([-.05, .05]))), 2)
        return c, f"decision_thr -> {c['decision_thr']}"
    return c, "noop"


def run_searcher(worker: int, max_exps: int, sleep: float):
    random.seed(worker * 7919 + int(time.time()) % 1000)
    os.makedirs(EXP_DIR, exist_ok=True)

    gb = read_global_best()
    if gb is None:                                   # worker 0 establishes baseline
        base = M.DEFAULT_CONFIG
        m = E.evaluate(base)
        eid = f"{int(time.time())}-{worker}"
        write_global_best(base, m.get("score", 0.0), eid)
        log_result(dict(ts=int(time.time()), exp_id=eid, worker=worker,
                        score=m.get("score", 0.0), ppv=round(m.get("ppv", 0), 4),
                        npv=round(m.get("npv", 0), 4), spec=round(m.get("spec", 0), 4),
                        mcc=round(m.get("mcc", 0), 4), brier=round(m.get("brier", 1), 4),
                        n_test=m.get("n_test", 0), status="baseline",
                        description="baseline DEFAULT_CONFIG"))
        local, local_score = base, m.get("score", 0.0)
        print(f"[w{worker}] BASELINE score={local_score:.6f}", flush=True)
    else:
        local, local_score = gb["config"], gb["score"]

    n = 0
    while max_exps == 0 or n < max_exps:
        n += 1
        gb = read_global_best()
        if gb and gb["score"] > local_score:
            local, local_score = gb["config"], gb["score"]   # adopt swarm best
        cand, desc = mutate(local)
        eid = f"{int(time.time()*1000)}-{worker}"
        try:
            m = E.evaluate(cand)
            score = m.get("score", 0.0)
        except Exception as e:                       # a crash never stops the loop
            log_result(dict(ts=int(time.time()), exp_id=eid, worker=worker, score=0.0,
                            ppv=0, npv=0, spec=0, mcc=0, brier=1, n_test=0,
                            status="crash", description=f"{desc} | {type(e).__name__}: {e}"))
            continue
        improved = score > local_score
        if improved:
            local, local_score = cand, score
            adopted = write_global_best(cand, score, eid)
            status = "keep" if adopted else "keep-local"
        else:
            status = "discard"
        log_result(dict(ts=int(time.time()), exp_id=eid, worker=worker,
                        score=round(score, 6), ppv=round(m.get("ppv", 0), 4),
                        npv=round(m.get("npv", 0), 4), spec=round(m.get("spec", 0), 4),
                        mcc=round(m.get("mcc", 0), 4), brier=round(m.get("brier", 1), 4),
                        n_test=m.get("n_test", 0), status=status, description=desc))
        flag = "+" if improved else " "
        print(f"[w{worker}] exp#{n} {flag} score={score:.6f} best={local_score:.6f} | {desc}", flush=True)
        if sleep:
            time.sleep(sleep)
    print(f"[w{worker}] done after {n} experiments. best={local_score:.6f}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--max-exps", type=int, default=0, help="0 = forever (24/7)")
    ap.add_argument("--sleep", type=float, default=0.0)
    ap.add_argument("--rebuild", action="store_true", help="force rebuild events cache")
    args = ap.parse_args()

    build_events(force=args.rebuild)                 # one-time expensive prep
    if args.workers <= 1:
        run_searcher(0, args.max_exps, args.sleep)
    else:
        procs = [mp.Process(target=run_searcher, args=(w, args.max_exps, args.sleep))
                 for w in range(args.workers)]
        for p in procs:
            p.start()
        for p in procs:
            p.join()


if __name__ == "__main__":
    main()
