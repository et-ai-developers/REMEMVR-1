# Analysis Plan: RQ 5.3.5 - IRT-CTT Convergence for Paradigm-Specific Forgetting

**Research Question:** 5.3.5
**Created:** 2025-12-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines methodological convergence between IRT theta scores and CTT mean scores for paradigm-specific forgetting trajectories across three retrieval paradigms (Free Recall, Cued Recall, Recognition). The analysis validates whether findings from RQ 5.3.1 (paradigm-specific trajectories) are robust to measurement approach by comparing IRT vs CTT at three levels: (1) score-level correlations per paradigm, (2) parallel LMM trajectory models, and (3) fixed effect agreement metrics.

**Pipeline:** Convergence analysis (IRT vs CTT comparison)
**Steps:** 8 total analysis steps
**Estimated Runtime:** Medium (30-60 minutes total)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni/Holm correction for all hypothesis tests)
- Decision D070: TSVR as time variable (hours since encoding, not nominal days)
- Decision D039: CTT computed on purified item set from RQ 5.3.1 (fair comparison - same items)

**Data Dependencies:**
- RQ 5.3.1 must complete Steps 0-3 (IRT calibration, purification, final theta scores)
- Uses IRT theta scores, purified item list, and TSVR mapping from RQ 5.3.1
- Extracts raw responses from dfData.csv filtered to purified items for CTT computation

---

## Analysis Plan

This RQ requires 8 steps:

### Step 0: Load Dependencies from RQ 5.3.1

**Dependencies:** None (first step, but requires RQ 5.3.1 completion)
**Complexity:** Low (data loading and validation only)

**Purpose:** Load IRT theta scores, TSVR mapping, and purified item list from RQ 5.3.1 dependency. Verify all required files exist and contain expected data structure.

**Input:**

**File 1:** results/ch5/5.3.1/data/step03_theta_scores.csv
**Source:** RQ 5.3.1 Step 3 (IRT Pass 2 calibration)
**Format:** CSV, wide format (one row per composite_ID)
**Required Columns:**
  - `composite_ID` (string, format: UID_test, e.g., P001_T1)
  - `theta_IFR` (float, IRT ability estimate for Item Free Recall paradigm)
  - `theta_ICR` (float, IRT ability estimate for Item Cued Recall paradigm)
  - `theta_IRE` (float, IRT ability estimate for Item Recognition paradigm)
  - `se_IFR` (float, standard error for IFR theta)
  - `se_ICR` (float, standard error for ICR theta)
  - `se_IRE` (float, standard error for IRE theta)
**Expected Rows:** 400 (100 participants x 4 test sessions)

