# RQ 7.1.4: Unique REMEMVR variance unexplained by all predictors?

**Chapter:** 7
**Type:** Predictive Validity (Core)
**Subtype:** Incremental Validity Assessment
**Full ID:** 7.1.4

---

## Research Question

**Primary Question:**
What proportion of REMEMVR variance remains unexplained after accounting for ALL available predictors (cognitive tests, demographics, self-report)?

**Scope:**
This RQ examines the unique variance captured by REMEMVR theta scores after hierarchical regression with 3 blocks of predictors: demographics (Age, Sex, Education), cognitive tests (RAVLT_T, BVMT_T, NART_T, RPM_T), and self-report variables (DASS_Dep, DASS_Anx, DASS_Str, VR_Exp, Sleep). Analysis uses mean theta per UID across all 4 test sessions. N=100 participants with complete cognitive test data.

**Theoretical Framing:**
This question addresses REMEMVR's incremental validity - whether it captures meaningful memory variance beyond traditional measures. The "ecological validity gap" represents what REMEMVR was designed to measure: naturalistic encoding, multi-day consolidation, and confidence monitoring processes not captured by lab-based tests.

---

## Theoretical Background

**Relevant Theories:**
- **Incremental Validity** (Hunsley & Meyer, 2003): New measures should explain variance beyond existing measures to justify their use
- **Ecological Validity Gap** (Chaytor & Schmitter-Edgecombe, 2003): Traditional tests may miss real-world cognitive processes due to artificial lab conditions
- **Transfer-Appropriate Processing**: REMEMVR's naturalistic VR encoding may engage different processes than traditional verbal/visuospatial tests

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
Traditional tests should predict REMEMVR moderately (convergent validity) but substantial residual should remain (incremental validity). REMEMVR's unique components - naturalistic encoding, multi-day consolidation, confidence monitoring - should not be captured by brief lab tests.

**Literature Gaps:**
Few studies have examined incremental validity of ecological memory measures over traditional neuropsychological tests. Most validation studies focus on convergent validity without quantifying unique variance.

---

## Hypothesis

**Primary Hypothesis:**
Substantial residual (>50%) should remain unexplained after accounting for all available predictors, supporting REMEMVR's incremental validity. This "ecological validity gap" represents the signal REMEMVR was designed to capture.

**Secondary Hypotheses:**
- Block 2 (cognitive tests) should show largest increment over demographics
- Block 3 (self-report) should add minimal incremental variance  
- When domain should show highest residual due to measurement challenges
- True residual (after removing measurement error) should exceed 40%

**Theoretical Rationale:**
If traditional tests comprehensively measured episodic memory, they should fully explain REMEMVR variance. Substantial residual indicates REMEMVR captures additional processes: naturalistic encoding contexts, multi-day consolidation, confidence monitoring, and ecological transfer not assessed by traditional tests.

**Expected Effect Pattern:**
Hierarchical R² pattern: Demographics (~12%) < + Cognitive tests (~40%) < + Self-report (~44%). Final model explains <55% of variance. Cohen's f² for cognitive block should be large (>0.35), self-report block small (<0.15).

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object identity memory from REMEMVR theta scores

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location)
  - [x] `-U-` tags (pick-up location)  
  - [x] `-D-` tags (put-down location)
  - Disambiguation: All spatial location tags included

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order memory from REMEMVR theta scores

**Inclusion Rationale:**
Analysis uses overall theta (all domains combined) as primary DV, plus domain-specific residual analysis. All three domains included to examine whether some domains show higher residual variance than others.

**Exclusion Rationale:**
None - all episodic memory domains included in comprehensive incremental validity assessment.

---

## Analysis Approach

**Analysis Type:**
Hierarchical Multiple Regression with 3-block entry + Cohen's f² effect sizes + domain-specific residual analysis

**High-Level Workflow:**

