# Analysis Plan: RQ 5.2.6 - Domain-Specific Variance Decomposition

**Research Question:** 5.2.6
**Created:** 2025-12-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines variance decomposition in forgetting trajectories across three episodic memory domains (What, Where, When). The analysis uses DERIVED data from RQ 5.2.1 (theta scores already calibrated, purified, and merged with TSVR). The focus is on quantifying between-person versus within-person variance in forgetting rate (random slopes) to determine whether forgetting is a stable individual difference (trait-like) or primarily measurement noise.

The analysis fits three domain-stratified Linear Mixed Models (separate LMM per domain) with random intercepts and slopes, extracts variance components and computes Intraclass Correlation Coefficients (ICC) for interpretation. Random effects from all three domains are exported for downstream clustering analysis (RQ 5.2.7 dependency). Intercept-slope correlations are tested using dual p-value reporting per Decision D068.

**Pipeline:** LMM-only (no IRT - uses theta from RQ 5.2.1)
**Steps:** 7 analysis steps (no Step 0 - data extraction not needed)
**Estimated Runtime:** Medium (30-60 minutes total - LMM fitting with random slopes can be computationally intensive)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni) for intercept-slope correlation tests
- Decision D070: TSVR_hours time variable (inherited from RQ 5.2.1 - already in input data)

**Critical Outputs:**
- 300 random effects (100 participants x 3 domains) required for RQ 5.2.7 clustering
- Domain-specific ICC estimates for characterizing trait-like versus state-like variance
- Intercept-slope correlations testing whether high performers maintain advantage over time

---

## Analysis Plan

This RQ requires 7 steps:

### Step 1: Fit Domain-Stratified LMMs with Random Slopes

**Dependencies:** None (first step - uses DERIVED data from RQ 5.2.1)
**Complexity:** High (30-40 minutes - 3 LMMs with random slopes, convergence may require multiple attempts)

**Purpose:** Fit three separate Linear Mixed Models (one per domain: What, Where, When) to allow domain-specific variance component estimation. Random slopes model enables individual-specific forgetting rates.

**Input:**

**File:** results/ch5/5.2.1/data/step04_lmm_input.csv
**Source:** RQ 5.2.1 Step 4 output (theta scores merged with TSVR, reshaped to long format)
**Format:** CSV, long format (one row per observation)
**Columns:**
  - `composite_ID` (string, format: UID_test, e.g., "P001_T1")
  - `UID` (string, participant identifier, e.g., "P001")
  - `test` (string, test session identifier: T1, T2, T3, T4 for Days 0, 1, 3, 6)
  - `TSVR_hours` (float, actual hours since encoding - Decision D070 time variable)
  - `domain` (string, memory domain factor: "What", "Where", "When")
  - `theta` (float, IRT ability estimate from domain-specific calibration)
  - `se` (float, standard error of theta estimate)

**Expected Rows:** 1200 (100 participants x 4 tests x 3 domains)
**Expected Values:**
  - TSVR_hours range: [0, 168] hours (0=encoding, 168=1 week)
  - theta range: [-3, 3] typical IRT scale
  - se range: [0.1, 1.0] typical standard errors
  - domain values: exactly {"What", "Where", "When"}

**Processing:**

**Model Specification:**
For each domain (What, Where, When) separately:
  - Formula: `theta ~ TSVR_hours + (TSVR_hours | UID)`
  - Random effects: Random intercept AND random slope (allows individual-specific forgetting rates)
  - Estimation: REML=False (consistent with RQ 5.2.1, enables model comparison via AIC if needed)
  - Time variable: TSVR_hours (actual hours per Decision D070, NOT nominal days 0/1/3/6)

**Convergence Strategy:**
Per 1_concept.md validation section, if model fails to converge:
  1. Try alternative optimizers (bobyqa, nlminb)
  2. Use likelihood ratio test (LRT) to compare random slopes vs intercept-only
  3. If LRT p < 0.05, retain slopes with simplified correlation structure (uncorrelated random effects)
  4. If LRT p >= 0.05, use random intercepts-only model for that domain
  5. Document which structure achieved per domain in model metadata

Reference: Bates et al. (2015) parsimonious mixed models guidelines per 1_concept.md.

**Output:**

**File 1:** data/step01_model_metadata_what.yaml
**Format:** YAML with model convergence and structure information
**Contents:**
  - `converged` (bool): True/False convergence status
  - `random_structure` (string): "Full" (intercept+slope correlated), "Uncorrelated" (intercept+slope independent), or "Intercept-only"
  - `optimizer` (string): Which optimizer succeeded (lbfgs, bobyqa, nlminb)
  - `log_likelihood` (float): Final log-likelihood value
  - `aic` (float): Akaike Information Criterion
  - `bic` (float): Bayesian Information Criterion
  - `n_obs` (int): 400 (100 participants x 4 tests for What domain)
  - `n_groups` (int): 100 (number of participants)

**File 2:** data/step01_model_metadata_where.yaml
**Format:** Same as File 1 (Where domain)

**File 3:** data/step01_model_metadata_when.yaml
**Format:** Same as File 1 (When domain)

**File 4:** data/step01_fitted_models.pkl
**Format:** Pickle file containing 3 fitted statsmodels MixedLM objects
**Contents:** Dictionary with keys {"What": model_what, "Where": model_where, "When": model_when}
**Purpose:** Preserve fitted models for downstream steps (variance extraction, random effects extraction)

**Validation Requirement:**

Validation tools MUST be used after LMM fitting tool execution. Specific validation tools will be determined by rq_tools based on LMM convergence and assumption checks. The rq_analysis agent will embed validation tool calls after the analysis tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_model_metadata_what.yaml exists (exact path)
- data/step01_model_metadata_where.yaml exists (exact path)
- data/step01_model_metadata_when.yaml exists (exact path)
- data/step01_fitted_models.pkl exists (exact path)
- All 4 files non-empty (>100 bytes for YAML, >1KB for pickle)

