# Analysis Plan for RQ 5.3: Do Free Recall, Cued Recall, and Recognition Exhibit Different Forgetting Trajectories?

**Created by:** rq_planner agent
**Date:** 2025-11-24
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This analysis plan specifies the step-by-step workflow to test whether paradigm-specific differences exist in the rate and pattern of episodic forgetting over 6 days. The research question compares three retrieval paradigms: Item Free Recall (IFR), Item Cued Recall (ICR), and Item Recognition (IRE), excluding Room Free Recall (RFR) and Task Cued Recall (TCR) due to response format differences and floor/ceiling effects.

The analysis follows an IRT -> LMM pipeline with 2-pass item purification (Decision D039). Unlike RQ 5.1 which used domain-based factors (What/Where/When), this RQ uses paradigm-based factors (Free Recall/Cued Recall/Recognition). The data derives from RQ 5.1 outputs, but requires fresh IRT calibration with a new Q-matrix that maps items to paradigms instead of domains.

**Pipeline:** IRT -> LMM (with paradigm-based factor structure)
**Steps:** 8 total analysis steps (Step 0 data preparation through Step 7 plot data preparation)
**Estimated Runtime:** High (60-90 minutes for full pipeline due to IRT calibration)

**Key Decisions Applied:**
- Decision D039: 2-pass IRT purification (mandatory for all IRT analyses)
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni for post-hoc contrasts)
- Decision D069: Dual-scale trajectory plots (theta-scale + probability-scale)
- Decision D070: TSVR as time variable (actual hours since encoding, not nominal days)

---

## Analysis Plan

This RQ requires 8 steps:

### Step 0: Filter and Prepare Data for Paradigm-Based IRT

**Dependencies:** None (first step, uses RQ 5.1 data extraction outputs)
**Complexity:** Low (data filtering and Q-matrix creation)

**Input:**

**File 1:** results/ch5/rq1/data/step00_irt_input.csv
**Source:** RQ 5.1 Step 0 output (extracted VR item data)
**Format:** CSV, wide format (composite_ID x item columns)
**Columns:**
- `composite_ID` (string, format: UID_test)
- Item columns matching pattern TQ_* (dichotomized 0/1 values)

**Expected Rows:** 400 (100 participants x 4 tests)

**File 2:** results/ch5/rq1/data/step00_tsvr_mapping.csv
**Source:** RQ 5.1 Step 0 output (TSVR time variable)
**Format:** CSV with columns:
- `composite_ID` (string)
- `TSVR_hours` (float, actual hours since encoding)
- `test` (string, T1/T2/T3/T4)

**Expected Rows:** 400

**Processing:**

1. Load RQ 5.1 IRT input data
2. Filter columns to keep only Item paradigm columns:
   - Include: *IFR-*ANS (Item Free Recall)
   - Include: *ICR-*ANS (Item Cued Recall)
   - Include: *IRE-*ANS (Item Recognition)
   - Exclude: *RFR-* (Room Free Recall - different response format)
   - Exclude: *TCR-* (Task Cued Recall - floor/ceiling effects)
3. Create new Q-matrix with paradigm-based factor structure:
   - free_recall factor: maps to *IFR* columns
   - cued_recall factor: maps to *ICR* columns
   - recognition factor: maps to *IRE* columns
4. Copy TSVR mapping file to local data folder
5. Save filtered IRT input and new Q-matrix

**Output:**

**File 1:** data/step00_irt_input.csv
**Format:** CSV, wide format (composite_ID x filtered item columns)
**Columns:**
- `composite_ID` (string)
- Filtered item columns (IFR, ICR, IRE paradigms only)

**Expected Rows:** 400 (100 participants x 4 tests)
**Expected Columns:** ~103 (composite_ID + approximately 102 item columns after filtering)

**File 2:** data/step00_q_matrix.csv
**Format:** CSV with columns:
- `item_name` (string, item column name)
- `free_recall` (int, 1 if item belongs to IFR, else 0)
- `cued_recall` (int, 1 if item belongs to ICR, else 0)
- `recognition` (int, 1 if item belongs to IRE, else 0)

**Expected Rows:** Number of retained items (approximately 102)

**File 3:** data/step00_tsvr_mapping.csv
**Format:** Copy of RQ 5.1 TSVR mapping
**Expected Rows:** 400

**Validation Requirement:**
Validation tools MUST be used after data preparation tool execution. Specific validation tools will be determined by rq_tools based on data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_irt_input.csv: 400 rows, approximately 103 columns (composite_ID + items)
- data/step00_q_matrix.csv: approximately 102 rows, 4 columns (item_name, free_recall, cued_recall, recognition)
- data/step00_tsvr_mapping.csv: 400 rows, 3 columns

*Value Ranges:*
- Item values in {0, 1, NaN} (dichotomized responses)
- Q-matrix factor columns in {0, 1} (binary loadings)
- TSVR_hours in [0, 200] (typical range for 6-day study)

*Data Quality:*
- All 400 composite_IDs present (no data loss)
- Each item appears in exactly one paradigm factor (row sums of Q-matrix factor columns = 1)
- No NaN in composite_ID column
- Q-matrix item names match IRT input column names

*Log Validation:*
- Required pattern: "Filtered to IFR, ICR, IRE paradigms"
- Required pattern: "Q-matrix created: X items"
- Forbidden patterns: "ERROR", "KeyError", "No items found"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step00_prepare_data.log
- Quit script immediately
- g_debug invoked to diagnose root cause

---

### Step 1: IRT Calibration Pass 1 (All Items)

**Dependencies:** Step 0 (requires filtered IRT input and paradigm Q-matrix)
**Complexity:** High (60+ minutes for multidimensional IRT calibration)

**Input:**

**File 1:** data/step00_irt_input.csv
**Format:** CSV, wide format (composite_ID x item columns)

**File 2:** data/step00_q_matrix.csv
**Format:** CSV with paradigm factor loadings

**Processing:**

1. Load IRT input data and Q-matrix
2. Configure IRT model:
   - Model type: Graded Response Model (GRM) with 2 categories (dichotomous items)
   - Factor structure: Correlated factors (free_recall, cued_recall, recognition)
   - Estimation: IWAVE variational inference
3. Fit IRT model via variational inference
4. Extract item parameters (discrimination a, difficulty b)
5. Extract theta scores per factor for each composite_ID
6. Save Pass 1 outputs to logs folder (diagnostic, not used in final analysis)

**Output:**

**File 1:** logs/step01_pass1_item_params.csv
**Format:** CSV with columns:
- `item_name` (string)
- `dimension` (string: free_recall, cued_recall, or recognition)
- `a` (float, discrimination parameter)
- `b` (float, difficulty parameter)

**Expected Rows:** Number of items (approximately 102)

**File 2:** logs/step01_pass1_theta.csv
**Format:** CSV with columns:
- `composite_ID` (string)
- `theta_free_recall` (float, ability estimate for IFR)
- `theta_cued_recall` (float, ability estimate for ICR)
- `theta_recognition` (float, ability estimate for IRE)
- `se_free_recall` (float, standard error)
- `se_cued_recall` (float, standard error)
- `se_recognition` (float, standard error)

**Expected Rows:** 400

**Validation Requirement:**
Validation tools MUST be used after IRT calibration tool execution. Specific validation tools will be determined by rq_tools based on IRT convergence and parameter quality criteria.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- logs/step01_pass1_item_params.csv: approximately 102 rows, 4 columns
- logs/step01_pass1_theta.csv: 400 rows, 7 columns

*Value Ranges:*
- Discrimination a in [0.1, 10.0] (values outside suggest estimation error)
- Difficulty b in [-6.0, 6.0] (extreme values possible for paradigm items)
- theta values in [-4, 4] (typical IRT ability range)
- Standard errors se in [0.1, 2.0] (above 2.0 = unreliable)

*Data Quality:*
- No NaN in item parameters (indicates estimation failure)
- All 400 composite_IDs present in theta output
- Each item assigned to exactly one dimension

*Log Validation:*
- Required pattern: "Model converged: True"
- Required pattern: "Extracting item parameters"
- Forbidden patterns: "CONVERGENCE FAILED", "ERROR", "NaN detected"
- Acceptable warnings: "Some parameters near boundary" (expected for difficult items)

**Expected Behavior on Validation Failure:**
- Raise error with specific convergence or parameter failure message
- Log failure to logs/step01_irt_calibration_pass1.log
- Quit script immediately
- g_debug invoked to diagnose (common causes: insufficient data, model misspecification)

---

### Step 2: Item Purification

**Dependencies:** Step 1 (requires Pass 1 item parameters)
**Complexity:** Low (filtering based on thresholds)

