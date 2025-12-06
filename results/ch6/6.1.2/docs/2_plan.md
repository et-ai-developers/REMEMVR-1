# Analysis Plan for RQ 6.1.2: Two-Phase Pattern in Confidence Decline

**Created by:** rq_planner agent
**Date:** 2025-12-06
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

RQ 6.1.2 tests whether confidence trajectories exhibit the same two-phase pattern (rapid early decline, slower late decline) observed for accuracy in Chapter 5 RQ 5.1.2. The analysis uses IRT-derived theta confidence scores from RQ 6.1.1 and tests three statistical criteria for two-phase pattern detection: (1) significant quadratic term, (2) piecewise model superiority over continuous model, and (3) Late/Early slope ratio < 0.5.

**Pipeline:** LMM trajectory analysis with piecewise time segments

**Steps:** 7 total analysis steps (Step 0: Data loading + Steps 1-6: Analysis and plot preparation)

**Estimated Runtime:** Low to Medium (~15-30 minutes total)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni correction for hypothesis tests)
- Decision D070: TSVR as time variable (actual hours since encoding, not nominal days)
- Decision D069: Dual-scale trajectory plots (theta scale + probability scale)

**Cross-RQ Dependencies:**
- RQ 6.1.1: Provides theta_confidence scores (IRT-derived confidence ability estimates from 5-category GRM)
- RQ 5.1.2: Provides accuracy two-phase pattern comparison benchmark

---

## Analysis Plan

### Step 0: Load Theta Confidence Scores

**Dependencies:** None (first step)
**Complexity:** Low (<5 minutes)

**Purpose:** Load IRT-derived confidence ability estimates from RQ 6.1.1 and merge with TSVR time mapping.

**Input:**

**File 1:** results/ch6/6.1.1/data/step03_theta_confidence.csv
**Source:** RQ 6.1.1 Step 3 (Pass 2 IRT calibration on confidence data)
**Format:** CSV with columns:
  - `composite_ID` (string, format: UID_test, e.g., P001_T1)
  - `theta_confidence` (float, IRT ability estimate for confidence)
  - `se_confidence` (float, standard error of theta estimate)
**Expected Rows:** ~400 (100 participants x 4 tests)

**File 2:** results/ch6/6.1.1/data/step00_tsvr_mapping.csv
**Source:** RQ 6.1.1 Step 0 (TSVR extraction from master.xlsx)
**Format:** CSV with columns:
  - `UID` (string, participant identifier, e.g., P001)
  - `test` (string, test session identifier, e.g., T1, T2, T3, T4)
  - `TSVR_hours` (float, actual hours since VR encoding session)
  - `composite_ID` (string, format: UID_test)
**Expected Rows:** ~400

**Processing:**
- Load theta_confidence.csv
- Load tsvr_mapping.csv
- Merge on composite_ID (left join - all theta scores must have TSVR match)
- Parse UID and test from composite_ID for grouping variables
- Verify no missing TSVR_hours (all theta scores have time data)

**Output:**

**File:** data/step00_lmm_input.csv
**Format:** CSV, long format (one row per observation)
**Columns:**
  - `composite_ID` (string, UID_test format)
  - `UID` (string, participant identifier)
  - `test` (string, test session T1/T2/T3/T4)
  - `theta_confidence` (float, IRT confidence ability estimate)
  - `se_confidence` (float, standard error of theta)
  - `TSVR_hours` (float, actual time since encoding)
**Expected Rows:** ~400 (100 participants x 4 tests)

**Validation Requirement:**
Validation tools MUST be used after data loading tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_lmm_input.csv exists (exact path)
- Expected rows: 400 (100 participants x 4 tests)
- Expected columns: 6 (composite_ID, UID, test, theta_confidence, se_confidence, TSVR_hours)
- Data types: string (composite_ID, UID, test), float (theta_confidence, se_confidence, TSVR_hours)

*Value Ranges:*
- theta_confidence in [-3, 3] (typical IRT ability range)
- se_confidence in [0.1, 1.5] (reasonable SE range - above 1.5 suggests unreliable estimates)
- TSVR_hours in [0, 200] hours (0=encoding, ~144=Day 6, some variability expected)

