"""
Tests for extract_segment_slopes_from_lmm function (Tool 26)

RQ 5.8 Test 4 (Convergent Evidence) requires Early/Late slope ratio < 0.5
to indicate robust two-phase forgetting pattern.

Delta method SE propagation required for ratio because ratio SE != simple quadrature.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from unittest.mock import Mock
from tools.analysis_lmm import extract_segment_slopes_from_lmm


# =============================================================================
# Test 1: Basic extraction with default parameters
# =============================================================================

def test_basic_extraction_default_params():
    """Test basic slope extraction with default column names"""
    # Create mock LMM result
    mock_lmm = Mock()
    mock_lmm.params = pd.Series({
        'Intercept': 0.5,
        'Days_within': -0.3,  # Early slope
        'Days_within:SegmentLate': 0.2,  # Interaction (adds to Early to get Late)
    })
    mock_lmm.bse = pd.Series({
        'Intercept': 0.05,
        'Days_within': 0.04,
        'Days_within:SegmentLate': 0.06,
    })
    # Covariance matrix for delta method
    mock_lmm.cov_params = pd.DataFrame({
        'Intercept': [0.0025, 0.0, 0.0],
        'Days_within': [0.0, 0.0016, 0.0004],
        'Days_within:SegmentLate': [0.0, 0.0004, 0.0036],
    }, index=['Intercept', 'Days_within', 'Days_within:SegmentLate'])

    result = extract_segment_slopes_from_lmm(mock_lmm)

    # Check structure
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3
    assert list(result.columns) == ['metric', 'value', 'SE', 'CI_lower', 'CI_upper', 'interpretation']

    # Check metric names
    assert list(result['metric']) == ['Early_slope', 'Late_slope', 'Ratio_Late_Early']

    # Check Early slope
    early = result.loc[result['metric'] == 'Early_slope'].iloc[0]
    assert early['value'] == pytest.approx(-0.3)
    assert early['SE'] == pytest.approx(0.04)
    assert early['CI_lower'] == pytest.approx(-0.3 - 1.96*0.04, abs=0.001)
    assert early['CI_upper'] == pytest.approx(-0.3 + 1.96*0.04, abs=0.001)

    # Check Late slope (Early + interaction)
    late = result.loc[result['metric'] == 'Late_slope'].iloc[0]
    assert late['value'] == pytest.approx(-0.1)  # -0.3 + 0.2

    # Check ratio (Late / Early)
    ratio = result.loc[result['metric'] == 'Ratio_Late_Early'].iloc[0]
    assert ratio['value'] == pytest.approx(-0.1 / -0.3, abs=0.01)  # ~0.33


# =============================================================================
# Test 2: Custom column names
# =============================================================================

def test_custom_column_names():
    """Test extraction with custom segment and time column names"""
    mock_lmm = Mock()
    mock_lmm.params = pd.Series({
        'Intercept': 0.5,
        'Time': -0.4,  # Custom time column
        'Time:PhaseLate': 0.3,  # Custom segment column (must end in "Late")
    })
    mock_lmm.bse = pd.Series({
        'Intercept': 0.05,
        'Time': 0.03,
        'Time:PhaseLate': 0.04,
    })
    mock_lmm.cov_params = pd.DataFrame({
        'Intercept': [0.0025, 0.0, 0.0],
        'Time': [0.0, 0.0009, 0.0],
        'Time:PhaseLate': [0.0, 0.0, 0.0016],
    }, index=['Intercept', 'Time', 'Time:PhaseLate'])

    result = extract_segment_slopes_from_lmm(
        mock_lmm,
        segment_col='Phase',
        time_col='Time'
    )

    # Should still extract slopes correctly
    early = result.loc[result['metric'] == 'Early_slope'].iloc[0]
    assert early['value'] == pytest.approx(-0.4)

    late = result.loc[result['metric'] == 'Late_slope'].iloc[0]
    assert late['value'] == pytest.approx(-0.1)  # -0.4 + 0.3


# =============================================================================
# Test 3: Delta method SE propagation for ratio
# =============================================================================

def test_delta_method_ratio_se():
    """Test that ratio SE uses delta method, not simple quadrature"""
    mock_lmm = Mock()
    mock_lmm.params = pd.Series({
        'Intercept': 0.0,
        'Days_within': -0.5,
        'Days_within:SegmentLate': 0.3,
    })
    mock_lmm.bse = pd.Series({
        'Intercept': 0.0,
        'Days_within': 0.1,
        'Days_within:SegmentLate': 0.15,
    })
    # Include covariance between early and late
    cov_early_late = 0.005
    mock_lmm.cov_params = pd.DataFrame({
        'Intercept': [0.0, 0.0, 0.0],
        'Days_within': [0.0, 0.01, cov_early_late],
        'Days_within:SegmentLate': [0.0, cov_early_late, 0.0225],
    }, index=['Intercept', 'Days_within', 'Days_within:SegmentLate'])

    result = extract_segment_slopes_from_lmm(mock_lmm)

    # Delta method formula:
    # SE_ratio² = (∂ratio/∂early)²×SE_early² + (∂ratio/∂late)²×SE_late² + 2×(∂ratio/∂early)×(∂ratio/∂late)×Cov(early,late)
    # where ratio = late / early
    # ∂ratio/∂early = -late / early²
    # ∂ratio/∂late = 1 / early

    early_val = -0.5
    late_val = -0.2  # -0.5 + 0.3
    se_early = 0.1
    se_late = np.sqrt(0.01 + 0.0225 + 2*cov_early_late)  # SE of sum

    # Ratio SE should NOT equal simple quadrature
    ratio = result.loc[result['metric'] == 'Ratio_Late_Early'].iloc[0]
    simple_quadrature = np.sqrt(se_early**2 + se_late**2)

    # Delta method should give different SE due to covariance
    assert ratio['SE'] != pytest.approx(simple_quadrature, abs=0.001)


# =============================================================================
# Test 4: Interpretation for two-phase forgetting (ratio < 0.5)
# =============================================================================

def test_interpretation_two_phase_forgetting():
    """Test interpretation when Late/Early ratio < 0.5 (robust two-phase)"""
    mock_lmm = Mock()
    mock_lmm.params = pd.Series({
        'Intercept': 0.0,
        'Days_within': -0.6,
        'Days_within:SegmentLate': 0.4,  # Late = -0.2, ratio = 0.33
    })
    mock_lmm.bse = pd.Series({
        'Intercept': 0.0,
        'Days_within': 0.05,
        'Days_within:SegmentLate': 0.07,
    })
    mock_lmm.cov_params = pd.DataFrame({
        'Intercept': [0.0, 0.0, 0.0],
        'Days_within': [0.0, 0.0025, 0.0],
        'Days_within:SegmentLate': [0.0, 0.0, 0.0049],
    }, index=['Intercept', 'Days_within', 'Days_within:SegmentLate'])

    result = extract_segment_slopes_from_lmm(mock_lmm)

    ratio = result.loc[result['metric'] == 'Ratio_Late_Early'].iloc[0]
    assert ratio['value'] < 0.5
    assert 'two-phase' in ratio['interpretation'].lower()


# =============================================================================
# Test 5: Interpretation for single-phase forgetting (ratio >= 0.5)
# =============================================================================

def test_interpretation_single_phase_forgetting():
    """Test interpretation when Late/Early ratio >= 0.5 (single-phase)"""
    mock_lmm = Mock()
    mock_lmm.params = pd.Series({
        'Intercept': 0.0,
        'Days_within': -0.4,
        'Days_within:SegmentLate': 0.1,  # Late = -0.3, ratio = 0.75
    })
    mock_lmm.bse = pd.Series({
        'Intercept': 0.0,
        'Days_within': 0.05,
        'Days_within:SegmentLate': 0.06,
    })
    mock_lmm.cov_params = pd.DataFrame({
        'Intercept': [0.0, 0.0, 0.0],
        'Days_within': [0.0, 0.0025, 0.0],
        'Days_within:SegmentLate': [0.0, 0.0, 0.0036],
    }, index=['Intercept', 'Days_within', 'Days_within:SegmentLate'])

    result = extract_segment_slopes_from_lmm(mock_lmm)

    ratio = result.loc[result['metric'] == 'Ratio_Late_Early'].iloc[0]
    assert ratio['value'] >= 0.5
    assert 'single-phase' in ratio['interpretation'].lower() or 'weak' in ratio['interpretation'].lower()


# =============================================================================
# Test 6: Positive slopes (memory improvement, not typical forgetting)
# =============================================================================

def test_positive_slopes():
    """Test handling of positive slopes (atypical, but mathematically valid)"""
    mock_lmm = Mock()
    mock_lmm.params = pd.Series({
        'Intercept': 0.0,
        'Days_within': 0.2,  # Positive early slope (improvement)
        'Days_within:SegmentLate': 0.1,  # Late = 0.3
    })
    mock_lmm.bse = pd.Series({
        'Intercept': 0.0,
        'Days_within': 0.03,
        'Days_within:SegmentLate': 0.04,
    })
    mock_lmm.cov_params = pd.DataFrame({
        'Intercept': [0.0, 0.0, 0.0],
        'Days_within': [0.0, 0.0009, 0.0],
        'Days_within:SegmentLate': [0.0, 0.0, 0.0016],
    }, index=['Intercept', 'Days_within', 'Days_within:SegmentLate'])

    result = extract_segment_slopes_from_lmm(mock_lmm)

    # Should handle positive slopes without error
    early = result.loc[result['metric'] == 'Early_slope'].iloc[0]
    assert early['value'] == pytest.approx(0.2)

    late = result.loc[result['metric'] == 'Late_slope'].iloc[0]
    assert late['value'] == pytest.approx(0.3)

    # Interpretation should note atypical pattern
    assert 'improvement' in early['interpretation'].lower() or 'positive' in early['interpretation'].lower()


# =============================================================================
# Test 7: Missing required coefficients raises error
# =============================================================================

def test_missing_time_coefficient_error():
    """Test that missing time coefficient raises clear error"""
    mock_lmm = Mock()
    mock_lmm.params = pd.Series({
        'Intercept': 0.0,
        'Days_within:SegmentLate': 0.2,  # Missing Days_within
    })

    with pytest.raises(KeyError, match="Days_within"):
        extract_segment_slopes_from_lmm(mock_lmm)


def test_missing_interaction_coefficient_error():
    """Test that missing interaction coefficient raises clear error"""
    mock_lmm = Mock()
    mock_lmm.params = pd.Series({
        'Intercept': 0.0,
        'Days_within': -0.3,  # Missing Days_within:SegmentLate
    })

    with pytest.raises(KeyError, match="Days_within:Segment"):
        extract_segment_slopes_from_lmm(mock_lmm)


# =============================================================================
# Test 8: 95% confidence intervals use 1.96 multiplier
# =============================================================================

def test_confidence_interval_multiplier():
    """Test that 95% CIs use correct z-score (1.96)"""
    mock_lmm = Mock()
    mock_lmm.params = pd.Series({
        'Intercept': 0.0,
        'Days_within': -0.5,
        'Days_within:SegmentLate': 0.3,
    })
    se_early = 0.1
    mock_lmm.bse = pd.Series({
        'Intercept': 0.0,
        'Days_within': se_early,
        'Days_within:SegmentLate': 0.12,
    })
    mock_lmm.cov_params = pd.DataFrame({
        'Intercept': [0.0, 0.0, 0.0],
        'Days_within': [0.0, se_early**2, 0.0],
        'Days_within:SegmentLate': [0.0, 0.0, 0.12**2],
    }, index=['Intercept', 'Days_within', 'Days_within:SegmentLate'])

    result = extract_segment_slopes_from_lmm(mock_lmm)

    early = result.loc[result['metric'] == 'Early_slope'].iloc[0]
    expected_lower = -0.5 - 1.96 * se_early
    expected_upper = -0.5 + 1.96 * se_early

    assert early['CI_lower'] == pytest.approx(expected_lower, abs=0.001)
    assert early['CI_upper'] == pytest.approx(expected_upper, abs=0.001)


# =============================================================================
# Test 9: Late slope SE correctly propagates from Early + Interaction
# =============================================================================

def test_late_slope_se_propagation():
    """Test that Late slope SE = sqrt(Var(Early) + Var(Interaction) + 2*Cov)"""
    mock_lmm = Mock()
    mock_lmm.params = pd.Series({
        'Intercept': 0.0,
        'Days_within': -0.4,
        'Days_within:SegmentLate': 0.25,
    })
    se_early = 0.08
    se_interaction = 0.10
    cov = 0.003
    mock_lmm.bse = pd.Series({
        'Intercept': 0.0,
        'Days_within': se_early,
        'Days_within:SegmentLate': se_interaction,
    })
    mock_lmm.cov_params = pd.DataFrame({
        'Intercept': [0.0, 0.0, 0.0],
        'Days_within': [0.0, se_early**2, cov],
        'Days_within:SegmentLate': [0.0, cov, se_interaction**2],
    }, index=['Intercept', 'Days_within', 'Days_within:SegmentLate'])

    result = extract_segment_slopes_from_lmm(mock_lmm)

    late = result.loc[result['metric'] == 'Late_slope'].iloc[0]
    expected_se = np.sqrt(se_early**2 + se_interaction**2 + 2*cov)

    assert late['SE'] == pytest.approx(expected_se, abs=0.001)


# =============================================================================
# Test 10: Zero Early slope (division by zero handling)
# =============================================================================

def test_zero_early_slope_handling():
    """Test handling when Early slope is exactly zero (ratio undefined)"""
    mock_lmm = Mock()
    mock_lmm.params = pd.Series({
        'Intercept': 0.0,
        'Days_within': 0.0,  # Zero early slope
        'Days_within:SegmentLate': -0.2,
    })
    mock_lmm.bse = pd.Series({
        'Intercept': 0.0,
        'Days_within': 0.05,
        'Days_within:SegmentLate': 0.06,
    })
    mock_lmm.cov_params = pd.DataFrame({
        'Intercept': [0.0, 0.0, 0.0],
        'Days_within': [0.0, 0.0025, 0.0],
        'Days_within:SegmentLate': [0.0, 0.0, 0.0036],
    }, index=['Intercept', 'Days_within', 'Days_within:SegmentLate'])

    result = extract_segment_slopes_from_lmm(mock_lmm)

    # Ratio should be inf or nan
    ratio = result.loc[result['metric'] == 'Ratio_Late_Early'].iloc[0]
    assert np.isinf(ratio['value']) or np.isnan(ratio['value'])

    # Interpretation should indicate undefined
    assert 'undefined' in ratio['interpretation'].lower() or 'infinite' in ratio['interpretation'].lower()
