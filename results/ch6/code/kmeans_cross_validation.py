#!/usr/bin/env python3
"""
T3.4: K-Means Cross-Validation for Clustering Stability
========================================================

Addresses potential overfitting in K-means clustering analyses:
- RQ 6.1.5: Confidence trajectory phenotypes (K=3)
- RQ 6.8.4: Location-type confidence phenotypes (K=3)

Procedure:
1. Split sample (70/30 train/test)
2. Fit K-means on training set
3. Assign test set to nearest centroid
4. Compare silhouette scores (train vs test)
5. Repeat 10× with different splits
6. Report stability: mean ± SD of test silhouette

Success Criteria:
- Mean test silhouette within 0.10 of train silhouette (stable)
- Test silhouette ≥ 0.25 (adequate separation even in holdout)
"""

import sys
from pathlib import Path
from datetime import datetime
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy import stats

# =============================================================================
# PATHS AND CONFIGURATION
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]  # REMEMVR
OUTPUT_DIR = PROJECT_ROOT / "results" / "ch6" / "diagnostics"
LOG_FILE = OUTPUT_DIR / "kmeans_cross_validation.log"

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Configuration
N_SPLITS = 10
TRAIN_FRACTION = 0.70
RANDOM_STATE_BASE = 42
K_CLUSTERS = 3  # Both RQs use K=3

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
# CROSS-VALIDATION FUNCTION
# =============================================================================

def cross_validate_kmeans(X: np.ndarray, k: int, n_splits: int = 10,
                          train_frac: float = 0.70, random_state_base: int = 42) -> dict:
    """
    Cross-validate K-means clustering with train/test splits.

    Parameters:
    -----------
    X : np.ndarray
        Feature matrix (N x D)
    k : int
        Number of clusters
    n_splits : int
        Number of random train/test splits
    train_frac : float
        Fraction of data for training (e.g., 0.70)
    random_state_base : int
        Base random state for reproducibility

    Returns:
    --------
    dict with:
        - train_silhouettes: list of train silhouette scores
        - test_silhouettes: list of test silhouette scores
        - train_mean, train_sd: summary statistics
        - test_mean, test_sd: summary statistics
        - gap_mean, gap_sd: train - test difference
        - stable: bool (gap < 0.10)
        - adequate_test: bool (test_mean >= 0.25)
    """
    n = len(X)
    n_train = int(n * train_frac)
    n_test = n - n_train

    train_silhouettes = []
    test_silhouettes = []

    for i in range(n_splits):
        # Set random state for this split
        np.random.seed(random_state_base + i)

        # Random permutation
        indices = np.random.permutation(n)
        train_idx = indices[:n_train]
        test_idx = indices[n_train:]

        X_train = X[train_idx]
        X_test = X[test_idx]

        # Fit K-means on training set
        kmeans = KMeans(n_clusters=k, random_state=random_state_base, n_init=10)
        kmeans.fit(X_train)

        # Get labels for training set
        train_labels = kmeans.labels_

        # Assign test set to nearest centroid
        test_labels = kmeans.predict(X_test)

        # Compute silhouette scores
        # Train silhouette
        if len(np.unique(train_labels)) > 1:
            train_sil = silhouette_score(X_train, train_labels)
        else:
            train_sil = np.nan  # Single cluster = no silhouette

        # Test silhouette
        if len(np.unique(test_labels)) > 1:
            test_sil = silhouette_score(X_test, test_labels)
        else:
            test_sil = np.nan  # Single cluster in test set

        train_silhouettes.append(train_sil)
        test_silhouettes.append(test_sil)

    # Remove NaN values for summary
    train_valid = [s for s in train_silhouettes if not np.isnan(s)]
    test_valid = [s for s in test_silhouettes if not np.isnan(s)]

    # Summary statistics
    train_mean = np.mean(train_valid) if train_valid else np.nan
    train_sd = np.std(train_valid, ddof=1) if len(train_valid) > 1 else np.nan
    test_mean = np.mean(test_valid) if test_valid else np.nan
    test_sd = np.std(test_valid, ddof=1) if len(test_valid) > 1 else np.nan

    # Gap analysis
    gap_mean = train_mean - test_mean if not np.isnan(train_mean) and not np.isnan(test_mean) else np.nan
    gap_sd = np.sqrt(train_sd**2 + test_sd**2) if not np.isnan(train_sd) and not np.isnan(test_sd) else np.nan

    # Success criteria
    stable = abs(gap_mean) < 0.10 if not np.isnan(gap_mean) else False
    adequate_test = test_mean >= 0.25 if not np.isnan(test_mean) else False

    return {
        'train_silhouettes': train_silhouettes,
        'test_silhouettes': test_silhouettes,
        'train_mean': train_mean,
        'train_sd': train_sd,
        'test_mean': test_mean,
        'test_sd': test_sd,
        'gap_mean': gap_mean,
        'gap_sd': gap_sd,
        'n_valid_splits': len(test_valid),
        'stable': stable,
        'adequate_test': adequate_test
    }

