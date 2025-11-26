# Analysis Plan for RQ 5.9: Does age affect baseline memory ability or forgetting rate?

**Created by:** rq_planner agent
**Date:** 2025-11-26
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This RQ examines age as a continuous predictor of both baseline episodic memory ability (Day 0 intercept) and forgetting rate (slope across 6-day retention interval). Analysis uses IRT-derived theta scores from RQ 5.7's "All" composite factor (What/Where/When combined) as the dependent variable. Age effects are tested on both linear and logarithmic time components using Lin+Log functional form (best model from RQ 5.7). Time variable uses TSVR (actual hours since encoding per Decision D070).

**Pipeline:** LMM only (no IRT - reuses theta scores from RQ 5.7)
**Steps:** 6 total (Step 0: data merge + Steps 1-5: LMM analysis and effect computation)
**Estimated Runtime:** Medium (~10-20 minutes total - primarily LMM fitting)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting for 3 Age effects (intercept, Age x Time, Age x log(Time+1)) - Bonferroni alpha = 0.0033
- Decision D070: TSVR as time variable (inherited from RQ 5.7, actual hours not nominal days)
- Grand-mean centering Age: Makes intercept interpretable as average-aged adult memory

**Cross-RQ Dependencies:**
- RQ 5.7 must complete Steps 0-3 (theta extraction for "All" composite factor)

---

## Analysis Plan

### Step 0: Merge RQ 5.7 Theta with Age and TSVR

**Purpose:** Combine theta scores from RQ 5.7 "All" analysis with Age variable and TSVR time mapping

**Dependencies:** None (first step)
**Complexity:** Low (<5 minutes - data merging only)

**Input:**

**File 1:** results/ch5/rq7/data/step03_theta_all.csv (DERIVED from RQ 5.7)
**Source:** RQ 5.7 Step 3 (IRT theta extraction for "All" composite factor)
**Format:** CSV with columns:
  - composite_ID (string, format: UID_TEST, e.g., P001_T1)
  - theta (float, IRT ability estimate for combined What/Where/When)
  - se (float, standard error of theta)
**Expected Rows:** ~400 (100 participants x 4 tests)

**File 2:** results/ch5/rq7/data/step00_tsvr_mapping.csv (DERIVED from RQ 5.7)
**Source:** RQ 5.7 Step 0 (TSVR extraction)
**Format:** CSV with columns:
  - UID (string, participant ID, e.g., P001)
  - TEST (string, test session, e.g., T1, T2, T3, T4)
  - TSVR (float, hours since encoding)
**Expected Rows:** ~400 (100 participants x 4 tests)

**File 3:** data/cache/dfData.csv (RAW data source)
**Source:** Project-level participant data file
**Format:** CSV with columns (subset used):
  - UID (string, participant ID, e.g., P001)
  - age (float, participant age in years at study enrollment)
**Expected Rows:** 100 (one row per participant)

**Processing:**

1. Load theta scores from RQ 5.7 (composite_ID, theta, se)
2. Parse composite_ID to extract UID and TEST (split on underscore)
3. Merge with TSVR mapping on UID + TEST (left join - all theta scores retained)
4. Merge with Age from dfData.csv on UID (left join - add Age column)
5. Verify no missing values:
   - All composite_IDs successfully parsed to UID + TEST
   - All UID + TEST matched in TSVR mapping (no NaN TSVR values)
   - All UIDs matched in dfData.csv (no NaN Age values)
6. Create composite_ID column for tracking: UID_TEST format
7. Select final columns: UID, TEST, TSVR, theta, se, age
8. Sort by UID, then TSVR (chronological order per participant)

**Output:**

**File:** data/step00_lmm_input_raw.csv
**Format:** CSV, long format (one row per measurement occasion)
**Columns:**
  - UID (string, participant ID)
  - TEST (string, test session: T1, T2, T3, T4)
  - TSVR (float, hours since encoding)
  - theta (float, IRT ability estimate from RQ 5.7 "All" factor)
  - se (float, standard error of theta)
  - age (float, participant age in years)
**Expected Rows:** ~400 (100 participants x 4 tests)
**Expected Columns:** 6

**Validation Requirement:**
Validation tools MUST be used after data merge execution. Specific validation tools will be determined by rq_tools based on data format requirements. The rq_analysis agent will embed validation tool calls after the merge operation for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_lmm_input_raw.csv exists (exact path)
- Expected rows: 400 (100 participants x 4 tests)
- Expected columns: 6 (UID, TEST, TSVR, theta, se, age)
- Data types: UID (object), TEST (object), TSVR (float64), theta (float64), se (float64), age (float64)

*Value Ranges:*
- TSVR in [0, 200] hours (0 = encoding, ~168 = 7 days maximum observed)
- theta in [-3, 3] (typical IRT ability range)
- se in [0.1, 1.0] (standard errors above 1.0 indicate unreliable estimates)
- age in [18, 90] years (adult participant range)

