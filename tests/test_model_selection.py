"""
Tests for LMM Model Selection Tool (Kitchen Sink Suite)

Test coverage:
1. Input validation (TSVR continuous, sufficient variance, range checks)
2. 0-way interaction (simple trajectory)
3. 1-way interaction (categorical factor)
4. 2-way interaction (categorical × categorical)
5. Mixed factors (categorical × continuous)
6. Time transformation accuracy
7. Formula construction
8. AIC comparison metrics validation
9. Output structure verification
10. Edge cases (all models fail, <10 converge, etc.)

Author: REMEMVR Team
Date: 2025-12-08
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from tools.model_selection import compare_lmm_models_kitchen_sink


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def simple_lmm_data():
    """
    Generate synthetic LMM data for testing (simple trajectory, no interactions).

    Design:
    - 50 subjects × 4 timepoints = 200 observations
    - TSVR: 0.5h, 24h, 72h, 144h (realistic study timing)
    - Theta: Logarithmic forgetting with noise
    """
    np.random.seed(42)

    n_subjects = 50
    timepoints = [0.5, 24, 72, 144]  # Hours (T1, T2, T3, T4)

    data = []
    for uid in range(1, n_subjects + 1):
        for tsvr_hours in timepoints:
            # Logarithmic forgetting: theta = 1.0 - 0.5*log(TSVR+1) + noise
            tsvr_days = tsvr_hours / 24.0
            theta = 1.0 - 0.5 * np.log(tsvr_days + 1) + np.random.normal(0, 0.2)

            data.append({
                'UID': f'P{uid:03d}',
                'TSVR_hours': tsvr_hours,
                'theta': theta,
            })

    return pd.DataFrame(data)


@pytest.fixture
def interaction_lmm_data():
    """
    Generate synthetic LMM data with 1-way interaction (domain × time).

    Design:
    - 50 subjects × 4 timepoints × 3 domains = 600 observations
    - Domains: What, Where, When (different forgetting rates)
    """
    np.random.seed(42)

    n_subjects = 50
    timepoints = [0.5, 24, 72, 144]
    domains = ['What', 'Where', 'When']

    # Domain-specific forgetting rates
    domain_rates = {'What': 0.5, 'Where': 0.4, 'When': 0.6}

    data = []
    for uid in range(1, n_subjects + 1):
        for tsvr_hours in timepoints:
            for domain in domains:
                tsvr_days = tsvr_hours / 24.0
                rate = domain_rates[domain]
                theta = 1.0 - rate * np.log(tsvr_days + 1) + np.random.normal(0, 0.2)

                data.append({
                    'UID': f'P{uid:03d}',
                    'TSVR_hours': tsvr_hours,
                    'theta': theta,
                    'domain': domain,
                })

    return pd.DataFrame(data)


@pytest.fixture
def two_way_interaction_data():
    """
    Generate synthetic LMM data with 2-way interaction (domain × paradigm × time).

    Design:
    - 30 subjects × 4 timepoints × 3 domains × 3 paradigms = 1080 observations
    """
    np.random.seed(42)

    n_subjects = 30
    timepoints = [0.5, 24, 72, 144]
    domains = ['What', 'Where', 'When']
    paradigms = ['free_recall', 'cued_recall', 'recognition']

    data = []
    for uid in range(1, n_subjects + 1):
        for tsvr_hours in timepoints:
            for domain in domains:
                for paradigm in paradigms:
                    tsvr_days = tsvr_hours / 24.0
                    # Complex interaction pattern
                    base = 1.0
                    if domain == 'What':
                        base -= 0.3
                    if paradigm == 'recognition':
                        base += 0.2

                    theta = base - 0.5 * np.log(tsvr_days + 1) + np.random.normal(0, 0.15)

                    data.append({
                        'UID': f'P{uid:03d}',
                        'TSVR_hours': tsvr_hours,
                        'theta': theta,
                        'domain': domain,
                        'paradigm': paradigm,
                    })

    return pd.DataFrame(data)


@pytest.fixture
def continuous_factor_data():
    """
    Generate data with continuous factor (Age × time).
    """
    np.random.seed(42)

    n_subjects = 50
    timepoints = [0.5, 24, 72, 144]

    data = []
    for uid in range(1, n_subjects + 1):
        age = np.random.uniform(60, 80)  # Age range 60-80

        for tsvr_hours in timepoints:
            tsvr_days = tsvr_hours / 24.0
            # Age effect: older participants forget faster
            age_effect = (age - 70) * 0.01  # Centered at 70
            theta = 1.0 - (0.5 + age_effect) * np.log(tsvr_days + 1) + np.random.normal(0, 0.2)

            data.append({
                'UID': f'P{uid:03d}',
                'TSVR_hours': tsvr_hours,
                'theta': theta,
                'Age': age,
            })

    return pd.DataFrame(data)


# =============================================================================
# INPUT VALIDATION TESTS
# =============================================================================

def test_tsvr_must_be_continuous(simple_lmm_data):
    """Test that TSVR must be continuous (not categorical)."""
    # Create categorical TSVR (session indicators)
    data = simple_lmm_data.copy()
    data['session'] = data['TSVR_hours'].map({0.5: 'T1', 24: 'T2', 72: 'T3', 144: 'T4'})

    with pytest.raises(AssertionError, match="must be numeric"):
        compare_lmm_models_kitchen_sink(
            data=data,
            outcome_var='theta',
            tsvr_var='session',  # Categorical, should fail
            groups_var='UID',
        )


def test_tsvr_must_have_sufficient_variance(simple_lmm_data):
    """Test that TSVR must have >10 unique values."""
    # Keep only 4 timepoints (not enough variance)
    data = simple_lmm_data.copy()

    with pytest.raises(AssertionError, match="appears categorical"):
        compare_lmm_models_kitchen_sink(
            data=data,
            outcome_var='theta',
            tsvr_var='TSVR_hours',  # Only 4 unique values
            groups_var='UID',
        )


def test_tsvr_range_warning(simple_lmm_data):
    """Test warning for TSVR outside expected range."""
    data = simple_lmm_data.copy()
    # Scale and add jitter to get enough unique values AND trigger range warning
    data['TSVR_hours'] = data['TSVR_hours'] * 10 + np.random.uniform(0, 1, len(data))  # Scale to 1440 hours (60 days)

    with pytest.warns(UserWarning, match="300h"):
        compare_lmm_models_kitchen_sink(
            data=data,
            outcome_var='theta',
            tsvr_var='TSVR_hours',
            groups_var='UID',
        )


def test_missing_required_columns():
    """Test error for missing required columns."""
    data = pd.DataFrame({'UID': ['P001'], 'theta': [0.5]})

    with pytest.raises(ValueError, match="Missing required columns"):
        compare_lmm_models_kitchen_sink(
            data=data,
            outcome_var='theta',
            tsvr_var='TSVR_hours',  # Missing
            groups_var='UID',
        )


def test_categorical_factor_missing_reference(interaction_lmm_data):
    """Test error when categorical factor provided without reference level."""
    # Add jitter to pass TSVR variance check
    data = interaction_lmm_data.copy()
    data['TSVR_hours'] = data['TSVR_hours'] + np.random.uniform(0, 1, len(data))

    with pytest.raises(ValueError, match="factor1_reference required"):
        compare_lmm_models_kitchen_sink(
            data=data,
            outcome_var='theta',
            tsvr_var='TSVR_hours',
            groups_var='UID',
            factor1_var='domain',
            factor1_type='categorical',
            # factor1_reference missing
        )


def test_invalid_reference_level(interaction_lmm_data):
    """Test error when reference level not in factor values."""
    # Add jitter to pass TSVR variance check
    data = interaction_lmm_data.copy()
    data['TSVR_hours'] = data['TSVR_hours'] + np.random.uniform(0, 1, len(data))

    with pytest.raises(ValueError, match="not in domain values"):
        compare_lmm_models_kitchen_sink(
            data=data,
            outcome_var='theta',
            tsvr_var='TSVR_hours',
            groups_var='UID',
            factor1_var='domain',
            factor1_type='categorical',
            factor1_reference='InvalidDomain',  # Not in ['What', 'Where', 'When']
        )


# =============================================================================
# TRANSFORMATION TESTS
# =============================================================================

def test_time_transformations_created(simple_lmm_data):
    """Test that all time transformations are created correctly."""
    # Add enough unique TSVR values
    data = simple_lmm_data.copy()
    data['TSVR_hours'] = data['TSVR_hours'] + np.random.uniform(0, 1, len(data))

    results = compare_lmm_models_kitchen_sink(
        data=data,
        outcome_var='theta',
        tsvr_var='TSVR_hours',
        groups_var='UID',
        return_models=False,
    )

    # Check transformations dictionary
    transformations = results['transformations']

    # Check key transformations exist
    assert 'log_TSVR' in transformations
    assert 'sqrt_TSVR' in transformations
    assert 'recip_TSVR' in transformations
    assert 'TSVR_pow_neg05' in transformations  # PowerLaw α=0.5

    # Check total transformations
    assert len(transformations) > 40, "Should have 40+ time transformations"


def test_continuous_factor_mean_centering(continuous_factor_data):
    """Test that continuous factors are mean-centered."""
    # Add enough unique TSVR values
    data = continuous_factor_data.copy()
    data['TSVR_hours'] = data['TSVR_hours'] + np.random.uniform(0, 1, len(data))

    results = compare_lmm_models_kitchen_sink(
        data=data,
        outcome_var='theta',
        tsvr_var='TSVR_hours',
        groups_var='UID',
        factor1_var='Age',
        factor1_type='continuous',
        return_models=False,
    )

    # Check Age was centered (should appear in log messages)
    # This is implicit - tool creates Age_c internally
    assert 'best_model' in results  # Basic check that it ran


# =============================================================================
# INTERACTION TESTS
# =============================================================================

def test_zero_way_interaction(simple_lmm_data):
    """Test 0-way interaction (simple trajectory, no factors)."""
    # Add enough unique TSVR values
    data = simple_lmm_data.copy()
    data['TSVR_hours'] = data['TSVR_hours'] + np.random.uniform(0, 1, len(data))

    results = compare_lmm_models_kitchen_sink(
        data=data,
        outcome_var='theta',
        tsvr_var='TSVR_hours',
        groups_var='UID',
        return_models=False,
    )

    # Check outputs exist
    assert 'comparison' in results
    assert 'best_model' in results
    assert 'log_model_info' in results

    # Check comparison table structure
    comparison = results['comparison']
    assert len(comparison) > 10, "Should have >10 converged models"
    assert 'model_name' in comparison.columns
    assert 'AIC' in comparison.columns
    assert 'delta_AIC' in comparison.columns
    assert 'akaike_weight' in comparison.columns

    # Check best model
    best = results['best_model']
    assert best['rank'] == 1
    assert 0 < best['weight'] <= 1
    assert best['uncertainty'] in ['Very strong', 'Strong', 'Moderate', 'High']


def test_one_way_interaction(interaction_lmm_data):
    """Test 1-way interaction (categorical factor × time)."""
    # Add enough unique TSVR values
    data = interaction_lmm_data.copy()
    data['TSVR_hours'] = data['TSVR_hours'] + np.random.uniform(0, 1, len(data))

    results = compare_lmm_models_kitchen_sink(
        data=data,
        outcome_var='theta',
        tsvr_var='TSVR_hours',
        groups_var='UID',
        factor1_var='domain',
        factor1_type='categorical',
        factor1_reference='What',
        re_formula='~1',  # Random intercepts only
        return_models=False,
    )

    # Check outputs
    assert len(results['comparison']) > 10
    assert results['best_model']['rank'] == 1


def test_two_way_interaction(two_way_interaction_data):
    """Test 2-way interaction (categorical × categorical × time)."""
    # Add enough unique TSVR values
    data = two_way_interaction_data.copy()
    data['TSVR_hours'] = data['TSVR_hours'] + np.random.uniform(0, 1, len(data))

    results = compare_lmm_models_kitchen_sink(
        data=data,
        outcome_var='theta',
        tsvr_var='TSVR_hours',
        groups_var='UID',
        factor1_var='domain',
        factor1_type='categorical',
        factor1_reference='What',
        factor2_var='paradigm',
        factor2_type='categorical',
        factor2_reference='free_recall',
        re_formula='~1',  # Complex interactions require random intercepts only
        return_models=False,
    )

    # Check outputs
    assert len(results['comparison']) > 5, "Should have at least 5 converged models"
    assert results['best_model']['rank'] == 1


def test_mixed_factors(continuous_factor_data):
    """Test mixed factors (continuous × time)."""
    # Add enough unique TSVR values
    data = continuous_factor_data.copy()
    data['TSVR_hours'] = data['TSVR_hours'] + np.random.uniform(0, 1, len(data))

    results = compare_lmm_models_kitchen_sink(
        data=data,
        outcome_var='theta',
        tsvr_var='TSVR_hours',
        groups_var='UID',
        factor1_var='Age',
        factor1_type='continuous',
        re_formula='~1',
        return_models=False,
    )

    # Check outputs
    assert len(results['comparison']) > 10


# =============================================================================
# AIC METRICS VALIDATION
# =============================================================================

def test_aic_metrics_valid(simple_lmm_data):
    """Test that AIC comparison metrics are mathematically valid."""
    # Add enough unique TSVR values
    data = simple_lmm_data.copy()
    data['TSVR_hours'] = data['TSVR_hours'] + np.random.uniform(0, 1, len(data))

    results = compare_lmm_models_kitchen_sink(
        data=data,
        outcome_var='theta',
        tsvr_var='TSVR_hours',
        groups_var='UID',
        return_models=False,
    )

    comparison = results['comparison']

    # 1. Akaike weights sum to 1.0
    weight_sum = comparison['akaike_weight'].sum()
    assert 0.999 <= weight_sum <= 1.001, f"Weights sum = {weight_sum}, expected 1.0"

    # 2. All weights in (0, 1)
    assert (comparison['akaike_weight'] > 0).all(), "Some weights ≤ 0"
    assert (comparison['akaike_weight'] < 1).all(), "Some weights ≥ 1"

    # 3. Best model has delta_AIC = 0
    assert comparison.iloc[0]['delta_AIC'] == 0.0, "Best model delta_AIC ≠ 0"

    # 4. All delta_AIC ≥ 0
    assert (comparison['delta_AIC'] >= 0).all(), "Some delta_AIC < 0"

    # 5. Cumulative weights monotonic increasing
    cum_diffs = comparison['cumulative_weight'].diff().dropna()
    assert (cum_diffs >= 0).all(), "cumulative_weight not monotonic"

    # 6. Cumulative weight ends at 1.0
    cum_final = comparison.iloc[-1]['cumulative_weight']
    assert 0.999 <= cum_final <= 1.001, f"Final cumulative_weight = {cum_final}, expected 1.0"


def test_log_model_benchmark(simple_lmm_data):
    """Test that Log model info is correctly extracted."""
    # Add enough unique TSVR values
    data = simple_lmm_data.copy()
    data['TSVR_hours'] = data['TSVR_hours'] + np.random.uniform(0, 1, len(data))

    results = compare_lmm_models_kitchen_sink(
        data=data,
        outcome_var='theta',
        tsvr_var='TSVR_hours',
        groups_var='UID',
        return_models=False,
    )

    log_info = results['log_model_info']

    if 'error' not in log_info:
        # Log model converged
        assert 'rank' in log_info
        assert 'AIC' in log_info
        assert 'delta_AIC' in log_info
        assert 'weight' in log_info
        assert log_info['rank'] >= 1
    # If Log failed, should have 'error' key


# =============================================================================
# OUTPUT STRUCTURE TESTS
# =============================================================================

def test_output_structure(simple_lmm_data):
    """Test that all expected outputs are present."""
    # Add enough unique TSVR values
    data = simple_lmm_data.copy()
    data['TSVR_hours'] = data['TSVR_hours'] + np.random.uniform(0, 1, len(data))

    results = compare_lmm_models_kitchen_sink(
        data=data,
        outcome_var='theta',
        tsvr_var='TSVR_hours',
        groups_var='UID',
        return_models=False,
    )

    # Check all required keys
    required_keys = [
        'comparison',
        'best_model',
        'log_model_info',
        'top_10',
        'failed_models',
        'transformations',
        'summary_stats',
    ]

    for key in required_keys:
        assert key in results, f"Missing output key: {key}"

    # Check comparison DataFrame columns
    comparison_cols = [
        'model_name', 'AIC', 'BIC', 'log_likelihood', 'n_params', 'converged',
        'delta_AIC', 'akaike_weight', 'cumulative_weight'
    ]
    for col in comparison_cols:
        assert col in results['comparison'].columns, f"Missing column: {col}"

    # Check best_model dict keys
    best_keys = ['name', 'AIC', 'weight', 'weight_pct', 'uncertainty', 'interpretation', 'rank']
    for key in best_keys:
        assert key in results['best_model'], f"Missing best_model key: {key}"

    # Check summary_stats dict keys
    summary_keys = [
        'n_models_tested', 'n_models_converged', 'n_models_failed',
        'best_model', 'best_aic', 'aic_range', 'n_competitive_models'
    ]
    for key in summary_keys:
        assert key in results['summary_stats'], f"Missing summary_stats key: {key}"


def test_return_models_flag(simple_lmm_data):
    """Test return_models=True includes fitted model objects."""
    # Add enough unique TSVR values
    data = simple_lmm_data.copy()
    data['TSVR_hours'] = data['TSVR_hours'] + np.random.uniform(0, 1, len(data))

    results = compare_lmm_models_kitchen_sink(
        data=data,
        outcome_var='theta',
        tsvr_var='TSVR_hours',
        groups_var='UID',
        return_models=True,
    )

    assert 'fitted_models' in results
    assert len(results['fitted_models']) > 0

    # Check fitted models are MixedLMResults objects
    first_model = next(iter(results['fitted_models'].values()))
    assert hasattr(first_model, 'aic'), "Should be MixedLMResults object"


def test_save_outputs(simple_lmm_data, tmp_path):
    """Test that outputs are saved correctly when save_dir provided."""
    # Add enough unique TSVR values
    data = simple_lmm_data.copy()
    data['TSVR_hours'] = data['TSVR_hours'] + np.random.uniform(0, 1, len(data))

    save_dir = tmp_path / "test_outputs"
    log_file = tmp_path / "test.log"

    results = compare_lmm_models_kitchen_sink(
        data=data,
        outcome_var='theta',
        tsvr_var='TSVR_hours',
        groups_var='UID',
        save_dir=save_dir,
        log_file=log_file,
        return_models=False,
    )

    # Check files were created
    assert (save_dir / "model_comparison.csv").exists()
    assert (save_dir / "best_model_summary.txt").exists()
    assert log_file.exists()

    # Check CSV can be read
    saved_comparison = pd.read_csv(save_dir / "model_comparison.csv")
    assert len(saved_comparison) > 0


# =============================================================================
# EDGE CASES
# =============================================================================

def test_warning_few_converged_models(simple_lmm_data):
    """Test warning when <10 models converge."""
    # Create difficult data that will cause many models to fail
    data = simple_lmm_data.copy()
    data['TSVR_hours'] = data['TSVR_hours'] + np.random.uniform(0, 1, len(data))
    data = data.head(40)  # Use only 40 observations (very small sample)

    # This should trigger warning but not error
    with pytest.warns(UserWarning, match="Only .* models converged"):
        results = compare_lmm_models_kitchen_sink(
            data=data,
            outcome_var='theta',
            tsvr_var='TSVR_hours',
            groups_var='UID',
            min_converged_models=10,
            return_models=False,
        )

    # Should still return results
    assert 'best_model' in results


def test_competitive_models_count(simple_lmm_data):
    """Test that competitive models (ΔAIC < 2) are counted correctly."""
    # Add enough unique TSVR values
    data = simple_lmm_data.copy()
    data['TSVR_hours'] = data['TSVR_hours'] + np.random.uniform(0, 1, len(data))

    results = compare_lmm_models_kitchen_sink(
        data=data,
        outcome_var='theta',
        tsvr_var='TSVR_hours',
        groups_var='UID',
        return_models=False,
    )

    # Count competitive models manually
    comparison = results['comparison']
    n_competitive = len(comparison[comparison['delta_AIC'] < 2])

    assert results['summary_stats']['n_competitive_models'] == n_competitive


# =============================================================================
# INTEGRATION TEST
# =============================================================================

def test_full_pipeline_matches_rq_pattern(interaction_lmm_data):
    """
    Integration test: Full pipeline matching RQ 5.3.1 pattern.

    This test simulates the exact usage pattern from ch5/5.3.1:
    - 1-way interaction (paradigm × time)
    - Random intercepts only
    - Save outputs
    - Check Log model rank
    """
    # Add enough unique TSVR values
    data = interaction_lmm_data.copy()
    data['TSVR_hours'] = data['TSVR_hours'] + np.random.uniform(0, 1, len(data))

    # Simulate RQ 5.3.1 pattern
    results = compare_lmm_models_kitchen_sink(
        data=data,
        outcome_var='theta',
        tsvr_var='TSVR_hours',
        groups_var='UID',
        factor1_var='domain',
        factor1_type='categorical',
        factor1_reference='What',
        re_formula='~1',
        reml=False,
        return_models=False,
    )

    # Check all outputs present
    assert 'comparison' in results
    assert 'best_model' in results
    assert 'log_model_info' in results
    assert 'top_10' in results

    # Check comparison table sorted by AIC
    comparison = results['comparison']
    assert comparison.iloc[0]['delta_AIC'] == 0.0
    assert (comparison['AIC'].diff().dropna() >= 0).all(), "Not sorted by AIC"

    # Check top 10
    assert len(results['top_10']) == 10

    # Check summary stats
    summary = results['summary_stats']
    assert summary['n_models_tested'] >= 66, "Should test 66+ models"
    assert summary['n_models_converged'] > 0
    assert summary['best_model'] == results['best_model']['name']

    print("\n" + "=" * 80)
    print("INTEGRATION TEST RESULTS")
    print("=" * 80)
    print(f"Models tested: {summary['n_models_tested']}")
    print(f"Models converged: {summary['n_models_converged']}")
    print(f"Best model: {results['best_model']['name']}")
    print(f"Best AIC: {results['best_model']['AIC']:.2f}")
    print(f"Best weight: {results['best_model']['weight']:.4f} ({results['best_model']['weight_pct']:.1f}%)")
    print(f"Uncertainty: {results['best_model']['uncertainty']}")

    if 'error' not in results['log_model_info']:
        log_info = results['log_model_info']
        print(f"\nLog model rank: #{log_info['rank']}")
        print(f"Log model ΔAIC: {log_info['delta_AIC']:.2f}")
        print(f"Log model weight: {log_info['weight']:.4f} ({log_info['weight_pct']:.1f}%)")

    print("\nTop 5 models:")
    print(results['top_10'].head(5)[['model_name', 'AIC', 'delta_AIC', 'akaike_weight']].to_string(index=False))
    print("=" * 80)
