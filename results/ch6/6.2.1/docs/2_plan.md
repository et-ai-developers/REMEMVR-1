# Analysis Plan for RQ 6.2.1: Calibration Over Time

**Created by:** rq_planner agent
**Date:** 2025-12-06
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This RQ examines whether calibration (confidence-accuracy alignment) changes from Day 0 to Day 6. Calibration is defined as the difference between confidence and accuracy at the person-timepoint level. This analysis merges IRT-derived theta scores from both accuracy (Ch5 5.1.1) and confidence (Ch6 6.1.1) domains.

The analysis pipeline consists of 7 steps:
1. Merge accuracy and confidence theta scores
2. Compute calibration metric (theta_confidence - theta_accuracy after z-standardization)
3. Compute Brier score at item level
4. Compute Expected Calibration Error (ECE) per timepoint
5. Fit LMM for calibration trajectory
6. Test Time effect with dual p-values (Decision D068)
7. Prepare plot data for calibration trajectory visualization (Decision D069 dual-scale)

**Pipeline:** Theta merge -> Calibration metrics -> LMM trajectory analysis -> Plot data preparation

**Steps:** 7 total analysis steps

**Estimated Runtime:** Medium (Step 5 LMM fitting may take 5-15 minutes, other steps <5 minutes each)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + correction method)
- Decision D069: Dual-scale trajectory plots (theta + probability scales)
- Decision D070: TSVR as time variable (actual hours, not nominal days)

---

## Analysis Plan

### Step 0a: Load Accuracy Theta Scores

**Dependencies:** None (reads from completed RQ 5.1.1)
**Complexity:** Low (<1 minute)

**Purpose:** Load accuracy theta scores from Ch5 5.1.1

**Input:**

**File:** results/ch5/5.1.1/data/step03_theta_scores.csv
**Source:** RQ 5.1.1 (IRT calibration of accuracy responses)
**Format:** CSV with columns:
  - `composite_ID` (string, format: UID_test, e.g., P001_T1)
  - `theta_all` (float, omnibus accuracy ability estimate)
  - `se_all` (float, standard error of theta estimate)
**Expected Rows:** 400 (100 participants x 4 tests)

**Processing:**
- Load CSV into pandas DataFrame
- Verify 400 rows (100 participants x 4 tests)
- Rename theta_all to theta_accuracy, se_all to se_accuracy (for clarity in merged dataset)

**Output:**

**File:** data/step00a_accuracy_theta.csv
**Format:** CSV with columns:
  - `composite_ID` (string)
  - `theta_accuracy` (float)
  - `se_accuracy` (float)
**Expected Rows:** 400

**Validation Requirement:**
Validation tools MUST be used after data loading. Specific validation tools determined by rq_tools based on data loading requirements (file exists, expected structure).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00a_accuracy_theta.csv exists
- Expected rows: 400 (100 participants x 4 tests)
- Expected columns: 3 (composite_ID, theta_accuracy, se_accuracy)
- Data types: composite_ID (object/string), theta_accuracy (float64), se_accuracy (float64)

*Value Ranges:*
- theta_accuracy in [-3, 3] (typical IRT ability range)
- se_accuracy in [0.1, 1.0] (standard error bounds)
- composite_ID format: UID_test (e.g., P001_T1)

*Data Quality:*
- No NaN values in theta_accuracy or se_accuracy
- All 100 participants present (no data loss)
- All 4 tests per participant (T1, T2, T3, T4)
- No duplicate composite_ID values

*Log Validation:*
- Required pattern: "Loaded accuracy theta: 400 rows"
- Required pattern: "Renamed columns: theta_all -> theta_accuracy, se_all -> se_accuracy"
- Forbidden patterns: "ERROR", "Missing values detected"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 400 rows, found 387")
- Log failure to logs/step00a_load_accuracy.log
- Quit script immediately
- g_debug invoked to diagnose root cause (likely RQ 5.1.1 incomplete or corrupted output)

---

### Step 0b: Load Confidence Theta Scores

**Dependencies:** None (reads from completed RQ 6.1.1)
**Complexity:** Low (<1 minute)

**Purpose:** Load confidence theta scores from Ch6 6.1.1

**Input:**

**File:** results/ch6/6.1.1/data/step03_theta_confidence.csv
**Source:** RQ 6.1.1 (IRT calibration of confidence ratings)
**Format:** CSV with columns:
  - `composite_ID` (string, format: UID_test)
  - `theta_confidence` (float, omnibus confidence ability estimate)
  - `se_confidence` (float, standard error of theta estimate)
**Expected Rows:** 400 (100 participants x 4 tests)

**Processing:**
- Load CSV into pandas DataFrame
- Verify 400 rows (100 participants x 4 tests)
- Column names already include "_confidence" suffix (no renaming needed)

**Output:**

**File:** data/step00b_confidence_theta.csv
**Format:** CSV with columns:
  - `composite_ID` (string)
  - `theta_confidence` (float)
  - `se_confidence` (float)
**Expected Rows:** 400

**Validation Requirement:**
Validation tools MUST be used after data loading.

**Substance Validation Criteria:**

*Output Files:*
- data/step00b_confidence_theta.csv exists
- Expected rows: 400
- Expected columns: 3 (composite_ID, theta_confidence, se_confidence)
- Data types: composite_ID (object), theta_confidence (float64), se_confidence (float64)

*Value Ranges:*
- theta_confidence in [-3, 3]
- se_confidence in [0.1, 1.0]

*Data Quality:*
- No NaN values
- All 100 participants present
- All 4 tests per participant
- No duplicate composite_ID values

*Log Validation:*
- Required: "Loaded confidence theta: 400 rows"
- Forbidden: "ERROR", "Missing values"

**Expected Behavior on Validation Failure:**
- Quit with error message
- g_debug investigates RQ 6.1.1 output integrity

---

### Step 0c: Load TSVR Mapping

**Dependencies:** None (reads from completed RQ 6.1.1)
**Complexity:** Low (<1 minute)

**Purpose:** Load TSVR time variable mapping (Decision D070)

**Input:**

**File:** results/ch6/6.1.1/data/step00_tsvr_mapping.csv
**Source:** RQ 6.1.1 (TSVR extracted during confidence data preparation)
**Format:** CSV with columns:
  - `composite_ID` (string)
  - `TSVR_hours` (float, actual hours since encoding)
  - `test` (string, test session identifier: T1, T2, T3, T4)
**Expected Rows:** 400

**Processing:**
- Load CSV
- Verify TSVR_hours values are non-negative (time cannot be negative)

**Output:**

**File:** data/step00c_tsvr_mapping.csv
**Format:** CSV with columns:
  - `composite_ID` (string)
  - `TSVR_hours` (float)
  - `test` (string)
**Expected Rows:** 400

**Validation Requirement:**
Validation tools MUST be used after data loading.

**Substance Validation Criteria:**

*Output Files:*
- data/step00c_tsvr_mapping.csv exists
- Expected rows: 400
- Expected columns: 3 (composite_ID, TSVR_hours, test)
- Data types: composite_ID (object), TSVR_hours (float64), test (object)

*Value Ranges:*
- TSVR_hours >= 0 (time since encoding must be non-negative)
- TSVR_hours in [0, 168] hours approximately (0 = encoding, ~168 = 1 week for T4)
- test in {T1, T2, T3, T4}

*Data Quality:*
- No NaN values in TSVR_hours or test
- All composite_ID values unique
- All 4 tests represented (T1, T2, T3, T4)

*Log Validation:*
- Required: "Loaded TSVR mapping: 400 rows"
- Forbidden: "ERROR", "Negative TSVR values"

**Expected Behavior on Validation Failure:**
- Quit with error
- g_debug checks TSVR extraction integrity

---

### Step 1: Merge Theta Scores with TSVR

**Dependencies:** Steps 0a, 0b, 0c (requires all three input files)
**Complexity:** Low (<1 minute)

**Purpose:** Merge accuracy theta, confidence theta, and TSVR into unified dataset

**Input:**

**File 1:** data/step00a_accuracy_theta.csv
**Columns:** composite_ID, theta_accuracy, se_accuracy

**File 2:** data/step00b_confidence_theta.csv
**Columns:** composite_ID, theta_confidence, se_confidence

**File 3:** data/step00c_tsvr_mapping.csv
**Columns:** composite_ID, TSVR_hours, test

**Processing:**
- Merge all three files on composite_ID (inner join - all composite_IDs must match exactly)
- Verify 400 rows after merge (no data loss)
- Extract UID from composite_ID (split on underscore, take first part)
- Z-standardize theta_accuracy and theta_confidence BEFORE computing calibration
  - Standardization needed because theta scales may differ between accuracy and confidence IRT calibrations
  - Use pandas (theta - theta.mean()) / theta.std()
  - Store standardized values as z_theta_accuracy, z_theta_confidence

**Output:**

**File:** data/step01_merged_theta.csv
**Format:** CSV with columns:
  - `UID` (string, participant identifier extracted from composite_ID)
  - `test` (string, test session: T1, T2, T3, T4)
  - `composite_ID` (string, original UID_test identifier)
  - `TSVR_hours` (float, time since encoding)
  - `theta_accuracy` (float, raw accuracy theta)
  - `se_accuracy` (float)
  - `theta_confidence` (float, raw confidence theta)
  - `se_confidence` (float)
  - `z_theta_accuracy` (float, z-standardized accuracy theta)
  - `z_theta_confidence` (float, z-standardized confidence theta)
