# Analysis Plan for RQ 6.6.2: Individual Difference Predictors of High-Confidence Errors

**Created by:** rq_planner agent
**Date:** 2025-12-06
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This RQ examines individual differences in high-confidence error (HCE) rates across N=100 participants. The analysis tests the Dunning-Kruger hypothesis in the episodic memory domain: whether low-performing individuals make more HCEs due to combined memory and metacognitive deficits. The workflow involves aggregating HCE rates per participant (from RQ 6.6.1), extracting baseline predictors (accuracy from Ch5 5.1.1, confidence from RQ 6.1.1, age from dfData.csv), computing confidence bias (baseline confidence - baseline accuracy), and fitting a multiple regression model with dual p-value reporting per Decision D068.

**Pipeline:** Multiple regression (no IRT, no LMM)
**Steps:** 5 analysis steps (Step 0: data merging + Steps 1-4: regression analysis)
**Estimated Runtime:** Low (<15 minutes total - data aggregation and regression only)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni correction for 4 predictors)

---

## Analysis Plan

### Step 0: Merge Predictor Data Sources

**Dependencies:** None (first step)
**Complexity:** Low (data extraction and merging only)

**Purpose:** Extract and merge all predictor variables from multiple source RQs and dfData.csv into a single analysis dataset.

**Input:**

**File 1:** results/ch6/6.6.1/data/step01_hce_rates.csv
**Source:** RQ 6.6.1 Step 1 (HCE rate computation)
**Format:** CSV with columns:
  - `composite_ID` (string, format: UID_test, e.g., P001_T1)
  - `HCE_rate` (float, range: [0, 1], proportion of high-confidence errors)
**Expected Rows:** 400 (100 participants x 4 tests)

**File 2:** results/ch5/5.1.1/data/step03_theta_scores.csv
**Source:** Ch5 5.1.1 Step 3 (IRT theta estimation for accuracy)
**Format:** CSV with columns:
  - `composite_ID` (string)
  - `theta_All` (float, IRT ability estimate for omnibus "All" factor)
  - `se_All` (float, standard error of theta estimate)
**Expected Rows:** 400 (100 participants x 4 tests)
**Filter:** Extract only T1 (Day 0) observations for baseline accuracy

**File 3:** results/ch6/6.1.1/data/step03_theta_confidence.csv
**Source:** RQ 6.1.1 Step 3 (IRT theta estimation for confidence ratings)
**Format:** CSV with columns:
  - `composite_ID` (string)
  - `theta_confidence` (float, IRT ability estimate for confidence)
  - `se_confidence` (float, standard error)
**Expected Rows:** 400 (100 participants x 4 tests)
**Filter:** Extract only T1 (Day 0) observations for baseline confidence

**File 4:** data/cache/dfData.csv
**Source:** Master data file
**Format:** CSV with columns:
  - `UID` (string, participant identifier)
  - `Age` (int, participant age in years)
**Expected Rows:** 100 participants (unique UIDs)

**Processing:**

1. **Aggregate HCE rates per participant:**
   - Group File 1 by UID (extract from composite_ID)
   - Compute mean(HCE_rate) across 4 timepoints per participant
   - Result: 100 rows (one per participant), columns: UID, HCE_rate_mean

2. **Extract baseline accuracy (Day 0 only):**
   - Filter File 2 to composite_ID ending in "_T1" (Day 0)
   - Extract columns: UID (from composite_ID), theta_All
   - Rename theta_All to baseline_accuracy
   - Result: 100 rows, columns: UID, baseline_accuracy

3. **Extract baseline confidence (Day 0 only):**
   - Filter File 3 to composite_ID ending in "_T1" (Day 0)
   - Extract columns: UID (from composite_ID), theta_confidence
   - Rename theta_confidence to baseline_confidence
   - Result: 100 rows, columns: UID, baseline_confidence

4. **Extract age:**
   - Read File 4, extract columns: UID, Age
   - Result: 100 rows, columns: UID, Age

