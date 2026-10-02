"""effect_sizes registra notes y manifest_ref explicitos (la raiz fusionada no es
la limpia por nombre, asi que no se puede inferir)."""
from __future__ import annotations

import numpy as np
import pandas as pd

from HPC_code_tunning import effect_sizes
from tdew_estimation import provenance as prov

ADDENDUM = "docs/protocol/timesfm_manifest_addendum_2026-10-02.yaml"


def test_main_records_explicit_notes_and_manifest_ref(tmp_path, monkeypatch):
    rng = np.random.default_rng(0)
    dates = pd.date_range("2020-01-01", periods=20)
    rows = []
    for i in range(12):
        for d in dates:
            obs = rng.normal()
            rows.append((i, i % 3, d, obs, obs + rng.normal(0, .3), obs + rng.normal(0, 1),
                         obs + rng.normal(0, 2), obs + rng.normal(0, 2), obs + rng.normal(0, .2)))
    frame = pd.DataFrame(rows, columns=["ID", "zone_id", "FECHA", "TD_obs", "pred_tuned",
                                        "pred_clim", "pred_tmin", "pred_ols", "pred_timesfm"])
    (tmp_path / "ll4").mkdir()
    frame.to_parquet(tmp_path / "ll4" / "predictions.parquet", index=False)
    records = []
    monkeypatch.setattr(prov, "record_metric_provenance", records.append)
    effect_sizes.main([
        "--backtest-root", str(tmp_path), "--splits", "ll4", "--focal", "timesfm",
        "--lead-time-methods", "timesfm,tuned", "--timesfm-variant", "tmin_anom_full",
        "--n-boot", "20", "--n-perm", "20", "--seed", "0",
        "--manifest-ref", ADDENDUM, "--notes", "deriva de backtest_clean",
    ])
    assert records
    for rec in records:
        assert rec.manifest_ref == ADDENDUM
        assert "deriva de backtest_clean" in rec.notes
        assert "cells=12" in rec.notes
        assert any(f.endswith("effect_sizes_all.csv") for f in rec.output_files)
        assert "n_boot=20" in rec.notes and "n_perm=20" in rec.notes and "seed=0" in rec.notes
