# Analysis Plan: RQ 7.2.4 - VR Scaffolding Validation

**Research Question:** 7.2.4
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

**Analysis Type:** Cross-sectional correlation comparison with dependent correlation testing (Steiger's Z-test)

**Research Question:** Does REMEMVR show age-invariance while RAVLT shows age decline in the same sample? This formally tests the VR scaffolding hypothesis by comparing age-related decline patterns between traditional (RAVLT) and VR-based (REMEMVR) episodic memory testing.

**Pipeline:** Bivariate correlations + Steiger's Z-test for dependent correlation comparison
**Steps:** 8 total analysis steps (Step 0: dependency validation + Steps 1-7: analysis pipeline)
**Estimated Runtime:** ~25 minutes total

**Theoretical Framework:** STAC theory predicts VR provides environmental scaffolding that attenuates age-related episodic memory decline compared to traditional list learning (RAVLT).

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 outputs and master.xlsx access before proceeding with analysis

**Input:**
- Primary: results/ch5/5.1.1/status.yaml (verify rq_results: success)
- Alternative: results/ch5/5.1.1/data/step03_theta_scores.csv
- Fallback pattern: results/ch5/5.1.1/data/*theta*.csv
- Master data: data/cache/master.xlsx
- Expected Ch5 content: REMEMVR omnibus theta estimates for 100 participants
- If Ch5 outputs not found: QUIT with "Ch5 5.1.1 theta outputs not found"

**Processing:**
- Check Ch5 5.1.1 status.yaml shows rq_results: success
- Locate theta score file using multiple patterns
- Verify file contains 100 participants with theta_all scores
- Test master.xlsx accessibility and RAVLT column presence
- Log validation results with specific file paths found
- Document dependency status for downstream steps

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file documenting all dependency checks
- Contains: Ch5 file paths found, master.xlsx status, participant counts

*Value Ranges:*
- Participant count must equal 100 (full sample)
- Ch5 status must show "success" for required agents

*Data Quality:*
- All required files accessible
- No permission or path errors
- Dependencies complete before proceeding

*Log Validation:*
- Required pattern: "Ch5 dependency validation: PASS"
- Required pattern: "Master.xlsx accessible: PASS"
- Forbidden patterns: "ERROR", "not found", "permission denied"

**Expected Behavior on Validation Failure:**
Raise error with specific missing dependency, log to logs/step00_validate_dependencies.log, quit immediately

---

### Step 1: Extract RAVLT and Demographics Data
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (<3 minutes)

**Purpose:** Extract RAVLT total scores and age data from master.xlsx for 100 participants

**Input:**
- data/cache/master.xlsx (demographics and RAVLT scores)
- Expected sheets: participant demographics, cognitive test scores
- Required columns: UID, Age, RAVLT_Total (or equivalent RAVLT composite)

**Processing:**
- Load master.xlsx using pandas.read_excel()
- Extract participant UIDs, Age, and RAVLT total scores
- Handle multiple sheet structure if necessary (try demographics + cognitive sheets)
- Clean age data (convert to numeric, check for missing values)
- Clean RAVLT data (verify scoring range, identify missing values)
- Standardize UIDs to match Ch5 format
- Report descriptive statistics: Age (mean, SD, range), RAVLT (mean, SD, range)
- Check for ceiling/floor effects in RAVLT (>95th percentile or <5th percentile)
- Exclude participants with missing RAVLT or Age data (document exclusions)

**Output:**
- data/step01_ravlt_demographics.csv (UID, Age, RAVLT_Total, Include_Flag)
- data/step01_descriptives.txt (Age and RAVLT descriptive statistics)

**Validation Requirement:**
Validation tools MUST be used after data extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_ravlt_demographics.csv: ~100 rows x 4 columns
- Columns: UID (object), Age (float64), RAVLT_Total (float64), Include_Flag (bool)
- data/step01_descriptives.txt: text file with summary statistics

*Value Ranges:*
- Age: 20-70 years (REMEMVR study range)
- RAVLT_Total: 0-75 points (typical RAVLT scoring range)
- Include_Flag: True for participants with complete data

*Data Quality:*
- Missing data rate <5% for Age and RAVLT combined
- No duplicate UIDs
- Age and RAVLT distributions approximately normal (visual check)

*Log Validation:*
- Required pattern: "RAVLT extraction complete: N participants"
- Required pattern: "Age range: XX-YY years"
- Forbidden patterns: "ERROR", "missing sheet", "column not found"

**Expected Behavior on Validation Failure:**
Log data quality issues, continue with available data if >90% complete, raise error if <90% complete

---

### Step 2: Extract REMEMVR Theta Scores
**Dependencies:** Step 1 (RAVLT data extracted)
**Complexity:** Low (<3 minutes)

**Purpose:** Load omnibus REMEMVR theta scores from Ch5 5.1.1 outputs

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/final_theta_estimates.csv
- Fallback pattern: results/ch5/5.1.1/data/*theta*.csv
- Expected content: UID column + theta_all (omnibus scores across T1-T4)

**Processing:**
- Load Ch5 theta file using pandas.read_csv()
- Verify contains theta_all column (omnibus scores across What/Where/When domains)
- Extract UID and theta_all for all 100 participants
- Report theta descriptive statistics: mean, SD, range, distribution shape
- Check for extreme theta values (|theta| > 3 suggests measurement issues)
- Standardize UIDs to match RAVLT data format
- Flag any participants missing from RAVLT data
- Compute theta z-scores for standardized comparison to RAVLT

**Output:**
- data/step02_rememvr_theta.csv (UID, theta_all, theta_z, Include_Flag)
- data/step02_theta_descriptives.txt (theta distribution summary)

**Validation Requirement:**
Validation tools MUST be used after theta extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_rememvr_theta.csv: 100 rows x 4 columns
- Columns: UID (object), theta_all (float64), theta_z (float64), Include_Flag (bool)
- data/step02_theta_descriptives.txt: text file with IRT theta summary

*Value Ranges:*
- theta_all: -3 to +3 (IRT ability scale bounds)
- theta_z: standardized scores (mean ~0, SD ~1)
- Include_Flag: True for participants with valid theta scores

*Data Quality:*
- All 100 participants present (no missing theta scores)
- theta_all distribution approximately normal
- No extreme outliers (|theta| > 4 would suggest IRT model issues)

*Log Validation:*
- Required pattern: "Theta extraction complete: 100 participants"
- Required pattern: "Theta range: [-X.X, +X.X]"
- Forbidden patterns: "ERROR", "missing file", "IRT convergence"

**Expected Behavior on Validation Failure:**
Raise error if theta file missing or <95% complete, log theta distribution warnings for review

---

### Step 3: Merge and Prepare Analysis Dataset
**Dependencies:** Steps 1-2 (RAVLT + REMEMVR data extracted)
**Complexity:** Low (<3 minutes)

**Purpose:** Combine RAVLT and REMEMVR data into single analysis dataset with complete cases

**Input:**
- data/step01_ravlt_demographics.csv (RAVLT scores and age)
- data/step02_rememvr_theta.csv (REMEMVR theta scores)

**Processing:**
- Merge datasets on UID using pandas.merge (inner join)
- Verify successful merge for expected number of participants
- Create final analysis flags: Include_Analysis = complete data for both measures
- Standardize both outcome measures (Age remains as-is for correlation interpretation)
  - RAVLT_z: z-score transformation of RAVLT_Total
  - theta_z: already computed in Step 2
- Compute pairwise correlation between RAVLT and REMEMVR (for model checking)
- Document final analysis sample size and any exclusions
- Check for systematic differences between included/excluded participants

**Output:**
- data/step03_analysis_dataset.csv (merged data for correlation analysis)
- data/step03_merge_summary.txt (merge results and sample composition)

**Validation Requirement:**
Validation tools MUST be used after data merging execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_analysis_dataset.csv: ~100 rows x 8 columns
- Columns: UID, Age, RAVLT_Total, RAVLT_z, theta_all, theta_z, Include_Analysis
- data/step03_merge_summary.txt: merge diagnostics and sample summary

*Value Ranges:*
- Age: 20-70 years (preserved from original)
- RAVLT_z and theta_z: standardized (mean ~0, SD ~1)
- Include_Analysis: Boolean flag for complete cases

*Data Quality:*
- Analysis sample >=95 participants (allowing <5% exclusions)
- No missing values for included participants
- RAVLT-REMEMVR correlation magnitude <0.80 (discriminant validity)

*Log Validation:*
- Required pattern: "Merge complete: N participants in final analysis"
- Required pattern: "RAVLT-REMEMVR correlation: r = X.XX"
- Forbidden patterns: "merge failed", "duplicate keys", "ERROR"

**Expected Behavior on Validation Failure:**
Raise error if final analysis sample <95 participants, log correlation warnings if r > 0.80

---

### Step 4: Compute Age-Correlation Statistics
**Dependencies:** Step 3 (analysis dataset prepared)
**Complexity:** Medium (~8 minutes including bootstrap)

**Purpose:** Calculate age correlations with RAVLT and REMEMVR using Pearson correlation with bootstrap confidence intervals

**Input:**
- data/step03_analysis_dataset.csv (complete analysis dataset)

**Processing:**
- Compute primary age correlations using scipy.stats.pearsonr:
  - r(Age, RAVLT_Total): Age correlation with traditional episodic memory
  - r(Age, theta_all): Age correlation with VR episodic memory
- Calculate 95% confidence intervals using Fisher's Z transformation
- Bootstrap confidence intervals for robustness:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - CI computation: percentile method (2.5th, 97.5th percentiles)
- Multiple comparison correction:
  - Family: Within-RQ (2 primary correlations)
  - Bonferroni: alpha = 0.05/2 = 0.025 per test
  - Also compute FDR using Benjamini-Hochberg
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Test statistical assumptions:
  - Linearity: Visual inspection via scatterplots
  - Normality: Shapiro-Wilk test on age and outcome variables
  - Homoscedasticity: Residual plots from linear regression
- Remedial actions if assumptions violated:
  - Normality p < 0.05: Report bootstrap CIs as primary
  - Non-linearity detected: Add Spearman correlation as sensitivity analysis
  - Extreme outliers: Report correlations with and without outliers

**Output:**
- data/step04_age_correlations.csv (correlation results with CIs)
- data/step04_bootstrap_cis.csv (bootstrap confidence intervals)
- data/step04_assumption_checks.txt (normality and linearity tests)

**Validation Requirement:**
Validation tools MUST be used after correlation computation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_age_correlations.csv: 2 rows x 8 columns
- Columns: measure, r, p_uncorrected, p_bonferroni, p_fdr, ci_lower, ci_upper, n
- data/step04_bootstrap_cis.csv: 2 rows x 4 columns (measure, r_bootstrap, ci_lower_boot, ci_upper_boot)

*Value Ranges:*
- Correlation coefficients: -1 to +1
- p-values: 0 to 1 (uncorrected and corrected)
- Confidence intervals: must bracket correlation point estimate

*Data Quality:*
- Both correlations successfully computed (no convergence failures)
- Bootstrap CIs overlap with analytical CIs (consistency check)
- Expected pattern: RAVLT shows negative age correlation, REMEMVR near zero

*Log Validation:*
- Required pattern: "Age correlations computed: RAVLT r = X.XX, REMEMVR r = X.XX"
- Required pattern: "Bootstrap complete: 1000 iterations"
- Forbidden patterns: "correlation failed", "bootstrap error", "ERROR"

**Expected Behavior on Validation Failure:**
Raise error if correlations cannot be computed, log assumption violation warnings for interpretation

---

### Step 5: Steiger's Z-Test for Dependent Correlation Comparison
**Dependencies:** Step 4 (age correlations computed)
**Complexity:** Medium (~5 minutes)

**Purpose:** Test whether age-related decline differs significantly between RAVLT and REMEMVR using Steiger's Z-test for dependent correlations

**Input:**
- data/step04_age_correlations.csv (age correlation results)
- data/step03_analysis_dataset.csv (raw data for correlation matrix)

**Processing:**
- Extract correlation values: r_age_ravlt, r_age_rememvr, r_ravlt_rememvr
- Implement Steiger's Z-test using tools.analysis_ctt.compare_correlations_dependent:
  - Test: H0: |r_age_ravlt| = |r_age_rememvr|
  - Alternative: H1: |r_age_ravlt| > |r_age_rememvr| (one-tailed, theoretical prediction)
- Calculate Z-statistic using Steiger (1980) formula
- Compute p-value for correlation difference test
- Calculate effect size for correlation difference:
  - Raw difference: |r_age_ravlt| - |r_age_rememvr|
  - Standardized difference with confidence interval
- Bootstrap validation of Steiger's test:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - For each iteration: resample participants, compute correlations, perform Steiger test
  - Generate distribution of Z-statistics for robustness check
- Interpret results in theoretical context:
  - Significant difference (p < 0.05) supports VR scaffolding hypothesis
  - Effect size magnitude indicates practical significance

**Output:**
- data/step05_steiger_test.csv (Steiger's Z-test results)
- data/step05_effect_sizes.csv (correlation difference effect sizes)
- data/step05_bootstrap_steiger.csv (bootstrap distribution of Z-statistics)

**Validation Requirement:**
Validation tools MUST be used after Steiger's test execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_steiger_test.csv: 1 row x 6 columns
- Columns: Z_statistic, p_value, r_diff, direction, n, significance
- data/step05_effect_sizes.csv: effect size metrics for correlation difference

*Value Ranges:*
- Z_statistic: typically -5 to +5 (extreme values suggest computation error)
- p_value: 0 to 1 (one-tailed test)
- r_diff: difference in correlation magnitudes

*Data Quality:*
- Steiger test successfully computed (no mathematical errors)
- Bootstrap distribution normal around observed Z-statistic
- Theoretical prediction supported: RAVLT > REMEMVR age decline

*Log Validation:*
- Required pattern: "Steiger's Z-test complete: Z = X.XX, p = X.XXX"
- Required pattern: "Correlation difference: r_diff = X.XX"
- Forbidden patterns: "mathematical error", "invalid correlation", "ERROR"

**Expected Behavior on Validation Failure:**
Raise error if Steiger test cannot be computed due to invalid correlation matrix, log interpretation warnings

---

### Step 6: Diagnostic Plots and Assumption Testing
**Dependencies:** Step 5 (Steiger's test completed)
**Complexity:** Medium (~4 minutes)

**Purpose:** Generate diagnostic visualizations and conduct comprehensive assumption testing for correlation analysis

**Input:**
- data/step03_analysis_dataset.csv (analysis data)
- data/step04_age_correlations.csv (correlation results)

**Processing:**
- Create diagnostic scatterplots:
  - Age vs RAVLT_Total with regression line and 95% CI
  - Age vs theta_all with regression line and 95% CI
  - Side-by-side comparison plot highlighting correlation differences
- Test correlation assumptions systematically:
  - Linearity: Visual inspection + residual plots from age regression
  - Normality: Shapiro-Wilk tests for Age, RAVLT_Total, theta_all
  - Homoscedasticity: Breusch-Pagan test on residuals
  - Outlier detection: Cook's distance > 4/n threshold
- Generate assumption diagnostic summary:
  - Pass/fail status for each assumption
  - Remedial actions triggered (if any)
  - Overall robustness assessment
- Create plot data CSVs for later visualization:
  - Scatterplot coordinates with fitted lines
  - Residual plot data
  - Assumption test results formatted for plotting

**Output:**
- data/step06_age_ravlt_plot_data.csv (scatterplot data for RAVLT)
- data/step06_age_rememvr_plot_data.csv (scatterplot data for REMEMVR)
- data/step06_assumption_results.csv (comprehensive assumption testing)
- data/step06_diagnostic_summary.txt (assumption testing summary)

**Validation Requirement:**
Validation tools MUST be used after diagnostic testing execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_age_ravlt_plot_data.csv: ~100 rows x 4 columns (Age, RAVLT, fitted, residuals)
- data/step06_age_rememvr_plot_data.csv: ~100 rows x 4 columns (Age, theta, fitted, residuals)
- data/step06_assumption_results.csv: assumption tests with p-values and decisions

*Value Ranges:*
- Age: 20-70 years (original data range)
- Fitted values: within observed outcome ranges
- Residuals: mean ~0 for proper model fit

*Data Quality:*
- Plot data contains full analysis sample
- No missing values in plot coordinates
- Assumption tests successfully executed for all variables

*Log Validation:*
- Required pattern: "Diagnostic plots generated: N data points"
- Required pattern: "Assumption testing complete: X/Y assumptions met"
- Forbidden patterns: "plot generation failed", "assumption error", "ERROR"

**Expected Behavior on Validation Failure:**
Log diagnostic warnings for assumption violations, continue with robust alternatives if available

---

### Step 7: Sensitivity and Power Analysis
**Dependencies:** Step 6 (diagnostics completed)
**Complexity:** Medium (~5 minutes)

**Purpose:** Conduct sensitivity analyses and post-hoc power analysis for correlation comparison

**Input:**
- data/step03_analysis_dataset.csv (full analysis data)
- data/step05_steiger_test.csv (primary Steiger results)
- data/step06_assumption_results.csv (assumption violations if any)

**Processing:**
- Sensitivity analyses based on assumption testing:
  - Outlier exclusion: Remove participants with Cook's D > 4/n, recompute all analyses
  - Non-parametric alternative: Spearman correlations if normality violated
  - Robust correlation: Winsorized correlations if extreme values detected
- Bootstrap validation of primary results:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Resample participants with replacement
  - Compute correlations and Steiger test for each iteration
  - Generate 95% CI for correlation difference
- Post-hoc power analysis for correlation comparison:
  - Given: N=100, observed correlation values, alpha=0.05
  - Calculate: achieved power for detecting observed correlation difference
  - Use: statsmodels.stats.power correlation power functions
  - Report: minimum detectable correlation difference at 80% power
  - If power < 0.80: acknowledge limitation in interpretation
- Cross-validation of correlation stability:
  - 5-fold cross-validation using sklearn.model_selection.KFold
  - Random seed: 42 for reproducibility
  - Compute correlations within each fold
  - Assess stability of correlation estimates across folds

**Output:**
- data/step07_sensitivity_analysis.csv (outlier-excluded results)
- data/step07_bootstrap_validation.csv (bootstrap CI for correlation difference)
- data/step07_power_analysis.csv (post-hoc power calculations)
- data/step07_cross_validation.csv (fold-wise correlation estimates)

**Validation Requirement:**
Validation tools MUST be used after sensitivity analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_sensitivity_analysis.csv: sensitivity results with/without outliers
- data/step07_bootstrap_validation.csv: 1000 bootstrap estimates
- data/step07_power_analysis.csv: power calculations and detectable effect sizes

*Value Ranges:*
- Bootstrap correlations: should center on observed values
- Power estimates: 0 to 1 (achieved power for observed effects)
- Cross-validation correlations: should be stable across folds

*Data Quality:*
- Sensitivity analyses converge to similar conclusions
- Bootstrap CIs consistent with analytical CIs
- Power analysis indicates adequate sensitivity for medium effects

*Log Validation:*
- Required pattern: "Sensitivity analysis complete: results stable"
- Required pattern: "Post-hoc power: X.XX for observed effect"
- Forbidden patterns: "bootstrap failed", "power calculation error", "ERROR"

**Expected Behavior on Validation Failure:**
Log sensitivity warnings if results unstable across methods, continue with primary analysis if bootstrap validates

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (dependency check results)
- data/step01_ravlt_demographics.csv (RAVLT and age data)
- data/step01_descriptives.txt (RAVLT/age descriptive statistics)
- data/step02_rememvr_theta.csv (REMEMVR theta scores)
- data/step02_theta_descriptives.txt (theta distribution summary)
- data/step03_analysis_dataset.csv (merged analysis data)
- data/step03_merge_summary.txt (merge diagnostics)
- data/step04_age_correlations.csv (primary correlation results)
- data/step04_bootstrap_cis.csv (bootstrap confidence intervals)
- data/step04_assumption_checks.txt (assumption testing results)
- data/step05_steiger_test.csv (dependent correlation comparison)
- data/step05_effect_sizes.csv (correlation difference effect sizes)
- data/step05_bootstrap_steiger.csv (bootstrap Steiger distribution)
- data/step06_age_ravlt_plot_data.csv (RAVLT scatterplot data)
- data/step06_age_rememvr_plot_data.csv (REMEMVR scatterplot data)
- data/step06_assumption_results.csv (diagnostic test results)
- data/step06_diagnostic_summary.txt (assumption summary)
- data/step07_sensitivity_analysis.csv (sensitivity/outlier analysis)
- data/step07_bootstrap_validation.csv (bootstrap validation)
- data/step07_power_analysis.csv (post-hoc power calculations)
- data/step07_cross_validation.csv (cross-validation stability)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_ravlt.log
- logs/step02_extract_theta.log
- logs/step03_merge_data.log
- logs/step04_compute_correlations.log
- logs/step05_steiger_test.log
- logs/step06_diagnostics.log
- logs/step07_sensitivity.log

### Plots (EMPTY until rq_plots runs)
Plot source CSVs created in data/ with step##_*_plot_data.csv format for later PNG/PDF generation.

### Results (EMPTY until rq_results runs)
Summary.md will be created by rq_results agent.

---

## Expected Data Formats

### Step-to-Step Transformations
1. Raw RAVLT/age -> standardized scores -> merged analysis dataset
2. Raw theta scores -> standardized scores -> merged analysis dataset  
3. Analysis dataset -> age correlations -> Steiger's test -> sensitivity analysis
4. Diagnostic plots generated from merged dataset throughout pipeline

### Column Naming Conventions
- UID: Participant identifier (consistent across all files)
- Age: Chronological age in years (preserved as continuous)
- RAVLT_Total: Raw RAVLT composite score
- RAVLT_z: Standardized RAVLT score  
- theta_all: Omnibus REMEMVR theta estimate
- theta_z: Standardized theta score
- Include_Analysis: Boolean flag for complete cases

### Data Type Constraints
- UID: object/string (not nullable)
- Age: float64 in [20, 70] range (not nullable)
- RAVLT_Total, theta_all: float64 (not nullable for analysis)
- Standardized scores: float64 with mean ~0, SD ~1
- p-values: float64 in [0, 1] range
- Correlation coefficients: float64 in [-1, 1] range

---

## Cross-RQ Dependencies

**Primary Dependency:** Ch5 5.1.1 (Functional Form Comparison)

**Required Ch5 Outputs:**
- results/ch5/5.1.1/status.yaml (rq_results: success)
- results/ch5/5.1.1/data/step03_theta_scores.csv (omnibus theta estimates)

**Fallback Paths:**
- results/ch5/5.1.1/data/final_theta_estimates.csv
- results/ch5/5.1.1/data/*theta*.csv

**Expected Ch5 Format:** 100 rows x 2+ columns (UID, theta_all)

**Circuit Breaker:** If Ch5 outputs not found, Step 0 will QUIT with specific error message

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
[Full 4-layer validation structure included above]

#### Step 1: Extract RAVLT Data
[Full 4-layer validation structure included above]

#### Step 2: Extract REMEMVR Theta
[Full 4-layer validation structure included above]

#### Step 3: Merge Analysis Dataset
[Full 4-layer validation structure included above]

#### Step 4: Compute Age Correlations
[Full 4-layer validation structure included above]

#### Step 5: Steiger's Z-Test
[Full 4-layer validation structure included above]

#### Step 6: Diagnostic Testing
[Full 4-layer validation structure included above]

#### Step 7: Sensitivity Analysis
[Full 4-layer validation structure included above]

---

## Summary

**Total Steps:** 8 (Step 0: dependency validation + Steps 1-7: analysis pipeline)
**Estimated Runtime:** ~25 minutes total
**Cross-RQ Dependencies:** Ch5 5.1.1 (omnibus theta scores)
**Primary Outputs:** Age correlations, Steiger's Z-test, sensitivity analyses
**Validation Coverage:** 100% (all 8 steps have 4-layer validation requirements)

**Key Hypothesis:** RAVLT shows significant age decline (r < -0.30) while REMEMVR shows minimal age decline (r ≈ 0), with statistically significant difference via Steiger's Z-test supporting VR scaffolding hypothesis.

**Critical Methodological Notes:**
- Steiger's Z-test correctly handles dependent correlations (both share Age variable)
- Bootstrap validation provides robust confidence intervals
- Multiple sensitivity analyses ensure result stability
- Power analysis assesses adequacy for detecting meaningful correlation differences
- Decision D068 compliance: dual p-value reporting throughout

**Statistical Implementation Features (v5.1):**
- Random seed = 42 for all bootstrap/resampling procedures
- 1000 bootstrap iterations with percentile CIs
- 5-fold cross-validation for correlation stability
- Comprehensive assumption testing with remedial actions
- Post-hoc power analysis for correlation differences
- Bonferroni correction for multiple comparisons (2 correlations)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent v5.1.0