5. **Merge all predictors:**
   - Left join aggregated HCE rates with baseline_accuracy on UID
   - Left join with baseline_confidence on UID
   - Left join with Age on UID
   - Check: All 100 participants have complete data (no NaN values)
   - Result: 100 rows, columns: UID, HCE_rate_mean, baseline_accuracy, baseline_confidence, Age

6. **Compute confidence bias:**
   - Standardize baseline_accuracy (z-score)
   - Standardize baseline_confidence (z-score)
   - confidence_bias = z(baseline_confidence) - z(baseline_accuracy)
   - Add confidence_bias column to dataset
   - Result: 100 rows, columns: UID, HCE_rate_mean, baseline_accuracy, baseline_confidence, Age, confidence_bias

**Output:**

**File:** data/step00_predictor_data.csv
**Format:** CSV, one row per participant
**Columns:**
  - `UID` (string, participant identifier)
  - `HCE_rate_mean` (float, mean HCE rate across 4 timepoints, range: [0, 1])
  - `baseline_accuracy` (float, Day 0 theta from Ch5 5.1.1, IRT scale typically [-3, 3])
  - `baseline_confidence` (float, Day 0 theta from RQ 6.1.1, IRT scale typically [-3, 3])
  - `Age` (int, years)
  - `confidence_bias` (float, difference of z-standardized confidence - accuracy)
**Expected Rows:** 100 (all participants)

**Validation Requirement:**

Validation tools MUST be used after data merging execution. Specific validation tools determined by rq_tools based on data format and completeness requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_predictor_data.csv exists (exact path)
- Expected rows: 100 (all participants)
- Expected columns: 6 (UID, HCE_rate_mean, baseline_accuracy, baseline_confidence, Age, confidence_bias)
- Data types: UID (string), HCE_rate_mean (float), baseline_accuracy (float), baseline_confidence (float), Age (int), confidence_bias (float)

*Value Ranges:*
- HCE_rate_mean in [0, 1] (proportion cannot exceed bounds)
- baseline_accuracy in [-3, 3] (typical IRT theta range)
- baseline_confidence in [-3, 3] (typical IRT theta range)
- Age in [18, 90] (study inclusion criteria)
- confidence_bias in [-6, 6] (difference of z-scores, extreme values indicate outliers)

*Data Quality:*
- No NaN values tolerated (complete case analysis required)
- Expected N: Exactly 100 rows (all participants)
- No duplicate UIDs
- Distribution check: HCE_rate_mean should have variance (not all identical values)

*Log Validation:*
- Required pattern: "Data merge complete: 100 participants with complete predictors"
- Required pattern: "All source files merged successfully"
- Forbidden patterns: "ERROR", "NaN values detected", "Missing data"
- Acceptable warnings: None expected for data merging

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 100 rows, found 87 - missing participant data")
- Log failure to logs/step00_merge_predictor_data.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose missing data source

---

### Step 1: Standardize Predictors

**Dependencies:** Step 0 (requires merged predictor data)
**Complexity:** Low (z-score transformations only)

**Purpose:** Standardize all predictors to z-scores for effect size comparison in regression model.

**Input:**

**File:** data/step00_predictor_data.csv
**Format:** CSV from Step 0
**Columns:** UID, HCE_rate_mean, baseline_accuracy, baseline_confidence, Age, confidence_bias
**Expected Rows:** 100

**Processing:**

1. **Standardize predictors (z-scores):**
   - z_baseline_accuracy = (baseline_accuracy - mean) / SD
   - z_baseline_confidence = (baseline_confidence - mean) / SD
   - z_Age = (Age - mean) / SD
   - z_confidence_bias = (confidence_bias - mean) / SD

2. **Leave outcome unstandardized:**
   - HCE_rate_mean remains on original [0, 1] scale (proportion)
   - Rationale: Interpretability of regression intercept (mean HCE rate at average predictor levels)

3. **Add standardized columns to dataset:**
   - Columns: UID, HCE_rate_mean, z_baseline_accuracy, z_baseline_confidence, z_Age, z_confidence_bias

**Output:**

