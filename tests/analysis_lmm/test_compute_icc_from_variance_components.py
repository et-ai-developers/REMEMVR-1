"""
Tests for compute_icc_from_variance_components function (Tool 7/25)

Purpose: Compute 3 ICC estimates for RQ 5.13 variance decomposition
TDD Status: RED phase (tests written first)
"""

import pytest
import pandas as pd
import numpy as np
from tools.analysis_lmm import compute_icc_from_variance_components


@pytest.fixture
def mock_variance_components():
    """Create mock variance components DataFrame"""
    return pd.DataFrame({
        'component': ['Intercept', 'TSVR_hours', 'Residual'],
        'variance': [0.25, 0.10, 0.15]
    })


def test_basic_structure(mock_variance_components):
    """Test output has required structure"""
    result = compute_icc_from_variance_components(mock_variance_components)

    assert isinstance(result, pd.DataFrame)
    assert 'icc_type' in result.columns
    assert 'icc_value' in result.columns
    assert len(result) == 3  # 3 ICC estimates


def test_icc_types_present(mock_variance_components):
    """Test all 3 ICC types are computed"""
    result = compute_icc_from_variance_components(mock_variance_components)

    icc_types = result['icc_type'].tolist()
    assert 'intercept' in icc_types
    assert 'slope_simple' in icc_types
    assert 'slope_conditional' in icc_types


def test_icc_bounds(mock_variance_components):
    """Test ICC values are in [0, 1] range"""
    result = compute_icc_from_variance_components(mock_variance_components)

    assert (result['icc_value'] >= 0).all()
    assert (result['icc_value'] <= 1).all()


def test_icc_intercept_formula(mock_variance_components):
    """Test ICC_intercept = var_intercept / (var_intercept + var_residual)"""
    result = compute_icc_from_variance_components(mock_variance_components)

    # Manual calculation
    var_intercept = 0.25
    var_residual = 0.15
    expected_icc = var_intercept / (var_intercept + var_residual)

    icc_intercept = result[result['icc_type'] == 'intercept']['icc_value'].iloc[0]
    np.testing.assert_almost_equal(icc_intercept, expected_icc, decimal=5)


def test_icc_slope_simple_formula(mock_variance_components):
    """Test ICC_slope_simple = var_slope / (var_slope + var_residual)"""
    result = compute_icc_from_variance_components(mock_variance_components)

    # Manual calculation
    var_slope = 0.10
    var_residual = 0.15
    expected_icc = var_slope / (var_slope + var_residual)

    icc_slope = result[result['icc_type'] == 'slope_simple']['icc_value'].iloc[0]
    np.testing.assert_almost_equal(icc_slope, expected_icc, decimal=5)


def test_icc_conditional_at_timepoint(mock_variance_components):
    """Test ICC_slope_conditional accounts for covariance at specific time"""
    # Add covariance to test data
    variance_df = pd.DataFrame({
        'component': ['Intercept', 'TSVR_hours', 'Intercept:TSVR_hours', 'Residual'],
        'variance': [0.25, 0.10, -0.05, 0.15]  # Negative covariance
    })

    result = compute_icc_from_variance_components(
        variance_df,
        time_point=6.0  # Day 6 (144 hours)
    )

    # ICC_conditional should differ from ICC_simple when covariance present
    icc_simple = result[result['icc_type'] == 'slope_simple']['icc_value'].iloc[0]
    icc_conditional = result[result['icc_type'] == 'slope_conditional']['icc_value'].iloc[0]

    # Should be different when covariance non-zero
    assert icc_simple != icc_conditional


def test_high_icc_interpretation(mock_variance_components):
    """Test high ICC values (>0.75) interpreted as high clustering"""
    # Create data with high between-subject variance
    variance_df = pd.DataFrame({
        'component': ['Intercept', 'TSVR_hours', 'Residual'],
        'variance': [0.80, 0.60, 0.10]  # High variance, low residual
    })

    result = compute_icc_from_variance_components(variance_df)

    # Both ICCs should be high (>0.75)
    assert all(result['icc_value'] > 0.75)


def test_low_icc_interpretation():
    """Test low ICC values (<0.10) indicate little clustering"""
    # Create data with low between-subject variance
    variance_df = pd.DataFrame({
        'component': ['Intercept', 'TSVR_hours', 'Residual'],
        'variance': [0.05, 0.03, 0.90]  # Low variance, high residual
    })

    result = compute_icc_from_variance_components(variance_df)

    # Both ICCs should be low (<0.10)
    assert all(result['icc_value'] < 0.10)


def test_interpretation_column_present(mock_variance_components):
    """Test interpretation strings are provided"""
    result = compute_icc_from_variance_components(mock_variance_components)

    assert 'interpretation' in result.columns
    assert result['interpretation'].notna().all()


def test_zero_variance_handling():
    """Test handles zero variance components gracefully"""
    variance_df = pd.DataFrame({
        'component': ['Intercept', 'TSVR_hours', 'Residual'],
        'variance': [0.0, 0.10, 0.15]  # Zero intercept variance
    })

    result = compute_icc_from_variance_components(variance_df)

    # ICC_intercept should be 0
    icc_intercept = result[result['icc_type'] == 'intercept']['icc_value'].iloc[0]
    assert icc_intercept == 0.0


def test_component_name_variations():
    """Test handles different component naming conventions"""
    # Alternative naming (slope vs TSVR_hours)
    variance_df = pd.DataFrame({
        'component': ['Intercept', 'slope', 'Residual'],
        'variance': [0.25, 0.10, 0.15]
    })

    result = compute_icc_from_variance_components(
        variance_df,
        slope_name='slope'  # Custom slope component name
    )

    assert len(result) == 3


def test_output_sorted_by_icc_type(mock_variance_components):
    """Test output is sorted by ICC type for consistency"""
    result = compute_icc_from_variance_components(mock_variance_components)

    # Check order: intercept, slope_conditional, slope_simple (alphabetical)
    icc_types = result['icc_type'].tolist()
    assert icc_types == sorted(icc_types)


def test_no_slope_variance_provided():
    """Test handles missing slope variance (intercept-only model)"""
    variance_df = pd.DataFrame({
        'component': ['Intercept', 'Residual'],
        'variance': [0.25, 0.15]
    })

    result = compute_icc_from_variance_components(variance_df)

    # Should only compute ICC_intercept
    assert len(result) == 1
    assert result['icc_type'].iloc[0] == 'intercept'


def test_realistic_rq513_values():
    """Test with realistic RQ 5.13 variance values"""
    # Example from longitudinal memory study
    variance_df = pd.DataFrame({
        'component': ['Intercept', 'TSVR_hours', 'Intercept:TSVR_hours', 'Residual'],
        'variance': [0.45, 0.08, -0.03, 0.22]
    })

    result = compute_icc_from_variance_components(
        variance_df,
        time_point=144.0  # Day 6
    )

    # All ICCs should be in valid range [0, 1]
    assert all((result['icc_value'] >= 0.0) & (result['icc_value'] <= 1.0))
    # At least one ICC should be moderate or higher (>0.1)
    assert any(result['icc_value'] > 0.1)