**File 2:** results/ch5/5.3.1/data/step00_tsvr_mapping.csv
**Source:** RQ 5.3.1 Step 0 (TSVR extraction)
**Format:** CSV, one row per composite_ID
**Required Columns:**
  - `composite_ID` (string, format: UID_test)
  - `UID` (string, participant identifier, format: P### with leading zeros)
  - `TEST` (string, test session identifier: T1, T2, T3, T4)
  - `TSVR_hours` (float, hours since VR encoding session)
  - `Days` (float, nominal days: 0, 1, 3, 6)
**Expected Rows:** 400

**File 3:** results/ch5/5.3.1/data/step02_purified_items.csv
**Source:** RQ 5.3.1 Step 2 (item purification per Decision D039)
**Format:** CSV, one row per retained item
**Required Columns:**
  - `item_name` (string, item tag from master.xlsx)
  - `paradigm` (string, paradigm factor: IFR, ICR, or IRE)
  - `dimension` (string, paradigm factor - same as paradigm column)
  - `a` (float, discrimination parameter from Pass 1 - informational only)
  - `b` (float, difficulty parameter from Pass 1 - informational only)
**Expected Rows:** 40-80 items (varies by purification outcome, minimum 10 items per paradigm required)

**File 4:** data/cache/dfData.csv
**Source:** Project-level raw data cache
**Format:** CSV, long format (one row per participant-test-item response)
**Required Columns:**
  - `UID` (string, participant identifier)
  - `TEST` (string, test session)
  - Item tag columns matching purified item names (binary 0/1 responses)
**Expected Volume:** ~40,000 rows (100 participants x 4 tests x ~100 items per test)

**Processing:**
1. Check that results/ch5/5.3.1/status.yaml shows rq_inspect: success (dependency completion verification)
2. Load theta_scores.csv, verify 400 rows with 7 columns (composite_ID + 3 theta + 3 se)
3. Load tsvr_mapping.csv, verify 400 rows with 5 columns
4. Load purified_items.csv, verify 40-80 rows with 5 columns
5. Count items per paradigm (IFR, ICR, IRE), verify >= 10 items each (minimum for stable IRT)
6. Verify composite_ID uniqueness across theta and TSVR files (no duplicates)
7. Read dfData.csv header, verify all purified item tags present as columns

**Output:**

**File 1:** data/step00_dependency_verification.txt
**Format:** Text report documenting dependency check results
**Content:**
  - RQ 5.3.1 completion status (from status.yaml)
  - Theta scores: 400 rows, 7 columns (composite_ID, theta_IFR/ICR/IRE, se_IFR/ICR/IRE)
  - TSVR mapping: 400 rows, 5 columns (composite_ID, UID, TEST, TSVR_hours, Days)
  - Purified items: N items (list counts per paradigm: IFR=X, ICR=Y, IRE=Z)
  - dfData.csv verified: All purified item tags present as columns
  - Dependency check: PASS (all files exist with expected structure)

**File 2:** data/step00_irt_theta.csv
**Format:** CSV, copy of theta scores for this RQ's analysis
**Columns:** Same as input (composite_ID, theta_IFR, theta_ICR, theta_IRE, se_IFR, se_ICR, se_IRE)
**Expected Rows:** 400

**File 3:** data/step00_tsvr_mapping.csv
**Format:** CSV, copy of TSVR mapping for this RQ's analysis
**Columns:** Same as input (composite_ID, UID, TEST, TSVR_hours, Days)
**Expected Rows:** 400

**File 4:** data/step00_purified_items.csv
**Format:** CSV, copy of purified item list for this RQ's analysis
**Columns:** Same as input (item_name, paradigm, dimension, a, b)
**Expected Rows:** 40-80 items

**Validation Requirement:**
Validation tools MUST be used after dependency loading. Specific validation tools will be determined by rq_tools based on file existence and structure checks. The rq_analysis agent will embed validation tool calls after the data loading tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_verification.txt exists (exact path)
- data/step00_irt_theta.csv: 400 rows x 7 columns (composite_ID: object, theta columns: float64, se columns: float64)
- data/step00_tsvr_mapping.csv: 400 rows x 5 columns (composite_ID: object, UID: object, TEST: object, TSVR_hours: float64, Days: float64)
- data/step00_purified_items.csv: 40-80 rows x 5 columns (item_name: object, paradigm: object, dimension: object, a: float64, b: float64)

*Value Ranges:*
- theta_IFR, theta_ICR, theta_IRE in [-4, 4] (typical IRT ability range with buffer for extremes)
- se_IFR, se_ICR, se_IRE in [0.1, 1.5] (standard errors - above 1.5 indicates unreliable estimates)
- TSVR_hours in [0, 200] hours (0=encoding, 200=~8 days buffer beyond Day 6)
- Days in [0, 1, 3, 6] (nominal test days - exact match required)
- Item counts per paradigm >= 10 (minimum for stable IRT calibration)

*Data Quality:*
- No NaN values in theta scores (model must estimate for all 400 observations)
- No NaN values in TSVR mapping (all sessions must have timing data)
- All 400 composite_IDs present in both theta and TSVR files (complete data)
- No duplicate composite_IDs (uniqueness constraint)
- Purified items: paradigm in {IFR, ICR, IRE} only (no other paradigms)
- All purified item tags present in dfData.csv header (data extraction feasibility verified)

*Log Validation:*
- Required pattern: "Dependency check: PASS"
- Required pattern: "IFR items: [10-40], ICR items: [10-40], IRE items: [10-40]"
- Required pattern: "All 400 composite_IDs matched between theta and TSVR"
- Forbidden patterns: "ERROR", "Dependency check: FAIL", "Missing items in dfData"
- Acceptable warnings: None expected for data loading

**Expected Behavior on Validation Failure:**
- If RQ 5.3.1 not complete: Raise error "EXPECTATIONS ERROR: RQ 5.3.1 must complete before RQ 5.3.5 (dependency)"
- If files missing: Raise error "EXPECTATIONS ERROR: Missing required file from RQ 5.3.1: [filename]"
- If row counts wrong: Raise error "STEP ERROR: Expected 400 rows in theta_scores.csv, found [N]"
- If item counts < 10 per paradigm: Raise error "CLARITY ERROR: Insufficient items for paradigm [X]: only [N] items (need >= 10)"
- Log failure to logs/step00_load_dependencies.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause (likely RQ 5.3.1 incomplete or purification too aggressive)

---

### Step 1: Compute CTT Mean Scores per Paradigm

**Dependencies:** Step 0 (requires purified item list and composite_ID structure)
**Complexity:** Medium (data extraction and aggregation across ~40-80 items)

**Purpose:** Compute Classical Test Theory (CTT) mean scores as proportion correct for each participant-test-paradigm combination using the purified item set from RQ 5.3.1. This ensures fair IRT-CTT comparison (same items for both measurement approaches).

**Input:**

**File 1:** data/step00_purified_items.csv (from Step 0)
**Columns:** item_name, paradigm, dimension, a, b
**Expected Rows:** 40-80 items

**File 2:** data/step00_tsvr_mapping.csv (from Step 0)
**Columns:** composite_ID, UID, TEST, TSVR_hours, Days
**Expected Rows:** 400

**File 3:** data/cache/dfData.csv (project-level raw data)
**Format:** Long format with binary item responses (0=incorrect, 1=correct)
**Required:** Item tag columns matching purified item names

**Processing:**
1. Read dfData.csv, filter to UID-TEST combinations present in TSVR mapping (100 participants x 4 tests = 400 observations)
2. For each paradigm (IFR, ICR, IRE):
   - Extract item tags from purified_items.csv where paradigm = [IFR/ICR/IRE]
   - Select corresponding item columns from dfData.csv
   - Compute row-wise mean across selected items (proportion correct per participant-test)
   - Handle missing responses: exclude NaN values from mean calculation (use available items only)
3. Create long-format output: one row per participant-test-paradigm combination (1200 rows: 400 x 3 paradigms)
4. Merge with composite_ID and paradigm labels for downstream analysis

**Output:**

**File 1:** data/step01_ctt_scores.csv
**Format:** CSV, long format (one row per participant-test-paradigm combination)
**Columns:**
  - `composite_ID` (string, format: UID_test, e.g., P001_T1)
  - `UID` (string, participant identifier)
  - `TEST` (string, test session: T1, T2, T3, T4)
  - `paradigm` (string, paradigm factor: IFR, ICR, or IRE)
  - `CTT_mean` (float, proportion correct: 0 to 1 scale)
  - `n_items` (int, number of items with valid responses for this paradigm - varies if missing data)
**Expected Rows:** 1200 (100 participants x 4 tests x 3 paradigms)

**File 2:** data/step01_ctt_computation_report.txt
**Format:** Text report documenting CTT computation details
**Content:**
  - Items per paradigm used (IFR: X items, ICR: Y items, IRE: Z items)
  - Missing response summary (% NaN per paradigm, median items available per observation)
  - CTT mean score descriptives per paradigm (mean, SD, min, max, N)
  - Participants with complete data (no missing responses): N (target: most participants should be complete)

**Validation Requirement:**
Validation tools MUST be used after CTT computation. Specific validation tools will be determined by rq_tools based on proportion correct calculation and data completeness checks. The rq_analysis agent will embed validation tool calls after the CTT computation tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_ctt_scores.csv exists (exact path)
- Expected rows: 1200 (100 participants x 4 tests x 3 paradigms)
- Expected columns: 6 (composite_ID, UID, TEST, paradigm, CTT_mean, n_items)
- Data types: composite_ID (object), UID (object), TEST (object), paradigm (object), CTT_mean (float64), n_items (int64)

*Value Ranges:*
- CTT_mean in [0, 1] (proportion correct - cannot exceed bounds)
- n_items >= 5 per observation (minimum items for stable mean - most should have >= 10)
- paradigm in {IFR, ICR, IRE} (categorical - no other values)
- TEST in {T1, T2, T3, T4} (categorical - exact match required)

*Data Quality:*
- No NaN values in CTT_mean (all 1200 observations must have valid proportion correct)
- No NaN values in n_items (all observations must report item count)
- Expected N: Exactly 1200 rows (100 participants x 4 tests x 3 paradigms - no missing combinations)
- Duplicate check: No duplicate composite_ID x paradigm combinations (uniqueness constraint)
- Distribution check: CTT_mean approximately normal per paradigm (or at least not degenerate - avoid floor/ceiling effects)

*Log Validation:*
- Required pattern: "CTT computation complete: 1200 scores created (400 x 3 paradigms)"
- Required pattern: "All paradigms represented: IFR, ICR, IRE"
- Required pattern: "No NaN values in CTT_mean column"
- Forbidden patterns: "ERROR", "NaN values detected in CTT_mean", "Missing paradigm"
- Acceptable warnings: "Some participants have missing item responses (<5% expected)" (acceptable if median n_items still high)

**Expected Behavior on Validation Failure:**
- If CTT_mean contains NaN: Raise error "STEP ERROR: NaN values detected in CTT_mean - check raw data completeness"
- If n_items < 5 for any observation: Raise error "CLARITY ERROR: Insufficient items for stable CTT mean - participant [UID] test [TEST] paradigm [paradigm] has only [N] items"
- If row count != 1200: Raise error "STEP ERROR: Expected 1200 rows, found [N] - missing paradigm combinations"
- Log failure to logs/step01_compute_ctt_scores.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose root cause (likely dfData.csv missing responses or paradigm assignment error)

---

### Step 2: Compute Pearson Correlations (IRT vs CTT per Paradigm)

**Dependencies:** Step 0 (IRT theta), Step 1 (CTT scores)
**Complexity:** Low (correlation computation and hypothesis testing)

**Purpose:** Compute Pearson correlations between IRT theta and CTT mean scores separately for each paradigm (IFR, ICR, IRE) plus overall correlation across all paradigms. Test correlation strength against convergence thresholds (r > 0.70 strong, r > 0.90 exceptional) with Holm-Bonferroni correction for 4 tests.

**Input:**

**File 1:** data/step00_irt_theta.csv (from Step 0)
**Columns:** composite_ID, theta_IFR, theta_ICR, theta_IRE, se_IFR, se_ICR, se_IRE
**Expected Rows:** 400

**File 2:** data/step01_ctt_scores.csv (from Step 1)
**Columns:** composite_ID, UID, TEST, paradigm, CTT_mean, n_items
**Expected Rows:** 1200 (long format)

**Processing:**
1. Reshape CTT scores from long to wide format: pivot on paradigm to create CTT_IFR, CTT_ICR, CTT_IRE columns (400 rows: one per composite_ID)
2. Merge IRT theta (wide) with CTT (wide) on composite_ID (inner join - all 400 should match)
3. Compute Pearson correlations:
   - r_IFR: correlation(theta_IFR, CTT_IFR) for 400 observations
   - r_ICR: correlation(theta_ICR, CTT_ICR) for 400 observations
   - r_IRE: correlation(theta_IRE, CTT_IRE) for 400 observations
   - r_overall: correlation across all 1200 observations (stack theta and CTT for all paradigms)
4. Compute p-values for each correlation (two-tailed test: H0: r = 0)
5. Apply Holm-Bonferroni correction for 4 tests (3 paradigms + overall):
   - Sort p-values ascending
   - Adjusted alpha: p_adj[i] = alpha / (k - i + 1) where k=4, alpha=0.05
   - p_bonferroni = min(p_uncorrected x (4 - rank + 1), 1.0)
6. Classify convergence strength per threshold:
   - Strong convergence: r > 0.70 (threshold from psychometric literature)
   - Exceptional convergence: r > 0.90 (near-identical rank ordering)
7. Report dual p-values per Decision D068 (p_uncorrected and p_bonferroni)

**Output:**

**File 1:** data/step02_correlations.csv
**Format:** CSV, one row per correlation test (4 rows: IFR, ICR, IRE, Overall)
**Columns:**
  - `paradigm` (string: IFR, ICR, IRE, Overall)
  - `n` (int, sample size for correlation: 400 for paradigm-specific, 1200 for overall)
  - `r` (float, Pearson correlation coefficient: -1 to 1)
  - `p_uncorrected` (float, uncorrected p-value: 0 to 1)
  - `p_bonferroni` (float, Holm-Bonferroni corrected p-value: 0 to 1)
  - `threshold_0.70` (bool, TRUE if r > 0.70 - strong convergence)
  - `threshold_0.90` (bool, TRUE if r > 0.90 - exceptional convergence)
  - `interpretation` (string, qualitative interpretation: "Weak", "Moderate", "Strong", "Exceptional")
**Expected Rows:** 4

**File 2:** data/step02_merged_irt_ctt.csv
**Format:** CSV, wide format with both IRT and CTT scores for downstream analysis
**Columns:**
  - `composite_ID` (string)
  - `UID` (string)
  - `TEST` (string)
  - `theta_IFR`, `theta_ICR`, `theta_IRE` (float, IRT ability estimates)
  - `CTT_IFR`, `CTT_ICR`, `CTT_IRE` (float, CTT proportion correct)
  - `se_IFR`, `se_ICR`, `se_IRE` (float, IRT standard errors)
**Expected Rows:** 400

**Validation Requirement:**
Validation tools MUST be used after correlation computation. Specific validation tools will be determined by rq_tools based on correlation calculation and p-value correction checks. The rq_analysis agent will embed validation tool calls after the correlation analysis tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_correlations.csv exists (exact path)
- Expected rows: 4 (3 paradigms + overall)
- Expected columns: 8 (paradigm, n, r, p_uncorrected, p_bonferroni, threshold_0.70, threshold_0.90, interpretation)
- Data types: paradigm (object), n (int64), r (float64), p columns (float64), threshold columns (bool), interpretation (object)

*Value Ranges:*
- r in [-1, 1] (correlation bounds - cannot exceed)
- p_uncorrected in [0, 1] (p-value bounds)
- p_bonferroni in [0, 1] (corrected p-value bounds)
- p_bonferroni >= p_uncorrected (correction never reduces p-value - mathematical constraint)
- n in {400, 1200} (sample sizes - 400 for paradigm-specific, 1200 for overall)
- Expected r > 0.50 for all (moderate to strong convergence expected - measurement of same construct)

*Data Quality:*
- No NaN values in any column (all correlations must compute successfully)
- Expected N: Exactly 4 rows (no more, no less)
- No duplicate paradigm labels (uniqueness constraint)
- Distribution check: At least 3/4 correlations should meet r > 0.70 threshold (strong convergence expected)
- Interpretation column matches r thresholds: r > 0.90 -> "Exceptional", r > 0.70 -> "Strong", r > 0.50 -> "Moderate", r <= 0.50 -> "Weak"

*Log Validation:*
- Required pattern: "Correlations computed: 4 tests (IFR, ICR, IRE, Overall)"
- Required pattern: "Holm-Bonferroni correction applied (4 tests, alpha=0.05)"
- Required pattern: "Strong convergence (r > 0.70): [N]/4 tests"
- Forbidden patterns: "ERROR", "NaN correlation", "p_bonferroni < p_uncorrected" (mathematical impossibility)
- Acceptable warnings: "Correlation below strong threshold (r < 0.70) for paradigm [X]" (would indicate poor convergence but not error)

**Expected Behavior on Validation Failure:**
- If any correlation NaN: Raise error "STEP ERROR: NaN correlation detected for paradigm [X] - check data completeness"
- If p_bonferroni < p_uncorrected: Raise error "TOOL ERROR: Bonferroni correction error - corrected p-value less than uncorrected (impossible)"
- If row count != 4: Raise error "STEP ERROR: Expected 4 rows, found [N] - missing paradigm correlations"
- If r < 0.50 for >1 paradigm: Raise error "CLARITY ERROR: Weak convergence detected (r < 0.50) for [N] paradigms - measurement validity concern"
- Log failure to logs/step02_compute_correlations.log
- Quit script immediately (do NOT proceed to Step 3)
- g_debug invoked to diagnose root cause (likely data quality issue or IRT-CTT measuring different constructs)

---

### Step 3: Fit Parallel LMMs (IRT vs CTT)

**Dependencies:** Step 2 (merged IRT-CTT data), data/step00_tsvr_mapping.csv
**Complexity:** High (LMM fitting with random effects - 30-60 minutes for convergence)

**Purpose:** Fit parallel Linear Mixed Models using identical model formula for IRT theta vs CTT mean scores. Model formula determined by best-fitting model from RQ 5.3.1 (likely includes Paradigm x Time interactions with random slopes). If either model fails to converge, simplify both models equally to maintain structural equivalence.

**Input:**

**File 1:** data/step02_merged_irt_ctt.csv (from Step 2)
**Columns:** composite_ID, UID, TEST, theta_IFR/ICR/IRE, CTT_IFR/ICR/IRE, se_IFR/ICR/IRE
**Expected Rows:** 400

**File 2:** data/step00_tsvr_mapping.csv (from Step 0)
**Columns:** composite_ID, UID, TEST, TSVR_hours, Days
**Expected Rows:** 400

**File 3:** results/ch5/5.3.1/data/step05_lmm_model_comparison.csv (RQ 5.3.1 model selection results)
**Source:** RQ 5.3.1 Step 5 (best model identification)
**Format:** CSV listing 5 candidate models with AIC/BIC
**Purpose:** Determine which functional form to use (Linear, Quadratic, Log, Lin+Log, Quad+Log)

**Processing:**
1. Read RQ 5.3.1 model comparison results, identify best-fitting model (lowest AIC)
2. Construct identical LMM formula for both IRT and CTT based on best model from RQ 5.3.1:
   - Independent variable: TSVR_hours (Decision D070 - actual hours, not nominal days)
   - Fixed effects: Paradigm (IFR/ICR/IRE) x Time transformation (from best model)
   - Random effects: (Time | UID) - random intercepts and slopes by participant
   - REML: False (for AIC comparison later in Step 6)
3. Reshape merged data from wide to long format (1200 rows: 400 x 3 paradigms):
   - IRT long: composite_ID, UID, TEST, TSVR_hours, paradigm, theta
   - CTT long: composite_ID, UID, TEST, TSVR_hours, paradigm, CTT_mean
4. Attempt to fit IRT model using formula from Step 2
5. Attempt to fit CTT model using SAME formula
6. Convergence handling (simplification if needed):
   - If BOTH converge: Proceed with full random slopes model
   - If EITHER fails: Simplify BOTH to random intercepts only: (1 | UID)
   - If BOTH still fail: Simplify BOTH to fixed effects only (no random effects)
   - Log all simplifications and convergence warnings
7. Extract model summaries for both final models (fixed effects, random effects, fit indices)

**Output:**

**File 1:** data/step03_irt_lmm_input.csv
**Format:** CSV, long format for IRT model fitting
**Columns:**
  - `composite_ID` (string)
  - `UID` (string)
  - `TEST` (string)
  - `TSVR_hours` (float, time variable per Decision D070)
  - `paradigm` (string: IFR, ICR, IRE)
  - `theta` (float, IRT ability estimate)
  - Time transformation columns (e.g., `Time_log`, `Time_squared` depending on best model from RQ 5.3.1)
**Expected Rows:** 1200

**File 2:** data/step03_ctt_lmm_input.csv
**Format:** CSV, long format for CTT model fitting (identical structure to IRT input)
**Columns:** Same as IRT input but `CTT_mean` instead of `theta`
**Expected Rows:** 1200

**File 3:** data/step03_irt_lmm_model.pkl
**Format:** Pickle file containing fitted statsmodels MixedLM object (IRT model)
**Content:** Fitted model object for downstream extraction and comparison

**File 4:** data/step03_ctt_lmm_model.pkl
**Format:** Pickle file containing fitted statsmodels MixedLM object (CTT model)
**Content:** Fitted model object for downstream extraction and comparison

**File 5:** data/step03_irt_lmm_summary.txt
**Format:** Text file with IRT model summary
**Content:**
  - Model formula used (fixed effects + random effects)
  - Convergence status (TRUE/FALSE with warnings if applicable)
  - Fixed effects table (coefficient, SE, z, p)
  - Random effects variance components
  - Model fit indices (AIC, BIC, log-likelihood)
  - Sample size (N observations, N groups)

**File 6:** data/step03_ctt_lmm_summary.txt
**Format:** Text file with CTT model summary (same structure as IRT summary)

**File 7:** data/step03_model_convergence_log.txt
**Format:** Text file documenting convergence attempts and simplifications
**Content:**
  - Model formula attempted (full random slopes)
  - IRT convergence status: PASS/FAIL
  - CTT convergence status: PASS/FAIL
  - Simplifications applied (if any): None / Random intercepts only / Fixed effects only
  - Final model structure used for both IRT and CTT
  - Rationale: "Both models converge with identical structure" OR "Simplified to maintain structural equivalence"

**Validation Requirement:**
Validation tools MUST be used after LMM fitting. Specific validation tools will be determined by rq_tools based on model convergence and fit quality checks. The rq_analysis agent will embed validation tool calls after the LMM fitting tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_irt_lmm_input.csv: 1200 rows x 7+ columns (composite_ID, UID, TEST, TSVR_hours, paradigm, theta, time transformations)
- data/step03_ctt_lmm_input.csv: 1200 rows x 7+ columns (same structure, CTT_mean instead of theta)
- data/step03_irt_lmm_model.pkl exists (binary file - check size > 1KB)
- data/step03_ctt_lmm_model.pkl exists (binary file - check size > 1KB)
- data/step03_irt_lmm_summary.txt exists (text file - check contains "Converged: TRUE" or simplification note)
- data/step03_ctt_lmm_summary.txt exists (text file - same convergence status as IRT)
- data/step03_model_convergence_log.txt exists

*Value Ranges:*
- TSVR_hours in [0, 200] (time variable bounds)
- theta in [-4, 4] (IRT ability range)
- CTT_mean in [0, 1] (proportion correct range)
- Fixed effect coefficients: typically in [-2, 2] for standardized models (extreme values suggest overfitting)
- Random effect variances > 0 (variance must be positive - negative indicates convergence failure)

*Data Quality:*
- No NaN values in theta or CTT_mean (all 1200 observations valid)
- Both models must have IDENTICAL convergence status (either both converge or both simplified)
- Both models must have IDENTICAL random structure (structural equivalence requirement)
- Expected N: 1200 rows in both input files, 100 groups (participants) in both models
- Convergence log must document simplifications if applied (transparency requirement)

*Log Validation:*
- Required pattern: "IRT model convergence: [TRUE/FALSE]"
- Required pattern: "CTT model convergence: [TRUE/FALSE]"
- Required pattern: "Structural equivalence: [MAINTAINED/SIMPLIFIED]"
- Required pattern: "Final random structure: [(Time | UID) / (1 | UID) / None]"
- Forbidden patterns: "ERROR", "IRT converged but CTT failed" (must be equal), "Negative variance" (impossible)
- Acceptable warnings: "Model simplified to random intercepts only" (acceptable if both simplified equally)

**Expected Behavior on Validation Failure:**
- If IRT converges but CTT fails (or vice versa): Raise error "STEP ERROR: Structural equivalence violated - IRT and CTT models must have identical structure"
- If both models fail to converge even after simplification to fixed effects only: Raise error "STEP ERROR: Both models failed to converge even with no random effects - data quality issue"
- If negative variance components detected: Raise error "TOOL ERROR: Negative variance detected - model convergence failure"
- If row counts != 1200: Raise error "STEP ERROR: Expected 1200 rows in LMM input, found [N]"
- Log failure to logs/step03_fit_parallel_lmms.log
- Quit script immediately (do NOT proceed to Step 4)
- g_debug invoked to diagnose root cause (likely model misspecification or insufficient data for random effects)

---

### Step 4: Validate LMM Assumptions

**Dependencies:** Step 3 (fitted LMM models)
**Complexity:** Medium (7 diagnostic tests per model - 15-30 minutes)

**Purpose:** Validate LMM assumptions for both IRT and CTT models: (1) linearity, (2) normality of residuals, (3) homoscedasticity, (4) independence of residuals, (5) normality of random effects, (6) absence of influential outliers. Document assumption violations and compare violation patterns across IRT vs CTT.

**Input:**

**File 1:** data/step03_irt_lmm_model.pkl (from Step 3)
**Content:** Fitted IRT model object

**File 2:** data/step03_ctt_lmm_model.pkl (from Step 3)
**Content:** Fitted CTT model object

**File 3:** data/step03_irt_lmm_input.csv (from Step 3)
**Columns:** Input data for IRT model (1200 rows)

**File 4:** data/step03_ctt_lmm_input.csv (from Step 3)
**Columns:** Input data for CTT model (1200 rows)

**Processing:**
1. Load both fitted models and input data
2. For EACH model (IRT and CTT), run 7 diagnostic tests:
   - **Linearity:** Residuals vs fitted values plot (pattern check - no U-shape or curvature)
   - **Normality of residuals:** Kolmogorov-Smirnov test (p > 0.05 indicates normality)
   - **Homoscedasticity:** Residuals vs fitted values variance (Levene's test or visual check - constant spread)
   - **Independence:** Autocorrelation function (ACF) of residuals (lag-1 ACF < 0.2 acceptable)
   - **Normality of random effects:** Q-Q plot for random intercepts and slopes (visual check + Shapiro-Wilk test)
   - **Influential outliers:** Cook's distance (values > 1.0 indicate influential points)
   - **Overall convergence:** Verify model.converged = TRUE (redundant with Step 3 but documented here)
3. Compare assumption violation patterns across IRT vs CTT:
   - Do both models show same violations (e.g., both non-normal residuals)?
   - Do violations differ (e.g., IRT normal but CTT skewed)?
4. Create diagnostic plots for both models (saved as plot data CSVs, actual PNGs created by rq_plots later)

**Output:**

**File 1:** data/step04_irt_assumptions.csv
**Format:** CSV, one row per diagnostic test
**Columns:**
  - `test_name` (string: Linearity, Normality_Residuals, Homoscedasticity, Independence, Normality_RE, Outliers, Convergence)
  - `statistic` (float, test statistic if applicable - e.g., KS statistic, ACF lag-1)
  - `p_value` (float, p-value if applicable - NA for visual tests)
  - `threshold` (float, acceptance threshold - e.g., p > 0.05 for normality)
  - `result` (string: PASS / FAIL / WARNING)
  - `interpretation` (string, brief qualitative interpretation)
**Expected Rows:** 7 (one per diagnostic test)

**File 2:** data/step04_ctt_assumptions.csv
**Format:** Same structure as IRT assumptions (7 rows)

**File 3:** data/step04_assumptions_comparison.csv
**Format:** CSV comparing violation patterns across IRT vs CTT
**Columns:**
  - `test_name` (string, diagnostic test)
  - `irt_result` (string: PASS/FAIL/WARNING)
  - `ctt_result` (string: PASS/FAIL/WARNING)
  - `agreement` (bool, TRUE if both have same result)
  - `interpretation` (string, comparative interpretation)
**Expected Rows:** 7

**File 4:** data/step04_irt_diagnostics_data.csv
**Format:** CSV with residuals and fitted values for IRT model diagnostic plotting
**Columns:**
  - `fitted` (float, fitted values from model)
  - `residuals` (float, residuals from model)
  - `standardized_residuals` (float, standardized residuals)
  - `observation_index` (int, row index for Cook's distance)
  - `cooks_distance` (float, Cook's distance for outlier detection)
**Expected Rows:** 1200

**File 5:** data/step04_ctt_diagnostics_data.csv
**Format:** Same structure as IRT diagnostics (1200 rows)

**Validation Requirement:**
Validation tools MUST be used after assumption checking. Specific validation tools will be determined by rq_tools based on diagnostic test execution and result interpretation. The rq_analysis agent will embed validation tool calls after the assumption validation tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_irt_assumptions.csv: 7 rows x 6 columns (test_name, statistic, p_value, threshold, result, interpretation)
- data/step04_ctt_assumptions.csv: 7 rows x 6 columns (same structure)
- data/step04_assumptions_comparison.csv: 7 rows x 5 columns (test_name, irt_result, ctt_result, agreement, interpretation)
- data/step04_irt_diagnostics_data.csv: 1200 rows x 5 columns (fitted, residuals, standardized_residuals, observation_index, cooks_distance)
- data/step04_ctt_diagnostics_data.csv: 1200 rows x 5 columns (same structure)

*Value Ranges:*
- p_value in [0, 1] (p-value bounds)
- result in {PASS, FAIL, WARNING} (categorical - exact match required)
- standardized_residuals approximately in [-3, 3] (most should fall within 3 SD)
- cooks_distance typically < 1.0 (values > 1.0 indicate influential outliers)
- ACF lag-1 typically in [-0.3, 0.3] (autocorrelation bounds - values > 0.3 indicate strong autocorrelation concern)

*Data Quality:*
- No NaN values in statistic or p_value columns (all tests must execute successfully unless NA by design)
- Expected N: Exactly 7 rows in each assumptions file
- Result column: At least 5/7 tests should PASS for acceptable model (some violations tolerable)
- Diagnostics data: Exactly 1200 rows (one per observation)
- Cook's distance: <5% of observations should exceed 1.0 (occasional outliers acceptable)

*Log Validation:*
- Required pattern: "Assumption validation complete: 7 tests run for IRT model"
- Required pattern: "Assumption validation complete: 7 tests run for CTT model"
- Required pattern: "Overall assessment: [N]/7 tests PASS for IRT, [M]/7 tests PASS for CTT"
- Forbidden patterns: "ERROR", "Test execution failed", "NaN in critical diagnostic"
- Acceptable warnings: "WARNING: Normality assumption violated for residuals (KS p = [X])" (some violations acceptable for large N)

**Expected Behavior on Validation Failure:**
- If row count != 7: Raise error "STEP ERROR: Expected 7 diagnostic tests, found [N] - missing tests"
- If any critical test fails to execute: Raise error "TOOL ERROR: Diagnostic test [name] failed to execute - check model object"
- If >3 tests FAIL for either model: Raise error "CLARITY ERROR: Multiple assumption violations detected ([N]/7 FAIL) - model validity concern"
- If Cook's distance > 1.0 for >10% of observations: Raise error "STEP ERROR: Excessive influential outliers detected ([N]% exceed Cook's distance = 1.0)"
- Log failure to logs/step04_validate_lmm_assumptions.log
- Quit script immediately (do NOT proceed to Step 5)
- g_debug invoked to diagnose root cause (likely model misspecification, outliers, or non-linear relationships)

---

### Step 5: Compare Fixed Effects (IRT vs CTT)

**Dependencies:** Step 3 (fitted models)
**Complexity:** Medium (coefficient extraction and agreement metrics - 15-30 minutes)

**Purpose:** Compare fixed effects between IRT and CTT models. Extract all fixed effect coefficients with standard errors, z-values, and p-values. Classify each effect as significant (p < 0.05) or non-significant. Compute Cohen's kappa for agreement on significance classifications (threshold: kappa > 0.60 indicates substantial agreement). Compute percentage agreement. Report dual p-values per Decision D068.

**Input:**

**File 1:** data/step03_irt_lmm_model.pkl (from Step 3)
**Content:** Fitted IRT model object

**File 2:** data/step03_ctt_lmm_model.pkl (from Step 3)
**Content:** Fitted CTT model object

**Processing:**
1. Load both fitted models
2. Extract fixed effects tables from both models:
   - IRT fixed effects: all terms (Intercept, Paradigm effects, Time effects, Paradigm x Time interactions)
   - CTT fixed effects: same terms (identical formula per Step 3)
3. For EACH model:
   - Extract coefficient, SE, z-value, p-value per fixed effect term
   - Classify significance: sig = TRUE if p < 0.05, sig = FALSE otherwise
   - Apply Bonferroni correction for multiple testing: p_bonferroni = min(p_uncorrected x k, 1.0) where k = number of fixed effects
4. Merge IRT and CTT fixed effects on term name (should be 1:1 match due to identical formula)
5. Compute agreement metrics:
   - **Cohen's kappa:** Agreement on significance classification (sig = TRUE/FALSE) beyond chance
   - **Percentage agreement:** Simple proportion of terms where IRT and CTT agree on significance
   - **Kappa interpretation:** < 0.40 = Poor, 0.40-0.60 = Moderate, 0.60-0.80 = Substantial, > 0.80 = Almost perfect
6. Report dual p-values per Decision D068 (p_uncorrected and p_bonferroni for ALL fixed effects)

**Output:**

**File 1:** data/step05_irt_fixed_effects.csv
**Format:** CSV, one row per fixed effect term
**Columns:**
  - `term` (string, fixed effect name: Intercept, paradigm[IFR], paradigm[ICR], Time, paradigm[IFR]:Time, etc.)
  - `coef` (float, coefficient estimate)
  - `se` (float, standard error)
  - `z` (float, z-statistic)
  - `p_uncorrected` (float, uncorrected p-value)
  - `p_bonferroni` (float, Bonferroni-corrected p-value per Decision D068)
  - `sig` (bool, TRUE if p_uncorrected < 0.05)
**Expected Rows:** 6-12 (depends on best model from RQ 5.3.1 - at least Intercept + 2 Paradigm main effects + Time + 2 Paradigm x Time interactions)

**File 2:** data/step05_ctt_fixed_effects.csv
**Format:** Same structure as IRT fixed effects (same number of rows)

**File 3:** data/step05_coefficient_comparison.csv
**Format:** CSV comparing IRT vs CTT fixed effects side-by-side
**Columns:**
  - `term` (string, fixed effect name)
  - `IRT_coef` (float, IRT coefficient)
  - `IRT_se` (float, IRT standard error)
  - `IRT_z` (float, IRT z-statistic)
  - `IRT_p_uncorrected` (float, IRT uncorrected p-value)
  - `IRT_p_bonferroni` (float, IRT Bonferroni p-value)
  - `IRT_sig` (bool, IRT significance classification)
  - `CTT_coef` (float, CTT coefficient)
  - `CTT_se` (float, CTT standard error)
  - `CTT_z` (float, CTT z-statistic)
  - `CTT_p_uncorrected` (float, CTT uncorrected p-value)
  - `CTT_p_bonferroni` (float, CTT Bonferroni p-value)
  - `CTT_sig` (bool, CTT significance classification)
  - `agreement` (bool, TRUE if IRT_sig == CTT_sig)
**Expected Rows:** 6-12 (same as fixed effects count)

**File 4:** data/step05_agreement_metrics.csv
**Format:** CSV with agreement summary statistics
**Columns:**
  - `metric` (string: Cohens_kappa, Percentage_agreement, Kappa_interpretation)
  - `value` (float, metric value)
  - `threshold` (float, threshold for interpretation - kappa > 0.60 for substantial agreement)
  - `result` (string: PASS / FAIL based on threshold)
  - `interpretation` (string, qualitative interpretation)
**Expected Rows:** 3

**Validation Requirement:**
Validation tools MUST be used after fixed effects comparison. Specific validation tools will be determined by rq_tools based on coefficient extraction and agreement metric calculation. The rq_analysis agent will embed validation tool calls after the coefficient comparison tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_irt_fixed_effects.csv: 6-12 rows x 7 columns (term, coef, se, z, p_uncorrected, p_bonferroni, sig)
- data/step05_ctt_fixed_effects.csv: 6-12 rows x 7 columns (same structure, same row count as IRT)
- data/step05_coefficient_comparison.csv: 6-12 rows x 14 columns (term, IRT_*, CTT_*, agreement)
- data/step05_agreement_metrics.csv: 3 rows x 5 columns (metric, value, threshold, result, interpretation)

*Value Ranges:*
- coef typically in [-3, 3] for standardized models (extreme values > 5 suggest estimation error)
- se > 0 (standard errors must be positive - negative or zero indicates error)
- z typically in [-5, 5] (extreme z-values > 10 rare but possible for strong effects)
- p_uncorrected in [0, 1] (p-value bounds)
- p_bonferroni in [0, 1] (corrected p-value bounds)
- p_bonferroni >= p_uncorrected (correction never reduces p-value - mathematical constraint)
- Cohens_kappa in [-1, 1] (kappa bounds - negative indicates worse than chance, positive indicates agreement)
- Percentage_agreement in [0, 1] (proportion bounds)

*Data Quality:*
- No NaN values in coefficient, se, z, or p-value columns (all terms must have valid estimates)
- IRT and CTT row counts MUST match (identical formula requirement)
- All term names must match between IRT and CTT (structural equivalence verification)
- Expected kappa > 0.60 (substantial agreement threshold per hypothesis)
- Expected percentage agreement >= 0.80 (80% agreement threshold per hypothesis)
- Dual p-values present for ALL terms per Decision D068

*Log Validation:*
- Required pattern: "Fixed effects extracted: [N] terms for IRT model"
- Required pattern: "Fixed effects extracted: [N] terms for CTT model"
- Required pattern: "Agreement metrics: Cohen's kappa = [X], Percentage agreement = [Y]"
- Required pattern: "Dual p-values reported per Decision D068"
- Forbidden patterns: "ERROR", "NaN coefficient", "p_bonferroni < p_uncorrected", "Term mismatch between IRT and CTT"
- Acceptable warnings: "Low kappa (< 0.60) indicates poor agreement" (would fail hypothesis but not analysis)

**Expected Behavior on Validation Failure:**
- If row counts differ: Raise error "STEP ERROR: IRT has [N] terms but CTT has [M] terms - structural equivalence violated"
- If term names don't match: Raise error "STEP ERROR: Term mismatch between IRT and CTT - [term] present in one but not other"
- If NaN coefficients: Raise error "TOOL ERROR: NaN coefficient detected for term [X] - model estimation failure"
- If kappa < 0.40: Raise error "CLARITY ERROR: Poor agreement (kappa < 0.40) - IRT and CTT yield contradictory conclusions"
- If p_bonferroni < p_uncorrected for any term: Raise error "TOOL ERROR: Bonferroni correction error - corrected p-value less than uncorrected (impossible)"
- Log failure to logs/step05_compare_fixed_effects.log
- Quit script immediately (do NOT proceed to Step 6)
- g_debug invoked to diagnose root cause (likely model convergence issue or term naming mismatch)

---

### Step 6: Compare Model Fit (AIC/BIC)

**Dependencies:** Step 3 (fitted models)
**Complexity:** Low (model fit extraction and comparison - <5 minutes)

**Purpose:** Compare model fit between IRT and CTT using AIC and BIC. Compute ”AIC and ”BIC (IRT - CTT). Interpret per Burnham & Anderson: |”| < 2 = equivalent fit, 2-10 = moderate evidence, > 10 = strong evidence for better model. Expected: equivalent fit (both capture same underlying trajectories).

**Input:**

**File 1:** data/step03_irt_lmm_model.pkl (from Step 3)
**Content:** Fitted IRT model object

**File 2:** data/step03_ctt_lmm_model.pkl (from Step 3)
**Content:** Fitted CTT model object

**Processing:**
1. Load both fitted models
2. Extract model fit indices from both:
   - AIC_irt = IRT model.aic
   - BIC_irt = IRT model.bic
   - AIC_ctt = CTT model.aic
   - BIC_ctt = CTT model.bic
3. Compute differences:
   - ”AIC = AIC_irt - AIC_ctt (negative favors IRT, positive favors CTT)
   - ”BIC = BIC_irt - BIC_ctt (negative favors IRT, positive favors CTT)
4. Interpret per Burnham & Anderson (2002) guidelines:
   - |”| < 2: Models have equivalent fit (no meaningful difference)
   - 2 <= |”| < 10: Moderate evidence for model with lower AIC/BIC
   - |”| >= 10: Strong evidence for model with lower AIC/BIC
5. Expected result: |”AIC| < 2 and |”BIC| < 2 (equivalent fit - both measurement approaches capture same underlying trajectories)

**Output:**

**File 1:** data/step06_model_fit_comparison.csv
**Format:** CSV with model fit comparison
**Columns:**
  - `metric` (string: AIC_IRT, AIC_CTT, BIC_IRT, BIC_CTT, ”AIC, ”BIC)
  - `value` (float, metric value)
  - `interpretation` (string, qualitative interpretation per Burnham & Anderson)
**Expected Rows:** 6

**File 2:** data/step06_fit_interpretation.txt
**Format:** Text file with detailed interpretation
**Content:**
  - AIC comparison: ”AIC = [X], interpretation: [equivalent/moderate/strong evidence for IRT/CTT]
  - BIC comparison: ”BIC = [Y], interpretation: [equivalent/moderate/strong evidence for IRT/CTT]
  - Overall conclusion: "IRT and CTT models show [equivalent/different] fit to data"
  - Convergence implication: "Both measurement approaches [are/are not] equally valid for paradigm-specific forgetting analysis"

**Validation Requirement:**
Validation tools MUST be used after model fit comparison. Specific validation tools will be determined by rq_tools based on fit index extraction and difference calculation. The rq_analysis agent will embed validation tool calls after the model comparison tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_model_fit_comparison.csv: 6 rows x 3 columns (metric, value, interpretation)
- data/step06_fit_interpretation.txt exists (text file - check contains "”AIC" and "”BIC")

*Value Ranges:*
- AIC_IRT, AIC_CTT typically in [500, 1500] for this sample size (absolute values less important than differences)
- BIC_IRT, BIC_CTT typically in [500, 1500] (BIC usually slightly higher than AIC due to penalty term)
- ”AIC typically in [-50, 50] (extreme differences > 100 rare unless models wildly different)
- ”BIC typically in [-50, 50] (similar range to ”AIC)
- Expected |”AIC| < 2 and |”BIC| < 2 (equivalent fit per hypothesis)

*Data Quality:*
- No NaN values in any metric (all fit indices must be finite)
- AIC and BIC must be positive (negative log-likelihood impossible for valid models)
- Expected N: Exactly 6 rows (4 fit indices + 2 differences)
- Interpretation column: Must contain "equivalent" / "moderate evidence" / "strong evidence" (not empty)

*Log Validation:*
- Required pattern: "Model fit comparison: ”AIC = [X], ”BIC = [Y]"
- Required pattern: "Interpretation: [equivalent fit / moderate evidence / strong evidence]"
- Forbidden patterns: "ERROR", "NaN AIC", "Negative AIC/BIC" (impossible for valid models)
- Acceptable warnings: "Moderate evidence favors [IRT/CTT]" (would suggest some divergence but not error)

**Expected Behavior on Validation Failure:**
- If NaN AIC or BIC: Raise error "TOOL ERROR: NaN fit index detected - model did not converge properly"
- If negative AIC or BIC: Raise error "TOOL ERROR: Negative AIC/BIC detected (impossible for valid models)"
- If row count != 6: Raise error "STEP ERROR: Expected 6 rows, found [N] - missing fit metrics"
- If |”AIC| > 10 or |”BIC| > 10: Raise error "CLARITY ERROR: Strong evidence for different fit (|”| > 10) - IRT and CTT measuring different constructs"
- Log failure to logs/step06_compare_model_fit.log
- Quit script immediately (do NOT proceed to Step 7)
- g_debug invoked to diagnose root cause (likely model convergence issue or data quality problem)

---

### Step 7: Prepare Scatterplot Data (IRT vs CTT Convergence)

**Dependencies:** Step 2 (merged IRT-CTT data), Step 3 (fitted models for predictions)
**Complexity:** Low (data aggregation for plotting - <5 minutes)

**Purpose:** Create dataset with 1200 rows (100 participants x 4 tests x 3 paradigms) containing: UID, test, paradigm, IRT_theta, CTT_mean, fitted values from both models. For plotting: scatterplot IRT vs CTT colored by paradigm, with y=x reference line and paradigm-specific regression lines.

**Input:**

**File 1:** data/step02_merged_irt_ctt.csv (from Step 2)
**Columns:** composite_ID, UID, TEST, theta_IFR/ICR/IRE, CTT_IFR/ICR/IRE, se_IFR/ICR/IRE
**Expected Rows:** 400

**File 2:** data/step03_irt_lmm_model.pkl (from Step 3)
**Content:** Fitted IRT model (for predictions)

**File 3:** data/step03_ctt_lmm_model.pkl (from Step 3)
**Content:** Fitted CTT model (for predictions)

**Processing:**
1. Reshape merged data from wide to long format (1200 rows):
   - Pivot theta_IFR/ICR/IRE into single `IRT_theta` column with `paradigm` factor
   - Pivot CTT_IFR/ICR/IRE into single `CTT_mean` column (aligned with paradigm)
2. Generate fitted values from both models:
   - IRT_fitted: Predict using IRT model on long-format data
   - CTT_fitted: Predict using CTT model on long-format data
3. Combine into single dataset for plotting: UID, TEST, paradigm, IRT_theta, CTT_mean, IRT_fitted, CTT_fitted
4. Sort by paradigm, then UID, then TEST (for organized plotting)

**Output:**

**File 1:** data/step07_scatterplot_data.csv
**Format:** CSV, long format for scatterplot visualization
**Columns:**
  - `UID` (string, participant identifier)
  - `TEST` (string, test session: T1, T2, T3, T4)
  - `paradigm` (string: IFR, ICR, IRE)
  - `IRT_theta` (float, IRT ability estimate)
  - `CTT_mean` (float, CTT proportion correct)
  - `IRT_fitted` (float, fitted value from IRT model)
  - `CTT_fitted` (float, fitted value from CTT model)
**Expected Rows:** 1200 (100 participants x 4 tests x 3 paradigms)

**Plot Description:** Scatterplot showing IRT theta (x-axis) vs CTT mean (y-axis), colored by paradigm (IFR=blue, ICR=green, IRE=red). Y=x reference line (dashed gray) shows perfect convergence. Paradigm-specific regression lines show actual IRT-CTT relationship per paradigm.

**Required for rq_plots:**
- Source CSV: data/step07_scatterplot_data.csv (created by this step)
- Plotting function: Scatterplot with regression lines
- PNG output: plots/step07_scatterplot_irt_ctt.png (created by rq_plots later)

**Validation Requirement:**
Validation tools MUST be used after scatterplot data preparation. Specific validation tools will be determined by rq_tools based on data aggregation and prediction generation. The rq_analysis agent will embed validation tool calls after the plot data preparation tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_scatterplot_data.csv exists (exact path)
- Expected rows: 1200 (100 participants x 4 tests x 3 paradigms)
- Expected columns: 7 (UID, TEST, paradigm, IRT_theta, CTT_mean, IRT_fitted, CTT_fitted)
- Data types: UID (object), TEST (object), paradigm (object), IRT_theta (float64), CTT_mean (float64), IRT_fitted (float64), CTT_fitted (float64)

*Value Ranges:*
- IRT_theta in [-4, 4] (typical IRT ability range)
- CTT_mean in [0, 1] (proportion correct bounds)
- IRT_fitted in [-4, 4] (model predictions should match theta range)
- CTT_fitted in [0, 1] (model predictions should match CTT_mean range)
- paradigm in {IFR, ICR, IRE} (categorical - exact match required)
- TEST in {T1, T2, T3, T4} (categorical - exact match required)

*Data Quality:*
- No NaN values in IRT_theta or CTT_mean (all 1200 observations valid)
- No NaN values in IRT_fitted or CTT_fitted (model predictions must succeed for all observations)
- Expected N: Exactly 1200 rows (no missing paradigm-test combinations)
- No duplicate rows (UID x TEST x paradigm combinations must be unique)
- Distribution check: All 3 paradigms represented equally (400 rows each)
- Distribution check: All 4 tests represented equally (300 rows each)

*Log Validation:*
- Required pattern: "Scatterplot data prepared: 1200 rows (400 x 3 paradigms)"
- Required pattern: "All paradigms represented: IFR, ICR, IRE"
- Required pattern: "Fitted values generated for both IRT and CTT models"
- Forbidden patterns: "ERROR", "NaN values in plot data", "Missing paradigm", "Prediction failed"
- Acceptable warnings: None expected for plot data preparation

**Expected Behavior on Validation Failure:**
- If row count != 1200: Raise error "STEP ERROR: Expected 1200 rows, found [N] - missing data"
- If NaN in IRT_theta or CTT_mean: Raise error "STEP ERROR: NaN values detected in observed scores - data completeness issue"
- If NaN in IRT_fitted or CTT_fitted: Raise error "TOOL ERROR: Model prediction failed - check model object and input data"
- If paradigm counts unequal: Raise error "STEP ERROR: Unequal paradigm representation - IFR=[A], ICR=[B], IRE=[C] (should be 400 each)"
- Log failure to logs/step07_prepare_scatterplot_data.log
- Quit script immediately (do NOT proceed to Step 8)
- g_debug invoked to diagnose root cause (likely reshaping error or model prediction issue)

---

### Step 8: Prepare Trajectory Comparison Data (IRT vs CTT)

**Dependencies:** Step 3 (fitted models), data/step03_irt_lmm_input.csv, data/step03_ctt_lmm_input.csv
**Complexity:** Low (data aggregation for trajectory plotting - <5 minutes)

**Purpose:** Prepare trajectory comparison data showing observed means and model predictions from both IRT and CTT models. Create aggregated dataset with paradigm x test means (12 rows: 3 paradigms x 4 tests) containing: observed IRT means, observed CTT means, IRT model predictions, CTT model predictions, confidence intervals. For plotting: two-panel figure (IRT trajectories vs CTT trajectories) showing convergence of forgetting patterns.

**Input:**

**File 1:** data/step03_irt_lmm_input.csv (from Step 3)
**Columns:** composite_ID, UID, TEST, TSVR_hours, paradigm, theta, time transformations
**Expected Rows:** 1200

**File 2:** data/step03_ctt_lmm_input.csv (from Step 3)
**Columns:** Same structure but CTT_mean instead of theta
**Expected Rows:** 1200

**File 3:** data/step03_irt_lmm_model.pkl (from Step 3)
**Content:** Fitted IRT model

**File 4:** data/step03_ctt_lmm_model.pkl (from Step 3)
**Content:** Fitted CTT model

**Processing:**
1. Load both LMM input files and fitted models
2. Aggregate observed means per paradigm x test (12 groups):
   - IRT observed: mean(theta) per paradigm-test combination
   - CTT observed: mean(CTT_mean) per paradigm-test combination
3. Generate model predictions at group level (paradigm x test):
   - Create prediction data: paradigm x test combinations with TSVR_hours from TSVR mapping (mean hours per test)
   - IRT predictions: predict using IRT model on group-level data
   - CTT predictions: predict using CTT model on group-level data
4. Compute 95% confidence intervals for observed means:
   - IRT CI: mean ± 1.96 x SE where SE = SD / sqrt(N participants per group)
   - CTT CI: mean ± 1.96 x SE (same calculation)
5. Combine into single dataset: paradigm, test, measurement_type, observed_mean, model_prediction, CI_lower, CI_upper
   - measurement_type in {IRT, CTT} - stack IRT and CTT rows for two-panel plotting

**Output:**

**File 1:** data/step08_trajectory_data.csv
**Format:** CSV with trajectory data for both IRT and CTT
**Columns:**
  - `paradigm` (string: IFR, ICR, IRE)
  - `TEST` (string: T1, T2, T3, T4)
  - `TSVR_hours` (float, mean hours since encoding per test)
  - `measurement_type` (string: IRT or CTT)
  - `observed_mean` (float, mean theta or CTT_mean per group)
  - `model_prediction` (float, fitted value from LMM)
  - `CI_lower` (float, lower 95% confidence bound for observed mean)
  - `CI_upper` (float, upper 95% confidence bound for observed mean)
**Expected Rows:** 24 (3 paradigms x 4 tests x 2 measurement types)

**Plot Description:** Two-panel figure showing IRT trajectories (left panel) vs CTT trajectories (right panel). Each panel: 3 lines (one per paradigm: IFR, ICR, IRE) with observed means (points + error bars) and model predictions (smooth lines). X-axis: TSVR_hours (0-168 hours). Y-axis IRT: theta scale (-3 to 3). Y-axis CTT: proportion correct (0 to 1).

**Required for rq_plots:**
- Source CSV: data/step08_trajectory_data.csv (created by this step)
- Plotting function: Two-panel trajectory comparison
- PNG output: plots/step08_trajectory_comparison_irt_ctt.png (created by rq_plots later)

**Validation Requirement:**
Validation tools MUST be used after trajectory data preparation. Specific validation tools will be determined by rq_tools based on data aggregation and prediction generation. The rq_analysis agent will embed validation tool calls after the plot data preparation tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_trajectory_data.csv exists (exact path)
- Expected rows: 24 (3 paradigms x 4 tests x 2 measurement types)
- Expected columns: 8 (paradigm, TEST, TSVR_hours, measurement_type, observed_mean, model_prediction, CI_lower, CI_upper)
- Data types: paradigm (object), TEST (object), TSVR_hours (float64), measurement_type (object), observed_mean (float64), model_prediction (float64), CI_lower (float64), CI_upper (float64)

*Value Ranges:*
- TSVR_hours in [0, 168] (0=encoding, 168=1 week)
- observed_mean for IRT in [-3, 3] (typical theta range for group means)
- observed_mean for CTT in [0, 1] (proportion correct bounds)
- model_prediction for IRT in [-3, 3] (theta scale predictions)
- model_prediction for CTT in [0, 1] (proportion correct predictions)
- CI_lower < observed_mean < CI_upper (confidence interval logic - must be ordered)
- paradigm in {IFR, ICR, IRE} (categorical)
- measurement_type in {IRT, CTT} (categorical)

*Data Quality:*
- No NaN values in any column (all 24 group means must compute successfully)
- Expected N: Exactly 24 rows (3 paradigms x 4 tests x 2 measurement types)
- No duplicate rows (paradigm x TEST x measurement_type combinations unique)
- Distribution check: CI_upper > CI_lower for all rows (confidence interval validity)
- Distribution check: All paradigms represented equally (8 rows each: 4 tests x 2 measurement types)
- Distribution check: All measurement types represented equally (12 rows each: 3 paradigms x 4 tests)

*Log Validation:*
- Required pattern: "Trajectory data prepared: 24 rows (3 paradigms x 4 tests x 2 measurement types)"
- Required pattern: "All paradigms represented: IFR, ICR, IRE"
- Required pattern: "Both measurement types present: IRT, CTT"
- Required pattern: "Confidence intervals valid: CI_lower < observed_mean < CI_upper for all rows"
- Forbidden patterns: "ERROR", "NaN values in trajectory data", "Missing paradigm", "CI_lower > CI_upper" (impossible)
- Acceptable warnings: None expected for trajectory data preparation

**Expected Behavior on Validation Failure:**
- If row count != 24: Raise error "STEP ERROR: Expected 24 rows, found [N] - missing paradigm-test-measurement combinations"
- If NaN in any column: Raise error "STEP ERROR: NaN values detected in trajectory data - check group mean calculations"
- If CI_lower > CI_upper: Raise error "TOOL ERROR: Invalid confidence interval - CI_lower > CI_upper (impossible)"
- If measurement_type not in {IRT, CTT}: Raise error "STEP ERROR: Invalid measurement_type value - expected IRT or CTT"
- Log failure to logs/step08_prepare_trajectory_data.log
- Quit script immediately
- g_debug invoked to diagnose root cause (likely aggregation error or model prediction issue)

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 -> Step 1:** Wide IRT theta (400 rows, 3 paradigm columns) + Purified items list (40-80 rows) -> CTT scores long format (1200 rows: 400 x 3 paradigms)

**Step 1 -> Step 2:** CTT long (1200 rows) reshapes to wide (400 rows, 3 CTT columns) -> Merges with IRT wide (400 rows, 6 columns: 3 theta + 3 CTT)

**Step 2 -> Step 3:** Merged wide (400 rows) reshapes to long for LMM (1200 rows: composite_ID x paradigm combinations)

**Step 3 -> Steps 4-8:** Fitted models (pkl objects) provide predictions and coefficients for all downstream comparisons

### Column Naming Conventions

**Participant Identifiers:**
- `UID` (string, format: P### with leading zeros, e.g., P001, P023, P100)
- `composite_ID` (string, format: UID_test, e.g., P001_T1, P023_T3)
- `TEST` (string, categorical: T1, T2, T3, T4 for Days 0, 1, 3, 6)

**Time Variables (Decision D070):**
- `TSVR_hours` (float, actual hours since VR encoding - primary time variable for LMM)
- `Days` (float, nominal days: 0, 1, 3, 6 - informational only, NOT used in LMM per D070)

**IRT Measurements:**
- `theta_IFR`, `theta_ICR`, `theta_IRE` (float, IRT ability estimates per paradigm)
- `se_IFR`, `se_ICR`, `se_IRE` (float, standard errors per paradigm)
- `theta` (float, stacked theta values in long format - generic name when paradigm is separate column)

**CTT Measurements:**
- `CTT_IFR`, `CTT_ICR`, `CTT_IRE` (float, CTT proportion correct per paradigm in wide format)
- `CTT_mean` (float, stacked CTT values in long format - generic name when paradigm is separate column)
- `n_items` (int, number of items with valid responses per observation)

**Grouping Variables:**
- `paradigm` (string, categorical: IFR, ICR, IRE)
- `measurement_type` (string, categorical: IRT, CTT - for stacked plotting)

**Model Outputs:**
- `IRT_fitted`, `CTT_fitted` (float, fitted values from respective LMM models)
- `IRT_coef`, `CTT_coef` (float, fixed effect coefficients)
- `IRT_sig`, `CTT_sig` (bool, significance classifications)

**Confidence Intervals:**
- `CI_lower`, `CI_upper` (float, 95% confidence bounds for observed means)

### Data Type Constraints

**Nullable vs Non-Nullable:**
- `UID`, `composite_ID`, `TEST`, `paradigm` - Non-nullable (required for all observations)
- `theta_*`, `CTT_*` - Non-nullable after Step 1 (all 1200 observations must have valid scores)
- `IRT_fitted`, `CTT_fitted` - Non-nullable after Step 3 (model predictions required for all)
- `n_items` - Non-nullable (all observations must report item count)

**Valid Ranges:**
- `theta_*` in [-4, 4] (IRT ability - typical range with buffer)
- `CTT_*` in [0, 1] (proportion correct - strict bounds)
- `TSVR_hours` in [0, 200] (hours since encoding - 0 to ~8 days)
- `r` (correlations) in [-1, 1] (correlation bounds)
- `p_*` (p-values) in [0, 1] (probability bounds)
- `kappa` in [-1, 1] (Cohen's kappa bounds)

**Categorical Values:**
- `paradigm` in {IFR, ICR, IRE} (no other values allowed)
- `TEST` in {T1, T2, T3, T4} (no other values allowed)
- `measurement_type` in {IRT, CTT} (no other values allowed)
- `result` in {PASS, FAIL, WARNING} (diagnostic test results)
- `interpretation` - Free text but should be non-empty

---

## Cross-RQ Dependencies

**Dependency Type:** DERIVED Data from RQ 5.3.1 (Paradigm-Specific Trajectories)

**This RQ requires outputs from:**
- **RQ 5.3.1** (Paradigm-Specific Trajectories - IRT calibration and purification)
  - File: results/ch5/5.3.1/data/step03_theta_scores.csv (final theta scores after Pass 2 calibration)
  - File: results/ch5/5.3.1/data/step02_purified_items.csv (retained items post-purification per Decision D039)
  - File: results/ch5/5.3.1/data/step00_tsvr_mapping.csv (time mapping: UID, TEST, TSVR_hours, Days)
  - File: results/ch5/5.3.1/data/step05_lmm_model_comparison.csv (best model identification for parallel LMM)
  - Used in: Step 0 (load all dependency files), Step 1 (CTT computation on purified items), Step 3 (LMM formula from best model)
  - Rationale: RQ 5.3.1 establishes IRT measurement framework and identifies best-fitting trajectory model. This RQ validates those findings by comparing IRT to CTT on the same purified item set.

**Execution Order Constraint:**
1. RQ 5.3.1 must complete Steps 0-5 first (data extraction, IRT calibration, purification, theta extraction, LMM model selection)
2. This RQ (5.3.5) executes after RQ 5.3.1 completion (uses theta scores, purified items, and best model formula)

**Data Source Boundaries (Per Specification 5.1.6):**
- **RAW data:** data/cache/dfData.csv extracted directly (raw binary responses for CTT computation)
- **DERIVED data:** Outputs from RQ 5.3.1 (theta scores, purified items, TSVR mapping, best model formula)
- **Scope:** This RQ does NOT re-calibrate IRT models (reuses RQ 5.3.1 calibration) but DOES compute CTT from raw responses

**Validation:**
- Step 0: Check results/ch5/5.3.1/status.yaml shows rq_inspect: success (circuit breaker: EXPECTATIONS ERROR if incomplete)
- Step 0: Verify all required files exist (circuit breaker: EXPECTATIONS ERROR if missing)
- Step 0: Validate file structures match expectations (circuit breaker: STEP ERROR if row counts or columns wrong)
- If RQ 5.3.1 incomplete: Quit with error "EXPECTATIONS ERROR: RQ 5.3.1 must complete before RQ 5.3.5 (dependency)"

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

| Step | Analysis | Validation Criteria |
|------|----------|---------------------|
| 0 | Load Dependencies | File existence (4 files from RQ 5.3.1), row counts (400, 400, 40-80, ~40000), column structure, composite_ID uniqueness, item counts per paradigm >= 10 |
| 1 | Compute CTT Scores | CTT_mean in [0,1], no NaN values, 1200 rows (400 x 3 paradigms), n_items >= 5 per observation, paradigm categories valid |
| 2 | Pearson Correlations | r in [-1,1], p_bonferroni >= p_uncorrected, 4 rows (3 paradigms + overall), r > 0.70 for strong convergence threshold, dual p-values present (Decision D068) |
| 3 | Fit Parallel LMMs | Both models converge OR both simplified equally (structural equivalence), random variances > 0, 1200 observations per model, identical formula structure |
| 4 | Validate LMM Assumptions | 7 diagnostic tests run per model (IRT and CTT), at least 5/7 tests PASS for acceptable model, residuals approximately normal, Cook's distance <1.0 for >95% observations |
| 5 | Compare Fixed Effects | Coefficient extraction successful for all terms, IRT and CTT row counts match, Cohen's kappa > 0.60 (substantial agreement threshold), percentage agreement >= 80%, dual p-values per Decision D068 |
| 6 | Compare Model Fit | AIC and BIC positive and finite, ”AIC and ”BIC computed, \|”AIC\| < 2 and \|”BIC\| < 2 expected (equivalent fit) |
| 7 | Prepare Scatterplot Data | 1200 rows (400 x 3 paradigms), no NaN in observed or fitted values, IRT_theta in [-4,4], CTT_mean in [0,1], all paradigms represented equally |
| 8 | Prepare Trajectory Data | 24 rows (3 paradigms x 4 tests x 2 measurement types), CI_lower < observed_mean < CI_upper, no NaN values, all paradigms and measurement types represented |

**NOTE:** Technical validation (files exist, formats correct, values in bounds) checked by validation tools DURING analysis execution. Scientific plausibility (effect directions, theoretical coherence) checked by rq_results AFTER all analysis complete.

---

## Summary

**Total Steps:** 8 (Step 0: load dependencies + Steps 1-7: analysis and plotting data preparation)
**Estimated Runtime:** Medium (30-60 minutes total - dominated by LMM fitting in Step 3)
**Cross-RQ Dependencies:** RQ 5.3.1 (Paradigm-Specific Trajectories - MUST complete Steps 0-5 before this RQ)
**Primary Outputs:**
- Correlation table (r > 0.70 convergence per paradigm)
- Parallel LMM summaries (IRT vs CTT with identical structure)
- Fixed effect comparison (Cohen's kappa > 0.60, agreement >= 80%)
- Model fit comparison (”AIC < 2, ”BIC < 2 expected)
- Scatterplot data (1200 observations: IRT vs CTT per paradigm)
- Trajectory comparison data (24 group means: paradigm x test x measurement type)

**Validation Coverage:** 100% (all 8 steps have validation requirements with 4-layer substance criteria)

**Key Success Criteria:**
- All Pearson correlations r > 0.70 (strong convergence threshold met)
- Cohen's kappa > 0.60 (substantial agreement on fixed effect significance)
- Agreement on statistical significance >= 80% of fixed effects
- Both IRT and CTT models converge with identical structure (or both simplified equally)
- Dual p-values present per Decision D068 (p_uncorrected and p_bonferroni reported)
- No NaN values in correlation or coefficient comparison tables
- Plot data files exist with correct row counts (1200 for scatterplot, 24 for trajectories)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-02): Initial plan created by rq_planner agent for RQ 5.3.5 (IRT-CTT Convergence for Paradigm-Specific Forgetting)
