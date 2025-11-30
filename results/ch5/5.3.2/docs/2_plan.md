# Analysis Plan for RQ 5.4: Linear Trend in Forgetting Rate Across Paradigms

**Created by:** rq_planner agent
**Date:** 2025-11-24
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

RQ 5.4 tests whether forgetting rate decreases monotonically from Free Recall -> Cued Recall -> Recognition, consistent with a retrieval support gradient hypothesis. This is a **secondary analysis** that operates on outputs from RQ 5.3 (Paradigm-Specific Forgetting Trajectories).

**Analysis Type:** Secondary Analysis (Linear Trend Contrast) on RQ 5.3 LMM model
**Pipeline:** LMM contrast testing (no IRT calibration - uses derived data from RQ 5.3)
**Total Steps:** 4 (Step 0: data loading, Steps 1-3: contrast testing and visualization)
**Estimated Runtime:** Low (< 5 minutes total - no model fitting, just contrast computation)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni-corrected)
- Decision D070: TSVR as time variable (inherited from RQ 5.3 model)

**Dependencies:**
- RQ 5.3 must complete successfully before RQ 5.4 can execute
- Required: LMM fitted model (step05_lmm_fitted_model.pkl), LMM input data (step04_lmm_input.csv)

---

## Analysis Plan

This RQ requires 4 steps:

### Step 0: Load RQ 5.3 Outputs

**Dependencies:** None (first step)
**Complexity:** Low (file loading only)

**Purpose:** Load the best-fitting LMM model and theta data from RQ 5.3 for contrast analysis.

**Input:**

**File 1:** results/ch5/rq3/data/step05_lmm_fitted_model.pkl
**Source:** RQ 5.3 Step 5 (LMM fitting)
**Format:** Pickle file containing fitted MixedLM model object
**Expected Content:** Log model (best AIC per RQ 5.3 results)

**File 2:** results/ch5/rq3/data/step04_lmm_input.csv
**Source:** RQ 5.3 Step 4 (TSVR merge)
**Format:** CSV, long format (one row per observation)
**Columns:**
  - composite_ID (string, format: UID_test)
  - UID (string, participant identifier)
  - test (int, values: 1, 2, 3, 4)
  - TSVR_hours (float, actual elapsed time)
  - TSVR_hours_sq (float, squared time for quadratic models)
  - TSVR_hours_log (float, log-transformed time for log models)
  - paradigm (string, values: free_recall, cued_recall, recognition)
  - theta (float, IRT ability estimate)
**Expected Rows:** ~1200 (100 participants x 4 tests x 3 paradigms)

**File 3:** results/ch5/rq3/data/step05_model_comparison.csv
**Source:** RQ 5.3 Step 5 (model comparison)
**Format:** CSV with model comparison results
**Columns:** model_name, AIC, delta_AIC, AIC_weight, converged
**Purpose:** Verify best model is Log (confirmation check)

**Processing:**
1. Load LMM model from pickle file using joblib or pickle
2. Load theta data from CSV using pandas
3. Load model comparison to verify best model is Log
4. Verify model object is valid (has .params, .cov_params() attributes)
5. Map paradigm names to ordered categories: Free_Recall=1, Cued_Recall=2, Recognition=3

**Output:**

**File 1:** data/step00_model_loaded.txt
**Format:** Text file confirming successful load
**Content:** Model name, number of observations, paradigm levels

**Validation Requirement:**
Validation tools MUST be used after data loading tool execution. Specific validation
tools determined by rq_tools based on file existence and model validity requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_model_loaded.txt exists (exact path)
- Expected content: confirmation of model type and data dimensions

*Value Ranges:*
- Model should be Log model (verify model_name in comparison)
- Data should have exactly 3 paradigm levels
- Data should have ~1200 observations (N=100 x 4 tests x 3 paradigms)

*Data Quality:*
- Model object must have valid parameters (not None, not NaN)
- Theta data must match model's nobs attribute
- No missing paradigm labels

*Log Validation:*
- Required pattern: "Model loaded successfully"
- Required pattern: "Best model confirmed: Log"
- Forbidden patterns: "ERROR", "FileNotFoundError", "Model load failed"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step00_load_rq53_outputs.log
- Quit immediately - cannot proceed without RQ 5.3 outputs

