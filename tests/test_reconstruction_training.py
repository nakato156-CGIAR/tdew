from __future__ import annotations

from collections import Counter

import pandas as pd
import pytest
import torch

import numpy as np

from experiments.reconstruction.tcn_runner import BalancedWindowBatches, TCNPreprocessor, WindowStore
from experiments.reconstruction.training import train_steps


class TinyModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = torch.nn.Linear(1, 1)

    def forward(self, dynamic, static, region, target_cond):
        return self.linear(dynamic[:, -1, :]).squeeze(-1)


def _batches():
    batches = []
    for value in (1.0, 2.0, 3.0):
        batches.append(
            {
                "dynamic": torch.tensor([[[value]], [[value + 0.5]]]),
                "static": torch.zeros(2, 1),
                "region": torch.zeros(2, dtype=torch.long),
                "target_cond": torch.zeros(2, 1),
                "label": torch.tensor([value * 0.5, (value + 0.5) * 0.5]),
                "department": ["Lima", "Cusco"],
            }
        )
    return batches


def _panel_store() -> WindowStore:
    dates = pd.date_range("2000-01-01", periods=60)
    pieces = []
    for location_id, department in enumerate(["Lima", "Lima", "Cusco", "Cusco"], start=1):
        pieces.append(
            pd.DataFrame(
                {
                    "ID": location_id,
                    "date": dates,
                    "department": department,
                    "region": "Costa" if department == "Lima" else "Sierra",
                    "_split": ["train"] * 40 + ["hidden"] * 20,
                    "TMIN": np.linspace(10, 11, 60),
                    "TD_anom": np.linspace(-0.5, 0.5, 60),
                    "DEM": 100.0 * location_id,
                    "sin_doy_1": 0.1,
                }
            )
        )
    frame = pd.concat(pieces, ignore_index=True)
    columns = ("TMIN", "DEM", "sin_doy_1")
    processor = TCNPreprocessor(
        dynamic_columns=("TMIN",),
        static_columns=("DEM",),
        target_columns=("sin_doy_1",),
        center={column: 0.0 for column in columns},
        scale={column: 1.0 for column in columns},
        fill={column: 0.0 for column in columns},
        td_center=0.0,
        td_scale=1.0,
    )
    return WindowStore(frame, processor, split="train", context_length=3, mode="direct")


def test_balanced_batches_keep_the_department_quota_and_distinct_cells():
    store = _panel_store()
    batches = list(BalancedWindowBatches(store, batch_size=4, n_batches=3, seed=0))
    assert len(batches) == 3
    for batch in batches:
        assert Counter(batch["department"]) == {"Lima": 2, "Cusco": 2}
        # DEM identifies the cell, so two equal values would mean a repeated cell.
        assert len(set(batch["static"].flatten().tolist())) == 4
    repeated = list(BalancedWindowBatches(store, batch_size=4, n_batches=3, seed=0))
    for left, right in zip(batches, repeated):
        torch.testing.assert_close(left["dynamic"], right["dynamic"], rtol=0, atol=0)


def test_step_checkpoint_resume_matches_uninterrupted(tmp_path):
    torch.manual_seed(4)
    full = TinyModel()
    full_optimizer = torch.optim.SGD(full.parameters(), lr=0.01)
    train_steps(
        full, _batches(), _batches(), optimizer=full_optimizer,
        checkpoint_dir=tmp_path / "full", config={}, mode="direct", device=torch.device("cpu"),
        max_steps=4, eval_every=1, patience=10, min_delta=0.0, resume="none",
    )

    torch.manual_seed(4)
    resumed = TinyModel()
    resumed_optimizer = torch.optim.SGD(resumed.parameters(), lr=0.01)
    train_steps(
        resumed, _batches(), _batches(), optimizer=resumed_optimizer,
        checkpoint_dir=tmp_path / "resume", config={}, mode="direct", device=torch.device("cpu"),
        max_steps=2, eval_every=1, patience=10, min_delta=0.0, resume="none",
    )
    train_steps(
        resumed, _batches(), _batches(), optimizer=resumed_optimizer,
        checkpoint_dir=tmp_path / "resume", config={}, mode="direct", device=torch.device("cpu"),
        max_steps=4, eval_every=1, patience=10, min_delta=0.0, resume="auto",
    )
    for left, right in zip(full.parameters(), resumed.parameters()):
        torch.testing.assert_close(left, right, rtol=0, atol=0)


def test_resume_refuses_a_checkpoint_that_already_passed_max_steps(tmp_path):
    torch.manual_seed(4)
    model = TinyModel()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
    train_steps(
        model, _batches(), _batches(), optimizer=optimizer,
        checkpoint_dir=tmp_path / "run", config={}, mode="direct", device=torch.device("cpu"),
        max_steps=4, eval_every=1, patience=10, min_delta=0.0, resume="none",
    )
    with pytest.raises(ValueError, match="already at step 4"):
        train_steps(
            model, _batches(), _batches(), optimizer=optimizer,
            checkpoint_dir=tmp_path / "run", config={}, mode="direct", device=torch.device("cpu"),
            max_steps=2, eval_every=1, patience=10, min_delta=0.0, resume="auto",
        )
