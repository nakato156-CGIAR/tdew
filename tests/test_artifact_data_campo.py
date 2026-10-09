"""Datos del campo 2017-2020 que embebe la pagina interactiva (E9)."""

from __future__ import annotations

import copy
import json

import numpy as np
import pandas as pd
import pytest

from experiments.timesfm import artifact_data as ad

N, CELLS = ad.CAMPO_VALORES, ad.CAMPO_CELDAS
DAYS = 1461


def _write(report, name, frame):
    d = report / ad.CAMPO
    d.mkdir(parents=True, exist_ok=True)
    frame.to_csv(d / f"{name}_limpio.csv", index=False)


def make_inputs(tmp_path, *, scale=2.0):
    """CSV sinteticos que cuadran entre si; TimesFM = ``scale`` x anomalia de Palacios."""
    report, agg = tmp_path / "report", tmp_path / "agg"
    agg.mkdir()
    base = np.sin(np.arange(DAYS) / 40.0) * 0.5 + 0.3
    _write(report, "anomaly_series", pd.DataFrame({
        "day": np.arange(DAYS), "date": pd.date_range("2017-01-01", periods=DAYS).strftime("%Y-%m-%d"),
        "n": CELLS, "bias": 0.0, "rmse": 0.1, "mean_timesfm": 20.0, "mean_palacios": 20.0, "doy": 1,
        "clim_mean": 20.0, "anom_timesfm": base * scale, "anom_palacios": base}))
    _write(report, "product_figures", pd.DataFrame({
        "product": ["timesfm", "palacios"], "n": N, "cells": CELLS, "nan": 0, "inf": 0,
        "mean": [19.44, 19.39], "min": [-14.3, -13.3], "max": [40.9, 41.2], "rows_only_in_this_product": 0,
        "mean_2017": 19.4, "mean_2018": 19.3, "mean_2019": 19.5, "mean_2020": 19.5}))
    _write(report, "reproduction_palacios", pd.DataFrame({
        "quantity": ["n", "mean", "mean_2019", "mean_2020"], "paper": [N, 19.39, 19.41, 19.51],
        "observed": [N, 19.388, 19.398, 19.503], "diff": [0.0, -0.002, -0.012, -0.007], "ok": [True, True, False, False]}))
    _write(report, "agreement_overall", pd.DataFrame([{"n": N, "rmse": 0.46, "mae": 0.32, "bias": 0.05, "r": 0.998}]))
    for name, col, keys in (("year", "year", [2017, 2018]), ("tier", "tier", ["within", "unsupported"]),
                            ("site", "site", ["lima", "otro"]), ("month", "month", [1, 2])):
        _write(report, f"agreement_by_{name}", pd.DataFrame({col: keys, "n": 10, "rmse": 0.4, "mae": 0.3, "bias": 0.0, "r": 0.99}))
    _write(report, "drift", pd.DataFrame([{"series": "diferencia_timesfm_menos_palacios", "slope_per_year": -0.005,
                                           "ci_low": -0.04, "ci_high": 0.03, "significant": False}]))

    # Cola: dos niveles de soporte; 100 valores sobre 35 C en TimesFM y 60 en Palacios.
    cells_t, vals_t = [1_000_000, CELLS - 1_000_000], [1_500_000_000, N - 1_500_000_000]
    summary = {"timesfm": 100, "palacios": 60}
    tier, zona, mes, anio, resumen = [], [], [], [], []
    for name, above in summary.items():
        tier += [{"product": name, "tier": "within", "cells": cells_t[0], "values": vals_t[0], "above_35": 0, "pct_above_35": 0.0, "cells_affected": 0},
                 {"product": name, "tier": "unsupported", "cells": cells_t[1], "values": vals_t[1], "above_35": above, "pct_above_35": 1.0, "cells_affected": 60}]
        zona += [{"product": name, "zone_class": "selva_A(r)A'", "above_35": above},
                 {"product": name, "zone_class": "resto", "above_35": 0}]
        mes += [{"product": name, "zone_class": zc, "month": m, "values": 1, "above_35": above if m == 11 else 0}
                for zc in ("todo", "selva_A(r)A'") for m in range(1, 13)]
        anio += [{"product": name, "year": y, "values": 1, "above_35": above if y == 2017 else 0} for y in (2017, 2018, 2019, 2020)]
        resumen.append({"product": name, "n": N, "nan": 0, "max": 40.0, "cells": CELLS,
                        "cells_with_exceedance": 5 if name == "timesfm" else 3, "above_35": above,
                        "pct_above_35": above / N * 100, "above_38": above // 4})
    _write(report, "tail_summary", pd.DataFrame(resumen))
    _write(report, "tail_by_tier", pd.DataFrame(tier))
    _write(report, "tail_by_zone_class", pd.DataFrame(zona))
    _write(report, "tail_by_month", pd.DataFrame(mes))
    _write(report, "tail_by_year", pd.DataFrame(anio))
    _write(report, "tail_joint", pd.DataFrame([{"zone_class": "todo", "rows": 10, "both_above_35": 3}]))
    _write(report, "tail_survival", pd.DataFrame([{"product": "timesfm", "group": "todo", "x": 35.0, "n_ge": 100,
                                                    "frac_ge": 1e-7, "n_group": 10}]))
    # Mapa: 3 celdas solo TimesFM + 2 comunes = 5 afectadas en TimesFM; 1 solo Palacios + 2 comunes = 3.
    pd.DataFrame({"ID": [10, 20, 30, 40, 50, 60], "n_above_timesfm": [1, 2, 3, 4, 5, 0],
                  "n_above_palacios": [0, 0, 0, 7, 8, 9]}).to_csv(agg / "tail_by_cell_limpio.csv", index=False)
    man = pd.DataFrame({"bucket": np.arange(8192), "cells_written": 0, "n_omitted": 0, "rows": 0, "bytes": 1,
                        "seconds": 1.0, "quantile_violation_rows": 0})
    man.loc[0, ["cells_written", "rows"]] = [CELLS, N]
    man_path = tmp_path / "MANIFEST.csv"
    man.to_csv(man_path, index=False)
    return report, agg, man_path


def payload_of(tmp_path, **kw):
    report, agg, man = make_inputs(tmp_path, **kw)
    return {"campo": ad.campo(report, agg, man)}, report


def test_plain_keeps_text_ints_and_bools_and_rounds_floats_and_nan_to_none():
    frame = pd.DataFrame({"a": ["x"], "b": [3], "c": [True], "d": [0.123456789], "e": [np.nan]})
    row = ad._plain(frame)[0]
    assert row == {"a": "x", "b": 3, "c": True, "d": 0.123457, "e": None}
    assert type(row["b"]) is int and type(row["c"]) is bool


def test_campo_is_strict_json_and_copies_the_csv_tables(tmp_path):
    payload, _ = payload_of(tmp_path)
    json.dumps(payload, allow_nan=False)
    c = payload["campo"]
    assert c["acuerdo"]["global"]["n"] == N
    assert [r["tier"] for r in c["acuerdo"]["tier"]] == ["within", "unsupported"]
    assert c["control"][0]["ok"] is True
    assert c["manifiesto"] == {"buckets": 8192, "celdas": CELLS, "omitidas": 0, "filas": N, "bytes": 8192,
                               "segundos": 8192.0, "celdas_por_s": pytest.approx(CELLS / 8192.0),
                               "violaciones_cuantiles": 0}


def test_anomaly_statistics_are_computed_from_the_daily_series(tmp_path):
    payload, _ = payload_of(tmp_path, scale=2.0)
    s = payload["campo"]["anomalia"]["estadisticos"]
    assert s["dias"] == DAYS and s["r"] == pytest.approx(1.0)
    assert s["cociente_desv"] == pytest.approx(2.0) and s["acuerdo_signo"] == pytest.approx(1.0)
    cal = s["extremos_calidos"]
    assert cal["n"] > 0 and cal["timesfm"] == pytest.approx(2.0 * cal["palacios"])
    assert s["dif_media"] == pytest.approx(s["media_palacios"])  # TimesFM - Palacios = Palacios si scale=2
    assert len(payload["campo"]["anomalia"]["timesfm"]) == DAYS


def test_cola_layer_codes_each_cell_by_which_product_exceeds(tmp_path):
    _, agg, _ = make_inputs(tmp_path)
    blob, counts = ad.cola_layer(agg)
    assert counts == {"solo_timesfm": 3, "solo_palacios": 1, "ambos": 2}
    import base64, zlib
    layer = np.frombuffer(zlib.decompress(base64.b64decode(blob)), dtype=np.uint8)
    assert layer.size == ad.N_LAT * ad.N_LON
    assert [int(layer[i]) for i in (10, 20, 30, 40, 50, 60)] == [1, 1, 1, 3, 3, 2]
    assert int((layer > 0).sum()) == 6


@pytest.fixture()
def paper_like(monkeypatch):
    """Las cifras sinteticas no son las del paper: se ajusta la referencia a lo que genera make_inputs."""
    monkeypatch.setattr(ad, "PAPER_COLA", {"celdas_por_tier": {"within": 0, "unsupported": 60}, "celdas": 3,
                                           "pct": round(60 / N * 100, 4), "max": 40.0})


def test_check_parity_campo_accepts_consistent_data(tmp_path, paper_like):
    payload, report = payload_of(tmp_path)
    ad.check_parity_campo(payload, report)


def test_check_parity_campo_aborts_if_palacios_does_not_reproduce_the_paper_tail(tmp_path):
    payload, report = payload_of(tmp_path)  # sin ajustar: las cifras sinteticas no son las del paper
    with pytest.raises(ValueError, match="paper"):
        ad.check_parity_campo(payload, report)


def test_ratios_and_extreme_days_are_computed_in_the_builder(tmp_path):
    payload, _ = payload_of(tmp_path)
    r = payload["campo"]["cola"]["razones"]
    assert r["tasa_35"] == pytest.approx(100 / 60) and r["celdas"] == pytest.approx(5 / 3)
    assert r["noviembre"]["timesfm"] == pytest.approx(1.0) and r["noviembre"]["palacios"] == pytest.approx(1.0)
    s = payload["campo"]["anomalia"]["estadisticos"]
    assert s["dia_mas_calido"]["timesfm"]["valor"] == pytest.approx(2.0 * s["dia_mas_calido"]["palacios"]["valor"])
    assert s["dia_mas_frio"]["palacios"]["fecha"].startswith("20")


@pytest.mark.parametrize("mutate, message", [
    (lambda c: c["producto"][0].__setitem__("cells", 5), "celdas"),
    (lambda c: c["cola"]["tier"][1].__setitem__("above_35", 1), "por tier"),
    (lambda c: c["cola"]["zona"][0].__setitem__("above_35", 1), "por clase"),
    (lambda c: c["cola"]["mes"][0].__setitem__("above_35", 1), "mes"),
    (lambda c: c["cola"]["celdas"].__setitem__("ambos", 0), "mapa"),
    (lambda c: c["anomalia"]["timesfm"].pop(), "1 461"),
    (lambda c: c["manifiesto"].__setitem__("omitidas", 3), "manifiesto"),
    (lambda c: c["control"][2].__setitem__("ok", True), "control de reproduccion"),
    (lambda c: c["acuerdo"]["global"].__setitem__("n", 5), "acuerdo"),
])
def test_check_parity_campo_aborts_on_each_inconsistency(tmp_path, paper_like, mutate, message):
    payload, report = payload_of(tmp_path)
    broken = copy.deepcopy(payload)
    mutate(broken["campo"])
    with pytest.raises(ValueError, match=message):
        ad.check_parity_campo(broken, report)


def test_check_parity_campo_works_without_a_manifest(tmp_path, paper_like):
    report, agg, _ = make_inputs(tmp_path)
    payload = {"campo": ad.campo(report, agg, tmp_path / "no_existe.csv")}
    assert payload["campo"]["manifiesto"] is None
    ad.check_parity_campo(payload, report)


def test_kl_layer_parity(tmp_path):
    from experiments.timesfm import artifact_data as ad

    d = tmp_path / ad.KL_DIR
    d.mkdir()
    counts = {"obs": [10, 30, 60], "palacios": [20, 30, 50], "timesfm": [12, 31, 57]}
    hist = pd.DataFrame({"bin_lo": [0.0, 0.5, 1.0], "bin_hi": [0.5, 1.0, 1.5], **counts})
    hist.to_csv(d / "kl_hist_limpio.csv", index=False)
    rows = []
    for m in ("palacios", "timesfm"):
        p = np.array(counts["obs"]) + 0.5
        q = np.array(counts[m]) + 0.5
        p, q = p / p.sum(), q / q.sum()
        rows.append({"group_kind": "todo", "group": "todo", "method": m, "bin_width": 0.5, "n": 100,
                     "n_out_of_range": 0, "kl_obs_method": float(np.sum(p * np.log(p / q))),
                     "kl_method_obs": 0.0, "jsd": 0.0})
    pd.DataFrame(rows).to_csv(d / "kl_by_group_limpio.csv", index=False)
    payload = {"kl": ad.kl_layer(tmp_path)}
    ad.check_parity_kl(payload, tmp_path)
    payload["kl"]["bins"]["aporte_timesfm"][0] += 0.01
    with pytest.raises(ValueError, match="paridad de KL"):
        ad.check_parity_kl(payload, tmp_path)
