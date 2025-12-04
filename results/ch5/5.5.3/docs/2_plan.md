# Analysis Plan: RQ 5.5.3 - Age Effects on Source-Destination Memory

**Research Question:** 5.5.3
**Created:** 2025-12-04
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ tests whether participant age (20-70 years) moderates the source-destination memory dissociation identified in RQ 5.5.1. The PRIMARY hypothesis is NULL: age will NOT significantly moderate the source (-U-) vs destination (-D-) memory difference or forgetting rates. This null prediction is theoretically motivated by the universal null pattern for age effects across Chapter 5 (RQs 5.1.3, 5.2.3, 5.3.4, 5.4.3), suggesting that ecological VR encoding creates age-resistant memory traces that buffer against hippocampal aging effects.

**Pipeline:** LMM only (no IRT calibration - uses DERIVED theta scores from RQ 5.5.1)

**Steps:** 6 total analysis steps (Step 0: dependency loading + Steps 1-5: analysis)

**Estimated Runtime:** Low-Medium (~20-30 minutes total)
- Step 0: Low (data loading)
- Step 1: Low (data preparation)
- Step 2: Medium (LMM fitting with 3-way interactions)
- Step 2.5: Low (assumption validation)
- Step 3: Low (interaction extraction)
- Step 3.5: Medium (power analysis via simulation - 1000 iterations)
- Step 4: Low (post-hoc contrasts)
- Step 5: Low (plot data aggregation)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni) for all hypothesis tests
- Decision D070: TSVR_hours as time variable (actual hours since encoding, not nominal days)

**Critical Feature - Type II Error Quantification:**
Since the primary hypothesis is NULL (age does NOT moderate source-destination forgetting), power analysis is MANDATORY to ensure the null finding is interpretable. Step 3.5 quantifies power to detect small effects (beta = 0.01 per Cohen, 1988), targeting power >= 0.80 to conclude study is adequately powered.

---

## Analysis Plan

### Step 0: Load Dependency Data from RQ 5.5.1

**Dependencies:** None (first step, but requires RQ 5.5.1 completion)

**Complexity:** Low (data loading and validation, <2 minutes)

**Purpose:** Load IRT theta scores by location type from RQ 5.5.1 and TSVR mapping. Load Age variable from raw data. Verify RQ 5.5.1 dependency is complete.

**Input:**

**File 1:** results/ch5/5.5.1/data/step03_theta_scores.csv
**Source:** RQ 5.5.1 Step 3 (IRT calibration Pass 2)
**Format:** CSV with columns:
  - composite_ID (string, format: UID_test, e.g., P001_T1)
  - theta_source (float, IRT ability estimate for pick-up locations)
  - se_source (float, standard error for source theta)
  - theta_destination (float, IRT ability estimate for put-down locations)
  - se_destination (float, standard error for destination theta)
**Expected Rows:** 400 (100 participants x 4 tests)

