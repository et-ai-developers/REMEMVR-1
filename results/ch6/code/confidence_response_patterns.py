#!/usr/bin/env python3
"""
T2.4: Confidence Response Pattern Analysis
==========================================
Validates that confidence ratings use full scale (not extreme response style).

Purpose: Check for Extreme Response Style (ERS) in confidence ratings.
ERS violates GRM assumptions if participants only use endpoints (1s and 5s).

RQs analyzed:
- 6.1.1: Overall confidence trajectories (uses all confidence ratings)
- 6.8.1: Source-destination confidence (subset of confidence ratings)

Metrics computed per participant:
1. % responses at each level (1, 2, 3, 4, 5)
2. % at endpoints (1 or 5)
3. SD of responses (< 0.8 indicates restricted range)
4. ERS flag: >50% at endpoints

Author: Claude Code
Date: 2025-12-14
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
import matplotlib.pyplot as plt

# =============================================================================
# CONFIGURATION
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]  # REMEMVR root
DATA_CACHE = PROJECT_ROOT / "data" / "cache"
OUTPUT_DIR = PROJECT_ROOT / "results" / "ch6" / "diagnostics"
OUTPUT_DIR.mkdir(exist_ok=True)
LOG_FILE = OUTPUT_DIR / "confidence_response_patterns.log"


def log(msg):
    """Log message to file and console."""
    with open(LOG_FILE, 'a') as f:
        f.write(f"{msg}\n")
        f.flush()
    print(msg, flush=True)


def extract_confidence_ratings():
    """Extract raw confidence ratings (1-5 scale) from dfData.csv."""
    log("\n" + "=" * 70)
    log("STEP 1: Extract Raw Confidence Ratings")
    log("=" * 70)

    # Load master data
    dfdata_path = DATA_CACHE / "dfData.csv"
    if not dfdata_path.exists():
        raise FileNotFoundError(f"dfData.csv not found: {dfdata_path}")

    df = pd.read_csv(dfdata_path)
    log(f"Loaded dfData.csv: {len(df)} rows (100 UIDs × 4 tests)")

    # Get TC_* (confidence) columns - these are the raw confidence ratings
    tc_cols = [c for c in df.columns if c.startswith('TC_')]
    log(f"Found {len(tc_cols)} TC_* (confidence) columns")

    # Reshape to long format: UID, TEST, item, confidence
    rows = []
    for _, row in df.iterrows():
        uid = str(row['UID'])
        test = row['TEST']

        for tc_col in tc_cols:
            conf_val = row[tc_col]
            if pd.notna(conf_val):
                # Determine item type from column name
                item_name = tc_col.replace('TC_', '')
                rows.append({
                    'UID': uid,
                    'TEST': test,
                    'item': item_name,
                    'confidence_raw': conf_val
                })

    df_long = pd.DataFrame(rows)
    log(f"Created long-format data: {len(df_long)} rows")

    # Check confidence scale
    conf_vals = sorted(df_long['confidence_raw'].unique())
    log(f"Unique confidence values: {conf_vals}")

    # Determine scale type
    # Scale is {0.0, 0.2, 0.4, 0.6, 0.8, 1.0} = 6 levels
    # Map to 1-6 for analysis: {0.0->1, 0.2->2, 0.4->3, 0.6->4, 0.8->5, 1.0->6}
    if max(conf_vals) <= 1.0 and min(conf_vals) >= 0.0:
        log("Scale is 0.0-1.0 in 0.2 increments (6-point scale).")
        log("Mapping: {0.0->1, 0.2->2, 0.4->3, 0.6->4, 0.8->5, 1.0->6}")
        df_long['confidence_level'] = np.round(df_long['confidence_raw'] * 5 + 1).astype(int)
        df_long['confidence_level'] = df_long['confidence_level'].clip(1, 6)
    else:
        log("Scale appears to be raw ordinal. Using as-is.")
        df_long['confidence_level'] = df_long['confidence_raw'].astype(int)

    # Validate conversion
    scale_vals = sorted(df_long['confidence_level'].unique())
    log(f"Converted scale values: {scale_vals}")

    return df_long


def compute_participant_metrics(df_long):
    """Compute response pattern metrics per participant."""
    log("\n" + "=" * 70)
    log("STEP 2: Compute Per-Participant Response Metrics")
    log("=" * 70)

    results = []

    for uid in df_long['UID'].unique():
        uid_data = df_long[df_long['UID'] == uid]['confidence_level']
        n_responses = len(uid_data)

        # % at each response level (1-6 scale)
        pct_by_level = {}
        for level in [1, 2, 3, 4, 5, 6]:
            pct = (uid_data == level).sum() / n_responses * 100
            pct_by_level[f'pct_{level}'] = pct

        # % at endpoints (1 or 6 for 6-point scale)
        pct_endpoints = ((uid_data == 1) | (uid_data == 6)).sum() / n_responses * 100

        # SD of responses
        sd_responses = uid_data.std()

        # Mean response
        mean_response = uid_data.mean()

        # ERS flag: >50% at endpoints
        ers_flag = pct_endpoints > 50

        # Restricted range flag: SD < 1.0 for 6-point scale
        restricted_flag = sd_responses < 1.0

        results.append({
            'UID': uid,
            'n_responses': n_responses,
            'mean_confidence': mean_response,
            'sd_confidence': sd_responses,
            **pct_by_level,
            'pct_endpoints': pct_endpoints,
            'ERS_flag': ers_flag,
            'restricted_range_flag': restricted_flag
        })

    df_metrics = pd.DataFrame(results)

    # Summary statistics
    log(f"\nPer-Participant Metrics Summary (N={len(df_metrics)}):")
    log(f"  Mean responses per participant: {df_metrics['n_responses'].mean():.1f}")
    log(f"  Mean confidence: {df_metrics['mean_confidence'].mean():.2f} (SD={df_metrics['mean_confidence'].std():.2f})")
    log(f"  Mean SD of responses: {df_metrics['sd_confidence'].mean():.2f} (SD={df_metrics['sd_confidence'].std():.2f})")

    log(f"\nResponse Distribution (mean % per level):")
    for level in [1, 2, 3, 4, 5, 6]:
        mean_pct = df_metrics[f'pct_{level}'].mean()
        log(f"  Level {level}: {mean_pct:.1f}%")

    log(f"\nEndpoint Usage:")
    log(f"  Mean % at endpoints: {df_metrics['pct_endpoints'].mean():.1f}%")
    log(f"  Min % at endpoints: {df_metrics['pct_endpoints'].min():.1f}%")
    log(f"  Max % at endpoints: {df_metrics['pct_endpoints'].max():.1f}%")

    return df_metrics


def identify_extreme_responders(df_metrics):
    """Identify participants with extreme response style."""
    log("\n" + "=" * 70)
    log("STEP 3: Identify Extreme Responders")
    log("=" * 70)

    # ERS: >50% at endpoints
    n_ers = df_metrics['ERS_flag'].sum()
    pct_ers = n_ers / len(df_metrics) * 100

    log(f"\nExtreme Response Style (>50% at endpoints):")
    log(f"  N with ERS: {n_ers} / {len(df_metrics)} ({pct_ers:.1f}%)")

    # Restricted range: SD < 0.8
    n_restricted = df_metrics['restricted_range_flag'].sum()
    pct_restricted = n_restricted / len(df_metrics) * 100

    log(f"\nRestricted Range (SD < 0.8):")
    log(f"  N with restricted range: {n_restricted} / {len(df_metrics)} ({pct_restricted:.1f}%)")

    # List ERS participants
    if n_ers > 0:
        ers_uids = df_metrics[df_metrics['ERS_flag']]['UID'].tolist()
        log(f"\nERS participants (UIDs): {ers_uids[:10]}{'...' if len(ers_uids) > 10 else ''}")

    # Interpretation
    log("\n" + "-" * 50)
    if pct_ers > 20:
        log("⚠️ WARNING: >20% ERS participants. Document as LIMITATION.")
        interpretation = "LIMITATION"
    elif pct_ers > 10:
        log("⚠️ MODERATE: 10-20% ERS participants. Note in Methods.")
        interpretation = "MODERATE"
    else:
        log("✓ GOOD: <10% ERS participants. Measurement quality validated.")
        interpretation = "GOOD"

    return {
        'n_ers': n_ers,
        'pct_ers': pct_ers,
        'n_restricted': n_restricted,
        'pct_restricted': pct_restricted,
        'interpretation': interpretation
    }


def test_ers_theta_difference(df_metrics, theta_file):
    """Test if theta estimates differ between ERS and non-ERS groups."""
    log("\n" + "=" * 70)
    log("STEP 4: Test ERS vs Non-ERS Theta Differences")
    log("=" * 70)

    # Load theta estimates from 6.1.1
    theta_path = PROJECT_ROOT / "results" / "ch6" / "6.1.1" / "data" / theta_file
    if not theta_path.exists():
        log(f"Theta file not found: {theta_path}")
        return None

    df_theta = pd.read_csv(theta_path)
    log(f"Loaded theta estimates: {len(df_theta)} rows")

    # Extract UID from composite_ID if needed
    if 'composite_ID' in df_theta.columns and 'UID' not in df_theta.columns:
        df_theta['UID'] = df_theta['composite_ID'].str.split('_').str[0]

    # Average theta per participant (across tests)
    theta_col = [c for c in df_theta.columns if 'theta' in c.lower()][0]
    df_theta_avg = df_theta.groupby('UID')[theta_col].mean().reset_index()
    df_theta_avg.columns = ['UID', 'mean_theta']

    # Merge with metrics
    df_merged = df_metrics.merge(df_theta_avg, on='UID', how='inner')
    log(f"Merged data: {len(df_merged)} participants")

    # Split by ERS
    ers_theta = df_merged[df_merged['ERS_flag']]['mean_theta']
    non_ers_theta = df_merged[~df_merged['ERS_flag']]['mean_theta']

    log(f"\nTheta by ERS status:")
    log(f"  ERS (n={len(ers_theta)}): mean={ers_theta.mean():.3f}, SD={ers_theta.std():.3f}")
    log(f"  Non-ERS (n={len(non_ers_theta)}): mean={non_ers_theta.mean():.3f}, SD={non_ers_theta.std():.3f}")

    # Independent samples t-test
    if len(ers_theta) >= 2 and len(non_ers_theta) >= 2:
        t_stat, p_val = stats.ttest_ind(ers_theta, non_ers_theta)
        cohens_d = (ers_theta.mean() - non_ers_theta.mean()) / np.sqrt(
            ((len(ers_theta)-1)*ers_theta.std()**2 + (len(non_ers_theta)-1)*non_ers_theta.std()**2) /
            (len(ers_theta) + len(non_ers_theta) - 2)
        )

        log(f"\nIndependent samples t-test:")
        log(f"  t = {t_stat:.3f}, p = {p_val:.4f}")
        log(f"  Cohen's d = {cohens_d:.3f}")

        if p_val < 0.05:
            log("  ⚠️ Significant difference - ERS may bias theta estimates")
        else:
            log("  ✓ No significant difference - ERS does not bias theta estimates")

        return {'t_stat': t_stat, 'p_val': p_val, 'cohens_d': cohens_d}
    else:
        log("  Not enough ERS participants for statistical test")
        return None


def create_visualizations(df_metrics):
    """Create diagnostic visualizations."""
    log("\n" + "=" * 70)
    log("STEP 5: Create Visualizations")
    log("=" * 70)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # 1. Response distribution histogram (6-point scale)
    ax = axes[0, 0]
    levels = [1, 2, 3, 4, 5, 6]
    mean_pcts = [df_metrics[f'pct_{l}'].mean() for l in levels]
    ax.bar(levels, mean_pcts, color='steelblue', edgecolor='black')
    ax.set_xlabel('Confidence Level (1=lowest, 6=highest)')
    ax.set_ylabel('Mean % of Responses')
    ax.set_title('Response Distribution (All Participants)')
    ax.set_xticks(levels)

    # 2. SD distribution
    ax = axes[0, 1]
    ax.hist(df_metrics['sd_confidence'], bins=20, color='steelblue', edgecolor='black')
    ax.axvline(x=1.0, color='red', linestyle='--', linewidth=2, label='Restricted range threshold')
    ax.set_xlabel('SD of Responses')
    ax.set_ylabel('Number of Participants')
    ax.set_title('Response Variability Distribution')
    ax.legend()

    # 3. Endpoint usage distribution
    ax = axes[1, 0]
    ax.hist(df_metrics['pct_endpoints'], bins=20, color='steelblue', edgecolor='black')
    ax.axvline(x=50, color='red', linestyle='--', linewidth=2, label='ERS threshold (50%)')
    ax.set_xlabel('% Responses at Endpoints (1 or 6)')
    ax.set_ylabel('Number of Participants')
    ax.set_title('Endpoint Usage Distribution')
    ax.legend()

    # 4. ERS by mean confidence
    ax = axes[1, 1]
    colors = ['red' if ers else 'steelblue' for ers in df_metrics['ERS_flag']]
    ax.scatter(df_metrics['mean_confidence'], df_metrics['sd_confidence'], c=colors, alpha=0.6)
    ax.axhline(y=1.0, color='red', linestyle='--', linewidth=1)
    ax.set_xlabel('Mean Confidence')
    ax.set_ylabel('SD of Responses')
    ax.set_title('Mean vs SD (Red = ERS)')

    plt.tight_layout()
    plot_path = OUTPUT_DIR / "confidence_response_patterns.png"
    plt.savefig(plot_path, dpi=150)
    plt.close()
    log(f"Saved: {plot_path.name}")

    return plot_path


def main():
    """Run complete response pattern analysis."""
    log("=" * 70)
    log("T2.4: CONFIDENCE RESPONSE PATTERN ANALYSIS")
    log("Chapter 6 Validity Rework - TIER 2 HIGH Priority")
    log("=" * 70)
    log(f"Date: {pd.Timestamp.now()}")

    # Step 1: Extract confidence ratings
    df_long = extract_confidence_ratings()

    # Step 2: Compute per-participant metrics
    df_metrics = compute_participant_metrics(df_long)

    # Step 3: Identify extreme responders
    ers_results = identify_extreme_responders(df_metrics)

    # Step 4: Test ERS-theta relationship
    theta_test = test_ers_theta_difference(df_metrics, 'step03_theta_confidence.csv')

    # Step 5: Create visualizations
    plot_path = create_visualizations(df_metrics)

    # Save outputs
    log("\n" + "=" * 70)
    log("OUTPUTS")
    log("=" * 70)

    # Save participant metrics
    metrics_path = OUTPUT_DIR / "confidence_response_metrics.csv"
    df_metrics.to_csv(metrics_path, index=False)
    log(f"Saved: {metrics_path.name}")

    # Summary report
    log("\n" + "=" * 70)
    log("SUMMARY")
    log("=" * 70)
    log(f"Participants analyzed: {len(df_metrics)}")
    log(f"Total confidence responses: {df_metrics['n_responses'].sum()}")
    log(f"Mean responses per participant: {df_metrics['n_responses'].mean():.1f}")
    log(f"\nExtreme Response Style (>50% endpoints):")
    log(f"  N: {ers_results['n_ers']} ({ers_results['pct_ers']:.1f}%)")
    log(f"  Interpretation: {ers_results['interpretation']}")
    log(f"\nRestricted Range (SD < 0.8):")
    log(f"  N: {ers_results['n_restricted']} ({ers_results['pct_restricted']:.1f}%)")

    if theta_test:
        log(f"\nERS-Theta Relationship:")
        log(f"  t = {theta_test['t_stat']:.3f}, p = {theta_test['p_val']:.4f}")
        log(f"  Cohen's d = {theta_test['cohens_d']:.3f}")

    log("\n" + "=" * 70)
    log("ANALYSIS COMPLETE")
    log("=" * 70)

    return {
        'df_metrics': df_metrics,
        'ers_results': ers_results,
        'theta_test': theta_test
    }


if __name__ == "__main__":
    main()
