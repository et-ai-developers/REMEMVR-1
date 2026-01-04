# Analysis Plan: RQ 7.1.2 - Intercept vs Slope Prediction

**Research Question:** 7.1.2 - Do cognitive tests predict baseline ability (Day 0 intercept) more than forgetting rate (slope), consistent with tests measuring encoding but not consolidation?
**Created:** 2026-01-04
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines differential prediction of LMM random effects using cognitive tests. The analysis tests whether traditional neuropsychological tests (RAVLT, BVMT, RPM) predict encoding ability (intercept) more strongly than consolidation efficiency (slope). This addresses the theoretical question of what cognitive tests actually measure in relation to real-world memory processes.

**Pipeline:** Linear regression with LMM random effects extraction
**Steps:** 8 total analysis steps (Step 0: extractions + Steps 1-7: analysis)
**Estimated Runtime:** Medium complexity (~45 minutes total)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected and Bonferroni-corrected)
- Simultaneous modeling approach to avoid two-stage bias per concept validation
- Bootstrap confidence intervals with 1000 iterations and random seed=42

---

## Analysis Plan

### Step 0: Extract Ch5 LMM Data

**Dependencies:** None (first step)
**Complexity:** Low (5 minutes)

**Purpose:** Extract random effects from Ch5 5.1.1 LMM model for intercept/slope analysis

**Input:**
- File: results/ch5/5.1.1/data/step05_lmm_model_summary.txt (LMM fitted model)
- Alternative: results/ch5/5.1.1/data/step04_lmm_input.csv (theta scores with TSVR)
- Note: Uses DERIVED data from Ch5 5.1.1 omnibus episodic memory analysis

**Processing:**
- Extract random effects (BLUPs) for intercepts and slopes from Ch5 LMM
- Function: `extract_random_effects_from_lmm()`
- Creates per-participant intercept (Day 0 baseline) and slope (forgetting rate)
- Acknowledges BLUP shrinkage bias (extreme values pulled toward mean)

**Output:**
- File: data/step00_random_effects.csv
- Format: CSV with columns: UID, intercept, slope, se_intercept, se_slope
- Expected Rows: 100 (one per participant)
- Expected Columns: 5

**Validation Requirement:**
Validation tools MUST be used after random effects extraction. Specific validation tools will be determined by rq_tools based on random effects data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_random_effects.csv exists (exact path)
- Expected rows: 100 (one per participant)
- Expected columns: 5 (UID, intercept, slope, se_intercept, se_slope)
- Data types: UID (object), intercept (float64), slope (float64), se_intercept (float64), se_slope (float64)

*Value Ranges:*
- intercept in [-3, 3] (theta ability scale)
- slope in [-2, 2] (typical change per log-day)
- se_intercept in [0.1, 1.0] (reasonable standard errors)
- se_slope in [0.1, 1.0] (reasonable standard errors)

*Data Quality:*
- All 100 participants present (no missing data)
- No NaN values tolerated (all participants must have estimates)
- No duplicate UIDs (each participant appears once)
- Standard errors all positive (SE > 0)

*Log Validation:*
- Required pattern: "Random effects extracted: 100 participants"
- Required pattern: "Columns created: intercept, slope, se_intercept, se_slope"
- Forbidden patterns: "ERROR", "NaN values detected", "Missing participants"
- Acceptable warnings: "BLUP shrinkage noted" (expected per concept)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step00_extract_random_effects.log
- Quit script immediately
- g_debug invoked to diagnose root cause

---

### Step 1: Extract Cognitive Test Scores

**Dependencies:** None (independent extraction)
**Complexity:** Low (3 minutes)

**Purpose:** Extract and standardize cognitive test scores as predictors

**Input:**
- File: data/dfnonvr.csv
- Required columns: RAVLT_Total, BVMT_Total_Recognition, RPM_Total
- Note: NART excluded per concept due to language validity concerns

**Processing:**
- Function: `extract_cognitive_tests()` for RAVLT, BVMT, RPM
- Function: `standardize_to_t_scores()` to convert to T-scores (M=50, SD=10)
- Creates standardized predictors for regression analysis

