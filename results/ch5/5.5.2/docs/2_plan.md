# Analysis Plan: RQ 5.5.2 - Source-Destination Consolidation (Two-Phase)

**Research Question:** 5.5.2
**Created:** 2025-12-04
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines whether source (-U- pick-up location) and destination (-D- put-down location) memories exhibit differential consolidation patterns across two retention windows: Early phase (Day 0->1, 0-48h) and Late phase (Day 1->6, 48-144h). The analysis uses a piecewise linear mixed model with 48-hour breakpoint to test if weaker initial encoding of destination memory (per RQ 5.5.1 findings) leads to steeper Early-phase forgetting due to sleep-dependent consolidation preferentially benefiting strongly encoded traces.

**Pipeline:** LMM only (NO IRT - uses DERIVED theta scores from RQ 5.5.1)

**Steps:** 8 total analysis steps (Step 0 through Step 7)

**Estimated Runtime:** Low to Medium (5-20 minutes total - no IRT calibration, LMM fitting only)

**Key Decisions Applied:**
- Decision D070: TSVR_hours as time variable (inherited from RQ 5.5.1)
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni alpha=0.025)
- Decision D069: Dual-scale trajectory plots (theta + probability scales)
- NO Decision D039: No 2-pass IRT purification (uses existing theta from RQ 5.5.1)

---

## Analysis Plan

### Step 0: Load Dependency Data from RQ 5.5.1

**Purpose:** Load IRT theta scores and TSVR mapping from completed RQ 5.5.1, verify dependency completion

**Dependencies:** None (first step, but RQ 5.5.1 must be complete before execution)

**Complexity:** Low (<1 minute - data loading and validation only)

**Input:**

