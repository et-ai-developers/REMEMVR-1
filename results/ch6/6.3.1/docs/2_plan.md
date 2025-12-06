# Analysis Plan: RQ 6.3.1 - Domain Confidence Trajectories

**Research Question:** 6.3.1
**Created:** 2025-12-06
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines whether What/Where/When episodic memory domains show different confidence decline patterns across a 6-day retention interval using IRT-derived ability estimates from 5-level Likert confidence ratings (TC_* items). The analysis tests whether metacognitive monitoring (confidence) shows the same domain-invariant pattern found for accuracy in Ch5 5.2.1 (NULL hypothesis: domain x time interaction non-significant).

**Pipeline:** IRT (Graded Response Model for ordinal data) -> LMM (trajectory modeling with TSVR time variable)

**Steps:** 8 total analysis steps (Step 0: extraction + Steps 1-7: analysis)

**Estimated Runtime:** High (2-3 hours total - Step 1 and Step 3 IRT calibrations dominate, ~45-60 min each)

**Key Decisions Applied:**
- Decision D039: 2-pass IRT purification (mandatory for all IRT analyses)
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni for post-hoc contrasts)
- Decision D069: Dual-scale trajectory plots (theta + probability scales for interpretability)
- Decision D070: TSVR as LMM time variable (actual hours, not nominal days)

**Critical Note:** When domain may be excluded AFTER Step 2 purification if <10 items remain (Ch5 showed When floor effects). Analysis continues with What/Where only if When excluded, with documentation of decision.

---

## Analysis Plan

This RQ requires 8 steps:

### Step 0: Extract Confidence Item Data

**Dependencies:** None (first step - extracts from RAW data source)
**Complexity:** Low (5-10 minutes - data extraction only)

**Purpose:** Extract TC_* confidence items from dfData.csv, filter by domain tags (What: *-N-*, Where: *-L-*/*-U-*/*-D-*, When: *-O-*), create 3-factor Q-matrix (What/Where/When).

**Input:**

**File:** data/cache/dfData.csv (project-level RAW data source)

**Required Columns:**
- UID (participant identifier)
- test (test session: T1, T2, T3, T4 for Days 0, 1, 3, 6)
- TC_* item columns (5-category ordinal confidence ratings: 0, 0.25, 0.5, 0.75, 1.0)

**Filters:**
- Item type: TC_* only (confidence ratings, NOT TQ_* accuracy items)
- Paradigm: Interactive paradigms only (IFR, ICR, IRE) - exclude RFR/TCR/RRE
- Domain tags:
  - What: tag contains '-N-' (object identity)
  - Where: tag contains '-L-' OR '-U-' OR '-D-' (spatial location - all subtags combined)
  - When: tag contains '-O-' (temporal order)

**Processing:**

1. Load dfData.csv
2. Filter to TC_* columns matching interactive paradigms (IFR, ICR, IRE)
3. Parse item tags to assign domain (What/Where/When based on tag patterns)
4. Create composite_ID (UID_test format, e.g., P001_T1)
5. Reshape to wide format (composite_ID x item columns)
6. Create Q-matrix for 3-factor IRT structure:
   - Factor 1: What domain items
   - Factor 2: Where domain items (combining -L-, -U-, -D-)
   - Factor 3: When domain items
7. Extract TSVR time mapping (composite_ID -> TSVR_hours for Step 4)

**Output:**

**File 1:** data/step00_irt_input.csv
**Format:** CSV, wide format (one row per composite_ID)
**Columns:**
  - composite_ID (string, format: UID_test, e.g., P001_T1)
  - One column per TC_* item (ordinal values: 0, 0.25, 0.5, 0.75, 1.0)
**Expected Rows:** 400 (100 participants x 4 tests)
**Expected Columns:** ~103 (composite_ID + ~102 TC_* items)

**File 2:** data/step00_tsvr_mapping.csv
**Format:** CSV, one row per composite_ID
**Columns:**
  - composite_ID (string)
  - TSVR_hours (float, actual hours since encoding per Decision D070)
  - test (string, T1/T2/T3/T4)
**Expected Rows:** 400

**File 3:** data/step00_q_matrix.csv
**Format:** CSV, one row per item
**Columns:**
  - item_name (string, TC_* tag)
  - dimension (int, 1=What, 2=Where, 3=When)
  - domain (string, What/Where/When for readability)
**Expected Rows:** ~102 items

