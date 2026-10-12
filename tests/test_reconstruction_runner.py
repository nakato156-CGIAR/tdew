"""End-to-end checks of the TCN runner on a synthetic canonical table."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
import torch

from experiments.tcn import checkpoint as checkpoint_io
from experiments.reconstruction.tcn_runner import run_tcn

DEPARTMENTS = (("Lima", "Costa"), ("Cusco", "Sierra"))


def _canonical(end: str) -> pd.DataFrame:
    dates = pd.date_range("1981-01-01", end)
    seasonal = np.sin(2 * np.pi * dates.dayofyear.to_numpy() / 366.0)
    pieces = []
    for index, (department, region) in enumerate(DEPARTMENTS, start=1):
        noise = np.cos(2 * np.pi * np.arange(len(dates)) / (37.0 * index))
        pieces.append(
            pd.DataFrame(
                {
                    "ID": index,
                    "date": dates,
                    "department": department,
                    "region": region,
                    "longitude": -77.0 + index,
                    "latitude": -12.0 + index,
                    "DEM": 100.0 * index,
                    "TDI": 0.2 * index,
                    "LST_DAY": 25.0 + index,
                    "LST_NIGHT": 15.0 + index,
                    "TMIN": 10.0 + seasonal + index + 0.1 * noise,
                    "TMAX": 20.0 + seasonal + index + 0.2 * noise,
                    "TD": 8.0 + seasonal + index + 0.3 * noise,
                }
            )
        )
    return pd.concat(pieces, ignore_index=True)


def _run(canonical, tmp_path, *, protocol, name, checkpoint=None, batch_size=256, learning_rate=3e-4):
    return run_tcn(
        canonical,
        protocol=protocol,
        mode="direct",
        feature_set="tmin",
        seed=0,
        output_path=tmp_path / name / "predictions.parquet",
        checkpoint=checkpoint,
        context_length=3,
        max_steps=2,
        eval_every=2,
        batch_size=batch_size,
        num_workers=0,
        learning_rate=learning_rate,
        objective="mse",
        unlock_ll4=False,
        device="cpu",
    )


def test_direct_run_covers_the_hidden_block_without_reading_its_td(tmp_path):
    canonical = _canonical("2008-12-31")
    predictions = _run(canonical, tmp_path, protocol="dev_a", name="dev_a")

    assert len(predictions) == 2 * 1461
    assert predictions["date"].min() == pd.Timestamp("2005-01-01")
    assert predictions["date"].max() == pd.Timestamp("2008-12-31")
    assert set(predictions["year_horizon"]) == {1, 2, 3, 4}
    assert np.isfinite(predictions["TD_pred"].to_numpy()).all()

    blinded = canonical.copy()
    hidden = blinded["date"] >= pd.Timestamp("2005-01-01")
    blinded.loc[hidden, "TD"] = 9999.0
    repeated = _run(blinded, tmp_path, protocol="dev_a", name="dev_a_blinded")
    np.testing.assert_allclose(
        repeated["TD_pred"].to_numpy(), predictions["TD_pred"].to_numpy(), rtol=0, atol=0
    )


def test_refit_from_a_frozen_checkpoint_reuses_its_batch_size_and_learning_rate(tmp_path):
    canonical = _canonical("2012-12-31")
    selected = _run(canonical, tmp_path, protocol="dev_a", name="dev_a", batch_size=256, learning_rate=7e-4)
    frozen = tmp_path / "dev_a" / "checkpoints" / "predictions" / "best.pt"
    assert frozen.is_file()

    _run(
        canonical, tmp_path, protocol="dev_b", name="dev_b",
        checkpoint=frozen, batch_size=1024, learning_rate=1e-2,
    )
    refit = checkpoint_io.load_checkpoint(tmp_path / "dev_b" / "checkpoints" / "predictions_refit" / "final.pt")
    assert refit["config"]["batch_size"] == 256
    assert refit["config"]["learning_rate"] == pytest.approx(7e-4)
    assert refit["config"]["fixed_refit"] is True
    assert refit["config"]["selected_from_checkpoint"] == str(frozen)
    assert selected.attrs["mode"] == "direct"
    assert selected.attrs["trained"] is True


def test_same_protocol_frozen_checkpoint_is_inference_only_and_not_trained(tmp_path):
    """Reusing a checkpoint under the SAME protocol it was frozen for skips
    train_steps entirely (tcn_runner.run_tcn's inference_only branch) -- its
    predictions.attrs must say trained=False, not the ridge/histgb default."""
    canonical = _canonical("2008-12-31")
    _run(canonical, tmp_path, protocol="dev_a", name="dev_a")
    frozen = tmp_path / "dev_a" / "checkpoints" / "predictions" / "best.pt"
    assert frozen.is_file()

    reused = _run(canonical, tmp_path, protocol="dev_a", name="dev_a_again", checkpoint=frozen)
    assert reused.attrs["trained"] is False


def test_sealed_holdout_stays_closed_without_an_explicit_unlock(tmp_path):
    canonical = _canonical("2016-12-31").head(10)
    with pytest.raises(PermissionError, match="sealed"):
        _run(canonical, tmp_path, protocol="ll4", name="ll4")


def test_feature_cache_is_written_once_and_reused(tmp_path):
    from experiments.reconstruction.protocol import protocol_spec
    from experiments.reconstruction.tcn_runner import prepare_frame

    canonical = _canonical("2008-12-31")
    spec = protocol_spec("dev_a")
    cache = tmp_path / "features" / "dev_a.parquet"

    combined, train, hidden = prepare_frame(canonical, spec, cache_path=cache)
    assert cache.is_file()
    assert len(train) + len(hidden) == len(combined)
    assert set(hidden["_split"]) == {"hidden"}
    assert hidden["date"].min() == pd.Timestamp("2005-01-01")

    # A different canonical must not be re-featured once the cache exists.
    shifted = canonical.assign(TMIN=canonical["TMIN"] + 5.0)
    cached, _, _ = prepare_frame(shifted, spec, cache_path=cache)
    pd.testing.assert_frame_equal(cached, combined)
    assert not list(cache.parent.glob("*.partial"))
