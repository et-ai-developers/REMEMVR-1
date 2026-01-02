# Analysis Plan: RQ 7.1.2: Intercept vs Slope Prediction

**Research Question:** 7.1.2
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines differential prediction of LMM random effects (intercepts vs slopes) using cognitive tests (RAVLT, BVMT, RPM). The analysis tests whether traditional neuropsychological tests predict baseline ability (Day 0 intercept) more than forgetting rate (slope), consistent with tests measuring encoding but not consolidation processes.

**Pipeline:** LINEAR REGRESSION on LMM random effects with SIMULTANEOUS MODELING primary approach
**Steps:** 7 total analysis steps (Step 0: data extraction + Steps 1-6: analysis)
**Estimated Runtime:** HIGH (60-90 minutes total: 30-45 min LMM fitting + 15-30 min regression/bootstrap + 15 min validation)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni correction)
- CRITICAL: Simultaneous modeling as PRIMARY approach to avoid BLUP extraction bias
- Bootstrap confidence intervals with participant-level resampling (preserves correlation structure)
- Comprehensive bias documentation: BLUP shrinkage effects on subsequent regression validity

---

## Analysis Plan

### Step 0: Extract Random Effects and Cognitive Tests

**Dependencies:** None (first step)
**Complexity:** Low (data extraction, no model fitting)

**Input:**

**File 1:** results/ch5/5.1.1/data/step05_lmm_model_summary.txt
**Source:** Ch5 5.1.1 LMM fitting results
**Format:** Text summary containing model formula, random effects structure
**Required Content:** Confirmation of random intercepts/slopes model fitted

**File 2:** results/ch5/5.1.1/data/step04_lmm_input.csv
**Source:** Ch5 5.1.1 theta scores merged with TSVR
**Format:** CSV, long format (one row per observation)
**Columns:**
  - `UID` (string): Participant identifier (P001-P100)
  - `test` (int): Test session (T1=0, T2=1, T3=3, T4=6)
  - `theta_common` (float): IRT ability estimate
  - `TSVR_hours` (float): Time since VR session in hours
**Expected Rows:** ~400 (100 participants x 4 observations per participant)

**File 3:** master.xlsx (Sheet: cognitive_tests)
**Source:** Project-level cognitive test scores
**Required Columns:**
  - `UID` (string): Participant identifier matching LMM data
  - `RAVLT_Total` (int): RAVLT sum of trials T1-T5
  - `BVMT_Total_Recognition` (int): BVMT total recognition score
  - `RPM` (int): Raven's Progressive Matrices score
**Expected Rows:** 100 participants

**Processing:**
1. Load Ch5 5.1.1 LMM data and verify random intercepts/slopes structure exists
2. Extract cognitive test scores from master.xlsx for all 100 participants
3. Standardize cognitive tests to T-scores (M=50, SD=10) to enable coefficient comparison
4. EXCLUDE NART due to language validity concerns in diverse sample
5. Prepare data for simultaneous modeling approach (primary) and BLUP extraction (secondary sensitivity)

**Output:**

**File 1:** data/step00_lmm_input.csv
**Format:** CSV, long format for simultaneous modeling
**Columns:**
  - `UID` (string): Participant identifier
  - `test` (int): Test session
  - `theta_common` (float): IRT ability estimate
  - `TSVR_hours` (float): Time variable
  - `log_TSVR` (float): Logarithmic transformation of time
**Expected Rows:** ~400 observations
**Note:** Direct input for simultaneous LMM in Step 1

**File 2:** data/step00_cognitive_tests.csv
**Format:** CSV, wide format (one row per participant)
**Columns:**
  - `UID` (string): Participant identifier
  - `RAVLT_T` (float): RAVLT T-score (M=50, SD=10)
  - `BVMT_T` (float): BVMT T-score (M=50, SD=10)
  - `RPM_T` (float): RPM T-score (M=50, SD=10)
**Expected Rows:** 100 participants

**Validation Requirement:**
Validation tools MUST be used after data extraction execution. Specific validation tools will be determined by rq_tools based on data extraction requirements (file format validation, merge validation, standardization validation). The rq_analysis agent will embed validation tool calls after the analysis tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_lmm_input.csv: 400 rows x 5 columns (UID: object, test: int64, theta_common: float64, TSVR_hours: float64, log_TSVR: float64)
- data/step00_cognitive_tests.csv: 100 rows x 4 columns (UID: object, RAVLT_T: float64, BVMT_T: float64, RPM_T: float64)

*Value Ranges:*
- theta_common in [-3, 3] (typical IRT ability range)
- TSVR_hours in [0, 168] (0 hours = encoding, 168 = 1 week max)
- log_TSVR in [0, 5.13] (log(168) = 5.13 for 1-week max)
- T-scores in [20, 80] (T-score range: M=50, SD=10, 3 SD range)

*Data Quality:*
- All 100 participants present in both files (no missing UIDs)
- No NaN values in cognitive T-scores (standardization must be complete)
- T-score distributions approximately normal (mean ~50, SD ~10)
- All UIDs match between LMM input and cognitive tests

*Log Validation:*
- Required pattern: "Cognitive tests standardized: RAVLT_T mean=XX.X, SD=XX.X"
- Required pattern: "LMM input prepared: 400 rows, 5 columns"
- Forbidden patterns: "ERROR", "Missing UID", "Standardization failed"
- Acceptable warnings: None expected for data extraction

