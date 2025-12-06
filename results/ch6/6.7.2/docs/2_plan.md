# Analysis Plan for RQ 6.7.2: Confidence Variability Predicts Memory Variability

**Created by:** rq_planner agent
**Date:** 2025-12-06
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This RQ examines whether within-person confidence variability correlates with within-person accuracy variability. The analysis tests if individuals with variable confidence judgments (high SD of confidence across items) also show variable memory performance (high SD of accuracy across items). This is a correlation analysis using Pearson r with dual p-value reporting per Decision D068.

**Pipeline:** Correlation analysis (no IRT/LMM - raw item-level data only)

**Steps:** 4 analysis steps

**Estimated Runtime:** Low (<10 minutes total - primarily data aggregation and correlation computation)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (parametric Pearson test + permutation-based resampling)

**Data Source:** Item-level confidence (TC_*) and accuracy (TQ_*) tags from data/cache/dfData.csv

**Analysis Level:** Person-by-timepoint (N=100 participants x 4 tests = 400 observations)

---

## Analysis Plan

### Step 1: Compute Within-Person Confidence Variability

**Dependencies:** None (first step)
**Complexity:** Low (data aggregation - <2 minutes)

**Purpose:** Compute standard deviation of confidence ratings across items for each participant at each test session.

**Input:**

**File:** data/cache/dfData.csv (master dataset)
**Required Columns:**
- `UID` (string, participant identifier)
- `test` (string, test session: T1, T2, T3, T4)
- TC_* columns (confidence ratings, 5-level Likert: 0, 0.25, 0.5, 0.75, 1.0)

**Filters:**
- Paradigms: IFR, ICR, IRE (interactive VR paradigms only, exclude RFR/TCR/RRE)
- Items: All domains (What/Where/When aggregated - omnibus analysis)
- All 100 participants
- All 4 test sessions

**Processing:**

1. Extract TC_* columns for each participant x test combination
2. Compute SD(confidence) across items (within each participant x test)
3. Minimum items requirement: >= 10 items per participant per test for stable SD estimate
4. If participant has < 10 items at a given test, flag as missing (exclude that observation)

**Output:**

**File:** data/step01_sd_confidence.csv
**Format:** CSV, one row per participant x test
**Columns:**
- `UID` (string, participant identifier)
- `test` (string, test session: T1, T2, T3, T4)
- `SD_confidence` (float, standard deviation of confidence ratings across items)
- `N_items` (int, number of items used to compute SD)

**Expected Rows:** ~400 (100 participants x 4 tests, may be fewer if participants have < 10 items)
**Expected Columns:** 4 (UID, test, SD_confidence, N_items)

**Validation Requirement:**

Validation tools MUST be used after data aggregation tool execution. Specific validation tools determined by rq_tools based on data aggregation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_sd_confidence.csv exists (exact path)
- Expected rows: 380-400 (100 participants x 4 tests, some missing allowed if < 10 items)
- Expected columns: 4 (UID, test, SD_confidence, N_items)
- Data types: UID (object/string), test (object/string), SD_confidence (float64), N_items (int64)

*Value Ranges:*
- SD_confidence in [0, 0.5] (confidence on 0-1 scale, max SD = 0.5 when half items are 0, half are 1)
- N_items >= 10 (minimum for stable SD estimate)
- No negative values (SD cannot be negative)

*Data Quality:*
- No NaN values in SD_confidence (if < 10 items, exclude observation entirely)
- No NaN values in N_items (all observations must have item count)
- Expected N: 380-400 rows (some participants may have < 10 items at some tests)
- No duplicate UID x test combinations

*Log Validation:*
- Required pattern: "Computed SD_confidence for {N} observations"
- Required pattern: "Excluded {M} observations with < 10 items"
- Forbidden patterns: "ERROR", "NaN detected in SD_confidence"
- Acceptable warnings: "Participant {UID} test {test} has < 10 items, excluding"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "SD_confidence contains NaN values")
- Log failure to logs/step01_compute_sd_confidence.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose root cause

---

### Step 2: Compute Within-Person Accuracy Variability

**Dependencies:** None (parallel to Step 1, independent)
**Complexity:** Low (data aggregation - <2 minutes)

