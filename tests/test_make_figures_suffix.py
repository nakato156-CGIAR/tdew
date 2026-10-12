"""make_figures.build con sufijo: regenera las figuras desde los directorios
``*_limpio`` sin pisar las figuras con fuga (PLAN_1 §Paso 5, principio de no sobrescritura)."""
from __future__ import annotations

import shutil
from pathlib import Path

import pandas as pd

from experiments.timesfm import make_figures

REAL = Path(__file__).resolve().parents[1] / "reports/timesfm_benchmark"


def _report(tmp_path):
    report = tmp_path / "report"
    (report / "nacional_limpio").mkdir(parents=True)
    (report / "figs").mkdir()
    shutil.copy(REAL / "nacional_limpio/leaderboard.csv", report / "nacional_limpio/leaderboard.csv")
    for name in ("lead_time_curve.png", "ll4_bias_by_month.png", "ll4_delta_rmse_hist.png",
                 "ll1_rmse_ladder.png", "ll2_rmse_ladder.png", "ll4_rmse_ladder.png"):
        shutil.copy(REAL / "nacional_limpio" / name, report / "nacional_limpio" / name)
    pd.DataFrame({"split": "ll4", "method": ["tuned"] * 3 + ["timesfm"] * 3,
                  "dia": [1, 2, 3] * 2,
                  "rmse_acumulado": [1.0, 1.1, 1.2, .9, .9, .95]}).to_csv(
        report / "curva_error_nacional_limpio.csv", index=False)
    sentinel = report / "figs" / "escalera_nacional.png"
    sentinel.write_bytes(b"con-fuga")
    return report, sentinel


def test_suffix_build_writes_limpio_figures_and_keeps_leaky_ones(tmp_path):
    report, sentinel = _report(tmp_path)
    made = make_figures.build(report, suffix="_limpio")
    names = {p.name for p in made}
    assert {"escalera_nacional_limpio.png", "crecimiento_error_nacional_limpio.png",
            "nacional_curva_horizonte_limpio.png", "nacional_bias_by_month_limpio.png",
            "nacional_delta_rmse_hist_limpio.png", "nacional_rmse_ladder_limpio.png",
            "nacional_ll1_rmse_ladder_limpio.png", "nacional_ll2_rmse_ladder_limpio.png",
            } <= names
    assert all(p.exists() and p.stat().st_size > 0 for p in made)
    assert sentinel.read_bytes() == b"con-fuga"
    assert not (report / "figs" / "coste_throughput_limpio.png").exists()


def test_default_build_is_unchanged_without_suffix(tmp_path):
    report, _ = _report(tmp_path)
    assert make_figures.build(report) == []


def test_effect_figures_are_copied_from_the_matching_split_file(tmp_path):
    report, _ = _report(tmp_path)
    src = report / "nacional_limpio"
    for i, name in enumerate(("ll1_rmse_ladder.png", "ll2_rmse_ladder.png", "ll4_rmse_ladder.png")):
        (src / name).write_bytes(f"distinto-{i}".encode())
    make_figures.build(report, suffix="_limpio")
    figs = report / "figs"
    assert (figs / "nacional_ll1_rmse_ladder_limpio.png").read_bytes() == b"distinto-0"
    assert (figs / "nacional_ll2_rmse_ladder_limpio.png").read_bytes() == b"distinto-1"
    assert (figs / "nacional_rmse_ladder_limpio.png").read_bytes() == b"distinto-2"


def test_unsuffixed_build_reads_unsuffixed_inputs_only(tmp_path):
    report, _ = _report(tmp_path)
    (report / "nacional").mkdir()
    shutil.copy(report / "nacional_limpio/leaderboard.csv", report / "nacional/leaderboard.csv")
    made = make_figures.build(report)
    assert [p.name for p in made] == ["escalera_nacional.png"]
