# Analysis Plan: RQ 7.4.1 - RAVLT Process-Specific Transfer Validation

**Research Question:** 7.4.1
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

**Analysis Type:** Bivariate correlation analysis with dependent correlation comparison using Steiger's Z-test

**Pipeline:** Process-Specific Transfer Validation
**Steps:** 6 total analysis steps (Step 0: dependency validation + Steps 1-5: analysis)
**Estimated Runtime:** ~25 minutes

**Research Question:**
Does RAVLT (verbal free recall task) show stronger prediction for REMEMVR Free Recall than Recognition, consistent with transfer-appropriate processing theory?

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Chapter-level Bonferroni correction: alpha = 0.00179 (0.05/28 tests)
- Bootstrap sensitivity analysis for robustness
- Steiger's Z-test for dependent correlation comparison

**Theoretical Framework:**
Transfer-Appropriate Processing (TAP) theory predicts stronger correlations between tasks sharing similar cognitive processes. Both RAVLT and REMEMVR Free Recall require generative retrieval, while Recognition relies more on familiarity-based processes.

**Expected Pattern:**
r(RAVLT, FreeRecall) > r(RAVLT, Recognition) with significant Steiger's Z-test supporting process-specificity hypothesis.

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 paradigm outputs exist before proceeding

**Input:**
- Primary: results/ch5/5.3.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.3.2/data/paradigm_theta_estimates.csv
- Fallback pattern: results/ch5/5.3.*/data/*theta*.csv
- Expected: Paradigm-separated theta scores for Free Recall (IFR) and Recognition (IRE)
- Also verify: data/cache/master.xlsx accessible (RAVLT scores)

**Processing:**
- Check Ch5 5.3.x completed successfully (any RQ in series)
- Locate paradigm-specific theta file using search patterns
- Verify file contains columns: UID, paradigm, theta, se
- Verify paradigms include 'IFR' (Free Recall) and 'IRE' (Recognition)
- Check master.xlsx contains RAVLT_Total column
- Log validation results with specific files found

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with dependency status
- Content: File paths found, paradigm counts, RAVLT availability

*Value Ranges:*
- Paradigm count >= 2 (must include IFR and IRE)
- RAVLT_Total present in master.xlsx
- File sizes > 0 bytes (non-empty files)

*Data Quality:*
- Ch5 dependency file exists and readable
- master.xlsx accessible and contains required columns
- No critical missing dependencies

*Log Validation:*
- Required patterns: "Dependencies validated successfully"
- Required patterns: "Found paradigm file:", "RAVLT column verified"
- Forbidden patterns: "ERROR", "MISSING", "dependency not found"

**Expected Behavior on Validation Failure:**
Quit with specific error message indicating missing dependency and suggested actions.

---

### Step 1: Extract and Prepare Cognitive Test Data
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (~5 minutes)

**Purpose:** Extract RAVLT Total scores from master.xlsx and prepare for analysis

**Input:**
- data/cache/master.xlsx (RAVLT cognitive test battery)
- Expected column: RAVLT_Total (raw total score across trials 1-5)

**Processing:**
- Load master.xlsx using pandas.read_excel()
- Extract columns: UID, RAVLT_Total
- Check for missing data: document patterns and counts
- Apply quality checks:
  - RAVLT_Total in expected range [0, 75] (15 words x 5 trials max)
  - No negative values
  - Reasonable distribution (check for floor/ceiling effects)
- Test normality using Shapiro-Wilk test (p>0.05 for normality)
- Document descriptive statistics: mean, SD, min, max, skewness
- Flag outliers using z-score threshold (|z| > 3.0)
- Missing data strategy: Complete case analysis, document exclusions

**Output:**
- data/step01_ravlt_scores.csv (UID, RAVLT_Total, z_score, outlier_flag)
- data/step01_ravlt_diagnostics.txt (descriptives, normality test, missing data summary)

**Validation Requirement:**
Validation tools MUST be used after cognitive test extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_ravlt_scores.csv: 100 rows x 4 columns (UID, RAVLT_Total, z_score, outlier_flag)
- data/step01_ravlt_diagnostics.txt: text file with descriptive statistics

*Value Ranges:*
- RAVLT_Total in [0, 75] (valid RAVLT score range)
- z_score in [-4, 4] (reasonable standardized range)
- outlier_flag: 0 or 1 (binary indicator)

*Data Quality:*
- All 100 UIDs present with no duplicates
- Missing RAVLT data < 5% of sample
- Mean RAVLT_Total in [35, 55] (expected healthy adult range)
- Standard deviation in [8, 15] (reasonable variability)

*Log Validation:*
- Required patterns: "RAVLT extraction complete"
- Required patterns: "Normality test: W=", "Missing data: N="
- Forbidden patterns: "ERROR", "invalid scores", "extraction failed"

**Expected Behavior on Validation Failure:**
Log specific validation failure, document in diagnostics file, proceed with available data if >95% complete.

---

### Step 2: Extract and Prepare Paradigm Theta Scores
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Medium (~8 minutes including aggregation)

**Purpose:** Extract and aggregate paradigm-specific theta scores for Free Recall and Recognition

**Input:**
- Ch5 paradigm theta file (identified in Step 0)
- Expected format: UID, test, paradigm, item_id, theta, se

**Processing:**
- Load paradigm theta file using pandas.read_csv()
- Filter to required paradigms:
  - IFR: Free Recall paradigm
  - IRE: Recognition paradigm
- Aggregate theta scores by participant and paradigm:
  - Method: Mean theta across all items within paradigm
  - Weighted by inverse standard error if SE column available
  - Handle multiple tests: average across T1-T4 test sessions
- Quality checks:
  - Theta scores in expected range [-3, 3] (IRT ability scale)
  - Standard errors in (0, 1] (positive and bounded)
  - Sufficient data per participant (>=5 items per paradigm)
- Test normality of aggregated theta scores using Shapiro-Wilk
- Flag participants with extreme theta scores (|z| > 3.0)
- Document missing paradigm data patterns

**Output:**
- data/step02_paradigm_theta.csv (UID, theta_FreeRecall, theta_Recognition, n_items_FR, n_items_RE)
- data/step02_theta_diagnostics.txt (descriptives by paradigm, normality tests, aggregation summary)

**Validation Requirement:**
Validation tools MUST be used after paradigm theta extraction and aggregation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_paradigm_theta.csv: 100 rows x 5 columns
- Columns: UID, theta_FreeRecall, theta_Recognition, n_items_FR, n_items_RE
- data/step02_theta_diagnostics.txt: aggregation summary and diagnostics

*Value Ranges:*
- theta_FreeRecall in [-3, 3] (IRT ability scale bounds)
- theta_Recognition in [-3, 3] (IRT ability scale bounds)
- n_items_FR >= 5, n_items_RE >= 5 (minimum items per paradigm)

*Data Quality:*
- All 100 participants have both paradigm theta scores
- No missing theta values (NaN not allowed)
- Theta correlation between paradigms in [0.3, 0.8] (related but distinct)
- Item counts reasonable (typically 20-40 per paradigm)

*Log Validation:*
- Required patterns: "Paradigm aggregation complete"
- Required patterns: "Free Recall: N=100", "Recognition: N=100"
- Required patterns: "Normality test - FR:", "Normality test - RE:"
- Forbidden patterns: "ERROR", "aggregation failed", "insufficient data"

**Expected Behavior on Validation Failure:**
Report specific aggregation issues, document participants with insufficient data, proceed if >95% have complete paradigm data.

---

### Step 3: Merge Datasets and Compute Correlations
**Dependencies:** Steps 1-2 (RAVLT and paradigm theta data)
**Complexity:** Medium (~8 minutes including assumption testing)

**Purpose:** Merge RAVLT and theta data, compute bivariate correlations with assumption testing

**Input:**
- data/step01_ravlt_scores.csv (RAVLT Total scores)
- data/step02_paradigm_theta.csv (paradigm-specific theta scores)

**Processing:**
- Merge datasets on UID using inner join (complete cases only)
- Document final sample size and any exclusions
- Check correlation assumptions:
  - Normality: Shapiro-Wilk test for RAVLT_Total, theta_FreeRecall, theta_Recognition
  - Linearity: Visual inspection via scatter plots (logged for diagnostics)
  - Independence: Verified by study design (between-participant analysis)
  - Outliers: Mahalanobis distance > chi-square critical value
- Compute primary correlations:
  - r1 = pearson(RAVLT_Total, theta_FreeRecall)
  - r2 = pearson(RAVLT_Total, theta_Recognition)
  - Also compute Spearman correlations as robustness check
- Bootstrap 95% confidence intervals:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - CI: Percentile method (2.5th, 97.5th percentiles)
- Apply multiple comparison correction:
  - Family: Within-RQ (2 correlations)
  - Bonferroni: alpha = 0.00179/2 = 0.000895 per test
  - Report BOTH uncorrected AND corrected p-values (Decision D068)

**Output:**
- data/step03_merged_data.csv (UID, RAVLT_Total, theta_FreeRecall, theta_Recognition, outlier_flag)
- data/step03_correlation_results.csv (correlation_type, r_value, ci_lower, ci_upper, p_uncorrected, p_bonferroni, method)
- data/step03_assumption_diagnostics.txt (normality tests, linearity assessment, outlier detection)

**Validation Requirement:**
Validation tools MUST be used after correlation analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_merged_data.csv: N rows x 5 columns (where N>=95)
- data/step03_correlation_results.csv: 4 rows x 7 columns (Pearson + Spearman for both correlations)
- data/step03_assumption_diagnostics.txt: assumption test results

*Value Ranges:*
- r_value in [-1, 1] (valid correlation range)
- ci_lower, ci_upper in [-1, 1] with ci_lower < r_value < ci_upper
- p_uncorrected, p_bonferroni in [0, 1]
- Sample size N >= 95 (allow up to 5% missing data)

*Data Quality:*
- Both correlations computed successfully
- Bootstrap CIs do not include impossible values (outside [-1,1])
- Bonferroni p-values = uncorrected p-values x 2
- Assumption tests completed without errors

*Log Validation:*
- Required patterns: "Correlations computed successfully"
- Required patterns: "Bootstrap CIs: 1000 iterations"
- Required patterns: "Assumption testing complete"
- Forbidden patterns: "ERROR", "correlation failed", "bootstrap error"

**Expected Behavior on Validation Failure:**
Report specific correlation computation failures, use alternative methods if assumption violations detected, document all remedial actions taken.

---

### Step 4: Steiger's Z-test for Dependent Correlations
**Dependencies:** Step 3 (correlation results)
**Complexity:** Medium (~5 minutes)

**Purpose:** Test process-specificity hypothesis using Steiger's Z-test for dependent correlations

**Input:**
- data/step03_correlation_results.csv (correlation coefficients and CIs)
- data/step03_merged_data.csv (raw data for Steiger test computation)

**Processing:**
- Extract correlations:
  - r12 = cor(RAVLT, theta_FreeRecall)
  - r13 = cor(RAVLT, theta_Recognition)  
  - r23 = cor(theta_FreeRecall, theta_Recognition)
- Implement Steiger's Z-test for dependent correlations:
  - H0: r12 = r13 (no difference in correlations)
  - H1: r12 > r13 (Free Recall shows stronger correlation)
  - Formula: Z = (r12 - r13) * sqrt((n-1)(1+r23)) / sqrt(2(1-r12²-r13²-r23²+2*r12*r13*r23))
- Bootstrap the correlation difference:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Resample participants with replacement
  - Compute r12-r13 for each iteration
  - 95% CI for difference using percentile method
- Effect size calculation:
  - Correlation difference: r12 - r13
  - Cohen's q transformation for effect size interpretation
- Statistical decisions:
  - Primary alpha: 0.05 for Steiger test (standard for difference test)
  - Effect size threshold: |difference| > 0.10 for meaningful difference
  - Bootstrap CI exclusion of zero as confirmation

**Output:**
- data/step04_steiger_test.csv (Z_statistic, p_value, correlation_difference, effect_size_q)
- data/step04_bootstrap_difference.csv (iteration, correlation_difference)
- data/step04_process_specificity_summary.txt (interpretation and statistical decision)

**Validation Requirement:**
Validation tools MUST be used after Steiger's Z-test execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_steiger_test.csv: 1 row x 4 columns (test results)
- data/step04_bootstrap_difference.csv: 1000 rows x 2 columns (bootstrap results)
- data/step04_process_specificity_summary.txt: text summary of findings

*Value Ranges:*
- Z_statistic: reasonable range [-5, 5] for correlation difference test
- p_value in [0, 1] (valid probability)
- correlation_difference in [-2, 2] (difference of correlations)
- Bootstrap difference 95% CI computed correctly

*Data Quality:*
- Steiger test computed without numerical errors
- Bootstrap completed all 1000 iterations
- Effect size interpretation included in summary
- Statistical decision clearly stated (reject/fail to reject H0)

*Log Validation:*
- Required patterns: "Steiger test completed"
- Required patterns: "Bootstrap difference: 1000 iterations"
- Required patterns: "Statistical decision:"
- Forbidden patterns: "ERROR", "numerical instability", "test failed"

**Expected Behavior on Validation Failure:**
Report Steiger test computation issues, use alternative approaches (permutation test) if numerical problems, document all computational decisions.

---

### Step 5: Visualization and Sensitivity Analysis
**Dependencies:** Steps 3-4 (correlations and Steiger test)
**Complexity:** Low (~5 minutes)

**Purpose:** Create visualizations and conduct sensitivity analyses for robustness

**Input:**
- data/step03_merged_data.csv (analysis dataset)
- data/step03_correlation_results.csv (correlation results)
- data/step04_steiger_test.csv (process-specificity test results)

**Processing:**
- Create scatter plots for visualization:
  - Plot 1: RAVLT vs theta_FreeRecall with regression line and 95% CI
  - Plot 2: RAVLT vs theta_Recognition with regression line and 95% CI
  - Save plot data CSVs for rq_plots agent
- Sensitivity analyses:
  - Outlier exclusion: Remove outliers (|z|>3) and recompute correlations
  - Spearman alternative: Use rank correlations if normality violated
  - Restriction of range check: Document RAVLT score range and variance
- Generate summary statistics:
  - Descriptive statistics for all variables
  - Sample characteristics for results interpretation
  - Missing data summary and handling decisions
- Create interpretation summary:
  - Process-specificity hypothesis support/rejection
  - Effect size interpretation using Cohen's conventions
  - Clinical/practical significance assessment
  - Limitations and future directions

**Output:**
- data/step05_scatter_plot_data_FR.csv (plot data for RAVLT vs Free Recall)
- data/step05_scatter_plot_data_RE.csv (plot data for RAVLT vs Recognition)
- data/step05_sensitivity_analysis.csv (alternative correlation results)
- data/step05_descriptive_summary.csv (sample characteristics)
- data/step05_interpretation_summary.txt (findings interpretation)

**Validation Requirement:**
Validation tools MUST be used after visualization and sensitivity analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_scatter_plot_data_FR.csv: N rows x 3 columns (x, y, fitted_y)
- data/step05_scatter_plot_data_RE.csv: N rows x 3 columns (x, y, fitted_y)
- data/step05_sensitivity_analysis.csv: M rows x 6 columns (sensitivity results)
- data/step05_descriptive_summary.csv: 3 rows x 8 columns (variable summaries)
- data/step05_interpretation_summary.txt: text interpretation

*Value Ranges:*
- Plot data x-values (RAVLT) in observed range
- Plot data y-values (theta) in [-3, 3] range
- fitted_y values within reasonable regression bounds
- Sensitivity correlations in [-1, 1] range

*Data Quality:*
- Plot data contains all analysis participants
- Sensitivity analyses completed without errors
- Interpretation summary addresses key findings
- All output files properly formatted and complete

*Log Validation:*
- Required patterns: "Visualization data prepared"
- Required patterns: "Sensitivity analysis complete"
- Required patterns: "Interpretation summary generated"
- Forbidden patterns: "ERROR", "plotting failed", "analysis incomplete"

**Expected Behavior on Validation Failure:**
Report specific visualization or sensitivity analysis failures, generate alternative plot formats if needed, ensure interpretation summary always created.

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (dependency check results)
- data/step01_ravlt_scores.csv (extracted RAVLT data with diagnostics)
- data/step01_ravlt_diagnostics.txt (RAVLT descriptives and quality checks)
- data/step02_paradigm_theta.csv (aggregated paradigm-specific theta scores)
- data/step02_theta_diagnostics.txt (theta aggregation summary)
- data/step03_merged_data.csv (final analysis dataset)
- data/step03_correlation_results.csv (primary correlation analysis)
- data/step03_assumption_diagnostics.txt (assumption testing results)
- data/step04_steiger_test.csv (dependent correlation comparison)
- data/step04_bootstrap_difference.csv (bootstrap sensitivity for difference)
- data/step04_process_specificity_summary.txt (Steiger test interpretation)
- data/step05_scatter_plot_data_FR.csv (Free Recall visualization data)
- data/step05_scatter_plot_data_RE.csv (Recognition visualization data)
- data/step05_sensitivity_analysis.csv (outlier and alternative method results)
- data/step05_descriptive_summary.csv (sample characteristics)
- data/step05_interpretation_summary.txt (overall findings interpretation)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_ravlt.log
- logs/step02_extract_paradigm_theta.log
- logs/step03_compute_correlations.log
- logs/step04_steiger_test.log
- logs/step05_visualization_sensitivity.log

### Plots (EMPTY until rq_plots runs)
- Plot source CSVs created in data/ folder for:
  - RAVLT vs Free Recall scatter plot with regression line
  - RAVLT vs Recognition scatter plot with regression line
  - Correlation comparison visualization

### Results (EMPTY until rq_results runs)
- summary.md will be created by rq_results agent

---

## Expected Data Formats

### Step-to-Step Transformations
1. **Step 0 -> Step 1:** Dependency validation enables RAVLT extraction from master.xlsx
2. **Step 0 -> Step 2:** Ch5 file location enables paradigm theta extraction and aggregation
3. **Steps 1,2 -> Step 3:** RAVLT and theta data merge for correlation analysis
4. **Step 3 -> Step 4:** Correlation coefficients feed into Steiger's dependent correlation test
5. **Steps 3,4 -> Step 5:** All results combine for visualization and sensitivity analysis

### Column Naming Conventions
- **UID:** Participant identifier (consistent across all files)
- **RAVLT_Total:** Raw total score across RAVLT trials 1-5
- **theta_FreeRecall:** Mean IRT theta for Free Recall paradigm items
- **theta_Recognition:** Mean IRT theta for Recognition paradigm items
- **r_value:** Pearson correlation coefficient
- **p_uncorrected:** Raw p-value before multiple comparison correction
- **p_bonferroni:** Bonferroni-corrected p-value (Decision D068)

### Data Type Constraints
- **UID:** object (string identifier)
- **RAVLT_Total:** int64, non-negative, range [0, 75]
- **theta_*:** float64, nullable=False, range [-3, 3]
- **r_value:** float64, range [-1, 1]
- **p_*:** float64, range [0, 1]
- **outlier_flag:** int64, binary {0, 1}

---

## Cross-RQ Dependencies

**Primary Dependency:** Ch5 5.3.x (Paradigm-specific IRT analyses)
- **Required Output:** Paradigm-separated theta estimates for Free Recall (IFR) and Recognition (IRE)
- **File Pattern:** results/ch5/5.3.*/data/*theta*.csv
- **Expected Format:** UID, test, paradigm, item_id, theta, se
- **Fallback Strategy:** Try multiple Ch5 5.3.x RQs (5.3.1, 5.3.2, 5.3.3) in sequence
- **Critical Requirements:** Must contain both 'IFR' and 'IRE' paradigm codes

**Secondary Dependency:** Master cognitive test data
- **Required File:** data/cache/master.xlsx
- **Expected Content:** RAVLT_Total column with raw scores
- **No Fallback:** This is primary data source, must be accessible

**Dependency Validation Strategy:**
- Step 0 explicitly validates all dependencies before proceeding
- Flexible file discovery using pattern matching
- Clear error messages if dependencies unavailable
- No execution proceeds without confirmed dependencies

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
**4-Layer Validation Structure:**
- Output Files: dependency_validation.txt with file paths and status
- Value Ranges: File sizes > 0, required columns present
- Data Quality: All critical dependencies available and readable
- Log Validation: Success patterns required, error patterns forbidden

#### Step 1: Extract RAVLT Data
**4-Layer Validation Structure:**
- Output Files: ravlt_scores.csv (100x4) + diagnostics.txt
- Value Ranges: RAVLT_Total [0,75], z_score [-4,4]
- Data Quality: All UIDs present, <5% missing, mean in [35,55]
- Log Validation: Extraction success, normality test results, missing data counts

#### Step 2: Extract Paradigm Theta
**4-Layer Validation Structure:**
- Output Files: paradigm_theta.csv (100x5) + diagnostics.txt
- Value Ranges: theta_* [-3,3], n_items >= 5
- Data Quality: All paradigm theta scores present, reasonable correlation between paradigms
- Log Validation: Aggregation success, normality tests, item counts

#### Step 3: Compute Correlations
**4-Layer Validation Structure:**
- Output Files: merged_data.csv (95+x5), correlation_results.csv (4x7), diagnostics.txt
- Value Ranges: r_value [-1,1], CIs valid, p_values [0,1]
- Data Quality: Bootstrap CIs exclude impossible values, dual p-value reporting
- Log Validation: Correlation success, bootstrap completion, assumption testing

#### Step 4: Steiger's Z-test
**4-Layer Validation Structure:**
- Output Files: steiger_test.csv (1x4), bootstrap_difference.csv (1000x2), summary.txt
- Value Ranges: Z_statistic reasonable, correlation_difference [-2,2]
- Data Quality: Test computed successfully, bootstrap completed, decision stated
- Log Validation: Test completion, bootstrap iterations, statistical decision

#### Step 5: Visualization and Sensitivity
**4-Layer Validation Structure:**
- Output Files: Multiple plot data CSVs, sensitivity_analysis.csv, summaries
- Value Ranges: Plot coordinates within observed ranges, sensitivity results valid
- Data Quality: All visualizations prepared, sensitivity analyses complete
- Log Validation: Visualization success, sensitivity completion, interpretation generated

---

## Summary

**Total Steps:** 6 (Step 0: validation + Steps 1-5: analysis)
**Estimated Runtime:** ~25 minutes
**Cross-RQ Dependencies:** Ch5 5.3.x paradigm theta estimates + master.xlsx RAVLT data
**Primary Outputs:** Correlation analysis with process-specificity test, visualization data, interpretation summary
**Validation Coverage:** 100% (all 6 steps have 4-layer validation requirements)

**Key Hypothesis:** r(RAVLT, FreeRecall) > r(RAVLT, Recognition) supporting transfer-appropriate processing theory

**Critical Methodological Notes:**
- Uses Steiger's Z-test for dependent correlations (gold standard method)
- Chapter-level Bonferroni correction (alpha=0.00179) for multiple testing control
- Bootstrap sensitivity analysis with 1000 iterations for robustness
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Complete assumption testing with remedial actions for violations
- Flexible dependency resolution with fallback patterns

**Statistical Specifications Compliance:**
- Random seed: 42 for all bootstrap procedures
- Cross-validation: Not applicable (correlation analysis)
- Bootstrap: 1000 iterations, participant-level resampling, percentile CIs
- Power analysis: Post-hoc power adequate with N=100 for correlation differences
- Multiple comparisons: Within-RQ Bonferroni correction applied
- Remedial actions: Spearman correlations if normality violated, outlier sensitivity

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent v5.1 with enhanced statistical specifications