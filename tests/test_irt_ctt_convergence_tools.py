"""
Tests for IRT-CTT Convergence Tools.

TDD Red-Green-Refactor approach:
1. Write tests FIRST (Red - tests fail)
2. Implement functions (Green - tests pass)
3. Refactor if needed

These tools support RQ 5.2.4 (Domains), 5.3.5 (Paradigms), 5.4.4 (Congruence)
IRT-CTT convergence analyses.

Functions tested:
- compute_ctt_mean_scores_by_factor: CTT score computation by any factor
- compute_pearson_correlations_with_correction: Correlations with Holm-Bonferroni
- compute_cohens_kappa_agreement: Cohen's kappa for significance classification
- compare_lmm_fit_aic_bic: AIC/BIC model comparison
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from tools.analysis_ctt import (
    compute_ctt_mean_scores_by_factor,
    compute_pearson_correlations_with_correction,
    compute_cohens_kappa_agreement,
    compare_lmm_fit_aic_bic,
)


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def sample_raw_responses():
    """
    Create sample raw binary response data (wide format).
    Simulates 20 participants x 4 tests x 12 items (4 per factor).
    """
    np.random.seed(42)
    n_participants = 20
    n_tests = 4

    rows = []
    for uid in range(1, n_participants + 1):
        for test in range(1, n_tests + 1):
            row = {
                'UID': f'P{uid:03d}',
                'TEST': f'T{test}',
                'composite_ID': f'P{uid:03d}_T{test}',
            }
            # Factor A items (higher accuracy)
            for i in range(1, 5):
                row[f'item_A_{i}'] = np.random.binomial(1, 0.8)
            # Factor B items (medium accuracy)
            for i in range(1, 5):
                row[f'item_B_{i}'] = np.random.binomial(1, 0.6)
            # Factor C items (lower accuracy)
            for i in range(1, 5):
                row[f'item_C_{i}'] = np.random.binomial(1, 0.4)
            rows.append(row)

    return pd.DataFrame(rows)


@pytest.fixture
def sample_item_factor_mapping():
    """
    Create item-to-factor mapping.
    """
    items = []
    for factor in ['A', 'B', 'C']:
        for i in range(1, 5):
            items.append({
                'item_name': f'item_{factor}_{i}',
                'factor': factor
            })
    return pd.DataFrame(items)


@pytest.fixture
def sample_irt_ctt_scores():
    """
    Create sample IRT theta and CTT scores for correlation testing.
    """
    np.random.seed(42)
    n_obs = 80  # 20 participants x 4 tests

    # Create correlated IRT and CTT scores (r ~ 0.85)
    irt_scores = np.random.normal(0, 1, n_obs)
    ctt_scores = 0.85 * irt_scores + 0.53 * np.random.normal(0, 1, n_obs)
    ctt_scores = (ctt_scores - ctt_scores.min()) / (ctt_scores.max() - ctt_scores.min())

    return pd.DataFrame({
        'composite_ID': [f'P{(i//4)+1:03d}_T{(i%4)+1}' for i in range(n_obs)],
        'factor': ['A'] * 40 + ['B'] * 40,  # Two factors
        'IRT_score': np.concatenate([irt_scores[:40], irt_scores[:40] + np.random.normal(0, 0.2, 40)]),
        'CTT_score': np.concatenate([ctt_scores[:40], ctt_scores[:40] + np.random.normal(0, 0.05, 40)])
    })


@pytest.fixture
def sample_significance_classifications():
    """
    Create sample significance classifications for kappa testing.
    """
    # IRT model: 8 effects, 5 significant
    irt_sig = [True, True, True, False, True, False, True, False]
    # CTT model: 8 effects, 5 significant (6 agreements)
    ctt_sig = [True, True, False, False, True, True, True, False]

    return {
        'IRT_significant': irt_sig,
        'CTT_significant': ctt_sig,
        'effect_names': ['Intercept', 'Time', 'Factor_B', 'Factor_C',
                        'Time:Factor_B', 'Time:Factor_C', 'log_Time', 'log_Time:Factor_B']
    }


# =============================================================================
# Tests for compute_ctt_mean_scores_by_factor
# =============================================================================

class TestComputeCttMeanScoresByFactor:
    """Tests for CTT mean score computation."""

    def test_basic_computation(self, sample_raw_responses, sample_item_factor_mapping):
        """Test basic CTT score computation returns expected structure."""
        result = compute_ctt_mean_scores_by_factor(
            df_wide=sample_raw_responses,
            item_factor_df=sample_item_factor_mapping,
            factor_col='factor',
            item_col='item_name'
        )

        # Check output structure
        assert isinstance(result, pd.DataFrame)
        assert 'composite_ID' in result.columns
        assert 'UID' in result.columns
        assert 'test' in result.columns
        assert 'factor' in result.columns
        assert 'CTT_score' in result.columns
        assert 'n_items' in result.columns

    def test_correct_row_count(self, sample_raw_responses, sample_item_factor_mapping):
        """Test output has correct number of rows (N_obs × N_factors)."""
        result = compute_ctt_mean_scores_by_factor(
            df_wide=sample_raw_responses,
            item_factor_df=sample_item_factor_mapping,
            factor_col='factor',
            item_col='item_name'
        )

        # 20 participants x 4 tests x 3 factors = 240 rows
        expected_rows = 20 * 4 * 3
        assert len(result) == expected_rows

    def test_score_range(self, sample_raw_responses, sample_item_factor_mapping):
        """Test CTT scores are in [0, 1] range (proportion correct)."""
        result = compute_ctt_mean_scores_by_factor(
            df_wide=sample_raw_responses,
            item_factor_df=sample_item_factor_mapping,
            factor_col='factor',
            item_col='item_name'
        )

        assert result['CTT_score'].min() >= 0.0
        assert result['CTT_score'].max() <= 1.0

    def test_item_count_per_factor(self, sample_raw_responses, sample_item_factor_mapping):
        """Test n_items reflects correct item count per factor."""
        result = compute_ctt_mean_scores_by_factor(
            df_wide=sample_raw_responses,
            item_factor_df=sample_item_factor_mapping,
            factor_col='factor',
            item_col='item_name'
        )

        # All factors have 4 items
        assert (result['n_items'] == 4).all()

    def test_factor_filter(self, sample_raw_responses, sample_item_factor_mapping):
        """Test optional factor filtering (include only subset)."""
        result = compute_ctt_mean_scores_by_factor(
            df_wide=sample_raw_responses,
            item_factor_df=sample_item_factor_mapping,
            factor_col='factor',
            item_col='item_name',
            include_factors=['A', 'B']  # Exclude C
        )

        # 20 participants x 4 tests x 2 factors = 160 rows
        assert len(result) == 160
        assert set(result['factor'].unique()) == {'A', 'B'}

    def test_missing_items_handled(self, sample_raw_responses, sample_item_factor_mapping):
        """Test graceful handling when some items missing from data."""
        # Add a phantom item to mapping that doesn't exist in data
        extra_item = pd.DataFrame([{'item_name': 'phantom_item', 'factor': 'A'}])
        extended_mapping = pd.concat([sample_item_factor_mapping, extra_item], ignore_index=True)

        # Should not raise, should use available items
        result = compute_ctt_mean_scores_by_factor(
            df_wide=sample_raw_responses,
            item_factor_df=extended_mapping,
            factor_col='factor',
            item_col='item_name'
        )

        assert len(result) > 0

    def test_raises_on_empty_data(self, sample_item_factor_mapping):
        """Test raises ValueError on empty input data."""
        empty_df = pd.DataFrame()

        with pytest.raises(ValueError, match="empty"):
            compute_ctt_mean_scores_by_factor(
                df_wide=empty_df,
                item_factor_df=sample_item_factor_mapping,
                factor_col='factor',
                item_col='item_name'
            )


# =============================================================================
# Tests for compute_pearson_correlations_with_correction
# =============================================================================

class TestComputePearsonCorrelationsWithCorrection:
    """Tests for Pearson correlations with multiple testing correction."""

    def test_basic_computation(self, sample_irt_ctt_scores):
        """Test basic correlation computation returns expected structure."""
        result = compute_pearson_correlations_with_correction(
            df=sample_irt_ctt_scores,
            irt_col='IRT_score',
            ctt_col='CTT_score',
            factor_col='factor'
        )

        # Check output structure
        assert isinstance(result, pd.DataFrame)
        assert 'factor' in result.columns
        assert 'r' in result.columns
        assert 'p_uncorrected' in result.columns
        assert 'p_holm' in result.columns
        assert 'CI_lower' in result.columns
        assert 'CI_upper' in result.columns
        assert 'n' in result.columns

    def test_includes_overall_correlation(self, sample_irt_ctt_scores):
        """Test output includes overall correlation (all factors pooled)."""
        result = compute_pearson_correlations_with_correction(
            df=sample_irt_ctt_scores,
            irt_col='IRT_score',
            ctt_col='CTT_score',
            factor_col='factor'
        )

        assert 'Overall' in result['factor'].values

    def test_d068_dual_pvalues(self, sample_irt_ctt_scores):
        """Test D068 compliance: both p_uncorrected and p_holm present."""
        result = compute_pearson_correlations_with_correction(
            df=sample_irt_ctt_scores,
            irt_col='IRT_score',
            ctt_col='CTT_score',
            factor_col='factor'
        )

        # Both p-value columns must exist and be numeric
        assert 'p_uncorrected' in result.columns
        assert 'p_holm' in result.columns
        assert result['p_uncorrected'].notna().all()
        assert result['p_holm'].notna().all()

    def test_holm_correction_valid(self, sample_irt_ctt_scores):
        """Test Holm-Bonferroni correction is valid (p_holm >= p_uncorrected)."""
        result = compute_pearson_correlations_with_correction(
            df=sample_irt_ctt_scores,
            irt_col='IRT_score',
            ctt_col='CTT_score',
            factor_col='factor'
        )

        # Corrected p-values cannot be smaller than uncorrected
        assert (result['p_holm'] >= result['p_uncorrected']).all()

    def test_correlation_bounds(self, sample_irt_ctt_scores):
        """Test correlations are in [-1, 1] range."""
        result = compute_pearson_correlations_with_correction(
            df=sample_irt_ctt_scores,
            irt_col='IRT_score',
            ctt_col='CTT_score',
            factor_col='factor'
        )

        assert (result['r'] >= -1.0).all()
        assert (result['r'] <= 1.0).all()

    def test_ci_brackets_point_estimate(self, sample_irt_ctt_scores):
        """Test CI bounds bracket the point estimate (CI_lower < r < CI_upper)."""
        result = compute_pearson_correlations_with_correction(
            df=sample_irt_ctt_scores,
            irt_col='IRT_score',
            ctt_col='CTT_score',
            factor_col='factor'
        )

        assert (result['CI_lower'] < result['r']).all()
        assert (result['r'] < result['CI_upper']).all()

    def test_threshold_columns(self, sample_irt_ctt_scores):
        """Test threshold classification columns present."""
        result = compute_pearson_correlations_with_correction(
            df=sample_irt_ctt_scores,
            irt_col='IRT_score',
            ctt_col='CTT_score',
            factor_col='factor',
            thresholds=[0.70, 0.90]
        )

        assert 'threshold_0.70' in result.columns
        assert 'threshold_0.90' in result.columns


# =============================================================================
# Tests for compute_cohens_kappa_agreement
# =============================================================================

class TestComputeCohensKappaAgreement:
    """Tests for Cohen's kappa agreement metric."""

    def test_basic_computation(self, sample_significance_classifications):
        """Test basic kappa computation returns expected structure."""
        result = compute_cohens_kappa_agreement(
            classifications_1=sample_significance_classifications['IRT_significant'],
            classifications_2=sample_significance_classifications['CTT_significant'],
            labels=sample_significance_classifications['effect_names']
        )

        # Check output structure
        assert isinstance(result, dict)
        assert 'kappa' in result
        assert 'agreement_percent' in result
        assert 'interpretation' in result
        assert 'n_effects' in result

    def test_kappa_bounds(self, sample_significance_classifications):
        """Test kappa is in [-1, 1] range."""
        result = compute_cohens_kappa_agreement(
            classifications_1=sample_significance_classifications['IRT_significant'],
            classifications_2=sample_significance_classifications['CTT_significant']
        )

        assert result['kappa'] >= -1.0
        assert result['kappa'] <= 1.0

    def test_perfect_agreement(self):
        """Test kappa = 1.0 for perfect agreement."""
        same = [True, True, False, False, True]

        result = compute_cohens_kappa_agreement(
            classifications_1=same,
            classifications_2=same
        )

        assert result['kappa'] == pytest.approx(1.0, abs=0.01)
        assert result['agreement_percent'] == 100.0

    def test_agreement_percentage_correct(self, sample_significance_classifications):
        """Test agreement percentage is calculated correctly."""
        result = compute_cohens_kappa_agreement(
            classifications_1=sample_significance_classifications['IRT_significant'],
            classifications_2=sample_significance_classifications['CTT_significant']
        )

        # Manual calculation: 6 agreements out of 8
        expected_agreement = 6 / 8 * 100
        assert result['agreement_percent'] == pytest.approx(expected_agreement, abs=0.1)

    def test_interpretation_thresholds(self):
        """Test interpretation follows Landis & Koch (1977) guidelines."""
        # Perfect agreement
        result = compute_cohens_kappa_agreement([True, True], [True, True])
        assert 'perfect' in result['interpretation'].lower() or 'almost' in result['interpretation'].lower()

    def test_substantial_agreement_threshold(self, sample_significance_classifications):
        """Test substantial agreement detection (kappa > 0.60)."""
        result = compute_cohens_kappa_agreement(
            classifications_1=sample_significance_classifications['IRT_significant'],
            classifications_2=sample_significance_classifications['CTT_significant']
        )

        # Check if meets substantial threshold
        assert 'substantial_agreement' in result
        assert isinstance(result['substantial_agreement'], bool)


