"""
Tests for validate_probability_range validator.

Purpose: Validate probability values are in [0, 1] with no NaN/inf
Used by: RQ 5.9 probability transformation validation
"""

import numpy as np
import pandas as pd
import pytest
from tools.validation import validate_probability_range


class TestValidateProbabilityRange:
    """Tests for validate_probability_range validator."""

    def test_basic_structure(self):
        """Test basic output structure."""
        df = pd.DataFrame({'prob': [0.1, 0.5, 0.9]})
        result = validate_probability_range(df, prob_columns=['prob'])

        assert 'valid' in result
        assert 'message' in result
        assert 'violations' in result
        assert isinstance(result['valid'], bool)
        assert isinstance(result['message'], str)
        assert isinstance(result['violations'], list)

    def test_valid_probabilities_in_range(self):
        """Test valid probabilities [0, 1]."""
        df = pd.DataFrame({'prob': [0.0, 0.25, 0.50, 0.75, 1.0]})
        result = validate_probability_range(df, prob_columns=['prob'])

        assert result['valid'] is True
        assert len(result['violations']) == 0
        assert 'All probability values valid' in result['message']

    def test_probability_below_zero_invalid(self):
        """Test probabilities < 0 are invalid."""
        df = pd.DataFrame({'prob': [0.5, -0.1, 0.8]})
        result = validate_probability_range(df, prob_columns=['prob'])

        assert result['valid'] is False
        assert len(result['violations']) > 0
        assert 'below 0' in result['message'].lower() or 'negative' in result['message'].lower()

    def test_probability_above_one_invalid(self):
        """Test probabilities > 1 are invalid."""
        df = pd.DataFrame({'prob': [0.5, 1.2, 0.8]})
        result = validate_probability_range(df, prob_columns=['prob'])

        assert result['valid'] is False
        assert len(result['violations']) > 0
        assert 'above 1' in result['message'].lower() or '>1' in result['message']

    def test_boundary_values_valid(self):
        """Test 0 and 1 are valid (inclusive)."""
        df = pd.DataFrame({'prob': [0.0, 1.0]})
        result = validate_probability_range(df, prob_columns=['prob'])

        assert result['valid'] is True
        assert len(result['violations']) == 0

    def test_nan_values_invalid(self):
        """Test NaN values are invalid."""
        df = pd.DataFrame({'prob': [0.5, np.nan, 0.8]})
        result = validate_probability_range(df, prob_columns=['prob'])

        assert result['valid'] is False
        assert 'nan' in result['message'].lower()

    def test_infinite_values_invalid(self):
        """Test infinite values are invalid."""
        df = pd.DataFrame({'prob': [0.5, np.inf, 0.8]})
        result = validate_probability_range(df, prob_columns=['prob'])

        assert result['valid'] is False
        assert 'inf' in result['message'].lower()

    def test_multiple_columns(self):
        """Test validation across multiple probability columns."""
        df = pd.DataFrame({
            'prob_1': [0.1, 0.5, 0.9],
            'prob_2': [0.2, 0.6, 0.95],
            'prob_3': [0.0, 0.4, 1.0]
        })
        result = validate_probability_range(df, prob_columns=['prob_1', 'prob_2', 'prob_3'])

        assert result['valid'] is True
        assert len(result['violations']) == 0

    def test_multiple_columns_one_violation(self):
        """Test violation in one of multiple columns."""
        df = pd.DataFrame({
            'prob_1': [0.1, 0.5],
            'prob_2': [0.2, 1.5]  # Violation here
        })
        result = validate_probability_range(df, prob_columns=['prob_1', 'prob_2'])

        assert result['valid'] is False
        assert len(result['violations']) > 0

    def test_empty_dataframe(self):
        """Test empty DataFrame handling."""
        df = pd.DataFrame({'prob': []})
        result = validate_probability_range(df, prob_columns=['prob'])

        assert result['valid'] is True
        assert len(result['violations']) == 0

    def test_realistic_probability_transformation(self):
        """Test realistic IRT theta→probability transformation (RQ 5.9)."""
        # Probabilities from IRT GRM transformation
        df = pd.DataFrame({
            'prob_T1': [0.15, 0.30, 0.50, 0.70, 0.85],
            'prob_T2': [0.12, 0.28, 0.48, 0.68, 0.82],
            'prob_T3': [0.10, 0.25, 0.45, 0.65, 0.80],
            'prob_T4': [0.08, 0.22, 0.42, 0.62, 0.78]
        })
        prob_cols = ['prob_T1', 'prob_T2', 'prob_T3', 'prob_T4']
        result = validate_probability_range(df, prob_columns=prob_cols)

        assert result['valid'] is True
        assert len(result['violations']) == 0
        assert '4' in result['message']  # 4 columns validated
