"""CPU baselines and train-only shrinkage calibration for reconstruction."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

RIDGE_ALPHAS = (0.0, 0.1, 1.0, 10.0, 100.0)
HISTGB_GRID = tuple(
    {
        "max_leaf_nodes": leaves,
        "min_samples_leaf": samples,
        "l2_regularization": l2,
        "learning_rate": 0.05,
        "max_iter": 500,
    }
    for leaves in (15, 31)
    for samples in (100, 500)
    for l2 in (1.0, 10.0)
)

THERMAL_FEATURES = (
    "TMIN", "TMAX", "TMIN_anom", "TMAX_anom", "TEMP_mean", "DTR",
    "es_TMIN", "es_TMAX", "es_range",
)
SEASONAL_FEATURES = ("sin_doy_1", "cos_doy_1", "sin_doy_2", "cos_doy_2")
STATIC_CANDIDATES = ("DEM", "TDI", "longitude", "latitude", "LST_DAY", "LST_NIGHT")


def reference_predictions(frame: pd.DataFrame) -> dict[str, np.ndarray]:
    """Deterministic climatology and Td=Tmin reference predictions."""
    required = {"TD_clim", "TMIN"}
    missing = required - set(frame)
    if missing:
        raise ValueError(f"Missing reference-baseline columns: {sorted(missing)}")
    return {
        "climatology": frame["TD_clim"].to_numpy(dtype=float),
        "td_equals_tmin": frame["TMIN"].to_numpy(dtype=float),
    }


def feature_columns(frame: pd.DataFrame, feature_set: str) -> list[str]:
    autoregressive = feature_set.endswith("_ar")
    base_feature_set = feature_set.removesuffix("_ar")
    if base_feature_set == "tmin":
        wanted = ["TMIN"]
    elif base_feature_set == "thermal":
        wanted = list(THERMAL_FEATURES) + list(SEASONAL_FEATURES)
    elif base_feature_set == "exogenous_full":
        rolling = [
            column for column in frame
            if any(column.startswith(f"{source}_") for source in ("TMIN", "TMAX", "DTR"))
            and any(token in column for token in ("lag", "mean_", "std_", "slope_"))
        ]
        wanted = list(THERMAL_FEATURES) + list(SEASONAL_FEATURES) + list(STATIC_CANDIDATES) + rolling + ["department", "region"]
    else:
        raise ValueError(f"Unknown feature set: {feature_set}")
    if autoregressive:
        wanted += [f"TD_anom_lag{lag}" for lag in (1, 2, 3, 7, 30)]
    columns = [column for column in dict.fromkeys(wanted) if column in frame]
    if not columns:
        raise ValueError(f"Feature set {feature_set!r} has no available columns")
    return columns


def make_estimator(
    model: str,
    frame: pd.DataFrame,
    columns: list[str],
    *,
    params: Mapping[str, Any] | None = None,
    seed: int = 0,
) -> Pipeline:
    params = dict(params or {})
    categorical = [column for column in columns if not pd.api.types.is_numeric_dtype(frame[column])]
    numeric = [column for column in columns if column not in categorical]
    transform = ColumnTransformer(
        [
            ("numeric", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric),
            ("categorical", Pipeline([("impute", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))]), categorical),
        ],
        remainder="drop",
    )
    if model == "ridge":
        regressor = Ridge(alpha=float(params.get("alpha", 1.0)))
    elif model == "histgb":
        regressor = HistGradientBoostingRegressor(random_state=seed, **params)
    else:
        raise ValueError(f"Unsupported baseline model: {model}")
    return Pipeline([("features", transform), ("model", regressor)])


@dataclass
class FittedBaseline:
    estimator: Pipeline
    feature_columns: list[str]
    model: str
    feature_set: str
    params: dict[str, Any]

    def predict_anomaly(self, frame: pd.DataFrame) -> np.ndarray:
        return np.asarray(self.estimator.predict(frame[self.feature_columns]), dtype=float)

    def predict_td(self, frame: pd.DataFrame) -> np.ndarray:
        return self.predict_anomaly(frame) + frame["TD_clim"].to_numpy(dtype=float)


def fit_baseline(
    train: pd.DataFrame,
    *,
    model: str,
    feature_set: str,
    params: Mapping[str, Any] | None = None,
    seed: int = 0,
) -> FittedBaseline:
    columns = feature_columns(train, feature_set)
    usable = train["TD_anom"].notna()
    if not usable.any():
        raise ValueError("No finite TD_anom labels in training data")
    estimator = make_estimator(model, train, columns, params=params, seed=seed)
    estimator.fit(train.loc[usable, columns], train.loc[usable, "TD_anom"])
    return FittedBaseline(estimator, columns, model, feature_set, dict(params or {}))


def parameter_grid(model: str) -> Iterable[dict[str, Any]]:
    if model == "ridge":
        return ({"alpha": alpha} for alpha in RIDGE_ALPHAS)
    if model == "histgb":
        return iter(HISTGB_GRID)
    raise ValueError(f"Unsupported baseline model: {model}")


def fit_shrinkage_alpha(predictions: pd.DataFrame) -> dict[str, float]:
    """Fit alpha in clim + alpha*(pred-clim), independently by department."""
    required = {"department", "TD_obs", "TD_clim", "TD_pred"}
    missing = required - set(predictions)
    if missing:
        raise ValueError(f"Missing calibration columns: {sorted(missing)}")
    result: dict[str, float] = {}
    for department, group in predictions.groupby("department", sort=True):
        x = group["TD_pred"].to_numpy(dtype=float) - group["TD_clim"].to_numpy(dtype=float)
        y = group["TD_obs"].to_numpy(dtype=float) - group["TD_clim"].to_numpy(dtype=float)
        finite = np.isfinite(x) & np.isfinite(y)
        denom = float(np.dot(x[finite], x[finite]))
        alpha = float(np.dot(x[finite], y[finite]) / denom) if denom > 0 else 0.0
        result[str(department)] = float(np.clip(alpha, 0.0, 1.0))
    return result


def apply_shrinkage(predictions: pd.DataFrame, alphas: Mapping[str, float]) -> pd.Series:
    alpha = predictions["department"].map(alphas)
    if alpha.isna().any():
        missing = sorted(predictions.loc[alpha.isna(), "department"].astype(str).unique())
        raise ValueError(f"No calibration alpha for departments: {missing}")
    return predictions["TD_clim"] + alpha * (predictions["TD_pred"] - predictions["TD_clim"])
