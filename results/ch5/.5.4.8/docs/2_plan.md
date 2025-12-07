# Analysis Plan: RQ 5.4.8 - Congruence x Item Difficulty Interaction

**Research Question:** 5.4.8
**Created:** 2025-12-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines whether the relationship between item difficulty and forgetting rate varies across three schema congruence levels (Common, Congruent, Incongruent). Unlike prior RQs that examined participant-level theta scores, this analysis operates at the **item-level** using ~24,000-32,000 binary response observations (100 participants x 4 tests x 60-80 items post-purification).

**Key Analysis Features:**
- **No IRT calibration** (uses DERIVED item difficulty parameters from RQ 5.4.1 Pass 2)
- **Cross-classified GLMM** with binomial family and logit link (handles binary responses appropriately)
- **3-way interaction test:** Time x Difficulty_c x Congruence at Bonferroni alpha = 0.0033
- **Crossed random effects:** Participants (UID) and Items (ItemID) both as random factors
- **Exploratory analysis:** No directional prediction, tests which theoretical pattern emerges

**Pipeline:** DERIVED data merge -> GLMM fitting -> Interaction extraction -> Plot preparation

**Steps:** 6 total analysis steps (Step 0 through Step 5)

**Estimated Runtime:** Medium (~30-60 minutes total, dominated by Step 3 GLMM fitting with crossed random effects)

**Key Decisions Applied:**
- **Decision D068:** Dual p-value reporting (uncorrected + Bonferroni for 3-way interaction)
- **Decision D070:** TSVR_hours as time variable (actual hours since encoding)
- **Decision D069:** NOT APPLICABLE (no theta-scale trajectories; GLMM produces probability-scale predictions directly)

**Critical Technical Note:**
This RQ uses **GLMM (Generalized Linear Mixed Model)** with binomial family, NOT standard LMM, because item-level responses are binary (0/1). Standard LMM assumes normally distributed residuals, which is violated with binary data. GLMM with logit link is the appropriate method. Coefficients are on log-odds scale; exponentiate for odds ratios.

---

## Analysis Plan

This RQ requires 6 steps:

### Step 0: Extract Item Parameters from RQ 5.4.1

**Dependencies:** None (first step, but requires RQ 5.4.1 completion)

**Complexity:** Low (<5 minutes, data loading only)

**Purpose:** Load IRT item difficulty parameters from RQ 5.4.1 Pass 2 calibration to use as predictor variable in GLMM.

**Input:**

**File 1:** results/ch5/5.4.1/data/step03_item_parameters.csv
**Source:** RQ 5.4.1 Pass 2 IRT calibration (post-purification)
**Format:** CSV with columns:
  - `item_name` (string, format: VR-{paradigm}-{test}-{domain}-i{number}, e.g., VR-IFR-A01-N-i1)
  - `dimension` (string, values: {Common, Congruent, Incongruent})
  - `a` (float, discrimination parameter, range: [0.4, 10.0] per D039 purification)
  - `b` (float, difficulty parameter, range: [-3.0, 3.0] per D039 purification)
**Expected Rows:** 60-80 items (post-purification from RQ 5.4.1)

**File 2:** results/ch5/5.4.1/data/step02_purified_items.csv
**Source:** RQ 5.4.1 purification step (items retained after quality filtering)
**Format:** CSV with column:
  - `item_name` (string, list of retained items)
**Expected Rows:** 60-80 items
**Purpose:** Validation - cross-check that item_parameters.csv contains only purified items

**Circuit Breaker Check:**
If results/ch5/5.4.1/data/step03_item_parameters.csv does NOT exist -> EXPECTATIONS ERROR "RQ 5.4.1 Step 3 must complete before RQ 5.4.8 can run"

**Processing:**
- Load item_parameters.csv
- Validate: All items have valid a (>= 0.4) and b (|b| <= 3.0) per D039 thresholds
- Validate: Item count in expected range (60-80 items)
- Extract columns: item_name, dimension (rename to Congruence for clarity), b (rename to Difficulty)
- No filtering (use all purified items from RQ 5.4.1)

**Output:**

**File:** data/step00_item_difficulty_by_congruence.csv
**Format:** CSV with columns:
  - `ItemID` (string, renamed from item_name for consistency)
  - `Congruence` (string, values: {Common, Congruent, Incongruent}, renamed from dimension)
  - `Difficulty` (float, IRT difficulty parameter b, range: [-3.0, 3.0])
**Expected Rows:** 60-80 items (matches RQ 5.4.1 purified item count)

**Validation Requirement:**

Validation tools MUST be used after data extraction execution. Specific validation tools will be determined by rq_tools based on data format requirements (likely validate_dataframe_structure, validate_numeric_range).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_item_difficulty_by_congruence.csv exists (exact path)
- Expected rows: 60-80 (matches RQ 5.4.1 purification output)
- Expected columns: 3 (ItemID: object, Congruence: object, Difficulty: float64)
- No index column written to CSV

*Value Ranges:*
- Difficulty in [-3.0, 3.0] (D039 purification thresholds, all items passed)
- Congruence in {Common, Congruent, Incongruent} (categorical, no typos)

*Data Quality:*
- No NaN values tolerated (all items have valid difficulty estimates)
- Expected N: Exactly 60-80 items (if <60 or >80, RQ 5.4.1 purification issue)
- No duplicate ItemID values (each item appears once)
- Congruence distribution: ~20-27 items per category (balanced across 3 levels)

*Log Validation:*
- Required pattern: "Loaded {N} items from RQ 5.4.1" where N in [60, 80]
- Required pattern: "All items have valid Difficulty in [-3.0, 3.0]"
- Forbidden patterns: "ERROR", "NaN detected", "Difficulty out of range"
- Acceptable warnings: None expected for this step

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 60-80 items, found 45")
- Log failure to logs/step00_extract_item_difficulty.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose (common causes: RQ 5.4.1 incomplete, file path wrong)

---

### Step 1: Extract Item-Level Response Data and Merge TSVR

**Dependencies:** Step 0 (requires item list to filter raw responses)

**Complexity:** Low (~5 minutes, data extraction + merge)