**Output:**
- File: data/step01_cognitive_tests.csv
- Format: CSV with columns: UID, RAVLT_T, BVMT_T, RPM_T
- Expected Rows: 100 (one per participant)
- Expected Columns: 4

**Validation Requirement:**
Validation tools MUST be used after cognitive test extraction and standardization.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_cognitive_tests.csv exists (exact path)
- Expected rows: 100 (one per participant)
- Expected columns: 4 (UID, RAVLT_T, BVMT_T, RPM_T)
- Data types: UID (object), all test scores (float64)

*Value Ranges:*
- RAVLT_T in [10, 90] (T-score range, 4 SD from mean)
- BVMT_T in [10, 90] (T-score range, 4 SD from mean)
- RPM_T in [10, 90] (T-score range, 4 SD from mean)
- T-scores approximately M=50, SD=10 across sample

*Data Quality:*
- All 100 participants present
- No NaN values tolerated (complete cognitive data required)
- No duplicate UIDs
- T-score distributions approximately normal

*Log Validation:*
- Required pattern: "Cognitive tests extracted: RAVLT, BVMT, RPM"
- Required pattern: "T-score standardization complete: M~50, SD~10"
- Forbidden patterns: "ERROR", "Missing test scores", "Standardization failed"
- Acceptable warnings: None expected for cognitive extraction

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step01_extract_cognitive_tests.log
- Quit script immediately
- g_debug invoked to diagnose root cause

---

### Step 2: Merge Random Effects with Cognitive Tests

**Dependencies:** Step 0 (random effects), Step 1 (cognitive tests)
**Complexity:** Low (2 minutes)

**Purpose:** Create complete dataset for regression analysis

**Input:**
- File 1: data/step00_random_effects.csv (from Step 0)
- File 2: data/step01_cognitive_tests.csv (from Step 1)

**Processing:**
- Merge datasets on UID (inner join - all participants must have both datasets)
- Creates complete regression input with intercept/slope outcomes and cognitive predictors

**Output:**
- File: data/step02_regression_input.csv
- Format: CSV with columns: UID, intercept, slope, se_intercept, se_slope, RAVLT_T, BVMT_T, RPM_T
- Expected Rows: 100 (complete cases only)
- Expected Columns: 8

**Validation Requirement:**
Validation tools MUST be used after data merging to verify complete dataset.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_regression_input.csv exists (exact path)
- Expected rows: 100 (all participants matched)
- Expected columns: 8 (UID + 4 random effects + 3 cognitive tests)
- Data types: UID (object), all numeric columns (float64)

*Value Ranges:*
- intercept in [-3, 3], slope in [-2, 2] (from Step 0)
- se_intercept in [0.1, 1.0], se_slope in [0.1, 1.0] (from Step 0)
- RAVLT_T, BVMT_T, RPM_T in [10, 90] (from Step 1)

*Data Quality:*
- All 100 participants present (no data loss during merge)
- No NaN values tolerated (complete cases required)
- No duplicate UIDs
- All columns from both input files preserved

*Log Validation:*
- Required pattern: "Merge complete: 100 participants with complete data"
- Required pattern: "Columns merged: random effects + cognitive tests"
- Forbidden patterns: "ERROR", "Data loss during merge", "Missing UIDs"
- Acceptable warnings: None expected for merge operation

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step02_merge_data.log
- Quit script immediately
- g_debug invoked to diagnose root cause

---

### Step 3: Fit Intercept Prediction Model

**Dependencies:** Step 2 (regression input)
**Complexity:** Medium (5 minutes)

**Purpose:** Predict LMM intercepts using cognitive test scores

**Input:**
- File: data/step02_regression_input.csv
- Outcome: intercept (Day 0 baseline ability)
- Predictors: RAVLT_T, BVMT_T, RPM_T

**Processing:**
- Function: `fit_multiple_regression()` for intercept ~ RAVLT_T + BVMT_T + RPM_T
- Function: `compute_regression_diagnostics()` for VIF, assumptions
- Function: `bootstrap_regression_ci()` for 95% CIs (1000 iterations, seed=42)
- Checks linearity assumptions via partial regression plots
- Reports R, individual coefficients, VIF values