**Expected Behavior on Validation Failure:**
Raise error with specific failure message (e.g., "Expected 100 participants, found 97"), log failure to logs/step00_extract.log, quit script immediately, invoke g_debug for diagnosis.

---

### Step 1: Fit Simultaneous LMM (Primary Approach)

**Dependencies:** Step 0 (requires LMM input and cognitive test data)
**Complexity:** HIGH (30-45 minute LMM fitting with interactions)

**Input:**

**File 1:** data/step00_lmm_input.csv
**Source:** Step 0 LMM data preparation
**Format:** CSV, long format

**File 2:** data/step00_cognitive_tests.csv
**Source:** Step 0 cognitive test standardization
**Format:** CSV, wide format

**Processing:**
Fit simultaneous LMM testing differential prediction hypothesis directly:

**Model Formula:**
`theta_common ~ log_TSVR + (1 + log_TSVR | UID) + RAVLT_T*log_TSVR + BVMT_T*log_TSVR + RPM_T*log_TSVR`

**Model Components:**
- **Fixed Intercept:** Overall Day 0 ability
- **Fixed log_TSVR:** Population-level decline
- **Random Intercepts:** Participant-specific Day 0 ability (what cognitive tests should predict strongly)
- **Random Slopes:** Participant-specific decline rates (what cognitive tests should predict weakly)
- **RAVLT_T main effect:** Intercept prediction by RAVLT
- **BVMT_T main effect:** Intercept prediction by BVMT
- **RPM_T main effect:** Intercept prediction by RPM
- **RAVLT_T*log_TSVR interaction:** Slope prediction by RAVLT
- **BVMT_T*log_TSVR interaction:** Slope prediction by BVMT
- **RPM_T*log_TSVR interaction:** Slope prediction by RPM

**Hypothesis Tests:**
1. **Intercept prediction (main effects):** RAVLT_T, BVMT_T, RPM_T coefficients
2. **Slope prediction (interaction effects):** RAVLT_T*log_TSVR, BVMT_T*log_TSVR, RPM_T*log_TSVR coefficients
3. **Differential prediction test:** Main effects should be larger than interaction effects

**Output:**

**File 1:** data/step01_simultaneous_lmm.pkl
**Format:** Pickled statsmodels LMM object
**Contents:** Fitted simultaneous model with all parameters
**Note:** Enables coefficient extraction and variance component analysis

**File 2:** data/step01_simultaneous_lmm_summary.txt
**Format:** Text summary
**Contents:** Fixed effects table, random effects variances, model diagnostics
**Key Sections:** 
  - Main effects (intercept prediction): RAVLT_T, BVMT_T, RPM_T coefficients + p-values
  - Interaction effects (slope prediction): RAVLT_T*log_TSVR, BVMT_T*log_TSVR, RPM_T*log_TSVR coefficients + p-values
  - Model fit indices (AIC, BIC, log-likelihood)

**Validation Requirement:**
Validation tools MUST be used after simultaneous LMM execution. Specific validation tools will be determined by rq_tools based on LMM fitting requirements (convergence validation, parameter bounds validation, residual validation). The rq_analysis agent will embed validation tool calls after the analysis tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_simultaneous_lmm.pkl: Binary file exists (statsmodels LMM object)
- data/step01_simultaneous_lmm_summary.txt: Text file with model summary (50-100 lines expected)

*Value Ranges:*
- Fixed effect coefficients in [-2, 2] (reasonable for standardized predictors)
- P-values in [0, 1] (valid probability range)
- Random effect variances > 0 (positive variance components required)
- AIC/BIC values positive (model comparison metrics)

*Data Quality:*
- Model convergence achieved (no convergence warnings in summary)
- All variance components estimated (no "unable to estimate" messages)
- Expected degrees of freedom (6 fixed effects: intercept + log_TSVR + 3 main + 3 interactions)
- Random effects structure: 2 components (intercept variance, slope variance, covariance)

*Log Validation:*
- Required pattern: "Model converged successfully"
- Required pattern: "Fixed effects estimated: 6 parameters"
- Required pattern: "Random effects estimated: intercept variance, slope variance"
- Forbidden patterns: "CONVERGENCE FAILED", "Singular fit", "Unable to estimate"
- Acceptable warnings: "Some correlations may be unreliable" (expected with many parameters)

**Expected Behavior on Validation Failure:**
Raise error with specific failure message (e.g., "LMM convergence failed"), log failure to logs/step01_fit_simultaneous_lmm.log, quit script immediately, invoke g_debug for convergence diagnosis.

---

### Step 2: Extract Random Effects (Secondary Approach)

**Dependencies:** Step 0 (requires prepared LMM input for BLUP extraction)
**Complexity:** MEDIUM (15-20 minute LMM fitting for BLUP extraction)

**Input:**

**File 1:** data/step00_lmm_input.csv
**Source:** Step 0 LMM data preparation
**Format:** CSV, long format

**Processing:**
Fit baseline LMM without cognitive test predictors to extract BLUPs for sensitivity analysis:

**Model Formula:**
`theta_common ~ log_TSVR + (1 + log_TSVR | UID)`

**BLUP Extraction:**
- Extract participant-specific random intercepts (baseline ability estimates)
- Extract participant-specific random slopes (decline rate estimates)
- **CRITICAL BIAS WARNING:** BLUPs exhibit shrinkage toward population mean
  - Extreme intercepts/slopes pulled toward zero
  - Differential shrinkage affects subsequent regression validity
  - Document shrinkage magnitude for transparency

