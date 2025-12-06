# Analysis Plan: RQ 6.6.1 - High-Confidence Errors Over Time

**Research Question:** 6.6.1
**Created:** 2025-12-06
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines whether high-confidence errors (HCE: Confidence >= 0.75 AND Accuracy = 0) increase from Day 0 to Day 6, reflecting metacognitive failure where confidence doesn't track memory degradation. The analysis uses item-level confidence-accuracy data (~27,200 item-responses) aggregated to participant-level HCE rates (400 observations: 100 participants x 4 tests), then models HCE trajectories using Linear Mixed Models.

**Pipeline:** LMM only (no IRT calibration - uses raw confidence/accuracy data)

**Steps:** 4 analysis steps (Step 0: extraction + Steps 1-3: analysis)

**Estimated Runtime:** Low to Medium (data extraction + LMM fitting + trajectory aggregation, ~10-20 minutes total)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + correction) for Time effect test
- Decision D070: TSVR as time variable (actual hours, not nominal days)

---

## Analysis Plan

### Step 0: Extract Item-Level Confidence-Accuracy Data

**Dependencies:** None (first step - RAW data extraction from dfData.csv)

**Complexity:** Low (data extraction only, ~2-5 minutes)

**Input:**

**File:** data/cache/dfData.csv (project-level data source)

**Required Columns:**
- `UID` (string, participant identifier)
- `TEST` (string, test session identifier: T1/T2/T3/T4)
- `TSVR` (float, actual hours since encoding per Decision D070)
- Confidence items: TC_* tags (5-level Likert: 0, 0.25, 0.5, 0.75, 1.0)
- Accuracy items: TQ_* tags (dichotomous: 0=incorrect, 1=correct)

**Tag Patterns:**
- Paradigms: IFR, ICR, IRE (interactive paradigms with paired confidence/accuracy data)
- Exclude: RFR (no confidence data), TCR, RRE (text-based, not VR episodic memory)
- Domains: All WWW domains (-N- What, -L-/-U-/-D- Where, -O- When)

**Processing:**

1. Filter dfData.csv to TC_* and TQ_* columns (confidence and accuracy items)
2. Filter to interactive paradigms only (IFR, ICR, IRE) - exclude RFR, TCR, RRE
3. Reshape to long format: one row per item-response
4. Match confidence and accuracy items by item code (TC_XXX pairs with TQ_XXX)
5. Merge UID, TEST, TSVR metadata
6. Create item-level dataset with columns: UID, TEST, TSVR, item_code, confidence, accuracy

**Output:**

**File:** data/step00_item_level.csv

**Format:** CSV, long format (one row per item-response)

