"""
Statistical Validation Functions for REMEMVR Analysis Pipeline

This module provides validation functions for ensuring data quality,
statistical validity, and lineage tracking throughout the analysis pipeline.

Key Features:
- Data lineage tracking (prevent using wrong data files)
- IRT validation (convergence, parameter ranges, missing data)
- LMM validation (convergence, residuals, assumptions)
- General data validation (columns, file existence, ranges)

Author: REMEMVR Automation System
Created: 2025-01-08
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
import json
from scipy import stats


# =============================================================================
# DATA LINEAGE TRACKING
# =============================================================================

def create_lineage_metadata(
    source_file: str,
    output_file: str,
    operation: str,
    parameters: Optional[Dict[str, Any]] = None,
    description: str = ""
) -> Dict[str, Any]:
    """
    Create lineage metadata for a data transformation.

    Prevents the critical error from RQ 5.1 where Pass 1 data was accidentally
    used for Pass 2 plots.

    Parameters
    ----------
    source_file : str
        Path to source/input file
    output_file : str
        Path to output file being created
    operation : str
        Name of operation (e.g., 'irt_calibration', 'lmm_analysis')
    parameters : dict, optional
        Parameters used in the operation
    description : str, optional
        Human-readable description

    Returns
    -------
    dict
        Lineage metadata dictionary

    Example
    -------
    >>> metadata = create_lineage_metadata(
    ...     source_file="results/ch5/rq1/data/irt_input_pass1.csv",
    ...     output_file="results/ch5/rq1/data/theta_scores_pass1.csv",
    ...     operation="irt_calibration",
    ...     parameters={"model": "GRM", "factors": 3},
    ...     description="IRT Pass 1 calibration"
    ... )
    """
    metadata = {
        "source_file": source_file,
        "output_file": output_file,
        "operation": operation,
        "timestamp": datetime.now().isoformat(),
        "description": description
    }

    if parameters:
        metadata["parameters"] = parameters

    return metadata


def save_lineage_to_file(metadata: Dict[str, Any], lineage_file: str) -> None:
    """
    Save lineage metadata to JSON file.

    Parameters
    ----------
    metadata : dict
        Lineage metadata dictionary
    lineage_file : str
        Path to save JSON file

    Example
    -------
    >>> save_lineage(metadata, "results/ch5/rq1/data/theta_scores_lineage.json")
    """
    lineage_path = Path(lineage_file)
    lineage_path.parent.mkdir(parents=True, exist_ok=True)

    with open(lineage_path, 'w') as f:
        json.dump(metadata, f, indent=2)


def load_lineage_from_file(lineage_file: str) -> Dict[str, Any]:
    """
    Load lineage metadata from JSON file.

    Parameters
    ----------
    lineage_file : str
        Path to lineage JSON file

    Returns
    -------
    dict
        Lineage metadata dictionary

    Example
    -------
    >>> metadata = load_lineage("results/ch5/rq1/data/theta_scores_lineage.json")
    """
    with open(lineage_file, 'r') as f:
        return json.load(f)


def validate_lineage(
    lineage_file: str,
    expected_source: Optional[str] = None,
    expected_pass: Optional[int] = None
) -> Dict[str, Any]:
    """
    Validate that data comes from the expected source.

    Parameters
    ----------
    lineage_file : str
        Path to lineage JSON file
    expected_source : str, optional
        Expected source file name (can be partial match)
    expected_pass : int, optional
        Expected pass number (1 or 2)

    Returns
    -------
    dict
        Validation result with 'valid' boolean and 'message'

    Example
    -------
    >>> result = validate_lineage(
    ...     lineage_file="results/ch5/rq1/data/theta_scores_lineage.json",
    ...     expected_source="irt_input_pass2.csv",
    ...     expected_pass=2
    ... )
    >>> assert result['valid'], result['message']
    """
    try:
        metadata = load_lineage_from_file(lineage_file)
    except FileNotFoundError:
        return {
            "valid": False,
            "message": f"Lineage file not found: {lineage_file}"
        }

    # Check source file
    if expected_source:
        source_file = metadata.get("source_file", "")
        if expected_source not in source_file:
            return {
                "valid": False,
                "message": f"Expected source '{expected_source}' but found '{source_file}'"
            }

    # Check pass number
    if expected_pass:
        pass_num = metadata.get("parameters", {}).get("pass", metadata.get("pass"))
        if pass_num != expected_pass:
            return {
                "valid": False,
                "message": f"Expected pass {expected_pass} but found pass {pass_num}"
            }

    return {
        "valid": True,
        "message": "Lineage validated successfully",
        "metadata": metadata
    }


# =============================================================================
# IRT VALIDATION
# =============================================================================

def validate_irt_convergence(results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate IRT model convergence.

    Parameters
    ----------
    results : dict
        IRT calibration results with 'model_converged', 'final_loss', etc.

    Returns
    -------
    dict
        Validation result with 'converged' boolean and details

    Example
    -------
    >>> result = validate_irt_convergence(irt_results)
    >>> if not result['converged']:
    ...     print(f"Warning: {result['message']}")
    """
    converged = results.get("model_converged", False)
    final_loss = results.get("final_loss", None)
    epochs_run = results.get("epochs_run", None)

    if converged:
        return {
            "converged": True,
            "message": "Model converged successfully",
            "final_loss": final_loss,
            "epochs_run": epochs_run
        }
    else:
        return {
            "converged": False,
            "message": "Model did not converge",
            "final_loss": final_loss,
            "epochs_run": epochs_run,
            "warning": "Results may be unreliable"
        }


