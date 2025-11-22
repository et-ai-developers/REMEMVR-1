"""
Test extract_fixed_effects_from_lmm function.

Tests extraction of fixed effects table from LMM results.
"""
import pytest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock


class TestExtractFixedEffectsFromLmm:
    """Tests for extract_fixed_effects_from_lmm function."""

    @pytest.fixture
    def mock_lmm_result(self):
        """Create mock LMM result object."""
        mock = MagicMock()

        # Create summary that returns tables
        summary_mock = MagicMock()

        # Create a DataFrame-like table
        table_data = pd.DataFrame({
            'Coef.': [0.5, -0.1, 0.2],
            'Std.Err.': [0.05, 0.02, 0.08],
            'z': [10.0, -5.0, 2.5],
            'P>|z|': [0.001, 0.001, 0.015],
            '[0.025': [0.4, -0.14, 0.04],
            '0.975]': [0.6, -0.06, 0.36]
        }, index=['Intercept', 'Days', 'Factor'])

        summary_mock.tables = [None, table_data]  # tables[1] is fixed effects
        mock.summary.return_value = summary_mock

        return mock

    def test_import_function(self):
        """Test function can be imported."""
        from tools.analysis_lmm import extract_fixed_effects_from_lmm
        assert callable(extract_fixed_effects_from_lmm)

    def test_returns_dataframe(self, mock_lmm_result):
        """Test function returns DataFrame."""
        from tools.analysis_lmm import extract_fixed_effects_from_lmm

        result = extract_fixed_effects_from_lmm(mock_lmm_result)

        assert isinstance(result, pd.DataFrame)

    def test_has_coefficient_column(self, mock_lmm_result):
        """Test output has coefficient/estimate column."""
        from tools.analysis_lmm import extract_fixed_effects_from_lmm

        result = extract_fixed_effects_from_lmm(mock_lmm_result)

        columns = [c.lower() for c in result.columns.tolist()]
        coef_cols = [c for c in columns if 'coef' in c or 'estimate' in c or 'beta' in c]
        assert len(coef_cols) > 0

    def test_has_standard_error(self, mock_lmm_result):
        """Test output has standard error column."""
        from tools.analysis_lmm import extract_fixed_effects_from_lmm

        result = extract_fixed_effects_from_lmm(mock_lmm_result)

        columns = [c.lower() for c in result.columns.tolist()]
        se_cols = [c for c in columns if 'std' in c or 'se' in c or 'err' in c]
        assert len(se_cols) > 0

    def test_has_pvalue(self, mock_lmm_result):
        """Test output has p-value column."""
        from tools.analysis_lmm import extract_fixed_effects_from_lmm

        result = extract_fixed_effects_from_lmm(mock_lmm_result)

        columns = [c.lower() for c in result.columns.tolist()]
        p_cols = [c for c in columns if 'p' in c or 'sig' in c]
        assert len(p_cols) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
