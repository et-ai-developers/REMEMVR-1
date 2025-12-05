#!/usr/bin/env python3
"""
RQ 5.5.7: Scatter Plot Matrix for Source-Destination Clustering

Creates a 4x4 scatter plot matrix showing pairwise relationships among:
- Source_intercept, Source_slope, Destination_intercept, Destination_slope
Colored by cluster membership (K=4 clusters).
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Setup paths
PLOTS_DIR = Path(__file__).parent
DATA_DIR = PLOTS_DIR.parent / "data"

def main():
    """Create scatter plot matrix."""

    # Load data
    plot_data_path = PLOTS_DIR / "step06_cluster_scatter_matrix_data.csv"
    centers_path = DATA_DIR / "step04_cluster_centers.csv"
    char_path = DATA_DIR / "step05_cluster_characterization.csv"

    df = pd.read_csv(plot_data_path)
    df_centers = pd.read_csv(centers_path)
    df_char = pd.read_csv(char_path)

    print(f"Loaded {len(df)} rows for plotting")

    # Feature columns
    feature_cols = ['Source_intercept', 'Source_slope',
                    'Destination_intercept', 'Destination_slope']

    # Get cluster labels for legend
    cluster_labels = {int(row['cluster']): row['label'].split(':')[0]
                     for _, row in df_char.iterrows()}

    # Colors for clusters
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']  # Blue, Orange, Green, Red
    K = df['cluster'].nunique()

    # Create figure
    fig, axes = plt.subplots(4, 4, figsize=(12, 12))
    fig.suptitle('RQ 5.5.7: Source-Destination Memory Clustering\n'
                 f'(K={K}, Silhouette=0.417, Jaccard=0.831)',
                 fontsize=14, fontweight='bold')

    # Create scatter plots
    for i, col_i in enumerate(feature_cols):
        for j, col_j in enumerate(feature_cols):
            ax = axes[i, j]

            if i == j:
                # Diagonal: histograms by cluster
                for k in range(K):
                    cluster_data = df[df['cluster'] == k][col_i]
                    ax.hist(cluster_data, bins=10, alpha=0.6, color=colors[k],
                           label=cluster_labels.get(k, f'C{k}'))
                ax.set_ylabel('')
                ax.set_xlabel(col_i.replace('_', ' ').title() if i == 3 else '')

            else:
                # Off-diagonal: scatter plots
                for k in range(K):
                    cluster_data = df[df['cluster'] == k]
                    ax.scatter(cluster_data[col_j], cluster_data[col_i],
                              c=colors[k], alpha=0.6, s=30,
                              label=cluster_labels.get(k, f'C{k}'))

                # Add cluster centers
                for k in range(K):
                    center_x = df_centers[df_centers['cluster'] == k][col_j].values[0]
                    center_y = df_centers[df_centers['cluster'] == k][col_i].values[0]
                    ax.scatter(center_x, center_y, c=colors[k], marker='X',
                              s=150, edgecolor='black', linewidth=1.5)

                # Add reference lines at z=0
                ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5, linewidth=0.8)
                ax.axvline(x=0, color='gray', linestyle='--', alpha=0.5, linewidth=0.8)

            # Labels
            if i == 0:
                ax.set_title(col_j.replace('_', '\n').title(), fontsize=9)
            if j == 0:
                ax.set_ylabel(col_i.replace('_', '\n').title(), fontsize=9)

            # Remove ticks for inner plots
            if i < 3:
                ax.set_xticklabels([])
            if j > 0:
                ax.set_yticklabels([])

    # Add legend
    handles = [plt.scatter([], [], c=colors[k], s=50,
                          label=cluster_labels.get(k, f'Cluster {k}'))
               for k in range(K)]
    fig.legend(handles, [cluster_labels.get(k, f'Cluster {k}') for k in range(K)],
              loc='lower center', ncol=K, fontsize=9,
              bbox_to_anchor=(0.5, 0.02))

    plt.tight_layout()
    plt.subplots_adjust(top=0.92, bottom=0.08)

    # Save
    output_path = PLOTS_DIR / "step06_cluster_scatter_matrix.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"Saved to {output_path}")

    plt.close()

if __name__ == "__main__":
    main()
