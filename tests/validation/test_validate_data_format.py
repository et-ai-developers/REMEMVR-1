"""
Tests for validate_data_format validator.

Purpose: Validate DataFrame has required columns with no missing values
Used by: RQ 5.9 fixed effects table validation
"""

import numpy as np
import pandas as pd
import pytest
from tools.validation import validate_data_format


class TestValidateDataFormat:
    """Tests for validate_data_format validator."""

    def test_basic_structure(self):
        """Test basic output structure."""
        df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        result = validate_data_format(df, required_cols=['col1'])

        assert 'valid' in result
        assert 'message' in result
        assert 'missing_cols' in result
        assert isinstance(result['valid'], bool)
        assert isinstance(result['message'], str)
        assert isinstance(result['missing_cols'], list)

    def test_valid_all_columns_present(self):
        """Test DataFrame with all required columns present."""
        df = pd.DataFrame({
            'predictor': ['Age', 'Domain', 'Time'],
            'coef': [0.1, 0.2, 0.3],
            'se': [0.01, 0.02, 0.03],
            'p_value': [0.001, 0.01, 0.05]
        })
        required_cols = ['predictor', 'coef', 'se', 'p_value']
        result = validate_data_format(df, required_cols=required_cols)

        assert result['valid'] is True
        assert len(result['missing_cols']) == 0
        assert 'All required columns present' in result['message']

    def test_missing_single_column(self):
        """Test detection of single missing column."""
        df = pd.DataFrame({
            'predictor': ['Age', 'Domain'],
            'coef': [0.1, 0.2],
            'se': [0.01, 0.02]
        })
        required_cols = ['predictor', 'coef', 'se', 'p_value']
        result = validate_data_format(df, required_cols=required_cols)

        assert result['valid'] is False
        assert 'p_value' in result['missing_cols']
        assert len(result['missing_cols']) == 1
        assert 'Missing required columns' in result['message']

    def test_missing_multiple_columns(self):
        """Test detection of multiple missing columns."""
        df = pd.DataFrame({
            'predictor': ['Age', 'Domain'],
            'coef': [0.1, 0.2]
        })
        required_cols = ['predictor', 'coef', 'se', 'p_value', 'ci_lower', 'ci_upper']
        result = validate_data_format(df, required_cols=required_cols)

        assert result['valid'] is False
        assert 'se' in result['missing_cols']
        assert 'p_value' in result['missing_cols']
        assert 'ci_lower' in result['missing_cols']
        assert 'ci_upper' in result['missing_cols']
        assert len(result['missing_cols']) == 4

    def test_extra_columns_allowed(self):
        """Test extra columns don't interfere with validation."""
        df = pd.DataFrame({
            'predictor': ['Age'],
            'coef': [0.1],
            'extra_col': ['ignored']
        })
        required_cols = ['predictor', 'coef']
        result = validate_data_format(df, required_cols=required_cols)

        assert result['valid'] is True
        assert len(result['missing_cols']) == 0

    def test_empty_dataframe(self):
        """Test empty DataFrame handling."""
        df = pd.DataFrame()
        required_cols = ['predictor', 'coef']
        result = validate_data_format(df, required_cols=required_cols)

        assert result['valid'] is False
        assert 'predictor' in result['missing_cols']
        assert 'coef' in result['missing_cols']

    def test_empty_required_cols_list(self):
        """Test with empty required_cols list (trivially valid)."""
        df = pd.DataFrame({'col1': [1, 2]})
        result = validate_data_format(df, required_cols=[])

        assert result['valid'] is True
        assert len(result['missing_cols']) == 0

    def test_case_sensitive_column_names(self):
        """Test column names are case-sensitive."""
        df = pd.DataFrame({'PREDICTOR': ['Age'], 'coef': [0.1]})
        required_cols = ['predictor', 'coef']
        result = validate_data_format(df, required_cols=required_cols)

        assert result['valid'] is False
        assert 'predictor' in result['missing_cols']  # lowercase not found

    def test_column_order_irrelevant(self):
        """Test column order doesn't matter."""
        df = pd.DataFrame({
            'p_value': [0.05],
            'predictor': ['Age'],
            'coef': [0.1]
        })
        required_cols = ['predictor', 'coef', 'p_value']
        result = validate_data_format(df, required_cols=required_cols)

        assert result['valid'] is True

    def test_nan_values_in_columns_allowed(self):
        """Test NaN values in data don't affect column presence check."""
        df = pd.DataFrame({
            'predictor': ['Age', None],
            'coef': [0.1, np.nan]
        })
        required_cols = ['predictor', 'coef']
        result = validate_data_format(df, required_cols=required_cols)

        # Column presence check only - NaN values don't matter for this validator
        assert result['valid'] is True

    def test_realistic_lmm_fixed_effects(self):
        """Test realistic LMM fixed effects table (RQ 5.9 scenario)."""
        df = pd.DataFrame({
            'term': ['Intercept', 'Age_c', 'Domain[T.What]', 'Domain[T.When]', 'TSVR_hours'],
            'coef': [1.5, 0.02, -0.3, -0.5, -0.1],
            'se': [0.05, 0.01, 0.08, 0.09, 0.02],
            'z': [30.0, 2.0, -3.75, -5.56, -5.0],
            'p_uncorrected': [0.000, 0.046, 0.0002, 0.0000, 0.0000],
            'p_bonferroni': [0.000, 0.230, 0.0010, 0.0000, 0.0000]
        })
        required_cols = ['term', 'coef', 'se', 'z', 'p_uncorrected', 'p_bonferroni']
        result = validate_data_format(df, required_cols=required_cols)

        assert result['valid'] is True
        assert len(result['missing_cols']) == 0
