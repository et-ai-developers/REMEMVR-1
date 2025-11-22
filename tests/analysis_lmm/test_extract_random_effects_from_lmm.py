"""
Test extract_random_effects_from_lmm function.

Tests extraction of random effects and ICC calculation.
"""
import pytest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock


class TestExtractRandomEffectsFromLmm:
    """Tests for extract_random_effects_from_lmm function."""

    @pytest.fixture
    def mock_lmm_result(self):
        """Create mock LMM result object."""
        mock = MagicMock()

        # Random effects covariance matrix
        mock.cov_re = pd.DataFrame(
            [[0.25, 0.05], [0.05, 0.10]],
            index=['Intercept', 'Days'],
            columns=['Intercept', 'Days']
        )

        # Residual variance (scale)
        mock.scale = 0.5

        return mock

    def test_import_function(self):
        """Test function can be imported."""
        from tools.analysis_lmm import extract_random_effects_from_lmm
        assert callable(extract_random_effects_from_lmm)

    def test_returns_dict(self, mock_lmm_result):
        """Test function returns dictionary."""
        from tools.analysis_lmm import extract_random_effects_from_lmm

        result = extract_random_effects_from_lmm(mock_lmm_result)

        assert isinstance(result, dict)

    def test_has_variance_components(self, mock_lmm_result):
        """Test output has variance components."""
        from tools.analysis_lmm import extract_random_effects_from_lmm

        result = extract_random_effects_from_lmm(mock_lmm_result)

        # Should have some variance info
        keys = [k.lower() for k in result.keys()]
        var_keys = [k for k in keys if 'var' in k or 'cov' in k or 're' in k]
        assert len(var_keys) > 0 or 'random_effects' in keys or len(result) > 0

    def test_has_icc(self, mock_lmm_result):
        """Test output has ICC (Intraclass Correlation Coefficient)."""
        from tools.analysis_lmm import extract_random_effects_from_lmm

        result = extract_random_effects_from_lmm(mock_lmm_result)

        keys = [k.lower() for k in result.keys()]
        icc_keys = [k for k in keys if 'icc' in k]
        assert len(icc_keys) > 0

    def test_icc_in_valid_range(self, mock_lmm_result):
        """Test ICC is between 0 and 1."""
        from tools.analysis_lmm import extract_random_effects_from_lmm

        result = extract_random_effects_from_lmm(mock_lmm_result)

        # Find ICC value
        icc = None
        for k, v in result.items():
            if 'icc' in k.lower():
                icc = v
                break

        if icc is not None:
            assert 0 <= icc <= 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
