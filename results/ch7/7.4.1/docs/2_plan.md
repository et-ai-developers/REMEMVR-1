# Analysis Plan: RQ 7.4.1 - RAVLT Free Recall vs Recognition Process-Specific Prediction

**Research Question:** 7.4.1
**Created:** 2026-01-04
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines process-specific transfer between RAVLT (standardized verbal free recall) and REMEMVR paradigm-specific theta scores across N=100 participants. The analysis tests Transfer-Appropriate Processing (TAP) theory by comparing bivariate correlations: r(RAVLT, REMEMVR_FreeRecall) vs r(RAVLT, REMEMVR_Recognition). 

**Pipeline:** Correlation analysis with dependent correlation comparison
**Steps:** 6 total analysis steps (Step 0: data extraction + Steps 1-5: analysis)
**Estimated Runtime:** Low (approximately 10-15 minutes total - primarily data manipulation and correlation computation)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni correction)
- Bootstrap confidence intervals with 1000 iterations and seed=42 for reproducibility
- Steiger's Z-test for dependent correlation comparison
- Alpha = 0.00179 (chapter-level correction per concept)

---

## Analysis Plan

This RQ requires 6 steps:

### Step 0: Extract RAVLT Cognitive Test Data

**Dependencies:** None (first step)
**Complexity:** Low (data extraction only, <2 minutes)

**Purpose:** Extract RAVLT Total scores from master.xlsx cognitive assessments

**Input:**
- File: data/cache/master.xlsx (project-level data source)
- Required Sheet: Data or cognitive assessment sheet
- Expected Variables: RAVLT_T1, RAVLT_T2, RAVLT_T3, RAVLT_T4, RAVLT_T5 (trial scores)
- Filter: All 100 participants with complete RAVLT data

**Processing:**
- Use extract_cognitive_tests function to extract RAVLT scores
- Compute RAVLT_Total = T1 + T2 + T3 + T4 + T5 (total learning across 5 trials)
- Retain raw scores (NOT T-scored) per concept requirement
- Validate no missing RAVLT data

**Output:**
- File: data/step00_cognitive_tests.csv
- Format: CSV with columns: UID, RAVLT_T1, RAVLT_T2, RAVLT_T3, RAVLT_T4, RAVLT_T5, RAVLT_Total
- Expected Rows: 100 participants
- Expected Columns: 7 total (UID + 6 RAVLT variables)

**Validation Requirement:**
Validation tools MUST be used after analysis tool execution. Specific validation tools will be determined by rq_tools based on data extraction requirements. The rq_analysis agent will embed validation tool calls after the analysis tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_cognitive_tests.csv: 100 rows x 7 columns (UID: object, RAVLT_T1-T5: int64, RAVLT_Total: int64)

*Value Ranges:*
- RAVLT_T1-T5 each in [0, 15] (maximum 15 words per trial)
- RAVLT_Total in [0, 75] (sum of 5 trials)
- RAVLT_Total typically 25-65 for healthy adults

*Data Quality:*
- All 100 participants present (no missing UIDs)
- No NaN values in RAVLT columns (complete cognitive data required)
- No duplicate UIDs
- RAVLT_Total = sum(T1 + T2 + T3 + T4 + T5) for all rows

*Log Validation:*
- Required: "RAVLT extraction complete: 100 participants"
- Required: "RAVLT_Total computed: min=X, max=Y, mean=Z"
- Forbidden: "ERROR", "NaN detected in RAVLT", "Missing participants"

**Expected Behavior:** Extract cognitive test scores, compute total score, validate completeness

---

### Step 1: Extract Paradigm-Specific Theta Scores

**Dependencies:** None (independent extraction)
**Complexity:** Low (data loading from Ch5 results, <2 minutes)

**Purpose:** Load theta scores from Ch5 5.3.x paradigm analyses (Free Recall vs Recognition)

**Input:**
- Source: Ch5 5.3.x results (paradigm-specific theta scores)
- Required Files: Results from paradigm analyses with IFR (Free Recall) and IRE (Recognition) theta estimates
- Expected Format: Composite_ID, paradigm, theta scores aggregated across domains (What/Where/When)

