# Analysis Plan for RQ 5.13: Between-Person Variance in Forgetting Rates

**Created by:** rq_planner agent
**Date:** 2025-11-26
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This RQ examines the variance decomposition of forgetting trajectories from RQ 5.7's best-fitting LMM. It quantifies what proportion of variation in forgetting rates reflects stable individual differences (between-person variance) versus measurement noise or within-person fluctuation. The analysis uses random slopes from the saved LMM with all VR items (single-factor "All" analysis) across four test sessions.

**Pipeline:** Variance Decomposition Analysis (DERIVED data from RQ 5.7)
**Steps:** 5 analysis steps (Step 0: data loading + Steps 1-4: variance extraction and visualization)
**Estimated Runtime:** Low (10-15 minutes total - no model fitting, only extraction/computation)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (intercept-slope correlation test)
- Cross-RQ Dependency: Requires RQ 5.7 complete (saved LMM model object with random slopes)

**Analysis Approach:**
This RQ does NOT fit new models. Instead, it loads RQ 5.7's saved LMM object and extracts variance components, random effects, and ICC values to quantify individual differences in forgetting rate. Key outputs include ICC for intercepts and slopes, intercept-slope correlation, and distribution of individual random slopes (saved for RQ 5.14 clustering analysis).

---

## Analysis Plan

### Step 0: Load Data from RQ 5.7

**Purpose:** Load saved LMM model object and associated data files from RQ 5.7

**Dependencies:** None (first step)
**Complexity:** Low (<5 minutes)

**Input:**

**File 1:** results/ch5/rq7/data/step05_lmm_all_bestmodel.pkl
**Source:** RQ 5.7 Step 5 (best-fitting LMM with random slopes)
**Format:** Python pickle file (statsmodels MixedLM fitted model object)
**Required Properties:**
  - Model fitted with random intercepts AND random slopes
  - Converged successfully (convergence status = True)
  - Contains random effects covariance matrix
  - Contains residual variance estimate

**File 2:** results/ch5/rq7/data/step04_theta_scores_allitems.csv
**Source:** RQ 5.7 Step 4 (IRT theta scores for "All" factor)
**Format:** CSV with columns:
  - UID (string, participant identifier)
  - TEST (string, test session: T1/T2/T3/T4)
  - theta (float, ability estimate)
**Expected Rows:** ~400 (100 participants x 4 tests)

**File 3:** results/ch5/rq7/data/step00_tsvr_mapping.csv
**Source:** RQ 5.7 Step 0 (TSVR time variable mapping)
**Format:** CSV with columns:
  - UID (string, participant identifier)
  - TEST (string, test session)
  - TSVR (float, hours since encoding, range: [0, ~168])
**Expected Rows:** ~400 (100 participants x 4 tests)

**Processing:**
- Load pickled LMM model object using pickle.load() or joblib.load()
- Verify model convergence status (raise error if not converged)
- Load theta scores and TSVR mapping CSVs
- Validate that all files exist and have expected structure

**Output:**

**File:** data/step00_loaded_model_info.txt
**Format:** Text file with model metadata
**Content:**
  - Model convergence status
  - Number of observations
  - Random effects structure (intercepts + slopes)
  - Fixed effects formula
  - Number of participants
  - Timestamp of RQ 5.7 model fit

**Expected Rows:** N/A (metadata text file, ~15-20 lines)

**Validation Requirement:**
Validation tools MUST be used after data loading. Specific validation tools will be determined by rq_tools based on file existence and model object structure validation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_loaded_model_info.txt exists (exact path)
- Expected lines: 15-20 lines of metadata
- Contains convergence status line
- Contains random effects structure confirmation

*Value Ranges:*
- N/A (metadata file, no numeric ranges)

*Data Quality:*
- Convergence status = True (if False, entire RQ invalid)
- Random effects include BOTH intercepts AND slopes (if slopes missing, variance decomposition impossible)
- Number of observations matches expected ~400 (100 participants x 4 tests)

