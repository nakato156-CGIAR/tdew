"""Build the Word reference document the TAAC submission is rendered against.

The journal asks for a minimum 11 pt font, Times New Roman or Arial, 1.5 line spacing and
line numbers. Pandoc's stock reference document satisfies none of the three, and the font
is not settable from the Quarto front matter, so the docx is patched directly.

The patch goes in <w:docDefaults>, not in the Normal style: Normal carries no run
properties at all, and the font it inherits is a theme font, so overriding it there would
be ignored. Run this whenever pandoc's default changes; build_taac.py only consumes the
result.
"""
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "reference-taac.docx"
TMP = HERE / "_refdocx"


def main() -> int:
    subprocess.run(["quarto", "pandoc", "-o", OUT.name,
                    "--print-default-data-file", "reference.docx"], cwd=HERE, check=True)
    shutil.rmtree(TMP, ignore_errors=True)
    TMP.mkdir()
    with zipfile.ZipFile(OUT) as z:
        z.extractall(TMP)

    sty = TMP / "word" / "styles.xml"
    x = sty.read_text(encoding="utf-8")
    # Times New Roman in place of the theme font, at 12 pt.
    x, n_font = re.subn(
        r'<w:rFonts w:asciiTheme="minorHAnsi"[^/]*/>',
        '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" '
        'w:eastAsia="Times New Roman" w:cs="Times New Roman"/>', x, count=1)
    # 1.5 line spacing: 360 twentieths of a point against a 240 single-spaced line.
    x, n_space = re.subn(r'(<w:pPrDefault>\s*<w:pPr>)',
                         r'\1<w:spacing w:line="360" w:lineRule="auto"/>', x, count=1)
    assert n_font == 1 and n_space == 1, f"font {n_font}, spacing {n_space}"
    sty.write_text(x, encoding="utf-8")

    doc = TMP / "word" / "document.xml"
    d = doc.read_text(encoding="utf-8")
    d, n_ln = re.subn(r"<w:sectPr",
                      '<w:sectPr><w:lnNumType w:countBy="1" w:restart="continuous" '
                      'w:distance="360"/>', d, count=1)
    assert n_ln == 1
    doc.write_text(d, encoding="utf-8")

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(TMP.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(TMP))
    shutil.rmtree(TMP)
    print(f"wrote {OUT.name}: Times New Roman 12 pt, 1.5 spacing, continuous line numbers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
