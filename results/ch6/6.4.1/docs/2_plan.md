# Analysis Plan for RQ 6.4.1: Paradigm Confidence Trajectories

**Created by:** rq_planner agent
**Date:** 2025-12-06
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This RQ examines confidence decline patterns across three retrieval paradigms (Free Recall, Cued Recall, Recognition) using IRT-derived ability estimates from TC_* (confidence) items. The analysis tests whether retrieval support affects not only memory accuracy (Ch5 5.3.1-5.3.2 found NULL slope differences) but also subjective confidence in memory.

**Analysis Pipeline:** IRT (Graded Response Model for 5-category ordinal confidence data) -> LMM (Paradigm x Time interaction test)

**Total Steps:** 8 analysis steps (Step 0: extraction + Steps 1-7: analysis)

**Estimated Runtime:** High (90-120 minutes total - IRT calibration dominates)

**Key Decisions Applied:**
- Decision D039: 2-pass IRT purification (MANDATORY for all IRT)
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni for post-hoc contrasts)
- Decision D069: Dual-scale trajectory plots (theta + probability scales for interpretability)
- Decision D070: TSVR as time variable (actual hours, not nominal days)

**Critical Methodological Note:**
Confidence items (TC_*) are 5-category ordinal (0, 0.25, 0.5, 0.75, 1.0), NOT dichotomous like accuracy items (TQ_* are 0/1). Must use Graded Response Model (GRM) for IRT calibration. This is distinct from Ch5 accuracy analyses which used 2PL.

---

## Analysis Plan

### Step 0: Extract TC_* Confidence Items by Paradigm

**Dependencies:** None (first step)
**Complexity:** Low (5-10 minutes, data extraction only)

**Purpose:** Extract 5-category ordinal confidence items from dfData.csv, filter to interactive paradigms (IFR, ICR, IRE), create Q-matrix for 3-factor IRT structure.

**Input:**

