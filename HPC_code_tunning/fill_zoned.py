#!/usr/bin/env python3
"""HPC_code_tunning.fill_zoned — B3: the production gap-fill driver.

Runs the tuned autoregressive Td forecast (``forecast_zoned``) over **all** grid buckets
to produce the 2017-2020 gap-filled Td product, parallelised across buckets with a process
pool. Each bucket is fully independent — its inputs are read once and its ``pred.parquet``
is written in isolation (``forecast_bucket_zoned_from_disk``) — so the fan-out is a plain
map over buckets with no shared state. The numerical recursion is reused untouched (it is
pinned by ``tests/test_forecast_zoned.py``); this module only adds the CLI + parallelism.

Inputs (all under ``--base``, the tuning results root ``$RES``):
  * coeffs:      ``tuning/zoned_coeffs/id_bucket=XXXX/coeffs.parquet``   (B0)
  * climatology: ``climatology_by_bucket/id_bucket=XXXX/climatology.parquet``
  * history:     ``bucketed_training_data/id_bucket=XXXX/``  (seeds lags from history_end_year)
  * future TMIN: ``future_tmin_by_bucket/id_bucket=XXXX/``   (B2, exogenous horizon Tmin)

Output:
  * ``tuning/predictions_2017_2020/id_bucket=XXXX/pred.parquet``  (``[FECHA, ID, TD_predicted]``)

Example::

    python -m HPC_code_tunning.fill_zoned --base "$RES" \
        --pred-start 2017 --pred-end 2020 --history-end-year 2016 \
        --n-workers "$(nproc)" --overwrite
"""
from __future__ import annotations

import argparse
import logging
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from tdew_estimation.bucket_layout import discover_bucket_ids  # noqa: E402

from HPC_code_tunning.forecast_zoned import forecast_bucket_zoned_from_disk  # noqa: E402

log = logging.getLogger("fill_zoned")


def _default_roots(base: Path) -> dict:
    return {
        "coeffs_root": base / "tuning" / "zoned_coeffs",
        "climatology_root": base / "climatology_by_bucket",
        "prepared_training_root": base / "bucketed_training_data",
        "future_tmin_root": base / "future_tmin_by_bucket",
        "predictions_output_root": base / "tuning" / "predictions_2017_2020",
    }


def _fill_one(payload: dict) -> dict:
    """Worker: forecast a single bucket end-to-end (top-level so it is picklable)."""
    return forecast_bucket_zoned_from_disk(
        bucket_id=payload["bucket_id"],
        coeffs_root=payload["coeffs_root"],
        climatology_root=payload["climatology_root"],
        prepared_training_root=payload["prepared_training_root"],
        future_tmin_root=payload["future_tmin_root"],
        predictions_output_root=payload["predictions_output_root"],
        prediction_years=tuple(payload["prediction_years"]),
        history_end_year=payload["history_end_year"],
        overwrite=payload["overwrite"],
    )


def run_fill(
    *,
    base: Path,
    prediction_years: Tuple[int, int],
    history_end_year: int,
    n_workers: int = 1,
    overwrite: bool = False,
    bucket_ids: Optional[Sequence[int]] = None,
    roots: Optional[dict] = None,
) -> Counter:
    """Fan the per-bucket fill across a process pool; return a status Counter."""
    roots = roots or _default_roots(base)
    coeffs_root = Path(roots["coeffs_root"])
    buckets = (
        discover_bucket_ids(coeffs_root) if bucket_ids is None
        else sorted({int(b) for b in bucket_ids})
    )
    if not buckets:
        raise ValueError(f"No buckets found under {coeffs_root}")

    payloads = [
        {
            "bucket_id": int(b),
            "coeffs_root": str(roots["coeffs_root"]),
            "climatology_root": str(roots["climatology_root"]),
            "prepared_training_root": str(roots["prepared_training_root"]),
            "future_tmin_root": str(roots["future_tmin_root"]),
            "predictions_output_root": str(roots["predictions_output_root"]),
            "prediction_years": list(prediction_years),
            "history_end_year": int(history_end_year),
            "overwrite": bool(overwrite),
        }
        for b in buckets
    ]

    workers = max(1, min(n_workers, len(payloads)))
    log.info(
        "[fill] %d buckets over %d workers -> %s (pred %s, history_end=%d, overwrite=%s)",
        len(payloads), workers, roots["predictions_output_root"],
        prediction_years, history_end_year, overwrite,
    )

    status: Counter = Counter()
    rows_total = 0
    done = 0
    log_every = max(1, len(payloads) // 50)

    if workers == 1:
        for p in payloads:
            r = _fill_one(p)
            status[r.get("status", "error")] += 1
            rows_total += int(r.get("rows", 0))
            done += 1
            if done % log_every == 0 or done == len(payloads):
                log.info("[fill]   %d/%d buckets (%s)", done, len(payloads), dict(status))
    else:
        with ProcessPoolExecutor(max_workers=workers) as ex:
            futs = {ex.submit(_fill_one, p): p["bucket_id"] for p in payloads}
            for fut in as_completed(futs):
                b = futs[fut]
                try:
                    r = fut.result()
                except Exception as exc:  # noqa: BLE001 — one bad bucket must not abort
                    log.warning("[fill] bucket %s crashed: %s: %s", b, type(exc).__name__, exc)
                    status["error"] += 1
                else:
                    status[r.get("status", "error")] += 1
                    rows_total += int(r.get("rows", 0))
                done += 1
                if done % log_every == 0 or done == len(payloads):
                    log.info("[fill]   %d/%d buckets (%s)", done, len(payloads), dict(status))

    log.info("[fill] DONE: %d buckets, %d predicted rows, status=%s",
             len(payloads), rows_total, dict(status))
    return status


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="B3: parallel full-grid tuned Td gap-fill (2017-2020).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--base", required=True, type=Path, help="Tuning results root ($RES).")
    p.add_argument("--pred-start", type=int, default=2017)
    p.add_argument("--pred-end", type=int, default=2020)
    p.add_argument("--history-end-year", type=int, default=2016,
                   help="Year whose December seeds the autoregressive lags.")
    p.add_argument("--n-workers", type=int, default=1,
                   help="Process-pool workers across buckets (1 = sequential).")
    p.add_argument("--overwrite", action="store_true", help="Recompute buckets with an existing pred.parquet.")
    p.add_argument("--bucket-limit", type=int, default=None,
                   help="Only the first N buckets (smoke test).")
    p.add_argument("--bucket-ids", default=None,
                   help="Comma-separated explicit bucket ids (smoke test).")
    return p


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    args = build_parser().parse_args(argv)

    bucket_ids: Optional[List[int]] = None
    if args.bucket_ids:
        bucket_ids = [int(x) for x in args.bucket_ids.split(",") if x.strip() != ""]
    elif args.bucket_limit is not None:
        roots = _default_roots(args.base)
        all_b = discover_bucket_ids(Path(roots["coeffs_root"]))
        bucket_ids = all_b[: args.bucket_limit]

    status = run_fill(
        base=args.base,
        prediction_years=(args.pred_start, args.pred_end),
        history_end_year=args.history_end_year,
        n_workers=args.n_workers,
        overwrite=args.overwrite,
        bucket_ids=bucket_ids,
    )
    # Non-zero exit if nothing succeeded (all missing_inputs/error).
    return 0 if (status.get("ok", 0) + status.get("skipped", 0) + status.get("empty", 0)) > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
