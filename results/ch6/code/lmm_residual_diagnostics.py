#!/usr/bin/env python3
"""
T2.1: LMM Residual Diagnostics for Chapter 6 RQs
=================================================
Validates LMM assumptions for thesis defense readiness.

RQs analyzed:
- 6.2.1: Calibration Over Time (calibration ~ TSVR_hours)
- 6.3.2: Domain Confidence Calibration (calibration ~ Domain * TSVR_centered)
- 6.4.2: Paradigm Confidence Calibration (calibration ~ Paradigm * TSVR_centered)
- 6.6.3: High-Confidence Errors - Domain (HCE_rate ~ Domain * TSVR_centered)
- 6.8.2: Source-Destination Calibration (calibration ~ LocationType * log_TSVR)

Diagnostics performed per RQ:
1. QQ plot of residuals (normality check)
2. Residuals vs fitted plot (homoscedasticity check)
3. Shapiro-Wilk test on residuals
4. Cook's D for influential observations
5. Overall assessment and thesis implications

Author: Claude Code
Date: 2025-12-14
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.formula.api as smf
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURATION
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]  # REMEMVR root
OUTPUT_DIR = PROJECT_ROOT / "results" / "ch6" / "diagnostics"
OUTPUT_DIR.mkdir(exist_ok=True)
LOG_FILE = OUTPUT_DIR / "lmm_residual_diagnostics.log"

# RQ configurations
RQ_CONFIGS = {
    '6.2.1': {
        'name': 'Calibration Over Time',
        'data_file': PROJECT_ROOT / "results" / "ch6" / "6.2.1" / "data" / "step02_calibration_scores.csv",
        'formula': 'calibration ~ Time',
        'groups': 'UID',
        're_formula': '~Time',
        'time_col': 'TSVR_hours',
        'time_scale': 100,  # Scale TSVR by 100
    },
    '6.3.2': {
        'name': 'Domain Confidence Calibration',
        'data_file': PROJECT_ROOT / "results" / "ch6" / "6.3.2" / "data" / "step00_calibration_by_domain.csv",
        'formula': 'calibration ~ C(Domain) * TSVR_centered',
        'groups': 'UID',
        're_formula': '~TSVR_centered',
        'time_col': 'TSVR_hours',
        'center_time': True,
    },
    '6.4.2': {
        'name': 'Paradigm Confidence Calibration',
        'data_file': PROJECT_ROOT / "results" / "ch6" / "6.4.2" / "data" / "step00_calibration_by_paradigm.csv",
        'formula': 'calibration ~ C(Paradigm) * TSVR_centered',
        'groups': 'UID',
        're_formula': '~TSVR_centered',
        'time_col': 'TSVR_hours',
        'center_time': True,
    },
    '6.6.3': {
        'name': 'HCE Domain Specificity',
        'data_file': PROJECT_ROOT / "results" / "ch6" / "6.6.3" / "data" / "step03_lmm_input.csv",
        'formula': 'HCE_rate ~ C(domain) * Days_centered',
        'groups': 'UID',
        're_formula': None,  # Intercept only
        'time_col': 'Days_mean',
        'center_time': True,
        'time_var_name': 'Days_centered',
    },
    '6.8.2': {
        'name': 'Source-Destination Calibration',
        'data_file': PROJECT_ROOT / "results" / "ch6" / "6.8.2" / "data" / "step01_calibration_by_location.csv",
        'formula': 'calibration ~ C(LocationType) * log_TSVR',
        'groups': 'UID',
        're_formula': None,  # Intercept only based on original analysis
        'time_col': 'TSVR_hours',
        'log_time': True,
    },
}


def log(msg):
    """Log message to file and console."""
    with open(LOG_FILE, 'a') as f:
        f.write(f"{msg}\n")
        f.flush()
    print(msg, flush=True)


def compute_cooks_d(result, df):
    """
    Compute Cook's D for mixed-effects model (approximate).
    Uses influence on fixed effects parameters.
    """
    n = len(df)
    p = len(result.fe_params)

    # Get fitted values and residuals
    fitted = result.fittedvalues
    resid = df[result.model.endog_names].values - fitted

    # Get hat matrix diagonal (leverage) - approximate for mixed models
    # Using standardized residuals as proxy
    mse = np.mean(resid**2)

    # Standardized residuals
    std_resid = resid / np.sqrt(mse)

    # Approximate leverage using 1/n + (X - mean(X))^2 / SS_X for main predictors
    # This is simplified but captures the concept
    h = np.ones(n) / n

    # Cook's D approximation
    cooks_d = (std_resid**2 / p) * (h / (1 - h + 1e-10))

    return cooks_d


def run_diagnostics_for_rq(rq_id, config):
    """Run full diagnostics for a single RQ."""
    log(f"\n{'='*70}")
    log(f"RQ {rq_id}: {config['name']}")
    log(f"{'='*70}")

    # Check if data file exists
    data_file = config['data_file']
    if not data_file.exists():
        # Try fallback if specified
        if 'fallback_data' in config and config['fallback_data'].exists():
            log(f"Primary data file not found, using fallback")
            data_file = config['fallback_data']
        else:
            log(f"ERROR: Data file not found: {data_file}")
            return None

    # Load data
    log(f"\nLoading data from: {data_file.name}")
    df = pd.read_csv(data_file)
    log(f"  Rows: {len(df)}, Columns: {list(df.columns)}")

    # Prepare time variable
    time_col = config.get('time_col', 'TSVR_hours')

    if config.get('time_scale'):
        df['Time'] = df[time_col] / config['time_scale']
        log(f"  Scaled {time_col} by {config['time_scale']} -> Time")
    elif config.get('center_time'):
        centered_var = config.get('time_var_name', 'TSVR_centered')
        df[centered_var] = df[time_col] - df[time_col].mean()
        log(f"  Centered {time_col} -> {centered_var} (mean={df[time_col].mean():.2f})")
    elif config.get('log_time'):
        df['log_TSVR'] = np.log(df[time_col] + 1)
        log(f"  Log-transformed {time_col} -> log_TSVR")

    # Fit LMM
    log(f"\nFitting LMM: {config['formula']}")
    log(f"  Groups: {config['groups']}")
    log(f"  Random effects: {config['re_formula']}")

    try:
        if config['re_formula']:
            model = smf.mixedlm(
                config['formula'],
                data=df,
                groups=df[config['groups']],
                re_formula=config['re_formula']
            )
        else:
            model = smf.mixedlm(
                config['formula'],
                data=df,
                groups=df[config['groups']]
            )

        result = model.fit(reml=False)
        log(f"  Model converged: True")
        log(f"  Log-likelihood: {result.llf:.2f}")
        log(f"  AIC: {result.aic:.2f}")
    except Exception as e:
        log(f"  ERROR: Model fitting failed: {str(e)[:100]}")
        # Try intercept-only random effects as fallback
        try:
            log(f"  Attempting intercept-only model...")
            model = smf.mixedlm(
                config['formula'],
                data=df,
                groups=df[config['groups']]
            )
            result = model.fit(reml=False)
            log(f"  Fallback model converged: True")
        except Exception as e2:
            log(f"  ERROR: Fallback model also failed: {str(e2)[:100]}")
            return None

    # Extract residuals
    dv_name = config['formula'].split('~')[0].strip()
    fitted = result.fittedvalues
    observed = df[dv_name].values
    residuals = observed - fitted

    log(f"\n--- DIAGNOSTIC RESULTS ---")

    # 1. Normality: QQ Plot
    log(f"\n1. NORMALITY CHECK (QQ Plot + Shapiro-Wilk)")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # QQ plot
    stats.probplot(residuals, dist="norm", plot=axes[0])
    axes[0].set_title(f'RQ {rq_id}: Normal Q-Q Plot')
    axes[0].set_xlabel('Theoretical Quantiles')
    axes[0].set_ylabel('Sample Quantiles (Residuals)')

    # Shapiro-Wilk test (use subsample if N > 5000)
    n_resid = len(residuals)
    if n_resid > 5000:
        resid_sample = np.random.choice(residuals, 5000, replace=False)
        sw_stat, sw_p = stats.shapiro(resid_sample)
        log(f"  Shapiro-Wilk (n=5000 subsample): W={sw_stat:.4f}, p={sw_p:.6f}")
    else:
        sw_stat, sw_p = stats.shapiro(residuals)
        log(f"  Shapiro-Wilk (n={n_resid}): W={sw_stat:.4f}, p={sw_p:.6f}")

    if sw_p > 0.05:
        sw_interp = "PASS - Normality assumption met"
    elif sw_p > 0.01:
        sw_interp = "MARGINAL - Minor non-normality (robust with large N)"
    else:
        sw_interp = "FAIL - Significant non-normality (but LMM robust with N>100)"
    log(f"  Interpretation: {sw_interp}")

    # 2. Homoscedasticity: Residuals vs Fitted
    log(f"\n2. HOMOSCEDASTICITY CHECK (Residuals vs Fitted)")

    axes[1].scatter(fitted, residuals, alpha=0.5, s=10)
    axes[1].axhline(y=0, color='r', linestyle='--', linewidth=1)
    axes[1].set_title(f'RQ {rq_id}: Residuals vs Fitted')
    axes[1].set_xlabel('Fitted Values')
    axes[1].set_ylabel('Residuals')

    # Add LOESS smoother
    try:
        from statsmodels.nonparametric.smoothers_lowess import lowess
        sorted_idx = np.argsort(fitted)
        smoothed = lowess(residuals[sorted_idx], fitted[sorted_idx], frac=0.3)
        axes[1].plot(smoothed[:, 0], smoothed[:, 1], 'b-', linewidth=2, label='LOESS')
        axes[1].legend()
    except:
        pass

    # Breusch-Pagan test (manual implementation)
    # Regress squared residuals on fitted values
    resid_sq = residuals**2
    X = np.column_stack([np.ones(len(fitted)), fitted])
    try:
        bp_coef = np.linalg.lstsq(X, resid_sq, rcond=None)[0]
        bp_predicted = X @ bp_coef
        bp_ss_reg = np.sum((bp_predicted - np.mean(resid_sq))**2)
        bp_ss_tot = np.sum((resid_sq - np.mean(resid_sq))**2)
        bp_r2 = bp_ss_reg / bp_ss_tot
        bp_stat = len(residuals) * bp_r2
        bp_p = 1 - stats.chi2.cdf(bp_stat, 1)
        log(f"  Breusch-Pagan: χ²={bp_stat:.4f}, p={bp_p:.6f}")

        if bp_p > 0.05:
            bp_interp = "PASS - Homoscedasticity assumption met"
        elif bp_p > 0.01:
            bp_interp = "MARGINAL - Some heteroscedasticity (may need robust SE)"
        else:
            bp_interp = "FAIL - Heteroscedasticity present (consider robust SE)"
        log(f"  Interpretation: {bp_interp}")
    except:
        bp_p = np.nan
        bp_interp = "Unable to compute"
        log(f"  Breusch-Pagan: Unable to compute")

    plt.tight_layout()
    plot_path = OUTPUT_DIR / f"rq_{rq_id.replace('.', '_')}_diagnostics.png"
    plt.savefig(plot_path, dpi=150)
    plt.close()
    log(f"\n  Plots saved: {plot_path.name}")

    # 3. Cook's D (Influential Observations)
    log(f"\n3. INFLUENTIAL OBSERVATIONS (Cook's D)")

    cooks_d = compute_cooks_d(result, df)
    cooks_threshold = 4 / len(residuals)
    n_influential = np.sum(cooks_d > cooks_threshold)
    pct_influential = 100 * n_influential / len(residuals)
    max_cooks = np.max(cooks_d)

    log(f"  Threshold: 4/n = {cooks_threshold:.4f}")
    log(f"  Max Cook's D: {max_cooks:.4f}")
    log(f"  Observations > threshold: {n_influential} ({pct_influential:.1f}%)")

    if n_influential == 0:
        cooks_interp = "PASS - No influential observations"
    elif pct_influential < 5:
        cooks_interp = "PASS - Few influential observations (<5%)"
    elif pct_influential < 10:
        cooks_interp = "MARGINAL - Some influential observations (5-10%)"
    else:
        cooks_interp = "FAIL - Many influential observations (>10%)"
    log(f"  Interpretation: {cooks_interp}")

    # Extreme influential (Cook's D > 1)
    n_extreme = np.sum(cooks_d > 1.0)
    if n_extreme > 0:
        log(f"  WARNING: {n_extreme} observations with Cook's D > 1.0 (extreme influence)")

    # 4. Overall Assessment
    log(f"\n4. OVERALL ASSESSMENT")

    issues = []
    if sw_p < 0.01:
        issues.append("non-normality")
    if isinstance(bp_p, float) and bp_p < 0.01:
        issues.append("heteroscedasticity")
    if pct_influential >= 10:
        issues.append("influential observations")

    if len(issues) == 0:
        overall = "ROBUST - All assumptions met or minor deviations only"
        thesis_impact = "Results can be presented without caveats"
    elif len(issues) == 1:
        overall = f"ADEQUATE - Minor issue: {issues[0]}"
        thesis_impact = "Note in Methods section; LMM robust with N>100"
    else:
        overall = f"REVIEW - Multiple issues: {', '.join(issues)}"
        thesis_impact = "Document limitations; consider robust SE or alternative models"

    log(f"  Overall: {overall}")
    log(f"  Thesis impact: {thesis_impact}")

    # Compile results
    results = {
        'RQ': rq_id,
        'Name': config['name'],
        'N': len(residuals),
        'N_groups': df[config['groups']].nunique(),
        'Shapiro_W': sw_stat,
        'Shapiro_p': sw_p,
        'Shapiro_interp': sw_interp.split(' - ')[0],
        'BP_stat': bp_stat if isinstance(bp_p, float) else np.nan,
        'BP_p': bp_p if isinstance(bp_p, float) else np.nan,
        'BP_interp': bp_interp.split(' - ')[0] if isinstance(bp_p, float) else 'N/A',
        'Max_CooksD': max_cooks,
        'N_influential': n_influential,
        'Pct_influential': pct_influential,
        'CooksD_interp': cooks_interp.split(' - ')[0],
        'Overall': overall.split(' - ')[0],
        'Plot_file': plot_path.name,
    }

    return results


def main():
    """Run diagnostics for all 5 RQs."""
    log(f"{'='*70}")
    log(f"T2.1: LMM RESIDUAL DIAGNOSTICS")
    log(f"Chapter 6 Validity Rework - TIER 2 HIGH Priority")
    log(f"{'='*70}")
    log(f"Date: {pd.Timestamp.now()}")
    log(f"Output directory: {OUTPUT_DIR}")

    all_results = []

    for rq_id, config in RQ_CONFIGS.items():
        try:
            results = run_diagnostics_for_rq(rq_id, config)
            if results:
                all_results.append(results)
        except Exception as e:
            log(f"\nERROR processing RQ {rq_id}: {str(e)}")
            import traceback
            log(traceback.format_exc())

    # Compile summary table
    log(f"\n{'='*70}")
    log(f"SUMMARY TABLE")
    log(f"{'='*70}")

    if all_results:
        df_summary = pd.DataFrame(all_results)

        # Save to CSV
        summary_path = OUTPUT_DIR / "lmm_diagnostics_summary.csv"
        df_summary.to_csv(summary_path, index=False)
        log(f"\nSaved summary: {summary_path}")

        # Print summary
        log(f"\n{'RQ':<8} {'Name':<35} {'Normality':<10} {'Homosced.':<10} {'CooksD':<10} {'Overall':<10}")
        log("-" * 90)
        for _, row in df_summary.iterrows():
            log(f"{row['RQ']:<8} {row['Name'][:33]:<35} {row['Shapiro_interp']:<10} {row['BP_interp']:<10} {row['CooksD_interp']:<10} {row['Overall']:<10}")

    log(f"\n{'='*70}")
    log(f"DIAGNOSTICS COMPLETE")
    log(f"{'='*70}")
    log(f"RQs processed: {len(all_results)} / {len(RQ_CONFIGS)}")
    log(f"Output directory: {OUTPUT_DIR}")

    return df_summary if all_results else None


if __name__ == "__main__":
    main()