**File 1:** results/ch5/5.5.1/data/step03_theta_scores.csv
**Source:** RQ 5.5.1 Step 3 (IRT Pass 2 calibration)
**Format:** CSV with columns:
  - `UID` (string, format: P### with leading zeros, e.g., P001)
  - `test` (string, values: T1, T2, T3, T4)
  - `theta_source` (float, IRT ability estimate for -U- pick-up locations)
  - `theta_destination` (float, IRT ability estimate for -D- put-down locations)
  - `se_source` (float, standard error for theta_source)
  - `se_destination` (float, standard error for theta_destination)
**Expected Rows:** 400 (100 participants x 4 tests)
**Expected Columns:** 6

**File 2:** results/ch5/5.5.1/data/step00_tsvr_mapping.csv
**Source:** RQ 5.5.1 Step 0 (TSVR extraction)
**Format:** CSV with columns:
  - `UID` (string, format: P###)
  - `test` (string, values: T1, T2, T3, T4)
  - `TSVR_hours` (float, actual hours since VR encoding, range: [0, 168])
**Expected Rows:** 400 (100 participants x 4 tests)
**Expected Columns:** 3

**File 3:** results/ch5/5.5.1/status.yaml
**Source:** RQ 5.5.1 workflow tracking
**Purpose:** Verify RQ 5.5.1 completed successfully before loading data

**Processing:**

1. **Dependency Verification:**
   - Read results/ch5/5.5.1/status.yaml
   - Check `rq_results.status = "success"` (entire RQ 5.5.1 workflow complete)
   - If status != success: QUIT with EXPECTATIONS ERROR (dependency incomplete)

2. **Load Theta Scores:**
   - Read results/ch5/5.5.1/data/step03_theta_scores.csv
   - Validate 400 rows (100 UID x 4 tests)
   - Validate 6 columns present (UID, test, theta_source, theta_destination, se_source, se_destination)

3. **Load TSVR Mapping:**
   - Read results/ch5/5.5.1/data/step00_tsvr_mapping.csv
   - Validate 400 rows
   - Validate 3 columns present (UID, test, TSVR_hours)

4. **Merge on UID + test:**
   - Left join: theta_scores (left) + tsvr_mapping (right) on [UID, test]
   - Expected result: 400 rows, 8 columns (UID, test, theta_source, theta_destination, se_source, se_destination, TSVR_hours, no NaN in TSVR_hours)
   - If any TSVR_hours missing: QUIT with error (incomplete TSVR data)

**Output:**

**File:** data/step00_theta_from_rq551.csv
**Format:** CSV, merged theta scores + TSVR
**Columns:**
  - `UID` (string)
  - `test` (string, T1/T2/T3/T4)
  - `theta_source` (float)
  - `theta_destination` (float)
  - `se_source` (float)
  - `se_destination` (float)
  - `TSVR_hours` (float, range: [0, 168])
**Expected Rows:** 400 (100 participants x 4 tests)
**Expected Columns:** 7

**Validation Requirement:**

Validation tools MUST be used after data loading and merge execution. Specific validation tools will be determined by rq_tools based on data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_theta_from_rq551.csv exists (exact path)
- Expected rows: 400 (100 UID x 4 tests)
- Expected columns: 7 (UID, test, theta_source, theta_destination, se_source, se_destination, TSVR_hours)
- Data types: UID (object/string), test (object/string), theta_source (float64), theta_destination (float64), se_source (float64), se_destination (float64), TSVR_hours (float64)

*Value Ranges:*
- theta_source in [-3, 3] (typical IRT ability range)
- theta_destination in [-3, 3]
- se_source in [0.1, 1.0] (SEs above 1.0 indicate unreliable estimates)
- se_destination in [0.1, 1.0]
- TSVR_hours in [0, 168] (0 = encoding T1, 168 = 1 week T4)

*Data Quality:*
- No NaN values tolerated in any column (all cells must have valid values)
- Expected N: Exactly 400 rows (no data loss from merge)
- All 100 UIDs present (P001-P100)
- All 4 tests present per UID (T1, T2, T3, T4)
- No duplicate UID x test combinations

*Log Validation:*
- Required pattern: "RQ 5.5.1 dependency verified: status = success"
- Required pattern: "Loaded theta scores: 400 rows"
- Required pattern: "Loaded TSVR mapping: 400 rows"
- Required pattern: "Merged successfully: 400 rows, 0 missing TSVR values"
- Forbidden patterns: "ERROR", "status = pending", "status = failed", "NaN values detected"
- Acceptable warnings: None expected for data loading step

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "RQ 5.5.1 incomplete: status = pending")
- Log failure to logs/step00_load_dependency_data.log
- Quit script immediately (do NOT proceed to Step 1)
- Master invokes g_debug to diagnose root cause (e.g., run RQ 5.5.1 first)

---

### Step 1: Create Piecewise Time Variables

**Purpose:** Create time variables for piecewise LMM with 48-hour breakpoint: Early segment (0-48h), Late segment (48-144h)

**Dependencies:** Step 0 (requires merged theta + TSVR data)

**Complexity:** Low (<1 minute - data transformation only)

**Input:**

**File:** data/step00_theta_from_rq551.csv (400 rows from Step 0)
**Columns Required:** UID, test, TSVR_hours

**Processing:**

1. **Assign Segment Factor:**
   - If TSVR_hours in [0, 48]: Segment = "Early" (consolidation window)
   - If TSVR_hours in (48, 168]: Segment = "Late" (post-consolidation decay)
   - Note: 48-hour breakpoint based on consolidation literature (Diekelmann & Born, 2010)

2. **Compute Days_within (recentered time for interpretable intercepts):**
   - Early segment: Days_within = TSVR_hours / 24 (range: [0, 2] days)
   - Late segment: Days_within = (TSVR_hours - 48) / 24 (range: [0, 5] days, recentered to 0 at segment start)
   - Purpose: Days_within = 0 at start of each segment, so intercept = segment start value

3. **Add to dataframe:**
   - Append Segment (categorical: Early, Late)
   - Append Days_within (float: recentered days within segment)

**Output:**

**File:** data/step01_piecewise_time_variables.csv
**Format:** CSV, wide format (one row per UID x test)
**Columns:**
  - All columns from step00 (UID, test, theta_source, theta_destination, se_source, se_destination, TSVR_hours)
  - `Segment` (string, values: "Early", "Late")
  - `Days_within` (float, range: [0, 5], recentered time within each segment)
**Expected Rows:** 400 (100 UID x 4 tests)
**Expected Columns:** 9

**Validation Requirement:**

Validation tools MUST be used after time variable creation. Specific validation tools determined by rq_tools based on transformation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_piecewise_time_variables.csv exists
- Expected rows: 400
- Expected columns: 9
- Data types: Segment (object/string), Days_within (float64)

*Value Ranges:*
- Segment in {"Early", "Late"} (exactly 2 unique values)
- Days_within in [0, 5] (recentered, cannot be negative)
- Early segment: Days_within in [0, 2] (tests T1->T2)
- Late segment: Days_within in [0, 5] (tests T2->T3->T4)

*Data Quality:*
- No NaN values in Segment or Days_within columns
- Segment assignment correct: T1 (Day 0, ~0-24h) -> Early, T2 (Day 1, ~24-48h) -> Early, T3 (Day 3, ~72h) -> Late, T4 (Day 6, ~144h) -> Late
- Expected distribution: ~200 Early observations (T1+T2), ~200 Late observations (T3+T4)

*Log Validation:*
- Required pattern: "Segment assignment: 200 Early, 200 Late"
- Required pattern: "Days_within range: [0.00, 5.00]"
- Forbidden patterns: "ERROR", "NaN values detected", "negative Days_within"
- Acceptable warnings: "Minor TSVR variability in segment assignment" (some T2 may be >48h if delayed)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Segment assignment failed: 150 Early, 250 Late")
- Log failure to logs/step01_create_piecewise_time_variables.log
- Quit script immediately
- g_debug invoked to diagnose (check TSVR values, breakpoint logic)

---

### Step 2: Reshape Wide to Long Format

**Purpose:** Convert wide-format data (1 row per UID x test, 2 theta columns) to long format (2 rows per UID x test, 1 theta column, LocationType factor) for LMM fitting

**Dependencies:** Step 1 (requires piecewise time variables)

**Complexity:** Low (<1 minute - data reshaping only)

**Input:**

**File:** data/step01_piecewise_time_variables.csv (400 rows from Step 1)
**Format:** Wide (1 row per UID x test, theta_source and theta_destination as separate columns)

**Processing:**

1. **Reshape from wide to long:**
   - Input: 400 rows x 9 columns (UID, test, theta_source, theta_destination, se_source, se_destination, TSVR_hours, Segment, Days_within)
   - Reshape: "melt" theta_source and theta_destination into single theta column with LocationType factor
   - Output: 800 rows x 9 columns (UID, test, LocationType, theta, se, TSVR_hours, Segment, Days_within)

2. **Create LocationType factor:**
   - Values: "Source" (for theta_source), "Destination" (for theta_destination)
   - Treatment coding: Source as reference level (for LMM contrast interpretation)

3. **Match SE to theta:**
   - When LocationType = "Source": se = se_source
   - When LocationType = "Destination": se = se_destination

**Output:**

**File:** data/step02_lmm_input_long.csv
**Format:** CSV, long format (2 rows per UID x test)
**Columns:**
  - `UID` (string, participant identifier)
  - `test` (string, T1/T2/T3/T4)
  - `LocationType` (string, values: "Source", "Destination", treatment-coded with Source as reference)
  - `theta` (float, IRT ability estimate for given location type)
  - `se` (float, standard error for theta)
  - `TSVR_hours` (float, actual hours since encoding)
  - `Segment` (string, "Early" or "Late")
  - `Days_within` (float, recentered time within segment)
**Expected Rows:** 800 (400 observations x 2 location types)
**Expected Columns:** 8

**Validation Requirement:**

Validation tools MUST be used after reshape operation. Specific validation tools determined by rq_tools based on data format transformation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_lmm_input_long.csv exists
- Expected rows: 800 (100 UID x 4 tests x 2 location types)
- Expected columns: 8
- Data types: LocationType (object/string), theta (float64), se (float64)

*Value Ranges:*
- theta in [-3, 3]
- se in [0.1, 1.0]
- LocationType in {"Source", "Destination"}

*Data Quality:*
- No NaN values in any column
- Expected distribution: 400 Source observations, 400 Destination observations
- Each UID x test combination appears exactly 2 times (once for Source, once for Destination)
- All 100 UIDs present, all 4 tests present per UID

*Log Validation:*
- Required pattern: "Reshaped to long format: 800 rows"
- Required pattern: "LocationType distribution: 400 Source, 400 Destination"
- Required pattern: "All 100 UIDs present with 8 observations each (4 tests x 2 locations)"
- Forbidden patterns: "ERROR", "NaN values detected", "duplicate rows"
- Acceptable warnings: None expected for reshape step

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Expected 800 rows, found 798")
- Log failure to logs/step02_reshape_wide_to_long.log
- Quit script immediately
- g_debug invoked to diagnose (check reshape logic, missing data)

---

### Step 3: Fit Piecewise LMM

**Purpose:** Fit piecewise linear mixed model testing LocationType x Phase interaction (primary hypothesis)

**Dependencies:** Step 2 (requires long-format LMM input)

**Complexity:** Medium (5-10 minutes - LMM fitting with 3-way interaction)

**Input:**

**File:** data/step02_lmm_input_long.csv (800 rows from Step 2)
**Columns Required:** UID, theta, Days_within, Segment, LocationType

**Processing:**

1. **Fit Piecewise LMM:**
   - Formula: `theta ~ Days_within * Segment * LocationType + (1 + Days_within | UID)`
   - Fixed effects:
     - Days_within (slope within segment)
     - Segment (Early vs Late intercept difference)
     - LocationType (Source vs Destination intercept difference)
     - Days_within:Segment (consolidation benefit: Early slope differs from Late slope)
     - Days_within:LocationType (location-specific forgetting rates)
     - Segment:LocationType (location-specific segment intercepts)
     - Days_within:Segment:LocationType (PRIMARY HYPOTHESIS: LocationType x Phase interaction on slopes)
   - Random effects:
     - Random intercepts by UID (baseline individual differences)
     - Random slopes for Days_within by UID (individual forgetting rate differences within segments)
   - Estimation: REML=False (for AIC comparison if needed)
   - Treatment coding: Source as reference for LocationType, Early as reference for Segment

2. **Save model object:**
   - Save fitted model to data/step03_piecewise_lmm_model.pkl (for downstream slope extraction)

3. **Extract model summary:**
   - Fixed effects table (coefficients, SE, z-scores, p-values)
   - Random effects variance components
   - Convergence status
   - Model fit indices (AIC, BIC, log-likelihood)

**Output:**

**File 1:** data/step03_piecewise_lmm_model.pkl
**Format:** Pickle file, saved statsmodels MixedLM model object
**Purpose:** Downstream slope extraction in Step 4

**File 2:** data/step03_piecewise_lmm_summary.txt
**Format:** Text file, model summary output
**Contents:**
  - Fixed effects table (8 terms: intercept, Days_within, Segment, LocationType, 2-way interactions x3, 3-way interaction)
  - Random effects variance components (var_intercept, var_slope, cov_int_slope, var_residual)
  - Convergence status (converged: True/False)
  - Model fit: AIC, BIC, log-likelihood
  - Sample: N=100 participants, 800 observations

**Validation Requirement:**

Validation tools MUST be used after LMM fitting. Specific validation tools determined by rq_tools based on LMM convergence and fit requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_piecewise_lmm_model.pkl exists (file size > 10 KB)
- data/step03_piecewise_lmm_summary.txt exists (file size > 1 KB)

*Model Convergence:*
- model.converged = True (required, no singular fit warnings)
- Fixed effects: 8 terms present (intercept + 7 interaction terms)
- Random effects: var_intercept > 0, var_slope > 0 (no negative variances)

*Value Ranges:*
- Fixed effect coefficients: reasonable bounds (|coef| < 5.0 on theta scale)
- Standard errors: all finite, positive (no NaN or inf)
- p-values: all in [0, 1]

*Data Quality:*
- Model used all 800 observations (no exclusions due to missing data)
- Random effects: 100 groups (one per UID)

*Log Validation:*
- Required pattern: "Model converged: True"
- Required pattern: "Fixed effects: 8 terms estimated"
- Required pattern: "Random effects: 100 groups (UID)"
- Required pattern: "Observations: 800"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "Singular matrix", "NaN coefficients"
- Acceptable warnings: "Gradient not finite" (if model still converged)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Model did not converge after 100 iterations")
- Log failure to logs/step03_fit_piecewise_lmm.log
- Quit script immediately (do NOT proceed to slope extraction)
- g_debug invoked to diagnose (common causes: insufficient data, random effects too complex)

---

### Step 4: Extract Segment-Location Slopes

**Purpose:** Extract 4 segment-location slopes via linear combinations from fitted piecewise LMM

**Dependencies:** Step 3 (requires fitted piecewise LMM model)

**Complexity:** Low (<1 minute - coefficient extraction and linear algebra)

**Input:**

**File:** data/step03_piecewise_lmm_model.pkl (fitted model from Step 3)

**Processing:**

1. **Load fitted model:**
   - Read data/step03_piecewise_lmm_model.pkl
   - Verify convergence status (model.converged = True)

2. **Extract 4 segment-location slopes via linear combinations:**

   Model formula: `theta ~ Days_within * Segment * LocationType`

   Treatment coding: Source as reference, Early as reference

   **Source_Early slope:**
   - Linear combination: beta_Days_within (main effect)
   - Represents: Forgetting rate for Source memory during Early phase (Day 0->1)

   **Source_Late slope:**
   - Linear combination: beta_Days_within + beta_Days_within:Segment[Late]
   - Represents: Forgetting rate for Source memory during Late phase (Day 1->6)

   **Destination_Early slope:**
   - Linear combination: beta_Days_within + beta_Days_within:LocationType[Destination]
   - Represents: Forgetting rate for Destination memory during Early phase

   **Destination_Late slope:**
   - Linear combination: beta_Days_within + beta_Days_within:Segment[Late] + beta_Days_within:LocationType[Destination] + beta_Days_within:Segment:LocationType
   - Represents: Forgetting rate for Destination memory during Late phase

3. **Compute standard errors via delta method:**
   - Use variance-covariance matrix of fixed effects
   - Propagate uncertainty through linear combinations
   - Compute 95% confidence intervals: CI_lower = estimate - 1.96*SE, CI_upper = estimate + 1.96*SE

**Output:**

**File:** data/step04_segment_location_slopes.csv
**Format:** CSV, 4 rows (one per segment-location combination)
**Columns:**
  - `Segment` (string, "Early" or "Late")
  - `LocationType` (string, "Source" or "Destination")
  - `slope` (float, forgetting rate in theta units per day)
  - `SE` (float, standard error of slope estimate)
  - `CI_lower` (float, lower 95% confidence bound)
  - `CI_upper` (float, upper 95% confidence bound)
  - `p_value` (float, two-tailed test of slope != 0)
**Expected Rows:** 4
**Expected Columns:** 7

**Validation Requirement:**

Validation tools MUST be used after slope extraction. Specific validation tools determined by rq_tools based on linear combination computation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_segment_location_slopes.csv exists
- Expected rows: 4 (Source_Early, Source_Late, Destination_Early, Destination_Late)
- Expected columns: 7
- Data types: slope (float64), SE (float64), CI_lower (float64), CI_upper (float64), p_value (float64)

*Value Ranges:*
- slope in [-2, 0] (forgetting = negative slope, typical range)
- SE in [0.01, 1.0] (standard errors should be finite and reasonable)
- CI_lower < slope < CI_upper (confidence interval properly ordered)
- p_value in [0, 1]

*Data Quality:*
- No NaN values in any column
- All 4 segment-location combinations present (no duplicates, no missing)
- Confidence intervals non-overlapping or overlapping as expected from hypothesis

*Log Validation:*
- Required pattern: "Extracted 4 segment-location slopes"
- Required pattern: "All slopes have valid SE and 95% CI"
- Forbidden patterns: "ERROR", "NaN in slope estimates", "CI_lower > CI_upper"
- Acceptable warnings: None expected for linear combination step

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "NaN slope for Destination_Late")
- Log failure to logs/step04_extract_segment_location_slopes.log
- Quit script immediately
- g_debug invoked to diagnose (check model convergence, variance-covariance matrix)

