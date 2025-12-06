# RQ 6.1.4: ICC Decomposition

**Chapter:** 6
**Type:** Confidence
**Subtype:** ICC Decomposition
**Full ID:** 6.1.4

---

## Research Question

**Primary Question:**
Is confidence decline trait-like or state-like? Does 5-level ordinal data reveal slope variance that dichotomous accuracy data missed?

**Scope:**
This RQ examines intraclass correlation coefficients (ICC) using confidence trajectories from N=100 participants across 4 test sessions (T1, T2, T3, T4; Days 0, 1, 3, 6). The analysis decomposes variance into intercept (baseline confidence) and slope (confidence decline rate) components. Critically compares ICC estimates from 5-level ordinal confidence data versus dichotomous accuracy data from Chapter 5.

**Theoretical Framing:**
This RQ tests whether the apparent absence of trait-level forgetting rate variance in Chapter 5 (ICC_slope H 0.0005) was a methodological artifact of dichotomous data or a true reflection of minimal individual differences in forgetting dynamics. If 5-level ordinal confidence data reveals detectable slope variance (ICC_slope > 0.10), it demonstrates that ordinal data provides 2.3× more information per response and can detect trait variance that binary measures miss. If confidence ICC_slope H 0 as well, it confirms that forgetting rate truly shows minimal trait variance regardless of measurement precision.

---

## Theoretical Background

**Relevant Theories:**
- **Trait vs State Memory Framework**: Memory performance can be decomposed into stable individual differences (trait: intercept variance) versus situational fluctuations (state: residual variance). Forgetting rate variance tests whether decline trajectories are individualized (trait-like) or universal (state-like).
- **Psychometric Information Theory**: Ordinal polytomous data (5-level Likert) provides substantially more information per item than dichotomous data. Graded Response Model (GRM) for 5-category responses theoretically yields 2.3× more information than 2-parameter logistic (2PL) for binary responses. This increased precision may reveal latent variance that binary measures cannot detect.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
Two competing predictions:
1. **Measurement Artifact Hypothesis**: ICC_slope_confidence > 0.10 (detectable trait variance) while ICC_slope_accuracy H 0. This would suggest dichotomous accuracy data in Chapter 5 lacked precision to detect individual differences in forgetting rate, not that such differences don't exist.
2. **Universal Forgetting Hypothesis**: ICC_slope_confidence H 0, replicating Chapter 5 accuracy findings. This would confirm that forgetting rate shows minimal trait variance regardless of measurement precision, suggesting universal forgetting dynamics.

**Literature Gaps:**
[To be identified by rq_scholar - need evidence on whether ordinal vs binary data affects ICC estimation for longitudinal slopes]

---

## Hypothesis

**Primary Hypothesis:**
CRITICAL HYPOTHESIS: ICC_slope for confidence will exceed 0.10 (detectable with 5-level ordinal data) while Chapter 5 accuracy ICC_slope H 0.0005 (dichotomous data limitation).

**Secondary Hypotheses:**
- ICC_intercept (baseline confidence variance) will be substantial (> 0.30), paralleling Chapter 5 accuracy findings
- Intercept-slope correlation may emerge for confidence data if slope variance is detectable

**Theoretical Rationale:**
5-level Likert confidence items provide 2.3× more information per response than 0/1 accuracy items. This increased precision should enable detection of latent slope variance that dichotomous measures cannot resolve. If ICC_slope_confidence > 0.10 but ICC_slope_accuracy H 0, this proves the Chapter 5 finding was a measurement limitation, not a substantive conclusion about forgetting dynamics.

Conversely, if ICC_slope_confidence H 0 (replicating accuracy), it confirms that forgetting rate truly shows minimal trait variance - a substantive finding that forgetting trajectories are remarkably universal across individuals despite large baseline differences.

**Expected Effect Pattern:**
- ICC_intercept_confidence > 0.30 (substantial baseline variance)
- ICC_slope_confidence > 0.10 (detectable slope variance) OR ICC_slope_confidence H 0 (replicating accuracy)
- Critical comparison: |ICC_slope_confidence - ICC_slope_accuracy| tested for significant difference
- If ICC_slope differs, interpretation focuses on measurement (ordinal vs binary) effects on variance detection
- If ICC_slope replicates H 0, interpretation focuses on universal forgetting dynamics

---

## Memory Domains

**Domains Examined:**

- [x] **Omnibus "All" Factor**
  - Description: Single composite factor aggregating all interactive VR paradigm items (IFR, ICR, IRE) into omnibus confidence measure
  - Rationale: Parallels Chapter 5 General analysis structure (5.1.X series)

- [ ] **What** (Object Identity)
  - Tag Code: `-N-`
  - Status: Not examined (domain-specific analysis in RQ 6.3.X series)

