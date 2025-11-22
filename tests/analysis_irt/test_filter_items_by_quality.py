"""
Test filter_items_by_quality function (D039 implementation).

Tests the 2-pass IRT item purification with thresholds:
- a >= 0.4 (discrimination)
- |b| <= 3.0 (difficulty)
"""
import pytest
import pandas as pd
import numpy as np

# Skip entire module if torch not available (analysis_irt requires torch)
pytest.importorskip("torch", reason="Requires torch (PyTorch)")

from tools.analysis_irt import filter_items_by_quality


class TestFilterItemsByQuality:
    """Tests for filter_items_by_quality function (D039)."""

    @pytest.fixture
    def sample_item_params(self):
        """Create sample item parameters DataFrame."""
        return pd.DataFrame({
            'item_name': ['item1', 'item2', 'item3', 'item4', 'item5', 'item6'],
            'a': [0.8, 0.3, 1.2, 0.5, 0.2, 0.9],  # items 2, 5 below threshold
            'b': [0.5, 1.0, -2.5, 3.5, 0.0, -3.2],  # items 4, 6 above threshold
            'factor': ['F1', 'F1', 'F2', 'F2', 'F1', 'F2']
        })

    def test_returns_tuple_of_two_dataframes(self, sample_item_params):
        """Test function returns tuple of two DataFrames."""
        retained, excluded = filter_items_by_quality(sample_item_params)

        assert isinstance(retained, pd.DataFrame)
        assert isinstance(excluded, pd.DataFrame)

    def test_default_a_threshold(self, sample_item_params):
        """Test default a threshold is 0.4 (D039)."""
        retained, excluded = filter_items_by_quality(sample_item_params)

        # All retained items should have a >= 0.4
        assert all(retained['a'] >= 0.4)

    def test_default_b_threshold(self, sample_item_params):
        """Test default b threshold is 3.0 (D039)."""
        retained, excluded = filter_items_by_quality(sample_item_params)

        # All retained items should have |b| <= 3.0
        assert all(abs(retained['b']) <= 3.0)

    def test_correct_items_retained(self, sample_item_params):
        """Test correct items are retained."""
        retained, excluded = filter_items_by_quality(sample_item_params)

        # item1: a=0.8>=0.4, |b|=0.5<=3.0 -> RETAIN
        # item2: a=0.3<0.4 -> EXCLUDE
        # item3: a=1.2>=0.4, |b|=2.5<=3.0 -> RETAIN
        # item4: a=0.5>=0.4, |b|=3.5>3.0 -> EXCLUDE
        # item5: a=0.2<0.4 -> EXCLUDE
        # item6: a=0.9>=0.4, |b|=3.2>3.0 -> EXCLUDE

        retained_names = set(retained['item_name'].tolist())
        assert retained_names == {'item1', 'item3'}

    def test_correct_items_excluded(self, sample_item_params):
        """Test correct items are excluded."""
        retained, excluded = filter_items_by_quality(sample_item_params)

        excluded_names = set(excluded['item_name'].tolist())
        assert excluded_names == {'item2', 'item4', 'item5', 'item6'}

    def test_custom_a_threshold(self, sample_item_params):
        """Test custom a threshold works."""
        retained, excluded = filter_items_by_quality(
            sample_item_params,
            a_threshold=0.5
        )

        # With a_threshold=0.5, items with a < 0.5 are excluded
        assert all(retained['a'] >= 0.5)

    def test_custom_b_threshold(self, sample_item_params):
        """Test custom b threshold works."""
        retained, excluded = filter_items_by_quality(
            sample_item_params,
            b_threshold=2.0
        )

        # With b_threshold=2.0, items with |b| > 2.0 are excluded
        assert all(abs(retained['b']) <= 2.0)

    def test_total_count_preserved(self, sample_item_params):
        """Test total item count is preserved."""
        retained, excluded = filter_items_by_quality(sample_item_params)

        total = len(retained) + len(excluded)
        assert total == len(sample_item_params)

    def test_no_overlap(self, sample_item_params):
        """Test no items appear in both retained and excluded."""
        retained, excluded = filter_items_by_quality(sample_item_params)

        retained_names = set(retained['item_name'].tolist())
        excluded_names = set(excluded['item_name'].tolist())

        assert len(retained_names & excluded_names) == 0

    def test_all_pass_scenario(self):
        """Test all items pass when all meet thresholds."""
        good_items = pd.DataFrame({
            'item_name': ['item1', 'item2'],
            'a': [0.8, 1.0],
            'b': [0.5, -0.5]
        })

        retained, excluded = filter_items_by_quality(good_items)

        assert len(retained) == 2
        assert len(excluded) == 0

    def test_all_fail_scenario(self):
        """Test all items fail when none meet thresholds."""
        bad_items = pd.DataFrame({
            'item_name': ['item1', 'item2'],
            'a': [0.1, 0.2],  # All below 0.4
            'b': [0.5, -0.5]
        })

        retained, excluded = filter_items_by_quality(bad_items)

        assert len(retained) == 0
        assert len(excluded) == 2

    def test_handles_multivariate_format(self):
        """Test function handles multivariate (multiple difficulty columns) format."""
        # Multivariate format has 'Difficulty' column and multiple b columns
        multivariate_items = pd.DataFrame({
            'item_name': ['item1', 'item2', 'item3'],
            'a': [0.8, 0.3, 1.0],
            'Difficulty': [0.5, 1.0, -2.5],  # Primary difficulty
            'b_1': [0.5, 1.0, -2.5],
            'b_2': [0.6, 1.1, -2.4],
            'b_3': [0.7, 1.2, -2.3]
        })

        # Should auto-detect multivariate and use Difficulty column
        retained, excluded = filter_items_by_quality(multivariate_items)

        assert isinstance(retained, pd.DataFrame)
        assert isinstance(excluded, pd.DataFrame)

    def test_empty_dataframe(self):
        """Test empty DataFrame returns empty results."""
        empty_df = pd.DataFrame(columns=['item_name', 'a', 'b'])

        retained, excluded = filter_items_by_quality(empty_df)

        assert len(retained) == 0
        assert len(excluded) == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
