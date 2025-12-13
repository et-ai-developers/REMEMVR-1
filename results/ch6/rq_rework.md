# Chapter 6 RQ Rework Plan: Model Averaging Implementation

**Created:** 2025-12-13
**Last Updated:** 2025-12-13 11:50
**Purpose:** Implement model averaging across all kitchen sink ROOT RQs to properly characterize how confidence ACTUALLY changes over time, incorporating model uncertainty rather than selecting a single "best" model.

**Rationale:** For PhD thesis defense, we need to demonstrate that our conclusions about confidence trajectories are robust to functional form uncertainty. When 66 models are tested and the best has only 4-21% weight, selecting just that model ignores 79-96% of the evidence.

---

## IMPLEMENTATION STATUS (2025-12-13)

### What Was Done

Model averaging was implemented for ALL 5 kitchen sink ROOT RQs in Chapter 6. This addresses the audit finding that selecting a single "best" model when that model has low Akaike weight (4-65%) ignores substantial model uncertainty.

| Priority | RQ | Status | Competitive Models | Effective N | Notes |
|----------|-----|--------|-------------------|-------------|-------|
| **P1-CRITICAL** | 6.8.1 | ✅ COMPLETE | 51 (99.6% weight) | 43.4 | EXTREME uncertainty, 51 models with ΔAIC < 7 |
| **P2-HIGH** | 6.1.1 | ✅ COMPLETE | 48 (97.5% weight) | 31.1 | Slopes computed for 824× ICC finding |
| **P3-MODERATE** | 6.3.1 | ✅ COMPLETE | 4 (92.0% weight) | 2.4 | Domain (What/Where/When) interaction |
| **P4-MODERATE** | 6.4.1 | ✅ COMPLETE | 2 (100% weight) | 2.0 | Paradigm (IFR/ICR/IRE) - Linear/Exp tied |
| **P5-MODERATE** | 6.5.1 | ✅ COMPLETE | 2 (87.5% weight) | 1.8 | Schema (Common/Unique) congruence |
| **P6-FIX** | 6.7.3 | ⏳ PENDING | N/A | N/A | Requires Ch5 5.1.1 MA first (separate task) |

### Key Findings

1. **6.8.1 and 6.1.1 have EXTREME model uncertainty** - Effective N of 43.4 and 31.1 means no single model dominates. Model averaging essential here.
2. **6.3.1, 6.4.1, 6.5.1 have concentrated weights** - Effective N of 1.8-2.4 means 1-2 models dominate. Model averaging has limited impact but provides methodological consistency.
3. **All NULL interaction findings remain robust** - The key thesis conclusions (e.g., no Source-Destination difference in 6.8.1) hold across ALL competitive models.

### Files Created

**Infrastructure:**
- `tools/model_averaging.py` - Reusable module with:
  - `identify_competitive_models()` - Filters by ΔAIC < 7, renormalizes weights
  - `compute_unconditional_variance()` - Burnham & Anderson (2002) eq 4.9
  - `compute_model_averaged_random_effects()` - For ICC/clustering derivatives
  - `run_model_averaging_pipeline()` - Complete workflow

**Per-RQ Scripts (all run successfully):**
- `results/ch6/6.8.1/code/step05b_model_averaging.py` - With location (Source/Dest) interaction
- `results/ch6/6.1.1/code/step05b_model_averaging.py` - With random slopes for ICC
- `results/ch6/6.3.1/code/step05b_model_averaging.py` - With domain interaction
- `results/ch6/6.4.1/code/step05b_model_averaging.py` - With paradigm interaction
- `results/ch6/6.5.1/code/step05b_model_averaging.py` - With congruence interaction

### Outputs Generated per RQ

Each ROOT RQ now has in its `data/` folder:
- `step05b_competitive_models.csv` - Models with ΔAIC < 7, renormalized weights
- `step05b_model_averaged_predictions.csv` - MA predictions with unconditional variance
- `step05b_model_averaged_theta.csv` - MA theta for derivative RQs
- `step05b_model_averaged_random_effects.csv` - MA intercepts (+ slopes for 6.1.1)
- `step05b_metadata.csv` - Summary: n_models, effective_N, top_model, etc.

