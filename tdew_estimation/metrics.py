"""
tdew_estimation.metrics

Shared regression-scoring utilities for TD (dewpoint) baselines/models.

Formulas match ``HPC_code_tunning/backtest.py::_metrics``/``_score_all``
(the evaluation regime documented in ``docs/evaluation_methodology.md``) so
numbers from different experiments stay comparable in format, without
importing from ``HPC_code_tunning`` (a different, autoregressive gap-fill
evaluation regime with its own leakage rules).
"""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence

import numpy as np
import pandas as pd


def regression_metrics(pred: np.ndarray, obs: np.ndarray) -> Dict[str, float]:
    """n, rmse, mae, bias, r for ``pred`` vs ``obs`` over finite (pred - obs) pairs."""
    pred = np.asarray(pred, dtype=float)
    obs = np.asarray(obs, dtype=float)
    err = pred - obs
    finite = np.isfinite(err)
    err = err[finite]
    n = err.size
    if n == 0:
        return {"n": 0, "rmse": np.nan, "mae": np.nan, "bias": np.nan, "r": np.nan}
    p, o = pred[finite], obs[finite]
    r = float(np.corrcoef(p, o)[0, 1]) if n > 1 and np.std(p) > 0 and np.std(o) > 0 else np.nan
    return {
        "n": int(n),
        "rmse": float(np.sqrt(np.mean(err**2))),
        "mae": float(np.mean(np.abs(err))),
        "bias": float(np.mean(err)),
        "r": r,
    }


def _score_group(
    df: pd.DataFrame,
    *,
    obs_col: str,
    method_cols: Dict[str, str],
    clim_col: str,
) -> List[Dict[str, object]]:
    obs = df[obs_col].to_numpy(dtype=float)
    clim_rmse = regression_metrics(df[clim_col].to_numpy(dtype=float), obs)["rmse"]
    rows: List[Dict[str, object]] = []
    for method, col in method_cols.items():
        m = regression_metrics(df[col].to_numpy(dtype=float), obs)
        m["method"] = method
        m["skill_vs_clim"] = (1.0 - m["rmse"] / clim_rmse) if clim_rmse and np.isfinite(clim_rmse) else np.nan
        rows.append(m)
    return rows


def score_methods(
    df: pd.DataFrame,
    *,
    obs_col: str,
    method_cols: Dict[str, str],
    clim_col: str,
    group_cols: Optional[Sequence[str]] = None,
    pooled_group_value: str = "ALL",
) -> pd.DataFrame:
    """Score every ``method_cols`` prediction column against ``obs_col``.

    If ``group_cols`` is given (e.g. ``["site"]``), returns one row per
    ``(group..., method)`` plus a pooled row per method with the group
    column(s) set to ``pooled_group_value`` (all rows, ignoring grouping).
    ``skill_vs_clim = 1 - rmse_method / rmse_clim`` is computed within each
    group (never mixed across groups), matching ``HPC_code_tunning``'s
    per-split skill_vs_clim.
    """
    cols = ["n", "rmse", "mae", "bias", "r", "skill_vs_clim", "method"]

    if not group_cols:
        rows = _score_group(df, obs_col=obs_col, method_cols=method_cols, clim_col=clim_col)
        return pd.DataFrame(rows)[cols]

    group_cols = list(group_cols)
    all_rows: List[Dict[str, object]] = []
    for key, gdf in df.groupby(group_cols, sort=True):
        key_tuple = key if isinstance(key, tuple) else (key,)
        for row in _score_group(gdf, obs_col=obs_col, method_cols=method_cols, clim_col=clim_col):
            row.update(dict(zip(group_cols, key_tuple)))
            all_rows.append(row)

    for row in _score_group(df, obs_col=obs_col, method_cols=method_cols, clim_col=clim_col):
        row.update({g: pooled_group_value for g in group_cols})
        all_rows.append(row)

    return pd.DataFrame(all_rows)[group_cols + cols]


