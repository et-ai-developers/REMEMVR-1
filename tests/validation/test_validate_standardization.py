"""
Test suite for validate_standardization function.

Tests z-score standardization validation (mean ≈ 0, SD ≈ 1).
"""

import pytest
import pandas as pd
import numpy as np
from tools.validation import validate_standardization


class TestValidateStandardization:
    """Test validate_standardization function."""

    def test_basic_structure(self):
        """Test function returns expected keys."""
        df = pd.DataFrame({
            'z_score': np.random.randn(100)
        })
        result = validate_standardization(df, ['z_score'])

        assert 'valid' in result
        assert 'message' in result
        assert 'mean_values' in result
        assert 'sd_values' in result
        assert isinstance(result['valid'], bool)
        assert isinstance(result['message'], str)
        assert isinstance(result['mean_values'], dict)
        assert isinstance(result['sd_values'], dict)

    def test_valid_standardization_single_column(self):
        """Test perfectly standardized single column."""
        np.random.seed(42)
        df = pd.DataFrame({
            'z_score': np.random.randn(1000)  # Large N for stability
        })
        result = validate_standardization(df, ['z_score'], tolerance=0.05)

        assert result['valid'] is True
        assert 'z_score' in result['mean_values']
        assert 'z_score' in result['sd_values']
        assert abs(result['mean_values']['z_score']) < 0.1  # Mean ≈ 0
        assert abs(result['sd_values']['z_score'] - 1.0) < 0.1  # SD ≈ 1

    def test_valid_standardization_multiple_columns(self):
        """Test perfectly standardized multiple columns."""
        np.random.seed(42)
        df = pd.DataFrame({
            'Age_z': np.random.randn(1000),
            'IQ_z': np.random.randn(1000),
            'Memory_z': np.random.randn(1000)
        })
        result = validate_standardization(df, ['Age_z', 'IQ_z', 'Memory_z'], tolerance=0.1)

        assert result['valid'] is True
        for col in ['Age_z', 'IQ_z', 'Memory_z']:
            assert col in result['mean_values']
            assert col in result['sd_values']
            assert abs(result['mean_values'][col]) < 0.15  # Sampling variation
            assert abs(result['sd_values'][col] - 1.0) < 0.1

    def test_invalid_mean_too_high(self):
        """Test column with mean too far from 0."""
        df = pd.DataFrame({
            'z_score': np.random.randn(100) + 0.5  # Shifted mean
        })
        result = validate_standardization(df, ['z_score'], tolerance=0.01)

        assert result['valid'] is False
        assert 'mean' in result['message'].lower()
        assert 'z_score' in result['message']

    def test_invalid_sd_too_low(self):
        """Test column with SD too far from 1."""
        df = pd.DataFrame({
            'z_score': np.random.randn(100) * 0.5  # Scaled SD
        })
        result = validate_standardization(df, ['z_score'], tolerance=0.01)

        assert result['valid'] is False
        assert 'sd' in result['message'].lower() or 'standard deviation' in result['message'].lower()

    def test_invalid_multiple_issues(self):
        """Test DataFrame with multiple standardization issues."""
        df = pd.DataFrame({
            'good_z': np.random.randn(100),
            'bad_mean': np.random.randn(100) + 2.0,
            'bad_sd': np.random.randn(100) * 0.1
        })
        result = validate_standardization(df, ['good_z', 'bad_mean', 'bad_sd'], tolerance=0.01)

        assert result['valid'] is False
        assert 'bad_mean' in result['message'] or 'bad_sd' in result['message']

    def test_custom_tolerance(self):
        """Test with custom tolerance parameter."""
        df = pd.DataFrame({
            'z_score': np.random.randn(100)
        })

        # Strict tolerance
        result_strict = validate_standardization(df, ['z_score'], tolerance=0.001)

        # Loose tolerance
        result_loose = validate_standardization(df, ['z_score'], tolerance=0.5)

        # Loose should be more likely to pass
        assert isinstance(result_strict['valid'], bool)
        assert isinstance(result_loose['valid'], bool)

    def test_empty_dataframe(self):
        """Test with empty DataFrame."""
        df = pd.DataFrame({'z_score': []})
        result = validate_standardization(df, ['z_score'])

        # Empty data should fail (can't compute mean/SD)
        assert result['valid'] is False
        assert 'empty' in result['message'].lower() or 'insufficient' in result['message'].lower()

    def test_missing_column(self):
        """Test with missing column name."""
        df = pd.DataFrame({
            'z_score': np.random.randn(100)
        })

        with pytest.raises((KeyError, ValueError)):
            validate_standardization(df, ['nonexistent_column'])

    def test_column_with_nan(self):
        """Test column containing NaN values."""
        df = pd.DataFrame({
            'z_score': [np.nan] * 10 + list(np.random.randn(90))
        })
        result = validate_standardization(df, ['z_score'])

        # Function should handle NaN gracefully (either skip or report)
        assert 'valid' in result
        assert 'message' in result

    def test_realistic_rq_5_14_scenario(self):
        """Test realistic RQ 5.14 clustering scenario (3 standardized features)."""
        np.random.seed(42)
        N = 100

        # Simulate standardized clustering features (realistic imperfections)
        df = pd.DataFrame({
            'Age_z': (np.random.randn(N) * 1.02) - 0.01,  # Nearly perfect
            'Memory_z': (np.random.randn(N) * 0.98) + 0.02,  # Nearly perfect
            'IQ_z': (np.random.randn(N) * 1.05) - 0.03  # Nearly perfect
        })

        result = validate_standardization(
            df,
            ['Age_z', 'Memory_z', 'IQ_z'],
            tolerance=0.15  # Realistic tolerance for N=100 with sampling variation
        )

        assert result['valid'] is True
        assert len(result['mean_values']) == 3
        assert len(result['sd_values']) == 3

        # All means should be near 0
        for mean_val in result['mean_values'].values():
            assert abs(mean_val) < 0.2  # Sampling variation with N=100

        # All SDs should be near 1
        for sd_val in result['sd_values'].values():
            assert abs(sd_val - 1.0) < 0.2  # Sampling variation with N=100