---

### Step 5: Test Consolidation Benefit Per Location Type

**Purpose:** Test whether each location type shows consolidation benefit (Early slope > Late slope)

**Dependencies:** Step 4 (requires segment-location slopes)

**Complexity:** Low (<1 minute - hypothesis testing on extracted slopes)

**Input:**

**File:** data/step04_segment_location_slopes.csv (4 rows from Step 4)

**Processing:**

1. **Compute consolidation benefit per location type:**
   - **Source consolidation benefit:** Source_Early_slope - Source_Late_slope
   - **Destination consolidation benefit:** Destination_Early_slope - Destination_Late_slope
   - Positive value = Early forgetting steeper than Late (consolidation benefit present)

2. **Compute standard error via delta method:**
   - SE(difference) = sqrt(SE_Early^2 + SE_Late^2 - 2*cov(Early, Late))
   - Use variance-covariance matrix from fitted model

3. **Compute 95% confidence interval:**
   - CI_lower = difference - 1.96*SE
   - CI_upper = difference + 1.96*SE

4. **Statistical test:**
   - If CI excludes 0: consolidation benefit significant at alpha = 0.05
   - Report as: "Consolidation benefit confirmed" if CI_lower > 0, else "No consolidation benefit"

**Output:**

**File:** data/step05_consolidation_benefit.csv
**Format:** CSV, 2 rows (one per location type)
**Columns:**
  - `LocationType` (string, "Source" or "Destination")
  - `Early_slope` (float, forgetting rate during Early phase)
  - `Late_slope` (float, forgetting rate during Late phase)
  - `Difference` (float, Early - Late, positive = consolidation benefit)
  - `SE` (float, standard error of difference)
  - `CI_lower` (float, lower 95% confidence bound)
  - `CI_upper` (float, upper 95% confidence bound)
  - `Significant` (boolean, True if CI excludes 0)
