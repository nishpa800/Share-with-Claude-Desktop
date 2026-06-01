"""
R&D AutoResearch — evaluate.py   [SACRED — the ground-truth metric]
=============================================================================
Karpathy `evaluate_bpb` equivalent. Walk-forward: train on earlier sessions,
score on the most-recent held-out sessions. Returns RND_Northstar.

RND_Northstar = 0.30*PPV + 0.20*NPV + 0.20*MCC_norm + 0.15*Specificity + 0.15*(1-Brier)

Specificity is weighted on purpose: the expensive error in Anish's thesis is the
BULL TRAP (a bullish plot that rolls into a bearish leg). Higher = better.
"""
from __future__ import annotations
import numpy as np
from sklearn.metrics import brier_score_loss, matthews_corrcoef

import model as M
from prepare import load_events

HOLDOUT_DAYS = 20   # most-recent N unique sessions are out-of-sample


def _confusion_metrics(y, pred, proba):
    tp = int(np.sum((pred == 1) & (y == 1)))
    tn = int(np.sum((pred == 0) & (y == 0)))
    fp = int(np.sum((pred == 1) & (y == 0)))
    fn = int(np.sum((pred == 0) & (y == 1)))
    ppv = tp / (tp + fp) if (tp + fp) else 0.0
    npv = tn / (tn + fn) if (tn + fn) else 0.0
    sens = tp / (tp + fn) if (tp + fn) else 0.0
    spec = tn / (tn + fp) if (tn + fp) else 0.0
    mcc = matthews_corrcoef(y, pred) if len(np.unique(y)) > 1 and len(np.unique(pred)) > 1 else 0.0
    try:
        brier = brier_score_loss(y, proba)
    except Exception:
        brier = 1.0
    return dict(ppv=ppv, npv=npv, sens=sens, spec=spec, mcc=mcc, brier=brier,
                tp=tp, tn=tn, fp=fp, fn=fn)


def northstar(m: dict) -> float:
    mcc_norm = (m["mcc"] + 1.0) / 2.0
    return (0.30 * m["ppv"] + 0.20 * m["npv"] + 0.20 * mcc_norm
            + 0.15 * m["spec"] + 0.15 * (1.0 - m["brier"]))


def evaluate(cfg: dict, events=None) -> dict:
    df = load_events() if events is None else events
    df = df[M.event_mask(df, cfg)].copy()
    if len(df) < 200:
        return dict(score=0.0, reason="too_few_events", n_events=len(df))

    dates = np.sort(df["date"].unique())
    if len(dates) <= HOLDOUT_DAYS + 5:
        return dict(score=0.0, reason="too_few_dates", n_events=len(df))
    cutoff = dates[-HOLDOUT_DAYS]
    feats = cfg["features"]
    tr = df[df["date"] < cutoff]
    te = df[df["date"] >= cutoff]
    if tr["label"].nunique() < 2 or len(te) < 30:
        return dict(score=0.0, reason="degenerate_split", n_events=len(df))

    Xtr, ytr = tr[feats].to_numpy(), tr["label"].to_numpy().astype(int)
    Xte, yte = te[feats].to_numpy(), te["label"].to_numpy().astype(int)

    clf = M.build_model(cfg)
    clf.fit(Xtr, ytr)
    proba = clf.predict_proba(Xte)[:, 1]
    pred = (proba >= cfg.get("decision_thr", 0.5)).astype(int)

    m = _confusion_metrics(yte, pred, proba)
    m["score"] = round(northstar(m), 6)
    m["n_train"], m["n_test"] = len(tr), len(te)
    m["test_base_rate"] = round(float(yte.mean()), 4)
    return m


if __name__ == "__main__":
    import json
    print(json.dumps(evaluate(M.DEFAULT_CONFIG), indent=2, default=float))