*Data Quality:*
- No NaN values allowed in any column (all merges must succeed)
- Expected N: Exactly 400 rows (100 participants x 4 tests, no data loss)
- UID format: P### (3 digits with leading zeros, e.g., P001 not P1)
- TEST values: Must be in {T1, T2, T3, T4} (no other values allowed)
- No duplicate UID x TEST combinations (each participant-test unique)

*Log Validation:*
- Required pattern: "Merge complete: 400 rows created"
- Required pattern: "No missing values detected in TSVR or age columns"
- Required pattern: "All 100 participants have 4 test sessions"
- Forbidden patterns: "ERROR", "NaN values detected", "Missing Age for UID"
- Acceptable warnings: None expected for data merge

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Missing Age for 5 participants")
- Log failure to logs/step00_merge_rq7_theta_age.log
- Quit script immediately (do NOT proceed to Step 1)
- Check RQ 5.7 completion status (theta file exists?)
- Check dfData.csv for missing Age values

---

### Step 1: Prepare Age Predictor (Grand-Mean Centering)

**Purpose:** Grand-mean center Age variable to make intercept interpretable as average-aged adult memory

**Dependencies:** Step 0 (requires merged data with Age column)
**Complexity:** Low (<1 minute - simple transformation)

**Input:**

**File:** data/step00_lmm_input_raw.csv
**Source:** Generated by Step 0
**Format:** CSV with columns: UID, TEST, TSVR, theta, se, age
**Expected Rows:** ~400

**Processing:**

1. Load merged data from Step 0
2. Compute grand mean of Age across all participants:
   - Age_mean = mean(unique age values per UID)
   - Note: Each participant has same Age value across 4 tests, so compute mean on unique UIDs only
3. Create centered Age variable:
   - Age_c = age - Age_mean
   - This makes Age_c = 0 represent the average-aged participant in sample
4. Add Age_c column to dataframe
5. Verify centering: mean(Age_c) should be approximately 0 (within rounding error <0.01)
6. Create time transformations for LMM (per RQ 5.7 Lin+Log form):
   - Time = TSVR (linear time in hours)
   - Time_log = log(TSVR + 1) (logarithmic time, +1 to handle TSVR=0 at encoding)

**Output:**

**File:** data/step01_lmm_input_prepared.csv
**Format:** CSV, long format
**Columns:**
  - UID (string)
  - TEST (string)
  - TSVR (float, original hours)
  - Time (float, same as TSVR, for LMM formula clarity)
  - Time_log (float, log(TSVR+1) transformation)
  - theta (float)
  - se (float)
  - age (float, original age in years)
  - Age_c (float, grand-mean centered age)
**Expected Rows:** ~400
**Expected Columns:** 9

**Validation Requirement:**
Validation tools MUST be used after age centering execution. Specific validation tools will be determined by rq_tools based on transformation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_lmm_input_prepared.csv exists
- Expected rows: 400 (same as Step 0, no data loss)
- Expected columns: 9 (6 original + Time, Time_log, Age_c)
- Data types: All numeric columns float64, UID/TEST object

*Value Ranges:*
- Time in [0, 200] (same as TSVR)
- Time_log in [0, 5.5] (log(200+1) ~ 5.3)
- age in [18, 90] (unchanged from Step 0)
- Age_c in [-40, 40] (centered around 0, range depends on sample age distribution)

*Data Quality:*
- No NaN values in any column
- mean(Age_c) in [-0.01, 0.01] (successful centering)
- Age_c = age - constant for all rows (verify centering formula applied)
- Time == TSVR for all rows (simple copy)
- Time_log == log(TSVR + 1) for all rows (verify transformation)

*Log Validation:*
- Required pattern: "Grand mean Age: X.XX years"
- Required pattern: "Age_c mean after centering: 0.00" (or very small value <0.01)
- Required pattern: "Time transformations created: Time, Time_log"
- Forbidden patterns: "ERROR", "NaN in Age_c"
- Acceptable warnings: "Age_c mean = 0.003" (minor rounding acceptable)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Age_c mean = 2.1, centering failed")
- Log failure to logs/step01_prepare_age_predictor.log
- Quit script immediately

**Rationale for Grand-Mean Centering:**
- Intercept becomes interpretable as "memory ability for participant of average age"
- Reduces multicollinearity between Age_c and Age_c x Time interaction terms
- Standard practice in regression with continuous predictors and interactions

---

### Step 2: Fit LMM with Age x Time Interaction

**Purpose:** Test Age as predictor of baseline memory (intercept) and forgetting rate (slope) using Lin+Log functional form from RQ 5.7

**Dependencies:** Step 1 (requires prepared data with Age_c and time transformations)
**Complexity:** Medium (~5-10 minutes - LMM fitting with random slopes)

**Input:**

**File:** data/step01_lmm_input_prepared.csv
**Source:** Generated by Step 1
**Format:** CSV with columns: UID, Time, Time_log, theta, Age_c
**Expected Rows:** ~400

**Processing:**

