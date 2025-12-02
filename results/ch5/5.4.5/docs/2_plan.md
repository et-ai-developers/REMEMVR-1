# Analysis Plan: RQ 5.4.5 - Purified CTT Effects

**Research Question:** 5.4.5
**Created:** 2025-12-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines measurement convergence between IRT theta scores and CTT mean scores computed using purified (IRT-retained) items versus full (all items) for three schema congruence levels (Common, Congruent, Incongruent). The central question: **Does IRT-based item purification yield CTT scores that converge more strongly with IRT theta estimates?**

**Analysis Pipeline:** CTT score computation (Full and Purified item sets) -> Correlation analysis (Steiger's z-test for dependent correlations) -> Reliability assessment (Cronbach's alpha) -> Z-standardization for comparability -> Parallel LMMs (IRT, Full CTT, Purified CTT) -> AIC comparison -> Plot data preparation for visualization.

**Pipeline Type:** Classical Test Theory (CTT) with convergence validation

**Steps:** 9 steps planned (Step 0: dependency verification + Steps 1-8: analysis)

**Estimated Runtime:** Low-Medium complexity (~20-30 minutes total)
- Step 0-4: Low (data loading, CTT computation, reliability)
- Step 5-6: Low (correlation analysis, z-standardization)
- Step 7: Medium (3 LMMs x 3 congruence levels = 9 model fits)
- Step 8: Low (plot data preparation)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting for Steiger's z-test (uncorrected + Bonferroni for 3 congruence levels, alpha = 0.0167)
- Decision D070: TSVR as LMM time variable (inherited from RQ 5.4.1 outputs)
- Z-standardization for LMM coefficient comparability (concept lines 121-139)
- Bivariate normality check for Steiger's z-test (concept lines 140-147)

**Data Source:** DERIVED from RQ 5.4.1 outputs (purified_items.csv, theta_scores.csv, tsvr_mapping.csv) + RAW from dfData.csv (binary responses for CTT computation)

---

## Analysis Plan

This RQ requires 9 steps (Step 0 = dependency verification, Steps 1-8 = analysis):

### Step 0: Verify Dependencies and Load RQ 5.4.1 Outputs

**Dependencies:** None (first step - dependency verification)
**Complexity:** Low (file existence checks + data loading, <2 minutes)

**Purpose:** Verify RQ 5.4.1 has completed successfully and load required outputs for CTT computation and convergence analysis.

**Input:**

**File 1:** results/ch5/5.4.1/status.yaml
**Source:** RQ 5.4.1 workflow tracking
**Format:** YAML
**Required Fields:**
  - rq_results.status = "success" (confirms RQ 5.4.1 complete)

**File 2:** results/ch5/5.4.1/data/step02_purified_items.csv
**Source:** RQ 5.4.1 Step 2 (item purification per Decision D039)
**Format:** CSV with columns:
  - item_code (string): Item identifier (e.g., VR-IFR-A01-N-ANS-i1)
  - dimension (string): Congruence level (Common, Congruent, Incongruent)
  - a (float): Item discrimination (all > 0.4 after purification)
  - b (float): Item difficulty (all |b| <= 3.0 after purification)
  - retained (bool): TRUE for all rows (only retained items in this file)
**Expected Rows:** 36-40 items (70-80% retention from ~48-52 original items)

**File 3:** results/ch5/5.4.1/data/step03_theta_scores.csv
**Source:** RQ 5.4.1 Step 3 (IRT calibration Pass 2)
**Format:** CSV with columns:
  - composite_ID (string): UID_test format (e.g., P001_T1)
  - theta_common (float): IRT ability for Common items
  - theta_congruent (float): IRT ability for Congruent items
  - theta_incongruent (float): IRT ability for Incongruent items
  - se_common (float): Standard error for Common theta
  - se_congruent (float): Standard error for Congruent theta
  - se_incongruent (float): Standard error for Incongruent theta
**Expected Rows:** ~400 (100 participants x 4 tests)

**File 4:** results/ch5/5.4.1/data/step00_tsvr_mapping.csv
**Source:** RQ 5.4.1 Step 0 (TSVR extraction)
**Format:** CSV with columns:
  - composite_ID (string): UID_test format
  - TSVR_hours (float): Time since VR encoding in hours
  - test (string): Test session identifier (T1, T2, T3, T4)
**Expected Rows:** ~400

**File 5:** data/cache/dfData.csv (RAW data source)
**Source:** Project-level raw data cache
**Format:** Long-format CSV with columns:
  - composite_ID (string): UID_test format
  - item_code (string): Item identifier
  - response (int): Binary response (0=incorrect, 1=correct)
**Purpose:** Binary responses needed for CTT mean score computation (both Full and Purified item sets)

**Processing:**
1. Read RQ 5.4.1 status.yaml and verify rq_results.status = "success"
2. If RQ 5.4.1 incomplete: Quit with EXPECTATIONS ERROR ("RQ 5.4.1 must complete before RQ 5.4.5")
3. Load step02_purified_items.csv -> Extract retained item codes by congruence dimension
4. Load step03_theta_scores.csv -> IRT theta estimates (3 dimensions x 400 observations)
5. Load step00_tsvr_mapping.csv -> TSVR time variable for LMM
6. Load dfData.csv -> Filter to congruence-relevant items (i1/i2=Common, i3/i4=Congruent, i5/i6=Incongruent)

**Output:**

