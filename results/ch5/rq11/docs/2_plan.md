# Analysis Plan for RQ 5.11: IRT-CTT Convergent Validity

**Created by:** rq_planner agent
**Date:** 2025-11-27
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This RQ examines convergent validity between IRT and CTT measurement approaches for domain-specific episodic memory ability across three domains (What, Where, When) and four test sessions (T1-T4). The analysis compares IRT theta scores (from RQ 5.1) with CTT mean scores (computed from raw data using the same purified item set) via correlation analysis and parallel LMM trajectory modeling.

**Key Objectives:**
1. Test correlation strength (r > 0.70 threshold for strong convergence per psychometric standards)
2. Compare statistical significance patterns in parallel LMMs (Cohen's kappa > 0.60 for substantial agreement)
3. Assess model fit equivalence (AIC/BIC comparison)
4. Visualize IRT vs CTT trajectories to identify scaling differences vs pattern differences

**Pipeline Type:** Correlation Analysis + Parallel LMM Comparison (NOT IRT calibration - uses DERIVED data from RQ 5.1)

**Total Steps:** 9 analysis steps (Step 0 = data loading, Steps 1-8 = analysis and plotting)

**Estimated Runtime:** Medium (30-60 minutes total)
- Step 0: Low (5 min - data loading)
- Step 1: Low (5 min - CTT computation)
- Step 2: Low (5 min - correlation analysis)
- Step 3: High (30-40 min - parallel LMM fitting with convergence testing)
- Step 4: Medium (10 min - comprehensive assumption validation for both models)
- Step 5: Low (5 min - coefficient extraction and comparison)
- Step 6: Low (2 min - AIC/BIC comparison)
- Step 7-8: Low (5 min each - plot data preparation)

**Key Decisions Applied:**
- **Decision D068:** Dual p-value reporting (uncorrected + Holm-Bonferroni for correlations, uncorrected + Bonferroni for LMM coefficients if contrasts needed)
- **Decision D070:** TSVR as LMM time variable (actual hours since encoding, not nominal days 0/1/3/6)
- **NOT D039:** No 2-pass IRT purification (uses pre-computed theta from RQ 5.1)
- **NOT D069:** No dual-scale theta/probability plots (plotting correlations and trajectory comparisons, not IRT-specific transformations)

---

## Analysis Plan

### Step 0: Load Data from RQ 5.1 and Master Dataset

**Purpose:** Load IRT theta scores from RQ 5.1 and extract raw VR item data for CTT computation

**Dependencies:** None (first step, but requires RQ 5.1 completion)

**Complexity:** Low (5 minutes - file reading and basic filtering)

**Input:**

**File 1:** results/ch5/rq1/data/step03_theta_scores.csv (DERIVED from RQ 5.1)
**Source:** RQ 5.1 Step 3 (IRT calibration Pass 2 theta extraction)
**Format:** CSV with columns:
  - `composite_ID` (string, format: {UID}_{test}, e.g., P001_T1)
  - `theta_common` (float, common item ability estimate)
  - `se_common` (float, standard error for common items)
  - `theta_congruent` (float, congruent item ability estimate)
  - `se_congruent` (float, standard error for congruent items)
  - `theta_incongruent` (float, incongruent item ability estimate)
  - `se_incongruent` (float, standard error for incongruent items)
**Expected Rows:** ~400 (100 participants x 4 tests)
**Note:** Theta scores are from purified item set (RQ 5.1 Pass 2)

**File 2:** results/ch5/rq1/data/step00_tsvr_mapping.csv (DERIVED from RQ 5.1)
**Source:** RQ 5.1 Step 0 (TSVR extraction)
**Format:** CSV with columns:
  - `UID` (string, participant identifier, e.g., P001)
  - `test` (string, test session, e.g., T1, T2, T3, T4)
  - `TSVR_hours` (float, actual hours since encoding per Decision D070)
**Expected Rows:** ~400 (100 participants x 4 tests)

**File 3:** results/ch5/rq1/data/step02_purified_items.csv (DERIVED from RQ 5.1)
**Source:** RQ 5.1 Step 2 (item purification per Decision D039)
**Format:** CSV with columns:
  - `item_name` (string, item tag from master.xlsx, e.g., VR-IFR-A01-N-ANS)
  - `dimension` (string, domain classification: common/congruent/incongruent)
  - `a` (float, Pass 1 discrimination parameter - for reference)
  - `b` (float, Pass 1 difficulty parameter - for reference)
**Expected Rows:** ~40-60 items (40-50% retention per Decision D039 expectations for temporal items)
**Purpose:** Ensures CTT scores computed from SAME item set as IRT for fair comparison

**File 4:** data/cache/dfData.csv (RAW master dataset)
**Source:** Project-level master data file
**Format:** CSV with columns:
  - `UID` (string, participant identifier)
  - `TEST` (string, test session)
  - Item columns matching tags from purified_items.csv (values: {0, 1, NaN})
**Expected Rows:** ~400 (100 participants x 4 tests)
**Purpose:** Source for CTT mean score computation

**Processing:**
1. Load IRT theta scores (File 1)
2. Load TSVR mapping (File 2)
3. Load purified item list (File 3) - extract item_name column as filter
4. Load raw master data (File 4)
5. Filter master data to retain ONLY items in purified_items.csv (ensures IRT-CTT comparison uses same items)
6. Parse domain from item tags:
   - What domain: `-N-` tag pattern
   - Where domain: `-L-`, `-U-`, `-D-` tag patterns (all three per concept.md)
   - When domain: `-O-` tag pattern
7. No aggregation yet (Step 1 computes CTT scores)

**Output:**

**File 1:** data/step00_irt_theta_loaded.csv
**Format:** CSV (copy of RQ 5.1 theta scores for local reference)
**Columns:** composite_ID, theta_common, se_common, theta_congruent, se_congruent, theta_incongruent, se_incongruent
**Expected Rows:** ~400

**File 2:** data/step00_tsvr_loaded.csv
**Format:** CSV (copy of RQ 5.1 TSVR for local reference)
**Columns:** UID, test, TSVR_hours
**Expected Rows:** ~400

**File 3:** data/step00_purified_items.csv
**Format:** CSV (copy of RQ 5.1 purified items for local reference)
**Columns:** item_name, dimension, a, b
**Expected Rows:** ~40-60

**File 4:** data/step00_raw_data_filtered.csv
**Format:** CSV, wide format (one row per UID x test)
**Columns:** UID, TEST, [item columns from purified set only]
**Expected Rows:** ~400
**Expected Columns:** 2 (UID, TEST) + ~40-60 item columns = ~42-62 total

**Validation Requirement:**
Validation tools MUST be used after data loading tool execution. Specific validation tools will be determined by rq_tools based on data loading requirements (file existence checks, column validation, row count verification).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_irt_theta_loaded.csv: 400 rows x 7 columns (composite_ID: object, theta/se columns: float64)
- data/step00_tsvr_loaded.csv: 400 rows x 3 columns (UID: object, test: object, TSVR_hours: float64)
- data/step00_purified_items.csv: 40-60 rows x 4 columns (item_name: object, dimension: object, a: float64, b: float64)
- data/step00_raw_data_filtered.csv: 400 rows x 42-62 columns (UID: object, TEST: object, items: float64)

*Value Ranges:*
- theta columns in [-3, 3] (typical IRT ability range)
- se columns in [0.1, 1.0] (standard error bounds)
- TSVR_hours in [0, 200] hours (0 = encoding, ~168 = 1 week, allow buffer)
- Item discrimination a > 0.4 (purification threshold from RQ 5.1)
- Item difficulty b unrestricted (temporal items can have extreme values)
- Raw item scores in {0, 1, NaN} (binary responses)

*Data Quality:*
- All 400 composite_IDs present in theta file (no data loss from RQ 5.1)
- All 400 UID x test combinations present in TSVR file
- Purified items count: 40-60 items (40-50% retention expected per Decision D039)
- Raw data filtered to match purified items exactly (column names must match item_name from purified_items.csv)
- No unexpected NaN patterns (>90% missing per item suggests filtering error)

*Log Validation:*
- Required pattern: "Loaded IRT theta scores: 400 rows"
- Required pattern: "Loaded TSVR mapping: 400 rows"
- Required pattern: "Loaded purified items: [N] items"
- Required pattern: "Filtered raw data to [N] purified items"
- Required pattern: "All domain tags parsed successfully (What/Where/When)"
- Forbidden patterns: "ERROR", "File not found", "Missing required column"
- Acceptable warnings: "Some items have NaN (expected for not-administered items)"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "RQ 5.1 theta file not found - RQ 5.1 must complete first")
- Log failure to logs/step00_load_data.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked by master to diagnose root cause (likely RQ 5.1 incomplete or file path mismatch)

