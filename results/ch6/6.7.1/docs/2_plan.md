# Analysis Plan: RQ 6.7.1 - Initial Confidence Predicting Forgetting Rates

**Research Question:** 6.7.1
**Created:** 2025-12-06
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines whether high initial confidence at Day 0 (T1) predicts slower forgetting trajectories over a 6-day retention interval. The analysis tests the predictive validity of metacognitive judgments at encoding for subsequent memory dynamics.

**Pipeline:** DERIVED data analysis (correlation and regression)

**Steps:** 5 analysis steps

**Estimated Runtime:** Low (all steps involve data loading, merging, and statistical testing with no model calibration)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected and Bonferroni-corrected)

**Data Sources:**
- RQ 6.1.1: Day 0 confidence estimates (theta_confidence at T1)
- Ch5 RQ 5.1.4: Individual forgetting slopes (random slopes from accuracy LMM)

---

## Analysis Plan

### Step 1: Load Day 0 Confidence Data

**Dependencies:** None (first step - loads from RQ 6.1.1)
**Complexity:** Low (file read and filter operation)

**Purpose:** Extract Day 0 confidence estimates for all 100 participants from RQ 6.1.1

**Input:**

**File:** results/ch6/6.1.1/data/step03_theta_confidence.csv
**Source:** RQ 6.1.1 Step 3 (IRT calibration for confidence)
**Format:** CSV with columns:
  - `composite_ID` (string, format: UID_test, e.g., P001_T1)
  - `theta_confidence` (float, IRT ability estimate for confidence)
  - `se_confidence` (float, standard error of theta estimate)
  - `test` (string, test session: T1, T2, T3, T4)

**Expected Rows:** ~400 (100 participants x 4 tests)

**Filters:**
- Retain ONLY T1 (Day 0) rows
- Extract UID from composite_ID (format: UID_test -> UID)

**Processing:**

**Method:** Data filtering and transformation
1. Read results/ch6/6.1.1/data/step03_theta_confidence.csv
2. Filter to test == 'T1' (Day 0 baseline only)
3. Extract UID from composite_ID (split on underscore, take first part)
4. Rename theta_confidence -> Day0_confidence for clarity
5. Select columns: UID, Day0_confidence, se_confidence

**Output:**