**File:** data/step01_standardized_predictors.csv
**Format:** CSV, one row per participant
**Columns:**
  - `UID` (string)
  - `HCE_rate_mean` (float, unstandardized outcome)
  - `z_baseline_accuracy` (float, z-scored predictor)
  - `z_baseline_confidence` (float, z-scored predictor)
  - `z_Age` (float, z-scored predictor)
  - `z_confidence_bias` (float, z-scored predictor)
**Expected Rows:** 100

**Validation Requirement:**

Validation tools MUST be used after standardization execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_standardized_predictors.csv exists
- Expected rows: 100
- Expected columns: 6 (UID, HCE_rate_mean, z_baseline_accuracy, z_baseline_confidence, z_Age, z_confidence_bias)
- Data types: UID (string), all others (float)

*Value Ranges:*
- HCE_rate_mean in [0, 1] (unchanged from Step 0)
- z_baseline_accuracy approximately in [-3, 3] (z-scores, extreme values rare)
- z_baseline_confidence approximately in [-3, 3]
- z_Age approximately in [-3, 3]
- z_confidence_bias approximately in [-3, 3]

*Data Quality:*
- No NaN values
- All 100 participants present
- Z-score validation: mean(z_*) approximately 0 (within 0.01 tolerance)
- Z-score validation: SD(z_*) approximately 1 (within 0.01 tolerance)

*Log Validation:*
- Required pattern: "Standardization complete: 4 predictors z-scored"
- Required pattern: "Z-score validation PASS: mean near 0, SD near 1"
- Forbidden patterns: "ERROR", "Standardization FAIL"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Z-score mean = 0.15, expected near 0")
- Log failure to logs/step01_standardize_predictors.log
- Quit script immediately
- g_debug invoked

---

### Step 2: Fit Multiple Regression Model

**Dependencies:** Step 1 (requires standardized predictors)
**Complexity:** Low (OLS regression fitting only)

**Purpose:** Fit multiple regression predicting HCE_rate_mean from 4 standardized predictors.

**Input:**

**File:** data/step01_standardized_predictors.csv
**Format:** CSV from Step 1
**Columns:** UID, HCE_rate_mean, z_baseline_accuracy, z_baseline_confidence, z_Age, z_confidence_bias
**Expected Rows:** 100

**Processing:**

1. **Specify regression model:**
   - Formula: HCE_rate_mean ~ z_baseline_accuracy + z_baseline_confidence + z_Age + z_confidence_bias
   - Method: Ordinary Least Squares (OLS)
   - No interaction terms (main effects only)

2. **Fit model:**
   - Use statsmodels OLS or similar
   - Extract: coefficients, SE, t-values, p-values, R-squared, F-statistic

3. **Check convergence:**
   - Model should converge successfully (no warnings)
   - All coefficients should have finite values (no NaN or inf)

**Output:**

**File:** data/step02_regression_model_summary.txt
**Format:** Plain text summary
**Contents:**
  - Model formula
  - R-squared and Adjusted R-squared
  - F-statistic and p-value for overall model
  - Coefficient table (see Step 3 for CSV format)
  - Residual diagnostics summary (mean, SD, normality test)

**Validation Requirement:**

Validation tools MUST be used after regression fitting execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_regression_model_summary.txt exists
- File size > 500 bytes (should contain full summary)

*Value Ranges:*
- R-squared in [0, 1]
- Adjusted R-squared in [0, 1]
- F-statistic > 0
- All coefficients finite (no NaN or inf)
- All SE > 0 (negative SE indicates error)

*Data Quality:*
- Model converged successfully
- All 4 predictors present in coefficient table
- Residuals approximately normal (Shapiro-Wilk p > 0.05 OR visual Q-Q check acceptable)

*Log Validation:*
- Required pattern: "Regression model fitted successfully"
- Required pattern: "R-squared: [value]"
- Forbidden patterns: "ERROR", "Model convergence failed", "NaN coefficients"
- Acceptable warnings: "Residuals slightly non-normal" (regression robust to minor violations)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Model convergence failed")
- Log failure to logs/step02_fit_regression.log
- Quit script immediately
- g_debug invoked to diagnose convergence issue

