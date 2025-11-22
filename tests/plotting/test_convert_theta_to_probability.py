"""
Test convert_theta_to_probability function.

Tests IRT 2PL probability transformation.
"""
import pytest
import numpy as np

from tools.plotting import convert_theta_to_probability


class TestConvertThetaToProbability:
    """Tests for convert_theta_to_probability function."""

    def test_returns_array(self):
        """Test function returns numpy array."""
        theta = np.array([0.0])
        result = convert_theta_to_probability(theta, discrimination=1.0, difficulty=0.0)

        assert isinstance(result, np.ndarray)

    def test_output_shape_matches_input(self):
        """Test output shape matches input shape."""
        theta = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
        result = convert_theta_to_probability(theta, discrimination=1.0, difficulty=0.0)

        assert result.shape == theta.shape

    def test_probability_at_difficulty(self):
        """Test P = 0.5 when theta = difficulty."""
        theta = np.array([0.0])
        result = convert_theta_to_probability(theta, discrimination=1.0, difficulty=0.0)

        # At theta = b, P should be exactly 0.5
        assert np.isclose(result[0], 0.5, atol=1e-10)

    def test_probability_above_difficulty(self):
        """Test P > 0.5 when theta > difficulty."""
        theta = np.array([1.0])
        result = convert_theta_to_probability(theta, discrimination=1.0, difficulty=0.0)

        assert result[0] > 0.5

    def test_probability_below_difficulty(self):
        """Test P < 0.5 when theta < difficulty."""
        theta = np.array([-1.0])
        result = convert_theta_to_probability(theta, discrimination=1.0, difficulty=0.0)

        assert result[0] < 0.5

    def test_probability_range(self):
        """Test all probabilities are in [0, 1]."""
        theta = np.linspace(-5, 5, 100)
        result = convert_theta_to_probability(theta, discrimination=1.0, difficulty=0.0)

        assert np.all(result >= 0)
        assert np.all(result <= 1)

    def test_higher_discrimination_steeper(self):
        """Test higher discrimination gives steeper curve."""
        theta = np.array([0.5])  # Slightly above difficulty

        # Low discrimination
        p_low = convert_theta_to_probability(theta, discrimination=0.5, difficulty=0.0)

        # High discrimination
        p_high = convert_theta_to_probability(theta, discrimination=2.0, difficulty=0.0)

        # Higher discrimination should give higher P for theta > b
        assert p_high[0] > p_low[0]

    def test_difficulty_shift(self):
        """Test difficulty parameter shifts the curve."""
        theta = np.array([1.0])

        # Easy item (low difficulty)
        p_easy = convert_theta_to_probability(theta, discrimination=1.0, difficulty=-1.0)

        # Hard item (high difficulty)
        p_hard = convert_theta_to_probability(theta, discrimination=1.0, difficulty=1.0)

        # Easier item should have higher P
        assert p_easy[0] > p_hard[0]

    def test_monotonically_increasing(self):
        """Test probability increases with theta."""
        theta = np.linspace(-3, 3, 100)
        result = convert_theta_to_probability(theta, discrimination=1.0, difficulty=0.0)

        # Each successive value should be >= previous
        assert np.all(np.diff(result) >= 0)

    def test_extreme_theta_values(self):
        """Test function handles extreme theta values."""
        theta = np.array([-10.0, 10.0])
        result = convert_theta_to_probability(theta, discrimination=1.0, difficulty=0.0)

        # Should approach 0 and 1 respectively
        assert result[0] < 0.01  # Very low for theta << b
        assert result[1] > 0.99  # Very high for theta >> b

    def test_scalar_input(self):
        """Test function handles scalar input."""
        result = convert_theta_to_probability(
            np.array([0.0]),
            discrimination=1.0,
            difficulty=0.0
        )
        assert result[0] == pytest.approx(0.5)

    def test_irt_2pl_formula(self):
        """Test exact IRT 2PL formula: P = 1 / (1 + exp(-(a * (theta - b))))."""
        theta = np.array([1.0])
        a = 1.5  # discrimination
        b = 0.5  # difficulty

        result = convert_theta_to_probability(theta, discrimination=a, difficulty=b)

        # Calculate expected value directly
        expected = 1 / (1 + np.exp(-(a * (theta[0] - b))))

        assert np.isclose(result[0], expected)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
