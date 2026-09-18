"""Assemble the Theoretical and Applied Climatology submission from paper.qmd.

Two manuscripts from one body. paper.qmd is the working document and stays the
single source of the science; this script rearranges it into the structure a Springer
research journal expects and adds the parts a journal submission needs and a working
draft does not: a conclusions section, the declarations block, keywords.

What changes, and why:

  * Order. Springer expects Introduction, Data and methods, Results, Discussion,
    Conclusions. Limitations becomes a subsection of Discussion rather than a section of
    its own, which is where a reviewer will look for it.
  * Supplementary material leaves the body. Springer takes it as Electronic Supplementary
    Material in a separate file, so it is written to its own document.
  * The internal apparatus goes. The draft banner and the sign-off table are ours, for
    tracking validation before submission; they are not part of a manuscript.
  * AI use is not dropped but moved, into Declarations, where a publisher expects to find
    it rather than as a section of the paper.
  * References switch to Springer basic author-date.

Run from reports/paper/:  python3 build_taac.py
"""
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "paper.qmd"
OUT = HERE / "paper_taac.qmd"
ESM = HERE / "paper_taac_esm.qmd"


def sections(text: str) -> dict:
    lines = text.split("\n")
    heads = [(i, l) for i, l in enumerate(lines) if l.startswith("## ")]
    out = {}
    for k, (i, l) in enumerate(heads):
        end = heads[k + 1][0] if k + 1 < len(heads) else len(lines)
        out[re.sub(r"\s*\{.*\}$", "", l[3:]).strip()] = "\n".join(lines[i + 1:end]).strip("\n")
    return out


def demote(body: str) -> str:
    """### -> #### so a former section can sit inside Discussion."""
    return re.sub(r"^### ", "#### ", body, flags=re.M)


FRONT = """---
title: "Extending the PISCO gridded dew-point record for Peru (2017--2020) from the continued minimum-temperature record, using per-climate-zone seasonal model selection"
date: last-modified
bibliography: references.bib
csl: springer-basic-author-date.csl
crossref:
  fig-title: "Fig."
  fig-prefix: "Fig."
  tbl-title: "Table"
  tbl-prefix: "Table"
format:
  typst:
    toc: false
    number-sections: true
    papersize: a4
    margin: {x: 2.5cm, y: 2.5cm}
    include-in-header: taac_format.typ
---

"""

TITLE_PAGE = """
::: {.content-visible}
**Piero Palacios**^1^\\*  ·  **Henry Juarez**^1^

^1^ International Potato Center (CIP), Lima, Peru

\\* Corresponding author. piero.palacios@cgiar.org

ORCID: [TODO: add the 16-digit ORCID of each author.]
:::

**Acknowledgments.** [TODO: acknowledge people, grants and funds here; the guidelines
require this on the title page, and funding organizations must be written in full.]

**Author contributions.** [TODO: confirm with the co-author before submission.] Both authors
conceived the study. PP implemented the method, ran the analyses and drafted the manuscript.
HJ contributed to the design and to the interpretation of results. Both authors read and
approved the final manuscript.

\\newpage
"""

ABSTRACT = """
The PISCO gridded climate product for Peru provides daily dew-point temperature through 2016,
while its minimum-temperature record extends to 2020, leaving a four-year gap in a variable
required for reference-evapotranspiration, disease-risk and crop models. We reconstruct dew point
for 2017--2020 by learning the minimum-temperature to dew-point mapping on the 1981--2016 overlap
and applying it forward at every grid cell. The model is a weighted local linear regression on
climate anomalies, fitted per cell and day of year, with the predictor subset and the day-of-year
smoothing bandwidth selected jointly for each climate zone and day of year by leave-one-year-out
cross-validation. Because no observed dew point exists in the gap, reconstruction is
autoregressive: each predicted day supplies the dew-point lags of subsequent days.

Validation withholds the four most recent years and scores against observation under the same
autoregressive conditions the real gap imposes, with selection confined to the training years.
Within the domain where the source product is constrained by stations, the model attains a
root-mean-square error of 0.946 °C at a skill score of 0.251 against daily climatology, the
incumbent choice for gap filling, and a bias of +0.010 °C. Accuracy degrades monotonically with
distance from that domain, reaching 1.724 °C beyond 200 km, so the reconstruction is released with
a per-cell distance to it. The conventional arid-region correction to the FAO-56 approximation
increases error here in every moisture class, including the arid classes for which it was devised.
"""