**Expected Rows:** 2 (Source, Destination)
**Expected Columns:** 8

**Validation Requirement:**

Validation tools MUST be used after consolidation benefit testing. Specific validation tools determined by rq_tools based on hypothesis test requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_consolidation_benefit.csv exists
- Expected rows: 2
- Expected columns: 8
- Data types: Difference (float64), SE (float64), Significant (bool)

*Value Ranges:*
- Early_slope in [-2, 0]
- Late_slope in [-2, 0]
- Difference in [-1, 1] (Early - Late should be small positive for consolidation benefit)
- SE in [0.01, 1.0]
- CI_lower < Difference < CI_upper

*Data Quality:*
- No NaN values
- Both location types present (Source, Destination)

*Log Validation:*
- Required pattern: "Consolidation benefit computed for 2 location types"
- Required pattern: "Source: Difference = [value], CI = [lower, upper]"
- Required pattern: "Destination: Difference = [value], CI = [lower, upper]"
- Forbidden patterns: "ERROR", "NaN in difference estimates"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "NaN in Source consolidation benefit")
- Log failure to logs/step05_test_consolidation_benefit.log
- Quit script immediately
- g_debug invoked to diagnose

---

### Step 6: Test LocationType x Phase Interaction (Primary Hypothesis)

**Purpose:** Test whether consolidation benefit differs between Source and Destination (LocationType x Phase interaction)

