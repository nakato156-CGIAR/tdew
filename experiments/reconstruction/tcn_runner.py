"""Materialization, training and inference runner for reconstruction TCNs."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np
import pandas as pd
import torch
from torch.utils.data import default_collate

from experiments.tcn import checkpoint as checkpoint_io

from .data import AR_LAGS, add_td_targets, build_exogenous_features
from .protocol import Protocol, ProtocolSpec, horizon_year, require_protocol_access
from .tcn import ReconstructionTCNConfig, build_tcn
from .training import train_fixed_steps, train_steps

DYNAMIC_SETS = {
    "tmin": ("TMIN", "TMIN_anom", "sin_doy_1", "cos_doy_1"),
    "thermal": (
        "TMIN", "TMAX", "TMIN_anom", "TMAX_anom", "TEMP_mean", "DTR",
        "es_TMIN", "es_TMAX", "es_range", "sin_doy_1", "cos_doy_1",
        "sin_doy_2", "cos_doy_2",
    ),
}
STATIC_COLUMNS = ("DEM", "TDI", "longitude", "latitude")
TARGET_COLUMNS = ("sin_doy_1", "cos_doy_1", "LST_DAY", "LST_NIGHT")
REGION_INDEX = {"Costa": 0, "Sierra": 1, "Selva": 2}


@dataclass(frozen=True)
class TCNPreprocessor:
    dynamic_columns: tuple[str, ...]
    static_columns: tuple[str, ...]
    target_columns: tuple[str, ...]
    center: dict[str, float]
    scale: dict[str, float]
    fill: dict[str, float]
    td_center: float
    td_scale: float

    def normalize(self, frame: pd.DataFrame, columns: Sequence[str]) -> np.ndarray:
        arrays = []
        for column in columns:
            values = frame[column].fillna(self.fill[column]).to_numpy(dtype=np.float32)
            arrays.append((values - self.center[column]) / self.scale[column])
        return np.column_stack(arrays).astype(np.float32)

    def normalize_td(self, values: np.ndarray) -> np.ndarray:
        return ((np.asarray(values, dtype=np.float32) - self.td_center) / self.td_scale).astype(np.float32)

    def invert_td(self, values: np.ndarray) -> np.ndarray:
        return np.asarray(values, dtype=float) * self.td_scale + self.td_center

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for key in ("dynamic_columns", "static_columns", "target_columns"):
            payload[key] = list(payload[key])
        return payload

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "TCNPreprocessor":
        copy = dict(payload)
        for key in ("dynamic_columns", "static_columns", "target_columns"):
            copy[key] = tuple(copy[key])
        return cls(**copy)


class WindowStore:
    """Per-cell arrays used to create windows lazily instead of per-row objects."""

    def __init__(
        self,
        frame: pd.DataFrame,
        preprocessor: TCNPreprocessor,
        *,
        split: str,
        context_length: int,
        mode: str,
        rollout_days: int = 31,
    ) -> None:
        self.context_length = context_length
        self.mode = mode
        self.rollout_days = rollout_days
        self.cells: dict[int, dict[str, Any]] = {}
        self.by_department: dict[str, list[int]] = {}
        for location_id, group in frame.groupby("ID", sort=True):
            group = group.sort_values("date").reset_index(drop=True)
            candidate = np.flatnonzero(group["_split"].to_numpy() == split)
            if mode == "direct":
                positions = candidate[candidate >= context_length - 1]
            else:
                positions = candidate[:1] if split == "hidden" else candidate[::rollout_days]
                positions = np.asarray(
                    [
                        start for start in positions
                        if start >= max(context_length - 1, max(AR_LAGS))
                        and start + rollout_days <= len(group)
                        and np.all(group["_split"].iloc[start : start + rollout_days].to_numpy() == split)
                    ],
                    dtype=int,
                )
            positions = np.asarray(
                [pos for pos in positions if self._position_is_dense(group["date"], int(pos))], dtype=int
            )
            if positions.size == 0:
                continue
            department = str(group["department"].iloc[0])
            self.cells[int(location_id)] = {
                "dynamic": preprocessor.normalize(group, preprocessor.dynamic_columns),
                "static": preprocessor.normalize(group, preprocessor.static_columns),
                "target_cond": preprocessor.normalize(group, preprocessor.target_columns),
                "label": preprocessor.normalize_td(group["TD_anom"].to_numpy(dtype=float)),
                "region": REGION_INDEX[str(group["region"].iloc[0])],
                "department": department,
                "positions": positions,
            }
            self.by_department.setdefault(department, []).append(int(location_id))
        if not self.cells:
            raise ValueError(f"No eligible {split} TCN cells")

    def _position_is_dense(self, dates: pd.Series, position: int) -> bool:
        end = position if self.mode == "direct" else position + self.rollout_days - 1
        return _dense_window(dates, position - self.context_length + 1, end)

    def sample(self, location_id: int, position: int) -> dict[str, Any]:
        cell = self.cells[int(location_id)]
        start = position - self.context_length + 1
        common = {
            "static": torch.from_numpy(cell["static"][position]),
            "region": torch.tensor(cell["region"], dtype=torch.long),
            "department": cell["department"],
        }
        if self.mode == "direct":
            return {
                **common,
                "dynamic": torch.from_numpy(cell["dynamic"][start : position + 1]),
                "target_cond": torch.from_numpy(cell["target_cond"][position]),
                "label": torch.tensor(cell["label"][position], dtype=torch.float32),
            }
        end = position + self.rollout_days
        windows = np.stack(
            [cell["dynamic"][pos - self.context_length + 1 : pos + 1] for pos in range(position, end)]
        )
        return {
            **common,
            "dynamic_windows": torch.from_numpy(windows),
            "target_cond": torch.from_numpy(cell["target_cond"][position:end]),
            "initial_td_history": torch.from_numpy(cell["label"][position - max(AR_LAGS) : position]),
            "label": torch.from_numpy(cell["label"][position:end]),
        }


class BalancedWindowBatches:
    def __init__(self, store: WindowStore, *, batch_size: int, n_batches: int, seed: int):
        self.store, self.batch_size, self.n_batches, self.seed = store, batch_size, n_batches, seed

    def __iter__(self):
        rng = np.random.default_rng(self.seed)
        departments = sorted(self.store.by_department)
        quota = max(1, self.batch_size // len(departments))
        for _ in range(self.n_batches):
            samples = []
            for department in departments:
                cells = np.asarray(self.store.by_department[department], dtype=int)
                chosen = rng.choice(cells, size=quota, replace=len(cells) < quota)
                for location_id in chosen:
                    positions = self.store.cells[int(location_id)]["positions"]
                    position = int(positions[int(rng.integers(0, len(positions)))])
                    samples.append(self.store.sample(int(location_id), position))
            yield default_collate(samples)


class SequentialWindowBatches:
    def __init__(self, store: WindowStore, *, batch_size: int):
        self.store, self.batch_size = store, batch_size

    def __iter__(self):
        batch = []
        for location_id in sorted(self.store.cells):
            for position in self.store.cells[location_id]["positions"]:
                batch.append(self.store.sample(location_id, int(position)))
                if len(batch) == self.batch_size:
                    yield default_collate(batch)
                    batch = []
        if batch:
            yield default_collate(batch)


def dynamic_columns(frame: pd.DataFrame, feature_set: str) -> tuple[str, ...]:
    if feature_set in DYNAMIC_SETS:
        return tuple(column for column in DYNAMIC_SETS[feature_set] if column in frame)
    if feature_set != "exogenous_full":
        raise ValueError(f"Unknown TCN feature set: {feature_set}")
    rolling = tuple(
        column for column in frame
        if column.startswith(("TMIN_", "TMAX_", "DTR_"))
        and any(token in column for token in ("lag", "mean_", "std_", "slope_"))
    )
    return tuple(dict.fromkeys(DYNAMIC_SETS["thermal"] + rolling))


def fit_preprocessor(train: pd.DataFrame, feature_set: str) -> TCNPreprocessor:
    dynamic = dynamic_columns(train, feature_set)
    static = tuple(column for column in STATIC_COLUMNS if column in train)
    target = tuple(column for column in TARGET_COLUMNS if column in train)
    columns = tuple(dict.fromkeys(dynamic + static + target))
    center, scale, fill = {}, {}, {}
    for column in columns:
        values = train[column].dropna().to_numpy(dtype=float)
        if values.size == 0:
            raise ValueError(f"No training values for {column}")
        fill[column] = float(np.median(values))
        center[column] = float(values.mean())
        std = float(values.std(ddof=0))
        scale[column] = std if std > 0 else 1.0
    td = train["TD_anom"].dropna().to_numpy(dtype=float)
    td_center = float(td.mean())
    td_std = float(td.std(ddof=0))
    return TCNPreprocessor(dynamic, static, target, center, scale, fill, td_center, td_std if td_std > 0 else 1.0)


def prepare_frame(
    canonical: pd.DataFrame, spec: ProtocolSpec, *, cache_path: Path | None = None
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Build the featured panel, reusing a cached copy when one is given.

    The rolling statistics cost tens of minutes on a full panel and depend only
    on the canonical rows and the protocol, so a screening sweep over context
    lengths or seeds can reuse a single materialization per fold.
    """
    if cache_path is not None and cache_path.is_file():
        combined = pd.read_parquet(cache_path)
    else:
        featured = build_exogenous_features(canonical, spec)
        train, hidden = add_td_targets(featured, spec)
        combined = pd.concat([train.assign(_split="train"), hidden.assign(_split="hidden")], ignore_index=True)
        combined = combined.sort_values(["ID", "date"]).reset_index(drop=True)
        if cache_path is not None:
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            staging = cache_path.with_name(f"{cache_path.name}.partial")
            combined.to_parquet(staging, index=False)
            staging.replace(cache_path)
    splits = combined["_split"].to_numpy()
    return combined, combined[splits == "train"].copy(), combined[splits == "hidden"].copy()


