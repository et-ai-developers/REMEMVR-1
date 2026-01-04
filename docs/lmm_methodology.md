# LMM Methodology Reference

**Last Updated:** 2025-12-13
**Purpose:** Document Linear Mixed Model (LMM) methodology for REMEMVR thesis analysis

---

## Overview

This document specifies the LMM methodology used for longitudinal trajectory analysis in Chapters 5-7 of the REMEMVR thesis. The approach follows Burnham & Anderson (2002) multi-model inference principles.

---

## Model Averaging Procedure

### Background

When analyzing forgetting trajectories, the functional form (linear, logarithmic, power law, etc.) represents a source of uncertainty. Traditional approaches select a single "best" model based on AIC, but this ignores model selection uncertainty.

**Problem:** In REMEMVR analyses, the best single model often has low Akaike weight (<30%), meaning >70% of model evidence supports other functional forms.

**Solution:** Model averaging (Burnham & Anderson, 2002) synthesizes predictions across competitive models weighted by their Akaike weights.

### Standard Procedure (Step 05b)

**1. Kitchen Sink Model Comparison (Step 05)**

Fit 65+ candidate models including:
- Linear, quadratic, cubic, polynomial combinations
- Logarithmic variants (log, log-log, log10)
- Power law with varying exponents (α = 0.1 to 1.0)
- Fractional exponents (square root, cube root, fourth root)
- Trigonometric (sin, cos, tanh)
- Combined forms (Lin+Log, Quad+Log, PowerLaw+Log, etc.)

**2. Identify Competitive Models (ΔAIC < 7)**

Following Burnham & Anderson (2002):
- ΔAIC < 2: Substantial support
- ΔAIC 2-4: Moderate support
- ΔAIC 4-7: Weak support
- ΔAIC > 7: Essentially no support

Threshold: ΔAIC < 7 (conservative, includes all models with non-negligible support)

**3. Compute Renormalized Weights**

```python
# Within competitive set only
renorm_weight = akaike_weight / sum(competitive_akaike_weights)
```

**4. Compute Effective Number of Models**

Shannon entropy-based measure:
```python
effective_n = exp(-sum(weights * log(weights)))
```

Interpretation:
- Effective N ≈ 1: One model dominates
- Effective N >> 1: Weight distributed across many models (high uncertainty)

**5. Fit Competitive Models with Random Effects**

For each competitive model:
1. Create time transformation (log, power law, etc.)
2. Fit LMM with random intercepts (and slopes if required)
3. Extract fitted values, random effects

**6. Compute Model-Averaged Outputs**

Weighted averages using renormalized Akaike weights:
```python
ma_prediction = sum(weight_i * prediction_i)
ma_random_intercept = sum(weight_i * intercept_i)
ma_random_slope = sum(weight_i * slope_i)  # if applicable
```

### Output Files (Step 05b)

| File | Contents |
|------|----------|
| `step05b_competitive_models.csv` | Models with ΔAIC < 7, renormalized weights |
| `step05b_model_averaged_predictions.csv` | MA fitted values for each observation |
| `step05b_model_averaged_theta.csv` | MA theta scores for derivative RQs |
| `step05b_model_averaged_random_effects.csv` | MA intercepts and slopes per participant |
| `step05b_metadata.csv` | Summary: effective_n, top_model, uncertainty level |

### Uncertainty Classification

| Effective N | Classification | Interpretation |
|-------------|----------------|----------------|
| < 2 | LOW | One model clearly dominates |
| 2-5 | MODERATE | 2-5 models competitive |
| 5-20 | HIGH | Many models competitive, substantial uncertainty |
| > 20 | EXTREME | No clear functional form, maximum uncertainty |

---

## Application to REMEMVR RQs

### Chapter 5 (Accuracy Trajectories)

**RQ 5.1.1 - Functional Form:**
- Competitive models: 51 (ΔAIC < 7)
- Effective N: 40.09 (EXTREME)
- Top model: PowerLaw_04 (5.6% weight)
- Effective α: 0.41 (power law family dominates)

### Chapter 6 (Confidence Trajectories)

| RQ | Competitive Models | Effective N | Classification | Top Model |
|----|-------------------|-------------|----------------|-----------|
| 6.8.1 | 51 | 43.4 | EXTREME | Sin+Cos (2.0%) |
| 6.1.1 | 48 | 31.1 | EXTREME | Sin+Cos (21.7%) |
| 6.3.1 | 4 | 2.4 | LOW | Ultimate (55.6%) |
| 6.4.1 | 2 | 2.0 | LOW | Linear (50%) |
| 6.5.1 | 2 | 1.8 | LOW | Quad+Log+SquareRoot (65%) |

