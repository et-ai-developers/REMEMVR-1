# Analysis Plan for RQ 5.1.6: Item Difficulty Interaction

**Created by:** rq_planner agent
**Date:** 2025-12-02
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This RQ examines whether item difficulty (IRT parameter 'b' from RQ 5.2.1) moderates forgetting rate, testing three competing theoretical predictions: (1) easier items show faster forgetting (positive interaction), (2) easier items show slower forgetting due to ceiling effects (negative interaction), or (3) difficulty affects baseline only, not forgetting rate (no interaction). Analysis uses cross-classified binomial GLMM with item-level binary responses (~28,000-42,000 observations from 100 participants x 4 tests x 70-105 purified items).

**Pipeline:** GLMM only (no IRT calibration - uses DERIVED item parameters from RQ 5.2.1)
**Steps:** 8 total analysis steps (Step 0: load dependencies -> Step 7: plot data preparation)
**Estimated Runtime:** High (90-120 minutes total - Step 4 GLMM fitting is computationally intensive with crossed random effects)

**Key Decisions Applied:**
- Decision D068: Single planned comparison (Time:Difficulty_c interaction), alpha=0.05, no Bonferroni correction (exploratory analysis)
- Decision D070: TSVR_hours as time variable (actual elapsed time, not nominal days)
- **NOT** Decision D039: No 2-pass IRT purification (RQ uses DERIVED item parameters from RQ 5.2.1)
- **NOT** Decision D069: No dual-scale plots (GLMM uses probability scale natively via inverse logit, not theta scale)

**Critical Dependencies:**
- RQ 5.2.1 must complete Step 3 (IRT Pass 2 item parameters available)
- Item difficulty range expected: approximately -3 to +3 (IRT difficulty 'b' parameter)
- Expected ~70-105 purified items (30-70% retention from RQ 5.2.1)

---

## Analysis Plan

### Step 0: Load Item Difficulty Parameters from RQ 5.2.1

**Dependencies:** None (first step, but requires RQ 5.2.1 completion)
**Complexity:** Low (<5 minutes - file loading and validation only)

**Purpose:** Load IRT item difficulty parameters ('b' values) from RQ 5.2.1 Pass 2 calibration to use as predictor variable in GLMM.

**Input:**

**File 1:** results/ch5/5.2.1/data/step03_item_parameters.csv
**Source:** RQ 5.2.1 Step 3 (IRT Pass 2 calibration on purified items)
**Format:** CSV with columns:
- `item_name` (string, VR item tag format: VR-{paradigm}-{test}-{domain}-ANS)
- `dimension` (string, domain grouping: "what", "where", "when")
- `a` (float, IRT discrimination parameter, range typically 0.4 to 4.0)
- `b` (float, IRT difficulty parameter, range typically -3.0 to +3.0, unrestricted)
- Additional columns may exist (c parameters, thresholds, etc.)

**Expected Rows:** 70-105 items (post-purification from RQ 5.2.1 applying Decision D039 thresholds)

