# Analysis Plan for RQ 6.2.2: Over-Underconfidence Trajectory

**Created by:** rq_planner agent
**Date:** 2025-12-06
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This RQ examines whether overconfidence emerges as memories fade over the 6-day retention interval. Using calibration scores from RQ 6.2.1 (N=400 observations: 100 participants x 4 test sessions), we classify each observation as overconfident (Calibration > 0, confidence exceeds accuracy), underconfident (Calibration < 0), or calibrated (Calibration approximately 0). The primary analysis tests whether the proportion of overconfident observations increases from Day 0 to Day 6, indicating that confidence lags behind accuracy decline.

This is a DERIVED data analysis (depends on RQ 6.2.1 calibration scores). The workflow involves 5 analysis steps:
1. Load calibration data from RQ 6.2.1
2. Classify observations by calibration sign
3. Compute proportion overconfident per timepoint
4. Trend test (logistic regression of overconfidence ~ Time)
5. Prepare plot data for trajectory visualization

**Estimated Runtime:** Low (~5 minutes total - all descriptive/inferential statistics, no model calibration)

---

## Analysis Plan

### Step 0: Load Calibration Data

**Dependencies:** RQ 6.2.1 must be complete (requires calibration scores)
**Complexity:** Low (<1 minute - data loading only)

**Input:**

