# Analysis Plan for RQ 5.1: Domain-Specific Forgetting Trajectories (What/Where/When)

**Created by:** rq_planner agent
**Date:** 2025-11-21
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This RQ examines domain-specific forgetting trajectories across three episodic memory components (What, Where, When) using IRT-derived theta ability estimates across four test sessions (Days 0, 1, 3, 6). The analysis tests whether object identity (What) is more resilient than spatial (Where) or temporal (When) memory, consistent with dual-process theories predicting differential hippocampal dependence.

**Analysis Pipeline:** IRT (2-pass GRM purification) -> LMM (5 candidate trajectory models with Domain x Time interaction)

**Total Steps:** 8 analysis steps (Step 0: data extraction + Steps 1-7: analysis and visualization)

**Estimated Runtime:** High (120+ minutes total - IRT calibration is computationally intensive)

**Key Decisions Applied:**
- Decision D039: 2-pass IRT purification (|b| > 3.0 OR a < 0.4 excluded)
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni-corrected)
- Decision D069: Dual-scale trajectory plots (theta + probability scales)
- Decision D070: TSVR as time variable (actual hours since encoding, not nominal days)

---

## Analysis Plan

### Step 0: Extract VR Item Data and TSVR

**Dependencies:** None (first step)
**Complexity:** Low (data extraction only, <5 minutes)

**Purpose:** Load data from dfData.csv, extract TQ_* columns matching What/Where/When domain patterns, dichotomize accuracy scores, and prepare wide-format IRT input.

**Input:**

**File:** data/cache/dfData.csv (project-level cached data derived from master.xlsx)

**Required Columns:**
- `UID` (string, participant identifier)
- `TEST` (string, test session: T1, T2, T3, T4)
- `TSVR` (float, Time Since VR in hours)
- `TQ_*` (float, test question accuracy scores for VR items)

**Tag Patterns for Domain Extraction:**
- **What domain:** TQ_* columns matching `*-N-*` pattern (object identity)
- **Where domain:** TQ_* columns matching `*-L-*`, `*-U-*`, `*-D-*` patterns (spatial location - static, pick-up, put-down)
- **When domain:** TQ_* columns matching `*-O-*` pattern (temporal order)

**Expected Data Volume:**
- Rows: ~400 (100 participants x 4 test sessions)
- Columns: ~400+ (UID, TEST, TSVR + TQ_* columns for all VR items)

**Processing:**

1. **Load dfData.csv:** Read CSV file preserving all columns
2. **Select relevant columns:** Keep ['UID', 'TEST', 'TSVR', 'TQ_*']
3. **Dichotomize accuracy:** Transform TQ_* values: `value < 1 -> 0`, `value >= 1 -> 1`
4. **Filter by domain patterns:**
   - What: Extract TQ_* where column name contains `-N-`
   - Where: Extract TQ_* where column name contains `-L-`, `-U-`, or `-D-`
   - When: Extract TQ_* where column name contains `-O-`
5. **Create composite_ID:** Combine UID and TEST (format: `{UID}_{TEST}`)
6. **Pivot to wide format:** One row per composite_ID, one column per item
7. **Save TSVR mapping separately:** composite_ID, TSVR_hours (for Step 4 merge)

**Output:**

**File 1:** data/step00_irt_input.csv
**Format:** CSV, wide format (one row per composite_ID)
**Columns:**
  - `composite_ID` (string, format: {UID}_{TEST}, e.g., "A010_T1")
  - One column per item code (e.g., TQ_RVR-T1-IFR-N-i1CM-...-ANS)
  - Values: {0, 1, NaN} (0=incorrect, 1=correct, NaN=missing/not administered)
**Expected Rows:** ~400 (100 participants x 4 tests)
**Expected Columns:** ~103+ (composite_ID + item columns for What/Where/When domains)

**File 2:** data/step00_tsvr_mapping.csv
**Format:** CSV, long format
**Columns:**
  - `composite_ID` (string, matches step00_irt_input.csv)
  - `TSVR_hours` (float, actual hours since encoding)
  - `test` (string, T1/T2/T3/T4 for joining)
**Expected Rows:** ~400 (one per composite_ID)

**Validation Requirement:**

Validation tools MUST be used after data extraction tool execution. Specific validation tools will be determined by rq_tools based on extraction type.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_irt_input.csv: 400 rows x 103+ columns (composite_ID + items)
- data/step00_tsvr_mapping.csv: 400 rows x 3 columns (composite_ID, TSVR_hours, test)
- Data types: composite_ID (object), items (float64), TSVR_hours (float64), test (object)

*Value Ranges:*
- Item scores in {0, 1, NaN} (dichotomized accuracy)
- TSVR_hours in [0, 200] hours (reasonable upper bound: ~8 days maximum delay)
- test in {T1, T2, T3, T4}

*Data Quality:*
- All 100 participants present (400 composite_IDs total: 100 x 4 tests)
- No duplicate composite_IDs (each UID_test combination unique)
- NaN acceptable in item columns (not all items administered to all participants)
- No NaN in composite_ID, TSVR_hours, test columns (required fields)

*Log Validation:*
- Required pattern: "Data extraction complete: 400 rows, 103+ columns"
- Required pattern: "TSVR mapping created: 400 rows"
- Forbidden patterns: "ERROR", "Duplicate composite_ID detected"
- Acceptable warnings: "Some items have >50% missing data" (expected for temporal domain)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 400 rows, found 387")
- Log failure to logs/step00_extract_vr_data.log
- Quit script immediately (do NOT proceed to Step 1)

---

### Step 1: IRT Calibration Pass 1 (All Items)

**Dependencies:** Step 0 (requires step00_irt_input.csv)
**Complexity:** High (60-90 minutes - variational inference on 400 observations x 100+ items x 3 dimensions)

