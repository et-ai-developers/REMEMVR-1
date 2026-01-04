#!/usr/bin/env python3
"""
Generate plots for RQ 7.1.3: Domain-Specific Prediction Patterns
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Paths
RQ_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = RQ_DIR / "data"
PLOTS_DIR = RQ_DIR / "plots"

# =============================================================================
# Plot 1: Beta Coefficient Heatmap
# =============================================================================

def plot_beta_heatmap():
    """Create heatmap of beta coefficients across domains and predictors."""
    
    # Load data
    heatmap_data = pd.read_csv(DATA_DIR / "step03_heatmap_plot_data.csv")
    
    # Pivot for heatmap
    pivot_data = heatmap_data.pivot(index='domain', columns='predictor', values='beta')
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create heatmap
    sns.heatmap(pivot_data, annot=True, fmt='.3f', cmap='RdBu_r', center=0,
                cbar_kws={'label': 'Standardized Beta Coefficient'},
                linewidths=0.5, linecolor='gray', ax=ax)
    
    # Add significance markers
    for i, domain in enumerate(['What', 'Where', 'When']):
        for j, predictor in enumerate(['BVMT_T', 'RAVLT_T', 'RPM_T']):
            row = heatmap_data[(heatmap_data['domain'] == domain) & 
                              (heatmap_data['predictor'] == predictor)]
            if not row.empty:
                sig = row['significance'].values[0]
                if sig != 'ns':
                    ax.text(j + 0.5, i + 0.7, sig, ha='center', va='center',
                           fontsize=12, color='black', weight='bold')
    
    plt.title('Domain-Specific Prediction Patterns\nStandardized Beta Coefficients', 
             fontsize=14, weight='bold')
    plt.xlabel('Cognitive Test Predictor', fontsize=12)
    plt.ylabel('Memory Domain', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "domain_beta_heatmap.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✓ Beta coefficient heatmap saved")

# =============================================================================
# Plot 2: R² Comparison Bar Plot
# =============================================================================

def plot_r_squared_comparison():
    """Create bar plot comparing R² values across domains with CIs."""
    
    # Load data
    comparison = pd.read_csv(DATA_DIR / "step05_model_comparison.csv")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Prepare data
    domains = comparison['domain'].values
    r_squared = comparison['r_squared'].values
    ci_lower = comparison['r2_ci_lower'].values
    ci_upper = comparison['r2_ci_upper'].values
    
    # Calculate error bars
    yerr_lower = r_squared - ci_lower
    yerr_upper = ci_upper - r_squared
    yerr = [yerr_lower, yerr_upper]
    
    # Colors based on effect size
    colors = ['#2E7D32' if r > 0.09 else '#FFA726' if r > 0.01 else '#EF5350' 
              for r in r_squared]
    
    # Create bar plot
    bars = ax.bar(domains, r_squared, yerr=yerr, capsize=5, 
                   color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, r_squared)):
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.01,
                f'{val:.3f}', ha='center', va='bottom', fontsize=11, weight='bold')
    
    # Add reference lines
    ax.axhline(y=0.09, color='gray', linestyle='--', alpha=0.5, 
               label='Medium effect (R²=0.09)')
    ax.axhline(y=0.25, color='gray', linestyle='--', alpha=0.5, 
               label='Large effect (R²=0.25)')
    
    # Labels and title
    ax.set_xlabel('Memory Domain', fontsize=12)
    ax.set_ylabel('R² (Variance Explained)', fontsize=12)
    ax.set_title('Model Performance Across Memory Domains\nwith 95% Bootstrap Confidence Intervals', 
                 fontsize=14, weight='bold')
    ax.set_ylim(0, max(ci_upper) * 1.1)
    
    # Legend
    ax.legend(loc='upper right', framealpha=0.9)
    
    # Grid
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "r_squared_comparison.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✓ R² comparison plot saved")

# =============================================================================
# Plot 3: Predictor Contributions Stacked Bar
# =============================================================================

def plot_predictor_contributions():
    """Create stacked bar plot showing semi-partial R² contributions."""
    
    # Load data
    contributions = pd.read_csv(DATA_DIR / "step05_predictor_contributions.csv")
    
    # Pivot for stacking
    pivot_contrib = contributions.pivot(index='domain', columns='predictor', values='semi_partial_r2')
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create stacked bar
    domains = pivot_contrib.index
    bottom = np.zeros(len(domains))
    
    colors = {'RAVLT_T': '#FF6B6B', 'BVMT_T': '#4ECDC4', 'RPM_T': '#45B7D1'}
    
    for predictor in ['RAVLT_T', 'BVMT_T', 'RPM_T']:
        values = pivot_contrib[predictor].values
        bars = ax.bar(domains, values, bottom=bottom, label=predictor.replace('_T', ''),
                      color=colors[predictor], alpha=0.8, edgecolor='white', linewidth=1)
        
        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, values)):
            if val > 0.005:  # Only show if contribution is meaningful
                ax.text(bar.get_x() + bar.get_width()/2, 
                       bottom[i] + val/2,
                       f'{val:.3f}', ha='center', va='center', 
                       fontsize=9, color='white', weight='bold')
        
        bottom += values
    
    # Labels and title
    ax.set_xlabel('Memory Domain', fontsize=12)
    ax.set_ylabel('Semi-Partial R² (Unique Variance Explained)', fontsize=12)
    ax.set_title('Unique Predictor Contributions by Domain\n(Semi-Partial R² Values)', 
                 fontsize=14, weight='bold')
    
    # Legend
    ax.legend(title='Cognitive Test', loc='upper right', framealpha=0.9)
    
    # Grid
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "predictor_contributions.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✓ Predictor contributions plot saved")

# =============================================================================
# Main execution
# =============================================================================

if __name__ == "__main__":
    print("\nGenerating plots for RQ 7.1.3...")
    
    # Create plots directory if needed
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate plots
    plot_beta_heatmap()
    plot_r_squared_comparison()
    plot_predictor_contributions()
    
    print("\n✓ All plots generated successfully!")
    print(f"  Location: {PLOTS_DIR}/")
    print("  Files:")
    print("  - domain_beta_heatmap.png")
    print("  - r_squared_comparison.png")
    print("  - predictor_contributions.png")