---

### Step 1: Extract Marginal Means at Day 3 Midpoint

**Dependencies:** Step 0 (requires loaded model and data)
**Complexity:** Low (prediction computation)

**Purpose:** Extract paradigm-specific marginal means (predicted theta values) at Day 3 midpoint for contrast testing.

**Input:**

**File 1:** Loaded LMM model object (from Step 0 in memory)
**File 2:** data/step00_model_loaded.txt (confirmation of successful load)

**Processing:**
1. Determine Day 3 timepoint in TSVR_hours (approximately 72 hours post-encoding)
2. Create prediction grid: 3 paradigms x Day 3 timepoint
3. For Log model: Use log(72) = 4.277 as time value
4. Compute marginal means using model.predict() with paradigm contrasts
5. Extract standard errors for each paradigm mean from model covariance matrix
6. Create summary table: paradigm, marginal_mean, SE, CI_lower, CI_upper

**Technical Notes:**
- Day 3 midpoint chosen to avoid extrapolation (within observation window: Days 0-6)
- Log model uses log_Days as predictor, so evaluate at log(72/24) = log(3) for nominal Day 3
- Marginal means represent expected theta at Day 3 for each paradigm

**Output:**

**File 1:** data/step01_marginal_means.csv
**Format:** CSV with paradigm-level predictions
**Columns:**
  - paradigm (string): Free_Recall, Cued_Recall, Recognition
  - marginal_mean (float): Predicted theta at Day 3
  - SE (float): Standard error of prediction
  - CI_lower (float): 95% CI lower bound
  - CI_upper (float): 95% CI upper bound
**Expected Rows:** 3 (one per paradigm)

**Validation Requirement:**
Validation tools MUST be used after marginal means extraction tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_marginal_means.csv exists (exact path)
- Expected rows: 3 (one per paradigm)
- Expected columns: 5 (paradigm, marginal_mean, SE, CI_lower, CI_upper)
- Data types: string (paradigm), float (all numeric columns)

*Value Ranges:*
- marginal_mean in [-3, 3] (typical theta range)
- SE in [0.01, 1.0] (reasonable standard error range)
- CI_lower < marginal_mean < CI_upper (confidence interval logic)
- Based on RQ 5.3 results: expect Recognition > Cued >= Free ordering

*Data Quality:*
- All 3 paradigms present (Free_Recall, Cued_Recall, Recognition)
- No NaN values in any column
- No duplicate paradigm rows

*Log Validation:*
- Required pattern: "Marginal means computed at Day 3"
- Required pattern: "All 3 paradigms computed successfully"
- Forbidden patterns: "ERROR", "NaN in marginal means"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step01_extract_marginal_means.log
- Quit immediately

---

### Step 2: Compute Linear Trend Contrast

**Dependencies:** Step 1 (requires marginal means)
**Complexity:** Low (contrast computation)

**Purpose:** Test linear trend contrast within the RQ 5.3 LMM using contrast weights [-1, 0, +1] for ordered paradigms (Free < Cued < Recognition). This tests whether forgetting follows the retrieval support gradient.

**Input:**

**File 1:** Loaded LMM model object (from Step 0 in memory)
**File 2:** data/step01_marginal_means.csv (for reference/verification)

**Processing:**
1. Define linear contrast weights: Free_Recall=-1, Cued_Recall=0, Recognition=+1
2. Extract paradigm coefficients from model fixed effects
3. Compute contrast estimate: sum(weight_i x coefficient_i)
4. Compute contrast SE from model covariance matrix
5. Compute z-statistic: estimate / SE
6. Compute p-value (two-tailed from z)
7. Apply Bonferroni correction: corrected_alpha = 0.0033 (adjusting for ~15 tests across ch5)
8. Report both uncorrected and Bonferroni-corrected significance (Decision D068)

**Statistical Method:**
- **Within-LMM contrast testing:** Tests linear trend directly within RQ 5.3 LMM (preserves full N=100 information and proper degrees of freedom)
- **Contrast weights:** [-1, 0, +1] represent linear polynomial for ordered categorical predictor
- **Interpretation:** Positive contrast estimate = forgetting decreases from Free to Recognition (supports gradient hypothesis)

