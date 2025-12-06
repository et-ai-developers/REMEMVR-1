# Analysis Plan for RQ 6.1.4: ICC Decomposition

**Created by:** rq_planner agent
**Date:** 2025-12-06
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This analysis plan decomposes variance in confidence trajectories into trait-like (intercept: baseline confidence) and state-like (residual: within-person fluctuation) components, with specific focus on slope variance (forgetting rate individual differences). The central research question tests whether 5-level ordinal confidence data reveals detectable slope variance that dichotomous accuracy data from Chapter 5 could not resolve (measurement precision hypothesis).

The workflow comprises 6 analysis steps:
1. Load best-fitting LMM from RQ 6.1.1 (functional form winner with random intercepts and slopes)
2. Extract 4 variance components (intercept, slope, covariance, residual)
3. Compute 3 ICC estimates following Hoffman & Stawski (2009) methodology
4. Extract 100 participant-level random effects (REQUIRED for downstream clustering in RQ 6.1.5)
5. Test intercept-slope correlation (baseline-decline relationship)
6. CRITICAL COMPARISON: Test if ICC_slope_confidence differs significantly from ICC_slope_accuracy (0.0005 from Chapter 5 RQ 5.1.4)

Estimated total runtime: Low (10-15 minutes) - No model fitting, only variance decomposition from existing LMM object.

**Key Decision Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni) for intercept-slope correlation and Chapter 5 comparison tests

---

## Analysis Plan

### Step 0: Load Best-Fitting LMM

**Dependencies:** None (first step)
**Complexity:** Low (1-2 minutes, file loading only)

**Purpose:** Load fitted LMM model object from RQ 6.1.1 functional form comparison winner

**Input:**

**File:** results/ch6/6.1.1/data/step06_best_model.pkl
**Source:** RQ 6.1.1 Step 6 (functional form comparison via AIC, saved winner model object)
**Format:** Python pickle file containing fitted statsmodels MixedLM object
**Expected Structure:**
- Random effects structure: Random intercepts + random slopes for time (TSVR_hours)
- Formula: theta ~ f(TSVR_hours) + (1 + TSVR_hours | UID)
- f(TSVR_hours) = functional form determined by RQ 6.1.1 (Linear, Quadratic, Log, etc.)

**Processing:**
- Load pickle file using tools.config.load_model_from_file or equivalent
- Verify model converged successfully (check model.converged attribute)
- Verify random effects structure includes both intercept and slope variance
- Extract model summary for metadata documentation

**Output:**

**File 1:** data/step00_model_metadata.txt
**Format:** Plain text summary
**Contents:**
- Model formula (functional form of time effect)
- Sample size (N participants, N observations)
- Random effects structure confirmation
- Convergence status
- Source file path and load timestamp

**Validation Requirement:**

Validation tools MUST be used after model loading. Specific validation tools determined by rq_tools based on LMM object validation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_model_metadata.txt exists (exact path)
- File size > 0 bytes (not empty)
- Contains convergence status line

*Value Ranges:*
- N/A (metadata file, no numeric outputs to validate)

*Data Quality:*
- Model object loaded successfully (Python object type: statsmodels.regression.mixed_linear_model.MixedLMResults)
- Random effects structure confirmed: variance components for both intercept and slope present
- Convergence status = True (model estimation succeeded)

*Log Validation:*
- Required pattern: "Model loaded successfully from results/ch6/6.1.1/data/step06_best_model.pkl"
- Required pattern: "Model converged: True"
- Required pattern: "Random effects structure confirmed: intercept + slope"
- Forbidden patterns: "ERROR", "FileNotFoundError", "Model did not converge"
- Acceptable warnings: None expected for file loading

**Expected Behavior on Validation Failure:**
- If file missing: Raise FileNotFoundError with message "RQ 6.1.1 must complete Step 6 (functional form comparison) before RQ 6.1.4 can run"
- If model did not converge: Raise ValueError with message "Loaded model shows convergence failure - RQ 6.1.1 Step 6 output invalid"
- If random effects structure incorrect: Raise ValueError with message "Model lacks random slope variance - cannot compute ICC_slope"
- Log failure to logs/step00_load_best_model.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause (likely RQ 6.1.1 incomplete or model specification error)

---

### Step 1: Extract Variance Components

**Dependencies:** Step 0 (requires loaded LMM model object)
**Complexity:** Low (1-2 minutes, extraction from fitted model)

**Purpose:** Extract 4 variance components from LMM random effects for ICC computation

**Input:**

**File:** Loaded model object from Step 0 (in memory, not file-based)
**Structure:** statsmodels MixedLMResults object with fitted random effects

