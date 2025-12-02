# Analysis Plan: RQ 5.4.3 - Age x Schema Interactions

**Research Question:** 5.4.3
**Created:** 2025-12-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines whether age-related forgetting effects differ across schema congruence levels (common, congruent, incongruent) using a 3-way Age x Congruence x Time interaction in a Linear Mixed Model. The analysis tests the hypothesis that older adults rely more on schema-based consolidation, predicting that age effects will be smallest for congruent items (maximum schema support) and largest for incongruent items (minimum schema support).

**Pipeline:** LMM-only (uses DERIVED theta scores from RQ 5.4.1)

**Steps:** 6 total analysis steps (Step 0: dependency validation + Steps 1-5: analysis)

**Estimated Runtime:** Medium (~15-20 minutes total)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni for 3-way interaction terms, Tukey for post-hoc contrasts)
- Decision D070: TSVR as time variable (actual hours since encoding, not nominal days)

---

## Analysis Plan

### Step 0: Load and Validate Dependency Files

**Dependencies:** None (first step)
**Complexity:** Low (data loading and validation only, <1 minute)

**Purpose:** Load theta scores from RQ 5.4.1, TSVR mapping from RQ 5.4.1, and Age variable from master data. Validate all dependencies exist and have correct structure before proceeding.

**Input:**

**File 1:** results/ch5/5.4.1/data/step03_theta_scores.csv
**Source:** RQ 5.4.1 Step 3 (IRT calibration for congruence factors)
**Format:** CSV, wide format (one row per composite_ID)
**Expected Columns:**
  - `composite_ID` (string, format: UID_test, e.g., P001_T1)
  - `theta_common` (float, ability estimate for common items)
  - `theta_congruent` (float, ability estimate for congruent items)
  - `theta_incongruent` (float, ability estimate for incongruent items)
  - `se_common` (float, standard error for common theta)
  - `se_congruent` (float, standard error for congruent theta)
  - `se_incongruent` (float, standard error for incongruent theta)
**Expected Rows:** 400 (100 participants x 4 tests)

**File 2:** results/ch5/5.4.1/data/step00_tsvr_mapping.csv
**Source:** RQ 5.4.1 Step 0 (TSVR extraction)
**Format:** CSV, one row per composite_ID
**Expected Columns:**
  - `composite_ID` (string, format: UID_test)
  - `TSVR_hours` (float, actual hours since VR encoding session)
  - `test` (string, values: T1, T2, T3, T4)
**Expected Rows:** 400 (100 participants x 4 tests)

