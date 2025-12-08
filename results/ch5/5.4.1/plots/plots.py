#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plotting script for RQ 5.4.1 - Schema Congruence Effects on Forgetting Trajectories

REGENERATED: 2025-12-08
PURPOSE: Update plots with model-averaged predictions from kitchen sink analysis (66 models)

CONTEXT:
- Original plots based on 5-model Log comparison
- Extended analysis: Kitchen sink (66 models) + model averaging
- EXTREME model uncertainty: 15 competitive models (effective N=13.96)
- Best model: PowerLaw_01 (6.0% weight), Log #2 (5.7% weight)
- Model averaging MANDATORY due to extreme uncertainty

PLOTS GENERATED:
1. trajectory_theta.png - Theta-scale trajectory (ORIGINAL, empirical data only)
2. trajectory_probability.png - Probability-scale trajectory (ORIGINAL, empirical data only)
3. trajectory_averaged_theta.png - Model-averaged theta trajectories with uncertainty
4. trajectory_averaged_probability.png - Model-averaged probability trajectories with uncertainty

DECISION D069 COMPLIANCE:
Both theta-scale AND probability-scale trajectory plots are generated
to ensure interpretability for both psychometricians and general audiences.

MODEL AVERAGING NOTE:
The kitchen sink revealed EXTREME model uncertainty with 15 competitive models
(ΔAIC < 2). This is the most extreme case in Chapter 5. Model-averaged predictions
provide robust estimates that account for model uncertainty.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.plotting import set_plot_style_defaults, convert_theta_to_probability

# =============================================================================
# SETUP
# =============================================================================

# Get absolute path to RQ root (plots.py is in results/ch5/5.4.1/plots/)
RQ_ROOT = Path(__file__).parent.parent

# Apply consistent plotting theme from config/plotting.yaml
set_plot_style_defaults()

print("=" * 70)
print("PLOTTING FOR RQ 5.4.1: Schema Congruence Forgetting Trajectories")
print("WITH MODEL-AVERAGED PREDICTIONS (Kitchen Sink: 66 models)")
print("=" * 70)
print(f"RQ root: {RQ_ROOT}")

# Color scheme for congruence categories (consistent with REMEMVR project)
COLORS = {
    "common": "#9B59B6",       # Purple - schema-neutral baseline
    "congruent": "#2ECC71",    # Green - schema-consistent
    "incongruent": "#E74C3C"   # Red - schema-violating
}

# =============================================================================
# PLOT 1: TRAJECTORY (THETA-SCALE) - ORIGINAL EMPIRICAL
# =============================================================================

print("\n" + "-" * 70)
print("Generating Plot 1: Theta-scale trajectory (ORIGINAL, empirical data)...")
print("-" * 70)

# Load plot source CSV (created by analysis pipeline in step07)
theta_data_path = RQ_ROOT / "plots" / "step07_trajectory_theta_data.csv"
df_theta = pd.read_csv(theta_data_path)
print(f"  Loaded {len(df_theta)} rows from step07_trajectory_theta_data.csv")
print(f"  Columns: {list(df_theta.columns)}")
print(f"  Congruence categories: {df_theta['congruence'].unique().tolist()}")

# Create figure
fig_theta, ax_theta = plt.subplots(figsize=(10, 6))

# Plot each congruence category
for congruence in ["common", "congruent", "incongruent"]:
    group_data = df_theta[df_theta["congruence"] == congruence].sort_values("time")

    color = COLORS.get(congruence, "#333333")
    label = congruence.capitalize()

    # Plot mean line with markers
    ax_theta.plot(
        group_data["time"],
        group_data["theta_mean"],
        "o-",
        color=color,
        linewidth=2.5,
        markersize=8,
        label=label
    )

    # Add confidence interval band
    ax_theta.fill_between(
        group_data["time"],
        group_data["CI_lower"],
        group_data["CI_upper"],
        color=color,
        alpha=0.2
    )

