"""
Tests for validate_numeric_range validator.

Purpose: Validate numeric values fall within specified range [min_val, max_val]
Used by: RQ 5.9 probability transformation validation
"""

import numpy as np
import pandas as pd
import pytest
from tools.validation import validate_numeric_range


class TestValidateNumericRange:
    """Tests for validate_numeric_range validator."""

    def test_basic_structure(self):
        """Test basic output structure."""
        data = np.array([1.0, 2.0, 3.0])
        result = validate_numeric_range(data, min_val=0.0, max_val=5.0, column_name='test')

        assert 'valid' in result
        assert 'message' in result
        assert 'out_of_range_count' in result
        assert 'violations' in result
        assert isinstance(result['valid'], bool)
        assert isinstance(result['message'], str)
        assert isinstance(result['out_of_range_count'], int)
        assert isinstance(result['violations'], list)

    def test_valid_range_all_within(self):
        """Test all values within valid range."""
        data = np.array([1.0, 2.5, 4.0, 0.5])
        result = validate_numeric_range(data, min_val=0.0, max_val=5.0, column_name='theta')

        assert result['valid'] is True
        assert result['out_of_range_count'] == 0
        assert len(result['violations']) == 0
        assert 'All values within range' in result['message']

    def test_values_below_minimum(self):
        """Test detection of values below minimum."""
        data = np.array([-1.0, 0.5, 1.0, -2.0])
        result = validate_numeric_range(data, min_val=0.0, max_val=5.0, column_name='theta')

        assert result['valid'] is False
        assert result['out_of_range_count'] == 2
        assert len(result['violations']) == 2
        assert -1.0 in result['violations']
        assert -2.0 in result['violations']
        assert '2 values out of range' in result['message']

    def test_values_above_maximum(self):
        """Test detection of values above maximum."""
        data = np.array([1.0, 2.0, 6.0, 7.5])
        result = validate_numeric_range(data, min_val=0.0, max_val=5.0, column_name='theta')

        assert result['valid'] is False
        assert result['out_of_range_count'] == 2
        assert len(result['violations']) == 2
        assert 6.0 in result['violations']
        assert 7.5 in result['violations']

    def test_values_both_below_and_above(self):
        """Test detection of violations in both directions."""
        data = np.array([-1.0, 2.0, 3.0, 10.0])
        result = validate_numeric_range(data, min_val=0.0, max_val=5.0, column_name='theta')

        assert result['valid'] is False
        assert result['out_of_range_count'] == 2
        assert len(result['violations']) == 2
        assert -1.0 in result['violations']
        assert 10.0 in result['violations']

    def test_boundary_values_inclusive(self):
        """Test boundary values are considered valid (inclusive range)."""
        data = np.array([0.0, 2.5, 5.0])
        result = validate_numeric_range(data, min_val=0.0, max_val=5.0, column_name='theta')

        assert result['valid'] is True
        assert result['out_of_range_count'] == 0
        assert len(result['violations']) == 0

    def test_pandas_series_input(self):
        """Test works with pandas Series input."""
        data = pd.Series([1.0, 2.0, 3.0], name='theta')
        result = validate_numeric_range(data, min_val=0.0, max_val=5.0, column_name='theta')

        assert result['valid'] is True
        assert result['out_of_range_count'] == 0

    def test_empty_data(self):
        """Test empty data handling."""
        data = np.array([])
        result = validate_numeric_range(data, min_val=0.0, max_val=5.0, column_name='theta')

        assert result['valid'] is True
        assert result['out_of_range_count'] == 0
        assert len(result['violations']) == 0

    def test_nan_values_reported(self):
        """Test NaN values are reported as violations."""
        data = np.array([1.0, np.nan, 3.0, np.nan])
        result = validate_numeric_range(data, min_val=0.0, max_val=5.0, column_name='theta')

        assert result['valid'] is False
        assert result['out_of_range_count'] >= 2  # At least 2 NaN violations
        assert 'NaN' in result['message'] or 'nan' in result['message'].lower()

    def test_infinite_values_reported(self):
        """Test infinite values are reported as violations."""
        data = np.array([1.0, np.inf, 3.0, -np.inf])
        result = validate_numeric_range(data, min_val=0.0, max_val=5.0, column_name='theta')

        assert result['valid'] is False
        assert result['out_of_range_count'] >= 2
        assert 'inf' in result['message'].lower()

    def test_column_name_in_message(self):
        """Test column name appears in error message."""
        data = np.array([10.0])
        result = validate_numeric_range(data, min_val=0.0, max_val=5.0, column_name='theta_scores')

        assert 'theta_scores' in result['message']

    def test_realistic_theta_range(self):
        """Test realistic theta score range validation (RQ 5.9 scenario)."""
        # Realistic theta scores from IRT calibration
        theta = np.array([-2.5, -1.0, 0.0, 1.5, 2.8, -3.1])  # One outlier at -3.1
        result = validate_numeric_range(theta, min_val=-3.0, max_val=3.0, column_name='theta')

        assert result['valid'] is False
        assert result['out_of_range_count'] == 1
        assert -3.1 in result['violations']
        assert 'theta' in result['message']
