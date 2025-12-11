#!/usr/bin/env python3
"""
RQ 6.4.2: Paradigm Confidence Calibration - Plots
===================================================
Generates publication-quality visualizations for paradigm-specific calibration analysis.

Key Finding: Paradigm main effect SIGNIFICANT (p=0.040 Bonferroni), but NO interaction with time.
Calibration differs by paradigm but follows parallel trajectories.
ICR (Cued Recall) shows slight underconfidence, IFR/IRE show slight overconfidence.

Plots:
1. Calibration trajectories by paradigm (main finding - parallel trajectories)
2. Paradigm ranking comparison (absolute calibration)
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
RQ_DIR = Path(__file__).resolve().parents[1]  # results/ch6/6.4.2
DATA_DIR = RQ_DIR / "data"
PLOTS_DIR = RQ_DIR / "plots"

# Plot style
plt.style.use('seaborn-v0_8-whitegrid')
COLORS = {'IFR': '#1f77b4', 'ICR': '#ff7f0e', 'IRE': '#2ca02c'}
LABELS = {'IFR': 'Free Recall', 'ICR': 'Cued Recall', 'IRE': 'Recognition'}


def plot_calibration_trajectories():
    """
    Plot 1: Calibration trajectories by paradigm over time.
    Shows parallel trajectories - Paradigm main effect but no interaction.
    """
    # Load data
    df = pd.read_csv(DATA_DIR / "step04_calibration_trajectory_data.csv")

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot each paradigm
    for paradigm in ['IFR', 'ICR', 'IRE']:
        paradigm_data = df[df['Paradigm'] == paradigm].sort_values('TSVR_hours')

        ax.plot(
            paradigm_data['TSVR_hours'],
            paradigm_data['mean_calibration'],
            marker='o',
            markersize=8,
            linewidth=2,
            color=COLORS[paradigm],
            label=f"{LABELS[paradigm]} ({paradigm})"
        )

        # Add confidence intervals
        ax.fill_between(
            paradigm_data['TSVR_hours'],
            paradigm_data['CI_lower'],
            paradigm_data['CI_upper'],
            alpha=0.2,
            color=COLORS[paradigm]
        )

    # Add reference line at zero (perfect calibration)
    ax.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5, label='Perfect calibration')

    # Add shaded regions for interpretation
    ax.axhspan(0, 1, alpha=0.05, color='red', label='_Overconfidence')
    ax.axhspan(-1, 0, alpha=0.05, color='blue', label='_Underconfidence')

    # Labels
    ax.set_xlabel('Time Since VR Encoding (Hours)', fontsize=12)
    ax.set_ylabel('Calibration (Confidence - Accuracy, z-standardized)', fontsize=12)
    ax.set_title('RQ 6.4.2: Paradigm-Specific Calibration Trajectories\n(Paradigm Effect p=0.040, No Interaction with Time)', fontsize=14)

    # Add annotation for key regions
    ax.annotate('Overconfident', xy=(0.02, 0.98), xycoords='axes fraction',
                fontsize=10, color='darkred', alpha=0.7, va='top')
    ax.annotate('Underconfident', xy=(0.02, 0.02), xycoords='axes fraction',
                fontsize=10, color='darkblue', alpha=0.7, va='bottom')

    # Legend
    ax.legend(loc='upper right', fontsize=10)

    # Set axis limits
    ax.set_xlim(-5, 160)
    ax.set_ylim(-0.5, 0.5)

    # Add test markers on x-axis
    ax.set_xticks([0, 24, 72, 144])
    ax.set_xticklabels(['T1\n(Day 0)', 'T2\n(Day 1)', 'T3\n(Day 3)', 'T4\n(Day 6)'])

    plt.tight_layout()

    # Save
    output_path = PLOTS_DIR / "calibration_trajectories_by_paradigm.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")


def plot_paradigm_ranking():
    """
    Plot 2: Paradigm ranking by calibration quality (absolute calibration).
    """
    # Load data
    df = pd.read_csv(DATA_DIR / "step03_paradigm_ranking.csv")

    fig, ax = plt.subplots(figsize=(8, 5))

    # Create bar plot
    bars = ax.bar(
        [LABELS[p] for p in df['Paradigm']],
        df['mean_abs_calibration'],
        yerr=df['sd_abs_calibration'] / np.sqrt(df['N']) * 1.96,  # 95% CI
        capsize=5,
        color=[COLORS[p] for p in df['Paradigm']],
        edgecolor='black',
        linewidth=1.5
    )

    # Add rank labels on bars
    for i, (_, row) in enumerate(df.iterrows()):
        ax.text(
            i, row['mean_abs_calibration'] + 0.05,
            f"Rank {int(row['rank'])}",
            ha='center', fontsize=10, fontweight='bold'
        )

    # Labels
    ax.set_xlabel('Retrieval Paradigm', fontsize=12)
    ax.set_ylabel('Mean Absolute Calibration (|z|)', fontsize=12)
    ax.set_title('RQ 6.4.2: Paradigm Ranking by Calibration Quality\n(Lower = Better Calibrated)', fontsize=14)

    # Annotation
    ax.annotate(
        'Key Finding:\n'
        '• Free Recall: Best calibrated (supports hypothesis)\n'
        '• Recognition: Worst calibrated (supports fluency-familiarity heuristic)\n'
        '• Differences are small (d < 0.11)',
        xy=(0.98, 0.98), xycoords='axes fraction',
        fontsize=9, ha='right', va='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    )

    ax.set_ylim(0, 1.1)

    plt.tight_layout()

    # Save
    output_path = PLOTS_DIR / "paradigm_calibration_ranking.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")


def plot_paradigm_means():
    """
    Plot 3: Paradigm calibration means (signed, showing over/under-confidence direction).
    """
    # Load raw data
    df = pd.read_csv(DATA_DIR / "step00_calibration_by_paradigm.csv")

    fig, ax = plt.subplots(figsize=(8, 5))

    # Compute means and CIs
    paradigm_stats = df.groupby('Paradigm')['calibration'].agg(['mean', 'std', 'count']).reset_index()
    paradigm_stats['se'] = paradigm_stats['std'] / np.sqrt(paradigm_stats['count'])
    paradigm_stats['ci_lower'] = paradigm_stats['mean'] - 1.96 * paradigm_stats['se']
    paradigm_stats['ci_upper'] = paradigm_stats['mean'] + 1.96 * paradigm_stats['se']

    # Order paradigms
    paradigm_order = ['IFR', 'ICR', 'IRE']
    paradigm_stats = paradigm_stats.set_index('Paradigm').loc[paradigm_order].reset_index()

    # Create bar plot with error bars
    x = np.arange(len(paradigm_order))
    bars = ax.bar(
        x,
        paradigm_stats['mean'],
        yerr=[paradigm_stats['mean'] - paradigm_stats['ci_lower'],
              paradigm_stats['ci_upper'] - paradigm_stats['mean']],
        capsize=5,
        color=[COLORS[p] for p in paradigm_order],
        edgecolor='black',
        linewidth=1.5
    )

    # Add reference line at zero
    ax.axhline(y=0, color='black', linestyle='--', linewidth=1.5, alpha=0.7)

    # Add value labels on bars
    for i, (_, row) in enumerate(paradigm_stats.iterrows()):
        label_y = row['mean'] + 0.02 if row['mean'] >= 0 else row['mean'] - 0.03
        cal_type = "Over" if row['mean'] > 0 else "Under"
        ax.text(i, label_y, f"{cal_type}\n{row['mean']:.3f}",
                ha='center', fontsize=9, fontweight='bold')

    # Labels
    ax.set_xticks(x)
    ax.set_xticklabels([LABELS[p] for p in paradigm_order], fontsize=11)
    ax.set_xlabel('Retrieval Paradigm', fontsize=12)
    ax.set_ylabel('Mean Calibration (z-standardized)', fontsize=12)
    ax.set_title('RQ 6.4.2: Calibration Direction by Paradigm\n(Positive = Overconfidence, Negative = Underconfidence)', fontsize=14)

    # Annotation regions
    ax.annotate('OVERCONFIDENT', xy=(0.95, 0.98), xycoords='axes fraction',
                fontsize=10, color='darkred', alpha=0.7, va='top', ha='right')
    ax.annotate('UNDERCONFIDENT', xy=(0.95, 0.02), xycoords='axes fraction',
                fontsize=10, color='darkblue', alpha=0.7, va='bottom', ha='right')

    ax.set_ylim(-0.15, 0.15)

    plt.tight_layout()

    # Save
    output_path = PLOTS_DIR / "paradigm_calibration_direction.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")


def main():
    """Generate all plots."""
    print(f"Generating plots for RQ 6.4.2...")
    print(f"Data directory: {DATA_DIR}")
    print(f"Plots directory: {PLOTS_DIR}")

    plot_calibration_trajectories()
    plot_paradigm_ranking()
    plot_paradigm_means()

    print("\nAll plots generated successfully!")


if __name__ == "__main__":
    main()