**File:** data/step01_day0_confidence.csv
**Format:** CSV with columns:
  - `UID` (string, participant identifier, format: P### with leading zeros)
  - `Day0_confidence` (float, confidence theta at T1/Day 0)
  - `se_confidence` (float, standard error of confidence estimate)

**Expected Rows:** 100 (one per participant)

**Validation Requirement:**
Validation tools MUST be used after data loading and filtering. Specific validation tools determined by rq_tools based on data extraction requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_day0_confidence.csv exists (exact path)
- Expected rows: 100 (one per participant)
- Expected columns: 3 (UID, Day0_confidence, se_confidence)
- Data types: UID (object/string), Day0_confidence (float64), se_confidence (float64)

*Value Ranges:*
- Day0_confidence in [-3, 3] (typical IRT theta range)
- se_confidence in [0.1, 1.5] (below 0.1 = suspiciously precise, above 1.5 = unreliable)

*Data Quality:*
- No NaN values tolerated (all participants must have Day 0 confidence)
- Expected N: Exactly 100 rows (all participants present)
- No duplicate UIDs (each participant appears once)
- UID format check: P### pattern with leading zeros

*Log Validation:*
- Required pattern: "Loaded 100 Day 0 confidence estimates"
- Required pattern: "Filtered to T1 only: 100 rows retained"
- Forbidden patterns: "ERROR", "NaN values detected", "Missing participants"
- Acceptable warnings: None expected for simple filtering

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 100 rows, found 87")
- Log failure to logs/step01_load_day0_confidence.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose root cause (missing RQ 6.1.1 data, incomplete participants)

---

### Step 2: Load Forgetting Slopes Data

**Dependencies:** None (independent of Step 1 - loads from Ch5 5.1.4)
**Complexity:** Low (file read and column selection)

**Purpose:** Extract individual forgetting slopes from Ch5 5.1.4 random effects

**Input:**

**File:** results/ch5/5.1.4/data/step04_random_effects.csv
**Source:** Ch5 RQ 5.1.4 Step 4 (random effects extraction from accuracy LMM)
**Format:** CSV with columns:
  - `UID` (string, participant identifier)
  - `random_intercept` (float, individual baseline accuracy)
  - `random_slope` (float, individual forgetting rate)
  - `se_intercept` (float, standard error of intercept)
  - `se_slope` (float, standard error of slope)

**Expected Rows:** ~100 (one per participant)

**Processing:**

**Method:** Data loading and column selection
1. Read results/ch5/5.1.4/data/step04_random_effects.csv
2. Select columns: UID, random_slope, se_slope
3. Rename random_slope -> forgetting_slope for clarity
4. Sort by UID for consistent ordering

**Output:**

**File:** data/step02_forgetting_slopes.csv
**Format:** CSV with columns:
  - `UID` (string, participant identifier)
  - `forgetting_slope` (float, individual forgetting rate from accuracy LMM)
  - `se_slope` (float, standard error of forgetting slope)

**Expected Rows:** 100 (one per participant)

**Validation Requirement:**
Validation tools MUST be used after data loading. Specific validation tools determined by rq_tools based on data extraction requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_forgetting_slopes.csv exists (exact path)
- Expected rows: 100 (one per participant)
- Expected columns: 3 (UID, forgetting_slope, se_slope)
- Data types: UID (object/string), forgetting_slope (float64), se_slope (float64)

*Value Ranges:*
- forgetting_slope in [-0.5, 0.2] (negative = forgetting, positive = improvement unlikely but possible)
- se_slope in [0.01, 0.2] (below 0.01 = suspiciously precise, above 0.2 = very unreliable)

*Data Quality:*
- No NaN values tolerated (all participants must have forgetting slopes)
- Expected N: Exactly 100 rows (all participants present)
- No duplicate UIDs (each participant appears once)

*Log Validation:*
- Required pattern: "Loaded 100 forgetting slopes"
- Required pattern: "Data source: Ch5 RQ 5.1.4"
- Forbidden patterns: "ERROR", "NaN values detected", "Missing participants"
- Acceptable warnings: None expected for simple loading

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 100 rows, found 93")
- Log failure to logs/step02_load_forgetting_slopes.log
- Quit script immediately (do NOT proceed to Step 3)
- g_debug invoked to diagnose root cause (missing Ch5 5.1.4 data, incomplete participants)

---

### Step 3: Merge Confidence and Slopes Data

**Dependencies:** Steps 1 and 2 (requires both confidence and slopes data)
**Complexity:** Low (merge operation with validation)

**Purpose:** Create analysis-ready dataset combining Day 0 confidence with forgetting slopes

**Input:**

**File 1:** data/step01_day0_confidence.csv
**Source:** Step 1 output
**Format:** 100 rows x 3 columns (UID, Day0_confidence, se_confidence)

**File 2:** data/step02_forgetting_slopes.csv
**Source:** Step 2 output
**Format:** 100 rows x 3 columns (UID, forgetting_slope, se_slope)

**Processing:**

**Method:** Inner join on UID
1. Read data/step01_day0_confidence.csv
2. Read data/step02_forgetting_slopes.csv
3. Merge on UID (inner join - only participants with BOTH confidence and slopes)
4. Sort by UID for consistent ordering
5. Validate: All 100 participants matched (no missing data)

**Merge Logic:**
- **Key:** UID (must match exactly between files)
- **Type:** Inner join (only participants with both confidence and slopes)
- **Null handling:** If any participant missing from either file, raise error (validation failure)

**Output:**

**File:** data/step03_predictive_data.csv
**Format:** CSV with columns:
  - `UID` (string, participant identifier)
  - `Day0_confidence` (float, confidence theta at T1)
  - `se_confidence` (float, standard error of confidence)
  - `forgetting_slope` (float, individual forgetting rate)
  - `se_slope` (float, standard error of slope)

**Expected Rows:** 100 (all participants with both measures)

**Validation Requirement:**
Validation tools MUST be used after merge operation. Specific validation tools determined by rq_tools based on data merge requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_predictive_data.csv exists (exact path)
- Expected rows: 100 (all participants matched)
- Expected columns: 5 (UID, Day0_confidence, se_confidence, forgetting_slope, se_slope)
- Data types: UID (object/string), all others (float64)

*Value Ranges:*
- Day0_confidence in [-3, 3]
- se_confidence in [0.1, 1.5]
- forgetting_slope in [-0.5, 0.2]
- se_slope in [0.01, 0.2]

*Data Quality:*
- No NaN values tolerated (all columns must have valid data)
- Expected N: Exactly 100 rows (no data loss from merge)
- No duplicate UIDs (each participant appears once)
- All UIDs from Step 1 present in merged data (validate complete match)
- All UIDs from Step 2 present in merged data (validate complete match)

*Log Validation:*
- Required pattern: "Merged 100 participants successfully"
- Required pattern: "No data loss: 100 participants with both measures"
- Forbidden patterns: "ERROR", "NaN values detected", "Participants missing from merge"
- Acceptable warnings: None expected for complete merge

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Merge incomplete: 5 participants missing forgetting slopes")
- Log failure to logs/step03_merge_data.log
- Quit script immediately (do NOT proceed to Step 4)
- g_debug invoked to diagnose root cause (incomplete source data, UID mismatch)

---

### Step 4: Compute Correlation and Tertile Analysis

**Dependencies:** Step 3 (requires merged predictive data)
**Complexity:** Low (statistical tests with no model fitting)

**Purpose:** Test correlation between Day 0 confidence and forgetting slopes, plus tertile group comparison

**Input:**

**File:** data/step03_predictive_data.csv
**Source:** Step 3 output
**Format:** 100 rows x 5 columns (UID, Day0_confidence, se_confidence, forgetting_slope, se_slope)

**Processing:**

**Method:** Correlation analysis with dual p-values (Decision D068) and tertile group comparison

**1. Correlation Analysis:**
- Compute Pearson r between Day0_confidence and forgetting_slope
- Test directional hypothesis: High confidence predicts slower forgetting (positive correlation expected)
- Report dual p-values per Decision D068:
  - Uncorrected p-value (standard Pearson test)
  - Bonferroni-corrected p-value (conservative adjustment)
- Compute 95% confidence interval for r

**2. Tertile Analysis:**
- Create tertiles of Day0_confidence (Low/Med/High)
- Ensure balanced groups (each tertile ~33 participants)
- Compute mean forgetting_slope per tertile
- Test if High confidence tertile has slower (less negative) forgetting than Low tertile
- Report dual p-values per Decision D068

**3. Effect Size:**
- Compute Cohen's d for High vs Low tertile comparison
- Interpret effect direction (positive d = high confidence -> slower forgetting)

**Output:**

**File 1:** data/step04_correlation.csv
**Format:** CSV with columns:
  - `correlation_r` (float, Pearson correlation coefficient)
  - `CI_lower` (float, lower 95% confidence bound for r)
  - `CI_upper` (float, upper 95% confidence bound for r)
  - `p_uncorrected` (float, uncorrected p-value)
  - `p_bonferroni` (float, Bonferroni-corrected p-value per Decision D068)
  - `N` (int, sample size = 100)
  - `direction` (string, "positive" or "negative" or "null")

**Expected Rows:** 1 (single correlation result)

**File 2:** data/step04_tertile_analysis.csv
**Format:** CSV with columns:
  - `tertile` (string, "Low" / "Med" / "High")
  - `N` (int, participants per tertile)
  - `mean_Day0_confidence` (float, mean confidence per tertile)
  - `mean_forgetting_slope` (float, mean forgetting rate per tertile)
  - `se_forgetting_slope` (float, standard error of mean slope)

**Expected Rows:** 3 (one per tertile)

**File 3:** data/step04_tertile_test.csv
**Format:** CSV with columns:
  - `comparison` (string, "High vs Low")
  - `cohens_d` (float, effect size)
  - `p_uncorrected` (float, uncorrected t-test p-value)
  - `p_bonferroni` (float, Bonferroni-corrected p-value per Decision D068)
  - `interpretation` (string, effect direction description)

**Expected Rows:** 1 (High vs Low comparison)

**Validation Requirement:**
Validation tools MUST be used after correlation and tertile analysis. Specific validation tools determined by rq_tools based on statistical test requirements. Decision D068 validation function must verify dual p-value presence.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_correlation.csv exists: 1 row x 7 columns
- data/step04_tertile_analysis.csv exists: 3 rows x 5 columns
- data/step04_tertile_test.csv exists: 1 row x 5 columns

*Value Ranges:*
- correlation_r in [-1, 1] (Pearson correlation bounds)
- p_uncorrected in [0, 1] (p-value bounds)
- p_bonferroni in [0, 1] (corrected p-value)
- cohens_d unrestricted (but typically in [-2, 2] for reasonable effects)
- N = 100 (correlation sample size)
- Tertile N in [30, 35] (balanced groups, ~33 each)

*Data Quality:*
- No NaN values tolerated (all statistics must be computed)
- Expected N: Exactly 100 across all tertiles (sum of tertile Ns = 100)
- CI_upper > CI_lower for correlation (confidence interval validity)
- p_bonferroni >= p_uncorrected (correction never reduces p-value)

*Log Validation:*
- Required pattern: "Correlation computed: r = X.XX, p_uncorrected = X.XX, p_bonferroni = X.XX"
- Required pattern: "Tertile analysis complete: 3 groups created (Low/Med/High)"
- Required pattern: "Dual p-values reported per Decision D068"
- Forbidden patterns: "ERROR", "NaN in correlation", "Tertile imbalance"
- Acceptable warnings: "Bonferroni correction yields non-significant result" (informative, not error)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Correlation NaN - check data distribution")
- Log failure to logs/step04_compute_statistics.log
- Quit script immediately (do NOT proceed to Step 5)
- g_debug invoked to diagnose root cause (insufficient variance, outliers, data errors)

---

### Step 5: Prepare Plot Data (Confidence Predicts Forgetting)

**Dependencies:** Step 4 (requires tertile analysis results)
**Complexity:** Low (data aggregation for visualization)

**Purpose:** Create plot source CSV showing relationship between initial confidence and forgetting trajectories

**Input:**

**File 1:** data/step03_predictive_data.csv
**Source:** Step 3 output
**Format:** 100 rows x 5 columns (UID, Day0_confidence, forgetting_slope, SEs)

**File 2:** data/step04_tertile_analysis.csv
**Source:** Step 4 output
**Format:** 3 rows x 5 columns (tertile statistics)

**Processing:**

**Method:** Aggregate observed data for scatterplot with tertile overlays

**1. Scatterplot Data:**
- All 100 individual data points (Day0_confidence vs forgetting_slope)
- Add tertile labels (Low/Med/High) to each participant

**2. Tertile Summary Lines:**
- Mean Day0_confidence per tertile (x-coordinate)
- Mean forgetting_slope per tertile (y-coordinate)
- SE bars for forgetting_slope (error bars)

**Plot Description:**
Scatterplot showing relationship between Day 0 confidence (x-axis) and forgetting slope (y-axis), with tertile means overlaid as summary points with error bars.

**Output:**

**File:** data/step05_confidence_predicts_forgetting_data.csv
**Format:** CSV with columns:
  - `UID` (string, participant identifier)
  - `Day0_confidence` (float, x-axis value)
  - `forgetting_slope` (float, y-axis value)
  - `tertile` (string, "Low" / "Med" / "High" for color coding)
  - `is_mean` (bool, True for tertile means, False for individual points)
  - `se_slope` (float, error bar size for tertile means, NaN for individuals)

**Expected Rows:** 103 (100 individuals + 3 tertile means)

**Plotting Function (rq_plots will call):** Scatterplot with tertile overlay
- rq_plots agent maps to appropriate plotting function
- X-axis: Day0_confidence (theta scale, -3 to 3)
- Y-axis: forgetting_slope (rate scale, -0.5 to 0.2)
- Points: Individual participants (scatter)
- Overlays: Tertile means with error bars (distinguishable markers)
- PNG output saved to plots/ folder by rq_plots

**Validation Requirement:**
Validation tools MUST be used after plot data preparation. Specific validation tools determined by rq_tools based on plot data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_confidence_predicts_forgetting_data.csv exists (exact path)
- Expected rows: 103 (100 individuals + 3 tertile means)
- Expected columns: 6 (UID, Day0_confidence, forgetting_slope, tertile, is_mean, se_slope)
- Data types: UID (object), Day0_confidence (float64), forgetting_slope (float64), tertile (object), is_mean (bool), se_slope (float64)

*Value Ranges:*
- Day0_confidence in [-3, 3]
- forgetting_slope in [-0.5, 0.2]
- tertile in {"Low", "Med", "High"}
- is_mean: 3 True values (tertile means), 100 False values (individuals)
- se_slope: 3 non-NaN values (tertile means), 100 NaN values (individuals)

*Data Quality:*
- No NaN in Day0_confidence or forgetting_slope (all individuals + means have valid data)
- Expected N: Exactly 103 rows (100 + 3)
- Exactly 3 rows with is_mean == True (one per tertile)
- Exactly 100 rows with is_mean == False (all individuals)
- All tertiles represented: "Low", "Med", "High" each appear

*Log Validation:*
- Required pattern: "Plot data preparation complete: 103 rows created (100 individuals + 3 tertile means)"
- Required pattern: "All tertiles represented: Low, Med, High"
- Forbidden patterns: "ERROR", "NaN values in coordinates", "Missing tertile"
- Acceptable warnings: None expected for plot data preparation

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 103 rows, found 100 - tertile means missing")
- Log failure to logs/step05_prepare_plot_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- g_debug invoked to diagnose root cause

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 1 Transformation:**
- Input: results/ch6/6.1.1/data/step03_theta_confidence.csv (400 rows - all tests)
- Filter: test == 'T1' (Day 0 only)
- Parse: composite_ID -> UID (split on underscore)
- Output: data/step01_day0_confidence.csv (100 rows - one per participant)

**Step 2 Transformation:**
- Input: results/ch5/5.1.4/data/step04_random_effects.csv (100 rows)
- Select: UID, random_slope, se_slope
- Rename: random_slope -> forgetting_slope
- Output: data/step02_forgetting_slopes.csv (100 rows)

**Step 3 Transformation:**
- Input: Two files (100 rows each)
- Merge: Inner join on UID
- Validate: No data loss (100 rows retained)
- Output: data/step03_predictive_data.csv (100 rows x 5 columns)

**Step 4 Transformation:**
- Input: data/step03_predictive_data.csv (100 rows)
- Compute: Pearson correlation + tertile groups
- Output: 3 files (correlation, tertile stats, tertile test)

**Step 5 Transformation:**
- Input: data/step03_predictive_data.csv + data/step04_tertile_analysis.csv
- Combine: Individual points + tertile means
- Output: data/step05_confidence_predicts_forgetting_data.csv (103 rows)

### Column Naming Conventions

Per names.md established conventions:

**Identifier Columns:**
- `UID` - Participant identifier (format: P### with leading zeros)
- `composite_ID` - Combined UID_test (format: P###_T#)
- `test` - Test session (T1, T2, T3, T4)

**Statistical Columns:**
- `Day0_confidence` - Confidence theta at baseline (derived name, descriptive)
- `forgetting_slope` - Individual forgetting rate (derived name, descriptive)
- `se_confidence` - Standard error of confidence estimate (lowercase se prefix)
- `se_slope` - Standard error of slope estimate (lowercase se prefix)
- `correlation_r` - Pearson correlation coefficient (lowercase r suffix)
- `p_uncorrected` - Uncorrected p-value (Decision D068 dual reporting)
- `p_bonferroni` - Bonferroni-corrected p-value (Decision D068 dual reporting)
- `cohens_d` - Effect size estimate (lowercase cohen, underscore separator)

**Plot Columns:**
- `tertile` - Categorical grouping (Low/Med/High)
- `is_mean` - Boolean flag for summary vs individual points
- `CI_lower` - Lower 95% confidence bound
- `CI_upper` - Upper 95% confidence bound

### Data Type Constraints

**Participant Identifiers:**
- `UID` - String, non-nullable, format: P### (e.g., P001, P100)
- `composite_ID` - String, non-nullable, format: UID_test (e.g., P001_T1)

**Theta Estimates:**
- `Day0_confidence` - Float64, non-nullable, range: [-3, 3] (IRT theta scale)
- `forgetting_slope` - Float64, non-nullable, range: [-0.5, 0.2] (negative = forgetting)

**Standard Errors:**
- `se_confidence` - Float64, non-nullable, range: [0.1, 1.5]
- `se_slope` - Float64, nullable for individuals (NaN), non-nullable for tertile means

**Statistical Results:**
- `correlation_r` - Float64, range: [-1, 1]
- `p_uncorrected` - Float64, range: [0, 1]
- `p_bonferroni` - Float64, range: [0, 1], >= p_uncorrected
- `cohens_d` - Float64, unrestricted range

**Categorical Variables:**
- `tertile` - String, values: {"Low", "Med", "High"}
- `direction` - String, values: {"positive", "negative", "null"}
- `is_mean` - Boolean, values: {True, False}

---

## Cross-RQ Dependencies

**Dependency Type:** DERIVED Data from Other RQs (Dependencies Exist)

**This RQ requires outputs from:**

**RQ 6.1.1** (Confidence Functional Form - Day 0 confidence estimates)
- **File:** results/ch6/6.1.1/data/step03_theta_confidence.csv
- **Used in:** Step 1 (extract Day 0 confidence for all participants)
- **Rationale:** RQ 6.1.1 establishes IRT-based confidence estimates. This RQ uses Day 0 (T1) confidence as predictor variable for forgetting trajectories.
- **Required Status:** RQ 6.1.1 must complete Step 3 (IRT calibration complete)

**Ch5 RQ 5.1.4** (Accuracy ICC Decomposition - individual forgetting slopes)
- **File:** results/ch5/5.1.4/data/step04_random_effects.csv
- **Used in:** Step 2 (extract individual forgetting slopes for all participants)
- **Rationale:** RQ 5.1.4 decomposes variance in accuracy trajectories into between-person and within-person components. This RQ uses individual random slopes (forgetting rates) as outcome variable to test if Day 0 confidence predicts subsequent memory dynamics.
- **Required Status:** Ch5 RQ 5.1.4 must complete Step 4 (random effects extraction from LMM)

**Execution Order Constraint:**
1. RQ 6.1.1 must complete first (provides confidence estimates)
2. Ch5 RQ 5.1.4 must complete second (provides forgetting slopes)
3. This RQ executes third (uses both outputs)

**Data Source Boundaries:**
- **RAW data:** None (this RQ uses ONLY derived data from other RQs)
- **DERIVED data:**
  - RQ 6.1.1: Day 0 confidence theta scores
  - Ch5 5.1.4: Individual random slopes from accuracy LMM
- **Scope:** This RQ does NOT re-calibrate IRT models or re-fit LMMs (uses existing estimates as inputs)

**Validation:**
- Step 1: Check results/ch6/6.1.1/data/step03_theta_confidence.csv exists (circuit breaker: FILE_MISSING if absent)
- Step 2: Check results/ch5/5.1.4/data/step04_random_effects.csv exists (circuit breaker: FILE_MISSING if absent)
- If either file missing -> quit with error -> user must execute dependency RQs first

**Cross-RQ Validation Notes:**
- This RQ assumes both dependency RQs completed successfully (status = success in their respective status.yaml files)
- File existence checks are MINIMUM validation - additional checks verify row counts and data completeness
- If dependency RQ outputs exist but have data quality issues (missing participants, NaN values), this RQ will detect during merge (Step 3) and fail validation

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

#### Step 1: Load Day 0 Confidence Data

**Analysis Tool:** (determined by rq_tools - likely pandas read_csv + filtering)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_data_format + validate_numeric_range)

**What Validation Checks:**
- Output file exists (data/step01_day0_confidence.csv)
- Expected column count (3 columns: UID, Day0_confidence, se_confidence)
- Expected row count (100 rows: one per participant)
- No NaN values in any column
- Day0_confidence range: [-3, 3]
- se_confidence range: [0.1, 1.5]
- UID format correct (P### pattern)
- No duplicate UIDs

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 100 rows, found 87 - check RQ 6.1.1 completion")
- Log failure to logs/step01_load_day0_confidence.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose root cause

---

#### Step 2: Load Forgetting Slopes Data

**Analysis Tool:** (determined by rq_tools - likely pandas read_csv + column selection)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_data_format + validate_numeric_range)

**What Validation Checks:**
- Output file exists (data/step02_forgetting_slopes.csv)
- Expected column count (3 columns: UID, forgetting_slope, se_slope)
- Expected row count (100 rows: one per participant)
- No NaN values in any column
- forgetting_slope range: [-0.5, 0.2]
- se_slope range: [0.01, 0.2]
- No duplicate UIDs

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 100 rows, found 93 - check Ch5 5.1.4 completion")
- Log failure to logs/step02_load_forgetting_slopes.log
- Quit script immediately (do NOT proceed to Step 3)
- g_debug invoked to diagnose root cause

---

#### Step 3: Merge Confidence and Slopes Data

**Analysis Tool:** (determined by rq_tools - likely pandas merge)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_data_format + check_missing_data)

**What Validation Checks:**
- Output file exists (data/step03_predictive_data.csv)
- Expected column count (5 columns)
- Expected row count (100 rows - no data loss from merge)
- No NaN values in any column
- All UIDs from Step 1 present in merged data
- All UIDs from Step 2 present in merged data
- Value ranges maintained from source data

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Merge incomplete: 5 participants missing forgetting slopes")
- Log failure to logs/step03_merge_data.log
- Quit script immediately (do NOT proceed to Step 4)
- g_debug invoked to diagnose root cause

---

#### Step 4: Compute Correlation and Tertile Analysis

**Analysis Tool:** (determined by rq_tools - likely scipy.stats.pearsonr + pandas groupby)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_correlation_test_d068 + validate_numeric_range)