**Shrinkage Documentation:**
1. Compute empirical intercepts/slopes (participant-specific OLS fits)
2. Compare BLUP variance to empirical variance
3. Report shrinkage factor: 1 - (var_BLUP / var_empirical)
4. Expected shrinkage: 20-40% (typical for N=4 observations per participant)

**Output:**

**File 1:** data/step02_random_effects.csv
**Format:** CSV, wide format (one row per participant)
**Columns:**
  - `UID` (string): Participant identifier
  - `intercept` (float): Random intercept BLUP (baseline ability)
  - `slope` (float): Random slope BLUP (decline rate)
  - `se_intercept` (float): Standard error of intercept BLUP
  - `se_slope` (float): Standard error of slope BLUP
**Expected Rows:** 100 participants

**File 2:** data/step02_shrinkage_analysis.csv
**Format:** CSV, comparison of BLUP vs empirical variances
**Columns:**
  - `parameter` (string): "intercept" or "slope"
  - `variance_empirical` (float): Empirical variance (OLS)
  - `variance_blup` (float): BLUP variance (shrunken)
  - `shrinkage_factor` (float): 1 - (var_BLUP / var_empirical)
**Expected Rows:** 2 (intercept and slope variances)

**File 3:** data/step02_baseline_lmm_summary.txt
**Format:** Text summary of baseline LMM (without cognitive predictors)
**Contents:** Model summary for BLUP extraction reference

**Validation Requirement:**
Validation tools MUST be used after BLUP extraction execution. Specific validation tools will be determined by rq_tools based on LMM fitting and random effects extraction requirements. The rq_analysis agent will embed validation tool calls after the analysis tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_random_effects.csv: 100 rows x 5 columns (UID: object, intercept: float64, slope: float64, se_intercept: float64, se_slope: float64)
- data/step02_shrinkage_analysis.csv: 2 rows x 4 columns (parameter: object, variance_empirical: float64, variance_blup: float64, shrinkage_factor: float64)

*Value Ranges:*
- intercept in [-2, 2] (reasonable baseline ability range)
- slope in [-1, 1] (reasonable decline rate range)
- Standard errors > 0 (positive uncertainty estimates)
- shrinkage_factor in [0, 1] (0% = no shrinkage, 100% = complete shrinkage)

*Data Quality:*
- All 100 participants present (no missing random effects)
- No NaN values in random effects (BLUP estimation must succeed for all)
- Shrinkage factors in expected range: 0.15-0.50 (15-50% shrinkage typical)
- Standard errors reasonable: se_intercept in [0.1, 0.5], se_slope in [0.05, 0.3]

*Log Validation:*
- Required pattern: "Random effects extracted for 100 participants"
- Required pattern: "Shrinkage analysis: intercept=XX.X%, slope=XX.X%"
- Forbidden patterns: "BLUP extraction failed", "Missing random effects"
- Acceptable warnings: "Some random effects may be unreliable" (expected with limited observations)

**Expected Behavior on Validation Failure:**
Raise error with specific failure message (e.g., "Random effects missing for 5 participants"), log failure to logs/step02_extract_random_effects.log, quit script immediately, invoke g_debug for extraction diagnosis.

---

### Step 3: Predict Intercepts (Two-Stage Analysis)

**Dependencies:** Step 0 (cognitive tests), Step 2 (random effects)
**Complexity:** LOW (5 minute regression fitting)

**Input:**

**File 1:** data/step00_cognitive_tests.csv
**Source:** Step 0 standardized cognitive tests
**Format:** CSV, wide format

**File 2:** data/step02_random_effects.csv
**Source:** Step 2 BLUP extraction
**Format:** CSV, wide format

**Processing:**
Predict random intercepts using cognitive tests:

**Model Formula:**
`intercept ~ RAVLT_T + BVMT_T + RPM_T`

**Statistical Procedures:**
1. Fit multiple linear regression predicting baseline ability
2. Check linearity assumptions: Partial regression plots for each predictor
3. Test multicollinearity: VIF < 5 threshold
4. Compute R-squared (key outcome for hypothesis test)
5. Extract individual beta coefficients with confidence intervals
6. Apply Bonferroni correction: alpha = 0.05/6 = 0.0083 (3 predictors x 2 models)
7. Bootstrap 95% CIs for all coefficients (1000 replications, participant-level resampling)

**Diagnostic Checks:**
- Linearity: Partial residual plots (if non-linear, consider transformations)
- Homoscedasticity: Breusch-Pagan test
- Normality: Shapiro-Wilk test on residuals
- Multicollinearity: VIF values for all predictors

**Output:**

**File 1:** data/step03_intercept_model_summary.txt
**Format:** Text summary
**Contents:** Model R-squared, F-test, individual coefficients with p-values
**Key Metrics:** 
  - R-squared (primary outcome for hypothesis)
  - F-statistic and p-value for overall model
  - Individual betas: RAVLT_T, BVMT_T, RPM_T with uncorrected + Bonferroni p-values

**File 2:** data/step03_intercept_predictions.csv
**Format:** CSV regression results
**Columns:**
  - `predictor` (string): Cognitive test name
  - `beta` (float): Regression coefficient
  - `se` (float): Standard error
  - `t_stat` (float): T-statistic
  - `p_uncorrected` (float): Uncorrected p-value
  - `p_bonferroni` (float): Bonferroni-corrected p-value (Decision D068)
  - `ci_lower` (float): Bootstrap 95% CI lower bound
  - `ci_upper` (float): Bootstrap 95% CI upper bound