*Data Quality:*
- No NaN values tolerated (all cells must have valid values)
- Expected N: Exactly 400 rows (no data loss from merge)
- No duplicate composite_IDs (unique observations)
- All UIDs appear 4 times (complete data per participant)

*Log Validation:*
- Required pattern: "Data loaded: 400 rows from theta_confidence.csv"
- Required pattern: "Merge complete: 400 rows matched on composite_ID"
- Forbidden patterns: "ERROR", "Missing TSVR_hours", "Duplicate composite_ID"
- Acceptable warnings: None expected for data loading

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 400 rows, found 387 - missing data")
- Log failure to logs/step00_load_theta_data.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause (likely RQ 6.1.1 incomplete or data corruption)

---

### Step 1: Create Piecewise Time Variables

**Dependencies:** Step 0 (requires TSVR_hours)
**Complexity:** Low (<5 minutes)

**Purpose:** Create Early (0-48h) and Late (48-144h) segment indicators with centered time variables for piecewise LMM.

**Input:**

**File:** data/step00_lmm_input.csv (from Step 0)
**Required Columns:** composite_ID, UID, test, theta_confidence, se_confidence, TSVR_hours

**Processing:**
- Create segment indicator: `Segment = "Early"` if TSVR_hours < 48, else `"Late"`
- Create Early time variable: `Time_Early = TSVR_hours` if Segment=="Early", else 0
- Create Late time variable: `Time_Late = TSVR_hours - 48` if Segment=="Late", else 0
- This creates continuous piecewise function with breakpoint at 48 hours
- Centering at breakpoint ensures interpretable intercept (confidence at 48h)

**Output:**

**File:** data/step01_piecewise_input.csv
**Format:** CSV, long format
**Columns:** All columns from step00_lmm_input.csv PLUS:
  - `Segment` (string, values: "Early", "Late")
  - `Time_Early` (float, hours within Early segment, 0 for Late observations)
  - `Time_Late` (float, hours within Late segment offset from 48h, 0 for Early observations)
**Expected Rows:** ~400

**Validation Requirement:**
Validation tools MUST be used after piecewise variable creation.

**Substance Validation Criteria:**

*Output Files:*
- data/step01_piecewise_input.csv exists
- Expected rows: 400 (same as input)
- Expected columns: 9 (original 6 + 3 piecewise variables)
- Data types: string (Segment), float (Time_Early, Time_Late)

*Value Ranges:*
- Segment in {"Early", "Late"} (categorical, exactly 2 levels)
- Time_Early in [0, 48] (Early observations) or exactly 0 (Late observations)
- Time_Late in [0, 96] (Late observations span 48-144h = 96h range) or exactly 0 (Early observations)

*Data Quality:*
- No NaN values in Segment, Time_Early, Time_Late
- All rows have EITHER Time_Early > 0 OR Time_Late > 0 (not both 0, not both > 0)
- Expected Early count: ~200 rows (T1, T2 sessions at 0h, 24h)
- Expected Late count: ~200 rows (T3, T4 sessions at 72h, 144h)

*Log Validation:*
- Required pattern: "Piecewise variables created: Early N=XXX, Late N=XXX"
- Required pattern: "Breakpoint at 48 hours"
- Forbidden patterns: "ERROR", "Both Time_Early and Time_Late > 0 for same row"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log to logs/step01_create_piecewise_variables.log
- Quit immediately, invoke g_debug

---

### Step 2: Test 1 - Quadratic Model

**Dependencies:** Step 0 (requires TSVR_hours, theta_confidence)
**Complexity:** Medium (~5-10 minutes)

**Purpose:** Test for two-phase pattern via significant quadratic term (curvature in trajectory).

**Input:**

**File:** data/step00_lmm_input.csv (from Step 0)
**Required Columns:** UID, TSVR_hours, theta_confidence

**Processing:**
- Fit LMM: `theta_confidence ~ TSVR_hours + TSVR_hours^2 + (1 + TSVR_hours | UID)`
- Random effects: Random intercept + random slope for time per participant
- Time variable: TSVR_hours (Decision D070 - actual hours, not nominal days)
- Extract fixed effects table with coefficients, SE, z-scores, p-values
- Test quadratic term significance at Bonferroni-corrected alpha = 0.01 (Decision D068 dual p-values)
- If quadratic term p < 0.01: Evidence FOR two-phase pattern (curvature detected)
- If quadratic term p >= 0.01: Evidence AGAINST two-phase pattern (linear sufficient)

