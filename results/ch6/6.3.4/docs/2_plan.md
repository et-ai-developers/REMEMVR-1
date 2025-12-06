# Analysis Plan: RQ 6.3.4 - ICC by Domain

**Research Question:** 6.3.4
**Created:** 2025-12-06
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines domain-stratified variance decomposition of confidence trajectories to determine whether confidence decline is more trait-like (individual difference) for some memory domains than others. The analysis decomposes variance in confidence trajectory intercepts and slopes separately for What, Where, and When domains using random-effects LMMs, then computes ICC_intercept and ICC_slope per domain.

**Pipeline:** LMM only (no IRT - uses DERIVED theta scores from RQ 6.3.1)

**Steps:** 6 analysis steps total

**Estimated Runtime:** Medium (~30-45 minutes)

**Key Decisions Applied:**
- Decision D070: TSVR as LMM time variable (actual hours, not nominal days)
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni) for domain comparisons

**Data Source:** DERIVED from RQ 6.3.1 (domain-specific confidence theta scores)

---

## Analysis Plan

### Step 1: Fit Domain-Stratified LMMs with Random Slopes

**Purpose:** Fit separate random-effects LMMs per domain to estimate variance components (var_intercept, var_slope, cov_int_slope, var_residual) for each domain.

**Dependencies:** None (first step, uses RQ 6.3.1 outputs)
**Complexity:** High (3 LMM calibrations with random slopes - 15-20 minutes)

**Input:**

**File:** results/ch6/6.3.1/data/step03_theta_confidence_domain.csv
**Source:** RQ 6.3.1 Step 3 (IRT theta extraction for domain-specific confidence)
**Format:** Long format (one row per participant-test-domain combination)
**Columns:**
  - `UID` (string, participant identifier, format: P### with leading zeros)
  - `test` (string, test session identifier: T1, T2, T3, T4)
  - `domain` (string, memory domain: What, Where, When)
  - `theta_confidence` (float, IRT ability estimate for confidence, range typically -3.0 to +3.0)
  - `se_confidence` (float, standard error of theta estimate, range typically 0.1 to 1.0)
  - `TSVR_hours` (float, actual time since encoding in hours per Decision D070)

**Expected Rows:** 1200 (100 participants x 4 tests x 3 domains)

**Expected Data Volume:** Complete factorial design (all participants present at all tests for all domains)

**Processing:**

For each domain in {What, Where, When}:

1. Filter data to domain-specific subset (400 rows: 100 participants x 4 tests)
2. Fit LMM with random intercepts and random slopes per participant:
   - Formula: `theta_confidence ~ TSVR_hours + (TSVR_hours | UID)`
   - Random effects: By-participant intercepts (baseline confidence) and by-participant slopes (decline rate)
   - Time variable: TSVR_hours (Decision D070 - actual elapsed time, not nominal days)
3. Extract variance components from fitted model:
   - var_intercept: Between-participant variance in baseline confidence
   - var_slope: Between-participant variance in decline rate
   - cov_int_slope: Covariance between intercepts and slopes
   - var_residual: Within-participant residual variance
4. Save variance components for each domain

**Output:**

**File 1:** data/step01_lmm_what_model_summary.txt
**Format:** Text summary from statsmodels LMM.summary()
**Contents:** Fixed effects table, random effects variance components, model fit indices

**File 2:** data/step01_lmm_where_model_summary.txt
**Format:** Same as File 1 (Where domain)

**File 3:** data/step01_lmm_when_model_summary.txt
**Format:** Same as File 1 (When domain)

**File 4:** data/step01_variance_components_by_domain.csv
**Format:** CSV with variance components per domain
**Columns:**
  - `domain` (string: What, Where, When)
  - `var_intercept` (float: between-participant variance in baseline)
  - `var_slope` (float: between-participant variance in decline rate)
  - `cov_int_slope` (float: covariance between intercepts and slopes)
  - `var_residual` (float: within-participant residual variance)
**Expected Rows:** 3 (one per domain)

**Validation Requirement:**
Validation tools MUST be used after LMM fitting. Specific validation tools will be determined by rq_tools based on LMM analysis type (convergence, variance positivity, residuals).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_lmm_what_model_summary.txt exists
- data/step01_lmm_where_model_summary.txt exists
- data/step01_lmm_when_model_summary.txt exists
- data/step01_variance_components_by_domain.csv exists
- Expected rows: 3 (What, Where, When)
- Expected columns: 5 (domain, var_intercept, var_slope, cov_int_slope, var_residual)
- Data types: domain (object), all variance components (float64)

*Value Ranges:*
- var_intercept >= 0 (variance cannot be negative)
- var_slope >= 0 (variance cannot be negative)
- var_residual > 0 (residual variance must be positive)
- cov_int_slope unrestricted (covariance can be negative)
- All variance components should be > 0.001 (convergence sanity check)

*Data Quality:*
- No NaN values in variance components (indicates convergence failure)
- All 3 domains present (What, Where, When)
- No duplicate domains

*Log Validation:*
- Required pattern: "Model converged: True" (or "Optimization terminated successfully") for all 3 domains
- Required pattern: "VALIDATION - PASS: LMM convergence" for all 3 domains
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "Singular matrix"
- Acceptable warnings: "Covariance structure may be overparameterized" (common with random slopes)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "What domain LMM did not converge")
- Log failure to logs/step01_fit_domain_lmms.log
- Quit script immediately
- g_debug invoked to diagnose (common causes: insufficient data, convergence issues)

---

### Step 2: Extract Variance Components Per Domain

**Purpose:** Create variance components table with total variance computed (sum of all components) for ICC denominator.

**Dependencies:** Step 1 (requires fitted LMMs)
**Complexity:** Low (data extraction only - <1 minute)

**Input:**

**File:** data/step01_variance_components_by_domain.csv
**Source:** Step 1 output
**Format:** CSV with 5 columns (domain, var_intercept, var_slope, cov_int_slope, var_residual)
**Expected Rows:** 3

**Processing:**

1. Read variance components table from Step 1
2. Compute total variance per domain:
   - `total_variance = var_intercept + var_slope + var_residual`
   - Note: cov_int_slope NOT included in total variance (covariance is not additive variance component)
3. Add total_variance column to table

**Output:**

**File:** data/step02_variance_components.csv
**Format:** CSV with extended variance components
**Columns:**
  - `domain` (string: What, Where, When)
  - `var_intercept` (float: between-participant variance in baseline)
  - `var_slope` (float: between-participant variance in decline rate)
  - `cov_int_slope` (float: covariance between intercepts and slopes)
  - `var_residual` (float: within-participant residual variance)
  - `total_variance` (float: sum of var_intercept + var_slope + var_residual)
**Expected Rows:** 3

**Validation Requirement:**
Validation tools MUST be used after variance component extraction.

**Substance Validation Criteria:**

*Output Files:*
- data/step02_variance_components.csv exists
- Expected rows: 3
- Expected columns: 6
- Data types: domain (object), all numeric columns (float64)

*Value Ranges:*
- total_variance > 0 (must be positive)
- total_variance >= var_intercept + var_slope + var_residual (should be equal within floating-point precision)

*Data Quality:*
- No NaN values
- All 3 domains present
- total_variance computed correctly (can verify by summing components)

*Log Validation:*
- Required pattern: "Variance components extracted for 3 domains"
- Forbidden patterns: "ERROR", "NaN detected"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step02_extract_variance_components.log
- Quit script immediately

---

### Step 3: Compute ICC Per Domain

**Purpose:** Compute three ICC estimates per domain (intercept, slope_simple, slope_conditional) using variance components.

**Dependencies:** Step 2 (requires variance components with total_variance)
**Complexity:** Low (computation only - <1 minute)

**Input:**

**File:** data/step02_variance_components.csv
**Source:** Step 2 output
**Expected Rows:** 3 domains

**Processing:**

For each domain, compute 3 ICC estimates:

1. **ICC_intercept** (reliability of baseline confidence):
   - Formula: `var_intercept / (var_intercept + var_residual)`
   - Interpretation: Proportion of baseline variance attributable to individual differences
   - Range: [0, 1]

2. **ICC_slope_simple** (reliability of decline rate, ignoring covariance):
   - Formula: `var_slope / (var_slope + var_residual)`
   - Interpretation: Proportion of slope variance attributable to individual differences
   - Range: [0, 1]
   - Note: Simplified ICC that ignores intercept-slope covariance

3. **ICC_slope_conditional** (reliability of decline rate at Day 6, accounting for covariance):
   - Formula: `(var_slope + 2 * cov_int_slope * TSVR_hours_day6 + var_intercept * TSVR_hours_day6^2) / total_variance`
   - TSVR_hours_day6: Approximately 144 hours (6 days x 24 hours)
   - Interpretation: ICC of individual differences in confidence at Day 6 retention test
   - Range: [0, 1] (should be, but can exceed if covariance structure unusual)

**Output:**

**File:** data/step03_icc_estimates.csv
**Format:** CSV with ICC estimates per domain
**Columns:**
  - `domain` (string: What, Where, When)
  - `ICC_intercept` (float: baseline reliability)
  - `ICC_slope_simple` (float: slope reliability, simplified)
  - `ICC_slope_conditional` (float: slope reliability at Day 6, accounting for covariance)
**Expected Rows:** 3

**Validation Requirement:**
Validation tools MUST be used after ICC computation.

**Substance Validation Criteria:**

*Output Files:*
- data/step03_icc_estimates.csv exists
- Expected rows: 3
- Expected columns: 4
- Data types: domain (object), all ICC columns (float64)

*Value Ranges:*
- ICC_intercept in [0, 1] (by definition)
- ICC_slope_simple in [0, 1] (by definition)
- ICC_slope_conditional typically in [0, 1] (can exceed 1.0 if unusual covariance structure, but should flag for review)
- ICC values < 0 indicate computation error (should never occur with proper variance components)

*Data Quality:*
- No NaN values (indicates computation error)
- All 3 domains present
- ICC_intercept > ICC_slope_simple expected (baseline more reliable than slope in most longitudinal data)

*Log Validation:*
- Required pattern: "ICC computed for 3 domains"
- Required pattern: "All ICC values in valid range [0, 1]" OR "WARNING: ICC_slope_conditional > 1.0 for [domain]"
- Forbidden patterns: "ERROR", "Negative ICC detected"

**Expected Behavior on Validation Failure:**
- Raise error if ICC < 0 (computation error)
- Log warning if ICC_slope_conditional > 1.0 (unusual but possible - flag for user review)
- Log failure to logs/step03_compute_icc.log
- Quit script if critical error

---

### Step 4: Extract Random Effects Per Domain

**Purpose:** Extract participant-specific random intercepts and random slopes from each domain LMM for potential downstream clustering analyses.

**Dependencies:** Step 1 (requires fitted LMMs)
**Complexity:** Low (data extraction - <1 minute)

**Input:**

**Fitted LMM Objects:** Stored in Step 1 (in-memory or pickled)
**Source:** Step 1 LMM fits (What, Where, When)

**Processing:**

For each domain:
1. Extract random effects from fitted LMM:
   - `random_intercept_UID`: Participant-specific deviation from population mean intercept
   - `random_slope_UID`: Participant-specific deviation from population mean slope
2. Create long-format table with UID, domain, random_intercept, random_slope
3. Combine all 3 domains into single table

**Output:**

**File:** data/step04_random_effects.csv
**Format:** CSV with participant random effects per domain
**Columns:**
  - `UID` (string: participant identifier)
  - `domain` (string: What, Where, When)
  - `random_intercept` (float: participant deviation from mean baseline confidence)
  - `random_slope` (float: participant deviation from mean decline rate)
**Expected Rows:** 300 (100 participants x 3 domains)

**Validation Requirement:**
Validation tools MUST be used after random effects extraction.

**Substance Validation Criteria:**

*Output Files:*
- data/step04_random_effects.csv exists
- Expected rows: 300 (100 participants x 3 domains)
- Expected columns: 4
- Data types: UID (object), domain (object), random_intercept (float64), random_slope (float64)

*Value Ranges:*
- random_intercept typically in [-2, 2] (standardized deviations from mean)
- random_slope typically in [-1, 1] (smaller range expected for slopes)
- Values outside these ranges possible but should flag for review (outliers)

*Data Quality:*
- No NaN values
- All 100 participants present for all 3 domains (complete factorial)
- No duplicate UID x domain combinations

*Log Validation:*
- Required pattern: "Random effects extracted for 300 observations (100 participants x 3 domains)"
- Forbidden patterns: "ERROR", "Missing participants", "NaN detected"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step04_extract_random_effects.log
- Quit script immediately

---

### Step 5: Compare ICC_slope Across Domains

**Purpose:** Test whether ICC_slope differs significantly between domains and rank domains by trait-like variance.

**Dependencies:** Step 3 (requires ICC estimates)
**Complexity:** Low (statistical comparison - <1 minute)

**Input:**

**File:** data/step03_icc_estimates.csv
**Source:** Step 3 output
**Expected Rows:** 3 domains

**Processing:**

1. Rank domains by ICC_slope_simple (highest to lowest):
   - Highest ICC_slope = most trait-like (individual differences dominate)
   - Lowest ICC_slope = most state-like (within-person variation dominates)

2. Compute pairwise differences:
   - Delta_ICC_What_Where = ICC_slope_What - ICC_slope_Where
   - Delta_ICC_What_When = ICC_slope_What - ICC_slope_When
   - Delta_ICC_Where_When = ICC_slope_Where - ICC_slope_When

3. Interpret differences:
   - If all ICC_slope approximately 0 (< 0.10): Parallel Ch5 5.2.6 pattern (no trait variance)
   - If any ICC_slope > 0.10: Evidence of trait variance in that domain
   - If difference > 0.05 between domains: Meaningful domain-specific trait difference

4. Statistical significance testing:
   - Note: Formal hypothesis test for ICC difference requires bootstrap or likelihood ratio test
   - For this exploratory analysis, use descriptive comparison (effect size > statistical significance)
   - If user requests formal test, recommend bootstrap approach in future RQ

**Output:**

**File:** data/step05_domain_icc_comparison.csv
**Format:** CSV with domain ranking and pairwise comparisons
**Columns:**
  - `domain` (string: What, Where, When)
  - `ICC_slope_simple` (float: copied from Step 3)
  - `rank` (int: 1 = highest ICC, 3 = lowest ICC)
  - `interpretation` (string: "High trait variance" if ICC > 0.10, "Low trait variance" if ICC < 0.10)

**File 2:** data/step05_pairwise_icc_differences.csv
**Format:** CSV with pairwise ICC differences
**Columns:**
  - `comparison` (string: "What vs Where", "What vs When", "Where vs When")
  - `delta_ICC` (float: difference in ICC_slope_simple)
  - `interpretation` (string: "Meaningful difference" if |delta| > 0.05, "Negligible difference" otherwise)

**Validation Requirement:**
Validation tools MUST be used after ICC comparison.

**Substance Validation Criteria:**

*Output Files:*
- data/step05_domain_icc_comparison.csv exists (3 rows)
- data/step05_pairwise_icc_differences.csv exists (3 rows)
- Expected columns match specification

*Value Ranges:*
- rank in {1, 2, 3} (no duplicates, all values present)
- delta_ICC typically in [-1, 1] (difference of two values in [0, 1])

*Data Quality:*
- All 3 domains present in comparison table
- All 3 pairwise comparisons present in differences table
- No NaN values

