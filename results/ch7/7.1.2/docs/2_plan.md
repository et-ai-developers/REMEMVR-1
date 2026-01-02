# Analysis Plan: RQ 7.1.2 - Intercept vs Slope Prediction

**Research Question:** 7.1.2
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines whether cognitive tests predict baseline ability (Day 0 intercept) more than forgetting rate (slope) from Chapter 5 LMM models. The analysis uses a two-stage approach: (1) extract random effects from Ch5 5.1.1 LMM, (2) predict intercepts and slopes using cognitive test scores (RAVLT, BVMT, RPM). The hypothesis is that traditional neuropsychological tests capture encoding processes (intercept) but not consolidation processes (slope).

**Pipeline:** Linear regression (two separate models - one for intercept, one for slope)
**Steps:** 6 total analysis steps (Step 0: dependency validation + Steps 1-5: analysis)
**Estimated Runtime:** Medium (~30-45 minutes total)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni-corrected)
- Two-stage analysis with BLUP extraction bias acknowledged

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify Ch5 5.1.1 outputs exist before proceeding with random effects extraction

**Input:**
- results/ch5/5.1.1/status.yaml (verify rq_results: success)
- results/ch5/5.1.1/data/step05_lmm_model_summary.txt (verify LMM completed)

**Processing:**
- Check Ch5 5.1.1 status shows complete analysis pipeline
- Verify required dependency files exist
- Log dependency validation results

**Output:**
- data/step00_dependency_validation.txt (validation report)

**Validation Requirement:**
Validation tools MUST be used after dependency validation execution. Validation will check that all required dependency files exist and Ch5 5.1.1 completed successfully.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: 1 file, text format
- Content: Status checks for Ch5 5.1.1 completion

*Value Ranges:*
- Text file: Contains "PASS" indicators for each dependency
- No numeric ranges applicable (text validation)

*Data Quality:*
- Required dependencies verified as existing
- Ch5 5.1.1 status.yaml shows rq_results: success
- No missing dependency files

*Log Validation:*
- Required pattern: "All dependencies validated: PASS"
- Required pattern: "Ch5 5.1.1 status: success"
- Forbidden patterns: "ERROR", "Missing dependency"

**Expected Behavior:**
Validate all cross-RQ dependencies exist before proceeding to analysis steps

---

### Step 1: Extract Random Effects from Ch5 LMM
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (<5 minutes)

**Purpose:** Extract participant-level random intercepts and slopes from Ch5 5.1.1 LMM model

**Input:**
- results/ch5/5.1.1/data/step05_lmm_model_summary.txt (or equivalent LMM output)
- results/ch5/5.1.1/data/step04_lmm_input.csv (participant identifiers)

**Processing:**
- Extract random effects (BLUPs) from fitted LMM: Intercept_i and Slope_i per participant
- Alternative approach: Re-fit simplified LMM Theta ~ log_TSVR + (1 + log_TSVR | UID)
- Create participant-level dataset with UID, random intercept, random slope
- Document BLUP extraction method and potential shrinkage bias

**Output:**
- data/step01_random_effects.csv

**Expected Format:**
- Columns: UID (string), intercept (float), slope (float)
- Rows: 100 participants
- Values: intercept in [-2, 2], slope in [-1, 1] (typical random effect ranges)

**Validation Requirement:**
Validation tools MUST be used after random effects extraction tool execution. Validation will verify successful extraction of random effects with appropriate value ranges.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_random_effects.csv: 100 rows x 3 columns (UID: object, intercept: float64, slope: float64)

*Value Ranges:*
- intercept in [-3, 3] (random intercepts centered around 0)
- slope in [-2, 2] (random slopes centered around 0)
- No NaN values (all participants must have random effects)

*Data Quality:*
- All 100 participants present (no missing UIDs)
- No duplicate UIDs
- All numeric values finite (no inf values)

*Log Validation:*
- Required pattern: "Random effects extracted: 100 participants"
- Required pattern: "VALIDATION - PASS: intercept range"
- Forbidden patterns: "ERROR", "NaN random effects", "Extraction failed"

**Expected Behavior:**
Successfully extract random intercepts and slopes for all 100 participants from Ch5 LMM

