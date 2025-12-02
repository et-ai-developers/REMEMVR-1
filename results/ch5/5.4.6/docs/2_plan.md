# Analysis Plan: RQ 5.4.6 - Schema-Specific Variance Decomposition

**Research Question:** 5.4.6
**Created:** 2025-12-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines **variance decomposition of episodic memory forgetting trajectories** across three schema congruence levels (Common, Congruent, Incongruent). The analysis uses **DERIVED data** from RQ 5.4.1 (IRT theta scores + LMM model) for N=100 participants across 4 test sessions, producing 1200 total observations.

**Research Question:**
What proportion of variance in forgetting rate is between-person vs within-person for each congruence level?

**Analysis Approach:**
Stratified Linear Mixed Models (LMM) with random slopes, fitted separately for each congruence level. Compute Intraclass Correlation Coefficients (ICC) for intercepts and slopes to quantify trait-like stability of forgetting rate. Test intercept-slope correlations within each congruence level. Compare ICC estimates across congruence levels to assess differential stability of schema-based memory.

**Pipeline:** LMM-only (NO IRT - uses theta from RQ 5.4.1)

**Steps:** 6 analysis steps (no Step 0 extraction - data pre-exists in RQ 5.4.1)

**Estimated Runtime:** Medium (~15-30 minutes total)
- Step 1: Low (5 min - dependency loading + validation)
- Step 2: Medium (10-15 min - 3 LMM fits with random slopes)
- Step 3: Low (2 min - ICC computation)
- Step 4: Low (2 min - random effects extraction)
- Step 5: Medium (5 min - correlation tests + diagnostic plots)
- Step 6: Low (2 min - comparison table + bar plot)

**Key Decisions Applied:**
- **Decision D070:** TSVR as time variable (inherited from RQ 5.4.1 LMM input)
- **Decision D068:** Dual p-value reporting for intercept-slope correlation tests (p_uncorrected + p_bonferroni)
- **NO Decision D039:** No IRT calibration in this RQ (theta scores from RQ 5.4.1)
- **NO Decision D069:** No trajectory plots (diagnostic plots only - histograms + Q-Q plots)

---

## Analysis Plan

This RQ requires 6 steps:

### Step 1: Load Dependency Data from RQ 5.4.1

**Dependencies:** None (first step - but REQUIRES RQ 5.4.1 completion)

**Complexity:** Low (~5 minutes - data loading + validation)

**Purpose:** Load theta scores, TSVR mapping, and LMM model from RQ 5.4.1. Verify data structure and convergence status before proceeding to congruence-stratified analysis.

**Input:**

**File 1:** results/ch5/5.4.1/data/step03_theta_scores.csv
**Source:** RQ 5.4.1 Step 3 (IRT Pass 2 calibration on purified items)
**Format:** CSV with columns:
  - `composite_ID` (string, format: {UID}_{test}, e.g., "P001_T1")
  - `theta_common` (float, IRT ability estimate for Common items)
  - `theta_congruent` (float, IRT ability estimate for Congruent items)
  - `theta_incongruent` (float, IRT ability estimate for Incongruent items)
  - `se_common` (float, standard error for Common theta)
  - `se_congruent` (float, standard error for Congruent theta)
  - `se_incongruent` (float, standard error for Incongruent theta)
**Expected Rows:** 400 (100 participants x 4 tests)
**Note:** Wide format - one row per composite_ID, separate theta columns per congruence level

**File 2:** results/ch5/5.4.1/data/step04_lmm_input.csv
**Source:** RQ 5.4.1 Step 4 (theta merged with TSVR, reshaped to long format)
**Format:** CSV, long format with columns:
  - `UID` (string, participant identifier, e.g., "P001")
  - `test` (string, test session identifier: T1/T2/T3/T4)
  - `TSVR_hours` (float, actual hours since encoding per Decision D070)
  - `congruence` (string, categorical: "Common" / "Congruent" / "Incongruent")
  - `theta` (float, IRT ability estimate for given congruence level)
  - `SE` (float, standard error of theta)
**Expected Rows:** 1200 (100 participants x 4 tests x 3 congruence levels)
**Note:** This is the primary input for stratified LMM analysis

**File 3:** results/ch5/5.4.1/data/step05_lmm_fitted_model.pkl
**Source:** RQ 5.4.1 Step 5 (best-fitting LMM with Congruence x Time interaction)
**Format:** Pickled statsmodels MixedLM object
**Purpose:** Reference for model convergence status and variance component structure (NOT re-fitted in this RQ)

**File 4:** results/ch5/5.4.1/status.yaml
**Source:** RQ 5.4.1 workflow status
**Purpose:** Verify RQ 5.4.1 completion (rq_results.status = success)

**Processing:**

1. **Check RQ 5.4.1 Completion:**
   - Read results/ch5/5.4.1/status.yaml
   - Parse rq_results.status field
   - If rq_results.status != "success" -> Circuit breaker: EXPECTATIONS ERROR ("RQ 5.4.1 must complete before RQ 5.4.6")

2. **Load Theta Scores:**
   - Read step03_theta_scores.csv
   - Verify 400 rows (100 UID x 4 tests)
   - Verify 7 columns (composite_ID + 3 theta + 3 SE)
   - Check for NaN values (theta/SE should be non-null for all observations)

3. **Load LMM Input:**
   - Read step04_lmm_input.csv
   - Verify 1200 rows (100 UID x 4 tests x 3 congruence)
   - Verify required columns: UID, test, TSVR_hours, congruence, theta, SE
   - Check TSVR_hours range: [0, 168] hours (0=encoding, 168=1 week)
   - Verify congruence levels: exactly 3 unique values (Common, Congruent, Incongruent)

4. **Load Reference Model:**
   - Load step05_lmm_fitted_model.pkl
   - Check model.converged = True (if False -> warning, proceed cautiously)
   - Extract model formula for reference (should be: theta ~ Congruence * TSVR_hours + ...)

**Output:**

