# Analysis Plan for RQ 5.8: Evidence for Two-Phase Forgetting (Rapid then Slow)

**Created by:** rq_planner agent
**Date:** 2025-11-26
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This RQ tests whether episodic memory forgetting exhibits a two-phase pattern: rapid initial decline (Day 0-1, pre-consolidation) followed by slower decay (Day 1-6, post-consolidation). The analysis uses IRT-derived theta scores from RQ 5.7 (collapsed across What/Where/When domains) as the outcome variable.

**Theoretical Rationale:**
Consolidation theory predicts memory traces undergo time-dependent stabilization during the first ~24 hours post-encoding. During this vulnerable period, forgetting is rapid. After consolidation, traces stabilize and forgetting decelerates. The inflection point should occur around Day 1 (after one night's sleep). This RQ uses three convergent tests to triangulate evidence for two-phase forgetting.

**Three Convergent Tests:**
1. **Quadratic Term Significance:** Fit Theta ~ Time + Time² + (Time | UID), test if Time² coefficient is positive and significant (p < 0.0033 Bonferroni-corrected)
2. **Piecewise vs Continuous Model Comparison:** Fit Theta ~ Days_within x Segment + (Days_within | UID), compare AIC to best continuous model from RQ 5.7 (”AIC < -2 favors piecewise)
3. **Early vs Late Slope Ratio:** Extract slopes for Early segment (0-48 hours) and Late segment (48-240 hours), compute Late/Early ratio (expect < 0.5 if two-phase robust)

**Analysis Approach:**
This is an LMM-only analysis using DERIVED data from RQ 5.7. No IRT calibration is performed - theta scores and TSVR mapping are loaded directly from RQ 5.7 outputs. The analysis focuses on testing whether forgetting trajectory shows inflection at theoretically meaningful breakpoint (48 hours TSVR = Day 1 after one night's sleep).

**Total Steps:** 7 steps (Step 0: Get Data, Steps 1-6: Analysis + Visualization)
**Estimated Runtime:** Medium (30-60 minutes total - LMM fitting with random slopes + comprehensive assumption validation)
**Cross-RQ Dependencies:** RQ 5.7 must complete successfully (provides theta scores, TSVR mapping, best continuous model)
**Primary Outputs:** Quadratic model summary, piecewise model summary, assumption validation report, slope comparison, plot source CSV for visualization

**Key Decisions Applied:**
- Decision D070: TSVR as time variable (inherited from RQ 5.7 - actual hours, not nominal days)
- Decision D069: Dual-scale trajectory plots (NOT APPLICABLE - this RQ creates plot data preparation CSV, but does not generate dual-scale plots; visualization handled by rq_plots agent)

**Convergence Fallback Strategy:**
Both quadratic and piecewise models attempt maximal random slopes structure (Time | UID, Days_within | UID). With N=100 participants, complex random structures may not converge (Bates et al., 2015 recommend N>=200). Fallback hierarchy: (1) attempt maximal model, (2) if fails, simplify to uncorrelated slopes (Time || UID), (3) if still fails, random intercepts only (1 | UID). Convergence decisions documented transparently in validation reports.

---

## Cross-RQ Dependencies

**Dependency Type:** DERIVED Data from Other RQs (Dependencies Exist)

**This RQ requires outputs from:**
- **RQ 5.7** (Forgetting trajectory functional forms)
  - File: results/ch5/rq7/data/step02_theta_long.csv
  - Used in: Step 0 (load theta scores as outcome variable)
  - Rationale: RQ 5.7 calibrates IRT model, extracts theta scores, and merges with TSVR. This RQ uses those theta scores to test two-phase hypothesis.

  - File: results/ch5/rq7/data/step00_tsvr_mapping.csv
  - Used in: Step 0 (load time variable for piecewise segmentation)
  - Rationale: TSVR (actual hours since encoding per Decision D070) is required to define Early (0-48h) and Late (48-240h) segments.

  - File: results/ch5/rq7/data/step03_best_model.pkl
  - Used in: Step 3 (load best continuous model for AIC comparison)
  - Rationale: RQ 5.7 fits 5 candidate continuous models (Linear, Quadratic, Log, Lin+Log, Quad+Log) and selects best by AIC. This RQ compares piecewise model AIC to that best continuous model to test if piecewise improves fit.

**Execution Order Constraint:**
1. RQ 5.7 must complete all steps (IRT calibration, purification, theta extraction, TSVR merge, LMM trajectory modeling, best model selection)
2. This RQ (RQ 5.8) executes after RQ 5.7 completes (uses Step 0, Step 2, Step 3 outputs from RQ 5.7)

**Data Source Boundaries:**
- **RAW data:** None - this RQ uses only DERIVED data from RQ 5.7
- **DERIVED data:** Theta scores, TSVR mapping, best continuous model (all from RQ 5.7)
- **Scope:** This RQ does NOT re-calibrate IRT models, does NOT re-fit continuous models. It accepts RQ 5.7 outputs as given and tests two-phase hypothesis using those outputs.

**Validation:**
- Step 0: Check results/ch5/rq7/data/step02_theta_long.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch5/rq7/data/step00_tsvr_mapping.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch5/rq7/data/step03_best_model.pkl exists (circuit breaker: EXPECTATIONS ERROR if absent)
- If ANY file missing -> quit with error -> user must execute RQ 5.7 first

---

## Analysis Plan

### Step 0: Get Data

**Purpose:** Load theta scores, TSVR mapping, and best continuous model from RQ 5.7 outputs

**Dependencies:** None (first step, but requires RQ 5.7 completion)

**Complexity:** Low (data loading only, <5 minutes)

**Input:**

**File 1:** results/ch5/rq7/data/step02_theta_long.csv
**Source:** Generated by RQ 5.7 Step 2 (theta extraction after Pass 2 IRT calibration)
**Format:** CSV, long format (one row per participant-test-domain combination)
**Columns:**
  - `UID` (string, participant identifier, format: P### with leading zeros)
  - `test` (string, test session identifier: T1, T2, T3, T4)
  - `domain` (string, memory domain: What, Where, When)
  - `theta` (float, IRT ability estimate for given domain)
**Expected Rows:** ~1200 rows (100 participants x 4 tests x 3 domains)
**Note:** This RQ collapses across domains (uses aggregate theta), but domain column retained for potential post-hoc domain-specific analyses

**File 2:** results/ch5/rq7/data/step00_tsvr_mapping.csv
**Source:** Generated by RQ 5.7 Step 0 (TSVR extraction from master.xlsx)
**Format:** CSV, one row per participant-test combination
**Columns:**
  - `UID` (string, participant identifier)
  - `test` (string, test session identifier)
  - `TSVR_hours` (float, actual time since VR encoding in hours, Decision D070)
**Expected Rows:** ~400 rows (100 participants x 4 tests)

**File 3:** results/ch5/rq7/data/step03_best_model.pkl
**Source:** Generated by RQ 5.7 Step 3 (best continuous model selection by AIC)
**Format:** Pickled Python object (statsmodels MixedLM fitted model)
**Contents:** Fitted LMM object with AIC, fixed effects, random effects
**Note:** Used for AIC comparison in Step 3 (piecewise vs continuous)

**Processing:**

1. **Load theta scores:**
   - Read results/ch5/rq7/data/step02_theta_long.csv
   - Verify columns present: UID, test, domain, theta
   - Verify no NaN in theta (IRT calibration should produce theta for all participants)

2. **Load TSVR mapping:**
   - Read results/ch5/rq7/data/step00_tsvr_mapping.csv
   - Verify columns present: UID, test, TSVR_hours
   - Verify no NaN in TSVR_hours (all participants have actual time data)

3. **Merge theta with TSVR:**
   - Merge on (UID, test) keys
   - Expected merge: All theta rows should match TSVR rows (left join should have 0 missing)
   - Resulting columns: UID, test, domain, theta, TSVR_hours

4. **Collapse across domains:**
   - Group by (UID, test, TSVR_hours), compute mean(theta) across 3 domains
   - Rationale: This RQ tests general two-phase pattern, not domain-specific
   - Resulting columns: UID, test, TSVR_hours, theta_mean
   - Expected rows after collapse: ~400 rows (100 participants x 4 tests)

5. **Load best continuous model:**
   - Read results/ch5/rq7/data/step03_best_model.pkl using pickle.load()
   - Extract AIC value for Step 3 comparison
   - Store AIC in metadata for later use

**Output:**

**File 1:** data/step00_theta_tsvr.csv
**Format:** CSV, long format (one row per participant-test combination)
**Columns:**
  - `UID` (string, participant identifier)
  - `test` (string, test session identifier)
  - `TSVR_hours` (float, time since VR encoding in hours)
  - `theta` (float, mean theta across 3 domains)
**Expected Rows:** ~400 rows (100 participants x 4 tests)

**File 2:** data/step00_best_continuous_aic.txt
**Format:** Plain text file with single AIC value
**Contents:** AIC of best continuous model from RQ 5.7 (for Step 3 comparison)
**Example:** "12345.67"

**Validation Requirement:**
Validation tools MUST be used after data loading execution. Specific validation tools will be determined by rq_tools based on data loading requirements (file existence validation, merge validation, schema validation). The rq_analysis agent will embed validation tool calls after the data loading tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_theta_tsvr.csv exists (exact path)
- Expected rows: 380-400 (100 participants x 4 tests, some missing data acceptable)
- Expected columns: 4 (UID, test, TSVR_hours, theta)
- Data types: UID (string), test (string), TSVR_hours (float64), theta (float64)
- data/step00_best_continuous_aic.txt exists (exact path)

*Value Ranges:*
- TSVR_hours in [0, 240] hours (0 = encoding, 240 = 10 days maximum retention)
- theta in [-3, 3] (typical IRT ability range, domain-collapsed)
- test in {T1, T2, T3, T4} (categorical, 4 levels)
- AIC > 0 (AIC must be positive, typical range 10000-20000 for this dataset)

*Data Quality:*
- No NaN in theta column (IRT produces theta for all participants)
- No NaN in TSVR_hours column (all participants have time data)
- Expected N: 380-400 rows (some missing tests acceptable, but >95% retention expected)
- No duplicate (UID, test) combinations (each participant-test unique)
- Distribution check: TSVR_hours should have 4 clusters (T1~0h, T2~24h, T3~72h, T4~144h)

*Log Validation:*
- Required pattern: "Loaded theta scores: 1200 rows from RQ 5.7"
- Required pattern: "Loaded TSVR mapping: 400 rows from RQ 5.7"
- Required pattern: "Merged theta with TSVR: 1200 rows matched"
- Required pattern: "Collapsed across domains: 400 rows (mean theta computed)"
- Required pattern: "Loaded best continuous model AIC: [value]"
- Forbidden patterns: "ERROR", "TSVR merge failed", "NaN values detected"
- Acceptable warnings: "Missing data for participant [UID] test [test]" (if <5% missing)

**Expected Behavior on Validation Failure:**
- If ANY RQ 5.7 file missing -> QUIT with EXPECTATIONS ERROR: "RQ 5.7 must complete before RQ 5.8"
- If merge fails (TSVR rows don't match theta rows) -> QUIT with error, log details, invoke g_debug
- If NaN detected in critical columns -> QUIT with error, list affected rows
- If row count <380 (>5% data loss) -> QUIT with error, investigate data quality issue

---

### Step 1: Create Time Transformations

**Purpose:** Create time transformations for quadratic model (TSVR, TSVR²) and piecewise model (Early/Late segments, Days_within)

**Dependencies:** Step 0 (requires merged theta + TSVR data)

**Complexity:** Low (data transformations only, <5 minutes)

**Input:**

**File:** data/step00_theta_tsvr.csv
**Source:** Generated by Step 0 (merged theta + TSVR from RQ 5.7)
**Format:** CSV, long format
**Columns:** UID, test, TSVR_hours, theta
**Expected Rows:** ~400 rows (100 participants x 4 tests)

**Processing:**

1. **Create quadratic time variables:**
   - `Time` = TSVR_hours (continuous time variable)
   - `Time_squared` = TSVR_hours²

2. **Create log time variable:**
   - `Time_log` = log(TSVR_hours + 1)
   - Add 1 to avoid log(0) at encoding (TSVR_hours = 0)

3. **Create piecewise segments (inflection at 48 hours):**
   - `Segment` = "Early" if TSVR_hours <= 48, else "Late"
   - Early segment: 0-48 hours (Day 0-1, pre-consolidation)
   - Late segment: 48-240 hours (Day 1-6, post-consolidation)
   - Theoretical rationale: 48 hours = Day 1 after one night's sleep (consolidation window)

4. **Create Days_within variable:**
   - `Days_within` = time recentered within each segment
   - Early segment: Days_within = TSVR_hours (starts at 0)
   - Late segment: Days_within = TSVR_hours - 48 (starts at 0, 48 hours after encoding)
   - Rationale: Allows separate slope estimation per segment with 0 = segment start

**Output:**

**File:** data/step01_time_transformed.csv
**Format:** CSV, long format (one row per participant-test combination)
**Columns:**
  - `UID` (string, participant identifier)
  - `test` (string, test session identifier)
  - `TSVR_hours` (float, original time variable)
  - `theta` (float, outcome variable)
  - `Time` (float, copy of TSVR_hours for quadratic model)
  - `Time_squared` (float, TSVR_hours² for quadratic term)
  - `Time_log` (float, log(TSVR_hours + 1) for potential log model)
  - `Segment` (string, "Early" or "Late" based on 48-hour inflection)
  - `Days_within` (float, time recentered within segment)
**Expected Rows:** ~400 rows (same as input)

**Validation Requirement:**
Validation tools MUST be used after time transformation execution. Specific validation tools will be determined by rq_tools based on data transformation requirements (column creation validation, value range validation). The rq_analysis agent will embed validation tool calls after the transformation tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_time_transformed.csv exists (exact path)
- Expected rows: 380-400 (same as Step 0 output)
- Expected columns: 9 (UID, test, TSVR_hours, theta, Time, Time_squared, Time_log, Segment, Days_within)
- Data types: UID (string), test (string), TSVR_hours (float64), theta (float64), Time (float64), Time_squared (float64), Time_log (float64), Segment (string), Days_within (float64)

*Value Ranges:*
- Time = TSVR_hours (identical values)
- Time_squared in [0, 57600] (max = 240² hours)
- Time_log in [0, 5.5] (log(0+1)=0, log(240+1)~5.48)
- Segment in {"Early", "Late"} (categorical, 2 levels)
- Days_within in [0, 192] (Early: 0-48, Late: 0-192 recentered)

*Data Quality:*
- No NaN in any column (all transformations deterministic)
- Row count matches Step 0 output (no data loss during transformation)
- Distribution check: Segment should have ~50% Early, ~50% Late (2 tests per segment)
- Days_within starts at 0 for both segments (recentering correct)

*Log Validation:*
- Required pattern: "Created quadratic time variables: Time, Time_squared"
- Required pattern: "Created log time variable: Time_log"
- Required pattern: "Assigned piecewise segments: Early (0-48h), Late (48-240h)"
- Required pattern: "Created Days_within: recentered time per segment"
- Forbidden patterns: "ERROR", "NaN created", "Invalid segment assignment"
- Acceptable warnings: None expected for deterministic transformations

**Expected Behavior on Validation Failure:**
- If NaN created -> QUIT with error, log which transformation failed
- If Segment assignment incorrect (all Early or all Late) -> QUIT with error, investigate inflection point logic
- If Days_within negative values -> QUIT with error, recentering failed

---

### Step 2: Fit Quadratic Model (Test 1 - Quadratic Term Significance)

**Purpose:** Fit Theta ~ Time + Time² + (Time | UID), test if Time² coefficient is positive and significant (p < 0.0033 Bonferroni-corrected)

**Dependencies:** Step 1 (requires time-transformed data)

**Complexity:** Medium (LMM fitting with random slopes, 10-20 minutes)

**Input:**

**File:** data/step01_time_transformed.csv
**Source:** Generated by Step 1 (time transformations applied)
**Format:** CSV, long format
**Columns:** UID, test, TSVR_hours, theta, Time, Time_squared, Time_log, Segment, Days_within
**Expected Rows:** ~400 rows

**Processing:**

1. **Attempt maximal random slopes model:**
   - Formula: `theta ~ Time + Time_squared + (Time | UID)`
   - Fixed effects: Intercept, Time (linear term), Time_squared (quadratic term)
   - Random effects: Random intercept + random slope for Time per participant
   - Random structure: Correlated (allows intercept-slope correlation)

2. **Convergence fallback strategy:**
   - If maximal model fails to converge (checked via validate_lmm_convergence):
     - **Fallback 1:** Simplify to uncorrelated random slopes: `(Time || UID)`
     - Removes intercept-slope correlation parameter (reduces complexity)
   - If still fails:
     - **Fallback 2:** Random intercepts only: `(1 | UID)`
     - No random slopes (population-average trajectory only)
   - Document convergence decisions in model summary

3. **Extract fixed effects:**
   - Intercept coefficient, SE, z-value, p-value
   - Time coefficient (linear term), SE, z-value, p-value
   - Time_squared coefficient (quadratic term), SE, z-value, p-value

4. **Test quadratic term significance:**
   - Bonferroni-corrected threshold: ± = 0.05 / 15 = 0.0033 (15 RQs in Chapter 5)
   - If Time_squared p-value < 0.0033 AND coefficient > 0: Evidence for deceleration (two-phase)
   - If Time_squared p-value >= 0.0033 OR coefficient <= 0: No evidence for deceleration

5. **Generate model predictions:**
   - Create prediction grid: Time = [0, 24, 48, 72, 96, 120, 144, 168, 192, 216, 240] hours
   - Compute predicted theta for each timepoint using fixed effects
   - Compute 95% confidence intervals using fixed effects SE

**Output:**

**File 1:** results/step02_quadratic_model_summary.txt
**Format:** Plain text file
**Contents:**
  - Model formula (including random structure used)
  - Convergence status (maximal / fallback1 / fallback2)
  - Fixed effects table (coefficient, SE, z, p for Intercept, Time, Time_squared)
  - Random effects variance components
  - AIC, BIC, log-likelihood
  - Interpretation: Time_squared significance test result (p < 0.0033 or not)

**File 2:** data/step02_quadratic_predictions.csv
**Format:** CSV with predicted values
**Columns:**
  - `Time` (float, prediction grid: 0, 24, 48, ..., 240 hours)
  - `predicted_theta` (float, predicted theta from quadratic model)
  - `CI_lower` (float, lower 95% confidence bound)
  - `CI_upper` (float, upper 95% confidence bound)
**Expected Rows:** 11 rows (11 timepoints in prediction grid)

**Validation Requirement:**
Validation tools MUST be used after LMM fitting execution. Specific validation tools will be determined by rq_tools based on LMM fitting requirements (convergence validation, parameter bounds validation). The rq_analysis agent will embed validation tool calls after the LMM fitting tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step02_quadratic_model_summary.txt exists (exact path)
- data/step02_quadratic_predictions.csv exists (exact path)
- Expected rows (predictions): 11 (one per timepoint in grid)
- Expected columns (predictions): 4 (Time, predicted_theta, CI_lower, CI_upper)
- Data types (predictions): float64 for all columns

*Value Ranges:*
- predicted_theta in [-3, 3] (IRT ability scale)
- CI_lower in [-4, 2] (confidence bounds can extend slightly beyond theta range)
- CI_upper in [-2, 4] (confidence bounds can extend slightly beyond theta range)
- CI_upper > CI_lower for all rows (confidence interval valid)
- Time in [0, 240] (prediction grid range)

*Data Quality:*
- No NaN in fixed effects table (model must produce estimates for all parameters)
- No NaN in predictions (model must produce predictions for all timepoints)
- AIC > 0 (typical range 10000-20000 for this dataset)
- Convergence status documented (maximal / fallback1 / fallback2)
- Time_squared p-value in [0, 1] (valid p-value)

*Log Validation:*
- Required pattern: "Fitting quadratic model: theta ~ Time + Time_squared + (Time | UID)"
- Required pattern: "Model converged: True" OR "Convergence failed, using fallback: [fallback type]"
- Required pattern: "Time_squared coefficient: [value], p-value: [value]"
- Required pattern: "Bonferroni threshold (15 tests): 0.0033"
- Required pattern: "Test 1 result: [PASS/FAIL] - quadratic term [significant/not significant]"
- Forbidden patterns: "ERROR", "Model did not converge and no fallback succeeded"
- Acceptable warnings: "Convergence not achieved, simplifying to uncorrelated random slopes" (documented fallback)

**Expected Behavior on Validation Failure:**
- If all convergence attempts fail -> QUIT with error, log details, invoke g_debug
- If fixed effects contain NaN -> QUIT with error, model estimation failed
- If predictions contain NaN -> QUIT with error, prediction failed

---

### Step 3: Fit Piecewise Model (Test 2 - Piecewise vs Continuous Comparison)

**Purpose:** Fit Theta ~ Days_within x Segment + (Days_within | UID), compare AIC to best continuous model from RQ 5.7 (”AIC < -2 favors piecewise)

**Dependencies:** Step 1 (requires piecewise structure), Step 0 (requires best continuous AIC for comparison)

**Complexity:** Medium (LMM fitting with random slopes + AIC comparison, 10-20 minutes)

**Input:**

**File 1:** data/step01_time_transformed.csv
**Source:** Generated by Step 1
**Format:** CSV, long format
**Columns:** UID, test, TSVR_hours, theta, Time, Time_squared, Time_log, Segment, Days_within
**Expected Rows:** ~400 rows

**File 2:** data/step00_best_continuous_aic.txt
**Source:** Generated by Step 0 (AIC of best continuous model from RQ 5.7)
**Format:** Plain text with single AIC value

**Processing:**

1. **Attempt maximal random slopes model:**
   - Formula: `theta ~ Days_within * Segment + (Days_within | UID)`
   - Fixed effects: Intercept, Days_within (main effect), Segment (Early/Late factor), Days_within x Segment (interaction)
   - Random effects: Random intercept + random slope for Days_within per participant
   - Random structure: Correlated (allows intercept-slope correlation)
   - Interaction term: Tests if slope differs between Early and Late segments

2. **Convergence fallback strategy:**
   - Same as Step 2 (maximal -> uncorrelated -> intercepts only)
   - Document convergence decisions in model summary

3. **Extract fixed effects:**
   - Intercept coefficient (Early segment intercept at Days_within=0)
   - Days_within coefficient (Early segment slope)
   - SegmentLate coefficient (Late segment intercept shift)
   - Days_within:SegmentLate coefficient (Late segment slope difference)
   - Test interaction significance with Bonferroni threshold (p < 0.0033)

4. **Compute segment slopes:**
   - Early segment slope = Days_within coefficient
   - Late segment slope = Days_within coefficient + Days_within:SegmentLate coefficient
   - Both slopes expected to be negative (forgetting = theta decline)

5. **Compare AIC to best continuous model:**
   - Load AIC from data/step00_best_continuous_aic.txt
   - Compute ”AIC = AIC_piecewise - AIC_continuous
   - Decision rule:
     - ”AIC < -2: Piecewise superior (evidence for two-phase)
     - ”AIC > +2: Continuous superior (no two-phase)
     - |”AIC| < 2: Models equivalent (inconclusive)

6. **Generate model predictions:**
   - Create prediction grid for Early segment: Days_within = [0, 6, 12, 18, 24, 30, 36, 42, 48] hours
   - Create prediction grid for Late segment: Days_within = [0, 24, 48, 72, 96, 120, 144, 168, 192] hours
   - Compute predicted theta for each segment x timepoint
   - Compute 95% confidence intervals

**Output:**

**File 1:** results/step03_piecewise_model_summary.txt
**Format:** Plain text file
**Contents:**
  - Model formula (including random structure used)
  - Convergence status (maximal / fallback1 / fallback2)
  - Fixed effects table (coefficient, SE, z, p for Intercept, Days_within, SegmentLate, interaction)
  - Random effects variance components
  - AIC, BIC, log-likelihood
  - AIC comparison: AIC_piecewise, AIC_continuous (from RQ 5.7), ”AIC, interpretation
  - Segment slopes: Early slope, Late slope
  - Interaction significance test result (p < 0.0033 or not)

**File 2:** data/step03_piecewise_predictions.csv
**Format:** CSV with predicted values per segment
**Columns:**
  - `Segment` (string, "Early" or "Late")
  - `Days_within` (float, time within segment)
  - `TSVR_hours` (float, actual time since encoding, for plotting)
  - `predicted_theta` (float, predicted theta from piecewise model)
  - `CI_lower` (float, lower 95% confidence bound)
  - `CI_upper` (float, upper 95% confidence bound)
**Expected Rows:** 18 rows (9 Early + 9 Late timepoints)

**Validation Requirement:**
Validation tools MUST be used after piecewise model fitting execution. Specific validation tools will be determined by rq_tools based on LMM fitting requirements (convergence validation, interaction term validation, AIC comparison validation). The rq_analysis agent will embed validation tool calls after the piecewise fitting tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step03_piecewise_model_summary.txt exists (exact path)
- data/step03_piecewise_predictions.csv exists (exact path)
- Expected rows (predictions): 18 (9 Early + 9 Late)
- Expected columns (predictions): 6 (Segment, Days_within, TSVR_hours, predicted_theta, CI_lower, CI_upper)
- Data types (predictions): Segment (string), Days_within (float64), TSVR_hours (float64), predicted_theta (float64), CI_lower (float64), CI_upper (float64)

*Value Ranges:*
- predicted_theta in [-3, 3] (IRT ability scale)
- CI_lower in [-4, 2] (confidence bounds)
- CI_upper in [-2, 4] (confidence bounds)
- CI_upper > CI_lower for all rows
- Segment in {"Early", "Late"}
- Days_within in [0, 192] (Early: 0-48, Late: 0-192)
- TSVR_hours in [0, 240]
- ”AIC in [-1000, 1000] (plausible AIC difference range)

*Data Quality:*
- No NaN in fixed effects table
- No NaN in predictions
- AIC > 0 (typical range 10000-20000)
- ”AIC computed correctly (AIC_piecewise - AIC_continuous)
- Convergence status documented
- Interaction p-value in [0, 1]

*Log Validation:*
- Required pattern: "Fitting piecewise model: theta ~ Days_within * Segment + (Days_within | UID)"
- Required pattern: "Model converged: True" OR "Convergence failed, using fallback: [fallback type]"
- Required pattern: "Early segment slope: [value]"
- Required pattern: "Late segment slope: [value]"
- Required pattern: "AIC comparison: piecewise=[value], continuous=[value], ”AIC=[value]"
- Required pattern: "Test 2 result: [PASS/FAIL] - piecewise [superior/inferior/equivalent]"
- Forbidden patterns: "ERROR", "AIC comparison failed", "Interaction term estimation failed"
- Acceptable warnings: Same as Step 2 (convergence fallback documented)

**Expected Behavior on Validation Failure:**
- If convergence fails completely -> QUIT with error, invoke g_debug
- If interaction term estimation fails -> QUIT with error, log details
- If AIC comparison fails (cannot load continuous AIC) -> QUIT with error, check RQ 5.7 outputs

---

### Step 4: Validate LMM Assumptions (Test 3 - Comprehensive Assumption Checks)

**Purpose:** Perform comprehensive LMM assumption validation for both quadratic and piecewise models (6 assumption checks: normality, homoscedasticity, autocorrelation, random effects normality, linearity, outliers)

**Dependencies:** Step 2 (requires fitted quadratic model), Step 3 (requires fitted piecewise model)

**Complexity:** Low (diagnostic tests only, <5 minutes)

**Input:**

**File 1:** Fitted quadratic model object (in memory from Step 2)
**File 2:** Fitted piecewise model object (in memory from Step 3)
**File 3:** data/step01_time_transformed.csv (for residual computation)

**Processing:**

1. **Residual Normality (Shapiro-Wilk test):**
   - Test both quadratic and piecewise residuals
   - Null hypothesis: Residuals are normally distributed
   - p > 0.05: Assumption satisfied
   - p <= 0.05: Assumption violated (consider robust SE)

2. **Homoscedasticity (residuals vs fitted plot):**
   - Visual inspection for funnel patterns
   - Quantitative test: Breusch-Pagan test
   - p > 0.05: Homoscedasticity assumption satisfied
   - p <= 0.05: Heteroscedasticity detected (consider variance structure)

3. **Random Effects Normality (Q-Q plots):**
   - Extract random intercepts and slopes
   - Q-Q plot for normality assessment
   - Shapiro-Wilk test on random effects
   - p > 0.05: Random effects normally distributed

4. **Independence / Autocorrelation (ACF plots):**
   - Compute Lag-1 autocorrelation of residuals
   - Threshold: |ACF(1)| < 0.1 acceptable for repeated measures
   - If |ACF(1)| >= 0.1: Autocorrelation detected (consider AR(1) structure)

5. **Linearity within segments (partial residual plots):**
   - For piecewise model: Check linearity within Early and Late segments separately
   - For quadratic model: Check if quadratic term captures all curvature

6. **Outlier Detection (Cook's distance):**
   - Compute Cook's distance for all observations
   - Threshold: Cook's D > 4/n (n = 400 observations)
   - Flag influential observations (if any)

**Output:**

**File:** results/step04_assumption_validation_report.txt
**Format:** Plain text file
**Contents:**
  - **Quadratic Model Assumptions:**
    - Residual normality: Shapiro-Wilk test statistic, p-value, result (PASS/FAIL)
    - Homoscedasticity: Breusch-Pagan test statistic, p-value, result (PASS/FAIL)
    - Random effects normality: Shapiro-Wilk test statistic, p-value, result (PASS/FAIL)
    - Autocorrelation: Lag-1 ACF, result (PASS/FAIL)
    - Linearity: Visual assessment result
    - Outliers: Number of influential points (Cook's D > 4/n)
  - **Piecewise Model Assumptions:**
    - (Same 6 checks as quadratic model)
  - **Remedial Actions Recommended:**
    - List any assumption violations with suggested remedies
    - Example: "Heteroscedasticity detected -> consider modeling variance structure"
  - **Overall Assessment:**
    - Summary: How many assumptions satisfied for each model
    - Conclusion: Models suitable for inference or require modifications

**Validation Requirement:**
Validation tools MUST be used after assumption validation execution. Specific validation tools will be determined by rq_tools based on assumption checking requirements (test statistic bounds validation, p-value validation). The rq_analysis agent will embed validation tool calls after the assumption validation tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step04_assumption_validation_report.txt exists (exact path)
- File size > 1 KB (comprehensive report with all 6 checks for 2 models)

*Value Ranges:*
- All p-values in [0, 1]
- All test statistics finite (not NaN, not Inf)
- Lag-1 ACF in [-1, 1]
- Cook's D values in [0, Inf) (non-negative)

*Data Quality:*
- All 6 assumption checks performed for both models (12 total checks)
- Results clearly labeled (PASS/FAIL for each check)
- Remedial actions listed if any assumption violated
- Overall assessment provided

*Log Validation:*
- Required pattern: "Performing assumption validation for quadratic model"
- Required pattern: "Performing assumption validation for piecewise model"
- Required pattern: "Residual normality test: Shapiro-Wilk W=[value], p=[value]"
- Required pattern: "Homoscedasticity test: Breusch-Pagan chi2=[value], p=[value]"
- Required pattern: "Autocorrelation check: Lag-1 ACF=[value]"
- Required pattern: "Overall assessment: [X]/6 assumptions satisfied for quadratic, [Y]/6 for piecewise"
- Forbidden patterns: "ERROR", "Test failed to execute", "Cannot compute residuals"
- Acceptable warnings: "Assumption violated: [specific assumption] - remedial action recommended"

**Expected Behavior on Validation Failure:**
- If assumption tests cannot execute -> QUIT with error, invoke g_debug
- If all assumptions violated for both models -> QUIT with error, models not suitable for inference
- If some assumptions violated -> Document in report, suggest remedial actions, proceed to Step 5

---

### Step 5: Extract Slopes and Compute Ratio (Test 4 - Early vs Late Slope Comparison)

**Purpose:** Extract Early segment slope and Late segment slope from piecewise model, compute Late/Early ratio (expect < 0.5 if two-phase robust)

**Dependencies:** Step 3 (requires fitted piecewise model with segment slopes)

**Complexity:** Low (slope extraction and ratio computation, <5 minutes)

**Input:**

**File:** results/step03_piecewise_model_summary.txt
**Source:** Generated by Step 3
**Format:** Plain text file with fixed effects table
**Contains:** Early slope (Days_within coefficient), Late slope (Days_within + interaction coefficient)

**Processing:**

1. **Extract slopes from fixed effects:**
   - Early slope = coefficient for `Days_within` (main effect)
   - Late slope = coefficient for `Days_within` + coefficient for `Days_within:SegmentLate` (interaction)
   - Extract SE for both slopes (via delta method for Late slope)

2. **Compute slope ratio:**
   - Ratio = Late slope / Early slope
   - Expected: Ratio < 0.5 if two-phase pattern robust
   - Interpretation:
     - Ratio < 0.5: Late forgetting is less than half as steep as Early (strong two-phase)
     - 0.5 <= Ratio < 1.0: Late forgetting slower than Early (moderate two-phase)
     - Ratio >= 1.0: Late forgetting as steep or steeper than Early (no two-phase)

3. **Compute 95% confidence interval for ratio:**
   - Use delta method to propagate SE from slope estimates to ratio
   - CI excludes 1.0 if two-phase pattern is statistically significant

4. **Test Segment x Time interaction:**
   - Extract p-value for `Days_within:SegmentLate` interaction term
   - Bonferroni threshold: p < 0.0033
   - Significant interaction = slopes differ significantly between segments

**Output:**

**File:** results/step05_slope_comparison.csv
**Format:** CSV with slope estimates and ratio
**Columns:**
  - `metric` (string, metric name: "Early_slope", "Late_slope", "Ratio", "Interaction_p")
  - `value` (float, estimated value)
  - `SE` (float, standard error, NA for p-value)
  - `CI_lower` (float, lower 95% CI, NA for p-value)
  - `CI_upper` (float, upper 95% CI, NA for p-value)
  - `interpretation` (string, verbal interpretation)
**Expected Rows:** 4 rows (Early slope, Late slope, Ratio, Interaction p-value)

**Validation Requirement:**
Validation tools MUST be used after slope extraction execution. Specific validation tools will be determined by rq_tools based on slope extraction requirements (coefficient bounds validation, ratio computation validation). The rq_analysis agent will embed validation tool calls after the slope extraction tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step05_slope_comparison.csv exists (exact path)
- Expected rows: 4 (Early slope, Late slope, Ratio, Interaction p)
- Expected columns: 6 (metric, value, SE, CI_lower, CI_upper, interpretation)
- Data types: metric (string), value (float64), SE (float64), CI_lower (float64), CI_upper (float64), interpretation (string)

*Value Ranges:*
- Early_slope in [-0.1, 0.0] (negative = forgetting, close to 0 = minimal forgetting)
- Late_slope in [-0.05, 0.0] (negative, shallower than Early)
- Ratio in [0, 2.0] (positive, typically < 1.0 if Late slower than Early)
- Interaction_p in [0, 1]

*Data Quality:*
- No NaN in value column (all metrics must be estimated)
- SE provided for slopes and ratio (not for p-value)
- CI_lower < CI_upper for all metrics with CIs
- Interpretation field non-empty (verbal summary per metric)

*Log Validation:*
- Required pattern: "Extracted Early segment slope: [value] (SE=[value])"
- Required pattern: "Extracted Late segment slope: [value] (SE=[value])"
- Required pattern: "Computed Late/Early ratio: [value] (95% CI: [lower], [upper])"
- Required pattern: "Interaction significance test: p=[value]"
- Required pattern: "Test 4 result: [PASS/FAIL] - ratio [< 0.5 / >= 0.5]"
- Forbidden patterns: "ERROR", "Slope extraction failed", "Delta method failed"
- Acceptable warnings: None expected for slope extraction

**Expected Behavior on Validation Failure:**
- If slope extraction fails -> QUIT with error, invoke g_debug
- If delta method fails (cannot compute ratio SE) -> QUIT with error, log details
- If ratio computation produces NaN -> QUIT with error, check denominator (Early slope = 0?)

---

### Step 6: Prepare Plot Data

**Purpose:** Aggregate observed means and model predictions for visualization (Option B: plot source CSV for rq_plots agent)

**Dependencies:** Step 0 (observed theta), Step 2 (quadratic predictions), Step 3 (piecewise predictions)

**Complexity:** Low (data aggregation, <5 minutes)

**Input:**

**File 1:** data/step00_theta_tsvr.csv
**Source:** Generated by Step 0
**Columns:** UID, test, TSVR_hours, theta
**Use:** Compute observed means with 95% CIs per timepoint

**File 2:** data/step02_quadratic_predictions.csv
**Source:** Generated by Step 2
**Columns:** Time, predicted_theta, CI_lower, CI_upper
**Use:** Overlay quadratic model predictions on plot

**File 3:** data/step03_piecewise_predictions.csv
**Source:** Generated by Step 3
**Columns:** Segment, Days_within, TSVR_hours, predicted_theta, CI_lower, CI_upper
**Use:** Overlay piecewise model predictions on plot with inflection at 48 hours

**Processing:**

1. **Compute observed means:**
   - Group data/step00_theta_tsvr.csv by TSVR_hours (4 unique values: ~0, ~24, ~72, ~144)
   - Compute mean(theta), SE(theta), 95% CI per timepoint
   - Label as "Observed" source

2. **Format quadratic predictions:**
   - Rename Time -> TSVR_hours for consistency
   - Label as "Quadratic Model" source

3. **Format piecewise predictions:**
   - Already has TSVR_hours column
   - Label as "Piecewise Model" source
   - Add segment indicator (Early/Late) for visual distinction

4. **Combine all sources:**
   - Stack observed means, quadratic predictions, piecewise predictions
   - Add `source` column to distinguish ("Observed", "Quadratic", "Piecewise")
   - Sort by TSVR_hours for plotting

**Output:**

**File:** plots/step06_piecewise_comparison_data.csv
**Format:** CSV with observed + predicted data for plotting
**Columns:**
  - `source` (string, "Observed", "Quadratic", or "Piecewise")
  - `TSVR_hours` (float, time since encoding)
  - `theta` (float, observed or predicted theta)
  - `CI_lower` (float, lower 95% CI)
  - `CI_upper` (float, upper 95% CI)
  - `Segment` (string, "Early" or "Late" for piecewise, NA for others)
**Expected Rows:** ~33 rows (4 observed + 11 quadratic + 18 piecewise)

**Plot Description (for rq_plots agent):**
Two-panel plot comparing piecewise vs continuous models:
- Panel 1: Observed means (points with error bars) + quadratic model (smooth line)
- Panel 2: Observed means (points with error bars) + piecewise model (two-segment line with inflection at 48 hours)
- X-axis: TSVR_hours (0-240)
- Y-axis: Theta (-3 to 3)
- Highlight inflection point at 48 hours (vertical dashed line)

**Plotting Function:** Two-panel comparison plot (rq_plots maps to appropriate plotting function from tools/plots.py)

**Validation Requirement:**
Validation tools MUST be used after plot data preparation execution. Specific validation tools will be determined by rq_tools based on plot data aggregation requirements (row count validation, column schema validation, value range validation). The rq_analysis agent will embed validation tool calls after the plot preparation tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- plots/step06_piecewise_comparison_data.csv exists (exact path)
- Expected rows: 30-35 rows (4 observed + 11 quadratic + 18 piecewise)
- Expected columns: 6 (source, TSVR_hours, theta, CI_lower, CI_upper, Segment)
- Data types: source (string), TSVR_hours (float64), theta (float64), CI_lower (float64), CI_upper (float64), Segment (string)

*Value Ranges:*
- TSVR_hours in [0, 240]
- theta in [-3, 3]
- CI_lower in [-4, 2]
- CI_upper in [-2, 4]
- CI_upper > CI_lower for all rows
- source in {"Observed", "Quadratic", "Piecewise"}
- Segment in {"Early", "Late", NA} (NA for Observed and Quadratic)

*Data Quality:*
- No NaN in source, TSVR_hours, theta, CI_lower, CI_upper columns
- Segment can be NA for non-piecewise sources
- Expected N: Exactly 4 observed timepoints
- Distribution check: TSVR_hours should have 4 clusters for observed data

*Log Validation:*
- Required pattern: "Computed observed means: 4 timepoints"
- Required pattern: "Formatted quadratic predictions: 11 timepoints"
- Required pattern: "Formatted piecewise predictions: 18 timepoints (9 Early + 9 Late)"
- Required pattern: "Combined plot data: [N] rows total"
- Forbidden patterns: "ERROR", "Merge failed", "Missing data source"
- Acceptable warnings: None expected for data aggregation

**Expected Behavior on Validation Failure:**
- If observed means computation fails -> QUIT with error, invoke g_debug
- If prediction formatting fails -> QUIT with error, check Step 2/3 outputs
- If row count incorrect -> QUIT with error, investigate missing data

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 -> Step 1:**
- Input: data/step00_theta_tsvr.csv (UID, test, TSVR_hours, theta)
- Transformation: Add columns (Time, Time_squared, Time_log, Segment, Days_within)
- Output: data/step01_time_transformed.csv (UID, test, TSVR_hours, theta, Time, Time_squared, Time_log, Segment, Days_within)
- Format: Long (one row per participant-test)

**Step 1 -> Step 2:**
- Input: data/step01_time_transformed.csv
- Transformation: LMM fitting (quadratic model)
- Output: results/step02_quadratic_model_summary.txt (model summary), data/step02_quadratic_predictions.csv (predictions)
- Format: Summary (text), Predictions (CSV with 11 rows)

**Step 1 -> Step 3:**
- Input: data/step01_time_transformed.csv
- Transformation: LMM fitting (piecewise model)
- Output: results/step03_piecewise_model_summary.txt (model summary), data/step03_piecewise_predictions.csv (predictions)
- Format: Summary (text), Predictions (CSV with 18 rows, 2 segments)

**Step 2, Step 3 -> Step 4:**
- Input: Fitted model objects (in memory)
- Transformation: Assumption validation (6 checks per model)
- Output: results/step04_assumption_validation_report.txt
- Format: Text report with test statistics and interpretations

**Step 3 -> Step 5:**
- Input: results/step03_piecewise_model_summary.txt (fixed effects)
- Transformation: Slope extraction and ratio computation
- Output: results/step05_slope_comparison.csv
- Format: CSV with 4 rows (Early slope, Late slope, Ratio, Interaction p)

**Step 0, Step 2, Step 3 -> Step 6:**
- Input: data/step00_theta_tsvr.csv, data/step02_quadratic_predictions.csv, data/step03_piecewise_predictions.csv
- Transformation: Aggregate observed means + format predictions + stack
- Output: plots/step06_piecewise_comparison_data.csv
- Format: CSV with ~33 rows (3 sources combined)

### Column Naming Conventions

**Per names.md:**
- `UID` - Participant unique identifier (format: P### with leading zeros)
- `test` - Test session identifier (T1, T2, T3, T4)
- `TSVR_hours` - Time Since VR in hours (Decision D070)
- `theta` - IRT latent ability estimate (domain-collapsed for this RQ)
- `composite_ID` - NOT USED in this RQ (no IRT calibration, theta inherited from RQ 5.7)

**New Variables (RQ 5.8-specific):**
- `Time` - Copy of TSVR_hours for quadratic model (convention: match formula variable name)
- `Time_squared` - TSVR_hours² for quadratic term
- `Time_log` - log(TSVR_hours + 1) for potential log model
- `Segment` - "Early" or "Late" based on 48-hour inflection
- `Days_within` - Time recentered within segment (0 = segment start)

### Data Type Constraints

**Nullable vs Non-Nullable:**
- UID, test, TSVR_hours, theta: Non-nullable (all participants must have values)
- Time, Time_squared, Time_log, Segment, Days_within: Non-nullable (deterministic transformations)
- Segment in Step 6 plot data: Nullable for Observed and Quadratic sources (only Piecewise has segments)

**Valid Ranges:**
- TSVR_hours: [0, 240] hours (0 = encoding, 240 = 10 days maximum)
- theta: [-3, 3] typical IRT range (extreme values possible but rare)
- Time_squared: [0, 57600] (max = 240²)
- Time_log: [0, 5.5] (log(240+1))
- Days_within: [0, 192] (Early: 0-48, Late: 0-192 recentered)

**Categorical Values:**
- Segment: {"Early", "Late"}
- source (plot data): {"Observed", "Quadratic", "Piecewise"}

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

#### Step 0: Get Data

**Analysis Tool:** (determined by rq_tools - likely pandas.read_csv + pandas.merge)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_merge_operation)

**What Validation Checks:**
- All 3 RQ 5.7 files exist (theta, TSVR, best model)
- Merge produces expected row count (~400 rows)
- No unexpected NaN after merge
- Domain collapse produces single theta per (UID, test)
- AIC value is positive and reasonable (10000-20000 range)

**Expected Behavior on Validation Failure:**
- If RQ 5.7 file missing -> QUIT with EXPECTATIONS ERROR
- If merge fails -> QUIT with error, log details, invoke g_debug
- If NaN detected -> QUIT with error, list affected rows
- If row count <380 -> QUIT with error, investigate data loss

---

#### Step 1: Create Time Transformations

**Analysis Tool:** (determined by rq_tools - likely pandas operations for column creation)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_column_creation)

**What Validation Checks:**
- All expected columns created (Time, Time_squared, Time_log, Segment, Days_within)
- No NaN created (transformations are deterministic)
- Segment assignment correct (~50% Early, ~50% Late)
- Days_within starts at 0 for both segments

**Expected Behavior on Validation Failure:**
- If column missing -> QUIT with error, transformation failed
- If NaN created -> QUIT with error, log which transformation failed
- If Segment imbalanced (>70% Early or Late) -> QUIT with error, investigate inflection logic

---

#### Step 2: Fit Quadratic Model

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.fit_lmm_trajectory_tsvr)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_lmm_convergence + validate_lmm_assumptions_comprehensive)

**What Validation Checks:**
- Model converged (or documented fallback used)
- Fixed effects estimated (no NaN in coefficients)
- Predictions generated for all timepoints (11 rows)
- Time_squared p-value in [0, 1]
- AIC > 0

**Expected Behavior on Validation Failure:**
- If all convergence attempts fail -> QUIT with error, invoke g_debug
- If fixed effects contain NaN -> QUIT with error, model estimation failed
- If predictions missing -> QUIT with error, prediction failed

---

#### Step 3: Fit Piecewise Model

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.fit_lmm_trajectory_tsvr with piecewise formula)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_lmm_convergence + tools.validation.validate_aic_comparison)

**What Validation Checks:**
- Model converged (or documented fallback used)
- Fixed effects estimated (Intercept, Days_within, SegmentLate, interaction)
- Predictions generated for all segment x timepoint combinations (18 rows)
- AIC comparison computed (”AIC finite, not NaN)
- Interaction p-value in [0, 1]

**Expected Behavior on Validation Failure:**
- If convergence fails -> QUIT with error, invoke g_debug
- If interaction estimation fails -> QUIT with error, log details
- If AIC comparison fails -> QUIT with error, check RQ 5.7 best model AIC

---

#### Step 4: Validate LMM Assumptions

**Analysis Tool:** (determined by rq_tools - likely tools.validation.validate_lmm_assumptions_comprehensive)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_hypothesis_tests for p-value bounds)