**Purpose:** Extract raw binary responses for purified items from dfData.csv and merge with TSVR time mapping from RQ 5.4.1.

**Input:**

**File 1:** data/cache/dfData.csv (project-level RAW data source)
**Format:** Long format with columns:
  - `UID` (string, participant identifier, format: P### with leading zeros)
  - `test` (string, test session, values: {T1, T2, T3, T4})
  - `item_name` (string, VR item identifier)
  - `TQ` (int, ternary quality score: 0=incorrect, 1=low-quality correct, 2=high-quality correct)
**Filter:** Retain only items present in step00_item_difficulty_by_congruence.csv (purified item set)
**Expected Rows BEFORE filtering:** ~1,800,000 (100 participants x 4 tests x all VR items)
**Expected Rows AFTER filtering:** ~24,000-32,000 (100 participants x 4 tests x 60-80 purified items)

**File 2:** results/ch5/5.4.1/data/step00_tsvr_mapping.csv
**Source:** RQ 5.4.1 extraction step (TSVR time variable per participant-test)
**Format:** CSV with columns:
  - `UID` (string, participant identifier)
  - `test` (string, test session)
  - `TSVR_hours` (float, actual time since VR encoding in hours, Decision D070)
**Expected Rows:** 400 (100 participants x 4 tests)

**Circuit Breaker Check:**
If results/ch5/5.4.1/data/step00_tsvr_mapping.csv does NOT exist -> EXPECTATIONS ERROR "RQ 5.4.1 Step 0 must complete before RQ 5.4.8 can run"

**Processing:**
- Load dfData.csv (full dataset)
- Load step00_item_difficulty_by_congruence.csv (purified item list from Step 0)
- Filter dfData to retain only items in purified list
- Dichotomize responses: TQ < 1 -> 0 (incorrect), TQ >= 1 -> 1 (correct) [inherited from RQ 5.4.1 logic]
- Load step00_tsvr_mapping.csv
- Merge TSVR_hours onto filtered response data (left join on UID + test)
- Validate: All responses have matched TSVR_hours (no NaN after merge)
- Output columns: UID, test, ItemID (renamed from item_name), Response (binary 0/1), TSVR_hours

**Output:**

**File:** data/step01_response_level_data.csv
**Format:** CSV, long format (one row per response observation)
**Columns:**
  - `UID` (string, participant identifier)
  - `test` (string, test session: T1, T2, T3, T4)
  - `ItemID` (string, item identifier, matches Step 0 ItemID)
  - `Response` (int, binary: 0=incorrect, 1=correct)
  - `TSVR_hours` (float, actual time since encoding, Decision D070)
**Expected Rows:** ~24,000-32,000 (100 participants x 4 tests x 60-80 items)

**Validation Requirement:**

Validation tools MUST be used after data extraction + merge execution. Specific validation tools determined by rq_tools (likely validate_dataframe_structure, validate_numeric_range, check_missing_data).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_response_level_data.csv exists (exact path)
- Expected rows: 24,000-32,000 (100 participants x 4 tests x 60-80 items)
- Expected columns: 5 (UID: object, test: object, ItemID: object, Response: int64, TSVR_hours: float64)
- No index column written

*Value Ranges:*
- Response in {0, 1} (binary, no other values)
- TSVR_hours in [0, 168] hours (0=encoding Day 0, 168=1 week for Day 6)
- test in {T1, T2, T3, T4} (categorical, no typos)

*Data Quality:*
- No NaN values tolerated (all responses have matched TSVR_hours)
- Expected N: 24,000-32,000 rows (if outside range, item count or participant count issue)
- All 100 participants present (no data loss)
- All 4 test sessions per participant (complete data)
- Item distribution: Each item appears ~400 times (100 participants x 4 tests)

*Log Validation:*
- Required pattern: "Filtered to {N} purified items" where N in [60, 80]
- Required pattern: "Extracted {M} response observations" where M in [24000, 32000]
- Required pattern: "All responses matched with TSVR_hours (no missing)"
- Forbidden patterns: "ERROR", "NaN in TSVR_hours", "Response outside {0,1}"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Found {X} responses with missing TSVR_hours")
- Log failure to logs/step01_extract_responses.log
- Quit immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose (common causes: TSVR mapping incomplete, merge key mismatch)

---

### Step 2: Merge Item Difficulty and Center Difficulty Variable

**Dependencies:** Steps 0, 1 (requires item difficulty and response data)

**Complexity:** Low (<5 minutes, merge + centering)

**Purpose:** Add item difficulty and congruence labels to response-level data, then grand-mean center difficulty for interaction interpretation.

**Input:**

**File 1:** data/step01_response_level_data.csv (from Step 1)
**Format:** Long format with ~24,000-32,000 rows
**Columns:** UID, test, ItemID, Response, TSVR_hours

**File 2:** data/step00_item_difficulty_by_congruence.csv (from Step 0)
**Format:** Item-level metadata with 60-80 rows
**Columns:** ItemID, Congruence, Difficulty

**Processing:**
- Load response data (Step 1 output)
- Load item difficulty data (Step 0 output)
- Merge item difficulty + congruence onto response data (left join on ItemID)
- Validate: All responses have matched item difficulty (no NaN after merge)
- Compute grand mean of Difficulty across all items
- Center difficulty: Difficulty_c = Difficulty - mean(Difficulty)
- Validate: mean(Difficulty_c) approximately 0 (within +/- 0.01)
- Output: response data with added columns Difficulty, Difficulty_c, Congruence

**Output:**

**File:** data/step02_merged_data.csv
**Format:** CSV, long format (one row per response observation)
**Columns:**
  - `UID` (string, participant identifier)
  - `test` (string, test session)
  - `ItemID` (string, item identifier)
  - `Response` (int, binary: 0=incorrect, 1=correct)
  - `TSVR_hours` (float, time variable per D070)
  - `Difficulty` (float, raw IRT difficulty parameter b)
  - `Difficulty_c` (float, grand-mean centered difficulty for interaction interpretation)
  - `Congruence` (string, categorical: Common, Congruent, Incongruent)
**Expected Rows:** ~24,000-32,000 (same as Step 1 input)

**Validation Requirement:**

Validation tools MUST be used after data merge + centering execution. Specific validation tools determined by rq_tools (likely validate_dataframe_structure, validate_standardization, check_missing_data).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_merged_data.csv exists (exact path)
- Expected rows: 24,000-32,000 (matches Step 1 input exactly)
- Expected columns: 8 (UID, test, ItemID, Response, TSVR_hours, Difficulty, Difficulty_c, Congruence)
- All columns have correct data types

*Value Ranges:*
- Difficulty in [-3.0, 3.0] (inherited from Step 0, D039 purification bounds)
- Difficulty_c approximately centered: mean in [-0.01, 0.01], SD approximately equal to SD(Difficulty)
- Congruence in {Common, Congruent, Incongruent} (categorical)
- Response in {0, 1}, TSVR_hours in [0, 168] (inherited from Step 1)

*Data Quality:*
- No NaN values tolerated (all responses have matched item difficulty and congruence)
- Row count matches Step 1 exactly (no data loss during merge)
- Centering validation: mean(Difficulty_c) within +/- 0.01 of zero
- Congruence distribution: ~1/3 responses per category (balanced across Common/Congruent/Incongruent)

*Log Validation:*
- Required pattern: "Merged item difficulty for {N} items" where N in [60, 80]
- Required pattern: "Centered difficulty: mean = {M}" where |M| < 0.01
- Required pattern: "All responses matched with item difficulty (no missing)"
- Forbidden patterns: "ERROR", "NaN in Difficulty", "Centering failed"
- Acceptable warnings: "Mean Difficulty_c = 0.008" (slightly off zero acceptable)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Mean Difficulty_c = 0.15, centering failed")
- Log failure to logs/step02_merge_difficulty.log
- Quit immediately (do NOT proceed to Step 3)
- g_debug invoked to diagnose (common causes: merge key mismatch, centering arithmetic error)

---

### Step 3: Fit Cross-Classified GLMM with 3-Way Interaction

**Dependencies:** Step 2 (requires merged response data with difficulty and congruence)

**Complexity:** High (30-60 minutes, cross-classified GLMM with binomial family is computationally intensive)

**Purpose:** Fit Generalized Linear Mixed Model (GLMM) with binomial family and logit link to test 3-way Time x Difficulty_c x Congruence interaction on binary response data.

**Critical Technical Note:**
Item-level responses are binary (0/1). Standard LMM assumes normally distributed residuals, which is violated with binary data. GLMM with binomial family and logit link is the appropriate method for binary outcomes.

**Input:**

**File:** data/step02_merged_data.csv (from Step 2)
**Format:** Long format with ~24,000-32,000 rows
**Columns:** UID, test, ItemID, Response, TSVR_hours, Difficulty, Difficulty_c, Congruence
**Key Variables:**
  - DV: Response (binary: 0/1)
  - Time: TSVR_hours (continuous, Decision D070)
  - Item-level predictor: Difficulty_c (continuous, grand-mean centered)
  - Group factor: Congruence (categorical: Common=reference, Congruent, Incongruent)

**Processing:**

**Model Formula:**
```
Response ~ TSVR_hours * Difficulty_c * Congruence + (TSVR_hours | UID) + (1 | ItemID)
Family: binomial (link = "logit")
```

**Interpretation:**
- Fixed effects on log-odds scale
- Exponentiate coefficients for odds ratios: OR = exp(beta)
- 3-way interaction term: TSVR_hours:Difficulty_c:Congruent and TSVR_hours:Difficulty_c:Incongruent (test whether difficulty effect on forgetting differs by congruence level)

**Random Effects:**
- By-participant random intercepts + random slopes for TSVR_hours: (TSVR_hours | UID)
- By-item random intercepts only: (1 | ItemID) [cannot have random slope for Difficulty because Difficulty is item-level predictor]
- Crossed structure: participants and items are non-nested (each participant responds to all items)

**Implementation:**
- Use pymer4.Lmer() with family='binomial' parameter, OR
- Direct R lme4::glmer() call via rpy2 if pymer4 unavailable
- Optimizer: bobyqa (lme4 default for GLMM)
- Convergence tolerance: default lme4 settings

**Convergence Contingency Plan (if full model fails to converge):**
1. Try alternative optimizers: nloptwrap, nlminbwrap
2. Simplify random effects: Remove random slopes, use (1 | UID) + (1 | ItemID)
3. If still fails: Fit participant-aggregated model (mean accuracy per UID x test x Congruence, loses item-level variance but tests interaction)
4. Document which specification achieved convergence in model summary

**Output:**

**File 1:** data/step03_glmm_model_summary.txt
**Format:** Plain text summary of fitted model
**Contents:**
  - Model formula
  - Family and link function
  - Fixed effects table (coefficient, SE, z-value, p-value on log-odds scale)
  - Odds ratios table (exponentiated coefficients with 95% CIs)
  - Random effects variance components (UID intercept, UID slope, ItemID intercept)
  - Model fit statistics (AIC, BIC, log-likelihood, deviance)
  - Convergence diagnostics (converged: TRUE/FALSE, singularity warnings if any)
  - Sample size (N observations, N participants, N items)

**File 2:** data/step03_fixed_effects.csv
**Format:** CSV, one row per fixed effect term
**Columns:**
  - `term` (string, predictor name)
  - `estimate` (float, coefficient on log-odds scale)
  - `SE` (float, standard error)
  - `z` (float, z-statistic)
  - `p_uncorrected` (float, uncorrected p-value)
  - `p_bonferroni` (float, Bonferroni-corrected p-value, alpha = 0.05 / 15 = 0.0033, Decision D068)
  - `OR` (float, odds ratio = exp(estimate))
  - `OR_CI_lower` (float, lower bound of 95% CI for odds ratio)
  - `OR_CI_upper` (float, upper bound of 95% CI for odds ratio)
**Expected Rows:** ~15 (intercept + 3 main effects + 3 two-way interactions + 2 three-way interactions + Congruence dummy codes)

**File 3:** data/step03_random_effects.csv
**Format:** CSV, one row per random effect component
**Columns:**
  - `component` (string, e.g., "UID_intercept", "UID_slope_TSVR", "ItemID_intercept")
  - `variance` (float, variance estimate, must be > 0)
  - `SD` (float, standard deviation = sqrt(variance))
**Expected Rows:** 3 (UID intercept, UID slope for TSVR_hours, ItemID intercept) if full model converges; 2 if simplified to intercepts-only

**Validation Requirement:**

Validation tools MUST be used after GLMM fitting execution. Specific validation tools determined by rq_tools (likely validate_model_convergence, validate_variance_positivity, validate_lmm_assumptions_comprehensive adapted for GLMM, validate_hypothesis_test_dual_pvalues per D068).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_glmm_model_summary.txt exists (exact path)
- data/step03_fixed_effects.csv exists (exact path)
- data/step03_random_effects.csv exists (exact path)
- Fixed effects: ~15 rows (depends on Congruence coding scheme)
- Random effects: 2-3 rows (depends on convergence - full model has 3, simplified has 2)

*Value Ranges:*
- Fixed effect estimates (log-odds): typically in [-5, 5] (extreme values suggest convergence issues)
- Odds ratios (OR): > 0 always (OR = exp(estimate), cannot be negative)
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1]
- Random effect variances: > 0 (negative variance impossible, zero suggests singularity)

