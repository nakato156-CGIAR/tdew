"""Leak-safe direct and autoregressive reconstruction rollouts."""

from __future__ import annotations

from collections import deque
from typing import Callable, Mapping, Sequence

import numpy as np
import pandas as pd

from .data import AR_LAGS

StepPredictor = Callable[[pd.DataFrame], np.ndarray]


def direct_rollout(hidden: pd.DataFrame, predict: StepPredictor) -> np.ndarray:
    """Predict a hidden block without exposing TD or TD_anom to the model."""
    forbidden = [column for column in hidden if column == "TD" or column.startswith("TD_anom")]
    safe = hidden.drop(columns=forbidden)
    result = np.asarray(predict(safe), dtype=float)
    if result.shape != (len(hidden),):
        raise ValueError(f"Predictor returned shape {result.shape}; expected {(len(hidden),)}")
    return result


def recursive_rollout(
    history: pd.DataFrame,
    hidden: pd.DataFrame,
    predict: StepPredictor,
    *,
    lags: Sequence[int] = AR_LAGS,
) -> np.ndarray:
    """Roll forward per ID using predictions for every hidden-block TD lag.

    ``history`` must end immediately before the hidden block and may contain
    observed ``TD_anom``. The hidden frame's observed TD columns are dropped
    before prediction. The callback receives one row with TD_anom_lag{n}.
    """
    if "TD_anom" not in history:
        raise ValueError("history must contain observed TD_anom")
    required_history = max(lags)
    predictions = pd.Series(index=hidden.index, dtype=float)
    for location_id, future in hidden.groupby("ID", sort=False):
        past = history.loc[history["ID"] == location_id].sort_values("date")["TD_anom"].dropna().to_numpy(dtype=float)
        if len(past) < required_history:
            raise ValueError(f"ID {location_id} has {len(past)} history rows; {required_history} required")
        state = deque(past[-required_history:].tolist(), maxlen=required_history)
        for index, row in future.sort_values("date").iterrows():
            safe = row.drop(labels=[c for c in row.index if c == "TD" or c == "TD_anom" or c.startswith("TD_anom_lag")])
            one = safe.to_frame().T
            for lag in lags:
                one[f"TD_anom_lag{lag}"] = state[-lag]
            prediction = np.asarray(predict(one), dtype=float)
            if prediction.shape not in ((1,), (1, 1)):
                raise ValueError("Recursive predictor must return one value for one input row")
            value = float(prediction.reshape(-1)[0])
            predictions.loc[index] = value
            state.append(value)
    return predictions.loc[hidden.index].to_numpy(dtype=float)


def teacher_forcing_forbidden_columns(columns: Sequence[str]) -> tuple[str, ...]:
    """Return observed target columns that must be removed inside a holdout."""
    return tuple(column for column in columns if column == "TD" or column == "TD_anom")


def recursive_lag_values(history: Sequence[float], lags: Sequence[int] = AR_LAGS) -> Mapping[str, float]:
    if len(history) < max(lags):
        raise ValueError(f"At least {max(lags)} prior predictions/observations are required")
    return {f"TD_anom_lag{lag}": float(history[-lag]) for lag in lags}

