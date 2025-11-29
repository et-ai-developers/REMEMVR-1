#!/usr/bin/env python3
"""
RQ 5.11 Visualization Script
IRT-CTT Convergent Validity Comparison

Generates:
1. Scatterplot: IRT vs CTT per domain with regression lines
2. Trajectory comparison: IRT vs CTT trajectories over time
"""

import sys
from pathlib import Path

# Setup project root path
PROJECT_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# Set publication-quality style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['legend.fontsize'] = 9

# Define paths
RQ_DIR = PROJECT_ROOT / "results" / "ch5" / "rq11"
DATA_DIR = RQ_DIR / "data"
PLOTS_DIR = RQ_DIR / "plots"

def plot_irt_ctt_scatterplots():
    """
    Generate 3-panel scatterplot showing IRT vs CTT correlation per domain.

    Each panel shows:
    - Scatter points (IRT_score vs CTT_score)
    - Regression line (OLS)
    - Correlation coefficient annotation
    """
    print("[PLOT 1] Generating IRT vs CTT scatterplots...")

    # Load data
    scatter_data = pd.read_csv(DATA_DIR / "step07_scatterplot_data.csv")
    print(f"  Loaded {len(scatter_data)} observations")

    # Create figure with 3 panels (1 row, 3 columns)
    fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=True)

    domains = ["what", "where", "when"]
    domain_labels = {"what": "What (Objects)", "where": "Where (Locations)", "when": "When (Time)"}
    colors = {"what": "#2E86AB", "where": "#A23B72", "when": "#F18F01"}

    for idx, domain in enumerate(domains):
        ax = axes[idx]

        # Filter data for this domain
        domain_data = scatter_data[scatter_data['domain'] == domain].copy()

        if len(domain_data) == 0:
            print(f"  WARNING: No data for domain {domain}")
            continue

        # Get correlation coefficient (from r column)
        r = domain_data['r'].iloc[0]

        # Scatter plot
        ax.scatter(domain_data['IRT_score'], domain_data['CTT_score'],
                  alpha=0.6, s=30, color=colors[domain], edgecolors='white', linewidth=0.5)

        # Regression line
        slope, intercept, r_val, p_val, std_err = stats.linregress(
            domain_data['IRT_score'], domain_data['CTT_score']
        )
        x_range = np.linspace(domain_data['IRT_score'].min(), domain_data['IRT_score'].max(), 100)
        y_pred = slope * x_range + intercept
        ax.plot(x_range, y_pred, 'k--', linewidth=1.5, label=f'OLS: y = {slope:.2f}x + {intercept:.2f}')

        # Formatting
        ax.set_xlabel("IRT Theta Score")
        if idx == 0:
            ax.set_ylabel("CTT Mean Score (Proportion Correct)")
        ax.set_title(domain_labels[domain])
        ax.grid(True, alpha=0.3)

        # Annotate with correlation
        ax.text(0.05, 0.95, f'r = {r:.3f}',
               transform=ax.transAxes, fontsize=11, weight='bold',
               verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    plt.tight_layout()

    # Save
    output_path = PLOTS_DIR / "irt_ctt_scatterplots.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"  Saved: {output_path}")
    plt.close()


def plot_irt_ctt_trajectories():
    """
    Generate 3-panel trajectory comparison showing IRT vs CTT over time.

    Each panel shows:
    - IRT trajectory with 95% CI (aggregated by timepoint bins)
    - CTT trajectory with 95% CI (aggregated by timepoint bins)
    - TSVR_hours on x-axis with smooth binned averages
    """
    print("[PLOT 2] Generating IRT vs CTT trajectory comparison...")

    # Load data
    trajectory_data = pd.read_csv(DATA_DIR / "step08_trajectory_data.csv")
    print(f"  Loaded {len(trajectory_data)} timepoint observations")

    # Create figure with 3 panels
    fig, axes = plt.subplots(1, 3, figsize=(14, 4), sharey=False)

    # Normalize domain names (handle case variations)
    trajectory_data['domain'] = trajectory_data['domain'].str.capitalize()

    domains = ["What", "Where", "When"]
    domain_labels = {"What": "What (Objects)", "Where": "Where (Locations)", "When": "When (Time)"}
    colors = {"IRT": "#1B9E77", "CTT": "#D95F02"}

    # Define timepoint bins for aggregation (reduce noise from individual participants)
    # Bins: 0-30h (Day 1), 30-80h (Day 3), 80-140h (Day 6), 140-250h (Day 7+)
    time_bins = [0, 30, 80, 140, 250]
    time_labels = [15, 55, 110, 195]  # Midpoints for plotting

    for idx, domain in enumerate(domains):
        ax = axes[idx]

        # Filter data for this domain
        domain_data = trajectory_data[trajectory_data['domain'] == domain].copy()

        if len(domain_data) == 0:
            print(f"  WARNING: No data for domain {domain}")
            continue

        # Bin TSVR_hours for smoother aggregation
        domain_data['time_bin'] = pd.cut(domain_data['TSVR_hours'], bins=time_bins, labels=time_labels)

        # Plot IRT and CTT separately
        for model in ["IRT", "CTT"]:
            model_data = domain_data[domain_data['model'] == model].copy()

            if len(model_data) == 0:
                continue

            # Aggregate by time bin (weighted mean where n > 1)
            binned = model_data.groupby('time_bin', observed=True).apply(
                lambda g: pd.Series({
                    'mean_score': np.average(g['mean_score'], weights=g['n'].fillna(1)),
                    'CI_lower': np.average(g['CI_lower'].fillna(g['mean_score']), weights=g['n'].fillna(1)),
                    'CI_upper': np.average(g['CI_upper'].fillna(g['mean_score']), weights=g['n'].fillna(1)),
                    'total_n': g['n'].sum()
                })
            ).reset_index()

            # Convert time_bin back to numeric for plotting
            binned['time_numeric'] = binned['time_bin'].astype(float)

            # Plot mean trajectory with line and markers
            ax.plot(binned['time_numeric'], binned['mean_score'],
                   color=colors[model], linewidth=2.5, label=model, alpha=0.9,
                   marker='o', markersize=6)

            # Plot confidence interval
            ax.fill_between(binned['time_numeric'],
                           binned['CI_lower'], binned['CI_upper'],
                           color=colors[model], alpha=0.25)

        # Formatting
        ax.set_xlabel("Time Since Encoding (hours)")
        if idx == 0:
            ax.set_ylabel("Mean Score")
        ax.set_title(domain_labels[domain])
        ax.legend(loc='best', framealpha=0.9)
        ax.grid(True, alpha=0.3)

        # Add reference line at y=0 for IRT scale
        ax.axhline(y=0, color='gray', linestyle=':', linewidth=1, alpha=0.5)

        # Set x-axis limits for clarity
        ax.set_xlim(-5, 250)

    plt.tight_layout()

    # Save
    output_path = PLOTS_DIR / "irt_ctt_trajectories.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"  Saved: {output_path}")
    plt.close()


if __name__ == "__main__":
    print("=" * 60)
    print("RQ 5.11: IRT-CTT Convergent Validity Visualization")
    print("=" * 60)

    # Generate plots
    plot_irt_ctt_scatterplots()
    plot_irt_ctt_trajectories()

    print("\n[SUCCESS] All plots generated")
    print(f"Output directory: {PLOTS_DIR}")