---

### Step 3: Extract Coefficients with Dual P-Values (Decision D068)

**Dependencies:** Step 2 (requires fitted regression model)
**Complexity:** Low (coefficient extraction + Bonferroni correction)

**Purpose:** Extract regression coefficients and compute dual p-values per Decision D068 (uncorrected + Bonferroni-corrected).

**Input:**

**File:** Fitted regression model object from Step 2 (in-memory or pickled)
**Format:** statsmodels OLS results object

**Processing:**

1. **Extract coefficient table:**
   - Predictor name
   - Coefficient (beta weight - standardized effect size)
   - Standard error
   - t-value
   - p-value (uncorrected)

2. **Compute Bonferroni correction:**
   - Number of predictors: 4
   - Bonferroni alpha: 0.05 / 4 = 0.0125
   - p_bonferroni = min(p_uncorrected x 4, 1.0)

3. **Flag significance:**
   - sig_uncorrected: p_uncorrected < 0.05
   - sig_bonferroni: p_bonferroni < 0.05

**Output:**

**File:** data/step03_regression_coefficients.csv
**Format:** CSV, one row per predictor (4 predictors + 1 intercept = 5 rows)
**Columns:**
  - `predictor` (string: Intercept, z_baseline_accuracy, z_baseline_confidence, z_Age, z_confidence_bias)
  - `coefficient` (float, beta weight)
  - `SE` (float, standard error)
  - `t_value` (float)
  - `p_uncorrected` (float, range: [0, 1])
  - `p_bonferroni` (float, range: [0, 1])
  - `sig_uncorrected` (bool, TRUE if p_uncorrected < 0.05)
  - `sig_bonferroni` (bool, TRUE if p_bonferroni < 0.05)
**Expected Rows:** 5 (Intercept + 4 predictors)

**Validation Requirement:**

Validation tools MUST be used after coefficient extraction execution. Specific validation tools determined by rq_tools (Decision D068 dual p-value validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_regression_coefficients.csv exists
- Expected rows: 5 (Intercept + 4 predictors)
- Expected columns: 8 (predictor, coefficient, SE, t_value, p_uncorrected, p_bonferroni, sig_uncorrected, sig_bonferroni)
- Data types: predictor (string), coefficient (float), SE (float), t_value (float), p_uncorrected (float), p_bonferroni (float), sig_uncorrected (bool), sig_bonferroni (bool)

*Value Ranges:*
- coefficient in [-10, 10] (extreme values unlikely for z-scored predictors predicting [0,1] outcome)
- SE > 0 (negative SE impossible)
- t_value finite (no NaN or inf)
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1]
- p_bonferroni >= p_uncorrected (Bonferroni correction weakens significance)

*Data Quality:*
- All 5 rows present (Intercept + 4 predictors)
- No NaN values in coefficient or SE
- At least one p_bonferroni value < 1.0 (correction applied, not all saturated at 1.0)

*Log Validation:*
- Required pattern: "Coefficients extracted with dual p-values (Decision D068)"
- Required pattern: "Bonferroni correction applied: 4 predictors"
- Forbidden patterns: "ERROR", "Missing predictor", "NaN p-value"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Missing predictor: z_baseline_accuracy")
- Log failure to logs/step03_extract_coefficients.log
- Quit script immediately
- g_debug invoked

---

### Step 4: Compute Effect Sizes

**Dependencies:** Step 2 (requires fitted regression model)
**Complexity:** Low (R-squared and partial R-squared computation)

**Purpose:** Compute effect size metrics for overall model and individual predictors.

**Input:**

**File 1:** Fitted regression model object from Step 2
**File 2:** data/step01_standardized_predictors.csv (for partial R-squared computation)

**Processing:**

1. **Overall effect size:**
   - R-squared (total variance explained by all 4 predictors)
   - Adjusted R-squared (penalized for number of predictors)

