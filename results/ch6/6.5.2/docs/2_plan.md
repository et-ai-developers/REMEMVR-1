# Analysis Plan for RQ 6.5.2: Schema Confidence Calibration

**Created by:** rq_planner agent
**Date:** 2025-12-06
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This analysis examines metacognitive calibration across three schema congruence levels (Common, Congruent, Incongruent). The hypothesis is that congruent items will show overconfidence - high subjective confidence driven by schema-induced familiarity that does not reflect actual episodic memory accuracy.

The workflow involves 3 steps:
1. Merge accuracy theta (from RQ 5.4.1) and confidence theta (from RQ 6.5.1)
2. Compute calibration scores as standardized difference (confidence - accuracy)
3. Fit LMM to test Congruence main effect and Congruence x Time interaction with dual p-value reporting (Decision D068)

Expected runtime: Medium (5-15 minutes - no IRT calibration, LMM only with bootstrap)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (parametric and bootstrap) for all hypothesis tests
- Decision D070: TSVR as time variable inherited from source RQs (5.4.1, 6.5.1)

---

## Analysis Plan

This RQ requires 3 analysis steps:

### Step 0: Merge Accuracy and Confidence Theta Scores

**Dependencies:** None (first step, relies on completed source RQs)

**Complexity:** Low (data merging only, <1 minute)

**Input:**

**File 1:** results/ch5/5.4.1/data/step03_theta_scores.csv (accuracy theta by congruence)
**Source:** RQ 5.4.1 (Schema effects on accuracy)
**Format:** CSV with columns:
  - `composite_ID` (string, format: UID_test, e.g., P001_T1)
  - `theta_common` (float, IRT ability estimate for common items)
  - `theta_congruent` (float, IRT ability estimate for congruent items)
  - `theta_incongruent` (float, IRT ability estimate for incongruent items)
  - `se_common`, `se_congruent`, `se_incongruent` (float, standard errors)
**Expected Rows:** ~400 (100 participants x 4 tests)
**Expected Columns:** 7 (composite_ID + 3 theta + 3 SE)

**File 2:** results/ch6/6.5.1/data/step03_theta_confidence_scores.csv (confidence theta by congruence)
**Source:** RQ 6.5.1 (Schema effects on confidence)
**Format:** CSV with columns:
  - `composite_ID` (string, format: UID_test)
  - `theta_confidence_common` (float, confidence IRT estimate for common items)
  - `theta_confidence_congruent` (float, confidence IRT estimate for congruent items)
  - `theta_confidence_incongruent` (float, confidence IRT estimate for incongruent items)
  - `se_confidence_common`, `se_confidence_congruent`, `se_confidence_incongruent` (float, standard errors)
**Expected Rows:** ~400 (100 participants x 4 tests)
**Expected Columns:** 7 (composite_ID + 3 theta + 3 SE)

**Processing:**

1. Read accuracy theta file from RQ 5.4.1
2. Read confidence theta file from RQ 6.5.1
3. Merge on composite_ID (inner join - must have both accuracy and confidence)
4. Verify all composite_IDs matched (no unmatched rows)
5. Reshape to long format with congruence as factor:
   - Each composite_ID contributes 3 rows (Common, Congruent, Incongruent)
   - Columns: composite_ID, congruence, theta_accuracy, se_accuracy, theta_confidence, se_confidence
6. Parse composite_ID to extract UID and test (for LMM grouping)
7. Save merged data

**Output:**

**File:** data/step00_merged_accuracy_confidence.csv
**Format:** Long format (one row per composite_ID x congruence combination)
**Columns:**
  - `composite_ID` (string, format: UID_test)
  - `UID` (string, participant identifier, e.g., P001)
  - `test` (string, test session identifier: T1, T2, T3, T4)
  - `congruence` (string, categorical: Common, Congruent, Incongruent)
  - `theta_accuracy` (float, accuracy IRT estimate)
  - `se_accuracy` (float, accuracy standard error)
  - `theta_confidence` (float, confidence IRT estimate)
  - `se_confidence` (float, confidence standard error)
**Expected Rows:** ~1200 (400 composite_IDs x 3 congruence levels)

**Validation Requirement:**