---

### Step 2: Extract and Standardize Cognitive Tests
**Dependencies:** Step 1 (participant list from random effects)
**Complexity:** Low (<5 minutes)

**Purpose:** Extract cognitive test scores and convert to T-scores (M=50, SD=10) for standardized interpretation

**Input:**
- data/master.xlsx (cognitive test scores)
- data/step01_random_effects.csv (participant UIDs for matching)

**Processing:**
- Extract RAVLT Total (sum of T1-T5), BVMT Total Recognition, RPM scores
- Exclude NART per concept (language validity concerns)
- Convert raw scores to T-scores: T = 50 + 10 * ((X - M) / SD)
- Merge with participant UIDs from Step 1 for consistency
- Handle any missing cognitive test data

**Output:**
- data/step02_cognitive_tests.csv

**Expected Format:**
- Columns: UID (string), RAVLT_T (float), BVMT_T (float), RPM_T (float)
- Rows: 100 participants
- Values: T-scores centered around 50, SD around 10 (20-80 typical range)

**Validation Requirement:**
Validation tools MUST be used after cognitive test standardization execution. Validation will verify T-score conversion was performed correctly.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_cognitive_tests.csv: 100 rows x 4 columns (UID: object, RAVLT_T: float64, BVMT_T: float64, RPM_T: float64)

*Value Ranges:*
- RAVLT_T in [20, 80] (T-scores 3 SD from mean)
- BVMT_T in [20, 80] (T-scores 3 SD from mean)
- RPM_T in [20, 80] (T-scores 3 SD from mean)
- T-score distribution: mean approximately 50, SD approximately 10

*Data Quality:*
- All 100 participants present
- No duplicate UIDs
- Missing data <10% per test (document exclusions if higher)
- T-score standardization verified (mean near 50, SD near 10)

*Log Validation:*
- Required pattern: "T-score conversion complete: 3 tests standardized"
- Required pattern: "RAVLT_T mean: [45-55], SD: [8-12]" (approximate T-score distribution)
- Forbidden patterns: "ERROR", "Standardization failed", "Invalid T-scores"

**Expected Behavior:**
Successfully extract and standardize cognitive test scores for all participants with T-score properties

---

### Step 3: Predict Intercepts (Baseline Ability)
**Dependencies:** Steps 1-2 (random effects + cognitive tests)
**Complexity:** Low (<5 minutes)

**Purpose:** Fit linear regression predicting random intercepts using cognitive test T-scores

**Input:**
- data/step01_random_effects.csv (intercept values)
- data/step02_cognitive_tests.csv (cognitive predictors)

**Processing:**
- Merge datasets on UID
- Fit model: Intercept ~ RAVLT_T + BVMT_T + RPM_T
- Extract R², adjusted R², F-statistic, overall model p-value
- Extract individual beta coefficients, standard errors, t-statistics
- Compute uncorrected p-values for each predictor
- Apply Bonferroni correction: alpha = 0.05/6 = 0.0083 (3 predictors x 2 models)
- Report BOTH uncorrected AND Bonferroni-corrected p-values (Decision D068)
- Check model assumptions: residual normality, homoscedasticity, multicollinearity (VIF)

**Output:**
- data/step03_intercept_predictions.csv (model results)
- data/step03_intercept_diagnostics.txt (assumption checks)

**Expected Format - Model Results:**
- Columns: predictor (string), beta (float), se (float), t_stat (float), p_uncorrected (float), p_bonferroni (float)
- Additional: R_squared (float), adj_R_squared (float), F_stat (float), model_p (float)

**Validation Requirement:**
Validation tools MUST be used after intercept regression execution. Validation will verify model fitting, dual p-value reporting, and assumption checks.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_intercept_predictions.csv: 3 rows x 6 columns (predictors + statistics)
- data/step03_intercept_diagnostics.txt: 1 file, text format (assumption tests)

*Value Ranges:*
- beta in [-2, 2] (standardized predictors, reasonable effect sizes)
- se > 0 (standard errors must be positive)
- t_stat in [-10, 10] (reasonable test statistics)
- p_uncorrected in [0, 1], p_bonferroni in [0, 1] (valid p-values)
- R_squared in [0, 1] (valid proportion of variance)
- VIF < 10 (multicollinearity check, <5 preferred)