**File 1:** data/step00_dependency_check.txt
**Format:** Text report documenting dependency verification
**Content:**
  - RQ 5.4.1 status: success/incomplete
  - Files loaded: List of 4 files with row counts
  - Item counts by congruence: Common (retained/total), Congruent (retained/total), Incongruent (retained/total)
  - Theta availability: 400 observations x 3 dimensions confirmed
**Purpose:** Audit trail for dependency verification

**File 2:** data/step00_full_item_list.csv
**Format:** CSV with columns:
  - item_code (string): All items from dfData.csv with i1-i6 tags
  - dimension (string): Congruence level (Common, Congruent, Incongruent)
  - retained (bool): TRUE if in purified_items.csv, FALSE if removed
**Expected Rows:** 48-52 items (all items before purification)
**Purpose:** Map which items are Full-only vs Purified

**Validation Requirement:**
Validation tools MUST be used after dependency verification execution. Specific validation tools determined by rq_tools based on file existence and data format requirements. The rq_analysis agent will embed validation tool calls after the dependency check for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_check.txt exists (exact path)
- data/step00_full_item_list.csv: 48-52 rows x 3 columns (item_code: object, dimension: object, retained: bool)

*Value Ranges:*
- dimension in {Common, Congruent, Incongruent} (categorical)
- retained: boolean only (True/False)
- Item counts: 36-40 retained (TRUE), 8-16 removed (FALSE)

*Data Quality:*
- No NaN values in item_code or dimension columns
- All purified_items.csv items must have retained=TRUE in full_item_list.csv
- Expected retention rate: 70-80% per congruence level
- No duplicate item_codes (each item listed once)

*Log Validation:*
- Required pattern: "RQ 5.4.1 status: success"
- Required pattern: "Loaded 4 dependency files"
- Required pattern: "Item mapping complete: [N] total items, [M] retained"
- Forbidden patterns: "ERROR", "RQ 5.4.1 incomplete", "File not found"

**Expected Behavior on Validation Failure:**
- If RQ 5.4.1 status != "success": Quit with EXPECTATIONS ERROR, log to logs/step00_verify_dependencies.log
- If any dependency file missing: Quit with EXPECTATIONS ERROR, specify which file
- If retention rate < 60% or > 90%: Log warning (acceptable but unusual), continue
- If validation fails: g_debug invoked to diagnose root cause

---

### Step 1: Map Retained vs Removed Items by Congruence Category

**Dependencies:** Step 0 (requires full_item_list.csv with retention flags)
**Complexity:** Low (filtering and aggregation, <1 minute)

**Purpose:** Quantify item purification effects separately for Common, Congruent, and Incongruent congruence levels to test whether purification differentially affects congruence categories.

**Input:**

**File:** data/step00_full_item_list.csv
**Source:** Step 0 output
**Format:** CSV with columns:
  - item_code (string)
  - dimension (string): Common, Congruent, Incongruent
  - retained (bool): TRUE=purified set, FALSE=removed by D039

**Processing:**
1. Group by dimension (Common, Congruent, Incongruent)
2. Count retained (TRUE) vs removed (FALSE) per dimension
3. Compute retention rate: N_retained / (N_retained + N_removed)
4. Test whether retention rates differ across congruence levels (chi-square test, report dual p-values per D068)

**Output:**

**File:** data/step01_item_mapping.csv
**Format:** CSV with columns:
  - dimension (string): Congruence level
  - N_total (int): Total items before purification
  - N_retained (int): Items retained after purification
  - N_removed (int): Items removed by purification
  - retention_rate (float): N_retained / N_total
**Expected Rows:** 3 (one per congruence level)

**Validation Requirement:**
Validation tools MUST be used after item mapping execution. Specific validation tools determined by rq_tools based on aggregation correctness and retention rate plausibility.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_item_mapping.csv: 3 rows x 5 columns (dimension: object, N_total: int64, N_retained: int64, N_removed: int64, retention_rate: float64)

*Value Ranges:*
- N_total: 14-20 per dimension (expected item count range)
- N_retained: 10-16 per dimension (70-80% retention)
- N_removed: 2-8 per dimension (20-30% exclusion)
- retention_rate in [0.6, 0.9] (60-90% retention plausible)
- N_total = N_retained + N_removed (accounting identity)

*Data Quality:*
- Exactly 3 rows (Common, Congruent, Incongruent)
- No NaN values
- Sum of N_total across dimensions = 48-52 (matches step00_full_item_list.csv)
- All retention_rate values > 0 (cannot have zero items retained)

*Log Validation:*
- Required pattern: "Item mapping complete: 3 congruence levels"
- Required pattern: "Retention rates: Common=[X]%, Congruent=[Y]%, Incongruent=[Z]%"
- Forbidden patterns: "ERROR", "retention_rate = 0", "NaN detected"

**Expected Behavior on Validation Failure:**
- If retention_rate < 0.5 for any dimension: Quit with error (too few items for reliable CTT)
- If retention_rate > 0.95 for any dimension: Log warning (purification had minimal effect)
- If N_total != N_retained + N_removed: Quit with error (accounting violation)
- If validation fails: g_debug invoked

---

### Step 2: Compute Full CTT Mean Scores

**Dependencies:** Step 0 (requires dfData.csv binary responses, step00_full_item_list.csv)
**Complexity:** Low (mean computation, <2 minutes)

**Purpose:** Compute CTT mean scores using ALL items (before purification) separately for each congruence level. These Full CTT scores serve as baseline for comparison with Purified CTT scores.

**Input:**

**File 1:** data/cache/dfData.csv
**Source:** Project-level raw data
**Format:** Long-format CSV with composite_ID, item_code, response (0/1)

**File 2:** data/step00_full_item_list.csv
**Source:** Step 0 output
**Required Columns:** item_code, dimension (to filter by congruence)

**Processing:**
1. Filter dfData.csv to items in step00_full_item_list.csv (all items, retained + removed)
2. Group by composite_ID and dimension
3. Compute mean(response) per group -> CTT proportion correct [0, 1]
4. Pivot to wide format: composite_ID x 3 congruence columns (ctt_full_common, ctt_full_congruent, ctt_full_incongruent)

**Output:**

**File:** data/step02_ctt_full_scores.csv
**Format:** CSV, wide format
**Columns:**
  - composite_ID (string): UID_test format
  - ctt_full_common (float): Full CTT score for Common items
  - ctt_full_congruent (float): Full CTT score for Congruent items
  - ctt_full_incongruent (float): Full CTT score for Incongruent items
**Expected Rows:** ~400 (100 participants x 4 tests)

**Validation Requirement:**
Validation tools MUST be used after CTT computation execution. Specific validation tools determined by rq_tools based on CTT score range validation and missing data checks.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_ctt_full_scores.csv: ~400 rows x 4 columns (composite_ID: object, ctt_full_common: float64, ctt_full_congruent: float64, ctt_full_incongruent: float64)

*Value Ranges:*
- All CTT scores in [0, 1] (proportion correct scale)
- Mean CTT scores expected ~0.4-0.7 (moderate difficulty)
- SD CTT scores expected ~0.15-0.25 (reasonable variance)

*Data Quality:*
- No NaN values (all participants have responses for all congruence levels)
- All composite_IDs unique (no duplicates)
- Expected N: 400 rows (100 participants x 4 tests, no exclusions)
- Distribution approximately normal (Central Limit Theorem with N=14-20 items per score)

*Log Validation:*
- Required pattern: "CTT Full scores computed: 400 observations x 3 congruence levels"
- Required pattern: "Value ranges: Common [min-max], Congruent [min-max], Incongruent [min-max]"
- Forbidden patterns: "ERROR", "NaN detected", "Out of bounds [0,1]"

**Expected Behavior on Validation Failure:**
- If any CTT score < 0 or > 1: Quit with error (impossible values)
- If NaN values detected: Quit with error (missing data not expected)
- If N != 400: Quit with error (data loss)
- If validation fails: g_debug invoked

---

### Step 3: Compute Purified CTT Mean Scores

**Dependencies:** Step 0 (requires dfData.csv, purified_items.csv)
**Complexity:** Low (mean computation, <2 minutes)

**Purpose:** Compute CTT mean scores using ONLY purified items (retained after Decision D039 thresholds) separately for each congruence level. These Purified CTT scores should converge more strongly with IRT theta than Full CTT scores.

**Input:**

**File 1:** data/cache/dfData.csv
**Source:** Project-level raw data
**Format:** Long-format CSV with composite_ID, item_code, response (0/1)

**File 2:** results/ch5/5.4.1/data/step02_purified_items.csv
**Source:** RQ 5.4.1 Step 2 (loaded in Step 0)
**Required Columns:** item_code, dimension (only retained items)

**Processing:**
1. Filter dfData.csv to items in purified_items.csv (retained items only, ~70-80% of Full)
2. Group by composite_ID and dimension
3. Compute mean(response) per group -> CTT proportion correct [0, 1]
4. Pivot to wide format: composite_ID x 3 congruence columns (ctt_purified_common, ctt_purified_congruent, ctt_purified_incongruent)

**Output:**

**File:** data/step03_ctt_purified_scores.csv
**Format:** CSV, wide format
**Columns:**
  - composite_ID (string): UID_test format
  - ctt_purified_common (float): Purified CTT score for Common items
  - ctt_purified_congruent (float): Purified CTT score for Congruent items
  - ctt_purified_incongruent (float): Purified CTT score for Incongruent items
**Expected Rows:** ~400 (100 participants x 4 tests)

**Validation Requirement:**
Validation tools MUST be used after CTT computation execution. Specific validation tools determined by rq_tools based on CTT score range validation and missing data checks.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_ctt_purified_scores.csv: ~400 rows x 4 columns (composite_ID: object, ctt_purified_common: float64, ctt_purified_congruent: float64, ctt_purified_incongruent: float64)

*Value Ranges:*
- All CTT scores in [0, 1] (proportion correct scale)
- Mean CTT scores expected ~0.42-0.72 (slightly higher than Full due to item removal)
- SD CTT scores expected ~0.14-0.24 (possibly lower variance with fewer items)

*Data Quality:*
- No NaN values (all participants have responses for retained items)
- All composite_IDs unique (no duplicates)
- Expected N: 400 rows (same as Full CTT)
- Distribution approximately normal

*Log Validation:*
- Required pattern: "CTT Purified scores computed: 400 observations x 3 congruence levels"
- Required pattern: "Value ranges: Common [min-max], Congruent [min-max], Incongruent [min-max]"
- Forbidden patterns: "ERROR", "NaN detected", "Out of bounds [0,1]"

**Expected Behavior on Validation Failure:**
- If any CTT score < 0 or > 1: Quit with error (impossible values)
- If NaN values detected: Quit with error (missing data not expected)
- If N != 400: Quit with error (data loss)
- If validation fails: g_debug invoked

---

### Step 4: Cronbach's Alpha Reliability Assessment

**Dependencies:** Steps 2-3 (requires Full and Purified CTT scores)
**Complexity:** Low (reliability computation with bootstrap, <3 minutes)

**Purpose:** Assess internal consistency reliability (Cronbach's alpha) for Full and Purified CTT scores separately per congruence level. Purified scores expected to show equal or slightly higher alpha due to removal of low-discrimination items.

**Input:**

**File 1:** data/cache/dfData.csv
**Source:** Project-level raw data
**Format:** Long-format with binary item responses

**File 2:** data/step00_full_item_list.csv
**Source:** Step 0 (item mapping with retained flags)

**Processing:**
1. For each congruence level (Common, Congruent, Incongruent):
   a. Full CTT: Extract binary responses for all items (retained + removed)
   b. Purified CTT: Extract binary responses for retained items only
   c. Compute Cronbach's alpha with 1000 bootstrap iterations for 95% CI
   d. Compare Full alpha vs Purified alpha (expect Purified >= Full)

**Output:**

**File:** data/step04_reliability_assessment.csv
**Format:** CSV with columns:
  - dimension (string): Congruence level
  - alpha_full (float): Cronbach's alpha for Full item set
  - alpha_full_CI_lower (float): Lower 95% CI for Full alpha
  - alpha_full_CI_upper (float): Upper 95% CI for Full alpha
  - alpha_purified (float): Cronbach's alpha for Purified item set
  - alpha_purified_CI_lower (float): Lower 95% CI for Purified alpha
  - alpha_purified_CI_upper (float): Upper 95% CI for Purified alpha
  - delta_alpha (float): alpha_purified - alpha_full
**Expected Rows:** 3 (one per congruence level)

**Validation Requirement:**
Validation tools MUST be used after reliability computation execution. Specific validation tools determined by rq_tools based on alpha range validation and CI validity checks.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_reliability_assessment.csv: 3 rows x 8 columns (dimension: object, all alpha values: float64)

*Value Ranges:*
- All alpha values in [0, 1] (reliability coefficient bounds)
- Expected alpha_full: 0.65-0.85 (acceptable to good reliability)
- Expected alpha_purified: 0.68-0.88 (equal or slightly higher than Full)
- delta_alpha in [-0.05, 0.10] (small positive expected, small negative acceptable)
- CI_lower < alpha < CI_upper for all estimates (interval validity)

*Data Quality:*
- Exactly 3 rows (Common, Congruent, Incongruent)
- No NaN values
- All CIs non-negative width (CI_upper > CI_lower)
- Bootstrap CIs should not include 1.0 (perfect reliability unlikely)

*Log Validation:*
- Required pattern: "Reliability assessment complete: 3 congruence levels"
- Required pattern: "Bootstrap iterations: 1000"
- Required pattern: "Alpha Full: [values], Alpha Purified: [values]"
- Forbidden patterns: "ERROR", "alpha > 1.0", "CI width negative"

**Expected Behavior on Validation Failure:**
- If any alpha < 0.5: Log warning (questionable reliability, acceptable for exploratory analysis)
- If any alpha > 1.0: Quit with error (impossible value)
- If delta_alpha < -0.10: Log warning (purification reduced reliability unexpectedly)
- If validation fails: g_debug invoked

---

### Step 5: Correlation Analysis with Steiger's Z-Test

**Dependencies:** Steps 0, 2-3 (requires IRT theta, Full CTT, Purified CTT scores)
**Complexity:** Low (correlation + hypothesis test, <2 minutes)

**Purpose:** Test primary hypothesis that Purified CTT correlates more strongly with IRT theta than Full CTT (expected delta_r ~ +0.02). Use Steiger's z-test for dependent correlations with Bonferroni correction for 3 comparisons (alpha = 0.0167 per Decision D068).

**Input:**

**File 1:** results/ch5/5.4.1/data/step03_theta_scores.csv
**Source:** RQ 5.4.1 Step 3 (loaded in Step 0)
**Columns:** composite_ID, theta_common, theta_congruent, theta_incongruent

**File 2:** data/step02_ctt_full_scores.csv
**Source:** Step 2
**Columns:** composite_ID, ctt_full_common, ctt_full_congruent, ctt_full_incongruent

**File 3:** data/step03_ctt_purified_scores.csv
**Source:** Step 3
**Columns:** composite_ID, ctt_purified_common, ctt_purified_congruent, ctt_purified_incongruent

**Processing:**
1. Merge all three files on composite_ID
2. For each congruence level (Common, Congruent, Incongruent):
   a. Compute Pearson r: theta vs ctt_full (r_full)
   b. Compute Pearson r: theta vs ctt_purified (r_purified)
   c. Compute delta_r = r_purified - r_full
   d. Steiger's z-test for dependent correlations (tests whether r_purified significantly differs from r_full)
   e. Report BOTH p_uncorrected and p_bonferroni (Bonferroni correction for 3 tests: alpha = 0.05/3 = 0.0167 per D068)
3. Check bivariate normality assumption for Steiger's test (scatter plot inspection + Mardia's test per concept lines 140-147)
4. If normality violated: Report bootstrap CIs for delta_r as sensitivity analysis

**Output:**

**File:** data/step05_correlation_analysis.csv
**Format:** CSV with columns:
  - dimension (string): Congruence level
  - r_full (float): Pearson r for Full CTT vs IRT theta
  - r_purified (float): Pearson r for Purified CTT vs IRT theta
  - delta_r (float): r_purified - r_full
  - steiger_z (float): Z-statistic from Steiger's test
  - p_uncorrected (float): Uncorrected p-value
  - p_bonferroni (float): Bonferroni-corrected p-value (alpha = 0.0167)
  - normality_check (string): "PASS" if bivariate normal, "FAIL" with remediation
  - N (int): Sample size for correlation (should be 400)
**Expected Rows:** 3 (one per congruence level)

**Validation Requirement:**
Validation tools MUST be used after correlation analysis execution. Specific validation tools determined by rq_tools based on correlation range validation and dual p-value reporting per Decision D068.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_correlation_analysis.csv: 3 rows x 9 columns (dimension: object, r_full: float64, r_purified: float64, delta_r: float64, steiger_z: float64, p_uncorrected: float64, p_bonferroni: float64, normality_check: object, N: int64)

*Value Ranges:*
- r_full in [0.60, 0.90] (strong positive correlation expected)
- r_purified in [0.62, 0.92] (equal or slightly higher than r_full)
- delta_r in [-0.05, 0.10] (small positive improvement expected)
- steiger_z unrestricted (can be positive or negative)
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1], p_bonferroni = min(p_uncorrected x 3, 1.0)
- N = 400 for all rows (complete data)

*Data Quality:*
- Exactly 3 rows
- No NaN values in numeric columns
- Dual p-values present per Decision D068 (both p_uncorrected and p_bonferroni)
- normality_check in {"PASS", "FAIL - bootstrap CIs reported"}

*Log Validation:*
- Required pattern: "Correlation analysis complete: 3 congruence levels"
- Required pattern: "Dual p-values reported per Decision D068"
- Required pattern: "Bonferroni alpha = 0.0167 (3 comparisons)"
- Required pattern: "Bivariate normality check: [results]"
- Forbidden patterns: "ERROR", "r > 1.0", "p-value missing"

**Expected Behavior on Validation Failure:**
- If any r_full or r_purified outside [-1, 1]: Quit with error (impossible correlation)
- If p_bonferroni != min(p_uncorrected x 3, 1.0): Quit with error (correction formula wrong)
- If normality_check = "FAIL" but no bootstrap CIs: Quit with error (remediation missing)
- If validation fails: g_debug invoked

---

### Step 6: Z-Standardize All Measurements

**Dependencies:** Steps 0, 2-3 (requires IRT theta, Full CTT, Purified CTT scores)
**Complexity:** Low (standardization, <1 minute)

**Purpose:** Z-standardize IRT theta, Full CTT, and Purified CTT scores to enable direct comparison of LMM regression coefficients across measurement types. Standardization ensures all scores have mean = 0, SD = 1 per concept lines 121-139.

**Input:**

**File 1:** results/ch5/5.4.1/data/step03_theta_scores.csv
**Columns:** composite_ID, theta_common, theta_congruent, theta_incongruent

**File 2:** data/step02_ctt_full_scores.csv
**Columns:** composite_ID, ctt_full_common, ctt_full_congruent, ctt_full_incongruent

**File 3:** data/step03_ctt_purified_scores.csv
**Columns:** composite_ID, ctt_purified_common, ctt_purified_congruent, ctt_purified_incongruent

**Processing:**
1. Merge all three files on composite_ID
2. For each score column:
   a. Grand-mean center: score_c = score - mean(score)
   b. Scale to unit variance: score_z = score_c / SD(score_c)
   c. Verify: mean(score_z) ~ 0 (tolerance: |mean| < 0.01), SD(score_z) ~ 1 (tolerance: |SD - 1| < 0.01)
3. Create z-standardized versions of all 9 columns (3 IRT + 3 Full + 3 Purified)

**Output:**

**File:** data/step06_standardized_scores.csv
**Format:** CSV with columns:
  - composite_ID (string)
  - z_theta_common, z_theta_congruent, z_theta_incongruent (float): Z-standardized IRT theta
  - z_ctt_full_common, z_ctt_full_congruent, z_ctt_full_incongruent (float): Z-standardized Full CTT
  - z_ctt_purified_common, z_ctt_purified_congruent, z_ctt_purified_incongruent (float): Z-standardized Purified CTT
  - TSVR_hours (float): Time variable from RQ 5.4.1 (not standardized, used as-is)
**Expected Rows:** ~400

**Validation Requirement:**
Validation tools MUST be used after z-standardization execution. Specific validation tools determined by rq_tools based on standardization validation (mean ~ 0, SD ~ 1).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_standardized_scores.csv: ~400 rows x 11 columns (composite_ID: object, 9 z-scores: float64, TSVR_hours: float64)

*Value Ranges:*
- All z-scores: typically in [-3, 3] (3 SD range covers 99.7% of normal distribution)
- mean(z_*) in [-0.01, 0.01] for all 9 z-score columns (near-zero mean)
- SD(z_*) in [0.99, 1.01] for all 9 z-score columns (unit variance)
- TSVR_hours in [0, 168] hours (unchanged from input)

*Data Quality:*
- No NaN values in any column
- All composite_IDs unique
- Expected N: 400 rows (no data loss)
- Distribution of z-scores approximately standard normal (mean=0, SD=1)

*Log Validation:*
- Required pattern: "Z-standardization complete: 9 score columns"
- Required pattern: "Verification: mean ~ 0, SD ~ 1 for all columns"
- Required pattern: "Standardization criteria met (tolerance: 0.01)"
- Forbidden patterns: "ERROR", "Mean out of tolerance", "SD out of tolerance"

**Expected Behavior on Validation Failure:**
- If |mean(z_*)| > 0.01 for any column: Quit with error (standardization failed)
- If |SD(z_*) - 1| > 0.01 for any column: Quit with error (standardization failed)
- If NaN values detected: Quit with error (data loss)
- If validation fails: g_debug invoked