Validation tools MUST be used after data merging tool execution. Specific validation tools will be determined by rq_tools based on data merging requirements. The rq_analysis agent will embed validation tool calls after the merging tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_merged_accuracy_confidence.csv exists (exact path)
- Expected rows: ~1200 (400 composite_IDs x 3 congruence levels, some data loss acceptable)
- Expected columns: 8 (composite_ID, UID, test, congruence, theta_accuracy, se_accuracy, theta_confidence, se_confidence)
- Data types: composite_ID (string), UID (string), test (string), congruence (string), theta/se columns (float64)

*Value Ranges:*
- theta_accuracy in [-3, 3] (typical IRT range)
- theta_confidence in [-3, 3] (typical IRT range)
- se_accuracy in [0.1, 1.5] (above 1.5 suggests unreliable estimates)
- se_confidence in [0.1, 1.5] (above 1.5 suggests unreliable estimates)
- congruence in {Common, Congruent, Incongruent} (categorical, exact case)
- test in {T1, T2, T3, T4} (categorical)

*Data Quality:*
- No NaN values in theta or congruence columns (critical for LMM)
- SE columns may have NaN if estimation failed (flag but do not fail)
- Expected N: 1140-1200 rows (95-100% retention, some data loss acceptable)
- No duplicate composite_ID x congruence combinations (unique key)
- All 3 congruence levels represented for each composite_ID (complete factorial design)
- UID count: 95-100 unique participants (some exclusions acceptable)

*Log Validation:*
- Required pattern: "Merge complete: {N} rows created" where N in [1140, 1200]
- Required pattern: "All composite_IDs matched successfully: 100%"
- Required pattern: "Congruence levels: Common, Congruent, Incongruent"
- Forbidden patterns: "ERROR", "Merge failed", "Unmatched composite_IDs"
- Acceptable warnings: "SE values > 1.5 detected for {N} observations" (unreliable estimates flagged)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Missing congruence level: Incongruent for composite_ID P001_T1")
- Log failure to logs/step00_merge_accuracy_confidence.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause (likely source RQ incompatibility)

---

### Step 1: Compute Calibration Scores

**Dependencies:** Step 0 (requires merged accuracy and confidence data)

**Complexity:** Low (arithmetic transformation, <1 minute)

**Input:**

**File:** data/step00_merged_accuracy_confidence.csv (from Step 0)
**Format:** Long format (one row per composite_ID x congruence)
**Columns:** composite_ID, UID, test, congruence, theta_accuracy, se_accuracy, theta_confidence, se_confidence
**Expected Rows:** ~1200

**Processing:**

1. Read merged data from Step 0
2. Z-standardize theta_accuracy WITHIN each congruence level (mean=0, SD=1 per congruence)
3. Z-standardize theta_confidence WITHIN each congruence level (mean=0, SD=1 per congruence)
4. Compute calibration score: calibration = theta_confidence_z - theta_accuracy_z
   - Positive calibration = overconfidence (confidence exceeds accuracy)
   - Negative calibration = underconfidence (accuracy exceeds confidence)
   - Zero calibration = perfect calibration (confidence matches accuracy)
5. Merge with TSVR timing data (if not already present in composite_ID parse)
6. Add TSVR_hours column for LMM time variable (Decision D070 inherited from source RQs)
7. Save calibration data

**Output:**

**File:** data/step01_calibration_by_congruence.csv
**Format:** Long format (one row per composite_ID x congruence)
**Columns:**
  - `composite_ID` (string)
  - `UID` (string, participant identifier)
  - `test` (string, test session: T1, T2, T3, T4)
  - `congruence` (string, categorical: Common, Congruent, Incongruent)
  - `theta_accuracy_z` (float, z-standardized accuracy within congruence level)
  - `theta_confidence_z` (float, z-standardized confidence within congruence level)
  - `calibration` (float, confidence_z - accuracy_z, range typically [-4, 4])
  - `TSVR_hours` (float, time since encoding in hours per Decision D070)
**Expected Rows:** ~1200 (same as Step 0 input)

**Validation Requirement:**

Validation tools MUST be used after calibration computation tool execution. Specific validation tools will be determined by rq_tools based on z-score standardization and arithmetic validation requirements. The rq_analysis agent will embed validation tool calls after the calibration tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_calibration_by_congruence.csv exists (exact path)
- Expected rows: ~1200 (same as Step 0 input, no data loss)
- Expected columns: 8 (composite_ID, UID, test, congruence, theta_accuracy_z, theta_confidence_z, calibration, TSVR_hours)
- Data types: composite_ID/UID/test/congruence (string), theta/calibration/TSVR (float64)

