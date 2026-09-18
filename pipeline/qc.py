#!/usr/bin/env python3
"""
pipeline.qc

QC table per site x variable, read directly from ``Data/silver/{tmin,tmax,td}``
(before the ``pipeline.gold`` join), restricted to the frozen modeling range
2002-01-01..2016-12-31 (``docs/protocol/week1_manifest.yaml`` ``period.full_range``).

Silver's daily tables are already scoped to the 4 protocol departments (see
``tdew-ztn.2`` / ``pipeline.silver --departments``), so this reads
``Data/silver/department_grid_ids/{slug}.csv`` per site to know which ``ID``s
belong to it, then for each ``(site, var)`` accumulates, file by file (one
``{var}_daily_{year}_{month:02d}.parquet`` at a time, so nothing beyond a
single month x site needs to fit in memory):

- ``missing_pct``: share of expected ``(ID, date)`` pairs (site's cell count x
  every calendar day in range) that never appear in the raw table.
- ``duplicate_rows``: rows minus distinct ``(ID, date)`` pairs (duplicates can
  only occur within a single monthly file, since files partition the date
  range, so summing per-file duplicate counts is exact).
- ``missing_calendar_days``: calendar days in range with zero rows for that
  (site, var) at all — a cheap, exact way to catch whole missing months.

Alignment across the three series is then a per-site comparison of which
calendar days each variable actually covers (a set of at most ~5478 dates per
series — cheap to diff exactly): ``misaligned_days`` counts dates covered by
at least one of the three series but not all three, within 2002-2016.

Output
------
``Data/qc/qc_table.csv`` — one row per (site, variable), plus one
``alignment`` row per site.

Usage
-----
python -m pipeline.qc
python -m pipeline.qc --silver-dir Data/silver --out Data/qc/qc_table.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SILVER_DIR = REPO_ROOT / "Data" / "silver"
DEFAULT_OUT = REPO_ROOT / "Data" / "qc" / "qc_table.csv"

FULL_RANGE_START = pd.Timestamp("2002-01-01")
FULL_RANGE_END = pd.Timestamp("2016-12-31")
VARS = ("tmin", "tmax", "td")

# docs/protocol/week1_manifest.yaml sites.departments[].grid_ids_file basenames
SITES = ("lima", "cusco", "iquitos_loreto", "tarapoto_san_martin")


def load_site_ids(silver_dir: Path, site: str) -> pd.Index:
    path = silver_dir / "department_grid_ids" / f"{site}.csv"
    if not path.exists():
        raise FileNotFoundError(f"Department grid-id file not found: {path}")
    return pd.Index(pd.read_csv(path)["ID"].to_numpy())


def var_files_in_range(silver_dir: Path, var: str) -> list[Path]:
    var_dir = silver_dir / var
    if not var_dir.exists():
        return []
    files = []
    for f in sorted(var_dir.glob(f"{var}_daily_*.parquet")):
        # filenames: {var}_daily_{year}_{month:02d}.parquet
        try:
            year = int(f.stem.split("_")[-2])
        except (IndexError, ValueError):
            continue
        if FULL_RANGE_START.year <= year <= FULL_RANGE_END.year:
            files.append(f)
    return files


def qc_for_site_var(silver_dir: Path, site: str, var: str, site_ids: pd.Index) -> tuple[dict, set]:
    expected_days = int((FULL_RANGE_END - FULL_RANGE_START).days) + 1
    n_cells = len(site_ids)
    expected_pairs = expected_days * n_cells

    total_rows = 0
    distinct_pairs = 0
    dates_present: set[pd.Timestamp] = set()

    for f in var_files_in_range(silver_dir, var):
        df = pd.read_parquet(f, columns=["ID", "date"])
        df = df[df["ID"].isin(site_ids)]
        df = df[(df["date"] >= FULL_RANGE_START) & (df["date"] <= FULL_RANGE_END)]
        if df.empty:
            continue
        total_rows += len(df)
        distinct_pairs += len(df.drop_duplicates(subset=["ID", "date"]))
        dates_present.update(pd.DatetimeIndex(df["date"].unique()))

    missing_pairs = max(expected_pairs - distinct_pairs, 0)
    row = {
        "site": site,
        "variable": var,
        "n_cells": n_cells,
        "expected_days": expected_days,
        "expected_pairs": expected_pairs,
        "observed_pairs": distinct_pairs,
        "missing_pairs": missing_pairs,
        "missing_pct": round(100 * missing_pairs / expected_pairs, 4) if expected_pairs else float("nan"),
        "total_rows": total_rows,
        "duplicate_rows": max(total_rows - distinct_pairs, 0),
        "distinct_days_present": len(dates_present),
        "missing_calendar_days": expected_days - len(dates_present),
    }
    return row, dates_present


def build_qc_table(silver_dir: Path) -> pd.DataFrame:
    rows = []
    for site in SITES:
        site_ids = load_site_ids(silver_dir, site)
        dates_by_var = {}
        for var in VARS:
            row, dates_present = qc_for_site_var(silver_dir, site, var, site_ids)
            rows.append(row)
            dates_by_var[var] = dates_present

        all_dates = set().union(*dates_by_var.values()) if dates_by_var else set()
        misaligned = {d for d in all_dates if not all(d in dates_by_var[var] for var in VARS)}
        rows.append(
            {
                "site": site,
                "variable": "alignment(tmin,tmax,td)",
                "n_cells": len(site_ids),
                "expected_days": int((FULL_RANGE_END - FULL_RANGE_START).days) + 1,
                "expected_pairs": None,
                "observed_pairs": None,
                "missing_pairs": None,
                "missing_pct": None,
                "total_rows": None,
                "duplicate_rows": None,
                "distinct_days_present": len(all_dates),
                "missing_calendar_days": len(misaligned),
            }
        )
    return pd.DataFrame(rows)


def run(silver_dir: Path, out_path: Path) -> Path:
    table = build_qc_table(silver_dir)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(out_path, index=False)
    print(f"[qc] wrote {out_path} ({len(table)} rows)")
    return out_path


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="QC table per site x variable (missing, duplicates, alignment).")
    p.add_argument("--silver-dir", type=Path, default=DEFAULT_SILVER_DIR)
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    run(args.silver_dir, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
