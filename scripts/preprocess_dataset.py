from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import StratifiedKFold, cross_val_score

MODEL_TYPES = {
    "random_forest": RandomForestClassifier,
    "logistic_regression": LogisticRegression,
}


def train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    model_name: str = "random_forest",
    output_dir: str | Path = "ml/models",
    model_version: str = "v1.0",
):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    model_cls = MODEL_TYPES.get(model_name.lower(), RandomForestClassifier)
    if model_name.lower() == "random_forest":
        model = model_cls(
            n_estimators=200,
            random_state=42,
            class_weight="balanced",
            n_jobs=-1,
        )
    elif model_name.lower() == "logistic_regression":
        model = model_cls(max_iter=1000, random_state=42)
    else:
        model = model_cls(random_state=42)

    model.fit(X_train, y_train)
    joblib.dump(model, output_dir / "ddos_model.pkl")

    metadata = {
        "model_name": model_name,
        "model_version": model_version,
        "trained_at": pd.Timestamp.utcnow().isoformat(),
        "feature_count": int(X_train.shape[1]),
        "status": "trained",
    }
    with (output_dir / "model_metadata.json").open("w", encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2)
    return model


def cross_validate_model(X: pd.DataFrame, y: pd.Series, model_name: str = "random_forest") -> dict[str, float]:
    model_cls = MODEL_TYPES.get(model_name.lower(), RandomForestClassifier)
    if model_name.lower() == "random_forest":
        estimator = model_cls(n_estimators=150, random_state=42, class_weight="balanced")
    elif model_name.lower() == "logistic_regression":
        estimator = model_cls(max_iter=1000, random_state=42)
    else:
        estimator = model_cls(random_state=42)

    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    scores = cross_val_score(estimator, X, y, cv=cv, scoring="f1")
    return {
        "cv_f1_mean": float(scores.mean()),
        "cv_f1_std": float(scores.std()),
        "cv_folds": int(len(scores)),
    }


def train_pipeline(
    dataset_path: str | Path,
    output_dir: str | Path = "ml/models",
    label_column: str = "label",
    model_name: str = "random_forest",
    selected_features: list[str] | None = None,
) -> dict[str, Any]:
    from ml.preprocessing.preprocess import DatasetPreprocessor

    preprocessor = DatasetPreprocessor(
        dataset_path=dataset_path,
        output_dir=output_dir,
        label_column=label_column,
        selected_features=selected_features,
    )
    X_train, X_val, X_test, y_train, y_val, y_test = preprocessor.fit_and_transform()
    model = train_model(X_train, y_train, model_name=model_name, output_dir=output_dir)

    return {
        "train_samples": int(len(X_train)),
        "validation_samples": int(len(X_val)),
        "test_samples": int(len(X_test)),
        "feature_count": int(X_train.shape[1]),
        "model_name": model_name,
        "model_path": str(Path(output_dir) / "ddos_model.pkl"),
        "status": "trained",
    }
