# Analysis Plan: RQ 5.2.8 - Domain x Item Difficulty Interaction

**Research Question:** 5.2.8
**Created:** 2025-12-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines whether the relationship between item difficulty and forgetting rate varies across episodic memory domains (What, Where, When). The analysis uses a cross-classified Generalized Linear Mixed Model (GLMM) with binomial family to model item-level binary responses (correct=1, incorrect=0), testing whether easier items show faster or slower forgetting and whether this pattern differs by domain.

**Analysis Type:** Cross-classified GLMM with binomial family and logit link

**Key Theoretical Question:** Does item difficulty interact with forgetting rate differently for object identity (What, perirhinal-dependent) versus spatiotemporal binding (Where/When, hippocampal-dependent)?

**Pipeline:** DERIVED data dependency (RQ 5.2.1) + RAW response extraction -> GLMM with crossed random effects (UID x Item) -> Interaction extraction with dual p-values -> Plot data preparation

**Steps:** 7 total analysis steps (Step 0: item difficulty loading + Steps 1-6: analysis)

**Estimated Runtime:** Medium-High (~60-90 minutes total)
- Steps 0-3: Low complexity (~5-10 min total - data manipulation)
- Step 4: High complexity (~45-60 min - GLMM fitting with convergence challenges)
- Steps 5-6: Low complexity (~5-10 min - extraction and plotting)

**Key Decisions Applied:**
- **Decision D068:** Dual p-value reporting (uncorrected + Bonferroni for 3 domain post-hoc contrasts)
- **Decision D070:** TSVR_hours as time variable (actual elapsed time, not nominal days)
- **Exploratory Design:** Omnibus 3-way interaction test (alpha=0.05) followed by post-hoc contrasts only if significant (Bonferroni alpha=0.0167)

**Critical Notes:**
- GLMM required (NOT LMM) - binary responses violate normality assumption
- Random slopes convergence risk with N=100 - pre-specified simplification strategy documented
- Coefficients represent log-odds; odds ratios (exp(beta)) reported for interpretation
- Predicted probabilities bounded [0,1] via logit link

---

## Analysis Plan

### Step 0: Load Item Difficulty from RQ 5.2.1

**Dependencies:** None (first step, but requires RQ 5.2.1 completion)

**Complexity:** Low (<5 minutes - file loading and merging)

**Purpose:** Load IRT-derived item difficulty parameters from RQ 5.2.1 and merge with domain labels to create item-level difficulty lookup table.

**Input:**

**File 1:** results/ch5/5.2.1/data/step03_item_parameters.csv
**Source:** RQ 5.2.1 Step 3 (IRT Pass 2 calibration on purified items)
**Format:** CSV with columns:
  - `item_name` (string, format: tag pattern like VR-IFR-A01-N-ANS)
  - `dimension` (string, values: {what, where, when} - lowercase domain names)
  - `a` (float, discrimination parameter, range typically [0.4, 4.0] after purification)
  - `b` (float, difficulty parameter, unrestricted range but typically [-3, 3] after purification)
**Expected Rows:** ~70 items (29 What + 50 Where + 26 When, post-purification per Decision D039)
**Expected Columns:** 4 (item_name, dimension, a, b)

**File 2:** results/ch5/5.2.1/data/step02_purified_items.csv
**Source:** RQ 5.2.1 Step 2 (purification after Pass 1)
**Format:** CSV with columns:
  - `item_name` (string, item tags)
  - `dimension` (string, domain)
  - `retained` (bool, True for purified items)
**Purpose:** Verification that item_parameters.csv contains only purified items
**Expected Rows:** ~70 items (subset of original ~105 items)

**Processing:**

1. **Load item parameters** from RQ 5.2.1 step03_item_parameters.csv
2. **Extract difficulty column** (b parameter) and dimension (domain) column
3. **Map dimension to domain labels:**
   - "what" -> "What" (standardize capitalization)
   - "where" -> "Where"
   - "when" -> "When"
4. **Create item difficulty lookup:** item_name, domain, difficulty
5. **Verify purified items:** Check all items in lookup exist in step02_purified_items.csv with retained=True
6. **Save output:** data/step00_item_difficulty_by_domain.csv

**Output:**

**File:** data/step00_item_difficulty_by_domain.csv
**Format:** CSV with columns:
  - `item_name` (string, unique item identifier from master.xlsx tag pattern)
  - `domain` (string, categorical: {What, Where, When})
  - `difficulty` (float, IRT b parameter, typically [-3, 3] range after purification)
**Expected Rows:** ~70 items (post-purification count from RQ 5.2.1)
**Expected Columns:** 3 (item_name, domain, difficulty)

**Validation Requirement:**

Validation tools MUST be used after data loading and transformation. Specific validation tools will be determined by rq_tools based on file format and content requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_item_difficulty_by_domain.csv: 70 rows x 3 columns (item_name: object, domain: object, difficulty: float64)

*Value Ranges:*
- difficulty in [-6, 6] (IRT b parameter unrestricted, but extreme values rare after purification)
- domain in {What, Where, When} (exact string match, case-sensitive)

*Data Quality:*
- All 70 items present (no missing data from RQ 5.2.1 item_parameters.csv)
- No NaN values in any column
- No duplicate item_name values (each item appears exactly once)
- Domain distribution approximately: What ~29, Where ~50, When ~26 (per concept.md)

*Log Validation:*
- Required pattern: "Loaded 70 items from RQ 5.2.1"
- Required pattern: "Domain distribution: What=29, Where=50, When=26" (approximate counts)
- Required pattern: "All items verified in purified_items.csv"
- Forbidden patterns: "ERROR", "NaN detected", "Missing items"
- Acceptable warnings: None expected (straightforward file loading)

**Expected Behavior on Validation Failure:**
- If item count != 70: Raise error "Expected ~70 items from RQ 5.2.1, found {N}"
- If NaN values detected: Raise error "Missing difficulty values for items: {list}"
- If domain values invalid: Raise error "Invalid domain values: {list}, expected What/Where/When"
- Log failure to logs/step00_load_item_difficulty.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose (likely RQ 5.2.1 dependency issue)

**Cross-RQ Dependency Check:**
- Verify RQ 5.2.1 status.yaml shows rq_results: success (or at minimum rq_inspect: success for Step 3)
- If RQ 5.2.1 incomplete: QUIT with EXPECTATIONS ERROR "RQ 5.2.1 must complete Steps 1-3 before RQ 5.2.8 can run"

---

### Step 1: Extract Raw Binary Responses in Long Format

**Dependencies:** Step 0 (requires item difficulty lookup to filter items)

**Complexity:** Low (<5 minutes - data extraction from dfData.csv)

**Purpose:** Extract raw binary response data (correct=1, incorrect=0) for all purified items from RQ 5.2.1, reshape from wide format (one row per UID x test) to long format (one row per UID x test x item response).

**Input:**

