# Analysis Plan: RQ 6.7.3 - Calibration Predicts Trajectory Stability

**Research Question:** 6.7.3
**Created:** 2025-12-06
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines whether metacognitive skill (Day 0 calibration quality) predicts forgetting trajectory stability. The analysis uses DERIVED data from two source RQs: calibration scores from RQ 6.2.1 (Day 0 confidence-accuracy alignment) and trajectory residuals from Ch5 5.1.1 (individual deviations from LMM-predicted forgetting curves). The core hypothesis is that well-calibrated individuals show more stable (less variable) forgetting patterns.

The analysis pipeline computes trajectory variability (SD of residuals across 4 timepoints per participant) and tests its correlation with Day 0 calibration quality. This is a simple correlation analysis with dual p-value reporting (Decision D068) and scatterplot visualization.

**Pipeline:** Correlation analysis (no IRT, no LMM)
**Steps:** 4 total analysis steps
**Estimated Runtime:** Low (data aggregation + correlation test, <5 minutes total)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (one-tailed: negative correlation expected; two-tailed: any relationship)

---

## Analysis Plan

### Step 0: Extract Calibration and Residuals Data

**Dependencies:** None (first step - loads from dependency RQs)
**Complexity:** Low (data loading and filtering only)

**Purpose:** Load Day 0 calibration scores from RQ 6.2.1 and trajectory residuals from Ch5 5.1.1.

**Input:**

**File 1:** results/ch6/6.2.1/data/step02_calibration_scores.csv (DERIVED from RQ 6.2.1)
**Source:** RQ 6.2.1 Step 2 (calibration computation)
**Format:** CSV with columns:
  - `composite_ID` (string, format: UID_test, e.g., P001_T1)
  - `calibration` (float, z-standardized difference: confidence_theta - accuracy_theta)
  - `test` (string, values: T1, T2, T3, T4)

**Required Rows:** 400 rows (100 participants x 4 tests)
**Filter:** Extract T1 rows only (Day 0 calibration predictor)
**Expected after filter:** 100 rows (one per participant)

**File 2:** results/ch5/5.1.1/data/step05_lmm_model_summary.txt (DERIVED from Ch5 5.1.1)
**Source:** Ch5 5.1.1 Step 5 (best LMM fitted)
**Format:** Text file containing model summary
**Alternative:** results/ch5/5.1.1/data/step05_lmm_residuals.csv
  - If residuals saved separately, load from CSV
  - Columns: `composite_ID`, `residual`
  - Rows: 400 (100 participants x 4 tests)

**File 3 (if needed):** results/ch5/5.1.1/data/step04_lmm_input.csv
**Source:** Ch5 5.1.1 Step 4 (LMM input with observed theta)
**Use:** Extract observed theta and re-compute residuals if not saved
**Columns:** `composite_ID`, `theta`, `TSVR_hours`, etc.

**Processing:**
1. Load calibration scores from RQ 6.2.1, filter to T1 (Day 0) only
2. Extract UID from composite_ID (remove _T1 suffix) -> creates calibration_day0.csv with UID, calibration
3. Load trajectory residuals from Ch5 5.1.1 (either from saved file or recompute from LMM input)
4. Ensure 400 residuals present (100 participants x 4 tests)
5. Validate no missing data (100 UIDs in calibration, 400 composite_IDs in residuals)

**Output:**