**Purpose:** Compute standard deviation of accuracy responses across items for each participant at each test session.

**Input:**

**File:** data/cache/dfData.csv (master dataset)
**Required Columns:**
- `UID` (string, participant identifier)
- `test` (string, test session: T1, T2, T3, T4)
- TQ_* columns (accuracy responses, binary: 0 = incorrect, 1 = correct)

**Filters:**
- Same as Step 1 (IFR/ICR/IRE paradigms, all domains, all participants, all tests)

**Processing:**

1. Extract TQ_* columns for each participant x test combination
2. Compute SD(accuracy) across items (within each participant x test)
3. Minimum items requirement: >= 10 items per participant per test (same as Step 1)
4. If participant has < 10 items at a given test, flag as missing (exclude that observation)

**Output:**

**File:** data/step02_sd_accuracy.csv
**Format:** CSV, one row per participant x test
**Columns:**
- `UID` (string, participant identifier)
- `test` (string, test session: T1, T2, T3, T4)
- `SD_accuracy` (float, standard deviation of accuracy responses across items)
- `N_items` (int, number of items used to compute SD)

**Expected Rows:** ~400 (100 participants x 4 tests, may be fewer if participants have < 10 items)
**Expected Columns:** 4 (UID, test, SD_accuracy, N_items)

**Validation Requirement:**

Validation tools MUST be used after data aggregation tool execution. Specific validation tools determined by rq_tools based on data aggregation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_sd_accuracy.csv exists (exact path)
- Expected rows: 380-400 (100 participants x 4 tests, some missing allowed if < 10 items)
- Expected columns: 4 (UID, test, SD_accuracy, N_items)
- Data types: UID (object/string), test (object/string), SD_accuracy (float64), N_items (int64)

*Value Ranges:*
- SD_accuracy in [0, 0.5] (accuracy is binary 0/1, max SD = 0.5 when half items are 0, half are 1)
- N_items >= 10 (minimum for stable SD estimate)
- No negative values (SD cannot be negative)

*Data Quality:*
- No NaN values in SD_accuracy (if < 10 items, exclude observation entirely)
- No NaN values in N_items (all observations must have item count)
- Expected N: 380-400 rows (some participants may have < 10 items at some tests)
- No duplicate UID x test combinations

*Log Validation:*
- Required pattern: "Computed SD_accuracy for {N} observations"
- Required pattern: "Excluded {M} observations with < 10 items"
- Forbidden patterns: "ERROR", "NaN detected in SD_accuracy"
- Acceptable warnings: "Participant {UID} test {test} has < 10 items, excluding"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "SD_accuracy contains NaN values")
- Log failure to logs/step02_compute_sd_accuracy.log
- Quit script immediately (do NOT proceed to Step 3)
- g_debug invoked to diagnose root cause

---

### Step 3: Correlate Confidence Variability vs Accuracy Variability

**Dependencies:** Steps 1 and 2 (requires both SD_confidence and SD_accuracy)
**Complexity:** Low (correlation computation - <1 minute)

**Purpose:** Test correlation between within-person confidence variability and within-person accuracy variability using Pearson r with dual p-values per Decision D068.

**Input:**

**File 1:** data/step01_sd_confidence.csv
**Format:** CSV with columns: UID, test, SD_confidence, N_items
**Expected Rows:** ~400

**File 2:** data/step02_sd_accuracy.csv
**Format:** CSV with columns: UID, test, SD_accuracy, N_items
**Expected Rows:** ~400

**Merge Logic:**
- Merge on UID + test (inner join - keep only observations present in BOTH datasets)
- After merge, expected rows: ~380-400 (some observations may be missing from either dataset)

**Processing:**

1. Merge SD_confidence and SD_accuracy on UID + test
2. Compute Pearson correlation: r(SD_confidence, SD_accuracy)
3. Compute dual p-values per Decision D068:
   - Parametric: Standard Pearson correlation test (assumes bivariate normality)
   - Permutation-based: 10,000 random permutations of SD_confidence, compute null distribution of r
4. Compute 95% confidence interval for r (bootstrapped, 1000 resamples)
5. Interpret effect size: r > 0.50 = strong, r = 0.30-0.50 = moderate, r < 0.30 = weak

**Output:**

