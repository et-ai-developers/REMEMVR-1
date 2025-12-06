# Analysis Plan for RQ 6.1.1: Functional Form Comparison for Confidence Decline

**Created by:** rq_planner agent
**Date:** 2025-12-06
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This RQ determines the optimal functional form for modeling confidence decline trajectories over a 6-day retention interval. Analysis parallels Ch5 RQ 5.1.1 (accuracy functional form) to test whether metacognitive confidence monitoring tracks memory accuracy decay patterns. Uses 5-category ordinal Likert confidence ratings (TC_* items: 0, 0.25, 0.5, 0.75, 1.0) from interactive VR paradigms (IFR, ICR, IRE) across all memory domains (omnibus "All" factor).

**Pipeline:** IRT (Graded Response Model for polytomous data) -> LMM (5 candidate functional forms) -> Model Selection (AIC comparison)

**Steps:** 8 total analysis steps (Step 0: data extraction + Steps 1-7: analysis)

**Estimated Runtime:** High complexity (90-120 minutes total)
- Step 0: Low (5 min - data extraction)
- Step 1: High (60 min - GRM calibration Pass 1, 5-category ordinal model)
- Step 2: Low (5 min - item purification)
- Step 3: High (60 min - GRM calibration Pass 2)
- Step 4: Low (5 min - TSVR merge)
- Step 5: Medium (30 min - fit 5 LMM candidates)
- Step 6: Low (10 min - AIC comparison, Akaike weights)
- Step 7: Low (10 min - compare to Ch5 5.1.1 accuracy results)

**Key Decisions Applied:**
- Decision D039: 2-pass IRT purification (mandatory for all IRT analyses)
- Decision D070: TSVR as LMM time variable (actual hours, not nominal days)
- Decision D069: NOT applicable (no trajectory plots in this RQ - model selection only)
- Decision D068: NOT applicable (no group comparisons in this RQ)

**Critical Note on GRM:**
TC_* confidence items are 5-category ordinal (0, 0.25, 0.5, 0.75, 1.0), NOT dichotomous like TQ_* accuracy items. This REQUIRES Graded Response Model (GRM) for polytomous ordered responses. Using 2PL (dichotomous model) would be INCORRECT and violate measurement assumptions.

---

## Analysis Plan

### Step 0: Extract Confidence Data from dfData.csv

**Dependencies:** None (first step, extracts from RAW source)
**Complexity:** Low (5 minutes - data extraction only, no modeling)

**Purpose:** Extract 5-category ordinal confidence ratings (TC_* items) from dfData.csv for omnibus "All" factor analysis. Create IRT input (wide format), TSVR mapping (time variable per Decision D070), and Q-matrix (single factor structure).

**Input:**

**File:** data/cache/dfData.csv (project-level RAW data source)

