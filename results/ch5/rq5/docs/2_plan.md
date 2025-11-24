# Analysis Plan for RQ 5.5: Schema Congruence Effects on Forgetting Trajectories

**Created by:** rq_planner agent
**Date:** 2025-11-24
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

RQ 5.5 examines whether schema congruence (Common, Congruent, Incongruent) affects the trajectory of episodic forgetting over 6 days. This analysis uses IRT-derived ability estimates (theta) from a 3-dimensional Graded Response Model where dimensions represent congruence categories, followed by Linear Mixed Models to test differential forgetting rates.

**Key Theoretical Question:** Does schema-congruent information benefit from consolidation processes, resulting in slower forgetting compared to schema-violating (incongruent) information?

**Pipeline:** IRT (2-pass GRM with purification) -> LMM (5 candidate models, best by AIC)

**Total Steps:** 8 (Step 00 through Step 07)

**Estimated Runtime:** High (IRT calibration x2 + LMM model selection)

**Key Decisions Applied:**
- Decision D039: 2-pass IRT purification (Pass 1 -> purification -> Pass 2)
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni)
- Decision D069: Dual-scale trajectory plots (theta + probability)
- Decision D070: TSVR as LMM time variable (actual hours, not nominal days)

**Critical Design Notes:**
- Congruence factor (Common/Congruent/Incongruent) based on item codes (i1-i2, i3-i4, i5-i6)
- Treatment coding with Common as reference category (schema-neutral baseline)
- Data DERIVED from RQ 5.1 outputs (step00_irt_input.csv, step00_tsvr_mapping.csv)
- Only Interactive paradigms included (IFR, ICR, IRE) - RFR excluded

---

## Cross-RQ Dependencies

### Dependency Type: DERIVED Data from RQ 5.1

**This RQ requires outputs from:**
- **RQ 5.1** (Domain-Specific Forgetting Trajectories)
  - File: `results/ch5/rq1/data/step00_irt_input.csv` (raw VR item responses)
  - File: `results/ch5/rq1/data/step00_tsvr_mapping.csv` (TSVR time mapping)
  - Used in: Step 00 (data preparation)
  - Rationale: RQ 5.1 already extracted VR item data from master.xlsx. RQ 5.5 reuses this extraction but applies different grouping (congruence instead of WWW domain).

**Execution Order Constraint:**
1. RQ 5.1 must have completed at least Step 00 (provides step00_irt_input.csv, step00_tsvr_mapping.csv)
2. This RQ (5.5) can execute after RQ 5.1 Step 00 completes

**Data Source Boundaries:**
- **RAW data:** None directly from master.xlsx (uses RQ 5.1 extraction)
- **DERIVED data:** step00_irt_input.csv, step00_tsvr_mapping.csv from RQ 5.1

**Validation:**
- Step 00: Check results/ch5/rq1/data/step00_irt_input.csv exists
- Step 00: Check results/ch5/rq1/data/step00_tsvr_mapping.csv exists
- If either file missing -> QUIT with "EXPECTATIONS ERROR: RQ 5.1 Step 00 outputs required"

---

## Analysis Plan

### Step 00: Data Preparation and Congruence Q-Matrix Creation

**Dependencies:** RQ 5.1 Step 00 outputs (cross-RQ dependency)
**Complexity:** Low (data filtering and restructuring)

**Purpose:** Extract interactive paradigm items from RQ 5.1 data and create Q-matrix mapping items to congruence categories.

**Input:**

**File 1:** `results/ch5/rq1/data/step00_irt_input.csv`
- Format: Wide format (composite_ID x item columns)
- Columns: composite_ID, VR item tags (e.g., VR_IFR_A01_N_ANS_i1)
- Expected Rows: ~400 (100 participants x 4 tests)

**File 2:** `results/ch5/rq1/data/step00_tsvr_mapping.csv`
- Format: Long format (one row per composite_ID)
- Columns: composite_ID, TSVR_hours, test
- Expected Rows: ~400

**Processing:**

1. **Load RQ 5.1 IRT input data**
2. **Filter columns to Interactive paradigms only:**
   - Keep: VR_IFR_*, VR_ICR_*, VR_IRE_*
   - Remove: VR_RFR_* (Room Free Recall - different response format)
   - Remove: TQ_* columns if present (Text Questions not interactive paradigm)
