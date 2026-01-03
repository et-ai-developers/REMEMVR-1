"""
Test suite for tools.data module
Testing data extraction and preprocessing tools for Ch7
"""

import unittest
import numpy as np
import pandas as pd
from unittest.mock import patch, MagicMock, mock_open
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.data import (
    extract_cognitive_tests,
    standardize_to_t_scores,
    extract_domain_theta_scores,
    merge_theta_cognitive,
    extract_dass_scores,
    extract_sleep_per_test,
    extract_discrepancy_scores,
    load_participant_data,
    load_test_data
)


class TestDataLoading(unittest.TestCase):
    """Test basic data loading functions"""
    
    def setUp(self):
        """Create mock data"""
        # Create participant-level data (100 rows)
        np.random.seed(42)
        self.df_nonvr = pd.DataFrame({
            'uid': [f'P{i:03d}' for i in range(1, 101)],
            'age': np.random.randint(18, 80, 100),
            'ravlt_total': np.random.randint(30, 75, 100),
            'bvmt_total': np.random.randint(20, 36, 100),
            'nart_iq': np.random.normal(100, 15, 100),
            'rpm_score': np.random.randint(0, 60, 100),
            'dass_d': np.random.randint(0, 42, 100),
            'dass_a': np.random.randint(0, 42, 100),
            'dass_s': np.random.randint(0, 42, 100)
        })
        
        # Create test-level data (400 rows - 4 per participant)
        test_data = []
        for i in range(1, 101):
            for test in range(1, 5):
                test_data.append({
                    'uid': f'P{i:03d}',
                    'test_number': test,
                    'sleep_hours': np.random.uniform(4, 10),
                    'strategy_score': np.random.randint(1, 5),
                    'accuracy': np.random.uniform(0.3, 1.0)
                })
        self.df_data = pd.DataFrame(test_data)
    
    @patch('tools.data.pd.read_csv')
    @patch('tools.data.os.path.exists')
    def test_load_participant_data(self, mock_exists, mock_read_csv):
        """Test loading participant-level data"""
        mock_exists.return_value = True
        mock_read_csv.return_value = self.df_nonvr
        
        df = load_participant_data()
        
        mock_read_csv.assert_called_once_with('./data/dfnonvr.csv')
        self.assertEqual(len(df), 100)
        self.assertIn('uid', df.columns)
    
    @patch('tools.data.pd.read_csv')
    @patch('tools.data.os.path.exists')
    def test_load_test_data(self, mock_exists, mock_read_csv):
        """Test loading test-level data"""
        mock_exists.return_value = True
        mock_read_csv.return_value = self.df_data
        
        df = load_test_data()
        
        mock_read_csv.assert_called_once_with('./data/dfdata.csv')
        self.assertEqual(len(df), 400)
        self.assertIn('test_number', df.columns)


class TestCognitiveExtraction(unittest.TestCase):
    """Test cognitive test extraction"""
    
    def setUp(self):
        np.random.seed(42)
        self.df_nonvr = pd.DataFrame({
            'uid': [f'P{i:03d}' for i in range(1, 11)],
            'ravlt_total': np.random.randint(30, 75, 10),
            'bvmt_total': np.random.randint(20, 36, 10),
            'nart_iq': np.random.normal(100, 15, 10),
            'rpm_score': np.random.randint(0, 60, 10)
        })
    
    @patch('tools.data.load_participant_data')
    def test_extract_cognitive_tests(self, mock_load):
        """Test extracting cognitive test scores"""
        mock_load.return_value = self.df_nonvr
        
        # Extract for specific UIDs
        uid_list = ['P001', 'P002', 'P003']
        result = extract_cognitive_tests(uid_list)
        
        # Check structure
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 3)
        
        # Check columns present
        for col in ['uid', 'ravlt_total', 'bvmt_total', 'nart_iq', 'rpm_score']:
            self.assertIn(col, result.columns)
        
        # Check filtering worked
        self.assertTrue(all(uid in uid_list for uid in result['uid']))
    
    @patch('tools.data.load_participant_data')
    def test_extract_cognitive_all(self, mock_load):
        """Test extracting all participants when no list provided"""
        mock_load.return_value = self.df_nonvr
        
        result = extract_cognitive_tests()
        
        self.assertEqual(len(result), 10)


class TestStandardization(unittest.TestCase):
    """Test score standardization functions"""
    
    def test_t_score_conversion(self):
        """Test conversion to T-scores (M=50, SD=10)"""
        # Create scores with known mean and SD
        scores = np.array([85, 100, 115])  # IQ scores
        population_mean = 100
        population_sd = 15
        
        t_scores = standardize_to_t_scores(scores, population_mean, population_sd)
        
        # Check T-score conversion
        # T = 50 + 10 * (score - mean) / sd
        expected = np.array([40, 50, 60])  # (85-100)/15*10+50=40, etc.
        np.testing.assert_array_almost_equal(t_scores, expected)
    
    def test_t_score_series(self):
        """Test with pandas Series input"""
        scores = pd.Series([90, 100, 110])
        t_scores = standardize_to_t_scores(scores, 100, 10)
        
        expected = np.array([40, 50, 60])
        np.testing.assert_array_almost_equal(t_scores, expected)


