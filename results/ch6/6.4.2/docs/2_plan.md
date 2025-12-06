# Analysis Plan for RQ 6.4.2: Paradigm Confidence Calibration

**Created by:** rq_planner agent
**Date:** 2025-12-06
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This RQ examines calibration (confidence-accuracy alignment) across three retrieval paradigms (Free Recall, Cued Recall, Recognition). The analysis tests whether retrieval support systematically affects metacognitive accuracy, with Recognition predicted to show highest overconfidence due to fluency-familiarity heuristic.

**Pipeline:** DERIVED data merge -> Calibration computation -> LMM analysis -> Post-hoc contrasts
**Steps:** 5 analysis steps (Step 0: merge, Steps 1-4: calibration computation, LMM, contrasts, plot preparation)
**Estimated Runtime:** Low-Medium (no IRT calibration, primarily data merging and LMM fitting)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni for contrasts)
- Decision D070: TSVR as time variable (actual hours, not nominal days - inherited from source RQs)

**Data Sources:**
- RQ 5.3.1: Accuracy theta estimates by paradigm (IFR, ICR, IRE)
- RQ 6.4.1: Confidence theta estimates by paradigm (IFR, ICR, IRE)
- Both sources provide 1200 observations (100 participants x 4 tests x 3 paradigms)

---

## Analysis Plan

### Step 0: Merge Accuracy and Confidence Theta Estimates

**Dependencies:** None (first step)
**Complexity:** Low (data merging only)

**Purpose:** Combine accuracy theta (from Ch5 5.3.1) and confidence theta (from Ch6 6.4.1) to create calibration dataset.

**Input:**