**Processing:**
- Use extract_domain_theta_scores function to load Ch5 paradigm results
- Filter to IFR (Image-First Recall = Free Recall) and IRE (Image-Recognition = Recognition) paradigms only
- Aggregate theta scores across all memory domains (What/Where/When) per paradigm per participant
- Compute mean theta per participant per paradigm across all 4 tests (T1-T4)

**Output:**
- File: data/step01_paradigm_theta.csv
- Format: CSV with columns: UID, Theta_FreeRecall, Theta_Recognition
- Expected Rows: 100 participants
- Expected Columns: 3 (UID + 2 theta columns)

**Validation Requirement:**
Validation tools MUST be used after analysis tool execution. Specific validation tools will be determined by rq_tools based on theta score extraction requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_paradigm_theta.csv: 100 rows x 3 columns (UID: object, Theta_FreeRecall: float64, Theta_Recognition: float64)

*Value Ranges:*
- Theta_FreeRecall in [-3, 3] (typical IRT ability range)
- Theta_Recognition in [-3, 3] (typical IRT ability range)
- Both theta variables should be roughly normal distribution

*Data Quality:*
- All 100 participants present (no missing UIDs)
- No NaN values in theta columns (complete paradigm data required)
- No duplicate UIDs
- Mean theta values near 0 (IRT calibration centers at 0)

*Log Validation:*
- Required: "Paradigm theta extraction complete: 100 participants"
- Required: "Free Recall theta: mean=X, sd=Y"
- Required: "Recognition theta: mean=X, sd=Y"
- Forbidden: "ERROR", "NaN detected in theta", "Missing paradigm data"

**Expected Behavior:** Load paradigm-specific theta scores, aggregate across domains and tests

---

### Step 2: Merge RAVLT and Theta Data

**Dependencies:** Steps 0, 1 (requires both cognitive tests and theta scores)
**Complexity:** Low (data merging, <1 minute)

**Purpose:** Create unified analysis dataset merging RAVLT scores with paradigm theta scores

**Input:**
- File 1: data/step00_cognitive_tests.csv (RAVLT scores)
- File 2: data/step01_paradigm_theta.csv (paradigm theta scores)
- Merge Key: UID (participant identifier)

**Processing:**
- Use merge_theta_cognitive function to merge datasets on UID
- Inner join to ensure only participants with both RAVLT and theta data
- Validate no missing values after merge
- Add correlation input variables for analysis

**Output:**
- File: data/step02_correlation_input.csv
- Format: CSV with columns: UID, RAVLT_Total, Theta_FreeRecall, Theta_Recognition
- Expected Rows: 100 participants (or fewer if missing data)
- Expected Columns: 4 total

**Validation Requirement:**
Validation tools MUST be used after analysis tool execution. Specific validation tools will be determined by rq_tools based on data merging requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_correlation_input.csv: 100 rows x 4 columns (UID: object, RAVLT_Total: int64, Theta_FreeRecall: float64, Theta_Recognition: float64)

*Value Ranges:*
- RAVLT_Total in [0, 75] (sum of 5 trials)
- Theta_FreeRecall in [-3, 3] (IRT ability range)
- Theta_Recognition in [-3, 3] (IRT ability range)

*Data Quality:*
- Expected N: 100 participants (no data loss from merge)
- No NaN values (complete cases only)
- No duplicate UIDs
- All variables numeric and within expected ranges

*Log Validation:*
- Required: "Merge complete: 100 participants with complete data"
- Required: "All variables validated: RAVLT, Theta_FreeRecall, Theta_Recognition"
- Forbidden: "ERROR", "NaN values detected", "Merge failed", "Data loss detected"

**Expected Behavior:** Merge cognitive and theta data, validate completeness

---

### Step 3: Compute Bivariate Correlations with Bootstrap CIs

**Dependencies:** Step 2 (requires merged correlation input data)
**Complexity:** Medium (bootstrap computation, ~5 minutes for 1000 iterations)

**Purpose:** Compute r(RAVLT, FreeRecall) and r(RAVLT, Recognition) with confidence intervals

**Input:**
- File: data/step02_correlation_input.csv
- Required Columns: RAVLT_Total, Theta_FreeRecall, Theta_Recognition
- Expected N: 100 participants

**Processing:**
- Use bootstrap_correlation_ci function with following parameters:
  - n_bootstrap = 1000 (per v5.1 specification)
  - random_state = 42 (reproducibility)
  - confidence_level = 0.95 (95% CIs)
  - method = 'pearson' (Pearson product-moment correlations)
