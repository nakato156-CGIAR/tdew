"""Score the withheld-year validation by observational-support tier.

The pooled accuracy figure averages over a field half of which lies beyond the classified
domain, where the source product is weakly constrained. That average therefore describes
neither the region the product is used in nor the region it is extrapolated into. Splitting
it costs nothing: the tiers come from a static per-cell distance and the predictions already
exist.

The split is on an external criterion, the classified domain, fixed before any error was
examined, and every tier is reported. Reads the leak-free backtest.
"""
import os

import numpy as np
import pandas as pd

RES = os.environ.get("RES", "/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning")
ROOT = os.environ.get("BACKTEST_ROOT", f"{RES}/tuning/backtest_clean")
TIERS = ["within", "near", "marginal", "extrapolated", "unsupported"]


def score(pred: np.ndarray, obs: np.ndarray) -> dict:
    e = pred - obs
    ok = np.isfinite(e)
    e, p, o = e[ok], pred[ok], obs[ok]
    return {
        "rmse": float(np.sqrt((e ** 2).mean())),
        "mae": float(np.abs(e).mean()),
        "bias": float(e.mean()),
        "r": float(np.corrcoef(p, o)[0, 1]),
    }


def main() -> int:
    sd = pd.read_parquet(f"{RES}/tuning/support_distance.parquet",
                         columns=["ID", "dist_km", "tier"])
    rows = []
    for split in ("ll1", "ll2", "ll4"):
        f = f"{ROOT}/{split}/predictions.parquet"
        if not os.path.exists(f):
            continue
        d = pd.read_parquet(f, columns=["ID", "TD_obs", "pred_tuned", "pred_clim",
                                        "pred_tmin", "pred_ols"]).merge(sd, on="ID")
        for t in TIERS:
            s = d[d.tier == t]
            if not len(s):
                continue
            obs = s["TD_obs"].to_numpy(dtype=float)
            m = score(s["pred_tuned"].to_numpy(dtype=float), obs)
            c = score(s["pred_clim"].to_numpy(dtype=float), obs)
            rows.append({
                "split": split, "tier": t, "cells": s["ID"].nunique(), "n": len(s),
                **{f"tuned_{k}": v for k, v in m.items()},
                "clim_rmse": c["rmse"],
                "skill": 1 - m["rmse"] / c["rmse"],
                "tmin_rmse": score(s["pred_tmin"].to_numpy(dtype=float), obs)["rmse"],
                "ols_rmse": score(s["pred_ols"].to_numpy(dtype=float), obs)["rmse"],
            })
    t = pd.DataFrame(rows)
    t.to_csv(os.path.join(os.path.dirname(__file__), "validation_by_support.csv"), index=False)

    four = t[t.split == "ll4"]
    print("=== four-year withheld block, by support tier ===")
    print(f"{'tier':>14} {'cells':>7} {'RMSE':>7} {'MAE':>6} {'bias':>7} {'r':>6} "
          f"{'clim':>7} {'skill':>7} {'Td=Tmin':>8} {'zone OLS':>9}")
    for _, r in four.iterrows():
        print(f"{r.tier:>14} {r.cells:>7,} {r.tuned_rmse:>7.3f} {r.tuned_mae:>6.3f} "
              f"{r.tuned_bias:>+7.3f} {r.tuned_r:>6.3f} {r.clim_rmse:>7.3f} "
              f"{r.skill:>7.3f} {r.tmin_rmse:>8.3f} {r.ols_rmse:>9.3f}")

    print("\n=== skill by tier and lead time ===")
    piv = t.pivot(index="tier", columns="split", values="skill").reindex(TIERS)
    print(piv.round(3).to_string())
    print("\nskill declines with lead time within every tier: "
          f"{bool((piv['ll1'] > piv['ll2']).all() and (piv['ll2'] > piv['ll4']).all())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
