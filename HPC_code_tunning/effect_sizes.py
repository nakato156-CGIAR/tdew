"""Phase-A effect sizes, bootstrap CIs, and a null test (plan §4/§5, task A3).

Consumes a backtest ``predictions.parquet`` (from ``backtest.py``: one row per held-out
ID x day with ``TD_obs`` and each method's prediction) and turns the raw errors into the
paper's inferential evidence, reported as **effect sizes with uncertainty**, not p-values
alone:

* **ΔRMSE (°C) with block-bootstrap CIs.** The block is the *location* (ID): we resample
  IDs with replacement and recompute the pooled RMSE, so within-location temporal
  autocorrelation is respected (each cell's whole time series moves together). 95% CI on
  ``RMSE_baseline − RMSE_tuned`` for every baseline.
* **Skill vs climatology / vs Td=Tmin** with the same bootstrap CI.
* **Per-location improvement distribution** and the **fraction of cells where tuned wins**
  (paired per-ID RMSE).
* **Cohen's d** on the paired per-location RMSE differences (companion effect size).
* **Paired permutation (sign-flip) null test** on per-location ΔRMSE: under H0 (tuned no
  better than baseline) each location's improvement is equally likely +/−, so we flip signs
  at random and build the null distribution of the mean ΔRMSE → a p-value that tuned's
  aggregate advantage is not chance.

  NOTE the stronger "shuffle-years, re-select" null (§4) targets the *selection* uplift
  (tuned vs fixed-5) and needs the re-selection machinery — that is deferred to task A5;
  this module's null tests tuned vs the incumbent baselines.

Plots (matplotlib, Agg): RMSE ladder with bootstrap CIs, per-location ΔRMSE histogram,
lead-time skill curve (across splits), and tuned bias-by-month (the known Dec warm-bias
check). Writes ``effect_sizes.csv`` + PNGs next to the predictions.
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

from experiments.timesfm.evaluate import build_row_provenance
from tdew_estimation import provenance as prov

logger = logging.getLogger("effect_sizes")

METHOD_COLS = {
    "climatology": "pred_clim",
    "td_eq_tmin": "pred_tmin",
    "zone_ols": "pred_ols",
    "tuned": "pred_tuned",
    # Added for the TimesFM benchmark (bead tdew-214). Methods whose column is
    # absent from a given predictions.parquet are skipped, so the original
    # four-method files keep working unchanged.
    "timesfm": "pred_timesfm",
}
DEFAULT_FOCAL = "tuned"


def present_methods(df: pd.DataFrame) -> Dict[str, str]:
    """The subset of METHOD_COLS whose prediction column exists in ``df``."""
    return {m: c for m, c in METHOD_COLS.items() if c in df.columns}


# ---------------------------------------------------------------------------------------
# Per-location sufficient stats (sum of squared error + count) for fast bootstrapping
# ---------------------------------------------------------------------------------------
def _per_id_se(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Per-ID sum of squared error and finite count for one method."""
    err = df[col].to_numpy(dtype=float) - df["TD_obs"].to_numpy(dtype=float)
    finite = np.isfinite(err)
    g = pd.DataFrame({"ID": df["ID"].to_numpy()[finite], "se": err[finite] ** 2})
    out = g.groupby("ID").agg(se=("se", "sum"), n=("se", "size")).reset_index()
    return out


def _pooled_rmse(se: np.ndarray, n: np.ndarray) -> float:
    tot = n.sum()
    return float(np.sqrt(se.sum() / tot)) if tot > 0 else np.nan


def block_bootstrap_delta(
    per_id: pd.DataFrame, method: str, baseline: str, n_boot: int, seed: int
) -> Dict[str, float]:
    """Bootstrap ``RMSE_baseline − RMSE_tuned`` by resampling location blocks (IDs).

    ``per_id`` has columns ``se_<m>``/``n_<m>`` per method aligned on ID. Returns point
    ΔRMSE, skill (1 − RMSE_m/RMSE_base), and their 95% percentile CIs.
    """
    rng = np.random.default_rng(seed)
    se_m = per_id[f"se_{method}"].to_numpy()
    n_m = per_id[f"n_{method}"].to_numpy()
    se_b = per_id[f"se_{baseline}"].to_numpy()
    n_b = per_id[f"n_{baseline}"].to_numpy()

    rmse_m = _pooled_rmse(se_m, n_m)
    rmse_b = _pooled_rmse(se_b, n_b)
    point_delta = rmse_b - rmse_m
    point_skill = 1.0 - rmse_m / rmse_b if rmse_b else np.nan

    n_ids = len(per_id)
    deltas = np.empty(n_boot)
    skills = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, n_ids, n_ids)
        rm = _pooled_rmse(se_m[idx], n_m[idx])
        rb = _pooled_rmse(se_b[idx], n_b[idx])
        deltas[i] = rb - rm
        skills[i] = 1.0 - rm / rb if rb else np.nan
    return {
        "rmse": rmse_m,
        "rmse_baseline": rmse_b,
        "delta_rmse": point_delta,
        "delta_lo": float(np.nanpercentile(deltas, 2.5)),
        "delta_hi": float(np.nanpercentile(deltas, 97.5)),
        "skill": point_skill,
        "skill_lo": float(np.nanpercentile(skills, 2.5)),
        "skill_hi": float(np.nanpercentile(skills, 97.5)),
    }