**Output:**

**File 1:** results/step02_linear_trend_contrast.csv
**Format:** CSV with contrast test results
**Columns:**
  - contrast_name (string): "Linear_Trend"
  - estimate (float): Contrast estimate (weighted sum)
  - SE (float): Standard error of contrast
  - z_value (float): z-statistic
  - p_value_uncorrected (float): Two-tailed p-value
  - p_value_bonferroni (float): Bonferroni-corrected p-value
  - significant_uncorrected (bool): p < 0.05
  - significant_bonferroni (bool): p < 0.0033
  - CI_lower (float): 95% CI lower bound
  - CI_upper (float): 95% CI upper bound
**Expected Rows:** 1 (single linear trend test)

**File 2:** results/step02_contrast_interpretation.txt
**Format:** Text file with plain-language interpretation
**Content:**
  - Contrast estimate and direction
  - Statistical significance (both uncorrected and corrected)
  - Theoretical interpretation (supports/does not support gradient hypothesis)

**Validation Requirement:**
Validation tools MUST be used after contrast computation tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step02_linear_trend_contrast.csv exists (exact path)
- results/step02_contrast_interpretation.txt exists (exact path)
- Expected rows in CSV: 1 (single contrast)
- Expected columns: 10 (as listed above)

*Value Ranges:*
- estimate: unbounded (but typically in [-2, 2] for theta-scale effects)
- SE in [0.01, 1.0] (reasonable standard error range)
- z_value: unbounded (but |z| > 5 would be unusual)
- p_value_uncorrected in [0, 1]
- p_value_bonferroni in [0, 1]
- p_value_bonferroni >= p_value_uncorrected (Bonferroni is more conservative)

*Data Quality:*
- No NaN values in any column
- SE > 0 (standard error must be positive)
- CI_lower < estimate < CI_upper (confidence interval logic)

*Log Validation:*
- Required pattern: "Linear trend contrast computed"
- Required pattern: "Contrast weights: Free=-1, Cued=0, Recognition=+1"
- Required pattern: "Decision D068: Dual p-values reported"
- Forbidden patterns: "ERROR", "Division by zero", "Invalid contrast"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step02_compute_linear_trend_contrast.log
- Quit immediately

---

### Step 3: Prepare Visualization Data and Generate Plot

**Dependencies:** Step 1 and Step 2 (requires marginal means and contrast results)
**Complexity:** Low (data preparation and plotting)

**Purpose:** Create plot source CSV for bar plot showing forgetting rates across paradigms with linear trend overlay. This follows Option B architecture (g_code creates plot source CSV, rq_plots generates final visualization).

**Input:**

**File 1:** data/step01_marginal_means.csv
**Format:** CSV with paradigm-level predictions
**Columns:** paradigm, marginal_mean, SE, CI_lower, CI_upper

**File 2:** results/step02_linear_trend_contrast.csv
**Format:** CSV with contrast results
**Columns:** contrast_name, estimate, SE, z_value, p_value_uncorrected, p_value_bonferroni, etc.

**Processing:**
1. Load marginal means from Step 1
2. Add ordered numeric code: Free_Recall=1, Cued_Recall=2, Recognition=3
3. Add contrast result summary (p-value, significance status) for plot annotation
4. Compute fitted linear trend line values using contrast coefficients
5. Add zero reference line coordinates
6. Save plot source CSV

**Output:**

**File 1:** plots/step03_paradigm_forgetting_rates_data.csv
**Format:** CSV, plot-ready data
**Columns:**
  - paradigm (string): Free_Recall, Cued_Recall, Recognition
  - paradigm_code (int): 1, 2, 3 (for x-axis ordering)
  - marginal_mean (float): Predicted theta at Day 3 (y-axis values for bars)
  - SE (float): Standard error (for error bars)
  - CI_lower (float): 95% CI lower bound
  - CI_upper (float): 95% CI upper bound
  - trend_line (float): Fitted linear trend values (for overlay line)
**Expected Rows:** 3 (one per paradigm)