**What Validation Checks:**
- All 6 assumption checks performed for both models (12 total)
- Test statistics finite (not NaN, not Inf)
- p-values in [0, 1]
- PASS/FAIL results documented for each check
- Remedial actions listed if violations detected

**Expected Behavior on Validation Failure:**
- If assumption tests cannot execute -> QUIT with error, invoke g_debug
- If all assumptions violated for both models -> QUIT with error, models unsuitable
- If some violations -> Document, recommend remedies, proceed to Step 5

---

#### Step 5: Extract Slopes and Compute Ratio

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.extract_segment_slopes_from_lmm)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_slope_extraction)

**What Validation Checks:**
- Both slopes extracted (Early, Late)
- Ratio computed (finite, not NaN)
- SE computed via delta method
- 95% CIs non-overlapping (CI_lower < CI_upper)
- Interaction p-value in [0, 1]

**Expected Behavior on Validation Failure:**
- If slope extraction fails -> QUIT with error, invoke g_debug
- If delta method fails -> QUIT with error, log details
- If ratio is NaN -> QUIT with error, check denominator (Early slope = 0?)

---

#### Step 6: Prepare Plot Data

**Analysis Tool:** (determined by rq_tools - likely pandas groupby + merge operations)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_plot_data_preparation)

**What Validation Checks:**
- All 3 data sources loaded successfully
- Observed means computed (4 timepoints)
- Predictions formatted correctly (11 quadratic + 18 piecewise)
- Combined data has expected row count (30-35)
- All required columns present (source, TSVR_hours, theta, CI_lower, CI_upper, Segment)
- No NaN in critical columns (source, TSVR_hours, theta, CIs)