**File 2:** results/ch5/5.5.1/data/step00_tsvr_mapping.csv
**Source:** RQ 5.5.1 Step 0 (extraction)
**Format:** CSV with columns:
  - composite_ID (string, format: UID_test)
  - UID (string, format: P###, e.g., P001)
  - test (string, values: T1, T2, T3, T4)
  - TSVR_hours (float, actual hours since VR encoding)
**Expected Rows:** 400 (100 participants x 4 tests)

**File 3:** data/cache/dfData.csv
**Source:** Project-level raw data cache
**Format:** CSV with columns (relevant subset):
  - UID (string, participant identifier)
  - Age (int, range 20-70 years)
**Expected Rows:** 100 participants

**Processing:**

1. Check RQ 5.5.1 completion: verify results/ch5/5.5.1/status.yaml shows rq_results: success
2. Load theta scores from RQ 5.5.1
3. Load TSVR mapping from RQ 5.5.1
4. Load Age variable from dfData.csv
5. Validate row counts (400 for theta/TSVR, 100 for Age)
6. Validate column presence and data types
7. Check for missing values (no NaN allowed in theta, TSVR_hours, Age)

**Output:**

**File 1:** data/step00_theta_from_rq551.csv
**Format:** CSV, copy of RQ 5.5.1 theta scores for lineage tracking
**Columns:** composite_ID, theta_source, se_source, theta_destination, se_destination
**Expected Rows:** 400

**File 2:** data/step00_tsvr_from_rq551.csv
**Format:** CSV, copy of TSVR mapping for lineage tracking
**Columns:** composite_ID, UID, test, TSVR_hours
**Expected Rows:** 400

**File 3:** data/step00_age_from_dfdata.csv
**Format:** CSV, extracted Age variable
**Columns:** UID, Age
**Expected Rows:** 100

**Validation Requirement:**

Validation tools MUST be used after data loading execution. Specific validation tools will be determined by rq_tools based on data loading and dependency checking requirements. The rq_analysis agent will embed validation tool calls after the data loading tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_theta_from_rq551.csv: 400 rows x 5 columns (composite_ID: object, theta_source: float64, se_source: float64, theta_destination: float64, se_destination: float64)
- data/step00_tsvr_from_rq551.csv: 400 rows x 4 columns (composite_ID: object, UID: object, test: object, TSVR_hours: float64)
- data/step00_age_from_dfdata.csv: 100 rows x 2 columns (UID: object, Age: int64)

*Value Ranges:*
- theta_source in [-4, 4] (typical IRT ability range, allowing extremes)
- theta_destination in [-4, 4]
- se_source in [0.1, 1.5] (below 0.1 = suspiciously precise, above 1.5 = unreliable)
- se_destination in [0.1, 1.5]
- TSVR_hours in [0, 168] (0 = encoding, 168 = 1 week maximum)
- Age in [20, 70] (per participant inclusion criteria)

*Data Quality:*
- No NaN values allowed in any column (complete data required)
- All 100 participants present in Age file (no missing UIDs)
- All 400 composite_IDs unique (no duplicates)
- composite_ID format validated (UID_test pattern, e.g., P001_T1)
- UID format validated (P### with leading zeros)
- test values in {T1, T2, T3, T4} (categorical)

*Log Validation:*
- Required: "RQ 5.5.1 dependency verified: status.yaml shows rq_results = success"
- Required: "Loaded 400 theta observations from RQ 5.5.1"
- Required: "Loaded 400 TSVR mappings from RQ 5.5.1"
- Required: "Loaded 100 Age values from dfData.csv"
- Required: "VALIDATION - PASS: All data quality checks passed"
- Forbidden: "ERROR", "MISSING FILE", "NaN detected", "RQ 5.5.1 incomplete"
- Acceptable warnings: None expected for data loading

**Expected Behavior on Validation Failure:**
- If RQ 5.5.1 incomplete -> Raise error "DEPENDENCY ERROR: RQ 5.5.1 must complete before RQ 5.5.3", quit immediately
- If file missing -> Raise error with specific path, quit immediately
- If row count mismatch -> Raise error "Expected 400 rows, found N", quit immediately
- If NaN detected -> Raise error "NaN values in column X", quit immediately
- Log failure to logs/step00_load_dependency_data.log
- g_debug invoked to diagnose root cause

---

### Step 1: Prepare LMM Input Data

**Dependencies:** Step 0 (requires theta, TSVR, Age loaded)

**Complexity:** Low (data merging and transformation, <2 minutes)

**Purpose:** Merge theta scores with TSVR and Age, grand-mean center Age variable, create log-transformed TSVR predictor, reshape to long format with LocationType factor.

**Input:**

**From Step 0:**
- data/step00_theta_from_rq551.csv (400 rows, 5 cols)
- data/step00_tsvr_from_rq551.csv (400 rows, 4 cols)
- data/step00_age_from_dfdata.csv (100 rows, 2 cols)

**Processing:**

1. Parse composite_ID to extract UID (split on underscore, take first part)
2. Merge theta with TSVR on composite_ID (left join, all theta rows retained)
3. Merge with Age on UID (left join, all theta-TSVR rows retained)
4. Verify 400 observations after merge (no data loss)
5. Grand-mean center Age: Age_c = Age - mean(Age)
6. Verify Age_c mean approximately 0 (within +/- 0.01)
7. Create log-transformed TSVR: log_TSVR = log(TSVR_hours + 1)
8. Reshape wide to long: 400 rows x 2 location types = 800 rows
   - Create LocationType column: {Source, Destination}
   - Create theta column: theta_source or theta_destination depending on location type
   - Create se column: se_source or se_destination
9. Treatment code LocationType: Source = reference category (0), Destination = 1

**Output:**

**File:** data/step01_lmm_input.csv
**Format:** CSV, long format (one row per observation)
**Columns:**
  - composite_ID (string, format: UID_test_location, e.g., P001_T1_Source)
  - UID (string, participant identifier, e.g., P001)
  - test (string, T1/T2/T3/T4)
  - TSVR_hours (float, actual time since encoding)
  - log_TSVR (float, log(TSVR_hours + 1))
  - Age (int, raw age in years)
  - Age_c (float, grand-mean centered age)
  - LocationType (string, Source or Destination, Treatment-coded)
  - theta (float, IRT ability estimate for this location type)
  - se (float, standard error for theta)
**Expected Rows:** 800 (100 participants x 4 tests x 2 location types)
**Expected Columns:** 10

**Validation Requirement:**

Validation tools MUST be used after data preparation execution. Specific validation tools will be determined by rq_tools based on data transformation and validation requirements. The rq_analysis agent will embed validation tool calls after the data preparation tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_lmm_input.csv: 800 rows x 10 columns (all columns with correct data types)

*Value Ranges:*
- theta in [-4, 4] (IRT ability range)
- se in [0.1, 1.5] (standard error range)
- TSVR_hours in [0, 168] (time range)
- log_TSVR in [0, 5.13] (log(168+1) = 5.13 maximum)
- Age in [20, 70] (raw age)
- Age_c in [-30, 30] (centered age, typically [-20, +20] but allow extremes)

*Data Quality:*
- Exactly 800 rows (400 composite_IDs x 2 location types)
- No NaN values in any column
- All 100 participants present (no data loss during merge)
- Age_c mean approximately 0 (|mean(Age_c)| <= 0.01)
- Age_c standard deviation > 0 (variability exists)
- LocationType balanced: 400 Source, 400 Destination
- composite_ID format: UID_test_location (e.g., P001_T1_Source)

*Log Validation:*
- Required: "Merged theta with TSVR: 400 observations"
- Required: "Merged with Age: 400 observations (no data loss)"
- Required: "Age_c grand-mean centered: mean = X (|X| <= 0.01)"
- Required: "Created log_TSVR: range [0, 5.13]"
- Required: "Reshaped to long format: 800 observations (400 x 2 locations)"
- Required: "VALIDATION - PASS: All transformations successful"
- Forbidden: "ERROR", "NaN detected", "Data loss", "Age_c mean > 0.01"
- Acceptable warnings: None expected for data preparation

**Expected Behavior on Validation Failure:**
- If merge fails (row count != 400) -> Raise error "Merge failed: expected 400, found N", quit
- If Age_c mean > 0.01 -> Raise error "Age_c not centered: mean = X", quit
- If reshape fails (row count != 800) -> Raise error "Reshape failed: expected 800, found N", quit
- If NaN detected -> Raise error "NaN values in column X", quit
- Log failure to logs/step01_prepare_lmm_input.log
- g_debug invoked to diagnose root cause

---

### Step 2: Fit LMM with 3-Way Age x LocationType x Time Interactions

**Dependencies:** Step 1 (requires prepared LMM input)

**Complexity:** Medium (LMM fitting with complex interaction structure, 5-10 minutes)

**Purpose:** Fit Linear Mixed Model with full 3-way Age_c x LocationType x Time interaction to test whether age moderates source-destination forgetting trajectories. Primary test: 3-way interaction terms (null hypothesis).

**Input:**

**From Step 1:**
- data/step01_lmm_input.csv (800 rows, 10 cols)

**Processing:**

1. Load LMM input data
2. Specify model formula:
   theta ~ TSVR_hours + log_TSVR + Age_c + LocationType +
           TSVR_hours:Age_c + log_TSVR:Age_c +
           TSVR_hours:LocationType + log_TSVR:LocationType +
           Age_c:LocationType +
           TSVR_hours:Age_c:LocationType + log_TSVR:Age_c:LocationType +
           (TSVR_hours | UID)
3. Fit using statsmodels MixedLM with REML=False (ML estimation for model comparison)
4. Extract convergence status (model.converged = True expected)
5. Extract fixed effects table (coefficients, SE, z-values, p-values)
6. Extract random effects variance components
7. Compute AIC, BIC fit indices
8. Save fitted model object for downstream steps

**Model Structure Details:**
- **Fixed Effects:** 12 terms total
  - Main effects: TSVR_hours, log_TSVR, Age_c, LocationType (4)
  - 2-way interactions: TSVR_hours:Age_c, log_TSVR:Age_c, TSVR_hours:LocationType, log_TSVR:LocationType, Age_c:LocationType (5)
  - 3-way interactions: TSVR_hours:Age_c:LocationType, log_TSVR:Age_c:LocationType (2)
  - Intercept (1)
- **Random Effects:** Random intercept and TSVR_hours slope per participant (UID)
- **Estimation:** Maximum Likelihood (REML=False)

**Output:**

**File 1:** data/step02_lmm_model.pkl
**Format:** Pickle file, saved statsmodels MixedLMResults object
**Purpose:** Model object for downstream extraction and power analysis

**File 2:** data/step02_lmm_summary.txt
**Format:** Text file, model summary
**Content:** Convergence status, AIC/BIC, fixed effects table, random effects variance components, ICC estimates

**File 3:** data/step02_fixed_effects.csv
**Format:** CSV, fixed effects table
**Columns:** term (string), coef (float), se (float), z (float), p (float), ci_lower (float), ci_upper (float)
**Expected Rows:** 12 (all fixed effects terms)

**Validation Requirement:**

Validation tools MUST be used after LMM fitting execution. Specific validation tools will be determined by rq_tools based on LMM convergence and fit validation requirements. The rq_analysis agent will embed validation tool calls after the LMM fitting tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_lmm_model.pkl: exists, file size > 1KB (model object saved)
- data/step02_lmm_summary.txt: exists, file size > 500 bytes (summary text)
- data/step02_fixed_effects.csv: 12 rows x 7 columns (all fixed effects present)

*Value Ranges:*
- coef (coefficients): unrestricted (can be positive/negative)
- se (standard errors): all > 0 (must be positive)
- z (z-statistics): unrestricted
- p (p-values): all in [0, 1]
- ci_lower < ci_upper for all terms (confidence interval logic)

*Data Quality:*
- Model converged: model.converged = True (CRITICAL)
- All 12 fixed effects present (no missing terms)
- Random variances positive: var_intercept > 0, var_slope >= 0, var_residual > 0
- AIC and BIC finite (not NaN or inf)
- No singular fit warnings (variance components not at boundary)
- All 800 observations used (no data loss during fitting)

*Log Validation:*
- Required: "Model converged: True"
- Required: "Fixed effects estimated: 12 terms"
- Required: "Random effects: intercept and TSVR_hours slope per UID"
- Required: "AIC = X, BIC = Y (finite values)"
- Required: "All variance components positive"
- Required: "VALIDATION - PASS: Model fit successful"
- Forbidden: "ERROR", "Model failed to converge", "Singular fit", "NaN coefficients"
- Acceptable warnings: "Gradient norm may not be zero" (common, acceptable if converged = True)

**Expected Behavior on Validation Failure:**
- If model fails to converge -> Raise error "LMM failed to converge", log convergence diagnostics, quit
- If fixed effects != 12 -> Raise error "Expected 12 fixed effects, found N", quit
- If variance component <= 0 -> Raise error "Variance component not positive: var_X = Y", quit
- If singular fit -> Log warning "Singular fit detected", continue (not critical failure)
- Log failure to logs/step02_fit_lmm.log
- g_debug invoked to diagnose convergence issues

---

### Step 2.5: Validate LMM Assumptions

**Dependencies:** Step 2 (requires fitted LMM model)

**Complexity:** Low (assumption checking with diagnostic plots, 2-3 minutes)

**Purpose:** Comprehensive validation of LMM assumptions using 7 diagnostic checks. Documents violations and recommends remedial actions if needed.

**Input:**

**From Step 2:**
- data/step02_lmm_model.pkl (fitted model object)
- data/step01_lmm_input.csv (original data for residual extraction)

**Processing:**

1. Load fitted LMM model
2. Extract residuals (observed - fitted)
3. Extract fitted values (model predictions)
4. Extract random effects (BLUPs for intercepts and slopes)

**Run 7 Assumption Checks:**

**(1) Linearity:** Residuals vs fitted values plot
- Visual: Expect random scatter around y = 0 horizontal line
- Test: No U-shaped or systematic patterns
- Criterion: PASS if visual inspection shows no pattern

**(2) Homoscedasticity:** Scale-location plot + Breusch-Pagan test
- Visual: Expect horizontal trend in sqrt(|residuals|) vs fitted
- Test: Breusch-Pagan test for heteroscedasticity (p > 0.05 = homoscedastic)
- Criterion: PASS if BP test p > 0.05

**(3) Normality of Residuals:** Q-Q plot + Shapiro-Wilk test
- Visual: Q-Q plot, expect points along diagonal
- Test: Shapiro-Wilk test (p > 0.05 = normal), but lenient for large n
- Criterion: PASS if visual assessment acceptable (Q-Q mostly linear)

**(4) Normality of Random Effects:** Q-Q plot for BLUPs + Shapiro-Wilk
- Visual: Q-Q plot for random intercepts and slopes
- Test: Shapiro-Wilk test for BLUPs
- Criterion: PASS if visual assessment acceptable

**(5) Independence:** Residuals vs observation order + Durbin-Watson test
- Visual: Residuals vs row index, expect random scatter
- Test: Durbin-Watson statistic (1.5 to 2.5 acceptable, ~2.0 ideal)
- Criterion: PASS if DW in [1.5, 2.5]

**(6) No Multicollinearity:** Variance Inflation Factor (VIF)
- Compute VIF for all fixed effects predictors
- Criterion: PASS if all VIF < 10 (VIF > 10 = problematic multicollinearity)

**(7) No Influential Observations:** Cook's distance
- Compute Cook's D for all observations
- Criterion: PASS if all Cook's D < 1.0 (D > 1.0 = highly influential)

**Output:**

**File 1:** data/step02.5_assumption_validation.csv
**Format:** CSV, assumption test results
**Columns:** assumption (string), test (string), statistic (float), p_value (float), criterion (string), result (string: PASS/FAIL)
**Expected Rows:** 7 (one per assumption)

**File 2:** data/step02.5_assumption_diagnostics.txt
**Format:** Text report, detailed diagnostics
**Content:** Pass/fail summary, violation descriptions, remedial action recommendations

**Validation Requirement:**

Validation tools MUST be used after assumption validation execution. Specific validation tools will be determined by rq_tools based on assumption checking requirements. The rq_analysis agent will embed validation tool calls after the assumption validation tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02.5_assumption_validation.csv: 7 rows x 6 columns
- data/step02.5_assumption_diagnostics.txt: exists, file size > 200 bytes

*Value Ranges:*
- p_value in [0, 1] (for tests that have p-values)
- statistic: unrestricted (different scales for different tests)
- VIF: all >= 1.0 (VIF = 1 means no multicollinearity, VIF < 1 impossible)
- Cook's D: all >= 0 (cannot be negative)
- Durbin-Watson: typically in [0, 4] (2.0 = no autocorrelation)

*Data Quality:*
- All 7 assumptions tested (no missing rows)
- At least 5/7 assumptions pass (>= 71% pass rate acceptable)
- result column contains only {PASS, FAIL}
- All p-values valid (not NaN)
- Violations documented in diagnostics.txt

*Log Validation:*
- Required: "Assumption validation complete: 7 tests run"
- Required: "Passed: X/7 assumptions (X >= 5 acceptable)"
- Required: "VALIDATION - PASS: Assumption checking successful"
- Forbidden: "ERROR", "Unable to compute test X", "Assumption validation failed"
- Acceptable warnings: "Assumption X failed: [description]" (documented failure)

**Expected Behavior on Validation Failure:**
- If < 5 assumptions pass -> Log warning "Multiple assumption violations: see diagnostics.txt", continue (not critical failure)
- If assumption test raises exception -> Raise error "Assumption test X failed: [exception]", quit
- Log results to logs/step02.5_validate_assumptions.log
- Remedial actions documented in diagnostics.txt (e.g., "Consider robust standard errors for heteroscedasticity")

---

### Step 3: Extract 3-Way Interaction Terms

**Dependencies:** Step 2 (requires fitted LMM model)

**Complexity:** Low (fixed effects extraction, <1 minute)

**Purpose:** Extract 3-way Age_c x LocationType x Time interaction terms and test significance at Bonferroni-corrected alpha = 0.025 (correcting for 2 time predictors). Primary null hypothesis test.

**Input:**

**From Step 2:**
- data/step02_lmm_model.pkl (fitted model object)
- data/step02_fixed_effects.csv (all fixed effects)

**Processing:**

1. Load fitted LMM model
2. Extract 3-way interaction terms from fixed effects:
   - TSVR_hours:Age_c:LocationType
   - log_TSVR:Age_c:LocationType
3. Apply Bonferroni correction: alpha = 0.05 / 2 = 0.025
4. Report BOTH uncorrected and Bonferroni-corrected p-values (Decision D068)
5. Interpret significance at corrected alpha = 0.025
6. Compute 95% confidence intervals for interaction coefficients

**Output:**

**File:** data/step03_interaction_terms.csv
**Format:** CSV, 3-way interaction results
**Columns:** term (string), coef (float), se (float), z (float), p_uncorrected (float), p_bonferroni (float), ci_lower (float), ci_upper (float), significant_at_0025 (bool)
**Expected Rows:** 2 (two 3-way interaction terms)

**Validation Requirement:**

Validation tools MUST be used after interaction extraction execution. Specific validation tools will be determined by rq_tools based on hypothesis testing and dual p-value validation requirements (Decision D068). The rq_analysis agent will embed validation tool calls after the interaction extraction tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_interaction_terms.csv: 2 rows x 9 columns

*Value Ranges:*
- coef: unrestricted (interaction coefficients can be any value)
- se > 0 (standard errors must be positive)
- z: unrestricted
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1]
- p_bonferroni >= p_uncorrected (Bonferroni correction makes p-values larger/more conservative)
- ci_lower < ci_upper

*Data Quality:*
- Exactly 2 rows (two 3-way interactions)
- Both p-value columns present (Decision D068 compliance)
- All p-values valid (not NaN)
- significant_at_0025 column is boolean (True/False)
- Bonferroni correction applied correctly (p_bonferroni = min(1.0, p_uncorrected * 2))

*Log Validation:*
- Required: "Extracted 2 three-way interaction terms"
- Required: "Bonferroni correction applied: alpha = 0.025 (correcting for 2 tests)"
- Required: "Dual p-values reported per Decision D068"
- Required: "VALIDATION - PASS: Interaction extraction successful"
- Forbidden: "ERROR", "Missing interaction term", "p_bonferroni < p_uncorrected"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- If interaction terms != 2 -> Raise error "Expected 2 interaction terms, found N", quit
- If p_bonferroni < p_uncorrected -> Raise error "Bonferroni correction failed: p_bonf < p_uncorr", quit
- If NaN p-values -> Raise error "NaN p-values detected", quit
- Log failure to logs/step03_extract_interactions.log
- g_debug invoked to diagnose extraction issues

---

### Step 3.5: Power Analysis for Null Hypothesis Testing

**Dependencies:** Step 2 (requires fitted LMM model)

**Complexity:** Medium (simulation-based power analysis, 5-10 minutes for 1000 iterations)

**Purpose:** Quantify Type II error (power) to detect small Age x LocationType x Time interaction effects. Since the primary hypothesis is NULL, power analysis is MANDATORY to ensure null finding is interpretable (not due to insufficient power).

**Input:**

**From Step 2:**
- data/step02_lmm_model.pkl (fitted model object)
- data/step01_lmm_input.csv (data for simulation)

**Processing:**

**Simulation-Based Power Analysis:**

1. Load fitted LMM model (null model with Age_c x LocationType x Time interaction beta = observed)
2. Extract observed model parameters:
   - Fixed effects coefficients
   - Random effects variance components
   - Residual variance
3. Define alternative hypothesis effect size:
   - Age_c:LocationType:TSVR_hours interaction beta = 0.01 (small effect per Cohen, 1988)
   - Age_c:LocationType:log_TSVR interaction beta = 0.01
4. Simulate 1000 datasets under alternative hypothesis:
   - Use observed data structure (800 observations, 100 participants)
   - Add small interaction effect (beta = 0.01) to data-generating model
   - Add random noise based on observed variance components
5. For each simulated dataset:
   - Fit LMM with same formula as Step 2
   - Extract 3-way interaction p-values
   - Test significance at Bonferroni alpha = 0.025
   - Record: detected (p < 0.025) or not detected (p >= 0.025)
6. Compute power:
   - Power = proportion of simulations where interaction detected
   - 95% CI for power estimate (binomial confidence interval)
7. Target: Power >= 0.80 to detect small effects
8. If power < 0.80: Compute minimum detectable effect size at 80% power via binary search

**Output:**

**File:** data/step03.5_power_analysis.csv
**Format:** CSV, power analysis results
**Columns:** effect_size (float), n_simulations (int), n_detected (int), power (float), ci_lower (float), ci_upper (float), target_met (bool)
**Expected Rows:** 1 (effect_size = 0.01, n_simulations = 1000)

**Optional File (if power < 0.80):**
**File:** data/step03.5_minimum_detectable_effect.csv
**Format:** CSV, minimum effect size at 80% power
**Columns:** power_target (float = 0.80), mde (float), n_simulations (int)

**Validation Requirement:**

Validation tools MUST be used after power analysis execution. Specific validation tools will be determined by rq_tools based on simulation validation and power estimation requirements. The rq_analysis agent will embed validation tool calls after the power analysis tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03.5_power_analysis.csv: 1 row x 7 columns
- data/step03.5_minimum_detectable_effect.csv: 0 or 1 rows (present only if power < 0.80)

*Value Ranges:*
- effect_size = 0.01 (small effect per Cohen)
- n_simulations = 1000 (specified)
- n_detected in [0, 1000] (count of significant simulations)
- power in [0, 1] (proportion, power = n_detected / n_simulations)
- ci_lower in [0, 1], ci_upper in [0, 1], ci_lower <= power <= ci_upper
- target_met = (power >= 0.80)

*Data Quality:*
- power = n_detected / n_simulations (formula correct)
- Confidence interval computed correctly (binomial CI)
- All 1000 simulations completed (no early termination)
- If power < 0.80: MDE file exists with valid mde > 0.01

*Log Validation:*
- Required: "Power analysis initiated: 1000 simulations at effect_size = 0.01"
- Required: "Simulations complete: N detected / 1000 total"
- Required: "Power = X.XX (95% CI: [lower, upper])"
- Required: "Target power 0.80: [MET/NOT MET]"
- Required: "VALIDATION - PASS: Power analysis complete"
- Forbidden: "ERROR", "Simulation failed", "Power > 1.0", "Negative power"
- Acceptable warnings: "Power < 0.80: computing minimum detectable effect size" (if applicable)

**Expected Behavior on Validation Failure:**
- If simulations fail -> Raise error "Power simulation failed at iteration N", quit
- If power > 1.0 or power < 0 -> Raise error "Invalid power estimate: X", quit
- If n_detected > n_simulations -> Raise error "n_detected exceeds n_simulations", quit
- Log progress to logs/step03.5_power_analysis.log (simulation progress updates)
- g_debug invoked if simulation errors occur

---

### Step 4: Location-Specific Age Effects at Day 3

**Dependencies:** Step 2 (requires fitted LMM model)

**Complexity:** Low (post-hoc contrasts, 1-2 minutes)

**Purpose:** Compute location-specific marginal age effects at Day 3 (midpoint of retention interval) using Tukey HSD post-hoc contrasts. Compare age slope for Source vs Destination at this representative timepoint.

**Input:**

**From Step 2:**
- data/step02_lmm_model.pkl (fitted model object)
- data/step01_lmm_input.csv (data for marginal means)

**Processing:**

1. Load fitted LMM model
2. Define Day 3 timepoint:
   - TSVR_hours = 72 (nominal Day 3 = 72 hours after encoding)
   - log_TSVR = log(72 + 1) = 4.29
3. Compute marginal age effects for Source and Destination at Day 3:
   - Source age effect: partial derivative of theta with respect to Age_c at TSVR_hours = 72, LocationType = Source
   - Destination age effect: partial derivative with respect to Age_c at TSVR_hours = 72, LocationType = Destination
4. Compute contrast: Destination_age_effect - Source_age_effect
5. Use Tukey HSD adjustment for 2 comparisons
6. Report BOTH uncorrected and Tukey-adjusted p-values (Decision D068)
7. Compute Cohen's d effect size for contrast

**Output:**

**File 1:** data/step04_age_effects_by_location.csv
**Format:** CSV, location-specific age effects
**Columns:** location (string), age_slope (float), se (float), z (float), p_uncorrected (float), p_tukey (float), ci_lower (float), ci_upper (float)
**Expected Rows:** 2 (Source, Destination)

**File 2:** data/step04_post_hoc_contrasts.csv
**Format:** CSV, contrast between locations
**Columns:** contrast (string = "Destination - Source"), diff (float), se (float), z (float), p_uncorrected (float), p_tukey (float), cohens_d (float), ci_lower (float), ci_upper (float)
**Expected Rows:** 1 (one contrast)

**Validation Requirement:**

Validation tools MUST be used after post-hoc contrast execution. Specific validation tools will be determined by rq_tools based on contrast computation and dual p-value validation requirements (Decision D068). The rq_analysis agent will embed validation tool calls after the post-hoc contrast tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_age_effects_by_location.csv: 2 rows x 8 columns
- data/step04_post_hoc_contrasts.csv: 1 row x 9 columns

*Value Ranges:*
- age_slope: unrestricted (can be positive, negative, or near zero)
- se > 0 (standard errors positive)
- z: unrestricted
- p_uncorrected in [0, 1]
- p_tukey in [0, 1]
- p_tukey >= p_uncorrected (Tukey adjustment is conservative)
- cohens_d: typically in [-2, 2] (|d| > 2 suggests very large effect or error)
- ci_lower < ci_upper

*Data Quality:*
- Exactly 2 rows in age_effects (Source, Destination)
- Exactly 1 row in contrasts (Destination - Source)
- Both p-value columns present (Decision D068 compliance)
- All p-values valid (not NaN)
- Cohen's d computed correctly (standardized difference)

*Log Validation:*
- Required: "Marginal age effects computed at Day 3 (TSVR_hours = 72)"
- Required: "Source age slope: X (SE = Y)"
- Required: "Destination age slope: X (SE = Y)"
- Required: "Tukey HSD post-hoc contrast: Destination - Source"
- Required: "Dual p-values reported per Decision D068"
- Required: "VALIDATION - PASS: Post-hoc contrasts successful"
- Forbidden: "ERROR", "p_tukey < p_uncorrected", "NaN p-values"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- If location count != 2 -> Raise error "Expected 2 locations, found N", quit
- If p_tukey < p_uncorrected -> Raise error "Tukey adjustment failed", quit
- If NaN p-values -> Raise error "NaN p-values detected", quit
- Log failure to logs/step04_post_hoc_contrasts.log
- g_debug invoked to diagnose contrast issues

---

### Step 5: Prepare Age Tertile Plot Data

**Dependencies:** Step 1 (requires prepared LMM input)

**Complexity:** Low (data aggregation for plotting, 1-2 minutes)

**Purpose:** Create age tertiles (Young/Middle/Older based on 33rd and 67th percentiles) and aggregate observed theta means by age tertile x location type x test for plotting. Compute 95% confidence intervals per group.

**Input:**

**From Step 1:**
- data/step01_lmm_input.csv (800 rows with Age, LocationType, test, theta)

**Processing:**

1. Load LMM input data
2. Compute age tertile cutoffs:
   - Young: Age <= 33rd percentile
   - Middle: 33rd percentile < Age <= 67th percentile
   - Older: Age > 67th percentile
3. Assign each observation to age tertile
4. Group by age tertile x location type x test
5. Compute per group:
   - Mean theta
   - Standard error (SE = SD / sqrt(N))
   - 95% confidence interval (mean +/- 1.96 * SE)
   - Sample size (N observations per group)
6. Validate completeness: all 24 groups present (3 tertiles x 2 locations x 4 tests)

**Output:**

**File:** data/step05_age_tertile_plot_data.csv
**Format:** CSV, plot source data
**Columns:** age_tertile (string: Young/Middle/Older), location (string: Source/Destination), test (string: T1/T2/T3/T4), theta_mean (float), se (float), ci_lower (float), ci_upper (float), n (int)
**Expected Rows:** 24 (3 tertiles x 2 locations x 4 tests)
**Expected Columns:** 8

**Note:** This CSV is read by rq_plots later to generate age tertile trajectory plot. PNG output goes to plots/ folder when rq_plots runs.

**Validation Requirement:**

Validation tools MUST be used after plot data preparation execution. Specific validation tools will be determined by rq_tools based on plot data format and completeness requirements. The rq_analysis agent will embed validation tool calls after the plot data preparation tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_age_tertile_plot_data.csv: 24 rows x 8 columns

*Value Ranges:*
- theta_mean in [-4, 4] (typical IRT range)
- se in [0.05, 1.0] (standard errors reasonable for group means)
- ci_lower in [-4, 4], ci_upper in [-4, 4]
- ci_upper > ci_lower for all rows (confidence interval logic)
- n >= 5 per group (minimum group size for stable estimates)

*Data Quality:*
- Exactly 24 rows (complete factorial design: 3 x 2 x 4)
- All age tertiles present: Young, Middle, Older (3 unique values)
- All locations present: Source, Destination (2 unique values)
- All tests present: T1, T2, T3, T4 (4 unique values)
- No NaN values in any column
- Group sizes balanced (n should be approximately 100/3 = 33 per tertile, accounting for 2 locations x 4 tests)
- ci_lower = theta_mean - 1.96 * se (formula correct)
- ci_upper = theta_mean + 1.96 * se (formula correct)

*Log Validation:*
- Required: "Age tertile cutoffs computed: 33rd percentile = X, 67th percentile = Y"
- Required: "Age tertiles assigned: Young (n=A), Middle (n=B), Older (n=C)"
- Required: "Aggregated means: 24 groups (3 tertiles x 2 locations x 4 tests)"
- Required: "All groups present: complete factorial design"
- Required: "VALIDATION - PASS: Plot data preparation successful"
- Forbidden: "ERROR", "Missing group", "NaN detected", "CI_upper <= CI_lower"
- Acceptable warnings: "Unbalanced tertile sizes" (age distribution may not split evenly)

**Expected Behavior on Validation Failure:**
- If row count != 24 -> Raise error "Expected 24 groups, found N (missing groups detected)", quit
- If NaN detected -> Raise error "NaN values in column X", quit
- If ci_upper <= ci_lower -> Raise error "Invalid confidence interval for group X", quit
- If n < 5 for any group -> Log warning "Small group size (n < 5) for group X"
- Log failure to logs/step05_prepare_plot_data.log
- g_debug invoked to diagnose aggregation issues

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs - intermediate and final)

