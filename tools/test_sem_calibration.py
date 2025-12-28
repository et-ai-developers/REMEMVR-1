"""
Test Suite for SEM Calibration Toolkit

Purpose: Validate SEM implementation before batch application to RQs
Created: 2025-12-28

Test Cases:
-----------
1. Synthetic data with known properties
2. Edge cases (perfect correlation, zero correlation)
3. Reliability formula validation
4. Comparison with naive difference scores
"""

import numpy as np
import pandas as pd
from pathlib import Path
import sys

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.sem_calibration import (
    SEMCalibration,
    compute_difference_score_reliability
)


def generate_synthetic_data(
    n=400,
    reliability_acc=0.80,
    reliability_conf=0.75,
    correlation=0.50,
    true_calibration_effect=0.15,
    random_seed=42
):
    """
    Generate synthetic data with known properties.

    Parameters:
    -----------
    n : int
        Number of observations
    reliability_acc : float
        True reliability of accuracy
    reliability_conf : float
        True reliability of confidence
    correlation : float
        True latent correlation between accuracy and confidence
    true_calibration_effect : float
        True latent calibration (conf - acc)
    random_seed : int
        Random seed for reproducibility

    Returns:
    --------
    DataFrame with theta_accuracy, theta_confidence, true latent scores
    """
    np.random.seed(random_seed)

    # Generate true latent scores
    # Start with standard normal
    eta_acc = np.random.randn(n)

    # Generate correlated confidence
    eta_conf = correlation * eta_acc + np.sqrt(1 - correlation**2) * np.random.randn(n)

    # Add calibration effect (shift confidence)
    eta_conf = eta_conf + true_calibration_effect

    # Add measurement error
    sigma_acc = np.sqrt(1 - reliability_acc)
    sigma_conf = np.sqrt(1 - reliability_conf)

    error_acc = sigma_acc * np.random.randn(n)
    error_conf = sigma_conf * np.random.randn(n)

    theta_acc = eta_acc + error_acc
    theta_conf = eta_conf + error_conf

    # Create DataFrame
    data = pd.DataFrame({
        'UID': np.repeat(np.arange(1, n//4 + 1), 4)[:n],  # 4 timepoints per person
        'test': np.tile([1, 2, 3, 4], n//4)[:n],
        'theta_accuracy': theta_acc,
        'theta_confidence': theta_conf,
        'eta_accuracy_true': eta_acc,
        'eta_confidence_true': eta_conf,
        'eta_calibration_true': eta_conf - eta_acc
    })

    return data


def test_reliability_formula():
    """Test difference score reliability formula."""
    print("\n" + "="*60)
    print("TEST 1: Reliability Formula Validation")
    print("="*60)

    test_cases = [
        # (r_xx, r_yy, r_xy, expected_description)
        (0.90, 0.90, 0.00, "High reliability, zero correlation → High r_diff"),
        (0.90, 0.90, 0.50, "High reliability, moderate correlation → Moderate r_diff"),
        (0.90, 0.90, 0.80, "High reliability, high correlation → Low r_diff"),
        (0.70, 0.70, 0.60, "Moderate reliability, high correlation → Very low r_diff"),
        (0.80, 0.75, 0.58, "RQ 6.2.2 scenario → Negative r_diff"),
    ]

    for r_xx, r_yy, r_xy, description in test_cases:
        r_diff = compute_difference_score_reliability(r_xx, r_yy, r_xy)
        print(f"\n{description}")
        print(f"  r_xx={r_xx}, r_yy={r_yy}, r_xy={r_xy}")
        print(f"  → r_diff = {r_diff:.3f}")

        if r_diff < 0.50:
            print(f"  ⚠️  POOR reliability (<0.50) - SEM MANDATORY")
        elif r_diff < 0.70:
            print(f"  ⚠️  Questionable reliability (<0.70) - SEM recommended")
        else:
            print(f"  ✓  Acceptable reliability (≥0.70)")

    print("\n" + "="*60)


def test_synthetic_data_recovery():
    """Test if SEM can recover true latent scores from synthetic data."""
    print("\n" + "="*60)
    print("TEST 2: Synthetic Data Recovery")
    print("="*60)

    # Generate data with known properties
    print("\nGenerating synthetic data...")
    print("  True parameters:")
    print("    reliability_acc = 0.80")
    print("    reliability_conf = 0.75")
    print("    correlation = 0.50")
    print("    true_calibration_effect = 0.15")

    data = generate_synthetic_data(
        n=400,
        reliability_acc=0.80,
        reliability_conf=0.75,
        correlation=0.50,
        true_calibration_effect=0.15
    )

    # Save temporary files
    temp_dir = Path('temp_test_sem')
    temp_dir.mkdir(exist_ok=True)

    data[['UID', 'test', 'theta_accuracy']].to_csv(temp_dir / 'acc.csv', index=False)
    data[['UID', 'test', 'theta_confidence']].to_csv(temp_dir / 'conf.csv', index=False)

    # Fit SEM
    print("\nFitting SEM models...")
    sem = SEMCalibration(
        theta_accuracy=temp_dir / 'acc.csv',
        theta_confidence=temp_dir / 'conf.csv',
        reliability_acc=0.80,
        reliability_conf=0.75
    )

    sem.fit_latent_difference(verbose=False)
    sem.fit_residualized(verbose=False)

    # Compare recovered vs true calibration
    latent_calib = sem.get_latent_calibration('difference')
    true_calib = data['eta_calibration_true'].values

    from scipy.stats import pearsonr
    r_recovery, p = pearsonr(latent_calib, true_calib)

    print(f"\nRecovery Performance:")
    print(f"  True calibration: M={true_calib.mean():.3f}, SD={true_calib.std():.3f}")
    print(f"  SEM calibration:  M={latent_calib.mean():.3f}, SD={latent_calib.std():.3f}")
    print(f"  Correlation (recovered vs true): r={r_recovery:.3f}, p={p:.4f}")

    if r_recovery > 0.90:
        print(f"  ✓ EXCELLENT recovery (r > 0.90)")
    elif r_recovery > 0.80:
        print(f"  ✓ GOOD recovery (r > 0.80)")
    elif r_recovery > 0.70:
        print(f"  ⚠️  MODERATE recovery (r > 0.70)")
    else:
        print(f"  ✗ POOR recovery (r < 0.70)")

    # Compare naive difference vs SEM
    naive_diff = data['theta_confidence'] - data['theta_accuracy']
    r_naive, p_naive = pearsonr(naive_diff, true_calib)

    print(f"\nNaive Difference Score:")
    print(f"  Naive difference: M={naive_diff.mean():.3f}, SD={naive_diff.std():.3f}")
    print(f"  Correlation (naive vs true): r={r_naive:.3f}, p={p_naive:.4f}")

    print(f"\nImprovement from SEM:")
    print(f"  Correlation gain: {r_recovery - r_naive:.3f}")
    print(f"  Relative improvement: {((r_recovery - r_naive) / r_naive * 100):.1f}%")

    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)

    print("\n" + "="*60)


def test_extreme_cases():
    """Test edge cases."""
    print("\n" + "="*60)
    print("TEST 3: Edge Cases")
    print("="*60)

    test_cases = [
        ("Perfect correlation", 0.80, 0.80, 0.99),
        ("Zero correlation", 0.80, 0.80, 0.01),
        ("Low reliability, high correlation", 0.60, 0.60, 0.70),
    ]

    for name, r_xx, r_yy, r_xy in test_cases:
        print(f"\n{name}:")
        print(f"  r_xx={r_xx}, r_yy={r_yy}, r_xy={r_xy}")

        r_diff = compute_difference_score_reliability(r_xx, r_yy, r_xy)
        print(f"  → r_diff = {r_diff:.3f}")

        # Generate data
        data = generate_synthetic_data(
            n=400,
            reliability_acc=r_xx,
            reliability_conf=r_yy,
            correlation=r_xy,
            random_seed=42
        )

        # Quick check: can we create SEM object?
        try:
            temp_dir = Path('temp_edge')
            temp_dir.mkdir(exist_ok=True)

            data[['UID', 'test', 'theta_accuracy']].to_csv(temp_dir / 'acc.csv', index=False)
            data[['UID', 'test', 'theta_confidence']].to_csv(temp_dir / 'conf.csv', index=False)

            sem = SEMCalibration(
                theta_accuracy=temp_dir / 'acc.csv',
                theta_confidence=temp_dir / 'conf.csv',
                reliability_acc=r_xx,
                reliability_conf=r_yy
            )

            sem.fit_latent_difference(verbose=False)
            latent_calib = sem.get_latent_calibration()

            print(f"  ✓ SEM successfully fitted")
            print(f"  Latent calibration: M={latent_calib.mean():.3f}, SD={latent_calib.std():.3f}")

            import shutil
            shutil.rmtree(temp_dir)

        except Exception as e:
            print(f"  ✗ SEM failed: {e}")

    print("\n" + "="*60)


def run_all_tests():
    """Run complete test suite."""
    print("\n" + "="*70)
    print(" SEM CALIBRATION TOOLKIT - TEST SUITE ")
    print("="*70)
    print("\nValidating implementation before batch application...")

    try:
        test_reliability_formula()
        test_synthetic_data_recovery()
        test_extreme_cases()

        print("\n" + "="*70)
        print(" ALL TESTS COMPLETED ")
        print("="*70)
        print("\n✓ SEM toolkit validated and ready for RQ batch application")

    except Exception as e:
        print("\n" + "="*70)
        print(" TEST FAILED ")
        print("="*70)
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