*Value Ranges:*
- theta_accuracy_z in [-4, 4] (z-scores, extreme outliers >4 sigma suspect)
- theta_confidence_z in [-4, 4] (z-scores, extreme outliers >4 sigma suspect)
- calibration in [-6, 6] (difference of z-scores, >6 indicates extreme miscalibration)
- TSVR_hours in [0, 200] hours (0=encoding, ~144=Day 6, 200=upper bound for late testing)
- congruence in {Common, Congruent, Incongruent} (categorical)
- test in {T1, T2, T3, T4} (categorical)

*Data Quality:*
- No NaN values in calibration column (critical for LMM dependent variable)
- Z-score standardization check: mean(theta_accuracy_z) ~= 0 within each congruence level (tolerance +/- 0.1)
- Z-score standardization check: SD(theta_accuracy_z) ~= 1 within each congruence level (tolerance +/- 0.1)
- Same standardization checks for theta_confidence_z
- Expected N: Same as Step 0 input (no data loss during computation)
- No duplicate composite_ID x congruence combinations
- TSVR_hours must increase with test number (T1 < T2 < T3 < T4 within each UID)

*Log Validation:*
- Required pattern: "Calibration computed: {N} observations" where N ~= 1200
- Required pattern: "Z-standardization within congruence levels: PASS" (mean ~0, SD ~1 checks)
- Required pattern: "TSVR merge successful: 100% matched"
- Forbidden patterns: "ERROR", "NaN calibration values", "Standardization FAIL"
- Acceptable warnings: "Extreme calibration values detected (|calibration| > 4): {N} observations" (flag outliers)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Z-standardization failed: mean(theta_accuracy_z) = 0.5 for Common (expected ~0)")
- Log failure to logs/step01_compute_calibration.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose root cause (likely standardization bug or data corruption)

---

### Step 2: Fit LMM and Test Congruence Effects

**Dependencies:** Step 1 (requires calibration scores)

**Complexity:** Medium (LMM fitting with bootstrap for dual p-values, 5-10 minutes)

**Input:**

**File:** data/step01_calibration_by_congruence.csv (from Step 1)
**Format:** Long format (one row per observation)
**Columns:** composite_ID, UID, test, congruence, theta_accuracy_z, theta_confidence_z, calibration, TSVR_hours
**Expected Rows:** ~1200

**Processing:**

1. Read calibration data from Step 1
2. Fit LMM with formula: calibration ~ Congruence * TSVR_hours + (TSVR_hours | UID)
   - Fixed effects: Congruence (3 levels: Common, Congruent, Incongruent), TSVR_hours (continuous time), Congruence x TSVR_hours interaction
   - Random effects: Random intercepts and random slopes for TSVR_hours by UID
   - Reference level: Common (baseline congruence)
3. Test Congruence main effect (Congruent vs Common, Incongruent vs Common)
4. Test Congruence x Time interaction (does schema effect on calibration change over time?)
5. Compute dual p-values for all effects (Decision D068):
   - Parametric p-values from LMM summary
   - Bootstrap p-values (1000 iterations, bias-corrected percentile method)
6. Post-hoc contrasts (if Congruence main effect significant):
   - Congruent vs Common (test overconfidence hypothesis: Congruent > Common)
   - Incongruent vs Common (test whether incongruent differs from baseline)
   - Congruent vs Incongruent (test whether congruent shows more overconfidence than incongruent)
   - Apply Bonferroni correction: alpha = 0.05 / 3 = 0.0167 for 3 contrasts
   - Report both uncorrected and Bonferroni-corrected p-values (Decision D068)
