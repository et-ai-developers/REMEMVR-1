# GEE Validation Protocol - Binary Outcomes

**Purpose:** Complete protocol for validating Linear Probability Model (LPM) results using Generalized Estimating Equations (GEE) with binomial family and logit link for binary outcome variables.

**Related Topics:**
- ch6_100_pct_certification_complete.md
- schema_baseline_trajectory_framework_finalized.md

---

## RQ 6.5.3 GEE Validation - Protocol Established (2025-12-30)

**Blocker:** Original analysis used Linear Probability Model (LPM), summary.md flagged GEE as HIGH PRIORITY

**Decision:** User selected Option A - Run GEE analysis (~30-45 min, statistical rigor)

**Archived from:** state.md Session (2025-12-30 Continuation)
**Original Date:** 2025-12-30
**Reason:** GEE validation complete, protocol established, NULL result confirmed robustly

---

### GEE Implementation (~30 min)

**Created:** step03b_gee_validation.py (260 lines, statsmodels GEE)

**Model Specification:**
- Family: Binomial
- Link: Logit
- Correlation: Exchangeable (within-participant)
- Sample: N=7,200 item-responses (100 UID × 4 tests × 18 items)

**Execution:** <20 seconds (converged successfully)

**Code Structure:**
```python
# 1. Load binary outcome data (HCE: 0/1)
# 2. Specify model: HCE ~ Schema_Level + Test
# 3. Fit GEE with binomial family, logit link, exchangeable correlation
# 4. Extract Bonferroni-corrected contrasts (3 pairwise schema comparisons)
# 5. Save results to CSV + model summary to TXT
```

---

### Results - NULL CONFIRMED

**Comparison of LPM vs GEE:**

| Method | Incongruent vs Common | p_uncorr | p_bonf | Conclusion |
|--------|----------------------|----------|--------|------------|
| **LPM** (2025-12-12) | β=0.0185 (1.85 pp) | .043 | .130 | NULL |
| **GEE** (2025-12-30) | OR=1.46 [0.99-2.15] | .056 | **.169** | NULL ✅ |

**Convergence:** Both methods show marginal uncorrected effect that FAILS Bonferroni correction → NULL result ROBUST

**Interpretation:**
- LPM: 1.85 percentage point difference (marginal, p_bonf=.130)
- GEE: Odds ratio 1.46 (46% higher odds, marginal, p_bonf=.169)
- Both methods agree: Effect exists at uncorrected level but NOT significant after multiple comparison correction
- NULL result is METHODOLOGICALLY ROBUST (not artifact of LPM assumptions)

---

### Files Created

1. code/step03b_gee_validation.py
2. data/step03b_gee_results.csv
3. data/step03b_gee_contrasts.csv
4. data/step03b_gee_model_summary.txt
5. logs/step03b_gee_validation.log
6. PLATINUM_FINALIZATION_REPORT.md

---

### glmm_candidates.md Update

**Line 59 updated:**
- **Before:** "GEE recommended but NOT DONE"
- **After:** "GEE validated (p_bonf=.169) ✅ NULL CONFIRMED"

**Added to schema pattern summary:**
- Validated "Quadruple NULL" schema pattern (later revised to "Baseline Effects, Trajectory Nulls")
- RQ 6.5.3 is the ONLY schema RQ with TRUE NULL in BOTH IRT→LMM AND GLMM/GEE

---

### Protocol for Future Binary Outcome Validations

**When to use GEE instead of LMM:**
- Outcome variable is binary (0/1)
- LPM used originally (concerns about predicted probabilities outside [0,1])
- Within-subject correlation structure needs explicit modeling

**GEE Model Specification (Template):**
```python
import statsmodels.api as sm
from statsmodels.genmod.generalized_estimating_equations import GEE
from statsmodels.genmod.families import Binomial
from statsmodels.genmod.cov_struct import Exchangeable

# Fit GEE
model = GEE(
    endog=df['binary_outcome'],
    exog=sm.add_constant(df[predictors]),
    groups=df['participant_id'],
    family=Binomial(),
    cov_struct=Exchangeable()
)
result = model.fit()
```

**Validation Criteria:**
- Check convergence (result.converged == True)
- Compare to LPM: Similar p-values → method-invariant result
- Interpret OR (odds ratios) from GEE vs β (probability differences) from LPM
- Apply multiple comparison correction (Bonferroni) to both

**Execution Time:** ~10-30 seconds for N=7,200 observations

---

**End of Entry**
