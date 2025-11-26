"""
Tests for validate_contrasts_dual_pvalues function.

Test Coverage:
- Basic structure (4 required keys)
- Valid D068 compliant DataFrame with required comparisons
- Missing required comparison
- Missing p_uncorrected column
- Missing p_tukey column
- Alternative correction names (p_bonferroni, p_holm accepted)
- Empty required_comparisons list (still checks D068)
- Empty DataFrame handling
- Extra columns don't interfere
- Partial comparison matching (only some required comparisons present)
- Realistic RQ 5.10 scenario (3 domain pairwise comparisons post-hoc)
"""

import pandas as pd
import pytest
from tools.validation import validate_contrasts_dual_pvalues


def test_validate_contrasts_dual_pvalues_basic_structure():
    """Test output has required keys."""
    df = pd.DataFrame({
        'comparison': ['A-B', 'A-C'],
        'p_uncorrected': [0.01, 0.05],
        'p_tukey': [0.03, 0.15]
    })
    result = validate_contrasts_dual_pvalues(df, required_comparisons=['A-B'])

    assert 'valid' in result
    assert 'd068_compliant' in result
    assert 'missing_comparisons' in result
    assert 'message' in result


def test_validate_contrasts_dual_pvalues_valid_compliant():
    """Test valid D068 compliant contrasts with required comparisons."""
    df = pd.DataFrame({
        'comparison': ['Where-What', 'When-What', 'Where-When'],
        'estimate': [0.5, -0.3, 0.8],
        'p_uncorrected': [0.01, 0.05, 0.001],
        'p_tukey': [0.03, 0.15, 0.003]
    })
    result = validate_contrasts_dual_pvalues(
        df,
        required_comparisons=['Where-What', 'When-What', 'Where-When']
    )

    assert result['valid'] is True
    assert result['d068_compliant'] is True
    assert len(result['missing_comparisons']) == 0
    assert 'ALL required comparisons present' in result['message']


def test_validate_contrasts_dual_pvalues_missing_comparison():
    """Test missing required comparison."""
    df = pd.DataFrame({
        'comparison': ['Where-What', 'When-What'],  # Missing Where-When
        'p_uncorrected': [0.01, 0.05],
        'p_tukey': [0.03, 0.15]
    })
    result = validate_contrasts_dual_pvalues(
        df,
        required_comparisons=['Where-What', 'When-What', 'Where-When']
    )

    assert result['valid'] is False
    assert 'Where-When' in result['missing_comparisons']
    assert 'Missing required comparisons' in result['message']


def test_validate_contrasts_dual_pvalues_missing_p_uncorrected():
    """Test missing p_uncorrected column."""
    df = pd.DataFrame({
        'comparison': ['A-B', 'A-C'],
        'p_tukey': [0.03, 0.15]
    })
    result = validate_contrasts_dual_pvalues(df, required_comparisons=['A-B'])

    assert result['valid'] is False
    assert result['d068_compliant'] is False
    assert 'p_uncorrected' in result['message']


def test_validate_contrasts_dual_pvalues_missing_p_tukey():
    """Test missing correction column."""
    df = pd.DataFrame({
        'comparison': ['A-B', 'A-C'],
        'p_uncorrected': [0.01, 0.05]
    })
    result = validate_contrasts_dual_pvalues(df, required_comparisons=['A-B'])

    assert result['valid'] is False
    assert result['d068_compliant'] is False
    assert 'p_tukey' in result['message']


def test_validate_contrasts_dual_pvalues_alternative_correction():
    """Test alternative correction names accepted (p_bonferroni, p_holm)."""
    # Test with p_bonferroni
    df_bonf = pd.DataFrame({
        'comparison': ['A-B'],
        'p_uncorrected': [0.01],
        'p_bonferroni': [0.03]
    })
    result_bonf = validate_contrasts_dual_pvalues(df_bonf, required_comparisons=['A-B'])
    assert result_bonf['valid'] is True
    assert result_bonf['d068_compliant'] is True

    # Test with p_holm
    df_holm = pd.DataFrame({
        'comparison': ['A-B'],
        'p_uncorrected': [0.01],
        'p_holm': [0.02]
    })
    result_holm = validate_contrasts_dual_pvalues(df_holm, required_comparisons=['A-B'])
    assert result_holm['valid'] is True
    assert result_holm['d068_compliant'] is True


def test_validate_contrasts_dual_pvalues_empty_required():
    """Test empty required_comparisons list (still checks D068)."""
    df = pd.DataFrame({
        'comparison': ['A-B', 'A-C'],
        'p_uncorrected': [0.01, 0.05],
        'p_tukey': [0.03, 0.15]
    })
    result = validate_contrasts_dual_pvalues(df, required_comparisons=[])

    assert result['valid'] is True
    assert result['d068_compliant'] is True
    assert len(result['missing_comparisons']) == 0


def test_validate_contrasts_dual_pvalues_empty_dataframe():
    """Test empty DataFrame handling."""
    df = pd.DataFrame(columns=['comparison', 'p_uncorrected', 'p_tukey'])
    result = validate_contrasts_dual_pvalues(df, required_comparisons=['A-B'])

    assert result['valid'] is False
    assert 'Empty DataFrame' in result['message']


def test_validate_contrasts_dual_pvalues_extra_columns():
    """Test extra columns don't interfere with validation."""
    df = pd.DataFrame({
        'comparison': ['A-B'],
        'estimate': [0.5],
        'se': [0.1],
        'z': [5.0],
        'p_uncorrected': [0.001],
        'p_tukey': [0.003],
        'significant': [True],
        'interpretation': ['Large effect']
    })
    result = validate_contrasts_dual_pvalues(df, required_comparisons=['A-B'])

    assert result['valid'] is True
    assert result['d068_compliant'] is True


def test_validate_contrasts_dual_pvalues_partial_match():
    """Test partial comparison matching."""
    df = pd.DataFrame({
        'comparison': ['Where-What', 'When-What'],  # Only 2 of 3
        'p_uncorrected': [0.01, 0.05],
        'p_tukey': [0.03, 0.15]
    })
    result = validate_contrasts_dual_pvalues(
        df,
        required_comparisons=['Where-What', 'When-What', 'Where-When']
    )

    assert result['valid'] is False
    assert len(result['missing_comparisons']) == 1
    assert 'Where-When' in result['missing_comparisons']
    assert 'Where-What' not in result['missing_comparisons']
    assert 'When-What' not in result['missing_comparisons']


def test_validate_contrasts_dual_pvalues_realistic_rq510():
    """Test realistic RQ 5.10 scenario (3 domain pairwise post-hoc)."""
    df = pd.DataFrame({
        'comparison': [
            'Where-What',
            'Where-When',
            'What-When'
        ],
        'estimate': [0.45, 0.82, 0.37],
        'se': [0.12, 0.13, 0.11],
        'z': [3.75, 6.31, 3.36],
        'p_uncorrected': [0.0002, 0.0001, 0.0008],
        'p_tukey': [0.0006, 0.0003, 0.0024],
        'significant_uncorrected': [True, True, True],
        'significant_tukey': [True, True, True]
    })
    result = validate_contrasts_dual_pvalues(
        df,
        required_comparisons=['Where-What', 'Where-When', 'What-When']
    )

    assert result['valid'] is True
    assert result['d068_compliant'] is True
    assert len(result['missing_comparisons']) == 0
    assert 'ALL required comparisons present' in result['message']
    assert 'Decision D068 compliant' in result['message']