**File 1:** data/step01_dependency_validation_report.txt
**Format:** Text report
**Content:**
  - RQ 5.4.1 completion status
  - Theta scores data summary (rows, columns, NaN counts)
  - LMM input data summary (rows, congruence levels, TSVR range)
  - Reference model convergence status
  - Timestamp and validation status (PASS/FAIL)

**File 2:** data/step01_loaded_lmm_input.csv
**Format:** CSV (copy of RQ 5.4.1 step04 output for local workflow)
**Columns:** UID, test, TSVR_hours, congruence, theta, SE
**Expected Rows:** 1200
**Note:** Cached copy to avoid repeated cross-RQ reads in subsequent steps

**Validation Requirement:**

Validation tools MUST be used after data loading. Specific validation tools will be determined by rq_tools based on data format requirements and cross-RQ dependency checks.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_dependency_validation_report.txt exists (text file, >500 bytes)
- data/step01_loaded_lmm_input.csv exists (CSV, 1200 rows x 6 columns)

*Value Ranges:*
- theta in [-3, 3] (typical IRT ability range)
- SE in [0.1, 1.0] (above 1.0 = unreliable estimates)
- TSVR_hours in [0, 168] (0=encoding, 168=1 week max)
- congruence in {Common, Congruent, Incongruent} (exactly 3 categorical levels)

*Data Quality:*
- All 1200 rows present (100 UID x 4 tests x 3 congruence - no missing observations)
- No NaN in theta or TSVR_hours columns (SE can be missing if theta failed to estimate)
- Exactly 3 unique congruence levels (no typos like "Congruent " with trailing space)
- Each UID has exactly 12 rows (4 tests x 3 congruence)

*Log Validation:*
- Required pattern: "RQ 5.4.1 status: rq_results = success"
- Required pattern: "Loaded 1200 observations from step04_lmm_input.csv"
- Required pattern: "Congruence levels: 3 (Common, Congruent, Incongruent)"
- Forbidden patterns: "ERROR", "RQ 5.4.1 incomplete", "NaN detected in theta"
- Acceptable warnings: None expected for dependency loading

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "RQ 5.4.1 status != success, found: pending")
- Log failure to logs/step01_load_dependency_data.log
- Quit script immediately (do NOT proceed to Step 2)
- Circuit breaker triggers: EXPECTATIONS ERROR if RQ 5.4.1 incomplete

---

### Step 2: Fit Congruence-Stratified LMMs

**Dependencies:** Step 1 (requires loaded LMM input)

**Complexity:** Medium (~10-15 minutes - 3 LMM fits with random slopes)

**Purpose:** Fit three separate LMMs, one per congruence level (Common, Congruent, Incongruent), to estimate variance components for between-person and within-person variance in intercepts and slopes.

**Input:**

**File 1:** data/step01_loaded_lmm_input.csv
**Source:** Step 1 output (cached LMM input from RQ 5.4.1)
**Format:** CSV, long format
**Columns:** UID, test, TSVR_hours, congruence, theta, SE
**Expected Rows:** 1200

**Processing:**

1. **Stratify by Congruence:**
   - Split data into 3 subsets:
     - df_common = rows where congruence == "Common" (400 rows: 100 UID x 4 tests)
     - df_congruent = rows where congruence == "Congruent" (400 rows)
     - df_incongruent = rows where congruence == "Incongruent" (400 rows)

2. **Fit LMM for Common:**
   - Formula: `theta ~ TSVR_hours + (TSVR_hours | UID)`
   - Method: REML=True (unbiased variance estimates per best practices)
   - Random effects: Random intercept + random slope (unstructured covariance)
   - Convergence: Check model.converged = True

3. **Fit LMM for Congruent:**
   - Formula: `theta ~ TSVR_hours + (TSVR_hours | UID)`
   - Method: REML=True
   - Random effects: Random intercept + random slope

4. **Fit LMM for Incongruent:**
   - Formula: `theta ~ TSVR_hours + (TSVR_hours | UID)`
   - Method: REML=True
   - Random effects: Random intercept + random slope

5. **Extract Variance Components per Congruence:**
   - var_intercept: Random intercept variance (between-person variance at Time=0)
   - var_slope: Random slope variance (between-person variance in forgetting rate)
   - cov_int_slope: Covariance between intercept and slope
   - var_residual: Residual variance (within-person variance)

6. **Convergence Contingency (per 1_concept.md):**
   - If any model fails to converge with random slopes:
     a. Try alternative optimizers (bobyqa, nlminb)
     b. Likelihood Ratio Test (LRT): Compare random slopes vs intercept-only
     c. If LRT p < 0.05: Retain slopes with simplified correlation structure (diagonal)
     d. If LRT p >= 0.05: Use random intercepts-only model
   - **Critical:** If random slopes cannot be estimated, ICC_slope cannot be computed -> Report limitation explicitly in output

**Output:**

**File 1:** data/step02_model_metadata_common.yaml
**Format:** YAML
**Content:**
  - model_formula: "theta ~ TSVR_hours + (TSVR_hours | UID)"
  - converged: True/False
  - reml: True
  - n_observations: 400
  - n_participants: 100
  - timestamp: YYYY-MM-DD HH:MM:SS

**File 2:** data/step02_model_metadata_congruent.yaml
**Format:** YAML (same structure as File 1)

**File 3:** data/step02_model_metadata_incongruent.yaml
**Format:** YAML (same structure as File 1)

**File 4:** data/step02_variance_components.csv
**Format:** CSV
**Columns:**
  - `congruence` (string: Common/Congruent/Incongruent)
  - `component` (string: var_intercept / var_slope / cov_int_slope / var_residual / var_total)
  - `value` (float: variance estimate)
**Expected Rows:** 15 (5 variance components x 3 congruence levels)
**Note:** var_total = var_intercept + var_slope + var_residual (for reference)

**File 5:** data/step02_fitted_model_common.pkl
**Format:** Pickled statsmodels MixedLM object (Common congruence model)

**File 6:** data/step02_fitted_model_congruent.pkl
**Format:** Pickled statsmodels MixedLM object (Congruent congruence model)

**File 7:** data/step02_fitted_model_incongruent.pkl
**Format:** Pickled statsmodels MixedLM object (Incongruent congruence model)

