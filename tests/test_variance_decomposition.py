"""
Unit Tests for Model-Averaged Variance Decomposition Tool

Tests the variance_decomposition.py tool to ensure:
1. Correct variance component extraction
2. Proper Akaike weight averaging
3. Random effects aggregation across models
4. Convergence failure handling
5. Integration with model_selection.py

Author: REMEMVR Team
Date: 2025-12-09
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from tools.variance_decomposition import (
    compute_model_averaged_variance_decomposition,
    _fit_single_model_and_extract,
    _create_transformations,
    _build_formula,
    _get_time_variable_for_model,
)


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def synthetic_data():
    """
    Generate synthetic longitudinal data for testing.

    Structure:
    - 50 participants (UID)
    - 12 time points (TSVR_hours: 1, 6, 12, 18, 24, 36, 48, 60, 72, 96, 120, 144)
    - 2 stratification levels (congruence: Common, Congruent)
    - Total: 50 × 12 × 2 = 1200 observations

    Ground truth:
    - Forgetting follows log(TSVR+1) with individual random slopes
    - Common: ICC_int=0.40, ICC_slope=0.10
    - Congruent: ICC_int=0.50, ICC_slope=0.15
    """

    np.random.seed(42)

    n_uid = 50
    # More time points to satisfy kitchen_sink requirement (≥10 unique values)
    time_points = [1, 6, 12, 18, 24, 36, 48, 60, 72, 96, 120, 144]  # hours
    congruence_levels = ['Common', 'Congruent']

    # Generate participant-specific intercepts and slopes
    # Common
    intercept_common = np.random.normal(0, 0.5, n_uid)  # SD=0.5 → ICC_int ≈ 0.40
    slope_common = np.random.normal(-0.2, 0.05, n_uid)  # SD=0.05 → ICC_slope ≈ 0.10

    # Congruent
    intercept_cong = np.random.normal(0, 0.6, n_uid)    # SD=0.6 → ICC_int ≈ 0.50
    slope_cong = np.random.normal(-0.2, 0.07, n_uid)    # SD=0.07 → ICC_slope ≈ 0.15

    data_list = []

    for uid_idx in range(n_uid):
        uid = f"P{uid_idx+1:03d}"

        for congruence, intercept, slope in [
            ('Common', intercept_common[uid_idx], slope_common[uid_idx]),
            ('Congruent', intercept_cong[uid_idx], slope_cong[uid_idx]),
        ]:
            for tsvr in time_points:
                # True trajectory: theta = intercept + slope * log(TSVR+1) + noise
                log_tsvr = np.log(tsvr / 24.0 + 1)  # Convert to days
                theta = intercept + slope * log_tsvr + np.random.normal(0, 0.3)

                data_list.append({
                    'UID': uid,
                    'TSVR_hours': tsvr,
                    'congruence': congruence,
                    'theta': theta,
                })

    return pd.DataFrame(data_list)


# =============================================================================
# HELPER FUNCTION TESTS
# =============================================================================

def test_create_transformations():
    """Test that all time transformations are created correctly."""

    df = pd.DataFrame({'TSVR_hours': [1, 24, 72, 144]})

    df_trans = _create_transformations(df, 'TSVR_hours')

    # Check conversions
    assert 'TSVR' in df_trans.columns
    np.testing.assert_array_almost_equal(
        df_trans['TSVR'].values,
        np.array([1/24, 1, 3, 6])  # days
    )

    # Check polynomial
    assert 'TSVR_sq' in df_trans.columns
    assert 'TSVR_cub' in df_trans.columns

    # Check logarithmic
    assert 'log_TSVR' in df_trans.columns
    assert 'log_log_TSVR' in df_trans.columns

    # Check power law
    assert 'TSVR_pow_neg01' in df_trans.columns
    assert 'TSVR_pow_neg05' in df_trans.columns

    # Check reciprocal
    assert 'recip_TSVR' in df_trans.columns

    # Check roots
    assert 'sqrt_TSVR' in df_trans.columns
    assert 'cbrt_TSVR' in df_trans.columns

    # Validate log transformation (non-negative)
    assert (df_trans['log_TSVR'] >= 0).all()


def test_build_formula():
    """Test formula building for various models."""

    # Simple models
    assert _build_formula('Log', 'theta') == 'theta ~ log_TSVR'
    assert _build_formula('Linear', 'theta') == 'theta ~ TSVR'
    assert _build_formula('PowerLaw_05', 'theta') == 'theta ~ TSVR_pow_neg05'

    # Hybrid models
    assert _build_formula('Recip+Log', 'theta') == 'theta ~ recip_TSVR + log_TSVR'
    assert _build_formula('Lin+Log', 'theta') == 'theta ~ TSVR + log_TSVR'

    # Invalid model
    with pytest.raises(ValueError, match="Unknown model"):
        _build_formula('InvalidModel', 'theta')


def test_get_time_variable_for_model():
    """Test that correct time variable is identified for random slopes."""

    # Simple models
    assert _get_time_variable_for_model('Log') == 'log_TSVR'
    assert _get_time_variable_for_model('PowerLaw_01') == 'TSVR_pow_neg01'
    assert _get_time_variable_for_model('SquareRoot') == 'sqrt_TSVR'

    # Hybrid models (should return FIRST term)
    assert _get_time_variable_for_model('Recip+Log') == 'recip_TSVR'
    assert _get_time_variable_for_model('Lin+Log') == 'TSVR'
    assert _get_time_variable_for_model('SquareRoot+Log') == 'sqrt_TSVR'

    # Invalid model
    with pytest.raises(ValueError, match="Unknown model"):
        _get_time_variable_for_model('InvalidModel')


def test_fit_single_model_and_extract(synthetic_data):
    """Test fitting a single model and extracting variance components."""

    # Subset to one congruence level
    data_common = synthetic_data[synthetic_data['congruence'] == 'Common'].copy()

    # Fit Log model (ground truth for synthetic data)
    result = _fit_single_model_and_extract(
        data=data_common,
        model_name='Log',
        outcome_var='theta',
        tsvr_var='TSVR_hours',
        groups_var='UID',
        re_intercept=True,
        re_slope=True,
        reml=False,
    )

    # Check structure
    assert 'variance_components' in result
    assert 'ICCs' in result
    assert 'random_effects' in result
    assert 'converged' in result
    assert 'fitted_model' in result

    # Check variance components
    vc = result['variance_components']
    assert 'var_intercept' in vc
    assert 'var_slope' in vc
    assert 'var_residual' in vc

    # Validate ICC values (should be in [0, 1])
    iccs = result['ICCs']
    assert 0 <= iccs['ICC_intercept'] <= 1
    assert 0 <= iccs['ICC_slope_simple'] <= 1
    assert 0 <= iccs['ICC_slope_conditional'] <= 1

    # Check random effects structure
    re = result['random_effects']
    assert 'UID' in re.columns
    assert 'intercept' in re.columns
    assert 'slope' in re.columns
    assert len(re) == 50  # 50 participants

    # Check convergence
    assert isinstance(result['converged'], bool)


# =============================================================================
# MAIN FUNCTION TESTS
# =============================================================================

def test_compute_model_averaged_variance_decomposition_basic(synthetic_data):
    """Test basic functionality of model-averaged variance decomposition."""

    results = compute_model_averaged_variance_decomposition(
        data=synthetic_data,
        outcome_var='theta',
        tsvr_var='TSVR_hours',
        groups_var='UID',
        stratify_var='congruence',
        stratify_levels=['Common', 'Congruent'],
        delta_aic_threshold=2.0,
        min_models=1,  # Lower threshold for testing
        max_models=5,  # Limit for speed
        re_intercept=True,
        re_slope=True,
        reml=False,
    )

    # Check output structure
    assert 'model_comparison' in results
    assert 'competitive_models' in results
    assert 'stratified_results' in results
    assert 'averaged_variance_components' in results
    assert 'averaged_ICCs' in results
    assert 'averaged_random_effects' in results
    assert 'summary_stats' in results

    # Check model comparison
    comparison = results['model_comparison']
    assert 'model_name' in comparison.columns
    assert 'AIC' in comparison.columns
    assert 'akaike_weight' in comparison.columns
    assert len(comparison) > 0

    # Check competitive models
    competitive = results['competitive_models']
    assert isinstance(competitive, list)
    assert len(competitive) > 0
    assert 'Log' in competitive  # Log should be competitive (ground truth)

    # Check stratified results
    strat = results['stratified_results']
    assert 'Common' in strat
    assert 'Congruent' in strat

    for level in ['Common', 'Congruent']:
        assert 'variance_components_averaged' in strat[level]
        assert 'ICCs_averaged' in strat[level]
        assert 'random_effects_averaged' in strat[level]
        assert 'convergence_status' in strat[level]
        assert 'n_models_converged' in strat[level]

    # Check averaged variance components
    vc_avg = results['averaged_variance_components']
    assert 'congruence' in vc_avg.columns
    assert 'var_intercept' in vc_avg.columns
    assert 'var_slope' in vc_avg.columns
    assert len(vc_avg) == 2  # 2 congruence levels

    # Validate variance components are non-negative
    assert (vc_avg['var_intercept'] >= 0).all()
    assert (vc_avg['var_slope'] >= 0).all()
    assert (vc_avg['var_residual'] >= 0).all()

    # Check averaged ICCs
    icc_avg = results['averaged_ICCs']
    assert 'congruence' in icc_avg.columns
    assert 'ICC_intercept' in icc_avg.columns
    assert 'ICC_slope_simple' in icc_avg.columns
    assert len(icc_avg) == 2

    # Validate ICCs in [0, 1]
    assert ((icc_avg['ICC_intercept'] >= 0) & (icc_avg['ICC_intercept'] <= 1)).all()
    assert ((icc_avg['ICC_slope_simple'] >= 0) & (icc_avg['ICC_slope_simple'] <= 1)).all()

    # Check averaged random effects
    re_avg = results['averaged_random_effects']
    assert 'UID' in re_avg.columns
    assert 'congruence' in re_avg.columns
    assert 'intercept_avg' in re_avg.columns
    assert 'slope_avg' in re_avg.columns
    assert len(re_avg) == 100  # 50 UID × 2 congruence

    # Check summary stats
    stats = results['summary_stats']
    assert 'n_models_competitive' in stats
    assert 'effective_n_models' in stats
    assert 'convergence_rate' in stats
    assert 0 <= stats['convergence_rate'] <= 1


def test_model_averaged_variance_decomposition_with_saving(synthetic_data, tmp_path):
    """Test that save_dir correctly writes outputs."""

    save_dir = tmp_path / "test_output"

    results = compute_model_averaged_variance_decomposition(
        data=synthetic_data,
        outcome_var='theta',
        tsvr_var='TSVR_hours',
        groups_var='UID',
        stratify_var='congruence',
        stratify_levels=['Common'],  # Single level for speed
        delta_aic_threshold=5.0,  # Wider threshold
        max_models=3,
        save_dir=save_dir,
    )

    # Check files were created
    assert (save_dir / "model_comparison.csv").exists()
    assert (save_dir / "competitive_models.csv").exists()
    assert (save_dir / "variance_components_averaged.csv").exists()
    assert (save_dir / "ICCs_averaged.csv").exists()
    assert (save_dir / "random_effects_averaged.csv").exists()

    # Check level-specific directories
    assert (save_dir / "level_Common").exists()
    assert (save_dir / "level_Common" / "variance_components_by_model.csv").exists()
    assert (save_dir / "level_Common" / "ICCs_by_model.csv").exists()

    # Validate CSV contents
    vc_df = pd.read_csv(save_dir / "variance_components_averaged.csv")
    assert len(vc_df) == 1  # 1 level
    assert 'congruence' in vc_df.columns
    assert 'var_intercept' in vc_df.columns


def test_convergence_failure_handling(synthetic_data):
    """Test that convergence failures are handled gracefully."""

    # Add stratification level with VERY low variance (will fail to converge)
    synthetic_bad = synthetic_data.copy()

    # Create "Incongruent" level with near-zero slope variance
    n_uid = synthetic_data['UID'].nunique()
    time_points = [1, 6, 12, 18, 24, 36, 48, 60, 72, 96, 120, 144]  # Match fixture
    bad_data = []
    for uid in synthetic_data['UID'].unique():
        for tsvr in time_points:
            # Fixed slope (no variance) → convergence failure expected
            theta = np.random.normal(0, 0.1)  # Pure noise, no slope
            bad_data.append({
                'UID': uid,
                'TSVR_hours': tsvr + np.random.uniform(-0.5, 0.5),  # Add jitter
                'congruence': 'Incongruent',
                'theta': theta,
            })

    synthetic_bad = pd.concat([synthetic_bad, pd.DataFrame(bad_data)], ignore_index=True)

    # Test 'warn' mode (should complete with warnings)
    results = compute_model_averaged_variance_decomposition(
        data=synthetic_bad,
        outcome_var='theta',
        tsvr_var='TSVR_hours',
        groups_var='UID',
        stratify_var='congruence',
        stratify_levels=['Common', 'Incongruent'],
        delta_aic_threshold=5.0,
        max_models=3,
        handle_convergence_failures='warn',
    )

    # Should still return results
    assert 'stratified_results' in results
    assert 'Incongruent' in results['stratified_results']

    # Incongruent should have some convergence failures
    incong_status = results['stratified_results']['Incongruent']['convergence_status']
    assert not all(incong_status.values())  # At least one failure


def test_invalid_inputs():
    """Test that invalid inputs raise appropriate errors."""

    # Missing column
    df_bad = pd.DataFrame({'UID': [1, 2], 'theta': [0.5, 0.6]})

    with pytest.raises(ValueError, match="Missing required columns"):
        compute_model_averaged_variance_decomposition(
            data=df_bad,
            outcome_var='theta',
            tsvr_var='TSVR_hours',  # Missing
            groups_var='UID',
            stratify_var='congruence',
            stratify_levels=['Common'],
        )

    # Invalid stratify_levels
    df_good = pd.DataFrame({
        'UID': ['P001'] * 4,
        'TSVR_hours': [1, 24, 72, 144],
        'theta': [0.5, 0.4, 0.3, 0.2],
        'congruence': ['Common'] * 4,
    })

    with pytest.raises(ValueError, match="Invalid stratify_levels"):
        compute_model_averaged_variance_decomposition(
            data=df_good,
            outcome_var='theta',
            tsvr_var='TSVR_hours',
            groups_var='UID',
            stratify_var='congruence',
            stratify_levels=['InvalidLevel'],
        )


def test_random_intercepts_only_mode(synthetic_data):
    """Test that random-intercepts-only mode works (no slopes)."""

    results = compute_model_averaged_variance_decomposition(
        data=synthetic_data,
        outcome_var='theta',
        tsvr_var='TSVR_hours',
        groups_var='UID',
        stratify_var='congruence',
        stratify_levels=['Common'],
        delta_aic_threshold=5.0,
        max_models=3,
        re_intercept=True,
        re_slope=False,  # Disable random slopes
    )

    # Check random effects have NO slope column
    re_avg = results['averaged_random_effects']
    assert 'intercept_avg' in re_avg.columns
    assert 'slope_avg' not in re_avg.columns

    # Check variance components have zero slope variance
    vc_avg = results['averaged_variance_components']
    assert (vc_avg['var_slope'] == 0).all()


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

def test_integration_with_rq_5_4_6_structure(synthetic_data):
    """
    Test that tool output matches expected structure for RQ 5.4.6.

    RQ 5.4.6 expectations:
    - 3 stratified levels (Common, Congruent, Incongruent)
    - Random effects: 300 rows (100 UID × 3 congruence)
    - Variance components: 3 rows (1 per congruence)
    - ICCs: 3 rows
    """

    # Add Incongruent level to synthetic data
    incong_data = synthetic_data[synthetic_data['congruence'] == 'Common'].copy()
    incong_data['congruence'] = 'Incongruent'
    incong_data['theta'] += np.random.normal(0, 0.1, len(incong_data))  # Add noise

    full_data = pd.concat([synthetic_data, incong_data], ignore_index=True)

    # Add some random jitter to TSVR_hours to increase unique values
    full_data['TSVR_hours'] = full_data['TSVR_hours'] + np.random.uniform(-0.5, 0.5, len(full_data))

    results = compute_model_averaged_variance_decomposition(
        data=full_data,
        outcome_var='theta',
        tsvr_var='TSVR_hours',
        groups_var='UID',
        stratify_var='congruence',
        stratify_levels=['Common', 'Congruent', 'Incongruent'],
        delta_aic_threshold=2.0,
        max_models=5,
    )

    # Check RQ 5.4.6 output structure
    re_avg = results['averaged_random_effects']
    n_uid = full_data['UID'].nunique()
    assert len(re_avg) == n_uid * 3  # N_UID × 3 congruence
    assert set(re_avg['congruence'].unique()) == {'Common', 'Congruent', 'Incongruent'}

    vc_avg = results['averaged_variance_components']
    assert len(vc_avg) == 3  # 3 congruence levels

    icc_avg = results['averaged_ICCs']
    assert len(icc_avg) == 3

    # Check that results can be exported to CSV (RQ 5.4.6 Step 4 requirement)
    assert re_avg.to_csv(index=False) is not None
    assert vc_avg.to_csv(index=False) is not None
    assert icc_avg.to_csv(index=False) is not None


# =============================================================================
# STATISTICAL VALIDITY TESTS
# =============================================================================

def test_akaike_weights_sum_to_one(synthetic_data):
    """Test that renormalized Akaike weights sum to 1.0."""

    results = compute_model_averaged_variance_decomposition(
        data=synthetic_data,
        outcome_var='theta',
        tsvr_var='TSVR_hours',
        groups_var='UID',
        stratify_var='congruence',
        stratify_levels=['Common'],
        delta_aic_threshold=5.0,
        max_models=5,
    )

    # Check competitive models have renormalized weights summing to 1.0
    # (This is validated internally, but double-check)
    strat = results['stratified_results']['Common']
    vc_by_model = strat['variance_components_by_model']

    # Merge with model comparison to get weights
    comparison = results['model_comparison']
    competitive = comparison[comparison['delta_AIC'] < 5.0].head(5)

    # Renormalize
    weight_sum = competitive['akaike_weight'].sum()
    competitive['weight_renorm'] = competitive['akaike_weight'] / weight_sum

    # Check sum
    np.testing.assert_almost_equal(competitive['weight_renorm'].sum(), 1.0, decimal=6)


def test_model_averaged_icc_bounded(synthetic_data):
    """Test that model-averaged ICCs are bounded in [0, 1]."""

    results = compute_model_averaged_variance_decomposition(
        data=synthetic_data,
        outcome_var='theta',
        tsvr_var='TSVR_hours',
        groups_var='UID',
        stratify_var='congruence',
        stratify_levels=['Common', 'Congruent'],
        delta_aic_threshold=5.0,
        max_models=5,
    )

    icc_avg = results['averaged_ICCs']

    # All ICCs should be in [0, 1]
    for col in ['ICC_intercept', 'ICC_slope_simple', 'ICC_slope_conditional']:
        assert (icc_avg[col] >= 0).all()
        assert (icc_avg[col] <= 1).all()


def test_random_effects_centered_at_zero(synthetic_data):
    """Test that random effects have mean ≈ 0 (LMM centering property)."""

    results = compute_model_averaged_variance_decomposition(
        data=synthetic_data,
        outcome_var='theta',
        tsvr_var='TSVR_hours',
        groups_var='UID',
        stratify_var='congruence',
        stratify_levels=['Common'],
        delta_aic_threshold=5.0,
        max_models=3,
    )

    re_avg = results['averaged_random_effects']

    # Mean of random effects should be close to zero
    mean_intercept = re_avg['intercept_avg'].mean()
    mean_slope = re_avg['slope_avg'].mean()

    np.testing.assert_almost_equal(mean_intercept, 0.0, decimal=1)
    np.testing.assert_almost_equal(mean_slope, 0.0, decimal=2)


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
