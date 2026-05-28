"""
Figure generation for the Kakataibo intergenerational variation study.

Produces:
  ../figures/fig1_boxplots.png   — Boxplots of all SR variables by generational group
  ../figures/fig2_scatter.png    — Scatter plots: age vs. 3 key variables (with Spearman ρ)

Requirements: pandas, scipy, matplotlib, openpyxl
  pip install pandas scipy matplotlib openpyxl
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

# ─── Configuration ────────────────────────────────────────────────────────────

DATA_PATH   = "../data/matrizcompletavariacion.xlsx"
OUTPUT_DIR  = "../figures"
DPI         = 150

GROUP_ORDER  = ["Elderly", "Adult", "Young"]
GROUP_LABELS = ["Elderly\n(62–90 yrs)", "Adult\n(37–55 yrs)", "Young\n(18–23 yrs)"]
COLORS       = ["#2166ac", "#fc8d59", "#1a9850"]

# ─── Load data ────────────────────────────────────────────────────────────────

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="Hoja1")
    df = df.dropna(subset=["ID"])
    df.columns = [
        "ID", "sex", "age", "home",
        "type1", "type2", "conn", "total_sr",
        "ss", "ds", "other", "words", "sents",
    ]

    def assign_group(row):
        id_ = str(row["ID"])
        if id_.startswith("El"):   return "Elderly"
        elif id_.startswith("Ad"): return "Adult"
        elif id_.startswith("Yo"): return "Young"

    df["group"]      = df.apply(assign_group, axis=1)
    df["sr_rate"]    = df["total_sr"] / df["sents"]
    df["type2_rate"] = df["type2"]    / df["sents"]
    return df


# ─── Figure 1: Boxplots ───────────────────────────────────────────────────────

def plot_boxplots(df: pd.DataFrame, output_path: str) -> None:
    variables = [
        ("total_sr",   "Total SR markers (SR_total)",             "(a)"),
        ("type1",      "Poorly embedded SR (SR_type1)",           "(b)"),
        ("type2",      "Highly embedded SR (SR_type2)",           "(c)"),
        ("conn",       "SR on connectors/adverbials (SR_conn)",   "(d)"),
        ("sents",      "Number of sentences",                     "(e)"),
        ("sr_rate",    "SR markers per sentence (SR_rate)",       "(f)"),
    ]

    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    fig.suptitle(
        "Switch-Reference Variables by Generational Group",
        fontsize=14, fontweight="bold", y=0.98,
    )

    for ax, (var, label, panel) in zip(axes.flatten(), variables):
        data = [df[df["group"] == g][var].values for g in GROUP_ORDER]
        bp = ax.boxplot(data, patch_artist=True, widths=0.6,
                        medianprops=dict(color="black", linewidth=2))
        for patch, color in zip(bp["boxes"], COLORS):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        ax.set_xticklabels(["Elderly", "Adult", "Young"], fontsize=10)
        ax.set_ylabel(label, fontsize=9)
        ax.set_title(panel, fontsize=10, fontweight="bold", loc="left")
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.savefig(output_path, dpi=DPI, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


# ─── Figure 2: Scatter plots (age vs variables) ───────────────────────────────

def plot_scatter(df: pd.DataFrame, output_path: str) -> None:
    scatter_vars = [
        ("total_sr",  "Total SR markers (SR_total)",           "ρ = 0.927, p < 0.001"),
        ("type2",     "Highly embedded SR (SR_type2)",          "ρ = 0.814, p < 0.001"),
        ("sr_rate",   "SR markers per sentence (SR_rate)",      "ρ = 0.729, p < 0.001"),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    fig.suptitle("Age vs. Switch-Reference Variables", fontsize=13, fontweight="bold")

    for ax, (var, ylabel, rho_text) in zip(axes, scatter_vars):
        for g, color in zip(GROUP_ORDER, COLORS):
            sub = df[df["group"] == g]
            ax.scatter(sub["age"], sub[var], color=color, s=65, alpha=0.85,
                       label=g, edgecolors="black", linewidths=0.5, zorder=3)

        # Linear trend line
        m, b, *_ = stats.linregress(df["age"], df[var])
        x_line = np.linspace(15, 95, 100)
        ax.plot(x_line, m * x_line + b, "k--", linewidth=1.2, alpha=0.6)

        ax.set_xlabel("Age (years)", fontsize=10)
        ax.set_ylabel(ylabel, fontsize=10)
        ax.set_title(rho_text, fontsize=9, style="italic")
        ax.grid(linestyle="--", alpha=0.4)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    handles = [mpatches.Patch(color=c, label=g) for g, c in zip(GROUP_ORDER, COLORS)]
    axes[0].legend(handles=handles, loc="upper left", fontsize=9, framealpha=0.8)

    plt.tight_layout()
    plt.savefig(output_path, dpi=DPI, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = load_data(DATA_PATH)

    plot_boxplots(df, os.path.join(OUTPUT_DIR, "fig1_boxplots.png"))
    plot_scatter(df,  os.path.join(OUTPUT_DIR, "fig2_scatter.png"))


if __name__ == "__main__":
    main()