**Validation Requirement:**
Validation tools MUST be used after data extraction tool execution. Specific validation tools will be determined by rq_tools based on extraction type (IRT input validation, Q-matrix validation, TSVR mapping validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_irt_input.csv: 400 rows x ~103 columns (composite_ID + items)
- data/step00_tsvr_mapping.csv: 400 rows x 3 columns (composite_ID, TSVR_hours, test)
- data/step00_q_matrix.csv: ~102 rows x 3 columns (item_name, dimension, domain)
- Data types: composite_ID (string), items (float: 0/0.25/0.5/0.75/1.0), TSVR_hours (float), dimension (int)

*Value Ranges:*
- TC_* item values in {0.0, 0.25, 0.5, 0.75, 1.0} (ordinal scale)
- TSVR_hours in [0, 168] hours (0=encoding, 168=1 week)
- dimension in {1, 2, 3} (What, Where, When)
- NaN acceptable for TC_* items (missing data expected <10% per item)

*Data Quality:*
- All 100 participants present (no data loss)
- All 4 tests present per participant (400 composite_IDs)
- Composite_ID format correct (UID_test pattern)
- Q-matrix: all three dimensions represented (What, Where, When)
- Q-matrix: no items without dimension assignment
- TSVR: all 400 composite_IDs have TSVR_hours (no missing time data)

*Log Validation:*
- Required: "Extracted N TC_* items from dfData.csv" (where N ~102)
- Required: "Created 3-factor Q-matrix: What (N1 items), Where (N2 items), When (N3 items)"
- Required: "TSVR mapping created: 400 composite_IDs"
- Forbidden: "ERROR", "No TC_* items found", "Missing TSVR data"
- Acceptable: "Warning: <10% missing data in item TC_XYZ" (expected)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 400 rows, found 350")
- Log failure to logs/step00_extract_confidence_data.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause

---

### Step 1: IRT Calibration Pass 1 (All Items)

**Dependencies:** Step 0 (requires extracted item data + Q-matrix)
**Complexity:** High (45-60 minutes - GRM calibration for 3-factor ordinal model with ~102 items)

**Purpose:** Calibrate Graded Response Model (GRM) on all TC_* items using 3-factor structure (What/Where/When). Pass 1 identifies items for purification (Decision D039).

**CRITICAL NOTE:** GRM required for ordinal data (5-category: 0, 0.25, 0.5, 0.75, 1.0). 2PL assumes dichotomous responses and CANNOT be used for TC_* confidence items.

**MINIMAL SETTINGS TESTING:** First run should use minimal settings (max_iter=50, mc_samples=10, iw_samples=10) to validate pipeline in ~10 minutes before committing to production run (~45-60 min).

**Input:**

**File 1:** data/step00_irt_input.csv (from Step 0)
**Format:** Wide format (composite_ID x items)
**Expected:** 400 rows x ~103 columns

**File 2:** data/step00_q_matrix.csv (from Step 0)
**Format:** Q-matrix specifying 3-factor structure
**Expected:** ~102 rows x 3 columns

**Processing:**

1. Load IRT input + Q-matrix
2. Configure GRM model with 3 dimensions (What, Where, When)
3. Apply p1_med prior (standard prior for moderate discrimination)
4. Calibrate model using variational inference (IWAVE algorithm)
5. Production settings: max_iter=200, mc_samples=100, iw_samples=100
6. Minimal settings (first test): max_iter=50, mc_samples=10, iw_samples=10
7. Extract item parameters (discrimination a, difficulty b per category)
8. Extract theta_confidence estimates per domain (diagnostic, not final)

**Output:**

**File 1:** data/step01_pass1_item_params.csv
**Format:** CSV, one row per item
**Columns:**
  - item_name (string, TC_* tag)
  - dimension (string, What/Where/When)
  - a (float, discrimination parameter)
  - b (float, difficulty parameter - may have multiple columns b1, b2, b3, b4 for 5-category GRM)
**Expected Rows:** ~102 items

**File 2:** data/step01_pass1_theta.csv
**Format:** CSV, one row per composite_ID
**Columns:**
  - composite_ID (string)
  - theta_What (float, ability estimate for What domain)
  - se_What (float, standard error for What)
  - theta_Where (float, ability estimate for Where domain)
  - se_Where (float, standard error for Where)
  - theta_When (float, ability estimate for When domain)
  - se_When (float, standard error for When)
**Expected Rows:** 400

**Validation Requirement:**
Validation tools MUST be used after IRT calibration tool execution. Specific validation tools will be determined by rq_tools based on IRT model type (GRM convergence validation, parameter bounds validation, dimensionality validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_pass1_item_params.csv: ~102 rows x ~6 columns (item_name, dimension, a, b1-b4)
- data/step01_pass1_theta.csv: 400 rows x 7 columns (composite_ID, theta_What, se_What, theta_Where, se_Where, theta_When, se_When)
- Data types: a (float >0), b (float unrestricted), theta (float), se (float >0)

*Value Ranges:*
- a (discrimination) in [0.0, 10.0] (above 10.0 suggests estimation error)
- b (difficulty) in [-6.0, +6.0] (extreme values possible for temporal items but note for review)
- theta in [-4, 4] (IRT ability range, wider than typical [-3, 3] for confidence data)
- se in [0.1, 1.5] (standard error - above 1.5 indicates unreliable estimation)
- No NaN in a or b (indicates estimation failure)
- NaN acceptable in theta/se if participant has all missing data for a domain

*Data Quality:*
- All ~102 items have parameters (no missing items)
- All 400 composite_IDs present (no data loss)
- Three dimensions represented in item_params (What, Where, When)
- Model converged successfully (check log)

*Log Validation:*
- Required: "Model converged: True"
- Required: "VALIDATION - PASS: Convergence achieved"
- Required: "VALIDATION - PASS: Item parameters in valid ranges"
- Forbidden: "ERROR", "CONVERGENCE FAILED", "NaN in item parameters"
- Acceptable: "Warning: Item TC_XYZ has extreme difficulty b > 3.0" (expected for temporal items)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Item TC_XYZ has NaN discrimination")
- Log failure to logs/step01_irt_calibration_pass1.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose (common causes: insufficient data, model misspecification, convergence issues)

---

### Step 2: Item Purification (Decision D039)

**Dependencies:** Step 1 (requires Pass 1 item parameters)
**Complexity:** Low (5 minutes - threshold-based filtering)

**Purpose:** Filter items by quality thresholds (|b| <= 3.0, a >= 0.4) per Decision D039. Check When domain item count - if <10 items remain, exclude entire When domain and document.

**Input:**

**File:** data/step01_pass1_item_params.csv (from Step 1)
**Format:** Item parameters with a, b per item
**Expected:** ~102 rows

**Processing:**

1. Load Pass 1 item parameters
2. Apply purification thresholds:
   - Exclude if |b| > 3.0 (extreme difficulty)
   - Exclude if a < 0.4 (low discrimination)
3. Identify retained items per dimension
4. **CRITICAL CHECK:** Count When domain retained items
   - If When >= 10 items: Proceed with 3-factor model (What/Where/When)
   - If When < 10 items: Exclude When domain, proceed with 2-factor model (What/Where only)
5. Create purified item list + purification report
6. Update Q-matrix based on When domain status

**Output:**

**File 1:** data/step02_purified_items.csv
**Format:** CSV, one row per retained item
**Columns:**
  - item_name (string, TC_* tag)
  - dimension (string, What/Where/When)
  - a (float, discrimination from Pass 1)
  - b (float, difficulty from Pass 1)
  - retention_reason (string, "RETAINED: passes thresholds")
**Expected Rows:** Variable (40-60 items expected based on Ch5 40-50% retention, potentially fewer if When excluded)

**File 2:** data/step02_purification_report.txt
**Format:** Text report
**Contents:**
  - Total items tested: N
  - Items retained: M (per dimension breakdown)
  - Items excluded: N-M (with reasons: low a, extreme b)
  - When domain status: INCLUDED (>=10 items) OR EXCLUDED (<10 items)
  - If When excluded: list excluded items, rationale (floor effects in Ch5)

**File 3:** data/step02_q_matrix_purified.csv
**Format:** CSV, Q-matrix for Pass 2 (updated based on When status)
**Columns:**
  - item_name (string, only retained items)
  - dimension (int, 1=What, 2=Where, 3=When if included)
  - domain (string, What/Where/When or What/Where if When excluded)
**Expected Rows:** Variable (matches purified_items.csv row count)

**Validation Requirement:**
Validation tools MUST be used after purification tool execution. Specific validation tools will be determined by rq_tools based on purification criteria (item retention validation, domain representation validation, Q-matrix consistency validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_purified_items.csv: 40-60 rows x 5 columns (item_name, dimension, a, b, retention_reason)
- data/step02_purification_report.txt: Text file exists with required sections
- data/step02_q_matrix_purified.csv: 40-60 rows x 3 columns (matches purified_items count)
- Data types: same as Pass 1 item_params

*Value Ranges:*
- All retained items: a >= 0.4 (purification threshold enforced)
- All retained items: |b| <= 3.0 (purification threshold enforced)
- Retention rate: 20-80% (outside this range suggests calibration problem)

*Data Quality:*
- At least 10 items per dimension (minimum for reliable estimation)
  - EXCEPTION: When domain may have <10 -> entire domain excluded
- purified_items.csv row count matches q_matrix_purified.csv row count
- No duplicate item_names in purified list
- purification_report.txt documents When domain status explicitly

*Log Validation:*
- Required: "Purification complete: M items retained out of N"
- Required: "What domain: N1 items retained"
- Required: "Where domain: N2 items retained"
- Required: "When domain: N3 items retained" OR "When domain EXCLUDED: <10 items post-purification"
- Forbidden: "ERROR", "No items retained in dimension", "Q-matrix mismatch"
- Acceptable: "Warning: 60% item exclusion rate" (expected for difficult temporal items)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "What domain has 8 items, minimum 10 required")
- Log failure to logs/step02_purify_items.log
- Quit script immediately (do NOT proceed to Step 3)
- g_debug invoked to diagnose (common causes: overly strict thresholds, poor calibration, insufficient item pool)

---

### Step 3: IRT Calibration Pass 2 (Purified Items Only)

**Dependencies:** Step 2 (requires purified item list + updated Q-matrix)
**Complexity:** High (45-60 minutes - GRM re-calibration on purified items)

**Purpose:** Re-calibrate GRM on purified items using updated Q-matrix (2-factor if When excluded, 3-factor if When included). Extract final theta_confidence estimates per domain.

**MINIMAL SETTINGS TESTING:** First run should use minimal settings to validate pipeline before production run.

**Input:**

**File 1:** data/step00_irt_input.csv (original wide data, will filter to purified items)
**Expected:** 400 rows x ~103 columns

**File 2:** data/step02_purified_items.csv (from Step 2)
**Expected:** 40-60 rows (list of retained items)

**File 3:** data/step02_q_matrix_purified.csv (from Step 2)
**Expected:** 40-60 rows (updated Q-matrix)

**Processing:**

1. Load original IRT input
2. Filter to purified items only (columns matching step02_purified_items.csv)
3. Load updated Q-matrix (2-factor or 3-factor based on When status)
4. Configure GRM model with updated dimensionality
5. Calibrate model (same settings as Pass 1: max_iter=200, mc_samples=100, iw_samples=100)
6. Extract final item parameters
7. Extract final theta_confidence estimates per domain
8. Create long-format theta file for LMM (composite_ID, domain, theta, se)

**Output:**

**File 1:** data/step03_item_parameters.csv
**Format:** CSV, one row per purified item
**Columns:**
  - item_name (string)
  - dimension (string, What/Where or What/Where/When)
  - a (float, discrimination)
  - b1, b2, b3, b4 (float, difficulty thresholds for 5-category GRM)
**Expected Rows:** 40-60 items (matches purified count)

**File 2:** data/step03_theta_scores.csv
**Format:** CSV, wide format (one row per composite_ID)
**Columns:**
  - composite_ID (string)
  - theta_What (float)
  - se_What (float)
  - theta_Where (float)
  - se_Where (float)
  - [theta_When (float) - only if When included]
  - [se_When (float) - only if When included]
**Expected Rows:** 400

**File 3:** data/step03_theta_long.csv
**Format:** CSV, long format for LMM (one row per composite_ID x domain)
**Columns:**
  - composite_ID (string)
  - domain (string, What/Where or What/Where/When)
  - theta (float)
  - se (float)
**Expected Rows:** 800 (if When excluded: 100 x 4 tests x 2 domains) OR 1200 (if When included: 100 x 4 tests x 3 domains)

**Validation Requirement:**
Validation tools MUST be used after IRT calibration tool execution. Specific validation tools will be determined by rq_tools based on Pass 2 calibration requirements (convergence, improved fit vs Pass 1, theta reliability).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_item_parameters.csv: 40-60 rows x ~6 columns
- data/step03_theta_scores.csv: 400 rows x 5 or 7 columns (depends on When status)
- data/step03_theta_long.csv: 800 or 1200 rows x 4 columns
- Data types: same as Pass 1

*Value Ranges:*
- a in [0.4, 10.0] (lower bound enforced by purification)
- b in [-3.0, 3.0] (bounds enforced by purification)
- theta in [-4, 4]
- se in [0.1, 1.5]
- No NaN in item_parameters (all purified items must calibrate successfully)

*Data Quality:*
- All 400 composite_IDs present in theta files
- theta_long.csv row count: 800 (if 2-factor) OR 1200 (if 3-factor)
- All domains in theta_long match Q-matrix dimensions
- Model converged (improved fit vs Pass 1 expected)

*Log Validation:*
- Required: "Pass 2 calibration complete: N items"
- Required: "Model converged: True"
- Required: "VALIDATION - PASS: Theta reliability acceptable"
- Required: "When domain status: INCLUDED" OR "When domain status: EXCLUDED"
- Forbidden: "ERROR", "CONVERGENCE FAILED", "NaN in theta estimates"
- Acceptable: "Note: Pass 2 fit improved over Pass 1 (expected)"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step03_irt_calibration_pass2.log
- Quit script immediately
- g_debug invoked

---

### Step 4: Merge Theta with TSVR Time Data

**Dependencies:** Step 3 (requires theta_long.csv), Step 0 (requires TSVR mapping)
**Complexity:** Low (5 minutes - simple merge operation)

**Purpose:** Merge theta_confidence estimates with TSVR time variable (actual hours since encoding) per Decision D070. Create LMM-ready input file.

**Input:**

**File 1:** data/step03_theta_long.csv (from Step 3)
**Expected:** 800 or 1200 rows x 4 columns

**File 2:** data/step00_tsvr_mapping.csv (from Step 0)
**Expected:** 400 rows x 3 columns (composite_ID, TSVR_hours, test)

**Processing:**

1. Load theta_long + TSVR mapping
2. Merge on composite_ID (left join - keep all theta observations, add TSVR_hours)
3. Verify all composite_IDs matched (no missing TSVR data)
4. Parse UID from composite_ID (for LMM random effects grouping)
5. Add time transformations for LMM functional form exploration:
   - TSVR_hours (raw - Decision D070)
   - log_TSVR (log-transformed - likely best based on Ch5/Ch6 prior RQs)
   - TSVR_squared (quadratic term if needed)

**Output:**

**File:** data/step04_lmm_input.csv
**Format:** CSV, long format LMM-ready
**Columns:**
  - composite_ID (string)
  - UID (string, participant identifier for random effects)
  - test (string, T1/T2/T3/T4)
  - domain (string, What/Where or What/Where/When)
  - theta (float, confidence ability estimate)
  - se (float, standard error)
  - TSVR_hours (float, time since encoding - Decision D070)
  - log_TSVR (float, log-transformed time)
  - TSVR_squared (float, quadratic time term)
**Expected Rows:** 800 (if When excluded) OR 1200 (if When included)

**Validation Requirement:**
Validation tools MUST be used after merge tool execution. Specific validation tools will be determined by rq_tools based on merge requirements (all IDs matched, no missing time data, valid transformations).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_lmm_input.csv: 800 or 1200 rows x 9 columns
- Data types: composite_ID (string), UID (string), test (string), domain (string), theta (float), se (float), TSVR_hours (float), log_TSVR (float), TSVR_squared (float)

*Value Ranges:*
- TSVR_hours in [0, 168] hours
- log_TSVR in [-inf, 5.2] (log(168) ~ 5.13)
- TSVR_squared in [0, 28224] (168^2)
- theta in [-4, 4]
- se in [0.1, 1.5]
- No NaN in TSVR_hours (all observations must have time data)
- NaN acceptable in theta/se if participant missing all data for domain

*Data Quality:*
- All 800 or 1200 observations present (no data loss during merge)
- All composite_IDs from theta_long matched with TSVR (100% merge rate)
- UID correctly parsed from composite_ID (format: extract before underscore)
- Time transformations mathematically correct (log_TSVR = log(TSVR_hours), TSVR_squared = TSVR_hours^2)

*Log Validation:*
- Required: "Merge complete: 800 or 1200 observations"
- Required: "All composite_IDs matched with TSVR data (100% merge rate)"
- Required: "Time transformations created: log_TSVR, TSVR_squared"
- Forbidden: "ERROR", "Missing TSVR data", "Merge failure"
- Acceptable: None expected

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "50 composite_IDs missing TSVR data")
- Log failure to logs/step04_merge_theta_tsvr.log
- Quit script immediately
- g_debug invoked

---

### Step 5: Fit LMM with Domain x Time Interaction

**Dependencies:** Step 4 (requires LMM input with TSVR time variable)
**Complexity:** Medium (15-30 minutes - LMM fitting + interaction tests)

**Purpose:** Fit Linear Mixed Model to test primary hypothesis (Domain x Time interaction). Use TSVR_hours as time variable (Decision D070). Test whether confidence decline rate differs across domains.

**Input:**

**File:** data/step04_lmm_input.csv (from Step 4)
**Expected:** 800 or 1200 rows x 9 columns

**Processing:**

1. Load LMM input
2. Determine time transformation based on Ch6 prior RQ findings (likely log_TSVR)
3. Fit primary LMM model:
   - Fixed effects: Domain * Time (interaction term critical for hypothesis)
   - Random effects: (Time | UID) - allows individual trajectories
   - Time variable: log_TSVR (or TSVR_hours if linear best)
   - REML=False (for model comparison if needed)
4. Extract fixed effects table (coefficients, SE, z, p-values)
5. Test Domain x Time interaction significance (primary hypothesis test)
6. Compute effect sizes for main effects and interaction

**Output:**

**File 1:** data/step05_lmm_model_summary.txt
**Format:** Text file with statsmodels summary
**Contents:**
  - Fixed effects table (coefficients, SE, z, p)
  - Random effects variance components
  - Model fit indices (AIC, BIC, log-likelihood)
  - Domain x Time interaction test result

**File 2:** data/step05_fixed_effects.csv
**Format:** CSV, one row per fixed effect term
**Columns:**
  - term (string, e.g., "Intercept", "Domain[Where]", "log_TSVR", "Domain[Where]:log_TSVR")
  - coef (float)
  - se (float)
  - z (float)
  - p_uncorrected (float)
  - p_bonferroni (float, Decision D068 dual p-values for exploratory reporting)
**Expected Rows:** Variable (depends on 2-factor vs 3-factor model)

**File 3:** data/step05_effect_sizes.csv
**Format:** CSV, effect sizes for main effects and interaction
**Columns:**
  - term (string)
  - cohens_f2 (float)
  - interpretation (string, small/medium/large)
**Expected Rows:** Matches fixed_effects.csv row count

**Validation Requirement:**
Validation tools MUST be used after LMM fitting tool execution. Specific validation tools will be determined by rq_tools based on LMM requirements (convergence, residual normality, homoscedasticity, no autocorrelation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_lmm_model_summary.txt: Text file exists with statsmodels output
- data/step05_fixed_effects.csv: Variable rows x 6 columns
- data/step05_effect_sizes.csv: Variable rows x 3 columns
- Data types: coef (float), se (float >0), z (float), p (float in [0,1]), cohens_f2 (float >=0)

*Value Ranges:*
- coef: unrestricted (can be negative)
- se > 0 (standard errors must be positive)
- z: unrestricted
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1], p_bonferroni >= p_uncorrected (correction cannot decrease p-value)
- cohens_f2 >= 0 (effect sizes non-negative)

*Data Quality:*
- Model converged successfully (check log + summary file)
- Domain x Time interaction term present in fixed_effects.csv
- Dual p-values present for all terms (Decision D068)
- Residuals approximately normal (diagnostic check)
- No severe heteroscedasticity (diagnostic check)

*Log Validation:*
- Required: "LMM fitting complete"
- Required: "Model converged: True"
- Required: "VALIDATION - PASS: LMM assumptions acceptable"
- Required: "Domain x Time interaction: p = X.XXX" (primary hypothesis test)
- Forbidden: "ERROR", "CONVERGENCE FAILED", "Singular convergence"
- Acceptable: "Warning: Minor heteroscedasticity detected" (common in real data)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step05_fit_lmm.log
- Quit script immediately
- g_debug invoked

---

### Step 6: Post-Hoc Contrasts (If Interaction Significant)

**Dependencies:** Step 5 (requires LMM fitted model)
**Complexity:** Low (10 minutes - pairwise contrasts)

**Purpose:** If Domain x Time interaction significant (p < 0.05), compute post-hoc pairwise domain comparisons. Apply Bonferroni correction per Decision D068. If interaction NULL (p >= 0.05), document and skip contrasts.

**Input:**

**File 1:** data/step05_lmm_model_summary.txt (from Step 5)
**File 2:** data/step05_fixed_effects.csv (from Step 5)
**File 3:** data/step04_lmm_input.csv (raw data for contrasts)

**Processing:**

1. Check Domain x Time interaction p-value from Step 5
2. **IF p < 0.05 (interaction significant):**
   - Compute pairwise domain contrasts: What vs Where, When vs others (if When included)
   - Report BOTH uncorrected AND Bonferroni-corrected p-values (Decision D068)
   - Compute Cohen's d effect sizes for contrasts
3. **IF p >= 0.05 (interaction NULL - expected hypothesis):**
   - Document NULL finding
   - Skip contrasts (no post-hoc needed for non-significant interaction)
   - Create empty contrasts file with note

**Output:**

**File 1:** data/step06_post_hoc_contrasts.csv
**Format:** CSV, one row per contrast
**Columns:**
  - contrast (string, e.g., "What vs Where")
  - estimate (float, mean difference)
  - se (float)
  - t (float)
  - p_uncorrected (float)
  - p_bonferroni (float, Decision D068)
  - cohens_d (float, effect size)
**Expected Rows:** 0 (if interaction NULL) OR 2-3 (if interaction significant: What vs Where, When vs others)

**File 2:** data/step06_contrast_decision.txt
**Format:** Text file documenting decision
**Contents:**
  - Domain x Time interaction p-value
  - Decision: "Contrasts COMPUTED (interaction significant)" OR "Contrasts SKIPPED (interaction NULL - expected)"
  - Rationale

**Validation Requirement:**
Validation tools MUST be used after contrasts tool execution. Specific validation tools will be determined by rq_tools based on contrast requirements (dual p-values present, Bonferroni correction correct, effect sizes valid).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_post_hoc_contrasts.csv: 0-3 rows x 7 columns
- data/step06_contrast_decision.txt: Text file exists with decision documented
- Data types: estimate (float), se (float >0), t (float), p (float in [0,1]), cohens_d (float)

*Value Ranges:*
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1], p_bonferroni >= p_uncorrected
- cohens_d: unrestricted (can be negative for directional contrasts)
- se > 0