**File 3:** data/cache/dfData.csv
**Source:** Master data cache (participant demographics)
**Format:** CSV, one row per participant
**Required Columns:**
  - `UID` (string, participant unique identifier, format: P### with leading zeros)
  - `Age` (int or float, participant age in years at encoding, range: 20-70)
**Expected Rows:** >= 100 (must include all participants in RQ 5.4.1 theta scores)

**Processing:**
1. Read theta_scores.csv, validate 400 rows and all 7 required columns present
2. Read tsvr_mapping.csv, validate 400 rows and all 3 required columns present
3. Read dfData.csv, validate Age column present
4. Extract composite_ID list from theta_scores.csv
5. Parse composite_ID to extract UID list (remove _test suffix)
6. Validate all UIDs present in dfData.csv Age column
7. Check for missing values in critical columns (theta columns, TSVR_hours, Age)
8. Validate TSVR_hours range (expected: 0 to ~168 hours for 1-week retention)
9. Validate Age range (expected: 20 to 70 years)
10. Save validation report to logs

**Output:**

**File 1:** data/step00_theta_wide.csv
**Format:** CSV, copy of RQ 5.4.1 theta scores with validation confirmed
**Columns:** Same as input (composite_ID, theta_common, theta_congruent, theta_incongruent, se_common, se_congruent, se_incongruent)
**Expected Rows:** 400

**File 2:** data/step00_tsvr_mapping.csv
**Format:** CSV, copy of RQ 5.4.1 TSVR mapping with validation confirmed
**Columns:** Same as input (composite_ID, TSVR_hours, test)
**Expected Rows:** 400

**File 3:** data/step00_age_data.csv
**Format:** CSV, extracted Age data for participants in this RQ
**Columns:**
  - `UID` (string, participant identifier)
  - `Age` (int or float, age in years)
**Expected Rows:** 100 (one row per unique participant)

**Validation Requirement:**
Validation tools MUST be used after data loading tool execution. Specific validation tools will be determined by rq_tools based on data format requirements (file existence, column presence, row counts, value ranges).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_theta_wide.csv: 400 rows x 7 columns (composite_ID: object, theta_common: float64, theta_congruent: float64, theta_incongruent: float64, se_common: float64, se_congruent: float64, se_incongruent: float64)
- data/step00_tsvr_mapping.csv: 400 rows x 3 columns (composite_ID: object, TSVR_hours: float64, test: object)
- data/step00_age_data.csv: 100 rows x 2 columns (UID: object, Age: int64 or float64)

*Value Ranges:*
- theta_common, theta_congruent, theta_incongruent in [-4, 4] (typical IRT ability range, slightly wider than [-3, 3] to accommodate outliers)
- se_common, se_congruent, se_incongruent in [0.1, 1.5] (standard error range, above 1.5 suggests unreliable estimates)
- TSVR_hours in [0, 200] hours (0=encoding T1, ~168=1 week for T4, allow buffer for scheduling variation)
- Age in [20, 70] years (study inclusion criteria)

*Data Quality:*
- No NaN values in theta columns (all participants must have estimates)
- No NaN values in TSVR_hours (all sessions must have timing data)
- No NaN values in Age (all participants must have age recorded)
- All 400 composite_IDs present from RQ 5.4.1 (no data loss)
- All 100 UIDs present when parsing composite_IDs
- test column contains only {T1, T2, T3, T4} (no unexpected values)

*Log Validation:*
- Required pattern: "Loaded theta_scores: 400 rows, 7 columns"
- Required pattern: "Loaded tsvr_mapping: 400 rows, 3 columns"
- Required pattern: "Loaded age_data: 100 participants"
- Required pattern: "All dependency files validated successfully"
- Forbidden patterns: "ERROR", "Missing file", "Column not found", "NaN detected in critical columns"
- Acceptable warnings: None expected for dependency loading

**Expected Behavior on Validation Failure:**
- If RQ 5.4.1 files missing: QUIT with "EXPECTATIONS ERROR: RQ 5.4.1 must complete Step 3 before this RQ"
- If Age column missing in dfData.csv: QUIT with "EXPECTATIONS ERROR: Age variable not found in master data"
- If row counts mismatch: QUIT with specific error (e.g., "Expected 400 composite_IDs, found 387")
- If NaN values detected: QUIT with "Data quality error: NaN values in [column names]"
- Log failure to logs/step00_load_dependencies.log
- g_debug invoked to diagnose root cause

---

### Step 1: Merge Data and Prepare LMM Input

**Dependencies:** Step 0 (requires validated theta, TSVR, Age files)
**Complexity:** Low (data transformation only, <1 minute)

**Purpose:** Merge theta scores with TSVR and Age variables, reshape from wide to long format (400 rows -> 1200 rows: 100 participants x 4 tests x 3 congruence levels), grand-mean center Age, create time transformations for LMM.

**Input:**

**File 1:** data/step00_theta_wide.csv (from Step 0)
**File 2:** data/step00_tsvr_mapping.csv (from Step 0)
**File 3:** data/step00_age_data.csv (from Step 0)

**Processing:**

**Merge Logic:**
1. Parse composite_ID in theta_wide to extract UID (remove _test suffix)
2. Left join theta_wide with age_data on UID (adds Age column, expect all 400 rows matched)
3. Left join result with tsvr_mapping on composite_ID (adds TSVR_hours and test columns, expect all 400 rows matched)
4. Validate no NaN values introduced during merges (merge keys must match perfectly)

**Reshape Logic (Wide -> Long):**
1. Current format: 400 rows x columns (composite_ID, theta_common, theta_congruent, theta_incongruent, se_common, se_congruent, se_incongruent, Age, TSVR_hours, test)
2. Reshape using pd.melt or equivalent:
   - id_vars: composite_ID, Age, TSVR_hours, test
   - value_vars: theta_common, theta_congruent, theta_incongruent
   - var_name: congruence (values: theta_common -> Common, theta_congruent -> Congruent, theta_incongruent -> Incongruent)
   - value_name: theta
3. Similarly reshape SE columns:
   - value_vars: se_common, se_congruent, se_incongruent
   - var_name: se_congruence
   - value_name: se_theta
4. Merge theta and se_theta long dataframes on composite_ID + congruence
5. Result: 1200 rows (400 composite_IDs x 3 congruence levels) x columns (composite_ID, test, congruence, theta, se_theta, Age, TSVR_hours)

**Age Centering:**
1. Compute grand mean of Age across all 100 participants: Age_mean = mean(Age)
2. Create Age_c = Age - Age_mean (grand-mean centered, mean approximately 0)
3. Validate Age_c mean close to 0 (within ±0.1 tolerance for sampling variation)

**Time Transformations:**
1. Create log_TSVR = log(TSVR_hours + 1) (log transformation, add 1 to handle TSVR_hours=0 at encoding)
2. TSVR_hours remains as linear time variable
3. Both time variables will be used in LMM per RQ 5.4.1 best model selection (linear + logarithmic time terms)

**Contrast Coding for Congruence:**
1. Set reference category: Common (schema-neutral baseline per concept.md Section "Congruence Reference Category")
2. Create dummy variables: Congruent (1 if congruence=Congruent, 0 otherwise), Incongruent (1 if congruence=Incongruent, 0 otherwise)
3. Common is implicit reference when both dummies = 0

**Output:**

**File:** data/step01_lmm_input.csv
**Format:** CSV, long format (one row per observation)
**Columns:**
  - `UID` (string, participant identifier parsed from composite_ID)
  - `composite_ID` (string, original composite_ID for traceability)
  - `test` (string, values: T1, T2, T3, T4)
  - `congruence` (string, values: Common, Congruent, Incongruent)
  - `theta` (float, IRT ability estimate for this participant-test-congruence combination)
  - `se_theta` (float, standard error of theta estimate)
  - `Age` (float, participant age in years, original scale)
  - `Age_c` (float, grand-mean centered age, mean approximately 0)
  - `TSVR_hours` (float, linear time variable per Decision D070)
  - `log_TSVR` (float, logarithmic time transformation)
**Expected Rows:** 1200 (100 participants x 4 tests x 3 congruence levels)
**Expected Format:** Long format ready for LMM fitting

**Validation Requirement:**
Validation tools MUST be used after data transformation tool execution. Specific validation tools determined by rq_tools based on reshaping and centering requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_lmm_input.csv: 1200 rows x 10 columns (UID: object, composite_ID: object, test: object, congruence: object, theta: float64, se_theta: float64, Age: float64, Age_c: float64, TSVR_hours: float64, log_TSVR: float64)

*Value Ranges:*
- theta in [-4, 4] (IRT ability range)
- se_theta in [0.1, 1.5] (standard error range)
- Age in [20, 70] years (original scale)
- Age_c in [-30, 30] years (centered, range = original range ± mean age ~45)
- TSVR_hours in [0, 200] hours
- log_TSVR in [0, 5.5] (log(200+1) approximately 5.3)

*Data Quality:*
- Exactly 1200 rows (no data loss during reshape: 400 wide rows x 3 congruence levels = 1200 long rows)
- No NaN values in any column (all merges successful, all transformations valid)
- congruence column contains only {Common, Congruent, Incongruent} (no unexpected values)
- test column contains only {T1, T2, T3, T4}
- Age_c mean within ±0.1 of 0 (grand-mean centering successful)
- Age_c standard deviation approximately equal to Age standard deviation (centering preserves spread)
- Each UID appears exactly 12 times (4 tests x 3 congruence levels)

*Log Validation:*
- Required pattern: "Merged data: 400 rows (all composite_IDs matched)"
- Required pattern: "Reshaped to long format: 1200 rows (400 x 3 congruence levels)"
- Required pattern: "Age grand-mean centered: mean(Age_c) = [value close to 0]"
- Required pattern: "Time transformations created: TSVR_hours (linear), log_TSVR (logarithmic)"
- Required pattern: "Contrast coding applied: Common (reference), Congruent, Incongruent"
- Forbidden patterns: "ERROR", "NaN introduced", "Merge failed", "Row count mismatch"
- Acceptable warnings: None expected for data merging/reshaping

**Expected Behavior on Validation Failure:**
- If merge introduces NaN: QUIT with "Data quality error: Merge failed, NaN values introduced in [columns]"
- If row count != 1200: QUIT with "Reshape error: Expected 1200 rows, found [actual]"
- If Age_c mean > 0.1: QUIT with "Centering error: Age_c mean = [value], expected approximately 0"
- Log failure to logs/step01_prepare_lmm_input.log
- g_debug invoked to diagnose

---

### Step 2: Fit LMM with 3-Way Age x Congruence x Time Interaction

**Dependencies:** Step 1 (requires prepared LMM input)
**Complexity:** Medium (LMM fitting with complex interaction structure, ~5-10 minutes depending on convergence)

**Purpose:** Fit Linear Mixed Model testing 3-way Age x Congruence x Time interaction. Model includes random intercepts and slopes for TSVR_hours by participant. Tests whether age-related forgetting effects differ across schema congruence levels.

**Input:**

**File:** data/step01_lmm_input.csv (from Step 1)
**Format:** Long format, 1200 rows x 10 columns

**Processing:**

**Model Formula:**
```
theta ~ 1 + TSVR_hours + log_TSVR + Age_c + Congruent + Incongruent +
        (Age_c * TSVR_hours) + (Age_c * log_TSVR) +
        (Congruent * TSVR_hours) + (Congruent * log_TSVR) +
        (Incongruent * TSVR_hours) + (Incongruent * log_TSVR) +
        (Age_c * Congruent) + (Age_c * Incongruent) +
        (Age_c * Congruent * TSVR_hours) + (Age_c * Congruent * log_TSVR) +
        (Age_c * Incongruent * TSVR_hours) + (Age_c * Incongruent * log_TSVR)
```

**Fixed Effects:**
- Intercept (baseline theta for Common congruence at Age_c=0, TSVR_hours=0)
- TSVR_hours (linear time effect for Common congruence)
- log_TSVR (logarithmic time effect for Common congruence)
- Age_c (main effect of age on theta for Common congruence at encoding)
- Congruent (difference between Congruent and Common at Age_c=0, TSVR_hours=0)
- Incongruent (difference between Incongruent and Common at Age_c=0, TSVR_hours=0)
- Age_c:TSVR_hours (2-way interaction: age x linear time for Common congruence)
- Age_c:log_TSVR (2-way interaction: age x logarithmic time for Common congruence)
- Congruent:TSVR_hours (2-way interaction: Congruent vs Common x linear time)
- Congruent:log_TSVR (2-way interaction: Congruent vs Common x logarithmic time)
- Incongruent:TSVR_hours (2-way interaction: Incongruent vs Common x linear time)
- Incongruent:log_TSVR (2-way interaction: Incongruent vs Common x logarithmic time)
- Age_c:Congruent (2-way interaction: age x Congruent vs Common)
- Age_c:Incongruent (2-way interaction: age x Incongruent vs Common)
- **Age_c:Congruent:TSVR_hours** (3-way interaction: PRIMARY HYPOTHESIS TERM 1)
- **Age_c:Congruent:log_TSVR** (3-way interaction: PRIMARY HYPOTHESIS TERM 2)
- **Age_c:Incongruent:TSVR_hours** (3-way interaction: PRIMARY HYPOTHESIS TERM 3)
- **Age_c:Incongruent:log_TSVR** (3-way interaction: PRIMARY HYPOTHESIS TERM 4)

**Random Effects:**
- Random intercepts by UID: (1 | UID)
- Random slopes for TSVR_hours by UID: (TSVR_hours | UID)
- Allows each participant to have unique baseline theta and unique forgetting rate over time

**Convergence Contingency Plan (per concept.md Section "Convergence Contingency Plan"):**
1. Attempt full model with random slopes (TSVR_hours | UID)
2. If convergence fails:
   a. Try alternative optimizers (bobyqa, nlminb)
   b. Likelihood ratio test (LRT) comparing random slopes vs intercept-only
   c. If LRT p < 0.05: Retain slopes with simplified correlation structure
   d. If LRT p >= 0.05: Use random intercepts-only model (1 | UID)
3. Document which random structure achieved convergence in model summary

**Fitting Method:**
- Use REML (Restricted Maximum Likelihood) for variance component estimation
- statsmodels MixedLM or similar LMM implementation
- Maximum iterations: 200 (default), increase to 500 if initial convergence fails
- Convergence tolerance: default (typically 1e-4 for gradient norm)

**Output:**

**File 1:** data/step02_lmm_model.pkl
**Format:** Pickled Python object (statsmodels MixedLMResults or equivalent)
**Purpose:** Save fitted model for downstream steps (contrast extraction, marginal means)

**File 2:** data/step02_lmm_model_summary.txt
**Format:** Plain text file
**Content:**
- Model formula
- Convergence status (True/False)
- Random effects structure used (slopes or intercepts-only)
- Fixed effects table (coefficient, SE, z-statistic, p-value for all terms)
- Random effects variance components (intercept variance, slope variance, residual variance)
- Model fit indices (AIC, BIC, log-likelihood)
- Sample size (N=1200 observations, N_groups=100 participants)

**File 3:** data/step02_fixed_effects.csv
**Format:** CSV
**Columns:**
  - `term` (string, fixed effect name, e.g., "Age_c:Congruent:TSVR_hours")
  - `coef` (float, estimated coefficient)
  - `se` (float, standard error)
  - `z` (float, z-statistic)
  - `p` (float, p-value, two-tailed)
**Expected Rows:** 18 (all fixed effects terms)

**Validation Requirement:**
Validation tools MUST be used after LMM fitting tool execution. Specific validation tools determined by rq_tools based on LMM convergence, residuals, and assumptions (tools.validation.validate_lmm_assumptions_comprehensive per tools_catalog.md).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_lmm_model.pkl: Python pickle object (size > 10 KB, indicates fitted model saved)
- data/step02_lmm_model_summary.txt: Text file (size > 1 KB, indicates summary written)
- data/step02_fixed_effects.csv: 18 rows x 5 columns (term: object, coef: float64, se: float64, z: float64, p: float64)

*Value Ranges:*
- coef unrestricted (interaction coefficients can be positive or negative)
- se in [0.001, 2.0] (standard errors must be positive, above 2.0 suggests estimation problem)
- z unrestricted (z-statistics can be any value)
- p in [0, 1] (p-values must be valid probabilities)
- All 4 three-way interaction terms present in fixed_effects.csv: Age_c:Congruent:TSVR_hours, Age_c:Congruent:log_TSVR, Age_c:Incongruent:TSVR_hours, Age_c:Incongruent:log_TSVR

*Data Quality:*
- Model converged successfully (model.converged = True in model object)
- All 18 fixed effects terms present (no missing estimates)
- No NaN values in coefficient, SE, z, or p columns
- Standard errors all positive (SE > 0 for all terms)
- p-values valid (no NaN, no negative, no > 1.0)
- Model summary contains convergence status statement

*Log Validation:*
- Required pattern: "Model converged: True"
- Required pattern: "Random effects structure: [slopes/intercepts-only]"
- Required pattern: "Fixed effects: 18 terms estimated"
- Required pattern: "VALIDATION - PASS: LMM convergence"
- Required pattern: "VALIDATION - PASS: LMM residuals normality"
- Required pattern: "VALIDATION - PASS: LMM assumptions (homoscedasticity, linearity, independence)"
- Forbidden patterns: "Model converged: False", "ERROR", "Singular covariance matrix", "NaN in estimates"
- Acceptable warnings: "Convergence warning" (if alternative optimizer succeeded), "Random slopes simplified" (if LRT justified intercepts-only)

**Expected Behavior on Validation Failure:**
- If convergence fails after contingency plan: QUIT with "Model fitting error: LMM did not converge after trying alternative optimizers and random structures"
- If NaN estimates: QUIT with "Model fitting error: NaN values in coefficient estimates"
- If assumptions violated: Log warnings, report robust SEs recommended in model summary, but proceed to Step 3
- Log failure to logs/step02_fit_lmm.log
- g_debug invoked for convergence failures

---

### Step 3: Extract 3-Way Interaction Terms with Dual P-Values

**Dependencies:** Step 2 (requires fitted LMM model)
**Complexity:** Low (extraction and correction only, <1 minute)

**Purpose:** Extract the 4 three-way interaction terms (Age_c x Congruence x Time) from fitted model and apply Bonferroni correction for multiple comparisons. Report dual p-values per Decision D068.

**Input:**

**File 1:** data/step02_lmm_model.pkl (from Step 2)
**File 2:** data/step02_fixed_effects.csv (from Step 2)

**Processing:**

**Extract 3-Way Interaction Terms:**
1. Filter fixed_effects.csv for rows where term contains all three components: "Age_c", congruence level ("Congruent" or "Incongruent"), and time term ("TSVR_hours" or "log_TSVR")
2. Expected terms:
   - Age_c:Congruent:TSVR_hours
   - Age_c:Congruent:log_TSVR
   - Age_c:Incongruent:TSVR_hours
   - Age_c:Incongruent:log_TSVR
3. Extract coefficient, SE, z-statistic, p-value for each term

**Bonferroni Correction:**
1. Number of time terms tested: 2 (TSVR_hours and log_TSVR)
2. Bonferroni alpha = 0.05 / 2 = 0.025 (per concept.md hypothesis section)
3. For each term:
   - p_uncorrected = original p-value from model
   - p_bonferroni = min(p_uncorrected * 2, 1.0) (Bonferroni correction factor = 2)
4. Decision criterion: Reject null hypothesis if p_bonferroni < 0.025

**Interpretation (per concept.md Section "Congruence Reference Category and Contrast Coding"):**
- Age_c:Congruent:TSVR_hours: Does age effect on linear forgetting differ between Congruent and Common?
- Age_c:Congruent:log_TSVR: Does age effect on logarithmic forgetting differ between Congruent and Common?
- Age_c:Incongruent:TSVR_hours: Does age effect on linear forgetting differ between Incongruent and Common?
- Age_c:Incongruent:log_TSVR: Does age effect on logarithmic forgetting differ between Incongruent and Common?

**Output:**

**File:** data/step03_interaction_terms.csv
**Format:** CSV
**Columns:**
  - `term` (string, interaction term name)
  - `coef` (float, estimated coefficient)
  - `se` (float, standard error)
  - `z` (float, z-statistic)
  - `p_uncorrected` (float, original p-value from model)
  - `p_bonferroni` (float, Bonferroni-corrected p-value)
  - `significant_bonferroni` (bool, True if p_bonferroni < 0.025)
**Expected Rows:** 4 (one row per 3-way interaction term)

**Validation Requirement:**
Validation tools MUST be used after extraction tool execution. Specific validation tools determined by rq_tools (tools.validation.validate_hypothesis_test_dual_pvalues per tools_catalog.md to ensure dual p-values present per Decision D068).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_interaction_terms.csv: 4 rows x 7 columns (term: object, coef: float64, se: float64, z: float64, p_uncorrected: float64, p_bonferroni: float64, significant_bonferroni: bool)

*Value Ranges:*
- coef unrestricted (can be positive or negative)
- se in [0.001, 2.0] (must be positive)
- z unrestricted
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1] (corrected p-values capped at 1.0)
- significant_bonferroni in {True, False}

