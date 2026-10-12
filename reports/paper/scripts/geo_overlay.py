"""Peru's national and departmental boundaries, for drawing over the map figures.

The outline is not decoration here. The reconstruction covers a rectangular grid about
twice the area of Peru, and accuracy degrades with distance from the Peruvian station
network that constrains the source product. Drawing the border makes that visible: a reader
can see at a glance that the part of the field with the largest errors, and every
implausible value in it, lies outside the territory the observations come from.

Departmental boundaries (GADM level 1) are drawn faintly so that regions named in the text
can be located. The national boundary is drawn heavily because it is the one that carries
the argument.

Source: GADM 4.1, level 1 for Peru, whose extent agrees with the SENAMHI classification
shapefile to three decimal places -- two independent sources on the same border.
"""
import os
from pathlib import Path

GEO = Path(__file__).resolve().parent.parent / "geo"
GADM = Path(os.environ.get("GADM_PER1", GEO / "gadm41_PER_1.json.zip"))

_cache: dict = {}


def _boundaries():
    """(departments, national outline) as shapely geometries, read once."""
    if "geom" not in _cache:
        import geopandas as gpd
        from shapely.ops import unary_union
        g = gpd.read_file(f"zip://{GADM}!gadm41_PER_1.json")
        _cache["geom"] = (g.geometry.values, unary_union(g.geometry.values).boundary)
    return _cache["geom"]


def add_peru_outline(ax, admin1: bool = True, national_lw: float = 0.9,
                     admin1_lw: float = 0.3, colour: str = "0.25",
                     alpha: float = 0.85) -> bool:
    """Draw the boundaries on a lon/lat axis, leaving its limits untouched.

    Returns False and draws nothing if the GADM file is absent, so that a figure still
    builds on a machine without it.
    """
    if not GADM.exists():
        return False
    depts, national = _boundaries()
    # Adding geometry would otherwise expand the axis to the whole country.
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    if admin1:
        for geom in depts:
            for part in (geom.geoms if hasattr(geom, "geoms") else [geom]):
                x, y = part.exterior.xy
                ax.plot(x, y, lw=admin1_lw, color=colour, alpha=alpha * 0.55,
                        zorder=5, solid_capstyle="round")
    for part in (national.geoms if hasattr(national, "geoms") else [national]):
        x, y = part.xy
        ax.plot(x, y, lw=national_lw, color=colour, alpha=alpha, zorder=6,
                solid_capstyle="round")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    return True
