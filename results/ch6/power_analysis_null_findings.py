"""
RQ 6.X - Post-Hoc Power Analysis for NULL Findings

PURPOSE:
For RQs that reported NULL findings (p > 0.05), compute post-hoc power to distinguish:
- "Well-powered null" (evidence of no effect)
- "Underpowered study" (absence of evidence, not evidence of absence)

NULL RQs to analyze:
- 6.1.3, 6.2.5, 6.3.3, 6.4.3, 6.5.2, 6.5.3, 6.7.3, 6.8.2

METHODOLOGY:
1. For each NULL RQ, compute power for detecting:
   - d = 0.20 (small effect)
   - d = 0.30 (medium effect)
   - d = 0.50 (large effect)
2. Compute minimum detectable effect size (MDES) at 80% power
3. Classify findings

CLASSIFICATION:
- Well-powered null (power ≥ 0.80 for d=0.20): Can claim "evidence of no meaningful effect"
- Adequately powered null (power ≥ 0.80 for d=0.30): Can claim "no medium/large effect"
- Underpowered (power < 0.50 for d=0.30): Absence of evidence, not evidence of absence

Author: Claude Code
Date: 2025-12-14
Task: T2.2 from rq_rework.md
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Setup paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

LOG_FILE = OUTPUT_DIR / "power_analysis_null_findings.log"

# Clear log file
with open(LOG_FILE, 'w') as f:
    f.write("")

def log(msg):
    """Log message to file and stdout with flush"""
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{msg}\n")
        f.flush()
    print(msg, flush=True)


def compute_power_ttest(n, d, alpha=0.05, two_tailed=True):
    """
    Compute power for one-sample t-test (or paired t-test equivalent).

    For repeated measures (within-subject) designs, this is approximately
    correct when comparing change scores or testing against zero.

    Parameters:
    - n: sample size
    - d: Cohen's d (standardized effect size)
    - alpha: significance level
    - two_tailed: whether test is two-tailed
    """
    # Non-centrality parameter
    ncp = d * np.sqrt(n)

    # Critical t-value
    if two_tailed:
        t_crit = stats.t.ppf(1 - alpha/2, df=n-1)
    else:
        t_crit = stats.t.ppf(1 - alpha, df=n-1)

    # Power = P(T > t_crit | H1 is true)
    # Under H1, T follows non-central t distribution with ncp = d*sqrt(n)
    power = 1 - stats.nct.cdf(t_crit, df=n-1, nc=ncp)

    if two_tailed:
        # Add power from lower tail
        power += stats.nct.cdf(-t_crit, df=n-1, nc=ncp)

    return power


def compute_power_lmm(n_subjects, n_timepoints, d, alpha=0.05, rho=0.5):
    """
    Approximate power for LMM with repeated measures.

    For a simple random intercept model, effective N ≈ N_subjects * (1 + (n-1)*rho) / n
    where rho is the ICC (intra-class correlation).

    This is a conservative approximation.

    Parameters:
    - n_subjects: number of participants
    - n_timepoints: number of repeated measurements
    - d: Cohen's d
    - alpha: significance level
    - rho: ICC (default 0.5 for typical cognitive data)
    """
    # Design effect for repeated measures
    design_effect = 1 + (n_timepoints - 1) * rho

    # Effective sample size (adjusted for clustering)
    n_eff = n_subjects * n_timepoints / design_effect

    # Use effective N for power calculation
    ncp = d * np.sqrt(n_eff)

    # Critical z-value (normal approximation for large N)
    z_crit = stats.norm.ppf(1 - alpha/2)

    # Power
    power = 1 - stats.norm.cdf(z_crit - ncp) + stats.norm.cdf(-z_crit - ncp)

    return power


def compute_mdes(n, alpha=0.05, power_target=0.80, two_tailed=True):
    """
    Compute minimum detectable effect size (MDES) for given N and power.

    Uses binary search to find d such that power(d) = power_target.
    """
    from scipy.optimize import brentq

    def power_diff(d):
        return compute_power_ttest(n, d, alpha, two_tailed) - power_target

    # Find d in range [0.01, 2.0]
    try:
        mdes = brentq(power_diff, 0.01, 2.0)
    except ValueError:
        mdes = np.nan

    return mdes


def main():
    log("=" * 80)
    log("Post-Hoc Power Analysis for NULL Findings (Chapter 6)")
    log(f"Started: {datetime.now().isoformat()}")
    log("=" * 80)

    # =========================================================================
    # Define NULL RQs and their parameters
    # =========================================================================
    log("\n[STEP 1] Define NULL RQs")
    log("-" * 60)

    # NULL RQs with their observed effect sizes (from summaries)
    # Format: RQ, N_subjects, N_timepoints, observed_d, test_type, description
    null_rqs = [
        {'rq': '6.1.3', 'n': 100, 'timepoints': 4, 'observed_d': 0.05, 'test': 'lmm',
         'description': 'Time interaction effect (confidence trajectory stability)'},
        {'rq': '6.2.5', 'n': 100, 'timepoints': 4, 'observed_d': 0.08, 'test': 'lmm',
         'description': 'ECE change over time'},
        {'rq': '6.3.3', 'n': 100, 'timepoints': 4, 'observed_d': 0.04, 'test': 'lmm',
         'description': 'Domain × Time interaction on calibration'},
        {'rq': '6.4.3', 'n': 100, 'timepoints': 4, 'observed_d': 0.06, 'test': 'lmm',
         'description': 'Paradigm × Time interaction on calibration'},
        {'rq': '6.5.2', 'n': 100, 'timepoints': 4, 'observed_d': 0.07, 'test': 'lmm',
         'description': 'Confidence-accuracy correlation × Time'},
        {'rq': '6.5.3', 'n': 100, 'timepoints': 4, 'observed_d': 0.03, 'test': 'lmm',
         'description': 'C-A correlation domain specificity'},
        {'rq': '6.7.3', 'n': 100, 'timepoints': 1, 'observed_d': 0.15, 'test': 'ttest',
         'description': 'Variability predicts forgetting (person-level)'},
        {'rq': '6.8.2', 'n': 100, 'timepoints': 4, 'observed_d': 0.05, 'test': 'lmm',
         'description': 'Calibration trajectory group differences'},
    ]

    log(f"  Found {len(null_rqs)} NULL RQs to analyze")

    # =========================================================================
    # Compute Power for Each NULL RQ
    # =========================================================================
    log("\n[STEP 2] Compute Power for Each NULL RQ")
    log("-" * 60)

    results = []

    for rq in null_rqs:
        log(f"\n  RQ {rq['rq']}: {rq['description']}")
        log(f"    N = {rq['n']}, Timepoints = {rq['timepoints']}, Observed d = {rq['observed_d']:.2f}")

        # Compute power for different effect sizes
        if rq['test'] == 'ttest':
            power_d20 = compute_power_ttest(rq['n'], 0.20)
            power_d30 = compute_power_ttest(rq['n'], 0.30)
            power_d50 = compute_power_ttest(rq['n'], 0.50)
            mdes = compute_mdes(rq['n'])
        else:  # LMM
            power_d20 = compute_power_lmm(rq['n'], rq['timepoints'], 0.20)
            power_d30 = compute_power_lmm(rq['n'], rq['timepoints'], 0.30)
            power_d50 = compute_power_lmm(rq['n'], rq['timepoints'], 0.50)
            # MDES for LMM (approximate using effective N)
            n_eff = rq['n'] * rq['timepoints'] / (1 + (rq['timepoints'] - 1) * 0.5)
            mdes = compute_mdes(int(n_eff))

        log(f"    Power for d=0.20: {power_d20:.2%}")
        log(f"    Power for d=0.30: {power_d30:.2%}")
        log(f"    Power for d=0.50: {power_d50:.2%}")
        log(f"    MDES (80% power): d = {mdes:.3f}")

        # Classify
        if power_d20 >= 0.80:
            classification = "WELL-POWERED NULL"
            interpretation = "Evidence supports no meaningful effect (d < 0.20)"
        elif power_d30 >= 0.80:
            classification = "ADEQUATELY POWERED NULL"
            interpretation = "Evidence supports no medium/large effect (d < 0.30)"
        elif power_d30 >= 0.50:
            classification = "MARGINALLY POWERED"
            interpretation = "Inconclusive - could not detect medium effect reliably"
        else:
            classification = "UNDERPOWERED"
            interpretation = "Absence of evidence, not evidence of absence"

        log(f"    Classification: {classification}")
        log(f"    {interpretation}")

        results.append({
            'rq': rq['rq'],
            'description': rq['description'],
            'n_subjects': rq['n'],
            'n_timepoints': rq['timepoints'],
            'test_type': rq['test'],
            'observed_d': rq['observed_d'],
            'power_d020': power_d20,
            'power_d030': power_d30,
            'power_d050': power_d50,
            'mdes_80pct': mdes,
            'classification': classification,
            'interpretation': interpretation
        })

    # =========================================================================
    # Save Results
    # =========================================================================
    log("\n[STEP 3] Save Results")
    log("-" * 60)

    results_df = pd.DataFrame(results)
    output_path = OUTPUT_DIR / "power_analysis_null_findings.csv"
    results_df.to_csv(output_path, index=False)
    log(f"  ✓ Saved: {output_path}")

    # =========================================================================
    # Summary Statistics
    # =========================================================================
    log("\n" + "=" * 80)
    log("[SUMMARY] Power Analysis Results")
    log("=" * 80)

    n_well = sum(1 for r in results if r['classification'] == 'WELL-POWERED NULL')
    n_adequate = sum(1 for r in results if r['classification'] == 'ADEQUATELY POWERED NULL')
    n_marginal = sum(1 for r in results if r['classification'] == 'MARGINALLY POWERED')
    n_under = sum(1 for r in results if r['classification'] == 'UNDERPOWERED')

    log(f"\n  Classification Summary:")
    log(f"    Well-powered nulls: {n_well}/{len(results)}")
    log(f"    Adequately powered nulls: {n_adequate}/{len(results)}")
    log(f"    Marginally powered: {n_marginal}/{len(results)}")
    log(f"    Underpowered: {n_under}/{len(results)}")

    log(f"\n  Thesis Implications:")
    if n_well + n_adequate >= len(results) * 0.75:
        log(f"    Most NULL findings are well-powered - can claim genuine null effects")
    elif n_under >= len(results) * 0.5:
        log(f"    Many NULL findings are underpowered - caution in interpretation")
    else:
        log(f"    Mixed power - interpret each NULL finding individually")

    # Summary table
    log(f"\n  Power Summary Table:")
    log(f"  {'RQ':<8} {'Observed d':>10} {'Power d=0.20':>12} {'Power d=0.30':>12} {'MDES':>8} {'Classification':>25}")
    log(f"  {'-'*85}")
    for r in results:
        log(f"  {r['rq']:<8} {r['observed_d']:>10.2f} {r['power_d020']:>12.1%} {r['power_d030']:>12.1%} {r['mdes_80pct']:>8.3f} {r['classification']:>25}")

    log(f"\nCompleted: {datetime.now().isoformat()}")

    return results_df


if __name__ == "__main__":
    try:
        results = main()
    except Exception as e:
        log(f"\n[ERROR] {e}")
        import traceback
        log(traceback.format_exc())
        raise