**Output:**

**File 1:** data/step02_quadratic_model_summary.txt
**Format:** Text summary of fitted LMM (fixed effects, random effects, fit indices)

**File 2:** data/step02_quadratic_test.csv
**Format:** CSV with columns:
  - `term` (string, values: "TSVR_hours", "TSVR_hours^2")
  - `estimate` (float, coefficient estimate)
  - `se` (float, standard error)
  - `z` (float, z-score)
  - `p_uncorrected` (float, uncorrected p-value)
  - `p_bonferroni` (float, Bonferroni-corrected p-value)
  - `significant_bonferroni` (bool, p_bonferroni < 0.01)
**Expected Rows:** 2 (linear + quadratic terms)

**Validation Requirement:**
Validation tools MUST be used after LMM fitting tool execution.

**Substance Validation Criteria:**

*Output Files:*
- data/step02_quadratic_model_summary.txt exists
- data/step02_quadratic_test.csv exists
- Expected rows in CSV: 2 (linear + quadratic terms)
- Expected columns in CSV: 7 (term, estimate, se, z, p_uncorrected, p_bonferroni, significant_bonferroni)
- Data types: string (term), float (estimate, se, z, p_*), bool (significant_bonferroni)

*Value Ranges:*
- estimate: unrestricted (can be negative for decline)
- se > 0 (standard errors must be positive)
- z: unrestricted (estimate / se)
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1]

*Data Quality:*
- No NaN values in any column
- p_bonferroni = p_uncorrected x 2 (Bonferroni correction for 2 tests)
- Model convergence confirmed (check summary.txt for convergence warnings)

*Log Validation:*
- Required pattern: "Quadratic model fitted successfully"
- Required pattern: "VALIDATION - PASS: Model converged"
- Required pattern: "Quadratic term p-value (Bonferroni): X.XXX"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "NaN in coefficients"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log to logs/step02_fit_quadratic_model.log
- Quit immediately, invoke g_debug (likely convergence issue or data problem)

---

### Step 3: Test 2 - Piecewise vs Continuous Comparison

**Dependencies:** Step 1 (requires piecewise time variables)
**Complexity:** Medium (~5-10 minutes)

**Purpose:** Test for two-phase pattern by comparing piecewise model (separate Early/Late slopes) to continuous linear model via AIC.

**Input:**

**File:** data/step01_piecewise_input.csv (from Step 1)
**Required Columns:** UID, TSVR_hours, Time_Early, Time_Late, theta_confidence

**Processing:**
- Fit Continuous Model: `theta_confidence ~ TSVR_hours + (1 + TSVR_hours | UID)`
- Fit Piecewise Model: `theta_confidence ~ Time_Early + Time_Late + (1 + Time_Early + Time_Late | UID)`
- Extract AIC for both models
- Compute delta AIC = AIC_continuous - AIC_piecewise
- If delta AIC > 2: Piecewise model preferred (evidence FOR two-phase pattern)
- If delta AIC <= 2: Models equivalent (evidence AGAINST two-phase pattern)

**Output:**

**File:** data/step03_piecewise_comparison.csv
**Format:** CSV with columns:
  - `model` (string, values: "Continuous", "Piecewise")
  - `AIC` (float, Akaike Information Criterion)
  - `delta_AIC` (float, AIC_continuous - AIC_piecewise)
  - `piecewise_preferred` (bool, delta_AIC > 2)
**Expected Rows:** 2 (one per model) + 1 summary row for delta_AIC

**Validation Requirement:**
Validation tools MUST be used after model comparison tool execution.

**Substance Validation Criteria:**

*Output Files:*
- data/step03_piecewise_comparison.csv exists
- Expected rows: 3 (Continuous, Piecewise, Summary)
- Expected columns: 4 (model, AIC, delta_AIC, piecewise_preferred)
- Data types: string (model), float (AIC, delta_AIC), bool (piecewise_preferred)

*Value Ranges:*
- AIC: unrestricted but typically 500-1500 for N=400 LMMs
- delta_AIC: unrestricted (positive = piecewise better, negative = continuous better)