*Data Quality:*
- No NaN values in fixed effects table (all terms must have valid estimates)
- No infinite values in odds ratios (suggests extreme coefficient estimates)
- Convergence flag: TRUE (model must converge for valid inference)
- Singularity warnings: Document if present (suggests overfitted random effects structure)
- Variance components all positive (variance = 0 indicates convergence issue)

*Log Validation:*
- Required pattern: "Model converged: TRUE" OR "Simplified model converged: TRUE" (if contingency plan used)
- Required pattern: "VALIDATION - PASS: Convergence" (from validation tool)
- Required pattern: "VALIDATION - PASS: Variance positivity" (all variances > 0)
- Forbidden patterns: "ERROR", "Convergence failure", "NaN in fixed effects"
- Acceptable warnings: "Singularity warning" (document, but model may still be interpretable)

*GLMM-Specific Validation (Document in Log):*
- Overdispersion check: Residual deviance / residual df should be approximately 1 (if > 1.5, overdispersion present)
- Link function adequacy: Partial residual plots suggest logit link appropriate (or document if probit sensitivity analysis needed)
- Random effects normality: Q-Q plot of random effects approximately normal (inference robust to mild violations)

**Expected Behavior on Validation Failure:**
- If convergence fails after trying contingency plan -> Raise error "GLMM convergence failed with all optimizers and random structures"
- If variance components <= 0 -> Raise error "Random effects variance non-positive, model singularity"
- If NaN in fixed effects -> Raise error "Fixed effects contain NaN, model fitting failed"
- Log all failures to logs/step03_fit_glmm.log
- Quit immediately (do NOT proceed to Step 4)
- g_debug invoked to diagnose (common causes: perfect separation, insufficient data, overfitted random effects)

