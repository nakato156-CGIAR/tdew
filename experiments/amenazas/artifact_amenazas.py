"""Datos de la seccion de amenazas A1-A4 del artefacto TimesFM (``datos_amenazas.js``).

Lee los CSV de ``reports/paper_nuevo/resultados/`` (A1, escalera de contexto, A3 y A4) y
escribe ``reports/timesfm_benchmark/artifact/datos_amenazas.js`` con ``window.AMENAZAS``. La
pagina no recalcula nada: toda cifra de la seccion sale de este archivo.

A3 (control de Tmin barajada, bead ``tdew-077``) no tenia CSV: su script de evaluacion
(``experiments.timesfm.control_tmin_barajada_eval``) solo imprime. ``--capturar-a3`` lo
ejecuta, analiza su salida y escribe ``a3_control_tmin_barajada.csv`` con su registro de
proveniencia; hace falta acceso a las predicciones en ``$TDEW_TIMESFM_WORK``.

Uso::

    uv run python -m experiments.amenazas.artifact_amenazas --capturar-a3   # una vez
    uv run python -m experiments.amenazas.artifact_amenazas
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

import pandas as pd

RES = Path("reports/paper_nuevo/resultados")
OUT = Path("reports/timesfm_benchmark/artifact/datos_amenazas.js")
A3_CSV = RES / "a3_control_tmin_barajada.csv"
A3_MODULE = "experiments.timesfm.control_tmin_barajada_eval"
A3_PANEL = Path("reports/timesfm_benchmark/panels/cribado_estratificado.csv")

# Archivo de origen -> clave en window.AMENAZAS. El filtro por fila, si lo hay, se aplica
# antes de exportar; la prueba lo reproduce para comparar cifra por cifra.
FUENTES = {
    "porMetodo": ("a1_por_metodo.csv", None),
    "brechas": ("a1_brechas.csv", None),
    "victorias": ("a1_victorias_zona.csv", None),
    "escalera": ("a1_escalera_contexto.csv", None),
    "escaleraBrechas": ("a1_escalera_contexto_brechas.csv", None),
    "a4PorAnio": ("a4_por_anio.csv", ("muestra", "con_reanalisis")),
    "a4PorPeriodo": ("a4_por_periodo.csv", ("muestra", "con_reanalisis")),
    "a4Delta": ("a4_delta_rmse_bootstrap.csv", ("muestra", "con_reanalisis")),
    "a3": ("a3_control_tmin_barajada.csv", None),
}

# Que informacion recibe cada metodo (descripcion del protocolo, no un resultado).
INFORMACION = [
    {"metodo": "timesfm_anom", "grupo": "b", "tmin_dia": "sí",
     "tmin_otros": "todo el contexto y el horizonte", "td": "sí", "zona": "no"},
    {"metodo": "llr_simple", "grupo": "a", "tmin_dia": "sí", "tmin_otros": "no",
     "td": "no", "zona": "no"},
    {"metodo": "llr_rezagos_sel", "grupo": "a", "tmin_dia": "sí", "tmin_otros": "rezagos {lags}",
     "td": "no", "zona": "no"},
    {"metodo": "tuned", "grupo": "b", "tmin_dia": "sí", "tmin_otros": "rezagos de Tmin",
     "td": "rezagos de Td con recursión", "zona": "sí"},
    {"metodo": "tuned_sin_td", "grupo": "a", "tmin_dia": "sí", "tmin_otros": "rezagos de Tmin",
     "td": "no", "zona": "sí"},
]

_LINEA_A3 = re.compile(r"^(\S+)\s+rmse\s+([\d.]+)\s+skill\s+([+-][\d.]+)\s+bias\s+([+-][\d.]+)\s*$")
_CELDAS_A3 = re.compile(r"^celdas\s+(\d+)\s+filas\s+(\d+)\s*$")


def _registros(frame: pd.DataFrame) -> list[dict]:
    out = []
    for row in frame.to_dict(orient="records"):
        out.append({k: (None if isinstance(v, float) and pd.isna(v) else v) for k, v in row.items()})
    return out


def leer(clave: str, res: Path = RES) -> pd.DataFrame:
    nombre, filtro = FUENTES[clave]
    frame = pd.read_csv(res / nombre)
    if filtro:
        frame = frame[frame[filtro[0]] == filtro[1]].reset_index(drop=True)
    return frame


def meta() -> dict:
    from experiments.amenazas.desglose import BLOCK_DEG, N_BOOT
    from experiments.amenazas.escalera_contexto import CLIM_START, STARTS
    from experiments.llr_simple.llr import (
        H_GRID_SEL,
        TRAIN_START_GRID,
        VALIDATION_YEARS,
    )
    from experiments.llr_simple.llr_lags import DEFAULT_LAGS
    from experiments.timesfm.panel import SPLITS

    return {
        "bloques": {s: {"contextoFin": SPLITS[s][0], "prueba": list(SPLITS[s][1])} for s in ("ll4", "ll4b")},
        "real": {"prueba": list(SPLITS["real"][1])},
        "rezagos": list(DEFAULT_LAGS),
        "aniosValidacion": VALIDATION_YEARS,
        "hSel": list(H_GRID_SEL),
        "inicioSel": list(TRAIN_START_GRID),
        "escaleraInicios": list(STARTS),
        "escaleraClimInicio": CLIM_START,
        "bootstrap": N_BOOT,
        "bloqueGrados": BLOCK_DEG,
    }


def payload(res: Path = RES) -> dict:
    datos = {"meta": meta()}
    lags = ", ".join(str(x) for x in datos["meta"]["rezagos"][:-1]) + f" y {datos['meta']['rezagos'][-1]}"
    datos["informacion"] = [{**r, "tmin_otros": r["tmin_otros"].format(lags=lags)} for r in INFORMACION]
    for clave in FUENTES:
        datos[clave] = _registros(leer(clave, res))
    return datos


def build(out: Path = OUT, res: Path = RES) -> dict:
    datos = payload(res)
    body = json.dumps(datos, ensure_ascii=False, separators=(",", ":"))
    out.write_text(f"window.AMENAZAS = {body};\n", encoding="utf-8")
    return datos


def parse_a3(texto: str) -> pd.DataFrame:
    """Convierte la salida de ``control_tmin_barajada_eval`` en una tabla."""
    celdas = filas = None
    rows = []
    for linea in texto.splitlines():
        m = _CELDAS_A3.match(linea.strip())
        if m:
            celdas, filas = int(m.group(1)), int(m.group(2))
            continue
        m = _LINEA_A3.match(linea.strip())
        if not m:
            continue
        tag = m.group(1)
        if tag == "pred_clim":
            metodo, variante, tmin, modo, semilla = "clim", None, None, None, None
        elif tag == "pred_tuned":
            metodo, variante, tmin, modo, semilla = "tuned", None, "real", None, None
        elif tag.startswith("real_"):
            metodo, variante, tmin, modo, semilla = "timesfm", tag.removeprefix("real_"), "real", None, None
        elif tag.startswith("shuf_"):
            _, variante, modo, sem = tag.split("_")
            metodo, tmin, semilla = "timesfm", "barajada", int(sem.removeprefix("s"))
        else:
            raise ValueError(f"etiqueta desconocida en la salida de A3: {tag}")
        rows.append({"corrida": tag, "metodo": metodo, "variante": variante, "tmin": tmin,
                     "modo": modo, "semilla": semilla, "rmse": float(m.group(2)),
                     "skill": float(m.group(3)), "sesgo": float(m.group(4))})
    if celdas is None or not rows:
        raise ValueError("la salida de A3 no tiene la linea de celdas o ninguna corrida")
    frame = pd.DataFrame(rows)
    frame.insert(6, "celdas", celdas)
    frame.insert(7, "filas", filas)
    frame["semilla"] = frame["semilla"].astype("Int64")
    return frame


def capturar_a3(out: Path = A3_CSV) -> pd.DataFrame:
    texto = subprocess.run([sys.executable, "-m", A3_MODULE], check=True, capture_output=True,
                           text=True).stdout
    frame = parse_a3(texto)
    frame.to_csv(out, index=False)
    _provenance_a3(out, frame)
    return frame


def _provenance_a3(out: Path, frame: pd.DataFrame) -> None:
    from experiments.timesfm.panel import SPLITS
    from tdew_estimation import provenance as prov

    train_end, (t0, t1) = SPLITS["ll4"]
    notes = (f"Control negativo A3 (tdew-077): salida de `uv run python -m {A3_MODULE}` capturada por "
             "experiments.amenazas.artifact_amenazas --capturar-a3, sin recalcular. TimesFM 3.0 zero-shot "
             "(trained=False en el modelo; la climatologia y tuned si usan 1981-train_end) con la Tmin del "
             "bloque oculto real o barajada entre anios (semillas) o entre celdas; filas comunes con el run "
             f"limpio de Palacios (ll4). Corridas: {list(frame.corrida)}")
    record = prov.MetricProvenance(
        run_id=prov.new_run_id(), generated_at=prov.now_iso(), git_commit=prov.git_commit(),
        bead_id="tdew-077", manifest_ref="docs/protocol/timesfm_manifest.yaml",
        model_family="comparison", model_id="multi", variant_label="a3_control_tmin_barajada",
        trained=True, training_period=("1981-01-01", f"{train_end}-12-31"), validation_period=None,
        test_period=(f"{t0}-01-01", f"{t1}-12-31"), split_id="ll4", autoregressive=True,
        target_type="td_raw", climatology_used=True, climatology_role="baseline_and_anomaly_reference",
        inputs=("TMIN", "TMIN_anom", "TD_anom_context", "doy"), panel_id="cribado_comun_tuned",
        panel_cell_count=int(frame.celdas.iloc[0]), panel_file=str(A3_PANEL),
        output_files=(str(out),), seeds=tuple(sorted(int(s) for s in frame.semilla.dropna().unique())),
        notes=notes,
    )
    prov.record_metric_provenance(record)


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--capturar-a3", action="store_true",
                    help="ejecuta el control de Tmin barajada y escribe a3_control_tmin_barajada.csv")
    a = ap.parse_args(argv)
    if a.capturar_a3:
        print(capturar_a3().to_string(index=False))
    datos = build(a.out)
    print(f"{a.out}: {a.out.stat().st_size} bytes, claves {list(datos)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
