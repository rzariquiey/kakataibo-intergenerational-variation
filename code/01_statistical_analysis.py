"""
Statistical analysis of intergenerational variation in Kakataibo switch-reference.

Study: From Clause-Chaining to Parataxis: Intergenerational Variation in Clause
       Linkage Strategies among Kakataibo Speakers (Pano, Peru)
Author: Roberto Zariquiey (Pontificia Universidad Católica del Perú)

Method: Non-parametric statistics
  - Kruskal-Wallis H test (3-group comparison)
  - Pairwise Mann-Whitney U tests with Bonferroni correction (α = 0.017)
  - Spearman rank correlations (age as continuous variable)
  - Effect sizes via rank-biserial correlation r

Data: matrizcompletavariacion.xlsx
  Groups:
    El1–El9  Elderly speakers   (ages 62–90)
    Ad1–Ad9  Adult speakers     (ages 37–55)
    Yo1–Yo9  Young speakers     (ages 18–23)

  Variables:
    type1    Switch-reference constructions type 1 (poorly embedded)
    type2    Switch-reference constructions type 2 (highly embedded)
    conn     Switch-reference markers on connectors and adverbials
    total_sr Total switch-reference markers (type1 + type2 + conn)
    ss       Same-subject constructions
    ds       Different-subject constructions
    other    Other (non-canonical) categories
    words    Orthographic word count
    sents    Number of sentences

Requirements: pandas, scipy, openpyxl
  pip install pandas scipy openpyxl
"""

import pandas as pd
import numpy as np
from scipy import stats

# ─── Configuration ────────────────────────────────────────────────────────────

DATA_PATH = "../data/matrizcompletavariacion.xlsx"
BONFERRONI_ALPHA = 0.05 / 3   # = 0.0167

# ─── Load data ────────────────────────────────────────────────────────────────

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="Hoja1")
    df = df.dropna(subset=["ID"])

    # Rename columns to short names
    df.columns = [
        "ID", "sex", "age", "home",
        "type1", "type2", "conn", "total_sr",
        "ss", "ds", "other", "words", "sents",
    ]

    # Assign generational group
    def assign_group(row):
        id_ = str(row["ID"])
        if id_.startswith("El"):
            return "Elderly"
        elif id_.startswith("Ad"):
            return "Adult"
        elif id_.startswith("Yo"):
            return "Young"
        return None

    df["group"] = df.apply(assign_group, axis=1)

    # Derived variables
    df["sr_rate"]       = df["total_sr"] / df["sents"]   # SR markers per sentence
    df["type2_rate"]    = df["type2"]    / df["sents"]   # Highly embedded per sentence

    return df


# ─── Descriptive statistics ────────────────────────────────────────────────────

def descriptive_stats(df: pd.DataFrame, variables: list[str]) -> pd.DataFrame:
    groups = ["Elderly", "Adult", "Young"]
    rows = []
    for var in variables:
        row = {"variable": var}
        for g in groups:
            sub = df[df["group"] == g][var]
            row[f"{g}_M"]   = round(sub.mean(), 2)
            row[f"{g}_SD"]  = round(sub.std(),  2)
            row[f"{g}_Med"] = round(sub.median(), 2)
        rows.append(row)
    return pd.DataFrame(rows)


# ─── Kruskal-Wallis tests ─────────────────────────────────────────────────────

def kruskal_wallis(df: pd.DataFrame, variables: list[str]) -> pd.DataFrame:
    results = []
    for var in variables:
        groups = [df[df["group"] == g][var].values for g in ["Elderly", "Adult", "Young"]]
        H, p = stats.kruskal(*groups)
        results.append({"variable": var, "H": round(H, 3), "p": round(p, 4),
                         "significant": p < 0.05})
    return pd.DataFrame(results)


# ─── Pairwise Mann-Whitney U tests ───────────────────────────────────────────

def mannwhitney_pairwise(df: pd.DataFrame, variables: list[str]) -> pd.DataFrame:
    pairs = [("Elderly", "Adult"), ("Elderly", "Young"), ("Adult", "Young")]
    results = []
    for var in variables:
        for g1, g2 in pairs:
            s1 = df[df["group"] == g1][var].values
            s2 = df[df["group"] == g2][var].values
            U, p = stats.mannwhitneyu(s1, s2, alternative="two-sided")
            n1, n2 = len(s1), len(s2)
            r = round(1 - (2 * U) / (n1 * n2), 3)   # rank-biserial correlation
            results.append({
                "variable": var,
                "comparison": f"{g1} vs {g2}",
                "U": U,
                "p": round(p, 4),
                "r": r,
                "significant_bonferroni": p < BONFERRONI_ALPHA,
            })
    return pd.DataFrame(results)


# ─── Spearman correlations ────────────────────────────────────────────────────

def spearman_correlations(df: pd.DataFrame, variables: list[str]) -> pd.DataFrame:
    results = []
    for var in variables:
        rho, p = stats.spearmanr(df["age"], df[var])
        results.append({
            "variable": var,
            "rho": round(rho, 3),
            "p": round(p, 4),
            "significant": p < 0.05,
        })
    return pd.DataFrame(results).sort_values("rho", key=abs, ascending=False)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    df = load_data(DATA_PATH)

    print(f"N = {len(df)} speakers")
    print(f"Age: M = {df['age'].mean():.1f}, SD = {df['age'].std():.1f}, "
          f"range {df['age'].min():.0f}–{df['age'].max():.0f}\n")

    for g in ["Elderly", "Adult", "Young"]:
        sub = df[df["group"] == g]
        print(f"{g:8s}: n={len(sub)}, age M={sub['age'].mean():.1f} "
              f"SD={sub['age'].std():.1f}, range {sub['age'].min():.0f}–{sub['age'].max():.0f}")

    VARS = ["total_sr", "type1", "type2", "conn", "ss", "ds", "sents", "sr_rate", "type2_rate"]

    print("\n" + "=" * 60)
    print("DESCRIPTIVE STATISTICS BY GENERATIONAL GROUP")
    print("=" * 60)
    desc = descriptive_stats(df, VARS)
    print(desc.to_string(index=False))

    print("\n" + "=" * 60)
    print("KRUSKAL-WALLIS TESTS (H, df=2)")
    print("=" * 60)
    kw = kruskal_wallis(df, VARS)
    print(kw.to_string(index=False))

    print("\n" + "=" * 60)
    print(f"PAIRWISE MANN-WHITNEY U TESTS (Bonferroni α = {BONFERRONI_ALPHA:.4f})")
    print("=" * 60)
    mw = mannwhitney_pairwise(df, ["total_sr", "type2", "type1", "conn", "sents", "sr_rate", "type2_rate"])
    print(mw.to_string(index=False))

    print("\n" + "=" * 60)
    print("SPEARMAN RANK CORRELATIONS WITH AGE")
    print("=" * 60)
    sp = spearman_correlations(df, VARS)
    print(sp.to_string(index=False))

    print("\n" + "=" * 60)
    print("SR RATE PER SENTENCE (normalized)")
    print("=" * 60)
    for g in ["Elderly", "Adult", "Young"]:
        sub = df[df["group"] == g]
        print(f"{g:8s}: SR/sent M={sub['sr_rate'].mean():.2f}  "
              f"type2/sent M={sub['type2_rate'].mean():.2f}  "
              f"sents M={sub['sents'].mean():.1f}")


if __name__ == "__main__":
    main()
