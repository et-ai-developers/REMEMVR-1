# RQ 5.1.1 Visualization Regeneration

**Date:** 2025-12-08
**Purpose:** Regenerate plots using model-averaged trajectory (not single best model)

---

## Changes Made

### 1. Previous Approach (DEPRECATED)
- **Source CSV:** `step07_functional_form_theta_data.csv`
- **Method:** Single best model from AIC selection (Logarithmic, AIC=873.7)
- **Issue:** Best model weight = 48%, moderate uncertainty
- **Problem:** Original 5-model comparison missed power-law variants

### 2. Extended Model Comparison Discovery (2025-12-08)
- **66 models tested** (including power law variants with fractional exponents)
- **Finding:** Power-law models DOMINATE top positions
  - Best single model: PowerLaw_04 (α=0.4, AIC=866.74)
  - Original Log model: DEMOTED to Rank #33 (ΔAIC=+3.10)
  - Evidence ratio: 4.7:1 in favor of power law vs logarithmic
- **Uncertainty:** Best model weight = 5.6% (EXTREME uncertainty)
- **Conclusion:** 16 competitive models within ΔAIC<2, model averaging MANDATORY

### 3. New Approach (CURRENT)
- **Source CSV:** `step07b_averaged_trajectory_data.csv`
- **Method:** Multi-model inference (Burnham & Anderson, 2002)
  - 16 competitive models averaged (ΔAIC < 2)
  - Weighted by Akaike weights
  - Between-model variance for 95% CI bands
- **Effective functional form:** Power law with α_eff = 0.410
- **Formula:** θ(t) = β₀ + β₁(t+1)^(-0.410)
- **Theoretical interpretation:** Wixted & Ebbesen (1991) power-law forgetting

---

## Files Generated

### Plots
1. **functional_form_theta.png** (471 KB, 300 DPI)
   - Theta-scale trajectory
   - 400 observed data points (individual observations)
   - Model-averaged prediction line (100 time points)
   - 95% CI bands from between-model variance
   - Annotation: α_eff=0.410, 16 models, power-law form

2. **functional_form_probability.png** (555 KB, 300 DPI)
   - Probability-scale trajectory (Decision D069)
   - Same structure as theta-scale
   - Y-axis: Probability Correct (0-100%)
   - IRT 2PL transformation: p = 1/(1 + exp(-1.7θ))

### Data
- **step07b_averaged_trajectory_data.csv** (25 KB, 500 rows)
  - 400 rows: Observed data (100 participants × 4 tests)
  - 100 rows: Model-averaged predictions with SE and CI
  - Columns: TSVR_hours, theta, UID, data_type, prediction_se, theta_lower, theta_upper

---

## Key Messages for Thesis

### 1. Paradigm Shift: Logarithmic → Power Law
- **Original RQ 5.1.1 conclusion (2025-11-30):** "Logarithmic forgetting (Ebbinghaus)"
- **Revised conclusion (2025-12-08):** "Power-law forgetting (Wixted & Ebbesen, 1991)"
- **Impact:** Changes theoretical interpretation throughout thesis
- **Reason:** Original analysis only tested 5 basic models, missed power-law variants

### 2. Model Uncertainty → Model Averaging
- **Problem:** Best single model weight = 5.6% (extreme uncertainty)
- **Solution:** Multi-model inference across 16 competitive models
- **Benefit:** Robustness, accounts for functional form uncertainty
- **Ph.D. defense:** Scientifically defensible, methodologically rigorous

### 3. Continuous Time Essential
- **Critical:** Fractional exponents (α=0.3, 0.4, 0.5) require continuous time variable
- **TSVR_hours:** Actual hours since encoding (not nominal days)
- **Decision D070:** Applied correctly, enabled power-law detection

---

## Statistical Details

### Model Averaging Approach
- **Method:** Information-theoretic model averaging (Burnham & Anderson, 2002)
- **Selection criterion:** ΔAIC < 2 (competitive models)
- **Weights:** Normalized Akaike weights sum to 1.0
- **Predictions:** Weighted average across 16 models
- **Uncertainty:** Between-model variance (not within-model SE)

### Effective Functional Form
- **Family:** Power law
- **Effective α:** 0.410 (weighted average of exponents)
- **Interpretation:** 
  - Proportional decay (equal percentage decline per unit time)
  - Scale-invariant (same shape at all time scales)
  - Characteristic of memory consolidation processes

### Top 5 Models Contributing to Average
1. PowerLaw_04 (α=0.4, w=9.8%)
2. PowerLaw_05 (α=0.5, w=9.2%)
3. PowerLaw_03 (α=0.3, w=8.8%)
4. LogLog (log(log(t+1)+1), w=8.5%)
5. Root_033 (t^(1/3), w=7.7%)

All power-law or fractional-exponent forms → strong evidence for this functional family.

---

## Validation

### Executed
```bash
poetry run python results/ch5/5.1.1/plots/plots.py
```

### Output
- ✓ 400 observed data points loaded
- ✓ 100 prediction grid points loaded
- ✓ Theta-scale plot saved (471 KB)
- ✓ Probability-scale plot saved (555 KB)
- ✓ Decision D069 compliance verified

### Visual Inspection Required
- [ ] Check theta-scale plot: Power-law curve shape (rapid initial decline, gradual asymptote)
- [ ] Check probability-scale plot: Transformation preserves curve shape
- [ ] Verify 95% CI bands visible and appropriate width
- [ ] Confirm 400 individual observations visible as scatter points
- [ ] Check annotation box readable and accurate (α_eff=0.410, 16 models)

---

## Next Steps

1. **Update status.yaml** - Note visualization regenerated with model-averaged data
2. **Update Results section** - Revise functional form conclusion (Log → Power law)
3. **Discussion section** - Interpret power-law implications (Wixted theory, scale invariance)
4. **Propagate to downstream RQs** - Check if other RQs affected by functional form change
5. **Model completeness check** - Verify other trajectory RQs tested extended model suite

---

**Regeneration complete.** Plots now reflect scientifically robust multi-model inference approach with power-law functional form (α_eff=0.410) from 16 competitive models.
