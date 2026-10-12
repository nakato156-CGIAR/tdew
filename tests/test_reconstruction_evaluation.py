from __future__ import annotations

import numpy as np
import pandas as pd

from experiments.reconstruction.baselines import apply_shrinkage, fit_shrinkage_alpha
from experiments.reconstruction.evaluation import approval_gate, evaluate_predictions, paired_cell_tests


DEPARTMENTS = ("Lima", "Cusco", "Loreto", "San Martin")


def _predictions(model: str, error: float) -> pd.DataFrame:
    rows = []
    for seed in (0, 1, 2):
        for dep_idx, department in enumerate(DEPARTMENTS):
            for year in (1, 2, 3, 4):
                for cell_offset in range(3):
                    obs = 10.0 + dep_idx + year + cell_offset * 0.1
                    rows.append(
                        {
                            "ID": dep_idx * 10 + cell_offset,
                            "department": department,
                            "date": pd.Timestamp(2012 + year, 6, 1),
                            "year_horizon": year,
                            "TD_obs": obs,
                            "TD_clim": obs + 1.0,
                            "TD_pred": obs + error * (-1 if cell_offset == 0 else 1),
                            "model": model,
                            "seed": seed,
                            "fold": "ll4",
                        }
                    )
    return pd.DataFrame(rows)


def test_metrics_include_department_and_horizon_skill():
    metrics = evaluate_predictions(_predictions("candidate", 0.1))
    assert {"pooled", "department", "horizon_year", "department_horizon_year", "month"} <= set(metrics["level"])
    assert (metrics["skill_vs_climatology"] > 0).all()


def test_paired_tests_and_approval_accept_clear_improvement():
    candidate = _predictions("candidate", 0.05)
    tuned = _predictions("tuned", 0.5)
    paired = paired_cell_tests(
        candidate[candidate.seed == 0], tuned[tuned.seed == 0], n_bootstrap=200, n_permutations=200, seed=0
    )
    assert paired.rmse_difference < 0 and paired.ci_upper < 0
    result = approval_gate(candidate, tuned, n_bootstrap=200, n_permutations=200, seed=0)
    assert result.approved, result.failures


def test_department_shrinkage_is_bounded_and_reduces_to_climatology():
    frame = pd.DataFrame(
        {
            "department": ["Lima", "Lima"],
            "TD_obs": [10.0, 10.0],
            "TD_clim": [10.0, 10.0],
            "TD_pred": [20.0, 0.0],
        }
    )
    alphas = fit_shrinkage_alpha(frame)
    assert alphas == {"Lima": 0.0}
    np.testing.assert_array_equal(apply_shrinkage(frame, alphas), frame["TD_clim"])