---

### Step 1: Compute CTT Mean Scores

**Purpose:** Calculate CTT (Classical Test Theory) mean scores per UID x test x domain using same purified item set as RQ 5.1 IRT

**Dependencies:** Step 0 (requires filtered raw data and purified item list)

**Complexity:** Low (5 minutes - aggregation only)

**Input:**

**File 1:** data/step00_raw_data_filtered.csv
**Source:** Generated by Step 0
**Format:** CSV, wide format
**Columns:** UID, TEST, [~40-60 purified item columns]
**Expected Rows:** ~400

**File 2:** data/step00_purified_items.csv
**Source:** Generated by Step 0
**Format:** CSV
**Columns:** item_name, dimension, a, b
**Expected Rows:** ~40-60

**Processing:**
1. Parse item tags to assign domains:
   - Extract tag components: VR-{paradigm}-{test}-{domain}-{type}
   - What domain: `-N-` pattern
   - Where domain: `-L-` OR `-U-` OR `-D-` patterns (aggregate all three per concept.md)
   - When domain: `-O-` pattern
2. Group items by domain (What items, Where items, When items)
3. Compute CTT mean scores per UID x TEST x domain:
   - CTT_What = mean of all What items (ignoring NaN)
   - CTT_Where = mean of all Where items (ignoring NaN)
   - CTT_When = mean of all When items (ignoring NaN)
4. Reshape to long format:
   - One row per UID x TEST x domain
   - Columns: UID, TEST, domain, CTT_score
5. Create composite_ID column: composite_ID = {UID}_{TEST} (matches IRT theta format)

**Output:**

**File:** data/step01_ctt_scores.csv
**Format:** CSV, long format (one row per UID x test x domain)
**Columns:**
  - `composite_ID` (string, format: {UID}_{test}, e.g., P001_T1)
  - `UID` (string, participant identifier)
  - `test` (string, test session: T1, T2, T3, T4)
  - `domain` (string, memory domain: What, Where, When)
  - `CTT_score` (float, mean accuracy across domain items, range [0, 1])
  - `n_items` (int, number of items contributing to mean - diagnostic)
**Expected Rows:** 1200 (400 UID x test combinations x 3 domains)
**Expected Values:** CTT_score in [0, 1] (proportion correct)

**Validation Requirement:**
Validation tools MUST be used after CTT computation tool execution. Specific validation tools will be determined by rq_tools based on aggregation requirements (row count, value ranges, completeness checks).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_ctt_scores.csv: 1200 rows x 6 columns (composite_ID: object, UID: object, test: object, domain: object, CTT_score: float64, n_items: int64)

*Value Ranges:*
- CTT_score in [0, 1] (proportion correct - cannot exceed 1.0)
- n_items > 0 (at least 1 item per domain, expected: 10-20 items per domain)
- n_items approximately equal across domains (What ~= Where ~= When within 50% tolerance)

*Data Quality:*
- Exactly 1200 rows (400 UID x test x 3 domains, no missing combinations)
- All 3 domains present (What, Where, When) for each UID x test
- No NaN in CTT_score (if insufficient items, flag as data quality issue)
- composite_ID matches format from IRT theta file (for merge in Step 2)

*Log Validation:*
- Required pattern: "Computed CTT scores: 1200 rows (400 UID x test x 3 domains)"
- Required pattern: "Domain distribution: What [N] items, Where [N] items, When [N] items"
- Required pattern: "CTT_score range: [min, max] (expected [0, 1])"
- Forbidden patterns: "ERROR", "No items for domain", "CTT_score > 1.0"
- Acceptable warnings: "Some participants missing items (NaN ignored in mean)"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 1200 rows, found 900 - missing domain data")
- Log failure to logs/step01_compute_ctt.log
- Quit script immediately
- g_debug invoked to diagnose (likely domain tag parsing error or incomplete purified item set)

---

### Step 2: Correlation Analysis (IRT vs CTT per Domain)

**Purpose:** Compute Pearson correlations between IRT theta and CTT mean scores for each domain, test significance with Holm-Bonferroni correction per concept.md

**Dependencies:** Steps 0, 1 (requires IRT theta and CTT scores)

**Complexity:** Low (5 minutes - correlation computation)

**Input:**

**File 1:** data/step00_irt_theta_loaded.csv
**Source:** Generated by Step 0
**Format:** CSV
**Columns:** composite_ID, theta_common, se_common, theta_congruent, se_congruent, theta_incongruent, se_incongruent
**Expected Rows:** ~400

**File 2:** data/step01_ctt_scores.csv
**Source:** Generated by Step 1
**Format:** CSV, long format
**Columns:** composite_ID, UID, test, domain, CTT_score, n_items
**Expected Rows:** 1200

**Processing:**
1. Map RQ 5.1 IRT dimensions to domains:
   - theta_common -> corresponds to "common items" (likely What domain per RQ 5.1 design)
   - theta_congruent -> corresponds to "congruent items" (likely Where domain)
   - theta_incongruent -> corresponds to "incongruent items" (likely When domain)
   - NOTE: Exact mapping should match RQ 5.1 dimension definitions (check RQ 5.1 1_concept.md if unclear)
2. Reshape IRT theta to long format for merge:
   - Create rows: composite_ID, domain (What/Where/When), IRT_score
3. Merge IRT and CTT on composite_ID + domain
4. Compute Pearson correlations per domain:
   - r_What = corr(IRT_What, CTT_What)
   - r_Where = corr(IRT_Where, CTT_Where)
   - r_When = corr(IRT_When, CTT_When)
   - r_overall = corr(IRT_all, CTT_all) [pooled across domains]
5. Compute 95% confidence intervals for each correlation (Fisher z-transformation)
6. Test significance with Holm-Bonferroni correction:
   - 4 tests total (What, Where, When, overall)
   - Rank p-values from smallest to largest
   - Compare each p to alpha/(m - k + 1) where m=4, k=rank
   - Report BOTH uncorrected and Holm-Bonferroni corrected p-values (per Decision D068 dual reporting philosophy)
7. Test thresholds:
   - Primary: r > 0.70 (strong convergence per psychometric standards, concept.md)
   - Secondary: r > 0.90 (exceptional convergence, concept.md)

**Output:**

**File:** results/step02_correlations.csv
**Format:** CSV
**Columns:**
  - `domain` (string: What, Where, When, Overall)
  - `r` (float, Pearson correlation coefficient, range [-1, 1])
  - `CI_lower` (float, 95% CI lower bound)
  - `CI_upper` (float, 95% CI upper bound)
  - `p_uncorrected` (float, uncorrected p-value)
  - `p_holm` (float, Holm-Bonferroni corrected p-value per Decision D068)
  - `n` (int, sample size for correlation)
  - `threshold_0.70` (boolean, TRUE if r > 0.70)
  - `threshold_0.90` (boolean, TRUE if r > 0.90)
**Expected Rows:** 4 (What, Where, When, Overall)

**Validation Requirement:**
Validation tools MUST be used after correlation tool execution. Specific validation tools will be determined by rq_tools based on correlation analysis requirements (dual p-value validation per Decision D068, value range checks).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step02_correlations.csv: 4 rows x 9 columns (domain: object, r/CI/p/n: float64, thresholds: bool)

