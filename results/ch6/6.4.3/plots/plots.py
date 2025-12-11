#!/usr/bin/env python3
"""
RQ 6.4.3: Age x Paradigm Interaction Plots
==========================================
Generates visualizations for Age x Paradigm x Time 3-way interaction test.

Plots:
1. Age tertile trajectories by paradigm (3x3 facet grid)
2. Interaction effect sizes bar chart
3. Age effect summary (forest plot style)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Configuration
RQ_DIR = Path(__file__).resolve().parents[1]  # results/ch6/6.4.3
PLOTS_DIR = RQ_DIR / "plots"
DATA_DIR = RQ_DIR / "data"

# Load data
df = pd.read_csv(DATA_DIR / "step00_lmm_input.csv")
interaction_df = pd.read_csv(DATA_DIR / "step02_interaction_terms.csv")
effect_sizes = pd.read_csv(DATA_DIR / "step03_effect_sizes.csv")


def plot_age_tertile_trajectories():
    """
    Plot 1: Age tertile trajectories by paradigm.

    Shows theta confidence trajectories for Low/Medium/High age tertiles
    across the three paradigms (IFR, ICR, IRE).
    """
    # Compute age tertiles
    age_per_uid = df.groupby('UID')['Age'].first()
    p33 = age_per_uid.quantile(0.33)
    p67 = age_per_uid.quantile(0.67)

    def assign_tertile(age):
        if age <= p33:
            return 'Young'
        elif age <= p67:
            return 'Middle'
        else:
            return 'Older'

    df['age_tertile'] = df['Age'].apply(assign_tertile)

    # Aggregate by age_tertile x paradigm x test
    agg = df.groupby(['age_tertile', 'Paradigm', 'test']).agg(
        mean_theta=('theta_confidence', 'mean'),
        se_theta=('theta_confidence', lambda x: x.std() / np.sqrt(len(x))),
        N=('theta_confidence', 'count')
    ).reset_index()

    # Map test to numeric for plotting
    test_map = {'T1': 0, 'T2': 1, 'T3': 3, 'T4': 6}  # Nominal days
    agg['day'] = agg['test'].map(test_map)

    # Create figure
    fig, axes = plt.subplots(1, 3, figsize=(14, 5), sharey=True)

    paradigms = ['IFR', 'ICR', 'IRE']
    paradigm_names = {'IFR': 'Free Recall', 'ICR': 'Cued Recall', 'IRE': 'Recognition'}
    colors = {'Young': '#2ecc71', 'Middle': '#3498db', 'Older': '#e74c3c'}

    for ax, paradigm in zip(axes, paradigms):
        para_data = agg[agg['Paradigm'] == paradigm]

        for tertile in ['Young', 'Middle', 'Older']:
            tertile_data = para_data[para_data['age_tertile'] == tertile].sort_values('day')
            ax.errorbar(
                tertile_data['day'],
                tertile_data['mean_theta'],
                yerr=1.96 * tertile_data['se_theta'],
                marker='o',
                markersize=8,
                linewidth=2,
                color=colors[tertile],
                label=tertile,
                capsize=4
            )

        ax.set_xlabel('Days Since Encoding', fontsize=11)
        ax.set_title(paradigm_names[paradigm], fontsize=12, fontweight='bold')
        ax.set_xticks([0, 1, 3, 6])
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)

    axes[0].set_ylabel('Confidence (θ)', fontsize=11)
    axes[0].legend(title='Age Tertile', loc='lower left')

    fig.suptitle('RQ 6.4.3: Age × Paradigm × Time Interaction\n(NULL: Parallel trajectories across age groups)',
                 fontsize=13, fontweight='bold')
    plt.tight_layout()

    # Save
    output_path = PLOTS_DIR / "age_tertile_trajectories_by_paradigm.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")


def plot_effect_sizes():
    """
    Plot 2: Effect sizes bar chart.

    Shows Cohen's f² for each Age_c-related term.
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    # Prepare data
    terms = effect_sizes['term'].values
    f_squared = effect_sizes['f_squared'].values

    # Clean term names for display
    display_terms = ['Age (main)', 'Age × Time', 'Age × Paradigm × Time']

    # Color by interpretation
    colors = []
    for f2 in f_squared:
        if f2 < 0.02:
            colors.append('#95a5a6')  # Gray for negligible
        elif f2 < 0.15:
            colors.append('#3498db')  # Blue for small
        elif f2 < 0.35:
            colors.append('#f39c12')  # Orange for medium
        else:
            colors.append('#e74c3c')  # Red for large

    bars = ax.barh(display_terms, f_squared, color=colors, edgecolor='black')

    # Add value labels
    for bar, f2 in zip(bars, f_squared):
        width = bar.get_width()
        ax.text(width + 0.002, bar.get_y() + bar.get_height()/2,
                f'f² = {f2:.4f}', va='center', fontsize=10)

    # Add threshold lines
    ax.axvline(x=0.02, color='gray', linestyle='--', alpha=0.7, label='Small (0.02)')
    ax.axvline(x=0.15, color='gray', linestyle=':', alpha=0.7, label='Medium (0.15)')

    ax.set_xlabel("Cohen's f²", fontsize=11)
    ax.set_title("RQ 6.4.3: Effect Sizes for Age-Related Terms", fontsize=12, fontweight='bold')
    ax.set_xlim(0, max(f_squared) * 1.5)
    ax.legend(loc='lower right', fontsize=9)

    plt.tight_layout()

    # Save
    output_path = PLOTS_DIR / "effect_sizes.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")


