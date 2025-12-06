# RQ 6.6.2: Individual Difference Predictors of High-Confidence Errors

**Chapter:** 6
**Type:** HCE (High-Confidence Errors)
**Subtype:** Profiles
**Full ID:** 6.6.2

---

## Research Question

**Primary Question:**
Who makes high-confidence errors? What individual difference variables predict the tendency to be highly confident when incorrect?

**Scope:**
This RQ examines HCE rates across N=100 participants over 4 test sessions. Individual-level HCE rate computed as mean across timepoints. Predictors examined: baseline accuracy (Day 0 theta from Ch5 5.1.1), baseline confidence (Day 0 theta from RQ 6.1.1), age (from dfData.csv), and confidence bias (defined as Mean(confidence) - Mean(accuracy) at Day 0).

**Theoretical Framing:**
High-confidence errors represent metacognitive failure: the inability to distinguish known from unknown information. Understanding who makes HCEs reveals whether this failure is due to poor memory (can't remember), poor metacognition (can't judge), overconfidence bias, or age-related decline. Critical test of Dunning-Kruger hypothesis in episodic memory domain.

---

## Theoretical Background

**Relevant Theories:**
- **Dunning-Kruger Effect** (Kruger & Dunning, 1999): Low performers overestimate competence due to metacognitive deficits. Predicts low baseline accuracy -> high HCE rate.
- **Metacognitive Signal Detection** (Fleming & Lau, 2014): Confidence judgments reflect noisy signal detection process. Poor metacognitive sensitivity produces miscalibration and HCEs.
- **Dual-Process Theory** (Yonelinas, 2002): Familiarity-based responses generate false confidence (feels familiar but is incorrect). High reliance on familiarity may predict more HCEs.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
- Dunning-Kruger: Low baseline accuracy predicts high HCE rate
- Metacognitive skill: Low baseline confidence predicts high HCE rate (poor self-knowledge)
- Confidence bias: High confidence bias (overconfidence) predicts high HCE rate
- Age: NULL expected (paralleling Ch5 universal age null pattern)

**Literature Gaps:**
Most HCE research focuses on semantic/general knowledge. Little work examining HCEs in episodic memory with ecologically valid encoding. VR paradigm allows examination of individual differences in natural forgetting context.

---

## Hypothesis

**Primary Hypothesis:**
Low baseline performers will show higher HCE rates, supporting Dunning-Kruger effect in episodic memory domain. High confidence bias individuals will make more HCEs due to general overconfidence tendency.

**Secondary Hypotheses:**
- Baseline confidence will negatively predict HCE rate (good self-knowledge protects against HCEs)
- Age will NOT significantly predict HCE rates, consistent with Ch5 universal age null findings (VR ecological encoding produces age-invariant memory and metacognition)