*Data Quality:*
- If contrasts.csv has rows: ALL rows have dual p-values (Decision D068 enforced)
- contrast_decision.txt explicitly states contrast status
- Bonferroni correction mathematically correct (p_bonf = min(p_uncorr * N_contrasts, 1.0))

*Log Validation:*
- Required: "Domain x Time interaction: p = X.XXX"
- Required: "Contrast decision: COMPUTED" OR "Contrast decision: SKIPPED (NULL interaction)"
- If computed: "VALIDATION - PASS: Dual p-values present"
- Forbidden: "ERROR", "Missing Bonferroni correction"
- Acceptable: None expected

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step06_compute_post_hoc_contrasts.log
- Quit script immediately
- g_debug invoked

---

### Step 7: Prepare Trajectory Plot Data (Dual-Scale per Decision D069)

**Dependencies:** Steps 3, 4 (requires theta_long.csv, lmm_input.csv, LMM fitted model from Step 5)
**Complexity:** Low (10 minutes - data aggregation for plotting)

**Purpose:** Create plot source CSVs for trajectory visualization (Option B architecture). Decision D069 requires BOTH theta-scale AND probability-scale plots for interpretability.

**Plot Description:** Trajectory over time with confidence bands showing theta_confidence decline across memory domains (What/Where or What/Where/When). Dual-scale presentation (theta + probability) for non-psychometrician interpretability.