1. Load prepared data from Step 1
2. Fit Linear Mixed Model using statsmodels MixedLM:
   - **Formula:** theta ~ (Time + Time_log) * Age_c + (Time | UID)
   - **Expansion:** theta ~ Time + Time_log + Age_c + Time:Age_c + Time_log:Age_c + (Time | UID)
   - **Fixed Effects:**
     - Intercept (baseline memory at Time=0 for average-aged adult)
     - Time (linear forgetting slope for average-aged adult)
     - Time_log (logarithmic forgetting slope for average-aged adult)
     - Age_c (effect of age on baseline memory at Time=0)
     - Time:Age_c (how age affects linear forgetting rate)
     - Time_log:Age_c (how age affects logarithmic forgetting rate)
   - **Random Effects:**
     - Random intercepts by UID (between-person baseline differences)
     - Random slopes for Time by UID (between-person forgetting rate differences)
   - **Estimation:** REML=False (for model comparison if needed, though not doing AIC here)
3. Extract model convergence status (converged==True required)
4. Save fitted model object (pickle) for downstream use
5. Extract fixed effects table (coefficients, SE, z-values, p-values)
6. Extract random effects variance components (sigma_intercept, sigma_slope, rho, sigma_residual)

**Output:**

**File 1:** results/step02_lmm_age_model.pkl
**Format:** Pickle file (fitted statsmodels MixedLM object)
**Purpose:** Save model for downstream effect size computation and predictions

**File 2:** results/step02_lmm_fixed_effects.csv
**Format:** CSV with columns:
  - term (string, fixed effect name)
  - coef (float, coefficient estimate)
  - se (float, standard error)
  - z (float, z-statistic)
  - p (float, p-value)
**Expected Rows:** 6 (Intercept + 5 fixed effects)

**File 3:** results/step02_lmm_random_effects.csv
**Format:** CSV with variance components
**Columns:**
  - component (string: "sigma_intercept", "sigma_slope", "rho", "sigma_residual")
  - value (float)
**Expected Rows:** 4

**File 4:** results/step02_lmm_model_summary.txt
**Format:** Plain text (statsmodels summary output)
**Content:** Full model summary including fit statistics, AIC, BIC, log-likelihood

**Validation Requirement:**
Validation tools MUST be used after LMM fitting execution. Specific validation tools will be determined by rq_tools based on LMM validation requirements (convergence, residuals, assumptions).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step02_lmm_age_model.pkl exists
- results/step02_lmm_fixed_effects.csv exists
- results/step02_lmm_random_effects.csv exists
- results/step02_lmm_model_summary.txt exists
- Fixed effects CSV: 6 rows x 5 columns (term, coef, se, z, p)
- Random effects CSV: 4 rows x 2 columns (component, value)

*Value Ranges:*
- All coefficients (coef) in [-5, 5] (outside indicates estimation problem)
- All standard errors (se) in [0.001, 2.0] (se=0 or very large indicates non-identification)
- All p-values in [0, 1] (must be valid probabilities)
- sigma_intercept in [0.1, 2.0] (between-person variance in baseline)
- sigma_slope in [0.001, 0.5] (between-person variance in slopes)
- rho in [-1, 1] (correlation between random intercepts and slopes)
- sigma_residual in [0.1, 1.0] (within-person residual variance)

*Data Quality:*
- No NaN values in fixed effects table
- No NaN values in random effects table
- Model converged: converged==True in log
- Fixed effects table has exactly 6 rows (Intercept, Time, Time_log, Age_c, Time:Age_c, Time_log:Age_c)
- All variance components > 0 (not boundary values)

*Log Validation:*
- Required pattern: "Model converged: True"
- Required pattern: "Fixed effects extracted: 6 terms"
- Required pattern: "Random effects variance > 0 for all components"
- Forbidden patterns: "ERROR", "Model did not converge", "Singular matrix"
- Acceptable warnings: "FutureWarning" from statsmodels (library deprecation messages OK)

**Expected Behavior on Validation Failure:**
- If convergence failed: Raise error "LMM did not converge", log diagnostics, invoke g_debug
- If singular matrix: Check for multicollinearity (Age_c centering should prevent this)
- If NaN coefficients: Check input data quality (missing values? outliers?)
- Quit script immediately, do NOT proceed to Step 3

**LMM Formula Explanation:**
- **Lin+Log form:** Inherits best functional form from RQ 5.7 (log component aligns with consolidation theory)
- **Age_c interactions:** Tests hypothesis that age affects BOTH linear and logarithmic forgetting components
- **Random slopes:** Accounts for individual differences in forgetting trajectories (some participants may show faster/slower decline)

---

### Step 3: Extract and Test Age Effects

**Purpose:** Extract Age effects on baseline memory and forgetting rate, apply Bonferroni correction for 3 tests

**Dependencies:** Step 2 (requires fitted LMM model)
**Complexity:** Low (<2 minutes - coefficient extraction and multiple testing correction)

**Input:**