**Expected Behavior on Validation Success:**
- Document which model specification converged (full vs simplified random effects)
- Document overdispersion ratio (if > 1.5, note as limitation)
- Proceed to Step 4

---

### Step 4: Extract 3-Way Interaction and Congruence-Stratified Difficulty Effects

**Dependencies:** Step 3 (requires fitted GLMM with convergence)

**Complexity:** Low (~5 minutes, coefficient extraction + stratified re-fitting)

**Purpose:** Extract 3-way interaction term with dual p-values (Decision D068), then fit congruence-stratified models to extract Time x Difficulty_c interaction coefficient for each congruence level separately.

**Input:**

**File 1:** data/step03_fixed_effects.csv (from Step 3)
**Format:** CSV with fixed effects table
**Filter:** Extract row where term contains "TSVR_hours:Difficulty_c:Congruent" and "TSVR_hours:Difficulty_c:Incongruent" (3-way interaction terms)

**File 2:** data/step02_merged_data.csv (from Step 2, needed for congruence-stratified models)
**Format:** Long format response data
**Filter:** Split into 3 subsets by Congruence (Common, Congruent, Incongruent)

**Processing:**

**Part A: Extract 3-Way Interaction Term**
- Load step03_fixed_effects.csv
- Filter to 3-way interaction terms (TSVR_hours:Difficulty_c:Congruent, TSVR_hours:Difficulty_c:Incongruent)
- Verify dual p-values present: p_uncorrected and p_bonferroni columns exist (Decision D068 compliance)
- Extract: term, estimate, SE, z, p_uncorrected, p_bonferroni, OR, OR_CI_lower, OR_CI_upper
- Primary test: Is p_bonferroni < 0.0033? (Bonferroni alpha for 15 comparisons across workflow)

**Part B: Fit Congruence-Stratified Models**
For each congruence level (Common, Congruent, Incongruent):
  - Subset data to that congruence level only
  - Fit GLMM: Response ~ TSVR_hours * Difficulty_c + (TSVR_hours | UID) + (1 | ItemID), family = binomial
  - Extract Time x Difficulty_c interaction coefficient (TSVR_hours:Difficulty_c term)
  - Compute: estimate, SE, z, p-value, OR with 95% CI
  - Note: These p-values are NOT corrected (exploratory post-hoc, not primary hypothesis test)

**Output:**

**File 1:** data/step04_interaction_3way.csv
**Format:** CSV with 3-way interaction term(s)
**Columns:**
  - `term` (string, e.g., "TSVR_hours:Difficulty_c:Congruent", "TSVR_hours:Difficulty_c:Incongruent")
  - `estimate` (float, log-odds scale)
  - `SE` (float, standard error)
  - `z` (float, z-statistic)
  - `p_uncorrected` (float, uncorrected p-value)
  - `p_bonferroni` (float, Bonferroni-corrected p-value, alpha = 0.0033)
  - `OR` (float, odds ratio)
  - `OR_CI_lower` (float, 95% CI lower bound)
  - `OR_CI_upper` (float, 95% CI upper bound)
  - `significant_bonferroni` (bool, TRUE if p_bonferroni < 0.0033)
**Expected Rows:** 2 (one for Congruent contrast, one for Incongruent contrast, both relative to Common reference)