**Required Data Sources:**
- data/step03_theta_long.csv (theta estimates per domain)
- data/step04_lmm_input.csv (TSVR_hours time variable)
- Step 5 LMM fitted model (predicted values + CIs)

**Aggregation Logic:**
1. Merge theta_long with lmm_input on composite_ID + domain (adds TSVR_hours)
2. Group by domain + test, compute:
   - Mean theta per domain per timepoint
   - 95% CI (±1.96 * SE_mean)
   - Sample size per cell
3. Extract LMM predicted values + CIs from Step 5 model
4. **Theta-scale CSV:** Raw theta values (-4 to +4 range)
5. **Probability-scale CSV:** Transform theta to probability using IRT conversion (Decision D069)
6. Sort by domain, then time
7. Save to data/step07_trajectory_theta_data.csv and data/step07_trajectory_probability_data.csv

**Output:**

**File 1:** data/step07_trajectory_theta_data.csv
**Format:** CSV, plot source data for theta-scale trajectory
**Columns:**
  - time (float, TSVR_hours: 0, 24, 72, 144 nominal)
  - theta (float, mean theta per domain per timepoint)
  - CI_lower (float, lower 95% confidence bound)
  - CI_upper (float, upper 95% confidence bound)
  - domain (string, What/Where or What/Where/When)
  - n (int, sample size per cell)
