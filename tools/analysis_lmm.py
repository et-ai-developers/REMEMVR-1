"""
Linear Mixed Model (LMM) Analysis Tool

Functions for fitting longitudinal mixed-effects models to theta scores.
Implements model comparison via AIC for trajectory analysis.

Author: REMEMVR Team
Date: 2025-01-07
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from statsmodels.regression.mixed_linear_model import MixedLMResults
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import warnings


# ============================================================================
# DATA PREPARATION
# ============================================================================

def prepare_lmm_data(
    theta_scores: pd.DataFrame,
    factors: Optional[list] = None
) -> pd.DataFrame:
    """
    Convert theta scores from wide to long format and add time variables.

    Parameters
    ----------
    theta_scores : pd.DataFrame
        Wide-format dataframe with columns:
        - UID : Participant ID
        - test : Test session (1, 2, 3, 4)
        - Theta_What, Theta_Where, Theta_When : Ability estimates

    factors : list, optional
        List of theta column names to melt. If None, uses all Theta_* columns.

    Returns
    -------
    pd.DataFrame
        Long-format dataframe with columns:
        - UID, test, Factor, Ability
        - Days, Days_sq, log_Days (time variables)

    Raises
    ------
    ValueError
        If required theta columns are missing

    Examples
    --------
    >>> df_wide = pd.DataFrame({
    ...     'UID': ['A001', 'A001'],
    ...     'test': [1, 2],
    ...     'Theta_What': [0.5, 0.3],
    ...     'Theta_Where': [0.2, 0.1],
    ...     'Theta_When': [0.8, 0.6]
    ... })
    >>> df_long = prepare_lmm_data(df_wide)
    >>> df_long.shape
    (6, 7)  # 2 obs × 3 factors = 6 rows
    """
    # Detect theta columns
    if factors is None:
        factors = [col for col in theta_scores.columns if col.startswith('Theta_')]

    if len(factors) == 0:
        raise ValueError("Missing required theta columns (Theta_*)")

    # Melt to long format
    df_long = theta_scores.melt(
        id_vars=['UID', 'test'],
        value_vars=factors,
        var_name='Factor',
        value_name='Ability'
    )

    # Clean Factor names (remove "Theta_" prefix)
    df_long['Factor'] = df_long['Factor'].str.replace('Theta_', '')

    # Add time variables
    day_map = {1: 0, 2: 1, 3: 3, 4: 6}  # Days since VR encoding
    df_long['Days'] = df_long['test'].map(day_map)
    df_long['Days_sq'] = df_long['Days'] ** 2
    df_long['log_Days'] = np.log(df_long['Days'] + 1)

    # Sort for readability
    df_long = df_long.sort_values(['UID', 'Factor', 'test']).reset_index(drop=True)

    return df_long


# ============================================================================
# MODEL CONFIGURATION
# ============================================================================

def configure_candidate_models(
    n_factors: int,
    reference_group: Optional[str] = None
) -> Dict[str, Dict[str, str]]:
    """
    Generate formulas for 5 candidate LMM models.

    Parameters
    ----------
    n_factors : int
        Number of factors (1 = single domain, >1 = multiple domains)

    reference_group : str, optional
        Reference level for Factor (e.g., 'What'). Required if n_factors > 1.

    Returns
    -------
    dict
        Dictionary with model configurations:
        {
            'Linear': {'formula': '...', 're_formula': '...'},
            'Quadratic': {...},
            ...
        }

    Raises
    ------
    ValueError
        If n_factors > 1 and reference_group is None

    Examples
    --------
    >>> models = configure_candidate_models(n_factors=3, reference_group='What')
    >>> models['Linear']['formula']
    "Ability ~ Days * C(Factor, Treatment('What'))"
    """
    if n_factors > 1 and reference_group is None:
        raise ValueError("Reference group must be specified for multi-factor analysis")

    models = {}

    if n_factors == 1:
        # Single-factor models (no Factor interaction)
        models = {
            'Linear': {
                'formula': 'Ability ~ Days',
                're_formula': '~Days'
            },
            'Quadratic': {
                'formula': 'Ability ~ Days + Days_sq',
                're_formula': '~Days'
            },
            'Log': {
                'formula': 'Ability ~ log_Days',
                're_formula': '~log_Days'
            },
            'Lin+Log': {
                'formula': 'Ability ~ Days + log_Days',
                're_formula': '~Days'
            },
            'Quad+Log': {
                'formula': 'Ability ~ Days + Days_sq + log_Days',
                're_formula': '~Days'
            }
        }
    else:
        # Multi-factor models (with Factor interaction)
        factor_term = f"C(Factor, Treatment('{reference_group}'))"

        models = {
            'Linear': {
                'formula': f'Ability ~ Days * {factor_term}',
                're_formula': '~Days'
            },
            'Quadratic': {
                'formula': f'Ability ~ (Days + Days_sq) * {factor_term}',
                're_formula': '~Days'
            },
            'Log': {
                'formula': f'Ability ~ log_Days * {factor_term}',
                're_formula': '~log_Days'
            },
            'Lin+Log': {
                'formula': f'Ability ~ (Days + log_Days) * {factor_term}',
                're_formula': '~Days'
            },
            'Quad+Log': {
                'formula': f'Ability ~ (Days + Days_sq + log_Days) * {factor_term}',
                're_formula': '~Days'
            }
        }

    return models


# ============================================================================
# SINGLE MODEL FITTING
# ============================================================================

def fit_lmm_model(
    data: pd.DataFrame,
    formula: str,
    groups: str,
    re_formula: str,
    reml: bool = False
) -> MixedLMResults:
    """
    Fit a single linear mixed model.

    Parameters
    ----------
    data : pd.DataFrame
        Long-format data with outcome, predictors, and grouping variable

    formula : str
        R-style formula for fixed effects (e.g., 'Ability ~ Days')

    groups : str
        Column name for grouping variable (typically 'UID')

    re_formula : str
        Formula for random effects (e.g., '~Days')

    reml : bool, default False
        Use restricted maximum likelihood? Set False for AIC comparison.

    Returns
    -------
    MixedLMResults
        Fitted model object with methods: .summary(), .aic, .params, etc.

    Raises
    ------
    RuntimeError
        If model fails to converge

    Examples
    --------
    >>> result = fit_lmm_model(
    ...     data=df_long,
    ...     formula='Ability ~ Days',
    ...     groups='UID',
    ...     re_formula='~Days',
    ...     reml=False
    ... )
    >>> print(result.aic)
    """
    # Build model
    model = smf.mixedlm(
        formula=formula,
        data=data,
        groups=data[groups],
        re_formula=re_formula
    )

    # Fit model
    try:
        result = model.fit(method=['lbfgs'], reml=reml)
    except Exception as e:
        raise RuntimeError(f"Model fitting failed: {str(e)}")

    # Check convergence
    if not result.converged:
        warnings.warn(
            f"Model did not converge. Formula: {formula}",
            UserWarning
        )

    return result


# ============================================================================
# MODEL COMPARISON
# ============================================================================

def compare_models(
    data: pd.DataFrame,
    n_factors: int,
    reference_group: Optional[str] = None,
    groups: str = 'UID',
    save_dir: Optional[Union[str, Path]] = None
) -> Dict:
    """
    Fit all candidate models and compare via AIC.

    Parameters
    ----------
    data : pd.DataFrame
        Long-format LMM data (from prepare_lmm_data)

    n_factors : int
        Number of factors in analysis

    reference_group : str, optional
        Reference level for Factor (required if n_factors > 1)

    groups : str, default 'UID'
        Column name for grouping variable

    save_dir : str or Path, optional
        Directory to save fitted models (.pkl files)

    Returns
    -------
    dict
        Results dictionary with keys:
        - 'models' : dict of fitted MixedLMResults
        - 'aic_comparison' : DataFrame with AIC, delta_AIC, weights
        - 'best_model_name' : str, name of best model
        - 'best_model' : MixedLMResults, best fitted model

    Examples
    --------
    >>> results = compare_models(
    ...     data=df_long,
    ...     n_factors=3,
    ...     reference_group='What'
    ... )
    >>> print(results['best_model_name'])
    'Lin+Log'
    >>> print(results['aic_comparison'])
    """
    # Get candidate models
    model_configs = configure_candidate_models(n_factors, reference_group)

    # Fit all models
    fitted_models = {}
    aics = {}

    for model_name, config in model_configs.items():
        print(f"Fitting {model_name} model...")

        # Check if saved model exists
        if save_dir is not None:
            model_path = Path(save_dir) / f"lmm_{model_name}.pkl"
            if model_path.exists():
                print(f"  Loading existing model from {model_path}")
                fitted_models[model_name] = MixedLMResults.load(str(model_path))
                aics[model_name] = fitted_models[model_name].aic
                continue

        # Fit model
        try:
            result = fit_lmm_model(
                data=data,
                formula=config['formula'],
                groups=groups,
                re_formula=config['re_formula'],
                reml=False
            )

            fitted_models[model_name] = result
            aics[model_name] = result.aic

            # Save model if directory specified
            if save_dir is not None:
                Path(save_dir).mkdir(parents=True, exist_ok=True)
                result.save(str(model_path))
                print(f"  Model saved to {model_path}")

        except Exception as e:
            print(f"  WARNING: {model_name} model failed: {str(e)}")
            fitted_models[model_name] = None
            aics[model_name] = np.inf

    # Create AIC comparison table
    aic_df = pd.DataFrame({
        'model_name': list(aics.keys()),
        'AIC': list(aics.values())
    })

    # Calculate delta AIC and weights
    aic_df = aic_df.sort_values('AIC').reset_index(drop=True)
    aic_df['delta_AIC'] = aic_df['AIC'] - aic_df['AIC'].min()
    aic_df['AIC_weight'] = np.exp(-aic_df['delta_AIC'] / 2)
    aic_df['AIC_weight'] = aic_df['AIC_weight'] / aic_df['AIC_weight'].sum()

    # Identify best model
    best_model_name = aic_df.iloc[0]['model_name']
    best_model = fitted_models[best_model_name]

    return {
        'models': fitted_models,
        'aic_comparison': aic_df,
        'best_model_name': best_model_name,
        'best_model': best_model
    }


# ============================================================================
# EXTRACT RESULTS
# ============================================================================

def extract_fixed_effects(result: MixedLMResults) -> pd.DataFrame:
    """
    Extract fixed effects table from fitted model.

    Parameters
    ----------
    result : MixedLMResults
        Fitted model

    Returns
    -------
    pd.DataFrame
        Fixed effects with columns: Term, Coef, Std_Err, z, P_value, CI_lower, CI_upper

    Examples
    --------
    >>> fe_table = extract_fixed_effects(fitted_model)
    >>> print(fe_table)
    """
    # Get fixed effects summary table
    fe_summary = result.summary().tables[1]

    # Check if it's already a DataFrame or needs conversion
    if isinstance(fe_summary, pd.DataFrame):
        fe_df = fe_summary.copy()
        # Reset index to make term names a column
        fe_df = fe_df.reset_index()
        fe_df.columns = ['Term', 'Coef', 'Std_Err', 'z', 'P_value', 'CI_lower', 'CI_upper']
    else:
        # SimpleTable object - extract data
        fe_df = pd.DataFrame(fe_summary.data[1:], columns=fe_summary.data[0])
        fe_df.columns = ['Term', 'Coef', 'Std_Err', 'z', 'P_value', 'CI_lower', 'CI_upper']

    # Convert numeric columns
    numeric_cols = ['Coef', 'Std_Err', 'z', 'P_value', 'CI_lower', 'CI_upper']
    for col in numeric_cols:
        fe_df[col] = pd.to_numeric(fe_df[col], errors='coerce')

    return fe_df


def extract_random_effects(result: MixedLMResults) -> Dict:
    """
    Extract random effects variances and ICC.

    Parameters
    ----------
    result : MixedLMResults
        Fitted model

    Returns
    -------
    dict
        Random effects summary with keys:
        - 're_variance' : dict, variance components
        - 'residual_variance' : float
        - 'icc' : float, intraclass correlation

    Examples
    --------
    >>> re_summary = extract_random_effects(fitted_model)
    >>> print(re_summary['icc'])
    """
    # Random effects variance-covariance matrix
    re_cov = result.cov_re

    # Residual variance
    residual_var = result.scale

    # ICC (intraclass correlation)
    # ICC = var(u0) / (var(u0) + var(residual))
    if re_cov.shape[0] > 0:
        u0_variance = re_cov.iloc[0, 0] if isinstance(re_cov, pd.DataFrame) else re_cov[0, 0]
        icc = u0_variance / (u0_variance + residual_var)
    else:
        icc = 0.0

    return {
        're_variance': re_cov,
        'residual_variance': residual_var,
        'icc': icc
    }


# ============================================================================
# FULL PIPELINE
# ============================================================================

def run_lmm_analysis(
    theta_scores: pd.DataFrame,
    output_dir: Union[str, Path],
    n_factors: int,
    reference_group: Optional[str] = None,
    save_models: bool = True
) -> Dict:
    """
    Complete LMM analysis pipeline.

    Steps:
    1. Prepare data (wide to long)
    2. Fit candidate models
    3. Compare via AIC
    4. Extract fixed/random effects from best model
    5. Save results

    Parameters
    ----------
    theta_scores : pd.DataFrame
        Wide-format theta scores (UID, test, Theta_*)

    output_dir : str or Path
        Directory to save outputs

    n_factors : int
        Number of factors in analysis

    reference_group : str, optional
        Reference level for Factor

    save_models : bool, default True
        Save fitted model .pkl files?

    Returns
    -------
    dict
        Complete results with keys:
        - 'df_long' : Long-format data
        - 'best_model_name' : Best model by AIC
        - 'best_model' : Fitted MixedLMResults
        - 'aic_comparison' : AIC comparison table
        - 'fixed_effects' : Fixed effects table
        - 'random_effects' : Random effects summary

    Examples
    --------
    >>> results = run_lmm_analysis(
    ...     theta_scores=df_theta,
    ...     output_dir='results/ch5/rq1/lmm/',
    ...     n_factors=3,
    ...     reference_group='What'
    ... )
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("LMM ANALYSIS PIPELINE")
    print("=" * 60)

    # Step 1: Prepare data
    print("\n[1/5] Preparing data (wide to long format)...")
    df_long = prepare_lmm_data(theta_scores)
    print(f"  Data shape: {df_long.shape}")
    print(f"  Factors: {df_long['Factor'].unique().tolist()}")

    # Save long-format data
    df_long.to_csv(output_dir / 'lmm_data_long.csv', index=False)
    print(f"  Saved: {output_dir / 'lmm_data_long.csv'}")

    # Step 2-3: Fit and compare models
    print("\n[2/5] Fitting candidate models and comparing via AIC...")
    save_dir = output_dir if save_models else None
    comparison_results = compare_models(
        data=df_long,
        n_factors=n_factors,
        reference_group=reference_group,
        save_dir=save_dir
    )

    best_model_name = comparison_results['best_model_name']
    best_model = comparison_results['best_model']
    aic_df = comparison_results['aic_comparison']

    print(f"\n  Best model: {best_model_name}")
    print(f"  AIC: {best_model.aic:.2f}")

    # Save AIC comparison
    aic_df.to_csv(output_dir / 'aic_comparison.csv', index=False)
    print(f"  Saved: {output_dir / 'aic_comparison.csv'}")

    # Step 4: Extract fixed effects
    print("\n[3/5] Extracting fixed effects...")
    fe_table = extract_fixed_effects(best_model)
    fe_table.to_csv(output_dir / 'fixed_effects.csv', index=False)
    print(f"  Saved: {output_dir / 'fixed_effects.csv'}")

    # Step 5: Extract random effects
    print("\n[4/5] Extracting random effects...")
    re_summary = extract_random_effects(best_model)
    print(f"  ICC = {re_summary['icc']:.3f}")

    # Save random effects summary
    with open(output_dir / 'random_effects.txt', 'w') as f:
        f.write("RANDOM EFFECTS SUMMARY\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Residual Variance: {re_summary['residual_variance']:.4f}\n")
        f.write(f"ICC (Intraclass Correlation): {re_summary['icc']:.4f}\n\n")
        f.write("Random Effects Covariance Matrix:\n")
        f.write(str(re_summary['re_variance']))

    # Step 6: Save model summary
    print("\n[5/5] Saving model summary...")
    with open(output_dir / 'model_summary.txt', 'w') as f:
        f.write("=" * 60 + "\n")
        f.write(f"BEST MODEL: {best_model_name}\n")
        f.write("=" * 60 + "\n\n")
        f.write(best_model.summary().as_text())
        f.write("\n\n" + "=" * 60 + "\n")
        f.write("AIC COMPARISON\n")
        f.write("=" * 60 + "\n\n")
        f.write(aic_df.to_string(index=False))

    print(f"  Saved: {output_dir / 'model_summary.txt'}")

    print("\n" + "=" * 60)
    print("LMM ANALYSIS COMPLETE")
    print("=" * 60 + "\n")

    return {
        'df_long': df_long,
        'best_model_name': best_model_name,
        'best_model': best_model,
        'aic_comparison': aic_df,
        'fixed_effects': fe_table,
        'random_effects': re_summary
    }