**File:** results/ch6/6.2.1/data/step02_calibration_scores.csv
**Source:** RQ 6.2.1 Step 2 (merged accuracy + confidence theta with computed calibration)
**Format:** CSV with columns:
  - `UID` (string, participant identifier, format: P### with leading zeros)
  - `test` (string, test session identifier: T1, T2, T3, T4)
  - `theta_accuracy` (float, accuracy ability estimate from Ch5 5.1.1)
  - `theta_confidence` (float, confidence ability estimate from 6.1.1)
  - `Calibration` (float, difference score: theta_confidence - theta_accuracy, z-standardized)
  - `SE_accuracy` (float, standard error of theta_accuracy)
  - `SE_confidence` (float, standard error of theta_confidence)
**Expected Rows:** 400 (100 participants x 4 tests)
**Expected Columns:** 7

**Processing:**
- Load CSV using pandas.read_csv
- Validate expected structure (400 rows, 7 columns)
- Check for missing values in Calibration column (should be zero NaN)
- Verify UID and test combinations match expected pattern

**Output:**

**File:** data/step00_calibration_loaded.csv
**Format:** Identical to input (copy for lineage tracking)
**Columns:** Same as input
**Expected Rows:** 400

**Validation Requirement:**
Validation tools MUST be used after data loading. Specific validation tools determined by rq_tools based on data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_calibration_loaded.csv exists (exact path)
- Expected rows: 400 (100 participants x 4 tests)
- Expected columns: 7 (UID, test, theta_accuracy, theta_confidence, Calibration, SE_accuracy, SE_confidence)
- Data types: UID (object), test (object), theta_* (float64), Calibration (float64), SE_* (float64)

*Value Ranges:*
- theta_accuracy in [-3, 3] (typical IRT ability range)
- theta_confidence in [-3, 3]
- Calibration in [-6, 6] (difference of two z-scores, typically within +/-3 SD)
- SE_accuracy in [0.1, 1.0] (standard error bounds)
- SE_confidence in [0.1, 1.0]
- test in {T1, T2, T3, T4} (categorical)

*Data Quality:*
- No NaN values tolerated in Calibration column (all observations must have valid calibration scores)
- Expected N: Exactly 400 rows (no more, no less)
- No duplicate UID x test combinations (each participant-test combination unique)
- Distribution check: Calibration approximately normal (z-standardized difference)

*Log Validation:*
- Required pattern: "Loaded calibration data: 400 rows, 7 columns"
- Required pattern: "No missing values in Calibration column"
- Forbidden patterns: "ERROR", "NaN values detected in Calibration", "Duplicate UID-test combinations"
- Acceptable warnings: None expected for data loading step

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 400 rows, found 387")
- Log failure to logs/step00_load_calibration_data.log
- Quit script immediately (do NOT proceed to Step 1)
- Check RQ 6.2.1 completion status (dependency might have failed)

---

### Step 1: Classify Observations by Calibration Sign

**Dependencies:** Step 0 (requires loaded calibration data)
**Complexity:** Low (<1 minute - simple classification logic)

**Input:**

**File:** data/step00_calibration_loaded.csv
**Source:** Step 0 output
**Required Columns:** UID, test, Calibration

**Processing:**
- Create classification variable based on Calibration sign:
  - `Overconfident`: Calibration > epsilon (confidence exceeds accuracy)
  - `Underconfident`: Calibration < -epsilon (accuracy exceeds confidence)
  - `Calibrated`: |Calibration| <= epsilon (well-calibrated)
- Epsilon threshold: 0.1 SD units (scientifically meaningful difference)
- Add classification column to DataFrame

**Output:**

**File:** data/step01_calibration_classified.csv
**Format:** CSV, same structure as input + classification column
**Columns:**
  - All columns from step00_calibration_loaded.csv (UID, test, theta_accuracy, theta_confidence, Calibration, SE_accuracy, SE_confidence)
  - `Classification` (string, categorical: "Overconfident", "Underconfident", "Calibrated")
**Expected Rows:** 400

**Validation Requirement:**
Validation tools MUST be used after classification. Specific validation tools determined by rq_tools based on classification completeness.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_calibration_classified.csv exists (exact path)
- Expected rows: 400 (same as input)
- Expected columns: 8 (7 from input + Classification)
- Data types: Classification (object - categorical string)

*Value Ranges:*
- Classification in {"Overconfident", "Underconfident", "Calibrated"} (exactly these three categories, case-sensitive)

*Data Quality:*
- No NaN values in Classification column (all 400 observations must be classified)
- Expected N: Exactly 400 rows
- All three categories present (at least 1 observation in each category expected given N=400)
- Distribution check: Proportion Overconfident + Underconfident + Calibrated = 1.0 (within rounding error)

*Log Validation:*
- Required pattern: "Classification complete: 400 observations classified"
- Required pattern: "Overconfident: [N] ([%]), Underconfident: [N] ([%]), Calibrated: [N] ([%])"
- Forbidden patterns: "ERROR", "NaN in Classification", "Unrecognized category"
- Acceptable warnings: None expected for classification step

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Classification column contains NaN values")
- Log failure to logs/step01_classify_observations.log
- Quit script immediately (do NOT proceed to Step 2)

---

### Step 2: Compute Proportion Overconfident Per Timepoint

**Dependencies:** Step 1 (requires classified observations)
**Complexity:** Low (<1 minute - groupby aggregation)

**Input:**

**File:** data/step01_calibration_classified.csv
**Source:** Step 1 output
**Required Columns:** test, Classification

**Processing:**
- Group by test (T1, T2, T3, T4)
- For each test, compute:
  - N_total: Total observations per test (should be 100)
  - N_overconfident: Count of "Overconfident" observations
  - proportion_overconfident: N_overconfident / N_total
  - CI_lower, CI_upper: Binomial proportion 95% confidence intervals (Wilson score method)
- Create summary table with one row per test

**Output:**

**File:** data/step02_proportion_overconfident.csv
**Format:** CSV, one row per test session
**Columns:**
  - `test` (string: T1, T2, T3, T4)
  - `N_total` (int: total observations per test)
  - `N_overconfident` (int: count of overconfident observations)
  - `proportion_overconfident` (float: ratio, range [0, 1])
  - `CI_lower` (float: lower bound of 95% CI)
  - `CI_upper` (float: upper bound of 95% CI)
**Expected Rows:** 4 (one per test session)

**Validation Requirement:**
Validation tools MUST be used after proportion computation. Specific validation tools determined by rq_tools based on proportion calculation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_proportion_overconfident.csv exists (exact path)
- Expected rows: 4 (one per test T1, T2, T3, T4)
- Expected columns: 6 (test, N_total, N_overconfident, proportion_overconfident, CI_lower, CI_upper)
- Data types: test (object), N_total (int64), N_overconfident (int64), proportion_overconfident (float64), CI_* (float64)

*Value Ranges:*
- N_total = 100 for all rows (exactly 100 participants per test)
- N_overconfident in [0, 100] (count, must be integer)
- proportion_overconfident in [0, 1] (ratio)
- CI_lower in [0, 1], CI_upper in [0, 1] (probability bounds)
- CI_lower < proportion_overconfident < CI_upper (confidence interval must contain point estimate)

*Data Quality:*
- No NaN values tolerated (all 4 tests must have valid proportions)
- Expected N: Exactly 4 rows (one per test, no duplicates)
- test values must be {T1, T2, T3, T4} (complete set, no extras)
- Consistency check: N_overconfident / N_total = proportion_overconfident (within rounding error)

*Log Validation:*
- Required pattern: "Proportion overconfident computed: 4 timepoints"
- Required pattern: "T1: [proportion] ([CI_lower, CI_upper])" (repeat for T2, T3, T4)
- Forbidden patterns: "ERROR", "NaN in proportions", "Division by zero"
- Acceptable warnings: None expected for proportion computation

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "N_total != 100 for test T2")
- Log failure to logs/step02_compute_proportions.log
- Quit script immediately (do NOT proceed to Step 3)

