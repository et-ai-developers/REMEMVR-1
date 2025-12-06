# Analysis Plan: RQ 6.5.1 - Schema Congruence Effects on Confidence Trajectories

**Research Question:** 6.5.1
**Created:** 2025-12-06
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines whether schema congruence (Common/Congruent/Incongruent items) affects confidence decline patterns across a 6-day retention interval. Analysis uses IRT-derived ability estimates from 5-level Likert confidence ratings (TC_* tags) and tests Schema x Time interaction via Linear Mixed Models. Expected outcome is NULL interaction (paralleling Ch5 5.4.1 accuracy findings), but potential main effect of Congruence on baseline confidence due to schema-based fluency heuristic.

**Pipeline:** IRT (Graded Response Model for ordinal data) -> LMM (trajectory modeling with Schema x Time interaction)

**Steps:** 8 total analysis steps (Step 0: extraction + Steps 1-7: analysis)

**Estimated Runtime:** High (~60-90 minutes total - dominated by two GRM calibrations)

**Key Decisions Applied:**
- Decision D039: 2-pass IRT purification (MANDATORY for all IRT)
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni for post-hoc tests)
- Decision D069: Dual-scale trajectory plots (theta + probability scales)
- Decision D070: TSVR as time variable (actual hours, not nominal days)

---

## Analysis Plan

### Step 0: Extract Confidence Data with Congruence Tags

**Dependencies:** None (first step)
**Complexity:** Low (<5 min, data extraction only)

**Purpose:** Extract 5-level Likert confidence ratings (TC_* tags) from dfData.csv, filter to interactive paradigms (IFR, ICR, IRE) with congruence tags (i1-i6), create omnibus dataset with three schema factors.

**Input:**

**File:** data/cache/dfData.csv (project-level data source)