**Expected Rows:** 400 (100 participants x 4 tests)

**Validation Requirement:**
Validation tools MUST be used after merge operation.

**Substance Validation Criteria:**

*Output Files:*
- data/step01_merged_theta.csv exists
- Expected rows: 400 (no data loss during merge)
- Expected columns: 10 (UID, test, composite_ID, TSVR_hours, theta_accuracy, se_accuracy, theta_confidence, se_confidence, z_theta_accuracy, z_theta_confidence)
- Data types: UID (object), test (object), composite_ID (object), TSVR_hours (float64), all theta/se columns (float64)

*Value Ranges:*
- theta_accuracy, theta_confidence in [-3, 3]
- se_accuracy, se_confidence in [0.1, 1.0]
- TSVR_hours in [0, 168]
- z_theta_accuracy, z_theta_confidence approximately in [-3, 3] (z-scores)

*Data Quality:*
- No NaN values in any column
- All 100 participants present (check UID unique count = 100)
- All 4 tests per participant (check test value counts)
- Z-standardization successful: mean(z_theta_accuracy) approximately 0, std(z_theta_accuracy) approximately 1 (within 0.01 tolerance)
- Z-standardization successful: mean(z_theta_confidence) approximately 0, std(z_theta_confidence) approximately 1

*Log Validation:*
- Required: "Merged 3 files: 400 rows retained"
- Required: "Z-standardization complete: theta_accuracy (mean=0.00, sd=1.00), theta_confidence (mean=0.00, sd=1.00)"
- Forbidden: "ERROR", "Merge resulted in data loss", "NaN values detected"

**Expected Behavior on Validation Failure:**
- Quit with detailed error (which file had mismatch, how many composite_IDs unmatched)
- g_debug checks for composite_ID format inconsistencies across source RQs

---

### Step 2: Compute Calibration Metric

**Dependencies:** Step 1 (requires merged theta with z-standardization)
**Complexity:** Low (<1 minute)

**Purpose:** Compute calibration as difference between z-standardized confidence and accuracy

**Input:**

**File:** data/step01_merged_theta.csv
**Required Columns:** z_theta_accuracy, z_theta_confidence

**Processing:**
- Compute calibration metric: calibration = z_theta_confidence - z_theta_accuracy
- Positive calibration = overconfidence (confidence exceeds accuracy)
- Negative calibration = underconfidence (accuracy exceeds confidence)
- Zero calibration = perfect alignment

**Output:**

**File:** data/step02_calibration_scores.csv
**Format:** CSV with columns:
  - `UID` (string)
  - `test` (string)
  - `composite_ID` (string)
  - `TSVR_hours` (float)
  - `z_theta_accuracy` (float)
  - `z_theta_confidence` (float)
  - `calibration` (float, difference score: z_theta_confidence - z_theta_accuracy)
**Expected Rows:** 400

**Validation Requirement:**
Validation tools MUST be used after calibration computation.

**Substance Validation Criteria:**

*Output Files:*
- data/step02_calibration_scores.csv exists
- Expected rows: 400
- Expected columns: 7 (UID, test, composite_ID, TSVR_hours, z_theta_accuracy, z_theta_confidence, calibration)
- Data types: calibration (float64)

*Value Ranges:*
- calibration approximately in [-6, 6] (difference of two z-scores, typically smaller range like [-3, 3])
- z_theta_accuracy, z_theta_confidence in [-3, 3]

*Data Quality:*
- No NaN values in calibration column
- Calibration = z_theta_confidence - z_theta_accuracy (verify arithmetic for sample rows)
- Distribution check: calibration should be approximately normal with mean near 0 (if no systematic bias)

*Log Validation:*
- Required: "Calibration metric computed: 400 observations"
- Required: "Calibration range: [min, max]" (log actual range for inspection)
- Forbidden: "ERROR", "NaN in calibration"

**Expected Behavior on Validation Failure:**
- Quit with error
- g_debug checks for arithmetic errors or unexpected value ranges

---

### Step 3: Compute Brier Score

**Dependencies:** None (reads raw item-level data from dfData.csv)
**Complexity:** Medium (5-10 minutes for item-level processing across 400 observations x ~100 items)

**Purpose:** Compute Brier score at item level for calibration assessment

**Input:**

**File:** data/cache/dfData.csv
**Required Columns:**
  - `UID` (participant identifier)
  - `TEST` (test session)
  - `TQ_*` columns (item-level accuracy: 0/1)
  - `TC_*` columns (item-level confidence: 0, 0.25, 0.5, 0.75, 1.0)

**Filter:**
- Include only interactive paradigm items (IFR, ICR, IRE) matching omnibus "All" factor
- Exclude RFR, TCR, RRE per standard extraction protocol

