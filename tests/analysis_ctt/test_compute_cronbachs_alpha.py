"""
Tests for compute_cronbachs_alpha function.

TDD RED Phase: Write tests FIRST before implementation.
Expected: All tests FAIL until implementation complete.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from tools.analysis_ctt import compute_cronbachs_alpha


class TestComputeCronbachsAlpha:
    """Test suite for Cronbach's alpha with bootstrap CIs."""

    def test_basic_perfect_reliability(self):
        """Test alpha = 1.0 when all items perfectly correlated."""
        # All participants give same pattern
        data = pd.DataFrame({
            'item1': [1, 1, 0, 0, 1],
            'item2': [1, 1, 0, 0, 1],
            'item3': [1, 1, 0, 0, 1]
        })

        result = compute_cronbachs_alpha(data, n_bootstrap=100)

        assert 'alpha' in result
        assert 'ci_lower' in result
        assert 'ci_upper' in result
        assert 'n_items' in result
        assert result['alpha'] == pytest.approx(1.0, abs=0.01)
        assert result['n_items'] == 3

    def test_basic_zero_reliability(self):
        """Test alpha ≈ 0 when items uncorrelated."""
        # Completely random binary data
        np.random.seed(42)
        data = pd.DataFrame({
            'item1': np.random.randint(0, 2, 100),
            'item2': np.random.randint(0, 2, 100),
            'item3': np.random.randint(0, 2, 100)
        })

        result = compute_cronbachs_alpha(data, n_bootstrap=100)

        assert result['alpha'] < 0.3  # Low reliability for random data

    def test_moderate_reliability(self):
        """Test moderate alpha (~0.7) with realistic item correlations."""
        # Create correlated items (typical for episodic memory)
        np.random.seed(42)
        n = 100
        ability = np.random.randn(n)
        data = pd.DataFrame({
            'item1': (ability + np.random.randn(n) * 0.5 > 0).astype(int),
            'item2': (ability + np.random.randn(n) * 0.5 > 0).astype(int),
            'item3': (ability + np.random.randn(n) * 0.5 > 0).astype(int),
            'item4': (ability + np.random.randn(n) * 0.5 > 0).astype(int)
        })

        result = compute_cronbachs_alpha(data, n_bootstrap=100)

        assert 0.5 <= result['alpha'] <= 0.9  # Reasonable range
        assert result['ci_lower'] < result['alpha'] < result['ci_upper']

    def test_confidence_interval_brackets_alpha(self):
        """Test that bootstrap CI brackets the point estimate."""
        np.random.seed(42)
        data = pd.DataFrame({
            'item1': [1, 0, 1, 0, 1, 0, 1, 0],
            'item2': [1, 0, 1, 1, 1, 0, 1, 0],
            'item3': [1, 1, 1, 0, 1, 0, 1, 1]
        })

        result = compute_cronbachs_alpha(data, n_bootstrap=100)

        assert result['ci_lower'] < result['alpha']
        assert result['alpha'] < result['ci_upper']

    def test_confidence_interval_width(self):
        """Test CI width is reasonable for N=100."""
        np.random.seed(42)
        n = 100
        ability = np.random.randn(n)
        data = pd.DataFrame({
            f'item{i}': (ability + np.random.randn(n) * 0.5 > 0).astype(int)
            for i in range(1, 11)  # 10 items
        })

        result = compute_cronbachs_alpha(data, n_bootstrap=1000)

        ci_width = result['ci_upper'] - result['ci_lower']
        assert 0.02 <= ci_width <= 0.20  # Narrow CIs with N=100

    def test_kr20_equivalence_dichotomous(self):
        """Test that alpha equals KR-20 for dichotomous items."""
        # For binary items, Cronbach's alpha = KR-20 (when using sample variance formula)
        data = pd.DataFrame({
            'item1': [1, 0, 1, 0, 1, 0, 1, 0],
            'item2': [1, 1, 1, 0, 1, 0, 1, 0],
            'item3': [1, 0, 1, 1, 1, 0, 1, 1],
            'item4': [0, 0, 1, 0, 1, 1, 1, 0]
        })

        result = compute_cronbachs_alpha(data, n_bootstrap=100)

        # Compute using general alpha formula (should match our implementation)
        k = 4
        item_variances = data.var(axis=0, ddof=1).sum()
        total_var = data.sum(axis=1).var(ddof=1)
        expected_alpha = (k / (k - 1)) * (1 - item_variances / total_var)

        assert result['alpha'] == pytest.approx(expected_alpha, abs=0.001)

    def test_handles_missing_data(self):
        """Test function handles NaN values (pairwise deletion)."""
        data = pd.DataFrame({
            'item1': [1, 0, 1, np.nan, 1],
            'item2': [1, 1, np.nan, 0, 1],
            'item3': [1, 0, 1, 1, np.nan]
        })

        result = compute_cronbachs_alpha(data, n_bootstrap=100)

        # Should complete without error
        assert 'alpha' in result
        assert result['n_items'] == 3

    def test_minimum_items(self):
        """Test requires at least 2 items."""
        data = pd.DataFrame({'item1': [1, 0, 1, 0, 1]})

        with pytest.raises(ValueError, match="at least 2 items"):
            compute_cronbachs_alpha(data, n_bootstrap=100)

    def test_minimum_participants(self):
        """Test requires at least 3 participants for variance."""
        data = pd.DataFrame({
            'item1': [1, 0],
            'item2': [1, 1]
        })

        with pytest.raises(ValueError, match="at least 3 participants"):
            compute_cronbachs_alpha(data, n_bootstrap=100)

    def test_bootstrap_reproducibility(self):
        """Test results reproducible with same random seed."""
        np.random.seed(42)
        data = pd.DataFrame({
            'item1': [1, 0, 1, 0, 1, 0, 1, 0],
            'item2': [1, 1, 1, 0, 1, 0, 1, 0],
            'item3': [1, 0, 1, 1, 1, 0, 1, 1]
        })

        result1 = compute_cronbachs_alpha(data, n_bootstrap=100)

        np.random.seed(42)
        result2 = compute_cronbachs_alpha(data, n_bootstrap=100)

        assert result1['alpha'] == result2['alpha']
        assert result1['ci_lower'] == pytest.approx(result2['ci_lower'], abs=0.01)
        assert result1['ci_upper'] == pytest.approx(result2['ci_upper'], abs=0.01)

    def test_output_structure(self):
        """Test output Dict has all required keys."""
        data = pd.DataFrame({
            'item1': [1, 0, 1, 0, 1],
            'item2': [1, 1, 1, 0, 1],
            'item3': [1, 0, 1, 1, 1]
        })

        result = compute_cronbachs_alpha(data, n_bootstrap=100)

        required_keys = {'alpha', 'ci_lower', 'ci_upper', 'n_items', 'n_participants'}
        assert set(result.keys()) == required_keys

    def test_alpha_bounds(self):
        """Test alpha in valid range [-1, 1] (typically [0, 1])."""
        np.random.seed(42)
        data = pd.DataFrame({
            'item1': np.random.randint(0, 2, 50),
            'item2': np.random.randint(0, 2, 50),
            'item3': np.random.randint(0, 2, 50)
        })

        result = compute_cronbachs_alpha(data, n_bootstrap=100)

        # Alpha can theoretically be negative (poor reliability)
        # but should be in [-1, 1] range
        assert -1 <= result['alpha'] <= 1
        assert -1 <= result['ci_lower'] <= 1
        assert -1 <= result['ci_upper'] <= 1

    def test_large_bootstrap_iterations(self):
        """Test with 1000 bootstrap iterations (RQ 5.12 spec)."""
        np.random.seed(42)
        data = pd.DataFrame({
            'item1': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            'item2': [1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
            'item3': [1, 0, 1, 1, 1, 0, 1, 1, 1, 0]
        })

        result = compute_cronbachs_alpha(data, n_bootstrap=1000)

        assert 'alpha' in result
        # Should complete in reasonable time (<5 seconds)