*Data Quality:*
- No NaN values
- Both models converged (check logs)
- delta_AIC computed correctly (AIC_continuous - AIC_piecewise)

*Log Validation:*
- Required pattern: "Continuous model AIC: XXX.XX"
- Required pattern: "Piecewise model AIC: XXX.XX"
- Required pattern: "Delta AIC: X.XX (Piecewise preferred: TRUE/FALSE)"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log to logs/step03_compare_piecewise_models.log
- Quit immediately, invoke g_debug

---

### Step 4: Test 3 - Slope Ratio

**Dependencies:** Step 3 (requires fitted piecewise model from comparison)
**Complexity:** Low (~5 minutes)

**Purpose:** Test for two-phase pattern by computing Late/Early slope ratio (expect < 0.5 if late decline slower).

**Input:**

**File:** Piecewise model object from Step 3 (in-memory or re-fitted)
**Required:** Fixed effects estimates for Time_Early and Time_Late coefficients

**Processing:**
- Extract Early slope: beta_Early (coefficient for Time_Early term)
- Extract Late slope: beta_Late (coefficient for Time_Late term)
- Compute slope ratio: ratio = beta_Late / beta_Early
- Note: Both slopes expected negative (decline), so ratio = |beta_Late| / |beta_Early|
- If ratio < 0.5: Late decline less than half Early decline (evidence FOR two-phase pattern)
- If ratio >= 0.5: Late decline similar to Early (evidence AGAINST two-phase pattern)

**Output:**

**File:** data/step04_slope_ratio.csv
**Format:** CSV with columns:
  - `segment` (string, values: "Early", "Late", "Ratio")
  - `slope` (float, beta coefficient for time term)
  - `se` (float, standard error of slope)
  - `ratio_value` (float, |beta_Late| / |beta_Early|, only for Ratio row)
  - `two_phase_evidence` (bool, ratio < 0.5, only for Ratio row)
**Expected Rows:** 3 (Early, Late, Ratio)

**Validation Requirement:**
Validation tools MUST be used after slope ratio computation.

**Substance Validation Criteria:**

*Output Files:*
- data/step04_slope_ratio.csv exists
- Expected rows: 3 (Early, Late, Ratio summary)
- Expected columns: 5 (segment, slope, se, ratio_value, two_phase_evidence)
- Data types: string (segment), float (slope, se, ratio_value), bool (two_phase_evidence)

*Value Ranges:*
- slope: negative values expected (confidence decline), typically -0.05 to -0.001 per hour
- se > 0 (standard errors positive)
- ratio_value in [0, infinity] (ratio of absolute values)

*Data Quality:*
- No NaN values in Early/Late rows
- ratio_value only populated for Ratio row
- two_phase_evidence only populated for Ratio row
- Ratio computed correctly: |slope_Late| / |slope_Early|

*Log Validation:*
- Required pattern: "Early slope: -X.XXX (SE: X.XXX)"
- Required pattern: "Late slope: -X.XXX (SE: X.XXX)"
- Required pattern: "Slope ratio: X.XX (Two-phase evidence: TRUE/FALSE)"
- Forbidden patterns: "ERROR", "Division by zero"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log to logs/step04_compute_slope_ratio.log
- Quit immediately, invoke g_debug

---

### Step 5: Compare to Ch5 5.1.2 Accuracy Pattern

**Dependencies:** Steps 2, 3, 4 (requires all three test results)
**Complexity:** Low (~5 minutes)

**Purpose:** Document whether confidence two-phase pattern replicates accuracy two-phase pattern from Chapter 5 RQ 5.1.2.

**Input:**

**File 1:** data/step02_quadratic_test.csv (from Step 2)
**File 2:** data/step03_piecewise_comparison.csv (from Step 3)
**File 3:** data/step04_slope_ratio.csv (from Step 4)

**File 4 (Comparison Benchmark):** results/ch5/5.1.2/data/step0X_two_phase_summary.csv
**Note:** Exact filename depends on Ch5 5.1.2 implementation (use actual path from that RQ)
**Expected:** Summary of Ch5 5.1.2 findings (quadratic significant?, piecewise preferred?, slope ratio?)

**Processing:**
- Load all three test results from Steps 2-4
- Count evidence: How many of 3 tests support two-phase pattern?
- Determine overall conclusion: 2/3 tests = SUPPORT, 0/3 tests = NULL (paralleling accuracy), 1/3 = INCONCLUSIVE
- Load Ch5 5.1.2 findings (if available)
- Compare: Does confidence replicate accuracy pattern? Diverge? Parallel?

**Output:**

**File:** data/step05_ch5_comparison.csv
**Format:** CSV with columns:
  - `measure` (string, values: "Confidence (Ch6 6.1.2)", "Accuracy (Ch5 5.1.2)")
  - `quadratic_significant` (bool, p < 0.01 Bonferroni)
  - `piecewise_preferred` (bool, delta AIC > 2)
  - `slope_ratio_small` (bool, ratio < 0.5)
  - `evidence_count` (int, 0-3, how many tests support two-phase)
  - `conclusion` (string, "SUPPORT", "NULL", "INCONCLUSIVE")
  - `pattern_match` (string, "REPLICATED", "DIVERGED", "INCONCLUSIVE")
**Expected Rows:** 2 (Confidence, Accuracy)

**Validation Requirement:**
Validation tools MUST be used after comparison table creation.

**Substance Validation Criteria:**

*Output Files:*
- data/step05_ch5_comparison.csv exists
- Expected rows: 2 (Confidence from this RQ, Accuracy from Ch5 5.1.2)
- Expected columns: 7 (measure, 3 test bools, evidence_count, conclusion, pattern_match)
- Data types: string (measure, conclusion, pattern_match), bool (test results), int (evidence_count)

*Value Ranges:*
- evidence_count in [0, 3] (count of supporting tests)
- conclusion in {"SUPPORT", "NULL", "INCONCLUSIVE"}
- pattern_match in {"REPLICATED", "DIVERGED", "INCONCLUSIVE", "N/A"} (N/A if Ch5 data unavailable)

*Data Quality:*
- No NaN values
- evidence_count matches sum of 3 test bools
- pattern_match = "REPLICATED" if both measures have same conclusion

*Log Validation:*
- Required pattern: "Confidence two-phase evidence: X/3 tests support"
- Required pattern: "Accuracy two-phase evidence (Ch5 5.1.2): X/3 tests support"
- Required pattern: "Pattern comparison: REPLICATED/DIVERGED/INCONCLUSIVE"
- Acceptable warnings: "Ch5 5.1.2 data not found - comparison skipped"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log to logs/step05_compare_to_ch5.log
- Quit immediately, invoke g_debug

---

### Step 6: Prepare Two-Phase Plot Data

**Dependencies:** Step 1 (requires piecewise variables), Step 3 (requires piecewise model predictions)
**Complexity:** Low (~5 minutes)

**Purpose:** Create plot source CSVs for visualizing two-phase pattern (Option B architecture).

**Input:**

**File 1:** data/step01_piecewise_input.csv (from Step 1)
**File 2:** Piecewise model predictions from Step 3 (fitted values + CIs)

**Processing:**
- Aggregate observed means by Segment (Early/Late) and TSVR_hours
- Extract model predictions from piecewise model (fitted theta + 95% CI)
- Create theta-scale plot data (Decision D069 dual-scale requirement)
- Create probability-scale plot data by transforming theta -> probability via IRT 2PL formula
- Format data for trajectory plotting (time, theta, CI_lower, CI_upper, segment)

**Plot Description:** Two-panel trajectory showing Early segment (0-48h) and Late segment (48-144h) with observed means, fitted lines, and confidence bands. Demonstrates whether decline rate differs between segments.

**Required Data Sources:**
- data/step01_piecewise_input.csv (observed theta_confidence, TSVR_hours, Segment)
- Piecewise model object from Step 3 (fitted values, predictions)

**Output (Plot Source CSVs):**

**File 1:** data/step06_twophase_theta_data.csv
**Format:** CSV, plot source data for theta-scale trajectory
**Columns:**
  - `TSVR_hours` (float, time since encoding)
  - `theta_confidence` (float, mean theta per segment per timepoint)
  - `CI_lower` (float, lower 95% confidence bound)
  - `CI_upper` (float, upper 95% confidence bound)
  - `Segment` (string, "Early" or "Late")
  - `fitted` (float, model predicted value)
