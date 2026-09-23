from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix


def build_confusion_matrix(y_true: pd.Series, y_pred: np.ndarray) -> np.ndarray:
    """Return the binary confusion matrix for the classification output."""
    return confusion_matrix(y_true, y_pred, labels=[0, 1])