**Processing:**
- Extract random effects covariance matrix (model.cov_re attribute)
- Decompose into 4 components:
  1. var_intercept: Variance of random intercepts (diagonal element [0,0])
  2. var_slope: Variance of random slopes for TSVR_hours (diagonal element [1,1])
  3. cov_int_slope: Covariance between intercepts and slopes (off-diagonal element [0,1])
  4. var_residual: Residual variance (model.scale attribute)
- Compute correlation from covariance: cor_int_slope = cov_int_slope / sqrt(var_intercept * var_slope)

**Output:**

**File:** data/step01_variance_components.csv
**Format:** CSV with 4 rows (one per component)
**Columns:**
- component (string): {"var_intercept", "var_slope", "cov_int_slope", "var_residual"}
- value (float): Variance/covariance estimate
- SE (float): Standard error of estimate (if available from model, else NA)
**Expected Rows:** 4 (one per variance component)

**Validation Requirement:**

Validation tools MUST be used after variance extraction. Specific validation tools determined by rq_tools based on variance component validation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_variance_components.csv exists (exact path)
- Expected rows: 4 (var_intercept, var_slope, cov_int_slope, var_residual)
- Expected columns: 3 (component, value, SE)
- Data types: component (object/string), value (float64), SE (float64)

*Value Ranges:*
- var_intercept > 0 (variance must be positive)
- var_slope >= 0 (can be zero if no individual differences in forgetting rate)
- var_residual > 0 (residual variance must be positive)
- cov_int_slope unrestricted (can be negative, zero, or positive)
- |cov_int_slope| <= sqrt(var_intercept * var_slope) (mathematical constraint from correlation bounds)

*Data Quality:*
- All 4 components present (no missing rows)
- No NaN values in value column (all components successfully extracted)
- SE column may contain NA for var_residual (acceptable - residual SE not always reported by statsmodels)

*Log Validation:*
- Required pattern: "Extracted 4 variance components from LMM"
- Required pattern: "var_intercept = [value]" (confirms intercept variance extracted)
- Required pattern: "var_slope = [value]" (confirms slope variance extracted)
- Required pattern: "Correlation(intercept, slope) = [value]" (confirms covariance converted to correlation)
- Forbidden patterns: "ERROR", "Variance component extraction failed", "NaN variance"
- Acceptable warnings: "Standard error not available for var_residual" (statsmodels limitation)

**Expected Behavior on Validation Failure:**
- If variance components negative: Raise ValueError with message "Negative variance detected - model estimation error or boundary issue"
- If covariance exceeds correlation bounds: Raise ValueError with message "Invalid covariance magnitude - exceeds sqrt(var_intercept * var_slope)"
- If NaN values present: Raise ValueError with message "Variance extraction failed - NaN in variance components"
- Log failure to logs/step01_extract_variance_components.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose root cause (likely model convergence issue or statsmodels API change)

---

### Step 2: Compute ICC Estimates

**Dependencies:** Step 1 (requires variance components)
**Complexity:** Low (1-2 minutes, mathematical computation from variances)

**Purpose:** Compute 3 ICC estimates following Hoffman & Stawski (2009) methodology for longitudinal data

**Input:**

**File:** data/step01_variance_components.csv
**Expected Columns:** component, value, SE
**Expected Rows:** 4 (var_intercept, var_slope, cov_int_slope, var_residual)

**Processing:**

Compute 3 ICC estimates using extracted variance components:

1. **ICC_intercept:** Proportion of total variance attributable to stable individual differences in baseline confidence
   - Formula: var_intercept / (var_intercept + var_slope * mean_time^2 + var_residual)
   - mean_time: Average TSVR_hours across all observations (compute from RQ 6.1.1 data or use typical value ~72 hours for midpoint)
   - Interpretation: High ICC_intercept (>0.30) indicates substantial baseline variance

2. **ICC_slope_simple:** Proportion of slope variance relative to total variance in change rates
   - Formula: var_slope / (var_slope + var_residual / mean_time^2)
   - Interpretation: High ICC_slope (>0.10) indicates detectable individual differences in forgetting rate
   - CRITICAL for RQ hypothesis: If ICC_slope_confidence > 0.10 but ICC_slope_accuracy = 0.0005, supports measurement artifact hypothesis

3. **ICC_slope_conditional:** Slope variance proportion conditional on final timepoint (Day 6 = 144 hours)
   - Formula: var_slope / (var_slope + var_residual / 144^2)
   - Interpretation: Slope variance at final assessment (when forgetting most pronounced)

**Output:**