**Validation Requirement:**

Validation tools MUST be used after LMM fitting. Specific validation tools determined by rq_tools based on LMM convergence and variance component validation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_model_metadata_common.yaml exists (YAML, >200 bytes)
- data/step02_model_metadata_congruent.yaml exists (YAML, >200 bytes)
- data/step02_model_metadata_incongruent.yaml exists (YAML, >200 bytes)
- data/step02_variance_components.csv exists (CSV, 15 rows x 3 columns)
- data/step02_fitted_model_common.pkl exists (pickle file, >5KB)
- data/step02_fitted_model_congruent.pkl exists (pickle file, >5KB)
- data/step02_fitted_model_incongruent.pkl exists (pickle file, >5KB)

*Value Ranges:*
- var_intercept > 0 (negative variance impossible)
- var_slope > 0 (negative variance impossible)
- var_residual > 0 (negative variance impossible)
- cov_int_slope unrestricted (can be negative, zero, or positive)
- All variance components < 10.0 (values >10 suggest estimation problem for theta scale)

*Data Quality:*
- Exactly 15 rows in variance_components.csv (5 components x 3 congruence)
- No NaN values in variance estimates (model must converge successfully)
- All 3 congruence levels present (Common, Congruent, Incongruent)
- converged = True in all 3 YAML metadata files

*Log Validation:*
- Required pattern: "Model converged: True" (3 times, once per congruence)
- Required pattern: "Extracted variance components for Common: 5 components"
- Required pattern: "Extracted variance components for Congruent: 5 components"
- Required pattern: "Extracted variance components for Incongruent: 5 components"
- Forbidden patterns: "ERROR", "Convergence failed", "NaN variance"
- Acceptable warnings: "Covariance matrix not positive definite" (acceptable if LRT fallback applied per contingency plan)

**Expected Behavior on Validation Failure:**
- If convergence fails for ANY congruence: Apply contingency plan (alternative optimizer -> LRT -> simplified structure)
- If ALL contingencies fail: Raise error, log to logs/step02_fit_stratified_lmms.log
- Quit script if variance components cannot be estimated
- g_debug invoked to diagnose (common causes: insufficient data, model misspecification)

---

### Step 3: Compute ICC Estimates

**Dependencies:** Step 2 (requires variance components)

**Complexity:** Low (~2 minutes - ICC computation from variance components)

**Purpose:** Compute three types of Intraclass Correlation Coefficients (ICC) for each congruence level to quantify between-person vs within-person variance in intercepts and slopes.

**Input:**

**File 1:** data/step02_variance_components.csv
**Source:** Step 2 output
**Format:** CSV
**Columns:** congruence, component, value
**Expected Rows:** 15 (5 variance components x 3 congruence levels)

**Processing:**

1. **ICC Formulas (per congruence level):**

   **ICC_intercept:**
   - Formula: var_intercept / (var_intercept + var_residual)
   - Interpretation: Proportion of variance in baseline ability (Time=0) that is between-person

   **ICC_slope_simple:**
   - Formula: var_slope / (var_slope + var_residual)
   - Interpretation: Proportion of variance in forgetting rate (slope) that is between-person (ignoring intercept-slope covariance)

   **ICC_slope_conditional:**
   - Formula: var_slope / (var_slope + var_residual + 2 * t * cov_int_slope + t^2 * var_intercept)
   - Where: t = Day 6 timepoint (144 hours for TSVR_hours scale)
   - Interpretation: Proportion of variance in ability at Day 6 that is between-person, accounting for intercept-slope covariance

2. **Compute ICCs for Each Congruence:**
   - Common: 3 ICCs (intercept, slope_simple, slope_conditional)
   - Congruent: 3 ICCs
   - Incongruent: 3 ICCs
   - Total: 9 ICC estimates

3. **Classify ICC Magnitude:**
   - ICC < 0.20: "Low" (mostly within-person variance)
   - 0.20 <= ICC < 0.40: "Moderate" (mixed)
   - ICC >= 0.40: "Substantial" (trait-like stability, between-person variance dominant)

4. **Create Interpretive Summary:**
   - For each congruence level:
     - Report all 3 ICC values
     - Classify magnitude per thresholds above
     - Interpret theoretical meaning (e.g., "Common items show substantial between-person variance in slopes (ICC=0.52), indicating forgetting rate is a stable individual difference")

**Output:**

**File 1:** data/step03_icc_estimates.csv
**Format:** CSV
**Columns:**
  - `congruence` (string: Common/Congruent/Incongruent)
  - `icc_type` (string: intercept / slope_simple / slope_conditional)
  - `value` (float: ICC estimate, range [0, 1])
  - `magnitude` (string: Low / Moderate / Substantial)
**Expected Rows:** 9 (3 ICC types x 3 congruence levels)

**File 2:** data/step03_icc_summary.txt
**Format:** Text report
**Content:**
  - Header: "ICC Summary by Congruence Level"
  - For each congruence:
    - ICC_intercept: value, magnitude, interpretation
    - ICC_slope_simple: value, magnitude, interpretation
    - ICC_slope_conditional: value, magnitude, interpretation
  - Footer: Timestamp and validation status

**Validation Requirement:**

Validation tools MUST be used after ICC computation. Specific validation tools determined by rq_tools based on ICC range validation (must be in [0, 1]).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_icc_estimates.csv exists (CSV, 9 rows x 4 columns)
- data/step03_icc_summary.txt exists (text file, >1000 bytes)

*Value Ranges:*
- All ICC values in [0, 1] (values outside this range indicate computation error)
- ICC_slope_conditional typically lower than ICC_slope_simple (accounting for covariance reduces ICC at later timepoint)
- No NaN values (variance components must be non-zero)

*Data Quality:*
- Exactly 9 rows in icc_estimates.csv (3 ICC types x 3 congruence)
- All 3 congruence levels present (Common, Congruent, Incongruent)
- All 3 ICC types present per congruence (intercept, slope_simple, slope_conditional)
- magnitude column contains only: "Low" / "Moderate" / "Substantial" (case-sensitive)

