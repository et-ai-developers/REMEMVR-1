"""
Test prepare_irt_input_from_long function.

Tests the conversion of long-format data to IRT tensors.
"""
import pytest
import pandas as pd
import numpy as np

# Skip entire module if torch not available
torch = pytest.importorskip("torch", reason="Requires torch (PyTorch)")

from tools.analysis_irt import prepare_irt_input_from_long


class TestPrepareIrtInputFromLong:
    """Tests for prepare_irt_input_from_long function."""

    @pytest.fixture
    def sample_long_data(self):
        """Create sample long-format IRT data."""
        # 3 participants, 4 items, 2 factors
        data = []
        for uid in ['P001', 'P002', 'P003']:
            for test in ['T1', 'T2', 'T3', 'T4']:
                composite_id = f"{uid}_{test}"
                for item in ['item_A1', 'item_A2', 'item_B1', 'item_B2']:
                    factor = 'FactorA' if item.startswith('item_A') else 'FactorB'
                    response = np.random.randint(0, 3)  # 0, 1, or 2 (3 categories)
                    data.append({
                        'composite_ID': composite_id,
                        'item': item,
                        'response': response,
                        'factor': factor
                    })
        return pd.DataFrame(data)

    @pytest.fixture
    def sample_groups(self):
        """Create sample groups configuration."""
        return {
            'FactorA': ['item_A1', 'item_A2'],
            'FactorB': ['item_B1', 'item_B2']
        }

    def test_returns_tuple_of_five(self, sample_long_data, sample_groups):
        """Test function returns tuple of 5 elements."""
        result = prepare_irt_input_from_long(sample_long_data, sample_groups)
        assert isinstance(result, tuple)
        assert len(result) == 5

    def test_returns_correct_types(self, sample_long_data, sample_groups):
        """Test each element has correct type."""
        response_matrix, missing_mask, q_matrix, composite_ids, item_list = \
            prepare_irt_input_from_long(sample_long_data, sample_groups)

        assert isinstance(response_matrix, torch.Tensor)
        assert isinstance(missing_mask, torch.Tensor)
        assert isinstance(q_matrix, torch.Tensor)
        assert isinstance(composite_ids, list)
        assert isinstance(item_list, list)

    def test_response_matrix_shape(self, sample_long_data, sample_groups):
        """Test response matrix has correct shape (n_responses x n_items)."""
        response_matrix, _, _, composite_ids, item_list = \
            prepare_irt_input_from_long(sample_long_data, sample_groups)

        n_responses = len(composite_ids)
        n_items = len(item_list)

        assert response_matrix.shape == (n_responses, n_items)

    def test_q_matrix_shape(self, sample_long_data, sample_groups):
        """Test Q-matrix has correct shape (n_items x n_factors)."""
        _, _, q_matrix, _, item_list = \
            prepare_irt_input_from_long(sample_long_data, sample_groups)

        n_items = len(item_list)
        n_factors = len(sample_groups)

        assert q_matrix.shape == (n_items, n_factors)

    def test_q_matrix_binary(self, sample_long_data, sample_groups):
        """Test Q-matrix contains only 0s and 1s."""
        _, _, q_matrix, _, _ = prepare_irt_input_from_long(sample_long_data, sample_groups)

        unique_values = torch.unique(q_matrix)
        assert all(v in [0, 1] for v in unique_values.tolist())

    def test_q_matrix_one_factor_per_item(self, sample_long_data, sample_groups):
        """Test each item loads on exactly one factor (confirmatory model)."""
        _, _, q_matrix, _, _ = prepare_irt_input_from_long(sample_long_data, sample_groups)

        # Each row should sum to 1
        row_sums = q_matrix.sum(dim=1)
        assert all(s == 1 for s in row_sums.tolist())

    def test_missing_mask_shape_matches_response(self, sample_long_data, sample_groups):
        """Test missing mask has same shape as response matrix."""
        response_matrix, missing_mask, _, _, _ = \
            prepare_irt_input_from_long(sample_long_data, sample_groups)

        assert missing_mask.shape == response_matrix.shape

    def test_empty_dataframe_raises(self, sample_groups):
        """Test empty DataFrame raises ValueError."""
        empty_df = pd.DataFrame()

        with pytest.raises(ValueError, match="empty"):
            prepare_irt_input_from_long(empty_df, sample_groups)

    def test_missing_columns_raises(self, sample_groups):
        """Test missing required columns raises ValueError."""
        bad_df = pd.DataFrame({'wrong_col': [1, 2, 3]})

        with pytest.raises(ValueError):
            prepare_irt_input_from_long(bad_df, sample_groups)

    def test_composite_ids_unique(self, sample_long_data, sample_groups):
        """Test composite IDs are unique."""
        _, _, _, composite_ids, _ = prepare_irt_input_from_long(sample_long_data, sample_groups)

        assert len(composite_ids) == len(set(composite_ids))

    def test_item_list_matches_groups(self, sample_long_data, sample_groups):
        """Test item list contains all items from groups."""
        _, _, _, _, item_list = prepare_irt_input_from_long(sample_long_data, sample_groups)

        all_items = set()
        for items in sample_groups.values():
            all_items.update(items)

        assert set(item_list) == all_items


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