**File 2:** plots/step03_contrast_annotation.txt
**Format:** Text file with plot annotation text
**Content:**
  - Linear trend: estimate, z, p (formatted for plot subtitle)
  - Significance statement

**Plot Description:** Bar plot with x-axis = paradigms (ordered), y-axis = marginal mean theta at Day 3, error bars showing 95% CI, linear trend line overlaid, horizontal reference line at zero.

**Plotting Function (rq_plots will call):** Bar plot with error bars and trend line overlay
- rq_plots agent maps this description to appropriate tools/plots.py functions
- Plot reads plots/step03_paradigm_forgetting_rates_data.csv (created by this step)
- No data aggregation in rq_plots (visualization only per Option B)

**Validation Requirement:**
Validation tools MUST be used after plot data preparation tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- plots/step03_paradigm_forgetting_rates_data.csv exists (exact path)
- plots/step03_contrast_annotation.txt exists (exact path)
- Expected rows: 3 (one per paradigm)
- Expected columns: 7 (paradigm, paradigm_code, marginal_mean, SE, CI_lower, CI_upper, trend_line)
- Data types: string (paradigm), int (paradigm_code), float (all numeric columns)

*Value Ranges:*
- paradigm_code in {1, 2, 3}
- marginal_mean in [-3, 3] (typical theta range)
- SE in [0.01, 1.0]
- trend_line in [-3, 3]
- CI_lower < CI_upper for all rows

*Data Quality:*
- All 3 paradigms present
- paradigm_code correctly ordered (Free=1, Cued=2, Recognition=3)
- No NaN values
- No duplicate paradigm rows

*Log Validation:*
- Required pattern: "Plot data preparation complete: 3 rows created"
- Required pattern: "All paradigms represented"
- Required pattern: "Trend line computed"
- Forbidden patterns: "ERROR", "NaN values detected", "Missing paradigm"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step03_prepare_paradigm_plot_data.log
- Quit immediately - do NOT proceed to rq_plots

---

## Expected Data Formats

### Step-to-Step Data Flow

```
RQ 5.3 Outputs                    RQ 5.4 Analysis
--------------                    ---------------
step05_lmm_fitted_model.pkl  -->  Step 0: Load model
step04_lmm_input.csv         -->  Step 0: Load data
                                       |
                                       v
                                  Step 1: Extract marginal means at Day 3
                                       |
                                       v
                                  Step 2: Compute linear trend contrast
                                       |
                                       v
                                  Step 3: Prepare plot data
                                       |
                                       v
                                  rq_plots: Generate visualization
```

### Column Naming Conventions (from names.md)

- `paradigm`: Memory retrieval paradigm factor (Free_Recall, Cued_Recall, Recognition)
- `marginal_mean`: Model-predicted theta at specified timepoint
- `SE`: Standard error of estimate
- `CI_lower`, `CI_upper`: 95% confidence interval bounds
- `paradigm_code`: Numeric ordering for plotting (1=Free, 2=Cued, 3=Recognition)

### Data Type Constraints

| Column | Type | Nullable | Valid Range |
|--------|------|----------|-------------|
| paradigm | string | No | {Free_Recall, Cued_Recall, Recognition} |
| paradigm_code | int | No | {1, 2, 3} |
| marginal_mean | float | No | [-3, 3] |
| SE | float | No | [0.01, 1.0] |
| CI_lower | float | No | [-3, 3] |
| CI_upper | float | No | [-3, 3] |
| trend_line | float | No | [-3, 3] |
| estimate | float | No | unbounded |
| z_value | float | No | unbounded |
| p_value_uncorrected | float | No | [0, 1] |
| p_value_bonferroni | float | No | [0, 1] |

---

## Cross-RQ Dependencies

### Dependency Type 2: DERIVED Data from Other RQs (Dependencies Exist)

**This RQ requires outputs from:**
- **RQ 5.3** (Paradigm-Specific Forgetting Trajectories)
  - File 1: results/ch5/rq3/data/step05_lmm_fitted_model.pkl
    - Used in: Step 0 (load model for contrast testing)
    - Rationale: RQ 5.3 fits the best LMM model (Log model) comparing paradigms. RQ 5.4 tests linear trend contrast WITHIN this model.
  - File 2: results/ch5/rq3/data/step04_lmm_input.csv
    - Used in: Step 0 (load data for prediction grid)
    - Rationale: Contains theta scores with paradigm labels needed for marginal means computation.
  - File 3: results/ch5/rq3/data/step05_model_comparison.csv
    - Used in: Step 0 (verify best model is Log)
    - Rationale: Confirms which model won AIC comparison (should be Log).