**Input:**

**File:** logs/step01_pass1_item_params.csv
**Format:** CSV with item parameters from Pass 1
**Required Columns:** item_name, dimension, a, b

**Processing:**

1. Load Pass 1 item parameters
2. Apply Decision D039 purification thresholds:
   - Discrimination threshold: a >= 0.4 (items below = poor discrimination)
   - Difficulty threshold: |b| <= 3.0 (items outside = extreme difficulty)
3. Filter items within each paradigm factor
4. Create list of retained items
5. Document excluded items with reasons
6. Save purification report and purified item list

**Output:**

**File 1:** data/step02_purified_items.csv
**Format:** CSV with columns:
- `item_name` (string)
- `dimension` (string: free_recall, cued_recall, recognition)
- `a` (float, discrimination - all >= 0.4)
- `b` (float, difficulty - all |b| <= 3.0)

**Expected Rows:** 40-80 items (40-80% retention typical for paradigm items)

**File 2:** logs/step02_purification_report.txt
**Format:** Text report listing:
- Total items before purification
- Items excluded for low discrimination (a < 0.4)
- Items excluded for extreme difficulty (|b| > 3.0)
- Items retained per paradigm
- Retention percentage

**Validation Requirement:**
Validation tools MUST be used after item purification tool execution. Specific validation tools will be determined by rq_tools based on purification quality criteria.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_purified_items.csv: 40-80 rows, 4 columns
- logs/step02_purification_report.txt: text file exists

*Value Ranges:*
- All retained items have a >= 0.4
- All retained items have |b| <= 3.0

*Data Quality:*
- At least 10 items retained per paradigm (minimum for IRT estimation)
- No paradigm completely eliminated
- Retention rate between 30-90% (outside = review needed)

*Log Validation:*
- Required pattern: "Purification complete"
- Required pattern: "Items retained: X"
- Required pattern: "free_recall: X items, cued_recall: X items, recognition: X items"
- Forbidden patterns: "ERROR", "0 items retained"

**Expected Behavior on Validation Failure:**
- Raise error if any paradigm has fewer than 10 retained items
- Log failure to logs/step02_purify_items.log
- Quit script immediately
- g_debug invoked to diagnose (may need threshold adjustment)

---

### Step 3: IRT Calibration Pass 2 (Purified Items)

**Dependencies:** Step 2 (requires purified item list)
**Complexity:** High (60+ minutes for multidimensional IRT calibration)

**Input:**

**File 1:** data/step00_irt_input.csv
**Format:** CSV, wide format (original IRT input)

**File 2:** data/step02_purified_items.csv
**Format:** CSV with retained items list

**File 3:** data/step00_q_matrix.csv
**Format:** CSV with paradigm Q-matrix (will be filtered to purified items)

**Processing:**

1. Load original IRT input data
2. Load purified items list
3. Filter IRT input to include only purified items
4. Filter Q-matrix to include only purified items
5. Configure IRT model (same as Pass 1):
   - Model type: GRM with 2 categories
   - Factor structure: Correlated factors (free_recall, cued_recall, recognition)
6. Fit IRT model via variational inference
7. Extract final item parameters
8. Extract final theta scores (these are used in LMM analysis)
9. Save Pass 2 outputs to data folder (primary analysis outputs)

**Output:**

**File 1:** data/step03_item_parameters.csv
**Format:** CSV with columns:
- `item_name` (string)
- `dimension` (string: free_recall, cued_recall, recognition)
- `a` (float, final discrimination)
- `b` (float, final difficulty)

**Expected Rows:** Same as step02_purified_items.csv (40-80 items)

**File 2:** data/step03_theta_scores.csv
**Format:** CSV with columns:
- `composite_ID` (string)
- `theta_free_recall` (float)
- `theta_cued_recall` (float)
- `theta_recognition` (float)
- `se_free_recall` (float)
- `se_cued_recall` (float)
- `se_recognition` (float)

**Expected Rows:** 400

**Validation Requirement:**
Validation tools MUST be used after IRT calibration tool execution. Specific validation tools will be determined by rq_tools based on IRT convergence and improved fit criteria.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_item_parameters.csv: 40-80 rows, 4 columns
- data/step03_theta_scores.csv: 400 rows, 7 columns

*Value Ranges:*
- theta values in [-3, 3] (typical IRT ability range - tighter than Pass 1)
- Standard errors se in [0.1, 1.0] (should improve from Pass 1)
- All a >= 0.4 (by construction from purification)
- All |b| <= 3.0 (by construction from purification)

