"""Test suite for clinical analysis module using TDD."""

import numpy as np
import pandas as pd
import pytest
from unittest.mock import Mock, patch

# Import the functions we're about to create
from tools.clinical import (
    compute_sensitivity_specificity,
    compute_roc_auc,
    compute_diagnostic_odds_ratio,
    compute_youden_index,
    compute_likelihood_ratios
)


class TestComputeSensitivitySpecificity:
    """Test sensitivity, specificity and related metrics."""
    
    def test_perfect_classification(self):
        """Test with perfect classification."""
        y_true = np.array([1, 1, 1, 0, 0, 0])
        y_pred = np.array([1, 1, 1, 0, 0, 0])
        
        result = compute_sensitivity_specificity(y_true, y_pred)
        
        assert 'sensitivity' in result
        assert 'specificity' in result
        assert 'ppv' in result  # Positive Predictive Value
        assert 'npv' in result  # Negative Predictive Value
        assert 'accuracy' in result
        assert 'balanced_accuracy' in result
        
        # Perfect classification
        assert result['sensitivity'] == 1.0
        assert result['specificity'] == 1.0
        assert result['ppv'] == 1.0
        assert result['npv'] == 1.0
        assert result['accuracy'] == 1.0
        assert result['balanced_accuracy'] == 1.0
    
    def test_all_false_positives(self):
        """Test when all negatives are misclassified."""
        y_true = np.array([1, 1, 0, 0, 0])
        y_pred = np.array([1, 1, 1, 1, 1])  # All predicted positive
        
        result = compute_sensitivity_specificity(y_true, y_pred)
        
        assert result['sensitivity'] == 1.0  # All positives detected
        assert result['specificity'] == 0.0  # No negatives detected
        assert result['ppv'] == 2/5  # 2 true positives out of 5 predicted
        assert result['npv'] == 0.0  # No true negatives
    
    def test_all_false_negatives(self):
        """Test when all positives are misclassified."""
        y_true = np.array([1, 1, 1, 0, 0])
        y_pred = np.array([0, 0, 0, 0, 0])  # All predicted negative
        
        result = compute_sensitivity_specificity(y_true, y_pred)
        
        assert result['sensitivity'] == 0.0  # No positives detected
        assert result['specificity'] == 1.0  # All negatives detected
        assert result['ppv'] == 0.0  # No true positives
        assert result['npv'] == 2/5  # 2 true negatives out of 5 predicted
    
    def test_confusion_matrix_included(self):
        """Test that confusion matrix is included."""
        y_true = np.array([1, 1, 0, 0, 1, 0])
        y_pred = np.array([1, 0, 0, 1, 1, 0])
        
        result = compute_sensitivity_specificity(y_true, y_pred, 
                                                  return_confusion_matrix=True)
        
        assert 'confusion_matrix' in result
        assert 'tp' in result  # True positives
        assert 'tn' in result  # True negatives
        assert 'fp' in result  # False positives
        assert 'fn' in result  # False negatives
        
        # Check counts
        assert result['tp'] == 2  # [1,1] and [1,1] at positions 0 and 4
        assert result['tn'] == 2  # [0,0] at positions 2 and 5
        assert result['fp'] == 1  # [0,1] at position 3
        assert result['fn'] == 1  # [1,0] at position 1
    
    def test_with_threshold(self):
        """Test with probability scores and threshold."""
        y_true = np.array([1, 1, 0, 0, 1, 0])
        y_scores = np.array([0.9, 0.8, 0.3, 0.2, 0.7, 0.4])
        
        # Test with default threshold (0.5)
        result = compute_sensitivity_specificity(y_true, y_scores=y_scores, threshold=0.5)
        
        # y_pred would be [1, 1, 0, 0, 1, 0] at threshold 0.5
        assert result['sensitivity'] == 1.0
        assert result['specificity'] == 1.0
        
        # Test with different threshold
        result2 = compute_sensitivity_specificity(y_true, y_scores=y_scores, threshold=0.75)
        
        # y_pred would be [1, 1, 0, 0, 0, 0] at threshold 0.75
        assert result2['sensitivity'] == 2/3  # 2 out of 3 positives detected
        assert result2['specificity'] == 1.0  # All negatives correctly classified


class TestComputeROCAUC:
    """Test ROC curve and AUC calculation."""
    
    def test_perfect_classifier(self):
        """Test ROC AUC for perfect classifier."""
        y_true = np.array([1, 1, 0, 0, 1, 0])
        y_scores = np.array([0.9, 0.95, 0.1, 0.05, 0.85, 0.2])
        
        result = compute_roc_auc(y_true, y_scores)
        
        assert 'auc' in result
        assert 'fpr' in result  # False positive rates
        assert 'tpr' in result  # True positive rates
        assert 'thresholds' in result
        
        # Perfect classifier should have AUC = 1.0
        assert result['auc'] == 1.0
        assert len(result['fpr']) == len(result['tpr'])
        assert len(result['fpr']) == len(result['thresholds'])
    
    def test_random_classifier(self):
        """Test ROC AUC for random classifier."""
        np.random.seed(42)
        y_true = np.random.randint(0, 2, 100)
        y_scores = np.random.rand(100)  # Random scores
        
        result = compute_roc_auc(y_true, y_scores)
        
        # Random classifier should have AUC ≈ 0.5
        assert 0.3 < result['auc'] < 0.7
    
    def test_confidence_intervals(self):
        """Test bootstrap confidence intervals for AUC."""
        np.random.seed(42)
        y_true = np.array([1, 1, 0, 0, 1, 0, 1, 0, 1, 0])
        y_scores = np.array([0.8, 0.7, 0.3, 0.2, 0.9, 0.4, 0.75, 0.35, 0.85, 0.25])
        
        result = compute_roc_auc(y_true, y_scores, bootstrap_ci=True, 
                                  n_bootstrap=100, seed=42)
        
        assert 'auc_ci_lower' in result
        assert 'auc_ci_upper' in result
        assert result['auc_ci_lower'] <= result['auc'] <= result['auc_ci_upper']


