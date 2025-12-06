# RQ 6.4.4: Is confidence decline more trait-like for some paradigms?

**Chapter:** 6
**Type:** Paradigm Confidence
**Subtype:** ICC by Paradigm
**Full ID:** 6.4.4

---

## Research Question

**Primary Question:**
Is confidence decline (trajectory slope) more trait-like for some memory paradigms than others?

**Scope:**
This RQ examines individual differences in confidence trajectory slopes across three retrieval paradigms: Free Recall (IFR), Cued Recall (ICR), and Recognition (IRE). Analysis uses IRT-derived confidence ability estimates (theta_confidence) from RQ 6.4.1 across four test sessions (T1, T2, T3, T4; nominal Days 0, 1, 3, 6). N=100 participants x 4 tests x 3 paradigms = 1200 observations. Intraclass correlation coefficients (ICC) are computed separately for each paradigm to determine whether forgetting slopes show trait-like variance (stable individual differences) or state-like variance (random fluctuation).

**Theoretical Framing:**
Free Recall (most challenging) may show highest ICC_slope if individual differences are more pronounced under cognitive demand. Alternatively, all paradigms may show minimal slope ICC, paralleling Chapter 5 accuracy findings where ICC_slope H 0 across all analyses. This RQ tests whether the 5-level confidence data reveals slope variance that dichotomous accuracy data missed, and whether this variance differs by retrieval support level.

---

## Theoretical Background

**Relevant Theories:**
- **Trait vs State Memory Theory**: Individual differences can be trait-like (stable across contexts, high ICC) or state-like (context-dependent, low ICC). High ICC_slope for confidence trajectories would indicate stable individual differences in metacognitive monitoring decline rates.
- **Retrieval Support Theory**: Free Recall (minimal support), Cued Recall (moderate support), and Recognition (maximum support) differ in cognitive demand. Higher demand may amplify individual differences, leading to higher ICC_slope for Free Recall.
- **Dual-Process Theory**: Recognition relies on familiarity (fast, automatic), while Free Recall requires recollection (slow, effortful). If metacognitive monitoring tracks retrieval processes, ICC patterns may differ by paradigm.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
Free Recall may show highest ICC_slope (individual differences magnified under high cognitive demand). Alternatively, all paradigms may show ICC_slope H 0, paralleling Chapter 5 accuracy findings where retrieval support affected baseline but not slope variance. If 5-level confidence data reveals slope variance (as hypothesized in RQ 6.1.4), this variance may be paradigm-specific.

**Literature Gaps:**
[To be identified by rq_scholar]

---

## Hypothesis

**Primary Hypothesis:**
Free Recall may show highest ICC_slope (most variability in challenging task). Alternatively, all paradigms may show ICC_slope H 0, replicating Chapter 5 findings. Comparison to Ch5 5.3.7 will determine if paradigm-specific slope variance exists for confidence but not accuracy.

**Secondary Hypotheses:**
If ICC_slope differs by paradigm, this indicates that retrieval support moderates trait-like individual differences in metacognitive monitoring decline. If ICC_slope is uniformly low across paradigms (H 0), this confirms that confidence decline rates are state-like (random fluctuation) regardless of retrieval paradigm.

**Theoretical Rationale:**
Chapter 5 5.3.7 found minimal slope variance for accuracy across all paradigms (ICC_slope H 0). If confidence shows similar pattern, this confirms that forgetting rates are fundamentally state-like regardless of measurement (accuracy vs confidence) or retrieval support. However, if 5-level confidence data reveals paradigm-specific slope variance, this would indicate that dichotomous accuracy data underestimated trait variance.

**Expected Effect Pattern:**
ICC_intercept > 0.30 for all paradigms (baseline confidence shows individual differences). ICC_slope tested separately per paradigm. If Free Recall shows ICC_slope > 0.10 while Cued/Recognition show ICC_slope H 0, this indicates paradigm-specific trait variance. Comparison to Ch5 5.3.7 ICC values critical for interpretation.

---

## Memory Domains

**Domains Examined:**

- [ ] **What** (Object Identity)
  - Tag Code: `-N-`
  - Not examined in this RQ (paradigm analysis aggregates across domains)

- [ ] **Where** (Spatial Location)
  - Tag Codes: `-L-`, `-U-`, `-D-`
  - Not examined in this RQ (paradigm analysis aggregates across domains)

