#!/usr/bin/env python3
"""
Generate plots for RQ 7.3.2: Calibration Quality Prediction
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Setup paths
PLOTS_DIR = Path(__file__).parent
RQ_DIR = PLOTS_DIR.parent
DATA_DIR = RQ_DIR / "data"

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def create_plots():
    """Create all visualization plots"""
    
    # Load data
    reg_df = pd.read_csv(DATA_DIR / "step04_regression_results.csv")
    model_df = pd.read_csv(DATA_DIR / "step04_model_comparison.csv")
    cv_df = pd.read_csv(DATA_DIR / "step06_cross_validation.csv")
    effect_df = pd.read_csv(DATA_DIR / "step08_effect_sizes.csv")
    
    # 1. Hierarchical Regression Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Model comparison
    models = model_df['model'].values
    r2_values = model_df['r2'].values
    ax1.bar(models, r2_values)
    ax1.set_ylabel('R²')
    ax1.set_title('Hierarchical Regression: Model Comparison')
    ax1.set_ylim(0, max(0.1, max(r2_values) * 1.2))
    
    # Effect sizes
    cognitive_effects = effect_df[effect_df['predictor'].isin(['RAVLT_T', 'BVMT_T', 'RPM_T'])]
    ax2.barh(cognitive_effects['predictor'], cognitive_effects['sr_squared'])
    ax2.set_xlabel('Semi-partial R²')
    ax2.set_title('Cognitive Predictor Importance')
    
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'hierarchical_regression.png', dpi=300)
    plt.close()
    
    # 2. Cross-validation Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Train vs Test R²
    ax1.scatter(cv_df.index + 1, cv_df['train_r2'], label='Train', s=100)
    ax1.scatter(cv_df.index + 1, cv_df['test_r2'], label='Test', s=100)
    ax1.axhline(0, color='black', linestyle='--', alpha=0.3)
    ax1.set_xlabel('Fold')
    ax1.set_ylabel('R²')
    ax1.set_title('Cross-Validation: Train vs Test Performance')
    ax1.legend()
    
    # RMSE across folds
    ax2.plot(cv_df.index + 1, cv_df['rmse'], marker='o')
    ax2.set_xlabel('Fold')
    ax2.set_ylabel('RMSE')
    ax2.set_title('Cross-Validation: Prediction Error')
    
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'cross_validation.png', dpi=300)
    plt.close()
    
    # 3. Calibration vs Accuracy Comparison
    if (DATA_DIR / 'step10_accuracy_comparison.csv').exists():
        comp_df = pd.read_csv(DATA_DIR / 'step10_accuracy_comparison.csv')
        
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Bar plot comparison
        measures = comp_df['measure'].values
        r2_vals = comp_df['r2'].values
        colors = ['#FF6B6B', '#4ECDC4']
        
        bars = ax.bar(measures, r2_vals, color=colors)
        ax.set_ylabel('R²')
        ax.set_title('Cognitive Predictors: Calibration vs Accuracy')
        ax.set_ylim(0, max(0.3, np.nanmax(r2_vals) * 1.2))
        
        # Add value labels
        for bar, val in zip(bars, r2_vals):
            if not np.isnan(val):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                       f'{val:.3f}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(PLOTS_DIR / 'calibration_vs_accuracy.png', dpi=300)
        plt.close()
    
    print(f"Created plots in {PLOTS_DIR}")

if __name__ == "__main__":
    create_plots()