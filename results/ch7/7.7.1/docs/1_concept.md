# RQ 7.7.1: Reverse Inference - Can REMEMVR predict RAVLT?

**Chapter:** 7
**Type:** Clinical Utility
**Subtype:** Reverse Inference
**Full ID:** 7.7.1

---

## Research Question

**Primary Question:**
Can REMEMVR performance predict standard test performance (RAVLT, BVMT)? If REMEMVR is a "purer" episodic measure, it should predict traditional tests.

**Scope:**
This RQ examines reverse prediction from REMEMVR theta scores to cognitive test scores. Uses bidirectional comparison: tests ’ REMEMVR (forward) vs REMEMVR ’ tests (reverse). N=100 participants with complete REMEMVR data from Ch5 and cognitive test scores from master.xlsx.

**Theoretical Framing:**
Reverse inference tests whether REMEMVR contains the construct measured by traditional tests. If REMEMVR fully encompasses RAVLT's construct, REMEMVR ’ RAVLT should be strong. Asymmetry in prediction strength reveals unique variance captured by each measure.

---

## Theoretical Background

**Relevant Theories:**
- **Reverse Inference Framework**: If REMEMVR is a "purer" episodic measure, it should predict traditional tests strongly while tests may predict REMEMVR less completely due to task-specific variance.
- **Construct Validity Theory**: Bidirectional prediction reveals construct overlap - symmetric prediction suggests shared construct, asymmetric prediction suggests one measure is a subset of another.

**Key Citations:**
[To be enhanced by rq_scholar]

**Theoretical Predictions:**
Reverse inference tests whether REMEMVR contains the construct measured by traditional tests. If REMEMVR fully encompasses RAVLT's construct, REMEMVR ’ RAVLT should be strong. If forward > reverse, tests contain unique construct REMEMVR doesn't measure. If reverse > forward, REMEMVR is a superset of tests.

**Literature Gaps:**
Limited research on ecological memory measures predicting traditional neuropsychological tests. Most validation studies examine forward prediction only (tests ’ real-world performance).

---

## Hypothesis

**Primary Hypothesis:**
Bidirectional prediction - tests predict REMEMVR and REMEMVR predicts tests, but neither completely explains the other. Expected moderate reverse prediction (R² = 0.25-0.35) suggesting shared but not identical constructs.

**Secondary Hypotheses:**
Forward prediction (7.1.1) should be stronger than reverse prediction, as traditional tests capture additional variance (crystallized abilities, test-taking strategies) beyond pure episodic memory that REMEMVR measures.

**Theoretical Rationale:**
REMEMVR measures ecological episodic memory in isolation, while RAVLT/BVMT involve additional cognitive processes (attention, working memory, strategy use). This predicts asymmetric bidirectional relationships.

**Expected Effect Pattern:**
Forward R² (Tests’REMEMVR) = 0.35, Reverse R² (REMEMVR’RAVLT) = 0.28, Reverse R² (REMEMVR’BVMT) = 0.22. REMEMVR predicts traditional tests moderately, confirming shared construct but incomplete overlap.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Included in overall theta_all scores

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Description: Included in overall theta_all scores

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Included in overall theta_all scores

**Inclusion Rationale:**
Uses omnibus theta_all scores from Ch5 5.1.1 that aggregate across all episodic memory domains. This provides comprehensive REMEMVR ability estimate for predicting traditional tests.

**Exclusion Rationale:**
No domain-specific exclusions. Analysis requires comprehensive episodic memory measure for meaningful comparison with traditional omnibus tests (RAVLT Total, BVMT Total Recall).

---

## Analysis Approach

**Analysis Type:**
Multiple regression with hierarchical entry and cross-validation

**High-Level Workflow:**

**Step 1:** Extract and prepare data
- Load mean theta_all scores from Ch5 5.1.1 results
- Extract RAVLT_Total and BVMT_TotR from master.xlsx  
- Standardize all variables to T-scores (M=50, SD=10)
- Check data quality and missingness

**Step 2:** Reverse regression models
- Model 1: RAVLT_Total ~ REMEMVR_Theta (reverse prediction)
- Model 2: BVMT_TotR ~ REMEMVR_Theta (reverse prediction)
- Report R², beta coefficients with 95% CIs

**Step 3:** Compare to forward regression
- Extract forward R² values from RQ 7.1.1 results
- Compute asymmetry ratios: Forward R² / Reverse R²
- Test difference in prediction strength

**Step 4:** Effect sizes and importance
- Cohen's f² = R²/(1-R²)
- Semi-partial correlations for unique variance
- Bootstrap CIs (1000 iterations)

**Step 5:** Model diagnostics
- Multicollinearity: VIF < 5
- Residual normality: Shapiro-Wilk test, Q-Q plot
- Homoscedasticity: Breusch-Pagan test
- Influential points: Cook's D < 4/N

**Step 6:** Cross-validation
- Method: 5-fold CV
- Metrics: Test R², RMSE, MAE
- Check for overfitting

**Step 7:** Statistical significance
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Primary correction: Bonferroni (± = 0.05/28 = 0.00179)
- Secondary: FDR for comparison

**Step 8:** Power analysis
- Post-hoc power for observed effects
- Sensitivity: smallest detectable effect at 80% power

**Expected Outputs:**
- data/step01_cognitive_tests.csv (RAVLT, BVMT scores)
- data/step02_theta_means.csv (mean theta_all per participant)
- data/step03_analysis_input.csv (merged analysis dataset)
- data/step04_reverse_regression.csv (reverse model results)
- data/step05_forward_comparison.csv (comparison with 7.1.1)
- data/step06_effect_sizes.csv (R², f², with 95% CIs)
- data/step07_model_diagnostics.csv (VIF, residuals, Cook's D)
- data/step08_cross_validation.csv (CV results)
- data/step09_power_analysis.csv (post-hoc and sensitivity)
- results/reverse_inference_summary.md (text summary for thesis)
- plots/reverse_prediction_scatter.png (REMEMVR predicting tests)

**Success Criteria:**
- Reverse models explain significant variance (p < 0.00179)
- R² between 0.20 and 0.40 (meaningful but not redundant)
- Forward vs reverse comparison shows interpretable asymmetry
- VIF < 5 (no multicollinearity issues)
- Residuals normally distributed (Shapiro-Wilk p > 0.05)
- Homoscedasticity confirmed (Breusch-Pagan p > 0.05)
- No influential outliers (Cook's D < 4/N)
- Cross-validation R² within 15% of training R²
- Power > 0.80 for medium effect (f² = 0.15)

---

## Data Source

**Data Type:**
DERIVED (from Ch5 5.1.1 outputs + master.xlsx cognitive tests)

### DERIVED Data Sources:

**Source RQ:**
Ch5 5.1.1 (Functional Form Comparison - provides omnibus theta_all scores)

**File Paths:**
- results/ch5/5.1.1/data/step03_theta_scores.csv (theta_all estimates)
- data/cache/master.xlsx (RAVLT_Total, BVMT_TotR cognitive test scores)

**Dependencies:**
Ch5 5.1.1 must complete through Step 3 (final theta estimation) before this RQ can run

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants with complete REMEMVR data
- [x] Must have both theta_all scores and cognitive test scores
- [ ] Exclude: Participants missing either REMEMVR or cognitive data

**Items:**
- N/A (uses aggregated theta_all scores, not item-level data)

**Tests:**
- [x] All 4 REMEMVR tests (T1, T2, T3, T4) - aggregated in theta_all
- [x] RAVLT Total score (sum of T1-T5)
- [x] BVMT Total Recall (sum of trials 1-3)

---