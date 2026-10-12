#!/usr/bin/env python3
"""
experiments.baselines.plot_leaderboard

Renders ``reports/week1_baselines/leaderboard.csv`` (produced by
``experiments.baselines.train_baselines``) as a grouped bar chart of
``skill_vs_clim`` (test split) per site and method — the headline comparison
for the tdew-x46 baseline ladder. See
``reports/week1_baselines/TRACEABILITY.md`` for what protocol/data this reads.

Colors: fixed per-method assignment (never re-cycled) from the Okabe-Ito
colorblind-safe categorical palette, since this is a static report image
(this workstation has no browser — see the ``workstation-ssh-headless``
memory — so an interactive HTML chart is not the right deliverable here).

Usage
-----
uv run python -m experiments.baselines.plot_leaderboard
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LEADERBOARD = REPO_ROOT / "reports" / "week1_baselines" / "leaderboard.csv"
DEFAULT_OUT = REPO_ROOT / "reports" / "week1_baselines" / "skill_vs_climatology.png"

# docs/protocol/week1_manifest.yaml sites.departments order; ALL = pooled.
SITE_ORDER = ["lima", "cusco", "iquitos_loreto", "tarapoto_san_martin", "ALL"]
SITE_LABELS = {
    "lima": "Lima\n(Costa)",
    "cusco": "Cusco\n(Sierra)",
    "iquitos_loreto": "Loreto/Iquitos\n(Selva)",
    "tarapoto_san_martin": "San Martín/\nTarapoto (Selva)",
    "ALL": "ALL\n(pooled)",
}
# climatology is excluded (skill_vs_clim == 0 by definition, it's the reference line).
METHOD_ORDER = ["persistence", "dept_ols", "dept_mlr", "generalist_mlr"]
METHOD_LABELS = {
    "persistence": "persistence",
    "dept_ols": "dept_ols",
    "dept_mlr": "dept_mlr",
    "generalist_mlr": "generalist_mlr",
}
# Okabe-Ito colorblind-safe categorical palette, one fixed hue per method.
METHOD_COLORS = {
    "persistence": "#E69F00",
    "dept_ols": "#56B4E9",
    "dept_mlr": "#009E73",
    "generalist_mlr": "#CC79A7",
}


def plot(leaderboard: pd.DataFrame, *, split: str = "test") -> plt.Figure:
    df = leaderboard[leaderboard["split"] == split]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    n_methods = len(METHOD_ORDER)
    bar_width = 0.8 / n_methods
    x = np.arange(len(SITE_ORDER))

    for i, method in enumerate(METHOD_ORDER):
        vals = [
            df[(df["site"] == site) & (df["method"] == method)]["skill_vs_clim"].squeeze() for site in SITE_ORDER
        ]
        offset = (i - (n_methods - 1) / 2) * bar_width
        ax.bar(
            x + offset,
            vals,
            width=bar_width,
            color=METHOD_COLORS[method],
            label=METHOD_LABELS[method],
        )

    ax.axhline(0.0, color="#4d4d4d", linewidth=1)
    ax.text(
        len(SITE_ORDER) - 0.5,
        0.01,
        "climatology (referencia, skill=0)",
        ha="right",
        va="bottom",
        fontsize=8,
        color="#4d4d4d",
    )

    ax.set_xticks(x)
    ax.set_xticklabels([SITE_LABELS[s] for s in SITE_ORDER])
    ax.set_ylabel("skill_vs_clim = 1 − RMSE_método / RMSE_climatología  (test, 2015–2016)")
    ax.set_title("tdew-x46 — baselines vs. climatología, por sitio (Semana 1, protocolo congelado)")
    ax.grid(axis="y", color="#e0e0e0", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper left", ncols=n_methods, frameon=False, bbox_to_anchor=(0, 1.12))

    fig.tight_layout()
    return fig


def run(leaderboard_path: Path, out_path: Path, *, split: str = "test") -> Path:
    leaderboard = pd.read_csv(leaderboard_path)
    fig = plot(leaderboard, split=split)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    print(f"[plot_leaderboard] wrote {out_path}")
    return out_path


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Plot the tdew-x46 baseline leaderboard (skill_vs_clim by site/method).")
    p.add_argument("--leaderboard", type=Path, default=DEFAULT_LEADERBOARD)
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    p.add_argument("--split", type=str, default="test", choices=["validation", "test"])
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    run(args.leaderboard, args.out, split=args.split)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
