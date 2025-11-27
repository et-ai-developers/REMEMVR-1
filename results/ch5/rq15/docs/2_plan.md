# Analysis Plan for RQ 5.15: Item Difficulty x Time Interaction

**Created by:** rq_planner agent
**Date:** 2025-11-27
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This RQ examines the cross-level interaction between item-level difficulty (from IRT calibration) and person-level forgetting trajectories (time). The research question asks whether easier items show faster or slower forgetting than harder items, testing competing theoretical predictions from strength theory (easier = faster forgetting) versus ceiling effects (easier = slower forgetting).

The analysis uses a **cross-classified Linear Mixed Model (LMM)** with crossed random effects for participants (UID) and items. This design differs from standard trajectory RQs by including item-level predictors (difficulty) that interact with person-level trajectories (time). The cross-classified structure accounts for both participant heterogeneity (some participants forget faster overall) and item heterogeneity (some items are easier/harder overall) while testing whether difficulty moderates forgetting rate.

**Pipeline:** DERIVED data (RQ 5.1 difficulty estimates) + RAW data (response data from dfData.csv) -> LMM with cross-level interaction

**Total Steps:** 6 analysis steps (Step 0: data loading and merging, Step 1: predictor centering, Step 2: LMM fitting with model selection, Step 3: extract interaction term, Step 4: comprehensive LMM validation, Step 5: plot interaction)

**Estimated Runtime:** Medium-High (60-90 minutes total)
- Step 0: Low (5 min - data loading/merging)
- Step 1: Low (2 min - centering)
- Step 2: High (30-60 min - cross-classified LMM with convergence testing)
- Step 3: Low (2 min - extract interaction)
- Step 4: Medium (10-15 min - comprehensive validation with 7 diagnostics)
- Step 5: Low (5 min - plot preparation)

**Key Decisions Applied:**
- Decision D070: TSVR (actual hours since encoding) as time variable (not nominal days)
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni alpha = 0.0033 for 15 RQs)

**Critical Dependencies:**
This RQ requires outputs from **RQ 5.1** (IRT calibration):
- `results/ch5/rq1/data/step03_difficulty.csv` (purified item difficulty estimates)
- `results/ch5/rq1/data/step00_tsvr_mapping.csv` (TSVR time variable)

RQ 5.1 must complete Steps 0-3 before this RQ can execute.

---

## Analysis Plan

### Step 0: Load and Merge Data

**Dependencies:** None (first step, but requires RQ 5.1 completion)
**Complexity:** Low (5 minutes - data loading and merging operations)

**Purpose:** Load item-level response data, merge with item difficulty estimates from RQ 5.1, merge with TSVR time variable, create analysis-ready dataset.

**Input:**

