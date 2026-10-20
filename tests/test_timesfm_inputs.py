"""Armado de entradas para TimesFM: anchos, canales y deshacer la anomalia."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from experiments.timesfm.panel import PanelBatch, split_spec
from experiments.timesfm.run import build_inputs, build_provenance, output_name, to_physical
from experiments.timesfm.variants import VARIANTS, variant


@pytest.fixture
def panel():
    spec = split_spec("ll4", context_start_year=2011)
    context, horizon, cells = spec.context_length, spec.horizon, 3
    ctx_dates = pd.date_range(spec.context_start, spec.context_end, freq="D")
    hold_dates = pd.date_range(spec.holdout_start, spec.holdout_end, freq="D")
    rng = np.random.default_rng(0)
    clim = rng.normal(size=(cells, 367)).astype("float32")
    return PanelBatch(
        spec=spec,
        ids=np.arange(cells, dtype=np.int64),
        td_ctx=rng.normal(size=(cells, context)).astype("float32"),
        tmin_ctx=rng.normal(size=(cells, context)).astype("float32"),
        td_hold=rng.normal(size=(cells, horizon)).astype("float32"),
        tmin_hold=rng.normal(size=(cells, horizon)).astype("float32"),
        td_clim=clim,
        tmin_clim=rng.normal(size=(cells, 367)).astype("float32"),
        ctx_doy=ctx_dates.dayofyear.to_numpy(dtype=np.int16),
        hold_doy=hold_dates.dayofyear.to_numpy(dtype=np.int16),
        ctx_dates=ctx_dates,
        hold_dates=hold_dates,
    )


def test_covariate_width_is_exactly_context_plus_horizon(panel):
    """El ancho de la covariable futura define el horizonte dentro del modelo.

    `timesfm3/torch/model.py:395-396` reescribe el horizonte a partir de ese ancho
    y no valida nada, asi que un arreglo mal dimensionado cambia en silencio
    cuantos dias se predicen.
    """
    expected = panel.td_ctx.shape[1] + panel.td_hold.shape[1]
    for spec in VARIANTS:
        if not spec.covariates or spec.covariates == ("TMIN_anom",):
            continue
        _, covariates = build_inputs(panel, variant(spec.key))
        if covariates is None:
            continue
        for array in covariates:
            assert array.shape[1] == expected, spec.key


def test_variant_without_covariates_sends_none(panel):
    contexts, covariates = build_inputs(panel, variant("uni_td_full"))
    assert covariates is None
    assert len(contexts) == panel.n_cells
    assert contexts[0].shape == (panel.td_ctx.shape[1],)


def test_day_of_year_variant_adds_two_channels(panel):
    _, covariates = build_inputs(panel, variant("tmin_doy_td_full"))
    assert covariates[0].shape[0] == 3  # Tmin + seno + coseno
    sine, cosine = covariates[0][1], covariates[0][2]
    np.testing.assert_allclose(sine**2 + cosine**2, np.ones_like(sine), atol=1e-5)


def test_anomaly_target_is_the_context_minus_climatology(panel):
    contexts, _ = build_inputs(panel, variant("uni_anom_full"))
    expected = panel.td_ctx[0] - panel.td_clim[0, panel.ctx_doy]
    np.testing.assert_allclose(contexts[0], expected, rtol=1e-5)


def test_to_physical_undoes_the_anomaly_and_leaves_td_alone(panel):
    raw = np.zeros((panel.n_cells, panel.td_hold.shape[1]), dtype=np.float32)
    np.testing.assert_allclose(to_physical(raw, panel, variant("uni_td_full")), raw)
    restored = to_physical(raw, panel, variant("uni_anom_full"))
    np.testing.assert_allclose(restored, panel.td_clim[:, panel.hold_doy], rtol=1e-5)


def test_unknown_covariate_is_rejected(panel):
    from dataclasses import replace

    broken = replace(variant("tmin_td_full"), covariates=("LLUVIA",))
    with pytest.raises(ValueError, match="covariable desconocida"):
        build_inputs(panel, broken)


def test_unknown_target_is_rejected(panel):
    from dataclasses import replace

    broken = replace(variant("tmin_td_full"), target="TMAX")
    with pytest.raises(ValueError, match="objetivo desconocido"):
        build_inputs(panel, broken)


def test_every_variant_key_is_unique():
    keys = [spec.key for spec in VARIANTS]
    assert len(keys) == len(set(keys)) == 10


def test_tmin_anom_med_is_tmin_anom_full_with_short_context():
    """Control de regimen MODIS (tdew-03g): misma entrada que la titular, contexto desde 2002."""
    full, med = variant("tmin_anom_full"), variant("tmin_anom_med")
    assert (med.target, med.covariates) == (full.target, full.covariates)
    assert med.context_start_year == 2002 and full.context_start_year == 1981
    assert (med.symmetric_averaging, med.znorm, med.autoregressive) == (False, False, False)


def test_to_physical_also_converts_the_quantile_cube(panel):
    """Los cuantiles deben recibir el mismo desplazamiento que la predicción puntual.

    Sin esto, una variante sobre anomalía escribe el punto en grados y los nueve
    deciles en anomalía, y toda la evaluación probabilística de esa variante
    compara magnitudes distintas.
    """
    horizon = panel.td_hold.shape[1]
    cube = np.zeros((panel.n_cells, horizon, 9), dtype=np.float32)
    same = to_physical(cube, panel, variant("uni_td_full"))
    np.testing.assert_allclose(same, cube)

    shifted = to_physical(cube, panel, variant("uni_anom_full"))
    assert shifted.shape == cube.shape
    expected = panel.td_clim[:, panel.hold_doy]
    for level in range(9):
        np.testing.assert_allclose(shifted[:, :, level], expected, rtol=1e-5)

    point = to_physical(np.zeros((panel.n_cells, horizon), dtype=np.float32),
                        panel, variant("uni_anom_full"))
    np.testing.assert_allclose(shifted[:, :, 4], point, rtol=1e-6)


def test_shards_are_disjoint_and_cover_every_cell():
    """El reparto entre procesos no puede perder ni duplicar celdas.

    Se reparte por resto del identificador y no por bloques contiguos: los IDs son
    densos en orden row-major, así que un corte contiguo daría a cada proceso una
    franja geográfica distinta y sus tiempos serían dispares.
    """
    cells = sorted({7, 15, 8192 * 3 + 7, 1234, 99999, 2, 8193})
    for total in (2, 3, 5):
        pieces = [[c for c in cells if c % total == index] for index in range(total)]
        union: list[int] = []
        for piece in pieces:
            union.extend(piece)
        assert sorted(union) == cells
        assert len(union) == len(set(union))


def test_target_type_matches_target_suffix():
    assert variant("uni_td_full").target_type == "td_raw"
    assert variant("uni_anom_full").target_type == "td_anomaly"
    assert variant("tmin_anom_full").target_type == "td_anomaly"


def test_climatology_used_true_for_anomaly_target_or_anomaly_covariate():
    assert variant("uni_anom_full").climatology_used is True
    assert variant("tmin_anom_full").climatology_used is True


def test_climatology_used_false_for_raw_target_with_raw_covariates():
    assert variant("uni_td_full").climatology_used is False
    assert variant("tmin_td_full").climatology_used is False


def test_climatology_role_matches_climatology_used():
    for spec in VARIANTS:
        if not spec.climatology_used:
            assert spec.climatology_role is None
        elif spec.target_type == "td_anomaly":
            assert spec.climatology_role == "target_anomaly_base"
        else:
            assert spec.climatology_role == "input_covariate"


def test_inputs_is_an_alias_for_covariates():
    for spec in VARIANTS:
        assert spec.inputs == spec.covariates


def test_no_timesfm_variant_is_autoregressive():
    """Todas las variantes son de una sola pasada (zero-shot, horizonte completo
    en una llamada); ninguna realimenta su propia predicción como `tuned` de
    Palacios. Ver docs/protocol/timesfm_manifest.yaml, seccion `rivales`."""
    for spec in VARIANTS:
        assert spec.autoregressive is False


def test_build_provenance_for_raw_target_variant(tmp_path):
    spec = variant("tmin_td_full")
    panel_spec = split_spec("ll4")
    ids_file = tmp_path / "panels" / "nacional_17041.csv"
    target = tmp_path / "preds" / "ll4__tmin_td_full.parquet"

    record = build_provenance(
        spec,
        split="ll4",
        panel_spec=panel_spec,
        ids_file=ids_file,
        cells=[1, 2, 3],
        target=target,
        bead_id="tdew-214",
    )

    assert record.bead_id == "tdew-214"
    assert record.manifest_ref == "docs/protocol/timesfm_manifest.yaml@2026-09-22"
    assert record.model_family == "timesfm-3.0"
    assert record.model_id == spec.checkpoint
    assert record.variant_label == "tmin_td_full"
    assert record.trained is False
    assert record.training_period is None
    assert record.test_period == ("2013-01-01", "2016-12-31")
    assert record.split_id == "ll4"
    assert record.autoregressive is False
    assert record.target_type == "td_raw"
    assert record.climatology_used is False
    assert record.climatology_role is None
    assert record.inputs == ("TMIN",)
    assert record.panel_id == "nacional_17041"
    assert record.panel_cell_count == 3
    assert record.panel_file == str(ids_file)
    assert record.output_files == (str(target),)


def test_build_provenance_for_anomaly_target_variant_sets_climatology_role(tmp_path):
    spec = variant("tmin_anom_full")
    panel_spec = split_spec("ll4")

    record = build_provenance(
        spec,
        split="ll4",
        panel_spec=panel_spec,
        ids_file=tmp_path / "cribado_estratificado.csv",
        cells=range(1106),
        target=tmp_path / "out.parquet",
    )

    assert record.target_type == "td_anomaly"
    assert record.climatology_used is True
    assert record.climatology_role == "target_anomaly_base"
    assert record.panel_cell_count == 1106


def test_output_name_marks_the_context_override_and_keeps_the_default():
    """Escalera de contexto (tdew-03g): el recorte va en el nombre y no pisa la salida titular."""
    assert output_name("ll4", "tmin_anom_full") == "ll4__tmin_anom_full.parquet"
    assert output_name("ll4b", "tmin_anom_full", context_start_year=1991) == "ll4b__tmin_anom_full__ctx1991.parquet"
    assert (
        output_name("ll4", "tmin_anom_full", shard=(0, 2), context_start_year=1986)
        == "ll4__tmin_anom_full__ctx1986__shard0de2.parquet"
    )
    assert (
        output_name("ll4b", "tmin_anom_full", context_start_year=1991, clim_start_year=1981)
        == "ll4b__tmin_anom_full__ctx1991__clim1981.parquet"
    )


def test_build_provenance_records_the_context_override(tmp_path):
    spec = variant("tmin_anom_full")
    panel_spec = split_spec("ll4b", context_start_year=1996)
    common = dict(split="ll4b", panel_spec=panel_spec, ids_file=tmp_path / "cribado_estratificado.csv",
                  cells=[1, 2], target=tmp_path / "out.parquet")

    record = build_provenance(spec, context_start_year=1996, **common)
    assert "CONTEXTO desde 1996" in record.notes and "la variante dice 1981" in record.notes
    assert "CLIMATOLOGIA de las anomalias con 1996-2008" in record.notes
    assert f"{panel_spec.context_length} dias" in record.notes

    fixed = build_provenance(spec, context_start_year=1996, clim_start_year=1981,
                             **{**common, "panel_spec": split_spec("ll4b", context_start_year=1996,
                                                                   clim_start_year=1981)})
    assert "CLIMATOLOGIA de las anomalias con 1981-2008" in fixed.notes
    assert "--clim-start-year=1981" in fixed.notes

    default = build_provenance(spec, **common)
    assert "CONTEXTO" not in default.notes and "CLIMATOLOGIA" not in default.notes


def test_context_start_year_cli_reaches_run_variant(monkeypatch, tmp_path):
    from experiments.timesfm import run as run_mod

    seen = {}

    def fake_run_variant(keys, **kwargs):
        seen.update(kwargs)
        return pd.DataFrame([{"variant": "tmin_anom_full"}])

    monkeypatch.setattr(run_mod, "run_variant", fake_run_variant)
    ids = tmp_path / "ids.csv"
    pd.DataFrame({"ID": [1, 2]}).to_csv(ids, index=False)
    out = tmp_path / "out"
    out.mkdir()
    base = ["--variants", "tmin_anom_full", "--split", "ll4b", "--ids-file", str(ids), "--out-dir", str(out)]
    run_mod.main(base + ["--context-start-year", "1986"])
    assert seen["context_start_year"] == 1986 and seen["clim_start_year"] is None
    assert (out / "runtime_ll4b_ctx1986.csv").exists()
    run_mod.main(base + ["--context-start-year", "1986", "--clim-start-year", "1981"])
    assert seen["clim_start_year"] == 1981
    assert (out / "runtime_ll4b_ctx1986_clim1981.csv").exists()
    run_mod.main(base)
    assert seen["context_start_year"] is None and seen["clim_start_year"] is None