7. Compute effect sizes (Cohen's f-squared for fixed effects)
8. Save LMM summary, contrasts, and effect sizes

**Output:**

**File 1:** data/step02_lmm_summary.txt
**Format:** Plain text summary from statsmodels LMM
**Content:**
  - Model formula
  - Fixed effects table (coefficient, SE, z, p-value parametric, p-value bootstrap)
  - Random effects variance components
  - Model fit indices (AIC, BIC, log-likelihood)
  - Convergence status

**File 2:** data/step02_congruence_effects.csv
**Format:** CSV with hypothesis test results
**Columns:**
  - `effect` (string, e.g., "Congruence_main", "Congruence_x_Time")
  - `coefficient` (float, estimated effect size)
  - `SE` (float, standard error)
  - `z` (float, z-statistic)
  - `p_parametric` (float, parametric p-value from LMM)
  - `p_bootstrap` (float, bootstrap p-value, Decision D068)
  - `CI_lower` (float, 95% CI lower bound)
  - `CI_upper` (float, 95% CI upper bound)
**Expected Rows:** 6 (Intercept, Congruent, Incongruent, TSVR_hours, Congruent:TSVR, Incongruent:TSVR)

**File 3:** data/step02_post_hoc_contrasts.csv
**Format:** CSV with pairwise contrasts
**Columns:**
  - `contrast` (string, e.g., "Congruent - Common", "Incongruent - Common", "Congruent - Incongruent")
  - `estimate` (float, estimated difference in calibration)
  - `SE` (float, standard error)
  - `z` (float, z-statistic)
  - `p_uncorrected` (float, uncorrected p-value)
  - `p_bonferroni` (float, Bonferroni-corrected p-value for 3 contrasts)
  - `CI_lower` (float, 95% CI lower bound)
  - `CI_upper` (float, 95% CI upper bound)
**Expected Rows:** 3 (Congruent-Common, Incongruent-Common, Congruent-Incongruent)

**File 4:** data/step02_effect_sizes.csv
**Format:** CSV with Cohen's f-squared
**Columns:**
  - `effect` (string, fixed effect name)
  - `f_squared` (float, Cohen's f-squared effect size)
  - `interpretation` (string, small/medium/large per Cohen's thresholds: 0.02/0.15/0.35)
**Expected Rows:** 5 (Congruent, Incongruent, TSVR_hours, Congruent:TSVR, Incongruent:TSVR)

**Validation Requirement:**

Validation tools MUST be used after LMM fitting tool execution. Specific validation tools will be determined by rq_tools based on LMM convergence, residual diagnostics, and dual p-value reporting requirements (Decision D068). The rq_analysis agent will embed validation tool calls after the LMM tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_lmm_summary.txt exists (plain text summary)
- data/step02_congruence_effects.csv exists (6 rows, 8 columns)
- data/step02_post_hoc_contrasts.csv exists (3 rows, 8 columns)
- data/step02_effect_sizes.csv exists (5 rows, 3 columns)
- All files non-empty (>100 bytes for text, >50 bytes for CSV)

*Value Ranges:*
- Coefficients in [-5, 5] (typical range for standardized calibration, >5 suggests estimation error)
- SE in [0.01, 2.0] (SE > 2.0 suggests poor precision, SE < 0.01 suspiciously low)
- p-values in [0, 1] (both parametric and bootstrap)
- CI bounds: CI_lower < coefficient < CI_upper (logical consistency)
- f_squared >= 0 (Cohen's f-squared non-negative by definition)

*Data Quality:*
- LMM convergence: "Converged: True" in summary.txt (required)
- No NaN coefficients or p-values (model estimation must succeed)
- Dual p-values present: BOTH p_parametric AND p_bootstrap for all effects (Decision D068)
- Bonferroni correction applied: p_bonferroni = p_uncorrected * 3 (or capped at 1.0)
- Expected effect directions (hypothesis check, not validation failure):
  - Congruent > Common (positive coefficient, overconfidence hypothesis)
  - Test in log, but do not fail if effect direction unexpected (scientific question)
- Random effects variance > 0 (negative variance indicates convergence failure)

*Log Validation:*
- Required pattern: "Model converged: True"
- Required pattern: "Dual p-values computed: parametric and bootstrap" (Decision D068)
- Required pattern: "Post-hoc contrasts: 3 comparisons with Bonferroni correction"
- Required pattern: "Effect sizes computed: Cohen's f-squared"
- Forbidden patterns: "ERROR", "Model failed to converge", "Singular fit", "Variance component negative"
- Acceptable warnings: "Bootstrap convergence warnings: {N} iterations failed" (if <5% failure rate)
- Acceptable warnings: "Residual normality assumption violated (KS test p < 0.05)" (LMM robust to moderate violations)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Model convergence failed: singular fit detected")
- Log failure to logs/step02_fit_lmm_congruence.log
- Quit script immediately (do NOT create plots or results)
- g_debug invoked to diagnose root cause (likely insufficient data, model misspecification, or convergence issues)

---

## Expected Data Formats

### Step 0 -> Step 1 Transformation

**Input (Step 0 output):** Wide theta format per congruence level
- Format: One row per composite_ID, separate columns for each congruence level
- Columns: composite_ID, theta_common, theta_congruent, theta_incongruent (and SE columns)

**Output (Step 1 input):** Long theta format with congruence as factor
- Format: One row per composite_ID x congruence combination
- Transformation: Reshape from wide to long, creating congruence factor
- Columns: composite_ID, UID, test, congruence, theta_accuracy, se_accuracy, theta_confidence, se_confidence

**Reshape Logic:**
- Parse composite_ID to extract UID and test (e.g., "P001_T1" -> UID="P001", test="T1")
- Stack congruence levels: each composite_ID becomes 3 rows (Common, Congruent, Incongruent)
- Congruence column values: "Common", "Congruent", "Incongruent" (exact case, categorical)

### Step 1 -> Step 2 Transformation

**Input (Step 1 output):** Long format with z-standardized theta and calibration scores
- Format: One row per observation (composite_ID x congruence)
- Columns: composite_ID, UID, test, congruence, theta_accuracy_z, theta_confidence_z, calibration, TSVR_hours

**LMM Preparation:**
- No additional transformation needed (already in long format)
- Congruence factor: Categorical with 3 levels, reference = "Common"
- TSVR_hours: Continuous time variable (Decision D070)
- Grouping variable: UID (random effects by participant)
- Dependent variable: calibration (continuous, typically [-4, 4] range)

**Column Naming Conventions:**
Per names.md:
- UID: participant identifier (no underscore, format: P### with leading zeros)
- test: test session identifier (T1, T2, T3, T4 for Days 0, 1, 3, 6)
- TSVR_hours: time variable for LMM (uppercase acronym + underscore + unit per Decision D070)
- calibration: computed difference (lowercase, descriptive name)

---

## Cross-RQ Dependencies

### Dependency Type 2: DERIVED Data from Other RQs (Dependencies Exist)

**This RQ requires outputs from:**

- **RQ 5.4.1** (Schema Effects on Accuracy Trajectories)
  - File: results/ch5/5.4.1/data/step03_theta_scores.csv
  - Used in: Step 0 (merge accuracy theta by congruence level)
  - Rationale: RQ 5.4.1 provides accuracy theta estimates for Common, Congruent, Incongruent items. This RQ uses those estimates as the "objective performance" component of calibration.
  - Expected structure: composite_ID, theta_common, theta_congruent, theta_incongruent, se_common, se_congruent, se_incongruent

- **RQ 6.5.1** (Schema Effects on Confidence Trajectories)
  - File: results/ch6/6.5.1/data/step03_theta_confidence_scores.csv
  - Used in: Step 0 (merge confidence theta by congruence level)
  - Rationale: RQ 6.5.1 provides confidence theta estimates for Common, Congruent, Incongruent items. This RQ uses those estimates as the "subjective confidence" component of calibration.
  - Expected structure: composite_ID, theta_confidence_common, theta_confidence_congruent, theta_confidence_incongruent, se_confidence_common, se_confidence_congruent, se_confidence_incongruent

**Execution Order Constraint:**
1. RQ 5.4.1 must complete Steps 0-3 (IRT calibration for accuracy by congruence)
2. RQ 6.5.1 must complete Steps 0-3 (IRT calibration for confidence by congruence)
3. This RQ (6.5.2) executes after both dependencies complete

**Data Source Boundaries:**
- **RAW data:** None (this RQ does not extract from master.xlsx)
- **DERIVED data:** 100% derived from RQ 5.4.1 and 6.5.1 theta outputs
- **Scope:** This RQ does NOT re-calibrate IRT models (uses pre-computed theta scores from source RQs)

**Validation:**
- Step 0: Check results/ch5/5.4.1/data/step03_theta_scores.csv exists (EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch6/6.5.1/data/step03_theta_confidence_scores.csv exists (EXPECTATIONS ERROR if absent)
- If either file missing -> quit with error -> user must execute dependency RQs first

**Critical Alignment Requirement:**
- Both source RQs MUST use same 3-level congruence categorization:
  - Common = i1, i2 tags
  - Congruent = i3, i4 tags
  - Incongruent = i5, i6 tags
- If categorization mismatches, merge will fail (detected in Step 0 validation)

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

#### Step 0: Merge Accuracy and Confidence Theta Scores

**Analysis Tool:** (determined by rq_tools - likely pandas merge operations or custom tools.data function)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_data_format + validate_dataframe_structure)

**What Validation Checks (TECHNICAL - rq_inspect scope):**
- Output file exists (data/step00_merged_accuracy_confidence.csv)
- Expected row count (~1200 rows: 400 composite_IDs x 3 congruence levels)
- Expected column count (8 columns: composite_ID, UID, test, congruence, theta_accuracy, se_accuracy, theta_confidence, se_confidence)
- All composite_IDs matched between source files (100% match rate required)
- No NaN in theta columns (critical for downstream calibration computation)
- Congruence factor has exactly 3 levels: Common, Congruent, Incongruent (case-sensitive)
- composite_ID format correct (UID_test pattern)

**NOTE:** Technical validation (files exist, formats correct, values in bounds) checked by rq_inspect DURING analysis. Scientific plausibility (effect directions, theoretical coherence) checked by rq_results AFTER all analysis complete.

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Merge incomplete: 50 composite_IDs unmatched")
- Log failure to logs/step00_merge_accuracy_confidence.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked by master to diagnose root cause (likely source RQ file structure mismatch)

---

#### Step 1: Compute Calibration Scores

**Analysis Tool:** (determined by rq_tools - likely pandas operations with z-score standardization)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_standardization + validate_numeric_range)

**What Validation Checks:**
- Output file exists (data/step01_calibration_by_congruence.csv)
- Expected row count (same as Step 0 input, no data loss)
- Z-standardization correctness:
  - mean(theta_accuracy_z) ~= 0 within each congruence level (tolerance +/- 0.1)
  - SD(theta_accuracy_z) ~= 1 within each congruence level (tolerance +/- 0.1)
  - Same checks for theta_confidence_z
- Calibration values in reasonable range (typically [-6, 6], extreme outliers flagged)
- No NaN in calibration column (critical for LMM dependent variable)
- TSVR_hours increases with test number within each UID (temporal consistency)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Z-standardization failed: mean(theta_confidence_z) = 0.8 for Congruent (expected ~0)")
- Log failure to logs/step01_compute_calibration.log
- Quit script immediately
- g_debug invoked to diagnose (likely standardization algorithm bug or data corruption)

---

#### Step 2: Fit LMM and Test Congruence Effects

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.fit_lmm_trajectory_tsvr)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_lmm_convergence + validate_hypothesis_test_dual_pvalues + validate_contrasts_dual_pvalues)

**What Validation Checks:**
- Output files exist (lmm_summary.txt, congruence_effects.csv, post_hoc_contrasts.csv, effect_sizes.csv)
- Model convergence successful (log reports "Converged: True")
- Dual p-values present for all effects (Decision D068):
  - Both p_parametric and p_bootstrap columns in congruence_effects.csv
  - Both p_uncorrected and p_bonferroni columns in post_hoc_contrasts.csv
- Random effects variance components > 0 (negative variance indicates convergence failure)
- Coefficients and SEs in reasonable ranges (no extreme values suggesting estimation error)
- Bonferroni correction applied correctly (p_bonferroni = min(p_uncorrected * 3, 1.0))
- Effect sizes non-negative (Cohen's f-squared >= 0 by definition)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Model convergence failed: singular fit detected", "Missing bootstrap p-values (Decision D068 violation)")
- Log failure to logs/step02_fit_lmm_congruence.log
- Quit script immediately
- g_debug invoked to diagnose (common causes: insufficient data, model too complex for data, convergence issues)

---

## Summary

**Total Steps:** 3 (Step 0: merge, Step 1: calibration, Step 2: LMM)

**Estimated Runtime:** Medium (5-15 minutes)
- Step 0: <1 minute (data merging)
- Step 1: <1 minute (arithmetic transformation)
- Step 2: 5-10 minutes (LMM fitting with bootstrap for dual p-values)

**Cross-RQ Dependencies:** 2 source RQs required
- RQ 5.4.1 (accuracy theta by congruence)
- RQ 6.5.1 (confidence theta by congruence)

**Primary Outputs:**
- data/step01_calibration_by_congruence.csv (calibration scores for all observations)
- data/step02_congruence_effects.csv (hypothesis test results with dual p-values)
- data/step02_post_hoc_contrasts.csv (pairwise contrasts testing overconfidence hypothesis)
- data/step02_effect_sizes.csv (Cohen's f-squared for fixed effects)

**Validation Coverage:** 100% (all 3 steps have validation requirements with 4-layer substance criteria)

**Key Hypothesis Test:** Congruent > Common calibration (overconfidence for schema-congruent items)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent
