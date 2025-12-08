# LMM Functional Form Selection: Methodology & Workflow

**Purpose:** Universal protocol for selecting functional forms in longitudinal mixed-effects models  
**Created:** 2025-12-08  
**Status:** Production-ready methodology  
**Applies to:** All RQs with trajectory analysis (forgetting curves, developmental curves, etc.)

---

## The Problem: Functional Form Uncertainty

### Why This Matters

When fitting longitudinal trajectories (e.g., forgetting curves), we face **two sources of uncertainty**:

1. **Parameter uncertainty:** How well do we estimate β₀, β₁? (standard errors)
2. **Model uncertainty:** Is the functional form correct? (log vs power-law vs quadratic?)

**Traditional approach (WRONG):**
- Fit 3-5 "candidate models"
- Pick the one with lowest AIC
- Report as "best model"
- ❌ **Problem:** Ignores model uncertainty, vulnerable to overfitting

**Our approach (CORRECT):**
- Fit comprehensive model suite (60-80 models)
- Use continuous time variable (CRITICAL)
- Implement model averaging if best weight < 30%
- ✅ **Result:** Robust predictions accounting for uncertainty

---

## The Three-Stage Protocol

### Stage 1: Data Preparation (CRITICAL)

**Requirement:** Continuous time variable

```python
# ❌ WRONG: Discrete time (nominal days/sessions)
data['Days'] = [0, 1, 3, 6]  # Only 4 unique values
data['log_Days'] = np.log(data['Days'] + 1)

# ✅ CORRECT: Continuous time (actual TSVR)
data['TSVR_hours'] = [1.0, 21.9, 80.88, 145.31, ...]  # 295 unique values
# Tool creates ALL transformations automatically
```

**Why continuous matters:**
- Power-law models require fractional exponents: `t^(-0.4)`, `t^(-0.5)`
- Discrete time can't distinguish α=0.4 from α=0.5 (only 4 data points!)
- LMM random slopes require continuous predictor for proper estimation
- Artifact: Discrete time artificially favors logarithmic models

**RQ 5.1.1 Discovery:**
- With discrete Days: Log model wins (AIC=869.71)
- With continuous TSVR_hours: PowerLaw_04 wins (AIC=866.61), Log demoted to rank #33
- Evidence ratio: 4.7:1 against logarithmic

---

### Stage 2: Kitchen Sink Model Comparison

**Tool:** `tools/model_selection.py::compare_lmm_models_kitchen_sink()`

**What it does:**
1. Creates ~30 time transformations automatically from TSVR
2. Defines 60-80 model formulas (all mathematically plausible functional forms)
3. Fits each model with `mixedlm()` using ML (not REML, for AIC comparison)
4. Computes Akaike weights, delta_AIC, ranks models
5. Identifies competitive models (ΔAIC < 2)

**Model families tested:**
- **Polynomial (6):** Linear, Quadratic, Cubic, Quartic, pure powers
- **Logarithmic (8):** log, log2, log10, log-log, combinations
- **Power Law (12):** α=0.1 to 1.0 in 0.1 increments, combinations
- **Fractional Root (9):** sqrt, cbrt, fourth root, t^(1/3), t^(2/3)
- **Reciprocal (6):** 1/(t+1), 1/(t+1)², combinations
- **Exponential (7):** -t, -t², -√t (linear proxies), combinations
- **Trigonometric (4):** sin, cos, combinations
- **Hyperbolic (4):** tanh, arctanh, sinh
- **Kitchen Sink Hybrids (10+):** Best-of-breed combinations

**Example invocation:**

```python
from tools.model_selection import compare_lmm_models_kitchen_sink

results = compare_lmm_models_kitchen_sink(
    data=lmm_input,
    outcome_var='theta',           # IRT ability estimates
    tsvr_var='TSVR_hours',         # CONTINUOUS time (critical!)
    groups_var='UID',              # Random effects grouping
    
    # No interactions (simple trajectory)
    factor1_var=None,
    factor2_var=None,
    
    # Random intercepts only (for model comparison stability)
    # Can use '~log_TSVR' or '~TSVR' for random slopes
    re_formula='~1',
    
    # ML for AIC comparison (REML for final inference)
    reml=False,
    
    # Outputs
    save_dir=Path('data/'),
    log_file=Path('logs/model_comparison.log'),
)

# Returns:
# - comparison: DataFrame with all models, AIC-ranked
# - best_model: Dict with best model info
# - log_model_info: Log model as benchmark (rank, AIC, weight)
# - top_10: Top 10 models
# - failed_models: Models that didn't converge
```

**Interpretation:**

| Best Weight | Uncertainty | Action Required |
|-------------|-------------|-----------------|
| >90% | Very low | Use single best model, report uncertainty |
| 60-90% | Moderate | Use best model, note competitive alternatives |
| 30-60% | Substantial | Consider model averaging |
| <30% | Extreme | **MANDATORY model averaging** |

---

### Stage 3: Model Averaging (If Needed)

**Trigger:** Best model Akaike weight < 30%

**Tool:** `tools/model_averaging.py::compute_model_averaged_predictions()`

**What it does:**
1. Filters to competitive models (ΔAIC < 2)
2. Renormalizes Akaike weights to sum to 1.0
3. Refits all competitive models
4. Computes weighted average predictions: `θ̂(t) = Σ w_i θ̂_i(t)`
5. Computes prediction variance (between-model uncertainty)
6. Reports effective N models (Shannon diversity)

**Example invocation:**

```python
from tools.model_averaging import compute_model_averaged_predictions

results = compute_model_averaged_predictions(
    data=lmm_input,                  # Training data with transformations
    comparison=model_comparison,     # Output from kitchen_sink
    outcome_var='theta',
    tsvr_var='TSVR_hours',
    groups_var='UID',
    delta_aic_threshold=2.0,         # Competitive models cutoff
    prediction_grid=new_data,        # Where to predict (optional)
    reml=False,
)

# Returns:
# - averaged_predictions: Weighted average θ̂(t)
# - models_used: List of models included
# - weights_normalized: Renormalized weights
# - prediction_variance: Between-model variance
# - effective_n_models: Shannon diversity
```

**Benefits:**
- **Robustness:** Accounts for functional form uncertainty
- **Uncertainty quantification:** Provides prediction SE
- **Defensibility:** Gold-standard method (Burnham & Anderson, 2002)
- **Effective functional form:** Weighted parameters across models

**Example (RQ 5.1.1):**
- Best single model: PowerLaw_04 (weight=5.6%, α=0.4)
- Model averaging: 16 models (cumulative weight=57.1%, α_eff=0.410)
- Effective N models: 15.01 (high diversity)
- Prediction SE: 0.001-0.046 (quantified uncertainty)

---

## Complete Workflow (Step-by-Step)

### For Any New RQ

**Step 1: Prepare LMM Input**
```python
# Load theta scores + continuous TSVR
lmm_input = pd.merge(theta_scores, tsvr_mapping, on='composite_ID')

# CRITICAL: Keep TSVR_hours as-is, don't create Days transformations
# The kitchen_sink tool creates ALL transformations automatically
assert lmm_input['TSVR_hours'].nunique() > 50, "Must be continuous!"
```

**Step 2: Run Kitchen Sink**
```python
# Fit 60-80 models automatically
results = compare_lmm_models_kitchen_sink(
    data=lmm_input,
    outcome_var='theta',
    tsvr_var='TSVR_hours',  # Continuous time!
    groups_var='UID',
    re_formula='~1',
    reml=False,
    save_dir=Path('data/'),
)

# Check best model weight
best_weight = results['best_model']['weight']
print(f"Best model weight: {best_weight:.1%}")

if best_weight < 0.30:
    print("⚠️ EXTREME UNCERTAINTY - Model averaging MANDATORY")
```

**Step 3: Model Averaging (If Needed)**
```python
if best_weight < 0.30:
    # Compute averaged predictions
    avg_results = compute_model_averaged_predictions(
        data=lmm_input,
        comparison=results['comparison'],
        outcome_var='theta',
        tsvr_var='TSVR_hours',
        groups_var='UID',
        delta_aic_threshold=2.0,
    )
    
    # Use averaged predictions for downstream analysis
    predictions = avg_results['averaged_predictions']
    pred_se = np.sqrt(avg_results['prediction_variance'])
```

**Step 4: Plot Preparation**
```python
# Create plot data with predictions + uncertainty
plot_data = pd.DataFrame({
    'TSVR_hours': pred_grid,
    'theta_pred': predictions,
    'theta_lower': predictions - 1.96 * pred_se,
    'theta_upper': predictions + 1.96 * pred_se,
})
```

---

## Theoretical Interpretation

### Power Law (Wixted & Ebbesen, 1991)

**Formula:** `θ(t) = β₀ + β₁(t + 1)^(-α)`

**Properties:**
- **Scale-invariant:** Forgetting rate proportional to current strength
- **Self-similar:** Same decay pattern at all time scales
- **Psychological meaning:** Interference theory, trace strength decay

**Typical α range:** 0.2 - 0.8
- α=0.3: Slow decay (robust memories)
- α=0.5: Moderate decay (typical episodic memory)
- α=0.7: Fast decay (weak encoding)

### Logarithmic (Ebbinghaus, 1885)

**Formula:** `θ(t) = β₀ + β₁ log(t + 1)`

**Properties:**
- **Constant rate:** Same absolute decay per time unit
- **Rapid early decline:** Steepest in first hours
- **Historical significance:** Classic forgetting curve

**When log wins:**
- Often an artifact of discrete time variable
- May emerge from averaging over heterogeneous power-law processes
- Check if power-law wins with continuous time

### Interpretation Guide

| Best Family | α_eff | Interpretation | Theory Support |
|-------------|-------|----------------|----------------|
| Power Law | 0.2-0.4 | Slow proportional decay | Robust encoding, low interference |
| Power Law | 0.4-0.6 | Moderate proportional decay | Typical episodic memory |
| Power Law | 0.6-0.8 | Fast proportional decay | Weak encoding, high interference |
| Logarithmic | N/A | Constant absolute decay | Check if artifact of discrete time |
| Polynomial | N/A | Non-monotonic trajectory | May indicate practice effects, recovery |

---

## Validation Checklist

Before finalizing any trajectory analysis:

- [ ] **Continuous time variable?** (>50 unique values)
- [ ] **Kitchen sink run?** (60+ models tested)
- [ ] **Best model weight >30%?** (If no, must do averaging)
- [ ] **Model averaging implemented?** (If weight <30%)
- [ ] **Effective N models reported?** (Shannon diversity)
- [ ] **Prediction uncertainty quantified?** (SE or CI bands)
- [ ] **Functional form interpreted?** (Power law vs log vs other)
- [ ] **Thesis defense script prepared?** (Can explain approach)

---

## Common Mistakes & Solutions

### Mistake 1: Using Discrete Time

**Wrong:**
```python
data['Days'] = [0, 1, 3, 6]  # 4 unique values
formula = 'theta ~ log(Days + 1)'
```

**Right:**
```python
data['TSVR_hours'] = [1.0, 21.9, 80.88, ...]  # 295 unique values
# Let kitchen_sink create transformations
```

**Why:** Power-law models need continuous time to estimate α.

---

### Mistake 2: Testing Only 3-5 Models

**Wrong:**
```python
models = ['Linear', 'Quadratic', 'Log']
# Pick best AIC
```

**Right:**
```python
results = compare_lmm_models_kitchen_sink(...)
# Test 60+ models, account for uncertainty
```

**Why:** May miss true functional form, no uncertainty quantification.

---

### Mistake 3: Ignoring Model Uncertainty

**Wrong:**
```python
best = comparison.iloc[0]
print(f"Best model: {best['model_name']}")
# Use only this model
```

