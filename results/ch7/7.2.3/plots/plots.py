#!/usr/bin/env python3
"""
Generate plots for RQ 7.2.3 - Age x Cognitive Test Interactions
Purpose: Visualize null interaction findings

Scientific Context:
- All interactions non-significant
- Showing parallel slopes across ages supports VR Scaffolding Hypothesis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(PROJECT_ROOT))

# Define paths
RQ_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = RQ_DIR / "data"
PLOTS_DIR = RQ_DIR / "plots"
PLOTS_DIR.mkdir(exist_ok=True, parents=True)

# Set plot style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def plot_interaction_effects():
    """Plot interaction coefficients with CIs."""
    
    # Load data
    coef_df = pd.read_csv(DATA_DIR / "step03_interaction_coefficients.csv")
    ci_df = pd.read_csv(DATA_DIR / "step06_bootstrap_CIs.csv")
    
    # Merge for plotting
    plot_df = pd.merge(coef_df[['test_name', 'interaction_coef', 'interaction_p_bonf']], 
                       ci_df[['test_name', 'CI_2.5', 'CI_97.5']], 
                       on='test_name')
    
    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    # Plot coefficients with error bars
    x_pos = np.arange(len(plot_df))
    ax.errorbar(x_pos, plot_df['interaction_coef'], 
                yerr=[plot_df['interaction_coef'] - plot_df['CI_2.5'],
                      plot_df['CI_97.5'] - plot_df['interaction_coef']],
                fmt='o', markersize=10, capsize=5, capthick=2, linewidth=2)
    
    # Add horizontal line at zero
    ax.axhline(y=0, color='red', linestyle='--', alpha=0.5, label='No interaction')
    
    # Labels
    ax.set_xticks(x_pos)
    ax.set_xticklabels(plot_df['test_name'])
    ax.set_xlabel('Cognitive Test', fontsize=12)
    ax.set_ylabel('Age x Test Interaction Coefficient', fontsize=12)
    ax.set_title('Age x Cognitive Test Interactions on REMEMVR Performance\n(All Non-Significant)', 
                 fontsize=14, fontweight='bold')
    
    # Add p-values as text
    for i, row in plot_df.iterrows():
        p_text = f"p = {row['interaction_p_bonf']:.3f}" if row['interaction_p_bonf'] < 1 else "p > 0.99"
        ax.text(i, row['CI_97.5'] + 0.0001, p_text, ha='center', va='bottom', fontsize=9)
    
    ax.legend()
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "interaction_coefficients.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created: interaction_coefficients.png")

def plot_test_slopes_by_age():
    """Plot test slopes at different ages showing parallel relationships."""
    
    # Load slope comparison data
    slope_df = pd.read_csv(DATA_DIR / "step04_slope_comparison.csv")
    
    # Create figure with subplots for each test
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    
    tests = ['RAVLT', 'BVMT', 'NART', 'RPM']
    colors = ['blue', 'green', 'orange', 'red']
    
    for i, (test, color) in enumerate(zip(tests, colors)):
        ax = axes[i]
        test_data = slope_df[slope_df['test_name'] == test]
        
        # Create bar plot
        x_pos = np.arange(len(test_data))
        ax.bar(x_pos, test_data['test_slope'], color=color, alpha=0.7)
        
        # Labels
        ax.set_xticks(x_pos)
        ax.set_xticklabels(test_data['age_group'], rotation=0)
        ax.set_ylabel('Test Slope', fontsize=10)
        ax.set_title(f'{test} Slope Across Ages', fontsize=12, fontweight='bold')
        
        # Add horizontal line at mean slope
        mean_slope = test_data['test_slope'].mean()
        ax.axhline(y=mean_slope, color='black', linestyle='--', alpha=0.5)
        
        # Add text showing slope range
        slope_range = test_data['test_slope'].max() - test_data['test_slope'].min()
        ax.text(0.5, 0.95, f'Range: {slope_range:.4f}', 
                transform=ax.transAxes, ha='center', va='top', fontsize=9)
    
    plt.suptitle('Test Slopes at Different Ages (Showing Age-Invariance)', 
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "test_slopes_by_age.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created: test_slopes_by_age.png")

def plot_effect_sizes():
    """Plot Cohen's f² effect sizes for interactions."""
    
    # Load effect size data
    effect_df = pd.read_csv(DATA_DIR / "step05_effect_sizes.csv")
    
    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    # Plot effect sizes
    x_pos = np.arange(len(effect_df))
    bars = ax.bar(x_pos, effect_df['cohens_f2'], color='skyblue', edgecolor='navy', linewidth=2)
    
    # Color bars by interpretation
    colors = {'negligible': 'lightgray', 'small': 'lightblue', 'medium': 'orange', 'large': 'red'}
    for bar, interp in zip(bars, effect_df['interpretation']):
        bar.set_color(colors[interp])
    
    # Add reference lines for effect size thresholds
    ax.axhline(y=0.02, color='green', linestyle='--', alpha=0.5, label='Small (f²=0.02)')
    ax.axhline(y=0.15, color='orange', linestyle='--', alpha=0.5, label='Medium (f²=0.15)')
    
    # Labels
    ax.set_xticks(x_pos)
    ax.set_xticklabels(effect_df['test_name'])
    ax.set_xlabel('Cognitive Test', fontsize=12)
    ax.set_ylabel("Cohen's f² for Interaction", fontsize=12)
    ax.set_title("Effect Sizes for Age x Test Interactions\n(All Negligible to Small)", 
                 fontsize=14, fontweight='bold')
    
    # Add values on bars
    for i, (f2, interp) in enumerate(zip(effect_df['cohens_f2'], effect_df['interpretation'])):
        ax.text(i, f2 + 0.001, f'{f2:.4f}\n({interp})', ha='center', va='bottom', fontsize=9)
    
    ax.legend(loc='upper right')
    ax.set_ylim(0, max(0.03, effect_df['cohens_f2'].max() * 1.2))
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "effect_sizes.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created: effect_sizes.png")