*Data Quality:*
- Exactly 4 rows (all 4 three-way interaction terms present)
- No NaN values in any column
- BOTH p_uncorrected AND p_bonferroni columns present (Decision D068 dual p-value requirement)
- p_bonferroni = min(p_uncorrected * 2, 1.0) for all rows (verify correction applied correctly)
- significant_bonferroni = (p_bonferroni < 0.025) for all rows (verify threshold applied correctly)

*Log Validation:*
- Required pattern: "Extracted 4 three-way interaction terms"
- Required pattern: "Bonferroni correction applied: alpha = 0.025, correction factor = 2"
- Required pattern: "VALIDATION - PASS: Dual p-values present (uncorrected + bonferroni)"
- Forbidden patterns: "ERROR", "Missing interaction term", "NaN in p-values"
- Acceptable warnings: None expected for extraction step

**Expected Behavior on Validation Failure:**
- If < 4 interaction terms found: QUIT with "Extraction error: Expected 4 three-way interaction terms, found [actual]"
- If dual p-values missing: QUIT with "Decision D068 violation: Must report both p_uncorrected and p_bonferroni"
- If Bonferroni correction incorrect: QUIT with "Correction error: p_bonferroni != p_uncorrected * 2 for term [name]"
- Log failure to logs/step03_extract_interactions.log
- g_debug invoked