**Expected Rows:** 8 (if When excluded: 2 domains x 4 timepoints) OR 12 (if When included: 3 domains x 4 timepoints)

**File 2:** data/step07_trajectory_probability_data.csv
**Format:** CSV, plot source data for probability-scale trajectory (Decision D069 dual-scale)
**Columns:** Same as theta_data but with probability values (0-1 scale)
**Expected Rows:** 8 OR 12 (matches theta_data)

**Validation Requirement:**
Validation tools MUST be used after plot data preparation tool execution. Specific validation tools will be determined by rq_tools based on plot data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_trajectory_theta_data.csv: 8 or 12 rows x 6 columns
- data/step07_trajectory_probability_data.csv: 8 or 12 rows x 6 columns
- Data types: time (float), theta/probability (float), CI bounds (float), domain (string), n (int)

*Value Ranges:*
- time in [0, 168] hours
- theta in [-4, 4]
- probability in [0, 1] (theta-scale transformation valid)
- CI_lower < CI_upper for all rows
- n > 0 (all cells have data)

*Data Quality:*
- No NaN values tolerated (all cells must have valid values)
- Expected N: Exactly 8 rows (if 2-factor) OR 12 rows (if 3-factor)
- No duplicate rows (domain x time combinations unique)
- All domains represented: What + Where (minimum) or What + Where + When
- Row counts match between theta_data and probability_data (same observations)