**Expected Rows:** ~20-30 (aggregated timepoints within each segment)

**File 2:** data/step06_twophase_probability_data.csv
**Format:** CSV, plot source data for probability-scale trajectory (Decision D069 dual-scale)
**Columns:** Same as theta_data but with probability values (0-1 scale) instead of theta scale

**Validation Requirement:**
Validation tools MUST be used after plot data preparation tool execution.

**Substance Validation Criteria:**

*Output Files:*
- data/step06_twophase_theta_data.csv exists
- data/step06_twophase_probability_data.csv exists
- Expected rows: 20-30 per file (aggregated timepoints)
- Expected columns: 6 (TSVR_hours, theta_confidence, CI_lower, CI_upper, Segment, fitted)
- Data types: float (time, theta, CI, fitted), string (Segment)

*Value Ranges:*
- TSVR_hours in [0, 144] (entire retention interval)
- theta_confidence in [-3, 3] (IRT ability range)
- CI_lower in [-3, 3], CI_upper in [-3, 3]
- probability values in [0, 1] (for probability_data.csv)
- Segment in {"Early", "Late"}

*Data Quality:*
- No NaN values tolerated
- CI_upper > CI_lower for all rows
- Both segments represented (Early and Late rows present)
- TSVR_hours sorted within each segment

*Log Validation:*
- Required pattern: "Plot data prepared: XX rows theta scale, XX rows probability scale"
- Required pattern: "Segments represented: Early, Late"
- Forbidden patterns: "ERROR", "Missing segment", "NaN values detected"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log to logs/step06_prepare_twophase_plot_data.log
- Quit immediately, invoke g_debug

**Plotting Function (rq_plots will call later):** Two-panel trajectory plot with separate Early/Late slopes
- rq_plots reads data/step06_twophase_theta_data.csv and data/step06_twophase_probability_data.csv
- Generates dual-scale plots (theta + probability per Decision D069)
- Saves PNG to plots/ folder (not created by this step)

---

## Expected Data Formats

### TSVR Time Variable (Decision D070)

**Format:** Actual hours since VR encoding session

**Rationale:** Nominal days (0, 1, 3, 6) assume fixed intervals, but actual participant sessions vary by hours or days. Using TSVR_hours (actual elapsed time) ensures accurate temporal modeling. This is Project Decision D070 applied to confidence data.

**Expected Values:**
- T1 (Day 0): TSVR_hours ~= 0 (encoding session)
- T2 (Day 1): TSVR_hours ~= 24 (range: 20-30 hours)
- T3 (Day 3): TSVR_hours ~= 72 (range: 65-80 hours)
- T4 (Day 6): TSVR_hours ~= 144 (range: 135-155 hours)

### Piecewise Time Variables

**Breakpoint:** 48 hours (nominal Day 1, post-sleep consolidation)

**Time_Early:** TSVR_hours if TSVR_hours < 48, else 0
**Time_Late:** TSVR_hours - 48 if TSVR_hours >= 48, else 0

**Rationale:** Continuous piecewise function allows separate slopes for Early and Late segments while maintaining a single model framework. Centering Late segment at 48h ensures interpretable intercept (confidence level at breakpoint).

### Theta to Probability Transformation (Decision D069)

**Formula:** probability = 1 / (1 + exp(-1.702 * theta))

**Rationale:** IRT 2PL transformation converts theta scale (-3 to +3) to probability scale (0 to 1) for interpretability by non-psychometricians. Dual-scale plotting required for trajectory RQs per Decision D069.

---

## Cross-RQ Dependencies

**Dependency Type:** DERIVED data from other RQs (not RAW data from master.xlsx)

**This RQ requires outputs from:**

**RQ 6.1.1** (Confidence Model Selection - provides theta_confidence scores)
- File 1: results/ch6/6.1.1/data/step03_theta_confidence.csv (IRT ability estimates for confidence)
- File 2: results/ch6/6.1.1/data/step00_tsvr_mapping.csv (time mapping)
- Used in: Step 0 (load theta scores + TSVR)
- Rationale: RQ 6.1.1 performs IRT calibration on 5-category confidence data (GRM Pass 1, purification, GRM Pass 2). This RQ uses those theta estimates to test trajectory patterns.