*Log Validation:*
- Required pattern: "Computed 9 ICC estimates (3 types x 3 congruence levels)"
- Required pattern: "All ICC values in valid range [0, 1]"
- Forbidden patterns: "ERROR", "ICC out of bounds", "NaN ICC"
- Acceptable warnings: None expected for ICC computation

**Expected Behavior on Validation Failure:**
- If ICC value < 0 or > 1: Raise error (indicates variance component estimation error)
- Log failure to logs/step03_compute_icc.log
- Quit script immediately
- g_debug invoked to diagnose (check variance component signs)

---

### Step 4: Extract Random Effects

**Dependencies:** Step 2 (requires fitted LMM models)

**Complexity:** Low (~2 minutes - random effects extraction)

**Purpose:** Extract individual-level random intercepts and slopes for all 100 participants, separately for each congruence level, to enable intercept-slope correlation testing and distribution visualization.

**Input:**

**File 1:** data/step02_fitted_model_common.pkl
**Source:** Step 2 output
**Format:** Pickled statsmodels MixedLM object

**File 2:** data/step02_fitted_model_congruent.pkl
**Source:** Step 2 output

**File 3:** data/step02_fitted_model_incongruent.pkl
**Source:** Step 2 output

**Processing:**

1. **Extract Random Effects from Each Model:**
   - Load fitted model (Common/Congruent/Incongruent)
   - Extract random effects: model.random_effects
   - For each UID:
     - Total_Intercept = random intercept (deviation from fixed intercept)
     - Total_Slope = random slope (deviation from fixed slope)

2. **Combine Across Congruence Levels:**
   - Create single DataFrame with 300 rows (100 UID x 3 congruence)
   - Columns: UID, congruence, Total_Intercept, Total_Slope

3. **Compute Descriptive Statistics per Congruence:**
   - Mean, SD, Min, Max, Median for Total_Intercept and Total_Slope
   - Separately for Common, Congruent, Incongruent
   - Output to text report

**Output:**

**File 1:** data/step04_random_effects.csv
**Format:** CSV
**Columns:**
  - `UID` (string: participant identifier, e.g., "P001")
  - `congruence` (string: Common/Congruent/Incongruent)
  - `Total_Intercept` (float: random intercept deviation)
  - `Total_Slope` (float: random slope deviation)
**Expected Rows:** 300 (100 UID x 3 congruence levels)
**Note:** Each UID appears 3 times (once per congruence level)

**File 2:** data/step04_random_slopes_descriptives.txt
**Format:** Text report
**Content:**
  - Header: "Random Slopes Descriptive Statistics by Congruence Level"
  - For each congruence:
    - Total_Intercept: Mean, SD, Min, Max, Median
    - Total_Slope: Mean, SD, Min, Max, Median
  - Footer: Timestamp

**Validation Requirement:**

Validation tools MUST be used after random effects extraction. Specific validation tools determined by rq_tools based on random effects distribution validation (outlier detection, normality checks).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_random_effects.csv exists (CSV, 300 rows x 4 columns)
- data/step04_random_slopes_descriptives.txt exists (text file, >500 bytes)

*Value Ranges:*
- Total_Intercept in [-3, 3] (outside indicates extreme outliers)
- Total_Slope unrestricted (can be strongly negative for rapid forgetting or positive for practice effects)
- Mean of Total_Intercept ~ 0 (random effects should center at 0)
- Mean of Total_Slope ~ 0 (random effects should center at 0)

*Data Quality:*
- Exactly 300 rows (100 UID x 3 congruence)
- No NaN values in Total_Intercept or Total_Slope (model must estimate for all participants)
- Each UID appears exactly 3 times (once per congruence level)
- All 3 congruence levels present (Common, Congruent, Incongruent)

*Log Validation:*
- Required pattern: "Extracted random effects for 100 participants"
- Required pattern: "Total observations: 300 (100 UID x 3 congruence)"
- Forbidden patterns: "ERROR", "NaN random effects", "Missing UID"
- Acceptable warnings: "Extreme random slope detected" (acceptable if >3 SD from mean, documented in descriptives)

**Expected Behavior on Validation Failure:**
- If NaN random effects detected: Raise error (indicates model failed to estimate for some participants)
- If UID count != 100: Raise error (missing participants)
- Log failure to logs/step04_extract_random_effects.log
- Quit script immediately
- g_debug invoked to diagnose (check model convergence, data completeness)

---

### Step 5: Test Intercept-Slope Correlation and Create Diagnostic Plots

**Dependencies:** Step 4 (requires random effects)

**Complexity:** Medium (~5 minutes - 3 correlation tests + 6 diagnostic plots)

**Purpose:** Test the correlation between random intercepts and random slopes within each congruence level using Pearson correlation. Apply Bonferroni correction for multiple comparisons per Decision D068 (dual p-values). Create diagnostic plots (histograms + Q-Q plots) to assess random slope distribution normality.

**Input:**

**File 1:** data/step04_random_effects.csv
**Source:** Step 4 output
**Format:** CSV
**Columns:** UID, congruence, Total_Intercept, Total_Slope
**Expected Rows:** 300 (100 UID x 3 congruence)

**Processing:**

1. **Stratify by Congruence:**
   - Split data into 3 subsets:
     - df_common (100 rows)
     - df_congruent (100 rows)
     - df_incongruent (100 rows)

2. **Pearson Correlation per Congruence (Decision D068):**
   - Common: Correlate Total_Intercept with Total_Slope
     - Compute r, p_uncorrected
     - Apply Bonferroni correction: p_bonferroni = p_uncorrected * 3 (3 tests)
     - Cap at 1.0 if p_bonferroni > 1.0
   - Congruent: Same procedure
   - Incongruent: Same procedure

3. **Bonferroni Alpha Threshold:**
   - Familywise alpha = 0.05
   - Per-test alpha = 0.05 / 3 = 0.0167
   - Report BOTH p_uncorrected and p_bonferroni per Decision D068

