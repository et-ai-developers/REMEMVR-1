"""Test suite for analysis_stats module using TDD."""

import numpy as np
import pandas as pd
import pytest
from unittest.mock import Mock, patch

# Import the functions we're about to create
from tools.analysis_stats import (
    one_way_anova_d068,
    chi_square_test_d068,
    compute_cramers_v
)


class TestOneWayAnovaD068:
    """Test one-way ANOVA with dual p-value reporting."""
    
    def test_three_groups_basic(self):
        """Test basic 3-group ANOVA."""
        # Create data with clear group differences
        group1 = np.array([5, 6, 7, 5, 6])  # Mean ~6
        group2 = np.array([8, 9, 10, 8, 9])  # Mean ~9  
        group3 = np.array([12, 13, 14, 12, 13])  # Mean ~13
        
        groups = [group1, group2, group3]
        result = one_way_anova_d068(groups)
        
        # Should detect significant differences
        assert 'F' in result
        assert 'p_uncorrected' in result
        assert 'p_corrected' in result
        assert 'eta_squared' in result
        assert 'df_between' in result
        assert 'df_within' in result
        
        # F should be large (big group differences)
        assert result['F'] > 10
        # Uncorrected p should be very small
        assert result['p_uncorrected'] < 0.001
        # Eta squared should be large
        assert result['eta_squared'] > 0.5
    
    def test_bonferroni_correction(self):
        """Test Bonferroni correction properly applied."""
        group1 = np.array([1, 2, 3, 4, 5])
        group2 = np.array([2, 3, 4, 5, 6])
        group3 = np.array([3, 4, 5, 6, 7])
        
        groups = [group1, group2, group3]
        result = one_way_anova_d068(groups, correction='bonferroni', n_comparisons=3)
        
        # Corrected p should be larger than uncorrected
        assert result['p_corrected'] >= result['p_uncorrected']
        # Should be exactly 3x if using Bonferroni with 3 comparisons
        if result['p_uncorrected'] * 3 <= 1.0:
            assert np.isclose(result['p_corrected'], result['p_uncorrected'] * 3)
    
    def test_no_correction(self):
        """Test with no correction applied."""
        group1 = np.array([1, 2, 3])
        group2 = np.array([4, 5, 6])
        
        groups = [group1, group2]
        result = one_way_anova_d068(groups, correction=None)
        
        # With no correction, both p-values should be identical
        assert result['p_corrected'] == result['p_uncorrected']
    
    def test_dataframe_input(self):
        """Test with DataFrame input format."""
        df = pd.DataFrame({
            'group': ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C'],
            'value': [1, 2, 3, 4, 5, 6, 7, 8, 9]
        })
        
        result = one_way_anova_d068(data=df, dv='value', between='group')
        
        assert 'F' in result
        assert result['F'] > 0
        assert 0 <= result['eta_squared'] <= 1
    
    def test_post_hoc_included(self):
        """Test that post-hoc tests are included when requested."""
        group1 = np.array([1, 2, 3])
        group2 = np.array([4, 5, 6])
        group3 = np.array([7, 8, 9])
        
        groups = [group1, group2, group3]
        result = one_way_anova_d068(groups, post_hoc='tukey')
        
        assert 'post_hoc' in result
        assert 'pairwise_comparisons' in result['post_hoc']


class TestChiSquareTestD068:
    """Test chi-square test with dual p-value reporting."""
    
    def test_2x2_contingency(self):
        """Test basic 2x2 contingency table."""
        # Create contingency table with association
        # [[10, 2], [3, 15]] - strong association
        contingency_table = np.array([[10, 2], [3, 15]])
        
        result = chi_square_test_d068(contingency_table)
        
        assert 'chi2' in result
        assert 'p_uncorrected' in result
        assert 'p_corrected' in result
        assert 'cramers_v' in result
        assert 'df' in result
        
        # Should detect significant association
        assert result['chi2'] > 0
        assert result['p_uncorrected'] < 0.05
        assert 0 <= result['cramers_v'] <= 1
    
    def test_3x3_contingency(self):
        """Test 3x3 contingency table."""
        contingency_table = np.array([
            [10, 5, 2],
            [5, 20, 5],
            [2, 5, 15]
        ])
        
        result = chi_square_test_d068(contingency_table)
        
        assert result['df'] == 4  # (3-1) * (3-1)
        assert result['cramers_v'] > 0
    
    def test_yates_correction(self):
        """Test Yates correction for 2x2 table."""
        contingency_table = np.array([[5, 3], [2, 4]])
        
        result = chi_square_test_d068(contingency_table, yates_correction=True)
        
        # Yates correction should reduce chi2
        result_no_yates = chi_square_test_d068(contingency_table, yates_correction=False)
        assert result['chi2'] <= result_no_yates['chi2']
    
    def test_expected_frequencies(self):
        """Test that expected frequencies are calculated."""
        contingency_table = np.array([[10, 20], [15, 25]])
        
        result = chi_square_test_d068(contingency_table, return_expected=True)
        
        assert 'expected' in result
        assert result['expected'].shape == contingency_table.shape


class TestComputeCramersV:
    """Test Cramér's V effect size calculation."""
    
    def test_2x2_table(self):
        """Test Cramér's V for 2x2 table."""
        chi2 = 10.0
        n = 100
        k = 2  # min(rows, cols)
        
        v = compute_cramers_v(chi2, n, k)
        
        # V = sqrt(chi2 / (n * (k-1)))
        expected = np.sqrt(10.0 / (100 * 1))
        assert np.isclose(v, expected)
        assert 0 <= v <= 1
    
    def test_3x4_table(self):
        """Test Cramér's V for 3x4 table."""
        chi2 = 25.0
        n = 200
        k = 3  # min(3 rows, 4 cols)
        
        v = compute_cramers_v(chi2, n, k)
        
        # V = sqrt(chi2 / (n * (k-1)))
        expected = np.sqrt(25.0 / (200 * 2))
        assert np.isclose(v, expected)
    
    def test_perfect_association(self):
        """Test maximum Cramér's V."""
        # Perfect association scenario
        n = 100
        k = 2
        chi2 = n * (k - 1)  # Maximum possible chi2
        
        v = compute_cramers_v(chi2, n, k)
        
        assert np.isclose(v, 1.0)
    
    def test_no_association(self):
        """Test minimum Cramér's V."""
        chi2 = 0.0  # No association
        n = 100
        k = 3
        
        v = compute_cramers_v(chi2, n, k)
        
        assert v == 0.0