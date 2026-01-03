"""
Test suite for tools.analysis_stats module
Testing statistical analysis tools with D068 dual p-value reporting
"""

import unittest
import numpy as np
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.analysis_stats import (
    one_way_anova_d068,
    chi_square_test_d068,
    compute_cramers_v,
    t_test_d068,
    kruskal_wallis_d068,
    mann_whitney_d068,
    friedman_test_d068,
    compute_effect_sizes
)


class TestANOVA(unittest.TestCase):
    """Test one-way ANOVA with D068 compliance"""
    
    def setUp(self):
        """Create sample data for testing"""
        np.random.seed(42)
        # Three groups with different means
        self.group1 = np.random.normal(10, 2, 30)
        self.group2 = np.random.normal(12, 2, 30)
        self.group3 = np.random.normal(15, 2, 30)
        self.groups = [self.group1, self.group2, self.group3]
        
        # DataFrame format
        self.df = pd.DataFrame({
            'value': np.concatenate(self.groups),
            'group': np.repeat(['A', 'B', 'C'], 30)
        })
    
    def test_basic_anova(self):
        """Test basic ANOVA functionality"""
        result = one_way_anova_d068(
            groups=self.groups,
            dv='score',
            correction='bonferroni'
        )
        
        # Check structure
        self.assertIn('F', result)
        self.assertIn('p_uncorrected', result)
        self.assertIn('p_corrected', result)
        self.assertIn('eta_squared', result)
        self.assertIn('df_between', result)
        self.assertIn('df_within', result)
        
        # F should be positive
        self.assertGreater(result['F'], 0)
        
        # Corrected p should be >= uncorrected
        self.assertGreaterEqual(result['p_corrected'], result['p_uncorrected'])
    
    def test_anova_with_dataframe(self):
        """Test ANOVA with DataFrame input"""
        result = one_way_anova_d068(
            data=self.df,
            dv='value',
            between='group',
            correction='fdr'
        )
        
        # Should detect significant difference
        self.assertLess(result['p_uncorrected'], 0.05)
        
        # Check effect size
        self.assertGreater(result['eta_squared'], 0.1)  # Medium effect
    
    def test_post_hoc(self):
        """Test post-hoc comparisons"""
        result = one_way_anova_d068(
            groups=self.groups,
            dv='score',
            post_hoc='tukey'
        )
        
        # Should include post-hoc results
        self.assertIn('post_hoc', result)
        self.assertIn('pairwise_comparisons', result['post_hoc'])


class TestChiSquare(unittest.TestCase):
    """Test chi-square test with D068"""
    
    def setUp(self):
        """Create contingency table"""
        self.contingency = pd.DataFrame({
            'Yes': [20, 15, 10],
            'No': [10, 15, 20]
        }, index=['Group1', 'Group2', 'Group3'])
    
    def test_chi_square_basic(self):
        """Test basic chi-square functionality"""
        result = chi_square_test_d068(self.contingency)
        
        # Check structure
        self.assertIn('chi2', result)
        self.assertIn('p_uncorrected', result)
        self.assertIn('p_corrected', result)
        self.assertIn('cramers_v', result)
        self.assertIn('df', result)
        
        # Chi2 should be positive
        self.assertGreater(result['chi2'], 0)
        
        # Cramér's V should be between 0 and 1
        self.assertGreaterEqual(result['cramers_v'], 0)
        self.assertLessEqual(result['cramers_v'], 1)
    
    def test_chi_square_correction(self):
        """Test multiple testing correction"""
        result = chi_square_test_d068(
            self.contingency,
            correction='bonferroni',
            n_comparisons=3
        )
        
        # Corrected p should be 3x uncorrected (Bonferroni)
        expected_p = min(result['p_uncorrected'] * 3, 1.0)
        self.assertAlmostEqual(result['p_corrected'], expected_p, places=10)


