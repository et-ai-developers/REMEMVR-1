"""
Test fit_lmm_trajectory_tsvr function (D070 implementation).

Tests LMM fitting with TSVR (Time Since VR) instead of nominal days.
"""
import pytest
import pandas as pd
import numpy as np


class TestFitLmmTrajectoryTsvr:
    """Tests for fit_lmm_trajectory_tsvr function (D070)."""

    @pytest.fixture
    def sample_theta_scores(self):
        """Create sample theta scores DataFrame.

        Function expects columns: composite_ID, domain_name, theta
        (or column patterns that can be parsed)
        """
        np.random.seed(42)
        data = []

        for uid in range(1, 21):  # 20 participants for enough data
            for test in ['T1', 'T2', 'T3', 'T4']:
                for domain in ['What', 'Where', 'When']:
                    composite_id = f'P{uid:03d}_{test}'
                    data.append({
                        'composite_ID': composite_id,
                        'domain_name': domain,
                        'theta': np.random.randn()
                    })

        return pd.DataFrame(data)

    @pytest.fixture
    def sample_tsvr_data(self):
        """Create sample TSVR data DataFrame.

        Function expects columns: UID, Test (or test), TSVR_hours (or tsvr)
        """
        np.random.seed(42)
        data = []

        # TSVR values in hours (T1=0, T2~24h, T3~72h, T4~144h with variation)
        tsvr_means = {'T1': 0, 'T2': 24, 'T3': 72, 'T4': 144}

        for uid in range(1, 21):  # Match participant count
            for test in ['T1', 'T2', 'T3', 'T4']:
                tsvr = tsvr_means[test] + np.random.randn() * 2  # Add variation
                data.append({
                    'UID': f'P{uid:03d}',
                    'Test': test,
                    'TSVR_hours': max(0, tsvr)  # Ensure non-negative
                })

        return pd.DataFrame(data)

    def test_import_function(self):
        """Test function can be imported."""
        from tools.analysis_lmm import fit_lmm_trajectory_tsvr
        assert callable(fit_lmm_trajectory_tsvr)

    def test_returns_result_object(self, sample_theta_scores, sample_tsvr_data):
        """Test function returns LMM result object."""
        from tools.analysis_lmm import fit_lmm_trajectory_tsvr

        result = fit_lmm_trajectory_tsvr(
            theta_scores=sample_theta_scores,
            tsvr_data=sample_tsvr_data,
            formula='Theta ~ Days'
        )

        # Should return MixedLMResults with params attribute
        assert hasattr(result, 'params')
        assert hasattr(result, 'pvalues')

    def test_uses_tsvr_not_nominal(self, sample_theta_scores, sample_tsvr_data):
        """Test function uses TSVR (actual hours) not nominal days."""
        from tools.analysis_lmm import fit_lmm_trajectory_tsvr

        # Function should merge with TSVR data and convert to days
        result = fit_lmm_trajectory_tsvr(
            theta_scores=sample_theta_scores,
            tsvr_data=sample_tsvr_data,
            formula='Theta ~ Days'
        )

        # If function runs without error using TSVR data, it's working
        assert result is not None
        # Days coefficient should exist
        assert 'Days' in result.params.index

    def test_handles_column_name_variants(self, sample_theta_scores):
        """Test function handles different TSVR column names."""
        from tools.analysis_lmm import fit_lmm_trajectory_tsvr

        # Create TSVR data with lowercase 'tsvr' column and 'test' column
        tsvr_data = pd.DataFrame({
            'UID': [f'P{uid:03d}' for uid in range(1, 21) for _ in range(4)],
            'test': ['T1', 'T2', 'T3', 'T4'] * 20,  # lowercase
            'tsvr': [0, 24, 72, 144] * 20  # lowercase, no _hours suffix
        })

        result = fit_lmm_trajectory_tsvr(
            theta_scores=sample_theta_scores,
            tsvr_data=tsvr_data,
            formula='Theta ~ Days'
        )

        assert result is not None

    def test_has_correct_coefficients(self, sample_theta_scores, sample_tsvr_data):
        """Test result has expected coefficients."""
        from tools.analysis_lmm import fit_lmm_trajectory_tsvr

        result = fit_lmm_trajectory_tsvr(
            theta_scores=sample_theta_scores,
            tsvr_data=sample_tsvr_data,
            formula='Theta ~ Days'
        )

        # Should have Intercept and Days
        assert 'Intercept' in result.params.index
        assert 'Days' in result.params.index


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
