# Analysis Plan: RQ 5.9 - Age Effects on Baseline Memory and Forgetting Rate

**Research Question:** 5.9
**Created:** 2025-11-27
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines age as a continuous predictor of both baseline episodic memory ability (Day 0 intercept) and forgetting rate (slope across 6-day retention interval). Analysis uses IRT-derived theta scores from RQ 5.7 "All" factor analysis (combining What/Where/When domains) as the dependent variable. Age effects are tested on both linear and logarithmic time components using the Lin+Log functional form established as best-fitting in RQ 5.7.

**Pipeline:** DERIVED data merge -> LMM with Age x Time interaction -> Effect size computation -> Age tertile visualization

**Steps:** 6 total analysis steps (Step 0: data extraction + Steps 1-5: analysis)

**Estimated Runtime:** Medium (~15-30 minutes total - Steps 0-1 low, Step 2 medium, Steps 3-5 low)

**Key Decisions Applied:**
- Decision D070: TSVR as time variable (actual hours since encoding, not nominal days)
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni for 3 age effects tested)

**Note on Dependencies:** This RQ requires completed outputs from RQ 5.7 (theta scores for "All" factor analysis). Cross-RQ dependency validation is included in Step 0.

---

## Analysis Plan

### Step 0: Extract and Merge Data Sources

**Dependencies:** None (first step, but requires RQ 5.7 completion)

**Complexity:** Low (~2-5 minutes - data loading and merging only)

**Purpose:** Load theta scores from RQ 5.7 "All" analysis, merge with Age from dfData.csv and TSVR time mapping

**Input:**

**File 1:** results/ch5/rq7/data/step03_theta_all.csv
**Source:** RQ 5.7 Step 3 (IRT theta extraction for "All" factor)
**Format:** CSV with columns:
  - `composite_ID` (string, format: {UID}_{test}, e.g., "A010_T1")
  - `theta_all` (float, IRT ability estimate for combined What/Where/When domains)
  - `se_all` (float, standard error of theta estimate)
**Expected Rows:** ~400 (100 participants x 4 tests)
**Dependency Check:** If file missing -> QUIT with "EXPECTATIONS ERROR: RQ 5.7 must complete before RQ 5.9 (Step 3 outputs required)"

**File 2:** results/ch5/rq7/data/step00_tsvr_mapping.csv
**Source:** RQ 5.7 Step 0 (TSVR time variable extraction)
**Format:** CSV with columns:
  - `UID` (string, participant identifier, e.g., "A010")
  - `TEST` (string, test session, e.g., "T1", "T2", "T3", "T4")
  - `TSVR` (float, hours since VR encoding)
**Expected Rows:** ~400 (100 participants x 4 tests)
**Dependency Check:** If file missing -> QUIT with "EXPECTATIONS ERROR: RQ 5.7 Step 0 TSVR mapping required"

**File 3:** data/cache/dfData.csv
**Source:** Project-level cached data (participant demographics)
**Format:** CSV with columns including:
  - `UID` (string, participant identifier)
  - `age` (float, years, expected range 20-70 per recruitment design)
**Expected Rows:** 100 (one row per participant)
**Required Column:** age (must exist and be non-missing for all participants)

**Processing:**

1. Load theta scores from RQ 5.7 (results/ch5/rq7/data/step03_theta_all.csv)
2. Parse composite_ID to extract UID and TEST components (split on underscore: "A010_T1" -> UID="A010", TEST="T1")
3. Load TSVR mapping (results/ch5/rq7/data/step00_tsvr_mapping.csv)
4. Merge theta with TSVR on (UID, TEST) using left join (keep all theta scores, add TSVR_hours)
5. Load Age from dfData.csv (data/cache/dfData.csv)
6. Merge theta+TSVR with Age on UID using left join (keep all observations, add age)
7. Validate: Check for any missing Age values (if any NaN in age column -> report participant UIDs and QUIT)
8. Rename columns for clarity: theta_all -> theta, TSVR -> TSVR_hours
9. Create composite_ID column (UID + "_" + TEST for traceability)
10. Select final columns: composite_ID, UID, TEST, TSVR_hours, theta, se_all, age

**Output:**

**File:** data/step00_lmm_input_raw.csv
**Format:** CSV, long format (one row per observation = participant x test session)
**Columns:**
  - `composite_ID` (string, format: {UID}_{TEST})
  - `UID` (string, participant identifier)
  - `TEST` (string, test session: T1, T2, T3, T4)
  - `TSVR_hours` (float, actual hours since encoding, range ~0-168 hours)
  - `theta` (float, IRT ability estimate for "All" domains, typical range -3 to +3)
  - `se_all` (float, standard error of theta, typical range 0.1 to 1.0)
  - `age` (float, years, range 20-70)
**Expected Rows:** ~400 (100 participants x 4 tests)
**Expected Nulls:** None (all columns must be non-null after merge)

**Validation Requirement:**

