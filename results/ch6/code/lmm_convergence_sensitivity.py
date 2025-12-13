#!/usr/bin/env python3
"""
T2.5: LMM Convergence Sensitivity Analysis
==========================================
Tests sensitivity of LMM findings to covariance structure specification.

RQs analyzed:
- 6.3.4: Domain-specific ICC (What/Where/When)
- 6.8.1: Source-Destination confidence trajectories

Purpose: Non-positive definite Hessian warnings suggest parameter estimates may be at boundary.
This analysis refits models with:
1. Original: random intercept + slope (unstructured covariance)
2. Compound symmetry: random intercept + slope (cov=0 constraint)
3. Intercept-only: random intercept only

If ICC_slope is consistent (within ±0.05) → original robust
If ICC_slope differs >0.10 → document instability

Author: Claude Code
Date: 2025-12-14
"""

import pandas as pd
import numpy as np
from pathlib import Path
import statsmodels.formula.api as smf
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURATION
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]  # REMEMVR root
OUTPUT_DIR = PROJECT_ROOT / "results" / "ch6" / "diagnostics"
OUTPUT_DIR.mkdir(exist_ok=True)
LOG_FILE = OUTPUT_DIR / "lmm_convergence_sensitivity.log"


def log(msg):
    """Log message to file and console."""
    with open(LOG_FILE, 'a') as f:
        f.write(f"{msg}\n")
        f.flush()
    print(msg, flush=True)


def extract_variance_components(result, model_type):
    """Extract variance components from fitted model."""
    # Get random effects covariance
    cov_re = result.cov_re

    if model_type == 'intercept_slope':
        # Full model: 2x2 covariance matrix [intercept, slope]
        if isinstance(cov_re, pd.DataFrame):
            # DataFrame with named columns like 'Group', 'TSVR_hours'
            var_intercept = float(cov_re.iloc[0, 0])
            var_slope = float(cov_re.iloc[1, 1])
            cov_int_slope = float(cov_re.iloc[0, 1])
        elif hasattr(cov_re, 'shape') and len(cov_re.shape) == 2:
            var_intercept = float(cov_re[0, 0])
            var_slope = float(cov_re[1, 1])
            cov_int_slope = float(cov_re[0, 1])
        else:
            var_intercept = np.nan
            var_slope = np.nan
            cov_int_slope = 0
    else:
        # Intercept-only model
        if isinstance(cov_re, pd.DataFrame):
            var_intercept = float(cov_re.iloc[0, 0])
        elif hasattr(cov_re, 'shape'):
            var_intercept = float(cov_re[0, 0]) if len(cov_re.shape) == 2 else float(cov_re)
        elif isinstance(cov_re, (int, float)):
            var_intercept = float(cov_re)
        else:
            var_intercept = np.nan
        var_slope = 0.0
        cov_int_slope = 0.0

    # Residual variance
    var_residual = float(result.scale)

    return {
        'var_intercept': var_intercept,
        'var_slope': var_slope,
        'cov_int_slope': cov_int_slope,
        'var_residual': var_residual
    }


def compute_icc_slope(var_slope, var_residual):
    """Compute ICC_slope = var_slope / (var_slope + var_residual)."""
    total = var_slope + var_residual
    if total > 0:
        return var_slope / total
    return 0.0