**Output:**
- File: data/step03_intercept_predictions.csv
- Format: CSV with columns: predictor, beta, se, t, p_uncorrected, p_bonferroni, CI_lower, CI_upper, VIF
- Expected Rows: 4 (intercept + 3 predictors)
- Expected Columns: 9

**Validation Requirement:**
Validation tools MUST be used after regression model fitting and diagnostics.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_intercept_predictions.csv exists (exact path)
- Expected rows: 4 (intercept term + 3 cognitive predictors)
- Expected columns: 9 (predictor, beta, se, t, p_uncorrected, p_bonferroni, CI_lower, CI_upper, VIF)
- Data types: predictor (object), all numeric columns (float64)

*Value Ranges:*
- beta unrestricted (effect size can be positive/negative)
- se in [0.01, 2.0] (reasonable standard errors)
- t unrestricted (test statistic)
- p_uncorrected in [0, 1] (p-value range)
- p_bonferroni in [0, 1] (Bonferroni-corrected p-values)
- CI_lower < CI_upper (confidence interval bounds)
- VIF in [1, 10] (multicollinearity check, warn if >5)

*Data Quality:*
- All 4 terms present (intercept + 3 predictors)
- No NaN values except for intercept term VIF (undefined)
- p_bonferroni = p_uncorrected * 3 (Bonferroni correction factor)
- CI intervals include beta values

*Log Validation:*
- Required pattern: "Regression model fitted: R = [value]"
- Required pattern: "VIF computed: all values < 5"
- Required pattern: "Bootstrap CIs computed: 1000 iterations"
- Forbidden patterns: "ERROR", "Convergence failed", "VIF > 10"
- Acceptable warnings: "VIF between 5-10" (moderate multicollinearity)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step03_fit_intercept_model.log
- Quit script immediately
- g_debug invoked to diagnose root cause

---

### Step 4: Fit Slope Prediction Model

**Dependencies:** Step 2 (regression input)
**Complexity:** Medium (5 minutes)

**Purpose:** Predict LMM slopes using cognitive test scores

**Input:**
- File: data/step02_regression_input.csv
- Outcome: slope (forgetting rate)
- Predictors: RAVLT_T, BVMT_T, RPM_T

**Processing:**
- Function: `fit_multiple_regression()` for slope ~ RAVLT_T + BVMT_T + RPM_T
- Function: `compute_regression_diagnostics()` for VIF, assumptions
- Function: `bootstrap_regression_ci()` for 95% CIs (1000 iterations, seed=42)
- Same analysis as Step 3 but with slope as outcome
- Critical limitation: BLUP shrinkage may bias slope R estimates

**Output:**
- File: data/step04_slope_predictions.csv
- Format: CSV with columns: predictor, beta, se, t, p_uncorrected, p_bonferroni, CI_lower, CI_upper, VIF
- Expected Rows: 4 (intercept + 3 predictors)
- Expected Columns: 9

**Validation Requirement:**
Validation tools MUST be used after slope regression model fitting and diagnostics.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_slope_predictions.csv exists (exact path)
- Expected rows: 4 (intercept term + 3 cognitive predictors)
- Expected columns: 9 (predictor, beta, se, t, p_uncorrected, p_bonferroni, CI_lower, CI_upper, VIF)
- Data types: predictor (object), all numeric columns (float64)

*Value Ranges:*
- beta unrestricted (effect size can be positive/negative)
- se in [0.01, 2.0] (reasonable standard errors)
- t unrestricted (test statistic)
- p_uncorrected in [0, 1] (p-value range)
- p_bonferroni in [0, 1] (Bonferroni-corrected p-values)
- CI_lower < CI_upper (confidence interval bounds)
- VIF in [1, 10] (multicollinearity check, warn if >5)

*Data Quality:*
- All 4 terms present (intercept + 3 predictors)
- No NaN values except for intercept term VIF (undefined)
- p_bonferroni = p_uncorrected * 3 (Bonferroni correction factor)
- CI intervals include beta values

*Log Validation:*
- Required pattern: "Regression model fitted: R = [value]"
- Required pattern: "VIF computed: all values < 5"
- Required pattern: "Bootstrap CIs computed: 1000 iterations"
- Required pattern: "BLUP shrinkage bias acknowledged"
- Forbidden patterns: "ERROR", "Convergence failed", "VIF > 10"
- Acceptable warnings: "VIF between 5-10", "Low R may reflect BLUP bias"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step04_fit_slope_model.log
- Quit script immediately
- g_debug invoked to diagnose root cause