**Processing:**
- For each participant-test-item combination:
  - Extract accuracy (TQ_* column: 0 or 1)
  - Extract confidence (TC_* column: 0, 0.25, 0.5, 0.75, or 1.0)
  - Compute squared error: (confidence - accuracy)^2
- Aggregate Brier score per participant-test: mean((confidence - accuracy)^2) across all items
- Lower Brier score indicates better calibration (confidence closer to actual accuracy)

**Output:**

**File:** data/step03_brier_scores.csv
**Format:** CSV with columns:
  - `UID` (string)
  - `TEST` (string)
  - `composite_ID` (string, UID_TEST)
  - `brier_score` (float, mean squared error across items)
  - `n_items` (int, number of items included in Brier computation)
**Expected Rows:** 400 (100 participants x 4 tests)

**Validation Requirement:**
Validation tools MUST be used after Brier computation.

**Substance Validation Criteria:**

*Output Files:*
- data/step03_brier_scores.csv exists
- Expected rows: 400
- Expected columns: 5 (UID, TEST, composite_ID, brier_score, n_items)
- Data types: brier_score (float64), n_items (int64)

*Value Ranges:*
- brier_score in [0, 1] (squared error, cannot exceed 1.0)
- n_items approximately 80-120 (depends on omnibus factor item count)
- brier_score typically in [0.1, 0.5] for reasonable calibration

*Data Quality:*
- No NaN values in brier_score
- All brier_score values >= 0 (squared error cannot be negative)
- n_items > 0 for all rows (every participant should have responded to some items)
- n_items consistent across participants (omnibus factor same for all)

*Log Validation:*
- Required: "Brier scores computed: 400 observations"
- Required: "Mean Brier score: [value]" (log descriptive statistics)
- Required: "Items per observation: [min, max, mean]"
- Forbidden: "ERROR", "Brier > 1.0 detected"

**Expected Behavior on Validation Failure:**
- Quit with error
- g_debug checks item extraction logic or confidence-accuracy alignment

---

### Step 4: Compute Expected Calibration Error (ECE)

**Dependencies:** None (reads raw item-level data from dfData.csv)
**Complexity:** Medium (5-10 minutes for binning and aggregation)

**Purpose:** Compute ECE per timepoint by binning items by confidence level

**Input:**

**File:** data/cache/dfData.csv
**Required Columns:** UID, TEST, TQ_* (accuracy), TC_* (confidence)

**Processing:**
- For each test session (T1, T2, T3, T4):
  - Bin all item-level responses by confidence level (5 bins: 0, 0.25, 0.5, 0.75, 1.0)
  - Within each bin, compute:
    - mean_confidence (should equal bin value if discretized)
    - mean_accuracy (proportion of items answered correctly in this confidence bin)
    - bin_error = abs(mean_confidence - mean_accuracy)
    - n_items_in_bin (sample size for weighting)
  - Compute ECE = weighted average of bin_error (weighted by n_items_in_bin)
- Lower ECE indicates better calibration (confidence levels align with actual accuracy)

**Output:**

**File:** data/step04_ece_by_time.csv
**Format:** CSV with columns:
  - `test` (string: T1, T2, T3, T4)
  - `ECE` (float, expected calibration error)
  - `n_items` (int, total items included across all bins)
  - `bin_0_error`, `bin_025_error`, `bin_05_error`, `bin_075_error`, `bin_1_error` (float, bin-specific errors for inspection)
**Expected Rows:** 4 (one per test session)

**Validation Requirement:**
Validation tools MUST be used after ECE computation.

**Substance Validation Criteria:**

*Output Files:*
- data/step04_ece_by_time.csv exists
- Expected rows: 4 (T1, T2, T3, T4)
- Expected columns: 9 (test, ECE, n_items, 5 bin_error columns)
- Data types: ECE (float64), n_items (int64), bin errors (float64)

*Value Ranges:*
- ECE in [0, 1] (calibration error bounded by 0-1)
- ECE typically in [0.05, 0.3] for realistic calibration patterns
- bin_*_error in [0, 1]

*Data Quality:*
- No NaN values in ECE
- test values = {T1, T2, T3, T4} (all 4 tests present)
- n_items consistent across tests (same omnibus factor)

*Log Validation:*
- Required: "ECE computed for 4 timepoints"
- Required: "ECE range: [min, max]"
- Forbidden: "ERROR", "ECE > 1.0"

**Expected Behavior on Validation Failure:**
- Quit with error
- g_debug checks binning logic or confidence-accuracy extraction

---

### Step 5: Fit LMM for Calibration Trajectory

**Dependencies:** Step 2 (requires calibration scores with TSVR)
**Complexity:** Medium-High (5-15 minutes for LMM fitting)

