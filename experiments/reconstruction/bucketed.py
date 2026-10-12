"""Bucketed source adapter for the continuous reconstruction protocol.

The adapter intentionally separates two disk-heavy operations:

1. ``materialize_silver_buckets`` scans each monthly silver TMIN/TMAX file
   once and writes hive-style ID buckets.
2. ``build_canonical_buckets`` joins one historical bucket at a time with the
   matching silver buckets and small spatial lookups.

Neither function runs at import time.  The next session can invoke the CLI
after checking paths and storage capacity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Iterable, Iterator, Sequence

import pandas as pd

from pipeline.qc import SITES
from tdew_estimation.bucket_layout import discover_bucket_ids

from .data import audit_sources, canonicalize_columns, select_spatial_panel
from .protocol import protocol_spec

SITE_LABELS = {
    "lima": "Lima",
    "cusco": "Cusco",
    "iquitos_loreto": "Loreto",
    "tarapoto_san_martin": "San Martin",
}
SITE_REGIONS = {
    "lima": "Costa",
    "cusco": "Sierra",
    "iquitos_loreto": "Selva",
    "tarapoto_san_martin": "Selva",
}


def bucket_path(root: Path, bucket_id: int) -> Path:
    """Resolve padded or unpadded hive partition names."""
    candidates = (root / f"id_bucket={bucket_id}", root / f"id_bucket={bucket_id:04d}")
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def read_bucket(root: Path, bucket_id: int, *, columns: Sequence[str] | None = None) -> pd.DataFrame:
    path = bucket_path(Path(root), bucket_id)
    if not path.exists():
        return pd.DataFrame(columns=list(columns or ()))
    # Bucket directories also hold the per-bucket audit sidecar, so the parquet
    # files are listed explicitly instead of handing the directory to pyarrow.
    sources = sorted(path.glob("*.parquet")) if path.is_dir() else [path]
    if not sources:
        return pd.DataFrame(columns=list(columns or ()))
    frame = pd.read_parquet(sources, columns=list(columns) if columns else None)
    # Passing explicit paths makes pyarrow infer the hive key as a column; the
    # bucket id is already known by the caller and must not reach the join.
    return frame.drop(columns="id_bucket", errors="ignore")


def iter_canonical_buckets(
    root: Path,
    *,
    bucket_ids: Sequence[int] | None = None,
    columns: Sequence[str] | None = None,
) -> Iterator[tuple[int, pd.DataFrame]]:
    ids = list(bucket_ids) if bucket_ids is not None else discover_bucket_ids(root)
    for bucket_id in ids:
        frame = read_bucket(root, bucket_id, columns=columns)
        if not frame.empty:
            yield bucket_id, canonicalize_columns(frame)


def load_canonical_input(path: Path, *, ids: Iterable[int] | None = None) -> pd.DataFrame:
    """Read a canonical parquet file or bucket root, optionally filtering IDs."""
    path = Path(path)
    selected = None if ids is None else pd.Index([int(value) for value in ids])
    if path.is_file():
        frame = pd.read_parquet(path)
        if selected is not None:
            frame = frame[frame["ID"].isin(selected)]
        return canonicalize_columns(frame).sort_values(["ID", "date"]).reset_index(drop=True)
    if not path.is_dir():
        raise FileNotFoundError(path)
    pieces = []
    bucket_ids = None
    manifest_path = path / "manifest.json"
    if selected is not None and manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        num_buckets = int(manifest["num_buckets"])
        available = {int(item["bucket_id"]) for item in manifest.get("buckets", [])}
        bucket_ids = sorted({int(value) % num_buckets for value in selected} & available)
    for _, frame in iter_canonical_buckets(path, bucket_ids=bucket_ids):
        if selected is not None:
            frame = frame[frame["ID"].isin(selected)]
        if not frame.empty:
            pieces.append(frame)
    if not pieces:
        raise ValueError(f"No canonical rows found under {path}")
    return pd.concat(pieces, ignore_index=True).sort_values(["ID", "date"]).reset_index(drop=True)


def materialize_silver_buckets(
    silver_dir: Path,
    output_root: Path,
    *,
    num_buckets: int,
    variables: Sequence[str] = ("tmin", "tmax"),
    selected_ids: pd.Index | None = None,
    overwrite: bool = False,
    months_per_part: int = 12,
) -> Path:
    """Scan every monthly silver file once and partition it by ``ID % N``.

    Monthly files are grouped into parts of ``months_per_part`` before being
    written. One parquet per month and bucket would mean close to two million
    files for a panel spread over 8192 buckets; the group size trades that
    file count against the rows held in memory while a part is built.
    """
    silver_dir, output_root = Path(silver_dir), Path(output_root)
    if months_per_part < 1:
        raise ValueError("months_per_part must be at least 1")
    if output_root.exists() and overwrite:
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    for variable in variables:
        source_files = sorted((silver_dir / variable).glob(f"{variable}_daily_*.parquet"))
        if not source_files:
            raise FileNotFoundError(f"No {variable} monthly parquet files under {silver_dir / variable}")
        variable_root = output_root / variable
        for start in range(0, len(source_files), months_per_part):
            part_files = source_files[start : start + months_per_part]
            part_name = f"{part_files[0].stem}__{part_files[-1].stem}"
            marker = variable_root / ".done" / f"{part_name}.json"
            if marker.exists() and not overwrite:
                continue
            pieces = []
            for source in part_files:
                frame = pd.read_parquet(source, columns=["ID", "date", "value"])
                if selected_ids is not None:
                    frame = frame[frame["ID"].isin(selected_ids)]
                if not frame.empty:
                    pieces.append(frame)
            marker.parent.mkdir(parents=True, exist_ok=True)
            if not pieces:
                marker.write_text(json.dumps({"sources": [f.name for f in part_files], "rows": 0}))
                continue
            frame = pd.concat(pieces, ignore_index=True).rename(columns={"value": variable.upper()})
            frame["id_bucket"] = (frame["ID"].astype("int64") % int(num_buckets)).astype("int32")
            for bucket_id, part in frame.groupby("id_bucket", sort=True):
                target_dir = variable_root / f"id_bucket={int(bucket_id)}"
                target_dir.mkdir(parents=True, exist_ok=True)
                part.drop(columns="id_bucket").to_parquet(target_dir / f"{part_name}.parquet", index=False)
            marker.write_text(json.dumps({"sources": [f.name for f in part_files], "rows": len(frame)}))
    (output_root / "manifest.json").write_text(
        json.dumps({"num_buckets": int(num_buckets), "variables": list(variables)}, indent=2, sort_keys=True)
    )
    return output_root


def department_lookup(silver_dir: Path) -> pd.DataFrame:
    rows = []
    for site in SITES:
        path = Path(silver_dir) / "department_grid_ids" / f"{site}.csv"
        if not path.exists():
            raise FileNotFoundError(path)
        frame = pd.read_csv(path, usecols=["ID"])
        frame["department"] = SITE_LABELS[site]
        frame["region"] = SITE_REGIONS[site]
        rows.append(frame)
    result = pd.concat(rows, ignore_index=True)
    if result["ID"].duplicated().any():
        raise ValueError("At least one ID belongs to more than one protocol department")
    return result


def prepare_spatial(
    silver_dir: Path, *, selected_ids: pd.Index | None = None
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Build the per-cell lookup and its monthly LST normals once.

    Both tables are restricted to the cells that will actually be joined, so
    the per-bucket merge does not scan the whole grid or the 33.8 million rows
    of ``lst_normals.parquet`` for every bucket.
    """
    silver_dir = Path(silver_dir)
    departments = department_lookup(silver_dir)
    if selected_ids is not None:
        departments = departments[departments["ID"].isin(selected_ids)]
        if departments.empty:
            raise ValueError("The requested panel has no cell in the protocol departments")
    grid = canonicalize_columns(pd.read_parquet(silver_dir / "grid_index.parquet"))
    static = canonicalize_columns(pd.read_parquet(silver_dir / "static_covariates.parquet"))
    static_columns = [column for column in ("ID", "DEM", "TDI") if column in static]
    spatial = grid[grid["ID"].isin(departments["ID"])].merge(
        static[static_columns], on="ID", how="left", validate="one_to_one"
    )
    spatial = spatial.merge(departments, on="ID", how="inner", validate="one_to_one")
    lst = pd.read_parquet(silver_dir / "lst_normals.parquet")
    lst = lst[lst["ID"].isin(spatial["ID"])]
    return spatial, lst