**File 1:** data/step00_calibration_day0.csv
**Format:** CSV with columns:
  - `UID` (string, format: P###)
  - `calibration` (float, z-standardized, Day 0 calibration quality)
**Expected Rows:** 100 (one per participant)

**File 2:** data/step00_trajectory_residuals.csv
**Format:** CSV with columns:
  - `composite_ID` (string, format: UID_test)
  - `UID` (string, extracted participant ID)
  - `test` (string, values: T1, T2, T3, T4)
  - `residual` (float, deviation from LMM-predicted theta)
**Expected Rows:** 400 (100 participants x 4 tests)

**Validation Requirement:**
Validation tools MUST be used after data extraction execution. Specific validation tools will be determined by rq_tools based on data extraction requirements. The rq_analysis agent will embed validation tool calls after the extraction tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_calibration_day0.csv: 100 rows x 2 columns (UID: object, calibration: float64)
- data/step00_trajectory_residuals.csv: 400 rows x 4 columns (composite_ID: object, UID: object, test: object, residual: float64)

*Value Ranges:*
- calibration: z-standardized values (mean approx 0, SD approx 1, range typically -3 to 3)
- residual: typically in [-2, 2] (deviations from LMM fit, could be larger for outliers)
- test: categorical, values in {T1, T2, T3, T4}

*Data Quality:*
- No NaN values tolerated in calibration or residual columns
- Expected N: Exactly 100 UIDs in calibration_day0.csv, exactly 400 rows in trajectory_residuals.csv
- No duplicate UIDs in calibration_day0.csv
- Each UID appears exactly 4 times in trajectory_residuals.csv (once per test T1-T4)
- UIDs match between files (all 100 UIDs from calibration present in residuals)

*Log Validation:*
- Required pattern: "Loaded 400 calibration scores from RQ 6.2.1"
- Required pattern: "Filtered to 100 Day 0 (T1) calibration scores"
- Required pattern: "Loaded 400 trajectory residuals from Ch5 5.1.1"
- Required pattern: "All 100 participants have complete data"
- Forbidden patterns: "ERROR", "File not found", "Missing data for UID"
- Acceptable warnings: None expected for data loading

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 100 Day 0 calibration scores, found 87")
- Log failure to logs/step00_extract_data.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause (dependency RQ incomplete? file path wrong?)

**Circuit Breaker (Dependency Check):**
- If RQ 6.2.1 status.yaml shows rq_results != "success": QUIT with "RQ 6.2.1 must complete before RQ 6.7.3 (dependency)"
- If Ch5 5.1.1 status.yaml shows rq_results != "success": QUIT with "Ch5 5.1.1 must complete before RQ 6.7.3 (dependency)"

---

### Step 1: Compute Trajectory Variability Per Participant

**Dependencies:** Step 0 (requires trajectory_residuals.csv)
**Complexity:** Low (data aggregation only, <1 minute)

**Purpose:** Compute SD of residuals across 4 timepoints for each participant (trajectory variability measure).

**Input:**

**File:** data/step00_trajectory_residuals.csv
**Format:** CSV with columns: UID, test, residual
**Expected Rows:** 400 (100 participants x 4 tests)

**Processing:**
1. Group by UID (creates 100 groups)
2. Compute SD of residuals per UID (standard deviation across 4 timepoint residuals)
3. Create trajectory_variability column (SD value per participant)
4. Validate all 100 participants have exactly 4 residuals (no missing tests)

**Output:**

**File:** data/step01_trajectory_variability.csv
**Format:** CSV with columns:
  - `UID` (string, participant ID)
  - `trajectory_variability` (float, SD of residuals across 4 tests)
**Expected Rows:** 100 (one per participant)

**Validation Requirement:**
Validation tools MUST be used after trajectory variability computation. Specific validation tools determined by rq_tools based on aggregation type.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_trajectory_variability.csv: 100 rows x 2 columns (UID: object, trajectory_variability: float64)

*Value Ranges:*
- trajectory_variability: SD values, must be >= 0 (SD cannot be negative)
- Typical range: [0.1, 2.0] (residual SDs, higher = more variable trajectories)
- Values > 3.0 suggest extreme variability or data error

*Data Quality:*
- No NaN values tolerated (all 100 participants must have computable SD)
- Expected N: Exactly 100 rows (one per participant)
- No duplicate UIDs
- All trajectory_variability values > 0 (SD = 0 only if all 4 residuals identical, unlikely)

*Log Validation:*
- Required pattern: "Computed trajectory variability for 100 participants"
- Required pattern: "Mean variability: [value], SD variability: [value]"
- Forbidden patterns: "ERROR", "NaN trajectory_variability", "UID with <4 residuals"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "UID P042 has only 3 residuals, expected 4")
- Log failure to logs/step01_compute_variability.log
- Quit script immediately
- g_debug invoked to diagnose (missing test data? extraction error in Step 0?)

---

### Step 2: Merge Calibration and Variability

**Dependencies:** Steps 0, 1 (requires calibration_day0.csv and trajectory_variability.csv)
**Complexity:** Low (data merge only, <1 minute)

**Purpose:** Merge Day 0 calibration with trajectory variability for correlation analysis.

**Input:**

**File 1:** data/step00_calibration_day0.csv
**Columns:** UID, calibration
**Rows:** 100

**File 2:** data/step01_trajectory_variability.csv
**Columns:** UID, trajectory_variability
**Rows:** 100

**Processing:**
1. Merge on UID (inner join to ensure complete data)
2. Validate all 100 participants present in both files (no missing data)
3. Create merged dataset for correlation

**Output:**

**File:** data/step02_calibration_variability.csv
**Format:** CSV with columns:
  - `UID` (string, participant ID)
  - `calibration` (float, Day 0 calibration quality, z-standardized)
  - `trajectory_variability` (float, SD of residuals)