2. **Partial R-squared per predictor:**
   - Fit full model: HCE_rate_mean ~ all 4 predictors
   - For each predictor:
     - Fit reduced model: HCE_rate_mean ~ other 3 predictors (exclude target predictor)
     - Partial R-squared = R2_full - R2_reduced
     - Interpretation: unique variance explained by that predictor

3. **Standardized beta weights:**
   - Already computed in Step 3 (coefficients on z-scored predictors)
   - Interpretation: effect size in standard deviation units

**Output:**

**File:** data/step04_effect_sizes.csv
**Format:** CSV
**Columns:**
  - `metric` (string: R_squared, Adjusted_R_squared, partial_R2_baseline_accuracy, partial_R2_baseline_confidence, partial_R2_Age, partial_R2_confidence_bias)
  - `value` (float, range: [0, 1] for R-squared metrics)
**Expected Rows:** 6 (2 overall metrics + 4 partial R-squared)

**Validation Requirement:**

Validation tools MUST be used after effect size computation execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_effect_sizes.csv exists
- Expected rows: 6
- Expected columns: 2 (metric, value)
- Data types: metric (string), value (float)

*Value Ranges:*
- All R-squared values in [0, 1]
- Adjusted_R_squared <= R_squared (penalty cannot increase R-squared)
- Sum of partial R-squared values <= R_squared (partial effects non-additive due to correlation)

*Data Quality:*
- No NaN values
- All 6 metrics present
- R_squared > 0 (at least some variance explained)

*Log Validation:*
- Required pattern: "Effect sizes computed: R-squared and partial R-squared"
- Required pattern: "Overall R-squared: [value]"
- Forbidden patterns: "ERROR", "Invalid R-squared"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "R-squared = 1.05, exceeds valid range")
- Log failure to logs/step04_compute_effect_sizes.log
- Quit script immediately
- g_debug invoked

---

## Expected Data Formats

### Step 0 Output: Predictor Data

**File:** data/step00_predictor_data.csv

**Format:** CSV, wide format (one row per participant)