def build_canonical_bucket(
    bucket_id: int,
    *,
    historical_root: Path,
    silver_bucket_root: Path,
    spatial: pd.DataFrame,
    lst: pd.DataFrame,
    num_buckets: int,
) -> tuple[pd.DataFrame, dict[str, object]]:
    historical = canonicalize_columns(read_bucket(historical_root, bucket_id))
    if historical.empty:
        return historical, {"bucket_id": bucket_id, "rows": 0}
    required = {"ID", "date", "TD", "TMIN"}
    missing = required - set(historical)
    if missing:
        raise ValueError(f"Historical bucket {bucket_id} lacks {sorted(missing)}")
    historical["date"] = pd.to_datetime(historical["date"])
    # The silver side is rebucketed with ``num_buckets``. If that modulus does
    # not reproduce the historical partition, the per-bucket join would keep
    # only the IDs the two layouts happen to share instead of failing.
    residues = historical["ID"].astype("int64") % int(num_buckets)
    if not bool((residues == int(bucket_id)).all()):
        raise ValueError(
            f"Historical bucket {bucket_id} was not written with {num_buckets} buckets; "
            "rebucket silver with the historical bucket count"
        )
    historical = historical[["ID", "date", "TD", "TMIN"]].drop_duplicates(["ID", "date"])
    historical = historical[historical["ID"].isin(pd.Index(spatial["ID"]))]
    if historical.empty:
        return historical, {"bucket_id": bucket_id, "rows": 0}

    tmin = read_bucket(Path(silver_bucket_root) / "tmin", bucket_id)
    tmax = read_bucket(Path(silver_bucket_root) / "tmax", bucket_id)
    if tmin.empty or tmax.empty:
        raise ValueError(f"Silver TMIN/TMAX bucket {bucket_id} is empty")
    silver = tmin.merge(tmax, on=["ID", "date"], how="outer", validate="one_to_one")
    silver["date"] = pd.to_datetime(silver["date"])
    ids = pd.Index(historical["ID"].unique())
    silver = silver[silver["ID"].isin(ids)]
    silver = silver.merge(spatial, on="ID", how="inner", validate="many_to_one")
    silver["month"] = silver["date"].dt.month
    silver = silver.merge(lst, on=["ID", "month"], how="left", validate="many_to_one")
    audit = audit_sources(historical, silver)
    canonical = silver.merge(
        historical[["ID", "date", "TD"]], on=["ID", "date"], how="left", validate="one_to_one"
    )
    canonical = canonical.sort_values(["ID", "date"]).reset_index(drop=True)
    metadata = {
        "bucket_id": bucket_id,
        "rows": len(canonical),
        "n_ids": audit.n_ids,
        "coordinate_hash": audit.coordinate_hash,
        "tmin_parity_max_c": audit.max_tmin_difference,
    }
    return canonical, metadata


