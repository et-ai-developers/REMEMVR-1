"""
Tests for validate_effect_sizes validator.

Purpose: Validate Cohen's f² effect sizes are within reasonable bounds
Used by: RQ 5.9 effect size validation
"""

import numpy as np
import pandas as pd
import pytest
from tools.validation import validate_effect_sizes


class TestValidateEffectSizes:
    """Tests for validate_effect_sizes validator."""

    def test_basic_structure(self):
        """Test basic output structure."""
        df = pd.DataFrame({'cohens_f2': [0.02, 0.15, 0.35]})
        result = validate_effect_sizes(df)

        assert 'valid' in result
        assert 'message' in result
        assert 'warnings' in result
        assert isinstance(result['valid'], bool)
        assert isinstance(result['message'], str)
        assert isinstance(result['warnings'], list)

    def test_valid_effect_sizes_small_to_large(self):
        """Test valid effect sizes (small, medium, large per Cohen 1988)."""
        df = pd.DataFrame({'cohens_f2': [0.02, 0.15, 0.35]})  # small, medium, large
        result = validate_effect_sizes(df)

        assert result['valid'] is True
        assert len(result['warnings']) == 0
        assert 'All effect sizes valid' in result['message']

    def test_negative_effect_size_invalid(self):
        """Test negative effect sizes are invalid."""
        df = pd.DataFrame({'cohens_f2': [0.1, -0.05, 0.2]})
        result = validate_effect_sizes(df)

        assert result['valid'] is False
        assert 'negative' in result['message'].lower()

    def test_very_large_effect_size_warning(self):
        """Test very large f² (>1.0) triggers warning but not invalid."""
        df = pd.DataFrame({'cohens_f2': [0.1, 1.5, 0.3]})
        result = validate_effect_sizes(df)

        # Still valid, but with warnings
        assert result['valid'] is True
        assert len(result['warnings']) > 0
        assert any('very large' in w.lower() or '>1.0' in w for w in result['warnings'])

    def test_nan_values_invalid(self):
        """Test NaN values are invalid."""
        df = pd.DataFrame({'cohens_f2': [0.1, np.nan, 0.3]})
        result = validate_effect_sizes(df)

        assert result['valid'] is False
        assert 'nan' in result['message'].lower()

    def test_infinite_values_invalid(self):
        """Test infinite values are invalid."""
        df = pd.DataFrame({'cohens_f2': [0.1, np.inf, 0.3]})
        result = validate_effect_sizes(df)

        assert result['valid'] is False
        assert 'inf' in result['message'].lower()

    def test_zero_effect_size_valid(self):
        """Test f²=0 is valid (no effect)."""
        df = pd.DataFrame({'cohens_f2': [0.0, 0.1, 0.2]})
        result = validate_effect_sizes(df)

        assert result['valid'] is True
        assert len(result['warnings']) == 0

    def test_custom_column_name(self):
        """Test custom f² column name."""
        df = pd.DataFrame({'effect_size_f2': [0.02, 0.15]})
        result = validate_effect_sizes(df, f2_column='effect_size_f2')

        assert result['valid'] is True

    def test_missing_default_column_error(self):
        """Test error when default column missing."""
        df = pd.DataFrame({'other_col': [1, 2]})

        with pytest.raises(KeyError):
            validate_effect_sizes(df)

    def test_empty_dataframe(self):
        """Test empty DataFrame handling."""
        df = pd.DataFrame({'cohens_f2': []})
        result = validate_effect_sizes(df)

        assert result['valid'] is True  # Empty is valid (no violations)
        assert len(result['warnings']) == 0

    def test_exactly_one_at_threshold(self):
        """Test f²=1.0 exactly (boundary)."""
        df = pd.DataFrame({'cohens_f2': [1.0]})
        result = validate_effect_sizes(df)

        # f²=1.0 is large but not "very large" (threshold is >1.0)
        assert result['valid'] is True
        assert len(result['warnings']) == 0

    def test_multiple_large_values_multiple_warnings(self):
        """Test multiple very large values generate warnings."""
        df = pd.DataFrame({'cohens_f2': [0.1, 1.5, 2.0, 0.3, 3.5]})
        result = validate_effect_sizes(df)

        assert result['valid'] is True
        assert len(result['warnings']) > 0
        # Warning should mention how many values exceed threshold
        assert any('3' in w for w in result['warnings'])  # 3 values >1.0

    def test_realistic_lmm_effect_sizes(self):
        """Test realistic LMM effect sizes (RQ 5.9 scenario)."""
        df = pd.DataFrame({
            'predictor': ['Age_c', 'Domain[T.What]', 'Domain[T.When]', 'TSVR_hours'],
            'cohens_f2': [0.01, 0.05, 0.08, 0.15]  # Mostly small to medium
        })
        result = validate_effect_sizes(df)

        assert result['valid'] is True
        assert len(result['warnings']) == 0