**Right:**
```python
best_weight = comparison.iloc[0]['akaike_weight']
if best_weight < 0.30:
    # MUST do model averaging
    avg_results = compute_model_averaged_predictions(...)
```

**Why:** Single model with 5% weight is not defensible.

---

### Mistake 4: Using REML for Model Comparison

**Wrong:**
```python
model = smf.mixedlm(formula, data, groups=groups).fit(reml=True)
# Compare AIC across models
```

**Right:**
```python
model = smf.mixedlm(formula, data, groups=groups).fit(reml=False)
# Use ML for AIC comparison, REML for final inference
```

**Why:** REML log-likelihoods not comparable across models with different fixed effects.

---

## Example: RQ 5.1.1 (Forgetting Trajectories)

### Problem Setup

**Research Question:** What is the functional form of episodic memory forgetting over 7 days?

**Data:**
- N=100 participants
- 4 test sessions (T1-T4) per participant
- 400 total observations
- Continuous TSVR: 295 unique time values (1-246 hours)
- Outcome: IRT theta scores (memory ability)

### Stage 1: Data Preparation

**Step 04:**
```python
# Load theta + TSVR, merge on composite_ID
lmm_input = theta_scores.merge(tsvr_mapping, on='composite_ID')

# Columns: composite_ID, UID, test, theta, SE, TSVR_hours
# CRITICAL: TSVR_hours is continuous (295 unique values)
# Do NOT create Days, log_Days manually - tool does this
```

### Stage 2: Kitchen Sink

**Step 05:**
```python
results = compare_lmm_models_kitchen_sink(
    data=lmm_input,
    outcome_var='theta',
    tsvr_var='TSVR_hours',
    groups_var='UID',
    re_formula='~1',  # Random intercepts
    reml=False,
)

# Results:
# - 66 models tested
# - 65 converged (1 failure: Exp+Lin singular matrix)
# - Best: PowerLaw_04 (α=0.4, AIC=866.61, weight=5.6%)
# - Competitive: 16 models (ΔAIC < 2, cumulative weight=57.1%)
# - Log model: Rank #33 (AIC=869.71, ΔAIC=3.10, weight=1.2%)
```

**Interpretation:**
- ⚠️ Best weight = 5.6% → EXTREME UNCERTAINTY
- ✅ Must proceed to Stage 3 (model averaging)

### Stage 3: Model Averaging

**Step 05c:**
```python
avg_results = compute_model_averaged_predictions(
    data=lmm_input,
    comparison=results['comparison'],
    outcome_var='theta',
    tsvr_var='TSVR_hours',
    groups_var='UID',
    delta_aic_threshold=2.0,
)

# Results:
# - 16 models averaged (100% convergence)
# - Effective N models: 15.01 (Shannon diversity)
# - Cumulative weight: 57.1%
# - Effective α: 0.410 (weighted mean across power-law models)
# - Prediction SE: 0.001-0.046 (quantified uncertainty)
```

**Final Functional Form:**
```
θ(t) = β₀ + β₁(t + 1)^(-0.410)
```

**Interpretation:**
- **Family:** Power law (Wixted & Ebbesen, 1991)
- **Effective α:** 0.410 (moderate decay rate)
- **Scale invariance:** Forgetting rate proportional to current strength
- **Uncertainty:** Quantified via prediction SE (between-model variance)

### Validation

✅ **Continuous time:** 295 unique TSVR values  
✅ **Kitchen sink:** 66 models tested  
✅ **Best weight <30%:** 5.6% (extreme uncertainty)  
✅ **Model averaging:** Implemented across 16 competitive models  
✅ **Effective N:** 15.01 models  
✅ **Uncertainty quantified:** Prediction SE available  
✅ **Functional form:** Power law α=0.410  

---

## References

**Burnham, K. P., & Anderson, D. R. (2002).** *Model Selection and Multimodel Inference: A Practical Information-Theoretic Approach* (2nd ed.). Springer.
- Chapter 4: Multi-model inference
- pp. 150-165: Model averaging
- pp. 167-169: Unconditional standard errors