---

### Step 3: Trend Test (Logistic Regression)

**Dependencies:** Step 2 (requires proportion data)
**Complexity:** Low (<1 minute - simple logistic regression)

**Input:**

**File 1:** data/step01_calibration_classified.csv
**Source:** Step 1 output (observation-level data for regression)
**Required Columns:** test, Classification

**File 2:** data/step02_proportion_overconfident.csv
**Source:** Step 2 output (descriptive summary for context)

**Processing:**
- Create binary outcome variable: overconfident_binary (1 if Classification == "Overconfident", else 0)
- Create ordinal time predictor: time_ordinal (T1=0, T2=1, T3=3, T4=6, nominal days)
- Fit logistic regression: overconfident_binary ~ time_ordinal
- Extract slope (log-odds per day), SE, z-statistic, p-value
- Compute odds ratio: exp(slope) with 95% CI
- Test hypothesis: slope > 0 (overconfidence increases over time)

**Output:**

**File:** data/step03_trend_test.csv
**Format:** CSV, one row (single model summary)
**Columns:**
  - `term` (string: "Intercept", "time_ordinal")
  - `estimate` (float: coefficient in log-odds units)
  - `SE` (float: standard error of estimate)
  - `z` (float: z-statistic)
  - `p_value` (float: two-tailed p-value)
  - `OR` (float: odds ratio = exp(estimate) for time_ordinal only)
  - `OR_CI_lower` (float: lower bound of 95% CI for OR)
  - `OR_CI_upper` (float: upper bound of 95% CI for OR)
**Expected Rows:** 2 (Intercept + time_ordinal)

**Validation Requirement:**
Validation tools MUST be used after trend test. Specific validation tools determined by rq_tools based on logistic regression requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_trend_test.csv exists (exact path)
- Expected rows: 2 (Intercept + time_ordinal terms)
- Expected columns: 8 (term, estimate, SE, z, p_value, OR, OR_CI_lower, OR_CI_upper)
- Data types: term (object), estimate (float64), SE (float64), z (float64), p_value (float64), OR (float64), OR_CI_* (float64)

*Value Ranges:*
- estimate: unrestricted (log-odds scale, can be positive or negative)
- SE > 0 (standard error must be positive)
- z: unrestricted (can be positive or negative)
- p_value in [0, 1] (probability)
- OR > 0 (odds ratio must be positive, OR=1 means no effect, OR>1 means increasing overconfidence)
- OR_CI_lower < OR < OR_CI_upper (confidence interval must contain point estimate)

*Data Quality:*
- No NaN values tolerated (both Intercept and time_ordinal must have valid estimates)
- Expected N: Exactly 2 rows (Intercept + time_ordinal)
- term values must be {"Intercept", "time_ordinal"} (exact match)
- Model convergence required (check logs for convergence message)

*Log Validation:*
- Required pattern: "Logistic regression converged: True"
- Required pattern: "Trend test complete: slope = [estimate], p = [p_value]"
- Required pattern: "Odds ratio per day: [OR] ([OR_CI_lower, OR_CI_upper])"
- Forbidden patterns: "ERROR", "Model did not converge", "Singular matrix"
- Acceptable warnings: "Algorithm converged in [N] iterations" (informational, not error)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Logistic regression did not converge")
- Log failure to logs/step03_trend_test.log
- Quit script immediately (do NOT proceed to Step 4)
- Report convergence diagnostics (iteration count, gradient norm, parameter stability)

