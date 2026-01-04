# Analysis Plan: RQ 7.2.2 - Do cognitive tests attenuate age effects on REMEMVR?

**Research Question:** 7.2.2
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

**Research Question:**
What proportion of age-related variance is attenuated when controlling for cognitive tests? Complete attenuation suggests tests capture all age-sensitive processes; partial attenuation suggests REMEMVR captures additional age-sensitive processes.

**Pipeline:** Attenuation Analysis with Bootstrap Confidence Intervals
**Steps:** 7 total analysis steps (Step 0: validation + Steps 1-6: analysis)
**Estimated Runtime:** 30-40 minutes (including 1000 bootstrap iterations)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Ch7 Bonferroni correction: alpha = 0.05/4 = 0.0125 for 4 domains
- Bootstrap seed=42 for reproducibility
- VR scaffolding hypothesis testing via domain comparisons

**Cross-RQ Dependencies:**
- RQ 7.2.1: Age coefficients (bivariate vs controlled effects)
- Ch5 domain analyses: theta scores for What, Where, When domains

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies

**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (5 minutes)

**Purpose:** Verify required RQ 7.2.1 outputs and Ch5 theta scores exist before proceeding

**Input:**
- Primary: results/ch7/7.2.1/data/step04_regression_results.csv (age coefficients)
- Alternative: results/ch7/7.2.1/data/*regression*.csv
- Fallback: results/ch7/7.2.1/data/step*_age_*.{csv,txt}
- Ch5 theta files:
  - results/ch5/5.1.1/data/step03_theta_scores.csv (overall theta_all)
  - results/ch5/5.2.1/data/step03_theta_scores.csv (What domain)
  - results/ch5/5.2.2/data/step03_theta_scores.csv (Where domain)  
  - results/ch5/5.2.3/data/step03_theta_scores.csv (When domain)
- Expected content: Age coefficients for bivariate and controlled models

**Processing:**
- Check RQ 7.2.1 status.yaml (rq_results = success)
- Locate regression results file using fallback patterns
- Verify file contains both beta_age_bivariate and beta_age_controlled
- Check Ch5 theta score files exist for all 4 analyses
- Verify theta files contain 100 participants each
- Log all validation checks with success/failure status

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Log entries confirming dependency status

*Value Ranges:*
- N/A (validation step only)

*Data Quality:*
- All 5 dependency files located and accessible
- Each theta file contains exactly 100 participants
- Regression file contains both required coefficients

*Log Validation:*
- Required patterns: "RQ 7.2.1 regression file located", "Ch5 theta files validated"
- Required patterns: "VALIDATION - PASS"
- Forbidden patterns: "DEPENDENCY MISSING", "ERROR", "file not found"

**Expected Behavior on Validation Failure:**
Quit immediately with specific dependency error message and invoke g_debug agent.

---

### Step 1: Extract and Merge Regression Coefficients

**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (5 minutes)

**Purpose:** Load age coefficients from RQ 7.2.1 and merge with participant theta scores

**Input:**
- results/ch7/7.2.1/data/step04_regression_results.csv
- results/ch5/5.1.1/data/step03_theta_scores.csv (overall)
- results/ch5/5.2.1/data/step03_theta_scores.csv (What)
- results/ch5/5.2.2/data/step03_theta_scores.csv (Where)
- results/ch5/5.2.3/data/step03_theta_scores.csv (When)

**Processing:**
- Load regression coefficients for age from RQ 7.2.1
- Extract beta_age_bivariate (Model 1: age only)
- Extract beta_age_controlled (Model 2: age + cognitive tests)
- Load participant theta scores from all 4 Ch5 analyses
- Verify participant alignment across datasets (same UIDs)
- Create merged dataset with coefficients and theta scores
- Document sample size and missing data patterns

**Output:**
- data/step01_merged_coefficients.csv (coefficients + theta scores)
- data/step01_data_summary.txt (sample description)

**Validation Requirement:**
Validation tools MUST be used after data extraction and merging.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_merged_coefficients.csv: 100 rows x 8 columns
- Columns: UID, theta_all, theta_what, theta_where, theta_when, beta_age_bivariate_all, beta_age_controlled_all, beta_age_bivariate_domain
- data/step01_data_summary.txt: text summary of merged data

*Value Ranges:*
- theta scores in [-3, 3] (IRT ability scale)
- beta_age coefficients in [-0.5, 0.5] (standardized regression coefficients)
- All coefficients non-missing (no NaN values)

*Data Quality:*
- Exactly 100 participants in merged dataset
- No duplicate UIDs
- All theta scores non-missing
- All age coefficients non-missing

*Log Validation:*
- Required patterns: "Merged dataset: 100 participants x 8 variables"
- Required patterns: "Age coefficients extracted: bivariate and controlled"
- Forbidden patterns: "ERROR", "missing data", "merge failed"

**Expected Behavior on Validation Failure:**
Log specific merge error and quit execution with g_debug invocation.

---

### Step 2: Compute Attenuation Ratios

**Dependencies:** Step 1 (merged coefficients)
**Complexity:** Medium (10 minutes)

**Purpose:** Calculate attenuation ratios as percentage reduction in age coefficients when controlling for cognitive tests

**Input:**
- data/step01_merged_coefficients.csv

**Processing:**
- Calculate attenuation ratio for overall REMEMVR:
  - Formula: (beta_age_bivariate - beta_age_controlled) / beta_age_bivariate
  - Convert to percentage: multiply by 100
- Calculate domain-specific attenuation ratios:
  - What domain: using What-specific age coefficients
  - Where domain: using Where-specific age coefficients  
  - When domain: using When-specific age coefficients
- Handle edge cases:
  - If beta_age_bivariate = 0: set attenuation = NaN
  - If attenuation < 0: flag as "negative attenuation" (unexpected)
- Compute absolute and relative effect sizes
- Document attenuation classification:
  - <30%: minimal attenuation
  - 30-70%: partial attenuation
  - >70%: substantial attenuation

**Output:**
- data/step02_attenuation_ratios.csv (point estimates by domain)
- data/step02_effect_classification.txt (interpretive categories)

**Validation Requirement:**
Validation tools MUST be used after attenuation ratio computation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_attenuation_ratios.csv: 4 rows x 6 columns
- Columns: domain, beta_bivariate, beta_controlled, attenuation_ratio, attenuation_percent, classification
- data/step02_effect_classification.txt: text interpretation of effect sizes

*Value Ranges:*
- attenuation_percent in [0, 100] for positive attenuation
- attenuation_percent may be negative (flag as unexpected)
- beta coefficients consistent with Step 1 ranges

*Data Quality:*
- All 4 domains present (overall, What, Where, When)
- No missing attenuation values unless beta_bivariate = 0
- Classifications match percentage thresholds

*Log Validation:*
- Required patterns: "Attenuation ratios computed for 4 domains"
- Required patterns: "Effect sizes classified using standard thresholds"
- Forbidden patterns: "ERROR", "division by zero", "invalid calculation"

**Expected Behavior on Validation Failure:**
Log computation error details and invoke g_debug for diagnostic analysis.

---

### Step 3: Bootstrap Confidence Intervals for Attenuation

**Dependencies:** Step 2 (attenuation ratios)
**Complexity:** High (15 minutes including bootstrap)

**Purpose:** Generate bootstrap confidence intervals for attenuation ratios using participant-level resampling

**Input:**
- data/step01_merged_coefficients.csv (for bootstrap resampling)
- data/step02_attenuation_ratios.csv (observed point estimates)

**Processing:**
- Implement participant-level block bootstrap (preserves within-participant correlation):
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Resample participants WITH replacement
  - Keep all observations for selected participants
- For each bootstrap iteration:
  - Fit bivariate age models (age -> theta_domain)
  - Fit controlled age models (age + cognitive tests -> theta_domain)
  - Extract age coefficients from both models
  - Compute attenuation ratio using same formula as Step 2
- Store bootstrap distribution for each domain
- Compute 95% confidence intervals:
  - Method: percentile method (2.5th, 97.5th percentiles)
  - Document CI width as percentage of point estimate
  - Flag if CI width > 40% of point estimate (unstable)
- Significance testing:
  - H0: attenuation = 0 (no mediation)
  - Two-tailed test: CI excludes 0 indicates p < 0.05
  - Report bootstrap p-value: proportion of iterations where attenuation <= 0

**Output:**
- data/step03_bootstrap_distributions.csv (1000 x 4 bootstrap samples)
- data/step03_confidence_intervals.csv (CI results by domain)
- data/step03_bootstrap_diagnostics.txt (stability assessment)

**Validation Requirement:**
Validation tools MUST be used after bootstrap confidence interval computation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_bootstrap_distributions.csv: 1000 rows x 4 columns
- Columns: overall, what, where, when (bootstrap attenuation values)
- data/step03_confidence_intervals.csv: 4 rows x 7 columns
- Columns: domain, point_estimate, ci_lower, ci_upper, ci_width, ci_width_percent, bootstrap_p
- data/step03_bootstrap_diagnostics.txt: convergence and stability checks

*Value Ranges:*
- Bootstrap attenuation values in [-50, 150] (allow for sampling variability)
- ci_lower < point_estimate < ci_upper for valid CIs
- bootstrap_p in [0, 1]
- ci_width_percent in [0, 100]

*Data Quality:*
- Exactly 1000 bootstrap iterations completed
- All 4 domains have valid CIs
- No convergence failures in bootstrap
- Bootstrap seed=42 documented

*Log Validation:*
- Required patterns: "Bootstrap complete: 1000 iterations, seed=42"
- Required patterns: "CIs computed using percentile method"
- Required patterns: "Bootstrap stability: all domains converged"
- Forbidden patterns: "ERROR", "convergence failed", "singular matrix"

**Expected Behavior on Validation Failure:**
Log bootstrap failure details, check for model convergence issues, invoke g_debug.

---

### Step 4: Domain Comparison Analysis

**Dependencies:** Step 3 (bootstrap CIs)
**Complexity:** Medium (8 minutes)

**Purpose:** Test whether domains show differential attenuation patterns using bootstrap hypothesis tests

**Input:**
- data/step03_bootstrap_distributions.csv
- data/step03_confidence_intervals.csv

**Processing:**
- Pairwise domain comparisons using bootstrap distributions:
  - Compare: What vs Where, What vs When, Where vs When
  - Test statistic: difference in attenuation percentages
  - Bootstrap p-value: proportion where difference <= 0
- Multiple comparison corrections:
  - Family: Within-RQ domain comparisons (3 pairwise tests)
  - Bonferroni correction: alpha = 0.05/3 = 0.0167 per test
  - FDR correction: Benjamini-Hochberg procedure
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Effect size calculations:
  - Cohen's d for attenuation differences
  - Bootstrap 95% CI for each pairwise difference
- Theoretical pattern testing:
  - H1: What > Where > When (VR scaffolding hypothesis)
  - Directional tests using one-tailed bootstrap p-values
- Summary interpretation:
  - Document which comparisons are significant
  - Assess alignment with theoretical predictions

**Output:**
- data/step04_domain_comparisons.csv (pairwise test results)
- data/step04_multiple_corrections.csv (corrected p-values)
- data/step04_pattern_analysis.txt (theoretical alignment assessment)

**Validation Requirement:**
Validation tools MUST be used after domain comparison analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_domain_comparisons.csv: 3 rows x 8 columns
- Columns: comparison, difference, ci_lower, ci_upper, p_uncorrected, p_bonferroni, p_fdr, cohens_d
- data/step04_multiple_corrections.csv: 3 rows x 5 columns
- Columns: comparison, p_uncorrected, p_bonferroni, p_fdr, significant_corrected
- data/step04_pattern_analysis.txt: theoretical pattern evaluation

*Value Ranges:*
- difference in [-100, 100] (percentage points)
- p_uncorrected in [0, 1]
- p_bonferroni <= p_uncorrected x 3 (Bonferroni bound)
- p_fdr <= p_uncorrected (FDR bound)
- cohens_d in [-3, 3] (standardized effect sizes)

*Data Quality:*
- All 3 pairwise comparisons present
- Dual p-value reporting for all tests (Decision D068)
- Bootstrap CIs valid for all differences
- Theoretical pattern assessment documented

*Log Validation:*
- Required patterns: "Domain comparisons: 3 pairwise tests completed"
- Required patterns: "Multiple corrections applied: Bonferroni + FDR"
- Required patterns: "Theoretical pattern analysis complete"
- Forbidden patterns: "ERROR", "invalid comparison", "correction failed"

**Expected Behavior on Validation Failure:**
Log comparison failure details and check bootstrap distribution validity.

---

### Step 5: Effect Size Analysis and Power Assessment

**Dependencies:** Step 4 (domain comparisons)
**Complexity:** Medium (7 minutes)

**Purpose:** Compute comprehensive effect sizes and post-hoc power analysis for attenuation detection

**Input:**
- data/step02_attenuation_ratios.csv
- data/step03_confidence_intervals.csv
- results/ch7/7.2.1/data/step04_regression_results.csv (for R-squared values)

**Processing:**
- Effect size calculations:
  - Cohen's f-squared: R_squared_change / (1 - R_squared_controlled)
  - For each domain: compare Model 1 vs Model 2 R-squared
  - Bootstrap 95% CI for f-squared using delta method
- Power analysis for attenuation detection:
  - Post-hoc power analysis for detecting >30% attenuation
  - Given: N=100, alpha=0.0125 (Bonferroni corrected)
  - Effect size: observed attenuation converted to Cohen's d
  - Use: custom power calculation for mediation effects
  - Report: actual power for observed effect sizes
- Practical significance assessment:
  - Classify effect sizes: small (f² = 0.02), medium (f² = 0.15), large (f² = 0.35)
  - Compare to published mediation studies in aging literature
  - Document clinical/practical significance thresholds
- Sensitivity analysis preparation:
  - Identify minimum detectable effect size at 80% power
  - Document limitations if power < 0.80 for any domain

**Output:**
- data/step05_effect_sizes.csv (f-squared and CIs by domain)
- data/step05_power_analysis.csv (power calculations)
- data/step05_practical_significance.txt (interpretive guidelines)

**Validation Requirement:**
Validation tools MUST be used after effect size and power analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_effect_sizes.csv: 4 rows x 6 columns
- Columns: domain, f_squared, f_squared_ci_lower, f_squared_ci_upper, effect_classification, r_squared_change
- data/step05_power_analysis.csv: 4 rows x 5 columns
- Columns: domain, observed_attenuation, effect_size_d, power, minimum_detectable_effect
- data/step05_practical_significance.txt: interpretive framework

*Value Ranges:*
- f_squared in [0, 2] (reasonable range for mediation effects)
- power in [0, 1]
- effect_size_d in [0, 2] (positive effect sizes expected)
- r_squared_change in [0, 0.5] (mediation typically modest)

*Data Quality:*
- All 4 domains have valid effect size calculations
- Power analysis completed for each domain
- Effect classifications match standard thresholds
- Practical significance guidelines documented

*Log Validation:*
- Required patterns: "Effect sizes computed: f-squared with 95% CIs"
- Required patterns: "Power analysis: N=100, alpha=0.0125"
- Required patterns: "Practical significance assessment complete"
- Forbidden patterns: "ERROR", "power calculation failed", "invalid effect size"

**Expected Behavior on Validation Failure:**
Log effect size calculation errors and check for numerical issues in power analysis.

---

### Step 6: Model Diagnostics and Sensitivity Analysis

**Dependencies:** Step 5 (effect sizes and power)
**Complexity:** Medium (10 minutes)

**Purpose:** Comprehensive diagnostic checks and sensitivity analysis for robustness assessment

**Input:**
- data/step01_merged_coefficients.csv (original data)
- data/step02_attenuation_ratios.csv (main results)
- data/step03_bootstrap_distributions.csv (bootstrap samples)

**Processing:**
- Assumption validation for underlying regression models:
  - Normality: Shapiro-Wilk test on residuals from RQ 7.2.1
  - Homoscedasticity: Breusch-Pagan test for residuals
  - Linearity: Check age-theta relationships using scatterplots
  - Multicollinearity: VIF assessment for age + cognitive predictors
- Remedial actions if assumptions violated:
  - Normality p < 0.05: Report bootstrap CIs as primary (already done)
  - Heteroscedasticity p < 0.05: Note impact on standard errors
  - VIF > 5: Document multicollinearity impact on attenuation
- Outlier analysis:
  - Identify potential outliers using Cook's distance > 4/n
  - Sensitivity analysis: recompute attenuation without outliers
  - Document impact: change in attenuation > 5% considered meaningful
- Bootstrap stability assessment:
  - Check bootstrap convergence using running means
  - Assess CI stability: compare 500 vs 1000 iterations
  - Document any instability issues
- Cross-validation approach:
  - 5-fold cross-validation for attenuation estimates
  - Random seed: 42 for reproducibility
  - Assess generalizability of attenuation across data subsets

**Output:**
- data/step06_assumption_checks.csv (diagnostic test results)
- data/step06_sensitivity_analysis.csv (outlier impact)
- data/step06_bootstrap_stability.txt (convergence assessment)
- data/step06_crossvalidation_results.csv (CV stability)

**Validation Requirement:**
Validation tools MUST be used after comprehensive diagnostic analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_assumption_checks.csv: 4 rows x 6 columns
- Columns: domain, normality_p, homoscedasticity_p, max_vif, outlier_count, assumptions_met
- data/step06_sensitivity_analysis.csv: 4 rows x 4 columns
- Columns: domain, attenuation_original, attenuation_no_outliers, percent_change
- data/step06_bootstrap_stability.txt: convergence diagnostics
- data/step06_crossvalidation_results.csv: 5 rows x 3 columns (CV folds)

*Value Ranges:*
- p-values in [0, 1] for assumption tests
- max_vif in [1, 10] (acceptable multicollinearity range)
- outlier_count in [0, 20] (reasonable outlier range)
- percent_change in [-20, 20] (sensitivity threshold)

*Data Quality:*
- All 4 domains assessed for assumptions
- Sensitivity analysis completed successfully
- Bootstrap stability documented with numerical evidence
- Cross-validation results stable across folds

*Log Validation:*
- Required patterns: "Assumption checks completed for all domains"
- Required patterns: "Sensitivity analysis: outlier impact assessed"
- Required patterns: "Bootstrap stability confirmed"
- Required patterns: "Cross-validation: stable attenuation estimates"
- Forbidden patterns: "ERROR", "assumption check failed", "convergence issues"

**Expected Behavior on Validation Failure:**
Log specific diagnostic failure and provide remedial analysis recommendations.

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)

**Step 0:** data/step00_dependency_validation.txt
**Step 1:** data/step01_merged_coefficients.csv, data/step01_data_summary.txt  
**Step 2:** data/step02_attenuation_ratios.csv, data/step02_effect_classification.txt
**Step 3:** data/step03_bootstrap_distributions.csv, data/step03_confidence_intervals.csv, data/step03_bootstrap_diagnostics.txt
**Step 4:** data/step04_domain_comparisons.csv, data/step04_multiple_corrections.csv, data/step04_pattern_analysis.txt
**Step 5:** data/step05_effect_sizes.csv, data/step05_power_analysis.csv, data/step05_practical_significance.txt
**Step 6:** data/step06_assumption_checks.csv, data/step06_sensitivity_analysis.csv, data/step06_bootstrap_stability.txt, data/step06_crossvalidation_results.csv

**Plot Source Data:** data/step04_domain_comparisons_plot_data.csv (attenuation by domain for visualization)

### Logs (ONLY execution logs)

**Step 0:** logs/step00_dependency_validation.log
**Step 1:** logs/step01_extract_merge_coefficients.log
**Step 2:** logs/step02_compute_attenuation.log
**Step 3:** logs/step03_bootstrap_confidence_intervals.log
**Step 4:** logs/step04_domain_comparisons.log
**Step 5:** logs/step05_effect_sizes_power.log
**Step 6:** logs/step06_diagnostics_sensitivity.log

### Plots (EMPTY until rq_plots runs)

Will be populated by rq_plots agent using plot source data from data/ folder.

### Results (EMPTY until rq_results runs)

Will contain summary.md created by rq_results agent.

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 -> Step 1:** Dependency validation enables coefficient extraction
**Step 1 -> Step 2:** Merged coefficients enable attenuation ratio calculation  
**Step 2 -> Step 3:** Point estimates enable bootstrap confidence interval computation
**Step 3 -> Step 4:** Bootstrap distributions enable domain comparison testing
**Step 4 -> Step 5:** Comparison results enable comprehensive effect size analysis
**Step 5 -> Step 6:** Effect sizes enable diagnostic assessment and sensitivity testing

### Column Naming Conventions

**Participant IDs:** UID (consistent across all files)
**Theta scores:** theta_all, theta_what, theta_where, theta_when
**Coefficients:** beta_age_bivariate, beta_age_controlled  
**Attenuation:** attenuation_ratio, attenuation_percent
**Confidence intervals:** ci_lower, ci_upper, ci_width_percent
**p-values:** p_uncorrected, p_bonferroni, p_fdr (Decision D068 compliance)

### Data Type Constraints

**UID:** object (string identifier)
**Theta scores:** float64, nullable=False, range=[-3, 3]
**Beta coefficients:** float64, nullable=False, range=[-1, 1]  
**Attenuation ratios:** float64, nullable=True (NaN if beta_bivariate=0)
**p-values:** float64, nullable=False, range=[0, 1]
**Effect sizes:** float64, nullable=False, range=[0, 3]

---

## Cross-RQ Dependencies

**RQ 7.2.1 (Age and cognitive test effects):**
- Primary: results/ch7/7.2.1/data/step04_regression_results.csv
- Alternative patterns: results/ch7/7.2.1/data/*regression*.csv
- Fallback patterns: results/ch7/7.2.1/data/step*_age_*.{csv,txt}
- Required content: beta_age_bivariate and beta_age_controlled coefficients
- Status requirement: rq_results = success in status.yaml

**Ch5 Domain Analyses (Theta scores):**
- Overall: results/ch5/5.1.1/data/step03_theta_scores.csv
- What domain: results/ch5/5.2.1/data/step03_theta_scores.csv  
- Where domain: results/ch5/5.2.2/data/step03_theta_scores.csv
- When domain: results/ch5/5.2.3/data/step03_theta_scores.csv
- Required content: 100 participants with theta estimates
- Status requirement: rq_results = success for all Ch5 RQs

**Circuit Breaker:** If ANY dependency missing, QUIT with specific error message and invoke g_debug.

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

All validation requirements are embedded in each step specification above using the 4-layer validation structure:

1. **Output Files:** Exact paths, row/column counts, data types
2. **Value Ranges:** Scientific bounds with justification  
3. **Data Quality:** Missing data tolerance, expected N, distribution checks
4. **Log Validation:** Required patterns, forbidden patterns, acceptable warnings

### Post-Execution Validation Flow

1. **Tool execution** (rq_analysis + g_code)
2. **Mandatory validation** (rq_inspect using criteria above)  
3. **Success confirmation** (all 4 layers pass)
4. **Failure handling** (specific error reporting + g_debug invocation)

---

## Summary

**Total Steps:** 7 (Step 0: validation + Steps 1-6: analysis)
**Estimated Runtime:** 30-40 minutes total
**Cross-RQ Dependencies:** RQ 7.2.1 (regression coefficients) + Ch5 domain analyses (theta scores)
**Primary Outputs:** Attenuation ratios with bootstrap CIs, domain comparisons, effect sizes
**Validation Coverage:** 100% (all 7 steps have 4-layer validation requirements)

**Key Hypothesis:** 
VR scaffolding hypothesis predicts >70% attenuation of age effects by cognitive tests, with domain pattern What > Where > When.

**Critical Methodological Notes:**
- Participant-level bootstrap preserves within-participant correlation structure
- Bootstrap seed=42 ensures reproducibility across runs
- Dual p-value reporting (D068) for all significance tests  
- Bonferroni correction (alpha=0.0125) for family-wise error control
- Comprehensive sensitivity analysis addresses robustness concerns
- Cross-validation confirms generalizability of attenuation estimates

**Statistical Specifications (v5.1 Enhanced):**
- Random seed: 42 for ALL randomized procedures
- Bootstrap: 1000 iterations, participant-level, percentile CIs
- Cross-validation: 5-fold, shuffle=True, seed=42
- Multiple comparisons: Within-RQ family, Bonferroni + FDR corrections
- Power analysis: Post-hoc for N=100, alpha=0.0125, observed effect sizes
- Remedial actions: Bootstrap CIs for normality violations, robust SEs for heteroscedasticity

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml  
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code
5. rq_inspect validates outputs using embedded criteria

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent v5.1.0
- Enhanced with mandatory statistical specifications (CV, bootstrap, power, corrections)
- Comprehensive 4-layer validation requirements embedded per step
- Cross-RQ dependency handling with fallback paths implemented