**File:** data/step02_icc_estimates.csv
**Format:** CSV with 3 rows (one per ICC type)
**Columns:**
- icc_type (string): {"ICC_intercept", "ICC_slope_simple", "ICC_slope_conditional"}
- value (float): ICC estimate in [0, 1]
- interpretation (string): Verbal interpretation {"negligible" (<0.05), "small" (0.05-0.10), "moderate" (0.10-0.30), "substantial" (>0.30)}
**Expected Rows:** 3 (one per ICC type)

**Validation Requirement:**

Validation tools MUST be used after ICC computation. Specific validation tools determined by rq_tools based on ICC validation requirements (tools.validation.validate_icc_bounds).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_icc_estimates.csv exists (exact path)
- Expected rows: 3 (ICC_intercept, ICC_slope_simple, ICC_slope_conditional)
- Expected columns: 3 (icc_type, value, interpretation)
- Data types: icc_type (object/string), value (float64), interpretation (object/string)

*Value Ranges:*
- All ICC values in [0, 1] (mathematical constraint - proportion of variance)
- ICC_intercept expected > 0.30 based on Chapter 5 parallels (substantial baseline variance)
- ICC_slope_simple CRITICAL: >0.10 supports measurement artifact hypothesis, near 0 supports universal forgetting hypothesis
- ICC_slope_conditional typically >= ICC_slope_simple (conditional at extreme timepoint)

*Data Quality:*
- All 3 ICC types present (no missing rows)
- No NaN values in value column
- Interpretation column populated for all rows (consistent with value thresholds)
- ICC_slope_conditional >= ICC_slope_simple (mathematical property - conditional variance at extreme time should not be smaller)

*Log Validation:*
- Required pattern: "Computed 3 ICC estimates following Hoffman & Stawski (2009)"
- Required pattern: "ICC_intercept = [value] ([interpretation])"
- Required pattern: "ICC_slope_simple = [value] ([interpretation])"
- Required pattern: "ICC_slope_conditional = [value] ([interpretation])"
- Required pattern: "All ICC values in valid range [0, 1]"
- Forbidden patterns: "ERROR", "ICC out of bounds", "NaN ICC"
- Acceptable warnings: None expected for ICC computation

**Expected Behavior on Validation Failure:**
- If ICC out of [0, 1] bounds: Raise ValueError with message "ICC value [value] exceeds valid range [0, 1] - variance component error"
- If ICC_slope_conditional < ICC_slope_simple: Raise ValueError with message "Conditional ICC cannot be smaller than simple ICC - formula error"
- If NaN values present: Raise ValueError with message "ICC computation failed - NaN in ICC estimates"
- Log failure to logs/step02_compute_icc_estimates.log
- Quit script immediately (do NOT proceed to Step 3)
- g_debug invoked to diagnose root cause (likely variance extraction error or division by zero)

---

### Step 3: Extract Participant-Level Random Effects

**Dependencies:** Step 0 (requires loaded LMM model object)
**Complexity:** Low (1-2 minutes, extraction from fitted model)

**Purpose:** Extract 100 participant-level random effects (intercept + slope) for downstream clustering analysis in RQ 6.1.5

**Input:**

**File:** Loaded model object from Step 0 (in memory)
**Structure:** statsmodels MixedLMResults object with fitted random effects

**Processing:**
- Extract participant-level random effects from model.random_effects attribute
- Structure: Dictionary with UID as keys, random effects array as values
- Each participant has 2 random effects: [intercept_deviation, slope_deviation]
- Convert to DataFrame with columns: UID, random_intercept, random_slope

**Output:**