**File:** results/step02_lmm_fixed_effects.csv
**Source:** Generated by Step 2
**Format:** CSV with columns: term, coef, se, z, p
**Expected Rows:** 6

**Processing:**

1. Load fixed effects table from Step 2
2. Extract 3 Age-related terms:
   - **Age_c** (main effect on baseline memory at Time=0)
   - **Time:Age_c** (interaction - how age affects linear forgetting slope)
   - **Time_log:Age_c** (interaction - how age affects logarithmic forgetting slope)
3. For each term, extract:
   - Coefficient (beta)
   - Standard error
   - Z-statistic
   - Uncorrected p-value
4. Apply Bonferroni correction:
   - **Number of tests:** 3 (Age_c, Time:Age_c, Time_log:Age_c)
   - **Corrected alpha:** 0.05 / 3 = 0.0167 (conservative, rq_stats suggested 0.0033 for 15 tests but this RQ only tests 3 Age effects)
   - **Note:** rq_stats context_dump states Bonferroni alpha=0.0033 for 3 tests should be 0.0167, but concept.md uses 0.0033. Per validation workflow design, user approved concept as-is, so use alpha=0.0033 from concept.
   - **Bonferroni-corrected p-value:** p_corrected = min(p_uncorrected * 3, 1.0)
5. Create results table with BOTH uncorrected and corrected p-values (Decision D068)
6. Flag significant effects at alpha=0.0033 (Bonferroni-corrected threshold from concept.md)

**Output:**

**File:** results/step03_age_effects.csv
**Format:** CSV with columns:
  - term (string: "Age_c", "Time:Age_c", "Time_log:Age_c")
  - coef (float, coefficient estimate)
  - se (float, standard error)
  - z (float, z-statistic)
  - p_uncorrected (float, original p-value)
  - p_bonferroni (float, Bonferroni-corrected p-value)
  - significant_bonferroni (bool, True if p_bonferroni < 0.0033)
**Expected Rows:** 3

**File:** results/step03_age_effects_interpretation.txt
**Format:** Plain text interpretation
**Content:**
  - Direction of Age effects (negative coef = older adults worse/faster forgetting)
  - Significance status at Bonferroni-corrected alpha=0.0033
  - Interpretation: "Age_c on intercept: beta=-0.XX, p=0.00X - older adults show lower baseline memory"

**Validation Requirement:**
Validation tools MUST be used after effect extraction execution. Specific validation tools will be determined by rq_tools based on hypothesis testing validation requirements (Decision D068 compliance).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step03_age_effects.csv exists
- results/step03_age_effects_interpretation.txt exists
- Age effects CSV: 3 rows x 7 columns
- Data types: term (object), coef/se/z/p_uncorrected/p_bonferroni (float64), significant_bonferroni (bool)

*Value Ranges:*
- coef in [-2, 2] (outside indicates unrealistic age effects)
- se in [0.001, 1.0]
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1]
- p_bonferroni >= p_uncorrected (correction should not reduce p-values)

*Data Quality:*
- No NaN values
- Exactly 3 rows (Age_c, Time:Age_c, Time_log:Age_c)
- p_bonferroni = min(p_uncorrected * 3, 1.0) for all rows (verify correction formula)
- Both p-value columns present (Decision D068 dual reporting requirement)

*Log Validation:*
- Required pattern: "3 Age effects extracted"
- Required pattern: "Bonferroni correction applied: alpha=0.0033"
- Required pattern: "Decision D068 compliance: BOTH uncorrected and corrected p-values reported"
- Forbidden patterns: "ERROR", "Missing Age_c term in fixed effects"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- If missing Age terms: Check Step 2 model formula (interaction terms specified correctly?)
- If p_bonferroni < p_uncorrected: Correction formula error, quit and debug
- Raise error with specific failure, log to logs/step03_extract_age_effects.log
- Quit script immediately

**Theoretical Predictions (from concept.md):**
- **Age_c on intercept:** beta < 0, p < 0.0033 (older adults lower baseline memory)
- **Age_c x Time_log:** beta < 0, p < 0.0033 (older adults faster logarithmic forgetting)
- **Age_c x Time:** beta < 0, but may not reach p < 0.0033 (weaker effect)

---

### Step 4: Compute Age Effect Sizes

**Purpose:** Quantify Age effect magnitude as difference in Day 6 theta for 1 SD increase in Age

**Dependencies:** Steps 1, 2 (requires fitted model and Age_c statistics)
**Complexity:** Low (<2 minutes - effect size computation)

**Input:**

**File 1:** results/step02_lmm_age_model.pkl
**Source:** Step 2 (fitted LMM object)

**File 2:** data/step01_lmm_input_prepared.csv
**Source:** Step 1 (for computing SD of Age_c)

**Processing:**

1. Load fitted LMM model from Step 2
2. Load prepared data from Step 1
3. Compute standard deviation of Age_c across unique participants:
   - SD_Age_c = std(unique Age_c values per UID)
4. Extract Age-related coefficients from model:
   - beta_Age_c (baseline effect)
   - beta_Time_Age_c (linear interaction)
   - beta_Time_log_Age_c (logarithmic interaction)