- [ ] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Not examined in this RQ (paradigm analysis aggregates across domains)

**Paradigms Examined:**

- [x] **Free Recall (IFR)** - Minimal retrieval support
- [x] **Cued Recall (ICR)** - Moderate retrieval support
- [x] **Recognition (IRE)** - Maximum retrieval support

**Inclusion Rationale:**
This RQ focuses on paradigm-specific ICC decomposition, not domain-specific effects. All three interactive retrieval paradigms (IFR, ICR, IRE) are included. Passive paradigms (RFR, TCR, RRE) are excluded as they were not included in confidence IRT calibration (RQ 6.4.1).

**Exclusion Rationale:**
Room Free Recall (RFR), Trivia Cued Recall (TCR), and Recognition (RRE) excluded as they represent passive (non-interactive) paradigms and are not part of the WWW episodic memory framework central to this thesis.

---

## Analysis Approach

**Analysis Type:**
Linear Mixed Models (LMM) for trajectory modeling + Intraclass Correlation Coefficient (ICC) decomposition

**High-Level Workflow:**

**Step 1:** Fit paradigm-stratified LMMs with random slopes
- Three separate LMMs (one per paradigm: IFR, ICR, IRE)
- Model structure: theta_confidence ~ Time + (Time | UID)
- Random slopes allow individual differences in confidence decline rate per paradigm

**Step 2:** Extract variance components per paradigm
- var_intercept: variance in baseline confidence (Day 0)
- var_slope: variance in confidence decline rate
- cov_int_slope: covariance between intercept and slope
- var_residual: within-person residual variance

**Step 3:** Compute ICC per paradigm
- ICC_intercept: proportion of baseline variance explained by between-person differences
- ICC_slope_simple: proportion of slope variance explained by between-person differences (unconditional)
- ICC_slope_conditional: proportion of slope variance at Day 6 accounting for intercept-slope correlation

**Step 4:** Compare ICC_slope across paradigms
- Test if Free Recall shows higher ICC_slope than Cued Recall or Recognition
- Determine if paradigm moderates trait-like individual differences in confidence decline

**Step 5:** Compare to Ch5 5.3.7
- Extract Ch5 5.3.7 ICC values for accuracy across paradigms
- Test if confidence ICC_slope differs from accuracy ICC_slope
- Determine if 5-level data reveals variance that dichotomous data missed

**Expected Outputs:**
- data/step02_variance_components.csv (variance components for all 3 paradigms)
- data/step03_icc_estimates.csv (ICC values for all 3 paradigms)
- results/step05_paradigm_icc_comparison.csv (ICC comparison across paradigms)
- results/step06_ch5_comparison.csv (comparison to Ch5 5.3.7 accuracy ICC values)

**Success Criteria:**
- All 3 paradigm-stratified LMMs converge successfully
- Variance components extracted with finite values (no negative variances)
- ICC values computed in valid range [0, 1]
- Comparison to Ch5 5.3.7 documented with interpretation of accuracy vs confidence ICC differences
- If ICC_slope differs significantly across paradigms, paradigm-specific trait variance is documented

---

## Data Source

**Data Type:**
DERIVED (from RQ 6.4.1 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 6.4.1 (Paradigm Confidence Trajectories)

**File Paths:**
- results/ch6/6.4.1/data/step03_theta_confidence_paradigm.csv (1200 rows: 100 participants x 4 tests x 3 paradigms)

**Dependencies:**
RQ 6.4.1 must complete Steps 0-3 (data extraction, IRT calibration with 3-factor GRM for IFR/ICR/IRE, purification, final theta estimation) before this RQ can run.

**Comparison Data:**
- results/ch5/5.3.7/data/step03_icc_estimates.csv (Ch5 accuracy ICC values by paradigm)

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants from RQ 6.4.1 (inherited inclusion criteria, N=100)

**Items:**
- N/A (theta scores already aggregated per paradigm per participant per test)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4; nominal Days 0, 1, 3, 6)
- Inherited from RQ 6.4.1

**Paradigms:**
- [x] Free Recall (IFR)
- [x] Cued Recall (ICR)
- [x] Recognition (IRE)
- [ ] Room Free Recall (RFR) - EXCLUDED (passive paradigm)
- [ ] Trivia Cued Recall (TCR) - EXCLUDED (passive paradigm)
- [ ] Recognition RRE (RRE) - EXCLUDED (passive paradigm)

---
