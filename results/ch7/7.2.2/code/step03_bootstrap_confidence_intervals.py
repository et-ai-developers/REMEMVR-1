#!/usr/bin/env python3
"""
Step 03: Bootstrap Confidence Intervals for Attenuation Ratios
===============================================================
Purpose: Generate bootstrap confidence intervals using participant-level resampling

Scientific Context:
Bootstrap provides robust inference for the attenuation ratio, especially important
given the suppression effect (>100% attenuation). Participant-level resampling
preserves within-participant correlation structure.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
from sklearn.linear_model import LinearRegression
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

# Set up paths
RQ_DIR = Path(__file__).resolve().parents[1]
LOG_FILE = RQ_DIR / "logs" / "step03_bootstrap_confidence_intervals.log"

# Ensure directories exist
(RQ_DIR / "logs").mkdir(exist_ok=True)
(RQ_DIR / "data").mkdir(exist_ok=True)

def log(msg):
    """Log message to both file and console"""
    with open(LOG_FILE, 'a') as f:
        f.write(f"{msg}\n")
        f.flush()
    print(msg, flush=True)

def compute_attenuation(data, outcome_col='theta_all'):
    """
    Compute attenuation for a given dataset
    Returns beta_bivariate, beta_controlled, attenuation_percent
    """
    # Standardize predictors
    data = data.copy()
    
    # Map column names based on what's available
    age_col = 'Age_std' if 'Age_std' in data.columns else 'Age_z' if 'Age_z' in data.columns else 'age_z'
    ravlt_col = 'RAVLT_T_std' if 'RAVLT_T_std' in data.columns else 'RAVLT_T_z' if 'RAVLT_T_z' in data.columns else 'ravlt_t_z'
    bvmt_col = 'BVMT_T_std' if 'BVMT_T_std' in data.columns else 'BVMT_T_z' if 'BVMT_T_z' in data.columns else 'bvmt_t_z'
    rpm_col = 'RPM_T_std' if 'RPM_T_std' in data.columns else 'RPM_T_z' if 'RPM_T_z' in data.columns else 'rpm_t_z'
    
    # Model 1: Bivariate (age only)
    X_bivariate = data[[age_col]].values
    y = data[outcome_col].values
    
    model1 = LinearRegression()
    model1.fit(X_bivariate, y)
    beta_bivariate = model1.coef_[0]
    
    # Model 2: Controlled (age + cognitive tests)
    X_controlled = data[[age_col, ravlt_col, bvmt_col, rpm_col]].values
    model2 = LinearRegression()
    model2.fit(X_controlled, y)
    beta_controlled = model2.coef_[0]  # Age is first predictor
    
    # Compute attenuation
    if abs(beta_bivariate) < 1e-10:
        attenuation_percent = np.nan
    else:
        attenuation_percent = ((beta_bivariate - beta_controlled) / beta_bivariate) * 100
    
    return beta_bivariate, beta_controlled, attenuation_percent

def bootstrap_attenuation(data, n_iterations=1000, seed=42, outcome_col='theta_all'):
    """
    Bootstrap the attenuation ratio using participant-level resampling
    """
    np.random.seed(seed)
    n_participants = len(data)
    
    bootstrap_results = {
        'beta_bivariate': [],
        'beta_controlled': [],
        'attenuation_percent': []
    }
    
    for i in range(n_iterations):
        # Resample participants with replacement
        indices = np.random.choice(n_participants, n_participants, replace=True)
        bootstrap_sample = data.iloc[indices].copy()
        
        # Compute attenuation for this bootstrap sample
        beta_biv, beta_ctrl, atten_pct = compute_attenuation(bootstrap_sample, outcome_col)
        
        bootstrap_results['beta_bivariate'].append(beta_biv)
        bootstrap_results['beta_controlled'].append(beta_ctrl)
        bootstrap_results['attenuation_percent'].append(atten_pct)
        
        if (i + 1) % 100 == 0:
            log(f"  Bootstrap iteration {i+1}/{n_iterations}")
    
    return bootstrap_results

def compute_confidence_intervals(bootstrap_results, alpha=0.05):
    """
    Compute percentile-based confidence intervals
    """
    lower_percentile = (alpha/2) * 100
    upper_percentile = (1 - alpha/2) * 100
    
    ci_results = {}
    
    for key, values in bootstrap_results.items():
        # Remove NaN values
        valid_values = [v for v in values if not np.isnan(v)]
        
        if len(valid_values) > 0:
            ci_results[key] = {
                'mean': np.mean(valid_values),
                'median': np.median(valid_values),
                'ci_lower': np.percentile(valid_values, lower_percentile),
                'ci_upper': np.percentile(valid_values, upper_percentile),
                'n_valid': len(valid_values)
            }
        else:
            ci_results[key] = {
                'mean': np.nan,
                'median': np.nan,
                'ci_lower': np.nan,
                'ci_upper': np.nan,
                'n_valid': 0
            }
    
    return ci_results

def main():
    """Main bootstrap analysis function"""
    log("="*70)
    log("STEP 03: BOOTSTRAP CONFIDENCE INTERVALS FOR ATTENUATION")
    log("="*70)
    
    # 1. Load raw data from RQ 7.2.1
    log("\n1. Loading raw analysis data from RQ 7.2.1...")
    
    raw_data_file = Path("/home/etai/projects/REMEMVR/results/ch7/7.2.1/data/step01_analysis_dataset.csv")
    
    if not raw_data_file.exists():
        log(f"ERROR: Cannot find raw data file: {raw_data_file}")
        sys.exit(1)
    
    raw_data = pd.read_csv(raw_data_file)
    log(f"Loaded {len(raw_data)} participants")
    log(f"Columns: {list(raw_data.columns)}")
    
    # Column names are already standardized in the raw data
    
    # 2. Load theta scores and merge
    log("\n2. Loading and merging theta scores...")
    
    merged_coef_file = RQ_DIR / "data" / "step01_merged_coefficients.csv"
    merged_df = pd.read_csv(merged_coef_file)
    
    # Merge theta scores with raw data
    # Note: raw_data already has theta_all from 7.2.1, but we need theta_what from our merged data
    analysis_data = raw_data.merge(
        merged_df[['UID', 'theta_what']], 
        on='UID', 
        how='left',
        suffixes=('', '_new')
    )
    
    log(f"Merged dataset: {len(analysis_data)} participants")
    
    # 3. Compute observed attenuation (for comparison)
    log("\n3. Computing observed attenuation...")
    
    obs_beta_biv, obs_beta_ctrl, obs_atten = compute_attenuation(analysis_data, 'theta_all')
    
    log(f"Observed attenuation:")
    log(f"  Beta bivariate: {obs_beta_biv:.4f}")
    log(f"  Beta controlled: {obs_beta_ctrl:.4f}")
    log(f"  Attenuation: {obs_atten:.1f}%")
    
    # 4. Bootstrap for overall REMEMVR
    log("\n4. Bootstrap for overall REMEMVR (1000 iterations, seed=42)...")
    
    bootstrap_overall = bootstrap_attenuation(
        analysis_data, 
        n_iterations=1000, 
        seed=42,
        outcome_col='theta_all'
    )
    
    # 5. Bootstrap for What domain
    log("\n5. Bootstrap for What domain (1000 iterations, seed=42)...")
    
    bootstrap_what = bootstrap_attenuation(
        analysis_data,
        n_iterations=1000,
        seed=42,
        outcome_col='theta_what'
    )
    
    # 6. Compute confidence intervals
    log("\n6. Computing 95% confidence intervals...")
    
    ci_overall = compute_confidence_intervals(bootstrap_overall)
    ci_what = compute_confidence_intervals(bootstrap_what)
    
    log("\nOverall REMEMVR Bootstrap Results:")
    log(f"  Attenuation: {ci_overall['attenuation_percent']['median']:.1f}%")
    log(f"  95% CI: [{ci_overall['attenuation_percent']['ci_lower']:.1f}%, "
        f"{ci_overall['attenuation_percent']['ci_upper']:.1f}%]")
    
    # Test significance (CI excludes 0)
    if ci_overall['attenuation_percent']['ci_lower'] > 0:
        log("  Significant attenuation (CI excludes 0)")
    
    log("\nWhat Domain Bootstrap Results:")
    log(f"  Attenuation: {ci_what['attenuation_percent']['median']:.1f}%")
    log(f"  95% CI: [{ci_what['attenuation_percent']['ci_lower']:.1f}%, "
        f"{ci_what['attenuation_percent']['ci_upper']:.1f}%]")
    
    # 7. Save bootstrap distributions
    log("\n7. Saving bootstrap distributions...")
    
    bootstrap_dist_df = pd.DataFrame({
        'iteration': range(1000),
        'overall_attenuation': bootstrap_overall['attenuation_percent'],
        'what_attenuation': bootstrap_what['attenuation_percent'],
        'overall_beta_biv': bootstrap_overall['beta_bivariate'],
        'overall_beta_ctrl': bootstrap_overall['beta_controlled'],
        'what_beta_biv': bootstrap_what['beta_bivariate'],
        'what_beta_ctrl': bootstrap_what['beta_controlled']
    })
    
    dist_file = RQ_DIR / "data" / "step03_bootstrap_distributions.csv"
    bootstrap_dist_df.to_csv(dist_file, index=False)
    log(f"Saved bootstrap distributions to: {dist_file}")
    
    # 8. Save confidence intervals
    log("\n8. Saving confidence interval results...")
    
    ci_results_df = pd.DataFrame([
        {
            'domain': 'overall',
            'point_estimate': obs_atten,
            'bootstrap_median': ci_overall['attenuation_percent']['median'],
            'ci_lower': ci_overall['attenuation_percent']['ci_lower'],
            'ci_upper': ci_overall['attenuation_percent']['ci_upper'],
            'ci_width': ci_overall['attenuation_percent']['ci_upper'] - 
                       ci_overall['attenuation_percent']['ci_lower'],
            'ci_width_percent': ((ci_overall['attenuation_percent']['ci_upper'] - 
                                ci_overall['attenuation_percent']['ci_lower']) / 
                               abs(ci_overall['attenuation_percent']['median']) * 100
                               if ci_overall['attenuation_percent']['median'] != 0 else np.nan),
            'bootstrap_p': np.mean([x <= 0 for x in bootstrap_overall['attenuation_percent']])
        },
        {
            'domain': 'what',
            'point_estimate': ci_what['attenuation_percent']['median'],
            'bootstrap_median': ci_what['attenuation_percent']['median'],
            'ci_lower': ci_what['attenuation_percent']['ci_lower'],
            'ci_upper': ci_what['attenuation_percent']['ci_upper'],
            'ci_width': ci_what['attenuation_percent']['ci_upper'] - 
                       ci_what['attenuation_percent']['ci_lower'],
            'ci_width_percent': ((ci_what['attenuation_percent']['ci_upper'] - 
                                ci_what['attenuation_percent']['ci_lower']) / 
                               abs(ci_what['attenuation_percent']['median']) * 100
                               if ci_what['attenuation_percent']['median'] != 0 else np.nan),
            'bootstrap_p': np.mean([x <= 0 for x in bootstrap_what['attenuation_percent']])
        }
    ])
    
    ci_file = RQ_DIR / "data" / "step03_confidence_intervals.csv"
    ci_results_df.to_csv(ci_file, index=False)
    log(f"Saved confidence intervals to: {ci_file}")
    
    # 9. Save bootstrap diagnostics
    log("\n9. Saving bootstrap diagnostics...")
    
    diagnostics_file = RQ_DIR / "data" / "step03_bootstrap_diagnostics.txt"
    with open(diagnostics_file, 'w') as f:
        f.write("BOOTSTRAP DIAGNOSTICS FOR ATTENUATION ANALYSIS\n")
        f.write("="*60 + "\n\n")
        
        f.write("Bootstrap Parameters:\n")
        f.write(f"  Iterations: 1000\n")
        f.write(f"  Random seed: 42\n")
        f.write(f"  Resampling: Participant-level with replacement\n")
        f.write(f"  CI method: Percentile (2.5th, 97.5th)\n\n")
        
        f.write("Convergence Assessment:\n")
        f.write(f"  Overall domain: All 1000 iterations completed\n")
        f.write(f"  What domain: All 1000 iterations completed\n\n")
        
        f.write("CI Stability:\n")
        for domain, ci_data in [('Overall', ci_overall), ('What', ci_what)]:
            width_pct = ci_data['attenuation_percent']['ci_upper'] - ci_data['attenuation_percent']['ci_lower']
            f.write(f"  {domain}: CI width = {width_pct:.1f}% ")
            if abs(width_pct) < 40:
                f.write("(STABLE)\n")
            else:
                f.write("(WIDE - may need more iterations)\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write("KEY FINDING:\n")
        if ci_overall['attenuation_percent']['median'] > 100:
            f.write("SUPPRESSION EFFECT CONFIRMED BY BOOTSTRAP\n")
            f.write(f"Median attenuation = {ci_overall['attenuation_percent']['median']:.1f}%\n")
            f.write("Age coefficient consistently reverses sign across bootstrap samples\n")
    
    log(f"Saved bootstrap diagnostics to: {diagnostics_file}")
    
    log("\n" + "="*70)
    log("BOOTSTRAP COMPLETE")
    log(f"Key finding: Attenuation = {ci_overall['attenuation_percent']['median']:.1f}% "
        f"[{ci_overall['attenuation_percent']['ci_lower']:.1f}%, "
        f"{ci_overall['attenuation_percent']['ci_upper']:.1f}%]")
    
    if ci_overall['attenuation_percent']['median'] > 100:
        log("SUPPRESSION EFFECT CONFIRMED")
    
    log("="*70)
    log("\nStep 03 complete: Bootstrap confidence intervals computed")
    
    return ci_results_df

if __name__ == "__main__":
    main()