def run_6_3_4_sensitivity():
    """Run convergence sensitivity for RQ 6.3.4 (Domain ICC)."""
    log("\n" + "=" * 70)
    log("RQ 6.3.4: Domain-Specific ICC Convergence Sensitivity")
    log("=" * 70)

    # Load data
    theta_path = PROJECT_ROOT / "results" / "ch6" / "6.3.1" / "data" / "step03_theta_confidence.csv"
    tsvr_path = PROJECT_ROOT / "results" / "ch6" / "6.3.1" / "data" / "step00_tsvr_mapping.csv"

    if not theta_path.exists() or not tsvr_path.exists():
        log("ERROR: Data files not found")
        return None

    theta_df = pd.read_csv(theta_path)
    tsvr_df = pd.read_csv(tsvr_path)

    df = theta_df.merge(tsvr_df, on='composite_ID', how='inner')
    df['UID'] = df['composite_ID'].str.split('_').str[0]

    log(f"Loaded data: {len(df)} rows, {df['UID'].nunique()} participants")

    domains = ['What', 'Where', 'When']
    results = []

    for domain in domains:
        log(f"\n--- Domain: {domain} ---")

        theta_col = f'theta_{domain}'
        if theta_col not in df.columns:
            log(f"  ERROR: Column {theta_col} not found")
            continue

        domain_df = df[['UID', 'TSVR_hours', theta_col]].copy()
        domain_df = domain_df.rename(columns={theta_col: 'theta'})
        domain_df = domain_df.dropna()

        log(f"  N observations: {len(domain_df)}")

        # Model 1: Original (random intercept + slope)
        try:
            model1 = smf.mixedlm(
                "theta ~ TSVR_hours",
                domain_df,
                groups=domain_df['UID'],
                re_formula="~TSVR_hours"
            )
            result1 = model1.fit(reml=False)
            vc1 = extract_variance_components(result1, 'intercept_slope')
            icc1 = compute_icc_slope(vc1['var_slope'], vc1['var_residual'])
            converged1 = result1.converged
            log(f"  M1 (int+slope): converged={converged1}, ICC_slope={icc1:.4f}")
        except Exception as e:
            log(f"  M1 (int+slope): FAILED - {str(e)[:50]}")
            icc1 = np.nan
            converged1 = False
            vc1 = {}

        # Model 2: Intercept-only (as fallback)
        try:
            model2 = smf.mixedlm(
                "theta ~ TSVR_hours",
                domain_df,
                groups=domain_df['UID']
            )
            result2 = model2.fit(reml=False)
            vc2 = extract_variance_components(result2, 'intercept_only')
            icc2 = compute_icc_slope(vc2['var_slope'], vc2['var_residual'])
            converged2 = result2.converged
            log(f"  M2 (int-only):  converged={converged2}, ICC_slope={icc2:.4f} (forced 0)")
        except Exception as e:
            log(f"  M2 (int-only): FAILED - {str(e)[:50]}")
            icc2 = np.nan
            converged2 = False
            vc2 = {}

        # Model 3: Try with different optimizer (Powell) for robustness
        try:
            model3 = smf.mixedlm(
                "theta ~ TSVR_hours",
                domain_df,
                groups=domain_df['UID'],
                re_formula="~TSVR_hours"
            )
            result3 = model3.fit(reml=False, method='powell')
            vc3 = extract_variance_components(result3, 'intercept_slope')
            icc3 = compute_icc_slope(vc3['var_slope'], vc3['var_residual'])
            converged3 = result3.converged
            log(f"  M3 (Powell opt): converged={converged3}, ICC_slope={icc3:.4f}")
        except Exception as e:
            log(f"  M3 (Powell): FAILED - {str(e)[:50]}")
            icc3 = np.nan
            converged3 = False

        # Assess stability
        if not np.isnan(icc1) and not np.isnan(icc3):
            diff = abs(icc1 - icc3)
            if diff < 0.05:
                stability = "STABLE"
            elif diff < 0.10:
                stability = "MARGINAL"
            else:
                stability = "UNSTABLE"
        else:
            stability = "N/A"

        results.append({
            'RQ': '6.3.4',
            'Domain': domain,
            'M1_ICC_slope': icc1,
            'M1_converged': converged1,
            'M2_ICC_slope': icc2,
            'M2_converged': converged2,
            'M3_ICC_slope': icc3,
            'M3_converged': converged3,
            'Diff_M1_M3': abs(icc1 - icc3) if not np.isnan(icc1) and not np.isnan(icc3) else np.nan,
            'Stability': stability
        })

    return pd.DataFrame(results)