- data/step00_theta_from_rq551.csv (from Step 0: theta scores from RQ 5.5.1)
- data/step00_tsvr_from_rq551.csv (from Step 0: TSVR mapping from RQ 5.5.1)
- data/step00_age_from_dfdata.csv (from Step 0: Age variable from dfData.csv)
- data/step01_lmm_input.csv (from Step 1: merged and prepared LMM input, 800 rows)
- data/step02_lmm_model.pkl (from Step 2: saved LMM model object)
- data/step02_lmm_summary.txt (from Step 2: model summary text)
- data/step02_fixed_effects.csv (from Step 2: all fixed effects, 12 rows)
- data/step02.5_assumption_validation.csv (from Step 2.5: assumption test results, 7 rows)
- data/step02.5_assumption_diagnostics.txt (from Step 2.5: diagnostics report)
- data/step03_interaction_terms.csv (from Step 3: 3-way interactions, 2 rows)
- data/step03.5_power_analysis.csv (from Step 3.5: power results, 1 row)
- data/step03.5_minimum_detectable_effect.csv (from Step 3.5: MDE if power < 0.80, optional)
- data/step04_age_effects_by_location.csv (from Step 4: location-specific age effects, 2 rows)
- data/step04_post_hoc_contrasts.csv (from Step 4: Tukey HSD contrasts, 1 row)
- data/step05_age_tertile_plot_data.csv (from Step 5: plot source data, 24 rows)

### Logs (ONLY execution logs - .log files capturing stdout/stderr)

- logs/step00_load_dependency_data.log
- logs/step01_prepare_lmm_input.log
- logs/step02_fit_lmm.log
- logs/step02.5_validate_assumptions.log
- logs/step03_extract_interactions.log
- logs/step03.5_power_analysis.log
- logs/step04_post_hoc_contrasts.log
- logs/step05_prepare_plot_data.log

### Plots (EMPTY until rq_plots runs)

- plots/ (folder remains empty until rq_plots generates visualizations)

### Results (EMPTY until rq_results runs)

- results/ (folder remains empty until rq_results generates summary.md)

---

## Cross-RQ Dependencies

**This RQ depends on:** RQ 5.5.1 (Source-Destination Trajectories ROOT)

**Required Files from RQ 5.5.1:**
- results/ch5/5.5.1/data/step03_theta_scores.csv (IRT ability estimates by location type: 400 rows)
- results/ch5/5.5.1/data/step00_tsvr_mapping.csv (TSVR time mapping: 400 rows)

**Status Check:**
- Step 0 of this RQ verifies results/ch5/5.5.1/status.yaml shows rq_results: success
- If RQ 5.5.1 incomplete: QUIT with "DEPENDENCY ERROR: RQ 5.5.1 must complete before RQ 5.5.3 (requires theta scores)"

