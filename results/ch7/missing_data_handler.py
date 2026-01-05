#!/usr/bin/env python3
"""
Missing Data Analysis Utility for Chapter 7
Provides proper missing data handling and documentation

Addresses the systematic issue of excluding participants without proper analysis.
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Tuple, Dict, List

def analyze_missing_pattern(df: pd.DataFrame, 
                           key_columns: List[str] = None) -> Dict:
    """
    Analyze missing data patterns in a dataframe.
    
    Args:
        df: DataFrame to analyze
        key_columns: List of important columns to focus on (default: all)
        
    Returns:
        Dictionary with missing data statistics and patterns
    """
    if key_columns is None:
        key_columns = df.columns.tolist()
    
    analysis = {
        'total_observations': len(df),
        'complete_cases': df.dropna().shape[0],
        'incomplete_cases': df.shape[0] - df.dropna().shape[0],
        'percent_complete': (df.dropna().shape[0] / df.shape[0]) * 100,
        'column_missing': {},
        'pattern_summary': None,
        'mcar_test': None
    }
    
    # Analyze each column
    for col in key_columns:
        if col in df.columns:
            n_missing = df[col].isna().sum()
            pct_missing = (n_missing / len(df)) * 100
            analysis['column_missing'][col] = {
                'n_missing': n_missing,
                'percent_missing': round(pct_missing, 2)
            }
    
    # Identify missing data patterns
    missing_pattern = df[key_columns].isna()
    pattern_counts = missing_pattern.value_counts()
    
    analysis['pattern_summary'] = {
        'n_patterns': len(pattern_counts),
        'most_common_pattern': str(pattern_counts.index[0]) if len(pattern_counts) > 0 else None,
        'pattern_frequencies': pattern_counts.to_dict() if len(pattern_counts) < 10 else 'Too many patterns'
    }
    
    return analysis

def little_mcar_test(df: pd.DataFrame, 
                     columns: List[str] = None) -> Tuple[float, float, bool]:
    """
    Simplified MCAR test (Little's MCAR test approximation).
    
    Note: This is a simplified version. For publication, use specialized packages
    like impyute or R's naniar/mice packages for full Little's MCAR test.
    
    Args:
        df: DataFrame to test
        columns: Columns to include in test
        
    Returns:
        Tuple of (chi2_statistic, p_value, is_mcar)
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Create missingness indicators
    missing_indicators = df[columns].isna().astype(int)
    
    # Simple test: Check if missingness in one variable predicts values in others
    # This is a simplified approach - proper Little's test requires EM algorithm
    
    # For each variable with missing data
    test_results = []
    for col in columns:
        if df[col].isna().sum() > 0 and df[col].isna().sum() < len(df):
            # Test if missingness is related to other variables
            for other_col in columns:
                if other_col != col and df[other_col].notna().sum() > 0:
                    # Compare means of other_col between missing and non-missing groups
                    group_missing = df[df[col].isna()][other_col].dropna()
                    group_complete = df[df[col].notna()][other_col].dropna()
                    
                    if len(group_missing) > 1 and len(group_complete) > 1:
                        t_stat, p_val = stats.ttest_ind(group_missing, group_complete)
                        test_results.append(p_val)
    
    if test_results:
        # Combine p-values using Fisher's method
        chi2_stat = -2 * np.sum(np.log(test_results))
        df_chi2 = 2 * len(test_results)
        p_value = 1 - stats.chi2.cdf(chi2_stat, df_chi2)
        is_mcar = p_value > 0.05  # Not reject MCAR if p > 0.05
    else:
        # No missing data or all missing
        chi2_stat, p_value = 0, 1.0
        is_mcar = True
    
    return chi2_stat, p_value, is_mcar

def document_excluded_participants(df_full: pd.DataFrame,
                                  df_complete: pd.DataFrame,
                                  uid_col: str = 'UID',
                                  demo_cols: List[str] = None) -> pd.DataFrame:
    """
    Document characteristics of excluded participants.
    
    Args:
        df_full: Full dataset with missing data
        df_complete: Dataset after exclusions
        uid_col: Name of participant ID column
        demo_cols: Demographic columns to compare
        
    Returns:
        DataFrame comparing included vs excluded participants
    """
    if demo_cols is None:
        demo_cols = ['age', 'sex', 'education']
    
    # Identify excluded participants
    included_ids = set(df_complete[uid_col])
    excluded_mask = ~df_full[uid_col].isin(included_ids)
    
    excluded_df = df_full[excluded_mask]
    included_df = df_full[~excluded_mask]
    
    comparison = {
        'Variable': [],
        'Included_Mean': [],
        'Included_SD': [],
        'Excluded_Mean': [],
        'Excluded_SD': [],
        'Difference': [],
        'p_value': []
    }
    
    for col in demo_cols:
        if col in df_full.columns:
            inc_data = included_df[col].dropna()
            exc_data = excluded_df[col].dropna()
            
            if len(exc_data) > 0:
                if inc_data.dtype in [np.float64, np.int64]:
                    inc_mean = inc_data.mean()
                    inc_std = inc_data.std()
                    exc_mean = exc_data.mean()
                    exc_std = exc_data.std()
                    
                    if len(exc_data) > 1:
                        t_stat, p_val = stats.ttest_ind(inc_data, exc_data)
                    else:
                        p_val = np.nan
                    
                    comparison['Variable'].append(col)
                    comparison['Included_Mean'].append(round(inc_mean, 2))
                    comparison['Included_SD'].append(round(inc_std, 2))
                    comparison['Excluded_Mean'].append(round(exc_mean, 2))
                    comparison['Excluded_SD'].append(round(exc_std, 2))
                    comparison['Difference'].append(round(exc_mean - inc_mean, 2))
                    comparison['p_value'].append(round(p_val, 3) if not np.isnan(p_val) else 'N/A')
    
    return pd.DataFrame(comparison)

def create_missing_data_report(df: pd.DataFrame,
                              key_columns: List[str],
                              uid_col: str = 'UID') -> str:
    """
    Create comprehensive missing data report.
    
    Args:
        df: DataFrame to analyze
        key_columns: Important columns for analysis
        uid_col: Participant identifier column
        
    Returns:
        Formatted report string
    """
    analysis = analyze_missing_pattern(df, key_columns)
    
    report = []
    report.append("=" * 60)
    report.append("MISSING DATA ANALYSIS REPORT")
    report.append("=" * 60)
    report.append("")
    
    # Overall summary
    report.append("OVERALL SUMMARY")
    report.append("-" * 40)
    report.append(f"Total participants: {analysis['total_observations']}")
    report.append(f"Complete cases: {analysis['complete_cases']} ({analysis['percent_complete']:.1f}%)")
    report.append(f"Incomplete cases: {analysis['incomplete_cases']} ({100-analysis['percent_complete']:.1f}%)")
    report.append("")
    
    # Column-specific missing
    report.append("MISSING DATA BY VARIABLE")
    report.append("-" * 40)
    for col, stats in analysis['column_missing'].items():
        if stats['n_missing'] > 0:
            report.append(f"{col:30} {stats['n_missing']:3} missing ({stats['percent_missing']:.1f}%)")
    report.append("")
    
    # MCAR test
    report.append("MISSING COMPLETELY AT RANDOM (MCAR) TEST")
    report.append("-" * 40)
    
    # Perform simplified MCAR test
    numeric_cols = [c for c in key_columns if c in df.columns and df[c].dtype in [np.float64, np.int64]]
    if numeric_cols:
        chi2, p_val, is_mcar = little_mcar_test(df[numeric_cols])
        report.append(f"Test statistic: {chi2:.2f}")
        report.append(f"p-value: {p_val:.4f}")
        report.append(f"Result: {'Data appears to be MCAR' if is_mcar else 'Data may not be MCAR'}")
        report.append("")
        report.append("Note: This is a simplified test. For publication, use")
        report.append("      specialized packages for full Little's MCAR test.")
    else:
        report.append("No numeric columns available for MCAR test")
    report.append("")
    
    # Recommendations
    report.append("RECOMMENDATIONS")
    report.append("-" * 40)
    
    if analysis['percent_complete'] >= 95:
        report.append("• Complete case analysis is reasonable (>95% complete)")
    elif analysis['percent_complete'] >= 90:
        report.append("• Consider complete case analysis with sensitivity check")
        report.append("• Document characteristics of excluded participants")
    else:
        report.append("• Consider multiple imputation for missing data")
        report.append("• Complete case analysis may introduce bias")
    
    if not is_mcar and p_val < 0.05:
        report.append("• Data may not be MCAR - consider MAR assumptions")
        report.append("• Multiple imputation recommended over listwise deletion")
    
    report.append("")
    report.append("=" * 60)
    
    return "\n".join(report)

def handle_missing_data(df: pd.DataFrame,
                        key_columns: List[str],
                        method: str = 'complete_case',
                        document: bool = True) -> Tuple[pd.DataFrame, Dict]:
    """
    Handle missing data with proper documentation.
    
    Args:
        df: DataFrame with potential missing data
        key_columns: Columns that must be complete
        method: 'complete_case', 'impute_mean', or 'impute_median'
        document: Whether to generate documentation
        
    Returns:
        Tuple of (processed_dataframe, documentation_dict)
    """
    documentation = {}
    
    if document:
        # Analyze before processing
        documentation['before'] = analyze_missing_pattern(df, key_columns)
        documentation['method'] = method
    
    if method == 'complete_case':
        # Drop rows with missing values in key columns
        df_processed = df.dropna(subset=[c for c in key_columns if c in df.columns])
        documentation['excluded_n'] = len(df) - len(df_processed)
        
    elif method == 'impute_mean':
        df_processed = df.copy()
        for col in key_columns:
            if col in df.columns and df[col].dtype in [np.float64, np.int64]:
                mean_val = df[col].mean()
                df_processed[col].fillna(mean_val, inplace=True)
                documentation[f'{col}_imputed_value'] = mean_val
                
    elif method == 'impute_median':
        df_processed = df.copy()
        for col in key_columns:
            if col in df.columns and df[col].dtype in [np.float64, np.int64]:
                median_val = df[col].median()
                df_processed[col].fillna(median_val, inplace=True)
                documentation[f'{col}_imputed_value'] = median_val
    else:
        raise ValueError(f"Unknown method: {method}")
    
    if document:
        documentation['after'] = analyze_missing_pattern(df_processed, key_columns)
        documentation['report'] = create_missing_data_report(df, key_columns)
    
    return df_processed, documentation

if __name__ == "__main__":
    print("Missing Data Handler Utility")
    print("=" * 60)
    print("\nFunctions available:")
    print("  - analyze_missing_pattern(): Analyze patterns of missing data")
    print("  - little_mcar_test(): Test if data is Missing Completely At Random")
    print("  - document_excluded_participants(): Compare included vs excluded")
    print("  - create_missing_data_report(): Generate comprehensive report")
    print("  - handle_missing_data(): Process missing data with documentation")
    print("\n" + "=" * 60)
    print("Import this module to add proper missing data handling to Ch7 scripts.")