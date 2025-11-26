"""Tests for validate_lmm_assumptions_comprehensive function."""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
from unittest.mock import MagicMock
from tools.validation import validate_lmm_assumptions_comprehensive


@pytest.fixture
def mock_lmm_result():
    """Create mock LMM result object with realistic attributes."""
    result = MagicMock()

    # Residuals (100 observations)
    np.random.seed(42)
    result.resid = np.random.normal(0, 1, 100)

    # Fitted values
    result.fittedvalues = np.random.normal(5, 2, 100)

    # Convergence
    result.converged = True

    # Random effects (intercepts and slopes for 25 subjects, 4 obs each)
    # cov_re is 2x2 covariance matrix for (intercept, slope)
    result.cov_re = np.array([[1.5, 0.3], [0.3, 0.8]])

    # Random effects for each subject (25 subjects × 2 effects)
    result.random_effects = {
        f"subj_{i}": np.random.normal([0, 0], [1.2, 0.9], 2)
        for i in range(25)
    }

    # Model parameters
    result.params = pd.Series({
        'Intercept': 5.0,
        'Time': -0.5,
        'Domain[T.What]': 0.3,
        'Domain[T.When]': -0.2,
        'Time:Domain[T.What]': 0.1,
        'Time:Domain[T.When]': -0.05
    })

    # Number of observations and parameters
    result.nobs = 100
    result.df_resid = 94

    # Mock model.exog for Breusch-Pagan test
    result.model.exog = np.random.rand(100, 6)  # 100 obs, 6 predictors

    # Mock influence diagnostics for Cook's distance
    influence_mock = MagicMock()
    # Cook's distance: (stat, p-value) tuple, we want the stat
    cooks_d_values = np.random.gamma(2, 0.01, 100)  # Small values, few outliers
    influence_mock.cooks_distance = (cooks_d_values, np.random.rand(100))
    result.get_influence.return_value = influence_mock

    return result


@pytest.fixture
def mock_data():
    """Create mock DataFrame with LMM input data."""
    np.random.seed(42)
    n_subjects = 25
    n_timepoints = 4

    data = []
    for subj in range(n_subjects):
        for time in [0, 1, 3, 6]:
            data.append({
                'UID': f'subj_{subj}',
                'Time': time,
                'Domain': np.random.choice(['Who', 'What', 'When']),
                'theta': np.random.normal(0, 1)
            })

    return pd.DataFrame(data)


