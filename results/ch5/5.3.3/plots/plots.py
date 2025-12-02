#!/usr/bin/env python3
"""
Plotting script for RQ 5.3.3 - Paradigm Consolidation Window

Generates piecewise trajectory visualization showing forgetting rates
across paradigms (IFR, ICR, IRE) during Early (consolidation) vs Late
(decay) temporal segments.

Decision D069 compliance: Dual-scale plots (theta + probability).
"""

import sys
from pathlib import Path

import pandas as pd

# Setup paths
SCRIPT_DIR = Path(__file__).resolve().parent
RQ_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = RQ_DIR.parents[2]

# Add project root to path for imports
sys.path.insert(0, str(PROJECT_ROOT))

from tools.plotting import plot_piecewise_trajectory, set_plot_style_defaults


def main():
    """Generate piecewise trajectory plots."""
    print("=" * 60)
    print("RQ 5.3.3 - Generating Piecewise Trajectory Plots")
    print("=" * 60)

    # Set consistent styling
    set_plot_style_defaults()

    # Define paths
    theta_file = RQ_DIR / "data" / "step06_piecewise_theta_data.csv"
    prob_file = RQ_DIR / "data" / "step06_piecewise_probability_data.csv"
    output_file = RQ_DIR / "plots" / "piecewise_trajectory.png"

    # Load data
    print(f"Loading theta data from: {theta_file}")
    theta_data = pd.read_csv(theta_file)
    print(f"  Rows: {len(theta_data)}")

    print(f"Loading probability data from: {prob_file}")
    prob_data = pd.read_csv(prob_file)
    print(f"  Rows: {len(prob_data)}")

    # Generate plot
    print("\nGenerating piecewise trajectory plot...")
    fig, axes = plot_piecewise_trajectory(
        theta_data=theta_data,
        prob_data=prob_data,
        segment_col='Segment',
        paradigm_col='paradigm',
        time_col='Days_within',
        theta_obs_col='theta_observed',
        theta_pred_col='theta_predicted',
        prob_obs_col='prob_observed',
        prob_pred_col='prob_predicted',
        ci_lower_col='CI_lower',
        ci_upper_col='CI_upper',
        slope_col='slope',
        data_type_col='data_type',
        segment_order=['Early', 'Late'],
        paradigm_colors={
            'IFR': '#E74C3C',  # Red - Free Recall
            'ICR': '#3498DB',  # Blue - Cued Recall
            'IRE': '#2ECC71'   # Green - Recognition
        },
        figsize=(14, 6),
        output_path=output_file,
        suptitle='RQ 5.3.3: Paradigm Consolidation Window (Early vs Late Segments)'
    )

    print(f"\nPlot saved: {output_file}")
    print(f"  Size: {output_file.stat().st_size / 1024:.1f} KB")

    print("\n" + "=" * 60)
    print("PLOTTING COMPLETE")
    print("=" * 60)

    return fig, axes


if __name__ == "__main__":
    main()
