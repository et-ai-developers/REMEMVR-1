"""
Test validate_irt_convergence function.

Tests validation of IRT model convergence.
"""
import pytest

from tools.validation import validate_irt_convergence


class TestValidateIrtConvergence:
    """Tests for validate_irt_convergence function."""

    def test_returns_dict(self):
        """Test function returns dictionary."""
        results = {'converged': True, 'final_loss': 0.5}
        result = validate_irt_convergence(results)
        assert isinstance(result, dict)

    def test_converged_key_present(self):
        """Test output has 'converged' key."""
        results = {'model_converged': True}
        result = validate_irt_convergence(results)
        assert 'converged' in result

    def test_converged_true_passes_through(self):
        """Test model_converged=True results in converged=True."""
        results = {'model_converged': True, 'final_loss': 0.1}
        result = validate_irt_convergence(results)
        assert result['converged'] is True

    def test_converged_false_passes_through(self):
        """Test model_converged=False results in converged=False."""
        results = {'model_converged': False, 'final_loss': 10.0}
        result = validate_irt_convergence(results)
        assert result['converged'] is False

    def test_missing_converged_key(self):
        """Test handles missing 'converged' key gracefully."""
        results = {'final_loss': 0.5}
        result = validate_irt_convergence(results)
        assert isinstance(result, dict)

    def test_has_message(self):
        """Test output has message explaining result."""
        results = {'converged': True}
        result = validate_irt_convergence(results)
        assert 'message' in result

    def test_empty_results(self):
        """Test handles empty results dict."""
        results = {}
        result = validate_irt_convergence(results)
        assert isinstance(result, dict)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