---

### Step 5: Compare R Values with Bootstrap

**Dependencies:** Step 3 (intercept model), Step 4 (slope model)
**Complexity:** Medium (10 minutes)

**Purpose:** Test hypothesis that R_intercept > R_slope with statistical inference

**Input:**
- File 1: data/step03_intercept_predictions.csv (intercept model results)
- File 2: data/step04_slope_predictions.csv (slope model results)
- File 3: data/step02_regression_input.csv (raw data for bootstrap)

**Processing:**
- Extract R values from both models
- Function: `bootstrap_regression_ci()` for R difference (1000 iterations, seed=42)
- Participant-level block bootstrap preserving correlation structure
- Compute 95% CI for R_intercept - R_slope difference
- Test hypothesis: R_intercept > R_slope (one-tailed)

**Output:**
- File: data/step05_r_squared_comparison.csv
- Format: CSV with columns: model, r_squared, adj_r_squared, bootstrap_ci_lower, bootstrap_ci_upper, difference, difference_ci_lower, difference_ci_upper, p_value
- Expected Rows: 3 (intercept, slope, difference)
- Expected Columns: 9

**Validation Requirement:**
Validation tools MUST be used after R comparison and bootstrap inference.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_r_squared_comparison.csv exists (exact path)
- Expected rows: 3 (intercept, slope, difference rows)
- Expected columns: 9 (model through p_value)
- Data types: model (object), all numeric columns (float64)

*Value Ranges:*
- r_squared in [0, 1] (coefficient of determination bounds)
- adj_r_squared in [0, 1] (adjusted R bounds)
- bootstrap_ci_lower < bootstrap_ci_upper (CI bounds)
- difference unrestricted (can be positive/negative)
- p_value in [0, 1] (one-tailed test p-value)

*Data Quality:*
- All 3 model rows present (intercept, slope, difference)
- No NaN values in R or CI columns
- Difference row: difference = r_squared_intercept - r_squared_slope
- Bootstrap CIs based on 1000 iterations

*Log Validation:*
- Required pattern: "Bootstrap comparison: 1000 iterations complete"
- Required pattern: "R difference computed: [value]"
- Required pattern: "Bootstrap CI: [lower, upper]"
- Required pattern: "Hypothesis test: R_intercept > R_slope"
- Forbidden patterns: "ERROR", "Bootstrap failed", "Invalid R values"
- Acceptable warnings: "Wide CI suggests uncertain difference"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step05_compare_r_squared.log
- Quit script immediately
- g_debug invoked to diagnose root cause

---

### Step 6: Test Individual Predictor Significance

**Dependencies:** Step 3 (intercept model), Step 4 (slope model)
**Complexity:** Low (3 minutes)

**Purpose:** Examine which individual cognitive tests predict intercept vs slope after multiple comparison correction

**Input:**
- File 1: data/step03_intercept_predictions.csv (intercept predictor effects)
- File 2: data/step04_slope_predictions.csv (slope predictor effects)

**Processing:**
- Extract individual predictor p-values from both models
- Apply Decision D068: Report BOTH uncorrected AND Bonferroni-corrected p-values
- Bonferroni correction: alpha = 0.05/6 = 0.0083 (3 predictors  2 models)
- Test secondary hypothesis: No predictor significantly predicts slope after correction

**Output:**
- File: data/step06_predictor_significance.csv
- Format: CSV with columns: predictor, outcome, beta, p_uncorrected, p_bonferroni, sig_uncorrected, sig_bonferroni, effect_interpretation
- Expected Rows: 6 (3 predictors  2 outcomes)
- Expected Columns: 8

**Validation Requirement:**
Validation tools MUST be used after predictor significance testing with dual p-value reporting.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_predictor_significance.csv exists (exact path)
- Expected rows: 6 (RAVLT/BVMT/RPM  intercept/slope)
- Expected columns: 8 (predictor through effect_interpretation)
- Data types: predictor (object), outcome (object), effect_interpretation (object), all numeric columns (float64)

