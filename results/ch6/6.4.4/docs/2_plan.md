# Analysis Plan: RQ 6.4.4 - Paradigm-Specific Trait Variance in Confidence Decline

**Research Question:** 6.4.4
**Created:** 2025-12-06
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines whether confidence trajectory slopes show paradigm-specific trait-like individual differences. Analysis uses Linear Mixed Models (LMM) with random slopes to decompose variance in confidence decline rates across three retrieval paradigms: Free Recall (IFR), Cued Recall (ICR), and Recognition (IRE). The primary research question asks: Is ICC_slope higher for Free Recall (high cognitive demand) compared to Cued Recall and Recognition (lower demand)?

**Pipeline:** LMM with variance decomposition + ICC computation
**Steps:** 6 total analysis steps (Step 0: data import + Steps 1-5: analysis)
**Estimated Runtime:** Low (LMM fitting only, no IRT calibration required)

**Key Decisions Applied:**
- Decision D070: TSVR as time variable (actual hours, not nominal days)
- Decision D068: Dual p-value reporting (if paradigm ICC comparisons tested)

**Note:** This RQ uses DERIVED data from RQ 6.4.1 (theta_confidence scores already computed). No IRT calibration or purification steps required.

---

## Analysis Plan

### Step 0: Import Theta Confidence Data

**Dependencies:** None (first step)
**Complexity:** Low (data import from RQ 6.4.1)

**Input:**

**File:** results/ch6/6.4.1/data/step03_theta_confidence_paradigm.csv
**Source:** RQ 6.4.1 (IRT calibration with 3-factor GRM for IFR/ICR/IRE paradigms)
**Format:** CSV with columns:
  - composite_ID (string, format: {UID}_{test}, e.g., P001_T1)
  - paradigm (string, values: {IFR, ICR, IRE})
  - theta_confidence (float, IRT ability estimate on confidence scale)
  - se_confidence (float, standard error of theta estimate)
**Expected Rows:** 1200 (100 participants x 4 tests x 3 paradigms)

**Processing:**

1. Read theta_confidence_paradigm.csv from RQ 6.4.1
2. Verify all 3 paradigms present (IFR, ICR, IRE)
3. Extract UID and test from composite_ID (parse {UID}_{test} format)
4. Merge with TSVR_hours from master.xlsx (Time Since VR in actual hours per Decision D070)
5. Create long-format dataset ready for LMM fitting

**Output:**

**File 1:** data/step00_lmm_input.csv
**Format:** CSV, long format (one row per observation: participant x test x paradigm)
**Columns:**
  - UID (string, participant identifier, e.g., P001)
  - test (string, test session: T1, T2, T3, T4)
  - TSVR_hours (float, actual time since encoding in hours, Decision D070)
  - paradigm (string, retrieval paradigm: IFR, ICR, IRE)
  - theta_confidence (float, IRT ability estimate)
  - se_confidence (float, standard error)
**Expected Rows:** 1200 (100 participants x 4 tests x 3 paradigms)

**Validation Requirement:**
Validation tools MUST be used after data import. Specific validation tools determined by rq_tools based on data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_lmm_input.csv exists (exact path)
- Expected rows: 1200 (100 participants x 4 tests x 3 paradigms)
- Expected columns: 6 (UID, test, TSVR_hours, paradigm, theta_confidence, se_confidence)
- Data types: UID (string), test (string), TSVR_hours (float), paradigm (string), theta_confidence (float), se_confidence (float)

*Value Ranges:*
- TSVR_hours in [0, 168] hours (0 = encoding, 168 = 1 week max)
- theta_confidence in [-3, 3] (typical IRT ability range)
- se_confidence in [0.1, 1.0] (above 1.0 = unreliable)
- paradigm in {IFR, ICR, IRE} (categorical, all 3 present)

*Data Quality:*
- No NaN values allowed in UID, test, TSVR_hours, paradigm, theta_confidence
- NaN acceptable in se_confidence if <5% (rare estimation issues)
- Expected N: Exactly 1200 rows (100 participants x 4 tests x 3 paradigms)
- No duplicate composite_ID x paradigm combinations
- All 100 UIDs present (no participant data loss)