**Expected Rows:** 100 (one per participant)

**Validation Requirement:**
Validation tools MUST be used after merge execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_calibration_variability.csv: 100 rows x 3 columns (UID: object, calibration: float64, trajectory_variability: float64)

*Value Ranges:*
- calibration: z-standardized, typically in [-3, 3]
- trajectory_variability: SD values, typically in [0.1, 2.0]

*Data Quality:*
- No NaN values tolerated in any column
- Expected N: Exactly 100 rows (all participants with complete data)
- No duplicate UIDs

*Log Validation:*
- Required pattern: "Merged calibration and variability: 100 participants with complete data"
- Forbidden patterns: "ERROR", "Missing data for UID", "Inner join resulted in <100 rows"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Only 87 participants after merge, expected 100")
- Log failure to logs/step02_merge_data.log
- Quit script immediately
- g_debug invoked to diagnose (data loss in prior steps?)

---

### Step 3: Compute Correlation with Dual P-Values

**Dependencies:** Step 2 (requires calibration_variability.csv)
**Complexity:** Low (single correlation test, <1 minute)

**Purpose:** Test correlation between Day 0 calibration and trajectory variability with dual p-value reporting (Decision D068).

**Input:**

**File:** data/step02_calibration_variability.csv
**Columns:** UID, calibration, trajectory_variability
**Rows:** 100

**Processing:**
1. Compute Pearson correlation: r(calibration, trajectory_variability)
2. Test significance with dual p-values:
   - One-tailed (negative correlation expected): H0: r >= 0, H1: r < 0
   - Two-tailed (any relationship): H0: r = 0, H1: r != 0
3. Compute effect size classification:
   - Small: |r| > 0.20
   - Moderate: |r| > 0.30
   - Large: |r| > 0.50
4. Interpret direction: better calibration (lower absolute error) should predict lower variability (more stable)

**Output:**

**File:** data/step03_correlation.csv
**Format:** CSV with columns:
  - `r` (float, Pearson correlation coefficient)
  - `p_one_tailed` (float, one-tailed p-value for negative correlation)
  - `p_two_tailed` (float, two-tailed p-value for any relationship)
  - `n` (int, sample size = 100)
  - `effect_size` (string, classification: small/moderate/large/negligible)
  - `direction` (string, positive/negative/null)
**Expected Rows:** 1 (single correlation result)

**Validation Requirement:**
Validation tools MUST be used after correlation computation. Specific validation tools determined by rq_tools (validate_correlation_test_d068 function checks dual p-values present).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_correlation.csv: 1 row x 6 columns (r: float64, p_one_tailed: float64, p_two_tailed: float64, n: int64, effect_size: object, direction: object)

*Value Ranges:*
- r: Pearson r in [-1, 1]
- p_one_tailed: p-value in [0, 1]
- p_two_tailed: p-value in [0, 1]
- n: exactly 100
- effect_size: categorical, values in {negligible, small, moderate, large}
- direction: categorical, values in {positive, negative, null}

*Data Quality:*
- No NaN values tolerated in any column
- Expected N: Exactly 1 row
- BOTH p-values present (Decision D068 requirement)
- p_two_tailed should be approximately 2 x p_one_tailed (if one-tailed test appropriate)

*Log Validation:*
- Required pattern: "Pearson r = [value], p (one-tailed) = [value], p (two-tailed) = [value]"
- Required pattern: "Effect size: [classification]"
- Required pattern: "Direction: [positive/negative/null]"
- Forbidden patterns: "ERROR", "NaN correlation", "Missing p-value"
- Acceptable warnings: "Correlation not significant at alpha=0.05" (if null result)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Missing one-tailed p-value, Decision D068 requires dual reporting")
- Log failure to logs/step03_correlation.log
- Quit script immediately
- g_debug invoked to diagnose

---

### Step 4: Prepare Scatterplot Data

**Dependencies:** Step 2 (requires calibration_variability.csv)
**Complexity:** Low (data copy + regression line computation, <1 minute)

**Purpose:** Prepare plot source CSV for scatterplot visualization (Option B architecture).

**Input:**

**File:** data/step02_calibration_variability.csv
**Columns:** UID, calibration, trajectory_variability
**Rows:** 100

**Processing:**
1. Copy calibration_variability.csv data
2. Compute regression line: trajectory_variability ~ calibration (for plotting)
3. Add predicted values column (regression line y-values)
4. Format for plotting (x = calibration, y = trajectory_variability, y_pred = regression line)

**Output:**

