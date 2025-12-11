#!/usr/bin/env python3
"""
RQ 6.2.1: Calibration Over Time - Plots
========================================
Creates publication-quality visualizations for calibration trajectory analysis.

Plots:
1. calibration_trajectory.png - Main trajectory with CI bands
2. brier_by_test.png - Brier scores across tests
3. ece_by_test.png - ECE across tests

Author: Claude Code
Date: 2025-12-11
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Configuration
RQ_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = RQ_DIR / "data"
PLOTS_DIR = RQ_DIR / "plots"

# Styling
plt.style.use('seaborn-v0_8-whitegrid')
COLORS = {'main': '#1f77b4', 'ci': '#a6cee3', 'secondary': '#ff7f0e'}


def plot_calibration_trajectory():
    """Plot calibration trajectory over time (Decision D069 compliant)."""
    df = pd.read_csv(DATA_DIR / "step07_calibration_trajectory_theta_data.csv")

    fig, ax = plt.subplots(figsize=(10, 6))

    # Sort by time
    df = df.sort_values('time')

    # Plot CI band
    ax.fill_between(df['time'], df['CI_lower'], df['CI_upper'],
                    alpha=0.3, color=COLORS['ci'], label='95% CI')

    # Plot trajectory line
    ax.plot(df['time'], df['calibration'], 'o-', color=COLORS['main'],
            linewidth=2, markersize=10, label='Mean Calibration')

    # Add zero reference line
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.7, label='Perfect Calibration')

    # Annotations for each test
    for _, row in df.iterrows():
        ax.annotate(f"{row['test']}\n{row['calibration']:.3f}",
                    xy=(row['time'], row['calibration']),
                    xytext=(0, 15), textcoords='offset points',
                    ha='center', fontsize=9)

    # Labels and title
    ax.set_xlabel('Time Since Encoding (hours)', fontsize=12)
    ax.set_ylabel('Calibration (z_confidence - z_accuracy)', fontsize=12)
    ax.set_title('RQ 6.2.1: Calibration Trajectory Over Time\n'
                 'Positive = Overconfidence, Negative = Underconfidence', fontsize=14)

    # Add result annotation
    time_effect = pd.read_csv(DATA_DIR / "step06_time_effect.csv")
    p_lrt = time_effect['p_corrected'].iloc[0]
    coef = time_effect['coefficient_per_hour'].iloc[0]

    result_text = (f"Time Effect: β = {coef:.6f}/hour\n"
                   f"p (LRT) = {p_lrt:.4f} **\n"
                   f"Calibration WORSENS over time")
    ax.text(0.98, 0.02, result_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    ax.legend(loc='upper left')
    ax.set_xlim(-5, 170)

    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "calibration_trajectory.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: calibration_trajectory.png")


def plot_brier_scores():
    """Plot Brier scores by test session."""
    df = pd.read_csv(DATA_DIR / "step03_brier_scores.csv")

    # Aggregate by test
    brier_by_test = df.groupby('TEST')['brier_score'].agg(['mean', 'std', 'count']).reset_index()
    brier_by_test['se'] = brier_by_test['std'] / np.sqrt(brier_by_test['count'])
    brier_by_test['ci'] = 1.96 * brier_by_test['se']

    # Sort by test
    brier_by_test['test_order'] = brier_by_test['TEST'].str.extract(r'(\d)').astype(int)
    brier_by_test = brier_by_test.sort_values('test_order')

    fig, ax = plt.subplots(figsize=(8, 6))

    x = range(len(brier_by_test))
    ax.bar(x, brier_by_test['mean'], yerr=brier_by_test['ci'], capsize=5,
           color=COLORS['main'], alpha=0.7, edgecolor='black')

    ax.set_xticks(x)
    ax.set_xticklabels(brier_by_test['TEST'])
    ax.set_xlabel('Test Session', fontsize=12)
    ax.set_ylabel('Brier Score (lower = better calibration)', fontsize=12)
    ax.set_title('RQ 6.2.1: Item-Level Calibration (Brier Score) by Test', fontsize=14)

    # Add mean annotation
    for i, row in brier_by_test.iterrows():
        ax.annotate(f"{row['mean']:.3f}",
                    xy=(list(x)[list(brier_by_test.index).index(i)], row['mean'] + row['ci']),
                    ha='center', va='bottom', fontsize=10)

    ax.set_ylim(0, max(brier_by_test['mean'] + brier_by_test['ci']) * 1.2)

    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "brier_by_test.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: brier_by_test.png")


def plot_ece():
    """Plot Expected Calibration Error by test session."""
    df = pd.read_csv(DATA_DIR / "step04_ece_by_time.csv")

    # Convert test to proper format
    df['test'] = 'T' + df['test'].astype(str).str.replace('.0', '', regex=False)
    df = df.sort_values('test')

    fig, ax = plt.subplots(figsize=(8, 6))

    x = range(len(df))
    ax.bar(x, df['ECE'], color=COLORS['secondary'], alpha=0.7, edgecolor='black')

    ax.set_xticks(x)
    ax.set_xticklabels(df['test'])
    ax.set_xlabel('Test Session', fontsize=12)
    ax.set_ylabel('Expected Calibration Error (ECE)', fontsize=12)
    ax.set_title('RQ 6.2.1: ECE by Test Session\n(lower = better calibration)', fontsize=14)

    # Add value annotations
    for i, row in df.iterrows():
        ax.annotate(f"{row['ECE']:.3f}",
                    xy=(list(x)[list(df.index).index(i)], row['ECE']),
                    ha='center', va='bottom', fontsize=10)

    ax.set_ylim(0, max(df['ECE']) * 1.3)

    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "ece_by_test.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: ece_by_test.png")


def main():
    """Generate all plots."""
    print(f"RQ 6.2.1: Generating plots...")
    print(f"Data directory: {DATA_DIR}")
    print(f"Plots directory: {PLOTS_DIR}")

    plot_calibration_trajectory()
    plot_brier_scores()
    plot_ece()

    print("All plots generated successfully.")


if __name__ == "__main__":
    main()