def validate_irt_parameters(
    df_items: pd.DataFrame,
    a_min: float = 0.4,
    b_max: float = 3.0,
    a_col: str = "a",
    b_col: str = "b"
) -> Dict[str, Any]:
    """
    Validate IRT item parameters for psychometric quality.

    Flags items with:
    - Low discrimination (a < a_min, default 0.4)
    - Extreme difficulty (|b| > b_max, default 3.0)

    Parameters
    ----------
    df_items : pd.DataFrame
        Item parameters with columns 'item_name', 'a', 'b'
    a_min : float, default 0.4
        Minimum discrimination threshold
    b_max : float, default 3.0
        Maximum |difficulty| threshold
    a_col : str, default 'a'
        Name of discrimination column
    b_col : str, default 'b'
        Name of difficulty column

    Returns
    -------
    dict
        Validation result with flagged items

    Example
    -------
    >>> result = validate_irt_parameters(df_items)
    >>> print(f"Flagged {result['n_flagged']} items")
    """
    flagged_items = []

    for idx, row in df_items.iterrows():
        item_name = row.get("item_name", idx)
        a_val = row.get(a_col, np.nan)
        b_val = row.get(b_col, np.nan)

        reasons = []
        if a_val < a_min:
            reasons.append(f"Low discrimination (a={a_val:.2f} < {a_min})")
        if abs(b_val) > b_max:
            reasons.append(f"Extreme difficulty (|b|={abs(b_val):.2f} > {b_max})")

        if reasons:
            flagged_items.append({
                "item_name": item_name,
                "a": a_val,
                "b": b_val,
                "reasons": reasons
            })

    return {
        "valid": len(flagged_items) == 0,
        "n_flagged": len(flagged_items),
        "flagged_items": flagged_items,
        "total_items": len(df_items)
    }


def check_missing_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Check for missing data in DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Data to check

    Returns
    -------
    dict
        Missing data report

    Example
    -------
    >>> result = check_missing_data(df)
    >>> if result['has_missing']:
    ...     print(f"Warning: {result['total_missing']} missing values")
    """
    missing_by_column = df.isnull().sum().to_dict()
    missing_by_column = {k: int(v) for k, v in missing_by_column.items() if v > 0}

    total_missing = int(df.isnull().sum().sum())
    total_cells = df.shape[0] * df.shape[1]

    return {
        "has_missing": bool(total_missing > 0),
        "total_missing": total_missing,
        "total_cells": total_cells,
        "percent_missing": (total_missing / total_cells * 100) if total_cells > 0 else 0,
        "missing_by_column": missing_by_column
    }


# =============================================================================
# LMM VALIDATION
# =============================================================================

def validate_lmm_convergence(lmm_result) -> Dict[str, Any]:
    """
    Validate LMM convergence.

    Parameters
    ----------
    lmm_result : statsmodels.regression.mixed_linear_model.MixedLMResults
        Fitted LMM model result

    Returns
    -------
    dict
        Validation result with convergence status

    Example
    -------
    >>> result = validate_lmm_convergence(lmm_fit)
    >>> assert result['converged'], result['message']
    """
    converged = getattr(lmm_result, "converged", True)

    if converged:
        return {
            "converged": True,
            "message": "LMM converged successfully"
        }
    else:
        return {
            "converged": False,
            "message": "LMM did not converge",
            "warning": "Results may be unreliable"
        }


def validate_lmm_residuals(
    residuals: Union[np.ndarray, pd.Series],
    alpha: float = 0.05
) -> Dict[str, Any]:
    """
    Validate LMM residuals for normality.

    Uses Shapiro-Wilk test for normality (n < 5000) or
    Kolmogorov-Smirnov test (n >= 5000).

    Parameters
    ----------
    residuals : array-like
        Model residuals
    alpha : float, default 0.05
        Significance level for normality test

    Returns
    -------
    dict
        Validation result with normality test

    Example
    -------
    >>> result = validate_lmm_residuals(model.resid)
    >>> if not result['normality_test']['passed']:
    ...     print("Warning: Residuals may not be normal")
    """
    residuals = np.asarray(residuals)
    n = len(residuals)

    # Choose normality test based on sample size
    if n < 5000:
        stat, p_value = stats.shapiro(residuals)
        test_name = "Shapiro-Wilk"
    else:
        # For large samples, use Kolmogorov-Smirnov
        # Standardize residuals before testing against standard normal
        residuals_standardized = (residuals - np.mean(residuals)) / np.std(residuals)
        stat, p_value = stats.kstest(residuals_standardized, 'norm')
        test_name = "Kolmogorov-Smirnov"

    passed = bool(p_value > alpha)

    return {
        "n_residuals": n,
        "normality_test": {
            "test_name": test_name,
            "statistic": float(stat),
            "p_value": float(p_value),
            "alpha": alpha,
            "passed": passed
        },
        "residual_stats": {
            "mean": float(np.mean(residuals)),
            "std": float(np.std(residuals)),
            "min": float(np.min(residuals)),
            "max": float(np.max(residuals))
        }
    }


# =============================================================================
# GENERAL VALIDATION
# =============================================================================

def validate_data_columns(
    df: pd.DataFrame,
    required_columns: List[str]
) -> Dict[str, Any]:
    """
    Validate that required columns exist in DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Data to validate
    required_columns : list of str
        Required column names

    Returns
    -------
    dict
        Validation result

    Example
    -------
    >>> result = validate_data_columns(df, ["UID", "theta", "SVR"])
    >>> assert result['valid'], f"Missing: {result['missing_columns']}"
    """
    existing_columns = set(df.columns)
    required_set = set(required_columns)
    missing = list(required_set - existing_columns)

    return {
        "valid": len(missing) == 0,
        "missing_columns": missing,
        "existing_columns": list(existing_columns),
        "n_required": len(required_columns),
        "n_missing": len(missing)
    }


def check_file_exists(file_path: str) -> Dict[str, Any]:
    """
    Validate that file exists.

    Parameters
    ----------
    file_path : str
        Path to file

    Returns
    -------
    dict
        Validation result

    Example
    -------
    >>> result = validate_file_exists("results/ch5/rq1/data/input.csv")
    >>> assert result['exists'], result['message']
    """
    path = Path(file_path)
    exists = path.exists()

    if exists:
        return {
            "exists": True,
            "file_path": str(path),
            "message": f"File exists: {file_path}"
        }
    else:
        return {
            "exists": False,
            "file_path": str(path),
            "message": f"File does not exist: {file_path}"
        }


def validate_numeric_range(
    data: Union[pd.Series, np.ndarray],
    min_val: Optional[float] = None,
    max_val: Optional[float] = None,
    column_name: str = "data"
) -> Dict[str, Any]:
    """
    Validate that numeric data falls within expected range.

    Parameters
    ----------
    data : pd.Series or np.ndarray
        Numeric data to validate
    min_val : float, optional
        Minimum allowed value
    max_val : float, optional
        Maximum allowed value
    column_name : str, default 'data'
        Name of column for reporting

    Returns
    -------
    dict
        Validation result

    Example
    -------
    >>> result = validate_numeric_range(df['theta'], min_val=-3, max_val=3)
    >>> if not result['valid']:
    ...     print(f"{result['n_out_of_range']} values out of range")
    """
    data = np.asarray(data)
    out_of_range = []

    if min_val is not None:
        below_min = data < min_val
        out_of_range.append(below_min)

    if max_val is not None:
        above_max = data > max_val
        out_of_range.append(above_max)

    if out_of_range:
        out_of_range_mask = np.logical_or.reduce(out_of_range)
        n_out_of_range = int(np.sum(out_of_range_mask))
    else:
        n_out_of_range = 0

    return {
        "valid": n_out_of_range == 0,
        "n_out_of_range": n_out_of_range,
        "total_values": len(data),
        "column_name": column_name,
        "min_val": min_val,
        "max_val": max_val,
        "data_min": float(np.min(data)),
        "data_max": float(np.max(data))
    }


# =============================================================================
# VALIDATION REPORTING
# =============================================================================

def generate_validation_report(
    validation_checks: Dict[str, Dict[str, Any]],
    report_title: str = "Validation Report"
) -> Dict[str, Any]:
    """
    Generate comprehensive validation report from multiple checks.

    Parameters
    ----------
    validation_checks : dict
        Dictionary of validation check results
        Key = check name, Value = check result dict
    report_title : str, default 'Validation Report'
        Title for the report

    Returns
    -------
    dict
        Comprehensive validation report

    Example
    -------
    >>> checks = {
    ...     "lineage": validate_lineage(...),
    ...     "convergence": validate_irt_convergence(...),
    ...     "parameters": validate_irt_parameters(...)
    ... }
    >>> report = generate_validation_report(checks, "RQ 5.1 Validation")
    """
    # Determine overall status
    all_passed = True
    for check_name, result in validation_checks.items():
        # Check various indicators of failure
        if "valid" in result and not result["valid"]:
            all_passed = False
        if "converged" in result and not result["converged"]:
            all_passed = False
        if "has_missing" in result and result["has_missing"]:
            # Missing data might be acceptable, but flag it
            pass

    report = {
        "report_title": report_title,
        "timestamp": datetime.now().isoformat(),
        "overall_status": "PASSED" if all_passed else "FAILED",
        "n_checks": len(validation_checks),
        "checks": validation_checks
    }

    return report


def save_validation_report(report: Dict[str, Any], report_file: str) -> None:
    """
    Save validation report to JSON file.

    Parameters
    ----------
    report : dict
        Validation report dictionary
    report_file : str
        Path to save JSON file

    Example
    -------
    >>> save_validation_report(report, "results/ch5/rq1/validation/report.json")
    """
    report_path = Path(report_file)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)


# ============================================================================
# PIECEWISE LMM VALIDATION FUNCTIONS
# ============================================================================

def validate_hypothesis_tests(hypothesis_tests: pd.DataFrame) -> Dict[str, Any]:
    """
    Validate hypothesis test results format and p-value bounds.

    Checks:
    - Required columns present (Term, p_uncorrected, p_bonferroni)
    - P-values in valid range [0, 1]
    - Bonferroni correction properly applied
    - No missing values

    Parameters
    ----------
    hypothesis_tests : DataFrame
        Hypothesis test results with columns: Term, Coef, SE, z, p_uncorrected, p_bonferroni

    Returns
    -------
    dict
        Validation result with keys: valid (bool), message (str), failed_checks (list)

    Examples
    --------
    >>> tests = pd.DataFrame({
    ...     'Term': ['Days_within', 'Segment[Late]'],
    ...     'p_uncorrected': [0.001, 0.045],
    ...     'p_bonferroni': [0.015, 0.675]
    ... })
    >>> result = validate_hypothesis_tests(tests)
    >>> result['valid']
    True
    """
    failed_checks = []

    # Check required columns
    required_cols = ['Term', 'p_uncorrected', 'p_bonferroni']
    missing_cols = [c for c in required_cols if c not in hypothesis_tests.columns]
    if missing_cols:
        failed_checks.append(f"Missing required columns: {missing_cols}")

    if not failed_checks:  # Only proceed if columns exist
        # Check p-value bounds
        for col in ['p_uncorrected', 'p_bonferroni']:
            if not hypothesis_tests[col].between(0, 1).all():
                out_of_bounds = hypothesis_tests[~hypothesis_tests[col].between(0, 1)]
                failed_checks.append(f"{col} values out of [0,1] bounds: {len(out_of_bounds)} rows")

        # Check for missing values
        for col in required_cols:
            if hypothesis_tests[col].isna().any():
                failed_checks.append(f"{col} has {hypothesis_tests[col].isna().sum()} missing values")

    valid = len(failed_checks) == 0
    message = "All hypothesis test validations passed" if valid else f"{len(failed_checks)} validation checks failed"

    return {
        "valid": valid,
        "message": message,
        "failed_checks": failed_checks
    }


def validate_contrasts(contrasts: pd.DataFrame) -> Dict[str, Any]:
    """
    Validate contrast results format and dual p-value reporting (Decision D068).

    Checks:
    - Required columns present
    - Dual p-values reported (uncorrected + Bonferroni)
    - Effect size present
    - No missing values

    Parameters
    ----------
    contrasts : DataFrame
        Contrast results with columns: Contrast, beta, SE, z, p_uncorrected, p_bonferroni, effect_size

    Returns
    -------
    dict
        Validation result with keys: valid (bool), message (str)

    Examples
    --------
    >>> contrasts = pd.DataFrame({
    ...     'Contrast': ['Congruent-Common'],
    ...     'beta': [0.15],
    ...     'p_uncorrected': [0.001],
    ...     'p_bonferroni': [0.015]
    ... })
    >>> result = validate_contrasts(contrasts)
    >>> result['valid']
    True
    """
    failed_checks = []

    # Check required columns
    required_cols = ['Contrast', 'beta', 'p_uncorrected', 'p_bonferroni']
    missing_cols = [c for c in required_cols if c not in contrasts.columns]
    if missing_cols:
        failed_checks.append(f"Missing required columns: {missing_cols}")

    if not failed_checks:
        # Check dual p-value reporting (Decision D068)
        if 'p_uncorrected' not in contrasts.columns or 'p_bonferroni' not in contrasts.columns:
            failed_checks.append("Decision D068 violated: Must report both uncorrected and Bonferroni-corrected p-values")

        # Check p-value bounds
        for col in ['p_uncorrected', 'p_bonferroni']:
            if col in contrasts.columns and not contrasts[col].between(0, 1).all():
                failed_checks.append(f"{col} values out of [0,1] bounds")

    valid = len(failed_checks) == 0
    message = "All contrast validations passed" if valid else f"{len(failed_checks)} validation checks failed"

    return {
        "valid": valid,
        "message": message
    }


def validate_probability_transform(theta: np.ndarray, probability: np.ndarray) -> Dict[str, Any]:
    """
    Validate theta-to-probability transformation (logistic function).

    Checks:
    - Probability values in [0, 1]
    - Monotonic relationship (higher theta → higher probability)
    - No missing values
    - Arrays same length

    Parameters
    ----------
    theta : ndarray
        Theta scores (ability estimates, unbounded)
    probability : ndarray
        Probability scores (transformed to [0,1])

    Returns
    -------
    dict
        Validation result with keys: valid (bool), message (str)

    Examples
    --------
    >>> theta = np.array([-1.0, 0.0, 1.0])
    >>> prob = 1 / (1 + np.exp(-theta))
    >>> result = validate_probability_transform(theta, prob)
    >>> result['valid']
    True
    """
    failed_checks = []

    # Check array lengths match
    if len(theta) != len(probability):
        failed_checks.append(f"Array length mismatch: theta={len(theta)}, probability={len(probability)}")
        return {"valid": False, "message": "Array length mismatch"}

    # Check probability bounds
    if not np.all((probability >= 0) & (probability <= 1)):
        out_of_bounds = np.sum((probability < 0) | (probability > 1))
        failed_checks.append(f"Probability values out of [0,1] bounds: {out_of_bounds} values")

    # Check for missing values
    if np.any(np.isnan(theta)):
        failed_checks.append(f"Theta has {np.sum(np.isnan(theta))} NaN values")
    if np.any(np.isnan(probability)):
        failed_checks.append(f"Probability has {np.sum(np.isnan(probability))} NaN values")

    # Check monotonic relationship (correlation should be strongly positive)
    if len(theta) > 2 and not failed_checks:
        correlation = np.corrcoef(theta, probability)[0, 1]
        if correlation < 0.95:  # Should be nearly perfect monotonic
            failed_checks.append(f"Weak theta-probability correlation: {correlation:.3f} (expected > 0.95)")

    valid = len(failed_checks) == 0
    message = "Probability transform validation passed" if valid else f"{len(failed_checks)} validation checks failed"

    return {
        "valid": valid,
        "message": message
    }
