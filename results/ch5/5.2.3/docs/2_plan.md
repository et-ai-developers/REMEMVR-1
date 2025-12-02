# Analysis Plan: RQ 5.2.3 - Domain-Specific Age Effects on Forgetting

**Research Question:** 5.2.3
**Created:** 2025-11-26
**Updated:** 2025-12-02 (When domain excluded due to floor effect)
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Note on When Domain Exclusion

**When domain EXCLUDED** due to floor effect discovered in RQ 5.2.1:
- Performance at 6-9% probability throughout study (near 0% floor)
- 20/26 When items (77%) excluded for low discrimination in IRT calibration
- Cannot meaningfully assess age-related forgetting for When domain

**Analysis focuses on What vs Where comparison only.**

---

## Overview

This RQ examines whether age-related memory decline differs across episodic memory domains (What, Where) using a 3-way Age x Domain x Time interaction in LMM analysis. The analysis tests the hippocampal aging hypothesis: domains relying on hippocampal binding (Where) should show greater age-related vulnerability than familiarity-based memory (What, which relies on perirhinal cortex). Note: When domain excluded due to floor effect (see above).

**Pipeline:** LMM-only (uses DERIVED theta scores from RQ 5.1)

**Steps:** 6 total analysis steps (Step 0: data extraction + Steps 1-5: analysis)

**Estimated Runtime:** Medium (5-15 minutes total)
- Step 0: Low (<1 min) - DERIVED data extraction from RQ 5.1
- Step 1: Low (1-2 min) - Data preparation and reshaping
- Step 2: Medium (2-5 min) - LMM fitting with 3-way interaction
- Step 2b: Low (1-2 min) - LMM assumption validation
- Step 2c: Low (1-2 min) - Random effects model selection
- Step 3: Low (<1 min) - Extract 3-way interaction terms
- Step 4: Low (1-2 min) - Compute domain-specific age effects and post-hoc contrasts
- Step 5: Low (1-2 min) - Prepare visualization plot data

**Key Decisions Applied:**
- Decision D070: TSVR as time variable (actual hours since encoding, not nominal days)
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni for interaction tests)
- Decision D069: Dual-scale trajectory plots NOT applicable (age effects visualization uses age tertiles, not trajectories)

---

## Analysis Plan

This RQ requires 6 steps (Step 0 for data extraction, Steps 1-5 for analysis):

### Step 0: Get Data from RQ 5.1

**Dependencies:** RQ 5.1 must be complete (status.yaml shows rq_results: success)

**Complexity:** Low (<1 minute - DERIVED data extraction from completed RQ)

**Purpose:** Extract theta scores, TSVR mapping, and Age variable from RQ 5.1 outputs and dfData.csv

**Input:**

**File 1:** results/ch5/5.2.1/data/step04_lmm_input.csv
**Source:** RQ 5.2.1 Step 4 (LMM input with theta scores)
**Format:** CSV with columns:
  - composite_ID (string, format: UID_test, e.g., P001_T1)
  - domain (string, values: What, Where - When excluded)
  - test (string, values: T1, T2, T3, T4)
  - theta (float, IRT ability estimate, range typically -3 to 3)
**Expected Rows:** 800 (100 participants x 4 tests x 2 domains - When excluded)
**Note:** RQ 5.2.1 provides theta estimates for What/Where domains (When excluded due to floor effect)

**File 2:** results/ch5/5.1.1/data/step00_tsvr_mapping.csv
**Source:** RQ 5.1 Step 0 (TSVR extraction)
**Format:** CSV with columns:
  - composite_ID (string, format: UID_test)
  - test (string, values: T1, T2, T3, T4)
  - TSVR_hours (float, actual time since encoding in hours, range 0 to ~200)
**Expected Rows:** 400 (100 participants x 4 tests)

