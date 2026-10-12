"""Publica un CSV intermedio (bajo ``$WORK``) en el repo con proveniencia propia.

``merge_predictions`` y ``effect_sizes`` escriben sus CSV fuera del repo. Para citar
una cifra desde ``reports/`` cada CSV publicado necesita filas del registro cuyo
``output_files`` lo nombren. Este modulo copia el archivo y clona, con ``run_id``
nuevo, cada fila que documentaba el original. El registro es de solo adicion.
"""
from __future__ import annotations

import argparse
import shutil
from dataclasses import fields
from pathlib import Path
from typing import Sequence

from tdew_estimation import provenance as prov


def _recorded_path(path: Path, repo_root: Path) -> str:
    """Ruta como se guarda en el registro: relativa al repo si esta bajo el, para que
    el registro sobreviva a un cambio de checkout o de worktree; absoluta si no."""
    resolved = Path(path).resolve()
    try:
        return str(resolved.relative_to(Path(repo_root).resolve()))
    except ValueError:
        return str(resolved)


def _clone(row: dict, *, output_file: str, source: Path) -> prov.MetricProvenance:
    names = {f.name for f in fields(prov.MetricProvenance)}
    data = {k: v for k, v in row.items() if k in names}
    for key in ("training_period", "validation_period", "test_period"):
        if data.get(key) is not None:
            data[key] = tuple(data[key])
    for key in ("inputs", "seeds"):
        data[key] = tuple(data.get(key) or ())
    link = f"published_from={source}; source_run_id={row['run_id']}"
    data.update(
        notes=f"{row['notes']}; {link}" if row.get("notes") else link,
        run_id=prov.new_run_id(),
        generated_at=prov.now_iso(),
        git_commit=prov.git_commit(),
        output_files=(output_file,),
    )
    return prov.MetricProvenance(**data)


def publish_csv(
    src: Path,
    dst: Path,
    *,
    registry_path: Path = prov.DEFAULT_REGISTRY_PATH,
    repo_root: Path = prov.REPO_ROOT,
) -> int:
    """Copia ``src`` a ``dst`` y devuelve cuantas filas de proveniencia se clonaron."""
    src, dst = Path(src), Path(dst)
    target, dst_resolved = src.resolve(), dst.resolve()
    registry = prov.load_registry(registry_path)

    def documents(row: dict, path: Path) -> bool:
        return any(
            prov.resolve_recorded_path(f, repo_root=repo_root) == path
            for f in row.get("output_files", [])
        )

    rows = [r for r in registry if documents(r, target)]
    if not rows:
        raise ValueError(f"{src} sin registros de proveniencia en {registry_path}")
    already = {
        part.split("=", 1)[1]
        for r in registry if documents(r, dst_resolved)
        for part in (r.get("notes") or "").split("; ") if part.startswith("source_run_id=")
    }
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    pending = [r for r in rows if r["run_id"] not in already]
    for row in pending:
        prov.record_metric_provenance(
            _clone(row, output_file=_recorded_path(dst, repo_root), source=src.resolve()),
            registry_path=registry_path, repo_root=repo_root,
        )
    return len(pending)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--src", type=Path, required=True, nargs="+")
    parser.add_argument("--dst-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    for src in args.src:
        n = publish_csv(src, args.dst_dir / src.name)
        print(f"{src} -> {args.dst_dir / src.name} ({n} registros)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