**Purpose:** Test whether calibration changes over time (Time effect on calibration metric)

**Input:**

**File:** data/step02_calibration_scores.csv
**Required Columns:** UID, TSVR_hours, calibration

**Processing:**
- Fit Linear Mixed Model: calibration ~ TSVR_hours + (TSVR_hours | UID)
  - Fixed effect: TSVR_hours (tests whether calibration changes over time)
  - Random effects: Random intercepts and slopes per UID (allows individual differences in calibration trajectories)
  - Time variable: TSVR_hours (actual hours since encoding per Decision D070)
- Extract model summary (fixed effects, random effects, fit indices)
- Extract Time coefficient (TSVR_hours effect on calibration)
  - Positive coefficient = calibration increases over time (worsening, increasing overconfidence)
  - Negative coefficient = calibration decreases over time (improving, decreasing overconfidence)
  - Null coefficient = calibration stable over time

**Output:**

**File:** data/step05_lmm_model_summary.txt
**Format:** Text file containing:
  - Model formula
  - Fixed effects table (coefficient, SE, z, p-value)
  - Random effects variance components
  - Model fit indices (AIC, BIC, log-likelihood)
  - Convergence status

**Validation Requirement:**
Validation tools MUST be used after LMM fitting.

**Substance Validation Criteria:**

*Output Files:*
- data/step05_lmm_model_summary.txt exists
- File size > 500 bytes (contains full model summary, not just error message)

*Value Ranges:*
- TSVR_hours coefficient typically in [-0.01, 0.01] (small effect per hour)
- Standard errors positive (SE > 0)
- p-values in [0, 1]

*Data Quality:*
- Model converged successfully (check convergence status in summary)
- Random effects variance components > 0 (no boundary estimates)
- AIC, BIC finite (not NaN or inf)

*Log Validation:*
- Required: "LMM converged: True"
- Required: "VALIDATION - PASS: LMM convergence"
- Required: "Fixed effects extracted: TSVR_hours coefficient = [value]"
- Forbidden: "ERROR", "CONVERGENCE FAILED", "Model did not converge"

**Expected Behavior on Validation Failure:**
- Quit with error message
- g_debug checks for convergence issues (potential causes: insufficient variance in calibration, collinearity, random structure too complex)

---

### Step 6: Test Time Effect with Dual P-Values

**Dependencies:** Step 5 (requires fitted LMM)
**Complexity:** Low (<1 minute)

**Purpose:** Test Time effect on calibration using dual p-value reporting (Decision D068)

**Input:**

**File:** data/step05_lmm_model_summary.txt (text file with model results)
**Derived Data:** LMM fitted model object (in memory from Step 5)

**Processing:**
- Extract TSVR_hours fixed effect from LMM
- Compute dual p-values per Decision D068:
  - Uncorrected p-value: Wald test p-value from model summary
  - Corrected p-value: Likelihood Ratio Test (LRT) comparing full model vs model without TSVR_hours
- Interpret Time effect:
  - If both p-values < 0.05: Significant Time effect (calibration changes over time)
  - If uncorrected < 0.05 but corrected >= 0.05: Marginal Time effect (interpret cautiously)
  - If both p-values >= 0.05: No significant Time effect (calibration stable)
- Report direction of effect (positive or negative coefficient)

**Output:**

**File:** data/step06_time_effect.csv
**Format:** CSV with columns:
  - `effect` (string: "TSVR_hours")
  - `coefficient` (float, Time effect size)
  - `se` (float, standard error)
  - `p_uncorrected` (float, Wald p-value)
  - `p_corrected` (float, LRT p-value)
  - `interpretation` (string: "Significant" / "Marginal" / "Not significant")
  - `direction` (string: "Positive" / "Negative" / "Null")
**Expected Rows:** 1 (single Time effect test)

**Validation Requirement:**
Validation tools MUST be used after hypothesis testing.

**Substance Validation Criteria:**

*Output Files:*
- data/step06_time_effect.csv exists
- Expected rows: 1
- Expected columns: 7 (effect, coefficient, se, p_uncorrected, p_corrected, interpretation, direction)
- Data types: coefficient (float64), se (float64), p-values (float64), strings (object)

*Value Ranges:*
- coefficient typically in [-0.01, 0.01] (small effect per hour)
- se > 0 (standard error positive)
- p_uncorrected, p_corrected in [0, 1]

*Data Quality:*
- No NaN values
- interpretation in {"Significant", "Marginal", "Not significant"}
- direction in {"Positive", "Negative", "Null"}
- Dual p-values present per Decision D068

*Log Validation:*
- Required: "VALIDATION - PASS: Dual p-values present (D068)"
- Required: "Time effect: [interpretation] ([direction])"
- Forbidden: "ERROR", "Missing p-value"