**Columns:**
- `UID` (string, participant identifier, format: P### with leading zeros)
- `TEST` (string, test session: T1, T2, T3, T4)
- `TSVR` (float, hours since encoding)
- `item_code` (string, item identifier)
- `confidence` (float, 5-level: 0, 0.25, 0.5, 0.75, 1.0)
- `accuracy` (int, dichotomous: 0=incorrect, 1=correct)

**Expected Rows:** ~27,200 (100 participants x 4 tests x ~68 items)

**Validation Requirement:**

Validation tools MUST be used after data extraction tool execution. Specific validation tools will be determined by rq_tools based on extraction type (data format validation, missing data checks, value range validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_item_level.csv exists (exact path)
- Expected rows: 26,000-28,000 (100 participants x 4 tests x ~65-70 items, some variation acceptable)
- Expected columns: 6 (UID, TEST, TSVR, item_code, confidence, accuracy)
- Data types: UID (string), TEST (string), TSVR (float64), item_code (string), confidence (float64), accuracy (int64)

*Value Ranges:*
- confidence in {0, 0.25, 0.5, 0.75, 1.0} (5-level Likert, no other values allowed)
- accuracy in {0, 1} (dichotomous, no other values allowed)
- TSVR in [0, 200] hours (0=encoding, up to ~8 days maximum)
- TEST in {T1, T2, T3, T4} (categorical, no other values)

*Data Quality:*
- <5% NaN tolerated in confidence/accuracy (some missing data expected)
- All 100 participants present (UID count = 100)
- All 4 tests present per participant (4 observations per UID)
- No duplicate rows (UID x TEST x item_code combinations unique)

*Log Validation:*
- Required pattern: "Extracted {N} item-responses from {M} participants"
- Required pattern: "Paradigms included: IFR, ICR, IRE"
- Forbidden patterns: "ERROR", "No confidence data found", "TSVR missing"
- Acceptable warnings: "Missing confidence for item X" (some missingness expected)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected confidence in {0, 0.25, 0.5, 0.75, 1.0}, found 0.8")
- Log failure to logs/step00_extract_item_level.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause

---

### Step 1: Compute HCE Rate Per Participant Per Timepoint

**Dependencies:** Step 0 (requires extracted item-level data)

**Complexity:** Low (data aggregation only, <5 minutes)

**Input:**

**File:** data/step00_item_level.csv (from Step 0)

**Format:** Long format (one row per item-response)

**Columns:**
- `UID` (string, participant identifier)
- `TEST` (string, test session: T1, T2, T3, T4)
- `TSVR` (float, hours since encoding)
- `item_code` (string, item identifier)
- `confidence` (float, 5-level: 0, 0.25, 0.5, 0.75, 1.0)
- `accuracy` (int, dichotomous: 0=incorrect, 1=correct)

**Processing:**

1. Define HCE: confidence >= 0.75 AND accuracy = 0 (high-confidence incorrect responses)
2. Group by UID and TEST
3. Count HCE instances per participant per test: n_HCE = sum(confidence >= 0.75 AND accuracy = 0)
4. Count total items per participant per test: n_total = count(non-NaN confidence AND non-NaN accuracy)
5. Compute HCE_rate = n_HCE / n_total per participant per timepoint
6. Merge TSVR (time variable for LMM per Decision D070)

**Output:**

**File:** data/step01_hce_rates.csv

**Format:** CSV, long format (one row per participant-test combination)

**Columns:**
- `UID` (string, participant identifier)
- `TEST` (string, test session: T1, T2, T3, T4)
- `TSVR` (float, hours since encoding)
- `HCE_rate` (float, proportion: n_HCE / n_total, range [0, 1])
- `n_HCE` (int, count of high-confidence errors)
- `n_total` (int, count of total valid item-responses)

**Expected Rows:** 400 (100 participants x 4 tests)

**Validation Requirement:**

Validation tools MUST be used after HCE computation tool execution. Specific validation tools will be determined by rq_tools based on computation type (proportion validation, count validation, data format validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_hce_rates.csv exists (exact path)
- Expected rows: 400 (100 participants x 4 tests)
- Expected columns: 6 (UID, TEST, TSVR, HCE_rate, n_HCE, n_total)
- Data types: UID (string), TEST (string), TSVR (float64), HCE_rate (float64), n_HCE (int64), n_total (int64)

*Value Ranges:*
- HCE_rate in [0, 1] (proportion, scientifically reasonable)
- n_HCE >= 0 (count, non-negative)
- n_total > 0 (count, positive - every participant must have valid items)
- n_HCE <= n_total (HCE cannot exceed total)
- TSVR in [0, 200] hours (time range)

*Data Quality:*
- No NaN values in HCE_rate (all participants must have computable rate)
- All 100 participants present (UID count = 100)
- All 4 tests present per participant (4 observations per UID)
- No duplicate rows (UID x TEST combinations unique)
- n_total reasonable range: 50-80 items per participant per test (some variation acceptable)

*Log Validation:*
- Required pattern: "Computed HCE rates for 400 observations (100 participants x 4 tests)"
- Required pattern: "Mean HCE_rate: {value}" (sanity check - should be <0.5 typically)
- Forbidden patterns: "ERROR", "Division by zero", "NaN HCE_rate"
- Acceptable warnings: "Participant {UID} has zero HCE at {TEST}" (possible, not error)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 400 rows, found 387")
- Log failure to logs/step01_compute_hce_rates.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose root cause

---

### Step 2: Fit LMM for HCE Trajectory

**Dependencies:** Step 1 (requires computed HCE rates)

**Complexity:** Low to Medium (LMM fitting, ~5-10 minutes)

**Input:**

**File:** data/step01_hce_rates.csv (from Step 1)

**Format:** Long format (one row per participant-test combination)

**Columns:**
- `UID` (string, participant identifier)
- `TEST` (string, test session: T1, T2, T3, T4)
- `TSVR` (float, hours since encoding)
- `HCE_rate` (float, proportion: range [0, 1])

**Processing:**

1. Prepare LMM input:
   - Dependent variable: HCE_rate (proportion)
   - Fixed effect: TSVR (continuous time variable per Decision D070)
   - Random effects: Random intercepts and slopes by UID (Time | UID)
2. Fit Linear Mixed Model:
   - Formula: HCE_rate ~ TSVR + (TSVR | UID)
   - Method: REML=True (for variance estimation)
   - Family: Gaussian (assuming normally distributed residuals)
3. Extract model summary:
   - Fixed effects table (coefficients, SE, t-values, p-values)
   - Random effects variance components
   - Model fit indices (AIC, BIC, log-likelihood)
4. Save model summary to text file

**Output:**

**File:** data/step02_hce_lmm.txt

**Format:** Plain text model summary

**Contents:**
- Fixed effects table (TSVR coefficient, intercept)
- Random effects variance components (intercept variance, slope variance, residual variance)
- Model fit indices (AIC, BIC, log-likelihood)
- Convergence status

**Validation Requirement:**

Validation tools MUST be used after LMM fitting tool execution. Specific validation tools will be determined by rq_tools based on model type (LMM convergence validation, residual normality, homoscedasticity checks).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_hce_lmm.txt exists (exact path)
- File size > 500 bytes (non-empty model summary)

*Value Ranges:*
- TSVR coefficient (slope): scientifically reasonable range [-0.01, 0.01] (proportion change per hour)
- Intercept: [0, 1] (starting HCE rate at encoding)
- Variance components > 0 (positive variance)
- p-values in [0, 1] (valid probability)

*Data Quality:*
- Model converged successfully (no convergence warnings)
- Residuals approximately normal (Kolmogorov-Smirnov test p > 0.05)
- No extreme outliers in residuals (studentized residuals within [-3, 3])

*Log Validation:*
- Required pattern: "Model converged: True"
- Required pattern: "VALIDATION - PASS: LMM convergence"
- Required pattern: "VALIDATION - PASS: Residual normality"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "Singular matrix"
- Acceptable warnings: "Random slope variance small" (possible if limited variation)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Model did not converge after 100 iterations")
- Log failure to logs/step02_fit_hce_lmm.log
- Quit script immediately (do NOT proceed to Step 3)
- g_debug invoked to diagnose root cause

---

### Step 3: Test Time Effect on HCE Rate (Dual P-Values per D068)

**Dependencies:** Step 2 (requires fitted LMM model)

**Complexity:** Low (hypothesis test extraction, <5 minutes)

**Input:**

**File:** data/step02_hce_lmm.txt (from Step 2 - model summary)

**Source:** Fitted LMM model object (in memory or saved as pickle if rq_tools specifies)

**Processing:**

1. Extract TSVR fixed effect from fitted model:
   - Coefficient (slope of HCE_rate over time)
   - Standard error
   - Wald test p-value (from model summary)
2. Compute Likelihood Ratio Test (LRT) for Time effect:
   - Fit reduced model: HCE_rate ~ 1 + (TSVR | UID) (no TSVR fixed effect)
   - Compare full vs reduced via LRT
   - Extract LRT p-value
3. Report dual p-values per Decision D068:
   - Uncorrected p-value: Wald test p-value from full model
   - LRT p-value: Likelihood Ratio Test comparing full vs reduced
4. Save Time effect test results to CSV

**Output:**

**File:** data/step03_time_effect.csv

**Format:** CSV with hypothesis test results

**Columns:**
- `effect` (string, fixed: "TSVR")
- `coefficient` (float, TSVR slope estimate)
- `SE` (float, standard error of coefficient)
- `p_wald` (float, Wald test p-value, uncorrected)
- `p_lrt` (float, Likelihood Ratio Test p-value)
- `significant` (bool, TRUE if either p < 0.05)

**Expected Rows:** 1 (single Time effect test)

**Validation Requirement:**

Validation tools MUST be used after hypothesis test extraction tool execution. Specific validation tools will be determined by rq_tools based on test type (dual p-value validation per Decision D068, effect size validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_time_effect.csv exists (exact path)
- Expected rows: 1 (single Time effect)
- Expected columns: 6 (effect, coefficient, SE, p_wald, p_lrt, significant)
- Data types: effect (string), coefficient (float64), SE (float64), p_wald (float64), p_lrt (float64), significant (bool)

*Value Ranges:*
- coefficient in [-0.01, 0.01] (scientifically reasonable proportion change per hour)
- SE > 0 (positive standard error)
- p_wald in [0, 1] (valid probability)
- p_lrt in [0, 1] (valid probability)

*Data Quality:*
- Both p_wald and p_lrt present (dual p-values required per D068)
- SE not suspiciously small (<0.0001 suggests estimation problem)
- coefficient and SE have consistent signs (if coefficient positive, SE positive)

*Log Validation:*
- Required pattern: "VALIDATION - PASS: Dual p-values present (Wald and LRT)"
- Required pattern: "Time effect (TSVR): coefficient = {value}, p_wald = {value}, p_lrt = {value}"
- Forbidden patterns: "ERROR", "Missing p-value", "NaN coefficient"
- Acceptable warnings: "LRT p-value differs substantially from Wald" (possible, not error)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Missing LRT p-value, only Wald present")
- Log failure to logs/step03_test_time_effect.log
- Quit script immediately (do NOT proceed to Step 4)
- g_debug invoked to diagnose root cause

---

### Step 4: Compute Mean HCE Rate by Timepoint (Plot Data Preparation)

**Dependencies:** Step 1 (requires computed HCE rates)

**Complexity:** Low (data aggregation, <5 minutes)

**Input:**

**File:** data/step01_hce_rates.csv (from Step 1)

**Format:** Long format (one row per participant-test combination)

**Columns:**
- `UID` (string, participant identifier)
- `TEST` (string, test session: T1, T2, T3, T4)
- `TSVR` (float, hours since encoding)
- `HCE_rate` (float, proportion)

**Processing:**

1. Group by TEST (aggregate across participants)
2. Compute mean HCE_rate per timepoint
3. Compute standard error: SE = SD / sqrt(N)
4. Compute 95% confidence intervals: CI_lower = mean - 1.96*SE, CI_upper = mean + 1.96*SE
5. Extract mean TSVR per timepoint (for x-axis plotting)
6. Create plot source CSV with columns: time, HCE_rate_mean, CI_lower, CI_upper, test

**Output:**

**File:** data/step04_hce_trajectory_data.csv

**Format:** CSV, plot source data for HCE trajectory visualization

**Columns:**
- `time` (float, mean TSVR hours per timepoint)
- `HCE_rate_mean` (float, mean HCE rate across participants)
- `CI_lower` (float, lower 95% confidence bound)
- `CI_upper` (float, upper 95% confidence bound)
- `test` (string, test session label: T1, T2, T3, T4)

**Expected Rows:** 4 (4 timepoints: T1, T2, T3, T4)

**Note:** This CSV is read by rq_plots later for trajectory visualization. PNG output goes to plots/ when rq_plots runs.

**Validation Requirement:**

Validation tools MUST be used after plot data preparation tool execution. Specific validation tools will be determined by rq_tools based on plot data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_hce_trajectory_data.csv exists (exact path)
- Expected rows: 4 (4 timepoints)
- Expected columns: 5 (time, HCE_rate_mean, CI_lower, CI_upper, test)
- Data types: time (float64), HCE_rate_mean (float64), CI_lower (float64), CI_upper (float64), test (string)

*Value Ranges:*
- time in [0, 200] hours (timepoint range)
- HCE_rate_mean in [0, 1] (proportion range)
- CI_lower in [0, 1] (confidence bound range)
- CI_upper in [0, 1] (confidence bound range)
- CI_upper > CI_lower for all rows (confidence interval logic)

*Data Quality:*
- No NaN values tolerated (all cells must have valid values)
- Expected N: Exactly 4 rows (no more, no less)
- No duplicate rows (test values unique)
- time values monotonically increasing (T1 < T2 < T3 < T4 chronologically)

*Log Validation:*
- Required pattern: "Plot data preparation complete: 4 timepoints created"
- Required pattern: "All tests represented: T1, T2, T3, T4"
- Forbidden patterns: "ERROR", "NaN values detected", "Missing timepoint"
- Acceptable warnings: None expected for plot data preparation

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 4 rows, found 3")
- Log failure to logs/step04_prepare_trajectory_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- g_debug invoked to diagnose root cause

**Plotting Function (rq_plots will call):** Trajectory plot showing HCE rate over time with confidence bands
- rq_plots agent maps this description to specific tools/plots.py function (likely plot_trajectory)
- Plot reads data/step04_hce_trajectory_data.csv (created by this step)
- No data aggregation in rq_plots (visualization only per Option B)
- PNG output saved to plots/ folder by rq_plots

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs - intermediate and final)
- data/step00_item_level.csv (from Step 0: item-level extraction, ~27,200 rows)
- data/step01_hce_rates.csv (from Step 1: HCE rates per participant-test, 400 rows)
- data/step02_hce_lmm.txt (from Step 2: LMM model summary)
- data/step03_time_effect.csv (from Step 3: Time effect test with dual p-values, 1 row)
- data/step04_hce_trajectory_data.csv (from Step 4: plot source CSV, 4 rows)

### Logs (ONLY execution logs - .log files capturing stdout/stderr)
- logs/step00_extract_item_level.log
- logs/step01_compute_hce_rates.log
- logs/step02_fit_hce_lmm.log
- logs/step03_test_time_effect.log
- logs/step04_prepare_trajectory_data.log

### Plots (EMPTY until rq_plots runs)
- plots/hce_trajectory.png (created by rq_plots, NOT analysis steps)

### Results (EMPTY until rq_results runs)
- results/summary.md (created by rq_results, NOT analysis steps)

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 -> Step 1 (Wide to Aggregated):**
- Input: Item-level data (~27,200 rows, one per item-response)
- Output: Participant-level HCE rates (400 rows, one per participant-test)
- Transformation: Group by UID x TEST, compute HCE_rate = n_HCE / n_total

**Step 1 -> Step 2 (Long Format for LMM):**
- Input: Participant-level HCE rates (400 rows)
- Output: LMM model summary (text file)
- Transformation: Fit LMM with TSVR as time variable (Decision D070)

**Step 2 -> Step 3 (Model to Test Results):**
- Input: Fitted LMM model object
- Output: Time effect test results (1 row CSV)
- Transformation: Extract TSVR coefficient, compute dual p-values (Wald and LRT per D068)

**Step 1 -> Step 4 (Aggregated for Plotting):**
- Input: Participant-level HCE rates (400 rows)
- Output: Timepoint-level mean HCE rates (4 rows)
- Transformation: Group by TEST, compute mean HCE_rate + 95% CI

### Column Naming Conventions

Per names.md (populated during RQ 5.1):
- `UID`: participant identifier (no underscore)
- `TEST`: test session (T1, T2, T3, T4)
- `TSVR`: Time Since VR in hours (Decision D070 - actual time, not nominal days)
- `HCE_rate`: High-Confidence Error rate (proportion)
- `CI_lower`, `CI_upper`: 95% confidence interval bounds

### Data Type Constraints

**Categorical Variables:**
- TEST: {T1, T2, T3, T4} (no other values)
- UID: string format (participant identifier)

**Continuous Variables:**
- HCE_rate: [0, 1] (proportion, non-negative, bounded)
- TSVR: [0, 200] hours (time range, non-negative)
- confidence: {0, 0.25, 0.5, 0.75, 1.0} (ordinal, 5 levels)
- accuracy: {0, 1} (dichotomous)

**Counts:**
- n_HCE: non-negative integer
- n_total: positive integer
- n_HCE <= n_total (logical constraint)

---

## Cross-RQ Dependencies

**This RQ uses:** Only dfData.csv (RAW data extraction)

**No dependencies on other RQs:** Can be executed independently

**Execution order:** Flexible (no prerequisite RQs required)

**Data Sources:**
- dfData.csv (confidence and accuracy items: TC_*, TQ_* tags)
- TSVR metadata (actual hours since encoding per Decision D070)

**Note:** All data extraction uses direct reading from dfData.csv. No intermediate outputs from other RQs required.

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

#### Step 0: Extract Item-Level Confidence-Accuracy Data

**Analysis Tool:** (determined by rq_tools - likely data extraction function)

**Validation Tool:** (determined by rq_tools - likely validate_data_format, validate_numeric_range)

**What Validation Checks:**
- Output file exists (data/step00_item_level.csv)
- Expected row count (~26,000-28,000 item-responses)
- Expected column count (6 columns: UID, TEST, TSVR, item_code, confidence, accuracy)
- confidence values in {0, 0.25, 0.5, 0.75, 1.0} only
- accuracy values in {0, 1} only
- TSVR in [0, 200] hours
- <5% NaN in confidence/accuracy columns

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected confidence in {0, 0.25, 0.5, 0.75, 1.0}, found 0.8")
- Log failure to logs/step00_extract_item_level.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked by master to diagnose root cause

---

#### Step 1: Compute HCE Rate Per Participant Per Timepoint

**Analysis Tool:** (determined by rq_tools - likely custom HCE computation function)

**Validation Tool:** (determined by rq_tools - likely validate_probability_range, validate_dataframe_structure)

**What Validation Checks:**
- Output file exists (data/step01_hce_rates.csv)
- Expected row count (400 rows: 100 participants x 4 tests)
- HCE_rate in [0, 1] (proportion range)
- n_HCE <= n_total (logical constraint)
- No NaN in HCE_rate column
- All 100 participants present
- All 4 tests present per participant

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Expected 400 rows, found 387")
- Log failure to logs/step01_compute_hce_rates.log
- Quit script immediately
- g_debug invoked to diagnose root cause

---

#### Step 2: Fit LMM for HCE Trajectory

**Analysis Tool:** (determined by rq_tools - likely fit_lmm_trajectory_tsvr)

**Validation Tool:** (determined by rq_tools - likely validate_lmm_convergence, validate_lmm_residuals)

**What Validation Checks:**
- Output file exists (data/step02_hce_lmm.txt)
- Model converged successfully (no convergence warnings)
- Residuals approximately normal (KS test p > 0.05)
- Variance components > 0 (positive variance)
- TSVR coefficient in scientifically reasonable range
- No extreme outliers in residuals

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Model did not converge")
- Log failure to logs/step02_fit_hce_lmm.log
- Quit script immediately
- g_debug invoked to diagnose root cause

---

#### Step 3: Test Time Effect on HCE Rate

**Analysis Tool:** (determined by rq_tools - likely extract_fixed_effects_from_lmm + LRT function)

**Validation Tool:** (determined by rq_tools - likely validate_hypothesis_test_dual_pvalues per D068)

**What Validation Checks:**
- Output file exists (data/step03_time_effect.csv)
- Expected row count (1 row: single Time effect)
- Both p_wald and p_lrt present (dual p-values per D068)
- p-values in [0, 1] range
- SE > 0 (positive standard error)
- coefficient in scientifically reasonable range

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Missing LRT p-value, only Wald present")
- Log failure to logs/step03_test_time_effect.log
- Quit script immediately
- g_debug invoked to diagnose root cause

---

#### Step 4: Compute Mean HCE Rate by Timepoint

**Analysis Tool:** (determined by rq_tools - likely data aggregation function)

**Validation Tool:** (determined by rq_tools - likely validate_plot_data_completeness, validate_probability_range)

**What Validation Checks:**
- Output file exists (data/step04_hce_trajectory_data.csv)
- Expected row count (4 rows: 4 timepoints)
- Expected column count (5 columns)
- HCE_rate_mean in [0, 1] range
- CI_upper > CI_lower for all rows
- No NaN values
- All 4 tests represented (T1, T2, T3, T4)
- time values monotonically increasing

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Expected 4 rows, found 3")
- Log failure to logs/step04_prepare_trajectory_data.log
- Quit script immediately
- g_debug invoked to diagnose root cause

---

## Summary

**Total Steps:** 4 (Step 0: extraction + Steps 1-3: analysis)

**Estimated Runtime:** Low to Medium (~10-20 minutes total: extraction + HCE computation + LMM fitting + trajectory aggregation)

**Cross-RQ Dependencies:** None (RAW data only from dfData.csv)

**Primary Outputs:**
- data/step01_hce_rates.csv (HCE rates per participant-test, 400 rows)
- data/step02_hce_lmm.txt (LMM model summary with Time effect)
- data/step03_time_effect.csv (Time effect test with dual p-values per D068, 1 row)
- data/step04_hce_trajectory_data.csv (plot source CSV, 4 rows)

**Validation Coverage:** 100% (all 4 steps have validation requirements with 4-layer substance criteria)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent
