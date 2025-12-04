"""
RQ 5.5.3 Plots - Age Effects on Source-Destination Memory

Generates:
1. age_tertile_trajectory_theta.png - Theta by test for each age tertile x location
2. age_tertile_trajectory_probability.png - Probability scale version
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Setup paths
RQ_DIR = Path(__file__).parent.parent
DATA_DIR = RQ_DIR / "data"
PLOTS_DIR = RQ_DIR / "plots"

# IRT parameters from RQ 5.5.1 for probability conversion
FACTOR_PARAMS = {
    'Source': {'discrimination': 1.096, 'difficulty': -0.453},
    'Destination': {'discrimination': 0.873, 'difficulty': 1.371}
}


def convert_theta_to_probability(theta, discrimination, difficulty):
    """Convert theta to probability using 2PL IRT model."""
    logit = discrimination * (theta - difficulty)
    return 1 / (1 + np.exp(-logit))


def main():
    print("[PLOTS] RQ 5.5.3 - Age Effects on Source-Destination Memory")

    # Load plot data
    plot_data = pd.read_csv(DATA_DIR / "step05_age_tertile_plot_data.csv")
    print(f"[LOADED] {len(plot_data)} rows from step05_age_tertile_plot_data.csv")

    # Convert test to numeric for plotting
    test_map = {1: 0, 2: 1, 3: 3, 4: 6}  # Days: 0, 1, 3, 6
    plot_data['day'] = plot_data['test'].map(test_map)

    # =========================================================================
    # Plot 1: Theta scale - Age tertile trajectories
    # =========================================================================
    print("[PLOT 1] Age tertile trajectory (theta scale)")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    colors = {'Young': '#2ca02c', 'Middle': '#1f77b4', 'Older': '#d62728'}
    markers = {'Young': 'o', 'Middle': 's', 'Older': '^'}
    tertile_order = ['Young', 'Middle', 'Older']

    for i, location in enumerate(['Source', 'Destination']):
        ax = axes[i]
        loc_data = plot_data[plot_data['location'] == location]

        for tertile in tertile_order:
            tert_data = loc_data[loc_data['age_tertile'] == tertile].sort_values('day')
            ax.errorbar(
                tert_data['day'], tert_data['theta_mean'],
                yerr=1.96 * tert_data['se'],
                label=tertile, color=colors[tertile], marker=markers[tertile],
                capsize=3, capthick=1.5, linewidth=2, markersize=8
            )

        ax.set_xlabel('Days Since Encoding', fontsize=12)
        ax.set_ylabel('Theta (IRT Ability)', fontsize=12)
        ax.set_title(f'{location} Memory', fontsize=14, fontweight='bold')
        ax.set_xticks([0, 1, 3, 6])
        ax.set_xlim(-0.5, 6.5)
        ax.grid(True, alpha=0.3)
        ax.legend(title='Age Tertile', loc='upper right')

    plt.suptitle('RQ 5.5.3: Age Effects on Source-Destination Memory\n'
                 '(Theta Scale - No Significant Age x Location x Time Interaction)',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "age_tertile_trajectory_theta.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("[SAVED] age_tertile_trajectory_theta.png")

    # =========================================================================
    # Plot 2: Probability scale - with factor-specific conversion
    # =========================================================================
    print("[PLOT 2] Age tertile trajectory (probability scale)")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for i, location in enumerate(['Source', 'Destination']):
        ax = axes[i]
        loc_data = plot_data[plot_data['location'] == location].copy()

        # Convert theta to probability using factor-specific parameters
        params = FACTOR_PARAMS[location]
        loc_data['prob_mean'] = convert_theta_to_probability(
            loc_data['theta_mean'], params['discrimination'], params['difficulty']
        )
        # Approximate probability SE using delta method
        # d(prob)/d(theta) = a * prob * (1 - prob)
        loc_data['prob_deriv'] = params['discrimination'] * loc_data['prob_mean'] * (1 - loc_data['prob_mean'])
        loc_data['prob_se'] = loc_data['se'] * loc_data['prob_deriv']

        for tertile in tertile_order:
            tert_data = loc_data[loc_data['age_tertile'] == tertile].sort_values('day')
            ax.errorbar(
                tert_data['day'], tert_data['prob_mean'] * 100,
                yerr=1.96 * tert_data['prob_se'] * 100,
                label=tertile, color=colors[tertile], marker=markers[tertile],
                capsize=3, capthick=1.5, linewidth=2, markersize=8
            )

        ax.set_xlabel('Days Since Encoding', fontsize=12)
        ax.set_ylabel('Accuracy (%)', fontsize=12)
        ax.set_title(f'{location} Memory', fontsize=14, fontweight='bold')
        ax.set_xticks([0, 1, 3, 6])
        ax.set_xlim(-0.5, 6.5)
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3)
        ax.legend(title='Age Tertile', loc='upper right')

    plt.suptitle('RQ 5.5.3: Age Effects on Source-Destination Memory\n'
                 '(Probability Scale - No Significant Age x Location x Time Interaction)',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "age_tertile_trajectory_probability.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("[SAVED] age_tertile_trajectory_probability.png")

    # =========================================================================
    # Plot 3: Combined dual-scale plot (2x2 grid)
    # =========================================================================
    print("[PLOT 3] Dual-scale combined plot")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Top row: Theta scale
    for i, location in enumerate(['Source', 'Destination']):
        ax = axes[0, i]
        loc_data = plot_data[plot_data['location'] == location]

        for tertile in tertile_order:
            tert_data = loc_data[loc_data['age_tertile'] == tertile].sort_values('day')
            ax.errorbar(
                tert_data['day'], tert_data['theta_mean'],
                yerr=1.96 * tert_data['se'],
                label=tertile, color=colors[tertile], marker=markers[tertile],
                capsize=3, capthick=1.5, linewidth=2, markersize=8
            )

        ax.set_xlabel('Days Since Encoding', fontsize=11)
        ax.set_ylabel('Theta (IRT Ability)', fontsize=11)
        ax.set_title(f'{location} Memory (Theta)', fontsize=12, fontweight='bold')
        ax.set_xticks([0, 1, 3, 6])
        ax.set_xlim(-0.5, 6.5)
        ax.grid(True, alpha=0.3)
        if i == 1:
            ax.legend(title='Age Tertile', loc='upper right')

    # Bottom row: Probability scale
    for i, location in enumerate(['Source', 'Destination']):
        ax = axes[1, i]
        loc_data = plot_data[plot_data['location'] == location].copy()

        params = FACTOR_PARAMS[location]
        loc_data['prob_mean'] = convert_theta_to_probability(
            loc_data['theta_mean'], params['discrimination'], params['difficulty']
        )
        loc_data['prob_deriv'] = params['discrimination'] * loc_data['prob_mean'] * (1 - loc_data['prob_mean'])
        loc_data['prob_se'] = loc_data['se'] * loc_data['prob_deriv']

        for tertile in tertile_order:
            tert_data = loc_data[loc_data['age_tertile'] == tertile].sort_values('day')
            ax.errorbar(
                tert_data['day'], tert_data['prob_mean'] * 100,
                yerr=1.96 * tert_data['prob_se'] * 100,
                label=tertile, color=colors[tertile], marker=markers[tertile],
                capsize=3, capthick=1.5, linewidth=2, markersize=8
            )

        ax.set_xlabel('Days Since Encoding', fontsize=11)
        ax.set_ylabel('Accuracy (%)', fontsize=11)
        ax.set_title(f'{location} Memory (Probability)', fontsize=12, fontweight='bold')
        ax.set_xticks([0, 1, 3, 6])
        ax.set_xlim(-0.5, 6.5)
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3)
        if i == 1:
            ax.legend(title='Age Tertile', loc='upper right')

    plt.suptitle('RQ 5.5.3: Age Effects on Source-Destination Memory\n'
                 'Primary Hypothesis SUPPORTED (NULL): Age Does NOT Moderate Source-Destination Forgetting\n'
                 '3-way Interaction: p=0.16 (TSVR), p=0.33 (log_TSVR), Power=1.00',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "age_tertile_dual_scale.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("[SAVED] age_tertile_dual_scale.png")

    print("[SUCCESS] All plots generated")


if __name__ == "__main__":
    main()