**Expected Rows:** 3 (RAVLT, BVMT, RPM coefficients)

**File 3:** data/step03_intercept_diagnostics.csv
**Format:** CSV diagnostic results
**Columns:**
  - `test` (string): Diagnostic test name
  - `statistic` (float): Test statistic
  - `p_value` (float): P-value
  - `interpretation` (string): PASS/FAIL result
**Expected Rows:** 4 (linearity, homoscedasticity, normality, multicollinearity)

**Validation Requirement:**
Validation tools MUST be used after intercept prediction execution. Specific validation tools will be determined by rq_tools based on regression analysis requirements (R-squared validation, coefficient validation, diagnostic validation). The rq_analysis agent will embed validation tool calls after the analysis tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_intercept_predictions.csv: 3 rows x 8 columns (predictor: object, beta: float64, se: float64, t_stat: float64, p_uncorrected: float64, p_bonferroni: float64, ci_lower: float64, ci_upper: float64)
- data/step03_intercept_diagnostics.csv: 4 rows x 4 columns (test: object, statistic: float64, p_value: float64, interpretation: object)

*Value Ranges:*
- beta coefficients in [-1, 1] (reasonable for standardized predictors)
- Standard errors > 0 (positive uncertainty estimates)
- P-values in [0, 1] (valid probability range)
- R-squared in [0, 1] (proportion of variance explained)

*Data Quality:*
- All 3 cognitive tests present as predictors (no missing coefficients)
- Bonferroni p-values >= uncorrected p-values (correction should increase p-values)
- Bootstrap CIs contain point estimates (sanity check)
- Diagnostic tests completed: linearity, homoscedasticity, normality, multicollinearity

*Log Validation:*
- Required pattern: "Intercept model R-squared = 0.XXX"
- Required pattern: "All diagnostic tests completed: 4/4"
- Required pattern: "Bootstrap confidence intervals computed: 1000 replications"
- Forbidden patterns: "Regression failed", "Diagnostic test error"
- Acceptable warnings: "Weak evidence for assumption violation" (p < 0.1 on diagnostics)

**Expected Behavior on Validation Failure:**
Raise error with specific failure message (e.g., "Bootstrap CI computation failed"), log failure to logs/step03_predict_intercepts.log, quit script immediately, invoke g_debug for regression diagnosis.

---

### Step 4: Predict Slopes (Two-Stage Analysis)

**Dependencies:** Step 0 (cognitive tests), Step 2 (random effects)
**Complexity:** LOW (5 minute regression fitting)

**Input:**

**File 1:** data/step00_cognitive_tests.csv
**Source:** Step 0 standardized cognitive tests
**Format:** CSV, wide format

**File 2:** data/step02_random_effects.csv
**Source:** Step 2 BLUP extraction
**Format:** CSV, wide format

**Processing:**
Predict random slopes using cognitive tests:

**Model Formula:**
`slope ~ RAVLT_T + BVMT_T + RPM_T`

**Statistical Procedures:** Same as Step 3, applied to slope prediction
1. Fit multiple linear regression predicting decline rates
2. Check linearity assumptions and multicollinearity (VIF < 5)
3. Compute R-squared (key outcome for comparison with intercept R-squared)
4. Extract individual beta coefficients with confidence intervals
5. Apply same Bonferroni correction: alpha = 0.0083
6. Bootstrap 95% CIs for all coefficients (1000 replications)

**CRITICAL BIAS WARNING:**
BLUP slopes exhibit differential shrinkage affecting regression validity:
- Extreme slopes shrunken more than moderate slopes
- This non-uniform shrinkage can artificially reduce or inflate R-squared
- Results may not reflect true predictive relationships
- Simultaneous model (Step 1) provides unbiased estimates

**Output:**

**File 1:** data/step04_slope_model_summary.txt
**Format:** Text summary (same structure as Step 3)
**Contents:** Model R-squared, F-test, individual coefficients with bias warning
**Key Metrics:**
  - R-squared (for comparison with intercept prediction)
  - Individual betas with uncorrected + Bonferroni p-values
  - BIAS WARNING: Note differential shrinkage effects

**File 2:** data/step04_slope_predictions.csv
**Format:** CSV regression results (same structure as Step 3)
**Columns:** Same as Step 3 intercept predictions file
**Expected Rows:** 3 (RAVLT, BVMT, RPM coefficients for slope prediction)

**File 3:** data/step04_slope_diagnostics.csv
**Format:** CSV diagnostic results (same structure as Step 3)
**Expected Rows:** 4 (same diagnostic tests as intercept prediction)

**Validation Requirement:**
Validation tools MUST be used after slope prediction execution. Specific validation tools will be determined by rq_tools based on regression analysis requirements. The rq_analysis agent will embed validation tool calls after the analysis tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_slope_predictions.csv: 3 rows x 8 columns (same structure as intercept predictions)
- data/step04_slope_diagnostics.csv: 4 rows x 4 columns (same structure as intercept diagnostics)

*Value Ranges:*
- beta coefficients in [-0.5, 0.5] (smaller range expected for slope prediction)
- Standard errors > 0 (positive uncertainty estimates)
- P-values in [0, 1] (valid probability range)
- R-squared in [0, 1], expected < 0.15 per hypothesis

*Data Quality:*
- All 3 cognitive tests present as predictors (consistent with Step 3)
- Bonferroni p-values >= uncorrected p-values (correction consistency)
- Bootstrap CIs contain point estimates
- All diagnostic tests completed successfully