3. **Create Congruence Q-Matrix:**
   - Parse item suffixes from column names
   - Map: `*_i1` and `*_i2` -> "common"
   - Map: `*_i3` and `*_i4` -> "congruent"
   - Map: `*_i5` and `*_i6` -> "incongruent"
   - Q-matrix format: item_name x dimension (binary loading matrix)
4. **Copy TSVR mapping (unchanged from RQ 5.1)**
5. **Validate item counts per congruence category**

**Output:**

**File 1:** `data/step00_irt_input.csv`
- Format: Wide format (composite_ID x item columns)
- Columns: composite_ID + interactive paradigm item columns only
- Expected Rows: ~400 (100 participants x 4 tests)
- Expected Columns: Reduced from RQ 5.1 (only IFR/ICR/IRE items)

**File 2:** `data/step00_q_matrix.csv`
- Format: Item-by-dimension matrix
- Columns: item_name, common, congruent, incongruent (binary 0/1)
- Expected Rows: Number of retained interactive items (estimate: 90-120 items)
- Values: Each item loads on exactly one dimension

**File 3:** `data/step00_tsvr_mapping.csv`
- Format: Copy of RQ 5.1 TSVR mapping
- Columns: composite_ID, TSVR_hours, test
- Expected Rows: ~400

**Validation Requirement:**
Validation tools MUST be used after data extraction tool execution. Specific validation tools determined by rq_tools based on data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_irt_input.csv exists (exact path)
- data/step00_q_matrix.csv exists (exact path)
- data/step00_tsvr_mapping.csv exists (exact path)
- IRT input: ~400 rows (100 participants x 4 tests)
- Q-matrix: 90-120 rows (interactive items), 4 columns (item_name + 3 dimensions)

*Value Ranges:*
- Item responses in {0, 1, NaN} (binary correct/incorrect)
- Q-matrix values in {0, 1} (binary dimension loading)
- TSVR_hours in [0, 170] (encoding to Day 6)
- Each item loads on exactly 1 dimension (row sum = 1)

*Data Quality:*
- No NaN in composite_ID column
- All 3 congruence categories represented (common, congruent, incongruent)
- Item count per category approximately equal (30-40 items each)
- All 400 composite_IDs from RQ 5.1 preserved

*Log Validation:*
- Required: "Loaded RQ 5.1 data: X rows, Y columns"
- Required: "Filtered to interactive paradigms: Z items retained"
- Required: "Q-matrix created: common=N1, congruent=N2, incongruent=N3"
- Forbidden: "ERROR", "FileNotFoundError", "KeyError"

**Expected Behavior on Validation Failure:**
- Raise error with specific message (e.g., "Missing paradigm: no IFR items found")
- Log failure to logs/step00_extract_congruence_data.log
- Quit script immediately (do NOT proceed to Step 01)
- g_debug invoked to diagnose

---

### Step 01: IRT Calibration Pass 1 (All Items)

**Dependencies:** Step 00 (requires step00_irt_input.csv, step00_q_matrix.csv)
**Complexity:** High (IRT model calibration ~30-60 minutes)

**Purpose:** Calibrate 3-dimensional GRM model on all interactive items to obtain initial item parameters for purification.

**Input:**

**File 1:** `data/step00_irt_input.csv`
- Format: Wide format (composite_ID x item columns)
- Expected Rows: ~400

**File 2:** `data/step00_q_matrix.csv`
- Format: Item x dimension matrix with binary loadings
- Dimensions: common, congruent, incongruent

**Processing:**

1. **Load IRT input data and Q-matrix**
2. **Configure 3-dimensional GRM model:**
   - Model type: Graded Response Model (GRM)
   - Dimensions: 3 (common, congruent, incongruent)
   - Factor structure: Correlated factors (allow inter-factor correlations)
   - Response categories: 2 (dichotomous: 0/1)
3. **Fit IRT model via variational inference (IWAVE algorithm)**
4. **Extract item parameters (discrimination a, difficulty b)**
5. **Extract theta scores (diagnostic only, not final)**
6. **Save Pass 1 outputs to logs/ (diagnostic reference)**

**Output:**

**File 1:** `logs/step01_pass1_item_params.csv`
- Format: CSV with item parameters
- Columns: item_name, dimension, a (discrimination), b (difficulty)
- Expected Rows: 90-120 items
- Purpose: Used in Step 02 for purification threshold application

**File 2:** `logs/step01_pass1_theta.csv`
- Format: CSV with theta estimates
- Columns: composite_ID, theta_common, theta_congruent, theta_incongruent, se_common, se_congruent, se_incongruent
- Expected Rows: ~400
- Purpose: Diagnostic only (not used in analysis - Pass 2 theta is final)

