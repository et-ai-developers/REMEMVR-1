# Analysis Plan: RQ 7.6.2 - RAVLT Delayed Forgetting Predicts REMEMVR Slope

**Research Question:** 7.6.2
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines whether RAVLT forgetting (T5 - Delayed Recall) predicts REMEMVR forgetting rate using correlation analysis with cross-validation and bootstrap confidence intervals. The analysis tests consolidation theory predictions that individual differences in forgetting should correlate across different time scales (20-30 minutes vs 6 days).

**Pipeline:** Correlation Analysis (Bivariate + Partial)
**Steps:** 8 total analysis steps (Step 0: dependency validation + Steps 1-7: correlation analysis)
**Estimated Runtime:** ~25 minutes

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Chapter 7 Bonferroni correction: alpha = 0.05/28 = 0.00179

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 outputs and master.xlsx accessibility before proceeding

**Input:**
- Primary: results/ch5/5.1.1/status.yaml (verify rq_results: success)
- Alternative: results/ch5/5.1.1/data/step06_best_model.pkl (LMM output)
- Fallback: results/ch5/5.1.1/data/*lmm*.{txt,rds,csv} (search pattern)
- Master data: data/cache/master.xlsx (RAVLT T5Sc, DRSc columns)
- Expected content: Completed Ch5 omnibus analysis with individual slopes

**Processing:**
- Check Ch5 5.1.1 status shows rq_results: success
- Locate LMM model file using multiple search patterns
- Verify master.xlsx contains required RAVLT columns (RAV_T5Sc, RAV_DRSc)
- Test file accessibility and basic structure validation
- Log all validation checks with PASS/FAIL status
- If Ch5 incomplete: QUIT with "Ch5 5.1.1 not complete - slopes unavailable"
- If master.xlsx missing RAVLT: QUIT with "RAVLT data missing from master.xlsx"

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file ~20 lines
- Content: validation results for Ch5 status and master.xlsx access

*Value Ranges:*
- Status checks: binary PASS/FAIL results
- File counts: Ch5 files >= 1, master.xlsx = 1 file

*Data Quality:*
- All prerequisite checks completed
- No missing critical dependencies identified
- Clear PASS/FAIL determination per check

*Log Validation:*
- Required patterns: "Ch5 5.1.1: PASS", "master.xlsx: PASS", "Dependencies validated"
- Forbidden patterns: "ERROR", "FAIL", "missing", "not found"
- Acceptable warnings: None (all dependencies must pass)

**Expected Behavior on Validation Failure:**
Quit immediately with specific missing dependency message, log to logs/step00_validate_dependencies.log

### Step 1: Extract REMEMVR Slopes from Ch5 Output
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Medium (~5 minutes)

**Purpose:** Extract individual participant slopes from Ch5 omnibus LMM analysis

**Input:**
- Primary: results/ch5/5.1.1/data/step06_best_model.pkl (fitted LMM object)
- Alternative: results/ch5/5.1.1/data/step04_lmm_input.csv (for slope extraction)
- Fallback: results/ch5/5.1.1/data/lmm_fitted_*.{pkl,rds,csv} (search pattern)
- Expected content: LMM with random slopes for individual participants

**Processing:**
- Load fitted LMM model object from Ch5 output
- Extract individual participant random slopes (slope component of random effects)
- Create participant-slope mapping: UID -> REMEMVR_Slope
- Slopes represent forgetting rate (negative values = more forgetting)
- Verify N=100 participants with valid slope estimates
- Check for convergence warnings or failed slope estimates
- Standardize slopes for effect size interpretation
- Quality checks: slopes in reasonable range, no extreme outliers
- Export clean slope dataset with participant identifiers

**Output:**
- data/step01_rememvr_slopes.csv (UID, REMEMVR_Slope, slope_se)

**Validation Requirement:**
Validation tools MUST be used after slope extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_rememvr_slopes.csv: 100 rows x 3 columns
- Columns: UID (object), REMEMVR_Slope (float64), slope_se (float64)

*Value Ranges:*
- REMEMVR_Slope in [-2, 2] (standardized forgetting rates)
- slope_se > 0 and < 1.0 (positive standard errors, bounded)
- UID format: consistent with Ch5 participant coding

*Data Quality:*
- Exactly 100 participants (complete sample)
- No missing slope values (all participants converged)
- No duplicate UIDs
- Standard error values reasonable (not inflated)

*Log Validation:*
- Required patterns: "100 slopes extracted", "LMM convergence: success"
- Forbidden patterns: "convergence failed", "ERROR", "missing slopes"
- Acceptable warnings: "boundary (singular) fit" if noted

**Expected Behavior on Validation Failure:**
Log specific slope extraction issue, quit with error message, invoke g_debug for LMM troubleshooting

### Step 2: Extract and Process RAVLT Data
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (<5 minutes)

**Purpose:** Extract RAVLT T5 and Delayed Recall scores, compute forgetting index

**Input:**
- data/cache/master.xlsx (RAVLT columns: RAV_T5Sc, RAV_DRSc)
- Expected format: standardized T-scores (mean=50, sd=10)

**Processing:**
- Load master.xlsx and extract RAVLT columns (RAV_T5Sc, RAV_DRSc)
- Compute RAVLT_Forgetting = RAV_T5Sc - RAV_DRSc
- Higher values = more forgetting (worse delayed vs immediate recall)
- Quality checks: T-scores in reasonable range (20-80), no extreme outliers
- Check for missing data: exclude participants with missing RAVLT scores
- Standardize forgetting index for effect size interpretation
- Verify participant UIDs match Ch5 sample (100 participants expected)
- Create merged participant list for analysis

**Output:**
- data/step02_ravlt_data.csv (UID, RAV_T5Sc, RAV_DRSc, RAVLT_Forgetting, RAVLT_Forgetting_z)

**Validation Requirement:**
Validation tools MUST be used after RAVLT processing execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_ravlt_data.csv: 100 rows x 5 columns
- Columns: UID, RAV_T5Sc, RAV_DRSc, RAVLT_Forgetting, RAVLT_Forgetting_z

*Value Ranges:*
- RAV_T5Sc, RAV_DRSc in [20, 80] (T-score range)
- RAVLT_Forgetting in [-30, 50] (difference in T-scores)
- RAVLT_Forgetting_z in [-3, 3] (standardized scores)

*Data Quality:*
- Complete data for all 100 participants (no missing RAVLT)
- No duplicate UIDs
- Forgetting values mathematically consistent (T5 - Delayed)
- Reasonable distribution (not all identical values)

*Log Validation:*
- Required patterns: "RAVLT data loaded: 100 participants", "Forgetting index computed"
- Forbidden patterns: "missing data", "ERROR", "invalid T-scores"
- Acceptable warnings: None (complete data expected)

**Expected Behavior on Validation Failure:**
Document missing data patterns, proceed with available participants if N >= 95, otherwise quit with insufficient data error

### Step 3: Create Analysis Dataset
**Dependencies:** Steps 1-2 (slopes + RAVLT data)
**Complexity:** Low (<5 minutes)

**Purpose:** Merge REMEMVR slopes with RAVLT data for correlation analysis

**Input:**
- data/step01_rememvr_slopes.csv (individual slopes)
- data/step02_ravlt_data.csv (RAVLT forgetting indices)

**Processing:**
- Merge datasets on UID (inner join to ensure complete data)
- Verify successful merge: target N=100, minimum acceptable N=95
- Create analysis-ready dataset with all required variables
- Compute descriptive statistics for all variables
- Check for extreme multivariate outliers using Mahalanobis distance
- Export clean analysis dataset
- Document final sample size and any exclusions
- Prepare summary statistics table

**Output:**
- data/step03_analysis_input.csv (UID, REMEMVR_Slope, RAVLT_Forgetting, RAVLT_Forgetting_z)
- data/step03_descriptives.csv (variable summaries)

**Validation Requirement:**
Validation tools MUST be used after dataset merging execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_analysis_input.csv: 95-100 rows x 4 columns
- data/step03_descriptives.csv: 3 rows x 6 columns (mean, sd, min, max, skew, kurt)
- Columns in analysis_input: UID, REMEMVR_Slope, RAVLT_Forgetting, RAVLT_Forgetting_z

*Value Ranges:*
- REMEMVR_Slope in [-2, 2] (standardized slopes)
- RAVLT_Forgetting in [-30, 50] (T-score differences)
- Sample size N in [95, 100] (acceptable range)

*Data Quality:*
- Complete data for all included participants
- No missing values in key analysis variables
- Reasonable descriptive statistics (no extreme skew > 3)
- Successful merge documented in logs

*Log Validation:*
- Required patterns: "Merge complete: N=XX participants", "Descriptives computed"
- Forbidden patterns: "merge failed", "ERROR", "insufficient data"
- Acceptable warnings: "N < 100 due to missing data" if documented

**Expected Behavior on Validation Failure:**
Log merge issues, document exclusions, proceed if N >= 95, otherwise quit with insufficient data for analysis

### Step 4: Bivariate Correlation Analysis
**Dependencies:** Step 3 (merged analysis dataset)
**Complexity:** Medium (~5 minutes)

**Purpose:** Compute primary bivariate correlation between RAVLT forgetting and REMEMVR slope

**Input:**
- data/step03_analysis_input.csv (merged correlation dataset)

**Processing:**
- Compute Pearson correlation: r(RAVLT_Forgetting, REMEMVR_Slope)
- Implementation: scipy.stats.pearsonr with complete-case analysis
- Extract correlation coefficient, sample size, degrees of freedom
- Compute 95% confidence interval using Fisher's z-transformation
- Bootstrap confidence intervals for robustness:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Resampling: participant-level with replacement
  - CI method: percentile (2.5th, 97.5th percentiles)
- Compute BOTH uncorrected AND corrected p-values (Decision D068):
  - Uncorrected: standard two-tailed test
  - Bonferroni: alpha = 0.05/28 = 0.00179 (Chapter 7 family)
- Effect size interpretation using Cohen's guidelines:
  - Small: |r| = 0.10, Medium: |r| = 0.30, Large: |r| = 0.50
- Document correlation assumptions (linearity via scatterplot)

**Output:**
- data/step04_bivariate_correlation.csv (r, ci_lower, ci_upper, p_uncorrected, p_bonferroni, n, effect_size)

**Validation Requirement:**
Validation tools MUST be used after correlation computation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_bivariate_correlation.csv: 1 row x 7 columns
- Columns: r, ci_lower, ci_upper, p_uncorrected, p_bonferroni, n, effect_size

*Value Ranges:*
- r in [-1, 1] (valid correlation coefficient)
- ci_lower < r < ci_upper (valid confidence interval)
- p_uncorrected, p_bonferroni in [0, 1] (valid probabilities)
- n in [95, 100] (sample size range)
- effect_size: text ("small", "medium", "large", or "negligible")

*Data Quality:*
- Correlation coefficient not NaN or infinite
- Bootstrap CI successfully computed
- Both p-values computed and reported (Decision D068)
- Confidence interval mathematically valid

*Log Validation:*
- Required patterns: "Correlation computed: r = X.XX", "Bootstrap complete: 1000 iterations"
- Required patterns: "Dual p-values: uncorrected = X.XXX, corrected = X.XXX"
- Forbidden patterns: "ERROR", "NaN correlation", "bootstrap failed"
- Acceptable warnings: "weak correlation detected"

**Expected Behavior on Validation Failure:**
Log correlation computation issue, check for data problems (constant values, extreme outliers), invoke diagnostic procedures

### Step 5: Partial Correlation Analysis
**Dependencies:** Step 4 (bivariate correlation)
**Complexity:** Medium (~5 minutes)

**Purpose:** Compute partial correlation controlling for initial encoding levels

**Input:**
- data/step03_analysis_input.csv (analysis dataset)
- Control variables: RAVLT T5 (initial encoding), REMEMVR intercept (if available)

**Processing:**
- Extract control variables for partial correlation
- For REMEMVR intercept: extract from Ch5 LMM random effects if available
- If intercept unavailable: proceed with RAVLT T5 control only
- Compute partial correlation: r(RAVLT_Forgetting, REMEMVR_Slope | Controls)
- Implementation: pingouin.partial_corr with complete-case analysis
- Bootstrap partial correlation confidence intervals:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Resampling: participant-level with replacement
  - For each iteration: compute partial correlation
  - CI method: percentile (2.5th, 97.5th percentiles)
- Compute BOTH uncorrected AND corrected p-values (Decision D068):
  - Uncorrected: standard partial correlation p-value
  - Bonferroni: alpha = 0.05/28 = 0.00179
- Compare partial vs bivariate correlation magnitudes
- Interpretation: control for encoding quality effects

**Output:**
- data/step05_partial_correlation.csv (r_partial, ci_lower, ci_upper, p_uncorrected, p_bonferroni, controls_used)

**Validation Requirement:**
Validation tools MUST be used after partial correlation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_partial_correlation.csv: 1 row x 6 columns
- Columns: r_partial, ci_lower, ci_upper, p_uncorrected, p_bonferroni, controls_used

*Value Ranges:*
- r_partial in [-1, 1] (valid partial correlation)
- ci_lower < r_partial < ci_upper (valid confidence interval)
- p_uncorrected, p_bonferroni in [0, 1] (valid probabilities)
- controls_used: text description of control variables

*Data Quality:*
- Partial correlation successfully computed
- Bootstrap CI mathematically valid
- Both p-values computed (Decision D068)
- Control variables documented

*Log Validation:*
- Required patterns: "Partial correlation: r = X.XX", "Controls: [variable list]"
- Required patterns: "Bootstrap complete: 1000 iterations"
- Forbidden patterns: "ERROR", "singular matrix", "computation failed"
- Acceptable warnings: "intercept unavailable, using T5 only"

**Expected Behavior on Validation Failure:**
Document control variable issues, attempt analysis with available controls, report limitations in interpretation

### Step 6: Assumption Validation and Diagnostics
**Dependencies:** Steps 4-5 (correlation analyses)
**Complexity:** Medium (~5 minutes)

**Purpose:** Check correlation assumptions and identify potential violations

**Input:**
- data/step03_analysis_input.csv (analysis dataset)
- Correlation results for diagnostic plotting

**Processing:**
- Check linearity assumption:
  - Create scatterplot: RAVLT_Forgetting vs REMEMVR_Slope
  - Visual inspection for non-linear patterns
  - Lowess smooth overlay for trend assessment
- Check normality assumptions:
  - Shapiro-Wilk test on both variables (alpha = 0.05)
  - Q-Q plots for visual assessment
  - Skewness and kurtosis statistics
- Check for outliers:
  - Cook's distance calculation for bivariate relationship
  - Threshold: D > 4/N (where N = sample size)
  - Mahalanobis distance for multivariate outliers
- Homoscedasticity assessment:
  - Residual plots from regression: REMEMVR ~ RAVLT_Forgetting
  - Visual inspection for heteroscedasticity patterns
- Remedial actions if violations detected:
  - Normality violation (p < 0.05): Report bootstrap CIs as primary
  - Outliers detected: Report correlations with/without outliers
  - Non-linearity: Consider Spearman correlation as alternative
- Document all assumption checks with PASS/FAIL status

**Output:**
- data/step06_assumption_checks.csv (test results, p-values, PASS/FAIL status)
- data/step06_outlier_analysis.csv (outlier IDs, Cook's D, Mahalanobis D)

**Validation Requirement:**
Validation tools MUST be used after assumption checking execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_assumption_checks.csv: 4 rows x 4 columns
- Columns: assumption, test_statistic, p_value, status (PASS/FAIL)
- data/step06_outlier_analysis.csv: N rows x 4 columns (one per participant)
- Columns: UID, cooks_d, mahal_d, outlier_flag

*Value Ranges:*
- p_value in [0, 1] (valid test p-values)
- cooks_d >= 0 (Cook's distance non-negative)
- mahal_d >= 0 (Mahalanobis distance non-negative)
- outlier_flag: boolean (TRUE/FALSE)

*Data Quality:*
- All 4 assumptions tested (linearity, normality x2, outliers)
- Cook's D computed for all participants
- Clear PASS/FAIL determination per assumption
- Outlier flags based on objective threshold (4/N)

*Log Validation:*
- Required patterns: "Assumptions checked: 4 tests", "Outliers detected: N cases"
- Required patterns: "Shapiro-Wilk results: [variable] p = X.XXX"
- Forbidden patterns: "ERROR", "test failed", "computation error"
- Acceptable warnings: "normality violated", "outliers detected"

**Expected Behavior on Validation Failure:**
Log specific assumption violation details, document remedial action recommendations, proceed with robust methods

### Step 7: Cross-Validation and Sensitivity Analysis
**Dependencies:** Steps 4-6 (correlations + diagnostics)
**Complexity:** Medium (~5 minutes)

**Purpose:** Assess correlation stability and sensitivity to methodological choices

**Input:**
- data/step03_analysis_input.csv (analysis dataset)
- data/step06_outlier_analysis.csv (outlier identification)

**Processing:**
- Bootstrap stability assessment (additional to Step 4):
  - Compute correlation for each of 1000 bootstrap samples
  - Assess distribution of correlation coefficients
  - Flag if bootstrap distribution is highly skewed or bimodal
  - Compute bias-corrected confidence intervals if needed
- Sensitivity to outliers:
  - Re-compute correlations excluding identified outliers
  - Compare correlation with/without outliers
  - Document change in correlation magnitude and significance
- Alternative correlation methods:
  - Spearman rank correlation (robust to normality violations)
  - Kendall's tau (robust alternative for small samples)
  - Compare Pearson vs non-parametric correlations
- Sensitivity to missing data:
  - If any participants excluded: document impact on correlation
  - Consider multiple imputation if missing data > 5%
- Power analysis for observed effect:
  - Post-hoc power for observed correlation coefficient
  - Minimum detectable correlation for N at 80% power
  - Use: scipy.stats or statsmodels power functions
  - Alpha level: both 0.05 and 0.00179 (corrected)

**Output:**
- data/step07_sensitivity_analysis.csv (correlation comparisons across methods)
- data/step07_power_analysis.csv (power calculations, minimum detectable effects)

**Validation Requirement:**
Validation tools MUST be used after sensitivity analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_sensitivity_analysis.csv: 4 rows x 5 columns
- Columns: method, r, ci_lower, ci_upper, robust_flag
- data/step07_power_analysis.csv: 2 rows x 4 columns (alpha=0.05, alpha=0.00179)
- Columns: alpha, observed_power, min_detectable_r, adequate_power_flag

*Value Ranges:*
- r in [-1, 1] for all correlation methods
- observed_power in [0, 1] (valid power values)
- min_detectable_r in [0, 1] (positive correlation bounds)
- robust_flag: boolean indicating outlier exclusion

*Data Quality:*
- All 4 correlation methods computed (Pearson, Pearson-no-outliers, Spearman, Kendall)
- Power analysis completed for both alpha levels
- Sensitivity results interpretable and consistent
- Bootstrap stability assessment completed

*Log Validation:*
- Required patterns: "Sensitivity analysis: 4 methods", "Power analysis complete"
- Required patterns: "Bootstrap stability: stable/unstable"
- Forbidden patterns: "ERROR", "computation failed", "invalid correlation"
- Acceptable warnings: "low power detected", "unstable bootstrap"

**Expected Behavior on Validation Failure:**
Log sensitivity analysis issues, document method-specific problems, report available results with caveats

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (prerequisite checks)
- data/step01_rememvr_slopes.csv (individual slopes from Ch5)
- data/step02_ravlt_data.csv (RAVLT T5, Delayed, forgetting index)
- data/step03_analysis_input.csv (merged correlation dataset)
- data/step03_descriptives.csv (variable summaries)
- data/step04_bivariate_correlation.csv (primary correlation results)
- data/step05_partial_correlation.csv (controlled correlation results)
- data/step06_assumption_checks.csv (assumption validation results)
- data/step06_outlier_analysis.csv (outlier identification)
- data/step07_sensitivity_analysis.csv (method comparisons)
- data/step07_power_analysis.csv (power calculations)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_slopes.log
- logs/step02_process_ravlt.log
- logs/step03_merge_datasets.log
- logs/step04_bivariate_correlation.log
- logs/step05_partial_correlation.log
- logs/step06_check_assumptions.log
- logs/step07_sensitivity_analysis.log

### Plots (EMPTY until rq_plots runs)
Note: Plot source data will be created in data/ with prefix step##_plot_data_:
- data/step04_plot_data_scatterplot.csv (bivariate relationship)
- data/step06_plot_data_assumptions.csv (diagnostic plots)
- data/step07_plot_data_sensitivity.csv (method comparisons)

### Results (EMPTY until rq_results runs)
Summary markdown will be created by rq_results agent.

---

## Expected Data Formats

### Step-to-Step Transformations
1. Step 0 -> Step 1: Dependency validation enables slope extraction
2. Step 1 -> Step 2: Parallel processing (slopes + RAVLT independent)
3. Step 2 -> Step 3: Merge on UID creates analysis dataset
4. Step 3 -> Step 4: Direct input to correlation analysis
5. Step 4 -> Step 5: Bivariate results inform partial correlation
6. Step 5 -> Step 6: Correlation results enable assumption checking
7. Step 6 -> Step 7: Diagnostic results guide sensitivity analysis

### Column Naming Conventions
- Participant IDs: UID (consistent with Ch5 coding)
- REMEMVR slopes: REMEMVR_Slope (negative = more forgetting)
- RAVLT scores: RAV_T5Sc, RAV_DRSc (standardized T-scores)
- Forgetting index: RAVLT_Forgetting (raw), RAVLT_Forgetting_z (standardized)
- Correlations: r (Pearson), r_partial (partial), r_spearman, r_kendall
- P-values: p_uncorrected, p_bonferroni (Decision D068 compliance)
- Confidence intervals: ci_lower, ci_upper (95% intervals)

### Data Type Constraints
- UID: object (string participant identifiers)
- All numeric variables: float64 (allows missing values as NaN)
- Effect size categories: object (text: "small", "medium", "large", "negligible")
- Boolean flags: bool (outlier_flag, robust_flag, adequate_power_flag)
- Status indicators: object (text: "PASS", "FAIL")

---

## Cross-RQ Dependencies

**Ch5 5.1.1 Dependency (DERIVED data):**
- **Required:** Completed omnibus LMM analysis with individual random slopes
- **Status Check:** results/ch5/5.1.1/status.yaml must show rq_results: success
- **File Patterns:** 
  - Primary: results/ch5/5.1.1/data/step06_best_model.pkl
  - Alternative: results/ch5/5.1.1/data/lmm_fitted_model.rds
  - Fallback: results/ch5/5.1.1/data/*lmm*.{pkl,rds,csv}
- **Content Expected:** LMM object with N=100 participant random slopes
- **Fallback Action:** If Ch5 incomplete, QUIT with dependency error

**Master Data Dependency:**
- **Required:** RAVLT T5 and Delayed Recall scores
- **File:** data/cache/master.xlsx
- **Columns:** RAV_T5Sc, RAV_DRSc (standardized T-scores)
- **Fallback Action:** If missing, QUIT with RAVLT data unavailable error

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
**Validation Focus:** File accessibility and prerequisite completion
- Output file validation: dependency_validation.txt exists with all checks
- Value validation: All checks return PASS status
- Quality validation: Ch5 status confirmed, RAVLT columns present
- Log validation: Required success patterns, no forbidden error patterns

#### Step 1: Extract REMEMVR Slopes
**Validation Focus:** Slope extraction completeness and validity
- Output file validation: slopes CSV with 100 rows x 3 columns
- Value validation: slopes in [-2, 2] range, standard errors positive
- Quality validation: no missing slopes, convergence successful
- Log validation: extraction completion, LMM convergence confirmation

#### Step 2: Extract RAVLT Data
**Validation Focus:** RAVLT data integrity and forgetting index computation
- Output file validation: RAVLT CSV with expected columns and dimensions
- Value validation: T-scores in [20, 80], forgetting index mathematically consistent
- Quality validation: complete data for analysis sample
- Log validation: successful data loading, forgetting computation

#### Step 3: Merge Analysis Dataset
**Validation Focus:** Successful data integration and sample size adequacy
- Output file validation: merged dataset with complete variables
- Value validation: all variables within expected ranges
- Quality validation: adequate sample size (N >= 95), no merge failures
- Log validation: successful merge confirmation

#### Step 4: Bivariate Correlation
**Validation Focus:** Correlation computation accuracy and Decision D068 compliance
- Output file validation: correlation results with all required statistics
- Value validation: correlation in [-1, 1], p-values in [0, 1], valid CIs
- Quality validation: bootstrap completion, dual p-values present
- Log validation: correlation computation success, bootstrap completion

#### Step 5: Partial Correlation
**Validation Focus:** Partial correlation validity with encoding controls
- Output file validation: partial correlation results with control documentation
- Value validation: partial correlation coefficient valid, CIs mathematically sound
- Quality validation: control variables successfully used, bootstrap completed
- Log validation: partial correlation computation, control variable confirmation

#### Step 6: Assumption Validation
**Validation Focus:** Comprehensive assumption checking and outlier identification
- Output file validation: assumption checks with PASS/FAIL status for each test
- Value validation: test statistics and p-values valid, Cook's D non-negative
- Quality validation: all 4 assumptions tested, outlier analysis completed
- Log validation: assumption test completion, outlier detection results

#### Step 7: Sensitivity Analysis
**Validation Focus:** Method comparison completeness and power analysis
- Output file validation: sensitivity results across multiple methods
- Value validation: all correlation methods produce valid coefficients
- Quality validation: power analysis completed, method comparisons interpretable
- Log validation: sensitivity analysis completion, power calculation success

---

## Summary

**Total Steps:** 8 (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** ~25 minutes
**Cross-RQ Dependencies:** Ch5 5.1.1 (required LMM slopes)
**Primary Outputs:** Bivariate and partial correlations with bootstrap CIs
**Validation Coverage:** 100% (all 8 steps have 4-layer validation requirements)

**Key Hypothesis:** Weak positive correlation (r ~ 0.15) between RAVLT forgetting and REMEMVR slope, reflecting consolidation efficiency individual differences across time scales

**Critical Methodological Notes:**
- Decision D068 compliance: dual p-value reporting throughout
- Chapter 7 Bonferroni correction: alpha = 0.05/28 = 0.00179
- Bootstrap CIs provide robustness to normality violations
- Partial correlation controls for encoding quality confounds
- Cross-time scale correlation may be attenuated by different mechanisms
- Power analysis acknowledges limitations for small effect detection

**Statistical Implementation Specifications:**
- Random seed: 42 for all randomized procedures
- Bootstrap iterations: 1000 with participant-level resampling
- Confidence intervals: 95% using percentile method
- Multiple comparisons: Bonferroni family-wise correction
- Assumption violations: bootstrap CIs for normality, outlier sensitivity analysis
- Cross-validation: bootstrap stability assessment across 1000 iterations

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent v5.1.0