# Formatting
ax_theta.set_xlabel("Time Since VR Encoding (hours)", fontweight="bold")
ax_theta.set_ylabel("Memory Ability (Theta)", fontweight="bold")
ax_theta.set_title("RQ 5.4.1: Forgetting Trajectories by Schema Congruence - Theta Scale\n(Empirical Data)",
                   fontweight="bold", pad=15)
ax_theta.legend(title="Congruence", loc="upper right", framealpha=0.95)
ax_theta.grid(True, alpha=0.3)

# Add horizontal reference line at theta=0
ax_theta.axhline(y=0, color="gray", linestyle="--", linewidth=1, alpha=0.5)

plt.tight_layout()

# Save theta-scale plot
theta_output_path = RQ_ROOT / "plots" / "trajectory_theta.png"
fig_theta.savefig(theta_output_path, dpi=300, bbox_inches="tight")
plt.close(fig_theta)

print(f"  [PASS] Saved: {theta_output_path}")

# =============================================================================
# PLOT 2: TRAJECTORY (PROBABILITY-SCALE) - ORIGINAL EMPIRICAL
# =============================================================================

print("\n" + "-" * 70)
print("Generating Plot 2: Probability-scale trajectory (ORIGINAL, empirical data)...")
print("-" * 70)

# Load plot source CSV
prob_data_path = RQ_ROOT / "plots" / "step07_trajectory_probability_data.csv"
df_prob = pd.read_csv(prob_data_path)
print(f"  Loaded {len(df_prob)} rows from step07_trajectory_probability_data.csv")
print(f"  Columns: {list(df_prob.columns)}")

# Create figure
fig_prob, ax_prob = plt.subplots(figsize=(10, 6))

# Plot each congruence category
for congruence in ["common", "congruent", "incongruent"]:
    group_data = df_prob[df_prob["congruence"] == congruence].sort_values("time")

    color = COLORS.get(congruence, "#333333")
    label = congruence.capitalize()

    # Convert probability to percentage for display
    mean_pct = group_data["prob_mean"] * 100
    ci_lower_pct = group_data["CI_lower"] * 100
    ci_upper_pct = group_data["CI_upper"] * 100

    # Plot mean line with markers
    ax_prob.plot(
        group_data["time"],
        mean_pct,
        "o-",
        color=color,
        linewidth=2.5,
        markersize=8,
        label=label
    )

    # Add confidence interval band
    ax_prob.fill_between(
        group_data["time"],
        ci_lower_pct,
        ci_upper_pct,
        color=color,
        alpha=0.2
    )

# Formatting
ax_prob.set_xlabel("Time Since VR Encoding (hours)", fontweight="bold")
ax_prob.set_ylabel("Probability Correct (%)", fontweight="bold")
ax_prob.set_title("RQ 5.4.1: Forgetting Trajectories by Schema Congruence - Probability Scale\n(Empirical Data)",
                  fontweight="bold", pad=15)
ax_prob.legend(title="Congruence", loc="upper right", framealpha=0.95)
ax_prob.grid(True, alpha=0.3)

# Set y-axis limits to 0-100% range
ax_prob.set_ylim(0, 100)

# Add horizontal reference line at 50% (chance level for binary items)
ax_prob.axhline(y=50, color="gray", linestyle="--", linewidth=1, alpha=0.5, label="_nolegend_")

plt.tight_layout()

# Save probability-scale plot
prob_output_path = RQ_ROOT / "plots" / "trajectory_probability.png"
fig_prob.savefig(prob_output_path, dpi=300, bbox_inches="tight")
plt.close(fig_prob)

print(f"  [PASS] Saved: {prob_output_path}")

# =============================================================================
# PLOT 3: MODEL-AVERAGED TRAJECTORY (THETA-SCALE)
# =============================================================================