*Log Validation:*
- Required pattern: "Model loaded successfully from RQ 5.7"
- Required pattern: "Convergence status: True"
- Required pattern: "Random effects: intercepts + slopes"
- Forbidden patterns: "ERROR", "Model convergence failed", "Slopes not estimated"
- Acceptable warnings: None expected for data loading

**Expected Behavior on Validation Failure:**
- If model file missing: Raise error "RQ 5.7 not complete - run RQ 5.7 first", quit immediately
- If convergence = False: Raise error "RQ 5.7 model did not converge - check RQ 5.7 logs", quit immediately
- If slopes missing: Raise error "RQ 5.7 model missing random slopes - refit with random slopes enabled", quit immediately
- Log failure to logs/step00_load_data.log
- g_debug invoked to diagnose dependency issues

---

### Step 1: Extract Variance Components

**Purpose:** Extract variance components from LMM random effects covariance matrix

**Dependencies:** Step 0 (requires loaded LMM model object)
**Complexity:** Low (<5 minutes)

**Input:**

**Object:** Loaded LMM model object (from Step 0, in memory)
**Required Attributes:**
  - cov_re (random effects covariance matrix, 2x2 for intercepts + slopes)
  - scale (residual variance, scalar)
  - random_effects (dictionary of participant-specific random effects)

**Processing:**
- Extract random effects covariance matrix (cov_re) from model object
- Compute variance components:
  - var_intercept = cov_re[0, 0] (variance of random intercepts)
  - var_slope = cov_re[1, 1] (variance of random slopes)
  - cov_int_slope = cov_re[0, 1] (covariance between intercepts and slopes)
- Extract residual variance (scale parameter from model)
- Compute correlation between intercepts and slopes: r = cov / sqrt(var_int * var_slope)

**Output:**

**File:** data/step01_variance_components.csv
**Format:** CSV with columns:
  - component (string: var_intercept, var_slope, cov_int_slope, var_residual, cor_int_slope)
  - value (float: variance/covariance estimate)
**Expected Rows:** 5 (one row per variance component)

**Validation Requirement:**
Validation tools MUST be used after variance extraction. Specific validation tools will be determined by rq_tools based on variance component properties.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_variance_components.csv exists (exact path)
- Expected rows: 5 (var_intercept, var_slope, cov_int_slope, var_residual, cor_int_slope)
- Expected columns: 2 (component: string, value: float)

*Value Ranges:*
- var_intercept > 0 (variance must be positive)
- var_slope > 0 (variance must be positive)
- var_residual > 0 (variance must be positive)
- cov_int_slope unrestricted (can be negative, zero, or positive)
- cor_int_slope in [-1, 1] (correlation bounds)

*Data Quality:*
- No NaN values tolerated (all components must be estimated)
- var_intercept typically in [0.1, 2.0] (theta scale)
- var_slope typically in [0.001, 0.1] (slope scale smaller than intercept)
- Expected pattern: var_intercept > var_slope (baseline more variable than rate)

*Log Validation:*
- Required pattern: "Variance components extracted: 5 components"
- Required pattern: "Intercept variance: {value}" (value > 0)
- Required pattern: "Slope variance: {value}" (value > 0)
- Forbidden patterns: "ERROR", "NaN variance", "Negative variance"
- Acceptable warnings: "High intercept-slope correlation (|r| > 0.5)" (theoretical interest, not error)

**Expected Behavior on Validation Failure:**
- If variance <= 0: Raise error "Invalid variance estimate (non-positive) - check model fit", quit immediately
- If NaN detected: Raise error "Missing variance component - model estimation issue", quit immediately
- Log failure to logs/step01_extract_variance.log
- g_debug invoked to diagnose model structure issues

---

### Step 2: Compute Intraclass Correlation Coefficients (ICC)

**Purpose:** Compute ICC for intercepts and slopes to quantify between-person variance proportion

**Dependencies:** Step 1 (requires variance components)
**Complexity:** Low (<5 minutes)

**Input:**

