# Analysis Plan: Age Effects on Confidence

**Research Question:** 6.1.3
**Created:** 2025-12-06
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines whether age moderates confidence trajectories across a 6-day retention interval. It uses IRT-derived theta confidence scores from RQ 6.1.1 and tests Age x Time interactions via Linear Mixed Model (LMM). The analysis parallels Chapter 5 age effect RQs (5.1.3, 5.2.3, 5.3.4, 5.4.3), allowing direct comparison between age effects on accuracy vs metacognitive monitoring.

**Pipeline:** LMM-only (no IRT - uses DERIVED theta from RQ 6.1.1)

**Steps:** 6 analysis steps (Step 0: load data + Steps 1-5: LMM analysis and comparison)

**Estimated Runtime:** Medium (~15-30 minutes total: data loading low, LMM fitting medium, effect size computation low, tertile aggregation low, comparison low)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni alpha = 0.0167 for three comparisons)
- Decision D070: TSVR as time variable (actual hours since encoding, not nominal days)
- NO Decision D039: No IRT calibration in this RQ (uses DERIVED theta from RQ 6.1.1)
- NO Decision D069: No trajectory plots in this RQ (descriptive tertile plots only, not dual-scale trajectory requirement)

---

## Analysis Plan

This RQ requires 6 steps:

### Step 0: Load Theta Confidence and Merge with TSVR and Age

**Dependencies:** None (first step, but requires RQ 6.1.1 completion)

**Complexity:** Low (data loading and merging only, ~2-5 minutes)

**Input:**

**File 1:** results/ch6/6.1.1/data/step03_theta_confidence.csv
**Source:** RQ 6.1.1 Step 3 (IRT Pass 2 final theta estimates)
**Format:** CSV with columns:
  - `composite_ID` (string, format: {UID}_{test}, e.g., P001_T1)
  - `theta_confidence` (float, IRT ability estimate for metacognitive monitoring)
  - `se_confidence` (float, standard error of theta estimate)
**Expected Rows:** 400 (100 participants x 4 tests)

**File 2:** results/ch6/6.1.1/data/step00_tsvr_mapping.csv
**Source:** RQ 6.1.1 Step 0 (time variable extraction)
**Format:** CSV with columns:
  - `composite_ID` (string, format: {UID}_{test})
  - `TSVR_hours` (float, actual hours since VR encoding session per Decision D070)
  - `test` (string, test session identifier: T1, T2, T3, T4)
**Expected Rows:** 400 (100 participants x 4 tests)

**File 3:** data/cache/dfData.csv
**Source:** Project master demographics file
**Format:** CSV with columns:
  - `UID` (string, participant unique identifier, e.g., P001)
  - `Age` (int or float, participant age in years at enrollment)
**Expected Rows:** >=100 participants (extract Age for merge)

**Processing:**

1. Load theta_confidence.csv and verify 400 rows (100 participants x 4 tests)
2. Load tsvr_mapping.csv and verify 400 rows matching theta data
3. Merge theta with TSVR on composite_ID (left join - keep all theta rows, add TSVR_hours and test columns)
4. Parse UID from composite_ID (extract substring before underscore: "P001_T1" -> "P001")
5. Load dfData.csv and extract Age column
6. Merge with Age on UID (left join - add Age column to each composite_ID row)
7. Verify no missing TSVR_hours or Age values after merge (all 400 rows must have complete data)
8. Save merged data to data/step00_lmm_input_raw.csv

**Output:**

**File:** data/step00_lmm_input_raw.csv
**Format:** CSV, wide format (one row per composite_ID)
**Columns:**
  - `composite_ID` (string, format: {UID}_{test})
  - `UID` (string, participant identifier extracted from composite_ID)
  - `test` (string, test session: T1, T2, T3, T4)
  - `theta_confidence` (float, IRT ability estimate)
  - `se_confidence` (float, standard error of theta)
  - `TSVR_hours` (float, time since encoding in hours per Decision D070)
  - `Age` (int or float, participant age in years)
**Expected Rows:** 400 (100 participants x 4 tests)
**Expected Nulls:** None (all columns non-null after merge - validation failure if NaN detected)

**Validation Requirement:**

Validation tools MUST be used after data loading and merging tool execution. Specific validation tools will be determined by rq_tools based on data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_lmm_input_raw.csv exists (exact path)
- Expected rows: 400 (100 participants x 4 tests)
- Expected columns: 7 (composite_ID, UID, test, theta_confidence, se_confidence, TSVR_hours, Age)
- Data types: composite_ID (object), UID (object), test (object), theta_confidence (float64), se_confidence (float64), TSVR_hours (float64), Age (int64 or float64)

*Value Ranges:*
- theta_confidence in [-3, 3] (typical IRT ability range, outside suggests calibration problem)
- se_confidence in [0.1, 1.0] (above 1.0 = unreliable estimates)
- TSVR_hours in [0, 200] hours (0 = T1 encoding, ~24h = T2, ~72h = T3, ~144h = T4, max 200h reasonable)
- Age in [18, 90] years (adult sample, outside suggests data error)