*Value Ranges:*
- beta unrestricted (effect size can be positive/negative)
- p_uncorrected in [0, 1] (p-value range)
- p_bonferroni in [0, 1] (corrected p-value range)
- sig_uncorrected in {0, 1} (binary significance at alpha=0.05)
- sig_bonferroni in {0, 1} (binary significance at alpha=0.0083)

*Data Quality:*
- All 6 predictor-outcome combinations present
- p_bonferroni = min(p_uncorrected * 6, 1.0) (Bonferroni correction)
- sig_uncorrected = (p_uncorrected < 0.05)
- sig_bonferroni = (p_bonferroni < 0.05)
- effect_interpretation describes beta direction and magnitude

*Log Validation:*
- Required pattern: "Predictor significance tested: 3 predictors  2 outcomes"
- Required pattern: "Bonferroni correction applied: alpha = 0.0083"
- Required pattern: "Dual p-values reported per Decision D068"
- Forbidden patterns: "ERROR", "Missing predictors", "Incorrect alpha"
- Acceptable warnings: "No predictors significant after correction"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step06_test_predictor_significance.log
- Quit script immediately
- g_debug invoked to diagnose root cause

---

### Step 7: Create Model Diagnostics Summary

**Dependencies:** Step 3 (intercept model), Step 4 (slope model)
**Complexity:** Medium (5 minutes)

**Purpose:** Summarize regression diagnostics and model assumptions

**Input:**
- File 1: data/step03_intercept_predictions.csv (intercept diagnostics)
- File 2: data/step04_slope_predictions.csv (slope diagnostics)
- File 3: data/step02_regression_input.csv (residuals analysis)

**Processing:**
- Function: `compute_regression_diagnostics()` for comprehensive assumption checking
- Normality tests (Shapiro-Wilk on residuals)
- Homoscedasticity tests (Breusch-Pagan)
- VIF assessment for multicollinearity
- Cook's D for influential observations
- Recommendations for assumption violations

**Output:**
- File: data/step07_model_diagnostics.csv
- Format: CSV with columns: model, test, statistic, p_value, assumption_met, remedial_action
- Expected Rows: ~12 (6 tests  2 models)
- Expected Columns: 6

**Validation Requirement:**
Validation tools MUST be used after diagnostic testing and assumption evaluation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_model_diagnostics.csv exists (exact path)
- Expected rows: 10-15 (diagnostic tests for both models)
- Expected columns: 6 (model through remedial_action)
- Data types: model (object), test (object), remedial_action (object), all numeric columns (float64)

*Value Ranges:*
- statistic unrestricted (depends on test type)
- p_value in [0, 1] (diagnostic test p-values)
- assumption_met in {0, 1} (binary pass/fail)

*Data Quality:*
- Both models represented (intercept, slope)
- All key diagnostic tests present (normality, homoscedasticity, VIF, Cook's D)
- assumption_met = (p_value > 0.05) for most tests
- remedial_action provides specific recommendations

*Log Validation:*
- Required pattern: "Diagnostic tests completed: intercept and slope models"
- Required pattern: "Assumption violations detected: [count]"
- Required pattern: "Remedial actions recommended where needed"
- Forbidden patterns: "ERROR", "Diagnostic test failed", "Missing model"
- Acceptable warnings: "Assumption violation: [specific test]"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step07_model_diagnostics.log
- Quit script immediately
- g_debug invoked to diagnose root cause

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs - intermediate and final)
- data/step00_random_effects.csv (extracted LMM random effects from Ch5)
- data/step01_cognitive_tests.csv (standardized RAVLT, BVMT, RPM T-scores)
- data/step02_regression_input.csv (merged dataset for analysis)
- data/step03_intercept_predictions.csv (intercept regression results)
- data/step04_slope_predictions.csv (slope regression results)
- data/step05_r_squared_comparison.csv (bootstrap comparison of R values)
- data/step06_predictor_significance.csv (individual predictor tests with dual p-values)
- data/step07_model_diagnostics.csv (assumption testing and diagnostics)