*Value Ranges:*
- converged: True for all 3 domains (if False, trigger STEP ERROR)
- log_likelihood: negative value (log of probability in [0,1])
- aic, bic: positive values, typically 1000-5000 range for N=400 observations
- n_obs: exactly 400 for What/Where/When (100 participants x 4 tests)
- n_groups: exactly 100 (number of unique UIDs)

*Data Quality:*
- All 3 domain models must converge (converged=True in all YAML files)
- Random structure documented (Full/Uncorrelated/Intercept-only) per domain
- If any domain fails convergence after all remedies attempted, QUIT with error (cannot proceed to variance decomposition without fitted models)

*Log Validation:*
- Required pattern: "Model converged: True" for each domain (What, Where, When)
- Required pattern: "Random structure: [Full|Uncorrelated|Intercept-only]" for each domain
- Required pattern: "Writing data/step01_model_metadata_<domain>.yaml"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "Maximum iterations reached without convergence"
- Acceptable warnings: "Covariance matrix singular" (if LRT test leads to simplified structure), "Optimizer switched to [bobyqa|nlminb]" (contingency plan executed)

**Expected Behavior on Validation Failure:**
- If any domain fails to converge after all contingency plans: Raise error with specific domain name
- Log failure to logs/step01_fit_domain_lmms.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose root cause (common causes: insufficient within-person variance, data scaling issues, optimizer sensitivity)

---

### Step 2: Extract Variance Components per Domain

**Dependencies:** Step 1 (requires fitted LMM models)
**Complexity:** Low (5-10 minutes - extracting variance components from fitted models)

**Purpose:** Extract variance components (var_intercept, var_slope, cov_int_slope, var_residual) from each of the three domain-stratified LMMs for ICC computation and interpretation.

**Input:**

**File 1:** data/step01_fitted_models.pkl
**Source:** Step 1 output (3 fitted MixedLM objects)
**Format:** Pickle file with dictionary {"What": model, "Where": model, "When": model}

**File 2-4:** data/step01_model_metadata_<domain>.yaml (all 3 domains)
**Source:** Step 1 output (convergence and structure metadata)
**Purpose:** Check which random structure was fit (Full/Uncorrelated/Intercept-only) to correctly extract variance components

**Processing:**

For each domain (What, Where, When):
  1. Load fitted model from pickle file
  2. Extract variance components from model.cov_re (random effects covariance matrix):
     - `var_intercept`: Between-person variance in baseline ability (diagonal element [0,0])
     - `var_slope`: Between-person variance in forgetting rate (diagonal element [1,1] if random slopes fit)
     - `cov_int_slope`: Intercept-slope covariance (off-diagonal element [0,1] if correlated structure)
  3. Extract residual variance from model.scale (within-person variance / measurement error)
  4. Handle simplified structures:
     - If Uncorrelated: cov_int_slope = 0 (by definition)
     - If Intercept-only: var_slope = NA, cov_int_slope = NA (no slopes estimated)

**Output:**

**File:** data/step02_variance_components.csv
**Format:** CSV with one row per variance component per domain
**Columns:**
  - `domain` (string): "What", "Where", "When"
  - `component` (string): "var_intercept", "var_slope", "cov_int_slope", "var_residual", "total_variance"
  - `value` (float): Variance/covariance estimate
  - `interpretation` (string): Plain-language description

**Expected Rows:** 15 (5 components x 3 domains)
**Component Definitions:**
  - var_intercept: Between-person variance in baseline theta (Day 0)
  - var_slope: Between-person variance in forgetting rate (theta change per hour)
  - cov_int_slope: Correlation between baseline and forgetting rate
  - var_residual: Within-person variance (measurement error + unexplained variation)
  - total_variance: var_intercept + var_slope + var_residual (for What/Where/When separately)

**Validation Requirement:**

Validation tools MUST be used after variance component extraction tool execution. Specific validation tools will be determined by rq_tools based on variance component properties (positivity, bounds).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_variance_components.csv exists (exact path)
- Expected rows: 15 (5 components x 3 domains)
- Expected columns: 4 (domain, component, value, interpretation)
- Data types: domain (string), component (string), value (float64), interpretation (string)

*Value Ranges:*
- var_intercept > 0 for all 3 domains (Heywood case if <=0)
- var_slope > 0 for all 3 domains (if random slopes fit; NA if Intercept-only)
- var_residual > 0 for all 3 domains (must be positive)
- cov_int_slope: unrestricted range (can be negative, zero, or positive)
- total_variance > 0 for all 3 domains (sum of components)

*Data Quality:*
- No NaN values in var_intercept or var_residual (QUIT if present - indicates model failure)
- var_slope may be NaN if Intercept-only structure fit (acceptable only if documented in step01 metadata)
- All 3 domains present (What, Where, When)
- All 5 components present per domain

*Log Validation:*
- Required pattern: "Extracted variance components for What domain: 5 components"
- Required pattern: "Extracted variance components for Where domain: 5 components"
- Required pattern: "Extracted variance components for When domain: 5 components"
- Required pattern: "Writing data/step02_variance_components.csv: 15 rows"
- Forbidden patterns: "ERROR", "Negative variance detected", "Heywood case"
- Acceptable warnings: "var_slope = NA for [domain] (Intercept-only structure)" (if LRT test failed in Step 1)

**Expected Behavior on Validation Failure:**
- If any variance component <=0 (except cov_int_slope): Raise error "Heywood case detected in [domain]"
- Log failure to logs/step02_extract_variance_components.log
- Quit script immediately
- g_debug invoked (common causes: model not converged, insufficient data, collinearity)

---

### Step 3: Compute ICC Estimates per Domain

**Dependencies:** Step 2 (requires variance components)
**Complexity:** Low (5 minutes - computing ICC from variance components)