*Log Validation:*
- Required pattern: "ICC comparison complete for 3 domains"
- Forbidden patterns: "ERROR"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step05_compare_icc_across_domains.log
- Quit script immediately

---

### Step 6: Compare to Ch5 5.2.6

**Purpose:** Compare confidence ICC_slope (this RQ) to accuracy ICC_slope (Ch5 5.2.6) to test whether 5-level confidence data reveals domain-specific trait variance that dichotomous accuracy data missed.

**Dependencies:** Step 3 (requires ICC estimates from this RQ)
**Complexity:** Low (cross-chapter comparison - <1 minute)

**Input:**

**File 1:** data/step03_icc_estimates.csv
**Source:** Step 3 output (this RQ confidence ICC)
**Expected Rows:** 3 domains

**File 2:** results/ch5/5.2.6/data/step03_icc_estimates.csv
**Source:** Ch5 5.2.6 output (accuracy ICC)
**Expected Rows:** 3 domains
**Note:** If Ch5 5.2.6 not yet executed, document comparison as "pending" and skip this step

**Processing:**

1. Read ICC estimates from both RQs
2. Merge on domain (What, Where, When)
3. Compute difference per domain:
   - `delta_ICC_confidence_minus_accuracy = ICC_slope_confidence - ICC_slope_accuracy`