**Required Columns:**
- `UID` (string, format: P### with leading zeros, e.g., P001)
- `TEST` (string, values: T1/T2/T3/T4 for Days 0/1/3/6)
- TC_* columns (5-category ordinal: 0, 0.25, 0.5, 0.75, 1.0)
- TSVR (float, hours since VR encoding per Decision D070)

**Filters:**
- Paradigm codes: IFR, ICR, IRE (interactive paradigms only)
- Exclude: RFR, TCR, RRE (room paradigms excluded per 1_concept.md)
- Items: All TC_* confidence rating columns
- Participants: All 100 participants (no exclusions)
- Tests: All 4 tests (T1, T2, T3, T4)

**Expected Data Volume:**
- 100 participants x 4 tests = 400 rows (observations)
- Estimated ~102 TC_* items (varies by domain coverage)

**Processing:**

1. Load dfData.csv from data/cache/
2. Filter to TC_* columns (confidence ratings)
3. Filter to interactive paradigms (IFR, ICR, IRE)
4. Create composite_ID = UID + "_" + TEST (format: P001_T1)
5. Pivot to wide format: composite_ID x TC_* items
6. Extract TSVR_hours mapping: composite_ID -> TSVR
7. Create Q-matrix: single "All" factor (all TC_* items load on one dimension)

**Output:**

**File 1:** data/step00_irt_input.csv
**Format:** CSV, wide format (one row per composite_ID)
**Columns:**
  - `composite_ID` (string, format: UID_TEST, e.g., P001_T1)
  - One column per TC_* item (e.g., TC_IFR_OBJ_F, TC_ICR_LOC_N, ...)
  - Values: {0, 0.25, 0.5, 0.75, 1.0, NaN} (5-category ordinal + missing)
**Expected Rows:** 400 (100 participants x 4 tests)
**Expected Columns:** ~103 (composite_ID + ~102 TC_* items)

**File 2:** data/step00_tsvr_mapping.csv
**Format:** CSV with composite_ID -> TSVR hours mapping
**Columns:**
  - `composite_ID` (string)
  - `TSVR_hours` (float, actual hours since encoding per Decision D070)
  - `test` (string, values: T1/T2/T3/T4)
**Expected Rows:** 400
**Note:** Decision D070 requires TSVR (actual time) NOT nominal days (0/1/3/6)

**File 3:** data/step00_q_matrix.csv
**Format:** CSV with item x factor loading structure
**Columns:**
  - `item_name` (string, TC_* item codes)
  - `All` (int, values: 1 for all items - single omnibus factor)
**Expected Rows:** ~102 items
**Note:** Single-factor Q-matrix (omnibus "All" factor, no domain separation)

**Validation Requirement:**
Validation tools MUST be used after data extraction tool execution. Specific validation tools will be determined by rq_tools based on data extraction validation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_irt_input.csv: 400 rows x ~103 columns (composite_ID + ~102 items)
- data/step00_tsvr_mapping.csv: 400 rows x 3 columns (composite_ID, TSVR_hours, test)
- data/step00_q_matrix.csv: ~102 rows x 2 columns (item_name, All)
- All files: UTF-8 encoding, CSV format

*Value Ranges:*
- TC_* items in {0, 0.25, 0.5, 0.75, 1.0} OR NaN (5-category ordinal + missing)
- TSVR_hours in [0, 168] hours (0=encoding, 168=1 week max)
- Q-matrix "All" column: all values = 1 (single factor, all items load)

*Data Quality:*
- No fully missing items (every TC_* column must have >0 valid responses)
- No fully missing participants (every composite_ID must have >0 valid items)
- Missing data acceptable: <50% per item (>50% suggests extraction error)
- Expected N: Exactly 400 composite_IDs (100 UID x 4 tests, no exclusions)
- No duplicate composite_IDs in irt_input or tsvr_mapping

*Log Validation:*
- Required pattern: "Extracted {N} TC_* items for {M} composite_IDs"
- Required pattern: "Created Q-matrix: 1 factor ('All'), {N} items"
- Required pattern: "TSVR mapping created: 400 rows"
- Forbidden patterns: "ERROR", "No TC_* items found", "Missing TSVR for UID"
- Acceptable warnings: "Item {name} has {X}% missing data" (if X < 50%)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 400 rows, found 387")
- Log failure to logs/step00_extract_vr_data.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause (missing participants, incorrect filters, TSVR gaps)

---

### Step 1: IRT Calibration Pass 1 (All Items, GRM)

**Dependencies:** Step 0 (requires irt_input.csv, q_matrix.csv)
**Complexity:** High (60 minutes - GRM calibration on 5-category ordinal data)

**Purpose:** Calibrate Graded Response Model (GRM) on all TC_* confidence items (Pass 1 of Decision D039 2-pass purification). GRM is appropriate for ordered polytomous responses (5 categories: 0, 0.25, 0.5, 0.75, 1.0). Extract item parameters (discrimination a, threshold b) for purification decision in Step 2.

**Critical Note:** GRM for polytomous data, NOT 2PL for dichotomous. Using 2PL would violate measurement assumptions for 5-category ordinal responses.

**Input:**

**File 1:** data/step00_irt_input.csv (from Step 0)
**Format:** Wide format (composite_ID x items)
**Expected:** 400 rows x ~103 columns
**Values:** {0, 0.25, 0.5, 0.75, 1.0, NaN}

**File 2:** data/step00_q_matrix.csv (from Step 0)
**Format:** Item x factor loadings
**Expected:** ~102 rows x 2 columns
**Note:** Single "All" factor (omnibus structure)

**Processing:**

1. Load irt_input.csv and q_matrix.csv
2. Configure GRM model with:
   - Model type: Graded Response Model (for 5-category ordinal)
   - Number of categories: 5 (0, 0.25, 0.5, 0.75, 1.0)
   - Number of dimensions: 1 (omnibus "All" factor)
   - Prior: p1_med (medium-strength prior for stability)
   - Max iterations: 50 (minimal settings testing first)
   - MC samples: 10, IW samples: 10 (minimal for testing)
3. Fit GRM via IWAVE variational inference
4. Extract item parameters: discrimination (a), thresholds (b1, b2, b3, b4) per item
5. Extract theta estimates (diagnostic, used for purification decisions)
6. Save item parameters and theta to CSV

**Note on Minimal Settings:**
Per Decision D039 and best practices, ALL IRT calibrations should test with minimal settings FIRST (max_iter=50, mc_samples=10, iw_samples=10) to validate pipeline in ~10 minutes before committing to production settings (max_iter=200, mc_samples=100, iw_samples=100) which take 60+ minutes. If minimal settings test passes validation, re-run with production settings.

**Output:**

**File 1:** data/step01_pass1_item_params.csv
**Format:** CSV with item parameters
**Columns:**
  - `item_name` (string, TC_* item codes)
  - `dimension` (string, "All" for all items)
  - `a` (float, discrimination parameter, must be > 0)
  - `b1`, `b2`, `b3`, `b4` (float, threshold parameters for 5-category model)
**Expected Rows:** ~102 items

**File 2:** data/step01_pass1_theta.csv
**Format:** CSV with theta estimates (diagnostic)
**Columns:**
  - `composite_ID` (string)
  - `theta_All` (float, latent ability estimate for omnibus factor)
  - `se_All` (float, standard error of theta)
**Expected Rows:** 400 (100 participants x 4 tests)

**Validation Requirement:**
Validation tools MUST be used after IRT calibration tool execution. Specific validation tools will be determined by rq_tools based on GRM calibration validation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_pass1_item_params.csv: ~102 rows x 6 columns (item_name, dimension, a, b1-b4)
- data/step01_pass1_theta.csv: 400 rows x 3 columns (composite_ID, theta_All, se_All)
- Data types: item_name (string), dimension (string), a/b*/theta/se (float64)

*Value Ranges:*
- Discrimination a in [0.01, 10.0] (>10.0 suggests estimation error, 0 impossible)
- Thresholds b1-b4: unrestricted but typically in [-6, 6] (extreme values flag misfit)
- Theta in [-4, 4] (outside suggests poor calibration or extreme responders)
- SE in [0.1, 1.5] (above 1.5 = unreliable, below 0.1 = suspicious)

*Data Quality:*
- No NaN in item parameters (all items must estimate, NaN = convergence failure)
- No NaN in theta (all composite_IDs must estimate)
- All ~102 items present in item_params (no items dropped silently)
- Expected N: 400 composite_IDs in theta file (no participant loss)
- Threshold ordering: b1 < b2 < b3 < b4 for all items (GRM constraint)

*Log Validation:*
- Required pattern: "Model converged: True"
- Required pattern: "VALIDATION - PASS: theta range" (from validation tool)
- Required pattern: "Calibration complete: {N} items, {M} participants"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "NaN parameters detected"
- Acceptable warnings: "Item {name} has extreme difficulty b > 3.0" (expected for some temporal items)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Item TC_IFR_OBJ_F has NaN discrimination")
- Log failure to logs/step01_irt_calibration_pass1.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose (common causes: insufficient data, model misspecification, need more iterations)

---

### Step 2: Purify Items (Decision D039 Thresholds)

**Dependencies:** Step 1 (requires pass1_item_params.csv)
**Complexity:** Low (5 minutes - filtering based on thresholds, no modeling)

**Purpose:** Apply Decision D039 purification thresholds to exclude poorly performing items. Retention criteria: |b| <= 3.0 (threshold parameter magnitude) AND a >= 0.4 (discrimination). Expected 30-70% item retention (temporal items difficult, may have |b| > 3.0).

**Note on GRM Purification:**
For GRM with 4 thresholds (b1-b4), purification evaluates MEAN threshold |b_mean| = |mean(b1, b2, b3, b4)| against 3.0 cutoff. This differs from 2PL which has single difficulty parameter b.

**Input:**

**File:** data/step01_pass1_item_params.csv (from Step 1)
**Columns:** item_name, dimension, a, b1, b2, b3, b4
**Expected Rows:** ~102 items

**Processing:**

1. Load pass1_item_params.csv
2. Compute b_mean = mean(b1, b2, b3, b4) for each item
3. Compute |b_mean| (absolute value)
4. Apply thresholds:
   - Retain if: a >= 0.4 (sufficient discrimination)
   - Retain if: |b_mean| <= 3.0 (reasonable difficulty)
   - Exclude if EITHER threshold violated
5. Create retained_items list (item_name values that passed)
6. Create exclusion_report (item_name, reason: "Low discrimination" or "Extreme difficulty")
7. Compute retention rate (retained / total)
8. Save retained items and exclusion report

**Output:**

**File 1:** data/step02_purified_items.csv
**Format:** CSV with list of retained item names
**Columns:**
  - `item_name` (string, TC_* item codes that passed thresholds)
**Expected Rows:** 30-70% of ~102 items (31-71 items approximately)

**File 2:** data/step02_purification_report.txt
**Format:** Plain text report
**Content:**
  - Total items evaluated: {N}
  - Items retained: {M} ({M/N}% retention rate)
  - Items excluded: {N-M}
  - Exclusion reasons:
    - Low discrimination (a < 0.4): {count}
    - Extreme difficulty (|b_mean| > 3.0): {count}
  - List of excluded items with reasons

**Validation Requirement:**
Validation tools MUST be used after item purification tool execution. Specific validation tools will be determined by rq_tools based on purification validation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_purified_items.csv: 31-71 rows x 1 column (item_name)
- data/step02_purification_report.txt: exists, >0 bytes, UTF-8 text

*Value Ranges:*
- Retention rate in [0.30, 0.70] (30-70% per Decision D039 expectations)
- No negative counts in report
- Exclusion reasons sum to total excluded count

*Data Quality:*
- All retained items must exist in step01_pass1_item_params.csv (no invented items)
- No duplicate item_name in purified_items.csv
- Expected N: 31-71 items (if <30% or >70%, flag as unusual but not error)
- Report must list ALL excluded items (count matches total - retained)

*Log Validation:*
- Required pattern: "Purification complete: {M} items retained ({X}%)"
- Required pattern: "Excluded {N} items: {A} low discrimination, {B} extreme difficulty"
- Forbidden patterns: "ERROR", "No items retained", "Retention rate 0%"
- Acceptable warnings: "Retention rate {X}% outside expected 30-70% range" (flag for review)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Retention rate 12% below expected 30% minimum")
- Log failure to logs/step02_purify_items.log
- Quit script immediately (do NOT proceed to Step 3)
- g_debug invoked to diagnose (common causes: overly strict thresholds, poor Pass 1 calibration, insufficient data quality)

---

### Step 3: IRT Calibration Pass 2 (Purified Items, GRM)

**Dependencies:** Step 2 (requires purified_items.csv), Step 0 (requires irt_input.csv)
**Complexity:** High (60 minutes - GRM recalibration on purified item set)

**Purpose:** Re-calibrate GRM on purified items only (Pass 2 of Decision D039). Extract final theta_confidence scores (ability estimates on latent confidence trait) for LMM trajectory analysis in Step 4-5.

**Input:**

**File 1:** data/step00_irt_input.csv (from Step 0)
**Format:** Wide format (composite_ID x all items)
**Expected:** 400 rows x ~103 columns

**File 2:** data/step02_purified_items.csv (from Step 2)
**Format:** List of retained item names
**Expected:** 31-71 rows x 1 column

**Processing:**

1. Load irt_input.csv (all items)
2. Load purified_items.csv (retained item names)
3. Filter irt_input to retained items only (subset columns)
4. Create Q-matrix for retained items (single "All" factor)
5. Configure GRM model (same settings as Step 1)
6. Fit GRM on purified items
7. Extract final theta_confidence and SE for all composite_IDs
8. Extract final item parameters (for documentation/reporting)
9. Save theta and item parameters to CSV

**Output:**

**File 1:** data/step03_theta_confidence.csv
**Format:** CSV with final ability estimates
**Columns:**
  - `composite_ID` (string)
  - `theta_All` (float, final confidence ability estimate)
  - `se_All` (float, standard error of theta)
**Expected Rows:** 400 (100 participants x 4 tests)

**File 2:** data/step03_item_parameters.csv
**Format:** CSV with final item parameters (Pass 2)
**Columns:**
  - `item_name` (string, TC_* retained items only)
  - `dimension` (string, "All")
  - `a` (float, discrimination)
  - `b1`, `b2`, `b3`, `b4` (float, thresholds)
**Expected Rows:** 31-71 items (matches purified_items.csv row count)

**Validation Requirement:**
Validation tools MUST be used after IRT calibration tool execution. Specific validation tools will be determined by rq_tools based on GRM calibration validation requirements (same as Step 1).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_theta_confidence.csv: 400 rows x 3 columns (composite_ID, theta_All, se_All)
- data/step03_item_parameters.csv: 31-71 rows x 6 columns (item_name, dimension, a, b1-b4)
- Data types: composite_ID/item_name/dimension (string), theta/se/a/b* (float64)

*Value Ranges:*
- Theta in [-4, 4] (outside suggests poor calibration)
- SE in [0.1, 1.5] (above 1.5 = unreliable)
- Discrimination a in [0.01, 10.0] (>10.0 = estimation error)
- Thresholds b1-b4: unrestricted but typically in [-6, 6]
- Threshold ordering: b1 < b2 < b3 < b4 for all items

*Data Quality:*
- No NaN in theta_confidence.csv (all composite_IDs must estimate)
- No NaN in item_parameters.csv (all items must estimate)
- Expected N: 400 composite_IDs (no participant loss from Pass 1 to Pass 2)
- Item count matches purified_items.csv (no silent item loss)
- Improved fit vs Pass 1 (compare convergence metrics if available)

*Log Validation:*
- Required pattern: "Model converged: True"
- Required pattern: "VALIDATION - PASS: theta range"
- Required pattern: "Pass 2 calibration complete: {N} items, 400 participants"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "NaN parameters"
- Acceptable warnings: None expected for Pass 2 (purified items should calibrate cleanly)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Theta estimates contain NaN for composite_ID P001_T1")
- Log failure to logs/step03_irt_calibration_pass2.log
- Quit script immediately (do NOT proceed to Step 4)
- g_debug invoked to diagnose (common causes: purification too aggressive, insufficient data, model misspecification)

---

### Step 4: Merge Theta with TSVR (Decision D070)

**Dependencies:** Step 3 (requires theta_confidence.csv), Step 0 (requires tsvr_mapping.csv)
**Complexity:** Low (5 minutes - data merge and transformations, no modeling)

**Purpose:** Merge theta_confidence scores with TSVR time variable (Decision D070: actual hours since encoding, NOT nominal days). Create time transformations for 5 candidate LMM models: Days = TSVR_hours / 24, Days_squared, log_Days_plus1 = log(Days + 1).

**Input:**

**File 1:** data/step03_theta_confidence.csv (from Step 3)
**Columns:** composite_ID, theta_All, se_All
**Expected Rows:** 400

**File 2:** data/step00_tsvr_mapping.csv (from Step 0)
**Columns:** composite_ID, TSVR_hours, test
**Expected Rows:** 400

**Processing:**

1. Load theta_confidence.csv
2. Load tsvr_mapping.csv
3. Merge on composite_ID (left join - keep all theta rows)
4. Verify all composite_IDs matched (no missing TSVR)
5. Create time transformations:
   - Days = TSVR_hours / 24
   - Days_squared = Days^2
   - log_Days_plus1 = log(Days + 1) (log(0+1)=0, handles Day 0)
6. Extract UID from composite_ID (split on "_", take first part)
7. Save merged data to CSV

**Note on Decision D070:**
TSVR_hours (actual elapsed time) is used instead of nominal days (0/1/3/6) because test sessions vary by hours/days depending on participant scheduling. Using actual time provides more accurate temporal modeling.

**Output:**

**File:** data/step04_lmm_input.csv
**Format:** CSV, long format (one row per observation)
**Columns:**
  - `composite_ID` (string, format: UID_TEST)
  - `UID` (string, participant identifier, e.g., P001)
  - `test` (string, values: T1/T2/T3/T4)
  - `theta_All` (float, confidence ability estimate)
  - `se_All` (float, standard error)
  - `TSVR_hours` (float, actual hours since encoding)
  - `Days` (float, TSVR_hours / 24)
  - `Days_squared` (float, Days^2)
  - `log_Days_plus1` (float, log(Days + 1))
**Expected Rows:** 400 (100 participants x 4 tests)

**Validation Requirement:**
Validation tools MUST be used after TSVR merge tool execution. Specific validation tools will be determined by rq_tools based on data merge validation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_lmm_input.csv: 400 rows x 9 columns (composite_ID, UID, test, theta_All, se_All, TSVR_hours, Days, Days_squared, log_Days_plus1)
- Data types: composite_ID/UID/test (string), all others (float64)

*Value Ranges:*
- TSVR_hours in [0, 168] hours (0=encoding, 168=1 week max)
- Days in [0, 7] (TSVR_hours / 24)
- Days_squared in [0, 49] (Days^2, max = 7^2)
- log_Days_plus1 in [0, 2.08] (log(7+1) = 2.08 max)
- theta_All in [-4, 4], se_All in [0.1, 1.5] (inherited from Step 3)

*Data Quality:*
- No NaN in any column (all theta rows must have matched TSVR)
- Expected N: Exactly 400 rows (no data loss from merge)
- No duplicate composite_IDs
- Test values: Only {T1, T2, T3, T4} (no unexpected test codes)
- UID count: 100 unique UIDs (all participants present)

*Log Validation:*
- Required pattern: "Merge complete: 400 theta scores matched with TSVR"
- Required pattern: "Created time transformations: Days, Days_squared, log_Days_plus1"
- Required pattern: "No missing TSVR values - all composite_IDs matched"
- Forbidden patterns: "ERROR", "Missing TSVR for composite_ID", "NaN values detected"
- Acceptable warnings: None expected for clean merge

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Missing TSVR for composite_ID P001_T1")
- Log failure to logs/step04_merge_theta_tsvr.log
- Quit script immediately (do NOT proceed to Step 5)
- g_debug invoked to diagnose (common causes: composite_ID mismatch between theta and TSVR, missing TSVR data)

---

### Step 5: Fit 5 Candidate LMM Models (Model Comparison)

**Dependencies:** Step 4 (requires lmm_input.csv with time transformations)
**Complexity:** Medium (30 minutes - fit 5 LMM models, compare by AIC)

**Purpose:** Fit 5 candidate functional forms for confidence decline trajectory. Use REML=False for model comparison (enables AIC comparison across models with different fixed effects). Models: Linear, Quadratic, Logarithmic, Linear+Logarithmic, Quadratic+Logarithmic. All include random intercepts and slopes by participant (UID).

**Input:**

**File:** data/step04_lmm_input.csv (from Step 4)
**Columns:** composite_ID, UID, test, theta_All, se_All, TSVR_hours, Days, Days_squared, log_Days_plus1
**Expected Rows:** 400

**Processing:**

1. Load lmm_input.csv
2. Define 5 candidate model formulas (using statsmodels MixedLM syntax):
   - Model 1 (Linear): theta_All ~ Days, random intercepts + slopes by UID
   - Model 2 (Quadratic): theta_All ~ Days + Days_squared, random intercepts + slopes by UID
   - Model 3 (Logarithmic): theta_All ~ log_Days_plus1, random intercepts + slopes by UID
   - Model 4 (Linear+Logarithmic): theta_All ~ Days + log_Days_plus1, random intercepts + slopes by UID
   - Model 5 (Quadratic+Logarithmic): theta_All ~ Days + Days_squared + log_Days_plus1, random intercepts + slopes by UID
3. Fit each model with REML=False (enables AIC comparison)
4. Extract fit statistics for each model:
   - AIC (Akaike Information Criterion)
   - BIC (Bayesian Information Criterion)
   - Log-likelihood
   - Number of parameters
   - Convergence status
5. Save model comparison table to CSV
6. Save each fitted model object to pickle (for potential post-hoc analysis)

**Note on Random Effects Structure:**
All models use maximal random effects structure (random intercepts + random slopes for all time predictors by UID). This accounts for participant-level variation in baseline confidence and decline rates.

**Output:**

**File 1:** data/step05_model_comparison.csv
**Format:** CSV with model fit statistics
**Columns:**
  - `model_name` (string, values: Linear, Quadratic, Logarithmic, Linear+Logarithmic, Quadratic+Logarithmic)
  - `AIC` (float, Akaike Information Criterion - lower is better)
  - `BIC` (float, Bayesian Information Criterion - lower is better)
  - `log_likelihood` (float, log-likelihood)
  - `num_params` (int, number of parameters estimated)
  - `converged` (bool, convergence status)
**Expected Rows:** 5 (one per model)

**File 2:** data/step05_model1_linear.pkl (and model2-5.pkl)
**Format:** Python pickle file with fitted statsmodels MixedLM object
**Note:** One pickle per model for potential post-hoc analysis

**Validation Requirement:**
Validation tools MUST be used after LMM fitting tool execution. Specific validation tools will be determined by rq_tools based on LMM fit validation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_model_comparison.csv: 5 rows x 6 columns (model_name, AIC, BIC, log_likelihood, num_params, converged)
- data/step05_model1_linear.pkl through model5_quadratic_logarithmic.pkl (5 files)
- Data types: model_name (string), AIC/BIC/log_likelihood (float64), num_params (int), converged (bool)

*Value Ranges:*
- AIC: finite values (not NaN, not Inf)
- BIC: finite values
- log_likelihood: negative values (typically -200 to -600 for this data scale)
- num_params: reasonable counts (5-15 parameters typical for these models)
- converged: all TRUE (all 5 models must converge)

*Data Quality:*
- Expected N: Exactly 5 rows (one per model)
- All models converged=True (no convergence failures)
- No NaN in AIC, BIC, log_likelihood columns
- AIC values differ across models (not all identical)
- Model names: exact set {Linear, Quadratic, Logarithmic, Linear+Logarithmic, Quadratic+Logarithmic}

*Log Validation:*
- Required pattern: "Fitted 5 candidate models successfully"
- Required pattern: "All models converged: True"
- Required pattern: "Model comparison saved to step05_model_comparison.csv"
- Forbidden patterns: "ERROR", "Model {name} failed to converge", "NaN AIC detected"
- Acceptable warnings: "Model {name} took {N} iterations to converge" (if N reasonable)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Model Quadratic failed to converge")
- Log failure to logs/step05_fit_lmm.log
- Quit script immediately (do NOT proceed to Step 6)
- g_debug invoked to diagnose (common causes: insufficient data, random effects too complex, scaling issues)

---

### Step 6: Select Best Model via AIC (Akaike Weights)

**Dependencies:** Step 5 (requires model_comparison.csv)
**Complexity:** Low (10 minutes - compute AIC weights and select best model)

**Purpose:** Compute Akaike weights (model probabilities) from AIC values. Identify best model (lowest AIC, highest Akaike weight). Save best model and comparison results. Akaike weight > 0.30 indicates clear winner (per 1_concept.md success criteria).

**Input:**

**File:** data/step05_model_comparison.csv (from Step 5)
**Columns:** model_name, AIC, BIC, log_likelihood, num_params, converged
**Expected Rows:** 5

**Processing:**

1. Load model_comparison.csv
2. Compute delta_AIC = AIC - min(AIC) for each model
3. Compute relative likelihood = exp(-0.5 * delta_AIC)
4. Compute Akaike weights = relative_likelihood / sum(relative_likelihood)
5. Identify best model (lowest AIC, highest weight)
6. Verify Akaike weights sum to 1.0 +/- 0.01
7. Save AIC comparison table with weights
8. Copy best model pickle to canonical name (step06_best_model.pkl)

**Output:**

**File 1:** data/step06_aic_comparison.csv
**Format:** CSV with AIC comparison results
**Columns:**
  - `model_name` (string)
  - `AIC` (float)
  - `delta_AIC` (float, AIC - min(AIC))
  - `relative_likelihood` (float, exp(-0.5 * delta_AIC))
  - `akaike_weight` (float, model probability)
  - `is_best` (bool, True for model with lowest AIC)
**Expected Rows:** 5
**Note:** Rows sorted by AIC ascending (best model first)

**File 2:** data/step06_best_model.pkl
**Format:** Python pickle file (copy of best model from Step 5)
**Note:** Canonical filename for downstream use

**Validation Requirement:**
Validation tools MUST be used after model selection tool execution. Specific validation tools will be determined by rq_tools based on model selection validation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_aic_comparison.csv: 5 rows x 6 columns (model_name, AIC, delta_AIC, relative_likelihood, akaike_weight, is_best)
- data/step06_best_model.pkl: exists, >0 bytes
- Data types: model_name (string), AIC/delta_AIC/relative_likelihood/akaike_weight (float64), is_best (bool)

*Value Ranges:*
- AIC: finite values (inherited from Step 5)
- delta_AIC in [0, Inf) (best model has delta_AIC=0)
- relative_likelihood in (0, 1] (best model has relative_likelihood=1)
- akaike_weight in (0, 1) (probabilities)
- Akaike weights sum to 1.0 +/- 0.01 (probability constraint)

*Data Quality:*
- Expected N: Exactly 5 rows
- Exactly one row with is_best=True (unique best model)
- Best model has delta_AIC=0 (by definition)
- Best model has highest akaike_weight
- Rows sorted by AIC ascending (best first)

*Log Validation:*
- Required pattern: "Best model: {model_name} (AIC={AIC}, weight={weight})"
- Required pattern: "Akaike weights sum: {sum} (expected 1.0)"
- Required pattern: "Best model weight: {weight} (>0.30 = clear winner)"
- Forbidden patterns: "ERROR", "Akaike weights sum != 1.0", "No best model identified"
- Acceptable warnings: "Best model weight {weight} < 0.30 (no clear winner)" (flag for review)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Akaike weights sum to 0.87, expected 1.0")
- Log failure to logs/step06_select_best_model.log
- Quit script immediately (do NOT proceed to Step 7)
- g_debug invoked to diagnose (common causes: AIC computation error, numerical precision issues)

---

### Step 7: Compare to Ch5 5.1.1 Accuracy Model Selection

**Dependencies:** Step 6 (requires aic_comparison.csv), Ch5 RQ 5.1.1 (requires results/ch5/5.1.1/data/step06_aic_comparison.csv)
**Complexity:** Low (10 minutes - cross-RQ comparison, no modeling)

**Purpose:** Compare confidence functional form (this RQ) to accuracy functional form (Ch5 RQ 5.1.1) to test if metacognitive monitoring tracks memory decay. If both show same best model (e.g., Logarithmic), suggests confidence parallels accuracy. If divergent, suggests dissociable memory vs metacognition systems.

**Input:**

**File 1:** data/step06_aic_comparison.csv (from Step 6, this RQ)
**Columns:** model_name, AIC, delta_AIC, relative_likelihood, akaike_weight, is_best
**Expected Rows:** 5

**File 2:** results/ch5/5.1.1/data/step06_aic_comparison.csv (from Ch5 RQ 5.1.1)
**Columns:** Same structure as File 1
**Expected Rows:** 5
**Note:** Ch5 5.1.1 must be complete before this step runs

**Processing:**

1. Load this RQ's aic_comparison.csv (confidence)
2. Load Ch5 5.1.1 aic_comparison.csv (accuracy)
3. Extract best model for each:
   - Confidence best model: model_name where is_best=True
   - Accuracy best model: model_name where is_best=True
4. Compare Akaike weights for each model across RQs
5. Create comparison table:
   - Rows: 5 model names
   - Columns: confidence_weight, accuracy_weight, weight_difference
6. Document conclusion:
   - If same best model: "Confidence parallels accuracy ({model_name})"
   - If different best models: "Confidence diverges from accuracy (Conf={X}, Acc={Y})"
7. Save comparison table to CSV

**Output:**

**File:** data/step07_ch5_comparison.csv
**Format:** CSV with cross-RQ model comparison
**Columns:**
  - `model_name` (string)
  - `confidence_weight` (float, Akaike weight from this RQ)
  - `accuracy_weight` (float, Akaike weight from Ch5 5.1.1)
  - `weight_difference` (float, confidence_weight - accuracy_weight)
  - `best_in_confidence` (bool, True if best model for confidence)
  - `best_in_accuracy` (bool, True if best model for accuracy)
**Expected Rows:** 5
**Note:** Comparison documents whether metacognitive monitoring (confidence) tracks memory decay (accuracy)

**Validation Requirement:**
Validation tools MUST be used after cross-RQ comparison tool execution. Specific validation tools will be determined by rq_tools based on comparison validation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_ch5_comparison.csv: 5 rows x 6 columns (model_name, confidence_weight, accuracy_weight, weight_difference, best_in_confidence, best_in_accuracy)
- Data types: model_name (string), weights/difference (float64), best_in_* (bool)

*Value Ranges:*
- confidence_weight in (0, 1) (probabilities from Step 6)
- accuracy_weight in (0, 1) (probabilities from Ch5 5.1.1)
- weight_difference in (-1, 1) (difference of probabilities)
- Confidence weights sum to 1.0 +/- 0.01
- Accuracy weights sum to 1.0 +/- 0.01

*Data Quality:*
- Expected N: Exactly 5 rows (one per model)
- Exactly one row with best_in_confidence=True
- Exactly one row with best_in_accuracy=True
- Model names: exact set {Linear, Quadratic, Logarithmic, Linear+Logarithmic, Quadratic+Logarithmic}
- No NaN values in any column

*Log Validation:*
- Required pattern: "Comparison complete: Confidence best={X}, Accuracy best={Y}"
- Required pattern: "Confidence weights from step06_aic_comparison.csv (sum={sum})"
- Required pattern: "Accuracy weights from Ch5 5.1.1 step06_aic_comparison.csv (sum={sum})"
- Forbidden patterns: "ERROR", "File not found: Ch5 5.1.1", "Weight sum != 1.0"
- Acceptable warnings: "Ch5 5.1.1 incomplete - skipping comparison" (if dependency RQ not run yet)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Ch5 5.1.1 aic_comparison.csv not found")
- Log failure to logs/step07_compare_to_ch5.log
- Quit script immediately
- g_debug invoked to diagnose (common causes: Ch5 5.1.1 incomplete, file path incorrect, data format mismatch)

**Note on Dependency:**
If Ch5 RQ 5.1.1 has not been executed yet, this step should be skipped or flag a clear error. The comparison is informative but not critical for RQ 6.1.1 completion (primary goal is identifying best confidence model, not comparison to accuracy).

---

## Expected Data Formats

### Wide vs Long Format Transitions

**Step 0 Output (Wide Format):**
- data/step00_irt_input.csv: composite_ID x TC_* items (400 rows x ~103 columns)
- One row per observation (participant-test combination)
- Item responses in columns

**Steps 1-3 (IRT Pipeline):**
- Wide format maintained for IRT calibration
- GRM expects response matrix (participants x items)

**Step 4 Output (Long Format for LMM):**
- data/step04_lmm_input.csv: one row per observation (400 rows)
- Columns: composite_ID, UID, test, theta_All, se_All, TSVR_hours, Days, Days_squared, log_Days_plus1
- Long format suitable for repeated-measures LMM (UID as grouping variable)

### Column Naming Conventions

**Time Variables (Decision D070):**
- `TSVR_hours` (float): Actual hours since VR encoding (range: [0, 168])
- `Days` (float): TSVR_hours / 24 (range: [0, 7])
- `Days_squared` (float): Days^2 (range: [0, 49])
- `log_Days_plus1` (float): log(Days + 1) (range: [0, 2.08])

**Confidence Variables:**
- `theta_All` (float): IRT ability estimate for omnibus confidence factor (range: [-4, 4])
- `se_All` (float): Standard error of theta (range: [0.1, 1.5])

**Identifiers:**
- `composite_ID` (string): UID_TEST (e.g., P001_T1)
- `UID` (string): Participant identifier (e.g., P001)
- `test` (string): Test session (T1, T2, T3, T4)

**GRM Parameters (5-category ordinal model):**
- `a` (float): Discrimination parameter (>0, typically 0.4-4.0)
- `b1`, `b2`, `b3`, `b4` (float): Threshold parameters (ordered: b1 < b2 < b3 < b4)

### Data Type Constraints

**String columns (non-nullable):**
- composite_ID, UID, test, item_name, dimension, model_name

**Float columns (non-nullable after merge/calibration):**
- theta_All, se_All, TSVR_hours, Days, Days_squared, log_Days_plus1
- a, b1, b2, b3, b4 (GRM parameters)
- AIC, BIC, log_likelihood, akaike_weight

**Boolean columns:**
- converged, is_best, best_in_confidence, best_in_accuracy

**Integer columns:**
- num_params

---

## Cross-RQ Dependencies

### Dependency Type: Mixed (RAW + DERIVED)

**RAW Data:**
- data/cache/dfData.csv (project-level data source)
- All participants, tests, and TC_* confidence items extracted directly
- No dependencies on other RQs for primary analysis (Steps 0-6)

**DERIVED Data (Optional for Step 7):**
- **RQ 5.1.1** (Ch5 Accuracy Functional Form Comparison)
  - File: results/ch5/5.1.1/data/step06_aic_comparison.csv
  - Used in: Step 7 (cross-RQ model comparison)
  - Rationale: Compare confidence functional form to accuracy functional form to test if metacognitive monitoring tracks memory decay
  - Status: Optional (Step 7 can be skipped if Ch5 5.1.1 incomplete)

**Execution Order Constraint:**
- Steps 0-6: No dependencies (can execute independently)
- Step 7: Requires Ch5 RQ 5.1.1 complete (soft dependency - can skip if not available)

**Data Source Boundaries:**
- **RAW data:** dfData.csv TC_* columns extracted directly (Steps 0-6)
- **DERIVED data:** Ch5 5.1.1 AIC comparison (Step 7 only)
- **Scope:** This RQ performs full IRT calibration and LMM model selection independently

**Validation:**
- Step 7: Check results/ch5/5.1.1/data/step06_aic_comparison.csv exists before comparison
- If file missing: Log warning "Ch5 5.1.1 incomplete, skipping comparison" and quit Step 7 (not fatal error)

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

#### Step 0: Extract Confidence Data
**What Validation Checks:**
- Output files exist (irt_input.csv, tsvr_mapping.csv, q_matrix.csv)
- Expected column counts (irt_input: ~103, tsvr_mapping: 3, q_matrix: 2)
- Expected row counts (irt_input: 400, tsvr_mapping: 400, q_matrix: ~102)
- TC_* values in {0, 0.25, 0.5, 0.75, 1.0, NaN} (5-category ordinal + missing)
- TSVR_hours in [0, 168] (reasonable time range)
- No fully missing items or participants
- composite_ID format correct (UID_TEST pattern)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step00_extract_vr_data.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose extraction issues

---

#### Step 1: IRT Calibration Pass 1 (GRM)
**What Validation Checks:**
- Output files exist (pass1_item_params.csv, pass1_theta.csv)
- Model convergence achieved (from log output)
- Item parameters in valid ranges:
  - Discrimination a in [0.01, 10.0]
  - Thresholds b1-b4 typically in [-6, 6]
  - Threshold ordering: b1 < b2 < b3 < b4 (GRM constraint)
- Theta estimates in [-4, 4], SE in [0.1, 1.5]
- No NaN parameters (indicates estimation failure)
- Expected row counts (item_params: ~102, theta: 400)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step01_irt_calibration_pass1.log
- Quit script immediately
- g_debug invoked to diagnose calibration issues

---

#### Step 2: Purify Items
**What Validation Checks:**
- Output files exist (purified_items.csv, purification_report.txt)
- Retention rate in [0.30, 0.70] (expected range per Decision D039)
- All retained items exist in pass1_item_params.csv
- No duplicate item_name in purified_items.csv
- Exclusion reasons sum to total excluded count

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step02_purify_items.log
- Quit script immediately
- g_debug invoked to diagnose purification issues

---

#### Step 3: IRT Calibration Pass 2 (GRM)
**What Validation Checks:**
- Same as Step 1, plus:
- Item count matches purified_items.csv (no silent item loss)
- Improved fit vs Pass 1 (if metrics available)
- Expected row counts (item_params: 31-71, theta: 400)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step03_irt_calibration_pass2.log
- Quit script immediately
- g_debug invoked to diagnose recalibration issues

---

#### Step 4: Merge Theta with TSVR
**What Validation Checks:**
- Output file exists (lmm_input.csv)
- Expected columns present (9 total)
- Expected row count (400, no data loss from merge)
- No NaN in any column (all theta rows matched with TSVR)
- TSVR_hours in [0, 168], Days in [0, 7], etc.
- 100 unique UIDs present

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step04_merge_theta_tsvr.log
- Quit script immediately
- g_debug invoked to diagnose merge issues

---

#### Step 5: Fit 5 Candidate LMMs
**What Validation Checks:**
- Output files exist (model_comparison.csv, 5 pkl files)
- Expected row count (5 models)
- All models converged=True
- AIC, BIC, log_likelihood finite (not NaN/Inf)
- Model names match expected set

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step05_fit_lmm.log
- Quit script immediately
- g_debug invoked to diagnose LMM fitting issues

---

#### Step 6: Select Best Model via AIC
**What Validation Checks:**
- Output files exist (aic_comparison.csv, best_model.pkl)
- Expected row count (5 models)
- Exactly one is_best=True
- Akaike weights sum to 1.0 +/- 0.01
- Best model has delta_AIC=0

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step06_select_best_model.log
- Quit script immediately
- g_debug invoked to diagnose selection issues

---

#### Step 7: Compare to Ch5 5.1.1
**What Validation Checks:**
- Output file exists (ch5_comparison.csv)
- Expected row count (5 models)
- Confidence and accuracy weights sum to 1.0 +/- 0.01 separately
- Exactly one best_in_confidence=True, one best_in_accuracy=True
- Ch5 5.1.1 file exists (soft check - can skip if missing)

**Expected Behavior on Validation Failure:**
- If Ch5 file missing: Log warning and skip step (not fatal)
- If data validation fails: Raise error, log failure, quit
- g_debug invoked to diagnose comparison issues

---

## Summary

**Total Steps:** 8 (Step 0: extraction + Steps 1-7: analysis)

**Estimated Runtime:** 90-120 minutes total
- High complexity steps: 1, 3 (GRM calibration ~60 min each)
- Medium complexity steps: 5 (LMM fitting ~30 min)
- Low complexity steps: 0, 2, 4, 6, 7 (~5-10 min each)

**Cross-RQ Dependencies:**
- Primary analysis (Steps 0-6): None (RAW data only from dfData.csv)
- Comparison (Step 7): Ch5 RQ 5.1.1 (optional, soft dependency)

**Primary Outputs:**
- data/step03_theta_confidence.csv (400 confidence ability estimates)
- data/step06_best_model.pkl (best functional form LMM)
- data/step06_aic_comparison.csv (model selection results)
- data/step07_ch5_comparison.csv (confidence vs accuracy comparison)

**Validation Coverage:** 100% (all 8 steps have validation requirements with 4-layer substance criteria)

**Critical Success Criteria:**
- GRM calibration converges for 5-category ordinal data (NOT 2PL)
- Item purification retains 30-70% of items
- All 5 LMM models converge successfully
- Akaike weights sum to 1.0 +/- 0.01
- Best model identified with weight > 0.30 (clear winner)
- Comparison to Ch5 5.1.1 documents if confidence parallels accuracy

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent for RQ 6.1.1