**Purpose:** Compute Intraclass Correlation Coefficients (ICC) for intercepts and slopes to quantify between-person versus within-person variance. ICC > 0.40 indicates substantial trait-like stability (primary hypothesis test).

**Input:**

**File:** data/step02_variance_components.csv
**Source:** Step 2 output (15 rows: 5 components x 3 domains)
**Format:** CSV with columns: domain, component, value, interpretation

**Processing:**

For each domain (What, Where, When):
  1. ICC_intercept = var_intercept / (var_intercept + var_residual)
     - Interpretation: Proportion of baseline theta variance due to stable individual differences
  2. ICC_slope_simple = var_slope / (var_slope + var_residual)
     - Interpretation: Proportion of forgetting rate variance due to stable individual differences (ignoring intercept-slope correlation)
  3. ICC_slope_conditional = ICC at Day 6 accounting for intercept-slope correlation
     - Formula: [var_intercept + 2*cov_int_slope*TSVR_D6 + var_slope*TSVR_D6^2] / [var_intercept + 2*cov_int_slope*TSVR_D6 + var_slope*TSVR_D6^2 + var_residual]
     - Where TSVR_D6 = 144 hours (6 days x 24 hours/day)
     - Interpretation: Proportion of theta variance at Day 6 due to stable individual differences (accounts for correlation)
  4. Characterize ICC magnitude using thresholds (per 1_concept.md):
     - ICC < 0.20 = "Low" (mostly measurement noise)
     - 0.20 <= ICC < 0.40 = "Moderate" (mixed trait and state variance)
     - ICC >= 0.40 = "Substantial" (trait-like individual differences dominate)

**ICC Threshold Justification (from 1_concept.md):**
Per Koo & Li (2016) reliability guidelines adapted for individual differences research:
  - ICC < 0.50 = Poor reliability
  - ICC 0.50-0.75 = Moderate reliability
  - ICC 0.75-0.90 = Good reliability
  - ICC > 0.90 = Excellent reliability

This RQ uses more lenient threshold (ICC > 0.40 = "substantial") per McGraw & Wong (1996) ICC(2,1) guidelines for single-measurement reliability, acknowledging forgetting rate reliability is typically lower than test-retest reliability.

**Output:**

**File:** data/step03_icc_estimates.csv
**Format:** CSV with one row per ICC type per domain
**Columns:**
  - `domain` (string): "What", "Where", "When"
  - `icc_type` (string): "intercept", "slope_simple", "slope_conditional"
  - `icc_value` (float): ICC estimate in [0, 1]
  - `interpretation` (string): "Low", "Moderate", or "Substantial" based on thresholds
  - `threshold_used` (string): "<0.20", "0.20-0.40", ">=0.40"

**Expected Rows:** 9 (3 ICC types x 3 domains)

**Validation Requirement:**

Validation tools MUST be used after ICC computation tool execution. Specific validation tools will be determined by rq_tools based on ICC range validation (must be in [0,1]).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_icc_estimates.csv exists (exact path)
- Expected rows: 9 (3 ICC types x 3 domains)
- Expected columns: 5 (domain, icc_type, icc_value, interpretation, threshold_used)
- Data types: domain (string), icc_type (string), icc_value (float64), interpretation (string), threshold_used (string)

*Value Ranges:*
- icc_value in [0, 1] for all 9 rows (probability constraint - values outside indicate computation error)
- icc_value not NaN (QUIT if NaN - indicates missing variance components or division by zero)

*Data Quality:*
- All 3 domains present (What, Where, When)
- All 3 ICC types present per domain (intercept, slope_simple, slope_conditional)
- interpretation values exactly {"Low", "Moderate", "Substantial"} (case-sensitive)
- threshold_used values exactly {"<0.20", "0.20-0.40", ">=0.40"} (case-sensitive)

*Log Validation:*
- Required pattern: "Computed ICC estimates for What domain: 3 types"
- Required pattern: "Computed ICC estimates for Where domain: 3 types"
- Required pattern: "Computed ICC estimates for When domain: 3 types"
- Required pattern: "Writing data/step03_icc_estimates.csv: 9 rows"
- Forbidden patterns: "ERROR", "ICC out of bounds", "Division by zero"
- Acceptable warnings: None expected for ICC computation

**Expected Behavior on Validation Failure:**
- If any ICC outside [0,1]: Raise error "ICC computation error: value [X] outside valid range [0,1]"
- Log failure to logs/step03_compute_icc_estimates.log
- Quit script immediately
- g_debug invoked (common causes: negative variance components from Step 2, formula error)

---

### Step 4: Extract Individual Random Effects per Domain

**Dependencies:** Step 1 (requires fitted models)
**Complexity:** Low (5-10 minutes - extracting random effects from fitted models)

**Purpose:** Extract individual-specific random intercepts and slopes for all 100 participants across all 3 domains. Output required for RQ 5.2.7 (domain-based clustering using random effect profiles).

**Input:**

**File 1:** data/step01_fitted_models.pkl
**Source:** Step 1 output (3 fitted MixedLM objects)
**Format:** Pickle file with dictionary {"What": model, "Where": model, "When": model}

**File 2-4:** data/step01_model_metadata_<domain>.yaml (all 3 domains)
**Source:** Step 1 output (convergence and structure metadata)
**Purpose:** Check which random structure was fit (Full/Uncorrelated/Intercept-only)

**Processing:**

For each domain (What, Where, When):
  1. Load fitted model from pickle file
  2. Extract random effects from model.random_effects attribute:
     - Dictionary with keys = UID (participant identifiers)
     - Values = random effect estimates (2D if intercept+slope, 1D if intercept-only)
  3. For each participant:
     - `Total_Intercept`: Random intercept estimate (deviation from population mean baseline theta)
     - `Total_Slope`: Random slope estimate (deviation from population mean forgetting rate) if random slopes fit
  4. Combine across domains into single DataFrame with 300 rows (100 UID x 3 domains)

