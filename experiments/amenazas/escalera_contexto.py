"""Escalera de inicio del contexto (tdew-03g, A1): longitud del historial frente a regimen PISCO.

TimesFM ``tmin_anom_full`` con contexto desde 1981, 1986, 1991, 1996 y 2002 (climatologia de
las anomalias fija en 1981-train_end, ``13_escalera_contexto.sh``) y los dos LLR con los
mismos anios de inicio para los coeficientes y la eleccion de ``h`` (climatologia tambien
1981-train_end, ``14_escalera_llr.sh``). En ll4b se anade el control con contexto y
climatologia desde 2002 (el comportamiento de ``tmin_anom_med``).

Todo se evalua sobre las mismas filas ``(ID, FECHA)``: celdas del panel de cribado comunes con
``tuned`` (en ll4 el run limpio de Palacios, ``$RES/tuning/backtest_clean/ll4``; en ll4b
``$WORK/tuning_ll4b/ll4b``) e interseccion de todas las corridas. Salidas:

- ``a1_escalera_contexto.csv``: RMSE, sesgo y MAE por bloque, metodo, inicio y periodo
  (total y cada anio del bloque), con la diferencia frente al inicio 1981;
- ``a1_escalera_contexto_brechas.csv``: brechas pareadas RMSE(A) - RMSE(B) con IC 95 % por
  bootstrap de bloques mes-anio y espaciales de 2 grados (2000 replicas, semilla 0).

Uso: ``uv run python -m experiments.amenazas.escalera_contexto``
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd

from experiments.amenazas.desglose import BLOCK_DEG, N_BOOT, SEED, block_bootstrap, block_keys
from experiments.timesfm import paths
from experiments.timesfm.panel import SPLITS

logger = logging.getLogger("amenazas.escalera_contexto")

WORK = paths.WORK
RES = paths.RES
PANEL = Path("reports/timesfm_benchmark/panels/cribado_estratificado.csv")
OUT = Path("reports/paper_nuevo/resultados")
STARTS = (1981, 1986, 1991, 1996, 2002)
CLIM_START = 1981
TFM_DIR = WORK / "preds_cribado_escalera"
LLR_DIR = WORK / "llr_escalera"
METHODS = ("timesfm", "llr_simple", "llr_rezagos")
# Control de climatologia: (split, inicio de contexto, inicio de climatologia).
CONTROLS = (("ll4b", 2002, 2002),)


def tuned_path(split: str) -> Path:
    return {"ll4": RES / "tuning/backtest_clean/ll4/predictions.parquet",
            "ll4b": WORK / "tuning_ll4b/ll4b/predictions.parquet"}[split]


def sources(split: str) -> dict[str, tuple[Path, str]]:
    """Columna -> (parquet, columna de prediccion). Nombre de columna ``metodo@inicio``."""
    out: dict[str, tuple[Path, str]] = {}
    for s in STARTS:
        out[f"timesfm@{s}"] = (TFM_DIR / f"{split}__tmin_anom_full__ctx{s}__clim{CLIM_START}.parquet", "pred")
        out[f"llr_simple@{s}"] = (LLR_DIR / f"{split}__llr_simple__train{s}.parquet", "pred_llr_simple")
        out[f"llr_rezagos@{s}"] = (LLR_DIR / f"{split}__llr_tmin_lags__train{s}.parquet", "pred_llr_tmin_lags")
    for sp, ctx, clim in CONTROLS:
        if sp == split:
            out[f"timesfm_clim_propia@{ctx}"] = (
                TFM_DIR / f"{split}__tmin_anom_full__ctx{ctx}__clim{clim}.parquet", "pred")
    out["tuned@1981"] = (tuned_path(split), "pred_tuned")
    return out


def load_split(split: str, panel: Path = PANEL) -> tuple[pd.DataFrame, list[str], dict[str, str]]:
    """Tabla (ID, FECHA, TD_obs, clim, una columna por corrida) sobre las filas comunes."""
    ids = set(pd.read_csv(panel)["ID"].astype(np.int64))
    ref_ids = set(pd.read_parquet(tuned_path(split), columns=["ID"]).ID.unique().astype(np.int64))
    keep = np.array(sorted(ids & ref_ids), dtype=np.int64)
    logger.info("%s: %d celdas del panel, %d comunes con tuned", split, len(ids), keep.size)
    base = LLR_DIR / f"{split}__llr_simple__train{CLIM_START}.parquet"
    df = pd.read_parquet(base, columns=["ID", "FECHA", "TD_obs", "pred_clim"])
    df = df[df.ID.isin(keep)].rename(columns={"pred_clim": f"clim@{CLIM_START}"})
    used = {f"clim@{CLIM_START}": str(base)}
    for name, (path, col) in sources(split).items():
        if not path.exists():
            raise FileNotFoundError(f"{split} {name}: falta {path}")
        p = pd.read_parquet(path, columns=["ID", "FECHA", col]).rename(columns={col: name})
        n0 = len(df)
        df = df.merge(p[p.ID.isin(keep)], on=["ID", "FECHA"], how="inner")
        if len(df) != n0:
            logger.warning("%s %s: inner join %d -> %d filas", split, name, n0, len(df))
        used[name] = str(path)
    runs = [c for c in df.columns if "@" in c]
    ok = df[["TD_obs", *runs]].notna().all(axis=1)
    if not ok.all():
        logger.warning("%s: se descartan %d filas con NaN", split, int((~ok).sum()))
        df = df[ok]
    df = df.sort_values(["ID", "FECHA"], ignore_index=True)
    zones = pd.read_parquet(RES / "zone_table.parquet", columns=["ID", "lon", "lat"])
    df = df.merge(zones, on="ID", how="left")
    df["year"] = df.FECHA.dt.year.astype(np.int16)
    df["month"] = df.FECHA.dt.month.astype(np.int8)
    return df, runs, used


def _split_name(run: str) -> tuple[str, int]:
    method, start = run.split("@")
    return method, int(start)


def per_run(split: str, df: pd.DataFrame, runs: Sequence[str]) -> pd.DataFrame:
    """RMSE, sesgo y MAE por corrida, total y por anio; delta frente al mismo metodo en 1981."""
    train_end = SPLITS[split][0]
    o = df.TD_obs.to_numpy("f8")
    rows = []
    periods = [("total", np.ones(len(df), bool))] + [
        (str(y), (df.year == y).to_numpy()) for y in sorted(df.year.unique())]
    for run in runs:
        method, start = _split_name(run)
        clim = start if method == "timesfm_clim_propia" else CLIM_START
        pred = df[run].to_numpy("f8")
        for period, idx in periods:
            e = pred[idx] - o[idx]
            rows.append({"split": split, "metodo": method, "inicio": start, "anios_historial": train_end - start + 1,
                         "clim_inicio": clim, "clim_fin": train_end, "periodo": period, "n": int(idx.sum()),
                         "celdas": int(df.ID[idx].nunique()), "rmse": float(np.sqrt(np.mean(e ** 2))),
                         "sesgo": float(e.mean()), "mae": float(np.mean(np.abs(e)))})
    out = pd.DataFrame(rows)
    ref = out[out.inicio == CLIM_START].set_index(["metodo", "periodo"]).rmse
    key = [m if m != "timesfm_clim_propia" else "timesfm" for m in out.metodo]
    out["delta_rmse_vs_1981"] = out.rmse.to_numpy() - ref.reindex(list(zip(key, out.periodo))).to_numpy()
    return out


def gap_pairs(runs: Sequence[str]) -> list[tuple[str, str]]:
    """Cada inicio contra 1981 y contra el escalon anterior; TimesFM contra cada LLR al mismo
    inicio; el control de climatologia contra la escalera con climatologia fija."""
    pairs: list[tuple[str, str]] = []
    for m in METHODS:
        for s in STARTS[1:]:
            pairs.append((f"{m}@{s}", f"{m}@{STARTS[0]}"))
        for a, b in zip(STARTS[1:], STARTS[:-1]):
            if a != STARTS[1]:
                pairs.append((f"{m}@{a}", f"{m}@{b}"))
    for s in STARTS:
        pairs += [(f"timesfm@{s}", f"llr_rezagos@{s}"), (f"timesfm@{s}", f"llr_simple@{s}")]
    for r in runs:
        if r.startswith("timesfm_clim_propia@"):
            s = _split_name(r)[1]
            pairs += [(r, f"timesfm@{s}"), (r, f"timesfm@{STARTS[0]}")]
    return [(a, b) for a, b in pairs if a in runs and b in runs]


def gaps(split: str, df: pd.DataFrame, runs: Sequence[str]) -> pd.DataFrame:
    o = df.TD_obs.to_numpy("f8")
    se = pd.DataFrame({r: (df[r].to_numpy("f8") - o) ** 2 for r in runs}, index=df.index)
    out = []
    for scheme in ("mes_anio", "espacial_2g"):
        g = se.groupby(block_keys(df, scheme))
        n = g.size().to_numpy("f8")
        sums = {r: g[r].sum().to_numpy("f8") for r in runs}
        out.append(block_bootstrap(n, sums, gap_pairs(runs)).assign(esquema=scheme))
    t = pd.concat(out, ignore_index=True).assign(split=split)
    return t[["split", "esquema", *[c for c in t.columns if c not in ("split", "esquema")]]]


def run(splits: Sequence[str] = ("ll4b", "ll4"), out: Path = OUT) -> dict[str, pd.DataFrame]:
    out.mkdir(parents=True, exist_ok=True)
    tabs, gtabs, inputs, cells = [], [], {}, {}
    for split in splits:
        df, runs, used = load_split(split)
        inputs[split] = used
        cells[split] = int(df.ID.nunique())
        logger.info("%s: %d filas, %d celdas", split, len(df), cells[split])
        tabs.append(per_run(split, df, runs))
        gtabs.append(gaps(split, df, runs))
    result = {"escalera": pd.concat(tabs, ignore_index=True), "brechas": pd.concat(gtabs, ignore_index=True)}
    files = {"escalera": out / "a1_escalera_contexto.csv", "brechas": out / "a1_escalera_contexto_brechas.csv"}
    for k, path in files.items():
        result[k].to_csv(path, index=False, float_format="%.5f")
    write_provenance([str(p) for p in files.values()], inputs, splits, cells)
    write_tables_md(result, out / "a1_escalera_contexto.md")
    return result


MD_START, MD_END = "<!-- tablas:inicio -->", "<!-- tablas:fin -->"


def _f(x: float, sign: bool = False, nd: int = 3) -> str:
    return (f"{x:+.{nd}f}" if sign else f"{x:.{nd}f}").replace(".", ",").replace("-", "−")


def tables_md(result: dict[str, pd.DataFrame]) -> str:
    t, b = result["escalera"], result["brechas"]
    label = {"timesfm": "TimesFM tmin_anom_full", "llr_simple": "LLR simple", "llr_rezagos": "LLR con rezagos",
             "clim": "climatología", "tuned": "tuned (referencia)",
             "timesfm_clim_propia": "TimesFM, climatología propia (control)"}
    lines = []
    for sp in dict.fromkeys(t.split):
        tt = t[(t.split == sp) & (t.periodo == "total")]
        n, c = int(tt.n.iloc[0]), int(tt.celdas.iloc[0])
        lines += [f"### Bloque `{sp}`: RMSE total (°C) por inicio del historial ({c} celdas, " + f"{n:,}".replace(",", ".") + " filas)", "",
                  "| método | " + " | ".join(str(s) for s in STARTS) + " | Δ 2002 − 1981 |",
                  "|---|" + "---|" * (len(STARTS) + 1)]
        for m in ("timesfm", "llr_simple", "llr_rezagos"):
            r = tt[tt.metodo == m].set_index("inicio").rmse
            lines.append(f"| {label[m]} | " + " | ".join(_f(r[s]) for s in STARTS)
                         + f" | {_f(r[STARTS[-1]] - r[STARTS[0]], True)} |")
        for m in ("timesfm_clim_propia", "clim", "tuned"):
            for _, r in tt[tt.metodo == m].iterrows():
                cells = [_f(r.rmse) if s == r.inicio else "" for s in STARTS]
                lines.append(f"| {label[m]} | " + " | ".join(cells) + " | |")
        lines.append("")
        ty = t[(t.split == sp) & (t.periodo != "total") & t.metodo.isin(["timesfm", "llr_simple", "llr_rezagos"])]
        years = sorted(ty.periodo.unique())
        lines += [f"### Bloque `{sp}`: RMSE por año del bloque (°C)", "",
                  "| método | inicio | " + " | ".join(years) + " |", "|---|---|" + "---|" * len(years)]
        for m in ("timesfm", "llr_simple", "llr_rezagos"):
            for s in STARTS:
                r = ty[(ty.metodo == m) & (ty.inicio == s)].set_index("periodo").rmse
                lines.append(f"| {label[m]} | {s} | " + " | ".join(_f(r[y]) for y in years) + " |")
        lines.append("")
    lines += ["### Brechas pareadas RMSE(A) − RMSE(B), IC 95 % (°C; negativo favorece a A)", "",
              "| bloque | A − B | brecha | IC mes-año | IC espacial 2° |", "|---|---|---|---|---|"]
    for (sp, a, bb), g in b.groupby(["split", "metodo_a", "metodo_b"], sort=False):
        e = g.set_index("esquema")
        lines.append(f"| {sp} | {a} − {bb} | {_f(e.brecha.iloc[0], True, 4)} | "
                     f"[{_f(e.ic_lo['mes_anio'], True, 4)}; {_f(e.ic_hi['mes_anio'], True, 4)}] | "
                     f"[{_f(e.ic_lo['espacial_2g'], True, 4)}; {_f(e.ic_hi['espacial_2g'], True, 4)}] |")
    lines.append("")
    return "\n".join(lines)


def write_tables_md(result: dict[str, pd.DataFrame], path: Path) -> None:
    """Reemplaza el bloque de tablas entre marcadores y deja intacto el texto escrito a mano."""
    block = f"{MD_START}\n{tables_md(result)}\n{MD_END}"
    if path.exists() and MD_START in (text := path.read_text()) and MD_END in text:
        head, rest = text.split(MD_START, 1)
        text = head + block + rest.split(MD_END, 1)[1]
    else:
        text = f"# A1: escalera de inicio del contexto\n\n{block}\n"
    path.write_text(text)


def write_provenance(output_files: list[str], inputs: dict, splits: Sequence[str], cells: dict) -> None:
    from tdew_estimation import provenance as prov

    ends = {s: SPLITS[s][0] for s in splits}
    notes = ("Escalera de inicio del historial (tdew-03g, A1) sobre el panel de cribado restringido a las "
             f"celdas comunes con tuned; celdas evaluadas por split {cells}. TimesFM tmin_anom_full "
             f"zero-shot (trained=False) con contexto desde {list(STARTS)} y climatologia de anomalias "
             f"fija {CLIM_START}-train_end; control {list(CONTROLS)} (split, contexto, climatologia). "
             "LLR simple y con rezagos de Tmin (1, 2, 7, 30) con coeficientes y eleccion de h desde el "
             f"mismo inicio y climatologia {CLIM_START}-train_end; tuned de referencia (autoregressive). "
             f"train_end por split {ends}. Bootstrap {N_BOOT} replicas semilla {SEED}, bloques mes-anio "
             f"y espaciales de {BLOCK_DEG:g} grados. Entradas: {inputs}")
    record = prov.MetricProvenance(
        run_id=prov.new_run_id(), generated_at=prov.now_iso(), git_commit=prov.git_commit(),
        bead_id="tdew-03g", manifest_ref="docs/protocol/timesfm_manifest.yaml",
        model_family="comparison", model_id="multi", variant_label="a1_escalera_contexto",
        trained=True, training_period=(f"{min(STARTS)}-01-01", f"{max(ends.values())}-12-31"),
        validation_period=None,
        test_period=(f"{min(SPLITS[s][1][0] for s in splits)}-01-01",
                     f"{max(SPLITS[s][1][1] for s in splits)}-12-31"),
        split_id=",".join(splits), autoregressive=True, target_type="td_raw",
        climatology_used=True, climatology_role="baseline_and_anomaly_reference",
        inputs=tuple(sorted({m for d in inputs.values() for m in d})),
        panel_id="cribado_comun_tuned", panel_cell_count=max(cells.values()), panel_file=str(PANEL),
        output_files=tuple(output_files), seeds=(SEED,), notes=notes,
    )
    prov.record_metric_provenance(record)


def main(argv: Sequence[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--splits", nargs="+", default=["ll4b", "ll4"])
    ap.add_argument("--out", type=Path, default=OUT)
    a = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(message)s")
    run(a.splits, a.out)


if __name__ == "__main__":
    main()