**File:** data/step03_correlation.csv
**Format:** CSV, single row with correlation results
**Columns:**
- `r` (float, Pearson correlation coefficient)
- `p_parametric` (float, parametric p-value from Pearson test)
- `p_permutation` (float, permutation-based p-value from 10,000 resamples)
- `CI_lower` (float, lower bound of 95% confidence interval for r)
- `CI_upper` (float, upper bound of 95% confidence interval for r)
- `N` (int, number of observations used in correlation)
- `effect_size_category` (string, "strong" / "moderate" / "weak")

**Expected Rows:** 1 (single correlation result)
**Expected Columns:** 7

**Validation Requirement:**

Validation tools MUST be used after correlation computation. Specific validation tools determined by rq_tools based on Decision D068 dual p-value requirement.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_correlation.csv exists (exact path)
- Expected rows: 1 (single correlation result)
- Expected columns: 7 (r, p_parametric, p_permutation, CI_lower, CI_upper, N, effect_size_category)
- Data types: r (float64), p_parametric (float64), p_permutation (float64), CI_lower (float64), CI_upper (float64), N (int64), effect_size_category (object/string)

*Value Ranges:*
- r in [-1, 1] (correlation coefficient bounds)
- p_parametric in [0, 1] (p-value bounds)
- p_permutation in [0, 1] (p-value bounds)
- CI_lower in [-1, 1] (confidence interval bounds)
- CI_upper in [-1, 1] (confidence interval bounds)
- CI_lower <= r <= CI_upper (confidence interval must contain r)
- N >= 300 (expect ~380-400 observations after merge)

*Data Quality:*
- No NaN values in any column (single-row result must be complete)
- effect_size_category in {"strong", "moderate", "weak"} (valid categories only)
- Consistency check: If |r| > 0.50, effect_size_category = "strong"
- Consistency check: If 0.30 <= |r| <= 0.50, effect_size_category = "moderate"
- Consistency check: If |r| < 0.30, effect_size_category = "weak"

*Log Validation:*
- Required pattern: "Pearson r = {r:.3f}, p_parametric = {p:.4f}, p_permutation = {p:.4f}"
- Required pattern: "95% CI: [{CI_lower:.3f}, {CI_upper:.3f}]"
- Required pattern: "Effect size: {effect_size_category}"
- Required pattern: "VALIDATION - PASS: Dual p-values present (parametric + permutation)"
- Forbidden patterns: "ERROR", "NaN detected in correlation results"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Correlation r outside [-1, 1] bounds")
- Log failure to logs/step03_correlate_variability.log
- Quit script immediately (do NOT proceed to Step 4)
- g_debug invoked to diagnose root cause

---

### Step 4: Prepare Scatterplot Data

**Dependencies:** Step 3 (requires merged SD_confidence + SD_accuracy data)
**Complexity:** Low (data formatting for plotting - <1 minute)

**Purpose:** Create plot source CSV for scatterplot showing relationship between confidence variability and accuracy variability.

**Input:**

**File:** Merged data from Step 3 (SD_confidence + SD_accuracy, created during correlation step)
**Format:** DataFrame with columns: UID, test, SD_confidence, SD_accuracy
**Expected Rows:** ~380-400

**Processing:**

1. Use merged data from Step 3 (already contains both SD_confidence and SD_accuracy)
2. Add regression line coordinates:
   - Fit linear regression: SD_accuracy ~ SD_confidence
   - Generate regression line points: x = seq(min(SD_confidence), max(SD_confidence), length=100)
   - Compute y = intercept + slope * x
3. Format for plotting:
   - Observed points: UID, test, SD_confidence, SD_accuracy
   - Regression line: x, y (100 points for smooth line)

**Output:**

**File 1:** data/step04_variability_scatterplot_data.csv
**Format:** CSV, one row per observation (participant x test)
**Columns:**
- `UID` (string, participant identifier)
- `test` (string, test session)
- `SD_confidence` (float, x-axis)
- `SD_accuracy` (float, y-axis)

**Expected Rows:** ~380-400
**Expected Columns:** 4

**File 2:** data/step04_variability_regression_line.csv
**Format:** CSV, regression line coordinates
**Columns:**
- `SD_confidence` (float, x values for regression line)
- `SD_accuracy_predicted` (float, y values for regression line)