def build_canonical_buckets(
    historical_root: Path,
    silver_bucket_root: Path,
    silver_dir: Path,
    output_root: Path,
    *,
    overwrite: bool = False,
    max_buckets: int | None = None,
    selected_ids: pd.Index | None = None,
) -> Path:
    """Join and audit historical/silver sources one ID bucket at a time."""
    historical_root = Path(historical_root)
    silver_dir, output_root = Path(silver_dir), Path(output_root)
    spatial, lst = prepare_spatial(silver_dir, selected_ids=selected_ids)
    available = discover_bucket_ids(historical_root)
    silver_manifest = Path(silver_bucket_root) / "manifest.json"
    if not silver_manifest.exists():
        raise FileNotFoundError(f"Missing silver bucket manifest: {silver_manifest}")
    num_buckets = int(json.loads(silver_manifest.read_text())["num_buckets"])
    if available and max(available) >= num_buckets:
        raise ValueError("Historical and silver bucket counts are incompatible")
    if len(available) > num_buckets:
        raise ValueError(
            f"{historical_root} holds {len(available)} buckets but silver was rebucketed with {num_buckets}"
        )
    # Only the buckets that hold a requested cell are opened. A 2,048-cell
    # panel touches at most 2,048 of the 8,192 historical buckets.
    wanted = {int(value) % num_buckets for value in spatial["ID"]}
    bucket_ids = [bucket_id for bucket_id in available if bucket_id in wanted]
    if max_buckets is not None:
        bucket_ids = bucket_ids[:max_buckets]
    manifest = []
    for bucket_id in bucket_ids:
        target = output_root / f"id_bucket={bucket_id}" / "part.parquet"
        metadata_path = target.with_suffix(".json")
        if target.exists() and not overwrite:
            manifest.append(json.loads(metadata_path.read_text()) if metadata_path.exists() else {"bucket_id": bucket_id})
            continue
        canonical, metadata = build_canonical_bucket(
            bucket_id,
            historical_root=historical_root,
            silver_bucket_root=silver_bucket_root,
            spatial=spatial,
            lst=lst,
            num_buckets=num_buckets,
        )
        if canonical.empty:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        canonical.to_parquet(target, index=False)
        metadata["sha256"] = _file_sha256(target)
        metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True))
        manifest.append(metadata)
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "manifest.json").write_text(
        json.dumps({"num_buckets": num_buckets, "buckets": manifest}, indent=2, sort_keys=True)
    )
    return output_root