*Data Quality:*
- All 3 predictors present (RAVLT_T, BVMT_T, RPM_T)
- Dual p-values for each predictor (Decision D068 compliance)
- Model converged successfully (no estimation failures)
- Assumption tests completed (normality, homoscedasticity)

*Log Validation:*
- Required pattern: "Intercept model fitted: R² = X.XX"
- Required pattern: "VALIDATION - PASS: dual p-values"
- Required pattern: "Assumption checks complete: VIF < 10"
- Forbidden patterns: "ERROR", "Model failed", "Convergence issues"
- Acceptable warnings: "Bonferroni correction applied"

**Expected Behavior:**
Fit regression model predicting intercepts with dual p-value reporting and assumption validation

---

### Step 4: Predict Slopes (Forgetting Rate)
**Dependencies:** Steps 1-2 (random effects + cognitive tests)
**Complexity:** Low (<5 minutes)

**Purpose:** Fit linear regression predicting random slopes using cognitive test T-scores

**Input:**
- data/step01_random_effects.csv (slope values)
- data/step02_cognitive_tests.csv (cognitive predictors)

**Processing:**
- Merge datasets on UID (same as Step 3)
- Fit model: Slope ~ RAVLT_T + BVMT_T + RPM_T
- Extract identical statistics as Step 3 (R², betas, dual p-values)
- Apply same Bonferroni correction (alpha = 0.0083)
- Check same model assumptions
- Document BLUP extraction bias limitation for slopes

**Output:**
- data/step04_slope_predictions.csv (model results)
- data/step04_slope_diagnostics.txt (assumption checks)

**Expected Format:**
Same as Step 3 (predictor, beta, se, t_stat, p_uncorrected, p_bonferroni, R², etc.)

**Validation Requirement:**
Validation tools MUST be used after slope regression execution. Validation will verify model fitting and dual p-value reporting identical to intercept model.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_slope_predictions.csv: 3 rows x 6 columns (predictors + statistics)
- data/step04_slope_diagnostics.txt: 1 file, text format (assumption tests)

*Value Ranges:*
- Same ranges as Step 3 (beta, se, t_stat, p-values, R²)
- VIF < 10 for multicollinearity

*Data Quality:*
- Same requirements as Step 3 (3 predictors, dual p-values, convergence)
- BLUP bias acknowledged in diagnostics file

*Log Validation:*
- Required pattern: "Slope model fitted: R² = X.XX"
- Required pattern: "VALIDATION - PASS: dual p-values"
- Required pattern: "BLUP bias documented"
- Forbidden patterns: "ERROR", "Model failed"

**Expected Behavior:**
Fit regression model predicting slopes with same structure as intercept model

---

### Step 5: Compare R² Values Between Models
**Dependencies:** Steps 3-4 (both regression models)
**Complexity:** Medium (5-15 minutes for bootstrap)

**Purpose:** Test hypothesis that R²_intercept significantly > R²_slope using bootstrap confidence intervals

**Input:**
- data/step03_intercept_predictions.csv (R²_intercept)
- data/step04_slope_predictions.csv (R²_slope)
- data/step01_random_effects.csv + data/step02_cognitive_tests.csv (for bootstrap resampling)

**Processing:**
- Extract R² from both models
- Compute R² difference: ” = R²_intercept - R²_slope
- Implement participant-level block bootstrap (1000 replications)
- For each bootstrap sample: resample participants, refit both models, compute ”_bootstrap
- Compute 95% confidence interval for ” using percentile method
- Test hypothesis: H€: ” d 0 vs H: ” > 0 (one-tailed)
- Optional: Fisher's Z-test for comparing dependent correlations (if assumptions met)

**Output:**
- data/step05_r_squared_comparison.csv

**Expected Format:**
- Columns: R2_intercept (float), R2_slope (float), R2_difference (float), CI_lower (float), CI_upper (float), bootstrap_p (float)
- Single row with comparison results

**Validation Requirement:**
Validation tools MUST be used after R² comparison execution. Validation will verify bootstrap procedure and confidence interval computation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_r_squared_comparison.csv: 1 row x 6 columns (R² statistics)

