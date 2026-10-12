from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from experiments.reconstruction.data import (
    audit_sources,
    build_exogenous_features,
    select_spatial_panel,
)
from experiments.reconstruction.protocol import Protocol, protocol_spec, require_protocol_access


def _daily_frame(start: str, end: str, ids=(1, 2)) -> pd.DataFrame:
    rows = []
    for location_id in ids:
        for date in pd.date_range(start, end):
            seasonal = np.sin(2 * np.pi * date.dayofyear / 366)
            rows.append(
                {
                    "ID": location_id,
                    "date": date,
                    "department": "Lima" if location_id == 1 else "Cusco",
                    "longitude": -77.0 + location_id,
                    "latitude": -12.0 + location_id,
                    "DEM": 100.0 * location_id,
                    "TDI": 0.2,
                    "TMIN": 10.0 + seasonal + location_id,
                    "TMAX": 20.0 + seasonal + location_id,
                    "TD": 8.0 + seasonal + location_id,
                }
            )
    return pd.DataFrame(rows)


def test_protocol_boundaries_and_ll4_guard():
    spec = protocol_spec(Protocol.DEV_A)
    assert spec.train_end == pd.Timestamp("2004-12-31")
    assert spec.hidden_start == pd.Timestamp("2005-01-01")
    assert spec.horizon_days == 1461
    with pytest.raises(PermissionError, match="sealed"):
        require_protocol_access("ll4")
    assert require_protocol_access("ll4", unlock_ll4=True).hidden_end.year == 2016


def test_audit_detects_tmin_parity_failure():
    historical = _daily_frame("2002-01-01", "2002-01-03")
    silver = historical.drop(columns=["TD"]).copy()
    result = audit_sources(historical, silver, parity_end="2002-01-03")
    assert result.max_tmin_difference == 0
    silver.loc[0, "TMIN"] += 0.001
    with pytest.raises(ValueError, match="parity failed"):
        audit_sources(historical, silver, parity_end="2002-01-03")


def test_exogenous_features_ignore_hidden_td_and_do_not_cross_ids():
    frame = _daily_frame("2004-01-01", "2005-02-15")
    spec = protocol_spec("dev_a")
    first = build_exogenous_features(frame, spec)
    changed = frame.copy()
    changed.loc[changed["date"].dt.year == 2005, "TD"] = 9999.0
    second = build_exogenous_features(changed, spec)
    exogenous = [column for column in first if column != "TD"]
    pd.testing.assert_frame_equal(first[exogenous], second[exogenous])
    first_rows = first.groupby("ID", sort=False).head(1)
    assert first_rows["TMIN_lag1"].isna().all()


def test_spatial_panel_is_balanced_and_deterministic():
    cells = pd.DataFrame(
        {
            "ID": np.arange(80),
            "department": np.repeat(["Lima", "Cusco"], 40),
            "longitude": np.linspace(-80, -70, 80),
            "latitude": np.linspace(-18, -2, 80),
            "DEM": np.arange(80) * 50,
        }
    )
    a = select_spatial_panel(cells, 12, seed=7)
    b = select_spatial_panel(cells, 12, seed=7)
    pd.testing.assert_frame_equal(a, b)
    assert a.groupby("department").size().to_dict() == {"Cusco": 12, "Lima": 12}