*Log Validation:*
- Required pattern: "Slope model R-squared = 0.XXX"
- Required pattern: "BIAS WARNING: BLUP shrinkage may affect validity"
- Required pattern: "Bootstrap confidence intervals computed: 1000 replications"
- Forbidden patterns: "Regression failed", "Diagnostic test error"
- Acceptable warnings: Same as Step 3 diagnostic warnings

**Expected Behavior on Validation Failure:**
Raise error with specific failure message, log failure to logs/step04_predict_slopes.log, quit script immediately, invoke g_debug for regression diagnosis.

---

### Step 5: Compare R-Squared Values

**Dependencies:** Step 1 (simultaneous model), Step 3 (intercept prediction), Step 4 (slope prediction)
**Complexity:** MEDIUM (15-20 minutes for bootstrap comparison)

**Input:**

**File 1:** data/step01_simultaneous_lmm.pkl
**Source:** Step 1 simultaneous LMM
**Format:** Pickled model object

**File 2:** data/step03_intercept_model_summary.txt
**Source:** Step 3 intercept prediction
**Format:** Text summary containing R-squared value

**File 3:** data/step04_slope_model_summary.txt
**Source:** Step 4 slope prediction
**Format:** Text summary containing R-squared value

**Processing:**
Compare predictive strength using multiple approaches:

**1. Primary Analysis (Simultaneous Model):**
- Extract main effect coefficients (intercept prediction): RAVLT_T, BVMT_T, RPM_T
- Extract interaction coefficients (slope prediction): RAVLT_T*log_TSVR, BVMT_T*log_TSVR, RPM_T*log_TSVR
- Compute pseudo-R-squared for main effects vs interaction effects
- Test hypothesis: main effects significantly larger than interaction effects

**2. Secondary Analysis (Two-Stage Comparison):**
- Compare R²_intercept vs R²_slope from Steps 3-4
- Bootstrap hypothesis test: R²_intercept > R²_slope
- Participant-level block bootstrap (1000 replications, seed=42)
- Preserves within-participant correlation structure
- Bootstrap 95% CI for R²_intercept - R²_slope difference

**3. Statistical Testing:**
- Bootstrap percentile method (primary)
- Fisher's Z-test only if normality verified (Q-Q plots, Shapiro-Wilk)
- If normality violated: Use bootstrap exclusively

**Hypothesis Tests:**
1. **Primary:** Simultaneous model main effects > interaction effects
2. **Secondary:** R²_intercept significantly > R²_slope (bootstrap CI excludes 0)
3. **Individual tests:** No cognitive test significantly predicts slope after Bonferroni correction

**Output:**

**File 1:** data/step05_r_squared_comparison.csv
**Format:** CSV comparison results
**Columns:**
  - `approach` (string): "simultaneous" or "two_stage"
  - `intercept_r_squared` (float): Intercept prediction strength
  - `slope_r_squared` (float): Slope prediction strength
  - `difference` (float): R²_intercept - R²_slope
  - `ci_lower` (float): Bootstrap 95% CI lower bound
  - `ci_upper` (float): Bootstrap 95% CI upper bound
  - `p_value` (float): Bootstrap hypothesis test p-value
  - `conclusion` (string): "Supported" or "Not supported"
**Expected Rows:** 2 (simultaneous and two-stage approaches)

**File 2:** data/step05_bootstrap_results.csv
**Format:** CSV bootstrap replications (for transparency)
**Columns:**
  - `replication` (int): Bootstrap sample number (1-1000)
  - `r_squared_intercept` (float): R² for intercept prediction
  - `r_squared_slope` (float): R² for slope prediction
  - `difference` (float): R²_intercept - R²_slope for this replication
**Expected Rows:** 1000 bootstrap replications

**File 3:** data/step05_bias_comparison.txt
**Format:** Text summary comparing approaches
**Contents:** 
  - Simultaneous model advantages (no BLUP bias)
  - Two-stage limitations (shrinkage effects documented)
  - Convergence between approaches (consistency check)
  - Final conclusions with bias caveats

**Validation Requirement:**
Validation tools MUST be used after R-squared comparison execution. Specific validation tools will be determined by rq_tools based on bootstrap analysis requirements. The rq_analysis agent will embed validation tool calls after the analysis tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_r_squared_comparison.csv: 2 rows x 8 columns (approach: object, intercept_r_squared: float64, slope_r_squared: float64, difference: float64, ci_lower: float64, ci_upper: float64, p_value: float64, conclusion: object)
- data/step05_bootstrap_results.csv: 1000 rows x 4 columns (replication: int64, r_squared_intercept: float64, r_squared_slope: float64, difference: float64)

*Value Ranges:*
- R-squared values in [0, 1] (proportion variance explained)
- Differences in [-1, 1] (R²_intercept - R²_slope)
- P-values in [0, 1] (bootstrap hypothesis test)
- Bootstrap CI bounds in [-1, 1] (difference confidence interval)

*Data Quality:*
- Exactly 1000 bootstrap replications (complete bootstrap)
- Both approaches present: simultaneous and two-stage
- Bootstrap CIs calculated (ci_lower < ci_upper)
- Hypothesis conclusions drawn ("Supported" or "Not supported")

*Log Validation:*
- Required pattern: "Bootstrap completed: 1000 replications"
- Required pattern: "Hypothesis test: R²_intercept > R²_slope, p = 0.XXX"
- Required pattern: "PRIMARY approach: Simultaneous model (unbiased)"
- Required pattern: "SECONDARY approach: Two-stage (BLUP bias warning)"
- Forbidden patterns: "Bootstrap failed", "R-squared computation error"
- Acceptable warnings: "Some bootstrap samples failed to converge" (<5% failure acceptable)