*Value Ranges:*
- r in [-1, 1] (correlation coefficient bounds)
- CI_lower in [-1, 1], CI_upper in [-1, 1] (confidence bounds)
- CI_lower < r < CI_upper (confidence interval must bracket point estimate)
- p_uncorrected in [0, 1] (p-value bounds)
- p_holm in [0, 1] (corrected p-value bounds)
- p_holm >= p_uncorrected (correction cannot make p-value smaller)
- n > 0 (sample size must be positive)

*Data Quality:*
- Exactly 4 rows (What, Where, When, Overall)
- All domains present (no missing domain)
- No NaN in r, CI, or p columns (correlations must compute for all domains)
- Expected correlation strength: r > 0.70 for at least 2/4 tests (convergence expected per hypothesis)
- p_uncorrected and p_holm both present (Decision D068 dual reporting)

*Log Validation:*
- Required pattern: "Computed 4 correlations (What, Where, When, Overall)"
- Required pattern: "Holm-Bonferroni correction applied (m=4 tests)"
- Required pattern: "VALIDATION - PASS: Dual p-values present (uncorrected + Holm)"
- Required pattern: "[N] correlations exceed r > 0.70 threshold"
- Required pattern: "[N] correlations exceed r > 0.90 threshold"
- Forbidden patterns: "ERROR", "Missing domain", "p_holm < p_uncorrected"
- Acceptable warnings: "Some correlations below 0.70 threshold (divergence detected)"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Missing p_holm column - Decision D068 requires dual p-values")
- Log failure to logs/step02_correlations.log
- Quit script immediately
- g_debug invoked to diagnose (likely dual p-value implementation missing or correlation computation error)

---

### Step 3: Fit Parallel LMMs (IRT Model + CTT Model)

**Purpose:** Fit identical LMM structures for IRT and CTT scores to compare trajectory patterns and statistical significance

**Dependencies:** Steps 0, 1, 2 (requires IRT theta, CTT scores, TSVR mapping)

**Complexity:** High (30-40 minutes - LMM fitting with convergence testing, random structure selection)

**Input:**

**File 1:** data/step00_irt_theta_loaded.csv
**Source:** Generated by Step 0
**Columns:** composite_ID, theta_common, se_common, theta_congruent, se_congruent, theta_incongruent, se_incongruent
**Expected Rows:** ~400

**File 2:** data/step01_ctt_scores.csv
**Source:** Generated by Step 1
**Columns:** composite_ID, UID, test, domain, CTT_score, n_items
**Expected Rows:** 1200

**File 3:** data/step00_tsvr_loaded.csv
**Source:** Generated by Step 0
**Columns:** UID, test, TSVR_hours
**Expected Rows:** ~400

**Processing:**

**Data Preparation:**
1. Reshape IRT theta to long format:
   - Rows: composite_ID, domain (What/Where/When), IRT_score
   - Map dimensions to domains (theta_common -> What, theta_congruent -> Where, theta_incongruent -> When per RQ 5.1)
2. Merge IRT long with TSVR on UID + test
3. Merge CTT with TSVR on UID + test
4. Result: Two parallel datasets
   - irt_lmm_input: composite_ID, UID, test, domain, TSVR_hours, IRT_score
   - ctt_lmm_input: composite_ID, UID, test, domain, TSVR_hours, CTT_score

**LMM Specification (Identical for Both Models):**
- **Formula:** Score ~ (TSVR_hours + log(TSVR_hours + 1)) * domain + (TSVR_hours | UID)
  - Fixed effects: TSVR_hours (linear time), log(TSVR_hours + 1) (nonlinear time), domain (What/Where/When), interactions
  - Random effects: Random intercepts + random slopes for TSVR_hours per participant
- **Convergence Strategy (per concept.md):**
  - Attempt full random slopes model (TSVR_hours | UID) first
  - If EITHER model fails to converge (checked via validate_lmm_convergence):
    - Simplify BOTH to random intercepts only (1 | UID) to maintain identical structure
    - Document which model(s) failed and remedial action in results
  - Rationale: With N=100, random slopes may cause convergence issues (Bates et al. 2015 recommend N>=200)
- **Time Variable:** TSVR_hours (actual hours since encoding per Decision D070, NOT nominal days)

**Fitting Procedure:**
1. Fit IRT model: mixedlm(IRT_score ~ (TSVR_hours + log(TSVR_hours+1)) * domain, groups=UID, re_formula="TSVR_hours")
2. Fit CTT model: mixedlm(CTT_score ~ (TSVR_hours + log(TSVR_hours+1)) * domain, groups=UID, re_formula="TSVR_hours")
3. Check convergence for both models (validate_lmm_convergence)
4. If either fails: Re-fit both with random intercepts only (1 | UID)
5. Extract model summaries (fixed effects, random effects, fit indices)

**Output:**

**File 1:** data/step03_irt_lmm_input.csv
**Format:** CSV, long format
**Columns:** composite_ID, UID, test, domain, TSVR_hours, IRT_score
**Expected Rows:** 1200 (400 UID x test x 3 domains)

**File 2:** data/step03_ctt_lmm_input.csv
**Format:** CSV, long format
**Columns:** composite_ID, UID, test, domain, TSVR_hours, CTT_score
**Expected Rows:** 1200

**File 3:** results/step03_irt_lmm_summary.txt
**Format:** Text file with statsmodels MixedLM summary
**Content:** Fixed effects table, random effects variances, AIC, BIC, log-likelihood, convergence status

**File 4:** results/step03_ctt_lmm_summary.txt
**Format:** Text file with statsmodels MixedLM summary
**Content:** Fixed effects table, random effects variances, AIC, BIC, log-likelihood, convergence status

**File 5:** results/step03_irt_lmm_fixed_effects.csv
**Format:** CSV
**Columns:** term (coefficient name), estimate, SE, z, p_uncorrected
**Expected Rows:** ~10 (intercept, TSVR_hours, log(TSVR_hours+1), domain, interactions)

**File 6:** results/step03_ctt_lmm_fixed_effects.csv
**Format:** CSV
**Columns:** term, estimate, SE, z, p_uncorrected
**Expected Rows:** ~10

**File 7:** logs/step03_convergence_report.txt
**Format:** Text report documenting convergence decisions
**Content:**
  - Initial random structure attempted (random slopes or intercepts only)
  - Convergence status for IRT model (True/False)
  - Convergence status for CTT model (True/False)
  - Final random structure used (if simplified due to convergence failure)
  - Rationale for simplification (if applied)

**Validation Requirement:**
Validation tools MUST be used after LMM fitting tool execution. Specific validation tools will be determined by rq_tools based on LMM requirements (convergence checks, fit index validation, coefficient range checks).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_irt_lmm_input.csv: 1200 rows x 6 columns (composite_ID: object, UID: object, test: object, domain: object, TSVR_hours: float64, IRT_score: float64)
- data/step03_ctt_lmm_input.csv: 1200 rows x 6 columns (composite_ID: object, UID: object, test: object, domain: object, TSVR_hours: float64, CTT_score: float64)
- results/step03_irt_lmm_summary.txt: exists, >1000 characters (full summary)
- results/step03_ctt_lmm_summary.txt: exists, >1000 characters
- results/step03_irt_lmm_fixed_effects.csv: ~10 rows x 5 columns
- results/step03_ctt_lmm_fixed_effects.csv: ~10 rows x 5 columns
- logs/step03_convergence_report.txt: exists, documents convergence decisions

*Value Ranges:*
- IRT_score in [-3, 3] (typical IRT ability range)
- CTT_score in [0, 1] (proportion correct)
- TSVR_hours in [0, 200] (hours since encoding)
- Fixed effect estimates unrestricted (can be positive or negative)
- SE > 0 (standard errors must be positive)
- z unrestricted (Wald z-statistic)
- p_uncorrected in [0, 1]
- AIC/BIC > 0 (information criteria must be positive)