**Key Finding:** Confidence trajectories show HIGHER model uncertainty than accuracy (Effective N: 31-43 vs expected 5-15).

---

## Random Effects for ICC Decomposition

### When Random Slopes are Required

- ICC analyses (e.g., RQ 6.1.4) require random slope variance estimates
- Model-averaged random slopes provide robust ICC decomposition
- Individual trajectory heterogeneity captured across model uncertainty

### Procedure

1. Fit each competitive model with `(1 + time_var | UID)` random effects
2. Extract random intercept SD and random slope SD
3. Compute weighted average:
   ```python
   ma_intercept_sd = sum(weight_i * intercept_sd_i)
   ma_slope_sd = sum(weight_i * slope_sd_i)
   ```
4. Use MA estimates for ICC computation

---

## Implementation

### Tool Location

```
tools/model_averaging.py
```

### Key Functions

- `identify_competitive_models()` - Filter by ΔAIC threshold
- `compute_model_averaged_predictions()` - MA fitted values
- `compute_model_averaged_random_effects()` - MA intercepts/slopes
- `run_model_averaging_pipeline()` - Complete workflow

### Standard Invocation

```python
from tools.model_averaging import run_model_averaging_pipeline

results = run_model_averaging_pipeline(
    data=lmm_input,
    comparison=comparison_df,
    outcome_var='theta',
    tsvr_var='TSVR_hours',
    groups_var='UID',
    delta_aic_threshold=7.0,
    include_random_effects=True,
    include_random_slopes=True,  # For ICC RQs
    output_dir=RQ_DIR / 'data'
)
```

---

## References

- Burnham, K. P., & Anderson, D. R. (2002). *Model Selection and Multimodel Inference: A Practical Information-Theoretic Approach* (2nd ed.). Springer.
- Wixted, J. T., & Ebbesen, E. B. (1991). On the form of forgetting. *Psychological Science, 2*(6), 409-415.
- Wagenmakers, E. J., & Farrell, S. (2004). AIC model selection using Akaike weights. *Psychonomic Bulletin & Review, 11*(1), 192-196.

---

## Model Completeness Check (MANDATORY)

**Discovery (2025-12-08):** RQ 5.1.1 originally tested only 5 basic models and selected Logarithmic as best. Extended testing (17+ models) revealed power law models dominate (ΔAIC=2.97, evidence ratio 4.4:1 favoring power law over log).

### When Starting LMM Trajectory Analysis

**ALWAYS verify the model suite includes power law variants:**

| Model | Formula | Required |
|-------|---------|----------|
| PowerLaw_Alpha03 | `(t+1)^(-0.3)` | YES |
| PowerLaw_Alpha05 | `(t+1)^(-0.5)` | YES |
| PowerLaw_Alpha07 | `(t+1)^(-0.7)` | YES |
| PowerLaw_LogLog | `log(log(t+1)+1)` | YES |
| SquareRoot | `sqrt(t)` | YES |
| CubeRoot | `t^(1/3)` | YES |

**Minimum requirement:** 17 models including all power law variants above.

**Current standard:** 65+ models (kitchen sink approach) - see Step 05 procedure.

### Time Transformations

```python
lmm_input['log_log_Days'] = np.log(lmm_input['log_Days'] + 1)
lmm_input['sqrt_Days'] = np.sqrt(lmm_input['Days'])
lmm_input['cbrt_Days'] = np.cbrt(lmm_input['Days'])
lmm_input['recip_Days'] = 1.0 / (lmm_input['Days'] + 1)
lmm_input['Days_pow_neg05'] = (lmm_input['Days'] + 1) ** (-0.5)
lmm_input['Days_pow_neg03'] = (lmm_input['Days'] + 1) ** (-0.3)
lmm_input['Days_pow_neg07'] = (lmm_input['Days'] + 1) ** (-0.7)
```

### If Only Basic Models Were Tested

If you find an RQ only tested 5-7 basic models (Linear, Quadratic, Log, combinations):

1. **STOP** - Do not proceed with interpretation
2. **ALERT** user that power law variants are missing
3. Run extended model comparison before finalizing

---

## Version History

| Date | Changes |
|------|---------|
| 2025-12-13 | Initial documentation of model averaging procedure |
| 2025-12-13 | Added Ch5 5.1.1 and Ch6 ROOT RQ results |
| 2026-01-04 | Added Model Completeness Check section (from CLAUDE.md consolidation) |