CONCLUSIONS = """
## Conclusions

The minimum-temperature record for Peru continues four years beyond the dew-point record it is
paired with, and that asymmetry is enough to reconstruct the missing years. Learning the
$T_{\\min} \\rightarrow T_d$ mapping per grid cell and day of year, with the predictor subset and the
smoothing bandwidth chosen per climate zone and day of year, recovers dew point for 2017--2020 at
$0.946$ °C within the domain where the source product is station-constrained, against $1.264$ °C for
the daily climatology that gap filling would otherwise use.

Three findings generalise beyond this dataset.

The validation design matters more than the estimator. The task is extrapolation in time, so
spatial cross-validation, the prevailing choice for gridded products, measures the wrong thing:
withholding locations while retaining contemporaneous observations does not reproduce a setting in
which the target is unobserved everywhere. Withholding years and reconstructing them
autoregressively does, and selection must be confined to the training years or the result is
inflated, here by $0.009$ in skill.

The FAO-56 dew-point approximation does not improve under its own conventional correction over this
domain. Subtracting 2 °C in arid and semi-arid regions, the standard remedy, increases error in
every Thornthwaite moisture class including the arid ones, because gridded $T_d$ lies above
$T_{\\min}$ here rather than below it. The best single offset has the opposite sign. Corrections of
this kind should be re-estimated per product and region, not transferred.

Accuracy should be reported against observational support, not averaged over a domain. Error here
degrades monotonically with distance from the station network that constrains the source fields, from
$0.946$ °C inside it to $1.724$ °C beyond 200 km, and every physically implausible value in the
released field lies in the outer band. A single pooled figure conceals both facts. We therefore
release a per-cell distance to the classified domain alongside the field, and report accuracy by
distance band, so that a user can impose a support threshold appropriate to their application rather
than inherit ours.
"""

DECLARATIONS = """
## Statements and Declarations {.unnumbered}

**Funding.** [TODO: state the funding source, or "The authors did not receive support from any
organization for the submitted work."]

**Competing interests.** The authors declare no competing interests.

**Ethics approval.** Not applicable. This study involves no human participants, human data or
animals.

**Consent to participate / Consent for publication.** Not applicable.

**Data availability.** [TODO: deposit and cite the DOI.] The reconstructed dew-point field for
2017--2020, the per-cell support-distance layer, and the model coefficients will be deposited in a
public repository on acceptance. The source PISCO products are those of @huerta2022 and the climate
classification that of @senamhi2021.

**Code availability.** [TODO: cite the frozen release DOI.] The analysis code implementing model
selection, coefficient fitting, autoregressive reconstruction and the validation harness, together
with the scripts reproducing every figure and reported statistic, will be released publicly on
acceptance.

**Use of generative artificial intelligence.** See also Sect. 3.6, where the guidelines
require this to be documented.

**Detail.** The analysis pipeline, the figures and a first draft
of this manuscript were produced with the assistance of a large language model (Anthropic Claude)
under author direction. Every quantitative result reported here was computed by code the authors
reviewed, from the recorded outputs of the runs described, and the claim attributed to each cited
work was checked against the full text of that work, except where the bibliography notes otherwise.
The authors take full responsibility for the content.
"""


LLM_IN_METHODS = """
### Use of a large language model {#sec-llm}

The journal requires that use of a large language model be documented in the Methods. The analysis
pipeline described above, the figures, and a first draft of this manuscript were produced with the
assistance of a large language model (Anthropic Claude) under author direction. Every quantitative
result reported here was computed by code the authors reviewed, from the recorded outputs of the
runs described; the claim attributed to each cited work was checked against the full text of that
work, except where the bibliography notes otherwise. The model is not an author: authorship carries
accountability that cannot be assigned to it. The authors take full responsibility for the content.
"""



def place_bibliography_before_declarations() -> None:
    """Move the bibliography above Statements and Declarations, then recompile.

    The journal says the statements go "after the References section", but Quarto's Typst
    writer emits #bibliography() at the end of the document whatever the position of the
    #refs div, which would put the reference list last and the statements above it. The
    generated Typst is patched rather than the document restructured, because the document
    is right and only the renderer disagrees.

    Springer's own page is inconsistent here: its Competing Interests section says the
    declarations go *before* the reference list. We follow the dedicated Statements &
    Declarations section, which is the more specific instruction and also names the heading.
    """
    typ = HERE / "paper_taac.typ"
    if not typ.exists():
        print("no paper_taac.typ; skipping bibliography move")
        return
    t = typ.read_text()
    m = re.search(r"\n#set bibliography\([^\n]*\)\n+#bibliography\(\([^\n]*\)\)\s*$", t)
    marker = "#heading(level: 1, numbering: none)[Statements and Declarations]"
    if not m or marker not in t:
        print("bibliography or declarations marker not found; leaving output as rendered")
        return
    block = m.group(0).strip()
    t = t[:m.start()] + "\n"
    t = t.replace(marker, block + "\n\n" + marker)
    typ.write_text(t)
    subprocess.run(["quarto", "typst", "compile", "paper_taac.typ", "paper_taac.pdf"],
                   cwd=HERE, check=True)
    print("moved bibliography above Statements and Declarations")