**File:** data/cache/dfData.csv
**Required Columns:**
- `UID` (participant identifier, format: P### with leading zeros)
- `test` (test session: T1, T2, T3, T4 for Days 0, 1, 3, 6)
- TC_* confidence items with paradigm tags (IFR, ICR, IRE)
- TSVR_hours (actual time since encoding)

**Paradigm Tag Patterns:**
- IFR: Interactive Free Recall confidence items
- ICR: Interactive Cued Recall confidence items
- IRE: Interactive Recognition confidence items

**Exclusions:**
- Room-level paradigms: RFR, TCR, RRE (not object-level tasks)
- Accuracy items: TQ_* (analyzed in Ch5, not relevant for confidence)

**Processing:**

1. Filter dfData.csv to TC_* confidence items with IFR/ICR/IRE tags
2. Create composite_ID = UID_test (e.g., "P001_T1")
3. Reshape to wide format: rows = composite_ID, columns = TC_* items
4. Extract TSVR_hours mapping (composite_ID -> TSVR_hours)
5. Create Q-matrix: 3 factors (Factor1=IFR confidence, Factor2=ICR confidence, Factor3=IRE confidence)
6. Validate: All values in {0, 0.25, 0.5, 0.75, 1.0, NaN}

**Output:**

**File 1:** data/step00_irt_input.csv
**Format:** CSV, wide format (composite_ID x TC_* items)
**Columns:**
- `composite_ID` (string, format: UID_test, e.g., "P001_T1")
- One column per TC_* item (TC_IFR_item1, TC_ICR_item2, TC_IRE_item3, ...)
- Values: {0, 0.25, 0.5, 0.75, 1.0, NaN} (5-category ordinal)
**Expected Rows:** ~400 (100 participants x 4 tests)
**Expected Columns:** ~102 TC_* items + 1 composite_ID column = 103 total

**File 2:** data/step00_tsvr_mapping.csv
**Format:** CSV, time mapping
**Columns:**
- `composite_ID` (string)
- `UID` (string)
- `test` (string: T1, T2, T3, T4)
- `TSVR_hours` (float, actual time since encoding per Decision D070)
**Expected Rows:** ~400

**File 3:** data/step00_q_matrix.csv
**Format:** CSV, Q-matrix for 3-factor IRT structure
**Columns:**
- `item_name` (string, TC_* item identifier)
- `factor1_IFR` (int, 0/1: does item load on IFR factor?)
- `factor2_ICR` (int, 0/1: does item load on ICR factor?)
- `factor3_IRE` (int, 0/1: does item load on IRE factor?)
**Expected Rows:** ~102 items
**Notes:** Each item loads on exactly ONE factor (simple structure)

**Validation Requirement:**
Validation tools MUST be used after data extraction tool execution. Specific validation tools will be determined by rq_tools based on extraction requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_irt_input.csv exists, ~400 rows x ~103 columns
- data/step00_tsvr_mapping.csv exists, ~400 rows x 4 columns
- data/step00_q_matrix.csv exists, ~102 rows x 4 columns
- All files UTF-8 encoded, CSV format

*Value Ranges:*
- step00_irt_input.csv: Values in {0, 0.25, 0.5, 0.75, 1.0, NaN} only (5-category ordinal)
- step00_tsvr_mapping.csv: TSVR_hours in [0, 168] (0=encoding, 168=1 week)
- step00_q_matrix.csv: factor columns in {0, 1} only

*Data Quality:*
- composite_ID format correct: UID_test pattern (e.g., "P001_T1")
- No duplicate composite_IDs in any file
- TSVR_hours: No NaN values (all participants have timing data)
- Q-matrix: Each item loads on exactly 1 factor (sum of factor columns = 1 per row)
- Missing data: <50% NaN per TC_* item acceptable (>50% suggests extraction error)

*Log Validation:*
- Required pattern: "Extracted N TC_* items for N participants x 4 tests"
- Required pattern: "Q-matrix: 3 factors (IFR, ICR, IRE) with N items per factor"
- Forbidden patterns: "ERROR", "No TC_* items found", "TSVR_hours missing"
- Acceptable warnings: "Missing confidence ratings for participant P### in test T#"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step00_extract_confidence_data.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause

---

### Step 1: IRT Calibration Pass 1 (All Items)

**Dependencies:** Step 0 (requires extracted confidence items)
**Complexity:** High (60-90 minutes for full GRM calibration with 3 factors)

**Purpose:** Calibrate Graded Response Model (GRM) on all TC_* confidence items (3-factor structure: IFR/ICR/IRE) to obtain Pass 1 item parameters for purification (Decision D039).

**CRITICAL:** Use MINIMAL SETTINGS FIRST for pipeline validation (~10 minutes), then production settings after validation passes.

**Input:**

**File 1:** data/step00_irt_input.csv
**Source:** Generated by Step 0
**Format:** Wide format (composite_ID x TC_* items)
**Values:** {0, 0.25, 0.5, 0.75, 1.0, NaN} (5-category ordinal)

**File 2:** data/step00_q_matrix.csv
**Source:** Generated by Step 0
**Format:** Q-matrix (item x factor loadings)

**Processing:**

**IRT Model:** Graded Response Model (GRM) for 5-category ordinal data
**Dimensions:** 3 factors (IFR confidence, ICR confidence, IRE confidence)
**Prior:** p1_med (medium informativeness per IWAVE defaults)
**Algorithm:** IWAVE variational inference

**MINIMAL Settings (Pipeline Validation):**
- max_iter: 50 (vs 200 production)
- mc_samples: 10 (vs 100 production)
- iw_samples: 10 (vs 100 production)
- Runtime: ~10 minutes

**Production Settings (After Validation):**
- max_iter: 200
- mc_samples: 100
- iw_samples: 100
- Runtime: 60-90 minutes

**Workflow:**
1. Load step00_irt_input.csv + step00_q_matrix.csv
2. Configure GRM model (3 factors, 5-category ordinal)
3. Fit model using IWAVE (MINIMAL settings first)
4. Extract item parameters (discrimination a, difficulty b per threshold)
5. Extract theta estimates (diagnostic, not final)
6. Save Pass 1 outputs

**Output:**

**File 1:** data/step01_pass1_item_params.csv
**Format:** CSV, item parameters
**Columns:**
- `item_name` (string, TC_* identifier)
- `factor` (string: IFR, ICR, IRE)
- `a` (float, discrimination parameter, must be > 0)
- `b1`, `b2`, `b3`, `b4` (float, threshold parameters for 5-category GRM)
**Expected Rows:** ~102 items

**File 2:** data/step01_pass1_theta.csv
**Format:** CSV, theta estimates (diagnostic)
**Columns:**
- `composite_ID` (string)
- `theta_IFR` (float, IFR confidence ability)
- `theta_ICR` (float, ICR confidence ability)
- `theta_IRE` (float, IRE confidence ability)
- `se_IFR`, `se_ICR`, `se_IRE` (float, standard errors)
**Expected Rows:** ~400

**Validation Requirement:**
Validation tools MUST be used after IRT calibration tool execution. Specific validation tools determined by rq_tools (likely validate_irt_calibration, validate_irt_convergence).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_pass1_item_params.csv: ~102 rows x 6 columns (item_name, factor, a, b1-b4)
- data/step01_pass1_theta.csv: ~400 rows x 7 columns (composite_ID, theta_IFR/ICR/IRE, se_IFR/ICR/IRE)

*Value Ranges:*
- Discrimination (a): (0, 10] (values >10 suggest estimation error)
- Thresholds (b1-b4): [-6, 6] (extreme values suggest misfit but not necessarily error)
- Thresholds ordered: b1 < b2 < b3 < b4 (MANDATORY for GRM)
- Theta: [-4, 4] (outside suggests calibration problem)
- SE: [0.1, 1.5] (above 1.5 = unreliable)

*Data Quality:*
- No NaN in discrimination (a) - estimation failure if present
- Thresholds may have NaN for extreme categories (acceptable for some items)
- All ~400 composite_IDs present in theta file (no participant loss)
- Theta SE: mean SE < 0.8 indicates good precision

*Log Validation:*
- Required pattern: "Model converged: True"
- Required pattern: "VALIDATION - PASS: GRM threshold ordering"
- Required pattern: "VALIDATION - PASS: theta range [-4, 4]"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "NaN discrimination"
- Acceptable warnings: "Threshold b4 extreme for item TC_IFR_item#"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step01_irt_calibration_pass1.log
- Quit script immediately
- g_debug invoked to diagnose (common: insufficient data, model misspecification, need more iterations)

---

### Step 2: Purify Items (Decision D039)

**Dependencies:** Step 1 (requires Pass 1 item parameters)
**Complexity:** Low (<5 minutes, filtering only)

**Purpose:** Filter items by quality thresholds to identify well-performing items for Pass 2 calibration (Decision D039: 2-pass IRT purification).

**Input:**

**File:** data/step01_pass1_item_params.csv
**Source:** Generated by Step 1
**Columns:** item_name, factor, a, b1-b4

**Processing:**

**Purification Thresholds (Decision D039):**
- Discrimination: a >= 0.4 (items below have poor discriminatory power)
- Difficulty: |b_mean| <= 3.0 (where b_mean = mean of b1, b2, b3, b4)

**Workflow:**
1. Load Pass 1 item parameters
2. Compute b_mean = mean(b1, b2, b3, b4) per item
3. Apply filters: keep item if (a >= 0.4) AND (|b_mean| <= 3.0)
4. Expected retention: 40-50% per factor (GRM stricter than 2PL)
5. Ensure minimum 10 items per factor retained (else warn)
6. Save retained item list + purification report

**Output:**

**File 1:** data/step02_purified_items.csv
**Format:** CSV, retained items
**Columns:**
- `item_name` (string, TC_* identifier)
- `factor` (string: IFR, ICR, IRE)
- `a` (float, discrimination from Pass 1)
- `b_mean` (float, mean threshold from Pass 1)
**Expected Rows:** 40-60 items (40-50% retention from ~102 items)

**File 2:** data/step02_purification_report.txt
**Format:** Plain text report
**Contents:**
- Total items Pass 1: N
- Items retained: N (X%)
- Items excluded: N (Y%)
- Exclusion reasons breakdown:
  - Low discrimination (a < 0.4): N items
  - Extreme difficulty (|b_mean| > 3.0): N items
  - Both criteria failed: N items
- Retention by factor:
  - IFR: N/M items retained (X%)
  - ICR: N/M items retained (X%)
  - IRE: N/M items retained (X%)
- List of excluded items with reasons

**Validation Requirement:**
Validation tools MUST be used after purification tool execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_purified_items.csv: 40-60 rows x 4 columns
- data/step02_purification_report.txt exists, non-empty

*Value Ranges:*
- Retained items: a >= 0.4, |b_mean| <= 3.0 (thresholds enforced)
- Retention rate: 30-70% per factor (outside suggests data issue)

*Data Quality:*
- Minimum 10 items per factor retained (else insufficient for calibration)
- No duplicate item_names
- All retained items present in Pass 1 parameters

*Log Validation:*
- Required pattern: "Purification complete: N items retained from M"
- Required pattern: "All factors have >= 10 items"
- Forbidden patterns: "ERROR", "Factor IFR has <10 items"
- Acceptable warnings: "Retention rate 35% (below typical 40-50%)"

**Expected Behavior on Validation Failure:**
- If any factor <10 items: CRITICAL ERROR (insufficient data for Pass 2)
- Log failure to logs/step02_purify_items.log
- Quit script immediately
- g_debug invoked (may need to relax thresholds or exclude factor)

---

### Step 3: IRT Calibration Pass 2 (Purified Items)

**Dependencies:** Step 2 (requires purified item list)
**Complexity:** High (60-90 minutes for production GRM)

**Purpose:** Re-calibrate GRM on purified items only to obtain final theta_confidence estimates (Decision D039 Pass 2).

**Input:**

**File 1:** data/step00_irt_input.csv
**Source:** Generated by Step 0
**Usage:** Filter to purified items only

**File 2:** data/step02_purified_items.csv
**Source:** Generated by Step 2
**Usage:** List of items to include in Pass 2

**File 3:** data/step00_q_matrix.csv
**Source:** Generated by Step 0
**Usage:** Filter to purified items only

**Processing:**

**IRT Model:** Graded Response Model (GRM) for 5-category ordinal data
**Dimensions:** 3 factors (IFR/ICR/IRE) with purified items only
**Prior:** p1_med

**MINIMAL Settings (Pipeline Validation):**
- Same as Step 1 minimal (~10 minutes)

**Production Settings:**
- Same as Step 1 production (60-90 minutes)

**Workflow:**
1. Filter step00_irt_input.csv to purified items from step02_purified_items.csv
2. Filter step00_q_matrix.csv to purified items
3. Configure GRM model (3 factors, fewer items than Pass 1)
4. Fit model using IWAVE (expect better convergence than Pass 1)
5. Extract final theta_confidence estimates
6. Extract final item parameters (for documentation)
7. Save Pass 2 outputs

**Output:**

**File 1:** data/step03_item_parameters.csv
**Format:** CSV, final item parameters
**Columns:**
- `item_name` (string)
- `factor` (string: IFR, ICR, IRE)
- `a` (float, discrimination)
- `b1`, `b2`, `b3`, `b4` (float, thresholds)
**Expected Rows:** 40-60 items (purified set)

**File 2:** data/step03_theta_confidence_paradigm.csv
**Format:** CSV, final theta estimates
**Columns:**
- `composite_ID` (string)
- `theta_IFR` (float, IFR confidence ability)
- `theta_ICR` (float, ICR confidence ability)
- `theta_IRE` (float, IRE confidence ability)
- `se_IFR`, `se_ICR`, `se_IRE` (float, standard errors)
**Expected Rows:** ~400 (100 participants x 4 tests)

**Validation Requirement:**
Validation tools MUST be used after Pass 2 IRT calibration tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_item_parameters.csv: 40-60 rows x 6 columns
- data/step03_theta_confidence_paradigm.csv: ~400 rows x 7 columns

*Value Ranges:*
- Discrimination (a): [0.4, 10] (purification enforces a >= 0.4)
- Thresholds (b1-b4): [-6, 6], ordered b1 < b2 < b3 < b4
- Theta: [-4, 4] (confidence ability estimates)
- SE: [0.1, 1.5]

*Data Quality:*
- All ~400 composite_IDs present (no participant loss)
- Mean SE improved vs Pass 1 (purification should increase precision)
- No NaN in discrimination or theta

*Log Validation:*
- Required pattern: "Pass 2 converged: True"
- Required pattern: "Mean SE Pass 2 < Mean SE Pass 1" (precision improvement)
- Required pattern: "VALIDATION - PASS: All criteria"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED"

**Expected Behavior on Validation Failure:**
- Raise error
- Log failure to logs/step03_irt_calibration_pass2.log
- Quit script immediately
- g_debug invoked

---

### Step 4: Merge Theta with TSVR and Create Time Transformations

**Dependencies:** Step 3 (requires final theta estimates)
**Complexity:** Low (<5 minutes, data manipulation only)

**Purpose:** Merge theta_confidence with TSVR_hours time variable, create Days and log_Days_plus1 transformations for LMM candidate models (Decision D070).

**Input:**

**File 1:** data/step03_theta_confidence_paradigm.csv
**Source:** Generated by Step 3
**Columns:** composite_ID, theta_IFR/ICR/IRE, se_IFR/ICR/IRE

**File 2:** data/step00_tsvr_mapping.csv
**Source:** Generated by Step 0
**Columns:** composite_ID, UID, test, TSVR_hours

**Processing:**

**Merge Logic:**
1. Left join: theta_confidence LEFT JOIN tsvr_mapping ON composite_ID
2. If any TSVR_hours missing: CRITICAL ERROR (all participants must have timing)
3. Create time transformations:
   - Days = TSVR_hours / 24 (convert hours to days)
   - log_Days_plus1 = log(Days + 1) (log transformation for candidate models)
4. Reshape to long format for LMM:
   - Each row = one paradigm observation (UID x test x paradigm)
   - From wide (theta_IFR, theta_ICR, theta_IRE) to long (theta_confidence, paradigm)
5. Result: 1200 rows (100 participants x 4 tests x 3 paradigms)

**Output:**

**File:** data/step04_lmm_input.csv
**Format:** CSV, long format (one row per paradigm observation)
**Columns:**
- `UID` (string, participant identifier)
- `test` (string: T1, T2, T3, T4)
- `composite_ID` (string, UID_test)
- `paradigm` (string: IFR, ICR, IRE)
- `theta_confidence` (float, confidence ability for this paradigm)
- `se_confidence` (float, standard error)
- `TSVR_hours` (float, actual time since encoding)
- `Days` (float, TSVR_hours / 24)
- `log_Days_plus1` (float, log(Days + 1))
**Expected Rows:** 1200 (100 participants x 4 tests x 3 paradigms)

**Validation Requirement:**
Validation tools MUST be used after TSVR merge tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_lmm_input.csv: 1200 rows x 9 columns

*Value Ranges:*
- TSVR_hours: [0, 168] (0=encoding, 168=1 week)
- Days: [0, 7] (derived from TSVR_hours)
- log_Days_plus1: [0, 2.1] (log(1) to log(8))
- theta_confidence: [-4, 4]
- paradigm: in {IFR, ICR, IRE} only

*Data Quality:*
- Exactly 1200 rows (100 x 4 x 3)
- No NaN in TSVR_hours, Days, log_Days_plus1 (all required for LMM)
- All 100 UIDs present with 12 rows each (4 tests x 3 paradigms)
- No duplicate (UID x test x paradigm) combinations

*Log Validation:*
- Required pattern: "Merged theta with TSVR: 1200 observations"
- Required pattern: "All composite_IDs matched (no missing TSVR)"
- Forbidden patterns: "ERROR", "TSVR_hours missing for composite_ID"
- Acceptable warnings: None expected for this step

**Expected Behavior on Validation Failure:**
- Raise error
- Log failure to logs/step04_merge_theta_tsvr.log
- Quit script immediately
- g_debug invoked

---

### Step 5: Fit LMM with Paradigm x Time Interaction

**Dependencies:** Step 4 (requires LMM input data)
**Complexity:** Medium (10-20 minutes, LMM fitting with 1200 observations)

**Purpose:** Fit Linear Mixed Model to test Paradigm x Time interaction (primary hypothesis: interaction NULL, paralleling Ch5 5.3.1-5.3.2 accuracy findings).

**Input:**

**File:** data/step04_lmm_input.csv
**Source:** Generated by Step 4
**Columns:** UID, test, paradigm, theta_confidence, TSVR_hours, Days, log_Days_plus1

**Processing:**

**LMM Formula:**
```
theta_confidence ~ Paradigm * (Days + log_Days_plus1) + (Days + log_Days_plus1 | UID)
```

**Fixed Effects:**
- Paradigm main effect (IFR vs ICR vs IRE baseline differences)
- Days main effect (linear time trend)
- log_Days_plus1 main effect (nonlinear time trend)
- Paradigm x Days interaction (tests if linear slopes differ by paradigm)
- Paradigm x log_Days_plus1 interaction (tests if nonlinear slopes differ)

**Random Effects:**
- Random intercept per UID (baseline confidence varies across participants)
- Random slopes for Days and log_Days_plus1 per UID (individual decline rates)
- Unstructured covariance (allows intercept-slope correlations)

**Time Variable (Decision D070):**
Use TSVR-derived Days (actual elapsed time), NOT nominal days (0, 1, 3, 6)

**Algorithm:**
statsmodels MixedLM with REML estimation

**Workflow:**
1. Load step04_lmm_input.csv
2. Fit LMM formula above
3. Check convergence (must converge for valid inference)
4. Extract fixed effects table (coefficients, SE, z, p-values)
5. Extract random effects variance components
6. Test Paradigm x Time interactions via likelihood ratio tests (Decision D068: dual p-values)
7. Save model summary and fit statistics

**Output:**

**File 1:** data/step05_lmm_model_summary.txt
**Format:** Plain text
**Contents:**
- Formula specification
- Fixed effects table (Estimate, SE, z-value, p-value)
- Random effects variance components
- ICC (intraclass correlation)
- AIC, BIC, log-likelihood
- Convergence status
- Paradigm x Days interaction test (LRT + Wald)
- Paradigm x log_Days_plus1 interaction test (LRT + Wald)

**File 2:** data/step05_fixed_effects.csv
**Format:** CSV
**Columns:**
- `term` (string: fixed effect name)
- `estimate` (float: coefficient)
- `se` (float: standard error)
- `z_value` (float: z-statistic)
- `p_value` (float: uncorrected p-value per D068)
**Expected Rows:** ~10 (intercept + main effects + interactions)

**File 3:** data/step05_random_effects.csv
**Format:** CSV
**Columns:**
- `component` (string: variance component name)
- `variance` (float: variance estimate)
- `sd` (float: standard deviation)
**Expected Rows:** ~6 (intercept, Days slope, log_Days_plus1 slope, residual, + covariances)

**Validation Requirement:**
Validation tools MUST be used after LMM fitting tool execution. Specific validation tools determined by rq_tools (likely validate_lmm_convergence, validate_lmm_residuals, validate_lmm_assumptions_comprehensive).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_lmm_model_summary.txt exists, non-empty
- data/step05_fixed_effects.csv: ~10 rows x 5 columns
- data/step05_random_effects.csv: ~6 rows x 3 columns

*Value Ranges:*
- Coefficients: [-5, 5] (outside suggests estimation issue)
- SE: [0.01, 2.0] (very small or very large SE suggests problem)
- z_value: [-10, 10] (extreme values possible for strong effects)
- p_value: [0, 1]
- Variances: > 0 (negative variance = convergence failure)

*Data Quality:*
- Convergence: TRUE (model must converge)
- No NaN in fixed effects (estimation failure if present)
- All variances > 0 (positivity constraint)
- ICC in [0, 1] (outside suggests computation error)

*Log Validation:*
- Required pattern: "Model converged: True"
- Required pattern: "VALIDATION - PASS: LMM residuals normality"
- Required pattern: "VALIDATION - PASS: Variance components positive"
- Required pattern: "Paradigm x Days interaction: p = X.XXX (uncorrected), p = Y.YYY (LRT)"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "Variance component negative"
- Acceptable warnings: "Random slope variance near boundary (may simplify random structure)"

**Expected Behavior on Validation Failure:**
- Raise error
- Log failure to logs/step05_fit_lmm.log
- Quit script immediately
- g_debug invoked (common: need to simplify random effects, check for collinearity)

---

### Step 6: Post-Hoc Paradigm Contrasts

**Dependencies:** Step 5 (requires fitted LMM)
**Complexity:** Low (5-10 minutes, contrast computation only)

**Purpose:** Compute pairwise paradigm comparisons for baseline confidence (Day 0) and slope differences with dual p-value reporting (Decision D068).

**Input:**

**File:** data/step05_lmm_model_summary.txt (or fitted model object)
**Source:** Generated by Step 5

**Processing:**

**Contrasts to Compute:**

*Baseline Comparisons (Day 0):*
1. IFR vs ICR baseline confidence
2. IFR vs IRE baseline confidence
3. ICR vs IRE baseline confidence

*Slope Comparisons (Paradigm x Days interaction):*
4. IFR vs ICR slope difference (linear)
5. IFR vs IRE slope difference (linear)
6. ICR vs IRE slope difference (linear)

*Slope Comparisons (Paradigm x log_Days_plus1 interaction):*
7. IFR vs ICR slope difference (nonlinear)
8. IFR vs IRE slope difference (nonlinear)
9. ICR vs IRE slope difference (nonlinear)

**Correction Method (Decision D068):**
- Report BOTH uncorrected and Bonferroni-corrected p-values
- Bonferroni: alpha = 0.05 / 9 comparisons = 0.0056 threshold

**Workflow:**
1. Load fitted LMM from Step 5
2. Define contrast matrices for each pairwise comparison
3. Compute contrasts using statsmodels or emmeans-equivalent
4. Extract: estimate, SE, z-value, p_uncorrected, p_bonferroni
5. Compute Cohen's d effect sizes for each contrast
6. Save contrasts table

**Output:**

**File 1:** data/step06_paradigm_contrasts.csv
**Format:** CSV
**Columns:**
- `contrast` (string: comparison name, e.g., "IFR vs ICR baseline")
- `estimate` (float: difference estimate)
- `se` (float: standard error)
- `z_value` (float: z-statistic)
- `p_uncorrected` (float: uncorrected p-value per D068)
- `p_bonferroni` (float: Bonferroni-corrected p-value per D068)
- `cohens_d` (float: effect size)
**Expected Rows:** 9 contrasts

**File 2:** data/step06_effect_sizes.csv
**Format:** CSV
**Columns:**
- `contrast` (string)
- `cohens_d` (float: standardized effect size)
- `interpretation` (string: negligible/small/medium/large)
**Expected Rows:** 9 contrasts

**Validation Requirement:**
Validation tools MUST be used after post-hoc contrast tool execution. Specific validation tools determined by rq_tools (likely validate_contrasts_dual_pvalues per D068).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_paradigm_contrasts.csv: 9 rows x 7 columns
- data/step06_effect_sizes.csv: 9 rows x 3 columns

*Value Ranges:*
- estimate: [-3, 3] (differences in theta units)
- se: [0.05, 1.0] (very small or large SE suggests problem)
- p_uncorrected: [0, 1]
- p_bonferroni: [0, 1], >= p_uncorrected (correction increases p)
- cohens_d: [-2, 2] (outside suggests very large or erroneous effect)

*Data Quality:*
- All 9 contrasts present (baseline x3, linear slope x3, nonlinear slope x3)
- p_bonferroni >= p_uncorrected for all rows (correction never decreases p)
- No NaN in estimate or p-values

*Log Validation:*
- Required pattern: "VALIDATION - PASS: Dual p-values present (uncorrected + bonferroni)"
- Required pattern: "Computed 9 paradigm contrasts with effect sizes"
- Forbidden patterns: "ERROR", "Missing p_bonferroni column"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- Raise error
- Log failure to logs/step06_compute_post_hoc_contrasts.log
- Quit script immediately
- g_debug invoked

---

### Step 7: Compare to Ch5 5.3.1 Accuracy Paradigm Analysis

**Dependencies:** Step 6 (requires paradigm contrast results)
**Complexity:** Low (<5 minutes, comparison only)

**Purpose:** Document how confidence paradigm effects compare to accuracy paradigm effects from Ch5 5.3.1-5.3.2 (test if confidence replicates accuracy NULL slope findings).

**Input:**

**File 1:** data/step06_paradigm_contrasts.csv
**Source:** Generated by Step 6 (confidence paradigm contrasts)

**File 2:** results/ch5/5.3.1/data/step06_paradigm_contrasts.csv (if exists)
**Source:** Ch5 RQ 5.3.1 accuracy paradigm analysis
**Note:** File may not exist yet if Ch5 5.3.1 not completed. In that case, create placeholder comparison noting "Ch5 5.3.1 pending".

**Processing:**

**Comparison Metrics:**
1. Baseline effect sizes (confidence vs accuracy)
   - Compare Cohen's d for IFR vs ICR, IFR vs IRE, ICR vs IRE at Day 0
   - Expected: Recognition highest baseline for BOTH accuracy and confidence
2. Slope effect sizes (confidence vs accuracy)
   - Compare Cohen's d for paradigm x time interactions
   - Expected: BOTH NULL (p > 0.05) - parallel decline rates
3. Pattern consistency
   - Do confidence and accuracy show same paradigm ordering?
   - Do confidence and accuracy show same NULL slope pattern?

**Workflow:**
1. Load confidence contrasts from step06_paradigm_contrasts.csv
2. Load accuracy contrasts from Ch5 5.3.1 (if available)
3. Create comparison table:
   - Contrast name
   - Confidence effect size
   - Accuracy effect size (if available)
   - Pattern match (YES/NO/PENDING)
4. Summarize:
   - Baseline: Do both show Recognition > Cued > Free?
   - Slopes: Do both show NULL interaction (parallel decline)?
5. Save comparison report

**Output:**

**File:** data/step07_ch5_comparison.csv
**Format:** CSV
**Columns:**
- `contrast` (string: comparison name)
- `confidence_d` (float: Cohen's d from this RQ)
- `confidence_p` (float: p-value from this RQ)
- `accuracy_d` (float: Cohen's d from Ch5 5.3.1, or NA if pending)
- `accuracy_p` (float: p-value from Ch5 5.3.1, or NA if pending)
- `pattern_match` (string: YES/NO/PENDING)
- `interpretation` (string: brief interpretation)
**Expected Rows:** 9 contrasts

**Validation Requirement:**
Validation tools MUST be used after comparison tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_ch5_comparison.csv: 9 rows x 7 columns

*Value Ranges:*
- confidence_d: [-2, 2]
- confidence_p: [0, 1]
- accuracy_d: [-2, 2] or NA
- accuracy_p: [0, 1] or NA
- pattern_match: in {YES, NO, PENDING}

*Data Quality:*
- All 9 contrasts present
- If Ch5 5.3.1 available: accuracy_d and accuracy_p not NA
- If Ch5 5.3.1 pending: accuracy_d and accuracy_p all NA, pattern_match all "PENDING"

*Log Validation:*
- Required pattern: "Comparison to Ch5 5.3.1 complete"
- If pending: "Ch5 5.3.1 not available - comparison deferred"
- Forbidden patterns: "ERROR"
- Acceptable warnings: "Ch5 5.3.1 pending - using NA for accuracy metrics"

**Expected Behavior on Validation Failure:**
- Raise error
- Log failure to logs/step07_compare_to_ch5.log
- Quit script immediately
- g_debug invoked

---

### Step 8: Prepare Trajectory Plot Data (Dual-Scale per D069)

**Dependencies:** Steps 3, 4 (requires theta estimates and TSVR mapping)
**Complexity:** Low (5-10 minutes, data aggregation only)

**Purpose:** Create plot source CSVs for trajectory visualization with dual-scale (theta + probability) per Decision D069. Option B architecture: g_code creates plot source CSV during analysis, rq_plots reads CSV and generates PNG later.

**Plot Description:**
Trajectory plot showing confidence decline over time (Days 0-6) with 95% confidence bands, grouped by paradigm (IFR, ICR, IRE). Dual-scale output: theta scale (-4 to 4) AND probability scale (0 to 1) for interpretability.

**Input:**

**File 1:** data/step03_theta_confidence_paradigm.csv
**Source:** Generated by Step 3
**Columns:** composite_ID, theta_IFR/ICR/IRE, se_IFR/ICR/IRE

**File 2:** data/step04_lmm_input.csv
**Source:** Generated by Step 4
**Columns:** UID, test, paradigm, theta_confidence, TSVR_hours, Days

**Processing:**

**Aggregation Logic:**
1. Merge theta_confidence with TSVR/Days on composite_ID and paradigm
2. Group by paradigm + test (or paradigm + Days bins)
3. Compute observed means: mean(theta_confidence) per group
4. Compute 95% CI: SE = sd(theta_confidence) / sqrt(n), CI = mean +/- 1.96*SE
5. For probability scale: convert theta to probability using IRT transform
   - Probability = 1 / (1 + exp(-(a*theta - b)))
   - Use typical GRM parameters: a=1.0, b=0 (neutral item)
6. Create two output CSVs: theta_data and probability_data

**Output:**

**File 1:** data/step08_trajectory_theta_data.csv
**Format:** CSV, plot source data for theta-scale trajectory
**Columns:**
- `paradigm` (string: IFR, ICR, IRE)
- `Days` (float: time since encoding in days, e.g., 0, 1, 3, 6)
- `theta_mean` (float: mean theta_confidence per paradigm per timepoint)
- `CI_lower` (float: lower 95% confidence bound)
- `CI_upper` (float: upper 95% confidence bound)
- `n` (int: sample size per group)
**Expected Rows:** 12 (3 paradigms x 4 timepoints)

**File 2:** data/step08_trajectory_probability_data.csv
**Format:** CSV, plot source data for probability-scale trajectory (Decision D069 dual-scale)
**Columns:**
- `paradigm` (string: IFR, ICR, IRE)
- `Days` (float: 0, 1, 3, 6)
- `probability_mean` (float: mean probability per paradigm per timepoint, range [0,1])
- `CI_lower` (float: lower 95% CI on probability scale)
- `CI_upper` (float: upper 95% CI on probability scale)
- `n` (int: sample size)
**Expected Rows:** 12

**Validation Requirement:**
Validation tools MUST be used after plot data preparation tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_trajectory_theta_data.csv: 12 rows x 6 columns
- data/step08_trajectory_probability_data.csv: 12 rows x 6 columns

*Value Ranges:*
- Days: in {0, 1, 3, 6} (nominal timepoints)
- theta_mean: [-4, 4] (typical IRT ability range)
- probability_mean: [0, 1] (valid probability range)
- CI_lower < mean < CI_upper for all rows
- n: [80, 100] per timepoint (some missing data acceptable)

*Data Quality:*
- Exactly 12 rows per file (3 paradigms x 4 timepoints)
- All paradigms represented: IFR, ICR, IRE
- All timepoints represented: 0, 1, 3, 6 Days
- No NaN in theta_mean, probability_mean, CI bounds
- No duplicate (paradigm x Days) combinations

*Log Validation:*
- Required pattern: "Plot data preparation complete: 12 rows created per scale"
- Required pattern: "All paradigms represented: IFR, ICR, IRE"
- Required pattern: "All timepoints represented: 0, 1, 3, 6 Days"
- Forbidden patterns: "ERROR", "NaN values detected", "Missing paradigm"
- Acceptable warnings: "Sample size <100 at Day 6 (missing data)"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step08_prepare_trajectory_plot_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- g_debug invoked to diagnose root cause

**Plotting Function (rq_plots will call later):**
Trajectory plot with confidence bands. rq_plots agent maps this description to tools/plots.py functions:
- `plot_trajectory()` for theta scale
- `plot_trajectory_probability()` for probability scale
- Plot reads data/step08_trajectory_theta_data.csv and data/step08_trajectory_probability_data.csv
- No data aggregation in rq_plots (visualization only per Option B)
- PNG outputs saved to plots/ folder by rq_plots

---

## Expected Data Formats

### IRT Input Format (Step 0)

**Wide Format:**
- Rows: composite_ID (UID_test combinations, ~400 rows)
- Columns: TC_* item tags (5-category ordinal values: 0, 0.25, 0.5, 0.75, 1.0, NaN)
- Example row: P001_T1 | 0.5 | 0.75 | 0.25 | ... (one value per TC_* item)

**Q-Matrix Format:**
- Rows: items (~102 TC_* items)
- Columns: factor1_IFR, factor2_ICR, factor3_IRE (binary 0/1 loadings)
- Example row: TC_IFR_item1 | 1 | 0 | 0 (loads on IFR factor only)

### Theta Estimates Format (Step 3)

**Wide Format:**
- Rows: composite_ID (~400 rows)
- Columns: theta_IFR, theta_ICR, theta_IRE, se_IFR, se_ICR, se_IRE
- Example row: P001_T1 | -0.52 | 0.31 | 0.88 | 0.18 | 0.21 | 0.16

### LMM Input Format (Step 4)

**Long Format:**
- Rows: UID x test x paradigm observations (1200 rows)
- Columns: UID, test, paradigm, theta_confidence, se_confidence, TSVR_hours, Days, log_Days_plus1
- Example row: P001 | T1 | IFR | -0.52 | 0.18 | 0.0 | 0.0 | 0.0

### Plot Data Format (Step 8)

**Aggregated Format:**
- Rows: paradigm x timepoint combinations (12 rows per scale)
- Columns: paradigm, Days, theta_mean (or probability_mean), CI_lower, CI_upper, n
- Example row: IFR | 0 | 0.85 | 0.72 | 0.98 | 98

---

## Cross-RQ Dependencies

**This RQ uses:** Only dfData.csv (RAW data extraction)

**No dependencies on other RQs:** Can be executed independently

**Execution order:** Flexible within Chapter 6

**Data Sources:**
- data/cache/dfData.csv (participant confidence ratings, TC_* items)
- TSVR timing data (embedded in dfData.csv)

**Optional Cross-Reference to Ch5 5.3.1:**
- Step 7 compares confidence paradigm effects to accuracy paradigm effects
- If Ch5 5.3.1 not yet complete, Step 7 creates placeholder comparison noting "Ch5 5.3.1 pending"
- This is NOT a blocking dependency (Step 7 can execute with NA values for accuracy metrics)

---

## Validation Requirements

**CRITICAL MANDATE:**

Every analysis step in this plan MUST use validation tools after analysis tool execution.

This is not optional. This is the core architectural principle preventing cascading failures observed in v3.0 (where analysis errors propagated undetected through multiple downstream steps before discovery).

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

**Step 0:** Data extraction validation
- File existence, row/column counts, value ranges, composite_ID format, Q-matrix structure

**Step 1:** IRT Pass 1 calibration validation
- Convergence, parameter bounds, threshold ordering (b1 < b2 < b3 < b4), theta range, SE range

**Step 2:** Purification validation
- Retention rate, minimum items per factor, threshold enforcement

**Step 3:** IRT Pass 2 calibration validation
- Convergence, precision improvement vs Pass 1, parameter bounds, theta range

**Step 4:** TSVR merge validation
- Row count (1200), no missing TSVR_hours, time transformation correctness

**Step 5:** LMM fitting validation
- Convergence, residuals normality, variance positivity, ICC bounds, dual p-values for interactions

**Step 6:** Post-hoc contrasts validation
- Dual p-values (uncorrected + Bonferroni), contrast completeness, effect size bounds

**Step 7:** Ch5 comparison validation
- Comparison table completeness, handling of missing Ch5 data

**Step 8:** Plot data preparation validation
- Row count (12 per scale), paradigm completeness, timepoint completeness, value ranges, no NaN

---

## Summary

**Total Steps:** 8 analysis steps (Step 0: extraction + Steps 1-7: analysis + Step 8: plot prep)

**Estimated Runtime:**
- MINIMAL settings (pipeline validation): ~30 minutes
- Production settings: 90-120 minutes total
  - Step 0: 5-10 min
  - Step 1: 60-90 min (GRM Pass 1)
  - Step 2: <5 min
  - Step 3: 60-90 min (GRM Pass 2)
  - Step 4: <5 min
  - Step 5: 10-20 min
  - Step 6: 5-10 min
  - Step 7: <5 min
  - Step 8: 5-10 min

**Cross-RQ Dependencies:** None (RAW data only)

**Primary Outputs:**
- data/step03_theta_confidence_paradigm.csv (final confidence ability estimates, 3 factors)
- data/step05_lmm_model_summary.txt (Paradigm x Time interaction test)
- data/step06_paradigm_contrasts.csv (post-hoc comparisons with dual p-values)
- data/step07_ch5_comparison.csv (confidence vs accuracy paradigm effects)
- data/step08_trajectory_theta_data.csv (plot source CSV, theta scale)
- data/step08_trajectory_probability_data.csv (plot source CSV, probability scale)

**Validation Coverage:** 100% (all 9 steps have validation requirements with 4-layer substance criteria)

**Key Hypotheses:**
- Paradigm x Time interaction NULL (p > 0.05) - parallel decline rates across paradigms
- Recognition shows highest baseline confidence (retrieval support hypothesis)
- Confidence pattern replicates accuracy pattern from Ch5 5.3.1-5.3.2

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent for RQ 6.4.1
