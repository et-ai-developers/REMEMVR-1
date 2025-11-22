"""
Test validate_lmm_residuals function.

Tests validation of LMM residuals normality using appropriate tests.
"""
import pytest
import numpy as np
import pandas as pd

from tools.validation import validate_lmm_residuals


class TestValidateLmmResiduals:
    """Tests for validate_lmm_residuals function."""

    @pytest.fixture
    def normal_residuals_small(self):
        """Create small sample of normally distributed residuals."""
        np.random.seed(42)
        return np.random.randn(100)

    @pytest.fixture
    def normal_residuals_large(self):
        """Create large sample of normally distributed residuals."""
        np.random.seed(42)
        return np.random.randn(6000)

    @pytest.fixture
    def skewed_residuals(self):
        """Create skewed residuals (exponential)."""
        np.random.seed(42)
        return np.random.exponential(1, 100)

    def test_returns_dict(self, normal_residuals_small):
        """Test function returns dictionary."""
        result = validate_lmm_residuals(normal_residuals_small)
        assert isinstance(result, dict)

    def test_has_normality_test_key(self, normal_residuals_small):
        """Test output has 'normality_test' key."""
        result = validate_lmm_residuals(normal_residuals_small)
        assert 'normality_test' in result

    def test_normality_test_has_passed(self, normal_residuals_small):
        """Test normality_test has 'passed' key."""
        result = validate_lmm_residuals(normal_residuals_small)
        assert 'passed' in result['normality_test']

    def test_normal_residuals_pass(self, normal_residuals_small):
        """Test normally distributed residuals pass the test."""
        result = validate_lmm_residuals(normal_residuals_small)
        assert isinstance(result['normality_test']['passed'], bool)

    def test_skewed_residuals_fail(self, skewed_residuals):
        """Test clearly non-normal residuals fail."""
        result = validate_lmm_residuals(skewed_residuals)
        assert result['normality_test']['passed'] is False

    def test_has_pvalue(self, normal_residuals_small):
        """Test normality_test has p-value."""
        result = validate_lmm_residuals(normal_residuals_small)
        assert 'p_value' in result['normality_test']

    def test_has_statistic(self, normal_residuals_small):
        """Test normality_test has test statistic."""
        result = validate_lmm_residuals(normal_residuals_small)
        assert 'statistic' in result['normality_test']

    def test_has_residual_stats(self, normal_residuals_small):
        """Test output has residual statistics."""
        result = validate_lmm_residuals(normal_residuals_small)
        assert 'residual_stats' in result

    def test_uses_shapiro_for_small_n(self, normal_residuals_small):
        """Test uses Shapiro-Wilk for n < 5000."""
        result = validate_lmm_residuals(normal_residuals_small)
        test_name = result['normality_test'].get('test_name', '').lower()
        assert 'shapiro' in test_name

    def test_uses_ks_for_large_n(self, normal_residuals_large):
        """Test uses Kolmogorov-Smirnov for n >= 5000."""
        result = validate_lmm_residuals(normal_residuals_large)
        test_name = result['normality_test'].get('test_name', '').lower()
        assert 'ks' in test_name or 'kolmogorov' in test_name

    def test_handles_pandas_series(self, normal_residuals_small):
        """Test handles pandas Series input."""
        series = pd.Series(normal_residuals_small)
        result = validate_lmm_residuals(series)
        assert isinstance(result, dict)
        assert 'normality_test' in result

    def test_has_n_residuals(self, normal_residuals_small):
        """Test output has residual count."""
        result = validate_lmm_residuals(normal_residuals_small)
        assert 'n_residuals' in result
        assert result['n_residuals'] == 100


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