def post_hoc_contrasts(
    lmm_result,
    comparisons: List[str],
    family_alpha: float = 0.05
) -> pd.DataFrame:
    """
    Compute post-hoc pairwise contrasts with dual reporting (Decision D068).

    Implements dual reporting of p-values:
    - Uncorrected (α = 0.05)
    - Bonferroni-corrected (α_corrected = family_alpha / k)

    where k = number of comparisons in this RQ.

    Args:
        lmm_result: Fitted MixedLM result object
        comparisons: List of comparison strings, e.g., ["Where-What", "When-What"]
        family_alpha: Family-wise alpha level (default: 0.05)

    Returns:
        DataFrame with columns:
        - comparison: Comparison label
        - beta: Estimated effect size
        - se: Standard error
        - z: z-statistic
        - p_uncorrected: Uncorrected p-value
        - alpha_corrected: Bonferroni-corrected alpha threshold
        - p_corrected: Corrected p-value (p * k)
        - sig_uncorrected: Significant at α=0.05 (bool)
        - sig_corrected: Significant at α_corrected (bool)

    Example:
        ```python
        comparisons = ["Where-What", "When-What", "When-Where"]
        df_contrasts = post_hoc_contrasts(result, comparisons, family_alpha=0.05)
        ```

    Decision D068 Context:
        Exploratory thesis requires reporting BOTH uncorrected and corrected results.
        - Uncorrected: Shows raw effects (transparency)
        - Corrected: Controls Type I error (rigor)
        Reviewers can assess robustness across both thresholds.
    """
    print("\n" + "=" * 60)
    print("POST-HOC PAIRWISE CONTRASTS (Decision D068)")
    print("=" * 60)

    k = len(comparisons)
    alpha_corrected = family_alpha / k

    print(f"Family-wise alpha: {family_alpha}")
    print(f"Number of comparisons: {k}")
    print(f"Bonferroni-corrected alpha: {alpha_corrected:.4f}")

    results = []

    for comparison in comparisons:
        # Parse comparison string (e.g., "Where-What" → Where - What)
        parts = comparison.split('-')
        if len(parts) != 2:
            raise ValueError(f"Invalid comparison format: {comparison}. Expected 'A-B'")

        level1, level2 = parts[0].strip(), parts[1].strip()

        # Try to extract coefficient from model
        # Treatment coding: level1 coefficient represents level1 - reference
        # So Where-What means C(Domain, Treatment)[T.Where]
        coef_name_options = [
            f'C(Domain, Treatment)[T.{level1}]',
            f'C(Domain)[T.{level1}]',
            f'Domain[T.{level1}]',
            level1
        ]

        coef_name = None
        for option in coef_name_options:
            if option in lmm_result.params.index:
                coef_name = option
                break

        if coef_name is None:
            print(f"  Warning: Coefficient for '{level1}' not found. Skipping {comparison}.")
            continue

        # Extract parameters
        beta = lmm_result.params[coef_name]
        se = lmm_result.bse[coef_name]
        z = beta / se
        p_uncorrected = lmm_result.pvalues[coef_name]
        p_corrected = min(p_uncorrected * k, 1.0)  # Cap at 1.0

        # Significance flags
        sig_uncorrected = p_uncorrected < 0.05
        sig_corrected = p_uncorrected < alpha_corrected

        results.append({
            'comparison': comparison,
            'beta': beta,
            'se': se,
            'z': z,
            'p_uncorrected': p_uncorrected,
            'alpha_corrected': alpha_corrected,
            'p_corrected': p_corrected,
            'sig_uncorrected': sig_uncorrected,
            'sig_corrected': sig_corrected
        })

    df_contrasts = pd.DataFrame(results)

    # Summary
    print(f"\nResults:")
    print(f"  Significant (uncorrected α=0.05): {df_contrasts['sig_uncorrected'].sum()}/{k}")
    print(f"  Significant (corrected α={alpha_corrected:.4f}): {df_contrasts['sig_corrected'].sum()}/{k}")

    print("=" * 60 + "\n")

    return df_contrasts


