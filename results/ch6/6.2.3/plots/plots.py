#!/usr/bin/env python3
"""
RQ 6.2.3: Resolution Over Time - Visualization

Plots:
1. Resolution trajectory: Observed means with CIs + model-predicted line
2. Threshold comparison: Gamma vs 0.50 threshold at each timepoint
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Configuration
RQ_DIR = Path(__file__).resolve().parents[1]  # results/ch6/6.2.3
DATA_DIR = RQ_DIR / "data"
PLOTS_DIR = RQ_DIR / "plots"

def plot_resolution_trajectory():
    """Plot resolution (gamma) trajectory over time with model prediction."""

    # Load data
    df_plot = pd.read_csv(DATA_DIR / "step06_resolution_trajectory_data.csv")
    df_time_effect = pd.read_csv(DATA_DIR / "step03_time_effect.csv")

    # Extract statistics
    time_coef = df_time_effect.iloc[0]['coefficient']
    time_p = df_time_effect.iloc[0]['p_uncorrected']

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot observed means with error bars (95% CI)
    ax.errorbar(
        df_plot['time_days'],
        df_plot['observed_mean'],
        yerr=[df_plot['observed_mean'] - df_plot['CI_lower'],
              df_plot['CI_upper'] - df_plot['observed_mean']],
        fmt='o-',
        color='#2196F3',
        markersize=10,
        linewidth=2,
        capsize=5,
        capthick=2,
        label='Observed (±95% CI)'
    )

    # Plot model-predicted line
    x_pred = np.linspace(0, 7, 100)
    intercept = df_plot['predicted_mean'].iloc[0] - time_coef * df_plot['time_days'].iloc[0]
    y_pred = intercept + time_coef * x_pred

    ax.plot(x_pred, y_pred, '--', color='#FF5722', linewidth=2, alpha=0.8,
            label=f'LMM Predicted (β = {time_coef:.4f}/day)')

    # Add threshold line
    ax.axhline(y=0.50, color='gray', linestyle=':', linewidth=2, alpha=0.7,
               label='Threshold (γ = 0.50)')

    # Formatting
    ax.set_xlabel('Time (Days Since Encoding)', fontsize=12)
    ax.set_ylabel('Resolution (Goodman-Kruskal γ)', fontsize=12)
    ax.set_title(f'RQ 6.2.3: Metacognitive Resolution Decline Over Time\n'
                 f'Time Effect: β = {time_coef:.4f}, p = {time_p:.4f} ({"Significant" if time_p < 0.05 else "Non-significant"})',
                 fontsize=14)

    ax.set_xlim(-0.5, 7.5)
    ax.set_ylim(0.4, 0.85)
    ax.set_xticks([0, 1, 3, 6])
    ax.set_xticklabels(['Day 0\n(T1)', 'Day 1\n(T2)', 'Day 3\n(T3)', 'Day 6\n(T4)'])

    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)

    # Add annotation
    decline_pct = 100 * (df_plot.iloc[0]['observed_mean'] - df_plot.iloc[-1]['observed_mean']) / df_plot.iloc[0]['observed_mean']
    ax.annotate(
        f'9.1% decline\n(γ: 0.73 → 0.66)',
        xy=(6, df_plot.iloc[-1]['observed_mean']),
        xytext=(4.5, 0.55),
        fontsize=10,
        arrowprops=dict(arrowstyle='->', color='gray', lw=1.5),
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray', alpha=0.8)
    )

    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "resolution_trajectory.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {PLOTS_DIR / 'resolution_trajectory.png'}")


def plot_gamma_distribution():
    """Plot gamma distribution by timepoint."""

    # Load data
    df_gamma = pd.read_csv(DATA_DIR / "step01_gamma_scores.csv")
    df_threshold = pd.read_csv(DATA_DIR / "step05_gamma_threshold_tests.csv")

    fig, axes = plt.subplots(1, 4, figsize=(14, 4), sharey=True)

    colors = ['#4CAF50', '#2196F3', '#FF9800', '#F44336']

    for i, test in enumerate(['T1', 'T2', 'T3', 'T4']):
        ax = axes[i]
        test_data = df_gamma[df_gamma['TEST'] == test]['gamma']
        threshold_row = df_threshold[df_threshold['TEST'] == test].iloc[0]

        # Histogram
        ax.hist(test_data, bins=20, color=colors[i], alpha=0.7, edgecolor='white')

        # Mean line
        mean_val = test_data.mean()
        ax.axvline(x=mean_val, color='black', linestyle='-', linewidth=2, label=f'Mean: {mean_val:.3f}')

        # Threshold line
        ax.axvline(x=0.50, color='red', linestyle='--', linewidth=2, label='Threshold: 0.50')

        # Labels
        ax.set_xlabel('Resolution (γ)', fontsize=10)
        if i == 0:
            ax.set_ylabel('Count', fontsize=10)
        ax.set_title(f'{test}\n(p < 0.001***)', fontsize=11)
        ax.set_xlim(0, 1)
        ax.legend(fontsize=8, loc='upper left')

    plt.suptitle('RQ 6.2.3: Gamma Distribution by Timepoint (All Exceed Threshold)', fontsize=12, y=1.02)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "gamma_distribution.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {PLOTS_DIR / 'gamma_distribution.png'}")


def main():
    """Generate all plots."""
    print("Generating RQ 6.2.3 plots...")
    plot_resolution_trajectory()
    plot_gamma_distribution()
    print("All plots generated.")


if __name__ == "__main__":
    main()