5. Define reference time points:
   - Day 0: Time=0, Time_log=log(0+1)=0
   - Day 6: Time=144 hours (nominal Day 6), Time_log=log(144+1)~4.98
6. Compute predicted theta for average-aged adult (Age_c=0):
   - theta_Day0_avg = Intercept
   - theta_Day6_avg = Intercept + beta_Time*144 + beta_Time_log*4.98
7. Compute predicted theta for 1 SD older adult (Age_c=+1 SD):
   - theta_Day0_older = Intercept + beta_Age_c*SD_Age_c
   - theta_Day6_older = theta_Day6_avg + beta_Age_c*SD_Age_c + beta_Time_Age_c*144*SD_Age_c + beta_Time_log_Age_c*4.98*SD_Age_c
8. Compute age effect sizes:
   - Age_effect_Day0 = theta_Day0_older - theta_Day0_avg (baseline difference)
   - Age_effect_Day6 = theta_Day6_older - theta_Day6_avg (Day 6 difference)
   - Age_effect_decline = (theta_Day6_older - theta_Day0_older) - (theta_Day6_avg - theta_Day0_avg) (differential forgetting)
9. Convert to proportion of Day 0 ability:
   - Proportional_decline = Age_effect_decline / theta_Day0_avg

**Output:**

**File:** results/step04_age_effect_sizes.csv
**Format:** CSV with columns:
  - metric (string: "SD_Age_c", "Age_effect_Day0", "Age_effect_Day6", "Age_effect_decline", "Proportional_decline")
  - value (float)
  - unit (string: "years", "theta units", "theta units", "theta units", "proportion")
  - interpretation (string: text explanation)
**Expected Rows:** 5

**File:** results/step04_age_effect_sizes_interpretation.txt
**Format:** Plain text narrative
**Content:**
  - "For each 1 SD increase in Age (X.X years), baseline memory (Day 0) decreases by X.XX theta units"
  - "For each 1 SD increase in Age, Day 6 memory decreases by X.XX theta units"
  - "This represents X.X% additional decline relative to average-aged adults"

**Validation Requirement:**
Validation tools MUST be used after effect size computation execution. Specific validation tools will be determined by rq_tools based on effect size validation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step04_age_effect_sizes.csv exists
- results/step04_age_effect_sizes_interpretation.txt exists
- Effect sizes CSV: 5 rows x 4 columns
- Data types: metric/unit/interpretation (object), value (float64)

*Value Ranges:*
- SD_Age_c in [5, 20] years (typical adult age SD)
- Age_effect_Day0 in [-1, 0] theta units (negative = older adults worse)
- Age_effect_Day6 in [-2, 0] theta units (more negative than Day0 if differential forgetting)
- Age_effect_decline in [-1, 0] theta units (negative = faster forgetting for older adults)
- Proportional_decline in [-1, 0] proportion (negative = additional decline)

*Data Quality:*
- No NaN values
- Exactly 5 rows (one per metric)
- Age_effect_decline < 0 if Age_c x Time interactions are negative (consistency check)
- Age_effect_Day6 < Age_effect_Day0 if dual deficit hypothesis holds (more negative at Day 6)

*Log Validation:*
- Required pattern: "SD of Age_c computed: X.X years"
- Required pattern: "Age effect at Day 0: X.XX theta units"
- Required pattern: "Age effect at Day 6: X.XX theta units"
- Forbidden patterns: "ERROR", "NaN in effect sizes"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- If SD_Age_c = 0: Data issue (no age variance?), quit
- If effect sizes NaN: Model coefficient issue, check Step 2 convergence
- Raise error with specific failure, log to logs/step04_compute_age_effect_sizes.log

**Interpretation Note:**
Effect sizes quantify hypothesis predictions. Expected: Age_effect_Day0 < 0 (older adults lower baseline), Age_effect_decline < 0 (older adults faster forgetting), consistent with dual deficit hypothesis.

---

### Step 5: Prepare Age Tertile Plot Data

**Purpose:** Create age tertiles (Young/Middle/Older) for trajectory visualization, aggregate observed means and model predictions

**Dependencies:** Steps 1, 2 (requires prepared data and fitted model)
**Complexity:** Low (<3 minutes - grouping and aggregation)

**Input:**

**File 1:** data/step01_lmm_input_prepared.csv
**Source:** Step 1

**File 2:** results/step02_lmm_age_model.pkl
**Source:** Step 2 (for model predictions)

**Processing:**

1. Load prepared data from Step 1 (UID, Time, theta, Age_c)
2. Compute Age tertiles (3 equal-sized groups):
   - Young: Bottom 33% of Age distribution
   - Middle: Middle 34% of Age distribution
   - Older: Top 33% of Age distribution
