#!/usr/bin/env python3
"""
RQ 6.7.1: Plots for Initial Confidence Predicting Forgetting Rates
===================================================================

Generates scatterplot showing relationship between Day 0 confidence and
trajectory slopes with tertile group overlays.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(PROJECT_ROOT))

RQ_DIR = Path(__file__).resolve().parents[1]  # results/ch6/6.7.1

def create_confidence_slope_scatterplot():
    """Create scatterplot showing confidence-slope relationship with tertile overlays."""

    # Load plot data
    df = pd.read_csv(RQ_DIR / "data" / "step05_confidence_predicts_forgetting_data.csv")

    # Separate individuals and means
    df_ind = df[df['is_mean'] == False]
    df_means = df[df['is_mean'] == True]

    # Load correlation result
    corr = pd.read_csv(RQ_DIR / "data" / "step04_correlation.csv")
    r = corr['correlation_r'].values[0]
    p = corr['p_uncorrected'].values[0]
    method = corr['primary_method'].values[0]

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))

    # Color map for tertiles
    colors = {'Low': '#E74C3C', 'Med': '#3498DB', 'High': '#27AE60'}

    # Plot individual points
    for tertile in ['Low', 'Med', 'High']:
        mask = df_ind['tertile'] == tertile
        ax.scatter(df_ind.loc[mask, 'Day0_confidence'],
                   df_ind.loc[mask, 'forgetting_slope'],
                   c=colors[tertile], alpha=0.5, s=50, label=f'{tertile} confidence')

    # Plot tertile means with error bars
    for _, row in df_means.iterrows():
        tertile = row['tertile']
        ax.errorbar(row['Day0_confidence'], row['forgetting_slope'],
                    yerr=row['se_slope'], fmt='s', markersize=12,
                    color=colors[tertile], markeredgecolor='black',
                    markeredgewidth=2, capsize=5, capthick=2,
                    label=f'{tertile} mean' if tertile == 'Low' else '')

    # Add regression line
    x_line = np.linspace(df_ind['Day0_confidence'].min(), df_ind['Day0_confidence'].max(), 100)
    # Use Spearman rank-based fit (just for visualization, actual correlation is rank-based)
    z = np.polyfit(df_ind['Day0_confidence'], df_ind['forgetting_slope'], 1)
    p_line = np.poly1d(z)
    ax.plot(x_line, p_line(x_line), 'k--', linewidth=2, alpha=0.7, label='Regression line')

    # Labels and title
    ax.set_xlabel('Day 0 Confidence (theta)', fontsize=12)
    ax.set_ylabel('Accuracy Trajectory Slope', fontsize=12)
    ax.set_title(f'RQ 6.7.1: Day 0 Confidence vs Accuracy Trajectory\n'
                 f'{method} r = {r:.2f}, p < .001', fontsize=14)

    # Add annotation box with interpretation
    textstr = (f'Correlation: {method} ρ = {r:.2f}\n'
               f'95% CI: [{corr["CI_lower"].values[0]:.2f}, {corr["CI_upper"].values[0]:.2f}]\n'
               f'p < .001\n\n'
               f'Interpretation:\n'
               f'High Day 0 confidence →\n'
               f'  Lower slope (less improvement)\n'
               f'Low Day 0 confidence →\n'
               f'  Higher slope (more improvement)')

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)

    # Add horizontal line at mean slope
    mean_slope = df_ind['forgetting_slope'].mean()
    ax.axhline(y=mean_slope, color='gray', linestyle=':', alpha=0.5)

    # Legend
    ax.legend(loc='lower right', fontsize=10)

    # Grid
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    # Save
    output_path = RQ_DIR / "plots" / "confidence_predicts_slope.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Saved: {output_path}")
    plt.close()

    return output_path


def create_tertile_barplot():
    """Create bar plot showing mean slope by confidence tertile."""

    # Load tertile analysis
    df = pd.read_csv(RQ_DIR / "data" / "step04_tertile_analysis.csv")

    # Load tertile test
    test = pd.read_csv(RQ_DIR / "data" / "step04_tertile_test.csv")
    d = test['cohens_d'].values[0]
    p = test['p_uncorrected'].values[0]

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 6))

    # Colors
    colors = ['#E74C3C', '#3498DB', '#27AE60']  # Low, Med, High

    # Bar positions
    x = np.arange(3)

    # Bar plot
    bars = ax.bar(x, df['mean_forgetting_slope'], yerr=df['se_forgetting_slope'],
                  color=colors, capsize=8, edgecolor='black', linewidth=1.5)

    # Labels
    ax.set_xticks(x)
    ax.set_xticklabels(['Low\nConfidence', 'Medium\nConfidence', 'High\nConfidence'])
    ax.set_ylabel('Mean Accuracy Slope', fontsize=12)
    ax.set_title(f'RQ 6.7.1: Accuracy Trajectory by Day 0 Confidence Tertile\n'
                 f'High vs Low: Cohen\'s d = {d:.2f}, p < .001', fontsize=14)

    # Add N labels on bars
    for i, (bar, row) in enumerate(zip(bars, df.itertuples())):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + row.se_forgetting_slope + 0.0005,
                f'N={int(row.N)}', ha='center', va='bottom', fontsize=10)

    # Add confidence mean labels below bars
    for i, row in df.iterrows():
        ax.text(i, ax.get_ylim()[0] + 0.001,
                f'θ={row["mean_Day0_confidence"]:.2f}', ha='center', fontsize=9, style='italic')

    # Grid
    ax.grid(True, axis='y', alpha=0.3)

    plt.tight_layout()

    # Save
    output_path = RQ_DIR / "plots" / "tertile_slope_comparison.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Saved: {output_path}")
    plt.close()

    return output_path


def main():
    """Generate all plots for RQ 6.7.1."""
    print("=" * 60)
    print("RQ 6.7.1: Generating Plots")
    print("=" * 60)

    # Ensure plots directory exists
    (RQ_DIR / "plots").mkdir(parents=True, exist_ok=True)

    # Create plots
    plot1 = create_confidence_slope_scatterplot()
    plot2 = create_tertile_barplot()

    print("\n" + "=" * 60)
    print("All plots generated successfully")
    print("=" * 60)


if __name__ == "__main__":
    main()