**Expected Behavior on Validation Failure:**
- Quit with error
- g_debug checks LRT computation or p-value extraction

---

### Step 7: Prepare Calibration Trajectory Plot Data

**Dependencies:** Steps 2, 5 (requires calibration scores and LMM predictions)
**Complexity:** Low (<1 minute)

**Purpose:** Create plot source CSVs for calibration trajectory visualization (Decision D069 dual-scale)

**Plot Description:** Trajectory over time showing calibration evolution from Day 0 to Day 6 with confidence bands

**Required Data Sources:**
- data/step02_calibration_scores.csv (observed calibration per person-timepoint)
- LMM fitted model from Step 5 (model predictions with confidence intervals)

**Aggregation Logic:**
1. Group calibration scores by test session (T1, T2, T3, T4)
2. Compute mean calibration per test + 95% confidence interval
3. Extract LMM predictions for mean trajectory (fitted values from model)
4. Merge observed means + model predictions + CIs
5. For theta-scale: Use raw calibration values (z-score difference)
6. For probability-scale: Transform calibration to probability metric (if applicable - may not apply for difference scores, TBD)

**Output (Plot Source CSVs):**

**File 1:** data/step07_calibration_trajectory_theta_data.csv
**Format:** CSV, plot source data for theta-scale trajectory
**Columns:**
  - `time` (float): TSVR hours (aggregated by test session)
  - `calibration` (float): Mean calibration per timepoint
  - `CI_lower` (float): Lower 95% confidence bound
  - `CI_upper` (float): Upper 95% confidence bound
  - `test` (string): Test session identifier (T1, T2, T3, T4)
**Expected Rows:** 4 (one per test session)

**Note:** Probability-scale may not be applicable for calibration difference scores. If calibration is interpreted as probability metric (e.g., via logistic transformation), create step07_calibration_trajectory_probability_data.csv. Otherwise, single theta-scale plot sufficient.

**Validation Requirement:**
Validation tools MUST be used after plot data preparation.

**Substance Validation Criteria:**

*Output Files:*
- data/step07_calibration_trajectory_theta_data.csv exists
- Expected rows: 4 (T1, T2, T3, T4)
- Expected columns: 5 (time, calibration, CI_lower, CI_upper, test)
- Data types: time (float64), calibration (float64), CI bounds (float64), test (object)

*Value Ranges:*
- time in [0, 168] hours (TSVR range)
- calibration approximately in [-3, 3] (z-score difference)
- CI_lower < CI_upper for all rows

*Data Quality:*
- No NaN values in any column
- All 4 tests represented (T1, T2, T3, T4)
- CI_upper > CI_lower (confidence bounds correctly ordered)

*Log Validation:*
- Required: "Plot data preparation complete: 4 rows created"
- Required: "All tests represented: T1, T2, T3, T4"
- Forbidden: "ERROR", "NaN values detected", "Missing test"

**Expected Behavior on Validation Failure:**
- Quit with error
- g_debug checks aggregation logic or CI computation

**Plotting Function (rq_plots will call):** Trajectory plot with confidence bands
- rq_plots reads data/step07_calibration_trajectory_theta_data.csv
- No data aggregation in rq_plots (visualization only per Option B)
- PNG output saved to plots/ folder by rq_plots

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0a-0c -> Step 1: Merge Transformation**
- Input: Three separate CSV files (accuracy, confidence, TSVR)
- Transformation: Inner join on composite_ID + extract UID + z-standardize theta scores
- Output: Unified dataset with 10 columns (identifiers + raw theta + standardized theta)

**Step 1 -> Step 2: Calibration Computation**
- Input: Z-standardized theta scores
- Transformation: Arithmetic difference (z_theta_confidence - z_theta_accuracy)
- Output: Calibration metric added as new column

**Step 2 -> Step 5: LMM Input Format**
- Input: Calibration scores in long format (one row per observation)
- Transformation: None needed (already in long format for LMM)
- Output: LMM fitted on existing long-format data

**Step 2, 5 -> Step 7: Plot Data Aggregation**
- Input: Observed calibration scores + LMM predictions
- Transformation: Group by test, compute mean + CI, merge with model predictions
- Output: Aggregated plot source CSV (4 rows)

### Column Naming Conventions

Per names.md:
- `composite_ID`: UID_test identifier (e.g., P001_T1)
- `UID`: Participant identifier (e.g., P001)
- `test`: Test session (T1, T2, T3, T4)
- `TSVR_hours`: Time since encoding in hours (Decision D070)
- `theta_accuracy`, `theta_confidence`: Raw IRT ability estimates
- `z_theta_accuracy`, `z_theta_confidence`: Z-standardized theta scores
- `calibration`: Difference score (z_theta_confidence - z_theta_accuracy)
- `CI_lower`, `CI_upper`: 95% confidence interval bounds