**File 1:** data/cache/dfData.csv
**Source:** Preprocessed participant response data (created by data pipeline from master.xlsx)
**Format:** CSV with columns:
  - `UID` (string, participant identifier, format: A### like A010, A053)
  - `TEST` (string, test session, values: {T1, T2, T3, T4})
  - Item response columns with tag patterns (0/1 binary, NaN for missing)
**Expected Rows:** 400 (100 participants x 4 tests)
**Tag Patterns for Extraction:**
  - What domain: `-N-` tags (object identity items, ~29 items)
  - Where domain: `-L-`, `-U-`, `-D-` tags (spatial location items, ~50 items)
  - When domain: `-O-` tags (temporal order items, ~26 items)
**Extraction Filter:** Only items present in step00_item_difficulty_by_domain.csv (purified items from RQ 5.2.1)

**File 2:** data/step00_item_difficulty_by_domain.csv
**Source:** Step 0 output
**Purpose:** Filter to only purified items (exclude items removed during RQ 5.2.1 purification)

**Processing:**

1. **Load dfData.csv** with UID, TEST, and all VR item columns
2. **Filter to purified items only:** Use item_name list from step00_item_difficulty_by_domain.csv to select columns
3. **Reshape wide to long:**
   - Input: 400 rows x (2 ID cols + 70 item cols)
   - Output: 28,000 rows (400 composite_IDs x 70 items per composite)
   - Columns: UID, TEST, item_name, response (0/1/NaN)
4. **Create composite_ID:** Concatenate UID + "_" + TEST (format: A010_T1, A053_T3)
5. **Handle missing responses:** Retain NaN values (represent items not administered or skipped)
6. **Save output:** data/step01_response_level_data_raw.csv

**Output:**

**File:** data/step01_response_level_data_raw.csv
**Format:** CSV, long format (one row per UID x test x item response)
**Columns:**
  - `composite_ID` (string, format: {UID}_{TEST}, e.g., A010_T1)
  - `UID` (string, participant identifier)
  - `TEST` (string, test session: T1, T2, T3, T4)
  - `item_name` (string, item tag from master.xlsx)
  - `response` (float, values: {0.0, 1.0, NaN}, where 0=incorrect, 1=correct, NaN=missing)
**Expected Rows:** 28,000 (100 participants x 4 tests x 70 purified items)
**Expected Columns:** 5 (composite_ID, UID, TEST, item_name, response)

**Validation Requirement:**

Validation tools MUST be used after data extraction and reshaping. Specific validation tools will be determined by rq_tools based on extraction logic and long-format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_response_level_data_raw.csv: 28,000 rows x 5 columns (composite_ID: object, UID: object, TEST: object, item_name: object, response: float64)

*Value Ranges:*
- response in {0.0, 1.0, NaN} (binary outcome, NaN acceptable for missing data)
- TEST in {T1, T2, T3, T4} (all four test sessions represented)
- composite_ID format: {UID}_{TEST} (e.g., A010_T1)

*Data Quality:*
- Expected rows: 28,000 (400 composite_IDs x 70 items)
- All 100 participants present (UID count = 100 unique values)
- All 4 test sessions present per participant (TEST distribution balanced)
- Missing data rate <30% (NaN responses acceptable but not excessive)
- No duplicate rows (composite_ID x item_name combinations unique)

*Log Validation:*
- Required pattern: "Extracted 28,000 responses from dfData.csv"
- Required pattern: "70 purified items included"
- Required pattern: "100 participants x 4 tests = 400 composite_IDs"
- Required pattern: "Missing data rate: {X}% (acceptable <30%)"
- Forbidden patterns: "ERROR", "Extraction failed", "Item mismatch"
- Acceptable warnings: "Missing responses detected: {N} NaN values ({X}%)" if <30%

**Expected Behavior on Validation Failure:**
- If row count != 28,000: Raise error "Expected 28,000 rows (400 x 70), found {N}"
- If missing data rate >30%: Raise error "Excessive missing data: {X}%, threshold 30%"
- If item count != 70: Raise error "Expected 70 purified items, found {N}"
- Log failure to logs/step01_extract_responses.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose (likely dfData.csv extraction issue or tag mismatch)

---

### Step 2: Merge Responses with Item Difficulty and TSVR Time

**Dependencies:** Step 0 (item difficulty), Step 1 (raw responses)

**Complexity:** Low (<5 minutes - data merging operations)

**Purpose:** Merge raw binary responses with item difficulty parameters from Step 0 and TSVR time mapping from RQ 5.2.1 to create complete dataset for GLMM analysis.

**Input:**

**File 1:** data/step01_response_level_data_raw.csv
**Source:** Step 1 output
**Format:** CSV, long format with 28,000 rows (UID x test x item responses)
**Columns:** composite_ID, UID, TEST, item_name, response

**File 2:** data/step00_item_difficulty_by_domain.csv
**Source:** Step 0 output
**Format:** CSV with item-level difficulty and domain
**Columns:** item_name, domain, difficulty

**File 3:** results/ch5/5.2.1/data/step00_tsvr_mapping.csv
**Source:** RQ 5.2.1 Step 0 (TSVR extraction)
**Format:** CSV with composite_ID to TSVR_hours mapping
**Columns:**
  - `composite_ID` (string, format: UID_TEST)
  - `TSVR_hours` (float, actual hours since encoding, range typically [0, 168] for 0-7 days)
**Expected Rows:** 400 (100 participants x 4 tests)

**Processing:**

1. **Merge responses with item difficulty:**
   - Left join step01_response_level_data_raw with step00_item_difficulty_by_domain on item_name
   - Adds columns: domain, difficulty
   - Expected output: 28,000 rows (no row loss - all items have difficulty)

2. **Merge with TSVR time mapping:**
   - Left join merged data with RQ 5.2.1 tsvr_mapping.csv on composite_ID
   - Adds column: TSVR_hours
   - Expected output: 28,000 rows (no row loss - all composite_IDs have TSVR)

3. **Verify merge completeness:**
   - Check for NaN in domain, difficulty, TSVR_hours (should be 0)
   - All 28,000 rows should have complete data except response column (NaN acceptable)

4. **Create test number column:**
   - Extract test number from TEST (T1->0, T2->1, T3->3, T4->6)
   - Used for plotting (nominal days) while TSVR_hours used for modeling

5. **Save output:** data/step02_response_with_difficulty_tsvr.csv

**Output:**

**File:** data/step02_response_with_difficulty_tsvr.csv
**Format:** CSV, long format with complete predictor variables
**Columns:**
  - `composite_ID` (string, format: UID_TEST)
  - `UID` (string, participant identifier)
  - `TEST` (string, test session: T1, T2, T3, T4)
  - `test_num` (int, nominal days: 0, 1, 3, 6)
  - `item_name` (string, item tag)
  - `response` (float, 0/1/NaN)
  - `domain` (string, What/Where/When)
  - `difficulty` (float, IRT b parameter)
  - `TSVR_hours` (float, actual time since encoding)
**Expected Rows:** 28,000 (100 participants x 4 tests x 70 items)
**Expected Columns:** 9

**Validation Requirement:**

Validation tools MUST be used after merging operations. Specific validation tools will be determined by rq_tools based on merge requirements and data completeness checks.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_response_with_difficulty_tsvr.csv: 28,000 rows x 9 columns (all columns with correct data types)

*Value Ranges:*
- TSVR_hours in [0, 240] hours (0=encoding, 240=10 days - allows for delayed test completion)
- test_num in {0, 1, 3, 6} (nominal days corresponding to T1-T4)
- difficulty in [-6, 6] (IRT b parameter range)
- response in {0.0, 1.0, NaN}
- domain in {What, Where, When}

*Data Quality:*
- Expected rows: 28,000 (no row loss during merges)
- No NaN in: composite_ID, UID, TEST, test_num, item_name, domain, difficulty, TSVR_hours
- NaN acceptable only in: response column (missing responses)
- All 400 composite_IDs from Step 1 present (100% merge success with tsvr_mapping.csv)
- All 70 items from Step 0 present (100% merge success with item_difficulty.csv)

*Log Validation:*
- Required pattern: "Merged 28,000 responses with item difficulty: 0 NaN in domain/difficulty"
- Required pattern: "Merged with TSVR mapping: 0 NaN in TSVR_hours"
- Required pattern: "All 400 composite_IDs matched successfully"
- Required pattern: "All 70 items matched successfully"
- Forbidden patterns: "ERROR", "Merge failed", "NaN detected in predictors"
- Acceptable warnings: "Missing responses: {N} NaN in response column" if <30%

**Expected Behavior on Validation Failure:**
- If row count != 28,000: Raise error "Row loss during merge: expected 28,000, found {N}"
- If NaN in predictors: Raise error "Missing predictor values: {column} has {N} NaN"
- If composite_ID mismatch: Raise error "TSVR mapping incomplete: {N} composite_IDs unmatched"
- If item_name mismatch: Raise error "Item difficulty mapping incomplete: {N} items unmatched"
- Log failure to logs/step02_merge_data.log
- Quit script immediately (do NOT proceed to Step 3)
- g_debug invoked to diagnose (likely RQ 5.2.1 dependency issue or tag mismatch)

---

### Step 3: Grand-Mean Center Item Difficulty

**Dependencies:** Step 2 (merged response data with difficulty)

**Complexity:** Low (<5 minutes - simple transformation)

**Purpose:** Grand-mean center item difficulty (Difficulty_c) to enable interpretation of main effects and interactions in GLMM. Centering ensures that main effects represent effects at average difficulty rather than at difficulty=0 (which may not be meaningful).

**Input:**

**File:** data/step02_response_with_difficulty_tsvr.csv
**Source:** Step 2 output
**Format:** CSV with 28,000 rows (response-level data)
**Columns:** composite_ID, UID, TEST, test_num, item_name, response, domain, difficulty, TSVR_hours

**Processing:**

1. **Compute grand mean of difficulty:**
   - Grand_mean = mean(difficulty) across all 70 unique items
   - Expected value: ~0 (IRT b parameters typically centered around 0 after calibration)
   - Compute once per item, not per response (difficulty is item property)

2. **Create centered difficulty:**
   - Difficulty_c = difficulty - Grand_mean
   - Add as new column to dataframe

3. **Verify centering:**
   - Check mean(Difficulty_c) approximately 0 (tolerance: |mean| < 0.01)
   - Check SD(Difficulty_c) = SD(difficulty) (centering preserves variance)

4. **Create time transformation:**
   - Time = TSVR_hours (primary time variable per Decision D070)
   - Optionally: log_Time = log(TSVR_hours + 1) if concept requires (check 1_concept.md)

5. **Save output:** data/step03_glmm_input.csv

**Output:**

**File:** data/step03_glmm_input.csv
**Format:** CSV, long format with centered predictors ready for GLMM
**Columns:**
  - `composite_ID` (string)
  - `UID` (string, random effect grouping variable)
  - `TEST` (string)
  - `test_num` (int, for plotting)
  - `item_name` (string, random effect grouping variable)
  - `response` (float, 0/1/NaN, outcome variable)
  - `domain` (string, What/Where/When, categorical predictor)
  - `difficulty` (float, original IRT b parameter)
  - `Difficulty_c` (float, grand-mean centered, predictor in GLMM)
  - `TSVR_hours` (float, Time variable per Decision D070)
  - `Time` (float, same as TSVR_hours for model clarity)
**Expected Rows:** 28,000
**Expected Columns:** 11

**Validation Requirement:**

Validation tools MUST be used after centering and transformation. Specific validation tools will be determined by rq_tools based on standardization and transformation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_glmm_input.csv: 28,000 rows x 11 columns (all columns with correct data types)

*Value Ranges:*
- Difficulty_c approximately centered: mean(Difficulty_c) in [-0.1, 0.1] (tolerance for rounding)
- SD(Difficulty_c) = SD(difficulty) within 1% (centering preserves variance)
- Time = TSVR_hours (identical values)
- response in {0.0, 1.0, NaN}

*Data Quality:*
- Expected rows: 28,000 (no row loss during transformation)
- No NaN in: Difficulty_c, Time (centering and copy operations should not introduce missing)
- Difficulty_c distribution: approximately normal if difficulty was normal (check histogram in log)
- All 70 unique items contribute to grand mean calculation

*Log Validation:*
- Required pattern: "Grand mean difficulty: {X} (expected ~0)"
- Required pattern: "Difficulty_c centered: mean={X}, SD={Y}"
- Required pattern: "Centering verification: |mean(Difficulty_c)| < 0.1"
- Required pattern: "Variance preserved: SD(difficulty)={X}, SD(Difficulty_c)={Y}"
- Forbidden patterns: "ERROR", "Centering failed", "NaN introduced"
- Acceptable warnings: None expected (simple arithmetic operation)

**Expected Behavior on Validation Failure:**
- If |mean(Difficulty_c)| > 0.1: Raise error "Centering failed: mean(Difficulty_c)={X}, expected ~0"
- If variance changed: Raise error "Variance not preserved: SD changed from {X} to {Y}"
- If NaN introduced: Raise error "Centering introduced NaN values in Difficulty_c"
- Log failure to logs/step03_center_difficulty.log
- Quit script immediately (do NOT proceed to Step 4)
- g_debug invoked to diagnose (likely computational error)

---

### Step 4: Fit Cross-Classified GLMM with Model Selection Strategy

**Dependencies:** Step 3 (GLMM input with centered difficulty)

**Complexity:** High (45-60 minutes - GLMM fitting with binomial family, potential convergence challenges)

**Purpose:** Fit cross-classified Generalized Linear Mixed Model with binomial family and logit link to test whether item difficulty interacts with forgetting rate (Time) and whether this interaction differs across domains (3-way Time x Difficulty_c x domain). Uses pymer4 for crossed random effects structure (UID x Item). Implements pre-specified model selection strategy for random effects due to convergence risk with N=100 and binary data.

**Input:**

**File:** data/step03_glmm_input.csv
**Source:** Step 3 output
**Format:** CSV with 28,000 rows (response-level data)
**Columns:** composite_ID, UID, TEST, test_num, item_name, response, domain, Difficulty_c, Time, and others
**Key Variables:**
  - Outcome: response (0/1, NaN excluded during fitting)
  - Fixed effects: Time, Difficulty_c, domain, all 2-way interactions, 3-way Time:Difficulty_c:domain
  - Random effects: (Time | UID) + (1 | Item) - crossed random effects structure
  - Family: binomial(link='logit')

**Processing:**

**4a. Remove Missing Responses:**
1. Filter out rows where response is NaN (GLMM cannot fit missing outcomes)
2. Expected remaining rows: ~19,600-22,400 (70-80% completion rate per concept assumption)
3. Verify minimum data per participant: at least 40 responses per UID (out of 280 possible = 4 tests x 70 items)
4. Verify minimum data per item: at least 280 responses per item (out of 400 possible = 100 participants x 4 tests)

**4b. Model Selection Strategy for Random Effects (Pre-Specified):**

With N=100 participants and binary responses, random slopes may fail to converge. Per concept.md Step 4b:

**Attempt 1:** Full model with correlated random effects
- Formula: `Response ~ Time * Difficulty_c * domain + (Time | UID) + (1 | Item)`
- Family: binomial(link='logit')
- Implementation: pymer4.models.Lmer(formula, data, family='binomial')
- Optimizer: Default (lme4 default)

**If convergence fails (model.converged = False OR warnings about singular fit):**

**Attempt 2:** Try alternative optimizers
- Optimizers to try: 'bobyqa', 'Nelder_Mead', 'nlminb'
- Same formula as Attempt 1
- If any optimizer converges: accept that model

**If all optimizers fail:**

**Attempt 3:** Simplify to uncorrelated random effects
- Formula: `Response ~ Time * Difficulty_c * domain + (1 + Time || UID) + (1 | Item)`
- Note: `||` syntax means uncorrelated random intercept and slope
- Rationale: Estimating correlation with N=100 may be unstable

**If still fails:**

**Attempt 4:** Use random intercepts only
- Formula: `Response ~ Time * Difficulty_c * domain + (1 | UID) + (1 | Item)`
- Rationale: Random slopes may be too complex for available data

**Final Model Documentation:**
- Log which attempt succeeded
- Document final random effects structure in model summary
- Note: Fixed effects (interaction terms) interpretable regardless of random effects structure
- Acknowledge any simplification in results interpretation

**4c. Fit GLMM:**
1. Use pymer4 Lmer() with family='binomial'
2. Set REML=False (required for model comparison, though not comparing here)
3. Extract fitted model object
4. Verify convergence: model.converged = True (or document which simplification used)
5. Extract fixed effects table (coefficients, SE, z-statistics, p-values)
6. Extract random effects variance components
7. Save fitted model and summary

**Output:**

**File 1:** data/step04_glmm_model.pkl
**Format:** Pickle file containing fitted pymer4 Lmer model object
**Purpose:** Save fitted model for downstream extraction (Step 5)

**File 2:** data/step04_glmm_model_summary.txt
**Format:** Text file with complete model output
**Contents:**
  - Model formula (including final random effects structure)
  - Convergence status (True/False)
  - Optimizer used
  - Random effects structure attempted and final (log selection path)
  - Fixed effects table (all main effects, 2-way interactions, 3-way interaction)
  - Random effects variance components
  - Model fit statistics (AIC, BIC, log-likelihood)
  - Number of observations used (after removing NaN responses)

**File 3:** data/step04_fixed_effects.csv
**Format:** CSV with fixed effects estimates
**Columns:**
  - `term` (string, predictor name)
  - `estimate` (float, log-odds coefficient)
  - `SE` (float, standard error)
  - `z_value` (float, z-statistic)
  - `p_value` (float, uncorrected p-value)
  - `OR` (float, odds ratio = exp(estimate))
  - `OR_CI_lower` (float, exp(estimate - 1.96*SE))
  - `OR_CI_upper` (float, exp(estimate + 1.96*SE))
**Expected Rows:** 14 terms (1 intercept + 3 main effects + 6 two-way + 4 three-way interactions for 3-level domain factor)
- Intercept
- Time
- Difficulty_c
- domain[Where] (reference: What)
- domain[When] (reference: What)
- Time:Difficulty_c
- Time:domain[Where]
- Time:domain[When]
- Difficulty_c:domain[Where]
- Difficulty_c:domain[When]
- Time:Difficulty_c:domain[Where]
- Time:Difficulty_c:domain[When]
- (Plus 2 more if domain has 3 levels and model expands interactions)

**Note:** Exact term count depends on pymer4 factor encoding (treatment coding with What as reference)

**Validation Requirement:**

Validation tools MUST be used after GLMM fitting. Specific validation tools will be determined by rq_tools based on GLMM convergence, assumption checks (binomial family), and fixed effects extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_glmm_model.pkl: Pickle file >10 KB (fitted model object)
- data/step04_glmm_model_summary.txt: Text file >5 KB (complete summary)
- data/step04_fixed_effects.csv: ~14 rows x 8 columns (fixed effects table)

*Value Ranges:*
- estimate (log-odds): unrestricted, typically [-5, 5] for reasonable effects
- SE: positive values, typically [0.01, 2.0] depending on sample size
- z_value: unrestricted (estimate / SE)
- p_value: in [0, 1]
- OR (odds ratio): positive values (exp(estimate)), typically [0.01, 100] for reasonable effects
- OR_CI_lower, OR_CI_upper: positive values, CI_lower < OR < CI_upper

*Data Quality:*
- Model converged: True OR documented simplification strategy applied
- All fixed effect terms present (no singularity excluding terms)
- No NaN in estimates, SE, z_value, p_value, OR, CI bounds
- Random effects variance components positive (if extracted)
- Observations used: ~19,600-22,400 (70-80% of 28,000 after removing NaN responses)
- All 100 participants present in analysis (no UID excluded due to insufficient data)
- All 70 items present in analysis (no item excluded)

*Log Validation:*
- Required pattern: "Model converged: {True/False}"
- Required pattern: "Random effects structure: {formula}" (documents which attempt succeeded)
- Required pattern: "Optimizer used: {name}"
- Required pattern: "Observations: {N} (after removing NaN responses)"
- Required pattern: "Fixed effects: 14 terms estimated"
- Required pattern: "All variance components positive" (if random effects retained)
- Forbidden patterns: "ERROR", "GLMM fitting failed", "Singular fit unresolved"
- Acceptable warnings: "Convergence not achieved with full model, simplified to {structure}" (if simplification applied)

**Expected Behavior on Validation Failure:**
- If model.converged = False AND all simplifications exhausted: Raise error "GLMM convergence failed after all 4 attempts"
- If singular fit warnings persist: Document in log, proceed with caution (fixed effects still interpretable)
- If fixed effects table incomplete: Raise error "Missing interaction terms: expected 14, found {N}"
- If NaN in fixed effects: Raise error "Estimation failed: NaN coefficients for terms: {list}"
- Log failure to logs/step04_fit_glmm.log
- Quit script immediately (do NOT proceed to Step 5)
- g_debug invoked to diagnose (likely convergence issue, data structure problem, or insufficient variation)

**GLMM Assumption Checks (Documented in Log):**

Per concept.md validation procedures:
1. **Overdispersion:** Residual deviance / df approximately 1.0 (acceptable range: 0.8-1.2)
   - If overdispersion detected: Log warning, note in summary (quasi-binomial as sensitivity analysis if severe)
2. **Link Function:** Predicted probabilities span reasonable range (not all near 0 or 1)
   - Compute fitted values, check range [0.1, 0.9] covers majority (>50% of predictions)
3. **Random Effects:** Q-Q plot of random intercepts and slopes (if retained) saved to logs/
4. **Influential Observations:** Identify items or participants with extreme residuals (log outliers)

**Remedial Actions (if needed):**
- Overdispersion >1.2: Note in summary, consider quasi-binomial in discussion (not re-fit here)
- Extreme observations: Sensitivity analysis excluding outliers (optional, not required for Step 4)

---

### Step 5: Extract Interaction Terms with Dual P-Values

**Dependencies:** Step 4 (fitted GLMM model)

**Complexity:** Low (<5 minutes - extraction from fitted model)

**Purpose:** Extract Time x Difficulty_c x domain three-way interaction terms from fitted GLMM and apply Decision D068 dual p-value reporting (uncorrected + Bonferroni correction). Test exploratory omnibus interaction at alpha=0.05; if significant, conduct domain-specific post-hoc contrasts with Bonferroni alpha=0.0167 (correcting for 3 domain comparisons).

**Input:**

**File 1:** data/step04_glmm_model.pkl
**Source:** Step 4 output (fitted pymer4 GLMM model)

**File 2:** data/step04_fixed_effects.csv
**Source:** Step 4 output (all fixed effects)

**Processing:**

**5a. Omnibus Three-Way Interaction Test:**
1. **Extract 3-way interaction terms** from fixed effects:
   - `Time:Difficulty_c:domain[Where]`
   - `Time:Difficulty_c:domain[When]`
   - (Reference level: What - interaction included in intercept)

2. **Test omnibus interaction** at alpha=0.05 (exploratory design per concept.md):
   - Method: Likelihood ratio test comparing full model vs model without 3-way terms
   - OR: Use Wald test on 3-way terms (chi-square with 2 df for 2 interaction coefficients)
   - Report omnibus p-value

3. **Decision rule:**
   - If omnibus p < 0.05: Proceed to domain-specific post-hoc contrasts (Step 5b)
   - If omnibus p >= 0.05: Report non-significant, skip post-hoc, report effect sizes regardless

**5b. Domain-Specific Post-Hoc Contrasts (only if omnibus significant):**

**Per concept.md:** If omnibus interaction significant, conduct domain-specific tests of Time x Difficulty_c interaction within each domain.

**Contrasts to test:**
1. **Where vs What:** Test if Time:Difficulty_c interaction differs between Where and What domains
2. **When vs What:** Test if Time:Difficulty_c interaction differs between When and What domains
3. **Where vs When:** Test if Time:Difficulty_c interaction differs between Where and When domains

**Method:**
- Extract domain-stratified slopes (marginal effects)
- Compute pairwise differences with delta method SEs
- Report Bonferroni correction: alpha = 0.05 / 3 = 0.0167

**Decision D068 Dual P-Values:**
- Report BOTH p_uncorrected AND p_bonferroni for all 3 contrasts
- Rationale: Transparent reporting for exploratory thesis, avoid overconfidence from uncorrected p-values

**5c. Interpretation Guidelines:**

For each significant interaction term, interpret using odds ratios:
- **Positive coefficient (OR > 1):** Easier items show FASTER forgetting (encoding strength effect)
  - As difficulty decreases (easier items), the effect of Time on log-odds of correct response becomes more negative
  - Interpretation: Weakly encoded easy items decay faster
- **Negative coefficient (OR < 1):** Easier items show SLOWER forgetting (ceiling effect)
  - As difficulty decreases, the effect of Time becomes less negative
  - Interpretation: Easy items maintain high performance (ceiling), appear to forget slower

**Output:**

**File 1:** data/step05_omnibus_interaction_test.csv
**Format:** CSV with omnibus test results
**Columns:**
  - `test_type` (string, "omnibus_3way")
  - `chi_square` (float, test statistic)
  - `df` (int, degrees of freedom, expected 2)
  - `p_value` (float, uncorrected p-value)
  - `significant` (bool, True if p < 0.05)
**Expected Rows:** 1

**File 2:** data/step05_three_way_interaction_terms.csv
**Format:** CSV with 3-way interaction coefficients
**Columns:**
  - `term` (string, interaction term name)
  - `domain_contrast` (string, which domain vs reference What)
  - `estimate` (float, log-odds coefficient)
  - `SE` (float, standard error)
  - `z_value` (float, z-statistic)
  - `p_uncorrected` (float, uncorrected p-value)
  - `OR` (float, odds ratio)
  - `OR_CI_lower` (float, 95% CI lower bound)
  - `OR_CI_upper` (float, 95% CI upper bound)
  - `interpretation` (string, "encoding strength" if OR>1, "ceiling effect" if OR<1, "null" if not significant)
**Expected Rows:** 2 (Where vs What, When vs What)

**File 3:** data/step05_post_hoc_contrasts.csv (only created if omnibus significant)
**Format:** CSV with domain-specific post-hoc tests
**Columns:**
  - `contrast` (string, e.g., "Where - What", "When - What", "Where - When")
  - `estimate` (float, difference in Time:Difficulty_c interaction log-odds)
  - `SE` (float, standard error)
  - `z_value` (float, z-statistic)
  - `p_uncorrected` (float, uncorrected p-value)
  - `p_bonferroni` (float, Bonferroni-corrected p-value = p_uncorrected * 3, capped at 1.0)
  - `significant_uncorrected` (bool, p_uncorrected < 0.05)
  - `significant_bonferroni` (bool, p_bonferroni < 0.0167)
**Expected Rows:** 3 (if omnibus significant, else file not created)

**Validation Requirement:**

Validation tools MUST be used after interaction extraction and contrast computation. Specific validation tools will be determined by rq_tools based on contrast requirements and Decision D068 dual p-value architecture.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_omnibus_interaction_test.csv: 1 row x 5 columns
- data/step05_three_way_interaction_terms.csv: 2 rows x 9 columns
- data/step05_post_hoc_contrasts.csv: 3 rows x 7 columns (only if omnibus p < 0.05, else file absent)

*Value Ranges:*
- chi_square: positive value, typically [0, 20] for non-extreme effects
- p_value, p_uncorrected, p_bonferroni: in [0, 1]
- p_bonferroni = min(p_uncorrected * 3, 1.0) per Bonferroni correction
- OR: positive values
- OR_CI_lower < OR < OR_CI_upper

*Data Quality:*
- Omnibus test df = 2 (two 3-way interaction terms)
- If omnibus significant (p < 0.05): post_hoc_contrasts.csv MUST exist
- If omnibus non-significant (p >= 0.05): post_hoc_contrasts.csv MUST NOT exist
- Decision D068 compliance: BOTH p_uncorrected AND p_bonferroni present in post-hoc file
- p_bonferroni >= p_uncorrected (correction never decreases p-value)

*Log Validation:*
- Required pattern: "Omnibus 3-way interaction test: chi^2({df})={X}, p={Y}"
- Required pattern: "Omnibus interaction significant: {True/False}"
- If omnibus significant: Required pattern: "Conducting 3 post-hoc contrasts with Bonferroni alpha=0.0167"
- If omnibus not significant: Required pattern: "Omnibus not significant, skipping post-hoc contrasts"
- Required pattern: "Decision D068: Dual p-values reported (uncorrected + Bonferroni)"
- Forbidden patterns: "ERROR", "Extraction failed", "Missing p_bonferroni column"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- If omnibus df != 2: Raise error "Omnibus test df mismatch: expected 2, found {N}"
- If omnibus significant but post_hoc file missing: Raise error "Omnibus p < 0.05 but post-hoc contrasts not computed"
- If p_bonferroni missing in post-hoc: Raise error "Decision D068 violation: p_bonferroni column missing"
- If p_bonferroni < p_uncorrected: Raise error "Bonferroni correction error: corrected p < uncorrected p"
- Log failure to logs/step05_extract_interactions.log
- Quit script immediately (do NOT proceed to Step 6)
- g_debug invoked to diagnose (likely extraction logic error or contrast computation failure)

---

### Step 6: Prepare Plot Data for Difficulty Trajectories by Domain

**Dependencies:** Step 4 (fitted GLMM model), Step 3 (GLMM input data)

**Complexity:** Low (<10 minutes - data aggregation for plotting)

**Purpose:** Create plot source CSV showing predicted trajectories for easy items (Difficulty = -1SD) versus hard items (Difficulty = +1SD) stratified by domain. Generates 6 trajectory lines: What-Easy, What-Hard, Where-Easy, Where-Hard, When-Easy, When-Hard. Uses model predictions on probability scale (logit-transformed) for interpretability.

**Input:**

**File 1:** data/step04_glmm_model.pkl
**Source:** Step 4 output (fitted GLMM for predictions)

**File 2:** data/step03_glmm_input.csv
**Source:** Step 3 output (for observed marginal means)

**Processing:**

**6a. Define Difficulty Levels:**
1. Compute SD of Difficulty_c across all 70 items (item-level, not response-level)
2. Define difficulty levels:
   - Easy: Difficulty_c = -1 * SD(Difficulty_c)
   - Hard: Difficulty_c = +1 * SD(Difficulty_c)

**6b. Create Prediction Grid:**
1. Expand grid of:
   - domain: {What, Where, When}
   - difficulty_level: {Easy, Hard}
   - Time: {0, 24, 72, 144} hours (corresponding to T1-T4 nominal schedule)
2. Total rows: 3 domains x 2 difficulty levels x 4 timepoints = 24 rows
3. Add Difficulty_c values: Easy=-1SD, Hard=+1SD
4. Set UID to reference participant (or population average if using marginal predictions)

**6c. Generate Model Predictions:**
1. Use fitted GLMM to predict log-odds for each row in prediction grid
2. Transform log-odds to probability: p = exp(log_odds) / (1 + exp(log_odds))
3. Compute 95% CIs for probabilities using delta method or parametric bootstrap
4. Add columns: predicted_probability, CI_lower, CI_upper

**6d. Compute Observed Marginal Means (Optional):**
1. For each domain x test_num combination:
   - Filter to items with difficulty in [-1SD-0.25, -1SD+0.25] for Easy group
   - Filter to items with difficulty in [+1SD-0.25, +1SD+0.25] for Hard group
2. Compute marginal mean response (proportion correct) per group
3. Compute 95% CIs using normal approximation or bootstrapping
4. Merge with predicted data for comparison plot

**6e. Create Plot-Ready CSV:**
1. Combine predicted probabilities with observed means
2. Add labels: difficulty_label ("Easy (-1SD)", "Hard (+1SD)")
3. Add domain labels
4. Sort by domain, difficulty_level, Time

**Output:**

**File:** data/step06_difficulty_trajectories_by_domain.csv
**Format:** CSV, plot source data for 6-line trajectory plot
**Columns:**
  - `domain` (string, What/Where/When)
  - `difficulty_level` (string, Easy/Hard)
  - `difficulty_label` (string, descriptive label for legend)
  - `Difficulty_c` (float, -1SD or +1SD)
  - `Time` (float, TSVR_hours: 0, 24, 72, 144)
  - `test_num` (int, nominal days: 0, 1, 3, 6)
  - `predicted_probability` (float, model prediction on [0,1] scale)
  - `CI_lower` (float, 95% CI lower bound)
  - `CI_upper` (float, 95% CI upper bound)
  - `observed_probability` (float, marginal mean from data, optional)
  - `observed_CI_lower` (float, optional)
  - `observed_CI_upper` (float, optional)
**Expected Rows:** 24 (3 domains x 2 difficulty levels x 4 timepoints)
**Expected Columns:** 12 (with optional observed columns) or 9 (predicted only)

**Note:** This CSV is created during ANALYSIS (by g_code in Step 14 CODE EXECUTION LOOP), NOT during plotting. The rq_plots agent will later read this CSV and generate PNG output to plots/ folder per Option B architecture.

**Validation Requirement:**

Validation tools MUST be used after plot data preparation. Specific validation tools will be determined by rq_tools based on plot data format requirements and Option B architecture specifications.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_difficulty_trajectories_by_domain.csv: 24 rows x 9-12 columns (depending on observed data inclusion)

*Value Ranges:*
- predicted_probability in [0, 1] (bounded by logit transformation)
- CI_lower in [0, 1], CI_upper in [0, 1]
- CI_lower < predicted_probability < CI_upper for all rows
- observed_probability in [0, 1] (if included)
- Time in {0, 24, 72, 144} hours
- test_num in {0, 1, 3, 6} days
- Difficulty_c: Easy approximately -1SD, Hard approximately +1SD (check against computed SD)

*Data Quality:*
- Expected rows: exactly 24 (no more, no less)
- Complete factorial design: all combinations of 3 domains x 2 difficulty x 4 timepoints present
- No NaN values in predicted_probability, CI_lower, CI_upper
- No duplicate rows (domain x difficulty_level x Time combinations unique)
- CI_upper > CI_lower for all rows (confidence intervals valid)

*Log Validation:*
- Required pattern: "Plot data prepared: 24 rows (3 domains x 2 difficulty levels x 4 timepoints)"
- Required pattern: "Difficulty levels: Easy={X} SD, Hard={Y} SD"
- Required pattern: "Predicted probabilities bounded [0,1]: min={X}, max={Y}"
- Required pattern: "All confidence intervals valid (CI_upper > CI_lower)"
- Forbidden patterns: "ERROR", "NaN in predictions", "Missing domain/difficulty combinations"
- Acceptable warnings: "Observed means not computed (predicted only)" if observed columns absent

**Expected Behavior on Validation Failure:**
- If row count != 24: Raise error "Expected 24 rows (factorial design), found {N}"
- If predicted_probability outside [0,1]: Raise error "Invalid probabilities: {N} values outside [0,1]"
- If CI bounds invalid: Raise error "Invalid CIs: {N} rows with CI_upper < CI_lower"
- If missing combinations: Raise error "Incomplete factorial design: missing {list of combinations}"
- Log failure to logs/step06_prepare_plot_data.log
- Quit script immediately (do NOT proceed to plotting - but rq_plots is separate agent)
- g_debug invoked to diagnose (likely prediction grid error or model prediction failure)

**Plotting Notes (for rq_plots agent, NOT executed in this RQ's analysis steps):**
- rq_plots will read data/step06_difficulty_trajectories_by_domain.csv
- Generate 6-line trajectory plot: 3 domains x 2 difficulty levels
- Use probability scale (NOT theta scale - this is GLMM, not IRT theta)
- X-axis: Time (TSVR_hours) or test_num (nominal days)
- Y-axis: Predicted probability of correct response [0,1]
- Group by: domain (color) + difficulty_level (line style)
- Include confidence bands (CI_lower, CI_upper as shaded regions)
- Optionally overlay observed means if included in CSV
- Save PNG output to plots/step06_difficulty_trajectories_by_domain.png

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs - intermediate and final)

**Step 0 Outputs:**
- data/step00_item_difficulty_by_domain.csv (70 rows, 3 cols: item_name, domain, difficulty)

**Step 1 Outputs:**
- data/step01_response_level_data_raw.csv (28,000 rows, 5 cols: composite_ID, UID, TEST, item_name, response)

**Step 2 Outputs:**
- data/step02_response_with_difficulty_tsvr.csv (28,000 rows, 9 cols: merged with difficulty and TSVR)

**Step 3 Outputs:**
- data/step03_glmm_input.csv (28,000 rows, 11 cols: centered difficulty, ready for GLMM)

**Step 4 Outputs:**
- data/step04_glmm_model.pkl (fitted pymer4 GLMM object)
- data/step04_glmm_model_summary.txt (text summary with convergence status)
- data/step04_fixed_effects.csv (14 rows: all fixed effects with odds ratios)

**Step 5 Outputs:**
- data/step05_omnibus_interaction_test.csv (1 row: chi-square test of 3-way interaction)
- data/step05_three_way_interaction_terms.csv (2 rows: Where vs What, When vs What)
- data/step05_post_hoc_contrasts.csv (3 rows: domain contrasts with dual p-values, created only if omnibus significant)

**Step 6 Outputs:**
- data/step06_difficulty_trajectories_by_domain.csv (24 rows: plot source data for 6 trajectories)

### Logs (ONLY execution logs - .log files capturing stdout/stderr)

- logs/step00_load_item_difficulty.log
- logs/step01_extract_responses.log
- logs/step02_merge_data.log
- logs/step03_center_difficulty.log
- logs/step04_fit_glmm.log
- logs/step05_extract_interactions.log
- logs/step06_prepare_plot_data.log

### Plots (EMPTY until rq_plots runs)

**Note:** Plot source CSV created during analysis (Step 6), but actual PNG visualization generated later by rq_plots agent.

- plots/step06_difficulty_trajectories_by_domain.png (created by rq_plots, NOT by analysis steps)
  - 6-line trajectory plot: 3 domains x 2 difficulty levels
  - Probability scale [0,1]
  - Confidence bands
  - Predicted trajectories from GLMM

### Results (EMPTY until rq_results runs)

- results/summary.md (created by rq_results, NOT by analysis steps)

---

## Expected Data Formats

### Long Format Structure (Steps 1-6)

All data from Step 1 onward uses **long format** (one row per UID x test x item response):
- **Rows:** 28,000 (100 participants x 4 tests x 70 items)
- **Unit of analysis:** Individual item response (binary outcome)
- **Random effects grouping:** UID (participants) and item_name (items) - crossed structure

**Critical for GLMM:**
- Outcome variable (response) is binary: {0, 1, NaN}
- NaN responses excluded during model fitting
- Crossed random effects require explicit specification: `(Time | UID) + (1 | Item)`

### Column Naming Conventions

Per names.md established conventions:
- **composite_ID:** {UID}_{TEST} format (e.g., A010_T1)
- **UID:** Participant identifier (A### format)
- **TEST:** Test session (T1, T2, T3, T4)
- **test_num:** Nominal days (0, 1, 3, 6)
- **Time:** TSVR_hours (actual elapsed time per Decision D070)
- **domain:** Categorical factor {What, Where, When} - capitalized
- **difficulty:** IRT b parameter (original)
- **Difficulty_c:** Grand-mean centered difficulty (predictor in GLMM)
- **response:** Binary outcome {0.0, 1.0, NaN}

### Data Type Constraints

**Nullable columns:**
- `response` (NaN acceptable for missing/unadministered items)

**Non-nullable columns:**
- All predictors: UID, TEST, test_num, Time, domain, difficulty, Difficulty_c, item_name
- Missing predictors indicate data merge failure (QUIT with error)

**Value Ranges:**
- response: {0.0, 1.0, NaN}
- Time (TSVR_hours): [0, 240] (allows delayed test completion)
- test_num: {0, 1, 3, 6}
- difficulty: typically [-6, 6] (IRT b parameter)
- Difficulty_c: centered around 0, same range as difficulty
- domain: exact string match {What, Where, When}

---

## Cross-RQ Dependencies

### Dependency Type: DERIVED Data from Other RQs + RAW Data

**This RQ requires outputs from:**

**RQ 5.2.1 (Domain-Specific Trajectories) - MUST complete Steps 0-3:**

**File 1:** results/ch5/5.2.1/data/step03_item_parameters.csv
- **Used in:** Step 0 (load item difficulty)
- **Rationale:** RQ 5.2.1 performs IRT calibration with 3-factor What/Where/When structure and 2-pass purification (Decision D039). This RQ uses those item difficulty estimates as predictor variable.
- **Required columns:** item_name, dimension, a, b

**File 2:** results/ch5/5.2.1/data/step02_purified_items.csv
- **Used in:** Step 0 (verify purification)
- **Rationale:** Ensure only purified items (a >= 0.4, |b| <= 3.0) are included in analysis.
- **Required columns:** item_name, dimension, retained

**File 3:** results/ch5/5.2.1/data/step00_tsvr_mapping.csv
- **Used in:** Step 2 (merge TSVR time variable)
- **Rationale:** Decision D070 requires TSVR_hours (actual time since encoding) as time variable, not nominal days.
- **Required columns:** composite_ID, TSVR_hours

**Execution Order Constraint:**
1. **RQ 5.2.1 must complete first** (Steps 0-3: IRT calibration, purification, final theta extraction)
2. **This RQ executes second** (uses RQ 5.2.1 item parameters as predictor)

**RAW Data Source (No RQ dependency):**

**File:** data/cache/dfData.csv
- **Used in:** Step 1 (extract raw binary responses)
- **Rationale:** Item-level responses needed for GLMM (NOT aggregated theta scores - this is response-level analysis)
- **Tag Patterns:**
  - What domain: `-N-` tags
  - Where domain: `-L-`, `-U-`, `-D-` tags
  - When domain: `-O-` tags
- **Extraction:** Binary responses (0/1) for items present in RQ 5.2.1 purified item list

**Data Source Boundaries:**

**DERIVED data:**
- Item difficulty parameters from RQ 5.2.1 (IRT calibration output)
- TSVR mapping from RQ 5.2.1 (time variable)
- Purified item list from RQ 5.2.1 (item filtering)

**RAW data:**
- Binary item responses from dfData.csv (extracted directly, no RQ dependency)

**Scope:**
- This RQ does NOT re-calibrate IRT models (uses RQ 5.2.1 parameters as fixed predictor)
- This RQ does NOT perform item purification (uses RQ 5.2.1 purification results)
- This RQ analyzes item-level responses with crossed random effects (new analysis, not derivative of RQ 5.2.1 LMM)

**Validation:**

**Circuit Breaker: Dependency Check in Step 0**
- Check: results/ch5/5.2.1/data/step03_item_parameters.csv exists
- Check: results/ch5/5.2.1/data/step02_purified_items.csv exists
- Check: results/ch5/5.2.1/data/step00_tsvr_mapping.csv exists
- If ANY file missing -> QUIT with EXPECTATIONS ERROR:
  - "RQ 5.2.1 must complete Steps 0-3 before RQ 5.2.8 can run"
  - "Missing file: {path}"
  - "Action: Execute RQ 5.2.1 first or verify rq_inspect: success for Steps 0-3"

**Reference:** Best practices workflow.md Section 5 (Data Source Conventions), Concept.md Section "Data Source"

---

## Validation Requirements

### CRITICAL MANDATE

Every analysis step in this plan MUST use validation tools after analysis tool execution.

This is not optional. This is the core architectural principle preventing cascading failures observed in v3.0 (where analysis errors propagated undetected through 5+ downstream steps before discovery).

**Exact Specification Requirement:**

> "Validation tools MUST be used after analysis tool execution"

**Implementation:**
- rq_tools (Step 11 workflow) will read tools_catalog.md validation tools section
- rq_tools will specify BOTH analysis tool + validation tool per step in 3_tools.yaml
- rq_analysis (Step 12 workflow) will embed validation tool call AFTER analysis tool call in 4_analysis.yaml
- g_code (Step 14 workflow) will generate stepNN_name.py scripts with validation function calls
- bash execution (Step 14 workflow) will run analysis -> validation -> error on validation failure

**Downstream Agent Requirements:**
- **rq_tools:** MUST specify validation tool for EVERY analysis step (no exceptions)
- **rq_analysis:** MUST embed validation tool call for EVERY analysis step (no exceptions)
- **g_code:** MUST generate code with validation function calls (no exceptions)
- **rq_inspect:** MUST verify validation ran successfully (checks logs/stepNN_name.log for validation output)

---

### Validation Requirements By Step

#### Step 0: Load Item Difficulty from RQ 5.2.1

**Analysis Tool:** (determined by rq_tools - likely tools.data loading functions + pandas operations)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure, check_file_exists, validate_data_columns)

**What Validation Checks:**
- File exists: results/ch5/5.2.1/data/step03_item_parameters.csv
- Expected columns present: item_name, dimension, a, b
- Expected row count: ~70 items (post-purification)
- No NaN values in difficulty (b) column
- Domain values valid: {what, where, when} -> mapped to {What, Where, When}
- All items in item_parameters.csv present in purified_items.csv with retained=True

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "File not found: item_parameters.csv")
- Log failure to logs/step00_load_item_difficulty.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked by master to diagnose root cause (likely RQ 5.2.1 incomplete or file path error)

