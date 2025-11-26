"""
Test suite for validate_dataframe_structure function.

Tests DataFrame structure validation (rows, columns, types).
"""

import pytest
import pandas as pd
import numpy as np
from tools.validation import validate_dataframe_structure


class TestValidateDataframeStructure:
    """Test validate_dataframe_structure function."""

    def test_basic_structure(self):
        """Test function returns expected keys."""
        df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        result = validate_dataframe_structure(df, expected_rows=2, expected_columns=['A', 'B'])

        assert 'valid' in result
        assert 'message' in result
        assert 'checks' in result
        assert isinstance(result['valid'], bool)
        assert isinstance(result['message'], str)
        assert isinstance(result['checks'], dict)

    def test_valid_exact_rows_and_columns(self):
        """Test valid DataFrame with exact row count and columns."""
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        result = validate_dataframe_structure(df, expected_rows=3, expected_columns=['A', 'B'])

        assert result['valid'] is True
        assert result['checks']['row_count_valid'] is True
        assert result['checks']['columns_valid'] is True

    def test_valid_row_range(self):
        """Test valid DataFrame with row count in range."""
        df = pd.DataFrame({'A': [1, 2, 3, 4]})
        result = validate_dataframe_structure(df, expected_rows=(3, 5), expected_columns=['A'])

        assert result['valid'] is True
        assert result['checks']['row_count_valid'] is True

    def test_invalid_row_count_too_few(self):
        """Test DataFrame with too few rows."""
        df = pd.DataFrame({'A': [1, 2]})
        result = validate_dataframe_structure(df, expected_rows=3, expected_columns=['A'])

        assert result['valid'] is False
        assert result['checks']['row_count_valid'] is False

    def test_invalid_row_count_too_many(self):
        """Test DataFrame with too many rows."""
        df = pd.DataFrame({'A': [1, 2, 3, 4, 5]})
        result = validate_dataframe_structure(df, expected_rows=(1, 3), expected_columns=['A'])

        assert result['valid'] is False
        assert result['checks']['row_count_valid'] is False

    def test_invalid_missing_columns(self):
        """Test DataFrame missing required columns."""
        df = pd.DataFrame({'A': [1, 2]})
        result = validate_dataframe_structure(df, expected_rows=2, expected_columns=['A', 'B'])

        assert result['valid'] is False
        assert result['checks']['columns_valid'] is False
        assert 'B' in result['checks']['missing_columns']

    def test_valid_extra_columns_allowed(self):
        """Test DataFrame with extra columns (should be valid)."""
        df = pd.DataFrame({'A': [1, 2], 'B': [3, 4], 'C': [5, 6]})
        result = validate_dataframe_structure(df, expected_rows=2, expected_columns=['A', 'B'])

        assert result['valid'] is True

    def test_valid_column_types(self):
        """Test DataFrame with correct column types."""
        df = pd.DataFrame({'A': [1, 2], 'B': ['x', 'y']})
        result = validate_dataframe_structure(
            df,
            expected_rows=2,
            expected_columns=['A', 'B'],
            column_types={'A': (int, np.integer), 'B': (str, object)}
        )

        assert result['valid'] is True
        assert result['checks']['types_valid'] is True

    def test_invalid_column_types(self):
        """Test DataFrame with incorrect column types."""
        df = pd.DataFrame({'A': ['x', 'y'], 'B': [1, 2]})
        result = validate_dataframe_structure(
            df,
            expected_rows=2,
            expected_columns=['A', 'B'],
            column_types={'A': (int, np.integer), 'B': (str, object)}
        )

        assert result['valid'] is False
        assert result['checks']['types_valid'] is False

    def test_realistic_rq_5_14_scenario(self):
        """Test realistic RQ 5.14 clustering assignments DataFrame."""
        # K-means cluster assignments (N=100, K=3)
        np.random.seed(42)
        df = pd.DataFrame({
            'UID': [f'A{i:03d}' for i in range(100)],
            'cluster': np.random.choice([0, 1, 2], 100)
        })

        result = validate_dataframe_structure(
            df,
            expected_rows=100,
            expected_columns=['UID', 'cluster']
        )

        assert result['valid'] is True
        assert result['checks']['row_count_valid'] is True
        assert result['checks']['columns_valid'] is True