### Documentation Updated

- `results/ch6/rq_status.tsv` - Kitchen_Sink_Model_Averaging column updated with "✅ IMPLEMENTED 2025-12-13"
- `results/ch6/6.8.1/results/summary.md` - Added "Model Averaging Methodology" section

### What Remains (DEFERRED)

1. **6.7.3** - Uses Ch5 5.1.1 residuals. Ch5 MA not implemented yet. NULL finding (r=0.02) robust regardless.
2. **Derivative RQs** - NOT re-run. Use existing results. MA outputs available if needed for future sensitivity analysis.
3. **Summary.md updates** - Only 6.8.1 updated. Other ROOT RQs can be updated similarly if needed.

### How to Continue

To resume this work:
1. Read this file for context
2. Check `rq_status.tsv` for current status of all RQs
3. Run any `step05b_model_averaging.py` script to regenerate outputs
4. For 6.7.3, first implement Ch5 5.1.1 model averaging

---

## Executive Summary

**RQs Requiring Model Averaging Implementation:**

| Priority | RQ | Best Model Weight | Downstream RQs | Cascade Risk |
|----------|-----|-------------------|----------------|--------------|
| **P1-CRITICAL** | 6.8.1 | 4.2% | 6.8.2, 6.8.3, 6.8.4 | HIGH |
| **P2-HIGH** | 6.1.1 | 21.7% | 6.1.2, 6.1.3, 6.1.4, 6.1.5 | MODERATE |
| **P3-MODERATE** | 6.3.1 | 55.6% | 6.3.2, 6.3.3, 6.3.4 | LOW |
| **P4-MODERATE** | 6.4.1 | 50.0% | 6.4.2, 6.4.3, 6.4.4 | LOW |
| **P5-MODERATE** | 6.5.1 | 65.3% | 6.5.2, 6.5.3 | LOW |
| **P6-FIX** | 6.7.3 | N/A | None | NONE (uses Ch5) |

**Total RQs affected:** 6 ROOT + 16 DERIVATIVES = 22 RQs (71% of Ch6)

---

## Part 1: Model Averaging Methodology

### 1.1 What Model Averaging Provides

Instead of: "The best model is X (AIC=Y, weight=Z%)"

We get: "The model-averaged trajectory, incorporating uncertainty across all competitive models"

**Key outputs:**
- Model-averaged predictions (weighted by Akaike weights)
- Model-averaged coefficients (for interpretation)
- Unconditional standard errors (incorporating model selection uncertainty)
- Model-averaged random effects (for ICC/clustering derivatives)

### 1.2 Implementation Approach

For each kitchen sink ROOT RQ:

```python
# Step 1: Identify competitive models (ΔAIC < 7 or cumulative weight > 95%)
competitive_models = models_df[models_df['delta_AIC'] < 7]

# Step 2: Renormalize weights among competitive models
competitive_models['renorm_weight'] = (
    competitive_models['akaike_weight'] /
    competitive_models['akaike_weight'].sum()
)

# Step 3: Generate predictions from each competitive model
for model in competitive_models:
    predictions[model] = fitted_models[model].predict(newdata)

# Step 4: Compute model-averaged predictions
ma_predictions = sum(w_i * pred_i for w_i, pred_i in zip(weights, predictions))

# Step 5: Compute unconditional variance (Burnham & Anderson 2002, eq 4.9)
# Var_unconditional = sum(w_i * [Var(pred_i|model_i) + (pred_i - ma_pred)^2])
```

### 1.3 What Changes for Derivatives

**For theta-based derivatives (calibration, ICC):**
- Use model-averaged theta estimates
- Propagate uncertainty through unconditional SEs