**Validation Requirement:**
Validation tools MUST be used after IRT calibration tool execution. Specific validation tools determined by rq_tools based on IRT convergence and parameter validity requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- logs/step01_pass1_item_params.csv exists
- logs/step01_pass1_theta.csv exists
- Item params: 90-120 rows, 4 columns
- Theta: ~400 rows, 7 columns (composite_ID + 3 theta + 3 SE)

*Value Ranges:*
- Discrimination a in [0.01, 10.0] (all positive, extremely high = estimation issue)
- Difficulty b in [-6.0, 6.0] (extreme values expected for some items)
- Theta in [-4.0, 4.0] (wider range for Pass 1)
- SE in [0.05, 2.0] (very high SE = unreliable)

*Data Quality:*
- No NaN in a or b parameters (model must estimate all)
- All items have valid parameters
- All 3 dimensions represented
- No infinite values

*Log Validation:*
- Required: "Model converged" or "Convergence achieved"
- Required: "ELBO" or "loss" decreasing (evidence of optimization)
- Forbidden: "ERROR", "NaN loss", "DIVERGED"
- Acceptable: "Warning: Some items with extreme parameters" (expected before purification)

**Expected Behavior on Validation Failure:**
- Raise error with specific message (e.g., "IRT model did not converge after N iterations")
- Log failure to logs/step01_irt_calibration_pass1.log
- Quit script immediately
- g_debug invoked to diagnose

---

### Step 02: Item Purification (Decision D039)

**Dependencies:** Step 01 (requires step01_pass1_item_params.csv)
**Complexity:** Low (threshold filtering ~1 minute)

**Purpose:** Identify and remove items with extreme difficulty or low discrimination per Decision D039 thresholds.

**Input:**

**File 1:** `logs/step01_pass1_item_params.csv`
- Format: CSV with item parameters from Pass 1
- Columns: item_name, dimension, a, b

**Processing:**

1. **Load Pass 1 item parameters**
2. **Apply Decision D039 purification thresholds:**
   - Exclude items where |b| > 3.0 (extreme difficulty)
   - Exclude items where a < 0.4 (low discrimination)
   - Retain items meeting BOTH criteria: |b| <= 3.0 AND a >= 0.4
3. **Check minimum items per dimension:**
   - Require >= 10 items per congruence category after purification
   - If any dimension < 10 items: Flag WARNING, consider relaxed thresholds
4. **Generate purification report**
5. **Save purified and removed item lists**

**Purification Thresholds (Decision D039):**
- Maximum difficulty: |b| <= 3.0
- Minimum discrimination: a >= 0.4
- Expected retention: 40-70% of items (schema congruence may have more variability than WWW domains)

**Output:**

**File 1:** `data/step02_purified_items.csv`
- Format: CSV listing retained items
- Columns: item_name, dimension, a, b, retention_reason
- Expected Rows: 50-90 items (estimate based on ~40-70% retention)

**File 2:** `data/step02_removed_items.csv`
- Format: CSV listing excluded items
- Columns: item_name, dimension, a, b, removal_reason
- Expected Rows: 20-50 items

**File 3:** `logs/step02_purification_report.txt`
- Format: Text report
- Content: Summary statistics, items removed per reason, items per dimension before/after

**Validation Requirement:**
Validation tools MUST be used after purification tool execution. Specific validation tools determined by rq_tools based on purification requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_purified_items.csv exists
- data/step02_removed_items.csv exists
- logs/step02_purification_report.txt exists
- Purified items: 50-90 rows, 5 columns
- Removed items: 20-50 rows, 5 columns

*Value Ranges:*
- Retained items: a >= 0.4, |b| <= 3.0 (by definition)
- Removed items: a < 0.4 OR |b| > 3.0 (by definition)
- Retention rate: 40-70% expected

*Data Quality:*
- No dimension eliminated (all 3 congruence categories have >= 10 items)
- >= 50 total items retained (sufficient for IRT estimation)
- Purified + removed = original item count (no items lost)

*Log Validation:*
- Required: "Purification complete: N items retained"
- Required: "Items per dimension: common=X, congruent=Y, incongruent=Z"
- Forbidden: "ERROR", "Dimension eliminated"
- Acceptable: "Warning: Low retention in dimension X" (if >= 10 still retained)