### Logs (ONLY execution logs - .log files capturing stdout/stderr)
- logs/step00_extract_random_effects.log
- logs/step01_extract_cognitive_tests.log
- logs/step02_merge_data.log
- logs/step03_fit_intercept_model.log
- logs/step04_fit_slope_model.log
- logs/step05_compare_r_squared.log
- logs/step06_test_predictor_significance.log
- logs/step07_model_diagnostics.log

### Plots (EMPTY until rq_plots runs)
- plots/intercept_vs_slope_comparison.png (created by rq_plots, NOT analysis steps)
- plots/regression_diagnostics.png (created by rq_plots)

### Results (EMPTY until rq_results runs)
- results/summary.md (created by rq_results, NOT analysis steps)

---

## Expected Data Formats

### Random Effects Format (Step 0 Output)
- File: data/step00_random_effects.csv
- Format: Wide format (one row per participant)
- Columns: UID (participant ID), intercept (Day 0 baseline), slope (forgetting rate), se_intercept, se_slope
- Data Types: UID (string), numeric columns (float64)
- Expected: 100 rows x 5 columns

### Cognitive Tests Format (Step 1 Output)  
- File: data/step01_cognitive_tests.csv
- Format: Wide format (one row per participant)
- Columns: UID, RAVLT_T (T-score), BVMT_T (T-score), RPM_T (T-score)
- Data Types: UID (string), test scores (float64)
- T-scores: M=50, SD=10 standardization
- Expected: 100 rows x 4 columns

### Regression Results Format (Steps 3-4 Output)
- Files: data/step03_intercept_predictions.csv, data/step04_slope_predictions.csv
- Format: Long format (one row per model term)
- Columns: predictor, beta, se, t, p_uncorrected, p_bonferroni, CI_lower, CI_upper, VIF
- Expected: 4 rows x 9 columns per model
- Terms: (Intercept), RAVLT_T, BVMT_T, RPM_T

### R Comparison Format (Step 5 Output)
- File: data/step05_r_squared_comparison.csv
- Format: Summary format (one row per comparison)
- Columns: model, r_squared, adj_r_squared, bootstrap_ci_lower, bootstrap_ci_upper, difference, difference_ci_lower, difference_ci_upper, p_value
- Expected: 3 rows x 9 columns
- Models: intercept, slope, difference (intercept - slope)

---

## Cross-RQ Dependencies

**This RQ depends on:** Ch5 5.1.1 (Functional Form Comparison - provides LMM random effects)

**Required Files from Ch5 5.1.1:**
- results/ch5/5.1.1/data/step05_lmm_model_summary.txt (fitted LMM model)
- Alternative: results/ch5/5.1.1/data/step04_lmm_input.csv (theta scores with TSVR)

**Status Check:**
- Step 0 should verify Ch5 5.1.1 LMM outputs exist
- If missing: QUIT with "FAIL: Ch5 5.1.1 must complete LMM fitting before this RQ"

**Data Integration:**
- Step 0: Extract random effects from Ch5 LMM using `extract_random_effects_from_lmm()`
- Expected: 100 participants with intercept/slope estimates
- BLUP shrinkage bias acknowledged but analysis proceeds per concept validation

---

## Validation Requirements

**CRITICAL MANDATE:**

Every analysis step in this plan MUST use validation tools after analysis tool execution.

This is not optional. This is the core architectural principle preventing cascading failures observed in v3.0 (where analysis errors propagated undetected through multiple downstream steps before discovery).

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

#### Step 0: Extract Random Effects from Ch5 LMM

**Analysis Tool:** `extract_random_effects_from_lmm` (determined by rq_tools)
**Validation Tool:** (determined by rq_tools - likely `validate_dataframe_structure`)

**What Validation Checks:**
- Output file exists (data/step00_random_effects.csv)
- Expected column count (5 columns: UID + 4 random effects terms)
- Expected row count (100 participants)
- Value ranges: intercept/slope in reasonable bounds, SEs positive
- No NaN values in random effects estimates
- UID format consistency

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step00_extract_random_effects.log
- Quit script immediately
- g_debug invoked to diagnose random effects extraction

#### Step 1: Extract and Standardize Cognitive Tests

**Analysis Tool:** `extract_cognitive_tests` + `standardize_to_t_scores`
**Validation Tool:** (determined by rq_tools - likely `validate_standardization`)