**Expected Behavior on Validation Failure:**
- If observed means fail -> QUIT with error, invoke g_debug
- If prediction formatting fails -> QUIT with error, check Step 2/3 outputs
- If row count incorrect -> QUIT with error, investigate missing data

---

## Summary

**Total Steps:** 7 (Step 0: Get Data, Steps 1-6: Analysis + Visualization)
**Estimated Runtime:** 30-60 minutes (medium complexity - LMM fitting with random slopes + comprehensive assumption validation)
**Cross-RQ Dependencies:** RQ 5.7 must complete successfully (provides theta scores, TSVR mapping, best continuous model)
**Primary Outputs:**
  - Quadratic model summary (Test 1 results)
  - Piecewise model summary (Test 2 results)
  - Assumption validation report (Test 3 results)
  - Slope comparison (Test 4 results)
  - Plot source CSV for visualization (two-panel piecewise vs continuous comparison)
**Validation Coverage:** 100% (all 7 steps have validation requirements with 4-layer substance criteria)

**Triangulation Strategy:**
Evidence for two-phase forgetting comes from convergence of three independent tests:
1. Significant positive quadratic term (deceleration)
2. Piecewise model superior to continuous (”AIC < -2)
3. Late/Early slope ratio < 0.5 (late forgetting less than half as steep)

If all three tests converge, evidence is strong. If tests diverge, interpretation is nuanced (e.g., quadratic significant but AIC inconclusive suggests weak two-phase pattern).

**Convergence Considerations:**
With N=100 participants, complex random slopes structures may not converge. Fallback hierarchy ensures models fit even if maximal structure fails. Convergence decisions documented transparently. If fallback to random intercepts only (1 | UID) required, triangulation evidence applies to population-average trajectory, not individual-level patterns.

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_name.py scripts

---

**Version History:**
- v1.0 (2025-11-26): Initial plan created by rq_planner agent for RQ 5.8
