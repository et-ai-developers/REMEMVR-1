"""
Model Averaging for LMM Trajectory Analysis

Implements Burnham & Anderson (2002) multi-model inference approach.
When best model has low Akaike weight (<30%), model averaging provides
more robust predictions accounting for model selection uncertainty.

Author: REMEMVR Team
Date: 2025-12-08
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
import statsmodels.formula.api as smf


def compute_model_averaged_predictions(
    data: pd.DataFrame,
    comparison: pd.DataFrame,
    outcome_var: str,
    tsvr_var: str,
    groups_var: str,
    delta_aic_threshold: float = 2.0,
    prediction_grid: pd.DataFrame = None,
    reml: bool = False,
) -> Dict:
    """
    Compute model-averaged predictions using Akaike weights.
    
    Parameters
    ----------
    data : DataFrame
        Training data with all time transformations
    comparison : DataFrame
        Model comparison table from kitchen_sink (has model_name, akaike_weight)
    outcome_var : str
        Outcome variable name (e.g., 'theta')
    tsvr_var : str
        Continuous TSVR variable (e.g., 'TSVR_hours')
    groups_var : str
        Grouping variable for random effects (e.g., 'UID')
    delta_aic_threshold : float
        Only average models with ΔAIC < threshold (default=2.0)
    prediction_grid : DataFrame, optional
        New data for predictions. If None, uses training data.
    reml : bool
        Use REML (True) or ML (False) for final fits
        
    Returns
    -------
    dict
        {
            'averaged_predictions': Series with model-averaged predictions,
            'models_used': list of model names included,
            'weights_normalized': dict of renormalized weights,
            'prediction_variance': Series with prediction uncertainty,
            'effective_n_models': float (effective number of models),
        }
    """
    
    print("[MODEL AVERAGING] Starting multi-model inference...")
    
    # Filter to competitive models
    competitive = comparison[comparison['delta_AIC'] < delta_aic_threshold].copy()
    print(f"  Competitive models (ΔAIC < {delta_aic_threshold}): {len(competitive)}")
    
    if len(competitive) == 0:
        raise ValueError(f"No models with ΔAIC < {delta_aic_threshold}")
    
    # Renormalize weights (sum competitive weights to 1.0)
    competitive['weight_normalized'] = (
        competitive['akaike_weight'] / competitive['akaike_weight'].sum()
    )
    
    print(f"  Total weight of competitive set: {competitive['akaike_weight'].sum():.1%}")
    print(f"  Renormalized to 100% across {len(competitive)} models")
    
    # Create time transformations
    data_trans = _create_transformations(data, tsvr_var)
    if prediction_grid is not None:
        pred_trans = _create_transformations(prediction_grid, tsvr_var)
    else:
        pred_trans = data_trans
    
    # Fit models and collect predictions
    predictions_matrix = []
    weights = []
    model_names = []
    
    for idx, row in competitive.iterrows():
        model_name = row['model_name']
        weight = row['weight_normalized']
        
        try:
            # Get formula for this model
            formula = _build_formula(model_name, outcome_var, data_trans)
            
            # Fit model
            model = smf.mixedlm(formula, data_trans, groups=data_trans[groups_var])
            fitted = model.fit(reml=reml, method='powell')
            
            # Get predictions
            preds = fitted.predict(pred_trans)
            
            predictions_matrix.append(preds.values)
            weights.append(weight)
            model_names.append(model_name)
            
            print(f"    [{idx+1}/{len(competitive)}] {model_name:20s} w={weight:.4f} ✓")
            
        except Exception as e:
            print(f"    [{idx+1}/{len(competitive)}] {model_name:20s} FAILED: {e}")
            continue
    
    if len(predictions_matrix) == 0:
        raise ValueError("All models failed to fit")
    
    # Convert to array
    predictions_matrix = np.array(predictions_matrix)  # (n_models, n_obs)
    weights = np.array(weights)
    
    # Renormalize weights (some models may have failed)
    weights = weights / weights.sum()
    
    # Compute model-averaged predictions
    averaged = np.average(predictions_matrix, axis=0, weights=weights)
    
    # Compute prediction variance (unconditional variance)
    # Var(avg) = E[Var(Y|model)] + Var(E[Y|model])
    # First term: within-model variance (ignore for now, constant SE)
    # Second term: between-model variance
    model_means = predictions_matrix
    grand_mean = averaged
    between_var = np.average((model_means - grand_mean[np.newaxis, :])**2, 
                             axis=0, weights=weights)
    
    # Effective number of models (Shannon diversity)
    effective_n = np.exp(-np.sum(weights * np.log(weights + 1e-10)))
    
    print(f"\n[RESULTS] Model averaging complete:")
    print(f"  Models used: {len(model_names)}/{len(competitive)}")
    print(f"  Effective N models: {effective_n:.2f}")
    print(f"  Prediction variance range: [{np.min(between_var):.4f}, {np.max(between_var):.4f}]")
    
    return {
        'averaged_predictions': pd.Series(averaged, index=pred_trans.index),
        'models_used': model_names,
        'weights_normalized': dict(zip(model_names, weights)),
        'prediction_variance': pd.Series(between_var, index=pred_trans.index),
        'effective_n_models': effective_n,
    }


def _create_transformations(df: pd.DataFrame, tsvr_var: str) -> pd.DataFrame:
    """Create all time transformations needed for model averaging."""
    df = df.copy()
    
    # Convert TSVR_hours to days
    df['TSVR'] = df[tsvr_var] / 24.0
    
    # Polynomial
    df['TSVR_sq'] = df['TSVR'] ** 2
    df['TSVR_cub'] = df['TSVR'] ** 3
    df['TSVR_4th'] = df['TSVR'] ** 4
    
    # Logarithmic
    df['log_TSVR'] = np.log(df['TSVR'] + 1)
    df['log2_TSVR'] = np.log2(df['TSVR'] + 1)
    df['log10_TSVR'] = np.log10(df['TSVR'] + 1)
    df['log_log_TSVR'] = np.log(df['log_TSVR'] + 1)
    
    # Power law
    for alpha in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        col_name = f'TSVR_pow_neg{int(alpha*10):02d}'
        df[col_name] = (df['TSVR'] + 1) ** (-alpha)
    
    # Roots
    df['sqrt_TSVR'] = np.sqrt(df['TSVR'])
    df['cbrt_TSVR'] = np.cbrt(df['TSVR'])
    df['TSVR_pow_025'] = df['TSVR'] ** 0.25
    df['TSVR_pow_033'] = df['TSVR'] ** 0.333
    df['TSVR_pow_067'] = df['TSVR'] ** 0.667
    
    # Reciprocal
    df['recip_TSVR'] = 1.0 / (df['TSVR'] + 1)
    df['recip_TSVR_sq'] = 1.0 / ((df['TSVR'] + 1) ** 2)
    
    # Exponential proxies
    df['neg_TSVR'] = -df['TSVR']
    df['neg_TSVR_sq'] = -(df['TSVR'] ** 2)
    df['neg_sqrt_TSVR'] = -np.sqrt(df['TSVR'])
    
    # Trigonometric
    tsvr_max = df['TSVR'].max()
    df['sin_TSVR'] = np.sin(df['TSVR'] / tsvr_max * 2 * np.pi)
    df['cos_TSVR'] = np.cos(df['TSVR'] / tsvr_max * 2 * np.pi)
    
    # Hyperbolic
    tsvr_norm = df['TSVR'] / tsvr_max
    df['tanh_TSVR'] = np.tanh(tsvr_norm)
    df['arctanh_TSVR'] = np.arctanh(tsvr_norm * 0.99)
    df['sinh_TSVR'] = np.sinh(tsvr_norm)
    
    return df


def _build_formula(model_name: str, outcome: str, df: pd.DataFrame) -> str:
    """Build formula for a specific model."""
    
    # Map model names to formulas (from kitchen_sink model definitions)
    formulas = {
        'Linear': 'TSVR',
        'Quadratic': 'TSVR + TSVR_sq',
        'Cubic': 'TSVR + TSVR_sq + TSVR_cub',
        'Quartic': 'TSVR + TSVR_sq + TSVR_cub + TSVR_4th',
        'Quadratic_pure': 'TSVR_sq',
        'Cubic_pure': 'TSVR_cub',
        'Log': 'log_TSVR',
        'Log2': 'log2_TSVR',
        'Log10': 'log10_TSVR',
        'LogLog': 'log_log_TSVR',
        'Lin+Log': 'TSVR + log_TSVR',
        'Quad+Log': 'TSVR + TSVR_sq + log_TSVR',
        'Log+LogLog': 'log_TSVR + log_log_TSVR',
        'Lin+Quad+Log': 'TSVR + TSVR_sq + log_TSVR',
        'PowerLaw_01': 'TSVR_pow_neg01',
        'PowerLaw_02': 'TSVR_pow_neg02',
        'PowerLaw_03': 'TSVR_pow_neg03',
        'PowerLaw_04': 'TSVR_pow_neg04',
        'PowerLaw_05': 'TSVR_pow_neg05',
        'PowerLaw_06': 'TSVR_pow_neg06',
        'PowerLaw_07': 'TSVR_pow_neg07',
        'PowerLaw_08': 'TSVR_pow_neg08',
        'PowerLaw_09': 'TSVR_pow_neg09',
        'PowerLaw_10': 'TSVR_pow_neg10',
        'PowerLaw_Log': 'TSVR_pow_neg05 + log_TSVR',
        'PowerLaw_Lin': 'TSVR_pow_neg05 + TSVR',
        'SquareRoot': 'sqrt_TSVR',
        'CubeRoot': 'cbrt_TSVR',
        'FourthRoot': 'TSVR_pow_025',
        'Root_033': 'TSVR_pow_033',
        'Root_067': 'TSVR_pow_067',
        'SquareRoot+Log': 'sqrt_TSVR + log_TSVR',
        'CubeRoot+Log': 'cbrt_TSVR + log_TSVR',
        'SquareRoot+Lin': 'sqrt_TSVR + TSVR',
        'Root_Multi': 'sqrt_TSVR + cbrt_TSVR',
        'Reciprocal': 'recip_TSVR',
        'Recip+Log': 'recip_TSVR + log_TSVR',
        'Recip+Lin': 'recip_TSVR + TSVR',
        'Recip+Quad': 'recip_TSVR + TSVR + TSVR_sq',
        'Recip_sq': 'recip_TSVR_sq',
        'Recip+PowerLaw': 'recip_TSVR + TSVR_pow_neg05',
        'Exponential_proxy': 'neg_TSVR',
        'Exp+Log': 'neg_TSVR + log_TSVR',
        'Exp+Lin': 'neg_TSVR + TSVR',
        'Exp_fast': 'neg_TSVR_sq',
        'Exp_slow': 'neg_sqrt_TSVR',
        'Exp+PowerLaw': 'neg_TSVR + TSVR_pow_neg05',
        'Exp+Recip': 'neg_TSVR + recip_TSVR',
        'Sin': 'sin_TSVR',
        'Cos': 'cos_TSVR',
        'Sin+Cos': 'sin_TSVR + cos_TSVR',
        'Sin+Log': 'sin_TSVR + log_TSVR',
        'Tanh': 'tanh_TSVR',
        'Tanh+Log': 'tanh_TSVR + log_TSVR',
        'Arctanh': 'arctanh_TSVR',
        'Sinh': 'sinh_TSVR',
        'Log+PowerLaw05': 'log_TSVR + TSVR_pow_neg05',
        'Log+SquareRoot': 'log_TSVR + sqrt_TSVR',
        'Log+Recip': 'log_TSVR + recip_TSVR',
        'SquareRoot+PowerLaw': 'sqrt_TSVR + TSVR_pow_neg05',
        'SquareRoot+Recip': 'sqrt_TSVR + recip_TSVR',
        'Recip+PowerLaw05': 'recip_TSVR + TSVR_pow_neg05',
        'Lin+Log+PowerLaw': 'TSVR + log_TSVR + TSVR_pow_neg05',
        'Quad+Log+SquareRoot': 'TSVR + TSVR_sq + log_TSVR + sqrt_TSVR',
        'PowerLaw+Recip+Log': 'TSVR_pow_neg05 + recip_TSVR + log_TSVR',
        'Ultimate': 'TSVR + TSVR_sq + log_TSVR + sqrt_TSVR + TSVR_pow_neg05 + recip_TSVR',
    }
    
    if model_name not in formulas:
        raise ValueError(f"Unknown model: {model_name}")
    
    return f"{outcome} ~ {formulas[model_name]}"