**File 2:** results/ch5/5.2.1/data/step00_tsvr_mapping.csv
**Source:** RQ 5.2.1 Step 0 (TSVR extraction from master.xlsx)
**Format:** CSV with columns:
- `UID` (string, participant ID format: P### with leading zeros)
- `test` (string, test session: T1, T2, T3, T4)
- `TSVR_hours` (float, actual hours since VR encoding session)
- `composite_ID` (string, format: {UID}_{test})

**Expected Rows:** 400 (100 participants x 4 tests)

**Processing:**
1. Read item parameters CSV using pandas
2. Validate required columns exist: item_name, dimension, a, b
3. Filter to columns needed: item_name, b (difficulty only - discrimination 'a' not used in GLMM)
4. Validate item difficulty range: approximately -3 to +3 (extreme values acceptable for temporal items)
5. Validate no NaN values in 'b' column (all items must have difficulty estimates)
6. Read TSVR mapping CSV
7. Validate required columns: UID, test, TSVR_hours, composite_ID
8. Validate TSVR_hours range: 0 to 240 hours (0=encoding, 240=Day 6 @ 24h/day x 6 days + variance)
9. Validate no NaN in TSVR_hours (all observations must have timing data)

**Output:**

**File 1:** data/step00_item_difficulty.csv
**Format:** CSV, one row per item
**Columns:**
- `item_name` (string, item tag)
- `b` (float, IRT difficulty parameter)
- `dimension` (string, domain for reference: "what", "where", "when")
**Expected Rows:** 70-105 items (depends on RQ 5.2.1 purification results)

**File 2:** data/step00_tsvr_mapping.csv
**Format:** CSV, one row per participant-test combination
**Columns:**
- `UID` (string)
- `test` (string)
- `TSVR_hours` (float)
- `composite_ID` (string)
**Expected Rows:** 400

**Validation Requirement:**

Validation tools MUST be used after data loading execution. Specific validation tools will be determined by rq_tools based on file format requirements (CSV structure validation, required columns check, data type validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_item_difficulty.csv: 70-105 rows x 3 columns (item_name: object, b: float64, dimension: object)
- data/step00_tsvr_mapping.csv: 400 rows x 4 columns (UID: object, test: object, TSVR_hours: float64, composite_ID: object)

*Value Ranges:*
- b (difficulty) in [-6, 6] (extreme values rare but possible, especially for temporal items)
- TSVR_hours in [0, 240] (0=encoding, 240=approximately 6 days + measurement variance)

*Data Quality:*
- No NaN values in b column (all items must have difficulty estimates)
- No NaN values in TSVR_hours column (all observations must have timing data)
- Item count 70-105 (expected retention rate from RQ 5.2.1: 30-70%)
- Expected N: Exactly 400 rows in TSVR mapping (100 participants x 4 tests)
- No duplicate item_name values (items must be unique)
- No duplicate composite_ID values (participant-test combinations must be unique)

*Log Validation:*
- Required pattern: "Loaded {N} items from RQ 5.2.1" where N in [70, 105]
- Required pattern: "Loaded 400 TSVR observations"
- Required pattern: "VALIDATION - PASS: Item difficulty range check"
- Required pattern: "VALIDATION - PASS: TSVR range check"
- Forbidden patterns: "ERROR", "FileNotFoundError", "KeyError", "NaN values detected"
- Acceptable warnings: None expected (dependency RQ must be complete before this RQ runs)

**Expected Behavior on Validation Failure:**

If RQ 5.2.1 files missing: Raise FileNotFoundError with message "RQ 5.2.1 must complete Step 3 before running RQ 5.1.6"
If item count < 70: Raise ValueError with message "Insufficient items retained (expected >= 70, found {N})"
If NaN detected: Raise ValueError with specific column name "NaN values in column {column_name}"
Validation failure -> Log to logs/step00_load_item_difficulty.log -> Quit immediately -> g_debug invoked

---

### Step 1: Extract and Reshape Raw Response Data

**Dependencies:** Step 0 (requires item list to filter dfData.csv)
**Complexity:** Medium (10-15 minutes - large file read, filtering, reshaping ~28k-42k observations)

**Purpose:** Extract binary item-level responses from dfData.csv for items retained in RQ 5.2.1, reshape from wide format (one row per UID x test) to long format (one row per UID x test x item) for item-level GLMM analysis.

**Input:**

**File 1:** data/cache/dfData.csv
**Source:** Project-level RAW data cache (all VR responses)
**Format:** Wide-format CSV with columns:
- `UID` (string, participant ID)
- `TEST` (string, test session: T1/T2/T3/T4)
- Item columns: VR-{paradigm}-{test}-{domain}-ANS (integer values 0-4 representing TQ scores)
- Approximately 850+ item columns (full VR battery before purification)

**Expected Rows:** ~400 (100 participants x 4 tests, may have slight attrition)

**File 2:** data/step00_item_difficulty.csv (from Step 0)
**Purpose:** Item list filter (only extract items with difficulty parameters)

**Processing:**
1. Read dfData.csv (large file, ~850 columns)
2. Read item difficulty file to get list of retained items
3. Filter dfData.csv to include only UID, TEST columns + retained item columns (70-105 items)
4. Dichotomize item responses: TQ < 1 -> 0 (incorrect), TQ >= 1 -> 1 (correct)
   - Rationale: Binomial GLMM requires binary outcomes (0/1), not ordinal (0-4)
   - Loss of information acknowledged (ordinal -> binary), justified by analytical necessity
5. Reshape from wide to long format using pd.melt():
   - Wide: One row per UID x TEST, items as columns
   - Long: One row per UID x TEST x item_name observation
   - Columns after melt: UID, TEST, item_name, response (binary 0/1)
6. Create composite_ID column: {UID}_{TEST} for merging with TSVR
7. Validate expected row count: ~400 x ~87.5 (midpoint of 70-105) = ~35,000 rows
   - Actual range: 28,000 (400 x 70) to 42,000 (400 x 105) depending on RQ 5.2.1 retention

**Output:**

**File:** data/step01_response_level_data.csv
**Format:** CSV, long format (one row per item-level observation)
**Columns:**
- `UID` (string, participant ID)
- `TEST` (string, test session: T1/T2/T3/T4)
- `composite_ID` (string, format: {UID}_{TEST})
- `item_name` (string, VR item tag)
- `response` (int, binary 0=incorrect, 1=correct)

**Expected Rows:** 28,000 to 42,000 (100 participants x 4 tests x 70-105 items)
**Data Type:** All string except response (int64, values: 0 or 1)

**Validation Requirement:**

Validation tools MUST be used after data extraction and reshaping execution. Specific validation tools determined by rq_tools (likely data format validation, binary response check, row count validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_response_level_data.csv exists (exact path)
- Expected rows: 28,000 to 42,000 (depends on RQ 5.2.1 item retention)
- Expected columns: 5 (UID, TEST, composite_ID, item_name, response)
- Data types: UID (object), TEST (object), composite_ID (object), item_name (object), response (int64)

*Value Ranges:*
- response in {0, 1} ONLY (binary outcomes required for binomial GLMM)
- No values outside {0, 1} tolerated (no 2, 3, 4, NaN)

*Data Quality:*
- No NaN values in response column (missing data handled via exclusion, not NaN coding)
- Expected N: 28,000 to 42,000 rows (calculated as N_participants x N_tests x N_items)
- All composite_ID values must match Step 0 TSVR mapping (400 unique composite_IDs)
- All item_name values must match Step 0 item difficulty list (70-105 unique items)
- Response distribution: approximately 50-70% correct responses expected (memory task, some forgetting)

*Log Validation:*
- Required pattern: "Reshaped data: {N} observations created" where N in [28000, 42000]
- Required pattern: "VALIDATION - PASS: Binary response check (all values in {0, 1})"
- Required pattern: "VALIDATION - PASS: Composite ID match (400 unique)"
- Required pattern: "VALIDATION - PASS: Item name match ({N} unique)" where N in [70, 105]
- Forbidden patterns: "ERROR", "Non-binary response detected", "Item mismatch"
- Acceptable warnings: "Some participants missing data for specific items" (real-world missing data acceptable)

**Expected Behavior on Validation Failure:**

If response values outside {0, 1}: Raise ValueError "Non-binary response detected: {unique_values}"
If composite_ID mismatch: Raise ValueError "Composite IDs do not match TSVR mapping"
If item_name mismatch: Raise ValueError "Item names do not match item difficulty list"
Validation failure -> Log to logs/step01_extract_response_data.log -> Quit immediately -> g_debug invoked

---

### Step 2: Merge Item Difficulty and TSVR into Response Data

**Dependencies:** Steps 0 and 1 (requires item difficulty, TSVR mapping, and response data)
**Complexity:** Low (5-10 minutes - two merge operations on large DataFrame)

**Purpose:** Create analysis-ready dataset by merging item-level difficulty predictor (from RQ 5.2.1) and time variable (TSVR_hours) into response-level data. This creates the input for cross-classified GLMM.

**Input:**

**File 1:** data/step01_response_level_data.csv (from Step 1)
**Rows:** 28,000 to 42,000
**Columns:** UID, TEST, composite_ID, item_name, response

**File 2:** data/step00_item_difficulty.csv (from Step 0)
**Rows:** 70-105
**Columns:** item_name, b (difficulty), dimension

**File 3:** data/step00_tsvr_mapping.csv (from Step 0)
**Rows:** 400
**Columns:** UID, test, TSVR_hours, composite_ID

**Processing:**
1. Read all three input files
2. **Merge 1:** Left join response data with item difficulty on item_name
   - Key: item_name (must match exactly between files)
   - Type: Left join (keep all response observations, add difficulty values)
   - Validation: No NaN in 'b' column after merge (all items must have difficulty)
3. **Merge 2:** Left join result with TSVR mapping on composite_ID
   - Key: composite_ID (format: {UID}_{TEST})
   - Type: Left join (keep all observations, add TSVR_hours)
   - Validation: No NaN in TSVR_hours after merge (all observations must have timing)
4. Rename TEST -> test (lowercase for consistency with TSVR mapping)
5. Select final columns: UID, test, composite_ID, item_name, response, b (difficulty), TSVR_hours, dimension
6. Sort by UID, test, item_name for reproducibility and readability
7. Validate final row count matches Step 1 (no rows lost in merge)

**Output:**

**File:** data/step02_merged_data.csv
**Format:** CSV, long format (one row per item-level observation)
**Columns:**
- `UID` (string)
- `test` (string, lowercase: t1/t2/t3/t4)
- `composite_ID` (string)
- `item_name` (string)
- `response` (int, binary 0/1)
- `b` (float, item difficulty from IRT)
- `TSVR_hours` (float, actual time since encoding)
- `dimension` (string, domain: "what"/"where"/"when" for reference)

**Expected Rows:** 28,000 to 42,000 (same as Step 1 - no rows lost in merge)
**Expected Columns:** 8

**Validation Requirement:**

Validation tools MUST be used after merge execution. Specific validation tools determined by rq_tools (merge validation, NaN check, row count consistency).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_merged_data.csv exists
- Expected rows: 28,000 to 42,000 (EXACTLY matches Step 1 row count - no data loss)
- Expected columns: 8
- Data types: UID/test/composite_ID/item_name/dimension (object), response (int64), b/TSVR_hours (float64)

*Value Ranges:*
- response in {0, 1} (binary outcomes)
- b (difficulty) in [-6, 6] (IRT difficulty range)
- TSVR_hours in [0, 240] (time since encoding range)
- dimension in {"what", "where", "when"} (three memory domains)

*Data Quality:*
- **CRITICAL:** No NaN values in any column (merges must be complete)
- Row count exactly matches Step 1 (merge should add columns, not filter rows)
- All 400 unique composite_IDs present (no participant-test combinations lost)
- All 70-105 unique item_names present (no items lost)
- Distribution check: mean(response) approximately 0.50 to 0.70 (expected accuracy range)

*Log Validation:*
- Required pattern: "Merge 1 complete: {N} rows retained" where N matches Step 1
- Required pattern: "Merge 2 complete: {N} rows retained" where N matches Step 1
- Required pattern: "VALIDATION - PASS: No NaN values after merge"
- Required pattern: "VALIDATION - PASS: Row count preserved ({N} rows)"
- Forbidden patterns: "ERROR", "NaN detected after merge", "Rows lost in merge"
- Acceptable warnings: None expected (merge is deterministic operation)

**Expected Behavior on Validation Failure:**

If NaN in 'b' after Merge 1: Raise ValueError "Item difficulty missing for items: {item_list}"
If NaN in TSVR_hours after Merge 2: Raise ValueError "TSVR missing for composite_IDs: {id_list}"
If row count mismatch: Raise ValueError "Expected {N_step1} rows, found {N_actual} after merge"
Validation failure -> Log to logs/step02_merge_data.log -> Quit immediately -> g_debug invoked

---

### Step 3: Grand-Mean Center Item Difficulty

**Dependencies:** Step 2 (requires merged data with difficulty values)
**Complexity:** Low (<5 minutes - simple transformation and validation)

**Purpose:** Create grand-mean centered difficulty predictor (Difficulty_c) to facilitate interpretation of GLMM main effects and reduce multicollinearity between Time and Difficulty. Centering ensures Difficulty_c has mean approximately 0.

**Input:**

**File:** data/step02_merged_data.csv (from Step 2)
**Rows:** 28,000 to 42,000
**Columns:** UID, test, composite_ID, item_name, response, b (difficulty), TSVR_hours, dimension

**Processing:**
1. Read merged data
2. Compute grand mean of 'b' column across all observations
   - Grand mean computed on item-level (not participant-level) difficulty
   - Expected grand mean: approximately 0 (IRT difficulty centered around 0 by design, but may deviate)
3. Create Difficulty_c = b - grand_mean(b)
   - Centering makes mean(Difficulty_c) = 0
   - SD(Difficulty_c) = SD(b) (centering preserves variance)
4. Validate centering: mean(Difficulty_c) approximately 0 (tolerance: +/- 0.01)
5. Add Difficulty_c as new column to dataset
6. Retain original 'b' column for reference/validation

**Output:**

**File:** data/step03_difficulty_centered.csv
**Format:** CSV, long format
**Columns:**
- All columns from Step 2: UID, test, composite_ID, item_name, response, b, TSVR_hours, dimension
- **New column:** `Difficulty_c` (float, grand-mean centered difficulty)

**Expected Rows:** 28,000 to 42,000 (same as Step 2)
**Expected Columns:** 9 (8 from Step 2 + 1 new)

**Validation Requirement:**

Validation tools MUST be used after centering execution. Specific validation tools determined by rq_tools (centering validation, mean check, variance preservation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_difficulty_centered.csv exists
- Expected rows: 28,000 to 42,000 (matches Step 2 exactly)
- Expected columns: 9 (includes Difficulty_c)
- Data types: Difficulty_c (float64), all others same as Step 2

*Value Ranges:*
- Difficulty_c approximately in [-6, 6] (same range as 'b', but centered around 0)
- mean(Difficulty_c) approximately 0 (tolerance: +/- 0.01)
- SD(Difficulty_c) = SD(b) (variance preserved by centering)

*Data Quality:*
- No NaN values in Difficulty_c column (centering should not introduce NaN)
- mean(Difficulty_c) in [-0.01, 0.01] (CRITICAL for centering validation)
- Correlation(b, Difficulty_c) = 1.0 (perfect correlation - centering is linear transformation)
- Row count exactly matches Step 2 (transformation adds column, not rows)

*Log Validation:*
- Required pattern: "Grand mean difficulty: {value:.3f}" (report actual grand mean)
- Required pattern: "Centering complete: mean(Difficulty_c) = {value:.6f}" where |value| < 0.01
- Required pattern: "VALIDATION - PASS: Centering successful (mean approximately 0)"
- Required pattern: "VALIDATION - PASS: Variance preserved"
- Forbidden patterns: "ERROR", "Centering failed", "Mean deviation > 0.01"
- Acceptable warnings: "Grand mean differs from 0 by {delta}" (informational, not error)

**Expected Behavior on Validation Failure:**

If mean(Difficulty_c) > 0.01: Raise ValueError "Centering failed: mean(Difficulty_c) = {actual_mean}, expected ~0"
If SD mismatch: Raise ValueError "Variance not preserved: SD(b)={sd_b}, SD(Difficulty_c)={sd_dc}"
If NaN introduced: Raise ValueError "NaN values introduced during centering"
Validation failure -> Log to logs/step03_center_difficulty.log -> Quit immediately -> g_debug invoked

---

### Step 4: Fit Cross-Classified Binomial GLMM

**Dependencies:** Step 3 (requires centered difficulty predictor)
**Complexity:** High (60-90 minutes - computationally intensive due to crossed random effects structure with ~30k-42k observations)

**Purpose:** Fit cross-classified generalized linear mixed model to test whether item difficulty moderates forgetting rate. Model uses binomial family (logit link) with crossed random effects for participants (UID) and items (item_name). Primary hypothesis: Time:Difficulty_c interaction term significance.

**Input:**

**File:** data/step03_difficulty_centered.csv (from Step 3)
**Rows:** 28,000 to 42,000
**Columns:** UID, test, composite_ID, item_name, response, b, TSVR_hours, dimension, Difficulty_c

**Processing:**

**Model Specification:**

Formula: `response ~ TSVR_hours * Difficulty_c + (TSVR_hours | UID) + (1 | item_name)`

**Fixed Effects:**
- TSVR_hours: Main effect of time (forgetting trajectory on log-odds scale)
- Difficulty_c: Main effect of item difficulty (baseline difficulty on log-odds scale)
- TSVR_hours:Difficulty_c: **FOCAL INTERACTION** - tests if forgetting rate depends on item difficulty

**Random Effects:**
- (TSVR_hours | UID): Random intercepts and slopes by participant
  - Accounts for individual differences in baseline performance and forgetting rate
  - Allows each participant to have unique trajectory
  - Correlated random effects (intercept-slope correlation estimated)
- (1 | item_name): Random intercepts by item
  - Accounts for item-specific difficulty beyond IRT 'b' parameter
  - Captures residual item variation not explained by fixed difficulty predictor

**Model Family:** Binomial with logit link
- Response variable: Binary (0=incorrect, 1=correct)
- Link function: logit(p) = log(p / (1-p))
- Coefficients interpreted on log-odds scale
- Exponentiate coefficients for odds ratio interpretation

**Estimation Method:**

1. Use pymer4.Lmer() wrapper for lme4 backend
2. Initial attempt: Full model with nAGQ=1 (Laplace approximation, fastest)
   - Formula as specified above
   - family='binomial' (specifies logit link automatically)
   - Convergence check: model.converged attribute
3. If convergence fails (common with crossed random effects + large data):
   - **Fallback Tier 1:** Increase quadrature points nAGQ=7 (more accurate but slower)
   - **Fallback Tier 2:** Simplify to uncorrelated random effects (TSVR_hours || UID)
     - Removes intercept-slope correlation parameter
     - Reduces model complexity, often improves convergence
   - **Fallback Tier 3:** Remove random slopes (1 | UID) + (1 | item_name)
     - Intercepts-only random effects
     - Major simplification, but preserves crossed structure
   - **Fallback Tier 4:** Single grouping factor (1 | UID), remove item random effects
     - Last resort, loses item-level variance modeling
4. Document which model tier converged successfully
5. If all tiers fail: Report convergence failure as legitimate finding (model complexity exceeds data support)

**Model Comparison (if fallback used):**
- Conduct likelihood ratio test (LRT) comparing simplified model to full model
- Report chi-square, df, p-value
- Justify simplification statistically (not just for convergence)

**Output:**

**File 1:** data/step04_glmm_model_summary.txt
**Format:** Plain text, full pymer4 model summary
**Contents:**
- Fixed effects table: coefficient, SE, z-statistic, p-value for all 4 terms
- Random effects table: variance components for UID (intercept, slope, correlation) and item_name (intercept)
- Model fit: AIC, BIC, log-likelihood
- Convergence status: TRUE/FALSE with warnings if applicable
- Optimizer used: nAGQ value, lme4 backend version
- Sample size: N observations, N participants, N items

**File 2:** data/step04_convergence_log.txt
**Format:** Plain text, convergence diagnostics
**Contents:**
- Initial model attempt (nAGQ=1): Success/Failure
- Fallback tier used (if any): Tier 1/2/3/4 or None
- Convergence warnings: Exact lme4 warning messages (if any)
- LRT results (if fallback used): Chi-square, df, p-value comparing simplified to full model
- Recommendation: Which model to use for inference
- Rationale: Statistical justification for model selection

**File 3:** data/step04_fixed_effects.csv
**Format:** CSV, one row per fixed effect term
**Columns:**
- `term` (string, e.g., "TSVR_hours", "Difficulty_c", "TSVR_hours:Difficulty_c")
- `estimate` (float, log-odds coefficient)
- `SE` (float, standard error)
- `z` (float, z-statistic)
- `p` (float, p-value, two-tailed)

**Expected Rows:** 4 (Intercept, TSVR_hours, Difficulty_c, TSVR_hours:Difficulty_c)

**File 4:** data/step04_random_effects_variances.csv
**Format:** CSV, variance components
**Columns:**
- `grouping_factor` (string, "UID" or "item_name")
- `parameter` (string, "intercept", "slope", "correlation")
- `variance` (float, variance estimate)
- `SD` (float, standard deviation = sqrt(variance))

**Expected Rows:** 5 (UID: intercept variance, slope variance, correlation; item_name: intercept variance; residual variance if reported)

**Validation Requirement:**

Validation tools MUST be used after GLMM fitting execution. Specific validation tools determined by rq_tools (GLMM convergence check, fixed effects extraction validation, variance positivity check).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_glmm_model_summary.txt exists (full summary with >= 50 lines expected)
- data/step04_convergence_log.txt exists (convergence diagnostics)
- data/step04_fixed_effects.csv: 4 rows x 5 columns (term, estimate, SE, z, p)
- data/step04_random_effects_variances.csv: 3-5 rows (depends on final model structure)

*Value Ranges:*
- Fixed effect estimates (log-odds) typically in [-5, 5] (extreme values rare but possible)
- SE (standard errors) > 0 (must be positive and finite)
- z-statistics finite (no Inf or NaN)
- p-values in [0, 1] (valid probability range)
- Variance components > 0 (must be positive for all random effects)
- SD values > 0 (square root of variances, must be positive)

*Data Quality:*
- Model converged = TRUE (or Fallback Tier documented with LRT justification)
- All 4 fixed effect terms present (Intercept, TSVR_hours, Difficulty_c, TSVR_hours:Difficulty_c)
- No NaN or Inf in any coefficient or SE
- Variance components positive (negative variance indicates convergence failure)
- AIC and BIC finite (model fit indices must be computable)
- Expected focal test: TSVR_hours:Difficulty_c term has finite p-value (hypothesis test computable)

*Log Validation:*
- Required pattern: "Model converged: True" OR "Fallback Tier {N} converged: True"
- Required pattern: "VALIDATION - PASS: All variance components positive"
- Required pattern: "VALIDATION - PASS: Fixed effects table complete (4 terms)"
- Required pattern: "Fitted {N} observations, {N_UID} participants, {N_items} items"
- Forbidden patterns: "ERROR", "Convergence failure (all tiers failed)", "Negative variance", "NaN coefficient"
- Acceptable warnings: "Convergence warning: Model failed to converge initially, used Fallback Tier {N}" (fallback is expected and acceptable)

**Expected Behavior on Validation Failure:**

If all convergence tiers fail: Write convergence_log.txt documenting all attempts, QUIT with message "GLMM convergence failure across all 4 tiers - model complexity exceeds data support"
If negative variance detected: Raise ValueError "Negative variance detected for {grouping_factor} - indicates convergence failure"
If NaN in fixed effects: Raise ValueError "NaN coefficient for term {term_name} - model estimation failed"
If focal interaction missing: Raise ValueError "TSVR_hours:Difficulty_c term not found in fixed effects - model specification error"
Validation failure -> Log to logs/step04_fit_glmm.log -> Quit immediately -> g_debug invoked

**Critical Note on Runtime:**

This step is the computational bottleneck. Crossed random effects with 30k-42k observations require substantial memory and CPU time. Expected runtime: 60-90 minutes depending on convergence tier needed. User should be informed of expected duration before execution.

---

### Step 5: Validate GLMM Assumptions and Diagnostics

**Dependencies:** Step 4 (requires fitted GLMM model)
**Complexity:** Medium (15-20 minutes - multiple diagnostic checks on large dataset)

**Purpose:** Assess GLMM model assumptions (overdispersion, residual patterns, random effects normality) to ensure valid inference. Binomial GLMM assumptions differ from standard LMM - focus on overdispersion and random effects distribution.

**Input:**

**File 1:** data/step04_glmm_model_summary.txt (from Step 4)
**File 2:** data/step03_difficulty_centered.csv (original data for residual computation)
**File 3:** Fitted model object (in-memory from Step 4 or reloaded from saved .pkl if needed)

**Processing:**

**Diagnostic 1: Overdispersion Check**
- Compute dispersion parameter: residual deviance / residual df
- Expected value: approximately 1.0 for well-fitted binomial model
- Threshold: 0.8 to 1.2 acceptable, >1.5 indicates overdispersion (common with clustered data)
- If overdispersed: Note in report, consider quasi-binomial family (future work)
- Rationale: Overdispersion invalidates SE estimates (too narrow) -> conservative inference

**Diagnostic 2: Residual Patterns**
- Compute Pearson residuals: (observed - predicted) / sqrt(predicted variance)
- Visual check: Plot residuals vs fitted values on logit scale
- Expected pattern: Random scatter around 0, no systematic curvature
- Check for: Heteroscedasticity (fan-shaped pattern), non-linearity (curvature)
- Quantitative test: DHARMa package simulation-based residuals (if available), or visual inspection

**Diagnostic 3: Random Effects Normality**
- Extract random intercepts and slopes for UID (100 participants)
- Extract random intercepts for item_name (70-105 items)
- Q-Q plots for each random effect component
- Shapiro-Wilk test (if N < 5000 per component, otherwise visual only)
- Expected: Approximate normality (some deviation tolerable with large N)
- Severe non-normality (heavy skew, outliers) suggests model misspecification

**Diagnostic 4: Influential Observations**
- Identify participants or items with extreme random effects (> 3 SD from mean)
- Flag for sensitivity analysis (exclude and refit if > 5% of cases extreme)
- Document which UIDs or items are outliers

**Diagnostic 5: Linearity of Time Effect**
- Plot observed proportion correct vs TSVR_hours (binned)
- Overlay predicted probabilities from model
- Check: Linear decline on logit scale translates to nonlinear on probability scale (expected)
- If severe non-linearity: Consider polynomial time term (future work)

**Output:**

**File 1:** data/step05_glmm_diagnostics.txt
**Format:** Plain text report
**Contents:**
- Overdispersion statistic: value, interpretation (acceptable/overdispersed/underdispersed)
- Residual pattern description: Visual assessment (random/heteroscedastic/nonlinear)
- Random effects normality: Q-Q plot assessment, Shapiro-Wilk results (if computed)
- Influential observations: List of extreme UIDs/items with random effect values
- Linearity assessment: Observed vs predicted trajectory alignment
- Overall conclusion: Assumptions met/violated, impact on inference, recommendations

**File 2:** data/step05_overdispersion.csv
**Format:** CSV, single row
**Columns:**
- `residual_deviance` (float)
- `residual_df` (int)
- `dispersion_parameter` (float, = residual_deviance / residual_df)
- `interpretation` (string, "acceptable" / "overdispersed" / "underdispersed")

**File 3:** data/step05_random_effects_normality.csv
**Format:** CSV, one row per random effect component
**Columns:**
- `grouping_factor` (string, "UID" or "item_name")
- `parameter` (string, "intercept" or "slope")
- `shapiro_W` (float, Shapiro-Wilk test statistic, if N <= 5000)
- `shapiro_p` (float, p-value)
- `interpretation` (string, "approximately normal" / "non-normal")

**Expected Rows:** 3 (UID intercept, UID slope, item_name intercept)

**Validation Requirement:**

Validation tools MUST be used after diagnostics computation. Specific validation tools determined by rq_tools (diagnostics completeness check, value range validation, interpretation consistency).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_glmm_diagnostics.txt exists (>= 30 lines expected, comprehensive report)
- data/step05_overdispersion.csv: 1 row x 4 columns
- data/step05_random_effects_normality.csv: 3 rows x 5 columns

*Value Ranges:*
- dispersion_parameter typically in [0.5, 2.0] (values > 2 indicate severe overdispersion)
- shapiro_W in [0, 1] (test statistic range)
- shapiro_p in [0, 1] (p-value range)

*Data Quality:*
- Overdispersion parameter finite and positive
- Dispersion interpretation matches value (e.g., if dispersion > 1.2, interpretation should mention overdispersion)
- Shapiro-Wilk tests run for all 3 random effect components (or documented reason if skipped)
- No NaN in diagnostic statistics
- Diagnostics report addresses all 5 diagnostic categories listed above

*Log Validation:*
- Required pattern: "Overdispersion parameter: {value:.3f}" (value reported)
- Required pattern: "VALIDATION - PASS: Diagnostics complete (5 checks performed)"
- Required pattern: "Random effects normality assessed: {N} components tested"
- Forbidden patterns: "ERROR", "Diagnostic computation failed", "NaN in diagnostic"
- Acceptable warnings: "Overdispersion detected (parameter = {value})" (informational, not fatal error)
- Acceptable warnings: "Non-normality detected for {component}" (common with large N, often negligible impact)

**Expected Behavior on Validation Failure:**

If dispersion parameter > 2.0: Flag WARNING (not error) - "Severe overdispersion detected, consider quasi-binomial model"
If all random effects severely non-normal (p < 0.001): Flag WARNING - "Random effects non-normality may affect inference"
If diagnostic computation fails: Raise ValueError "Diagnostic {diagnostic_name} failed: {error_message}"
Validation failure (computation error, not assumption violation) -> Log to logs/step05_validate_glmm.log -> Quit immediately -> g_debug invoked

**Note:** Assumption violations (e.g., overdispersion, non-normality) are FLAGS, not errors. Analysis proceeds with documented limitations. Only computation failures (NaN, errors) trigger quit.

---

### Step 6: Extract and Report Time:Difficulty_c Interaction

**Dependencies:** Steps 4 and 5 (requires fitted GLMM and validated diagnostics)
**Complexity:** Low (5 minutes - extract focal term from fixed effects table)

**Purpose:** Extract the focal hypothesis test (Time:Difficulty_c interaction) from GLMM fixed effects table and report with interpretive statistics. This is the primary scientific finding: does item difficulty moderate forgetting rate?

**Input:**

**File 1:** data/step04_fixed_effects.csv (from Step 4)
**File 2:** data/step04_glmm_model_summary.txt (for context)

**Processing:**

1. Read fixed effects table
2. Filter to interaction term: TSVR_hours:Difficulty_c
3. Extract statistics: estimate (log-odds coefficient), SE, z-statistic, p-value
4. Compute odds ratio: OR = exp(estimate)
   - Interpretation: Multiplicative change in odds per unit change in difficulty x time
5. Compute 95% confidence interval for OR:
   - CI_lower = exp(estimate - 1.96 * SE)
   - CI_upper = exp(estimate + 1.96 * SE)
6. Determine statistical significance: p < 0.05 (single planned comparison, no Bonferroni)
7. Interpret coefficient sign on log-odds scale:
   - **Positive estimate:** Easier items (lower difficulty 'b') show faster forgetting
     - As difficulty decreases (items get easier), forgetting rate increases
     - Consistent with weak encoding hypothesis
   - **Negative estimate:** Easier items show slower forgetting
     - As difficulty decreases, forgetting rate decreases
     - Consistent with ceiling effect hypothesis
   - **Non-significant (p >= 0.05):** Difficulty affects baseline performance only, not forgetting rate
     - Null hypothesis: All items decay at same rate regardless of difficulty
8. Document interpretation with theoretical mapping to 3 competing predictions from concept.md

**Output:**

**File:** data/step06_difficulty_interaction.csv
**Format:** CSV, single row
**Columns:**
- `term` (string, "TSVR_hours:Difficulty_c")
- `estimate` (float, log-odds coefficient)
- `SE` (float, standard error)
- `z` (float, z-statistic)
- `p_value` (float, two-tailed p-value)
- `OR` (float, odds ratio = exp(estimate))
- `OR_CI_lower` (float, 95% CI lower bound)
- `OR_CI_upper` (float, 95% CI upper bound)
- `significant` (bool, TRUE if p < 0.05, FALSE otherwise)
- `interpretation` (string, "Positive: Easier -> Faster forgetting" / "Negative: Easier -> Slower forgetting" / "Null: No differential forgetting")
- `theoretical_prediction` (string, maps to one of 3 predictions from concept.md)

**Expected Rows:** 1

**Validation Requirement:**

Validation tools MUST be used after interaction extraction. Specific validation tools determined by rq_tools (term presence check, OR computation validation, interpretation consistency).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_difficulty_interaction.csv exists
- Expected rows: 1 (single focal term)
- Expected columns: 11 (term, estimate, SE, z, p_value, OR, OR_CI_lower, OR_CI_upper, significant, interpretation, theoretical_prediction)
- Data types: term/interpretation/theoretical_prediction (object), estimate/SE/z/p_value/OR/OR_CI_lower/OR_CI_upper (float64), significant (bool)

*Value Ranges:*
- estimate (log-odds) typically in [-2, 2] (extreme values rare for interactions)
- SE > 0 (must be positive)
- z-statistic finite (not Inf or NaN)
- p_value in [0, 1]
- OR > 0 (odds ratio must be positive)
- OR_CI_lower < OR < OR_CI_upper (CI bounds must bracket point estimate)

*Data Quality:*
- No NaN in any column
- OR computed correctly: OR = exp(estimate) (within floating-point precision)
- OR_CI computed correctly: exp(estimate +/- 1.96 * SE)
- significant field matches p < 0.05 threshold
- interpretation field matches estimate sign (positive estimate -> "Easier -> Faster forgetting")
- theoretical_prediction field maps to one of 3 predictions from concept.md

*Log Validation:*
- Required pattern: "Extracted TSVR_hours:Difficulty_c interaction: estimate = {estimate:.3f}, p = {p:.4f}"
- Required pattern: "Odds ratio: {OR:.3f}, 95% CI [{CI_lower:.3f}, {CI_upper:.3f}]"
- Required pattern: "Interpretation: {interpretation_text}"
- Required pattern: "VALIDATION - PASS: Interaction term extracted successfully"
- Forbidden patterns: "ERROR", "Interaction term not found", "NaN in results", "OR computation failed"
- Acceptable warnings: None expected (extraction is deterministic)

**Expected Behavior on Validation Failure:**

If interaction term missing: Raise KeyError "TSVR_hours:Difficulty_c not found in fixed effects table"
If OR computation incorrect: Raise ValueError "OR mismatch: expected {expected}, computed {actual}"
If interpretation inconsistent: Raise ValueError "Interpretation does not match coefficient sign"
Validation failure -> Log to logs/step06_extract_interaction.log -> Quit immediately -> g_debug invoked

---

### Step 7: Prepare Plot Data (Easy vs Hard Item Trajectories)

**Dependencies:** Steps 4 and 6 (requires fitted GLMM and interaction results)
**Complexity:** Medium (10-15 minutes - model predictions for plotting)

**Purpose:** Create plot source CSV comparing predicted probability trajectories for easy items (difficulty at -1SD) vs hard items (difficulty at +1SD) across 4 test sessions. Decision D069 does NOT apply (no dual-scale requirement for GLMM - plots use probability scale natively via inverse logit).

**Input:**

**File 1:** data/step04_glmm_model_summary.txt (fitted model coefficients)
**File 2:** data/step03_difficulty_centered.csv (for computing SD of Difficulty_c)
**File 3:** Fitted model object (for generating predictions)

**Processing:**

1. Compute SD of Difficulty_c across all observations (item-level SD)
2. Define easy items: Difficulty_c = -1 * SD(Difficulty_c)
3. Define hard items: Difficulty_c = +1 * SD(Difficulty_c)
4. Create prediction grid:
   - TSVR_hours: 0, 24, 72, 144 (nominal T1-T4 assuming exact 24h/day spacing)
   - Difficulty_c: {-1SD, +1SD}
   - UID: Fixed to "average participant" (random effects set to 0 for population-level trajectory)
   - item_name: Fixed to "average item" (random effects set to 0)
5. Generate model predictions on logit scale:
   - logit(p) = Intercept + beta_Time * TSVR_hours + beta_Difficulty * Difficulty_c + beta_Interaction * (TSVR_hours * Difficulty_c)
   - Random effects = 0 (population-average trajectory)
6. Transform to probability scale: p = 1 / (1 + exp(-logit(p)))
   - Decision D069 NOT applicable (no theta scale in GLMM context)
7. Compute 95% confidence intervals:
   - Use model variance-covariance matrix for fixed effects
   - Delta method for SE propagation to probability scale
   - CI_lower = p - 1.96 * SE(p)
   - CI_upper = p + 1.96 * SE(p)
   - Ensure CI in [0, 1] (truncate if needed)
8. Create two trajectories:
   - Easy items: 4 timepoints (T1-T4) at Difficulty_c = -1SD
   - Hard items: 4 timepoints (T1-T4) at Difficulty_c = +1SD
9. Label trajectories for plotting: "Easy Items (-1SD difficulty)" vs "Hard Items (+1SD difficulty)"

**Output:**

**File:** data/step07_difficulty_trajectories_data.csv
**Format:** CSV, plot source data
**Columns:**
- `TSVR_hours` (float, time values: 0, 24, 72, 144)
- `Difficulty_level` (string, "Easy (-1SD)" or "Hard (+1SD)")
- `Difficulty_c` (float, actual centered difficulty value: -1SD or +1SD)
- `predicted_probability` (float, model prediction on probability scale, range [0, 1])
- `CI_lower` (float, 95% CI lower bound, range [0, 1])
- `CI_upper` (float, 95% CI upper bound, range [0, 1])
- `test` (string, test session label: T1/T2/T3/T4 for plotting)

**Expected Rows:** 8 (2 difficulty levels x 4 timepoints)

**Validation Requirement:**

Validation tools MUST be used after plot data preparation. Specific validation tools determined by rq_tools (plot data format validation, probability range check, CI bounds validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_difficulty_trajectories_data.csv exists
- Expected rows: 8 (2 difficulty levels x 4 timepoints)
- Expected columns: 7
- Data types: TSVR_hours/Difficulty_c/predicted_probability/CI_lower/CI_upper (float64), Difficulty_level/test (object)

*Value Ranges:*
- TSVR_hours in {0, 24, 72, 144} (exact nominal values)
- Difficulty_c: one value approximately -1SD, one value approximately +1SD (SD computed from data)
- predicted_probability in [0, 1] (valid probability range)
- CI_lower in [0, 1] (truncated if prediction goes below 0)
- CI_upper in [0, 1] (truncated if prediction goes above 1)
- CI_lower < predicted_probability < CI_upper (CI must bracket point estimate, except at boundaries)

*Data Quality:*
- No NaN values in any column
- Exactly 8 rows (2 difficulty levels x 4 timepoints)
- Exactly 2 unique Difficulty_level values ("Easy (-1SD)", "Hard (+1SD)")
- Exactly 4 unique TSVR_hours values (0, 24, 72, 144)
- Expected pattern: predicted_probability decreases over time for both difficulty levels (forgetting trajectory)
- If interaction significant (from Step 6): Trajectories should diverge over time (non-parallel)
- If interaction non-significant: Trajectories should be approximately parallel (constant difference)

*Log Validation:*
- Required pattern: "SD(Difficulty_c) = {sd:.3f}"
- Required pattern: "Easy items Difficulty_c = {easy_value:.3f} (-1SD)"
- Required pattern: "Hard items Difficulty_c = {hard_value:.3f} (+1SD)"
- Required pattern: "Generated {N} predictions (2 difficulty levels x 4 timepoints)"
- Required pattern: "VALIDATION - PASS: All probabilities in [0, 1]"
- Required pattern: "VALIDATION - PASS: CI bounds valid"
- Forbidden patterns: "ERROR", "Probability out of bounds", "NaN in predictions", "CI invalid"
- Acceptable warnings: "CI truncated to [0, 1] at {timepoint}" (can happen at extreme values)

**Expected Behavior on Validation Failure:**

If probability out of [0, 1]: Raise ValueError "Predicted probability {value} outside valid range [0, 1]"
If CI_lower > CI_upper: Raise ValueError "Invalid CI bounds at TSVR_hours={time}: CI_lower={lower} > CI_upper={upper}"
If row count != 8: Raise ValueError "Expected 8 rows (2 difficulty x 4 time), found {N_actual}"
Validation failure -> Log to logs/step07_prepare_plot_data.log -> Quit immediately -> g_debug invoked

**Note on Plotting:**

This step creates plot SOURCE CSV in data/ folder. The actual PNG plot will be generated later by rq_plots agent (Step 15 workflow) reading this CSV and calling tools/plotting.py functions. Option B architecture: data manipulation (this step) separated from visualization (rq_plots).

---

## Expected Data Formats

### Long Format (Item-Level Observations)

This RQ uses **long format** data structure (one row per UID x test x item observation), NOT the typical wide format (one row per UID x test) used in other RQs. This is required for item-level GLMM with crossed random effects.

**Example Structure (Step 2 merged data):**

```
UID    | test | composite_ID | item_name              | response | b     | TSVR_hours | dimension
-------|------|--------------|------------------------|----------|-------|------------|----------
P001   | t1   | P001_t1      | VR-IFR-A01-N-ANS       | 1        | -0.52 | 0.0        | what
P001   | t1   | P001_t1      | VR-IFR-A01-L-ANS       | 0        | 1.23  | 0.0        | where
P001   | t1   | P001_t1      | VR-ICR-A01-O-ANS       | 1        | 0.87  | 0.0        | when
P001   | t2   | P001_t2      | VR-IFR-A01-N-ANS       | 1        | -0.52 | 28.5       | what
P001   | t2   | P001_t2      | VR-IFR-A01-L-ANS       | 0        | 1.23  | 28.5       | where
...
```

**Key Features:**
- **Rows:** One per unique combination of UID x test x item (28,000-42,000 total)
- **Repeated measures:** Same item appears 4 times (once per test session) for same UID
- **Item identifier:** item_name (VR tag) uniquely identifies items
- **Response:** Binary (0/1), NOT ordinal (0-4 TQ scores) - dichotomized in Step 1
- **Difficulty:** Item-level 'b' parameter merged from RQ 5.2.1, constant across UID and test for given item

### TSVR as Time Variable (Decision D070)

Per Decision D070, TSVR_hours (actual elapsed time in hours) is used as the time variable in GLMM, NOT nominal days (0, 1, 3, 6).

**Rationale:**
- Nominal days assume exact 24-hour intervals between tests
- Reality: Participants tested at variable times due to scheduling constraints
- TSVR_hours captures actual temporal precision
- Example: T2 may occur at 28.5 hours (not 24.0) due to session timing

**Expected TSVR Distribution:**
- T1 (Day 0): TSVR_hours approximately 0 (range: 0-2 hours, encoding session baseline)
- T2 (Day 1): TSVR_hours approximately 24 (range: 20-30 hours, 24 +/- 4 scheduling variance)
- T3 (Day 3): TSVR_hours approximately 72 (range: 68-80 hours, 72 +/- 8)
- T4 (Day 6): TSVR_hours approximately 144 (range: 136-156 hours, 144 +/- 12)

### Difficulty Centering (Step 3)

Item difficulty 'b' is grand-mean centered to create Difficulty_c:

**Formula:** Difficulty_c = b - mean(b)

**Properties:**
- mean(Difficulty_c) approximately 0 (tolerance: +/- 0.01)
- SD(Difficulty_c) = SD(b) (variance preserved)
- Centering DOES NOT change interpretation of interaction
- Centering DOES facilitate interpretation of main effects:
  - TSVR_hours coefficient = forgetting rate at average difficulty (Difficulty_c = 0)
  - Difficulty_c coefficient = difficulty effect at baseline (TSVR_hours = 0)

**Why Center:**
- Reduces multicollinearity between Time and Difficulty predictors
- Makes main effects interpretable (conditional on mean of other predictor)
- Standard practice for interaction models

### Cross-Classified Random Effects Structure

**Formula:** `(TSVR_hours | UID) + (1 | item_name)`

**Random Effects by UID (Participants):**
- **Random intercepts:** Each participant has unique baseline log-odds of correct response
- **Random slopes:** Each participant has unique forgetting rate (TSVR_hours effect)
- **Correlation:** Intercept-slope correlation estimated (do high performers forget faster or slower?)
- **N groups:** 100 participants

**Random Effects by item_name (Items):**
- **Random intercepts:** Each item has unique baseline log-odds (difficulty beyond fixed 'b' parameter)
- **NO random slopes:** Items do not have time-varying effects (same item difficulty across tests)
- **N groups:** 70-105 items (depends on RQ 5.2.1 purification)

**Crossed Structure:**
- Every participant responds to every item (complete crossing)
- NOT nested: Items not nested within participants, participants not nested within items
- Requires pymer4/lme4 for crossed random effects (statsmodels cannot fit crossed structure)

### Column Naming Conventions

Per names.md (populated from RQ 5.1):

| Variable | Column Name | Data Type | Description |
|----------|-------------|-----------|-------------|
| Participant ID | `UID` | string | Format: P### (leading zeros) |
| Test session | `test` | string | Lowercase: t1, t2, t3, t4 |
| Composite ID | `composite_ID` | string | Format: {UID}_{test} |
| Item identifier | `item_name` | string | VR tag: VR-{paradigm}-{test}-{domain}-ANS |
| Binary response | `response` | int | Values: {0, 1} only |
| IRT difficulty | `b` | float | Unrestricted range (typically -3 to +3) |
| Centered difficulty | `Difficulty_c` | float | Grand-mean centered, mean approximately 0 |
| Time variable | `TSVR_hours` | float | Decision D070 requirement |
| Memory domain | `dimension` | string | Values: {"what", "where", "when"} |

---

## Cross-RQ Dependencies

**Dependency Type:** DERIVED Data from Other RQ (Requires RQ 5.2.1 Completion)

**This RQ requires outputs from:**

**RQ 5.2.1 (Domain-Specific Trajectories - ROOT RQ for Domains Type)**
- **File 1:** results/ch5/5.2.1/data/step03_item_parameters.csv
  - **Used in:** Step 0 (load item difficulty 'b' parameter)
  - **Required columns:** item_name, dimension, a, b
  - **Rationale:** RQ 5.1.6 does NOT calibrate IRT models (no 2-pass purification). Instead, uses DERIVED difficulty parameters from RQ 5.2.1 as predictor variable in GLMM. This dependency is essential - without item difficulty values, interaction cannot be tested.

- **File 2:** results/ch5/5.2.1/data/step00_tsvr_mapping.csv
  - **Used in:** Step 0 (load TSVR time variable)
  - **Required columns:** UID, test, TSVR_hours, composite_ID
  - **Rationale:** TSVR_hours is the time variable (Decision D070). RQ 5.2.1 extracts this from master.xlsx. RQ 5.1.6 reuses it rather than re-extracting (DRY principle - Don't Repeat Yourself).

**Execution Order Constraint:**
1. **RQ 5.2.1 must complete through Step 3** (IRT Pass 2 calibration on purified items)
2. **Then RQ 5.1.6 can execute** (uses RQ 5.2.1 item parameters as input)

**Data Source Boundaries (Per Specification 5.1.6):**

**DERIVED Data:**
- Item difficulty parameters ('b' values) from RQ 5.2.1 IRT calibration
- TSVR timing data from RQ 5.2.1 extraction
- Purified item list (which items survived Decision D039 thresholds in RQ 5.2.1)

**RAW Data:**
- Binary item responses from data/cache/dfData.csv (extracted directly in Step 1)
- Response data NOT derived from RQ 5.2.1 (fresh extraction to avoid data provenance issues)

**Scope:**
- This RQ does NOT re-calibrate IRT models (Decision D039 does NOT apply)
- This RQ does NOT purify items (uses RQ 5.2.1 purified item set as-is)
- This RQ ONLY tests difficulty x time interaction using DERIVED difficulty + RAW responses

**Validation (Circuit Breaker):**

Step 0 MUST check:
1. results/ch5/5.2.1/data/step03_item_parameters.csv exists
   - If missing: QUIT with "EXPECTATIONS ERROR: RQ 5.2.1 must complete Step 3 before running RQ 5.1.6"
2. results/ch5/5.2.1/data/step00_tsvr_mapping.csv exists
   - If missing: QUIT with "EXPECTATIONS ERROR: RQ 5.2.1 must complete Step 0 before running RQ 5.1.6"
3. Item count in step03_item_parameters.csv >= 70
   - If < 70: QUIT with "EXPECTATIONS ERROR: Insufficient purified items from RQ 5.2.1 (expected >= 70, found {N})"

**Dependency Rationale:**

RQ 5.1.6 is a **secondary analysis** building on RQ 5.2.1 outputs. RQ 5.2.1 is the **root RQ** for Domains type (5.2.X), performing the foundational IRT calibration and purification. RQ 5.1.6 extends this by asking: "Do item characteristics (difficulty) moderate forgetting, beyond domain differences?" This analysis requires valid difficulty estimates, which only exist after RQ 5.2.1 completes.

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

---

## Summary

**Total Steps:** 8 (Step 0 through Step 7)
**Estimated Runtime:** High (90-120 minutes total, dominated by Step 4 GLMM fitting)
**Cross-RQ Dependencies:** RQ 5.2.1 (must complete Step 3 for item parameters and Step 0 for TSVR mapping)
**Primary Outputs:**
- data/step06_difficulty_interaction.csv (focal hypothesis test: Time:Difficulty_c interaction)
- data/step07_difficulty_trajectories_data.csv (plot source CSV for easy vs hard item trajectories)
- data/step04_glmm_model_summary.txt (full model results)
- data/step05_glmm_diagnostics.txt (assumption validation report)

**Validation Coverage:** 100% (all 8 steps have validation requirements stated explicitly with 4-layer substance criteria)

**Critical Notes:**
- **No IRT calibration:** RQ 5.1.6 uses DERIVED item parameters from RQ 5.2.1, does NOT apply Decision D039 (2-pass purification)
- **No dual-scale plots:** Decision D069 does NOT apply (GLMM uses probability scale natively, no theta scale)
- **TSVR time variable:** Decision D070 DOES apply (TSVR_hours used, not nominal days)
- **Single planned comparison:** Decision D068 alpha=0.05, no Bonferroni correction (exploratory analysis, single focal test)
- **Convergence fallback:** 4-tier strategy documented in Step 4 (adaptive response to crossed random effects complexity)
- **Item-level analysis:** Long format data (~28k-42k observations) required for crossed random effects structure

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-02): Initial plan created by rq_planner agent for RQ 5.1.6 (Item Difficulty Interaction)