class TestEffectSizes(unittest.TestCase):
    """Test effect size calculations"""
    
    def test_cramers_v(self):
        """Test Cramér's V calculation"""
        chi2 = 10.0
        n = 100
        k = 2  # 2x2 table
        
        v = compute_cramers_v(chi2, n, k)
        
        # Manual calculation
        expected = np.sqrt(chi2 / (n * (k - 1)))
        self.assertAlmostEqual(v, expected)
    
    def test_compute_effect_sizes(self):
        """Test comprehensive effect size calculation"""
        # Two-group comparison
        group1 = np.array([1, 2, 3, 4, 5])
        group2 = np.array([3, 4, 5, 6, 7])
        
        effects = compute_effect_sizes(group1, group2, test_type='t-test')
        
        # Should include Cohen's d
        self.assertIn('cohens_d', effects)
        self.assertIn('hedges_g', effects)
        self.assertIn('glass_delta', effects)
        
        # Cohen's d should be positive (group2 > group1)
        self.assertGreater(effects['cohens_d'], 0)


class TestTTest(unittest.TestCase):
    """Test t-test with D068"""
    
    def test_independent_t_test(self):
        """Test independent samples t-test"""
        np.random.seed(42)
        group1 = np.random.normal(10, 2, 30)
        group2 = np.random.normal(12, 2, 30)
        
        result = t_test_d068(
            group1, group2,
            paired=False,
            correction='fdr'
        )
        
        # Check structure
        self.assertIn('t', result)
        self.assertIn('p_uncorrected', result)
        self.assertIn('p_corrected', result)
        self.assertIn('cohens_d', result)
        self.assertIn('df', result)
        self.assertIn('ci_lower', result)
        self.assertIn('ci_upper', result)
        
        # Should detect difference
        self.assertLess(result['p_uncorrected'], 0.05)
    
    def test_paired_t_test(self):
        """Test paired samples t-test"""
        np.random.seed(42)
        pre = np.random.normal(10, 2, 30)
        post = pre + np.random.normal(2, 1, 30)  # Add improvement
        
        result = t_test_d068(
            pre, post,
            paired=True
        )
        
        # Should detect improvement
        self.assertLess(result['p_uncorrected'], 0.01)
        
        # Effect size should be positive
        self.assertGreater(result['cohens_d'], 0)


class TestNonParametric(unittest.TestCase):
    """Test non-parametric tests with D068"""
    
    def test_kruskal_wallis(self):
        """Test Kruskal-Wallis H test"""
        np.random.seed(42)
        # Three groups with different medians
        group1 = np.random.exponential(2, 30)
        group2 = np.random.exponential(3, 30)
        group3 = np.random.exponential(4, 30)
        
        result = kruskal_wallis_d068([group1, group2, group3])
        
        # Check structure
        self.assertIn('H', result)
        self.assertIn('p_uncorrected', result)
        self.assertIn('p_corrected', result)
        self.assertIn('eta_squared', result)
        
        # H should be positive
        self.assertGreater(result['H'], 0)
    
    def test_mann_whitney(self):
        """Test Mann-Whitney U test"""
        np.random.seed(42)
        group1 = np.random.exponential(2, 30)
        group2 = np.random.exponential(3, 30)
        
        result = mann_whitney_d068(group1, group2)
        
        # Check structure
        self.assertIn('U', result)
        self.assertIn('p_uncorrected', result)
        self.assertIn('p_corrected', result)
        self.assertIn('rank_biserial', result)
        
        # U should be positive
        self.assertGreaterEqual(result['U'], 0)
    
    def test_friedman(self):
        """Test Friedman test for repeated measures"""
        np.random.seed(42)
        # Three time points
        time1 = np.random.normal(10, 2, 20)
        time2 = time1 + np.random.normal(1, 1, 20)
        time3 = time2 + np.random.normal(1, 1, 20)
        
        result = friedman_test_d068([time1, time2, time3])
        
        # Check structure
        self.assertIn('chi2', result)
        self.assertIn('p_uncorrected', result)
        self.assertIn('p_corrected', result)
        self.assertIn('kendall_w', result)
        
        # Should detect trend
        self.assertLess(result['p_uncorrected'], 0.05)


if __name__ == '__main__':
    unittest.main()