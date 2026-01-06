#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plotting script for RQ 7.5.2 - DASS predict memory performance

Simple diagnostic plots for hierarchical regression analysis.
"""

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns

# Set up paths
RQ_DIR = Path(__file__).resolve().parent.parent
data_dir = RQ_DIR / "data"
plots_dir = RQ_DIR / "plots"

def main():
    """Generate simple diagnostic plots for DASS regression analysis."""
    
    print("[PLOTS] Starting plot generation for RQ 7.5.2...")
    
    # Check required data files exist
    required_files = [
        "step01_analysis_dataset.csv",
        "step03_hierarchical_models.csv", 
        "step04_individual_predictors.csv",
        "step05_residual_analysis.csv"
    ]
    
    for file in required_files:
        if not (data_dir / file).exists():
            print(f"[ERROR] Missing required file: {file}")
            return 1
    
    # Plot 1: Hierarchical model comparison
    try:
        models_df = pd.read_csv(data_dir / "step03_hierarchical_models.csv")
        
        plt.figure(figsize=(8, 6))
        plt.bar(models_df['model'], models_df['R2'])
        plt.ylabel('R-squared')
        plt.title('Hierarchical Model Comparison')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(plots_dir / "model_comparison.png", dpi=300, bbox_inches='tight')
        plt.close()
        print("[SAVED] model_comparison.png")
        
    except Exception as e:
        print(f"[ERROR] Failed to create model comparison: {e}")
    
    # Plot 2: Individual predictor effects  
    try:
        predictors_df = pd.read_csv(data_dir / "step04_individual_predictors.csv")
        
        plt.figure(figsize=(10, 6))
        x_pos = range(len(predictors_df))
        plt.bar(x_pos, predictors_df['beta'])
        plt.errorbar(x_pos, predictors_df['beta'], 
                    yerr=[predictors_df['beta'] - predictors_df['ci_lower'],
                          predictors_df['ci_upper'] - predictors_df['beta']],
                    fmt='none', color='black', capsize=5)
        plt.ylabel('Standardized Beta')
        plt.title('DASS Predictor Effects')
        plt.xticks(x_pos, predictors_df['predictor'], rotation=45)
        plt.axhline(y=0, color='red', linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.savefig(plots_dir / "predictor_effects.png", dpi=300, bbox_inches='tight')
        plt.close()
        print("[SAVED] predictor_effects.png")
        
    except Exception as e:
        print(f"[ERROR] Failed to create predictor effects: {e}")
    
    # Plot 3: Regression diagnostics (residuals vs fitted)
    try:
        residuals_df = pd.read_csv(data_dir / "step05_residual_analysis.csv")
        
        plt.figure(figsize=(12, 8))
        
        # Subplot 1: Residuals vs Fitted
        plt.subplot(2, 2, 1)
        plt.scatter(residuals_df['fitted'], residuals_df['residual'], alpha=0.6)
        plt.xlabel('Fitted Values')
        plt.ylabel('Residuals')
        plt.title('Residuals vs Fitted')
        plt.axhline(y=0, color='red', linestyle='--')
        
        # Subplot 2: Q-Q Plot (approximate)
        plt.subplot(2, 2, 2)
        from scipy import stats
        stats.probplot(residuals_df['residual'], dist="norm", plot=plt)
        plt.title('Normal Q-Q Plot')
        
        # Subplot 3: Scale-Location
        plt.subplot(2, 2, 3)
        sqrt_abs_resid = np.sqrt(np.abs(residuals_df['standardized_residual']))
        plt.scatter(residuals_df['fitted'], sqrt_abs_resid, alpha=0.6)
        plt.xlabel('Fitted Values')
        plt.ylabel('√|Standardized Residuals|')
        plt.title('Scale-Location')
        
        # Subplot 4: Cook's Distance
        plt.subplot(2, 2, 4)
        plt.bar(range(len(residuals_df)), residuals_df['cooks_d'])
        plt.xlabel('Observation')
        plt.ylabel("Cook's Distance")
        plt.title("Cook's Distance")
        plt.axhline(y=0.04, color='red', linestyle='--', label='Threshold')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(plots_dir / "regression_diagnostics.png", dpi=300, bbox_inches='tight')
        plt.close()
        print("[SAVED] regression_diagnostics.png")
        
    except Exception as e:
        print(f"[ERROR] Failed to create diagnostics: {e}")
        
    # Plot 4: Memory performance distribution
    try:
        data_df = pd.read_csv(data_dir / "step01_analysis_dataset.csv")
        
        plt.figure(figsize=(10, 6))
        
        # Create depression groups (median split)
        dep_median = data_df['dass_dep'].median()
        data_df['dep_group'] = data_df['dass_dep'].apply(lambda x: 'High Depression' if x > dep_median else 'Low Depression')
        
        # Plot distributions
        for group in ['Low Depression', 'High Depression']:
            group_data = data_df[data_df['dep_group'] == group]['theta_all']
            plt.hist(group_data, alpha=0.6, label=group, bins=15)
        
        plt.xlabel('Memory Performance (theta_all)')
        plt.ylabel('Frequency')
        plt.title('Memory Distribution by Depression Level')
        plt.legend()
        plt.tight_layout()
        plt.savefig(plots_dir / "memory_distribution.png", dpi=300, bbox_inches='tight')
        plt.close()
        print("[SAVED] memory_distribution.png")
        
    except Exception as e:
        print(f"[ERROR] Failed to create distribution plot: {e}")
    
    print("[PLOTS] Plot generation complete!")
    return 0

if __name__ == "__main__":
    sys.exit(main())