*Log Validation:*
- Required pattern: "Data import complete: 1200 rows loaded"
- Required pattern: "All 3 paradigms present: IFR, ICR, IRE"
- Required pattern: "TSVR merge successful: 1200 matches"
- Forbidden patterns: "ERROR", "Missing paradigm", "TSVR merge failed"
- Acceptable warnings: None expected for data import

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 1200 rows, found 1150")
- Log failure to logs/step00_import_data.log
- Quit script immediately (do NOT proceed to Step 1)
- Master investigates RQ 6.4.1 dependency or TSVR merge issues

---

### Step 1: Fit Paradigm-Stratified LMMs with Random Slopes

**Dependencies:** Step 0 (requires lmm_input.csv)
**Complexity:** Medium (3 separate LMM fits, 5-10 min total)

**Input:**

**File:** data/step00_lmm_input.csv
**Source:** Step 0 (theta_confidence merged with TSVR)
**Format:** Long format (one row per observation)
**Expected Rows:** 1200 (100 participants x 4 tests x 3 paradigms)

**Processing:**

1. Split data by paradigm (IFR, ICR, IRE)
2. Fit 3 separate LMMs, one per paradigm:
   - Formula: theta_confidence ~ TSVR_hours + (TSVR_hours | UID)
   - Random intercepts: Baseline confidence individual differences
   - Random slopes: Confidence decline rate individual differences
   - Time variable: TSVR_hours (actual hours per Decision D070, not nominal days)
3. Extract variance components per paradigm:
   - var_intercept: variance in baseline confidence (Day 0)
   - var_slope: variance in confidence decline rate
   - cov_int_slope: covariance between intercept and slope
   - var_residual: within-person residual variance
4. Check convergence for all 3 models (must converge successfully)

**Output:**

**File 1:** data/step01_lmm_ifr_summary.txt
**Format:** Text file with LMM summary (fixed effects, random effects, fit indices)
**Content:** Full statsmodels summary for Free Recall (IFR) paradigm

**File 2:** data/step01_lmm_icr_summary.txt
**Format:** Text file with LMM summary
**Content:** Full statsmodels summary for Cued Recall (ICR) paradigm

**File 3:** data/step01_lmm_ire_summary.txt
**Format:** Text file with LMM summary
**Content:** Full statsmodels summary for Recognition (IRE) paradigm

**Validation Requirement:**
Validation tools MUST be used after LMM fitting. Specific validation tools determined by rq_tools based on LMM diagnostic requirements (convergence, residuals, assumptions).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_lmm_ifr_summary.txt exists
- data/step01_lmm_icr_summary.txt exists
- data/step01_lmm_ire_summary.txt exists
- Each file >1 KB (contains full model summary)

*Value Ranges:*
- Fixed effect coefficients: TSVR_hours coefficient expected negative (confidence declines over time)
- Variance components: all >0 (negative variance = model misspecification)
- Random slope variance: tested if >0 (indicates individual differences in decline rate)

*Data Quality:*
- All 3 models must converge successfully
- No singular fit warnings (indicates model identifiability)
- Residuals approximately normal (K-S test or Q-Q plot visual inspection)

*Log Validation:*
- Required pattern: "Model converged: True" (for each of 3 paradigms)
- Required pattern: "Variance components extracted: var_intercept, var_slope, cov_int_slope, var_residual"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "Singular matrix"
- Acceptable warnings: "Gradient close to zero" acceptable if model converged

**Expected Behavior on Validation Failure:**
- Raise error with paradigm-specific failure (e.g., "IFR model failed to converge")
- Log failure to logs/step01_fit_lmm.log
- Quit script immediately
- Master invokes g_debug to diagnose convergence issues

---

### Step 2: Extract Variance Components Per Paradigm

**Dependencies:** Step 1 (requires fitted LMMs)
**Complexity:** Low (extract variance from fitted models)

**Input:**

**File:** Fitted LMM models from Step 1 (in-memory Python objects, not CSV files)
**Source:** Step 1 LMM fitting

**Processing:**

