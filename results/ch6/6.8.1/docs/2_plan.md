# Analysis Plan for RQ 6.8.1: Source-Destination Confidence Trajectories

**Created by:** rq_planner agent
**Date:** 2025-12-06
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This RQ examines whether source (-U-/pick-up) and destination (-D-/put-down) locations show different confidence decline patterns over the 6-day retention interval. Using 5-category ordinal confidence data from TC_* items, we will test whether the source-destination dissociation found for accuracy in Ch5 5.5.1 replicates in metacognitive judgments.

**Analysis Pipeline:** IRT -> LMM with TSVR time variable

**Total Steps:** 8 (Step 0: data extraction + Steps 1-7: analysis/plotting)

**Estimated Runtime:** High (~90-120 minutes total - IRT calibration is most time-intensive)

**Key Decisions Applied:**
- Decision D039: 2-pass IRT purification (MANDATORY for all IRT)
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni for contrasts)
- Decision D069: Dual-scale trajectory plots (theta + probability scales)
- Decision D070: TSVR as time variable (actual hours, not nominal days)

**Critical Note:** This RQ uses 5-category ordinal confidence data (0, 0.25, 0.5, 0.75, 1.0), requiring GRM calibration. This is fundamentally different from binary accuracy data (0/1) which uses 2PL models.

---

## Analysis Plan

### Step 0: Extract Confidence Item Data

**Dependencies:** None (first step)
**Complexity:** Low (~2 minutes - data extraction only)

**Purpose:** Extract 5-category ordinal confidence responses for source (-U-) and destination (-D-) location items from dfData.csv.

**Input:**

**File:** data/cache/dfData.csv (project-level data source)

**Required Columns:**
- UID (participant identifier)
- TEST (test session: T1, T2, T3, T4)
- TC_* confidence items with -U- or -D- tags (5-category ordinal: 0, 0.25, 0.5, 0.75, 1.0)
- TSVR_hours (actual time since encoding in hours)

**Tag Patterns:**
- TC_*-U-* (source/pick-up location confidence items)
- TC_*-D-* (destination/put-down location confidence items)
- Excludes: TC_*-L-* (legacy general location), TQ_* (accuracy items)

**Extraction Filters:**
- All 100 participants
- All 4 test sessions (T1, T2, T3, T4)
- Only TC_* confidence items (NOT TQ_* accuracy items)
- Only -U- and -D- tags (exclude -L- legacy tags)

**Processing:**
1. Read dfData.csv
2. Filter to TC_* items matching -U- or -D- tags
3. Create wide-format IRT input (composite_ID x item columns)
4. Create Q-matrix for 2-factor GRM (Source dimension, Destination dimension)
5. Extract TSVR mapping (composite_ID, UID, TEST, TSVR_hours)
6. Save outputs to data/

**Output:**

**File 1:** data/step00_irt_input.csv
**Format:** CSV, wide format (one row per composite_ID)
**Columns:**
- composite_ID (string, format: UID_TEST, e.g., P001_T1)
- TC_*-U-* columns (5-category ordinal: 0, 0.25, 0.5, 0.75, 1.0)
- TC_*-D-* columns (5-category ordinal: 0, 0.25, 0.5, 0.75, 1.0)
**Expected Rows:** 400 (100 participants x 4 tests)
**Expected Columns:** ~50-60 (composite_ID + source items + destination items)

**File 2:** data/step00_q_matrix.csv
**Format:** CSV, Q-matrix defining factor structure
**Columns:**
- item_name (TC_* tag)
- Source (0 or 1 - loads on source dimension)
- Destination (0 or 1 - loads on destination dimension)
**Expected Rows:** ~50-60 items
**Note:** Each item loads on ONE dimension only (simple structure)

**File 3:** data/step00_tsvr_mapping.csv
**Format:** CSV, time mapping for LMM
**Columns:**
- composite_ID (string, matches IRT input)
- UID (participant identifier)
- TEST (test session)
- TSVR_hours (float, actual time since encoding)
**Expected Rows:** 400 (100 participants x 4 tests)

**Validation Requirement:**
Validation tools MUST be used after data extraction tool execution. Specific validation tools determined by rq_tools based on extraction format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_irt_input.csv exists (exact path)
- Expected rows: 400 (100 participants x 4 tests)
- Expected columns: 50-60 (composite_ID + TC items)
- Data types: composite_ID (object), TC items (float64 - ordinal 0/0.25/0.5/0.75/1.0)

*Value Ranges:*
- TC_* values in {0, 0.25, 0.5, 0.75, 1.0} ONLY (5-category ordinal - no intermediate values)
- TSVR_hours in [0, 168] hours (0=encoding, 168=1 week maximum)
- Missing data acceptable (<30% per item - confidence items may have more missingness than accuracy)

*Data Quality:*
- All 100 participants present (no data loss)
- All 4 test sessions represented
- composite_ID format correct (UID_TEST pattern)
- Q-matrix has no items loading on both dimensions (simple structure)
- At least 20 items per dimension (minimum for stable calibration)

*Log Validation:*
- Required pattern: "Extracted {N} source items, {M} destination items"
- Required pattern: "Created Q-matrix: 2 dimensions (Source, Destination)"
- Required pattern: "TSVR mapping: 400 observations"
- Forbidden patterns: "ERROR", "No items found", "Missing TSVR"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 400 rows, found 387")
- Log failure to logs/step00_extract_vr_data.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause

---

### Step 1: IRT Calibration Pass 1

**Dependencies:** Step 0 (requires extracted confidence item data)
**Complexity:** High (~40-60 minutes - GRM calibration with 5-category ordinal data)

**Purpose:** Calibrate 2-factor GRM model on all confidence items (before purification). This is Pass 1 of Decision D039 2-pass purification.

**CRITICAL:** Use Graded Response Model (GRM) for 5-category ordinal data (0, 0.25, 0.5, 0.75, 1.0), NOT 2PL which is for binary data. GRM estimates threshold parameters for category boundaries.

**Input:**

**File 1:** data/step00_irt_input.csv
**Format:** Wide format, 5-category ordinal responses
**Columns:** composite_ID + TC_* items (values in {0, 0.25, 0.5, 0.75, 1.0})

**File 2:** data/step00_q_matrix.csv
**Format:** Q-matrix, 2 dimensions (Source, Destination)

**Processing:**
1. Load IRT input and Q-matrix
2. Configure 2-factor GRM model with p1_med prior
3. Fit model using IWAVE variational inference algorithm
4. Extract item parameters (discrimination a, thresholds b1-b4 for 5 categories)
5. Extract theta estimates (source confidence, destination confidence)
6. Save outputs to data/

**GRM Model Specification:**
- **Factors:** 2 (Source, Destination)
- **Response Categories:** 5 (0, 0.25, 0.5, 0.75, 1.0)
- **Threshold Parameters:** 4 per item (b1, b2, b3, b4 - boundaries between categories)
- **Discrimination:** 1 per item (a - slope parameter)
- **Prior:** p1_med (regularization to prevent extreme parameter estimates)

**Output:**

**File 1:** data/step01_pass1_item_params.csv
**Format:** CSV, item parameters from Pass 1
**Columns:**
- item_name (TC_* tag)
- dimension (Source or Destination)
- a (discrimination parameter)
- b1, b2, b3, b4 (threshold parameters for 5-category GRM)
**Expected Rows:** ~50-60 items
**Note:** GRM has 4 thresholds per item (NOT single difficulty like 2PL)

**File 2:** data/step01_pass1_theta.csv
**Format:** CSV, ability estimates from Pass 1
**Columns:**
- composite_ID (matches input)
- theta_Source (source confidence ability)
- theta_Destination (destination confidence ability)
- se_Source (standard error for source)
- se_Destination (standard error for destination)
**Expected Rows:** 400 (100 participants x 4 tests)

**Validation Requirement:**
Validation tools MUST be used after IRT calibration tool execution. Specific validation tools determined by rq_tools based on GRM convergence and parameter range requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_pass1_item_params.csv exists (exact path)
- Expected rows: 50-60 items (all items calibrated)
- Expected columns: 7 (item_name, dimension, a, b1, b2, b3, b4)
- Data types: item_name (object), dimension (object), a/b (float64)

*Value Ranges:*
- a (discrimination) in [0.1, 10.0] (>10 suggests estimation error, <0.1 suggests non-discrimination)
- b1 < b2 < b3 < b4 (thresholds MUST be ordered for GRM)
- b thresholds typically in [-6, +6] (extreme values possible but rare)
- theta_Source in [-4, 4] (IRT ability estimates)
- theta_Destination in [-4, 4]
- se in [0.1, 2.0] (standard errors - above 2.0 = very unreliable)

*Data Quality:*
- All 400 observations have theta estimates (no NaN)
- No negative discrimination parameters (a > 0 required)
- Threshold ordering preserved (b1 < b2 < b3 < b4 for all items)
- At least 80% of items converged successfully

*Log Validation:*
- Required pattern: "Model converged: True"
- Required pattern: "GRM calibration complete: {N} items, 2 dimensions"
- Required pattern: "Threshold ordering validated: all items"
- Forbidden patterns: "ERROR", "Convergence failed", "Negative discrimination"
- Acceptable warnings: "Some threshold estimates extreme" (expected for difficult items)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Item TC_U_01 has b2 > b3 threshold reversal")
- Log failure to logs/step01_irt_calibration_pass1.log
- Quit script immediately
- g_debug invoked to diagnose (common causes: insufficient data, misspecified categories)

---

### Step 2: Purify Items (Decision D039)

**Dependencies:** Step 1 (requires Pass 1 item parameters)
**Complexity:** Low (~1 minute - filtering based on thresholds)

**Purpose:** Filter items by quality thresholds per Decision D039. Retain items with a >= 0.4 AND mean(|b1|, |b2|, |b3|, |b4|) <= 3.0.

**CRITICAL:** For GRM, difficulty threshold applies to MEAN of absolute threshold values, not single b parameter.

**Input:**

**File:** data/step01_pass1_item_params.csv
**Columns:** item_name, dimension, a, b1, b2, b3, b4

**Processing:**
1. Load Pass 1 item parameters
2. Compute mean_abs_b = mean(|b1|, |b2|, |b3|, |b4|) for each item
3. Apply thresholds:
   - Retain if: (a >= 0.4) AND (mean_abs_b <= 3.0)
   - Exclude otherwise