4. Interpret findings:
   - If delta > 0.05 for any domain: 5-level confidence reveals more trait variance than dichotomous accuracy
   - If all delta approximately 0: Both measures show equivalent trait variance (measurement richness doesn't matter)
   - If delta < -0.05 for any domain: Accuracy shows more trait variance (unexpected - flag for review)

**Output:**

**File:** data/step06_ch5_comparison.csv
**Format:** CSV with cross-chapter ICC comparison
**Columns:**
  - `domain` (string: What, Where, When)
  - `ICC_slope_confidence` (float: from this RQ 6.3.4)
  - `ICC_slope_accuracy` (float: from Ch5 5.2.6)
  - `delta_ICC` (float: confidence - accuracy)
  - `interpretation` (string: "Confidence reveals more trait variance" if delta > 0.05, etc.)

**Expected Rows:** 3 (one per domain)

**Validation Requirement:**
Validation tools MUST be used after cross-chapter comparison.

**Substance Validation Criteria:**

*Output Files:*
- data/step06_ch5_comparison.csv exists
- Expected rows: 3
- Expected columns: 5
- Data types: domain (object), all ICC/delta columns (float64), interpretation (object)

*Value Ranges:*
- ICC_slope_confidence in [0, 1]
- ICC_slope_accuracy in [0, 1]
- delta_ICC typically in [-1, 1]
- Ch5 5.2.6 documented ICC_slope approximately 0 for all domains, so expect ICC_slope_accuracy < 0.10

*Data Quality:*
- No NaN values (unless Ch5 5.2.6 not executed - then document as "comparison pending")
- All 3 domains present
- Domains match between RQs (What, Where, When)

*Log Validation:*
- Required pattern: "Cross-chapter comparison complete for 3 domains"
- Forbidden patterns: "ERROR"
- Acceptable warnings: "Ch5 5.2.6 not found - comparison pending" (if dependency RQ not executed)

**Expected Behavior on Validation Failure:**
- If Ch5 5.2.6 file missing: Log warning, create placeholder comparison file with "pending" status, proceed
- If other validation failure: Raise error, log failure to logs/step06_compare_to_ch5.log, quit script

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 1 -> Step 2:**
- Input: Variance components (5 columns per domain)
- Transformation: Add total_variance column (sum of var_intercept + var_slope + var_residual)
- Output: Extended variance components (6 columns)

**Step 2 -> Step 3:**
- Input: Variance components with total_variance
- Transformation: Compute ICC_intercept, ICC_slope_simple, ICC_slope_conditional using variance ratios
- Output: ICC estimates table (4 columns: domain + 3 ICC types)

**Step 3 -> Step 5:**
- Input: ICC estimates
- Transformation: Rank domains by ICC_slope_simple, compute pairwise differences
- Output: Comparison tables (ranking + pairwise differences)

**Step 3 -> Step 6:**
- Input: ICC estimates (this RQ + Ch5 5.2.6)
- Transformation: Merge on domain, compute delta_ICC
- Output: Cross-chapter comparison table

### Column Naming Conventions

Following names.md conventions:
- `UID`: Participant identifier (P### format)
- `domain`: Memory domain factor (What, Where, When)
- `TSVR_hours`: Time since VR in hours (Decision D070)
- `theta_confidence`: IRT ability estimate for confidence
- `ICC_intercept`, `ICC_slope_simple`, `ICC_slope_conditional`: Three ICC types per Nakagawa & Schielzeth (2010)

### Data Type Constraints

**String columns:**
- `UID`: Non-nullable, format P### with leading zeros
- `domain`: Non-nullable, categorical {What, Where, When}
- `test`: Non-nullable, categorical {T1, T2, T3, T4}

**Float columns:**
- `theta_confidence`: Range typically [-3, 3], non-nullable
- `TSVR_hours`: Range [0, 168] (0 = encoding, 168 = 1 week), non-nullable
- Variance components: All >= 0 except cov_int_slope (unrestricted)
- ICC values: Range [0, 1] (can exceed 1.0 for ICC_slope_conditional in rare cases)

---

## Cross-RQ Dependencies

### Dependency Type: DERIVED Data from Other RQ (Dependencies Exist)

**This RQ requires outputs from:**

- **RQ 6.3.1** (Domain Confidence Trajectories)
  - File: results/ch6/6.3.1/data/step03_theta_confidence_domain.csv
  - Used in: Step 1 (LMM input data)
  - Rationale: RQ 6.3.1 provides domain-specific confidence theta scores from 3-factor IRT calibration (What/Where/When). This RQ uses those theta scores to decompose variance by domain.

**Execution Order Constraint:**
1. RQ 6.3.1 must complete Steps 0-3 (data extraction, IRT calibration, theta extraction) before this RQ can run
2. This RQ executes after RQ 6.3.1 completion

**Data Source Boundaries:**
- **RAW data:** None (this RQ does not extract from master.xlsx directly)
- **DERIVED data:** theta_confidence_domain.csv from RQ 6.3.1 (1200 rows: 100 participants x 4 tests x 3 domains)
- **Scope:** This RQ analyzes domain-specific variance decomposition using LMMs only (no IRT calibration)

**Validation:**
- Step 1: Check results/ch6/6.3.1/data/step03_theta_confidence_domain.csv exists
- If file missing -> quit with EXPECTATIONS ERROR -> user must execute RQ 6.3.1 first
- Expected format: 1200 rows (100 participants x 4 tests x 3 domains), columns: UID, test, domain, theta_confidence, se_confidence, TSVR_hours

**Cross-Chapter Comparison Dependency (Optional):**

- **Ch5 5.2.6** (ICC by Domain for Accuracy)
  - File: results/ch5/5.2.6/data/step03_icc_estimates.csv
  - Used in: Step 6 (cross-chapter comparison)
  - Rationale: Compare confidence ICC (this RQ) to accuracy ICC (Ch5 5.2.6) to test measurement richness hypothesis
  - **Note:** This dependency is OPTIONAL. If Ch5 5.2.6 not executed, Step 6 creates placeholder comparison with "pending" status.

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

#### Step 1: Fit Domain-Stratified LMMs with Random Slopes

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.fit_lmm_trajectory_tsvr)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_lmm_convergence + validate_variance_positivity)

**What Validation Checks:**
- All 3 domain LMMs converged successfully
- Variance components all non-negative (var_intercept >= 0, var_slope >= 0, var_residual > 0)
- No singular convergence warnings
- Output files exist with expected format

**Expected Behavior on Validation Failure:**
- Raise error with specific domain that failed (e.g., "When domain LMM did not converge")
- Log failure to logs/step01_fit_domain_lmms.log
- Quit script immediately
- g_debug invoked to diagnose

---

#### Step 2: Extract Variance Components Per Domain

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.extract_random_effects_from_lmm)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure)

**What Validation Checks:**
- Output file exists (data/step02_variance_components.csv)
- Expected rows (3 domains)
- Expected columns (6: domain + 5 variance components)
- total_variance computed correctly (sum of var_intercept + var_slope + var_residual)
- No NaN values

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log to logs/step02_extract_variance_components.log
- Quit script immediately

---

#### Step 3: Compute ICC Per Domain

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.compute_icc_from_variance_components)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_icc_bounds)

**What Validation Checks:**
- Output file exists
- Expected rows (3)
- Expected columns (4)
- ICC values in [0, 1] (or flag if ICC_slope_conditional > 1.0)
- No negative ICC values (computation error)
- No NaN values

**Expected Behavior on Validation Failure:**
- Raise error if ICC < 0
- Log warning if ICC_slope_conditional > 1.0 (unusual but possible)
- Quit script if critical error

---

#### Step 4: Extract Random Effects Per Domain

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.extract_random_effects_from_lmm)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure)

**What Validation Checks:**
- Output file exists
- Expected rows (300: 100 participants x 3 domains)
- Expected columns (4)
- All participants present for all domains (complete factorial)
- No NaN values
- No duplicate UID x domain combinations

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log to logs/step04_extract_random_effects.log
- Quit script immediately

---

#### Step 5: Compare ICC_slope Across Domains

**Analysis Tool:** (determined by rq_tools - likely custom comparison function)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure)

**What Validation Checks:**
- Output files exist (comparison + pairwise differences)
- Expected rows (3 for comparison, 3 for pairwise)
- All domains present
- Rank values in {1, 2, 3} (no duplicates)
- No NaN values

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log to logs/step05_compare_icc_across_domains.log
- Quit script immediately

---

#### Step 6: Compare to Ch5 5.2.6

**Analysis Tool:** (determined by rq_tools - likely custom comparison function)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure)

**What Validation Checks:**
- Output file exists
- Expected rows (3)
- Expected columns (5)
- All domains present
- ICC values in expected ranges
- If Ch5 5.2.6 missing: placeholder with "pending" status

**Expected Behavior on Validation Failure:**
- If Ch5 5.2.6 missing: Log warning, create placeholder, proceed
- If other validation failure: Raise error, log to logs/step06_compare_to_ch5.log, quit script

---

## Summary

**Total Steps:** 6

**Estimated Runtime:** Medium (30-45 minutes total)
  - Step 1: High (15-20 min - 3 LMMs with random slopes)
  - Steps 2-6: Low (<1 min each - data extraction and computation)

**Cross-RQ Dependencies:**
  - Required: RQ 6.3.1 (theta_confidence_domain.csv)
  - Optional: Ch5 5.2.6 (accuracy ICC for comparison)

**Primary Outputs:**
  - data/step01_variance_components_by_domain.csv (variance decomposition per domain)
  - data/step03_icc_estimates.csv (ICC_intercept, ICC_slope_simple, ICC_slope_conditional per domain)
  - data/step04_random_effects.csv (participant random effects per domain)
  - data/step05_domain_icc_comparison.csv (domain ranking by trait variance)
  - data/step06_ch5_comparison.csv (confidence vs accuracy ICC comparison)

**Validation Coverage:** 100% (all 6 steps have validation requirements)

**Key Hypotheses Tested:**
1. Do some domains show higher ICC_slope than others? (domain-specific trait variance)
2. Does 5-level confidence data reveal trait variance that dichotomous accuracy data missed?
3. If ICC_slope > 0.10 for any domain: Evidence of trait-like confidence decline (individual differences)
4. If all ICC_slope approximately 0: Parallel Ch5 5.2.6 pattern (no trait variance detected)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent for RQ 6.3.4