1. Extract variance components from each fitted model (IFR, ICR, IRE):
   - var_intercept (baseline confidence variance)
   - var_slope (decline rate variance)
   - cov_int_slope (intercept-slope covariance)
   - var_residual (within-person residual variance)
2. Compute total variance per paradigm: var_total = var_intercept + var_slope + var_residual
3. Save variance components to CSV for downstream ICC computation

**Output:**

**File 1:** data/step02_variance_components.csv
**Format:** CSV with one row per paradigm
**Columns:**
  - paradigm (string: IFR, ICR, IRE)
  - var_intercept (float: baseline variance)
  - var_slope (float: slope variance)
  - cov_int_slope (float: intercept-slope covariance)
  - var_residual (float: within-person variance)
  - var_total (float: sum of variance components)
**Expected Rows:** 3 (one per paradigm)

**Validation Requirement:**
Validation tools MUST be used after variance component extraction. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_variance_components.csv exists
- Expected rows: 3 (IFR, ICR, IRE)
- Expected columns: 6 (paradigm, var_intercept, var_slope, cov_int_slope, var_residual, var_total)
- Data types: paradigm (string), all variance columns (float)

*Value Ranges:*
- All variance components >0 (negative variance impossible, indicates estimation error)
- var_total = var_intercept + var_slope + var_residual (sanity check)
- Covariance unrestricted (can be positive, negative, or zero)

*Data Quality:*
- Exactly 3 rows (one per paradigm)
- All paradigms present: IFR, ICR, IRE
- No NaN values (variance must be finite)
- No duplicate paradigm rows

*Log Validation:*
- Required pattern: "Variance components extracted for all 3 paradigms"
- Required pattern: "All variances positive: var_intercept, var_slope, var_residual"
- Forbidden patterns: "ERROR", "Negative variance detected", "NaN variance"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- Raise error with paradigm-specific failure (e.g., "IFR variance components invalid")
- Log failure to logs/step02_extract_variance.log
- Quit script immediately
- Master investigates LMM fitting issues from Step 1

---

### Step 3: Compute ICC Per Paradigm

**Dependencies:** Step 2 (requires variance components)
**Complexity:** Low (ICC computation from variance components)

**Input:**

**File:** data/step02_variance_components.csv
**Source:** Step 2 (variance component extraction)
**Expected Rows:** 3 (one per paradigm)

**Processing:**

1. Compute 3 ICC estimates per paradigm:
   - **ICC_intercept:** var_intercept / var_total (proportion of baseline variance between-person)
   - **ICC_slope_simple:** var_slope / var_total (proportion of slope variance between-person, unconditional)
   - **ICC_slope_conditional:** (var_slope + 2 x cov_int_slope + var_intercept) / var_total (slope ICC at Day 6, accounting for intercept-slope correlation)
2. Interpret ICC values using standard thresholds:
   - <0.10: Minimal trait variance (state-like)
   - 0.10-0.30: Low-moderate trait variance
   - 0.30-0.50: Moderate trait variance
   - >0.50: High trait variance (trait-like)
3. Save ICC estimates with interpretation flags

**Output:**

**File 1:** data/step03_icc_estimates.csv
**Format:** CSV with one row per paradigm
**Columns:**
  - paradigm (string: IFR, ICR, IRE)
  - ICC_intercept (float: baseline ICC)
  - ICC_slope_simple (float: unconditional slope ICC)
  - ICC_slope_conditional (float: conditional slope ICC at Day 6)
  - interpretation_intercept (string: e.g., "Moderate trait variance")
  - interpretation_slope (string: e.g., "Minimal trait variance")
**Expected Rows:** 3 (one per paradigm)

**Validation Requirement:**
Validation tools MUST be used after ICC computation. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_icc_estimates.csv exists
- Expected rows: 3 (IFR, ICR, IRE)
- Expected columns: 6 (paradigm, ICC_intercept, ICC_slope_simple, ICC_slope_conditional, interpretation_intercept, interpretation_slope)
- Data types: paradigm (string), ICC values (float), interpretations (string)