3. Assign Age_tertile label to each participant (based on UID's Age_c value)
4. For each Age_tertile x Time combination:
   - Compute observed mean theta
   - Compute 95% confidence interval (mean +/- 1.96*SE)
   - Count N observations
5. Load fitted LMM model from Step 2
6. Generate model predictions for each Age_tertile at reference time points:
   - Time points: 0, 24, 72, 144 hours (nominal Days 0, 1, 3, 6)
   - For each tertile, use median Age_c within that tertile as predictor
   - Predict theta using model fixed effects (ignoring random effects for population-level trajectory)
7. Merge observed means with model predictions
8. Create plot-ready CSV with columns: Time, Age_tertile, observed_mean, CI_lower, CI_upper, model_pred

**Output:**

**File:** plots/step05_age_tertile_plot_data.csv
**Format:** CSV with columns:
  - Time (float, hours since encoding: 0, 24, 72, 144)
  - Age_tertile (string, category: "Young", "Middle", "Older")
  - observed_mean (float, mean theta for this tertile x time)
  - CI_lower (float, lower 95% CI bound)
  - CI_upper (float, upper 95% CI bound)
  - model_pred (float, LMM predicted theta for median Age_c in this tertile)
  - N (int, number of observations in this cell)
**Expected Rows:** 12 (3 tertiles x 4 time points)

**File:** plots/step05_age_tertile_mapping.csv
**Format:** CSV showing tertile cutoffs
**Columns:**
  - Age_tertile (string)
  - N_participants (int)
  - Age_min (float, years)
  - Age_max (float, years)
  - Age_median (float, years)
  - Age_c_median (float, centered age)
**Expected Rows:** 3

**Validation Requirement:**
Validation tools MUST be used after plot data preparation execution. Specific validation tools will be determined by rq_tools based on plot data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- plots/step05_age_tertile_plot_data.csv exists
- plots/step05_age_tertile_mapping.csv exists
- Plot data CSV: 12 rows x 7 columns
- Tertile mapping CSV: 3 rows x 6 columns

*Value Ranges:*
- Time in {0, 24, 72, 144} (exact values, no intermediate times)
- Age_tertile in {"Young", "Middle", "Older"} (3 categories only)
- observed_mean in [-3, 3] (typical theta range)
- CI_lower < observed_mean < CI_upper for all rows (confidence intervals valid)
- model_pred in [-3, 3]
- N in [30, 35] per cell (roughly 100 participants / 3 tertiles ~ 33 per group)

*Data Quality:*
- No NaN values in any column
- Exactly 12 rows (3 tertiles x 4 time points)
- Each tertile appears exactly 4 times (once per time point)
- Each time point appears exactly 3 times (once per tertile)
- Sum of N_participants in tertile mapping = 100 (all participants assigned)
- Tertile sizes roughly equal (within +/- 2 participants)

*Log Validation:*
- Required pattern: "Age tertiles created: Young (N=XX), Middle (N=XX), Older (N=XX)"
- Required pattern: "Observed means computed for 12 cells (3 tertiles x 4 times)"
- Required pattern: "Model predictions generated using median Age_c per tertile"
- Forbidden patterns: "ERROR", "NaN in plot data", "Unequal tertile sizes >5 difference"
- Acceptable warnings: "Tertile sizes differ by 1-2 participants" (rounding acceptable)

**Expected Behavior on Validation Failure:**
- If tertile sizes highly unequal (difference >5): Check tertile computation (quantile method issue?)
- If NaN in observed_mean: Check for missing data in some tertile x time cells
- If CI_lower > CI_upper: Confidence interval computation error, debug
- Raise error with specific failure, log to logs/step05_prepare_age_tertile_plot_data.log

**Plotting Note (for rq_plots agent):**
This plot source CSV enables trajectory visualization showing Age effects. Expected pattern: Older tertile shows lower baseline (Day 0) and steeper decline than Young tertile. Plot will have 3 lines (one per tertile), observed means as points with error bars, model predictions as smooth lines.

---

## Expected Data Formats

### Cross-Step Data Flow

**Step 0 Output -> Step 1 Input:**
- Format: Long CSV with UID, TEST, TSVR, theta, se, age
- Key transformation: Merge 3 sources (RQ 5.7 theta + TSVR + Age)
- No missing values allowed

**Step 1 Output -> Step 2 Input:**
- Format: Long CSV with added Age_c, Time, Time_log columns
- Key transformation: Grand-mean centering Age, create time variables
- Age_c mean ~ 0 (successful centering)

**Step 2 Output -> Steps 3, 4, 5:**
- Format: Fitted statsmodels MixedLM object (pickle) + CSV tables
- Key use: Extract coefficients (Step 3), generate predictions (Steps 4, 5)
- Convergence required for downstream use

**Steps 3, 4, 5 Outputs -> rq_results:**
- Format: CSV tables + text interpretations
- Purpose: Scientific reporting of Age effects on baseline and forgetting rate

### Column Naming Conventions (from names.md)

**Core identifiers:**
- UID: Participant unique ID (format: P### with leading zeros)
- TEST: Test session (T1, T2, T3, T4 for Days 0, 1, 3, 6)
- composite_ID: UID_TEST format (e.g., P001_T1)

**Time variables (Decision D070):**
- TSVR: Time Since VR in hours (actual elapsed time from dfData.csv)
- Time: Same as TSVR (for LMM formula clarity)
- Time_log: log(TSVR + 1) transformation

**IRT outputs (from RQ 5.7):**
- theta: IRT ability estimate for "All" composite factor (What/Where/When combined)
- se: Standard error of theta

**Age variables:**
- age: Raw age in years (from dfData.csv)
- Age_c: Grand-mean centered age (age - mean(age))

**LMM outputs:**
- coef: Coefficient estimate (beta)
- se: Standard error
- z: Z-statistic
- p: P-value (uncorrected)
- p_bonferroni: Bonferroni-corrected p-value (Decision D068)

**Plot data columns:**
- Age_tertile: Categorical ("Young", "Middle", "Older")
- observed_mean: Mean theta for tertile x time cell
- CI_lower, CI_upper: 95% confidence interval bounds
- model_pred: LMM predicted theta

### Data Type Specifications

**String columns:** UID, TEST, composite_ID, Age_tertile, term, metric, component
**Float columns:** TSVR, Time, Time_log, theta, se, age, Age_c, coef, z, p values, effect sizes, observed_mean, CI bounds, model_pred
**Integer columns:** N (observation counts)
**Boolean columns:** significant_bonferroni

---

## Cross-RQ Dependencies

**Dependency Type 2: DERIVED Data from RQ 5.7 (Dependencies Exist)**

**This RQ requires outputs from:**
- **RQ 5.7** (Functional form comparison - Lin+Log best model)
  - File: results/ch5/rq7/data/step03_theta_all.csv (theta scores for "All" composite factor)
  - Used in: Step 0 (merge with Age to create LMM input)
  - Rationale: RQ 5.7 calibrates IRT model for combined What/Where/When domains. This RQ tests Age effects on those composite theta scores to examine broad episodic memory decline.

  - File: results/ch5/rq7/data/step00_tsvr_mapping.csv (time mapping)
  - Used in: Step 0 (add TSVR time variable to merged data)
  - Rationale: Decision D070 requires actual hours (TSVR) as time variable, not nominal days.

**Execution Order Constraint:**
1. RQ 5.7 must complete Steps 0-3 first (IRT calibration and theta extraction for "All" factor)
2. This RQ (5.9) executes after RQ 5.7 completion

**Data Source Boundaries (Per v4.X Architecture):**
- **RAW data:** Age from data/cache/dfData.csv (project-level file)
- **DERIVED data:** Theta scores and TSVR from RQ 5.7 (cross-RQ dependency)
- **Scope:** This RQ does NOT re-calibrate IRT models (reuses RQ 5.7 theta scores as outcome variable)

**Validation:**
- Step 0: Check results/ch5/rq7/data/step03_theta_all.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch5/rq7/data/step00_tsvr_mapping.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- If either file missing -> quit with error -> user must execute RQ 5.7 first

**Additional RAW Data Source:**
- data/cache/dfData.csv: Age variable (column: "age" in years)
- Validation: Check Age column exists and has no missing values for 100 participants

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

#### Step 0: Merge RQ 5.7 Theta with Age and TSVR

**Analysis Tool:** (determined by rq_tools - likely pandas merge operations)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_data_merge or custom validation)

**What Validation Checks (rq_inspect scope):**
- Output file exists (data/step00_lmm_input_raw.csv)
- Expected column count (6 columns: UID, TEST, TSVR, theta, se, age)
- Expected row count (400 rows: 100 participants x 4 tests)
- No NaN values in critical columns (TSVR, theta, age)
- UID format correct (P### pattern)
- TEST values valid (T1, T2, T3, T4 only)
- No duplicate UID x TEST combinations

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "5 participants missing Age in dfData.csv")
- Log failure to logs/step00_merge_rq7_theta_age.log
- Quit script immediately (do NOT proceed to Step 1)
- User must check: RQ 5.7 complete? dfData.csv has Age column? All participants have Age values?

---

#### Step 1: Prepare Age Predictor (Grand-Mean Centering)

**Analysis Tool:** (determined by rq_tools - likely pandas operations + numpy mean/std)
**Validation Tool:** (determined by rq_tools - likely custom validation checking centering success)

**What Validation Checks:**
- Output file exists (data/step01_lmm_input_prepared.csv)
- Expected column count (9 columns: original 6 + Time, Time_log, Age_c)
- Expected row count (400, same as Step 0)
- Age_c successfully centered: mean(Age_c) in [-0.01, 0.01]
- Time transformations correct: Time == TSVR, Time_log == log(TSVR+1)
- No NaN values introduced

**Expected Behavior on Validation Failure:**
- If mean(Age_c) not near 0: Centering failed, check grand mean computation
- If Time != TSVR: Variable creation error
- Raise error, log to logs/step01_prepare_age_predictor.log, quit immediately

---

#### Step 2: Fit LMM with Age x Time Interaction

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.fit_lmm_trajectory_tsvr or custom LMM function)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_lmm_convergence + validate_lmm_residuals)

