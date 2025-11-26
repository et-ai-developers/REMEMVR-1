# Analysis Plan: RQ 5.15 - Item Difficulty x Time Interaction

**Research Question:** 5.15
**Created:** 2025-11-26
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines whether item difficulty moderates forgetting trajectories via cross-level interaction (Time x Difficulty_c). Analysis uses cross-classified Linear Mixed Model with pymer4 to handle crossed random effects (UID x Item). The research question is exploratory with competing theoretical predictions: strength theory predicts easier items forget faster (negative interaction), ceiling effects predict easier items forget slower (positive interaction), or no interaction (difficulty affects intercept only).

**Pipeline:** LMM only (no IRT calibration - uses DERIVED difficulty estimates from RQ 5.1)

**Steps:** 6 analysis steps (Step 0: load data, Step 1: center predictors, Step 2: fit cross-classified LMM, Step 3: extract interaction, Step 4: validate assumptions, Step 5: prepare plot data)

**Estimated Runtime:** Medium (30-60 minutes total - cross-classified LMM fitting is computationally intensive)

**Key Decisions Applied:**
- Decision D070: TSVR as time variable (actual hours, not nominal days)
- Bonferroni correction: alpha = 0.05/15 = 0.0033 (15 RQs in Chapter 5)
- Comprehensive LMM assumption validation (Step 4.5 from validated concept)
- Cross-classified random effects require pymer4 (statsmodels doesn't support crossed UID x Item)

---

## Analysis Plan

### Step 0: Load and Merge Data

**Dependencies:** None (first step, but requires RQ 5.1 outputs to exist)

**Complexity:** Low (data loading and merging only, <5 minutes)

**Purpose:** Load item difficulty estimates from RQ 5.1, load response data, merge TSVR time variable, create analysis-ready dataset.

**Input:**

**File 1:** results/ch5/rq1/data/step03_difficulty.csv
**Source:** RQ 5.1 Step 3 (Pass 2 IRT calibration on purified items)
**Format:** CSV with columns:
  - `item_name` (string, item tag identifier from master.xlsx)
  - `dimension` (string, domain: What/Where/When)
  - `b` (float, IRT difficulty parameter, range typically -6.0 to +6.0)
  - `a` (float, IRT discrimination parameter, range typically 0.4 to 10.0 for purified items)
**Expected Rows:** ~100 items (purified set from RQ 5.1 after Decision D039 filtering)
**Note:** Only column `b` (difficulty) is used in this RQ; `a` (discrimination) not needed for cross-level interaction

**File 2:** data/cache/dfData.csv
**Source:** Created by RQ 5.1 Step 0 (raw extraction from master.xlsx)
**Format:** CSV with long-format response data
**Columns:**
  - `UID` (string, participant identifier, format: P### with leading zeros)
  - `test` (string, test session: T1/T2/T3/T4)
  - `item_name` (string, item tag identifier)
  - `response` (int, dichotomized response: 0=incorrect, 1=correct)
**Expected Rows:** ~40,000 rows (100 participants x 4 tests x ~100 purified items)
**Note:** dfData.csv contains responses for ALL items, must filter to purified items only (match on item_name with step03_difficulty.csv)

**File 3:** results/ch5/rq1/data/step00_tsvr_mapping.csv
**Source:** RQ 5.1 Step 0 (TSVR time variable extraction per Decision D070)
**Format:** CSV with columns:
  - `UID` (string, participant identifier)
  - `test` (string, test session: T1/T2/T3/T4)
  - `TSVR_hours` (float, actual hours since encoding, range: 0 to ~168 hours)
**Expected Rows:** 400 rows (100 participants x 4 tests)
**Note:** TSVR_hours is actual elapsed time, NOT nominal days (0,1,3,6)

**Processing:**

1. **Load difficulty estimates:** Read step03_difficulty.csv, extract item_name and b (difficulty) columns
2. **Load response data:** Read dfData.csv (long format: UID x test x item_name x response)
3. **Filter to purified items:** Inner join response data with difficulty data on item_name (keeps only items with difficulty estimates)
4. **Load TSVR mapping:** Read step00_tsvr_mapping.csv
5. **Merge TSVR:** Left join response data with TSVR mapping on (UID, test) -> adds TSVR_hours column
6. **Verify merge completeness:** Check that all response rows have non-null TSVR_hours (validation failure if any missing)
7. **Add Days variable:** Create nominal Days column from test (T1=0, T2=1, T3=3, T4=6) for interpretability
8. **Verify data structure:** Count unique UIDs (~100), unique items (~100), total rows (~40,000)

**Output:**

**File 1:** data/step00_merged_data.csv
**Format:** CSV, long format (one row per UID-test-item response)
**Columns:**
  - `UID` (string, participant identifier)
  - `test` (string, test session: T1/T2/T3/T4)
  - `item_name` (string, item tag identifier)
  - `response` (int, 0/1)
  - `Difficulty` (float, item difficulty from IRT, range: -6.0 to +6.0)
  - `TSVR_hours` (float, actual time since encoding)
  - `Days` (int, nominal days: 0/1/3/6 for interpretability)
**Expected Rows:** ~40,000 (100 UIDs x 4 tests x ~100 purified items)
**Expected Columns:** 7

**Validation Requirement:**

Validation tools MUST be used after data merging execution. Specific validation tools will be determined by rq_tools based on data format requirements (validate merged data structure, check for missing values, verify expected dimensions).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_merged_data.csv exists (exact path)
- Expected rows: 38,000 to 42,000 (100 participants x 4 tests x 95-105 items - some variability in purified item count acceptable)
- Expected columns: 7 (UID, test, item_name, response, Difficulty, TSVR_hours, Days)
- Data types: UID (object), test (object), item_name (object), response (int64), Difficulty (float64), TSVR_hours (float64), Days (int64)

*Value Ranges:*
- response in {0, 1} (dichotomized, no other values)
- Difficulty in [-6, 6] (IRT difficulty range, purified items typically [-3, 3] but allow wider range)
- TSVR_hours in [0, 200] hours (encoding to ~1 week, allows some schedule variability)
- Days in {0, 1, 3, 6} (nominal test days, exact values only)

*Data Quality:*
- No NaN in TSVR_hours (merge must be complete - all response rows have time data)
- No NaN in Difficulty (merge must be complete - all items have difficulty estimates)
- Expected unique UIDs: 95 to 100 (some participant exclusions possible but should be minimal)
- Expected unique items: 90 to 110 (purified item count from RQ 5.1 varies by domain)
- Distribution check: response mean between 0.3 and 0.7 (reasonable accuracy range, not floor/ceiling)

*Log Validation:*
- Required pattern: "Merged data: [N] rows created" where N in [38000, 42000]
- Required pattern: "Unique UIDs: [M]" where M in [95, 100]
- Required pattern: "Unique items: [K]" where K in [90, 110]
- Required pattern: "No missing TSVR_hours (100% merge success)"
- Required pattern: "No missing Difficulty (100% merge success)"
- Forbidden patterns: "ERROR", "NaN detected in TSVR_hours", "NaN detected in Difficulty", "Merge failed"
- Acceptable warnings: None expected for data merging step

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected ~40,000 rows, found 25,000" or "Missing TSVR_hours for 15% of rows")
- Log failure to logs/step00_merged_data.log
- Quit script immediately (do NOT proceed to Step 1)
- Check RQ 5.1 outputs exist and are complete (dependency issue)

---

### Step 1: Center Predictors

**Dependencies:** Step 0 (requires merged data with Difficulty column)

**Complexity:** Low (simple transformation, <1 minute)

**Purpose:** Grand-mean center item difficulty for interpretability (allows LMM intercept to represent average item at average difficulty).

**Input:**

**File:** data/step00_merged_data.csv (from Step 0)
**Required Columns:** Difficulty (float, item difficulty from IRT)

**Processing:**

1. **Compute grand mean:** Calculate mean(Difficulty) across all items (pooled across all responses)
2. **Center difficulty:** Create Difficulty_c = Difficulty - mean(Difficulty)
3. **Verify centering:** Check that mean(Difficulty_c) is approximately 0 (within rounding error, <0.001)
4. **Rationale:** Grand-mean centering is appropriate because items are crossed with participants (not nested). Cluster-mean centering (within-participant) not applicable since each item has single difficulty value across all participants (Enders & Tofighi, 2007).

**Output:**

**File:** data/step01_centered_data.csv
**Format:** CSV, long format (same structure as input with added column)
**Columns:** All columns from step00_merged_data.csv PLUS:
  - `Difficulty_c` (float, centered difficulty: Difficulty - mean(Difficulty))
**Expected Rows:** Same as input (~40,000)
**Expected Columns:** 8 (7 from Step 0 + 1 new column)

**Validation Requirement:**

Validation tools MUST be used after centering transformation execution. Specific validation tools determined by rq_tools based on centering requirements (check mean approximately zero, verify no NaN introduced).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_centered_data.csv exists (exact path)
- Expected rows: Same as step00_merged_data.csv (no rows added/removed)
- Expected columns: 8 (7 original + Difficulty_c)
- Data types: All original columns unchanged, Difficulty_c (float64)

*Value Ranges:*
- Difficulty_c in [-6, 6] (same range as Difficulty but shifted)
- Mean of Difficulty_c: -0.001 to +0.001 (approximately zero, allows rounding error)

*Data Quality:*
- No NaN in Difficulty_c (centering should not introduce missing values)
- SD of Difficulty_c equals SD of Difficulty (centering preserves variance)

*Log Validation:*
- Required pattern: "Grand mean of Difficulty: [value]" where value in [-6, 6]
- Required pattern: "Mean of Difficulty_c: [value]" where value in [-0.001, 0.001]
- Required pattern: "Centering successful: SD preserved"
- Forbidden patterns: "ERROR", "NaN introduced in Difficulty_c"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Mean of Difficulty_c = 0.15, not approximately zero")
- Log failure to logs/step01_centered_data.log
- Quit immediately

---

### Step 2: Fit Cross-Classified LMM

**Dependencies:** Step 1 (requires centered predictors)

**Complexity:** High (cross-classified random effects computationally intensive, 20-40 minutes)

**Purpose:** Fit Linear Mixed Model testing Time x Difficulty_c interaction with crossed random effects (UID x Item). Model selection strategy: attempt full random slopes (Time | UID) first, simplify to uncorrelated slopes (Time || UID) or random intercepts only (1 | UID) if convergence fails.

**Input:**

**File:** data/step01_centered_data.csv (from Step 1)
**Required Columns:**
  - `UID` (string, grouping variable for person-level random effects)
  - `item_name` (string, grouping variable for item-level random effects)
  - `response` (int, 0/1 dichotomized outcome)
  - `TSVR_hours` (float, time variable per Decision D070)
  - `Difficulty_c` (float, centered item difficulty)
  - `Days` (int, nominal days for interpretability)

**Processing:**

1. **Model Formula (Maximal):**
   - Fixed effects: `response ~ TSVR_hours * Difficulty_c`
     - TSVR_hours: Main effect of time (forgetting trajectory)
     - Difficulty_c: Main effect of item difficulty (easier vs harder items)
     - TSVR_hours * Difficulty_c: Cross-level interaction (does difficulty moderate forgetting rate?)
   - Random effects: `(TSVR_hours | UID) + (1 | item_name)`
     - (TSVR_hours | UID): Random intercepts and slopes for time within participants (allows individual differences in forgetting rate)
     - (1 | item_name): Random intercepts for items (accounts for item-specific variability)
     - Crossed structure: UIDs crossed with items (not nested)

2. **Software:** pymer4 (Python wrapper for R's lme4)
   - Rationale: statsmodels doesn't support crossed random effects
   - Fallback: If pymer4 unavailable, treat item_name as fixed effect (loses generalizability but allows convergence)

3. **Model Selection Strategy (if convergence fails):**
   - Step 2a: Attempt maximal model: (TSVR_hours | UID) + (1 | item_name)
   - Step 2b: If singular fit warning or convergence failure, simplify to uncorrelated random slopes: (TSVR_hours || UID) + (1 | item_name)
     - Removes correlation between random intercepts and random slopes
   - Step 2c: If still fails, simplify to random intercepts only: (1 | UID) + (1 | item_name)
   - Step 2d: Document which model converged in results

4. **Convergence Diagnostics:**
   - Check optimizer convergence message (no warnings/errors from pymer4)
   - Check for singular fit warnings (variance estimates near zero = overparameterization)
   - Check random effects correlations near +/-1 (indicates instability)
   - Use validate_lmm_convergence tool (automated convergence checks)

5. **Estimation Method:**
   - REML (Restricted Maximum Likelihood) for variance component estimation
   - Switch to ML (Maximum Likelihood) if comparing nested models via likelihood ratio test

6. **Extract Results:**
   - Fixed effects table: coefficients, SE, z-values, p-values
   - Random effects: variance components, ICC
   - Interaction term: Time x Difficulty_c coefficient and p-value
   - Model fit: AIC, BIC, log-likelihood

**Output:**

**File 1:** results/step02_lmm_model_summary.txt
**Format:** Plain text summary
**Content:**
  - Model formula used (which random structure converged)
  - Fixed effects table (coefficients, SE, z, p for TSVR_hours, Difficulty_c, interaction)
  - Random effects variance components (UID variance, item variance, residual variance)
  - ICC (Intraclass Correlation Coefficient)
  - Model fit indices (AIC, BIC, log-likelihood)
  - Convergence status (successful or warnings encountered)

**File 2:** results/step02_fixed_effects.csv
**Format:** CSV
**Columns:**
  - `term` (string, predictor name: Intercept, TSVR_hours, Difficulty_c, TSVR_hours:Difficulty_c)
  - `estimate` (float, regression coefficient)
  - `se` (float, standard error)
  - `z_value` (float, z-statistic)
  - `p_value` (float, uncorrected p-value)
  - `p_bonferroni` (float, Bonferroni-corrected p-value: p_value * 15)
**Expected Rows:** 4 (intercept + 2 main effects + 1 interaction)

**File 3:** results/step02_random_effects.csv
**Format:** CSV
**Columns:**
  - `group` (string, UID or item_name)
  - `variance` (float, variance component for that grouping level)
  - `sd` (float, standard deviation: sqrt(variance))
**Expected Rows:** 2-4 rows (depends on random structure: UID intercept, UID slope if converged, item intercept, residual)

**File 4:** data/step02_model_object.pkl
**Format:** Pickle file (serialized pymer4 model object)
**Purpose:** Save fitted model for assumption validation (Step 4) and plotting (Step 5)
**Note:** Required for extracting residuals, fitted values, random effects for diagnostics

**Validation Requirement:**

Validation tools MUST be used after LMM fitting execution. Specific validation tools determined by rq_tools based on LMM requirements (validate_lmm_convergence checks convergence status, singular fit warnings, random effects correlations).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step02_lmm_model_summary.txt exists
- results/step02_fixed_effects.csv exists with 4 rows x 6 columns
- results/step02_random_effects.csv exists with 2-4 rows (depends on random structure)
- data/step02_model_object.pkl exists (serialized model)

*Value Ranges:*
- Fixed effects estimates: -10 to +10 (regression coefficients on response scale 0-1, extreme values >10 implausible)
- p_value in [0, 1] (all p-values)
- p_bonferroni in [0, 15] (corrected p-values can exceed 1.0, capped at 15 for reporting)
- Variance components: > 0 (variances must be non-negative, exactly 0 indicates singular fit)
- ICC in [0, 1] (proportion of variance attributable to grouping)

*Data Quality:*
- No NaN in fixed effects table (model must estimate all coefficients)
- No NaN in random effects (variance components must be estimated)
- Convergence status: Model converged successfully OR documented simplification to parsimonious structure
- Singular fit warnings: Acceptable if documented (indicates overparameterization addressed via model selection)

*Log Validation:*
- Required pattern: "Model converged: True" OR "Model simplified to [formula] - converged successfully"
- Required pattern: "Fixed effects extracted: 4 terms"
- Required pattern: "Random effects extracted: [N] variance components" where N in [2, 4]
- Required pattern: "Interaction term: TSVR_hours:Difficulty_c [estimate] (p=[value])"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "Model fitting crashed"
- Acceptable warnings: "Singular fit warning - simplified random structure" (documented in results)

**Expected Behavior on Validation Failure:**
- Convergence failure: Quit with error, log attempted model formulas, check data structure (N=100 may be insufficient for complex random slopes)
- Singular fit: Document warning, attempt model simplification per Step 2b-2c strategy
- Estimation errors: Log error details, suggest rescaling predictors or increasing optimizer iterations
- g_debug invoked if convergence fails even after simplification

---

### Step 3: Extract Interaction Effect

**Dependencies:** Step 2 (requires fitted LMM model)

**Complexity:** Low (extraction only, <1 minute)

**Purpose:** Extract Time x Difficulty_c interaction coefficient and test significance using Bonferroni-corrected threshold (alpha = 0.0033).

**Input:**

**File:** results/step02_fixed_effects.csv (from Step 2)
**Required Columns:** term, estimate, se, z_value, p_value, p_bonferroni

**Processing:**

1. **Extract interaction row:** Filter to term == "TSVR_hours:Difficulty_c"
2. **Test significance:** Compare p_bonferroni < 0.0033 (Bonferroni correction: 0.05/15 RQs)
3. **Interpret direction:**
   - Positive estimate (beta > 0): Easier items (lower difficulty) forget slower -> supports ceiling effects hypothesis
   - Negative estimate (beta < 0): Easier items forget faster -> supports strength theory hypothesis
   - Non-significant (p_bonferroni >= 0.0033): Difficulty affects intercept only, not forgetting rate -> supports orthogonality hypothesis
4. **Create interpretation summary:** Text description of finding with theoretical framing

**Output:**

**File 1:** results/step03_interaction_summary.txt
**Format:** Plain text interpretation
**Content:**
  - Interaction coefficient (estimate +/- SE)
  - Uncorrected p-value
  - Bonferroni-corrected p-value (alpha = 0.0033)
  - Significance determination (significant/non-significant)
  - Effect direction interpretation (positive/negative/null)
  - Theoretical framing (which hypothesis supported: ceiling effects/strength theory/orthogonality)

**File 2:** results/step03_interaction_coefficient.csv
**Format:** CSV (single row)
**Columns:**
  - `term` (string, "TSVR_hours:Difficulty_c")
  - `estimate` (float, interaction coefficient)
  - `se` (float, standard error)
  - `z_value` (float, z-statistic)
  - `p_uncorrected` (float, uncorrected p-value)
  - `p_bonferroni` (float, Bonferroni-corrected p-value)
  - `alpha_threshold` (float, 0.0033)
  - `significant` (bool, p_bonferroni < alpha_threshold)
  - `direction` (string, "positive" / "negative" / "null" based on estimate sign and significance)
**Expected Rows:** 1

**Validation Requirement:**

Validation tools MUST be used after interaction extraction execution. Specific validation tools determined by rq_tools based on hypothesis test requirements (validate p-values in bounds, check significance determination logic).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step03_interaction_summary.txt exists (text file with interpretation)
- results/step03_interaction_coefficient.csv exists with 1 row x 9 columns

*Value Ranges:*
- estimate in [-10, 10] (interaction coefficient, extreme values >10 implausible)
- se > 0 (standard error must be positive)
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 15] (can exceed 1.0, capped for reporting)
- alpha_threshold exactly 0.0033 (Bonferroni correction constant)
- significant in {True, False} (boolean)
- direction in {"positive", "negative", "null"} (categorical)

*Data Quality:*
- No NaN in estimate, se, p-values (extraction must succeed)
- Significance logic correct: significant = True if p_bonferroni < 0.0033, else False
- Direction logic correct: "positive" if estimate > 0 AND significant, "negative" if estimate < 0 AND significant, "null" if not significant

*Log Validation:*
- Required pattern: "Interaction term extracted: TSVR_hours:Difficulty_c"
- Required pattern: "Estimate: [value] +/- [SE]"
- Required pattern: "p_bonferroni = [value] (alpha = 0.0033)"
- Required pattern: "Significance: [True/False]"
- Required pattern: "Direction: [positive/negative/null]"
- Forbidden patterns: "ERROR", "Interaction term not found in fixed effects"

**Expected Behavior on Validation Failure:**
- Interaction term missing: Quit with error, check Step 2 model fitting (interaction must be in model formula)
- Invalid p-values: Quit with error, check Step 2 fixed effects extraction

---

### Step 4: Validate LMM Assumptions

**Dependencies:** Step 2 (requires fitted model object for residual extraction)

**Complexity:** Medium (6 comprehensive checks, 5-10 minutes)

**Purpose:** Perform comprehensive LMM assumption validation per concept Step 4.5 using validate_lmm_assumptions_comprehensive tool. Critical with N=100 and complex random structures where assumption violations can affect Type I error rates.

**Input:**

**File 1:** data/step02_model_object.pkl (fitted model from Step 2)
**File 2:** data/step01_centered_data.csv (data used for fitting)

**Processing:**

1. **Residual Normality:**
   - Extract residuals from fitted model
   - Q-Q plot of residuals (visual inspection)
   - Shapiro-Wilk test (p > 0.05 threshold for normality)
   - Remedial action if violated: Use robust standard errors

2. **Homoscedasticity:**
   - Residual vs fitted values plot (visual inspection for funnel patterns)
   - Levene's test or Breusch-Pagan test (p > 0.05 threshold)
   - Remedial action if violated: Model variance structure (weights parameter in pymer4)

3. **Random Effects Normality:**
   - Extract random intercepts and slopes (if converged) from model
   - Q-Q plots for each random effect level (UID, item)
   - Shapiro-Wilk test per random effect grouping
   - Remedial action if violated: Consider transformation or robust estimation

4. **Independence (Autocorrelation Check):**
   - ACF plot of residuals by UID (check for temporal autocorrelation)
   - Lag-1 ACF < 0.1 threshold (values >0.1 indicate autocorrelation)
   - Remedial action if violated: Add AR(1) correlation structure to model

5. **Linearity:**
   - Partial residual plots for TSVR_hours and Difficulty_c
   - Check for non-linear patterns suggesting model misspecification
   - Remedial action if violated: Add polynomial terms or transform predictors

6. **Outliers:**
   - Cook's distance for each observation (D > 4/n threshold where n = number of observations)
   - Flag high-leverage observations
   - Remedial action if violated: Sensitivity analysis excluding outliers, or robust regression

**Output:**

**File 1:** results/step04_assumption_validation_report.txt
**Format:** Plain text summary
**Content:**
  - Results of all 6 assumption checks (pass/fail/warning)
  - Test statistics and p-values for formal tests
  - Recommendations for remedial actions if any assumptions violated
  - Overall assessment (assumptions met / minor violations / major violations)

**File 2:** plots/step04_diagnostic_plots.png
**Format:** Multi-panel PNG image (6 panels, one per assumption check)
**Panels:**
  - Panel 1: Residual Q-Q plot (normality)
  - Panel 2: Residual vs fitted plot (homoscedasticity)
  - Panel 3: Random effects Q-Q plot (normality of random effects)
  - Panel 4: ACF plot (autocorrelation)
  - Panel 5: Partial residual plot for TSVR_hours (linearity)
  - Panel 6: Cook's distance plot (outliers)

**File 3:** results/step04_assumption_tests.csv
**Format:** CSV
**Columns:**
  - `assumption` (string, assumption name: normality, homoscedasticity, etc.)
  - `test_name` (string, formal test used: Shapiro-Wilk, Levene, etc.)
  - `statistic` (float, test statistic)
  - `p_value` (float, p-value)
  - `threshold` (float, decision threshold: 0.05 for most tests)
  - `result` (string, "PASS" / "FAIL" / "WARNING")
  - `recommendation` (string, remedial action if violated)
**Expected Rows:** 6 (one per assumption check)

**Validation Requirement:**

Validation tools MUST be used after assumption validation execution. Meta-validation: validate that validate_lmm_assumptions_comprehensive ran successfully and produced expected outputs.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step04_assumption_validation_report.txt exists
- plots/step04_diagnostic_plots.png exists (multi-panel image)
- results/step04_assumption_tests.csv exists with 6 rows x 7 columns

*Value Ranges:*
- p_value in [0, 1] (all assumption tests)
- threshold in [0, 1] (decision thresholds)
- result in {"PASS", "FAIL", "WARNING"} (categorical)

*Data Quality:*
- All 6 assumptions tested (no missing rows in step04_assumption_tests.csv)
- No NaN in test statistics or p-values (all tests completed)
- Diagnostic plots generated (PNG file size > 0 KB)

*Log Validation:*
- Required pattern: "Assumption validation complete: 6 checks performed"
- Required pattern: "Residual normality: [PASS/FAIL/WARNING]"
- Required pattern: "Homoscedasticity: [PASS/FAIL/WARNING]"
- Required pattern: "Autocorrelation: [PASS/FAIL/WARNING]"
- Required pattern: "Overall assessment: [assumptions met/minor violations/major violations]"
- Forbidden patterns: "ERROR", "validate_lmm_assumptions_comprehensive failed"
- Acceptable warnings: Assumption violations documented with remedial actions (not a failure, just flagged for interpretation)

**Expected Behavior on Validation Failure:**
- Tool execution failure: Quit with error, check that step02_model_object.pkl is valid pymer4 model
- Assumption violations: Document in report, suggest remedial actions, but DO NOT quit (violations are findings, not errors)
- Major violations: Log recommendation to refit model with robust methods or transformations

---

### Step 5: Prepare Interaction Plot Data

**Dependencies:** Step 2 (requires fitted model for predictions)

**Complexity:** Low (prediction and aggregation, <5 minutes)

**Purpose:** Generate predicted response trajectories for easy items (-1 SD difficulty) vs hard items (+1 SD difficulty) to visualize the Time x Difficulty_c interaction. Creates plot source CSV per Option B architecture (g_code creates data, rq_plots creates visualization).

**Plot Description:** Interaction plot showing predicted response trajectories over time (Days 0, 1, 3, 6) for easy vs hard items. If interaction significant, trajectories diverge (different slopes). If non-significant, trajectories are parallel.

**Input:**

**File 1:** data/step02_model_object.pkl (fitted model from Step 2)
**File 2:** data/step01_centered_data.csv (for SD of Difficulty_c)

**Processing:**

1. **Compute Difficulty SD:** Calculate SD(Difficulty_c) from centered data (approximately 1.0 for standardized predictor)
2. **Define Easy/Hard Items:**
   - Easy items: Difficulty_c = -1 * SD(Difficulty_c) (one SD below mean)
   - Hard items: Difficulty_c = +1 * SD(Difficulty_c) (one SD above mean)
3. **Create Prediction Grid:**
   - TSVR_hours: Values corresponding to Days 0, 1, 3, 6 (convert nominal days to median TSVR from data)
   - Difficulty_c: Two levels (easy = -1 SD, hard = +1 SD)
   - UID: Average across participants (population-level predictions)
   - item_name: Average across items (marginal predictions)
4. **Generate Predictions:**
   - Use fitted model to predict response probability for each combination
   - Extract fixed effects predictions (not including random effects, for population-level trajectory)
5. **Compute Confidence Intervals:**
   - 95% CI for predictions using SE from model
   - CI_lower, CI_upper for each prediction
6. **Format for Plotting:**
   - Columns: Days (0/1/3/6), ItemType (easy/hard), PredictedResponse (0-1 scale), CI_lower, CI_upper

**Required Data Sources:**
- data/step02_model_object.pkl (fitted LMM model)
- data/step01_centered_data.csv (SD of Difficulty_c, median TSVR per test)

**Output (Plot Source CSV):** plots/step05_interaction_plot_data.csv

**Required Columns:**
- `Days` (int): Nominal days (0, 1, 3, 6)
- `ItemType` (string): "Easy (-1 SD)" or "Hard (+1 SD)"
- `PredictedResponse` (float): Model-predicted response probability (0-1 scale)
- `CI_lower` (float): Lower 95% confidence bound
- `CI_upper` (float): Upper 95% confidence bound

**Expected Rows:** 8 (2 item types x 4 time points)

**Aggregation Logic:**
1. Extract SD(Difficulty_c) from centered data
2. Define easy = -1 SD, hard = +1 SD
3. Convert Days to median TSVR_hours per test from step01_centered_data.csv
4. Create prediction grid (8 rows: 2 item types x 4 time points)
5. Generate predictions using pymer4 model.predict() with re.form=None (population-level)
6. Compute 95% CI using prediction SE
7. Format and save to plots/step05_interaction_plot_data.csv

**Validation Requirement:**

Validation tools MUST be used after plot data preparation execution. Specific validation tools determined by rq_tools based on plot data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- plots/step05_interaction_plot_data.csv exists (exact path)
- Expected rows: 8 (2 item types x 4 time points)
- Expected columns: 5 (Days, ItemType, PredictedResponse, CI_lower, CI_upper)
- Data types: Days (int64), ItemType (object), PredictedResponse (float64), CI_lower (float64), CI_upper (float64)

*Value Ranges:*
- Days in {0, 1, 3, 6} (nominal test days, exact values only)
- ItemType in {"Easy (-1 SD)", "Hard (+1 SD)"} (categorical, exact strings)
- PredictedResponse in [0, 1] (probability scale, cannot exceed bounds)
- CI_lower in [0, 1] (confidence bounds on probability scale)
- CI_upper in [0, 1] (confidence bounds on probability scale)

*Data Quality:*
- No NaN values in any column (all predictions must succeed)
- Expected N: Exactly 8 rows (no more, no less)
- No duplicate rows (Days x ItemType combinations unique)
- Distribution check: CI_upper > CI_lower for all rows (confidence intervals valid)
- Logical check: Easy and Hard trajectories differ if interaction significant (Step 3 result)

*Log Validation:*
- Required pattern: "Plot data preparation complete: 8 rows created"
- Required pattern: "Item types represented: Easy (-1 SD), Hard (+1 SD)"
- Required pattern: "Time points: 0, 1, 3, 6 days"
- Required pattern: "Predictions generated from population-level fixed effects"
- Forbidden patterns: "ERROR", "NaN values detected", "Prediction failed"
- Acceptable warnings: None expected for plot data preparation

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 8 rows, found 4")
- Log failure to logs/step05_interaction_plot_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- Check that step02_model_object.pkl is valid pymer4 model

**Plotting Function (rq_plots will call):** Interaction plot with separate lines for easy/hard items
- rq_plots agent maps this description to appropriate plotting function
- Plot reads plots/step05_interaction_plot_data.csv (created by this step)
- No data aggregation in rq_plots (visualization only per Option B)
- Expected visualization: Days on x-axis, PredictedResponse on y-axis, two lines (easy vs hard), confidence bands

---

## Expected Data Formats

### Cross-Classified LMM Structure

**Response Variable:**
- `response` (int, 0/1): Dichotomized accuracy (1 = correct, 0 = incorrect)
- Binary outcome appropriate for logistic mixed model (family = binomial, link = logit)
- Note: pymer4 uses generalized LMM (GLMM) for binary outcomes

**Fixed Effects:**
- `TSVR_hours` (float): Continuous time variable (Decision D070), range: 0 to ~168 hours
- `Difficulty_c` (float): Centered item difficulty, range: approximately -3 to +3 for purified items
- `TSVR_hours:Difficulty_c` (float): Cross-level interaction term (automatic in formula specification)

**Random Effects:**
- `UID` (string, grouping factor): ~100 levels (participants)
- `item_name` (string, grouping factor): ~100 levels (purified items from RQ 5.1)
- Crossed structure: Not nested (each UID responds to all items, each item administered to all UIDs)

**Data Format:**
- Long format: One row per UID-test-item response observation
- Expected rows: ~40,000 (100 UIDs x 4 tests x ~100 items)
- Grouping: Rows nested within (UID x item) cross-classification

### TSVR Time Variable (Decision D070)

**Format:**
- Column name: `TSVR_hours` (per names.md convention)
- Data type: float64
- Range: 0 to ~200 hours (0 = encoding, ~168 = 1 week, allows schedule variability)

**Why TSVR, not Days:**
- Nominal Days (0,1,3,6) assume fixed intervals, but actual timing varies by participant schedule
- TSVR_hours captures actual elapsed time for precise temporal modeling
- Decision D070 mandates TSVR for all trajectory/longitudinal LMM analyses

**Mapping:**
- T1 (Day 0): TSVR_hours median ~0 hours (encoding session)
- T2 (Day 1): TSVR_hours median ~24 hours (range: 20-30 hours)
- T3 (Day 3): TSVR_hours median ~72 hours (range: 65-80 hours)
- T4 (Day 6): TSVR_hours median ~144 hours (range: 135-160 hours)

### Grand-Mean Centering Rationale

**Why Grand-Mean (Not Cluster-Mean):**
- Item difficulty is crossed with participants (not nested within participants)
- Each item has single difficulty value across all participants
- Cluster-mean centering (within-participant) not applicable because Difficulty is item-level predictor
- Grand-mean centering allows intercept to represent average item at average difficulty (Enders & Tofighi, 2007)

**Centering Formula:**
- Difficulty_c = Difficulty - mean(Difficulty)
- mean(Difficulty_c) should be approximately 0 (within rounding error <0.001)
- SD(Difficulty_c) equals SD(Difficulty) (centering preserves variance)

### Column Naming Conventions

Per names.md (RQ 5.1 established conventions):
- `UID` (participant identifier, NOT composite_ID for this RQ - long format uses UID)
- `test` (test session: T1/T2/T3/T4)
- `item_name` (item tag identifier from master.xlsx)
- `TSVR_hours` (time variable, uppercase acronym + underscore + unit)
- `Difficulty` (original IRT difficulty parameter, NOT centered)
- `Difficulty_c` (centered difficulty, lowercase suffix _c for centered)

---

## Cross-RQ Dependencies

### Dependency Type 2: DERIVED Data from Other RQs (Dependencies Exist)

**This RQ requires outputs from:**

- **RQ 5.1** (IRT calibration baseline for difficulty estimates + TSVR mapping)
  - File 1: results/ch5/rq1/data/step03_difficulty.csv
    - Used in: Step 0 (merge item difficulty into response data)
    - Rationale: RQ 5.1 calibrates IRT model and estimates item difficulty parameters. This RQ uses those difficulty estimates as predictor of forgetting trajectories (cross-level interaction).
  - File 2: results/ch5/rq1/data/step00_tsvr_mapping.csv
    - Used in: Step 0 (merge TSVR time variable into response data)
    - Rationale: RQ 5.1 extracts TSVR (actual hours since encoding) per Decision D070. This RQ uses TSVR as time variable in LMM.
  - File 3: data/cache/dfData.csv (optional dependency if created by RQ 5.1)
    - Used in: Step 0 (load raw response data in long format)
    - Rationale: RQ 5.1 Step 0 creates dfData.csv from master.xlsx extraction. This RQ can reuse that file instead of re-extracting.

**Execution Order Constraint:**
1. RQ 5.1 must complete Steps 0-3 first (provides step03_difficulty.csv, step00_tsvr_mapping.csv, dfData.csv)
2. This RQ (5.15) executes after RQ 5.1 completes (uses RQ 5.1 outputs)

**Data Source Boundaries:**
- **RAW data:** Response data from dfData.csv (extracted from master.xlsx by RQ 5.1 or re-extracted)
- **DERIVED data:** Item difficulty estimates from RQ 5.1 IRT calibration (step03_difficulty.csv), TSVR time variable from RQ 5.1 extraction (step00_tsvr_mapping.csv)
- **Scope:** This RQ does NOT re-calibrate IRT models (uses RQ 5.1 difficulty as fixed predictor), does NOT re-extract TSVR (uses RQ 5.1 mapping)

**Validation:**
- Step 0: Check results/ch5/rq1/data/step03_difficulty.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch5/rq1/data/step00_tsvr_mapping.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 0: Check data/cache/dfData.csv exists (circuit breaker: EXPECTATIONS ERROR if absent, or re-extract from master.xlsx)
- If any dependency file missing -> quit with error -> user must execute RQ 5.1 first

**Reference:** Best practices Section 1.1 (EXPECTATIONS ERROR for missing prerequisite files)

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
- g_code (Step 14 workflow) will generate stepNN_*.py scripts with validation function calls
- bash execution (Step 14 workflow) will run analysis -> validation -> error on validation failure

**Downstream Agent Requirements:**
- **rq_tools:** MUST specify validation tool for EVERY analysis step (no exceptions)
- **rq_analysis:** MUST embed validation tool call for EVERY analysis step (no exceptions)
- **g_code:** MUST generate code with validation function calls (no exceptions)
- **rq_inspect:** MUST verify validation ran successfully (checks logs/stepNN_*.log for validation output)

### Validation Requirements By Step

#### Step 0: Load and Merge Data

**Analysis Tool:** (determined by rq_tools - likely pandas merge operations + custom data loading)
**Validation Tool:** (determined by rq_tools - likely custom data format validation)

**What Validation Checks:**
- Output file exists (data/step00_merged_data.csv)
- Expected row count (~40,000 rows: 100 UIDs x 4 tests x ~100 items)
- Expected column count (7 columns: UID, test, item_name, response, Difficulty, TSVR_hours, Days)
- No NaN in TSVR_hours (merge completeness check - all responses have time data)
- No NaN in Difficulty (merge completeness check - all items have difficulty estimates)
- Value ranges valid (response in {0,1}, Difficulty in [-6,6], TSVR_hours in [0,200], Days in {0,1,3,6})

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected ~40,000 rows, found 25,000")
- Log failure to logs/step00_merged_data.log
- Quit script immediately (do NOT proceed to Step 1)
- Check RQ 5.1 outputs exist and are complete (dependency issue)

---

#### Step 1: Center Predictors

**Analysis Tool:** (determined by rq_tools - likely pandas arithmetic operations)
**Validation Tool:** (determined by rq_tools - likely custom centering validation)

**What Validation Checks:**
- Output file exists (data/step01_centered_data.csv)
- Difficulty_c column added (8 columns total)
- Mean of Difficulty_c approximately 0 (within rounding error <0.001)
- SD of Difficulty_c equals SD of Difficulty (centering preserves variance)
- No NaN in Difficulty_c (centering should not introduce missing values)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Mean of Difficulty_c = 0.15, not approximately zero")
- Log failure to logs/step01_centered_data.log
- Quit immediately

---

#### Step 2: Fit Cross-Classified LMM

**Analysis Tool:** (determined by rq_tools - likely fit_lmm_trajectory_tsvr or custom pymer4 wrapper)
**Validation Tool:** (determined by rq_tools - likely validate_lmm_convergence)

**What Validation Checks:**
- Output files exist (step02_lmm_model_summary.txt, step02_fixed_effects.csv, step02_random_effects.csv, step02_model_object.pkl)
- Model converged successfully (convergence message from pymer4, no critical warnings)
- Fixed effects table has 4 rows (intercept + 2 main effects + 1 interaction)
- Random effects variance components > 0 (no singular fit, or documented if simplified model)
- Interaction term present: TSVR_hours:Difficulty_c in fixed effects
- No NaN in coefficients, SE, p-values

**Expected Behavior on Validation Failure:**
- Convergence failure: Quit with error, log attempted model formulas, suggest model simplification
- Singular fit: Document warning, attempt simplification per Step 2b-2c strategy
- Estimation errors: Log error details, invoke g_debug for diagnosis

---

#### Step 3: Extract Interaction Effect

**Analysis Tool:** (determined by rq_tools - likely pandas filtering + custom interpretation logic)
**Validation Tool:** (determined by rq_tools - likely validate_hypothesis_tests)

**What Validation Checks:**
- Output files exist (step03_interaction_summary.txt, step03_interaction_coefficient.csv)
- Interaction row extracted (term == "TSVR_hours:Difficulty_c")
- p_bonferroni calculated correctly (p_value * 15)
- Significance determination correct (significant = True if p_bonferroni < 0.0033)
- Direction determination correct (positive/negative/null based on estimate sign and significance)

**Expected Behavior on Validation Failure:**
- Interaction term missing: Quit with error, check Step 2 model fitting
- Invalid p-values: Quit with error, check Step 2 fixed effects extraction

---

#### Step 4: Validate LMM Assumptions

**Analysis Tool:** (determined by rq_tools - likely validate_lmm_assumptions_comprehensive)
**Validation Tool:** Meta-validation (check that comprehensive validation ran successfully)

**What Validation Checks:**
- Output files exist (step04_assumption_validation_report.txt, step04_diagnostic_plots.png, step04_assumption_tests.csv)
- All 6 assumptions tested (normality, homoscedasticity, random effects normality, autocorrelation, linearity, outliers)
- Diagnostic plots generated (PNG file size > 0 KB)
- Test statistics and p-values valid (no NaN, p-values in [0,1])
- Overall assessment provided (assumptions met / minor violations / major violations)

**Expected Behavior on Validation Failure:**
- Tool execution failure: Quit with error, check step02_model_object.pkl validity
- Assumption violations: Document in report, suggest remedial actions (not a failure, just flagged)

---

#### Step 5: Prepare Interaction Plot Data

**Analysis Tool:** (determined by rq_tools - likely custom prediction + aggregation)
**Validation Tool:** (determined by rq_tools - likely custom plot data format validation)

**What Validation Checks:**
- Output file exists (plots/step05_interaction_plot_data.csv)
- Expected row count (8 rows: 2 item types x 4 time points)
- Expected column count (5 columns: Days, ItemType, PredictedResponse, CI_lower, CI_upper)
- Value ranges valid (PredictedResponse, CI_lower, CI_upper in [0,1]; Days in {0,1,3,6})
- No NaN values (all predictions succeeded)
- CI_upper > CI_lower for all rows (valid confidence intervals)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 8 rows, found 4")
- Log failure to logs/step05_interaction_plot_data.log
- Quit immediately (do NOT proceed to rq_plots)

---

## Summary

**Total Steps:** 6 (Step 0-5: data loading, centering, LMM fitting, interaction extraction, assumption validation, plot data preparation)

**Estimated Runtime:** Medium (30-60 minutes total)
- Step 0: Low (<5 min - data loading/merging)
- Step 1: Low (<1 min - centering)
- Step 2: High (20-40 min - cross-classified LMM fitting with pymer4)
- Step 3: Low (<1 min - interaction extraction)
- Step 4: Medium (5-10 min - comprehensive assumption validation)
- Step 5: Low (<5 min - plot data preparation)

**Cross-RQ Dependencies:** RQ 5.1 (requires step03_difficulty.csv, step00_tsvr_mapping.csv, dfData.csv)

**Primary Outputs:**
- results/step02_lmm_model_summary.txt (fitted cross-classified LMM summary)
- results/step02_fixed_effects.csv (fixed effects with Bonferroni-corrected p-values)
- results/step03_interaction_coefficient.csv (Time x Difficulty_c interaction term)
- results/step03_interaction_summary.txt (interpretation with theoretical framing)
- results/step04_assumption_validation_report.txt (comprehensive LMM assumption checks)
- plots/step05_interaction_plot_data.csv (plot source CSV for easy vs hard item trajectories)

**Validation Coverage:** 100% (all 6 steps have validation requirements with 4-layer substance criteria)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_*.py scripts

---

**Version History:**
- v1.0 (2025-11-26): Initial plan created by rq_planner agent for RQ 5.15