*Data Quality:*
- No NaN values tolerated (all 400 rows x 7 columns must be complete)
- Expected N: Exactly 400 rows (100 participants x 4 tests, no data loss)
- No duplicate composite_IDs (each participant-test combination appears once)
- UID count: Exactly 100 unique UIDs (all participants present)

*Log Validation:*
- Required pattern: "Merged theta with TSVR: 400 rows"
- Required pattern: "Merged with Age: 400 rows, 0 missing"
- Required pattern: "Data loading complete: 400 rows x 7 columns"
- Forbidden patterns: "ERROR", "NaN detected", "Missing TSVR", "Missing Age"
- Acceptable warnings: None expected for data merge

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 400 rows, found 387" or "NaN detected in Age column")
- Log failure to logs/step00_load_data.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause

---

### Step 1: Center Age Variable

**Dependencies:** Step 0 (requires step00_lmm_input_raw.csv)

**Complexity:** Low (simple transformation, <1 minute)

**Input:**

**File:** data/step00_lmm_input_raw.csv
**Source:** Generated by Step 0 (merged theta, TSVR, Age)
**Format:** CSV with columns: composite_ID, UID, test, theta_confidence, se_confidence, TSVR_hours, Age
**Expected Rows:** 400

**Processing:**

1. Load step00_lmm_input_raw.csv
2. Compute mean(Age) across all participants (grand mean centering)
3. Create Age_c column: Age_c = Age - mean(Age) for each row
4. Verify Age_c has mean approximately 0 (within tolerance for rounding: |mean(Age_c)| < 0.001)
5. Add Age_c column to DataFrame
6. Save to data/step01_lmm_input.csv

**Rationale for Centering:**
- Enables intercept interpretation as "average-age participant" baseline confidence
- Reduces multicollinearity in Age x Time interaction term
- Standard practice for continuous moderators in LMM

**Output:**

**File:** data/step01_lmm_input.csv
**Format:** CSV, wide format (one row per composite_ID)
**Columns:**
  - All columns from step00_lmm_input_raw.csv PLUS:
  - `Age_c` (float, centered Age: Age - mean(Age))
**Expected Rows:** 400 (100 participants x 4 tests)
**Expected Nulls:** None

**Validation Requirement:**

Validation tools MUST be used after age centering tool execution. Specific validation tools will be determined by rq_tools based on centering operation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_lmm_input.csv exists (exact path)
- Expected rows: 400
- Expected columns: 8 (step00 columns + Age_c)
- Data types: Age_c (float64)

