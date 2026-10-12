"""Reconstruye los seis paneles de celdas del benchmark TimesFM y los compara con los publicados.

Los paneles se armaron durante el benchmark con fragmentos sueltos que no quedaron en el
repositorio. Este script reproduce cada uno desde sus fuentes con la misma regla y la misma
semilla, y verifica que el resultado sea identico al archivo que usaron las corridas:

| panel | celdas | regla |
|---|---|---|
| ``nacional_17041.csv`` | 17.041 | celdas de ``$RES/tuning/backtest/ll4`` (run con fuga, 64 buckets) |
| ``nacional_17027.csv`` | 17.027 | celdas de ``$RES/tuning/backtest_clean/ll4`` (run limpio) |
| ``cribado_estratificado.csv`` | 1.106 | hasta 40 por zona sobre ``nacional_17041``, ``default_rng(20260922)`` |
| ``ll4_reducido_512.csv`` | 2.048 | panel ``dev_a`` de la reconstruccion: 512 por departamento, ``seed=0`` |
| ``panel_436k.csv`` | 436.519 | union de ``Data/silver/department_grid_ids/*.csv`` |
| ``panel_escala_submuestra.csv`` | 61.113 | 14 % redondeado de cada departamento, ``default_rng(20260922)`` |

Uso::

    uv run python -m experiments.timesfm.scripts.make_panels --out-dir /tmp/panels --check
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from experiments.timesfm import paths

SITES = ("cusco", "iquitos_loreto", "lima", "tarapoto_san_martin")
PANEL_SEED = 20260922
CRIBADO_PER_ZONE = 40
ESCALA_FRACTION = 0.14
REPORT_PANELS = Path("reports/timesfm_benchmark/panels")

PUBLISHED = {
    "nacional_17041.csv": REPORT_PANELS / "nacional_17041.csv",
    "nacional_17027.csv": REPORT_PANELS / "nacional_17027.csv",
    "cribado_estratificado.csv": REPORT_PANELS / "cribado_estratificado.csv",
    "ll4_reducido_512.csv": paths.RECONSTRUCTION_WORK / "panels" / "ll4_reducido_512.csv",
    "panel_436k.csv": paths.WORK / "panel_436k.csv",
    "panel_escala_submuestra.csv": paths.WORK / "panel_escala_submuestra.csv",
}


def backtest_panel(predictions: Path) -> pd.DataFrame:
    """``ID`` y ``zone_id`` de un ``predictions.parquet`` del backtest de Palacios."""
    cells = pd.read_parquet(predictions, columns=["ID", "zone_id"]).drop_duplicates()
    return cells.sort_values("ID").reset_index(drop=True)


def cribado(nacional: pd.DataFrame) -> pd.DataFrame:
    """Hasta 40 celdas por zona SENAMHI, en orden de ``zone_id``, sin reemplazo."""
    rng = np.random.default_rng(PANEL_SEED)
    picks = []
    for _, group in nacional.groupby("zone_id", sort=True):
        ids = group["ID"].to_numpy()
        picks.append(group[group["ID"].isin(rng.choice(ids, min(CRIBADO_PER_ZONE, len(ids)), replace=False))])
    return pd.concat(picks).sort_values(["zone_id", "ID"]).reset_index(drop=True)


def departamental(silver: Path) -> pd.DataFrame:
    """Panel ``dev_a`` de la reconstruccion: 512 celdas por departamento, estratificadas."""
    from experiments.reconstruction.bucketed import select_panel

    return select_panel(silver, "dev_a", seed=0)


def escala(silver: Path) -> pd.DataFrame:
    ids = pd.concat([pd.read_csv(silver / "department_grid_ids" / f"{s}.csv")[["ID"]] for s in SITES])
    return ids.drop_duplicates().sort_values("ID").reset_index(drop=True)


def escala_submuestra(silver: Path) -> pd.DataFrame:
    """14 % de cada departamento, proporcional, para el rival ``tuned`` de la prueba de escala."""
    rng = np.random.default_rng(PANEL_SEED)
    picks = []
    for site in SITES:
        ids = pd.read_csv(silver / "department_grid_ids" / f"{site}.csv")["ID"].to_numpy()
        picks.append(rng.choice(ids, int(round(ESCALA_FRACTION * len(ids))), replace=False))
    return pd.DataFrame({"ID": np.sort(np.concatenate(picks))})


def build(res: Path, silver: Path) -> dict[str, pd.DataFrame]:
    nacional = backtest_panel(res / "tuning" / "backtest" / "ll4" / "predictions.parquet")
    return {
        "nacional_17041.csv": nacional,
        "nacional_17027.csv": backtest_panel(res / "tuning" / "backtest_clean" / "ll4" / "predictions.parquet"),
        "cribado_estratificado.csv": cribado(nacional),
        "ll4_reducido_512.csv": departamental(silver),
        "panel_436k.csv": escala(silver),
        "panel_escala_submuestra.csv": escala_submuestra(silver),
    }


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--res", type=Path, default=paths.RES)
    parser.add_argument("--silver", type=Path, default=Path("Data/silver"))
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--check", action="store_true",
                        help="compara cada panel con el archivo que usaron las corridas (mismas celdas)")
    args = parser.parse_args(argv)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    failures = 0
    for name, frame in build(args.res, args.silver).items():
        out = args.out_dir / name
        frame.to_csv(out, index=False)
        line = f"{name:30s} {len(frame):>8,d} celdas  sha256 {_sha256(out)[:16]}"
        if args.check:
            published = PUBLISHED[name]
            if not published.exists():
                line += f"  (sin archivo publicado en {published})"
            else:
                same = set(pd.read_csv(published)["ID"]) == set(frame["ID"])
                line += "  igual al publicado" if same else f"  DISTINTO de {published}"
                failures += not same
        print(line)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
