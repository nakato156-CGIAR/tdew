"""Desglose A1 (tdew-03g): RMSE por metodo, anio, zona SENAMHI y ambito (panel o solo Peru).

Para los bloques ll4 (test 2013-2016) y ll4b (test 2009-2012) sobre las 17.027 celdas de
``reports/timesfm_benchmark/panels/nacional_17027.csv``:

(a) RMSE agregado, sesgo y RMSE por anio de cada metodo disponible;
(b) lo mismo restringido a las celdas dentro del Peru, con la misma mascara que dio
    8.272 dentro / 8.755 fuera (``experiments.timesfm.artifact_data.peru_mask``:
    ``shapely.contains_xy`` contra la union de los contornos departamentales);
(c) RMSE macro por zona (promedio simple del RMSE de cada zona) y numero de zonas en
    que cada metodo gana a cada otro;
(d) IC 95 % de brechas pareadas RMSE(A) - RMSE(B) por bootstrap de bloques espaciales
    de 2 grados y de bloques mes-anio (2000 replicas, semilla 0).

Todos los metodos se evaluan sobre las mismas filas (interseccion de ID y FECHA). Los
metodos opcionales (``tuned`` sin rezagos de Td, TimesFM ``tmin_anom_med`` con contexto
desde 2002, LLR simple y con rezagos con ``h`` y anio de inicio del ajuste elegidos por
validacion interna, ``llr_simple_sel`` y ``llr_rezagos_sel``, de ``15_llr_seleccion.sh``)
entran solos si su parquet existe, de modo que basta re-ejecutar el script cuando aparezcan.

Uso: ``uv run python -m experiments.amenazas.desglose [--splits ll4 ll4b]``
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
import pandas as pd

from experiments.timesfm import paths

logger = logging.getLogger("amenazas.desglose")

WORK = paths.WORK
RES = paths.RES
PANEL = Path("reports/timesfm_benchmark/panels/nacional_17027.csv")
OUT = Path("reports/paper_nuevo/resultados")
N_BOOT = 2000
SEED = 0
BLOCK_DEG = 2.0
N_PERU = 8272
TRAIN_END = {"ll4": 2012, "ll4b": 2008}

# Etiqueta -> (ruta por split, columna de prediccion). Orden = orden en las tablas.
def method_sources(split: str) -> dict[str, tuple[Path, str]]:
    tuned = {"ll4": RES / "tuning/backtest_clean/ll4/predictions.parquet",
             "ll4b": WORK / "tuning_ll4b/ll4b/predictions.parquet"}[split]
    tfm_dir = WORK / ("preds_nacional" if split == "ll4" else f"preds_nacional_{split}")
    return {
        "clim": (WORK / f"llr_simple/{split}__llr_simple.parquet", "pred_clim"),
        "tuned": (tuned, "pred_tuned"),
        "tuned_sin_td": (WORK / f"tuning_sin_td_{split}/{split}/predictions.parquet", "pred_tuned"),
        "llr_simple": (WORK / f"llr_simple/{split}__llr_simple.parquet", "pred_llr_simple"),
        "llr_rezagos": (WORK / f"llr_simple/{split}__llr_tmin_lags.parquet", "pred_llr_tmin_lags"),
        "llr_simple_sel": (WORK / f"llr_simple/{split}__llr_simple_sel.parquet", "pred_llr_simple_sel"),
        "llr_rezagos_sel": (WORK / f"llr_simple/{split}__llr_tmin_lags_sel.parquet", "pred_llr_tmin_lags_sel"),
        "timesfm_td": (tfm_dir / f"{split}__tmin_td_full.parquet", "pred"),
        "timesfm_anom": (tfm_dir / f"{split}__tmin_anom_full.parquet", "pred"),
        "timesfm_anom_med": (WORK / f"preds_nacional_med/{split}__tmin_anom_med.parquet", "pred"),
    }


# Brechas clave RMSE(A) - RMSE(B): negativo favorece a A. Solo se calculan si ambos existen.
KEY_GAPS: tuple[tuple[str, str], ...] = (
    ("timesfm_anom", "llr_rezagos"),
    ("timesfm_anom", "llr_simple"),
    ("timesfm_anom", "tuned"),
    ("tuned", "llr_simple"),
    ("tuned", "llr_rezagos"),
    ("timesfm_td", "llr_simple"),
    ("tuned", "tuned_sin_td"),
    ("tuned_sin_td", "llr_simple"),
    ("timesfm_anom", "tuned_sin_td"),
    ("timesfm_anom_med", "timesfm_anom"),
    ("timesfm_anom_med", "llr_rezagos"),
    ("timesfm_anom", "llr_rezagos_sel"),
    ("timesfm_anom", "llr_simple_sel"),
    ("llr_rezagos_sel", "llr_rezagos"),
    ("llr_simple_sel", "llr_simple"),
)


def peru_cells(ids: np.ndarray) -> np.ndarray:
    """True para las celdas dentro del Peru, con la mascara de ``artifact_data``."""
    from experiments.timesfm.artifact_data import peru_mask

    return peru_mask()[np.asarray(ids, dtype=np.int64)]


def load_split(split: str, panel: Path = PANEL) -> tuple[pd.DataFrame, list[str], dict[str, str]]:
    """Tabla alineada (ID, FECHA, TD_obs, una columna por metodo) sobre filas comunes."""
    ids = pd.read_csv(panel)["ID"].to_numpy(np.int64)
    sources = method_sources(split)
    base_path = sources["llr_simple"][0]
    df = pd.read_parquet(base_path, columns=["ID", "FECHA", "TD_obs", "pred_clim", "pred_llr_simple"])
    df = df[df.ID.isin(ids)].sort_values(["ID", "FECHA"], ignore_index=True)
    df = df.rename(columns={"pred_clim": "clim", "pred_llr_simple": "llr_simple"})
    used = {"clim": str(base_path), "llr_simple": str(base_path)}
    for name, (path, col) in sources.items():
        if name in used:
            continue
        if not path.exists():
            logger.info("%s %s: no existe %s, se omite", split, name, path)
            continue
        p = pd.read_parquet(path, columns=["ID", "FECHA", col]).rename(columns={col: name})
        p = p[p.ID.isin(ids)].sort_values(["ID", "FECHA"], ignore_index=True)
        if len(p) == len(df) and np.array_equal(p.ID.to_numpy(), df.ID.to_numpy()) \
                and np.array_equal(p.FECHA.to_numpy(), df.FECHA.to_numpy()):
            df[name] = p[name].to_numpy()
        else:
            n0 = len(df)
            df = df.merge(p, on=["ID", "FECHA"], how="inner")
            logger.warning("%s %s: filas no alineadas, inner join %d -> %d", split, name, n0, len(df))
        used[name] = str(path)
    methods = [m for m in sources if m in df]
    ok = df[["TD_obs", *methods]].notna().all(axis=1)
    if not ok.all():
        logger.warning("%s: se descartan %d filas con NaN", split, int((~ok).sum()))
        df = df[ok].reset_index(drop=True)
    zones = pd.read_parquet(RES / "zone_table.parquet", columns=["ID", "zone_id", "zone_label", "lon", "lat"])
    df = df.merge(zones, on="ID", how="left")
    df["peru"] = peru_cells(df.ID.to_numpy())
    df["year"] = df.FECHA.dt.year.astype(np.int16)
    df["month"] = df.FECHA.dt.month.astype(np.int8)
    return df, methods, used


def squared_errors(df: pd.DataFrame, methods: Sequence[str]) -> pd.DataFrame:
    o = df.TD_obs.to_numpy("f8")
    return pd.DataFrame({m: (df[m].to_numpy("f8") - o) ** 2 for m in methods}, index=df.index)


def per_method(df: pd.DataFrame, methods: Sequence[str]) -> pd.DataFrame:
    """RMSE, sesgo y n por metodo, total y por anio."""
    o = df.TD_obs.to_numpy("f8")
    rows = []
    for period, idx in [("total", np.ones(len(df), bool))] + [
            (str(y), (df.year == y).to_numpy()) for y in sorted(df.year.unique())]:
        for m in methods:
            e = df[m].to_numpy("f8")[idx] - o[idx]
            rows.append({"metodo": m, "periodo": period, "n": int(idx.sum()),
                         "celdas": int(df.ID[idx].nunique()),
                         "rmse": float(np.sqrt(np.mean(e ** 2))), "sesgo": float(e.mean()),
                         "mae": float(np.mean(np.abs(e)))})
    return pd.DataFrame(rows)


def per_zone(df: pd.DataFrame, se: pd.DataFrame, methods: Sequence[str]) -> pd.DataFrame:
    g = se.groupby(df.zone_id.to_numpy())
    rmse = g.mean().pow(0.5)
    meta = df.groupby("zone_id").agg(zone_label=("zone_label", "first"), celdas=("ID", "nunique"),
                                     n=("ID", "size"))
    out = rmse.join(meta).reset_index(names="zone_id")
    return out.melt(id_vars=["zone_id", "zone_label", "celdas", "n"], value_vars=list(methods),
                    var_name="metodo", value_name="rmse")


def zone_wins(zone_long: pd.DataFrame, methods: Sequence[str]) -> pd.DataFrame:
    """Numero de zonas en que A tiene RMSE estrictamente menor que B."""
    wide = zone_long.pivot(index="zone_id", columns="metodo", values="rmse")
    rows = []
    for a in methods:
        for b in methods:
            if a != b:
                rows.append({"metodo_a": a, "metodo_b": b, "zonas": len(wide),
                             "zonas_a_gana": int((wide[a] < wide[b]).sum())})
    return pd.DataFrame(rows)


def block_bootstrap(n: np.ndarray, sums: dict[str, np.ndarray], pairs: Iterable[tuple[str, str]],
                    n_boot: int = N_BOOT, seed: int = SEED) -> pd.DataFrame:
    """IC por remuestreo de bloques: ``n`` filas y suma de errores cuadraticos por bloque.

    Todas las parejas usan las mismas replicas (mismos bloques sorteados), lo que hace
    pareada la comparacion. Devuelve brecha puntual RMSE(A) - RMSE(B) y percentiles.
    """
    k = len(n)
    rng = np.random.default_rng(seed)
    draws = rng.integers(0, k, size=(n_boot, k))
    w = np.zeros((n_boot, k))
    np.add.at(w, (np.repeat(np.arange(n_boot), k), draws.ravel()), 1.0)
    big_n = w @ n
    rows = []
    for a, b in pairs:
        point = np.sqrt(sums[a].sum() / n.sum()) - np.sqrt(sums[b].sum() / n.sum())
        rep = np.sqrt((w @ sums[a]) / big_n) - np.sqrt((w @ sums[b]) / big_n)
        lo, hi = np.percentile(rep, [2.5, 97.5])
        rows.append({"metodo_a": a, "metodo_b": b, "bloques": k, "brecha": float(point),
                     "ic_lo": float(lo), "ic_hi": float(hi),
                     "bloques_a_gana": int((sums[a] < sums[b]).sum())})
    return pd.DataFrame(rows)


def block_keys(df: pd.DataFrame, scheme: str) -> np.ndarray:
    if scheme == "espacial_2g":
        bx = np.floor(df.lon.to_numpy() / BLOCK_DEG).astype(np.int64)
        by = np.floor(df.lat.to_numpy() / BLOCK_DEG).astype(np.int64)
        return (bx + 1000) * 10000 + (by + 1000)
    if scheme == "mes_anio":
        return df.year.to_numpy(np.int64) * 100 + df.month.to_numpy(np.int64)
    raise ValueError(scheme)


def gaps(df: pd.DataFrame, se: pd.DataFrame, methods: Sequence[str]) -> pd.DataFrame:
    pairs = [(a, b) for a, b in KEY_GAPS if a in methods and b in methods]
    out = []
    for scheme in ("espacial_2g", "mes_anio"):
        key = block_keys(df, scheme)
        g = se.groupby(key)
        n = g.size().to_numpy("f8")
        sums = {m: g[m].sum().to_numpy("f8") for m in methods}
        out.append(block_bootstrap(n, sums, pairs).assign(esquema=scheme))
    return pd.concat(out, ignore_index=True)


def run(splits: Sequence[str], out: Path = OUT) -> dict[str, pd.DataFrame]:
    out.mkdir(parents=True, exist_ok=True)
    tabs: dict[str, list[pd.DataFrame]] = {"metodo": [], "zona": [], "victorias": [], "brechas": []}
    inputs: dict[str, dict[str, str]] = {}
    for split in splits:
        df, methods, used = load_split(split)
        inputs[split] = used
        logger.info("%s: %d filas, %d celdas, metodos %s", split, len(df), df.ID.nunique(), methods)
        for ambito, sub in (("panel", df), ("peru", df[df.peru].reset_index(drop=True))):
            se = squared_errors(sub, methods)
            tag = {"split": split, "ambito": ambito}
            pm = per_method(sub, methods)
            zl = per_zone(sub, se, methods)
            macro = zl.groupby("metodo").rmse.mean().rename("rmse_macro_zona")
            pm = pm.merge(macro, left_on="metodo", right_index=True, how="left")
            pm.loc[pm.periodo != "total", "rmse_macro_zona"] = np.nan
            pm["zonas"] = zl.zone_id.nunique()
            tabs["metodo"].append(pm.assign(**tag))
            tabs["zona"].append(zl.assign(**tag))
            tabs["victorias"].append(zone_wins(zl, methods).assign(**tag))
            tabs["brechas"].append(gaps(sub, se, methods).assign(**tag))
        del df
    result = {k: pd.concat(v, ignore_index=True) for k, v in tabs.items()}
    front = ["split", "ambito"]
    files = {"metodo": "a1_por_metodo.csv", "zona": "a1_por_zona.csv",
             "victorias": "a1_victorias_zona.csv", "brechas": "a1_brechas.csv"}
    for k, name in files.items():
        t = result[k]
        t = t[front + [c for c in t.columns if c not in front]]
        t.to_csv(out / name, index=False, float_format="%.5f")
        result[k] = t
    write_provenance([str(out / n) for n in files.values()], inputs, splits)
    write_tables_md(result, out / "a1_desglose.md")
    return result


MD_START, MD_END = "<!-- tablas:inicio -->", "<!-- tablas:fin -->"


def _f(x: float, sign: bool = False) -> str:
    return (f"{x:+.3f}" if sign else f"{x:.3f}").replace(".", ",").replace("-", "−")


def tables_md(result: dict[str, pd.DataFrame]) -> str:
    """Tablas en Markdown generadas desde los CSV (se regeneran en cada corrida)."""
    m, b, v = result["metodo"], result["brechas"], result["victorias"]
    amb_txt = {"panel": "panel (17.027)", "peru": "Perú (8.272)"}
    lines = []
    for sp in dict.fromkeys(m.split):
        t = m[m.split == sp]
        years = sorted(p for p in t.periodo.unique() if p != "total")
        lines += [f"### RMSE y sesgo por método, bloque `{sp}` (°C)", "",
                  "| método | ámbito | RMSE | sesgo | RMSE macro por zona | " + " | ".join(years) + " |",
                  "|---|---|---|---|---|" + "---|" * len(years)]
        for amb in ("panel", "peru"):
            for me in dict.fromkeys(t.metodo):
                r = t[(t.ambito == amb) & (t.metodo == me)].set_index("periodo")
                lines.append(f"| {me} | {amb_txt[amb]} | {_f(r.rmse['total'])} | {_f(r.sesgo['total'], True)} | "
                             f"{_f(r.rmse_macro_zona['total'])} | " + " | ".join(_f(r.rmse[y]) for y in years) + " |")
        lines.append("")
    lines += ["### Brechas pareadas RMSE(A) − RMSE(B) con IC 95 % (°C; negativo favorece a A)", "",
              "| bloque | ámbito | A − B | brecha | IC bloques espaciales 2° | IC bloques mes-año |",
              "|---|---|---|---|---|---|"]
    for (sp, amb, a, bb), g in b.groupby(["split", "ambito", "metodo_a", "metodo_b"], sort=False):
        e = g.set_index("esquema")
        lines.append(f"| {sp} | {amb_txt[amb]} | {a} − {bb} | {_f(e.brecha.iloc[0], True)} | "
                     f"[{_f(e.ic_lo['espacial_2g'], True)}; {_f(e.ic_hi['espacial_2g'], True)}] | "
                     f"[{_f(e.ic_lo['mes_anio'], True)}; {_f(e.ic_hi['mes_anio'], True)}] |")
    lines.append("")
    for (sp, amb), t in v.groupby(["split", "ambito"], sort=False):
        ms = list(dict.fromkeys(t.metodo_a))
        lines += [f"### Zonas en que el método de la fila gana al de la columna, `{sp}`, {amb_txt[amb]} "
                  f"({int(t.zonas.iloc[0])} zonas)", "",
                  "| A \\ B | " + " | ".join(ms) + " |", "|---|" + "---|" * len(ms)]
        for a in ms:
            cells = ["—" if a == bb else str(int(t[(t.metodo_a == a) & (t.metodo_b == bb)].zonas_a_gana.iloc[0]))
                     for bb in ms]
            lines.append(f"| {a} | " + " | ".join(cells) + " |")
        lines.append("")
    return "\n".join(lines)


def write_tables_md(result: dict[str, pd.DataFrame], path: Path) -> None:
    """Reemplaza el bloque de tablas entre marcadores y deja intacto el texto escrito a mano."""
    block = f"{MD_START}\n{tables_md(result)}\n{MD_END}"
    if path.exists() and MD_START in (text := path.read_text()) and MD_END in text:
        head, rest = text.split(MD_START, 1)
        text = head + block + rest.split(MD_END, 1)[1]
    else:
        text = f"# A1: desglose de la comparación\n\n{block}\n"
    path.write_text(text)


def write_provenance(output_files: list[str], inputs: dict, splits: Sequence[str]) -> None:
    from tdew_estimation import provenance as prov

    notes = ("Entrenamiento 1981 hasta el anio previo al bloque de prueba de cada split "
             f"({ {s: TRAIN_END[s] for s in splits} }); autoregressive=True porque incluye tuned. "
             "Comparacion A1 sobre filas comunes a todos los metodos; mascara Peru = "
             "experiments.timesfm.artifact_data.peru_mask (shapely.contains_xy, "
             f"{N_PERU} celdas dentro); bootstrap {N_BOOT} replicas semilla {SEED}, bloques "
             f"espaciales de {BLOCK_DEG:g} grados y mes-anio. Entradas: {inputs}")
    record = prov.MetricProvenance(
        run_id=prov.new_run_id(), generated_at=prov.now_iso(), git_commit=prov.git_commit(),
        bead_id="tdew-03g", manifest_ref="docs/protocol/timesfm_manifest.yaml",
        model_family="comparison", model_id="multi", variant_label="a1_desglose",
        trained=True, training_period=("1981-01-01", f"{max(TRAIN_END[s] for s in splits)}-12-31"),
        validation_period=None,
        test_period=(f"{min(TRAIN_END[s] for s in splits) + 1}-01-01",
                     f"{max(TRAIN_END[s] for s in splits) + 4}-12-31"),
        split_id=",".join(splits), autoregressive=True, target_type="td_raw",
        climatology_used=True, climatology_role="baseline_and_anomaly_reference",
        inputs=tuple(sorted({m for d in inputs.values() for m in d})),
        panel_id="nacional_17027", panel_cell_count=17027, panel_file=str(PANEL),
        output_files=tuple(output_files), seeds=(SEED,), notes=notes,
    )
    prov.record_metric_provenance(record)


def main(argv: Sequence[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--splits", nargs="+", default=["ll4", "ll4b"])
    ap.add_argument("--out", type=Path, default=OUT)
    a = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(message)s")
    run(a.splits, a.out)


if __name__ == "__main__":
    main()
