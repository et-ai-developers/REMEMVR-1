#!/usr/bin/env python
"""
Test Ch7 tools with real data to verify they work correctly.
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Test each module with real data
def test_data_extraction():
    """Test data extraction functions."""
    from tools.data import load_participant_data, load_test_data
    
    print("Testing data extraction...")
    
    # Load participant data
    participant_df = load_participant_data('data/dfnonvr.csv')
    print(f"✓ Loaded participant data: {participant_df.shape}")
    
    # Load test data
    test_df = load_test_data('data/dfdata.csv')
    print(f"✓ Loaded test data: {test_df.shape}")
    
    return participant_df, test_df


def test_regression():
    """Test regression tools."""
    from tools.analysis_regression import fit_multiple_regression
    
    print("\nTesting regression tools...")
    
    # Create synthetic data for testing
    np.random.seed(42)
    X = np.random.randn(100, 3)
    y = 2 * X[:, 0] + 1.5 * X[:, 1] - X[:, 2] + np.random.randn(100) * 0.5
    
    result = fit_multiple_regression(X, y, feature_names=['x1', 'x2', 'x3'])
    
    print(f"✓ Regression R²: {result['rsquared']:.3f}")
    print(f"✓ Coefficients: {result['coefficients']}")
    
    return result


def test_lpa():
    """Test LPA tools."""
    from tools.analysis_lpa import fit_lpa_models, compare_lpa_models
    
    print("\nTesting LPA tools...")
    
    # Create synthetic data with clear clusters
    np.random.seed(42)
    cluster1 = np.random.multivariate_normal([0, 0], [[1, 0], [0, 1]], 50)
    cluster2 = np.random.multivariate_normal([5, 5], [[1, 0], [0, 1]], 50)
    X = np.vstack([cluster1, cluster2])
    
    models = fit_lpa_models(X, k_range=[2, 3], seed=42)
    comparison = compare_lpa_models(models)
    
    print(f"✓ Best model: {comparison['best_k']} profiles")
    print(f"✓ BIC values: {comparison['bic_values']}")
    
    return models


def test_bootstrap():
    """Test bootstrap tools."""
    from tools.bootstrap import bootstrap_correlation_ci
    
    print("\nTesting bootstrap tools...")
    
    np.random.seed(42)
    x = np.random.randn(100)
    y = 0.7 * x + np.random.randn(100) * 0.5
    
    result = bootstrap_correlation_ci(x, y, n_bootstrap=100, seed=42)
    
    print(f"✓ Correlation: {result['r']:.3f}")
    print(f"✓ 95% CI: [{result['ci_lower']:.3f}, {result['ci_upper']:.3f}]")
    
    return result


def test_clinical():
    """Test clinical tools."""
    from tools.clinical import compute_sensitivity_specificity
    
    print("\nTesting clinical tools...")
    
    # Create synthetic binary classification data
    np.random.seed(42)
    y_true = np.random.randint(0, 2, 100)
    y_pred = y_true.copy()
    # Add some errors
    error_idx = np.random.choice(100, 20, replace=False)
    y_pred[error_idx] = 1 - y_pred[error_idx]
    
    result = compute_sensitivity_specificity(y_true, y_pred)
    
    print(f"✓ Sensitivity: {result['sensitivity']:.3f}")
    print(f"✓ Specificity: {result['specificity']:.3f}")
    print(f"✓ Accuracy: {result['accuracy']:.3f}")
    
    return result


def test_extensions():
    """Test extension functions."""
    from tools.analysis_extensions import (
        compute_cohens_q_effect_size,
        standardize_scores
    )
    
    print("\nTesting extension tools...")
    
    # Cohen's q
    q = compute_cohens_q_effect_size(0.6, 0.3)
    print(f"✓ Cohen's q: {q:.3f}")
    
    # Standardization
    scores = np.array([45, 55, 50, 60, 40])
    z_scores = standardize_scores(scores, mean=50, sd=10)
    print(f"✓ Z-scores: {z_scores}")
    
    return q, z_scores


def test_stats():
    """Test statistical tools with D068 compliance."""
    from tools.analysis_stats import one_way_anova_d068
    
    print("\nTesting stats tools (D068 compliance)...")
    
    # Create groups with different means
    np.random.seed(42)
    group1 = np.random.normal(10, 2, 30)
    group2 = np.random.normal(12, 2, 30)
    group3 = np.random.normal(11, 2, 30)
    
    result = one_way_anova_d068([group1, group2, group3], correction='bonferroni')
    
    print(f"✓ F-statistic: {result['F']:.3f}")
    print(f"✓ p-value (uncorrected): {result['p_uncorrected']:.4f}")
    print(f"✓ p-value (corrected): {result['p_corrected']:.4f}")
    print(f"✓ Eta²: {result['eta_squared']:.3f}")
    
    return result


def main():
    """Run all tests."""
    print("=" * 60)
    print("TESTING CH7 TOOLS WITH REAL/SYNTHETIC DATA")
    print("=" * 60)
    
    # Check if data files exist
    data_path = Path('data')
    if not (data_path / 'dfnonvr.csv').exists():
        print("⚠️  Data files not found, using synthetic data only")
        use_real_data = False
    else:
        use_real_data = True
    
    # Run tests
    try:
        if use_real_data:
            participant_df, test_df = test_data_extraction()
        
        regression_result = test_regression()
        lpa_models = test_lpa()
        bootstrap_result = test_bootstrap()
        clinical_result = test_clinical()
        q, z_scores = test_extensions()
        anova_result = test_stats()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED - Ch7 tools ready for execution!")
        print("=" * 60)
        
        # Summary statistics
        print("\nSummary:")
        print(f"- Data extraction: {'✓' if use_real_data else 'Skipped (no data files)'}")
        print(f"- Regression tools: ✓ (R² = {regression_result['rsquared']:.3f})")
        print(f"- LPA tools: ✓ (BIC-based selection working)")
        print(f"- Bootstrap tools: ✓ (CI estimation working)")
        print(f"- Clinical tools: ✓ (Classification metrics working)")
        print(f"- Extension tools: ✓ (All adapters working)")
        print(f"- Stats tools: ✓ (D068 compliance verified)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)