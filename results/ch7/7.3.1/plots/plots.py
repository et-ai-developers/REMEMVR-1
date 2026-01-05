#!/usr/bin/env python3
"""
Generate plots for RQ 7.3.1
Creates diagnostic and comparison visualizations
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Setup paths
RQ_DIR = Path(__file__).resolve().parents[1]

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300

# Load data
hier_df = pd.read_csv(RQ_DIR / "data" / "step05_hierarchical_models.csv")
pred_df = pd.read_csv(RQ_DIR / "data" / "step06_individual_predictors.csv")
cv_df = pd.read_csv(RQ_DIR / "data" / "step07_cross_validation.csv")
effect_df = pd.read_csv(RQ_DIR / "data" / "step08_effect_sizes.csv")
comparison_df = pd.read_csv(RQ_DIR / "data" / "step10_accuracy_comparison.csv")

# Figure 1: Hierarchical Regression Comparison
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# R² comparison
models = ['Demographics', 'Cognitive']
r2_values = [hier_df[hier_df['model'] == m]['R_squared'].iloc[0] for m in models]
ax1 = axes[0]
bars = ax1.bar(models, r2_values, color=['#8B4513', '#4682B4'])
ax1.set_ylabel('R²', fontsize=12)
ax1.set_title('Model Comparison', fontsize=14)
ax1.set_ylim(0, 0.3)
for bar, val in zip(bars, r2_values):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
             f'{val:.3f}', ha='center', fontsize=10)

# Individual predictor effects
ax2 = axes[1]
cognitive_preds = pred_df[pred_df['predictor'].isin(['RAVLT_T', 'BVMT_T', 'RPM_T'])]
x_pos = np.arange(len(cognitive_preds))
ax2.bar(x_pos, cognitive_preds['sr2'].values, color='#4682B4')
ax2.set_xticks(x_pos)
ax2.set_xticklabels(['RAVLT', 'BVMT', 'RPM'])
ax2.set_ylabel('Semi-partial r²', fontsize=12)
ax2.set_title('Individual Predictor Effects', fontsize=14)
ax2.set_ylim(0, 0.06)

plt.tight_layout()
plt.savefig(RQ_DIR / "plots" / "hierarchical_regression.png")
plt.close()

# Figure 2: Cross-validation Results
fig, ax = plt.subplots(1, 1, figsize=(8, 6))
folds = cv_df['fold'].values
width = 0.35
x = np.arange(len(folds))
ax.bar(x - width/2, cv_df['train_R2'], width, label='Training', color='#4682B4')
ax.bar(x + width/2, cv_df['test_R2'], width, label='Test', color='#DC143C')
ax.set_xlabel('Fold', fontsize=12)
ax.set_ylabel('R²', fontsize=12)
ax.set_title('5-Fold Cross-Validation Results', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(folds)
ax.legend()
ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
plt.tight_layout()
plt.savefig(RQ_DIR / "plots" / "cross_validation.png")
plt.close()

# Figure 3: Confidence vs Accuracy Comparison
fig, ax = plt.subplots(1, 1, figsize=(8, 6))
comp_data = comparison_df[comparison_df['predictor'] != 'Overall_Model']
predictors = comp_data['predictor'].values
x_pos = np.arange(len(predictors))
width = 0.35
ax.bar(x_pos - width/2, comp_data['sr2_confidence'], width, 
       label='Confidence', color='#FF6347')
ax.bar(x_pos + width/2, comp_data['sr2_accuracy'], width, 
       label='Accuracy', color='#4169E1')
ax.set_xlabel('Cognitive Test', fontsize=12)
ax.set_ylabel('Semi-partial r²', fontsize=12)
ax.set_title('Confidence vs Accuracy Prediction', fontsize=14)
ax.set_xticks(x_pos)
ax.set_xticklabels(['RAVLT', 'BVMT', 'RPM'])
ax.legend()
plt.tight_layout()
plt.savefig(RQ_DIR / "plots" / "confidence_vs_accuracy.png")
plt.close()

print(f"Plots saved to {RQ_DIR / 'plots'}/")
