"""
RQ 5.4.5 Plots: Correlation Comparison and AIC Comparison

Generates grouped bar charts comparing Full CTT vs Purified CTT
across congruence levels (Common, Congruent, Incongruent).
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Paths
DATA_DIR = Path("/home/etai/projects/REMEMVR/results/ch5/5.4.5/data")
PLOT_DIR = Path("/home/etai/projects/REMEMVR/results/ch5/5.4.5/plots")

def plot_correlation_comparison():
    """Generate grouped bar chart for CTT-IRT correlation comparison."""

    # Load data
    df = pd.read_csv(DATA_DIR / "step08_correlation_comparison_data.csv")

    # Prepare data for grouped bar chart
    dimensions = ["Common", "Congruent", "Incongruent"]
    x = np.arange(len(dimensions))
    width = 0.35

    # Extract values by CTT type
    full_vals = df[df["CTT_type"] == "Full"]["r_value"].values
    purified_vals = df[df["CTT_type"] == "Purified"]["r_value"].values

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create bars
    bars1 = ax.bar(x - width/2, full_vals, width, label="Full CTT", color="#4472C4", alpha=0.8)
    bars2 = ax.bar(x + width/2, purified_vals, width, label="Purified CTT", color="#ED7D31", alpha=0.8)

    # Reference line at r = 0.70 (adequate convergence)
    ax.axhline(y=0.70, color="gray", linestyle="--", linewidth=1, label="r = 0.70 (adequate)")

    # Labels and title
    ax.set_xlabel("Congruence Level", fontsize=12)
    ax.set_ylabel("Correlation with IRT Theta (r)", fontsize=12)
    ax.set_title("CTT-IRT Correlation by Congruence Level\n(Higher = Better Convergence)", fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(dimensions)
    ax.set_ylim(0.65, 0.95)
    ax.legend(loc="lower right")

    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax.annotate(f'{height:.3f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

    for bar in bars2:
        height = bar.get_height()
        ax.annotate(f'{height:.3f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

    # Add significance markers
    # From step05: Congruent and Incongruent are significant (p_bonf < 0.0167)
    ax.annotate('*', xy=(1, 0.89), fontsize=16, ha='center', fontweight='bold')
    ax.annotate('*', xy=(2, 0.91), fontsize=16, ha='center', fontweight='bold')
    ax.annotate('ns', xy=(0, 0.88), fontsize=10, ha='center', color='gray')

    plt.tight_layout()
    plt.savefig(PLOT_DIR / "correlation_comparison.png", dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Saved: {PLOT_DIR / 'correlation_comparison.png'}")


def plot_aic_comparison():
    """Generate grouped bar chart for LMM AIC comparison."""

    # Load data
    df = pd.read_csv(DATA_DIR / "step08_aic_comparison_data.csv")

    # Prepare data for grouped bar chart
    dimensions = ["Common", "Congruent", "Incongruent"]
    x = np.arange(len(dimensions))
    width = 0.35

    # Extract values by CTT type
    full_vals = df[df["CTT_type"] == "Full"]["AIC"].values
    purified_vals = df[df["CTT_type"] == "Purified"]["AIC"].values

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create bars
    bars1 = ax.bar(x - width/2, full_vals, width, label="Full CTT", color="#4472C4", alpha=0.8)
    bars2 = ax.bar(x + width/2, purified_vals, width, label="Purified CTT", color="#ED7D31", alpha=0.8)

    # Labels and title
    ax.set_xlabel("Congruence Level", fontsize=12)
    ax.set_ylabel("AIC (lower = better fit)", fontsize=12)
    ax.set_title("LMM Model Fit (AIC) by Congruence Level\n(Lower AIC = Better Model Fit)", fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(dimensions)
    ax.legend(loc="upper right")

    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

    for bar in bars2:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

    # Add delta AIC annotations
    deltas = purified_vals - full_vals
    for i, delta in enumerate(deltas):
        if delta > 0:
            annotation = f"Δ = +{delta:.1f}\n(Full better)"
            color = "green"
        else:
            annotation = f"Δ = {delta:.1f}\n(Purified better)"
            color = "red"
        ax.annotate(annotation, xy=(i, max(full_vals[i], purified_vals[i]) + 15),
                    ha='center', fontsize=8, color=color)

    plt.tight_layout()
    plt.savefig(PLOT_DIR / "aic_comparison.png", dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Saved: {PLOT_DIR / 'aic_comparison.png'}")


if __name__ == "__main__":
    print("Generating RQ 5.4.5 plots...")
    plot_correlation_comparison()
    plot_aic_comparison()
    print("Done!")
