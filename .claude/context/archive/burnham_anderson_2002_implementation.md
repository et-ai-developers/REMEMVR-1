# Burnham & Anderson (2002) Model Averaging - Implementation Details

This archive documents the implementation of Burnham & Anderson (2002) model averaging methodology as applied to Chapter 6 LMM kitchen sink comparisons, including formulas, thresholds, and design decisions.

---

## Burnham & Anderson (2002) Implementation (2025-12-13 14:30)

**Archived from:** state.md Session (2025-12-13 14:30)
**Original Date:** 2025-12-13 14:30
**Reason:** Session 3+ old, archiving to topic-based storage per context-manager protocol

### Reference

**Full Citation:**
Burnham, K. P., & Anderson, D. R. (2002). *Model selection and multimodel inference: A practical information-theoretic approach* (2nd ed.). Springer.

**Key Concepts Implemented:**
- ΔAIC threshold for competitive models (p. 70-71)
- Akaike weight calculation and interpretation (p. 75)
- Model-averaged predictions (p. 152)
- Unconditional variance (eq 4.9, p. 162)
- Effective number of models (p. 168)

### Implementation in tools/model_averaging.py

#### 1. Competitive Model Selection (ΔAIC < 7 Threshold)

**Function:** `identify_competitive_models()`

**Burnham & Anderson recommendation (p. 70):**
- ΔAIC < 2: Substantial evidence (model is competitive)
- ΔAIC 4-7: Considerably less support (borderline)
- ΔAIC > 10: Essentially no support (exclude)

**Our threshold: ΔAIC < 7**
- Rationale: Inclusive approach that captures "considerably less support" models
- Conservative: Better to include borderline models than arbitrarily exclude
- Results in 2-51 competitive models across Ch6 ROOT RQs

**Code:**
```python
def identify_competitive_models(aic_df, delta_aic_threshold=7.0):
    """
    Filter to competitive models (ΔAIC < threshold) and renormalize weights
    """
    best_aic = aic_df['aic'].min()
    aic_df['delta_aic'] = aic_df['aic'] - best_aic

    # Filter to competitive set
    competitive = aic_df[aic_df['delta_aic'] < delta_aic_threshold].copy()

    # Renormalize Akaike weights to sum to 1.0
    competitive['renormalized_weight'] = (
        competitive['akaike_weight'] / competitive['akaike_weight'].sum()
    )

    return competitive
```

#### 2. Akaike Weight Calculation (already in kitchen sink)

**Formula (B&A p. 75):**
```
w_i = exp(-ΔAIC_i / 2) / Σ exp(-ΔAIC_j / 2)
```

**Interpretation:**
- w_i ≈ "probability" that model i is the best model in the set
- Sum to 1.0 across candidate set
- Model with lowest AIC has highest weight

**Implementation:**
Already computed in kitchen sink step (`step05_kitchen_sink.py`), stored in `akaike_weight` column.

**Renormalization for competitive set:**
If we filter to ΔAIC < 7, original weights no longer sum to 1.0. Renormalize:
```
w_renorm = w_original / Σ(w_competitive)
```

#### 3. Model-Averaged Predictions (B&A p. 152)

**Function:** `compute_model_averaged_predictions()`

**Formula:**
```
ŷ_MA = Σ w_i * ŷ_i
```
where:
- ŷ_MA = model-averaged prediction
- w_i = renormalized Akaike weight for model i
- ŷ_i = prediction from model i

**Code:**
```python
def compute_model_averaged_predictions(lmm_input, competitive_models, lmm_fits):
    """
    Compute weighted average predictions across competitive models
    """
    ma_predictions = np.zeros(len(lmm_input))

    for idx, row in competitive_models.iterrows():
        model_name = row['model_name']
        weight = row['renormalized_weight']
        fitted = lmm_fits[model_name].fittedvalues

        ma_predictions += weight * fitted

    return ma_predictions
```

#### 4. Unconditional Variance (B&A eq 4.9, p. 162) - CRITICAL

**Formula:**
```
var_unconditional(ŷ) = Σ w_i * [var_i(ŷ) + (ŷ_i - ŷ_MA)²]
                       \_________/   \_______________/
                       conditional    model selection
                       variance       variance
```

**Interpretation:**
- **Conditional variance:** Uncertainty WITHIN model i (parameter estimation uncertainty)
- **Model selection variance:** Uncertainty BETWEEN models (functional form uncertainty)
- **Unconditional variance:** Total uncertainty accounting for both sources

**Why this matters:**
- Standard LMM output gives conditional variance only (assumes model is correct)
- When model uncertainty is high (Effective N > 30), model selection variance dominates
- Unconditional SE is larger than conditional SE
- Failing to account for model uncertainty = underestimated confidence intervals

**Code:**
```python
def compute_unconditional_variance(lmm_input, competitive_models, lmm_fits, ma_predictions):
    """
    Burnham & Anderson (2002) eq 4.9
    """
    unconditional_var = np.zeros(len(lmm_input))

    for idx, row in competitive_models.iterrows():
        model_name = row['model_name']
        weight = row['renormalized_weight']

        fitted = lmm_fits[model_name].fittedvalues
        conditional_var = lmm_fits[model_name].scale  # Residual variance

        # Model selection variance component
        model_selection_var = (fitted - ma_predictions) ** 2

        # Weighted contribution
        unconditional_var += weight * (conditional_var + model_selection_var)

    return unconditional_var
```

#### 5. Model-Averaged Random Effects (Extension)

**Not explicitly in B&A (2002), but natural extension:**

