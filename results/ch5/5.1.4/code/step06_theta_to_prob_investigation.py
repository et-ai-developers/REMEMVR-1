#!/usr/bin/env python3
"""
Theta-to-Probability Scale Investigation for ICC Anomaly

PURPOSE:
Test whether the anomalously low ICC_slope (0.0005) is an artifact of analyzing
forgetting on the IRT theta scale rather than the probability scale.

HYPOTHESIS:
- Literature uses proportion correct (bounded 0-1) for ICC computation
- We use IRT theta (unbounded, -3 to +3)
- Nonlinear logit transformation may compress individual differences
- Converting theta → probability may reveal higher ICC_slope

METHOD:
1. Load theta scores and item parameters
2. Convert theta → probability via:
   a. Simple inverse logit (approximate)
   b. Test Characteristic Curve using item parameters (proper)
3. Merge with TSVR time variable
4. Fit LMM on probability scale (same model structure as theta analysis)
5. Extract variance components
6. Compute ICC_slope and ICC_intercept on probability scale
7. Compare with theta-scale results

TARGET: RQ 5.1.4 (Between-Person Variance in Forgetting)
"""

import sys
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(PROJECT_ROOT))

# =============================================================================
# Configuration
# =============================================================================
RQ_DIR = Path(__file__).resolve().parents[1]
LOG_FILE = RQ_DIR / "logs" / "step06_theta_to_prob.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# Input files from RQ 5.1.1
THETA_SCORES = RQ_DIR / "../5.1.1/data/step03_theta_scores.csv"
LMM_INPUT = RQ_DIR / "../5.1.1/data/step04_lmm_input.csv"
ITEM_PARAMS = RQ_DIR / "../5.1.1/logs/step01_item_parameters.csv"
PURIFIED_ITEMS = RQ_DIR / "../5.1.1/data/step02_purified_items.csv"

# Output files
PROB_TRAJECTORIES = RQ_DIR / "data" / "step06_probability_trajectories.csv"
PROB_LMM_INPUT = RQ_DIR / "data" / "step07_prob_lmm_input.csv"
PROB_VARIANCE = RQ_DIR / "data" / "step08_prob_variance_components.csv"
PROB_ICC = RQ_DIR / "data" / "step09_prob_icc_estimates.csv"
SCALE_COMPARISON = RQ_DIR / "results" / "step10_scale_comparison.md"

# Theta-scale results (from existing analysis)
THETA_VARIANCE = RQ_DIR / "data" / "step02_variance_components.csv"
THETA_ICC = RQ_DIR / "data" / "step03_icc_estimates.csv"


