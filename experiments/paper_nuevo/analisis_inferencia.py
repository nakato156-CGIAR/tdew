"""Inferencia adicional para el paper nuevo (tdew-4w2), respuesta a la revision simulada.

Reutiliza ``experiments.amenazas.desglose`` (``load_split``, ``block_bootstrap``, ``BLOCK_DEG``,
``N_BOOT``, ``SEED``). Brecha = RMSE(TimesFM) - RMSE(rival); negativo favorece a TimesFM.

1. ``r1_brecha_horizonte.csv``: brecha por mes desde el inicio del bloque (1..48) y por anio
   dentro del bloque (1..4), con IC 95 % por bootstrap de bloques espaciales de 2 grados.
2. ``r1_bootstrap_espaciotemporal.csv``: IC con bloques 2 grados x anio (espacio-tiempo) y bloques
   solo temporales trimestre-anio (16 bloques), mismas N_BOOT y SEED. El esquema ``espacial_2g``
   se recalcula como control y debe reproducir ``a1_brechas.csv``.
3. ``r1_diebold_mariano.csv``: Diebold-Mariano sobre la serie diaria de la perdida media sobre
   celdas d_t = media(e_A^2 - e_B^2), varianza Newey-West (nucleo de Bartlett) con dos reglas de
   rezago: floor(4 (T/100)^(2/9)) y 30 dias. Se reporta el estadistico DM con p normal y la version
   con la correccion de Harvey-Leybourne-Newbold (h = 1, p con t de T-1 gl). p ajustado por Holm
   sobre la familia pares x bloques x ambitos, por separado para cada regla de rezago.

Uso: ``uv run python -m experiments.paper_nuevo.analisis_inferencia [--splits ll4 ll4b]``
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd
from scipy import stats

from experiments.amenazas import desglose as dg
from experiments.amenazas.desglose import BLOCK_DEG, N_BOOT, SEED, block_bootstrap, load_split

logger = logging.getLogger("paper_nuevo.inferencia")

OUT = Path("reports/paper_nuevo/resultados")
TFM = "timesfm_anom"
RIVALS = ("tuned", "tuned_sin_td", "llr_rezagos_sel", "llr_simple_sel")
SCHEMES = ("espacial_2g", "espaciotemporal_2g_anio", "temporal_trim_anio")
LONG_LAG = 30
FILES = {"horizonte": "r1_brecha_horizonte.csv", "boot": "r1_bootstrap_espaciotemporal.csv",
         "dm": "r1_diebold_mariano.csv"}


def block_keys(df: pd.DataFrame, scheme: str) -> np.ndarray:
    """Claves de bloque: los esquemas de desglose mas dos espacio-tiempo/temporales nuevos."""
    if scheme in ("espacial_2g", "mes_anio"):
        return dg.block_keys(df, scheme)
    year = df.year.to_numpy(np.int64)
    if scheme == "espaciotemporal_2g_anio":
        return dg.block_keys(df, "espacial_2g") * 10000 + year
    if scheme == "temporal_trim_anio":
        quarter = (df.month.to_numpy(np.int64) - 1) // 3 + 1
        return year * 10 + quarter
    raise ValueError(scheme)


def horizon_index(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """(mes desde el inicio del bloque 1..48, anio dentro del bloque 1..4)."""
    y0 = int(df.year.min())
    year = df.year.to_numpy(np.int64) - y0
    return year * 12 + df.month.to_numpy(np.int64), year + 1


def nw_lag(t: int) -> int:
    """Regla de rezago de Newey-West (1994) con nucleo de Bartlett: floor(4 (T/100)^(2/9))."""
    return int(np.floor(4.0 * (t / 100.0) ** (2.0 / 9.0)))


def nw_variance(x: np.ndarray, lag: int) -> float:
    """Varianza de largo plazo de x (Bartlett), para la varianza de la media dividir entre T."""
    t = len(x)
    xc = x - x.mean()
    lrv = float(xc @ xc) / t
    for k in range(1, min(lag, t - 1) + 1):
        lrv += 2.0 * (1.0 - k / (lag + 1.0)) * float(xc[k:] @ xc[:-k]) / t
    return lrv


def diebold_mariano(d: np.ndarray, lag: int) -> dict[str, float]:
    """DM con HAC Newey-West y correccion HLN (h=1). d = perdida(A) - perdida(B)."""
    d = np.asarray(d, dtype="f8")
    t = len(d)
    lrv = max(nw_variance(d, lag), 1e-300)
    dm = float(d.mean() / np.sqrt(lrv / t))
    hln = dm * np.sqrt((t + 1 - 2 + 0.0) / t)  # h = 1: (T + 1 - 2h + h(h-1)/T) / T
    return {"T": t, "rezago": lag, "perdida_media": float(d.mean()), "dm": dm,
            "p_normal": float(2 * stats.norm.sf(abs(dm))), "dm_hln": float(hln),
            "p_hln": float(2 * stats.t.sf(abs(hln), t - 1))}


def holm(p: Sequence[float]) -> np.ndarray:
    """Ajuste de Holm (step-down) de una familia de p-values."""
    p = np.asarray(p, dtype="f8")
    m = len(p)
    order = np.argsort(p)
    adj = np.empty(m)
    run = 0.0
    for i, j in enumerate(order):
        run = max(run, (m - i) * p[j])
        adj[j] = min(1.0, run)
    return adj


def _pairs(methods: Sequence[str]) -> list[tuple[str, str]]:
    return [(TFM, r) for r in RIVALS if r in methods and TFM in methods]


def horizon_gaps(df: pd.DataFrame, se: pd.DataFrame, pairs, n_boot: int = N_BOOT) -> pd.DataFrame:
    month, year = horizon_index(df)
    bkey = block_keys(df, "espacial_2g")
    out = []
    for unit, h in (("mes", month), ("anio", year)):
        for lvl in np.unique(h):
            m = h == lvl
            g = se[m].groupby(bkey[m])
            n = g.size().to_numpy("f8")
            sums = {c: g[c].sum().to_numpy("f8") for c in se.columns}
            res = block_bootstrap(n, sums, pairs, n_boot=n_boot)
            res.insert(0, "horizonte", int(lvl))
            res.insert(0, "unidad", unit)
            res["n"] = int(m.sum())
            res["rmse_a"] = float(np.sqrt(se.loc[m, pairs[0][0]].mean()))
            res["rmse_b"] = [float(np.sqrt(se.loc[m, b].mean())) for _, b in pairs]
            out.append(res)
    return pd.concat(out, ignore_index=True)


def scheme_gaps(df: pd.DataFrame, se: pd.DataFrame, pairs, n_boot: int = N_BOOT) -> pd.DataFrame:
    out = []
    for scheme in SCHEMES:
        g = se.groupby(block_keys(df, scheme))
        n = g.size().to_numpy("f8")
        sums = {c: g[c].sum().to_numpy("f8") for c in se.columns}
        out.append(block_bootstrap(n, sums, pairs, n_boot=n_boot).assign(esquema=scheme))
    return pd.concat(out, ignore_index=True)


def dm_table(df: pd.DataFrame, se: pd.DataFrame, pairs) -> pd.DataFrame:
    by_day = se.groupby(df.FECHA.to_numpy()).mean().sort_index()
    rows = []
    t = len(by_day)
    for a, b in pairs:
        d = (by_day[a] - by_day[b]).to_numpy()
        for regla, lag in (("nw_auto", nw_lag(t)), ("nw_30", LONG_LAG)):
            rows.append({"metodo_a": a, "metodo_b": b, "regla_rezago": regla,
                         **diebold_mariano(d, lag)})
    return pd.DataFrame(rows)


def run(splits: Sequence[str], out: Path = OUT, n_boot: int = N_BOOT) -> dict[str, pd.DataFrame]:
    out.mkdir(parents=True, exist_ok=True)
    tabs: dict[str, list[pd.DataFrame]] = {"horizonte": [], "boot": [], "dm": []}
    inputs: dict[str, dict[str, str]] = {}
    for split in splits:
        df, methods, used = load_split(split)
        pairs = _pairs(methods)
        cols = sorted({m for p in pairs for m in p})
        inputs[split] = {m: used[m] for m in cols}
        for ambito, sub in (("panel", df), ("peru", df[df.peru].reset_index(drop=True))):
            se = dg.squared_errors(sub, cols)
            tag = {"split": split, "ambito": ambito}
            tabs["horizonte"].append(horizon_gaps(sub, se, pairs, n_boot).assign(**tag))
            tabs["boot"].append(scheme_gaps(sub, se, pairs, n_boot).assign(**tag))
            tabs["dm"].append(dm_table(sub, se, pairs).assign(**tag))
            logger.info("%s %s listo", split, ambito)
        del df
    res = {k: pd.concat(v, ignore_index=True) for k, v in tabs.items()}
    dm = res["dm"]
    dm["p_holm"] = np.nan
    for _, idx in dm.groupby("regla_rezago").groups.items():
        dm.loc[idx, "p_holm"] = holm(dm.loc[idx, "p_hln"].to_numpy())
    dm["familia"] = dm.groupby("regla_rezago").p_hln.transform("size")
    res["dm"] = dm
    front = ["split", "ambito"]
    for k, name in FILES.items():
        t = res[k]
        res[k] = t[front + [c for c in t.columns if c not in front]]
        res[k].to_csv(out / name, index=False, float_format="%.6g")
    check_a1(res["boot"], out / "a1_brechas.csv")
    write_provenance([str(out / n) for n in FILES.values()], inputs, splits, n_boot)
    return res


def check_a1(boot: pd.DataFrame, a1_path: Path, tol: float = 5e-6) -> None:
    """Las brechas espacial_2g deben reproducir los puntos de a1_brechas.csv."""
    if not a1_path.exists():
        return
    a1 = pd.read_csv(a1_path)
    a1 = a1[a1.esquema == "espacial_2g"]
    m = boot[boot.esquema == "espacial_2g"].merge(
        a1, on=["split", "ambito", "metodo_a", "metodo_b"], suffixes=("", "_a1"))
    if m.empty:
        raise AssertionError("sin interseccion con a1_brechas.csv")
    diff = (m.brecha - m.brecha_a1).abs().max()
    ic = max((m.ic_lo - m.ic_lo_a1).abs().max(), (m.ic_hi - m.ic_hi_a1).abs().max())
    logger.info("control a1: %d brechas, max|dif punto|=%.2e, max|dif IC|=%.2e", len(m), diff, ic)
    if diff > tol or ic > tol:
        raise AssertionError(f"no reproduce a1_brechas.csv: punto {diff}, IC {ic}")


def write_provenance(output_files: list[str], inputs: dict, splits: Sequence[str], n_boot: int) -> None:
    from tdew_estimation import provenance as prov

    notes = (f"Inferencia R1 (tdew-4w2): brecha por horizonte, bootstrap espacio-tiempo ({n_boot} replicas, "
             f"semilla {SEED}, bloques {BLOCK_DEG:g} grados x anio y trimestre-anio) y Diebold-Mariano HAC "
             f"(rezago floor(4(T/100)^(2/9)) y {LONG_LAG}, HLN, Holm). Filas comunes a todos los metodos "
             f"(desglose.load_split); mascara Peru = peru_mask. Entradas: {inputs}")
    ends = {"ll4": 2012, "ll4b": 2008}
    record = prov.MetricProvenance(
        run_id=prov.new_run_id(), generated_at=prov.now_iso(), git_commit=prov.git_commit(),
        bead_id="tdew-4w2", manifest_ref="docs/protocol/timesfm_manifest.yaml",
        model_family="comparison", model_id="multi", variant_label="r1_inferencia",
        trained=True, training_period=("1981-01-01", f"{max(ends[s] for s in splits)}-12-31"),
        validation_period=None,
        test_period=(f"{min(ends[s] for s in splits) + 1}-01-01", f"{max(ends[s] for s in splits) + 4}-12-31"),
        split_id=",".join(splits), autoregressive=True, target_type="td_raw",
        climatology_used=True, climatology_role="baseline_and_anomaly_reference",
        inputs=tuple(sorted({m for d in inputs.values() for m in d})),
        panel_id="nacional_17027", panel_cell_count=17027, panel_file=str(dg.PANEL),
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