*Value Ranges:*
- Age_c mean approximately 0 (|mean(Age_c)| < 0.001)
- Age_c range: typically [-30, 30] years from mean age (depends on sample age range)
- Age_c SD: should match SD(Age) from step00 (centering doesn't change spread)

*Data Quality:*
- No NaN in Age_c column
- All 400 rows present
- Age_c = Age - mean(Age) verified for sample rows (spot check)

*Log Validation:*
- Required pattern: "Age centered: mean(Age_c) = {value}" where |value| < 0.001
- Required pattern: "Age_c added to LMM input: 400 rows"
- Forbidden patterns: "ERROR", "NaN in Age_c"

**Expected Behavior on Validation Failure:**
- Raise error (e.g., "Age_c mean = 2.5, expected ~0")
- Log failure to logs/step01_center_age.log
- Quit immediately
- g_debug invoked

---

### Step 2: Determine Time Predictors from RQ 6.1.1

**Dependencies:** Step 1 (requires step01_lmm_input.csv), RQ 6.1.1 functional form selection

**Complexity:** Low (reading configuration, no fitting, <1 minute)

**Input:**

**File 1:** data/step01_lmm_input.csv
**Source:** Generated by Step 1 (LMM input with Age_c)
**Format:** CSV with theta_confidence, TSVR_hours, Age, Age_c columns
**Expected Rows:** 400

**File 2:** results/ch6/6.1.1/data/step05_functional_form_selection.csv (or similar)
**Source:** RQ 6.1.1 Step 5 (functional form comparison results)
**Format:** CSV documenting which time transformation(s) were selected as optimal
**Expected Content:** Selected predictors (e.g., "Time" only, "Time + Time_log", "Time + Time_quad", etc.)
**Note:** If RQ 6.1.1 doesn't create explicit selection file, read from 6.1.1 LMM summary or 2_plan.md

**Processing:**

1. Load step01_lmm_input.csv
2. Read RQ 6.1.1 functional form selection (determine which time predictors were optimal)
3. Create time predictor columns matching 6.1.1 selection:
   - If "Time" only: Time = TSVR_hours (no transformation)
   - If "Time + Time_log": Time = TSVR_hours, Time_log = log(TSVR_hours + 1) [+1 to handle T1 = 0 hours]
   - If "Time + Time_quad": Time = TSVR_hours, Time_quad = TSVR_hours^2
   - If "Time_log" only: Time_log = log(TSVR_hours + 1)
4. Add time predictor column(s) to DataFrame
5. Save to data/step02_lmm_input_with_time.csv

**Rationale:**
- RQ 6.1.3 uses SAME functional form as RQ 6.1.1 for consistency across confidence analyses
- Age effects tested on top of optimal time trajectory shape (not forcing linear when data are curvilinear)

**Output:**

**File:** data/step02_lmm_input_with_time.csv
**Format:** CSV, wide format (one row per composite_ID)
**Columns:**
  - All columns from step01_lmm_input.csv PLUS:
  - Time predictors matching RQ 6.1.1 selection (e.g., `Time`, `Time_log`, or both)
**Expected Rows:** 400
**Expected Nulls:** None

**Validation Requirement:**

Validation tools MUST be used after time transformation tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_lmm_input_with_time.csv exists
- Expected rows: 400
- Expected columns: 8-10 (depends on how many time predictors added: 1-2 additional columns)
- Data types: Time (float64), Time_log (float64 if present), Time_quad (float64 if present)

*Value Ranges:*
- Time = TSVR_hours in [0, 200] (no transformation)
- Time_log in [0, 5.5] approximately (log(200+1) ~= 5.3, log(0+1) = 0)
- Time_quad in [0, 40000] approximately (200^2 = 40000, 0^2 = 0)

*Data Quality:*
- No NaN in time predictor columns
- Time values match TSVR_hours exactly (if Time used)
- Time_log values match log(TSVR_hours + 1) for sample rows (spot check)
- All 400 rows present

*Log Validation:*
- Required pattern: "Time predictors created: {list of predictors}"
- Required pattern: "Functional form matches RQ 6.1.1: {form}"
- Forbidden patterns: "ERROR", "NaN in time predictors"

**Expected Behavior on Validation Failure:**
- Raise error (e.g., "Time_log contains NaN")
- Log failure to logs/step02_create_time_predictors.log
- Quit immediately

---

### Step 3: Fit LMM with Age x Time Interaction

**Dependencies:** Step 2 (requires step02_lmm_input_with_time.csv)

**Complexity:** Medium (LMM fitting with random slopes, ~5-15 minutes depending on convergence)

**Input:**

**File:** data/step02_lmm_input_with_time.csv
**Source:** Generated by Step 2 (LMM input with time predictors and Age_c)
**Format:** CSV with columns: composite_ID, UID, test, theta_confidence, se_confidence, TSVR_hours, Age, Age_c, Time predictors (Time, Time_log, etc.)
**Expected Rows:** 400

**Processing:**

1. Load step02_lmm_input_with_time.csv
2. Determine LMM formula based on RQ 6.1.1 time predictors:
   - If Time only: `theta_confidence ~ Time * Age_c + (Time | UID)`
   - If Time + Time_log: `theta_confidence ~ (Time + Time_log) * Age_c + (Time + Time_log | UID)`
   - Interaction syntax: `* Age_c` expands to main effects + interaction (Time + Age_c + Time:Age_c)
3. Fit LMM using statsmodels.formula.api.mixedlm (REML estimation)
4. Random effects structure: Random slopes for time predictors by UID (allows individual variation in decline rates)
5. Check convergence (no singularity warnings, optimizer converged successfully)
6. Extract model summary (fixed effects table, random effects variance components)
7. Save full summary to data/step03_lmm_summary.txt
8. Extract fixed effects table and save to data/step03_lmm_fixed_effects.csv

**Fixed Effects of Interest:**
- Age_c main effect: Baseline confidence difference (intercept shift for +1 year age)
- Time:Age_c interaction: Differential decline rate (does forgetting slope change with age?)
- Time main effect: Overall decline rate (average across ages)

**Output:**

**File 1:** data/step03_lmm_summary.txt
**Format:** Plain text, full statsmodels summary
**Content:** Fixed effects, random effects variance components, fit indices (log-likelihood, AIC, BIC)
**Expected Lines:** ~50-100 lines (comprehensive model output)

**File 2:** data/step03_lmm_fixed_effects.csv
**Format:** CSV with columns:
  - `term` (string, predictor name: Intercept, Time, Age_c, Time:Age_c, Time_log, Time_log:Age_c, etc.)
  - `estimate` (float, coefficient estimate)
  - `se` (float, standard error)
  - `z` (float, z-statistic)
  - `p` (float, uncorrected p-value)
**Expected Rows:** 3-7 rows depending on time predictors (Intercept + Time + Age_c + interaction(s))

**Validation Requirement:**

Validation tools MUST be used after LMM fitting tool execution. Specific validation tools will be determined by rq_tools based on LMM requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_lmm_summary.txt exists (exact path)
- data/step03_lmm_fixed_effects.csv exists
- Expected rows in fixed_effects.csv: 3-7 (depends on number of time predictors)
- Expected columns in fixed_effects.csv: 5 (term, estimate, se, z, p)
- Data types: term (object), estimate (float64), se (float64), z (float64), p (float64)

*Value Ranges:*
- estimate (coefficients): typically in [-2, 2] for standardized predictors (outside suggests extreme effect or scaling issue)
- se (standard errors): typically in [0.01, 1.0] (near 0 = overfitting, >1 = high uncertainty)
- z-statistic: unrestricted (large |z| indicates significance)
- p in [0, 1] (probability, must be valid)

*Data Quality:*
- No NaN in fixed effects table (convergence failure produces NaN)
- All expected terms present: Intercept, Time (or time predictors from 6.1.1), Age_c, interaction(s)
- Age_c and Time:Age_c terms must be present (primary hypothesis test)
- No duplicate terms (each predictor appears once)

*Log Validation:*
- Required pattern: "Model converged: True"
- Required pattern: "Fixed effects extracted: {N} terms"
- Required pattern: "Age_c term present: estimate = {value}"
- Required pattern: "Time:Age_c interaction term present: estimate = {value}"
- Forbidden patterns: "ERROR", "Convergence failed", "Singular matrix", "NaN in fixed effects"
- Acceptable warnings: "Random effects variance near boundary" (common with small slope variance, not critical)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Model did not converge" or "Age_c term missing from fixed effects")
- Log failure to logs/step03_fit_lmm.log
- Quit script immediately
- g_debug invoked (common causes: convergence issues, model misspecification, insufficient data)

---

### Step 4: Extract Age Effects with Dual P-Values

**Dependencies:** Step 3 (requires step03_lmm_fixed_effects.csv)

**Complexity:** Low (extracting rows and applying Bonferroni correction, <1 minute)

**Input:**

**File:** data/step03_lmm_fixed_effects.csv
**Source:** Generated by Step 3 (LMM fixed effects table)
**Format:** CSV with columns: term, estimate, se, z, p (uncorrected)
**Expected Rows:** 3-7

**Processing:**

1. Load step03_lmm_fixed_effects.csv
2. Extract rows for Age_c main effect and Time:Age_c interaction (primary hypothesis terms)
3. Apply Bonferroni correction per Decision D068:
   - Three comparisons: Time main effect, Age_c main effect, Time:Age_c interaction
   - Bonferroni alpha = 0.05 / 3 = 0.0167
4. Create dual p-value columns:
   - `p_uncorrected` (original p-value from LMM)
   - `p_bonferroni` (same value, but interpret against alpha = 0.0167 threshold)
5. Flag significance at both thresholds:
   - `sig_uncorrected` (p < 0.05)
   - `sig_bonferroni` (p < 0.0167)
6. Save extracted effects to data/step04_age_effects.csv

**Hypothesis Test:**
- Null Hypothesis: Age_c:Time interaction coefficient = 0 (age does NOT moderate decline rate)
- Alternative: Age_c:Time interaction coefficient != 0 (older adults decline faster/slower)
- Expected: NULL (paralleling Ch5 RQs 5.1.3, 5.2.3, 5.3.4, 5.4.3 all NULL for age x time interaction)

**Output:**

**File:** data/step04_age_effects.csv
**Format:** CSV with columns:
  - `term` (string, predictor name: Age_c, Time:Age_c)
  - `estimate` (float, coefficient estimate)
  - `se` (float, standard error)
  - `z` (float, z-statistic)
  - `p_uncorrected` (float, original p-value)
  - `p_bonferroni` (float, same value, interpreted against alpha = 0.0167)
  - `sig_uncorrected` (bool, p < 0.05)
  - `sig_bonferroni` (bool, p < 0.0167)
**Expected Rows:** 2 (Age_c main effect + Time:Age_c interaction)
**Note:** Time main effect also reported in step03_lmm_fixed_effects.csv, but not extracted here (focus on age-specific effects)

**Validation Requirement:**

Validation tools MUST be used after dual p-value extraction tool execution. Specific validation tools will be determined by rq_tools based on Decision D068 requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_age_effects.csv exists (exact path)
- Expected rows: 2 (Age_c main effect + Time:Age_c interaction)
- Expected columns: 8 (term, estimate, se, z, p_uncorrected, p_bonferroni, sig_uncorrected, sig_bonferroni)
- Data types: term (object), estimate (float64), se (float64), z (float64), p_uncorrected (float64), p_bonferroni (float64), sig_uncorrected (bool), sig_bonferroni (bool)

*Value Ranges:*
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1] (same as uncorrected, different interpretation threshold)
- sig_uncorrected: True if p < 0.05, False otherwise
- sig_bonferroni: True if p < 0.0167, False otherwise