**File:** data/step04_scatterplot_data.csv
**Format:** CSV with columns:
  - `calibration` (float, x-axis variable)
  - `trajectory_variability` (float, y-axis variable, observed)
  - `y_predicted` (float, regression line predictions)
**Expected Rows:** 100 (one per participant)

**Validation Requirement:**
Validation tools MUST be used after plot data preparation. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_scatterplot_data.csv: 100 rows x 3 columns (calibration: float64, trajectory_variability: float64, y_predicted: float64)

*Value Ranges:*
- calibration: z-standardized, typically in [-3, 3]
- trajectory_variability: SD values, typically in [0.1, 2.0]
- y_predicted: regression predictions, should span similar range as trajectory_variability

*Data Quality:*
- No NaN values tolerated in any column
- Expected N: Exactly 100 rows
- y_predicted should be linear function of calibration (monotonic relationship)

*Log Validation:*
- Required pattern: "Plot data prepared: 100 observations"
- Required pattern: "Regression line computed"
- Forbidden patterns: "ERROR", "NaN in plot data"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "NaN values in y_predicted column")
- Log failure to logs/step04_prepare_plot_data.log
- Quit script immediately
- g_debug invoked to diagnose

**Plotting Function (rq_plots will call):** Scatterplot with regression line
- rq_plots agent maps this to appropriate plotting function
- Plot reads data/step04_scatterplot_data.csv (created by this step)
- No data aggregation in rq_plots (visualization only per Option B)
- PNG output saved to plots/ folder by rq_plots

---

## Expected Data Formats

### Calibration Variable

**Source:** RQ 6.2.1 (confidence_theta - accuracy_theta, z-standardized)
**Format:** Continuous numeric, z-standardized (mean approx 0, SD approx 1)
**Interpretation:** Higher values = overconfidence (confidence > accuracy), lower values = underconfidence
**Absolute value:** Better calibration = lower |calibration| (closer to 0)
**Range:** Typically [-3, 3] for z-scores

### Trajectory Variability

**Source:** SD of residuals from Ch5 5.1.1 LMM fit
**Format:** Continuous numeric, SD values (always >= 0)
**Interpretation:** Higher values = more variable trajectories (less stable forgetting)
**Range:** Typically [0.1, 2.0] for residual SDs

### Correlation Interpretation

**Expected Direction:** Negative correlation (good calibration predicts low variability)
- If r < 0 and p < 0.05: Supports hypothesis (calibration predicts stability)
- If r approx 0 or p > 0.05: Null result (no relationship)
- If r > 0 and p < 0.05: Unexpected (poor calibration predicts stability?)

**Effect Size Thresholds:**
- |r| > 0.20: Small effect
- |r| > 0.30: Moderate effect
- |r| > 0.50: Large effect

---

## Cross-RQ Dependencies

### Dependency Type: DERIVED Data from Two RQs

**This RQ requires outputs from:**

- **RQ 6.2.1** (Calibration Over Time)
  - File: results/ch6/6.2.1/data/step02_calibration_scores.csv
  - Used in: Step 0 (extract Day 0 calibration predictor)
  - Rationale: RQ 6.2.1 computes confidence-accuracy alignment. This RQ uses Day 0 calibration as predictor variable.

- **Ch5 5.1.1** (Functional Form Comparison)
  - File: results/ch5/5.1.1/data/step05_lmm_residuals.csv (or recompute from lmm_input.csv)
  - Used in: Step 0 (extract trajectory residuals for variability computation)
  - Rationale: Ch5 5.1.1 fits best LMM trajectory model. This RQ uses individual deviations (residuals) as stability measure.

**Execution Order Constraint:**
1. RQ 6.2.1 must complete through Step 2 (calibration scores computed)
2. Ch5 5.1.1 must complete through Step 5 (LMM fitted, residuals available)
3. This RQ executes after both dependencies satisfied

**Data Source Boundaries:**
- **RAW data:** None used (no direct master.xlsx extraction)
- **DERIVED data:** 100% of inputs from other RQs (RQ 6.2.1 and Ch5 5.1.1)
- **Scope:** This RQ does NOT re-run IRT or LMM (uses existing outputs)

**Validation:**
- Step 0: Check results/ch6/6.2.1/status.yaml shows rq_results: success (circuit breaker if not)
- Step 0: Check results/ch5/5.1.1/status.yaml shows rq_results: success (circuit breaker if not)
- If either dependency incomplete -> quit with error -> user must execute dependency RQs first

---

## Validation Requirements

**CRITICAL MANDATE:**

Every analysis step in this plan MUST use validation tools after analysis tool execution.