def plot_interaction_summary():
    """
    Plot 3: Forest plot style summary of interaction tests.

    Shows p-values with Bonferroni threshold.
    """
    fig, ax = plt.subplots(figsize=(9, 4))

    # Prepare data
    terms = interaction_df['term'].values
    p_uncorr = interaction_df['p_wald_uncorrected'].values
    p_bonf = interaction_df['p_wald_bonferroni'].values

    # Clean term names
    display_terms = ['Age (main)', 'Age × Time', 'Age × Paradigm × Time\n(PRIMARY TEST)']
    y_pos = np.arange(len(terms))

    # Plot uncorrected and Bonferroni-corrected p-values
    bars1 = ax.barh(y_pos - 0.2, -np.log10(p_uncorr + 1e-10), height=0.35,
                    color='#3498db', label='Uncorrected', alpha=0.8)
    bars2 = ax.barh(y_pos + 0.2, -np.log10(p_bonf + 1e-10), height=0.35,
                    color='#e74c3c', label='Bonferroni', alpha=0.8)

    # Add threshold lines
    ax.axvline(x=-np.log10(0.05), color='green', linestyle='--', linewidth=2,
               label='α = 0.05')
    ax.axvline(x=-np.log10(0.0167), color='orange', linestyle='--', linewidth=2,
               label='α = 0.0167 (Bonferroni)')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(display_terms)
    ax.set_xlabel('-log₁₀(p)', fontsize=11)
    ax.set_title('RQ 6.4.3: Significance of Age-Related Terms\n(Higher = More Significant)',
                 fontsize=12, fontweight='bold')
    ax.legend(loc='upper right', fontsize=9)

    # Add p-value annotations
    for i, (pu, pb) in enumerate(zip(p_uncorr, p_bonf)):
        ax.text(0.2, i - 0.2, f'p = {pu:.3f}', va='center', fontsize=9)
        ax.text(0.2, i + 0.2, f'p = {pb:.3f}', va='center', fontsize=9)

    plt.tight_layout()

    # Save
    output_path = PLOTS_DIR / "interaction_significance.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")


def main():
    """Generate all plots for RQ 6.4.3."""
    print("Generating RQ 6.4.3 plots...")

    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    plot_age_tertile_trajectories()
    plot_effect_sizes()
    plot_interaction_summary()

    print("\nAll plots generated successfully!")


if __name__ == "__main__":
    main()