*Data Quality:*
- Both Age_c and Time:Age_c rows present (no missing)
- p_uncorrected and p_bonferroni have identical values (correction is in threshold, not value)
- No NaN in any column

*Log Validation:*
- Required pattern: "Age effects extracted: 2 rows"
- Required pattern: "Dual p-values created per Decision D068"
- Required pattern: "Bonferroni alpha = 0.0167 for 3 comparisons"
- Forbidden patterns: "ERROR", "Missing Age_c term", "NaN in p-values"

**Expected Behavior on Validation Failure:**
- Raise error (e.g., "Expected 2 rows, found 1" or "Missing Time:Age_c interaction term")
- Log failure to logs/step04_extract_age_effects.log
- Quit immediately

---

### Step 5: Compute Effect Size at Day 6

**Dependencies:** Step 3 (requires step03_lmm_fixed_effects.csv and fitted model object)

**Complexity:** Low (prediction and difference computation, ~2-5 minutes)

**Input:**

**File:** data/step03_lmm_fixed_effects.csv
**Source:** Generated by Step 3 (fixed effects coefficients)
**Format:** CSV with coefficients for Age_c and Time:Age_c interaction

**File:** data/step02_lmm_input_with_time.csv (for Age and Time descriptive stats)
**Source:** Generated by Step 2 (used to compute SD(Age) for +/- 1 SD effect size calculation)