**Expected Behavior on Validation Failure:**
- Raise error (e.g., "Purification failed: congruent dimension has only 5 items")
- Log failure to logs/step02_purify_items.log
- Quit script immediately
- g_debug invoked to diagnose (may need threshold relaxation)

---

### Step 03: IRT Calibration Pass 2 (Purified Items)

**Dependencies:** Step 02 (requires step02_purified_items.csv), Step 00 (requires step00_irt_input.csv)
**Complexity:** High (IRT model calibration ~30-60 minutes)

**Purpose:** Calibrate final 3-dimensional GRM model on purified items to obtain publication-quality theta estimates.

**Input:**

**File 1:** `data/step00_irt_input.csv`
- Format: Wide format (original IRT input)
- Used for: Raw response data

**File 2:** `data/step02_purified_items.csv`
- Format: List of retained items
- Used for: Column selection (only calibrate purified items)

**Processing:**

1. **Load original IRT input data**
2. **Filter columns to purified items only**
3. **Rebuild Q-matrix with purified items (subset of original)**
4. **Configure 3-dimensional GRM model (same structure as Pass 1)**
5. **Fit IRT model via variational inference**
6. **Extract final item parameters**
7. **Extract final theta scores (these are used in LMM)**

**Output:**

**File 1:** `data/step03_item_parameters.csv`
- Format: CSV with final item parameters
- Columns: item_name, dimension, a, b
- Expected Rows: 50-90 items (purified set)
- Note: These are FINAL parameters for publication

**File 2:** `data/step03_theta_scores.csv`
- Format: CSV with final theta estimates
- Columns: composite_ID, theta_common, theta_congruent, theta_incongruent, se_common, se_congruent, se_incongruent
- Expected Rows: ~400 (100 participants x 4 tests)
- Note: These are FINAL theta scores used in LMM (Step 05)

**Validation Requirement:**
Validation tools MUST be used after IRT calibration tool execution. Specific validation tools determined by rq_tools based on IRT convergence and parameter validity requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_item_parameters.csv exists
- data/step03_theta_scores.csv exists
- Item params: 50-90 rows, 4 columns
- Theta: ~400 rows, 7 columns

*Value Ranges:*
- Discrimination a in [0.4, 8.0] (all >= 0.4 after purification)
- Difficulty b in [-3.0, 3.0] (all |b| <= 3.0 after purification)
- Theta in [-3.0, 3.0] (tighter range for publication-quality estimates)
- SE in [0.1, 1.0] (above 1.0 = unreliable, below 0.1 = suspicious)

*Data Quality:*
- No NaN in any theta or parameter column
- All 400 composite_IDs present
- All 3 dimensions have valid estimates
- SE values reasonable (mean SE < 0.5)

*Log Validation:*
- Required: "Model converged" or "Convergence achieved"
- Required: "Final item parameters saved"
- Required: "Final theta scores saved"
- Forbidden: "ERROR", "NaN loss", "DIVERGED"
- Acceptable: None (Pass 2 should be clean)

**Expected Behavior on Validation Failure:**
- Raise error with specific message
- Log failure to logs/step03_irt_calibration_pass2.log
- Quit script immediately
- g_debug invoked to diagnose

---

### Step 04: Merge Theta Scores with TSVR (Decision D070)

**Dependencies:** Step 03 (requires step03_theta_scores.csv), Step 00 (requires step00_tsvr_mapping.csv)
**Complexity:** Low (data merge ~1 minute)

**Purpose:** Merge theta scores with TSVR (Time Since VR) to create LMM input with actual hours as time variable per Decision D070.

**Input:**

**File 1:** `data/step03_theta_scores.csv`
- Format: Wide format with theta scores per dimension
- Columns: composite_ID, theta_common, theta_congruent, theta_incongruent, se_common, se_congruent, se_incongruent

**File 2:** `data/step00_tsvr_mapping.csv`
- Format: TSVR time mapping
- Columns: composite_ID, TSVR_hours, test

**Processing:**

1. **Load theta scores and TSVR mapping**
2. **Merge on composite_ID (left join, keep all theta rows)**
3. **Parse UID from composite_ID** (format: UID_test -> extract UID)
4. **Reshape from wide to long format:**
   - Melt theta columns (theta_common, theta_congruent, theta_incongruent)
   - Create 'congruence' factor variable
   - Result: One row per participant-test-congruence combination