**Output:**

**File:** data/step04_random_effects.csv
**Format:** CSV with one row per participant per domain
**Columns:**
  - `UID` (string): Participant identifier (e.g., "P001")
  - `domain` (string): "What", "Where", "When"
  - `Total_Intercept` (float): Random intercept estimate for this participant in this domain
  - `Total_Slope` (float): Random slope estimate for this participant in this domain (NA if Intercept-only)
  - `intercept_se` (float): Standard error of random intercept
  - `slope_se` (float): Standard error of random slope (NA if Intercept-only)

**Expected Rows:** 300 (100 participants x 3 domains)

**CRITICAL NOTE:** This file is a REQUIRED INPUT for RQ 5.2.7 (domain-based clustering). RQ 5.2.7 cannot proceed without all 300 random effects present.

**Validation Requirement:**

Validation tools MUST be used after random effects extraction tool execution. Specific validation tools will be determined by rq_tools based on random effects structure validation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_random_effects.csv exists (exact path)
- Expected rows: 300 (100 participants x 3 domains)
- Expected columns: 6 (UID, domain, Total_Intercept, Total_Slope, intercept_se, slope_se)
- Data types: UID (string), domain (string), Total_Intercept (float64), Total_Slope (float64), intercept_se (float64), slope_se (float64)

*Value Ranges:*
- Total_Intercept: unrestricted range (can be negative, zero, or positive - represents deviation from mean)
- Total_Slope: unrestricted range if random slopes fit; NA if Intercept-only structure
- intercept_se > 0 for all 300 rows (standard errors must be positive)
- slope_se > 0 if random slopes fit; NA if Intercept-only structure
- UID values: exactly 100 unique (all participants present)
- domain values: exactly {"What", "Where", "When"} (all domains present)

*Data Quality:*
- All 100 participants present (no missing UIDs)
- All 3 domains present for each participant (complete data for clustering)
- No NaN in Total_Intercept column (QUIT if present - indicates extraction failure)
- Total_Slope may be NaN if Intercept-only structure fit for that domain (acceptable only if documented in step01 metadata)

*Log Validation:*
- Required pattern: "Extracted random effects for 100 participants x 3 domains = 300 rows"
- Required pattern: "All participants present: 100 unique UIDs"
- Required pattern: "All domains present: What, Where, When"
- Required pattern: "Writing data/step04_random_effects.csv: 300 rows"
- Forbidden patterns: "ERROR", "Missing participants", "Incomplete domain coverage"
- Acceptable warnings: "Total_Slope = NA for [domain] (Intercept-only structure)" (if LRT test failed in Step 1)

**Expected Behavior on Validation Failure:**
- If <300 rows: Raise error "Incomplete random effects: expected 300 rows (100 UID x 3 domains), found [N]"
- If missing participants: Raise error "Missing UIDs: [list of missing]"
- If missing domains: Raise error "Incomplete domain coverage: [domain] missing for [N] participants"
- Log failure to logs/step04_extract_random_effects.log
- Quit script immediately
- g_debug invoked (common causes: model object corrupted, extraction logic error, incomplete fits)

**Downstream Dependency Check:**
RQ 5.2.7 expects this exact file path: results/ch5/5.2.6/data/step04_random_effects.csv with 300 rows. If this file is incomplete or missing, RQ 5.2.7 will trigger EXPECTATIONS ERROR.

---

### Step 5: Test Intercept-Slope Correlations per Domain

**Dependencies:** Step 4 (requires random effects)
**Complexity:** Low (5 minutes - Pearson correlation tests)

**Purpose:** Test whether baseline ability (intercept) is correlated with forgetting rate (slope) within each domain. Negative correlation indicates high performers maintain advantage over time (Fan Effect). Report dual p-values per Decision D068.

**Input:**

**File:** data/step04_random_effects.csv
**Source:** Step 4 output (300 rows: 100 UID x 3 domains)
**Format:** CSV with columns: UID, domain, Total_Intercept, Total_Slope, intercept_se, slope_se

**Processing:**

For each domain (What, Where, When):
  1. Filter data to domain subset (100 participants)
  2. Compute Pearson correlation between Total_Intercept and Total_Slope
  3. Test significance with two-tailed test
  4. Report DUAL p-values per Decision D068:
     - `p_uncorrected`: Raw p-value from correlation test
     - `p_bonferroni`: Bonferroni-corrected p-value (alpha = 0.01 / 3 domains = 0.0033)
  5. Characterize correlation:
     - Negative correlation: High performers maintain advantage (baseline predicts persistence)
     - Positive correlation: High performers decline faster (regression to mean)
     - Near-zero correlation: Baseline and forgetting rate independent

**Bonferroni Correction Rationale:**
Testing 3 correlations (one per domain) at family-wise alpha = 0.01 requires Bonferroni correction: alpha_per_test = 0.01 / 3 = 0.0033. This controls Type I error rate across multiple tests.

**Output:**

**File:** data/step05_intercept_slope_correlations.csv
**Format:** CSV with one row per domain
**Columns:**
  - `domain` (string): "What", "Where", "When"
  - `r` (float): Pearson correlation coefficient in [-1, 1]
  - `p_uncorrected` (float): Raw p-value from correlation test in [0, 1]
  - `p_bonferroni` (float): Bonferroni-corrected p-value = p_uncorrected * 3 (capped at 1.0)
  - `n` (int): Sample size (100 participants per domain)
  - `interpretation` (string): "Negative correlation: high performers maintain advantage" OR "Positive correlation: high performers decline faster" OR "No significant correlation"

**Expected Rows:** 3 (one per domain)

**Validation Requirement:**