---

### Step 4: Compute Congruence-Specific Age Effects at Day 3 with Tukey HSD Post-Hoc

**Dependencies:** Step 2 (requires fitted LMM model), Step 1 (requires lmm_input for marginal means computation)
**Complexity:** Medium (marginal effects computation + post-hoc contrasts, ~3-5 minutes)

**Purpose:** Compute age effect slopes at Day 3 (midpoint retention interval) for each congruence level separately. Perform Tukey HSD post-hoc tests to compare age effect sizes across Common, Congruent, and Incongruent conditions. Report dual p-values per Decision D068.

**Input:**

**File 1:** data/step02_lmm_model.pkl (from Step 2)
**File 2:** data/step01_lmm_input.csv (from Step 1)

**Processing:**

**Select Day 3 Timepoint:**
1. Filter lmm_input.csv for test == "T3" (Day 3, midpoint retention interval)
2. Compute average TSVR_hours for T3 across all participants (expected approximately 72 hours, actual varies per participant)
3. Use mean(TSVR_hours | test=T3) as evaluation point for marginal slopes

**Compute Marginal Age Slopes by Congruence:**
1. For each congruence level (Common, Congruent, Incongruent):
   a. Set congruence dummy variables accordingly
   b. Compute marginal effect of Age_c on theta at Day 3 TSVR_hours
   c. Marginal slope = partial derivative of theta with respect to Age_c, holding TSVR_hours constant at Day 3 value
   d. Include all interaction terms: Age_c + (Age_c:Congruent if congruent) + (Age_c:Incongruent if incongruent) + (Age_c:Congruent:TSVR_hours * TSVR_day3 if congruent) + (Age_c:Congruent:log_TSVR * log(TSVR_day3+1) if congruent) + etc.