def plot_model_diagnostics():
    """Plot diagnostic results for all models."""
    
    # Load diagnostics data
    diag_df = pd.read_csv(DATA_DIR / "step05_diagnostics.csv")
    
    # Create figure with diagnostic plots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Plot 1: Normality p-values
    ax = axes[0, 0]
    x_pos = np.arange(len(diag_df))
    bars1 = ax.bar(x_pos, diag_df['shapiro_p'], color='green', alpha=0.7)
    ax.axhline(y=0.05, color='red', linestyle='--', label='α=0.05')
    ax.set_xticks(x_pos)
    ax.set_xticklabels([m.replace('Age x ', '') for m in diag_df['model']])
    ax.set_ylabel('Shapiro-Wilk p-value')
    ax.set_title('Normality Test Results')
    ax.legend()
    
    # Plot 2: Homoscedasticity p-values
    ax = axes[0, 1]
    bars2 = ax.bar(x_pos, diag_df['breusch_pagan_p'], color='blue', alpha=0.7)
    ax.axhline(y=0.05, color='red', linestyle='--', label='α=0.05')
    ax.set_xticks(x_pos)
    ax.set_xticklabels([m.replace('Age x ', '') for m in diag_df['model']])
    ax.set_ylabel('Breusch-Pagan p-value')
    ax.set_title('Homoscedasticity Test Results')
    ax.legend()
    
    # Plot 3: Cook's D max values
    ax = axes[1, 0]
    bars3 = ax.bar(x_pos, diag_df['max_cooks_d'], color='orange', alpha=0.7)
    ax.axhline(y=4/100, color='red', linestyle='--', label='4/n threshold')
    ax.set_xticks(x_pos)
    ax.set_xticklabels([m.replace('Age x ', '') for m in diag_df['model']])
    ax.set_ylabel("Max Cook's D")
    ax.set_title("Influential Observations")
    ax.legend()
    
    # Plot 4: Number of outliers
    ax = axes[1, 1]
    bars4 = ax.bar(x_pos, diag_df['n_outliers'], color='red', alpha=0.7)
    ax.axhline(y=5, color='red', linestyle='--', label='Acceptable threshold')
    ax.set_xticks(x_pos)
    ax.set_xticklabels([m.replace('Age x ', '') for m in diag_df['model']])
    ax.set_ylabel('Number of Outliers')
    ax.set_title('Outlier Detection')
    ax.legend()
    
    plt.suptitle('Model Diagnostics for Age x Test Interactions', 
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "model_diagnostics.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created: model_diagnostics.png")

def main():
    """Generate all plots."""
    
    print("=" * 60)
    print("GENERATING PLOTS FOR RQ 7.2.3")
    print("=" * 60)
    
    plot_interaction_effects()
    plot_test_slopes_by_age()
    plot_effect_sizes()
    plot_model_diagnostics()
    
    print(f"\nAll plots saved to: {PLOTS_DIR}")
    print("Ready for rq_plots agent")

if __name__ == "__main__":
    main()