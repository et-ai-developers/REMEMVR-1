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
        """Create sample theta scores DataFrame (wide format).

        Function expects columns: UID, test, Theta_* (e.g., Theta_What, Theta_Where)
        """
        data = []
        for uid in ['P001', 'P002', 'P003']:
            for test in [1, 2, 3, 4]:  # Function expects integer test
                data.append({
                    'UID': uid,
                    'test': test,
                    'Theta_What': np.random.randn(),
                    'Theta_Where': np.random.randn()
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
        with pytest.warns(DeprecationWarning, match="TSVR"):
            prepare_lmm_input_from_theta(sample_theta_scores)

    def test_output_is_long_format(self, sample_theta_scores):
        """Test output is melted to long format."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            result = prepare_lmm_input_from_theta(sample_theta_scores)

        # Long format should have Factor and Ability columns
        assert 'Factor' in result.columns
        assert 'Ability' in result.columns

    def test_output_has_time_variable(self, sample_theta_scores):
        """Test output has time variable (Days)."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            result = prepare_lmm_input_from_theta(sample_theta_scores)

        # Should have Days variable
        assert 'Days' in result.columns
        # Should also have Days_sq and log_Days
        assert 'Days_sq' in result.columns
        assert 'log_Days' in result.columns

    def test_preserves_uid_info(self, sample_theta_scores):
        """Test UID information is preserved."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            result = prepare_lmm_input_from_theta(sample_theta_scores)

        # Should have UID column
        assert 'UID' in result.columns
        # Check UIDs are preserved
        assert set(result['UID'].unique()) == {'P001', 'P002', 'P003'}

    def test_factors_parameter(self, sample_theta_scores):
        """Test factors parameter filters output."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            result = prepare_lmm_input_from_theta(
                sample_theta_scores,
                factors=['Theta_What']
            )

        # Should only have What factor (prefix removed)
        assert set(result['Factor'].unique()) == {'What'}

    def test_correct_day_mapping(self, sample_theta_scores):
        """Test days are mapped correctly from test number."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            result = prepare_lmm_input_from_theta(sample_theta_scores)

        # Day mapping: {1: 0, 2: 1, 3: 3, 4: 6}
        day_values = set(result['Days'].unique())
        expected_days = {0, 1, 3, 6}
        assert day_values == expected_days


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
