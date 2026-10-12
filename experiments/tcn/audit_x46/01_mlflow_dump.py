"""Lee mlflow.db en SOLO LECTURA (sqlite URI ro) y vuelca params/metrics
de todos los runs del experimento tdew-week1."""
import sqlite3, sys, os, json
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / "mlflow.db"
uri = f"file:{DB.resolve()}?mode=ro"
con = sqlite3.connect(uri, uri=True)
cur = con.cursor()

print("=== experiments ===")
for row in cur.execute("select experiment_id, name, lifecycle_stage from experiments"):
    print(row)

print("\n=== runs ===")
runs = list(cur.execute(
    "select run_uuid, name, experiment_id, status, start_time, end_time, lifecycle_stage from runs order by start_time"))
for r in runs:
    print(r)

print("\n=== params por run ===")
for r in runs:
    rid = r[0]
    ps = dict(cur.execute("select key, value from params where run_uuid=?", (rid,)))
    print(f"\n-- run {rid} ({r[1]}) status={r[3]}")
    for k in sorted(ps):
        print(f"   {k} = {ps[k]}")
    tags = dict(cur.execute("select key, value from tags where run_uuid=?", (rid,)))
    for k in sorted(tags):
        if not k.startswith("mlflow.source"):
            print(f"   [tag] {k} = {tags[k]}")

print("\n=== metrics por run (todas las filas) ===")
for r in runs:
    rid = r[0]
    rows = list(cur.execute(
        "select key, step, value, timestamp from metrics where run_uuid=? order by key, step, timestamp", (rid,)))
    if not rows:
        continue
    print(f"\n-- run {rid} ({r[1]}) n_metric_rows={len(rows)}")
    for k, step, v, ts in rows:
        print(f"   {k:22s} step={step:4d} value={v!r} ts={ts}")
con.close()