**Purpose:** Calibrate multidimensional IRT model (Graded Response Model with correlated factors) on ALL items to estimate initial item parameters. This is the first pass of 2-pass purification (Decision D039).

**Input:**

**File:** data/step00_irt_input.csv
**Source:** Generated by Step 0
**Format:** Wide format (composite_ID x items)
**Expected Rows:** ~400 (100 participants x 4 tests)
**Expected Columns:** ~103+ (composite_ID + items)

**Factor Assignments:**
- Dimension 1 (What): All items matching `*-N-*` pattern
- Dimension 2 (Where): All items matching `*-L-*`, `*-U-*`, `*-D-*` patterns
- Dimension 3 (When): All items matching `*-O-*` pattern

**Processing:**

**IRT Model Specification:**
- **Model:** Graded Response Model (GRM)
- **Response Categories:** 2 (binary: 0=incorrect, 1=correct)
- **Dimensions:** 3 (What, Where, When)
- **Factor Correlation:** Correlated factors (estimate inter-dimensional correlations)
- **Estimation:** Variational inference (deepirtools backend)

**Method:** Call IRT calibration tool with:
1. Input data: step00_irt_input.csv (wide format)
2. Factor structure: 3 correlated dimensions
3. Response categories: 2 (dichotomous)
4. Convergence criteria: Default deepirtools settings

**Output:**

**File 1:** logs/step01_pass1_item_params.csv
**Format:** CSV, one row per item
**Columns:**
  - `item_code` (string, original TQ_* column name)
  - `dimension` (string, What/Where/When)
  - `a` (float, discrimination parameter, typically 0.0 to 4.0)
  - `b` (float, difficulty parameter, unrestricted range)
**Expected Rows:** ~103+ items (all items from input data)

**File 2:** logs/step01_pass1_theta.csv
**Format:** CSV, one row per composite_ID
**Columns:**
  - `composite_ID` (string)
  - `theta_What` (float, ability estimate for What dimension)
  - `theta_Where` (float, ability estimate for Where dimension)
  - `theta_When` (float, ability estimate for When dimension)
  - `se_What` (float, standard error for What theta)
  - `se_Where` (float, standard error for Where theta)
  - `se_When` (float, standard error for When theta)
**Expected Rows:** ~400 (one per composite_ID)

**Note:** Pass 1 theta estimates are diagnostic only (saved to logs/ folder). Final theta estimates from Pass 2 (Step 3) will be used for analysis.

**Validation Requirement:**

