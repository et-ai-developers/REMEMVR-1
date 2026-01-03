"""
Test suite for tools.analysis_regression module
Testing regression analysis tools for Ch7 RQs
"""

import unittest
import numpy as np
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.analysis_regression import (
    fit_multiple_regression,
    fit_hierarchical_regression, 
    compute_regression_diagnostics,
    cross_validate_regression,
    bootstrap_regression_ci,
    compute_cohens_f2,
    compute_post_hoc_power,
    variance_decomposition
)


class TestMultipleRegression(unittest.TestCase):
    """Test fit_multiple_regression function"""
    
    def setUp(self):
        """Create sample data for testing"""
        np.random.seed(42)
        n = 100
        self.X = np.random.randn(n, 3)
        self.y = 2*self.X[:, 0] + 3*self.X[:, 1] - self.X[:, 2] + np.random.randn(n)*0.5
        self.feature_names = ['age', 'education', 'income']
    
    def test_basic_regression(self):
        """Test basic multiple regression fitting"""
        result = fit_multiple_regression(self.X, self.y, self.feature_names)
        
        # Check structure
        self.assertIn('coefficients', result)
        self.assertIn('pvalues', result)
        self.assertIn('rsquared', result)
        self.assertIn('rsquared_adj', result)
        self.assertIn('residuals', result)
        self.assertIn('fvalue', result)
        self.assertIn('f_pvalue', result)
        
        # Check dimensions
        self.assertEqual(len(result['coefficients']), 4)  # intercept + 3 features
        self.assertEqual(len(result['pvalues']), 4)
        self.assertEqual(len(result['residuals']), 100)
        
        # Check approximate coefficient recovery
        self.assertAlmostEqual(result['coefficients']['age'], 2.0, places=0)
        self.assertAlmostEqual(result['coefficients']['education'], 3.0, places=0)
        
    def test_with_dataframe(self):
        """Test with pandas DataFrame input"""
        df = pd.DataFrame(self.X, columns=self.feature_names)
        result = fit_multiple_regression(df, self.y)
        
        self.assertIn('rsquared', result)
        self.assertGreater(result['rsquared'], 0.7)  # Should explain most variance


class TestHierarchicalRegression(unittest.TestCase):
    """Test fit_hierarchical_regression function"""
    
    def setUp(self):
        np.random.seed(42)
        n = 100
        self.X1 = np.random.randn(n, 2)  # Block 1
        self.X2 = np.random.randn(n, 2)  # Block 2
        self.y = 2*self.X1[:, 0] + 3*self.X1[:, 1] + self.X2[:, 0] + np.random.randn(n)*0.5
        
    def test_hierarchical_blocks(self):
        """Test hierarchical regression with blocks"""
        X_blocks = [self.X1, self.X2]
        block_names = ['demographics', 'cognitive']
        
        result = fit_hierarchical_regression(X_blocks, self.y, block_names)
        
        # Check structure
        self.assertIn('models', result)
        self.assertIn('delta_r2', result)
        self.assertIn('f_tests', result)
        
        # Should have 2 models (one per block)
        self.assertEqual(len(result['models']), 2)
        
        # Delta R² for block 2 should be positive
        self.assertGreater(result['delta_r2']['cognitive'], 0)
        
        # F-test for block 2 should have p-value
        self.assertIn('p_value', result['f_tests']['cognitive'])


class TestRegressionDiagnostics(unittest.TestCase):
    """Test compute_regression_diagnostics function"""
    
    def setUp(self):
        np.random.seed(42)
        n = 100
        self.X = np.random.randn(n, 3)
        self.y = 2*self.X[:, 0] + np.random.randn(n)*0.5
        
    def test_diagnostics_output(self):
        """Test regression diagnostics computation"""
        from statsmodels.api import OLS, add_constant
        X_with_const = add_constant(self.X)
        model = OLS(self.y, X_with_const).fit()
        
        result = compute_regression_diagnostics(model, self.X, self.y)
        
        # Check all diagnostics present
        self.assertIn('vif', result)
        self.assertIn('cooks_d', result)
        self.assertIn('leverage', result)
        self.assertIn('studentized_residuals', result)
        self.assertIn('durbin_watson', result)
        
        # Check dimensions
        self.assertEqual(len(result['vif']), 3)  # One per predictor
        self.assertEqual(len(result['cooks_d']), 100)
        self.assertEqual(len(result['leverage']), 100)


