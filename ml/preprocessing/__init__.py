from __future__ import annotations

from typing import Any

import pandas as pd


def map_attack_labels(df: pd.DataFrame, label_column: str = "label") -> pd.DataFrame:
    """Standardize common attack labels into a binary attack/not-attack form."""
    if label_column not in df.columns:
        return df

    cleaned = df.copy()
    label_map = {
        "benign": 0,
        "normal": 0,
        "background": 0,
        "ddos": 1,
        "dos": 1,
        "syn_flood": 1,
        "udp_flood": 1,
        "http_flood": 1,
        "icmp_flood": 1,
        "attack": 1,
        "malicious": 1,
    }

    cleaned[label_column] = cleaned[label_column].astype(str).str.strip().str.lower()
    cleaned[label_column] = cleaned[label_column].map(label_map).fillna(cleaned[label_column])

    # convert string labels to numeric if a custom mapping isn't available
    try:
        cleaned[label_column] = pd.to_numeric(cleaned[label_column], errors="raise")
    except (TypeError, ValueError):
        cleaned[label_column] = cleaned[label_column].map({
            "benign": 0,
            "normal": 0,
            "attack": 1,
            "ddos": 1,
            "dos": 1,
        }).fillna(0)

    return cleaned


def encode_labels(df: pd.DataFrame, label_column: str = "label") -> pd.DataFrame:
    """Encode labels to integer categories required by ML models."""
    if label_column not in df.columns:
        return df

    cleaned = df.copy()
    cleaned[label_column] = pd.to_numeric(cleaned[label_column], errors="coerce")
    cleaned = cleaned.dropna(subset=[label_column])
    cleaned[label_column] = cleaned[label_column].astype(int)
    return cleaned


def build_label_mapping(raw_values: list[Any]) -> dict[str, int]:
    unique_values = list(dict.fromkeys(str(v).strip().lower() for v in raw_values if pd.notna(v)))
    mapping = {value: idx for idx, value in enumerate(unique_values)}
    return mapping