Validation tools MUST be used after IRT calibration tool execution. Specific validation tools will be determined by rq_tools based on IRT calibration requirements (convergence checks, parameter bounds, dimensionality validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- logs/step01_pass1_item_params.csv: 103+ rows x 4 columns (item_code, dimension, a, b)
- logs/step01_pass1_theta.csv: 400 rows x 7 columns (composite_ID, 3 theta, 3 SE)
- Data types: item_code (object), dimension (object), a (float64), b (float64), theta (float64), SE (float64)

*Value Ranges:*
- Discrimination (a) in [0.0, 10.0] (above 10.0 suggests estimation error)
- Difficulty (b) unrestricted (temporal items may have |b| > 3.0 - that's why we purify)
- Theta in [-4.0, 4.0] (extreme values acceptable if SE high)
- SE in [0.1, 2.0] (below 0.1 unrealistically precise, above 2.0 unreliable)

*Data Quality:*
- All 103+ items present in item_params (no missing items)
- All 400 composite_IDs present in theta (no participant loss)
- No NaN in a, b, theta, SE columns (model MUST estimate for all)
- dimension in {What, Where, When} (no other values)

*Log Validation:*
- Required pattern: "IRT calibration converged: True"
- Required pattern: "ELBO improvement achieved"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "NaN parameters detected"
- Acceptable warnings: "Some items have low discrimination (a < 0.4)" (expected - that's what purification addresses)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Model did not converge after 5000 iterations")
- Log failure to logs/step01_irt_calibration_pass1.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose (common causes: insufficient data, model misspecification, numerical instability)

---

### Step 2: Purify Items (2-Pass Methodology)

**Dependencies:** Step 1 (requires logs/step01_pass1_item_params.csv)
**Complexity:** Low (<5 minutes - filtering based on thresholds)

**Purpose:** Apply Decision D039 purification thresholds to exclude psychometrically problematic items. Items with extreme difficulty (|b| > 3.0) or low discrimination (a < 0.4) are removed to improve measurement quality in Pass 2.

**Input:**

**File:** logs/step01_pass1_item_params.csv
**Source:** Generated by Step 1 (Pass 1 calibration)
**Format:** CSV with item parameters
**Columns:** item_code, dimension, a, b
**Expected Rows:** ~103+ items

**Purification Thresholds (Decision D039):**
- **Maximum absolute difficulty:** |b| <= 3.0 (items with |b| > 3.0 excluded)
- **Minimum discrimination:** a >= 0.4 (items with a < 0.4 excluded)

**Exclusion Logic:** Item RETAINED if (|b| <= 3.0) AND (a >= 0.4). Item EXCLUDED otherwise.

**Processing:**

**Method:** Call item purification tool with:
1. Input: step01_pass1_item_params.csv
2. Thresholds: max_abs_difficulty=3.0, min_discrimination=0.4
3. Apply within-dimension filtering (retain at least 10 items per dimension)

**Steps:**
1. Load Pass 1 item parameters
2. For each item, check: (|b| <= 3.0) AND (a >= 0.4)
3. Mark items failing either criterion for exclusion
4. Ensure at least 10 items retained per dimension (if dimension drops below 10, flag error)
5. Save purified item list

**Expected Retention Rate:** 40-60% per concept notes (temporal items particularly difficult, high exclusion rate expected)

**Output:**

**File 1:** data/step02_purified_items.csv
**Format:** CSV, one row per RETAINED item
**Columns:**
  - `item_code` (string, TQ_* column name)
  - `dimension` (string, What/Where/When)
  - `a` (float, discrimination from Pass 1)
  - `b` (float, difficulty from Pass 1)
  - `retained` (bool, always True in this file)
**Expected Rows:** 40-60 items (40-60% retention of ~103 input items)

**File 2:** logs/step02_purification_report.txt
**Format:** Plain text report
**Content:**
  - Total items evaluated: 103+
  - Items retained: XX (XX%)
  - Items excluded: XX (XX%)
  - Exclusion reasons breakdown:
    - Extreme difficulty (|b| > 3.0): XX items
    - Low discrimination (a < 0.4): XX items
    - Both criteria violated: XX items
  - Retention by dimension:
    - What: XX/YY retained (ZZ%)
    - Where: XX/YY retained (ZZ%)
    - When: XX/YY retained (ZZ%)

**Validation Requirement:**

Validation tools MUST be used after item purification tool execution. Specific validation tools will be determined by rq_tools based on purification requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_purified_items.csv: 40-60 rows x 5 columns (item_code, dimension, a, b, retained)
- logs/step02_purification_report.txt: text file with exclusion statistics
- Data types: item_code (object), dimension (object), a (float64), b (float64), retained (bool)

*Value Ranges:*
- Retained items: a >= 0.4 (all items must meet threshold)
- Retained items: |b| <= 3.0 (all items must meet threshold)
- Retention rate: 30-70% (below 30% or above 70% suggests threshold issue)

*Data Quality:*
- At least 10 items retained per dimension (minimum for stable calibration)
- No NaN values in purified_items.csv
- No duplicate item_codes
- All retained items satisfy BOTH thresholds

*Log Validation:*
- Required pattern: "Purification complete: XX items retained, YY items excluded"
- Required pattern: "All dimensions have >= 10 items (minimum threshold met)"
- Forbidden patterns: "ERROR", "Dimension eliminated (< 10 items)", "No items retained"
- Acceptable warnings: "When dimension: low retention (35%)" (temporal items expected to be difficult)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "When dimension only 8 items retained, minimum 10 required")
- Log failure to logs/step02_purify_items.log
- Quit script immediately (do NOT proceed to Step 3)
- If dimension eliminated: Report to master, may require threshold adjustment or dimension exclusion from analysis

---

### Step 3: IRT Calibration Pass 2 (Purified Items)

**Dependencies:** Steps 0, 2 (requires step00_irt_input.csv and step02_purified_items.csv)
**Complexity:** High (60-90 minutes - re-calibration on purified item set)

**Purpose:** Re-calibrate IRT model using only psychometrically sound items (retained from Step 2). This produces final theta estimates and item parameters for downstream LMM analysis.

**Input:**

**File 1:** data/step00_irt_input.csv (original wide-format data)
**File 2:** data/step02_purified_items.csv (list of retained items)

**Processing:**

**Method:**
1. Load step00_irt_input.csv (all items)
2. Load step02_purified_items.csv (purified item list)
3. Filter step00_irt_input.csv to include ONLY columns in purified item list
4. Call IRT calibration tool with same settings as Step 1:
   - Model: GRM, 2 categories, 3 correlated dimensions
   - Factor assignments: What/Where/When based on item codes
   - Estimation: Variational inference

**Expected Improvement:** Pass 2 should show better model fit (lower RMSEA, higher reliability) compared to Pass 1 due to exclusion of misfitting items.

**Output:**

**File 1:** data/step03_item_parameters.csv (FINAL item parameters)
**Format:** CSV, one row per RETAINED item
**Columns:**
  - `item_code` (string, TQ_* column name)
  - `dimension` (string, What/Where/When)
  - `a` (float, discrimination parameter)
  - `b` (float, difficulty parameter)
**Expected Rows:** 40-60 items (same as step02_purified_items.csv)

**File 2:** data/step03_theta_scores.csv (FINAL theta estimates)
**Format:** CSV, one row per composite_ID
**Columns:**
  - `composite_ID` (string, {UID}_{TEST})
  - `theta_What` (float, ability estimate for What dimension)
  - `theta_Where` (float, ability estimate for Where dimension)
  - `theta_When` (float, ability estimate for When dimension)
  - `se_What` (float, standard error for What theta)
  - `se_Where` (float, standard error for Where theta)
  - `se_When` (float, standard error for When theta)
**Expected Rows:** ~400 (one per composite_ID)

**Note:** These are the FINAL theta estimates used for LMM analysis (not diagnostic like Pass 1).

**Validation Requirement:**

Validation tools MUST be used after IRT calibration tool execution. Specific validation tools will be determined by rq_tools (same as Step 1, but with comparison to Pass 1 fit indices).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_item_parameters.csv: 40-60 rows x 4 columns (item_code, dimension, a, b)
- data/step03_theta_scores.csv: 400 rows x 7 columns (composite_ID, 3 theta, 3 SE)
- Data types: Same as Step 1 output

*Value Ranges:*
- Discrimination (a) in [0.4, 10.0] (should all meet purification threshold)
- Difficulty (b) in [-3.0, 3.0] (should all meet purification threshold)
- Theta in [-3.0, 3.0] (typical IRT ability range - outliers reduced vs Pass 1)
- SE in [0.1, 1.5] (should be lower than Pass 1 due to better item quality)

*Data Quality:*
- Item count matches step02_purified_items.csv (no item loss during recalibration)
- All 400 composite_IDs present (no participant loss)
- No NaN in a, b, theta, SE columns
- Pass 2 fit better than Pass 1 (check model comparison metrics)

*Log Validation:*
- Required pattern: "IRT calibration converged: True"
- Required pattern: "Pass 2 fit improved vs Pass 1" (or comparison metrics)
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "Pass 2 fit WORSE than Pass 1"
- Acceptable warnings: None expected (purified items should calibrate cleanly)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step03_irt_calibration_pass2.log
- Quit script immediately
- If Pass 2 fit worse than Pass 1: Report to master (suggests purification threshold issue)

---

### Step 4: Merge Theta Scores with TSVR Time Variable

**Dependencies:** Steps 0, 3 (requires step00_tsvr_mapping.csv and step03_theta_scores.csv)
**Complexity:** Low (<5 minutes - data merging only)

**Purpose:** Merge final theta estimates with TSVR (Time Since VR) time variable per Decision D070. TSVR represents actual hours since encoding (not nominal days 0, 1, 3, 6), enabling precise temporal modeling in LMM.

**Input:**

**File 1:** data/step03_theta_scores.csv
**Columns:** composite_ID, theta_What, theta_Where, theta_When, se_What, se_Where, se_When
**Expected Rows:** ~400

**File 2:** data/step00_tsvr_mapping.csv
**Columns:** composite_ID, TSVR_hours, test
**Expected Rows:** ~400

**Processing:**

**Method:**
1. Load step03_theta_scores.csv
2. Load step00_tsvr_mapping.csv
3. Merge on composite_ID (left join - keep all theta scores, add TSVR)
4. Validate: No missing TSVR_hours after merge (all composite_IDs must match)
5. Add derived time variables for LMM candidate models:
   - `TSVR_hours` (already present from mapping)
   - `TSVR_hours_sq` (TSVR_hours squared for quadratic models)
   - `log_TSVR_hours` (log(TSVR_hours + 1) for log models - add 1 to handle TSVR=0)

**Output:**

**File:** data/step04_lmm_input.csv
**Format:** CSV, one row per composite_ID (wide format)
**Columns:**
  - `composite_ID` (string)
  - `theta_What` (float)
  - `theta_Where` (float)
  - `theta_When` (float)
  - `se_What` (float)
  - `se_Where` (float)
  - `se_When` (float)
  - `TSVR_hours` (float, actual hours since encoding)
  - `TSVR_hours_sq` (float, TSVR_hours^2)
  - `log_TSVR_hours` (float, log(TSVR_hours + 1))
  - `test` (string, T1/T2/T3/T4)
**Expected Rows:** ~400 (one per composite_ID)

**Validation Requirement:**

Validation tools MUST be used after merge tool execution. Specific validation tools will be determined by rq_tools based on merge requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_lmm_input.csv: 400 rows x 11 columns
- Data types: composite_ID (object), theta (float64), SE (float64), TSVR (float64), test (object)

*Value Ranges:*
- TSVR_hours in [0, 200] (reasonable upper bound)
- TSVR_hours_sq in [0, 40000] (200^2)
- log_TSVR_hours in [0, 5.3] (log(200+1))
- Theta in [-3.0, 3.0]
- SE in [0.1, 1.5]

*Data Quality:*
- All 400 rows present (no data loss during merge)
- No NaN in TSVR_hours (ALL composite_IDs must have time variable)
- No NaN in theta, SE columns
- No duplicate composite_IDs

*Log Validation:*
- Required pattern: "Merge complete: 400 rows, all composite_IDs matched"
- Required pattern: "TSVR variables created: TSVR_hours, TSVR_hours_sq, log_TSVR_hours"
- Forbidden patterns: "ERROR", "Missing TSVR for composite_ID", "Merge produced NaN values"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "15 composite_IDs missing TSVR_hours")
- Log failure to logs/step04_merge_theta_tsvr.log
- Quit script immediately

---

### Step 5: Fit LMM Trajectory Models (5 Candidate Models)

**Dependencies:** Step 4 (requires step04_lmm_input.csv)
**Complexity:** Medium (30-60 minutes - 5 model fits with random effects estimation)

**Purpose:** Fit 5 candidate Linear Mixed Models with Domain x Time interactions to determine best-fitting trajectory functional form. Models compare linear, quadratic, logarithmic, and combined time transformations.

**Input:**

**File:** data/step04_lmm_input.csv
**Format:** Wide format (one row per composite_ID)
**Expected Rows:** ~400

**Data Transformation:**
1. Reshape wide to long: One row per observation (composite_ID x dimension)
2. Create domain factor: What/Where/When (from theta_What, theta_Where, theta_When columns)
3. Result: ~1200 rows (400 composite_IDs x 3 dimensions)

**Long Format Columns:**
- `composite_ID` (for random effects grouping)
- `UID` (parsed from composite_ID, participant identifier)
- `theta` (ability estimate, DV)
- `domain` (factor: What/Where/When)
- `TSVR_hours` (time variable)
- `TSVR_hours_sq` (time squared)
- `log_TSVR_hours` (log time)

**Processing:**

**5 Candidate Models (Domain x Time interaction in all):**

**Reference Level:** What domain (Treatment coding - Where and When compared to What)

1. **Linear:** `theta ~ domain * TSVR_hours + (1 + TSVR_hours | UID)`
2. **Quadratic:** `theta ~ domain * (TSVR_hours + TSVR_hours_sq) + (1 + TSVR_hours | UID)`
3. **Logarithmic:** `theta ~ domain * log_TSVR_hours + (1 + log_TSVR_hours | UID)`
4. **Linear + Log:** `theta ~ domain * (TSVR_hours + log_TSVR_hours) + (1 + TSVR_hours | UID)`
5. **Quadratic + Log:** `theta ~ domain * (TSVR_hours + TSVR_hours_sq + log_TSVR_hours) + (1 + TSVR_hours | UID)`

**Random Effects:** Random intercepts and slopes per participant (UID)

**Estimation:** REML=False (use ML estimation for AIC comparison)

**Model Selection:**
1. Fit all 5 models
2. Compute AIC for each
3. Calculate Akaike weights
4. Select best model (lowest AIC)
5. Report comparison table

**Output:**

**File 1:** results/step05_lmm_model_summary.txt
**Format:** Plain text summary
**Content:**
  - Best model formula
  - Fixed effects table (coefficient, SE, z, p-value, 95% CI)
  - Random effects variances
  - ICC (intraclass correlation)
  - Model fit indices (AIC, BIC, log-likelihood)

**File 2:** results/step05_model_comparison.csv
**Format:** CSV, one row per candidate model
**Columns:**
  - `model_name` (string: Linear, Quadratic, Log, Linear+Log, Quadratic+Log)
  - `AIC` (float)
  - `delta_AIC` (float, difference from best model)
  - `AIC_weight` (float, Akaike weight)
  - `formula` (string, model formula)
**Expected Rows:** 5 (one per candidate model)

**File 3:** data/step05_best_model_predictions.csv
**Format:** CSV, one row per observation
**Columns:**
  - `composite_ID` (string)
  - `domain` (string)
  - `TSVR_hours` (float)
  - `theta_observed` (float, actual theta)
  - `theta_predicted` (float, fitted value from best model)
  - `residual` (float, observed - predicted)
**Expected Rows:** ~1200 (400 composite_IDs x 3 dimensions)

**Validation Requirement:**

Validation tools MUST be used after LMM fitting tool execution. Specific validation tools will be determined by rq_tools based on LMM requirements (convergence, residual normality, homoscedasticity).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step05_lmm_model_summary.txt: text file with model summary
- results/step05_model_comparison.csv: 5 rows x 5 columns
- data/step05_best_model_predictions.csv: 1200 rows x 6 columns
- Data types: AIC (float64), delta_AIC (float64), AIC_weight (float64), theta (float64), residual (float64)

*Value Ranges:*
- AIC: positive values, reasonable range (lower is better)
- delta_AIC in [0, infinity] (best model has delta_AIC = 0)
- AIC_weight in [0, 1], sum to 1.0 across all models
- theta_observed in [-3.0, 3.0]
- theta_predicted in [-3.0, 3.0]
- residual in [-4.0, 4.0] (larger residuals acceptable if rare)

*Data Quality:*
- All 5 models converged (no convergence failures)
- All 1200 observations have predictions (no missing fitted values)
- No NaN in fixed effects, random effects, or predictions
- Residuals approximately normal (Shapiro-Wilk or QQ plot check)

*Log Validation:*
- Required pattern: "All 5 models converged successfully"
- Required pattern: "Best model selected: [model_name] (AIC = [value])"
- Forbidden patterns: "ERROR", "Model convergence failed", "Singular matrix"
- Acceptable warnings: "Random effects variance near boundary" (can occur with small random slopes)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Quadratic model failed to converge")
- Log failure to logs/step05_fit_lmm.log
- Quit script immediately
- g_debug invoked to diagnose (common causes: random effects overspecification, numerical instability)

---

### Step 6: Post-Hoc Contrasts and Effect Sizes

**Dependencies:** Step 5 (requires best LMM model from step05_lmm_model_summary.txt)
**Complexity:** Low (<5 minutes - contrast computation from fitted model)

**Purpose:** Compute post-hoc pairwise contrasts testing differential forgetting slopes across domains (Where-What, When-What). Apply Decision D068 dual p-value reporting (uncorrected + Bonferroni-corrected).

**Input:**

**File:** Best model object from Step 5 (MixedLMResults)

**Contrasts to Test:**
1. **Where vs What:** Test Domain x Time interaction coefficient for Where
2. **When vs What:** Test Domain x Time interaction coefficient for When

**Bonferroni Correction:** ± = 0.05 / 2 = 0.025 (two pairwise tests)

**Processing:**

**Method:**
1. Extract Domain x Time interaction terms from best model fixed effects
2. Compute pairwise contrasts (Where-What, When-What)
3. Report BOTH:
   - Uncorrected p-values (± = 0.05)
   - Bonferroni-corrected p-values (± = 0.025)
4. Compute effect sizes:
   - Cohen's d for domain differences at each timepoint (Days 0, 1, 3, 6)
   - Partial ·² for fixed effects

**Output:**

**File 1:** results/step06_post_hoc_contrasts.csv
**Format:** CSV, one row per contrast
**Columns:**
  - `contrast` (string: "Where-What", "When-What")
  - `estimate` (float, difference in slopes)
  - `SE` (float, standard error)
  - `z` (float, z-statistic)
  - `p_uncorrected` (float, p-value without correction)
  - `p_bonferroni` (float, p-value with Bonferroni correction)
  - `CI_lower` (float, 95% CI lower bound)
  - `CI_upper` (float, 95% CI upper bound)
**Expected Rows:** 2 (Where-What, When-What)

**File 2:** results/step06_effect_sizes.csv
**Format:** CSV, one row per domain comparison x timepoint
**Columns:**
  - `contrast` (string: "Where-What", "When-What")
  - `timepoint` (string: Day0, Day1, Day3, Day6)
  - `cohens_d` (float, standardized mean difference)
  - `cohens_d_CI_lower` (float, 95% CI)
  - `cohens_d_CI_upper` (float, 95% CI)
**Expected Rows:** 8 (2 contrasts x 4 timepoints)

**Validation Requirement:**

Validation tools MUST be used after post-hoc contrast tool execution. Specific validation tools will be determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step06_post_hoc_contrasts.csv: 2 rows x 8 columns
- results/step06_effect_sizes.csv: 8 rows x 5 columns
- Data types: estimate (float64), SE (float64), z (float64), p (float64), CI (float64), cohens_d (float64)

*Value Ranges:*
- estimate (slope difference) in [-2.0, 2.0] (reasonable effect size range)
- SE in [0.01, 0.5] (depends on sample size and variance)
- z in [-10, 10] (extreme z values possible if SE very small)
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1], p_bonferroni >= p_uncorrected (correction increases p-value)
- cohens_d in [-3.0, 3.0] (extreme effect sizes rare but possible)