**Columns:**
- `UID` (string, format: P### with leading zeros, e.g., P001)
- `HCE_rate_mean` (float, range: [0, 1], mean HCE rate across 4 timepoints)
- `baseline_accuracy` (float, IRT theta from Ch5 5.1.1 at Day 0)
- `baseline_confidence` (float, IRT theta from RQ 6.1.1 at Day 0)
- `Age` (int, years)
- `confidence_bias` (float, z(baseline_confidence) - z(baseline_accuracy))

**Expected Rows:** 100 (all participants)

**Data Type Constraints:**
- No NaN values allowed (complete case analysis)
- UID must be unique (no duplicates)
- HCE_rate_mean strictly in [0, 1] (proportion)
- Age strictly in [18, 90] (study inclusion criteria)

---

### Step 1 Output: Standardized Predictors

**File:** data/step01_standardized_predictors.csv

**Format:** CSV, wide format (one row per participant)

**Columns:**
- `UID` (string)
- `HCE_rate_mean` (float, unstandardized outcome)
- `z_baseline_accuracy` (float, z-scored)
- `z_baseline_confidence` (float, z-scored)
- `z_Age` (float, z-scored)
- `z_confidence_bias` (float, z-scored)

**Expected Rows:** 100

**Data Type Constraints:**
- All z-scored variables have mean approximately 0 (within 0.01)
- All z-scored variables have SD approximately 1 (within 0.01)
- HCE_rate_mean unchanged from Step 0 (same values)

---

### Step 3 Output: Regression Coefficients

**File:** data/step03_regression_coefficients.csv

**Format:** CSV, one row per predictor (5 rows total)

**Columns:**
- `predictor` (string)
- `coefficient` (float)
- `SE` (float)
- `t_value` (float)
- `p_uncorrected` (float)
- `p_bonferroni` (float)
- `sig_uncorrected` (bool)
- `sig_bonferroni` (bool)

**Expected Rows:** 5 (Intercept + 4 predictors)

**Decision D068 Compliance:**
- BOTH p_uncorrected AND p_bonferroni columns present
- p_bonferroni = min(p_uncorrected x 4, 1.0)
- sig_bonferroni flags survival of Bonferroni correction

---

### Step 4 Output: Effect Sizes

**File:** data/step04_effect_sizes.csv

**Format:** CSV, one row per metric (6 rows total)

**Columns:**
- `metric` (string: R_squared, Adjusted_R_squared, partial_R2_baseline_accuracy, partial_R2_baseline_confidence, partial_R2_Age, partial_R2_confidence_bias)
- `value` (float, range: [0, 1])

**Expected Rows:** 6

**Data Type Constraints:**
- All values in [0, 1]
- Adjusted_R_squared <= R_squared
- Sum(partial R-squared) <= R_squared (non-additive due to correlation)

---

## Cross-RQ Dependencies

### Dependency Type 2: DERIVED Data from Other RQs (Dependencies Exist)

**This RQ requires outputs from:**

- **RQ 6.6.1** (HCE Over Time)
  - File: results/ch6/6.6.1/data/step01_hce_rates.csv
  - Used in: Step 0 (compute individual-level HCE rate via mean across timepoints)
  - Rationale: RQ 6.6.1 computes HCE rates per person-timepoint. This RQ aggregates to person-level for individual difference analysis.

- **Ch5 5.1.1** (Functional Form Comparison - Accuracy Model)
  - File: results/ch5/5.1.1/data/step03_theta_scores.csv
  - Used in: Step 0 (extract Day 0 theta as baseline accuracy predictor)
  - Rationale: Baseline memory ability (Day 0) predicts HCE tendency. Ch5 5.1.1 provides IRT theta estimates for accuracy.

- **RQ 6.1.1** (Confidence Model Selection)
  - File: results/ch6/6.1.1/data/step03_theta_confidence.csv
  - Used in: Step 0 (extract Day 0 theta as baseline confidence predictor)
  - Rationale: Baseline metacognitive ability (Day 0) predicts HCE tendency. RQ 6.1.1 provides IRT theta estimates for confidence ratings.

- **dfData.csv** (Master data file)
  - File: data/cache/dfData.csv
  - Used in: Step 0 (extract Age variable)
  - Rationale: Age as individual difference predictor (testing age null hypothesis consistent with Ch5 findings)

**Execution Order Constraint:**
1. RQ 6.6.1 must complete Step 1 (HCE rates computed)
2. Ch5 5.1.1 must complete Step 3 (accuracy theta estimated)
3. RQ 6.1.1 must complete Step 3 (confidence theta estimated)
4. This RQ executes after all dependencies complete

**Data Source Boundaries:**
- **DERIVED data:** All inputs from prior RQ outputs (no RAW master.xlsx extraction in this RQ)
- **Scope:** This RQ performs regression analysis only (no IRT calibration, no LMM fitting)

**Validation:**
- Step 0: Check results/ch6/6.6.1/data/step01_hce_rates.csv exists (circuit breaker: FILE_MISSING if absent)
- Step 0: Check results/ch5/5.1.1/data/step03_theta_scores.csv exists (circuit breaker: FILE_MISSING if absent)
- Step 0: Check results/ch6/6.1.1/data/step03_theta_confidence.csv exists (circuit breaker: FILE_MISSING if absent)
- Step 0: Check data/cache/dfData.csv exists (circuit breaker: FILE_MISSING if absent)
- If any file missing -> quit with error -> user must execute dependency RQs first

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

---

### Validation Requirements By Step

#### Step 0: Merge Predictor Data Sources

**Analysis Tool:** (determined by rq_tools - likely pandas merge operations)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_data_format + validate_numeric_range)

**What Validation Checks:**
- Output file exists (data/step00_predictor_data.csv)
- Expected row count (100 participants)
- Expected column count (6 columns)
- No NaN values (complete case analysis required)
- HCE_rate_mean in [0, 1]
- baseline_accuracy in [-3, 3]
- baseline_confidence in [-3, 3]
- Age in [18, 90]
- confidence_bias in [-6, 6]
- No duplicate UIDs

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "87 participants found, expected 100 - missing source data")
- Log failure to logs/step00_merge_predictor_data.log
- Quit script immediately
- g_debug invoked to diagnose missing data source

