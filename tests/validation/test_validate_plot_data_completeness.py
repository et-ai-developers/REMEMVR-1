"""
Test suite for validate_plot_data_completeness function.

Tests plot data completeness validation (all domains/groups present).
"""

import pytest
import pandas as pd
from tools.validation import validate_plot_data_completeness


class TestValidatePlotDataCompleteness:
    """Test validate_plot_data_completeness function."""

    def test_basic_structure(self):
        """Test function returns expected keys."""
        df = pd.DataFrame({
            'domain': ['Where', 'What'],
            'group': ['Young', 'Young']
        })
        result = validate_plot_data_completeness(df, ['Where', 'What'], ['Young'])

        assert 'valid' in result
        assert 'message' in result
        assert 'missing_domains' in result
        assert 'missing_groups' in result

    def test_valid_all_present(self):
        """Test DataFrame with all required domains and groups."""
        df = pd.DataFrame({
            'domain': ['Where', 'What', 'When', 'Where', 'What', 'When'],
            'group': ['Young', 'Young', 'Young', 'Old', 'Old', 'Old']
        })
        result = validate_plot_data_completeness(
            df,
            required_domains=['Where', 'What', 'When'],
            required_groups=['Young', 'Old']
        )

        assert result['valid'] is True
        assert len(result['missing_domains']) == 0
        assert len(result['missing_groups']) == 0

    def test_invalid_missing_domain(self):
        """Test DataFrame missing a required domain."""
        df = pd.DataFrame({
            'domain': ['Where', 'What'],
            'group': ['Young', 'Young']
        })
        result = validate_plot_data_completeness(
            df,
            required_domains=['Where', 'What', 'When'],
            required_groups=['Young']
        )

        assert result['valid'] is False
        assert 'When' in result['missing_domains']

    def test_invalid_missing_group(self):
        """Test DataFrame missing a required group."""
        df = pd.DataFrame({
            'domain': ['Where', 'Where'],
            'group': ['Young', 'Middle']
        })
        result = validate_plot_data_completeness(
            df,
            required_domains=['Where'],
            required_groups=['Young', 'Middle', 'Older']
        )

        assert result['valid'] is False
        assert 'Older' in result['missing_groups']

    def test_valid_extra_values_allowed(self):
        """Test DataFrame with extra domains/groups (should be valid)."""
        df = pd.DataFrame({
            'domain': ['Where', 'What', 'Extra'],
            'group': ['Young', 'Young', 'Young']
        })
        result = validate_plot_data_completeness(
            df,
            required_domains=['Where', 'What'],
            required_groups=['Young']
        )

        assert result['valid'] is True

    def test_realistic_rq_5_10_scenario(self):
        """Test realistic RQ 5.10 age tertiles plot data."""
        # 3 domains × 3 tertiles × 4 timepoints = 36 rows
        domains = ['Where', 'What', 'When'] * 12
        tertiles = (['Young'] * 3 + ['Middle'] * 3 + ['Older'] * 3) * 4

        df = pd.DataFrame({
            'domain': domains,
            'age_tertile': tertiles,
            'theta_mean': [0.5] * 36
        })

        result = validate_plot_data_completeness(
            df,
            required_domains=['Where', 'What', 'When'],
            required_groups=['Young', 'Middle', 'Older'],
            domain_col='domain',
            group_col='age_tertile'
        )

        assert result['valid'] is True
        assert '3 domains' in result['message']
        assert '3 groups' in result['message']
