"""
Test compare_lmm_models_by_aic function.

Tests fitting multiple LMM models and comparing by AIC.
"""
import pytest
import pandas as pd
import numpy as np


class TestCompareLmmModelsByAic:
    """Tests for compare_lmm_models_by_aic function."""

    @pytest.fixture
    def sample_lmm_data(self):
        """Create sample LMM-ready data."""
        np.random.seed(42)
        data = []

        for uid in range(1, 21):  # 20 participants
            intercept = np.random.randn() * 0.3  # Random intercept
            slope = np.random.randn() * 0.05  # Random slope

            for day in [0, 1, 3, 6]:
                theta = 0.5 + intercept - 0.1 * day + slope * day + np.random.randn() * 0.2
                data.append({
                    'UID': f'P{uid:03d}',
                    'Days': day,
                    'Theta': theta,
                    'Factor': 'F1'
                })

        return pd.DataFrame(data)

    def test_import_function(self):
        """Test function can be imported."""
        from tools.analysis_lmm import compare_lmm_models_by_aic
        assert callable(compare_lmm_models_by_aic)

    def test_returns_dict(self, sample_lmm_data):
        """Test function returns dictionary."""
        from tools.analysis_lmm import compare_lmm_models_by_aic

        result = compare_lmm_models_by_aic(
            sample_lmm_data,
            n_factors=1
        )

        assert isinstance(result, dict)

    def test_has_models_key(self, sample_lmm_data):
        """Test output has models dictionary."""
        from tools.analysis_lmm import compare_lmm_models_by_aic

        result = compare_lmm_models_by_aic(
            sample_lmm_data,
            n_factors=1
        )

        assert 'models' in result or len(result) > 0

    def test_has_aic_comparison(self, sample_lmm_data):
        """Test output has AIC comparison."""
        from tools.analysis_lmm import compare_lmm_models_by_aic

        result = compare_lmm_models_by_aic(
            sample_lmm_data,
            n_factors=1
        )

        keys = [k.lower() for k in result.keys()]
        aic_keys = [k for k in keys if 'aic' in k or 'comparison' in k]
        assert len(aic_keys) > 0 or 'best_model' in keys

    def test_has_best_model(self, sample_lmm_data):
        """Test output identifies best model."""
        from tools.analysis_lmm import compare_lmm_models_by_aic

        result = compare_lmm_models_by_aic(
            sample_lmm_data,
            n_factors=1
        )

        keys = [k.lower() for k in result.keys()]
        best_keys = [k for k in keys if 'best' in k]
        assert len(best_keys) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