### Data Type Constraints

**Identifiers:**
- UID (object/string, format: P###)
- test (object/string, values: T1, T2, T3, T4)
- composite_ID (object/string, format: UID_test)

**Theta Scores:**
- theta_accuracy, theta_confidence (float64, range: [-3, 3])
- se_accuracy, se_confidence (float64, range: [0.1, 1.0])
- z_theta_accuracy, z_theta_confidence (float64, z-scores with mean=0, sd=1)

**Calibration Metrics:**
- calibration (float64, difference of z-scores)
- brier_score (float64, range: [0, 1])
- ECE (float64, range: [0, 1])

**Time Variable:**
- TSVR_hours (float64, non-negative, typically [0, 168])

**Statistical Outputs:**
- Coefficients, SE (float64, unrestricted but typically small values)
- p-values (float64, range: [0, 1])

---

## Cross-RQ Dependencies

### Dependency Type: DERIVED Data from Other RQs (Dependencies Exist)

**This RQ requires outputs from:**

- **RQ 5.1.1** (Ch5 Functional Form Comparison - Accuracy IRT)
  - File: results/ch5/5.1.1/data/step03_theta_scores.csv
  - Used in: Step 0a (load accuracy theta scores)
  - Rationale: RQ 5.1.1 provides omnibus accuracy ability estimates. This RQ uses those estimates as one component of calibration metric.

- **RQ 6.1.1** (Ch6 Confidence Model Selection - Confidence IRT)
  - File 1: results/ch6/6.1.1/data/step03_theta_confidence.csv
  - Used in: Step 0b (load confidence theta scores)
  - File 2: results/ch6/6.1.1/data/step00_tsvr_mapping.csv
  - Used in: Step 0c (load TSVR time variable)
  - Rationale: RQ 6.1.1 provides omnibus confidence ability estimates. This RQ uses those estimates as second component of calibration metric.

**Execution Order Constraint:**
1. RQ 5.1.1 must complete first (provides theta_accuracy)
2. RQ 6.1.1 must complete second (provides theta_confidence + TSVR)
3. This RQ (6.2.1) executes third (merges both theta sources)

**Data Source Boundaries:**
- **RAW data:** dfData.csv (for Brier and ECE item-level computations)
- **DERIVED data:** Theta scores from RQ 5.1.1 and RQ 6.1.1 (IRT-estimated abilities)
- **Scope:** This RQ does NOT re-calibrate IRT models. It uses existing theta estimates to compute calibration metrics and trajectory.

**Validation:**
- Step 0a: Check results/ch5/5.1.1/data/step03_theta_scores.csv exists (EXPECTATIONS ERROR if absent)
- Step 0b: Check results/ch6/6.1.1/data/step03_theta_confidence.csv exists (EXPECTATIONS ERROR if absent)
- Step 0c: Check results/ch6/6.1.1/data/step00_tsvr_mapping.csv exists (EXPECTATIONS ERROR if absent)
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
- g_code (Step 14 workflow) will generate stepNN_name.py scripts with validation function calls
- bash execution (Step 14 workflow) will run analysis -> validation -> error on validation failure

**Downstream Agent Requirements:**
- **rq_tools:** MUST specify validation tool for EVERY analysis step (no exceptions)
- **rq_analysis:** MUST embed validation tool call for EVERY analysis step (no exceptions)
- **g_code:** MUST generate code with validation function calls (no exceptions)
- **rq_inspect:** MUST verify validation ran successfully (checks logs/stepNN_name.log for validation output)

### Validation Requirements By Step

#### Step 0a: Load Accuracy Theta Scores

**Analysis Tool:** (determined by rq_tools - likely pandas read_csv + basic validation)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure)

**What Validation Checks:**
- File exists: results/ch5/5.1.1/data/step03_theta_scores.csv
- Expected structure: 400 rows x 3 columns
- Required columns: composite_ID, theta_all, se_all
- Value ranges: theta in [-3, 3], se in [0.1, 1.0]
- No NaN values in theta or se columns

**Expected Behavior on Validation Failure:**
- Raise error with specific message (e.g., "RQ 5.1.1 output file missing")
- Log failure to logs/step00a_load_accuracy.log
- Quit immediately
- g_debug investigates dependency RQ completion status

---

#### Step 0b: Load Confidence Theta Scores

**Validation Tool:** (determined by rq_tools)

**What Validation Checks:**
- File exists: results/ch6/6.1.1/data/step03_theta_confidence.csv
- Expected structure: 400 rows x 3 columns
- Required columns: composite_ID, theta_confidence, se_confidence
- Value ranges: theta in [-3, 3], se in [0.1, 1.0]
- No NaN values

