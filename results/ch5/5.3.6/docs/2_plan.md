# Analysis Plan: RQ 5.3.6 - Purified CTT Effects (Paradigms)

**Research Question:** 5.3.6
**Created:** 2025-12-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ tests measurement robustness by comparing two CTT scoring approaches: Full CTT (all items pre-purification) vs Purified CTT (only IRT-retained items per Decision D039). Examines paradigm-specific forgetting trajectories (Free Recall, Cued Recall, Recognition) across N=100 participants x 4 test sessions = 400 observations.

**Pipeline:** CTT scoring comparison + Correlation analysis (Steiger's z-test) + LMM (parallel models) + AIC comparison

**Steps:** 9 total analysis steps (Step 0: dependency validation + Steps 1-8: analysis)

**Estimated Runtime:** Medium (30-90 minutes total - dominated by LMM fitting and bootstrap iterations)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (Steiger's z-test with uncorrected + Bonferroni)
- Decision D070: TSVR as time variable (LMMs use TSVR_hours from RQ 5.3.1)

**Cross-RQ Dependencies:**
- RQ 5.3.1 must complete Steps 0-3 before this RQ can execute
- Uses: purified items list, IRT theta scores, TSVR mapping

**Theoretical Prediction:**
Item purification removes psychometrically problematic items (low discrimination a < 0.4, extreme difficulty |b| > 3.0), reducing measurement noise. Purified CTT should show:
1. Higher correlation with IRT theta vs Full CTT (convergent validity)
2. Higher internal consistency (Cronbach's alpha) despite fewer items
3. Better LMM fit (lower AIC) due to reduced measurement error
4. Replication of paradigm-specific forgetting pattern (IFR > ICR > IRE forgetting rates)

---

## Analysis Plan

### Step 0: Load Dependencies and Validate

**Dependencies:** None (first step)
**Complexity:** Low (<5 minutes - file validation only)

**Purpose:** Verify RQ 5.3.1 completion and load required outputs for CTT comparison.

**Input:**

**File 1:** results/ch5/5.3.1/status.yaml
**Purpose:** Verify RQ 5.3.1 completion
**Required Status:** rq_results.status = "success" (ensures all steps completed)

**File 2:** results/ch5/5.3.1/data/step02_purified_items.csv
**Source:** RQ 5.3.1 Step 2 (item purification)
**Format:** CSV with columns:
  - `item_name` (string, e.g., "VR-IFR-A01-N-ANS")
  - `dimension` (string, paradigm: "IFR", "ICR", "IRE")
  - `retained` (boolean, TRUE = item retained after purification)
  - `a` (float, discrimination parameter)
  - `b` (float, difficulty parameter)
**Expected Rows:** Variable (depends on RQ 5.3.1 purification outcome, typically 40-80 items total)

**File 3:** results/ch5/5.3.1/data/step03_theta_scores.csv
**Source:** RQ 5.3.1 Step 3 (IRT Pass 2 theta extraction)
**Format:** CSV with columns:
  - `composite_ID` (string, format: UID_test, e.g., "P001_T1")
  - `theta_IFR` (float, IRT ability for Free Recall paradigm)
  - `theta_ICR` (float, IRT ability for Cued Recall paradigm)
  - `theta_IRE` (float, IRT ability for Recognition paradigm)
  - `se_IFR` (float, standard error for IFR theta)
  - `se_ICR` (float, standard error for ICR theta)
  - `se_IRE` (float, standard error for IRE theta)
**Expected Rows:** 400 (100 participants x 4 tests)

**File 4:** results/ch5/5.3.1/data/step00_tsvr_mapping.csv
**Source:** RQ 5.3.1 Step 0 (TSVR extraction)
**Format:** CSV with columns:
  - `composite_ID` (string, matches theta_scores)
  - `TSVR_hours` (float, time since VR session in hours)
  - `test` (string, test session: T1, T2, T3, T4)
**Expected Rows:** 400

**Processing:**
1. Check results/ch5/5.3.1/status.yaml exists and rq_results.status = "success"
2. Load purified_items.csv and validate schema (5 required columns present)
3. Load theta_scores.csv and validate schema (7 required columns present)
4. Load tsvr_mapping.csv and validate schema (3 required columns present)
5. Check row counts match expectations (400 for theta and TSVR, variable for items)
6. Validate no missing values in critical columns (composite_ID, theta_*, TSVR_hours)

**Output:**

**File 1:** data/step00_dependency_validation_report.txt
**Format:** Plain text report
**Content:**
  - RQ 5.3.1 status check result
  - File existence confirmations
  - Schema validation results
  - Row count summaries
  - Missing data summary
**Purpose:** Audit trail confirming dependencies met

**Validation Requirement:**
Validation tools MUST be used after dependency loading. Specific validation tools determined by rq_tools based on file format and schema requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation_report.txt exists
- File size > 500 bytes (non-trivial report)

*Value Ranges:*
- N/A (validation step - no numeric outputs requiring range checks)

*Data Quality:*
- Report must contain "PASS" status for all 4 dependency checks
- No "ERROR" or "MISSING" flags in report

*Log Validation:*
- Required pattern: "Dependency validation: PASS"
- Required pattern: "All 4 required files loaded successfully"
- Forbidden patterns: "ERROR", "File not found", "Schema mismatch"

**Expected Behavior on Validation Failure:**
- If RQ 5.3.1 status != success: Quit with "RQ 5.3.1 incomplete - run RQ 5.3.1 before RQ 5.3.6"
- If any file missing: Quit with "Missing dependency file: [filename]"
- If schema mismatch: Quit with "Schema validation failed for [filename]: expected columns [list], found [list]"
- Log error to logs/step00_load_dependencies.log
- g_debug NOT invoked (user action required: complete RQ 5.3.1)

---

### Step 1: Map Items by Paradigm (Retained vs Removed)

**Dependencies:** Step 0 (requires purified_items.csv)
**Complexity:** Low (<5 minutes - table manipulation only)

**Purpose:** Create item mapping table stratified by paradigm showing which items retained after RQ 5.3.1 purification and compute retention rates per paradigm.

**Input:**

**File:** data/step00_purified_items.csv (loaded in Step 0, copied to this RQ's data/ folder)
**Source:** RQ 5.3.1 Step 2
**Columns:** item_name, dimension, retained, a, b

**Processing:**
1. Group items by dimension (paradigm: IFR, ICR, IRE)
2. Count total items per paradigm
3. Count retained items per paradigm (retained = TRUE)
4. Compute retention rate = retained / total per paradigm
5. Create summary table with paradigm-level statistics

**Output:**

**File 1:** data/step01_item_mapping.csv
**Format:** CSV, one row per item
**Columns:**
  - `item_name` (string, item identifier)
  - `paradigm` (string, IFR/ICR/IRE)
  - `retained` (boolean, TRUE/FALSE)
  - `a` (float, discrimination parameter from RQ 5.3.1)
  - `b` (float, difficulty parameter from RQ 5.3.1)
  - `exclusion_reason` (string, "low_discrimination" if a < 0.4, "extreme_difficulty" if |b| > 3.0, "retained" if kept, "both" if both violations)
**Expected Rows:** Variable (total items from RQ 5.3.1, typically 40-80)

**File 2:** data/step01_retention_summary.csv
**Format:** CSV, one row per paradigm
**Columns:**
  - `paradigm` (string, IFR/ICR/IRE)
  - `total_items` (int, original item count)
  - `retained_items` (int, items passing purification)
  - `removed_items` (int, items excluded)
  - `retention_rate` (float, retained / total, range [0,1])
**Expected Rows:** 3 (one per paradigm)

**Validation Requirement:**
Validation tools MUST be used after item mapping tool execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_item_mapping.csv: Variable rows (40-80 expected), 6 columns, types: item_name (object), paradigm (object), retained (bool), a (float64), b (float64), exclusion_reason (object)
- data/step01_retention_summary.csv: 3 rows, 5 columns, types: paradigm (object), total_items (int64), retained_items (int64), removed_items (int64), retention_rate (float64)

*Value Ranges:*
- retention_rate in [0, 1] (proportion, must be valid percentage)
- retained_items <= total_items (logical constraint)
- removed_items = total_items - retained_items (arithmetic consistency)
- a >= 0 (discrimination must be positive or zero)
- b unrestricted (difficulty can be any value)

*Data Quality:*
- All 3 paradigms present in retention_summary (IFR, ICR, IRE)
- No NaN values in retention_rate column
- Sum of retained + removed = total for each paradigm
- item_mapping has retained = TRUE/FALSE for all items (no NaN)

*Log Validation:*
- Required pattern: "Item mapping complete: [N] items processed"
- Required pattern: "Retention summary: IFR [X]%, ICR [Y]%, IRE [Z]%"
- Forbidden patterns: "ERROR", "Missing paradigm", "NaN retention rate"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Missing paradigm: IFR not found in retention summary")
- Log failure to logs/step01_map_items.log
- Quit script immediately
- g_debug invoked to diagnose (likely RQ 5.3.1 output schema mismatch)

---

### Step 2: Compute Full CTT Scores (All Items Pre-Purification)

**Dependencies:** Step 1 (requires item_mapping.csv to identify original item pool)
**Complexity:** Low (<10 minutes - data extraction and mean computation)

**Purpose:** Extract raw response data from dfData.csv for ALL paradigm items (pre-purification) and compute CTT scores as mean proportion correct per UID x Test x Paradigm.

**Input:**

**File 1:** data/cache/dfData.csv (project-level raw data source)
**Sheet/Format:** Single CSV with participant-level data
**Required Columns:**
  - `UID` (string, participant identifier)
  - `test` (string, test session: T1, T2, T3, T4)
  - TQ_* columns matching paradigm items from RQ 5.3.1 Step 0 (dichotomized responses: 0 = incorrect, 1 = correct)

**File 2:** data/step01_item_mapping.csv (to identify full item pool)
**Purpose:** Extract item_name list (all items, not just retained) to determine which TQ_* columns to include in Full CTT

**Processing:**
1. Load item_mapping.csv and extract all item_name values (retained = TRUE OR FALSE - include all)
2. Map item_name to TQ_* column names in dfData.csv
3. Extract raw response data for all items, stratified by paradigm
4. Compute mean score per UID x Test x Paradigm using all items:
   - CTT_full_IFR = mean(IFR items) per UID x Test
   - CTT_full_ICR = mean(ICR items) per UID x Test
   - CTT_full_IRE = mean(IRE items) per UID x Test
5. Merge scores into single DataFrame (UID, test, CTT_full_IFR, CTT_full_ICR, CTT_full_IRE)

**Output:**

**File:** data/step02_ctt_full_scores.csv
**Format:** CSV, one row per UID x test combination
**Columns:**
  - `UID` (string, participant identifier)
  - `test` (string, T1/T2/T3/T4)
  - `CTT_full_IFR` (float, mean proportion correct for IFR items, range [0,1])
  - `CTT_full_ICR` (float, mean proportion correct for ICR items, range [0,1])
  - `CTT_full_IRE` (float, mean proportion correct for IRE items, range [0,1])
**Expected Rows:** 400 (100 participants x 4 tests)
**Expected Values:** All CTT scores in [0, 1] (proportion correct)

**Validation Requirement:**
Validation tools MUST be used after Full CTT computation. Specific validation tools determined by rq_tools based on CTT scoring requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_ctt_full_scores.csv: 400 rows, 5 columns, types: UID (object), test (object), CTT_full_IFR (float64), CTT_full_ICR (float64), CTT_full_IRE (float64)

*Value Ranges:*
- CTT_full_IFR in [0, 1] (proportion correct)
- CTT_full_ICR in [0, 1]
- CTT_full_IRE in [0, 1]
- No negative values or values > 1.0 (impossible for proportions)

*Data Quality:*
- All 400 rows present (100 participants x 4 tests, no missing)
- No NaN values in CTT score columns (all participants have valid scores)
- No duplicate UID x test combinations (composite_ID must be unique)
- test column contains only {T1, T2, T3, T4} (no invalid test sessions)

*Log Validation:*
- Required pattern: "Full CTT scores computed: 400 observations"
- Required pattern: "IFR items: [N], ICR items: [M], IRE items: [K]"
- Forbidden patterns: "ERROR", "NaN values detected", "Invalid test session"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "CTT score out of range: CTT_full_IFR = 1.23 for UID P050_T2")
- Log failure to logs/step02_compute_full_ctt.log
- Quit script immediately
- g_debug invoked to diagnose (likely data extraction or mean computation error)

---

### Step 3: Compute Purified CTT Scores (Retained Items Only)

**Dependencies:** Steps 1, 2 (requires item_mapping.csv to identify retained items, uses same dfData.csv as Step 2)
**Complexity:** Low (<10 minutes - data extraction and mean computation)

**Purpose:** Extract raw response data from dfData.csv for ONLY IRT-retained items (retained = TRUE from RQ 5.3.1) and compute CTT scores as mean proportion correct per UID x Test x Paradigm.

**Input:**

**File 1:** data/cache/dfData.csv (same as Step 2)
**Required Columns:** Same as Step 2

**File 2:** data/step01_item_mapping.csv
**Purpose:** Extract item_name list WHERE retained = TRUE (purified item subset)

**Processing:**
1. Load item_mapping.csv and filter to retained = TRUE items only
2. Map retained item_name to TQ_* column names in dfData.csv
3. Extract raw response data for retained items only, stratified by paradigm
4. Compute mean score per UID x Test x Paradigm using purified items:
   - CTT_purified_IFR = mean(retained IFR items) per UID x Test
   - CTT_purified_ICR = mean(retained ICR items) per UID x Test
   - CTT_purified_IRE = mean(retained IRE items) per UID x Test
5. Merge scores into single DataFrame (UID, test, CTT_purified_IFR, CTT_purified_ICR, CTT_purified_IRE)

**Output:**

**File:** data/step03_ctt_purified_scores.csv
**Format:** CSV, one row per UID x test combination
**Columns:**
  - `UID` (string, participant identifier)
  - `test` (string, T1/T2/T3/T4)
  - `CTT_purified_IFR` (float, mean proportion correct for retained IFR items, range [0,1])
  - `CTT_purified_ICR` (float, mean proportion correct for retained ICR items, range [0,1])
  - `CTT_purified_IRE` (float, mean proportion correct for retained IRE items, range [0,1])
**Expected Rows:** 400 (100 participants x 4 tests)
**Expected Values:** All CTT scores in [0, 1] (proportion correct)

**Validation Requirement:**
Validation tools MUST be used after Purified CTT computation. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_ctt_purified_scores.csv: 400 rows, 5 columns, types: UID (object), test (object), CTT_purified_IFR (float64), CTT_purified_ICR (float64), CTT_purified_IRE (float64)

*Value Ranges:*
- CTT_purified_IFR in [0, 1]
- CTT_purified_ICR in [0, 1]
- CTT_purified_IRE in [0, 1]

*Data Quality:*
- All 400 rows present (no missing observations)
- No NaN values in CTT score columns
- No duplicate UID x test combinations
- test column contains only {T1, T2, T3, T4}

*Log Validation:*
- Required pattern: "Purified CTT scores computed: 400 observations"
- Required pattern: "Retained items - IFR: [N], ICR: [M], IRE: [K]"
- Forbidden patterns: "ERROR", "NaN values detected", "No retained items for paradigm"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "No retained items for paradigm IFR - cannot compute purified CTT")
- Log failure to logs/step03_compute_purified_ctt.log
- Quit script immediately
- g_debug invoked to diagnose

---

### Step 4: Reliability Assessment with Cronbach's Alpha

**Dependencies:** Steps 2, 3 (requires Full and Purified CTT scores)
**Complexity:** Medium (15-30 minutes - bootstrap iterations for confidence intervals)

**Purpose:** Compute Cronbach's alpha internal consistency for Full CTT and Purified CTT per paradigm with bootstrap 95% confidence intervals (10,000 iterations per 1_concept.md).

**Input:**

**File 1:** data/cache/dfData.csv
**Purpose:** Need raw item-level responses (not mean scores) to compute inter-item covariances for Cronbach's alpha

**File 2:** data/step01_item_mapping.csv
**Purpose:** Identify which items belong to Full vs Purified sets per paradigm

**Processing:**
1. For each paradigm (IFR, ICR, IRE):
   - Extract raw item-level responses for Full item set
   - Compute Cronbach's alpha_full using all items
   - Bootstrap alpha_full (10,000 iterations, sample participants with replacement, recompute alpha)
   - Compute 95% CI from bootstrap distribution (2.5th and 97.5th percentiles)
   - Extract raw item-level responses for Purified item set (retained = TRUE)
   - Compute Cronbach's alpha_purified using retained items only
   - Bootstrap alpha_purified (10,000 iterations)
   - Compute 95% CI from bootstrap distribution
2. Compare alpha_purified vs alpha_full per paradigm
3. Compute Spearman-Brown adjusted alpha_purified (extrapolate to Full item count for fair comparison)

**Output:**

**File:** data/step04_reliability_assessment.csv
**Format:** CSV, one row per paradigm
**Columns:**
  - `paradigm` (string, IFR/ICR/IRE)
  - `n_items_full` (int, total items in Full set)
  - `n_items_purified` (int, total items in Purified set)
  - `alpha_full` (float, Cronbach's alpha for Full CTT, range [0,1])
  - `alpha_full_CI_lower` (float, lower bound of 95% bootstrap CI)
  - `alpha_full_CI_upper` (float, upper bound of 95% bootstrap CI)
  - `alpha_purified` (float, Cronbach's alpha for Purified CTT, range [0,1])
  - `alpha_purified_CI_lower` (float, lower bound of 95% bootstrap CI)
  - `alpha_purified_CI_upper` (float, upper bound of 95% bootstrap CI)
  - `alpha_purified_SB_adjusted` (float, Spearman-Brown prophecy adjusted to Full item count, range [0,1])
  - `delta_alpha` (float, alpha_purified - alpha_full, range [-1,1])
**Expected Rows:** 3 (one per paradigm)

**Validation Requirement:**
Validation tools MUST be used after reliability assessment tool execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_reliability_assessment.csv: 3 rows, 11 columns, types: paradigm (object), n_items_* (int64), alpha_* (float64)

*Value Ranges:*
- alpha_full in [0, 1] (Cronbach's alpha is correlation-based)
- alpha_purified in [0, 1]
- alpha_purified_SB_adjusted in [0, 1]
- CI_lower <= alpha <= CI_upper for both Full and Purified (logical constraint)
- n_items_purified <= n_items_full (purification removes items)

*Data Quality:*
- All 3 paradigms present (IFR, ICR, IRE)
- No NaN values in alpha or CI columns
- CI_lower < CI_upper for all paradigms (bootstrap CIs must be valid intervals)
- n_items_full > 0 and n_items_purified > 0 (must have items to compute alpha)

*Log Validation:*
- Required pattern: "Reliability assessment complete: 3 paradigms"
- Required pattern: "Bootstrap iterations: 10000 per paradigm"
- Forbidden patterns: "ERROR", "NaN alpha detected", "Bootstrap failed"
- Acceptable warnings: "Low alpha (<0.70) detected for [paradigm]" (low reliability is informative, not error)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Alpha out of range: alpha_full = -0.15 for IFR")
- Log failure to logs/step04_reliability_assessment.log
- Quit script immediately
- g_debug invoked to diagnose (likely item covariance computation issue)

---

### Step 5: Correlation Analysis with Steiger's Z-Test

**Dependencies:** Steps 2, 3 (requires Full and Purified CTT scores), Step 0 (requires IRT theta scores)
**Complexity:** Low (<10 minutes - correlation computation and Steiger's test)

**Purpose:** Correlate Full CTT and Purified CTT with IRT theta per paradigm, then test whether correlations differ using Steiger's z-test for dependent correlations (sharing IRT theta variable). Report dual p-values per Decision D068.

**Input:**

**File 1:** data/step02_ctt_full_scores.csv (Full CTT scores)
**File 2:** data/step03_ctt_purified_scores.csv (Purified CTT scores)
**File 3:** data/step00_theta_scores.csv (IRT theta from RQ 5.3.1, loaded in Step 0)
**Required Columns:** composite_ID, theta_IFR, theta_ICR, theta_IRE

**Processing:**
1. Merge Full CTT, Purified CTT, and IRT theta on UID + test (create composite_ID = UID_test for matching)
2. For each paradigm (IFR, ICR, IRE):
   - Compute r_full = Pearson correlation between CTT_full_[paradigm] and theta_[paradigm]
   - Compute r_purified = Pearson correlation between CTT_purified_[paradigm] and theta_[paradigm]
   - Compute Steiger's z-test for dependent correlations:
     * H0: r_full = r_purified
     * H1: r_purified > r_full (directional hypothesis per 1_concept.md)
   - Extract z-statistic, p_uncorrected
   - Apply Bonferroni correction for 3 paradigms: p_bonferroni = p_uncorrected x 3 (Decision D068)
   - Compute delta_r = r_purified - r_full (effect size of purification)
3. Validate assumptions per 1_concept.md:
   - Check bivariate normality (scatter plots, Mardia's test)
   - Check linearity (lowess smoother on scatter plots)
   - If violations detected, report bootstrap CI for delta_r as sensitivity analysis

**Output:**

**File 1:** data/step05_correlation_analysis.csv
**Format:** CSV, one row per paradigm
**Columns:**
  - `paradigm` (string, IFR/ICR/IRE)
  - `r_full` (float, correlation between Full CTT and IRT theta, range [-1,1])
  - `r_purified` (float, correlation between Purified CTT and IRT theta, range [-1,1])
  - `delta_r` (float, r_purified - r_full, range [-2,2] theoretically, expected [-0.1, 0.1])
  - `steiger_z` (float, z-statistic from Steiger's test)
  - `p_uncorrected` (float, uncorrected p-value, range [0,1])
  - `p_bonferroni` (float, Bonferroni-corrected p-value = p_uncorrected x 3, range [0,1], capped at 1.0)
  - `normality_test_p` (float, Mardia's test p-value for bivariate normality assumption)
  - `linearity_flag` (string, "linear" or "nonlinear" based on lowess inspection)
**Expected Rows:** 3 (one per paradigm)

**File 2:** data/step05_steiger_assumptions_report.txt
**Format:** Plain text report
**Content:**
  - Scatter plot inspection results (saved as PNG for manual review)
  - Mardia's test results per paradigm
  - Linearity assessment per paradigm
  - Bootstrap sensitivity analysis results (if assumptions violated)

**Validation Requirement:**
Validation tools MUST be used after correlation analysis tool execution. Specific validation tools determined by rq_tools. Decision D068 validation (dual p-values) MANDATORY.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_correlation_analysis.csv: 3 rows, 9 columns, types: paradigm (object), r_* (float64), delta_r (float64), steiger_z (float64), p_* (float64), normality_test_p (float64), linearity_flag (object)
- data/step05_steiger_assumptions_report.txt: exists, size > 1000 bytes

*Value Ranges:*
- r_full in [-1, 1] (correlation bounds)
- r_purified in [-1, 1]
- delta_r in [-2, 2] (difference of correlations)
- steiger_z unrestricted (z-statistic can be any real number)
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1] (capped at 1.0 even if p_uncorrected x 3 > 1)
- normality_test_p in [0, 1]

*Data Quality:*
- All 3 paradigms present
- No NaN values in r_full, r_purified, delta_r, steiger_z
- BOTH p_uncorrected AND p_bonferroni present for all paradigms (Decision D068 requirement)
- linearity_flag contains only {"linear", "nonlinear"} (no other values)

*Log Validation:*
- Required pattern: "Correlation analysis complete: 3 paradigms"
- Required pattern: "Decision D068: Dual p-values reported (uncorrected + Bonferroni)"
- Required pattern: "Steiger's z-test: r_purified vs r_full for [paradigm]"
- Forbidden patterns: "ERROR", "NaN correlation", "Missing p-value"
- Acceptable warnings: "Normality assumption violated for [paradigm] - bootstrap sensitivity analysis recommended"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Missing p_bonferroni column - Decision D068 requires dual p-values")
- Log failure to logs/step05_correlation_analysis.log
- Quit script immediately
- g_debug invoked to diagnose

---

### Step 6: Z-Standardize Measurements

**Dependencies:** Steps 2, 3 (requires Full and Purified CTT scores), Step 0 (requires IRT theta)
**Complexity:** Low (<5 minutes - simple transformation)

**Purpose:** Grand-mean center and scale all measurements (IRT theta, Full CTT, Purified CTT) to z-scores for comparable LMM coefficients across measurement types.

**Input:**

**File 1:** data/step02_ctt_full_scores.csv
**File 2:** data/step03_ctt_purified_scores.csv
**File 3:** data/step00_theta_scores.csv (loaded in Step 0)

**Processing:**
1. Merge theta, Full CTT, and Purified CTT on composite_ID (UID_test)
2. For each paradigm (IFR, ICR, IRE):
   - Compute grand mean and SD for theta_[paradigm] across all 400 observations
   - Z-standardize: z_theta_[paradigm] = (theta_[paradigm] - mean) / SD
   - Compute grand mean and SD for CTT_full_[paradigm]
   - Z-standardize: z_CTT_full_[paradigm] = (CTT_full_[paradigm] - mean) / SD
   - Compute grand mean and SD for CTT_purified_[paradigm]
   - Z-standardize: z_CTT_purified_[paradigm] = (CTT_purified_[paradigm] - mean) / SD
3. Validate standardization: mean(z_*) ~ 0, SD(z_*) ~ 1 (tolerance ±0.01 per validation tools)

**Output:**

**File:** data/step06_standardized_scores.csv
**Format:** CSV, one row per UID x test combination
**Columns:**
  - `composite_ID` (string, UID_test format)
  - `UID` (string, participant identifier)
  - `test` (string, T1/T2/T3/T4)
  - `TSVR_hours` (float, time variable from Step 0)
  - `z_theta_IFR` (float, standardized IRT theta, mean ~ 0, SD ~ 1)
  - `z_theta_ICR` (float)
  - `z_theta_IRE` (float)
  - `z_CTT_full_IFR` (float, standardized Full CTT, mean ~ 0, SD ~ 1)
  - `z_CTT_full_ICR` (float)
  - `z_CTT_full_IRE` (float)
  - `z_CTT_purified_IFR` (float, standardized Purified CTT, mean ~ 0, SD ~ 1)
  - `z_CTT_purified_ICR` (float)
  - `z_CTT_purified_IRE` (float)
**Expected Rows:** 400 (100 participants x 4 tests)

**Validation Requirement:**
Validation tools MUST be used after standardization tool execution. Specific validation tools determined by rq_tools (validate_standardization function from tools_catalog.md).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_standardized_scores.csv: 400 rows, 13 columns, types: composite_ID (object), UID (object), test (object), TSVR_hours (float64), z_* (float64)

*Value Ranges:*
- z_* values typically in [-3, 3] (z-scores rarely exceed ±3 SD)
- TSVR_hours in [0, 168] (0 = encoding, 168 = 1 week max per study design)

*Data Quality:*
- All 400 rows present (no missing observations)
- No NaN values in z_* columns
- Mean(z_*) in [-0.01, 0.01] for all 9 z-score columns (standardization validation)
- SD(z_*) in [0.99, 1.01] for all 9 z-score columns (standardization validation)

*Log Validation:*
- Required pattern: "Standardization complete: 9 z-score columns created"
- Required pattern: "Validation: mean(z_*) ~ 0, SD(z_*) ~ 1 for all columns"
- Forbidden patterns: "ERROR", "Standardization failed", "Mean deviation > 0.01"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Standardization failed for z_theta_IFR: mean = 0.15 (expected ~0)")
- Log failure to logs/step06_standardize_measurements.log
- Quit script immediately
- g_debug invoked to diagnose

---

### Step 7: Fit Parallel LMMs and Compare AIC

**Dependencies:** Step 6 (requires z-standardized scores)
**Complexity:** High (30-60 minutes - 9 LMMs total: 3 paradigms x 3 measurement types)

**Purpose:** Fit parallel Linear Mixed Models on z-standardized scores (IRT theta, Full CTT, Purified CTT) with identical formula to compare model fit via AIC per Burnham & Anderson. Tests whether Purified CTT yields better model fit than Full CTT.

**Input:**

**File:** data/step06_standardized_scores.csv
**Required Columns:** composite_ID, UID, test, TSVR_hours, z_theta_*, z_CTT_full_*, z_CTT_purified_*

**Processing:**
1. For each paradigm (IFR, ICR, IRE):
   - Prepare long-format LMM input with columns: UID, TSVR_hours, Score, measurement_type
   - Fit 3 LMMs with identical formula: Score ~ TSVR_hours + (TSVR_hours | UID), REML=False
     * Model 1: Score = z_theta_[paradigm] (IRT reference)
     * Model 2: Score = z_CTT_full_[paradigm] (Full CTT)
     * Model 3: Score = z_CTT_purified_[paradigm] (Purified CTT)
   - Extract AIC per model
   - Compute delta_AIC = AIC_full - AIC_purified (positive = purified better)
   - Compute delta_AIC_IRT = AIC_purified - AIC_IRT (IRT as reference)
   - Extract fixed effect coefficients (intercept, TSVR_hours slope) per model
   - Compute Cohen's kappa for coefficient agreement between Full and Purified models
2. Apply convergence contingency plan per 1_concept.md and Bates et al. (2015):
   - If random slopes fail to converge:
     * Try alternative optimizers (bobyqa, nlminb)
     * Use likelihood ratio test (LRT) to compare random slopes vs intercept-only
     * If LRT p < 0.05, retain slopes with simplified correlation structure
     * If LRT p >= 0.05, use random intercepts-only model
     * **CRITICAL:** Apply same simplification to ALL models for structural equivalence
   - Document which random effects structure achieved convergence per paradigm

**Output:**

**File 1:** data/step07_lmm_model_comparison.csv
**Format:** CSV, one row per paradigm
**Columns:**
  - `paradigm` (string, IFR/ICR/IRE)
  - `AIC_IRT` (float, AIC for IRT theta model)
  - `AIC_full` (float, AIC for Full CTT model)
  - `AIC_purified` (float, AIC for Purified CTT model)
  - `delta_AIC_full_purified` (float, AIC_full - AIC_purified, positive = purified better)
  - `delta_AIC_purified_IRT` (float, AIC_purified - AIC_IRT, negative = IRT better)
  - `coef_intercept_IRT` (float, fixed intercept from IRT model)
  - `coef_slope_IRT` (float, fixed TSVR_hours slope from IRT model)
  - `coef_intercept_full` (float, fixed intercept from Full CTT model)
  - `coef_slope_full` (float, fixed TSVR_hours slope from Full CTT model)
  - `coef_intercept_purified` (float, fixed intercept from Purified CTT model)
  - `coef_slope_purified` (float, fixed TSVR_hours slope from Purified CTT model)
  - `cohen_kappa` (float, coefficient agreement between Full and Purified, range [-1,1], >0.60 = substantial)
  - `convergence_flag_IRT` (boolean, TRUE = converged)
  - `convergence_flag_full` (boolean, TRUE = converged)
  - `convergence_flag_purified` (boolean, TRUE = converged)
  - `random_structure` (string, "full_slopes" or "intercept_only" or "simplified_slopes" - documents convergence outcome)
**Expected Rows:** 3 (one per paradigm)

**File 2:** data/step07_lmm_convergence_report.txt
**Format:** Plain text report
**Content:**
  - Convergence outcomes per model and paradigm
  - LRT results if random structure simplification required
  - Optimizer settings used per model
  - Warning messages from statsmodels (if any)

**Validation Requirement:**
Validation tools MUST be used after LMM fitting tool execution. Specific validation tools determined by rq_tools (validate_lmm_convergence, validate_variance_positivity, validate_effect_sizes).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_lmm_model_comparison.csv: 3 rows, 17 columns, types: paradigm (object), AIC_* (float64), delta_AIC_* (float64), coef_* (float64), cohen_kappa (float64), convergence_flag_* (bool), random_structure (object)
- data/step07_lmm_convergence_report.txt: exists, size > 500 bytes

*Value Ranges:*
- AIC_* > 0 (AIC is always positive for valid models)
- delta_AIC_* unrestricted (can be positive or negative depending on relative fit)
- coef_intercept_* typically in [-0.5, 0.5] (z-standardized outcome, intercept ~ 0 expected)
- coef_slope_* typically in [-0.1, 0.0] (negative = forgetting over time)
- cohen_kappa in [-1, 1] (agreement coefficient)

*Data Quality:*
- All 3 paradigms present
- No NaN values in AIC or coefficient columns
- All convergence_flag_* = TRUE (convergence required for valid AIC comparison)
- random_structure contains only {"full_slopes", "intercept_only", "simplified_slopes"}

*Log Validation:*
- Required pattern: "LMM comparison complete: 9 models fitted (3 paradigms x 3 measurement types)"
- Required pattern: "Convergence: All models converged successfully" OR "Convergence: Simplified random structure applied per Bates et al. 2015"
- Required pattern: "AIC comparison: delta_AIC_full_purified = [X] for [paradigm]"
- Forbidden patterns: "ERROR", "Model did not converge", "AIC = NaN"
- Acceptable warnings: "Simplified random structure (intercept-only) used for [paradigm] per LRT p >= 0.05"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Model convergence failed for IFR Purified CTT despite optimizer attempts")
- Log failure to logs/step07_fit_parallel_lmms.log
- Quit script immediately
- g_debug invoked to diagnose (likely data issue or model misspecification)

---

### Step 8: Prepare Comparison Plot Data

**Dependencies:** Steps 4, 5, 7 (requires reliability, correlation, and AIC results)
**Complexity:** Low (<5 minutes - data aggregation for plotting)

**Purpose:** Create plot source CSVs for correlation comparison and AIC comparison visualizations (consumed by rq_plots later).

**Input:**

**File 1:** data/step05_correlation_analysis.csv (correlation results)
**File 2:** data/step07_lmm_model_comparison.csv (AIC results)

**Processing:**

**Correlation Comparison Plot Data:**
1. Reshape correlation results to long format for grouped plotting
2. Create 6 rows: 3 paradigms x 2 CTT types (Full, Purified)
3. Columns: paradigm, ctt_type, r, CI_lower, CI_upper (CIs from bootstrap if available, else Fisher z-transformation)

**AIC Comparison Plot Data:**
1. Extract AIC columns from LMM comparison
2. Create 3 rows: 3 paradigms
3. Columns: paradigm, AIC_IRT, AIC_full, AIC_purified, delta_AIC_full_purified

**Output:**

**File 1:** data/step08_correlation_comparison_data.csv
**Format:** CSV, plot source data
**Columns:**
  - `paradigm` (string, IFR/ICR/IRE)
  - `ctt_type` (string, "Full" or "Purified")
  - `r` (float, correlation with IRT theta, range [-1,1])
  - `CI_lower` (float, lower 95% CI bound)
  - `CI_upper` (float, upper 95% CI bound)
**Expected Rows:** 6 (3 paradigms x 2 CTT types)

**File 2:** data/step08_aic_comparison_data.csv
**Format:** CSV, plot source data (duplicate of step07 for plotting convenience)
**Columns:**
  - `paradigm` (string, IFR/ICR/IRE)
  - `AIC_IRT` (float)
  - `AIC_full` (float)
  - `AIC_purified` (float)
  - `delta_AIC_full_purified` (float)
**Expected Rows:** 3 (one per paradigm)

**Validation Requirement:**
Validation tools MUST be used after plot data preparation tool execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_correlation_comparison_data.csv: 6 rows, 5 columns, types: paradigm (object), ctt_type (object), r (float64), CI_lower (float64), CI_upper (float64)
- data/step08_aic_comparison_data.csv: 3 rows, 5 columns, types: paradigm (object), AIC_* (float64), delta_AIC_* (float64)

*Value Ranges:*
- r in [-1, 1] (correlation bounds)
- CI_lower in [-1, 1], CI_upper in [-1, 1]
- CI_lower <= r <= CI_upper (logical constraint)
- AIC_* > 0 (AIC positive for valid models)

*Data Quality:*
- correlation_comparison_data: All 3 paradigms x 2 CTT types present (6 rows, complete factorial)
- aic_comparison_data: All 3 paradigms present
- No NaN values in r, CI, or AIC columns
- ctt_type contains only {"Full", "Purified"} (no other values)

*Log Validation:*
- Required pattern: "Plot data preparation complete: 2 files created"
- Required pattern: "Correlation comparison: 6 rows (3 paradigms x 2 CTT types)"
- Required pattern: "AIC comparison: 3 rows (3 paradigms)"
- Forbidden patterns: "ERROR", "Missing paradigm", "NaN values detected"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Incomplete factorial design: Missing IFR Purified row")
- Log failure to logs/step08_prepare_plot_data.log
- Quit script immediately
- g_debug invoked to diagnose

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs - intermediate and final)

- data/step00_dependency_validation_report.txt (from Step 0: validation report)
- data/step01_item_mapping.csv (from Step 1: item retention table)
- data/step01_retention_summary.csv (from Step 1: paradigm-level retention rates)
- data/step02_ctt_full_scores.csv (from Step 2: Full CTT scores - all items)
- data/step03_ctt_purified_scores.csv (from Step 3: Purified CTT scores - retained items)
- data/step04_reliability_assessment.csv (from Step 4: Cronbach's alpha with bootstrap CIs)
- data/step05_correlation_analysis.csv (from Step 5: Steiger's z-test results with dual p-values)
- data/step05_steiger_assumptions_report.txt (from Step 5: assumption validation)
- data/step06_standardized_scores.csv (from Step 6: z-standardized measurements)
- data/step07_lmm_model_comparison.csv (from Step 7: AIC comparison and coefficients)
- data/step07_lmm_convergence_report.txt (from Step 7: LMM convergence details)
- data/step08_correlation_comparison_data.csv (from Step 8: plot source CSV)
- data/step08_aic_comparison_data.csv (from Step 8: plot source CSV)

### Logs (ONLY execution logs - .log files capturing stdout/stderr)

- logs/step00_load_dependencies.log
- logs/step01_map_items.log
- logs/step02_compute_full_ctt.log
- logs/step03_compute_purified_ctt.log
- logs/step04_reliability_assessment.log
- logs/step05_correlation_analysis.log
- logs/step06_standardize_measurements.log
- logs/step07_fit_parallel_lmms.log
- logs/step08_prepare_plot_data.log

### Plots (EMPTY until rq_plots runs)

- plots/ folder remains empty during analysis
- rq_plots will later create:
  - plots/correlation_comparison.png (grouped bar chart: r_full vs r_purified per paradigm)
  - plots/aic_comparison.png (grouped bar chart: AIC_IRT vs AIC_full vs AIC_purified per paradigm)

### Results (EMPTY until rq_results runs)

- results/ folder remains empty during analysis
- rq_results will later create summary.md with interpretation

---

## Expected Data Formats

### CTT Score Computation

**Full CTT (Step 2):**
- Input: Raw TQ_* columns from dfData.csv for ALL paradigm items
- Computation: Mean proportion correct per UID x Test x Paradigm
- Formula: CTT_full_IFR = sum(IFR item responses) / count(IFR items)
- Output range: [0, 1] (proportion correct)

**Purified CTT (Step 3):**
- Input: Raw TQ_* columns from dfData.csv for RETAINED paradigm items only
- Computation: Mean proportion correct per UID x Test x Paradigm
- Formula: CTT_purified_IFR = sum(retained IFR item responses) / count(retained IFR items)
- Output range: [0, 1] (proportion correct)

### Reliability Assessment (Step 4)

**Cronbach's Alpha:**
- Input: Item-level response matrix (N participants x K items)
- Computation: Alpha = (K / (K-1)) x (1 - sum(item_variances) / total_variance)
- For dichotomous items: KR-20 formula (equivalent to Cronbach's alpha)
- Output range: [0, 1] (internal consistency coefficient)

**Bootstrap Confidence Intervals:**
- Method: Sample participants with replacement (10,000 iterations)
- Recompute alpha per bootstrap sample
- CI bounds: 2.5th and 97.5th percentiles of bootstrap distribution
- Output: [alpha_CI_lower, alpha_CI_upper]

**Spearman-Brown Adjustment:**
- Purpose: Adjust Purified alpha to Full item count for fair comparison
- Formula: alpha_SB = (n x r_avg) / (1 + (n-1) x r_avg)
  - n = n_items_full / n_items_purified (item count ratio)
  - r_avg = average inter-item correlation from Purified set
- Interpretation: "If Purified set were extended to Full item count, expected alpha = alpha_SB"

### Correlation Analysis (Step 5)

**Steiger's Z-Test for Dependent Correlations:**
- Setup: Three variables (X1 = Full CTT, X2 = Purified CTT, X3 = IRT theta)
- Correlations: r13 (Full-IRT), r23 (Purified-IRT), r12 (Full-Purified)
- Null hypothesis: r13 = r23
- Test statistic: z = (r13 - r23) / sqrt(2 x (1 - r12) x ((n - 3)))
- Output: z-statistic, p-value (one-tailed if directional hypothesis)

**Decision D068 Dual P-Values:**
- p_uncorrected: Raw p-value from Steiger's test
- p_bonferroni: p_uncorrected x 3 (Bonferroni correction for 3 paradigms), capped at 1.0
- Both values reported in output CSV

### Standardization (Step 6)

**Z-Score Transformation:**
- Formula: z = (x - mean(x)) / SD(x)
- Computed across all 400 observations (grand mean and SD)
- Validation: mean(z) in [-0.01, 0.01], SD(z) in [0.99, 1.01]
- Purpose: Ensures comparable LMM coefficients across measurement types

### LMM Fitting (Step 7)

**Model Formula:**
```
Score ~ TSVR_hours + (TSVR_hours | UID)
```
- Fixed effects: Intercept, TSVR_hours slope (forgetting rate)
- Random effects: By-participant intercepts and slopes with correlation
- REML = False (maximum likelihood for AIC comparison)

**Convergence Contingency:**
- If random slopes fail: Try bobyqa, nlminb optimizers
- If still fail: Likelihood ratio test (LRT) comparing slopes vs intercepts-only
- If LRT p < 0.05: Retain slopes with simplified correlation (uncorrelated random effects)
- If LRT p >= 0.05: Use intercepts-only model
- Apply SAME structure to all models for valid AIC comparison

**AIC Comparison:**
- delta_AIC = AIC_full - AIC_purified
- Interpretation: delta_AIC > 2 = Purified model meaningfully better (Burnham & Anderson)
- Negative delta_AIC = Full model better (unexpected - purification should improve fit)

### Plot Data Formats (Step 8)

**Correlation Comparison Data:**
- Long format: One row per paradigm x CTT type combination
- Enables grouped bar chart with error bars
- Columns: paradigm, ctt_type, r, CI_lower, CI_upper

**AIC Comparison Data:**
- Wide format: One row per paradigm
- Enables grouped bar chart comparing 3 AIC values per paradigm
- Columns: paradigm, AIC_IRT, AIC_full, AIC_purified, delta_AIC

---

## Cross-RQ Dependencies

### Dependency Type: DERIVED Data from RQ 5.3.1

**This RQ requires outputs from:**
- **RQ 5.3.1** (Paradigm-Specific Trajectories - provides purified items and IRT theta)
  - File: results/ch5/5.3.1/data/step02_purified_items.csv
  - Used in: Steps 1, 2, 3 (identify Full vs Purified item sets)
  - Rationale: RQ 5.3.1 performs IRT purification per Decision D039. This RQ compares CTT scores using those purified vs full item sets.

  - File: results/ch5/5.3.1/data/step03_theta_scores.csv
  - Used in: Steps 5, 6, 7 (IRT theta as convergent validity criterion)
  - Rationale: IRT theta is the reference measurement. This RQ tests whether Purified CTT correlates more strongly with theta than Full CTT.

  - File: results/ch5/5.3.1/data/step00_tsvr_mapping.csv
  - Used in: Steps 6, 7 (TSVR_hours as LMM time variable per Decision D070)
  - Rationale: LMMs require time variable. TSVR_hours (actual elapsed time) more precise than nominal days.

**Execution Order Constraint:**
1. RQ 5.3.1 must complete Steps 0-3 first (extraction, IRT Pass 1, purification, IRT Pass 2)
2. This RQ executes after RQ 5.3.1 completion (uses purified items, theta, TSVR)

**Data Source Boundaries:**
- **RAW data:** dfData.csv extracted directly for Full CTT computation (Step 2)
- **DERIVED data:** RQ 5.3.1 outputs for Purified CTT computation (Step 3) and convergent validity (Step 5)
- **Scope:** This RQ does NOT re-calibrate IRT models (uses RQ 5.3.1 theta as fixed reference)

**Validation:**
- Step 0: Check results/ch5/5.3.1/status.yaml exists and rq_results.status = "success"
- Step 0: Check all 4 required files exist (circuit breaker: EXPECTATIONS ERROR if missing)
- If RQ 5.3.1 incomplete: Quit with "RQ 5.3.1 must complete before RQ 5.3.6"

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

[Per-step validation details already embedded in each step specification above - see Steps 0-8 for complete validation requirements including substance criteria]

---

## Summary

**Total Steps:** 9 (Step 0: dependency validation + Steps 1-8: analysis)

**Estimated Runtime:** 30-90 minutes total
- Step 0: <5 min (file validation)
- Step 1: <5 min (item mapping)
- Step 2: <10 min (Full CTT computation)
- Step 3: <10 min (Purified CTT computation)
- Step 4: 15-30 min (Cronbach's alpha with 10,000 bootstrap iterations)
- Step 5: <10 min (Steiger's z-test)
- Step 6: <5 min (standardization)
- Step 7: 30-60 min (9 LMMs: 3 paradigms x 3 measurement types)
- Step 8: <5 min (plot data aggregation)

**Cross-RQ Dependencies:** RQ 5.3.1 (must complete Steps 0-3 before this RQ can execute)

**Primary Outputs:**
- Item mapping and retention rates per paradigm
- Full CTT and Purified CTT scores per paradigm
- Cronbach's alpha with bootstrap CIs (reliability assessment)
- Steiger's z-test results with dual p-values (convergent validity)
- Parallel LMM AIC comparison (model fit assessment)
- Plot source CSVs for correlation and AIC comparisons

**Validation Coverage:** 100% (all 9 steps have validation requirements)

**Key Theoretical Contributions:**
- Tests whether IRT purification improves CTT measurement precision
- Validates purification process via convergent validity (higher theta correlation)
- Demonstrates improved model fit (lower AIC) as evidence for reduced measurement noise
- Provides empirical evidence for whether purification benefits translate across measurement frameworks (IRT vs CTT)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-02): Initial plan created by rq_planner agent for RQ 5.3.6