def check_compliance() -> None:
    """Re-check the guideline requirements that are mechanically checkable.

    Not a substitute for reading the guidelines, but these are the ones that silently
    regress when the text is edited.
    """
    txt = subprocess.run(["pdftotext", "paper_taac.pdf", "-"],
                         capture_output=True, text=True, cwd=HERE).stdout
    rows = []

    words = len(re.sub(r"\$[^$]*\$", " x ", ABSTRACT).split())
    rows.append(("abstract 150-250 words", 150 <= words <= 250, f"{words}"))

    chars = len(txt.replace("\n", ""))
    rows.append(("<= 100,000 characters", chars <= 100_000, f"{chars:,}"))

    depth = max(len(h) for h in re.findall(r"^(#+) ", OUT.read_text(), re.M))
    rows.append(("<= 3 heading levels", depth <= 3, f"{depth}"))

    lines = len(re.findall(r"^\s*\d{1,3}\s+\S", txt, re.M))
    rows.append(("line numbers present", lines > 100, f"{lines}"))

    refs = txt.find("\nReferences"), txt.find("\nStatements and Declarations")
    rows.append(("declarations after references",
                 -1 not in refs and refs[0] < refs[1], ""))

    # Figures and tables must be cited in consecutive numerical order. A citation and a
    # caption both begin "Fig. 3", so a caption is only one that continues into a caption
    # body; we compare the order of first mention instead, which is what the rule is about.
    for kind, pat in (("figures", r"Fig\. (\d+)"), ("tables", r"Table (\d+)")):
        order, seen = [], set()
        for n in re.findall(pat, txt):
            if n not in seen:
                seen.add(n)
                order.append(int(n))
        rows.append((f"{kind} numbered consecutively", order == sorted(order), str(order)))

    # Internal sign-off annotations must not reach a submission. The placeholders in the
    # declarations are a different thing and use a different form, "[TODO: what to supply]",
    # so they are left alone: a reviewer never sees them because the author fills them first.
    leaked = re.findall(r"\*\*\[(?:SME|TODO)[^\]]*\]\*\*", OUT.read_text())
    rows.append(("no internal markers in prose", not leaked, f"{len(leaked)} found"))

    print("\n  Springer / TAAC guideline check")
    for name, ok, detail in rows:
        print(f"    {'PASS' if ok else 'FAIL'}  {name:<32} {detail}")
    print("    NOTE  submission requires .docx or LaTeX; this build is Typst by request")


def main() -> int:
    sec = sections(SRC.read_text())

    body = [
        FRONT,
        TITLE_PAGE,
        "## Abstract {.unnumbered}\n",
        ABSTRACT.strip(),
        "\n\n**Keywords** dew-point temperature · gap filling · gridded climate data · "
        "local regression · model selection · Peru\n",
        "\n## Introduction {#sec-intro}\n", sec["Introduction"],
        "\n## Data {#sec-data}\n", sec["Data"],
        "\n## Methods {#sec-methods}\n", sec["Methods"], LLM_IN_METHODS,
        "\n## Results {#sec-results}\n", sec["Results"],
        "\n## Discussion {#sec-discussion}\n", sec["Discussion"],
        "\n### Limitations {#sec-limitations}\n", demote(sec["Limitations"]),
        CONCLUSIONS,
        # "This should be placed after the References section", per the guidelines. Their
        # Competing Interests section says before it instead; the more specific instruction wins.
        "\n## References {.unnumbered}\n\n::: {#refs}\n:::\n",
        DECLARATIONS,
    ]
    text = "\n".join(body)

    # The draft banner is internal, and the supplement is now a separate file that the
    # journal calls an Online Resource.
    text = re.sub(r"::: \{\.callout-important\}.*?:::\n", "", text, flags=re.S)
    text = text.replace("@sec-supp-version", "Online Resource 1")
    text = text.replace("@sec-supp-compute", "Online Resource 1")
    OUT.write_text(text)

    supp = sec["Supplementary material"]
    # Cross-references into the main manuscript cannot resolve from a separate file.
    supp = supp.replace("@sec-results-validation", "Sect. 4.2 of the main manuscript")
    esm = (FRONT.replace(
        'title: "Extending',
        'title: "Online Resource 1 --- Extending')
        + "\n" + supp
        + "\n\n## References {.unnumbered}\n\n::: {#refs}\n:::\n")
    ESM.write_text(esm)

    for f in (OUT, ESM):
        print(f"wrote {f.name}: {len(f.read_text().splitlines())} lines")
    for f in (OUT, ESM):
        subprocess.run(["quarto", "render", f.name, "--to", "typst",
                        "-M", "keep-typ:true"], cwd=HERE, check=True)
    place_bibliography_before_declarations()
    check_compliance()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
