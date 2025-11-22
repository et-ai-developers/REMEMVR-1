"""
Test compute_contrasts_pairwise function (D068 implementation).

Tests dual p-value reporting (uncorrected and Bonferroni-corrected).
"""
import pytest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock


class TestComputeContrastsPairwise:
    """Tests for compute_contrasts_pairwise function (D068)."""

    @pytest.fixture
    def mock_lmm_result(self):
        """Create mock LMM result object.

        The function looks for coefficient names in these patterns:
        - C(Factor, Treatment)[T.{level}]
        - C(Factor)[T.{level}]
        - Factor[T.{level}]
        - C(Domain, Treatment)[T.{level}]
        - C(Domain)[T.{level}]
        - Domain[T.{level}]
        - {level} (bare level name)
        """
        mock = MagicMock()

        # Create params with Factor coefficients using patterns the function expects
        mock.params = pd.Series({
            'Intercept': 0.5,
            'Days': -0.1,
            'Factor[T.Factor2]': 0.2,
            'Factor[T.Factor3]': -0.1,
            'Days:Factor[T.Factor2]': 0.05,
            'Days:Factor[T.Factor3]': -0.03
        })

        # Create standard errors
        mock.bse = pd.Series({
            'Intercept': 0.05,
            'Days': 0.02,
            'Factor[T.Factor2]': 0.08,
            'Factor[T.Factor3]': 0.07,
            'Days:Factor[T.Factor2]': 0.01,
            'Days:Factor[T.Factor3]': 0.01
        })

        # Create p-values
        mock.pvalues = pd.Series({
            'Intercept': 0.001,
            'Days': 0.001,
            'Factor[T.Factor2]': 0.015,
            'Factor[T.Factor3]': 0.180,
            'Days:Factor[T.Factor2]': 0.001,
            'Days:Factor[T.Factor3]': 0.002
        })

        return mock

    def test_import_function(self):
        """Test function can be imported."""
        from tools.analysis_lmm import compute_contrasts_pairwise
        assert callable(compute_contrasts_pairwise)

    def test_returns_dataframe(self, mock_lmm_result):
        """Test function returns DataFrame."""
        from tools.analysis_lmm import compute_contrasts_pairwise

        result = compute_contrasts_pairwise(
            mock_lmm_result,
            comparisons=['Factor2-Factor1', 'Factor3-Factor1']
        )

        assert isinstance(result, pd.DataFrame)

    def test_has_dual_pvalues(self, mock_lmm_result):
        """Test output has both uncorrected and corrected p-values (D068)."""
        from tools.analysis_lmm import compute_contrasts_pairwise

        result = compute_contrasts_pairwise(
            mock_lmm_result,
            comparisons=['Factor2-Factor1']
        )

        # Check for dual p-value columns
        assert 'p_uncorrected' in result.columns
        assert 'p_corrected' in result.columns

    def test_has_significance_flags(self, mock_lmm_result):
        """Test output has significance indicator columns."""
        from tools.analysis_lmm import compute_contrasts_pairwise

        result = compute_contrasts_pairwise(
            mock_lmm_result,
            comparisons=['Factor2-Factor1']
        )

        # Should have significance indicator columns
        assert 'sig_uncorrected' in result.columns
        assert 'sig_corrected' in result.columns

    def test_bonferroni_correction_applied(self, mock_lmm_result):
        """Test Bonferroni correction is properly applied."""
        from tools.analysis_lmm import compute_contrasts_pairwise

        result = compute_contrasts_pairwise(
            mock_lmm_result,
            comparisons=['Factor2-Factor1', 'Factor3-Factor1'],
            family_alpha=0.05
        )

        # With 2 comparisons, corrected alpha = 0.05/2 = 0.025
        # alpha_corrected column should reflect this
        assert 'alpha_corrected' in result.columns
        assert all(result['alpha_corrected'] == 0.025)

    def test_custom_family_alpha(self, mock_lmm_result):
        """Test custom family_alpha parameter."""
        from tools.analysis_lmm import compute_contrasts_pairwise

        result = compute_contrasts_pairwise(
            mock_lmm_result,
            comparisons=['Factor2-Factor1'],
            family_alpha=0.10
        )

        # With 1 comparison and alpha=0.10, corrected alpha = 0.10
        assert result['alpha_corrected'].iloc[0] == 0.10

    def test_corrected_p_capped_at_one(self, mock_lmm_result):
        """Test corrected p-value is capped at 1.0."""
        from tools.analysis_lmm import compute_contrasts_pairwise

        result = compute_contrasts_pairwise(
            mock_lmm_result,
            comparisons=['Factor2-Factor1', 'Factor3-Factor1']
        )

        # All corrected p-values should be <= 1.0
        assert all(result['p_corrected'] <= 1.0)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
