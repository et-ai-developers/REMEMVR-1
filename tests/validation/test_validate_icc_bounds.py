"""
Test suite for validate_icc_bounds function.

Tests ICC bounds validation (all values in [0,1]).
"""

import pytest
import pandas as pd
import numpy as np
from tools.validation import validate_icc_bounds


class TestValidateIccBounds:
    """Test validate_icc_bounds function."""

    def test_basic_structure(self):
        """Test function returns expected keys."""
        df = pd.DataFrame({
            'icc_type': ['intercept', 'slope'],
            'icc_value': [0.45, 0.23]
        })
        result = validate_icc_bounds(df, 'icc_value')

        assert 'valid' in result
        assert 'message' in result
        assert 'out_of_bounds' in result
        assert isinstance(result['valid'], bool)
        assert isinstance(result['message'], str)
        assert isinstance(result['out_of_bounds'], list)

    def test_valid_all_in_bounds(self):
        """Test DataFrame with all ICC values in [0,1]."""
        df = pd.DataFrame({
            'icc_type': ['intercept', 'slope', 'conditional'],
            'icc_value': [0.45, 0.23, 0.67]
        })
        result = validate_icc_bounds(df, 'icc_value')

        assert result['valid'] is True
        assert len(result['out_of_bounds']) == 0

    def test_valid_boundary_values(self):
        """Test boundary values 0.0 and 1.0 (valid)."""
        df = pd.DataFrame({
            'icc_type': ['zero_var', 'perfect_correlation'],
            'icc_value': [0.0, 1.0]
        })
        result = validate_icc_bounds(df, 'icc_value')

        assert result['valid'] is True
        assert len(result['out_of_bounds']) == 0

    def test_invalid_below_zero(self):
        """Test ICC value below 0 (invalid)."""
        df = pd.DataFrame({
            'icc_type': ['intercept', 'slope'],
            'icc_value': [0.45, -0.1]
        })
        result = validate_icc_bounds(df, 'icc_value')

        assert result['valid'] is False
        assert len(result['out_of_bounds']) == 1
        assert result['out_of_bounds'][0]['icc_value'] == -0.1

    def test_invalid_above_one(self):
        """Test ICC value above 1 (invalid)."""
        df = pd.DataFrame({
            'icc_type': ['intercept', 'slope'],
            'icc_value': [1.2, 0.5]
        })
        result = validate_icc_bounds(df, 'icc_value')

        assert result['valid'] is False
        assert len(result['out_of_bounds']) == 1
        assert result['out_of_bounds'][0]['icc_value'] == 1.2

    def test_invalid_multiple_out_of_bounds(self):
        """Test multiple ICC values out of bounds."""
        df = pd.DataFrame({
            'icc_type': ['intercept', 'slope', 'conditional'],
            'icc_value': [-0.1, 0.5, 1.5]
        })
        result = validate_icc_bounds(df, 'icc_value')

        assert result['valid'] is False
        assert len(result['out_of_bounds']) == 2

    def test_custom_icc_column_name(self):
        """Test with custom ICC column name."""
        df = pd.DataFrame({
            'type': ['a', 'b'],
            'correlation': [0.3, 0.7]
        })
        result = validate_icc_bounds(df, 'correlation')

        assert result['valid'] is True

    def test_empty_dataframe(self):
        """Test with empty DataFrame."""
        df = pd.DataFrame({'icc_value': []})
        result = validate_icc_bounds(df, 'icc_value')

        assert result['valid'] is False
        assert 'empty' in result['message'].lower()

    def test_nan_value(self):
        """Test ICC with NaN value (invalid)."""
        df = pd.DataFrame({
            'icc_type': ['intercept', 'slope'],
            'icc_value': [0.45, np.nan]
        })
        result = validate_icc_bounds(df, 'icc_value')

        assert result['valid'] is False
        assert len(result['out_of_bounds']) == 1

    def test_realistic_rq_5_13_scenario(self):
        """Test realistic RQ 5.13 ICC estimates scenario."""
        # Typical ICC estimates from compute_icc_from_variance_components
        df = pd.DataFrame({
            'icc_type': ['ICC_intercept', 'ICC_slope_simple', 'ICC_slope_conditional'],
            'icc_value': [0.611, 0.071, 0.543],
            'interpretation': ['High', 'Low', 'Moderate']
        })

        result = validate_icc_bounds(df, 'icc_value')

        assert result['valid'] is True
        assert len(result['out_of_bounds']) == 0
        assert '3 ICC values' in result['message']