*Value Ranges:*
- All ICC values in [0, 1] (outside = computation error)
- ICC_intercept typically >0.30 (baseline confidence shows individual differences)
- ICC_slope_simple and ICC_slope_conditional tested if >0.10 (trait-like slope variance)

*Data Quality:*
- Exactly 3 rows (one per paradigm)
- All paradigms present: IFR, ICR, IRE
- No NaN values (ICC must be finite)
- No duplicate paradigm rows
- Interpretation strings match ICC value ranges (e.g., ICC=0.05 should have "Minimal" interpretation)

*Log Validation:*
- Required pattern: "ICC computed for all 3 paradigms"
- Required pattern: "All ICC values in valid range [0, 1]"
- Forbidden patterns: "ERROR", "ICC out of bounds", "NaN ICC"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- Raise error with paradigm-specific failure (e.g., "IFR ICC_slope = 1.2, exceeds valid range")
- Log failure to logs/step03_compute_icc.log
- Quit script immediately
- Master investigates variance component extraction issues from Step 2

---

### Step 4: Compare ICC_slope Across Paradigms

**Dependencies:** Step 3 (requires ICC estimates)
**Complexity:** Low (descriptive comparison, no formal hypothesis test)

**Input:**

**File:** data/step03_icc_estimates.csv
**Source:** Step 3 (ICC computation)
**Expected Rows:** 3 (IFR, ICR, IRE)

**Processing:**

1. Compare ICC_slope_simple across paradigms:
   - Order paradigms by ICC_slope value (highest to lowest)
   - Compute ICC_slope differences (e.g., IFR - ICR, IFR - IRE, ICR - IRE)
   - Determine if Free Recall shows highest ICC_slope (as hypothesized)
2. Compare ICC_slope_conditional across paradigms (same logic)
3. Summarize paradigm-specific trait variance pattern:
   - If IFR > ICR > IRE: "Trait variance increases with cognitive demand"
   - If all ICC_slope H 0: "Confidence decline is state-like across all paradigms"
   - If mixed pattern: "No clear relationship between retrieval support and trait variance"
4. Save comparison summary

**Output:**

**File 1:** data/step04_paradigm_icc_comparison.csv
**Format:** CSV with pairwise ICC differences
**Columns:**
  - comparison (string: e.g., "IFR - ICR", "IFR - IRE", "ICR - IRE")
  - ICC_slope_diff_simple (float: difference in ICC_slope_simple)
  - ICC_slope_diff_conditional (float: difference in ICC_slope_conditional)
  - direction (string: "IFR higher", "ICR higher", "IRE higher", or "Equivalent")
**Expected Rows:** 3 (3 pairwise comparisons)

**File 2:** data/step04_paradigm_summary.txt
**Format:** Text summary of paradigm ICC pattern
**Content:**
  - Paradigm order by ICC_slope (highest to lowest)
  - Interpretation (trait variance pattern across paradigms)
  - Hypothesis test result (Free Recall highest? Yes/No)

**Validation Requirement:**
Validation tools MUST be used after paradigm comparison. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_paradigm_icc_comparison.csv exists
- data/step04_paradigm_summary.txt exists
- Expected rows: 3 (pairwise comparisons)
- Expected columns: 4 (comparison, ICC_slope_diff_simple, ICC_slope_diff_conditional, direction)

*Value Ranges:*
- ICC differences in [-1, 1] (difference of two [0,1] values)
- Direction strings must match sign of differences (e.g., positive diff -> "IFR higher")

*Data Quality:*
- Exactly 3 rows (IFR-ICR, IFR-IRE, ICR-IRE)
- No NaN values
- No duplicate comparison rows
- Summary text contains paradigm order and interpretation

*Log Validation:*
- Required pattern: "Paradigm comparison complete: 3 pairwise comparisons"
- Required pattern: "Hypothesis test: Free Recall highest ICC_slope = [Yes/No]"
- Forbidden patterns: "ERROR", "Missing comparison"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Missing IFR-IRE comparison")
- Log failure to logs/step04_compare_paradigms.log
- Quit script immediately
- Master investigates ICC computation issues from Step 3

---

### Step 5: Compare to Ch5 5.3.7 (Accuracy ICC)

