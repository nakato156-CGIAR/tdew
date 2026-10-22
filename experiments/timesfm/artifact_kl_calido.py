"""Datos de la subseccion "Divergencia calida" del artefacto TimesFM (``datos_kl_calido.js``).

Lee los CSV de ``reports/timesfm_benchmark/kl_calido/`` (salida de
``experiments.timesfm.kl_calido``, bead ``tdew-214.19``) y escribe
``reports/timesfm_benchmark/artifact/datos_kl_calido.js`` con ``window.D_KLC``. La pagina no
recalcula nada: copia columnas de esos CSV redondeadas a 4 decimales (delta y share a 5) y
un control comprueba que el total nacional derivado de los cortes coincide con el
histograma nacional.

Uso::

    uv run python -m experiments.timesfm.artifact_kl_calido
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

import numpy as np
import pandas as pd

SRC = Path("reports/timesfm_benchmark/kl_calido")
OUT = Path("reports/timesfm_benchmark/artifact/datos_kl_calido.js")
MAX_BYTES = 200 * 1024

MODELOS = ("timesfm", "llr", "clim")
CI = ["delta_B_lo_espacial_2g", "delta_B_hi_espacial_2g", "delta_B_lo_mes_anio", "delta_B_hi_mes_anio"]
BASE = ["model", "n_cells", "n", "p_obs_B", "delta_B", "share_B", "delta_Bp", "share_Bp"]
# Archivo -> (clave en window.D_KLC, columnas de grupo, columnas extra)
CORTES = {
    "zona": ("zona", ["zone_id", "zone_label"], CI),
    "anio": ("anio", ["anio"], CI),
    "anio_mes": ("anioMes", ["anio", "mes"], []),
    "depto": ("depto", ["depto"], []),
    "dem": ("dem", ["dem_band"], []),
}
FINOS = {"delta_B", "share_B", "delta_Bp", "share_Bp", *CI}
DEPTO_NOMBRE = {"MADRE DE DIOS": "Madre de Dios", "SAN MARTIN": "San Martín", "JUNIN": "Junín",
                "HUANUCO": "Huánuco", "APURIMAC": "Apurímac", "LA LIBERTAD": "La Libertad",
                "fuera_peru": "Fuera del Perú"}


def _registros(frame: pd.DataFrame) -> list[dict]:
    out = []
    for row in frame.to_dict(orient="records"):
        r = {}
        for k, v in row.items():
            if isinstance(v, float):
                r[k] = None if np.isnan(v) else round(v, 5 if k in FINOS else 4)
            elif isinstance(v, (np.integer,)):
                r[k] = int(v)
            else:
                r[k] = v
        out.append(r)
    return out


def leer(nombre: str, src: Path = SRC) -> pd.DataFrame:
    _, grupo, extra = CORTES[nombre]
    frame = pd.read_csv(src / f"{nombre}.csv")
    frame = frame[frame.model.isin(MODELOS)]
    return frame[grupo + BASE + extra].reset_index(drop=True)


def nacional(src: Path = SRC) -> dict:
    """P_obs y Delta nacionales en B y B', ponderando por n el corte por anio (que parte las filas).

    B' = [24,5, 27] es cerrado arriba y no coincide con bins de 0,5 C, asi que no se toma del
    histograma; ``check_parity`` compara solo B contra ``hist_nacional.csv``.
    """
    a = pd.read_csv(src / "anio.csv")
    out = {}
    for m in MODELOS:
        s = a[a.model == m]
        n = float(s.n.sum())
        out.setdefault("n", int(n))
        out.setdefault("p_obs_B", round(float((s.n * s.p_obs_B).sum()) / n, 5))
        out.setdefault("p_obs_Bp", round(float((s.n * s.p_obs_Bp).sum()) / n, 5))
        out[m] = {"delta_B": round(float((s.n * s.delta_B).sum()) / n, 5),
                  "delta_Bp": round(float((s.n * s.delta_Bp).sum()) / n, 5)}
    return out


def _delta_b_hist(src: Path, m: str) -> float:
    from .kl_calido import B_HI, B_LO

    h = pd.read_csv(src / "hist_nacional.csv")
    en_b = (h.bin_lo >= B_LO - 1e-9) & (h.bin_hi <= B_HI + 1e-9)
    return float(h[m][en_b].sum() - h.obs[en_b].sum()) / float(h.obs.sum())


def meta(src: Path = SRC) -> dict:
    from .kl_calido import B_HI, B_LO, BP_HI, BP_LO, N_BOOT

    prov = json.loads((src / "zona.csv.provenance.json").read_text())
    return {"B": [B_LO, B_HI], "Bp": [BP_LO, BP_HI], "bootstrap": N_BOOT, "bead": prov.get("bead_id"),
            "celdas": int(prov.get("panel_cell_count")), "prueba": prov.get("test_period")}


def payload(src: Path = SRC) -> dict:
    datos = {"meta": meta(src), "nacional": nacional(src)}
    for nombre, (clave, _, _) in CORTES.items():
        frame = leer(nombre, src)
        if nombre == "depto":
            frame.insert(1, "nombre", [DEPTO_NOMBRE.get(d, str(d).title()) for d in frame.depto])
        datos[clave] = _registros(frame)
    check_parity(datos, src)
    return datos


def check_parity(datos: dict, src: Path = SRC) -> None:
    """El total nacional de cada corte (suma de n*delta / n) debe igualar al del histograma."""
    problemas = []
    for clave in ("zona", "anio", "anioMes", "depto", "dem"):
        frame = pd.DataFrame(datos[clave])
        for m in MODELOS:
            s = frame[frame.model == m]
            if s.empty:
                problemas.append(f"{clave}: sin filas de {m}")
                continue
            if int(s.n.sum()) != datos["nacional"]["n"]:
                problemas.append(f"{clave}/{m}: n {int(s.n.sum())} frente a {datos['nacional']['n']}")
            d = float((s.n * s.delta_B).sum() / s.n.sum())
            if abs(d - datos["nacional"][m]["delta_B"]) > 5e-5:
                problemas.append(f"{clave}/{m}: delta_B {d:.6f} frente a {datos['nacional'][m]['delta_B']:.6f}")
    for m in MODELOS:
        d = _delta_b_hist(src, m)
        if abs(d - datos["nacional"][m]["delta_B"]) > 5e-5:
            problemas.append(f"histograma/{m}: delta_B {d:.6f} frente a {datos['nacional'][m]['delta_B']:.6f}")
    if problemas:
        raise ValueError("paridad de kl_calido: " + "; ".join(problemas))


def build(out: Path = OUT, src: Path = SRC) -> dict:
    datos = payload(src)
    body = json.dumps(datos, ensure_ascii=False, separators=(",", ":"))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f"window.D_KLC = {body};\n", encoding="utf-8")
    if out.stat().st_size > MAX_BYTES:
        raise ValueError(f"{out} pesa {out.stat().st_size} bytes; el limite es {MAX_BYTES}")
    return datos


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--src", type=Path, default=SRC)
    a = ap.parse_args(argv)
    datos = build(a.out, a.src)
    print(f"{a.out}: {a.out.stat().st_size} bytes, claves {list(datos)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
