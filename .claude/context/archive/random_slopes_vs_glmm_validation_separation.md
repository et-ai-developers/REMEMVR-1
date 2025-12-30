# Random Slopes vs GLMM Validation - Methodological Separation

**Purpose:** Clarification that random slopes testing and GLMM validation are TWO INDEPENDENT methodological requirements

**Status:** Clarified 2025-12-29 21:00

**Key Principle:** Random slopes = model specification (universal); GLMM validation = methodological validation (single-construct RQs only)

---

## Methodological Clarification (2025-12-29 21:00)

**Archived from:** state.md Session (2025-12-29 21:00)
**Original Date:** 2025-12-29 21:00
**Reason:** Two separate issues frequently confused, needed explicit separation

---

### The Confusion

**Initial Problem:**
- User said "Option A: GLMM applies to ALL LMMs"
- Agent interpreted as: "All LMMs need random slopes AND GLMM validation"
- These are SEPARATE requirements with different applicability rules

---

### Random Slopes Testing (Universal Requirement)

**Applies To:** ALL LMMs without exception

**Purpose:** Model specification - do individual trajectories vary?

**Method:**
- Compare two models via Likelihood Ratio Test (LRT)
- Model 1: Intercepts-only `re_formula="~1"`
- Model 2: Intercepts+slopes `re_formula="~time_predictor"`
- Metrics: ΔAIC, LRT χ² statistic, p-value

**Decision Criteria:**
- ΔAIC > 10: Slopes strongly favored
- ΔAIC 4-10: Slopes moderately favored
- ΔAIC < 4: Intercepts acceptable
- LRT p < 0.05: Slopes significantly improve fit

**Documentation Required:**
- Section 4.4 in validation.md (MANDATORY)
- Must report ΔAIC and LRT results
- Document decision rationale

**User's Rule:** "All LMMs should test random slopes"
- Interpretation: UNIVERSAL requirement (not just GLMM candidates)
- Separate from GLMM validation applicability

---

### GLMM Validation (Conditional Requirement)

**Applies To:** Single-construct RQs testing group intercepts

**Exempt:** Difference-score RQs (calibration), variance decomposition RQs, slope-focused RQs

**Purpose:** Methodological validation - does IRT→LMM aggregation miss intercept effects?

**Method:**
- Extract item-level data (N=28,800)
- Fit GLMM with crossed random effects `(1|UID) + (1|Item)`
- Compare fixed effects to IRT→LMM
- Inspect BOTH p-values AND effect sizes

**Decision Criteria:**
- GLMM changes p<0.05 AND β≠0: Real effect detected
- GLMM changes p<0.05 BUT β=0: Artifact (NULL confirmed)
- GLMM unchanged: IRT→LMM adequate

**Documentation Required:**
- Section in validation.md (variable presence)
- Must report effect sizes + confidence intervals (not just p-values)
- Explain interpretation (real effect vs artifact)

---

### Independence of Requirements

**Example 1: Single-Construct RQ**
- ✅ Random slopes testing: REQUIRED (universal)
- ✅ GLMM validation: REQUIRED (tests intercepts, single construct)

**Example 2: Calibration RQ**
- ✅ Random slopes testing: REQUIRED (universal)
- ❌ GLMM validation: EXEMPT (difference score, technical impossibility)

**Example 3: Variance Decomposition RQ**
- ✅ Random slopes testing: REQUIRED (universal)
- ❌ GLMM validation: NOT NEEDED (no group intercepts tested)

**Example 4: Slope Interaction RQ**
- ✅ Random slopes testing: REQUIRED (universal)
- ❌ GLMM validation: NOT NEEDED (slopes-focused, not intercept-focused)

---

### Critical Distinction

**Two Separate Issues:**

1. **Model Specification (Random Slopes):**
   - Question: Do individual trajectories vary around group trajectory?
   - Applies to: ALL LMMs
   - Decision: Statistical test (ΔAIC, LRT)
   - Impact: Which random effects structure to use

2. **Methodological Validation (GLMM):**
   - Question: Does aggregation miss baseline/intercept effects?
   - Applies to: Single-construct RQs testing group intercepts
   - Decision: Evidence-based (RQ characteristics, precedents)
   - Impact: Whether IRT→LMM findings are robust

**Can have random slopes WITHOUT GLMM validation:**
- Yes, if RQ is exempt (calibration, variance decomposition, slopes-focused)
- Random slopes = model improvement (universal)
- GLMM = methodological check (conditional)

---

### Practical Workflow

**Step 1: Random Slopes Testing (ALWAYS)**
```
For every LMM:
1. Fit intercepts-only model
2. Fit intercepts+slopes model
3. Calculate ΔAIC and run LRT
4. Document in validation.md Section 4.4
5. Choose final model based on results
```

**Step 2: GLMM Validation Decision (CONDITIONAL)**
```
If RQ characteristics match:
  - Single construct (theta_accuracy, theta_confidence)
  - Tests group intercepts (Age, Domain, Paradigm, Schema)
  - NOT difference score (calibration)
  - NOT variance decomposition
  - NOT slopes-focused
Then:
  Run GLMM validation (with effect size inspection)
Else:
  Document exemption reason in validation.md
```

---

### RQ 6.3.3 Example

**Random Slopes Testing:**
- ✅ Completed (ΔAIC=141, LRT p<0.001)
- Outcome: Slopes massively improve fit
- Paradox: σ²_slope=0.000006 but still improves
- Decision: Use random slopes model

**GLMM Validation:**
- ✅ Completed (N=28,800 observations)
- Outcome: Domain p=0.540→0.014 BUT β=0.000
- Interpretation: Artifact (NULL confirmed)
- Decision: IRT→LMM adequate, GLMM strengthened NULL

**Independence Demonstrated:**
- Random slopes improved model (statistical criterion)
- GLMM validated NULL (methodological criterion)
- Both requirements met, separate purposes

---

### User's "All LMMs" Rule Clarified

**Original Statement:** "Option A: GLMM applies to ALL LMMs (All LMMs should have random slopes)"

**Refined Interpretation:**
1. **Random slopes:** YES, test for ALL LMMs (universal requirement)
2. **GLMM validation:** NO, only single-construct RQs testing intercepts (conditional requirement)

**Two independent statements:**
- "All LMMs should TEST random slopes" = TRUE (model specification)
- "All LMMs should undergo GLMM validation" = FALSE (methodological validation is conditional)

---

**Last Updated:** 2025-12-29 21:00
**Status:** ✅ CLARIFIED - TWO INDEPENDENT METHODOLOGICAL REQUIREMENTS SEPARATED
**Related Topics:** glmm_policy_clarified_single_construct_vs_difference_score, rq_6_3_3_platinum_certified_glmm_p_value_artifact