**RQ 5.1.2** (Two-Phase Pattern in Accuracy - provides comparison benchmark)
- File: results/ch5/5.1.2/data/step0X_two_phase_summary.csv (accuracy two-phase findings)
- Used in: Step 5 (compare confidence pattern to accuracy pattern)
- Rationale: RQ 5.1.2 tests two-phase pattern for accuracy. This RQ tests whether confidence exhibits the same pattern. Comparison determines if metacognition parallels memory dynamics.

**Execution Order Constraint:**
1. RQ 6.1.1 must complete Steps 0-3 first (provides theta_confidence.csv)
2. RQ 5.1.2 should complete first (provides accuracy comparison benchmark, but comparison can be skipped if unavailable)
3. This RQ executes after RQ 6.1.1 completes

**Data Source Boundaries:**
- **RAW data:** None (all data derived from other RQs)
- **DERIVED data:** Theta_confidence from RQ 6.1.1, accuracy findings from RQ 5.1.2
- **Scope:** This RQ does NOT re-calibrate IRT models (uses RQ 6.1.1 theta estimates directly)

**Validation:**
- Step 0: Check results/ch6/6.1.1/data/step03_theta_confidence.csv exists (EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch6/6.1.1/data/step00_tsvr_mapping.csv exists (EXPECTATIONS ERROR if absent)
- Step 5: Check results/ch5/5.1.2/ exists (acceptable warning if missing - comparison skipped)
- If RQ 6.1.1 files missing -> quit with error -> user must execute RQ 6.1.1 first

---

## Validation Requirements

**CRITICAL MANDATE:**

Every analysis step in this plan MUST use validation tools after analysis tool execution.

This is not optional. This is the core architectural principle preventing cascading failures observed in v3.0 (where analysis errors propagated undetected through 5+ downstream steps before discovery).

**Exact Specification Requirement:**

> "Validation tools MUST be used after analysis tool execution"

**Implementation:**
- rq_tools (Step 11 workflow) will read tools_catalog.md validation tools section
- rq_tools will specify BOTH analysis tool + validation tool per step in 3_tools.yaml
- rq_analysis (Step 12 workflow) will embed validation tool call AFTER analysis tool call in 4_analysis.yaml
- g_code (Step 14 workflow) will generate stepNN_name.py scripts with validation function calls
- bash execution (Step 14 workflow) will run analysis -> validation -> error on validation failure

**Downstream Agent Requirements:**
- **rq_tools:** MUST specify validation tool for EVERY analysis step (no exceptions)
- **rq_analysis:** MUST embed validation tool call for EVERY analysis step (no exceptions)
- **g_code:** MUST generate code with validation function calls (no exceptions)
- **rq_inspect:** MUST verify validation ran successfully (checks logs for validation output)

### Validation Requirements By Step

#### Step 0: Load Theta Confidence Scores

**Analysis Tool:** (determined by rq_tools - likely pandas.read_csv + merge operations)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure)

**What Validation Checks:**
- Output file exists (data/step00_lmm_input.csv)
- Expected row count (400 rows: 100 participants x 4 tests)
- Expected column count (6 columns: composite_ID, UID, test, theta_confidence, se_confidence, TSVR_hours)
- No NaN values (all theta scores have TSVR match)
- Unique composite_IDs (no duplicates)
- All UIDs appear 4 times (complete data per participant)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Missing TSVR_hours for 15 composite_IDs")
- Log failure to logs/step00_load_theta_data.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked by master to diagnose root cause

---

#### Step 1: Create Piecewise Time Variables

**Analysis Tool:** (determined by rq_tools - likely custom piecewise variable creation function)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure + custom checks)

**What Validation Checks:**
- Output file exists (data/step01_piecewise_input.csv)
- Piecewise variables created (Segment, Time_Early, Time_Late columns present)
- Segment values in {"Early", "Late"} only
- Mutual exclusivity: Time_Early > 0 XOR Time_Late > 0 (not both, not neither)
- Expected Early/Late counts (~200 rows each)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log to logs/step01_create_piecewise_variables.log
- Quit immediately, invoke g_debug

---