**Dependencies:** Step 3 (requires fitted piecewise LMM model for interaction term extraction)

**Complexity:** Low (<1 minute - extract interaction term from model)

**Input:**

**File:** data/step03_piecewise_lmm_model.pkl (fitted model from Step 3)

**Processing:**

1. **Extract 3-way interaction term:**
   - Coefficient: beta_Days_within:Segment:LocationType
   - This term directly tests primary hypothesis: Does LocationType x Phase interaction on slopes differ from zero?

2. **Extract statistics:**
   - Coefficient estimate
   - Standard error
   - z-score
   - p_value (two-tailed test)

3. **Apply Bonferroni correction (Decision D068):**
   - Bonferroni alpha = 0.025 (2 main hypothesis tests: consolidation benefit per location type)
   - Compute p_bonferroni = min(p_uncorrected * 2, 1.0)
   - Report BOTH p_uncorrected and p_bonferroni per Decision D068

4. **Compute effect size (Cohen's f^2):**
   - Compare full model (with interaction) vs reduced model (without interaction)
   - f^2 = (R^2_full - R^2_reduced) / (1 - R^2_full)
   - Thresholds: f^2 > 0.02 (small), > 0.15 (medium), > 0.35 (large)

**Output:**

**File:** data/step06_interaction_tests.csv
**Format:** CSV, 1 row (primary hypothesis test)
**Columns:**
  - `Term` (string, "Days_within:Segment:LocationType")
  - `Estimate` (float, interaction coefficient)
  - `SE` (float, standard error)
  - `z_score` (float, z-statistic)
  - `p_uncorrected` (float, two-tailed p-value, uncorrected)
  - `p_bonferroni` (float, Bonferroni-corrected p-value, alpha=0.025)
  - `Significant_bonferroni` (boolean, True if p_bonferroni < 0.025)
  - `Cohens_f2` (float, effect size)
  - `Effect_interpretation` (string, "negligible", "small", "medium", "large")
**Expected Rows:** 1
**Expected Columns:** 9

**Validation Requirement:**

Validation tools MUST be used after interaction testing. Specific validation tools determined by rq_tools based on Decision D068 dual p-value requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_interaction_tests.csv exists
- Expected rows: 1
- Expected columns: 9
- Data types: p_uncorrected (float64), p_bonferroni (float64), Cohens_f2 (float64)

*Value Ranges:*
- Estimate: reasonable coefficient (-2 to 2 on theta scale)
- SE > 0 (finite, positive)
- z_score: finite
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1]
- p_bonferroni >= p_uncorrected (Bonferroni correction never decreases p-value)
- Cohens_f2 >= 0 (effect sizes non-negative)

*Data Quality:*
- No NaN values
- Dual p-values present (Decision D068 compliance)

*Log Validation:*
- Required pattern: "Interaction term: Days_within:Segment:LocationType"
- Required pattern: "p_uncorrected = [value], p_bonferroni = [value]"
- Required pattern: "Cohen's f^2 = [value] ([interpretation])"
- Required pattern: "VALIDATION - PASS: Dual p-values (Decision D068)"
- Forbidden patterns: "ERROR", "NaN in interaction term", "p_bonferroni < p_uncorrected"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Missing p_bonferroni column")
- Log failure to logs/step06_test_interaction.log
- Quit script immediately
- g_debug invoked to diagnose (check Decision D068 implementation)

---

### Step 7: Prepare Dual-Scale Plot Data

**Purpose:** Create plot source CSVs for theta-scale and probability-scale trajectory plots (Decision D069)

**Dependencies:** Steps 3, 4 (requires fitted model and segment-location slopes)

**Complexity:** Low (<1 minute - data aggregation for plotting)

**Input:**

**File 1:** data/step03_piecewise_lmm_model.pkl (fitted model for predictions)
**File 2:** data/step02_lmm_input_long.csv (observed data for aggregation)
**File 3:** data/step04_segment_location_slopes.csv (slopes for annotation)

**Processing:**

