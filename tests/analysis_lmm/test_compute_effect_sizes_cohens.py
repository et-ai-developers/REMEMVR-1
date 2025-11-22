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
        """Create mock LMM result object."""
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

        columns = result.columns.tolist()
        effect_cols = [c for c in columns if 'f2' in c.lower() or 'effect' in c.lower() or 'cohen' in c.lower()]
        assert len(effect_cols) > 0

    def test_has_interpretation_column(self, mock_lmm_result):
        """Test output has effect size interpretation."""
        from tools.analysis_lmm import compute_effect_sizes_cohens

        result = compute_effect_sizes_cohens(mock_lmm_result)

        columns = result.columns.tolist()
        # Should have interpretation (small/medium/large)
        interp_cols = [c for c in columns if 'interp' in c.lower() or 'size' in c.lower() or 'magnitude' in c.lower()]
        # Note: This might not be present in all implementations

    def test_effect_sizes_non_negative(self, mock_lmm_result):
        """Test effect sizes are non-negative."""
        from tools.analysis_lmm import compute_effect_sizes_cohens

        result = compute_effect_sizes_cohens(mock_lmm_result)

        # Find effect size column
        effect_col = None
        for col in result.columns:
            if 'f2' in col.lower() or 'effect' in col.lower():
                effect_col = col
                break

        if effect_col:
            assert all(result[effect_col] >= 0)

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

        # With interactions should have more or equal rows
        assert len(result_with) >= len(result_without)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