Validation tools MUST be used after correlation test tool execution. Specific validation tools will be determined by rq_tools based on Decision D068 dual p-value validation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_intercept_slope_correlations.csv exists (exact path)
- Expected rows: 3 (one per domain)
- Expected columns: 6 (domain, r, p_uncorrected, p_bonferroni, n, interpretation)
- Data types: domain (string), r (float64), p_uncorrected (float64), p_bonferroni (float64), n (int64), interpretation (string)

*Value Ranges:*
- r in [-1, 1] (correlation coefficient bounds)
- p_uncorrected in [0, 1] (probability bounds)
- p_bonferroni in [0, 1] (capped at 1.0 even if p_uncorrected * 3 > 1.0)
- n = 100 for all 3 domains (sample size)

*Data Quality:*
- All 3 domains present (What, Where, When)
- BOTH p_uncorrected AND p_bonferroni present (Decision D068 requirement - dual p-value reporting mandatory)
- No NaN in any column (complete correlation tests)

*Log Validation:*
- Required pattern: "Testing intercept-slope correlation for What domain: r=[value], p_uncorrected=[value], p_bonferroni=[value]"
- Required pattern: "Testing intercept-slope correlation for Where domain: r=[value], p_uncorrected=[value], p_bonferroni=[value]"
- Required pattern: "Testing intercept-slope correlation for When domain: r=[value], p_uncorrected=[value], p_bonferroni=[value]"
- Required pattern: "Decision D068: Dual p-values reported (uncorrected + Bonferroni)"
- Required pattern: "Writing data/step05_intercept_slope_correlations.csv: 3 rows"
- Forbidden patterns: "ERROR", "Missing p-value column", "Single p-value only"
- Acceptable warnings: None expected for correlation tests

**Expected Behavior on Validation Failure:**
- If p_bonferroni column missing: Raise error "Decision D068 violation: p_bonferroni column missing (dual p-value reporting required)"
- If any value outside valid range: Raise error "Correlation test error: [variable] = [value] outside valid range"
- Log failure to logs/step05_test_intercept_slope_correlations.log
- Quit script immediately
- g_debug invoked (common causes: Decision D068 validation tool not called, computation error)

---

### Step 6: Compare ICC Across Domains

**Dependencies:** Step 3 (requires ICC estimates)
**Complexity:** Low (5 minutes - domain comparison and ranking)

**Purpose:** Rank domains by ICC_slope_conditional magnitude to characterize domain-specific variance patterns. Test secondary hypothesis: Where/When (hippocampal-dependent) may show higher ICC than What (perirhinal-dependent) if hippocampal aging effects vary more across individuals.

**Input:**

**File:** data/step03_icc_estimates.csv
**Source:** Step 3 output (9 rows: 3 ICC types x 3 domains)
**Format:** CSV with columns: domain, icc_type, icc_value, interpretation, threshold_used

**Processing:**

1. Filter to ICC_slope_conditional rows only (3 rows: one per domain)
2. Rank domains by icc_value (descending order: highest ICC first)
3. Characterize domain differences:
   - Identify which domain(s) achieve "Substantial" (>=0.40) threshold
   - Compare rank order to theoretical prediction: ICC_When >= ICC_Where > ICC_What
   - Compute ICC differences (pairwise: What-Where, What-When, Where-When)
4. Create summary table for interpretation:
   - Domain rank order
   - ICC magnitude interpretation per domain
   - Theoretical prediction match (yes/no)

**Output:**

**File:** data/step06_domain_icc_comparison.csv
**Format:** CSV with one row per domain
**Columns:**
  - `domain` (string): "What", "Where", "When"
  - `icc_slope_conditional` (float): ICC value from Step 3 in [0, 1]
  - `interpretation` (string): "Low", "Moderate", or "Substantial"
  - `rank` (int): 1 (highest ICC), 2 (middle), 3 (lowest ICC)
  - `meets_threshold` (bool): True if ICC >= 0.40, False otherwise (primary hypothesis test)
  - `theoretical_prediction` (string): "Matches" or "Deviates" (compared to ICC_When >= ICC_Where > ICC_What)

**Expected Rows:** 3 (one per domain, sorted by rank)

**Validation Requirement:**

Validation tools MUST be used after domain comparison tool execution. Specific validation tools will be determined by rq_tools based on comparison logic validation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_domain_icc_comparison.csv exists (exact path)
- Expected rows: 3 (one per domain)
- Expected columns: 6 (domain, icc_slope_conditional, interpretation, rank, meets_threshold, theoretical_prediction)
- Data types: domain (string), icc_slope_conditional (float64), interpretation (string), rank (int64), meets_threshold (bool), theoretical_prediction (string)

*Value Ranges:*
- icc_slope_conditional in [0, 1] (probability bounds)
- rank in {1, 2, 3} (exactly one domain per rank - no ties expected but handle if occur)
- interpretation in {"Low", "Moderate", "Substantial"} (case-sensitive)
- theoretical_prediction in {"Matches", "Deviates"} (case-sensitive)

*Data Quality:*
- All 3 domains present (What, Where, When)
- Ranks unique (1, 2, 3) unless ties occur
- At least one domain should meet threshold (meets_threshold=True) if primary hypothesis supported
- No NaN in any column

*Log Validation:*
- Required pattern: "Domain ICC ranking (descending): [domain1], [domain2], [domain3]"
- Required pattern: "Domains meeting threshold (ICC >= 0.40): [N] domains"
- Required pattern: "Theoretical prediction: [Matches|Deviates]"
- Required pattern: "Writing data/step06_domain_icc_comparison.csv: 3 rows"
- Forbidden patterns: "ERROR", "Ranking failure", "Duplicate ranks"
- Acceptable warnings: "Tie detected between [domain1] and [domain2] at rank [N]" (if ICC values identical)

