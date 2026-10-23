"""Costo de pared de llr_simple_sel y llr_rezagos_sel (tdew-4w2): construye r3_costo_llr_sel.csv.

Lee el log de la corrida cronometrada (``r3_costo_llr_sel.log``: marcas CARGA_INI/CARGA_FIN/
SELECCION_FIN/PROC_FIN de ``costo_llr_sel_wrap.py`` y bloques ``/usr/bin/time -v``), compara las
predicciones nuevas con las existentes y registra la proveniencia.
"""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
RES = REPO / "reports/paper_nuevo/resultados"
LOG = RES / "r3_costo_llr_sel.log"
OUT = RES / "r3_costo_llr_sel.csv"
WORK = Path("/home/cvelasquez/tdew_timesfm")
HARDWARE = "Intel Core i9-14900K (32 hilos), 125 GB RAM"
PANEL = "reports/timesfm_benchmark/panels/nacional_17027.csv"
COLS = ["metodo", "bloque", "etapa", "celdas", "segundos_pared", "celdas_por_s", "hardware", "gpu", "inicio",
        "fin", "fuente", "observaciones", "insumos_de_diseno", "reproduce_max_abs_diff"]
METHODS = {"simple": ("llr_simple_sel", "llr_simple_sel", "1 proceso (numpy)"),
           "lags": ("llr_rezagos_sel", "llr_tmin_lags_sel", "12 procesos, bloques de 1000 celdas")}


def ts(line: str) -> datetime:
    return datetime.strptime(line[:23], "%Y-%m-%d %H:%M:%S,%f")


def blocks(text: str):
    for m in re.finditer(r"^--- (\w+) (\w+)\n(.*?)(?=^--- |\nALLDONE)", text, re.S | re.M):
        yield m.group(1), m.group(2), m.group(3)


def main() -> None:
    rows = []
    for kind, split, body in blocks(LOG.read_text()):
        t = {k: ts(next(l for l in body.splitlines() if k in l)) for k in
             ("PROC_INI", "CARGA_INI", "CARGA_FIN", "SELECCION_FIN", "PROC_FIN")}
        cpu = re.search(r"Percent of CPU this job got: (\d+)%", body).group(1)
        rss = int(re.search(r"Maximum resident set size \(kbytes\): (\d+)", body).group(1)) / 1e6
        wall = re.search(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): ([\d:.]+)", body).group(1)
        up = re.findall(r"load average: ([\d, ]+)", body)
        sel = re.search(r"train_start=(\d+) h=(\d+)", body)
        name, stem, par = METHODS[kind]
        a = pd.read_parquet(WORK / f"llr_simple/{split}__{stem}.parquet")
        b = pd.read_parquet(WORK / f"costo_llr_sel/{split}__{stem}.parquet")
        pc = [c for c in a.columns if c.startswith("pred")] + ["TD_obs"]
        assert (a.ID.values == b.ID.values).all() and (a.FECHA.values == b.FECHA.values).all()
        diff = float(max(np.nanmax(np.abs(a[c].values - b[c].values)) for c in pc))
        stages = [("carga de datos", "CARGA_INI", "CARGA_FIN", "inicio del proceso hasta fin de la lectura; sin arranque de uv"),
                  ("seleccion conjunta de h y train_start (10 x 4 = 40 combinaciones)", "CARGA_FIN", "SELECCION_FIN",
                   f"{par}; validacion 4 anios finales"),
                  ("ajuste final + prediccion + escritura", "SELECCION_FIN", "PROC_FIN", "incluye parquet de 24.876.447 filas"),
                  ("total", "PROC_INI", "PROC_FIN", f"{wall} con /usr/bin/time (incluye arranque de uv); CPU promedio {cpu} %; "
                   f"pico RSS {rss:.1f} GB; carga del sistema al terminar {up[-1].strip()}")]
        for etapa, i, f, obs in stages:
            seg = (t[f] - t[i]).total_seconds()
            rows.append({"metodo": name, "bloque": split, "etapa": etapa, "celdas": 17027, "segundos_pared": round(seg, 1),
                         "celdas_por_s": "", "hardware": HARDWARE, "gpu": "no",
                         "inicio": t[i].strftime("%Y-%m-%d %H:%M:%S"), "fin": t[f].strftime("%Y-%m-%d %H:%M:%S"),
                         "fuente": "r3_costo_llr_sel.log", "observaciones": obs + (f"; elegido train_start={sel[1]}, h={sel[2]}" if etapa == "total" else ""),
                         "insumos_de_diseno": "grilla h 7-180 (10 valores) x train_start 1981/1986/1991/1996" if etapa.startswith("selec") else "",
                         "reproduce_max_abs_diff": diff})
    pd.DataFrame(rows, columns=COLS).to_csv(OUT, index=False)
    from tdew_estimation import provenance as prov
    rec = prov.MetricProvenance(
        run_id=prov.new_run_id(), generated_at=prov.now_iso(), git_commit=prov.git_commit(),
        bead_id="tdew-4w2", manifest_ref="docs/protocol/timesfm_manifest.yaml",
        model_family="llr", model_id="llr_simple_sel,llr_rezagos_sel", variant_label="r3_costo_llr_sel",
        trained=True, training_period=("1981-01-01", "2012-12-31"), validation_period=None,
        test_period=("2009-01-01", "2012-12-31"), split_id="ll4b,ll4", autoregressive=False, target_type="td_raw",
        climatology_used=True, climatology_role="baseline_and_anomaly_reference",
        inputs=("experiments.llr_simple.llr", "experiments.llr_simple.llr_lags"),
        panel_id="nacional_17027", panel_cell_count=17027, panel_file=PANEL,
        output_files=(str(OUT.relative_to(REPO)),), seeds=(),
        notes=("Tiempos de pared de 15_llr_seleccion.sh (mismos comandos, --workers 12 --chunk 1000) re-corridos el "
               "2026-10-23 en tmux con costo_llr_sel_wrap.py; salidas en $WORK/costo_llr_sel/ y comparadas fila a fila con "
               "$WORK/llr_simple/ (reproduce_max_abs_diff). Sin metricas de error; estacion compartida con otras sesiones "
               "(carga ~0,5-1 antes de iniciar)."))
    prov.record_metric_provenance(rec)
    print(pd.read_csv(OUT)[["metodo", "bloque", "etapa", "segundos_pared", "reproduce_max_abs_diff"]].to_string())


if __name__ == "__main__":
    main()