4. Create purified item list
5. Generate purification report (excluded items with reasons)
6. Save outputs to data/

**Thresholds (Decision D039):**
- **Minimum discrimination:** a >= 0.4 (items with a < 0.4 poorly discriminate ability levels)
- **Maximum mean difficulty:** mean(|b1|, |b2|, |b3|, |b4|) <= 3.0 (extreme items may cause estimation problems)

**Expected Retention Rate:** 30-70% (confidence items may have lower retention than accuracy items due to higher variability)

**Output:**

**File 1:** data/step02_purified_items.csv
**Format:** CSV, list of retained items
**Columns:**
- item_name (TC_* tag)
- dimension (Source or Destination)
- a (discrimination)
- mean_abs_b (mean absolute threshold difficulty)
**Expected Rows:** 15-40 items (30-70% of ~50-60 original items)

**File 2:** data/step02_purification_report.txt
**Format:** Text report
**Content:**
- Total items before purification
- Items excluded for low discrimination (a < 0.4)
- Items excluded for extreme difficulty (mean_abs_b > 3.0)
- Items retained (count and percentage)
- Per-dimension breakdown (Source vs Destination retention)

**Validation Requirement:**
Validation tools MUST be used after purification tool execution. Specific validation tools determined by rq_tools based on purification criteria.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_purified_items.csv exists (exact path)
- Expected rows: 15-40 items (30-70% retention)
- Expected columns: 4 (item_name, dimension, a, mean_abs_b)
- Data types: item_name/dimension (object), a/mean_abs_b (float64)

*Value Ranges:*
- a >= 0.4 for ALL retained items (threshold enforcement)
- mean_abs_b <= 3.0 for ALL retained items (threshold enforcement)
- At least 5 items per dimension (minimum for stable calibration in Pass 2)

*Data Quality:*
- No duplicate item_names (each item listed once)
- Both dimensions represented (Source AND Destination have retained items)
- Retention rate documented in purification report
- All retained items exist in Pass 1 output (no phantom items)

*Log Validation:*
- Required pattern: "Purification complete: {N} items retained ({X}%)"
- Required pattern: "Source dimension: {A} items retained"
- Required pattern: "Destination dimension: {B} items retained"
- Forbidden patterns: "ERROR", "No items retained", "Dimension eliminated"
- Acceptable warnings: "Low retention rate" (if <40%, expected for confidence items)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Only 3 Source items retained, need >= 5")
- Log failure to logs/step02_purify_items.log
- Quit script immediately
- g_debug invoked to diagnose (may need to relax thresholds if retention too low)

---

### Step 3: IRT Calibration Pass 2

**Dependencies:** Step 2 (requires purified item list)
**Complexity:** High (~40-60 minutes - GRM recalibration on purified items)

**Purpose:** Recalibrate 2-factor GRM model on purified items only. This is Pass 2 of Decision D039 2-pass purification, producing final theta estimates for LMM.

**Input:**

**File 1:** data/step00_irt_input.csv
**Format:** Wide format, 5-category ordinal responses (original extraction)

**File 2:** data/step02_purified_items.csv
**Format:** List of items to retain
**Columns:** item_name, dimension, a, mean_abs_b

**Processing:**
1. Load original IRT input (step00)
2. Load purified item list (step02)
3. Filter IRT input to ONLY purified items
4. Recalibrate 2-factor GRM model (same specification as Pass 1)
5. Extract final item parameters
6. Extract final theta estimates (these are used for LMM)
7. Save outputs to data/

**GRM Model Specification:** Same as Pass 1 (2 factors, 5 categories, p1_med prior)

**Output:**

**File 1:** data/step03_item_parameters.csv
**Format:** CSV, final item parameters (Pass 2)
**Columns:**
- item_name (TC_* tag)
- dimension (Source or Destination)
- a (discrimination parameter)
- b1, b2, b3, b4 (threshold parameters)
**Expected Rows:** 15-40 items (matches purified item count)

**File 2:** data/step03_theta_scores.csv
**Format:** CSV, final ability estimates (Pass 2 - USED FOR LMM)
**Columns:**
- composite_ID (UID_TEST format)
- theta_Source (source confidence ability)
- theta_Destination (destination confidence ability)
- se_Source (standard error)
- se_Destination (standard error)
**Expected Rows:** 400 (100 participants x 4 tests)

**Validation Requirement:**
Validation tools MUST be used after IRT calibration tool execution. Specific validation tools determined by rq_tools based on GRM convergence and parameter quality requirements for final estimates.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_theta_scores.csv exists (exact path)
- Expected rows: 400 (100 participants x 4 tests)
- Expected columns: 5 (composite_ID, theta_Source, theta_Destination, se_Source, se_Destination)
- Data types: composite_ID (object), theta/se (float64)

*Value Ranges:*
- theta in [-4, 4] (IRT ability estimates for confidence)
- se in [0.1, 1.5] (standard errors - lower than Pass 1 due to better items)
- a >= 0.4 for ALL items (purification threshold enforced)
- b1 < b2 < b3 < b4 for ALL items (threshold ordering preserved)

*Data Quality:*
- All 400 observations have theta estimates (no NaN)
- SE values lower on average than Pass 1 (improved precision from purified items)
- Model converged successfully
- Item parameters stable (no extreme changes from Pass 1 for retained items)