5. **Create time transformations:**
   - TSVR_hours (raw)
   - TSVR_sq = TSVR_hours^2 (quadratic)
   - TSVR_log = log(TSVR_hours + 1) (logarithmic)
6. **Apply Treatment coding:**
   - Reference category: "common" (schema-neutral)
   - Contrasts: congruent vs common, incongruent vs common
7. **Validate no missing TSVR values**

**Output:**

**File 1:** `data/step04_lmm_input.csv`
- Format: Long format (one row per observation)
- Columns: UID, composite_ID, test, congruence, theta, se, TSVR_hours, TSVR_sq, TSVR_log
- Expected Rows: ~1200 (100 participants x 4 tests x 3 congruence categories)
- Note: Ready for LMM fitting

**Validation Requirement:**
Validation tools MUST be used after TSVR merge tool execution. Specific validation tools determined by rq_tools based on data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_lmm_input.csv exists
- Expected rows: ~1200 (400 composite_IDs x 3 congruence levels)
- Expected columns: 9 (UID, composite_ID, test, congruence, theta, se, TSVR_hours, TSVR_sq, TSVR_log)

*Value Ranges:*
- TSVR_hours in [0, 170] (encoding to ~Day 6)
- TSVR_sq in [0, 30000] (max ~170^2)
- TSVR_log in [0, 5.2] (log(171))
- theta in [-3.0, 3.0]
- congruence in {common, congruent, incongruent}

*Data Quality:*
- No NaN in TSVR_hours (all composite_IDs matched)
- No NaN in theta (all estimates present)
- All 100 participants (UIDs) present
- All 3 congruence categories present
- 4 tests per participant x 3 congruence = 12 rows per UID

*Log Validation:*
- Required: "Merged theta with TSVR: N rows"
- Required: "Reshaped to long format: M rows"
- Required: "Treatment coding applied: reference=common"
- Forbidden: "ERROR", "Missing TSVR", "Merge failed"

**Expected Behavior on Validation Failure:**
- Raise error (e.g., "TSVR missing for 15 composite_IDs")
- Log failure to logs/step04_merge_theta_tsvr.log
- Quit script immediately
- g_debug invoked to diagnose

---

### Step 05: LMM Model Fitting and Selection

**Dependencies:** Step 04 (requires step04_lmm_input.csv)
**Complexity:** High (5 model fits, comparison ~30-60 minutes)

**Purpose:** Fit 5 candidate LMMs with Congruence x Time interactions, select best by AIC, extract fixed effects.

**Input:**

**File 1:** `data/step04_lmm_input.csv`
- Format: Long format LMM input
- Columns: UID, composite_ID, test, congruence, theta, se, TSVR_hours, TSVR_sq, TSVR_log

**Processing:**

1. **Load LMM input data**
2. **Configure 5 candidate models with Treatment coding (Common as reference):**

   **Model 1 (Linear):**
   ```
   theta ~ TSVR_hours * congruence + (TSVR_hours | UID)
   ```

   **Model 2 (Quadratic):**
   ```
   theta ~ (TSVR_hours + TSVR_sq) * congruence + (TSVR_hours | UID)
   ```

   **Model 3 (Logarithmic):**
   ```
   theta ~ TSVR_log * congruence + (TSVR_log | UID)
   ```

   **Model 4 (Linear + Logarithmic):**
   ```
   theta ~ (TSVR_hours + TSVR_log) * congruence + (TSVR_hours | UID)
   ```

   **Model 5 (Quadratic + Logarithmic):**
   ```
   theta ~ (TSVR_hours + TSVR_sq + TSVR_log) * congruence + (TSVR_hours | UID)
   ```

3. **Fit all 5 models**
4. **Compare by AIC - select model with lowest AIC**
5. **Extract fixed effects table from best model**
6. **Save model summary and comparison table**

**Key Interaction Terms (Primary Hypothesis Test):**
- TSVR_hours:congruencecongruent - Tests if congruent slope differs from common
- TSVR_hours:congruenceincongruent - Tests if incongruent slope differs from common
- (Similar for quadratic/log terms depending on winning model)

**Output:**

**File 1:** `results/step05_model_comparison.csv`
- Format: CSV with model comparison metrics
- Columns: model_name, AIC, BIC, logLik, df
- Expected Rows: 5 (one per candidate model)

**File 2:** `results/step05_lmm_model_summary.txt`
- Format: Text summary of winning model
- Content: Fixed effects, random effects, fit indices, model formula