**File 3:** data/cache/dfData.csv
**Source:** Project-level demographic data
**Format:** CSV with columns:
  - UID (string, participant identifier, format: P###)
  - age (float, participant age in years, range typically 18-80)
  - [other demographic columns not used in this RQ]
**Expected Rows:** ~100 participants
**Note:** One row per participant (between-subjects variable)

**Processing:**
1. Read theta from RQ 5.2.1 (800 rows: 100 participants x 4 tests x 2 domains - When excluded)
2. Read tsvr_mapping.csv (400 rows: 100 participants x 4 tests)
3. Read dfData.csv Age column (100 rows: one per participant)
4. Verify all files exist (circuit breaker if RQ 5.2.1 incomplete)
5. **FILTER: Exclude When domain if present** (When excluded due to floor effect per RQ 5.2.1)
6. No transformations at this step (data passed to Step 1 as-is)

**Output:**

**File 1:** data/step00_theta_from_rq51.csv
**Format:** Copy of results/ch5/5.2.1/data/step04_lmm_input.csv (What/Where only)
**Columns:** composite_ID, domain, test, theta
**Expected Rows:** 800 (100 participants x 4 tests x 2 domains - When excluded)

**File 2:** data/step00_tsvr_from_rq51.csv
**Format:** Copy of results/ch5/5.1.1/data/step00_tsvr_mapping.csv
**Columns:** composite_ID, test, TSVR_hours
**Expected Rows:** 400 (100 participants x 4 tests)

**File 3:** data/step00_age_from_dfdata.csv
**Format:** Subset of dfData.csv with UID and age columns only
**Columns:** UID, age
**Expected Rows:** ~100 participants

**Validation Requirement:**
Validation tools MUST be used after data extraction. Specific validation tools will be determined by rq_tools based on DERIVED data extraction type. The rq_analysis agent will embed validation tool calls after the extraction tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_theta_from_rq51.csv: 800 rows x 4 columns (composite_ID: object, domain: object, test: object, theta: float64) - When excluded
- data/step00_tsvr_from_rq51.csv: 400 rows x 3 columns (composite_ID: object, test: object, TSVR_hours: float64)
- data/step00_age_from_dfdata.csv: ~100 rows x 2 columns (UID: object, age: float64)

*Value Ranges:*
- theta in [-3, 3] (IRT ability estimates from RQ 5.2.1)
- TSVR_hours in [0, 200] (actual time since encoding, T1=0, T4=~144-168 hours)
- age in [18, 80] (participant age in years, typical adult range)
- domain in {What, Where} (categorical, exactly 2 levels - When excluded)
- test in {T1, T2, T3, T4} (categorical, exactly 4 levels)

*Data Quality:*
- Theta file: All 800 rows present (100 participants x 4 tests x 2 domains, no missing combinations - When excluded)
- TSVR file: All 400 rows present (100 participants x 4 tests, no missing combinations)
- Age file: All ~100 participants present (one row per UID)
- No NaN values in theta, TSVR_hours, or age columns (complete data required)
- No duplicate composite_IDs within theta file
- No duplicate composite_IDs within TSVR file
- No duplicate UIDs within age file

*Log Validation:*
- Required: "Data extraction complete: 800 theta rows, 400 TSVR rows, ~100 age rows"
- Required: "All domains present: What, Where (When excluded due to floor effect)"
- Required: "All tests present: T1, T2, T3, T4"
- Forbidden: "ERROR", "FileNotFoundError", "RQ 5.2.1 incomplete"
- Acceptable warnings: None expected for data extraction

**Expected Behavior on Validation Failure:**
- If RQ 5.1 files missing: Raise error "RQ 5.1 must complete before RQ 5.2.3 (dependency)"
- If row counts mismatch: Raise error with specific counts (e.g., "Expected 1200 theta rows, found 1150")
- If NaN values detected: Raise error "Missing data in [column]: N rows affected"
- Log failure to logs/step00_get_data.log
- Quit immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause

**Expected Behavior:**
Extract DERIVED data from RQ 5.1 outputs and dfData.csv with no transformations. All merging and reshaping happens in Step 1.

---

### Step 1: Prepare LMM Input with Age Variable

**Dependencies:** Step 0 (requires theta, TSVR, and age data)

**Complexity:** Low (1-2 minutes - data merging and reshaping)

**Purpose:** Merge theta scores with TSVR and Age, grand-mean center Age, reshape to long format for LMM

**Input:**

**File 1:** data/step00_theta_from_rq51.csv (from Step 0)
**Format:** CSV with columns: composite_ID, domain, test, theta
**Expected Rows:** 1200 (100 participants x 4 tests x 3 domains)

**File 2:** data/step00_tsvr_from_rq51.csv (from Step 0)
**Format:** CSV with columns: composite_ID, test, TSVR_hours
**Expected Rows:** 400 (100 participants x 4 tests)

**File 3:** data/step00_age_from_dfdata.csv (from Step 0)
**Format:** CSV with columns: UID, age
**Expected Rows:** ~100 participants

**Processing:**

1. **Extract UID from composite_ID:**
   - Parse composite_ID (format: UID_test, e.g., P001_T1)
   - Create UID column (e.g., P001)

2. **Merge theta with TSVR:**
   - Left join theta_scores with tsvr_mapping on composite_ID and test
   - Verify all composite_IDs match (no missing TSVR values)

3. **Merge with Age:**
   - Left join result with age data on UID
   - Verify all UIDs match (no missing age values)

4. **Grand-mean center Age:**
   - Compute mean_age = mean(age) across all participants
   - Create Age_c = age - mean_age (centered age variable)
   - Rationale: Centering improves LMM convergence and interpretability (intercept = effect at mean age)

5. **Create time transformations:**
   - TSVR_hours already present (linear time variable per Decision D070)
   - Create log_TSVR = log(TSVR_hours + 1) (logarithmic time transformation)
   - Note: Adding 1 to handle TSVR_hours = 0 at encoding (T1)

6. **Treatment coding for Domain:**
   - Domain is categorical with 3 levels: What, Where, When
   - Treatment coding: What as reference category (least hippocampal-dependent, natural baseline)
   - Dummy variables: Domain_Where (1 if Where, 0 otherwise), Domain_When (1 if When, 0 otherwise)

7. **Verify data structure:**
   - Long format: One row per observation (participant x test x domain)
   - Expected: 1200 rows (100 participants x 4 tests x 3 domains)
   - Grouping: 12 rows per participant (4 tests x 3 domains)

**Output:**

**File 1:** data/step01_lmm_input.csv
**Format:** Long-format CSV (one row per observation)
**Columns:**
  - UID (string, participant identifier, e.g., P001)
  - composite_ID (string, UID_test, e.g., P001_T1)
  - test (string, T1/T2/T3/T4)
  - domain (string, What/Where/When)
  - theta (float, IRT ability estimate)
  - TSVR_hours (float, actual time since encoding)
  - log_TSVR (float, log(TSVR_hours + 1))
  - age (float, raw age in years)
  - Age_c (float, grand-mean centered age)
  - mean_age (float, grand mean age, constant for all rows)
**Expected Rows:** 1200 (100 participants x 4 tests x 3 domains)
**Expected Nulls:** None (all columns non-null after merges)

**File 2:** data/step01_preprocessing_summary.txt
**Format:** Text summary
**Content:**
  - Grand mean age: [value] years
  - Age range: [min, max] years
  - Age SD: [value] years
  - Centered age range: [min, max] (should be symmetric around 0)
  - TSVR range: [min, max] hours
  - N participants: [count]
  - N observations: [count]

**Validation Requirement:**
Validation tools MUST be used after data preparation tool execution. Specific validation tools will be determined by rq_tools based on data merging and transformation type. The rq_analysis agent will embed validation tool calls after the preparation tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_lmm_input.csv: 1200 rows x 10 columns (UID: object, composite_ID: object, test: object, domain: object, theta: float64, TSVR_hours: float64, log_TSVR: float64, age: float64, Age_c: float64, mean_age: float64)
- data/step01_preprocessing_summary.txt: text file exists

*Value Ranges:*
- theta in [-3, 3] (inherited from RQ 5.1)
- TSVR_hours in [0, 200] (T1=0, T4=~144-168 hours)
- log_TSVR in [0, 6] (log(1) = 0, log(201) = 5.3)
- age in [18, 80] (raw participant age)
- Age_c: symmetric around 0 (mean(Age_c) should be ~0 within floating point precision)
- mean_age in [30, 60] (typical sample mean age)
- domain in {What, Where, When}
- test in {T1, T2, T3, T4}

*Data Quality:*
- All 1200 rows present (100 participants x 4 tests x 3 domains)
- No NaN values in any column (complete data after merges)
- No duplicate rows (UID x test x domain combinations unique)
- Mean Age_c approximately 0 (within 1e-10 tolerance)
- Age_c range symmetric (|min(Age_c)| approximately equals max(Age_c))
- All UIDs have exactly 12 rows (4 tests x 3 domains)

*Log Validation:*
- Required: "Data preparation complete: 1200 rows created"
- Required: "Grand mean age: [value] years"
- Required: "Age centered: mean(Age_c) = [near-zero value]"
- Required: "All 100 participants have 12 observations"
- Forbidden: "ERROR", "NaN values detected", "Missing TSVR", "Missing age"
- Acceptable warnings: None expected for data preparation

**Expected Behavior on Validation Failure:**
- If TSVR merge fails: Raise error "Missing TSVR values for [N] composite_IDs"
- If Age merge fails: Raise error "Missing age values for [N] UIDs"
- If Age_c not centered: Raise error "Age centering failed: mean(Age_c) = [value], expected ~0"
- If row count mismatch: Raise error "Expected 1200 rows, found [N]"
- Log failure to logs/step01_prepare_lmm_input.log
- Quit immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose root cause

**Expected Behavior:**
Merge theta, TSVR, and age data, grand-mean center age, create time transformations, verify long-format structure (1200 rows, 10 columns, no NaN values).

---

### Step 2: Fit LMM with 3-Way Age x Domain x Time Interaction

**Dependencies:** Step 1 (requires prepared LMM input)

**Complexity:** Medium (2-5 minutes - LMM fitting with 3-way interaction)

**Purpose:** Fit Linear Mixed Model testing whether age effects on forgetting rate vary by memory domain

**Input:**

**File 1:** data/step01_lmm_input.csv (from Step 1)
**Format:** Long-format CSV
**Columns:** UID, composite_ID, test, domain, theta, TSVR_hours, log_TSVR, age, Age_c, mean_age
**Expected Rows:** 1200 (100 participants x 4 tests x 3 domains)

**Processing:**

**Model Formula:**
```
theta ~ TSVR_hours + log_TSVR + Age_c + domain +
        TSVR_hours:Age_c + log_TSVR:Age_c +
        TSVR_hours:domain + log_TSVR:domain +
        Age_c:domain +
        TSVR_hours:Age_c:domain + log_TSVR:Age_c:domain +
        (TSVR_hours | UID)
```

**Fixed Effects:**
- Main effects: TSVR_hours, log_TSVR, Age_c, domain (Where, When vs What reference)
- 2-way interactions: TSVR_hours:Age_c, log_TSVR:Age_c, TSVR_hours:domain, log_TSVR:domain, Age_c:domain
- 3-way interactions (PRIMARY HYPOTHESIS): TSVR_hours:Age_c:domain, log_TSVR:Age_c:domain

**Random Effects:**
- Random intercepts by participant: (1 | UID)
- Random slopes for time by participant: (TSVR_hours | UID)
- Note: Allows individual differences in baseline ability and forgetting rate

**Fitting Details:**
- REML = False (maximum likelihood for fixed effects inference)
- Decision D070: Use TSVR_hours (actual time since encoding, not nominal days 0/1/3/6)
- Treatment coding: What domain as reference (perirhinal-dependent, least vulnerable to aging)

**Interpretation:**
- TSVR_hours:Age_c:domain[Where]: Does age effect on linear forgetting rate differ for Where vs What?
- TSVR_hours:Age_c:domain[When]: Does age effect on linear forgetting rate differ for When vs What?
- log_TSVR:Age_c:domain[Where]: Does age effect on logarithmic forgetting rate differ for Where vs What?
- log_TSVR:Age_c:domain[When]: Does age effect on logarithmic forgetting rate differ for When vs What?

**Hypothesis Test:**
If EITHER 3-way interaction (linear or log) is significant at Bonferroni-corrected alpha = 0.025, the hippocampal aging hypothesis is supported (age effects differ by domain).

**Output:**

**File 1:** results/step02_lmm_model.pkl
**Format:** Pickle file (Python object)
**Content:** Fitted statsmodels MixedLM model object
**Note:** Required for Step 3 (extracting coefficients) and Step 4 (post-hoc contrasts)

**File 2:** results/step02_lmm_summary.txt
**Format:** Text file
**Content:**
  - Full model summary (fixed effects table, random effects variance, AIC, BIC, log-likelihood)
  - Number of observations, groups
  - Convergence status

**File 3:** data/step02_fixed_effects.csv
**Format:** CSV with fixed effects table
**Columns:**
  - term (string, coefficient name)
  - estimate (float, coefficient value)
  - se (float, standard error)
  - z (float, z-statistic)
  - p (float, p-value)
  - CI_lower (float, 95% confidence interval lower bound)
  - CI_upper (float, 95% confidence interval upper bound)
**Expected Rows:** ~20 rows (intercept + main effects + 2-way interactions + 3-way interactions)

**Validation Requirement:**
Validation tools MUST be used after LMM fitting tool execution. Specific validation tools will be determined by rq_tools based on LMM convergence and model diagnostics. The rq_analysis agent will embed validation tool calls after the fitting tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step02_lmm_model.pkl: pickle file exists (fitted model object)
- results/step02_lmm_summary.txt: text file exists
- data/step02_fixed_effects.csv: ~20 rows x 7 columns (term: object, estimate: float64, se: float64, z: float64, p: float64, CI_lower: float64, CI_upper: float64)

*Value Ranges:*
- estimate: unrestricted (can be positive or negative)
- se > 0 (standard errors must be positive)
- z: unrestricted (t-statistic can be positive or negative)
- p in [0, 1] (p-values must be valid probabilities)
- CI_lower < CI_upper (confidence intervals must be properly ordered)

*Data Quality:*
- All ~20 fixed effects terms present (intercept + main effects + interactions)
- No NaN values in estimate, se, z, p columns (convergence failure would produce NaN)
- 3-way interaction terms present: TSVR_hours:Age_c:domain[Where], TSVR_hours:Age_c:domain[When], log_TSVR:Age_c:domain[Where], log_TSVR:Age_c:domain[When]
- Model converged (check log for convergence status)

*Log Validation:*
- Required: "Model converged: True" OR "Optimization terminated successfully"
- Required: "Fixed effects extracted: [N] terms"
- Required: "3-way interactions present: TSVR_hours:Age_c:domain, log_TSVR:Age_c:domain"
- Forbidden: "ERROR", "Singular matrix", "Convergence failed", "NaN coefficients"
- Acceptable warnings: "The Hessian matrix at convergence is singular" (can occur with complex random effects, not fatal if model summary readable)

**Expected Behavior on Validation Failure:**
- If convergence fails: Raise error "LMM convergence failed: check model specification"
- If NaN coefficients: Raise error "NaN coefficients detected: [list terms]"
- If 3-way interactions missing: Raise error "3-way interaction terms not found in fixed effects"
- Log failure to logs/step02_fit_lmm.log
- Quit immediately (do NOT proceed to Step 2b)
- g_debug invoked to diagnose root cause (common causes: random effects too complex, insufficient data)

**Expected Behavior:**
Fit LMM with 3-way Age x Domain x Time interaction, extract fixed effects table, save model object for downstream steps. Model should converge successfully with all coefficients estimable.

---

### Step 2b: Validate LMM Assumptions

**Dependencies:** Step 2 (requires fitted LMM model)

**Complexity:** Low (1-2 minutes - diagnostic plots and assumption tests)

**Purpose:** Verify LMM assumptions before proceeding to inference (Step 3)

**Input:**

**File 1:** results/step02_lmm_model.pkl (from Step 2)
**Format:** Pickle file (fitted statsmodels MixedLM object)

**File 2:** data/step01_lmm_input.csv (from Step 1)
**Format:** Long-format CSV (used for residual diagnostics)

**Processing:**

**Assumption Checks (7 diagnostics per 1_concept.md):**

1. **Residual Normality:**
   - Generate Q-Q plot of marginal residuals
   - Shapiro-Wilk test (H0: residuals normally distributed)
   - Threshold: p > 0.05 indicates normality assumption satisfied
   - If violated: Note in report, consider robust standard errors

2. **Homoscedasticity:**
   - Plot residuals vs fitted values
   - Visual inspection for fanning pattern
   - If violated: Note in report, consider weighted LMM

3. **Random Effects Normality:**
   - Q-Q plot of random intercepts
   - Q-Q plot of random slopes (if present)
   - Visual inspection for deviations from normality
   - If violated: Note in report, may indicate outlier participants

4. **Independence (Autocorrelation):**
   - ACF plot of residuals (autocorrelation function)
   - Threshold: Lag-1 ACF < 0.1 indicates independence
   - If violated: Note in report, consider AR(1) error structure

5. **Linearity:**
   - Partial residual plots for Age_c and TSVR_hours
   - Visual inspection for linear relationships
   - If non-linear: Note in report, consider quadratic Age term

6. **Outliers/Influence:**
   - Cook's distance (threshold: D > 4/n = 4/100 = 0.04)
   - Identify influential observations
   - Report outliers, conduct sensitivity analysis if >5% of observations exceed threshold

7. **Convergence Diagnostics:**
   - Check for singularity warnings
   - Check gradient convergence
   - If warnings: Refit with simpler random structure (TSVR_hours || UID or 1 | UID)

**Output:**

**File 1:** results/step02b_assumption_diagnostics.txt
**Format:** Text summary
**Content:**
  - Residual normality: Shapiro-Wilk p-value, interpretation
  - Homoscedasticity: Visual assessment
  - Random effects normality: Visual assessment
  - Independence: Lag-1 ACF value
  - Linearity: Visual assessment
  - Outliers: Number of observations with Cook's D > 0.04
  - Convergence: Status (converged / warnings present)
  - Overall assessment: Pass / Conditional pass / Fail

**File 2:** plots/step02b_diagnostic_plots.png
**Format:** PNG image (multi-panel diagnostic plot)
**Panels:**
  - Q-Q plot (residuals)
  - Residuals vs fitted values
  - ACF plot
  - Cook's distance plot
**Dimensions:** 1200 x 1200 pixels @ 300 DPI

**Validation Requirement:**
Validation tools MUST be used after assumption checking tool execution. Specific validation tools will be determined by rq_tools based on diagnostic output format. The rq_analysis agent will embed validation tool calls after the assumption checking tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step02b_assumption_diagnostics.txt: text file exists
- plots/step02b_diagnostic_plots.png: PNG image exists

*Value Ranges:*
- Shapiro-Wilk p-value in [0, 1]
- Lag-1 ACF in [-1, 1] (autocorrelation coefficient bounded)
- Cook's distance >= 0 (non-negative by definition)

*Data Quality:*
- All 7 diagnostics reported (residual normality, homoscedasticity, random effects normality, independence, linearity, outliers, convergence)
- Overall assessment stated (Pass / Conditional pass / Fail)
- If violations detected: Specific recommendations provided

*Log Validation:*
- Required: "Assumption validation complete: [N] checks performed"
- Required: "Overall assessment: [Pass/Conditional/Fail]"
- Forbidden: "ERROR", "Diagnostic generation failed"
- Acceptable warnings: "Residual normality: p < 0.05 (minor violation)" (LMM robust to mild non-normality with N=1200)

**Expected Behavior on Validation Failure:**
- If diagnostic generation fails: Raise error "Assumption diagnostics failed: [specific failure]"
- If major violations detected: Flag in report, proceed with caution (not fatal - inference still valid for exploratory thesis)
- Log results to logs/step02b_validate_assumptions.log
- Proceed to Step 2c regardless (assumption checks inform interpretation, not blocking)

**Expected Behavior:**
Generate diagnostic plots and statistical tests for LMM assumptions. Report results with interpretations. Flag violations for user review but do not block workflow (exploratory thesis tolerates minor violations).

---

### Step 2c: Model Selection for Random Effects

**Dependencies:** Step 2 (requires fitted LMM model) and Step 2b (assumptions validated)

**Complexity:** Low (1-2 minutes - fit 3 models, compare via LRT)

**Purpose:** Select optimal random effects structure via likelihood ratio test

**Input:**

**File 1:** data/step01_lmm_input.csv (from Step 1)
**Format:** Long-format CSV (used for model fitting)

**Processing:**

**Candidate Models (per 1_concept.md Step 2c):**

1. **Full model:** theta ~ [fixed effects] + (TSVR_hours | UID)
   - Random intercepts + random slopes, correlated

2. **Uncorrelated model:** theta ~ [fixed effects] + (TSVR_hours || UID)
   - Random intercepts + random slopes, uncorrelated

3. **Intercept-only model:** theta ~ [fixed effects] + (1 | UID)
   - Random intercepts only, no random slopes

**Model Comparison:**
- Fit all 3 models with REML = True (for random effects comparison)
- Extract -2 log-likelihood for each model
- Compute LRT chi-square statistics:
  - Full vs Uncorrelated: df = 1 (testing correlation parameter)
  - Full vs Intercept-only: df = 2 (testing slope variance + correlation)
  - Uncorrelated vs Intercept-only: df = 1 (testing slope variance)
- Select most parsimonious model that significantly improves fit (p < 0.05)

**Refit Selected Model:**
- Refit selected model with REML = False (for fixed effects inference in Step 3)
- Replace step02_lmm_model.pkl with selected model
- Note: If Full model fails to converge, fall back to Uncorrelated or Intercept-only

**Output:**

**File 1:** results/step02c_model_selection.txt
**Format:** Text summary
**Content:**
  - Full model: -2 log-likelihood, convergence status
  - Uncorrelated model: -2 log-likelihood, convergence status
  - Intercept-only model: -2 log-likelihood, convergence status
  - LRT results: chi-square, df, p-value for each comparison
  - Selected model: [Full / Uncorrelated / Intercept-only]
  - Rationale: [Why this model was selected]

**File 2:** results/step02_lmm_model.pkl (UPDATED)
**Format:** Pickle file (fitted statsmodels MixedLM object with selected random structure)
**Note:** Replaces Step 2 output with selected model, refit with REML=False

**File 3:** data/step02_fixed_effects.csv (UPDATED)
**Format:** CSV with fixed effects table from selected model
**Note:** Replaces Step 2 output with fixed effects from selected model

**Validation Requirement:**
Validation tools MUST be used after model selection tool execution. Specific validation tools will be determined by rq_tools based on model comparison output format. The rq_analysis agent will embed validation tool calls after the model selection tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step02c_model_selection.txt: text file exists
- results/step02_lmm_model.pkl: pickle file exists (updated with selected model)
- data/step02_fixed_effects.csv: CSV file exists (updated with selected model fixed effects)

*Value Ranges:*
- -2 log-likelihood < 0 (log-likelihood is negative, -2LL is positive)
- LRT chi-square >= 0 (non-negative by definition)
- LRT p-value in [0, 1]

*Data Quality:*
- All 3 models fit successfully OR convergence failures documented
- Selected model converged (not failed model)
- Selected model rationale provided
- LRT comparisons performed (3 comparisons: Full vs Uncorrelated, Full vs Intercept-only, Uncorrelated vs Intercept-only)

*Log Validation:*
- Required: "Model selection complete: [Selected model] chosen"
- Required: "Refit with REML=False: [convergence status]"
- Forbidden: "ERROR", "All models failed to converge"
- Acceptable warnings: "Full model failed to converge: falling back to Uncorrelated model"

**Expected Behavior on Validation Failure:**
- If all models fail to converge: Raise error "Model selection failed: no models converged"
- If selected model not refit: Raise error "Selected model refit failed"
- Log failure to logs/step02c_model_selection.log
- Quit immediately (do NOT proceed to Step 3)
- g_debug invoked to diagnose root cause

**Expected Behavior:**
Fit 3 candidate random effects structures, compare via LRT, select most parsimonious model that significantly improves fit, refit with REML=False for fixed effects inference in Step 3.

---

### Step 3: Extract 3-Way Interaction Terms and Test Hypothesis

**Dependencies:** Step 2c (requires selected LMM model with REML=False)

**Complexity:** Low (<1 minute - coefficient extraction and hypothesis testing)

**Purpose:** Extract and test 3-way Age x Domain x Time interaction terms (primary hypothesis)

**Input:**

**File 1:** results/step02_lmm_model.pkl (from Step 2c - selected model, REML=False)
**Format:** Pickle file (fitted statsmodels MixedLM object)

**File 2:** data/step02_fixed_effects.csv (from Step 2c - selected model fixed effects)
**Format:** CSV with columns: term, estimate, se, z, p, CI_lower, CI_upper
**Expected Rows:** ~20 rows (all fixed effects terms)

**Processing:**

**Extract 3-Way Interaction Terms:**
1. Filter fixed_effects.csv for terms containing "TSVR_hours:Age_c:domain" and "log_TSVR:Age_c:domain"
2. Expected terms (4 total):
   - TSVR_hours:Age_c:domain[Where] (linear time x age x Where domain)
   - TSVR_hours:Age_c:domain[When] (linear time x age x When domain)
   - log_TSVR:Age_c:domain[Where] (log time x age x Where domain)
   - log_TSVR:Age_c:domain[When] (log time x age x When domain)

**Apply Bonferroni Correction:**
- Family-wise error rate: 2 hypothesis tests (linear 3-way interaction, log 3-way interaction)
- Bonferroni alpha: 0.05 / 2 = 0.025
- Test 1: Are BOTH linear 3-way terms jointly significant? (omnibus test)
- Test 2: Are BOTH log 3-way terms jointly significant? (omnibus test)
- Note: Individual term p-values also reported (uncorrected)

**Hypothesis Decision:**
- If EITHER omnibus test significant at alpha = 0.025: Hypothesis supported (age effects differ by domain)
- If BOTH omnibus tests non-significant: Hypothesis not supported (age effects uniform across domains)

**Output:**

**File 1:** data/step03_interaction_terms.csv
**Format:** CSV with 3-way interaction terms only
**Columns:** term, estimate, se, z, p, p_bonferroni, CI_lower, CI_upper
**Expected Rows:** 4 (two linear + two log 3-way interactions)
**Note:** p_bonferroni = min(p * 2, 1.0) for each individual term

**File 2:** results/step03_hypothesis_test.txt
**Format:** Text summary
**Content:**
  - Primary hypothesis: "Age effects on forgetting rate vary by memory domain"
  - Bonferroni-corrected alpha: 0.025
  - Linear 3-way interaction test:
    - TSVR_hours:Age_c:domain[Where]: estimate, p-value, interpretation
    - TSVR_hours:Age_c:domain[When]: estimate, p-value, interpretation
    - Omnibus test: chi-square, df=2, p-value (joint test)
  - Log 3-way interaction test:
    - log_TSVR:Age_c:domain[Where]: estimate, p-value, interpretation
    - log_TSVR:Age_c:domain[When]: estimate, p-value, interpretation
    - Omnibus test: chi-square, df=2, p-value (joint test)
  - Overall decision: Hypothesis [supported / not supported]
  - Interpretation: [Age effects differ by domain / Age effects uniform across domains]

**Validation Requirement:**
Validation tools MUST be used after hypothesis testing tool execution. Specific validation tools will be determined by rq_tools based on hypothesis test output format (Decision D068 compliance for dual p-values). The rq_analysis agent will embed validation tool calls after the hypothesis testing tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_interaction_terms.csv: 4 rows x 8 columns (term: object, estimate: float64, se: float64, z: float64, p: float64, p_bonferroni: float64, CI_lower: float64, CI_upper: float64)
- results/step03_hypothesis_test.txt: text file exists

*Value Ranges:*
- estimate: unrestricted (can be positive or negative)
- se > 0 (standard errors must be positive)
- z: unrestricted (z-statistic can be positive or negative)
- p in [0, 1] (uncorrected p-values)
- p_bonferroni in [0, 1] (Bonferroni-corrected p-values)
- CI_lower < CI_upper (confidence intervals properly ordered)

*Data Quality:*
- Exactly 4 rows (2 linear + 2 log 3-way interactions)
- All expected terms present: TSVR_hours:Age_c:domain[Where], TSVR_hours:Age_c:domain[When], log_TSVR:Age_c:domain[Where], log_TSVR:Age_c:domain[When]
- No NaN values in any column
- p_bonferroni correctly computed (p_bonferroni = min(p * 2, 1.0) for each term)
- Decision D068 compliance: BOTH uncorrected (p) AND corrected (p_bonferroni) p-values reported

*Log Validation:*
- Required: "3-way interaction terms extracted: 4 terms"
- Required: "Bonferroni correction applied: alpha = 0.025"
- Required: "Hypothesis test complete: [supported/not supported]"
- Forbidden: "ERROR", "Missing interaction terms", "p-values invalid"
- Acceptable warnings: None expected for hypothesis testing

**Expected Behavior on Validation Failure:**
- If interaction terms missing: Raise error "3-way interaction terms not found in fixed effects"
- If p-values invalid: Raise error "Invalid p-values: [list problematic values]"
- If Bonferroni correction not applied: Raise error "Decision D068 violation: missing corrected p-values"
- Log failure to logs/step03_extract_interactions.log
- Quit immediately (do NOT proceed to Step 4)
- g_debug invoked to diagnose root cause

**Expected Behavior:**
Extract 4 three-way interaction terms, apply Bonferroni correction (alpha = 0.025 for 2 omnibus tests), report hypothesis decision (supported if EITHER omnibus test significant).

---

### Step 4: Compute Domain-Specific Age Effects and Post-Hoc Contrasts

**Dependencies:** Step 3 (requires interaction terms and hypothesis test result)

**Complexity:** Low (1-2 minutes - marginal effects computation and pairwise contrasts)

**Purpose:** Quantify age effect on forgetting rate for each domain, test pairwise differences

**Input:**

**File 1:** results/step02_lmm_model.pkl (from Step 2c - selected model)
**Format:** Pickle file (fitted statsmodels MixedLM object)

**File 2:** data/step02_fixed_effects.csv (from Step 2c - all fixed effects)
**Format:** CSV with columns: term, estimate, se, z, p, CI_lower, CI_upper

**Processing:**

**Compute Domain-Specific Age Effects:**
1. Extract age effect on forgetting rate for each domain at Day 3 (TSVR = 72 hours, midpoint of observation window)
2. For What domain (reference): Age effect = coefficient(TSVR_hours:Age_c) + coefficient(log_TSVR:Age_c) * d(log(72+1))/d(TSVR)
3. For Where domain: Age effect = What effect + coefficient(TSVR_hours:Age_c:domain[Where]) + coefficient(log_TSVR:Age_c:domain[Where]) * d(log(72+1))/d(TSVR)
4. For When domain: Age effect = What effect + coefficient(TSVR_hours:Age_c:domain[When]) + coefficient(log_TSVR:Age_c:domain[When]) * d(log(72+1))/d(TSVR)
5. Compute standard errors via delta method
6. Test hypothesis: Where/When show stronger age-related decline than What (negative age effects larger in magnitude)

**Post-Hoc Pairwise Contrasts (if Step 3 hypothesis supported):**
- Compare age x time slopes across all domain pairs:
  1. Where vs What (age effect difference)
  2. When vs What (age effect difference)
  3. Where vs When (age effect difference)
- Apply Tukey HSD correction for 3 pairwise comparisons
- Critical value: q(3 groups, df) from Tukey distribution
- Report BOTH uncorrected and Tukey-corrected p-values per Decision D068

**Output:**

**File 1:** data/step04_age_effects_by_domain.csv
**Format:** CSV with domain-specific age effects
**Columns:**
  - domain (string, What/Where/When)
  - age_effect (float, effect of 1-year age increase on forgetting rate at Day 3)
  - se (float, standard error)
  - z (float, z-statistic)
  - p (float, p-value for age effect != 0)
  - CI_lower (float, 95% CI lower bound)
  - CI_upper (float, 95% CI upper bound)
**Expected Rows:** 3 (one per domain)
**Interpretation:** Negative age_effect means older adults show steeper forgetting (worse memory retention)

**File 2:** data/step04_post_hoc_contrasts.csv
**Format:** CSV with pairwise domain comparisons
**Columns:**
  - contrast (string, e.g., "Where vs What", "When vs What", "Where vs When")
  - estimate (float, difference in age effects)
  - se (float, standard error)
  - z (float, z-statistic)
  - p_uncorrected (float, uncorrected p-value)
  - p_tukey (float, Tukey HSD corrected p-value)
  - CI_lower (float, 95% CI lower bound)
  - CI_upper (float, 95% CI upper bound)
**Expected Rows:** 3 (all pairwise domain comparisons)
**Note:** Decision D068 compliance: BOTH uncorrected and corrected p-values reported

**File 3:** results/step04_summary.txt
**Format:** Text summary
**Content:**
  - Domain-specific age effects:
    - What: [age_effect] � [se], p = [p]
    - Where: [age_effect] � [se], p = [p]
    - When: [age_effect] � [se], p = [p]
  - Pairwise contrasts:
    - Where vs What: [estimate] � [se], p_uncorrected = [p], p_tukey = [p]
    - When vs What: [estimate] � [se], p_uncorrected = [p], p_tukey = [p]
    - Where vs When: [estimate] � [se], p_uncorrected = [p], p_tukey = [p]
  - Ordering hypothesis test: Age effect When > Where > What?
    - Result: [supported / not supported]
  - Interpretation: [Domain-specific vulnerability to aging]

**Validation Requirement:**
Validation tools MUST be used after post-hoc contrast tool execution. Specific validation tools will be determined by rq_tools based on contrast output format (Decision D068 compliance for dual p-values). The rq_analysis agent will embed validation tool calls after the contrast tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_age_effects_by_domain.csv: 3 rows x 7 columns (domain: object, age_effect: float64, se: float64, z: float64, p: float64, CI_lower: float64, CI_upper: float64)
- data/step04_post_hoc_contrasts.csv: 3 rows x 8 columns (contrast: object, estimate: float64, se: float64, z: float64, p_uncorrected: float64, p_tukey: float64, CI_lower: float64, CI_upper: float64)
- results/step04_summary.txt: text file exists

*Value Ranges:*
- age_effect: unrestricted (can be positive or negative, expected negative for forgetting)
- se > 0 (standard errors must be positive)
- z: unrestricted (z-statistic can be positive or negative)
- p in [0, 1], p_uncorrected in [0, 1], p_tukey in [0, 1]
- CI_lower < CI_upper (confidence intervals properly ordered)

*Data Quality:*
- Age effects file: exactly 3 rows (What, Where, When)
- Post-hoc contrasts file: exactly 3 rows (Where vs What, When vs What, Where vs When)
- No NaN values in any column
- Decision D068 compliance: BOTH p_uncorrected AND p_tukey columns present in contrasts file
- All domains represented: What, Where, When

*Log Validation:*
- Required: "Age effects computed: 3 domains"
- Required: "Post-hoc contrasts computed: 3 pairwise comparisons"
- Required: "Tukey HSD correction applied"
- Forbidden: "ERROR", "Missing domain", "Invalid p-values"
- Acceptable warnings: None expected for post-hoc contrasts

**Expected Behavior on Validation Failure:**
- If age effects missing: Raise error "Age effects computation failed: [specific failure]"
- If contrasts missing: Raise error "Post-hoc contrasts failed: [specific failure]"
- If Decision D068 violated: Raise error "Missing corrected p-values: Tukey column required"
- Log failure to logs/step04_compute_contrasts.log
- Quit immediately (do NOT proceed to Step 5)
- g_debug invoked to diagnose root cause

**Expected Behavior:**
Compute age effect on forgetting rate for each domain (What, Where, When), perform pairwise contrasts with Tukey HSD correction, report BOTH uncorrected and corrected p-values per Decision D068.

---

### Step 5: Prepare Visualization Plot Data

**Dependencies:** Step 4 (requires age effects and LMM predictions)

**Complexity:** Low (1-2 minutes - data aggregation for plotting)

**Purpose:** Create plot source CSV for multi-panel age effects visualization (Option B architecture)

**CRITICAL NOTE:** Plot data preparation IS an analysis step. It:
- Gets executed in Step 14 CODE EXECUTION LOOP (g_code -> bash -> rq_inspect)
- MUST have validation requirements (same as any analysis step)
- Outputs to plots/*.csv (not data/*.csv) but still validated by rq_inspect
- Created by g_code during analysis (NOT by rq_plots during visualization)

**Plot Description:** Multi-panel plot (3 panels: What, Where, When) showing age effects on forgetting trajectories. Within each panel: Age tertiles (Young/Middle/Older) with separate trajectories, observed means with 95% CIs, model predictions overlaid.

**Input:**

**File 1:** data/step01_lmm_input.csv (from Step 1)
**Format:** Long-format CSV with columns: UID, composite_ID, test, domain, theta, TSVR_hours, log_TSVR, age, Age_c, mean_age
**Expected Rows:** 1200 (100 participants x 4 tests x 3 domains)

**File 2:** results/step02_lmm_model.pkl (from Step 2c - selected model)
**Format:** Pickle file (for generating model predictions)

**File 3:** data/step04_age_effects_by_domain.csv (from Step 4)
**Format:** CSV with domain-specific age effects

**Processing:**

**Create Age Tertiles (for visualization only):**
1. Compute age tertiles across all participants:
   - Young: age <= 33rd percentile
   - Middle: 33rd percentile < age <= 67th percentile
   - Older: age > 67th percentile
2. Assign tertile labels to each observation
3. Note: Analysis uses continuous Age_c (not tertiles), tertiles for interpretable plotting only

**Aggregate Observed Means:**
1. Group by domain + test + age_tertile
2. Compute mean(theta), 95% CI for each group
3. Add TSVR_hours (mean per test: T1=0, T2=~24, T3=~72, T4=~144)

**Generate Model Predictions:**
1. Create prediction grid: domain x TSVR_hours (0 to 168 in steps of 1) x age_tertile_mean
2. Use fitted LMM to predict theta for each grid point
3. Add 95% prediction intervals

**Merge Observed and Predicted:**
1. Combine observed means with model predictions
2. Create unified data structure for plotting
3. Separate datasets by domain (3 panels)

**Output:**

**File 1:** plots/step05_age_effects_plot_data.csv
**Format:** Plot source CSV
**Columns:**
  - domain (string, What/Where/When)
  - age_tertile (string, Young/Middle/Older)
  - TSVR_hours (float, time since encoding in hours)
  - theta_observed (float, observed mean theta, NaN for prediction-only rows)
  - CI_lower_observed (float, observed 95% CI lower bound, NaN for prediction-only rows)
  - CI_upper_observed (float, observed 95% CI upper bound, NaN for prediction-only rows)
  - theta_predicted (float, model predicted theta)
  - CI_lower_predicted (float, predicted 95% CI lower bound)
  - CI_upper_predicted (float, predicted 95% CI upper bound)
  - data_type (string, "observed" or "predicted")
**Expected Rows:** ~600 rows (3 domains x 3 age tertiles x (4 observed timepoints + ~60 predicted timepoints))

**Required Data Sources:**
- data/step01_lmm_input.csv (theta, TSVR, age for observed means)
- results/step02_lmm_model.pkl (model predictions)
- data/step04_age_effects_by_domain.csv (domain-specific effects for interpretation)

**Aggregation Logic:**
1. Create age tertiles from continuous age variable (tertiles for visualization only)
2. Group observed data by domain + test + age_tertile, compute mean theta + 95% CI
3. Generate prediction grid: domain x TSVR_hours (0-168) x age_tertile_mean
4. Predict theta from LMM for all grid points with 95% prediction intervals
5. Merge observed and predicted into unified dataset
6. Sort by domain, age_tertile, TSVR_hours
7. Save to plots/step05_age_effects_plot_data.csv

**Validation Requirement:**
Validation tools MUST be used after plot data preparation tool execution. Specific validation tools will be determined by rq_tools based on plot data format requirements. The rq_analysis agent will embed validation tool calls after the plot data preparation tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- plots/step05_age_effects_plot_data.csv exists (exact path)
- Expected rows: ~600 (3 domains x 3 age tertiles x ~67 timepoints per group)
- Expected columns: 10 (domain, age_tertile, TSVR_hours, theta_observed, CI_lower_observed, CI_upper_observed, theta_predicted, CI_lower_predicted, CI_upper_predicted, data_type)
- Data types: string (domain, age_tertile, data_type), float (all other columns)

*Value Ranges:*
- TSVR_hours in [0, 168] (0=encoding, 168=1 week)
- theta_observed in [-3, 3] (IRT ability range, NaN for predicted-only rows acceptable)
- theta_predicted in [-3, 3] (model predictions within IRT range)
- CI bounds in [-3, 3] (confidence intervals within IRT range)
- domain in {What, Where, When} (exactly 3 levels)
- age_tertile in {Young, Middle, Older} (exactly 3 levels)
- data_type in {observed, predicted} (exactly 2 types)

*Data Quality:*
- All 3 domains represented (What, Where, When)
- All 3 age tertiles represented (Young, Middle, Older)
- Observed data rows: NaN in predicted columns acceptable
- Predicted data rows: NaN in observed columns acceptable
- No duplicate rows (domain x age_tertile x TSVR_hours combinations unique within data_type)
- Distribution check: CI_upper > CI_lower for all non-NaN rows

*Log Validation:*
- Required: "Plot data preparation complete: ~600 rows created"
- Required: "All domains represented: What, Where, When"
- Required: "All age tertiles represented: Young, Middle, Older"
- Required: "Observed data: [N] rows, Predicted data: [M] rows"
- Forbidden: "ERROR", "NaN values in critical columns", "Missing domain", "Missing age tertile"
- Acceptable warnings: "NaN in observed columns for predicted data rows" (expected per design)

**Expected Behavior on Validation Failure:**
- If row count unexpected: Raise error "Expected ~600 rows, found [N]"
- If domains missing: Raise error "Missing domains: [list]"
- If age tertiles missing: Raise error "Missing age tertiles: [list]"
- If value ranges violated: Raise error "Value out of bounds: [column] = [value]"
- Log failure to logs/step05_prepare_plot_data.log
- Quit immediately (do NOT proceed to rq_plots)
- g_debug invoked to diagnose root cause

**Plotting Function (rq_plots will call):** Multi-panel age effects plot with observed means and model predictions
- rq_plots agent maps this description to specific tools/plots.py function
- Plot reads plots/step05_age_effects_plot_data.csv (created by this step)
- No data aggregation in rq_plots (visualization only per Option B)
- 3 panels (What, Where, When), each with 3 age tertiles (Young, Middle, Older)
- Observed means as points with error bars, model predictions as lines with confidence bands

**Expected Behavior:**
Create plot source CSV with observed means (grouped by domain x test x age tertile) and model predictions (domain x TSVR_hours x age tertile), verify all domains and tertiles represented, output to plots/ folder for rq_plots consumption.

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 -> Step 1:**
- Input: 3 separate files (theta from RQ 5.1, TSVR from RQ 5.1, age from dfData.csv)
- Output: Merged long-format LMM input (1200 rows, 10 columns)
- Transformation: Merge on composite_ID and UID, grand-mean center age, create time transformations

**Step 1 -> Step 2:**
- Input: Long-format LMM input (1200 rows, 10 columns)
- Output: Fitted LMM model object + fixed effects table
- Transformation: LMM fitting with 3-way interaction, extract coefficients

**Step 2 -> Step 2b:**
- Input: Fitted LMM model object
- Output: Diagnostic plots and assumption test results
- Transformation: Residual extraction, Q-Q plots, ACF plots, Cook's distance

**Step 2 -> Step 2c:**
- Input: Long-format LMM input (for refitting)
- Output: Selected model object (updated) + model selection report
- Transformation: Fit 3 candidate models, LRT comparison, refit selected model

**Step 2c -> Step 3:**
- Input: Selected LMM model object + fixed effects table
- Output: 3-way interaction terms only (4 rows)
- Transformation: Filter fixed effects for 3-way interactions, apply Bonferroni correction

**Step 2c -> Step 4:**
- Input: Selected LMM model object + fixed effects table
- Output: Domain-specific age effects + pairwise contrasts
- Transformation: Marginal effects computation, Tukey HSD contrasts

**Step 1 + Step 2c + Step 4 -> Step 5:**
- Input: Long-format LMM input + fitted model + age effects
- Output: Plot source CSV (~600 rows)
- Transformation: Create age tertiles, aggregate observed means, generate model predictions, merge

### Column Naming Conventions

Per names.md (from RQ 5.1):
- UID: participant identifier (format: P### with leading zeros)
- composite_ID: UID_test (format: P001_T1)
- test: test session (T1, T2, T3, T4)
- domain: memory domain (What, Where, When)
- theta: IRT ability estimate (lowercase)
- TSVR_hours: time since VR in hours (uppercase acronym + underscore + unit)
- Age_c: grand-mean centered age (uppercase A, lowercase ge, _c suffix)

### Data Type Constraints

**String columns (categorical):**
- UID, composite_ID, test, domain, age_tertile (categorical factor variables)

**Float columns (continuous):**
- theta, TSVR_hours, log_TSVR, age, Age_c, mean_age (numeric predictors/outcomes)

**Nullable columns:**
- theta_observed, CI_lower_observed, CI_upper_observed (NaN for predicted-only rows in Step 5 output)

**Non-nullable columns:**
- All columns in Steps 0-4 outputs (complete data required for LMM fitting)

### Format Migrations

**Wide to Long (Step 1):**
- Input: theta scores already in long format from RQ 5.1 (no wide-to-long needed)
- Note: This RQ does NOT require wide-to-long transformation (data already long)

**Merging (Step 1):**
- Merge theta + TSVR on composite_ID (1:1 merge, 1200 rows)
- Merge result + age on UID (many:1 merge, 1200 rows)
- All merges are left joins (keep all theta observations, add TSVR and age)

**Aggregation (Step 5):**
- Group by domain + test + age_tertile
- Compute mean(theta), 95% CI
- Result: ~36 observed mean rows (3 domains x 4 tests x 3 age tertiles)
- Combine with ~564 predicted rows (3 domains x 3 age tertiles x ~63 timepoints per group)

---

## Cross-RQ Dependencies

### Dependency Type: DERIVED Data from RQ 5.1 (Dependencies Exist)

**This RQ requires outputs from:**
- **RQ 5.1** (Domain-Specific Forgetting Trajectories)
  - File 1: results/ch5/5.1.1/data/step03_theta_scores.csv (IRT ability estimates for What/Where/When domains)
  - File 2: results/ch5/5.1.1/data/step00_tsvr_mapping.csv (TSVR actual hours mapping)
  - Used in: Step 0 (get data from RQ 5.1)
  - Rationale: RQ 5.1 establishes domain-specific theta trajectories. This RQ tests whether age moderates those trajectories differently by domain.

**Execution Order Constraint:**
1. RQ 5.1 must complete first (provides theta_scores.csv and tsvr_mapping.csv)
2. This RQ (5.2.3) executes second (uses RQ 5.1 theta as outcome variable, tests age interactions)

**Data Source Boundaries:**
- **RAW data:** Age from data/cache/dfData.csv (extracted directly, no RQ dependencies)
- **DERIVED data:** Theta scores and TSVR from RQ 5.1 (dependency on completed RQ)
- **Scope:** This RQ does NOT re-calibrate IRT models (uses RQ 5.1 theta as-is, tests age as moderator)

**Validation:**
- Step 0: Check results/ch5/5.1.1/data/step03_theta_scores.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch5/5.1.1/data/step00_tsvr_mapping.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch5/5.1.1/status.yaml shows rq_results: success (circuit breaker: EXPECTATIONS ERROR if RQ 5.1 incomplete)
- If any file missing -> quit with error -> user must execute RQ 5.1 first

**Reference:** Specification section 5.1.6 (Data Source Boundaries) and 1_concept.md Step 0 (Get Data from RQ 5.1)

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

**Step 0: Get Data from RQ 5.1**
- Analysis Tool: (determined by rq_tools - likely custom DERIVED data extraction)
- Validation Tool: (determined by rq_tools - likely tools.validation.validate_data_extraction)
- What Validation Checks: File existence, row counts (1200 theta, 400 TSVR, ~100 age), column presence, no NaN values, domain/test completeness
- On Failure: Quit with error "RQ 5.1 dependency missing: [specific file]", log to logs/step00_get_data.log, g_debug invoked

**Step 1: Prepare LMM Input**
- Analysis Tool: (determined by rq_tools - likely custom merge/reshape function)
- Validation Tool: (determined by rq_tools - likely tools.validation.validate_lmm_input)
- What Validation Checks: Merge completeness (1200 rows, no NaN), Age_c centering (mean ~0), time transformations (log_TSVR >= 0), long format structure
- On Failure: Quit with error "Data preparation failed: [specific check]", log to logs/step01_prepare_lmm_input.log, g_debug invoked

**Step 2: Fit LMM**
- Analysis Tool: (determined by rq_tools - likely tools.analysis_lmm.fit_lmm_trajectory_tsvr)
- Validation Tool: (determined by rq_tools - likely tools.validation.validate_lmm_convergence)
- What Validation Checks: Model convergence, fixed effects estimable (no NaN coefficients), 3-way interaction terms present, AIC/BIC finite
- On Failure: Quit with error "LMM convergence failed: [diagnostic]", log to logs/step02_fit_lmm.log, g_debug invoked

**Step 2b: Validate LMM Assumptions**
- Analysis Tool: (determined by rq_tools - likely tools.validation.validate_lmm_assumptions_comprehensive)
- Validation Tool: (determined by rq_tools - may be same as analysis tool, or separate meta-validation)
- What Validation Checks: Diagnostic plots generated, Shapiro-Wilk p-value computed, ACF lag-1 computed, Cook's D computed, overall assessment stated
- On Failure: Flag violations in report, proceed (not blocking - assumption checks inform interpretation)

**Step 2c: Model Selection**
- Analysis Tool: (determined by rq_tools - likely custom LRT comparison function)
- Validation Tool: (determined by rq_tools - likely tools.validation.validate_model_selection)
- What Validation Checks: All 3 models fit, LRT statistics computed, selected model converged, selected model refit with REML=False
- On Failure: Quit with error "Model selection failed: [specific failure]", log to logs/step02c_model_selection.log, g_debug invoked

**Step 3: Extract 3-Way Interactions**
- Analysis Tool: (determined by rq_tools - likely custom coefficient extraction)
- Validation Tool: (determined by rq_tools - likely tools.validation.validate_hypothesis_tests)
- What Validation Checks: 4 interaction terms present, p-values in [0,1], Bonferroni correction applied, Decision D068 compliance (dual p-values)
- On Failure: Quit with error "Hypothesis test failed: [specific check]", log to logs/step03_extract_interactions.log, g_debug invoked

**Step 4: Compute Post-Hoc Contrasts**
- Analysis Tool: (determined by rq_tools - likely tools.analysis_lmm.compute_contrasts_pairwise)
- Validation Tool: (determined by rq_tools - likely tools.validation.validate_contrasts)
- What Validation Checks: 3 age effects computed, 3 contrasts computed, Tukey correction applied, Decision D068 compliance (dual p-values)
- On Failure: Quit with error "Post-hoc contrasts failed: [specific check]", log to logs/step04_compute_contrasts.log, g_debug invoked

**Step 5: Prepare Plot Data**
- Analysis Tool: (determined by rq_tools - likely custom plot data aggregation)
- Validation Tool: (determined by rq_tools - likely tools.validation.validate_plot_data)
- What Validation Checks: ~600 rows created, all domains/tertiles present, value ranges valid, CI ordering correct, no critical NaN values
- On Failure: Quit with error "Plot data preparation failed: [specific check]", log to logs/step05_prepare_plot_data.log, g_debug invoked

---

## Summary

**Total Steps:** 6 (Step 0: data extraction + Steps 1-5: analysis)

**Estimated Runtime:** Medium (5-15 minutes total)
- Step 0: Low (<1 min) - DERIVED data extraction
- Step 1: Low (1-2 min) - Data preparation
- Step 2: Medium (2-5 min) - LMM fitting
- Step 2b: Low (1-2 min) - Assumption validation
- Step 2c: Low (1-2 min) - Model selection
- Step 3: Low (<1 min) - Extract interactions
- Step 4: Low (1-2 min) - Post-hoc contrasts
- Step 5: Low (1-2 min) - Plot data preparation

**Cross-RQ Dependencies:** RQ 5.1 (theta scores, TSVR mapping)

**Primary Outputs:**
- results/step02_lmm_model.pkl (fitted LMM with selected random structure)
- data/step02_fixed_effects.csv (all fixed effects coefficients)
- data/step03_interaction_terms.csv (3-way Age x Domain x Time interactions)
- results/step03_hypothesis_test.txt (hypothesis decision: age effects differ by domain?)
- data/step04_age_effects_by_domain.csv (domain-specific age effects on forgetting)
- data/step04_post_hoc_contrasts.csv (pairwise domain comparisons with Tukey HSD)
- plots/step05_age_effects_plot_data.csv (plot source CSV for age effects visualization)

**Validation Coverage:** 100% (all 6 steps have validation requirements)

**Decisions Applied:**
- Decision D070: TSVR as time variable (actual hours, not nominal days)
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni/Tukey for all hypothesis tests)
- Decision D069: NOT applicable (no trajectory plotting - age effects visualization uses tertiles, not dual-scale)

**Hypothesis:**
Age effects on forgetting rate will be strongest for spatial (Where) and temporal (When) domains, which rely on hippocampal binding, compared to object identity (What), which relies on perirhinal cortex. This predicts a significant 3-way Age x Domain x Time interaction.

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-11-26): Initial plan created by rq_planner agent for RQ 5.2.3