*Log Validation:*
- Required pattern: "Model converged: True"
- Required pattern: "Pass 2 calibration complete: {N} purified items"
- Required pattern: "Final theta estimates: 400 observations, 2 dimensions"
- Required pattern: "Mean SE reduction vs Pass 1: {X}%"
- Forbidden patterns: "ERROR", "Convergence failed", "Threshold reversal"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Pass 2 SE higher than Pass 1 - purification failed")
- Log failure to logs/step03_irt_calibration_pass2.log
- Quit script immediately
- g_debug invoked to diagnose

---

### Step 4: Merge Theta with TSVR (Decision D070)

**Dependencies:** Step 3 (requires final theta estimates)
**Complexity:** Low (~1 minute - data merge only)

**Purpose:** Merge theta confidence estimates with TSVR time variable and create long-format LMM input. Per Decision D070, use TSVR_hours (actual time) not nominal days.

**Input:**

**File 1:** data/step03_theta_scores.csv
**Format:** Wide format, one row per composite_ID
**Columns:** composite_ID, theta_Source, theta_Destination, se_Source, se_Destination

**File 2:** data/step00_tsvr_mapping.csv
**Format:** Time mapping
**Columns:** composite_ID, UID, TEST, TSVR_hours

**Processing:**
1. Load theta scores (step03)
2. Load TSVR mapping (step00)
3. Merge on composite_ID (left join - keep all theta scores, add TSVR)
4. Reshape wide -> long (theta_Source and theta_Destination become rows)
5. Create LocationType factor (Source vs Destination)
6. Create standardized time variable (z-scored TSVR_hours for LMM numerical stability)
7. Save long-format LMM input to data/

**Merge Logic:**
- **Key:** composite_ID (must match exactly between files)
- **Type:** Left join (keep all 400 theta observations, add TSVR_hours)
- **Validation:** If TSVR_hours missing for any composite_ID, raise error

**Reshape Logic:**
- **Input:** 400 rows (composite_ID, theta_Source, theta_Destination)
- **Output:** 800 rows (composite_ID, LocationType, theta_confidence)
- **LocationType:** Source (from theta_Source) or Destination (from theta_Destination)

**Output:**

**File:** data/step04_lmm_input.csv
**Format:** CSV, long format for LMM
**Columns:**
- UID (participant identifier)
- TEST (test session: T1, T2, T3, T4)
- TSVR_hours (actual time since encoding - Decision D070)
- TSVR_hours_z (z-scored TSVR for numerical stability)
- LocationType (factor: Source vs Destination)
- theta_confidence (ability estimate for this location type)
- se (standard error for this estimate)
**Expected Rows:** 800 (400 composite_IDs x 2 location types)

**Validation Requirement:**
Validation tools MUST be used after merge tool execution. Specific validation tools determined by rq_tools based on merge completeness and format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_lmm_input.csv exists (exact path)
- Expected rows: 800 (400 composite_IDs x 2 location types)
- Expected columns: 7 (UID, TEST, TSVR_hours, TSVR_hours_z, LocationType, theta_confidence, se)
- Data types: UID/TEST/LocationType (object), TSVR/theta/se (float64)

*Value Ranges:*
- TSVR_hours in [0, 168] hours (0=encoding, 168=1 week)
- TSVR_hours_z approximately N(0, 1) (z-scored, mean near 0, SD near 1)
- theta_confidence in [-4, 4] (inherited from IRT)
- se in [0.1, 1.5] (inherited from IRT)
- LocationType in {Source, Destination} ONLY

*Data Quality:*
- All 800 rows have non-null values (no NaN from merge)
- All 100 participants present (no data loss)
- All 4 test sessions represented
- Exactly 2 rows per composite_ID (Source + Destination)
- TSVR_hours matched for all composite_IDs (no missing time data)

*Log Validation:*
- Required pattern: "Merged theta with TSVR: 800 observations"
- Required pattern: "LocationType: 400 Source, 400 Destination"
- Required pattern: "TSVR_hours_z: mean={X}, SD={Y}" (X near 0, Y near 1)
- Forbidden patterns: "ERROR", "Missing TSVR", "Merge failed"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "TSVR missing for composite_ID P001_T1")
- Log failure to logs/step04_merge_theta_tsvr.log
- Quit script immediately
- g_debug invoked to diagnose

---

### Step 5: Fit LMM with LocationType x Time Interaction

**Dependencies:** Step 4 (requires long-format LMM input)
**Complexity:** Medium (~10-15 minutes - LMM fitting with 800 observations)

**Purpose:** Fit Linear Mixed Model testing LocationType x Time interaction to determine if source and destination confidence decline at different rates.

**Input:**

**File:** data/step04_lmm_input.csv
**Format:** Long format, 800 observations
**Columns:** UID, TEST, TSVR_hours, TSVR_hours_z, LocationType, theta_confidence, se

**Processing:**
1. Load LMM input
2. Specify mixed model formula:
   - **Fixed effects:** LocationType * TSVR_hours_z (main effects + interaction)
   - **Random effects:** (1 + TSVR_hours_z | UID) - random intercepts and slopes