**Data Integration:**
- Step 0: Load theta and TSVR from RQ 5.5.1, merge with Age from dfData.csv
- Expected: 400 theta observations matched with 400 TSVR mappings matched with 100 Age values
- All merges on UID (participant identifier)
- No missing data allowed (all 100 participants must have Age values)

**Execution Order Constraint:**
1. RQ 5.5.1 must complete Steps 0-7 (full IRT -> LMM pipeline)
2. This RQ (5.5.3) executes using RQ 5.5.1 outputs (theta scores as dependent variable)

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

### Validation Requirements By Step

#### Step 0: Load Dependency Data from RQ 5.5.1

**Analysis Tool:** (determined by rq_tools - likely data loading and validation functions)
**Validation Tool:** (determined by rq_tools - likely validate_data_columns, check_file_exists, validate_numeric_range)

**What Validation Checks (for rq_inspect post-execution validation):**
- RQ 5.5.1 dependency complete (status.yaml check)
- All output files exist (3 CSV files)
- Expected row counts (400, 400, 100)
- Expected column counts (5, 4, 2)
- No NaN values in any column
- Value ranges scientifically reasonable (theta in [-4,4], Age in [20,70], TSVR in [0,168])
- composite_ID and UID format validation

**Expected Behavior on Validation Failure:**
- Dependency missing -> Raise error, quit immediately
- File missing -> Raise error with path, quit
- NaN detected -> Raise error, quit
- g_debug invoked to diagnose data loading issues