**Dependencies:** Step 3 (requires confidence ICC estimates)
**Complexity:** Low (cross-RQ comparison, no new computation)

**Input:**

**File 1:** data/step03_icc_estimates.csv
**Source:** Step 3 (confidence ICC estimates from this RQ)

**File 2:** results/ch5/5.3.7/data/step03_icc_estimates.csv
**Source:** Ch5 5.3.7 (accuracy ICC estimates by paradigm)
**Expected Rows:** 3 (IFR, ICR, IRE - assuming Ch5 5.3.7 used same paradigms)

**Processing:**

1. Load confidence ICC estimates from this RQ (Step 3)
2. Load accuracy ICC estimates from Ch5 5.3.7
3. Merge on paradigm (IFR, ICR, IRE)
4. Compute differences:
   - ICC_intercept_diff = ICC_intercept_confidence - ICC_intercept_accuracy
   - ICC_slope_diff = ICC_slope_confidence - ICC_slope_accuracy
5. Interpret differences:
   - If ICC_slope_confidence > ICC_slope_accuracy: "5-level confidence data reveals slope variance that dichotomous accuracy missed"
   - If ICC_slope_confidence H ICC_slope_accuracy: "Confidence and accuracy show similar trait variance patterns"
6. Document comparison results

**Output:**

**File 1:** data/step05_ch5_comparison.csv
**Format:** CSV with one row per paradigm
**Columns:**
  - paradigm (string: IFR, ICR, IRE)
  - ICC_intercept_confidence (float: from this RQ)
  - ICC_intercept_accuracy (float: from Ch5 5.3.7)
  - ICC_intercept_diff (float: confidence - accuracy)
  - ICC_slope_confidence (float: ICC_slope_simple from this RQ)
  - ICC_slope_accuracy (float: ICC_slope_simple from Ch5 5.3.7)
  - ICC_slope_diff (float: confidence - accuracy)
  - interpretation (string: e.g., "Confidence reveals more slope variance than accuracy")
**Expected Rows:** 3 (one per paradigm)

**File 2:** data/step05_ch5_summary.txt
**Format:** Text summary of accuracy vs confidence ICC comparison
**Content:**
  - Overall pattern (confidence > accuracy? confidence H accuracy?)
  - Paradigm-specific patterns (which paradigms show largest differences?)
  - Theoretical interpretation (does 5-level data reveal trait variance that dichotomous data missed?)

**Validation Requirement:**
Validation tools MUST be used after Ch5 comparison. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_ch5_comparison.csv exists
- data/step05_ch5_summary.txt exists
- Expected rows: 3 (IFR, ICR, IRE)
- Expected columns: 8 (paradigm, ICC_intercept_confidence, ICC_intercept_accuracy, ICC_intercept_diff, ICC_slope_confidence, ICC_slope_accuracy, ICC_slope_diff, interpretation)

*Value Ranges:*
- All ICC values in [0, 1] (from both RQs)
- ICC differences in [-1, 1] (difference of two [0,1] values)

*Data Quality:*
- Exactly 3 rows (one per paradigm)
- All paradigms present: IFR, ICR, IRE
- No NaN values (both RQs must have valid ICC estimates for all paradigms)
- No duplicate paradigm rows
- Summary text contains overall pattern and interpretation

*Log Validation:*
- Required pattern: "Ch5 comparison complete: 3 paradigms matched"
- Required pattern: "Overall pattern: [confidence > accuracy / confidence H accuracy]"
- Forbidden patterns: "ERROR", "Ch5 5.3.7 file not found", "Paradigm mismatch"
- Acceptable warnings: "Ch5 5.3.7 used different ICC formula" acceptable if documented

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Ch5 5.3.7 file missing: results/ch5/5.3.7/data/step03_icc_estimates.csv")
- Log failure to logs/step05_compare_ch5.log
- Quit script immediately
- Master investigates Ch5 5.3.7 dependency (may need to run Ch5 5.3.7 first)

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs - intermediate and final)
- data/step00_lmm_input.csv (from Step 0: theta_confidence + TSVR import)
- data/step01_lmm_ifr_summary.txt (from Step 1: IFR model summary)
- data/step01_lmm_icr_summary.txt (from Step 1: ICR model summary)
- data/step01_lmm_ire_summary.txt (from Step 1: IRE model summary)
- data/step02_variance_components.csv (from Step 2: variance components per paradigm)
- data/step03_icc_estimates.csv (from Step 3: ICC values per paradigm)
- data/step04_paradigm_icc_comparison.csv (from Step 4: pairwise ICC comparisons)
- data/step04_paradigm_summary.txt (from Step 4: paradigm pattern interpretation)
- data/step05_ch5_comparison.csv (from Step 5: confidence vs accuracy ICC comparison)
- data/step05_ch5_summary.txt (from Step 5: Ch5 comparison interpretation)

