"""
Tests for extract_marginal_age_slopes_by_domain function.

This function extracts domain-specific marginal age effects from a 3-way
Age×Domain×Time interaction LMM model using the delta method for standard errors.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.analysis_lmm import extract_marginal_age_slopes_by_domain


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def real_lmm_rq510():
    """Load real fitted LMM from RQ 5.10 step02."""
    from statsmodels.regression.mixed_linear_model import MixedLMResults
    model_path = PROJECT_ROOT / "results" / "ch5" / "rq10" / "data" / "step02_lmm_model.pkl"

    if not model_path.exists():
        pytest.skip(f"Real RQ 5.10 model not found: {model_path}")

    return MixedLMResults.load(str(model_path))


@pytest.fixture
def real_fixed_effects_rq510():
    """Load real fixed effects table from RQ 5.10 step02."""
    fe_path = PROJECT_ROOT / "results" / "ch5" / "rq10" / "data" / "step02_fixed_effects.csv"

    if not fe_path.exists():
        pytest.skip(f"Real RQ 5.10 fixed effects not found: {fe_path}")

    return pd.read_csv(fe_path, encoding='utf-8')


# =============================================================================
# Test 1: Function exists and has correct signature
# =============================================================================

def test_function_exists():
    """Test that extract_marginal_age_slopes_by_domain function exists."""
    assert callable(extract_marginal_age_slopes_by_domain)

    # Check signature
    import inspect
    sig = inspect.signature(extract_marginal_age_slopes_by_domain)
    params = list(sig.parameters.keys())

    assert 'lmm_result' in params
    assert 'eval_timepoint' in params
    assert 'domain_var' in params
    assert 'age_var' in params
    assert 'time_linear' in params
    assert 'time_log' in params


# =============================================================================
# Test 2: Returns DataFrame with correct structure
# =============================================================================

def test_returns_dataframe_with_correct_columns(real_lmm_rq510):
    """Test that function returns DataFrame with expected columns."""
    result = extract_marginal_age_slopes_by_domain(
        lmm_result=real_lmm_rq510,
        eval_timepoint=72.0
    )

    assert isinstance(result, pd.DataFrame)

    expected_cols = ['domain', 'age_slope', 'se', 'z', 'p', 'CI_lower', 'CI_upper']
    assert list(result.columns) == expected_cols


# =============================================================================
# Test 3: Returns 3 rows (one per domain)
# =============================================================================

def test_returns_three_rows(real_lmm_rq510):
    """Test that function returns exactly 3 rows (What, Where, When)."""
    result = extract_marginal_age_slopes_by_domain(
        lmm_result=real_lmm_rq510,
        eval_timepoint=72.0
    )

    assert len(result) == 3

    domains = set(result['domain'])
    assert domains == {'What', 'Where', 'When'}


# =============================================================================
# Test 4: Domain names are correct strings
# =============================================================================

def test_domain_names_are_strings(real_lmm_rq510):
    """Test that domain column contains strings."""
    result = extract_marginal_age_slopes_by_domain(
        lmm_result=real_lmm_rq510,
        eval_timepoint=72.0
    )

    assert result['domain'].dtype == object
    assert all(isinstance(d, str) for d in result['domain'])


# =============================================================================
# Test 5: All numeric columns are float
# =============================================================================

def test_numeric_columns_are_float(real_lmm_rq510):
    """Test that numeric columns are float dtype."""
    result = extract_marginal_age_slopes_by_domain(
        lmm_result=real_lmm_rq510,
        eval_timepoint=72.0
    )

    numeric_cols = ['age_slope', 'se', 'z', 'p', 'CI_lower', 'CI_upper']

    for col in numeric_cols:
        assert pd.api.types.is_float_dtype(result[col]), f"{col} should be float"


# =============================================================================
# Test 6: No NaN values
# =============================================================================

def test_no_nan_values(real_lmm_rq510):
    """Test that result contains no NaN values."""
    result = extract_marginal_age_slopes_by_domain(
        lmm_result=real_lmm_rq510,
        eval_timepoint=72.0
    )

    assert not result.isna().any().any(), "Result contains NaN values"


# =============================================================================
# Test 7: Standard errors are positive
# =============================================================================

def test_standard_errors_positive(real_lmm_rq510):
    """Test that all standard errors are positive."""
    result = extract_marginal_age_slopes_by_domain(
        lmm_result=real_lmm_rq510,
        eval_timepoint=72.0
    )

    assert all(result['se'] > 0), "Standard errors must be positive"


# =============================================================================
# Test 8: P-values are in valid range [0, 1]
# =============================================================================

def test_pvalues_valid_range(real_lmm_rq510):
    """Test that p-values are in [0, 1]."""
    result = extract_marginal_age_slopes_by_domain(
        lmm_result=real_lmm_rq510,
        eval_timepoint=72.0
    )

    assert all((result['p'] >= 0) & (result['p'] <= 1)), "P-values must be in [0, 1]"


# =============================================================================
# Test 9: Confidence intervals properly ordered
# =============================================================================

def test_confidence_intervals_ordered(real_lmm_rq510):
    """Test that CI_lower < CI_upper for all rows."""
    result = extract_marginal_age_slopes_by_domain(
        lmm_result=real_lmm_rq510,
        eval_timepoint=72.0
    )

    assert all(result['CI_lower'] < result['CI_upper']), "CI_lower must be < CI_upper"


# =============================================================================
# Test 10: Z-statistic computed correctly
# =============================================================================

def test_z_statistic_computed_correctly(real_lmm_rq510):
    """Test that z = age_slope / se."""
    result = extract_marginal_age_slopes_by_domain(
        lmm_result=real_lmm_rq510,
        eval_timepoint=72.0
    )

    expected_z = result['age_slope'] / result['se']
    np.testing.assert_allclose(result['z'], expected_z, rtol=1e-6)


# =============================================================================
# Test 11: Default parameters work
# =============================================================================

def test_default_parameters(real_lmm_rq510):
    """Test that function works with default parameters."""
    # Should work with only lmm_result
    result = extract_marginal_age_slopes_by_domain(lmm_result=real_lmm_rq510)

    assert len(result) == 3
    assert set(result['domain']) == {'What', 'Where', 'When'}


# =============================================================================
# Test 12: Custom eval_timepoint produces different results
# =============================================================================

def test_custom_eval_timepoint(real_lmm_rq510):
    """Test that different eval_timepoint changes results."""
    result_72 = extract_marginal_age_slopes_by_domain(
        lmm_result=real_lmm_rq510,
        eval_timepoint=72.0
    )

    result_24 = extract_marginal_age_slopes_by_domain(
        lmm_result=real_lmm_rq510,
        eval_timepoint=24.0
    )

    # Results should differ due to log term: 1/(TSVR+1) changes
    assert not np.allclose(result_72['age_slope'], result_24['age_slope'])


# =============================================================================
# Test 13: Reference domain (What) computed from 2-way terms only
# =============================================================================

def test_reference_domain_from_2way_terms(real_lmm_rq510):
    """Test that What domain uses only 2-way Age×Time terms (no 3-way)."""
    result = extract_marginal_age_slopes_by_domain(
        lmm_result=real_lmm_rq510,
        eval_timepoint=72.0
    )

    # Extract coefficients manually from LMM result
    from tools.analysis_lmm import extract_fixed_effects_from_lmm
    fe = extract_fixed_effects_from_lmm(real_lmm_rq510)
    beta_TSVR_Age = fe.loc[fe['Term'] == 'TSVR_hours:Age_c', 'Coef'].values[0]
    beta_log_Age = fe.loc[fe['Term'] == 'log_TSVR:Age_c', 'Coef'].values[0]

    # Compute expected What slope: β(TSVR:Age_c) + β(log_TSVR:Age_c) × 1/(72+1)
    expected_what = beta_TSVR_Age + beta_log_Age * (1.0 / (72.0 + 1.0))

    what_result = result.loc[result['domain'] == 'What', 'age_slope'].values[0]

    np.testing.assert_allclose(what_result, expected_what, rtol=1e-5)


# =============================================================================
# Test 14: Non-reference domains add 3-way interaction terms
# =============================================================================

def test_nonreference_domains_include_3way(real_lmm_rq510):
    """Test that Where/When add 3-way interaction terms to reference effect."""
    result = extract_marginal_age_slopes_by_domain(
        lmm_result=real_lmm_rq510,
        eval_timepoint=72.0
    )

    # Extract coefficients from LMM result
    from tools.analysis_lmm import extract_fixed_effects_from_lmm
    fe = extract_fixed_effects_from_lmm(real_lmm_rq510)
    beta_TSVR_Age = fe.loc[fe['Term'] == 'TSVR_hours:Age_c', 'Coef'].values[0]
    beta_log_Age = fe.loc[fe['Term'] == 'log_TSVR:Age_c', 'Coef'].values[0]

    beta_TSVR_Age_Where = fe.loc[fe['Term'] == 'TSVR_hours:Age_c:domain[T.Where]', 'Coef'].values[0]
    beta_log_Age_Where = fe.loc[fe['Term'] == 'log_TSVR:Age_c:domain[T.Where]', 'Coef'].values[0]

    # Expected Where slope
    expected_where = (beta_TSVR_Age + beta_TSVR_Age_Where) + \
                     (beta_log_Age + beta_log_Age_Where) * (1.0 / 73.0)

    where_result = result.loc[result['domain'] == 'Where', 'age_slope'].values[0]

    np.testing.assert_allclose(where_result, expected_where, rtol=1e-5)


# =============================================================================
# Test 15: Confidence intervals consistent with z and p
# =============================================================================

def test_confidence_intervals_consistent(real_lmm_rq510):
    """Test that 95% CIs are consistent with estimate and SE."""
    result = extract_marginal_age_slopes_by_domain(
        lmm_result=real_lmm_rq510,
        eval_timepoint=72.0
    )

    # 95% CI: estimate ± 1.96 * SE
    expected_lower = result['age_slope'] - 1.96 * result['se']
    expected_upper = result['age_slope'] + 1.96 * result['se']

    np.testing.assert_allclose(result['CI_lower'], expected_lower, rtol=1e-5)
    np.testing.assert_allclose(result['CI_upper'], expected_upper, rtol=1e-5)
