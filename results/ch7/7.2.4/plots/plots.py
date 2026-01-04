#!/usr/bin/env python3
"""
Generate plots for RQ 7.2.4 - VR Scaffolding Validation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Setup
RQ_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = RQ_DIR / "data"
PLOT_DIR = RQ_DIR / "plots"

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def main():
    print("Generating plots for RQ 7.2.4...")
    
    # Load data
    df_merged = pd.read_csv(DATA_DIR / "step03_merged_data.csv")
    df_corr = pd.read_csv(DATA_DIR / "step03_correlations.csv")
    df_sensitivity = pd.read_csv(DATA_DIR / "step06_sensitivity_age_groups.csv")
    
    # Plot 1: Side-by-side Age Correlation Scatterplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # RAVLT vs Age
    ax1.scatter(df_merged['Age'], df_merged['RAVLT_Total'], alpha=0.6, s=50)
    z = np.polyfit(df_merged['Age'], df_merged['RAVLT_Total'], 1)
    p = np.poly1d(z)
    ax1.plot(df_merged['Age'], p(df_merged['Age']), "r-", alpha=0.8, linewidth=2)
    
    r_ravlt = df_corr[df_corr['variable_pair'] == 'Age_RAVLT']['r'].iloc[0]
    p_ravlt = df_corr[df_corr['variable_pair'] == 'Age_RAVLT']['p_uncorrected'].iloc[0]
    
    ax1.set_xlabel('Age (years)', fontsize=12)
    ax1.set_ylabel('RAVLT Total Score', fontsize=12)
    ax1.set_title('Traditional Test: RAVLT vs Age', fontsize=14, fontweight='bold')
    ax1.text(0.05, 0.95, f'r = {r_ravlt:.3f}\np = {p_ravlt:.4f}', 
             transform=ax1.transAxes, fontsize=11, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # REMEMVR vs Age
    ax2.scatter(df_merged['Age'], df_merged['theta_all'], alpha=0.6, s=50)
    z = np.polyfit(df_merged['Age'], df_merged['theta_all'], 1)
    p = np.poly1d(z)
    ax2.plot(df_merged['Age'], p(df_merged['Age']), "b-", alpha=0.8, linewidth=2)
    
    r_rememvr = df_corr[df_corr['variable_pair'] == 'Age_REMEMVR']['r'].iloc[0]
    p_rememvr = df_corr[df_corr['variable_pair'] == 'Age_REMEMVR']['p_uncorrected'].iloc[0]
    
    ax2.set_xlabel('Age (years)', fontsize=12)
    ax2.set_ylabel('REMEMVR Theta Score', fontsize=12)
    ax2.set_title('VR Test: REMEMVR vs Age', fontsize=14, fontweight='bold')
    ax2.text(0.05, 0.95, f'r = {r_rememvr:.3f}\np = {p_rememvr:.4f}', 
             transform=ax2.transAxes, fontsize=11, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    
    plt.suptitle('VR Scaffolding Hypothesis: Age Correlation Comparison', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "scaffolding_comparison.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # Plot 2: Correlation Comparison Bar Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    tests = ['RAVLT\n(Traditional)', 'REMEMVR\n(VR-based)']
    correlations = [abs(r_ravlt), abs(r_rememvr)]
    
    # Get raw CI values (may be negative)
    ci_lower_ravlt = df_corr[df_corr['variable_pair'] == 'Age_RAVLT']['ci_lower'].iloc[0]
    ci_upper_ravlt = df_corr[df_corr['variable_pair'] == 'Age_RAVLT']['ci_upper'].iloc[0]
    ci_lower_rememvr = df_corr[df_corr['variable_pair'] == 'Age_REMEMVR']['ci_lower'].iloc[0]
    ci_upper_rememvr = df_corr[df_corr['variable_pair'] == 'Age_REMEMVR']['ci_upper'].iloc[0]
    
    # For absolute correlations, convert CI bounds appropriately
    ci_lower = [abs(ci_upper_ravlt) - abs(r_ravlt),  # Lower error for absolute value
                abs(ci_upper_rememvr) - abs(r_rememvr)]
    ci_upper = [abs(ci_lower_ravlt) - abs(r_ravlt),  # Upper error for absolute value
                abs(ci_lower_rememvr) - abs(r_rememvr)]
    
    # Ensure errors are positive
    errors = [[max(0, -c) for c in ci_lower],
              [max(0, c) for c in ci_upper]]
    
    bars = ax.bar(tests, correlations, yerr=errors, capsize=10, 
                  color=['coral', 'skyblue'], edgecolor='black', linewidth=2)
    
    ax.set_ylabel('Absolute Age Correlation |r|', fontsize=12)
    ax.set_title('Age-Related Decline: Traditional vs VR Assessment', fontsize=14, fontweight='bold')
    ax.set_ylim([0, 0.5])
    
    # Add significance indicators
    ax.text(0, correlations[0] + 0.02, '**' if p_ravlt < 0.01 else '*' if p_ravlt < 0.05 else 'ns',
            ha='center', fontsize=12, fontweight='bold')
    ax.text(1, correlations[1] + 0.02, '**' if p_rememvr < 0.01 else '*' if p_rememvr < 0.05 else 'ns',
            ha='center', fontsize=12, fontweight='bold')
    
    # Add interpretation
    diff = correlations[0] - correlations[1]
    ax.text(0.5, 0.45, f'Difference = {diff:.3f}\n(Steiger Z-test p = 0.221)',
            ha='center', fontsize=11, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
    
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "correlation_comparison.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # Plot 3: Age-Stratified Analysis
    fig, ax = plt.subplots(figsize=(10, 6))
    
    younger = df_sensitivity[df_sensitivity['age_group'] == 'younger_adults']
    older = df_sensitivity[df_sensitivity['age_group'] == 'older_adults']
    
    x = np.arange(2)
    width = 0.35
    
    younger_corrs = [abs(younger[younger['variable_pair'] == 'Age_RAVLT']['r'].iloc[0]),
                     abs(younger[younger['variable_pair'] == 'Age_REMEMVR']['r'].iloc[0])]
    older_corrs = [abs(older[older['variable_pair'] == 'Age_RAVLT']['r'].iloc[0]),
                   abs(older[older['variable_pair'] == 'Age_REMEMVR']['r'].iloc[0])]
    
    bars1 = ax.bar(x - width/2, younger_corrs, width, label='Younger Adults (<45y)', color='lightgreen')
    bars2 = ax.bar(x + width/2, older_corrs, width, label='Older Adults (>45y)', color='lightcoral')
    
    ax.set_ylabel('Absolute Age Correlation |r|', fontsize=12)
    ax.set_title('Age-Stratified Analysis: Differential Patterns', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(['RAVLT', 'REMEMVR'])
    ax.legend()
    ax.set_ylim([0, 0.6])
    
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "age_stratified_analysis.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Generated 3 plots in {PLOT_DIR}")
    
    # Also save individual scatterplots as requested
    # Age vs RAVLT only
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df_merged['Age'], df_merged['RAVLT_Total'], alpha=0.6, s=50, color='coral')
    z = np.polyfit(df_merged['Age'], df_merged['RAVLT_Total'], 1)
    p = np.poly1d(z)
    ax.plot(df_merged['Age'], p(df_merged['Age']), "r-", alpha=0.8, linewidth=2)
    ax.set_xlabel('Age (years)', fontsize=12)
    ax.set_ylabel('RAVLT Total Score', fontsize=12)
    ax.set_title('RAVLT Shows Age-Related Decline', fontsize=14, fontweight='bold')
    ax.text(0.05, 0.95, f'r = {r_ravlt:.3f}\np = {p_ravlt:.4f}', 
            transform=ax.transAxes, fontsize=11, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "age_ravlt_scatter.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # Age vs REMEMVR only
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df_merged['Age'], df_merged['theta_all'], alpha=0.6, s=50, color='skyblue')
    z = np.polyfit(df_merged['Age'], df_merged['theta_all'], 1)
    p = np.poly1d(z)
    ax.plot(df_merged['Age'], p(df_merged['Age']), "b-", alpha=0.8, linewidth=2)
    ax.set_xlabel('Age (years)', fontsize=12)
    ax.set_ylabel('REMEMVR Theta Score', fontsize=12)
    ax.set_title('REMEMVR Shows Age-Invariance', fontsize=14, fontweight='bold')
    ax.text(0.05, 0.95, f'r = {r_rememvr:.3f}\np = {p_rememvr:.4f}', 
            transform=ax.transAxes, fontsize=11, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "age_rememvr_scatter.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("All plots generated successfully")

if __name__ == "__main__":
    main()