*Data Quality:*
- All 2 contrasts present
- All 8 effect size rows present (2 contrasts x 4 timepoints)
- No NaN values (all contrasts computable)
- p_bonferroni = min(p_uncorrected * 2, 1.0) (correct Bonferroni formula)

*Log Validation:*
- Required pattern: "Post-hoc contrasts complete: 2 comparisons computed"
- Required pattern: "Bonferroni correction applied: ± = 0.025 (2 tests)"
- Forbidden patterns: "ERROR", "Contrast computation failed"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step06_compute_post_hoc_contrasts.log
- Quit script immediately

---

### Step 7: Prepare Trajectory Plot Data (Dual-Scale per Decision D069)

**Dependencies:** Steps 3, 4, 5 (requires theta scores, TSVR, and LMM predictions)
**Complexity:** Low (<5 minutes - data aggregation for plotting)

**Purpose:** Create plot source CSVs for trajectory visualization per Option B architecture (Decision D069 requires BOTH theta-scale AND probability-scale plots). This step aggregates analysis outputs into plot-ready format.

**NOTE:** This is an ANALYSIS step (executed during Step 14 CODE EXECUTION LOOP), NOT a plotting step. rq_plots (Step 18) will READ these CSVs to generate plots.

**Input:**

**File 1:** data/step03_theta_scores.csv (theta estimates per composite_ID)
**File 2:** data/step04_lmm_input.csv (theta + TSVR merged)
**File 3:** data/step05_best_model_predictions.csv (fitted values from LMM)
**File 4:** data/step03_item_parameters.csv (for theta->probability conversion)

