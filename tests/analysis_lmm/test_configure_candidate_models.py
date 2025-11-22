"""
Test configure_candidate_models function.

Tests generation of 5 candidate LMM model formulas.
"""
import pytest

from tools.analysis_lmm import configure_candidate_models


class TestConfigureCandidateModels:
    """Tests for configure_candidate_models function."""

    def test_returns_dict(self):
        """Test function returns dictionary."""
        result = configure_candidate_models(n_factors=1)
        assert isinstance(result, dict)

    def test_returns_five_models(self):
        """Test function returns exactly 5 models."""
        result = configure_candidate_models(n_factors=1)
        assert len(result) == 5

    def test_model_keys_present(self):
        """Test expected model names are present."""
        result = configure_candidate_models(n_factors=1)

        expected_models = [
            'intercept_only',
            'random_intercept',
            'random_slope',
            'random_intercept_slope',
            'full'
        ]

        for model_name in expected_models:
            assert model_name in result

    def test_each_model_has_formula(self):
        """Test each model has formula and re_formula."""
        result = configure_candidate_models(n_factors=1)

        for model_name, model_spec in result.items():
            assert 'formula' in model_spec
            assert isinstance(model_spec['formula'], str)

    def test_single_factor_formulas(self):
        """Test formulas for single-factor model."""
        result = configure_candidate_models(n_factors=1)

        # Intercept only should be simple
        assert 'Theta' in result['intercept_only']['formula']
        assert 'Days' in result['random_slope']['formula']

    def test_multi_factor_formulas(self):
        """Test formulas for multi-factor model."""
        result = configure_candidate_models(n_factors=3, reference_group='Factor1')

        # Should include Factor interactions
        full_formula = result['full']['formula']
        assert 'Factor' in full_formula or 'C(' in full_formula

    def test_reference_group_required_for_multi(self):
        """Test reference_group is used for multi-factor."""
        result = configure_candidate_models(n_factors=2, reference_group='FactorA')

        # Check reference group appears in formula (as treatment contrast)
        full_formula = result['full']['formula']
        assert 'Factor' in full_formula or 'C(' in full_formula


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