def compute_effect_sizes(
    lmm_result,
    include_interactions: bool = False
) -> pd.DataFrame:
    """
    Compute effect sizes (Cohen's f²) for LMM fixed effects.

    Args:
        lmm_result: Fitted MixedLM result object
        include_interactions: Whether to include interaction terms (default: False)

    Returns:
        DataFrame with columns:
        - effect: Effect name
        - f_squared: Cohen's f² effect size
        - interpretation: Small/Medium/Large based on Cohen 1988 thresholds

    Cohen 1988 Thresholds:
        - Small: f² >= 0.02
        - Medium: f² >= 0.15
        - Large: f² >= 0.35

    Example:
        ```python
        df_effect_sizes = compute_effect_sizes(result, include_interactions=True)
        ```

    Note:
        This is a simplified approximation using (β/SE)² / N.
        Proper implementation would require nested model comparison (future enhancement).
    """
    print("\n" + "=" * 60)
    print("EFFECT SIZES (Cohen's f²)")
    print("=" * 60)

    results = []

    # Extract fixed effects (exclude Intercept and Group Var)
    for param_name in lmm_result.params.index:
        # Skip intercept
        if param_name == 'Intercept':
            continue

        # Skip Group Var (random effects variance)
        if 'Group' in param_name or 'Var' in param_name:
            continue

        # Skip interactions if not requested
        if not include_interactions and ':' in param_name:
            continue

        beta = lmm_result.params[param_name]
        se = lmm_result.bse[param_name]

        # Simplified f² approximation
        n = lmm_result.nobs
        f_squared = (beta / se) ** 2 / n

        # Interpret using Cohen 1988 thresholds
        if f_squared < 0.02:
            interpretation = 'negligible'
        elif f_squared < 0.15:
            interpretation = 'small'
        elif f_squared < 0.35:
            interpretation = 'medium'
        else:
            interpretation = 'large'

        results.append({
            'effect': param_name,
            'f_squared': f_squared,
            'interpretation': interpretation
        })

    df_effect_sizes = pd.DataFrame(results)

    # Summary
    print(f"\nEffect sizes computed for {len(df_effect_sizes)} fixed effects")
    print(f"  Negligible (f²<0.02): {(df_effect_sizes['interpretation']=='negligible').sum()}")
    print(f"  Small (0.02≤f²<0.15): {(df_effect_sizes['interpretation']=='small').sum()}")
    print(f"  Medium (0.15≤f²<0.35): {(df_effect_sizes['interpretation']=='medium').sum()}")
    print(f"  Large (f²≥0.35): {(df_effect_sizes['interpretation']=='large').sum()}")

    print("=" * 60 + "\n")

    return df_effect_sizes


