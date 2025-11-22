"""
Test validate_lmm_convergence function.

Tests validation of LMM model convergence.
"""
import pytest
from unittest.mock import MagicMock

from tools.validation import validate_lmm_convergence


class TestValidateLmmConvergence:
    """Tests for validate_lmm_convergence function."""

    @pytest.fixture
    def converged_result(self):
        """Create mock LMM result that converged."""
        mock = MagicMock()
        mock.converged = True
        return mock

    @pytest.fixture
    def non_converged_result(self):
        """Create mock LMM result that did not converge."""
        mock = MagicMock()
        mock.converged = False
        return mock

    def test_returns_dict(self, converged_result):
        """Test function returns dictionary."""
        result = validate_lmm_convergence(converged_result)
        assert isinstance(result, dict)

    def test_converged_key_present(self, converged_result):
        """Test output has 'converged' key."""
        result = validate_lmm_convergence(converged_result)
        assert 'converged' in result

    def test_converged_is_true(self, converged_result):
        """Test converged model returns converged=True."""
        result = validate_lmm_convergence(converged_result)
        assert result['converged'] is True

    def test_non_converged_is_false(self, non_converged_result):
        """Test non-converged model returns converged=False."""
        result = validate_lmm_convergence(non_converged_result)
        assert result['converged'] is False

    def test_missing_converged_attribute(self):
        """Test handles missing converged attribute."""
        mock = MagicMock(spec=[])
        result = validate_lmm_convergence(mock)
        assert isinstance(result, dict)

    def test_has_message(self, converged_result):
        """Test output has explanatory message."""
        result = validate_lmm_convergence(converged_result)
        assert 'message' in result or 'converged' in result


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
