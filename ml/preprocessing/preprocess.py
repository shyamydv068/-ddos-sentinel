from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from ml.preprocessing.feature_selection import select_features
from ml.preprocessing.feature_scaling import fit_scaler, transform_features
from ml.preprocessing.label_encoding import encode_labels, map_attack_labels


DEFAULT_LABEL_COLUMN = "label"
DEFAULT_OUTPUT_DIR = Path("ml/models")


class DatasetPreprocessor:
    """Build a reusable preprocessing pipeline for CICDDoS2019-style network data."""

    def __init__(
        self,
        dataset_path: str | Path,
        output_dir: str | Path = DEFAULT_OUTPUT_DIR,
        label_column: str = DEFAULT_LABEL_COLUMN,
        selected_features: list[str] | None = None,
    ) -> None:
        self.dataset_path = Path(dataset_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.label_column = label_column
        self.selected_features = selected_features

    def load_dataset(self) -> pd.DataFrame:
        if not self.dataset_path.exists():
            raise FileNotFoundError(f"Dataset not found: {self.dataset_path}")
        df = pd.read_csv(self.dataset_path)
        df.columns = [
            str(col).strip().lower().replace(" ", "_").replace("-", "_")
            for col in df.columns
        ]
        return df

    def clean_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df = df.dropna(axis=1, how="all")

        for col in df.columns:
            if df[col].dtype.kind in "ifc":
                df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.dropna(how="any")
        df = df.drop_duplicates()
        df = df.reset_index(drop=True)
        return df

    def prepare_data(self) -> tuple[pd.DataFrame, pd.Series, list[str], dict[str, Any]]:
        df = self.load_dataset()
        df = self.clean_dataset(df)

        if self.label_column not in df.columns:
            label_candidates = [c for c in df.columns if "label" in c or "class" in c or "target" in c]
            if not label_candidates:
                raise ValueError("No label column found; expected 'label' or similar.")
            self.label_column = label_candidates[0]

        df = map_attack_labels(df, label_column=self.label_column)
        df = encode_labels(df, label_column=self.label_column)

        feature_columns = select_features(df, feature_columns=self.selected_features, label_column=self.label_column)
        X = df[feature_columns]
        y = df[self.label_column]

        stats = {
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "selected_features": feature_columns,
            "label_distribution": y.value_counts().to_dict(),
        }
        return X, y, feature_columns, stats

    def fit_and_transform(
        self,
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series]:
        X, y, feature_columns, stats = self.prepare_data()

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        X_train, X_val, y_train, y_val = train_test_split(
            X_train, y_train, test_size=0.25, random_state=42, stratify=y_train
        )

        scaler = StandardScaler()
        X_train_scaled = transform_features(X_train, scaler, fit=True)
        X_val_scaled = transform_features(X_val, scaler, fit=False)
        X_test_scaled = transform_features(X_test, scaler, fit=False)

        scaler_path = self.output_dir / "scaler.pkl"
        joblib.dump(scaler, scaler_path)

        self.save_metadata(
            {
                "feature_columns": feature_columns,
                "label_column": self.label_column,
                "rows": int(len(X)),
                "train_rows": int(len(X_train)),
                "validation_rows": int(len(X_val)),
                "test_rows": int(len(X_test)),
                "stats": stats,
            }
        )

        return X_train_scaled, X_val_scaled, X_test_scaled, y_train, y_val, y_test

    def save_metadata(self, payload: dict[str, Any]) -> None:
        metadata_path = self.output_dir / "preprocessing_metadata.json"
        with metadata_path.open("w", encoding="utf-8") as file_obj:
            json.dump(payload, file_obj, indent=2, default=str)


def run_preprocessing(
    dataset_path: str | Path,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
    label_column: str = DEFAULT_LABEL_COLUMN,
    selected_features: list[str] | None = None,
) -> dict[str, Any]:
    preprocessor = DatasetPreprocessor(
        dataset_path=dataset_path,
        output_dir=output_dir,
        label_column=label_column,
        selected_features=selected_features,
    )
    X_train, X_valid, X_test, y_train, y_valid, y_test = preprocessor.fit_and_transform()
    return {
        "train_samples": int(len(X_train)),
        "validation_samples": int(len(X_valid)),
        "test_samples": int(len(X_test)),
        "label_column": preprocessor.label_column,
        "feature_count": int(X_train.shape[1]),
    }
