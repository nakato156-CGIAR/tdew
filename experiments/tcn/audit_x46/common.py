"""Utilidades compartidas de la auditoria.

Submuestreo reproducible de ventanas reales usando EXACTAMENTE el codigo del
proyecto (`TdewWindowDataset._load_bucket` y `_samples_for_rows`): se eligen
buckets y celdas al azar con semilla fija y se emiten todas las fechas
elegibles de cada celda. No se copia ninguna constante: las estadisticas de
normalizacion, los pesos por sitio y los ids por sitio se leen de disco.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
import pandas as pd
import torch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from experiments.tcn.dataset import (  # noqa: E402
    TdewWindowDataset, DEFAULT_GOLD_DIR, DEFAULT_SILVER_DIR, load_site_weights,
    DYNAMIC_COLS, STATIC_COLS, TARGET_COND_COLS,
)
from pipeline.qc import SITES  # noqa: E402
from tdew_estimation.bucket_layout import discover_bucket_ids  # noqa: E402
from tdew_estimation.models import TCNAttentionConfig, TCNAttentionModel  # noqa: E402

CKDIR = ROOT / "experiments/tcn/checkpoints/week1-tcn-attention_L31_seed0"
SITE_WEIGHTS_PATH = ROOT / "experiments/tcn/site_weights.json"
NORM_STATS_PATH = DEFAULT_GOLD_DIR / "normalization_stats.json"


def td_anom_stats():
    s = json.loads(NORM_STATS_PATH.read_text())["TD_anom"]
    return float(s["mean"]), float(s["std"])


def make_dataset(split: str, context_length: int = 31) -> TdewWindowDataset:
    return TdewWindowDataset(
        DEFAULT_GOLD_DIR, DEFAULT_SILVER_DIR,
        context_length=context_length, split=split,
        site_weights=load_site_weights(SITE_WEIGHTS_PATH),
        sites=SITES, shuffle_buffer_size=0, seed=0,
    )


def sample_windows(split: str, *, n_buckets: int, cells_per_site_per_bucket: int,
                   max_dates_per_cell: int | None = None, seed: int = 20260921,
                   context_length: int = 31, verbose: bool = True) -> dict:
    """Devuelve un dict de arrays con `n` ventanas reales del split pedido."""
    ds = make_dataset(split, context_length)
    rng = np.random.default_rng(seed)
    all_buckets = discover_bucket_ids(DEFAULT_GOLD_DIR / "model_features_norm")
    buckets = sorted(rng.choice(all_buckets, size=n_buckets, replace=False).tolist())
    if verbose:
        print(f"[sample_windows] split={split} buckets elegidos (de {len(all_buckets)}): {buckets}")

    out = {k: [] for k in ["dynamic", "static", "region", "target_cond", "label",
                           "td_clim", "weight", "id", "date_ordinal", "site"]}
    for b in buckets:
        bucket = ds._load_bucket(b)
        if bucket is None:
            continue
        seq = bucket["seq"].assign(_site=bucket["seq"]["ID"].map(ds._site_of_id))
        for site in SITES:
            rows = seq[seq["_site"] == site]
            if rows.empty:
                continue
            k = min(cells_per_site_per_bucket, len(rows))
            rows = rows.sample(n=k, random_state=int(rng.integers(0, 2**31 - 1)))
            for s in ds._samples_for_rows(bucket, rows):
                out["dynamic"].append(s["dynamic"])
                out["static"].append(s["static"])
                out["region"].append(s["region"])
                out["target_cond"].append(s["target_cond"])
                out["label"].append(s["label"])
                out["td_clim"].append(s["td_clim_target"])
                out["weight"].append(s["weight"])
                out["id"].append(s["id"])
                out["date_ordinal"].append(s["date_ordinal"])
                out["site"].append(site)
        del bucket
    res = {
        "dynamic": np.stack(out["dynamic"]).astype(np.float32),
        "static": np.stack(out["static"]).astype(np.float32),
        "region": np.array(out["region"], dtype=np.int64),
        "target_cond": np.stack(out["target_cond"]).astype(np.float32),
        "label": np.array(out["label"], dtype=np.float32),
        "td_clim": np.array(out["td_clim"], dtype=np.float32),
        "weight": np.array(out["weight"], dtype=np.float32),
        "id": np.array(out["id"], dtype=np.int64),
        "date_ordinal": np.array(out["date_ordinal"], dtype=np.int64),
        "site": np.array(out["site"]),
    }
    if max_dates_per_cell is not None:
        pass
    if verbose:
        print(f"[sample_windows] n={len(res['label'])}, celdas unicas={len(np.unique(res['id']))}")
        for s in SITES:
            m = res["site"] == s
            print(f"    {s:22s} n={m.sum():>8d} celdas={len(np.unique(res['id'][m])):>5d}")
    return res


def load_model(ckpt_name: str = "last.pt") -> TCNAttentionModel:
    ck = torch.load(CKDIR / ckpt_name, map_location="cpu", weights_only=False)
    cfg = ck["config"]
    model = TCNAttentionModel(TCNAttentionConfig(
        d_model=cfg["d_model"], n_tcn_blocks=cfg["n_tcn_blocks"],
        kernel_size=cfg["kernel_size"], dilation_base=cfg["dilation_base"],
        n_attention_heads=cfg["n_attention_heads"], dropout=cfg["dropout"]))
    model.load_state_dict(ck["model_state_dict"])
    model.eval()
    return model


@torch.no_grad()
def predict_norm(model, sample: dict, *, batch: int = 8192,
                 dynamic=None, static=None, region=None, target_cond=None) -> np.ndarray:
    dyn = sample["dynamic"] if dynamic is None else dynamic
    sta = sample["static"] if static is None else static
    reg = sample["region"] if region is None else region
    tc = sample["target_cond"] if target_cond is None else target_cond
    outs = []
    for i in range(0, len(dyn), batch):
        outs.append(model(torch.from_numpy(np.ascontiguousarray(dyn[i:i+batch])),
                          torch.from_numpy(np.ascontiguousarray(sta[i:i+batch])),
                          torch.from_numpy(np.ascontiguousarray(reg[i:i+batch])),
                          torch.from_numpy(np.ascontiguousarray(tc[i:i+batch]))).numpy())
    return np.concatenate(outs)


def metrics(pred_phys: np.ndarray, obs_phys: np.ndarray) -> dict:
    err = pred_phys - obs_phys
    f = np.isfinite(err)
    err, p, o = err[f], pred_phys[f], obs_phys[f]
    return {"n": int(err.size), "rmse": float(np.sqrt(np.mean(err**2))),
            "mae": float(np.mean(np.abs(err))), "bias": float(np.mean(err)),
            "r": float(np.corrcoef(p, o)[0, 1])}


def to_phys(pred_norm, sample, mean, std):
    return pred_norm * std + mean + sample["td_clim"]