### Logs (ONLY execution logs - .log files capturing stdout/stderr)
- logs/step00_import_data.log
- logs/step01_fit_lmm.log
- logs/step02_extract_variance.log
- logs/step03_compute_icc.log
- logs/step04_compare_paradigms.log
- logs/step05_compare_ch5.log

### Plots (EMPTY until rq_plots runs)
- No plots planned for this RQ (ICC comparison is tabular)

### Results (EMPTY until rq_results runs)
- results/summary.md (created by rq_results, NOT analysis steps)

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
- rq_tools: MUST specify validation tool for EVERY analysis step (no exceptions)
- rq_analysis: MUST embed validation tool call for EVERY analysis step (no exceptions)
- g_code: MUST generate code with validation function calls (no exceptions)
- rq_inspect: MUST verify validation ran successfully (checks logs/stepN_name.log for validation output)

### Validation Requirements By Step

#### Step 0: Import Theta Confidence Data

**Analysis Tool:** (determined by rq_tools - likely tools.data manipulation functions)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_data_format)

**What Validation Checks:**
- Output file exists (data/step00_lmm_input.csv)
- Expected row count (1200 rows: 100 participants x 4 tests x 3 paradigms)
- Expected column count (6 columns: UID, test, TSVR_hours, paradigm, theta_confidence, se_confidence)
- All required columns present (case-sensitive)
- No unexpected NaN patterns (theta_confidence must be non-NaN for all rows)
- TSVR_hours in valid range [0, 168] hours
- All 3 paradigms present (IFR, ICR, IRE)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 1200 rows, found 1150")
- Log failure to logs/step00_import_data.log
- Quit script immediately
- Master investigates RQ 6.4.1 dependency or TSVR merge issues

---

#### Step 1: Fit Paradigm-Stratified LMMs

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.fit_lmm_trajectory_tsvr)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_lmm_convergence)

**What Validation Checks:**
- All 3 models converged successfully (convergence status = True)
- Variance components all positive (var_intercept, var_slope, var_residual >0)
- No singular fit warnings (indicates model identifiability)
- Residuals approximately normal (K-S test or Q-Q plot)
- Output files exist (3 model summaries: IFR, ICR, IRE)

**Expected Behavior on Validation Failure:**
- Raise error with paradigm-specific failure (e.g., "IFR model failed to converge")
- Log failure to logs/step01_fit_lmm.log
- Quit script immediately
- Master invokes g_debug to diagnose convergence issues

---

#### Step 2: Extract Variance Components

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.extract_random_effects_from_lmm)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_variance_positivity)

**What Validation Checks:**
- Output file exists (data/step02_variance_components.csv)
- Expected row count (3 rows: one per paradigm)
- All variance components positive (var_intercept, var_slope, var_residual >0)
- var_total = var_intercept + var_slope + var_residual (sanity check)
- No NaN values
- All 3 paradigms present

**Expected Behavior on Validation Failure:**
- Raise error with paradigm-specific failure (e.g., "IFR variance components invalid")
- Log failure to logs/step02_extract_variance.log
- Quit script immediately
- Master investigates LMM fitting issues from Step 1

---

#### Step 3: Compute ICC

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.compute_icc_from_variance_components)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_icc_bounds)

**What Validation Checks:**
- Output file exists (data/step03_icc_estimates.csv)
- Expected row count (3 rows: one per paradigm)
- All ICC values in [0, 1] (outside = computation error)
- No NaN values
- All 3 paradigms present
- Interpretation strings match ICC value ranges