*Log Validation:*
- Required: "Plot data preparation complete: N rows created" (N=8 or 12)
- Required: "All domains represented: What, Where" OR "What, Where, When"
- Required: "Dual-scale data created: theta + probability (Decision D069)"
- Forbidden: "ERROR", "NaN values detected", "Missing domain"
- Acceptable: None expected

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Expected 12 rows, found 9")
- Log failure to logs/step07_prepare_trajectory_plot_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- g_debug invoked

**Plotting Function (rq_plots will call later):** Trajectory plot with confidence bands
- rq_plots agent maps to tools/plots.py functions (plot_trajectory for theta, plot_trajectory_probability for probability)
- Plots read data/step07_trajectory_*.csv (created by this step)
- NO data aggregation in rq_plots (visualization only per Option B)
- PNG outputs saved to plots/ folder by rq_plots (NOT by this step)

---

### Step 8: Document Comparison to Ch5 5.2.1 Accuracy Findings

**Dependencies:** Steps 5, 6 (requires LMM results + contrast results)
**Complexity:** Low (5 minutes - summary documentation)

**Purpose:** Compare confidence domain findings (this RQ) to accuracy domain findings (Ch5 5.2.1) to test convergence/divergence between metacognitive monitoring and objective performance.

**Input:**

**File 1:** data/step05_fixed_effects.csv (Domain x Time interaction from this RQ)
**File 2:** data/step06_post_hoc_contrasts.csv (domain contrasts if interaction significant)
**File 3:** results/ch5/5.2.1/data/step05_fixed_effects.csv (Ch5 accuracy domain interaction - external reference)