---

#### Step 1: Extract Raw Binary Responses

**Analysis Tool:** (determined by rq_tools - likely tools.data extraction functions)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure, check_missing_data, validate_data_columns)

**What Validation Checks:**
- File loaded: data/cache/dfData.csv
- Expected columns present: UID, TEST, item columns matching purified item tags
- Expected row count after reshape: 28,000 (100 participants x 4 tests x 70 items)
- Response values valid: {0.0, 1.0, NaN} only
- composite_ID format correct: {UID}_{TEST} pattern
- Missing data rate <30% (NaN responses acceptable but not excessive)
- All 100 participants present (UID count = 100 unique)
- All 4 test sessions present (TEST values = {T1, T2, T3, T4})

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Row count mismatch: expected 28,000, found {N}")
- Log failure to logs/step01_extract_responses.log
- Quit script immediately
- g_debug invoked to diagnose (likely dfData.csv extraction error or tag mismatch)

---

#### Step 2: Merge Responses with Difficulty and TSVR

**Analysis Tool:** (determined by rq_tools - likely pandas merge operations)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure, check_missing_data)

**What Validation Checks:**
- Output file exists: data/step02_response_with_difficulty_tsvr.csv
- Expected row count: 28,000 (no row loss during merges)
- Expected columns present: composite_ID, UID, TEST, test_num, item_name, response, domain, difficulty, TSVR_hours
- No NaN in predictor columns: domain, difficulty, TSVR_hours (merge should be complete)
- NaN acceptable only in response column (missing responses)
- All 400 composite_IDs from Step 1 matched with TSVR mapping (100% merge success)
- All 70 items from Step 0 matched with difficulty (100% merge success)
- TSVR_hours range reasonable: [0, 240] hours

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "NaN detected in TSVR_hours: {N} rows")
- Log failure to logs/step02_merge_data.log
- Quit script immediately
- g_debug invoked to diagnose (likely RQ 5.2.1 TSVR mapping incomplete or merge key mismatch)

