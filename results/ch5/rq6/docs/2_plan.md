# Analysis Plan for RQ 5.6: Congruent Items and Early Consolidation

**Created by:** rq_planner agent
**Date:** 2025-11-25
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This RQ examines whether schema congruence effects on forgetting are driven by differential consolidation (Day 0-1) or later decay (Day 1-6). The analysis uses piecewise Linear Mixed Models (LMM) to model two distinct temporal phases: Early segment (Days 0-1, consolidation-dominated with one night's sleep) and Late segment (Days 1-6, decay-dominated). The investigation tests sleep consolidation theory's prediction that schema-congruent items preferentially benefit from hippocampal-neocortical dialogue during sleep.

**Pipeline Type:** LMM-only (no IRT calibration - uses DERIVED theta scores from RQ 5.5)

**Total Steps:** 7 analysis steps (Step 0: data extraction from RQ 5.5 + Steps 1-6: piecewise LMM analysis and validation)

**Estimated Runtime:** Medium (~15-30 minutes total)
- Step 0: Low (1-2 min, data extraction from RQ 5.5)
- Step 1: Low (2-3 min, data preparation and piecewise structure)
- Step 2: Medium (5-10 min, LMM fitting with 3-way interaction)
- Step 3: Low (1-2 min, slope extraction)
- Step 4: Low (1-2 min, hypothesis testing)
- Step 5: Medium (3-5 min, assumption validation)
- Step 6: Low (2-3 min, plot data preparation)

**Key Decisions Applied:**
- **Decision D068:** Dual p-value reporting (uncorrected + Bonferroni correction with alpha = 0.0033)
- **Decision D070:** TSVR as LMM time variable (actual hours, not nominal days)
- **Decision D069:** NOT applicable (concept Section 5 mentions "two-panel piecewise trajectory plot" but no dual-scale requirement for piecewise segment comparison plots)

**Cross-RQ Dependency:** RQ 5.5 must complete Steps 1-3 before this RQ can execute (DERIVED theta scores required)

---

## Analysis Plan

### Step 0: Extract Theta Scores from RQ 5.5

**Dependencies:** RQ 5.5 Step 3 complete (theta scores by congruence available)
**Complexity:** Low (1-2 minutes, file read and validation)

**Purpose:** Extract IRT ability estimates (theta scores) from RQ 5.5 analysis. RQ 5.5 calibrated IRT models on "Items by Congruence" factor structure (Common/Congruent/Incongruent), producing theta estimates that this RQ uses as outcome variable for piecewise LMM.

**Input:**

**File 1:** results/ch5/rq5/data/step03_theta_scores.csv
**Source:** RQ 5.5 Step 3 (IRT calibration Pass 2 theta extraction)
**Format:** CSV with columns:
  - `composite_ID` (string, format: {UID}_{test}, e.g., P001_T1)
  - `theta_common` (float, ability estimate for Common congruence items)
  - `theta_congruent` (float, ability estimate for Congruent items)
  - `theta_incongruent` (float, ability estimate for Incongruent items)
  - `se_common` (float, standard error for Common theta)
  - `se_congruent` (float, standard error for Congruent theta)
  - `se_incongruent` (float, standard error for Incongruent theta)
**Expected Rows:** 400 (100 participants x 4 tests)
**Expected Columns:** 7 (composite_ID + 3 theta + 3 SE)

**Processing:**
1. Check RQ 5.5 status: Read results/ch5/rq5/status.yaml, verify rq_results.status = "success"
2. If RQ 5.5 incomplete: QUIT with EXPECTATIONS ERROR "RQ 5.5 must complete before RQ 5.6 (DERIVED data dependency)"
3. Read results/ch5/rq5/data/step03_theta_scores.csv
4. Validate expected structure (400 rows, 7 columns, no NaN in theta columns)
5. Copy to results/ch5/rq6/data/step00_theta_scores_from_rq5.csv (local cache for this RQ)

**Output:**

**File:** data/step00_theta_scores_from_rq5.csv
**Format:** Identical to RQ 5.5 theta scores (CSV with 7 columns)
**Expected Rows:** 400
**Expected Columns:** 7 (composite_ID, theta_common, theta_congruent, theta_incongruent, se_common, se_congruent, se_incongruent)

**Validation Requirement:**
Validation tools MUST be used after data extraction tool execution. Specific validation tools will be determined by rq_tools based on file format and dependency checks (RQ 5.5 status validation, file existence validation, schema validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_theta_scores_from_rq5.csv: 400 rows x 7 columns (composite_ID: object, theta_*: float64, se_*: float64)

*Value Ranges:*
- theta_common in [-3, 3] (typical IRT ability range)
- theta_congruent in [-3, 3]
- theta_incongruent in [-3, 3]
- se_common in [0.1, 1.0] (standard errors above 1.0 indicate unreliable estimates)
- se_congruent in [0.1, 1.0]
- se_incongruent in [0.1, 1.0]

*Data Quality:*
- All 400 rows present (100 participants x 4 tests, no missing data)
- No NaN values in theta or SE columns (IRT must estimate for all observations)
- No duplicate composite_IDs (each participant-test combination unique)
- All three congruence types present (Common, Congruent, Incongruent)

*Log Validation:*
- Required pattern: "RQ 5.5 status verified: rq_results = success"
- Required pattern: "Theta scores extracted: 400 rows, 7 columns"
- Required pattern: "VALIDATION - PASS: theta range check"
- Required pattern: "VALIDATION - PASS: no missing data"
- Forbidden patterns: "ERROR", "RQ 5.5 incomplete", "File not found"
- Acceptable warnings: None expected for data extraction

**Expected Behavior on Validation Failure:**
- If RQ 5.5 incomplete: Raise EXPECTATIONS ERROR, log to logs/step00_extract_theta.log, quit immediately
- If file missing: Raise EXPECTATIONS ERROR, log error, quit immediately
- If schema mismatch (wrong columns): Raise EXPECTATIONS ERROR with details, quit immediately
- If value ranges violated: Raise EXPECTATIONS ERROR with specific violations, quit immediately
- Master invokes g_debug to diagnose root cause (RQ 5.5 execution problem or file corruption)

---

### Step 1: Prepare Piecewise LMM Input

**Dependencies:** Step 0 (theta scores from RQ 5.5)
**Complexity:** Low (2-3 minutes, data reshaping and variable creation)

**Purpose:** Transform theta scores from wide format (3 congruence columns) to long format (Congruence as factor variable) and create piecewise time structure with two segments: Early (Days 0-1, consolidation window) and Late (Days 1-6, decay-dominated phase).

**Input:**

**File 1:** data/step00_theta_scores_from_rq5.csv (from Step 0)
**Format:** CSV, wide format (one row per composite_ID, 3 theta columns)
**Expected Rows:** 400
**Expected Columns:** 7 (composite_ID, theta_common, theta_congruent, theta_incongruent, se_common, se_congruent, se_incongruent)

**File 2:** data/master.xlsx (Sheet: TSVR lookup - actual time since VR encoding)
**Source:** Project-level data source
**Required Tags:** {UID}-RVR-{Test}-STA-X-TSVR (hours since VR encoding, per Decision D070)
**Expected Rows:** 400 (100 participants x 4 tests)
**Note:** TSVR extracted via data.py functions, not direct Excel read

**Processing:**

**1. Reshape theta scores to long format:**
- Input: Wide format (composite_ID, theta_common, theta_congruent, theta_incongruent, se_common, se_congruent, se_incongruent)
- Output: Long format with Congruence as factor variable
- Transformation: Melt theta columns into (Congruence, theta, SE) triplets
- Expected result: 1200 rows (400 composite_IDs x 3 congruence types)

**2. Parse composite_ID:**
- Extract UID and test from composite_ID (format: {UID}_{test}, e.g., P001_T1)
- Create UID column (participant identifier)
- Create test column (T1, T2, T3, T4)

**3. Merge TSVR time variable (Decision D070):**
- Extract TSVR_hours from master.xlsx using data.py functions
- Pattern: {UID}-RVR-{Test}-STA-X-TSVR (actual hours since VR encoding)
- Merge on (UID, test) to add TSVR_hours column
- Expected: All 1200 rows matched (no missing TSVR values)

**4. Create piecewise segment structure:**
- Assign tests to segments based on TSVR_hours:
  - Early segment: TSVR_hours in [0, 24] hours (Days 0-1, includes one night's sleep)
  - Late segment: TSVR_hours in (24, 168] hours (Days 1-6, decay-dominated)
- Create Segment factor variable: "Early" or "Late"
- CRITICAL: Day 1 (TSVR ~ 24 hours) assigned to Early segment only (no overlap)

**5. Create Days_within variable:**
- Centered time variable for piecewise regression (0 at start of each segment)
- Early segment: Days_within = (TSVR_hours - 0) / 24 (range: 0 to 1 day)
- Late segment: Days_within = (TSVR_hours - 24) / 24 (range: 0 to 6 days)
- Purpose: Allows separate slope estimation per segment

**6. Treatment coding for factors:**
- Congruence: Common as reference level (baseline)
- Segment: Early as reference level (baseline)
- Purpose: Interaction term directly tests consolidation benefit (Early vs Late difference for Congruent vs Incongruent)

**Output:**

**File:** data/step01_lmm_input_piecewise.csv
**Format:** CSV, long format (one row per observation: participant x test x congruence)
**Expected Rows:** 1200 (400 composite_IDs x 3 congruence types)
**Expected Columns:** 9
  - `UID` (string, participant identifier, e.g., P001)
  - `test` (string, test session: T1, T2, T3, T4)
  - `composite_ID` (string, format: {UID}_{test})
  - `Congruence` (string, factor: Common, Congruent, Incongruent)
  - `theta` (float, IRT ability estimate for this congruence type)
  - `SE` (float, standard error of theta)
  - `TSVR_hours` (float, actual time since VR encoding, Decision D070)
  - `Segment` (string, factor: Early, Late)
  - `Days_within` (float, centered time variable: 0 at segment start)

**Validation Requirement:**
Validation tools MUST be used after data preparation tool execution. Specific validation tools determined by rq_tools based on piecewise structure requirements (segment assignment validation, no overlap validation, Days_within centering validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_lmm_input_piecewise.csv: 1200 rows x 9 columns (UID, test, composite_ID, Congruence, theta, SE, TSVR_hours, Segment, Days_within - all with correct data types)

*Value Ranges:*
- theta in [-3, 3] (IRT ability range)
- SE in [0.1, 1.0] (standard errors)
- TSVR_hours in [0, 168] hours (0 = encoding, 168 = 7 days)
- Days_within in [0, 1] for Early segment (0 to 1 day)
- Days_within in [0, 6] for Late segment (0 to 6 days after Day 1)
- Congruence in {Common, Congruent, Incongruent} (categorical)
- Segment in {Early, Late} (categorical)

*Data Quality:*
- Expected N: Exactly 1200 rows (400 composite_IDs x 3 congruence types)
- No NaN values in any column (all data complete)
- No duplicate rows (UID x test x Congruence combinations unique)
- Segment assignment check: Early segment has TSVR_hours <= 24, Late segment has TSVR_hours > 24
- No overlap: Each observation in exactly one segment
- Days_within centered correctly: Days_within = 0 at start of each segment
- All three congruence types present per composite_ID (data reshape correct)

*Log Validation:*
- Required pattern: "Data reshaped: 400 wide rows -> 1200 long rows"
- Required pattern: "TSVR merge complete: All 1200 rows matched"
- Required pattern: "Segment assignment: Early = {N_early} rows, Late = {N_late} rows"
- Required pattern: "Days_within centered: Early [0, 1], Late [0, 6]"
- Required pattern: "VALIDATION - PASS: no segment overlap"
- Required pattern: "VALIDATION - PASS: all congruence types present"
- Forbidden patterns: "ERROR", "Missing TSVR values", "Segment overlap detected", "NaN in critical columns"
- Acceptable warnings: None expected for data preparation

**Expected Behavior on Validation Failure:**
- If TSVR merge fails (missing values): Raise EXPECTATIONS ERROR, log specific UIDs with missing TSVR, quit immediately
- If segment overlap detected: Raise EXPECTATIONS ERROR, log overlapping rows, quit immediately
- If Days_within centering incorrect: Raise EXPECTATIONS ERROR, log range violations, quit immediately
- If row count wrong (!= 1200): Raise EXPECTATIONS ERROR, log actual vs expected, quit immediately
- Master invokes g_debug to diagnose root cause (data extraction error or transformation logic error)

---

### Step 2: Fit Piecewise LMM with 3-Way Interaction

**Dependencies:** Step 1 (piecewise LMM input prepared)
**Complexity:** Medium (5-10 minutes, model fitting with random effects)

**Purpose:** Fit piecewise Linear Mixed Model testing whether schema congruence effects differ between Early (consolidation) and Late (decay) segments. The 3-way interaction (Days_within x Segment x Congruence) tests the mechanistic prediction that congruent items benefit more during consolidation than decay.

**Input:**

**File:** data/step01_lmm_input_piecewise.csv (from Step 1)
**Format:** CSV, long format (1200 rows x 9 columns)
**Required Columns:** UID, Days_within, Segment, Congruence, theta
**Expected Rows:** 1200 (400 composite_IDs x 3 congruence types)

**Processing:**

**LMM Formula:**
```
theta ~ Days_within * Segment * Congruence + (1 + Days_within | UID)
```

**Fixed Effects Structure:**
- Main effects: Days_within, Segment[Late], Congruence[Congruent], Congruence[Incongruent]
- 2-way interactions: Days_within:Segment[Late], Days_within:Congruence[Congruent], Days_within:Congruence[Incongruent], Segment[Late]:Congruence[Congruent], Segment[Late]:Congruence[Incongruent]
- 3-way interactions: Days_within:Segment[Late]:Congruence[Congruent], Days_within:Segment[Late]:Congruence[Incongruent]

**Random Effects Structure:**
- Random intercepts by UID: (1 | UID)
- Random slopes by UID: (Days_within | UID)
- Note: N=100 participants at lower boundary for random slopes (Newsom recommends 100-200 groups)
- Convergence strategy: Attempt maximal model first, simplify to intercepts-only if convergence fails (documented in Section 7.2 of concept)

**Treatment Coding:**
- Congruence reference: Common (baseline)
- Segment reference: Early (baseline)
- Interpretation: Interaction terms test how Congruent/Incongruent differ from Common, and how Late differs from Early

**Model Fitting:**
- Method: REML=False (for model comparison via Likelihood Ratio Test)
- Optimization: Maximum 200 iterations (increased from default 100 per concept Section 7.2)
- Convergence check: Singular fit warnings, gradient norm < 0.01, Hessian positive definite

**Key Hypothesis Test:**
- Primary: 3-way interaction Days_within:Segment[Late]:Congruence[Congruent]
- Interpretation: Does congruent slope differ between Early and Late segments more than common slope?
- Expected: Negative coefficient (congruent benefit stronger in Early than Late)

**Output:**

**File 1:** results/step02_lmm_model_summary.txt
**Format:** Plain text summary of fitted model
**Content:**
  - Fixed effects table (coefficient, SE, z-value, p-value for each term)
  - Random effects variance components
  - Model fit statistics (AIC, BIC, log-likelihood)
  - Convergence status and warnings

**File 2:** results/step02_lmm_model.pkl
**Format:** Pickled Python object (fitted statsmodels MixedLM object)
**Purpose:** Save fitted model for downstream steps (slope extraction, post-hoc tests)

**File 3:** logs/step02_lmm_fitting.log
**Format:** Plain text log
**Content:**
  - Model formula
  - Convergence diagnostics (iterations, gradient norm, Hessian status)
  - Warnings or errors during fitting
  - Timestamp and execution duration

**Validation Requirement:**
Validation tools MUST be used after LMM fitting tool execution. Specific validation tools determined by rq_tools based on LMM convergence requirements (convergence status validation, singular fit detection, parameter bounds validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step02_lmm_model_summary.txt: exists, contains "Fixed Effects" section with 11 terms (main effects + interactions)
- results/step02_lmm_model.pkl: exists, valid pickle file (can be loaded)
- logs/step02_lmm_fitting.log: exists, contains convergence diagnostics

*Value Ranges:*
- Fixed effects coefficients: Scientifically reasonable (no extreme values > 10 in absolute value)
- Standard errors: All positive, typically < 1.0 (large SEs indicate estimation problems)
- P-values: in [0, 1] (by definition)
- Random effects variances: All positive (negative variances indicate model misspecification)
- AIC/BIC: Positive values (log-likelihood-based fit statistics)

*Data Quality:*
- All 11 fixed effects present (4 main effects + 5 two-way + 2 three-way = 11 total terms)
- No NaN coefficients (indicates estimation failure)
- No NaN standard errors (indicates variance-covariance matrix issues)
- Random effects variance components > 0 (variance cannot be negative)
- Convergence achieved: No "singular fit" warnings in log
- Gradient norm < 0.01 (optimization converged)

*Log Validation:*
- Required pattern: "Model converged: True"
- Required pattern: "Iterations: {N} (N < 200, optimization successful)"
- Required pattern: "Gradient norm: {value} (value < 0.01)"
- Required pattern: "VALIDATION - PASS: convergence check"
- Required pattern: "VALIDATION - PASS: no singular fit warnings"
- Forbidden patterns: "ERROR", "Singular fit", "Convergence failed", "NaN coefficients"
- Acceptable warnings: "Random slopes model: consider simplifying if convergence issues" (advisory only)

**Expected Behavior on Validation Failure:**
- If convergence fails: Log warning, attempt simplified model (intercepts-only), log comparison, proceed with best-converged model
- If both models fail: Raise EXPECTATIONS ERROR, log details, quit immediately
- If singular fit detected: Log warning, check variance components, document in results, proceed cautiously
- If NaN coefficients: Raise EXPECTATIONS ERROR, log specific terms with NaN, quit immediately
- Master invokes g_debug to diagnose root cause (model misspecification, collinearity, insufficient data)

---

### Step 3: Extract Segment-Specific Slopes

**Dependencies:** Step 2 (piecewise LMM fitted)
**Complexity:** Low (1-2 minutes, coefficient extraction and computation)

**Purpose:** Extract Early and Late segment slopes for each congruence type (Common, Congruent, Incongruent) from fitted piecewise LMM. Compute standard errors and 95% confidence intervals for slope estimates.

**Input:**

**File 1:** results/step02_lmm_model.pkl (from Step 2)
**Format:** Pickled statsmodels MixedLM object
**Content:** Fitted piecewise LMM with 3-way interaction

**File 2:** results/step02_lmm_model_summary.txt (from Step 2)
**Format:** Plain text summary
**Content:** Fixed effects table with coefficients and SEs

**Processing:**

**Early Segment Slopes (Segment = Early, reference level):**
- Common slope: beta_Days_within (main effect of Days_within)
- Congruent slope: beta_Days_within + beta_Days_within:Congruence[Congruent]
- Incongruent slope: beta_Days_within + beta_Days_within:Congruence[Incongruent]

**Late Segment Slopes (Segment = Late):**
- Common slope: beta_Days_within + beta_Days_within:Segment[Late]
- Congruent slope: beta_Days_within + beta_Days_within:Segment[Late] + beta_Days_within:Congruence[Congruent] + beta_Days_within:Segment[Late]:Congruence[Congruent]
- Incongruent slope: beta_Days_within + beta_Days_within:Segment[Late] + beta_Days_within:Congruence[Incongruent] + beta_Days_within:Segment[Late]:Congruence[Incongruent]

**Standard Error Computation:**
- Use delta method (variance-covariance matrix of fixed effects)
- Formula: SE(linear combination) = sqrt(a' * Sigma * a) where a is coefficient vector, Sigma is vcov matrix
- 95% CI: slope +/- 1.96 * SE

**Output:**

**File:** results/step03_segment_slopes.csv
**Format:** CSV with 6 rows (3 congruence types x 2 segments)
**Expected Columns:** 7
  - `Segment` (string, Early or Late)
  - `Congruence` (string, Common, Congruent, or Incongruent)
  - `Slope` (float, estimated slope in units theta/day)
  - `SE` (float, standard error of slope)
  - `CI_lower` (float, lower 95% confidence bound)
  - `CI_upper` (float, upper 95% confidence bound)
  - `Interpretation` (string, descriptive text: "decline" if negative, "improvement" if positive)

**Expected Rows:** 6
1. Early, Common, slope, SE, CI_lower, CI_upper, interpretation
2. Early, Congruent, slope, SE, CI_lower, CI_upper, interpretation
3. Early, Incongruent, slope, SE, CI_lower, CI_upper, interpretation
4. Late, Common, slope, SE, CI_lower, CI_upper, interpretation
5. Late, Congruent, slope, SE, CI_lower, CI_upper, interpretation
6. Late, Incongruent, slope, SE, CI_lower, CI_upper, interpretation

**Validation Requirement:**
Validation tools MUST be used after slope extraction tool execution. Specific validation tools determined by rq_tools based on statistical computation requirements (delta method validation, CI computation validation, slope interpretation validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step03_segment_slopes.csv: 6 rows x 7 columns (Segment, Congruence, Slope, SE, CI_lower, CI_upper, Interpretation - all with correct data types)

*Value Ranges:*
- Slope in [-2, 2] theta/day (forgetting slopes expected to be negative, typically -0.5 to -0.1 range)
- SE in [0.01, 0.5] (standard errors for slopes typically small with N=100)
- CI_lower < Slope < CI_upper (by definition)
- CI width (CI_upper - CI_lower) in [0.05, 1.0] (reasonable precision with N=100)

*Data Quality:*
- Expected N: Exactly 6 rows (3 congruence x 2 segments)
- No NaN values in any column (delta method must compute for all slopes)
- No duplicate rows (Segment x Congruence combinations unique)
- CI ordering correct: CI_lower < Slope < CI_upper for all rows
- Interpretation consistent with slope sign (negative slope -> "decline", positive -> "improvement")
- All three congruence types present per segment

*Log Validation:*
- Required pattern: "Slopes extracted: 6 combinations (3 congruence x 2 segments)"
- Required pattern: "Delta method SE computation: successful for all 6 slopes"
- Required pattern: "95% CI computed: all intervals valid"
- Required pattern: "VALIDATION - PASS: CI ordering check"
- Required pattern: "VALIDATION - PASS: no missing slopes"
- Forbidden patterns: "ERROR", "Delta method failed", "NaN in slope estimates", "CI computation error"
- Acceptable warnings: None expected for slope extraction

**Expected Behavior on Validation Failure:**
- If delta method fails (vcov matrix singular): Raise EXPECTATIONS ERROR, log which slope failed, quit immediately
- If CI computation error: Raise EXPECTATIONS ERROR, log details, quit immediately
- If slope interpretation inconsistent: Raise EXPECTATIONS ERROR, log inconsistency, quit immediately
- If row count wrong (!= 6): Raise EXPECTATIONS ERROR, log actual vs expected, quit immediately
- Master invokes g_debug to diagnose root cause (model fitting error or extraction logic error)

---

### Step 4: Test Key Hypothesis - Congruent Consolidation Benefit

**Dependencies:** Step 2 (piecewise LMM fitted)
**Complexity:** Low (1-2 minutes, hypothesis test extraction)

**Purpose:** Extract and test the key hypothesis: Congruent items show less forgetting during Early segment (consolidation window) compared to Incongruent items, and this benefit is larger in Early than Late segment (3-way interaction test).

**Input:**

**File 1:** results/step02_lmm_model.pkl (from Step 2)
**Format:** Pickled statsmodels MixedLM object
**Content:** Fitted piecewise LMM with 3-way interaction

**File 2:** results/step02_lmm_model_summary.txt (from Step 2)
**Format:** Plain text summary
**Content:** Fixed effects table with p-values

**Processing:**

**Primary Hypothesis Test:**
- Term: Days_within:Segment[Late]:Congruence[Congruent]
- Interpretation: Does congruent slope differ between Early and Late segments?
- Expected: Negative coefficient (congruent benefit stronger in Early than Late)
- Significance: Test at two thresholds per Decision D068
  - Uncorrected: alpha = 0.05
  - Bonferroni-corrected: alpha = 0.0033 (0.05 / 15 tests, per concept Section 7.3)

**Secondary Hypothesis Tests (15 tests total per concept Section 7.3):**
1. 3-way: Days_within:Segment[Late]:Congruence[Congruent]
2. 3-way: Days_within:Segment[Late]:Congruence[Incongruent]
3. 2-way: Days_within:Congruence[Congruent] (Early segment)
4. 2-way: Days_within:Congruence[Incongruent] (Early segment)
5. 2-way: Days_within:Segment[Late] (Common congruence)
6. 2-way: Segment[Late]:Congruence[Congruent] (across time)
7. 2-way: Segment[Late]:Congruence[Incongruent] (across time)
8. Main: Days_within (Early segment, Common congruence)
9. Main: Segment[Late] (Common congruence, Day 0)
10. Main: Congruence[Congruent] (Early segment, Day 0)
11. Main: Congruence[Incongruent] (Early segment, Day 0)
12-15. Post-hoc contrasts (computed in Step 6 if needed)

**Dual P-Value Reporting (Decision D068):**
- Report BOTH uncorrected p-value AND Bonferroni-corrected p-value
- Rationale: Exploratory thesis, transparent reporting of multiple testing
- Interpretation: Significant at uncorrected but not corrected = suggestive evidence, interpret cautiously

**Output:**

**File:** results/step04_hypothesis_tests.csv
**Format:** CSV with 11 rows (11 primary tests from LMM output, excluding post-hoc contrasts)
**Expected Columns:** 7
  - `Test_Name` (string, descriptive name of hypothesis test)
  - `Coefficient` (float, estimated effect size)
  - `SE` (float, standard error)
  - `z_value` (float, test statistic)
  - `p_uncorrected` (float, uncorrected p-value)
  - `p_bonferroni` (float, Bonferroni-corrected p-value = p_uncorrected * 15)
  - `Significant_Bonferroni` (boolean, TRUE if p_bonferroni < 0.05)

**Expected Rows:** 11 (all main effects, 2-way interactions, 3-way interactions from LMM)

**Validation Requirement:**
Validation tools MUST be used after hypothesis testing tool execution. Specific validation tools determined by rq_tools based on statistical inference requirements (p-value bounds validation, Bonferroni correction validation, significance labeling validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step04_hypothesis_tests.csv: 11 rows x 7 columns (Test_Name, Coefficient, SE, z_value, p_uncorrected, p_bonferroni, Significant_Bonferroni - all with correct data types)

*Value Ranges:*
- Coefficient: Scientifically reasonable (no extreme values > 10 in absolute value)
- SE: All positive, typically < 1.0
- z_value: Typically in [-5, 5] range (extreme z-values > 10 suggest problems)
- p_uncorrected in [0, 1] (by definition)
- p_bonferroni in [0, 15] (p_uncorrected * 15, can exceed 1.0)
- Significant_Bonferroni: TRUE if p_bonferroni < 0.05, FALSE otherwise

*Data Quality:*
- Expected N: Exactly 11 rows (all LMM fixed effects terms)
- No NaN values in any column (all tests must produce results)
- No duplicate Test_Name values (each test unique)
- Bonferroni correction applied correctly: p_bonferroni = p_uncorrected * 15
- Significance labeling correct: Significant_Bonferroni matches p_bonferroni < 0.05
- Primary hypothesis (3-way interaction Congruent) present in table

*Log Validation:*
- Required pattern: "Hypothesis tests extracted: 11 tests from LMM fixed effects"
- Required pattern: "Bonferroni correction applied: alpha = 0.05 / 15 = 0.0033"
- Required pattern: "Primary hypothesis: Days_within:Segment[Late]:Congruence[Congruent]"
- Required pattern: "Dual p-values reported per Decision D068"
- Required pattern: "VALIDATION - PASS: p-value bounds check"
- Required pattern: "VALIDATION - PASS: Bonferroni correction check"
- Forbidden patterns: "ERROR", "p-value out of bounds", "Bonferroni correction failed", "Missing primary hypothesis"
- Acceptable warnings: "Some tests non-significant after Bonferroni correction (expected for exploratory thesis)"

**Expected Behavior on Validation Failure:**
- If p-values out of bounds: Raise EXPECTATIONS ERROR, log specific violations, quit immediately
- If Bonferroni correction wrong: Raise EXPECTATIONS ERROR, log formula error, quit immediately
- If primary hypothesis missing: Raise EXPECTATIONS ERROR, log missing test, quit immediately
- If row count wrong (!= 11): Raise EXPECTATIONS ERROR, log actual vs expected, quit immediately
- Master invokes g_debug to diagnose root cause (LMM output parsing error or computation error)

---

### Step 5: Validate LMM Assumptions

**Dependencies:** Step 2 (piecewise LMM fitted)
**Complexity:** Medium (3-5 minutes, assumption diagnostics)

**Purpose:** Validate six core LMM assumptions per concept Section 7.1: residual normality, residual homoscedasticity, random effects normality, autocorrelation, outlier detection, and multicollinearity. Perform convergence diagnostics and sensitivity analyses per concept Sections 7.2-7.4.

**Input:**

**File 1:** results/step02_lmm_model.pkl (from Step 2)
**Format:** Pickled statsmodels MixedLM object
**Content:** Fitted piecewise LMM

**File 2:** data/step01_lmm_input_piecewise.csv (from Step 1)
**Format:** CSV, long format (1200 rows x 9 columns)
**Content:** Original data used for LMM fitting

**Processing:**

**1. Residual Normality:**
- Extract standardized residuals from fitted model
- Q-Q plot (saved to plots/)
- Shapiro-Wilk test: p > 0.05 acceptable
- Threshold: Moderate departures acceptable (LMM robust with N=100)

**2. Residual Homoscedasticity:**
- Residuals vs fitted values plot (saved to plots/)
- Levene's test or Breusch-Pagan test: p > 0.05 acceptable
- Threshold: Variance ratio across groups < 3:1 acceptable

**3. Random Effects Normality:**
- Extract BLUPs (Best Linear Unbiased Predictors) for random intercepts and slopes
- Q-Q plots for random effects (saved to plots/)
- Shapiro-Wilk test on BLUPs: p > 0.01 (more lenient than residuals)

**4. Autocorrelation:**
- ACF plot of residuals within participants (saved to plots/)
- Durbin-Watson statistic: 1.5-2.5 acceptable range
- Threshold: First-order autocorrelation |r| < 0.3 acceptable

**5. Outlier Detection:**
- Identify observations with |standardized residual| > 3
- Identify participants with random effects > 3 SD from mean
- Cook's distance for influential observations: D > 4/n threshold

**6. Multicollinearity:**
- Compute VIF (Variance Inflation Factor) for fixed effects
- Threshold: VIF < 5 acceptable, VIF < 10 tolerable
- Note: Unlikely with orthogonal time variable, but check anyway

**7. Convergence Diagnostics (Concept Section 7.2):**
- Check singular fit warnings
- Verify all variance components > 0
- Check gradient norm < 0.01
- Check Hessian matrix positive definite
- If convergence fails: Document simplified model strategy (intercepts-only)

**8. Sensitivity Analysis 1: Piecewise vs Continuous Time Models (Concept Section 7.4.1):**
- Fit continuous time models: Linear, Logarithmic, Lin+Log
- Compare AIC: If continuous models fit better, piecewise assumption may be unjustified
- Expected: Piecewise should fit better if consolidation vs decay are distinct processes

**9. Sensitivity Analysis 2: Knot Placement Sensitivity (Concept Section 7.4.2):**
- Test alternative knot placements: Day 0.5, Day 1.0, Day 1.5
- Compare AIC: If results highly sensitive to knot, conclusions fragile
- Expected: Day 1 knot should yield best fit (one night's sleep)

**10. Sensitivity Analysis 3: Derived Data Weighting (Concept Section 7.4.3):**
- Weight observations by inverse variance of theta estimates (1 / SE^2)
- Rationale: Theta scores have heterogeneous precision
- Compare weighted vs unweighted results: If substantially different, conclusions may be driven by imprecise estimates

**Output:**

**File 1:** results/step05_assumption_validation.txt
**Format:** Plain text report
**Content:**
  - Summary of all 6 assumption checks (pass/fail/warning)
  - Test statistics (Shapiro-Wilk p-values, Levene's p-value, Durbin-Watson statistic, VIF values)
  - Outlier counts (residual outliers, random effect outliers, influential observations)
  - Remedial actions recommended if assumptions violated

**File 2:** results/step05_convergence_diagnostics.txt
**Format:** Plain text report
**Content:**
  - Convergence status (success/failure)
  - Singular fit warnings (if any)
  - Variance components (all > 0?)
  - Gradient norm (< 0.01?)
  - Hessian status (positive definite?)
  - Model simplification strategy (if needed)

**File 3:** results/step05_sensitivity_analyses.csv
**Format:** CSV with 7 rows (1 primary piecewise model + 3 continuous models + 2 alternative knot models + 1 weighted model = 7 total)
**Expected Columns:** 7
  - `Model_Name` (string, descriptive name)
  - `Model_Type` (string, Piecewise, Linear, Logarithmic, Lin+Log, Weighted)
  - `AIC` (float, Akaike Information Criterion)
  - `BIC` (float, Bayesian Information Criterion)
  - `LogLik` (float, log-likelihood)
  - `Delta_AIC` (float, difference from best model)
  - `Best_Model` (boolean, TRUE if lowest AIC)

**File 4:** plots/step05_residual_diagnostics.png
**Format:** PNG image (4-panel diagnostic plot)
**Content:**
  - Panel 1: Q-Q plot of residuals
  - Panel 2: Residuals vs fitted values
  - Panel 3: Q-Q plot of random effects
  - Panel 4: ACF plot of residuals

**Validation Requirement:**
Validation tools MUST be used after assumption validation tool execution. Specific validation tools determined by rq_tools based on diagnostic requirements (assumption test completion validation, plot generation validation, sensitivity analysis completion validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step05_assumption_validation.txt: exists, contains all 6 assumption check results
- results/step05_convergence_diagnostics.txt: exists, contains convergence status and diagnostics
- results/step05_sensitivity_analyses.csv: 7 rows x 7 columns (Model_Name, Model_Type, AIC, BIC, LogLik, Delta_AIC, Best_Model)
- plots/step05_residual_diagnostics.png: exists, valid PNG file

*Value Ranges:*
- Shapiro-Wilk p-values in [0, 1]
- Levene's p-value in [0, 1]
- Durbin-Watson statistic in [0, 4] (1.5-2.5 ideal)
- VIF values > 0 (typically < 5 for good models)
- AIC/BIC: Positive values (log-likelihood-based)
- Delta_AIC in [0, Inf] (difference from best model)

*Data Quality:*
- All 6 assumption checks completed (results present in validation.txt)
- Convergence diagnostics complete (status present in convergence_diagnostics.txt)
- All 7 sensitivity models fitted (7 rows in sensitivity_analyses.csv)
- No NaN in sensitivity AIC/BIC values (all models converged)
- Best model identified (exactly one row with Best_Model = TRUE)
- Diagnostic plots generated (4-panel PNG exists)

*Log Validation:*
- Required pattern: "Assumption validation complete: 6 checks performed"
- Required pattern: "Residual normality: Shapiro-Wilk p = {value}"
- Required pattern: "Homoscedasticity: Levene's p = {value}"
- Required pattern: "Random effects normality: Shapiro-Wilk p = {value}"
- Required pattern: "Autocorrelation: Durbin-Watson = {value}"
- Required pattern: "Outliers detected: {N} observations"
- Required pattern: "Multicollinearity: Max VIF = {value}"
- Required pattern: "Convergence diagnostics: {status}"
- Required pattern: "Sensitivity analyses: 7 models fitted"
- Required pattern: "Best model: {name} (lowest AIC)"
- Required pattern: "VALIDATION - PASS: all assumption checks completed"
- Forbidden patterns: "ERROR", "Assumption check failed to compute", "Sensitivity model diverged", "Plot generation failed"
- Acceptable warnings: "Residual normality: slight departure (p = 0.03, acceptable)", "Random slopes: singular fit (consider simplifying)", "Knot placement: Day 1 not optimal (Day 0.5 has lower AIC by 2 units, within 2-unit threshold)"

**Expected Behavior on Validation Failure:**
- If assumption checks fail to compute: Raise EXPECTATIONS ERROR, log which check failed, quit immediately
- If convergence diagnostics indicate failure: Log warning, document simplified model strategy, proceed cautiously
- If sensitivity analyses fail (models don't converge): Log warning, report which models failed, proceed with primary model
- If diagnostic plots fail to generate: Raise EXPECTATIONS ERROR, log graphics error, quit immediately
- If all assumptions severely violated: Log warning, recommend interpreting results cautiously, proceed (don't quit - user may accept violations)
- Master invokes g_debug if critical failures (computation errors, not statistical violations)

---

### Step 6: Prepare Trajectory Plot Data (Two-Panel Early|Late Visualization)

**Dependencies:** Steps 2, 3 (piecewise LMM fitted, segment-specific slopes extracted)
**Complexity:** Low (2-3 minutes, data aggregation for plotting)

**Purpose:** Create plot source CSV for two-panel piecewise trajectory visualization showing Early segment (Days 0-1) and Late segment (Days 1-6) with separate lines for Common, Congruent, and Incongruent items. This is Option B architecture: plot data preparation executes during analysis (Step 14 CODE EXECUTION LOOP), rq_plots reads source CSV later for visualization-only.

**CRITICAL NOTE:** This is a plot data preparation step. It:
- Gets executed in Step 14 CODE EXECUTION LOOP (g_code -> bash -> rq_inspect)
- MUST have validation requirements (same as any analysis step)
- Outputs to plots/*.csv (not data/*.csv) but still validated by rq_inspect
- Created by g_code during analysis (NOT by rq_plots during visualization)

**Plot Description:** Two-panel trajectory plot showing forgetting curves separated by temporal segment (Early = consolidation window, Late = decay phase). Each panel shows three lines (Common/Congruent/Incongruent congruence types) with observed means and model predictions. Purpose: Visualize whether schema congruence effect is stronger during Early consolidation than Late decay.

**Required Data Sources:**
- results/step03_segment_slopes.csv (segment-specific slopes for model predictions)
- data/step01_lmm_input_piecewise.csv (observed data for means)
- results/step02_lmm_model.pkl (fitted model for predictions)

**Input:**

**File 1:** results/step03_segment_slopes.csv (from Step 3)
**Format:** CSV, 6 rows (3 congruence x 2 segments)
**Content:** Slope, SE, CI_lower, CI_upper per segment-congruence combination

**File 2:** data/step01_lmm_input_piecewise.csv (from Step 1)
**Format:** CSV, 1200 rows (400 composite_IDs x 3 congruence types)
**Content:** Observed theta values, Segment, Congruence, Days_within

**File 3:** results/step02_lmm_model.pkl (from Step 2)
**Format:** Pickled statsmodels MixedLM object
**Content:** Fitted piecewise LMM (for model predictions)

**Aggregation Logic:**

**1. Compute observed means per Segment x Congruence x Days_within:**
- Group data by (Segment, Congruence, Days_within)
- Compute mean(theta), 95% CI (mean +/- 1.96 * SE_mean)
- Expected: ~8 unique Days_within values per segment (Early: T1-T2, Late: T2-T4)

**2. Generate model predictions per Segment x Congruence:**
- Use fitted LMM to predict theta at Days_within grid (0 to 1 for Early, 0 to 6 for Late)
- Grid: 20 points per segment (smooth curves)
- Extract fixed effects predictions (population-level trajectories, not participant-specific)

**3. Merge observed means with model predictions:**
- Join on (Segment, Congruence, Days_within)
- For observed data: exact Days_within values
- For model predictions: interpolated grid

**4. Create two separate source CSVs (one per panel):**
- Early segment data: plots/step06_piecewise_early_data.csv
- Late segment data: plots/step06_piecewise_late_data.csv
- Reason: Two-panel plot requires separate data sources for faceting

**Output:**

**File 1:** plots/step06_piecewise_early_data.csv
**Format:** CSV for Early segment panel
**Expected Columns:** 7
  - `Days_within` (float, time within Early segment: 0 to 1 day)
  - `Congruence` (string, Common, Congruent, or Incongruent)
  - `theta_observed` (float, observed mean theta for this timepoint)
  - `CI_lower_observed` (float, lower 95% CI for observed mean)
  - `CI_upper_observed` (float, upper 95% CI for observed mean)
  - `theta_predicted` (float, model-predicted theta from LMM)
  - `Data_Type` (string, "Observed" or "Predicted")
**Expected Rows:** ~60 (3 congruence x 20 prediction grid points)

**File 2:** plots/step06_piecewise_late_data.csv
**Format:** CSV for Late segment panel
**Expected Columns:** 7 (same as Early segment)
**Expected Rows:** ~180 (3 congruence x 60 timepoints for Days 1-6 range)

**Plotting Function (rq_plots will call):** Two-panel trajectory plot with separate Early|Late facets
- rq_plots agent maps this description to tools/plots.py function (likely plot_piecewise_trajectory or similar)
- Plot reads plots/step06_piecewise_early_data.csv and plots/step06_piecewise_late_data.csv
- No data aggregation in rq_plots (visualization only per Option B)

**Validation Requirement:**
Validation tools MUST be used after plot data preparation tool execution. Specific validation tools determined by rq_tools based on plot data format requirements (observed means validation, model predictions validation, data merge validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- plots/step06_piecewise_early_data.csv: ~60 rows x 7 columns (Days_within, Congruence, theta_observed, CI_lower_observed, CI_upper_observed, theta_predicted, Data_Type)
- plots/step06_piecewise_late_data.csv: ~180 rows x 7 columns (same structure)

*Value Ranges:*
- Days_within in [0, 1] for Early segment
- Days_within in [0, 6] for Late segment
- theta_observed in [-3, 3] (IRT ability range)
- theta_predicted in [-3, 3]
- CI_lower_observed < theta_observed < CI_upper_observed (by definition)
- Congruence in {Common, Congruent, Incongruent}
- Data_Type in {Observed, Predicted}

*Data Quality:*
- Early segment: ~60 rows (3 congruence x 20 prediction points)
- Late segment: ~180 rows (3 congruence x 60 timepoints)
- No NaN in critical columns (theta_observed, theta_predicted, CI bounds)
- All three congruence types present in both segments
- CI ordering correct: CI_lower < theta_observed < CI_upper
- Predictions cover full Days_within range (0-1 for Early, 0-6 for Late)
- Observed means computed from aggregated data (not individual rows)

*Log Validation:*
- Required pattern: "Plot data prepared: Early segment = {N_early} rows, Late segment = {N_late} rows"
- Required pattern: "Observed means computed: {N_timepoints} unique Days_within values per segment"
- Required pattern: "Model predictions generated: 20 grid points per segment x 3 congruence types"
- Required pattern: "VALIDATION - PASS: all congruence types present"
- Required pattern: "VALIDATION - PASS: CI ordering correct"
- Forbidden patterns: "ERROR", "Missing congruence type", "NaN in theta columns", "Prediction grid incomplete"
- Acceptable warnings: "Some observed timepoints have <10 observations (small sample, wide CIs)"

**Expected Behavior on Validation Failure:**
- If observed means computation fails: Raise EXPECTATIONS ERROR, log which segment/congruence failed, quit immediately
- If model predictions fail: Raise EXPECTATIONS ERROR, log prediction error, quit immediately
- If merge fails (mismatched keys): Raise EXPECTATIONS ERROR, log merge issue, quit immediately
- If row counts wrong: Raise EXPECTATIONS ERROR, log actual vs expected, quit immediately
- Master invokes g_debug to diagnose root cause (aggregation error or model prediction error)

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 -> Step 1: Wide to Long Reshape**
- Input: Wide format (composite_ID, theta_common, theta_congruent, theta_incongruent)
- Output: Long format (composite_ID, Congruence, theta, SE)
- Transformation: Melt three theta columns into Congruence factor variable
- Row multiplication: 400 -> 1200 (x3 for three congruence types)

**Step 1 -> Step 2: Add Piecewise Structure**
- Input: Long format with Congruence factor
- Output: Long format with Segment and Days_within variables
- Transformation: Assign observations to Early/Late segments based on TSVR_hours, compute Days_within centered at segment start
- Row count: 1200 (unchanged)
- New columns: Segment, Days_within

**Step 2 -> Step 3: Extract Slopes from LMM**
- Input: Fitted LMM object (pickle)
- Output: Segment-specific slopes table (6 rows: 3 congruence x 2 segments)
- Transformation: Linear combination of fixed effects coefficients using delta method for SEs

**Step 3 -> Step 6: Aggregate for Plotting**
- Input: Segment slopes + observed data
- Output: Plot source CSVs (Early and Late panels)
- Transformation: Compute observed means, generate model predictions, merge for plotting

### Column Naming Conventions

**IRT Outputs (from RQ 5.5):**
- `theta_common`, `theta_congruent`, `theta_incongruent` (IRT ability estimates per congruence type)
- `se_common`, `se_congruent`, `se_incongruent` (standard errors)

**Piecewise LMM Variables:**
- `Segment` (factor: Early, Late)
- `Days_within` (numeric: time centered at segment start)
- `Congruence` (factor: Common, Congruent, Incongruent)
- `TSVR_hours` (numeric: actual time since VR encoding per Decision D070)

**LMM Outputs:**
- `Slope` (numeric: estimated slope in theta/day)
- `SE` (numeric: standard error of slope)
- `CI_lower`, `CI_upper` (numeric: 95% confidence interval bounds)
- `p_uncorrected`, `p_bonferroni` (numeric: dual p-values per Decision D068)

### Data Type Constraints

**Categorical Variables:**
- `Congruence`: String, must be in {Common, Congruent, Incongruent}
- `Segment`: String, must be in {Early, Late}
- `Data_Type`: String, must be in {Observed, Predicted}

**Numeric Variables:**
- `theta`: Float64, IRT ability estimates (nullable = FALSE)
- `SE`: Float64, standard errors (nullable = FALSE, must be positive)
- `TSVR_hours`: Float64, time variable (nullable = FALSE, must be non-negative)
- `Days_within`: Float64, centered time (nullable = FALSE)
- `p_uncorrected`, `p_bonferroni`: Float64, p-values (nullable = FALSE, range [0, 1] or [0, 15] for Bonferroni)

**ID Variables:**
- `UID`: String, participant identifier (format: P### with leading zeros)
- `composite_ID`: String, format {UID}_{test}
- `test`: String, must be in {T1, T2, T3, T4}

---

## Cross-RQ Dependencies

**Dependency Type:** DERIVED data from other RQ (RQ 5.5)

**This RQ requires outputs from:**
- **RQ 5.5** (Schema Congruence Effects on Forgetting)
  - File: results/ch5/rq5/data/step03_theta_scores.csv
  - Used in: Step 0 (extract theta scores by congruence)
  - Rationale: RQ 5.5 calibrated IRT models on "Items by Congruence" factor structure (Common/Congruent/Incongruent), producing theta estimates. This RQ uses those theta estimates as outcome variable for piecewise LMM, testing whether congruence effects differ between consolidation (Early segment) and decay (Late segment) phases.

**Execution Order Constraint:**
1. RQ 5.5 must complete Steps 1-3 first (IRT calibration, purification, theta extraction)
2. This RQ (RQ 5.6) executes second (uses RQ 5.5 theta scores)

**Data Source Boundaries (Per Best Practices Code.md):**
- **RAW data:** TSVR time variable from master.xlsx (actual hours since VR encoding)
- **DERIVED data:** Theta scores from RQ 5.5 (IRT ability estimates by congruence)
- **Scope:** This RQ does NOT re-calibrate IRT models (uses RQ 5.5 parameters as fixed input)

**Validation:**
- Step 0: Check results/ch5/rq5/status.yaml, verify rq_results.status = "success"
- Step 0: Check results/ch5/rq5/data/step03_theta_scores.csv exists
- If RQ 5.5 incomplete: QUIT with EXPECTATIONS ERROR "RQ 5.5 must complete before RQ 5.6 (DERIVED data dependency)"

**Reference:** Best Practices Code.md Section 2 (Data Source Boundaries)

---

## Validation Requirements

**CRITICAL MANDATE:**

Every analysis step in this plan MUST use validation tools after analysis tool execution.

This is not optional. This is the core architectural principle preventing cascading failures observed in v3.0 (where analysis errors propagated undetected through 5+ downstream steps before discovery).

**Exact Specification Requirement:**

> "Validation tools MUST be used after analysis tool execution"

**Implementation:**
- rq_tools (Step 11 workflow) will read tools_inventory.md validation tools section
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

**Step 0: Extract Theta Scores from RQ 5.5**
- **What Validation Checks:** RQ 5.5 status verification, file existence, schema validation (expected columns), value ranges (theta in [-3, 3], SE in [0.1, 1.0]), no missing data
- **Expected Behavior on Failure:** If RQ 5.5 incomplete or file missing -> QUIT with EXPECTATIONS ERROR, log details, master must run RQ 5.5 first

**Step 1: Prepare Piecewise LMM Input**
- **What Validation Checks:** Row count (1200 = 400 x 3), TSVR merge success (no missing values), segment assignment (Early = TSVR <= 24, Late = TSVR > 24), no segment overlap, Days_within centering (0 at segment start), all congruence types present
- **Expected Behavior on Failure:** If TSVR merge fails or segment overlap detected -> QUIT with EXPECTATIONS ERROR, log specific issue, g_debug investigates

**Step 2: Fit Piecewise LMM**
- **What Validation Checks:** Model convergence (no singular fit warnings, gradient norm < 0.01), all variance components > 0, no NaN coefficients, all 11 fixed effects present
- **Expected Behavior on Failure:** If convergence fails -> try simplified model (intercepts-only), log comparison, proceed with best-converged model. If both fail -> QUIT with EXPECTATIONS ERROR, g_debug investigates

**Step 3: Extract Segment-Specific Slopes**
- **What Validation Checks:** 6 rows present (3 congruence x 2 segments), delta method successful (no NaN SEs), CI ordering correct (CI_lower < Slope < CI_upper), slope interpretations consistent with sign
- **Expected Behavior on Failure:** If delta method fails or CI computation error -> QUIT with EXPECTATIONS ERROR, log which slope failed, g_debug investigates

**Step 4: Test Key Hypothesis**
- **What Validation Checks:** 11 hypothesis tests present, p-values in bounds [0, 1], Bonferroni correction applied correctly (p_bonferroni = p_uncorrected * 15), primary hypothesis (3-way interaction Congruent) present
- **Expected Behavior on Failure:** If p-values out of bounds or Bonferroni wrong -> QUIT with EXPECTATIONS ERROR, log computation error, g_debug investigates

**Step 5: Validate LMM Assumptions**
- **What Validation Checks:** All 6 assumption checks completed (residual normality, homoscedasticity, random effects normality, autocorrelation, outliers, multicollinearity), convergence diagnostics complete, all 7 sensitivity models fitted, diagnostic plots generated
- **Expected Behavior on Failure:** If assumption checks fail to compute -> QUIT with EXPECTATIONS ERROR, log which check failed, g_debug investigates. If assumptions violated statistically -> log warning, proceed cautiously (user may accept violations)

**Step 6: Prepare Plot Data**
- **What Validation Checks:** Two source CSVs created (Early and Late panels), expected row counts (~60 for Early, ~180 for Late), all congruence types present, CI ordering correct, no NaN in critical columns, predictions cover full Days_within range
- **Expected Behavior on Failure:** If aggregation fails or row counts wrong -> QUIT with EXPECTATIONS ERROR, log specific issue, g_debug investigates

**NOTE:** Technical validation (files exist, formats correct, values in bounds) checked by rq_inspect DURING analysis (Step 14 CODE EXECUTION LOOP). Scientific plausibility (effect directions, theoretical coherence) checked by rq_results AFTER all analysis complete (Step 16).

---

## Summary

**Total Steps:** 7 (Step 0: extraction + Steps 1-6: analysis and validation)

**Estimated Runtime:** Medium (~15-30 minutes total)
- Data extraction and preparation: 3-5 minutes (Steps 0-1)
- LMM fitting and hypothesis testing: 7-12 minutes (Steps 2-4)
- Assumption validation and sensitivity: 3-5 minutes (Step 5)
- Plot data preparation: 2-3 minutes (Step 6)

**Cross-RQ Dependencies:** RQ 5.5 must complete Steps 1-3 (theta extraction by congruence)

**Primary Outputs:**
- results/step02_lmm_model_summary.txt (piecewise LMM with 3-way interaction)
- results/step02_lmm_model.pkl (fitted model object)
- results/step03_segment_slopes.csv (6 slopes: 3 congruence x 2 segments)
- results/step04_hypothesis_tests.csv (11 hypothesis tests with dual p-values)
- results/step05_assumption_validation.txt (6 assumption checks)
- results/step05_convergence_diagnostics.txt (convergence status)
- results/step05_sensitivity_analyses.csv (7 models compared)
- plots/step06_piecewise_early_data.csv (Early segment plot source)
- plots/step06_piecewise_late_data.csv (Late segment plot source)

**Validation Coverage:** 100% (all 7 steps have validation requirements with 4-layer substance criteria)

**Key Hypothesis:** 3-way interaction Days_within:Segment[Late]:Congruence[Congruent] tests whether congruent items show less forgetting during Early consolidation window compared to Late decay phase (sleep consolidation theory prediction)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate in solution.md workflow)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_name.py scripts
5. Bash execution (Step 14): Run all 7 analysis steps with embedded validation
6. Step 15: rq_inspect validates all outputs match this plan's substance criteria
7. Step 16: rq_plots reads plot source CSVs, generates two-panel trajectory visualization
8. Step 17: rq_results synthesizes findings into results summary

---

**Version History:**
- v1.0 (2025-11-25): Initial plan created by rq_planner agent for RQ 5.6 (piecewise consolidation analysis)
