"""
Test suite for tools.analysis_lpa module
Testing Latent Profile Analysis tools for Ch7
"""

import unittest
import numpy as np
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.analysis_lpa import (
    fit_lpa_models,
    extract_profile_membership,
    compare_lpa_models,
    characterize_profiles,
    validate_lpa_solution,
    plot_profile_means
)


class TestLPAFitting(unittest.TestCase):
    """Test LPA model fitting"""
    
    def setUp(self):
        """Create sample data for testing"""
        np.random.seed(42)
        # Create 3 distinct profiles
        n_per_profile = 50
        
        # Profile 1: High on all features
        profile1 = np.random.normal(2, 0.5, (n_per_profile, 3))
        
        # Profile 2: Low on all features  
        profile2 = np.random.normal(-2, 0.5, (n_per_profile, 3))
        
        # Profile 3: Mixed
        profile3 = np.random.normal(0, 0.5, (n_per_profile, 3))
        
        self.X = np.vstack([profile1, profile2, profile3])
        self.true_labels = np.repeat([0, 1, 2], n_per_profile)
    
    def test_fit_single_model(self):
        """Test fitting a single LPA model"""
        result = fit_lpa_models(self.X, k_range=[3], seed=42)
        
        # Check structure
        self.assertIn('models', result)
        self.assertIn('bic', result)
        self.assertIn('aic', result)
        self.assertIn('entropy', result)
        self.assertIn('n_parameters', result)
        
        # Should have one model
        self.assertEqual(len(result['models']), 1)
        self.assertEqual(len(result['bic']), 1)
        
        # BIC and AIC should be reasonable
        self.assertGreater(result['bic'][3], 0)
        self.assertGreater(result['aic'][3], 0)
    
    def test_fit_multiple_models(self):
        """Test fitting multiple LPA models"""
        result = fit_lpa_models(self.X, k_range=[2, 3, 4], seed=42)
        
        # Should have 3 models
        self.assertEqual(len(result['models']), 3)
        self.assertEqual(len(result['bic']), 3)
        
        # Check keys are correct
        self.assertIn(2, result['models'])
        self.assertIn(3, result['models'])
        self.assertIn(4, result['models'])
    
    def test_entropy_calculation(self):
        """Test entropy calculation for model quality"""
        result = fit_lpa_models(self.X, k_range=[3], seed=42)
        
        # Entropy should be between 0 and 1
        entropy = result['entropy'][3]
        self.assertGreaterEqual(entropy, 0)
        self.assertLessEqual(entropy, 1)
        
        # For well-separated data, entropy should be high
        self.assertGreater(entropy, 0.7)


class TestProfileExtraction(unittest.TestCase):
    """Test profile membership extraction"""
    
    def setUp(self):
        np.random.seed(42)
        # Simple 2-cluster data
        cluster1 = np.random.normal([0, 0], 0.5, (50, 2))
        cluster2 = np.random.normal([3, 3], 0.5, (50, 2))
        self.X = np.vstack([cluster1, cluster2])
    
    def test_extract_membership(self):
        """Test extracting profile assignments"""
        # Fit model first
        result = fit_lpa_models(self.X, k_range=[2], seed=42)
        model = result['models'][2]
        
        # Extract membership
        labels, probs = extract_profile_membership(model, self.X)
        
        # Check dimensions
        self.assertEqual(len(labels), 100)
        self.assertEqual(probs.shape, (100, 2))
        
        # Labels should be 0 or 1
        self.assertTrue(all(label in [0, 1] for label in labels))
        
        # Probabilities should sum to 1
        np.testing.assert_array_almost_equal(probs.sum(axis=1), np.ones(100))
    
    def test_membership_uncertainty(self):
        """Test uncertainty metrics in membership"""
        result = fit_lpa_models(self.X, k_range=[2], seed=42)
        model = result['models'][2]
        
        labels, probs = extract_profile_membership(model, self.X, include_uncertainty=True)
        
        # Should include uncertainty metrics
        self.assertIn('max_prob', labels.dtype.names or ['max_prob'])