#### Step 2: Test 1 - Quadratic Model

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.fit_lmm_trajectory_tsvr)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_lmm_convergence + validate_hypothesis_test_dual_pvalues)

**What Validation Checks:**
- Model converged (no convergence warnings in summary)
- Fixed effects table has quadratic term (TSVR_hours^2 present)
- Dual p-values present (p_uncorrected AND p_bonferroni per Decision D068)
- p-values in [0, 1] range
- Standard errors positive

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Quadratic model did not converge")
- Log to logs/step02_fit_quadratic_model.log
- Quit immediately, invoke g_debug

---

#### Step 3: Test 2 - Piecewise vs Continuous Comparison

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.fit_lmm_trajectory_tsvr for both models)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_lmm_convergence + custom AIC comparison check)

**What Validation Checks:**
- Both models converged
- AIC values extracted and reasonable (typically 500-1500 for N=400)
- Delta AIC computed correctly
- Comparison conclusion documented

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log to logs/step03_compare_piecewise_models.log
- Quit immediately, invoke g_debug

---

#### Step 4: Test 3 - Slope Ratio

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.extract_segment_slopes_from_lmm)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_numeric_range + custom slope extraction check)

**What Validation Checks:**
- Early and Late slopes extracted
- Slopes are negative (confidence decline expected)
- Ratio computed correctly (|Late| / |Early|)
- Standard errors positive

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log to logs/step04_compute_slope_ratio.log
- Quit immediately, invoke g_debug

---

#### Step 5: Compare to Ch5 5.1.2 Accuracy Pattern

**Analysis Tool:** (determined by rq_tools - likely custom comparison table creation)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure)

**What Validation Checks:**
- Comparison table has 2 rows (Confidence, Accuracy)
- Evidence count matches sum of test bools
- Conclusion in {"SUPPORT", "NULL", "INCONCLUSIVE"}
- Pattern match documented

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log to logs/step05_compare_to_ch5.log
- Quit immediately, invoke g_debug

---

#### Step 6: Prepare Two-Phase Plot Data

**Analysis Tool:** (determined by rq_tools - likely custom plot data aggregation function)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_plot_data_completeness + validate_probability_range)

**What Validation Checks:**
- Both plot source CSVs created (theta_data.csv, probability_data.csv)
- Expected row counts (~20-30 aggregated timepoints)
- Both segments represented (Early and Late)
- CI_upper > CI_lower for all rows
- Probability values in [0, 1] range
- No NaN values

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log to logs/step06_prepare_twophase_plot_data.log
- Quit immediately, invoke g_debug

---

## Summary

**Total Steps:** 7 (Step 0: Data loading + Steps 1-6: Analysis and plot preparation)

**Estimated Runtime:** ~15-30 minutes total
- Step 0: <5 min (data loading)
- Step 1: <5 min (piecewise variables)
- Step 2: ~5-10 min (quadratic model fitting)
- Step 3: ~5-10 min (piecewise model comparison)
- Step 4: <5 min (slope ratio)
- Step 5: <5 min (Ch5 comparison)
- Step 6: <5 min (plot data preparation)

**Cross-RQ Dependencies:**
- RQ 6.1.1 (theta_confidence scores, TSVR mapping)
- RQ 5.1.2 (accuracy two-phase pattern comparison benchmark)

**Primary Outputs:**
- data/step02_quadratic_test.csv (Test 1 results: quadratic term significance)
- data/step03_piecewise_comparison.csv (Test 2 results: model comparison AIC)
- data/step04_slope_ratio.csv (Test 3 results: Early vs Late slope ratio)
- data/step05_ch5_comparison.csv (Confidence vs Accuracy pattern comparison)
- data/step06_twophase_theta_data.csv (Plot source CSV, theta scale)
- data/step06_twophase_probability_data.csv (Plot source CSV, probability scale)

**Validation Coverage:** 100% (all 7 steps have validation requirements)

**Success Criteria:**
- All models converge successfully
- 2 out of 3 tests support two-phase pattern (evidence FOR), OR 0 out of 3 tests support (evidence AGAINST - NULL pattern paralleling accuracy)
- Comparison to Ch5 5.1.2 documented (replication vs divergence)
- Plot data complete and validated

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent for RQ 6.1.2
