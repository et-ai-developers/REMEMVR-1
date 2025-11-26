"""
Tests for validate_hypothesis_test_dual_pvalues function (Tool 10/25).

RQ 5.10: Validate that hypothesis tests (e.g., 3-way interactions) include D068 dual p-value reporting.
"""

import pytest
import pandas as pd
import numpy as np
from tools.validation import validate_hypothesis_test_dual_pvalues


def test_basic_structure():
    """Test that output has required keys."""
    df = pd.DataFrame({
        'term': ['Age:Domain:Time'],
        'estimate': [0.15],
        'p_uncorrected': [0.001],
        'p_bonferroni': [0.015]
    })

    result = validate_hypothesis_test_dual_pvalues(
        df,
        required_terms=['Age:Domain:Time'],
        alpha_bonferroni=0.05
    )

    assert isinstance(result, dict)
    assert 'valid' in result
    assert 'missing_terms' in result
    assert 'd068_compliant' in result
    assert 'message' in result


def test_valid_single_interaction():
    """Test valid DataFrame with single required interaction term."""
    df = pd.DataFrame({
        'term': ['Intercept', 'Age', 'Domain', 'Time', 'Age:Domain:Time'],
        'estimate': [1.0, 0.1, 0.2, -0.3, 0.15],
        'se': [0.05, 0.02, 0.03, 0.04, 0.05],
        'p_uncorrected': [0.000, 0.001, 0.005, 0.000, 0.003],
        'p_bonferroni': [0.000, 0.015, 0.075, 0.000, 0.045]
    })

    result = validate_hypothesis_test_dual_pvalues(
        df,
        required_terms=['Age:Domain:Time']
    )

    assert result['valid'] is True
    assert result['d068_compliant'] is True
    assert len(result['missing_terms']) == 0


def test_valid_multiple_interactions():
    """Test valid DataFrame with multiple required terms."""
    df = pd.DataFrame({
        'term': ['Age:Domain', 'Domain:Time', 'Age:Time'],
        'p_uncorrected': [0.01, 0.05, 0.20],
        'p_bonferroni': [0.03, 0.15, 0.60]
    })

    result = validate_hypothesis_test_dual_pvalues(
        df,
        required_terms=['Age:Domain', 'Domain:Time', 'Age:Time']
    )

    assert result['valid'] is True
    assert len(result['missing_terms']) == 0


def test_missing_required_term():
    """Test when required interaction term is missing."""
    df = pd.DataFrame({
        'term': ['Age', 'Domain', 'Time'],
        'p_uncorrected': [0.01, 0.05, 0.20],
        'p_bonferroni': [0.03, 0.15, 0.60]
    })

    result = validate_hypothesis_test_dual_pvalues(
        df,
        required_terms=['Age:Domain:Time']
    )

    assert result['valid'] is False
    assert 'Age:Domain:Time' in result['missing_terms']


def test_missing_p_uncorrected_column():
    """Test when p_uncorrected column is missing."""
    df = pd.DataFrame({
        'term': ['Age:Domain:Time'],
        'estimate': [0.15],
        'p_bonferroni': [0.045]
    })

    result = validate_hypothesis_test_dual_pvalues(
        df,
        required_terms=['Age:Domain:Time']
    )

    assert result['valid'] is False
    assert result['d068_compliant'] is False


def test_missing_p_bonferroni_column():
    """Test when p_bonferroni column is missing."""
    df = pd.DataFrame({
        'term': ['Age:Domain:Time'],
        'estimate': [0.15],
        'p_uncorrected': [0.003]
    })

    result = validate_hypothesis_test_dual_pvalues(
        df,
        required_terms=['Age:Domain:Time']
    )

    assert result['valid'] is False
    assert result['d068_compliant'] is False