print("\n" + "-" * 70)
print("Generating Plot 3: Model-averaged theta-scale trajectory...")
print("  (Kitchen sink: 66 models, 15 competitive within ΔAIC < 2)")
print("-" * 70)

# Load model-averaged predictions
avg_data_path = RQ_ROOT / "data" / "step05c_averaged_predictions.csv"
df_avg = pd.read_csv(avg_data_path)
print(f"  Loaded {len(df_avg)} rows from step05c_averaged_predictions.csv")
print(f"  Columns: {list(df_avg.columns)}")
print(f"  Congruence categories: {df_avg['congruence'].unique().tolist()}")

# Create figure
fig_avg_theta, ax_avg_theta = plt.subplots(figsize=(10, 6))

# Plot each congruence category
for congruence in ["common", "congruent", "incongruent"]:
    group_data = df_avg[df_avg["congruence"] == congruence].sort_values("TSVR_hours")

    color = COLORS.get(congruence, "#333333")
    label = congruence.capitalize()

    # Model-averaged prediction
    theta_avg = group_data["theta_averaged"]

    # Uncertainty band (prediction SE = sqrt(prediction_variance))
    se = group_data["prediction_se"]
    ci_lower = theta_avg - 1.96 * se
    ci_upper = theta_avg + 1.96 * se

    # Plot model-averaged trajectory (smooth line, no markers)
    ax_avg_theta.plot(
        group_data["TSVR_hours"],
        theta_avg,
        "-",
        color=color,
        linewidth=2.5,
        label=label
    )

    # Add uncertainty band (lighter, more transparent to show model uncertainty)
    ax_avg_theta.fill_between(
        group_data["TSVR_hours"],
        ci_lower,
        ci_upper,
        color=color,
        alpha=0.15,
        label=f"{label} 95% CI"
    )

# Formatting
ax_avg_theta.set_xlabel("Time Since VR Encoding (hours)", fontweight="bold")
ax_avg_theta.set_ylabel("Memory Ability (Theta)", fontweight="bold")
ax_avg_theta.set_title("RQ 5.4.1: Model-Averaged Forgetting Trajectories - Theta Scale\n" +
                        "(66 models, 15 competitive, effective N = 13.96)",
                        fontweight="bold", pad=15, fontsize=12)
ax_avg_theta.legend(title="Congruence", loc="upper right", framealpha=0.95, fontsize=9)
ax_avg_theta.grid(True, alpha=0.3)

# Add horizontal reference line at theta=0
ax_avg_theta.axhline(y=0, color="gray", linestyle="--", linewidth=1, alpha=0.5)

# Add annotation about extreme model uncertainty
annotation_text = ("Uncertainty bands reflect model uncertainty\n" +
                  "(15 models within ΔAIC < 2)")
ax_avg_theta.text(0.02, 0.02, annotation_text,
                  transform=ax_avg_theta.transAxes,
                  fontsize=8, style='italic',
                  bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3),
                  verticalalignment='bottom')

plt.tight_layout()

# Save model-averaged theta-scale plot
avg_theta_output_path = RQ_ROOT / "plots" / "trajectory_averaged_theta.png"
fig_avg_theta.savefig(avg_theta_output_path, dpi=300, bbox_inches="tight")
plt.close(fig_avg_theta)

print(f"  [PASS] Saved: {avg_theta_output_path}")

# =============================================================================
# PLOT 4: MODEL-AVERAGED TRAJECTORY (PROBABILITY-SCALE)
# =============================================================================

print("\n" + "-" * 70)
print("Generating Plot 4: Model-averaged probability-scale trajectory (Decision D069)...")
print("-" * 70)

# Load item parameters to get mean discrimination
item_params_path = RQ_ROOT / "data" / "step03_item_parameters.csv"
df_items = pd.read_csv(item_params_path)
mean_discrimination = df_items['a'].mean()
print(f"  Mean item discrimination: {mean_discrimination:.3f}")

# Create figure
fig_avg_prob, ax_avg_prob = plt.subplots(figsize=(10, 6))

