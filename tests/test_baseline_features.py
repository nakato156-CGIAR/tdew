"""Unit tests for pipeline.baseline_features.

Builds a small synthetic model_features_norm-like frame spanning a real
train/validation split boundary (2012-12-31 -> 2013-01-01), derives its
sequence_index/L=31 exactly the way pipeline.sequences does (reused, not
reimplemented), and checks:
  - lag/target columns are correct per-day shifts (no off-by-one),
  - no feature column ever reaches past date t (the leakage_constraint),
  - eligibility correctly excludes the last day of a run/split (its target
    would fall in the next split) and the first 30 days of a run (not
    enough lookback for TD_anom_lag30).
"""

from __future__ import annotations

import pandas as pd

from pipeline.baseline_features import SEQUENCE_LENGTH, build_bucket_baseline_features
from pipeline.sequences import eligibility_for_length, find_runs


def _make_features_df() -> pd.DataFrame:
    # ID 1: a 61-day train run (2012-11-01..2012-12-31) followed by a
    # 10-day validation run (2013-01-01..2013-01-10) -- calendar-contiguous
    # but a different split, so pipeline.sequences.find_runs must split it.
    dates = pd.date_range("2012-11-01", "2013-01-10", freq="D")
    n = len(dates)
    df = pd.DataFrame(
        {
            "ID": 1,
            "date": dates,
            "doy": dates.dayofyear,
            "split": ["train" if d.year == 2012 else "validation" for d in dates],
            "TD": [20.0 + i for i in range(n)],
            "TD_clim": [20.0] * n,
            "TD_anom": [float(i) for i in range(n)],
            "TMIN_anom": [float(i) * 2 for i in range(n)],
            "sin_doy": [0.1 * i for i in range(n)],
            "cos_doy": [0.2 * i for i in range(n)],
            "LST_DAY": [25.0] * n,
            "LST_NIGHT": [15.0] * n,
            "DEM": [100.0] * n,
            "TDI": [0.5] * n,
            "X": [-76.0] * n,
            "Y": [-10.0] * n,
        }
    )
    return df


def _seq_index_for(df: pd.DataFrame) -> pd.DataFrame:
    runs = find_runs(df.sort_values(["ID", "date"]))
    return eligibility_for_length(runs, SEQUENCE_LENGTH)


def test_eligibility_respects_run_and_split_boundaries():
    df = _make_features_df()
    seq_index = _seq_index_for(df)
    out = build_bucket_baseline_features(df, seq_index)

    # Train run: 2012-11-01..2012-12-31 (61 days). Eligible target dates are
    # run_start+30 .. run_end-1 = 2012-12-01 .. 2012-12-30, i.e. eligible t
    # (row date) = target_date - 1 day = 2012-11-30 .. 2012-12-29.
    eligible_dates = set(out["date"])
    assert pd.Timestamp("2012-11-29") not in eligible_dates  # only 29 days lookback
    assert pd.Timestamp("2012-11-30") in eligible_dates  # exactly 30 days lookback
    assert pd.Timestamp("2012-12-29") in eligible_dates  # last eligible: target=12-30, same run
    assert pd.Timestamp("2012-12-30") not in eligible_dates  # target=12-31 exceeds last_eligible_target_date
    assert pd.Timestamp("2012-12-31") not in eligible_dates  # target would be 2013-01-01: different split/run
    # Validation run is only 10 days: never long enough for L=31 eligibility.
    assert not any(d.year == 2013 for d in eligible_dates)


def test_lag_and_target_columns_are_correct_shifts():
    df = _make_features_df()
    seq_index = _seq_index_for(df)
    out = build_bucket_baseline_features(df, seq_index)

    row = out[out["date"] == pd.Timestamp("2012-12-01")].iloc[0]
    # date 2012-12-01 is day index 30 (0-indexed from 2012-11-01) in TD_anom=i sequence.
    assert row["TD_anom_lag1"] == 30.0  # TD_anom(t)
    assert row["TD_anom_lag2"] == 29.0  # TD_anom(t-1)
    assert row["TD_anom_lag3"] == 28.0  # TD_anom(t-2)
    assert row["TD_anom_lag7"] == 24.0  # TD_anom(t-6)
    assert row["TD_anom_lag30"] == 1.0  # TD_anom(t-29)
    assert row["TMIN_anom_lag0"] == 60.0  # TMIN_anom(t) = 2*30
    assert row["TMIN_anom_lag1"] == 58.0  # TMIN_anom(t-1) = 2*29
    assert row["TD_anom_target"] == 31.0  # TD_anom(t+1)
    assert row["TD_target"] == 20.0 + 31.0  # TD(t+1)


def test_no_feature_uses_a_future_date():
    """Leakage_constraint check: every value in an eligible row must be
    derivable from date <= t. We verify this indirectly: TD_anom_lag1 (the
    most "recent" backward feature) must never exceed the value the raw
    series has *at or before* t, i.e. it must equal TD_anom(t) exactly, not
    TD_anom(t+1) (which would be off-by-one leakage of the target itself)."""
    df = _make_features_df()
    seq_index = _seq_index_for(df)
    out = build_bucket_baseline_features(df, seq_index)

    raw = df[["date", "TD_anom"]].rename(columns={"TD_anom": "TD_anom_raw_at_t"})
    merged = out.merge(raw, on="date")
    assert (merged["TD_anom_lag1"] == merged["TD_anom_raw_at_t"]).all()
    assert not (merged["TD_anom_lag1"] == merged["TD_anom_target"]).any()
