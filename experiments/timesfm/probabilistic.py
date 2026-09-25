"""Metricas probabilisticas sobre los nueve deciles que devuelve TimesFM.

TimesFM entrega los deciles 0,1 a 0,9 (`timesfm3_forecaster.py:54-56` y el
``config.json`` del checkpoint). Eso alcanza para la perdida pinball y para una
aproximacion del CRPS, pero **no** para intervalos del 90 % o del 95 %: el mas
ancho que se puede formar es el 80 % entre q10 y q90. Los rivales de este
benchmark (climatologia, el metodo de Palacios, la TCN) son deterministas, asi
que estas metricas describen a TimesFM, no lo comparan.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

LEVELS = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], dtype=np.float64)
COLUMNS = tuple(f"q{int(round(level * 100)):02d}" for level in LEVELS)


def pinball(observed: np.ndarray, quantiles: np.ndarray, levels: np.ndarray = LEVELS) -> np.ndarray:
    """Perdida pinball media por nivel.

    ``quantiles`` tiene forma ``(n, k)`` y ``observed`` forma ``(n,)``.
    """
    observed = np.asarray(observed, dtype=np.float64).reshape(-1, 1)
    quantiles = np.asarray(quantiles, dtype=np.float64)
    if quantiles.shape[1] != levels.size:
        raise ValueError(f"se esperaban {levels.size} niveles y llegaron {quantiles.shape[1]}")
    error = observed - quantiles
    loss = np.maximum(levels * error, (levels - 1.0) * error)
    return np.nanmean(loss, axis=0)


def crps_from_quantiles(observed: np.ndarray, quantiles: np.ndarray, levels: np.ndarray = LEVELS) -> float:
    """Aproximacion del CRPS por cuadratura sobre los niveles disponibles.

    Con una rejilla uniforme de K niveles, ``CRPS ~= (2/K) * sum_k pinball_k``. Es
    una aproximacion, no el CRPS exacto: el paquete no expone una distribucion
    continua ni muestras, solo nueve deciles, de modo que las colas por debajo de
    q10 y por encima de q90 no entran en la cuenta y el valor queda sesgado a la
    baja. Se reporta como ``crps_aprox`` por ese motivo.
    """
    losses = pinball(observed, quantiles, levels)
    return float(2.0 * losses.sum() / levels.size)


def interval_coverage(
    observed: np.ndarray, lower: np.ndarray, upper: np.ndarray
) -> dict[str, float]:
    """Cobertura empirica y anchura media del intervalo mas ancho disponible."""
    observed = np.asarray(observed, dtype=np.float64)
    lower = np.asarray(lower, dtype=np.float64)
    upper = np.asarray(upper, dtype=np.float64)
    valid = np.isfinite(observed) & np.isfinite(lower) & np.isfinite(upper)
    if not valid.any():
        return {"cobertura_80": np.nan, "anchura_80": np.nan, "n": 0}
    inside = (observed[valid] >= lower[valid]) & (observed[valid] <= upper[valid])
    return {
        "cobertura_80": float(inside.mean()),
        "anchura_80": float(np.mean(upper[valid] - lower[valid])),
        "n": int(valid.sum()),
    }


def probabilistic_metrics(frame: pd.DataFrame, *, obs_col: str = "TD_obs") -> dict[str, float]:
    """Resumen probabilistico de un marco con las nueve columnas de deciles."""
    missing = [name for name in COLUMNS if name not in frame.columns]
    if missing:
        raise ValueError(f"faltan columnas de cuantiles: {missing}")
    observed = frame[obs_col].to_numpy(dtype=np.float64)
    quantiles = frame[list(COLUMNS)].to_numpy(dtype=np.float64)
    finite = np.isfinite(observed) & np.isfinite(quantiles).all(axis=1)
    observed, quantiles = observed[finite], quantiles[finite]

    losses = pinball(observed, quantiles)
    out: dict[str, float] = {f"pinball_{name}": float(value) for name, value in zip(COLUMNS, losses)}
    out["pinball_medio"] = float(losses.mean())
    out["crps_aprox"] = crps_from_quantiles(observed, quantiles)
    out.update(interval_coverage(observed, quantiles[:, 0], quantiles[:, -1]))
    # Cruce de cuantiles antes de ordenar: el paquete ordena por defecto
    # (`sort_quantiles=True`), asi que esto deberia ser 0 y sirve de control.
    out["fraccion_cruces"] = float(np.mean(np.diff(quantiles, axis=1) < 0))
    return out