# Plot each congruence category
for congruence in ["common", "congruent", "incongruent"]:
    group_data = df_avg[df_avg["congruence"] == congruence].sort_values("TSVR_hours")

    color = COLORS.get(congruence, "#333333")
    label = congruence.capitalize()

    # Convert theta to probability using IRT 2PL transformation
    theta_avg = group_data["theta_averaged"]
    prob_avg = convert_theta_to_probability(theta_avg.values,
                                            discrimination=mean_discrimination,
                                            difficulty=0.0) * 100  # Convert to percentage

    # Uncertainty propagation: Transform CI bounds to probability scale
    se = group_data["prediction_se"]
    theta_lower = theta_avg - 1.96 * se
    theta_upper = theta_avg + 1.96 * se
    prob_lower = convert_theta_to_probability(theta_lower.values,
                                              discrimination=mean_discrimination,
                                              difficulty=0.0) * 100
    prob_upper = convert_theta_to_probability(theta_upper.values,
                                              discrimination=mean_discrimination,
                                              difficulty=0.0) * 100

    # Plot model-averaged trajectory
    ax_avg_prob.plot(
        group_data["TSVR_hours"],
        prob_avg,
        "-",
        color=color,
        linewidth=2.5,
        label=label
    )

    # Add uncertainty band
    ax_avg_prob.fill_between(
        group_data["TSVR_hours"],
        prob_lower,
        prob_upper,
        color=color,
        alpha=0.15,
        label=f"{label} 95% CI"
    )

# Formatting
ax_avg_prob.set_xlabel("Time Since VR Encoding (hours)", fontweight="bold")
ax_avg_prob.set_ylabel("Probability Correct (%)", fontweight="bold")
ax_avg_prob.set_title("RQ 5.4.1: Model-Averaged Forgetting Trajectories - Probability Scale\n" +
                      "(66 models, 15 competitive, effective N = 13.96)",
                      fontweight="bold", pad=15, fontsize=12)
ax_avg_prob.legend(title="Congruence", loc="upper right", framealpha=0.95, fontsize=9)
ax_avg_prob.grid(True, alpha=0.3)

# Set y-axis limits to 0-100% range
ax_avg_prob.set_ylim(0, 100)

# Add horizontal reference line at 50% (chance level)
ax_avg_prob.axhline(y=50, color="gray", linestyle="--", linewidth=1, alpha=0.5, label="_nolegend_")

# Add annotation about extreme model uncertainty
annotation_text = ("Uncertainty bands reflect model uncertainty\n" +
                  "(15 models within ΔAIC < 2)")
ax_avg_prob.text(0.02, 0.02, annotation_text,
                 transform=ax_avg_prob.transAxes,
                 fontsize=8, style='italic',
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3),
                 verticalalignment='bottom')

plt.tight_layout()

# Save model-averaged probability-scale plot
avg_prob_output_path = RQ_ROOT / "plots" / "trajectory_averaged_probability.png"
fig_avg_prob.savefig(avg_prob_output_path, dpi=300, bbox_inches="tight")
plt.close(fig_avg_prob)

print(f"  [PASS] Saved: {avg_prob_output_path}")

# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "=" * 70)
print("PLOTTING COMPLETE")
print("=" * 70)
print(f"Total plots generated: 4")
print(f"  - plots/trajectory_theta.png (Theta scale, empirical)")
print(f"  - plots/trajectory_probability.png (Probability scale, empirical)")
print(f"  - plots/trajectory_averaged_theta.png (Theta scale, model-averaged)")
print(f"  - plots/trajectory_averaged_probability.png (Probability scale, model-averaged)")
print("")
print("Decision D069 Compliance: BOTH theta-scale AND probability-scale plots generated")
print("Model Averaging: Kitchen sink (66 models) with extreme uncertainty (15 competitive)")
print("All plots saved with 300 DPI publication quality.")
print("=" * 70)