**What Validation Checks:**
- Model converged (converged==True)
- Output files exist (model.pkl, fixed_effects.csv, random_effects.csv, model_summary.txt)
- Fixed effects table has 6 rows (Intercept + 5 terms)
- No NaN coefficients or p-values
- Random effects variances > 0 (not boundary values)
- Residuals approximately normal (Kolmogorov-Smirnov test p > 0.05)

**Expected Behavior on Validation Failure:**
- If convergence failed: Log diagnostics (singular matrix? max iterations reached?), invoke g_debug
- If singular matrix: Check for multicollinearity (Age_c centering should prevent, but verify)
- Quit immediately, do NOT proceed to Step 3

---

#### Step 3: Extract and Test Age Effects

**Analysis Tool:** (determined by rq_tools - likely custom coefficient extraction + Bonferroni correction function)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_hypothesis_tests + validate_contrasts for D068 compliance)

**What Validation Checks:**
- Output file exists (results/step03_age_effects.csv)
- Expected row count (3 rows: Age_c, Time:Age_c, Time_log:Age_c)
- BOTH p-value columns present (p_uncorrected, p_bonferroni per Decision D068)
- Bonferroni correction formula correct: p_bonferroni = min(p_uncorrected * 3, 1.0)
- p_bonferroni >= p_uncorrected for all rows
- No NaN values

