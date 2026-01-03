"""Statistical analysis functions with D068 compliance (dual p-value reporting)."""

import numpy as np
import pandas as pd
from scipy import stats
from typing import List, Optional, Dict, Union, Tuple
import warnings


def one_way_anova_d068(
    groups: Optional[List[np.ndarray]] = None,
    data: Optional[pd.DataFrame] = None,
    dv: Optional[str] = None,
    between: Optional[str] = None,
    correction: Optional[str] = 'bonferroni',
    n_comparisons: Optional[int] = None,
    post_hoc: Optional[str] = None
) -> Dict:
    """
    Perform one-way ANOVA with dual p-value reporting (D068 compliance).
    
    Parameters
    ----------
    groups : List[np.ndarray], optional
        List of arrays, each containing values for one group
    data : pd.DataFrame, optional
        DataFrame with long-format data
    dv : str, optional
        Dependent variable column name (if using DataFrame)
    between : str, optional
        Grouping variable column name (if using DataFrame)
    correction : str, optional
        Multiple comparison correction ('bonferroni', 'holm', None)
    n_comparisons : int, optional
        Number of comparisons for correction (default: k*(k-1)/2 for k groups)
    post_hoc : str, optional
        Post-hoc test to run ('tukey', 'bonferroni', None)
    
    Returns
    -------
    Dict containing:
        - F: F-statistic
        - p_uncorrected: Uncorrected p-value
        - p_corrected: Corrected p-value
        - eta_squared: Effect size
        - df_between: Between-groups degrees of freedom
        - df_within: Within-groups degrees of freedom
        - post_hoc: Post-hoc test results (if requested)
    """
    # Handle DataFrame input
    if data is not None and dv is not None and between is not None:
        groups = [data[data[between] == level][dv].values 
                  for level in data[between].unique()]
    
    if groups is None or len(groups) < 2:
        raise ValueError("Need at least 2 groups for ANOVA")
    
    # Perform one-way ANOVA
    f_stat, p_uncorr = stats.f_oneway(*groups)
    
    # Calculate degrees of freedom
    k = len(groups)  # Number of groups
    n_total = sum(len(g) for g in groups)
    df_between = k - 1
    df_within = n_total - k
    
    # Calculate effect size (eta squared)
    # SS_between = sum(n_i * (mean_i - grand_mean)^2)
    grand_mean = np.concatenate(groups).mean()
    ss_between = sum(len(g) * (g.mean() - grand_mean)**2 for g in groups)
    
    # SS_total = sum of all squared deviations from grand mean
    ss_total = sum(np.sum((g - grand_mean)**2) for g in groups)
    
    eta_squared = ss_between / ss_total if ss_total > 0 else 0.0
    
    # Apply multiple comparison correction
    if correction is None:
        p_corr = p_uncorr
    elif correction == 'bonferroni':
        if n_comparisons is None:
            # Default to all pairwise comparisons
            n_comparisons = k * (k - 1) // 2
        p_corr = min(p_uncorr * n_comparisons, 1.0)
    elif correction == 'holm':
        # For single test, Holm is same as uncorrected
        p_corr = p_uncorr
    else:
        p_corr = p_uncorr
    
    result = {
        'F': f_stat,
        'p_uncorrected': p_uncorr,
        'p_corrected': p_corr,
        'eta_squared': eta_squared,
        'df_between': df_between,
        'df_within': df_within
    }
    
    # Add post-hoc tests if requested
    if post_hoc == 'tukey':
        from statsmodels.stats.multicomp import pairwise_tukeyhsd
        
        # Prepare data for Tukey HSD
        all_data = np.concatenate(groups)
        group_labels = np.concatenate([[i] * len(g) for i, g in enumerate(groups)])
        
        tukey_result = pairwise_tukeyhsd(all_data, group_labels)
        
        result['post_hoc'] = {
            'method': 'tukey',
            'pairwise_comparisons': {
                'groups': tukey_result.groupsunique.tolist(),
                'reject': tukey_result.reject.tolist(),
                'pvalues': tukey_result.pvalues.tolist()
            }
        }
    
    return result


def chi_square_test_d068(
    contingency_table: np.ndarray,
    correction: Optional[str] = 'bonferroni',
    n_comparisons: Optional[int] = 1,
    yates_correction: bool = False,
    return_expected: bool = False
) -> Dict:
    """
    Perform chi-square test with dual p-value reporting (D068 compliance).
    
    Parameters
    ----------
    contingency_table : np.ndarray
        Contingency table (2D array)
    correction : str, optional
        Multiple comparison correction method
    n_comparisons : int, optional
        Number of comparisons for correction
    yates_correction : bool
        Apply Yates continuity correction (for 2x2 tables)
    return_expected : bool
        Return expected frequencies
    
    Returns
    -------
    Dict containing:
        - chi2: Chi-square statistic
        - p_uncorrected: Uncorrected p-value
        - p_corrected: Corrected p-value
        - cramers_v: Cramér's V effect size
        - df: Degrees of freedom
        - expected: Expected frequencies (if requested)
    """
    # Perform chi-square test
    chi2, p_uncorr, dof, expected = stats.chi2_contingency(
        contingency_table, 
        correction=yates_correction
    )
    
    # Calculate Cramér's V
    n = contingency_table.sum()
    min_dim = min(contingency_table.shape)
    cramers_v = compute_cramers_v(chi2, n, min_dim)
    
    # Apply correction
    if correction is None:
        p_corr = p_uncorr
    elif correction == 'bonferroni':
        p_corr = min(p_uncorr * n_comparisons, 1.0)
    else:
        p_corr = p_uncorr
    
    result = {
        'chi2': chi2,
        'p_uncorrected': p_uncorr,
        'p_corrected': p_corr,
        'cramers_v': cramers_v,
        'df': dof
    }
    
    if return_expected:
        result['expected'] = expected
    
    return result


def compute_cramers_v(chi2: float, n: int, k: int) -> float:
    """
    Compute Cramér's V effect size for contingency tables.
    
    Parameters
    ----------
    chi2 : float
        Chi-square statistic
    n : int
        Total sample size
    k : int
        Minimum of rows and columns in contingency table
    
    Returns
    -------
    float
        Cramér's V (0 to 1)
    """
    if n == 0 or k <= 1:
        return 0.0
    
    # Cramér's V = sqrt(chi2 / (n * (k-1)))
    v = np.sqrt(chi2 / (n * (k - 1)))
    
    # Ensure it's between 0 and 1
    return min(max(v, 0.0), 1.0)