#!/usr/bin/env python3
"""
RQ 6.8.4: Clustering Visualization
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

RQ_DIR = Path(__file__).resolve().parents[1]

def plot_cluster_scatter():
    """
    Create scatter plot of clusters in PCA space.
    """
    # Load data
    df = pd.read_csv(RQ_DIR / "data" / "step07_cluster_scatter_data.csv")

    fig, ax = plt.subplots(figsize=(10, 8))

    # Colors for clusters
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6', '#f39c12']
    markers = ['o', 's', '^', 'D', 'v']

    for cluster in sorted(df['cluster'].unique()):
        subset = df[df['cluster'] == cluster]
        ax.scatter(
            subset['PC1'],
            subset['PC2'],
            c=colors[cluster % len(colors)],
            marker=markers[cluster % len(markers)],
            s=60,
            alpha=0.7,
            label=f'Cluster {cluster} (N={len(subset)})'
        )

    ax.set_xlabel('PC1 (58.4% variance)', fontsize=12)
    ax.set_ylabel('PC2 (34.0% variance)', fontsize=12)
    ax.set_title('RQ 6.8.4: Source-Destination Confidence Clustering\n(Silhouette = 0.33 - Below 0.40 Threshold)', fontsize=14)
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)

    # Add annotation
    ax.annotate(
        'Hypothesis NOT Supported:\nSilhouette=0.33 < 0.40 threshold\n(Ch5 5.5.7 accuracy: 0.417)',
        xy=(0.02, 0.02), xycoords='axes fraction',
        ha='left', va='bottom',
        fontsize=9,
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8)
    )

    plt.tight_layout()

    # Save
    output_path = RQ_DIR / "plots" / "cluster_scatter.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Saved: {output_path}")

    plt.close()

def main():
    print("Generating RQ 6.8.4 plots...")
    plot_cluster_scatter()
    print("Done.")

if __name__ == "__main__":
    main()
