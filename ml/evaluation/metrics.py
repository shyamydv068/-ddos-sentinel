from __future__ import annotations

from typing import Any

import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_val_score


def run_cross_validation(model: Any, X: pd.DataFrame, y: pd.Series, cv_folds: int = 5) -> dict[str, float]:
    """Perform stratified k-fold cross-validation using the provided model."""
    cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)
    scores = cross_val_score(model, X, y, cv=cv, scoring="f1")
    return {
        "mean_f1": float(scores.mean()),
        "std_f1": float(scores.std()),
        "fold_count": int(len(scores)),
    }