# =============================================================================
# RQ 6.1.5: Confidence Trajectory Phenotypes
# =============================================================================

def cv_6_1_5():
    """Cross-validate K-means for RQ 6.1.5 (confidence trajectory phenotypes)."""
    log("=" * 70)
    log("RQ 6.1.5: Confidence Trajectory Phenotypes - Cross-Validation")
    log("=" * 70)

    # Load standardized features
    data_file = PROJECT_ROOT / "results" / "ch6" / "6.1.5" / "data" / "step02_standardized_features.csv"
    log(f"Loading: {data_file}")
    df = pd.read_csv(data_file)
    log(f"  Loaded {len(df)} participants")

    # Extract feature matrix
    X = df[['intercept_z', 'slope_z']].values
    log(f"  Features: intercept_z, slope_z")
    log(f"  K = {K_CLUSTERS}")

    # Load original validation for comparison
    orig_file = PROJECT_ROOT / "results" / "ch6" / "6.1.5" / "data" / "step05_validation_metrics.csv"
    df_orig = pd.read_csv(orig_file)
    orig_sil = df_orig[df_orig['metric'] == 'silhouette']['value'].values[0]
    log(f"  Original full-sample silhouette: {orig_sil:.4f}")

    # Cross-validation
    log(f"\n  Running {N_SPLITS}-fold cross-validation (70/30 split)...")
    results = cross_validate_kmeans(X, K_CLUSTERS, N_SPLITS, TRAIN_FRACTION, RANDOM_STATE_BASE)

    # Display results
    log(f"\n  CROSS-VALIDATION RESULTS:")
    log(f"  {'Metric':<25} {'Value':>15}")
    log(f"  {'-'*25} {'-'*15}")
    log(f"  {'Train silhouette mean':<25} {results['train_mean']:>15.4f}")
    log(f"  {'Train silhouette SD':<25} {results['train_sd']:>15.4f}")
    log(f"  {'Test silhouette mean':<25} {results['test_mean']:>15.4f}")
    log(f"  {'Test silhouette SD':<25} {results['test_sd']:>15.4f}")
    log(f"  {'Gap (train - test)':<25} {results['gap_mean']:>15.4f}")
    log(f"  {'Gap SD':<25} {results['gap_sd']:>15.4f}")
    log(f"  {'Valid splits':<25} {results['n_valid_splits']:>15d}")

    log(f"\n  SUCCESS CRITERIA:")
    log(f"  {'Stability (gap < 0.10)':<25} {'PASS' if results['stable'] else 'FAIL':>15}")
    log(f"  {'Test adequate (≥0.25)':<25} {'PASS' if results['adequate_test'] else 'FAIL':>15}")

    # Overall assessment
    overall = 'ROBUST' if results['stable'] and results['adequate_test'] else 'REVIEW NEEDED'
    log(f"\n  OVERALL: {overall}")

    return {
        'rq': '6.1.5',
        'analysis': 'Confidence Trajectory Phenotypes',
        'k': K_CLUSTERS,
        'n_participants': len(df),
        'original_silhouette': orig_sil,
        **results,
        'overall': overall
    }

# =============================================================================
# RQ 6.8.4: Location-Type Confidence Phenotypes
# =============================================================================