---

#### Step 1: Standardize Predictors

**Analysis Tool:** (determined by rq_tools - likely z-score standardization function)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_standardization)

**What Validation Checks:**
- Output file exists (data/step01_standardized_predictors.csv)
- Expected row count (100)
- All z-scored variables have mean approximately 0 (within 0.01 tolerance)
- All z-scored variables have SD approximately 1 (within 0.01 tolerance)
- No NaN values
- HCE_rate_mean unchanged from Step 0 (unstandardized outcome preserved)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Z-score mean = 0.15, expected near 0")
- Log failure to logs/step01_standardize_predictors.log
- Quit script immediately
- g_debug invoked

---

#### Step 2: Fit Multiple Regression Model

**Analysis Tool:** (determined by rq_tools - likely statsmodels OLS)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_model_convergence)

**What Validation Checks:**
- Model converged successfully (no warnings)
- R-squared in [0, 1]
- F-statistic > 0
- All coefficients finite (no NaN or inf)
- All SE > 0
- Residuals approximately normal (Shapiro-Wilk p > 0.05 OR visual Q-Q acceptable)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Model convergence failed")
- Log failure to logs/step02_fit_regression.log
- Quit script immediately
- g_debug invoked to diagnose convergence issue

---

#### Step 3: Extract Coefficients with Dual P-Values

**Analysis Tool:** (determined by rq_tools - coefficient extraction + Bonferroni correction)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_hypothesis_test_dual_pvalues per Decision D068)

**What Validation Checks:**
- Output file exists (data/step03_regression_coefficients.csv)
- Expected row count (5: Intercept + 4 predictors)
- BOTH p_uncorrected AND p_bonferroni columns present (Decision D068 compliance)
- p_bonferroni >= p_uncorrected (correction weakens significance)
- All p-values in [0, 1]
- All SE > 0

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Missing p_bonferroni column - Decision D068 violated")
- Log failure to logs/step03_extract_coefficients.log
- Quit script immediately
- g_debug invoked

---

#### Step 4: Compute Effect Sizes

**Analysis Tool:** (determined by rq_tools - R-squared and partial R-squared computation)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_numeric_range)

**What Validation Checks:**
- Output file exists (data/step04_effect_sizes.csv)
- Expected row count (6 metrics)
- All R-squared values in [0, 1]
- Adjusted_R_squared <= R_squared
- No NaN values

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "R-squared = 1.05, exceeds valid range")
- Log failure to logs/step04_compute_effect_sizes.log
- Quit script immediately
- g_debug invoked

---

## Summary

**Total Steps:** 5 (Step 0 + Steps 1-4)
**Estimated Runtime:** Low (<15 minutes total - data merging, standardization, regression, coefficient extraction, effect sizes)
**Cross-RQ Dependencies:** 3 (RQ 6.6.1, Ch5 5.1.1, RQ 6.1.1) + dfData.csv
**Primary Outputs:**
- data/step00_predictor_data.csv (100 participants with 4 predictors + outcome)
- data/step01_standardized_predictors.csv (z-scored predictors)
- data/step02_regression_model_summary.txt (model fit statistics)
- data/step03_regression_coefficients.csv (coefficients with dual p-values per Decision D068)
- data/step04_effect_sizes.csv (R-squared and partial R-squared)
**Validation Coverage:** 100% (all 5 steps have validation requirements)

**Key Hypotheses Tested:**
- Dunning-Kruger: Low baseline accuracy predicts high HCE rate (negative coefficient, p < 0.05)
- Confidence bias: High overconfidence predicts high HCE rate (positive coefficient, p < 0.05)
- Metacognitive skill: Low baseline confidence predicts high HCE rate (negative coefficient, p < 0.05)
- Age null: Age does NOT predict HCE rate (p > 0.05, consistent with Ch5 universal age nulls)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent
