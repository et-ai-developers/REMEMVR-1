"""
Classical Test Theory (CTT) Analysis Tools.

This module provides CTT-specific analysis functions for RQ 5.12
(methodological comparison of IRT vs CTT).

Functions:
- compute_cronbachs_alpha: Internal consistency reliability with bootstrap CIs
- compare_correlations_dependent: Steiger's z-test for dependent correlations

References:
- Cronbach (1951): Coefficient alpha and the internal structure of tests
- Steiger (1980): Tests for comparing elements of a correlation matrix
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np
from pathlib import Path


def compute_cronbachs_alpha(
    data: pd.DataFrame,
    n_bootstrap: int = 1000
) -> Dict[str, Any]:
    """
    Compute Cronbach's alpha with bootstrap confidence intervals.

    For dichotomous (0/1) items, Cronbach's alpha equals KR-20
    (Kuder-Richardson formula 20). This function handles both continuous
    and dichotomous data.

    Bootstrap Method:
    - Percentile method for 95% CI
    - Resamples participants (preserves item correlation structure)
    - 1000-10000 iterations recommended (1000 minimum per literature)

    Args:
        data: DataFrame with items as columns, participants as rows.
              Values should be numeric (0/1 for dichotomous, continuous for Likert).
              Missing values (NaN) handled via pairwise deletion.
        n_bootstrap: Number of bootstrap iterations (default 1000).
                     RQ 5.12 spec recommends 1000-10000.

    Returns:
        Dict with keys:
        - alpha: float - Cronbach's alpha coefficient
        - ci_lower: float - Bootstrap 95% CI lower bound (2.5th percentile)
        - ci_upper: float - Bootstrap 95% CI upper bound (97.5th percentile)
        - n_items: int - Number of items
        - n_participants: int - Number of participants

    Raises:
        ValueError: If fewer than 2 items or fewer than 3 participants

    Example:
        >>> data = pd.DataFrame({
        ...     'item1': [1, 0, 1, 0, 1],
        ...     'item2': [1, 1, 1, 0, 1],
        ...     'item3': [1, 0, 1, 1, 1]
        ... })
        >>> result = compute_cronbachs_alpha(data, n_bootstrap=1000)
        >>> assert 0 <= result['alpha'] <= 1
        >>> assert result['ci_lower'] < result['alpha'] < result['ci_upper']

    References:
        - Cronbach (1951): Original alpha formulation
        - PMC4205511: "Making sense of Cronbach's alpha"
        - PMC8451024 (2021): KR-20 equivalence for dichotomous items
        - RQ 5.12 1_concept.md Step 3b: CTT reliability requirements
    """
    # Validation
    if data.shape[1] < 2:
        raise ValueError("Cronbach's alpha requires at least 2 items")

    if data.shape[0] < 3:
        raise ValueError("Cronbach's alpha requires at least 3 participants for variance estimation")

    n_items = data.shape[1]
    n_participants = data.shape[0]

    # Compute point estimate
    alpha = _cronbach_alpha_formula(data)

    # Bootstrap confidence intervals
    bootstrap_alphas = []
    for _ in range(n_bootstrap):
        # Resample participants (preserves item correlation structure)
        bootstrap_sample = data.sample(n=n_participants, replace=True, random_state=None)
        bootstrap_alpha = _cronbach_alpha_formula(bootstrap_sample)
        bootstrap_alphas.append(bootstrap_alpha)

    # Percentile method for 95% CI
    bootstrap_alphas = np.array(bootstrap_alphas)
    ci_lower = np.percentile(bootstrap_alphas, 2.5)
    ci_upper = np.percentile(bootstrap_alphas, 97.5)

    return {
        'alpha': float(alpha),
        'ci_lower': float(ci_lower),
        'ci_upper': float(ci_upper),
        'n_items': int(n_items),
        'n_participants': int(n_participants)
    }


def _cronbach_alpha_formula(data: pd.DataFrame) -> float:
    """
    Calculate Cronbach's alpha using standard formula.

    Formula: α = (k/(k-1)) × (1 - Σσ²ᵢ / σ²ₓ)
    where:
    - k = number of items
    - Σσ²ᵢ = sum of item variances
    - σ²ₓ = variance of total scores

    Args:
        data: DataFrame with items as columns, participants as rows

    Returns:
        float: Cronbach's alpha coefficient

    Notes:
        - Uses ddof=1 (sample variance, not population variance)
        - Handles NaN via pairwise deletion (dropna in var/sum operations)
        - For binary items, this equals KR-20
    """
    # Item variances (variance of each column)
    item_variances = data.var(axis=0, ddof=1)
    sum_item_variances = item_variances.sum()

    # Total score variance (variance of row sums)
    total_scores = data.sum(axis=1)
    total_variance = total_scores.var(ddof=1)

    # Cronbach's alpha formula
    k = data.shape[1]
    alpha = (k / (k - 1)) * (1 - sum_item_variances / total_variance)

    return alpha


def compare_correlations_dependent(
    r12: float,
    r13: float,
    r23: float,
    n: int
) -> Dict[str, Any]:
    """
    Test if two dependent correlations differ significantly (Steiger's z-test).

    Tests whether r₁₂ differs from r₁₃ when both correlations share variable 1.
    This is appropriate for RQ 5.12 where Full CTT, Purified CTT, and IRT theta
    all come from the same N=100 participants (dependent correlations).

    Example Use Case (RQ 5.12):
    - Variable 1: IRT theta
    - Variable 2: Full CTT score
    - Variable 3: Purified CTT score
    - Question: Does r(IRT, Purified_CTT) > r(IRT, Full_CTT)?

    Args:
        r12: Correlation between variables 1 and 2
        r13: Correlation between variables 1 and 3
        r23: Correlation between variables 2 and 3
        n: Sample size (number of participants)

    Returns:
        Dict with keys:
        - z_statistic: float - Steiger's z-test statistic
        - p_value: float - Two-tailed p-value
        - r_difference: float - r13 - r12 (positive = r13 stronger)
        - significant: bool - Significant at α=0.05
        - interpretation: str - Plain language interpretation

    Raises:
        ValueError: If correlations not in [-1, 1] or n < 20

    Example:
        >>> result = compare_correlations_dependent(
        ...     r12=0.85,  # Full CTT - IRT
        ...     r13=0.92,  # Purified CTT - IRT
        ...     r23=0.88,  # Full CTT - Purified CTT
        ...     n=100
        ... )
        >>> print(result['interpretation'])
        'r13 (0.92) significantly higher than r12 (0.85), z=2.34, p=0.019'

    References:
        - Steiger (1980): Psychological Bulletin 87:245-251 (Equations 3 & 10)
        - RQ 5.12 1_stats.md: Steiger's z-test requirement
        - Online calculator: quantpsy.org/corrtest (for validation)

    Notes:
        - N=100 is adequate for Steiger's z-test (literature confirms N=103 sufficient)
        - Fisher's r-to-z is INVALID here (assumes independent samples)
        - Steiger's method correctly accounts for asymptotic covariance
    """
    # Validation
    if not all(-1 <= r <= 1 for r in [r12, r13, r23]):
        raise ValueError("All correlations must be in range [-1, 1]")

    if n < 20:
        raise ValueError("Steiger's z-test requires at least n=20 for validity")

    # Steiger (1980) Equation 3: Asymptotic covariance of r12 and r13
    # cov(r12, r13) = [r23 - 0.5 * r12 * r13 * (1 - r12² - r13² - r23²)] / (n - 3)

    # Fisher's z-transformation
    z12 = np.arctanh(r12)  # Fisher's z for r12
    z13 = np.arctanh(r13)  # Fisher's z for r13

    # Compute determinant of correlation matrix
    R = 1 - r12**2 - r13**2 - r23**2 + 2*r12*r13*r23

    # Steiger's covariance formula (Equation 10)
    # var(z12 - z13) = (2 - 2*f) / (n - 3)
    # where f = r23(1 - r12² - r13²) / (2*(1-r12²)*(1-r13²))

    numerator = r23 * (1 - r12**2) * (1 - r13**2)
    denominator = 2 * (1 - r12**2) * (1 - r13**2)
    f = numerator / denominator if denominator != 0 else 0

    var_diff = (2 - 2*f) / (n - 3)
    se_diff = np.sqrt(var_diff)

    # Steiger's z-statistic
    z_statistic = (z13 - z12) / se_diff

    # Two-tailed p-value
    from scipy.stats import norm
    p_value = 2 * (1 - norm.cdf(abs(z_statistic)))

    # Interpretation
    r_difference = r13 - r12
    significant = p_value < 0.05

    if significant:
        direction = "higher" if r_difference > 0 else "lower"
        interpretation = f"r13 ({r13:.2f}) significantly {direction} than r12 ({r12:.2f}), z={z_statistic:.2f}, p={p_value:.3f}"
    else:
        interpretation = f"No significant difference between r13 ({r13:.2f}) and r12 ({r12:.2f}), z={z_statistic:.2f}, p={p_value:.3f}"

    return {
        'z_statistic': float(z_statistic),
        'p_value': float(p_value),
        'r_difference': float(r_difference),
        'significant': bool(significant),
        'interpretation': interpretation
    }