**Processing:**

1. Compute SD(Age) from original Age column (before centering) to define "younger" and "older" groups
2. Define comparison points:
   - Younger: Age_c = -1 * SD(Age) (1 SD below mean age)
   - Older: Age_c = +1 * SD(Age) (1 SD above mean age)
   - Time point: Day 6 retention test (maximum TSVR_hours in dataset, ~144 hours)
3. Load LMM fixed effects to extract coefficients
4. Predict theta_confidence for younger and older groups at Day 6:
   - Younger prediction: Intercept + (Time coef * TSVR_Day6) + (Age_c coef * [-1*SD]) + (Time:Age_c coef * TSVR_Day6 * [-1*SD])
   - Older prediction: Intercept + (Time coef * TSVR_Day6) + (Age_c coef * [+1*SD]) + (Time:Age_c coef * TSVR_Day6 * [+1*SD])
5. Compute difference: Older - Younger (positive = older adults more confident, negative = less confident)
6. Save effect size to data/step05_effect_size_day6.csv

**Rationale:**
- Effect size quantifies PRACTICAL significance of age effect (beyond p-value)
- Day 6 chosen as endpoint (maximum retention interval) where cumulative age differences largest
- +/- 1 SD captures realistic age variation in sample

**Output:**

**File:** data/step05_effect_size_day6.csv
**Format:** CSV with columns:
  - `comparison` (string, description: "Older vs Younger at Day 6")
  - `younger_theta` (float, predicted theta_confidence for Age_c = -1 SD)
  - `older_theta` (float, predicted theta_confidence for Age_c = +1 SD)
  - `difference` (float, older - younger in theta units)
  - `age_younger` (float, actual age corresponding to -1 SD, e.g., mean - 1*SD)
  - `age_older` (float, actual age corresponding to +1 SD, e.g., mean + 1*SD)
  - `tsvr_hours` (float, time point used for prediction, ~144 hours for Day 6)
**Expected Rows:** 1 (single comparison at Day 6)

**Validation Requirement:**

Validation tools MUST be used after effect size computation tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_effect_size_day6.csv exists
- Expected rows: 1
- Expected columns: 7 (comparison, younger_theta, older_theta, difference, age_younger, age_older, tsvr_hours)
- Data types: comparison (object), all numeric columns (float64)

*Value Ranges:*
- younger_theta in [-3, 3] (IRT theta range)
- older_theta in [-3, 3]
- difference in [-2, 2] (unreasonably large differences suggest computation error)
- age_younger in [18, 90] years (plausible adult ages)
- age_older in [18, 90] years, and age_older > age_younger
- tsvr_hours approximately 144 (Day 6 nominal = 144 hours, actual may vary slightly)

*Data Quality:*
- No NaN in any column
- age_older > age_younger (sanity check: older group has higher age)
- tsvr_hours > 0 (Day 6 is not encoding session)

*Log Validation:*
- Required pattern: "Effect size computed at Day 6 (TSVR = {hours} hours)"
- Required pattern: "Younger (Age_c = -{SD}): theta = {value}"
- Required pattern: "Older (Age_c = +{SD}): theta = {value}"
- Required pattern: "Difference: {value} theta units"
- Forbidden patterns: "ERROR", "NaN in predictions"

**Expected Behavior on Validation Failure:**
- Raise error (e.g., "Difference = 5.2 theta units (unreasonably large, expected < 2)")
- Log failure to logs/step05_compute_effect_size.log
- Quit immediately

---

### Step 6: Prepare Age Tertile Comparison Data

**Dependencies:** Step 2 (requires step02_lmm_input_with_time.csv for Age tertile assignment and observed means)

**Complexity:** Low (tertile assignment and aggregation, ~2-5 minutes)

**Input:**