# =============================================================================
# Tests for compare_lmm_fit_aic_bic
# =============================================================================

class TestCompareLmmFitAicBic:
    """Tests for AIC/BIC model comparison."""

    def test_basic_computation(self):
        """Test basic AIC/BIC comparison returns expected structure."""
        result = compare_lmm_fit_aic_bic(
            aic_model1=1500.0,
            bic_model1=1520.0,
            aic_model2=1510.0,
            bic_model2=1530.0,
            model1_name='IRT',
            model2_name='CTT'
        )

        # Check output structure
        assert isinstance(result, pd.DataFrame)
        assert 'metric' in result.columns
        assert 'IRT' in result.columns
        assert 'CTT' in result.columns
        assert 'delta' in result.columns
        assert 'interpretation' in result.columns

    def test_delta_computation(self):
        """Test delta is computed correctly (model2 - model1)."""
        result = compare_lmm_fit_aic_bic(
            aic_model1=1500.0,
            bic_model1=1520.0,
            aic_model2=1510.0,
            bic_model2=1530.0,
            model1_name='IRT',
            model2_name='CTT'
        )

        aic_row = result[result['metric'] == 'AIC'].iloc[0]
        assert aic_row['delta'] == pytest.approx(10.0, abs=0.01)

    def test_interpretation_equivalent(self):
        """Test interpretation for equivalent models (|delta| < 2)."""
        result = compare_lmm_fit_aic_bic(
            aic_model1=1500.0,
            bic_model1=1520.0,
            aic_model2=1501.0,  # Delta = 1
            bic_model2=1521.0,
            model1_name='IRT',
            model2_name='CTT'
        )

        aic_row = result[result['metric'] == 'AIC'].iloc[0]
        assert 'equivalent' in aic_row['interpretation'].lower()

    def test_interpretation_moderate(self):
        """Test interpretation for moderate difference (2 <= |delta| < 10)."""
        result = compare_lmm_fit_aic_bic(
            aic_model1=1500.0,
            bic_model1=1520.0,
            aic_model2=1505.0,  # Delta = 5
            bic_model2=1525.0,
            model1_name='IRT',
            model2_name='CTT'
        )

        aic_row = result[result['metric'] == 'AIC'].iloc[0]
        assert 'moderate' in aic_row['interpretation'].lower() or 'weak' in aic_row['interpretation'].lower()

    def test_interpretation_strong(self):
        """Test interpretation for strong difference (|delta| >= 10)."""
        result = compare_lmm_fit_aic_bic(
            aic_model1=1500.0,
            bic_model1=1520.0,
            aic_model2=1520.0,  # Delta = 20
            bic_model2=1540.0,
            model1_name='IRT',
            model2_name='CTT'
        )

        aic_row = result[result['metric'] == 'AIC'].iloc[0]
        assert 'strong' in aic_row['interpretation'].lower() or 'substantial' in aic_row['interpretation'].lower()

    def test_negative_delta_interpretation(self):
        """Test correct interpretation when model2 has lower AIC (negative delta)."""
        result = compare_lmm_fit_aic_bic(
            aic_model1=1520.0,  # Higher
            bic_model1=1540.0,
            aic_model2=1500.0,  # Lower (better)
            bic_model2=1520.0,
            model1_name='IRT',
            model2_name='CTT'
        )

        aic_row = result[result['metric'] == 'AIC'].iloc[0]
        # Delta should be negative (CTT - IRT = -20)
        assert aic_row['delta'] == pytest.approx(-20.0, abs=0.01)


# =============================================================================
# Integration Tests
# =============================================================================

class TestIntegration:
    """Integration tests for the full IRT-CTT convergence workflow."""

    def test_full_workflow(self, sample_raw_responses, sample_item_factor_mapping):
        """Test full workflow from raw data to correlations."""
        # Step 1: Compute CTT scores
        ctt_scores = compute_ctt_mean_scores_by_factor(
            df_wide=sample_raw_responses,
            item_factor_df=sample_item_factor_mapping,
            factor_col='factor',
            item_col='item_name'
        )

        # Create mock IRT scores (in real use, these come from IRT calibration)
        np.random.seed(42)
        irt_scores = ctt_scores.copy()
        irt_scores['IRT_score'] = irt_scores['CTT_score'] * 2 - 1 + np.random.normal(0, 0.1, len(irt_scores))

        # Step 2: Compute correlations
        correlations = compute_pearson_correlations_with_correction(
            df=irt_scores,
            irt_col='IRT_score',
            ctt_col='CTT_score',
            factor_col='factor'
        )

        # Verify workflow produced valid output
        assert len(correlations) == 4  # 3 factors + Overall
        assert correlations['r'].notna().all()
        assert (correlations['p_holm'] >= correlations['p_uncorrected']).all()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