class TestThetaExtraction(unittest.TestCase):
    """Test theta score extraction from Ch5 results"""
    
    def test_extract_domain_theta(self):
        """Test extracting domain-specific theta scores"""
        # The function will use mock data since file doesn't exist
        result = extract_domain_theta_scores(
            rq_path='results/ch5/5.2.1',
            domain='verbal'
        )
        
        # Check structure
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn('uid', result.columns)
        self.assertIn('theta_mean', result.columns)
        
        # Should have 100 rows from mock data
        self.assertEqual(len(result), 100)
        
        # Check theta values are reasonable (normal distribution)
        self.assertLess(result['theta_mean'].mean(), 2.0)
        self.assertGreater(result['theta_mean'].mean(), -2.0)


class TestMerging(unittest.TestCase):
    """Test merging theta and cognitive data"""
    
    def test_merge_data(self):
        """Test merging theta scores with cognitive predictors"""
        theta_df = pd.DataFrame({
            'uid': ['P001', 'P002', 'P003'],
            'theta_mean': [0.5, 0.3, -0.2]
        })
        
        cognitive_df = pd.DataFrame({
            'uid': ['P001', 'P002', 'P003', 'P004'],
            'ravlt': [50, 45, 60, 55],
            'bvmt': [30, 28, 35, 32]
        })
        
        result = merge_theta_cognitive(theta_df, cognitive_df)
        
        # Should inner join by default
        self.assertEqual(len(result), 3)
        self.assertIn('theta_mean', result.columns)
        self.assertIn('ravlt', result.columns)
        self.assertIn('bvmt', result.columns)
        
        # Check merge is correct
        self.assertEqual(result[result['uid'] == 'P001']['ravlt'].values[0], 50)


class TestDASSExtraction(unittest.TestCase):
    """Test DASS score extraction"""
    
    @patch('tools.data.load_participant_data')
    def test_extract_dass(self, mock_load):
        """Test extracting DASS subscales"""
        mock_df = pd.DataFrame({
            'uid': ['P001', 'P002', 'P003'],
            'dass_d': [10, 15, 20],
            'dass_a': [8, 12, 16],
            'dass_s': [14, 18, 22]
        })
        mock_load.return_value = mock_df
        
        result = extract_dass_scores(['P001', 'P002'])
        
        self.assertEqual(len(result), 2)
        self.assertIn('dass_d', result.columns)
        self.assertIn('dass_a', result.columns)
        self.assertIn('dass_s', result.columns)
        
        # Check values
        self.assertEqual(result[result['uid'] == 'P001']['dass_d'].values[0], 10)


class TestSleepExtraction(unittest.TestCase):
    """Test sleep data extraction"""
    
    @patch('tools.data.load_test_data')
    def test_extract_sleep_per_test(self, mock_load):
        """Test extracting sleep hours for specific test"""
        mock_df = pd.DataFrame({
            'uid': ['P001', 'P001', 'P002', 'P002'],
            'test_number': [1, 2, 1, 2],
            'sleep_hours': [7.5, 6.0, 8.0, 7.0]
        })
        mock_load.return_value = mock_df
        
        result = extract_sleep_per_test(uid_list=['P001', 'P002'], test_num=1)
        
        self.assertEqual(len(result), 2)
        self.assertIn('sleep_hours', result.columns)
        
        # Check correct test extracted
        self.assertEqual(result[result['uid'] == 'P001']['sleep_hours'].values[0], 7.5)
        self.assertEqual(result[result['uid'] == 'P002']['sleep_hours'].values[0], 8.0)


class TestDiscrepancyScores(unittest.TestCase):
    """Test discrepancy score calculation"""
    
    def test_compute_discrepancy(self):
        """Test computing standardized discrepancy scores"""
        traditional_scores = pd.Series([50, 55, 60, 45])
        vr_scores = pd.Series([55, 50, 65, 40])
        
        result = extract_discrepancy_scores(traditional_scores, vr_scores)
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn('discrepancy', result.columns)
        self.assertIn('z_score', result.columns)
        
        # Check discrepancy calculation
        expected_disc = vr_scores - traditional_scores
        np.testing.assert_array_almost_equal(result['discrepancy'], expected_disc)
        
        # Check z-scores are standardized
        self.assertAlmostEqual(result['z_score'].mean(), 0, places=5)
        self.assertAlmostEqual(result['z_score'].std(ddof=0), 1, places=5)


if __name__ == '__main__':
    unittest.main()