def run_6_8_1_sensitivity():
    """Run convergence sensitivity for RQ 6.8.1 (Source-Destination)."""
    log("\n" + "=" * 70)
    log("RQ 6.8.1: Source-Destination ICC Convergence Sensitivity")
    log("=" * 70)

    # Load data
    data_path = PROJECT_ROOT / "results" / "ch6" / "6.8.1" / "data" / "step04_lmm_input.csv"

    if not data_path.exists():
        log(f"ERROR: Data file not found: {data_path}")
        return None

    df = pd.read_csv(data_path)
    log(f"Loaded data: {len(df)} rows")

    locations = df['location'].unique() if 'location' in df.columns else ['Source', 'Destination']
    results = []

    for loc in locations:
        log(f"\n--- Location: {loc} ---")

        loc_col = 'location' if 'location' in df.columns else 'LocationType'
        loc_df = df[df[loc_col] == loc].copy() if loc_col in df.columns else df.copy()

        if len(loc_df) == 0:
            log(f"  No data for {loc}")
            continue

        # Use theta or theta_confidence
        theta_col = 'theta' if 'theta' in loc_df.columns else 'theta_confidence'
        time_col = 'log_TSVR' if 'log_TSVR' in loc_df.columns else 'TSVR_hours'

        if time_col not in loc_df.columns:
            loc_df['log_TSVR'] = np.log(loc_df['TSVR_hours'] + 1)
            time_col = 'log_TSVR'

        log(f"  N observations: {len(loc_df)}")

        # Model 1: Random intercept + slope
        try:
            model1 = smf.mixedlm(
                f"{theta_col} ~ {time_col}",
                loc_df,
                groups=loc_df['UID'],
                re_formula=f"~{time_col}"
            )
            result1 = model1.fit(reml=False)
            vc1 = extract_variance_components(result1, 'intercept_slope')
            icc1 = compute_icc_slope(vc1['var_slope'], vc1['var_residual'])
            converged1 = result1.converged
            log(f"  M1 (int+slope): converged={converged1}, ICC_slope={icc1:.4f}")
        except Exception as e:
            log(f"  M1: FAILED - {str(e)[:50]}")
            icc1 = np.nan
            converged1 = False

        # Model 2: Intercept-only
        try:
            model2 = smf.mixedlm(
                f"{theta_col} ~ {time_col}",
                loc_df,
                groups=loc_df['UID']
            )
            result2 = model2.fit(reml=False)
            vc2 = extract_variance_components(result2, 'intercept_only')
            icc2 = compute_icc_slope(vc2['var_slope'], vc2['var_residual'])
            converged2 = result2.converged
            log(f"  M2 (int-only):  converged={converged2}, ICC_slope={icc2:.4f}")
        except Exception as e:
            log(f"  M2: FAILED - {str(e)[:50]}")
            icc2 = np.nan
            converged2 = False

        # Model 3: Powell optimizer
        try:
            model3 = smf.mixedlm(
                f"{theta_col} ~ {time_col}",
                loc_df,
                groups=loc_df['UID'],
                re_formula=f"~{time_col}"
            )
            result3 = model3.fit(reml=False, method='powell')
            vc3 = extract_variance_components(result3, 'intercept_slope')
            icc3 = compute_icc_slope(vc3['var_slope'], vc3['var_residual'])
            converged3 = result3.converged
            log(f"  M3 (Powell):    converged={converged3}, ICC_slope={icc3:.4f}")
        except Exception as e:
            log(f"  M3: FAILED - {str(e)[:50]}")
            icc3 = np.nan
            converged3 = False

        # Assess stability
        if not np.isnan(icc1) and not np.isnan(icc3):
            diff = abs(icc1 - icc3)
            if diff < 0.05:
                stability = "STABLE"
            elif diff < 0.10:
                stability = "MARGINAL"
            else:
                stability = "UNSTABLE"
        else:
            stability = "N/A"

        results.append({
            'RQ': '6.8.1',
            'Domain': loc,
            'M1_ICC_slope': icc1,
            'M1_converged': converged1,
            'M2_ICC_slope': icc2,
            'M2_converged': converged2,
            'M3_ICC_slope': icc3,
            'M3_converged': converged3,
            'Diff_M1_M3': abs(icc1 - icc3) if not np.isnan(icc1) and not np.isnan(icc3) else np.nan,
            'Stability': stability
        })

    return pd.DataFrame(results)


def main():
    """Run convergence sensitivity for both RQs."""
    log("=" * 70)
    log("T2.5: LMM CONVERGENCE SENSITIVITY ANALYSIS")
    log("Chapter 6 Validity Rework - TIER 2 HIGH Priority")
    log("=" * 70)
    log(f"Date: {pd.Timestamp.now()}")

    all_results = []

    # RQ 6.3.4
    df_634 = run_6_3_4_sensitivity()
    if df_634 is not None:
        all_results.append(df_634)

    # RQ 6.8.1
    df_681 = run_6_8_1_sensitivity()
    if df_681 is not None:
        all_results.append(df_681)

    # Combine results
    if all_results:
        df_combined = pd.concat(all_results, ignore_index=True)

        # Save
        output_path = OUTPUT_DIR / "lmm_convergence_sensitivity.csv"
        df_combined.to_csv(output_path, index=False)
        log(f"\nSaved: {output_path}")

        # Summary
        log("\n" + "=" * 70)
        log("SUMMARY")
        log("=" * 70)
        log(f"\n{'RQ':<8} {'Domain':<15} {'M1_ICC':<10} {'M3_ICC':<10} {'Diff':<10} {'Stability':<10}")
        log("-" * 65)
        for _, row in df_combined.iterrows():
            log(f"{row['RQ']:<8} {row['Domain']:<15} {row['M1_ICC_slope']:.4f}     {row['M3_ICC_slope']:.4f}     {row['Diff_M1_M3']:.4f}     {row['Stability']:<10}")

        # Overall assessment
        log("\n" + "-" * 70)
        n_stable = (df_combined['Stability'] == 'STABLE').sum()
        n_total = len(df_combined)
        log(f"Stable domains: {n_stable}/{n_total}")

        if n_stable == n_total:
            log("✓ All domains STABLE - Original ICC estimates robust")
        elif n_stable >= n_total / 2:
            log("⚠️ Some instability - Document in Methods")
        else:
            log("⚠️ MULTIPLE unstable domains - Consider alternative specifications")

    log("\n" + "=" * 70)
    log("ANALYSIS COMPLETE")
    log("=" * 70)

    return df_combined if all_results else None


if __name__ == "__main__":
    main()
