"""
Tests for validate_model_convergence validator.

Purpose: Validate statsmodels LMM model convergence
Used by: RQ 5.13 model convergence validation
"""

import pytest
from unittest.mock import Mock
from tools.validation import validate_model_convergence


class TestValidateModelConvergence:
    """Tests for validate_model_convergence validator."""

    def test_basic_structure(self):
        """Test basic output structure."""
        # Create mock model with converged=True
        mock_model = Mock()
        mock_model.converged = True

        result = validate_model_convergence(mock_model)

        assert 'valid' in result
        assert 'message' in result
        assert 'converged' in result
        assert isinstance(result['valid'], bool)
        assert isinstance(result['message'], str)
        assert isinstance(result['converged'], bool)

    def test_converged_model_valid(self):
        """Test converged model returns valid."""
        mock_model = Mock()
        mock_model.converged = True

        result = validate_model_convergence(mock_model)

        assert result['valid'] is True
        assert result['converged'] is True
        assert 'Model converged successfully' in result['message']

    def test_not_converged_model_invalid(self):
        """Test non-converged model returns invalid."""
        mock_model = Mock()
        mock_model.converged = False

        result = validate_model_convergence(mock_model)

        assert result['valid'] is False
        assert result['converged'] is False
        assert 'Model did not converge' in result['message'] or 'failed to converge' in result['message']

    def test_missing_converged_attribute(self):
        """Test model without converged attribute."""
        mock_model = Mock(spec=[])  # Empty spec - no attributes

        # Should handle gracefully
        result = validate_model_convergence(mock_model)

        assert result['valid'] is False
        assert 'converged' in result['message'].lower() or 'attribute' in result['message'].lower()

    def test_realistic_statsmodels_converged(self):
        """Test realistic statsmodels MixedLMResults (converged)."""
        # Simulate statsmodels MixedLMResults
        mock_result = Mock()
        mock_result.converged = True
        mock_result.model = Mock()
        mock_result.params = {'Intercept': 1.5, 'Age_c': 0.02}

        result = validate_model_convergence(mock_result)

        assert result['valid'] is True
        assert result['converged'] is True

    def test_realistic_statsmodels_not_converged(self):
        """Test realistic statsmodels MixedLMResults (not converged)."""
        # Simulate statsmodels MixedLMResults with convergence failure
        mock_result = Mock()
        mock_result.converged = False
        mock_result.model = Mock()

        result = validate_model_convergence(mock_result)

        assert result['valid'] is False
        assert result['converged'] is False
