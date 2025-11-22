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

        # Actual model names from implementation
        expected_models = [
            'Linear',
            'Quadratic',
            'Log',
            'Lin+Log',
            'Quad+Log'
        ]

        for model_name in expected_models:
            assert model_name in result, f"Missing model: {model_name}"

    def test_each_model_has_formula(self):
        """Test each model has formula and re_formula."""
        result = configure_candidate_models(n_factors=1)

        for model_name, model_spec in result.items():
            assert 'formula' in model_spec, f"{model_name} missing formula"
            assert isinstance(model_spec['formula'], str)
            assert 're_formula' in model_spec, f"{model_name} missing re_formula"

    def test_single_factor_formulas(self):
        """Test formulas for single-factor model."""
        result = configure_candidate_models(n_factors=1)

        # Single-factor models should reference Ability and Days
        assert 'Ability' in result['Linear']['formula']
        assert 'Days' in result['Linear']['formula']
        assert 'Days' in result['Quadratic']['formula']
        assert 'Days_sq' in result['Quadratic']['formula']

    def test_multi_factor_formulas(self):
        """Test formulas for multi-factor model."""
        result = configure_candidate_models(n_factors=3, reference_group='What')

        # Should include Factor interactions with treatment coding
        full_formula = result['Linear']['formula']
        assert 'Factor' in full_formula or 'C(' in full_formula
        assert 'What' in full_formula  # Reference group

    def test_reference_group_required_for_multi(self):
        """Test reference_group is required for multi-factor."""
        # Should raise ValueError without reference_group
        with pytest.raises(ValueError):
            configure_candidate_models(n_factors=2, reference_group=None)

    def test_reference_group_in_formula(self):
        """Test reference group appears in formula."""
        result = configure_candidate_models(n_factors=2, reference_group='FactorA')

        # Check reference group appears in formula (as treatment contrast)
        full_formula = result['Linear']['formula']
        assert "Treatment('FactorA')" in full_formula


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