---

### Step 4: Compute Mean Calibration Per Timepoint

**Dependencies:** Step 0 (requires calibration scores)
**Complexity:** Low (<1 minute - groupby aggregation)

**Input:**

**File:** data/step00_calibration_loaded.csv
**Source:** Step 0 output
**Required Columns:** test, Calibration

**Processing:**
- Group by test (T1, T2, T3, T4)
- For each test, compute:
  - mean_calibration: Mean(Calibration)
  - SD_calibration: Standard deviation of Calibration
  - SE_calibration: Standard error of mean (SD / sqrt(N))
  - N: Number of observations per test (should be 100)
  - CI_lower, CI_upper: 95% CI for mean (mean +/- 1.96 * SE)
- Create summary table with one row per test

**Output:**

**File:** data/step04_mean_calibration.csv
**Format:** CSV, one row per test session
**Columns:**
  - `test` (string: T1, T2, T3, T4)
  - `N` (int: observations per test)
  - `mean_calibration` (float: mean Calibration score)
  - `SD_calibration` (float: standard deviation)
  - `SE_calibration` (float: standard error of mean)
  - `CI_lower` (float: lower bound of 95% CI)
  - `CI_upper` (float: upper bound of 95% CI)
**Expected Rows:** 4 (one per test session)

**Validation Requirement:**
Validation tools MUST be used after mean computation. Specific validation tools determined by rq_tools based on summary statistics requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_mean_calibration.csv exists (exact path)
- Expected rows: 4 (one per test T1, T2, T3, T4)
- Expected columns: 7 (test, N, mean_calibration, SD_calibration, SE_calibration, CI_lower, CI_upper)
- Data types: test (object), N (int64), mean_calibration (float64), SD_calibration (float64), SE_calibration (float64), CI_* (float64)

*Value Ranges:*
- N = 100 for all rows (exactly 100 participants per test)
- mean_calibration in [-3, 3] (z-standardized difference, typically within +/-3 SD)
- SD_calibration > 0 (standard deviation must be positive)
- SE_calibration > 0 (standard error must be positive)
- SE_calibration = SD_calibration / sqrt(100) = SD_calibration / 10 (within rounding error)
- CI_lower < mean_calibration < CI_upper (confidence interval must contain mean)

*Data Quality:*
- No NaN values tolerated (all 4 tests must have valid means)
- Expected N: Exactly 4 rows (one per test, no duplicates)
- test values must be {T1, T2, T3, T4} (complete set, no extras)
- Consistency check: SE = SD / sqrt(N) (within rounding error)

*Log Validation:*
- Required pattern: "Mean calibration computed: 4 timepoints"
- Required pattern: "T1: mean = [mean_calibration] ([CI_lower, CI_upper])" (repeat for T2, T3, T4)
- Forbidden patterns: "ERROR", "NaN in mean_calibration", "Division by zero"
- Acceptable warnings: None expected for mean computation

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "N != 100 for test T3")
- Log failure to logs/step04_compute_mean_calibration.log
- Quit script immediately (do NOT proceed to Step 5)

---

### Step 5: Prepare Overconfidence Trajectory Plot Data

**Dependencies:** Steps 2, 4 (requires proportion and mean data)
**Complexity:** Low (<1 minute - data merging and formatting)

**Plot Description:** Dual-axis trajectory plot showing (1) proportion overconfident (left y-axis) and (2) mean calibration (right y-axis) across four test sessions. Expected pattern: both metrics should increase from Day 0 to Day 6 if overconfidence emerges over time.

**Required Data Sources:**
- data/step02_proportion_overconfident.csv (proportion trajectory)
- data/step04_mean_calibration.csv (mean calibration trajectory)

**Input:**

**File 1:** data/step02_proportion_overconfident.csv
**Source:** Step 2 output
**Required Columns:** test, proportion_overconfident, CI_lower, CI_upper

**File 2:** data/step04_mean_calibration.csv
**Source:** Step 4 output
**Required Columns:** test, mean_calibration, CI_lower, CI_upper

**Processing:**
- Merge File 1 and File 2 on test (T1, T2, T3, T4)
- Rename columns to avoid collision:
  - proportion_overconfident, prop_CI_lower, prop_CI_upper (from File 1)
  - mean_calibration, mean_CI_lower, mean_CI_upper (from File 2)