**File 1:** data/cache/dfData.csv (project-level cached data)
**Source:** Created by RQ 5.1 Step 0 (extraction from master.xlsx)
**Format:** Long format with columns:
  - `UID` (string, participant identifier, format: P### with leading zeros)
  - `test` (string, test session: T1, T2, T3, T4)
  - Item response columns: `TQ_RVR-X-N-{IFR|ICR|IRE}-*`, `TQ_RVR-X-{L|U|D}-{IFR|ICR|IRE}-*`, `TQ_RVR-X-O-{IFR|ICR|IRE}-*`
  - Response values: {1.0, 0.0} (1 = correct, 0 = incorrect, NaN = missing)
**Expected Rows:** ~400 (100 participants x 4 tests)
**Expected Columns:** ~200+ (UID, test, plus ~150-200 item response columns matching What/Where/When domains)

**File 2:** results/ch5/rq1/data/step03_difficulty.csv (DERIVED from RQ 5.1)
**Source:** RQ 5.1 Step 3 (Pass 2 IRT calibration, purified items)
**Format:** CSV with columns:
  - `item_name` (string, item tag from master.xlsx, e.g., "RVR-X-N-IFR-MC")
  - `dimension` (string, memory domain: "What", "Where", "When")
  - `b` (float, IRT difficulty parameter, range typically -3 to +3 but temporal items can exceed)
**Expected Rows:** Number of purified items from RQ 5.1 (typically 40-50% retention after purification per Decision D039)
**Expected Columns:** 3 (item_name, dimension, b)

**File 3:** results/ch5/rq1/data/step00_tsvr_mapping.csv (DERIVED from RQ 5.1)
**Source:** RQ 5.1 Step 0 (TSVR extraction from master.xlsx)
**Format:** CSV with columns:
  - `UID` (string, participant identifier)
  - `test` (string, test session: T1, T2, T3, T4)
  - `TSVR_hours` (float, actual hours since encoding per Decision D070)
**Expected Rows:** ~400 (100 participants x 4 tests)
**Expected Columns:** 3 (UID, test, TSVR_hours)

**Processing:**

1. **Load response data:** Read data/cache/dfData.csv
2. **Reshape to long format:** Melt item response columns (TQ_*) to create one row per UID x test x item
   - ID columns: UID, test
   - Value columns: All TQ_* columns matching What/Where/When domains (per 1_concept.md domain specification)
   - Result: Long DataFrame with columns [UID, test, item_name, response]
3. **Filter items:** Keep only items present in step03_difficulty.csv (purified set from RQ 5.1)
4. **Merge difficulty:** Left join on item_name to add difficulty (b) and dimension columns
5. **Merge TSVR:** Left join on UID + test to add TSVR_hours
6. **Verify merge completeness:**
   - Check for NaN in difficulty column (indicates item not in RQ 5.1 purified set - should be 0 after filtering)
   - Check for NaN in TSVR_hours (indicates missing TSVR data - should be 0)
7. **Create nominal time variables:**
   - `Days` (int): Map T1->0, T2->1, T3->3, T4->6 (nominal days for plotting)
   - `log_Days` (float): log(Days + 1) for alternative time scaling

**Output:**

**File:** data/step00_lmm_input_cross_classified.csv
**Format:** Long format (one row per observation: UID x test x item response)
**Columns:**
  - `UID` (string, participant identifier)
  - `test` (string, test session: T1, T2, T3, T4)
  - `item_name` (string, item tag)
  - `dimension` (string, memory domain: What, Where, When)
  - `response` (float, {0.0, 1.0}, item response)
  - `Difficulty` (float, IRT item difficulty parameter b)
  - `TSVR_hours` (float, actual hours since encoding per D070)
  - `Days` (int, nominal days {0, 1, 3, 6})
  - `log_Days` (float, log(Days + 1))
**Expected Rows:** ~40,000-60,000 (100 participants x 4 tests x ~100-150 purified items, varies by RQ 5.1 purification results)
**Expected Columns:** 9

**Validation Requirement:**
Validation tools MUST be used after data loading and merging tool execution. Specific validation tools will be determined by rq_tools based on data format requirements (validate_data_format, validate_data_columns, check_missing_data).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_lmm_input_cross_classified.csv exists (exact path)
- Expected rows: 40,000-60,000 (exact count depends on RQ 5.1 purification, validate in range)
- Expected columns: 9 (UID, test, item_name, dimension, response, Difficulty, TSVR_hours, Days, log_Days)
- Data types: UID (object), test (object), item_name (object), dimension (object), response (float64), Difficulty (float64), TSVR_hours (float64), Days (int64), log_Days (float64)

*Value Ranges:*
- response in {0.0, 1.0} (binary responses only, no intermediate values)
- Difficulty in [-6, 6] (typical IRT range, temporal items can exceed -3 to 3)
- TSVR_hours in [0, 200] hours (0 = encoding, ~168 = 1 week, some participants tested late)
- Days in {0, 1, 3, 6} (nominal test days, categorical)
- log_Days in [0, 2.0] (log(0+1)=0, log(6+1)=1.95)
- dimension in {What, Where, When} (categorical)

*Data Quality:*
- No NaN values in Difficulty column (all items matched to RQ 5.1 output after filtering)
- No NaN values in TSVR_hours column (all UID-test combinations matched)
- NaN allowed in response column (participants may not have answered all items)
- Expected N participants: 100 unique UIDs (validate: df['UID'].nunique() == 100)
- Expected N items: 40-150 unique item_names (validate: 40 <= df['item_name'].nunique() <= 150, depends on RQ 5.1 purification)
- No duplicate rows (UID x test x item_name combinations unique)

*Log Validation:*
- Required pattern: "Data merge complete: {N} observations created"
- Required pattern: "Unique participants: 100"
- Required pattern: "Unique items: {M}" where M in [40, 150]
- Required pattern: "All items matched to difficulty estimates (0 NaN)"
- Required pattern: "All UID-test combinations matched to TSVR (0 NaN)"
- Forbidden patterns: "ERROR", "NaN values in Difficulty", "NaN values in TSVR_hours", "Merge failed"
- Acceptable warnings: "NaN values in response column: {K}%" (expected - not all participants answered all items)

**Expected Behavior on Validation Failure:**
- If Difficulty has NaN: Raise error "Items not found in RQ 5.1 difficulty estimates - check purified item set"
- If TSVR_hours has NaN: Raise error "TSVR data missing for some UID-test combinations - check step00_tsvr_mapping.csv"
- If UID count != 100: Raise error "Expected 100 participants, found {N}"
- If item count outside [40, 150]: Warn "Item count {M} outside expected range - verify RQ 5.1 purification results"
- Log failure to logs/step00_load_and_merge_data.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause

---

### Step 1: Center Predictors

**Dependencies:** Step 0 (requires merged data with Difficulty column)
**Complexity:** Low (2 minutes - grand-mean centering operation)

**Purpose:** Grand-mean center item difficulty to improve LMM interpretability (intercept represents average item at average difficulty).

**Input:**

**File:** data/step00_lmm_input_cross_classified.csv
**Source:** Generated by Step 0
**Format:** Long format (UID x test x item responses)
**Required Columns:** Difficulty (float, IRT item difficulty parameter)

**Processing:**

1. **Compute grand mean:** mean_Difficulty = mean(Difficulty) across all observations
2. **Center difficulty:** Difficulty_c = Difficulty - mean_Difficulty
3. **Add centered column:** Append Difficulty_c to DataFrame
4. **Verify centering:** Check mean(Difficulty_c) approximately 0 (tolerance ±0.01 for numerical precision)

**Centering Rationale:**
Grand-mean centering is appropriate for item-level predictor because items are crossed with participants (not nested within). Cluster-mean centering (within-participant) not applicable since each item has single difficulty value across all participants (Enders & Tofighi, 2007). Grand-mean centering allows LMM intercept to represent average response probability for average-difficulty item at Time=0.

**Output:**

**File:** data/step01_lmm_input_centered.csv
**Format:** Long format (same structure as input)
**Columns:**
  - All columns from Step 0 input PLUS
  - `Difficulty_c` (float, grand-mean centered difficulty)
**Expected Rows:** Same as Step 0 (~40,000-60,000)
**Expected Columns:** 10 (9 from Step 0 + 1 new)

**Validation Requirement:**
Validation tools MUST be used after predictor centering tool execution. Specific validation tools will be determined by rq_tools (validate_standardization with mean tolerance ±0.01).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_lmm_input_centered.csv exists (exact path)
- Expected rows: Same as Step 0 (40,000-60,000)
- Expected columns: 10 (original 9 + Difficulty_c)
- Data types: Difficulty_c (float64)

*Value Ranges:*
- Difficulty_c in [-9, 9] (original Difficulty range [-6, 6] shifted by mean, conservative upper bound)
- mean(Difficulty_c) in [-0.01, 0.01] (grand-mean centering verification, tolerance for numerical precision)
- SD(Difficulty_c) == SD(Difficulty) (centering preserves variance, check within 0.001 tolerance)

*Data Quality:*
- No NaN values in Difficulty_c (centering operation preserves non-missing structure)
- Row count unchanged from Step 0 (centering adds column, doesn't filter rows)

*Log Validation:*
- Required pattern: "Grand-mean centering complete"
- Required pattern: "Mean Difficulty_c = {value}" where abs(value) < 0.01
- Required pattern: "SD Difficulty_c = {value}"
- Forbidden patterns: "ERROR", "NaN values in Difficulty_c", "Centering failed"

**Expected Behavior on Validation Failure:**
- If mean(Difficulty_c) outside [-0.01, 0.01]: Raise error "Centering failed - mean not approximately zero"
- If NaN in Difficulty_c: Raise error "Centering introduced NaN values"
- Log failure to logs/step01_center_predictors.log
- Quit script immediately
- g_debug invoked

---

### Step 2: Fit Cross-Classified LMM with Model Selection

**Dependencies:** Step 1 (requires centered predictors)
**Complexity:** High (30-60 minutes - cross-classified LMM with convergence testing and model selection)

**Purpose:** Fit cross-classified Linear Mixed Model testing Time x Difficulty_c interaction with crossed random effects for participants (UID) and items. Use model selection strategy to handle convergence issues common with N=100 and complex random structures.

**Input:**

**File:** data/step01_lmm_input_centered.csv
**Source:** Generated by Step 1
**Required Columns:** UID, item_name, TSVR_hours, Difficulty_c, response

**Processing:**

**Model Selection Strategy (per 1_concept.md):**

Given N=100 participants and complex crossed random effects, convergence failures are likely (Bates et al., 2015 recommend N>=200 for random slopes). Use progressive fallback strategy:

1. **Attempt maximal random structure first:**
   - Formula: `response ~ TSVR_hours * Difficulty_c + (TSVR_hours | UID) + (1 | item_name)`
   - Random effects: Random intercepts + random slopes for Time within UID, random intercepts for items
   - Software: pymer4 (Python wrapper for R lme4, required for crossed random effects)
   - Check convergence via validate_lmm_convergence tool (optimizer messages, singular fit warnings, correlation near ±1)

2. **If maximal model fails convergence, simplify to uncorrelated random slopes:**
   - Formula: `response ~ TSVR_hours * Difficulty_c + (TSVR_hours || UID) + (1 | item_name)`
   - Notation: `||` removes intercept-slope correlation (reduces parameters)
   - Check convergence again

3. **If uncorrelated slopes fail, simplify to random intercepts only:**
   - Formula: `response ~ TSVR_hours * Difficulty_c + (1 | UID) + (1 | item_name)`
   - Random effects: Random intercepts only (most parsimonious)
   - Check convergence

4. **If all pymer4 models fail or pymer4 unavailable, fallback to fixed effects for items:**
   - Formula: `response ~ TSVR_hours * Difficulty_c + item_name + (TSVR_hours | UID)`
   - Trade-off: Treats items as fixed (loses generalizability to new items) but allows convergence
   - Note: This is least preferred option, document as limitation

**Model Fitting Procedure:**

1. Attempt Model 1 (maximal random structure)
2. Run validate_lmm_convergence:
   - Check optimizer convergence message (no warnings/errors)
   - Check singular fit warnings (variance estimates near zero = overparameterization)
   - Check random effects correlation near ±1 (indicates instability)
3. If convergence: STOP, use this model
4. If no convergence: Try Model 2 (uncorrelated slopes)
5. Repeat convergence check
6. If still no convergence: Try Model 3 (intercepts only)
7. If still no convergence: Try Model 4 (fixed items)
8. Document which model converged in model summary and logs

**Convergence Remedies (if needed):**
- Rescale predictors: Center and standardize TSVR_hours (z-score) if convergence issues persist
- Increase optimizer iterations: Set maxfun=100000 (default may be too low)
- Check data issues: Verify sufficient variance in predictors, no perfect collinearity

**Cross-Level Interaction:**
The fixed effect `TSVR_hours * Difficulty_c` tests whether item difficulty (item-level predictor) moderates forgetting rate (person-level trajectory). This is the key research question.

**Output:**

**File 1:** results/step02_lmm_model_summary.txt
**Format:** Plain text model summary from pymer4
**Content:**
  - Fixed effects table (coefficients, SE, z-values, p-values)
  - Random effects variance components
  - Model fit indices (AIC, BIC, log-likelihood)
  - Convergence status
  - Which model formula used (document fallback if needed)

**File 2:** data/step02_lmm_fixed_effects.csv
**Format:** CSV with fixed effects estimates
**Columns:**
  - `term` (string, predictor name: Intercept, TSVR_hours, Difficulty_c, TSVR_hours:Difficulty_c)
  - `estimate` (float, coefficient)
  - `se` (float, standard error)
  - `z_value` (float, z-statistic)
  - `p_value` (float, uncorrected p-value)
  - `p_value_bonferroni` (float, Bonferroni-corrected p-value for alpha=0.0033 per D068)
**Expected Rows:** 4 (Intercept, TSVR_hours, Difficulty_c, interaction)

**File 3:** data/step02_lmm_random_effects.csv
**Format:** CSV with random effects variance components
**Columns:**
  - `grouping_factor` (string, UID or item_name)
  - `effect` (string, Intercept or TSVR_hours)
  - `variance` (float, variance component)
  - `sd` (float, standard deviation)
**Expected Rows:** Depends on final model (2-4 rows)

**Validation Requirement:**
Validation tools MUST be used after LMM fitting tool execution. Specific validation tools will be determined by rq_tools (validate_lmm_convergence, validate_model_convergence, validate_variance_positivity).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step02_lmm_model_summary.txt exists
- data/step02_lmm_fixed_effects.csv: 4 rows x 6 columns
- data/step02_lmm_random_effects.csv: 2-4 rows x 4 columns (depends on random structure)

*Value Ranges:*
- estimate (coefficients): unrestricted (can be positive or negative)
- se (standard errors): > 0 (must be positive)
- p_value in [0, 1] (probability)
- p_value_bonferroni in [0, 1] (corrected probability)
- variance components: > 0 (must be positive, negative indicates convergence failure)
- sd (standard deviations): > 0 (sqrt of variance)

*Data Quality:*
- All 4 fixed effects present (Intercept, TSVR_hours, Difficulty_c, TSVR_hours:Difficulty_c)
- No NaN values in estimate, se, p_value columns
- Bonferroni correction: p_value_bonferroni = min(p_value * 15, 1.0) where 15 = number of RQs in Chapter 5
- Random effects variance > 0 for all components (check variance column > 0)

*Log Validation:*
- Required pattern: "Model converged: True" OR "Model {N} converged" where N in {1, 2, 3, 4}
- Required pattern: "Fixed effects extracted: 4 terms"
- Required pattern: "Random effects extracted: {M} variance components"
- Required pattern: "VALIDATION - PASS: Convergence"
- Required pattern: "VALIDATION - PASS: Variance components positive"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "Singular fit", "All models failed to converge"
- Acceptable warnings: "Model 1 failed, trying Model 2" (documents fallback strategy), "Correlation between random effects near ±1" (if Model 2+ used)

**Expected Behavior on Validation Failure:**
- If all models fail to converge: Raise error "All 4 model variants failed convergence - check data structure and predictor scaling"
- If variance components negative or zero: Raise error "Negative/zero variance estimate - model overparameterized or data insufficient"
- If fixed effects missing: Raise error "Expected 4 fixed effects (Intercept, TSVR_hours, Difficulty_c, interaction), found {N}"
- Log failure to logs/step02_fit_cross_classified_lmm.log
- Quit script immediately
- g_debug invoked to diagnose (common causes: insufficient data, extreme collinearity, overparameterization)

---

### Step 3: Extract and Interpret Cross-Level Interaction

**Dependencies:** Step 2 (requires fitted LMM with interaction term)
**Complexity:** Low (2 minutes - extract interaction coefficient and interpret sign)

**Purpose:** Extract Time x Difficulty_c interaction term, test significance using Bonferroni-corrected alpha = 0.0033, interpret coefficient sign to determine which theoretical account is supported.

**Input:**

**File:** data/step02_lmm_fixed_effects.csv
**Source:** Generated by Step 2
**Required Row:** term == "TSVR_hours:Difficulty_c" (interaction term)
**Required Columns:** estimate, se, p_value, p_value_bonferroni

**Processing:**

1. **Extract interaction row:** Filter fixed effects table to interaction term
2. **Test significance:**
   - Compare p_value_bonferroni to alpha = 0.0033 (Bonferroni for 15 RQs: 0.05/15)
   - Significant if p_value_bonferroni < 0.0033
3. **Interpret coefficient sign:**
   - **Positive estimate (>0):** Easier items (lower difficulty) forget SLOWER -> Supports ceiling effects hypothesis
   - **Negative estimate (<0):** Easier items forget FASTER -> Supports strength theory hypothesis
   - **Non-significant:** Difficulty affects intercept only (baseline performance) but not forgetting rate -> Supports orthogonality hypothesis
4. **Document interpretation:** Write results to summary file

**Theoretical Interpretations:**

- **Significant Positive Interaction (estimate > 0, p_bonferroni < 0.0033):**
  - As time increases, higher difficulty items show GREATER decline in response probability
  - Equivalently: Lower difficulty (easier) items show SLOWER decline
  - Theoretical support: Ceiling effects dominate (high T1 performance constrains apparent forgetting)
  - Implication: Apparent forgetting rate reflects measurement artifact, not memory process

- **Significant Negative Interaction (estimate < 0, p_bonferroni < 0.0033):**
  - As time increases, higher difficulty items show LESSER decline in response probability
  - Equivalently: Lower difficulty (easier) items show FASTER decline
  - Theoretical support: Strength theory (weaker initial encoding -> faster decay)
  - Implication: Item difficulty indexes encoding strength, which predicts forgetting rate

- **Non-Significant Interaction (p_bonferroni >= 0.0033):**
  - Item difficulty does NOT moderate forgetting rate
  - Difficulty affects baseline performance (intercept) but decay rate is uniform across difficulty levels
  - Theoretical support: Orthogonality hypothesis (difficulty and decay are independent)
  - Implication: Forgetting rate driven by retrieval processes independent of encoding strength

**Output:**

**File:** results/step03_interaction_interpretation.txt
**Format:** Plain text summary
**Content:**
  - Interaction coefficient estimate ± SE
  - Uncorrected p-value
  - Bonferroni-corrected p-value (alpha = 0.0033)
  - Significance decision (significant/non-significant)
  - Coefficient sign interpretation (positive/negative/zero)
  - Theoretical account supported (ceiling effects/strength theory/orthogonality)
  - Effect size interpretation (how much does difficulty moderate forgetting rate?)

**Validation Requirement:**
Validation tools MUST be used after interaction extraction tool execution. Specific validation tools will be determined by rq_tools (validate_hypothesis_test_dual_pvalues per D068, validate_numeric_range for coefficient bounds).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step03_interaction_interpretation.txt exists
- File contains all required content sections (estimate, p-values, interpretation)

*Value Ranges:*
- estimate (interaction coefficient): unrestricted (positive, negative, or near-zero all theoretically plausible)
- se > 0 (standard error must be positive)
- p_value in [0, 1]
- p_value_bonferroni in [0, 1]
- Bonferroni check: p_value_bonferroni == min(p_value * 15, 1.0)

*Data Quality:*
- Both p_value and p_value_bonferroni present (dual p-value reporting per D068)
- Interpretation section matches coefficient sign (positive estimate -> "ceiling effects", negative -> "strength theory", ns -> "orthogonality")

*Log Validation:*
- Required pattern: "Interaction term extracted: TSVR_hours:Difficulty_c"
- Required pattern: "Bonferroni-corrected p-value: {value}" where value in [0, 1]
- Required pattern: "Theoretical account supported: {theory}" where theory in {ceiling effects, strength theory, orthogonality}
- Forbidden patterns: "ERROR", "Interaction term not found", "Missing p-value"

**Expected Behavior on Validation Failure:**
- If interaction term missing: Raise error "TSVR_hours:Difficulty_c not found in fixed effects - check model formula"
- If p_value_bonferroni missing: Raise error "Bonferroni correction not applied - dual p-value reporting required (D068)"
- Log failure to logs/step03_extract_interaction.log
- Quit script immediately
- g_debug invoked

---

### Step 4: Validate LMM Assumptions (Comprehensive)

**Dependencies:** Step 2 (requires fitted LMM model object and residuals)
**Complexity:** Medium (10-15 minutes - 7 comprehensive diagnostics with plots)

**Purpose:** Perform comprehensive LMM assumption validation using validate_lmm_assumptions_comprehensive tool. Critical with N=100 and complex random structures where violations can substantially affect Type I error rates (Schielzeth et al., 2020).

**Input:**

**File 1:** Fitted LMM model object from Step 2 (in-memory object or serialized)
**File 2:** data/step01_lmm_input_centered.csv (for residual computations)

**Processing:**

Use validate_lmm_assumptions_comprehensive tool to perform 7 assumption checks:

1. **Residual Normality:**
   - Method: Q-Q plot + Shapiro-Wilk test (if N < 5000) or Kolmogorov-Smirnov test (if N >= 5000)
   - Threshold: p > 0.05 (null hypothesis: residuals are normal)
   - Violation remedy: Use robust standard errors if p < 0.05

2. **Homoscedasticity (Constant Variance):**
   - Method: Residual vs Fitted plot (visual inspection for funnel patterns)
   - Threshold: Visual - no systematic increase/decrease in spread across fitted values
   - Violation remedy: Model variance structure (add weights parameter to LMM)

3. **Random Effects Normality:**
   - Method: Q-Q plots of random intercepts and slopes
   - Threshold: Visual - points follow diagonal line
   - Violation remedy: Usually robust to moderate violations, log-transform response if severe

4. **Independence (No Autocorrelation):**
   - Method: ACF plot of residuals (autocorrelation function)
   - Threshold: Lag-1 ACF < 0.1 (minimal autocorrelation)
   - Violation remedy: Add AR(1) correlation structure to model

5. **Linearity:**
   - Method: Partial residual plots for TSVR_hours and Difficulty_c
   - Threshold: Visual - no systematic curvature in partial residuals
   - Violation remedy: Add polynomial terms (TSVR_hours^2) or use splines

6. **Outliers:**
   - Method: Cook's distance computation
   - Threshold: D > 4/n (where n = number of observations)
   - Violation remedy: Investigate influential observations, consider robust regression

7. **Convergence:**
   - Method: Check optimizer messages, singular fit warnings, random effects correlations near ±1
   - Threshold: No warnings, correlations in [-0.95, 0.95]
   - Already checked in Step 2, but re-verify after full model fitting

**Output:**

**File 1:** results/step04_assumption_validation_report.txt
**Format:** Plain text comprehensive report
**Content:**
  - All 7 assumption checks with PASS/FAIL status
  - Test statistics (Shapiro-Wilk W, KS D, Cook's D max, ACF lag-1)
  - Diagnostic plots saved to plots/ folder
  - Remedial recommendations if violations detected

**File 2:** plots/step04_diagnostic_qq_residuals.png
**File 3:** plots/step04_diagnostic_residuals_vs_fitted.png
**File 4:** plots/step04_diagnostic_qq_random_effects.png
**File 5:** plots/step04_diagnostic_acf.png
**File 6:** plots/step04_diagnostic_partial_residuals.png
**Format:** PNG images (800 x 600 @ 300 DPI)

**Validation Requirement:**
Validation tools MUST be used after comprehensive assumption validation tool execution. Specific validation tools will be determined by rq_tools (validate_plot_data_completeness for diagnostic plots, check_file_exists for report).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step04_assumption_validation_report.txt exists
- 5 diagnostic plot PNG files exist (plots/step04_diagnostic_*.png)
- Report contains all 7 assumption sections (normality, homoscedasticity, random effects, independence, linearity, outliers, convergence)

*Value Ranges:*
- Shapiro-Wilk W in [0, 1] (test statistic)
- p-values in [0, 1]
- ACF lag-1 in [-1, 1] (correlation coefficient)
- Cook's D in [0, Inf) (distance measure, non-negative)

*Data Quality:*
- Each assumption section has PASS or FAIL verdict
- If FAIL: Remedial recommendation present
- Diagnostic plots created (5 PNG files)

*Log Validation:*
- Required pattern: "VALIDATION - PASS: {assumption}" OR "VALIDATION - FAIL: {assumption}" for all 7 assumptions
- Required pattern: "Comprehensive validation complete: {N}/7 assumptions passed"
- Required pattern: "Diagnostic plots saved: 5 files"
- Forbidden patterns: "ERROR", "Validation crashed", "Missing diagnostic"
- Acceptable warnings: "VALIDATION - FAIL: Residual normality (p=0.03) - consider robust SE" (documents violation with remedy)

**Expected Behavior on Validation Failure:**
- If critical assumptions violated (e.g., severe heteroscedasticity, autocorrelation): Log warning with remedial recommendation
- Do NOT halt execution (assumption violations are common, remedies available)
- Document violations in results/step04_assumption_validation_report.txt
- If convergence re-check fails: Raise error "Model convergence unstable after full fitting"
- Continue to Step 5 (plotting) even if assumptions violated (document violations for user interpretation)

---

### Step 5: Visualize Interaction (Plot Data Preparation)

**Dependencies:** Steps 1, 2 (requires centered predictors and fitted LMM model)
**Complexity:** Low (5 minutes - compute predicted trajectories for easy vs hard items)

**Purpose:** Generate predicted trajectories for easy items (-1 SD difficulty) vs hard items (+1 SD difficulty) to visualize Time x Difficulty_c interaction. Create plot source CSV for rq_plots agent.

**Input:**

**File 1:** data/step01_lmm_input_centered.csv
**Source:** Generated by Step 1
**Required Columns:** Difficulty_c (for computing ±1 SD)

**File 2:** Fitted LMM model object from Step 2

**Processing:**

1. **Compute difficulty reference values:**
   - SD_Difficulty_c = standard deviation of Difficulty_c
   - Easy items: Difficulty_c = -1 * SD_Difficulty_c
   - Hard items: Difficulty_c = +1 * SD_Difficulty_c

2. **Generate prediction grid:**
   - Time points: Days = {0, 1, 3, 6} (nominal days for interpretability)
   - Difficulty levels: {Easy, Hard}
   - Total: 4 time points x 2 difficulty levels = 8 prediction points

3. **Compute predicted response probabilities:**
   - Use fitted LMM to predict response probability at each grid point
   - Extract population-level predictions (fixed effects only, marginalize over random effects)
   - Compute 95% confidence intervals via delta method or parametric bootstrap

4. **Format for plotting:**
   - Create long-format DataFrame with columns: Days, Difficulty_level, predicted_response, CI_lower, CI_upper
   - Difficulty_level: categorical {Easy, Hard}

**Output:**

**File:** plots/step05_interaction_plot_data.csv
**Format:** CSV for rq_plots agent
**Columns:**
  - `Days` (int, nominal days {0, 1, 3, 6})
  - `Difficulty_level` (string, {"Easy", "Hard"})
  - `predicted_response` (float, predicted response probability [0, 1])
  - `CI_lower` (float, lower 95% CI bound [0, 1])
  - `CI_upper` (float, upper 95% CI bound [0, 1])
**Expected Rows:** 8 (4 time points x 2 difficulty levels)
**Expected Columns:** 5

**Plot Description (for rq_plots agent):**
Generate trajectory plot with Days (0, 1, 3, 6) on x-axis, predicted response probability on y-axis. Two lines: one for Easy items (Difficulty = -1 SD, typically shown in blue), one for Hard items (Difficulty = +1 SD, typically shown in red). Include 95% confidence bands (shaded regions) around each trajectory. If interaction significant: trajectories diverge (non-parallel lines). If non-significant: trajectories parallel.

**Plotting Function (rq_plots will call):** Trajectory plot with confidence bands (similar to plot_trajectory function but with two groups instead of three domains)

**Validation Requirement:**
Validation tools MUST be used after plot data preparation tool execution. Specific validation tools will be determined by rq_tools (validate_probability_range for predicted_response/CI bounds, validate_plot_data_completeness for factorial design).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- plots/step05_interaction_plot_data.csv exists (exact path)
- Expected rows: 8 (4 time points x 2 difficulty levels)
- Expected columns: 5 (Days, Difficulty_level, predicted_response, CI_lower, CI_upper)
- Data types: Days (int64), Difficulty_level (object), predicted_response (float64), CI_lower (float64), CI_upper (float64)

*Value Ranges:*
- Days in {0, 1, 3, 6} (categorical, 4 unique values)
- Difficulty_level in {"Easy", "Hard"} (categorical, 2 unique values)
- predicted_response in [0, 1] (probability scale)
- CI_lower in [0, 1] (probability scale)
- CI_upper in [0, 1] (probability scale)
- CI_upper > CI_lower for all rows (confidence intervals valid)

*Data Quality:*
- No NaN values tolerated (all cells must have valid values)
- Expected N: Exactly 8 rows (4 Days x 2 Difficulty_level = complete factorial design)
- No duplicate rows (Days x Difficulty_level combinations unique)
- Both difficulty levels present at each time point (complete factorial: 4 rows Easy, 4 rows Hard)

*Log Validation:*
- Required pattern: "Plot data preparation complete: 8 rows created"
- Required pattern: "Difficulty levels represented: Easy, Hard"
- Required pattern: "Time points: 0, 1, 3, 6"
- Required pattern: "All predictions in [0, 1]"
- Forbidden patterns: "ERROR", "NaN values detected", "Missing difficulty level", "Missing time point"
- Acceptable warnings: None expected for plot data preparation

**Expected Behavior on Validation Failure:**
- If rows != 8: Raise error "Expected 8 rows (4 Days x 2 Difficulty), found {N}"
- If predicted_response outside [0, 1]: Raise error "Predicted probabilities outside valid range [0, 1]"
- If CI_upper <= CI_lower: Raise error "Invalid confidence intervals (upper <= lower)"
- If incomplete factorial design: Raise error "Missing Days x Difficulty combinations - expected complete factorial"
- Log failure to logs/step05_prepare_interaction_plot_data.log
- Quit script immediately
- g_debug invoked to diagnose root cause

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 -> Step 1:**
- **Input:** Wide format (UID x test with item response columns) PLUS separate difficulty/TSVR files
- **Transformation:** Melt to long (UID x test x item), merge difficulty and TSVR
- **Output:** Long format (UID x test x item) with difficulty and TSVR columns
- **Key Change:** Reshape from wide to long, merge external data sources

**Step 1 -> Step 2:**
- **Input:** Long format with raw difficulty
- **Transformation:** Grand-mean center difficulty
- **Output:** Long format with Difficulty_c column added
- **Key Change:** Add centered predictor column, preserve all rows

**Step 2 -> Step 3:**
- **Input:** Fitted LMM model + fixed effects table
- **Transformation:** Extract interaction row
- **Output:** Single row (interaction term) + interpretation text
- **Key Change:** Filter to interaction, interpret sign

**Step 2 -> Step 4:**
- **Input:** Fitted LMM model object
- **Transformation:** Compute diagnostics (residuals, Q-Q, ACF, Cook's D)
- **Output:** Diagnostic report + 5 plots
- **Key Change:** Model diagnostics, no data transformation

**Step 1, 2 -> Step 5:**
- **Input:** Centered predictors + fitted model
- **Transformation:** Generate prediction grid (±1 SD difficulty x 4 time points), compute predicted probabilities
- **Output:** 8-row plot source CSV
- **Key Change:** Aggregate to prediction grid, marginalize over random effects

### Column Naming Conventions

**Core Identifiers:**
- `UID` - Participant identifier (string, format: P### with leading zeros)
- `test` - Test session (string, T1/T2/T3/T4)
- `item_name` - Item tag (string, RVR-X-{domain}-{paradigm}-{variant})

**Time Variables (Decision D070):**
- `TSVR_hours` - Actual hours since encoding (float, continuous)
- `Days` - Nominal days (int, {0, 1, 3, 6}, categorical for plotting)
- `log_Days` - Log-transformed nominal days (float, log(Days+1))

**IRT Variables:**
- `Difficulty` - Raw IRT item difficulty parameter (float, typically -3 to 3 but can exceed)
- `Difficulty_c` - Grand-mean centered difficulty (float, mean approximately 0)
- `a` - Item discrimination (not used in this RQ but present in RQ 5.1 output)

**LMM Variables:**
- `response` - Item response (float, {0.0, 1.0})
- `dimension` - Memory domain (string, {What, Where, When})
- `predicted_response` - Model-predicted response probability (float, [0, 1])
- `CI_lower` / `CI_upper` - 95% confidence interval bounds (float, [0, 1])

**Plotting Variables:**
- `Difficulty_level` - Categorical difficulty for plotting (string, {Easy, Hard})

### Data Type Constraints

**Identifiers:** object (string)
**Numeric Continuous:** float64
**Numeric Discrete:** int64
**Categorical:** object (string) - use for `test`, `dimension`, `Difficulty_level`

**Nullable Columns:**
- `response` - NaN allowed (participants may not answer all items)
- All other columns: No NaN allowed after merging complete

---

## Cross-RQ Dependencies

**Dependency Type:** DERIVED Data from RQ 5.1 (IRT calibration baseline)

**This RQ requires outputs from:**

**RQ 5.1** (Domain-Specific Forgetting Trajectories - IRT Calibration)
- **File 1:** results/ch5/rq1/data/step03_difficulty.csv
  - Used in: Step 0 (merge item difficulty into response data)
  - Content: Purified item difficulty estimates (b parameter) from Pass 2 IRT calibration
  - Columns: item_name, dimension, b
  - Rationale: RQ 5.1 establishes item difficulty parameters using 2-pass purification (Decision D039). This RQ uses those difficulty estimates as predictor to test whether difficulty moderates forgetting rate.

- **File 2:** results/ch5/rq1/data/step00_tsvr_mapping.csv
  - Used in: Step 0 (merge TSVR time variable)
  - Content: Time Since VR mapping (actual hours per Decision D070)
  - Columns: UID, test, TSVR_hours
  - Rationale: Decision D070 requires TSVR (actual hours) as time variable instead of nominal days. RQ 5.1 creates this mapping during initial data extraction.

**Execution Order Constraint:**
1. RQ 5.1 must complete Steps 0-3 first (extraction, Pass 1 IRT, purification, Pass 2 IRT)
2. This RQ (5.15) executes after RQ 5.1 (uses difficulty estimates as predictor)

**Data Source Boundaries (Per Specification 5.1.6):**
- **RAW data:** Response data from data/cache/dfData.csv (extracted by RQ 5.1 but not analysis output)
- **DERIVED data:** Item difficulty parameters from results/ch5/rq1/data/step03_difficulty.csv (analysis output)
- **Scope:** This RQ does NOT re-calibrate IRT models (uses RQ 5.1 parameters as fixed predictors in LMM)

**Validation:**
- Step 0: Check results/ch5/rq1/data/step03_difficulty.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch5/rq1/data/step00_tsvr_mapping.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- If either file missing -> quit with error -> user must execute RQ 5.1 first

**Reference:** Specification section 5.1.6 (Data Source Boundaries), Decision D070 (TSVR as time variable)

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

**Step 0: Load and Merge Data**
- Validation tools: validate_data_format, validate_data_columns, check_missing_data
- Checks: All required columns present, no NaN in Difficulty/TSVR after merge, UID count = 100, item count in [40, 150]
- On failure: Quit with error specifying missing data source

**Step 1: Center Predictors**
- Validation tools: validate_standardization (mean tolerance ±0.01)
- Checks: mean(Difficulty_c) approximately 0, SD preserved from raw Difficulty
- On failure: Quit with error "Centering failed"

**Step 2: Fit Cross-Classified LMM**
- Validation tools: validate_lmm_convergence, validate_model_convergence, validate_variance_positivity
- Checks: Model converged, no singular fit warnings, variance components > 0
- On failure: Try fallback models, document which model converged

**Step 3: Extract Interaction**
- Validation tools: validate_hypothesis_test_dual_pvalues (Decision D068), validate_numeric_range
- Checks: Interaction term present, dual p-values (uncorrected + Bonferroni), coefficient in reasonable range
- On failure: Quit with error "Interaction term missing or invalid"

**Step 4: Validate LMM Assumptions**
- Validation tools: validate_lmm_assumptions_comprehensive (7 diagnostics)
- Checks: Normality, homoscedasticity, independence, linearity, outliers, random effects, convergence
- On failure: Log violations with remedial recommendations, continue to plotting

**Step 5: Visualize Interaction**
- Validation tools: validate_probability_range, validate_plot_data_completeness
- Checks: Predicted probabilities in [0, 1], complete factorial design (4 Days x 2 Difficulty), CI_upper > CI_lower
- On failure: Quit with error specifying invalid predictions

**NOTE:** Technical validation (files exist, formats correct, values in bounds) checked by rq_inspect DURING analysis. Scientific plausibility (interaction sign matches theory, effect size reasonable) checked by rq_results AFTER all analysis complete.

---

## Summary

**Total Steps:** 6 (Step 0: data loading/merging, Step 1: centering, Step 2: LMM fitting, Step 3: interaction extraction, Step 4: assumption validation, Step 5: plot preparation)

**Estimated Runtime:** 60-90 minutes total
- Data operations: ~7 min (Steps 0, 1, 3, 5)
- LMM fitting: 30-60 min (Step 2 - cross-classified with model selection)
- Validation: 10-15 min (Step 4 - comprehensive diagnostics)

**Cross-RQ Dependencies:** RQ 5.1 (requires step03_difficulty.csv and step00_tsvr_mapping.csv)

**Primary Outputs:**
- results/step02_lmm_model_summary.txt (full LMM results)
- data/step02_lmm_fixed_effects.csv (fixed effects with dual p-values per D068)
- results/step03_interaction_interpretation.txt (interaction coefficient interpretation)
- results/step04_assumption_validation_report.txt (comprehensive assumption checks)
- plots/step05_interaction_plot_data.csv (plot source CSV for rq_plots)

**Validation Coverage:** 100% (all 6 steps have validation requirements embedded per v4.X architecture)

**Key Methodological Decisions:**
- Decision D070: TSVR (actual hours) as time variable (not nominal days)
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni alpha = 0.0033)
- Grand-mean centering for item-level predictor (items crossed with participants)
- Progressive model selection strategy (maximal random structure -> simpler if convergence fails)
- Comprehensive assumption validation (7 diagnostics via validate_lmm_assumptions_comprehensive)

**Unique Aspects of This RQ:**
- Cross-classified random effects (UID x Item) instead of nested
- Item-level predictor (difficulty) instead of person-level only
- Cross-level interaction (item property moderating person trajectory)
- No IRT calibration in this RQ (uses RQ 5.1 outputs as predictors)
- Model selection strategy due to convergence challenges with N=100

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_*.py scripts

---

**Version History:**
- v1.0 (2025-11-27): Initial plan created by rq_planner agent for RQ 5.15 (cross-classified LMM with Item Difficulty x Time interaction)