- Compute r1 = cor(RAVLT_Total, Theta_FreeRecall)
- Compute r2 = cor(RAVLT_Total, Theta_Recognition)
- Bootstrap confidence intervals for both correlations
- Compute both uncorrected and Bonferroni-corrected p-values (Decision D068)

**Output:**
- File: data/step03_correlation_results.csv
- Format: CSV with columns: correlation_pair, r_value, CI_lower, CI_upper, p_uncorrected, p_bonferroni, n_obs
- Expected Rows: 2 (one for each correlation)
- Expected Columns: 7 total

**Validation Requirement:**
Validation tools MUST be used after analysis tool execution. Specific validation tools will be determined by rq_tools based on correlation computation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_correlation_results.csv: 2 rows x 7 columns (correlation_pair: object, r_value: float64, CI_lower: float64, CI_upper: float64, p_uncorrected: float64, p_bonferroni: float64, n_obs: int64)

*Value Ranges:*
- r_value in [-1, 1] (correlation bounds)
- CI_lower in [-1, 1], CI_upper in [-1, 1]
- CI_lower < r_value < CI_upper for all rows
- p_uncorrected in [0, 1], p_bonferroni in [0, 1]
- p_bonferroni >= p_uncorrected (correction increases p-values)
- n_obs = 100 for both correlations

*Data Quality:*
- Exactly 2 rows (Free Recall and Recognition correlations)
- No NaN values in any column
- Bootstrap CIs properly computed (CI_upper > CI_lower)
- Expected correlation direction: both positive (memory abilities correlated)

*Log Validation:*
- Required: "Bootstrap correlations computed: 1000 iterations with seed=42"
- Required: "RAVLT-FreeRecall: r=X.XX [CI_lower, CI_upper]"
- Required: "RAVLT-Recognition: r=X.XX [CI_lower, CI_upper]"
- Required: "Dual p-values computed: uncorrected and Bonferroni"
- Forbidden: "ERROR", "Bootstrap failed", "NaN in correlations"

**Expected Behavior:** Compute correlations with bootstrap confidence intervals and dual p-values

---

### Step 4: Test Process-Specificity with Steiger's Z-Test

**Dependencies:** Step 3 (requires correlation results)
**Complexity:** Low (dependent correlation test, <2 minutes)

**Purpose:** Test H1: r(RAVLT, FreeRecall) > r(RAVLT, Recognition) using Steiger's Z-test

**Input:**
- File: data/step03_correlation_results.csv (correlation results)
- File: data/step02_correlation_input.csv (raw data for r23 computation)
- Required: r12, r13, r23 correlations and sample size

**Processing:**
- Use compare_correlations_dependent function with:
  - r12 = cor(RAVLT, FreeRecall) from Step 3 results
  - r13 = cor(RAVLT, Recognition) from Step 3 results
  - r23 = cor(FreeRecall, Recognition) computed from raw data
  - n = 100 (sample size)
- Perform Steiger's Z-test for dependent correlations
- Test against chapter-level alpha = 0.00179 (Bonferroni correction)
- Compute effect size: difference in correlation coefficients (r1 - r2)

**Output:**
- File: data/step04_steiger_test.csv
- Format: CSV with columns: z_statistic, p_value, r_difference, significant, interpretation, alpha_threshold
- Expected Rows: 1 (single test result)
- Expected Columns: 6 total

**Validation Requirement:**
Validation tools MUST be used after analysis tool execution. Specific validation tools will be determined by rq_tools based on dependent correlation testing requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_steiger_test.csv: 1 row x 6 columns (z_statistic: float64, p_value: float64, r_difference: float64, significant: bool, interpretation: object, alpha_threshold: float64)

*Value Ranges:*
- z_statistic unrestricted (can be positive/negative)
- p_value in [0, 1]
- r_difference in [-2, 2] (difference of correlations)
- alpha_threshold = 0.00179 (chapter-level correction)
- significant: True/False based on p_value < alpha_threshold

*Data Quality:*
- Exactly 1 row (single test)
- No NaN values
- Expected r_difference > 0 (Free Recall > Recognition correlation per hypothesis)
- Consistent significance determination (significant = p_value < alpha_threshold)