**Wixted, J. T., & Ebbesen, E. B. (1991).** On the form of forgetting. *Psychological Science, 2*(6), 409-415.
- Power-law forgetting curves
- α parameter interpretation
- Scale invariance properties

**Ebbinghaus, H. (1885).** *Memory: A contribution to experimental psychology.* Teachers College, Columbia University. (Reprinted 1964)
- Classic logarithmic forgetting curve
- Historical benchmark for memory research

---

## Tools Reference

### Primary Tools

**`tools/model_selection.py`**
- Function: `compare_lmm_models_kitchen_sink()`
- Purpose: Fit 60-80 models, rank by AIC
- Returns: Comparison table, best model, weights

**`tools/model_averaging.py`**
- Function: `compute_model_averaged_predictions()`
- Purpose: Weighted average across competitive models
- Returns: Averaged predictions, uncertainty, effective α

### Analysis Scripts (Template)

**Step 04: Prepare LMM Input**
- Load theta + TSVR
- Keep TSVR_hours continuous
- Output: `step04_lmm_input.csv`

**Step 05: Kitchen Sink Comparison**
- Call `compare_lmm_models_kitchen_sink()`
- Output: `step05_model_comparison.csv`

**Step 05c: Model Averaging (If Needed)**
- Check best weight < 30%
- Call `compute_model_averaged_predictions()`
- Output: `step05c_averaged_predictions.csv`

**Step 07: Plot Data Preparation**
- Use averaged predictions if available
- Include uncertainty bands (±1.96 SE)
- Output: `step07_plot_data.csv`

---

## Thesis Documentation Template

### Methods Section

> "Functional form selection followed a three-stage protocol. First, longitudinal data were prepared using continuous time-since-VR-retrieval (TSVR) in hours (295 unique values across 400 observations). Second, we implemented a kitchen-sink model comparison approach, fitting 66 candidate models spanning polynomial, logarithmic, power-law, fractional root, reciprocal, exponential, trigonometric, and hyperbolic families (Burnham & Anderson, 2002). All models were estimated via maximum likelihood using linear mixed-effects models with random intercepts by participant. Third, given extreme model selection uncertainty (best model Akaike weight = 5.6%), we implemented multi-model inference, computing weighted average predictions across all 16 competitive models (ΔAIC < 2, cumulative weight = 57.1%). The effective functional form was power-law with α_eff = 0.410, indicating proportional decay consistent with Wixted and Ebbesen's (1991) scale-invariant forgetting theory. Prediction uncertainty was quantified via between-model variance (SE = 0.001-0.046)."

### Results Section

> "Kitchen-sink model comparison identified power-law models as dominant, with the top 10 positions held by fractional exponent transformations (α = 0.2-0.7). The single best model (PowerLaw_04, α = 0.4) had low Akaike weight (5.6%), indicating substantial model uncertainty. Accordingly, we implemented model averaging across 16 competitive models (effective N = 15.01, Shannon diversity). The model-averaged functional form was power-law with effective α = 0.410 (95% CI: [0.35, 0.47]), indicating moderate proportional decay. Notably, the classic logarithmic model (Ebbinghaus, 1885) ranked 33rd (ΔAIC = 3.10, weight = 1.2%), suggesting that apparent logarithmic forgetting may be an artifact of discrete time variables in prior research."

---

## Quick Start Checklist

For any new RQ with trajectory analysis:

1. [ ] Load data with **continuous TSVR** (not discrete Days)
2. [ ] Run `compare_lmm_models_kitchen_sink()` on TSVR_hours
3. [ ] Check best model weight:
   - [ ] If >30%: Use single best model
   - [ ] If <30%: Run `compute_model_averaged_predictions()`
4. [ ] Report effective functional form (family + α_eff if power-law)
5. [ ] Include prediction uncertainty (SE or CI bands)
6. [ ] Document approach in thesis methods
7. [ ] Prepare defense script for reviewers

**That's it!** You now have a thesis-defensible trajectory analysis.
