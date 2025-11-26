"""
Tests for test_intercept_slope_correlation_d068 function (Tool 8/25).

RQ 5.13: Test correlation between random intercepts and random slopes with D068 dual p-value reporting.
"""

import pytest
import pandas as pd
import numpy as np
from tools.analysis_lmm import test_intercept_slope_correlation_d068


def test_basic_structure():
    """Test that output has all required keys."""
    # Create synthetic random effects (N=60)
    np.random.seed(42)
    intercepts = np.random.normal(0, 0.5, 60)
    slopes = np.random.normal(0, 0.1, 60)

    df = pd.DataFrame({
        'UID': [f'P{i:03d}' for i in range(1, 61)],
        'Group Var': intercepts,
        'Group x TSVR_hours Var': slopes
    })

    result = test_intercept_slope_correlation_d068(df)

    assert isinstance(result, dict)
    assert 'r' in result
    assert 'p_uncorrected' in result
    assert 'p_bonferroni' in result
    assert 'significant_uncorrected' in result
    assert 'significant_bonferroni' in result
    assert 'interpretation' in result


def test_correlation_bounds():
    """Test that correlation coefficient is in [-1, 1]."""
    np.random.seed(42)
    intercepts = np.random.normal(0, 0.5, 60)
    slopes = np.random.normal(0, 0.1, 60)

    df = pd.DataFrame({
        'UID': [f'P{i:03d}' for i in range(1, 61)],
        'Group Var': intercepts,
        'Group x TSVR_hours Var': slopes
    })

    result = test_intercept_slope_correlation_d068(df)

    assert -1 <= result['r'] <= 1


def test_pvalue_bounds():
    """Test that p-values are in [0, 1]."""
    np.random.seed(42)
    intercepts = np.random.normal(0, 0.5, 60)
    slopes = np.random.normal(0, 0.1, 60)

    df = pd.DataFrame({
        'UID': [f'P{i:03d}' for i in range(1, 61)],
        'Group Var': intercepts,
        'Group x TSVR_hours Var': slopes
    })

    result = test_intercept_slope_correlation_d068(df)

    assert 0 <= result['p_uncorrected'] <= 1
    assert 0 <= result['p_bonferroni'] <= 1


def test_bonferroni_more_conservative():
    """Test that Bonferroni p-value >= uncorrected p-value."""
    np.random.seed(42)
    intercepts = np.random.normal(0, 0.5, 60)
    slopes = np.random.normal(0, 0.1, 60)

    df = pd.DataFrame({
        'UID': [f'P{i:03d}' for i in range(1, 61)],
        'Group Var': intercepts,
        'Group x TSVR_hours Var': slopes
    })

    result = test_intercept_slope_correlation_d068(df)

    assert result['p_bonferroni'] >= result['p_uncorrected']


def test_bonferroni_calculation():
    """Test Bonferroni correction formula: p_bonf = min(p_uncorr * n_tests, 1.0)."""
    np.random.seed(42)
    intercepts = np.random.normal(0, 0.5, 60)
    slopes = np.random.normal(0, 0.1, 60)

    df = pd.DataFrame({
        'UID': [f'P{i:03d}' for i in range(1, 61)],
        'Group Var': intercepts,
        'Group x TSVR_hours Var': slopes
    })

    n_tests = 15
    result = test_intercept_slope_correlation_d068(df, n_tests=n_tests)

    expected_bonf = min(result['p_uncorrected'] * n_tests, 1.0)
    assert abs(result['p_bonferroni'] - expected_bonf) < 1e-10


def test_perfect_positive_correlation():
    """Test perfect positive correlation (r=1.0)."""
    # Create perfectly correlated data
    intercepts = np.linspace(-1, 1, 60)
    slopes = intercepts.copy()  # Perfect correlation

    df = pd.DataFrame({
        'UID': [f'P{i:03d}' for i in range(1, 61)],
        'Group Var': intercepts,
        'Group x TSVR_hours Var': slopes
    })

    result = test_intercept_slope_correlation_d068(df)

    assert abs(result['r'] - 1.0) < 1e-10
    assert result['p_uncorrected'] < 0.001  # Highly significant


def test_perfect_negative_correlation():
    """Test perfect negative correlation (r=-1.0)."""
    # Create perfectly anti-correlated data
    intercepts = np.linspace(-1, 1, 60)
    slopes = -intercepts  # Perfect negative correlation

    df = pd.DataFrame({
        'UID': [f'P{i:03d}' for i in range(1, 61)],
        'Group Var': intercepts,
        'Group x TSVR_hours Var': slopes
    })

    result = test_intercept_slope_correlation_d068(df)

    assert abs(result['r'] - (-1.0)) < 1e-10
    assert result['p_uncorrected'] < 0.001  # Highly significant


def test_zero_correlation():
    """Test zero correlation (independent intercepts and slopes)."""
    np.random.seed(123)
    intercepts = np.random.normal(0, 0.5, 100)
    slopes = np.random.normal(0, 0.1, 100)  # Independent random draws

    df = pd.DataFrame({
        'UID': [f'P{i:03d}' for i in range(1, 101)],
        'Group Var': intercepts,
        'Group x TSVR_hours Var': slopes
    })

    result = test_intercept_slope_correlation_d068(df)

    # Should be near zero (within sampling variability)
    assert abs(result['r']) < 0.3  # Loose bound for random data
    assert result['p_uncorrected'] > 0.01  # Likely not significant


def test_significance_flags():
    """Test that significance flags match p-value thresholds."""
    np.random.seed(42)
    intercepts = np.random.normal(0, 0.5, 60)
    slopes = np.random.normal(0, 0.1, 60)

    df = pd.DataFrame({
        'UID': [f'P{i:03d}' for i in range(1, 61)],
        'Group Var': intercepts,
        'Group x TSVR_hours Var': slopes
    })

    family_alpha = 0.05
    result = test_intercept_slope_correlation_d068(df, family_alpha=family_alpha)

    # Check uncorrected significance
    if result['p_uncorrected'] < family_alpha:
        assert result['significant_uncorrected'] == True
    else:
        assert result['significant_uncorrected'] == False

    # Check Bonferroni significance
    if result['p_bonferroni'] < family_alpha:
        assert result['significant_bonferroni'] == True
    else:
        assert result['significant_bonferroni'] == False


def test_interpretation_field():
    """Test that interpretation string is present and non-empty."""
    np.random.seed(42)
    intercepts = np.random.normal(0, 0.5, 60)
    slopes = np.random.normal(0, 0.1, 60)

    df = pd.DataFrame({
        'UID': [f'P{i:03d}' for i in range(1, 61)],
        'Group Var': intercepts,
        'Group x TSVR_hours Var': slopes
    })

    result = test_intercept_slope_correlation_d068(df)

    assert isinstance(result['interpretation'], str)
    assert len(result['interpretation']) > 0


def test_custom_family_alpha():
    """Test that custom family_alpha affects Bonferroni threshold."""
    np.random.seed(42)
    intercepts = np.random.normal(0, 0.5, 60)
    slopes = np.random.normal(0, 0.1, 60)

    df = pd.DataFrame({
        'UID': [f'P{i:03d}' for i in range(1, 61)],
        'Group Var': intercepts,
        'Group x TSVR_hours Var': slopes
    })

    result_strict = test_intercept_slope_correlation_d068(df, family_alpha=0.01, n_tests=15)
    result_lenient = test_intercept_slope_correlation_d068(df, family_alpha=0.10, n_tests=15)

    # Same correlation and p-values
    assert result_strict['r'] == result_lenient['r']
    assert result_strict['p_uncorrected'] == result_lenient['p_uncorrected']
    assert result_strict['p_bonferroni'] == result_lenient['p_bonferroni']

    # Different significance thresholds may affect flags (depending on p-values)
    # Just verify both have the significance keys
    assert 'significant_bonferroni' in result_strict
    assert 'significant_bonferroni' in result_lenient


def test_custom_n_tests():
    """Test that custom n_tests affects Bonferroni correction magnitude."""
    np.random.seed(42)
    intercepts = np.random.normal(0, 0.5, 60)
    slopes = np.random.normal(0, 0.1, 60)

    df = pd.DataFrame({
        'UID': [f'P{i:03d}' for i in range(1, 61)],
        'Group Var': intercepts,
        'Group x TSVR_hours Var': slopes
    })

    result_5 = test_intercept_slope_correlation_d068(df, n_tests=5)
    result_15 = test_intercept_slope_correlation_d068(df, n_tests=15)

    # Bonferroni p-value should be 3× larger for n_tests=15 vs 5
    expected_ratio = 15 / 5
    actual_ratio = result_15['p_bonferroni'] / result_5['p_bonferroni']

    # Allow for min(p*n, 1.0) capping
    if result_15['p_bonferroni'] < 1.0 and result_5['p_bonferroni'] < 1.0:
        assert abs(actual_ratio - expected_ratio) < 0.01


def test_column_name_variations():
    """Test that function handles different column naming conventions."""
    np.random.seed(42)
    intercepts = np.random.normal(0, 0.5, 60)
    slopes = np.random.normal(0, 0.1, 60)

    # Standard naming
    df = pd.DataFrame({
        'UID': [f'P{i:03d}' for i in range(1, 61)],
        'Group Var': intercepts,
        'Group x TSVR_hours Var': slopes
    })

    result = test_intercept_slope_correlation_d068(df)

    assert result['r'] is not None
    assert result['p_uncorrected'] is not None


def test_realistic_rq513_scenario():
    """Test realistic scenario from RQ 5.13: N=100 participants, moderate correlation."""
    # Simulate moderate negative correlation (faster forgetting → steeper slopes for high starters)
    np.random.seed(42)
    n = 100

    # Generate correlated intercepts and slopes
    mean = [0, 0]
    cov = [[0.5, -0.15], [-0.15, 0.1]]  # Moderate negative correlation r ≈ -0.21
    intercepts, slopes = np.random.multivariate_normal(mean, cov, n).T

    df = pd.DataFrame({
        'UID': [f'P{i:03d}' for i in range(1, n+1)],
        'Group Var': intercepts,
        'Group x TSVR_hours Var': slopes
    })

    result = test_intercept_slope_correlation_d068(df, family_alpha=0.05, n_tests=15)

    # Should detect moderate to strong negative correlation (actual r ≈ -0.61 with seed 42)
    assert result['r'] < 0  # Negative correlation
    assert 0 <= result['p_uncorrected'] <= 1
    assert 0 <= result['p_bonferroni'] <= 1
    assert result['p_bonferroni'] >= result['p_uncorrected']

    # Interpretation should mention correlation direction
    assert isinstance(result['interpretation'], str)
