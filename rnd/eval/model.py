"""
R&D AutoResearch — model.py   [MUTABLE — this is the ONLY file experiments edit]
=============================================================================
Karpathy `train.py` equivalent. The autoresearch loop mutates DEFAULT_CONFIG
(features used, event-selection thresholds, classifier hyperparameters, decision
threshold) and keeps the change only if RND_Northstar improves on held-out days.

A "config" fully specifies one experiment. Everything here is fair game.
"""
from __future__ import annotations
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from prepare import FEATURE_COLS  # the full menu of available features

# The current research frontier. The loop hill-climbs on this.
DEFAULT_CONFIG = {
    # ---- which features the classifier sees (subset of FEATURE_COLS) ----
    "features": list(FEATURE_COLS),
    # ---- event selection: which rows count as "a bullish plot fired" ----
    "min_vol_ratio": 1.5,   # volume surge gate (kinetic energy proxy)
    "min_close_pos": 0.5,   # closed in upper half of range
    "require_up": True,     # ret1 > 0
    # ---- model ----
    "model": "hgb",         # "hgb" | "logreg"
    "max_depth": 3,
    "learning_rate": 0.08,
    "max_iter": 200,
    "l2": 0.0,
    "min_leaf": 30,
    # ---- decision ----
    "decision_thr": 0.5,    # P(launch) above this => predict LAUNCH
}


def build_model(cfg: dict):
    if cfg.get("model") == "logreg":
        return make_pipeline(StandardScaler(),
                             LogisticRegression(max_iter=1000, C=1.0 / max(cfg.get("l2", 0.0), 1e-6)
                                                if cfg.get("l2", 0.0) > 0 else 1.0))
    return HistGradientBoostingClassifier(
        max_depth=cfg.get("max_depth", 3),
        learning_rate=cfg.get("learning_rate", 0.08),
        max_iter=cfg.get("max_iter", 200),
        l2_regularization=cfg.get("l2", 0.0),
        min_samples_leaf=cfg.get("min_leaf", 30),
        random_state=0,
    )


def event_mask(df, cfg: dict):
    m = df["vol_ratio"] >= cfg.get("min_vol_ratio", 1.5)
    m &= df["close_pos"] >= cfg.get("min_close_pos", 0.5)
    if cfg.get("require_up", True):
        m &= df["ret1"] > 0
    return m