4. **Interpretation:**
   - If p_bonferroni < 0.0167: Significant negative correlation (high baseline -> maintained advantage)
   - If p_bonferroni >= 0.0167: Non-significant (no reliable relationship)
   - Expected pattern: Negative correlations (high intercept -> less negative slope = maintained advantage)

5. **Create Diagnostic Plots:**

   **Histograms (3 plots, 1 per congruence):**
   - x-axis: Total_Slope
   - y-axis: Frequency
   - Overlay: Normal distribution curve (mean, SD from data)
   - Title: "Random Slopes Distribution - {Congruence}"
   - Output: data/step05_random_slopes_histogram_common.png (etc.)

   **Q-Q Plots (3 plots, 1 per congruence):**
   - x-axis: Theoretical quantiles (normal distribution)
   - y-axis: Sample quantiles (Total_Slope)
   - Overlay: 45-degree reference line
   - Title: "Q-Q Plot: Random Slopes - {Congruence}"
   - Output: data/step05_random_slopes_qqplot_common.png (etc.)

**Output:**

**File 1:** data/step05_intercept_slope_correlation.csv
**Format:** CSV
**Columns:**
  - `congruence` (string: Common/Congruent/Incongruent)
  - `statistic` (string: r / p_uncorrected / p_bonferroni / CI_lower / CI_upper)
  - `value` (float: correlation coefficient or p-value)
**Expected Rows:** 15 (5 statistics x 3 congruence levels)
**Note:** CI = 95% confidence interval for correlation coefficient

**File 2:** data/step05_correlation_interpretation.txt
**Format:** Text report
**Content:**
  - Header: "Intercept-Slope Correlation by Congruence Level (Decision D068 Dual P-Values)"
  - For each congruence:
    - Pearson r, 95% CI
    - p_uncorrected, p_bonferroni
    - Significance at Bonferroni alpha = 0.0167
    - Interpretation (negative correlation expected)
  - Footer: Timestamp

**File 3:** data/step05_random_slopes_histogram_common.png
**Format:** PNG (800 x 600 @ 300 DPI)
**Note:** Histogram saved to data/ folder per v4.1 folder structure (analysis step output)

**File 4:** data/step05_random_slopes_histogram_congruent.png
**Format:** PNG (800 x 600 @ 300 DPI)

**File 5:** data/step05_random_slopes_histogram_incongruent.png
**Format:** PNG (800 x 600 @ 300 DPI)

**File 6:** data/step05_random_slopes_qqplot_common.png
**Format:** PNG (800 x 600 @ 300 DPI)

**File 7:** data/step05_random_slopes_qqplot_congruent.png
**Format:** PNG (800 x 600 @ 300 DPI)

**File 8:** data/step05_random_slopes_qqplot_incongruent.png
**Format:** PNG (800 x 600 @ 300 DPI)

**Validation Requirement:**

Validation tools MUST be used after correlation testing and plot creation. Specific validation tools determined by rq_tools based on dual p-value validation (Decision D068) and plot data completeness.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_intercept_slope_correlation.csv exists (CSV, 15 rows x 3 columns)
- data/step05_correlation_interpretation.txt exists (text file, >800 bytes)
- data/step05_random_slopes_histogram_common.png exists (PNG, >10KB)
- data/step05_random_slopes_histogram_congruent.png exists (PNG, >10KB)
- data/step05_random_slopes_histogram_incongruent.png exists (PNG, >10KB)
- data/step05_random_slopes_qqplot_common.png exists (PNG, >10KB)
- data/step05_random_slopes_qqplot_congruent.png exists (PNG, >10KB)
- data/step05_random_slopes_qqplot_incongruent.png exists (PNG, >10KB)

*Value Ranges:*
- r in [-1, 1] (correlation coefficient bounds)
- p_uncorrected in [0, 1] (p-value bounds)
- p_bonferroni in [0, 1] (capped at 1.0 after correction)
- CI_lower in [-1, 1], CI_upper in [-1, 1]
- Expected: r < 0 (negative correlations per hypothesis)

*Data Quality:*
- Exactly 15 rows in correlation.csv (5 statistics x 3 congruence)
- All 3 congruence levels present (Common, Congruent, Incongruent)
- All 5 statistics present per congruence (r, p_uncorrected, p_bonferroni, CI_lower, CI_upper)
- All 6 PNG files > 10KB (non-empty plots)
- No NaN values in correlation coefficients or p-values

*Log Validation:*
- Required pattern: "Computed 3 Pearson correlations (1 per congruence level)"
- Required pattern: "Applied Bonferroni correction: multiplier = 3"
- Required pattern: "Decision D068: Dual p-values reported (uncorrected + bonferroni)"
- Required pattern: "Created 6 diagnostic plots (3 histograms + 3 Q-Q plots)"
- Forbidden patterns: "ERROR", "NaN correlation", "Missing congruence level"
- Acceptable warnings: "Non-normal distribution detected in Q-Q plot" (acceptable, documented)

**Expected Behavior on Validation Failure:**
- If correlation computation fails: Raise error (e.g., "Insufficient variance in Total_Slope")
- If plot creation fails: Raise error (e.g., "Empty data for histogram")
- Log failure to logs/step05_test_correlations_plot_diagnostics.log
- Quit script immediately
- g_debug invoked to diagnose (check data completeness, plotting library issues)

---

### Step 6: Compare ICC Across Congruence Levels

**Dependencies:** Step 3 (requires ICC estimates)

**Complexity:** Low (~2 minutes - comparison table + bar plot)

**Purpose:** Compare ICC estimates across the three congruence levels (Common, Congruent, Incongruent) to assess differential stability of schema-based memory. Rank congruence levels by ICC_slope magnitude. Create bar plot for visualization.

**Input:**

**File 1:** data/step03_icc_estimates.csv
**Source:** Step 3 output
**Format:** CSV
**Columns:** congruence, icc_type, value, magnitude
**Expected Rows:** 9 (3 ICC types x 3 congruence levels)

**Processing:**

1. **Pivot ICC Estimates:**
   - Reshape data to wide format:
     - Rows: congruence (Common, Congruent, Incongruent)
     - Columns: icc_intercept, icc_slope_simple, icc_slope_conditional
   - 3 rows x 3 columns = 9 ICC values