**File:** data/step03_random_effects.csv
**Format:** CSV with 100 rows (one per participant)
**Columns:**
- UID (string): Participant identifier (format: P### with leading zeros)
- random_intercept (float): Participant-specific intercept deviation from population mean
- random_slope (float): Participant-specific slope deviation from population mean slope
**Expected Rows:** 100 (exactly N participants in RQ 6.1.1 sample)

**CRITICAL NOTE:** This output is REQUIRED for RQ 6.1.5 (Clustering Analysis), which uses random_intercept + random_slope as input features for K-means clustering. If this file is missing or incomplete, RQ 6.1.5 cannot execute.

**Validation Requirement:**

Validation tools MUST be used after random effects extraction. Specific validation tools determined by rq_tools based on random effects validation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_random_effects.csv exists (exact path)
- Expected rows: 100 (exactly N participants)
- Expected columns: 3 (UID, random_intercept, random_slope)
- Data types: UID (object/string), random_intercept (float64), random_slope (float64)

*Value Ranges:*
- random_intercept: Typically in [-2, +2] SD units (extreme values >3 SD rare but possible)
- random_slope: Typically in [-0.05, +0.05] per hour (extreme values rare but possible)
- Both intercept and slope distributions should be approximately normal (Q-Q plot visual check)

*Data Quality:*
- Exactly 100 rows (all participants present, no duplicates, no missing)
- No NaN values in any column (all participants successfully estimated)
- UID format correct: Pxxx pattern with leading zeros (e.g., P001, P050, P100)
- No duplicate UIDs (each participant appears exactly once)

*Log Validation:*
- Required pattern: "Extracted random effects for 100 participants"
- Required pattern: "Random intercept range: [min] to [max]"
- Required pattern: "Random slope range: [min] to [max]"
- Required pattern: "No NaN values in random effects"
- Forbidden patterns: "ERROR", "Missing random effects for participant", "NaN in random effects"
- Acceptable warnings: "Participant [UID] has extreme random intercept (>2 SD)" (rare but acceptable)

**Expected Behavior on Validation Failure:**
- If N != 100 rows: Raise ValueError with message "Expected 100 participants, found [N] - incomplete random effects extraction"
- If NaN values present: Raise ValueError with message "NaN random effects for participant [UID] - model estimation incomplete"
- If duplicate UIDs: Raise ValueError with message "Duplicate participant [UID] in random effects - data integrity error"
- Log failure to logs/step03_extract_random_effects.log
- Quit script immediately (do NOT proceed to Step 4)
- g_debug invoked to diagnose root cause (likely model convergence issue for specific participants)

---

### Step 4: Test Intercept-Slope Correlation

**Dependencies:** Step 3 (requires participant-level random effects)
**Complexity:** Low (1-2 minutes, Pearson correlation with dual p-value reporting)

**Purpose:** Test relationship between baseline confidence (intercept) and forgetting rate (slope) - Do high baseline individuals show faster or slower decline?

**Input:**

**File:** data/step03_random_effects.csv
**Expected Columns:** UID, random_intercept, random_slope
**Expected Rows:** 100 participants

**Processing:**
- Compute Pearson correlation between random_intercept and random_slope
- Report correlation coefficient r, 95% confidence interval, and sample size N
- Compute DUAL p-values per Decision D068:
  1. Uncorrected p-value from Pearson correlation test
  2. Bonferroni-corrected p-value (multiply by 1 since this is single planned comparison, not exploratory)
- Interpret correlation direction and magnitude:
  - Positive r: Higher baseline confidence -> slower forgetting (protective effect)
  - Negative r: Higher baseline confidence -> faster forgetting (regression to mean)
  - |r| < 0.10: negligible, 0.10-0.30: small, 0.30-0.50: moderate, >0.50: large

**Output:**

**File:** data/step04_intercept_slope_correlation.csv
**Format:** CSV with 1 row (single correlation test)
**Columns:**
- correlation_r (float): Pearson correlation coefficient in [-1, 1]
- CI_lower (float): Lower bound of 95% confidence interval
- CI_upper (float): Upper bound of 95% confidence interval
- N (int): Sample size (should be 100)
- p_uncorrected (float): Uncorrected p-value from correlation test
- p_bonferroni (float): Bonferroni-corrected p-value (same as uncorrected for single test)
- interpretation (string): Verbal interpretation of correlation direction and magnitude
**Expected Rows:** 1 (single correlation test)

**Validation Requirement:**

Validation tools MUST be used after correlation test. Specific validation tools determined by rq_tools based on correlation validation requirements (tools.validation.validate_correlation_test_d068 for dual p-value compliance).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_intercept_slope_correlation.csv exists (exact path)
- Expected rows: 1 (single correlation test)
- Expected columns: 7 (correlation_r, CI_lower, CI_upper, N, p_uncorrected, p_bonferroni, interpretation)
- Data types: correlation_r (float64), CI bounds (float64), N (int64), p-values (float64), interpretation (object/string)

*Value Ranges:*
- correlation_r in [-1, 1] (mathematical constraint)
- CI_lower < correlation_r < CI_upper (confidence interval bounds correlation)
- N = 100 (sample size matches participant count)
- p_uncorrected in [0, 1] (p-value valid range)
- p_bonferroni = p_uncorrected (single test, no correction needed)

*Data Quality:*
- Exactly 1 row (single test)
- No NaN values in any column
- CI_lower < CI_upper (valid confidence interval)
- Interpretation consistent with correlation_r magnitude and direction

*Log Validation:*
- Required pattern: "Pearson correlation computed: r = [value], p = [p_uncorrected]"
- Required pattern: "95% CI: [[CI_lower], [CI_upper]]"
- Required pattern: "Dual p-values: uncorrected = [p_uncorrected], Bonferroni = [p_bonferroni]"
- Required pattern: "Decision D068 compliance: PASS"
- Forbidden patterns: "ERROR", "NaN correlation", "Invalid p-value"
- Acceptable warnings: "Correlation not significant at alpha = 0.05" (acceptable finding)

**Expected Behavior on Validation Failure:**
- If correlation out of bounds: Raise ValueError with message "Correlation [r] exceeds valid range [-1, 1]"
- If p-values missing or invalid: Raise ValueError with message "Missing dual p-values - Decision D068 violation"
- If CI_lower > CI_upper: Raise ValueError with message "Invalid confidence interval bounds"
- Log failure to logs/step04_test_intercept_slope_correlation.log
- Quit script immediately (do NOT proceed to Step 5)
- g_debug invoked to diagnose root cause (likely statistical computation error)

---

### Step 5: Compare ICC_slope with Chapter 5 Accuracy Data

**Dependencies:** Step 2 (requires ICC_slope_simple from confidence data)
**Complexity:** Low (1-2 minutes, comparison with known value from Chapter 5)

**Purpose:** CRITICAL COMPARISON - Test if ICC_slope differs significantly between 5-level ordinal confidence data (this RQ) versus dichotomous accuracy data (Chapter 5 RQ 5.1.4 = 0.0005)

**Input:**

**File 1:** data/step02_icc_estimates.csv (from this RQ)
**Required Row:** ICC_slope_simple (confidence data from this RQ)

**File 2:** Known value from Chapter 5 RQ 5.1.4
**Source:** Chapter 5 RQ 5.1.4 reported ICC_slope_accuracy = 0.0005 (near-zero slope variance with dichotomous data)
**Note:** This is a KNOWN VALUE from prior analysis, not a file to load. Hard-code ICC_slope_accuracy = 0.0005 for comparison.

**Processing:**

1. Extract ICC_slope_simple from Step 2 output (confidence data)
2. Compare with ICC_slope_accuracy = 0.0005 (dichotomous accuracy data from Chapter 5)
3. Compute difference: delta_ICC = ICC_slope_confidence - ICC_slope_accuracy
4. Compute ratio: ratio_ICC = ICC_slope_confidence / ICC_slope_accuracy
5. Test significance:
   - If ICC_slope_confidence > 0.10 AND ICC_slope_accuracy = 0.0005: Difference is practically significant (20x increase)
   - If ICC_slope_confidence near 0 (e.g., <0.05): Replicates Chapter 5 finding despite increased precision
6. Interpret findings:
   - **Measurement Artifact Hypothesis SUPPORTED:** If ICC_slope_confidence > 0.10 (ordinal data reveals variance)
   - **Universal Forgetting Hypothesis SUPPORTED:** If ICC_slope_confidence near 0 (slope variance minimal regardless of precision)

**Output:**

**File:** data/step05_ch5_icc_comparison.csv
**Format:** CSV with 1 row (single comparison)
**Columns:**
- ICC_slope_confidence (float): From this RQ Step 2 (5-level ordinal data)
- ICC_slope_accuracy (float): From Chapter 5 RQ 5.1.4 (dichotomous data, hard-coded 0.0005)
- delta_ICC (float): Difference (confidence - accuracy)
- ratio_ICC (float): Ratio (confidence / accuracy)
- hypothesis_supported (string): {"Measurement Artifact" if confidence >0.10, "Universal Forgetting" if confidence <0.05, "Inconclusive" if 0.05-0.10}
- interpretation (string): Verbal interpretation of comparison results
**Expected Rows:** 1 (single comparison)

**Validation Requirement:**

Validation tools MUST be used after comparison. Specific validation tools determined by rq_tools based on comparison validation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_ch5_icc_comparison.csv exists (exact path)
- Expected rows: 1 (single comparison)
- Expected columns: 6 (ICC_slope_confidence, ICC_slope_accuracy, delta_ICC, ratio_ICC, hypothesis_supported, interpretation)
- Data types: ICC values (float64), delta (float64), ratio (float64), hypothesis/interpretation (object/string)

*Value Ranges:*
- ICC_slope_confidence in [0, 1] (valid ICC range)
- ICC_slope_accuracy = 0.0005 exactly (hard-coded from Chapter 5)
- delta_ICC unrestricted (can be negative if confidence < accuracy, though unlikely)
- ratio_ICC > 0 (both ICCs non-negative)

*Data Quality:*
- Exactly 1 row (single comparison)
- No NaN values in any column
- hypothesis_supported in {"Measurement Artifact", "Universal Forgetting", "Inconclusive"}
- Interpretation consistent with hypothesis_supported classification

*Log Validation:*
- Required pattern: "ICC_slope_confidence = [value] (5-level ordinal data from RQ 6.1.4)"
- Required pattern: "ICC_slope_accuracy = 0.0005 (dichotomous data from Chapter 5 RQ 5.1.4)"
- Required pattern: "Delta ICC = [delta_ICC] (difference: confidence - accuracy)"
- Required pattern: "Ratio ICC = [ratio_ICC] (fold change: confidence / accuracy)"
- Required pattern: "Hypothesis supported: [hypothesis_supported]"
- Forbidden patterns: "ERROR", "NaN in comparison", "Invalid ICC"
- Acceptable warnings: None expected for comparison step

**Expected Behavior on Validation Failure:**
- If ICC_slope_accuracy != 0.0005: Raise ValueError with message "Chapter 5 comparison value incorrect - must use ICC_slope_accuracy = 0.0005 from RQ 5.1.4"
- If NaN values present: Raise ValueError with message "Comparison failed - NaN in ICC comparison"
- If hypothesis_supported not in valid set: Raise ValueError with message "Invalid hypothesis classification - must be Measurement Artifact, Universal Forgetting, or Inconclusive"
- Log failure to logs/step05_compare_icc_ch5.log
- Quit script immediately (do NOT proceed to results interpretation)
- g_debug invoked to diagnose root cause (likely Step 2 ICC computation error)

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 -> Step 1:** LMM model object (in memory) -> variance components CSV
- Model object contains fitted random effects covariance matrix
- Extract diagonal elements (variances) and off-diagonal element (covariance)
- Add residual variance from model.scale attribute
- Output 4-row CSV (var_intercept, var_slope, cov_int_slope, var_residual)

**Step 1 -> Step 2:** Variance components CSV -> ICC estimates CSV
- Read 4 variance components
- Apply Hoffman & Stawski (2009) formulas for 3 ICC types
- Output 3-row CSV (ICC_intercept, ICC_slope_simple, ICC_slope_conditional)

**Step 0 -> Step 3:** LMM model object (in memory) -> participant-level random effects CSV
- Model object contains participant-specific random effects dictionary
- Extract intercept and slope deviations for each UID
- Output 100-row CSV (one per participant)

**Step 3 -> Step 4:** Random effects CSV -> intercept-slope correlation CSV
- Compute Pearson correlation between random_intercept and random_slope columns
- Report dual p-values per Decision D068
- Output 1-row CSV (single correlation test)

**Step 2 -> Step 5:** ICC estimates CSV -> Chapter 5 comparison CSV
- Extract ICC_slope_simple from Step 2
- Compare with hard-coded ICC_slope_accuracy = 0.0005 from Chapter 5 RQ 5.1.4
- Compute difference and ratio
- Output 1-row CSV (single comparison)

### Column Naming Conventions

**Variance Components (Step 1):**
- component: {"var_intercept", "var_slope", "cov_int_slope", "var_residual"}
- value: Variance/covariance estimate (float)
- SE: Standard error of estimate (float or NA)

**ICC Estimates (Step 2):**
- icc_type: {"ICC_intercept", "ICC_slope_simple", "ICC_slope_conditional"}
- value: ICC estimate in [0, 1] (float)
- interpretation: {"negligible", "small", "moderate", "substantial"}

**Random Effects (Step 3):**
- UID: Participant identifier (string, format Pxxx)
- random_intercept: Intercept deviation from population mean (float)
- random_slope: Slope deviation from population mean slope (float)

**Intercept-Slope Correlation (Step 4):**
- correlation_r: Pearson r in [-1, 1] (float)
- CI_lower, CI_upper: 95% confidence interval bounds (float)
- N: Sample size (int)
- p_uncorrected, p_bonferroni: Dual p-values per Decision D068 (float)
- interpretation: Verbal description of correlation (string)

**Chapter 5 Comparison (Step 5):**
- ICC_slope_confidence: From this RQ (float)
- ICC_slope_accuracy: From Chapter 5 (hard-coded 0.0005, float)
- delta_ICC: Difference (float)
- ratio_ICC: Fold change (float)
- hypothesis_supported: {"Measurement Artifact", "Universal Forgetting", "Inconclusive"}
- interpretation: Verbal description of comparison findings (string)

### Data Type Constraints

**All CSV files:**
- Encoding: UTF-8
- Delimiter: Comma
- Index: False (no index column written)
- Header: True (column names in first row)

**Numeric precision:**
- Variance components: 6 decimal places (scientific notation if <0.0001)
- ICC estimates: 4 decimal places (proportion format)
- Correlation r: 3 decimal places
- p-values: Scientific notation if <0.001, otherwise 4 decimal places

**String constraints:**
- UID format: Pxxx with leading zeros (e.g., P001, P050, P100)
- Categorical values: Exact spelling from conventions above (case-sensitive)

---

## Cross-RQ Dependencies

**Dependency Type 2: DERIVED Data from Other RQs (Dependencies Exist)**

**This RQ requires outputs from:**

**RQ 6.1.1** (Functional Form Comparison)
- File: results/ch6/6.1.1/data/step06_best_model.pkl
- Used in: Step 0 (load fitted LMM model object)
- Rationale: RQ 6.1.1 establishes best-fitting functional form for confidence trajectories via AIC comparison. This RQ decomposes variance from that winning model to compute ICC estimates. Without RQ 6.1.1 model, there is no fitted random effects structure to decompose.

**RQ 5.1.4** (Chapter 5 ICC Decomposition with Accuracy Data)
- File: KNOWN VALUE (not file-based): ICC_slope_accuracy = 0.0005
- Used in: Step 5 (critical comparison of ordinal vs dichotomous data precision)
- Rationale: RQ 5.1.4 established that dichotomous accuracy data shows near-zero slope variance (ICC_slope = 0.0005). This RQ tests whether 5-level ordinal confidence data reveals detectable slope variance that binary measures missed. Comparison is central to theoretical question.

**Execution Order Constraint:**
1. RQ 6.1.1 must complete Steps 1-6 (functional form comparison, save best_model.pkl)
2. This RQ (6.1.4) executes Steps 0-5 (load model, extract variance, compute ICC, compare with Chapter 5)
3. RQ 6.1.5 (Clustering) depends on this RQ Step 3 output (random_effects.csv)

**Data Source Boundaries:**
- **RAW data:** None (this RQ does not extract from master.xlsx)
- **DERIVED data:** Fitted LMM model object from RQ 6.1.1
- **Scope:** This RQ does NOT refit models (uses existing fitted object for variance decomposition only)

**Validation:**
- Step 0: Check results/ch6/6.1.1/data/step06_best_model.pkl exists (circuit breaker: EXPECTATIONS ERROR if absent)
- If file missing -> quit with error "RQ 6.1.1 must complete Step 6 before this RQ can run"
- User must execute RQ 6.1.1 first (functional form comparison)

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

#### Step 0: Load Best-Fitting LMM

**Analysis Tool:** (determined by rq_tools - likely tools.config.load_model_from_file or custom LMM loader)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_model_convergence)