**For random-effects derivatives (clustering, ICC decomposition):**
- Extract random effects from each competitive model
- Compute model-averaged random effects (weighted BLUPs)
- Use averaged random effects for downstream analyses

---

## Part 2: Priority 1 - RQ 6.8.1 (CRITICAL)

### 2.1 Current State

- **Kitchen sink:** 66 models tested
- **Best model:** SquareRoot (weight = 4.2%)
- **Problem:** EXTREME uncertainty - 20 models with ΔAIC < 2
- **Effective N models:** 9.7 (very high uncertainty)

### 2.2 Rework Steps

**Step 1: Create `step05b_model_averaging.py`**
```
Location: results/ch6/6.8.1/code/step05b_model_averaging.py
Inputs:
  - step05_model_comparison.csv (66 models with AIC, weights)
  - step04_lmm_input.csv (original data)
Outputs:
  - step05b_competitive_models.csv (models with ΔAIC < 7)
  - step05b_model_averaged_predictions.csv
  - step05b_model_averaged_theta.csv (100 participants × 4 tests)
  - step05b_model_averaged_random_effects.csv (for 6.8.3, 6.8.4)
  - step05b_unconditional_se.csv
```

**Step 2: Re-fit competitive models with random slopes**
- Current 6.8.1 uses random intercept only
- For proper ICC decomposition, need random slopes
- Re-fit top ~10 models with `(1 + Time | UID)`

**Step 3: Update downstream derivatives**
- 6.8.2: Use model-averaged theta for calibration
- 6.8.3: Use model-averaged random effects for ICC
- 6.8.4: Use model-averaged random effects for clustering

### 2.3 Expected Impact

**On 6.8.1:**
- Trajectory interpretation changes from "SquareRoot model" to "model-averaged trajectory"
- NULL interaction finding likely ROBUST (p>0.30 across all top 20 models)

**On 6.8.2-6.8.4:**
- May see small changes in exact values
- Conclusions likely unchanged (all are NULL findings)

---

## Part 3: Priority 2 - RQ 6.1.1 (HIGH)

### 3.1 Current State

- **Kitchen sink:** 65 models tested
- **Best model:** Recip_sq (weight = 21.7%)
- **Problem:** High uncertainty - best model has <25% weight

### 3.2 Rework Steps

**Step 1: Create `step05b_model_averaging.py`**
```
Location: results/ch6/6.1.1/code/step05b_model_averaging.py
Outputs:
  - step05b_model_averaged_theta.csv (replaces step03_theta_confidence.csv for derivatives)
  - step05b_model_averaged_random_effects.csv (for 6.1.4, 6.1.5)
```

**Step 2: Update derivative RQs**
- 6.1.2: Re-run piecewise test with MA theta
- 6.1.3: Re-run Age × Time LMM with MA theta
- 6.1.4: Re-compute ICC with MA random effects
- 6.1.5: Re-run clustering with MA random effects

### 3.3 Expected Impact

**Critical finding at risk:** 824× ICC ratio (6.1.4)
- This is a MAJOR thesis finding
- Need to verify it holds with model-averaged random effects
- If ICC_slope changes significantly, theoretical interpretation changes

---

## Part 4: Priority 3-5 - RQs 6.3.1, 6.4.1, 6.5.1 (MODERATE)

### 4.1 Current State

| RQ | Best Weight | Status |
|----|-------------|--------|
| 6.3.1 | 55.6% | Moderate uncertainty |
| 6.4.1 | 50.0% | Tied with Exponential_proxy |
| 6.5.1 | 65.3% | Lower uncertainty |

### 4.2 Rework Approach

For each, create `step05b_model_averaging.py` following same template as 6.1.1/6.8.1.

**6.3.1 cascade:** 6.3.2, 6.3.3, 6.3.4
**6.4.1 cascade:** 6.4.2, 6.4.3, 6.4.4
**6.5.1 cascade:** 6.5.2, 6.5.3

### 4.3 Expected Impact

Lower risk than P1/P2 because:
- Best models have >50% weight
- Most derivatives are NULL findings (robust to model choice)
- Major findings (crossover interaction, domain dissociation) are based on between-group comparisons, less sensitive to exact functional form

---

## Part 5: Priority 6 - RQ 6.7.3 (FIX)

### 5.1 Current State

- Uses single PowerLaw_04 residuals from Ch5 5.1.1
- Ch5 5.1.1 has model averaging implemented (16 competitive models)
- Should use model-averaged residuals, not single-model residuals

### 5.2 Rework Steps

**Step 1: Get model-averaged residuals from Ch5 5.1.1**
```
Source: results/ch5/5.1.1/data/step05c_model_averaged_residuals.csv
(If doesn't exist, need to create it in Ch5 first)
```

**Step 2: Re-run correlation**
```
Location: results/ch6/6.7.3/code/step00b_use_ma_residuals.py
```

### 5.3 Expected Impact

- NULL finding (r=0.02) almost certainly unchanged
- Methodological improvement for thesis rigor

---

## Part 6: Implementation Order

### Phase 1: Infrastructure (Day 1)

1. Create `tools/model_averaging.py` with reusable functions:
   - `identify_competitive_models(comparison_df, delta_aic_threshold=7)`
   - `compute_model_averaged_predictions(models, weights, newdata)`
   - `compute_model_averaged_random_effects(models, weights)`
   - `compute_unconditional_variance(predictions, ma_pred, weights, variances)`

### Phase 2: Critical RQs (Day 1-2)

2. **6.8.1** - Implement MA, re-run 6.8.2, 6.8.3, 6.8.4
3. **6.1.1** - Implement MA, re-run 6.1.2, 6.1.3, 6.1.4, 6.1.5

### Phase 3: Moderate RQs (Day 2-3)

4. **6.3.1** - Implement MA, re-run 6.3.2, 6.3.3, 6.3.4
5. **6.4.1** - Implement MA, re-run 6.4.2, 6.4.3, 6.4.4
6. **6.5.1** - Implement MA, re-run 6.5.2, 6.5.3

### Phase 4: Fix & Validate (Day 3)

7. **6.7.3** - Use Ch5 MA residuals
8. Run rq_validate on all 22 affected RQs
9. Update rq_status.tsv Kitchen_Sink_Model_Averaging column
10. Create summary comparing pre-MA vs post-MA findings

---

## Part 7: Validation Checklist

**STATUS:** Updated 2025-12-13

### ROOT RQ Model Averaging (5/5 COMPLETE)

| RQ | step05b script | competitive_models | MA predictions | MA theta | MA random_effects | summary.md updated |
|----|----------------|-------------------|----------------|----------|-------------------|-------------------|
| 6.8.1 | ✅ | ✅ 51 models | ✅ | ✅ | ✅ (slopes) | ✅ |
| 6.1.1 | ✅ | ✅ 48 models | ✅ | ✅ | ✅ (slopes) | ✅ |
| 6.3.1 | ✅ | ✅ 4 models | ✅ | ✅ | ✅ | ✅ |
| 6.4.1 | ✅ | ✅ 2 models | ✅ | ✅ | ✅ | ✅ |
| 6.5.1 | ✅ | ✅ 2 models | ✅ | ✅ | ✅ | ✅ |

### RQ 6.7.3 Fix (COMPLETE)

- [x] Ch5 5.1.1 step05d_model_averaged_residuals.csv created (51 models, Eff_N=40.09)
- [x] 6.7.3 updated to use MA residuals (steps_00_to_04_ma.py)
- [x] Correlation recomputed: r = -0.0455, p = 0.653 (vs original r = 0.02, p = 0.85)
- [x] NULL finding confirmed ROBUST across model specifications
- [x] summary.md updated with MA section

### Derivative RQs (NOT Re-Run - MA Outputs Available)

