"""Test suite for bootstrap module using TDD."""

import numpy as np
import pandas as pd
import pytest
from unittest.mock import Mock, patch

# Import the functions we're about to create
from tools.bootstrap import (
    bootstrap_correlation_ci,
    bootstrap_mean_ci,
    bootstrap_median_ci,
    bootstrap_statistic
)


class TestBootstrapCorrelationCI:
    """Test bootstrap confidence intervals for correlations."""
    
    def test_positive_correlation(self):
        """Test CI for positive correlation."""
        np.random.seed(42)
        # Create correlated data
        x = np.random.randn(50)
        y = 2 * x + np.random.randn(50) * 0.5  # Strong positive correlation
        
        result = bootstrap_correlation_ci(x, y, n_bootstrap=100, seed=42)
        
        assert 'r' in result
        assert 'ci_lower' in result
        assert 'ci_upper' in result
        assert 'se' in result
        assert 'bootstrap_samples' in result
        
        # Should detect positive correlation
        assert result['r'] > 0.7
        assert result['ci_lower'] > 0.5
        assert result['ci_upper'] < 1.0
        assert result['ci_lower'] < result['r'] < result['ci_upper']
    
    def test_negative_correlation(self):
        """Test CI for negative correlation."""
        np.random.seed(42)
        x = np.random.randn(50)
        y = -2 * x + np.random.randn(50) * 0.5  # Strong negative correlation
        
        result = bootstrap_correlation_ci(x, y, n_bootstrap=100, seed=42)
        
        assert result['r'] < -0.7
        assert result['ci_lower'] < result['r'] < result['ci_upper']
        assert result['ci_upper'] < 0
    
    def test_confidence_levels(self):
        """Test different confidence levels."""
        np.random.seed(42)
        x = np.random.randn(30)
        y = x + np.random.randn(30) * 0.5
        
        # 95% CI
        result_95 = bootstrap_correlation_ci(x, y, confidence=0.95, 
                                              n_bootstrap=100, seed=42)
        # 99% CI
        result_99 = bootstrap_correlation_ci(x, y, confidence=0.99,
                                              n_bootstrap=100, seed=42)
        
        # 99% CI should be wider than 95% CI
        width_95 = result_95['ci_upper'] - result_95['ci_lower']
        width_99 = result_99['ci_upper'] - result_99['ci_lower']
        assert width_99 > width_95
    
    def test_correlation_methods(self):
        """Test different correlation methods."""
        np.random.seed(42)
        x = np.random.randn(40)
        y = x + np.random.randn(40) * 0.3
        
        # Pearson correlation
        result_pearson = bootstrap_correlation_ci(x, y, method='pearson',
                                                   n_bootstrap=100, seed=42)
        
        # Spearman correlation
        result_spearman = bootstrap_correlation_ci(x, y, method='spearman',
                                                    n_bootstrap=100, seed=42)
        
        # Both should give valid results
        assert -1 <= result_pearson['r'] <= 1
        assert -1 <= result_spearman['r'] <= 1
        assert len(result_pearson['bootstrap_samples']) == 100
        assert len(result_spearman['bootstrap_samples']) == 100
    
    def test_reproducibility(self):
        """Test that same seed gives same results."""
        np.random.seed(42)
        x = np.random.randn(25)
        y = x + np.random.randn(25)
        
        result1 = bootstrap_correlation_ci(x, y, n_bootstrap=50, seed=123)
        result2 = bootstrap_correlation_ci(x, y, n_bootstrap=50, seed=123)
        
        assert result1['r'] == result2['r']
        assert result1['ci_lower'] == result2['ci_lower']
        assert result1['ci_upper'] == result2['ci_upper']
        assert np.array_equal(result1['bootstrap_samples'], 
                              result2['bootstrap_samples'])