2. **Rank by ICC_slope_simple:**
   - Sort congruence levels by icc_slope_simple descending
   - Expected hypothesis: Congruent > Common > Incongruent
   - Document ranking in comparison table

3. **Descriptive Comparison:**
   - For each congruence level:
     - Report all 3 ICC values
     - Compare magnitude classifications (Low/Moderate/Substantial)
     - Interpret pattern relative to hypothesis
   - NO formal significance test (ICCs are point estimates from separate models)
   - Report as descriptive comparison only

4. **Create Bar Plot:**
   - x-axis: Congruence level (Common, Congruent, Incongruent)
   - y-axis: ICC value (0 to 1 scale)
   - 3 grouped bars per congruence: intercept, slope_simple, slope_conditional
   - Horizontal reference lines at 0.20 (Moderate threshold) and 0.40 (Substantial threshold)
   - Title: "ICC Estimates by Congruence Level"
   - Legend: ICC_intercept, ICC_slope_simple, ICC_slope_conditional
   - Output: data/step06_congruence_icc_barplot.png

**Output:**

**File 1:** data/step06_congruence_icc_comparison.csv
**Format:** CSV
**Columns:**
  - `congruence` (string: Common/Congruent/Incongruent)
  - `icc_intercept` (float: ICC for intercepts)
  - `icc_slope_simple` (float: ICC for slopes, simple formula)
  - `icc_slope_conditional` (float: ICC for slopes at Day 6, conditional on intercept)
  - `rank_by_slope` (int: 1=highest ICC_slope_simple, 3=lowest)
**Expected Rows:** 3 (1 per congruence level)

**File 2:** data/step06_icc_comparison_interpretation.txt
**Format:** Text report
**Content:**
  - Header: "ICC Comparison Across Congruence Levels"
  - Ranking table (by ICC_slope_simple descending)
  - For each congruence:
    - All 3 ICC values
    - Magnitude classifications
    - Interpretation relative to hypothesis
  - Summary: Does ranking match hypothesis (Congruent > Common > Incongruent)?
  - Note: Descriptive comparison only (no formal significance test)
  - Footer: Timestamp

**File 3:** data/step06_congruence_icc_barplot.png
**Format:** PNG (800 x 600 @ 300 DPI)
**Note:** Bar plot saved to data/ folder per v4.1 folder structure (analysis step output)

**Validation Requirement:**

Validation tools MUST be used after ICC comparison and plot creation. Specific validation tools determined by rq_tools based on comparison table completeness and plot data validation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_congruence_icc_comparison.csv exists (CSV, 3 rows x 5 columns)
- data/step06_icc_comparison_interpretation.txt exists (text file, >600 bytes)
- data/step06_congruence_icc_barplot.png exists (PNG, >10KB)

*Value Ranges:*
- All ICC values in [0, 1] (inherited from Step 3 validation)
- rank_by_slope in {1, 2, 3} (consecutive integers, no duplicates)

*Data Quality:*
- Exactly 3 rows in comparison.csv (1 per congruence level)
- All 3 congruence levels present (Common, Congruent, Incongruent)
- All 3 ICC types populated per congruence (no NaN values)
- rank_by_slope: exactly one rank=1, one rank=2, one rank=3 (no ties)
- PNG file > 10KB (non-empty plot)

*Log Validation:*
- Required pattern: "Ranked congruence levels by ICC_slope_simple"
- Required pattern: "Created ICC comparison table: 3 rows"
- Required pattern: "Created bar plot: 3 congruence levels x 3 ICC types"
- Forbidden patterns: "ERROR", "Missing congruence level", "NaN ICC"
- Acceptable warnings: None expected for comparison step

**Expected Behavior on Validation Failure:**
- If missing congruence level: Raise error (e.g., "Expected 3 congruence levels, found 2")
- If plot creation fails: Raise error (e.g., "Empty data for bar plot")
- Log failure to logs/step06_compare_icc_across_congruence.log
- Quit script immediately
- g_debug invoked to diagnose (check data completeness)

---

## Expected Data Formats

### Cross-RQ Data (from RQ 5.4.1)

**step03_theta_scores.csv (RQ 5.4.1):**
- Format: CSV, wide format (one row per composite_ID)
- Columns: composite_ID, theta_common, theta_congruent, theta_incongruent, se_common, se_congruent, se_incongruent
- Rows: 400 (100 participants x 4 tests)
- Data Types: composite_ID (string), all theta/se (float)

**step04_lmm_input.csv (RQ 5.4.1):**
- Format: CSV, long format (one row per UID x test x congruence)
- Columns: UID, test, TSVR_hours, congruence, theta, SE
- Rows: 1200 (100 UID x 4 tests x 3 congruence)
- Data Types: UID (string), test (string), TSVR_hours (float), congruence (string), theta (float), SE (float)

**step05_lmm_fitted_model.pkl (RQ 5.4.1):**
- Format: Pickled statsmodels MixedLM object
- Purpose: Reference model with Congruence x Time interaction (NOT re-fitted in this RQ)

### Step-to-Step Transformations

**Step 1 -> Step 2:**
- Input: step01_loaded_lmm_input.csv (long format, 1200 rows)
- Transformation: Stratify by congruence level
- Output: 3 subsets (400 rows each: Common, Congruent, Incongruent)
- Processing: Split data where congruence == {level}

**Step 2 -> Step 3:**
- Input: step02_variance_components.csv (15 rows: 5 components x 3 congruence)
- Transformation: Apply ICC formulas
- Output: step03_icc_estimates.csv (9 rows: 3 ICC types x 3 congruence)
- Processing: ICC = var_between / (var_between + var_within) with variations

**Step 2 -> Step 4:**
- Input: step02_fitted_model_{congruence}.pkl (3 pickled models)
- Transformation: Extract random effects from model objects
- Output: step04_random_effects.csv (300 rows: 100 UID x 3 congruence)
- Processing: model.random_effects -> DataFrame