*Log Validation:*
- Required: "Steiger's Z-test computed: Z=X.XX, p=Y.YYY"
- Required: "Correlation difference: r_diff=X.XX (FreeRecall - Recognition)"
- Required: "Alpha threshold: 0.00179 (chapter-level correction)"
- Required: "Result: significant=True/False"
- Forbidden: "ERROR", "Steiger test failed", "NaN in test results"

**Expected Behavior:** Test dependent correlations using Steiger's Z-test with chapter-corrected alpha

---

### Step 5: Bootstrap Sensitivity Analysis for Correlation Difference

**Dependencies:** Step 4 (requires Steiger test results and raw data)
**Complexity:** Medium (bootstrap analysis, ~5 minutes for 1000 iterations)

**Purpose:** Bootstrap confidence intervals for correlation difference (r1 - r2) as sensitivity analysis

**Input:**
- File: data/step02_correlation_input.csv (raw data)
- Required Columns: RAVLT_Total, Theta_FreeRecall, Theta_Recognition
- Parameters: 1000 bootstrap iterations, seed=42

**Processing:**
- Bootstrap sampling with replacement (1000 iterations, seed=42)
- For each bootstrap sample:
  - Compute r1_boot = cor(RAVLT, FreeRecall)
  - Compute r2_boot = cor(RAVLT, Recognition)  
  - Compute diff_boot = r1_boot - r2_boot
- Compute 95% confidence interval for correlation difference
- Validate significance by checking if CI excludes zero
- Compare with Steiger's Z-test results for consistency

**Output:**
- File: data/step05_bootstrap_sensitivity.csv
- Format: CSV with columns: statistic, value, CI_lower, CI_upper, excludes_zero, n_bootstrap, seed
- Expected Rows: 1 (correlation difference result)
- Expected Columns: 7 total

**Validation Requirement:**
Validation tools MUST be used after analysis tool execution. Specific validation tools will be determined by rq_tools based on bootstrap sensitivity analysis requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_bootstrap_sensitivity.csv: 1 row x 7 columns (statistic: object, value: float64, CI_lower: float64, CI_upper: float64, excludes_zero: bool, n_bootstrap: int64, seed: int64)

*Value Ranges:*
- value in [-2, 2] (correlation difference)
- CI_lower in [-2, 2], CI_upper in [-2, 2]
- CI_lower < value < CI_upper
- n_bootstrap = 1000 (fixed parameter)
- seed = 42 (fixed parameter)
- excludes_zero: True/False based on confidence interval bounds

*Data Quality:*
- Exactly 1 row (single bootstrap result)
- No NaN values
- statistic = "correlation_difference"
- Proper CI computation (CI_upper > CI_lower)
- Expected positive value (Free Recall > Recognition per hypothesis)

*Log Validation:*
- Required: "Bootstrap sensitivity analysis: 1000 iterations with seed=42"
- Required: "Correlation difference: X.XX [CI_lower, CI_upper]"
- Required: "CI excludes zero: True/False"
- Required: "Bootstrap distribution computed successfully"
- Forbidden: "ERROR", "Bootstrap failed", "NaN in sensitivity results"

**Expected Behavior:** Bootstrap confidence intervals for correlation difference, validate against zero

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 ’ Step 1:** Independent extractions (no transformation)
- Step 0: RAVLT cognitive scores (wide format: 1 row per participant)
- Step 1: Paradigm theta scores (wide format: 1 row per participant)

**Step 1 ’ Step 2:** Inner join merge
- Input: Two separate DataFrames (RAVLT, theta)
- Merge key: UID (participant identifier)
- Output: Combined DataFrame with all analysis variables

**Step 2 ’ Step 3:** Correlation computation
- Input: Analysis dataset (100 rows x 4 columns)
- Processing: Bootstrap correlations between variable pairs
- Output: Correlation results (2 rows x 7 columns)

**Step 3 ’ Step 4:** Dependent correlation test
- Input: Correlation coefficients + raw data
- Processing: Steiger's Z-test for dependent correlations
- Output: Single test result (1 row x 6 columns)

**Step 4 ’ Step 5:** Bootstrap sensitivity analysis
- Input: Raw analysis dataset
- Processing: Bootstrap correlation differences
- Output: Sensitivity results (1 row x 7 columns)