**Required Columns:**
- UID (string, format: P### with leading zeros)
- TEST (string, values: T1, T2, T3, T4 for Days 0, 1, 3, 6)
- TC_* columns (5-level Likert: 0, 0.25, 0.5, 0.75, 1.0 for confidence ratings)

**Tag Patterns:**
- Confidence items: TC_* (5 ordinal categories representing Likert scale)
- Congruence tags embedded in item names:
  - Common: `*-i1` or `*-i2` patterns (everyday objects in typical placements)
  - Congruent: `*-i3` or `*-i4` patterns (schema-consistent placements)
  - Incongruent: `*-i5` or `*-i6` patterns (schema-violating placements)
- Interactive paradigms only: IFR, ICR, IRE (excludes RFR, TCR, RRE - no TC_* ratings)

**Processing:**

1. Load dfData.csv
2. Filter to TC_* columns (confidence ratings, 5-category ordinal)
3. Filter to items with i1-i6 congruence tags in item names
4. Filter to interactive paradigms (IFR, ICR, IRE) only
5. Create composite_ID (format: UID_test, e.g., P001_T1)
6. Recode Likert values 0, 0.25, 0.5, 0.75, 1.0 to ordinal integers 0-4 for GRM input
7. Extract TSVR time mapping (composite_ID -> TSVR_hours, actual elapsed time)
8. Create Q-matrix (3 factors: Common items load Factor 1, Congruent Factor 2, Incongruent Factor 3)
9. Save wide-format IRT input, TSVR mapping, Q-matrix

**Output:**

**File 1:** data/step00_irt_input.csv
**Format:** CSV, wide format (one row per composite_ID)
**Columns:**
  - composite_ID (string, format: {UID}_{test}, e.g., P001_T1)
  - One column per TC_* item with congruence tag (item name as column header)
  - Values: {0, 1, 2, 3, 4} (ordinal encoding of 5-level Likert: 0=no confidence, 4=very confident)
**Expected Rows:** 400 (100 participants x 4 tests)
**Expected Columns:** ~60-120 columns (composite_ID + TC_* items with i1-i6 tags, exact count depends on paradigm item distribution)

**File 2:** data/step00_tsvr_mapping.csv
**Format:** CSV, time variable mapping per Decision D070
**Columns:**
  - composite_ID (string)
  - TSVR_hours (float, actual time since encoding in hours)
  - test (string, T1/T2/T3/T4)
**Expected Rows:** 400 (100 participants x 4 tests)

**File 3:** data/step00_q_matrix.csv
**Format:** CSV, Q-matrix for 3-factor GRM
**Columns:**
  - item_name (string, TC_* item identifier with congruence tag)
  - factor_common (int, 1 if item is i1/i2, else 0)
  - factor_congruent (int, 1 if item is i3/i4, else 0)
  - factor_incongruent (int, 1 if item is i5/i6, else 0)
**Expected Rows:** ~60-120 items (all TC_* items with i1-i6 tags)
**Note:** Each item loads on exactly ONE factor (mutually exclusive congruence categories)

**Validation Requirement:**

Validation tools MUST be used after data extraction tool execution. Specific validation tools will be determined by rq_tools based on extraction type (TC_* confidence data with congruence tags).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_irt_input.csv: 400 rows x ~60-120 columns (composite_ID + TC_* items)
- data/step00_tsvr_mapping.csv: 400 rows x 3 columns (composite_ID: object, TSVR_hours: float64, test: object)
- data/step00_q_matrix.csv: ~60-120 rows x 4 columns (item_name: object, factor columns: int64)

*Value Ranges:*
- IRT input values in {0, 1, 2, 3, 4} (ordinal Likert encoding, NO 0.25/0.5/0.75 in GRM input)
- TSVR_hours in [0, 200] hours (0=encoding, ~168=1 week, allow margin for scheduling variation)
- Q-matrix factor loadings in {0, 1} (binary indicators)
- Each Q-matrix row sums to exactly 1 (each item loads on exactly one factor)

*Data Quality:*
- composite_ID unique in all three files (no duplicates)
- All 100 participants present (UID P001-P100)
- All 4 tests present per participant (T1, T2, T3, T4)
- Missing data <30% per item column (TC_* confidence ratings may have missingness, but excessive missing suggests extraction error)
- Q-matrix has at least 10 items per factor (minimum for GRM calibration)

*Log Validation:*
- Required: "Extracted {N} TC_* items with congruence tags (i1-i6)"
- Required: "Created 3-factor Q-matrix: Common={N1} items, Congruent={N2} items, Incongruent={N3} items"
- Required: "Recoded Likert values to ordinal 0-4 for GRM input"
- Forbidden: "ERROR", "No TC_* items found", "Congruence tags missing"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 400 rows, found 387" or "Q-matrix rows do not sum to 1")
- Log failure to logs/step00_extract_vr_data.log
- Quit immediately (do NOT proceed to Step 1)
- Master invokes g_debug to diagnose root cause

---

### Step 1: IRT Calibration Pass 1 (All Items)

**Dependencies:** Step 0 (requires IRT input, Q-matrix)
**Complexity:** High (30-60 min, 3-factor GRM calibration on ~60-120 ordinal items)

**Purpose:** Calibrate Graded Response Model (GRM) on all TC_* confidence items (5-category ordinal data) to obtain item parameters for purification. Decision D039 requires 2-pass methodology.

**Input:**

**File 1:** data/step00_irt_input.csv (from Step 0)
**File 2:** data/step00_q_matrix.csv (from Step 0)

**Processing:**

1. Load IRT input (wide format, ordinal responses 0-4)
2. Load Q-matrix (3 factors: Common, Congruent, Incongruent)
3. Configure 3-factor GRM model:
   - Model: Graded Response Model (GRM) for ordinal data (NOT 2PL binary)
   - Dimensions: 3 (Common, Congruent, Incongruent factors)
   - Ordinal categories: 5 (representing 0, 0.25, 0.5, 0.75, 1.0 Likert scale)
   - Prior: p1_med (median-based prior for stability)
4. Fit GRM via variational inference (IWAVE algorithm)
5. Extract item parameters (discrimination a, difficulty thresholds b1-b4 for 5 categories)
6. Extract theta_confidence estimates (diagnostic, for purification decisions)
7. Save Pass 1 item parameters and theta estimates

**Output:**

**File 1:** data/step01_pass1_item_params.csv
**Format:** CSV, item parameters from Pass 1
**Columns:**
  - item_name (string, TC_* identifier)
  - dimension (string, values: common/congruent/incongruent)
  - a (float, discrimination parameter)
  - b1, b2, b3, b4 (float, threshold parameters for 5-category GRM)
**Expected Rows:** ~60-120 items (all TC_* items from Step 0)

**File 2:** data/step01_pass1_theta.csv
**Format:** CSV, theta estimates from Pass 1 (diagnostic)
**Columns:**
  - composite_ID (string)
  - theta_common (float, confidence ability for common items)
  - theta_congruent (float, confidence ability for congruent items)
  - theta_incongruent (float, confidence ability for incongruent items)
  - se_common, se_congruent, se_incongruent (float, standard errors)
**Expected Rows:** 400 (100 participants x 4 tests)

**Validation Requirement:**

Validation tools MUST be used after IRT calibration tool execution. Specific validation tools will be determined by rq_tools based on GRM calibration type.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_pass1_item_params.csv: ~60-120 rows x 7 columns (item_name, dimension, a, b1-b4)
- data/step01_pass1_theta.csv: 400 rows x 7 columns (composite_ID, 3 theta, 3 SE)

*Value Ranges:*
- Discrimination a in [0, 10] (a>10 suggests estimation error, a<0 impossible)
- Thresholds b1-b4 in [-6, 6] (extreme values suggest misfit but not necessarily error)
- Theta in [-4, 4] (wider range than accuracy theta due to confidence variability)
- SE in [0.1, 2.0] (SE>2.0 indicates poor estimation, SE<0.1 suspiciously precise)
- Threshold ordering: b1 < b2 < b3 < b4 (GRM requirement for ordinal categories)

*Data Quality:*
- All items from Step 0 Q-matrix present in item_params (no missing items)
- All 400 composite_IDs present in theta file (no data loss)
- No NaN in discrimination a (convergence failure if NaN)
- No NaN in theta estimates (model must estimate for all participants)

*Log Validation:*
- Required: "Model converged: True"
- Required: "GRM calibration complete: 3 dimensions, 5 ordinal categories"
- Required: "VALIDATION - PASS: theta range [-4, 4]"
- Required: "VALIDATION - PASS: discrimination range [0, 10]"
- Forbidden: "ERROR", "CONVERGENCE FAILED", "NaN in item parameters"
- Acceptable warnings: "Item {name} has extreme difficulty (|b|>3)" (expected for hard confidence items)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Item TC_IFR_i1 has NaN discrimination" or "Threshold ordering violated for item TC_ICR_i5")
- Log failure to logs/step01_irt_calibration_pass1.log
- Quit immediately
- Master invokes g_debug to diagnose (common causes: insufficient data per category, model misspecification)

---

### Step 2: Item Purification (Decision D039)

**Dependencies:** Step 1 (requires Pass 1 item parameters)
**Complexity:** Low (<5 min, filtering by thresholds)

**Purpose:** Filter TC_* confidence items by quality thresholds to retain well-performing items for Pass 2 calibration. Decision D039 requires |b| <= 3.0 AND a >= 0.4, applied separately per factor.

**Input:**

**File:** data/step01_pass1_item_params.csv (from Step 1)

**Processing:**

1. Load Pass 1 item parameters
2. Apply Decision D039 thresholds PER FACTOR:
   - Discrimination: a >= 0.4 (items with a<0.4 provide little information)
   - Difficulty: |b_avg| <= 3.0 where b_avg = mean(b1, b2, b3, b4) for GRM thresholds
3. Retain items meeting BOTH criteria
4. Create purified item list per factor
5. Generate purification report (excluded items with reasons)
6. Save purified items and report

**Note on GRM Difficulty Criterion:**
GRM has 4 threshold parameters (b1-b4), not single difficulty b. Use AVERAGE of thresholds for |b|<=3.0 criterion: b_avg = (b1+b2+b3+b4)/4. This extends Decision D039 from 2PL (single b) to GRM (multiple thresholds).

**Output:**

**File 1:** data/step02_purified_items.csv
**Format:** CSV, list of retained items per factor
**Columns:**
  - item_name (string)
  - dimension (string, common/congruent/incongruent)
  - a (float, discrimination from Pass 1)
  - b_avg (float, average threshold from Pass 1)
  - retained (bool, always True in this file)
**Expected Rows:** 30-70% of Step 1 items (expect ~20-80 items retained, confidence items may have lower retention than accuracy items)

**File 2:** data/step02_purification_report.txt
**Format:** Plain text report
**Content:**
  - Total items evaluated per factor
  - Items retained per factor (N and %)
  - Items excluded per factor with reasons (low discrimination / extreme difficulty)
  - Threshold values used (a>=0.4, |b_avg|<=3.0)

**Validation Requirement:**

Validation tools MUST be used after purification tool execution. Specific validation tools will be determined by rq_tools based on filtering operation type.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_purified_items.csv: 30-70% of input rows, 5 columns
- data/step02_purification_report.txt: exists, >100 characters (non-empty report)

*Value Ranges:*
- All a values >= 0.4 (threshold enforcement)
- All |b_avg| values <= 3.0 (threshold enforcement)
- Retention rate per factor in [0.20, 0.90] (outside range suggests calibration problem)

*Data Quality:*
- At least 10 items retained per factor (minimum for GRM re-calibration)
- If any factor has <10 items: WARNING not error (may need to relax thresholds, but let user decide)
- No duplicate item_names
- All dimensions from Step 1 represented (common, congruent, incongruent)

*Log Validation:*
- Required: "Purification complete: Common {N1} retained, Congruent {N2} retained, Incongruent {N3} retained"
- Required: "Excluded {M} items: {K1} low discrimination, {K2} extreme difficulty"
- Forbidden: "ERROR", "No items retained"
- Acceptable warnings: "Factor {name} has <15 items (minimum viable, consider threshold relaxation)"

**Expected Behavior on Validation Failure:**
- If <10 items per factor: Log WARNING (not error), proceed but flag for user review
- If 0 items retained: QUIT with error "Purification failed: no items retained, thresholds too strict"
- If retention >90%: Log WARNING "High retention rate (>{X}%), purification may be ineffective"
- Log to logs/step02_purify_items.log

---

### Step 3: IRT Calibration Pass 2 (Purified Items)

**Dependencies:** Step 2 (requires purified item list), Step 0 (requires original IRT input)
**Complexity:** High (30-60 min, 3-factor GRM re-calibration on purified items)

**Purpose:** Re-calibrate Graded Response Model on purified items only to obtain final theta_confidence estimates for LMM. Decision D039 2-pass methodology ensures high-quality ability estimates.

**Input:**

**File 1:** data/step00_irt_input.csv (from Step 0, original wide-format data)
**File 2:** data/step02_purified_items.csv (from Step 2, retained item list)

**Processing:**

1. Load original IRT input (all items)
2. Load purified item list (retained items only)
3. Filter IRT input to purified items only (drop excluded items)
4. Update Q-matrix to purified items only (3 factors, fewer items per factor)
5. Configure 3-factor GRM model on purified items:
   - Same structure as Pass 1 (GRM, 3 dimensions, 5 ordinal categories)
   - Same prior (p1_med)
   - Fewer items (only purified items)
6. Fit GRM via variational inference
7. Extract FINAL theta_confidence estimates per congruence level
8. Extract FINAL item parameters (for documentation)
9. Save Pass 2 theta scores and item parameters

**Output:**

**File 1:** data/step03_theta_confidence_congruence.csv
**Format:** CSV, FINAL theta estimates from Pass 2
**Columns:**
  - composite_ID (string)
  - theta_common (float, confidence ability for common items)
  - theta_congruent (float, confidence ability for congruent items)
  - theta_incongruent (float, confidence ability for incongruent items)
  - se_common, se_congruent, se_incongruent (float, standard errors)
**Expected Rows:** 400 (100 participants x 4 tests)
**Note:** These are the FINAL theta estimates used in LMM (not Pass 1 diagnostic estimates)

**File 2:** data/step03_item_parameters.csv
**Format:** CSV, FINAL item parameters from Pass 2
**Columns:**
  - item_name (string)
  - dimension (string)
  - a (float, discrimination)
  - b1, b2, b3, b4 (float, GRM thresholds)
**Expected Rows:** ~20-80 items (purified item set from Step 2)

**Validation Requirement:**

Validation tools MUST be used after IRT calibration tool execution. Specific validation tools will be determined by rq_tools based on GRM calibration type.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_theta_confidence_congruence.csv: 400 rows x 7 columns (composite_ID, 3 theta, 3 SE)
- data/step03_item_parameters.csv: ~20-80 rows x 7 columns (item_name, dimension, a, b1-b4)

*Value Ranges:*
- Theta in [-4, 4] (confidence ability range)
- SE in [0.1, 1.5] (tighter than Pass 1 due to purified items, SE>1.5 suggests poor estimation)
- Discrimination a in [0.4, 10] (lower bound enforced by purification)
- Thresholds b1-b4 in [-6, 6], with b1 < b2 < b3 < b4 (ordering required)
- Average threshold |b_avg| <= 3.0 (enforced by purification, should hold in Pass 2)

*Data Quality:*
- All 400 composite_IDs present (no data loss from Pass 1 to Pass 2)
- No NaN in theta or SE (convergence must succeed)
- Item count matches Step 2 purified_items.csv (exactly the items retained)
- Improved SE relative to Pass 1: median(SE_pass2) <= median(SE_pass1) for each factor

*Log Validation:*
- Required: "Model converged: True"
- Required: "Pass 2 calibration complete: {N} purified items across 3 dimensions"
- Required: "VALIDATION - PASS: theta range [-4, 4]"
- Required: "VALIDATION - PASS: SE improvement vs Pass 1 (median SE reduced)"
- Forbidden: "ERROR", "CONVERGENCE FAILED", "NaN in theta estimates"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Theta out of range for composite_ID P015_T3")
- Log failure to logs/step03_irt_calibration_pass2.log
- Quit immediately
- Master invokes g_debug to diagnose

---

### Step 4: Merge Theta with TSVR (Decision D070)

**Dependencies:** Step 3 (requires theta_confidence), Step 0 (requires TSVR mapping)
**Complexity:** Low (<5 min, simple merge operation)

**Purpose:** Merge final theta_confidence estimates with TSVR time variable for LMM input. Decision D070 requires TSVR (actual hours) not nominal days (0/1/3/6).

**Input:**

**File 1:** data/step03_theta_confidence_congruence.csv (from Step 3, 400 rows x 7 cols)
**File 2:** data/step00_tsvr_mapping.csv (from Step 0, 400 rows x 3 cols)

**Processing:**

1. Load theta_confidence (composite_ID, theta per dimension, SE per dimension)
2. Load TSVR mapping (composite_ID, TSVR_hours, test)
3. Merge on composite_ID (left join, keep all theta scores)
4. Verify all composite_IDs matched (no missing TSVR values)
5. Reshape if needed for LMM format (likely needs long format: one row per observation = one dimension per composite_ID)
6. Create congruence factor column (categorical: Common/Congruent/Incongruent)
7. Save LMM input file

**Note on Reshaping:**
LMM with Schema x Time interaction requires LONG format where each row represents one observation (one schema level for one participant at one test). Step 3 theta file has 3 theta columns (wide). This step reshapes to long: 400 rows x 3 dimensions = 1200 rows.

**Output:**

**File:** data/step04_lmm_input.csv
**Format:** CSV, long format for LMM
**Columns:**
  - composite_ID (string, format: UID_test)
  - UID (string, participant identifier for random effects)
  - test (string, T1/T2/T3/T4)
  - TSVR_hours (float, time variable per Decision D070)
  - congruence (string, categorical: Common/Congruent/Incongruent)
  - theta_confidence (float, ability estimate for this congruence level)
  - se_confidence (float, standard error for this theta)
**Expected Rows:** 1200 (400 composite_IDs x 3 congruence levels)
**Expected Format:** Long (one row per measurement = one congruence level per participant-test)

**Validation Requirement:**

Validation tools MUST be used after merge tool execution. Specific validation tools will be determined by rq_tools based on merge operation type.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_lmm_input.csv: 1200 rows x 7 columns (composite_ID, UID, test, TSVR_hours, congruence, theta_confidence, se_confidence)

*Value Ranges:*
- TSVR_hours in [0, 200] (same as Step 0)
- theta_confidence in [-4, 4] (same as Step 3)
- se_confidence in [0.1, 1.5] (same as Step 3)
- congruence in {Common, Congruent, Incongruent} (exactly 3 categories)

*Data Quality:*
- Exactly 1200 rows (400 composite_IDs x 3 congruence levels)
- Each composite_ID appears exactly 3 times (once per congruence level)
- Each UID appears 12 times (4 tests x 3 congruence levels)
- No NaN in TSVR_hours (all composite_IDs must have matched TSVR)
- No NaN in theta_confidence or se_confidence (no data loss from merge)

*Log Validation:*
- Required: "Merge complete: all 400 composite_IDs matched with TSVR"
- Required: "Reshaped to long format: 1200 observations (400 x 3 congruence levels)"
- Required: "Congruence factor created: Common={N1}, Congruent={N2}, Incongruent={N3} observations"
- Forbidden: "ERROR", "Missing TSVR values", "Merge failed"

**Expected Behavior on Validation Failure:**
- If <1200 rows: QUIT with error "Expected 1200 rows, found {N} (reshape failed)"
- If any composite_ID has != 3 congruence levels: QUIT with error "Incomplete data for {composite_ID}"
- Log failure to logs/step04_merge_theta_tsvr.log

---

### Step 5: Fit LMM with Schema x Time Interaction

**Dependencies:** Step 4 (requires LMM input with congruence factor and TSVR)
**Complexity:** Medium (5-15 min, LMM with random slopes)

**Purpose:** Fit Linear Mixed Model to test primary hypothesis (Schema x Time interaction NULL) and secondary hypothesis (Congruence main effect on baseline confidence). Decision D070 uses TSVR_hours as time variable. Decision D068 applies to post-hoc tests if effects detected.

**Input:**

**File:** data/step04_lmm_input.csv (from Step 4, 1200 rows long format)

**Processing:**

1. Load LMM input (long format with congruence factor)
2. Check for time transformations (linear vs quadratic vs log):
   - If RQ 6.1.1 functional form selection available: use selected transformation
   - If not available: default to linear TSVR_hours (simplest model)
3. Specify LMM formula:
   - Fixed effects: theta_confidence ~ congruence * TSVR_hours (interaction term tests primary hypothesis)
   - Random effects: (1 + TSVR_hours | UID) - random intercepts and slopes per participant
4. Fit LMM via REML (restricted maximum likelihood)
5. Extract fixed effects table (coefficients, SE, z, p-values)
6. Test primary hypothesis: congruence:TSVR_hours interaction term p-value
7. Test secondary hypothesis: congruence main effect p-value
8. Save LMM model summary

**Output:**

**File:** data/step05_lmm_model_summary.txt
**Format:** Plain text LMM summary
**Content:**
  - Model formula
  - Fixed effects table (coefficients, SE, z, p-values for congruence, TSVR_hours, congruence:TSVR_hours)
  - Random effects variance components
  - Model fit indices (AIC, BIC, log-likelihood)
  - Convergence status
  - PRIMARY TEST: congruence:TSVR_hours interaction p-value (NULL hypothesis test)
  - SECONDARY TEST: congruence main effect p-values (baseline differences)

**Validation Requirement:**

Validation tools MUST be used after LMM fitting tool execution. Specific validation tools will be determined by rq_tools based on LMM type.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_lmm_model_summary.txt: exists, >500 characters (complete summary)

*Value Ranges:*
- Fixed effects coefficients in [-5, 5] (larger values unlikely for standardized theta)
- Standard errors > 0 (SE=0 suggests singular fit)
- p-values in [0, 1] (statistical requirement)
- Random effects variances > 0 (negative variance impossible, zero suggests convergence issue)

*Data Quality:*
- Model converged successfully (convergence flag = True)
- All fixed effects terms present: Intercept, congruence[Congruent], congruence[Incongruent], TSVR_hours, congruence[Congruent]:TSVR_hours, congruence[Incongruent]:TSVR_hours
- Random effects for both intercept and slope (2 variance components + covariance)
- No singular fit warnings (if present, log WARNING not error)

*Log Validation:*
- Required: "LMM converged: True"
- Required: "Fixed effects: 6 terms (intercept, 2 congruence levels, time, 2 interactions)"
- Required: "Random effects: intercept + slope by UID"
- Required: "PRIMARY TEST - Schema x Time interaction: congruence:TSVR_hours p={p-value}"
- Required: "SECONDARY TEST - Congruence main effect: p={p-value}"
- Forbidden: "ERROR", "CONVERGENCE FAILED", "Singular fit"
- Acceptable warnings: "Model may be overparameterized (complex random structure)" (proceed if converged)

**Expected Behavior on Validation Failure:**
- If convergence failed: QUIT with error "LMM did not converge, check random effects structure"
- If singular fit: Log WARNING, save summary, proceed to Step 6 (user decides if acceptable)
- Log failure to logs/step05_fit_lmm.log

---

### Step 6: Compute Post-Hoc Contrasts (If Effects Detected)

**Dependencies:** Step 5 (requires LMM model summary), Step 4 (requires LMM input for re-fitting)
**Complexity:** Low (<5 min, pairwise contrasts)

**Purpose:** If Step 5 detected significant Congruence effects (main effect or interaction), compute pairwise contrasts with dual p-value reporting per Decision D068 (uncorrected + Bonferroni). If NO effects detected, this step creates empty output (documented NULL result).

**Input:**

**File 1:** data/step05_lmm_model_summary.txt (from Step 5, check for significant effects)
**File 2:** data/step04_lmm_input.csv (from Step 4, for re-fitting contrasts)

**Processing:**

**Conditional Logic:**
1. Parse Step 5 summary for p-values:
   - Congruence main effect p-value
   - Congruence x Time interaction p-values
2. IF any p < 0.05: Compute post-hoc contrasts
3. IF all p >= 0.05: Document NULL result, create empty contrasts file

**If Contrasts Needed:**
1. Specify 3 pairwise comparisons:
   - Common vs Congruent
   - Common vs Incongruent
   - Congruent vs Incongruent
2. Compute contrasts at baseline (TSVR_hours=0, Day 0) for main effect
3. Compute contrasts at each timepoint for interaction effect (if interaction significant)
4. Report DUAL p-values per Decision D068:
   - p_uncorrected (raw comparison p-value)
   - p_bonferroni (Bonferroni correction for 3 comparisons: p_uncorrected x 3)
5. Compute effect sizes (Cohen's d for pairwise differences)
6. Save contrasts table

**Output:**

**File 1:** data/step06_post_hoc_contrasts.csv
**Format:** CSV, pairwise contrasts with dual p-values
**Columns:**
  - contrast (string, e.g., "Common vs Congruent")
  - estimate (float, mean difference)
  - SE (float, standard error)
  - z (float, z-statistic)
  - p_uncorrected (float, uncorrected p-value per Decision D068)
  - p_bonferroni (float, Bonferroni-corrected p-value per Decision D068)
  - timepoint (string, "Baseline" or "T1/T2/T3/T4" if interaction contrasts)
**Expected Rows:** 0 rows if NULL (no effects), 3 rows if main effect only, 12 rows if interaction (3 contrasts x 4 timepoints)

**File 2:** data/step06_effect_sizes.csv
**Format:** CSV, Cohen's d effect sizes for contrasts
**Columns:**
  - contrast (string)
  - cohens_d (float, effect size)
  - timepoint (string, if applicable)
**Expected Rows:** 0 rows if NULL, 3 rows if main effect, 12 rows if interaction

**Validation Requirement:**

Validation tools MUST be used after contrast computation tool execution. Specific validation tools will be determined by rq_tools based on post-hoc test type.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_post_hoc_contrasts.csv: 0-12 rows x 7 columns (conditional on Step 5 results)
- data/step06_effect_sizes.csv: 0-12 rows x 3 columns (matches contrasts file)

*Value Ranges:*
- estimate (mean difference) in [-3, 3] (theta scale, larger differences unlikely)
- SE > 0 (standard errors must be positive)
- p_uncorrected in [0, 1] (statistical requirement)
- p_bonferroni in [0, 1] AND p_bonferroni >= p_uncorrected (correction increases p-value)
- cohens_d in [-2, 2] (effect sizes beyond ±2 are extremely large)

*Data Quality:*
- If file has rows: BOTH p-value columns present (Decision D068 dual reporting MANDATORY)
- If file has 0 rows: Log "NULL result - no significant effects in Step 5"
- Row count matches expectation (3 for main effect, 12 for interaction, 0 for NULL)
- All 3 pairwise contrasts present if any rows (Common vs Congruent, Common vs Incongruent, Congruent vs Incongruent)

*Log Validation:*
- Required (if contrasts computed): "Post-hoc contrasts complete: {N} comparisons with dual p-values (Decision D068)"
- Required (if NULL): "No significant effects detected - NULL result documented"
- Required: "VALIDATION - PASS: Dual p-values present (uncorrected + Bonferroni)"
- Forbidden: "ERROR", "Missing p-value column"

**Expected Behavior on Validation Failure:**
- If p_bonferroni < p_uncorrected: QUIT with error "Bonferroni p-value less than uncorrected (calculation error)"
- If missing p-value column: QUIT with error "Decision D068 violation: dual p-values required"
- Log failure to logs/step06_compute_post_hoc_contrasts.log

---

### Step 7: Prepare Trajectory Plot Data (Decision D069 Dual-Scale)

**Dependencies:** Step 4 (requires LMM input), Step 5 (requires LMM model for predictions)
**Complexity:** Low (<5 min, data aggregation for plotting)

**Purpose:** Aggregate analysis outputs to create plot source CSVs for trajectory visualization. Decision D069 requires BOTH theta-scale and probability-scale plots for interpretability.

**Input:**

**File 1:** data/step04_lmm_input.csv (from Step 4, observed theta values)
**File 2:** data/step05_lmm_model_summary.txt (from Step 5, for extracting model predictions if needed)

**Processing:**

1. Load LMM input (1200 rows with theta_confidence, congruence, TSVR_hours)
2. Compute observed means per congruence x timepoint:
   - Group by congruence (Common/Congruent/Incongruent) and test (T1/T2/T3/T4)
   - Compute mean(theta_confidence), 95% CI (lower, upper bounds)
3. Compute model predictions (from LMM fixed effects):
   - Predict theta at each timepoint for each congruence level
   - Use TSVR_hours values corresponding to T1/T2/T3/T4 (aggregate or median TSVR per test)
4. Merge observed means + predictions
5. Create THETA-scale plot data (theta values on y-axis)
6. Transform theta to PROBABILITY scale:
   - Use IRT 2PL formula: P(correct) = 1 / (1 + exp(-(theta)))
   - This is simplified transformation (assumes average item difficulty b=0)
7. Create PROBABILITY-scale plot data (probability values 0-1 on y-axis)
8. Save both plot source CSVs

**Output:**

**File 1:** data/step07_trajectory_theta_data.csv
**Format:** CSV, plot source data for theta-scale trajectory (Decision D069)
**Columns:**
  - time (float, TSVR_hours, values: ~0, ~24, ~72, ~144 for nominal Days 0, 1, 3, 6)
  - theta (float, observed mean theta per congruence per timepoint)
  - CI_lower (float, lower 95% confidence bound for theta)
  - CI_upper (float, upper 95% confidence bound for theta)
  - congruence (string, Common/Congruent/Incongruent)
  - source (string, "Observed" or "Predicted" to distinguish data vs model)
**Expected Rows:** 24 (3 congruence levels x 4 timepoints x 2 sources) OR 12 if only observed (depends on plotting preference)

**File 2:** data/step07_trajectory_probability_data.csv
**Format:** CSV, plot source data for probability-scale trajectory (Decision D069)
**Columns:**
  - time (float, TSVR_hours)
  - probability (float, transformed theta to 0-1 scale)
  - CI_lower (float, lower 95% CI for probability)
  - CI_upper (float, upper 95% CI for probability)
  - congruence (string)
  - source (string)
**Expected Rows:** 24 (or 12, matches theta_data file)

**Validation Requirement:**

Validation tools MUST be used after plot data preparation tool execution. Specific validation tools will be determined by rq_tools based on data aggregation type.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_trajectory_theta_data.csv: 12-24 rows x 6 columns
- data/step07_trajectory_probability_data.csv: 12-24 rows x 6 columns

*Value Ranges:*
- time in [0, 168] hours (0=encoding, 168=1 week)
- theta in [-4, 4] (confidence ability range)
- probability in [0, 1] (transformed scale, 0.5 = theta=0)
- CI_lower in [-4, 4] for theta file, [0, 1] for probability file
- CI_upper in [-4, 4] for theta file, [0, 1] for probability file
- CI_upper > CI_lower for all rows (confidence intervals must be valid)

*Data Quality:*
- All 3 congruence levels present (Common, Congruent, Incongruent)
- All 4 timepoints present (approximately 0, 24, 72, 144 hours)
- Row counts match between theta and probability files (same data, different scales)
- No NaN values in any column (complete aggregation required)
- source column has valid values ("Observed" or "Predicted" if model predictions included)

*Log Validation:*
- Required: "Plot data preparation complete: 3 congruence levels x 4 timepoints"
- Required: "THETA-scale data created: data/step07_trajectory_theta_data.csv"
- Required: "PROBABILITY-scale data created: data/step07_trajectory_probability_data.csv (Decision D069)"
- Required: "All congruence levels present: Common, Congruent, Incongruent"
- Forbidden: "ERROR", "NaN values detected", "Missing congruence level"

**Expected Behavior on Validation Failure:**
- If missing congruence level: QUIT with error "Expected 3 congruence levels, found {N}"
- If CI_upper <= CI_lower: QUIT with error "Invalid confidence interval in row {i}"
- If probability out of [0,1]: QUIT with error "Probability transformation failed (value out of bounds)"
- Log failure to logs/step07_prepare_trajectory_plot_data.log

**Plotting Function (rq_plots will call later):**
- Plot type: Trajectory with confidence bands
- rq_plots agent maps this to plot_trajectory() and plot_trajectory_probability() functions from tools/plots.py
- Reads data/step07_trajectory_theta_data.csv and data/step07_trajectory_probability_data.csv (created by this step)
- NO data aggregation in rq_plots (visualization only per Option B architecture)
- PNG outputs saved to plots/ folder by rq_plots (plots/trajectory_theta.png, plots/trajectory_probability.png)

---

## Expected Data Formats

### Composite ID Format
**Pattern:** {UID}_{test}
**Examples:** P001_T1, P015_T3, P100_T4
**Used In:** All IRT and LMM files as primary key

### Congruence Factor Encoding
**Categories:** Common, Congruent, Incongruent
**Item Tag Mapping:**
- i1, i2 -> Common (everyday objects in typical placements)
- i3, i4 -> Congruent (schema-consistent placements)
- i5, i6 -> Incongruent (schema-violating placements)

### Time Variable (Decision D070)
**Variable:** TSVR_hours (Time Since VR in hours)
**Range:** [0, 200] hours (0 = encoding, ~24 = Day 1, ~72 = Day 3, ~144 = Day 6)
**NOT USED:** Nominal days (0, 1, 3, 6) - Decision D070 requires actual elapsed time

### Ordinal Likert Encoding for GRM
**Original Scale:** 0, 0.25, 0.5, 0.75, 1.0 (5-level Likert in master data)
**GRM Input:** 0, 1, 2, 3, 4 (ordinal integers for GRM algorithm)
**Mapping:** 0 -> 0, 0.25 -> 1, 0.5 -> 2, 0.75 -> 3, 1.0 -> 4
**Interpretation:** 0 = not at all confident, 4 = extremely confident

### IRT Q-Matrix Structure (3 Factors)
**Format:** Binary indicator matrix
**Dimensions:** N_items x 3 (Common, Congruent, Incongruent)
**Constraint:** Each row sums to 1 (each item loads on exactly one factor)
**Example:**
```
item_name          | factor_common | factor_congruent | factor_incongruent
TC_IFR_obj01_i1    | 1             | 0                | 0
TC_ICR_obj05_i3    | 0             | 1                | 0
TC_IRE_obj10_i6    | 0             | 0                | 1
```

### Wide-to-Long Transformation (Step 4)
**Input (Wide):** 400 rows x 7 columns (composite_ID, theta_common, theta_congruent, theta_incongruent, se_common, se_congruent, se_incongruent)
**Output (Long):** 1200 rows x 7 columns (composite_ID, UID, test, TSVR_hours, congruence, theta_confidence, se_confidence)
**Logic:** Each wide row (1 participant-test) becomes 3 long rows (1 per congruence level)

---

## Cross-RQ Dependencies

**Dependency Type:** RAW Data Only (No Dependencies)

**This RQ uses:** Only dfData.csv (project-level data source) for TC_* confidence items
**No dependencies on other RQs:** Can be executed independently
**Execution order:** Flexible (any order within Chapter 6)

**Data Sources:**
- data/cache/dfData.csv - participant TC_* confidence responses (5-level Likert)
- TSVR embedded in dfData.csv or master.xlsx - timing data (actual hours since encoding)

**Note:** All data extraction uses direct access to dfData.csv. No intermediate outputs from other RQs required. However, this RQ provides COMPARISON context to Ch5 5.4.1 (accuracy trajectories), comparing confidence vs accuracy schema effects.

**Comparison Reference (Not a Dependency):**
- **RQ 5.4.1** (Schema Congruence Effects on Accuracy Trajectories)
  - Expected finding: NULL Schema x Time interaction (congruence does NOT affect accuracy decline rate)
  - This RQ compares: Does confidence pattern match accuracy pattern (NULL) OR diverge (fluency bias)?
  - Files NOT required, but conceptual reference for interpretation

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

#### Step 0: Extract Confidence Data
**Analysis Tool:** (determined by rq_tools - likely tools.data.extract_confidence_items)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_data_format + validate_data_columns)

**What Validation Checks:**
- All 3 output files exist (irt_input, tsvr_mapping, q_matrix)
- irt_input: 400 rows, ~60-120 columns, values in {0,1,2,3,4}
- tsvr_mapping: 400 rows, 3 columns, TSVR_hours in [0,200]
- q_matrix: ~60-120 rows, 4 columns, factor loadings in {0,1}, rows sum to 1
- composite_ID unique across all files
- At least 10 items per factor in Q-matrix (minimum for GRM)

#### Step 1: IRT Pass 1
**Analysis Tool:** (determined by rq_tools - likely tools.analysis_irt.calibrate_irt with GRM)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_irt_convergence + validate_irt_parameters)

