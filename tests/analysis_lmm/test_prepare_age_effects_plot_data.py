"""
Tests for prepare_age_effects_plot_data function (Tool 6/25)

Purpose: Create age tertiles, aggregate means, generate predictions for RQ 5.10 visualization
TDD Status: RED phase (tests written first, function not yet implemented)
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from unittest.mock import Mock
from tools.analysis_lmm import prepare_age_effects_plot_data


@pytest.fixture
def mock_lmm_input():
    """Create mock LMM input DataFrame with age, domain, TSVR, theta"""
    np.random.seed(42)
    n_subjects = 60
    n_timepoints = 4
    domains = ['What', 'Where', 'When']

    rows = []
    for uid in range(1, n_subjects + 1):
        age = np.random.uniform(18, 75)  # Continuous age
        for domain in domains:
            for tsvr in [0, 24, 72, 144]:  # Hours: 0, 1d, 3d, 6d
                theta = np.random.normal(0, 1)
                rows.append({
                    'UID': uid,
                    'Age': age,
                    'domain_name': domain,
                    'TSVR_hours': tsvr,
                    'theta': theta
                })

    return pd.DataFrame(rows)


@pytest.fixture
def mock_lmm_model():
    """Create mock MixedLMResults with fittedvalues and predict method"""
    model = Mock()
    # Mock fitted values (720 rows = 60 subjects × 3 domains × 4 timepoints)
    model.fittedvalues = pd.Series(np.random.normal(0, 0.5, 720))
    # Mock predict method
    model.predict = Mock(return_value=np.random.normal(0, 0.5, 100))
    model.fe_params = pd.Series({'Intercept': 0.5, 'TSVR_hours': -0.01, 'Age_c': 0.02})
    return model


def test_basic_structure(mock_lmm_input, mock_lmm_model, tmp_path):
    """Test output has required columns"""
    output_path = tmp_path / "age_effects_plot_data.csv"
    result = prepare_age_effects_plot_data(
        lmm_input=mock_lmm_input,
        lmm_model=mock_lmm_model,
        output_path=output_path
    )

    # Check DataFrame returned
    assert isinstance(result, pd.DataFrame)

    # Required columns for rq_plots
    required_cols = ['domain_name', 'age_tertile', 'TSVR_hours', 'theta_observed',
                     'se_observed', 'ci_lower', 'ci_upper', 'theta_predicted']
    for col in required_cols:
        assert col in result.columns, f"Missing required column: {col}"


def test_age_tertiles_created(mock_lmm_input, mock_lmm_model, tmp_path):
    """Test age tertiles are created (Young, Middle, Older)"""
    output_path = tmp_path / "age_effects_plot_data.csv"
    result = prepare_age_effects_plot_data(
        lmm_input=mock_lmm_input,
        lmm_model=mock_lmm_model,
        output_path=output_path
    )

    # Check tertiles exist
    assert 'age_tertile' in result.columns
    tertiles = result['age_tertile'].unique()
    assert len(tertiles) == 3
    # Check labels (order doesn't matter)
    assert set(tertiles) == {'Young', 'Middle', 'Older'}


def test_tertiles_approximately_equal_size(mock_lmm_input, mock_lmm_model, tmp_path):
    """Test tertiles have approximately equal counts (qcut behavior)"""
    output_path = tmp_path / "age_effects_plot_data.csv"
    result = prepare_age_effects_plot_data(
        lmm_input=mock_lmm_input,
        lmm_model=mock_lmm_model,
        output_path=output_path
    )

    # Get original data with tertiles
    input_with_tertiles = mock_lmm_input.copy()
    input_with_tertiles['age_tertile'] = pd.qcut(
        input_with_tertiles['Age'],
        q=3,
        labels=['Young', 'Middle', 'Older']
    )

    # Count unique subjects per tertile (should be ~20 each for n=60)
    counts = input_with_tertiles.groupby('age_tertile')['UID'].nunique()
    assert all(counts >= 15), "Tertiles too imbalanced"
    assert all(counts <= 25), "Tertiles too imbalanced"


def test_aggregation_by_domain_tertile_time(mock_lmm_input, mock_lmm_model, tmp_path):
    """Test data is aggregated by domain × tertile × timepoint"""
    output_path = tmp_path / "age_effects_plot_data.csv"
    result = prepare_age_effects_plot_data(
        lmm_input=mock_lmm_input,
        lmm_model=mock_lmm_model,
        output_path=output_path
    )

    # Expected: 3 domains × 3 tertiles × 4 timepoints = 36 rows
    assert len(result) == 36, f"Expected 36 rows, got {len(result)}"

    # Check unique combinations
    domains = result['domain_name'].unique()
    assert len(domains) == 3

    tertiles = result['age_tertile'].unique()
    assert len(tertiles) == 3

    timepoints = result['TSVR_hours'].unique()
    assert len(timepoints) == 4


def test_observed_means_computed(mock_lmm_input, mock_lmm_model, tmp_path):
    """Test observed theta means are computed per group"""
    output_path = tmp_path / "age_effects_plot_data.csv"
    result = prepare_age_effects_plot_data(
        lmm_input=mock_lmm_input,
        lmm_model=mock_lmm_model,
        output_path=output_path
    )

    # Check theta_observed is numeric
    assert pd.api.types.is_numeric_dtype(result['theta_observed'])
    # No NaN values
    assert result['theta_observed'].notna().all()
    # Reasonable range (mean of standard normals)
    assert result['theta_observed'].between(-2, 2).all()


def test_standard_error_computed(mock_lmm_input, mock_lmm_model, tmp_path):
    """Test standard error (SEM) is computed"""
    output_path = tmp_path / "age_effects_plot_data.csv"
    result = prepare_age_effects_plot_data(
        lmm_input=mock_lmm_input,
        lmm_model=mock_lmm_model,
        output_path=output_path
    )

    # Check se_observed is numeric and positive
    assert pd.api.types.is_numeric_dtype(result['se_observed'])
    assert (result['se_observed'] > 0).all()
    assert result['se_observed'].notna().all()


def test_confidence_intervals_computed(mock_lmm_input, mock_lmm_model, tmp_path):
    """Test 95% CIs are computed (mean ± 1.96*SEM)"""
    output_path = tmp_path / "age_effects_plot_data.csv"
    result = prepare_age_effects_plot_data(
        lmm_input=mock_lmm_input,
        lmm_model=mock_lmm_model,
        output_path=output_path
    )

    # CI columns exist and numeric
    assert 'ci_lower' in result.columns
    assert 'ci_upper' in result.columns
    assert pd.api.types.is_numeric_dtype(result['ci_lower'])
    assert pd.api.types.is_numeric_dtype(result['ci_upper'])

    # CI should bracket the mean: ci_lower < theta_observed < ci_upper
    assert (result['ci_lower'] < result['theta_observed']).all()
    assert (result['theta_observed'] < result['ci_upper']).all()

    # Check CI width approximately equals 2*1.96*SEM
    ci_width = result['ci_upper'] - result['ci_lower']
    expected_width = 2 * 1.96 * result['se_observed']
    np.testing.assert_allclose(ci_width, expected_width, rtol=0.01)


def test_predictions_generated(mock_lmm_input, mock_lmm_model, tmp_path):
    """Test model predictions are generated"""
    output_path = tmp_path / "age_effects_plot_data.csv"
    result = prepare_age_effects_plot_data(
        lmm_input=mock_lmm_input,
        lmm_model=mock_lmm_model,
        output_path=output_path
    )

    # Check theta_predicted exists and is numeric
    assert 'theta_predicted' in result.columns
    assert pd.api.types.is_numeric_dtype(result['theta_predicted'])
    assert result['theta_predicted'].notna().all()


def test_predictions_reasonable_range(mock_lmm_input, mock_lmm_model, tmp_path):
    """Test predictions are in reasonable range"""
    output_path = tmp_path / "age_effects_plot_data.csv"
    result = prepare_age_effects_plot_data(
        lmm_input=mock_lmm_input,
        lmm_model=mock_lmm_model,
        output_path=output_path
    )

    # Predictions should be in reasonable theta range
    assert result['theta_predicted'].between(-3, 3).all()


def test_csv_saved_to_output_path(mock_lmm_input, mock_lmm_model, tmp_path):
    """Test CSV file is saved to output_path"""
    output_path = tmp_path / "age_effects_plot_data.csv"
    result = prepare_age_effects_plot_data(
        lmm_input=mock_lmm_input,
        lmm_model=mock_lmm_model,
        output_path=output_path
    )

    # File should exist
    assert output_path.exists()

    # File should be readable as CSV
    loaded = pd.read_csv(output_path)
    assert len(loaded) == len(result)
    assert set(loaded.columns) == set(result.columns)


def test_output_path_parent_creation(mock_lmm_input, mock_lmm_model, tmp_path):
    """Test parent directories are created if needed"""
    output_path = tmp_path / "subdir" / "nested" / "age_effects_plot_data.csv"
    result = prepare_age_effects_plot_data(
        lmm_input=mock_lmm_input,
        lmm_model=mock_lmm_model,
        output_path=output_path
    )

    # File and parents should exist
    assert output_path.exists()
    assert output_path.parent.exists()


def test_handles_missing_age_tertile_column(mock_lmm_input, mock_lmm_model, tmp_path):
    """Test function creates age_tertile if not present in input"""
    # Ensure input doesn't have age_tertile
    assert 'age_tertile' not in mock_lmm_input.columns

    output_path = tmp_path / "age_effects_plot_data.csv"
    result = prepare_age_effects_plot_data(
        lmm_input=mock_lmm_input,
        lmm_model=mock_lmm_model,
        output_path=output_path
    )

    # Result should have age_tertile
    assert 'age_tertile' in result.columns


def test_preserves_domain_order(mock_lmm_input, mock_lmm_model, tmp_path):
    """Test domain order is preserved (What, Where, When)"""
    output_path = tmp_path / "age_effects_plot_data.csv"
    result = prepare_age_effects_plot_data(
        lmm_input=mock_lmm_input,
        lmm_model=mock_lmm_model,
        output_path=output_path
    )

    # Check all three domains present
    domains = result['domain_name'].unique()
    assert len(domains) == 3
    assert set(domains) == {'What', 'Where', 'When'}


def test_row_count_matches_expectation(mock_lmm_input, mock_lmm_model, tmp_path):
    """Test output has expected number of rows (3 × 3 × 4 = 36)"""
    output_path = tmp_path / "age_effects_plot_data.csv"
    result = prepare_age_effects_plot_data(
        lmm_input=mock_lmm_input,
        lmm_model=mock_lmm_model,
        output_path=output_path
    )

    # 3 domains × 3 age tertiles × 4 timepoints = 36 rows
    assert len(result) == 36


def test_all_groups_have_data(mock_lmm_input, mock_lmm_model, tmp_path):
    """Test all domain × tertile × timepoint combinations have data"""
    output_path = tmp_path / "age_effects_plot_data.csv"
    result = prepare_age_effects_plot_data(
        lmm_input=mock_lmm_input,
        lmm_model=mock_lmm_model,
        output_path=output_path
    )

    # Check for complete factorial design
    grouped = result.groupby(['domain_name', 'age_tertile', 'TSVR_hours']).size()
    # Each combination should have exactly 1 row
    assert (grouped == 1).all()
    # Total combinations: 3 × 3 × 4 = 36
    assert len(grouped) == 36