---

#### Step 1: Prepare LMM Input Data

**Analysis Tool:** (determined by rq_tools - likely data merging and transformation functions)
**Validation Tool:** (determined by rq_tools - likely validate_dataframe_structure, validate_standardization)

**What Validation Checks:**
- Output file exists (step01_lmm_input.csv)
- Expected row count (800)
- Expected column count (10)
- No NaN values
- Age_c grand-mean centered (|mean| <= 0.01)
- LocationType balanced (400 Source, 400 Destination)
- Value ranges valid
- Reshape successful (400 -> 800 rows)

**Expected Behavior on Validation Failure:**
- Merge failure -> Raise error, quit
- Age_c not centered -> Raise error, quit
- Reshape failure -> Raise error, quit
- g_debug invoked to diagnose transformation issues

---

#### Step 2: Fit LMM with 3-Way Interactions

**Analysis Tool:** (determined by rq_tools - likely fit_lmm_trajectory_tsvr or similar)
**Validation Tool:** (determined by rq_tools - likely validate_lmm_convergence, validate_variance_positivity)

**What Validation Checks:**
- Model converged (model.converged = True)
- All 12 fixed effects present
- Random variances positive
- AIC/BIC finite
- All 800 observations used
- No singular fit

**Expected Behavior on Validation Failure:**
- Convergence failure -> Raise error, log diagnostics, quit
- Missing fixed effects -> Raise error, quit
- Variance components <= 0 -> Raise error, quit
- g_debug invoked to diagnose convergence issues

