"""Test suite for validate_cluster_assignment function."""

import pytest
import pandas as pd
from tools.validation import validate_cluster_assignment


class TestValidateClusterAssignment:
    """Test validate_cluster_assignment function."""

    def test_valid_consecutive_clusters(self):
        """Test valid cluster assignments (0, 1, 2)."""
        df = pd.DataFrame({'cluster': [0, 0, 1, 1, 2, 2]})
        result = validate_cluster_assignment(df, n_participants=6, min_cluster_size=2)

        assert result['valid'] is True
        assert result['cluster_sizes'] == {0: 2, 1: 2, 2: 2}

    def test_invalid_non_consecutive(self):
        """Test invalid non-consecutive cluster IDs."""
        df = pd.DataFrame({'cluster': [0, 0, 2, 2]})  # Missing cluster 1
        result = validate_cluster_assignment(df, n_participants=4, min_cluster_size=1)

        assert result['valid'] is False
        assert 'non-consecutive' in result['message'].lower()

    def test_invalid_small_cluster(self):
        """Test cluster smaller than minimum size."""
        df = pd.DataFrame({'cluster': [0, 0, 0, 1]})
        result = validate_cluster_assignment(df, n_participants=4, min_cluster_size=2)

        assert result['valid'] is False
        assert '[1]' in result['message']  # Cluster 1 in list

    def test_realistic_rq_5_14_scenario(self):
        """Test realistic K-means clustering (N=100, K=3)."""
        df = pd.DataFrame({'cluster': ([0]*35 + [1]*40 + [2]*25)})
        result = validate_cluster_assignment(df, n_participants=100, min_cluster_size=10)

        assert result['valid'] is True
        assert result['cluster_sizes'][0] == 35
        assert result['cluster_sizes'][1] == 40
        assert result['cluster_sizes'][2] == 25
