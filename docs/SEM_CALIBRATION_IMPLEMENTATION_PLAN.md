# SEM Implementation Plan for Calibration RQs

**Date:** 2025-12-28
**Purpose:** Replace unreliable difference scores with latent variable approach for PLATINUM certification
**Decision:** Option B - Full SEM implementation for ALL calibration RQs
**Rationale:** PLATINUM means we've done everything we can to properly answer the research question

---

## 1. PROBLEM STATEMENT

### Current Methodology (FLAWED)
```python
# Simple difference score
calibration = theta_confidence - theta_accuracy
```

**Critical Issues:**
- **Reliability formula:** `r_diff = (r_xx + r_yy - 2*r_xy) / (2 - 2*r_xy)`
- When `r_xy` is high (0.4-0.6) and `r_xx`, `r_yy` moderate (0.6-0.8):
  - **r_diff collapses** to very low values (-0.16 to 0.54)
  - Difference score dominated by **measurement error**, not true calibration
- **Lord's Paradox:** Regression to mean artifacts in group comparisons

**Observed Failures:**
- RQ 6.2.2: r_diff = -0.16 (SEVERE - worse than random!)
- RQ 6.3.2: r_diff = 0.085 (CRITICAL)
- RQ 6.5.2: r_diff = 0.536 (QUESTIONABLE)
- RQ 6.8.2: r_diff = 0.379 (POOR)

---

## 2. SEM SOLUTION

### Latent Variable Approach

**Conceptual Model:**
```
Latent_Accuracy → theta_accuracy (measured variable)
Latent_Confidence → theta_confidence (measured variable)

Calibration = function(Latent_Accuracy, Latent_Confidence)
```

**Key Advantages:**
1. **Accounts for measurement error** in both accuracy and confidence
2. **Prevents Lord's Paradox** - properly handles baseline differences
3. **Field standard** - reviewers expect SEM for difference scores
4. **More reliable estimates** - uses only true score variance

### Three SEM Approaches

**Approach A: Latent Difference Score (Recommended)**
- Directly models calibration as latent difference
- Most interpretable (preserves calibration = conf - acc)
- Requires constrained equality to identify model

**Approach B: Residualized Calibration**
- Model: `Latent_Confidence ~ Latent_Accuracy`
- Calibration = residual (confidence controlling for accuracy)
- Avoids difference score entirely

**Approach C: Bivariate LMM with Measurement Error**
- Multivariate LMM with time-varying accuracy and confidence
- Simultaneousmodeling with correlated random effects
- Most complex, highest precision

**Recommendation:** Start with **Approach A** (latent difference), validate with **Approach B** (residualized)

---

## 3. AFFECTED RQs INVENTORY

### Complete List (27 RQs with "calibration" in concept)

**High Priority (Derivative RQs with r_diff issues):**

**Tier 1 - CRITICAL (r_diff < 0.20):**
- ☐ **6.2.2** - Over-underconfidence trajectory (r_diff = -0.16)
- ☐ **6.3.2** - Domain calibration (r_diff = 0.085)

**Tier 2 - HIGH (r_diff < 0.50):**
- ☐ **6.8.2** - Source-destination calibration (r_diff = 0.379)

**Tier 3 - MODERATE (r_diff < 0.70):**
- ☐ **6.4.2** - Paradigm calibration (r_diff likely ~0.5-0.6, needs check)
- ☐ **6.5.2** - Schema calibration (r_diff = 0.536)

**Root RQs (Need SEM for downstream validity):**
- ☐ **6.2.1** - Calibration over time (root for 6.2.X series)
- ☐ **6.3.1** - Domain confidence trajectories (feeds 6.3.2, but not calibration itself)
- ☐ **6.4.1** - Paradigm confidence trajectories (feeds 6.4.2, but not calibration itself)
- ☐ **6.5.1** - Schema confidence trajectories (feeds 6.5.2, but not calibration itself)
- ☐ **6.8.1** - Source-destination confidence (feeds 6.8.2, but not calibration itself)

**Additional Calibration RQs (check if they exist and use difference scores):**
- ☐ **6.2.3** - Domain × Calibration
- ☐ **6.2.4** - Paradigm × Calibration
- ☐ **6.2.5** - Schema × Calibration
- ☐ **6.3.3** - Domain calibration age effects
- ☐ **6.3.4** - Domain calibration individual differences
- ☐ **6.4.3** - Paradigm calibration age effects
- ☐ **6.4.4** - Paradigm calibration individual differences
- ☐ **6.5.3** - Schema calibration trajectories
- ☐ **6.8.3** - Source-destination calibration age effects
- ☐ **6.8.4** - Source-destination calibration individual differences