def run_tcn(
    canonical: pd.DataFrame,
    *,
    protocol: Protocol | str,
    mode: str,
    feature_set: str,
    seed: int,
    output_path: Path,
    checkpoint: Path | None,
    context_length: int,
    max_steps: int,
    eval_every: int,
    batch_size: int,
    patience: int = 5,
    num_workers: int,
    learning_rate: float,
    objective: str,
    unlock_ll4: bool,
    device: str | None,
    feature_cache: Path | None = None,
) -> pd.DataFrame:
    spec = require_protocol_access(protocol, unlock_ll4=unlock_ll4)
    if spec.name is Protocol.LL4 and checkpoint is None:
        raise PermissionError("ll4 refit requires the frozen checkpoint selected on dev_a/dev_b")
    if spec.name is Protocol.PRODUCTION and checkpoint is None:
        raise PermissionError("production refit requires the approved ll4 checkpoint")
    if checkpoint is not None and spec.name in (Protocol.LL4, Protocol.PRODUCTION) and not checkpoint.is_file():
        raise FileNotFoundError(f"Frozen checkpoint does not exist or is not a file: {checkpoint}")
    torch.manual_seed(seed)
    np.random.seed(seed)
    resolved_device = torch.device(device or ("cuda" if torch.cuda.is_available() else "cpu"))
    frame, train, hidden = prepare_frame(canonical, spec, cache_path=feature_cache)

    frozen_payload = checkpoint_io.load_checkpoint(checkpoint) if checkpoint is not None and checkpoint.is_file() else None
    saved = frozen_payload["config"] if frozen_payload is not None else None
    inference_only = saved is not None and saved.get("protocol") == spec.name.value

    if inference_only:
        mode = str(saved["mode"])
        feature_set = str(saved["feature_set"])
        preprocessor = TCNPreprocessor.from_dict(saved["preprocessor"])
        model_config = ReconstructionTCNConfig(**saved["model_config"])
        context_length = int(saved["context_length"])
        model = build_tcn(model_config).to(resolved_device)
        checkpoint_io.restore_into(frozen_payload, model=model, restore_rng=False)
        checkpoint_used = checkpoint
    else:
        if saved is not None:
            context_length = int(saved["context_length"])
            feature_set = str(saved["feature_set"])
            mode = str(saved["mode"])
            objective = str(saved.get("objective", objective))
            batch_size = int(saved.get("batch_size", batch_size))
            learning_rate = float(saved.get("learning_rate", learning_rate))
            max_steps = int(frozen_payload["global_step"])
            model_config = ReconstructionTCNConfig(**saved["model_config"])
        else:
            model_config = None
        preprocessor = fit_preprocessor(train, feature_set)
        if model_config is None:
            model_config = ReconstructionTCNConfig(
                n_dynamic_features=len(preprocessor.dynamic_columns),
                n_static_features=len(preprocessor.static_columns),
                n_target_features=len(preprocessor.target_columns),
                autoregressive=mode == "recursive",
            )
        expected_dims = (
            len(preprocessor.dynamic_columns), len(preprocessor.static_columns),
            len(preprocessor.target_columns), mode == "recursive",
        )
        actual_dims = (
            model_config.n_dynamic_features, model_config.n_static_features,
            model_config.n_target_features, model_config.autoregressive,
        )
        if expected_dims != actual_dims:
            raise ValueError(f"Frozen TCN configuration {actual_dims} does not match refit data {expected_dims}")
        model = build_tcn(model_config).to(resolved_device)
        train_store = WindowStore(
            frame, preprocessor, split="train", context_length=context_length, mode=mode
        )
        # The directory is named after the output artifact so two runs that
        # differ only in their schedule (steps, eval_every) cannot share it and
        # resume from each other.
        run_dir = output_path.parent / "checkpoints" / output_path.stem
        checkpoint_dir = checkpoint if checkpoint is not None else run_dir
        if checkpoint_dir.is_file():
            checkpoint_dir = run_dir.with_name(f"{run_dir.name}_refit")
        optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
        config_payload = {
            "preprocessor": preprocessor.to_dict(), "model_config": asdict(model_config),
            "context_length": context_length, "feature_set": feature_set,
            "protocol": spec.name.value, "seed": seed,
            "selected_steps": max_steps, "eval_every": eval_every, "patience": patience,
            "batch_size": batch_size, "learning_rate": learning_rate,
            "selected_from_checkpoint": str(checkpoint) if frozen_payload is not None else None,
        }
        if frozen_payload is not None:
            train_loader = BalancedWindowBatches(
                train_store, batch_size=batch_size, n_batches=max_steps, seed=seed,
            )
            checkpoint_used = train_fixed_steps(
                model, train_loader, optimizer=optimizer, checkpoint_dir=checkpoint_dir,
                config=config_payload, mode=mode, device=resolved_device,
                max_steps=max_steps, checkpoint_every=eval_every, objective=objective,
            )
        else:
            validation_store = WindowStore(
                frame, preprocessor, split="hidden", context_length=context_length, mode=mode,
                rollout_days=spec.horizon_days if mode == "recursive" else 31,
            )
            train_loader = BalancedWindowBatches(
                train_store, batch_size=batch_size, n_batches=max_steps, seed=seed,
            )
            # A recursive validation sample spans the complete 1,461-day
            # hidden block.  Keep those batches deliberately smaller to
            # bound host and accelerator memory while preserving continuity.
            validation_batch_size = min(batch_size, 32) if mode == "recursive" else batch_size
            validation_loader = SequentialWindowBatches(validation_store, batch_size=validation_batch_size)
            train_steps(
                model, train_loader, validation_loader, optimizer=optimizer,
                checkpoint_dir=checkpoint_dir, config=config_payload,
                mode=mode, device=resolved_device, max_steps=max_steps,
                eval_every=eval_every, patience=patience, objective=objective, resume="auto",
            )
            checkpoint_used = checkpoint_dir / "best.pt"
        best = checkpoint_io.load_checkpoint(checkpoint_used)
        checkpoint_io.restore_into(best, model=model, restore_rng=False)

    predictions = predict_hidden(
        model, frame, hidden, preprocessor, spec=spec, mode=mode,
        context_length=context_length, device=resolved_device, seed=seed,
        batch_size=batch_size,
    )
    predictions.attrs["checkpoint"] = str(checkpoint_used)
    predictions.attrs["device"] = str(resolved_device)
    predictions.attrs["mode"] = mode
    predictions.attrs["feature_set"] = feature_set
    predictions.attrs["trained"] = not inference_only
    return predictions


