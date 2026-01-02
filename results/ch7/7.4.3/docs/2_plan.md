# Analysis Plan: RQ 7.4.3 - RPM Predicts Temporal Integration Performance

**Research Question:** 7.4.3
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

**Purpose:** Examine whether RPM (fluid intelligence) differentially predicts performance on items requiring integration of What+Where+When information versus single-domain items.

**Pipeline:** Multiple correlation analysis with Steiger's Z-test for dependent correlations
**Steps:** 9 total analysis steps (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** 45-60 minutes

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Bonferroni correction: alpha = 0.05/2 = 0.025 (two main correlations)
- Bootstrap confidence intervals for robust inference

**Methodological Approach:**
- Use When domain (-O- tags) as proxy for temporal integration complexity
- Compare r(RPM, When_theta) vs r(RPM, What_theta) for differential prediction
- Implement dependent correlation comparison via Steiger's Z-test
- Random seed = 42 for all randomized procedures

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 domain-specific outputs and cognitive data exist before proceeding

**Input:**
- Primary: results/ch5/5.2.1/data/step03_theta_scores.csv (What domain theta)
- Alternative: results/ch5/5.2.1/data/*theta*.csv (What domain outputs)
- Primary: results/ch5/5.2.3/data/step03_theta_scores.csv (When domain theta)
- Alternative: results/ch5/5.2.3/data/*theta*.csv (When domain outputs)
- Fallback: results/ch5/5.1.1/data/step03_theta_scores.csv (Overall theta)
- Primary: data/cache/master.xlsx (RPM_Scor cognitive test)
- Expected content: Theta estimates for N=100 participants, RPM scores

**Processing:**
- Check Ch5 5.2.1 and 5.2.3 completion status in their status.yaml files
- Locate domain-specific theta files using multiple path patterns
- Verify master.xlsx exists and contains RPM_Scor column
- Confirm participant overlap between datasets
- Log all dependency validation results
- If What or When domain files missing: use overall theta as fallback

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Contains dependency check results for 3+ file sources

*Value Ranges:*
- No numeric ranges (text validation file)
- Validation status: PASS/FAIL for each dependency

*Data Quality:*
- All required dependencies identified (What, When, RPM sources)
- Clear indication of which files found/missing
- Fallback paths documented if primary files unavailable

*Log Validation:*
- Required patterns: "Dependency check complete", "Ch5 outputs", "RPM data"
- Required patterns: "What domain: FOUND" OR "What domain: FALLBACK"
- Required patterns: "When domain: FOUND" OR "When domain: FALLBACK"
- Forbidden patterns: "ERROR", "CRITICAL FAILURE"

**Expected Behavior on Validation Failure:**
- Raise error with specific missing dependency
- Log to logs/step00_validate_dependencies.log
- Quit immediately if RPM data unavailable

### Step 1: Extract and Prepare Cognitive Data
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (<5 minutes)

**Purpose:** Extract RPM scores from master.xlsx and prepare for analysis

**Input:**
- data/cache/master.xlsx (RPM_Scor column)
- Validated availability from Step 0

**Processing:**
- Load master.xlsx using pandas.read_excel()
- Extract UID and RPM_Scor columns
- Check for missing RPM values (should be minimal)
- Compute descriptive statistics (mean, SD, range, skewness)
- Check for ceiling/floor effects (>90% at max/min)
- Identify potential outliers using IQR method (Q1-1.5*IQR, Q3+1.5*IQR)
- Log data quality metrics

**Output:**
- data/step01_rpm_extraction.csv (UID, RPM_Scor columns)
- data/step01_rpm_descriptives.txt (descriptive statistics)

**Validation Requirement:**
Validation tools MUST be used after RPM extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_rpm_extraction.csv: 100 rows x 2 columns (UID, RPM_Scor)
- data/step01_rpm_descriptives.txt: text file with descriptive statistics

*Value Ranges:*
- RPM_Scor in [0, 60] (standard RPM range)
- No negative values or values >60
- Mean RPM approximately 30-45 (typical range for adults)

*Data Quality:*
- All 100 participants present
- Missing RPM values <5% (acceptable threshold)
- No duplicate UIDs
- RPM scores follow expected distribution (not uniform)

*Log Validation:*
- Required patterns: "RPM extraction complete", "N=100 participants", "Missing data"
- Forbidden patterns: "ERROR", "FAIL", "excessive missing"

**Expected Behavior on Validation Failure:**
- Raise error if >5% missing RPM data
- Log warning if ceiling/floor effects detected
- Continue with available data if validation passes

### Step 2: Extract Domain-Specific Theta Scores
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (<5 minutes)

**Purpose:** Extract What and When domain theta scores from Ch5 analyses

**Input:**
- Primary: results/ch5/5.2.1/data/step03_theta_scores.csv (What domain)
- Primary: results/ch5/5.2.3/data/step03_theta_scores.csv (When domain)
- Fallback: results/ch5/5.1.1/data/step03_theta_scores.csv (Overall theta)

**Processing:**
- Load What domain theta scores (Ch5 5.2.1 output)
- Load When domain theta scores (Ch5 5.2.3 output)
- If domain-specific files unavailable: use overall theta as proxy
- Extract UID and theta columns from each dataset
- Rename theta columns for clarity: theta_What, theta_When
- Compute descriptive statistics for both domains
- Check theta range consistency with IRT scale [-3, 3]
- Identify participants with extreme theta values (>3 SD from mean)

**Output:**
- data/step02_theta_what.csv (UID, theta_What columns)
- data/step02_theta_when.csv (UID, theta_When columns)
- data/step02_theta_descriptives.txt (descriptive statistics)

**Validation Requirement:**
Validation tools MUST be used after theta extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_theta_what.csv: 100 rows x 2 columns (UID, theta_What)
- data/step02_theta_when.csv: 100 rows x 2 columns (UID, theta_When)
- data/step02_theta_descriptives.txt: descriptive statistics summary

*Value Ranges:*
- theta_What in [-4, 4] (IRT ability scale with outlier tolerance)
- theta_When in [-4, 4] (IRT ability scale with outlier tolerance)
- Most values in [-3, 3] range (standard IRT bounds)

*Data Quality:*
- All 100 participants present in both files
- No missing theta values (IRT provides estimates for all)
- UIDs match across What and When datasets
- Theta distributions approximately normal

*Log Validation:*
- Required patterns: "Theta extraction complete", "What domain loaded", "When domain loaded"
- Required patterns: "N=100 participants" for both domains
- Forbidden patterns: "ERROR", "FAIL", "missing theta"

**Expected Behavior on Validation Failure:**
- Raise error if theta files completely missing
- Log warning if >5% extreme values (|theta| > 3)
- Continue with available data if core requirements met

### Step 3: Merge and Prepare Analysis Dataset
**Dependencies:** Steps 1-2 (RPM + theta data)
**Complexity:** Low (<5 minutes)

**Purpose:** Merge RPM and theta datasets into analysis-ready format

**Input:**
- data/step01_rpm_extraction.csv
- data/step02_theta_what.csv
- data/step02_theta_when.csv

**Processing:**
- Merge datasets on UID using inner join (complete cases only)
- Create final analysis dataset with columns: UID, RPM_Scor, theta_What, theta_When
- Check for participants missing any required variables
- Compute pairwise correlations between all variables
- Create correlation matrix heatmap data for visualization
- Save complete cases count for power analysis
- Log final sample size and data completeness

**Output:**
- data/step03_analysis_dataset.csv (merged dataset for analysis)
- data/step03_correlation_matrix.csv (preliminary correlations)

**Validation Requirement:**
Validation tools MUST be used after dataset preparation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_analysis_dataset.csv: N rows x 4 columns (UID, RPM_Scor, theta_What, theta_When)
- data/step03_correlation_matrix.csv: 3x3 correlation matrix

*Value Ranges:*
- RPM_Scor in [0, 60]
- theta_What in [-4, 4]
- theta_When in [-4, 4]
- Correlations in [-1, 1]

*Data Quality:*
- N >= 90 (allow for some missing data)
- No missing values in analysis dataset (complete cases)
- All correlations reasonable magnitude (<0.9 to avoid singularity)
- RPM and theta scores show expected correlation pattern

*Log Validation:*
- Required patterns: "Merge complete", "N=XX complete cases", "Correlation matrix"
- Forbidden patterns: "ERROR", "FAIL", "insufficient data"

**Expected Behavior on Validation Failure:**
- Raise error if N < 80 (insufficient power)
- Log warning if N < 95 (some data loss)
- Continue with available complete cases if validation passes

### Step 4: Compute Primary Correlations with Bootstrap CIs
**Dependencies:** Step 3 (merged dataset)
**Complexity:** Medium (~15 minutes including bootstrap)

**Purpose:** Compute correlations r(RPM, theta_What) and r(RPM, theta_When) with robust confidence intervals

**Input:**
- data/step03_analysis_dataset.csv

**Processing:**
- Compute primary correlations:
  - r1 = cor(RPM_Scor, theta_What) [single-domain baseline]
  - r2 = cor(RPM_Scor, theta_When) [integration complexity proxy]
- Bootstrap confidence intervals for both correlations:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - CI computation: percentile method (2.5th, 97.5th percentiles)
- Check correlation assumptions:
  - Bivariate normality via Mardia test or visual inspection
  - Linearity via scatterplot inspection
  - Homoscedasticity via residual plots
- Compute sample size-adjusted correlations if needed
- Report both correlation estimates with 95% bootstrap CIs

**Output:**
- data/step04_primary_correlations.csv (r1, r2 with CIs and diagnostics)
- data/step04_bootstrap_distributions.csv (bootstrap replicates)

**Validation Requirement:**
Validation tools MUST be used after correlation computation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_primary_correlations.csv: 2 rows x 6 columns (correlation, domain, r, ci_lower, ci_upper, n)
- data/step04_bootstrap_distributions.csv: 1000 rows x 3 columns (iteration, r_what, r_when)

*Value Ranges:*
- Correlations r1, r2 in [-1, 1]
- Bootstrap CIs non-degenerate (ci_upper > ci_lower)
- Bootstrap distributions approximately normal
- CI width reasonable (<0.40 for adequate precision)

*Data Quality:*
- Bootstrap completed full 1000 iterations
- No NaN values in correlation estimates
- CI bounds contain point estimate (ci_lower <= r <= ci_upper)
- Adequate precision (CI width suggests adequate sample size)

*Log Validation:*
- Required patterns: "Correlations computed", "Bootstrap complete: 1000 iterations"
- Required patterns: "r_what = X.XXX", "r_when = X.XXX"
- Forbidden patterns: "ERROR", "FAIL", "bootstrap failed"

**Expected Behavior on Validation Failure:**
- Raise error if bootstrap fails to complete
- Log warning if correlation assumptions severely violated
- Continue with Spearman correlations if normality violated

### Step 5: Test Differential Prediction via Steiger's Z-test
**Dependencies:** Step 4 (primary correlations)
**Complexity:** Medium (~10 minutes)

**Purpose:** Test whether RPM predicts When domain performance differently than What domain performance

**Input:**
- data/step04_primary_correlations.csv
- data/step03_analysis_dataset.csv (for N and raw correlations)

**Processing:**
- Extract correlation coefficients: r1 (RPM-What), r2 (RPM-When)
- Compute correlation between What and When domains: r12
- Apply Steiger's Z-test for dependent correlations:
  - Null hypothesis: r1 = r2 (no differential prediction)
  - Alternative: r1 ≠ r2 (differential prediction exists)
  - Test statistic: Z = (Z1 - Z2) / SE_diff
  - Where Z1 = arctanh(r1), Z2 = arctanh(r2)
  - RPM is the shared variable across both correlations
- Multiple comparison correction:
  - Family: Within-RQ primary test (conservative approach)
  - Bonferroni: alpha = 0.05 (single primary hypothesis)
  - Also compute FDR using Benjamini-Hochberg for comparison
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Compute effect size (Cohen's q):
  - q = arctanh(r1) - arctanh(r2)
  - Interpretation: 0.1 small, 0.3 medium, 0.5 large difference

**Output:**
- data/step05_steiger_test.csv (test results with dual p-values)
- data/step05_effect_size.csv (Cohen's q with interpretation)

**Validation Requirement:**
Validation tools MUST be used after Steiger's test execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_steiger_test.csv: 1 row x 8 columns (r1, r2, r12, z_stat, p_uncorrected, p_bonferroni, p_fdr, n)
- data/step05_effect_size.csv: 1 row x 4 columns (cohens_q, q_interpretation, confidence_interval, method)

*Value Ranges:*
- r1, r2, r12 in [-1, 1] (correlation bounds)
- z_stat finite (not infinite or NaN)
- p-values in [0, 1] (valid probability range)
- Cohen's q reasonable magnitude (typically <2.0)

*Data Quality:*
- All correlation inputs valid (non-missing)
- Test statistic computed successfully
- Both uncorrected and corrected p-values present (Decision D068)
- Effect size interpretation provided

*Log Validation:*
- Required patterns: "Steiger test complete", "Z = X.XXX", "p_uncorrected = X.XXX"
- Required patterns: "Cohen's q = X.XXX", "Decision D068 applied"
- Forbidden patterns: "ERROR", "FAIL", "singular matrix"

**Expected Behavior on Validation Failure:**
- Raise error if correlations produce singular covariance matrix
- Log warning if effect size extremely large (suggests data issues)
- Continue with descriptive comparison if formal test fails

### Step 6: Check Statistical Assumptions and Diagnostics
**Dependencies:** Steps 4-5 (correlations and test results)
**Complexity:** Medium (~10 minutes)

**Purpose:** Verify assumptions underlying correlation analysis and identify potential issues

**Input:**
- data/step03_analysis_dataset.csv
- data/step04_primary_correlations.csv

**Processing:**
- Check assumptions for correlation analysis:
  - Normality: Shapiro-Wilk test for each variable (RPM, theta_What, theta_When)
  - Bivariate normality: QQ plots or Mardia test for multivariate normality
  - Linearity: Scatterplot inspection with lowess curves
  - Homoscedasticity: Residual plots for linear relationships
- Outlier detection:
  - Cook's distance for bivariate relationships: D > 4/n
  - Mahalanobis distance for multivariate outliers: p < 0.001
  - Leverage values: > 2(p+1)/n where p = number of predictors
- Influence analysis:
  - Compute correlations with/without potential outliers
  - Document impact of outliers on correlation magnitude
- Remedial actions if violations detected:
  - Normality p < 0.05: Report bootstrap CIs as primary (already computed)
  - Severe non-linearity: Consider Spearman correlations
  - Outliers detected: Report results with/without outliers

**Output:**
- data/step06_assumption_checks.csv (test results and thresholds)
- data/step06_outlier_analysis.csv (outlier identification and impact)
- data/step06_diagnostic_summary.txt (interpretation and remedial actions)

**Validation Requirement:**
Validation tools MUST be used after assumption checking execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_assumption_checks.csv: 6+ rows x 4 columns (test, variable, statistic, p_value)
- data/step06_outlier_analysis.csv: N rows x 5 columns (UID, cooks_d, mahalanobis_d, leverage, outlier_flag)
- data/step06_diagnostic_summary.txt: text summary with remedial actions

*Value Ranges:*
- Test statistics appropriate for each test type
- p-values in [0, 1]
- Cook's D >= 0
- Mahalanobis distance >= 0
- Leverage in [0, 1]

*Data Quality:*
- All assumption tests completed
- Outlier flags clearly identified (TRUE/FALSE)
- Number of outliers reasonable (<10% of sample)
- Remedial actions specified for any violations

*Log Validation:*
- Required patterns: "Assumption checks complete", "Outlier analysis complete"
- Required patterns: "Normality", "Linearity", "Outliers identified: X"
- Forbidden patterns: "ERROR", "FAIL", "test crashed"

**Expected Behavior on Validation Failure:**
- Log warning for assumption violations but continue analysis
- Document all violations for interpretation
- Apply remedial actions automatically where possible

### Step 7: Sensitivity Analyses and Robustness Checks
**Dependencies:** Step 6 (diagnostics)
**Complexity:** Medium (~10 minutes)

**Purpose:** Test robustness of primary findings through alternative approaches

**Input:**
- data/step03_analysis_dataset.csv
- data/step06_outlier_analysis.csv (outlier identification)

**Processing:**
- Outlier sensitivity analysis:
  - Recompute correlations excluding identified outliers
  - Rerun Steiger's test with outliers removed
  - Compare effect sizes with/without outliers
- Non-parametric alternative:
  - Compute Spearman rank correlations as alternative to Pearson
  - Apply bootstrap to Spearman correlations for CIs
  - Compare Pearson vs Spearman results for consistency
- Alternative integration definitions:
  - If available, compare When domain vs Overall theta correlations
  - Test whether domain-specific vs omnibus factor shows similar patterns
- Range restriction assessment:
  - Check if theta score range is artificially constrained
  - Compute range-corrected correlations if appropriate
- Bootstrap robustness:
  - Repeat bootstrap with different random seeds (43, 44)
  - Verify stability of confidence interval estimates

**Output:**
- data/step07_sensitivity_outliers.csv (correlations without outliers)
- data/step07_nonparametric.csv (Spearman correlation results)
- data/step07_robustness_summary.txt (comparison of all approaches)

**Validation Requirement:**
Validation tools MUST be used after sensitivity analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_sensitivity_outliers.csv: 2 rows x 4 columns (correlation, domain, r_full, r_no_outliers)
- data/step07_nonparametric.csv: 2 rows x 4 columns (correlation, pearson_r, spearman_r, difference)
- data/step07_robustness_summary.txt: text summary of robustness checks

*Value Ranges:*
- All correlation estimates in [-1, 1]
- Differences between approaches reasonable (<0.2 typically)
- Spearman correlations may differ but should show similar pattern

*Data Quality:*
- Outlier exclusion completed successfully
- Spearman correlations computed for all pairs
- Robustness comparison shows consistent pattern across methods
- Bootstrap stability confirmed

*Log Validation:*
- Required patterns: "Sensitivity analysis complete", "Outliers excluded: X"
- Required patterns: "Spearman correlations", "Robustness confirmed"
- Forbidden patterns: "ERROR", "FAIL", "unstable results"

**Expected Behavior on Validation Failure:**
- Log warning if sensitivity analyses show large discrepancies
- Continue with primary analysis if robustness checks suggest stability
- Flag potential data issues if results highly sensitive to methods

### Step 8: Power Analysis and Effect Size Interpretation
**Dependencies:** Steps 5-7 (primary results and sensitivity)
**Complexity:** Low (<5 minutes)

**Purpose:** Evaluate power for detected effects and provide interpretation framework

**Input:**
- data/step05_steiger_test.csv (effect size)
- data/step03_analysis_dataset.csv (sample size)

**Processing:**
- Post-hoc power analysis for correlation difference:
  - Given: N (sample size from merged dataset)
  - Given: alpha = 0.05, observed effect size (Cohen's q)
  - Calculate: achieved power for observed correlation difference
  - Use: manual calculation with standard formulas for correlation comparison
  - Report: power estimate and interpretation
- Sensitivity power analysis:
  - Calculate: minimum detectable correlation difference at 80% power
  - Given current N and alpha = 0.05
  - Compare to observed effect size
- Effect size interpretation:
  - Cohen's q classification: 0.1 small, 0.3 medium, 0.5 large
  - Practical significance assessment for VR memory testing
  - Clinical relevance in context of individual differences assessment
- Sample size recommendations:
  - For replication: N needed for 80% power to detect observed effect
  - For small effects: N needed for 80% power to detect q = 0.1

**Output:**
- data/step08_power_analysis.csv (power estimates and sample size recommendations)
- data/step08_interpretation.txt (effect size interpretation and implications)

**Validation Requirement:**
Validation tools MUST be used after power analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_power_analysis.csv: 4 rows x 3 columns (analysis_type, value, interpretation)
- data/step08_interpretation.txt: text summary with practical implications

*Value Ranges:*
- Power estimates in [0, 1]
- Sample size recommendations > 0 and reasonable (<1000)
- Cohen's q within typical range for psychology research

*Data Quality:*
- All power calculations completed
- Sample size recommendations reasonable and achievable
- Interpretation framework comprehensive
- Clinical relevance addressed

*Log Validation:*
- Required patterns: "Power analysis complete", "Achieved power", "Sample size recommendations"
- Forbidden patterns: "ERROR", "FAIL", "power calculation failed"

**Expected Behavior on Validation Failure:**
- Log warning if power calculations produce unreasonable values
- Continue with qualitative interpretation if quantitative power fails
- Document limitations in statistical power assessment

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (dependency check results)
- data/step01_rpm_extraction.csv (RPM scores: 100x2)
- data/step01_rpm_descriptives.txt (RPM descriptive statistics)
- data/step02_theta_what.csv (What domain theta: 100x2)
- data/step02_theta_when.csv (When domain theta: 100x2)
- data/step02_theta_descriptives.txt (theta descriptive statistics)
- data/step03_analysis_dataset.csv (merged analysis data: ~95x4)
- data/step03_correlation_matrix.csv (preliminary correlations: 3x3)
- data/step04_primary_correlations.csv (main correlations with CIs: 2x6)
- data/step04_bootstrap_distributions.csv (bootstrap replicates: 1000x3)
- data/step05_steiger_test.csv (differential prediction test: 1x8)
- data/step05_effect_size.csv (Cohen's q and interpretation: 1x4)
- data/step06_assumption_checks.csv (assumption test results: 6+x4)
- data/step06_outlier_analysis.csv (outlier identification: ~95x5)
- data/step06_diagnostic_summary.txt (remedial action summary)
- data/step07_sensitivity_outliers.csv (robustness without outliers: 2x4)
- data/step07_nonparametric.csv (Spearman correlation comparison: 2x4)
- data/step07_robustness_summary.txt (sensitivity analysis summary)
- data/step08_power_analysis.csv (power estimates and recommendations: 4x3)
- data/step08_interpretation.txt (effect size interpretation)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_rpm.log
- logs/step02_extract_theta.log
- logs/step03_merge_data.log
- logs/step04_correlations.log
- logs/step05_steiger_test.log
- logs/step06_diagnostics.log
- logs/step07_sensitivity.log
- logs/step08_power_analysis.log

### Plots (EMPTY until rq_plots runs)
Note: Plot source data will be created in data/ folder:
- data/step04_correlation_plot_data.csv (for scatterplots)
- data/step06_diagnostic_plot_data.csv (for assumption checking plots)
- data/step07_sensitivity_plot_data.csv (for robustness comparison plots)

### Results (EMPTY until rq_results runs)
Note: rq_results will create summary.md based on analysis outputs

---

## Expected Data Formats

### Step-to-Step Transformations
1. **RPM Extraction:** master.xlsx → extracted scores (step01)
2. **Theta Extraction:** Ch5 outputs → domain-specific theta (step02)
3. **Data Merge:** RPM + theta → analysis dataset (step03)
4. **Correlations:** Analysis dataset → correlations + bootstrap CIs (step04)
5. **Statistical Test:** Correlations → Steiger's Z-test results (step05)
6. **Diagnostics:** Analysis dataset → assumption checks + outliers (step06)
7. **Sensitivity:** All data → robustness checks (step07)
8. **Power:** Test results → power analysis (step08)

### Column Naming Conventions
- **UIDs:** Consistent "UID" column across all files
- **RPM:** "RPM_Scor" (matches master.xlsx)
- **Theta:** "theta_What", "theta_When" (domain-specific)
- **Correlations:** "r", "ci_lower", "ci_upper", "n"
- **Test Results:** "z_stat", "p_uncorrected", "p_bonferroni", "p_fdr"
- **Effect Sizes:** "cohens_q", "q_interpretation"

### Data Type Constraints
- **UIDs:** String/object type (e.g., "REMEM001")
- **RPM scores:** Integer [0, 60] (standard RPM range)
- **Theta scores:** Float [-4, 4] (IRT scale with tolerance)
- **Correlations:** Float [-1, 1] (bounded correlation range)
- **P-values:** Float [0, 1] (valid probability range)
- **Sample sizes:** Integer >0 (positive counts)

---

## Cross-RQ Dependencies

**Required Ch5 Outputs:**
- Ch5 5.2.1: What domain theta scores (primary dependency)
- Ch5 5.2.3: When domain theta scores (primary dependency)
- Ch5 5.1.1: Overall theta scores (fallback if domain-specific unavailable)

**Dependency Handling:**
- Primary path verification in Step 0
- Fallback to overall theta if domain-specific files missing
- Clear error messages if cognitive data (RPM) unavailable
- Graceful degradation with reduced functionality if partial data available

**Required Cognitive Data:**
- master.xlsx with RPM_Scor column (critical dependency)
- Must have >90% participant overlap with Ch5 theta scores

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
**Substance Validation:** 4-layer structure with file existence, path validation, content verification, and error handling patterns.

#### Step 1: Extract RPM Data  
**Substance Validation:** 4-layer structure with file dimensions, value ranges (RPM 0-60), missing data thresholds (<5%), and successful extraction patterns.

#### Step 2: Extract Theta Data
**Substance Validation:** 4-layer structure with file dimensions, IRT scale ranges (theta -4 to +4), domain consistency, and successful loading patterns.

#### Step 3: Merge Analysis Dataset
**Substance Validation:** 4-layer structure with merged dimensions (N≥90), complete cases verification, correlation matrix validity, and successful merge patterns.

#### Step 4: Primary Correlations
**Substance Validation:** 4-layer structure with correlation bounds [-1,1], bootstrap completion (1000 iterations), CI validity, and correlation computation patterns.

#### Step 5: Steiger's Z-test
**Substance Validation:** 4-layer structure with test statistic validity, dual p-values (Decision D068), effect size bounds, and successful test completion patterns.

#### Step 6: Assumption Diagnostics
**Substance Validation:** 4-layer structure with assumption test completion, outlier identification thresholds, diagnostic summary creation, and remedial action patterns.

#### Step 7: Sensitivity Analysis
**Substance Validation:** 4-layer structure with robustness check completion, method comparison validity, sensitivity result consistency, and alternative method patterns.

#### Step 8: Power Analysis
**Substance Validation:** 4-layer structure with power estimate bounds [0,1], sample size reasonableness, interpretation completeness, and power calculation patterns.

---

## Summary

**Total Steps:** 9 (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** 45-60 minutes
**Cross-RQ Dependencies:** Ch5 5.2.1, 5.2.3 (with 5.1.1 fallback) + master.xlsx cognitive data
**Primary Outputs:** Differential prediction analysis via Steiger's Z-test with bootstrap CIs and sensitivity analyses
**Validation Coverage:** 100% (all 9 steps have 4-layer validation requirements)

**Key Hypothesis:** RPM should predict complex integration (When domain) more strongly than simple object identification (What domain), reflecting fluid intelligence support for relational binding across temporal domains.

**Critical Methodological Notes:**
- Uses When domain (-O- tags) as proxy for temporal integration complexity
- Bootstrap CIs provide robust inference with 1000 iterations, seed=42
- Steiger's Z-test properly handles dependent correlations sharing RPM variable
- Decision D068 dual p-value reporting (uncorrected + Bonferroni)
- Comprehensive sensitivity analyses address outliers and non-parametric alternatives
- Post-hoc power analysis evaluates adequacy of effect size detection

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml  
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent v5.1 with enhanced statistical specifications