1. **Aggregate observed means per segment-location-timepoint:**
   - Group by: Segment, LocationType, test
   - Compute: mean(theta), SE(theta), 95% CI
   - Expected: 8 rows (2 segments x 2 locations x 2 timepoints per segment)

2. **Generate model predictions:**
   - Use fitted piecewise LMM to predict theta at Days_within = [0, max] within each segment
   - Create smooth trajectory lines (10 points per segment for smooth plotting)

3. **Create theta-scale plot data:**
   - Combine observed means + model predictions
   - Columns: Segment, LocationType, time (TSVR_hours or Days_within), theta, CI_lower, CI_upper, data_type (observed/predicted)

4. **Convert to probability scale (Decision D069):**
   - Apply IRT 2PL transformation: p = 1 / (1 + exp(-theta))
   - Transform theta, CI_lower, CI_upper to probability scale
   - Probability range: [0, 1]

5. **Save dual-scale data:**
   - data/step07_piecewise_theta_data.csv (theta scale)
   - data/step07_piecewise_probability_data.csv (probability scale)

**Output:**

**File 1:** data/step07_piecewise_theta_data.csv
**Format:** CSV, plot source data for theta-scale trajectory
**Columns:**
  - `Segment` (string, "Early" or "Late")
  - `LocationType` (string, "Source" or "Destination")
  - `time` (float, TSVR_hours or Days_within)
  - `theta` (float, mean or predicted theta)
  - `CI_lower` (float, lower 95% confidence bound)
  - `CI_upper` (float, upper 95% confidence bound)
  - `data_type` (string, "observed" or "predicted")
**Expected Rows:** ~60 (8 observed means + ~52 prediction points)
**Note:** This CSV is read by rq_plots later. PNG output goes to plots/ when rq_plots runs.

**File 2:** data/step07_piecewise_probability_data.csv
**Format:** CSV, plot source data for probability-scale trajectory (Decision D069 dual-scale)
**Columns:** Same as theta_data but with probability values (0-1 scale)
**Expected Rows:** ~60 (same as theta data)

**Validation Requirement:**

Validation tools MUST be used after plot data preparation. Specific validation tools determined by rq_tools based on plot data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_piecewise_theta_data.csv exists
- data/step07_piecewise_probability_data.csv exists
- Expected rows: ~60 each (8 observed + ~52 predicted points)
- Expected columns: 7 each

*Value Ranges:*
- Theta scale: theta in [-3, 3], CI_lower in [-3, 3], CI_upper in [-3, 3]
- Probability scale: theta in [0, 1], CI_lower in [0, 1], CI_upper in [0, 1]
- time in [0, 168] hours (or [0, 7] days if converted)
- CI_upper > CI_lower for all rows

*Data Quality:*
- No NaN values tolerated (all cells must have valid values)
- All 2 segments x 2 locations x 2 timepoints = 8 observed means present
- data_type in {"observed", "predicted"}
- Probability transformation correct (0 < p < 1 for all rows)

*Log Validation:*
- Required pattern: "Plot data prepared: ~60 rows theta scale"
- Required pattern: "Plot data prepared: ~60 rows probability scale"
- Required pattern: "All 8 segment-location-timepoint combinations present"
- Required pattern: "Probability transformation: all values in [0, 1]"
- Forbidden patterns: "ERROR", "NaN values detected", "probability > 1 or < 0"
- Acceptable warnings: None expected for plot data preparation

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected ~60 rows, found 45")
- Log failure to logs/step07_prepare_plot_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- g_debug invoked to diagnose root cause

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 -> Step 1:** Wide format preserved, add Segment and Days_within columns
- Input: 400 rows x 7 columns (UID, test, theta_source, theta_destination, se_source, se_destination, TSVR_hours)
- Output: 400 rows x 9 columns (added Segment, Days_within)

**Step 1 -> Step 2:** Wide to long reshape (LocationType factor)
- Input: 400 rows x 9 columns (wide format, 2 theta columns)
- Output: 800 rows x 8 columns (long format, 1 theta column, LocationType factor)
- Transformation: "Melt" theta_source/theta_destination into single theta column

**Step 2 -> Step 3:** Long format used for LMM fitting
- Input: 800 rows (LMM input)
- Output: Fitted model object + summary

**Step 3 -> Step 4:** Extract slopes from model
- Input: Fitted model coefficients + variance-covariance matrix
- Output: 4 rows (segment-location slopes with SE and CI)

**Step 4 -> Step 5:** Compute consolidation benefit
- Input: 4 slopes (Source_Early, Source_Late, Destination_Early, Destination_Late)
- Output: 2 rows (Source consolidation benefit, Destination consolidation benefit)

**Step 3 -> Step 6:** Extract interaction term from model
- Input: Fitted model coefficients
- Output: 1 row (interaction test with dual p-values)

**Steps 3,4 -> Step 7:** Aggregate for plotting
- Input: Fitted model + observed data + slopes
- Output: ~60 rows per scale (observed means + model predictions)

### Column Naming Conventions