---

#### Step 3: Grand-Mean Center Item Difficulty

**Analysis Tool:** (determined by rq_tools - likely pandas arithmetic operations)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_standardization or custom centering check)

**What Validation Checks:**
- Output file exists: data/step03_glmm_input.csv
- Expected row count: 28,000 (no row loss)
- Expected columns present: all from Step 2 + Difficulty_c, Time
- Difficulty_c centered: mean(Difficulty_c) in [-0.1, 0.1] (tolerance for rounding)
- Variance preserved: SD(Difficulty_c) = SD(difficulty) within 1%
- No NaN introduced in Difficulty_c or Time columns

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Centering failed: mean(Difficulty_c)={X}, expected ~0")
- Log failure to logs/step03_center_difficulty.log
- Quit script immediately
- g_debug invoked to diagnose (likely computational error in centering)

---

#### Step 4: Fit Cross-Classified GLMM

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_glmm or pymer4 wrapper functions)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_model_convergence, validate_lmm_assumptions_comprehensive adapted for GLMM)

**What Validation Checks:**
- Output files exist: step04_glmm_model.pkl, step04_glmm_model_summary.txt, step04_fixed_effects.csv
- Model converged: model.converged = True OR documented simplification applied
- Fixed effects table complete: ~14 terms estimated (intercept + main + 2-way + 3-way interactions)
- No NaN in estimates, SE, z_value, p_value, OR, CI bounds
- Random effects variance components positive (if extracted)
- Observations used: ~19,600-22,400 (70-80% of 28,000 after removing NaN responses)
- All 100 participants present in analysis
- All 70 items present in analysis
- **GLMM-specific checks:**
  - Overdispersion: Residual deviance / df in [0.8, 1.2] (acceptable range)
  - Predicted probabilities in reasonable range: [0.05, 0.95] for majority (>50%)
  - No singular fit warnings (or documented simplification if present)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "GLMM convergence failed after all 4 attempts")
