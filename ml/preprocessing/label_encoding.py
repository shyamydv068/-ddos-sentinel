from __future__ import annotations

import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler


def fit_scaler(X: pd.DataFrame, scaler: StandardScaler | None = None) -> StandardScaler:
    """Fit a standard scaler for selected flow features."""
    scaler = scaler or StandardScaler()
    scaler.fit(X)
    return scaler


def transform_features(X: pd.DataFrame, scaler: StandardScaler, fit: bool = False) -> pd.DataFrame:
    """Transform feature values using the supplied scaler."""
    if fit:
        scaler = fit_scaler(X, scaler)
    return pd.DataFrame(scaler.transform(X), columns=X.columns, index=X.index)


def save_scaler(scaler: StandardScaler, output_path: str) -> None:
    joblib.dump(scaler, output_path)