**Expected Behavior on Validation Failure:**
- If any ICC outside [0,1]: Raise error "ICC value error: [domain] ICC=[value] outside [0,1]"
- If ranks not {1,2,3}: Raise error "Ranking error: expected ranks {1,2,3}, found {ranks}"
- Log failure to logs/step06_compare_domain_icc.log
- Quit script immediately
- g_debug invoked (common causes: Step 3 ICC computation error, ranking logic failure)

---

### Step 7: Prepare Domain ICC Barplot Data

**Dependencies:** Step 6 (requires domain comparison)
**Complexity:** Low (5 minutes - aggregating data for barplot)

**Purpose:** Prepare plot source CSV for visualizing ICC_slope_conditional across domains. This enables comparison of between-person variance proportions, illustrating which domains show trait-like forgetting versus state-like noise.

**Plot Description:** Grouped barplot comparing ICC_slope_conditional across three domains (What, Where, When) with threshold line at 0.40 (substantial reliability cutoff). Y-axis: ICC (0-1 scale), X-axis: Domain, colored bars indicate interpretation category (Low/Moderate/Substantial).

**Input:**

**File:** data/step06_domain_icc_comparison.csv
**Source:** Step 6 output (3 rows: one per domain with rank and interpretation)
**Format:** CSV with columns: domain, icc_slope_conditional, interpretation, rank, meets_threshold, theoretical_prediction

**Processing:**

1. Load domain ICC comparison data
2. Add plot-specific columns:
   - `plot_order` (int): X-axis position (1=What, 2=Where, 3=When for alphabetical consistency)
   - `color_category` (string): Bar color based on interpretation ("Low"=red, "Moderate"=yellow, "Substantial"=green)
   - `threshold_line` (float): Horizontal reference line at 0.40 (all rows)
3. Sort by plot_order for consistent visualization

**Output:**

**File:** data/step07_domain_icc_barplot_data.csv
**Format:** CSV, plot source data for domain ICC comparison barplot
**Columns:**
  - `domain` (string): "What", "Where", "When"
  - `icc_slope_conditional` (float): ICC value in [0, 1]
  - `interpretation` (string): "Low", "Moderate", "Substantial"
  - `plot_order` (int): 1 (What), 2 (Where), 3 (When)
  - `color_category` (string): Bar color mapping ("Low", "Moderate", "Substantial")
  - `threshold_line` (float): 0.40 for all rows (horizontal reference line)

**Expected Rows:** 3 (one per domain)

**Note:** This CSV is plot source data created during analysis (by g_code). The actual PNG barplot will be generated later by rq_plots agent and saved to plots/ folder.

**Validation Requirement:**

Validation tools MUST be used after plot data preparation tool execution. Specific validation tools will be determined by rq_tools based on plot data format validation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_domain_icc_barplot_data.csv exists (exact path)
- Expected rows: 3 (one per domain)
- Expected columns: 6 (domain, icc_slope_conditional, interpretation, plot_order, color_category, threshold_line)
- Data types: domain (string), icc_slope_conditional (float64), interpretation (string), plot_order (int64), color_category (string), threshold_line (float64)

*Value Ranges:*
- icc_slope_conditional in [0, 1] (probability bounds)
- plot_order in {1, 2, 3} (exactly one domain per position)
- threshold_line = 0.40 for all 3 rows (constant reference line)
- color_category in {"Low", "Moderate", "Substantial"} (case-sensitive, matches interpretation)

*Data Quality:*
- All 3 domains present (What, Where, When)
- No NaN values (all cells must have valid values)
- No duplicate plot_order values (unique positions)
- color_category matches interpretation (Low=red, Moderate=yellow, Substantial=green mapping preserved)

*Log Validation:*
- Required pattern: "Plot data preparation complete: 3 rows created"
- Required pattern: "All domains represented: What, Where, When"
- Required pattern: "Threshold line set at 0.40 for all rows"
- Required pattern: "Writing data/step07_domain_icc_barplot_data.csv: 3 rows"
- Forbidden patterns: "ERROR", "Missing domain", "Duplicate plot_order"
- Acceptable warnings: None expected for plot data preparation

**Expected Behavior on Validation Failure:**
- If <3 rows: Raise error "Incomplete plot data: expected 3 rows (What, Where, When), found [N]"
- If any value outside valid range: Raise error "Plot data error: [column] = [value] outside valid range"
- Log failure to logs/step07_prepare_domain_icc_barplot_data.log
- Quit script immediately
- g_debug invoked (common causes: Step 6 data incomplete, column mapping error)

**Plotting Function (rq_plots will call later):** Grouped barplot with threshold reference line
- rq_plots agent maps this description to tools/plots.py function (likely plot_histogram_by_group or custom barplot)
- Plot reads data/step07_domain_icc_barplot_data.csv (created by this step)
- No data aggregation in rq_plots (visualization only per Option B architecture)
- PNG output saved to plots/ folder by rq_plots

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs - intermediate and final)

**Input (from RQ 5.2.1):**
- results/ch5/5.2.1/data/step04_lmm_input.csv (DERIVED data source: 1200 rows)

**Step 1 Outputs:**
- data/step01_model_metadata_what.yaml (What domain LMM metadata)
- data/step01_model_metadata_where.yaml (Where domain LMM metadata)
- data/step01_model_metadata_when.yaml (When domain LMM metadata)
- data/step01_fitted_models.pkl (3 fitted MixedLM objects)

**Step 2 Outputs:**
- data/step02_variance_components.csv (15 rows: 5 components x 3 domains)

**Step 3 Outputs:**
- data/step03_icc_estimates.csv (9 rows: 3 ICC types x 3 domains)

**Step 4 Outputs:**
- data/step04_random_effects.csv (300 rows: 100 UID x 3 domains) [REQUIRED for RQ 5.2.7]

**Step 5 Outputs:**
- data/step05_intercept_slope_correlations.csv (3 rows: one per domain, dual p-values)

