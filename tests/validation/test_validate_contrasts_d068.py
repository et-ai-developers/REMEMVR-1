"""
Tests for validate_contrasts_d068 function (Tool 9/25).

RQ 5.9: Validate that contrast results include Decision D068 dual p-value reporting.
"""

import pytest
import pandas as pd
import numpy as np
from tools.validation import validate_contrasts_d068


def test_basic_structure():
    """Test that output has required keys."""
    df = pd.DataFrame({
        'comparison': ['A vs B', 'A vs C'],
        'estimate': [0.5, 0.3],
        'p_uncorrected': [0.01, 0.05],
        'p_bonferroni': [0.03, 0.15]
    })

    result = validate_contrasts_d068(df)

    assert isinstance(result, dict)
    assert 'valid' in result
    assert 'd068_compliant' in result
    assert 'message' in result
    assert 'missing_cols' in result


def test_valid_d068_compliant_dataframe():
    """Test DataFrame with both required p-value columns."""
    df = pd.DataFrame({
        'comparison': ['A vs B', 'A vs C', 'B vs C'],
        'estimate': [0.5, 0.3, -0.2],
        'p_uncorrected': [0.01, 0.05, 0.20],
        'p_bonferroni': [0.03, 0.15, 0.60]
    })

    result = validate_contrasts_d068(df)

    assert result['valid'] is True
    assert result['d068_compliant'] is True
    assert len(result['missing_cols']) == 0
    assert 'both p_uncorrected and p_bonferroni' in result['message'].lower()


def test_missing_p_uncorrected():
    """Test DataFrame missing p_uncorrected column."""
    df = pd.DataFrame({
        'comparison': ['A vs B'],
        'estimate': [0.5],
        'p_bonferroni': [0.03]
    })

    result = validate_contrasts_d068(df)

    assert result['valid'] is False
    assert result['d068_compliant'] is False
    assert 'p_uncorrected' in result['missing_cols']
    assert 'p_uncorrected' in result['message']


def test_missing_p_bonferroni():
    """Test DataFrame missing p_bonferroni column."""
    df = pd.DataFrame({
        'comparison': ['A vs B'],
        'estimate': [0.5],
        'p_uncorrected': [0.01]
    })

    result = validate_contrasts_d068(df)

    assert result['valid'] is False
    assert result['d068_compliant'] is False
    assert 'p_bonferroni' in result['missing_cols']
    assert 'p_bonferroni' in result['message']


def test_missing_both_columns():
    """Test DataFrame missing both required columns."""
    df = pd.DataFrame({
        'comparison': ['A vs B'],
        'estimate': [0.5],
        'se': [0.1]
    })

    result = validate_contrasts_d068(df)

    assert result['valid'] is False
    assert result['d068_compliant'] is False
    assert 'p_uncorrected' in result['missing_cols']
    assert 'p_bonferroni' in result['missing_cols']
    assert len(result['missing_cols']) == 2


def test_alternative_corrected_column_name():
    """Test that p_tukey is accepted as alternative to p_bonferroni."""
    df = pd.DataFrame({
        'comparison': ['A vs B', 'A vs C'],
        'estimate': [0.5, 0.3],
        'p_uncorrected': [0.01, 0.05],
        'p_tukey': [0.03, 0.15]  # Tukey HSD correction
    })

    result = validate_contrasts_d068(df)

    assert result['valid'] is True
    assert result['d068_compliant'] is True
    assert len(result['missing_cols']) == 0


def test_alternative_holm_column_name():
    """Test that p_holm is accepted as alternative correction."""
    df = pd.DataFrame({
        'comparison': ['A vs B'],
        'estimate': [0.5],
        'p_uncorrected': [0.01],
        'p_holm': [0.02]  # Holm-Bonferroni correction
    })

    result = validate_contrasts_d068(df)

    assert result['valid'] is True
    assert result['d068_compliant'] is True


def test_empty_dataframe():
    """Test validation on empty DataFrame."""
    df = pd.DataFrame()

    result = validate_contrasts_d068(df)

    assert result['valid'] is False
    assert result['d068_compliant'] is False
    assert 'p_uncorrected' in result['missing_cols']
    assert 'p_bonferroni' in result['missing_cols']


def test_dataframe_with_extra_columns():
    """Test that extra columns don't interfere with validation."""
    df = pd.DataFrame({
        'comparison': ['A vs B'],
        'estimate': [0.5],
        'se': [0.1],
        'z_statistic': [5.0],
        'p_uncorrected': [0.01],
        'p_bonferroni': [0.03],
        'ci_lower': [0.3],
        'ci_upper': [0.7],
        'cohens_d': [0.8]
    })

    result = validate_contrasts_d068(df)

    assert result['valid'] is True
    assert result['d068_compliant'] is True


def test_column_case_sensitivity():
    """Test that column names are case-sensitive."""
    df = pd.DataFrame({
        'comparison': ['A vs B'],
        'P_Uncorrected': [0.01],  # Wrong case
        'P_Bonferroni': [0.03]    # Wrong case
    })

    result = validate_contrasts_d068(df)

    assert result['valid'] is False
    assert result['d068_compliant'] is False
    assert 'p_uncorrected' in result['missing_cols']
    assert 'p_bonferroni' in result['missing_cols']


def test_realistic_rq59_scenario():
    """Test realistic scenario from RQ 5.9: Domain contrasts with Bonferroni correction."""
    # 3 domains = 3 pairwise comparisons
    df = pd.DataFrame({
        'comparison': [
            'What vs Where',
            'What vs When',
            'Where vs When'
        ],
        'estimate': [0.25, 0.45, 0.20],
        'se': [0.08, 0.09, 0.07],
        'z_statistic': [3.13, 5.00, 2.86],
        'p_uncorrected': [0.0018, 0.0001, 0.0043],
        'p_bonferroni': [0.0054, 0.0003, 0.0129]
    })

    result = validate_contrasts_d068(df)

    assert result['valid'] is True
    assert result['d068_compliant'] is True
    assert len(result['missing_cols']) == 0
    assert 'Decision D068' in result['message'] or 'd068' in result['message'].lower()