---

### Step 7: Fit Parallel LMMs and Compare AIC

**Dependencies:** Step 6 (requires z-standardized scores), Step 0 (requires TSVR mapping)
**Complexity:** Medium (9 LMM fits: 3 score types x 3 congruence levels, ~10-15 minutes)

**Purpose:** Fit parallel LMMs with identical formula structure for IRT theta, Full CTT, and Purified CTT scores to test whether Purified CTT yields better model fit (lower AIC) than Full CTT. This tests secondary hypothesis that purification improves measurement quality.

**Input:**

**File:** data/step06_standardized_scores.csv
**Source:** Step 6
**Columns:** composite_ID, 9 z-standardized scores, TSVR_hours

**Processing:**
1. Extract UID from composite_ID for random effects grouping
2. For each congruence level (Common, Congruent, Incongruent):
   a. Fit LMM_IRT: z_theta ~ TSVR_hours + (TSVR_hours | UID)
   b. Fit LMM_Full: z_ctt_full ~ TSVR_hours + (TSVR_hours | UID)
   c. Fit LMM_Purified: z_ctt_purified ~ TSVR_hours + (TSVR_hours | UID)
   d. Extract AIC for all 3 models
   e. Compute delta_AIC = AIC_Purified - AIC_Full (negative = Purified better)
   f. Apply Burnham & Anderson threshold: |delta_AIC| > 2 = meaningful difference
3. Check LMM convergence for all 9 models (validate per tools.validation.validate_lmm_convergence)
4. Check LMM assumptions (residuals normality, homoscedasticity) per tools.validation.validate_lmm_assumptions_comprehensive

**Output:**

**File 1:** data/step07_lmm_model_comparison.csv
**Format:** CSV with columns:
  - dimension (string): Congruence level
  - AIC_IRT (float): AIC for IRT theta model
  - AIC_Full (float): AIC for Full CTT model
  - AIC_Purified (float): AIC for Purified CTT model
  - delta_AIC_Full_Purified (float): AIC_Purified - AIC_Full (negative = Purified better)
  - improvement (string): "Yes" if |delta_AIC| > 2, "No" otherwise
  - N (int): Sample size (400 per model)
**Expected Rows:** 3 (one per congruence level)

**File 2:** data/step07_lmm_summaries_theta.txt
**Format:** Text file with full LMM summaries for 3 IRT theta models

**File 3:** data/step07_lmm_summaries_full.txt
**Format:** Text file with full LMM summaries for 3 Full CTT models

**File 4:** data/step07_lmm_summaries_purified.txt
**Format:** Text file with full LMM summaries for 3 Purified CTT models

**Validation Requirement:**
Validation tools MUST be used after LMM fitting execution. Specific validation tools determined by rq_tools based on LMM convergence validation and assumption checks.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_lmm_model_comparison.csv: 3 rows x 7 columns (dimension: object, AIC values: float64, delta_AIC: float64, improvement: object, N: int64)
- data/step07_lmm_summaries_theta.txt exists
- data/step07_lmm_summaries_full.txt exists
- data/step07_lmm_summaries_purified.txt exists

*Value Ranges:*
- All AIC values > 0 (log-likelihood based, positive for typical sample sizes)
- delta_AIC_Full_Purified in [-20, 20] (typical AIC difference range)
- Expected delta_AIC ~ -2 to -5 (small improvement for Purified)
- N = 400 for all models (complete data)

*Data Quality:*
- Exactly 3 rows
- No NaN values
- improvement in {"Yes", "No"} (categorical)
- All 9 models converged successfully (check logs for "Convergence: True")

*Log Validation:*
- Required pattern: "LMM fitting complete: 9 models (3 score types x 3 congruence levels)"
- Required pattern: "All models converged: True"
- Required pattern: "AIC comparison: [results]"
- Required pattern: "Assumption checks passed: [results]"
- Forbidden patterns: "ERROR", "Model convergence failed", "AIC = NaN"

**Expected Behavior on Validation Failure:**
- If any model fails to converge: Log warning, report convergence status in output, continue
- If AIC_Purified > AIC_Full for all 3 dimensions: Log warning (unexpected pattern)
- If any AIC = NaN: Quit with error (model fitting error)
- If validation fails: g_debug invoked

---

### Step 8: Prepare Plot Data for Visualization

**Dependencies:** Steps 5, 7 (requires correlation analysis, LMM comparison)
**Complexity:** Low (data aggregation for plots, <2 minutes)

**Purpose:** Create plot source CSVs for two visualizations: (1) Correlation comparison (r_full vs r_purified by congruence), (2) AIC comparison (AIC_Full vs AIC_Purified by congruence). These CSVs will be read by rq_plots agent to generate final PNG visualizations.

**Input:**

**File 1:** data/step05_correlation_analysis.csv
**Source:** Step 5
**Columns:** dimension, r_full, r_purified, delta_r

**File 2:** data/step07_lmm_model_comparison.csv
**Source:** Step 7
**Columns:** dimension, AIC_Full, AIC_Purified, delta_AIC_Full_Purified

**Processing:**

**Plot 1 - Correlation Comparison:**
1. Reshape correlation data from wide to long format
2. Create columns: dimension, CTT_type (Full/Purified), r_value
3. Expected: 6 rows (3 dimensions x 2 CTT types)