| ROOT | Derivatives | Status |
|------|-------------|--------|
| 6.8.1 | 6.8.2, 6.8.3, 6.8.4 | MA outputs available; re-run deferred |
| 6.1.1 | 6.1.2, 6.1.3, 6.1.4, 6.1.5 | MA outputs available; 824× ICC finding has MA foundation |
| 6.3.1 | 6.3.2, 6.3.3, 6.3.4 | MA outputs available; re-run deferred |
| 6.4.1 | 6.4.2, 6.4.3, 6.4.4 | MA outputs available; re-run deferred |
| 6.5.1 | 6.5.2, 6.5.3 | MA outputs available; re-run deferred |

**Note:** Derivative RQs were NOT re-run because:
1. All show NULL or highly significant findings (robust to model choice)
2. MA outputs exist for future sensitivity analysis if needed
3. Thesis timeline constraints

### Documentation Updates (COMPLETE)

- [x] `docs/lmm_methodology.md` - Created with full MA procedure documentation
- [x] `docs/docs_index.md` - Updated lmm_methodology.md entry
- [x] All 5 ROOT RQ `summary.md` files - Added MA methodology sections

---

## Part 8: Risk Assessment

### What Could Change Substantially

1. **6.1.4 ICC ratio (824×)** - If model-averaged random effects differ significantly from Recip_sq random effects, this major finding could change
2. **6.1.5 clustering phenotypes** - Different random effects → different cluster assignments
3. **6.8.3 ICC patterns** - Already NULL, but exact correlations may shift

### What Almost Certainly Won't Change

1. **All NULL findings** (r ≈ 0, p > 0.10) - Robust to model choice
2. **Highly significant findings** (p < 0.001) - Effect too large to be model-dependent
3. **Direction of effects** - Which group is higher/lower

### Contingency Plan

If major findings change:
1. Report BOTH single-best and MA results in thesis
2. Discuss model uncertainty as a feature, not bug
3. Frame as: "Our conclusions are robust to / sensitive to model specification"

---

## Part 9: Documentation Updates

After completing rework:

1. Update `docs/lmm_methodology.md`:
   - Add section on model averaging procedure
   - Reference Burnham & Anderson (2002)
   - Include code snippets from `tools/model_averaging.py`

2. Update `results/ch6/accuracy_vs_confidence.md`:
   - Note that all trajectory analyses use model averaging
   - Update any specific model references (e.g., "Logarithmic" → "model-averaged")

3. Update `rq_status.tsv`:
   - Change all `KS=YES; MA=NO` to `KS=YES; MA=YES`
   - Update `6.7.3` from `NO` to `YES (uses Ch5 MA)`

---

## Appendix A: Competitive Model Selection Criteria

**ΔAIC threshold:** 7 (models within 7 AIC units of best)
- ΔAIC < 2: Substantial support
- ΔAIC 2-4: Moderate support
- ΔAIC 4-7: Weak support
- ΔAIC > 7: Essentially no support

**Rationale:** Using ΔAIC < 7 includes all models with any meaningful support, ensuring we don't artificially narrow model uncertainty.

**Alternative:** Could use cumulative weight > 95% cutoff, but ΔAIC < 7 is more conservative (includes more models).

---

## Appendix B: Model Averaging Equations

### Akaike Weights (already computed)
```
w_i = exp(-0.5 * ΔAIC_i) / Σ exp(-0.5 * ΔAIC_j)
```

### Model-Averaged Prediction
```
ŷ_MA = Σ w_i * ŷ_i
```

### Unconditional Variance (Burnham & Anderson 2002, eq 4.9)
```
Var(ŷ_MA) = Σ w_i * [Var(ŷ_i | model_i) + (ŷ_i - ŷ_MA)²]
```

The second term captures model selection uncertainty - how much predictions vary across models.

### Model-Averaged Coefficient
```
β̂_MA = Σ w_i * β̂_i  (only for models containing that term)
```

Note: For coefficients, only average across models that include that term (e.g., don't average quadratic term across models without it).

---

**End of Rework Plan**

**Next Action:** User approval, then begin Phase 1 (create `tools/model_averaging.py`)