**File 1:** results/ch5/5.3.1/data/step03_theta_accuracy_paradigm.csv
**Source:** RQ 5.3.1 (Paradigm Accuracy Trajectories)
**Format:** CSV with columns:
  - `UID` (string, format: P### with leading zeros)
  - `test` (string, values: {T1, T2, T3, T4} for Days 0, 1, 3, 6)
  - `paradigm` (string, values: {IFR, ICR, IRE})
  - `theta_accuracy` (float, IRT ability estimate for accuracy, range: -3 to 3)
  - `se_accuracy` (float, standard error, range: 0.1 to 1.0)
  - `TSVR_hours` (float, time since encoding in hours, Decision D070)
**Expected Rows:** 1200 (100 participants x 4 tests x 3 paradigms)

**File 2:** results/ch6/6.4.1/data/step03_theta_confidence_paradigm.csv
**Source:** RQ 6.4.1 (Paradigm Confidence Trajectories)
**Format:** CSV with columns:
  - `UID` (string, format: P### with leading zeros)
  - `test` (string, values: {T1, T2, T3, T4})
  - `paradigm` (string, values: {IFR, ICR, IRE})
  - `theta_confidence` (float, IRT ability estimate for confidence, range: -3 to 3)
  - `se_confidence` (float, standard error, range: 0.1 to 1.0)
  - `TSVR_hours` (float, time since encoding in hours, Decision D070)
**Expected Rows:** 1200 (100 participants x 4 tests x 3 paradigms)

**Processing:**
1. Read both CSV files
2. Merge on (UID, test, paradigm) - inner join (must match exactly)
3. Verify TSVR_hours values match between files (same participant-test-paradigm should have same TSVR)
4. Retain columns: UID, test, paradigm, TSVR_hours, theta_accuracy, se_accuracy, theta_confidence, se_confidence

**Output:**

**File:** data/step00_merged_accuracy_confidence.csv
**Format:** CSV, one row per participant-test-paradigm observation
**Columns:**
  - `UID` (string, participant identifier)
  - `test` (string, test session T1-T4)
  - `paradigm` (string, IFR/ICR/IRE)
  - `TSVR_hours` (float, time since encoding)
  - `theta_accuracy` (float, accuracy IRT estimate)
  - `se_accuracy` (float, accuracy standard error)
  - `theta_confidence` (float, confidence IRT estimate)
  - `se_confidence` (float, confidence standard error)
**Expected Rows:** 1200 (all observations matched)

**Validation Requirement:**
Validation tools MUST be used after data merge execution. Specific validation tools will be determined by rq_tools based on data merge requirements (likely validate_data_format, validate_dataframe_structure).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_merged_accuracy_confidence.csv exists (exact path)
- Expected rows: 1200 (100 participants x 4 tests x 3 paradigms)
- Expected columns: 8 (UID, test, paradigm, TSVR_hours, theta_accuracy, se_accuracy, theta_confidence, se_confidence)
- Data types: UID (object), test (object), paradigm (object), TSVR_hours (float64), theta_accuracy (float64), se_accuracy (float64), theta_confidence (float64), se_confidence (float64)

*Value Ranges:*
- theta_accuracy in [-3, 3] (typical IRT ability range)
- theta_confidence in [-3, 3] (typical IRT ability range)
- se_accuracy in [0.1, 1.0] (above 1.0 = unreliable, below 0.1 = suspicious)
- se_confidence in [0.1, 1.0] (above 1.0 = unreliable, below 0.1 = suspicious)
- TSVR_hours in [0, 168] hours (0=encoding, 168=1 week)
- paradigm in {IFR, ICR, IRE} (categorical)
- test in {T1, T2, T3, T4} (categorical)

*Data Quality:*
- No NaN values tolerated in theta columns (all participants must have estimates)
- No NaN values in TSVR_hours (time variable required for LMM)
- Expected N: Exactly 1200 rows (no data loss during merge)
- No duplicate (UID, test, paradigm) combinations
- All 100 participants present with 4 tests x 3 paradigms each

*Log Validation:*
- Required pattern: "Merge complete: 1200 rows created"
- Required pattern: "All paradigms represented: IFR, ICR, IRE"
- Required pattern: "TSVR_hours verification: all values matched"
- Forbidden patterns: "ERROR", "Merge key mismatch", "Missing observations"
- Acceptable warnings: None expected for data merge

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 1200 rows, found 1150 - missing data")
- Log failure to logs/step00_merge_accuracy_confidence.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose merge key mismatches or missing data

---

### Step 1: Compute Calibration Metric by Paradigm

**Dependencies:** Step 0 (requires merged accuracy-confidence data)
**Complexity:** Low (standardization and subtraction)

**Purpose:** Compute calibration as difference between confidence and accuracy on comparable z-score scales.

**Input:**

**File:** data/step00_merged_accuracy_confidence.csv
**Source:** Generated by Step 0
**Format:** CSV with 1200 rows, 8 columns (UID, test, paradigm, TSVR_hours, theta_accuracy, se_accuracy, theta_confidence, se_confidence)

**Processing:**
1. Z-standardize theta_accuracy across all observations (mean=0, SD=1)
2. Z-standardize theta_confidence across all observations (mean=0, SD=1)
3. Compute calibration: `calibration = z_confidence - z_accuracy`
4. Positive calibration = overconfidence (confidence exceeds accuracy)
5. Negative calibration = underconfidence (confidence below accuracy)
6. Calibration = 0 = perfect calibration (confidence matches accuracy)

**Output:**

**File:** data/step01_calibration_by_paradigm.csv
**Format:** CSV, one row per participant-test-paradigm observation
**Columns:**
  - `UID` (string, participant identifier)
  - `test` (string, test session T1-T4)
  - `paradigm` (string, IFR/ICR/IRE)
  - `TSVR_hours` (float, time since encoding)
  - `theta_accuracy` (float, raw accuracy IRT estimate)
  - `theta_confidence` (float, raw confidence IRT estimate)
  - `z_accuracy` (float, standardized accuracy, mean=0, SD=1)
  - `z_confidence` (float, standardized confidence, mean=0, SD=1)
  - `calibration` (float, z_confidence - z_accuracy, range: typically -3 to 3)
**Expected Rows:** 1200

**Validation Requirement:**
Validation tools MUST be used after calibration computation. Specific validation tools will be determined by rq_tools (likely validate_standardization, validate_numeric_range).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_calibration_by_paradigm.csv exists (exact path)
- Expected rows: 1200 (same as input)
- Expected columns: 9 (UID, test, paradigm, TSVR_hours, theta_accuracy, theta_confidence, z_accuracy, z_confidence, calibration)
- Data types: UID (object), test (object), paradigm (object), TSVR_hours (float64), theta_accuracy (float64), theta_confidence (float64), z_accuracy (float64), z_confidence (float64), calibration (float64)

*Value Ranges:*
- z_accuracy: mean approximately 0 (tolerance: -0.1 to 0.1), SD approximately 1 (tolerance: 0.9 to 1.1)
- z_confidence: mean approximately 0 (tolerance: -0.1 to 0.1), SD approximately 1 (tolerance: 0.9 to 1.1)
- calibration in [-4, 4] (extreme values possible but rare, >4 suggests computation error)

*Data Quality:*
- No NaN values in calibration column (all observations must have valid calibration)
- Expected N: Exactly 1200 rows (no data loss)
- Distribution check: calibration approximately normal (visual inspection in plots)
- Standardization check: z_accuracy and z_confidence meet standardization criteria (mean=0, SD=1)

*Log Validation:*
- Required pattern: "Calibration computed: 1200 observations"
- Required pattern: "z_accuracy: mean=0.00, SD=1.00"
- Required pattern: "z_confidence: mean=0.00, SD=1.00"
- Forbidden patterns: "ERROR", "NaN values detected in calibration", "Standardization failed"
- Acceptable warnings: "Slight deviation from SD=1.00 (0.98-1.02 range acceptable due to finite sample)"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "z_accuracy mean=0.23, expected 0.00 +/- 0.1")
- Log failure to logs/step01_compute_calibration.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose standardization issues

---

### Step 2: Fit LMM Testing Paradigm x Time Effects on Calibration

**Dependencies:** Step 1 (requires calibration metric)
**Complexity:** Medium (LMM model fitting, 5-10 minutes)

**Purpose:** Test whether calibration differs across paradigms and changes over time using Linear Mixed Model.

**Input:**

**File:** data/step01_calibration_by_paradigm.csv
**Source:** Generated by Step 1
**Format:** CSV with 1200 rows, 9 columns (includes calibration column)

**Processing:**
1. Prepare LMM input: long format with repeated measures (4 tests per participant x 3 paradigms)
2. Fit LMM: `calibration ~ paradigm * TSVR_hours + (TSVR_hours | UID)`
   - Fixed effects: paradigm (IFR, ICR, IRE), TSVR_hours, paradigm x TSVR_hours interaction
   - Random effects: participant-specific intercepts and slopes (TSVR_hours | UID)
3. Use TSVR_hours as time variable (Decision D070 - actual hours, not nominal days)
4. Extract fixed effects table (coefficients, SE, z-values, p-values)
5. Extract random effects variance components (between-participant variability)

**Output:**

**File 1:** data/step02_lmm_calibration_summary.txt
**Format:** Plain text model summary
**Contents:**
- Fixed effects table (paradigm coefficients, time slope, interaction terms)
- Random effects variance components
- Model fit indices (AIC, BIC, log-likelihood)
- Convergence status

**File 2:** data/step02_lmm_fixed_effects.csv
**Format:** CSV with fixed effects estimates
**Columns:**
  - `term` (string, e.g., "paradigmICR", "TSVR_hours", "paradigmICR:TSVR_hours")
  - `estimate` (float, coefficient value)
  - `se` (float, standard error)
  - `z_value` (float, test statistic)
  - `p_value` (float, uncorrected p-value)
**Expected Rows:** ~7 terms (Intercept, 2 paradigm dummies, TSVR_hours, 2 interactions)

**Validation Requirement:**
Validation tools MUST be used after LMM fitting. Specific validation tools will be determined by rq_tools (likely validate_lmm_convergence, validate_lmm_assumptions_comprehensive).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_lmm_calibration_summary.txt exists (exact path)
- data/step02_lmm_fixed_effects.csv exists (exact path)
- Expected rows in fixed effects: 6-8 (Intercept, paradigm main effects, time, interactions)
- Data types: term (object), estimate (float64), se (float64), z_value (float64), p_value (float64)

*Value Ranges:*
- estimate: unrestricted (calibration can be positive or negative)
- se > 0 (standard errors must be positive)
- p_value in [0, 1] (probability bounds)
- z_value: typically in [-5, 5] (extreme values >10 suggest estimation issues)

*Data Quality:*
- No NaN values in fixed effects table
- Model converged: convergence status = True
- Fixed effects include all expected terms: paradigm main effects, TSVR_hours, paradigm x TSVR_hours interactions
- Random effects variance components > 0 (no singular fit)

*Log Validation:*
- Required pattern: "Model converged: True"
- Required pattern: "Fixed effects extracted: [N] terms"
- Required pattern: "VALIDATION - PASS: LMM convergence"
- Required pattern: "VALIDATION - PASS: LMM assumptions"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "Singular fit detected", "NaN coefficients"
- Acceptable warnings: "Optimizer message: CONVERGENCE: REL_REDUCTION_OF_F <= FACTR*EPSMCH" (this is success message)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Model failed to converge after 200 iterations")
- Log failure to logs/step02_fit_lmm_calibration.log
- Quit script immediately (do NOT proceed to Step 3)
- g_debug invoked to diagnose convergence issues (common causes: scaling problems, insufficient data)

---

### Step 3: Compute Paradigm Contrasts with Dual P-Values

**Dependencies:** Step 2 (requires LMM fixed effects)
**Complexity:** Low (post-hoc contrast computation)

**Purpose:** Test specific paradigm comparisons with dual p-value reporting per Decision D068.

**Input:**

**File:** data/step02_lmm_calibration_summary.txt (contains fitted LMM model object path or refit from summary)
**Source:** Generated by Step 2
**Format:** Plain text with model summary

**Processing:**
1. Compute pairwise contrasts for paradigm main effects:
   - Recognition (IRE) vs Free Recall (IFR)
   - Cued Recall (ICR) vs Free Recall (IFR)
   - Recognition (IRE) vs Cued Recall (ICR)
2. Extract contrast estimates, standard errors, z-values
3. Compute uncorrected p-values
4. Compute Bonferroni-corrected p-values (multiply by number of contrasts = 3)
5. Decision D068: Report BOTH uncorrected and Bonferroni p-values

**Output:**

**File:** data/step03_paradigm_contrasts.csv
**Format:** CSV with pairwise contrasts
**Columns:**
  - `contrast` (string, e.g., "IRE - IFR", "ICR - IFR", "IRE - ICR")
  - `estimate` (float, difference in calibration between paradigms)
  - `se` (float, standard error of contrast)
  - `z_value` (float, test statistic)
  - `p_uncorrected` (float, uncorrected p-value per Decision D068)
  - `p_bonferroni` (float, Bonferroni-corrected p-value per Decision D068)
  - `significant_uncorrected` (bool, p_uncorrected < 0.05)
  - `significant_bonferroni` (bool, p_bonferroni < 0.05)
**Expected Rows:** 3 contrasts

**Validation Requirement:**
Validation tools MUST be used after contrast computation. Specific validation tools will be determined by rq_tools (likely validate_contrasts_dual_pvalues per Decision D068).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_paradigm_contrasts.csv exists (exact path)
- Expected rows: 3 (all pairwise paradigm comparisons)
- Expected columns: 8 (contrast, estimate, se, z_value, p_uncorrected, p_bonferroni, significant_uncorrected, significant_bonferroni)
- Data types: contrast (object), estimate (float64), se (float64), z_value (float64), p_uncorrected (float64), p_bonferroni (float64), significant_uncorrected (bool), significant_bonferroni (bool)

*Value Ranges:*
- estimate: unrestricted (calibration differences can be positive or negative)
- se > 0 (standard errors must be positive)
- p_uncorrected in [0, 1] (probability bounds)
- p_bonferroni in [0, 1] (Bonferroni correction can exceed 1.0, capped at 1.0)
- z_value: typically in [-5, 5] (extreme values >10 suggest computation issues)

*Data Quality:*
- No NaN values in any column
- All 3 expected contrasts present (IRE-IFR, ICR-IFR, IRE-ICR)
- Decision D068 requirement: BOTH p_uncorrected AND p_bonferroni columns present
- p_bonferroni >= p_uncorrected for all contrasts (correction cannot decrease p-value)

*Log Validation:*
- Required pattern: "Contrasts computed: 3 comparisons"
- Required pattern: "VALIDATION - PASS: Dual p-values (uncorrected + bonferroni)"
- Forbidden patterns: "ERROR", "NaN in contrasts", "Missing p-value column"
- Acceptable warnings: "Bonferroni correction very conservative (3 comparisons only)"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Missing p_bonferroni column - Decision D068 violated")
- Log failure to logs/step03_compute_contrasts.log
- Quit script immediately (do NOT proceed to Step 4)
- g_debug invoked to diagnose contrast computation issues

---

### Step 4: Prepare Calibration by Paradigm Plot Data

**Dependencies:** Steps 1, 2 (requires calibration data and LMM predictions)
**Complexity:** Low (data aggregation for plotting)

**Purpose:** Create plot source CSV for trajectory visualization showing calibration by paradigm over time (Option B architecture).

**Plot Description:** Trajectory over time with confidence bands showing calibration (confidence - accuracy) across three retrieval paradigms (IFR, ICR, IRE).

**Required Data Sources:**
- data/step01_calibration_by_paradigm.csv (columns: UID, test, paradigm, TSVR_hours, calibration)
- data/step02_lmm_calibration_summary.txt (LMM fitted model for predictions)

**Output (Plot Source CSV):** data/step04_calibration_paradigm_plot_data.csv

**Required Columns:**
- `paradigm` (string): Paradigm grouping (IFR, ICR, IRE)
- `TSVR_hours` (float): Time since encoding (0, 24, 72, 144 for T1-T4)
- `calibration_mean` (float): Mean calibration per paradigm per timepoint
- `CI_lower` (float): Lower 95% confidence bound
- `CI_upper` (float): Upper 95% confidence bound

**Expected Rows:** 12 (3 paradigms x 4 timepoints)

**Aggregation Logic:**
1. Group calibration data by paradigm + test
2. Compute mean(calibration) and 95% CI per group
3. Map test to TSVR_hours (T1=0, T2=24, T3=72, T4=144 - approximate, use actual TSVR means)
4. Optionally add LMM-predicted values for smooth trajectories
5. Select and rename columns to match required schema
6. Sort by paradigm, then TSVR_hours
7. Save to data/step04_calibration_paradigm_plot_data.csv

**Validation Requirement:**
Validation tools MUST be used after plot data preparation tool execution. Specific validation tools determined by rq_tools based on plot data format requirements (likely validate_plot_data_completeness, validate_dataframe_structure).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_calibration_paradigm_plot_data.csv exists (exact path)
- Expected rows: 12 (3 paradigms x 4 timepoints)
- Expected columns: 5 (paradigm, TSVR_hours, calibration_mean, CI_lower, CI_upper)
- Data types: paradigm (object), TSVR_hours (float64), calibration_mean (float64), CI_lower (float64), CI_upper (float64)

*Value Ranges:*
- TSVR_hours in [0, 168] hours (0=encoding, 168=1 week)
- calibration_mean: typically in [-2, 2] (z-score differences, extreme values >3 rare)
- CI_lower in [-3, 3] (confidence bounds)
- CI_upper in [-3, 3] (confidence bounds)
- paradigm in {IFR, ICR, IRE} (categorical)

*Data Quality:*
- No NaN values tolerated (all cells must have valid values)
- Expected N: Exactly 12 rows (no more, no less)
- No duplicate (paradigm, TSVR_hours) combinations
- Distribution check: CI_upper > CI_lower for all rows
- All 3 paradigms represented: IFR, ICR, IRE

*Log Validation:*
- Required pattern: "Plot data preparation complete: 12 rows created"
- Required pattern: "All paradigms represented: IFR, ICR, IRE"
- Required pattern: "VALIDATION - PASS: Plot data completeness"
- Forbidden patterns: "ERROR", "NaN values detected", "Missing paradigm"
- Acceptable warnings: None expected for plot data preparation

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 12 rows, found 9 - missing timepoint")
- Log failure to logs/step04_prepare_plot_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- g_debug invoked to diagnose aggregation issues

**Plotting Function (rq_plots will call):** Trajectory plot with confidence bands
- rq_plots agent maps this description to tools/plots.py::plot_trajectory function
- Plot reads data/step04_calibration_paradigm_plot_data.csv (created by this step)
- No data aggregation in rq_plots (visualization only per Option B)
- PNG output saved to plots/ folder by rq_plots

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 -> Step 1 Transformation:**
- Input: Two separate CSV files (accuracy theta, confidence theta)
- Merge: Inner join on (UID, test, paradigm)
- Output: Single CSV with both theta_accuracy and theta_confidence columns
- Format unchanged: Long format, one row per participant-test-paradigm observation

**Step 1 -> Step 2 Transformation:**
- Input: Calibration CSV with raw and z-standardized scores
- Processing: No format change (already in long format suitable for LMM)
- Output: LMM fitted model object and summary tables
- Format unchanged: Long format retained

**Step 2 -> Step 3 Transformation:**
- Input: LMM fixed effects table
- Processing: Pairwise contrast computation (3 comparisons)
- Output: Contrast results CSV (3 rows, one per comparison)
- Format change: Aggregated from model-level to contrast-level

**Step 3 -> Step 4 Transformation:**
- Input: Calibration data (from Step 1) + LMM predictions (from Step 2)
- Processing: Group by paradigm x timepoint, compute means and CIs
- Output: Plot source CSV (12 rows: 3 paradigms x 4 timepoints)
- Format change: Aggregated from observation-level to group-means-level

### Column Naming Conventions

Per names.md conventions:
- `UID`: Participant identifier (format: P### with leading zeros)
- `test`: Test session (T1, T2, T3, T4)
- `TSVR_hours`: Time Since VR in hours (Decision D070)
- `theta_accuracy`: IRT ability estimate for accuracy
- `theta_confidence`: IRT ability estimate for confidence
- `z_accuracy`: Standardized accuracy (mean=0, SD=1)
- `z_confidence`: Standardized confidence (mean=0, SD=1)
- `calibration`: z_confidence - z_accuracy (difference metric)
- `paradigm`: Retrieval paradigm (IFR, ICR, IRE)
- `CI_lower`, `CI_upper`: 95% confidence interval bounds for plots

### Data Type Constraints

**Nullable columns:** None (all columns required for analysis)

**Non-nullable columns:** All 9 columns in step01_calibration_by_paradigm.csv must be non-null

**Valid ranges documented in Validation sections above**

**Categorical values:**
- `paradigm`: {IFR, ICR, IRE} (no other values allowed)
- `test`: {T1, T2, T3, T4} (no other values allowed)

---

## Cross-RQ Dependencies

### Dependency Type: DERIVED Data from Other RQs (Dependencies Exist)

**This RQ requires outputs from:**

- **RQ 5.3.1** (Paradigm Accuracy Trajectories)
  - File: results/ch5/5.3.1/data/step03_theta_accuracy_paradigm.csv
  - Used in: Step 0 (merge with confidence theta)
  - Rationale: RQ 5.3.1 provides accuracy IRT estimates by paradigm. This RQ compares accuracy against confidence to compute calibration metric.

- **RQ 6.4.1** (Paradigm Confidence Trajectories)
  - File: results/ch6/6.4.1/data/step03_theta_confidence_paradigm.csv
  - Used in: Step 0 (merge with accuracy theta)
  - Rationale: RQ 6.4.1 provides confidence IRT estimates by paradigm. This RQ compares confidence against accuracy to compute calibration metric.

**Execution Order Constraint:**
1. RQ 5.3.1 must complete first (provides theta_accuracy_paradigm.csv)
2. RQ 6.4.1 must complete second (provides theta_confidence_paradigm.csv)
3. This RQ executes third (merges both outputs)

**Data Source Boundaries:**
- **RAW data:** None (this RQ uses only DERIVED data from other RQs)
- **DERIVED data:** Theta estimates from RQ 5.3.1 and RQ 6.4.1 (IRT calibrations already complete)
- **Scope:** This RQ does NOT perform IRT calibration (uses pre-computed theta estimates from source RQs)

**Validation:**
- Step 0: Check results/ch5/5.3.1/data/step03_theta_accuracy_paradigm.csv exists (EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch6/6.4.1/data/step03_theta_confidence_paradigm.csv exists (EXPECTATIONS ERROR if absent)
- Step 0: Verify both files have exactly 1200 rows (100 participants x 4 tests x 3 paradigms)
- Step 0: Verify matching (UID, test, paradigm) keys between files (merge should produce 1200 rows, no data loss)
- If either file missing -> quit with error -> user must execute dependency RQs first

---

## Validation Requirements

**CRITICAL MANDATE:**

Every analysis step in this plan MUST use validation tools after analysis tool execution.

This is not optional. This is the core architectural principle preventing cascading failures observed in v3.0 (where analysis errors propagated undetected through 5+ downstream steps before discovery).

**Exact Specification Requirement:**

> "Validation tools MUST be used after analysis tool execution"

**Implementation:**
- rq_tools (Step 11 workflow) will read tools_inventory.md validation tools section
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

#### Step 0: Merge Accuracy and Confidence Theta Estimates

**Analysis Tool:** (determined by rq_tools - likely pandas merge operations)
**Validation Tool:** (determined by rq_tools - likely validate_data_format, validate_dataframe_structure)

**What Validation Checks:**
- Output file exists (data/step00_merged_accuracy_confidence.csv)
- Expected row count (1200 rows: 100 participants x 4 tests x 3 paradigms)
- Expected column count (8 columns: UID, test, paradigm, TSVR_hours, theta_accuracy, se_accuracy, theta_confidence, se_confidence)
- No NaN values in theta columns (all observations must have estimates)
- Merge completeness (all 1200 expected observations matched)
- TSVR_hours consistency (values match between source files)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 1200 rows, found 1150 - missing data")
- Log failure to logs/step00_merge_accuracy_confidence.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked by master to diagnose merge key mismatches or missing data

---

#### Step 1: Compute Calibration Metric by Paradigm

**Analysis Tool:** (determined by rq_tools - likely pandas standardization + subtraction)
**Validation Tool:** (determined by rq_tools - likely validate_standardization, validate_numeric_range)

**What Validation Checks:**
- Output file exists (data/step01_calibration_by_paradigm.csv)
- Expected row count (1200 rows, same as input)
- Standardization successful: z_accuracy and z_confidence have mean=0, SD=1 (tolerance +/- 0.1)
- Calibration computed for all observations (no NaN values)
- Calibration values in reasonable range (typically -4 to 4)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "z_accuracy mean=0.23, expected 0.00 +/- 0.1")
- Log failure to logs/step01_compute_calibration.log
- Quit script immediately
- g_debug invoked to diagnose standardization issues

---

#### Step 2: Fit LMM Testing Paradigm x Time Effects on Calibration

**Analysis Tool:** (determined by rq_tools - likely fit_lmm_trajectory_tsvr)
**Validation Tool:** (determined by rq_tools - likely validate_lmm_convergence, validate_lmm_assumptions_comprehensive)

**What Validation Checks:**
- Output files exist (data/step02_lmm_calibration_summary.txt, data/step02_lmm_fixed_effects.csv)
- Model converged (convergence status = True)
- Fixed effects table has all expected terms (paradigm main effects, TSVR_hours, interactions)
- No NaN coefficients (estimation succeeded)
- Random effects variance components > 0 (no singular fit)
- Residuals pass normality test (LMM assumptions)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Model failed to converge after 200 iterations")
- Log failure to logs/step02_fit_lmm_calibration.log
- Quit script immediately
- g_debug invoked to diagnose convergence issues

---

#### Step 3: Compute Paradigm Contrasts with Dual P-Values

**Analysis Tool:** (determined by rq_tools - likely compute_contrasts_pairwise)
**Validation Tool:** (determined by rq_tools - likely validate_contrasts_dual_pvalues per Decision D068)

**What Validation Checks:**
- Output file exists (data/step03_paradigm_contrasts.csv)
- Expected row count (3 contrasts: IRE-IFR, ICR-IFR, IRE-ICR)
- Decision D068 requirement: BOTH p_uncorrected AND p_bonferroni columns present
- No NaN values in any column
- p_bonferroni >= p_uncorrected for all contrasts (correction cannot decrease p-value)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Missing p_bonferroni column - Decision D068 violated")
- Log failure to logs/step03_compute_contrasts.log
- Quit script immediately
- g_debug invoked to diagnose contrast computation issues

---

#### Step 4: Prepare Calibration by Paradigm Plot Data

**Analysis Tool:** (determined by rq_tools - likely pandas groupby + aggregation)
**Validation Tool:** (determined by rq_tools - likely validate_plot_data_completeness, validate_dataframe_structure)

**What Validation Checks:**
- Output file exists (data/step04_calibration_paradigm_plot_data.csv)
- Expected row count (12 rows: 3 paradigms x 4 timepoints)
- Expected column count (5 columns: paradigm, TSVR_hours, calibration_mean, CI_lower, CI_upper)
- All paradigms represented (IFR, ICR, IRE)
- No NaN values (all cells must have valid values)
- CI_upper > CI_lower for all rows (logical consistency)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Expected 12 rows, found 9 - missing timepoint")
- Log failure to logs/step04_prepare_plot_data.log
- Quit script immediately
- g_debug invoked to diagnose aggregation issues

---

## Summary

**Total Steps:** 5 (Step 0: merge, Steps 1-4: calibration computation, LMM, contrasts, plot preparation)
**Estimated Runtime:** Low-Medium (30-60 minutes total: merge <5 min, calibration <5 min, LMM 10-20 min, contrasts <5 min, plot prep <5 min)
**Cross-RQ Dependencies:** 2 (RQ 5.3.1 accuracy theta, RQ 6.4.1 confidence theta)
**Primary Outputs:**
- data/step01_calibration_by_paradigm.csv (1200 observations with calibration metric)
- data/step02_lmm_fixed_effects.csv (paradigm x time effects on calibration)
- data/step03_paradigm_contrasts.csv (3 pairwise paradigm comparisons with dual p-values)
- data/step04_calibration_paradigm_plot_data.csv (plot source CSV for trajectory visualization)
**Validation Coverage:** 100% (all 5 steps have validation requirements with 4-layer substance criteria)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 10 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent for RQ 6.4.2 (Paradigm Confidence Calibration)
