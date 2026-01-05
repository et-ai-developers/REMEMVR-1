#!/usr/bin/env python3
"""
Generate plots for RQ 7.3.5 - Calibration groups and cognitive reserve
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300

# Paths
RQ_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = RQ_DIR / "data"
PLOTS_DIR = RQ_DIR / "plots"

# Load data
groups_df = pd.read_csv(DATA_DIR / "step02_calibration_groups.csv")
anova_df = pd.read_csv(DATA_DIR / "step03_anova_results.csv")
corr_df = pd.read_csv(DATA_DIR / "step04_correlations.csv")

# Plot 1: Group comparisons on cognitive reserve indicators
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for idx, var in enumerate(['education', 'rpm', 'age']):
    ax = axes[idx]
    # Box plot
    groups_df.boxplot(column=var, by='group', ax=ax)
    ax.set_title(f'{var.capitalize()} by Calibration Group')
    ax.set_xlabel('Calibration Group')
    ax.set_ylabel(var.capitalize())
    plt.sca(ax)
    plt.xticks(rotation=45)

plt.suptitle('')  # Remove automatic suptitle from boxplot
plt.tight_layout()
plt.savefig(PLOTS_DIR / "calibration_groups_comparison.png", bbox_inches='tight')
plt.close()

# Plot 2: Calibration residuals vs cognitive reserve scatter plots
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for idx, var in enumerate(['education', 'rpm', 'age']):
    ax = axes[idx]
    # Scatter plot with regression line
    ax.scatter(groups_df['residual'], groups_df[var], alpha=0.6)
    
    # Add regression line
    z = np.polyfit(groups_df['residual'], groups_df[var], 1)
    p = np.poly1d(z)
    ax.plot(groups_df['residual'], p(groups_df['residual']), "r--", alpha=0.8)
    
    # Add correlation info
    corr_row = corr_df[corr_df['variable_pair'].str.contains(var)]
    if not corr_row.empty:
        r = corr_row['r'].values[0]
        p_val = corr_row['p_uncorrected'].values[0]
        ax.set_title(f'{var.capitalize()} vs Calibration Residual\nr = {r:.3f}, p = {p_val:.3f}')
    else:
        ax.set_title(f'{var.capitalize()} vs Calibration Residual')
    
    ax.set_xlabel('Calibration Residual')
    ax.set_ylabel(var.capitalize())
    ax.axvline(x=0, color='gray', linestyle=':', alpha=0.5)

plt.tight_layout()
plt.savefig(PLOTS_DIR / "calibration_correlations.png", bbox_inches='tight')
plt.close()

print(f"Plots saved to {PLOTS_DIR}")