**Execution Order Constraint:**
1. RQ 5.3 must complete all steps (Step 0 through Step 7) with rq_results: success
2. RQ 5.4 executes after RQ 5.3 completion

**Data Source Boundaries (Per Specification 5.1.6):**
- **RAW data:** None - this RQ uses no raw data from master.xlsx
- **DERIVED data:** All data from RQ 5.3 (theta scores, fitted LMM model)
- **Scope:** This RQ does NOT re-fit LMM models; it tests contrasts within RQ 5.3's best model

**Validation:**
- Step 0: Check results/ch5/rq3/status.yaml shows rq_results: success
- Step 0: Check results/ch5/rq3/data/step05_lmm_fitted_model.pkl exists
- Step 0: Check results/ch5/rq3/data/step04_lmm_input.csv exists
- If any file missing -> quit with error -> user must execute RQ 5.3 first

---

## Validation Requirements

**CRITICAL MANDATE:**

Every analysis step in this plan MUST use validation tools after analysis tool execution.

This is not optional. This is the core architectural principle preventing cascading
failures observed in v3.0 (where analysis errors propagated undetected through 5+
downstream steps before discovery).

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

#### Step 0: Load RQ 5.3 Outputs

**What Validation Checks:**
- Dependency files exist (pkl model, csv data)
- Model object valid (has required attributes)
- Data dimensions match expected (~1200 observations)
- Best model confirmed as Log

**Expected Behavior on Validation Failure:**
- Raise error: "RQ 5.3 dependency missing or invalid"
- Quit immediately

---

#### Step 1: Extract Marginal Means at Day 3

**What Validation Checks:**
- Output file exists (data/step01_marginal_means.csv)
- Exactly 3 rows (one per paradigm)
- All paradigms present
- Values in expected ranges
- No NaN values

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Quit immediately

---

#### Step 2: Compute Linear Trend Contrast

**What Validation Checks:**
- Output files exist (results/step02_linear_trend_contrast.csv, results/step02_contrast_interpretation.txt)
- Exactly 1 row (single contrast test)
- p-values in [0, 1]
- Bonferroni p >= uncorrected p
- SE > 0

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Quit immediately

---

#### Step 3: Prepare Visualization Data

**What Validation Checks:**
- Output files exist (plots/step03_paradigm_forgetting_rates_data.csv, plots/step03_contrast_annotation.txt)
- Exactly 3 rows (one per paradigm)
- paradigm_code correctly ordered
- No NaN values
- CI bounds logical (lower < upper)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Quit immediately - do NOT proceed to rq_plots

---

## Summary

**Total Steps:** 4
**Estimated Runtime:** < 5 minutes (no model fitting, contrast computation only)
**Cross-RQ Dependencies:** RQ 5.3 (DERIVED data - fitted LMM model and theta scores)

**Primary Outputs:**
- data/step01_marginal_means.csv (paradigm predictions at Day 3)
- results/step02_linear_trend_contrast.csv (linear trend test results)
- results/step02_contrast_interpretation.txt (plain-language interpretation)
- plots/step03_paradigm_forgetting_rates_data.csv (plot source CSV)
- plots/step03_contrast_annotation.txt (plot annotation text)

**Validation Coverage:** 100% (all 4 steps have validation requirements)

**Decisions Applied:**
- D068: Dual p-value reporting (uncorrected + Bonferroni-corrected)
- D070: TSVR as time variable (inherited from RQ 5.3 model)

**Theoretical Expectation:**
- Positive contrast estimate indicates forgetting rate decreases from Free -> Cued -> Recognition
- Significant linear trend supports retrieval support gradient hypothesis
- Based on RQ 5.3 pairwise contrasts (Recognition > Free/Cued, p=.002), linear trend expected to be significant

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-11-24): Initial plan created by rq_planner agent