**File:** data/step02_lmm_input_with_time.csv
**Source:** Generated by Step 2 (LMM input with Age and theta_confidence)
**Format:** CSV with 400 rows (100 participants x 4 tests)

**Processing:**

1. Load step02_lmm_input_with_time.csv
2. Assign participants to age tertiles based on Age variable:
   - Low: Age <= 33rd percentile
   - Medium: 33rd percentile < Age <= 67th percentile
   - High: Age > 67th percentile
3. Compute observed means for each tertile x test combination:
   - Group by: age_tertile (Low/Medium/High) and test (T1/T2/T3/T4)
   - Aggregate: mean(theta_confidence), SE(theta_confidence), N participants
4. Compute 95% CI: mean +/- 1.96 * SE
5. Save aggregated data to data/step06_age_tertile_data.csv

**Rationale:**
- Tertile plot provides visual inspection of age effect pattern (linear vs nonlinear, magnitude of separation)
- Complements LMM interaction test with descriptive visualization
- Facilitates comparison to Chapter 5 age tertile plots (expect similar pattern if confidence parallels accuracy)

**Output:**

**File:** data/step06_age_tertile_data.csv
**Format:** CSV with columns:
  - `age_tertile` (string, categorical: Low, Medium, High)
  - `test` (string, test session: T1, T2, T3, T4)
  - `mean_theta` (float, mean theta_confidence for tertile at this test)
  - `se_theta` (float, standard error of mean)
  - `CI_lower` (float, lower 95% CI bound)
  - `CI_upper` (float, upper 95% CI bound)
  - `N` (int, number of participants in tertile at this test)
**Expected Rows:** 12 (3 tertiles x 4 tests)
**Note:** This CSV is for plotting by rq_plots (Option B: plot source CSV created during analysis, visualization during rq_plots)

**Validation Requirement:**

Validation tools MUST be used after tertile aggregation tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_age_tertile_data.csv exists
- Expected rows: 12 (3 tertiles x 4 tests)
- Expected columns: 7 (age_tertile, test, mean_theta, se_theta, CI_lower, CI_upper, N)
- Data types: age_tertile (object), test (object), mean_theta (float64), se_theta (float64), CI_lower (float64), CI_upper (float64), N (int64)

*Value Ranges:*
- mean_theta in [-3, 3] (IRT theta range)
- se_theta in [0.1, 1.0] (reasonable SE for group means)
- CI_lower in [-3, 3], CI_upper in [-3, 3]
- CI_upper > CI_lower for all rows (sanity check)
- N in [20, 50] approximately (100 participants / 3 tertiles ~ 33 per tertile, some variation acceptable)

*Data Quality:*
- All 3 tertiles present: Low, Medium, High (no missing tertiles)
- All 4 tests present: T1, T2, T3, T4 (no missing tests)
- Exactly 12 rows (complete factorial: 3 x 4)
- No NaN in any column
- Each tertile x test combination appears exactly once (no duplicates)

*Log Validation:*
- Required pattern: "Age tertiles created: Low (N={n1}), Medium (N={n2}), High (N={n3})"
- Required pattern: "Aggregated means: 12 rows (3 tertiles x 4 tests)"
- Forbidden patterns: "ERROR", "Missing tertile", "NaN in aggregated data"

**Expected Behavior on Validation Failure:**
- Raise error (e.g., "Expected 12 rows, found 9" or "Missing High tertile")
- Log failure to logs/step06_prepare_tertile_data.log
- Quit immediately

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs - intermediate and final)

**FOLDER STRUCTURE (v4.2):**
- `/code` = ALL .py code files for running analysis
- `/data` = ALL inputs AND outputs from analysis steps (intermediate + final)
- `/docs` = ALL planning documentation (1_concept.md, 2_plan.md, 3_tools.yaml, 4_analysis.yaml, validation reports)
- `/logs` = ONLY .log files (execution logs from each step - stdout/stderr capture)
- `/plots` = EMPTY until rq_plots generates PNG/PDF visualizations
- `/results` = EMPTY until rq_results generates summary.md

**Data Files Created:**
- data/step00_lmm_input_raw.csv (from Step 0: merged theta, TSVR, Age - 400 rows x 7 columns)
- data/step01_lmm_input.csv (from Step 1: added Age_c - 400 rows x 8 columns)
- data/step02_lmm_input_with_time.csv (from Step 2: added time predictors - 400 rows x 8-10 columns)
- data/step03_lmm_summary.txt (from Step 3: full LMM output with fixed/random effects)
- data/step03_lmm_fixed_effects.csv (from Step 3: extracted fixed effects table - 3-7 rows)
- data/step04_age_effects.csv (from Step 4: Age_c and Time:Age_c effects with dual p-values - 2 rows)
- data/step05_effect_size_day6.csv (from Step 5: predicted difference at Day 6 - 1 row)
- data/step06_age_tertile_data.csv (from Step 6: aggregated means for tertile plot - 12 rows)