**Step 6 Outputs:**
- data/step06_domain_icc_comparison.csv (3 rows: domain rankings and interpretations)

**Step 7 Outputs:**
- data/step07_domain_icc_barplot_data.csv (3 rows: plot source CSV)

### Logs (ONLY execution logs - .log files capturing stdout/stderr)

- logs/step01_fit_domain_lmms.log
- logs/step02_extract_variance_components.log
- logs/step03_compute_icc_estimates.log
- logs/step04_extract_random_effects.log
- logs/step05_test_intercept_slope_correlations.log
- logs/step06_compare_domain_icc.log
- logs/step07_prepare_domain_icc_barplot_data.log

### Plots (EMPTY until rq_plots runs)

- plots/domain_icc_barplot.png (created by rq_plots, NOT by analysis steps)

### Results (EMPTY until rq_results runs)

- results/summary.md (created by rq_results, NOT by analysis steps)

---

## Expected Data Formats

### Step-to-Step Transformations

**No transformations needed** - Data already in long format from RQ 5.2.1 (step04_lmm_input.csv). Analysis consists of:
1. Subsetting by domain (What/Where/When)
2. Fitting LMMs to each subset
3. Extracting variance components and random effects
4. Computing ICC from variance components
5. Testing correlations and comparing domains

All outputs are tabular summaries (CSV) or model objects (pickle), no reshaping required.

### Column Naming Conventions

Per names.md conventions established in RQ 5.1:

**Inherited from RQ 5.2.1 input:**
- `composite_ID` (string): Participant-test combination (format: UID_test)
- `UID` (string): Participant identifier (format: P### with leading zeros)
- `test` (string): Test session identifier (T1, T2, T3, T4)
- `TSVR_hours` (float): Time Since VR in hours (Decision D070 time variable)
- `domain` (string): Memory domain factor ("What", "Where", "When")
- `theta` (float): IRT ability estimate from RQ 5.2.1
- `se` (float): Standard error of theta estimate

**New for RQ 5.2.6:**
- `Total_Intercept` (float): Random intercept estimate (deviation from population mean baseline)
- `Total_Slope` (float): Random slope estimate (deviation from population mean forgetting rate)
- `intercept_se` (float): Standard error of random intercept
- `slope_se` (float): Standard error of random slope
- `r` (float): Pearson correlation coefficient
- `p_uncorrected` (float): Raw p-value (Decision D068)
- `p_bonferroni` (float): Bonferroni-corrected p-value (Decision D068)

### Data Type Constraints

**Variance Components:**
- var_intercept, var_slope, var_residual: MUST be > 0 (Heywood case if <=0)
- cov_int_slope: unrestricted (can be negative, zero, positive)
- total_variance: MUST be > 0 (sum of components)

**ICC Estimates:**
- icc_value: MUST be in [0, 1] (probability constraint)
- interpretation: MUST be in {"Low", "Moderate", "Substantial"} (controlled vocabulary)

**Random Effects:**
- Total_Intercept, Total_Slope: unrestricted range (deviations can be negative/positive)
- intercept_se, slope_se: MUST be > 0 (standard errors always positive)

**Correlations:**
- r: MUST be in [-1, 1] (correlation coefficient bounds)
- p_uncorrected, p_bonferroni: MUST be in [0, 1] (probability bounds)

---

## Cross-RQ Dependencies

### Dependency Type: DERIVED Data from Other RQ (Dependencies Exist)

**This RQ requires outputs from:**

**RQ 5.2.1 (Domain-Specific Trajectories):**
- File: results/ch5/5.2.1/data/step04_lmm_input.csv
- Used in: All steps (primary data source)
- Rationale: RQ 5.2.1 performs IRT calibration with 3-factor What/Where/When model, item purification, theta score extraction, and merges with TSVR time variable. This RQ uses those theta scores to fit domain-stratified LMMs for variance decomposition.

**Execution Order Constraint:**
1. RQ 5.2.1 must complete Steps 1-4 first (IRT calibration -> purification -> theta extraction -> TSVR merge -> reshape to long)
2. This RQ executes second (fits domain-stratified LMMs to RQ 5.2.1 theta scores)
3. RQ 5.2.7 executes third (uses this RQ's step04_random_effects.csv for clustering)

**Data Source Boundaries:**
- **RAW data:** None (this RQ uses only DERIVED data from RQ 5.2.1)
- **DERIVED data:** results/ch5/5.2.1/data/step04_lmm_input.csv (1200 rows: theta scores in long format)
- **Scope:** This RQ does NOT re-run IRT calibration (reuses RQ 5.2.1 theta scores). It fits NEW domain-stratified LMMs (separate model per domain) to isolate domain-specific variance components.

**Validation:**
- Step 1: Check results/ch5/5.2.1/data/step04_lmm_input.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 1: Verify 1200 rows present (100 participants x 4 tests x 3 domains)
- If file missing OR incomplete rows -> quit with error -> user must execute RQ 5.2.1 first

**Downstream Dependency:**

**RQ 5.2.7 (Domain-Based Clustering) requires outputs from this RQ:**
- File: results/ch5/5.2.6/data/step04_random_effects.csv
- Rationale: RQ 5.2.7 clusters participants based on domain-specific random effect profiles (Total_Intercept and Total_Slope per domain). Requires all 300 rows (100 participants x 3 domains).

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

#### Step 1: Fit Domain-Stratified LMMs with Random Slopes

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.fit_lmm_trajectory_tsvr called 3 times, once per domain)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_lmm_convergence + tools.validation.validate_lmm_assumptions_comprehensive)

