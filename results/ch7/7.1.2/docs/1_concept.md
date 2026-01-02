# RQ 7.1.2: Do tests predict intercept (Day 0) vs slope (forgetting)?

**Chapter:** 7
**Type:** Predictive Validity (Core)
**Subtype:** Intercept vs Slope Prediction
**Full ID:** 7.1.2

---

## Research Question

**Primary Question:**
Do cognitive tests predict baseline ability (Day 0 intercept) more than forgetting rate (slope), consistent with tests measuring encoding but not consolidation?

**Scope:**
100 participants analyzed for individual differences in intercept (baseline ability) and slope (forgetting rate) from LMM random effects

**Theoretical Framing:**
Investigates whether traditional cognitive tests capture encoding/retrieval mechanisms (reflected in intercept) versus consolidation processes (reflected in slope) in multi-day episodic memory

---

## Theoretical Background

**Relevant Theories:**
Two-process theory (Craik & Rose, 2012) distinguishes encoding from consolidation processes in memory. Traditional cognitive tests measure encoding/retrieval over 20-30 minutes, not multi-day consolidation.

**Key Citations:**
Craik & Rose (2012) - Two-process theory of encoding vs consolidation
Eichenbaum (2014) - Hippocampal sequence encoding mechanisms

**Theoretical Predictions:**
If cognitive tests primarily measure encoding capacity, they should predict Day 0 performance (intercept) strongly but show weak associations with forgetting rate (slope) across days.

**Literature Gaps:**
Limited research examining whether traditional tests predict forgetting rates in ecologically valid multi-day paradigms versus immediate performance.

---

## Hypothesis

**Primary Hypothesis:**
Cognitive tests predict intercept strongly (R² > 0.30) but slope weakly (R² < 0.10)

**Secondary Hypotheses:**
- RAVLT and BVMT show stronger intercept prediction than slope prediction
- RPM shows similar weak prediction for both intercept and slope
- R²_intercept significantly greater than R²_slope (bootstrap CI excludes 0)

**Theoretical Rationale:**
Traditional tests measure encoding/retrieval over minutes, not multi-day consolidation processes. Ch5 established power-law forgetting with individual differences in slope (ICC_slope = 21% under model averaging).

**Expected Effect Pattern:**
- Intercept prediction: R² = 0.38, RAVLT_beta = 0.35***, BVMT_beta = 0.28**, RPM_beta = 0.15
- Slope prediction: R² = 0.08, all betas < 0.15, non-significant
- R²_intercept - R²_slope = 0.30, 95% CI [0.18, 0.42]

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Included in overall theta_all scores from Ch5 5.1.1

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Description: Included in overall theta_all scores from Ch5 5.1.1

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Included in overall theta_all scores from Ch5 5.1.1

**Inclusion Rationale:**
Uses omnibus theta_all scores from Ch5 5.1.1 that aggregate across all episodic memory domains to examine overall encoding vs consolidation prediction patterns.

**Exclusion Rationale:**
Domain-specific analysis is addressed separately in RQ 7.1.3.

---

## Analysis Approach

**Analysis Type:**
Multiple Regression with differential prediction analysis

**High-Level Workflow:**

**Step 1:** Extract random effects from LMM
- Use model-averaged predictions from Ch5 5.1.1
- Extract BLUPs: Intercept_i (Day 0 ability), Slope_i (forgetting rate)
- Alternative: Re-fit LMM: `Theta ~ log_Days + (1 + log_Days | UID)`

**Step 2:** Predict intercepts
- Model: `Intercept ~ RAVLT_T + BVMT_T + RPM_T`
- Report R², beta coefficients

**Step 3:** Predict slopes
- Model: `Slope ~ RAVLT_T + BVMT_T + RPM_T`
- Report R², beta coefficients

**Step 4:** Compare R² values
- Bootstrap 95% CI for R²_intercept - R²_slope
- Hypothesis: R²_intercept >> R²_slope

**Step 5:** Test differential prediction
- Fisher's Z-test for comparing model R²

**Expected Outputs:**
- data/step01_random_effects.csv (extracted intercepts and slopes)
- data/step02_cognitive_tests.csv (RAVLT, BVMT, RPM T-scores)
- data/step03_intercept_analysis.csv (intercept regression results)
- data/step04_slope_analysis.csv (slope regression results)
- data/step05_comparison_results.csv (R² difference testing)
- results/differential_prediction_summary.md (text summary)
- plots/intercept_vs_slope_prediction.png (visualization)

**Success Criteria:**
- [ ] R²_intercept > 0.25
- [ ] R²_slope < 0.15
- [ ] R²_intercept significantly > R²_slope (bootstrap CI excludes 0)
- [ ] No individual predictor significantly predicts slope

---

## Data Source

**Data Type:**
DERIVED (from Ch5 5.1.1 outputs + master.xlsx cognitive tests)

### DERIVED Data Sources:

**Source RQ:**
Ch5 5.1.1 (General episodic memory LMM with random intercepts and slopes)

**File Paths:**
- results/ch5/5.1.1/data/step03_lmm_random_effects.csv (individual intercepts/slopes)
- data/cache/master.xlsx (cognitive test scores)

**Dependencies:**
Ch5 5.1.1 must complete successfully before this RQ can run

### Cognitive Test Variables (master.xlsx):

**RAVLT:**
- Tag patterns: `{UID}-COG-X-RAV-T1Sc` through `T5Sc`
- Computed score: RAVLT_Total = sum(T1-T5), converted to T-scores

**BVMT:**
- Tag patterns: `{UID}-COG-X-BVM-TotR`
- Computed score: BVMT_Total, converted to T-scores

**RPM:**
- Tag pattern: `{UID}-COG-X-RPM-Scor`
- Computed score: RPM raw score, converted to T-scores

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants with complete cognitive test data
- [ ] Subset: Exclude if missing any of RAVLT, BVMT, RPM

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4) from Ch5 5.1.1 theta scores
- [x] Cognitive battery: RAVLT, BVMT, RPM (excluding NART due to language validity concerns)

**Statistical Standards:**
- Chapter-level alpha: 0.05/28 = 0.00179
- Bonferroni correction for multiple predictors: 0.00179/3 = 0.000597 per predictor
- Missing data: Listwise deletion, report final n per analysis

---