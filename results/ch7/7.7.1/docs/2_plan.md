# Analysis Plan: RQ 7.7.1 - Reverse Inference - Can REMEMVR predict RAVLT?

**Research Question:** 7.7.1
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

**Research Question:** Can REMEMVR performance predict standard test performance (RAVLT, BVMT)? If REMEMVR is a "purer" episodic measure, it should predict traditional tests.

**Analysis Approach:** Bidirectional prediction analysis using multiple regression. Compare reverse prediction (REMEMVR -> cognitive tests) with forward prediction from RQ 7.1.1 (cognitive tests -> REMEMVR) to assess construct overlap and directionality.

**Pipeline:** Reverse Multiple Linear Regression with Cross-validation and Effect Size Analysis
**Steps:** 9 total analysis steps (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** ~45 minutes

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Chapter-level Bonferroni correction: alpha = 0.05/28 = 0.00179
- Random seed=42 for all randomized procedures (reproducibility)

**Data Dependencies:** 
- Ch5 5.1.1 (theta_all scores) - CONFIRMED complete
- Ch7 7.1.1 (forward prediction R² for comparison) - CONFIRMED complete
- master.xlsx (cognitive test scores)

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required dependencies exist before proceeding with reverse inference analysis

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv (theta_all estimates)
- Alternative: results/ch5/5.1.1/data/*theta*.csv (search pattern)
- Primary: results/ch7/7.1.1/data/step04_forward_regression.csv (forward R² values)
- Alternative: results/ch7/7.1.1/data/*regression*.csv (search pattern)
- Primary: data/cache/master.xlsx (cognitive test scores)
- Fallback: data/master.xlsx if cache missing

**Processing:**
- Check Ch5 5.1.1 status.yaml shows rq_results: success
- Verify theta_all file exists with expected format (100 rows x theta_all column)
- Check Ch7 7.1.1 status.yaml shows rq_planner: success (forward analysis planned)
- Verify forward regression results exist (if available) for comparison
- Verify master.xlsx accessible with RAVLT_Total and BVMT_TotR columns
- Log all validation checks with success/failure status

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- File contains: dependency status, file paths found, expected vs actual formats

*Value Ranges:*
- N/A (validation step, no numeric analysis)

*Data Quality:*
- All required dependencies marked as PASS or AVAILABLE
- No MISSING or FAIL status for critical files

*Log Validation:*
- Required patterns: "Ch5 5.1.1: AVAILABLE", "master.xlsx: AVAILABLE"
- Forbidden patterns: "MISSING", "FAIL", "ERROR"
- Acceptable warnings: "Ch7 7.1.1 results not yet available (will compare if present)"

**Expected Behavior on Validation Failure:**
- Raise error with specific missing dependency
- Log to logs/step00_validate_dependencies.log
- QUIT immediately, invoke g_debug

---

### Step 1: Extract and Prepare Cognitive Test Data
**Dependencies:** Step 0 (validation complete)
**Complexity:** Low (~3 minutes)

**Purpose:** Extract RAVLT and BVMT scores from master.xlsx and prepare for analysis

**Input:**
- data/cache/master.xlsx (or data/master.xlsx as fallback)
- Expected columns: UID, RAVLT_Total, BVMT_TotR
- Expected N: 100 participants

**Processing:**
- Load master.xlsx using pandas.read_excel()
- Extract relevant columns: UID, RAVLT_Total, BVMT_TotR
- Check for missing data patterns
- Apply exclusion criteria: remove participants with missing cognitive data
- Convert to standardized T-scores: T = 50 + 10 * (X - mean_X) / SD_X
- Compute descriptive statistics (N, mean, SD, range) for each test
- Verify data quality: outliers >3 SD from mean, impossible values

**Output:**
- data/step01_cognitive_tests.csv (UID, RAVLT_Total, BVMT_TotR, RAVLT_T, BVMT_T)
- data/step01_cognitive_descriptives.csv (descriptive statistics)

**Validation Requirement:**
Validation tools MUST be used after cognitive test extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_cognitive_tests.csv: 95-100 rows x 5 columns (allowing for missing data exclusions)
- Columns: UID (object), RAVLT_Total (int), BVMT_TotR (int), RAVLT_T (float64), BVMT_T (float64)
- data/step01_cognitive_descriptives.csv: 4 rows x 5 columns (2 tests x raw/T-score, plus N row)

*Value Ranges:*
- RAVLT_Total in [15, 75] (sum of 5 trials, healthy adult range)
- BVMT_TotR in [5, 36] (sum of 3 trials, healthy adult range)
- T-scores in [20, 80] (standardized scores, 3 SD range)
- No negative values in raw scores

*Data Quality:*
- Final N >= 90 participants (allow up to 10% missing data)
- No duplicate UIDs
- T-scores properly centered: mean ~50, SD ~10
- No impossible values (negative scores, extreme outliers)

*Log Validation:*
- Required patterns: "Cognitive tests extracted: N=XX participants"
- Required patterns: "T-score standardization complete"
- Forbidden patterns: "ERROR", "FAIL", "negative scores detected"
- Acceptable warnings: "X participants excluded for missing data"

**Expected Behavior on Validation Failure:**
- Raise error with specific data quality issue
- Log to logs/step01_extract_cognitive_tests.log
- Quit immediately, invoke g_debug

---

### Step 2: Extract REMEMVR Theta Scores
**Dependencies:** Step 1 (cognitive tests ready)
**Complexity:** Low (~3 minutes)

**Purpose:** Extract mean theta_all scores from Ch5 5.1.1 and prepare for analysis

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/*theta*.csv
- Expected format: UID, theta_all (mean across sessions)

**Processing:**
- Load theta scores from Ch5 5.1.1 results
- Extract UID and theta_all columns (aggregate across REMEMVR sessions)
- Verify all participants have theta estimates
- Convert to standardized T-scores: T = 50 + 10 * (theta - mean_theta) / SD_theta
- Compute descriptive statistics for theta_all
- Check for extreme outliers (>3 SD from mean)

**Output:**
- data/step02_theta_means.csv (UID, theta_all, theta_T)
- data/step02_theta_descriptives.csv (descriptive statistics)

**Validation Requirement:**
Validation tools MUST be used after theta score extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_theta_means.csv: 100 rows x 3 columns
- Columns: UID (object), theta_all (float64), theta_T (float64)
- data/step02_theta_descriptives.csv: 1 row x 5 columns (N, mean, SD, min, max)

*Value Ranges:*
- theta_all in [-3, 3] (IRT ability scale range)
- theta_T in [20, 80] (T-score range, 3 SD)
- No missing values in theta estimates

*Data Quality:*
- All 100 participants present (complete REMEMVR data required)
- No duplicate UIDs
- Theta values within plausible IRT range
- T-scores properly standardized: mean ~50, SD ~10

*Log Validation:*
- Required patterns: "Theta scores extracted: N=100 participants"
- Required patterns: "T-score conversion complete"
- Forbidden patterns: "missing theta", "ERROR", "out of range"

**Expected Behavior on Validation Failure:**
- Raise error with specific theta score issue
- Log to logs/step02_extract_theta_scores.log
- Quit immediately, invoke g_debug

---

### Step 3: Merge Analysis Dataset
**Dependencies:** Steps 1-2 (cognitive tests + theta scores)
**Complexity:** Low (~2 minutes)

**Purpose:** Merge cognitive test scores with REMEMVR theta scores for regression analysis

**Input:**
- data/step01_cognitive_tests.csv (cognitive test T-scores)
- data/step02_theta_means.csv (theta T-scores)

**Processing:**
- Merge datasets on UID using pandas.merge(how='inner')
- Verify complete data for all participants
- Create correlation matrix between variables
- Check for extreme multicollinearity (r > 0.85)
- Apply final exclusions if any participants missing either dataset

**Output:**
- data/step03_analysis_input.csv (UID, RAVLT_T, BVMT_T, theta_T)
- data/step03_correlation_matrix.csv (3x3 correlation matrix)

**Validation Requirement:**
Validation tools MUST be used after dataset merging.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_analysis_input.csv: 90-100 rows x 4 columns
- Columns: UID (object), RAVLT_T (float64), BVMT_T (float64), theta_T (float64)
- data/step03_correlation_matrix.csv: 3 rows x 4 columns (variable names + 3 correlations)

*Value Ranges:*
- All T-scores in [20, 80] range
- Correlations in [-1, 1] range
- No missing values in final dataset

*Data Quality:*
- Final N >= 90 participants (some exclusions acceptable)
- No duplicate UIDs
- All correlations <0.85 (no extreme multicollinearity)
- Complete data for all retained participants

*Log Validation:*
- Required patterns: "Dataset merged: N=XX participants with complete data"
- Required patterns: "Correlation matrix computed"
- Forbidden patterns: "multicollinearity detected", "ERROR"
- Acceptable warnings: "Y participants excluded for incomplete data"

**Expected Behavior on Validation Failure:**
- Raise error with specific merging issue
- Log to logs/step03_merge_analysis_dataset.log
- Quit immediately, invoke g_debug

---

### Step 4: Reverse Regression Models
**Dependencies:** Step 3 (merged dataset ready)
**Complexity:** Medium (~8 minutes)

**Purpose:** Fit reverse prediction models: RAVLT ~ REMEMVR and BVMT ~ REMEMVR

**Input:**
- data/step03_analysis_input.csv (complete analysis dataset)

**Processing:**
- Fit Model 1: RAVLT_T ~ theta_T (reverse prediction to RAVLT)
- Fit Model 2: BVMT_T ~ theta_T (reverse prediction to BVMT)
- Implementation: statsmodels.api.OLS with standardized predictors
- Extract for each model: R², adjusted R², F-statistic, beta coefficients
- Compute standard errors and 95% confidence intervals
- Bootstrap 95% CIs for coefficients:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - CI computation: percentile method (2.5th, 97.5th percentiles)
- Multiple comparison correction:
  - Family: Within-RQ (2 models)
  - Bonferroni: alpha = 0.00179/2 = 0.000895 per model
  - Also compute FDR using Benjamini-Hochberg method
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Effect sizes: Cohen's f² = R²/(1-R²) for each model

**Output:**
- data/step04_reverse_regression.csv (model results with dual p-values)
- data/step04_model_coefficients.csv (coefficients with bootstrap CIs)

**Validation Requirement:**
Validation tools MUST be used after reverse regression execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_reverse_regression.csv: 2 rows x 10 columns
- Columns: model, outcome, R2, adj_R2, F_stat, p_uncorrected, p_bonferroni, p_fdr, cohens_f2, N
- data/step04_model_coefficients.csv: 4 rows x 8 columns (2 models x intercept+slope)

*Value Ranges:*
- R² in [0, 1] (valid explained variance range)
- F-statistics > 0 (positive F values)
- p-values in [0, 1] (valid probability range)
- Cohen's f² >= 0 (positive effect sizes)
- Bootstrap CIs: ci_lower < coefficient < ci_upper

*Data Quality:*
- Both models successfully fitted
- No convergence failures or NaN results
- Bootstrap CIs completed for all coefficients
- Dual p-values present for all tests (Decision D068)

*Log Validation:*
- Required patterns: "Model 1 fitted: RAVLT ~ REMEMVR, R² = X.XX"
- Required patterns: "Model 2 fitted: BVMT ~ REMEMVR, R² = X.XX"
- Required patterns: "Bootstrap complete: 1000 iterations"
- Forbidden patterns: "convergence failed", "ERROR", "NaN coefficients"

**Expected Behavior on Validation Failure:**
- Raise error with specific model fitting issue
- Log to logs/step04_reverse_regression.log
- Quit immediately, invoke g_debug

---

### Step 5: Compare to Forward Regression
**Dependencies:** Step 4 (reverse models fitted)
**Complexity:** Medium (~5 minutes)

**Purpose:** Extract forward prediction R² from RQ 7.1.1 and compute asymmetry ratios

**Input:**
- Primary: results/ch7/7.1.1/data/step04_forward_regression.csv (if available)
- Alternative: results/ch7/7.1.1/data/*regression*.csv
- Fallback: Skip comparison if 7.1.1 not completed
- data/step04_reverse_regression.csv (reverse model results)

**Processing:**
- Attempt to load forward regression results from Ch7 7.1.1
- If found: extract R² values for cognitive tests -> REMEMVR prediction
- Compute asymmetry ratios: Forward R² / Reverse R²
- Test difference in prediction strength using bootstrap:
  - Bootstrap difference: Forward R² - Reverse R²
  - Iterations: 1000, seed: 42
  - 95% CI for R² difference
- If 7.1.1 not available: document and proceed with reverse-only analysis
- Create comparison table with both directions

**Output:**
- data/step05_forward_comparison.csv (asymmetry ratios and differences)
- data/step05_bidirectional_summary.csv (comprehensive comparison table)

**Validation Requirement:**
Validation tools MUST be used after forward comparison.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_forward_comparison.csv: variable rows x 6 columns (depends on 7.1.1 availability)
- data/step05_bidirectional_summary.csv: 2 rows x 8 columns (RAVLT, BVMT comparisons)

*Value Ranges:*
- R² values in [0, 1] for both forward and reverse
- Asymmetry ratios > 0 (positive ratios)
- R² differences in [-1, 1] (valid difference range)

*Data Quality:*
- If 7.1.1 available: complete forward-reverse comparisons
- If 7.1.1 missing: documented as "not available for comparison"
- All computed ratios and differences valid (no division by zero)

*Log Validation:*
- Required patterns: "Forward comparison: STATUS" where STATUS = "COMPLETED" or "SKIPPED"
- If completed: "Asymmetry ratios computed for X comparisons"
- Forbidden patterns: "ERROR", "division by zero"
- Acceptable: "7.1.1 not available, reverse-only analysis"

**Expected Behavior on Validation Failure:**
- If comparison fails: log warning and continue with reverse-only
- Log to logs/step05_forward_comparison.log
- Do not quit - comparison is supplementary analysis

---

### Step 6: Effect Sizes and Importance Analysis
**Dependencies:** Step 5 (comparison complete)
**Complexity:** Medium (~6 minutes)

**Purpose:** Compute comprehensive effect sizes and assess practical importance

**Input:**
- data/step04_reverse_regression.csv (model results)
- data/step03_analysis_input.csv (raw data for effect size calculations)

**Processing:**
- Compute Cohen's f² for each model: f² = R²/(1-R²)
- Interpret effect sizes using Cohen's benchmarks: f²=0.02 (small), f²=0.15 (medium), f²=0.35 (large)
- Compute semi-partial correlations for unique variance explained
- Bootstrap effect size confidence intervals:
  - Iterations: 1000, seed: 42
  - Resample participants with replacement
  - Compute R² for each bootstrap sample
  - Convert to f² and compute 95% CI
- Calculate proportion of variance explained vs unexplained
- Assess practical significance thresholds (minimum meaningful R²)

**Output:**
- data/step06_effect_sizes.csv (Cohen's f², semi-partial r, interpretations)
- data/step06_effect_size_bootstrap.csv (bootstrap CIs for effect sizes)

**Validation Requirement:**
Validation tools MUST be used after effect size computation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_effect_sizes.csv: 2 rows x 8 columns (RAVLT, BVMT effect sizes)
- Columns: model, R2, cohens_f2, f2_interpretation, semipartial_r, variance_explained, variance_unexplained, practical_significance
- data/step06_effect_size_bootstrap.csv: 2 rows x 6 columns (bootstrap CIs)

*Value Ranges:*
- Cohen's f² >= 0 (positive effect sizes)
- Semi-partial r in [0, 1] (valid correlation range)
- Variance proportions sum to 1.0 (explained + unexplained = 100%)
- Bootstrap CIs: ci_lower <= f² <= ci_upper

*Data Quality:*
- Effect size interpretations match Cohen's benchmarks
- All bootstrap CIs successfully computed
- Practical significance assessments completed
- No missing values in effect size calculations

*Log Validation:*
- Required patterns: "Effect sizes computed: Cohen's f² for 2 models"
- Required patterns: "Bootstrap effect size CIs: 1000 iterations complete"
- Required patterns: "Practical significance assessed"
- Forbidden patterns: "ERROR", "negative effect size", "bootstrap failed"

**Expected Behavior on Validation Failure:**
- Raise error with specific effect size computation issue
- Log to logs/step06_effect_sizes.log
- Quit immediately, invoke g_debug

---

### Step 7: Model Diagnostics and Assumptions
**Dependencies:** Step 6 (effect sizes computed)
**Complexity:** Medium (~8 minutes)

**Purpose:** Check regression assumptions and apply remedial actions if needed

**Input:**
- data/step04_reverse_regression.csv (fitted models)
- data/step03_analysis_input.csv (raw data for residual analysis)

**Processing:**
- Check regression assumptions for both models:
  - Multicollinearity: VIF calculation (single predictor models, VIF=1)
  - Normality: Shapiro-Wilk test on residuals (p > 0.05 acceptable)
  - Homoscedasticity: Breusch-Pagan test (p > 0.05 acceptable)
  - Linearity: Partial residual plots, visual inspection
  - Influential points: Cook's distance (threshold: 4/N = 0.04 for N=100)
- Remedial actions if violations detected:
  - Normality p < 0.05: Report bootstrap CIs as primary inference
  - Heteroscedasticity p < 0.05: Compute HC3 robust standard errors
  - Cook's D > 0.04: Report results with and without influential points
  - Non-linearity: Document and consider polynomial terms
- Generate assumption summary with pass/fail status for each test

**Output:**
- data/step07_assumption_tests.csv (test results for both models)
- data/step07_model_diagnostics.csv (residual analysis, Cook's D, outliers)
- data/step07_robust_results.csv (robust SEs if heteroscedasticity detected)

**Validation Requirement:**
Validation tools MUST be used after assumption testing.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_assumption_tests.csv: 6 rows x 5 columns (3 tests x 2 models)
- Columns: model, test_type, test_statistic, p_value, status
- data/step07_model_diagnostics.csv: N rows x 6 columns (participant-level diagnostics)
- data/step07_robust_results.csv: present if heteroscedasticity detected

*Value Ranges:*
- Test statistics: appropriate range for each test type
- p-values in [0, 1] (valid probability range)
- Cook's D in [0, 1] typically (distance measure)
- VIF = 1.0 exactly (single predictor models)

*Data Quality:*
- All assumption tests completed for both models
- Status clearly marked as "PASS" or "FAIL" for each test
- If robust methods applied, results table present
- All participants included in diagnostics

*Log Validation:*
- Required patterns: "Assumption testing complete: 2 models x 3 tests"
- Required patterns: "Cook's D outliers: X participants flagged"
- Forbidden patterns: "test failed to run", "ERROR"
- Acceptable warnings: "Normality violated: using bootstrap CIs"

**Expected Behavior on Validation Failure:**
- Log specific assumption test failure
- Continue with available tests, mark failed tests as "ERROR"
- Log to logs/step07_model_diagnostics.log

---

### Step 8: Cross-Validation and Generalization
**Dependencies:** Step 7 (diagnostics complete)
**Complexity:** Medium (~10 minutes)

**Purpose:** Assess model generalizability using cross-validation

**Input:**
- data/step03_analysis_input.csv (complete dataset)
- Model specifications from Step 4

**Processing:**
- Implement 5-fold cross-validation for both models:
  - Random seed: 42 for reproducibility
  - Shuffle: True (randomize before splitting)
  - Stratification: None for regression (use quantile-based if outcome skewed)
  - For each fold: fit on training (80%), evaluate on test (20%)
- Compute cross-validation metrics:
  - Mean and SD of R² across 5 folds
  - Mean and SD of RMSE across folds
  - Mean and SD of MAE across folds
- Assess overfitting:
  - Compare training R² vs test R² for each fold
  - Flag overfitting if train-test gap > 0.10
- Compute generalization stability:
  - SD of test R² across folds (should be <0.05 for stable model)
- Generate learning curves if substantial overfitting detected

**Output:**
- data/step08_cross_validation.csv (5-fold CV results for both models)
- data/step08_generalization_summary.csv (overfitting assessment)

**Validation Requirement:**
Validation tools MUST be used after cross-validation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_cross_validation.csv: 10 rows x 8 columns (5 folds x 2 models)
- Columns: model, fold, train_R2, test_R2, RMSE, MAE, overfitting_gap, N_train, N_test
- data/step08_generalization_summary.csv: 2 rows x 6 columns (summary per model)

*Value Ranges:*
- R² values in [0, 1] for both training and test sets
- RMSE and MAE > 0 (positive error measures)
- Overfitting gap in [-0.5, 0.5] typically (train - test R²)
- N_train ~80, N_test ~20 per fold (5-fold split)

*Data Quality:*
- All 5 folds completed successfully for both models
- No convergence failures in any fold
- Overfitting gap computed for all folds
- Cross-validation stability assessed (SD of test R²)

*Log Validation:*
- Required patterns: "5-fold cross-validation complete: 2 models"
- Required patterns: "Mean test R² = X.XX ± Y.YY across folds"
- Required patterns: "Overfitting assessment: STATUS" (ACCEPTABLE/CONCERN)
- Forbidden patterns: "fold failed", "convergence error", "ERROR"

**Expected Behavior on Validation Failure:**
- Raise error with specific cross-validation issue
- Log to logs/step08_cross_validation.log
- Quit immediately, invoke g_debug

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs in data/ folder)
- step00_dependency_validation.txt (prerequisite check results)
- step01_cognitive_tests.csv (RAVLT, BVMT raw and T-scores)
- step01_cognitive_descriptives.csv (descriptive statistics)
- step02_theta_means.csv (REMEMVR theta_all and T-scores)
- step02_theta_descriptives.csv (theta descriptive statistics)
- step03_analysis_input.csv (merged analysis dataset)
- step03_correlation_matrix.csv (variable intercorrelations)
- step04_reverse_regression.csv (reverse model results with dual p-values)
- step04_model_coefficients.csv (coefficients with bootstrap CIs)
- step05_forward_comparison.csv (asymmetry ratios, if 7.1.1 available)
- step05_bidirectional_summary.csv (comprehensive bidirectional comparison)
- step06_effect_sizes.csv (Cohen's f², interpretations)
- step06_effect_size_bootstrap.csv (bootstrap CIs for effect sizes)
- step07_assumption_tests.csv (normality, homoscedasticity, Cook's D)
- step07_model_diagnostics.csv (residual analysis)
- step07_robust_results.csv (robust SEs if needed)
- step08_cross_validation.csv (5-fold CV results)
- step08_generalization_summary.csv (overfitting assessment)

### Logs (ONLY execution logs in logs/ folder)
- step00_validate_dependencies.log
- step01_extract_cognitive_tests.log
- step02_extract_theta_scores.log
- step03_merge_analysis_dataset.log
- step04_reverse_regression.log
- step05_forward_comparison.log
- step06_effect_sizes.log
- step07_model_diagnostics.log
- step08_cross_validation.log

### Plots (EMPTY until rq_plots runs)
Note: Plot source CSVs will be created in data/ folder:
- step04_*_plot_data.csv (scatter plots for reverse predictions)
- step07_*_plot_data.csv (residual plots, Q-Q plots)
- step08_*_plot_data.csv (cross-validation results)

### Results (EMPTY until rq_results runs)
- summary.md (created by rq_results with comprehensive analysis summary)

---

## Expected Data Formats

### Step-to-Step Transformations
1. **Raw Extraction (Steps 1-2):** master.xlsx + Ch5 theta -> separate T-score files
2. **Merging (Step 3):** Combine T-scores by UID -> complete analysis dataset
3. **Modeling (Step 4):** T-score dataset -> regression models + bootstrap CIs
4. **Comparison (Step 5):** Forward results (if available) -> asymmetry analysis
5. **Effect Sizes (Step 6):** Model R² -> Cohen's f² + practical significance
6. **Diagnostics (Step 7):** Model residuals -> assumption tests + remedial actions
7. **Validation (Step 8):** Complete dataset -> cross-validation metrics

### Column Naming Conventions
- **Participant IDs:** UID (consistent across all files)
- **Raw scores:** RAVLT_Total, BVMT_TotR, theta_all
- **Standardized scores:** RAVLT_T, BVMT_T, theta_T (T-score format)
- **Model results:** R2, adj_R2, cohens_f2 (underscore format)
- **Statistical tests:** p_uncorrected, p_bonferroni, p_fdr (dual reporting per D068)

### Data Type Constraints
- **UIDs:** object/string (no missing values, unique)
- **Scores:** float64 (allow decimal precision for T-scores)
- **Statistical results:** float64 (R², p-values, effect sizes)
- **Counts:** int64 (sample sizes, fold numbers)
- **Text:** object (status fields, interpretations)

---

## Cross-RQ Dependencies

**Dependency 1: Ch5 5.1.1 (REMEMVR theta estimates)**
- Status: CONFIRMED complete (rq_results: success)
- Files: results/ch5/5.1.1/data/step03_theta_scores.csv
- Content: UID + theta_all (mean ability across REMEMVR sessions)
- Fallback: Search pattern results/ch5/5.1.1/data/*theta*.csv

**Dependency 2: Ch7 7.1.1 (Forward prediction comparison)**
- Status: CONFIRMED planned (rq_planner: success)
- Files: results/ch7/7.1.1/data/step04_forward_regression.csv (if execution complete)
- Content: R² values for cognitive tests -> REMEMVR prediction
- Fallback: Skip bidirectional comparison if 7.1.1 not executed yet

**Dependency 3: master.xlsx (Cognitive test scores)**
- Status: Assumed available
- Files: data/cache/master.xlsx or data/master.xlsx
- Content: UID + RAVLT_Total + BVMT_TotR
- Fallback: Error if missing (critical dependency)

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

All 9 steps (Step 0-8) include comprehensive 4-layer validation requirements as specified above in each step's "Substance Validation Criteria" section. Each step requires:

1. **Output Files:** Exact paths, row/column counts, data types
2. **Value Ranges:** Scientific bounds appropriate for each variable
3. **Data Quality:** Missing data tolerance, distribution checks, completeness
4. **Log Validation:** Required success patterns, forbidden error patterns

---

## Summary

**Total Steps:** 9 (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** ~45 minutes
**Cross-RQ Dependencies:** Ch5 5.1.1 (required), Ch7 7.1.1 (optional for comparison)
**Primary Outputs:** Reverse regression models, effect sizes, bidirectional comparison
**Validation Coverage:** 100% (all 9 steps have 4-layer validation requirements)

**Key Hypothesis:** Bidirectional prediction asymmetry - REMEMVR predicts traditional tests moderately (R² = 0.25-0.35) but less strongly than forward prediction, confirming shared but not identical constructs.

**Critical Methodological Notes:**
- Bootstrap procedures use participant-level resampling (seed=42) for stable CIs
- Multiple testing correction applied within-RQ (Bonferroni + FDR)
- Cross-validation assesses generalizability with overfitting detection
- Assumption violations trigger specific remedial actions (robust SEs, bootstrap CIs)
- Bidirectional comparison requires Ch7 7.1.1 completion (fallback: reverse-only)

**Statistical Enhancement Features (v5.1):**
- Random seed=42 specified for all randomized procedures
- Bootstrap: 1000 iterations, participant-level resampling
- Cross-validation: 5-fold with shuffle, overfitting gap threshold 0.10
- Power analysis: Not applicable (descriptive effect size analysis)
- Corrections: Bonferroni α=0.000895, FDR backup, dual reporting (D068)
- Remedial actions: Robust SEs for heteroscedasticity, bootstrap for non-normality

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent v5.1.0
  - Enhanced with statistical implementation specifications per v5.1 requirements
  - Complete 4-layer validation for all 9 steps
  - Cross-RQ dependency validation with fallback paths
  - Bootstrap, CV, and correction specifications included