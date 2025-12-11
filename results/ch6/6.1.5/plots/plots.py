#!/usr/bin/env python3
"""
RQ 6.1.5: Trajectory Clustering - Plots
========================================

Generates:
1. cluster_scatter.png - 2D scatter of intercept vs slope with cluster colors
2. bic_elbow.png - BIC values across K=2-6
3. crosstab_heatmap.png - Heatmap of confidence x accuracy clusters

Author: Claude Code (rq_plots agent)
Date: 2025-12-11
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration
RQ_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = RQ_DIR / "data"
PLOTS_DIR = RQ_DIR / "plots"

# Style
plt.style.use('seaborn-v0_8-whitegrid')
COLORS = ['#2ecc71', '#3498db', '#e74c3c', '#9b59b6', '#f39c12', '#1abc9c']

def plot_cluster_scatter():
    """2D scatter plot of intercept vs slope with cluster colors."""
    # Load cluster assignments
    df = pd.read_csv(DATA_DIR / "step04_cluster_assignments.csv")

    # Load cluster characterization for phenotype labels
    char_df = pd.read_csv(DATA_DIR / "step06_cluster_characterization.csv")
    phenotype_map = dict(zip(char_df['cluster_label'], char_df['phenotype']))

    # Load cluster centers
    centers = pd.read_csv(DATA_DIR / "step04_cluster_centers.csv")

    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot each cluster
    for cluster_id in sorted(df['cluster_label'].unique()):
        mask = df['cluster_label'] == cluster_id
        cluster_data = df[mask]
        phenotype = phenotype_map.get(cluster_id, f"Cluster {cluster_id}")
        n = len(cluster_data)

        ax.scatter(
            cluster_data['intercept_z'],
            cluster_data['slope_z'],
            c=COLORS[cluster_id % len(COLORS)],
            alpha=0.7,
            s=80,
            label=f"{phenotype} (N={n})",
            edgecolors='white',
            linewidth=0.5
        )

    # Plot cluster centers
    for _, center in centers.iterrows():
        ax.scatter(
            center['intercept_z'],
            center['slope_z'],
            c='black',
            marker='X',
            s=200,
            edgecolors='white',
            linewidth=2,
            zorder=10
        )

    ax.set_xlabel('Baseline Confidence (Intercept, z-score)', fontsize=12)
    ax.set_ylabel('Confidence Decline Rate (Slope, z-score)', fontsize=12)
    ax.set_title('RQ 6.1.5: Confidence Trajectory Phenotypes\n(K-means Clustering, K=3)', fontsize=14)

    # Add reference lines
    ax.axhline(0, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(0, color='gray', linestyle='--', alpha=0.5)

    ax.legend(loc='upper left', fontsize=10)

    plt.tight_layout()
    output_path = PLOTS_DIR / "cluster_scatter.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path.name}")

    return output_path

def plot_bic_elbow():
    """BIC elbow curve for K selection."""
    df = pd.read_csv(DATA_DIR / "step03_cluster_selection.csv")

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.plot(df['K'], df['BIC'], 'o-', color='#3498db', linewidth=2, markersize=10)

    # Mark K=3 (selected)
    k3_row = df[df['K'] == 3].iloc[0]
    ax.scatter([3], [k3_row['BIC']], color='#e74c3c', s=200, zorder=10,
               marker='*', label='K=3 (selected, matched to Ch5 5.1.5)')

    ax.set_xlabel('Number of Clusters (K)', fontsize=12)
    ax.set_ylabel('BIC', fontsize=12)
    ax.set_title('RQ 6.1.5: BIC Elbow Analysis\n(K=3 selected for Ch5 5.1.5 comparability)', fontsize=14)
    ax.set_xticks(df['K'])

    ax.legend(loc='upper right', fontsize=10)

    # Add note about BIC trend
    ax.annotate('BIC monotonically decreases\n(not reliable for K selection)',
                xy=(5, df[df['K']==5]['BIC'].values[0]),
                xytext=(4.5, df[df['K']==3]['BIC'].values[0] + 30),
                fontsize=9, color='gray',
                arrowprops=dict(arrowstyle='->', color='gray'))

    plt.tight_layout()
    output_path = PLOTS_DIR / "bic_elbow.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path.name}")

    return output_path

def plot_crosstab_heatmap():
    """Heatmap of confidence x accuracy cluster cross-tabulation."""
    # Load crosstab
    crosstab = pd.read_csv(DATA_DIR / "step07_crosstab_confidence_accuracy.csv", index_col=0)

    # Load phenotype labels for confidence clusters
    conf_char = pd.read_csv(DATA_DIR / "step06_cluster_characterization.csv")
    conf_phenotypes = dict(zip(conf_char['cluster_label'], conf_char['phenotype']))

    # Create labels
    conf_labels = [f"Conf {i}\n({conf_phenotypes.get(i, '?')})" for i in crosstab.index]
    acc_labels = [f"Acc {col}" for col in crosstab.columns]

    fig, ax = plt.subplots(figsize=(10, 8))

    # Create heatmap
    sns.heatmap(
        crosstab,
        annot=True,
        fmt='d',
        cmap='Blues',
        ax=ax,
        cbar_kws={'label': 'Count'},
        xticklabels=acc_labels,
        yticklabels=conf_labels,
        linewidths=1,
        linecolor='white'
    )

    ax.set_xlabel('Ch5 5.1.5 Accuracy Clusters', fontsize=12)
    ax.set_ylabel('RQ 6.1.5 Confidence Clusters', fontsize=12)
    ax.set_title('Cross-Tabulation: Confidence × Accuracy Phenotypes\n' +
                 'χ² = 34.34, p < 0.000001, V = 0.41 (INTEGRATED)', fontsize=14)

    plt.tight_layout()
    output_path = PLOTS_DIR / "crosstab_heatmap.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path.name}")

    return output_path

def main():
    """Generate all plots for RQ 6.1.5."""
    print("RQ 6.1.5: Generating plots...")
    print("=" * 50)

    plot_cluster_scatter()
    plot_bic_elbow()
    plot_crosstab_heatmap()

    print("=" * 50)
    print("All plots generated successfully.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