def log(msg: str) -> None:
    """Write message to console and log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
    print(formatted_msg)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(formatted_msg + "\n")


def simple_inverse_logit(theta: float) -> float:
    """Simple inverse logit transformation: P = 1 / (1 + exp(-theta))"""
    return 1 / (1 + np.exp(-theta))


def compute_tcc(theta: float, a_values: np.ndarray, b_values: np.ndarray) -> float:
    """
    Compute expected proportion correct via Test Characteristic Curve.

    Uses 2PL IRT model: P(correct) = 1 / (1 + exp(-a*(theta - b)))
    Returns average across all items.

    Args:
        theta: Person ability estimate
        a_values: Item discrimination parameters (array)
        b_values: Item difficulty parameters (array)

    Returns:
        Expected proportion correct (0-1)
    """
    probs = 1 / (1 + np.exp(-a_values * (theta - b_values)))
    return probs.mean()


if __name__ == "__main__":
    try:
        log("=" * 70)
        log("THETA-TO-PROBABILITY SCALE INVESTIGATION")
        log("Testing ICC anomaly hypothesis")
        log("=" * 70)

        # =====================================================================
        # STEP 1: Load Data
        # =====================================================================
        log("\n[STEP 1] Loading data...")

        # Load theta scores
        df_theta = pd.read_csv(THETA_SCORES)
        log(f"  Theta scores: {len(df_theta)} rows")

        # Load LMM input (has TSVR time variable)
        df_lmm = pd.read_csv(LMM_INPUT)
        log(f"  LMM input: {len(df_lmm)} rows")

        # Load item parameters (all items)
        df_items_all = pd.read_csv(ITEM_PARAMS)
        log(f"  Item parameters (all): {len(df_items_all)} items")

        # Load purified items list
        df_purified = pd.read_csv(PURIFIED_ITEMS)
        purified_items = df_purified['item_name'].tolist()
        log(f"  Purified items: {len(purified_items)} items")

        # Filter to purified items only
        df_items = df_items_all[df_items_all['item_name'].isin(purified_items)].copy()
        log(f"  Item parameters (purified): {len(df_items)} items")

        # Extract a and b values for TCC computation
        a_values = df_items['a'].values
        b_values = df_items['b'].values

        log(f"  Item parameters: a range [{a_values.min():.3f}, {a_values.max():.3f}]")
        log(f"  Item parameters: b range [{b_values.min():.3f}, {b_values.max():.3f}]")

        # =====================================================================
        # STEP 2: Convert Theta to Probability
        # =====================================================================
        log("\n[STEP 2] Converting theta to probability scale...")

        # Method A: Simple inverse logit
        df_theta['Prob_simple'] = df_theta['Theta_All'].apply(simple_inverse_logit)

        # Method B: Test Characteristic Curve
        df_theta['Prob_TCC'] = df_theta['Theta_All'].apply(
            lambda t: compute_tcc(t, a_values, b_values)
        )

        # Check distributions
        log(f"  Theta range: [{df_theta['Theta_All'].min():.3f}, {df_theta['Theta_All'].max():.3f}]")
        log(f"  Prob_simple range: [{df_theta['Prob_simple'].min():.3f}, {df_theta['Prob_simple'].max():.3f}]")
        log(f"  Prob_TCC range: [{df_theta['Prob_TCC'].min():.3f}, {df_theta['Prob_TCC'].max():.3f}]")

        # Check for boundary issues (values very close to 0 or 1)
        n_near_floor = (df_theta['Prob_TCC'] < 0.05).sum()
        n_near_ceiling = (df_theta['Prob_TCC'] > 0.95).sum()
        log(f"  Boundary check: {n_near_floor} obs near floor (<0.05), {n_near_ceiling} obs near ceiling (>0.95)")

        # Save probability trajectories
        df_theta.to_csv(PROB_TRAJECTORIES, index=False)
        log(f"  Saved: {PROB_TRAJECTORIES}")

        # =====================================================================
        # STEP 3: Merge with TSVR Time Variable
        # =====================================================================
        log("\n[STEP 3] Merging with TSVR time variable...")

        # Merge theta probabilities with LMM input (has TSVR)
        df_prob_lmm = pd.merge(
            df_theta[['UID', 'test', 'Theta_All', 'Prob_simple', 'Prob_TCC']],
            df_lmm[['UID', 'test', 'TSVR_hours', 'Days', 'log_Days_plus1']],
            on=['UID', 'test'],
            how='inner'
        )

        # Add log_TSVR (matching theta-scale analysis)
        df_prob_lmm['log_TSVR'] = np.log(df_prob_lmm['TSVR_hours'])

        log(f"  Merged data: {len(df_prob_lmm)} rows")
        log(f"  Unique UIDs: {df_prob_lmm['UID'].nunique()}")

        # Save probability LMM input
        df_prob_lmm.to_csv(PROB_LMM_INPUT, index=False)
        log(f"  Saved: {PROB_LMM_INPUT}")

        # =====================================================================
        # STEP 4: Fit LMM on Probability Scale
        # =====================================================================
        log("\n[STEP 4] Fitting LMM on probability scale...")

        import statsmodels.formula.api as smf

        # Model structure matching theta-scale analysis:
        # Lin+Log model with random intercepts and slopes on log_TSVR
        # (We use log_TSVR because theta analysis established Log model as best)

        # Note: We're testing both simple and TCC probability
        results = {}

        for prob_col in ['Prob_TCC', 'Prob_simple']:
            log(f"\n  Fitting LMM for {prob_col}...")

            try:
                # Lin+Log model: Prob ~ Days + log(Days+1)
                model = smf.mixedlm(
                    f"{prob_col} ~ Days + log_Days_plus1",
                    data=df_prob_lmm,
                    groups="UID",
                    re_formula="~log_TSVR"  # Random intercepts and slopes on log time
                )

                result = model.fit(reml=False, method='lbfgs')

                if result.converged:
                    log(f"    Converged: True")

                    # Extract variance components from cov_re
                    cov_re = result.cov_re
                    log(f"    Random effects covariance matrix:\n{cov_re}")

                    # Variance components
                    var_intercept = cov_re.iloc[0, 0]  # Group Var
                    var_slope = cov_re.iloc[1, 1]  # log_TSVR Var
                    cov_int_slope = cov_re.iloc[0, 1]  # Covariance
                    var_residual = result.scale  # Residual variance

                    # Correlation between intercept and slope
                    if var_intercept > 0 and var_slope > 0:
                        cor_int_slope = cov_int_slope / np.sqrt(var_intercept * var_slope)
                    else:
                        cor_int_slope = np.nan

                    results[prob_col] = {
                        'var_intercept': var_intercept,
                        'var_slope': var_slope,
                        'cov_int_slope': cov_int_slope,
                        'var_residual': var_residual,
                        'cor_int_slope': cor_int_slope,
                        'converged': True,
                        'aic': result.aic,
                        'bic': result.bic
                    }

                    log(f"    var_intercept: {var_intercept:.6f}")
                    log(f"    var_slope: {var_slope:.6f}")
                    log(f"    cov_int_slope: {cov_int_slope:.6f}")
                    log(f"    var_residual: {var_residual:.6f}")
                    log(f"    cor_int_slope: {cor_int_slope:.4f}")

                else:
                    log(f"    WARNING: Model did not converge")
                    results[prob_col] = {'converged': False}

            except Exception as e:
                log(f"    ERROR: {str(e)}")
                results[prob_col] = {'converged': False, 'error': str(e)}

        # =====================================================================
        # STEP 5: Extract Variance Components
        # =====================================================================
        log("\n[STEP 5] Saving variance components...")

        # Save probability-scale variance components
        variance_rows = []
        for prob_col, res in results.items():
            if res.get('converged'):
                variance_rows.append({
                    'scale': prob_col,
                    'var_intercept': res['var_intercept'],
                    'var_slope': res['var_slope'],
                    'cov_int_slope': res['cov_int_slope'],
                    'var_residual': res['var_residual'],
                    'cor_int_slope': res['cor_int_slope']
                })

        df_prob_var = pd.DataFrame(variance_rows)
        df_prob_var.to_csv(PROB_VARIANCE, index=False)
        log(f"  Saved: {PROB_VARIANCE}")

        # =====================================================================
        # STEP 6: Compute ICC on Probability Scale
        # =====================================================================
        log("\n[STEP 6] Computing ICC on probability scale...")

        icc_rows = []
        for prob_col, res in results.items():
            if res.get('converged'):
                var_int = res['var_intercept']
                var_slope = res['var_slope']
                var_resid = res['var_residual']

                # ICC formulas
                icc_intercept = var_int / (var_int + var_resid)
                icc_slope_simple = var_slope / (var_slope + var_resid)

                icc_rows.append({
                    'scale': prob_col,
                    'icc_intercept': icc_intercept,
                    'icc_slope_simple': icc_slope_simple
                })

                log(f"  {prob_col}:")
                log(f"    ICC_intercept: {icc_intercept:.4f}")
                log(f"    ICC_slope: {icc_slope_simple:.6f}")

        df_prob_icc = pd.DataFrame(icc_rows)
        df_prob_icc.to_csv(PROB_ICC, index=False)
        log(f"  Saved: {PROB_ICC}")

        # =====================================================================
        # STEP 7: Compare with Theta-Scale Results
        # =====================================================================
        log("\n[STEP 7] Comparing with theta-scale results...")

        # Load theta-scale results
        df_theta_var = pd.read_csv(THETA_VARIANCE)
        df_theta_icc = pd.read_csv(THETA_ICC)

        # Get theta-scale values
        theta_var_int = df_theta_var[df_theta_var['component'] == 'var_intercept']['estimate'].values[0]
        theta_var_slope = df_theta_var[df_theta_var['component'] == 'var_slope']['estimate'].values[0]
        theta_var_resid = df_theta_var[df_theta_var['component'] == 'var_residual']['estimate'].values[0]
        theta_cor = df_theta_var[df_theta_var['component'] == 'cor_int_slope']['estimate'].values[0]

        theta_icc_int = df_theta_icc[df_theta_icc['icc_type'] == 'intercept']['icc_value'].values[0]
        theta_icc_slope = df_theta_icc[df_theta_icc['icc_type'] == 'slope_simple']['icc_value'].values[0]

        # Get probability-scale values (TCC method)
        if 'Prob_TCC' in results and results['Prob_TCC'].get('converged'):
            prob_res = results['Prob_TCC']
            prob_var_int = prob_res['var_intercept']
            prob_var_slope = prob_res['var_slope']
            prob_var_resid = prob_res['var_residual']
            prob_cor = prob_res['cor_int_slope']
            prob_icc_int = prob_var_int / (prob_var_int + prob_var_resid)
            prob_icc_slope = prob_var_slope / (prob_var_slope + prob_var_resid)
        else:
            prob_var_int = prob_var_slope = prob_var_resid = prob_cor = prob_icc_int = prob_icc_slope = np.nan

        # Create comparison table
        comparison_md = f"""# Scale Comparison: Theta vs Probability

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