**File 2:** data/step04_congruence_stratified_slopes.csv
**Format:** CSV, one row per congruence level
**Columns:**
  - `Congruence` (string, values: Common, Congruent, Incongruent)
  - `interaction_estimate` (float, TSVR_hours:Difficulty_c coefficient on log-odds scale)
  - `SE` (float, standard error)
  - `z` (float, z-statistic)
  - `p_value` (float, uncorrected p-value, exploratory only)
  - `OR` (float, odds ratio for interaction)
  - `OR_CI_lower` (float, 95% CI lower bound)
  - `OR_CI_upper` (float, 95% CI upper bound)
**Expected Rows:** 3 (one per congruence level)
**Purpose:** Compare interaction magnitudes across congruence levels (exploratory post-hoc)

**Validation Requirement:**

Validation tools MUST be used after interaction extraction execution. Specific validation tools determined by rq_tools (likely validate_hypothesis_test_dual_pvalues for 3-way interaction per D068, validate_dataframe_structure for stratified slopes).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_interaction_3way.csv exists (exact path)
- data/step04_congruence_stratified_slopes.csv exists (exact path)
- Interaction 3-way: 2 rows (Congruent, Incongruent contrasts vs Common reference)
- Stratified slopes: 3 rows (one per congruence level)

*Value Ranges:*
- Estimates (log-odds): typically in [-2, 2] (extreme values suggest overfitting)
- Odds ratios: > 0 always
- p_uncorrected in [0, 1], p_bonferroni in [0, 1]
- SE > 0 (negative SE impossible)

*Data Quality:*
- No NaN values in 3-way interaction table (all terms must have valid estimates)
- Dual p-values present: p_uncorrected AND p_bonferroni columns exist (Decision D068 compliance)
- Bonferroni alpha correctly calculated: p_bonferroni threshold = 0.0033 (0.05 / 15)
- Stratified slopes: All 3 congruence levels represented (no missing categories)

*Log Validation:*
- Required pattern: "Extracted 3-way interaction terms: {N}" where N = 2
- Required pattern: "VALIDATION - PASS: Dual p-values present (D068 compliance)"
- Required pattern: "Fit {N} congruence-stratified models" where N = 3
- Forbidden patterns: "ERROR", "NaN in interaction term", "Missing p_bonferroni column"
- Acceptable warnings: "Congruence-stratified model for {X} has singularity warning" (document)

**Expected Behavior on Validation Failure:**
- If dual p-values missing -> Raise error "3-way interaction missing p_bonferroni (Decision D068 violation)"
- If stratified models fail to converge -> Document which level(s) failed, proceed with available results
- Log failure to logs/step04_extract_interaction.log
- Quit if 3-way interaction extraction fails (do NOT proceed to Step 5)
- g_debug invoked to diagnose

**Expected Behavior on Validation Success:**
- Report 3-way interaction significance: p_bonferroni < 0.0033? (YES/NO)
- Report stratified interaction magnitudes for interpretation
- Proceed to Step 5

---

### Step 5: Prepare Trajectory Plot Data (6 Lines: 2 Difficulty x 3 Congruence)

**Dependencies:** Steps 3, 4 (requires fitted GLMM model to generate predictions)

**Complexity:** Low (~5 minutes, prediction generation + aggregation)

**Purpose:** Generate predicted probabilities for 6 trajectories (Easy/Hard difficulty x Common/Congruent/Incongruent congruence) across 4 timepoints to visualize 3-way interaction.

**Input:**

**File 1:** data/step03_glmm_model_summary.txt (from Step 3, fitted model object path if saved)
**Note:** If model object not saved, re-fit GLMM using same formula from Step 3

**File 2:** data/step02_merged_data.csv (from Step 2, for computing difficulty SD and TSVR means)

**Processing:**

**Define Difficulty Levels:**
- Easy: Difficulty_c = -1 SD below mean (mean Difficulty_c = 0, so Easy = -1 * SD(Difficulty))
- Hard: Difficulty_c = +1 SD above mean (Hard = +1 * SD(Difficulty))
- Compute SD(Difficulty) from step02_merged_data.csv

**Define Time Points:**
- Use actual TSVR means per test session from data:
  - T1 (Day 0): mean(TSVR_hours | test == "T1") ~ 0 hours
  - T2 (Day 1): mean(TSVR_hours | test == "T2") ~ 24 hours
  - T3 (Day 3): mean(TSVR_hours | test == "T3") ~ 72 hours
  - T4 (Day 6): mean(TSVR_hours | test == "T4") ~ 144 hours
- Alternative: Use representative values (0, 24, 72, 144) if TSVR means are close

**Generate Predictions:**
For each combination of:
  - Difficulty_Level: {Easy, Hard} (2 levels)
  - Congruence: {Common, Congruent, Incongruent} (3 levels)
  - Time: {T1, T2, T3, T4} (4 timepoints)
Total: 2 x 3 x 4 = 24 predicted values

Use GLMM model to predict probability of correct response:
- Fixed effects: TSVR_hours, Difficulty_c, Congruence, + interactions
- Random effects: Marginalize over participants and items (population-level predictions)
- Compute 95% confidence intervals (using model SE for fixed effects)
- Transform from log-odds to probability scale: p = exp(logit) / (1 + exp(logit))

**Output:**

**File:** data/step05_difficulty_trajectories_by_congruence_data.csv
**Format:** CSV, plot source data for 6-line trajectory plot
**Columns:**
  - `Congruence` (string, values: Common, Congruent, Incongruent)
  - `Difficulty_Level` (string, values: Easy, Hard)
  - `Time_Hours` (float, TSVR_hours representative values: 0, 24, 72, 144)
  - `Predicted_Probability` (float, predicted probability of correct response, range: [0, 1])
  - `CI_lower` (float, lower bound of 95% confidence interval, range: [0, 1])
  - `CI_upper` (float, upper bound of 95% confidence interval, range: [0, 1])
**Expected Rows:** 24 (2 difficulty x 3 congruence x 4 timepoints)
**Note:** This CSV is read by rq_plots later to generate 6-line trajectory plot. PNG output goes to plots/ when rq_plots runs.

**Validation Requirement:**