**File:** data/step01_variance_components.csv (from Step 1)
**Required Rows:**
  - var_intercept (variance of random intercepts)
  - var_slope (variance of random slopes)
  - var_residual (within-person error variance)
  - cov_int_slope (covariance between intercepts and slopes)

**Processing:**
- ICC for intercepts (simple ratio):
  - ICC_intercept = var_intercept / (var_intercept + var_residual)
  - Interpretation: Proportion of variance in baseline ability that is between-person

- ICC for slopes (Method 1 - simple ratio):
  - ICC_slope_simple = var_slope / (var_slope + var_residual)
  - Interpretation: Rough proportion of variance in forgetting rate that is between-person

- ICC for slopes (Method 2 - conditional at Day 6):
  - Accounts for intercept-slope covariance
  - Formula: ICC_slope_conditional = [var_intercept + 2*cov_int_slope*time + var_slope*time^2] / [var_intercept + 2*cov_int_slope*time + var_slope*time^2 + var_residual]
  - Evaluated at time = Day 6 (maximum follow-up)
  - Interpretation: Between-person variance proportion at end of trajectory

- Interpret ICC magnitude:
  - ICC > 0.40 = substantial (trait-like individual difference)
  - ICC 0.20-0.40 = moderate (mixed trait/state)
  - ICC < 0.20 = low (mostly noise)

**Output:**

**File:** results/step02_icc_estimates.csv
**Format:** CSV with columns:
  - icc_type (string: ICC_intercept, ICC_slope_simple, ICC_slope_conditional_day6)
  - icc_value (float, range: [0, 1])
  - interpretation (string: substantial/moderate/low)
**Expected Rows:** 3 (one row per ICC estimate)

**Validation Requirement:**
Validation tools MUST be used after ICC computation. Specific validation tools will be determined by rq_tools based on ICC calculation validation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step02_icc_estimates.csv exists (exact path)
- Expected rows: 3 (ICC_intercept, ICC_slope_simple, ICC_slope_conditional_day6)
- Expected columns: 3 (icc_type: string, icc_value: float, interpretation: string)

*Value Ranges:*
- icc_value in [0, 1] (proportion by definition)
- ICC_intercept typically in [0.4, 0.8] (hypothesis: high baseline stability)
- ICC_slope_simple typically in [0.2, 0.6] (hypothesis: moderate-to-high slope stability)
- ICC_slope_conditional typically close to ICC_slope_simple (unless high covariance)

*Data Quality:*
- No NaN values tolerated (all ICC must be computed)
- interpretation must match value: >0.40 = "substantial", 0.20-0.40 = "moderate", <0.20 = "low"
- Expected pattern: ICC_intercept > ICC_slope (baseline more stable than rate)

*Log Validation:*
- Required pattern: "ICC computed: 3 estimates"
- Required pattern: "ICC_intercept = {value} ({interpretation})"
- Required pattern: "ICC_slope_simple = {value} ({interpretation})"
- Forbidden patterns: "ERROR", "ICC outside [0,1]", "NaN ICC"
- Acceptable warnings: "ICC_slope < 0.20 (low stability - forgetting mostly noise)" (theoretical finding, not error)

**Expected Behavior on Validation Failure:**
- If ICC outside [0, 1]: Raise error "Invalid ICC (outside bounds) - check variance estimates", quit immediately
- If interpretation mismatch: Raise error "Interpretation inconsistent with ICC value", quit immediately
- Log failure to logs/step02_compute_icc.log
- g_debug invoked to diagnose computation issues

---

### Step 3: Extract Individual Random Effects and Test Correlation

**Purpose:** Extract person-specific random intercepts and slopes, compute correlation between them

**Dependencies:** Step 0 (requires loaded LMM model object)
**Complexity:** Low (<5 minutes)

**Input:**

**Object:** Loaded LMM model object (from Step 0, in memory)
**Required Attributes:**
  - random_effects (dictionary: keys = UID, values = [random_intercept, random_slope])
  - fe_params (fixed effects parameter estimates)

