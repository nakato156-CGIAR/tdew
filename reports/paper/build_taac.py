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
import json
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
author:
  - name: "Piero Palacios"
    affiliations:
      - name: "International Potato Center (CIP)"
        city: "Lima"
        country: "Peru"
    email: "piero.palacios@cgiar.org"
    attributes:
      corresponding: true
  - name: "Henry Juarez"
    affiliations:
      - name: "International Potato Center (CIP)"
        city: "Lima"
        country: "Peru"
    email: "h.juarez@cgiar.org"
date: last-modified
keywords:
  - dew-point temperature
  - gap filling
  - gridded climate data
  - local regression
  - model selection
  - Peru
bibliography: references.bib
csl: springer-basic-author-date.csl
format:
  typst:
    toc: false
    number-sections: true
    papersize: a4
    margin: {x: 2.5cm, y: 2.5cm}
    mainfont: "Libertinus Serif"
    fontsize: 11pt
---

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
## Declarations {.unnumbered}

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

**Author contributions.** [TODO: confirm with the co-author before submission.] Both authors
conceived the study. PP implemented the method, ran the analyses and drafted the manuscript. HJ
contributed to the design and to interpretation. Both authors read and approved the final
manuscript.

**Use of generative artificial intelligence.** The analysis pipeline, the figures and a first draft
of this manuscript were produced with the assistance of a large language model (Anthropic Claude)
under author direction. Every quantitative result reported here was computed by code the authors
reviewed, from the recorded outputs of the runs described, and the claim attributed to each cited
work was checked against the full text of that work, except where the bibliography notes otherwise.
The authors take full responsibility for the content.
"""


def main() -> int:
    sec = sections(SRC.read_text())

    body = [
        FRONT,
        "## Abstract {.unnumbered}\n",
        sec["Abstract"],
        "\n\n**Keywords** dew-point temperature · gap filling · gridded climate data · "
        "local regression · model selection · Peru\n",
        "\n## Introduction {#sec-intro}\n", sec["Introduction"],
        "\n## Data {#sec-data}\n", sec["Data"],
        "\n## Methods {#sec-methods}\n", sec["Methods"],
        "\n## Results {#sec-results}\n", sec["Results"],
        "\n## Discussion {#sec-discussion}\n", sec["Discussion"],
        "\n### Limitations {#sec-limitations}\n", demote(sec["Limitations"]),
        CONCLUSIONS,
        DECLARATIONS,
        "\n## References {.unnumbered}\n\n::: {#refs}\n:::\n",
    ]
    text = "\n".join(body)

    # The draft banner is internal; so is the pointer to a supplementary section that has
    # moved out of this document.
    text = re.sub(r"::: \{\.callout-important\}.*?:::\n", "", text, flags=re.S)
    text = text.replace("@sec-supp-version", "the Electronic Supplementary Material")
    text = text.replace("@sec-supp-compute", "the Electronic Supplementary Material")
    OUT.write_text(text)

    supp = sec["Supplementary material"]
    # Cross-references into the main manuscript cannot resolve from a separate file, so
    # they become prose pointers rather than dangling links.
    supp = supp.replace("@sec-results-validation", "Sect. 4.2 of the main manuscript")
    esm = (FRONT.replace(
        'title: "Extending',
        'title: "Electronic Supplementary Material --- Extending')
        .replace("toc: false", "toc: true")
        + "\n" + supp
        + "\n\n## References {.unnumbered}\n\n::: {#refs}\n:::\n")
    ESM.write_text(esm)

    for f in (OUT, ESM):
        print(f"wrote {f.name}: {len(f.read_text().splitlines())} lines")
    for f in (OUT, ESM):
        subprocess.run(["quarto", "render", f.name, "--to", "typst"], cwd=HERE, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