*Data Quality:*
- Exactly 1200 rows in both LMM input files
- All 3 domains present for each UID x test
- No NaN in TSVR_hours or score columns
- Both models converged OR both simplified to same random structure (parallelism maintained)
- Fixed effects tables have same row count for both models (identical structure)
- Convergence report documents decisions clearly

*Log Validation:*
- Required pattern: "Prepared IRT LMM input: 1200 rows"
- Required pattern: "Prepared CTT LMM input: 1200 rows"
- Required pattern: "Fitting IRT model with formula: Score ~ (TSVR_hours + log(TSVR_hours+1)) * domain + (...)"
- Required pattern: "Fitting CTT model with formula: Score ~ (TSVR_hours + log(TSVR_hours+1)) * domain + (...)"
- Required pattern: "IRT model converged: [True/False]"
- Required pattern: "CTT model converged: [True/False]"
- Required pattern: "Final random structure: [random slopes / random intercepts only]"
- Forbidden patterns: "ERROR", "Convergence failed for both models", "Formula mismatch between IRT and CTT"
- Acceptable warnings: "Random slopes convergence failed, simplified to random intercepts only"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Both models failed to converge even with random intercepts - data quality issue")
- Log failure to logs/step03_fit_lmm.log
- Quit script immediately
- g_debug invoked to diagnose (likely insufficient data, multicollinearity, or model misspecification)

---

### Step 4: Validate LMM Assumptions (Both Models)

**Purpose:** Perform comprehensive assumption checks for both IRT and CTT LMMs per concept.md requirement (residual normality, homoscedasticity, random effects normality, independence)

**Dependencies:** Step 3 (requires fitted LMM models)

**Complexity:** Medium (10 minutes - diagnostic plots and statistical tests)

**Input:**

**File 1:** results/step03_irt_lmm_summary.txt (fitted IRT model object via re-loading)
**File 2:** results/step03_ctt_lmm_summary.txt (fitted CTT model object via re-loading)
**File 3:** data/step03_irt_lmm_input.csv (for residual extraction)
**File 4:** data/step03_ctt_lmm_input.csv (for residual extraction)

**Processing:**

**For Each Model (IRT and CTT):**
1. **Residual Normality:**
   - Extract residuals from fitted model
   - Q-Q plot (visual inspection)
   - Shapiro-Wilk test (p > 0.05 threshold per concept.md)
2. **Homoscedasticity:**
   - Residuals vs fitted values plot (visual inspection)
   - No fanning pattern expected
3. **Random Effects Normality:**
   - Extract random intercepts (and slopes if fitted)
   - Q-Q plot for random effects distribution
4. **Independence (Repeated Measures):**
   - Autocorrelation Function (ACF) plot per participant
   - Lag-1 ACF < 0.1 threshold per concept.md
5. **Use validate_lmm_assumptions_comprehensive tool:**
   - Automated diagnostics with plots and remedial recommendations
   - 7 checks: normality, homoscedasticity, Q-Q, ACF, linearity, outliers, convergence

**Remedial Actions (per concept.md):**
- If EITHER model violates assumptions:
  - Apply same remediation to BOTH models (e.g., robust standard errors, AR(1) correlation structure)
  - Maintain parallelism between models
  - Document all assumption test results and remedial actions

**Output:**

**File 1:** results/step04_irt_assumptions_report.txt
**Format:** Text report
**Content:**
  - Shapiro-Wilk test result (statistic, p-value, pass/fail)
  - Homoscedasticity assessment (visual, pass/fail)
  - Random effects normality (visual, pass/fail)
  - ACF Lag-1 values per participant (mean, range, threshold check)
  - Overall verdict: PASS / CONDITIONAL / FAIL
  - Remedial actions recommended (if any)

**File 2:** results/step04_ctt_assumptions_report.txt
**Format:** Text report (same structure as IRT report)

**File 3:** plots/step04_irt_diagnostics.png
**Format:** PNG image (2x2 grid: residuals vs fitted, Q-Q, scale-location, ACF)
**Dimensions:** 800 x 600 pixels @ 300 DPI

**File 4:** plots/step04_ctt_diagnostics.png
**Format:** PNG image (same layout as IRT diagnostics)

**File 5:** results/step04_assumptions_comparison.csv
**Format:** CSV comparing assumption test results
**Columns:**
  - `model` (string: IRT, CTT)
  - `residual_normality_p` (float, Shapiro-Wilk p-value)
  - `residual_normality_pass` (boolean, p > 0.05)
  - `homoscedasticity_pass` (boolean, visual assessment)
  - `random_effects_normality_pass` (boolean, visual assessment)
  - `acf_lag1_mean` (float, mean ACF across participants)
  - `acf_lag1_pass` (boolean, mean < 0.1)
  - `overall_pass` (boolean, all checks passed)
  - `remedial_action` (string, description of remediation if applied)
**Expected Rows:** 2 (IRT, CTT)

**Validation Requirement:**
Validation tools MUST be used after assumption checking tool execution. Specific validation tools will be determined by rq_tools based on diagnostic requirements (file existence, value ranges, plot generation checks).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step04_irt_assumptions_report.txt: exists, >500 characters (comprehensive report)
- results/step04_ctt_assumptions_report.txt: exists, >500 characters
- plots/step04_irt_diagnostics.png: exists, valid PNG image
- plots/step04_ctt_diagnostics.png: exists, valid PNG image
- results/step04_assumptions_comparison.csv: 2 rows x 9 columns

*Value Ranges:*
- residual_normality_p in [0, 1] (p-value range)
- acf_lag1_mean in [-1, 1] (correlation coefficient range)
- All boolean columns in {True, False}

*Data Quality:*
- Exactly 2 rows in comparison CSV (IRT, CTT)
- Both models assessed with identical diagnostic suite
- If one model fails assumption, remedial_action documents fix applied to BOTH models
- Diagnostic plots generated successfully (PNG files valid)

*Log Validation:*
- Required pattern: "Running assumption checks for IRT model"
- Required pattern: "Running assumption checks for CTT model"
- Required pattern: "IRT residual normality: Shapiro-Wilk p = [value]"
- Required pattern: "CTT residual normality: Shapiro-Wilk p = [value]"
- Required pattern: "IRT ACF Lag-1 mean: [value]"
- Required pattern: "CTT ACF Lag-1 mean: [value]"
- Required pattern: "Assumption validation complete: [PASS/CONDITIONAL/FAIL]"
- Forbidden patterns: "ERROR", "Diagnostic plot generation failed"
- Acceptable warnings: "Slight deviation from normality (p=0.03) - acceptable for large N"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Severe assumption violation in both models - residuals non-normal (p < 0.001)")
- Log failure to logs/step04_validate_assumptions.log
- Quit script immediately
- g_debug invoked to diagnose (likely data quality issue, outliers, or model misspecification)

---

### Step 5: Extract and Compare Coefficients

**Purpose:** Extract fixed effects from both models, compare statistical significance patterns, calculate Cohen's kappa for agreement

**Dependencies:** Steps 3, 4 (requires fitted models and validated assumptions)

**Complexity:** Low (5 minutes - coefficient extraction and comparison)

**Input:**

**File 1:** results/step03_irt_lmm_fixed_effects.csv
**Source:** Generated by Step 3
**Columns:** term, estimate, SE, z, p_uncorrected
**Expected Rows:** ~10

**File 2:** results/step03_ctt_lmm_fixed_effects.csv
**Source:** Generated by Step 3
**Columns:** term, estimate, SE, z, p_uncorrected
**Expected Rows:** ~10

**Processing:**

**Significance Pattern Extraction:**
1. Merge IRT and CTT fixed effects on term (coefficient name)
2. For each coefficient, classify significance (p < 0.05 threshold):
   - IRT_sig: TRUE if p_uncorrected_irt < 0.05, else FALSE
   - CTT_sig: TRUE if p_uncorrected_ctt < 0.05, else FALSE