2. Use delta method to propagate standard errors from model coefficients to marginal slopes
3. Compute 95% confidence intervals for each marginal slope

**Tukey HSD Post-Hoc Contrasts:**
1. Three pairwise comparisons:
   - Congruent vs Common: Does age effect differ?
   - Incongruent vs Common: Does age effect differ?
   - Incongruent vs Congruent: Does age effect differ?
2. For each comparison:
   a. Compute difference in marginal age slopes
   b. Compute SE of difference using delta method
   c. Compute z-statistic and p-value (two-tailed)
   d. Apply Tukey HSD correction: p_tukey = p-value adjusted for 3 comparisons (family-wise error rate control)
   e. Report p_uncorrected AND p_tukey per Decision D068
3. Decision criterion: Significant if p_tukey < 0.05 (Tukey correction controls family-wise alpha at 0.05)

**Output:**

**File 1:** data/step04_age_effects_by_congruence.csv
**Format:** CSV
**Columns:**
  - `congruence` (string, values: Common, Congruent, Incongruent)
  - `age_slope` (float, marginal effect of Age_c on theta at Day 3)
  - `se` (float, standard error of age slope via delta method)
  - `CI_lower` (float, lower 95% confidence bound)
  - `CI_upper` (float, upper 95% confidence bound)
  - `TSVR_day3` (float, mean TSVR_hours at Day 3 used for evaluation)
**Expected Rows:** 3 (one per congruence level)

**File 2:** data/step04_tukey_contrasts.csv
**Format:** CSV
**Columns:**
  - `contrast` (string, pairwise comparison, e.g., "Congruent - Common")
  - `estimate` (float, difference in age slopes)
  - `se` (float, standard error of difference via delta method)
  - `z` (float, z-statistic)
  - `p_uncorrected` (float, original p-value)
  - `p_tukey` (float, Tukey HSD adjusted p-value)
  - `significant_tukey` (bool, True if p_tukey < 0.05)
**Expected Rows:** 3 (all pairwise comparisons: Congruent-Common, Incongruent-Common, Incongruent-Congruent)

**Validation Requirement:**
Validation tools MUST be used after contrast computation tool execution. Specific validation tools determined by rq_tools (tools.validation.validate_contrasts_dual_pvalues per tools_catalog.md to ensure Tukey dual p-values present per Decision D068).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_age_effects_by_congruence.csv: 3 rows x 6 columns (congruence: object, age_slope: float64, se: float64, CI_lower: float64, CI_upper: float64, TSVR_day3: float64)
- data/step04_tukey_contrasts.csv: 3 rows x 7 columns (contrast: object, estimate: float64, se: float64, z: float64, p_uncorrected: float64, p_tukey: float64, significant_tukey: bool)

*Value Ranges:*
- age_slope in [-0.05, 0.05] (marginal age effects typically small in theta units per year)
- se in [0.001, 0.02] (standard errors for marginal slopes)
- CI_lower < CI_upper for all rows (confidence intervals valid)
- TSVR_day3 in [60, 90] hours (Day 3 approximately 72 hours, allow variation)
- estimate in [-0.1, 0.1] (differences in age slopes)
- p_uncorrected in [0, 1]
- p_tukey in [0, 1]
- significant_tukey in {True, False}

*Data Quality:*
- Exactly 3 age effects rows (all congruence levels present)
- Exactly 3 contrast rows (all pairwise comparisons present)
- No NaN values in any column
- BOTH p_uncorrected AND p_tukey columns present in contrasts file (Decision D068 requirement)
- All 3 contrasts present: "Congruent - Common", "Incongruent - Common", "Incongruent - Congruent" (or similar naming)
- CI_upper > CI_lower for all age effects

*Log Validation:*
- Required pattern: "Computed marginal age effects at Day 3: TSVR_day3 = [value] hours"
- Required pattern: "Tukey HSD post-hoc contrasts: 3 comparisons"
- Required pattern: "VALIDATION - PASS: Dual p-values present (uncorrected + tukey)"
- Forbidden patterns: "ERROR", "Delta method failed", "NaN in marginal slopes", "Contrast missing"
- Acceptable warnings: None expected for post-hoc computation

**Expected Behavior on Validation Failure:**
- If marginal slopes contain NaN: QUIT with "Delta method error: NaN in marginal age slopes"
- If < 3 contrasts: QUIT with "Post-hoc error: Expected 3 Tukey contrasts, found [actual]"
- If dual p-values missing: QUIT with "Decision D068 violation: Must report both p_uncorrected and p_tukey"
- Log failure to logs/step04_compute_age_effects.log
- g_debug invoked

---

### Step 5: Prepare Age Effects Plot Data by Tertiles

**Dependencies:** Step 2 (requires fitted LMM model), Step 1 (requires lmm_input for grouping)
**Complexity:** Low (data aggregation for plotting, <1 minute)

**Purpose:** Create plot source CSV for visualizing age effects across congruence levels. Group participants into age tertiles (Young/Middle/Older), compute marginal means and confidence intervals for each age tertile x congruence level x test timepoint combination. Output used by rq_plots to generate 3-panel plot (one panel per congruence level).

**Input:**