**File 3:** `data/step05_lmm_fitted_model.pkl`
- Format: Pickled fitted model object
- Purpose: Used in Step 06 for post-hoc contrasts

**Validation Requirement:**
Validation tools MUST be used after LMM fitting tool execution. Specific validation tools determined by rq_tools based on LMM convergence and residual requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step05_model_comparison.csv exists
- results/step05_lmm_model_summary.txt exists
- data/step05_lmm_fitted_model.pkl exists
- Model comparison: 5 rows, 5 columns

*Value Ranges:*
- AIC: Reasonable values (typically 1000-5000 range for this data size)
- All models should converge (if any didn't, log warning)
- Fixed effect p-values in [0, 1]
- Random effect variances > 0

*Data Quality:*
- Best model clearly identified (lowest AIC)
- Model summary contains fixed effects table
- Interaction terms present (congruence x time)

*Log Validation:*
- Required: "Fitted 5 candidate models"
- Required: "Best model by AIC: [model_name]"
- Required: "Model converged" for winning model
- Forbidden: "ERROR", "ConvergenceWarning" for best model
- Acceptable: "ConvergenceWarning" for non-winning models (log but continue)

**Expected Behavior on Validation Failure:**
- Raise error if best model didn't converge
- Log failure to logs/step05_fit_lmm.log
- Quit script immediately
- g_debug invoked to diagnose

---

### Step 06: Post-Hoc Contrasts and Effect Sizes (Decision D068)

**Dependencies:** Step 05 (requires step05_lmm_fitted_model.pkl)
**Complexity:** Low (contrast extraction ~5 minutes)

**Purpose:** Extract pairwise slope contrasts between congruence categories with dual p-value reporting (Decision D068) and compute effect sizes.

**Input:**

**File 1:** `data/step05_lmm_fitted_model.pkl`
- Format: Pickled fitted LMM object
- Contains: Best model from Step 05

**File 2:** `data/step04_lmm_input.csv`
- Format: LMM input data
- Used for: Effect size computation (raw data needed)

**Processing:**

1. **Load fitted model**
2. **Extract interaction terms:**
   - TSVR_hours:congruencecongruent (congruent slope - common slope)
   - TSVR_hours:congruenceincongruent (incongruent slope - common slope)
   - (Plus any quadratic/log interactions from winning model)
3. **Compute additional contrast:**
   - Congruent vs Incongruent slope difference (requires linear combination)
4. **Apply Decision D068 dual p-value reporting:**
   - Uncorrected p-values (as computed)
   - Bonferroni-corrected p-values (alpha = 0.05 / 3 contrasts = 0.0167)
5. **Compute Cohen's d effect sizes:**
   - d at Day 6: theta difference between congruence categories
   - Standardize by pooled SD at Day 6

**Contrasts Computed:**
1. Congruent - Common (slope difference)
2. Incongruent - Common (slope difference)
3. Congruent - Incongruent (slope difference)

**Output:**

**File 1:** `results/step06_post_hoc_contrasts.csv`
- Format: CSV with contrast results
- Columns: contrast, estimate, SE, z_value, p_uncorrected, p_bonferroni, CI_lower, CI_upper
- Expected Rows: 3 (one per contrast)

**File 2:** `results/step06_effect_sizes.csv`
- Format: CSV with effect sizes
- Columns: comparison, cohen_d, d_CI_lower, d_CI_upper, interpretation
- Expected Rows: 3 (Cong-Com, Incong-Com, Cong-Incong)

**Validation Requirement:**
Validation tools MUST be used after contrast computation tool execution. Specific validation tools determined by rq_tools based on statistical output requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step06_post_hoc_contrasts.csv exists
- results/step06_effect_sizes.csv exists
- Contrasts: 3 rows, 8 columns
- Effect sizes: 3 rows, 5 columns

*Value Ranges:*
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1]
- p_bonferroni >= p_uncorrected (by definition)
- z_value in [-10, 10] (extreme z suggests estimation issue)
- cohen_d in [-2, 2] (typical range; > 2 = very large effect)

*Data Quality:*
- All 3 contrasts computed
- Both p-value types present (Decision D068 compliance)
- CI bounds logical (CI_lower < estimate < CI_upper)

*Log Validation:*
- Required: "Computed 3 pairwise contrasts"
- Required: "Bonferroni correction applied: alpha = 0.0167"
- Required: "Effect sizes computed"
- Forbidden: "ERROR", "NaN p-value"