**What Validation Checks:**
- Model converged (log-likelihood improved, not NaN)
- Item parameters in valid ranges (a in [0,10], b1-b4 in [-6,6], b1<b2<b3<b4)
- Theta in [-4,4], SE in [0.1,2.0]
- All 400 composite_IDs present (no data loss)
- No NaN in discrimination or theta

#### Step 2: Item Purification
**Analysis Tool:** (determined by rq_tools - likely tools.analysis_irt.filter_items_by_quality)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_irt_parameters)

**What Validation Checks:**
- All retained items meet thresholds (a>=0.4, |b_avg|<=3.0)
- At least 10 items per factor retained (minimum for re-calibration)
- Retention rate per factor in [0.20, 0.90] (outside suggests calibration issue)
- Purification report exists and non-empty

#### Step 3: IRT Pass 2
**Analysis Tool:** (determined by rq_tools - likely tools.analysis_irt.calibrate_irt with GRM on purified items)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_irt_convergence + validate_numeric_range)

**What Validation Checks:**
- Model converged successfully
- Theta in [-4,4], SE in [0.1,1.5] (tighter than Pass 1)
- All 400 composite_IDs present (no data loss)
- Item count matches Step 2 purified_items.csv
- SE improvement vs Pass 1 (median SE reduced)