**Theoretical Rationale:**
HCEs result from combination of poor memory (forget the event) and poor metacognition (don't realize forgetting occurred). Low performers lack both accurate memory and metacognitive awareness to recognize errors. Confidence bias (overconfidence) indicates systematic miscalibration, predicting HCEs across all accuracy levels. Age nulls in Ch5 suggest VR encoding eliminates typical aging effects, so metacognitive aging effects should also be minimal.

**Expected Effect Pattern:**
Multiple regression: HCE_rate ~ Baseline_accuracy + Baseline_confidence + Age + Confidence_bias
- Baseline_accuracy: negative coefficient, p < 0.05 (low accuracy -> high HCE)
- Confidence_bias: positive coefficient, p < 0.05 (overconfidence -> high HCE)
- Baseline_confidence: negative coefficient, p < 0.05 (low confidence -> high HCE)
- Age: NULL, p > 0.05 (no age effect)

R-squared > 0.10 indicates meaningful individual difference variance explained.

---

## Memory Domains

**Domains Examined:**

- [x] **All Domains Combined** (Omnibus)
  - Description: HCE rates computed across all item types (What/Where/When combined)
  - Rationale: Individual difference analysis requires maximum statistical power from all items

**Inclusion Rationale:**
This RQ focuses on individual differences in HCE tendency, not domain-specific patterns. Using all items maximizes statistical power for detecting predictor effects. Domain-specific HCE patterns examined in separate RQ (6.6.3).

**Exclusion Rationale:**
No domain-level separation needed for this individual differences analysis.

---

## Analysis Approach

**Analysis Type:**
Multiple regression predicting individual-level HCE rates from baseline memory, metacognition, age, and bias variables

**High-Level Workflow:**

**Step 0:** Load HCE rates from RQ 6.6.1 (400 rows: 100 participants x 4 tests)
**Step 1:** Load predictor variables:
  - Baseline accuracy: Ch5 5.1.1 Day 0 theta scores
  - Baseline confidence: RQ 6.1.1 Day 0 theta scores
  - Age: From data/cache/dfData.csv
  - Confidence bias: Computed as Mean(confidence) - Mean(accuracy) at Day 0

**Step 2:** Compute individual-level HCE rate (mean HCE rate across 4 timepoints per participant, N=100 rows)

**Step 3:** Multiple regression: HCE_rate ~ Baseline_accuracy + Baseline_confidence + Age + Confidence_bias
  - Standardize predictors (z-scores) for effect size comparison
  - Report standardized coefficients (beta weights)
  - Dual p-values per Decision D068 (report both uncorrected and Bonferroni-corrected)

**Step 4:** Identify significant predictors:
  - Test each predictor coefficient against alpha = 0.05 (uncorrected)
  - Test against Bonferroni alpha = 0.0125 (4 predictors)
  - Report which predictors survive Bonferroni correction

**Step 5:** Effect sizes:
  - Standardized beta coefficients (already computed in Step 3)
  - R-squared (total variance explained)
  - Partial R-squared per predictor (unique variance explained)

**Expected Outputs:**
- data/step01_predictor_data.csv (100 rows: UID, HCE_rate, baseline_accuracy, baseline_confidence, age, confidence_bias)
- results/step02_regression_summary.txt (model fit statistics, R-squared, F-test)
- results/step03_significant_predictors.csv (coefficients, SE, t-values, dual p-values, significance flags)
- results/step04_effect_sizes.csv (beta weights, partial R-squared)

**Success Criteria:**
- 100 participants with complete predictor data (no missing values)
- Regression model converges successfully
- All 4 predictors tested with dual p-values (uncorrected + Bonferroni)
- Effect sizes computed for all predictors
- R-squared reported (expect > 0.10 for meaningful individual differences)
- Dunning-Kruger hypothesis testable (baseline_accuracy coefficient sign and significance)
- Age null hypothesis testable (age coefficient p-value)

---

## Data Source

**Data Type:**
DERIVED (from multiple prior RQ outputs)

### DERIVED Data Sources:

**Source RQs:**
1. **RQ 6.6.1** (HCE Over Time): High-confidence error rates
2. **Ch5 5.1.1** (Functional Form): Baseline accuracy theta scores
3. **RQ 6.1.1** (Confidence Model Selection): Baseline confidence theta scores
4. **dfData.csv**: Age variable

**File Paths:**
- results/ch6/6.6.1/data/step01_hce_rates.csv (400 rows: UID x test, HCE_rate per person-timepoint)
- results/ch5/5.1.1/data/step03_theta_scores.csv (400 rows, filter to T1/Day 0 for baseline accuracy)
- results/ch6/6.1.1/data/step03_theta_confidence.csv (400 rows, filter to T1/Day 0 for baseline confidence)
- data/cache/dfData.csv (extract Age variable)

**Dependencies:**
1. RQ 6.6.1 must complete Step 1 (HCE rate computation)
2. Ch5 5.1.1 must complete Step 3 (IRT theta estimation)
3. RQ 6.1.1 must complete Step 3 (IRT theta estimation for confidence)

**Derived Variable Construction:**
- **Individual HCE rate**: Mean of HCE_rate across 4 timepoints per participant (from 6.6.1)
- **Baseline accuracy**: Theta score from Ch5 5.1.1 at T1 (Day 0)
- **Baseline confidence**: Theta score from RQ 6.1.1 at T1 (Day 0)
- **Confidence bias**: baseline_confidence - baseline_accuracy (both z-standardized first, then difference)
- **Age**: Direct extraction from dfData.csv

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (inherited from prior RQs)
- [ ] Exclude participants missing any predictor variable (complete case analysis)
- Expected: N=100 complete cases

**Items:**
- N/A (analysis uses aggregated HCE rates, not item-level data)

**Tests:**
- [x] All 4 tests used to compute individual-level HCE rate (mean across timepoints)
- Baseline variables extracted from T1 (Day 0) only

---