3. Classify agreement:
   - Both sig: agreement = TRUE
   - Both nonsig: agreement = TRUE
   - Mismatch: agreement = FALSE

**Agreement Metrics:**
1. Raw agreement percentage: sum(agreement) / total_coefficients * 100
2. Cohen's kappa (per concept.md):
   - Accounts for chance agreement
   - kappa > 0.60 = substantial agreement per Landis & Koch 1977
   - Formula: kappa = (p_o - p_e) / (1 - p_e)
     - p_o = observed agreement proportion
     - p_e = expected agreement by chance
3. Focus on interaction terms (Time x Domain):
   - Extract coefficients matching pattern: "TSVR_hours:domain" or "log(TSVR_hours+1):domain"
   - Compute kappa specifically for interaction terms (critical for trajectory comparison)

**Effect Size Comparison:**
1. Compare beta coefficients (IRT vs CTT):
   - Same sign expected (both positive or both negative)
   - Magnitude may differ due to scaling (IRT unbounded, CTT 0-1)
2. Compute ratio: beta_ctt / beta_irt (scaling factor)
3. Flag discrepancies: |beta_irt - beta_ctt| > 2*SE (substantial difference beyond scaling)

**Output:**

**File 1:** results/step05_coefficient_comparison.csv
**Format:** CSV
**Columns:**
  - `term` (string, coefficient name)
  - `estimate_irt` (float, IRT beta)
  - `SE_irt` (float, IRT standard error)
  - `p_irt` (float, IRT p-value)
  - `sig_irt` (boolean, p < 0.05)
  - `estimate_ctt` (float, CTT beta)
  - `SE_ctt` (float, CTT standard error)
  - `p_ctt` (float, CTT p-value)
  - `sig_ctt` (boolean, p < 0.05)
  - `agreement` (boolean, sig_irt == sig_ctt)
  - `beta_ratio` (float, estimate_ctt / estimate_irt)
  - `discrepancy_flag` (boolean, |beta_irt - beta_ctt| > 2*SE)
**Expected Rows:** ~10 (all fixed effects)

**File 2:** results/step05_agreement_metrics.csv
**Format:** CSV
**Columns:**
  - `metric` (string: raw_agreement_percent, cohens_kappa_all, cohens_kappa_interactions)
  - `value` (float)
  - `threshold` (float, expected value for convergence: 80% for raw agreement, 0.60 for kappa)
  - `pass` (boolean, value >= threshold)
**Expected Rows:** 3 (raw agreement, kappa all, kappa interactions)

