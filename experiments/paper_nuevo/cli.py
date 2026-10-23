"""CLI del paquete: ``uv run python -m experiments.paper_nuevo.cli {cifras,tablas,figuras,todo}``."""

from __future__ import annotations

import argparse
import logging
from collections.abc import Sequence


def main(argv: Sequence[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("que", choices=["cifras", "tablas", "figuras", "todo"])
    a = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(message)s")
    if a.que in ("cifras", "todo"):
        from experiments.paper_nuevo import cifras

        cifras.escribir()
    if a.que in ("tablas", "todo"):
        from experiments.paper_nuevo import tablas

        tablas.escribir()
    if a.que in ("figuras", "todo"):
        # Se importa solo al pedirlo: figuras.py y estilo.py los mantiene otro agente.
        from experiments.paper_nuevo import figuras

        figuras.generar_todas()


if __name__ == "__main__":
    main()
