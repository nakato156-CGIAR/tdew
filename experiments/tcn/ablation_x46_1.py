#!/usr/bin/env python3
"""
experiments.tcn.ablation_x46_1

Ablación correctiva del TCN+atención (bead ``tdew-x46.1``). Mide, con el mismo
presupuesto de pasos y el mismo orden de datos, si los tres cambios propuestos
tras el diagnóstico del run ``week1-tcn-attention`` cruzan el baseline:

1. ``residual_persistence`` — la cabeza predice el residuo sobre
   ``TD_anom_norm(t)`` y arranca en cero, de modo que el modelo sin entrenar
   *es* persistencia.
2. ``film_identity`` — FiLM como ``(1+gamma)*h + beta`` con generador
   inicializado en cero, para que la modulación empiece en la identidad en vez
   de anular el resumen de la ventana (``|gamma|`` medido = 0.120 tras 8.5M
   pasos con la forma original).
3. Ciclo por pasos — "época" = ``--steps`` pasos fijos y validación sobre una
   submuestra estratificada fija, en vez de 1.7M pasos y 305M píxeles por época
   (11.6 h). Esto es lo que hace medible la comparación; no es una hipótesis
   sobre el modelo.

Se ablaciona además el cuarto punto del bead, los pesos por sitio: el sampler de
``TdewWindowDataset`` ya entrega batches 25/25/25/25 por round-robin, así que el
``weight = 1/n_train_rows(site)`` de ``generalist_mlr`` se aplica encima de una
corrección que ya ocurrió, y deja a Loreto en 4.2% del gradiente siendo ~70% de
la validación agrupada.

Las cuatro variantes comparten seed, orden de datos, submuestra de validación y
número de pasos, así que la diferencia entre ellas no puede atribuirse a "más
entrenamiento". ``current`` reproduce exactamente la configuración con la que se
entrenó el run largo y sirve de control interno.

Referencias externas (no se recalculan aquí): ``reports/week1_baselines/leaderboard.csv``.

Uso
---
uv run python -m experiments.tcn.ablation_x46_1 --steps 8000
uv run python -m experiments.tcn.ablation_x46_1 --steps 200 --val-per-site 4000  # humo
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Dict, List, Optional

import mlflow
import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader

from experiments.tcn.dataset import (
    DEFAULT_GOLD_DIR,
    DEFAULT_SILVER_DIR,
    DYNAMIC_COLS,
    PROVENANCE_COMMON,
    TdewWindowDataset,
    load_site_weights,
)
from experiments.tcn.train import TOTAL_CELLS, TRAIN_PERIOD, VALIDATION_PERIOD
from pipeline.qc import SITES
from tdew_estimation import experiment_tracking as et
from tdew_estimation import provenance as prov
from tdew_estimation.models import TCNAttentionConfig, TCNAttentionModel, invert_to_physical
from tdew_estimation.models.losses import weighted_huber_loss

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SITE_WEIGHTS = Path(__file__).resolve().parent / "site_weights.json"
DEFAULT_NORM_STATS = DEFAULT_GOLD_DIR / "normalization_stats.json"
DEFAULT_LEADERBOARD = REPO_ROOT / "reports" / "week1_baselines" / "leaderboard.csv"
DEFAULT_OUT = REPO_ROOT / "reports" / "week1_tcn_ablation"
PERSISTENCE_IDX = DYNAMIC_COLS.index("TD_anom_norm")

# (residual_persistence, film_identity, uniform_site_weights)
VARIANTS: Dict[str, Dict[str, bool]] = {
    "current": {"residual": False, "film_identity": False, "uniform_weights": False},
    "residual": {"residual": True, "film_identity": False, "uniform_weights": False},
    "residual+film": {"residual": True, "film_identity": True, "uniform_weights": False},
    "residual+film+uniform": {"residual": True, "film_identity": True, "uniform_weights": True},
}

# PROVENANCE_COMMON vive en experiments/tcn/dataset.py (junto a DYNAMIC_COLS/
# LABEL_COL, los hechos de los que depende) para que train.py y esta auditoria
# no mantengan cada una su propia copia que pueda desviarse.


def build_provenance(
    *, variant: str, context_length: int, seed: int, bead_id: str,
    mlflow_run_id: Optional[str], output_files: tuple[str, ...],
) -> prov.MetricProvenance:
    return prov.MetricProvenance(
        run_id=prov.new_run_id(),
        generated_at=prov.now_iso(),
        git_commit=prov.git_commit(),
        bead_id=bead_id,
        manifest_ref=PROVENANCE_COMMON["manifest_ref"],
        model_family="tcn_attention",
        model_id="week1-tcn-attention-ablation-x46.1",
        variant_label=f"{variant}_L{context_length}_seed{seed}",
        trained=True,
        training_period=TRAIN_PERIOD,
        validation_period=VALIDATION_PERIOD,
        test_period=None,
        split_id="validation",
        autoregressive=PROVENANCE_COMMON["autoregressive"],
        target_type=PROVENANCE_COMMON["target_type"],
        climatology_used=PROVENANCE_COMMON["climatology_used"],
        climatology_role=PROVENANCE_COMMON["climatology_role"],
        inputs=PROVENANCE_COMMON["inputs"],
        panel_id="ALL",
        panel_cell_count=TOTAL_CELLS,
        panel_file=None,
        seeds=(seed,),
        mlflow_run_id=mlflow_run_id,
        output_files=output_files,
    )


def load_td_anom_stats(path: Path) -> tuple[float, float]:
    stats = json.loads(Path(path).read_text())["TD_anom"]
    return float(stats["mean"]), float(stats["std"])


def leaderboard_reference(path: Path) -> pd.DataFrame:
    """Filas ``split == validation`` del leaderboard de baselines, indexadas por
    (site, method). Se usan para dos cosas: los RMSE de referencia por sitio y
    los ``n`` por sitio con que se repondera el agrupado (la submuestra de este
    experimento está balanceada por construcción, la validación real no)."""
    df = pd.read_csv(path)
    return df[df["split"] == "validation"].set_index(["site", "method"])


def build_val_subsample(
    *,
    gold_dir: Path,
    silver_dir: Path,
    context_length: int,
    site_weights: Dict[str, float],
    per_site: int,
    max_buckets: int,
    batch_size: int,
    num_workers: int,
    seed: int,
) -> Dict[str, Dict[str, torch.Tensor]]:
    """Submuestra de validación fija y balanceada: ``per_site`` ventanas por
    sitio, materializadas en tensores. Fija de una vez para las cuatro variantes
    (la comparación es sobre exactamente las mismas ventanas) y en memoria
    porque volver a recorrer el parquet en cada evaluación sería el costo
    dominante del experimento."""
    ds = TdewWindowDataset(
        gold_dir,
        silver_dir,
        context_length=context_length,
        split="validation",
        site_weights=site_weights,
        sites=SITES,
        shuffle_buffer_size=0,
        seed=seed,
        max_buckets=max_buckets,
    )
    id2site = {loc_id: info[2] for loc_id, info in ds._id_lookup.items()}
    loader = DataLoader(ds, batch_size=batch_size, num_workers=num_workers)

    keep = ("dynamic", "static", "region", "target_cond", "label", "td_clim_target")
    chunks: Dict[str, List[Dict[str, torch.Tensor]]] = {s: [] for s in SITES}
    counts = {s: 0 for s in SITES}
    for batch in loader:
        sites = np.array([id2site[int(i)] for i in batch["id"].numpy()])
        for site in SITES:
            if counts[site] >= per_site:
                continue
            mask = torch.from_numpy(sites == site)
            if not bool(mask.any()):
                continue
            take = min(int(mask.sum()), per_site - counts[site])
            idx = torch.nonzero(mask, as_tuple=False).squeeze(-1)[:take]
            chunks[site].append({k: batch[k][idx] for k in keep})
            counts[site] += take
        if all(counts[s] >= per_site for s in SITES):
            break
    missing = [s for s in SITES if counts[s] == 0]
    if missing:
        raise RuntimeError(f"la submuestra de validación no cubrió los sitios {missing}; sube --val-max-buckets")
    return {site: {k: torch.cat([c[k] for c in chunks[site]]) for k in keep} for site in SITES}


@torch.no_grad()
def evaluate_subsample(
    model: Optional[TCNAttentionModel],
    subsample: Dict[str, Dict[str, torch.Tensor]],
    device: torch.device,
    *,
    td_anom_mean: float,
    td_anom_std: float,
    predictor: str = "model",
    eval_batch: int = 8192,
) -> Dict[str, Dict[str, float]]:
    """RMSE/MAE/sesgo por sitio sobre la submuestra. ``predictor`` puede ser
    ``model``, ``persistence`` (la anomalía normalizada del último día de la
    ventana, que es lo que mide la fila ``persistence`` del leaderboard) o
    ``climatology`` (anomalía 0)."""
    if model is not None:
        model.eval()
    out: Dict[str, Dict[str, float]] = {}
    for site, data in subsample.items():
        se = ae = be = 0.0
        n = 0
        for start in range(0, len(data["label"]), eval_batch):
            sl = slice(start, start + eval_batch)
            dyn = data["dynamic"][sl].to(device).float()
            clim = data["td_clim_target"][sl].to(device).float()
            label = data["label"][sl].to(device).float()
            if predictor == "model":
                pred_norm = model(
                    dyn,
                    data["static"][sl].to(device).float(),
                    data["region"][sl].to(device),
                    data["target_cond"][sl].to(device).float(),
                )
            elif predictor == "persistence":
                pred_norm = dyn[:, -1, PERSISTENCE_IDX]
            elif predictor == "climatology":
                pred_norm = torch.full_like(label, -td_anom_mean / td_anom_std)
            else:
                raise ValueError(predictor)
            err = (
                invert_to_physical(pred_norm, td_anom_mean, td_anom_std, clim)
                - invert_to_physical(label, td_anom_mean, td_anom_std, clim)
            )
            se += float((err**2).sum())
            ae += float(err.abs().sum())
            be += float(err.sum())
            n += err.numel()
        out[site] = {"n": n, "mse": se / n, "rmse": (se / n) ** 0.5, "mae": ae / n, "bias": be / n}
    return out


def pooled_rmse(per_site: Dict[str, Dict[str, float]], site_n: Dict[str, float]) -> float:
    """RMSE agrupado reponderando el MSE de cada sitio por su número de filas en
    la validación real. La submuestra está balanceada 1:1:1:1, mientras que la
    validación del leaderboard es ~70% Loreto; sin esta reponderación el número
    de este experimento no sería comparable con la fila ``site=ALL``."""
    num = sum(per_site[s]["mse"] * site_n[s] for s in per_site)
    return (num / sum(site_n[s] for s in per_site)) ** 0.5


def train_variant(
    name: str,
    flags: Dict[str, bool],
    *,
    gold_dir: Path,
    silver_dir: Path,
    context_length: int,
    site_weights: Dict[str, float],
    subsample: Dict[str, Dict[str, torch.Tensor]],
    site_n: Dict[str, float],
    td_anom_mean: float,
    td_anom_std: float,
    steps: int,
    eval_every: int,
    batch_size: int,
    num_workers: int,
    lr: float,
    huber_delta: float,
    seed: int,
    train_max_buckets: int,
    device: torch.device,
) -> List[Dict[str, float]]:
    torch.manual_seed(seed)
    np.random.seed(seed)

    config = TCNAttentionConfig(
        residual_persistence=flags["residual"],
        film_identity=flags["film_identity"],
        persistence_feature_index=PERSISTENCE_IDX,
    )
    model = TCNAttentionModel(config).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)

    dataset = TdewWindowDataset(
        gold_dir,
        silver_dir,
        context_length=context_length,
        split="train",
        site_weights=site_weights,
        sites=SITES,
        shuffle_buffer_size=20_000,
        seed=seed,
        max_buckets=train_max_buckets,
    )
    dataset.set_epoch(0)
    loader = DataLoader(dataset, batch_size=batch_size, num_workers=num_workers, pin_memory=device.type == "cuda")

    history: List[Dict[str, float]] = []

    def record(step: int, train_loss: float, elapsed: float) -> None:
        per_site = evaluate_subsample(
            model, subsample, device, td_anom_mean=td_anom_mean, td_anom_std=td_anom_std
        )
        row = {
            "variant": name,
            "step": step,
            "train_loss": train_loss,
            "seconds": elapsed,
            "rmse_pooled": pooled_rmse(per_site, site_n),
        }
        row.update({f"rmse_{s}": per_site[s]["rmse"] for s in per_site})
        row.update({f"bias_{s}": per_site[s]["bias"] for s in per_site})
        history.append(row)
        mlflow.log_metric("val_rmse_pooled", row["rmse_pooled"], step=step)
        for s in per_site:
            mlflow.log_metric(f"val_rmse_{s}", per_site[s]["rmse"], step=step)
        if np.isfinite(train_loss):
            mlflow.log_metric("train_loss", train_loss, step=step)
        print(
            f"  [{name}] paso {step:>6}  loss={train_loss:.5f}  "
            f"rmse_pooled={row['rmse_pooled']:.4f}  " + "  ".join(f"{s[:4]}={per_site[s]['rmse']:.4f}" for s in per_site),
            flush=True,
        )

    record(0, float("nan"), 0.0)

    t0 = time.time()
    running, seen, step = 0.0, 0, 0
    use_amp = device.type == "cuda"
    for batch in loader:
        model.train()
        batch = {k: v.to(device, non_blocking=True) for k, v in batch.items()}
        weight = torch.ones_like(batch["weight"]) if flags["uniform_weights"] else batch["weight"].float()
        optimizer.zero_grad(set_to_none=True)
        with torch.autocast(device_type=device.type, dtype=torch.bfloat16, enabled=use_amp):
            pred = model(
                batch["dynamic"].float(), batch["static"].float(), batch["region"], batch["target_cond"].float()
            )
            loss = weighted_huber_loss(pred, batch["label"].float(), weight, delta=huber_delta)
        loss.backward()
        optimizer.step()
        running += float(loss.item())
        seen += 1
        step += 1
        if step % eval_every == 0 or step == steps:
            record(step, running / max(seen, 1), time.time() - t0)
            running, seen = 0.0, 0
        if step >= steps:
            break
    return history


def run(
    *,
    gold_dir: Path = DEFAULT_GOLD_DIR,
    silver_dir: Path = DEFAULT_SILVER_DIR,
    context_length: int = 31,
    steps: int = 8000,
    eval_every: int = 1000,
    batch_size: int = 1024,
    num_workers: int = 3,
    lr: float = 3e-4,
    huber_delta: float = 1.0,
    seed: int = 0,
    val_per_site: int = 40_000,
    val_max_buckets: int = 1,
    train_max_buckets: int = 4,
    site_weights_path: Path = DEFAULT_SITE_WEIGHTS,
    norm_stats_path: Path = DEFAULT_NORM_STATS,
    leaderboard_path: Path = DEFAULT_LEADERBOARD,
    out_dir: Path = DEFAULT_OUT,
    variants: Optional[List[str]] = None,
    device: Optional[str] = None,
    bead_id: str = "tdew-x46.1",
) -> pd.DataFrame:
    resolved_device = torch.device(device or ("cuda" if torch.cuda.is_available() else "cpu"))
    if resolved_device.type == "cuda":
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True

    site_weights = load_site_weights(site_weights_path)
    td_anom_mean, td_anom_std = load_td_anom_stats(norm_stats_path)
    reference = leaderboard_reference(leaderboard_path)
    site_n = {s: float(reference.loc[(s, "persistence"), "n"]) for s in SITES}

    print(f"[ablation] dispositivo={resolved_device} pasos={steps} batch={batch_size}", flush=True)
    t0 = time.time()
    subsample = build_val_subsample(
        gold_dir=gold_dir,
        silver_dir=silver_dir,
        context_length=context_length,
        site_weights=site_weights,
        per_site=val_per_site,
        max_buckets=val_max_buckets,
        batch_size=4096,
        num_workers=num_workers,
        seed=seed,
    )
    print(
        f"[ablation] submuestra de validación fija: {val_per_site} ventanas x {len(SITES)} sitios "
        f"({time.time() - t0:.0f}s)",
        flush=True,
    )

    rows: List[Dict[str, float]] = []
    for predictor in ("climatology", "persistence"):
        per_site = evaluate_subsample(
            None, subsample, resolved_device, td_anom_mean=td_anom_mean, td_anom_std=td_anom_std, predictor=predictor
        )
        row = {"variant": predictor, "step": 0, "train_loss": float("nan"), "seconds": 0.0,
               "rmse_pooled": pooled_rmse(per_site, site_n)}
        row.update({f"rmse_{s}": per_site[s]["rmse"] for s in per_site})
        row.update({f"bias_{s}": per_site[s]["bias"] for s in per_site})
        rows.append(row)
        print(f"[ablation] {predictor:<12} rmse_pooled={row['rmse_pooled']:.4f}  "
              + "  ".join(f"{s[:4]}={per_site[s]['rmse']:.4f}" for s in per_site), flush=True)

    selected = variants or list(VARIANTS)
    mlflow_run_ids: Dict[str, str] = {}
    for name in selected:
        flags = VARIANTS[name]
        params = {
            "variant": name,
            "residual_persistence": flags["residual"],
            "film_identity": flags["film_identity"],
            "uniform_site_weights": flags["uniform_weights"],
            "steps": steps,
            "batch_size": batch_size,
            "lr": lr,
            "huber_delta": huber_delta,
            "train_max_buckets": train_max_buckets,
            "val_per_site": val_per_site,
        }
        with et.start_run(
            f"x46.1-ablation-{name}",
            seed=seed,
            dataset_version="Data/gold/model_features_norm",
            site="ALL",
            context_length=context_length,
            params=params,
        ) as active_run:
            mlflow_run_ids[name] = active_run.info.run_id
            rows.extend(
                train_variant(
                    name,
                    flags,
                    gold_dir=gold_dir,
                    silver_dir=silver_dir,
                    context_length=context_length,
                    site_weights=site_weights,
                    subsample=subsample,
                    site_n=site_n,
                    td_anom_mean=td_anom_mean,
                    td_anom_std=td_anom_std,
                    steps=steps,
                    eval_every=eval_every,
                    batch_size=batch_size,
                    num_workers=num_workers,
                    lr=lr,
                    huber_delta=huber_delta,
                    seed=seed,
                    train_max_buckets=train_max_buckets,
                    device=resolved_device,
                )
            )

    history = pd.DataFrame(rows)
    out_dir.mkdir(parents=True, exist_ok=True)
    history.to_csv(out_dir / "ablation_history.csv", index=False)

    final = history[history["step"] == history.groupby("variant")["step"].transform("max")].copy()
    ref_rows = []
    for method in ("persistence", "generalist_mlr", "dept_mlr"):
        r = {"variant": f"leaderboard:{method}", "step": np.nan,
             "rmse_pooled": float(reference.loc[("ALL", method), "rmse"])}
        r.update({f"rmse_{s}": float(reference.loc[(s, method), "rmse"]) for s in SITES})
        ref_rows.append(r)
    summary = pd.concat([final, pd.DataFrame(ref_rows)], ignore_index=True)
    cols = ["variant", "step", "rmse_pooled"] + [f"rmse_{s}" for s in SITES]
    summary = summary[cols]
    summary.to_csv(out_dir / "ablation_summary.csv", index=False)
    print("\n" + summary.to_string(index=False, float_format=lambda v: f"{v:.4f}"), flush=True)
    print(f"\n[ablation] escrito {out_dir / 'ablation_summary.csv'}", flush=True)

    output_files = (str(out_dir / "ablation_summary.csv"), str(out_dir / "ablation_history.csv"))
    for name in selected:
        prov.record_metric_provenance(
            build_provenance(
                variant=name, context_length=context_length, seed=seed, bead_id=bead_id,
                mlflow_run_id=mlflow_run_ids.get(name), output_files=output_files,
            )
        )
    return summary


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Ablación correctiva del TCN+atención (bead tdew-x46.1).")
    p.add_argument("--gold-dir", type=Path, default=DEFAULT_GOLD_DIR)
    p.add_argument("--silver-dir", type=Path, default=DEFAULT_SILVER_DIR)
    p.add_argument("--context-length", type=int, default=31)
    p.add_argument("--steps", type=int, default=8000)
    p.add_argument("--eval-every", type=int, default=1000)
    p.add_argument("--batch-size", type=int, default=1024)
    p.add_argument("--num-workers", type=int, default=3)
    p.add_argument("--lr", type=float, default=3e-4)
    p.add_argument("--huber-delta", type=float, default=1.0)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--val-per-site", type=int, default=40_000)
    p.add_argument("--val-max-buckets", type=int, default=1)
    p.add_argument("--train-max-buckets", type=int, default=4)
    p.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    p.add_argument("--variants", nargs="*", default=None, choices=list(VARIANTS))
    p.add_argument("--device", type=str, default=None)
    p.add_argument("--bead-id", default="tdew-x46.1",
                    help="bead que gobierna esta corrida, para tdew_estimation.provenance")
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    run(
        gold_dir=args.gold_dir,
        silver_dir=args.silver_dir,
        context_length=args.context_length,
        steps=args.steps,
        eval_every=args.eval_every,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        lr=args.lr,
        huber_delta=args.huber_delta,
        seed=args.seed,
        val_per_site=args.val_per_site,
        val_max_buckets=args.val_max_buckets,
        train_max_buckets=args.train_max_buckets,
        out_dir=args.out_dir,
        variants=args.variants,
        device=args.device,
        bead_id=args.bead_id,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