**Processing:**

1. Load this RQ's Domain x Time interaction p-value
2. Load Ch5 5.2.1 accuracy Domain x Time interaction p-value (if available)
3. Document convergence or divergence:
   - **Convergence:** Both NULL (p > 0.05) - supports unitized VR encoding hypothesis
   - **Divergence:** Confidence significant but accuracy NULL - suggests metacognitive monitoring dissociation
4. Document When domain status (included/excluded) and rationale
5. Create comparison summary table

**Output:**

**File:** data/step08_ch5_comparison.csv
**Format:** CSV, comparison summary
**Columns:**
  - measure (string, "Confidence" vs "Accuracy")
  - rq_id (string, "6.3.1" vs "5.2.1")
  - domain_time_interaction_p (float)
  - result (string, "NULL" or "SIGNIFICANT")
  - interpretation (string, brief summary)
**Expected Rows:** 2 (one for confidence, one for accuracy)

**File 2:** data/step08_when_domain_status.txt
**Format:** Text file documenting When domain inclusion/exclusion
**Contents:**
  - When domain status: INCLUDED or EXCLUDED
  - Post-purification item count
  - Rationale (floor effects in Ch5 if excluded)
  - Impact on analysis (2-factor vs 3-factor model)

**Validation Requirement:**
Validation tools MUST be used after comparison documentation tool execution. Specific validation tools will be determined by rq_tools based on documentation requirements (files exist, content complete, interpretations valid).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_ch5_comparison.csv: 2 rows x 5 columns
- data/step08_when_domain_status.txt: Text file exists
- Data types: measure (string), rq_id (string), domain_time_interaction_p (float in [0,1]), result (string), interpretation (string)

*Value Ranges:*
- domain_time_interaction_p in [0, 1]
- result in {"NULL", "SIGNIFICANT"}

*Data Quality:*
- Both rows present (Confidence + Accuracy)
- Confidence row matches this RQ's Step 5 findings
- Interpretation non-empty
- when_domain_status.txt explicitly states INCLUDED or EXCLUDED

*Log Validation:*
- Required: "Ch5 comparison complete"
- Required: "When domain status documented: INCLUDED" OR "EXCLUDED"
- Forbidden: "ERROR", "Missing Ch5 data"
- Acceptable: "Note: Ch5 5.2.1 data not yet available - comparison pending" (if Ch5 incomplete)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step08_document_ch5_comparison.log
- Quit script immediately
- g_debug invoked

---

## Expected Data Formats

