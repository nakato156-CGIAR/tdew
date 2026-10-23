"""Guardas del paper nuevo (reports/paper_nuevo/): variables, cifras a mano,
marcadores pendientes, includes, referencias cruzadas, citas y orden de secciones.

Los archivos se descubren dinamicamente: paper.qmd, suplemento.qmd y
secciones/*.qmd, mas los archivos de tablas/figuras que estos incluyen.

Test 3 (marcadores `[[FALTA` / `[[CITA`) falla mientras haya texto pendiente:
es intencional, no es xfail.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1] / "reports" / "paper_nuevo"

# --- Allowlist explicita y pequena para el detector de cifras (test 2) -------
# Tokens numericos que no son resultados: version de producto o parametro de
# diseno. Se comparan contra el token exacto (con "°" pegado si lo hay).
#   "3.0"   -> TimesFM 3.0 (version del modelo)
#   "0,01°" -> resolucion de la grilla PISCO
#   "2°"    -> tamano de bloque del bootstrap espacial
# (Tokens tipo "v1.1"/"v1.2" ya quedan fuera por el limite de palabra.)
NUM_ALLOWLIST = {"3.0", "0,01°", "2°", "v1.1", "v1.2"}


# --- Descubrimiento -----------------------------------------------------------
def source_files(root: Path = ROOT) -> list[Path]:
    files = [root / "paper.qmd", root / "suplemento.qmd"]
    files += sorted((root / "secciones").glob("*.qmd"))
    return [f for f in files if f.exists()]


INCLUDE_RE = re.compile(r"\{\{<\s*include\s+([^\s>]+)\s*>\}\}")


def includes_of(path: Path) -> list[str]:
    return INCLUDE_RE.findall(path.read_text(encoding="utf-8"))


def included_tables(root: Path = ROOT) -> list[Path]:
    out = []
    for f in source_files(root):
        for inc in includes_of(f):
            if not inc.startswith("secciones/"):
                out.append(root / inc)
    return out


# --- Limpieza de texto (conserva numeros de linea) ---------------------------
def _blank(m: re.Match) -> str:
    return re.sub(r"[^\n]", " ", m.group(0))


def strip_front_matter(text: str) -> str:
    m = re.match(r"---\n.*?\n---[ \t]*(?:\n|$)", text, flags=re.S)
    return text[: 0] + _blank(m) + text[m.end():] if m else text


def strip_code(text: str) -> str:
    """Quita comentarios HTML, bloques de codigo y code spans."""
    text = re.sub(r"<!--.*?-->", _blank, text, flags=re.S)
    text = re.sub(r"^(```+|~~~+).*?^\1[ \t]*$", _blank, text, flags=re.S | re.M)
    text = re.sub(r"`[^`\n]*`", _blank, text)
    return text


def strip_prose(text: str) -> str:
    """Deja solo prosa: sin front matter, comentarios, codigo, matematica,
    shortcodes, destinos de enlaces/imagenes, atributos ni citas."""
    text = strip_front_matter(text)
    text = strip_code(text)
    text = re.sub(r"\$\$.*?\$\$", _blank, text, flags=re.S)
    text = re.sub(r"\$[^$\n]+\$", _blank, text)
    text = re.sub(r"\{\{<.*?>\}\}", _blank, text, flags=re.S)
    text = re.sub(r"\]\([^)\n]*\)", lambda m: "]" + " " * (len(m.group(0)) - 1), text)
    text = re.sub(r"https?://\S+", _blank, text)
    text = re.sub(r"\{[^{}\n]*\}", _blank, text)
    text = re.sub(r"\[[^\]\n]*@[^\]\n]*\]", _blank, text)  # [@a; @b]
    text = re.sub(r"(?<![\w.])@[A-Za-z][\w:.-]*", _blank, text)  # @key, @fig-x
    return text


# --- Detector de cifras ------------------------------------------------------
TOKEN_RE = re.compile(r"(?<![\w.,])(\d+(?:[.,]\d+)*)(%|°)?(?!\w)")


def _is_year(tok: str) -> bool:
    return tok.isdigit() and len(tok) == 4 and 1900 <= int(tok) <= 2100


def find_numbers(text: str) -> list[tuple[int, str]]:
    """Devuelve (linea, token) de cifras sospechosas en prosa ya limpiada."""
    bad = []
    for ln, line in enumerate(text.splitlines(), 1):
        for m in TOKEN_RE.finditer(line):
            tok, suf = m.group(1), m.group(2) or ""
            full = tok + (suf if suf == "°" else "")
            if full in NUM_ALLOWLIST or tok in NUM_ALLOWLIST and suf != "%":
                continue
            if suf == "%" or re.search(r"[.,]", tok):
                bad.append((ln, tok + suf))
            elif not _is_year(tok) and int(tok) >= 10:
                bad.append((ln, tok + suf))
    return bad


# --- Variables ---------------------------------------------------------------
VAR_RE = re.compile(r"\{\{<\s*var\s+([^\s>]+)\s*>\}\}")


def resolve(variables: dict, key: str):
    node = variables
    for part in key.split("."):
        if not isinstance(node, dict) or part not in node:
            return KeyError
        node = node[part]
    return node


def all_text_files() -> list[Path]:
    return source_files() + [p for p in included_tables() if p.suffix == ".md" and p.exists()]


def test_variables_resolve_to_leaves_and_are_not_nd():
    variables = yaml.safe_load((ROOT / "_variables.yml").read_text(encoding="utf-8"))
    problems = []
    for f in all_text_files():
        text = strip_code(f.read_text(encoding="utf-8"))
        for ln, line in enumerate(text.splitlines(), 1):
            for key in VAR_RE.findall(line):
                val = resolve(variables, key)
                loc = f"{f.relative_to(ROOT)}:{ln} var {key}"
                if val is KeyError:
                    problems.append(f"{loc}: no existe en _variables.yml")
                elif isinstance(val, (dict, list)):
                    problems.append(f"{loc}: no es una hoja")
                elif str(val).strip().lower() in {"n. d.", "n.d.", "n. d", "nd"}:
                    problems.append(f"{loc}: vale 'n. d.'")
    assert not problems, "\n" + "\n".join(problems)


def test_no_hand_typed_numbers_in_prose():
    problems = []
    for f in source_files():
        clean = strip_prose(f.read_text(encoding="utf-8"))
        for ln, tok in find_numbers(clean):
            problems.append(f"{f.relative_to(ROOT)}:{ln}: {tok}")
    assert not problems, "Cifras escritas a mano (usar {{< var >}}):\n" + "\n".join(problems)


def test_no_pending_markers_FALTA_CITA_expected_to_fail_until_writers_finish():
    problems = []
    for f in source_files():
        for ln, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            for m in re.finditer(r"\[\[(FALTA|CITA)[^\]]*\]\]?", line):
                problems.append(f"{f.relative_to(ROOT)}:{ln}: {m.group(0)}")
    assert not problems, "Marcadores pendientes:\n" + "\n".join(problems)


# --- Includes, referencias cruzadas, citas ----------------------------------
ID_RE = re.compile(r"\{[^{}\n]*#((?:fig|tbl|sec|eq)-[\w:.-]+?)[\s}]")
REF_RE = re.compile(r"(?<![\w.])@((?:fig|tbl|sec|eq)-[\w:-]+)")
CITE_PREFIXES = ("fig-", "tbl-", "sec-", "eq-", "lst-", "thm-")


def test_included_files_and_figures_exist():
    missing = []
    for f in source_files():
        text = strip_code(f.read_text(encoding="utf-8"))
        for ln, line in enumerate(text.splitlines(), 1):
            for inc in INCLUDE_RE.findall(line):
                if not (ROOT / inc).exists():
                    missing.append(f"{f.relative_to(ROOT)}:{ln}: include {inc}")
            for m in re.finditer(r"!\[[^\]]*\]\(([^)\s]+)", line):
                tgt = m.group(1)
                if not re.match(r"[a-z]+://", tgt) and not (ROOT / tgt).exists():
                    missing.append(f"{f.relative_to(ROOT)}:{ln}: figura {tgt}")
    assert not missing, "\n" + "\n".join(missing)


def test_crossrefs_have_definitions():
    files = all_text_files()
    defined = set()
    for f in files:
        defined |= set(ID_RE.findall(strip_code(f.read_text(encoding="utf-8")) + " "))
    problems = []
    for f in source_files():
        clean = strip_front_matter(strip_code(f.read_text(encoding="utf-8")))
        clean = re.sub(r"\$\$.*?\$\$", _blank, clean, flags=re.S)
        clean = re.sub(r"\{\{<.*?>\}\}", _blank, clean, flags=re.S)
        for ln, line in enumerate(clean.splitlines(), 1):
            for ref in REF_RE.findall(line):
                if ref not in defined:
                    problems.append(f"{f.relative_to(ROOT)}:{ln}: @{ref} sin id")
    assert not problems, "\n" + "\n".join(problems)


def bib_keys() -> set[str]:
    return set(re.findall(r"^@\w+\{([^,\s]+),", (ROOT / "references.bib").read_text(encoding="utf-8"), flags=re.M))


def cited_keys(text: str) -> list[tuple[int, str]]:
    clean = strip_front_matter(strip_code(text))
    clean = re.sub(r"\$\$.*?\$\$", _blank, clean, flags=re.S)
    clean = re.sub(r"\$[^$\n]+\$", _blank, clean)
    clean = re.sub(r"\{\{<.*?>\}\}", _blank, clean, flags=re.S)
    clean = re.sub(r"https?://\S+", _blank, clean)
    out = []
    for ln, line in enumerate(clean.splitlines(), 1):
        for m in re.finditer(r"(?<![\w.])@([A-Za-z][\w:-]*)", line):
            key = m.group(1).rstrip(":-")
            if not key.startswith(CITE_PREFIXES):
                out.append((ln, key))
    return out


def test_citation_keys_exist_in_bib():
    keys = bib_keys()
    assert keys, "references.bib sin entradas"
    problems = []
    for f in source_files():
        for ln, key in cited_keys(f.read_text(encoding="utf-8")):
            if key not in keys:
                problems.append(f"{f.relative_to(ROOT)}:{ln}: @{key}")
    assert not problems, "Citas sin entrada en references.bib:\n" + "\n".join(problems)


def test_include_order_matches_sections():
    on_disk = sorted(p.name for p in (ROOT / "secciones").glob("[0-9][0-9]_*.qmd"))
    included = [Path(i).name for i in includes_of(ROOT / "paper.qmd") if i.startswith("secciones/")]
    assert included == on_disk, f"includes {included} != archivos {on_disk}"
    nums = [int(n[:2]) for n in on_disk]
    assert nums == list(range(0, 12)), f"numeracion de secciones {nums} no es 00..11"


# --- Autopruebas del detector (fixture sintetica) ----------------------------
def _scan(tmp_path, body: str):
    p = tmp_path / "x.qmd"
    p.write_text(body, encoding="utf-8")
    return find_numbers(strip_prose(p.read_text(encoding="utf-8")))


@pytest.mark.parametrize("body,expected", [
    ("El RMSE fue 1,12 en el dominio.\n", ["1,12"]),
    ("Mejora de 3.5 puntos.\n", ["3.5"]),
    ("Gana en 45% de celdas.\n", ["45%"]),
    ("Hay 24.876.447 filas.\n", ["24.876.447"]),
    ("Se usaron 17 zonas.\n", ["17"]),
    ("Un año suelto 2150 y 1800.\n", ["2150", "1800"]),
])
def test_detector_positive(tmp_path, body, expected):
    assert [t for _, t in _scan(tmp_path, body)] == expected


@pytest.mark.parametrize("body", [
    "---\ntitle: 'v 12,5 y 99'\n---\nTexto.\n",
    "<!-- 12,5 y 99% -->\nTexto.\n",
    "Se usa `12,5` y\n```python\nx = 99.5\n```\nfin.\n",
    "Vale $x = 12,5$ y $$y = 99$$.\n",
    "RMSE {{< var rmse.tuned >}} y {{< include tablas/s1.md >}}.\n",
    "Ver [texto](https://a.org/12.5/99) y ![f](figuras/fig12.png){#fig-a width=80%}.\n",
    "Segun [@das2024, p. 12; @woo2024] y @ansari2024 y @fig-a2 y @tbl-s10.\n",
    "Periodo 2009–2012 y 1981-2008, año 2020.\n",
    "TimesFM 3.0, v1.1, v1.2, grilla de 0,01° y bloques de 2°.\n",
    "Cuatro años y ll4b, ERA5, S1, A3, Td(t+1), 9 celdas.\n",
])
def test_detector_negative(tmp_path, body):
    assert _scan(tmp_path, body) == []


def test_detector_reports_line_numbers(tmp_path):
    assert _scan(tmp_path, "uno\n\ndos 12 tres\n") == [(3, "12")]


def test_cite_and_ref_helpers():
    txt = "Ver @das2024, [@a-b; @c], mail a x@y.org, @fig-1 y @sec-z.\n"
    assert [k for _, k in cited_keys(txt)] == ["das2024", "a-b", "c"]
    assert REF_RE.findall(txt) == ["fig-1", "sec-z"]