**Processing:**

**Method:**
1. **Aggregate observed data:**
   - Group step04_lmm_input.csv by domain + TSVR_hours
   - Compute mean theta, 95% CI per domain per timepoint
   - Result: Observed trajectory data

2. **Aggregate model predictions:**
   - Group step05_best_model_predictions.csv by domain + TSVR_hours
   - Compute mean predicted theta per domain per timepoint
   - Result: Fitted trajectory data

3. **Merge observed + fitted:**
   - Join on domain + TSVR_hours
   - Create unified plot source CSV with both observed and fitted values

4. **Convert theta to probability (Decision D069):**
   - Use mean discrimination and difficulty per domain from step03_item_parameters.csv
   - Apply IRT response function: `probability = 1 / (1 + exp(-(a * (theta - b))))`
   - Create probability-scale plot source CSV

**Output:**

**File 1:** plots/step07_trajectory_theta_data.csv (theta scale)
**Format:** CSV, one row per domain x timepoint combination
**Columns:**
  - `domain` (string: What, Where, When)
  - `TSVR_hours` (float: actual time values)
  - `theta_observed` (float: mean observed theta)
  - `theta_predicted` (float: mean fitted theta from LMM)
  - `CI_lower` (float: 95% CI lower bound for observed)
  - `CI_upper` (float: 95% CI upper bound for observed)
  - `N` (int: number of observations per point)