**Expected Behavior on Validation Failure:**
- Raise error with specific message
- Log failure to logs/step06_compute_post_hoc_contrasts.log
- Quit script immediately
- g_debug invoked to diagnose

---

### Step 07: Prepare Trajectory Plot Data (Decision D069)

**Dependencies:** Step 03 (requires step03_theta_scores.csv), Step 04 (requires step04_lmm_input.csv)
**Complexity:** Low (data aggregation ~5 minutes)

**CRITICAL NOTE:** Plot data preparation IS an analysis step. It:
- Gets executed in Step 14 CODE EXECUTION LOOP (g_code -> bash -> rq_inspect)
- MUST have validation requirements (same as any analysis step)
- Outputs to plots/*.csv (not data/*.csv) but still validated by rq_inspect
- Created by g_code during analysis (NOT by rq_plots during visualization)

**Purpose:** Aggregate theta scores by congruence and time for trajectory visualization (Option B architecture).

**Plot Description:** Trajectory plot showing forgetting curves for 3 congruence categories (Common, Congruent, Incongruent) over Days 0-6, with observed means and 95% confidence intervals.

**Input:**

**File 1:** `data/step04_lmm_input.csv`
- Format: Long format with theta per congruence per test
- Columns: UID, test, congruence, theta, TSVR_hours

**Processing:**

1. **Group by congruence and test**
2. **Compute per-group statistics:**
   - Mean theta
   - 95% CI (mean +/- 1.96 * SE)
   - N observations per group
3. **Create time variable from TSVR_hours:**
   - Use mean TSVR per test (accounts for participant timing variation)
4. **Create theta-scale plot data:**
   - Columns: time, theta_mean, CI_lower, CI_upper, congruence
5. **Create probability-scale plot data (Decision D069):**
   - Transform theta to probability via IRT 2PL formula
   - Assumes average item difficulty (b=0) for interpretability
   - Columns: time, prob_mean, CI_lower, CI_upper, congruence

**Output:**

**File 1:** `plots/step07_trajectory_theta_data.csv`
- Format: Plot source CSV (theta scale)
- Columns: time, theta_mean, CI_lower, CI_upper, congruence
- Expected Rows: 12 (3 congruence categories x 4 tests)

**File 2:** `plots/step07_trajectory_probability_data.csv`
- Format: Plot source CSV (probability scale per Decision D069)
- Columns: time, prob_mean, CI_lower, CI_upper, congruence
- Expected Rows: 12 (3 congruence categories x 4 tests)

**Validation Requirement:**
Validation tools MUST be used after plot data preparation tool execution. Specific validation tools determined by rq_tools based on plot data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- plots/step07_trajectory_theta_data.csv exists
- plots/step07_trajectory_probability_data.csv exists
- Both files: 12 rows, 5 columns

*Value Ranges:*
- time in [0, 170] hours (TSVR range)
- theta_mean in [-3, 3]
- prob_mean in [0, 1] (probability scale)
- CI bounds logical (CI_lower < mean < CI_upper)
- congruence in {common, congruent, incongruent}

*Data Quality:*
- All 12 time x congruence combinations present
- No NaN values
- All 3 congruence categories represented
- Monotonic or expected pattern (may show forgetting)

*Log Validation:*
- Required: "Plot data preparation complete: 12 rows created"
- Required: "Theta scale data saved"
- Required: "Probability scale data saved (Decision D069)"
- Forbidden: "ERROR", "NaN values detected"

**Expected Behavior on Validation Failure:**
- Raise error with specific message
- Log failure to logs/step07_prepare_trajectory_plot_data.log
- Quit script immediately
- g_debug invoked to diagnose

**Plotting Function (rq_plots will call):**
- Plot type: Trajectory plot with confidence bands
- rq_plots agent maps to appropriate tools/plots.py function
- Both theta-scale and probability-scale plots generated
- Separate lines for each congruence category

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 00 -> Step 01:**
- Input: Wide format (composite_ID x items)
- Output: Same format, passed to IRT calibration
- Transformation: Column filtering (interactive paradigms only)

**Step 01 -> Step 02:**
- Input: Item parameter table (item_name, dimension, a, b)
- Output: Filtered item list
- Transformation: Threshold application (D039)

**Step 02 -> Step 03:**
- Input: Purified item list + original response data
- Output: Final theta scores (wide format)
- Transformation: IRT re-calibration on purified items

**Step 03 -> Step 04:**
- Input: Theta scores (wide) + TSVR mapping
- Output: LMM input (long format)
- Transformation: Merge + reshape wide -> long (melt congruence columns)

**Step 04 -> Step 05:**
- Input: Long format LMM data
- Output: Fitted model + model comparison
- Transformation: LMM fitting

**Step 05 -> Step 06:**
- Input: Fitted model object
- Output: Contrast table + effect sizes
- Transformation: Post-hoc extraction

**Step 04 -> Step 07:**
- Input: Long format LMM data
- Output: Aggregated plot data
- Transformation: Group-by aggregation + probability transformation

### Column Naming Conventions

Per names.md (RQ 5.1 conventions):

| Variable | Pattern | Notes |
|----------|---------|-------|
| composite_ID | composite_ID | Primary key (UID_test format) |
| UID | UID | Participant identifier |
| test | test | Test session (T1, T2, T3, T4) |
| theta_* | theta_common, theta_congruent, theta_incongruent | Dimension-specific theta |
| se_* | se_common, se_congruent, se_incongruent | Standard errors |
| TSVR_hours | TSVR_hours | Time variable (Decision D070) |
| congruence | congruence | Factor: common/congruent/incongruent |

### Data Type Constraints

| Column | Data Type | Nullable | Valid Range |
|--------|-----------|----------|-------------|
| composite_ID | string | No | Format: P###_T# |
| UID | string | No | Format: P### |
| test | string | No | {T1, T2, T3, T4} |
| theta_* | float64 | No | [-3, 3] |
| se_* | float64 | No | [0.1, 1.0] |
| TSVR_hours | float64 | No | [0, 170] |
| congruence | string | No | {common, congruent, incongruent} |
| a | float64 | No | [0.4, 8.0] after purification |
| b | float64 | No | [-3.0, 3.0] after purification |

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
- g_code (Step 14 workflow) will generate stepNN_*.py scripts with validation function calls
- bash execution (Step 14 workflow) will run analysis -> validation -> error on validation failure

**Downstream Agent Requirements:**
- **rq_tools:** MUST specify validation tool for EVERY analysis step (no exceptions)
- **rq_analysis:** MUST embed validation tool call for EVERY analysis step (no exceptions)
- **g_code:** MUST generate code with validation function calls (no exceptions)
- **rq_inspect:** MUST verify validation ran successfully (checks logs for validation output)

### Validation Summary by Step

| Step | Analysis Type | Validation Focus |
|------|---------------|------------------|
| Step 00 | Data extraction | File existence, column structure, congruence mapping |
| Step 01 | IRT Pass 1 | Convergence, parameter ranges, no NaN |
| Step 02 | Purification | Thresholds applied correctly, minimum items retained |
| Step 03 | IRT Pass 2 | Convergence, final parameter quality, theta range |
| Step 04 | TSVR merge | Complete merge, no missing values, correct reshaping |
| Step 05 | LMM fitting | Model convergence, AIC comparison, fixed effects extraction |
| Step 06 | Post-hoc | Contrast computation, dual p-values, effect sizes |
| Step 07 | Plot data | Aggregation correct, both scales created, no NaN |

---

## Summary

**Total Steps:** 8 (Step 00 through Step 07)

**Estimated Runtime:** High (2x IRT calibration @ 30-60 min each + 5 LMM fits @ 5-10 min each)

**Cross-RQ Dependencies:** RQ 5.1 (step00_irt_input.csv, step00_tsvr_mapping.csv)

**Primary Outputs:**
- `data/step03_theta_scores.csv` - Final IRT ability estimates by congruence
- `results/step05_lmm_model_summary.txt` - Best LMM model results
- `results/step06_post_hoc_contrasts.csv` - Slope contrasts with dual p-values
- `results/step06_effect_sizes.csv` - Cohen's d effect sizes
- `plots/step07_trajectory_theta_data.csv` - Theta-scale plot source
- `plots/step07_trajectory_probability_data.csv` - Probability-scale plot source

**Validation Coverage:** 100% (all 8 steps have validation requirements)

**Key Hypotheses Tested:**
1. **Primary:** Congruence x Time interaction (differential forgetting rates)
2. **Secondary:** Congruent slower than Incongruent (schema consolidation benefit)
3. **Expected Pattern:** By Day 6: Congruent > Common > Incongruent

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_*.py scripts

---

**Version History:**
- v1.0 (2025-11-24): Initial plan created by rq_planner agent