**Validation Requirement:**
Validation tools MUST be used after coefficient comparison tool execution. Specific validation tools will be determined by rq_tools based on comparison requirements (value range checks, agreement metric validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step05_coefficient_comparison.csv: ~10 rows x 12 columns
- results/step05_agreement_metrics.csv: 3 rows x 4 columns

*Value Ranges:*
- estimate_irt unrestricted (can be positive or negative)
- estimate_ctt unrestricted
- SE_irt > 0, SE_ctt > 0
- p_irt in [0, 1], p_ctt in [0, 1]
- beta_ratio > 0 (assuming same sign for IRT and CTT)
- cohens_kappa in [-1, 1] (typically [0, 1] for agreement)
- raw_agreement_percent in [0, 100]

*Data Quality:*
- ~10 rows in coefficient comparison (all fixed effects present)
- Exactly 3 rows in agreement metrics
- No NaN in p-values or estimates (all coefficients computed)
- Expected: agreement >= 80% (strong convergence per hypothesis)
- Expected: cohens_kappa >= 0.60 (substantial agreement per Landis & Koch)
- Expected: Most beta_ratio values > 0 (same direction for IRT and CTT)

*Log Validation:*
- Required pattern: "Merged IRT and CTT coefficients: [N] terms"
- Required pattern: "Raw agreement: [X]% ([Y]/[Z] coefficients agree)"
- Required pattern: "Cohen's kappa (all terms): [value]"
- Required pattern: "Cohen's kappa (interactions only): [value]"
- Required pattern: "[N] discrepancies flagged (|beta_irt - beta_ctt| > 2*SE)"
- Forbidden patterns: "ERROR", "Missing term in one model", "NaN in p-values"
- Acceptable warnings: "Some beta_ratio values < 0 (sign disagreement - investigate)"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Cohen's kappa < 0 - indicates systematic disagreement beyond chance")
- Log failure to logs/step05_compare_coefficients.log
- Quit script immediately
- g_debug invoked to diagnose (likely model fitting error or fundamental IRT-CTT divergence)

---

### Step 6: Compare Model Fit (AIC/BIC)

**Purpose:** Compare AIC and BIC between IRT and CTT models to assess relative fit quality

**Dependencies:** Step 3 (requires fitted models with AIC/BIC)

**Complexity:** Low (2 minutes - simple arithmetic comparison)

**Input:**

**File 1:** results/step03_irt_lmm_summary.txt
**Content:** Contains AIC and BIC values for IRT model

**File 2:** results/step03_ctt_lmm_summary.txt
**Content:** Contains AIC and BIC values for CTT model

**Processing:**
1. Parse AIC from IRT summary (extract numeric value)
2. Parse AIC from CTT summary
3. Parse BIC from both summaries
4. Compute deltas:
   - delta_AIC = AIC_ctt - AIC_irt (negative = IRT better, positive = CTT better)
   - delta_BIC = BIC_ctt - BIC_irt
5. Interpret per concept.md thresholds:
   - |delta_AIC| < 2: Equivalent fit (no meaningful difference)
   - |delta_AIC| > 10: Substantial difference (strong preference for one model)
   - 2 <= |delta_AIC| <= 10: Moderate difference (weak preference)

**Output:**

**File:** results/step06_model_fit_comparison.csv
**Format:** CSV
**Columns:**
  - `model` (string: IRT, CTT)
  - `AIC` (float)
  - `BIC` (float)
  - `delta_AIC` (float, CTT - IRT, only in CTT row)
  - `delta_BIC` (float, CTT - IRT, only in CTT row)
  - `interpretation` (string: "Equivalent fit", "IRT better (weak)", "IRT better (strong)", "CTT better (weak)", "CTT better (strong)")
**Expected Rows:** 2 (IRT, CTT)

**Validation Requirement:**
Validation tools MUST be used after model fit comparison tool execution. Specific validation tools will be determined by rq_tools based on comparison requirements (AIC/BIC range checks, delta computation validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step06_model_fit_comparison.csv: 2 rows x 6 columns

*Value Ranges:*
- AIC > 0 (information criteria must be positive)
- BIC > 0
- delta_AIC unrestricted (can be negative, zero, or positive)
- delta_BIC unrestricted

*Data Quality:*
- Exactly 2 rows (IRT, CTT)
- No NaN in AIC or BIC columns
- delta values computed correctly (CTT - IRT)
- Interpretation matches delta magnitude per thresholds

*Log Validation:*
- Required pattern: "IRT model AIC: [value]"
- Required pattern: "CTT model AIC: [value]"
- Required pattern: "Delta AIC (CTT - IRT): [value]"
- Required pattern: "Delta BIC (CTT - IRT): [value]"
- Required pattern: "Interpretation: [Equivalent fit / IRT better / CTT better]"
- Forbidden patterns: "ERROR", "AIC or BIC missing from summary"
- Acceptable warnings: None expected (simple arithmetic)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "AIC not found in IRT model summary - model fitting incomplete")
- Log failure to logs/step06_compare_fit.log
- Quit script immediately
- g_debug invoked to diagnose (likely model summary parsing error)

---

### Step 7: Prepare Scatterplot Data (IRT vs CTT per Domain)

**Purpose:** Create plot source CSV for scatterplots showing IRT vs CTT correlation per domain (Option B architecture)

**Dependencies:** Steps 0, 1 (requires IRT theta and CTT scores)

**Complexity:** Low (5 minutes - data aggregation for plotting)

**Plot Description:** Scatterplots with IRT scores on x-axis, CTT scores on y-axis, separate panels per domain (What, Where, When), regression lines overlaid

**Required Data Sources:**
- data/step00_irt_theta_loaded.csv (IRT theta scores)
- data/step01_ctt_scores.csv (CTT mean scores)
- results/step02_correlations.csv (r values for annotation)

**Output (Plot Source CSV):** plots/step07_scatterplot_data.csv

**Required Columns:**
- `composite_ID` (string, participant-test identifier)
- `domain` (string, What/Where/When)
- `IRT_score` (float, IRT theta)
- `CTT_score` (float, CTT mean)
- `r` (float, correlation coefficient for domain - for plot annotation)

**Expected Rows:** 1200 (400 UID x test x 3 domains)

**Aggregation Logic:**
1. Reshape IRT theta to long format (composite_ID, domain, IRT_score)
2. Merge with CTT scores on composite_ID + domain
3. Join with correlations on domain (adds r column for annotation)
4. Select and rename columns to match required schema
5. Sort by domain, then composite_ID
6. Save to plots/step07_scatterplot_data.csv

**Input:**

**File 1:** data/step00_irt_theta_loaded.csv
**File 2:** data/step01_ctt_scores.csv
**File 3:** results/step02_correlations.csv

**Processing:**
1. Reshape IRT theta: theta_common -> What, theta_congruent -> Where, theta_incongruent -> When
2. Merge IRT and CTT on composite_ID + domain
3. Join correlations on domain (broadcast r to all rows for that domain)
4. Select columns: composite_ID, domain, IRT_score, CTT_score, r
5. Validate: No NaN in score columns, all 3 domains present

**Output:**

**File:** plots/step07_scatterplot_data.csv
**Format:** CSV
**Columns:** composite_ID, domain, IRT_score, CTT_score, r
**Expected Rows:** 1200
**Expected Domains:** What, Where, When (400 rows each)

**Validation Requirement:**
Validation tools MUST be used after plot data preparation tool execution. Specific validation tools will be determined by rq_tools based on plot data format requirements (Option B architecture validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- plots/step07_scatterplot_data.csv: 1200 rows x 5 columns (composite_ID: object, domain: object, IRT_score: float64, CTT_score: float64, r: float64)

*Value Ranges:*
- IRT_score in [-3, 3] (typical IRT ability range)
- CTT_score in [0, 1] (proportion correct)
- r in [-1, 1] (correlation coefficient)

*Data Quality:*
- Exactly 1200 rows (400 UID x test x 3 domains)
- All 3 domains present (What, Where, When)
- No NaN in IRT_score or CTT_score columns (all scores computed)
- r values match correlations from Step 2 (same per domain)
- Expected: 400 rows per domain (balanced design)

*Log Validation:*
- Required pattern: "Plot data preparation complete: 1200 rows created"
- Required pattern: "All domains represented: What, Where, When"
- Required pattern: "IRT_score range: [min, max]"
- Required pattern: "CTT_score range: [min, max]"
- Forbidden patterns: "ERROR", "NaN values detected", "Missing domain"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 1200 rows, found 900 - missing domain data")
- Log failure to logs/step07_prepare_scatterplot.log
- Quit script immediately
- g_debug invoked to diagnose (likely merge error or incomplete data)

**Plotting Function (rq_plots will call):** Scatterplot with regression lines
- rq_plots agent maps this description to specific tools/plots.py function
- Plot reads plots/step07_scatterplot_data.csv (created by this step)
- No data aggregation in rq_plots (visualization only per Option B)

---

### Step 8: Prepare Trajectory Comparison Plot Data

**Purpose:** Create plot source CSV for trajectory comparison showing IRT vs CTT trajectories over time per domain (Option B architecture)

**Dependencies:** Steps 3, 0 (requires LMM input data with TSVR)

**Complexity:** Low (5 minutes - aggregation of observed means)

**Plot Description:** Trajectory plot with time (TSVR_hours) on x-axis, ability/score on y-axis, separate panels per domain, IRT and CTT trajectories overlaid (solid = IRT, dashed = CTT)

**Required Data Sources:**
- data/step03_irt_lmm_input.csv (IRT scores with TSVR)
- data/step03_ctt_lmm_input.csv (CTT scores with TSVR)

**Output (Plot Source CSV):** plots/step08_trajectory_data.csv

**Required Columns:**
- `TSVR_hours` (float, time since encoding)
- `domain` (string, What/Where/When)
- `model` (string, IRT/CTT)
- `mean_score` (float, observed mean per time x domain x model)
- `CI_lower` (float, 95% CI lower bound)
- `CI_upper` (float, 95% CI upper bound)
- `n` (int, sample size for mean)

**Expected Rows:** ~24 (4 timepoints x 3 domains x 2 models)

**Aggregation Logic:**
1. For IRT data: Group by TSVR_hours + domain, compute mean(IRT_score), 95% CI, count
2. For CTT data: Group by TSVR_hours + domain, compute mean(CTT_score), 95% CI, count
3. Add model column: "IRT" for IRT rows, "CTT" for CTT rows
4. Stack IRT and CTT aggregations (rbind)
5. Sort by domain, model, TSVR_hours
6. Save to plots/step08_trajectory_data.csv

**Input:**

**File 1:** data/step03_irt_lmm_input.csv
**File 2:** data/step03_ctt_lmm_input.csv

**Processing:**
1. Aggregate IRT: mean_score, CI_lower, CI_upper per TSVR_hours x domain
2. Aggregate CTT: mean_score, CI_lower, CI_upper per TSVR_hours x domain
3. Add model identifier
4. Combine datasets
5. Validate: All 3 domains present, ~4 unique TSVR_hours values (timepoints), 2 models

**Output:**

**File:** plots/step08_trajectory_data.csv
**Format:** CSV
**Columns:** TSVR_hours, domain, model, mean_score, CI_lower, CI_upper, n
**Expected Rows:** ~24 (varies by exact number of unique TSVR_hours values)
**Expected Domains:** What, Where, When
**Expected Models:** IRT, CTT

**Validation Requirement:**
Validation tools MUST be used after plot data preparation tool execution. Specific validation tools will be determined by rq_tools based on plot data format requirements (Option B architecture validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- plots/step08_trajectory_data.csv: ~24 rows x 7 columns (TSVR_hours: float64, domain: object, model: object, mean_score: float64, CI_lower: float64, CI_upper: float64, n: int64)

*Value Ranges:*
- TSVR_hours in [0, 200] (hours since encoding)
- mean_score unrestricted (IRT unbounded, CTT in [0,1])
- CI_lower < mean_score < CI_upper (confidence bounds must bracket mean)
- n > 0 (sample size must be positive)

*Data Quality:*
- ~24 rows (4 timepoints x 3 domains x 2 models)
- All 3 domains present (What, Where, When)
- Both models present (IRT, CTT)
- No NaN in mean_score, CI_lower, CI_upper columns
- Expected: ~100 observations per timepoint (n ~= 100)

*Log Validation:*
- Required pattern: "Aggregated IRT trajectories: [N] timepoint x domain combinations"
- Required pattern: "Aggregated CTT trajectories: [N] timepoint x domain combinations"
- Required pattern: "Combined trajectory data: [N] rows (IRT + CTT)"
- Required pattern: "All domains represented: What, Where, When"
- Required pattern: "Both models represented: IRT, CTT"
- Forbidden patterns: "ERROR", "NaN values detected", "Missing domain or model"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected ~24 rows, found 12 - missing model data")
- Log failure to logs/step08_prepare_trajectory.log
- Quit script immediately
- g_debug invoked to diagnose (likely aggregation error or incomplete data)

**Plotting Function (rq_plots will call):** Trajectory comparison with overlaid lines
- rq_plots agent maps this description to specific tools/plots.py function
- Plot reads plots/step08_trajectory_data.csv (created by this step)
- No data aggregation in rq_plots (visualization only per Option B)

---

## Expected Data Formats

### IRT Theta Reshaping (Wide to Long)

**Input Format (from RQ 5.1):**
- File: data/step00_irt_theta_loaded.csv
- Format: Wide (one row per composite_ID)
- Columns: composite_ID, theta_common, se_common, theta_congruent, se_congruent, theta_incongruent, se_incongruent

**Reshape Logic:**
- Map dimensions to domains:
  - theta_common -> What domain (common items per RQ 5.1 design)
  - theta_congruent -> Where domain (congruent items)
  - theta_incongruent -> When domain (incongruent items)
- Create three rows per composite_ID:
  - Row 1: composite_ID, domain="What", IRT_score=theta_common, SE=se_common
  - Row 2: composite_ID, domain="Where", IRT_score=theta_congruent, SE=se_congruent
  - Row 3: composite_ID, domain="When", IRT_score=theta_incongruent, SE=se_incongruent

**Output Format:**
- File: Used internally for merging with CTT (not saved separately)
- Format: Long (one row per composite_ID x domain)
- Columns: composite_ID, domain, IRT_score, SE
- Expected Rows: 1200 (400 composite_IDs x 3 domains)

**Critical Decision:**
Dimension-to-domain mapping MUST match RQ 5.1 IRT calibration design. If RQ 5.1 used different dimension labels, adjust mapping accordingly (check RQ 5.1 1_concept.md for confirmation).

---

### CTT Computation from Raw Items

**Input Format:**
- File: data/step00_raw_data_filtered.csv
- Format: Wide (one row per UID x TEST, columns = items)
- Columns: UID, TEST, [~40-60 purified item columns]
- Values: {0, 1, NaN} (binary responses)

**Domain Assignment Logic:**
- Parse item tags: VR-{paradigm}-{test}-{domain}-{type}
- What domain: Items with `-N-` tag (e.g., VR-IFR-A01-N-ANS)
- Where domain: Items with `-L-`, `-U-`, OR `-D-` tags (aggregate all three per concept.md)
- When domain: Items with `-O-` tag (e.g., VR-IFR-A01-O-ANS)

**Aggregation Logic:**
- Group items by domain
- Compute mean per UID x TEST x domain:
  - CTT_What = mean([item1_What, item2_What, ...], na.rm=TRUE)
  - CTT_Where = mean([item1_Where, item2_Where, ...], na.rm=TRUE)
  - CTT_When = mean([item1_When, item2_When, ...], na.rm=TRUE)
- Result: CTT_score in [0, 1] (proportion correct)

**Output Format:**
- File: data/step01_ctt_scores.csv
- Format: Long (one row per UID x TEST x domain)
- Columns: composite_ID, UID, test, domain, CTT_score, n_items
- Expected Rows: 1200 (400 UID x TEST x 3 domains)

---

### Parallel LMM Input Format

**IRT LMM Input:**
- File: data/step03_irt_lmm_input.csv
- Columns: composite_ID, UID, test, domain, TSVR_hours, IRT_score
- Format: Long (one row per observation = UID x test x domain)
- Expected Rows: 1200

**CTT LMM Input:**
- File: data/step03_ctt_lmm_input.csv
- Columns: composite_ID, UID, test, domain, TSVR_hours, CTT_score
- Format: Long (one row per observation = UID x test x domain)
- Expected Rows: 1200

**Critical Requirement:**
BOTH datasets must have IDENTICAL structure:
- Same UID x test x domain combinations (no missing rows)
- Same TSVR_hours values (merged from same TSVR mapping)
- Only difference: IRT_score vs CTT_score column

**Why Identical Structure Required:**
Parallel LMM comparison requires same observations, same grouping, same time variable. Differences in data structure would confound IRT vs CTT comparison with sample size or timing differences.

---

### Column Naming Conventions

Per names.md (RQ 5.1 conventions applied):

**Core Identifiers:**
- `composite_ID` - Primary key (UID_test format)
- `UID` - Participant identifier
- `test` - Test session (T1, T2, T3, T4)

**Time Variable (Decision D070):**
- `TSVR_hours` - Actual hours since encoding (NOT nominal days 0/1/3/6)

**IRT Outputs:**
- `theta_<dimension>` - IRT ability estimate (e.g., theta_common)
- `se_<dimension>` - Standard error (e.g., se_common)

**CTT Outputs:**
- `CTT_score` - Mean proportion correct per domain
- `n_items` - Number of items contributing to mean (diagnostic)

**LMM/Plotting:**
- `domain` - Memory domain factor (What, Where, When)
- `CI_lower` - 95% confidence interval lower bound
- `CI_upper` - 95% confidence interval upper bound
- `mean_score` - Observed mean for plotting
- `model` - Model identifier (IRT, CTT) for trajectory comparison

---

## Cross-RQ Dependencies

**Dependency Type:** DERIVED Data from RQ 5.1 (requires RQ 5.1 completion)

**This RQ requires outputs from:**
- **RQ 5.1** (Domain-Specific Forgetting Trajectories)
  - File 1: results/ch5/rq1/data/step03_theta_scores.csv
    - Used in: Step 0 (IRT theta scores for comparison)
    - Rationale: RQ 5.1 calibrated IRT models and extracted theta scores. This RQ uses those theta scores as one measurement approach.
  - File 2: results/ch5/rq1/data/step00_tsvr_mapping.csv
    - Used in: Step 0 (TSVR time variable for LMM per Decision D070)
    - Rationale: TSVR provides actual hours since encoding for temporal modeling (not nominal days).
  - File 3: results/ch5/rq1/data/step02_purified_items.csv
    - Used in: Step 0 (ensures CTT uses same items as IRT for fair comparison)
    - Rationale: IRT item purification (Decision D039) removed psychometrically problematic items. CTT must use same purified set to avoid method-specific artifacts.

**Execution Order Constraint:**
1. RQ 5.1 must complete Steps 0-3 first (TSVR extraction, IRT Pass 1, purification, IRT Pass 2, theta extraction)
2. This RQ (5.11) executes after RQ 5.1 completes
3. No other RQ dependencies

**Data Source Boundaries (Per Specification 5.1.6):**
- **RAW data:** data/cache/dfData.csv (master dataset for CTT computation)
- **DERIVED data:** RQ 5.1 theta scores, TSVR mapping, purified items list
- **Scope:** This RQ does NOT re-calibrate IRT models (uses RQ 5.1 theta as fixed). CTT scores computed fresh from raw data.

**Validation:**
- Step 0: Check results/ch5/rq1/data/step03_theta_scores.csv exists (EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch5/rq1/data/step00_tsvr_mapping.csv exists (EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch5/rq1/data/step02_purified_items.csv exists (EXPECTATIONS ERROR if absent)
- If ANY file missing -> quit with error -> user must execute RQ 5.1 first

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

---

### Validation Requirements By Step

#### Step 0: Load Data from RQ 5.1 and Master Dataset

**Analysis Tool:** (determined by rq_tools - likely tools.data.load_csv or pandas.read_csv)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_data_columns + validate_numeric_range)

**What Validation Checks:**
- Output files exist (all 4 step00 files)
- Expected column counts match (7 cols for theta, 3 cols for TSVR, 4 cols for purified items, 42-62 cols for raw data)
- Expected row counts (~400 for theta/TSVR/raw, 40-60 for purified items)
- Value ranges (theta in [-3,3], TSVR in [0,200], item scores in {0,1,NaN})
- No critical missing data (all 400 composite_IDs present)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "RQ 5.1 theta file not found at results/ch5/rq1/data/step03_theta_scores.csv")
- Log failure to logs/step00_load_data.log
- Quit script immediately
- g_debug invoked to diagnose (likely RQ 5.1 incomplete or file path error)

---

#### Step 1: Compute CTT Mean Scores

**Analysis Tool:** (determined by rq_tools - likely pandas groupby + mean aggregation)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure + validate_numeric_range)

**What Validation Checks:**
- Output file exists (data/step01_ctt_scores.csv)
- Expected row count (exactly 1200 = 400 UID x test x 3 domains)
- Expected column count (6 columns)
- Value ranges (CTT_score in [0,1], n_items > 0)
- All 3 domains present (What, Where, When) for each UID x test
- No NaN in CTT_score column

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Expected 1200 rows, found 900 - missing domain data")
- Log failure to logs/step01_compute_ctt.log
- Quit script immediately
- g_debug invoked to diagnose (likely domain tag parsing error)

---

#### Step 2: Correlation Analysis (IRT vs CTT per Domain)

**Analysis Tool:** (determined by rq_tools - likely scipy.stats.pearsonr + Holm-Bonferroni correction)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_correlation_test_d068)

**What Validation Checks:**
- Output file exists (results/step02_correlations.csv)
- Expected row count (exactly 4 = What, Where, When, Overall)
- Dual p-values present (p_uncorrected AND p_holm columns per Decision D068)
- Value ranges (r in [-1,1], CI brackets r, p in [0,1], p_holm >= p_uncorrected)
- No NaN in r, CI, or p columns

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Missing p_holm column - Decision D068 requires dual p-values")
- Log failure to logs/step02_correlations.log
- Quit script immediately
- g_debug invoked to diagnose (likely dual p-value implementation missing)

---

#### Step 3: Fit Parallel LMMs (IRT Model + CTT Model)

**Analysis Tool:** (determined by rq_tools - likely tools.lmm.fit_lmm_trajectory_tsvr)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_lmm_convergence + validate_variance_positivity)