**Expected Behavior on Validation Failure:**
- Raise error with paradigm-specific failure (e.g., "IFR ICC_slope = 1.2, exceeds valid range")
- Log failure to logs/step03_compute_icc.log
- Quit script immediately
- Master investigates variance component extraction issues from Step 2

---

#### Step 4: Compare ICC Across Paradigms

**Analysis Tool:** (determined by rq_tools - likely custom comparison logic)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_data_format)

**What Validation Checks:**
- Output files exist (data/step04_paradigm_icc_comparison.csv, data/step04_paradigm_summary.txt)
- Expected row count (3 pairwise comparisons)
- ICC differences in [-1, 1]
- Direction strings match sign of differences
- All comparisons present (IFR-ICR, IFR-IRE, ICR-IRE)
- Summary text contains paradigm order and interpretation

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Missing IFR-IRE comparison")
- Log failure to logs/step04_compare_paradigms.log
- Quit script immediately
- Master investigates ICC computation issues from Step 3

---

#### Step 5: Compare to Ch5 5.3.7

**Analysis Tool:** (determined by rq_tools - likely custom comparison logic)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_data_format)

**What Validation Checks:**
- Ch5 5.3.7 file exists (results/ch5/5.3.7/data/step03_icc_estimates.csv)
- Output files exist (data/step05_ch5_comparison.csv, data/step05_ch5_summary.txt)
- Expected row count (3 rows: one per paradigm)
- All ICC values in [0, 1]
- ICC differences in [-1, 1]
- No NaN values
- All 3 paradigms matched (IFR, ICR, IRE)
- Summary text contains overall pattern and interpretation

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Ch5 5.3.7 file missing")
- Log failure to logs/step05_compare_ch5.log
- Quit script immediately
- Master investigates Ch5 5.3.7 dependency (may need to run Ch5 5.3.7 first)

---

## Expected Data Formats

### Step 0 Output: data/step00_lmm_input.csv

**Format:** Long format (one row per observation: participant x test x paradigm)

**Dimensions:** 1200 rows x 6 columns

**Columns:**
- UID (string, participant identifier, e.g., P001)
- test (string, test session: T1, T2, T3, T4)
- TSVR_hours (float, actual time since encoding in hours, Decision D070)
- paradigm (string, retrieval paradigm: IFR, ICR, IRE)
- theta_confidence (float, IRT ability estimate)
- se_confidence (float, standard error)

**Data Types:**
- UID: object (string)
- test: object (string)
- TSVR_hours: float64
- paradigm: object (string)
- theta_confidence: float64
- se_confidence: float64

**Example Rows:**
```
UID,test,TSVR_hours,paradigm,theta_confidence,se_confidence
P001,T1,0.0,IFR,-0.52,0.18
P001,T1,0.0,ICR,0.23,0.16
P001,T1,0.0,IRE,0.45,0.15
P001,T2,24.5,IFR,-0.68,0.19
```

---

### Step 2 Output: data/step02_variance_components.csv

**Format:** One row per paradigm

**Dimensions:** 3 rows x 6 columns

**Columns:**
- paradigm (string: IFR, ICR, IRE)
- var_intercept (float: baseline variance)
- var_slope (float: slope variance)
- cov_int_slope (float: intercept-slope covariance)
- var_residual (float: within-person variance)
- var_total (float: sum of variance components)

**Data Types:**
- paradigm: object (string)
- var_intercept: float64
- var_slope: float64
- cov_int_slope: float64
- var_residual: float64
- var_total: float64

**Example Rows:**
```
paradigm,var_intercept,var_slope,cov_int_slope,var_residual,var_total
IFR,0.42,0.05,-0.02,0.35,0.82
ICR,0.38,0.03,0.01,0.40,0.81
IRE,0.35,0.02,0.00,0.42,0.79
```

---

### Step 3 Output: data/step03_icc_estimates.csv

**Format:** One row per paradigm

**Dimensions:** 3 rows x 6 columns