def per_location_delta_rmse(per_id: pd.DataFrame, method: str, baseline: str) -> np.ndarray:
    """Per-location ``RMSE_baseline − RMSE_tuned`` (positive = method better at that cell)."""
    rm = np.sqrt(per_id[f"se_{method}"].to_numpy() / per_id[f"n_{method}"].to_numpy())
    rb = np.sqrt(per_id[f"se_{baseline}"].to_numpy() / per_id[f"n_{baseline}"].to_numpy())
    return rb - rm


def cohens_d_paired(delta: np.ndarray) -> float:
    """Cohen's d for paired differences: mean(Δ) / sd(Δ)."""
    delta = delta[np.isfinite(delta)]
    sd = np.std(delta, ddof=1)
    return float(np.mean(delta) / sd) if sd > 0 else np.nan


def sign_flip_permutation(delta: np.ndarray, n_perm: int, seed: int) -> float:
    """One-sided p-value that mean per-location ΔRMSE > 0 under random sign flips (H0)."""
    rng = np.random.default_rng(seed)
    delta = delta[np.isfinite(delta)]
    obs = np.mean(delta)
    mag = np.abs(delta)
    ge = 0
    for _ in range(n_perm):
        signs = rng.choice((-1.0, 1.0), size=mag.size)
        if np.mean(signs * mag) >= obs:
            ge += 1
    return (ge + 1) / (n_perm + 1)


# ---------------------------------------------------------------------------------------
# Orchestration for one split
# ---------------------------------------------------------------------------------------
def focal_provenance_method_name(focal: str, timesfm_variant: Optional[str]) -> Optional[str]:
    """The method name to pass to ``build_row_provenance`` for ``focal``, or
    ``None`` when there isn't enough information to record provenance (a bare
    ``"timesfm"`` focal with no ``--timesfm-variant``, since this module has no
    other way to know which variant was merged into ``pred_timesfm``)."""
    if focal != "timesfm":
        return focal
    if not timesfm_variant:
        return None
    return f"timesfm:{timesfm_variant}"


