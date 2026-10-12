"""Unit tests for experiments.tcn.dataset.TdewWindowDataset.

Builds a small synthetic model_features_norm + sequence_index/L=31 fixture
on disk (same train/validation split-boundary pattern as
tests/test_baseline_features.py: a 61-day train run 2012-11-01..2012-12-31
followed by a 10-day validation run 2013-01-01..2013-01-10, calendar-
contiguous but a different split), deriving sequence_index with
pipeline.sequences.find_runs/eligibility_for_length exactly as the real
pipeline does (reused, not reimplemented), and checks:
  - the emitted window never reaches date t+1 or later (leakage_constraint),
  - label/td_clim_target are read from exactly date t+1,
  - no window crosses the train/validation boundary,
  - the emitted per-sample weight matches the configured site weight,
  - (multi-site fixture) samples from different sites are round-robin
    interleaved, not grouped -- the fix for the site-homogeneous-batch issue
    described in experiments/tcn/dataset.py's module docstring.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from experiments.tcn.dataset import DYNAMIC_COLS, STATIC_COLS, TARGET_COND_COLS, TdewWindowDataset
from pipeline.sequences import eligibility_for_length, find_runs

CONTEXT_LENGTH = 31
LIMA_ID = 101


def _make_features_df() -> pd.DataFrame:
    dates = pd.date_range("2012-11-01", "2013-01-10", freq="D")
    n = len(dates)
    return pd.DataFrame(
        {
            "ID": LIMA_ID,
            "date": dates,
            "split": ["train" if d.year == 2012 else "validation" for d in dates],
            "TMIN_anom_norm": [float(i) * 2.0 for i in range(n)],
            "TMAX_anom_norm": [float(i) * 3.0 for i in range(n)],
            "TD_anom_norm": [float(i) for i in range(n)],  # index-valued, easy to decode in assertions
            "sin_doy": [0.1 * i for i in range(n)],
            "cos_doy": [0.2 * i for i in range(n)],
            "DEM_norm": [1.0] * n,
            "TDI_norm": [0.5] * n,
            "X_norm": [-0.3] * n,
            "Y_norm": [-0.1] * n,
            "LST_DAY_norm": [0.8] * n,
            "LST_NIGHT_norm": [0.2] * n,
            "TD_clim": [20.0] * n,
        }
    )


@pytest.fixture
def gold_and_silver_dirs(tmp_path: Path) -> tuple[Path, Path]:
    gold_dir = tmp_path / "gold"
    silver_dir = tmp_path / "silver"

    df = _make_features_df()
    feat_dir = gold_dir / "model_features_norm" / "id_bucket=0"
    feat_dir.mkdir(parents=True)
    df.sort_values(["ID", "date"]).to_parquet(feat_dir / "part.parquet", index=False)

    runs = find_runs(df.sort_values(["ID", "date"])[["ID", "date", "split"]])
    seq_index = eligibility_for_length(runs, CONTEXT_LENGTH)
    seq_dir = gold_dir / "sequence_index" / f"L={CONTEXT_LENGTH}" / "id_bucket=0"
    seq_dir.mkdir(parents=True)
    seq_index.to_parquet(seq_dir / "part.parquet", index=False)

    grid_ids_dir = silver_dir / "department_grid_ids"
    grid_ids_dir.mkdir(parents=True)
    pd.DataFrame({"ID": [LIMA_ID]}).to_csv(grid_ids_dir / "lima.csv", index=False)

    return gold_dir, silver_dir


def _collect(dataset: TdewWindowDataset) -> list[dict]:
    return list(iter(dataset))


def test_window_never_reaches_target_date_or_later(gold_and_silver_dirs):
    gold_dir, silver_dir = gold_and_silver_dirs
    dataset = TdewWindowDataset(
        gold_dir,
        silver_dir,
        context_length=CONTEXT_LENGTH,
        split="train",
        site_weights={"lima": 1.0},
        sites=("lima",),
        shuffle_buffer_size=0,
    )
    samples = _collect(dataset)
    assert len(samples) > 0

    td_anom_norm_idx = DYNAMIC_COLS.index("TD_anom_norm")
    for sample in samples:
        window = sample["dynamic"][:, td_anom_norm_idx]  # index-valued: window[k] == row_index of that day
        label = sample["label"]
        # label is TD_anom_norm(t+1) = row_index(t+1); window's last entry is
        # TD_anom_norm(t) = row_index(t) = row_index(t+1) - 1. If the window
        # ever reached t+1 or later, this last value would be >= label.
        assert window[-1] == pytest.approx(label - 1.0)
        # Every value in the window must be strictly less than the label's
        # row index (i.e. strictly before t+1) -- the leakage_constraint.
        assert (window < label).all()
        # And the window must be monotonically increasing by exactly 1 per
        # day (dense daily coverage, no skipped/future day sneaked in).
        assert (window[1:] - window[:-1] == 1.0).all()


def test_label_and_clim_come_from_target_date(gold_and_silver_dirs):
    gold_dir, silver_dir = gold_and_silver_dirs
    dataset = TdewWindowDataset(
        gold_dir,
        silver_dir,
        context_length=CONTEXT_LENGTH,
        split="train",
        site_weights={"lima": 1.0},
        sites=("lima",),
        shuffle_buffer_size=0,
    )
    df = _make_features_df().set_index("date")
    for sample in _collect(dataset):
        target_date = pd.Timestamp(sample["date_ordinal"], unit="D")
        row = df.loc[target_date]
        assert sample["label"] == pytest.approx(row["TD_anom_norm"])
        assert sample["td_clim_target"] == pytest.approx(row["TD_clim"])
        target_cond_idx = TARGET_COND_COLS.index("sin_doy")
        assert sample["target_cond"][target_cond_idx] == pytest.approx(row["sin_doy"])


def test_no_window_crosses_train_validation_boundary(gold_and_silver_dirs):
    gold_dir, silver_dir = gold_and_silver_dirs
    for split in ("train", "validation"):
        dataset = TdewWindowDataset(
            gold_dir,
            silver_dir,
            context_length=CONTEXT_LENGTH,
            split=split,
            site_weights={"lima": 1.0},
            sites=("lima",),
            shuffle_buffer_size=0,
        )
        samples = _collect(dataset)
        for sample in samples:
            target_date = pd.Timestamp(sample["date_ordinal"], unit="D")
            if split == "train":
                assert target_date.year == 2012
            else:
                assert target_date.year == 2013
    # The 10-day validation run is shorter than CONTEXT_LENGTH=31, so it can
    # never have an eligible target (matches test_baseline_features.py's
    # equivalent assertion for the L=31 baseline dataset).
    val_dataset = TdewWindowDataset(
        gold_dir,
        silver_dir,
        context_length=CONTEXT_LENGTH,
        split="validation",
        site_weights={"lima": 1.0},
        sites=("lima",),
        shuffle_buffer_size=0,
    )
    assert _collect(val_dataset) == []


def test_sample_weight_matches_configured_site_weight(gold_and_silver_dirs):
    gold_dir, silver_dir = gold_and_silver_dirs
    dataset = TdewWindowDataset(
        gold_dir,
        silver_dir,
        context_length=CONTEXT_LENGTH,
        split="train",
        site_weights={"lima": 0.0041},
        sites=("lima",),
        shuffle_buffer_size=0,
    )
    samples = _collect(dataset)
    assert len(samples) > 0
    for sample in samples:
        assert sample["weight"] == pytest.approx(0.0041)
        assert sample["region"] == 0  # lima -> Costa -> index 0


def test_dynamic_static_target_cond_shapes(gold_and_silver_dirs):
    gold_dir, silver_dir = gold_and_silver_dirs
    dataset = TdewWindowDataset(
        gold_dir,
        silver_dir,
        context_length=CONTEXT_LENGTH,
        split="train",
        site_weights={"lima": 1.0},
        sites=("lima",),
        shuffle_buffer_size=0,
    )
    sample = next(iter(dataset))
    assert sample["dynamic"].shape == (CONTEXT_LENGTH, len(DYNAMIC_COLS))
    assert sample["static"].shape == (len(STATIC_COLS),)
    assert sample["target_cond"].shape == (len(TARGET_COND_COLS),)


CUSCO_ID = 202


def _make_two_site_features_df() -> pd.DataFrame:
    """Two cells, one per site (lima=Costa, cusco=Sierra), same train-only
    date range and length -- enough to check round-robin interleaving
    without the ragged-tail edge case (unequal-length site streams)."""
    dates = pd.date_range("2012-11-01", "2012-12-31", freq="D")
    n = len(dates)

    def _site_block(location_id: int) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "ID": location_id,
                "date": dates,
                "split": "train",
                "TMIN_anom_norm": [0.0] * n,
                "TMAX_anom_norm": [0.0] * n,
                "TD_anom_norm": [float(i) for i in range(n)],
                "sin_doy": [0.0] * n,
                "cos_doy": [0.0] * n,
                "DEM_norm": [0.0] * n,
                "TDI_norm": [0.0] * n,
                "X_norm": [0.0] * n,
                "Y_norm": [0.0] * n,
                "LST_DAY_norm": [0.0] * n,
                "LST_NIGHT_norm": [0.0] * n,
                "TD_clim": [20.0] * n,
            }
        )

    return pd.concat([_site_block(LIMA_ID), _site_block(CUSCO_ID)], ignore_index=True)


@pytest.fixture
def two_site_dirs(tmp_path: Path) -> tuple[Path, Path]:
    gold_dir = tmp_path / "gold2"
    silver_dir = tmp_path / "silver2"

    df = _make_two_site_features_df().sort_values(["ID", "date"])
    feat_dir = gold_dir / "model_features_norm" / "id_bucket=0"
    feat_dir.mkdir(parents=True)
    df.to_parquet(feat_dir / "part.parquet", index=False)

    runs = find_runs(df[["ID", "date", "split"]])
    seq_index = eligibility_for_length(runs, CONTEXT_LENGTH)
    seq_dir = gold_dir / "sequence_index" / f"L={CONTEXT_LENGTH}" / "id_bucket=0"
    seq_dir.mkdir(parents=True)
    seq_index.to_parquet(seq_dir / "part.parquet", index=False)

    grid_ids_dir = silver_dir / "department_grid_ids"
    grid_ids_dir.mkdir(parents=True)
    pd.DataFrame({"ID": [LIMA_ID]}).to_csv(grid_ids_dir / "lima.csv", index=False)
    pd.DataFrame({"ID": [CUSCO_ID]}).to_csv(grid_ids_dir / "cusco.csv", index=False)

    return gold_dir, silver_dir


def test_sites_are_round_robin_interleaved_not_grouped(two_site_dirs):
    gold_dir, silver_dir = two_site_dirs
    dataset = TdewWindowDataset(
        gold_dir,
        silver_dir,
        context_length=CONTEXT_LENGTH,
        split="train",
        site_weights={"lima": 1.0, "cusco": 1.0},
        sites=("lima", "cusco"),
        shuffle_buffer_size=0,  # raw order, straight off the round-robin merge
    )
    ids_in_order = [int(sample["id"]) for sample in _collect(dataset)]
    assert len(ids_in_order) > 4
    assert set(ids_in_order) == {LIMA_ID, CUSCO_ID}

    # Both cells cover the exact same date range/length here, so round-robin
    # must alternate perfectly for the whole stream -- if it were the old
    # flat per-ID scan, this would instead be [LIMA_ID]*N + [CUSCO_ID]*N.
    even_positions = ids_in_order[0::2]
    odd_positions = ids_in_order[1::2]
    assert len(set(even_positions)) == 1
    assert len(set(odd_positions)) == 1
    assert even_positions[0] != odd_positions[0]


def test_single_site_dataset_is_unaffected_by_round_robin(gold_and_silver_dirs):
    # Regression guard: with only one site configured, round-robin over a
    # single generator must reduce to the original flat per-ID order.
    gold_dir, silver_dir = gold_and_silver_dirs
    dataset = TdewWindowDataset(
        gold_dir,
        silver_dir,
        context_length=CONTEXT_LENGTH,
        split="train",
        site_weights={"lima": 1.0},
        sites=("lima",),
        shuffle_buffer_size=0,
    )
    ids_in_order = [int(sample["id"]) for sample in _collect(dataset)]
    assert set(ids_in_order) == {LIMA_ID}
