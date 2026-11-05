"""Conteos anuales por celda para localizar la diferencia entre 20 y 24 °C."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from .kl_calido import (
    DEFAULT_GEO, DEFAULT_PALACIOS, DEFAULT_STATIC, DEFAULT_TFM,
    cell_table, load_pairs,
)
from .real_compare import DEFAULT_SUPPORT, DEFAULT_ZONE


def annual_counts(frame):
    """Una fila por celda–año; se conserva el mismo conjunto de pares para ambos modelos."""
    keys = ["ID", "year"]
    counts = frame[keys].copy()
    counts["n"] = 1
    for col in ("obs", "timesfm", "llr"):
        counts[col] = ((frame[col] >= 20) & (frame[col] < 24)).astype("int16")
    return counts.groupby(keys, sort=True).sum().reset_index()


def main():
    frame = load_pairs(DEFAULT_PALACIOS, DEFAULT_TFM)
    annual = annual_counts(frame)
    ids = np.sort(frame.ID.unique())
    cells = cell_table(ids, DEFAULT_ZONE, DEFAULT_SUPPORT, DEFAULT_STATIC, DEFAULT_GEO)
    # La zona numérica procede de las predicciones, como en el análisis original.
    cells = cells.merge(frame[["ID", "zone_id"]].drop_duplicates(), on="ID", validate="one_to_one")
    years = sorted(int(y) for y in annual.year.unique())
    del frame
    indexed = annual.set_index(["ID", "year"])
    rows = []
    for cell in cells.sort_values("ID").itertuples(index=False):
        a = indexed.loc[cell.ID].reindex(years)
        rows.append({
            "id": int(cell.ID), "lon": round(float(cell.lon), 5), "lat": round(float(cell.lat), 5),
            "depto": str(cell.depto), "zona": str(cell.zone_label), "zone_id": int(cell.zone_id),
            "n": [int(v) if np.isfinite(v) else 0 for v in a.n],
            **{col: [int(v) if np.isfinite(v) else 0 for v in a[col]]
               for col in ("obs", "timesfm", "llr")},
        })
    # Reproduce el corte anual existente antes de escribir el nuevo artifact.
    import pandas as pd
    reference = pd.read_csv("reports/timesfm_benchmark/kl_calido/anio.csv")
    for year in years:
        a = annual[annual.year == year]
        for model in ("timesfm", "llr"):
            measured = (a[model].sum() - a.obs.sum()) / a.n.sum()
            expected = reference[(reference.anio == year) & (reference.model == model)].iloc[0]
            # El CSV de referencia se escribió con float_format="%.6g".
            assert float(f"{measured:.6g}") == expected.delta_B, (year, model)
            assert int(a.n.sum()) == int(expected.n)
            assert int(a.obs.sum()) == int(expected.n_obs_B)
    # El artifact publicado se limita a las celdas dentro del territorio peruano.
    rows = [row for row in rows if row["depto"] != "fuera_peru"]
    cells = cells[cells.depto != "fuera_peru"]
    annual = annual[annual.ID.isin(cells.ID)]
    total_n = int(annual.n.sum())
    out = Path("reports/timesfm_benchmark/artifact/datos_kl_celdas.js")
    payload = {"years": years, "cells": rows, "outlines": json.loads(DEFAULT_GEO.read_text()),
               "meta": {"interval": [20, 24], "n": total_n, "bead": "tdew-6pe",
                        "palacios": str(DEFAULT_PALACIOS), "timesfm": str(DEFAULT_TFM),
                        "scope": "Perú",
                        "filter": "Solo Perú; mismos pares ID–FECHA con observación y ambos modelos presentes",
                        "criterion": "Menos valores en [20,24) que los observados; diferencia estrictamente negativa"}}
    out.write_text("window.D_KLC_CELLS=" + json.dumps(payload, ensure_ascii=False, separators=(",", ":"), allow_nan=False) + ";\n")
    csv = Path("reports/timesfm_benchmark/kl_calido/celda_anio.csv")
    annual.merge(cells[["ID", "lon", "lat", "depto", "zone_label"]], on="ID", validate="many_to_one").to_csv(csv, index=False)
    provenance = {**payload["meta"], "years": years, "cells": len(rows),
                  "counts": "n: pares válidos; obs/timesfm/llr: conteos en [20,24)",
                  "sources": [str(DEFAULT_PALACIOS), str(DEFAULT_TFM), str(DEFAULT_ZONE), str(DEFAULT_GEO)],
                  "validation": "Paridad de conteos y diferencias con anio.csv para los dos modelos y los cuatro años"}
    csv.with_suffix(".csv.provenance.json").write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n")
    print(f"Escritas {len(rows)} celdas, {len(annual)} filas anuales y {total_n} pares; paridad anual verificada.", flush=True)


if __name__ == "__main__":
    main()