**What Validation Checks:**
- Model object loaded successfully (Python object type verification)
- Model converged (model.converged = True)
- Random effects structure includes both intercept and slope variance
- Metadata file created with convergence status documented

**Expected Behavior on Validation Failure:**
- Raise error if file missing: "RQ 6.1.1 incomplete - best_model.pkl not found"
- Raise error if model did not converge: "Loaded model shows convergence failure"
- Log failure to logs/step00_load_best_model.log
- Quit script immediately
- g_debug invoked to diagnose (likely RQ 6.1.1 incomplete or model specification error)

---

#### Step 1: Extract Variance Components

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.extract_random_effects_from_lmm or custom variance extractor)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_variance_positivity + validate_dataframe_structure)

**What Validation Checks:**
- Output file exists (data/step01_variance_components.csv)
- Expected 4 rows (var_intercept, var_slope, cov_int_slope, var_residual)
- Expected 3 columns (component, value, SE)
- Variance components positive (var_intercept > 0, var_residual > 0)
- Slope variance non-negative (var_slope >= 0, can be zero)
- Covariance within correlation bounds (|cov| <= sqrt(var_int * var_slope))

**Expected Behavior on Validation Failure:**
- Raise error if negative variance: "Negative variance detected - model estimation error"
- Raise error if invalid covariance: "Covariance exceeds correlation bounds"
- Log failure to logs/step01_extract_variance_components.log
- Quit script immediately
- g_debug invoked to diagnose (likely model convergence issue)

