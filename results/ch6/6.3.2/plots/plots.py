#!/usr/bin/env python3
"""
RQ 6.3.2: Domain Confidence Calibration - Plots
================================================
Generates publication-quality visualizations for domain-specific calibration analysis.

Plots:
1. Calibration trajectories by domain (main finding - crossover interaction)
2. Domain ranking comparison (absolute calibration)
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Add project root to path for tools import
PROJECT_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(PROJECT_ROOT))

# Configuration
RQ_DIR = Path(__file__).resolve().parents[1]  # results/ch6/6.3.2
DATA_DIR = RQ_DIR / "data"
PLOTS_DIR = RQ_DIR / "plots"

# Plot style
plt.style.use('seaborn-v0_8-whitegrid')
COLORS = {'What': '#1f77b4', 'Where': '#ff7f0e', 'When': '#2ca02c'}


def plot_calibration_trajectories():
    """
    Plot 1: Calibration trajectories by domain over time.
    Shows crossover interaction - When domain has opposite trajectory.
    """
    # Load data
    df = pd.read_csv(DATA_DIR / "step04_calibration_trajectory_data.csv")

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot each domain
    for domain in ['What', 'Where', 'When']:
        domain_data = df[df['Domain'] == domain].sort_values('TSVR_hours')

        ax.plot(
            domain_data['TSVR_hours'],
            domain_data['mean_calibration'],
            marker='o',
            markersize=8,
            linewidth=2,
            color=COLORS[domain],
            label=domain
        )

        # Add confidence intervals
        ax.fill_between(
            domain_data['TSVR_hours'],
            domain_data['CI_lower'],
            domain_data['CI_upper'],
            alpha=0.2,
            color=COLORS[domain]
        )

    # Add reference line at zero (perfect calibration)
    ax.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5, label='Perfect calibration')

    # Add shaded regions for interpretation
    ax.axhspan(0, 3, alpha=0.05, color='red', label='_Overconfidence')
    ax.axhspan(-3, 0, alpha=0.05, color='blue', label='_Underconfidence')

    # Labels
    ax.set_xlabel('Time Since VR Encoding (Hours)', fontsize=12)
    ax.set_ylabel('Calibration (Confidence - Accuracy, z-standardized)', fontsize=12)
    ax.set_title('RQ 6.3.2: Domain-Specific Calibration Trajectories\n(Crossover Interaction: When vs What/Where)', fontsize=14)

    # Add annotation for key regions
    ax.annotate('Overconfident', xy=(0.02, 0.98), xycoords='axes fraction',
                fontsize=10, color='darkred', alpha=0.7, va='top')
    ax.annotate('Underconfident', xy=(0.02, 0.02), xycoords='axes fraction',
                fontsize=10, color='darkblue', alpha=0.7, va='bottom')

    # Legend
    ax.legend(loc='upper right', fontsize=10)

    # Set axis limits
    ax.set_xlim(-5, 160)
    ax.set_ylim(-1.0, 0.8)

    # Add test markers on x-axis
    ax.set_xticks([0, 24, 72, 144])
    ax.set_xticklabels(['T1\n(Day 0)', 'T2\n(Day 1)', 'T3\n(Day 3)', 'T4\n(Day 6)'])

    plt.tight_layout()

    # Save
    output_path = PLOTS_DIR / "calibration_trajectories_by_domain.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")


def plot_domain_ranking():
    """
    Plot 2: Domain ranking by calibration quality (absolute calibration).
    """
    # Load data
    df = pd.read_csv(DATA_DIR / "step03_domain_ranking.csv")

    fig, ax = plt.subplots(figsize=(8, 5))

    # Create bar plot
    bars = ax.bar(
        df['Domain'],
        df['mean_abs_calibration'],
        yerr=df['sd_abs_calibration'] / np.sqrt(df['N']) * 1.96,  # 95% CI
        capsize=5,
        color=[COLORS[d] for d in df['Domain']],
        edgecolor='black',
        linewidth=1.5
    )

    # Add rank labels on bars
    for i, (domain, row) in enumerate(df.iterrows()):
        ax.text(
            i, row['mean_abs_calibration'] + 0.05,
            f"Rank {int(row['rank'])}",
            ha='center', fontsize=10, fontweight='bold'
        )

    # Labels
    ax.set_xlabel('Memory Domain', fontsize=12)
    ax.set_ylabel('Mean Absolute Calibration (|z|)', fontsize=12)
    ax.set_title('RQ 6.3.2: Domain Ranking by Calibration Quality\n(Lower = Better Calibrated)', fontsize=14)

    # Annotation
    ax.annotate(
        '• When domain worst calibrated (highest variability)\n'
        '• What/Where nearly identical calibration quality',
        xy=(0.98, 0.98), xycoords='axes fraction',
        fontsize=9, ha='right', va='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    )

    ax.set_ylim(0, 1.3)

    plt.tight_layout()

    # Save
    output_path = PLOTS_DIR / "domain_calibration_ranking.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")


def main():
    """Generate all plots."""
    print(f"Generating plots for RQ 6.3.2...")
    print(f"Data directory: {DATA_DIR}")
    print(f"Plots directory: {PLOTS_DIR}")

    plot_calibration_trajectories()
    plot_domain_ranking()

    print("\nAll plots generated successfully!")


if __name__ == "__main__":
    main()