#### Step 4: Merge Theta with TSVR
**Analysis Tool:** (determined by rq_tools - likely pandas merge + reshape operations)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure)

**What Validation Checks:**
- Exactly 1200 rows (400 composite_IDs x 3 congruence levels)
- Each composite_ID appears exactly 3 times
- Each UID appears 12 times (4 tests x 3 congruence)
- No NaN in TSVR_hours, theta_confidence, se_confidence
- Congruence factor has exactly 3 categories

#### Step 5: Fit LMM
**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.fit_lmm_trajectory_tsvr)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_lmm_convergence + validate_lmm_assumptions_comprehensive)

**What Validation Checks:**
- Model converged (convergence flag True)
- All fixed effects terms present (intercept, 2 congruence, time, 2 interactions)
- Random effects variances > 0 (intercept + slope)
- p-values in [0,1]
- No singular fit (if present, WARNING not error)

#### Step 6: Post-Hoc Contrasts
**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.compute_contrasts_pairwise)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_contrasts_d068)

**What Validation Checks:**
- If contrasts computed: BOTH p-value columns present (p_uncorrected, p_bonferroni per Decision D068)
- p_bonferroni >= p_uncorrected (correction must increase p-value)
- All 3 pairwise contrasts present (if any rows)
- Effect sizes in reasonable range (cohens_d in [-2,2])

