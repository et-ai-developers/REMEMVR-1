#!/usr/bin/env python3
"""
RQ 6.3.3 Plots: Age x Domain Interaction in Confidence Decline
==============================================================
Generates publication-quality visualizations for 3-way Age x Domain x Time interaction analysis.

Plots:
1. Age tertile x domain trajectories (faceted by domain, colored by tertile)
2. 3-way interaction effect visualization (comparison to null)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

RQ_DIR = Path(__file__).resolve().parents[1]  # results/ch6/6.3.3
DATA_DIR = RQ_DIR / "data"
PLOT_DIR = RQ_DIR / "plots"

# Ensure plot directory exists
PLOT_DIR.mkdir(parents=True, exist_ok=True)

# Color palette for age tertiles (matching Ch5 conventions)
TERTILE_COLORS = {
    'Young': '#2ecc71',   # Green
    'Middle': '#3498db',  # Blue
    'Older': '#e74c3c'    # Red
}

# Domain colors (matching RQ 6.3.2)
DOMAIN_COLORS = {
    'What': '#3498db',   # Blue
    'Where': '#e74c3c',  # Red
    'When': '#f39c12'    # Orange
}


def plot_tertile_domain_trajectories():
    """
    Plot 1: Age tertile trajectories faceted by domain.

    Shows confidence decline over time for each age group within each domain.
    """
    # Load trajectory data
    df = pd.read_csv(DATA_DIR / "step04_tertile_domain_trajectories.csv")

    # Convert TSVR_hours to days for interpretability
    df['Days'] = df['TSVR_hours'] / 24

    # Create figure with 3 subplots (one per domain)
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

    for idx, domain in enumerate(['What', 'Where', 'When']):
        ax = axes[idx]
        domain_data = df[df['Domain'] == domain]

        for tertile in ['Young', 'Middle', 'Older']:
            tertile_data = domain_data[domain_data['age_tertile'] == tertile].sort_values('Days')

            # Plot mean trajectory with CI
            ax.fill_between(
                tertile_data['Days'],
                tertile_data['CI_lower'],
                tertile_data['CI_upper'],
                alpha=0.2,
                color=TERTILE_COLORS[tertile]
            )
            ax.plot(
                tertile_data['Days'],
                tertile_data['mean_theta'],
                'o-',
                color=TERTILE_COLORS[tertile],
                linewidth=2,
                markersize=8,
                label=tertile
            )

        ax.set_xlabel('Days Since Encoding', fontsize=12)
        ax.set_title(f'{domain} Domain', fontsize=14, fontweight='bold')
        ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        ax.grid(True, alpha=0.3)

        if idx == 0:
            ax.set_ylabel('Confidence (theta)', fontsize=12)
            ax.legend(title='Age Tertile', loc='lower left')

    plt.suptitle('RQ 6.3.3: Age x Domain Confidence Trajectories\n(NULL 3-way interaction: p > 0.26)',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()

    # Save
    output_path = PLOT_DIR / "age_tertile_domain_trajectories.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: {output_path}")


def plot_interaction_effects():
    """
    Plot 2: 3-way interaction effect sizes visualization.

    Shows the estimated interaction coefficients with confidence intervals.
    """
    # Load interaction terms
    df = pd.read_csv(DATA_DIR / "step03_interaction_terms.csv")

    # Clean up term names for display
    df['term_display'] = df['term'].str.replace('TSVR_hours:Age_c:C(Domain)[T.', '', regex=False)
    df['term_display'] = df['term_display'].str.replace(']', '', regex=False)

    # Calculate 95% CI
    df['CI_lower'] = df['estimate'] - 1.96 * df['se']
    df['CI_upper'] = df['estimate'] + 1.96 * df['se']

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 5))

    y_positions = range(len(df))

    # Plot point estimates with error bars
    for idx, (_, row) in enumerate(df.iterrows()):
        color = DOMAIN_COLORS.get(row['term_display'], '#666666')

        ax.errorbar(
            row['estimate'],
            idx,
            xerr=[[row['estimate'] - row['CI_lower']], [row['CI_upper'] - row['estimate']]],
            fmt='o',
            color=color,
            markersize=12,
            capsize=8,
            capthick=2,
            linewidth=2
        )

    # Add vertical line at 0 (null hypothesis)
    ax.axvline(x=0, color='black', linestyle='--', linewidth=1.5, label='Null (no interaction)')

    # Formatting
    ax.set_yticks(y_positions)
    ax.set_yticklabels([f"Age × Time × {d}" for d in df['term_display']], fontsize=12)
    ax.set_xlabel('Interaction Coefficient (unstandardized)', fontsize=12)
    ax.set_title('RQ 6.3.3: 3-Way Interaction Effects\n(Both contrasts p > 0.05, NOT SIGNIFICANT)',
                 fontsize=14, fontweight='bold')

    # Add p-value annotations
    for idx, (_, row) in enumerate(df.iterrows()):
        p_text = f"p = {row['p_uncorrected']:.3f}"
        ax.annotate(p_text, xy=(row['estimate'], idx), xytext=(10, 0),
                   textcoords='offset points', fontsize=10, va='center')

    ax.grid(True, axis='x', alpha=0.3)
    plt.tight_layout()

    # Save
    output_path = PLOT_DIR / "interaction_effects.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: {output_path}")


def plot_domain_parallel_trajectories():
    """
    Plot 3: Side-by-side comparison showing parallel trajectories across age groups.

    Emphasizes the NULL finding by showing similar decline patterns.
    """
    # Load trajectory data
    df = pd.read_csv(DATA_DIR / "step04_tertile_domain_trajectories.csv")
    df['Days'] = df['TSVR_hours'] / 24

    # Compute slopes per tertile per domain
    slopes = []
    for tertile in ['Young', 'Middle', 'Older']:
        for domain in ['What', 'Where', 'When']:
            subset = df[(df['age_tertile'] == tertile) & (df['Domain'] == domain)]
            if len(subset) >= 2:
                t1 = subset[subset['test'] == 'T1']['mean_theta'].values[0]
                t4 = subset[subset['test'] == 'T4']['mean_theta'].values[0]
                slope = (t4 - t1) / (subset[subset['test'] == 'T4']['Days'].values[0] -
                                     subset[subset['test'] == 'T1']['Days'].values[0])
                slopes.append({
                    'age_tertile': tertile,
                    'Domain': domain,
                    'slope': slope * 10,  # Per 10 days
                    'T1_to_T4_change': t4 - t1
                })

    slope_df = pd.DataFrame(slopes)

    # Create bar plot of slopes
    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.arange(3)  # Domain positions
    width = 0.25

    for i, tertile in enumerate(['Young', 'Middle', 'Older']):
        tertile_data = slope_df[slope_df['age_tertile'] == tertile]
        slopes_by_domain = [tertile_data[tertile_data['Domain'] == d]['T1_to_T4_change'].values[0]
                           for d in ['What', 'Where', 'When']]

        ax.bar(x + i * width, slopes_by_domain, width,
               label=tertile, color=TERTILE_COLORS[tertile], alpha=0.8)

    ax.set_ylabel('Confidence Change (T1 to T4)', fontsize=12)
    ax.set_xlabel('Memory Domain', fontsize=12)
    ax.set_title('RQ 6.3.3: Confidence Decline by Age Tertile and Domain\n(Parallel patterns support NULL 3-way interaction)',
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels(['What', 'Where', 'When'], fontsize=12)
    ax.legend(title='Age Tertile')
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax.grid(True, axis='y', alpha=0.3)

    plt.tight_layout()

    # Save
    output_path = PLOT_DIR / "parallel_decline_by_age_domain.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: {output_path}")


def main():
    """Generate all plots for RQ 6.3.3."""
    print("Generating RQ 6.3.3 plots...")

    plot_tertile_domain_trajectories()
    plot_interaction_effects()
    plot_domain_parallel_trajectories()

    print("\nAll plots generated successfully!")
    print(f"Output directory: {PLOT_DIR}")


if __name__ == "__main__":
    main()
