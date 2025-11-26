"""
Test suite for validate_variance_positivity function.

Tests variance component validation (all values > 0).
"""

import pytest
import pandas as pd
import numpy as np
from tools.validation import validate_variance_positivity


class TestValidateVariancePositivity:
    """Test validate_variance_positivity function."""

    def test_basic_structure(self):
        """Test function returns expected keys."""
        df = pd.DataFrame({
            'component': ['Intercept', 'Slope', 'Residual'],
            'variance': [1.5, 0.8, 0.3]
        })
        result = validate_variance_positivity(df, 'component', 'variance')

        assert 'valid' in result
        assert 'message' in result
        assert 'negative_components' in result
        assert isinstance(result['valid'], bool)
        assert isinstance(result['message'], str)
        assert isinstance(result['negative_components'], list)

    def test_valid_all_positive(self):
        """Test DataFrame with all positive variances."""
        df = pd.DataFrame({
            'component': ['Intercept', 'Slope', 'Residual'],
            'variance': [1.5, 0.8, 0.3]
        })
        result = validate_variance_positivity(df, 'component', 'variance')

        assert result['valid'] is True
        assert len(result['negative_components']) == 0
        assert '3 components' in result['message']

    def test_valid_small_positive(self):
        """Test DataFrame with very small but positive variances."""
        df = pd.DataFrame({
            'component': ['Intercept', 'Slope'],
            'variance': [0.001, 0.0001]
        })
        result = validate_variance_positivity(df, 'component', 'variance')

        assert result['valid'] is True
        assert len(result['negative_components']) == 0

    def test_invalid_single_negative(self):
        """Test DataFrame with one negative variance."""
        df = pd.DataFrame({
            'component': ['Intercept', 'Slope', 'Residual'],
            'variance': [1.5, -0.2, 0.3]
        })
        result = validate_variance_positivity(df, 'component', 'variance')

        assert result['valid'] is False
        assert len(result['negative_components']) == 1
        assert 'Slope' in result['negative_components']
        assert 'Slope' in result['message']

    def test_invalid_multiple_negative(self):
        """Test DataFrame with multiple negative variances."""
        df = pd.DataFrame({
            'component': ['Intercept', 'Slope', 'Residual'],
            'variance': [-0.5, -0.2, 0.3]
        })
        result = validate_variance_positivity(df, 'component', 'variance')

        assert result['valid'] is False
        assert len(result['negative_components']) == 2
        assert 'Intercept' in result['negative_components']
        assert 'Slope' in result['negative_components']

    def test_invalid_zero_variance(self):
        """Test DataFrame with zero variance (invalid)."""
        df = pd.DataFrame({
            'component': ['Intercept', 'Slope'],
            'variance': [1.5, 0.0]
        })
        result = validate_variance_positivity(df, 'component', 'variance')

        assert result['valid'] is False
        assert 'Slope' in result['negative_components']
        assert 'zero or negative' in result['message'].lower()

    def test_custom_column_names(self):
        """Test with custom column names."""
        df = pd.DataFrame({
            'var_name': ['Random Effect 1', 'Random Effect 2'],
            'var_value': [2.3, 1.1]
        })
        result = validate_variance_positivity(df, 'var_name', 'var_value')

        assert result['valid'] is True

    def test_empty_dataframe(self):
        """Test with empty DataFrame."""
        df = pd.DataFrame({
            'component': [],
            'variance': []
        })
        result = validate_variance_positivity(df, 'component', 'variance')

        assert result['valid'] is False
        assert 'empty' in result['message'].lower()

    def test_missing_column_name(self):
        """Test with missing component column."""
        df = pd.DataFrame({
            'component': ['Intercept'],
            'variance': [1.5]
        })

        with pytest.raises(KeyError):
            validate_variance_positivity(df, 'wrong_col', 'variance')

    def test_missing_value_column(self):
        """Test with missing variance column."""
        df = pd.DataFrame({
            'component': ['Intercept'],
            'variance': [1.5]
        })

        with pytest.raises(KeyError):
            validate_variance_positivity(df, 'component', 'wrong_col')

    def test_realistic_rq_5_13_scenario(self):
        """Test realistic RQ 5.13 variance components scenario."""
        # Typical LMM variance components for RQ 5.13
        df = pd.DataFrame({
            'Component': ['Group Var', 'Group x TSVR_hours Var', 'Residual'],
            'Variance': [0.245, 0.012, 0.156]
        })

        result = validate_variance_positivity(df, 'Component', 'Variance')

        assert result['valid'] is True
        assert len(result['negative_components']) == 0
        assert 'positive variance' in result['message'].lower()