3. Fit model using REML
4. Extract fixed effects table (coefficients, SE, t, p)
5. Extract random effects variance components
6. Compute ICC (intraclass correlation)
7. Save model summary and results to data/

**LMM Formula:**
```
theta_confidence ~ LocationType * TSVR_hours_z + (1 + TSVR_hours_z | UID)
```

**Critical Parameters:**
- **LocationType:** Categorical (Source vs Destination)
- **TSVR_hours_z:** Continuous (z-scored time)
- **Interaction term:** LocationType:TSVR_hours_z (tests differential decline)
- **Random structure:** Intercepts + slopes by participant (allows individual variation)

**Output:**

**File 1:** data/step05_lmm_model_summary.txt
**Format:** Text summary
**Content:**
- Model formula
- Fixed effects table (coefficients, SE, t, p-values)
- Random effects variance components
- Model fit indices (AIC, BIC, log-likelihood)
- Convergence status

**File 2:** data/step05_fixed_effects.csv
**Format:** CSV, fixed effects
**Columns:**
- term (LocationType, TSVR_hours_z, LocationType:TSVR_hours_z)
- coefficient (beta estimate)
- se (standard error)
- t_value (t-statistic)
- p_value (uncorrected p-value - Decision D068)
**Expected Rows:** 4 (intercept + 2 main effects + 1 interaction)

**File 3:** data/step05_random_effects_variance.csv
**Format:** CSV, variance components
**Columns:**
- component (Intercept, TSVR_hours_z, Residual)
- variance (variance estimate)
- sd (standard deviation)
**Expected Rows:** 3

**Validation Requirement:**
Validation tools MUST be used after LMM fitting tool execution. Specific validation tools determined by rq_tools based on convergence, assumptions, and residual diagnostics.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_fixed_effects.csv exists (exact path)
- Expected rows: 4 (intercept, LocationType, TSVR_hours_z, interaction)
- Expected columns: 5 (term, coefficient, se, t_value, p_value)
- Data types: term (object), others (float64)

*Value Ranges:*
- Coefficients in [-5, 5] (typical for standardized IRT theta outcomes)
- SE in [0.01, 2.0] (standard errors - very small or very large suggests problems)
- t_value unrestricted (but |t| > 10 rare, suggests extreme effect)
- p_value in [0, 1] (probability)
- Variance components > 0 (negative variance impossible)

*Data Quality:*
- Model converged successfully (convergence warnings inspected)
- All variance components positive (no boundary issues)
- Residuals approximately normal (Shapiro-Wilk or K-S test)
- No extreme outliers (residuals within +/-3 SD)
- Fixed effects table complete (no missing terms)

*Log Validation:*
- Required pattern: "LMM converged: True"
- Required pattern: "Fixed effects extracted: 4 terms"
- Required pattern: "Variance components: all positive"
- Required pattern: "Residual normality: p={X}" (Shapiro-Wilk p-value)
- Forbidden patterns: "ERROR", "Convergence failed", "Singular fit"
- Acceptable warnings: "Fixed-effect variance close to zero" (if weak main effect)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Residuals non-normal: Shapiro p < 0.001")
- Log failure to logs/step05_fit_lmm.log
- Quit script immediately
- g_debug invoked to diagnose (may need transformations or outlier removal)

---

### Step 6: Compute Location Contrasts (Decision D068)

**Dependencies:** Step 5 (requires fitted LMM)
**Complexity:** Low (~2 minutes - post-hoc contrasts)

**Purpose:** Extract and interpret LocationType x Time interaction, compute source vs destination slope contrasts with dual p-values per Decision D068.

**Input:**

**File:** data/step05_fixed_effects.csv
**Format:** CSV, fixed effects from LMM
**Columns:** term, coefficient, se, t_value, p_value

**Processing:**
1. Load fixed effects table
2. Extract LocationType:TSVR_hours_z interaction term
3. Compute marginal slopes for Source and Destination:
   - Source slope = TSVR_hours_z coefficient
   - Destination slope = TSVR_hours_z + LocationType:TSVR_hours_z coefficients
4. Compute contrast (Destination slope - Source slope)
5. Compute dual p-values (Decision D068):
   - Uncorrected p-value (from interaction term)
   - Bonferroni-corrected p-value (uncorrected x 1 comparison = uncorrected, but report both)