**File 1:** data/step02_lmm_model.pkl (from Step 2)
**File 2:** data/step01_lmm_input.csv (from Step 1)

**Processing:**

**Create Age Tertiles:**
1. Compute age tertile cutpoints using lmm_input.csv unique participants (N=100):
   - Tertile 1 (Young): Age <= 33rd percentile
   - Tertile 2 (Middle): 33rd percentile < Age <= 67th percentile
   - Tertile 3 (Older): Age > 67th percentile
2. Assign each participant to age tertile based on original Age variable
3. Add age_tertile column to lmm_input data (values: Young, Middle, Older)
4. Validate approximately 33-34 participants per tertile

**Compute Marginal Means:**
1. For each combination of age_tertile x congruence x test:
   a. Filter lmm_input for that combination
   b. Compute observed mean theta (descriptive statistic)
   c. Compute model-predicted mean theta using fitted LMM (marginal mean at tertile's median Age_c)
   d. Compute 95% confidence intervals for model predictions
2. Result: 3 age tertiles x 3 congruence levels x 4 tests = 36 rows

**Time Variable for Plotting:**
1. Use mean(TSVR_hours) per test across all participants as x-axis values
2. Expected approximately: T1=0h, T2=24h, T3=72h, T4=144h (1 week)

**Output:**

**File:** data/step05_age_effects_plot_data.csv
**Format:** CSV, plot source data for age effects visualization
**Columns:**
  - `age_tertile` (string, values: Young, Middle, Older)
  - `congruence` (string, values: Common, Congruent, Incongruent)
  - `test` (string, values: T1, T2, T3, T4)
  - `TSVR_hours` (float, mean TSVR hours for this test across participants)
  - `mean_theta_observed` (float, observed mean theta for this group)
  - `mean_theta_predicted` (float, model-predicted marginal mean theta)
  - `CI_lower` (float, lower 95% confidence bound for prediction)
  - `CI_upper` (float, upper 95% confidence bound for prediction)
  - `N` (int, number of observations in this cell)
**Expected Rows:** 36 (3 age tertiles x 3 congruence x 4 tests)

**Validation Requirement:**
Validation tools MUST be used after plot data preparation tool execution. Specific validation tools determined by rq_tools based on plot data format requirements (tools.validation.validate_plot_data_completeness to ensure all tertiles x congruence x tests present).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_age_effects_plot_data.csv: 36 rows x 9 columns (age_tertile: object, congruence: object, test: object, TSVR_hours: float64, mean_theta_observed: float64, mean_theta_predicted: float64, CI_lower: float64, CI_upper: float64, N: int64)

*Value Ranges:*
- TSVR_hours in [0, 200] hours (encoding to 1 week)
- mean_theta_observed in [-4, 4] (observed theta means)
- mean_theta_predicted in [-4, 4] (model predictions)
- CI_lower in [-4, 4], CI_upper in [-4, 4]
- N in [25, 50] (cell sizes, approximately 100 participants / 3 tertiles / 4 tests / 3 congruence = ~2-3 observations per cell after accounting for long format structure, but validation should be flexible)

*Data Quality:*
- Exactly 36 rows (complete factorial design: 3 age tertiles x 3 congruence x 4 tests)
- No NaN values in any column
- age_tertile contains only {Young, Middle, Older}
- congruence contains only {Common, Congruent, Incongruent}
- test contains only {T1, T2, T3, T4}
- CI_upper > CI_lower for all rows (valid confidence intervals)
- All 36 combinations present (no missing cells in factorial design)

*Log Validation:*
- Required pattern: "Created age tertiles: Young (N=[X]), Middle (N=[Y]), Older (N=[Z])"
- Required pattern: "Computed marginal means: 36 cells (3 tertiles x 3 congruence x 4 tests)"
- Required pattern: "VALIDATION - PASS: Plot data complete (all tertiles x congruence x tests present)"
- Forbidden patterns: "ERROR", "Missing combination", "NaN in plot data", "CI_lower >= CI_upper"
- Acceptable warnings: "Unequal tertile sizes" (if natural tertile boundaries don't split exactly 33/33/34)

**Expected Behavior on Validation Failure:**
- If < 36 rows: QUIT with "Plot data error: Expected 36 rows (3 tertiles x 3 congruence x 4 tests), found [actual]"
- If NaN in confidence intervals: QUIT with "Prediction error: NaN in confidence intervals for [cells]"
- If missing factorial combination: QUIT with "Data completeness error: Missing combination [tertile-congruence-test]"
- Log failure to logs/step05_prepare_plot_data.log
- g_debug invoked

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs - intermediate and final)
- data/step00_theta_wide.csv (from Step 0: validated theta scores from RQ 5.4.1)
- data/step00_tsvr_mapping.csv (from Step 0: validated TSVR from RQ 5.4.1)
- data/step00_age_data.csv (from Step 0: extracted Age from master data)
- data/step01_lmm_input.csv (from Step 1: long-format LMM input with Age_c, time transformations)
- data/step02_lmm_model.pkl (from Step 2: fitted LMM object)
- data/step02_lmm_model_summary.txt (from Step 2: model summary with convergence status)
- data/step02_fixed_effects.csv (from Step 2: all 18 fixed effects terms)
- data/step03_interaction_terms.csv (from Step 3: 4 three-way interaction terms with dual p-values)
- data/step04_age_effects_by_congruence.csv (from Step 4: marginal age slopes at Day 3)
- data/step04_tukey_contrasts.csv (from Step 4: Tukey HSD post-hoc with dual p-values)
- data/step05_age_effects_plot_data.csv (from Step 5: plot source CSV for age tertiles visualization)

### Logs (ONLY execution logs - .log files capturing stdout/stderr)
- logs/step00_load_dependencies.log
- logs/step01_prepare_lmm_input.log
- logs/step02_fit_lmm.log
- logs/step03_extract_interactions.log
- logs/step04_compute_age_effects.log
- logs/step05_prepare_plot_data.log

### Plots (EMPTY until rq_plots runs)
- plots/age_effects_by_congruence.png (created by rq_plots, NOT analysis steps)

### Results (EMPTY until rq_results runs)
- results/summary.md (created by rq_results, NOT analysis steps)

---

## Expected Data Formats

### Step 0 -> Step 1 Transformation

**Input (Wide Format - from RQ 5.4.1):**
```
composite_ID, theta_common, theta_congruent, theta_incongruent, se_common, se_congruent, se_incongruent
P001_T1,      -0.23,        0.15,            -0.48,             0.18,      0.19,         0.21
P001_T2,      -0.15,        0.22,            -0.35,             0.17,      0.18,         0.20
...
(400 rows total)
```

**Output (Long Format - after Step 1):**
```
UID,  composite_ID, test, congruence,   theta, se_theta, Age, Age_c, TSVR_hours, log_TSVR
P001, P001_T1,      T1,   Common,       -0.23, 0.18,     45,  0.2,   0.0,        0.0
P001, P001_T1,      T1,   Congruent,    0.15,  0.19,     45,  0.2,   0.0,        0.0
P001, P001_T1,      T1,   Incongruent,  -0.48, 0.21,     45,  0.2,   0.0,        0.0
P001, P001_T2,      T2,   Common,       -0.15, 0.17,     45,  0.2,   24.3,       3.22
P001, P001_T2,      T2,   Congruent,    0.22,  0.18,     45,  0.2,   24.3,       3.22
P001, P001_T2,      T2,   Incongruent,  -0.35, 0.20,     45,  0.2,   24.3,       3.22
...
(1200 rows total: 400 composite_IDs x 3 congruence levels)
```

**Transformation Logic:**
- Each wide-format row becomes 3 long-format rows (one per congruence level)
- composite_ID, Age, TSVR_hours, test replicated across congruence levels
- theta column contains theta_common for Common rows, theta_congruent for Congruent rows, theta_incongruent for Incongruent rows
- Age_c = Age - mean(Age) computed once across all participants
- log_TSVR = log(TSVR_hours + 1) computed for each row

### Column Naming Conventions (from names.md)

**Core Identifiers:**
- `UID`: Participant unique identifier (format: P### with leading zeros)
- `composite_ID`: Primary key combining UID and test (format: UID_test)
- `test`: Test session identifier (values: T1, T2, T3, T4)

**Time Variables (Decision D070):**
- `TSVR_hours`: Actual hours since VR encoding (linear time variable)
- `log_TSVR`: Logarithmic transformation of TSVR_hours (+ 1 to handle 0)

**IRT Outputs:**
- `theta_<dimension>`: IRT ability estimate (e.g., theta_common, theta_congruent, theta_incongruent)
- `se_<dimension>`: Standard error of theta estimate (e.g., se_common, se_congruent, se_incongruent)
- `theta`: Generic theta column in long format (contains values from theta_common/theta_congruent/theta_incongruent)
- `se_theta`: Generic SE column in long format

**Grouping Variables:**
- `congruence`: Schema congruence factor (values: Common, Congruent, Incongruent)
- `age_tertile`: Age grouping for plotting (values: Young, Middle, Older)

**Age Variables:**
- `Age`: Original age in years (continuous, range: 20-70)
- `Age_c`: Grand-mean centered age (continuous, mean approximately 0)

**Plotting Variables:**
- `CI_lower`: Lower bound of 95% confidence interval
- `CI_upper`: Upper bound of 95% confidence interval

---

## Cross-RQ Dependencies

**This RQ depends on:** RQ 5.4.1 (Schema-Specific Trajectories)

**Required Files from RQ 5.4.1:**
- results/ch5/5.4.1/data/step03_theta_scores.csv (IRT ability estimates: theta_common, theta_congruent, theta_incongruent in wide format)
- results/ch5/5.4.1/data/step00_tsvr_mapping.csv (TSVR time variable: actual hours since encoding)

**Status Check:**
Step 0 of this RQ verifies that RQ 5.4.1 has completed Step 3 successfully. If required files missing, QUIT with "EXPECTATIONS ERROR: RQ 5.4.1 must complete Step 3 before this RQ (theta scores dependency)".

**Data Integration:**
- Step 0: Load theta scores and TSVR from RQ 5.4.1, validate structure
- Step 1: Merge theta with Age from master data, reshape wide to long
- Expected: All 400 composite_IDs from RQ 5.4.1 matched successfully (no data loss)

**Execution Order Constraint:**
1. RQ 5.4.1 must execute first and complete Step 3 (IRT calibration for congruence factors)
2. This RQ (5.4.3) executes second using RQ 5.4.1 outputs as DERIVED data source

**Rationale:**
This RQ does not re-calibrate IRT models. It uses theta scores from RQ 5.4.1 as fixed ability estimates and examines how age moderates forgetting trajectories across congruence levels. Dependency ensures theta scores are computed once (RQ 5.4.1) and reused for multiple analyses (RQ 5.4.2 trajectories, RQ 5.4.3 age interactions, potentially RQ 5.4.4+ if applicable).

---

## Validation Requirements

**CRITICAL MANDATE:**

Every analysis step in this plan MUST use validation tools after analysis tool execution.

This is not optional. This is the core architectural principle preventing cascading failures observed in v3.0 (where analysis errors propagated undetected through 5+ downstream steps before discovery).

**Exact Specification Requirement:**

> "Validation tools MUST be used after analysis tool execution"

**Implementation:**
- rq_tools (Step 11 workflow) will read tools_inventory.md validation tools section
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

#### Step 0: Load and Validate Dependency Files

**Analysis Tool:** (determined by rq_tools - likely pd.read_csv with file existence checks)
**Validation Tool:** (determined by rq_tools - likely tools.validation.check_file_exists, validate_data_columns, validate_numeric_range)

**What Validation Checks:**
- All 3 dependency files exist (RQ 5.4.1 theta, RQ 5.4.1 TSVR, master Age)
- Expected column counts and names match specifications
- Expected row counts (400 for theta/TSVR, >=100 for Age)
- No NaN in critical columns (theta, se, TSVR_hours, Age)
- Value ranges scientifically reasonable (theta in [-4,4], TSVR in [0,200], Age in [20,70])
- All composite_IDs from theta file have matching TSVR entries
- All UIDs parsed from composite_IDs have matching Age entries

**Expected Behavior on Validation Failure:**
- If dependency file missing: QUIT with "EXPECTATIONS ERROR: RQ 5.4.1 must complete [step] before this RQ"
- If column missing: QUIT with "Data structure error: [file] missing required column [name]"
- If row count mismatch: QUIT with "Data size error: Expected [N] rows, found [actual]"
- Log failure to logs/step00_load_dependencies.log
- g_debug invoked to diagnose root cause

---

#### Step 1: Merge Data and Prepare LMM Input

**Analysis Tool:** (determined by rq_tools - likely pd.merge, pd.melt for reshaping, grand-mean centering)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_standardization for Age_c centering, validate_dataframe_structure for reshape)

**What Validation Checks:**
- Merge operations successful (no NaN introduced, all rows matched)
- Reshape produces exactly 1200 rows (400 wide x 3 congruence levels)
- Age_c mean within ±0.1 of 0 (grand-mean centering successful)
- congruence column contains only {Common, Congruent, Incongruent}
- test column contains only {T1, T2, T3, T4}
- Each UID appears exactly 12 times (4 tests x 3 congruence)
- No NaN values in any column
- Time transformations valid (log_TSVR computed correctly)

**Expected Behavior on Validation Failure:**
- If merge introduces NaN: QUIT with "Merge error: NaN introduced in [columns]"
- If reshape row count wrong: QUIT with "Reshape error: Expected 1200 rows, found [actual]"
- If Age_c not centered: QUIT with "Centering error: Age_c mean = [value], expected approximately 0"
- Log failure to logs/step01_prepare_lmm_input.log
- g_debug invoked

---

#### Step 2: Fit LMM with 3-Way Interaction

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.fit_lmm_trajectory_tsvr or statsmodels MixedLM)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_lmm_assumptions_comprehensive)