class TestComputeDiagnosticOddsRatio:
    """Test diagnostic odds ratio calculation."""
    
    def test_perfect_test(self):
        """Test DOR for perfect diagnostic test."""
        y_true = np.array([1, 1, 0, 0])
        y_pred = np.array([1, 1, 0, 0])
        
        result = compute_diagnostic_odds_ratio(y_true, y_pred)
        
        assert 'dor' in result
        assert 'ci_lower' in result
        assert 'ci_upper' in result
        assert 'log_dor' in result
        
        # Perfect test has high DOR (with Haldane correction it's not infinite)
        assert result['dor'] > 10  # (2.5*2.5)/(0.5*0.5) = 25
    
    def test_moderate_test(self):
        """Test DOR for moderate diagnostic test."""
        # TP=7, FN=3, FP=2, TN=8
        y_true = np.array([1]*10 + [0]*10)
        y_pred = np.array([1]*7 + [0]*3 + [1]*2 + [0]*8)
        
        result = compute_diagnostic_odds_ratio(y_true, y_pred)
        
        # DOR with Haldane correction = (7.5*8.5)/(2.5*3.5) = 63.75/8.75 = 7.29
        assert 7 < result['dor'] < 8
        assert result['ci_lower'] < result['dor'] < result['ci_upper']
    
    def test_worthless_test(self):
        """Test DOR for worthless diagnostic test."""
        # Random predictions
        np.random.seed(42)
        y_true = np.array([1, 1, 1, 0, 0, 0])
        y_pred = np.array([0, 1, 0, 1, 0, 1])  # Random
        
        result = compute_diagnostic_odds_ratio(y_true, y_pred)
        
        # Worthless test has DOR ≈ 1
        assert 0.1 < result['dor'] < 10


class TestComputeYoudenIndex:
    """Test Youden's J statistic calculation."""
    
    def test_perfect_classifier(self):
        """Test Youden index for perfect classifier."""
        y_true = np.array([1, 1, 0, 0])
        y_scores = np.array([0.9, 0.8, 0.2, 0.1])
        
        result = compute_youden_index(y_true, y_scores)
        
        assert 'youden_j' in result
        assert 'optimal_threshold' in result
        assert 'sensitivity_at_threshold' in result
        assert 'specificity_at_threshold' in result
        
        # Perfect classifier has J = 1
        assert result['youden_j'] == 1.0
        assert 0.2 <= result['optimal_threshold'] <= 0.8
    
    def test_random_classifier(self):
        """Test Youden index for random classifier."""
        np.random.seed(42)
        y_true = np.random.randint(0, 2, 50)
        y_scores = np.random.rand(50)
        
        result = compute_youden_index(y_true, y_scores)
        
        # Random classifier has J ≈ 0
        assert -0.3 < result['youden_j'] < 0.3


class TestComputeLikelihoodRatios:
    """Test likelihood ratio calculations."""
    
    def test_good_test(self):
        """Test LR+ and LR- for good diagnostic test."""
        # Sens=0.8, Spec=0.9
        y_true = np.array([1]*10 + [0]*10)
        y_pred = np.array([1]*8 + [0]*2 + [1]*1 + [0]*9)
        
        result = compute_likelihood_ratios(y_true, y_pred)
        
        assert 'lr_positive' in result
        assert 'lr_negative' in result
        assert 'lr_positive_ci' in result
        assert 'lr_negative_ci' in result
        
        # LR+ = sens/(1-spec) = 0.8/0.1 = 8
        assert 7 < result['lr_positive'] < 9
        # LR- = (1-sens)/spec = 0.2/0.9 = 0.22
        assert 0.2 < result['lr_negative'] < 0.25
    
    def test_interpretation(self):
        """Test LR interpretation categories."""
        # Strong positive test
        y_true = np.array([1]*5 + [0]*5)
        y_pred = np.array([1]*5 + [0]*5)  # Perfect
        
        result = compute_likelihood_ratios(y_true, y_pred, 
                                            include_interpretation=True)
        
        assert 'lr_positive_interpretation' in result
        assert 'lr_negative_interpretation' in result
        
        # LR+ > 10 is "Strong positive"
        assert 'strong' in result['lr_positive_interpretation'].lower()
        # LR- < 0.1 is "Strong negative"
        assert 'strong' in result['lr_negative_interpretation'].lower()