**Processing:**
- Extract random effects dictionary from model object
- For each participant:
  - Extract random intercept (deviation from fixed intercept)
  - Extract random slope (deviation from fixed slope)
  - Compute total intercept = fixed_intercept + random_intercept
  - Compute total slope = fixed_slope + random_slope
- Create DataFrame with columns: UID, random_intercept, random_slope, total_intercept, total_slope
- Compute descriptive statistics for random slopes: mean, SD, min, max, Q1, Q2 (median), Q3
- Test intercept-slope correlation:
  - Pearson r between random_intercept and random_slope
  - Hypothesis test: H0: r = 0 vs H1: r != 0 (two-tailed t-test)
  - Report BOTH uncorrected p-value AND Bonferroni-corrected p-value (Decision D068)
  - Bonferroni alpha = 0.05 / 15 = 0.0033 (15 tests in Chapter 5 per thesis plan)
  - Interpret direction: r < 0 = high baseline -> slower forgetting (maintain advantage)

**Output:**

**File 1:** data/step03_random_effects.csv
**Format:** CSV with columns:
  - UID (string, participant identifier)
  - random_intercept (float, deviation from population mean baseline)
  - random_slope (float, deviation from population mean forgetting rate)
  - total_intercept (float, participant-specific baseline ability)
  - total_slope (float, participant-specific forgetting rate)
**Expected Rows:** ~100 (one row per participant)

**File 2:** results/step03_slope_descriptives.csv
**Format:** CSV with columns:
  - statistic (string: mean, SD, min, max, Q1, Q2, Q3)
  - value (float, descriptive statistic for random slopes)
**Expected Rows:** 7 (one row per descriptive statistic)

**File 3:** results/step03_intercept_slope_correlation.csv
**Format:** CSV with columns:
  - correlation_r (float, Pearson r between intercepts and slopes)
  - p_uncorrected (float, uncorrected p-value)
  - p_bonferroni (float, Bonferroni-corrected p-value, alpha = 0.0033)
  - interpretation (string: "High baseline -> slower forgetting" if r < 0, "High baseline -> faster forgetting" if r > 0)
**Expected Rows:** 1 (single correlation test)

**Validation Requirement:**
Validation tools MUST be used after random effects extraction and correlation testing. Specific validation tools will be determined by rq_tools based on correlation test validation and Decision D068 compliance.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_random_effects.csv exists (exact path)
  - Expected rows: ~100 (one per participant)
  - Expected columns: 5 (UID, random_intercept, random_slope, total_intercept, total_slope)
- results/step03_slope_descriptives.csv exists
  - Expected rows: 7 (mean, SD, min, max, Q1, Q2, Q3)
  - Expected columns: 2 (statistic, value)
- results/step03_intercept_slope_correlation.csv exists
  - Expected rows: 1
  - Expected columns: 4 (correlation_r, p_uncorrected, p_bonferroni, interpretation)

*Value Ranges:*
- random_intercept approximately normal with mean ~ 0, SD ~ 0.4-0.8 (random effects centered at 0)
- random_slope approximately normal with mean ~ 0, SD ~ 0.05-0.15 (smaller scale than intercepts)
- total_intercept in [-3, 3] (theta scale)
- total_slope typically in [-0.3, 0.1] (negative = forgetting, positive = improvement)
- correlation_r in [-1, 1]
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1], typically 15x larger than p_uncorrected

*Data Quality:*
- All 100 participants present (no missing random effects)
- No NaN values (model must estimate random effects for all participants)
- Random effects approximately normally distributed (check via Q-Q plot in Step 4)
- Decision D068 compliance: BOTH p_uncorrected AND p_bonferroni reported

*Log Validation:*
- Required pattern: "Random effects extracted: 100 participants"
- Required pattern: "Slope descriptives computed: mean = {value}, SD = {value}"
- Required pattern: "Intercept-slope correlation: r = {value}, p_uncorrected = {value}, p_bonferroni = {value}"
- Required pattern: "Decision D068: Dual p-values reported"
- Forbidden patterns: "ERROR", "Missing random effects", "p-value outside [0,1]"
- Acceptable warnings: "Non-significant correlation (p > 0.05)" (theoretical finding, not error)