**Special Cases (mentioned calibration but may not use difference scores):**
- 6.1.1, 6.1.2, 6.1.4 - Confidence trajectories (NOT calibration RQs)
- 6.6.1, 6.6.2, 6.6.3 - High-confidence errors (NOT difference scores)
- 6.7.1, 6.7.2, 6.7.3 - Individual differences (NOT calibration)

**Estimated Scope:**
- **Confirmed calibration RQs:** 5 (6.2.2, 6.3.2, 6.4.2, 6.5.2, 6.8.2)
- **Likely calibration RQs:** 10-15 additional (6.2.X, 6.3.X, 6.4.X series)
- **Total estimate:** 15-20 RQs

---

## 4. IMPLEMENTATION WORKFLOW

### Phase 1: Infrastructure (8 hours)

**Task 1.1:** Create SEM methodology specification (2h)
- Document latent difference score model
- Document residualized calibration model
- Define measurement error modeling approach
- Specify identification constraints

**Task 1.2:** Develop SEM template code (4h)
- Create `tools/sem_calibration.py` with reusable functions
- Implement in Python using `semopy` or R `lavaan` via rpy2
- Functions:
  - `fit_latent_difference_model()`
  - `fit_residualized_model()`
  - `extract_calibration_scores()`
  - `compute_model_fit_indices()`
  - `run_diagnostics()`

**Task 1.3:** Create validation framework (2h)
- Model fit criteria (CFI > 0.95, RMSEA < 0.06, SRMR < 0.08)
- Convergence diagnostics
- Parameter stability checks
- Residual analysis

### Phase 2: Prototype Implementation (6 hours)

**Task 2.1:** RQ 6.2.2 SEM implementation (3h)
- Load theta estimates from 6.2.1
- Fit latent difference score model
- Fit residualized model (validation)
- Extract latent calibration scores
- Run LMM with latent scores
- Compare to original results

**Task 2.2:** Validation and diagnostics (1h)
- Model fit indices
- Convergence checks
- Residual diagnostics
- Sensitivity analysis

**Task 2.3:** Documentation and reporting (2h)
- Create PLATINUM_REPORT_SEM.md
- Document methodology changes
- Update validation.md
- Create before/after comparison table

### Phase 3: Batch Implementation (40-60 hours)

**For each RQ (3-4h per RQ × 15-20 RQs):**

**Step 1:** Identify upstream sources (30 min)
- Which RQs provide theta_accuracy?
- Which RQs provide theta_confidence?
- Check data availability

**Step 2:** Fit SEM models (1h)
- Load data
- Fit latent difference model
- Fit residualized model (if convergence issues)
- Extract latent calibration scores

**Step 3:** Re-run analysis with SEM scores (1h)
- Replace old calibration variable
- Re-fit LMMs or other models
- Extract new results

**Step 4:** Validation (30 min)
- Check model fit
- Compare to original findings
- Document changes

**Step 5:** Documentation (1h)
- Update results/summary.md with SEM methodology
- Update results/validation.md
- Create PLATINUM certification report
- Update status.yaml

**Optimization:**
- After 2-3 RQs, workflow time should drop to ~2h per RQ
- Parallelize where possible (independent RQ families)
- Reuse fitted models where upstream sources shared

### Phase 4: Cross-Validation and Finalization (6 hours)

**Task 4.1:** Compare original vs SEM findings (2h)
- Create comparison matrix for all RQs
- Identify which conclusions changed
- Document effect of methodology upgrade

**Task 4.2:** Update thesis documentation (2h)
- Create `docs/sem_calibration_methodology.md`
- Update `docs/glossary.md` with SEM terms
- Add to `docs/design_decisions.md`

**Task 4.3:** Quality assurance (2h)
- Verify all RQs use consistent SEM approach
- Check all model fit indices acceptable
- Ensure all documentation updated
- Run final PLATINUM certification checks

---

## 5. TECHNICAL SPECIFICATIONS

### SEM Model Specification (Latent Difference Approach)

**Measurement Model:**
```
# Latent variables
eta_accuracy =~ 1*theta_accuracy
eta_confidence =~ 1*theta_confidence

# Measurement error variances (fixed from IRT)
theta_accuracy ~~ sigma2_accuracy * theta_accuracy
theta_confidence ~~ sigma2_confidence * theta_confidence

# Latent calibration (difference)
eta_calibration := eta_confidence - eta_accuracy
```