**Identifier columns:**
- `UID` - Participant unique identifier (format: P### with leading zeros)
- `test` - Test session (T1, T2, T3, T4)
- `composite_ID` - NOT used in this RQ (no IRT here, but may appear in RQ 5.5.1 dependency)

**Time variables (Decision D070):**
- `TSVR_hours` - Time Since VR in hours (actual elapsed time, range: [0, 168])
- `Segment` - Piecewise segment factor ("Early": 0-48h, "Late": 48-144h)
- `Days_within` - Recentered time within each segment (range: [0, 5] days)

**IRT outputs (from RQ 5.5.1):**
- `theta_source` - IRT ability estimate for -U- pick-up locations
- `theta_destination` - IRT ability estimate for -D- put-down locations
- `se_source` - Standard error for theta_source
- `se_destination` - Standard error for theta_destination
- `theta` - Generic theta column in long format (combines theta_source and theta_destination)
- `se` - Generic SE column in long format

**LMM/plotting columns:**
- `LocationType` - Memory location type factor ("Source", "Destination")
- `slope` - Forgetting rate (theta units per day)
- `CI_lower` - Lower 95% confidence bound
- `CI_upper` - Upper 95% confidence bound
- `p_uncorrected` - Uncorrected p-value (Decision D068)
- `p_bonferroni` - Bonferroni-corrected p-value (Decision D068)
- `Cohens_f2` - Effect size for interaction test

### Data Type Constraints

**Categorical variables:**
- `UID`: string (object)
- `test`: string (object), values: {T1, T2, T3, T4}
- `Segment`: string (object), values: {Early, Late}
- `LocationType`: string (object), values: {Source, Destination}
- `data_type`: string (object), values: {observed, predicted}

**Numeric variables:**
- `theta`, `theta_source`, `theta_destination`: float64, range: [-3, 3]
- `se`, `se_source`, `se_destination`: float64, range: [0.1, 1.0]
- `TSVR_hours`: float64, range: [0, 168]
- `Days_within`: float64, range: [0, 5]
- `slope`: float64, range: [-2, 0] (negative = forgetting)
- `CI_lower`, `CI_upper`: float64
- `p_uncorrected`, `p_bonferroni`: float64, range: [0, 1]
- `Cohens_f2`: float64, range: [0, inf)

**Boolean variables:**
- `Significant`, `Significant_bonferroni`: bool

---

## Cross-RQ Dependencies

**Dependency Type 2: DERIVED Data from Other RQs (Dependencies Exist)**

**This RQ requires outputs from:**
- **RQ 5.5.1** (Source-Destination Trajectories - ROOT)
  - File 1: results/ch5/5.5.1/data/step03_theta_scores.csv
  - Used in: Step 0 (load IRT theta scores by location type)
  - Rationale: RQ 5.5.1 establishes source vs destination IRT ability estimates via 2-factor GRM. This RQ uses those theta scores to test consolidation dynamics.

  - File 2: results/ch5/5.5.1/data/step00_tsvr_mapping.csv
  - Used in: Step 0 (load TSVR time variable)
  - Rationale: Decision D070 requires TSVR_hours (actual hours since encoding) for accurate temporal modeling. RQ 5.5.1 extracts this from master.xlsx.

**Execution Order Constraint:**
1. RQ 5.5.1 must complete first (provides theta_scores.csv and tsvr_mapping.csv)
2. This RQ executes second (uses RQ 5.5.1 outputs for piecewise LMM)

**Data Source Boundaries (Per Specification 5.1.6):**
- **RAW data:** None (all data derived from RQ 5.5.1)
- **DERIVED data:** Outputs from RQ 5.5.1 (theta scores, TSVR mapping)
- **Scope:** This RQ does NOT re-calibrate IRT models (uses RQ 5.5.1 theta as fixed measurements)

**Validation:**
- Step 0: Check results/ch5/5.5.1/status.yaml exists and rq_results.status = "success"
- Step 0: Check results/ch5/5.5.1/data/step03_theta_scores.csv exists (400 rows expected)
- Step 0: Check results/ch5/5.5.1/data/step00_tsvr_mapping.csv exists (400 rows expected)
- If ANY file missing OR RQ 5.5.1 incomplete -> quit with EXPECTATIONS ERROR -> user must execute RQ 5.5.1 first

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

#### Step 0: Load Dependency Data from RQ 5.5.1

**Analysis Tool:** (determined by rq_tools - likely tools.data.load_rq_dependency)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_data_format + validate_dependency_completion)

**What Validation Checks (TECHNICAL - rq_inspect scope):**
- RQ 5.5.1 status.yaml: rq_results.status = "success" (dependency complete)
- Theta file exists: results/ch5/5.5.1/data/step03_theta_scores.csv
- TSVR file exists: results/ch5/5.5.1/data/step00_tsvr_mapping.csv
- Merged output: 400 rows, 7 columns, no NaN in TSVR_hours
- Value ranges: theta in [-3, 3], se in [0.1, 1.0], TSVR in [0, 168]

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "RQ 5.5.1 incomplete: status = pending")
- Log failure to logs/step00_load_dependency_data.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked by master to diagnose root cause

---

#### Step 1: Create Piecewise Time Variables

**Analysis Tool:** (determined by rq_tools - likely tools.lmm.assign_piecewise_segments)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_data_format + validate_segment_assignment)

**What Validation Checks:**
- Output file exists: data/step01_piecewise_time_variables.csv
- Expected row count: 400
- Expected column count: 9 (original 7 + Segment + Days_within)
- Segment values: {"Early", "Late"} (exactly 2 unique values)
- Days_within range: [0, 5] (no negatives)
- Segment distribution: ~200 Early, ~200 Late

**Expected Behavior on Validation Failure:**
- Raise error (e.g., "Segment assignment failed: 150 Early, 250 Late")
- Log failure to logs/step01_create_piecewise_time_variables.log
- Quit script immediately
- g_debug invoked

---

#### Step 2: Reshape Wide to Long Format

**Analysis Tool:** (determined by rq_tools - likely pandas.melt or custom reshape function)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure)