### Composite ID Format
- Pattern: `{UID}_{test}`
- Example: `P001_T1`, `P042_T3`
- Components:
  - UID: Participant identifier (P### with leading zeros)
  - test: Test session (T1, T2, T3, T4 for Days 0, 1, 3, 6)

### Domain Coding
- **2-factor model** (if When excluded): What, Where
- **3-factor model** (if When included): What, Where, When
- String values, not numeric codes

### Time Variable (Decision D070)
- **Primary:** TSVR_hours (actual hours since encoding)
- **Transformations:** log_TSVR, TSVR_squared (for functional form exploration)
- **NOT nominal days** (0, 1, 3, 6 are approximations - TSVR is actual elapsed time)

### IRT Item Format
- **Item naming:** TC_* tags from dfData.csv (5-category ordinal confidence: 0, 0.25, 0.5, 0.75, 1.0)
- **NOT TQ_* tags** (those are accuracy items used in Ch5)

### Q-Matrix Structure
- **Rows:** One per item
- **Columns:** item_name, dimension (int 1-3), domain (string for readability)
- **Dimensionality:** 2 or 3 factors depending on When domain status

---

## Cross-RQ Dependencies

**Data Type:** RAW (extracts directly from dfData.csv)

**No dependencies on other RQs for data extraction.** This RQ is self-contained.

**External Reference (for comparison only):**
- Ch5 5.2.1 accuracy domain analysis results (Step 8 comparison)
- Reference file: results/ch5/5.2.1/data/step05_fixed_effects.csv
- Used for: Documentation comparison only (NOT required for analysis execution)
- Status: Optional - if Ch5 5.2.1 incomplete, Step 8 notes "comparison pending"

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

#### Step 0: Extract Confidence Item Data
- Output files exist (irt_input.csv, tsvr_mapping.csv, q_matrix.csv)
- Expected dimensions (400 rows, ~103 columns for irt_input)
- TC_* item values in {0.0, 0.25, 0.5, 0.75, 1.0} (ordinal scale)
- TSVR_hours in valid range [0, 168]
- Q-matrix has 3 dimensions (What, Where, When)
- No unexpected NaN patterns (>50% missing per item = extraction error)

#### Step 1: IRT Calibration Pass 1
- Model converged (log-likelihood improved, not NaN)
- Item parameters in valid ranges (a in [0, 10], b in [-6, 6])
- No NaN in item parameters (all items calibrated successfully)
- Theta estimates in valid range ([-4, 4])
- Standard errors reasonable ([0.1, 1.5])

#### Step 2: Item Purification
- Purification thresholds enforced (a >= 0.4, |b| <= 3.0)
- At least 10 items per dimension (or When excluded if <10)
- Purified Q-matrix matches purified item list
- purification_report.txt documents When status

#### Step 3: IRT Calibration Pass 2
- Model converged on purified items
- Improved fit vs Pass 1 (expected)
- Theta_long row count correct (800 or 1200 depending on When status)
- All 400 composite_IDs present

#### Step 4: Merge Theta with TSVR
- 100% merge rate (all theta observations have TSVR data)
- Time transformations mathematically correct
- No NaN in TSVR_hours (all observations have time data)

#### Step 5: Fit LMM
- Model converged successfully
- Domain x Time interaction term present
- Dual p-values for all terms (Decision D068)
- Residuals approximately normal
- No severe heteroscedasticity

#### Step 6: Post-Hoc Contrasts
- IF interaction significant: dual p-values present (Decision D068)
- Bonferroni correction mathematically correct
- contrast_decision.txt documents status

#### Step 7: Prepare Trajectory Plot Data
- Dual-scale data created (theta + probability per Decision D069)
- Expected row count (8 or 12 depending on When status)
- No NaN values
- CI_lower < CI_upper for all rows

#### Step 8: Document Ch5 Comparison
- Comparison file has 2 rows (Confidence + Accuracy)
- When domain status documented explicitly

---

## Summary

**Total Steps:** 8 (Step 0: extraction + Steps 1-7: analysis)

**Estimated Runtime:** High (2-3 hours total)
- Step 0: 5-10 min (extraction)
- Step 1: 45-60 min (Pass 1 IRT - dominates runtime)
- Step 2: 5 min (purification)
- Step 3: 45-60 min (Pass 2 IRT - dominates runtime)
- Step 4: 5 min (merge)
- Step 5: 15-30 min (LMM fitting)
- Step 6: 10 min (contrasts)
- Step 7: 10 min (plot data prep)
- Step 8: 5 min (documentation)

**Cross-RQ Dependencies:** None (RAW data only from dfData.csv)

**Primary Outputs:**
- data/step03_theta_long.csv (final confidence ability estimates per domain)
- data/step05_fixed_effects.csv (Domain x Time interaction test - primary hypothesis)
- data/step06_post_hoc_contrasts.csv (domain comparisons if interaction significant)
- data/step07_trajectory_theta_data.csv + data/step07_trajectory_probability_data.csv (plot source CSVs for rq_plots)
- data/step08_ch5_comparison.csv (confidence vs accuracy domain pattern comparison)
- data/step08_when_domain_status.txt (When inclusion/exclusion documentation)

**Validation Coverage:** 100% (all 8 steps have validation requirements with 4-layer substance criteria)

**Critical Decision Points:**
1. When domain status (Step 2): Include if >=10 items post-purification, exclude if <10
2. Contrast computation (Step 6): Compute if interaction significant, skip if NULL (expected)
3. Time transformation (Step 5): Use log_TSVR if Ch6 prior RQs support, else TSVR_hours linear

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent for RQ 6.3.1