**Where:**
- `sigma2_accuracy` = measurement error variance from IRT (1 / test information)
- `sigma2_confidence` = measurement error variance from IRT (1 / test information)
- `eta_calibration` = latent calibration (error-free difference)

**Identification:**
- Fix latent variable scales by setting factor loadings = 1
- Fix measurement error variances from IRT test information
- Latent difference identified via defined variable

### SEM Model Specification (Residualized Approach)

**Structural Model:**
```
# Measurement model (same as above)
eta_accuracy =~ 1*theta_accuracy
eta_confidence =~ 1*theta_confidence

# Structural regression
eta_confidence ~ beta*eta_accuracy

# Residual calibration = residual from regression
eta_calibration := residuals(eta_confidence ~ eta_accuracy)
```

**Advantages:**
- Avoids Lord's Paradox (controls for baseline accuracy)
- More robust when accuracy-confidence correlation high
- Standard approach in psychometric literature

### Data Requirements Per RQ

**Input files needed:**
1. `theta_accuracy.csv` - IRT theta estimates for accuracy
2. `theta_confidence.csv` - IRT theta estimates for confidence
3. `irt_accuracy_info.csv` - Test information curves (for sigma2_accuracy)
4. `irt_confidence_info.csv` - Test information curves (for sigma2_confidence)

**If test information not available:**
- Use reliability estimates: `sigma2 = theta_var * (1 - reliability)`
- Typical IRT reliability ≈ 0.80-0.90
- Conservative estimate: reliability = 0.75

### Software Implementation

**Option A: semopy (Python) - RECOMMENDED**
```python
import semopy
from semopy import Model

# Define model
model_spec = """
# Measurement
eta_acc =~ 1*theta_acc
eta_conf =~ 1*theta_conf

# Fixed measurement error
theta_acc ~~ {sigma2_acc}*theta_acc
theta_conf ~~ {sigma2_conf}*theta_conf

# Latent difference
eta_calib := eta_conf - eta_acc
"""

# Fit model
model = Model(model_spec)
model.fit(data)

# Extract latent scores
latent_calibration = model.predict_factors()['eta_calib']
```

**Option B: lavaan (R via rpy2)**
```r
library(lavaan)

model <- '
  # Measurement
  eta_acc =~ 1*theta_acc
  eta_conf =~ 1*theta_conf

  # Fixed error
  theta_acc ~~ {sigma2_acc}*theta_acc
  theta_conf ~~ {sigma2_conf}*theta_conf

  # Latent difference
  eta_calib := eta_conf - eta_acc
'

fit <- sem(model, data=data)
latent_calib <- lavPredict(fit, type="lv")[,"eta_calib"]
```

### Model Fit Criteria

**Acceptable fit:**
- CFI (Comparative Fit Index) ≥ 0.95
- TLI (Tucker-Lewis Index) ≥ 0.95
- RMSEA (Root Mean Square Error of Approximation) < 0.06
- SRMR (Standardized Root Mean Square Residual) < 0.08

**Perfect fit expected:**
- Just-identified model (2 latent variables, 2 indicators)
- Should achieve perfect fit (CFI=1.0, RMSEA=0.0)
- If not perfect fit → measurement error variances misspecified

---

## 6. RESOURCE ALLOCATION

### Time Estimates

| Phase | Task | Hours | Notes |
|-------|------|-------|-------|
| **Phase 1** | Infrastructure | 8 | One-time setup |
| **Phase 2** | Prototype (6.2.2) | 6 | Proof of concept |
| **Phase 3** | Batch (15 RQs) | 45 | 3h/RQ average |
| **Phase 4** | Finalization | 6 | QA and docs |
| **Total** | | **65** | 60-120h range estimate |

**Optimistic:** 60 hours (if only 12-15 RQs affected)
**Realistic:** 75 hours (15-18 RQs)
**Conservative:** 100 hours (20+ RQs or significant complications)

### Execution Timeline

**If working 8 hours/day:**
- Phase 1: Day 1
- Phase 2: Day 2
- Phase 3: Days 3-8 (6 days)
- Phase 4: Day 9
- **Total: 9 working days**

**If working 4 hours/day:**
- **Total: 18 working days (~3 weeks)**

### Parallelization Opportunities

**Independent RQ families (can work in parallel):**
1. 6.2.X series (calibration over time)
2. 6.3.X series (domain calibration)
3. 6.4.X series (paradigm calibration)
4. 6.5.X series (schema calibration)
5. 6.8.X series (source-destination calibration)