**Plot 2 - AIC Comparison:**
1. Reshape AIC data from wide to long format
2. Create columns: dimension, CTT_type (Full/Purified), AIC
3. Expected: 6 rows (3 dimensions x 2 CTT types)

**Output:**

**File 1:** data/step08_correlation_comparison_data.csv
**Format:** CSV with columns:
  - dimension (string): Congruence level (Common, Congruent, Incongruent)
  - CTT_type (string): Full or Purified
  - r_value (float): Pearson r with IRT theta
**Expected Rows:** 6 (3 dimensions x 2 CTT types)
**Purpose:** Plot source CSV for grouped bar chart comparing r_full vs r_purified

**File 2:** data/step08_aic_comparison_data.csv
**Format:** CSV with columns:
  - dimension (string): Congruence level
  - CTT_type (string): Full or Purified
  - AIC (float): Model AIC
**Expected Rows:** 6 (3 dimensions x 2 CTT types)
**Purpose:** Plot source CSV for grouped bar chart comparing AIC_Full vs AIC_Purified

**Validation Requirement:**
Validation tools MUST be used after plot data preparation execution. Specific validation tools determined by rq_tools based on plot data completeness and format validation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_correlation_comparison_data.csv: 6 rows x 3 columns (dimension: object, CTT_type: object, r_value: float64)
- data/step08_aic_comparison_data.csv: 6 rows x 3 columns (dimension: object, CTT_type: object, AIC: float64)

*Value Ranges:*
- r_value in [0.60, 0.92] (correlations from Step 5)
- AIC > 0 (log-likelihood based, positive)
- CTT_type in {"Full", "Purified"}
- dimension in {"Common", "Congruent", "Incongruent"}

*Data Quality:*
- Exactly 6 rows per file
- No NaN values
- All 3 dimensions represented for both CTT types (complete factorial design)
- No duplicate dimension x CTT_type combinations

*Log Validation:*
- Required pattern: "Plot data preparation complete: 2 files created"
- Required pattern: "Correlation comparison: 6 rows (3 dimensions x 2 CTT types)"
- Required pattern: "AIC comparison: 6 rows (3 dimensions x 2 CTT types)"
- Forbidden patterns: "ERROR", "Missing dimension", "Duplicate rows"

