"""Construye y cachea las submuestras fijas (validation y train) usadas por
el resto de la auditoria."""
import sys, time
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import sample_windows

OUT = Path(__file__).resolve().parent / "out"
OUT.mkdir(exist_ok=True)

for split, nb, cps, seed in [("validation", 8, 25, 20260921), ("train", 4, 8, 777)]:
    f = OUT / f"sample_{split}.npz"
    if f.exists():
        print(f"{f} ya existe, se omite")
        continue
    t = time.time()
    s = sample_windows(split, n_buckets=nb, cells_per_site_per_bucket=cps, seed=seed)
    np.savez_compressed(f, **s)
    print(f"guardado {f} en {time.time()-t:.1f}s  ({f.stat().st_size/1e6:.0f} MB)")

# submuestra de train mas amplia (para la ablacion en GPU, audit/20)
f = OUT / "sample_train_big.npz"
if not f.exists():
    import time as _t
    t = _t.time()
    s = sample_windows("train", n_buckets=8, cells_per_site_per_bucket=20, seed=31337)
    np.savez(f, **s)
    print(f"guardado {f} en {_t.time()-t:.1f}s ({f.stat().st_size/1e6:.0f} MB)")
