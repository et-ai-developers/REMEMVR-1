"""
Test compute_effect_sizes_cohens function.

Tests Cohen's f^2 effect size calculation.
"""
import pytest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock


class TestComputeEffectSizesCohens:
    """Tests for compute_effect_sizes_cohens function."""

    @pytest.fixture
    def mock_lmm_result(self):
        """Create mock LMM result object.

        Function requires: params, bse, nobs
        """
        mock = MagicMock()

        mock.params = pd.Series({
            'Intercept': 0.5,
            'Days': -0.1,
            'Factor': 0.2,
            'Days:Factor': 0.05
        })

        mock.bse = pd.Series({
            'Intercept': 0.05,
            'Days': 0.02,
            'Factor': 0.08,
            'Days:Factor': 0.01
        })

        mock.nobs = 1000

        return mock

    def test_import_function(self):
        """Test function can be imported."""
        from tools.analysis_lmm import compute_effect_sizes_cohens
        assert callable(compute_effect_sizes_cohens)

    def test_returns_dataframe(self, mock_lmm_result):
        """Test function returns DataFrame."""
        from tools.analysis_lmm import compute_effect_sizes_cohens

        result = compute_effect_sizes_cohens(mock_lmm_result)

        assert isinstance(result, pd.DataFrame)

    def test_has_effect_size_column(self, mock_lmm_result):
        """Test output has effect size column."""
        from tools.analysis_lmm import compute_effect_sizes_cohens

        result = compute_effect_sizes_cohens(mock_lmm_result)

        # Column should be f_squared
        assert 'f_squared' in result.columns

    def test_has_interpretation_column(self, mock_lmm_result):
        """Test output has effect size interpretation."""
        from tools.analysis_lmm import compute_effect_sizes_cohens

        result = compute_effect_sizes_cohens(mock_lmm_result)

        # Should have interpretation column
        assert 'interpretation' in result.columns

    def test_effect_sizes_non_negative(self, mock_lmm_result):
        """Test effect sizes are non-negative."""
        from tools.analysis_lmm import compute_effect_sizes_cohens

        result = compute_effect_sizes_cohens(mock_lmm_result, include_interactions=True)

        # All f_squared values should be >= 0
        assert all(result['f_squared'] >= 0)

    def test_include_interactions_parameter(self, mock_lmm_result):
        """Test include_interactions parameter."""
        from tools.analysis_lmm import compute_effect_sizes_cohens

        result_with = compute_effect_sizes_cohens(
            mock_lmm_result,
            include_interactions=True
        )

        result_without = compute_effect_sizes_cohens(
            mock_lmm_result,
            include_interactions=False
        )

        # With interactions should have more rows (Days:Factor included)
        assert len(result_with) > len(result_without)

    def test_excludes_intercept(self, mock_lmm_result):
        """Test Intercept is excluded from results."""
        from tools.analysis_lmm import compute_effect_sizes_cohens

        result = compute_effect_sizes_cohens(mock_lmm_result, include_interactions=True)

        # Intercept should not be in effect column
        assert 'Intercept' not in result['effect'].values

    def test_interpretation_values(self, mock_lmm_result):
        """Test interpretation values are valid."""
        from tools.analysis_lmm import compute_effect_sizes_cohens

        result = compute_effect_sizes_cohens(mock_lmm_result, include_interactions=True)

        # All interpretations should be one of expected values
        valid_interpretations = {'negligible', 'small', 'medium', 'large'}
        assert all(i in valid_interpretations for i in result['interpretation'])


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