def select_panel(silver_dir: Path, protocol: str, *, seed: int = 0) -> pd.DataFrame:
    """Pick the deterministic panel frozen by a protocol."""
    spatial, _ = prepare_spatial(Path(silver_dir))
    requested = protocol_spec(protocol).panel_cells_per_department
    return spatial if requested is None else select_spatial_panel(spatial, requested, seed=seed)


def read_panel_ids(path: Path | None) -> pd.Index | None:
    if path is None:
        return None
    return pd.Index(pd.read_csv(path)["ID"].astype("int64").unique())


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Preparacion bucketed para reconstruccion continua de Td")
    sub = parser.add_subparsers(dest="command", required=True)
    panel = sub.add_parser("select-panel")
    panel.add_argument("--silver-dir", type=Path, required=True)
    panel.add_argument("--protocol", required=True)
    panel.add_argument("--output", type=Path, required=True)
    panel.add_argument("--seed", type=int, default=0)
    rebucket = sub.add_parser("rebucket-silver")
    rebucket.add_argument("--silver-dir", type=Path, required=True)
    rebucket.add_argument("--output", type=Path, required=True)
    rebucket.add_argument("--num-buckets", type=int, required=True)
    rebucket.add_argument("--panel-ids", type=Path, help="CSV con columna ID; por defecto, todas las celdas")
    rebucket.add_argument("--months-per-part", type=int, default=12)
    rebucket.add_argument("--overwrite", action="store_true")
    canonical = sub.add_parser("build-canonical")
    canonical.add_argument("--historical-root", type=Path, required=True)
    canonical.add_argument("--silver-bucket-root", type=Path, required=True)
    canonical.add_argument("--silver-dir", type=Path, required=True)
    canonical.add_argument("--output", type=Path, required=True)
    canonical.add_argument("--panel-ids", type=Path)
    canonical.add_argument("--max-buckets", type=int)
    canonical.add_argument("--overwrite", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "select-panel":
        panel = select_panel(args.silver_dir, args.protocol, seed=args.seed)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        panel.to_csv(args.output, index=False)
        print(f"{len(panel)} celdas -> {args.output}")
    elif args.command == "rebucket-silver":
        selected = read_panel_ids(args.panel_ids)
        if selected is None:
            selected = pd.Index(department_lookup(args.silver_dir)["ID"])
        materialize_silver_buckets(
            args.silver_dir, args.output, num_buckets=args.num_buckets,
            selected_ids=selected, overwrite=args.overwrite,
            months_per_part=args.months_per_part,
        )
    else:
        build_canonical_buckets(
            args.historical_root, args.silver_bucket_root, args.silver_dir,
            args.output, overwrite=args.overwrite, max_buckets=args.max_buckets,
            selected_ids=read_panel_ids(args.panel_ids),
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