Validation tools MUST be used after plot data preparation execution. Specific validation tools determined by rq_tools (likely validate_probability_range, validate_dataframe_structure, validate_plot_data_completeness).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_difficulty_trajectories_by_congruence_data.csv exists (exact path)
- Expected rows: 24 (2 difficulty x 3 congruence x 4 timepoints)
- Expected columns: 6 (Congruence, Difficulty_Level, Time_Hours, Predicted_Probability, CI_lower, CI_upper)

*Value Ranges:*
- Predicted_Probability in [0, 1] (probability scale, no values outside bounds)
- CI_lower in [0, 1], CI_upper in [0, 1]
- CI_lower <= Predicted_Probability <= CI_upper for all rows (confidence bounds must bracket point estimate)
- Time_Hours in {0, 24, 72, 144} (4 timepoints, approximate actual TSVR means)

*Data Quality:*
- No NaN values tolerated (all 24 predictions must be valid)
- Expected N: Exactly 24 rows (no more, no less)
- All 3 congruence levels present (Common, Congruent, Incongruent)
- Both difficulty levels present (Easy, Hard)
- All 4 timepoints present (0, 24, 72, 144 hours)
- Complete factorial design: 2 x 3 x 4 = 24 unique combinations

*Log Validation:*
- Required pattern: "Generated {N} predictions" where N = 24
- Required pattern: "All probabilities in [0, 1] range"
- Required pattern: "All CI bounds valid (CI_lower <= Predicted <= CI_upper)"
- Forbidden patterns: "ERROR", "NaN in predictions", "Probability outside [0,1]"
- Acceptable warnings: None expected for this step

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Expected 24 rows, found 18 (missing Easy x Incongruent combinations)")
- Log failure to logs/step05_prepare_plot_data.log
- Quit immediately (plot data incomplete, cannot proceed to rq_plots)
- g_debug invoked to diagnose (common causes: prediction generation error, missing factor levels)

**Expected Behavior on Validation Success:**
- Confirm 24 predictions generated successfully
- Confirm all probabilities and CIs valid
- Confirm complete factorial design (all 2 x 3 x 4 combinations present)
- Note: This step completes analysis pipeline. rq_plots will use this CSV to generate PNG later.

**Plotting Function (rq_plots will call later):**
- Plot type: 6-line trajectory plot (2 difficulty levels x 3 congruence levels)
- X-axis: Time_Hours (0 to 144)
- Y-axis: Predicted_Probability (0 to 1, probability scale)
- Lines: 6 total (Easy-Common, Easy-Congruent, Easy-Incongruent, Hard-Common, Hard-Congruent, Hard-Incongruent)
- Confidence bands: Shaded regions between CI_lower and CI_upper
- Color: By Congruence (3 colors)
- Linetype: By Difficulty_Level (Easy = dashed, Hard = solid)
- Expected pattern if 3-way interaction significant: Diverging slopes (Easy vs Hard separation varies by Congruence)

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs - intermediate and final)

- data/step00_item_difficulty_by_congruence.csv (from Step 0: item parameters from RQ 5.4.1)
- data/step01_response_level_data.csv (from Step 1: item-level binary responses with TSVR)
- data/step02_merged_data.csv (from Step 2: responses merged with difficulty + centered)
- data/step03_glmm_model_summary.txt (from Step 3: GLMM fitted model summary)
- data/step03_fixed_effects.csv (from Step 3: fixed effects table with dual p-values)
- data/step03_random_effects.csv (from Step 3: random effects variance components)
- data/step04_interaction_3way.csv (from Step 4: 3-way interaction term extraction)
- data/step04_congruence_stratified_slopes.csv (from Step 4: Time x Difficulty interaction per congruence level)
- data/step05_difficulty_trajectories_by_congruence_data.csv (from Step 5: plot source CSV)

### Logs (ONLY execution logs - .log files capturing stdout/stderr)

- logs/step00_extract_item_difficulty.log
- logs/step01_extract_responses.log
- logs/step02_merge_difficulty.log
- logs/step03_fit_glmm.log
- logs/step04_extract_interaction.log
- logs/step05_prepare_plot_data.log

### Plots (EMPTY until rq_plots runs)

- plots/difficulty_trajectories_by_congruence.png (created by rq_plots, NOT analysis steps)

### Results (EMPTY until rq_results runs)

- results/summary.md (created by rq_results, NOT analysis steps)

---

## Expected Data Formats

### step00_item_difficulty_by_congruence.csv

**Format:** CSV, one row per item (60-80 items)
**Columns:**
  - `ItemID` (string, VR item identifier, e.g., "VR-IFR-A01-N-i1")
  - `Congruence` (string, categorical: {Common, Congruent, Incongruent})
  - `Difficulty` (float, IRT difficulty parameter b, range: [-3.0, 3.0])
**Purpose:** Maps items to congruence categories and difficulty values for merging onto response data

### step01_response_level_data.csv