**Columns:**
- paradigm (string: IFR, ICR, IRE)
- ICC_intercept (float: baseline ICC)
- ICC_slope_simple (float: unconditional slope ICC)
- ICC_slope_conditional (float: conditional slope ICC at Day 6)
- interpretation_intercept (string: e.g., "Moderate trait variance")
- interpretation_slope (string: e.g., "Minimal trait variance")

**Data Types:**
- paradigm: object (string)
- ICC_intercept: float64
- ICC_slope_simple: float64
- ICC_slope_conditional: float64
- interpretation_intercept: object (string)
- interpretation_slope: object (string)

**Example Rows:**
```
paradigm,ICC_intercept,ICC_slope_simple,ICC_slope_conditional,interpretation_intercept,interpretation_slope
IFR,0.51,0.06,0.08,Moderate trait variance,Minimal trait variance
ICR,0.47,0.04,0.05,Moderate trait variance,Minimal trait variance
IRE,0.44,0.03,0.04,Moderate trait variance,Minimal trait variance
```

---

## Cross-RQ Dependencies

**This RQ depends on:**

**RQ 6.4.1** (Paradigm Confidence Trajectories)

**Required Files from RQ 6.4.1:**
- results/ch6/6.4.1/data/step03_theta_confidence_paradigm.csv (theta_confidence scores for IFR, ICR, IRE paradigms)

**Status Check:**
- rq_planner should verify results/ch6/6.4.1/status.yaml shows rq_results: success
- If RQ 6.4.1 incomplete: QUIT with "FAIL: RQ 6.4.1 must complete before this RQ (dependency)"

**Data Integration:**
- Step 0: Import theta_confidence_paradigm.csv from RQ 6.4.1
- Expected: 1200 rows (100 participants x 4 tests x 3 paradigms)
- Merge with TSVR_hours from master.xlsx

**Comparison Data:**

**Ch5 5.3.7** (Paradigm-Specific ICC for Accuracy Trajectories)

**Required Files from Ch5 5.3.7:**
- results/ch5/5.3.7/data/step03_icc_estimates.csv (accuracy ICC values by paradigm)

**Status Check:**
- Step 5 should verify Ch5 5.3.7 file exists before comparison
- If Ch5 5.3.7 incomplete: Log warning and skip Step 5 comparison (non-fatal)

**Rationale:**
RQ 6.4.1 provides theta_confidence scores (analysis input for this RQ). Ch5 5.3.7 provides accuracy ICC values (comparison benchmark for theoretical interpretation). This RQ tests whether paradigm-specific trait variance differs between confidence (5-level) and accuracy (dichotomous) data.

---

## Notes

**Naming Conventions:**

Per names.md conventions:
- Step numbers: step00, step01, step02, ... (zero-padded for sorting)
- Data files: data/stepNN_<description>.csv (all outputs in data/ folder per v4.1)
- Log files: logs/stepNN_<description>.log (execution logs only, one per step)
- Variable names: UID (participant), TSVR_hours (time), theta_confidence (ability), paradigm (retrieval type)

**Validation Philosophy:**

Per-step validation ensures errors caught at source, not 5 steps later. Each step has:
1. Validation requirement statement (tools MUST be used)
2. Substance validation criteria (4 layers: Output Files, Value Ranges, Data Quality, Log Validation)
3. Expected behavior on failure (raise error, log, quit, invoke g_debug)

**Tool Selection:**

rq_tools agent reads this plan and specifies exact tools from tool_inventory.md. Planner specifies WHAT needs to happen (LMM fitting, ICC computation), rq_tools specifies HOW (exact function calls).

**Code Generation:**

g_code agent generates Python scripts per rq_analysis instructions based on this plan. Each step becomes stepNN_<name>.py with embedded validation calls.

**Theoretical Context:**

This RQ tests whether retrieval support moderates trait-like individual differences in confidence decline. Comparison to Ch5 5.3.7 determines if 5-level confidence data reveals paradigm-specific slope variance that dichotomous accuracy data missed. If all paradigms show ICC_slope H 0 (replicating Ch5 findings), this confirms that forgetting rates are state-like regardless of measurement or retrieval paradigm.

---

**End of Analysis Plan**