@torch.no_grad()
def predict_hidden(
    model: torch.nn.Module,
    frame: pd.DataFrame,
    hidden: pd.DataFrame,
    preprocessor: TCNPreprocessor,
    *,
    spec: ProtocolSpec,
    mode: str,
    context_length: int,
    device: torch.device,
    seed: int,
    batch_size: int = 1024,
) -> pd.DataFrame:
    model.eval()
    rows = []
    records = []
    for location_id, group in frame.groupby("ID", sort=True):
        group = group.sort_values("date").reset_index(drop=True)
        positions = np.flatnonzero(group["_split"].to_numpy() == "hidden")
        if len(positions) == 0:
            continue
        records.append(
            {
                "ID": int(location_id), "frame": group, "positions": positions,
                "dynamic": preprocessor.normalize(group, preprocessor.dynamic_columns),
                "static": preprocessor.normalize(group, preprocessor.static_columns),
                "target_cond": preprocessor.normalize(group, preprocessor.target_columns),
                "labels": preprocessor.normalize_td(group["TD_anom"].to_numpy(dtype=float)),
                "region": REGION_INDEX[str(group["region"].iloc[0])],
            }
        )
    for chunk_start in range(0, len(records), batch_size):
        chunk = records[chunk_start : chunk_start + batch_size]
        horizon = len(chunk[0]["positions"])
        hidden_dates = chunk[0]["frame"].iloc[chunk[0]["positions"]]["date"].to_numpy()
        for record in chunk[1:]:
            dates = record["frame"].iloc[record["positions"]]["date"].to_numpy()
            if len(dates) != horizon or not np.array_equal(dates, hidden_dates):
                raise ValueError("TCN batched inference requires aligned hidden calendars")
        first_positions = np.asarray([record["positions"][0] for record in chunk], dtype=int)
        histories = None
        if mode == "recursive":
            histories = np.stack(
                [record["labels"][pos - max(AR_LAGS) : pos] for record, pos in zip(chunk, first_positions)]
            )
            if not np.isfinite(histories).all():
                raise ValueError("Recursive rollout lacks finite pre-hidden TD history")
        chunk_predictions = np.empty((len(chunk), horizon), dtype=np.float32)
        regions = torch.tensor([record["region"] for record in chunk], dtype=torch.long, device=device)
        static = torch.from_numpy(
            np.stack([record["static"][pos] for record, pos in zip(chunk, first_positions)])
        ).to(device)
        for day in range(horizon):
            positions = [int(record["positions"][day]) for record in chunk]
            dynamic = torch.from_numpy(
                np.stack(
                    [record["dynamic"][pos - context_length + 1 : pos + 1] for record, pos in zip(chunk, positions)]
                )
            ).to(device)
            target = torch.from_numpy(
                np.stack([record["target_cond"][pos] for record, pos in zip(chunk, positions)])
            ).to(device)
            if mode == "recursive":
                assert histories is not None
                lag_values = torch.from_numpy(
                    np.stack([histories[:, -lag] for lag in AR_LAGS], axis=1).astype(np.float32)
                ).to(device)
                target = torch.cat([target, lag_values], dim=1)
            prediction = model(dynamic, static, regions, target).detach().cpu().numpy().astype(np.float32)
            chunk_predictions[:, day] = prediction
            if histories is not None:
                histories = np.concatenate([histories, prediction[:, None]], axis=1)
        anomalies = preprocessor.invert_td(chunk_predictions)
        for cell_index, record in enumerate(chunk):
            for day, pos in enumerate(record["positions"]):
                row = record["frame"].iloc[int(pos)]
                rows.append(
                    {
                        "ID": record["ID"], "department": row["department"], "date": row["date"],
                        "year_horizon": int(horizon_year(pd.Series([row["date"]]), spec).iloc[0]),
                        "TD_obs": row["TD"], "TD_clim": row["TD_clim"],
                        "TD_pred": float(anomalies[cell_index, day]) + float(row["TD_clim"]),
                        "model": f"tcn_{mode}", "seed": int(seed), "fold": spec.name.value,
                    }
                )
    result = pd.DataFrame(rows)
    if result.empty:
        raise ValueError("TCN produced no hidden predictions")
    return result


def _dense_window(dates: pd.Series, start: int, end: int) -> bool:
    if start < 0 or end >= len(dates):
        return False
    return pd.Timestamp(dates.iloc[end]) - pd.Timestamp(dates.iloc[start]) == pd.Timedelta(days=end - start)
