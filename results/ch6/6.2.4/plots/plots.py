"""
RQ 6.2.4: Calibration by Accuracy Level - Visualization
========================================================

Creates two plots:
1. Scatterplot of baseline_accuracy vs abs_calibration with tertile coloring and regression
2. Scatterplot of baseline_accuracy vs mean_gamma with tertile coloring and regression

Author: Claude Code (automated generation)
Date: 2025-12-11
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import stats

# Configuration
RQ_DIR = Path(__file__).resolve().parents[1]  # results/ch6/6.2.4


def create_calibration_by_accuracy_plots():
    """Create two-panel scatterplot showing calibration metrics by accuracy."""

    # Load data
    df = pd.read_csv(RQ_DIR / "data" / "step05_calibration_by_accuracy_plot_data.csv")
    df_corr = pd.read_csv(RQ_DIR / "data" / "step04_correlation.csv")
    df_dk = pd.read_csv(RQ_DIR / "data" / "step03_dunning_kruger_test.csv")

    # Create figure with two panels
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Color mapping
    colors = {'Low': '#D62728', 'Med': '#FF7F0E', 'High': '#2CA02C'}

    # --- Panel 1: Accuracy vs Absolute Calibration ---
    ax1 = axes[0]

    for label in ['Low', 'Med', 'High']:
        subset = df[df['tertile_label'] == label]
        ax1.scatter(subset['baseline_accuracy'], subset['abs_calibration'],
                   c=colors[label], label=label, alpha=0.7, s=50, edgecolors='white', linewidth=0.5)

    # Regression line
    slope, intercept, r, p, se = stats.linregress(df['baseline_accuracy'], df['abs_calibration'])
    x_line = np.linspace(df['baseline_accuracy'].min(), df['baseline_accuracy'].max(), 100)
    ax1.plot(x_line, slope * x_line + intercept, 'k--', alpha=0.5, linewidth=1.5)

    # Get correlation from results
    corr_row = df_corr[df_corr['comparison'] == 'baseline_accuracy vs abs_calibration'].iloc[0]
    rho = corr_row['r_or_rho']
    p_val = corr_row['p_bonferroni']

    # Annotation
    sig_str = f"p={p_val:.3f}" if p_val >= 0.001 else "p<0.001"
    ax1.text(0.05, 0.95, f"Spearman \u03c1={rho:.3f}\n{sig_str}",
             transform=ax1.transAxes, fontsize=11, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax1.set_xlabel('Baseline Accuracy (\u03b8)', fontsize=12)
    ax1.set_ylabel('Absolute Calibration Error', fontsize=12)
    ax1.set_title('A. Calibration Error by Accuracy Level', fontsize=13, fontweight='bold')
    ax1.legend(title='Accuracy\nTertile', loc='upper right')
    ax1.grid(True, alpha=0.3)

    # --- Panel 2: Accuracy vs Gamma (Resolution) ---
    ax2 = axes[1]

    for label in ['Low', 'Med', 'High']:
        subset = df[df['tertile_label'] == label]
        ax2.scatter(subset['baseline_accuracy'], subset['mean_gamma'],
                   c=colors[label], label=label, alpha=0.7, s=50, edgecolors='white', linewidth=0.5)

    # Regression line
    slope, intercept, r, p, se = stats.linregress(df['baseline_accuracy'], df['mean_gamma'])
    x_line = np.linspace(df['baseline_accuracy'].min(), df['baseline_accuracy'].max(), 100)
    ax2.plot(x_line, slope * x_line + intercept, 'k--', alpha=0.5, linewidth=1.5)

    # Get correlation from results
    corr_row = df_corr[df_corr['comparison'] == 'baseline_accuracy vs mean_gamma'].iloc[0]
    rho = corr_row['r_or_rho']
    p_val = corr_row['p_bonferroni']

    # Annotation
    sig_str = f"p={p_val:.3f}" if p_val >= 0.001 else "p<0.001***"
    ax2.text(0.05, 0.95, f"Spearman \u03c1={rho:.3f}\n{sig_str}",
             transform=ax2.transAxes, fontsize=11, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax2.set_xlabel('Baseline Accuracy (\u03b8)', fontsize=12)
    ax2.set_ylabel('Mean Gamma (Resolution)', fontsize=12)
    ax2.set_title('B. Resolution by Accuracy Level', fontsize=13, fontweight='bold')
    ax2.legend(title='Accuracy\nTertile', loc='lower right')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0.5, color='gray', linestyle=':', alpha=0.5, label='_nolegend_')  # Threshold

    plt.tight_layout()

    # Save
    output_path = RQ_DIR / "plots" / "calibration_by_accuracy.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

    print(f"Saved: {output_path}")
    return output_path


def create_dunning_kruger_boxplot():
    """Create boxplot showing calibration by tertile (Dunning-Kruger visualization)."""

    # Load data
    df_metrics = pd.read_csv(RQ_DIR / "data" / "step00_merged_metrics.csv")
    df_tertiles = pd.read_csv(RQ_DIR / "data" / "step01_accuracy_tertiles.csv")
    df_dk = pd.read_csv(RQ_DIR / "data" / "step03_dunning_kruger_test.csv")

    # Merge
    df = df_metrics.merge(df_tertiles[['UID', 'tertile_label']], on='UID')

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 6))

    # Prepare data for boxplot
    data_by_tertile = [
        df[df['tertile_label'] == 'Low']['mean_calibration'].values,
        df[df['tertile_label'] == 'Med']['mean_calibration'].values,
        df[df['tertile_label'] == 'High']['mean_calibration'].values
    ]

    # Colors
    colors = ['#D62728', '#FF7F0E', '#2CA02C']

    bp = ax.boxplot(data_by_tertile, positions=[1, 2, 3], patch_artist=True, widths=0.6)

    # Style boxes
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)

    # Add individual points
    for i, (data, color) in enumerate(zip(data_by_tertile, colors)):
        x = np.random.normal(i+1, 0.08, len(data))
        ax.scatter(x, data, c=color, alpha=0.5, s=30, zorder=10)

    # Add horizontal line at y=0 (perfect calibration)
    ax.axhline(y=0, color='black', linestyle='--', alpha=0.5, linewidth=1.5)
    ax.text(3.4, 0.05, 'Perfect\nCalibration', fontsize=9, alpha=0.7)

    # Add mean markers with p-values
    for i, tertile in enumerate(['Low', 'Med', 'High']):
        row = df_dk[df_dk['tertile'] == tertile].iloc[0]
        mean_val = row['mean_calibration']
        p_bonf = row['p_bonferroni']

        # Plot mean
        ax.scatter([i+1], [mean_val], marker='D', c='white', s=100, zorder=11, edgecolors='black', linewidth=2)

        # Significance annotation
        if p_bonf < 0.001:
            sig = '***'
        elif p_bonf < 0.01:
            sig = '**'
        elif p_bonf < 0.05:
            sig = '*'
        else:
            sig = 'n.s.'

        y_offset = 0.1 if mean_val > 0 else -0.15
        ax.text(i+1, mean_val + y_offset, sig, ha='center', fontsize=11, fontweight='bold')

    # Labels
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(['Low\n(Bottom 33%)', 'Medium\n(Middle 34%)', 'High\n(Top 33%)'])
    ax.set_xlabel('Baseline Accuracy Tertile', fontsize=12)
    ax.set_ylabel('Mean Calibration\n(Confidence - Accuracy)', fontsize=12)
    ax.set_title('Dunning-Kruger Test: Calibration by Performance Level', fontsize=13, fontweight='bold')

    # Add interpretation labels
    ax.text(0.55, 0.95, 'OVERCONFIDENT\n(Confidence > Accuracy)', transform=ax.transAxes,
            fontsize=9, alpha=0.6, verticalalignment='top')
    ax.text(0.55, 0.12, 'UNDERCONFIDENT\n(Confidence < Accuracy)', transform=ax.transAxes,
            fontsize=9, alpha=0.6, verticalalignment='bottom')

    ax.grid(True, axis='y', alpha=0.3)

    plt.tight_layout()

    # Save
    output_path = RQ_DIR / "plots" / "dunning_kruger_boxplot.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

    print(f"Saved: {output_path}")
    return output_path


if __name__ == "__main__":
    print("RQ 6.2.4: Generating plots...")
    create_calibration_by_accuracy_plots()
    create_dunning_kruger_boxplot()
    print("All plots generated successfully.")