**Expected Behavior on Validation Failure:**
- If N != 6 for either file: Quit with error (incomplete data)
- If any dimension missing: Quit with error (data loss)
- If duplicate rows detected: Quit with error (data aggregation error)
- If validation fails: g_debug invoked

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs - intermediate and final)
- data/step00_dependency_check.txt (from Step 0: dependency verification report)
- data/step00_full_item_list.csv (from Step 0: item mapping with retention flags)
- data/step01_item_mapping.csv (from Step 1: retention rates by congruence)
- data/step02_ctt_full_scores.csv (from Step 2: Full CTT scores, 400 rows x 3 congruence columns)
- data/step03_ctt_purified_scores.csv (from Step 3: Purified CTT scores, 400 rows x 3 congruence columns)
- data/step04_reliability_assessment.csv (from Step 4: Cronbach's alpha for Full and Purified)
- data/step05_correlation_analysis.csv (from Step 5: Steiger's z-test results with dual p-values)
- data/step06_standardized_scores.csv (from Step 6: z-standardized IRT, Full CTT, Purified CTT)
- data/step07_lmm_model_comparison.csv (from Step 7: AIC comparison for 3 score types x 3 congruence)
- data/step07_lmm_summaries_theta.txt (from Step 7: IRT theta LMM summaries)
- data/step07_lmm_summaries_full.txt (from Step 7: Full CTT LMM summaries)
- data/step07_lmm_summaries_purified.txt (from Step 7: Purified CTT LMM summaries)
- data/step08_correlation_comparison_data.csv (from Step 8: plot source CSV for correlation comparison)
- data/step08_aic_comparison_data.csv (from Step 8: plot source CSV for AIC comparison)

### Logs (ONLY execution logs - .log files capturing stdout/stderr)
- logs/step00_verify_dependencies.log
- logs/step01_map_items.log
- logs/step02_compute_ctt_full.log
- logs/step03_compute_ctt_purified.log
- logs/step04_reliability_assessment.log
- logs/step05_correlation_analysis.log
- logs/step06_standardize_scores.log
- logs/step07_fit_lmms.log
- logs/step08_prepare_plot_data.log

### Plots (EMPTY until rq_plots runs)
- plots/correlation_comparison.png (created by rq_plots, NOT analysis steps)
- plots/aic_comparison.png (created by rq_plots)

### Results (EMPTY until rq_results runs)
- results/summary.md (created by rq_results, NOT analysis steps)

---

## Expected Data Formats

### CTT Score Format (Steps 2-3)

**Wide Format:**
- One row per composite_ID (participant x test combination)
- One column per congruence level
- Values: proportion correct in [0, 1]

**Example:**
```
composite_ID, ctt_full_common, ctt_full_congruent, ctt_full_incongruent
P001_T1,     0.65,            0.58,                0.52
P001_T2,     0.70,            0.62,                0.55
```

### Z-Standardized Format (Step 6)

**Wide Format:**
- One row per composite_ID
- 9 z-score columns (3 IRT + 3 Full + 3 Purified)
- TSVR_hours column (not standardized)
- All z-scores: mean ~ 0, SD ~ 1

**Example:**
```
composite_ID, z_theta_common, z_ctt_full_common, z_ctt_purified_common, TSVR_hours
P001_T1,     -0.32,          -0.28,             -0.25,                  0.0
P001_T2,     -0.18,          -0.15,             -0.12,                  24.5
```

### LMM Comparison Format (Step 7)

**Wide Format:**
- One row per congruence level
- AIC columns for 3 score types
- delta_AIC column showing improvement
- improvement flag ("Yes" if |delta_AIC| > 2)

**Example:**
```
dimension,   AIC_IRT, AIC_Full, AIC_Purified, delta_AIC_Full_Purified, improvement
Common,      1250.3,  1252.8,   1249.5,       -3.3,                    Yes
Congruent,   1275.2,  1278.1,   1276.8,       -1.3,                    No
Incongruent, 1290.5,  1293.2,   1289.8,       -3.4,                    Yes
```

### Plot Data Format (Step 8)

**Long Format (for grouped bar charts):**
- One row per dimension x CTT_type combination
- Separate files for correlation and AIC comparisons

**Correlation Comparison Example:**
```
dimension,   CTT_type, r_value
Common,      Full,     0.78
Common,      Purified, 0.80
Congruent,   Full,     0.75
Congruent,   Purified, 0.77
```

**AIC Comparison Example:**
```
dimension,   CTT_type, AIC
Common,      Full,     1252.8
Common,      Purified, 1249.5
Congruent,   Full,     1278.1
Congruent,   Purified, 1276.8
```

---

## Cross-RQ Dependencies

### Dependency Type: DERIVED Data from RQ 5.4.1

**This RQ requires outputs from:**
- **RQ 5.4.1** (Schema-Specific Trajectories - provides IRT purification results)
  - File 1: results/ch5/5.4.1/data/step02_purified_items.csv (retained items after Decision D039)
  - File 2: results/ch5/5.4.1/data/step03_theta_scores.csv (IRT ability estimates per congruence)
  - File 3: results/ch5/5.4.1/data/step00_tsvr_mapping.csv (TSVR time variable)
  - Used in: Steps 0-8 (all analysis steps depend on these outputs)
  - Rationale: RQ 5.4.1 performs IRT calibration with 2-pass purification. This RQ uses those purification decisions to test whether CTT scores computed from purified items converge better with IRT theta than full-item CTT scores.

**Execution Order Constraint:**
1. RQ 5.4.1 must complete fully (rq_results.status = "success")
2. This RQ executes after RQ 5.4.1 completes

**Data Source Boundaries:**
- **RAW data:** dfData.csv binary responses extracted directly (no RQ dependencies) for CTT score computation
- **DERIVED data:** RQ 5.4.1 outputs (purified_items.csv, theta_scores.csv, tsvr_mapping.csv)
- **Scope:** This RQ does NOT perform IRT calibration or item purification (reuses RQ 5.4.1 decisions)

**Validation:**
- Step 0: Check results/ch5/5.4.1/status.yaml shows rq_results.status = "success"
- Step 0: Check all 3 dependency files exist with expected row counts
- If RQ 5.4.1 incomplete: Quit with EXPECTATIONS ERROR ("RQ 5.4.1 must complete before RQ 5.4.5")
- If any dependency file missing: Quit with EXPECTATIONS ERROR specifying which file

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

**Per-Step Validation Summary:**

| Step | Analysis | Validation Criteria |
|------|----------|---------------------|
| 0 | Dependency verification | File existence, RQ 5.4.1 status = success, expected row counts |
| 1 | Item mapping | Retention rates 60-90%, accounting identity (N_total = N_retained + N_removed) |
| 2 | Full CTT computation | CTT scores in [0,1], no NaN, N=400, distribution normal |
| 3 | Purified CTT computation | CTT scores in [0,1], no NaN, N=400, distribution normal |
| 4 | Reliability assessment | Alpha in [0,1], CIs valid, delta_alpha plausible |
| 5 | Correlation analysis | r in [-1,1], dual p-values present (D068), normality check passed |
| 6 | Z-standardization | mean ~ 0 (tolerance 0.01), SD ~ 1 (tolerance 0.01) for all 9 columns |
| 7 | LMM fitting | All 9 models converge, AIC > 0, assumptions met |
| 8 | Plot data preparation | N=6 rows per file, complete factorial design, no NaN |

---

## Summary

**Total Steps:** 9 (Step 0: dependency verification + Steps 1-8: analysis)

**Estimated Runtime:** 20-30 minutes
- Steps 0-6: Low complexity (~10 minutes total)
- Step 7: Medium complexity (~10-15 minutes for 9 LMM fits)
- Step 8: Low complexity (~2 minutes)

**Cross-RQ Dependencies:** RQ 5.4.1 (must complete before this RQ executes)

**Primary Outputs:**
- CTT scores: Full (all items) and Purified (retained items only) per congruence level
- Reliability assessment: Cronbach's alpha with bootstrap CIs for Full and Purified
- Correlation analysis: Steiger's z-test comparing r_full vs r_purified with dual p-values (Decision D068)
- Z-standardized scores: 9 columns (3 IRT + 3 Full + 3 Purified) for LMM comparability
- LMM comparison: AIC comparison for IRT, Full CTT, Purified CTT models
- Plot source CSVs: Correlation comparison and AIC comparison for visualization

**Validation Coverage:** 100% (all 9 steps have validation requirements)

**Key Hypotheses Tested:**
1. Purified CTT correlates more strongly with IRT theta than Full CTT (delta_r ~ +0.02)
2. Purified CTT yields better LMM fit (lower AIC) than Full CTT
3. Effect consistent across all three congruence levels (Common, Congruent, Incongruent)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-02): Initial plan created by rq_planner agent for RQ 5.4.5