- Log failure to logs/step04_fit_glmm.log
- Quit script immediately
- g_debug invoked to diagnose (likely convergence issue, data structure problem, insufficient variation)

---

#### Step 5: Extract Interaction Terms

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm contrast extraction functions adapted for GLMM)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_hypothesis_test_dual_pvalues, validate_contrasts_dual_pvalues per Decision D068)

**What Validation Checks:**
- Output files exist: step05_omnibus_interaction_test.csv, step05_three_way_interaction_terms.csv
- If omnibus p < 0.05: step05_post_hoc_contrasts.csv MUST exist
- If omnibus p >= 0.05: step05_post_hoc_contrasts.csv MUST NOT exist
- Omnibus test df = 2 (two 3-way interaction terms)
- p_value in [0, 1]
- **Decision D068 compliance:**
  - Post-hoc contrasts (if created) have BOTH p_uncorrected AND p_bonferroni columns
  - p_bonferroni >= p_uncorrected (correction never decreases p-value)
  - p_bonferroni = min(p_uncorrected * 3, 1.0) per Bonferroni correction for 3 tests

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Decision D068 violation: p_bonferroni column missing")
- Log failure to logs/step05_extract_interactions.log
- Quit script immediately
- g_debug invoked to diagnose (likely extraction logic error or contrast computation failure)