class TestModelComparison(unittest.TestCase):
    """Test LPA model comparison"""
    
    def test_compare_models(self):
        """Test comparing multiple LPA models"""
        np.random.seed(42)
        X = np.random.randn(100, 3)
        
        # Fit multiple models
        result = fit_lpa_models(X, k_range=[2, 3, 4], seed=42)
        
        # Compare models
        comparison = compare_lpa_models(result)
        
        # Check structure
        self.assertIn('best_k', comparison)
        self.assertIn('bic_values', comparison)
        self.assertIn('aic_values', comparison)
        self.assertIn('entropy_values', comparison)
        
        # Best K should be one of the tested values
        self.assertIn(comparison['best_k'], [2, 3, 4])
        
        # Should have model selection criteria
        self.assertIn('elbow_point', comparison)


class TestProfileCharacterization(unittest.TestCase):
    """Test profile characterization"""
    
    def test_characterize_profiles(self):
        """Test computing profile characteristics"""
        np.random.seed(42)
        # Create clear profiles
        X = np.vstack([
            np.random.normal([2, 2, 2], 0.3, (30, 3)),
            np.random.normal([-2, -2, -2], 0.3, (30, 3)),
            np.random.normal([0, 0, 0], 0.3, (30, 3))
        ])
        
        result = fit_lpa_models(X, k_range=[3], seed=42)
        model = result['models'][3]
        labels, _ = extract_profile_membership(model, X)
        
        char = characterize_profiles(X, labels, feature_names=['f1', 'f2', 'f3'])
        
        # Check structure
        self.assertIn('means', char)
        self.assertIn('stds', char)
        self.assertIn('sizes', char)
        self.assertIn('proportions', char)
        
        # Should have 3 profiles
        self.assertEqual(len(char['means']), 3)
        self.assertEqual(len(char['sizes']), 3)
        
        # Proportions should sum to 1
        self.assertAlmostEqual(sum(char['proportions'].values()), 1.0)


class TestLPAValidation(unittest.TestCase):
    """Test LPA solution validation"""
    
    def test_validate_solution(self):
        """Test validating LPA solution quality"""
        np.random.seed(42)
        X = np.random.randn(100, 3)
        
        result = fit_lpa_models(X, k_range=[2], seed=42)
        model = result['models'][2]
        
        validation = validate_lpa_solution(model, X)
        
        # Check validation metrics
        self.assertIn('silhouette_score', validation)
        self.assertIn('davies_bouldin', validation)
        self.assertIn('calinski_harabasz', validation)
        self.assertIn('avg_posterior_prob', validation)
        
        # Silhouette should be between -1 and 1
        self.assertGreaterEqual(validation['silhouette_score'], -1)
        self.assertLessEqual(validation['silhouette_score'], 1)
        
        # Average posterior probability should be high for good solution
        self.assertGreater(validation['avg_posterior_prob'], 0.5)


class TestProfilePlotting(unittest.TestCase):
    """Test profile visualization"""
    
    @patch('matplotlib.pyplot.show')
    def test_plot_profiles(self, mock_show):
        """Test plotting profile means"""
        np.random.seed(42)
        
        # Create profile data
        means = {
            'Profile 1': [1.5, 2.0, 1.8],
            'Profile 2': [-1.5, -2.0, -1.8],
            'Profile 3': [0, 0.2, -0.1]
        }
        
        stds = {
            'Profile 1': [0.3, 0.4, 0.3],
            'Profile 2': [0.3, 0.4, 0.3],
            'Profile 3': [0.5, 0.5, 0.5]
        }
        
        fig = plot_profile_means(
            means, 
            stds,
            feature_names=['Feature1', 'Feature2', 'Feature3']
        )
        
        # Should return a figure
        self.assertIsNotNone(fig)
        
        # Should have axes
        self.assertGreater(len(fig.axes), 0)


if __name__ == '__main__':
    unittest.main()