This is not optional. This is the core architectural principle preventing cascading failures observed in v3.0 (where analysis errors propagated undetected through downstream steps before discovery).

**Exact Specification Requirement:**

> "Validation tools MUST be used after analysis tool execution"

**Implementation:**
- rq_tools (Step 11 workflow) will read tool_inventory.md validation tools section
- rq_tools will specify BOTH analysis tool + validation tool per step in 3_tools.yaml
- rq_analysis (Step 12 workflow) will embed validation tool call AFTER analysis tool call in 4_analysis.yaml
- g_code (Step 14 workflow) will generate stepNN_*.py scripts with validation function calls
- bash execution (Step 14 workflow) will run analysis -> validation -> error on validation failure

**Downstream Agent Requirements:**
- **rq_tools:** MUST specify validation tool for EVERY analysis step (no exceptions)
- **rq_analysis:** MUST embed validation tool call for EVERY analysis step (no exceptions)
- **g_code:** MUST generate code with validation function calls (no exceptions)
- **rq_inspect:** MUST verify validation ran successfully (checks logs/stepNN_*.log for validation output)

### Validation Requirements By Step

#### Step 0: Extract Calibration and Residuals Data

**Analysis Tool:** (determined by rq_tools - likely tools.data.load_derived_data or custom extraction)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure)

**What Validation Checks:**
- Output files exist (calibration_day0.csv, trajectory_residuals.csv)
- Expected row counts (100 for calibration, 400 for residuals)
- Expected column counts and names
- No unexpected NaN values
- UID matching between files (all 100 UIDs in calibration present in residuals)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step00_extract_data.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose (dependency RQ file missing? wrong path? incomplete data?)

---

#### Step 1: Compute Trajectory Variability

**Analysis Tool:** (determined by rq_tools - likely pandas groupby + std)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_numeric_range)

**What Validation Checks:**
- Output file exists (trajectory_variability.csv)
- Expected row count (100 participants)
- trajectory_variability values all >= 0 (SD cannot be negative)
- trajectory_variability in reasonable range [0.1, 3.0]
- No NaN values

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step01_compute_variability.log
- Quit script immediately
- g_debug invoked

---

#### Step 2: Merge Calibration and Variability

**Analysis Tool:** (determined by rq_tools - likely pandas merge)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_data_format)

**What Validation Checks:**
- Output file exists (calibration_variability.csv)
- Expected row count (100 participants)
- Required columns present (UID, calibration, trajectory_variability)
- No NaN values
- No duplicate UIDs

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step02_merge_data.log
- Quit script immediately
- g_debug invoked

---

#### Step 3: Compute Correlation with Dual P-Values

**Analysis Tool:** (determined by rq_tools - likely scipy.stats.pearsonr with custom dual p-value wrapper)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_correlation_test_d068)

**What Validation Checks:**
- Output file exists (correlation.csv)
- Expected row count (1 result)
- r value in [-1, 1]
- BOTH p-values present (p_one_tailed AND p_two_tailed per Decision D068)
- p-values in [0, 1]
- n = 100
- effect_size classification valid
- direction classification valid

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Missing p_two_tailed, Decision D068 requires dual reporting")
- Log failure to logs/step03_correlation.log
- Quit script immediately
- g_debug invoked

---

#### Step 4: Prepare Scatterplot Data

**Analysis Tool:** (determined by rq_tools - likely pandas + regression computation)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_plot_data_completeness)

**What Validation Checks:**
- Output file exists (scatterplot_data.csv)
- Expected row count (100 observations)
- Required columns present (calibration, trajectory_variability, y_predicted)
- No NaN values
- y_predicted values reasonable (regression line predictions)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step04_prepare_plot_data.log
- Quit script immediately
- g_debug invoked

---

## Summary

**Total Steps:** 4 (Step 0: extraction, Steps 1-3: analysis, Step 4: plot prep)
**Estimated Runtime:** Low (<5 minutes total - all data aggregation and single correlation test)
**Cross-RQ Dependencies:** RQ 6.2.1 (calibration scores), Ch5 5.1.1 (trajectory residuals)
**Primary Outputs:**
- data/step03_correlation.csv (correlation result with dual p-values)
- data/step04_scatterplot_data.csv (plot source CSV for visualization)
**Validation Coverage:** 100% (all 4 steps have validation requirements)

**Key Features:**
- DERIVED data analysis (no RAW data extraction from master.xlsx)
- Simple correlation test (no IRT, no LMM)
- Decision D068 applied (dual p-value reporting)
- Option B plotting architecture (plot data preparation as analysis step)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_*.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent for RQ 6.7.3
