#!/usr/bin/env python3
"""
RQ 6.2.2: Over-Underconfidence Trajectory Plots
================================================

Creates dual-panel plot showing:
1. Proportion overconfident by timepoint (left y-axis concept)
2. Mean calibration by timepoint with zero line

Both panels use same x-axis (Days since encoding).
"""

import sys
from pathlib import Path

# Add project root to path for tools imports
PROJECT_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ============================================================================
# SETUP
# ============================================================================

RQ_DIR = Path(__file__).resolve().parents[1]  # results/ch6/6.2.2
DATA_DIR = RQ_DIR / "data"
PLOTS_DIR = RQ_DIR / "plots"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# LOAD DATA
# ============================================================================

# Load plot data
df_plot = pd.read_csv(DATA_DIR / "step05_overconfidence_trajectory_data.csv")
df_trend = pd.read_csv(DATA_DIR / "step03_trend_test.csv")

# Extract trend test results
time_row = df_trend[df_trend['term'] == 'time_ordinal'].iloc[0]
trend_p = time_row['p_value']
trend_or = time_row['OR']

# ============================================================================
# PLOT 1: Proportion Overconfident Trajectory
# ============================================================================

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Panel A: Proportion Overconfident
ax1 = axes[0]

# Plot points with error bars
ax1.errorbar(
    df_plot['time_numeric'],
    df_plot['proportion_overconfident'],
    yerr=[
        df_plot['proportion_overconfident'] - df_plot['prop_CI_lower'],
        df_plot['prop_CI_upper'] - df_plot['proportion_overconfident']
    ],
    fmt='o-',
    color='#e74c3c',
    capsize=5,
    markersize=10,
    linewidth=2,
    label='Proportion Overconfident'
)

# Reference line at 0.5 (chance level for binary classification)
ax1.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='50% (chance)')

# Labels
ax1.set_xlabel('Days Since Encoding', fontsize=12)
ax1.set_ylabel('Proportion Overconfident', fontsize=12)
ax1.set_title('A. Proportion Overconfident Over Time', fontsize=14, fontweight='bold')
ax1.set_xticks([0, 1, 3, 6])
ax1.set_xticklabels(['Day 0\n(T1)', 'Day 1\n(T2)', 'Day 3\n(T3)', 'Day 6\n(T4)'])
ax1.set_ylim(0.25, 0.75)
ax1.set_xlim(-0.5, 7)
ax1.legend(loc='lower right')
ax1.grid(True, alpha=0.3)

# Add trend test annotation
if trend_p < 0.05:
    sig_text = f"Trend: OR={trend_or:.2f}, p={trend_p:.3f}*"
else:
    sig_text = f"Trend: OR={trend_or:.2f}, p={trend_p:.3f} (n.s.)"