- Add time_numeric column: T1=0, T2=1, T3=3, T4=6 (nominal days for x-axis)
- Sort by time_numeric
- Save merged data as plot source CSV

**Output (Plot Source CSV):**

**File:** data/step05_overconfidence_trajectory_data.csv
**Format:** CSV, plot source data for dual-axis trajectory
**Columns:**
  - `test` (string: T1, T2, T3, T4)
  - `time_numeric` (int: 0, 1, 3, 6 - nominal days for x-axis)
  - `proportion_overconfident` (float: range [0, 1])
  - `prop_CI_lower` (float: lower 95% CI for proportion)
  - `prop_CI_upper` (float: upper 95% CI for proportion)
  - `mean_calibration` (float: mean Calibration score)
  - `mean_CI_lower` (float: lower 95% CI for mean)
  - `mean_CI_upper` (float: upper 95% CI for mean)
**Expected Rows:** 4 (one per test session)
**Note:** This CSV is read by rq_plots later. PNG output goes to plots/ when rq_plots runs.

**Validation Requirement:**
Validation tools MUST be used after plot data preparation. Specific validation tools determined by rq_tools based on plot data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_overconfidence_trajectory_data.csv exists (exact path)
- Expected rows: 4 (one per test T1, T2, T3, T4)
- Expected columns: 8 (test, time_numeric, proportion_overconfident, prop_CI_lower, prop_CI_upper, mean_calibration, mean_CI_lower, mean_CI_upper)
- Data types: test (object), time_numeric (int64), all metrics (float64)

*Value Ranges:*
- time_numeric in {0, 1, 3, 6} (nominal days, must be exact match)
- proportion_overconfident in [0, 1] (ratio)
- prop_CI_lower in [0, 1], prop_CI_upper in [0, 1]
- prop_CI_lower < proportion_overconfident < prop_CI_upper (CI contains point estimate)
- mean_calibration in [-3, 3] (z-standardized difference)
- mean_CI_lower < mean_calibration < mean_CI_upper (CI contains mean)

*Data Quality:*
- No NaN values tolerated (all cells must have valid values)
- Expected N: Exactly 4 rows (no more, no less)
- test values must be {T1, T2, T3, T4} (complete set, sorted by time_numeric)
- Merge completeness: All 4 tests from both input files present (inner join should retain all rows)

*Log Validation:*
- Required pattern: "Plot data preparation complete: 4 rows created"
- Required pattern: "Merge successful: 4 tests matched across proportion and mean files"
- Forbidden patterns: "ERROR", "NaN values detected", "Merge lost rows"
- Acceptable warnings: None expected for plot data preparation

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 4 rows, found 3 after merge")
- Log failure to logs/step05_prepare_plot_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- Report merge diagnostics (which tests missing, which files incomplete)

**Plotting Function (rq_plots will call):** Dual-axis trajectory plot
- rq_plots agent maps this description to appropriate plotting function
- Plot reads data/step05_overconfidence_trajectory_data.csv (created by this step)
- No data aggregation in rq_plots (visualization only per Option B)
- PNG output saved to plots/ folder by rq_plots

---

## Expected Data Formats

### Data Transformation Overview

This RQ performs three types of transformations:
1. **Classification** (Step 1): Continuous Calibration score -> categorical Classification variable
2. **Aggregation** (Steps 2, 4): Observation-level data -> timepoint-level summaries
3. **Merging** (Step 5): Combine proportion and mean summaries for plotting

All transformations preserve observation count (400 rows in Steps 0-1, 4 rows in Steps 2-5).

### Column Naming Conventions

