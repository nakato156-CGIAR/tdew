"""
experiments.tcn.dataset

``TdewWindowDataset``: a ``torch.utils.data.IterableDataset`` that slices
``X_{t-L+1:t} -> Td(t+1)`` training windows on the fly from
``Data/gold/model_features_norm``, using ``Data/gold/sequence_index/L={L}``
(``pipeline.sequences``) as the eligibility index. It never materializes
windows on disk -- for L=60 that would multiply the multi-billion-row
dataset ~60x, the same reasoning ``pipeline/sequences.py`` documents for why
it only stores run boundaries.

Per bucket (``id_bucket=N``, one parquet file, ~1GB): load the needed
columns of ``model_features_norm`` once, resolve every eligible target
date's row offset with a single vectorized ``np.searchsorted`` per (ID,
split) run (not one search per window), then slice
``dyn_mat[offset-L:offset]`` for the window and read
label/target_cond/static/td_clim at ``offset`` (the row for date t+1).
``model_features_norm`` is already scoped to the 4 protocol departments (see
the ``tdew-silver-department-scoping`` project memory), so every ID present
belongs to one of them -- no extra department filter is needed on top of
what's already on disk.

Design decisions and their rationale are in the tcn-attention design plan
(bead tdew-x46, ``adaptive-leaping-summit.md``):
- site weights (`1/n_train_rows(site)`, generalist_mlr's criterion) are
  precomputed once (``experiments.tcn.site_weights``) and passed in, fixed
  across the three L runs;
- sharding across ``num_workers`` is by whole bucket, a deterministic
  permutation seeded by ``seed + epoch`` (same pattern as
  ``DistributedSampler.set_epoch``).

Batch composition / site interleaving (added 2026-09-18, after review):
``sequence_index`` rows inside a bucket are iterated by ``ID``, and each ID
contributes every one of its ~3,987 train-split target dates (L=31,
2002-2012) consecutively before the next ID. Department ``ID`` ranges are
two mostly-disjoint numeric blocks -- Loreto/San Martin (~181K-1.42M,
~347K/436K cells) and Lima/Cusco (~1.64M-2.37M) -- so a naive ascending-ID
scan spends the large majority of an epoch emitting Selva-only samples
before ever reaching Costa/Sierra. A bounded shuffle buffer alone cannot
fix this: at ~3,987 samples/cell, a 20,000-sample buffer only spans ~5
cells, nowhere near enough to bridge that numeric gap. Left uncorrected,
this would make most batches near-homogeneous in site -- harmless for
LayerNorm/GroupNorm (both normalize per-sample, independent of what else is
in the batch), but real for optimization: Adam's momentum would track long
runs of one site's gradient before ever seeing another, an unintended
"curriculum by site" the per-site loss weighting does not fix (that only
corrects the epoch-level average, not per-batch composition).

Fix: per bucket, split ``sequence_index`` rows by site, run one flat
generator per site (still sequential within a site -- one cell's dates
after another), and merge them with unweighted round-robin (one sample per
site per round, cycling; a site drops out of the rotation once its
in-bucket cells are exhausted). Every group of (number of sites present)
consecutive raw samples therefore contains one of each site, independent of
buffer size or ``num_workers``. Round-robin is deliberately *unweighted* by
``site_weight`` -- weighting here would under-represent Selva in the
stream, the opposite of the diversity goal; frequency correction is the
loss weighting's job, not the sampler's. The shuffle buffer still runs
afterwards (train split only) -- its remaining job is finer: decorrelating
the run of consecutive calendar days a single currently-open cell
contributes within its site's turn, not bridging sites (that's now
structural).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
import torch
from torch.utils.data import IterableDataset, get_worker_info

from pipeline.qc import SITES, load_site_ids
from tdew_estimation.bucket_layout import discover_bucket_ids

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_GOLD_DIR = REPO_ROOT / "Data" / "gold"
DEFAULT_SILVER_DIR = REPO_ROOT / "Data" / "silver"

# docs/protocol/week1_manifest.yaml sites.departments[].region_natural
REGION_NATURAL: Dict[str, str] = {
    "lima": "Costa",
    "cusco": "Sierra",
    "iquitos_loreto": "Selva",
    "tarapoto_san_martin": "Selva",
}
REGION_INDEX: Dict[str, int] = {"Costa": 0, "Sierra": 1, "Selva": 2}

DYNAMIC_COLS: Tuple[str, ...] = ("TMIN_anom_norm", "TMAX_anom_norm", "TD_anom_norm", "sin_doy", "cos_doy")
STATIC_COLS: Tuple[str, ...] = ("DEM_norm", "TDI_norm", "X_norm", "Y_norm")
TARGET_COND_COLS: Tuple[str, ...] = ("sin_doy", "cos_doy", "LST_DAY_norm", "LST_NIGHT_norm")
LABEL_COL = "TD_anom_norm"
TD_CLIM_COL = "TD_clim"
REQUIRED_COLS: Tuple[str, ...] = tuple(
    dict.fromkeys(("ID", "date") + DYNAMIC_COLS + STATIC_COLS + TARGET_COND_COLS + (LABEL_COL, TD_CLIM_COL))
)


def load_site_weights(path: Path) -> Dict[str, float]:
    payload = json.loads(Path(path).read_text())
    return {site: float(w) for site, w in payload["weight"].items()}


def _build_id_lookup(
    silver_dir: Path, sites: Sequence[str], site_weights: Dict[str, float]
) -> Dict[int, Tuple[int, float, str]]:
    """ID -> (region_index, sample_weight, site), built once from the
    per-site grid-id CSVs (``Data/silver/department_grid_ids/*.csv``). The
    site name is kept (not just region) so the dataset can split
    ``sequence_index`` rows by site for round-robin interleaving -- see the
    module docstring."""
    lookup: Dict[int, Tuple[int, float, str]] = {}
    for site in sites:
        ids = load_site_ids(silver_dir, site)
        region_idx = REGION_INDEX[REGION_NATURAL[site]]
        weight = site_weights[site]
        for location_id in ids:
            lookup[int(location_id)] = (region_idx, weight, site)
    return lookup


def _round_robin(generators: Sequence[Iterator[dict]]) -> Iterator[dict]:
    """Merge generators one-item-per-round, dropping a generator from the
    rotation once it's exhausted (does not wait for the others). With N
    generators still alive, every window of N consecutive outputs contains
    exactly one item from each."""
    alive = list(generators)
    while alive:
        still_alive = []
        for gen in alive:
            try:
                yield next(gen)
                still_alive.append(gen)
            except StopIteration:
                continue
        alive = still_alive


class TdewWindowDataset(IterableDataset):
    def __init__(
        self,
        gold_dir: Path,
        silver_dir: Path,
        *,
        context_length: int,
        split: str,
        site_weights: Dict[str, float],
        sites: Sequence[str] = SITES,
        shuffle_buffer_size: int = 20_000,
        seed: int = 0,
        max_buckets: Optional[int] = None,
    ):
        super().__init__()
        if split not in ("train", "validation", "test"):
            raise ValueError(f"split must be train/validation/test, got {split!r}")
        self.gold_dir = Path(gold_dir)
        self.silver_dir = Path(silver_dir)
        self.context_length = context_length
        self.split = split
        self.sites = tuple(sites)
        self.shuffle_buffer_size = shuffle_buffer_size
        self.seed = seed
        self.max_buckets = max_buckets
        self._epoch = 0

        self._seq_dir = self.gold_dir / "sequence_index" / f"L={context_length}"
        self._features_dir = self.gold_dir / "model_features_norm"
        self._id_lookup = _build_id_lookup(self.silver_dir, self.sites, site_weights)
        # Precomputed once (not per bucket): ID -> site, used to split each
        # bucket's sequence_index rows by site for round-robin interleaving.
        self._site_of_id = {loc_id: info[2] for loc_id, info in self._id_lookup.items()}

    def set_epoch(self, epoch: int) -> None:
        self._epoch = epoch

    def _bucket_ids_for_worker(self) -> List[int]:
        bucket_ids = discover_bucket_ids(self._features_dir)
        if self.max_buckets is not None:
            bucket_ids = bucket_ids[: self.max_buckets]
        rng = np.random.default_rng(self.seed + self._epoch)
        shuffled = rng.permutation(bucket_ids).tolist()

        worker_info = get_worker_info()
        if worker_info is None:
            return shuffled
        return shuffled[worker_info.id :: worker_info.num_workers]

    def _load_bucket(self, bucket_id: int) -> Optional[dict]:
        seq_path = self._seq_dir / f"id_bucket={bucket_id}" / "part.parquet"
        feat_path = self._features_dir / f"id_bucket={bucket_id}" / "part.parquet"
        if not seq_path.exists() or not feat_path.exists():
            return None

        seq = pd.read_parquet(seq_path)
        seq = seq[(seq["split"] == self.split) & (seq["n_eligible_targets"] > 0)]
        seq = seq[seq["ID"].isin(self._id_lookup.keys())]
        if seq.empty:
            return None

        feat = pd.read_parquet(feat_path, columns=list(REQUIRED_COLS))
        # model_features_norm is written sorted by (ID, date) (pipeline.gold /
        # pipeline.features); verify cheaply instead of re-sorting ~37M rows.
        id_arr = feat["ID"].to_numpy()
        if not np.all(np.diff(id_arr) >= 0):
            raise ValueError(f"bucket {bucket_id}: model_features_norm rows are not sorted by ID as expected")

        date_ord = feat["date"].to_numpy().astype("datetime64[D]").astype(np.int64)
        unique_ids, id_starts = np.unique(id_arr, return_index=True)
        id_ends = np.append(id_starts[1:], len(id_arr))
        id_ranges = dict(zip(unique_ids.tolist(), zip(id_starts.tolist(), id_ends.tolist())))

        dyn_mat = feat[list(DYNAMIC_COLS)].to_numpy(dtype=np.float32)
        static_mat = feat[list(STATIC_COLS)].to_numpy(dtype=np.float32)
        target_cond_mat = feat[list(TARGET_COND_COLS)].to_numpy(dtype=np.float32)
        label_arr = feat[LABEL_COL].to_numpy(dtype=np.float32)
        td_clim_arr = feat[TD_CLIM_COL].to_numpy(dtype=np.float32)

        return {
            "seq": seq,
            "date_ord": date_ord,
            "id_ranges": id_ranges,
            "dyn_mat": dyn_mat,
            "static_mat": static_mat,
            "target_cond_mat": target_cond_mat,
            "label_arr": label_arr,
            "td_clim_arr": td_clim_arr,
        }

    def _samples_for_rows(self, bucket, rows: pd.DataFrame) -> Iterator[dict]:
        """Yield samples for exactly the given ``sequence_index`` rows (all
        belonging to one site -- see ``_site_generators``), in the order
        ``rows`` is given (each row's cell contributes all its eligible
        dates consecutively, same as before the site split)."""
        L = self.context_length
        date_ord = bucket["date_ord"]
        id_ranges = bucket["id_ranges"]

        for row in rows.itertuples(index=False):
            location_id = int(row.ID)
            if location_id not in id_ranges:
                continue
            start, end = id_ranges[location_id]

            first_ord = np.datetime64(row.first_eligible_target_date, "D").astype(np.int64)
            last_ord = np.datetime64(row.last_eligible_target_date, "D").astype(np.int64)
            if last_ord < first_ord:
                continue
            target_ords = np.arange(first_ord, last_ord + 1, dtype=np.int64)

            local_dates = date_ord[start:end]
            local_offsets = np.searchsorted(local_dates, target_ords)
            if not np.array_equal(local_dates[local_offsets], target_ords):
                raise ValueError(f"ID {location_id}: expected dense daily coverage, found a calendar gap")
            offsets = local_offsets + start

            region_idx, weight, _site = self._id_lookup[location_id]
            for offset, target_ord in zip(offsets.tolist(), target_ords.tolist()):
                window_start = offset - L
                if window_start < start:
                    continue  # eligibility should prevent this; skip defensively
                yield {
                    "dynamic": bucket["dyn_mat"][window_start:offset].copy(),
                    "static": bucket["static_mat"][offset].copy(),
                    "region": np.int64(region_idx),
                    "target_cond": bucket["target_cond_mat"][offset].copy(),
                    "label": np.float32(bucket["label_arr"][offset]),
                    "td_clim_target": np.float32(bucket["td_clim_arr"][offset]),
                    "weight": np.float32(weight),
                    "id": np.int64(location_id),
                    "date_ordinal": np.int64(target_ord),
                }

    def _site_generators(self, bucket, rng: np.random.Generator) -> List[Iterator[dict]]:
        """Split this bucket's ``sequence_index`` rows by site and return
        one flat sample generator per site present (row order shuffled per
        site so within-site cell order isn't a second source of systematic
        drift, e.g. by latitude/elevation). ``__iter__`` round-robins these
        -- see the module docstring for why (site-homogeneous batches)."""
        seq = bucket["seq"]
        seq = seq.assign(_site=seq["ID"].map(self._site_of_id))

        generators: List[Iterator[dict]] = []
        for site in self.sites:
            site_rows = seq[seq["_site"] == site]
            if site_rows.empty:
                continue
            site_rows = site_rows.sample(frac=1.0, random_state=int(rng.integers(0, 2**31 - 1)))
            generators.append(self._samples_for_rows(bucket, site_rows))
        return generators

    def _shuffled(self, samples: Iterator[dict], rng: np.random.Generator) -> Iterator[dict]:
        if self.split != "train" or self.shuffle_buffer_size <= 1:
            yield from samples
            return
        buffer: List[dict] = []
        for sample in samples:
            if len(buffer) < self.shuffle_buffer_size:
                buffer.append(sample)
                continue
            idx = int(rng.integers(0, len(buffer)))
            yield buffer[idx]
            buffer[idx] = sample
        rng.shuffle(buffer)
        yield from buffer

    def __iter__(self) -> Iterator[dict]:
        rng = np.random.default_rng(self.seed + self._epoch + 1)
        bucket_ids = self._bucket_ids_for_worker()

        def _all_samples() -> Iterator[dict]:
            for bucket_id in bucket_ids:
                bucket = self._load_bucket(bucket_id)
                if bucket is None:
                    continue
                # Round-robin across sites (not a flat per-ID scan): see the
                # module docstring for why a flat scan would make most
                # batches near-homogeneous in site.
                site_gens = self._site_generators(bucket, rng)
                yield from _round_robin(site_gens)

        yield from self._shuffled(_all_samples(), rng)