**Step 1:** Extract and merge predictor data from master.xlsx (cognitive tests, demographics, self-report)
**Step 2:** Extract mean REMEMVR theta per UID from Ch5 results, compute T-scores for cognitive tests
**Step 3:** Build hierarchical regression with 3 blocks and cross-validation: Model 1 (demographics), Model 2 (+ cognitive tests), Model 3 (+ self-report)
- CRITICAL: Implement 5-fold cross-validation to assess model stability
- Report both training and test R² to detect overfitting
- Acceptable generalization gap: train-test R² difference < 0.10
**Step 4:** Compute incremental R² for each block with power analysis
- Delta_R²_block2 = R²_model2 - R²_model1
- Delta_R²_block3 = R²_model3 - R²_model2  
- F-test for each increment
- Post-hoc power analysis: Given N=100, 12 predictors, what effect size detectable at 80% power?
- Sensitivity analysis: minimum detectable f² with current sample
- If underpowered, acknowledge limitation in interpretation
**Step 5:** Calculate Cohen's f² effect sizes with interpretation
- f² = Delta_R² / (1 - R²_full)
- Interpret: 0.02=small, 0.15=medium, 0.35=large
- Report 95% CI for each f² using bootstrap
**Step 6:** Quantify unexplained variance with remedial actions
- Residual = 1 - R²_model3 (from cross-validated test set)
- Compute 95% CI for residual using bootstrap
- Separate measurement error from true residual using IRT theta SEs
- Remedial actions for assumption violations:
  - If normality violated: Report robust standard errors
  - If homoscedasticity violated: Use HC3 heteroscedasticity-consistent SEs
  - If multicollinearity detected (VIF > 5): Consider ridge regression
  - If outliers detected (Cook's D > 4/n): Report with and without outliers
**Step 7:** Repeat analysis for domain-specific theta scores (What, Where, When) to examine differential residuals
**Step 8:** Create variance decomposition visualization and prepare summary for thesis

**CRITICAL for Ch7 and multiple comparisons:**
- Report BOTH uncorrected AND Bonferroni-corrected p-values (Decision D068)
- Include model diagnostics (VIF < 5, residual normality, homoscedasticity)
- Include effect sizes with 95% CIs (R², f², partial eta²)
- Chapter-level alpha: 0.05/28 RQs = 0.00179 per RQ
- MANDATORY: 5-fold cross-validation to prevent overfitting
- Power analysis for each block's incremental validity
- Document all assumption checks and remedial actions taken

**Expected Outputs:**
- data/step01_cognitive_tests.csv (extracted and T-scored cognitive tests)
- data/step02_demographics.csv (age, sex, education data)
- data/step03_self_report.csv (DASS, VR experience, sleep data)
- data/step04_merged_predictors.csv (all predictors combined with theta scores)
- data/step05_hierarchical_models.csv (model comparison statistics)
- data/step06_variance_decomposition.csv (R², f², residuals by model)
- data/step07_domain_residuals.csv (residual analysis by What/Where/When)
- data/step08_incremental_validity_data.csv (plot source data)
- results/hierarchical_regression_summary.md (text summary for thesis)
- plots/variance_decomposition.png (visualization of explained vs unexplained variance)

**Success Criteria:**
- Block 2 (cognitive tests) significant increment (p < 0.00179)
- Total R² < 0.55 (at least 45% unexplained variance)
- True residual (after removing measurement error) > 40%
- When domain shows highest residual percentage
- Cohen's f² for cognitive block > 0.35 (large effect)
- Model diagnostics pass (VIF < 5, normality, homoscedasticity)

---

## Data Source

**Data Type:**
DERIVED (from Ch5 REMEMVR results) + RAW (from master.xlsx)

### DERIVED Data Source:

**Source RQ:**
Ch5 5.1.1 (overall REMEMVR theta scores) + Ch5 5.2.x (domain-specific theta scores)

**File Paths:**
- results/ch5/5.1.1/data/step03_theta_scores.csv (overall theta estimates)
- results/ch5/5.2.1/data/step03_theta_scores.csv (What domain theta)
- results/ch5/5.2.2/data/step03_theta_scores.csv (Where domain theta)  
- results/ch5/5.2.3/data/step03_theta_scores.csv (When domain theta)

**Dependencies:**
Ch5 analyses must complete IRT calibration and theta estimation before this RQ can run.

### RAW Data Source:

**Source File:**
data/cache/master.xlsx

**Tag Patterns:**
- Cognitive tests: `{UID}-COG-X-RAV-T1Sc` to `T5Sc`, `{UID}-COG-X-RAV-DRSc`, `{UID}-COG-X-BVM-TotR`, `{UID}-COG-X-NAR-Scor`, `{UID}-COG-X-RPM-Scor`
- Demographics: `{UID}-DEM-X-Age`, `{UID}-DEM-X-Sex`, `{UID}-DEM-X-Education`
- Self-report: `{UID}-DEM-X-DASS_Dep`, `{UID}-DEM-X-DASS_Anx`, `{UID}-DEM-X-DASS_Str`, `{UID}-DEM-X-VR_Exp`, `{UID}-DEM-X-SLEEP`

**Extraction Method:**
Step 1 extracts cognitive test scores, computes derived scores (RAVLT_Total = sum T1-T5), converts to T-scores (M=50, SD=10). Steps 2-3 extract demographics and self-report variables.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants with complete cognitive test data
- [ ] Exclude participants with missing DASS (expect ~97 with complete data)

**Variables:**
- [x] All cognitive test variables (RAVLT, BVMT, NART, RPM)
- [x] All demographic variables (Age, Sex, Education)
- [x] All self-report variables (DASS subscales, VR experience, sleep)

**Tests:**
- [x] Mean theta across all 4 test sessions (T1, T2, T3, T4)
- [ ] Per-test analysis not required for this RQ

---