Per names.md (from RQ 5.1 conventions):
- `UID`: Participant identifier (format P### with leading zeros)
- `test`: Test session identifier (T1, T2, T3, T4)
- `Classification`: Categorical variable ("Overconfident", "Underconfident", "Calibrated")
- `proportion_overconfident`: Ratio in [0, 1] range (not percentage)
- `CI_lower`, `CI_upper`: Confidence interval bounds (Wilson score for proportions, normal approximation for means)

### Data Type Constraints

- `UID`: object (string, case-sensitive)
- `test`: object (string, categorical: T1, T2, T3, T4)
- `time_numeric`: int64 (0, 1, 3, 6 - ordinal, not continuous)
- `Classification`: object (string, categorical: "Overconfident", "Underconfident", "Calibrated")
- `Calibration`: float64 (z-standardized difference, approximately N(0,1) distributed)
- `proportion_overconfident`: float64 (range [0, 1])
- `mean_calibration`: float64 (range typically [-3, 3])
- All `CI_*`: float64 (confidence interval bounds)
- All `N_*`: int64 (counts, non-negative integers)
- All `SE_*`: float64 (standard errors, positive)

---

## Cross-RQ Dependencies

### Dependency Type 2: DERIVED Data from Other RQs (Dependencies Exist)

**This RQ requires outputs from:**

- **RQ 6.2.1** (Calibration Over Time - Calibration Score Computation)
  - File: results/ch6/6.2.1/data/step02_calibration_scores.csv
  - Used in: Step 0 (load calibration data for classification and trend analysis)
  - Rationale: RQ 6.2.1 computes calibration scores (theta_confidence - theta_accuracy) by merging omnibus accuracy (Ch5 5.1.1) and omnibus confidence (6.1.1) theta estimates. This RQ analyzes the directionality and trajectory of those calibration scores.

**Execution Order Constraint:**
1. RQ 6.2.1 must complete Steps 0-2 first (provides calibration_scores.csv)
2. This RQ executes after RQ 6.2.1 (uses calibration scores)

**Data Source Boundaries (Per Specification 5.1.6):**
- **RAW data:** None (all analysis uses DERIVED calibration scores)
- **DERIVED data:** Calibration scores from RQ 6.2.1 (which itself derives from Ch5 5.1.1 and 6.1.1)
- **Scope:** This RQ does NOT re-compute calibration scores (uses RQ 6.2.1 outputs as input)

**Validation:**
- Step 0: Check results/ch6/6.2.1/data/step02_calibration_scores.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 0: Validate file has 400 rows, 7 columns (circuit breaker: STEP ERROR if dimensions wrong)
- If file missing -> quit with error -> user must execute RQ 6.2.1 first

**Reference:** Specification section 5.1.6 (Data Source Boundaries)

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
- g_code (Step 14 workflow) will generate stepNN_name.py scripts with validation function calls
- bash execution (Step 14 workflow) will run analysis -> validation -> error on validation failure

**Downstream Agent Requirements:**
- **rq_tools:** MUST specify validation tool for EVERY analysis step (no exceptions)
- **rq_analysis:** MUST embed validation tool call for EVERY analysis step (no exceptions)
- **g_code:** MUST generate code with validation function calls (no exceptions)
- **rq_inspect:** MUST verify validation ran successfully (checks logs/stepNN_name.log for validation output)

### Validation Requirements By Step

#### Step 0: Load Calibration Data

**Analysis Tool:** (determined by rq_tools - likely pandas.read_csv)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure)

**What Validation Checks:**
- File exists at expected path (results/ch6/6.2.1/data/step02_calibration_scores.csv)
- Expected column count (7 columns: UID, test, theta_accuracy, theta_confidence, Calibration, SE_accuracy, SE_confidence)
- Expected row count (400 rows: 100 participants x 4 tests)
- No NaN values in Calibration column (all observations must have valid calibration scores)
- UID and test combinations unique (no duplicates)
- Data types correct (UID: object, test: object, theta_*: float64, Calibration: float64, SE_*: float64)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Calibration column contains 12 NaN values")
- Log failure to logs/step00_load_calibration_data.log
- Quit script immediately (do NOT proceed to Step 1)
- Check RQ 6.2.1 status (dependency might have incomplete/corrupted output)

---

#### Step 1: Classify Observations by Calibration Sign

**Analysis Tool:** (determined by rq_tools - likely pandas DataFrame operations)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_data_columns + custom checks)

**What Validation Checks:**
- Classification column created and populated (no NaN values)
- All 400 observations classified (row count preserved)
- Only three categories present ("Overconfident", "Underconfident", "Calibrated" - case-sensitive)
- All three categories represented (at least 1 observation per category expected)
- Classification logic correct (Overconfident if Calibration > epsilon, Underconfident if Calibration < -epsilon, Calibrated otherwise)
- Proportions sum to 1.0 (within rounding error)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Classification column contains unrecognized category: 'overconfident' (lowercase)")
- Log failure to logs/step01_classify_observations.log
- Quit script immediately (do NOT proceed to Step 2)

