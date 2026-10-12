"""Canonical-table checks, deterministic panels and causal thermal features."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np
import pandas as pd

from .protocol import ProtocolSpec

PARITY_TOLERANCE_C = 1e-4
QC_RANGE_C = (-25.0, 30.0)
ROLLING_WINDOWS = (3, 7, 14, 30)
AR_LAGS = (1, 2, 3, 7, 30)

STATIC_FEATURES = ("DEM", "TDI", "longitude", "latitude", "LST_DAY", "LST_NIGHT")


@dataclass(frozen=True)
class AuditResult:
    coordinate_hash: str
    n_ids: int
    n_rows_compared: int
    max_tmin_difference: float


def fit_train_standardization(
    frame: pd.DataFrame, spec: ProtocolSpec, columns: Iterable[str]
) -> dict[str, dict[str, float]]:
    """Compute mean/std from protocol training years only."""
    train = frame.loc[spec.train_mask(frame["date"])]
    stats: dict[str, dict[str, float]] = {}
    for column in columns:
        values = train[column].dropna().to_numpy(dtype=float)
        if values.size == 0:
            raise ValueError(f"No training values for {column}")
        stats[column] = {"mean": float(values.mean()), "std": float(values.std(ddof=0))}
    return stats


def apply_standardization(
    frame: pd.DataFrame, stats: dict[str, dict[str, float]], *, suffix: str = "_norm"
) -> pd.DataFrame:
    out = frame.copy()
    for column, values in stats.items():
        scale = values["std"]
        out[f"{column}{suffix}"] = 0.0 if scale == 0 else (out[column] - values["mean"]) / scale
    return out


def coordinate_hash(frame: pd.DataFrame) -> str:
    frame = canonicalize_columns(frame)
    required = ["ID", "longitude", "latitude"]
    _require_columns(frame, required)
    coords = frame[required].drop_duplicates().sort_values("ID")
    if coords["ID"].duplicated().any():
        raise ValueError("An ID maps to more than one coordinate")
    payload = coords.to_csv(index=False, float_format="%.10f", lineterminator="\n").encode()
    return hashlib.sha256(payload).hexdigest()


def audit_sources(
    historical: pd.DataFrame,
    silver: pd.DataFrame,
    *,
    parity_start: str = "2002-01-01",
    parity_end: str = "2016-12-31",
    tolerance: float = PARITY_TOLERANCE_C,
) -> AuditResult:
    """Fail on coordinate/ID/calendar mismatch or TMIN disagreement.

    Both inputs use canonical names: ID, date, TMIN, longitude and latitude.
    Historical may contain TD; silver may contain TMAX. Units are validated as
    Celsius using broad physical limits before exact overlap parity is checked.
    """
    historical = canonicalize_columns(historical)
    silver = canonicalize_columns(silver)
    _require_columns(historical, ["ID", "date", "TMIN"])
    _require_columns(silver, ["ID", "date", "TMIN", "longitude", "latitude"])
    h = historical.copy()
    s = silver.copy()
    h["date"] = pd.to_datetime(h["date"])
    s["date"] = pd.to_datetime(s["date"])
    _validate_unique_dense(h, "historical")
    _validate_unique_dense(s, "silver")
    _validate_celsius(h, ["TMIN", "TD"])
    _validate_celsius(s, ["TMIN", "TMAX"])

    s_hash = coordinate_hash(s)
    if {"longitude", "latitude"}.issubset(h):
        h_hash = coordinate_hash(h)
        if h_hash != s_hash:
            raise ValueError("Coordinate/ID hashes differ between historical and silver sources")
    elif set(h["ID"].unique()) != set(s["ID"].unique()):
        raise ValueError("ID sets differ between historical and silver sources")

    start, end = pd.Timestamp(parity_start), pd.Timestamp(parity_end)
    h_overlap = h.loc[h["date"].between(start, end), ["ID", "date", "TMIN"]]
    s_overlap = s.loc[s["date"].between(start, end), ["ID", "date", "TMIN"]]
    expected_rows = h["ID"].nunique() * (int((end - start).days) + 1)
    if len(h_overlap) != expected_rows or len(s_overlap) != expected_rows:
        raise ValueError(
            f"Missing dates/cells in TMIN parity interval: expected {expected_rows}, "
            f"historical={len(h_overlap)}, silver={len(s_overlap)}"
        )
    merged = h_overlap.merge(s_overlap, on=["ID", "date"], suffixes=("_hist", "_silver"), how="outer", indicator=True)
    if not (merged["_merge"] == "both").all():
        counts = merged["_merge"].value_counts().to_dict()
        raise ValueError(f"Calendar/ID mismatch in TMIN overlap: {counts}")
    diffs = (merged["TMIN_hist"] - merged["TMIN_silver"]).abs()
    max_diff = float(diffs.max()) if len(diffs) else 0.0
    if not np.isfinite(max_diff) or max_diff > tolerance:
        raise ValueError(f"TMIN parity failed: max difference {max_diff:.8g} C exceeds {tolerance:g} C")
    return AuditResult(s_hash, int(h["ID"].nunique()), len(merged), max_diff)


def canonical_table(historical: pd.DataFrame, silver: pd.DataFrame) -> pd.DataFrame:
    """Join observed TD through 2016 to silver TMIN/TMAX through 2020."""
    historical = canonicalize_columns(historical)
    silver = canonicalize_columns(silver)
    audit_sources(historical, silver)
    hist_cols = [c for c in ["ID", "date", "TD"] if c in historical]
    silver_cols = [
        c for c in ["ID", "date", "department", "TMIN", "TMAX", *STATIC_FEATURES, "region"] if c in silver
    ]
    out = silver[silver_cols].merge(historical[hist_cols], on=["ID", "date"], how="left", validate="one_to_one")
    return out.sort_values(["ID", "date"]).reset_index(drop=True)


def select_spatial_panel(
    cells: pd.DataFrame,
    n_per_department: int,
    *,
    seed: int = 0,
    departments: Sequence[str] | None = None,
) -> pd.DataFrame:
    """Select a deterministic panel stratified by lon/lat grid and DEM quintile."""
    cells = canonicalize_columns(cells)
    _require_columns(cells, ["ID", "department", "longitude", "latitude", "DEM"])
    base = cells[["ID", "department", "longitude", "latitude", "DEM"]].drop_duplicates("ID")
    wanted = list(departments) if departments is not None else sorted(base["department"].unique())
    selected = []
    rng = np.random.default_rng(seed)
    for department in wanted:
        group = base[base["department"] == department].copy()
        if len(group) < n_per_department:
            raise ValueError(f"{department} has {len(group)} cells; {n_per_department} requested")
        group["_lon"] = _safe_quantile_bins(group["longitude"], 4)
        group["_lat"] = _safe_quantile_bins(group["latitude"], 4)
        group["_dem"] = _safe_quantile_bins(group["DEM"], 5)
        group["_key"] = group["_lon"].astype(str) + ":" + group["_lat"].astype(str) + ":" + group["_dem"].astype(str)
        # Random keys are seeded, then a round-robin across strata prevents a
        # large lowland stratum from consuming the panel.
        group["_random"] = rng.random(len(group))
        strata = [g.sort_values(["_random", "ID"]) for _, g in group.groupby("_key", sort=True)]
        rows = []
        depth = 0
        while len(rows) < n_per_department:
            added = False
            for stratum in strata:
                if depth < len(stratum):
                    rows.append(stratum.iloc[depth])
                    added = True
                    if len(rows) == n_per_department:
                        break
            if not added:
                break
            depth += 1
        selected.append(pd.DataFrame(rows)[base.columns])
    return pd.concat(selected, ignore_index=True).sort_values(["department", "ID"]).reset_index(drop=True)


def saturation_vapor_pressure(temp_c: pd.Series | np.ndarray) -> np.ndarray:
    """Tetens saturation vapor pressure in kPa for temperature in Celsius."""
    values = np.asarray(temp_c, dtype=float)
    return 0.6108 * np.exp(17.27 * values / (values + 237.3))


def fit_daily_climatology(frame: pd.DataFrame, spec: ProtocolSpec, columns: Iterable[str]) -> pd.DataFrame:
    train = frame.loc[spec.train_mask(frame["date"])].copy()
    if train.empty:
        raise ValueError("No rows in the protocol training interval")
    train["doy"] = pd.to_datetime(train["date"]).dt.dayofyear
    columns = list(columns)
    _require_columns(train, ["ID", *columns])
    return train.groupby(["ID", "doy"], as_index=False)[columns].mean().rename(
        columns={column: f"{column}_clim" for column in columns}
    )


def build_exogenous_features(frame: pd.DataFrame, spec: ProtocolSpec) -> pd.DataFrame:
    """Build features using only exogenous variables available on each date."""
    required = ["ID", "date", "department", "TMIN", "TMAX"]
    _require_columns(frame, required)
    out = frame.copy()
    out["date"] = pd.to_datetime(out["date"])
    out = out.sort_values(["ID", "date"]).reset_index(drop=True)
    _validate_unique_dense(out, "canonical")
    clim = fit_daily_climatology(out, spec, ["TMIN", "TMAX"])
    out["doy"] = out["date"].dt.dayofyear
    out = out.merge(clim, on=["ID", "doy"], how="left", validate="many_to_one")
    if out[["TMIN_clim", "TMAX_clim"]].isna().any().any():
        raise ValueError("Training climatology does not cover every ID/day-of-year")
    out["TMIN_anom"] = out["TMIN"] - out["TMIN_clim"]
    out["TMAX_anom"] = out["TMAX"] - out["TMAX_clim"]
    out["TEMP_mean"] = (out["TMIN"] + out["TMAX"]) / 2.0
    out["DTR"] = out["TMAX"] - out["TMIN"]
    out["es_TMIN"] = saturation_vapor_pressure(out["TMIN"])
    out["es_TMAX"] = saturation_vapor_pressure(out["TMAX"])
    out["es_range"] = out["es_TMAX"] - out["es_TMIN"]
    theta = 2.0 * np.pi * out["doy"] / 366.0
    for harmonic in (1, 2):
        out[f"sin_doy_{harmonic}"] = np.sin(harmonic * theta)
        out[f"cos_doy_{harmonic}"] = np.cos(harmonic * theta)

    grouped = out.groupby("ID", sort=False)
    for source in ("TMIN", "TMAX", "DTR"):
        out[f"{source}_lag1"] = grouped[source].shift(1)
        for window in ROLLING_WINDOWS:
            roll = grouped[source].rolling(window, min_periods=window)
            out[f"{source}_mean_{window}"] = roll.mean().reset_index(level=0, drop=True)
            out[f"{source}_std_{window}"] = roll.std(ddof=0).reset_index(level=0, drop=True)
            out[f"{source}_slope_{window}"] = grouped[source].transform(
                lambda values, w=window: values.rolling(w, min_periods=w).apply(_slope, raw=True)
            )
    return out


def add_td_targets(frame: pd.DataFrame, spec: ProtocolSpec) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Add train-only TD climatology and return (train rows, hidden rows)."""
    _require_columns(frame, ["TD"])
    clim = fit_daily_climatology(frame, spec, ["TD"])
    out = frame.copy()
    if "doy" not in out:
        out["doy"] = pd.to_datetime(out["date"]).dt.dayofyear
    out = out.merge(clim, on=["ID", "doy"], how="left", validate="many_to_one")
    out["TD_anom"] = out["TD"] - out["TD_clim"]
    return out.loc[spec.train_mask(out["date"])].copy(), out.loc[spec.hidden_mask(out["date"])].copy()


def _slope(values: np.ndarray) -> float:
    x = np.arange(len(values), dtype=float)
    centered = x - x.mean()
    return float(np.dot(centered, values - values.mean()) / np.dot(centered, centered))


def _safe_quantile_bins(values: pd.Series, q: int) -> pd.Series:
    ranked = values.rank(method="first")
    return pd.qcut(ranked, q=min(q, len(values)), labels=False, duplicates="drop")


def _validate_unique_dense(frame: pd.DataFrame, name: str) -> None:
    if frame.duplicated(["ID", "date"]).any():
        raise ValueError(f"{name} has duplicate (ID, date) rows")
    ordered = frame.sort_values(["ID", "date"])
    gaps = ordered.groupby("ID")["date"].diff().dropna()
    if not gaps.empty and not (gaps == pd.Timedelta(days=1)).all():
        raise ValueError(f"{name} has missing dates within at least one ID")


def _validate_celsius(frame: pd.DataFrame, columns: Iterable[str]) -> None:
    for column in columns:
        if column not in frame:
            continue
        values = frame[column].dropna().to_numpy(dtype=float)
        if values.size and (not np.isfinite(values).all() or values.min() < -100 or values.max() > 80):
            raise ValueError(f"{column} is outside broad Celsius limits; check units")


def _require_columns(frame: pd.DataFrame, columns: Iterable[str]) -> None:
    missing = sorted(set(columns) - set(frame.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def canonicalize_columns(frame: pd.DataFrame) -> pd.DataFrame:
    """Accept the repository's X/Y aliases while exposing canonical names."""
    rename = {}
    if "date" not in frame and "FECHA" in frame:
        rename["FECHA"] = "date"
    if "longitude" not in frame and "X" in frame:
        rename["X"] = "longitude"
    if "latitude" not in frame and "Y" in frame:
        rename["Y"] = "latitude"
    if "department" not in frame and "departamento" in frame:
        rename["departamento"] = "department"
    return frame.rename(columns=rename)
