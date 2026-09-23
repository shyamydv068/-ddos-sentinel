from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from ml.evaluation.confusion_matrix import build_confusion_matrix
from ml.evaluation.metrics import compute_metrics


def evaluate_model(
    model_path: str | Path,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    output_dir: str | Path = "ml/models",
) -> dict[str, Any]:
    """Load a trained model, predict on test data, and write evaluation metrics to disk."""
    model = joblib.load(model_path)
    y_pred = model.predict(X_test)

    try:
        y_score = model.predict_proba(X_test)[:, 1]
    except AttributeError:
        y_score = y_pred

    metrics = compute_metrics(y_test, y_pred, y_score)
    confusion = build_confusion_matrix(y_test, y_pred)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    metadata_path = output_dir / "model_metadata.json"
    existing = {}
    if metadata_path.exists():
        with metadata_path.open("r", encoding="utf-8") as fh:
            existing = json.load(fh)

    payload = {
        **existing,
        "model_name": existing.get("model_name", "RandomForest"),
        "model_version": existing.get("model_version", "v1.0"),
        "accuracy": metrics.get("accuracy", 0.0),
        "precision": metrics.get("precision", 0.0),
        "recall": metrics.get("recall", 0.0),
        "f1_score": metrics.get("f1_score", 0.0),
        "roc_auc": metrics.get("roc_auc", 0.0),
        "false_positive_rate": metrics.get("false_positive_rate", 0.0),
        "confusion_matrix": confusion.tolist(),
        "evaluation_status": "completed",
    }

    with metadata_path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)

    return payload