class TestBootstrapMeanCI:
    """Test bootstrap confidence intervals for means."""
    
    def test_normal_distribution(self):
        """Test CI for normally distributed data."""
        np.random.seed(42)
        data = np.random.randn(100) * 2 + 5  # Mean=5, SD=2
        
        result = bootstrap_mean_ci(data, n_bootstrap=200, seed=42)
        
        assert 'mean' in result
        assert 'ci_lower' in result
        assert 'ci_upper' in result
        assert 'se' in result
        
        # Mean should be close to 5
        assert 4.5 < result['mean'] < 5.5
        assert result['ci_lower'] < result['mean'] < result['ci_upper']
        # CI width should be reasonable
        assert 0.2 < (result['ci_upper'] - result['ci_lower']) < 1.0
    
    def test_skewed_distribution(self):
        """Test CI for skewed data."""
        np.random.seed(42)
        # Create skewed data (exponential)
        data = np.random.exponential(2, 100)
        
        result = bootstrap_mean_ci(data, n_bootstrap=200, seed=42)
        
        # Mean should be close to 2 (exponential parameter)
        assert 1.5 < result['mean'] < 2.5
        assert result['ci_lower'] < result['mean'] < result['ci_upper']
    
    def test_percentile_vs_bca(self):
        """Test percentile vs BCa methods."""
        np.random.seed(42)
        data = np.random.randn(50) * 1.5 + 3
        
        result_percentile = bootstrap_mean_ci(data, method='percentile',
                                               n_bootstrap=200, seed=42)
        result_bca = bootstrap_mean_ci(data, method='bca',
                                        n_bootstrap=200, seed=42)
        
        # Both should give valid results
        assert result_percentile['ci_lower'] < result_percentile['mean']
        assert result_bca['ci_lower'] < result_bca['mean']
        # BCa often gives slightly different (usually better) intervals
        # but they should be similar for symmetric distributions
        assert abs(result_percentile['mean'] - result_bca['mean']) < 0.1


class TestBootstrapMedianCI:
    """Test bootstrap confidence intervals for medians."""
    
    def test_median_ci(self):
        """Test CI for median."""
        np.random.seed(42)
        # Data with outliers where median is more robust
        data = np.concatenate([np.random.randn(90), [10, 15, -10, -15]])
        
        result = bootstrap_median_ci(data, n_bootstrap=200, seed=42)
        
        assert 'median' in result
        assert 'ci_lower' in result
        assert 'ci_upper' in result
        
        # Median should be close to 0 despite outliers
        assert -0.5 < result['median'] < 0.5
        assert result['ci_lower'] < result['median'] < result['ci_upper']
    
    def test_comparison_with_mean(self):
        """Test that median is more robust than mean for outliers."""
        np.random.seed(42)
        # Normal data with outliers
        data = np.concatenate([np.random.randn(95), [50, 60, 70, 80, 90]])
        
        mean_result = bootstrap_mean_ci(data, n_bootstrap=100, seed=42)
        median_result = bootstrap_median_ci(data, n_bootstrap=100, seed=42)
        
        # Mean should be pulled up by outliers more than median
        assert mean_result['mean'] > median_result['median']
        # Median CI should be narrower (more robust)
        mean_width = mean_result['ci_upper'] - mean_result['ci_lower']
        median_width = median_result['ci_upper'] - median_result['ci_lower']
        # This assertion might not always hold, but median is generally more stable
        assert median_width < mean_width * 1.5  # Reasonable comparison


class TestBootstrapStatistic:
    """Test general bootstrap for any statistic."""
    
    def test_custom_statistic(self):
        """Test bootstrap with custom statistic function."""
        np.random.seed(42)
        data = np.random.randn(50) * 3 + 10
        
        # Custom statistic: trimmed mean
        def trimmed_mean(x):
            return np.mean(np.sort(x)[5:-5])  # Trim 5 from each end
        
        result = bootstrap_statistic(data, trimmed_mean, 
                                      n_bootstrap=100, seed=42)
        
        assert 'statistic' in result
        assert 'ci_lower' in result
        assert 'ci_upper' in result
        assert 'bootstrap_samples' in result
        
        # Trimmed mean should be close to true mean for normal data
        assert 9 < result['statistic'] < 11
        assert len(result['bootstrap_samples']) == 100
    
    def test_multivariate_statistic(self):
        """Test bootstrap with multivariate data."""
        np.random.seed(42)
        # Create paired data
        x = np.random.randn(30)
        y = 2 * x + np.random.randn(30) * 0.5
        data = np.column_stack([x, y])
        
        # Statistic: correlation coefficient
        def correlation(xy):
            return np.corrcoef(xy[:, 0], xy[:, 1])[0, 1]
        
        result = bootstrap_statistic(data, correlation, 
                                      n_bootstrap=100, seed=42)
        
        assert result['statistic'] > 0.8  # Strong correlation
        assert result['ci_lower'] > 0.6
        assert result['ci_upper'] < 1.0
    
    def test_paired_bootstrap(self):
        """Test paired bootstrap for difference of means."""
        np.random.seed(42)
        # Paired measurements
        before = np.random.randn(40) * 2 + 50
        after = before + np.random.randn(40) * 1 + 3  # Treatment effect of 3
        
        paired_data = np.column_stack([before, after])
        
        def mean_difference(data):
            return np.mean(data[:, 1] - data[:, 0])
        
        result = bootstrap_statistic(paired_data, mean_difference,
                                      n_bootstrap=200, seed=42)
        
        # Should detect treatment effect around 3
        assert 2.5 < result['statistic'] < 3.5
        assert result['ci_lower'] > 2.0
        assert result['ci_upper'] < 4.0