ax1.annotate(sig_text, xy=(0.05, 0.95), xycoords='axes fraction',
             fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Panel B: Mean Calibration
ax2 = axes[1]

# Plot points with error bars
ax2.errorbar(
    df_plot['time_numeric'],
    df_plot['mean_calibration'],
    yerr=[
        df_plot['mean_calibration'] - df_plot['mean_CI_lower'],
        df_plot['mean_CI_upper'] - df_plot['mean_calibration']
    ],
    fmt='s-',
    color='#3498db',
    capsize=5,
    markersize=10,
    linewidth=2,
    label='Mean Calibration'
)

# Reference line at 0 (perfect calibration)
ax2.axhline(y=0, color='black', linestyle='-', linewidth=1, label='Perfect Calibration')

# Add shading for over/underconfidence regions
ax2.axhspan(0, 1.5, alpha=0.1, color='red', label='Overconfident region')
ax2.axhspan(-1.5, 0, alpha=0.1, color='green', label='Underconfident region')

# Labels
ax2.set_xlabel('Days Since Encoding', fontsize=12)
ax2.set_ylabel('Mean Calibration (z-units)', fontsize=12)
ax2.set_title('B. Mean Calibration Over Time', fontsize=14, fontweight='bold')
ax2.set_xticks([0, 1, 3, 6])
ax2.set_xticklabels(['Day 0\n(T1)', 'Day 1\n(T2)', 'Day 3\n(T3)', 'Day 6\n(T4)'])
ax2.set_ylim(-0.5, 0.5)
ax2.set_xlim(-0.5, 7)
ax2.legend(loc='lower right', fontsize=8)
ax2.grid(True, alpha=0.3)

# Add calibration interpretation
t1_cal = df_plot[df_plot['test'] == 'T1']['mean_calibration'].iloc[0]
t4_cal = df_plot[df_plot['test'] == 'T4']['mean_calibration'].iloc[0]
delta = t4_cal - t1_cal
interp_text = f"T1: {t1_cal:.2f} (under)\nT4: {t4_cal:+.2f} (over)\nΔ: {delta:+.2f}"
ax2.annotate(interp_text, xy=(0.95, 0.05), xycoords='axes fraction',
             fontsize=9, verticalalignment='bottom', horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig(PLOTS_DIR / 'overconfidence_trajectory.png', dpi=150, bbox_inches='tight')
plt.close()

print(f"Saved: {PLOTS_DIR / 'overconfidence_trajectory.png'}")

# ============================================================================
# PLOT 2: Classification Distribution by Timepoint (Stacked Bar)
# ============================================================================

# Load classified data for stacked bar chart
df_classified = pd.read_csv(DATA_DIR / "step01_calibration_classified.csv")

# Compute proportions by test and classification
prop_data = []
for test in ['T1', 'T2', 'T3', 'T4']:
    test_data = df_classified[df_classified['test'] == test]
    n_total = len(test_data)
    for cat in ['Underconfident', 'Calibrated', 'Overconfident']:
        n_cat = (test_data['Classification'] == cat).sum()
        prop_data.append({
            'test': test,
            'category': cat,
            'count': n_cat,
            'proportion': n_cat / n_total
        })

df_stack = pd.DataFrame(prop_data)

# Pivot for stacking
df_pivot = df_stack.pivot(index='test', columns='category', values='proportion')
df_pivot = df_pivot[['Underconfident', 'Calibrated', 'Overconfident']]  # Order

# Create stacked bar chart
fig, ax = plt.subplots(figsize=(8, 6))

x = np.arange(4)
width = 0.6

# Colors
colors = {'Underconfident': '#2ecc71', 'Calibrated': '#95a5a6', 'Overconfident': '#e74c3c'}

# Stack bars
bottom = np.zeros(4)
for cat in ['Underconfident', 'Calibrated', 'Overconfident']:
    values = df_pivot[cat].values
    ax.bar(x, values, width, bottom=bottom, label=cat, color=colors[cat])
    bottom += values

# Reference line at 50%
ax.axhline(y=0.5, color='white', linestyle='--', linewidth=2, alpha=0.7)

# Labels
ax.set_xlabel('Test Session', fontsize=12)
ax.set_ylabel('Proportion', fontsize=12)
ax.set_title('Classification Distribution by Timepoint', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(['Day 0 (T1)', 'Day 1 (T2)', 'Day 3 (T3)', 'Day 6 (T4)'])
ax.set_ylim(0, 1)
ax.legend(loc='upper right')

plt.tight_layout()
plt.savefig(PLOTS_DIR / 'classification_distribution.png', dpi=150, bbox_inches='tight')
plt.close()

print(f"Saved: {PLOTS_DIR / 'classification_distribution.png'}")

# ============================================================================
# SUMMARY
# ============================================================================

print("\nPlots created successfully:")
print(f"  1. {PLOTS_DIR / 'overconfidence_trajectory.png'} - Dual-panel trajectory plot")
print(f"  2. {PLOTS_DIR / 'classification_distribution.png'} - Stacked bar classification")