**What Validation Checks:**
- T-scores approximately M=50, SD=10 (standardization verification)
- Value ranges: T-scores in [10, 90] (reasonable bounds)
- No NaN values in cognitive test data
- All 3 tests present (RAVLT, BVMT, RPM)
- Expected participant count (100)

**Expected Behavior on Validation Failure:**
- Raise error with specific standardization failure
- Log failure to logs/step01_extract_cognitive_tests.log
- Quit script immediately
- g_debug invoked to diagnose cognitive data extraction

#### Step 2: Merge Datasets

**Analysis Tool:** pandas merge operation
**Validation Tool:** (determined by rq_tools - likely `validate_dataframe_structure`)

**What Validation Checks:**
- All participants successfully matched (100 rows preserved)
- All columns present from both input datasets
- No data loss during merge operation
- No duplicate UIDs in merged dataset

**Expected Behavior on Validation Failure:**
- Raise error with merge failure details
- Log failure to logs/step02_merge_data.log
- Quit script immediately
- g_debug invoked to diagnose merge issues

#### Steps 3-4: Regression Model Fitting

**Analysis Tool:** `fit_multiple_regression` + `compute_regression_diagnostics`
**Validation Tool:** (determined by rq_tools - likely `validate_regression_assumptions`)

**What Validation Checks:**
- Model convergence achieved
- VIF values < 10 (multicollinearity check)
- R in valid range [0, 1]
- Standard errors positive and reasonable
- Bootstrap CIs computed successfully (1000 iterations)
- All model terms present in output

**Expected Behavior on Validation Failure:**
- Raise error with specific regression failure
- Log failure to appropriate step log
- Quit script immediately  
- g_debug invoked to diagnose regression issues

#### Step 5: R Bootstrap Comparison

**Analysis Tool:** `bootstrap_regression_ci` for R difference
**Validation Tool:** (determined by rq_tools - likely `validate_numeric_range`)

**What Validation Checks:**
- Bootstrap completed 1000 iterations successfully
- R values in [0, 1] range
- Confidence intervals well-formed (lower < upper)
- P-value in [0, 1] range
- Difference calculation correct

**Expected Behavior on Validation Failure:**
- Raise error with bootstrap failure details
- Log failure to logs/step05_compare_r_squared.log
- Quit script immediately
- g_debug invoked to diagnose bootstrap issues

#### Steps 6-7: Significance Testing and Diagnostics

**Analysis Tool:** Multiple comparison correction + diagnostic testing
**Validation Tool:** (determined by rq_tools - likely `validate_hypothesis_test_dual_pvalues`)

**What Validation Checks:**
- Dual p-values present (uncorrected + Bonferroni per Decision D068)
- Bonferroni correction applied correctly (alpha = 0.05/6)
- All diagnostic tests completed
- Assumption violations flagged appropriately
- Remedial recommendations provided

**Expected Behavior on Validation Failure:**
- Raise error with validation specifics
- Log failure to appropriate step log
- Quit script immediately
- g_debug invoked to diagnose testing issues

---

## Summary

**Total Steps:** 8 (Step 0: extractions + Steps 1-7: analysis)
**Estimated Runtime:** Medium complexity (~45 minutes total)
**Cross-RQ Dependencies:** Ch5 5.1.1 (LMM random effects)
**Primary Outputs:** Random effects extraction, regression results, R comparison, predictor significance, diagnostics
**Validation Coverage:** 100% (all 8 steps have validation requirements)

**Key Hypotheses Tested:**
- H1: R_intercept > R_slope (cognitive tests predict encoding > consolidation)
- H2: R_intercept significantly > R_slope (bootstrap CI excludes 0)
- H3: No predictor significantly predicts slope after Bonferroni correction

**Critical Methods:**
- BLUP extraction with acknowledged shrinkage bias
- T-score standardization for cognitive predictors
- Bootstrap confidence intervals (1000 iterations, seed=42)
- Dual p-value reporting per Decision D068
- Comprehensive regression diagnostics

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2026-01-04): Initial plan created by rq_planner agent for RQ 7.1.2 intercept vs slope prediction analysis