**Expected Behavior on Validation Failure:**
Raise error with specific failure message (e.g., "Bootstrap confidence interval invalid"), log failure to logs/step05_compare_r_squared.log, quit script immediately, invoke g_debug for bootstrap diagnosis.

---

### Step 6: Prepare Results Summary Plot Data

**Dependencies:** Step 5 (R-squared comparison completed)
**Complexity:** LOW (5 minute data aggregation for visualization)

**  CRITICAL NOTE:** Plot data preparation IS an analysis step that gets executed in Step 14 CODE EXECUTION LOOP (g_code -> bash -> rq_inspect) and MUST have validation requirements.

**Purpose:** Aggregate R-squared comparison results for visualization showing intercept vs slope prediction strength

**Dependencies:** Step 5 (requires R-squared comparison results)

**Input:**

**File 1:** data/step05_r_squared_comparison.csv
**Source:** Step 5 R-squared comparison
**Format:** CSV with comparison results

**File 2:** data/step03_intercept_predictions.csv
**Source:** Step 3 individual predictor coefficients for intercept
**Format:** CSV with predictor-level results

**File 3:** data/step04_slope_predictions.csv
**Source:** Step 4 individual predictor coefficients for slope
**Format:** CSV with predictor-level results

**Plot Description:** Bar chart comparing R-squared values for intercept vs slope prediction, with error bars showing bootstrap confidence intervals. Separate bars for individual cognitive tests and combined model.

**Required Data Sources:**
- R-squared comparison from simultaneous and two-stage approaches
- Individual predictor results for cognitive tests
- Bootstrap confidence intervals for uncertainty quantification

**Output (Plot Source CSV):** data/step06_summary_plot_data.csv

**Required Columns:**
- `model` (string): Model type ("Simultaneous", "Two-Stage")
- `outcome` (string): Predicted outcome ("Intercept", "Slope") 
- `r_squared` (float): Model R-squared value
- `ci_lower` (float): Bootstrap 95% CI lower bound
- `ci_upper` (float): Bootstrap 95% CI upper bound
- `predictor` (string): Individual cognitive test ("Combined", "RAVLT", "BVMT", "RPM")

**Expected Rows:** 8-12 (2 approaches x 2 outcomes x 2-3 detail levels)

**Aggregation Logic:**
1. Extract R-squared values from step05_r_squared_comparison.csv
2. Extract individual predictor R-squared from regression summaries
3. Combine into plot-ready format with grouping variables
4. Add bootstrap confidence intervals for error bars
5. Include both combined model and individual predictor results
6. Sort by model type, then outcome, then predictor

**Validation Requirement:**
Validation tools MUST be used after plot data preparation execution. Specific validation tools will be determined by rq_tools based on plot data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_summary_plot_data.csv exists (exact path)
- Expected rows: 8-12 (2 approaches x 2 outcomes x detailed breakdown)
- Expected columns: 6 (model, outcome, r_squared, ci_lower, ci_upper, predictor)
- Data types: string (model, outcome, predictor), float (r_squared, CI bounds)

*Value Ranges:*
- r_squared in [0, 1] (proportion variance explained)
- ci_lower in [0, 1], ci_upper in [0, 1] (confidence bounds)
- ci_upper > ci_lower for all rows (valid confidence intervals)
- model in {"Simultaneous", "Two-Stage"} (categorical)
- outcome in {"Intercept", "Slope"} (categorical)

*Data Quality:*
- No NaN values tolerated (all aggregation must succeed)
- Expected N: 8-12 rows (complete factorial design)
- No duplicate combinations of model x outcome x predictor
- All cognitive tests represented: Combined, RAVLT, BVMT, RPM

*Log Validation:*
- Required pattern: "Plot data preparation complete: XX rows created"
- Required pattern: "All approaches represented: Simultaneous, Two-Stage"
- Required pattern: "All outcomes represented: Intercept, Slope"
- Forbidden patterns: "ERROR", "NaN values detected", "Missing model type"
- Acceptable warnings: None expected for plot data preparation

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 2 approaches, found 1")
- Log failure to logs/step06_prepare_summary_plot_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- g_debug invoked to diagnose root cause

**Plotting Function (rq_plots will call):** Bar chart with error bars comparing intercept vs slope prediction
- rq_plots agent maps this description to specific tools/plots.py function
- Plot reads data/step06_summary_plot_data.csv (created by this step)
- No data aggregation in rq_plots (visualization only per Option B)
- PNG output saved to plots/ folder by rq_plots

---

## Expected Data Formats

### Data Transformations

**Step 0 to Step 1 (Wide to Long Merge):**
- Input Format: Two separate files (LMM data + cognitive tests)
- Merge Logic: Left join on UID (all LMM observations retained, cognitive tests added)
- Output Format: Long format with cognitive test predictors for simultaneous modeling
- Critical Decision D068: Dual p-value reporting setup (uncorrected + Bonferroni)

**Step 2 (BLUP Extraction):**
- Input Format: Long format LMM data 
- BLUP Logic: Extract participant-specific random intercepts and slopes via empirical Bayes
- Shrinkage Documentation: Compare BLUP variance to empirical variance (bias quantification)
- Output Format: Wide format (one row per participant with intercept/slope)