**If parallelizable:** Could reduce Phase 3 to ~20-30 hours with concurrent execution

---

## 7. VALIDATION CRITERIA FOR PLATINUM

### For Each RQ to Achieve PLATINUM:

**Statistical Rigor:**
- ✅ SEM model achieves acceptable fit (CFI > 0.95)
- ✅ Convergence diagnostics pass
- ✅ Residuals normally distributed
- ✅ No Heywood cases (negative variances)

**Methodological Soundness:**
- ✅ Measurement error properly modeled
- ✅ Lord's Paradox avoided (residualized or within-subject)
- ✅ Latent calibration reliability > 0.70
- ✅ Sensitivity analysis (latent difference vs residualized) agree

**Documentation:**
- ✅ SEM model specification documented
- ✅ Model fit indices reported
- ✅ Before/after comparison table
- ✅ Methodology change rationale explained

**Theoretical Coherence:**
- ✅ Findings interpretable with SEM approach
- ✅ Conclusions remain valid (or updated appropriately)
- ✅ Literature alignment maintained

---

## 8. SUCCESS METRICS

### Macro-Level (Across All RQs)

**Primary Success:**
- 100% of calibration RQs achieve PLATINUM status
- All latent calibration reliabilities > 0.70
- All SEM models achieve acceptable fit

**Secondary Success:**
- Core findings robust to methodology change (< 20% change in effect sizes)
- NULL findings remain NULL or become stronger
- Significant findings remain significant or become stronger

### RQ-Level Success

**For each RQ:**
- Model converges without warnings
- Fit indices meet criteria
- Latent calibration scores extracted successfully
- Analysis re-run with new scores produces valid results
- Documentation complete

### Failure Criteria (Stop and Reassess)

**If ANY of these occur:**
- >30% of models fail to converge
- >30% of models fail fit criteria
- >50% of findings reverse direction (requires theoretical re-evaluation)
- Latent calibration reliability consistently < 0.50

**Contingency:** Fall back to Path C (Hybrid) - SEM for critical RQs only

---

## 9. DECISION TREE

```
START: RQ uses calibration = confidence - accuracy
  │
  ├─→ Step 1: Check if RQ exists and has analysis
  │   ├─ YES → Continue
  │   └─ NO → Skip this RQ
  │
  ├─→ Step 2: Compute current r_diff
  │   ├─ r_diff < 0.50 → TIER 1 (Critical)
  │   ├─ r_diff 0.50-0.70 → TIER 2 (High)
  │   └─ r_diff > 0.70 → TIER 3 (Moderate - may skip SEM if findings robust)
  │
  ├─→ Step 3: Fit SEM models
  │   ├─ Latent difference model
  │   └─ Residualized model (validation)
  │
  ├─→ Step 4: Check convergence
  │   ├─ Converged → Continue
  │   └─ Failed → Try simpler model or document limitation
  │
  ├─→ Step 5: Extract latent calibration scores
  │
  ├─→ Step 6: Re-run analysis
  │   ├─ LMM with latent scores
  │   ├─ Compare to original results
  │   └─ Document changes
  │
  ├─→ Step 7: Validate
  │   ├─ Model fit acceptable → PLATINUM certified
  │   └─ Model fit poor → Diagnose and iterate
  │
  └─→ DONE: RQ achieves PLATINUM status
```

---

## 10. NEXT STEPS (Immediate)

**User approved Option B (Full SEM) - Proceed with:**

1. **NOW:** Create SEM methodology specification document ✓ (this file)

2. **NEXT (2h):** Develop `tools/sem_calibration.py` template
   - Functions for latent difference model
   - Functions for residualized model
   - Utility functions for data prep
   - Validation functions

3. **THEN (6h):** Prototype on RQ 6.2.2 (r_diff = -0.16)
   - Most severe case = best test
   - If this works, others will be easier

4. **AFTER PROTOTYPE:** Batch apply to remaining RQs
   - Start with Tier 1 (critical)
   - Then Tier 2 (high priority)
   - Finally Tier 3 (moderate priority)

5. **FINAL:** Cross-validation and documentation
   - Compare all before/after results
   - Update methodology docs
   - PLATINUM certification for all calibration RQs

---

**Status:** APPROVED - Ready to implement
**Timeline:** 60-100 hours (9-18 working days)
**Next Action:** Create `tools/sem_calibration.py` template

**End of Implementation Plan**
