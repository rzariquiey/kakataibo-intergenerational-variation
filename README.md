# Kakataibo Intergenerational Variation — Data & Code

**Study:** *From Clause-Chaining to Parataxis: Intergenerational Variation in Clause Linkage Strategies among Kakataibo Speakers (Pano, Peru) and its Implications for the Grammatical Description of Minority Languages*

**Authors:** Roberto Zariquiey (PUCP) · Mariana Poblete (PUCP) · Jorge Sato (UNIA) · Amelia Torres (UNIA)

---

## Overview

This repository contains the corpus data and analysis scripts for a quantitative study of intergenerational variation in the switch-reference (SR) and clause-linkage system of Kakataibo, a Panoan language spoken in the Peruvian Amazon. The study documents a systematic reduction in SR density and structural complexity across three generational cohorts — elderly, adult, and young speakers — consistent with a large-scale shift from clause-chaining to paratactic discourse organization.

All statistical analyses use fully non-parametric methods appropriate for small within-group samples (*n* = 9 per cohort): Kruskal-Wallis *H* tests, pairwise Mann-Whitney *U* tests with Bonferroni correction, and Spearman rank correlations.

---

## Repository structure

```
├── data/
│   ├── matrizcompletavariacion.xlsx   ← speaker corpus matrix (27 speakers × 13 variables)
│   └── transcripts/                   ← 27 Isakuna narratives in Transcriber XML format
│       ├── El1.txt … El9.txt          ← elderly speakers (age 62–90)
│       ├── Ad1.txt … Ad9.txt          ← adult speakers  (age 37–55)
│       └── Yo1.txt … Yo9.txt          ← young speakers  (age 18–23)
├── code/
│   ├── 01_statistical_analysis.py     ← all statistical tests (KW, MW, Spearman)
│   └── 02_generate_figures.py         ← figure generation (boxplots + scatter plots)
├── figures/
│   ├── fig1_map.png                   ← Figure 1: map of Kakataibo territory
│   ├── fig2_boxplots.png              ← Figure 2: SR variables by generational group
│   └── fig3_scatter.png               ← Figure 3: age vs. key variables (Spearman ρ)
├── CITATION.cff
├── LICENSE
└── requirements.txt
```

---

## Data

### Speaker matrix (`data/matrizcompletavariacion.xlsx`, sheet: Hoja1)

| Column | Description |
|--------|-------------|
| ID | Speaker code (El1–El9 = elderly; Ad1–Ad9 = adult; Yo1–Yo9 = young) |
| sex | M / F |
| age | Age in years |
| home | Community of residence |
| type1 | SR constructions type 1 — SR predicate immediately precedes the 2nd-position enclitic complex (poorly embedded) |
| type2 | SR constructions type 2 — SR predicate subordinated to another SR predicate (highly embedded) |
| conn | SR markers on lexicalized connectors and adverbials |
| total_sr | Sum of type1 + type2 + conn |
| ss | Same-subject SR constructions |
| ds | Different-subject SR constructions |
| other | Non-canonical SR categories |
| words | Orthographic word count |
| sents | Number of independent sentences |

Derived variables computed in the analysis scripts:
- `SR_rate` = total_sr / sents
- `SR_type2_rate` = type2 / sents

### Transcripts (`data/transcripts/`)

Each file is an Isakuna story narrative recorded in Kakataibo. Files follow the [Transcriber](http://trans.sourceforge.net/) XML format (`.txt`). Speaker codes in file names correspond to IDs in the matrix above. Data were collected in Yamino and at UNIA (Universidad Nacional Intercultural de la Amazonía) in 2017–2018.

---

## Statistical methods

| Test | Purpose | Correction |
|------|---------|------------|
| Kruskal-Wallis *H* (*df* = 2) | 3-group comparison | — |
| Mann-Whitney *U* (two-tailed) | Pairwise post-hoc | Bonferroni α = .017 |
| Spearman *ρ* | Age as continuous predictor | — |
| Rank-biserial *r* | Effect size for Mann-Whitney | — |

### Key results

| Variable | KW *H* | *p* | Spearman *ρ* |
|----------|--------|-----|-------------|
| SR_total | 22.60 | < .001 | .927 |
| Same-subject (SS) | 23.36 | < .001 | .894 |
| SR_type1 | 19.13 | < .001 | .858 |
| SR_type2 | 16.53 | < .001 | .814 |
| SR_rate | 17.96 | < .001 | .729 |
| SR_conn | 3.38 | .185 (n.s.) | .061 (n.s.) |

**Main finding:** SR density (SR_rate: elderly *M* = 2.59 vs. adult *M* = 0.50 vs. young *M* = 0.45) and structural complexity (SR_type2: elderly *M* = 9.56 vs. adult *M* = 1.11 vs. young *M* = 0.44) decrease dramatically across generations. SR_conn is the only variable that does not differ significantly across cohorts, suggesting that SR morphology on lexicalized connectors is preserved even as the more syntactically productive uses of the system are lost.

---

## How to reproduce

**Requirements:** Python 3.9+

```bash
pip install -r requirements.txt
```

**Step 1 — Statistical analysis**

```bash
cd code
python 01_statistical_analysis.py
```

Prints descriptive statistics, Kruskal-Wallis results, pairwise Mann-Whitney results (with effect sizes), and Spearman correlations to stdout.

**Step 2 — Figures**

```bash
python 02_generate_figures.py
```

Writes `fig2_boxplots.png` and `fig3_scatter.png` to `../figures/`.

---

## Citation

If you use this data or code, please cite:

```
Zariquiey, R., Poblete, M., Sato, J., & Torres, A. (2026). From Clause-Chaining
to Parataxis: Intergenerational Variation in Clause Linkage Strategies among
Kakataibo Speakers (Pano, Peru). [Data and code]. GitHub.
https://github.com/rzariquiey/kakataibo-intergenerational-variation
```

See also `CITATION.cff` for machine-readable citation metadata.

---

## License

- **Code** (`code/`): MIT License
- **Data** (`data/`): Creative Commons Attribution 4.0 International (CC BY 4.0)

See `LICENSE` for full terms.

---

## Contact

Roberto Zariquiey · rzariquiey@pucp.edu.pe · Pontificia Universidad Católica del Perú