def analyze_split(
    pred_path: Path,
    *,
    n_boot: int = 1000,
    n_perm: int = 5000,
    seed: int = 0,
    focal: str = DEFAULT_FOCAL,
    baselines: Optional[Sequence[str]] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Return (effect-size table focal-vs-each-baseline, per-ID delta frame) for a split.

    ``focal`` is the method under test; every other present method becomes a
    baseline unless ``baselines`` says otherwise. The default reproduces the
    original behaviour exactly (tuned against the three baselines).
    """
    df = pd.read_parquet(pred_path)
    df = df.dropna(subset=["TD_obs"])

    methods = present_methods(df)
    if focal not in methods:
        raise KeyError(f"{focal!r} has no column in {pred_path}; present: {sorted(methods)}")

    # Align per-ID SE/n for every method on a common ID index.
    per_id: Optional[pd.DataFrame] = None
    for m, col in methods.items():
        s = _per_id_se(df, col).rename(columns={"se": f"se_{m}", "n": f"n_{m}"})
        per_id = s if per_id is None else per_id.merge(s, on="ID", how="inner")
    assert per_id is not None

    if baselines is None:
        baselines = [m for m in methods if m != focal]

    rows = []
    for baseline in baselines:
        if baseline not in methods:
            logger.warning("skip baseline %s: no column in %s", baseline, pred_path)
            continue
        bs = block_bootstrap_delta(per_id, focal, baseline, n_boot, seed)
        delta = per_location_delta_rmse(per_id, focal, baseline)
        rows.append({
            "focal": focal,
            "comparison": f"{focal}_vs_{baseline}",
            "rmse_focal": bs["rmse"],
            "rmse_baseline": bs["rmse_baseline"],
            "delta_rmse_C": bs["delta_rmse"],
            "delta_ci95": f"[{bs['delta_lo']:.3f}, {bs['delta_hi']:.3f}]",
            "skill": bs["skill"],
            "skill_ci95": f"[{bs['skill_lo']:.3f}, {bs['skill_hi']:.3f}]",
            "frac_cells_focal_wins": float(np.mean(delta > 0)),
            "cohens_d": cohens_d_paired(delta),
            "perm_p_value": sign_flip_permutation(delta, n_perm, seed),
            "n_cells": int(len(per_id)),
            # Legacy column names, kept so older readers of effect_sizes.csv
            # do not break; identical values to the *_focal columns.
            "rmse_tuned": bs["rmse"],
            "frac_cells_tuned_wins": float(np.mean(delta > 0)),
        })
    return pd.DataFrame(rows), per_id


# ---------------------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------------------
def _plots(
    pred_path: Path,
    per_id: pd.DataFrame,
    out_dir: Path,
    split_name: str,
    *,
    focal: str = DEFAULT_FOCAL,
) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    df = pd.read_parquet(pred_path).dropna(subset=["TD_obs"])

    # 1. RMSE ladder.
    methods = [m for m in present_methods(df) if f"se_{m}" in per_id.columns]
    rmses = [_pooled_rmse(per_id[f"se_{m}"].to_numpy(), per_id[f"n_{m}"].to_numpy()) for m in methods]
    fig, ax = plt.subplots(figsize=(6, 4))
    palette = ["#8a8f98", "#c77857", "#c7a233", "#4c78a8", "#59a14f"]
    colors = [palette[i % len(palette)] for i in range(len(methods))]
    ax.bar(methods, rmses, color=colors)
    for i, v in enumerate(rmses):
        ax.text(i, v + 0.02, f"{v:.3f}", ha="center", va="bottom", fontsize=9)
    ax.set_ylabel("RMSE (°C)")
    ax.set_title(f"Backtest RMSE ladder — {split_name}")
    fig.tight_layout(); fig.savefig(out_dir / "rmse_ladder.png", dpi=130); plt.close(fig)

    # 2. Per-location ΔRMSE vs climatology.
    delta = per_location_delta_rmse(per_id, focal, "climatology")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(delta[np.isfinite(delta)], bins=50, color="#4c78a8", alpha=0.85)
    ax.axvline(0, color="k", lw=1)
    ax.set_xlabel(f"ΔRMSE per cell (climatology − {focal}, °C)  →  right = {focal} better")
    ax.set_ylabel("cells")
    ax.set_title(f"Per-cell improvement over climatology — {split_name}\n"
                 f"{focal} wins {np.mean(delta > 0) * 100:.1f}% of cells")
    fig.tight_layout(); fig.savefig(out_dir / "delta_rmse_hist.png", dpi=130); plt.close(fig)

    # 3. Bias by month (the known Dec warm-bias check).
    d = df.copy()
    d["month"] = pd.to_datetime(d["FECHA"]).dt.month
    d["err"] = d[METHOD_COLS[focal]] - d["TD_obs"]
    mb = d.groupby("month")["err"].mean()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(mb.index, mb.to_numpy(), color=["#c77857" if v > 0 else "#4c78a8" for v in mb])
    ax.axhline(0, color="k", lw=1)
    ax.set_xlabel("month"); ax.set_ylabel("mean bias (pred − obs, °C)")
    ax.set_title(f"{focal} bias by month — {split_name}")
    fig.tight_layout(); fig.savefig(out_dir / "bias_by_month.png", dpi=130); plt.close(fig)


def lead_time_plot(
    metrics_all: pd.DataFrame, out_path: Path, *, methods: Sequence[str] = (DEFAULT_FOCAL,)
) -> None:
    """Skill-vs-climatology across splits (lead-time curve), one line per method."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    order = {"ll1": 1, "ll2": 2, "ll4": 4}
    palette = ["#4c78a8", "#59a14f", "#c77857", "#c7a233"]
    fig, ax = plt.subplots(figsize=(6, 4))
    drawn = 0
    for index, method in enumerate(methods):
        t = metrics_all[metrics_all["method"] == method].copy()
        t["lead"] = t["split"].map(order)
        t = t.dropna(subset=["lead"]).sort_values("lead")
        if t.empty:
            continue
        color = palette[index % len(palette)]
        ax.plot(t["lead"], t["skill_vs_clim"], "o-", color=color, label=method)
        for _, r in t.iterrows():
            ax.text(r["lead"], r["skill_vs_clim"] + 0.005, f"{r['skill_vs_clim']:.3f}",
                    ha="center", fontsize=9, color=color)
        drawn += 1
    if not drawn:
        plt.close(fig)
        return
    ax.set_xlabel("holdout length / max lead (years)")
    ax.set_ylabel("skill vs climatology")
    ax.set_title("Lead-time curve — skill vs climatology")
    ax.set_xticks(sorted(order.values()))
    # Headroom so the value label above the topmost point is not clipped.
    low, high = ax.get_ylim()
    ax.set_ylim(low, high + (high - low) * 0.10)
    if drawn > 1:
        ax.legend(frameon=False)
    fig.tight_layout(); fig.savefig(out_path, dpi=130); plt.close(fig)


# ---------------------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------------------
def main(argv=None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--backtest-root", required=True, type=Path,
                   help="dir holding <split>/predictions.parquet (e.g. $RES/tuning/backtest_clean)")
    p.add_argument("--manifest-ref", default=None,
                   help="governing document recorded in provenance (default: the original manifest)")
    p.add_argument("--notes", default=None,
                   help="free text appended to the provenance notes, e.g. which reference run "
                        "--backtest-root derives from")
    p.add_argument("--splits", type=str, default="ll1,ll2,ll4")
    p.add_argument("--n-boot", type=int, default=1000)
    p.add_argument("--n-perm", type=int, default=5000)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--focal", type=str, default=DEFAULT_FOCAL,
                   help=f"method under test; one of {sorted(METHOD_COLS)}")
    p.add_argument("--baselines", type=str, default=None,
                   help="comma list; default = every other method present in the file")
    p.add_argument("--lead-time-methods", type=str, default=None,
                   help="comma list drawn on lead_time_curve.png; default = the focal method")
    p.add_argument("--bead-id", default="tdew-214",
                   help="bead governing this run, for tdew_estimation.provenance")
    p.add_argument("--timesfm-variant", default=None,
                   help="variant key merged into pred_timesfm (see experiments.timesfm.variants); "
                        "required for provenance whenever --focal=timesfm")
    p.add_argument("--panel-id", default=None,
                   help="panel of cells scored; default = the name of --backtest-root")
    p.add_argument("--panel-file", default=None)
    args = p.parse_args(argv)

    root = args.backtest_root
    baselines = None
    if args.baselines:
        baselines = [x.strip() for x in args.baselines.split(",") if x.strip()]
    panel_id = args.panel_id or root.name
    all_es = []
    for s in [x.strip() for x in args.splits.split(",") if x.strip()]:
        pred_path = root / s / "predictions.parquet"
        if not pred_path.exists():
            logger.warning("skip %s: no %s", s, pred_path)
            continue
        es, per_id = analyze_split(pred_path, n_boot=args.n_boot, n_perm=args.n_perm,
                                   seed=args.seed, focal=args.focal, baselines=baselines)
        es.insert(0, "split", s)
        effect_sizes_path = root / s / "effect_sizes.csv"
        es.to_csv(effect_sizes_path, index=False)
        _plots(pred_path, per_id, root / s, s, focal=args.focal)
        all_es.append(es)
        logger.info("[%s] effect sizes:\n%s", s, es.to_string(index=False))

        # Provenance is recorded for the focal method only: every row in this
        # file is a comparison focal-vs-baseline, so the number being reported
        # is fundamentally about the focal method's performance. Baselines'
        # own provenance is recorded where their predictions actually come
        # from (HPC_code_tunning.backtest / experiments.timesfm.merge_predictions).
        method = focal_provenance_method_name(args.focal, args.timesfm_variant)
        if method is None:
            logger.warning(
                "[%s] focal='timesfm' sin --timesfm-variant; se omite el registro de "
                "proveniencia porque no se puede identificar la variante", s,
            )
        else:
            prov.record_metric_provenance(
                build_row_provenance(
                    method, split=s, cells=int(len(per_id)), bead_id=args.bead_id,
                    panel_id=panel_id, panel_file=args.panel_file,
                    output_files=(str(effect_sizes_path), str(root / "effect_sizes_all.csv")),
                    notes="; ".join(filter(None, [
                        f"backtest_root={Path(args.backtest_root).resolve()}",
                        f"cells={int(len(per_id))}",
                        f"n_boot={args.n_boot}; n_perm={args.n_perm}; seed={args.seed}",
                        args.notes])),
                    **({"manifest_ref": args.manifest_ref} if args.manifest_ref else {}),
                )
            )

    if all_es:
        combined = pd.concat(all_es, ignore_index=True)
        combined.to_csv(root / "effect_sizes_all.csv", index=False)
        metrics_all_path = root / "metrics_all.csv"
        if metrics_all_path.exists():
            lead_methods = (
                [x.strip() for x in args.lead_time_methods.split(",") if x.strip()]
                if args.lead_time_methods
                else [args.focal]
            )
            lead_time_plot(pd.read_csv(metrics_all_path), root / "lead_time_curve.png",
                           methods=lead_methods)
        logger.info("EFFECT SIZES (all splits):\n%s", combined.to_string(index=False))
        logger.info("wrote %s", root / "effect_sizes_all.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