---

#### Step 2.5: Validate LMM Assumptions

**Analysis Tool:** (determined by rq_tools - likely validate_lmm_assumptions_comprehensive)
**Validation Tool:** (determined by rq_tools - comprehensive assumption validation suite)

**What Validation Checks:**
- 7 assumption tests completed
- At least 5/7 assumptions pass
- Violations documented
- Remedial actions recommended

**Expected Behavior on Validation Failure:**
- < 5 assumptions pass -> Log warning, continue (not critical failure)
- Test exception -> Raise error, quit
- Remedial actions logged

---

#### Step 3: Extract 3-Way Interaction Terms

**Analysis Tool:** (determined by rq_tools - likely extract_fixed_effects_from_lmm)
**Validation Tool:** (determined by rq_tools - likely validate_hypothesis_test_dual_pvalues)

**What Validation Checks:**
- 2 interaction terms extracted
- Dual p-values present (Decision D068)
- p_bonferroni >= p_uncorrected
- All p-values in [0,1]
- Confidence intervals valid

**Expected Behavior on Validation Failure:**
- Term count != 2 -> Raise error, quit
- Bonferroni correction invalid -> Raise error, quit
- NaN p-values -> Raise error, quit
- g_debug invoked to diagnose extraction issues

---

#### Step 3.5: Power Analysis for Null Hypothesis