**Step 4 -> Step 5:**
- Input: step04_random_effects.csv (300 rows)
- Transformation: Stratify by congruence, compute Pearson correlation
- Output: step05_intercept_slope_correlation.csv (15 rows: 5 statistics x 3 congruence)
- Processing: Correlate Total_Intercept with Total_Slope per congruence

**Step 3 -> Step 6:**
- Input: step03_icc_estimates.csv (9 rows)
- Transformation: Pivot to wide format, rank by ICC_slope_simple
- Output: step06_congruence_icc_comparison.csv (3 rows: 1 per congruence)
- Processing: Reshape + ranking logic

### Column Naming Conventions

Per names.md (existing conventions from RQ 5.1):

**Identifiers:**
- `UID` - Participant unique identifier (format: P### with leading zeros)
- `composite_ID` - Primary key combining UID and test (format: UID_test)
- `test` - Test session identifier (T1, T2, T3, T4 for Days 0, 1, 3, 6)

**Time Variable (Decision D070):**
- `TSVR_hours` - Time Since VR in hours (actual elapsed time, NOT nominal days)

**IRT Outputs:**
- `theta_<dimension>` - IRT ability estimate for given dimension (e.g., theta_common, theta_congruent, theta_incongruent)
- `se_<dimension>` - Standard error of theta estimate (e.g., se_common)

**LMM Random Effects:**
- `Total_Intercept` - Random intercept deviation from fixed intercept
- `Total_Slope` - Random slope deviation from fixed slope

**Variance Components:**
- `var_intercept` - Random intercept variance
- `var_slope` - Random slope variance
- `cov_int_slope` - Covariance between intercept and slope
- `var_residual` - Residual (within-person) variance

**ICC Estimates:**
- `icc_intercept` - ICC for intercepts
- `icc_slope_simple` - ICC for slopes (simple formula)
- `icc_slope_conditional` - ICC for slopes at Day 6 (conditional on intercept)

**Statistical Outputs:**
- `r` - Pearson correlation coefficient
- `p_uncorrected` - Uncorrected p-value (Decision D068)
- `p_bonferroni` - Bonferroni-corrected p-value (Decision D068)
- `CI_lower` - Lower 95% confidence interval bound
- `CI_upper` - Upper 95% confidence interval bound

**Categorical Variables:**
- `congruence` - Schema congruence level (Common / Congruent / Incongruent)
- `magnitude` - ICC magnitude classification (Low / Moderate / Substantial)

---

## Cross-RQ Dependencies

### Dependency Type: DERIVED Data from RQ 5.4.1 (Dependencies Exist)

**This RQ requires outputs from:**
- **RQ 5.4.1** (Schema-Specific Trajectories)
  - File: results/ch5/5.4.1/data/step03_theta_scores.csv
  - Used in: Step 1 (verify theta structure)
  - Rationale: RQ 5.4.1 calibrates IRT model and estimates theta scores per congruence level. This RQ uses those theta scores for variance decomposition.

  - File: results/ch5/5.4.1/data/step04_lmm_input.csv
  - Used in: Step 1 (primary analysis input)
  - Rationale: RQ 5.4.1 creates long-format LMM input (UID x test x congruence) with TSVR. This RQ stratifies by congruence to fit separate LMMs.

  - File: results/ch5/5.4.1/data/step05_lmm_fitted_model.pkl
  - Used in: Step 1 (reference for convergence check)
  - Rationale: RQ 5.4.1 fits omnibus LMM with Congruence x Time interaction. This RQ uses it as reference for expected model structure (NOT re-fitted).

  - File: results/ch5/5.4.1/status.yaml
  - Used in: Step 1 (dependency validation)
  - Rationale: Verify RQ 5.4.1 completion before proceeding (circuit breaker if incomplete).

**Execution Order Constraint:**
1. RQ 5.4.1 must complete Steps 0-5 successfully (rq_results.status = success)
2. This RQ (5.4.6) executes after RQ 5.4.1 completion
3. NO other RQ dependencies

**Data Source Boundaries (Per Specification 5.1.6):**
- **RAW data:** None (no extraction from master.xlsx in this RQ)
- **DERIVED data:** All inputs from RQ 5.4.1 (theta scores, LMM input, fitted model)
- **Scope:** This RQ does NOT re-calibrate IRT models (uses RQ 5.4.1 theta as-is)
- **Scope:** This RQ fits NEW stratified LMMs (separate from RQ 5.4.1 omnibus model)

**Validation:**
- Step 1: Check results/ch5/5.4.1/status.yaml exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 1: Parse rq_results.status field (circuit breaker: EXPECTATIONS ERROR if != "success")
- Step 1: Check step03_theta_scores.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 1: Check step04_lmm_input.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 1: Check step05_lmm_fitted_model.pkl exists (circuit breaker: EXPECTATIONS ERROR if absent)
- If ANY file missing -> quit with error -> user must execute RQ 5.4.1 first

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
- g_code (Step 14 workflow) will generate stepN_name.py scripts with validation function calls
- bash execution (Step 14 workflow) will run analysis -> validation -> error on validation failure

**Downstream Agent Requirements:**
- **rq_tools:** MUST specify validation tool for EVERY analysis step (no exceptions)
- **rq_analysis:** MUST embed validation tool call for EVERY analysis step (no exceptions)
- **g_code:** MUST generate code with validation function calls (no exceptions)
- **rq_inspect:** MUST verify validation ran successfully (checks logs/stepN_name.log for validation output)

### Validation Requirements By Step

#### Step 1: Load Dependency Data from RQ 5.4.1

**Analysis Tool:** (determined by rq_tools - likely tools.data or pandas read functions)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure + cross-RQ dependency checks)

**What Validation Checks:**
- RQ 5.4.1 status.yaml exists and rq_results.status = "success"
- All 3 required files exist (theta_scores, lmm_input, fitted_model)
- step04_lmm_input.csv: 1200 rows, 6 columns (UID, test, TSVR_hours, congruence, theta, SE)
- Exactly 3 unique congruence levels (Common, Congruent, Incongruent)
- No NaN in theta or TSVR_hours columns
- TSVR_hours in [0, 168] range

