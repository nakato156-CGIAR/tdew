"""Build the observational-support distance layer released alongside the field.

The reconstruction covers a grid that extends well past Peru, because the gridded
predictors do. SENAMHI's station network, and therefore the kriging that produced the
source fields, stops at the national territory. Distance from that territory is the
physically meaningful measure of how well a cell is constrained; the border itself is not,
being a political line that no atmospheric process respects.

That distinction is testable, and the data settles it: the exceedance rate does not step at
the border. It is zero inside, still zero for the first 20 km outside, and then climbs
smoothly with distance. So we release the distance, and a tier derived from it, rather than
a nationality flag.

Writes
  $RES/tuning/support_distance.parquet   ID, lon, lat, dist_km, tier
and prints the tier statistics that justify the cuts.
"""
import glob
import os
import zipfile
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

RES = os.environ.get("RES", "/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning")
ZONE_ZIP = os.environ.get("ZONE_ZIP", str(Path.home() / "Downloads" / "clasif_clima_peru.zip"))
PRED = f"{RES}/tuning/predictions_2017_2020"
OUT = f"{RES}/tuning/support_distance.parquet"
WARM = 35.0

# Cuts in km from the classified domain. Chosen from the exceedance profile below, not
# from round numbers: the field is clean out to 50 km and degrades sharply past 100.
TIER_EDGES = [0.0, 50.0, 100.0, 200.0]
TIER_NAMES = ["within", "near", "marginal", "extrapolated", "unsupported"]


def domain_boundary_tree():
    """KD-tree over the boundary vertices of the dissolved classified domain."""
    import geopandas as gpd
    import shapely
    from shapely.ops import unary_union
    from scipy.spatial import cKDTree

    td = tempfile.mkdtemp()
    zipfile.ZipFile(ZONE_ZIP).extractall(td)
    g = gpd.read_file(next(Path(td).rglob("*.shp")))
    domain = unary_union(g.geometry.values).buffer(0)
    bnd = domain.boundary
    parts = bnd.geoms if hasattr(bnd, "geoms") else [bnd]
    coords = np.vstack([np.asarray(p.coords) for p in parts])
    return cKDTree(coords), domain, shapely


def _bucket_stats(args):
    """Per-bucket exceedance counts keyed by ID.

    Vectorised deliberately: a per-group apply over 8,192 buckets is minutes slower.
    """
    f, = args
    d = pd.read_parquet(f, columns=["ID", "TD_predicted"])
    d["warm"] = (d["TD_predicted"] > WARM).astype("int64")
    return d.groupby("ID")["warm"].agg(n="size", n_warm="sum")


def main() -> int:
    tree, domain, shapely = domain_boundary_tree()
    print(f"classified domain: {len(domain.geoms) if hasattr(domain, 'geoms') else 1} part(s)")

    zt = pd.read_parquet(f"{RES}/zone_table.parquet")
    files = sorted(glob.glob(f"{PRED}/id_bucket=*/pred.parquet"))
    print(f"scanning {len(files)} buckets of the released field ...")
    with ProcessPoolExecutor(12) as ex:
        stats = pd.concat(list(ex.map(_bucket_stats, [(f,) for f in files], chunksize=32)))
    stats = stats.groupby(level=0).sum()
    print(f"released field: {len(stats):,} cells, {int(stats['n'].sum()):,} values")

    m = zt[zt["ID"].isin(stats.index)].copy()
    xy = np.c_[m.lon.to_numpy(), m.lat.to_numpy()]
    dist, _ = tree.query(xy, workers=-1)
    pts = shapely.points(xy[:, 0], xy[:, 1])
    inside = shapely.contains(domain, pts)
    m["dist_km"] = np.where(inside, -1.0, 1.0) * dist * 111.32

    m["tier"] = pd.cut(m["dist_km"], [-np.inf] + TIER_EDGES + [np.inf],
                       labels=TIER_NAMES, right=False)

    j = m.set_index("ID").join(stats, how="inner")
    print("\n=== exceedance above 35 C by support tier, whole field ===")
    print(f"{'tier':>14} {'km from domain':>16} {'cells':>10} {'% of field':>11} "
          f"{'cells hit':>10} {'values >35 C':>13}")
    edges = ["< 0", "0-50", "50-100", "100-200", "> 200"]
    for name, rng in zip(TIER_NAMES, edges):
        s = j[j.tier == name]
        if not len(s):
            continue
        hit = int((s.n_warm > 0).sum())
        rate = 100 * s.n_warm.sum() / s.n.sum()
        print(f"{name:>14} {rng:>16} {len(s):>10,} {100*len(s)/len(j):>10.1f}% "
              f"{hit:>10,} {rate:>12.4f}%")

    out = m[["ID", "lon", "lat", "dist_km", "tier"]].copy()
    out["tier"] = out["tier"].astype(str)
    out.to_parquet(OUT, index=False)
    print(f"\nwrote {OUT}  ({len(out):,} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
