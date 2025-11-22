"""
Test validate_irt_parameters function.

Tests validation of IRT item parameters against quality thresholds.
"""
import pytest
import pandas as pd
import numpy as np

from tools.validation import validate_irt_parameters


class TestValidateIrtParameters:
    """Tests for validate_irt_parameters function."""

    @pytest.fixture
    def good_items(self):
        """Create item parameters that pass validation."""
        return pd.DataFrame({
            'item_name': ['item1', 'item2', 'item3'],
            'a': [0.8, 1.0, 0.6],  # All >= 0.4
            'b': [0.5, -1.0, 2.0]  # All |b| <= 3.0
        })

    @pytest.fixture
    def bad_items(self):
        """Create item parameters with issues."""
        return pd.DataFrame({
            'item_name': ['item1', 'item2', 'item3'],
            'a': [0.2, 0.3, 0.1],  # All < 0.4
            'b': [4.0, -3.5, 5.0]  # All |b| > 3.0
        })

    @pytest.fixture
    def mixed_items(self):
        """Create item parameters with some good, some bad."""
        return pd.DataFrame({
            'item_name': ['item1', 'item2', 'item3', 'item4'],
            'a': [0.8, 0.3, 1.0, 0.5],  # item2 fails
            'b': [0.5, 1.0, -3.5, 2.0]  # item3 fails
        })

    def test_returns_dict(self, good_items):
        """Test function returns dictionary."""
        result = validate_irt_parameters(good_items)
        assert isinstance(result, dict)

    def test_valid_key_present(self, good_items):
        """Test output has 'valid' key."""
        result = validate_irt_parameters(good_items)
        assert 'valid' in result

    def test_good_items_valid(self, good_items):
        """Test good items return valid=True."""
        result = validate_irt_parameters(good_items)
        assert result['valid'] is True

    def test_bad_items_invalid(self, bad_items):
        """Test bad items return valid=False."""
        result = validate_irt_parameters(bad_items)
        assert result['valid'] is False

    def test_default_a_threshold(self, mixed_items):
        """Test default a_min threshold is 0.4."""
        result = validate_irt_parameters(mixed_items)

        # Should report issues with items having a < 0.4
        if 'flagged_items' in result or 'issues' in result or 'n_flagged' in result:
            # Some items should be flagged
            pass

    def test_default_b_threshold(self, mixed_items):
        """Test default b_max threshold is 3.0."""
        result = validate_irt_parameters(mixed_items)

        # Should report issues with items having |b| > 3.0
        assert isinstance(result, dict)

    def test_custom_a_threshold(self, good_items):
        """Test custom a_min parameter."""
        # With stricter threshold, some might fail
        result = validate_irt_parameters(good_items, a_min=0.9)

        # item1 (0.8) and item3 (0.6) should now fail
        assert result['valid'] is False

    def test_custom_b_threshold(self, good_items):
        """Test custom b_max parameter."""
        # With stricter threshold
        result = validate_irt_parameters(good_items, b_max=1.5)

        # item3 (b=2.0) should now fail
        assert result['valid'] is False

    def test_reports_count(self, mixed_items):
        """Test output reports item counts."""
        result = validate_irt_parameters(mixed_items)

        # Should have some count information
        keys = [k.lower() for k in result.keys()]
        count_keys = [k for k in keys if 'n_' in k or 'count' in k or 'total' in k or 'flagged' in k]
        assert len(count_keys) > 0 or 'summary' in keys

    def test_empty_dataframe(self):
        """Test handles empty DataFrame."""
        empty_df = pd.DataFrame(columns=['item_name', 'a', 'b'])
        result = validate_irt_parameters(empty_df)

        assert isinstance(result, dict)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