**Format:** CSV, long format (one row per response observation, ~24,000-32,000 rows)
**Columns:**
  - `UID` (string, participant identifier, format: P### with leading zeros)
  - `test` (string, test session: T1, T2, T3, T4)
  - `ItemID` (string, item identifier, matches step00 ItemID)
  - `Response` (int, binary: 0=incorrect, 1=correct)
  - `TSVR_hours` (float, actual time since encoding, range: [0, 168])
**Purpose:** Item-level binary responses with time variable, ready for merging with item difficulty

### step02_merged_data.csv

**Format:** CSV, long format (one row per response observation, ~24,000-32,000 rows)
**Columns:**
  - `UID` (string, participant identifier)
  - `test` (string, test session)
  - `ItemID` (string, item identifier)
  - `Response` (int, binary: 0=incorrect, 1=correct)
  - `TSVR_hours` (float, time variable)
  - `Difficulty` (float, raw IRT difficulty parameter)
  - `Difficulty_c` (float, grand-mean centered difficulty, mean approximately 0)
  - `Congruence` (string, categorical: Common, Congruent, Incongruent)
**Purpose:** Complete GLMM input with all predictors (Time, Difficulty_c, Congruence) and crossed grouping factors (UID, ItemID)

### step03_fixed_effects.csv

**Format:** CSV, one row per fixed effect term (~15 rows)
**Columns:**
  - `term` (string, predictor name, e.g., "TSVR_hours", "Difficulty_c", "TSVR_hours:Difficulty_c:Congruent")
  - `estimate` (float, coefficient on log-odds scale)
  - `SE` (float, standard error)
  - `z` (float, z-statistic)
  - `p_uncorrected` (float, uncorrected p-value)
  - `p_bonferroni` (float, Bonferroni-corrected p-value, alpha = 0.0033)
  - `OR` (float, odds ratio = exp(estimate))
  - `OR_CI_lower` (float, 95% CI lower bound for odds ratio)
  - `OR_CI_upper` (float, 95% CI upper bound for odds ratio)
**Purpose:** Fixed effects inference table with dual p-values (Decision D068) and odds ratios for interpretation

### step04_interaction_3way.csv

**Format:** CSV, 2 rows (Congruent and Incongruent contrasts vs Common reference)
**Columns:** Same as step03_fixed_effects.csv (term, estimate, SE, z, p_uncorrected, p_bonferroni, OR, OR_CI_lower, OR_CI_upper, significant_bonferroni)
**Purpose:** Isolates 3-way interaction terms for primary hypothesis test (p_bonferroni < 0.0033?)

### step04_congruence_stratified_slopes.csv

**Format:** CSV, 3 rows (one per congruence level)
**Columns:**
  - `Congruence` (string, values: Common, Congruent, Incongruent)
  - `interaction_estimate` (float, TSVR_hours:Difficulty_c coefficient on log-odds scale)
  - `SE` (float, standard error)
  - `z` (float, z-statistic)
  - `p_value` (float, uncorrected p-value, exploratory only)
  - `OR` (float, odds ratio for interaction)
  - `OR_CI_lower` (float, 95% CI lower bound)
  - `OR_CI_upper` (float, 95% CI upper bound)
**Purpose:** Congruence-specific Time x Difficulty interactions for post-hoc pattern interpretation

### step05_difficulty_trajectories_by_congruence_data.csv

**Format:** CSV, 24 rows (2 difficulty x 3 congruence x 4 timepoints), plot source data
**Columns:**
  - `Congruence` (string, values: Common, Congruent, Incongruent)
  - `Difficulty_Level` (string, values: Easy, Hard)
  - `Time_Hours` (float, TSVR_hours: 0, 24, 72, 144)
  - `Predicted_Probability` (float, predicted P(correct), range: [0, 1])
  - `CI_lower` (float, 95% CI lower bound, range: [0, 1])
  - `CI_upper` (float, 95% CI upper bound, range: [0, 1])
**Purpose:** Plot source CSV for 6-line trajectory visualization (read by rq_plots, PNG saved to plots/)

---

## Cross-RQ Dependencies

**This RQ requires outputs from RQ 5.4.1:**

**Dependency RQ:** RQ 5.4.1 (Schema-Specific Trajectories)

**Required Files:**
1. results/ch5/5.4.1/data/step03_item_parameters.csv
   - Used in: Step 0 (extract item difficulty parameters)
   - Rationale: RQ 5.4.1 performs IRT calibration (2-pass purification) on schema congruence items. This RQ uses those difficulty estimates as predictor variable in GLMM.

2. results/ch5/5.4.1/data/step02_purified_items.csv
   - Used in: Step 0 (validation - cross-check purified item list)
   - Rationale: Ensures only items passing RQ 5.4.1 purification (a >= 0.4, |b| <= 3.0) are included in this analysis.

3. results/ch5/5.4.1/data/step00_tsvr_mapping.csv
   - Used in: Step 1 (merge TSVR_hours onto response data)
   - Rationale: Time variable uses actual hours since encoding (Decision D070), not nominal days. RQ 5.4.1 creates this mapping.

**Execution Order Constraint:**
1. RQ 5.4.1 must complete through Step 3 (IRT Pass 2 calibration)
2. This RQ (5.4.8) can then execute (uses RQ 5.4.1 outputs as DERIVED data source)

**Data Source Boundaries:**
- **RAW data:** dfData.csv (item-level binary responses extracted directly)
- **DERIVED data:** RQ 5.4.1 outputs (item parameters, purified item list, TSVR mapping)
- **Scope:** This RQ does NOT re-calibrate IRT models (uses RQ 5.4.1 difficulty parameters as fixed item-level predictors in GLMM)

**Validation:**
- Step 0: Check results/ch5/5.4.1/data/step03_item_parameters.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 1: Check results/ch5/5.4.1/data/step00_tsvr_mapping.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- If either file missing -> quit with error -> user must execute RQ 5.4.1 first

---

## Validation Requirements

**CRITICAL MANDATE:**

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

### Validation Requirements By Step

#### Step 0: Extract Item Parameters from RQ 5.4.1

**Analysis Tool:** (determined by rq_tools - likely pandas read_csv + filtering)
**Validation Tool:** (determined by rq_tools - likely validate_dataframe_structure, validate_numeric_range)

**What Validation Checks:**
- Output file exists (data/step00_item_difficulty_by_congruence.csv)
- Expected row count (60-80 items)
- Expected column count (3: ItemID, Congruence, Difficulty)
- Difficulty values in range [-3.0, 3.0] (D039 purification bounds)
- No NaN values (all items have valid difficulty estimates)
- Congruence categories valid: {Common, Congruent, Incongruent}

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 60-80 items, found 45")
- Log failure to logs/step00_extract_item_difficulty.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose (common causes: RQ 5.4.1 incomplete, file path wrong)

---

#### Step 1: Extract Item-Level Response Data and Merge TSVR

**Analysis Tool:** (determined by rq_tools - likely pandas read_csv + merge + filtering)
**Validation Tool:** (determined by rq_tools - likely validate_dataframe_structure, validate_numeric_range, check_missing_data)

**What Validation Checks:**
- Output file exists (data/step01_response_level_data.csv)
- Expected row count (24,000-32,000 observations)
- Expected column count (5: UID, test, ItemID, Response, TSVR_hours)
- Response values in {0, 1} (binary only)
- TSVR_hours in [0, 168] hours
- No NaN values in TSVR_hours (all responses matched)
- All 100 participants present
- All 4 test sessions per participant

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Found {X} responses with missing TSVR_hours")
- Log failure to logs/step01_extract_responses.log
- Quit immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose (common causes: TSVR mapping incomplete, merge key mismatch)

---

#### Step 2: Merge Item Difficulty and Center Difficulty Variable

**Analysis Tool:** (determined by rq_tools - likely pandas merge + centering arithmetic)
**Validation Tool:** (determined by rq_tools - likely validate_standardization, check_missing_data)

**What Validation Checks:**
- Output file exists (data/step02_merged_data.csv)
- Row count matches Step 1 exactly (no data loss during merge)
- Expected column count (8: UID, test, ItemID, Response, TSVR_hours, Difficulty, Difficulty_c, Congruence)
- No NaN values (all responses matched with item difficulty)
- Difficulty_c centering: mean within +/- 0.01 of zero
- Congruence distribution: approximately 1/3 responses per category

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Mean Difficulty_c = 0.15, centering failed")
- Log failure to logs/step02_merge_difficulty.log
- Quit immediately (do NOT proceed to Step 3)
- g_debug invoked to diagnose (common causes: merge key mismatch, centering arithmetic error)

---

#### Step 3: Fit Cross-Classified GLMM with 3-Way Interaction

**Analysis Tool:** (determined by rq_tools - likely pymer4.Lmer with family='binomial' or lme4::glmer via rpy2)
**Validation Tool:** (determined by rq_tools - likely validate_model_convergence, validate_variance_positivity, validate_lmm_assumptions_comprehensive adapted for GLMM, validate_hypothesis_test_dual_pvalues per D068)

**What Validation Checks:**
- Output files exist (glmm_model_summary.txt, fixed_effects.csv, random_effects.csv)
- Model convergence: converged = TRUE
- Variance components: all > 0 (no singularity)
- Fixed effects: no NaN values
- Dual p-values present: p_uncorrected AND p_bonferroni columns (Decision D068 compliance)
- Overdispersion check: Residual deviance / df approximately 1 (if > 1.5, document)
- Random effects normality: Q-Q plot approximately normal (mild violations acceptable)

**Expected Behavior on Validation Failure:**
- If convergence fails after contingency plan -> Raise error "GLMM convergence failed"
- If variance components <= 0 -> Raise error "Random effects singularity"
- If NaN in fixed effects -> Raise error "Model fitting failed"
- Log all failures to logs/step03_fit_glmm.log
- Quit immediately (do NOT proceed to Step 4)
- g_debug invoked to diagnose (common causes: perfect separation, insufficient data, overfitted random effects)

---

#### Step 4: Extract 3-Way Interaction and Congruence-Stratified Difficulty Effects

**Analysis Tool:** (determined by rq_tools - likely pandas filtering + pymer4 re-fitting for stratified models)
**Validation Tool:** (determined by rq_tools - likely validate_hypothesis_test_dual_pvalues, validate_dataframe_structure)

**What Validation Checks:**
- Output files exist (interaction_3way.csv, congruence_stratified_slopes.csv)
- 3-way interaction: 2 rows (Congruent, Incongruent contrasts)
- Stratified slopes: 3 rows (one per congruence level)
- Dual p-values present: p_uncorrected AND p_bonferroni columns (Decision D068 compliance)
- No NaN values in interaction or stratified tables
- Bonferroni alpha correctly calculated: 0.0033

**Expected Behavior on Validation Failure:**
- If dual p-values missing -> Raise error "3-way interaction missing p_bonferroni (D068 violation)"
- If stratified models fail -> Document which level(s) failed, proceed with available results
- Log failure to logs/step04_extract_interaction.log
- Quit if 3-way interaction extraction fails
- g_debug invoked to diagnose

---

#### Step 5: Prepare Trajectory Plot Data

**Analysis Tool:** (determined by rq_tools - likely pandas + GLMM predict method)
**Validation Tool:** (determined by rq_tools - likely validate_probability_range, validate_plot_data_completeness)

**What Validation Checks:**
- Output file exists (difficulty_trajectories_by_congruence_data.csv)
- Expected row count: 24 (2 difficulty x 3 congruence x 4 timepoints)
- Expected column count: 6 (Congruence, Difficulty_Level, Time_Hours, Predicted_Probability, CI_lower, CI_upper)
- Predicted_Probability in [0, 1]
- CI bounds valid: CI_lower <= Predicted_Probability <= CI_upper
- Complete factorial design: all 2 x 3 x 4 combinations present

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Expected 24 rows, found 18")
- Log failure to logs/step05_prepare_plot_data.log
- Quit immediately (plot data incomplete)
- g_debug invoked to diagnose (common causes: prediction generation error, missing factor levels)

---

## Summary

**Total Steps:** 6 (Step 0 through Step 5)

**Estimated Runtime:** Medium (~40-70 minutes total)
  - Step 0: <5 minutes (data loading)
  - Step 1: ~5 minutes (extraction + merge)
  - Step 2: <5 minutes (merge + centering)
  - Step 3: 30-60 minutes (GLMM fitting with crossed random effects, binomial family)
  - Step 4: ~5 minutes (coefficient extraction + stratified re-fitting)
  - Step 5: ~5 minutes (prediction generation)

**Cross-RQ Dependencies:** RQ 5.4.1 (requires item_parameters.csv, purified_items.csv, tsvr_mapping.csv)

**Primary Outputs:**
- step03_glmm_model_summary.txt (full GLMM results)
- step03_fixed_effects.csv (fixed effects with dual p-values)
- step04_interaction_3way.csv (3-way interaction term, primary hypothesis test)
- step04_congruence_stratified_slopes.csv (post-hoc congruence-specific difficulty effects)
- step05_difficulty_trajectories_by_congruence_data.csv (plot source CSV for 6-line trajectory)

**Validation Coverage:** 100% (all 6 steps have validation requirements with 4-layer substance criteria)

**Critical Methodological Note:**
This RQ uses GLMM with binomial family (NOT standard LMM) because responses are binary (0/1). Coefficients are on log-odds scale; exponentiate for odds ratios. Dual p-values reported per Decision D068. TSVR_hours used as time variable per Decision D070.

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-02): Initial plan created by rq_planner agent for RQ 5.4.8