**What Validation Checks:**
- Output files exist (3 files: correlation, tertile analysis, tertile test)
- Decision D068 compliance: Dual p-values present (p_uncorrected + p_bonferroni)
- Correlation coefficient in [-1, 1]
- p-values in [0, 1]
- p_bonferroni >= p_uncorrected (correction never reduces p-value)
- Tertile balance: each tertile has ~33 participants (range: 30-35)
- Sum of tertile Ns = 100
- CI_upper > CI_lower for correlation

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Correlation NaN - insufficient variance in predictors")
- Log failure to logs/step04_compute_statistics.log
- Quit script immediately (do NOT proceed to Step 5)
- g_debug invoked to diagnose root cause

---

#### Step 5: Prepare Plot Data

**Analysis Tool:** (determined by rq_tools - likely pandas concat + filtering)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_plot_data_completeness + validate_dataframe_structure)

**What Validation Checks:**
- Output file exists (data/step05_confidence_predicts_forgetting_data.csv)
- Expected row count (103 rows: 100 individuals + 3 tertile means)
- Expected column count (6 columns)
- Exactly 3 rows with is_mean == True
- Exactly 100 rows with is_mean == False
- All tertiles represented: "Low", "Med", "High"
- No NaN in Day0_confidence or forgetting_slope
- se_slope non-NaN for tertile means, NaN for individuals

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 103 rows, found 100 - tertile means missing")
- Log failure to logs/step05_prepare_plot_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- g_debug invoked to diagnose root cause

---

## Summary

**Total Steps:** 5 (Steps 1-5, no Step 0 - all derived data)

**Estimated Runtime:** Low (10-15 minutes total - no model calibration, only data loading and statistical tests)

**Cross-RQ Dependencies:**
- RQ 6.1.1 (Day 0 confidence estimates)
- Ch5 RQ 5.1.4 (individual forgetting slopes)

**Primary Outputs:**
- data/step03_predictive_data.csv (merged analysis dataset)
- data/step04_correlation.csv (correlation results with dual p-values)
- data/step04_tertile_analysis.csv (tertile group statistics)
- data/step04_tertile_test.csv (High vs Low comparison with dual p-values)
- data/step05_confidence_predicts_forgetting_data.csv (plot source data)

**Validation Coverage:** 100% (all 5 steps have validation requirements)

**Decision D068 Application:**
- Step 4: Correlation test reports dual p-values (uncorrected + Bonferroni)
- Step 4: Tertile comparison reports dual p-values (uncorrected + Bonferroni)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent for RQ 6.7.1
