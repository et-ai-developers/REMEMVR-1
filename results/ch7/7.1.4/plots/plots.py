#!/usr/bin/env python3
"""
Generate plots for RQ 7.1.4: Incremental Validity Assessment
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300

# Paths
RQ_DIR = Path(__file__).resolve().parents[1]
PLOTS_DIR = RQ_DIR / "plots"

def create_variance_decomposition():
    """Create variance decomposition pie chart."""
    
    # Load hierarchical results
    hier_df = pd.read_csv(RQ_DIR / "data" / "step07_hierarchical_models.csv")
    
    # Get R² values
    r2_demo = hier_df.iloc[0]['R2']
    r2_cog = hier_df.iloc[1]['R2'] - r2_demo
    r2_self = hier_df.iloc[2]['R2'] - hier_df.iloc[1]['R2']
    residual = 1 - hier_df.iloc[2]['R2']
    
    # Create pie chart
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    
    sizes = [r2_demo*100, r2_cog*100, r2_self*100, residual*100]
    labels = [
        f'Demographics\n({r2_demo*100:.1f}%)',
        f'Cognitive Tests\n({r2_cog*100:.1f}%)',
        f'Self-Report\n({r2_self*100:.1f}%)',
        f'Unexplained\n({residual*100:.1f}%)'
    ]
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
    explode = (0.05, 0.05, 0.05, 0.1)  # Explode the residual slice
    
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, 
                                       autopct='%1.1f%%', startangle=90,
                                       explode=explode, shadow=True)
    
    # Improve text
    for text in texts:
        text.set_fontsize(11)
        text.set_fontweight('bold')
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')
    
    ax.set_title('REMEMVR Variance Decomposition\nHierarchical Regression Analysis', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Add text box with key finding
    textstr = f'Key Finding:\n{residual*100:.1f}% of REMEMVR variance\nremains unexplained by all\ntraditional predictors'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax.text(1.3, 0.5, textstr, transform=ax.transAxes, fontsize=12,
            verticalalignment='center', bbox=props)
    
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "variance_decomposition.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # Save plot data
    plot_data = pd.DataFrame({
        'Block': ['Demographics', 'Cognitive Tests', 'Self-Report', 'Unexplained'],
        'Variance_Explained': sizes,
        'R_squared': [r2_demo, r2_cog, r2_self, residual]
    })
    plot_data.to_csv(PLOTS_DIR / "variance_decomposition_data.csv", index=False)
    print("[PLOT] Created variance_decomposition.png")

def create_incremental_validity_plot():
    """Create incremental validity bar plot."""
    
    # Load effect sizes
    effect_df = pd.read_csv(RQ_DIR / "data" / "step08_incremental_validity.csv")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: R² accumulation
    models = ['Demographics', '+ Cognitive', '+ Self-Report']
    r2_values = effect_df['R2'][:3].values
    ci_lower = effect_df['R2_CI_lower'][:3].values
    ci_upper = effect_df['R2_CI_upper'][:3].values
    
    x = np.arange(len(models))
    bars = ax1.bar(x, r2_values, color=['#ff9999', '#66b3ff', '#99ff99'])
    
    # Add error bars
    errors = [r2_values - ci_lower, ci_upper - r2_values]
    ax1.errorbar(x, r2_values, yerr=errors, fmt='none', 
                 ecolor='black', capsize=5, capthick=2)
    
    # Add values on bars
    for i, (bar, val) in enumerate(zip(bars, r2_values)):
        ax1.text(bar.get_x() + bar.get_width()/2, val + 0.02,
                f'{val:.3f}', ha='center', va='bottom', fontweight='bold')
    
    ax1.set_ylim(0, 0.6)
    ax1.set_ylabel('R² (Cumulative)', fontsize=12)
    ax1.set_title('Cumulative Variance Explained', fontsize=13, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(models)
    ax1.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label='50% threshold')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Plot 2: Cohen's f² effect sizes
    blocks = ['Demographics', 'Cognitive', 'Self-Report']
    f2_values = effect_df['Cohens_f2'][:3].values
    
    colors_f2 = ['red' if f < 0.15 else 'yellow' if f < 0.35 else 'green' for f in f2_values]
    bars2 = ax2.bar(blocks, f2_values, color=colors_f2, alpha=0.7)
    
    # Add values on bars
    for bar, val in zip(bars2, f2_values):
        ax2.text(bar.get_x() + bar.get_width()/2, val + 0.01,
                f'{val:.3f}', ha='center', va='bottom', fontweight='bold')
    
    # Add reference lines
    ax2.axhline(y=0.02, color='gray', linestyle=':', alpha=0.5, label='Small (0.02)')
    ax2.axhline(y=0.15, color='gray', linestyle='--', alpha=0.5, label='Medium (0.15)')
    ax2.axhline(y=0.35, color='gray', linestyle='-', alpha=0.5, label='Large (0.35)')
    
    ax2.set_ylim(0, 0.4)
    ax2.set_ylabel("Cohen's f²", fontsize=12)
    ax2.set_title('Incremental Effect Sizes', fontsize=13, fontweight='bold')
    ax2.legend(loc='upper right')
    ax2.grid(axis='y', alpha=0.3)
    
    plt.suptitle('RQ 7.1.4: Incremental Validity Assessment', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "incremental_validity.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # Save plot data
    plot_data = pd.DataFrame({
        'Model': models,
        'R2': r2_values,
        'R2_CI_lower': ci_lower,
        'R2_CI_upper': ci_upper,
        'Cohens_f2': f2_values[:3]
    })
    plot_data.to_csv(PLOTS_DIR / "incremental_validity_data.csv", index=False)
    print("[PLOT] Created incremental_validity.png")

def create_predictor_importance_plot():
    """Create predictor importance plot."""
    
    # Load merged data to get correlations
    merged_df = pd.read_csv(RQ_DIR / "data" / "step05_merged_predictors.csv")
    
    # Calculate correlations with theta
    predictors = []
    correlations = []
    categories = []
    
    # Demographics
    for col in ['age_z', 'sex_binary', 'education_z']:
        if col in merged_df.columns:
            corr = merged_df[col].corr(merged_df['theta'])
            predictors.append(col.replace('_z', '').replace('_', ' ').title())
            correlations.append(corr)
            categories.append('Demographics')
    
    # Cognitive
    for col in ['RAVLT_T_z', 'RAVLT_DR_T_z', 'BVMT_T_z', 'NART_T_z', 'RPM_T_z']:
        if col in merged_df.columns:
            corr = merged_df[col].corr(merged_df['theta'])
            predictors.append(col.replace('_T_z', '').replace('_z', '').replace('_', ' '))
            correlations.append(corr)
            categories.append('Cognitive')
    
    # Self-report
    for col in ['DASS_Dep_z', 'DASS_Anx_z', 'DASS_Str_z', 'VR_Exp_z', 'Sleep_z']:
        if col in merged_df.columns:
            corr = merged_df[col].corr(merged_df['theta'])
            predictors.append(col.replace('_z', '').replace('_', ' '))
            correlations.append(corr)
            categories.append('Self-Report')
    
    # Create DataFrame
    importance_df = pd.DataFrame({
        'Predictor': predictors,
        'Correlation': correlations,
        'Category': categories
    })
    
    # Sort by absolute correlation
    importance_df['Abs_Corr'] = importance_df['Correlation'].abs()
    importance_df = importance_df.sort_values('Abs_Corr', ascending=True)
    
    # Create plot
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    
    # Color by category
    color_map = {'Demographics': '#ff9999', 'Cognitive': '#66b3ff', 'Self-Report': '#99ff99'}
    colors = [color_map[cat] for cat in importance_df['Category']]
    
    bars = ax.barh(importance_df['Predictor'], importance_df['Correlation'], color=colors)
    
    # Add values
    for bar, val in zip(bars, importance_df['Correlation']):
        x_pos = val + 0.01 if val > 0 else val - 0.01
        ax.text(x_pos, bar.get_y() + bar.get_height()/2,
               f'{val:.3f}', ha='left' if val > 0 else 'right', 
               va='center', fontsize=9)
    
    ax.axvline(x=0, color='black', linewidth=0.8)
    ax.set_xlabel('Correlation with REMEMVR Theta', fontsize=12)
    ax.set_title('Individual Predictor Importance\n(Zero-Order Correlations)', 
                fontsize=13, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    ax.set_xlim(-0.5, 0.5)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=color_map[cat], label=cat) 
                       for cat in ['Demographics', 'Cognitive', 'Self-Report']]
    ax.legend(handles=legend_elements, loc='lower right')
    
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "predictor_importance.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # Save plot data
    importance_df.to_csv(PLOTS_DIR / "predictor_importance_data.csv", index=False)
    print("[PLOT] Created predictor_importance.png")

def main():
    """Generate all plots."""
    print("[START] Generating plots for RQ 7.1.4...")
    
    create_variance_decomposition()
    create_incremental_validity_plot()
    create_predictor_importance_plot()
    
    print("[SUCCESS] All plots generated")
    
if __name__ == "__main__":
    main()