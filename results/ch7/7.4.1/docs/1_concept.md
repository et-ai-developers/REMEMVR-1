# RQ 7.4.1: Does RAVLT Free Recall predict REMEMVR Free Recall > Recognition?

**Chapter:** 7
**Type:** Process-Specific Prediction
**Subtype:** Transfer-appropriate processing validation
**Full ID:** 7.4.1

---

## Research Question

**Primary Question:**
Does RAVLT (a verbal free recall task) show stronger prediction for REMEMVR Free Recall than Recognition, consistent with process-specific transfer?

**Scope:**
This RQ examines bivariate correlations between RAVLT Total scores and REMEMVR paradigm-specific theta scores (Free Recall vs Recognition) across N=100 participants. Uses Steiger's Z-test to compare dependent correlations with alpha = 0.00179 (chapter-level correction).

**Theoretical Framing:**
Process-specific transfer hypothesis suggests that tasks sharing similar cognitive processes show stronger correlations than tasks with different processes. RAVLT and REMEMVR Free Recall both require generative retrieval (self-initiated search), while Recognition relies on familiarity-based judgments.

---

## Theoretical Background

**Relevant Theories:**
- **Transfer-Appropriate Processing (TAP)** (Morris et al., 1977): Performance is better when encoding and retrieval processes match across tasks. Tasks requiring similar cognitive operations should show stronger correlations.
- **Dual-Process Theory** (Yonelinas, 2002): Recognition memory can rely on both familiarity (fast, automatic) and recollection (slow, effortful), while free recall primarily requires recollection-based retrieval.

**Key Citations:**
Morris, C. D., Bransford, J. D., & Franks, J. J. (1977). Levels of processing versus transfer appropriate processing. Journal of Verbal Learning and Verbal Behavior, 16(5), 519-533.

**Theoretical Predictions:**
TAP predicts stronger correlations between RAVLT and REMEMVR Free Recall than between RAVLT and REMEMVR Recognition, due to shared generative retrieval processes. Dual-process theory supports this by suggesting Recognition can bypass the effortful search processes required for both RAVLT and Free Recall.

**Literature Gaps:**
Few studies have tested process-specific transfer between standardized neuropsychological tests and novel VR episodic memory tasks across different retrieval paradigms.

---

## Hypothesis

**Primary Hypothesis:**
r(RAVLT, REMEMVR_FreeRecall) > r(RAVLT, REMEMVR_Recognition). Both RAVLT and Free Recall require generative retrieval (self-initiated search), while Recognition relies more on familiarity-based processes.

**Secondary Hypotheses:**
Both correlations should be significant and positive, but the difference between them should favor Free Recall prediction.

**Theoretical Rationale:**
Transfer-appropriate processing suggests that tasks sharing similar cognitive processes (generative retrieval) will show stronger associations. RAVLT Total requires active search and generation of verbal material from memory, similar to REMEMVR Free Recall but unlike REMEMVR Recognition which can rely on familiarity judgments.

**Expected Effect Pattern:**
Expected correlations: r(RAVLT, FreeRecall) H 0.45, r(RAVLT, Recognition) H 0.28. Steiger's Z-test should show significant difference (Z > 1.96, p < 0.05) supporting process-specificity hypothesis.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Included in paradigm-specific theta scores

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Description: Included in paradigm-specific theta scores

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Included in paradigm-specific theta scores

**Inclusion Rationale:**
Uses paradigm-specific theta scores from Ch5 5.3.x that aggregate across all episodic memory domains (What/Where/When) but separate by retrieval paradigm (Free Recall vs Recognition vs Cued Recall).

**Exclusion Rationale:**
Cued Recall paradigm excluded as it represents intermediate process between Free Recall (generative) and Recognition (familiarity), potentially complicating process-specific predictions.

---

## Analysis Approach

**Analysis Type:**
Bivariate correlation analysis with dependent correlation comparison using Steiger's Z-test

**High-Level Workflow:**

**Step 1:** Extract and prepare data
- Load paradigm-specific theta scores from Ch5 5.3.x results
- Extract RAVLT_Total scores from dfnonvr.csv (raw scores, not T-scored)
- Compute mean theta scores per participant for Free Recall and Recognition paradigms
- Check data quality and missingness

**Step 2:** Compute bivariate correlations
- r1 = cor(RAVLT_Total, Theta_FreeRecall)
- r2 = cor(RAVLT_Total, Theta_Recognition)
- Compute 95% confidence intervals for both correlations
- Report BOTH uncorrected AND corrected p-values (Decision D068)

**Step 3:** Test process-specificity hypothesis
- Steiger's Z-test for dependent correlations: H1: r1 > r2
- Alpha = 0.00179 (chapter-level Bonferroni correction)
- Effect size: difference in correlation coefficients (r1 - r2)

**Step 4:** Visualize relationships
- Scatter plots with regression lines for both correlations
- Difference in slopes should be visually apparent
- Include confidence bands around regression lines

**Step 5:** Sensitivity analyses
- Bootstrap confidence intervals (1000 iterations) for correlation difference
- Exclude potential outliers and recompute correlations
- Alternative: Use Spearman correlations for robustness check

**Expected Outputs:**
- data/step01_cognitive_tests.csv (extracted RAVLT scores)
- data/step02_paradigm_theta.csv (mean theta per participant by paradigm)
- data/step03_correlation_input.csv (merged analysis dataset)
- data/step04_correlation_results.csv (r values, CIs, dual p-values)
- data/step05_steiger_test.csv (Z-test results for dependent correlations)
- data/step06_bootstrap_results.csv (bootstrap CIs for sensitivity)
- results/process_specificity_summary.md (text summary for thesis)
- plots/ravlt_correlation_comparison.png (scatter plots)

**Success Criteria:**
- [ ] Both correlations significant (p < 0.00179 after correction)
- [ ] r_FreeRecall > r_Recognition in expected direction
- [ ] Steiger's Z-test significant (p < 0.05) confirming difference
- [ ] Effect size meaningful (|r1 - r2| > 0.10)
- [ ] Bootstrap CIs exclude zero for correlation difference
- [ ] No extreme outliers (standardized residuals within 3)
- [ ] Visual plots show clear difference in regression slopes

---

## Data Source

**Data Type:**
DERIVED (from Ch5 5.3.x paradigm outputs + master.xlsx cognitive tests)

### DERIVED Data Sources:

**Source RQ:**
Ch5 5.3.x (Paradigm-specific analyses - Free Recall, Cued Recall, Recognition)

**File Paths:**
- results/ch5/5.3.1/data/step03_theta_scores.csv (or similar paradigm analysis)
- data/cache/master.xlsx (RAVLT cognitive test scores)

**Dependencies:**
Ch5 5.3.x must complete IRT calibration and theta estimation before this RQ can run. Specifically requires paradigm-separated theta scores for Free Recall (IFR) and Recognition (IRE) paradigms.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants from Ch5 paradigm analyses
- [ ] Exclude: Any participants with missing RAVLT or incomplete paradigm data

**Items:**
- [x] All items contributing to paradigm-specific theta scores
- [x] Free Recall paradigm (IFR) items only for Theta_FreeRecall
- [x] Recognition paradigm (IRE) items only for Theta_Recognition

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4) contributing to paradigm theta aggregation
- [x] RAVLT baseline cognitive assessment

---