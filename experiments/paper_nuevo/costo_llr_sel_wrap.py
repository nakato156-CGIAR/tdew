"""Envoltorio de cronometraje (tdew-4w2): marca carga, seleccion y ajuste final de llr.main y llr_lags.main en el log
sin cambiar su computo. Uso: python experiments/paper_nuevo/costo_llr_sel_wrap.py <modulo> <args de main>."""
import importlib, logging, sys, time
sys.path.insert(0, "/home/cvelasquez/Code/tdew")
mod_name = sys.argv[1]; args = sys.argv[2:]
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("STAGE")
from experiments.llr_simple import llr as L
mod = importlib.import_module(mod_name)
orig_load = L.load_arrays
def load(*a, **k):
    log.info("CARGA_INI"); r = orig_load(*a, **k); log.info("CARGA_FIN"); return r
L.load_arrays = load
if mod is not L:
    pass
def wrap_best(f):
    def g(*a, **k):
        log.info("SELECCION_FIN"); return f(*a, **k)
    return g
L.best_cell = wrap_best(L.best_cell)
if mod is not L:
    mod.best_cell = L.best_cell
log.info("PROC_INI")
rc = mod.main(args)
log.info("PROC_FIN")
raise SystemExit(rc)