---

#### Step 2: Compute ICC Estimates

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.compute_icc_from_variance_components)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_icc_bounds + validate_dataframe_structure)

**What Validation Checks:**
- Output file exists (data/step02_icc_estimates.csv)
- Expected 3 rows (ICC_intercept, ICC_slope_simple, ICC_slope_conditional)
- Expected 3 columns (icc_type, value, interpretation)
- All ICC values in [0, 1] range (mathematical constraint)
- ICC_slope_conditional >= ICC_slope_simple (mathematical property)
- Interpretation consistent with value magnitude

**Expected Behavior on Validation Failure:**
- Raise error if ICC out of bounds: "ICC [value] exceeds valid range [0, 1]"
- Raise error if conditional < simple: "Conditional ICC cannot be smaller than simple ICC"
- Log failure to logs/step02_compute_icc_estimates.log
- Quit script immediately
- g_debug invoked to diagnose (likely variance extraction error or formula error)

---

#### Step 3: Extract Participant-Level Random Effects

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.extract_random_effects_from_lmm)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure + validate_numeric_range)

**What Validation Checks:**
- Output file exists (data/step03_random_effects.csv)
- Expected 100 rows (exactly N participants)
- Expected 3 columns (UID, random_intercept, random_slope)
- No NaN values (all participants successfully estimated)
- No duplicate UIDs (each participant appears once)
- UID format correct (Pxxx pattern)