### Column Naming Conventions

**Core Variables:**
- UID: Participant identifier (object)
- RAVLT_Total: Sum of 5 RAVLT trials (int64)
- Theta_FreeRecall: IRT ability for Free Recall paradigm (float64)
- Theta_Recognition: IRT ability for Recognition paradigm (float64)

**Correlation Results:**
- correlation_pair: Description of correlation (object)
- r_value: Pearson correlation coefficient (float64)
- CI_lower, CI_upper: Bootstrap 95% confidence bounds (float64)
- p_uncorrected, p_bonferroni: Dual p-values per D068 (float64)

**Statistical Test Results:**
- z_statistic: Steiger's Z test statistic (float64)
- p_value: Two-tailed p-value (float64)
- r_difference: Correlation difference (r1 - r2) (float64)
- significant: Boolean significance result (bool)

### Data Type Constraints

**Identifiers:** UID as object (string), no missing values allowed
**Scores:** RAVLT as int64 [0, 75], theta as float64 [-3, 3]
**Statistics:** Correlations as float64 [-1, 1], p-values as float64 [0, 1]
**Flags:** Significance as bool (True/False), no NaN values

---

## Cross-RQ Dependencies

**Dependency Type:** DERIVED Data from Ch5 Paradigm Analyses

**This RQ requires outputs from:**
- **Ch5 5.3.x** (Paradigm-Specific Analyses - Free Recall vs Recognition)
  - Source: Paradigm-separated theta scores from IFR (Free Recall) and IRE (Recognition)
  - Used in: Step 1 (extract paradigm-specific theta scores)
  - Rationale: This RQ compares RAVLT prediction across REMEMVR paradigms. Requires paradigm-specific (not domain-specific) theta estimates.

**Expected Source Files:**
- Results from Ch5 paradigm analyses with theta scores separated by retrieval paradigm
- Format: Composite_ID or UID-based theta scores for IFR and IRE paradigms
- Coverage: All memory domains (What/Where/When) aggregated within paradigm

**Data Source Boundaries:**
- **RAW data:** master.xlsx RAVLT cognitive scores (no RQ dependencies)
- **DERIVED data:** Ch5 5.3.x paradigm-specific theta scores (RQ dependency)
- **Scope:** This RQ analyzes correlations between standardized cognitive test and VR paradigm abilities

**Validation:**
- Step 1: Check availability of Ch5 paradigm results with IFR and IRE theta scores
- If paradigm data missing ’ STEP ERROR with message to complete Ch5 5.3.x first
- Expected paradigm coverage: Free Recall (IFR) and Recognition (IRE) with complete theta estimates

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
- g_code (Step 14 workflow) will generate stepN_name.py scripts with validation function calls
- bash execution (Step 14 workflow) will run analysis ’ validation ’ error on validation failure

**Downstream Agent Requirements:**
- **rq_tools:** MUST specify validation tool for EVERY analysis step (no exceptions)
- **rq_analysis:** MUST embed validation tool call for EVERY analysis step (no exceptions)
- **g_code:** MUST generate code with validation function calls (no exceptions)
- **rq_inspect:** MUST verify validation ran successfully (checks logs/stepN_name.log for validation output)

### Validation Requirements By Step

#### Step 0: Extract RAVLT Cognitive Test Data

**Analysis Tool:** (determined by rq_tools - likely tools.data.extract_cognitive_tests)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_data_format)

**What Validation Checks:**
- Output file exists (data/step00_cognitive_tests.csv)
- Expected column count (7 columns: UID + 6 RAVLT variables)
- Expected row count (100 participants)
- RAVLT value ranges valid (T1-T5 in [0,15], Total in [0,75])
- No NaN values (complete cognitive data required)
- RAVLT_Total = sum(T1+T2+T3+T4+T5) for all participants

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 100 participants, found 95")
- Log failure to logs/step00_extract_cognitive_tests.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked by master to diagnose root cause

---

#### Step 1: Extract Paradigm-Specific Theta Scores

**Analysis Tool:** (determined by rq_tools - likely tools.data.extract_domain_theta_scores)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_numeric_range)