**What Validation Checks:**
- All 3 models converged (converged=True in YAML metadata)
- Random structure documented (Full/Uncorrelated/Intercept-only) per domain
- Log-likelihood, AIC, BIC in valid ranges (negative log-likelihood, positive AIC/BIC)
- n_obs = 400 per domain (100 participants x 4 tests)
- n_groups = 100 per domain (all participants present)
- LMM assumptions: residual normality (Q-Q plot, Shapiro-Wilk), homoscedasticity (Levene's test), no autocorrelation (ACF plot), linearity (residuals vs TSVR_hours)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Where domain model failed to converge after all remedies")
- Log failure to logs/step01_fit_domain_lmms.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose (common causes: insufficient within-person variance, optimizer sensitivity)

---

#### Step 2: Extract Variance Components per Domain

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.extract_random_effects_from_lmm called 3 times)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_variance_positivity)

**What Validation Checks:**
- All variance components > 0 (Heywood case if <=0 for var_intercept, var_slope, var_residual)
- 15 rows total (5 components x 3 domains)
- All domains present (What, Where, When)
- No NaN in var_intercept or var_residual (critical components)

**Expected Behavior on Validation Failure:**
- Raise error "Heywood case detected in [domain]: [component] <= 0"
- Log failure to logs/step02_extract_variance_components.log
- Quit script immediately
- g_debug invoked (common causes: model not converged, collinearity)

---

#### Step 3: Compute ICC Estimates per Domain

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.compute_icc_from_variance_components)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_icc_bounds)

**What Validation Checks:**
- ICC values in [0, 1] for all 9 rows (probability constraint)
- No NaN values (complete ICC computation)
- 9 rows total (3 ICC types x 3 domains)
- interpretation values in {"Low", "Moderate", "Substantial"}

**Expected Behavior on Validation Failure:**
- Raise error "ICC computation error: [domain] [icc_type] = [value] outside [0,1]"
- Log failure to logs/step03_compute_icc_estimates.log
- Quit script immediately
- g_debug invoked (common causes: negative variance from Step 2, formula error)

---

#### Step 4: Extract Individual Random Effects per Domain

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.extract_random_effects_from_lmm called 3 times, aggregated)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure)

**What Validation Checks:**
- 300 rows exactly (100 participants x 3 domains)
- All 100 participants present (no missing UIDs)
- All 3 domains present per participant (complete coverage)
- No NaN in Total_Intercept column (critical for clustering)
- intercept_se, slope_se > 0 (standard errors positive)

**Expected Behavior on Validation Failure:**
- Raise error "Incomplete random effects: expected 300 rows, found [N]"
- Log failure to logs/step04_extract_random_effects.log
- Quit script immediately
- g_debug invoked (common causes: model object corrupted, incomplete fits)

**CRITICAL:** This file is required input for RQ 5.2.7. Validation must ensure complete data (no missing participants, no missing domains).

---

#### Step 5: Test Intercept-Slope Correlations per Domain

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.test_intercept_slope_correlation_d068)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_correlation_test_d068)

**What Validation Checks:**
- BOTH p_uncorrected AND p_bonferroni columns present (Decision D068 dual p-value requirement)
- r in [-1, 1] (correlation coefficient bounds)
- p_uncorrected, p_bonferroni in [0, 1] (probability bounds)
- 3 rows total (one per domain)
- No NaN values (complete correlation tests)

**Expected Behavior on Validation Failure:**
- Raise error "Decision D068 violation: p_bonferroni column missing (dual p-value reporting required)"
- Log failure to logs/step05_test_intercept_slope_correlations.log
- Quit script immediately
- g_debug invoked (common causes: Decision D068 validation tool not called)

---

#### Step 6: Compare ICC Across Domains

**Analysis Tool:** (determined by rq_tools - custom ranking/comparison logic, likely pandas operations)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure)

**What Validation Checks:**
- 3 rows total (one per domain)
- Ranks unique {1, 2, 3} unless ties occur
- ICC values in [0, 1] (probability bounds)
- interpretation in {"Low", "Moderate", "Substantial"}
- theoretical_prediction in {"Matches", "Deviates"}

**Expected Behavior on Validation Failure:**
- Raise error "Ranking error: expected ranks {1,2,3}, found {ranks}"
- Log failure to logs/step06_compare_domain_icc.log
- Quit script immediately
- g_debug invoked (common causes: Step 3 ICC computation error, ranking logic failure)

---

#### Step 7: Prepare Domain ICC Barplot Data

**Analysis Tool:** (determined by rq_tools - custom plot data preparation, likely pandas operations)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_plot_data_completeness)

**What Validation Checks:**
- 3 rows total (one per domain)
- All domains present (What, Where, When)
- plot_order unique {1, 2, 3} (no duplicates)
- threshold_line = 0.40 for all rows (constant reference)
- color_category matches interpretation (Low/Moderate/Substantial)
- No NaN values (complete plot data)

**Expected Behavior on Validation Failure:**
- Raise error "Incomplete plot data: expected 3 rows, found [N]"
- Log failure to logs/step07_prepare_domain_icc_barplot_data.log
- Quit script immediately
- g_debug invoked (common causes: Step 6 data incomplete, column mapping error)

---

## Summary

**Total Steps:** 7 (no Step 0 - data extraction not needed, uses DERIVED data from RQ 5.2.1)
**Estimated Runtime:** Medium (30-60 minutes - LMM fitting with random slopes is computationally intensive, variance/ICC computation is fast)
**Cross-RQ Dependencies:** RQ 5.2.1 (upstream: provides theta scores), RQ 5.2.7 (downstream: requires random effects)
**Primary Outputs:**
  - 3 domain-stratified LMMs with variance components
  - 9 ICC estimates (3 types x 3 domains) for hypothesis testing
  - 300 random effects (REQUIRED for RQ 5.2.7 clustering)
  - 3 intercept-slope correlations with dual p-values (Decision D068)
  - Domain ICC comparison and barplot data
**Validation Coverage:** 100% (all 7 steps have validation requirements with 4-layer substance criteria)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-02): Initial plan created by rq_planner agent for RQ 5.2.6
