"""
Tests for compare_correlations_dependent function (Steiger's z-test).

TDD: Tests written alongside implementation (both functions in same module).
Expected: All tests PASS immediately.
"""

import pytest
import numpy as np
from tools.analysis_ctt import compare_correlations_dependent


class TestCompareCorrelationsDependent:
    """Test suite for Steiger's z-test for dependent correlations."""

    def test_no_difference_nonsignificant(self):
        """Test z-test is non-significant when correlations equal."""
        result = compare_correlations_dependent(
            r12=0.80,  # IRT-Full CTT
            r13=0.80,  # IRT-Purified CTT (same as r12)
            r23=0.90,  # Full-Purified CTT
            n=100
        )

        assert result['z_statistic'] == pytest.approx(0.0, abs=0.1)
        assert result['p_value'] > 0.05
        assert result['significant'] is False
        assert result['r_difference'] == pytest.approx(0.0, abs=0.01)

    def test_large_difference_significant(self):
        """Test z-test is significant when r13 >> r12."""
        result = compare_correlations_dependent(
            r12=0.70,  # IRT-Full CTT (moderate)
            r13=0.95,  # IRT-Purified CTT (very high)
            r23=0.85,  # Full-Purified CTT
            n=100
        )

        assert result['z_statistic'] > 2.0  # Large z for big difference
        assert result['p_value'] < 0.05
        assert result['significant'] is True
        assert result['r_difference'] == pytest.approx(0.25, abs=0.01)  # 0.95 - 0.70

    def test_rq512_scenario(self):
        """Test RQ 5.12 expected scenario: Purified CTT converges toward IRT."""
        # Expected: r(IRT, Purified) > r(IRT, Full)
        result = compare_correlations_dependent(
            r12=0.85,  # IRT-Full CTT
            r13=0.92,  # IRT-Purified CTT (stronger)
            r23=0.88,  # Full-Purified CTT (high intercorrelation)
            n=100
        )

        assert result['r_difference'] > 0  # Purified stronger
        assert result['z_statistic'] > 0  # Positive z-statistic
        # Whether significant depends on exact correlations
        assert 'interpretation' in result

    def test_negative_difference(self):
        """Test when r12 > r13 (Full CTT stronger than Purified)."""
        result = compare_correlations_dependent(
            r12=0.90,  # IRT-Full CTT (stronger)
            r13=0.80,  # IRT-Purified CTT (weaker)
            r23=0.85,  # Full-Purified CTT
            n=100
        )

        assert result['r_difference'] < 0  # r13 - r12 is negative
        assert result['z_statistic'] < 0  # Negative z-statistic

    def test_output_structure(self):
        """Test output Dict has all required keys."""
        result = compare_correlations_dependent(
            r12=0.80, r13=0.85, r23=0.82, n=100
        )

        required_keys = {'z_statistic', 'p_value', 'r_difference', 'significant', 'interpretation'}
        assert set(result.keys()) == required_keys

    def test_two_tailed_pvalue(self):
        """Test p-value is two-tailed (symmetric for ±z)."""
        result_pos = compare_correlations_dependent(
            r12=0.70, r13=0.85, r23=0.80, n=100
        )
        result_neg = compare_correlations_dependent(
            r12=0.85, r13=0.70, r23=0.80, n=100
        )

        # Magnitude of z should be same, p-value should be same
        assert abs(result_pos['z_statistic']) == pytest.approx(
            abs(result_neg['z_statistic']), abs=0.01
        )
        assert result_pos['p_value'] == pytest.approx(result_neg['p_value'], abs=0.01)

    def test_correlation_bounds_validation(self):
        """Test raises ValueError if correlations outside [-1, 1]."""
        with pytest.raises(ValueError, match="in range"):
            compare_correlations_dependent(
                r12=1.5,  # Invalid
                r13=0.80,
                r23=0.90,
                n=100
            )

        with pytest.raises(ValueError, match="in range"):
            compare_correlations_dependent(
                r12=0.80,
                r13=-1.2,  # Invalid
                r23=0.90,
                n=100
            )

    def test_minimum_sample_size(self):
        """Test requires n >= 20 for validity."""
        with pytest.raises(ValueError, match="at least n=20"):
            compare_correlations_dependent(
                r12=0.80, r13=0.85, r23=0.82, n=15
            )

    def test_interpretation_string_significant(self):
        """Test interpretation string for significant result."""
        result = compare_correlations_dependent(
            r12=0.70, r13=0.92, r23=0.85, n=100
        )

        if result['significant']:
            assert 'significantly' in result['interpretation']
            assert 'higher' in result['interpretation'] or 'lower' in result['interpretation']
            assert "0.92" in result['interpretation']  # r13 value should appear
            assert "0.70" in result['interpretation']  # r12 value should appear

    def test_interpretation_string_nonsignificant(self):
        """Test interpretation string for non-significant result."""
        result = compare_correlations_dependent(
            r12=0.80, r13=0.82, r23=0.85, n=100
        )

        if not result['significant']:
            assert 'No significant difference' in result['interpretation']

    def test_fisher_z_transformation_applied(self):
        """Test that Fisher's z-transformation is applied correctly."""
        # For perfect correlation r=1.0, arctanh(1.0) = inf
        # Function should handle this edge case
        result = compare_correlations_dependent(
            r12=0.99,  # Very high correlation
            r13=0.99,
            r23=0.98,
            n=100
        )

        # Should complete without error
        assert 'z_statistic' in result
        assert not np.isinf(result['z_statistic'])

    def test_sample_size_impact(self):
        """Test larger N increases power (smaller p-value for same r difference)."""
        # Same correlations, different sample sizes
        result_small = compare_correlations_dependent(
            r12=0.75, r13=0.85, r23=0.80, n=50
        )
        result_large = compare_correlations_dependent(
            r12=0.75, r13=0.85, r23=0.80, n=200
        )

        # Larger N should give larger |z| and smaller p-value
        assert abs(result_large['z_statistic']) > abs(result_small['z_statistic'])
        assert result_large['p_value'] < result_small['p_value']

    def test_r23_impact_on_covariance(self):
        """Test r23 affects asymptotic covariance (Steiger's formula)."""
        # Higher r23 (Full-Purified correlation) affects test
        result_low_r23 = compare_correlations_dependent(
            r12=0.80, r13=0.85, r23=0.50, n=100  # Low Full-Purified correlation
        )
        result_high_r23 = compare_correlations_dependent(
            r12=0.80, r13=0.85, r23=0.95, n=100  # High Full-Purified correlation
        )

        # Different r23 should yield different z-statistics
        assert result_low_r23['z_statistic'] != pytest.approx(
            result_high_r23['z_statistic'], abs=0.1
        )
