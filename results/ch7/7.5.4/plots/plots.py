#!/usr/bin/env python3
"""
RQ 7.5.4 Visualization Generation
Within-person sleep effects on VR memory analysis plots
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Simple plotting without custom functions

# Set plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Define paths
RQ_ROOT = Path(__file__).parent.parent
DATA_DIR = RQ_ROOT / "data"
PLOTS_DIR = RQ_ROOT / "plots"

print("RQ 7.5.4: Within-Person Sleep Effects - Plot Generation")
print("=" * 60)

# Create simple effect sizes plot
try:
    # Read power/effect data
    power_data = pd.read_csv(DATA_DIR / "step08_power_effect_sizes.csv")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create bar plot of effect sizes
    bars = ax.bar(range(len(power_data)), power_data['cohens_d'], 
                  color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    
    ax.set_xlabel('Sleep Parameters')
    ax.set_ylabel("Cohen's d")
    ax.set_title('RQ 7.5.4: Effect Sizes for Sleep Parameters')
    ax.set_xticks(range(len(power_data)))
    ax.set_xticklabels(power_data['parameter'], rotation=45, ha='right')
    
    # Add effect size values on bars
    for i, (bar, value) in enumerate(zip(bars, power_data['cohens_d'])):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{value:.3f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "effect_sizes.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Generated: effect_sizes.png")
    
except Exception as e:
    print(f"Warning: Could not generate effect sizes plot: {e}")

# Create sleep variability plot
try:
    # Read analysis dataset
    analysis_data = pd.read_csv(DATA_DIR / "step04_analysis_dataset.csv")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Within-person sleep hours variability
    sleep_vars = analysis_data.groupby('UID')['Sleep_Hours_WP'].std()
    ax1.hist(sleep_vars.dropna(), bins=20, alpha=0.7, color='skyblue')
    ax1.set_xlabel('Within-Person Sleep Hours SD')
    ax1.set_ylabel('Number of Participants')
    ax1.set_title('(A) Sleep Hours Variability')
    
    # Within-person sleep quality variability  
    quality_vars = analysis_data.groupby('UID')['Sleep_Quality_WP'].std()
    ax2.hist(quality_vars.dropna(), bins=20, alpha=0.7, color='lightcoral')
    ax2.set_xlabel('Within-Person Sleep Quality SD')
    ax2.set_ylabel('Number of Participants')
    ax2.set_title('(B) Sleep Quality Variability')
    
    fig.suptitle('RQ 7.5.4: Within-Person Sleep Variability')
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "sleep_variability.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Generated: sleep_variability.png")
    
except Exception as e:
    print(f"Warning: Could not generate sleep variability plot: {e}")

# Create cross-validation results plot
try:
    cv_data = pd.read_csv(DATA_DIR / "step07_cross_validation.csv")
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Plot CV performance by fold
    if 'fold' in cv_data.columns and any(r2_col in cv_data.columns for r2_col in ['r2_marginal', 'R2']):
        r2_col = 'r2_marginal' if 'r2_marginal' in cv_data.columns else 'R2'
        ax.bar(cv_data['fold'], cv_data[r2_col], alpha=0.7, color='steelblue')
        ax.set_xlabel('CV Fold')
        ax.set_ylabel('R-squared')
        ax.set_title('RQ 7.5.4: Cross-Validation Performance')
        ax.axhline(y=0, color='red', linestyle='--', alpha=0.5)
        
        # Add mean line
        mean_r2 = cv_data[r2_col].mean()
        ax.axhline(y=mean_r2, color='orange', linestyle='-', 
                   label=f'Mean R² = {mean_r2:.3f}')
        ax.legend()
    else:
        ax.text(0.5, 0.5, 'CV Data Format Not Compatible', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title('RQ 7.5.4: Cross-Validation Performance')
    
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "cross_validation.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Generated: cross_validation.png")
    
except Exception as e:
    print(f"Warning: Could not generate CV plot: {e}")

print("\nPlot generation complete!")
print(f"Output directory: {PLOTS_DIR}")