- [ ] **Where** (Spatial Location)
  - Tag Codes: `-L-`, `-U-`, `-D-`
  - Status: Not examined (domain-specific analysis in RQ 6.3.X series)

- [ ] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Status: Not examined (domain-specific analysis in RQ 6.3.X series)

**Inclusion Rationale:**
This RQ uses the omnibus "All" factor to enable direct comparison with Chapter 5 RQ 5.1.4 (which also used omnibus factor). Domain-stratified ICC analyses are conducted separately in RQ 6.3.4.

**Exclusion Rationale:**
- Room Free Recall (RFR), Total Cued Recall (TCR), Room Recognition (RRE) paradigms excluded (non-interactive tasks)
- Focus on interactive paradigms (IFR, ICR, IRE) for consistency with Chapter 5 methodology

---

## Analysis Approach

**Analysis Type:**
Linear Mixed Model (LMM) variance decomposition with ICC computation

**High-Level Workflow:**

**Step 1:** Load best-fitting LMM from RQ 6.1.1 (functional form comparison winner with random intercepts and slopes)

**Step 2:** Extract variance components from LMM output:
- var_intercept: Random intercept variance (baseline confidence differences)
- var_slope: Random slope variance (forgetting rate differences)
- cov_int_slope: Covariance between intercept and slope
- var_residual: Residual variance (within-person fluctuation)

**Step 3:** Compute three ICC variants per Hoffman & Stawski (2009):
- ICC_intercept = var_intercept / (var_intercept + var_slope × time^2 + var_residual)
- ICC_slope_simple = var_slope / (var_slope + var_residual/time^2)
- ICC_slope_conditional = var_slope / (var_slope + var_residual) at Day 6 (144 hours)

**Step 4:** Extract 100 participant-level random effects (intercept + slope) for each participant (REQUIRED for downstream clustering in RQ 6.1.5)

**Step 5:** Test intercept-slope correlation (Do high baseline confidence individuals show faster or slower decline?)

**Step 6:** CRITICAL COMPARISON: Compare ICC_slope_confidence (from this RQ) versus ICC_slope_accuracy (from Chapter 5 RQ 5.1.4 = 0.0005):
- Test if difference is significant
- Interpret whether ordinal data reveals variance that dichotomous data missed
- Or whether both ICC_slope H 0 confirms universal forgetting pattern

**Expected Outputs:**
- data/step02_variance_components.csv (4 rows: var_intercept, var_slope, cov_int_slope, var_residual)
- data/step03_icc_estimates.csv (3 rows: ICC_intercept, ICC_slope_simple, ICC_slope_conditional)
- data/step04_random_effects.csv (100 rows, 1 per participant, REQUIRED for RQ 6.1.5)
- data/step05_intercept_slope_correlation.csv (correlation coefficient, p-value, interpretation)
- results/step06_ch5_icc_comparison.csv (CRITICAL: ICC_slope_confidence vs ICC_slope_accuracy = 0.0005)
- results/step06_interpretation.txt (Design effect vs measurement effect interpretation)

**Success Criteria:**
- All ICC values in [0, 1] range
- 100 random effects extracted (exactly N=100 participants)
- Intercept-slope correlation computed and tested
- CRITICAL: Chapter 5 comparison documented with explicit test of ICC_slope difference
- Interpretation addresses whether ordinal vs binary data explains any ICC differences
- Clear conclusion on Measurement Artifact vs Universal Forgetting hypothesis

---

## Data Source

**Data Type:**
DERIVED (from RQ 6.1.1 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 6.1.1 (Functional Form Comparison)

**File Paths:**
- results/ch6/6.1.1/data/step06_best_model.pkl (saved LMM model object with random effects structure)

**Dependencies:**
RQ 6.1.1 must complete Steps 1-6 (IRT calibration of 5-level ordinal confidence data using GRM, item purification, theta extraction, LMM functional form comparison, model selection via AIC/Akaike weights) before this RQ can run.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants from RQ 6.1.1 (N=100, inherited inclusion criteria)
- [ ] No additional exclusions

**Items:**
- N/A (analysis operates on theta scores, which aggregate across items)

**Tests:**
- [x] All 4 test sessions (T1, T2, T3, T4; Days 0, 1, 3, 6)
- [x] Inherited from RQ 6.1.1 (400 observations total)

**Critical Notes:**
- This RQ inherits the omnibus "All" factor structure from RQ 6.1.1
- Confidence data is 5-level ordinal (0, 0.25, 0.5, 0.75, 1.0 Likert scale)
- Comparison RQ is Chapter 5 RQ 5.1.4 (dichotomous accuracy data, 0/1 responses)
- The precision difference (5-level ordinal vs dichotomous) is the central theoretical question

---