class TestCrossValidation(unittest.TestCase):
    """Test cross_validate_regression function"""
    
    def test_cv_basic(self):
        """Test basic cross-validation"""
        np.random.seed(42)
        X = np.random.randn(100, 3)
        y = 2*X[:, 0] + X[:, 1] + np.random.randn(100)*0.5
        
        result = cross_validate_regression(X, y, n_folds=5, seed=42)
        
        # Check structure
        self.assertIn('cv_scores', result)
        self.assertIn('mean_r2', result)
        self.assertIn('std_r2', result)
        self.assertIn('fold_predictions', result)
        
        # Should have 5 scores
        self.assertEqual(len(result['cv_scores']), 5)
        
        # Mean R² should be reasonable
        self.assertGreater(result['mean_r2'], 0.5)
        self.assertLess(result['mean_r2'], 1.0)


class TestBootstrapCI(unittest.TestCase):
    """Test bootstrap_regression_ci function"""
    
    def test_bootstrap_basic(self):
        """Test bootstrap confidence intervals"""
        np.random.seed(42)
        X = np.random.randn(50, 2)
        y = 2*X[:, 0] + 3*X[:, 1] + np.random.randn(50)*0.5
        
        result = bootstrap_regression_ci(X, y, n_bootstrap=100, seed=42)
        
        # Check structure
        self.assertIn('ci_lower', result)
        self.assertIn('ci_upper', result)
        self.assertIn('boot_samples', result)
        self.assertIn('point_estimate', result)
        
        # CI should contain true values
        self.assertLess(result['ci_lower'][1], 2.5)  # First coef ~ 2
        self.assertGreater(result['ci_upper'][1], 1.5)
        
        # Boot samples should have correct shape
        self.assertEqual(result['boot_samples'].shape[0], 100)  # n_bootstrap
        self.assertEqual(result['boot_samples'].shape[1], 3)  # intercept + 2 predictors


class TestEffectSizes(unittest.TestCase):
    """Test effect size calculations"""
    
    def test_cohens_f2(self):
        """Test Cohen's f² calculation"""
        r2_full = 0.50
        r2_reduced = 0.40
        
        f2 = compute_cohens_f2(r2_full, r2_reduced)
        
        # f² = (R²_full - R²_reduced) / (1 - R²_full)
        expected = (0.50 - 0.40) / (1 - 0.50)
        self.assertAlmostEqual(f2, expected)
        self.assertAlmostEqual(f2, 0.20)
        
    def test_post_hoc_power(self):
        """Test post-hoc power analysis"""
        power = compute_post_hoc_power(n=100, k_predictors=3, r2=0.25, alpha=0.05)
        
        # Should return value between 0 and 1
        self.assertGreater(power, 0)
        self.assertLess(power, 1)
        
        # Larger sample should have more power
        power_large = compute_post_hoc_power(n=200, k_predictors=3, r2=0.25)
        self.assertGreater(power_large, power)


class TestVarianceDecomposition(unittest.TestCase):
    """Test variance_decomposition function"""
    
    def test_decomposition(self):
        """Test variance decomposition"""
        # Create mock model
        model = MagicMock()
        model.rsquared = 0.64
        model.nobs = 100
        
        result = variance_decomposition(model, measurement_error=0.10)
        
        # Check structure
        self.assertIn('true_variance', result)
        self.assertIn('error_variance', result)
        self.assertIn('residual_variance', result)
        self.assertIn('icc', result)
        
        # Values should sum to 1
        total = result['true_variance'] + result['error_variance'] + result['residual_variance']
        self.assertAlmostEqual(total, 1.0, places=5)


if __name__ == '__main__':
    unittest.main()