## Purpose

Test whether the anomalously low ICC_slope (0.0005) is an artifact of the IRT theta scale.

## Results

### Variance Components

| Component | Theta Scale | Probability Scale (TCC) | Ratio (Prob/Theta) |
|-----------|------------|------------------------|-------------------|
| var_intercept | {theta_var_int:.6f} | {prob_var_int:.6f} | {prob_var_int/theta_var_int:.2f}× |
| var_slope | {theta_var_slope:.6f} | {prob_var_slope:.6f} | {prob_var_slope/theta_var_slope:.2f}× |
| var_residual | {theta_var_resid:.6f} | {prob_var_resid:.6f} | {prob_var_resid/theta_var_resid:.2f}× |
| cor_int_slope | {theta_cor:.4f} | {prob_cor:.4f} | - |

### ICC Estimates

| Metric | Theta Scale | Probability Scale (TCC) | Ratio | Literature |
|--------|------------|------------------------|-------|------------|
| ICC_intercept | {theta_icc_int:.4f} | {prob_icc_int:.4f} | {prob_icc_int/theta_icc_int:.2f}× | 0.60-0.80 |
| ICC_slope | {theta_icc_slope:.6f} | {prob_icc_slope:.6f} | {prob_icc_slope/theta_icc_slope:.1f}× | 0.30-0.50 |