**What Validation Checks:**
- Model convergence (model.converged = True)
- All 18 fixed effects terms estimated (no missing coefficients)
- No NaN in coefficient estimates, SEs, p-values
- Standard errors all positive (SE > 0)
- Residuals approximately normal (Q-Q plot, Shapiro-Wilk or KS test)
- Homoscedasticity (residuals vs fitted plot, no funnel pattern)
- Independence (ACF plot shows no significant autocorrelation)
- Random effects variances positive (no boundary issues)
- Model fit indices reasonable (AIC, BIC, log-likelihood finite)

**Expected Behavior on Validation Failure:**
- If convergence fails: Try contingency plan (alternative optimizers, simplified random structure)
- If convergence still fails after contingency: QUIT with "LMM fitting error: Model did not converge"
- If NaN estimates: QUIT with "Estimation error: NaN in model coefficients"
- If assumptions violated: Log warnings, recommend robust SEs, but proceed (not fatal)
- Log failure to logs/step02_fit_lmm.log
- g_debug invoked for convergence failures

---

#### Step 3: Extract 3-Way Interaction Terms with Dual P-Values

**Analysis Tool:** (determined by rq_tools - likely custom extraction from fixed effects table)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_hypothesis_test_dual_pvalues)

**What Validation Checks:**
- Exactly 4 interaction terms extracted (Age_c:Congruent:TSVR_hours, Age_c:Congruent:log_TSVR, Age_c:Incongruent:TSVR_hours, Age_c:Incongruent:log_TSVR)
- BOTH p_uncorrected AND p_bonferroni columns present (Decision D068 requirement)
- Bonferroni correction applied correctly (p_bonferroni = min(p_uncorrected * 2, 1.0))
- significant_bonferroni threshold applied correctly (p_bonferroni < 0.025)
- No NaN in any column