*Data Quality:*
- All 400 composite_IDs present (no data loss)
- No NaN in theta scores (model must estimate for all)
- Factor correlations in valid range [-1, 1]

*Log Validation:*
- Required pattern: "Model converged: True"
- Required pattern: "Pass 2 calibration complete"
- Required pattern: "VALIDATION - PASS: theta range"
- Forbidden patterns: "CONVERGENCE FAILED", "ERROR"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step03_irt_calibration_pass2.log
- Quit script immediately
- g_debug invoked to diagnose

---

### Step 4: Merge Theta with TSVR for LMM Input

**Dependencies:** Step 3 (requires final theta scores)
**Complexity:** Low (data merging and reshaping)

**Input:**

**File 1:** data/step03_theta_scores.csv
**Format:** CSV with theta scores per paradigm
**Columns:** composite_ID, theta_free_recall, theta_cued_recall, theta_recognition, se_*

**File 2:** data/step00_tsvr_mapping.csv
**Format:** CSV with TSVR time variable
**Columns:** composite_ID, TSVR_hours, test

**Processing:**

1. Load theta scores (wide format: one row per composite_ID)
2. Load TSVR mapping
3. Merge theta with TSVR on composite_ID
4. Reshape from wide to long format:
   - Create `paradigm` factor column (free_recall, cued_recall, recognition)
   - Stack theta values into single `theta` column
   - Stack SE values into single `se_theta` column
5. Extract UID from composite_ID (remove test suffix)
6. Create time transformations for LMM:
   - TSVR_hours (continuous, Decision D070)
   - TSVR_hours_sq (squared term for quadratic models)
   - TSVR_hours_log (log(TSVR_hours + 1) for logarithmic models)
7. Validate factor structure
8. Save LMM input data

**Output:**

**File:** data/step04_lmm_input.csv
**Format:** CSV, long format (one row per observation = composite_ID x paradigm)
**Columns:**
- `composite_ID` (string)
- `UID` (string, participant identifier)
- `test` (string, T1/T2/T3/T4)
- `TSVR_hours` (float, continuous time since encoding)
- `TSVR_hours_sq` (float, squared term)
- `TSVR_hours_log` (float, log-transformed)
- `paradigm` (string: free_recall, cued_recall, recognition)
- `theta` (float, ability estimate)
- `se_theta` (float, standard error)

**Expected Rows:** 1200 (400 composite_IDs x 3 paradigms)

**Validation Requirement:**
Validation tools MUST be used after data merge tool execution. Specific validation tools will be determined by rq_tools based on data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_lmm_input.csv: 1200 rows, 9 columns

*Value Ranges:*
- TSVR_hours in [0, 200]
- TSVR_hours_sq in [0, 40000]
- TSVR_hours_log in [0, 6] (log scale)
- theta in [-3, 3]
- paradigm in {free_recall, cued_recall, recognition}

*Data Quality:*
- All 1200 observations present (400 x 3 paradigms)
- No NaN in TSVR_hours (all must have time variable)
- No duplicate composite_ID x paradigm combinations
- 100 unique UIDs

*Log Validation:*
- Required pattern: "Merged theta with TSVR: 1200 rows"
- Required pattern: "Paradigm factor levels: free_recall, cued_recall, recognition"
- Forbidden patterns: "ERROR", "Missing TSVR", "Merge failed"

**Expected Behavior on Validation Failure:**
- Raise error with specific merge or reshape failure message
- Log failure to logs/step04_merge_theta_tsvr.log
- Quit script immediately
- g_debug invoked to diagnose

---

### Step 5: Fit LMM and Select Best Model

**Dependencies:** Step 4 (requires LMM input data)
**Complexity:** Medium (5 model fits, ~5-10 minutes)

**Input:**

**File:** data/step04_lmm_input.csv
**Format:** CSV, long format
**Required Columns:** UID, TSVR_hours, TSVR_hours_sq, TSVR_hours_log, paradigm, theta

**Processing:**