## Interpretation

"""
        # Add interpretation based on results
        if prob_icc_slope > 0.10:
            interpretation = f"""### STRONG SUPPORT for Scale Hypothesis

ICC_slope on probability scale ({prob_icc_slope:.4f}) is {prob_icc_slope/theta_icc_slope:.0f}× higher than theta scale ({theta_icc_slope:.6f}).

**Conclusion:** The anomalously low ICC_slope WAS an artifact of the theta scale. On the probability scale,
individual differences in forgetting rates are now detectable and closer to literature values.

**Methodological Contribution:** IRT theta-scale analyses produce fundamentally different ICC estimates
than probability-scale analyses. When comparing to literature (which uses proportion correct),
probability-scale ICC should be reported.
"""
        elif prob_icc_slope > 0.01:
            interpretation = f"""### PARTIAL SUPPORT for Scale Hypothesis

ICC_slope on probability scale ({prob_icc_slope:.4f}) is {prob_icc_slope/theta_icc_slope:.0f}× higher than theta scale ({theta_icc_slope:.6f}),
but still below literature norms (0.30-0.50).

**Conclusion:** Scale transformation partially explains the anomaly but doesn't fully resolve it.
Other factors (short retention interval, sample characteristics) may also contribute.
"""
        else:
            interpretation = f"""### NO SUPPORT for Scale Hypothesis

ICC_slope on probability scale ({prob_icc_slope:.6f}) remains similar to theta scale ({theta_icc_slope:.6f}).

**Conclusion:** The low ICC_slope is a REAL finding, not a scale artifact.
VR episodic memory may genuinely show homogeneous forgetting rates across individuals.
"""

        comparison_md += interpretation

        comparison_md += f"""
## Technical Details

### Model Specification
- Formula: Prob_TCC ~ Days + log(Days+1)
- Random effects: ~log_TSVR (intercepts and slopes on log time)
- Method: ML estimation via LBFGS

### Data
- Observations: {len(df_prob_lmm)}
- Participants: {df_prob_lmm['UID'].nunique()}
- Purified items for TCC: {len(purified_items)}

### Boundary Check
- Near floor (<0.05): {n_near_floor} observations
- Near ceiling (>0.95): {n_near_ceiling} observations
"""

        # Save comparison report
        with open(SCALE_COMPARISON, 'w') as f:
            f.write(comparison_md)
        log(f"\n  Saved: {SCALE_COMPARISON}")

        # Print key results
        log("\n" + "=" * 70)
        log("KEY RESULTS")
        log("=" * 70)
        log(f"  Theta ICC_slope:       {theta_icc_slope:.6f}")
        log(f"  Probability ICC_slope: {prob_icc_slope:.6f}")
        log(f"  Ratio (Prob/Theta):    {prob_icc_slope/theta_icc_slope:.1f}×")
        log(f"  Literature norm:       0.30-0.50")

        if prob_icc_slope > 0.10:
            log("\n  VERDICT: STRONG SUPPORT for scale hypothesis")
        elif prob_icc_slope > 0.01:
            log("\n  VERDICT: PARTIAL SUPPORT for scale hypothesis")
        else:
            log("\n  VERDICT: NO SUPPORT - finding is real, not artifact")

        log("\n" + "=" * 70)
        log("INVESTIGATION COMPLETE")
        log("=" * 70)

        sys.exit(0)

    except Exception as e:
        log(f"[ERROR] {str(e)}")
        import traceback
        log(traceback.format_exc())
        sys.exit(1)