**Expected Behavior on Validation Failure:**
- If RQ 5.4.1 incomplete: Circuit breaker EXPECTATIONS ERROR -> quit
- If file missing: Circuit breaker EXPECTATIONS ERROR -> quit
- If data structure invalid: Raise error -> log to logs/step01_load_dependency_data.log -> quit
- g_debug invoked if unexpected data format

---

#### Step 2: Fit Congruence-Stratified LMMs

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.fit_lmm_trajectory_tsvr)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_lmm_convergence + validate_variance_positivity)

**What Validation Checks:**
- All 3 models converged (model.converged = True)
- Variance components positive (var_intercept > 0, var_slope > 0, var_residual > 0)
- No NaN in variance estimates
- Exactly 15 rows in variance_components.csv (5 components x 3 congruence)
- All 3 congruence levels present

**Expected Behavior on Validation Failure:**
- If convergence fails: Apply contingency plan (alternative optimizer -> LRT -> simplified structure)
- If all contingencies fail: Raise error -> log to logs/step02_fit_stratified_lmms.log -> quit
- g_debug invoked to diagnose (insufficient data, model misspecification)

---

#### Step 3: Compute ICC Estimates

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.compute_icc_from_variance_components)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_icc_bounds)

**What Validation Checks:**
- All ICC values in [0, 1] (out of bounds indicates computation error)
- Exactly 9 ICC estimates (3 types x 3 congruence)
- No NaN values
- magnitude column contains only: "Low" / "Moderate" / "Substantial"

**Expected Behavior on Validation Failure:**
- If ICC < 0 or > 1: Raise error (variance component sign error) -> log to logs/step03_compute_icc.log -> quit
- g_debug invoked to check variance component estimates

---

#### Step 4: Extract Random Effects

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.extract_random_effects_from_lmm)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure)

**What Validation Checks:**
- Exactly 300 rows (100 UID x 3 congruence)
- No NaN in Total_Intercept or Total_Slope
- Each UID appears exactly 3 times
- All 3 congruence levels present
- Mean of Total_Intercept ~ 0, Mean of Total_Slope ~ 0 (centering check)

**Expected Behavior on Validation Failure:**
- If NaN random effects: Raise error (model failed to estimate) -> log to logs/step04_extract_random_effects.log -> quit
- If UID count != 100: Raise error (missing participants) -> quit
- g_debug invoked to check model convergence

---

#### Step 5: Test Intercept-Slope Correlation and Create Diagnostic Plots

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.test_intercept_slope_correlation_d068)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_correlation_test_d068)

**What Validation Checks (Decision D068):**
- Exactly 15 rows in correlation.csv (5 statistics x 3 congruence)
- All statistics present: r, p_uncorrected, p_bonferroni, CI_lower, CI_upper
- p_uncorrected in [0, 1], p_bonferroni in [0, 1]
- r in [-1, 1], CI bounds in [-1, 1]
- All 6 PNG files exist and > 10KB (non-empty plots)

**Expected Behavior on Validation Failure:**
- If dual p-values missing: Raise error (Decision D068 violation) -> log to logs/step05_test_correlations_plot_diagnostics.log -> quit
- If plot creation fails: Raise error (empty data) -> quit
- g_debug invoked to diagnose correlation computation or plotting library issues

---

#### Step 6: Compare ICC Across Congruence Levels

**Analysis Tool:** (determined by rq_tools - likely pandas operations + plotting functions)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure)

**What Validation Checks:**
- Exactly 3 rows in comparison.csv (1 per congruence)
- All 3 congruence levels present
- All 3 ICC types populated (no NaN)
- rank_by_slope: exactly one rank=1, one rank=2, one rank=3 (no ties)
- PNG file exists and > 10KB

**Expected Behavior on Validation Failure:**
- If missing congruence: Raise error -> log to logs/step06_compare_icc_across_congruence.log -> quit
- If plot creation fails: Raise error -> quit
- g_debug invoked to check data completeness

---

## Summary

**Total Steps:** 6 (no Step 0 - data pre-exists in RQ 5.4.1)

**Estimated Runtime:** Medium (~15-30 minutes total)
- Step 1: 5 min (dependency loading + validation)
- Step 2: 10-15 min (3 LMM fits with random slopes)
- Step 3: 2 min (ICC computation)
- Step 4: 2 min (random effects extraction)
- Step 5: 5 min (correlation tests + 6 diagnostic plots)
- Step 6: 2 min (comparison table + bar plot)

**Cross-RQ Dependencies:** RQ 5.4.1 (Schema-Specific Trajectories) must complete successfully

**Primary Outputs:**
- Variance components per congruence (data/step02_variance_components.csv)
- ICC estimates per congruence (data/step03_icc_estimates.csv)
- Random effects (data/step04_random_effects.csv)
- Intercept-slope correlations with dual p-values (data/step05_intercept_slope_correlation.csv)
- Diagnostic plots: 6 PNGs (3 histograms + 3 Q-Q plots)
- ICC comparison across congruence (data/step06_congruence_icc_comparison.csv + bar plot)

**Validation Coverage:** 100% (all 6 steps have validation requirements)

**Key Theoretical Predictions:**
- ICC_slope > 0.40 (substantial) indicates forgetting rate is a stable, trait-like individual difference
- Congruent items expected to show highest ICC_slope (most stable due to schema support)
- Incongruent items expected to show lowest ICC_slope (more state-dependent)
- Negative intercept-slope correlations expected (high baseline -> maintained advantage)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-02): Initial plan created by rq_planner agent
  - 6 analysis steps (no extraction - DERIVED data from RQ 5.4.1)
  - LMM-only pipeline (stratified by congruence level)
  - ICC computation (3 types x 3 congruence levels = 9 estimates)
  - Decision D068 applied (dual p-values for correlation tests)
  - Decision D070 inherited (TSVR as time variable from RQ 5.4.1)
  - Cross-RQ dependency: RQ 5.4.1 (theta scores + LMM input)
  - Validation embedded in all 6 steps (per v4.X architecture)