---

#### Step 2: Compute Proportion Overconfident Per Timepoint

**Analysis Tool:** (determined by rq_tools - likely pandas.groupby + binomial CI computation)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_probability_range)

**What Validation Checks:**
- Expected row count (4 rows: one per test T1, T2, T3, T4)
- N_total = 100 for all tests (complete data per timepoint)
- N_overconfident in [0, 100] (valid count range)
- proportion_overconfident in [0, 1] (valid probability range)
- CI bounds valid (CI_lower < proportion < CI_upper)
- No NaN values (all proportions computed successfully)
- Consistency check: N_overconfident / N_total = proportion_overconfident (within rounding error)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "N_total = 87 for test T3, expected 100")
- Log failure to logs/step02_compute_proportions.log
- Quit script immediately (do NOT proceed to Step 3)

---

#### Step 3: Trend Test (Logistic Regression)

**Analysis Tool:** (determined by rq_tools - likely statsmodels.api.Logit or sklearn.linear_model.LogisticRegression)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_model_convergence)

**What Validation Checks:**
- Model converged successfully (convergence flag = True)
- Expected row count (2 rows: Intercept + time_ordinal terms)
- No NaN parameters (all estimates, SEs, p-values valid)
- Standard errors positive (SE > 0)
- p-values in [0, 1] range
- Odds ratio > 0 (OR must be positive)
- CI bounds valid (OR_CI_lower < OR < OR_CI_upper)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Logistic regression did not converge after 100 iterations")
- Log failure to logs/step03_trend_test.log
- Quit script immediately (do NOT proceed to Step 4)
- Report convergence diagnostics (iteration count, gradient norm, log-likelihood)

---

#### Step 4: Compute Mean Calibration Per Timepoint

**Analysis Tool:** (determined by rq_tools - likely pandas.groupby + scipy.stats for CI)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_numeric_range)

**What Validation Checks:**
- Expected row count (4 rows: one per test T1, T2, T3, T4)
- N = 100 for all tests (complete data per timepoint)
- SD_calibration > 0 (standard deviation must be positive)
- SE_calibration > 0 (standard error must be positive)
- SE = SD / sqrt(N) consistency check (within rounding error)
- mean_calibration in [-3, 3] (scientifically reasonable range for z-scores)
- CI bounds valid (CI_lower < mean < CI_upper)
- No NaN values (all means computed successfully)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "SD_calibration = 0 for test T1, indicates zero variance")
- Log failure to logs/step04_compute_mean_calibration.log
- Quit script immediately (do NOT proceed to Step 5)

---

#### Step 5: Prepare Overconfidence Trajectory Plot Data

**Analysis Tool:** (determined by rq_tools - likely pandas.merge)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_plot_data_completeness)

**What Validation Checks:**
- Expected row count (4 rows: one per test after merge)
- All 4 tests present (T1, T2, T3, T4 - complete factorial design)
- No NaN values (all cells must have valid data)
- Merge successful (no rows lost, inner join should retain all 4 tests)
- Column naming correct (no collisions: prop_CI_* vs mean_CI_*)
- CI bounds valid (all lower < point estimate < upper)
- Data sorted by time_numeric (0, 1, 3, 6 in ascending order)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Merge lost 1 row, expected 4 but found 3")
- Log failure to logs/step05_prepare_plot_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- Report merge diagnostics (which tests missing from each input file)

---

## Summary

**Total Steps:** 6 (Step 0: load + Steps 1-5: analysis/preparation)
**Estimated Runtime:** Low (~5 minutes total - all descriptive/inferential statistics, no model calibration)
**Cross-RQ Dependencies:** RQ 6.2.1 (calibration scores)
**Primary Outputs:**
- data/step01_calibration_classified.csv (400 observations classified)
- data/step02_proportion_overconfident.csv (proportion trajectory, 4 timepoints)
- data/step03_trend_test.csv (logistic regression results)
- data/step04_mean_calibration.csv (mean calibration trajectory, 4 timepoints)
- data/step05_overconfidence_trajectory_data.csv (plot source CSV for rq_plots)
**Validation Coverage:** 100% (all 6 steps have validation requirements)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent for RQ 6.2.2