1. Load LMM input data
2. Configure 5 candidate models (Treatment coding: free_recall as reference):
   - Linear: theta ~ TSVR_hours * paradigm + (TSVR_hours | UID)
   - Quadratic: theta ~ (TSVR_hours + TSVR_hours_sq) * paradigm + (TSVR_hours | UID)
   - Logarithmic: theta ~ TSVR_hours_log * paradigm + (TSVR_hours_log | UID)
   - Lin+Log: theta ~ (TSVR_hours + TSVR_hours_log) * paradigm + (TSVR_hours | UID)
   - Quad+Log: theta ~ (TSVR_hours + TSVR_hours_sq + TSVR_hours_log) * paradigm + (TSVR_hours | UID)
3. Fit all 5 models with REML=False (for AIC comparison)
4. Compare models by AIC, compute Akaike weights
5. Select best model (lowest AIC)
6. Extract fixed effects from best model
7. Save model comparison table and best model summary

**Output:**

**File 1:** results/step05_model_comparison.csv
**Format:** CSV with columns:
- `model` (string: Linear, Quadratic, Log, Lin+Log, Quad+Log)
- `AIC` (float)
- `BIC` (float)
- `LogLik` (float)
- `n_params` (int)
- `delta_AIC` (float, difference from best)
- `akaike_weight` (float)

**Expected Rows:** 5 (one per candidate model)

**File 2:** results/step05_lmm_model_summary.txt
**Format:** Text file with:
- Best model formula
- Fixed effects table (coefficients, SE, z, p-values)
- Random effects variance components
- Model fit statistics

**File 3:** results/step05_fixed_effects.csv
**Format:** CSV with fixed effects from best model
**Columns:** term, estimate, SE, z, p_value

**Validation Requirement:**
Validation tools MUST be used after LMM fitting tool execution. Specific validation tools will be determined by rq_tools based on LMM convergence and residual diagnostics.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step05_model_comparison.csv: 5 rows, 7 columns
- results/step05_lmm_model_summary.txt: text file exists
- results/step05_fixed_effects.csv: variable rows, 5 columns

*Value Ranges:*
- AIC values > 0 (valid likelihood-based criterion)
- Akaike weights sum to approximately 1.0
- delta_AIC >= 0 (best model has delta_AIC = 0)
- p_values in [0, 1]

*Data Quality:*
- All 5 models present in comparison table
- Best model delta_AIC = 0
- No NaN in AIC or coefficients (indicates convergence failure)

*Log Validation:*
- Required pattern: "Best model: [model_name]"
- Required pattern: "Model converged: True" (for at least best model)
- Required pattern: "AIC comparison complete"
- Forbidden patterns: "CONVERGENCE FAILED", "Singular fit"
- Acceptable warnings: "Convergence warning" for non-best models

**Expected Behavior on Validation Failure:**
- Raise error if best model failed to converge
- Log failure to logs/step05_fit_lmm.log
- Quit script immediately
- g_debug invoked to diagnose (common causes: singular random effects)

---

### Step 6: Post-hoc Contrasts and Effect Sizes

**Dependencies:** Step 5 (requires best model fixed effects)
**Complexity:** Low (coefficient extraction and contrast computation)

**Input:**

**File 1:** results/step05_fixed_effects.csv
**Format:** CSV with fixed effects from best model

**File 2:** data/step04_lmm_input.csv
**Format:** CSV, long format (for computing observed means)

**Processing:**

1. Load fixed effects from best model
2. Extract paradigm x time interaction terms:
   - TSVR_hours:paradigm[T.cued_recall] (cued vs free slope difference)
   - TSVR_hours:paradigm[T.recognition] (recognition vs free slope difference)
   - (Additional terms if Lin+Log or Quad model selected)
3. Apply dual p-value reporting (Decision D068):
   - Report uncorrected p-values
   - Compute Bonferroni correction (alpha = 0.05 / 3 = 0.0167 for 3 pairwise tests)
4. Compute Cohen's d effect sizes at Day 6 (maximal divergence expected):
   - d_free_cued: Free Recall vs Cued Recall
   - d_free_recognition: Free Recall vs Recognition
   - d_cued_recognition: Cued Recall vs Recognition
5. Save contrast results and effect sizes

**Output:**

**File 1:** results/step06_post_hoc_contrasts.csv
**Format:** CSV with columns:
- `contrast` (string, e.g., "cued_recall - free_recall")
- `estimate` (float, slope difference)
- `SE` (float)
- `z` (float)
- `p_uncorrected` (float)
- `p_bonferroni` (float)
- `significant_uncorrected` (bool)
- `significant_bonferroni` (bool)

**Expected Rows:** 3 or more (pairwise contrasts for linear and log terms)

