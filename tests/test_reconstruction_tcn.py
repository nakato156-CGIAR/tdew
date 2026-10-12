from __future__ import annotations

import torch
import numpy as np
import pandas as pd

from experiments.reconstruction.tcn import (
    ReconstructionTCNConfig,
    allowed_context_lengths,
    build_tcn,
    closed_rollout,
    rollout_loss,
)
from experiments.reconstruction.tcn_runner import (
    TARGET_COLUMNS,
    TCNPreprocessor,
    WindowStore,
)


def test_closed_rollout_backpropagates_through_feedback():
    torch.manual_seed(0)
    config = ReconstructionTCNConfig(3, 4, 2, autoregressive=True, d_model=8, n_tcn_blocks=1, n_attention_heads=2, dropout=0.0)
    model = build_tcn(config)
    dynamic = torch.randn(2, 4, 3, 3)
    static = torch.randn(2, 4)
    region = torch.tensor([0, 1])
    cond = torch.randn(2, 4, 2)
    history = torch.randn(2, 30)
    pred = closed_rollout(model, dynamic, static, region, cond, history)
    assert pred.shape == (2, 4)
    loss = rollout_loss(pred, torch.zeros_like(pred))
    loss.backward()
    assert any(parameter.grad is not None for parameter in model.parameters())


def test_long_context_gate_requires_both_fold_wins():
    assert allowed_context_lengths({7: (1.0, 1.0), 14: (0.9, 0.8)}) == (3, 7, 14, 31, 60)
    assert allowed_context_lengths({7: (1.0, 1.0), 14: (0.9, 1.1)}) == (3, 7, 14)


def _synthetic_frame() -> pd.DataFrame:
    dates = pd.date_range("2000-01-01", periods=100)
    return pd.DataFrame(
        {
            "ID": 1,
            "date": dates,
            "department": "Lima",
            "region": "Costa",
            "_split": ["train"] * 60 + ["hidden"] * 40,
            "TMIN": np.linspace(10, 11, 100),
            "TMIN_anom": np.linspace(-1, 1, 100),
            "TD_anom": np.linspace(-0.5, 0.5, 100),
            "DEM": 100.0,
            "TDI": 0.2,
            "longitude": -77.0,
            "latitude": -12.0,
            "sin_doy_1": 0.1,
            "cos_doy_1": 0.2,
            "LST_DAY": 25.0,
            "LST_NIGHT": 15.0,
        }
    )


def _identity_preprocessor() -> TCNPreprocessor:
    columns = ("TMIN", "TMIN_anom", "sin_doy_1", "cos_doy_1", "DEM", "TDI", "longitude", "latitude", *TARGET_COLUMNS)
    return TCNPreprocessor(
        dynamic_columns=("TMIN", "TMIN_anom", "sin_doy_1", "cos_doy_1"),
        static_columns=("DEM", "TDI", "longitude", "latitude"),
        target_columns=TARGET_COLUMNS,
        center={column: 0.0 for column in columns},
        scale={column: 1.0 for column in columns},
        fill={column: 0.0 for column in columns},
        td_center=0.0,
        td_scale=1.0,
    )


def test_window_store_builds_direct_and_closed_samples():
    frame = _synthetic_frame()
    processor = _identity_preprocessor()
    direct = WindowStore(frame, processor, split="hidden", context_length=7, mode="direct")
    closed = WindowStore(frame, processor, split="hidden", context_length=7, mode="recursive", rollout_days=31)
    assert direct.sample(1, 60)["dynamic"].shape == (7, 4)
    assert closed.sample(1, 60)["dynamic_windows"].shape == (31, 7, 4)
    assert closed.sample(1, 60)["initial_td_history"].shape == (30,)


def test_recursive_validation_window_can_span_the_complete_hidden_block():
    store = WindowStore(
        _synthetic_frame(), _identity_preprocessor(), split="hidden", context_length=7,
        mode="recursive", rollout_days=40,
    )
    sample = store.sample(1, 60)
    assert sample["dynamic_windows"].shape == (40, 7, 4)
    assert sample["label"].shape == (40,)
    assert list(store.cells[1]["positions"]) == [60]