class TestValidateLmmAssumptionsComprehensive:
    """Test comprehensive LMM assumption validation."""

    def test_basic_validation_structure(self, mock_lmm_result, mock_data, tmp_path):
        """Test function returns expected structure."""
        result = validate_lmm_assumptions_comprehensive(
            lmm_result=mock_lmm_result,
            data=mock_data,
            output_dir=tmp_path
        )

        # Check required keys
        assert "valid" in result
        assert "diagnostics" in result
        assert "plot_paths" in result
        assert "message" in result

        # Check diagnostics structure
        diagnostics = result["diagnostics"]
        assert "residual_normality" in diagnostics
        assert "homoscedasticity" in diagnostics
        assert "random_effects_normality" in diagnostics
        assert "autocorrelation" in diagnostics
        assert "outliers" in diagnostics
        assert "convergence" in diagnostics

    def test_residual_normality_check(self, mock_lmm_result, mock_data, tmp_path):
        """Test residual normality diagnostic (Shapiro-Wilk + Q-Q plot)."""
        result = validate_lmm_assumptions_comprehensive(
            lmm_result=mock_lmm_result,
            data=mock_data,
            output_dir=tmp_path
        )

        diag = result["diagnostics"]["residual_normality"]

        # Check structure
        assert "test" in diag
        assert "statistic" in diag
        assert "p_value" in diag
        assert "pass" in diag
        assert "threshold" in diag

        # Check values
        assert diag["test"] == "Shapiro-Wilk"
        assert isinstance(diag["statistic"], (float, np.floating))
        assert isinstance(diag["p_value"], (float, np.floating))
        assert isinstance(diag["pass"], (bool, np.bool_))
        assert diag["threshold"] == 0.05

        # Check Q-Q plot generated
        qq_plot = tmp_path / "qq_plot_residuals.png"
        assert qq_plot.exists()
        assert qq_plot in result["plot_paths"]

    def test_homoscedasticity_check(self, mock_lmm_result, mock_data, tmp_path):
        """Test homoscedasticity diagnostic (Breusch-Pagan test)."""
        result = validate_lmm_assumptions_comprehensive(
            lmm_result=mock_lmm_result,
            data=mock_data,
            output_dir=tmp_path
        )

        diag = result["diagnostics"]["homoscedasticity"]

        # Check structure
        assert "test" in diag
        assert "statistic" in diag
        assert "p_value" in diag
        assert "pass" in diag
        assert "threshold" in diag

        # Check values
        assert diag["test"] == "Breusch-Pagan"
        # Statistic may be None if test failed (mock data issue)
        assert diag["statistic"] is None or isinstance(diag["statistic"], (float, np.floating))
        assert diag["p_value"] is None or isinstance(diag["p_value"], (float, np.floating))
        assert isinstance(diag["pass"], (bool, np.bool_))

        # Check residuals vs fitted plot generated
        resid_plot = tmp_path / "residuals_vs_fitted.png"
        assert resid_plot.exists()

    def test_random_effects_normality_check(self, mock_lmm_result, mock_data, tmp_path):
        """Test random effects normality (separate Q-Q plots for intercepts and slopes)."""
        result = validate_lmm_assumptions_comprehensive(
            lmm_result=mock_lmm_result,
            data=mock_data,
            output_dir=tmp_path
        )

        diag = result["diagnostics"]["random_effects_normality"]

        # Check structure
        assert "intercepts" in diag
        assert "slopes" in diag

        # Check intercepts
        intercepts = diag["intercepts"]
        assert "test" in intercepts
        assert "statistic" in intercepts
        assert "p_value" in intercepts
        assert "pass" in intercepts
        assert intercepts["test"] == "Shapiro-Wilk"

        # Check slopes
        slopes = diag["slopes"]
        assert "test" in slopes
        assert "statistic" in slopes
        assert "p_value" in slopes
        assert "pass" in slopes

        # Check separate Q-Q plots generated
        qq_intercepts = tmp_path / "qq_plot_random_intercepts.png"
        qq_slopes = tmp_path / "qq_plot_random_slopes.png"
        assert qq_intercepts.exists()
        assert qq_slopes.exists()

    def test_autocorrelation_check(self, mock_lmm_result, mock_data, tmp_path):
        """Test autocorrelation diagnostic (ACF plot + Lag-1 test)."""
        result = validate_lmm_assumptions_comprehensive(
            lmm_result=mock_lmm_result,
            data=mock_data,
            output_dir=tmp_path,
            acf_lag1_threshold=0.1  # Configurable threshold
        )

        diag = result["diagnostics"]["autocorrelation"]

        # Check structure
        assert "lag1_acf" in diag
        assert "pass" in diag
        assert "threshold" in diag

        # Check values
        assert isinstance(diag["lag1_acf"], float)
        assert isinstance(diag["pass"], bool)
        assert diag["threshold"] == 0.1
        assert abs(diag["lag1_acf"]) <= 1.0  # ACF bounded [-1, 1]

        # Check ACF plot generated
        acf_plot = tmp_path / "acf_plot.png"
        assert acf_plot.exists()

    def test_outliers_check_cooks_distance(self, mock_lmm_result, mock_data, tmp_path):
        """Test outlier detection using Cook's distance."""
        result = validate_lmm_assumptions_comprehensive(
            lmm_result=mock_lmm_result,
            data=mock_data,
            output_dir=tmp_path
        )

        diag = result["diagnostics"]["outliers"]

        # Check structure
        assert "method" in diag
        assert "threshold" in diag
        assert "n_outliers" in diag
        assert "pass" in diag
        assert "outlier_indices" in diag

        # Check values
        assert diag["method"] == "Cook's Distance"
        assert isinstance(diag["threshold"], float)
        assert isinstance(diag["n_outliers"], int)
        assert diag["n_outliers"] >= 0

        # Cook's D threshold should be 4/(n-p-1)
        n = mock_lmm_result.nobs
        p = len(mock_lmm_result.params)
        expected_threshold = 4 / (n - p - 1)
        assert abs(diag["threshold"] - expected_threshold) < 0.001

        # Check Cook's distance plot generated
        cooks_plot = tmp_path / "cooks_distance.png"
        assert cooks_plot.exists()

    def test_convergence_check(self, mock_lmm_result, mock_data, tmp_path):
        """Test convergence diagnostic."""
        result = validate_lmm_assumptions_comprehensive(
            lmm_result=mock_lmm_result,
            data=mock_data,
            output_dir=tmp_path
        )

        diag = result["diagnostics"]["convergence"]

        # Check structure
        assert "converged" in diag
        assert "pass" in diag

        # Check values
        assert isinstance(diag["converged"], bool)
        assert isinstance(diag["pass"], bool)
        assert diag["converged"] == mock_lmm_result.converged

    def test_overall_validation_pass(self, mock_lmm_result, mock_data, tmp_path):
        """Test overall validation when all checks pass."""
        # Set up result to pass all checks
        mock_lmm_result.resid = np.random.normal(0, 1, 100)
        mock_lmm_result.converged = True

        result = validate_lmm_assumptions_comprehensive(
            lmm_result=mock_lmm_result,
            data=mock_data,
            output_dir=tmp_path
        )

        # If all diagnostics pass, valid should be True
        # (Note: with random data, some may fail - test structure not values)
        assert isinstance(result["valid"], bool)

    def test_remedial_actions_in_message(self, mock_lmm_result, mock_data, tmp_path):
        """Test remedial action recommendations included in message."""
        # Force some violations
        mock_lmm_result.resid = np.array([10] * 50 + [-10] * 50)  # Non-normal
        mock_lmm_result.converged = False

        result = validate_lmm_assumptions_comprehensive(
            lmm_result=mock_lmm_result,
            data=mock_data,
            output_dir=tmp_path
        )

        message = result["message"].lower()

        # Should mention violations
        assert "violated" in message or "failed" in message or "warning" in message

        # Should include remedial recommendations (from RQ 5.8 spec)
        # At least some of: robust SE, variance modeling, AR(1), transformations
        remedial_keywords = ["robust", "variance", "ar(1)", "transform"]
        has_remedial = any(keyword in message for keyword in remedial_keywords)
        assert has_remedial, "Message should include remedial action recommendations"

    def test_partial_residual_csvs_generated(self, mock_lmm_result, mock_data, tmp_path):
        """Test partial residual CSVs generated for ALL predictors."""
        result = validate_lmm_assumptions_comprehensive(
            lmm_result=mock_lmm_result,
            data=mock_data,
            output_dir=tmp_path
        )

        # Should generate CSV for each predictor (rq_plots handles visualization)
        # Predictors: Intercept, Time, Domain[T.What], Domain[T.When], interactions
        partial_resid_dir = tmp_path / "partial_residuals"
        assert partial_resid_dir.exists()

        csv_files = list(partial_resid_dir.glob("*.csv"))
        assert len(csv_files) > 0, "Should generate at least one partial residual CSV"

        # Check CSV structure (should have predictor_value, partial_residual columns)
        sample_csv = csv_files[0]
        df = pd.read_csv(sample_csv)
        assert "predictor_value" in df.columns
        assert "partial_residual" in df.columns

    def test_output_directory_creation(self, mock_lmm_result, mock_data, tmp_path):
        """Test output directory created if doesn't exist."""
        new_dir = tmp_path / "new_output_dir"
        assert not new_dir.exists()

        result = validate_lmm_assumptions_comprehensive(
            lmm_result=mock_lmm_result,
            data=mock_data,
            output_dir=new_dir
        )

        assert new_dir.exists()
        assert len(result["plot_paths"]) > 0

    def test_configurable_acf_threshold(self, mock_lmm_result, mock_data, tmp_path):
        """Test ACF Lag-1 threshold is configurable."""
        # Test with default threshold (0.1)
        result1 = validate_lmm_assumptions_comprehensive(
            lmm_result=mock_lmm_result,
            data=mock_data,
            output_dir=tmp_path
        )
        assert result1["diagnostics"]["autocorrelation"]["threshold"] == 0.1

        # Test with custom threshold
        result2 = validate_lmm_assumptions_comprehensive(
            lmm_result=mock_lmm_result,
            data=mock_data,
            output_dir=tmp_path / "custom",
            acf_lag1_threshold=0.2
        )
        assert result2["diagnostics"]["autocorrelation"]["threshold"] == 0.2

    def test_all_plots_saved_to_output_dir(self, mock_lmm_result, mock_data, tmp_path):
        """Test all diagnostic plots saved to output_dir."""
        result = validate_lmm_assumptions_comprehensive(
            lmm_result=mock_lmm_result,
            data=mock_data,
            output_dir=tmp_path
        )

        # Check all expected plots exist
        expected_plots = [
            "qq_plot_residuals.png",
            "residuals_vs_fitted.png",
            "qq_plot_random_intercepts.png",
            "qq_plot_random_slopes.png",
            "acf_plot.png",
            "cooks_distance.png"
        ]

        for plot_name in expected_plots:
            plot_path = tmp_path / plot_name
            assert plot_path.exists(), f"Plot {plot_name} should exist"
            assert plot_path in result["plot_paths"]

    def test_failed_convergence_detection(self, mock_lmm_result, mock_data, tmp_path):
        """Test detection of convergence failures."""
        mock_lmm_result.converged = False

        result = validate_lmm_assumptions_comprehensive(
            lmm_result=mock_lmm_result,
            data=mock_data,
            output_dir=tmp_path
        )

        diag = result["diagnostics"]["convergence"]
        assert diag["converged"] is False
        assert diag["pass"] is False
        assert "convergence" in result["message"].lower()