# ============================================================================
# MODULE EXPORTS
# ============================================================================

def fit_lmm_with_tsvr(
    theta_scores: pd.DataFrame,
    tsvr_data: pd.DataFrame,
    formula: str,
    groups: str = 'UID',
    re_formula: str = '~Days',
    reml: bool = False
) -> MixedLMResults:
    """
    Fit LMM using TSVR as time variable (Decision D070).

    Implements the IRT→LMM pipeline with TSVR instead of nominal days:
    1. Parse composite_ID to extract [UID, Test]
    2. Merge theta scores with TSVR data
    3. Convert TSVR hours → days
    4. Reshape to long format for LMM
    5. Fit model using actual time delays

    Args:
        theta_scores: DataFrame from IRT Pass 2
                      Columns: composite_ID, domain_name (e.g., "What", "Where", "When"), theta
        tsvr_data: DataFrame from data-prep
                   Columns: composite_ID, test, tsvr (hours)
        formula: LMM formula string (e.g., "Theta ~ Days + C(Domain)")
        groups: Grouping variable (default: 'UID')
        re_formula: Random effects formula (default: '~Days')
        reml: Use REML estimation (default: False for AIC comparison)

    Returns:
        Fitted MixedLMResults object

    Example:
        ```python
        # Load data
        theta_scores = pd.read_csv("data/pass2_theta.csv")
        tsvr_data = pd.read_csv("data/tsvr_data.csv")

        # Fit model
        result = fit_lmm_with_tsvr(
            theta_scores=theta_scores,
            tsvr_data=tsvr_data,
            formula="Theta ~ Days + C(Domain) + Days:C(Domain)",
            groups='UID',
            re_formula='~Days'
        )
        ```

    Decision D070 Context:
        Nominal days (0, 1, 3, 6) introduce measurement error because actual delays vary:
        - T1: 0.3-2.5h (not exactly 0 days)
        - T2: 20-32h (not exactly 1 day)
        - T3: 68-80h (not exactly 3 days)
        - T4: 140-156h (not exactly 6 days)

        Using TSVR (Time Since VR encoding) prevents biased slope estimates and
        reduced statistical power across ~40 RQs.
    """
    print("\n" + "=" * 60)
    print("LMM WITH TSVR TIME VARIABLE (Decision D070)")
    print("=" * 60)

    # Step 1: Parse composite_ID to extract UID and Test
    print("\n[1/5] Parsing composite_IDs...")

    # Theta scores: Parse composite_ID (e.g., "A010_T1" → UID="A010", Test="T1")
    theta_scores = theta_scores.copy()
    theta_scores[['UID', 'Test']] = theta_scores['composite_ID'].str.split('_', n=1, expand=True)

    # TSVR data: Ensure Test is string format (e.g., "T1", "T2", "T3", "T4")
    tsvr_data = tsvr_data.copy()
    test_col = 'test' if 'test' in tsvr_data.columns else 'Test'
    if tsvr_data[test_col].dtype in [int, float]:
        tsvr_data['Test'] = 'T' + tsvr_data[test_col].astype(int).astype(str)
    else:
        tsvr_data['Test'] = tsvr_data[test_col]

    # Create composite_ID from UID and Test if not already present
    if 'composite_ID' not in tsvr_data.columns:
        tsvr_data['UID'] = tsvr_data['UID'].astype(str)
        tsvr_data['composite_ID'] = tsvr_data['UID'] + '_' + tsvr_data['Test']

    # Handle TSVR column name (could be 'tsvr' or 'TSVR_hours')
    tsvr_col = 'tsvr' if 'tsvr' in tsvr_data.columns else 'TSVR_hours'
    if tsvr_col != 'tsvr':
        tsvr_data['tsvr'] = tsvr_data[tsvr_col]

    print(f"  Theta scores: {len(theta_scores)} rows")
    print(f"  TSVR data: {len(tsvr_data)} rows")

    # Step 2: Merge theta scores with TSVR
    print("\n[2/5] Merging theta scores with TSVR data...")

    # Merge on composite_ID
    merged = theta_scores.merge(
        tsvr_data[['composite_ID', 'tsvr']],
        on='composite_ID',
        how='left'
    )

    # Check for missing TSVR
    missing_tsvr = merged['tsvr'].isna().sum()
    if missing_tsvr > 0:
        print(f"  WARNING: {missing_tsvr} rows missing TSVR data ({missing_tsvr/len(merged)*100:.1f}%)")
    else:
        print(f"  ✓ All {len(merged)} rows have TSVR data")

    # Step 3: Convert TSVR hours → days
    print("\n[3/5] Converting TSVR hours to days...")

    merged['Days'] = merged['tsvr'] / 24.0

    print(f"  TSVR range: {merged['tsvr'].min():.1f}h - {merged['tsvr'].max():.1f}h")
    print(f"  Days range: {merged['Days'].min():.2f} - {merged['Days'].max():.2f} days")

    # Step 4: Prepare long format for LMM
    print("\n[4/5] Preparing long-format data for LMM...")

    # Ensure required columns exist
    if 'domain_name' in merged.columns:
        merged['Domain'] = merged['domain_name']
    elif 'factor' in merged.columns:
        merged['Domain'] = merged['factor']
    else:
        # If no domain column, assume single domain
        merged['Domain'] = 'Memory'

    # Rename theta column if needed
    if 'theta' in merged.columns:
        merged['Theta'] = merged['theta']

    # Create clean LMM dataset
    lmm_data = merged[['UID', 'Test', 'Domain', 'Theta', 'Days']].copy()

    print(f"  LMM data shape: {lmm_data.shape}")
    print(f"  Unique UIDs: {lmm_data['UID'].nunique()}")
    print(f"  Unique Domains: {lmm_data['Domain'].nunique()} ({sorted(lmm_data['Domain'].unique())})")

    # Step 5: Fit LMM
    print("\n[5/5] Fitting Linear Mixed Model...")
    print(f"  Formula: {formula}")
    print(f"  Random effects: {re_formula}")
    print(f"  Grouping: {groups}")

    result = fit_lmm_model(
        data=lmm_data,
        formula=formula,
        groups=groups,
        re_formula=re_formula,
        reml=reml
    )

    print("\n" + "=" * 60)
    print("LMM FIT COMPLETE")
    print("=" * 60)
    print(f"Log-Likelihood: {result.llf:.2f}")
    print(f"AIC: {result.aic:.2f}")
    print(f"BIC: {result.bic:.2f}")
    print()

    return result


__all__ = [
    'prepare_lmm_data',
    'configure_candidate_models',
    'fit_lmm_model',
    'compare_models',
    'extract_fixed_effects',
    'extract_random_effects',
    'run_lmm_analysis',
    'post_hoc_contrasts',
    'compute_effect_sizes',
    'fit_lmm_with_tsvr'
]