**Expected Behavior on Validation Failure:**
- Quit with error (RQ 6.1.1 incomplete or corrupted)
- g_debug checks dependency

---

#### Step 0c: Load TSVR Mapping

**Validation Tool:** (determined by rq_tools)

**What Validation Checks:**
- File exists: results/ch6/6.1.1/data/step00_tsvr_mapping.csv
- Expected structure: 400 rows x 3 columns
- TSVR_hours >= 0 (non-negative time)
- test in {T1, T2, T3, T4}

**Expected Behavior on Validation Failure:**
- Quit with error
- g_debug checks TSVR extraction

---

#### Step 1: Merge Theta Scores with TSVR

**Analysis Tool:** (determined by rq_tools - likely pandas merge operations + z-standardization)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_standardization + validate_dataframe_structure)

**What Validation Checks:**
- Merge successful: 400 rows retained (no data loss)
- All required columns present
- Z-standardization successful: mean(z_theta) approximately 0, std(z_theta) approximately 1
- No NaN values after merge

**Expected Behavior on Validation Failure:**
- Quit with detailed error (which composite_IDs failed to merge)
- g_debug checks format inconsistencies

---

#### Step 2: Compute Calibration Metric

**Analysis Tool:** (determined by rq_tools - arithmetic operation)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_numeric_range)

**What Validation Checks:**
- Calibration = z_theta_confidence - z_theta_accuracy (verify arithmetic)
- Value range approximately in [-6, 6] (difference of z-scores)
- No NaN values in calibration column

**Expected Behavior on Validation Failure:**
- Quit with error
- g_debug checks computation

---

#### Step 3: Compute Brier Score

**Analysis Tool:** (determined by rq_tools - item-level extraction + squared error computation)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_probability_range for Brier in [0,1])

**What Validation Checks:**
- Brier score in [0, 1] (squared error bounded)
- All 400 observations present
- n_items > 0 for all rows

**Expected Behavior on Validation Failure:**
- Quit with error
- g_debug checks item extraction or Brier computation

---

#### Step 4: Compute ECE

**Analysis Tool:** (determined by rq_tools - binning + weighted error)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_numeric_range for ECE in [0,1])

**What Validation Checks:**
- ECE in [0, 1]
- All 4 tests present (T1, T2, T3, T4)
- Bin errors in [0, 1]

**Expected Behavior on Validation Failure:**
- Quit with error
- g_debug checks binning logic

---

#### Step 5: Fit LMM for Calibration Trajectory

**Analysis Tool:** (determined by rq_tools - likely tools.lmm.fit_lmm_trajectory_tsvr)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_lmm_convergence + validate_lmm_assumptions_comprehensive)

**What Validation Checks:**
- Model converged successfully
- Random effects variance components > 0
- Residuals approximately normal (diagnostic plots)
- AIC, BIC finite (not NaN or inf)

**Expected Behavior on Validation Failure:**
- Quit with error (convergence failure)
- g_debug checks for insufficient variance, collinearity, or overparameterized random structure

---

#### Step 6: Test Time Effect with Dual P-Values

**Analysis Tool:** (determined by rq_tools - likely tools.lmm.extract_fixed_effects + LRT comparison)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_hypothesis_test_dual_pvalues per D068)

**What Validation Checks:**
- Dual p-values present (uncorrected + corrected per D068)
- p-values in [0, 1]
- Coefficient, SE extracted correctly

**Expected Behavior on Validation Failure:**
- Quit with error (missing p-value or invalid range)
- g_debug checks LRT computation

---

#### Step 7: Prepare Plot Data

**Analysis Tool:** (determined by rq_tools - aggregation + CI computation)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_plot_data_completeness)

**What Validation Checks:**
- All 4 tests represented (T1, T2, T3, T4)
- CI_upper > CI_lower for all rows
- No NaN values

**Expected Behavior on Validation Failure:**
- Quit with error (missing test or invalid CI)
- g_debug checks aggregation

---

## Summary

**Total Steps:** 7 (Steps 0a-0c, 1-7)

**Estimated Runtime:** Medium (20-30 minutes total - Steps 3, 4, 5 are Medium complexity)

**Cross-RQ Dependencies:** 2 dependency RQs (5.1.1, 6.1.1)

**Primary Outputs:**
- data/step02_calibration_scores.csv (calibration metric per person-timepoint)
- data/step03_brier_scores.csv (item-level calibration metric)
- data/step04_ece_by_time.csv (ECE per timepoint)
- data/step05_lmm_model_summary.txt (LMM trajectory results)
- data/step06_time_effect.csv (Time effect with dual p-values)
- data/step07_calibration_trajectory_theta_data.csv (plot source data)

**Validation Coverage:** 100% (all 7 steps + 3 sub-steps have validation requirements)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent for RQ 6.2.1
