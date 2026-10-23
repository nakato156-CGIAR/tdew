"""Formato numerico en espanol: coma decimal, punto de miles, menos tipografico U+2212.

El redondeo es siempre "mitad hacia arriba" sobre la representacion decimal del dato
(no el redondeo bancario de `round`), para que 1,04625 -> "1,046" y 0,0055 -> "0,006".
"""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

MINUS = "−"
NBSP = " "
# Desde cuantas cifras enteras se agrupan los miles con punto. El texto narrativo escribe
# "1.092 celdas" y "2.000 replicas", es decir, desde 1.000; se sigue esa convencion.
MIN_MILES = 1000
_SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def _dec(x: float) -> Decimal:
    return Decimal(repr(float(x)))


def _redondear(x: float, nd: int) -> Decimal:
    return abs(_dec(x)).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP)


def _agrupar(entero: str) -> str:
    if int(entero) < MIN_MILES:
        return entero
    return f"{int(entero):,}".replace(",", ".")


def num(x: float, nd: int = 3, signo: bool = False) -> str:
    """Decimal en espanol. `signo=True` fuerza "+" o "−" (el signo sigue al dato original)."""
    if x is None:
        raise ValueError("num(None)")
    d = _redondear(x, nd)
    if d == 0 and float(x) != 0:
        # El redondeo borraria un valor distinto de cero ("−0,000"): se muestran mas decimales
        # hasta que aparezca la primera cifra significativa.
        while d == 0 and nd < 12:
            nd += 1
            d = _redondear(x, nd)
    ent, _, frac = f"{d:f}".partition(".")
    txt = _agrupar(ent) + ("," + frac if nd > 0 else "")
    if float(x) < 0:
        return MINUS + txt
    return ("+" + txt) if signo and float(x) > 0 else txt


def ent(n: float) -> str:
    """Entero con punto de miles (>= MIN_MILES)."""
    return num(round(float(n)), 0)


def ic(lo: float, hi: float, nd: int = 3) -> str:
    return f"[{num(lo, nd, True)}; {num(hi, nd, True)}]"


def sci(x: float, nd: int = 2) -> str:
    """Notacion cientifica con superindice Pandoc: 1,12 × 10^−8^."""
    d = _dec(x)
    exp = d.adjusted()
    mant = (d / Decimal(10) ** exp).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP)
    return f"{str(mant).replace('.', ',')} × 10^{str(exp).replace('-', '−')}^"


def seg_enteros(seg: float) -> int:
    return int(_dec(seg).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def dur(seg: float) -> str:
    """Duracion legible: "X s", "X min Y s" (hasta 3 h), "X h Y min" (hasta 72 h), "≈N,N dias"."""
    s = seg_enteros(seg)
    if s < 60:
        return f"{s} s"
    if s <= 3 * 3600:
        m, r = divmod(s, 60)
        return f"{m} min {r} s"
    if s < 72 * 3600:
        m_tot = int((Decimal(s) / 60).quantize(Decimal(1), rounding=ROUND_HALF_UP))
        h, m = divmod(m_tot, 60)
        return f"{h} h {m} min"
    return f"≈{num(s / 86400, 1)} días"


def horas(seg: float, nd: int = 1) -> str:
    return num(seg / 3600, nd)


def dias(seg: float, nd: int = 1) -> str:
    return num(seg / 86400, nd)

ND = "n. d."