---

#### Step 6: Prepare Plot Data

**Analysis Tool:** (determined by rq_tools - likely tools.plotting.prepare_*_plot_data functions)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_plot_data_completeness, validate_probability_range, validate_dataframe_structure)

**What Validation Checks:**
- Output file exists: data/step06_difficulty_trajectories_by_domain.csv
- Expected row count: exactly 24 (3 domains x 2 difficulty levels x 4 timepoints)
- Expected columns present: domain, difficulty_level, Difficulty_c, Time, test_num, predicted_probability, CI_lower, CI_upper
- Complete factorial design: all combinations of 3 domains x 2 difficulty x 4 timepoints present
- No NaN values in predicted_probability, CI_lower, CI_upper
- predicted_probability in [0, 1] (bounded by logit transformation)
- CI_lower < predicted_probability < CI_upper for all rows
- No duplicate rows (domain x difficulty_level x Time combinations unique)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Expected 24 rows (factorial design), found {N}")
- Log failure to logs/step06_prepare_plot_data.log
- Quit script immediately (do NOT proceed to plotting - but rq_plots is separate agent)
- g_debug invoked to diagnose (likely prediction grid error or model prediction failure)

---

## Summary

**Total Steps:** 7 (Step 0 + Steps 1-6)

**Estimated Runtime:** 60-90 minutes total
- Steps 0-3: 10-15 min (data manipulation)
- Step 4: 45-60 min (GLMM fitting with potential convergence challenges)
- Steps 5-6: 5-15 min (extraction and plotting prep)