**What Validation Checks:**
- Output files exist (6 files: 2 LMM inputs, 2 summaries, 2 fixed effects CSVs, 1 convergence report)
- Expected row counts (1200 for LMM inputs, ~10 for fixed effects)
- Both models converged OR both simplified to same random structure
- AIC/BIC > 0 (information criteria valid)
- Fixed effects tables have same row count (identical structure maintained)
- Convergence report documents decisions

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Both models failed to converge even with random intercepts")
- Log failure to logs/step03_fit_lmm.log
- Quit script immediately
- g_debug invoked to diagnose (likely data quality issue or model misspecification)

---

#### Step 4: Validate LMM Assumptions (Both Models)

**Analysis Tool:** (determined by rq_tools - likely tools.validation.validate_lmm_assumptions_comprehensive)
**Validation Tool:** (determined by rq_tools - same tool performs both analysis and validation, or secondary validator checks diagnostic outputs)

**What Validation Checks:**
- Output files exist (2 assumption reports, 2 diagnostic plots, 1 comparison CSV)
- Diagnostic plots are valid PNG images
- Assumption comparison CSV has exactly 2 rows (IRT, CTT)
- p-values in [0,1], ACF in [-1,1], booleans in {True, False}
- Both models assessed with identical diagnostic suite

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Severe assumption violation - residuals non-normal (p < 0.001) for both models")
- Log failure to logs/step04_validate_assumptions.log
- Quit script immediately
- g_debug invoked to diagnose (likely data quality issue or outliers)

