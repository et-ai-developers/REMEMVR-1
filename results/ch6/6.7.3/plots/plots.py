"""
RQ 6.7.3 Plots: Calibration Predicts Trajectory Stability
=========================================================

Generates scatterplot showing (lack of) relationship between Day 0 calibration
and trajectory variability.

Author: Claude Code
Created: 2025-12-12
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# =============================================================================
# CONFIGURATION
# =============================================================================

RQ_DIR = Path(__file__).resolve().parents[1]  # results/ch6/6.7.3
DATA_DIR = RQ_DIR / "data"
PLOTS_DIR = RQ_DIR / "plots"


def create_scatterplot():
    """
    Create scatterplot of calibration vs trajectory variability.
    """
    # Load data
    df = pd.read_csv(DATA_DIR / "step04_scatterplot_data.csv")
    corr = pd.read_csv(DATA_DIR / "step03_correlation.csv")

    r = corr['r'].values[0]
    p_two = corr['p_two_tailed'].values[0]

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 6))

    # Scatterplot
    ax.scatter(df['calibration'], df['trajectory_variability'],
               alpha=0.6, s=50, edgecolor='black', linewidth=0.5)

    # Regression line
    ax.plot(df['calibration'], df['y_predicted'], 'r-', linewidth=2,
            label=f'Regression (r = {r:.3f}, p = {p_two:.3f})')

    # Labels
    ax.set_xlabel('Day 0 Calibration (z-score)\n(+) Overconfidence | (-) Underconfidence',
                  fontsize=12)
    ax.set_ylabel('Trajectory Variability (SD of Residuals)', fontsize=12)
    ax.set_title('RQ 6.7.3: Calibration Does NOT Predict Trajectory Stability\n(NULL Finding)',
                 fontsize=14, fontweight='bold')

    # Add stats annotation
    sig_text = "NOT SIGNIFICANT" if p_two >= 0.05 else "SIGNIFICANT"
    stats_text = f"r = {r:.3f}\np = {p_two:.3f}\nN = 100\n{sig_text}"
    ax.text(0.95, 0.95, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    ax.legend(loc='lower right')
    ax.grid(True, alpha=0.3)

    # Save
    output_path = PLOTS_DIR / "calibration_variability_scatterplot.png"
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"Saved: {output_path}")


def main():
    """Generate all plots for RQ 6.7.3."""
    print("=" * 60)
    print("RQ 6.7.3 Plots")
    print("=" * 60)

    create_scatterplot()

    print("=" * 60)
    print("ALL PLOTS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
