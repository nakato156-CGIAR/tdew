"""E5 y E8 en el artefacto interactivo: los datos salen de los CSV *_limpio de
PLAN_2, la paridad los protege y la pagina los muestra con las mismas cifras."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

import pandas as pd
import pytest

from experiments.timesfm import artifact_data

REAL = Path(__file__).resolve().parents[1] / "reports/timesfm_benchmark"
HTML = REAL / "artifact/index.html"
DATOS = REAL / "artifact/datos.js"


def _datos() -> dict:
    text = DATOS.read_text(encoding="utf-8")
    return json.loads(text[len("window.DATOS = "):].rstrip().rstrip(";"))


# ----------------------------------------------------------- datos (builder)

def test_tables_carry_every_tier_and_monthly_row_from_the_clean_csvs():
    t = artifact_data.tables(REAL)
    tiers = pd.read_csv(REAL / "nacional_limpio/tiers_limpio.csv")
    monthly = pd.read_csv(REAL / "nacional_limpio/sesgo_mensual_limpio.csv")
    assert len(t["soporte"]) == len(tiers) == 75
    assert len(t["sesgoMensual"]) == len(monthly) == 180
    for row in t["soporte"]:
        src = tiers[(tiers.split == row["split"]) & (tiers.tier == row["tier"])
                    & (tiers.method == row["method"])].iloc[0]
        for k in ("cells", "n", "rmse", "mae", "bias", "r", "skill"):
            assert row[k] == pytest.approx(src[k], abs=6e-5), (row["tier"], row["method"], k)
    for row in t["sesgoMensual"]:
        src = monthly[(monthly.split == row["split"]) & (monthly.method == row["method"])
                      & (monthly.month == row["month"])].iloc[0]
        assert row["bias_pooled"] == pytest.approx(src["bias_pooled"], abs=6e-5)
        if row["split"] == "ll4":
            assert row["cell_bias_std"] == pytest.approx(src["cell_bias_std"], abs=6e-5)
        else:
            assert row["cell_bias_std"] is None  # sin dispersion fuera de ll4: null, no NaN


def test_serialized_payload_is_strict_json_for_the_new_tables():
    t = artifact_data.tables(REAL)
    json.dumps({"soporte": t["soporte"], "sesgoMensual": t["sesgoMensual"]}, allow_nan=False)


def test_tier_and_month_tables_come_from_nacional_limpio_only(tmp_path):
    report = tmp_path / "report"
    shutil.copytree(REAL, report, ignore=shutil.ignore_patterns("artifact", "figs", "geo"))
    (report / "nacional_limpio/tiers_limpio.csv").write_text(
        "split,tier,method,cells,n,rmse,mae,bias,r,clim_rmse,skill\nll4,within,timesfm,1,1,9.0,9.0,9.0,0.5,9.0,0.0\n")
    t = artifact_data.tables(report)
    assert len(t["soporte"]) == 1 and t["soporte"][0]["rmse"] == 9.0


# -------------------------------------------------------------------- paridad

def _payload():
    return {"tablas": artifact_data.tables(REAL)}


def _row(payload, key, **match):
    return next(r for r in payload["tablas"][key] if all(r[k] == v for k, v in match.items()))


def test_parity_accepts_the_published_tier_and_month_tables():
    artifact_data.check_parity(_payload(), REAL)


@pytest.mark.parametrize("tamper", [
    lambda p: _row(p, "soporte", split="ll4", tier="within", method="tuned").update(rmse=0.95),
    lambda p: _row(p, "soporte", split="ll4", tier="unsupported", method="timesfm").update(rmse=1.60),
    lambda p: _row(p, "soporte", split="ll4", tier="near", method="timesfm").update(cells=1778),
    lambda p: _row(p, "sesgoMensual", split="ll4", method="tuned", month=12).update(bias_pooled=0.2),
    lambda p: _row(p, "sesgoMensual", split="ll4", method="timesfm", month=1).update(bias_pooled=-0.2),
    lambda p: p["tablas"]["soporte"].pop(),
    lambda p: p["tablas"]["sesgoMensual"].pop(),
])
def test_parity_detects_tampering_of_tier_and_month_tables(tamper):
    payload = _payload()
    tamper(payload)
    with pytest.raises(ValueError):
        artifact_data.check_parity(payload, REAL)


def test_parity_fails_when_the_new_tables_are_missing():
    payload = _payload()
    del payload["tablas"]["soporte"]
    with pytest.raises((ValueError, KeyError)):
        artifact_data.check_parity(payload, REAL)


# ----------------------------------------------------------------------- HTML

def _html() -> str:
    return HTML.read_text(encoding="utf-8")


def test_section_numbers_are_consecutive_and_unique():
    nums = re.findall(r'section-index">(\d\d) · ', _html())
    assert nums == [f"{i:02d}" for i in range(1, len(nums) + 1)]
    # Paper, Controles, Alcance, Limites y Protocolo (tdew-214.18).
    assert len(nums) == 5


def _exact_tier_gaps() -> dict[str, float]:
    t = pd.read_csv(REAL / "nacional_limpio/tiers_limpio.csv").query("split == 'll4'")
    w = t.pivot(index="tier", columns="method", values="rmse")
    return (w["tuned"] - w["timesfm"]).to_dict()


def test_datos_js_keeps_enough_precision_for_derived_differences():
    """El navegador resta RMSE ya volcados: con 4 decimales 0.9464 − 0.8669 daria 0.0795
    y se mostraria 0.080 en vez de 0.079."""
    d = _datos()["tablas"]["soporte"]
    rows = {(r["tier"], r["method"]): r["rmse"] for r in d if r["split"] == "ll4"}
    for tier, exact in _exact_tier_gaps().items():
        assert abs((rows[(tier, "tuned")] - rows[(tier, "timesfm")]) - exact) < 5e-6, tier