**Step 3-4 (Regression Analysis):**
- Input Format: Wide format (random effects + cognitive tests)
- Regression Logic: Multiple linear regression with standardized predictors
- Bootstrap Logic: Participant-level resampling preserves correlation structure
- Output Format: Regression results with dual p-values (Decision D068)

**Step 5 (Comparison Analysis):**
- Input Format: Multiple sources (simultaneous LMM + two regression models)
- Comparison Logic: Bootstrap difference testing for R²_intercept vs R²_slope  
- Statistical Methods: Bootstrap percentile CI, Fisher's Z-test conditional on normality
- Output Format: Comparison table with confidence intervals and hypothesis test results

### Column Naming Conventions

**From names.md established patterns:**
- `UID`: Participant identifier (consistent across all files)
- `theta_common`: IRT ability estimate (from Ch5 5.1.1)
- `TSVR_hours`: Time since VR in hours (Decision D070)
- `CI_lower`, `CI_upper`: Confidence interval bounds (plotting standard)

**New conventions for RQ 7.1.2:**
- `intercept`, `slope`: Random effects from BLUP extraction
- `se_intercept`, `se_slope`: Standard errors for random effects
- `RAVLT_T`, `BVMT_T`, `RPM_T`: T-scored cognitive tests (M=50, SD=10)
- `p_uncorrected`, `p_bonferroni`: Dual p-values (Decision D068)
- `shrinkage_factor`: BLUP shrinkage documentation (transparency)

### Data Type Constraints

**Required Data Types:**
- UID: string/object (participant identifiers)
- theta_common: float64 (IRT ability estimates)
- TSVR_hours: float64 (continuous time variable)
- Cognitive T-scores: float64 (standardized test scores)
- Random effects: float64 (BLUP estimates)
- P-values: float64 (must be in [0,1] range)
- Bootstrap results: float64 (confidence intervals)

**Nullable vs Non-Nullable:**
- UID: Non-nullable (all participants must have identifiers)
- theta_common: Non-nullable (all participants have IRT estimates from Ch5)
- Cognitive tests: Non-nullable after standardization (exclusions handled beforehand)
- Random effects: Non-nullable (BLUP estimation must succeed for analysis validity)
- Bootstrap results: Non-nullable (complete bootstrap required for inference)

---

## Cross-RQ Dependencies

**This RQ requires outputs from:**
- **Ch5 5.1.1** (Functional Form Comparison - provides LMM data and theta scores)
  - File 1: results/ch5/5.1.1/data/step04_lmm_input.csv
  - File 2: results/ch5/5.1.1/data/step05_lmm_model_summary.txt
  - Used in: Step 0 (LMM data preparation) and Step 1 (simultaneous modeling)
  - Rationale: Ch5 5.1.1 provides baseline episodic memory trajectories. This RQ examines what predicts individual differences in those trajectories.

**Execution Order Constraint:**
1. Ch5 5.1.1 must complete through Step 5 (LMM fitting with random intercepts/slopes)
2. This RQ executes using Ch5 outputs as foundation
3. All cognitive test data extracted independently from master.xlsx

**Data Source Boundaries:**
- **RAW data:** master.xlsx cognitive test scores (RAVLT, BVMT, RPM)
- **DERIVED data:** Ch5 5.1.1 LMM trajectories and theta scores
- **Scope:** This RQ does NOT re-estimate IRT models (uses Ch5 theta scores as given)

**Validation:**
- Step 0: Check results/ch5/5.1.1/data/step04_lmm_input.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch5/5.1.1/data/step05_lmm_model_summary.txt exists (circuit breaker: EXPECTATIONS ERROR if absent)
- If either file missing -> quit with error -> user must execute Ch5 5.1.1 first

---

## Validation Requirements

**CRITICAL MANDATE:**

Every analysis step in this plan MUST use validation tools after analysis tool execution.

This is not optional. This is the core architectural principle preventing cascading failures observed in v3.0 (where analysis errors propagated undetected through 5+ downstream steps before discovery).

**Exact Specification Requirement:**

> "Validation tools MUST be used after analysis tool execution"

**Implementation:**
- rq_tools (Step 11 workflow) will read tool_inventory.md validation tools section
- rq_tools will specify BOTH analysis tool + validation tool per step in 3_tools.yaml  
- rq_analysis (Step 12 workflow) will embed validation tool call AFTER analysis tool call in 4_analysis.yaml
- g_code (Step 14 workflow) will generate stepN_name.py scripts with validation function calls
- bash execution (Step 14 workflow) will run analysis -> validation -> error on validation failure

**Downstream Agent Requirements:**
- **rq_tools:** MUST specify validation tool for EVERY analysis step (no exceptions)
- **rq_analysis:** MUST embed validation tool call for EVERY analysis step (no exceptions)  
- **g_code:** MUST generate code with validation function calls (no exceptions)
- **rq_inspect:** MUST verify validation ran successfully (checks logs/stepN_name.log for validation output)

### Validation Requirements By Step

#### Step 0: Extract Random Effects and Cognitive Tests

**Analysis Tool:** (determined by rq_tools - likely tools.data.extract_cognitive_tests + tools.data.merge_with_lmm)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_standardization + tools.validation.validate_data_merge)

**What Validation Checks:**
- Output files exist (step00_lmm_input.csv, step00_cognitive_tests.csv)
- Expected dimensions (400 rows LMM input, 100 rows cognitive tests)
- T-score standardization successful (mean ~50, SD ~10)
- All UIDs matched between files (complete merge)
- Value ranges reasonable (theta in [-3,3], TSVR in [0,168], T-scores in [20,80])

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Standardization failed: RAVLT mean=45.2, expected ~50")
- Log failure to logs/step00_extract.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked by master to diagnose root cause