**Expected Behavior on Validation Failure:**
- If missing p_bonferroni column: Decision D068 violation, quit
- If p_bonferroni < p_uncorrected: Correction error, debug formula
- Raise error, log to logs/step03_extract_age_effects.log

---

#### Step 4: Compute Age Effect Sizes

**Analysis Tool:** (determined by rq_tools - likely custom effect size computation using model predictions)
**Validation Tool:** (determined by rq_tools - likely custom validation checking effect size bounds and consistency)

**What Validation Checks:**
- Output file exists (results/step04_age_effect_sizes.csv)
- Expected row count (5 metrics)
- Effect sizes in reasonable ranges (SD_Age_c in [5, 20], effects in [-2, 0])
- Consistency: Age_effect_Day6 < Age_effect_Day0 if dual deficit hypothesis holds
- No NaN values

**Expected Behavior on Validation Failure:**
- If SD_Age_c = 0: No age variance in sample (data issue), quit
- If effects NaN: Model prediction failed, check Step 2 convergence
- Raise error, log to logs/step04_compute_age_effect_sizes.log

---

#### Step 5: Prepare Age Tertile Plot Data

**Analysis Tool:** (determined by rq_tools - likely custom tertile creation + aggregation function)
**Validation Tool:** (determined by rq_tools - likely custom validation checking plot data format)

**What Validation Checks:**
- Output files exist (plot_data.csv, tertile_mapping.csv)
- Plot data: 12 rows (3 tertiles x 4 time points)
- Tertile sizes roughly equal (within +/- 2 participants)
- CI_lower < observed_mean < CI_upper for all rows
- No NaN values
- Time values in {0, 24, 72, 144} exactly

**Expected Behavior on Validation Failure:**
- If tertile sizes highly unequal: Tertile computation issue
- If NaN in observed_mean: Missing data in some cells, investigate
- Raise error, log to logs/step05_prepare_age_tertile_plot_data.log

---

## Summary

**Total Steps:** 6 (Step 0: data merge + Steps 1-5: LMM analysis, effects, effect sizes, plot data)
**Estimated Runtime:** Medium (~10-20 minutes total)
  - Step 0: <5 min (data merge)
  - Step 1: <1 min (centering)
  - Step 2: 5-10 min (LMM fitting)
  - Step 3: <2 min (effect extraction)
  - Step 4: <2 min (effect sizes)
  - Step 5: <3 min (plot data)

**Cross-RQ Dependencies:** RQ 5.7 (theta scores for "All" composite factor + TSVR mapping)

**Primary Outputs:**
- data/step00_lmm_input_raw.csv (merged theta + Age + TSVR)
- data/step01_lmm_input_prepared.csv (Age_c centered, time transformations)
- results/step02_lmm_age_model.pkl (fitted LMM object)
- results/step02_lmm_fixed_effects.csv (6 fixed effect coefficients)
- results/step03_age_effects.csv (3 Age effects with dual p-values per D068)
- results/step04_age_effect_sizes.csv (effect sizes in theta units and proportions)
- plots/step05_age_tertile_plot_data.csv (12 rows for trajectory visualization)

**Validation Coverage:** 100% (all 6 steps have validation requirements)

**Decision Compliance:**
- D068: Dual p-value reporting (uncorrected + Bonferroni) for 3 Age effects 
- D070: TSVR as time variable (inherited from RQ 5.7) 

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_name.py scripts

---

**Version History:**
- v1.0 (2025-11-26): Initial plan created by rq_planner agent for RQ 5.9