def cv_6_8_4():
    """Cross-validate K-means for RQ 6.8.4 (location-type confidence phenotypes)."""
    log("\n" + "=" * 70)
    log("RQ 6.8.4: Location-Type Confidence Phenotypes - Cross-Validation")
    log("=" * 70)

    # Load standardized features
    data_file = PROJECT_ROOT / "results" / "ch6" / "6.8.4" / "data" / "step01_standardized_features.csv"
    log(f"Loading: {data_file}")
    df = pd.read_csv(data_file)
    log(f"  Loaded {len(df)} participants")

    # Identify feature columns (z-scored)
    z_cols = [c for c in df.columns if '_z' in c]
    if not z_cols:
        # Try alternative naming
        z_cols = [c for c in df.columns if c not in ['UID', 'Unnamed: 0']]
        # Check if they look like features (numeric, not UID)
        z_cols = [c for c in z_cols if df[c].dtype in ['float64', 'int64']]

    log(f"  Features: {z_cols}")

    # Extract feature matrix
    X = df[z_cols].values
    log(f"  Feature matrix shape: {X.shape}")
    log(f"  K = {K_CLUSTERS}")

    # Load original validation for comparison
    orig_file = PROJECT_ROOT / "results" / "ch6" / "6.8.4" / "data" / "step04_validation.csv"
    df_orig = pd.read_csv(orig_file)
    orig_sil_row = df_orig[df_orig['metric'] == 'Silhouette']
    orig_sil = orig_sil_row['value'].values[0] if len(orig_sil_row) > 0 else np.nan
    log(f"  Original full-sample silhouette: {orig_sil:.4f}")

    # Cross-validation
    log(f"\n  Running {N_SPLITS}-fold cross-validation (70/30 split)...")
    results = cross_validate_kmeans(X, K_CLUSTERS, N_SPLITS, TRAIN_FRACTION, RANDOM_STATE_BASE)

    # Display results
    log(f"\n  CROSS-VALIDATION RESULTS:")
    log(f"  {'Metric':<25} {'Value':>15}")
    log(f"  {'-'*25} {'-'*15}")
    log(f"  {'Train silhouette mean':<25} {results['train_mean']:>15.4f}")
    log(f"  {'Train silhouette SD':<25} {results['train_sd']:>15.4f}")
    log(f"  {'Test silhouette mean':<25} {results['test_mean']:>15.4f}")
    log(f"  {'Test silhouette SD':<25} {results['test_sd']:>15.4f}")
    log(f"  {'Gap (train - test)':<25} {results['gap_mean']:>15.4f}")
    log(f"  {'Gap SD':<25} {results['gap_sd']:>15.4f}")
    log(f"  {'Valid splits':<25} {results['n_valid_splits']:>15d}")

    log(f"\n  SUCCESS CRITERIA:")
    log(f"  {'Stability (gap < 0.10)':<25} {'PASS' if results['stable'] else 'FAIL':>15}")
    log(f"  {'Test adequate (≥0.25)':<25} {'PASS' if results['adequate_test'] else 'FAIL':>15}")

    # Overall assessment
    overall = 'ROBUST' if results['stable'] and results['adequate_test'] else 'REVIEW NEEDED'
    log(f"\n  OVERALL: {overall}")

    return {
        'rq': '6.8.4',
        'analysis': 'Location-Type Confidence Phenotypes',
        'k': K_CLUSTERS,
        'n_participants': len(df),
        'original_silhouette': orig_sil,
        **results,
        'overall': overall
    }

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Execute K-means cross-validation for both RQs."""
    log("=" * 70)
    log("T3.4: K-Means Cross-Validation for Clustering Stability")
    log("=" * 70)
    log(f"Start time: {datetime.now()}")
    log(f"Project root: {PROJECT_ROOT}")
    log(f"Configuration: N_SPLITS={N_SPLITS}, TRAIN_FRAC={TRAIN_FRACTION}, K={K_CLUSTERS}")
    log("")

    results = []

    try:
        # Cross-validate RQ 6.1.5
        result_6_1_5 = cv_6_1_5()
        results.append(result_6_1_5)

        # Cross-validate RQ 6.8.4
        result_6_8_4 = cv_6_8_4()
        results.append(result_6_8_4)

        # Save combined results
        df_results = pd.DataFrame([{
            'rq': r['rq'],
            'analysis': r['analysis'],
            'k': r['k'],
            'n_participants': r['n_participants'],
            'original_silhouette': r['original_silhouette'],
            'train_sil_mean': r['train_mean'],
            'train_sil_sd': r['train_sd'],
            'test_sil_mean': r['test_mean'],
            'test_sil_sd': r['test_sd'],
            'gap_mean': r['gap_mean'],
            'gap_sd': r['gap_sd'],
            'n_valid_splits': r['n_valid_splits'],
            'stable': r['stable'],
            'adequate_test': r['adequate_test'],
            'overall': r['overall']
        } for r in results])

        out_file = OUTPUT_DIR / "kmeans_cross_validation.csv"
        df_results.to_csv(out_file, index=False)
        log(f"\nSaved: {out_file}")

        # =====================================================================
        # FINAL SUMMARY
        # =====================================================================
        log("\n" + "=" * 70)
        log("FINAL SUMMARY")
        log("=" * 70)

        log("\n1. RQ 6.1.5 (Confidence Trajectory Phenotypes):")
        log(f"   Original silhouette: {result_6_1_5['original_silhouette']:.4f}")
        log(f"   CV train silhouette: {result_6_1_5['train_mean']:.4f} ± {result_6_1_5['train_sd']:.4f}")
        log(f"   CV test silhouette: {result_6_1_5['test_mean']:.4f} ± {result_6_1_5['test_sd']:.4f}")
        log(f"   Gap (train-test): {result_6_1_5['gap_mean']:.4f}")
        log(f"   Stability: {'PASS' if result_6_1_5['stable'] else 'FAIL'}")
        log(f"   Test adequate: {'PASS' if result_6_1_5['adequate_test'] else 'FAIL'}")
        log(f"   OVERALL: {result_6_1_5['overall']}")

        log("\n2. RQ 6.8.4 (Location-Type Confidence Phenotypes):")
        log(f"   Original silhouette: {result_6_8_4['original_silhouette']:.4f}")
        log(f"   CV train silhouette: {result_6_8_4['train_mean']:.4f} ± {result_6_8_4['train_sd']:.4f}")
        log(f"   CV test silhouette: {result_6_8_4['test_mean']:.4f} ± {result_6_8_4['test_sd']:.4f}")
        log(f"   Gap (train-test): {result_6_8_4['gap_mean']:.4f}")
        log(f"   Stability: {'PASS' if result_6_8_4['stable'] else 'FAIL'}")
        log(f"   Test adequate: {'PASS' if result_6_8_4['adequate_test'] else 'FAIL'}")
        log(f"   OVERALL: {result_6_8_4['overall']}")

        # Overall assessment
        n_robust = sum(1 for r in results if r['overall'] == 'ROBUST')
        log(f"\n3. OVERALL:")
        log(f"   Robust clusters: {n_robust}/2")

        if n_robust == 2:
            log("   ASSESSMENT: Both clustering solutions are STABLE")
            log("   Findings generalize beyond training sample")
        elif n_robust == 1:
            log("   ASSESSMENT: MIXED stability")
            log("   One RQ shows potential overfitting; interpret cautiously")
        else:
            log("   ASSESSMENT: Both clustering solutions show INSTABILITY")
            log("   Phenotype boundaries may be sample-specific artifacts")

        # Thesis recommendation
        log("\n4. THESIS RECOMMENDATION:")
        log("   Document CV results in Methods section.")
        log("   Report test silhouette alongside full-sample metrics.")
        log("   Acknowledge that N=100 limits cluster generalizability.")

    except Exception as e:
        log(f"\nERROR: {e}")
        import traceback
        log(traceback.format_exc())
        sys.exit(1)

    log("\n" + "=" * 70)
    log("T3.4 COMPLETE")
    log("=" * 70)
    log(f"End time: {datetime.now()}")

if __name__ == "__main__":
    main()
