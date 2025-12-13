#!/usr/bin/env python3
"""
T3.3: GLMM Refit for Non-Independence Issues
=============================================

Addresses non-independence in binary outcome analyses:
- RQ 6.2.2: Overconfidence trajectory (logistic regression → mixed-effects)
- RQ 6.5.3: HCE by congruence (LPM → proper GLMM/GEE)

Issue: Standard logistic regression ignores 4-obs-per-participant clustering.
Solution: Use Generalized Estimating Equations (GEE) with exchangeable correlation
         as a robust alternative when true GLMM not available in statsmodels.

References:
- Zeger & Liang (1986): GEE for longitudinal binary data
- Hubbard et al. (2010): GEE vs GLMM for clustered binary data
"""

import sys
from pathlib import Path
from datetime import datetime
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.genmod.generalized_estimating_equations import GEE
from statsmodels.genmod.cov_struct import Exchangeable, Independence
from statsmodels.genmod.families import Binomial
from scipy import stats

# =============================================================================
# PATHS AND CONFIGURATION
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]  # REMEMVR
OUTPUT_DIR = PROJECT_ROOT / "results" / "ch6" / "diagnostics"
LOG_FILE = OUTPUT_DIR / "glmm_refit_non_independence.log"

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def log(msg: str):
    """Log message to file and stdout."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] {msg}"
    with open(LOG_FILE, 'a') as f:
        f.write(log_msg + '\n')
        f.flush()
    print(log_msg, flush=True)

# Clear log file
LOG_FILE.write_text("")

# =============================================================================
# RQ 6.2.2: OVERCONFIDENCE TRAJECTORY - GEE REFIT
# =============================================================================

def refit_6_2_2():
    """
    Refit RQ 6.2.2 using GEE with exchangeable correlation structure.

    Original: Standard logistic regression (ignores clustering)
    Improved: GEE logistic with exchangeable correlation within UID

    Hypothesis: Proportion overconfident increases over time (Day 0 → Day 6)
    """
    log("=" * 70)
    log("RQ 6.2.2: Overconfidence Trajectory - GEE Refit")
    log("=" * 70)

    # Load data
    data_file = PROJECT_ROOT / "results" / "ch6" / "6.2.2" / "data" / "step01_calibration_classified.csv"
    log(f"Loading: {data_file}")
    df = pd.read_csv(data_file)
    log(f"  Loaded {len(df)} rows, {df['UID'].nunique()} participants")

    # Create binary outcome: 1 if Overconfident, 0 otherwise
    df['overconfident_binary'] = (df['Classification'] == 'Overconfident').astype(int)

    # Create time predictor: nominal days (T1=0, T2=1, T3=3, T4=6)
    time_map = {'T1': 0, 'T2': 1, 'T3': 3, 'T4': 6}
    df['time_ordinal'] = df['test'].map(time_map)

    # Sort by UID and time (required for GEE)
    df = df.sort_values(['UID', 'time_ordinal']).reset_index(drop=True)

    log(f"\nData summary:")
    log(f"  Overconfident: {df['overconfident_binary'].sum()} ({df['overconfident_binary'].mean()*100:.1f}%)")
    log(f"  Time points: {sorted(df['time_ordinal'].unique())}")

    # -------------------------------------------------------------------------
    # Original Analysis: Standard Logistic Regression (for comparison)
    # -------------------------------------------------------------------------
    log("\n--- ORIGINAL: Standard Logistic Regression ---")

    X_orig = sm.add_constant(df['time_ordinal'])
    y_orig = df['overconfident_binary']

    logit_orig = sm.Logit(y_orig, X_orig)
    result_orig = logit_orig.fit(disp=False)

    beta_orig = result_orig.params['time_ordinal']
    se_orig = result_orig.bse['time_ordinal']
    z_orig = result_orig.tvalues['time_ordinal']
    p_orig = result_orig.pvalues['time_ordinal']
    or_orig = np.exp(beta_orig)

    log(f"  Time effect: β = {beta_orig:.4f}, SE = {se_orig:.4f}")
    log(f"  z = {z_orig:.3f}, p = {p_orig:.4f}")
    log(f"  OR = {or_orig:.4f}")
    log(f"  Conclusion: {'SIGNIFICANT' if p_orig < 0.05 else 'NON-SIGNIFICANT'}")

    # -------------------------------------------------------------------------
    # GEE Analysis: Exchangeable Correlation
    # -------------------------------------------------------------------------
    log("\n--- GEE: Exchangeable Correlation Structure ---")

    # GEE with exchangeable correlation (assumes equal correlation between timepoints within person)
    fam = Binomial()
    cov_struct = Exchangeable()

    gee_model = GEE.from_formula(
        "overconfident_binary ~ time_ordinal",
        groups="UID",
        data=df,
        family=fam,
        cov_struct=cov_struct
    )

    try:
        result_gee = gee_model.fit()
        converged = True
        log("  GEE converged successfully")
    except Exception as e:
        log(f"  GEE with exchangeable failed: {e}")
        # Try with independence (effectively robust SE)
        log("  Attempting GEE with independence structure...")
        cov_struct = Independence()
        gee_model = GEE.from_formula(
            "overconfident_binary ~ time_ordinal",
            groups="UID",
            data=df,
            family=fam,
            cov_struct=cov_struct
        )
        result_gee = gee_model.fit()
        converged = True

    beta_gee = result_gee.params['time_ordinal']
    se_gee = result_gee.bse['time_ordinal']
    z_gee = result_gee.tvalues['time_ordinal']
    p_gee = result_gee.pvalues['time_ordinal']
    or_gee = np.exp(beta_gee)

    # 95% CI for OR
    ci_lower = np.exp(beta_gee - 1.96 * se_gee)
    ci_upper = np.exp(beta_gee + 1.96 * se_gee)

    log(f"  Time effect: β = {beta_gee:.4f}, SE = {se_gee:.4f}")
    log(f"  z = {z_gee:.3f}, p = {p_gee:.4f}")
    log(f"  OR = {or_gee:.4f} [{ci_lower:.4f}, {ci_upper:.4f}]")
    log(f"  Estimated correlation: {result_gee.cov_struct.summary()}")
    log(f"  Conclusion: {'SIGNIFICANT' if p_gee < 0.05 else 'NON-SIGNIFICANT'}")

    # -------------------------------------------------------------------------
    # Comparison
    # -------------------------------------------------------------------------
    log("\n--- COMPARISON: Original vs GEE ---")
    log(f"  {'Metric':<20} {'Original':>15} {'GEE':>15} {'Change':>15}")
    log(f"  {'-'*20} {'-'*15} {'-'*15} {'-'*15}")
    log(f"  {'β (log-odds/day)':<20} {beta_orig:>15.4f} {beta_gee:>15.4f} {beta_gee-beta_orig:>+15.4f}")
    log(f"  {'SE':<20} {se_orig:>15.4f} {se_gee:>15.4f} {se_gee-se_orig:>+15.4f}")
    log(f"  {'p-value':<20} {p_orig:>15.4f} {p_gee:>15.4f} {p_gee-p_orig:>+15.4f}")
    log(f"  {'OR':<20} {or_orig:>15.4f} {or_gee:>15.4f} {or_gee-or_orig:>+15.4f}")

    # Did conclusion change?
    orig_sig = p_orig < 0.05
    gee_sig = p_gee < 0.05
    conclusion_changed = orig_sig != gee_sig

    log(f"\n  Conclusion changed: {conclusion_changed}")
    if conclusion_changed:
        log(f"  IMPORTANT: Original was {'SIGNIFICANT' if orig_sig else 'NON-SIGNIFICANT'}, "
            f"GEE is {'SIGNIFICANT' if gee_sig else 'NON-SIGNIFICANT'}")
    else:
        log(f"  Both methods agree: {'SIGNIFICANT' if gee_sig else 'NON-SIGNIFICANT'}")

    return {
        'rq': '6.2.2',
        'analysis': 'Overconfidence Trajectory',
        'original_beta': beta_orig,
        'original_se': se_orig,
        'original_p': p_orig,
        'original_or': or_orig,
        'gee_beta': beta_gee,
        'gee_se': se_gee,
        'gee_p': p_gee,
        'gee_or': or_gee,
        'gee_or_ci_lower': ci_lower,
        'gee_or_ci_upper': ci_upper,
        'se_change_pct': (se_gee - se_orig) / se_orig * 100,
        'conclusion_changed': conclusion_changed,
        'original_conclusion': 'SIGNIFICANT' if orig_sig else 'NON-SIGNIFICANT',
        'gee_conclusion': 'SIGNIFICANT' if gee_sig else 'NON-SIGNIFICANT'
    }

# =============================================================================
# RQ 6.5.3: HIGH-CONFIDENCE ERRORS - GEE REFIT
# =============================================================================

def refit_6_5_3():
    """
    Refit RQ 6.5.3 using GEE with exchangeable correlation structure.

    Original: Linear probability model (MixedLM on binary outcome)
    Improved: GEE logistic with exchangeable correlation within UID

    Hypothesis: Incongruent items produce more high-confidence errors
    """
    log("\n" + "=" * 70)
    log("RQ 6.5.3: High-Confidence Errors by Congruence - GEE Refit")
    log("=" * 70)

    # Load data
    data_file = PROJECT_ROOT / "results" / "ch6" / "6.5.3" / "data" / "step01_hce_flags.csv"
    log(f"Loading: {data_file}")
    df = pd.read_csv(data_file)
    log(f"  Loaded {len(df)} rows, {df['UID'].nunique()} participants")

    # Time mapping
    time_map = {1: 0, 2: 1, 3: 3, 4: 6}
    df['Time'] = df['Test'].map(time_map)

    # Sort by UID and Time
    df = df.sort_values(['UID', 'Time', 'ItemID']).reset_index(drop=True)

    # Set reference level for Congruence
    df['Congruence'] = pd.Categorical(
        df['Congruence'],
        categories=['Common', 'Congruent', 'Incongruent']
    )

    log(f"\nData summary:")
    log(f"  HCE: {df['HCE_flag'].sum()} ({df['HCE_flag'].mean()*100:.1f}%)")
    log(f"  By Congruence:")
    for cong in ['Common', 'Congruent', 'Incongruent']:
        subset = df[df['Congruence'] == cong]
        rate = subset['HCE_flag'].mean() * 100
        log(f"    {cong}: {subset['HCE_flag'].sum()}/{len(subset)} ({rate:.1f}%)")

    # -------------------------------------------------------------------------
    # Original Analysis: Linear Probability Model (for comparison)
    # -------------------------------------------------------------------------
    log("\n--- ORIGINAL: Linear Probability Model (MixedLM) ---")

    # Read original results
    orig_results_file = PROJECT_ROOT / "results" / "ch6" / "6.5.3" / "data" / "step03_congruence_hce_test.csv"
    df_orig = pd.read_csv(orig_results_file)

    # Extract Incongruent effect (key hypothesis)
    incong_row = df_orig[df_orig['Effect'].str.contains('Incongruent') & ~df_orig['Effect'].str.contains(':')]
    if len(incong_row) > 0:
        beta_orig = incong_row['Estimate'].values[0]
        se_orig = incong_row['SE'].values[0]
        z_orig = incong_row['z_value'].values[0]
        p_orig = incong_row['p_value'].values[0]
    else:
        log("  WARNING: Could not find Incongruent effect in original results")
        beta_orig = se_orig = z_orig = p_orig = np.nan

    log(f"  Incongruent vs Common: β = {beta_orig:.4f}, SE = {se_orig:.4f}")
    log(f"  z = {z_orig:.3f}, p = {p_orig:.4f}")
    log(f"  Note: LPM - coefficients are probability changes, not log-odds")
    log(f"  Conclusion: {'SIGNIFICANT' if p_orig < 0.05 else 'NON-SIGNIFICANT'}")

    # -------------------------------------------------------------------------
    # GEE Analysis: Exchangeable Correlation (Logistic Link)
    # -------------------------------------------------------------------------
    log("\n--- GEE: Logistic with Exchangeable Correlation ---")

    fam = Binomial()
    cov_struct = Exchangeable()

    gee_model = GEE.from_formula(
        "HCE_flag ~ C(Congruence, Treatment('Common')) * Time",
        groups="UID",
        data=df,
        family=fam,
        cov_struct=cov_struct
    )

    try:
        result_gee = gee_model.fit()
        converged = True
        log("  GEE converged successfully")
    except Exception as e:
        log(f"  GEE with exchangeable failed: {e}")
        log("  Attempting GEE with independence structure...")
        cov_struct = Independence()
        gee_model = GEE.from_formula(
            "HCE_flag ~ C(Congruence, Treatment('Common')) * Time",
            groups="UID",
            data=df,
            family=fam,
            cov_struct=cov_struct
        )
        result_gee = gee_model.fit()
        converged = True

    # Find Incongruent effect
    param_names = result_gee.params.index.tolist()
    incong_name = [n for n in param_names if 'Incongruent' in n and ':' not in n][0]

    beta_gee = result_gee.params[incong_name]
    se_gee = result_gee.bse[incong_name]
    z_gee = result_gee.tvalues[incong_name]
    p_gee = result_gee.pvalues[incong_name]
    or_gee = np.exp(beta_gee)

    # 95% CI for OR
    ci_lower = np.exp(beta_gee - 1.96 * se_gee)
    ci_upper = np.exp(beta_gee + 1.96 * se_gee)

    log(f"  Incongruent vs Common: β = {beta_gee:.4f}, SE = {se_gee:.4f}")
    log(f"  z = {z_gee:.3f}, p = {p_gee:.4f}")
    log(f"  OR = {or_gee:.4f} [{ci_lower:.4f}, {ci_upper:.4f}]")
    log(f"  Estimated correlation: {result_gee.cov_struct.summary()}")
    log(f"  Conclusion: {'SIGNIFICANT' if p_gee < 0.05 else 'NON-SIGNIFICANT'}")

    # Full model summary
    log("\n  Full GEE Model Fixed Effects:")
    log(f"  {'Effect':<55} {'β':>10} {'SE':>10} {'z':>10} {'p':>10}")
    log(f"  {'-'*55} {'-'*10} {'-'*10} {'-'*10} {'-'*10}")
    for name in param_names:
        b = result_gee.params[name]
        s = result_gee.bse[name]
        z = result_gee.tvalues[name]
        p = result_gee.pvalues[name]
        sig = '*' if p < 0.05 else ''
        log(f"  {name:<55} {b:>10.4f} {s:>10.4f} {z:>10.3f} {p:>9.4f}{sig}")

    # -------------------------------------------------------------------------
    # Comparison
    # -------------------------------------------------------------------------
    log("\n--- COMPARISON: Original LPM vs GEE ---")
    log(f"  Note: LPM β is probability change; GEE β is log-odds change")
    log(f"  Direct comparison of p-values and conclusions only")
    log(f"")
    log(f"  {'Metric':<20} {'LPM':>15} {'GEE':>15}")
    log(f"  {'-'*20} {'-'*15} {'-'*15}")
    log(f"  {'p-value':<20} {p_orig:>15.4f} {p_gee:>15.4f}")

    # Did conclusion change?
    orig_sig = p_orig < 0.05
    gee_sig = p_gee < 0.05
    conclusion_changed = orig_sig != gee_sig

    log(f"\n  Conclusion changed: {conclusion_changed}")
    if conclusion_changed:
        log(f"  IMPORTANT: Original was {'SIGNIFICANT' if orig_sig else 'NON-SIGNIFICANT'}, "
            f"GEE is {'SIGNIFICANT' if gee_sig else 'NON-SIGNIFICANT'}")
    else:
        log(f"  Both methods agree: {'SIGNIFICANT' if gee_sig else 'NON-SIGNIFICANT'}")

    return {
        'rq': '6.5.3',
        'analysis': 'HCE by Congruence',
        'original_beta': beta_orig,
        'original_se': se_orig,
        'original_p': p_orig,
        'original_or': np.nan,  # LPM doesn't have OR
        'gee_beta': beta_gee,
        'gee_se': se_gee,
        'gee_p': p_gee,
        'gee_or': or_gee,
        'gee_or_ci_lower': ci_lower,
        'gee_or_ci_upper': ci_upper,
        'se_change_pct': np.nan,  # Different scales
        'conclusion_changed': conclusion_changed,
        'original_conclusion': 'SIGNIFICANT' if orig_sig else 'NON-SIGNIFICANT',
        'gee_conclusion': 'SIGNIFICANT' if gee_sig else 'NON-SIGNIFICANT'
    }

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Execute GLMM refit for both RQs."""
    log("=" * 70)
    log("T3.3: GLMM Refit for Non-Independence Issues")
    log("=" * 70)
    log(f"Start time: {datetime.now()}")
    log(f"Project root: {PROJECT_ROOT}")
    log("")

    results = []

    try:
        # Refit RQ 6.2.2
        result_6_2_2 = refit_6_2_2()
        results.append(result_6_2_2)

        # Refit RQ 6.5.3
        result_6_5_3 = refit_6_5_3()
        results.append(result_6_5_3)

        # Save combined results
        df_results = pd.DataFrame(results)
        out_file = OUTPUT_DIR / "glmm_refit_non_independence.csv"
        df_results.to_csv(out_file, index=False)
        log(f"\nSaved: {out_file}")

        # =====================================================================
        # FINAL SUMMARY
        # =====================================================================
        log("\n" + "=" * 70)
        log("FINAL SUMMARY")
        log("=" * 70)

        log("\n1. RQ 6.2.2 (Overconfidence Trajectory):")
        log(f"   Original (Logistic): p = {result_6_2_2['original_p']:.4f} ({result_6_2_2['original_conclusion']})")
        log(f"   GEE (Exchangeable): p = {result_6_2_2['gee_p']:.4f} ({result_6_2_2['gee_conclusion']})")
        log(f"   SE change: {result_6_2_2['se_change_pct']:+.1f}%")
        log(f"   Conclusion changed: {result_6_2_2['conclusion_changed']}")

        log("\n2. RQ 6.5.3 (HCE by Congruence):")
        log(f"   Original (LPM): p = {result_6_5_3['original_p']:.4f} ({result_6_5_3['original_conclusion']})")
        log(f"   GEE (Logistic): p = {result_6_5_3['gee_p']:.4f} ({result_6_5_3['gee_conclusion']})")
        log(f"   Conclusion changed: {result_6_5_3['conclusion_changed']}")

        # Overall assessment
        n_changed = sum(1 for r in results if r['conclusion_changed'])
        log(f"\n3. OVERALL:")
        log(f"   Conclusions changed: {n_changed}/2")

        if n_changed == 0:
            log("   ASSESSMENT: Findings ROBUST to non-independence correction")
            log("   Original analyses are ADEQUATE for thesis")
        else:
            log("   ASSESSMENT: Some findings CHANGED with proper clustering")
            log("   Recommend reporting GEE results in thesis")

        # Thesis recommendation
        log("\n4. THESIS RECOMMENDATION:")
        log("   Document in Methods: 'For binary outcomes with repeated measures,")
        log("   GEE with exchangeable correlation was used to account for within-")
        log("   participant clustering (Zeger & Liang, 1986).'")

    except Exception as e:
        log(f"\nERROR: {e}")
        import traceback
        log(traceback.format_exc())
        sys.exit(1)

    log("\n" + "=" * 70)
    log("T3.3 COMPLETE")
    log("=" * 70)
    log(f"End time: {datetime.now()}")

if __name__ == "__main__":
    main()