**Expected Rows:** 12-20 (3 domains x 4-6 unique TSVR timepoints, depending on actual data distribution)

**File 2:** plots/step07_trajectory_probability_data.csv (probability scale)
**Format:** CSV, same structure as File 1 but with probability-transformed values
**Columns:**
  - `domain` (string: What, Where, When)
  - `TSVR_hours` (float)
  - `prob_observed` (float: theta_observed transformed to probability)
  - `prob_predicted` (float: theta_predicted transformed to probability)
  - `CI_lower` (float: probability scale)
  - `CI_upper` (float: probability scale)
  - `N` (int)
**Expected Rows:** 12-20 (same as theta scale)

**Validation Requirement:**

Validation tools MUST be used after plot data preparation tool execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- plots/step07_trajectory_theta_data.csv: 12-20 rows x 7 columns
- plots/step07_trajectory_probability_data.csv: 12-20 rows x 7 columns
- Data types: domain (object), TSVR_hours (float64), theta (float64), prob (float64), CI (float64), N (int64)

*Value Ranges:*
- TSVR_hours in [0, 200]
- theta_observed, theta_predicted in [-3.0, 3.0]
- prob_observed, prob_predicted in [0.0, 1.0]
- CI_lower < CI_upper for all rows
- N >= 10 per timepoint (sufficient observations for stable means)

*Data Quality:*
- All 3 domains present (What, Where, When)
- At least 4 timepoints represented (nominal Days 0, 1, 3, 6)
- No NaN in theta or probability columns
- No duplicate domain x TSVR combinations
- Distribution check: CI_upper > CI_lower for all rows

*Log Validation:*
- Required pattern: "Plot data preparation complete: 2 files created (theta + probability scales)"
- Required pattern: "All domains represented: What, Where, When"
- Required pattern: "Theta->probability conversion successful"
- Forbidden patterns: "ERROR", "NaN values detected", "Missing domain", "Probability outside [0,1]"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step07_prepare_trajectory_plot_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- g_debug invoked to diagnose