**What Validation Checks:**
- Output file exists: data/step02_lmm_input_long.csv
- Expected row count: 800 (2x input rows)
- Expected column count: 8
- LocationType distribution: 400 Source, 400 Destination
- Each UID x test appears exactly 2 times
- No NaN values in any column

**Expected Behavior on Validation Failure:**
- Raise error (e.g., "Expected 800 rows, found 798")
- Log failure to logs/step02_reshape_wide_to_long.log
- Quit script immediately
- g_debug invoked

---

#### Step 3: Fit Piecewise LMM

**Analysis Tool:** (determined by rq_tools - likely tools.lmm.fit_lmm_trajectory_tsvr with piecewise formula)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_lmm_convergence + validate_lmm_assumptions_comprehensive)

**What Validation Checks:**
- Model converged: model.converged = True
- Fixed effects: 8 terms present (intercept + 7 interactions)
- Random effects: var_intercept > 0, var_slope > 0
- No singular fit warnings
- 800 observations used (no exclusions)
- 100 random effect groups (one per UID)

**Expected Behavior on Validation Failure:**
- Raise error (e.g., "Model did not converge after 100 iterations")
- Log failure to logs/step03_fit_piecewise_lmm.log
- Quit script immediately
- g_debug invoked (common causes: insufficient data, random effects too complex)

---

#### Step 4: Extract Segment-Location Slopes

**Analysis Tool:** (determined by rq_tools - likely tools.lmm.extract_segment_slopes_from_lmm)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure + validate_numeric_range)

**What Validation Checks:**
- Output file exists: data/step04_segment_location_slopes.csv
- Expected row count: 4
- Expected column count: 7
- All slopes have valid SE (finite, positive)
- CI_lower < slope < CI_upper for all rows
- p_value in [0, 1]

**Expected Behavior on Validation Failure:**
- Raise error (e.g., "NaN slope for Destination_Late")
- Log failure to logs/step04_extract_segment_location_slopes.log
- Quit script immediately
- g_debug invoked

---

#### Step 5: Test Consolidation Benefit Per Location Type

**Analysis Tool:** (determined by rq_tools - likely custom consolidation_benefit_test function)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure)

**What Validation Checks:**
- Output file exists: data/step05_consolidation_benefit.csv
- Expected row count: 2 (Source, Destination)
- Expected column count: 8
- All differences have valid SE
- CI_lower < Difference < CI_upper

**Expected Behavior on Validation Failure:**
- Raise error (e.g., "NaN in Source consolidation benefit")
- Log failure to logs/step05_test_consolidation_benefit.log
- Quit script immediately
- g_debug invoked

---

#### Step 6: Test LocationType x Phase Interaction

**Analysis Tool:** (determined by rq_tools - likely extract interaction term from fitted model)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_hypothesis_test_dual_pvalues per D068)

**What Validation Checks:**
- Output file exists: data/step06_interaction_tests.csv
- Expected row count: 1
- Expected column count: 9
- Dual p-values present: p_uncorrected AND p_bonferroni (Decision D068 compliance)
- p_bonferroni >= p_uncorrected (Bonferroni correction never decreases p)
- Cohens_f2 >= 0

**Expected Behavior on Validation Failure:**
- Raise error (e.g., "Missing p_bonferroni column - Decision D068 violation")
- Log failure to logs/step06_test_interaction.log
- Quit script immediately
- g_debug invoked

---

#### Step 7: Prepare Dual-Scale Plot Data

**Analysis Tool:** (determined by rq_tools - likely tools.plotting.prepare_piecewise_plot_data + convert_theta_to_probability)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_plot_data_completeness + validate_probability_range)

**What Validation Checks:**
- Output files exist: data/step07_piecewise_theta_data.csv, data/step07_piecewise_probability_data.csv
- Expected row count: ~60 each
- Expected column count: 7 each
- Theta scale: theta in [-3, 3]
- Probability scale: all values in [0, 1] (no NaN, no out-of-range)
- All 8 segment-location-timepoint combinations present
- CI_upper > CI_lower for all rows

**Expected Behavior on Validation Failure:**
- Raise error (e.g., "Probability > 1 detected in row 23")
- Log failure to logs/step07_prepare_plot_data.log
- Quit script immediately
- g_debug invoked

---

## Summary

**Total Steps:** 8 (Step 0 through Step 7)

**Estimated Runtime:** Low to Medium (5-20 minutes total)
- Step 0: <1 min (data loading)
- Step 1: <1 min (time variable creation)
- Step 2: <1 min (reshape)
- Step 3: 5-10 min (LMM fitting)
- Step 4: <1 min (slope extraction)
- Step 5: <1 min (consolidation benefit)
- Step 6: <1 min (interaction test)
- Step 7: <1 min (plot data prep)

**Cross-RQ Dependencies:** RQ 5.5.1 (Source-Destination Trajectories ROOT)

**Primary Outputs:**
- data/step03_piecewise_lmm_model.pkl (fitted piecewise LMM)
- data/step04_segment_location_slopes.csv (4 segment-location slopes)
- data/step05_consolidation_benefit.csv (consolidation benefit per location type)
- data/step06_interaction_tests.csv (LocationType x Phase interaction with dual p-values)
- data/step07_piecewise_theta_data.csv (theta-scale plot data)
- data/step07_piecewise_probability_data.csv (probability-scale plot data)

**Validation Coverage:** 100% (all 8 steps have validation requirements, substance criteria specified)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate - workflow architecture)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts
5. Workflow continues to Step 14: bash executes scripts -> rq_inspect validates outputs

---

**Version History:**
- v1.0 (2025-12-04): Initial plan created by rq_planner agent for RQ 5.5.2