---

#### Step 5: Extract and Compare Coefficients

**Analysis Tool:** (determined by rq_tools - likely pandas merge + Cohen's kappa computation)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure + custom kappa validation)

**What Validation Checks:**
- Output files exist (coefficient comparison CSV, agreement metrics CSV)
- Expected row counts (~10 for coefficients, 3 for metrics)
- No NaN in p-values or estimates
- Cohen's kappa in [-1, 1] (typically [0, 1])
- Beta_ratio > 0 for most coefficients (same sign expected)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Cohen's kappa < 0 - systematic disagreement beyond chance")
- Log failure to logs/step05_compare_coefficients.log
- Quit script immediately
- g_debug invoked to diagnose (likely model fitting error or fundamental divergence)

---

#### Step 6: Compare Model Fit (AIC/BIC)

**Analysis Tool:** (determined by rq_tools - likely simple arithmetic on parsed AIC/BIC values)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure + AIC positivity check)

**What Validation Checks:**
- Output file exists (model fit comparison CSV)
- Expected row count (exactly 2 = IRT, CTT)
- AIC > 0, BIC > 0 (information criteria valid)
- Delta values computed correctly (CTT - IRT)
- Interpretation matches delta magnitude

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "AIC not found in IRT model summary - model fitting incomplete")
- Log failure to logs/step06_compare_fit.log
- Quit script immediately
- g_debug invoked to diagnose (likely model summary parsing error)

---

#### Step 7: Prepare Scatterplot Data (IRT vs CTT per Domain)

**Analysis Tool:** (determined by rq_tools - likely pandas merge + reshape)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_plot_data_completeness + validate_numeric_range)

**What Validation Checks:**
- Output file exists (plots/step07_scatterplot_data.csv)
- Expected row count (exactly 1200 = 400 UID x test x 3 domains)
- All 3 domains present (What, Where, When)
- No NaN in IRT_score or CTT_score columns
- r values match correlations from Step 2

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Expected 1200 rows, found 900 - missing domain data")
- Log failure to logs/step07_prepare_scatterplot.log
- Quit script immediately
- g_debug invoked to diagnose (likely merge error)

---

#### Step 8: Prepare Trajectory Comparison Plot Data

**Analysis Tool:** (determined by rq_tools - likely pandas groupby + mean aggregation)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_plot_data_completeness + validate_numeric_range)

**What Validation Checks:**
- Output file exists (plots/step08_trajectory_data.csv)
- Expected row count (~24 = 4 timepoints x 3 domains x 2 models)
- All 3 domains present (What, Where, When)
- Both models present (IRT, CTT)
- No NaN in mean_score, CI_lower, CI_upper columns
- CI_lower < mean_score < CI_upper

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Expected ~24 rows, found 12 - missing model data")
- Log failure to logs/step08_prepare_trajectory.log
- Quit script immediately
- g_debug invoked to diagnose (likely aggregation error)

---

## Summary

**Total Steps:** 9 (Step 0 = data loading, Steps 1-8 = analysis and plotting)

**Estimated Runtime:** 30-60 minutes total
- Data loading/preparation: ~10 minutes (Steps 0-1)
- Correlation analysis: ~5 minutes (Step 2)
- LMM fitting: ~30-40 minutes (Step 3 - high complexity due to convergence testing)
- Assumption validation: ~10 minutes (Step 4)
- Coefficient comparison: ~5 minutes (Steps 5-6)
- Plot data preparation: ~10 minutes (Steps 7-8)

**Cross-RQ Dependencies:** RQ 5.1 (requires theta scores, TSVR mapping, purified items)

**Primary Outputs:**
- Correlation results: results/step02_correlations.csv (r values, 95% CIs, dual p-values per Decision D068)
- LMM summaries: results/step03_irt_lmm_summary.txt, results/step03_ctt_lmm_summary.txt
- Coefficient comparison: results/step05_coefficient_comparison.csv (significance agreement, Cohen's kappa)
- Model fit comparison: results/step06_model_fit_comparison.csv (AIC/BIC deltas)
- Plot source CSVs: plots/step07_scatterplot_data.csv, plots/step08_trajectory_data.csv

**Validation Coverage:** 100% (all 9 steps have validation requirements with 4-layer substance criteria)

**Key Methodological Features:**
- Paired comparison design (IRT vs CTT on same participants/tests/domains)
- Identical LMM structures (isolates scaling differences from model structure differences)
- Holm-Bonferroni multiple testing correction (4 correlation tests)
- Cohen's kappa for significance agreement (accounts for chance agreement)
- Comprehensive LMM assumption validation (normality, homoscedasticity, ACF, random effects)
- Decision D068 compliance (dual p-value reporting)
- Decision D070 compliance (TSVR time variable)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-11-27): Initial plan created by rq_planner agent for RQ 5.11 (IRT-CTT convergent validity)
