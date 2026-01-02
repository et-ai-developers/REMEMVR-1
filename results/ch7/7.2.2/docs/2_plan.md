# Analysis Plan: RQ 7.2.2 - Do cognitive tests attenuate age effects on REMEMVR?

**Research Question:** 7.2.2
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

**Purpose:** Quantify how cognitive tests (RAVLT, BVMT, RPM) attenuate the relationship between age and REMEMVR theta scores through attenuation analysis comparing bivariate vs. controlled age effects.

**Pipeline:** Attenuation Analysis with Bootstrap Confidence Intervals
**Steps:** 7 total analysis steps (Step 0: validation + Steps 1-6: analysis)
**Estimated Runtime:** 30-40 minutes (including 1000 bootstrap iterations)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Ch7 Bonferroni correction: alpha = 0.05/4 = 0.0125 (4 domains: overall, What, Where, When)
- Bootstrap resampling for non-normal attenuation distributions

**Theoretical Framework:** Tests VR scaffolding hypothesis - if environmental support reduces age differences, cognitive tests should substantially attenuate age effects on REMEMVR (>70% expected).

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required RQ 7.2.1 outputs and Ch5 domain theta scores exist before proceeding

**Input:**
- Primary: results/ch7/7.2.1/data/step04_bivariate_regression.csv (age coefficients Model 1)
- Alternative: results/ch7/7.2.1/data/step04_regression_results.csv
- Fallback: results/ch7/7.2.1/data/*regression*.{csv,txt}
- Primary: results/ch7/7.2.1/data/step05_hierarchical_regression.csv (age coefficients Model 2)
- Alternative: results/ch7/7.2.1/data/step05_model_comparison.csv
- Fallback: results/ch7/7.2.1/data/*hierarchical*.{csv,txt}
- Expected content: Age coefficients from bivariate and controlled models
- If not found: QUIT with "Ch7 7.2.1 regression outputs not found - prerequisite incomplete"

**Processing:**
- Check RQ 7.2.1 status.yaml shows rq_results = success
- Locate regression coefficient files using pattern matching
- Verify files contain age coefficients for both models
- Check Ch5 domain theta scores accessibility
- Log validation results with specific file paths found

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Contains: file paths found, status checks, content verification

*Value Ranges:*
- Status values: "success" or "failed" for each dependency
- File counts: >= 1 file found per dependency type
- Content flags: "coefficients_found" = True

*Data Quality:*
- All required file types located successfully
- Ch5 domain files accessible (4 files: overall, What, Where, When)
- RQ 7.2.1 coefficient files contain age terms

*Log Validation:*
- Required patterns: "Dependency validation complete", "All files located"
- Forbidden patterns: "ERROR", "File not found", "QUIT triggered"

**Expected Behavior on Validation Failure:**
- Raise error with specific missing dependency
- Log to logs/step00_dependency_validation.log
- Quit immediately, invoke g_debug

### Step 1: Load Age Coefficients from RQ 7.2.1
**Dependencies:** Step 0 (validated file paths)
**Complexity:** Low (<5 minutes)

**Purpose:** Extract age coefficients from bivariate and controlled regression models for attenuation calculation

**Input:**
- data/step00_dependency_validation.txt (validated file paths)
- Regression results from RQ 7.2.1 (paths from Step 0)
- Expected coefficients: beta_age_bivariate, beta_age_controlled, standard errors

**Processing:**
- Load bivariate age effect (Model 1: Age -> REMEMVR)
- Load controlled age effect (Model 2: Age + Cognitive Tests -> REMEMVR)
- Extract for all domains: overall theta, What theta, Where theta, When theta
- Verify coefficient availability for all 4 analyses
- Store in standardized format with domain labels
- Include standard errors and confidence intervals from original models

**Output:**
- data/step01_age_coefficients.csv

**Validation Requirement:**
Validation tools MUST be used after coefficient extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_age_coefficients.csv: 8 rows x 6 columns
- Columns: domain, model_type, beta_age, se_age, ci_lower, ci_upper
- Rows: 4 domains x 2 models (bivariate, controlled)

*Value Ranges:*
- beta_age in [-0.5, 0.1] (negative age effects expected)
- se_age in [0.001, 0.1] (positive standard errors)
- CI bounds: ci_lower < beta_age < ci_upper

*Data Quality:*
- All 8 coefficient pairs present (4 domains x 2 models)
- No missing values in critical columns
- Controlled effects smaller in magnitude than bivariate (attenuation expected)

*Log Validation:*
- Required patterns: "Coefficients extracted: 8 values", "All domains loaded"
- Forbidden patterns: "ERROR", "Missing coefficient", "NaN detected"

**Expected Behavior on Validation Failure:**
- Raise error with specific coefficient missing
- Log to logs/step01_load_coefficients.log
- Quit immediately, invoke g_debug

### Step 2: Compute Attenuation Ratios
**Dependencies:** Step 1 (age coefficients loaded)
**Complexity:** Low (<5 minutes)

**Purpose:** Calculate percentage attenuation using formula: (beta_bivariate - beta_controlled) / beta_bivariate * 100

**Input:**
- data/step01_age_coefficients.csv

**Processing:**
- For each domain, compute: attenuation_pct = ((beta_age_bivariate - beta_age_controlled) / beta_age_bivariate) * 100
- Handle division by zero: if beta_age_bivariate ≈ 0, set attenuation = NA
- Calculate absolute attenuation: abs(beta_age_bivariate - beta_age_controlled)
- Compute residual age effect: beta_age_controlled (remaining after control)
- Store point estimates for bootstrap input
- Include coefficient standard errors for uncertainty propagation

**Output:**
- data/step02_attenuation_ratios.csv

**Validation Requirement:**
Validation tools MUST be used after attenuation computation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_attenuation_ratios.csv: 4 rows x 8 columns
- Columns: domain, beta_bivariate, beta_controlled, attenuation_pct, absolute_attenuation, residual_effect, se_bivariate, se_controlled
- Rows: overall, What, Where, When

*Value Ranges:*
- attenuation_pct in [0, 100] (percentage scale)
- absolute_attenuation >= 0 (positive reduction)
- residual_effect in [-0.5, 0.1] (remaining age effect)

*Data Quality:*
- All 4 domains computed successfully
- No infinite or NaN values in attenuation_pct
- Logical consistency: larger attenuation -> smaller residual effect

*Log Validation:*
- Required patterns: "Attenuation computed: 4 domains", "Range validation passed"
- Forbidden patterns: "Division by zero", "Infinite value", "NaN result"

**Expected Behavior on Validation Failure:**
- Raise error with specific computation problem
- Log to logs/step02_compute_attenuation.log
- Quit immediately, invoke g_debug

### Step 3: Bootstrap Confidence Intervals
**Dependencies:** Step 2 (attenuation point estimates)
**Complexity:** High (~15 minutes with 1000 iterations)

**Purpose:** Generate 95% confidence intervals for attenuation ratios using bootstrap resampling

**Input:**
- data/step02_attenuation_ratios.csv
- Original regression data from RQ 7.2.1 (participant-level for resampling)

**Processing:**
- Implement participant-level block bootstrap (preserves within-participant correlation)
- Iterations: 1000
- Random seed: 42 for reproducibility
- For each iteration:
  - Resample participants WITH replacement (N=100)
  - Keep all observations for selected participants
  - Re-fit both models (bivariate, controlled)
  - Compute attenuation ratio for each domain
- CI computation: percentile method (2.5th, 97.5th percentiles)
- Test significance: CI excludes 0 indicates significant attenuation
- Stability check: CI width < 40% of point estimate (flag if unstable)
- Store bootstrap distribution for domain comparisons

**Output:**
- data/step03_bootstrap_results.csv
- data/step03_bootstrap_distribution.csv (full 1000 x 4 matrix)

**Validation Requirement:**
Validation tools MUST be used after bootstrap completion.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_bootstrap_results.csv: 4 rows x 6 columns
- Columns: domain, attenuation_point, ci_lower_95, ci_upper_95, ci_width, stability_flag
- data/step03_bootstrap_distribution.csv: 1000 rows x 5 columns
- Columns: iteration, overall_atten, what_atten, where_atten, when_atten

*Value Ranges:*
- attenuation_point in [0, 100] (percentage scale)
- ci_lower_95, ci_upper_95 in [0, 100]
- ci_width > 0 (positive interval width)
- CI bounds: ci_lower_95 < attenuation_point < ci_upper_95

*Data Quality:*
- All 1000 bootstrap iterations completed
- No missing values in CI bounds
- Bootstrap distribution approximately normal (assess via range)
- Stability flags accurate (width < 40% threshold)

*Log Validation:*
- Required patterns: "Bootstrap complete: 1000 iterations", "CI computed: 4 domains", "Seed set: 42"
- Forbidden patterns: "ERROR", "Bootstrap failed", "Invalid CI"

**Expected Behavior on Validation Failure:**
- Raise error with specific bootstrap problem
- Log to logs/step03_bootstrap_ci.log
- Quit immediately, invoke g_debug

### Step 4: Statistical Significance Testing
**Dependencies:** Step 3 (bootstrap confidence intervals)
**Complexity:** Low (<5 minutes)

**Purpose:** Test significance of attenuation ratios with multiple comparison corrections

**Input:**
- data/step03_bootstrap_results.csv

**Processing:**
- Test H0: attenuation = 0 vs H1: attenuation > 0 for each domain
- Primary test: 95% CI excludes 0 (one-tailed, attenuation expected positive)
- Calculate uncorrected p-values using bootstrap distribution
- Bonferroni correction for 4 domains: alpha = 0.05/4 = 0.0125 per test
- FDR correction using Benjamini-Hochberg procedure
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Format: p_uncorrected, p_bonferroni, p_fdr
- Effect size interpretation: <30% minimal, 30-70% partial, >70% substantial

**Output:**
- data/step04_significance_tests.csv

**Validation Requirement:**
Validation tools MUST be used after significance testing.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_significance_tests.csv: 4 rows x 8 columns
- Columns: domain, attenuation_pct, p_uncorrected, p_bonferroni, p_fdr, significant_uncorrected, significant_bonferroni, effect_size_category

*Value Ranges:*
- All p-values in [0, 1] (valid probability range)
- p_bonferroni = p_uncorrected * 4 (or capped at 1.0)
- p_fdr <= p_bonferroni (FDR less conservative)

*Data Quality:*
- Logical consistency: significant flags match p-value thresholds
- Effect size categories: "minimal", "partial", or "substantial"
- Bonferroni inequality maintained (corrected >= uncorrected)

*Log Validation:*
- Required patterns: "Significance tests complete", "Multiple comparisons corrected", "Decision D068 compliance"
- Forbidden patterns: "Invalid p-value", "Correction failed"

**Expected Behavior on Validation Failure:**
- Raise error with specific testing problem
- Log to logs/step04_significance_testing.log
- Quit immediately, invoke g_debug

### Step 5: Domain Comparison Analysis
**Dependencies:** Step 3 (bootstrap distributions), Step 4 (significance results)
**Complexity:** Medium (~10 minutes)

**Purpose:** Compare attenuation patterns across domains to test VR scaffolding hypothesis (What > Where > When)

**Input:**
- data/step03_bootstrap_distribution.csv
- data/step04_significance_tests.csv

**Processing:**
- Pairwise comparisons using bootstrap distributions:
  - What vs Where: difference in attenuation percentages
  - What vs When: difference in attenuation percentages  
  - Where vs When: difference in attenuation percentages
- For each comparison:
  - Compute difference distribution: domain1_atten - domain2_atten
  - 95% CI for difference using percentile method
  - Test H0: difference = 0 vs H1: difference ≠ 0 (two-tailed)
- Multiple comparison correction: 3 tests, Bonferroni alpha = 0.05/3 = 0.0167
- Expected pattern test: What > Where > When (one-tailed tests)
- Report BOTH uncorrected AND corrected p-values (Decision D068)

**Output:**
- data/step05_domain_comparisons.csv

**Validation Requirement:**
Validation tools MUST be used after domain comparison.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_domain_comparisons.csv: 3 rows x 9 columns
- Columns: comparison, domain1, domain2, difference_point, difference_se, ci_lower, ci_upper, p_uncorrected, p_bonferroni

*Value Ranges:*
- difference_point in [-100, 100] (percentage difference scale)
- difference_se > 0 (positive standard error)
- CI bounds: ci_lower < difference_point < ci_upper
- p-values in [0, 1]

*Data Quality:*
- All 3 pairwise comparisons computed
- Comparison labels match expected pairs
- Standard errors derived from bootstrap variation

*Log Validation:*
- Required patterns: "Domain comparisons complete: 3 tests", "Bootstrap differences computed"
- Forbidden patterns: "Comparison failed", "Invalid difference"

**Expected Behavior on Validation Failure:**
- Raise error with specific comparison problem
- Log to logs/step05_domain_comparisons.log
- Quit immediately, invoke g_debug

### Step 6: Sensitivity and Validation Analysis
**Dependencies:** Steps 1-5 (all primary analyses)
**Complexity:** Medium (~10 minutes)

**Purpose:** Assess robustness through outlier exclusion and assumption validation

**Input:**
- data/step01_age_coefficients.csv
- Original participant-level data (for outlier detection)

**Processing:**
- Outlier detection using Cook's Distance from original RQ 7.2.1 regressions
- Threshold: Cook's D > 4/n = 4/100 = 0.04
- Sensitivity analysis: re-compute attenuation with outliers excluded
- Compare point estimates: robust vs. original (flag if difference > 5%)
- Bootstrap assumption checks:
  - Independence: note stratified age sampling as potential limitation
  - Sample size adequacy: 1000 iterations appropriate for N=100
- Cross-validation stability: 5-fold CV on attenuation estimates
- Generate robustness flags and recommendations

**Output:**
- data/step06_sensitivity_analysis.csv
- data/step06_robustness_summary.txt

**Validation Requirement:**
Validation tools MUST be used after sensitivity analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_sensitivity_analysis.csv: 4 rows x 6 columns
- Columns: domain, original_atten, robust_atten, difference, outliers_n, robust_flag
- data/step06_robustness_summary.txt: text summary with validation flags

*Value Ranges:*
- original_atten, robust_atten in [0, 100]
- difference = abs(robust_atten - original_atten)
- outliers_n in [0, 10] (reasonable outlier count)

*Data Quality:*
- Robust estimates computed for all domains
- Outlier count realistic (typically < 5% of sample)
- Robust flags accurate (difference > 5% threshold)

*Log Validation:*
- Required patterns: "Sensitivity analysis complete", "Outliers detected: N", "Robustness assessed"
- Forbidden patterns: "Sensitivity failed", "Invalid outlier count"

**Expected Behavior on Validation Failure:**
- Raise error with specific sensitivity problem
- Log to logs/step06_sensitivity_analysis.log
- Quit immediately, invoke g_debug

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (prerequisite verification)
- data/step01_age_coefficients.csv (extracted coefficients from RQ 7.2.1)
- data/step02_attenuation_ratios.csv (point estimates for each domain)
- data/step03_bootstrap_results.csv (confidence intervals)
- data/step03_bootstrap_distribution.csv (full bootstrap samples)
- data/step04_significance_tests.csv (p-values with corrections)
- data/step05_domain_comparisons.csv (between-domain tests)
- data/step06_sensitivity_analysis.csv (outlier robustness)
- data/step06_robustness_summary.txt (validation summary)

### Logs (ONLY execution logs)
- logs/step00_dependency_validation.log
- logs/step01_load_coefficients.log
- logs/step02_compute_attenuation.log
- logs/step03_bootstrap_ci.log
- logs/step04_significance_testing.log
- logs/step05_domain_comparisons.log
- logs/step06_sensitivity_analysis.log

### Plots (EMPTY until rq_plots runs)
- Note: Plot source data for domain comparison visualization will be in data/step05_domain_comparisons.csv

### Results (EMPTY until rq_results runs)
- Note: summary.md will be created by rq_results agent

---

## Expected Data Formats

### Step-to-Step Transformations
1. **Step 0 → Step 1:** File paths → Age coefficients
2. **Step 1 → Step 2:** Coefficients → Attenuation ratios (point estimates)
3. **Step 2 → Step 3:** Point estimates → Bootstrap distributions → Confidence intervals
4. **Step 3 → Step 4:** Bootstrap CIs → Significance tests with corrections
5. **Step 4 → Step 5:** Individual results → Between-domain comparisons
6. **All → Step 6:** Complete analysis → Sensitivity and robustness validation

### Column Naming Conventions
- **Domains:** "overall", "what", "where", "when"
- **Model types:** "bivariate", "controlled"
- **Statistical terms:** "beta_age", "se_age", "ci_lower", "ci_upper"
- **Attenuation:** "attenuation_pct", "absolute_attenuation", "residual_effect"
- **P-values:** "p_uncorrected", "p_bonferroni", "p_fdr"

### Data Type Constraints
- **Attenuation percentages:** float64, range [0, 100]
- **Coefficients:** float64, range [-1, 1]
- **P-values:** float64, range [0, 1]
- **Domain labels:** object (categorical)
- **Flags:** boolean or categorical ("significant"/"non-significant")

---

## Cross-RQ Dependencies

**Primary Dependency:** RQ 7.2.1 (Age and cognitive test effects on REMEMVR)

**Required Files:**
- Bivariate age coefficients (Model 1: Age → REMEMVR)
- Controlled age coefficients (Model 2: Age + Cognitive Tests → REMEMVR)
- Available for all domains: overall theta, What theta, Where theta, When theta

**File Discovery Patterns:**
- Primary: results/ch7/7.2.1/data/step04_regression_results.csv
- Alternative: results/ch7/7.2.1/data/*regression*.csv
- Fallback: results/ch7/7.2.1/data/*.{csv,txt} containing "age" and "coefficient"

**Dependency Validation Strategy:**
- Step 0 validates all dependencies before proceeding
- Fallback paths accommodate naming variations
- Circuit breaker: QUIT if coefficients unavailable

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
**Validation Tools Required:** File existence + content validation
**4-Layer Structure:** [As specified above in each step]

#### Step 1: Extract Coefficients  
**Validation Tools Required:** Data format + value range validation
**4-Layer Structure:** [As specified above in each step]

#### Step 2: Compute Attenuation
**Validation Tools Required:** Mathematical + logical consistency validation
**4-Layer Structure:** [As specified above in each step]

#### Step 3: Bootstrap CI
**Validation Tools Required:** Statistical + distribution validation
**4-Layer Structure:** [As specified above in each step]

#### Step 4: Significance Testing
**Validation Tools Required:** Statistical inference + multiple comparison validation
**4-Layer Structure:** [As specified above in each step]

#### Step 5: Domain Comparisons
**Validation Tools Required:** Pairwise comparison + pattern validation
**4-Layer Structure:** [As specified above in each step]

#### Step 6: Sensitivity Analysis
**Validation Tools Required:** Robustness + outlier validation
**4-Layer Structure:** [As specified above in each step]

---

## Summary

**Total Steps:** 7 (Step 0: validation + Steps 1-6: analysis)
**Estimated Runtime:** 30-40 minutes (dominated by 1000 bootstrap iterations)
**Cross-RQ Dependencies:** RQ 7.2.1 (age coefficients from hierarchical regression)
**Primary Outputs:** Attenuation ratios with bootstrap CIs for 4 domains
**Validation Coverage:** 100% (all 7 steps have 4-layer validation requirements)

**Key Hypothesis:** Substantial attenuation (>70%) expected for overall REMEMVR, consistent with VR scaffolding hypothesis. Domain pattern expected: What > Where > When attenuation.

**Critical Methodological Notes:**
- Bootstrap assumes independence (note potential age-group dependency)
- Attenuation analysis provides intuitive mediation interpretation
- Decision D068 compliance: dual p-value reporting throughout
- Ch7 alpha correction: 0.0125 for within-RQ family (4 domains)

**Statistical Implementation Details:**
- Random seed: 42 for all bootstrap procedures
- Bootstrap: 1000 iterations, participant-level resampling with replacement
- CI method: Percentile (2.5th, 97.5th percentiles)
- Multiple comparisons: Bonferroni + FDR correction
- Sensitivity: Cook's D > 0.04 outlier threshold

**Success Criteria:**
- Attenuation > 50% for overall REMEMVR (supports scaffolding hypothesis)
- Bootstrap CIs stable (width < 40% of point estimate)
- Pattern consistent with VR scaffolding (What > Where > When)
- Sensitivity analysis shows robust findings (±5% with outlier exclusion)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan → creates 3_tools.yaml
3. rq_analysis reads plan + tools → creates 4_analysis.yaml  
4. g_code reads analysis → generates executable code

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent with v5.1 enhancements