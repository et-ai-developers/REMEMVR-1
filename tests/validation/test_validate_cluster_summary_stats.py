"""Test suite for validate_cluster_summary_stats function."""

import pytest
import pandas as pd
from tools.validation import validate_cluster_summary_stats


class TestValidateClusterSummaryStats:
    """Test validate_cluster_summary_stats function."""

    def test_valid_consistent_stats(self):
        """Test valid summary statistics (min ≤ mean ≤ max, SD ≥ 0)."""
        df = pd.DataFrame({
            'cluster': [0, 1],
            'N': [35, 40],
            'Age_min': [20, 22],
            'Age_mean': [35, 37],
            'Age_max': [50, 52],
            'Age_SD': [10, 12]
        })
        result = validate_cluster_summary_stats(df)

        assert result['valid'] is True
        assert len(result['failed_checks']) == 0

    def test_invalid_mean_outside_range(self):
        """Test invalid mean outside [min, max]."""
        df = pd.DataFrame({
            'cluster': [0],
            'N': [10],
            'Age_min': [20],
            'Age_mean': [55],  # > max
            'Age_max': [50],
            'Age_SD': [10]
        })
        result = validate_cluster_summary_stats(df)

        assert result['valid'] is False
        assert len(result['failed_checks']) > 0

    def test_invalid_negative_sd(self):
        """Test invalid negative SD."""
        df = pd.DataFrame({
            'cluster': [0],
            'N': [10],
            'Age_min': [20],
            'Age_mean': [35],
            'Age_max': [50],
            'Age_SD': [-1]  # Negative!
        })
        result = validate_cluster_summary_stats(df)

        assert result['valid'] is False

    def test_realistic_rq_5_14_scenario(self):
        """Test realistic cluster summaries (K=3)."""
        df = pd.DataFrame({
            'cluster': [0, 1, 2],
            'N': [35, 40, 25],
            'Age_min': [18, 19, 20],
            'Age_mean': [32, 45, 67],
            'Age_max': [44, 64, 85],
            'Age_SD': [8.2, 10.5, 7.3]
        })
        result = validate_cluster_summary_stats(df)

        assert result['valid'] is True
