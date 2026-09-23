from __future__ import annotations

from typing import Iterable

import pandas as pd

DEFAULT_NETWORK_FEATURES = [
    "packet_count",
    "byte_count",
    "flow_duration",
    "source_port",
    "destination_port",
    "protocol_code",
    "packet_rate",
    "byte_rate",
    "unique_src_ips",
    "connection_count",
]


def select_features(
    df: pd.DataFrame,
    feature_columns: Iterable[str] | None = None,
    label_column: str | None = None,
) -> list[str]:
    """Choose the most relevant features for network-flow DDoS classification."""
    candidate_columns = list(df.columns)
    if label_column and label_column in candidate_columns:
        candidate_columns = [c for c in candidate_columns if c != label_column]

    if feature_columns is not None:
        requested = [c for c in feature_columns if c in df.columns]
        if requested:
            return requested

    available = [c for c in DEFAULT_NETWORK_FEATURES if c in df.columns]
    if available:
        return available

    numeric = df.select_dtypes(include="number").columns.tolist()
    selected = [c for c in numeric if c not in {label_column}]
    return selected[:10]