**Expected Rows:** 100 (smooth regression line)
**Expected Columns:** 2

**Validation Requirement:**

Validation tools MUST be used after plot data preparation. Specific validation tools determined by rq_tools based on plot data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_variability_scatterplot_data.csv exists (exact path)
- Expected rows: 380-400 (one per observation)
- Expected columns: 4 (UID, test, SD_confidence, SD_accuracy)
- Data types: all float64 except UID and test (object/string)

- data/step04_variability_regression_line.csv exists (exact path)
- Expected rows: 100 (regression line points)
- Expected columns: 2 (SD_confidence, SD_accuracy_predicted)
- Data types: both float64

*Value Ranges:*
- SD_confidence in [0, 0.5] (both files)
- SD_accuracy in [0, 0.5] (scatterplot data)
- SD_accuracy_predicted in [0, 0.5] (regression line, may extend slightly beyond data range)

*Data Quality:*
- No NaN values in any column (both files)
- No duplicate UID x test combinations (scatterplot data)
- Regression line x values sorted ascending (monotonic)

*Log Validation:*
- Required pattern: "Created scatterplot data: {N} observations"
- Required pattern: "Created regression line: 100 points"
- Forbidden patterns: "ERROR", "NaN detected in plot data"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Scatterplot data contains NaN values")
- Log failure to logs/step04_prepare_scatterplot_data.log
- Quit script immediately
- g_debug invoked to diagnose root cause

**Plot Description:** Scatterplot with observed points (SD_confidence vs SD_accuracy) and regression line, showing relationship between confidence variability and accuracy variability

**Plotting Function (rq_plots will call):** Scatterplot with regression line
- rq_plots agent will read data/step04_variability_scatterplot_data.csv and data/step04_variability_regression_line.csv
- Generate scatterplot with regression line overlay
- PNG output saved to plots/ folder by rq_plots (NOT during analysis)

---

## Expected Data Formats

### Step 1 -> Step 3 Transformation

**Input (Step 1 Output):**
- File: data/step01_sd_confidence.csv
- Format: One row per participant x test
- Columns: UID, test, SD_confidence, N_items

**Input (Step 2 Output):**
- File: data/step02_sd_accuracy.csv
- Format: One row per participant x test
- Columns: UID, test, SD_accuracy, N_items

**Merge Logic (Step 3):**
- Merge on: UID + test (inner join)
- Keep: Observations present in BOTH datasets
- Result: ~380-400 observations (some may be missing from either dataset if < 10 items)

**Output (Step 3 Correlation):**
- File: data/step03_correlation.csv
- Format: Single row with correlation statistics
- Columns: r, p_parametric, p_permutation, CI_lower, CI_upper, N, effect_size_category

### Column Naming Conventions

- `UID` - Participant unique identifier (format: P### with leading zeros)
- `test` - Test session identifier (T1, T2, T3, T4)
- `SD_confidence` - Standard deviation of confidence ratings within person x test
- `SD_accuracy` - Standard deviation of accuracy responses within person x test
- `N_items` - Number of items used to compute SD (must be >= 10)
- `r` - Pearson correlation coefficient
- `p_parametric` - Parametric p-value (Pearson test)
- `p_permutation` - Permutation-based p-value (10,000 resamples)
- `CI_lower` / `CI_upper` - 95% confidence interval bounds for r

---

## Cross-RQ Dependencies

**Dependency Type:** RAW Data Only (No Dependencies)

**This RQ uses:** Only data/cache/dfData.csv (project-level data source)

**No dependencies on other RQs:** Can be executed independently

**Execution order:** Flexible (no cross-RQ constraints)

**Data Sources:**
- data/cache/dfData.csv - Item-level TC_* (confidence) and TQ_* (accuracy) columns

**Note:** Unlike most Chapter 6 RQs which depend on IRT-derived theta scores from Chapter 5 or RQ 6.1.1, this RQ uses raw item-level responses directly. Variability analysis requires item-level dispersion, not aggregate ability estimates.

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

#### Step 1: Compute Within-Person Confidence Variability

**Analysis Tool:** (determined by rq_tools - likely pandas groupby + std)
**Validation Tool:** (determined by rq_tools - likely validate_dataframe_structure + validate_numeric_range)

**What Validation Checks:**
- Output file exists (data/step01_sd_confidence.csv)
- Expected column count (4 columns: UID, test, SD_confidence, N_items)
- Expected row count (380-400 rows)
- SD_confidence in [0, 0.5] (valid range for binary/Likert SD)
- N_items >= 10 (minimum for stable SD estimate)
- No NaN values in SD_confidence or N_items
- No duplicate UID x test combinations

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "SD_confidence contains NaN values")
- Log failure to logs/step01_compute_sd_confidence.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked by master to diagnose root cause

