#!/usr/bin/env python3
"""
RQ 6.7.2: Plots
================

Scatterplot showing relationship between confidence variability and accuracy variability.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

RQ_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = RQ_DIR / "data"
PLOTS_DIR = RQ_DIR / "plots"

def main():
    """Generate plots."""
    # Load data
    scatter_data = pd.read_csv(DATA_DIR / "step04_variability_scatterplot_data.csv")
    regression_line = pd.read_csv(DATA_DIR / "step04_variability_regression_line.csv")
    correlation = pd.read_csv(DATA_DIR / "step03_correlation.csv")
    suppression = pd.read_csv(DATA_DIR / "step05_suppression_analysis.csv")

    # Extract stats
    r = correlation['r'].values[0]
    p = correlation['p_parametric'].values[0]
    r_partial = correlation['r_partial'].values[0]
    p_partial = correlation['p_partial'].values[0]

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot scatter points
    ax.scatter(
        scatter_data['SD_confidence'],
        scatter_data['SD_accuracy'],
        alpha=0.6,
        s=50,
        c='steelblue',
        edgecolors='white',
        linewidth=0.5
    )

    # Plot regression line
    ax.plot(
        regression_line['SD_confidence'],
        regression_line['SD_accuracy_predicted'],
        'r-',
        linewidth=2,
        label=f'Zero-order: r = {r:.3f} (p = {p:.3f})'
    )

    # Labels
    ax.set_xlabel('Within-Person Confidence Variability (SD)', fontsize=12)
    ax.set_ylabel('Within-Person Accuracy Variability (SD)', fontsize=12)
    ax.set_title('RQ 6.7.2: Confidence Variability vs Accuracy Variability\n(Person-Level, N=100)', fontsize=14)

    # Add stats annotation
    stats_text = (
        f"Zero-order: r = {r:.3f}, p = {p:.3f}\n"
        f"Partial (|mean_acc): r = {r_partial:.3f}, p = {p_partial:.3f}\n\n"
        f"SUPPRESSION EFFECT:\n"
        f"True relationship masked by\n"
        f"ability-related confounds"
    )
    ax.text(
        0.95, 0.05,
        stats_text,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment='bottom',
        horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    )

    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)

    # Save
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "variability_correlation.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: plots/variability_correlation.png")

    # === SUPPRESSION MECHANISM PLOT ===
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Load person-level data for mechanism plots
    person_level = pd.read_csv(DATA_DIR / "step03_person_level.csv")

    # Plot 1: SD_conf vs mean_acc
    ax1 = axes[0]
    ax1.scatter(person_level['avg_mean_accuracy'], person_level['avg_SD_confidence'],
                alpha=0.6, s=50, c='green')
    r_xz = suppression['r_xz'].values[0]
    ax1.set_xlabel('Mean Accuracy', fontsize=11)
    ax1.set_ylabel('SD Confidence', fontsize=11)
    ax1.set_title(f'r = {r_xz:.3f}', fontsize=12)
    ax1.grid(True, alpha=0.3)

    # Plot 2: SD_acc vs mean_acc
    ax2 = axes[1]
    ax2.scatter(person_level['avg_mean_accuracy'], person_level['avg_SD_accuracy'],
                alpha=0.6, s=50, c='red')
    r_yz = suppression['r_yz'].values[0]
    ax2.set_xlabel('Mean Accuracy', fontsize=11)
    ax2.set_ylabel('SD Accuracy', fontsize=11)
    ax2.set_title(f'r = {r_yz:.3f}', fontsize=12)
    ax2.grid(True, alpha=0.3)

    # Plot 3: SD_conf vs SD_acc (original)
    ax3 = axes[2]
    ax3.scatter(person_level['avg_SD_confidence'], person_level['avg_SD_accuracy'],
                alpha=0.6, s=50, c='steelblue')
    ax3.set_xlabel('SD Confidence', fontsize=11)
    ax3.set_ylabel('SD Accuracy', fontsize=11)
    ax3.set_title(f'r = {r:.3f} (null)', fontsize=12)
    ax3.grid(True, alpha=0.3)

    fig.suptitle('Suppression Mechanism: Opposing Paths Cancel Out', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "suppression_mechanism.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: plots/suppression_mechanism.png")


if __name__ == "__main__":
    main()