**Cross-RQ Dependencies:** RQ 5.2.1 (must complete Steps 0-3 for item parameters, purification list, TSVR mapping)

**Primary Outputs:**
- Item difficulty lookup (Step 0)
- Long-format response data (Steps 1-3)
- Fitted GLMM with binomial family (Step 4)
- Three-way interaction tests with dual p-values (Step 5 - Decision D068)
- Plot source CSV for 6 difficulty trajectories by domain (Step 6)

**Validation Coverage:** 100% (all 7 steps have validation requirements with 4-layer substance criteria)

**Key Decisions Applied:**
- **D068:** Dual p-value reporting (uncorrected + Bonferroni for post-hoc contrasts)
- **D070:** TSVR_hours as time variable (actual elapsed time)
- **Exploratory design:** Omnibus test first, post-hoc only if significant

**Critical Notes:**
- GLMM required (NOT LMM) - binary responses
- Crossed random effects (UID x Item) - pymer4 implementation
- Random slopes convergence risk - pre-specified simplification strategy
- Odds ratios reported for interpretation
- Plot source CSV created in data/ during analysis, PNG created in plots/ later by rq_plots

---

**Next Steps (Workflow):**

1. User reviews and approves this plan (Step 7 user gate per workflow)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-02): Initial plan created by rq_planner agent for RQ 5.2.8