### Logs (ONLY execution logs - .log files capturing stdout/stderr)
- logs/step00_load_data.log
- logs/step01_center_age.log
- logs/step02_create_time_predictors.log
- logs/step03_fit_lmm.log
- logs/step04_extract_age_effects.log
- logs/step05_compute_effect_size.log
- logs/step06_prepare_tertile_data.log

### Plots (EMPTY until rq_plots runs)
- plots/age_tertile_trajectories.png (created by rq_plots, NOT analysis steps)
  - Source data: data/step06_age_tertile_data.csv
  - Plot type: Line plot with error bars (3 tertiles x 4 tests)

### Results (EMPTY until rq_results runs)
- results/summary.md (created by rq_results, summarizes age effects with Ch5 comparison)

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 -> Step 1:**
- Input: 3 separate CSVs (theta_confidence, tsvr_mapping, dfData)
- Transformation: Merge on composite_ID and UID
- Output: Single CSV with theta + TSVR + Age (wide format, 400 rows)

**Step 1 -> Step 2:**
- Input: Wide format with Age
- Transformation: Center Age (Age_c = Age - mean(Age))
- Output: Wide format with Age_c added (400 rows, 1 additional column)

**Step 2 -> Step 3:**
- Input: Wide format with Age_c
- Transformation: Create time predictors (Time, Time_log, or both based on RQ 6.1.1)
- Output: Wide format with time predictors (400 rows, 1-2 additional columns)

**Step 3 -> Step 4:**
- Input: Wide format LMM input (used for model fitting)
- Transformation: Extract fixed effects from fitted LMM object
- Output: Fixed effects table (narrow format, 3-7 rows x 5 columns)

**Step 4 -> Step 5:**
- Input: Fixed effects table
- Transformation: Filter to Age_c and Time:Age_c rows, add Bonferroni correction columns
- Output: Age effects table (2 rows x 8 columns)

**Step 5:**
- Input: Fixed effects coefficients + Age SD
- Transformation: Predict theta at +/- 1 SD Age_c for Day 6, compute difference
- Output: Effect size table (1 row x 7 columns)

**Step 6:**
- Input: Wide format LMM input
- Transformation: Assign age tertiles, aggregate by tertile x test
- Output: Aggregated means for plotting (12 rows x 7 columns)

### Column Naming Conventions