---

#### Step 2: Compute Within-Person Accuracy Variability

**Analysis Tool:** (determined by rq_tools - likely pandas groupby + std)
**Validation Tool:** (determined by rq_tools - likely validate_dataframe_structure + validate_numeric_range)

**What Validation Checks:**
- Output file exists (data/step02_sd_accuracy.csv)
- Expected column count (4 columns: UID, test, SD_accuracy, N_items)
- Expected row count (380-400 rows)
- SD_accuracy in [0, 0.5] (valid range for binary SD)
- N_items >= 10 (minimum for stable SD estimate)
- No NaN values in SD_accuracy or N_items
- No duplicate UID x test combinations

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "SD_accuracy outside valid range")
- Log failure to logs/step02_compute_sd_accuracy.log
- Quit script immediately (do NOT proceed to Step 3)
- g_debug invoked to diagnose root cause

---

#### Step 3: Correlate Confidence Variability vs Accuracy Variability

**Analysis Tool:** (determined by rq_tools - likely scipy.stats.pearsonr + custom permutation test)
**Validation Tool:** (determined by rq_tools - likely validate_correlation_test_d068)

**What Validation Checks:**
- Output file exists (data/step03_correlation.csv)
- Expected row count (1 row - single correlation result)
- Expected column count (7 columns)
- r in [-1, 1] (correlation coefficient bounds)
- Both p-values in [0, 1] (p-value bounds)
- CI_lower <= r <= CI_upper (confidence interval consistency)
- N >= 300 (sufficient observations for correlation)
- effect_size_category in {"strong", "moderate", "weak"} (valid categories)
- Dual p-values present (Decision D068 compliance)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Missing permutation p-value - Decision D068 violation")
- Log failure to logs/step03_correlate_variability.log
- Quit script immediately (do NOT proceed to Step 4)
- g_debug invoked to diagnose root cause

---

#### Step 4: Prepare Scatterplot Data

**Analysis Tool:** (determined by rq_tools - likely pandas operations + linear regression)
**Validation Tool:** (determined by rq_tools - likely validate_plot_data_completeness + validate_numeric_range)

**What Validation Checks:**
- Both output files exist (scatterplot data + regression line)
- Scatterplot data: 380-400 rows, 4 columns
- Regression line: 100 rows, 2 columns
- SD_confidence in [0, 0.5] (both files)
- SD_accuracy in [0, 0.5] (scatterplot data)
- No NaN values in any column
- No duplicate UID x test combinations (scatterplot data)
- Regression line x values sorted ascending

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Regression line contains NaN values")
- Log failure to logs/step04_prepare_scatterplot_data.log
- Quit script immediately
- g_debug invoked to diagnose root cause

---

## Summary

**Total Steps:** 4

**Estimated Runtime:** Low (<10 minutes total)

**Cross-RQ Dependencies:** None (RAW data only from dfData.csv)

**Primary Outputs:**
- data/step01_sd_confidence.csv (within-person confidence variability)
- data/step02_sd_accuracy.csv (within-person accuracy variability)
- data/step03_correlation.csv (Pearson r with dual p-values)
- data/step04_variability_scatterplot_data.csv (plot data - observed points)
- data/step04_variability_regression_line.csv (plot data - regression line)

**Validation Coverage:** 100% (all 4 steps have validation requirements)

**Key Statistical Tests:**
- Pearson correlation (parametric) with 95% CI
- Permutation test (non-parametric) with 10,000 resamples
- Effect size interpretation (strong/moderate/weak)

**Decision Compliance:**
- D068: Dual p-value reporting (parametric + permutation) for correlation test

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent
