"""
Tests for validate_correlation_test_d068 function.

Test Coverage:
- Basic structure (4 required keys)
- Valid D068 compliant correlation results
- Missing p_uncorrected column
- Missing p_bonferroni column
- Alternative correction names (p_holm, p_fdr accepted)
- Empty DataFrame handling
- Extra columns don't interfere
- Required columns parameter validation
- Multiple correlation tests
- Realistic RQ 5.13 scenario (intercept-slope correlation)
"""

import pandas as pd
import pytest
from tools.validation import validate_correlation_test_d068


def test_validate_correlation_test_d068_basic_structure():
    """Test output has required keys."""
    df = pd.DataFrame({
        'correlation': [0.5],
        'p_uncorrected': [0.01],
        'p_bonferroni': [0.03]
    })
    result = validate_correlation_test_d068(df)

    assert 'valid' in result
    assert 'd068_compliant' in result
    assert 'missing_cols' in result
    assert 'message' in result


def test_validate_correlation_test_d068_valid_compliant():
    """Test valid D068 compliant correlation results."""
    df = pd.DataFrame({
        'r': [-0.45],
        'p_uncorrected': [0.003],
        'p_bonferroni': [0.045],
        'significant_uncorrected': [True],
        'significant_bonferroni': [True]
    })
    result = validate_correlation_test_d068(df)

    assert result['valid'] is True
    assert result['d068_compliant'] is True
    assert len(result['missing_cols']) == 0
    assert 'Decision D068 compliant' in result['message']


def test_validate_correlation_test_d068_missing_p_uncorrected():
    """Test missing p_uncorrected column."""
    df = pd.DataFrame({
        'r': [0.5],
        'p_bonferroni': [0.03]
    })
    result = validate_correlation_test_d068(df)

    assert result['valid'] is False
    assert result['d068_compliant'] is False
    assert 'p_uncorrected' in result['missing_cols']
    assert 'p_uncorrected' in result['message']


def test_validate_correlation_test_d068_missing_p_bonferroni():
    """Test missing correction column."""
    df = pd.DataFrame({
        'r': [0.5],
        'p_uncorrected': [0.01]
    })
    result = validate_correlation_test_d068(df)

    assert result['valid'] is False
    assert result['d068_compliant'] is False
    assert 'p_bonferroni' in result['missing_cols']
    assert 'correction method' in result['message']


def test_validate_correlation_test_d068_alternative_correction():
    """Test alternative correction names accepted (p_holm, p_fdr)."""
    # Test with p_holm
    df_holm = pd.DataFrame({
        'r': [0.5],
        'p_uncorrected': [0.01],
        'p_holm': [0.02]
    })
    result_holm = validate_correlation_test_d068(df_holm)
    assert result_holm['valid'] is True
    assert result_holm['d068_compliant'] is True

    # Test with p_fdr
    df_fdr = pd.DataFrame({
        'r': [0.5],
        'p_uncorrected': [0.01],
        'p_fdr': [0.015]
    })
    result_fdr = validate_correlation_test_d068(df_fdr)
    assert result_fdr['valid'] is True
    assert result_fdr['d068_compliant'] is True


def test_validate_correlation_test_d068_empty_dataframe():
    """Test empty DataFrame handling."""
    df = pd.DataFrame(columns=['r', 'p_uncorrected', 'p_bonferroni'])
    result = validate_correlation_test_d068(df)

    assert result['valid'] is False
    assert 'Empty DataFrame' in result['message']


def test_validate_correlation_test_d068_extra_columns():
    """Test extra columns don't interfere with validation."""
    df = pd.DataFrame({
        'r': [-0.45],
        'r_squared': [0.20],
        'n': [100],
        'p_uncorrected': [0.003],
        'p_bonferroni': [0.045],
        'significant_uncorrected': [True],
        'significant_bonferroni': [True],
        'interpretation': ['Moderate negative correlation']
    })
    result = validate_correlation_test_d068(df)

    assert result['valid'] is True
    assert result['d068_compliant'] is True


def test_validate_correlation_test_d068_custom_required_cols():
    """Test custom required_cols parameter."""
    df = pd.DataFrame({
        'pearson_r': [0.5],
        'p_raw': [0.01],
        'p_adjusted': [0.03]
    })
    result = validate_correlation_test_d068(
        df,
        required_cols=['p_raw', 'p_adjusted']
    )

    # Custom required_cols present - should pass
    assert result['valid'] is True
    assert result['d068_compliant'] is True  # Assumes custom cols meet D068
    assert 'Custom validation' in result['message']


def test_validate_correlation_test_d068_multiple_correlations():
    """Test multiple correlation tests in DataFrame."""
    df = pd.DataFrame({
        'variable1': ['intercepts', 'intercepts'],
        'variable2': ['slopes', 'baseline_memory'],
        'r': [-0.45, 0.32],
        'p_uncorrected': [0.003, 0.012],
        'p_bonferroni': [0.045, 0.180]
    })
    result = validate_correlation_test_d068(df)

    assert result['valid'] is True
    assert result['d068_compliant'] is True
    assert '2 rows' in result['message'] or 'DataFrame' in result['message']


def test_validate_correlation_test_d068_realistic_rq513():
    """Test realistic RQ 5.13 scenario (intercept-slope correlation)."""
    df = pd.DataFrame({
        'r': [-0.42],
        'p_uncorrected': [0.0001],
        'p_bonferroni': [0.0015],  # 15 tests family-wise
        'significant_uncorrected': [True],
        'significant_bonferroni': [True],
        'interpretation': ['Strong negative correlation: Higher intercepts (better starters) associated with slower slopes (less forgetting)']
    })
    result = validate_correlation_test_d068(df)

    assert result['valid'] is True
    assert result['d068_compliant'] is True
    assert 'Decision D068 compliant' in result['message']
    assert 'p_bonferroni' in result['message']