def test_alternative_correction_names():
    """Test that alternative correction column names are accepted."""
    # Test with p_holm
    df1 = pd.DataFrame({
        'term': ['Age:Domain:Time'],
        'p_uncorrected': [0.003],
        'p_holm': [0.012]
    })

    result1 = validate_hypothesis_test_dual_pvalues(
        df1,
        required_terms=['Age:Domain:Time']
    )

    assert result1['valid'] is True
    assert result1['d068_compliant'] is True

    # Test with p_fdr
    df2 = pd.DataFrame({
        'term': ['Age:Domain'],
        'p_uncorrected': [0.01],
        'p_fdr': [0.02]
    })

    result2 = validate_hypothesis_test_dual_pvalues(
        df2,
        required_terms=['Age:Domain']
    )

    assert result2['valid'] is True


def test_empty_required_terms():
    """Test behavior when no terms are required (should still check D068)."""
    df = pd.DataFrame({
        'term': ['Age', 'Domain'],
        'p_uncorrected': [0.01, 0.05],
        'p_bonferroni': [0.03, 0.15]
    })

    result = validate_hypothesis_test_dual_pvalues(df, required_terms=[])

    # Should be valid if D068 compliant (has both p-value columns)
    assert result['valid'] is True
    assert result['d068_compliant'] is True
    assert len(result['missing_terms']) == 0


def test_empty_dataframe():
    """Test validation on empty DataFrame."""
    df = pd.DataFrame()

    result = validate_hypothesis_test_dual_pvalues(
        df,
        required_terms=['Age:Domain:Time']
    )

    assert result['valid'] is False
    assert 'Age:Domain:Time' in result['missing_terms']


def test_case_sensitive_term_matching():
    """Test that term names are case-sensitive."""
    df = pd.DataFrame({
        'term': ['age:domain:time'],  # lowercase
        'p_uncorrected': [0.003],
        'p_bonferroni': [0.045]
    })

    result = validate_hypothesis_test_dual_pvalues(
        df,
        required_terms=['Age:Domain:Time']  # Proper case
    )

    assert result['valid'] is False
    assert 'Age:Domain:Time' in result['missing_terms']


def test_realistic_rq510_scenario():
    """Test realistic RQ 5.10: Age × Domain × Time 3-way interaction."""
    # Typical fixed effects output from LMM
    df = pd.DataFrame({
        'term': [
            'Intercept',
            'Age_c',
            'Domain[What]',
            'Domain[Where]',
            'TSVR_hours',
            'Age_c:Domain[What]',
            'Age_c:Domain[Where]',
            'Age_c:TSVR_hours',
            'Domain[What]:TSVR_hours',
            'Domain[Where]:TSVR_hours',
            'Age_c:Domain[What]:TSVR_hours',
            'Age_c:Domain[Where]:TSVR_hours'
        ],
        'estimate': [0.5, 0.02, 0.3, 0.25, -0.05, 0.01, 0.015, -0.003, -0.02, -0.015, 0.005, 0.004],
        'se': [0.05] * 12,
        'z_statistic': [10.0, 1.0, 6.0, 5.0, -2.5, 0.5, 0.75, -1.0, -2.0, -1.5, 2.5, 2.0],
        'p_uncorrected': [0.000, 0.317, 0.000, 0.000, 0.012, 0.617, 0.453, 0.317, 0.046, 0.134, 0.012, 0.046],
        'p_bonferroni': [0.000, 1.000, 0.000, 0.000, 0.180, 1.000, 1.000, 1.000, 0.690, 1.000, 0.180, 0.690]
    })

    # RQ 5.10 hypothesis: Test 3-way interactions
    result = validate_hypothesis_test_dual_pvalues(
        df,
        required_terms=[
            'Age_c:Domain[What]:TSVR_hours',
            'Age_c:Domain[Where]:TSVR_hours'
        ],
        alpha_bonferroni=0.05
    )

    assert result['valid'] is True
    assert result['d068_compliant'] is True
    assert len(result['missing_terms']) == 0
    assert 'Decision D068' in result['message'] or 'd068' in result['message'].lower()
