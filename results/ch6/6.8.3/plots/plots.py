#!/usr/bin/env python3
"""
RQ 6.8.3: ICC Comparison Plot - Confidence vs Accuracy Pattern
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

RQ_DIR = Path(__file__).resolve().parents[1]

def plot_correlation_comparison():
    """
    Create comparison plot showing intercept-slope correlations for
    accuracy (Ch5 5.5.6) vs confidence (Ch6 6.8.3).
    """
    # Load comparison data
    df = pd.read_csv(RQ_DIR / "data" / "step05_ch5_comparison.csv")

    fig, ax = plt.subplots(figsize=(10, 6))

    # Data
    locations = df['location_type'].tolist()
    r_acc = df['correlation_accuracy'].tolist()
    r_conf = df['correlation_confidence'].tolist()

    x = np.arange(len(locations))
    width = 0.35

    # Bars
    bars_acc = ax.bar(x - width/2, r_acc, width, label='Accuracy (Ch5 5.5.6)',
                      color='steelblue', alpha=0.8)
    bars_conf = ax.bar(x + width/2, r_conf, width, label='Confidence (Ch6 6.8.3)',
                       color='coral', alpha=0.8)

    # Reference line at 0
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.7)

    # Labels and formatting
    ax.set_xlabel('Location Type', fontsize=12)
    ax.set_ylabel('Intercept-Slope Correlation (r)', fontsize=12)
    ax.set_title('RQ 6.8.3: Opposite Correlation Pattern Does NOT Replicate\n(Accuracy: Opposite Signs, Confidence: Same Sign)',
                 fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(locations)
    ax.legend(loc='upper right', fontsize=10)
    ax.set_ylim(-1.1, 1.1)
    ax.grid(True, alpha=0.3, axis='y')

    # Add value labels on bars
    for bar, val in zip(bars_acc, r_acc):
        ax.annotate(f'{val:+.2f}',
                   xy=(bar.get_x() + bar.get_width()/2, val),
                   ha='center', va='bottom' if val > 0 else 'top',
                   fontsize=10, fontweight='bold')

    for bar, val in zip(bars_conf, r_conf):
        ax.annotate(f'{val:+.2f}',
                   xy=(bar.get_x() + bar.get_width()/2, val),
                   ha='center', va='bottom' if val > 0 else 'top',
                   fontsize=10, fontweight='bold')

    # Annotation box
    ax.annotate(
        'Accuracy: Source (+) vs Dest (-) = OPPOSITE\n'
        'Confidence: Source (-) vs Dest (-) = SAME\n'
        'Pattern does NOT replicate',
        xy=(0.02, 0.02), xycoords='axes fraction',
        ha='left', va='bottom',
        fontsize=9,
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8)
    )

    plt.tight_layout()

    # Save
    output_path = RQ_DIR / "plots" / "icc_correlation_comparison.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Saved: {output_path}")

    plt.close()

def main():
    print("Generating RQ 6.8.3 plots...")
    plot_correlation_comparison()
    print("Done.")

if __name__ == "__main__":
    main()
