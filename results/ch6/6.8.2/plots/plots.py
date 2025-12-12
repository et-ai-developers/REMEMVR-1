#!/usr/bin/env python3
"""
RQ 6.8.2: Calibration by Location Type - Plot Generation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add project root to path for tools import
PROJECT_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(PROJECT_ROOT))

RQ_DIR = Path(__file__).resolve().parents[1]

def plot_calibration_by_location():
    """
    Create trajectory plot showing calibration over time by LocationType.
    Horizontal reference line at calibration = 0 (perfect calibration).
    """
    # Load plot data
    plot_data = pd.read_csv(RQ_DIR / "data" / "step03_calibration_plot_data.csv")

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Colors for location types
    colors = {'Source': '#2ecc71', 'Destination': '#e74c3c'}
    markers = {'Source': 'o', 'Destination': 's'}

    # Plot each location type
    for loc in ['Source', 'Destination']:
        subset = plot_data[plot_data['LocationType'] == loc].sort_values('TSVR_hours')

        ax.errorbar(
            subset['TSVR_hours'],
            subset['mean_calibration'],
            yerr=[subset['mean_calibration'] - subset['CI_lower'],
                  subset['CI_upper'] - subset['mean_calibration']],
            label=loc,
            color=colors[loc],
            marker=markers[loc],
            markersize=8,
            linewidth=2,
            capsize=5,
            capthick=2
        )

    # Add horizontal reference line at calibration = 0
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.7, label='Perfect Calibration')

    # Formatting
    ax.set_xlabel('Time Since Encoding (hours)', fontsize=12)
    ax.set_ylabel('Calibration (Z_confidence - Z_accuracy)', fontsize=12)
    ax.set_title('RQ 6.8.2: Source-Destination Calibration Over Time\n(Positive = Overconfidence, Negative = Underconfidence)', fontsize=14)
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)

    # Set y-axis limits to show calibration range
    ax.set_ylim(-0.5, 0.5)

    # Add timepoint labels
    timepoints = {1: 'T1\n(Day 0)', 29: 'T2\n(Day 1)', 79: 'T3\n(Day 3)', 151: 'T4\n(Day 6)'}
    ax.set_xticks([1, 29, 79, 151])
    ax.set_xticklabels([timepoints[t] for t in [1, 29, 79, 151]])

    # Add annotation for non-significant result
    ax.annotate(
        'LocationType effect: p = 0.248 (NS)\nInteraction: p = 0.198 (NS)',
        xy=(0.98, 0.02), xycoords='axes fraction',
        ha='right', va='bottom',
        fontsize=9,
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    )

    plt.tight_layout()

    # Save
    output_path = RQ_DIR / "plots" / "calibration_by_location.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Saved: {output_path}")

    plt.close()

def main():
    print("Generating RQ 6.8.2 plots...")
    plot_calibration_by_location()
    print("Done.")

if __name__ == "__main__":
    main()