**What Validation Checks:**
- Output file exists (data/step01_paradigm_theta.csv)
- Expected row count (100 participants)
- Expected column count (3: UID + 2 theta columns)
- Theta values in valid IRT range ([-3, 3])
- No NaN values (complete paradigm data required)
- Both paradigms represented (Free Recall and Recognition theta available)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Theta values outside range [-3,3]")
- Log failure to logs/step01_extract_paradigm_theta.log
- Quit script immediately
- g_debug invoked to diagnose (common causes: missing Ch5 results, paradigm mismatch)

---

#### Step 2: Merge RAVLT and Theta Data

**Analysis Tool:** (determined by rq_tools - likely tools.data.merge_theta_cognitive)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure)

**What Validation Checks:**
- Output file exists (data/step02_correlation_input.csv)
- No data loss from merge (100 participants maintained)
- All required columns present (UID, RAVLT_Total, Theta_FreeRecall, Theta_Recognition)
- No NaN values after merge (complete cases only)
- Variable ranges maintained post-merge

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Data loss detected: 95 rows after merge")
- Log failure to logs/step02_merge_ravlt_theta.log
- Quit script immediately
- g_debug invoked to investigate merge issues

---

#### Step 3: Compute Bivariate Correlations with Bootstrap CIs

**Analysis Tool:** (determined by rq_tools - likely tools.bootstrap.bootstrap_correlation_ci)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_correlation_test_d068)

**What Validation Checks:**
- Output file exists (data/step03_correlation_results.csv)
- Expected number of correlations (2: Free Recall and Recognition)
- Correlation values in valid range ([-1, 1])
- Bootstrap CIs properly computed (CI_lower < r_value < CI_upper)
- Dual p-values present (uncorrected and Bonferroni per D068)
- Bootstrap parameters correct (n=1000, seed=42)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Bootstrap CI validation failed")
- Log failure to logs/step03_compute_correlations.log
- Quit script immediately
- g_debug invoked to diagnose correlation/bootstrap issues

---

#### Step 4: Test Process-Specificity with Steiger's Z-Test

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_ctt.compare_correlations_dependent)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_hypothesis_test_dual_pvalues)

**What Validation Checks:**
- Output file exists (data/step04_steiger_test.csv)
- Single test result (1 row)
- Z-statistic and p-value computed
- Alpha threshold correct (0.00179 chapter-level correction)
- Significance determination consistent (p < alpha)
- Effect size (correlation difference) computed

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Steiger test computation failed")
- Log failure to logs/step04_steiger_test.log
- Quit script immediately
- g_debug invoked to diagnose dependent correlation test issues

---

#### Step 5: Bootstrap Sensitivity Analysis for Correlation Difference

**Analysis Tool:** (determined by rq_tools - likely tools.bootstrap.bootstrap_statistic)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_bootstrap_stability)

**What Validation Checks:**
- Output file exists (data/step05_bootstrap_sensitivity.csv)
- Bootstrap parameters correct (n=1000, seed=42)
- Confidence interval properly computed
- Zero exclusion determination correct
- Consistency with Steiger test results
- Single sensitivity result (1 row)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Bootstrap sensitivity analysis failed")
- Log failure to logs/step05_bootstrap_sensitivity.log
- Quit script immediately
- g_debug invoked to diagnose bootstrap sensitivity issues

---

## Summary

**Total Steps:** 6 (Step 0: extraction + Steps 1-5: analysis)
**Estimated Runtime:** Low (10-15 minutes total - primarily bootstrap computation time)
**Cross-RQ Dependencies:** Ch5 5.3.x paradigm analyses (Free Recall and Recognition theta scores)
**Primary Outputs:** 
- Bivariate correlations with bootstrap confidence intervals
- Steiger's Z-test for process-specificity hypothesis
- Bootstrap sensitivity analysis for correlation difference
- Complete correlation analysis dataset

**Validation Coverage:** 100% (all 6 steps have validation requirements)

**Key Analysis Features:**
- Process-specific transfer hypothesis testing (TAP theory)
- Dependent correlation comparison using Steiger's Z-test
- Bootstrap confidence intervals for robustness (1000 iterations, seed=42)
- Dual p-value reporting per Decision D068
- Chapter-level alpha correction (± = 0.00179)
- Complete sensitivity analysis for correlation difference

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan ’ creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml ’ creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml ’ generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2026-01-04): Initial plan created by rq_planner agent for process-specific transfer analysis