**Expected Behavior on Validation Failure:**
- If N != 100: Raise error "Missing random effects for some participants", quit immediately
- If NaN detected: Raise error "NaN random effects - model estimation issue", quit immediately
- If only one p-value reported: Raise error "Decision D068 violation - must report BOTH uncorrected and Bonferroni p-values", quit immediately
- Log failure to logs/step03_extract_random_effects.log
- g_debug invoked to diagnose extraction or Decision D068 compliance issues

---

### Step 4: Visualize Random Slopes Distribution

**Purpose:** Generate diagnostic plots for random slopes distribution and normality assumption

**Dependencies:** Step 3 (requires random effects data)
**Complexity:** Low (<5 minutes)

**Input:**

**File:** data/step03_random_effects.csv (from Step 3)
**Required Columns:**
  - UID (participant identifier)
  - random_slope (participant-specific forgetting rate deviation)

**Processing:**
- Create histogram of random_slope distribution:
  - Bins: 20-30 bins (automatic binning via matplotlib)
  - Overlay normal curve with mean = 0, SD = empirical SD from data
  - Add vertical line at mean (should be near 0 for random effects)
  - X-axis label: "Random Slope (Forgetting Rate Deviation from Population Mean)"
  - Y-axis label: "Frequency"
  - Title: "Distribution of Individual Forgetting Rates (Random Slopes)"

- Create Q-Q plot (quantile-quantile plot):
  - Compare empirical quantiles of random_slope to theoretical normal quantiles
  - Add reference line (y = x) for perfect normality
  - Assess deviation from normality: points should fall near reference line
  - Purpose: Validate LMM assumption that random effects are normally distributed

**Output:**

**File 1:** plots/step04_random_slopes_histogram.png
**Format:** PNG image
**Dimensions:** 800 x 600 pixels @ 300 DPI
**Content:** Histogram with normal curve overlay showing distribution of random slopes

**File 2:** plots/step04_random_slopes_qqplot.png
**Format:** PNG image
**Dimensions:** 800 x 600 pixels @ 300 DPI
**Content:** Q-Q plot assessing normality of random slopes

**Validation Requirement:**
Validation tools MUST be used after plot generation. Specific validation tools will be determined by rq_tools based on plot file validation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- plots/step04_random_slopes_histogram.png exists (exact path)
- plots/step04_random_slopes_qqplot.png exists (exact path)
- File sizes reasonable (10-200 KB for PNG images)

*Value Ranges:*
- N/A (image files, no numeric validation)

*Data Quality:*
- Both plots created successfully
- Image dimensions correct (800 x 600 pixels)
- No corrupted image files (can be opened)

*Log Validation:*
- Required pattern: "Histogram created: plots/step04_random_slopes_histogram.png"
- Required pattern: "Q-Q plot created: plots/step04_random_slopes_qqplot.png"
- Required pattern: "Normality assumption check: Q-Q plot available for inspection"
- Forbidden patterns: "ERROR", "Failed to create plot", "Image corrupted"
- Acceptable warnings: "Deviation from normality detected in Q-Q plot" (descriptive finding for discussion, not fatal error)

**Expected Behavior on Validation Failure:**
- If plot file missing: Raise error "Plot generation failed - check plotting library", quit immediately
- If file size = 0: Raise error "Empty plot file - plotting code error", quit immediately
- Log failure to logs/step04_visualize_slopes.log
- g_debug invoked to diagnose plotting issues

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 -> Step 1:** LMM model object (in-memory) -> variance components CSV
- Extract cov_re matrix (2x2 array) -> reshape to long format (5 rows: var_int, var_slope, cov, var_res, cor)

**Step 1 -> Step 2:** Variance components CSV -> ICC estimates CSV
- Read variance components -> compute ICC ratios -> write ICC table with interpretation

**Step 0 -> Step 3:** LMM model object (in-memory) -> random effects CSV
- Extract random_effects dictionary (keys = UID, values = [intercept, slope]) -> flatten to DataFrame (100 rows x 5 cols)

**Step 3 -> Step 4:** Random effects CSV -> plots (PNG images)
- Read random_slope column -> generate histogram + Q-Q plot -> save as images

### Column Naming Conventions

**Per names.md conventions:**
- UID: Participant identifier (string, format: P### with leading zeros)
- random_intercept: Participant-specific deviation from population mean baseline
- random_slope: Participant-specific deviation from population mean forgetting rate
- total_intercept: Participant-specific baseline ability (fixed + random)
- total_slope: Participant-specific forgetting rate (fixed + random)

**New conventions introduced in this RQ:**
- component: Variance component name (var_intercept, var_slope, cov_int_slope, var_residual, cor_int_slope)
- value: Variance/covariance estimate (float)
- icc_type: ICC name (ICC_intercept, ICC_slope_simple, ICC_slope_conditional_day6)
- icc_value: ICC estimate (proportion in [0, 1])
- interpretation: ICC magnitude interpretation (substantial/moderate/low)
- correlation_r: Pearson correlation coefficient
- p_uncorrected: Uncorrected p-value (Decision D068)
- p_bonferroni: Bonferroni-corrected p-value (Decision D068, alpha = 0.0033)

### Data Type Constraints

**Variance components:**
- var_intercept, var_slope, var_residual: Must be > 0 (variances are positive)
- cov_int_slope: Unrestricted (can be negative, zero, positive)
- cor_int_slope: Must be in [-1, 1] (correlation bounds)

**ICC estimates:**
- icc_value: Must be in [0, 1] (proportion by definition)
- interpretation: Must be categorical ("substantial", "moderate", "low")

**Random effects:**
- random_intercept, random_slope: Approximately normal with mean ~ 0 (random effects centered)
- total_intercept, total_slope: Theta scale, unrestricted range

**Correlation test:**
- correlation_r: Must be in [-1, 1]
- p_uncorrected, p_bonferroni: Must be in [0, 1]
- p_bonferroni = 15 * p_uncorrected (Bonferroni correction factor)

---

## Cross-RQ Dependencies

### Dependency Type 2: DERIVED Data from Other RQs (Dependencies Exist)

**This RQ requires outputs from:**
- **RQ 5.7** (Trajectory functional form analysis - best-fitting LMM)
  - File: results/ch5/rq7/data/step05_lmm_all_bestmodel.pkl
  - Used in: Step 0 (load saved LMM model object)
  - Rationale: RQ 5.7 fits the trajectory model with random slopes. This RQ extracts variance components from that fitted model to quantify individual differences.

  - File: results/ch5/rq7/data/step04_theta_scores_allitems.csv
  - Used in: Step 0 (participant ability estimates)
  - Rationale: Needed for context, not directly analyzed in variance decomposition

  - File: results/ch5/rq7/data/step00_tsvr_mapping.csv
  - Used in: Step 0 (time variable mapping)
  - Rationale: Needed for context, not directly analyzed in variance decomposition

**Execution Order Constraint:**
1. RQ 5.7 must complete ALL 5 steps (IRT calibration, purification, theta extraction, TSVR merge, LMM trajectory modeling with random slopes)
2. RQ 5.7 must SAVE the best-fitting LMM model object as .pkl file
3. This RQ executes after RQ 5.7 completion (uses saved model)

**Data Source Boundaries (Per Specification 5.1.6):**
- **RAW data:** None (this RQ uses DERIVED data exclusively)
- **DERIVED data:** All inputs from RQ 5.7 (model object, theta scores, TSVR mapping)
- **Scope:** This RQ does NOT fit models. It extracts variance components and random effects from pre-fitted RQ 5.7 model.

**Validation:**
- Step 0: Check results/ch5/rq7/data/step05_lmm_all_bestmodel.pkl exists (EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch5/rq7/data/step04_theta_scores_allitems.csv exists (EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch5/rq7/data/step00_tsvr_mapping.csv exists (EXPECTATIONS ERROR if absent)
- If ANY file missing -> quit with error -> user must execute RQ 5.7 first

**Downstream Usage:**
- data/step03_random_effects.csv will be used by RQ 5.14 (clustering analysis to identify fast vs slow forgetters)
- RQ 5.14 dependency documented in that RQ's 2_plan.md

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

#### Step 0: Load Data from RQ 5.7

**Analysis Tool:** (determined by rq_tools - likely custom file loading + model unpickling)
**Validation Tool:** (determined by rq_tools - likely file existence + model convergence check)

**What Validation Checks (Substance - rq_inspect scope):**
- All 3 required files exist (model .pkl, theta scores CSV, TSVR mapping CSV)
- Model object loads successfully (pickle unpacking works)
- Model convergence status = True (if False, variance decomposition invalid)
- Random effects structure includes BOTH intercepts AND slopes (if slopes missing, this RQ cannot proceed)
- Expected row counts match (~400 rows in theta scores and TSVR mapping)

**Expected Behavior on Validation Failure:**
- If file missing: Raise error "RQ 5.7 dependency not met - file {filename} missing", quit immediately
- If convergence = False: Raise error "RQ 5.7 model did not converge - check RQ 5.7 logs before proceeding", quit immediately
- If slopes missing: Raise error "RQ 5.7 model missing random slopes - refit model with random slopes enabled", quit immediately
- Log failure to logs/step00_load_data.log
- g_debug invoked to diagnose dependency or model structure issues

---

#### Step 1: Extract Variance Components

**Analysis Tool:** (determined by rq_tools - likely custom variance extraction from statsmodels LMM)
**Validation Tool:** (determined by rq_tools - likely variance positivity check + bounds validation)

**What Validation Checks (Substance - rq_inspect scope):**
- Output file exists (data/step01_variance_components.csv)
- Expected row count = 5 (var_intercept, var_slope, cov_int_slope, var_residual, cor_int_slope)
- All variance components > 0 (variances must be positive)
- Correlation in [-1, 1] (correlation bounds)
- No NaN values (all components must be estimated)

**Expected Behavior on Validation Failure:**
- If variance <= 0: Raise error "Invalid variance estimate (non-positive) - check RQ 5.7 model fit", quit immediately
- If correlation outside [-1, 1]: Raise error "Invalid correlation (outside bounds) - computation error", quit immediately
- If NaN detected: Raise error "Missing variance component - model estimation issue in RQ 5.7", quit immediately
- Log failure to logs/step01_extract_variance.log
- g_debug invoked to diagnose variance extraction or computation issues

---

#### Step 2: Compute Intraclass Correlation Coefficients (ICC)

**Analysis Tool:** (determined by rq_tools - likely custom ICC computation from variance components)
**Validation Tool:** (determined by rq_tools - likely ICC bounds check + interpretation consistency)

**What Validation Checks (Substance - rq_inspect scope):**
- Output file exists (results/step02_icc_estimates.csv)
- Expected row count = 3 (ICC_intercept, ICC_slope_simple, ICC_slope_conditional_day6)
- All ICC values in [0, 1] (proportion by definition)
- interpretation column matches value (>0.40 = substantial, 0.20-0.40 = moderate, <0.20 = low)
- No NaN values (all ICC must be computed)

**Expected Behavior on Validation Failure:**
- If ICC outside [0, 1]: Raise error "Invalid ICC (outside bounds) - check variance estimates from Step 1", quit immediately
- If interpretation mismatch: Raise error "Interpretation inconsistent with ICC value - logic error", quit immediately
- If NaN detected: Raise error "Missing ICC - computation error", quit immediately
- Log failure to logs/step02_compute_icc.log
- g_debug invoked to diagnose ICC computation or interpretation logic issues

---

#### Step 3: Extract Individual Random Effects and Test Correlation

**Analysis Tool:** (determined by rq_tools - likely custom random effects extraction + correlation test)
**Validation Tool:** (determined by rq_tools - likely Decision D068 compliance check + correlation bounds validation)

**What Validation Checks (Substance - rq_inspect scope):**
- Output files exist (data/step03_random_effects.csv, results/step03_slope_descriptives.csv, results/step03_intercept_slope_correlation.csv)
- Random effects: Expected rows ~ 100 (one per participant), 5 columns
- Slope descriptives: Expected rows = 7 (mean, SD, min, max, Q1, Q2, Q3)
- Correlation: Expected rows = 1, columns include correlation_r, p_uncorrected, p_bonferroni, interpretation
- Decision D068 compliance: BOTH p_uncorrected AND p_bonferroni present
- Correlation r in [-1, 1], p-values in [0, 1]
- No NaN values in random effects (all participants must have estimates)

**Expected Behavior on Validation Failure:**
- If N != 100: Raise error "Missing random effects for some participants - check RQ 5.7 model", quit immediately
- If only one p-value: Raise error "Decision D068 violation - must report BOTH uncorrected and Bonferroni p-values", quit immediately
- If correlation outside [-1, 1]: Raise error "Invalid correlation - computation error", quit immediately
- If NaN detected: Raise error "NaN random effects - model estimation issue in RQ 5.7", quit immediately
- Log failure to logs/step03_extract_random_effects.log
- g_debug invoked to diagnose extraction, correlation, or Decision D068 compliance issues

---

#### Step 4: Visualize Random Slopes Distribution

**Analysis Tool:** (determined by rq_tools - likely matplotlib histogram + Q-Q plot generation)
**Validation Tool:** (determined by rq_tools - likely plot file existence + size check)

**What Validation Checks (Substance - rq_inspect scope):**
- Output files exist (plots/step04_random_slopes_histogram.png, plots/step04_random_slopes_qqplot.png)
- File sizes reasonable (10-200 KB for PNG images)
- Files not corrupted (can be opened as valid images)

**Expected Behavior on Validation Failure:**
- If plot missing: Raise error "Plot generation failed - check plotting library installation", quit immediately
- If file size = 0: Raise error "Empty plot file - plotting code error", quit immediately
- If corrupted: Raise error "Corrupted image file - plotting issue", quit immediately
- Log failure to logs/step04_visualize_slopes.log
- g_debug invoked to diagnose plotting library or code issues

---

## Summary

**Total Steps:** 5 (Step 0: data loading + Steps 1-4: variance extraction, ICC computation, random effects extraction, visualization)
**Estimated Runtime:** 10-15 minutes (no model fitting, only extraction and computation)
**Cross-RQ Dependencies:** RQ 5.7 (must complete all 5 steps and save LMM model object)
**Primary Outputs:**
  - data/step01_variance_components.csv (variance decomposition)
  - results/step02_icc_estimates.csv (ICC for intercepts and slopes)
  - data/step03_random_effects.csv (individual random effects for RQ 5.14 clustering)
  - results/step03_intercept_slope_correlation.csv (baseline-forgetting correlation)
  - plots/step04_random_slopes_histogram.png (distribution visualization)
  - plots/step04_random_slopes_qqplot.png (normality check)
**Validation Coverage:** 100% (all 5 steps have validation requirements with substance criteria)

**Key Findings Expected:**
- ICC for intercepts: Likely high (0.60-0.70) indicating stable baseline ability
- ICC for slopes: Hypothesis >0.40 (substantial individual differences in forgetting rate)
- Intercept-slope correlation: Hypothesis r = -0.20 to -0.40 (high baseline -> slower forgetting)
- Random slopes distribution: Approximately normal (validates LMM assumptions)

**Theoretical Implications:**
- High slope ICC -> Forgetting rate is trait-like (justifies RQ 5.14 clustering analysis)
- Negative intercept-slope correlation -> High performers maintain advantage over time
- Low slope ICC -> Forgetting is mostly noise-driven (individual differences unstable)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts
5. After execution: data/step03_random_effects.csv used by RQ 5.14 (clustering analysis)

---

**Version History:**
- v1.0 (2025-11-26): Initial plan created by rq_planner agent for variance decomposition analysis