**Plot Description (for rq_plots agent):**
- **Plot Type:** Trajectory plot with confidence bands
- **X-axis:** TSVR_hours (actual time since encoding)
- **Y-axis (theta scale):** Theta ability (-3 to +3)
- **Y-axis (probability scale):** Probability correct (0 to 1)
- **Groups:** 3 lines (What, Where, When domains)
- **Data points:** Observed means with 95% CI error bars
- **Lines:** Fitted trajectories from best LMM model
- **Plotting function:** Trajectory plot (rq_plots maps to plot_trajectory for theta, plot_trajectory_probability for probability)

---

## Expected Data Formats

### Composite ID Structure

**Format:** `{UID}_{TEST}`

**Example:** `A010_T1` (Participant A010, Test 1)

**Components:**
- UID: Participant identifier (A### format)
- TEST: Test session (T1, T2, T3, T4)

**Usage:** Primary key for merging theta scores with TSVR and LMM predictions. Parsed to extract UID for random effects grouping.

---

### Wide to Long Transformation (Step 5)

**Input Format (Step 4 output):**
- File: data/step04_lmm_input.csv
- Format: Wide (one row per composite_ID)
- Columns: composite_ID, theta_What, theta_Where, theta_When, se_What, se_Where, se_When, TSVR_hours, TSVR_hours_sq, log_TSVR_hours, test

**Transformation:**
1. Reshape: One row per observation (composite_ID x dimension)
2. Create domain column: Melt theta_What, theta_Where, theta_When into single theta column with domain indicator
3. Add UID column: Parse from composite_ID (extract UID portion before underscore)

**Output Format (LMM input):**
- Format: Long (one row per composite_ID x dimension)
- Columns: composite_ID, UID, theta, se, domain, TSVR_hours, TSVR_hours_sq, log_TSVR_hours, test
- Expected Rows: ~1200 (400 composite_IDs x 3 dimensions)

**Transformation Code Pattern:**
```python
# Melt theta columns
df_long = pd.melt(
    df_wide,
    id_vars=['composite_ID', 'TSVR_hours', 'TSVR_hours_sq', 'log_TSVR_hours', 'test'],
    value_vars=['theta_What', 'theta_Where', 'theta_When'],
    var_name='dimension',
    value_name='theta'
)

# Create domain column (strip "theta_" prefix)
df_long['domain'] = df_long['dimension'].str.replace('theta_', '')

# Parse UID from composite_ID
df_long['UID'] = df_long['composite_ID'].str.split('_').str[0]
```

---

### Column Naming Conventions

Per names.md (RQ 5.1 conventions):

**Identifiers:**
- `composite_ID`: UID_test format (e.g., A010_T1)
- `UID`: Participant identifier (e.g., A010)
- `test`: Test session (T1, T2, T3, T4)

**Time Variables:**
- `TSVR_hours`: Actual hours since encoding (float)
- `TSVR_hours_sq`: TSVR_hours squared (for quadratic models)
- `log_TSVR_hours`: log(TSVR_hours + 1) (for log models)

**IRT Outputs:**
- `theta_<dimension>`: Ability estimate (e.g., theta_What)
- `se_<dimension>`: Standard error (e.g., se_What)
- `a`: Item discrimination
- `b`: Item difficulty

**LMM/Plotting:**
- `domain`: Factor (What, Where, When)
- `CI_lower`: 95% confidence interval lower bound
- `CI_upper`: 95% confidence interval upper bound

---

## Cross-RQ Dependencies

**Dependency Type:** RAW Data Only (No Dependencies)

**This RQ uses:** Only data/cache/dfData.csv (project-level cached data derived from master.xlsx)

**No dependencies on other RQs:** Can be executed independently

**Execution order:** Flexible (first RQ in chapter, no prerequisites)

**Data Sources:**
- dfData.csv: TQ_* columns (VR item accuracy), TSVR (time variable)
- All extraction uses direct column selection from dfData.csv
- No intermediate outputs from other RQs required

**Note:** dfData.csv is a PROJECT-LEVEL cached file, not an RQ-specific output. It is pre-processed from master.xlsx and available to all RQs.

---

## Validation Requirements

### CRITICAL MANDATE

Every analysis step in this plan MUST use validation tools after analysis tool execution.

This is not optional. This is the core architectural principle preventing cascading failures observed in v3.0 (where analysis errors propagated undetected through 5+ downstream steps before discovery).

### Exact Specification Requirement

> **"Validation tools MUST be used after analysis tool execution"**

### Implementation

- **rq_tools (Step 11 workflow)** will read tools_inventory.md validation tools section
- **rq_tools** will specify BOTH analysis tool + validation tool per step in 3_tools.yaml
- **rq_analysis (Step 12 workflow)** will embed validation tool call AFTER analysis tool call in 4_analysis.yaml
- **g_code (Step 14 workflow)** will generate stepN_name.py scripts with validation function calls
- **bash execution (Step 14 workflow)** will run analysis -> validation -> error on validation failure

### Downstream Agent Requirements

- **rq_tools:** MUST specify validation tool for EVERY analysis step (no exceptions)
- **rq_analysis:** MUST embed validation tool call for EVERY analysis step (no exceptions)
- **g_code:** MUST generate code with validation function calls (no exceptions)
- **rq_inspect:** MUST verify validation ran successfully (checks logs/stepN_name.log for validation output)

### Validation Requirements By Step

**Step 0: Extract VR Item Data and TSVR**
- **Analysis Tool:** (determined by rq_tools - likely data extraction function)
- **Validation Tool:** (determined by rq_tools - likely data quality validation)
- **What Validation Checks:**
  - Output files exist (step00_irt_input.csv, step00_tsvr_mapping.csv)
  - Expected row count (~400)
  - Expected column count (~103+)
  - No unexpected NaN patterns (>80% NaN per item suggests extraction error)
  - composite_ID format correct ({UID}_{TEST} pattern)
  - Item scores in {0, 1, NaN} (dichotomized)
  - TSVR_hours in reasonable range [0, 200]

**Step 1: IRT Calibration Pass 1**
- **Analysis Tool:** (determined by rq_tools - likely calibrate_irt or calibrate_grm)
- **Validation Tool:** (determined by rq_tools - likely validate_irt_convergence + validate_irt_parameters)
- **What Validation Checks:**
  - Model converged (ELBO improved, no divergence)
  - Item parameters in valid ranges (a in [0, 10], b unrestricted)
  - No NaN parameters (estimation failure indicator)
  - Expected row counts (103+ items, 400 composite_IDs)
  - Factor structure correct (3 dimensions)

**Step 2: Purify Items**
- **Analysis Tool:** (determined by rq_tools - likely filter_items_by_quality)
- **Validation Tool:** (determined by rq_tools - likely item retention validation)
- **What Validation Checks:**
  - Thresholds applied correctly (|b| <= 3.0, a >= 0.4)
  - Retention rate reasonable (30-70%)
  - At least 10 items retained per dimension (minimum for calibration)
  - Purification report created with exclusion statistics

**Step 3: IRT Calibration Pass 2**
- **Analysis Tool:** (same as Step 1)
- **Validation Tool:** (same as Step 1, plus Pass 1 vs Pass 2 comparison)
- **What Validation Checks:**
  - Same as Step 1, plus:
  - Pass 2 fit improved vs Pass 1 (or equivalent quality)
  - Item count matches purified list (no item loss)
  - Theta SE reduced vs Pass 1 (better precision expected)

**Step 4: Merge Theta Scores with TSVR**
- **Analysis Tool:** (determined by rq_tools - likely pandas merge or custom merge function)
- **Validation Tool:** (determined by rq_tools - likely merge validation)
- **What Validation Checks:**
  - All composite_IDs matched (no missing TSVR)
  - No NaN in merged TSVR_hours
  - Derived time variables created correctly (TSVR_hours_sq, log_TSVR_hours)
  - Expected row count (400)

**Step 5: Fit LMM Trajectory Models**
- **Analysis Tool:** (determined by rq_tools - likely fit_lmm_trajectory_tsvr or run_lmm_analysis)
- **Validation Tool:** (determined by rq_tools - likely validate_lmm_convergence + validate_lmm_residuals)
- **What Validation Checks:**
  - All 5 models converged
  - Residuals normally distributed (Shapiro-Wilk or QQ plot)
  - Homoscedasticity (residuals vs fitted plot)
  - No autocorrelation (Durbin-Watson test)
  - AIC comparison valid (all models fit to same data)

**Step 6: Post-Hoc Contrasts**
- **Analysis Tool:** (determined by rq_tools - likely compute_contrasts_pairwise)
- **Validation Tool:** (determined by rq_tools - likely contrast validation)
- **What Validation Checks:**
  - Both contrasts computed (Where-What, When-What)
  - Bonferroni correction applied correctly (p_bonf = min(p_uncorr * 2, 1.0))
  - Effect sizes in reasonable range
  - No NaN in contrast estimates or p-values

**Step 7: Prepare Trajectory Plot Data**
- **Analysis Tool:** (determined by rq_tools - likely custom aggregation function)
- **Validation Tool:** (determined by rq_tools - likely plot data validation)
- **What Validation Checks:**
  - Both files created (theta + probability scales)
  - All 3 domains present
  - At least 4 timepoints represented
  - Probability values in [0, 1]
  - CI_upper > CI_lower for all rows
  - No NaN in theta or probability columns

**NOTE:** Technical validation (files exist, formats correct, values in bounds) checked by rq_inspect DURING analysis. Scientific plausibility (effect directions, theoretical coherence) checked by rq_results AFTER all analysis complete.

### Expected Behavior on Validation Failure

- **Methodological failure:** Validation tool quits, logs error, master invokes g_debug
- **Substance failure:** rq_inspect quits with detailed report, master investigates

---

## Summary

**Total Steps:** 8 (Step 0: extraction + Steps 1-7: analysis/visualization)

**Estimated Runtime:** High (150-180 minutes total)
- Step 0: <5 min (data extraction)
- Step 1: 60-90 min (IRT Pass 1)
- Step 2: <5 min (purification)
- Step 3: 60-90 min (IRT Pass 2)
- Step 4: <5 min (TSVR merge)
- Step 5: 30-60 min (LMM fitting)
- Step 6: <5 min (post-hoc)
- Step 7: <5 min (plot data prep)

**Cross-RQ Dependencies:** None (RAW data only from dfData.csv)

**Primary Outputs:**
- data/step03_theta_scores.csv (final theta estimates, 3 dimensions)
- data/step03_item_parameters.csv (final item parameters, purified)
- results/step05_lmm_model_summary.txt (best trajectory model)
- results/step06_post_hoc_contrasts.csv (domain comparisons, dual p-values)
- plots/step07_trajectory_theta_data.csv (theta-scale plot source)
- plots/step07_trajectory_probability_data.csv (probability-scale plot source)

**Validation Coverage:** 100% (all 8 steps have validation requirements embedded)

**Decisions Applied:**
- D039: 2-pass IRT purification (Steps 1-3)
- D068: Dual p-value reporting (Step 6)
- D069: Dual-scale trajectory plots (Step 7)
- D070: TSVR time variable (Steps 0, 4, 5)

---

## Next Steps (Workflow)

1. **User reviews and approves this plan** (Step 7 user gate)
2. **Workflow continues to Step 11:** rq_tools reads this plan -> creates 3_tools.yaml
3. **Workflow continues to Step 12:** rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. **Workflow continues to Step 14:** g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-11-21): Initial plan created by rq_planner agent