*Value Ranges:*
- R2_intercept in [0, 1], R2_slope in [0, 1] (valid R² values)
- R2_difference in [-1, 1] (difference of valid proportions)
- CI_lower <= CI_upper (valid confidence interval)
- bootstrap_p in [0, 1] (valid p-value)

*Data Quality:*
- Bootstrap completed 1000 replications (check log for completion)
- Confidence interval computed correctly
- Hypothesis test performed (one-tailed for ” > 0)

*Log Validation:*
- Required pattern: "Bootstrap complete: 1000 replications"
- Required pattern: "R² comparison: intercept X.XX vs slope X.XX"
- Required pattern: "95% CI for difference: [X.XX, X.XX]"
- Forbidden patterns: "ERROR", "Bootstrap failed", "Invalid CI"

**Expected Behavior:**
Complete bootstrap comparison of R² values with confidence intervals supporting hypothesis test

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs - intermediate and final)
- data/step00_dependency_validation.txt (from Step 0: cross-RQ validation)
- data/step01_random_effects.csv (from Step 1: extracted intercepts/slopes)
- data/step02_cognitive_tests.csv (from Step 2: T-scored predictors)
- data/step03_intercept_predictions.csv (from Step 3: intercept model results)
- data/step03_intercept_diagnostics.txt (from Step 3: assumption checks)
- data/step04_slope_predictions.csv (from Step 4: slope model results)
- data/step04_slope_diagnostics.txt (from Step 4: assumption checks)
- data/step05_r_squared_comparison.csv (from Step 5: bootstrap comparison)

### Logs (ONLY execution logs - .log files capturing stdout/stderr)
- logs/step00_validate_dependencies.log
- logs/step01_extract_random_effects.log
- logs/step02_extract_cognitive_tests.log
- logs/step03_predict_intercepts.log
- logs/step04_predict_slopes.log
- logs/step05_compare_r_squared.log

### Plots (EMPTY until rq_plots runs)
- plots/intercept_slope_prediction.png (created by rq_plots, NOT analysis steps)
- plots/model_diagnostics.png (created by rq_plots)

### Results (EMPTY until rq_results runs)
- results/summary.md (created by rq_results, NOT analysis steps)

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 1 ’ Step 2:** Random effects provide participant UIDs for cognitive test extraction

**Steps 1-2 ’ Steps 3-4:** Both datasets merged on UID to create predictor-outcome pairs for regression

**Steps 3-4 ’ Step 5:** R² values extracted from model summary statistics for comparison

### Column Naming Conventions

**Random Effects (Step 1):**
- UID: Participant identifier (format: P### with leading zeros)
- intercept: Random intercept (BLUP) from Ch5 LMM
- slope: Random slope (BLUP) from Ch5 LMM

**Cognitive Tests (Step 2):**
- UID: Participant identifier (matches Step 1)
- RAVLT_T: T-score for RAVLT Total
- BVMT_T: T-score for BVMT Total Recognition
- RPM_T: T-score for Raven's Progressive Matrices

**Regression Results (Steps 3-4):**
- predictor: Test name (RAVLT_T, BVMT_T, RPM_T)
- beta: Standardized regression coefficient
- se: Standard error of beta
- t_stat: t-statistic for significance test
- p_uncorrected: Raw p-value
- p_bonferroni: Bonferroni-corrected p-value (Decision D068)

### Data Type Constraints

**Participant identifiers:** Non-nullable strings (UID must be present for all)
**Statistical estimates:** Non-nullable floats (all estimates must be finite)
**P-values:** Must be in [0, 1] range (invalid p-values indicate computation error)
**R²:** Must be in [0, 1] range (negative R² indicates model problems)
**T-scores:** Should be approximately normal with mean H 50, SD H 10

---

## Cross-RQ Dependencies

**This RQ depends on:** Ch5 5.1.1 (overall episodic memory LMM with random intercepts/slopes)

**Required Files from Ch5 5.1.1:**
- results/ch5/5.1.1/data/step05_lmm_model_summary.txt (fitted LMM with random effects)
- results/ch5/5.1.1/data/step04_lmm_input.csv (participant identifiers)

**Status Check:**
- rq_planner should verify results/ch5/5.1.1/status.yaml shows rq_results: success
- If Ch5 5.1.1 incomplete: QUIT with "FAIL: Ch5 5.1.1 must complete before RQ 7.1.2 (dependency)"

**Data Integration:**
- Step 1: Extract random effects from Ch5 5.1.1 LMM model
- Expected: 100 participants matched (no missing)
- Alternative: Re-fit simplified LMM if random effects extraction problematic

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
- bash execution (Step 14 workflow) will run analysis ’ validation ’ error on validation failure

**Downstream Agent Requirements:**
- **rq_tools:** MUST specify validation tool for EVERY analysis step (no exceptions)
- **rq_analysis:** MUST embed validation tool call for EVERY analysis step (no exceptions)
- **g_code:** MUST generate code with validation function calls (no exceptions)
- **rq_inspect:** MUST verify validation ran successfully (checks logs/stepN_name.log for validation output)

### Validation Requirements By Step

#### Step 0: Validate Cross-RQ Dependencies
**Analysis Tool:** (determined by rq_tools - likely custom dependency checker)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dependencies)

