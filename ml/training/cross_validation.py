from __future__ import annotations

from typing import Any

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV


def get_random_forest_param_grid() -> dict[str, list[Any]]:
    """Provide a small default grid for RandomForest tuning using attack detection features."""
    return {
        "n_estimators": [100, 200],
        "max_depth": [None, 8, 16],
        "min_samples_split": [2, 5],
        "class_weight": ["balanced", "balanced_subsample", None],
    }


def tune_random_forest(X, y) -> Any:
    """Tune RandomForest hyperparameters using cross-validation."""
    estimator = RandomForestClassifier(random_state=42)
    grid = GridSearchCV(
        estimator=estimator,
        param_grid=get_random_forest_param_grid(),
        scoring="f1",
        cv=3,
        n_jobs=-1,
    )
    grid.fit(X, y)
    return grid.best_estimator_, grid.best_params_, grid.best_score_