**Per names.md:**
- `composite_ID` - Primary key (format: UID_test, e.g., P001_T1)
- `UID` - Participant identifier (format: P### with leading zeros)
- `test` - Test session identifier (T1, T2, T3, T4)
- `TSVR_hours` - Time Since VR in hours (Decision D070 time variable)
- `theta_confidence` - IRT ability estimate for metacognitive monitoring
- `se_confidence` - Standard error of theta estimate
- `Age` - Participant age in years (original, uncentered)
- `Age_c` - Centered age (Age - mean(Age))
- `Time` - Time predictor (TSVR_hours or transformation thereof)
- `Time_log` - Log-transformed time (if used)
- `CI_lower`, `CI_upper` - 95% confidence interval bounds

### Data Type Constraints

**Nullable vs Non-Nullable:**
- **Non-nullable:** composite_ID, UID, test, theta_confidence, se_confidence, TSVR_hours, Age, Age_c, Time (all required for analysis)
- **No NaN tolerated** in any column after Step 0 merge (validation failure if missing)

**Valid Ranges:**
- theta_confidence in [-3, 3]
- se_confidence in [0.1, 1.0]
- TSVR_hours in [0, 200]
- Age in [18, 90]
- Age_c: approximately mean = 0 (tolerance |mean| < 0.001)

**Categorical Values:**
- test in {T1, T2, T3, T4}
- age_tertile in {Low, Medium, High}

---

## Cross-RQ Dependencies

**This RQ requires outputs from:**

**RQ 6.1.1** (Functional Form Comparison for Confidence)
- **File 1:** results/ch6/6.1.1/data/step03_theta_confidence.csv
  - Used in: Step 0 (primary dependent variable for LMM)
  - Content: IRT-derived theta confidence scores (400 rows: 100 participants x 4 tests)
  - Rationale: RQ 6.1.1 calibrates IRT model on 5-category ordinal confidence data. This RQ uses those theta estimates to test age moderation.

- **File 2:** results/ch6/6.1.1/data/step00_tsvr_mapping.csv
  - Used in: Step 0 (time variable for LMM per Decision D070)
  - Content: TSVR hours mapping (composite_ID, TSVR_hours, test)
  - Rationale: Actual hours since encoding (not nominal days 0/1/3/6) ensures accurate temporal modeling.

- **File 3:** RQ 6.1.1 functional form selection (from 2_plan.md or output file)
  - Used in: Step 2 (determine which time predictors to create)
  - Content: Selected time transformation (Time only, Time + Time_log, etc.)
  - Rationale: RQ 6.1.3 uses SAME functional form as RQ 6.1.1 for consistency across confidence trajectory analyses.

**Execution Order Constraint:**
1. RQ 6.1.1 must complete Steps 0-3 FIRST (provides theta_confidence.csv and tsvr_mapping.csv)
2. This RQ (6.1.3) executes AFTER RQ 6.1.1 completion (uses DERIVED data from 6.1.1)

**Data Source Boundaries:**
- **RAW data:** Age from data/cache/dfData.csv (project master demographics, not RQ-specific)
- **DERIVED data:** theta_confidence and TSVR from RQ 6.1.1 outputs
- **Scope:** This RQ does NOT re-calibrate IRT (uses RQ 6.1.1 theta estimates as given)

**Validation:**
- Step 0: Check results/ch6/6.1.1/data/step03_theta_confidence.csv exists (EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch6/6.1.1/data/step00_tsvr_mapping.csv exists (EXPECTATIONS ERROR if absent)
- Step 0: Check data/cache/dfData.csv exists and contains Age column (EXPECTATIONS ERROR if absent)
- If ANY dependency file missing -> quit with error -> user must execute RQ 6.1.1 first

**Comparison to Chapter 5:**
- Step 6 will document comparison to Ch5 RQ 5.1.3 (age effects on accuracy omnibus analysis)
- Expect parallel pattern: both accuracy and confidence show NULL Age x Time interaction (age-invariant decline)
- If divergent, suggests dissociation between memory and metacognition aging effects

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

**All validation requirements are embedded in the step-by-step plan above.**

Each step includes:
1. "Validation tools MUST be used after..." statement
2. Substance Validation Criteria (4 layers):
   - Output Files (paths, row counts, column counts, data types)
   - Value Ranges (scientifically reasonable bounds)
   - Data Quality (missing data tolerance, expected N, duplicate checks)
   - Log Validation (required patterns, forbidden patterns, acceptable warnings)
3. Expected Behavior on Validation Failure (quit, log, invoke g_debug)

**Per-Step Summary:**

| Step | Analysis | Validation Criteria Summary |
|------|----------|---------------------------|
| 0 | Data loading and merging | 400 rows, 7 columns, no NaN, all UIDs present, theta in [-3,3], Age in [18,90] |
| 1 | Age centering | Age_c mean ~= 0 (within 0.001), 400 rows, no NaN |
| 2 | Time predictors | Time predictors match RQ 6.1.1 functional form, no NaN, valid ranges |
| 3 | LMM fitting | Model converged, fixed effects table complete, Age_c and Time:Age_c terms present |
| 4 | Dual p-values | 2 rows (Age_c + interaction), p_uncorrected = p_bonferroni values, sig flags correct |
| 5 | Effect size | 1 row, predictions in [-3,3], older > younger age, TSVR ~= 144h |
| 6 | Tertile aggregation | 12 rows (3 tertiles x 4 tests), all tertiles present, no NaN, CI_upper > CI_lower |

**Validation Tool Selection:**
- rq_tools agent reads this table
- Selects appropriate validation functions from tool_inventory.md
- Pairs analysis tool + validation tool in 3_tools.yaml

**Error Handling:**
- Validation failure -> Step quits -> Logs error -> Invokes g_debug
- g_debug analyzes in sandbox -> Reports solution to master
- Master applies fix -> Re-runs step

---

## Summary

**Total Steps:** 6 (Step 0: data loading + Steps 1-5: LMM analysis and comparison)

**Estimated Runtime:** Medium (~15-30 minutes total)
- Step 0: Low (data loading, ~2-5 min)
- Step 1: Low (centering, <1 min)
- Step 2: Low (time predictors, <1 min)
- Step 3: Medium (LMM fitting, ~5-15 min depending on convergence)
- Step 4: Low (extraction, <1 min)
- Step 5: Low (effect size, ~2-5 min)
- Step 6: Low (tertile aggregation, ~2-5 min)

**Cross-RQ Dependencies:** RQ 6.1.1 (requires theta_confidence.csv, tsvr_mapping.csv, functional form selection)

**Primary Outputs:**
- data/step04_age_effects.csv (Age_c and Time:Age_c effects with dual p-values per Decision D068)
- data/step05_effect_size_day6.csv (predicted confidence difference at Day 6 between younger/older adults)
- data/step06_age_tertile_data.csv (plot source CSV for tertile comparison visualization)

**Validation Coverage:** 100% (all 6 steps have validation requirements with 4-layer substance criteria)

**Key Hypothesis Test:**
- Null: Age_c x Time interaction = 0 (age-invariant decline, paralleling Ch5 accuracy findings)
- Alternative: Age_c x Time interaction != 0 (differential decline rate by age)
- Expected: NULL (metacognitive monitoring parallels memory performance - both age-invariant in VR ecological encoding)

**Theoretical Significance:**
- If NULL: Validates VR ecological encoding framework (both memory and metacognition age-invariant)
- If significant: Suggests dissociation between memory and metacognitive aging effects

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 10 approval gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent for RQ 6.1.3 (Age Effects on Confidence)