**Analysis Tool:** (determined by rq_tools - likely custom simulation function)
**Validation Tool:** (determined by rq_tools - simulation validation)

**What Validation Checks:**
- 1000 simulations completed
- Power in [0, 1]
- Power formula correct (n_detected / n_simulations)
- Confidence interval valid
- MDE computed if power < 0.80

**Expected Behavior on Validation Failure:**
- Simulation failure -> Raise error at iteration N, quit
- Invalid power -> Raise error, quit
- g_debug invoked to diagnose simulation issues

---

#### Step 4: Location-Specific Age Effects

**Analysis Tool:** (determined by rq_tools - likely compute_contrasts_pairwise with Tukey adjustment)
**Validation Tool:** (determined by rq_tools - likely validate_contrasts_dual_pvalues)

**What Validation Checks:**
- 2 location-specific effects
- 1 contrast (Destination - Source)
- Dual p-values present (Decision D068)
- p_tukey >= p_uncorrected
- Cohen's d computed

**Expected Behavior on Validation Failure:**
- Location count != 2 -> Raise error, quit
- Tukey adjustment invalid -> Raise error, quit
- NaN p-values -> Raise error, quit
- g_debug invoked to diagnose contrast issues

---

#### Step 5: Prepare Age Tertile Plot Data

**Analysis Tool:** (determined by rq_tools - likely prepare_age_effects_plot_data or custom aggregation)
**Validation Tool:** (determined by rq_tools - likely validate_plot_data_completeness, validate_dataframe_structure)

**What Validation Checks:**
- 24 rows (complete factorial design)
- All tertiles present (Young, Middle, Older)
- All locations present (Source, Destination)
- All tests present (T1, T2, T3, T4)
- No NaN values
- CI_upper > CI_lower for all rows
- Group sizes >= 5

**Expected Behavior on Validation Failure:**
- Row count != 24 -> Raise error (missing groups), quit
- NaN detected -> Raise error, quit
- Invalid CI -> Raise error, quit
- Small group size (n < 5) -> Log warning, continue
- g_debug invoked to diagnose aggregation issues

---

## Summary

**Total Steps:** 6 (Step 0: dependency loading + Steps 1-5: analysis)

**Estimated Runtime:** Low-Medium (20-30 minutes total)
- Step 0: <2 min
- Step 1: <2 min
- Step 2: 5-10 min
- Step 2.5: 2-3 min
- Step 3: <1 min
- Step 3.5: 5-10 min (simulation)
- Step 4: 1-2 min
- Step 5: 1-2 min

**Cross-RQ Dependencies:** RQ 5.5.1 (theta scores by location type)

**Primary Outputs:**
- LMM model object (data/step02_lmm_model.pkl)
- 3-way interaction terms with dual p-values (data/step03_interaction_terms.csv)
- Power analysis results (data/step03.5_power_analysis.csv)
- Age tertile plot data (data/step05_age_tertile_plot_data.csv)

**Validation Coverage:** 100% (all 6 steps have validation requirements)

**Primary Hypothesis (NULL):** Age will NOT moderate source-destination forgetting (3-way Age x LocationType x Time interaction p > 0.025 Bonferroni-corrected)

**Type II Error Quantification:** Power analysis (Step 3.5) ensures null finding is interpretable (target power >= 0.80 for small effects)

**Decision Compliance:**
- D068: Dual p-values (uncorrected + Bonferroni/Tukey) for all hypothesis tests
- D070: TSVR_hours as time variable (actual hours, not nominal days)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-04): Initial plan created by rq_planner agent for RQ 5.5.3 (Age Effects on Source-Destination Memory)