6. Compute effect size (Cohen's f-squared for interaction)
7. Save contrasts to data/

**Output:**

**File 1:** data/step06_location_contrasts.csv
**Format:** CSV, location contrasts
**Columns:**
- contrast (description: "Destination slope - Source slope")
- estimate (slope difference)
- se (standard error of difference)
- t_value (t-statistic)
- p_uncorrected (uncorrected p-value - Decision D068)
- p_bonferroni (Bonferroni-corrected p-value - Decision D068)
**Expected Rows:** 1 (single contrast)

**File 2:** data/step06_marginal_slopes.csv
**Format:** CSV, marginal slopes by LocationType
**Columns:**
- LocationType (Source, Destination)
- slope (decline rate per z-scored TSVR unit)
- se (standard error)
**Expected Rows:** 2 (Source, Destination)

**File 3:** data/step06_effect_sizes.csv
**Format:** CSV, effect sizes
**Columns:**
- term (LocationType:TSVR_hours_z)
- cohens_f2 (Cohen's f-squared effect size)
- interpretation (small/medium/large per Cohen 1988 thresholds)
**Expected Rows:** 1 (interaction term)

**Validation Requirement:**
Validation tools MUST be used after contrast computation tool execution. Specific validation tools determined by rq_tools based on Decision D068 dual p-value requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_location_contrasts.csv exists (exact path)
- Expected rows: 1 (single contrast)
- Expected columns: 6 (contrast, estimate, se, t_value, p_uncorrected, p_bonferroni)
- Data types: contrast (object), others (float64)

*Value Ranges:*
- estimate (slope difference) in [-2, 2] (typical for standardized time effects)
- se in [0.01, 1.0] (standard error)
- t_value unrestricted
- p_uncorrected in [0, 1] (probability)
- p_bonferroni in [0, 1] (probability)
- p_bonferroni >= p_uncorrected (correction NEVER reduces p-value)
- cohens_f2 >= 0 (effect size non-negative)

*Data Quality:*
- BOTH p_uncorrected AND p_bonferroni present (Decision D068 mandate)
- Marginal slopes computed correctly (Source + Destination)
- Effect size interpretation matches Cohen 1988 thresholds
- No NaN values (all computations successful)

*Log Validation:*
- Required pattern: "Location contrasts computed: 1 contrast"
- Required pattern: "Dual p-values: uncorrected={X}, bonferroni={Y}" (Decision D068)
- Required pattern: "Effect size: Cohen's f2={Z}, interpretation={I}"
- Forbidden patterns: "ERROR", "Missing p-value", "Negative effect size"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "p_bonferroni missing - Decision D068 violated")
- Log failure to logs/step06_compute_post_hoc_contrasts.log
- Quit script immediately
- g_debug invoked to diagnose

---

### Step 7: Prepare Trajectory Plot Data (Option B Architecture)

**Dependencies:** Steps 3, 4, 5 (requires theta scores, TSVR mapping, LMM predictions)
**Complexity:** Low (~2 minutes - data aggregation only)

**Purpose:** Aggregate analysis outputs to create plot source CSVs for theta-scale and probability-scale trajectory plots (Decision D069 dual-scale requirement). This is Option B architecture - plot data preparation happens during analysis, visualization happens later via rq_plots.

**CRITICAL:** Plot data preparation IS an analysis step. It gets executed in Step 14 CODE EXECUTION LOOP (g_code -> bash -> rq_inspect) and MUST have validation requirements.

**Plot Description:** Trajectory over time with confidence bands showing confidence decline for source vs destination locations, displayed on both theta scale (-4 to +4) and probability scale (0 to 1) per Decision D069.

**Required Data Sources:**
- data/step03_theta_scores.csv (columns: composite_ID, theta_Source, theta_Destination)
- data/step00_tsvr_mapping.csv (columns: composite_ID, TSVR_hours, TEST)
- data/step05_fixed_effects.csv (for predicted trajectories)

**Input:**

**File 1:** data/step03_theta_scores.csv
**Format:** Wide format theta estimates
**Columns:** composite_ID, theta_Source, theta_Destination, se_Source, se_Destination

**File 2:** data/step00_tsvr_mapping.csv
**Format:** Time mapping
**Columns:** composite_ID, TSVR_hours, TEST

**File 3:** data/step05_fixed_effects.csv
**Format:** Fixed effects for predictions
**Columns:** term, coefficient, se, t_value, p_value

**Processing:**
1. Merge theta scores with TSVR mapping on composite_ID
2. Reshape wide -> long (Source and Destination as rows)
3. Group by LocationType x TEST, compute:
   - Observed mean theta
   - 95% CI (mean +/- 1.96 * SE)
4. Generate predicted trajectories from LMM fixed effects
5. Create theta-scale plot data (theta values -4 to +4)
6. Transform theta -> probability using IRT formula: P(theta) = 1 / (1 + exp(-1.7 * theta))
7. Create probability-scale plot data (probability values 0 to 1)
8. Save both source CSVs to data/

**Aggregation Logic:**
1. Merge theta_scores with tsvr_mapping on composite_ID (adds TSVR_hours, TEST)
2. Reshape: theta_Source and theta_Destination -> rows with LocationType factor
3. Group by LocationType + TEST, compute mean(theta_confidence), 95% CI
4. Add predicted values from LMM fixed effects
5. Select and rename columns to match required schema
6. Sort by LocationType, then TSVR_hours
7. Save theta-scale data to data/step07_trajectory_theta_data.csv
8. Transform theta -> probability scale (IRT transformation)
9. Save probability-scale data to data/step07_trajectory_probability_data.csv

**Output (Plot Source CSV):**

**File 1:** data/step07_trajectory_theta_data.csv
**Format:** CSV, plot source data for theta-scale trajectory
**Columns:**
- time (float): TSVR_hours (0, 24, 72, 144 approximate for T1-T4)
- theta (float): Observed mean theta per LocationType per timepoint
- theta_pred (float): Predicted theta from LMM
- CI_lower (float): Lower 95% confidence bound
- CI_upper (float): Upper 95% confidence bound
- LocationType (string): Source or Destination
**Expected Rows:** 8 (2 LocationTypes x 4 timepoints)

**File 2:** data/step07_trajectory_probability_data.csv
**Format:** CSV, plot source data for probability-scale trajectory (Decision D069 dual-scale)
**Columns:**
- time (float): TSVR_hours (same as theta-scale)
- probability (float): Transformed theta -> probability scale (0 to 1)
- probability_pred (float): Transformed predicted theta -> probability
- CI_lower (float): Lower 95% confidence bound (probability scale)
- CI_upper (float): Upper 95% confidence bound (probability scale)
- LocationType (string): Source or Destination
**Expected Rows:** 8 (2 LocationTypes x 4 timepoints)

**Note:** rq_plots agent will later read these CSVs from data/, generate plots.py that calls tools/plotting.py functions, and save PNG/PDF output to plots/ folder. NO data aggregation in rq_plots per Option B architecture.

**Validation Requirement:**
Validation tools MUST be used after plot data preparation tool execution. Specific validation tools determined by rq_tools based on plot data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_trajectory_theta_data.csv exists (exact path)
- data/step07_trajectory_probability_data.csv exists (exact path)
- Expected rows: 8 each (2 LocationTypes x 4 timepoints)
- Expected columns: 6 each (time, theta/probability, theta_pred/probability_pred, CI_lower, CI_upper, LocationType)
- Data types: time/theta/probability/CI (float64), LocationType (object)

*Value Ranges:*
- time in [0, 168] hours (0=encoding, 168=1 week)
- theta in [-4, 4] (typical IRT ability range for confidence)
- probability in [0, 1] (probability scale per Decision D069)
- CI_lower in [-4, 4] for theta scale, [0, 1] for probability scale
- CI_upper in [-4, 4] for theta scale, [0, 1] for probability scale
- LocationType in {Source, Destination} ONLY

*Data Quality:*
- No NaN values tolerated (all cells must have valid values)
- Expected N: Exactly 8 rows per file (no more, no less)
- No duplicate rows (LocationType x time combinations unique)
- Distribution check: CI_upper > CI_lower for all rows
- Probability transformation correct: probability = 1 / (1 + exp(-1.7 * theta))

*Log Validation:*
- Required pattern: "Plot data preparation complete: theta-scale 8 rows, probability-scale 8 rows"
- Required pattern: "LocationTypes represented: Source, Destination"
- Required pattern: "Probability transformation applied (Decision D069)"
- Forbidden patterns: "ERROR", "NaN values detected", "Missing LocationType"
- Acceptable warnings: None expected for plot data preparation

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 8 rows, found 6")
- Log failure to logs/step07_prepare_trajectory_plot_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- g_debug invoked to diagnose root cause

**Plotting Function (rq_plots will call):** Trajectory plot with confidence bands
- rq_plots agent maps this description to specific tools/plotting.py functions
- Theta-scale plot: plot_trajectory() reading data/step07_trajectory_theta_data.csv
- Probability-scale plot: plot_trajectory_probability() reading data/step07_trajectory_probability_data.csv
- No data aggregation in rq_plots (visualization only per Option B)
- PNG outputs saved to plots/ folder by rq_plots (plots/trajectory_theta.png, plots/trajectory_probability.png)

---

## Expected Data Formats

### Confidence Data Format (5-Category Ordinal)

**Critical Distinction from Accuracy Data:**

This RQ uses **5-category ordinal confidence data** (0, 0.25, 0.5, 0.75, 1.0), NOT binary accuracy data (0/1). This requires:
- **GRM (Graded Response Model)** calibration (NOT 2PL which is for binary data)
- **4 threshold parameters (b1-b4)** per item (NOT single difficulty parameter)
- **Ordered category structure** (b1 < b2 < b3 < b4 MUST hold)

**IRT Input Format:**
- Rows: composite_ID (UID_TEST format, e.g., P001_T1)
- Columns: TC_* item tags (5-category ordinal responses)
- Values: {0, 0.25, 0.5, 0.75, 1.0} ONLY (no intermediate values)
- Missing: NaN (acceptable, confidence items may have higher missingness)

**Q-Matrix Format:**
- Rows: TC_* item tags
- Columns: Source, Destination (binary 0/1 loadings)
- Structure: Simple (each item loads on ONE dimension only)

### TSVR Time Variable (Decision D070)

**Format:** TSVR_hours (continuous, actual elapsed time)

**Values:**
- T1 (encoding): ~0 hours
- T2 (immediate): ~24 hours (1 day)
- T3 (delay): ~72 hours (3 days)
- T4 (long-term): ~144 hours (6 days)

**Note:** Actual values vary per participant schedule. Use TSVR_hours (actual), NOT nominal days {0, 1, 3, 6}.

**Standardization:** Create TSVR_hours_z (z-scored) for LMM numerical stability.

### Theta Scores Format

**Wide Format (Step 3 output):**
- composite_ID (UID_TEST)
- theta_Source (source confidence ability)
- theta_Destination (destination confidence ability)
- se_Source (standard error)
- se_Destination (standard error)

**Long Format (Step 4 output for LMM):**
- UID (participant identifier)
- TEST (test session)
- TSVR_hours (time variable)
- LocationType (Source vs Destination)
- theta_confidence (ability estimate)
- se (standard error)

### LMM Input Format

**One row per observation** (800 rows total):
- UID (participant identifier - random effect grouping)
- TEST (test session - for reference)
- TSVR_hours (actual time - raw scale)
- TSVR_hours_z (z-scored time - used in LMM)
- LocationType (categorical: Source vs Destination)
- theta_confidence (outcome variable)
- se (standard error - can weight observations if needed)

### Plot Source CSV Format

**Theta-Scale CSV:**
- time (TSVR_hours)
- theta (observed mean)
- theta_pred (LMM predicted)
- CI_lower (95% confidence lower bound)
- CI_upper (95% confidence upper bound)
- LocationType (Source vs Destination)

**Probability-Scale CSV:**
- Same structure as theta-scale
- Values transformed: probability = 1 / (1 + exp(-1.7 * theta))
- Range: [0, 1] instead of [-4, 4]

---

## Cross-RQ Dependencies

**This RQ uses:** Only dfData.csv (RAW data extraction)

**No dependencies on other RQs:** Can be executed independently

**Execution order:** Flexible (any order within Chapter 6)

**Data Sources:**
- dfData.csv (cached participant responses)
- TC_* confidence items with -U- and -D- tags
- TSVR timing data

**Note:** All data extraction uses direct filtering of dfData.csv. No intermediate outputs from other RQs required.

**Comparison Reference:** Results will be compared to Ch5 5.5.1 (accuracy source-destination dissociation) in rq_results phase to test whether confidence replicates accuracy pattern. This is a QUALITATIVE comparison (read Ch5 5.5.1 summary, interpret consistency), NOT a dependency (does not require Ch5 5.5.1 data files).

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

**Step 0: Extract Confidence Item Data**
- Output file exists (data/step00_irt_input.csv)
- Expected dimensions (400 rows x 50-60 columns)
- Values in correct range ({0, 0.25, 0.5, 0.75, 1.0} ONLY)
- Q-matrix simple structure (no items load on multiple dimensions)
- TSVR mapping complete (all composite_IDs matched)

**Step 1: IRT Calibration Pass 1**
- Model convergence (log-likelihood stable)
- Parameter ranges (a in [0.1, 10], b ordered b1 < b2 < b3 < b4)
- Theta estimates in valid range ([-4, 4])
- No negative discrimination (a > 0 for all items)
- Threshold ordering preserved (critical for GRM)

**Step 2: Purify Items**
- Thresholds applied correctly (a >= 0.4, mean_abs_b <= 3.0)
- Retention rate reasonable (15-40 items, 30-70%)
- Both dimensions represented (Source AND Destination)
- Purification report generated (documents exclusions)

**Step 3: IRT Calibration Pass 2**
- Model convergence on purified items
- SE reduction vs Pass 1 (improved precision)
- Theta estimates stable (no extreme changes for participants)
- All 400 observations estimated (no data loss)

**Step 4: Merge Theta with TSVR**
- All composite_IDs matched (no missing TSVR)
- Reshape correct (800 rows = 400 x 2 LocationTypes)
- TSVR_hours_z standardized (mean near 0, SD near 1)
- No NaN values (complete merge)

**Step 5: Fit LMM**
- Model convergence (REML converged)
- Residuals approximately normal (Shapiro-Wilk p > 0.05 or close)
- Variance components positive (no boundary issues)
- Fixed effects table complete (4 terms)

**Step 6: Compute Contrasts**
- Dual p-values present (uncorrected + Bonferroni per Decision D068)
- Effect size computed (Cohen's f-squared)
- Marginal slopes calculated (Source + Destination)
- p_bonferroni >= p_uncorrected (correction logic correct)

**Step 7: Prepare Plot Data**
- Both theta and probability CSVs created (Decision D069 dual-scale)
- Expected dimensions (8 rows each, 6 columns)
- Value ranges correct (theta in [-4, 4], probability in [0, 1])
- Probability transformation applied (1 / (1 + exp(-1.7 * theta)))
- CI_upper > CI_lower for all rows

---

## Summary

**Total Steps:** 8 (Step 0: extraction + Steps 1-7: analysis/plotting)

**Estimated Runtime:** High (~90-120 minutes total)
- Step 0: ~2 minutes
- Step 1: ~40-60 minutes (GRM Pass 1)
- Step 2: ~1 minute
- Step 3: ~40-60 minutes (GRM Pass 2)
- Step 4: ~1 minute
- Step 5: ~10-15 minutes
- Step 6: ~2 minutes
- Step 7: ~2 minutes

**Cross-RQ Dependencies:** None (RAW data only from dfData.csv)

**Primary Outputs:**
- data/step03_theta_scores.csv (final confidence ability estimates)
- data/step05_lmm_model_summary.txt (trajectory model results)
- data/step06_location_contrasts.csv (source vs destination slope comparison)
- data/step07_trajectory_theta_data.csv (theta-scale plot source)
- data/step07_trajectory_probability_data.csv (probability-scale plot source)

**Validation Coverage:** 100% (all 8 steps have validation requirements with 4-layer substance criteria)

**Key Hypothesis Test:** LocationType x TSVR_hours_z interaction in LMM
- If p < 0.05: Source and destination confidence decline at different rates
- Expected pattern: Destination declines faster than source (replicating Ch5 5.5.1 accuracy finding)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 10 approval gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent for RQ 6.8.1