**Expected Behavior on Validation Failure:**
- Raise error if N != 100: "Expected 100 participants, found [N]"
- Raise error if NaN values: "NaN random effects for participant [UID]"
- Raise error if duplicates: "Duplicate participant [UID] in random effects"
- Log failure to logs/step03_extract_random_effects.log
- Quit script immediately
- g_debug invoked to diagnose (likely model convergence issue for specific participants)

---

#### Step 4: Test Intercept-Slope Correlation

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.test_intercept_slope_correlation_d068)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_correlation_test_d068 + validate_numeric_range)

**What Validation Checks:**
- Output file exists (data/step04_intercept_slope_correlation.csv)
- Expected 1 row (single correlation test)
- Expected 7 columns (correlation_r, CI_lower, CI_upper, N, p_uncorrected, p_bonferroni, interpretation)
- Correlation r in [-1, 1] (mathematical constraint)
- CI_lower < r < CI_upper (valid confidence interval)
- Dual p-values present (Decision D068 compliance)
- N = 100 (sample size matches participant count)

**Expected Behavior on Validation Failure:**
- Raise error if r out of bounds: "Correlation [r] exceeds valid range [-1, 1]"
- Raise error if missing p-values: "Missing dual p-values - Decision D068 violation"
- Raise error if invalid CI: "CI_lower > CI_upper - invalid confidence interval"
- Log failure to logs/step04_test_intercept_slope_correlation.log
- Quit script immediately
- g_debug invoked to diagnose (likely statistical computation error)