class MetricsAccum:
    """Streaming counterpart of ``regression_metrics`` for datasets too large to
    hold in memory at once (e.g. a whole department, ~30-300k cells x ~13
    years). Call ``add(pred, obs)`` once per chunk (e.g. per ``id_bucket``),
    then ``finalize()`` for the same n/rmse/mae/bias/r as ``regression_metrics``
    would give on the concatenated data — computed from running sums instead
    (same bucketed-accumulation philosophy as ``pipeline.gold``/``pipeline.
    normalize``, so no chunk boundary changes the result)."""

    def __init__(self) -> None:
        self.n = 0
        self.sum_err = 0.0
        self.sum_err2 = 0.0
        self.sum_abserr = 0.0
        self.sum_p = 0.0
        self.sum_o = 0.0
        self.sum_p2 = 0.0
        self.sum_o2 = 0.0
        self.sum_po = 0.0

    def add(self, pred: np.ndarray, obs: np.ndarray) -> None:
        pred = np.asarray(pred, dtype=float)
        obs = np.asarray(obs, dtype=float)
        finite = np.isfinite(pred) & np.isfinite(obs)
        p, o = pred[finite], obs[finite]
        if p.size == 0:
            return
        err = p - o
        self.n += err.size
        self.sum_err += float(err.sum())
        self.sum_err2 += float((err**2).sum())
        self.sum_abserr += float(np.abs(err).sum())
        self.sum_p += float(p.sum())
        self.sum_o += float(o.sum())
        self.sum_p2 += float((p**2).sum())
        self.sum_o2 += float((o**2).sum())
        self.sum_po += float((p * o).sum())

    def finalize(self) -> Dict[str, float]:
        if self.n == 0:
            return {"n": 0, "rmse": np.nan, "mae": np.nan, "bias": np.nan, "r": np.nan}
        n = self.n
        mp, mo = self.sum_p / n, self.sum_o / n
        varp = self.sum_p2 / n - mp**2
        varo = self.sum_o2 / n - mo**2
        cov = self.sum_po / n - mp * mo
        r = float(cov / np.sqrt(varp * varo)) if varp > 0 and varo > 0 else np.nan
        return {
            "n": int(n),
            "rmse": float(np.sqrt(self.sum_err2 / n)),
            "mae": float(self.sum_abserr / n),
            "bias": float(self.sum_err / n),
            "r": r,
        }


class NormalEquationsAccum:
    """Streaming (weighted) least-squares accumulator: ``y ~ X @ beta``.

    Accumulates ``X'WX`` (``p x p``) and ``X'Wy`` (``p``,) chunk by chunk (one
    ``id_bucket`` at a time), so fitting a department- or multi-site-scale
    regression never requires the full design matrix in memory — same
    philosophy as ``tdew_estimation.climatology``'s fixed accumulator.
    Mathematically equivalent to ``statsmodels.WLS(y, X, weights=w).fit()``
    on the concatenated data (up to the ``ridge`` regularization added at
    ``fit()`` time for numerical stability with collinear lag features).
    """

    def __init__(self, feature_names: Sequence[str]) -> None:
        self.feature_names = list(feature_names)
        p = len(self.feature_names)
        self.XtX = np.zeros((p, p), dtype=np.float64)
        self.Xty = np.zeros(p, dtype=np.float64)
        self.n = 0

    def add(self, X: np.ndarray, y: np.ndarray, w: Optional[np.ndarray] = None) -> None:
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64)
        w = np.ones(len(y), dtype=np.float64) if w is None else np.asarray(w, dtype=np.float64)
        Xw = X * w[:, None]
        self.XtX += Xw.T @ X
        self.Xty += Xw.T @ y
        self.n += len(y)

    def fit(self, *, ridge: float = 1e-6) -> Dict[str, float]:
        """Solve ``(X'WX + ridge*I) beta = X'Wy``. Returns ``{feature_name: coef}``."""
        p = self.XtX.shape[0]
        beta = np.linalg.solve(self.XtX + ridge * np.eye(p), self.Xty)
        return dict(zip(self.feature_names, beta.tolist()))


class OLSAccum:
    """Streaming sufficient-statistics accumulator for simple OLS ``y ~ a + b*x``.

    Same closed-form approach as ``HPC_code_tunning/backtest.py::_OLSAccum``
    (reimplemented here so this module has no dependency on ``HPC_code_tunning``,
    a separate evaluation regime). Lets a per-site fit accumulate over buckets
    without holding the full site in memory at once.
    """

    def __init__(self) -> None:
        self.n = 0.0
        self.sx = 0.0
        self.sy = 0.0
        self.sxx = 0.0
        self.sxy = 0.0

    def add(self, x: np.ndarray, y: np.ndarray) -> None:
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
        self.n += x.size
        self.sx += float(x.sum())
        self.sy += float(y.sum())
        self.sxx += float((x * x).sum())
        self.sxy += float((x * y).sum())

    def fit(self) -> tuple[float, float]:
        """Return (intercept, slope). Falls back to (mean(y), 0) if singular/empty."""
        denom = self.n * self.sxx - self.sx * self.sx
        if self.n < 2 or abs(denom) < 1e-9:
            return (self.sy / self.n if self.n else 0.0, 0.0)
        b = (self.n * self.sxy - self.sx * self.sy) / denom
        a = (self.sy - b * self.sx) / self.n
        return (a, b)
