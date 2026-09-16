#!/usr/bin/env python3
"""
pipeline.bronze

Bronze layer: land the raw data as-is. This only unpacks archives that arrive
zipped (e.g. ``spatial_covariables.zip``) and writes a flat inventory of what
ended up under ``Data/bronze`` — no parsing, cleaning, or reshaping. Safe to
re-run; existing extractions are skipped unless ``--overwrite`` is passed.

Usage
-----
python -m pipeline.bronze
python -m pipeline.bronze --bronze-dir Data/bronze --overwrite
"""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BRONZE_DIR = REPO_ROOT / "Data" / "bronze"
INVENTORY_FILE = "_inventory.csv"


def unzip_archives(bronze_dir: Path, *, overwrite: bool = False) -> list[Path]:
    """Extract every ``*.zip`` under ``bronze_dir`` into a sibling folder named
    after the archive's stem. Returns the list of extraction folders (new or
    already-present)."""
    extracted: list[Path] = []
    for zpath in sorted(bronze_dir.rglob("*.zip")):
        target = zpath.with_suffix("")
        if target.exists() and not overwrite:
            print(f"[bronze] {target.relative_to(bronze_dir)} already extracted, skip")
            extracted.append(target)
            continue
        target.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zpath) as zf:
            zf.extractall(target)
        print(f"[bronze] extracted {zpath.name} -> {target.relative_to(bronze_dir)}")
        extracted.append(target)
    return extracted


def build_inventory(bronze_dir: Path) -> pd.DataFrame:
    """Flat listing of every raw file under ``bronze_dir`` (archives excluded)."""
    rows = []
    for p in sorted(bronze_dir.rglob("*")):
        if not p.is_file() or p.suffix.lower() == ".zip" or p.name == INVENTORY_FILE:
            continue
        stat = p.stat()
        rows.append(
            {
                "relative_path": str(p.relative_to(bronze_dir)),
                "suffix": p.suffix.lower(),
                "size_bytes": stat.st_size,
                "modified": pd.Timestamp(stat.st_mtime, unit="s"),
            }
        )
    return pd.DataFrame(rows).sort_values("relative_path").reset_index(drop=True)


def run(bronze_dir: Path, *, overwrite: bool = False) -> Path:
    if not bronze_dir.exists():
        raise FileNotFoundError(f"Bronze dir not found: {bronze_dir}")
    unzip_archives(bronze_dir, overwrite=overwrite)
    inventory = build_inventory(bronze_dir)
    out_path = bronze_dir / INVENTORY_FILE
    inventory.to_csv(out_path, index=False)
    print(f"[bronze] wrote inventory ({len(inventory)} files) -> {out_path}")
    return out_path


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Bronze layer: unpack archives + inventory raw files.")
    p.add_argument("--bronze-dir", type=Path, default=DEFAULT_BRONZE_DIR)
    p.add_argument("--overwrite", action="store_true", help="Re-extract archives even if the target folder exists.")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    run(args.bronze_dir, overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
