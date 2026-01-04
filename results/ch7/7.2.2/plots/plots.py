#!/usr/bin/env python3
"""
Generate Plots for RQ 7.2.2 Attenuation Analysis
================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Set up paths  
RQ_DIR = Path(__file__).resolve().parents[1]
PLOTS_DIR = RQ_DIR / "plots"
DATA_DIR = RQ_DIR / "data"

def plot_attenuation_bar():
    """Create bar plot of attenuation with confidence intervals"""
    
    # Load data
    ci_df = pd.read_csv(DATA_DIR / "step03_confidence_intervals.csv")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Prepare data for plotting
    domains = ['Overall REMEMVR', 'What Domain']
    point_estimates = [ci_df.loc[0, 'point_estimate'], ci_df.loc[1, 'point_estimate']]
    ci_lower = [ci_df.loc[0, 'ci_lower'], ci_df.loc[1, 'ci_lower']]
    ci_upper = [ci_df.loc[0, 'ci_upper'], ci_df.loc[1, 'ci_upper']]
    
    # Calculate error bars
    yerr_lower = [pe - cl for pe, cl in zip(point_estimates, ci_lower)]
    yerr_upper = [cu - pe for pe, cu in zip(point_estimates, ci_upper)]
    
    # Create bar plot
    x_pos = np.arange(len(domains))
    bars = ax.bar(x_pos, point_estimates, yerr=[yerr_lower, yerr_upper],
                   capsize=5, alpha=0.8, edgecolor='black', linewidth=2)
    
    # Color bars based on classification
    colors = ['darkred' if pe > 100 else 'darkgreen' if pe > 70 else 'orange' 
              for pe in point_estimates]
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    
    # Add horizontal lines
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax.axhline(y=70, color='green', linestyle='--', alpha=0.5, 
               label='Substantial attenuation (>70%)')
    ax.axhline(y=100, color='red', linestyle='--', alpha=0.5,
               label='Suppression effect (>100%)')
    
    # Customize plot
    ax.set_xticks(x_pos)
    ax.set_xticklabels(domains, fontsize=12)
    ax.set_ylabel('Attenuation (%)', fontsize=12)
    ax.set_title('Age Effect Attenuation by Cognitive Tests\n(Suppression Effect Detected)', 
                 fontsize=14, fontweight='bold')
    
    # Add value labels
    for i, (pe, cl, cu) in enumerate(zip(point_estimates, ci_lower, ci_upper)):
        ax.text(i, pe + (cu - pe) * 0.1, f'{pe:.1f}%', 
                ha='center', fontsize=11, fontweight='bold')
        ax.text(i, -20, f'[{cl:.0f}%, {cu:.0f}%]',
                ha='center', fontsize=9, style='italic')
    
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'attenuation_bar_plot.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created: attenuation_bar_plot.png")

def plot_bootstrap_distribution():
    """Create histogram of bootstrap distribution"""
    
    # Load bootstrap distributions
    boot_df = pd.read_csv(DATA_DIR / "step03_bootstrap_distributions.csv")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Overall REMEMVR distribution
    ax1.hist(boot_df['overall_attenuation'], bins=50, alpha=0.7, 
             color='darkblue', edgecolor='black')
    ax1.axvline(x=119.8, color='red', linestyle='--', linewidth=2,
                label='Observed (119.8%)')
    ax1.axvline(x=100, color='orange', linestyle='--', alpha=0.7,
                label='Suppression threshold')
    ax1.axvline(x=0, color='black', linestyle='-', alpha=0.5)
    
    # Add CI bounds
    ci_lower = np.percentile(boot_df['overall_attenuation'], 2.5)
    ci_upper = np.percentile(boot_df['overall_attenuation'], 97.5)
    ax1.axvline(x=ci_lower, color='green', linestyle=':', alpha=0.7)
    ax1.axvline(x=ci_upper, color='green', linestyle=':', alpha=0.7)
    
    ax1.set_xlabel('Attenuation (%)', fontsize=11)
    ax1.set_ylabel('Frequency', fontsize=11)
    ax1.set_title('Overall REMEMVR\nBootstrap Distribution', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # What domain distribution
    ax2.hist(boot_df['what_attenuation'], bins=50, alpha=0.7,
             color='darkgreen', edgecolor='black')
    ax2.axvline(x=119.8, color='red', linestyle='--', linewidth=2,
                label='Observed (119.8%)')
    ax2.axvline(x=100, color='orange', linestyle='--', alpha=0.7,
                label='Suppression threshold')
    ax2.axvline(x=0, color='black', linestyle='-', alpha=0.5)
    
    # Add CI bounds
    ci_lower_what = np.percentile(boot_df['what_attenuation'], 2.5)
    ci_upper_what = np.percentile(boot_df['what_attenuation'], 97.5)
    ax2.axvline(x=ci_lower_what, color='green', linestyle=':', alpha=0.7)
    ax2.axvline(x=ci_upper_what, color='green', linestyle=':', alpha=0.7)
    
    ax2.set_xlabel('Attenuation (%)', fontsize=11)
    ax2.set_ylabel('Frequency', fontsize=11)
    ax2.set_title('What Domain\nBootstrap Distribution', fontsize=12)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.suptitle('Bootstrap Distributions of Attenuation Ratios (1000 iterations)',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'bootstrap_distributions.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created: bootstrap_distributions.png")

def plot_coefficient_comparison():
    """Create comparison of bivariate vs controlled coefficients"""
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Data
    conditions = ['Bivariate\n(Age only)', 'Controlled\n(Age + Cognitive)']
    coefficients = [-0.1302, 0.0258]
    colors = ['coral', 'lightgreen']
    
    # Create bar plot
    bars = ax.bar(conditions, coefficients, color=colors, alpha=0.8,
                   edgecolor='black', linewidth=2)
    
    # Add zero line
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
    
    # Add arrow showing change
    ax.annotate('', xy=(1, coefficients[1]), xytext=(0, coefficients[0]),
                arrowprops=dict(arrowstyle='->', lw=2, color='red'))
    ax.text(0.5, -0.05, 'SIGN REVERSAL\n(Suppression)', 
            ha='center', fontsize=11, color='red', fontweight='bold')
    
    # Labels
    ax.set_ylabel('Age Coefficient (β)', fontsize=12)
    ax.set_title('Age Coefficient Changes After Controlling for Cognitive Tests',
                 fontsize=14, fontweight='bold')
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, coefficients)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01 if height > 0 else height - 0.01,
                f'{val:.4f}', ha='center', va='bottom' if height > 0 else 'top',
                fontsize=11, fontweight='bold')
    
    # Add interpretation text
    ax.text(0.5, -0.18, 'Interpretation: After accounting for cognitive abilities,\n'
                        'older adults show BETTER VR memory performance,\n'
                        'suggesting they benefit more from VR scaffolding',
            ha='center', fontsize=10, transform=ax.transData,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    ax.set_ylim(-0.2, 0.1)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'coefficient_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created: coefficient_comparison.png")

def main():
    """Generate all plots"""
    PLOTS_DIR.mkdir(exist_ok=True)
    
    print("Generating plots for RQ 7.2.2...")
    
    plot_attenuation_bar()
    plot_bootstrap_distribution()
    plot_coefficient_comparison()
    
    print("\nAll plots generated successfully!")

if __name__ == "__main__":
    main()