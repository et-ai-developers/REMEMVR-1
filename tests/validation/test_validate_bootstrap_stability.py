"""Test suite for validate_bootstrap_stability function."""

import pytest
import pandas as pd
from tools.validation import validate_bootstrap_stability


class TestValidateBootstrapStability:
    """Test validate_bootstrap_stability function."""

    def test_valid_high_stability(self):
        """Test valid high stability (mean Jaccard ≥ threshold)."""
        df = pd.DataFrame({'jaccard': [0.85, 0.82, 0.88, 0.90]})
        result = validate_bootstrap_stability(df, min_jaccard_threshold=0.75)

        assert result['valid'] is True
        assert result['mean_jaccard'] >= 0.75

    def test_invalid_low_stability(self):
        """Test invalid low stability (mean Jaccard < threshold)."""
        df = pd.DataFrame({'jaccard': [0.50, 0.55, 0.60]})
        result = validate_bootstrap_stability(df, min_jaccard_threshold=0.75)

        assert result['valid'] is False
        assert result['mean_jaccard'] < 0.75

    def test_invalid_out_of_bounds(self):
        """Test Jaccard values outside [0,1]."""
        df = pd.DataFrame({'jaccard': [0.8, 1.2]})  # 1.2 > 1.0
        result = validate_bootstrap_stability(df, min_jaccard_threshold=0.75)

        assert result['valid'] is False

    def test_realistic_rq_5_14_scenario(self):
        """Test realistic bootstrap stability (1000 iterations)."""
        # Jaccard values centered at 0.86 with small variation
        df = pd.DataFrame({'jaccard': [0.82 + (i % 100)*0.0008 for i in range(1000)]})
        result = validate_bootstrap_stability(df, min_jaccard_threshold=0.75)

        assert result['valid'] is True
        assert 0.80 < result['mean_jaccard'] < 0.92  # Realistic range