**What Validation Checks:**
- Ch5 5.1.1 status.yaml shows rq_results: success
- Required dependency files exist and are non-empty
- Dependency validation report created successfully

**Expected Behavior on Validation Failure:**
- Raise error with specific missing dependency
- Log failure to logs/step00_validate_dependencies.log
- Quit immediately (do NOT proceed to Step 1)
- User must ensure Ch5 5.1.1 completes before re-running this RQ

#### Step 1: Extract Random Effects
**Analysis Tool:** (determined by rq_tools - likely custom random effects extractor)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_numeric_range)

**What Validation Checks:**
- Output file exists with expected 100 rows x 3 columns
- Random effects in reasonable ranges (intercept/slope not extreme)
- All UIDs present (no missing participants)
- No NaN or infinite values in random effects

#### Step 2: Extract Cognitive Tests
**Analysis Tool:** (determined by rq_tools - likely tools.data.extract_cognitive_tests)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_standardization)

**What Validation Checks:**
- T-score conversion performed correctly (mean H 50, SD H 10)
- All 3 cognitive tests extracted (RAVLT, BVMT, RPM)
- Participant count matches Step 1 (100 participants)
- T-scores in reasonable range [20, 80]

#### Steps 3-4: Regression Models
**Analysis Tool:** (determined by rq_tools - likely linear regression functions)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_hypothesis_test_dual_pvalues)

**What Validation Checks:**
- Model converged successfully
- Dual p-values present (uncorrected + Bonferroni) per Decision D068
- VIF values <10 for multicollinearity
- Residuals meet assumptions (normality, homoscedasticity)
- R² in valid [0, 1] range

#### Step 5: R² Comparison
**Analysis Tool:** (determined by rq_tools - bootstrap comparison function)
**Validation Tool:** (determined by rq_tools - bootstrap validation)

**What Validation Checks:**
- Bootstrap completed specified number of replications (1000)
- Confidence interval bounds are valid (CI_lower <= CI_upper)
- R² values extracted correctly from both models
- Bootstrap p-value in valid [0, 1] range

---

## Summary

**Total Steps:** 6 (Step 0: dependency validation + Steps 1-5: analysis)
**Estimated Runtime:** 30-45 minutes (mostly bootstrap in Step 5)
**Cross-RQ Dependencies:** Ch5 5.1.1 (LMM with random effects)
**Primary Outputs:** Regression models predicting intercepts vs slopes, R² comparison with bootstrap CI
**Validation Coverage:** 100% (all 6 steps have validation requirements)

**Key Hypothesis:** Cognitive tests predict baseline ability (intercept) more strongly than forgetting rate (slope), consistent with tests measuring encoding but not consolidation processes.

**Critical Methodological Notes:**
- Two-stage analysis with BLUP extraction bias acknowledged
- Decision D068 dual p-value reporting implemented
- Bootstrap confidence intervals for dependent R² comparison
- Bonferroni correction for multiple testing (6 tests total)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan ’ creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml ’ creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml ’ generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent