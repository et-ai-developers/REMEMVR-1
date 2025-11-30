#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Manual plotting script for RQ 5.12 - CTT-IRT Convergence via Item Purification

Generates:
1. Correlation comparison: Grouped bar chart (Full vs Purified CTT-IRT correlations)
2. AIC comparison: Bar chart with delta_AIC reference lines

Created: 2025-11-30
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
PLOTS_DIR = BASE_DIR / "plots"

# Input CSVs
correlation_csv = PLOTS_DIR / "step08_correlation_comparison_data.csv"
aic_csv = PLOTS_DIR / "step08_aic_comparison_data.csv"

# Output PNGs
correlation_png = PLOTS_DIR / "correlation_comparison.png"
aic_png = PLOTS_DIR / "aic_comparison.png"


def set_style():
    """Set publication-quality plot style"""
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.rcParams.update({
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 13,
        'xtick.labelsize': 11,
        'ytick.labelsize': 11,
        'legend.fontsize': 10,
        'figure.titlesize': 14,
        'figure.dpi': 300
    })


def plot_correlation_comparison():
    """
    Plot 1: Grouped bar chart comparing Full CTT vs Purified CTT correlations with IRT
    """
    # Load data
    df = pd.read_csv(correlation_csv)

    # Setup
    domains = ['What', 'Where', 'When']
    domain_order = {d: i for i, d in enumerate(domains)}
    df['domain_order'] = df['domain'].map(domain_order)
    df = df.sort_values('domain_order')

    # Extract values
    full_ctt = df[df['measurement_type'] == 'Full CTT']['correlation'].values
    purified_ctt = df[df['measurement_type'] == 'Purified CTT']['correlation'].values
    significance = df[df['measurement_type'] == 'Purified CTT']['significance'].values

    # Bar positions
    x = np.arange(len(domains))
    width = 0.35

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Bars
    bars1 = ax.bar(x - width/2, full_ctt, width, label='Full CTT-IRT', color='steelblue', alpha=0.8)
    bars2 = ax.bar(x + width/2, purified_ctt, width, label='Purified CTT-IRT', color='darkorange', alpha=0.8)

    # Add significance markers
    for i, sig in enumerate(significance):
        if sig:  # If significant
            # Add asterisk above purified CTT bar
            height = purified_ctt[i]
            ax.text(x[i] + width/2, height + 0.02, '*', ha='center', va='bottom', fontsize=16, fontweight='bold')

    # Formatting
    ax.set_xlabel('Memory Domain', fontweight='bold')
    ax.set_ylabel('Correlation with IRT Theta (r)', fontweight='bold')
    ax.set_title('RQ 5.12: CTT-IRT Convergent Validity by Item Purification', fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(domains)
    ax.set_ylim([0, 1.0])
    ax.axhline(y=0.7, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='Adequate (r=0.70)')
    ax.axhline(y=0.9, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='Excellent (r=0.90)')
    ax.legend(loc='lower right')
    ax.grid(axis='y', alpha=0.3)

    # Save
    plt.tight_layout()
    plt.savefig(correlation_png, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"[SUCCESS] Saved: {correlation_png}")


def plot_aic_comparison():
    """
    Plot 2: Bar chart showing delta_AIC with Burnham & Anderson reference lines
    """
    # Load data
    df = pd.read_csv(aic_csv)

    # Extract values
    measurements = df['measurement'].values
    delta_aic = df['delta_AIC'].values
    interpretations = df['interpretation'].values

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Color bars by interpretation
    colors = []
    for interp in interpretations:
        if 'BEST' in interp:
            colors.append('darkgreen')
        elif 'substantially worse' in interp:
            colors.append('darkred')
        else:
            colors.append('steelblue')

    # Bars
    x = np.arange(len(measurements))
    bars = ax.bar(x, delta_aic, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)

    # Add value labels on bars
    for i, (val, interp) in enumerate(zip(delta_aic, interpretations)):
        ax.text(i, val + 3 if val > 0 else val - 3, f'{val:.1f}',
                ha='center', va='bottom' if val > 0 else 'top', fontweight='bold', fontsize=11)

    # Reference lines (Burnham & Anderson 2002)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=2, label='Reference (IRT theta)')
    ax.axhline(y=2, color='orange', linestyle='--', linewidth=1.5, alpha=0.7, label='Weak evidence (ΔAICc = 2)')
    ax.axhline(y=-2, color='orange', linestyle='--', linewidth=1.5, alpha=0.7)
    ax.axhline(y=10, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='Strong evidence (ΔAICc = 10)')
    ax.axhline(y=-10, color='red', linestyle='--', linewidth=1.5, alpha=0.7)

    # Formatting
    ax.set_xlabel('Measurement Type', fontweight='bold')
    ax.set_ylabel('Δ AIC (relative to IRT theta)', fontweight='bold')
    ax.set_title('RQ 5.12: Model Fit Comparison - Forgetting Trajectory LMMs', fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(measurements, rotation=0, ha='center')
    ax.legend(loc='upper right')
    ax.grid(axis='y', alpha=0.3)

    # Add interpretation note
    note = "Negative ΔAICc = better fit than IRT | Positive ΔAICc = worse fit than IRT"
    ax.text(0.5, 0.02, note, ha='center', va='bottom', transform=ax.transAxes,
            fontsize=9, style='italic', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

    # Save
    plt.tight_layout()
    plt.savefig(aic_png, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"[SUCCESS] Saved: {aic_png}")


if __name__ == '__main__':
    print("\n=== RQ 5.12 Plotting Script ===\n")

    # Check inputs exist
    if not correlation_csv.exists():
        raise FileNotFoundError(f"Missing: {correlation_csv}")
    if not aic_csv.exists():
        raise FileNotFoundError(f"Missing: {aic_csv}")

    # Set style
    set_style()

    # Generate plots
    print("Generating Plot 1: Correlation Comparison...")
    plot_correlation_comparison()

    print("Generating Plot 2: AIC Comparison...")
    plot_aic_comparison()

    print("\n=== Plotting Complete ===\n")
    print(f"Output files:")
    print(f"  - {correlation_png}")
    print(f"  - {aic_png}")