**File 2:** results/step06_effect_sizes.csv
**Format:** CSV with columns:
- `comparison` (string, e.g., "free_vs_cued")
- `cohens_d` (float)
- `interpretation` (string: small/medium/large)

**Expected Rows:** 3 (pairwise effect sizes)

**Validation Requirement:**
Validation tools MUST be used after contrast computation tool execution. Specific validation tools will be determined by rq_tools based on contrast validity criteria.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step06_post_hoc_contrasts.csv: 3+ rows, 8 columns
- results/step06_effect_sizes.csv: 3 rows, 3 columns

*Value Ranges:*
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1]
- p_bonferroni >= p_uncorrected (always true)
- Cohen's d in [-3, 3] (typical range for meaningful effects)

*Data Quality:*
- All 3 pairwise comparisons present
- No NaN in estimates or p-values
- Bonferroni alpha = 0.0167 applied correctly

*Log Validation:*
- Required pattern: "Post-hoc contrasts computed"
- Required pattern: "Bonferroni alpha: 0.0167"
- Required pattern: "Effect sizes computed for Day 6"
- Forbidden patterns: "ERROR", "Division by zero"

**Expected Behavior on Validation Failure:**
- Raise error with specific contrast failure message
- Log failure to logs/step06_compute_post_hoc_contrasts.log
- Quit script immediately
- g_debug invoked to diagnose

---

### Step 7: Prepare Trajectory Plot Data