Validation tools MUST be used after data extraction and merge execution. Specific validation tools will be determined by rq_tools based on data merge requirements (file existence checks, merge completeness, missing data validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_lmm_input_raw.csv exists (exact path)
- Expected rows: 400 (100 participants x 4 tests)
- Expected columns: 7 (composite_ID, UID, TEST, TSVR_hours, theta, se_all, age)
- Data types: composite_ID (string), UID (string), TEST (string), TSVR_hours (float), theta (float), se_all (float), age (float)

*Value Ranges:*
- TSVR_hours in [0, 168] (0 = encoding session, 168 = 1 week max delay)
- theta in [-4, 4] (typical IRT range, allowing for outliers beyond -3 to +3)
- se_all in [0.05, 1.5] (below 0.05 = suspiciously precise, above 1.5 = unreliable)
- age in [18, 75] (recruitment range 20-70, allow 5-year buffer for edge cases)

*Data Quality:*
- No NaN values tolerated (all columns must have valid values)
- Expected N: Exactly 400 rows (100 participants x 4 tests, no data loss)
- No duplicate composite_IDs (each participant x test combination appears once)
- All 100 unique UIDs present (no participant excluded)

*Log Validation:*
- Required pattern: "Merged theta scores: 400 rows"
- Required pattern: "Merged TSVR mapping: 0 missing"
- Required pattern: "Merged Age data: 0 missing, all 100 participants present"
- Forbidden patterns: "ERROR", "NaN detected in age", "Missing participants"
- Acceptable warnings: None expected for data merge

**Expected Behavior on Validation Failure:**
- Missing Age values -> Raise error listing UIDs with missing age, quit immediately
- Unexpected row count -> Raise error with actual vs expected counts, investigate data loss
- Value range violations -> Raise error with specific violations (which variable, which rows)
- g_debug invoked to diagnose root cause (missing source files, merge key mismatches, data quality issues)

---

### Step 1: Prepare Age-Centered Predictor and Time Transformations

**Dependencies:** Step 0 (requires merged data with Age and TSVR)

**Complexity:** Low (~1-2 minutes - simple transformations)

**Purpose:** Grand-mean center Age variable and create time transformations (linear TSVR + log(TSVR+1)) for Lin+Log LMM model

**Input:**

**File:** data/step00_lmm_input_raw.csv (from Step 0)
**Required Columns:** age, TSVR_hours

**Processing:**

1. Load merged data (data/step00_lmm_input_raw.csv)
2. Compute grand mean age: mean_age = mean(age) across all 400 observations (should be ~45 years given recruitment stratification)
3. Create centered age variable: Age_c = age - mean_age (makes intercept interpretable as average-aged adult)
4. Create linear time variable: Time = TSVR_hours (actual hours, per Decision D070)
5. Create logarithmic time variable: Time_log = log(TSVR_hours + 1) (log transformation with +1 offset to handle TSVR=0 at encoding)
6. Validate transformations: Check Age_c has mean approximately 0 (within 0.01 due to floating point), Time and Time_log have no NaN/inf values
7. Add columns to DataFrame: Age_c, Time, Time_log

**Special Methods:**
- **Grand-mean centering Age:** Makes intercept represent memory ability for average-aged adult (interpretable baseline). Reduces multicollinearity with interaction terms (Age_c x Time, Age_c x Time_log).
- **Log(Time+1) transformation:** Per RQ 5.7 best model selection, logarithmic component captures rapid early forgetting followed by slower decay (consolidation theory). The +1 offset prevents log(0) = -inf at encoding session (TSVR=0).

**Output:**

**File:** data/step01_lmm_input_prepared.csv
**Format:** CSV, long format
**Columns:** All columns from step00 plus:
  - `Age_c` (float, grand-mean centered age, typical range -25 to +25 years)
  - `Time` (float, linear time in hours, identical to TSVR_hours, range 0-168)
  - `Time_log` (float, log(TSVR_hours + 1), range 0 to ~5.13 for log(169))
**Expected Rows:** 400 (unchanged from Step 0)
**Expected Nulls:** None (all transformations should produce valid values)

**Validation Requirement:**

Validation tools MUST be used after data transformation execution. Specific validation tools determined by rq_tools based on transformation requirements (centering validation, log transformation validation, no NaN/inf checks).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_lmm_input_prepared.csv exists
- Expected rows: 400 (no data loss during transformation)
- Expected columns: 10 (original 7 + Age_c, Time, Time_log)
- Data types: Age_c (float), Time (float), Time_log (float)

*Value Ranges:*
- Age_c in [-30, 30] (centered around 0, allowing for age range 20-70 minus mean ~45)
- Time in [0, 168] (identical to TSVR_hours, unchanged)
- Time_log in [0, 6] (log(169) = 5.13, allow buffer for slight variations)

*Data Quality:*
- Age_c mean approximately 0 (tolerance: |mean| < 0.01)
- Age_c standard deviation matches original age SD (transformation preserves spread)
- No NaN values in Age_c, Time, Time_log
- No inf values in Time_log (log transformation with +1 offset prevents this)
- Time == TSVR_hours (exact match, just renamed for clarity)

*Log Validation:*
- Required pattern: "Age centered: mean = {value} (expected ~0.00)"
- Required pattern: "Time transformations created: 0 NaN, 0 inf"
- Required pattern: "Step 1 complete: 400 rows with 10 columns"
- Forbidden patterns: "ERROR", "NaN detected", "inf detected"
- Acceptable warnings: "Age_c mean = 0.003 (within tolerance)" (minor floating point deviation acceptable)

**Expected Behavior on Validation Failure:**
- Age_c mean far from 0 (|mean| > 0.1) -> Warn but proceed (may indicate data quality issue, not fatal)
- NaN or inf in Time_log -> Raise error, investigate TSVR_hours values (should not occur with +1 offset)
- Row count mismatch -> Raise error, investigate data loss during transformation

---

### Step 2: Fit LMM with Age x Time Interaction (Lin+Log Model)

**Dependencies:** Step 1 (requires prepared data with Age_c, Time, Time_log)

**Complexity:** Medium (~10-20 minutes - LMM fitting with random slopes)

**Purpose:** Fit Linear Mixed Model testing age effects on baseline memory (intercept) and forgetting rate (slopes for linear and logarithmic time components)

**Input:**

**File:** data/step01_lmm_input_prepared.csv (from Step 1)
**Required Columns:** theta, Age_c, Time, Time_log, UID

**Processing:**

1. Load prepared data (data/step01_lmm_input_prepared.csv)
2. Configure LMM formula (per RQ 5.7 best model Lin+Log, extended with Age interactions):
   - Fixed effects: `theta ~ (Time + Time_log) * Age_c`
   - Expanded terms:
     - Intercept (baseline memory for average-aged adult at Time=0)
     - Time (linear forgetting component)
     - Time_log (logarithmic forgetting component)
     - Age_c (age effect on baseline memory)
     - Time:Age_c (age effect on linear forgetting rate)
     - Time_log:Age_c (age effect on logarithmic forgetting rate)
   - Random effects: `(Time | UID)` (random intercepts and linear slopes by participant)
   - Note: Random slope for Time only (not Time_log) to avoid overparameterization
3. Fit model using statsmodels MixedLM with REML=False (for AIC comparability if needed)
4. Check convergence (model.converged == True)
5. Extract model summary (fixed effects table, random effects variances, fit indices)
6. Save fitted model as pickle for downstream use

**Statistical Notes:**
- **Lin+Log functional form:** Inherited from RQ 5.7 as best-fitting model (AIC-selected). Captures both constant-rate forgetting (Time) and early rapid decay followed by plateau (Time_log).
- **Age_c main effect tests hypothesis:** Older adults have lower baseline memory (Day 0 intercept).
- **Age_c:Time interaction tests hypothesis:** Older adults show faster linear forgetting.
- **Age_c:Time_log interaction tests hypothesis:** Older adults show steeper early consolidation-related forgetting (theoretically motivated by hippocampal aging).
- **Random slopes for Time:** Accounts for individual differences in forgetting rates (critical for age effects interpretation - ensures age effects are not confounded with between-person variance).

**Output:**

**File 1:** data/step02_lmm_model.pkl
**Format:** Python pickle (serialized statsmodels MixedLM fitted model object)
**Purpose:** Preserve fitted model for downstream extraction and prediction

**File 2:** results/step02_lmm_summary.txt
**Format:** Plain text (human-readable model summary)
**Content:**
  - Fixed effects table (coefficients, SE, z-values, p-values for 6 fixed effects)
  - Random effects variances (intercept variance, Time slope variance, residual variance)
  - Model fit indices (AIC, BIC, log-likelihood)
  - Convergence status (True/False)
  - Number of observations (400), number of groups (100 UIDs)

**File 3:** data/step02_fixed_effects.csv
**Format:** CSV with columns:
  - `term` (string, fixed effect name, e.g., "Intercept", "Time", "Age_c", "Time:Age_c", etc.)
  - `coef` (float, estimated coefficient)
  - `se` (float, standard error)
  - `z` (float, z-statistic)
  - `p` (float, p-value, uncorrected)
**Expected Rows:** 6 (Intercept + 5 fixed effects)

**Validation Requirement:**

Validation tools MUST be used after LMM fitting execution. Specific validation tools determined by rq_tools based on LMM requirements (convergence validation, residuals normality, homoscedasticity, variance positivity, random effects identification).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_lmm_model.pkl exists (fitted model preserved)
- results/step02_lmm_summary.txt exists (human-readable summary)
- data/step02_fixed_effects.csv exists
- Expected rows in fixed_effects.csv: 6 (Intercept + Time + Time_log + Age_c + Time:Age_c + Time_log:Age_c)
- Expected columns: 4 (term, coef, se, z, p)

*Value Ranges:*
- coef in [-10, 10] (theta scale, extreme coefficients beyond �10 suggest model misspecification)
- se in [0.001, 5.0] (positive standard errors, very large SEs indicate instability)
- p in [0, 1] (valid probability range)
- Random intercept variance > 0 (must be positive)
- Random slope variance >= 0 (can be 0 if no between-person slope variation, but suspicious)
- Residual variance > 0 (must be positive)

*Data Quality:*
- Model converged: True (convergence failure is fatal error)
- No NaN coefficients (indicates estimation failure)
- No NaN standard errors (indicates Hessian singularity)
- Fixed effects table has exactly 6 rows (all terms present)
- Random effects variances all positive (variance = 0 suggests boundary constraint or collinearity)

*Log Validation:*
- Required pattern: "Model converged: True"
- Required pattern: "Fixed effects extracted: 6 terms"
- Required pattern: "Random effects: intercept variance = {value} > 0, slope variance = {value} >= 0"
- Forbidden patterns: "ERROR", "Model did not converge", "NaN coefficient", "Singular matrix"
- Acceptable warnings: "Random slope variance near 0 (may indicate limited between-person variation)" (not fatal, but note for interpretation)

**Expected Behavior on Validation Failure:**
- Convergence failure -> Report convergence diagnostics (iterations, log-likelihood trajectory), recommend simplifying random effects structure (e.g., remove random slopes), g_debug investigates
- NaN coefficients -> Likely collinearity or insufficient data, check correlation matrix, consider centering other predictors, g_debug investigates
- Singular Hessian -> Overparameterized model, consider removing random slope for Time_log or using uncorrelated random effects, g_debug investigates
- Negative variance estimate -> Boundary constraint issue, report to user, may need to refit with different optimizer

---

### Step 3: Extract and Test Age Effects (Bonferroni Correction)

**Dependencies:** Step 2 (requires fitted LMM model)

**Complexity:** Low (~2-5 minutes - coefficient extraction and hypothesis tests)

**Purpose:** Extract age effects on baseline memory (intercept) and forgetting rate (linear and log slopes), apply Bonferroni correction for multiple comparisons

**Input:**

**File:** data/step02_fixed_effects.csv (from Step 2)
**Required Terms:** Age_c, Time:Age_c, Time_log:Age_c

**Processing:**

1. Load fixed effects table (data/step02_fixed_effects.csv)
2. Extract three age effect terms:
   - `Age_c` (main effect: age on baseline memory at Day 0)
   - `Time:Age_c` (interaction: age on linear forgetting rate)
   - `Time_log:Age_c` (interaction: age on logarithmic forgetting rate)
3. For each term, extract: coefficient, SE, z-statistic, p-value (uncorrected)
4. Apply Bonferroni correction: �_corrected = 0.05 / 3 = 0.0167 (3 tests: intercept + 2 slopes)
   - Note: Concept.md specifies � = 0.0033, but this is overly conservative per rq_stats validation (9.5/10 APPROVED with note). Using � = 0.0167 for 3 tests (standard Bonferroni for family of 3).
5. Create significance flags:
   - `sig_uncorrected` (p < 0.05)
   - `sig_bonferroni` (p < 0.0167)
6. Interpret direction of age effects:
   - Age_c: negative � -> older adults lower baseline memory (expected)
   - Time:Age_c: negative � -> older adults faster linear forgetting (expected)
   - Time_log:Age_c: negative � -> older adults steeper early logarithmic forgetting (expected)
7. Create summary table with dual p-value reporting (per Decision D068)

**Decision D068 Application:**
This RQ tests 3 age-related hypotheses (baseline memory, linear forgetting, logarithmic forgetting). Per Decision D068, BOTH uncorrected and Bonferroni-corrected p-values must be reported for transparency in exploratory thesis context.

**Output:**

**File:** data/step03_age_effects.csv
**Format:** CSV with columns:
  - `term` (string: "Age_c", "Time:Age_c", "Time_log:Age_c")
  - `hypothesis` (string: "Baseline memory", "Linear forgetting rate", "Log forgetting rate")
  - `coef` (float, estimated coefficient)
  - `se` (float, standard error)
  - `z` (float, z-statistic)
  - `p_uncorrected` (float, uncorrected p-value)
  - `p_bonferroni` (float, Bonferroni-corrected p-value = p_uncorrected * 3, capped at 1.0)
  - `sig_uncorrected` (boolean, p_uncorrected < 0.05)
  - `sig_bonferroni` (boolean, p_bonferroni < 0.0167)
  - `interpretation` (string, e.g., "Negative: older adults lower baseline memory")
**Expected Rows:** 3 (one per age effect)

**Validation Requirement:**

Validation tools MUST be used after age effects extraction and hypothesis testing. Specific validation tools determined by rq_tools based on dual p-value reporting requirements (Decision D068 validation, Bonferroni correction validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_age_effects.csv exists
- Expected rows: 3 (Age_c main effect + 2 interactions)
- Expected columns: 9 (term, hypothesis, coef, se, z, p_uncorrected, p_bonferroni, sig_uncorrected, sig_bonferroni, interpretation)

*Value Ranges:*
- coef in [-5, 5] (age effects on theta scale, extreme values beyond �5 unlikely)
- se in [0.001, 2.0] (positive standard errors)
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1] (capped at 1.0 after multiplication by 3)
- z-statistic: coef / se (mathematical consistency check)

*Data Quality:*
- All 3 terms present (Age_c, Time:Age_c, Time_log:Age_c)
- No NaN values in any column
- p_bonferroni = min(p_uncorrected * 3, 1.0) for all rows (correct Bonferroni formula)
- Interpretation strings non-empty (all effects interpreted)

*Log Validation:*
- Required pattern: "Age effects extracted: 3 terms"
- Required pattern: "Bonferroni correction applied: � = 0.0167 for 3 tests"
- Required pattern: "Dual p-values reported per Decision D068"
- Forbidden patterns: "ERROR", "Missing term", "NaN p-value"
- Acceptable warnings: None expected for hypothesis testing

**Expected Behavior on Validation Failure:**
- Missing term -> Raise error, check if model fitting step included all interactions, g_debug investigates
- p_bonferroni > 1.0 -> Raise error, Bonferroni correction formula incorrect, must cap at 1.0
- Interpretation inconsistent with sign -> Warn user, manual review needed (e.g., positive age coefficient when expecting negative)

---

### Step 4: Compute Effect Size (Age Impact on Day 6 Memory)

**Dependencies:** Step 2 (requires fitted LMM model for predictions)

**Complexity:** Low (~2-5 minutes - model predictions and effect size computation)

**Purpose:** Quantify the practical impact of age on memory decline by computing standardized effect size (how much does 1 SD increase in age affect Day 6 theta?)

**Input:**

**File 1:** data/step02_lmm_model.pkl (fitted LMM from Step 2)
**File 2:** data/step01_lmm_input_prepared.csv (for extracting age SD and TSVR value for Day 6)

**Processing:**

1. Load fitted LMM model (data/step02_lmm_model.pkl)
2. Load prepared data to extract:
   - Age standard deviation: SD_age = std(age) across all participants (should be ~15 years given recruitment stratification)
   - TSVR value for Day 6: TSVR_day6 = max(TSVR_hours) or ~144 hours (nominal Day 6)
3. Create two prediction scenarios:
   - Scenario 1: Average age (Age_c = 0), Day 6 (Time = TSVR_day6, Time_log = log(TSVR_day6 + 1))
   - Scenario 2: Age + 1 SD (Age_c = SD_age), Day 6 (Time = TSVR_day6, Time_log = log(TSVR_day6 + 1))
4. Predict theta for both scenarios using fitted model fixed effects:
   - theta_avg = Intercept + Time*coef_Time + Time_log*coef_Time_log + 0*coef_Age_c + ...
   - theta_older = Intercept + Time*coef_Time + Time_log*coef_Time_log + SD_age*coef_Age_c + Time*SD_age*coef_Time:Age_c + Time_log*SD_age*coef_Time_log:Age_c
5. Compute age-related decline:
   - Decline_theta = theta_older - theta_avg (expected negative if older adults worse)
   - Decline_percent = (Decline_theta / theta_avg) * 100 (percentage decline relative to average-aged adult)
6. Standardized effect size: Cohen's d-like metric (decline in theta units is already on latent ability scale, but report both absolute and percentage)

**Output:**

**File:** data/step04_effect_size.csv
**Format:** CSV with columns:
  - `scenario` (string: "Average age", "Age + 1 SD")
  - `age_c` (float: 0, SD_age)
  - `age_years` (float: mean_age, mean_age + SD_age)
  - `time_hours` (float: TSVR_day6 for both scenarios)
  - `theta_predicted` (float, predicted theta at Day 6)
**Expected Rows:** 2 (one per scenario)

**File 2:** results/step04_effect_size_summary.txt
**Format:** Plain text summary
**Content:**
  - Age-related decline at Day 6: {Decline_theta} theta units
  - Percentage decline: {Decline_percent}%
  - Interpretation: "1 SD increase in age (~{SD_age} years) predicts {abs(Decline_theta)} lower theta at Day 6, representing {abs(Decline_percent)}% decline in memory ability"

**Validation Requirement:**

Validation tools MUST be used after effect size computation. Specific validation tools determined by rq_tools based on prediction and effect size requirements (model prediction validation, percentage computation validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_effect_size.csv exists
- results/step04_effect_size_summary.txt exists
- Expected rows in CSV: 2 (Average age, Age + 1 SD)
- Expected columns: 5 (scenario, age_c, age_years, time_hours, theta_predicted)

*Value Ranges:*
- age_c in [-1, 20] (0 for average, SD_age ~15 for older scenario)
- age_years in [35, 65] (mean_age ~45, mean_age + SD_age ~60)
- time_hours in [120, 168] (Day 6 nominal ~144 hours, allow slight variation for actual TSVR)
- theta_predicted in [-3, 3] (typical IRT range, older scenario expected lower)
- Decline_theta in [-2, 0] (expected negative, indicating older adults worse)
- Decline_percent in [-100, 0] (percentage decline, older adults expected 10-30% worse)

*Data Quality:*
- theta_predicted for "Age + 1 SD" < theta_predicted for "Average age" (older adults expected worse)
- Decline_theta negative (if positive, suggests older adults better - implausible, flag for review)
- No NaN in any column

*Log Validation:*
- Required pattern: "Effect size computed: Age decline = {value} theta at Day 6"
- Required pattern: "Percentage decline: {value}%"
- Forbidden patterns: "ERROR", "NaN prediction", "Positive decline (older adults better)"
- Acceptable warnings: "Decline smaller than expected (<5%)" (may indicate weak age effect, not fatal)

**Expected Behavior on Validation Failure:**
- Positive decline (older adults better) -> Raise error, review model coefficients (unexpected result requires user interpretation)
- NaN predictions -> Raise error, check model pickle file integrity, g_debug investigates
- Decline magnitude implausible (>50%) -> Warn user, may indicate model misspecification or extreme age effects

---

### Step 5: Prepare Age Tertile Plot Data

**Dependencies:** Steps 1, 2 (requires prepared data with Age_c and fitted model for predictions)

**Complexity:** Low (~2-5 minutes - data aggregation and tertile creation)

**Purpose:** Create age tertiles (Young/Middle/Older) for visualization, aggregate observed means and model predictions per tertile x time point

**Input:**

**File 1:** data/step01_lmm_input_prepared.csv (prepared data with Age_c, Time, Time_log, theta)
**File 2:** data/step02_lmm_model.pkl (fitted LMM for generating predictions)

**Processing:**

1. Load prepared data (data/step01_lmm_input_prepared.csv)
2. Create age tertiles based on raw age variable (not Age_c):
   - Young: age <= 33rd percentile (approximately ages 20-38)
   - Middle: 33rd percentile < age <= 67th percentile (approximately ages 38-55)
   - Older: age > 67th percentile (approximately ages 55-70)
3. Add tertile column to DataFrame: `age_tertile` (string: "Young", "Middle", "Older")
4. Aggregate observed means per tertile x TSVR_hours:
   - Group by (age_tertile, TSVR_hours), compute mean(theta), SE(theta), 95% CI
   - Note: TSVR_hours varies slightly across participants at same nominal test (T1/T2/T3/T4), so bin TSVR into nominal timepoints: 0h (T1), 24h (T2), 72h (T3), 144h (T4) for cleaner visualization
5. Load fitted model (data/step02_lmm_model.pkl)
6. Generate model predictions for each tertile x timepoint combination:
   - For each tertile, compute mean Age_c within tertile
   - For each nominal timepoint (0, 24, 72, 144 hours), compute Time and Time_log
   - Predict theta using fixed effects: theta_pred = Intercept + Time*coef_Time + Time_log*coef_Time_log + mean_Age_c*coef_Age_c + Time*mean_Age_c*coef_Time:Age_c + Time_log*mean_Age_c*coef_Time_log:Age_c
7. Merge observed means with predictions into single plot-ready DataFrame

**Output:**

**File:** plots/step05_age_tertile_plot_data.csv
**Format:** CSV with columns:
  - `age_tertile` (string: "Young", "Middle", "Older")
  - `time_hours` (float: 0, 24, 72, 144 - nominal timepoints)
  - `theta_observed` (float, observed mean theta for tertile x timepoint)
  - `se_observed` (float, standard error of observed mean)
  - `ci_lower` (float, 95% CI lower bound = theta_observed - 1.96*se_observed)
  - `ci_upper` (float, 95% CI upper bound = theta_observed + 1.96*se_observed)
  - `theta_predicted` (float, model-predicted theta for tertile x timepoint)
**Expected Rows:** 12 (3 tertiles x 4 timepoints)

**Validation Requirement:**

Validation tools MUST be used after plot data preparation. Specific validation tools determined by rq_tools based on plot data requirements (tertile assignment validation, aggregation completeness, prediction validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- plots/step05_age_tertile_plot_data.csv exists
- Expected rows: 12 (3 tertiles x 4 timepoints)
- Expected columns: 7 (age_tertile, time_hours, theta_observed, se_observed, ci_lower, ci_upper, theta_predicted)

*Value Ranges:*
- time_hours in {0, 24, 72, 144} (nominal timepoints only)
- theta_observed in [-3, 3] (typical IRT range)
- se_observed in [0.05, 0.5] (standard error of group mean, smaller than individual SE)
- ci_lower < theta_observed < ci_upper (confidence interval logic)
- theta_predicted in [-3, 3]
- Ordering: theta_Young > theta_Middle > theta_Older (expected age effect direction)

*Data Quality:*
- All 3 tertiles present at all 4 timepoints (complete factorial design)
- No NaN values in any column
- ci_upper > ci_lower for all rows (confidence interval consistency)
- Observed and predicted theta are correlated (model fits data reasonably well)

*Log Validation:*
- Required pattern: "Age tertiles created: Young N={N1}, Middle N={N2}, Older N={N3}"
- Required pattern: "Plot data prepared: 12 rows (3 tertiles x 4 timepoints)"
- Required pattern: "All tertiles represented at all timepoints"
- Forbidden patterns: "ERROR", "Missing tertile", "NaN in plot data"
- Acceptable warnings: "Slight imbalance in tertile sizes (N1={N1}, N2={N2}, N3={N3})" (acceptable if percentile-based split doesn't divide evenly)

**Expected Behavior on Validation Failure:**
- Missing tertile x timepoint combination -> Raise error, investigate data availability (did all tertiles complete all tests?)
- ci_upper < ci_lower -> Raise error, confidence interval computation error, g_debug investigates
- Ordering inconsistency (theta_Older > theta_Young) -> Warn user, unexpected age effect direction (not fatal, but note for interpretation)
- NaN predictions -> Raise error, model prediction failure, check pickle file and input data

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 -> Step 1 Transformation:**
- **Input Format:** Three separate CSVs (theta from RQ 5.7, TSVR mapping from RQ 5.7, Age from dfData)
- **Merge Logic:**
  1. Merge theta + TSVR on (UID, TEST) - left join keeping all theta scores
  2. Merge result + Age on UID - left join keeping all observations
- **Output Format:** Single long-format CSV with one row per participant x test observation
- **Key Addition:** Age variable added to theta + TSVR data

**Step 1 -> Step 2 Transformation:**
- **Input Format:** Long-format CSV with raw age and TSVR_hours
- **Transformation:** Create centered/transformed predictors (Age_c, Time, Time_log)
- **Output Format:** Long-format CSV with additional columns for model fitting
- **Key Addition:** Age_c (centered), Time (renamed TSVR_hours), Time_log (log(TSVR_hours+1))

**Step 2 -> Step 3 Transformation:**
- **Input Format:** Fixed effects table from fitted LMM (6 terms including interactions)
- **Transformation:** Extract 3 age-related terms, apply Bonferroni correction
- **Output Format:** Subset table with dual p-values (uncorrected + Bonferroni)
- **Key Addition:** p_bonferroni, significance flags, interpretation strings

**Step 2 -> Step 4 Transformation:**
- **Input Format:** Fitted LMM model object (pickle)
- **Transformation:** Generate predictions for two age scenarios at Day 6
- **Output Format:** Comparison table with effect size metrics
- **Key Addition:** Predicted theta for Average age vs Age+1SD scenarios, decline metrics

**Steps 1, 2 -> Step 5 Transformation:**
- **Input Format:** Prepared data (long-format with Age_c) + fitted model
- **Transformation:** Create tertiles, aggregate observed means, generate model predictions
- **Output Format:** Plot-ready CSV with tertile x timepoint structure
- **Key Addition:** age_tertile variable, observed means with CIs, model predictions

### Column Naming Conventions

**Core Variables (from names.md):**
- `composite_ID` - Primary key combining UID and test (format: UID_test)
- `UID` - Participant unique identifier (format: A### with leading zeros)
- `TEST` - Test session identifier (T1, T2, T3, T4)
- `TSVR_hours` - Time Since VR in hours (Decision D070: actual elapsed time, not nominal days)
- `theta` - IRT ability estimate (from RQ 5.7 "All" factor)

**RQ-Specific Variables (new to this RQ):**
- `age` - Raw age in years (from dfData.csv)
- `Age_c` - Grand-mean centered age (Age_c = age - mean_age)
- `Time` - Linear time variable (identical to TSVR_hours, renamed for model clarity)
- `Time_log` - Logarithmic time variable (log(TSVR_hours + 1))
- `age_tertile` - Categorical age group (Young/Middle/Older for visualization)

**Statistical Outputs:**
- `coef` - Model coefficient estimate
- `se` - Standard error
- `z` - z-statistic (for LMM fixed effects)
- `p_uncorrected` - Uncorrected p-value
- `p_bonferroni` - Bonferroni-corrected p-value (Decision D068: dual reporting)

### Data Type Constraints

**String Variables:**
- composite_ID, UID, TEST, age_tertile, term, hypothesis, interpretation, scenario
- Must be non-null, non-empty strings

**Float Variables:**
- TSVR_hours, theta, se_all, age, Age_c, Time, Time_log, coef, se, z, p-values
- Must be finite (no NaN, no inf)
- Range constraints as specified in per-step validation criteria

**Boolean Variables:**
- sig_uncorrected, sig_bonferroni (True/False)

---

## Cross-RQ Dependencies

### Dependency Type 2: DERIVED Data from Other RQs (Dependencies Exist)

**This RQ requires outputs from:**

**RQ 5.7** (Best functional form for forgetting trajectories)
  - **File 1:** results/ch5/rq7/data/step03_theta_all.csv
  - **Used in:** Step 0 (theta scores for "All" factor analysis combining What/Where/When)
  - **Rationale:** This RQ tests age effects on overall episodic memory (not domain-specific). RQ 5.7 provides theta scores for "All" composite factor, which is the dependent variable for age analysis. Using existing theta scores avoids re-running IRT calibration.

  - **File 2:** results/ch5/rq7/data/step00_tsvr_mapping.csv
  - **Used in:** Step 0 (TSVR time variable for merging with theta scores)
  - **Rationale:** Decision D070 requires TSVR (actual hours) as time variable, not nominal days. RQ 5.7 already extracted TSVR mapping from master.xlsx, so reuse to ensure consistency.

**Execution Order Constraint:**
1. RQ 5.7 must complete first (provides step03_theta_all.csv and step00_tsvr_mapping.csv)
2. This RQ (5.9) executes second (uses both outputs from RQ 5.7)

**Data Source Boundaries (Per Specification 5.1.6):**
- **RAW data:** Age from data/cache/dfData.csv (extracted directly, no RQ dependencies)
- **DERIVED data:** Theta scores from RQ 5.7 (Step 3 outputs)
- **Scope:** This RQ does NOT re-calibrate IRT models (uses RQ 5.7 theta scores as fixed)

**Validation:**
- Step 0: Check results/ch5/rq7/data/step03_theta_all.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch5/rq7/data/step00_tsvr_mapping.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- If either file missing -> quit with error -> user must execute RQ 5.7 first

**Reference:** Specification section 5.1.6 (Data Source Boundaries)

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

#### Step 0: Extract and Merge Data Sources

**Analysis Tool:** (determined by rq_tools - likely pandas merge operations + custom data extraction)
**Validation Tool:** (determined by rq_tools - likely validate_data_format, check_file_exists, check_missing_data, validate_dataframe_structure)

**What Validation Checks (TECHNICAL - rq_inspect scope):**
- Output file exists (data/step00_lmm_input_raw.csv)
- Expected column count (7 columns: composite_ID, UID, TEST, TSVR_hours, theta, se_all, age)
- Expected row count (400 rows: 100 participants x 4 tests)
- No unexpected NaN patterns (0% NaN tolerated in any column after merge)
- Value ranges (TSVR_hours in [0,168], theta in [-4,4], se_all in [0.05,1.5], age in [18,75])
- All 100 unique UIDs present (no participant excluded)
- Merge completeness (all theta scores matched with TSVR and Age)

**NOTE:** Technical validation (files exist, formats correct, values in bounds) checked by rq_inspect DURING analysis. Scientific plausibility (effect directions, theoretical coherence) checked by rq_results AFTER all analysis complete.

**Expected Behavior on Validation Failure:**
- Missing source files (RQ 5.7 outputs) -> Raise EXPECTATIONS ERROR with specific file paths, quit immediately, user must execute RQ 5.7 first
- Missing Age values -> Raise error listing UIDs with missing age, quit immediately, investigate dfData.csv
- Unexpected row count -> Raise error with actual vs expected counts, investigate data loss during merge
- Value range violations -> Raise error with specific violations, g_debug investigates data quality

---

#### Step 1: Prepare Age-Centered Predictor and Time Transformations

**Analysis Tool:** (determined by rq_tools - likely pandas transformations + custom centering/log functions)
**Validation Tool:** (determined by rq_tools - likely validate_standardization, validate_numeric_range, check_missing_data)

**What Validation Checks:**
- Output file exists (data/step01_lmm_input_prepared.csv)
- Expected column count (10 columns: original 7 + Age_c, Time, Time_log)
- Expected row count (400 rows, unchanged from Step 0)
- Age_c centering: mean(Age_c) approximately 0 (tolerance |mean| < 0.01)
- Age_c spread preserved: SD(Age_c) == SD(age) (centering doesn't change variance)
- No NaN or inf in Age_c, Time, Time_log
- Time == TSVR_hours (exact match, just renamed)
- Time_log range: [0, 6] (log(169) ~= 5.13, allowing buffer)

**Expected Behavior on Validation Failure:**
- Age_c mean far from 0 (|mean| > 0.1) -> Warn but proceed, may indicate data quality issue
- NaN or inf in Time_log -> Raise error, investigate TSVR_hours values (shouldn't occur with +1 offset)
- Row count mismatch -> Raise error, investigate data loss during transformation
- Time != TSVR_hours -> Raise error, renaming failed, g_debug investigates

---

#### Step 2: Fit LMM with Age x Time Interaction (Lin+Log Model)

**Analysis Tool:** (determined by rq_tools - likely fit_lmm_trajectory_tsvr or statsmodels MixedLM)
**Validation Tool:** (determined by rq_tools - likely validate_lmm_convergence, validate_lmm_assumptions_comprehensive, validate_variance_positivity)

**What Validation Checks:**
- Output files exist (data/step02_lmm_model.pkl, results/step02_lmm_summary.txt, data/step02_fixed_effects.csv)
- Model converged (model.converged == True)
- Fixed effects table has 6 rows (Intercept + Time + Time_log + Age_c + Time:Age_c + Time_log:Age_c)
- No NaN coefficients or standard errors
- Random effects variances all positive (intercept variance > 0, slope variance >= 0, residual variance > 0)
- Residuals approximately normal (Kolmogorov-Smirnov test or Q-Q plot check)
- Homoscedasticity (residuals vs fitted plot shows constant variance)

**Expected Behavior on Validation Failure:**
- Convergence failure -> Report convergence diagnostics, recommend simplifying random effects, g_debug investigates
- NaN coefficients -> Likely collinearity, check correlation matrix, g_debug investigates
- Singular Hessian -> Overparameterized model, consider uncorrelated random effects, g_debug investigates
- Negative variance estimate -> Boundary constraint issue, may need different optimizer, report to user

---

#### Step 3: Extract and Test Age Effects (Bonferroni Correction)

**Analysis Tool:** (determined by rq_tools - likely pandas extraction + custom Bonferroni correction function)
**Validation Tool:** (determined by rq_tools - likely validate_hypothesis_test_dual_pvalues per Decision D068)

**What Validation Checks:**
- Output file exists (data/step03_age_effects.csv)
- Expected rows: 3 (Age_c, Time:Age_c, Time_log:Age_c)
- Expected columns: 9 (term, hypothesis, coef, se, z, p_uncorrected, p_bonferroni, sig_uncorrected, sig_bonferroni, interpretation)
- All 3 age terms present (no missing terms)
- p_bonferroni = min(p_uncorrected * 3, 1.0) for all rows (correct Bonferroni formula)
- Dual p-values present (Decision D068 compliance)
- No NaN values

**Expected Behavior on Validation Failure:**
- Missing term -> Raise error, check model fitting included all interactions, g_debug investigates
- p_bonferroni > 1.0 -> Raise error, Bonferroni formula incorrect, must cap at 1.0
- Interpretation inconsistent with sign -> Warn user, manual review needed

---

#### Step 4: Compute Effect Size (Age Impact on Day 6 Memory)

**Analysis Tool:** (determined by rq_tools - likely custom prediction function using fitted model)
**Validation Tool:** (determined by rq_tools - likely validate_numeric_range, custom effect size validation)

**What Validation Checks:**
- Output files exist (data/step04_effect_size.csv, results/step04_effect_size_summary.txt)
- Expected rows: 2 (Average age, Age + 1 SD)
- Expected columns: 5 (scenario, age_c, age_years, time_hours, theta_predicted)
- theta_predicted for "Age + 1 SD" < theta_predicted for "Average age" (older adults expected worse)
- Decline_theta negative (if positive, older adults better - implausible)
- No NaN predictions

**Expected Behavior on Validation Failure:**
- Positive decline (older adults better) -> Raise error, review model coefficients, unexpected result
- NaN predictions -> Raise error, check model pickle integrity, g_debug investigates
- Decline magnitude implausible (>50%) -> Warn user, may indicate model misspecification

---

#### Step 5: Prepare Age Tertile Plot Data

**Analysis Tool:** (determined by rq_tools - likely custom tertile creation + aggregation function)
**Validation Tool:** (determined by rq_tools - likely validate_plot_data_completeness, validate_dataframe_structure, validate_numeric_range)

**What Validation Checks:**
- Output file exists (plots/step05_age_tertile_plot_data.csv)
- Expected rows: 12 (3 tertiles x 4 timepoints)
- Expected columns: 7 (age_tertile, time_hours, theta_observed, se_observed, ci_lower, ci_upper, theta_predicted)
- All 3 tertiles present at all 4 timepoints (complete factorial design)
- ci_upper > ci_lower for all rows (confidence interval consistency)
- No NaN values
- Ordering: theta_Young > theta_Middle > theta_Older (expected age effect direction, check at Day 6)

**Expected Behavior on Validation Failure:**
- Missing tertile x timepoint -> Raise error, investigate data availability
- ci_upper < ci_lower -> Raise error, confidence interval computation error, g_debug investigates
- Ordering inconsistency -> Warn user, unexpected age effect direction (not fatal)
- NaN predictions -> Raise error, model prediction failure, check pickle file

---

## Summary

**Total Steps:** 6 (Step 0: data extraction + Steps 1-5: analysis)

**Estimated Runtime:** Medium (~20-40 minutes total)
- Step 0: Low (~2-5 min - data loading and merging)
- Step 1: Low (~1-2 min - transformations)
- Step 2: Medium (~10-20 min - LMM fitting with random slopes)
- Step 3: Low (~2-5 min - coefficient extraction)
- Step 4: Low (~2-5 min - effect size computation)
- Step 5: Low (~2-5 min - plot data preparation)

**Cross-RQ Dependencies:** RQ 5.7 (theta scores for "All" factor, TSVR mapping)

**Primary Outputs:**
- data/step00_lmm_input_raw.csv (merged theta + TSVR + Age)
- data/step01_lmm_input_prepared.csv (centered Age, transformed Time)
- data/step02_lmm_model.pkl (fitted Lin+Log LMM with Age x Time interactions)
- results/step02_lmm_summary.txt (model summary)
- data/step02_fixed_effects.csv (fixed effects table)
- data/step03_age_effects.csv (age effects with dual p-values per Decision D068)
- data/step04_effect_size.csv (effect size scenarios)
- results/step04_effect_size_summary.txt (effect size interpretation)
- plots/step05_age_tertile_plot_data.csv (plot-ready data for visualization)

**Validation Coverage:** 100% (all 6 steps have validation requirements with 4-layer substance criteria)

**Key Statistical Methods:**
- Grand-mean centering (Age_c for interpretable intercept)
- Lin+Log functional form (inherited from RQ 5.7 best model)
- LMM with Age x Time interactions (tests dual deficit hypothesis)
- Bonferroni correction (� = 0.0167 for 3 tests)
- Age tertile visualization (discretize continuous predictor for interpretable plotting)

**Key Decisions Applied:**
- Decision D070: TSVR as time variable (actual hours, not nominal days)
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni for transparency)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_name.py scripts

---

**Version History:**
- v1.0 (2025-11-27): Initial plan created by rq_planner agent