---

#### Step 1: Fit Simultaneous LMM (Primary Approach)

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.fit_lmm_with_interactions)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_lmm_convergence + tools.validation.validate_lmm_parameters)

**What Validation Checks:**
- Model convergence achieved (no convergence warnings)
- All parameters estimated (6 fixed effects, 2 random variances + covariance)
- Parameter values reasonable (coefficients in [-2,2], variances > 0)
- Model summary generated successfully
- Fixed effects table contains all expected predictors and interactions

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "LMM did not converge: maximum iterations reached")
- Log failure to logs/step01_fit_simultaneous_lmm.log
- Quit script immediately
- g_debug invoked to diagnose (common causes: insufficient data, model misspecification)

---

#### Step 2: Extract Random Effects (Secondary Approach)

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.extract_random_effects_with_shrinkage)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_random_effects + tools.validation.validate_shrinkage_analysis)

**What Validation Checks:**
- Random effects extracted for all 100 participants (no missing BLUPs)
- Standard errors positive and reasonable (se in [0.1, 1.0])
- Shrinkage analysis completed (empirical vs BLUP variance comparison)
- Shrinkage factors in expected range (15-50% typical)
- No extreme outliers in random effects (|intercept| < 3, |slope| < 2)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Random effects missing for 5 participants")
- Log failure to logs/step02_extract_random_effects.log
- Quit script immediately
- g_debug invoked to diagnose BLUP extraction issues

---

#### Step 3: Predict Intercepts (Two-Stage Analysis)

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_regression.fit_multiple_regression_with_bootstrap)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_regression_diagnostics + tools.validation.validate_hypothesis_test_dual_pvalues)

**What Validation Checks:**
- Regression model fitted successfully (R-squared computed)
- All diagnostic tests completed (linearity, homoscedasticity, normality, multicollinearity)
- Bootstrap confidence intervals computed (1000 replications successful)
- Dual p-values present (uncorrected + Bonferroni per Decision D068)
- Coefficient values reasonable (standardized predictors: beta in [-1,1])

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Bootstrap failed: only 734 successful replications")
- Log failure to logs/step03_predict_intercepts.log
- Quit script immediately
- g_debug invoked to diagnose bootstrap or regression issues

---

#### Step 4: Predict Slopes (Two-Stage Analysis)

**Analysis Tool:** (Same as Step 3, applied to slope outcomes)
**Validation Tool:** (Same as Step 3, with BLUP bias warning checks)

**What Validation Checks:** (Same as Step 3, plus BLUP bias documentation)
- BLUP bias warning documented in outputs
- Shrinkage effects noted in model summary
- Results interpreted with bias caveats

**Expected Behavior on Validation Failure:** (Same as Step 3)

---

#### Step 5: Compare R-Squared Values

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_regression.compare_r_squared_bootstrap)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_bootstrap_comparison + tools.validation.validate_hypothesis_test)

**What Validation Checks:**
- Bootstrap comparison completed (1000 replications)
- Confidence intervals calculated (percentile method)
- Hypothesis test performed (R²_intercept > R²_slope)
- Both approaches compared (simultaneous + two-stage)
- Conclusions drawn with appropriate caveats

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Bootstrap confidence interval calculation failed")
- Log failure to logs/step05_compare_r_squared.log
- Quit script immediately
- g_debug invoked to diagnose bootstrap comparison issues

---

#### Step 6: Prepare Results Summary Plot Data

**Analysis Tool:** (determined by rq_tools - likely tools.plotting.prepare_summary_plot_data)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_plot_data_completeness)

**What Validation Checks:**
- Plot source CSV created with all required columns
- All factor levels present (approaches, outcomes, predictors)
- Value ranges appropriate (R-squared in [0,1], valid CIs)
- No missing data in plot source file
- Expected row count matches factorial design

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Missing approach: Expected 'Simultaneous', 'Two-Stage'")
- Log failure to logs/step06_prepare_summary_plot_data.log
- Quit script immediately
- g_debug invoked to diagnose data aggregation issues

---

## Summary

**Total Steps:** 7 (Step 0: extraction + Steps 1-6: analysis)
**Estimated Runtime:** HIGH (60-90 minutes: 45 min LMM + 30 min regression + 15 min validation)
**Cross-RQ Dependencies:** Ch5 5.1.1 (LMM trajectories and theta scores)
**Primary Outputs:** 
  - Simultaneous LMM results (unbiased approach)
  - Two-stage regression comparison (sensitivity analysis)
  - R-squared comparison with bootstrap hypothesis test
  - Plot source CSV for visualization
**Validation Coverage:** 100% (all 7 steps have validation requirements)

**CRITICAL METHODOLOGICAL NOTE:**
This analysis uses SIMULTANEOUS MODELING as the primary approach to avoid BLUP extraction bias. Two-stage analysis (Steps 2-4) serves as sensitivity analysis but results may be biased due to differential shrinkage. All interpretations will prioritize simultaneous model results with two-stage results reported for completeness.

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent for RQ 7.1.2
- Incorporates simultaneous modeling approach per validated concept (stats score 9.5/10)
- Addresses BLUP bias concerns with dual approach and comprehensive bias documentation
- Implements Decision D068 (dual p-value reporting) throughout
- Bootstrap methodology with participant-level resampling for valid inference