**CRITICAL NOTE:** Plot data preparation IS an analysis step. It:
- Gets executed in Step 14 CODE EXECUTION LOOP (g_code -> bash -> rq_inspect)
- MUST have validation requirements (same as any analysis step)
- Outputs to plots/*.csv (not data/*.csv) but still validated by rq_inspect
- Created by g_code during analysis (NOT by rq_plots during visualization)

**Dependencies:** Step 5 (requires best model for predictions), Step 4 (for observed means)
**Complexity:** Low (data aggregation, no model fitting)

**Purpose:** Aggregate analysis outputs for trajectory visualization (Option B: g_code creates plot source CSV)

**Plot Description:** Trajectory over time with confidence bands showing theta decline across three retrieval paradigms (Free Recall, Cued Recall, Recognition)

**Input:**

**File 1:** data/step04_lmm_input.csv
**Format:** CSV with observed theta values per paradigm per timepoint

**File 2:** results/step05_fixed_effects.csv
**Format:** CSV with model coefficients for predictions

**Required Data Sources:**
- data/step04_lmm_input.csv (columns: composite_ID, UID, TSVR_hours, paradigm, theta)
- results/step05_fixed_effects.csv (columns: term, estimate, SE)

**Processing:**

1. Load LMM input data
2. Compute observed means and 95% CIs per paradigm per timepoint:
   - Group by paradigm and test (nominal timepoints)
   - Calculate mean(theta), SD, N, and 95% CI bounds
3. Generate model predictions across continuous TSVR_hours (0 to 200):
   - Use fixed effects to compute predicted theta
   - Compute prediction intervals
4. Create theta-scale plot source CSV
5. Convert theta to probability scale using IRT 2PL formula (Decision D069)
6. Create probability-scale plot source CSV
7. Save both plot source CSVs

**Output (Plot Source CSVs):**

**File 1:** plots/step07_trajectory_theta_data.csv
**Required Columns:**
- `TSVR_hours` (float): Time since encoding (0 to 200)
- `theta_observed` (float): Mean observed theta per paradigm per timepoint
- `theta_predicted` (float): Model-predicted theta
- `CI_lower` (float): Lower 95% confidence bound
- `CI_upper` (float): Upper 95% confidence bound
- `paradigm` (string): free_recall, cued_recall, recognition

**Expected Rows:** ~60-100 (observed means at 4 timepoints x 3 paradigms + prediction grid)

**File 2:** plots/step07_trajectory_probability_data.csv
**Required Columns:**
- `TSVR_hours` (float): Time since encoding
- `probability_observed` (float): Mean observed probability
- `probability_predicted` (float): Model-predicted probability
- `CI_lower` (float): Lower 95% confidence bound (probability scale)
- `CI_upper` (float): Upper 95% confidence bound (probability scale)
- `paradigm` (string): free_recall, cued_recall, recognition

**Expected Rows:** Same as theta data

**Aggregation Logic:**
1. Group LMM input by paradigm + test -> compute mean(theta), 95% CI
2. Use best model coefficients to generate predictions at TSVR_hours = 0, 24, 72, 144 hours
3. Transform theta predictions to probability: P = 1 / (1 + exp(-theta))
4. Combine observed means and predictions into plot-ready format
5. Sort by paradigm, then TSVR_hours
6. Save to plots/step07_trajectory_*.csv

**Validation Requirement:**
Validation tools MUST be used after plot data preparation tool execution. Specific validation tools determined by rq_tools based on plot data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- plots/step07_trajectory_theta_data.csv exists (exact path)
- plots/step07_trajectory_probability_data.csv exists (exact path)
- Expected rows: 12-100 per file (depends on prediction grid density)
- Expected columns: 6 per file

*Value Ranges:*
- TSVR_hours in [0, 200]
- theta_observed and theta_predicted in [-3, 3]
- probability_observed and probability_predicted in [0, 1]
- CI_lower <= theta_predicted <= CI_upper (bounds must contain estimate)
- paradigm in {free_recall, cued_recall, recognition}

*Data Quality:*
- No NaN values in required columns
- All 3 paradigms represented in data
- CI_upper > CI_lower for all rows (valid confidence intervals)
- At least 12 rows (3 paradigms x 4 observed timepoints)

*Log Validation:*
- Required pattern: "Plot data preparation complete"
- Required pattern: "Theta scale data: X rows"
- Required pattern: "Probability scale data: X rows"
- Required pattern: "All paradigms represented: free_recall, cued_recall, recognition"
- Forbidden patterns: "ERROR", "NaN values detected", "Missing paradigm"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 3 paradigms, found 2")
- Log failure to logs/step07_prepare_trajectory_plot_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- g_debug invoked to diagnose root cause

**Plotting Function (rq_plots will call):** Trajectory plot with confidence bands
- rq_plots agent maps this description to specific tools/plots.py function
- Plot reads plots/step07_trajectory_theta_data.csv and plots/step07_trajectory_probability_data.csv
- No data aggregation in rq_plots (visualization only per Option B)
- Decision D069: BOTH theta-scale AND probability-scale plots generated

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 -> Step 1:** IRT input filtering
- Input: RQ 5.1 full IRT data (all paradigms, all domains)
- Output: Filtered to IFR, ICR, IRE only with paradigm-based Q-matrix

**Step 1 -> Step 2:** Pass 1 calibration results
- Input: Filtered IRT data + paradigm Q-matrix
- Output: Item parameters (a, b per item per paradigm)

**Step 2 -> Step 3:** Item purification
- Input: Pass 1 item parameters
- Output: List of retained items meeting D039 thresholds

**Step 3 -> Step 4:** Pass 2 calibration
- Input: Filtered IRT data (purified items only)
- Output: Final theta scores (wide format, one theta per paradigm)

**Step 4 -> Step 5:** LMM preparation
- Input: Wide theta scores + TSVR mapping
- Output: Long format (paradigm as factor, single theta column)
- Transformation: Wide -> Long reshape + TSVR merge

**Step 5 -> Step 6:** LMM fitting
- Input: Long format LMM data
- Output: Best model + fixed effects + AIC comparison

**Step 6 -> Step 7:** Post-hoc contrasts
- Input: Fixed effects from best model
- Output: Pairwise contrasts + effect sizes

**Step 5+4 -> Step 7:** Plot data preparation
- Input: Fixed effects (predictions) + LMM input (observed means)
- Output: Plot source CSVs (theta + probability scales)

### Column Naming Conventions

Per names.md:
- `composite_ID`: Primary key combining UID and test (format: UID_test)
- `UID`: Participant unique identifier
- `test`: Test session identifier (T1, T2, T3, T4)
- `TSVR_hours`: Time Since VR in hours (Decision D070)
- `theta_<paradigm>`: IRT ability estimate for paradigm factor
- `se_<paradigm>`: Standard error of theta estimate
- `paradigm`: Factor variable (free_recall, cued_recall, recognition)
- `CI_lower`, `CI_upper`: 95% confidence interval bounds

**New Convention for RQ 5.3:**
- `paradigm`: Factor variable for retrieval paradigm (free_recall, cued_recall, recognition)
  - Pattern: paradigm
  - Introduced: RQ 5.3
  - Notes: Analogous to domain factor in RQ 5.1, but for retrieval paradigm comparison

### Data Type Constraints

| Column | Type | Nullable | Valid Range |
|--------|------|----------|-------------|
| composite_ID | string | No | Format: {UID}_{test} |
| UID | string | No | Format: P### |
| test | string | No | {T1, T2, T3, T4} |
| TSVR_hours | float64 | No | [0, 200] |
| paradigm | string | No | {free_recall, cued_recall, recognition} |
| theta | float64 | No | [-3, 3] |
| se_theta | float64 | No | [0.1, 2.0] |
| a | float64 | No | [0.1, 10.0] |
| b | float64 | No | [-6.0, 6.0] |

---

## Cross-RQ Dependencies

### Dependency Type 2: DERIVED Data from Other RQs (Dependencies Exist)

**This RQ requires outputs from:**
- **RQ 5.1** (Domain-Specific Forgetting Trajectories)
  - File: results/ch5/rq1/data/step00_irt_input.csv
  - Used in: Step 0 (filter to paradigm items, reuse dichotomized VR scores)
  - Rationale: RQ 5.1 already extracted and dichotomized all VR items. This RQ reuses that extraction but applies different Q-matrix (paradigm factors instead of domain factors).

  - File: results/ch5/rq1/data/step00_tsvr_mapping.csv
  - Used in: Step 0 (copy TSVR time variable mapping)
  - Rationale: TSVR mapping is identical across RQs (same participants, same test sessions).

**Execution Order Constraint:**
1. RQ 5.1 must complete Step 0 (provides step00_irt_input.csv, step00_tsvr_mapping.csv)
2. This RQ (5.3) executes after RQ 5.1 Step 0 minimum

**Data Source Boundaries (Per Specification 5.1.6):**
- **RAW data:** Not directly used (reuses RQ 5.1 extraction)
- **DERIVED data:** Outputs from RQ 5.1 Step 0 (dichotomized VR scores, TSVR mapping)
- **Scope:** This RQ does NOT use RQ 5.1 theta scores or item parameters (runs fresh IRT with paradigm factors)

**Validation:**
- Step 0: Check results/ch5/rq1/data/step00_irt_input.csv exists
- Step 0: Check results/ch5/rq1/data/step00_tsvr_mapping.csv exists
- If either file missing -> quit with EXPECTATIONS ERROR -> user must execute RQ 5.1 Step 0 first

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

| Step | Analysis Type | Validation Criteria |
|------|---------------|---------------------|
| 0 | Data filtering | Column counts, Q-matrix structure, row sums = 1 |
| 1 | IRT Pass 1 | Convergence, a in [0.1, 10], b in [-6, 6], no NaN |
| 2 | Item purification | a >= 0.4, |b| <= 3.0, >=10 items per paradigm |
| 3 | IRT Pass 2 | Convergence, theta in [-3, 3], SE in [0.1, 1.0] |
| 4 | TSVR merge | 1200 rows, no NaN, 100 unique UIDs |
| 5 | LMM fitting | Convergence, AIC computed for all 5, weights sum to 1 |
| 6 | Post-hoc contrasts | p in [0, 1], Bonferroni applied, d in [-3, 3] |
| 7 | Plot data prep | Both CSVs exist, all paradigms present, CI valid |

---

## Summary

**Total Steps:** 8 (Step 0 through Step 7)
**Estimated Runtime:** High (90-120 minutes total due to 2x IRT calibration)
**Cross-RQ Dependencies:** RQ 5.1 Step 0 outputs (step00_irt_input.csv, step00_tsvr_mapping.csv)
**Primary Outputs:**
- data/step03_theta_scores.csv (paradigm-based ability estimates)
- results/step05_lmm_model_summary.txt (best model results)
- results/step06_post_hoc_contrasts.csv (paradigm comparisons)
- results/step06_effect_sizes.csv (Cohen's d at Day 6)
- plots/step07_trajectory_theta_data.csv (theta-scale plot source)
- plots/step07_trajectory_probability_data.csv (probability-scale plot source)

**Validation Coverage:** 100% (all 8 steps have validation requirements)

**Decisions Applied:**
- D039: 2-pass IRT purification (Steps 1-3)
- D068: Dual p-value reporting (Step 6)
- D069: Dual-scale trajectory plots (Step 7)
- D070: TSVR as time variable (Steps 4-7)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-11-24): Initial plan created by rq_planner agent

---

**End of Analysis Plan**
