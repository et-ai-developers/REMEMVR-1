# Analysis Plan: RQ 7.4.2 - BVMT predicts Where more than What

**Research Question:** 7.4.2
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

**Research Question:** Does BVMT (visuospatial memory test) show stronger prediction for Where (spatial location) than What (object identity)?

**Pipeline:** Dependent Correlations Comparison with Steiger's Z-test
**Steps:** 8 total analysis steps (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** ~30 minutes

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Chapter-level alpha correction: 0.05/28 = 0.00179 for Ch7

**Analysis Approach:**
This RQ tests domain-specificity in cognitive test prediction by comparing correlations between BVMT Total Recall scores and REMEMVR domain-specific theta scores (Where vs What). Uses Steiger's Z-test for dependent correlation comparison with comprehensive bootstrap validation and assumption checking. Analysis addresses critical gaps identified in statistical validation including power analysis, specific assumption test methods, and multiple comparison considerations.

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies

**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 domain outputs exist before proceeding with correlation analysis

**Input:**
- Primary: results/ch5/5.2.1/status.yaml (Where domain analysis status)
- Alternative: results/ch5/5.2.2/status.yaml (What domain analysis status)  
- Expected: Both Ch5 domain analyses completed (rq_results = success)
- Fallback pattern: results/ch5/5.2.*/status.yaml
- Master data: data/cache/master.xlsx (cognitive test scores)

**Processing:**
- Check Ch5 5.2.1 and 5.2.2 completion status
- Verify domain theta files exist: results/ch5/5.2.*/data/*theta*.csv
- Verify BVMT_TotR column exists in master.xlsx
- Log validation results with specific file paths found
- If dependencies missing: QUIT with "Ch5 domain analyses incomplete"

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: plain text file with validation results
- Expected sections: Ch5 status check, file discovery log, BVMT verification

*Value Ranges:*
- N/A (validation log file)

*Data Quality:*
- File contains "Ch5 5.2.1 status: success" and "Ch5 5.2.2 status: success"
- Lists actual file paths found for domain theta scores
- Confirms BVMT_TotR column exists in master.xlsx

*Log Validation:*
- Required pattern: "VALIDATION - PASS: All dependencies available"
- Required pattern: "Found domain files:"
- Forbidden patterns: "ERROR", "FAIL", "missing", "not found"

**Expected Behavior on Validation Failure:**
Quit analysis with error message identifying missing dependencies and log to logs/step00_validate_dependencies.log.

### Step 1: Extract Where Domain Theta Scores

**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (<5 minutes)

**Purpose:** Extract participant-level Where domain theta scores from Ch5 domain-specific analyses

**Input:**
- Primary: results/ch5/5.2.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.2.1/data/*theta*.csv
- Fallback: results/ch5/5.2.*/data/*where*theta*.csv
- Expected content: UID, theta estimates for spatial location items

**Processing:**
- Load Where domain theta scores from Ch5 5.2.1 output
- Filter for location tags: -L-, -U-, -D- (all spatial subtypes)
- Compute mean theta per participant across spatial location items
- Handle missing data: exclude participants with >50% missing location items
- Standardize UID format for merging

**Output:**
- data/step01_where_theta_scores.csv (UID, Mean_Theta_Where, N_Items_Where)

**Validation Requirement:**
Validation tools MUST be used after Where domain extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_where_theta_scores.csv: 100 rows x 3 columns
- Columns: UID (object), Mean_Theta_Where (float64), N_Items_Where (int64)

*Value Ranges:*
- Mean_Theta_Where in [-3, 3] (IRT ability scale)
- N_Items_Where in [5, 25] (reasonable item count range)
- All participants should have N_Items_Where >= 5

*Data Quality:*
- Exactly 100 participants (no missing UIDs)
- No duplicate UIDs
- Mean_Theta_Where not null for any participant
- N_Items_Where >= 5 for all participants (adequate domain sampling)

*Log Validation:*
- Required pattern: "Where domain extraction complete: 100 participants"
- Required pattern: "Mean items per participant: [numeric]"
- Forbidden patterns: "ERROR", "FAIL", "insufficient items"

**Expected Behavior on Validation Failure:**
Raise error with specific validation failure, log to logs/step01_extract_where_theta.log, quit immediately and invoke g_debug.

### Step 2: Extract What Domain Theta Scores

**Dependencies:** Step 1 (Where domain extraction)
**Complexity:** Low (<5 minutes)

**Purpose:** Extract participant-level What domain theta scores from Ch5 domain-specific analyses

**Input:**
- Primary: results/ch5/5.2.2/data/step03_theta_scores.csv (if separate What analysis)
- Alternative: results/ch5/5.2.1/data/step03_theta_scores.csv (if combined analysis)
- Fallback: results/ch5/5.2.*/data/*what*theta*.csv
- Expected content: UID, theta estimates for object identity items

**Processing:**
- Load What domain theta scores from appropriate Ch5 5.2.x output
- Filter for object identity tags: -N- (naming/identity items)
- Compute mean theta per participant across object identity items
- Handle missing data: exclude participants with >50% missing identity items
- Ensure same UIDs as Step 1 (Where domain)

**Output:**
- data/step02_what_theta_scores.csv (UID, Mean_Theta_What, N_Items_What)

**Validation Requirement:**
Validation tools MUST be used after What domain extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_what_theta_scores.csv: 100 rows x 3 columns
- Columns: UID (object), Mean_Theta_What (float64), N_Items_What (int64)

*Value Ranges:*
- Mean_Theta_What in [-3, 3] (IRT ability scale)
- N_Items_What in [5, 25] (reasonable item count range)
- All participants should have N_Items_What >= 5

*Data Quality:*
- Exactly 100 participants matching Step 1 UIDs
- No duplicate UIDs
- Mean_Theta_What not null for any participant
- UIDs identical to step01_where_theta_scores.csv

*Log Validation:*
- Required pattern: "What domain extraction complete: 100 participants"
- Required pattern: "UIDs match Where domain: 100/100"
- Forbidden patterns: "ERROR", "FAIL", "UID mismatch"

**Expected Behavior on Validation Failure:**
Raise error with specific validation failure, log to logs/step02_extract_what_theta.log, quit immediately and invoke g_debug.

### Step 3: Extract BVMT Cognitive Test Scores

**Dependencies:** Step 2 (What domain extraction)  
**Complexity:** Low (<5 minutes)

**Purpose:** Extract BVMT Total Recall scores from master cognitive test database

**Input:**
- data/cache/master.xlsx (cognitive test battery)
- Expected column: BVMT_TotR (Brief Visuospatial Memory Test Total Recall)

**Processing:**
- Load master.xlsx, extract BVMT_TotR column
- Match UIDs with domain theta participants (100 participants)
- Check for missing BVMT scores: exclude if missing
- Verify BVMT score distribution: check for ceiling/floor effects
- Document any participants excluded due to missing BVMT

**Output:**
- data/step03_bvmt_scores.csv (UID, BVMT_TotR, BVMT_Percentile)

**Validation Requirement:**
Validation tools MUST be used after BVMT extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_bvmt_scores.csv: 100 rows x 3 columns
- Columns: UID (object), BVMT_TotR (float64), BVMT_Percentile (float64)

*Value Ranges:*
- BVMT_TotR in [0, 36] (standard BVMT score range)
- BVMT_Percentile in [1, 99] (percentile rank)
- No negative scores

*Data Quality:*
- 95-100 participants (allowing for minor missing data)
- No duplicate UIDs
- BVMT_TotR not null for included participants
- Score distribution: mean 20-30, std 5-10 (typical healthy adult range)

*Log Validation:*
- Required pattern: "BVMT extraction complete: [95-100] participants"
- Required pattern: "Mean BVMT score: [20-30]"
- Forbidden patterns: "ERROR", "FAIL", "extreme outliers"

**Expected Behavior on Validation Failure:**
Raise error with specific validation failure, log to logs/step03_extract_bvmt_scores.log, quit immediately and invoke g_debug.

### Step 4: Merge Datasets and Compute Correlations

**Dependencies:** Steps 1-3 (domain theta + BVMT extraction)
**Complexity:** Medium (~10 minutes including bootstrap)

**Purpose:** Merge domain theta and BVMT data, compute bivariate correlations with bootstrap confidence intervals

**Input:**
- data/step01_where_theta_scores.csv
- data/step02_what_theta_scores.csv  
- data/step03_bvmt_scores.csv

**Processing:**
- Inner join on UID (keep only participants with all three measures)
- Compute correlations:
  - r1 = cor(BVMT_TotR, Mean_Theta_Where)
  - r2 = cor(BVMT_TotR, Mean_Theta_What)
- Bootstrap 95% confidence intervals:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - CI computation: percentile method (2.5th, 97.5th percentiles)
- Check assumptions:
  - Normality: Shapiro-Wilk test on residuals for each correlation
  - Linearity: Visual inspection of scatter plots
  - Homoscedasticity: Residual plots examination
- Extract sample statistics for power analysis

**Output:**
- data/step04_merged_dataset.csv (analysis-ready data)
- data/step04_correlations.csv (correlation results with bootstrap CIs)

**Validation Requirement:**
Validation tools MUST be used after correlation computation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_merged_dataset.csv: 95-100 rows x 4 columns
- Columns: UID, BVMT_TotR, Mean_Theta_Where, Mean_Theta_What
- data/step04_correlations.csv: 2 rows x 6 columns  
- Columns: domain, correlation, ci_lower, ci_upper, p_value, n_bootstrap

*Value Ranges:*
- Correlations in [-1, 1] (valid correlation range)
- p_values in [0, 1] 
- Bootstrap CIs: ci_lower < correlation < ci_upper
- n_bootstrap = 1000 for both correlations

*Data Quality:*
- 95-100 participants in merged dataset
- No missing values in analysis variables
- Bootstrap iterations completed: 1000 for each correlation
- Confidence intervals mathematically valid

*Log Validation:*
- Required pattern: "Correlations computed: r_Where = [value], r_What = [value]"
- Required pattern: "Bootstrap complete: 1000 iterations per correlation"
- Required pattern: "Final analysis N = [95-100]"
- Forbidden patterns: "ERROR", "FAIL", "bootstrap failed"

**Expected Behavior on Validation Failure:**
Raise error with specific validation failure, log to logs/step04_compute_correlations.log, quit immediately and invoke g_debug.

### Step 5: Steiger's Z-test for Dependent Correlations

**Dependencies:** Step 4 (correlation computation)
**Complexity:** Medium (~8 minutes including power analysis)

**Purpose:** Test hypothesis that r(BVMT, Where) > r(BVMT, What) using Steiger's Z-test for dependent correlations

**Input:**
- data/step04_correlations.csv (correlation coefficients)
- data/step04_merged_dataset.csv (raw data for intercorrelations)

**Processing:**
- Compute intercorrelation: cor(Mean_Theta_Where, Mean_Theta_What)
- Steiger's Z-test implementation:
  - Null hypothesis: r1 = r2 (equal correlations)
  - Alternative: r1 > r2 (Where correlation larger)
  - Use Williams modification for small samples
  - Calculate test statistic and one-tailed p-value
- Multiple comparison correction:
  - Family: Within-RQ (2 correlations, 1 comparison test)
  - Bonferroni: Not applicable (single comparison)
  - Report BOTH uncorrected AND chapter-corrected p-values (Decision D068)
  - Chapter correction: alpha = 0.05/28 = 0.00179
- Power analysis:
  - Post-hoc power for correlation difference detection
  - Given: N=95-100, observed correlations, alpha=0.00179
  - Calculate: minimum detectable correlation difference at 80% power
  - Use: statsmodels.stats.power or equivalent
  - Report: actual power for observed effect sizes

**Output:**
- data/step05_steiger_test.csv (test statistics, p-values, power analysis)

**Validation Requirement:**
Validation tools MUST be used after Steiger's test execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_steiger_test.csv: 1 row x 8 columns
- Columns: z_statistic, p_uncorrected, p_chapter_corrected, effect_size_d, power_observed, min_detectable_r_diff, r_where, r_what

*Value Ranges:*
- z_statistic: any real number
- p_uncorrected in [0, 1]
- p_chapter_corrected in [0, 1] (should be larger than uncorrected)
- effect_size_d >= 0 (Cohen's d for correlation difference)
- power_observed in [0, 1]
- min_detectable_r_diff in [0, 1]

*Data Quality:*
- All statistical values calculated (no NaN)
- p_chapter_corrected >= p_uncorrected (correction applied)
- Power analysis completed with realistic values
- Effect size Cohen's d calculated appropriately

*Log Validation:*
- Required pattern: "Steiger's Z = [value], p = [value]"
- Required pattern: "Dual p-values: uncorrected = [value], corrected = [value]"
- Required pattern: "Power analysis complete: power = [value]"
- Forbidden patterns: "ERROR", "FAIL", "computation failed"

**Expected Behavior on Validation Failure:**
Raise error with specific validation failure, log to logs/step05_steiger_test.log, quit immediately and invoke g_debug.

### Step 6: Effect Sizes and Descriptive Statistics

**Dependencies:** Step 5 (Steiger's test)
**Complexity:** Low (~5 minutes)

**Purpose:** Calculate effect sizes and comprehensive descriptive statistics for all analysis variables

**Input:**
- data/step04_merged_dataset.csv (raw data)
- data/step05_steiger_test.csv (test results)

**Processing:**
- Descriptive statistics for all variables:
  - Mean, SD, range, skewness, kurtosis
  - Missing data percentages
  - Outlier identification: values > 3 standard deviations
- Cohen's d for correlation difference:
  - Method: Fisher's z-transformation approach
  - Formula: (z1 - z2) / sqrt(1/(n-3) + 1/(n-3))
  - Bootstrap 95% CI for Cohen's d (1000 iterations, seed=42)
- Semi-partial correlations:
  - sr_Where: unique Where variance predicting BVMT
  - sr_What: unique What variance predicting BVMT
  - Method: residualize What from Where, correlate residuals with BVMT

**Output:**
- data/step06_descriptive_stats.csv (comprehensive descriptive statistics)
- data/step06_effect_sizes.csv (Cohen's d with bootstrap CI, semi-partial correlations)

**Validation Requirement:**
Validation tools MUST be used after effect size computation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_descriptive_stats.csv: 4 rows x 8 columns (one row per variable)
- Columns: variable, mean, sd, min, max, skewness, kurtosis, n_outliers
- data/step06_effect_sizes.csv: 1 row x 6 columns
- Columns: cohens_d, d_ci_lower, d_ci_upper, sr_where, sr_what, r_where_what

*Value Ranges:*
- Descriptive stats: realistic values for each measure type
- cohens_d: any real number (typically 0-2 for meaningful effects)
- Semi-partial correlations in [-1, 1]
- CI bounds: d_ci_lower < cohens_d < d_ci_upper

*Data Quality:*
- All 4 variables represented in descriptive stats
- Effect size calculations completed without errors
- Semi-partial correlations mathematically valid
- Bootstrap CI for Cohen's d completed (1000 iterations)

*Log Validation:*
- Required pattern: "Descriptive statistics complete: 4 variables"
- Required pattern: "Cohen's d = [value] [CI bounds]"
- Required pattern: "Semi-partial correlations: Where = [value], What = [value]"
- Forbidden patterns: "ERROR", "FAIL", "calculation failed"

**Expected Behavior on Validation Failure:**
Raise error with specific validation failure, log to logs/step06_effect_sizes.log, quit immediately and invoke g_debug.

### Step 7: Model Diagnostics and Assumption Checking

**Dependencies:** Step 6 (effect sizes)
**Complexity:** Medium (~7 minutes including remedial actions)

**Purpose:** Comprehensive assumption checking for correlation analysis with remedial actions if violations detected

**Input:**
- data/step04_merged_dataset.csv (raw data for assumption checking)
- data/step04_correlations.csv (correlation results)

**Processing:**
- Assumption checks with specific tests:
  - Normality: Shapiro-Wilk tests for each variable (BVMT, Where, What)
  - Linearity: Scatter plot inspection + polynomial fit comparison
  - Homoscedasticity: Breusch-Pagan test on correlation residuals
  - Outlier detection: Cook's distance equivalent for correlations (> 4/n)
- Range restriction assessment:
  - Check BVMT score distribution for ceiling/floor effects
  - Calculate coefficient of variation for each measure
  - Test for truncated distributions
- Remedial actions triggered by violations:
  - Normality p < 0.05: Report bootstrap CIs as primary (already computed)
  - Outliers identified: Recompute correlations excluding outliers
  - Range restriction detected: Apply Thorndike correction
  - Linearity violation: Consider Spearman correlations as alternative
- Sensitivity analysis: Report results with and without outliers

**Output:**
- data/step07_assumption_checks.csv (test results and violation flags)
- data/step07_sensitivity_analysis.csv (outlier-excluded results if applicable)

**Validation Requirement:**
Validation tools MUST be used after assumption checking execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_assumption_checks.csv: 4-6 rows x 4 columns
- Columns: assumption, test, p_value, violation_flag
- data/step07_sensitivity_analysis.csv: conditional creation based on outliers

*Value Ranges:*
- p_values in [0, 1] for all assumption tests
- violation_flag: TRUE/FALSE values
- If sensitivity file exists: contains alternative correlation results

*Data Quality:*
- All assumption tests completed (normality, linearity, homoscedasticity, outliers)
- Clear violation flags for each assumption
- Sensitivity analysis conducted if outliers detected
- Remedial actions documented

*Log Validation:*
- Required pattern: "Assumption checks complete: [4-6] tests"
- Required pattern: "Violations detected: [number]" or "No violations detected"
- Required pattern: "Sensitivity analysis: [completed/not needed]"
- Forbidden patterns: "ERROR", "FAIL", "test failed"

**Expected Behavior on Validation Failure:**
Raise error with specific validation failure, log to logs/step07_assumption_checks.log, quit immediately and invoke g_debug.

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)

**Analysis Input Data:**
- data/step00_dependency_validation.txt: Dependency check results
- data/step01_where_theta_scores.csv: Where domain theta scores (100 x 3)
- data/step02_what_theta_scores.csv: What domain theta scores (100 x 3)
- data/step03_bvmt_scores.csv: BVMT cognitive test scores (100 x 3)

**Analysis Results Data:**
- data/step04_merged_dataset.csv: Complete analysis dataset (95-100 x 4)
- data/step04_correlations.csv: Primary correlation results (2 x 6)
- data/step05_steiger_test.csv: Dependent correlation test results (1 x 8)
- data/step06_descriptive_stats.csv: Variable descriptive statistics (4 x 8)
- data/step06_effect_sizes.csv: Effect sizes and semi-partial correlations (1 x 6)
- data/step07_assumption_checks.csv: Assumption test results (4-6 x 4)
- data/step07_sensitivity_analysis.csv: Outlier sensitivity analysis (conditional)

**Plot Source Data (for rq_plots):**
- data/step04_scatter_plot_data.csv: Scatter plot points for both correlations
- data/step07_diagnostic_plot_data.csv: Assumption checking diagnostic plots

### Logs (ONLY execution logs)

- logs/step00_validate_dependencies.log: Dependency validation execution
- logs/step01_extract_where_theta.log: Where domain extraction execution  
- logs/step02_extract_what_theta.log: What domain extraction execution
- logs/step03_extract_bvmt_scores.log: BVMT extraction execution
- logs/step04_compute_correlations.log: Correlation analysis execution
- logs/step05_steiger_test.log: Dependent correlation test execution
- logs/step06_effect_sizes.log: Effect size computation execution
- logs/step07_assumption_checks.log: Assumption checking execution

### Plots (EMPTY until rq_plots runs)

Note: rq_plots will create visualization files in plots/ folder using data from:
- data/step04_scatter_plot_data.csv (correlation scatter plots)
- data/step07_diagnostic_plot_data.csv (assumption checking plots)

### Results (EMPTY until rq_results runs)

Note: rq_results will create summary.md in results/ folder synthesizing all analysis outputs.

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 -> Step 1:** Dependency validation -> Where domain extraction
- Transformation: Verify files available -> load domain-specific theta scores
- Key change: External validation -> participant-level theta means

**Steps 1-3:** Domain extraction
- Transformation: Ch5 domain outputs -> analysis-ready domain scores
- Key change: Item-level theta -> participant-level mean theta per domain

**Step 4:** Data integration + primary analysis  
- Transformation: Separate domain files -> merged analysis dataset
- Key change: Separate measures -> bivariate correlations with bootstrap CIs

**Step 5:** Hypothesis testing
- Transformation: Individual correlations -> dependent correlation comparison
- Key change: Descriptive correlations -> inferential test of domain-specificity

**Steps 6-7:** Effect sizes + diagnostics
- Transformation: Test statistics -> effect sizes + assumption validation
- Key change: Statistical results -> interpretable effects + methodological validation

### Column Naming Conventions

**Participant Identifiers:**
- UID: Consistent participant identifier across all files

**Theta Scores:**
- Mean_Theta_Where: Average theta for spatial location items  
- Mean_Theta_What: Average theta for object identity items
- N_Items_[Domain]: Number of items contributing to domain mean

**Cognitive Tests:**
- BVMT_TotR: Brief Visuospatial Memory Test Total Recall score
- BVMT_Percentile: Percentile rank for BVMT score

**Statistical Results:**
- correlation: Pearson correlation coefficient
- ci_lower, ci_upper: Bootstrap 95% confidence interval bounds
- p_uncorrected: Uncorrected p-value (Decision D068)
- p_chapter_corrected: Chapter-level corrected p-value
- z_statistic: Steiger's Z-test statistic
- cohens_d: Effect size for correlation difference

### Data Type Constraints

**Nullable vs Non-nullable:**
- UID: Non-nullable (required for all participants)
- Theta scores: Non-nullable after Step 4 merge (analysis sample)
- BVMT scores: Nullable in extraction, non-nullable in analysis
- Statistical results: Non-nullable (must compute successfully)

**Value Ranges:**
- Theta scores: [-3, 3] (IRT ability scale)
- BVMT_TotR: [0, 36] (standard BVMT range)
- Correlations: [-1, 1] (mathematical constraint)
- p_values: [0, 1] (probability constraint)

---

## Cross-RQ Dependencies

**Dependencies on Ch5 Domain Analyses:**

**Ch5 5.2.1 (Where Domain Analysis):**
- Required: rq_results = success in status.yaml
- Required files: results/ch5/5.2.1/data/step03_theta_scores.csv (or pattern match)
- Expected content: UID, theta estimates for spatial items (-L-, -U-, -D- tags)
- Fallback: Any domain analysis file containing Where/spatial theta scores

**Ch5 5.2.2 (What Domain Analysis):**
- Required: rq_results = success in status.yaml  
- Required files: results/ch5/5.2.2/data/step03_theta_scores.csv (or pattern match)
- Expected content: UID, theta estimates for object identity items (-N- tags)
- Alternative: Combined analysis in 5.2.1 with domain filtering

**Master Database:**
- Required: data/cache/master.xlsx accessible
- Required column: BVMT_TotR (Brief Visuospatial Memory Test Total Recall)
- Expected N: 100 participants matching domain analyses

**Circuit Breakers:**
- If Ch5 analyses incomplete: QUIT with "Domain analyses not available"
- If master.xlsx missing: QUIT with "Cognitive test data not available"
- If BVMT column missing: QUIT with "BVMT scores not found in master database"

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
- **Output validation:** Dependency log file created with required content sections
- **Content validation:** All dependency checks passed (Ch5 status, file existence, BVMT availability)
- **Error handling:** Clear error messages if dependencies missing

#### Step 1: Extract Where Domain
- **Data validation:** 100 participants, theta scores in valid range [-3, 3]
- **Quality validation:** Adequate item sampling (N_Items_Where >= 5), no duplicate UIDs
- **Content validation:** Where domain items properly identified and aggregated

#### Step 2: Extract What Domain  
- **Data validation:** 100 participants matching Step 1, theta scores in valid range
- **Quality validation:** Adequate item sampling (N_Items_What >= 5), UID consistency
- **Content validation:** What domain items properly identified and aggregated

#### Step 3: Extract BVMT Scores
- **Data validation:** 95-100 participants, BVMT scores in valid range [0, 36]
- **Quality validation:** Realistic score distribution, minimal missing data
- **Content validation:** BVMT Total Recall correctly extracted

#### Step 4: Compute Correlations
- **Statistical validation:** Correlations in valid range [-1, 1], bootstrap completed
- **Quality validation:** 95-100 participants in final analysis, no missing values
- **Content validation:** Both domain correlations computed with confidence intervals

#### Step 5: Steiger's Z-test  
- **Statistical validation:** Test statistic computed, dual p-values calculated
- **Quality validation:** Power analysis completed, effect sizes calculated
- **Content validation:** Dependent correlation test properly implemented

#### Step 6: Effect Sizes
- **Statistical validation:** Cohen's d with bootstrap CI, semi-partial correlations computed
- **Quality validation:** All effect sizes in valid ranges, descriptive statistics complete
- **Content validation:** Effect interpretations follow established conventions

#### Step 7: Assumption Checks
- **Statistical validation:** All assumption tests completed, violation flags accurate
- **Quality validation:** Remedial actions implemented if needed, sensitivity analysis conducted
- **Content validation:** Comprehensive diagnostic evaluation with clear conclusions

**Validation Coverage:** 100% (all 8 steps have comprehensive 4-layer validation requirements)

---

## Summary

**Total Steps:** 8 (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** ~30 minutes
**Cross-RQ Dependencies:** Ch5 5.2.1 (Where domain), Ch5 5.2.2 (What domain), master.xlsx
**Primary Outputs:** Dependent correlation test results, effect sizes, comprehensive diagnostics

**Key Hypothesis:** r(BVMT, Where) > r(BVMT, What) - visuospatial test shows stronger prediction for spatial memory domain

**Critical Methodological Notes:**
- Addresses statistical validation concerns: power analysis, specific assumption test methods, multiple testing
- Implements comprehensive bootstrap validation (1000 iterations, seed=42) 
- Uses Steiger's Z-test for dependent correlation comparison (gold standard)
- Follows Decision D068 dual p-value reporting (uncorrected + chapter-corrected)
- Includes remedial actions for assumption violations
- Comprehensive sensitivity analyses with outlier exclusion

**Statistical Enhancements Implemented:**
- Random seed=42 for all randomized procedures (bootstrap, resampling)
- Power analysis: post-hoc power calculation for correlation difference detection
- Multiple comparison strategy: chapter-level correction (alpha=0.00179) with dual reporting
- Assumption checking: specific tests (Shapiro-Wilk, Breusch-Pagan) with violation thresholds
- Remedial actions: bootstrap CIs for normality violations, outlier sensitivity analysis
- Effect size specifications: Cohen's d using Fisher's z-transformation method

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml  
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent v5.1 with enhanced statistical specifications