---

#### Step 5: Compare ICC_slope with Chapter 5 Accuracy Data

**Analysis Tool:** (determined by rq_tools - likely custom comparison function)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure + validate_numeric_range)

**What Validation Checks:**
- Output file exists (data/step05_ch5_icc_comparison.csv)
- Expected 1 row (single comparison)
- Expected 6 columns (ICC_slope_confidence, ICC_slope_accuracy, delta_ICC, ratio_ICC, hypothesis_supported, interpretation)
- ICC_slope_accuracy = 0.0005 exactly (hard-coded value from Chapter 5)
- ICC_slope_confidence in [0, 1] (valid ICC range)
- hypothesis_supported in {"Measurement Artifact", "Universal Forgetting", "Inconclusive"}
- Interpretation consistent with hypothesis classification

**Expected Behavior on Validation Failure:**
- Raise error if ICC_slope_accuracy != 0.0005: "Chapter 5 comparison value incorrect"
- Raise error if invalid hypothesis: "Invalid hypothesis classification"
- Log failure to logs/step05_compare_icc_ch5.log
- Quit script immediately
- g_debug invoked to diagnose (likely Step 2 ICC computation error)

---

## Summary

**Total Steps:** 6 (Step 0: Load model, Steps 1-5: Variance decomposition and comparison)
**Estimated Runtime:** 10-15 minutes (no model fitting, only variance extraction and computation)
**Cross-RQ Dependencies:** RQ 6.1.1 (provides best_model.pkl), Chapter 5 RQ 5.1.4 (provides ICC_slope_accuracy = 0.0005 for comparison)
**Primary Outputs:**
- data/step01_variance_components.csv (4 variance components from LMM)
- data/step02_icc_estimates.csv (3 ICC estimates following Hoffman & Stawski 2009)
- data/step03_random_effects.csv (100 participant-level intercepts + slopes, REQUIRED for RQ 6.1.5)
- data/step04_intercept_slope_correlation.csv (baseline-decline relationship with dual p-values)
- data/step05_ch5_icc_comparison.csv (CRITICAL comparison testing measurement artifact vs universal forgetting hypothesis)
**Validation Coverage:** 100% (all 6 steps have validation requirements with 4-layer substance criteria)

**Key Theoretical Contribution:**
This RQ tests whether 5-level ordinal confidence data reveals slope variance (individual differences in forgetting rate) that dichotomous accuracy data could not detect. If ICC_slope_confidence > 0.10 while ICC_slope_accuracy = 0.0005, it demonstrates that measurement precision affects our ability to detect trait variance in forgetting dynamics. If both near zero, it confirms universal forgetting pattern regardless of precision.

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent for RQ 6.1.4 (ICC Decomposition)