**Formula:**
```
u_i_MA = Σ w_j * u_i_j
```
where:
- u_i_MA = model-averaged random effect for participant i
- w_j = weight for model j
- u_i_j = random effect for participant i from model j

**Challenge:** Different models have different random effect structures
- Some models: random intercept only
- Some models: random intercept + slope
- Some models: different time terms (Days, log_Days, sqrt_Days)

**Solution:** `_get_primary_time_term()` function
Maps each model name to its primary time predictor for random slopes:
```python
def _get_primary_time_term(model_name):
    """Map model name to primary time predictor for random slopes"""
    if 'Linear' in model_name:
        return 'Days'
    elif 'Log' in model_name or 'Recip' in model_name:
        return 'log_Days'
    elif 'PowerLaw' in model_name:
        return 'Days_pow_neg05'  # or appropriate variant
    # ... etc
```

**Implementation:**
```python
def compute_model_averaged_random_effects(competitive_models, lmm_fits, uids):
    """
    Average random intercepts and slopes across models
    """
    n_uids = len(uids)
    ma_intercepts = np.zeros(n_uids)
    ma_slopes = np.zeros(n_uids)

    for idx, row in competitive_models.iterrows():
        model_name = row['model_name']
        weight = row['renormalized_weight']

        random_effects = lmm_fits[model_name].random_effects

        for i, uid in enumerate(uids):
            intercept = random_effects[uid]['Intercept']
            ma_intercepts[i] += weight * intercept

            # Slope if available
            time_term = _get_primary_time_term(model_name)
            if time_term in random_effects[uid]:
                slope = random_effects[uid][time_term]
                ma_slopes[i] += weight * slope

    return ma_intercepts, ma_slopes
```

#### 6. Effective Number of Models (B&A p. 168)

**Function:** `compute_effective_n()`

**Formula:**
```
N_eff = 1 / Σ w_i²
```

**Interpretation:**
- Measures dispersion of Akaike weights
- N_eff ≈ 1: Single model dominates (all weight on one model)
- N_eff ≈ K/2: Evidence dispersed across about half the models
- N_eff ≈ K: Evidence uniformly distributed (extreme uncertainty)

**Examples from Ch6:**
- 6.8.1: N_eff = 43.4 out of 51 models (highly dispersed)
- 6.1.1: N_eff = 31.1 out of 48 models (highly dispersed)
- 6.5.1: N_eff = 1.8 out of 2 models (concentrated, one dominates)

**Code:**
```python
def compute_effective_n(competitive_models):
    """
    Effective number of models (Burnham & Anderson 2002, p. 168)
    """
    weights = competitive_models['renormalized_weight'].values
    effective_n = 1.0 / np.sum(weights ** 2)
    return effective_n
```

### Design Decisions

#### Why ΔAIC < 7 instead of < 2?

**B&A recommendation:** ΔAIC < 2 for "substantial support"

**Our choice:** ΔAIC < 7 (includes "considerably less support" models)

**Rationale:**
1. Conservative: Better to include than exclude when uncertain
2. Functional form exploration: Ch6 confidence shows EXTREME uncertainty, want to see all plausible forms
3. Effective N quantifies actual influence: Models with ΔAIC = 6 have tiny weights anyway (~0.05)
4. Thesis defense: Can show we didn't arbitrarily exclude models

#### Why Not Use BIC Instead of AIC?

**BIC (Bayesian Information Criterion):** Stronger penalty for complexity

**AIC (Akaike Information Criterion):** Penalty based on information theory

**Our choice:** AIC (as per Burnham & Anderson 2002 throughout)

**Rationale:**
1. Consistency with kitchen sink (already computed AICs)
2. BIC favors simpler models more aggressively (may exclude plausible complex forms)
3. AIC standard in model averaging literature
4. Both are approximations; choice is methodological convention

#### Why Renormalize Weights?

**Original weights (kitchen sink):**
Sum to 1.0 across ALL 65-66 models tested

**After filtering to ΔAIC < 7:**
Weights of competitive models sum to 0.92-0.99 (some evidence excluded)

**Renormalization:**
Scale competitive weights to sum to 1.0

**Rationale:**
1. Model averaging requires weights sum to 1.0 (probability axiom)
2. We're saying: "Among plausible models (ΔAIC < 7), allocate evidence proportionally"
3. Excluded models (ΔAIC > 7) have essentially no support
4. Renormalization preserves relative evidence ratios

**Example:**
```
Original:
  ModelA: ΔAIC=0.0, w=0.50
  ModelB: ΔAIC=1.5, w=0.30
  ModelC: ΔAIC=2.0, w=0.15
  ModelD: ΔAIC=8.0, w=0.05  ← Exclude
  Sum = 0.95

Renormalized (ΔAIC < 7):
  ModelA: w=0.50/0.95 = 0.526
  ModelB: w=0.30/0.95 = 0.316
  ModelC: w=0.15/0.95 = 0.158
  Sum = 1.000
```

### Limitations and Future Directions

**Current implementation limitations:**

1. **Random slopes mapping:** `_get_primary_time_term()` uses heuristics to map model names to time predictors. Complex models (e.g., Sin+Cos) may not have obvious "primary" term.

2. **Unconditional variance:** Simplified implementation assumes constant residual variance. B&A eq 4.9 fully accounts for heteroscedasticity.

3. **Convergence filtering:** Non-converged models excluded automatically. Could investigate why some models didn't converge.

**Potential extensions:**

1. **Cross-validation:** Use CV to validate that model-averaged predictions generalize better than single-best

2. **Confidence intervals:** Use unconditional SE to compute 95% CIs for predictions/effects

3. **Evidence ratios:** Report evidence ratios (w_i / w_j) for key models to quantify relative support

---