#### Step 7: Prepare Plot Data
**Analysis Tool:** (determined by rq_tools - likely pandas groupby + transform operations)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_plot_data_completeness + validate_probability_range)

**What Validation Checks:**
- Both theta and probability files created (Decision D069)
- All 3 congruence levels present
- All 4 timepoints present
- Row counts match between files
- theta in [-4,4], probability in [0,1]
- CI_upper > CI_lower for all rows
- No NaN values

---

## Summary

**Total Steps:** 8 (Step 0: extraction + Steps 1-7: analysis)
**Estimated Runtime:** 60-90 minutes (dominated by two GRM calibrations ~30-60 min each)
**Cross-RQ Dependencies:** None (RAW data only from dfData.csv)
**Primary Outputs:**
- data/step03_theta_confidence_congruence.csv (FINAL theta estimates, 400 rows x 7 cols)
- data/step05_lmm_model_summary.txt (Schema x Time interaction test)
- data/step06_post_hoc_contrasts.csv (pairwise comparisons if effects detected, with dual p-values per Decision D068)
- data/step07_trajectory_theta_data.csv + data/step07_trajectory_probability_data.csv (plot source CSVs for Decision D069 dual-scale plotting)

**Validation Coverage:** 100% (all 8 steps have validation requirements with 4-layer substance criteria)

**Key Hypotheses:**
- **Primary (NULL expected):** Schema x Time interaction p > 0.05 (congruence does NOT affect confidence decline rate, paralleling Ch5 5.4.1 accuracy findings)
- **Secondary (exploratory):** Congruence main effect on baseline may be significant (p < 0.05) if fluency heuristic biases initial confidence ratings for schema-congruent items

**Comparison Context:**
- Results will be compared to Ch5 5.4.1 (accuracy trajectories)
- If confidence shows effects where accuracy showed NULL: Evidence of metacognitive bias (schema affects subjective experience but not objective performance)
- If both NULL: Schema-neutral consolidation for both accuracy and confidence in immersive VR

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent for RQ 6.5.1
