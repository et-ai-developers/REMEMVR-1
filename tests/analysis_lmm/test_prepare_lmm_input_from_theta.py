"""
Test prepare_lmm_input_from_theta function.

Tests conversion of theta scores to LMM-ready format.
Note: This function is DEPRECATED per Decision D070 - use fit_lmm_trajectory_tsvr instead.
"""
import pytest
import pandas as pd
import numpy as np
import warnings

from tools.analysis_lmm import prepare_lmm_input_from_theta


class TestPrepareLmmInputFromTheta:
    """Tests for prepare_lmm_input_from_theta function."""

    @pytest.fixture
    def sample_theta_scores(self):
        """Create sample theta scores DataFrame (wide format)."""
        data = []
        for uid in ['P001', 'P002', 'P003']:
            for test in ['T1', 'T2', 'T3', 'T4']:
                composite_id = f"{uid}_{test}"
                data.append({
                    'composite_ID': composite_id,
                    'Factor1_Theta': np.random.randn(),
                    'Factor2_Theta': np.random.randn()
                })
        return pd.DataFrame(data)

    def test_returns_dataframe(self, sample_theta_scores):
        """Test function returns DataFrame."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            result = prepare_lmm_input_from_theta(sample_theta_scores)

        assert isinstance(result, pd.DataFrame)

    def test_emits_deprecation_warning(self, sample_theta_scores):
        """Test function emits DeprecationWarning per D070."""
        with pytest.warns(DeprecationWarning):
            prepare_lmm_input_from_theta(sample_theta_scores)

    def test_output_is_long_format(self, sample_theta_scores):
        """Test output is melted to long format."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            result = prepare_lmm_input_from_theta(sample_theta_scores)

        # Long format should have Factor and Theta columns
        assert 'Factor' in result.columns or 'Domain' in result.columns
        assert 'Theta' in result.columns

    def test_output_has_time_variable(self, sample_theta_scores):
        """Test output has time variable (Days or similar)."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            result = prepare_lmm_input_from_theta(sample_theta_scores)

        # Should have some time variable
        time_cols = [c for c in result.columns if 'Day' in c or 'Time' in c or 'Test' in c]
        assert len(time_cols) > 0 or 'test' in result.columns.str.lower().tolist()

    def test_preserves_uid_info(self, sample_theta_scores):
        """Test UID information is preserved."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            result = prepare_lmm_input_from_theta(sample_theta_scores)

        # Should have UID or be derivable from composite_ID
        assert 'UID' in result.columns or 'composite_ID' in result.columns

    def test_factors_parameter(self, sample_theta_scores):
        """Test factors parameter filters output."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            result = prepare_lmm_input_from_theta(
                sample_theta_scores,
                factors=['Factor1']
            )

        # Should only have Factor1 data
        if 'Factor' in result.columns:
            assert set(result['Factor'].unique()) == {'Factor1'}


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