**Expected Behavior on Validation Failure:**
- If < 4 terms: QUIT with "Extraction error: Expected 4 terms, found [actual]"
- If dual p-values missing: QUIT with "Decision D068 violation: Must report p_uncorrected and p_bonferroni"
- If correction wrong: QUIT with "Bonferroni error: p_bonferroni != p_uncorrected * 2"
- Log failure to logs/step03_extract_interactions.log
- g_debug invoked

---

#### Step 4: Compute Age Effects with Tukey HSD

**Analysis Tool:** (determined by rq_tools - likely marginal effects computation + Tukey contrasts)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_contrasts_dual_pvalues)

**What Validation Checks:**
- 3 age effects computed (one per congruence level)
- 3 Tukey contrasts computed (all pairwise comparisons)
- BOTH p_uncorrected AND p_tukey columns present in contrasts (Decision D068 requirement)
- Delta method SEs valid (all positive, no NaN)
- Confidence intervals valid (CI_upper > CI_lower)
- All required contrasts present (Congruent-Common, Incongruent-Common, Incongruent-Congruent)
- No NaN in any column

**Expected Behavior on Validation Failure:**
- If marginal slopes contain NaN: QUIT with "Delta method error: NaN in age slopes"
- If < 3 contrasts: QUIT with "Tukey error: Expected 3 contrasts, found [actual]"
- If dual p-values missing: QUIT with "Decision D068 violation: Must report p_uncorrected and p_tukey"
- Log failure to logs/step04_compute_age_effects.log
- g_debug invoked

---

#### Step 5: Prepare Plot Data

**Analysis Tool:** (determined by rq_tools - likely tertile creation + marginal means aggregation)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_plot_data_completeness)

**What Validation Checks:**
- Exactly 36 rows (3 age tertiles x 3 congruence x 4 tests)
- All factorial combinations present (no missing cells)
- age_tertile contains only {Young, Middle, Older}
- congruence contains only {Common, Congruent, Incongruent}
- test contains only {T1, T2, T3, T4}
- CI_upper > CI_lower for all rows
- No NaN in any column

**Expected Behavior on Validation Failure:**
- If < 36 rows: QUIT with "Plot data error: Expected 36 rows, found [actual]"
- If missing combination: QUIT with "Completeness error: Missing [tertile-congruence-test]"
- If NaN in CI: QUIT with "Prediction error: NaN in confidence intervals"
- Log failure to logs/step05_prepare_plot_data.log
- g_debug invoked

---

## Summary

**Total Steps:** 6 (Step 0: dependency validation + Steps 1-5: analysis)
**Estimated Runtime:** Medium (~15-20 minutes total)
**Cross-RQ Dependencies:** RQ 5.4.1 (theta scores, TSVR mapping)
**Primary Outputs:**
- LMM model with 3-way Age x Congruence x Time interaction (data/step02_lmm_model.pkl)
- Three-way interaction terms with dual p-values (data/step03_interaction_terms.csv)
- Congruence-specific age effects at Day 3 with Tukey HSD post-hoc (data/step04_age_effects_by_congruence.csv, data/step04_tukey_contrasts.csv)
- Age tertile plot data for visualization (data/step05_age_effects_plot_data.csv)

**Validation Coverage:** 100% (all 6 steps have validation requirements with 4-layer substance criteria)

**Decision Compliance:**
- D068: Dual p-value reporting (uncorrected + Bonferroni for 3-way interactions, uncorrected + Tukey for post-hoc contrasts)
- D070: TSVR as time variable (actual hours, not nominal days)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-02): Initial plan created by rq_planner agent
