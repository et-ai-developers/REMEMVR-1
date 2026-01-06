#!/usr/bin/env python3
"""
Plot generation for RQ 7.4.3: RPM Predicts Temporal Integration Performance
Creates visualizations showing differential prediction results.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Setup paths
RQ_DIR = Path(__file__).resolve().parents[1]  # results/ch7/7.4.3/
PLOTS_DIR = RQ_DIR / "plots"
DATA_DIR = RQ_DIR / "data"

def load_data():
    """Load all analysis results for plotting."""
    
    # Load datasets
    rpm_data = pd.read_csv(DATA_DIR / "step01_rpm_scores.csv")
    overall_data = pd.read_csv(DATA_DIR / "step02_overall_theta.csv")
    what_data = pd.read_csv(DATA_DIR / "step03_what_theta.csv")
    
    # Merge for scatterplots
    merged = rpm_data.merge(overall_data, on='UID').merge(what_data, on='UID')
    
    # Load analysis results
    corr_results = pd.read_csv(DATA_DIR / "step04_correlation_results.csv")
    steiger_results = pd.read_csv(DATA_DIR / "step05_steiger_test.csv")
    
    return merged, corr_results, steiger_results

def create_correlation_scatterplots(merged_data, corr_results):
    """Create side-by-side scatterplots showing RPM correlations."""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1: RPM vs Overall Theta (Complex Integration)
    r1 = corr_results[corr_results['correlation_type'] == 'RPM_vs_Overall_theta']['r'].iloc[0]
    ax1.scatter(merged_data['rpm_score'], merged_data['theta_overall'], alpha=0.7, s=50)
    ax1.set_xlabel('RPM Score (Fluid Intelligence)')
    ax1.set_ylabel('Overall Theta (Complex Integration)')
    ax1.set_title(f'Complex Integration\nr = {r1:.3f}')
    ax1.grid(True, alpha=0.3)
    
    # Add regression line
    z = np.polyfit(merged_data['rpm_score'], merged_data['theta_overall'], 1)
    p = np.poly1d(z)
    ax1.plot(merged_data['rpm_score'], p(merged_data['rpm_score']), "r--", alpha=0.8)
    
    # Plot 2: RPM vs What Theta (Simple Single-Domain)
    r2 = corr_results[corr_results['correlation_type'] == 'RPM_vs_What_theta']['r'].iloc[0]
    ax2.scatter(merged_data['rpm_score'], merged_data['theta_what'], alpha=0.7, s=50)
    ax2.set_xlabel('RPM Score (Fluid Intelligence)')
    ax2.set_ylabel('What Theta (Simple Single-Domain)')
    ax2.set_title(f'Simple Single-Domain\nr = {r2:.3f}')
    ax2.grid(True, alpha=0.3)
    
    # Add regression line
    z = np.polyfit(merged_data['rpm_score'], merged_data['theta_what'], 1)
    p = np.poly1d(z)
    ax2.plot(merged_data['rpm_score'], p(merged_data['rpm_score']), "r--", alpha=0.8)
    
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'correlation_scatterplots.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Created correlation_scatterplots.png")

def create_comparison_barplot(corr_results, steiger_results):
    """Create bar plot comparing correlation strengths with significance test."""
    
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    
    # Extract correlations and CIs
    correlations = corr_results['r'].values
    ci_lower = corr_results['ci_lower'].values
    ci_upper = corr_results['ci_upper'].values
    labels = ['Complex\nIntegration', 'Simple\nSingle-Domain']
    
    # Create bars
    x_pos = [0, 1]
    bars = ax.bar(x_pos, correlations, 
                  yerr=[correlations - ci_lower, ci_upper - correlations],
                  capsize=5, alpha=0.7, color=['#1f77b4', '#ff7f0e'])
    
    # Add value labels on bars
    for i, (bar, r) in enumerate(zip(bars, correlations)):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                f'r = {r:.3f}', ha='center', va='bottom', fontweight='bold')
    
    ax.set_ylabel('Correlation with RPM')
    ax.set_title('RPM Correlation Comparison\n(Fluid Intelligence Prediction)')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, max(ci_upper) + 0.1)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add Steiger test results
    z_stat = steiger_results['z_statistic'].iloc[0]
    p_val = steiger_results['p_uncorrected'].iloc[0]
    ax.text(0.5, max(ci_upper) + 0.05, 
            f'Differential Prediction Test:\nSteiger Z = {z_stat:.3f}, p = {p_val:.3f}',
            ha='center', va='center', fontsize=10, 
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'correlation_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Created correlation_comparison.png")

def create_domain_correlation_plot(merged_data):
    """Show the extremely high correlation between Overall and What domains."""
    
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    
    # Scatterplot
    ax.scatter(merged_data['theta_overall'], merged_data['theta_what'], alpha=0.7, s=50)
    
    # Calculate correlation
    r_domains = np.corrcoef(merged_data['theta_overall'], merged_data['theta_what'])[0, 1]
    
    # Add regression line
    z = np.polyfit(merged_data['theta_overall'], merged_data['theta_what'], 1)
    p = np.poly1d(z)
    ax.plot(merged_data['theta_overall'], p(merged_data['theta_overall']), "r--", alpha=0.8)
    
    ax.set_xlabel('Overall Theta (Complex Integration)')
    ax.set_ylabel('What Theta (Simple Single-Domain)')
    ax.set_title(f'Domain Correlation\nr = {r_domains:.3f}\n(Explains why no differential prediction)')
    ax.grid(True, alpha=0.3)
    
    # Add diagonal reference line
    lims = [max(ax.get_xlim()[0], ax.get_ylim()[0]),
            min(ax.get_xlim()[1], ax.get_ylim()[1])]
    ax.plot(lims, lims, 'k-', alpha=0.3, zorder=0)
    ax.set_aspect('equal')
    
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'domain_correlation.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Created domain_correlation.png")

if __name__ == "__main__":
    print("Generating plots for RQ 7.4.3...")
    
    # Load data
    merged_data, corr_results, steiger_results = load_data()
    
    # Create plots
    create_correlation_scatterplots(merged_data, corr_results)
    create_comparison_barplot(corr_results, steiger_results)
    create_domain_correlation_plot(merged_data)
    
    print("All plots generated successfully!")