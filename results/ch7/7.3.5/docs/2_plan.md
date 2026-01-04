# Analysis Plan: RQ 7.3.5 - Confidence-accuracy gap predicting cognitive reserve

**Research Question:** 7.3.5
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This analysis examines whether individuals with high confidence AND high accuracy (well-calibrated high performers) show signs of cognitive reserve compared to overconfident or underconfident groups. The analysis creates calibration groups based on confidence-accuracy residuals and compares groups on education, RPM scores, and age as cognitive reserve indicators.

**Pipeline:** ANOVA with correlational analysis
**Steps:** 7 total analysis steps (Step 0: validation + Steps 1-6: analysis)  
**Estimated Runtime:** ~45 minutes (includes bootstrap procedures)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Bonferroni correction for within-RQ family (3 ANOVAs, 3 correlations = 6 tests)
- Bootstrap CIs for all correlations (1000 iterations, seed=42)

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies

**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 5.1.1 and Ch6 outputs exist before proceeding

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv (overall episodic memory theta)
- Alternative: results/ch5/5.1.1/data/*theta*.csv (theta score patterns)
- Ch6 confidence: results/ch6/*/data/*confidence*theta*.csv (confidence-theta calibration)
- Fallback Ch6: results/ch6/*/data/confidence_ratings.csv (raw confidence data)
- Master data: data/cache/master.xlsx (cognitive reserve indicators)
- Expected: 100 participants with theta_all, confidence_theta, education, RPM, age

**Processing:**
- Check Ch5 5.1.1 status.yaml shows rq_results: success
- Locate theta score file using multiple patterns
- Locate Ch6 confidence data (try multiple RQ folders in ch6/)
- Verify master.xlsx accessible with required columns
- Log all validation checks with PASS/FAIL status
- If any critical file missing: QUIT with specific error message

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Contains PASS/FAIL status for each dependency
- File size >200 bytes (comprehensive validation logging)

*Value Ranges:*
- All dependencies report "PASS" status
- No "MISSING" or "FAIL" entries for critical files
- Ch5 5.1.1 status confirmed as "success"

*Data Quality:*
- Validation covers all 4 dependency sources (Ch5, Ch6, master.xlsx, status files)
- Each dependency has explicit PASS/FAIL determination
- No ambiguous or incomplete validation results

*Log Validation:*
- Required patterns: "Dependency validation COMPLETE", "ALL CRITICAL FILES: PASS"
- Forbidden patterns: "FAIL", "MISSING", "ERROR", "cannot locate"
- Acceptable warnings: "Alternative path used" (fallback success)

**Expected Behavior on Validation Failure:**
QUIT immediately with specific error about missing dependency. Log to logs/step00_validate_dependencies.log and invoke g_debug for troubleshooting.

---

### Step 1: Extract and Merge Data Sources

**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (~5 minutes)

**Purpose:** Load and merge theta scores, confidence ratings, and cognitive reserve indicators into single analysis dataset

**Input:**
- results/ch5/5.1.1/data/step03_theta_scores.csv (or validated alternative)
- results/ch6/*/data/*confidence*theta*.csv (or raw confidence + calibration)
- data/cache/master.xlsx (education, RPM scores, age data)

**Processing:**
- Load theta_all scores from Ch5 output (expected columns: UID, theta_all, theta_se)
- Load confidence_theta scores from Ch6 output (expected: UID, confidence_theta)
- Load cognitive reserve data from master.xlsx:
  - Education years (EDUC_YEARS column)
  - RPM total score (RPM_TOTAL column) 
  - Age (AGE column)
- Merge on UID with inner join (participants must have all data)
- Check for missing values and document exclusions
- Verify final N >= 80 participants (adequate for group comparisons)
- Save merged dataset with standardized column names

**Output:**
- data/step01_merged_data.csv (UID, theta_all, confidence_theta, education, rpm, age)

**Validation Requirement:**
Validation tools MUST be used after data extraction and merging.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_merged_data.csv: 80-100 rows x 6 columns
- Columns: UID (object), theta_all (float64), confidence_theta (float64), education (int), rpm (int), age (int)
- No duplicate UIDs, all values non-null

*Value Ranges:*
- theta_all in [-3, 3] (IRT ability scale)
- confidence_theta in [-3, 3] (IRT confidence scale)
- education in [8, 25] (years of education range)
- rpm in [0, 60] (RPM total score range)
- age in [18, 85] (participant age range)

*Data Quality:*
- N >= 80 participants (adequate sample size)
- Missing data = 0% after inner join
- All UIDs from original datasets preserved
- No extreme outliers flagged (>3 SD from mean)

*Log Validation:*
- Required patterns: "Merge complete: N=[80-100] participants", "No missing values detected"
- Required patterns: "VALIDATION - PASS"
- Forbidden patterns: "ERROR", "merge failed", "missing values"
- Acceptable warnings: "N excluded due to missing data" (if <20)

**Expected Behavior on Validation Failure:**
Raise error with specific failure details. If N <80, acknowledge limitation but proceed if N >= 60. Log to logs/step01_extract_merge.log.

---

### Step 2: Create Calibration Groups

**Dependencies:** Step 1 (merged data)
**Complexity:** Medium (~8 minutes)

**Purpose:** Compute confidence-accuracy residuals and create three calibration groups for comparison

**Input:**
- data/step01_merged_data.csv (theta_all and confidence_theta scores)

**Processing:**
- Compute correlation between theta_all and confidence_theta across all participants
- Fit linear regression: confidence_theta ~ theta_all
- Extract standardized residuals (confidence - predicted confidence)
- Create three groups based on residual distribution:
  - Well-calibrated: residuals in [-0.5 SD, +0.5 SD]
  - Overconfident: residuals > +0.5 SD (higher confidence than accuracy)
  - Underconfident: residuals < -0.5 SD (lower confidence than accuracy)
- Validate group sizes: each group should have n >= 15 for ANOVA
- If groups unbalanced, try tertile split as alternative
- Compute descriptive statistics per group (means, SDs for all variables)
- Document group creation method and final N per group

**Output:**
- data/step02_calibration_groups.csv (UID, theta_all, confidence_theta, residual, group, group_n)
- data/step02_group_descriptives.csv (group-level means and SDs)

**Validation Requirement:**
Validation tools MUST be used after calibration group creation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_calibration_groups.csv: 80-100 rows x 6 columns
- data/step02_group_descriptives.csv: 3 rows x 8 columns (group stats)
- Group column contains exactly 3 unique values
- All groups have n >= 15 participants

*Value Ranges:*
- residual in [-3, 3] (standardized residual bounds)
- group_n >= 15 for each group (adequate sample size)
- Total N across groups equals input N from Step 1
- residual mean approximately 0 across all participants

*Data Quality:*
- No participants unassigned to groups
- Group assignments mutually exclusive and exhaustive
- Residual computation successful (no NaN values)
- Group balance reasonable (largest group <60% of total)

*Log Validation:*
- Required patterns: "Groups created: Well-calibrated n=X, Overconfident n=Y, Underconfident n=Z"
- Required patterns: "All groups n>=15", "VALIDATION - PASS"
- Forbidden patterns: "ERROR", "group size too small", "residual computation failed"

**Expected Behavior on Validation Failure:**
If any group n <15, try tertile split alternative. If still unbalanced, proceed with warning but acknowledge limitation. Log to logs/step02_create_groups.log.

---

### Step 3: One-Way ANOVA Comparisons

**Dependencies:** Step 2 (calibration groups)  
**Complexity:** Medium (~10 minutes including assumption checks)

**Purpose:** Compare calibration groups on cognitive reserve indicators (education, RPM, age) using one-way ANOVA with assumption testing

**Input:**
- data/step02_calibration_groups.csv (group assignments)
- Dependent variables: education, rpm, age from Step 1 merge

**Processing:**
- Run three one-way ANOVAs: DV ~ calibration group
  1. Education ~ group
  2. RPM ~ group  
  3. Age ~ group
- For each ANOVA, implement complete statistical specification:
  - Method: scipy.stats.f_oneway or statsmodels.api.OLS with categorical predictor
  - Effect size: eta-squared with 95% CI
  - Post-hoc tests: Tukey HSD for pairwise comparisons
- Assumption checking for each ANOVA:
  - Normality: Shapiro-Wilk test on residuals per group
  - Homogeneity of variance: Levene's test
  - Independence: verified by design (between-subjects)
- Remedial actions if assumptions violated:
  - Normality p < 0.05: Report non-parametric Kruskal-Wallis as alternative
  - Heteroscedasticity p < 0.05: Report Welch ANOVA (unequal variances)
  - Both violated: Use non-parametric with bootstrap CIs
- Multiple comparison correction:
  - Family: Within-RQ ANOVAs (3 tests)
  - Bonferroni: alpha = 0.05/6 = 0.0083 (3 ANOVAs + 3 correlations in Step 4)
  - Report BOTH uncorrected AND corrected p-values (Decision D068)

**Output:**
- data/step03_anova_results.csv (F-stats, p-values, effect sizes, group means)
- data/step03_assumption_checks.csv (normality and homoscedasticity test results)
- data/step03_posthoc_comparisons.csv (Tukey HSD pairwise results)

**Validation Requirement:**
Validation tools MUST be used after ANOVA execution and assumption testing.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_anova_results.csv: 3 rows x 10 columns (one per DV)
- Columns include: DV, F_stat, p_uncorrected, p_bonferroni, eta_squared, eta_ci_lower, eta_ci_upper
- data/step03_assumption_checks.csv: 6 rows (3 DVs x 2 tests each)
- data/step03_posthoc_comparisons.csv: 9 rows (3 DVs x 3 pairwise comparisons)

*Value Ranges:*
- F_stat >= 0 (F-statistics non-negative)
- p_uncorrected in [0, 1], p_bonferroni in [0, 1]
- eta_squared in [0, 1] (proportion variance explained)
- Effect size CIs: eta_ci_lower >= 0, eta_ci_upper <= 1

*Data Quality:*
- All 3 ANOVAs completed successfully
- Both uncorrected and corrected p-values present (Decision D068)
- Effect sizes computed with confidence intervals
- Assumption check results for all DVs available

*Log Validation:*
- Required patterns: "3 ANOVAs completed", "Assumption checks complete", "Dual p-values reported"
- Required patterns: "VALIDATION - PASS"
- Forbidden patterns: "ERROR", "convergence failed", "assumption check failed"
- Acceptable warnings: "normality violation - non-parametric alternative noted"

**Expected Behavior on Validation Failure:**
Raise error with specific ANOVA failure. If assumptions violated, ensure alternative methods reported alongside parametric results. Log to logs/step03_anova_comparisons.log.

---

### Step 4: Correlation Analysis with Bootstrap CIs

**Dependencies:** Step 2 (calibration groups created)
**Complexity:** Medium (~12 minutes with bootstrap)

**Purpose:** Examine correlations between calibration quality (continuous residual) and cognitive reserve indicators with bootstrap confidence intervals

**Input:**
- data/step02_calibration_groups.csv (residual scores as continuous calibration measure)
- Variables: residual (calibration quality), education, rpm, age

**Processing:**
- Compute Pearson correlations between calibration residual and each reserve indicator:
  1. Calibration residual vs education
  2. Calibration residual vs RPM
  3. Calibration residual vs age
- For each correlation, implement bootstrap confidence intervals:
  - Method: Participant-level bootstrap (preserves any within-participant structure)
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Resampling: WITH replacement
  - CI computation: percentile method (2.5th, 97.5th percentiles for 95% CI)
- Multiple comparison correction:
  - Family: Within-RQ correlations (3 tests, combined with 3 ANOVAs = 6 total)
  - Bonferroni: alpha = 0.05/6 = 0.0083 per test
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Effect size interpretation:
  - Small: r = 0.10, Medium: r = 0.30, Large: r = 0.50
  - Document practical significance alongside statistical significance

**Output:**
- data/step04_correlations.csv (correlations, p-values, bootstrap CIs)
- data/step04_bootstrap_distributions.csv (full bootstrap results for inspection)

**Validation Requirement:**
Validation tools MUST be used after correlation and bootstrap execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_correlations.csv: 3 rows x 8 columns
- Columns: variable_pair, r, p_uncorrected, p_bonferroni, ci_lower, ci_upper, n_boot, effect_size
- data/step04_bootstrap_distributions.csv: 3000 rows (3 correlations x 1000 iterations)

*Value Ranges:*
- r in [-1, 1] (correlation coefficient bounds)
- p_uncorrected in [0, 1], p_bonferroni in [0, 1]  
- ci_lower <= r <= ci_upper (correlation within bootstrap CI)
- n_boot = 1000 for all correlations (complete bootstrap)

*Data Quality:*
- All 3 correlations completed successfully
- Bootstrap CIs computed for all correlations
- Dual p-value reporting (uncorrected and corrected)
- Effect size classifications provided (small/medium/large)

*Log Validation:*
- Required patterns: "3 correlations computed", "Bootstrap complete: 1000 iterations each"
- Required patterns: "Dual p-values reported", "VALIDATION - PASS"  
- Forbidden patterns: "ERROR", "bootstrap failed", "correlation computation error"
- Acceptable warnings: "weak correlation detected" (expected for exploratory analysis)

**Expected Behavior on Validation Failure:**
Raise error with specific correlation failure details. If bootstrap fails, report parametric CIs as alternative. Log to logs/step04_correlations_bootstrap.log.

---

### Step 5: Effect Size Calculations and Power Analysis

**Dependencies:** Steps 3-4 (ANOVA and correlation results)
**Complexity:** Medium (~8 minutes)

**Purpose:** Compute comprehensive effect sizes for group comparisons and assess post-hoc power for detecting meaningful differences

**Input:**
- data/step03_anova_results.csv (ANOVA F-statistics and group means)
- data/step04_correlations.csv (correlation coefficients)
- Group descriptive statistics from Step 2

**Processing:**
- Compute Cohen's d for all pairwise group comparisons:
  - Well-calibrated vs Overconfident (for each of 3 DVs)
  - Well-calibrated vs Underconfident (for each of 3 DVs)  
  - Overconfident vs Underconfident (for each of 3 DVs)
  - Total: 9 pairwise effect sizes
- Effect size computation:
  - Method: Pooled standard deviation formula
  - Include 95% CIs using non-central t-distribution
  - Classification: Small d=0.2, Medium d=0.5, Large d=0.8
- Post-hoc power analysis:
  - Type: Post-hoc power for ANOVA F-tests
  - Given: N per group, observed effect sizes, alpha = 0.0083 (Bonferroni corrected)
  - Calculate: achieved power for observed effects
  - Software: statsmodels.stats.power.FTestAnovaPower()
  - Target: 0.80 power benchmark
  - If power < 0.80: acknowledge limitation and minimum detectable effect size
- For correlations, compute achieved power using sample size N=80-100

**Output:**
- data/step05_effect_sizes.csv (Cohen's d for all pairwise comparisons)
- data/step05_power_analysis.csv (achieved power for ANOVAs and correlations)

**Validation Requirement:**
Validation tools MUST be used after effect size and power calculations.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_effect_sizes.csv: 9 rows x 7 columns (pairwise Cohen's d)
- Columns: comparison, dv, cohens_d, d_ci_lower, d_ci_upper, classification, n1, n2
- data/step05_power_analysis.csv: 6 rows (3 ANOVAs + 3 correlations)

*Value Ranges:*
- cohens_d typically in [-2, 2] (reasonable range for group differences)
- d_ci_lower <= cohens_d <= d_ci_upper (effect size within CI)
- achieved_power in [0, 1] (power proportion)
- alpha = 0.0083 for all tests (Bonferroni correction applied)

*Data Quality:*
- All 9 pairwise comparisons computed successfully
- Effect size CIs exclude infinity or undefined values
- Power calculations successful for all 6 statistical tests
- Classifications (small/medium/large) assigned correctly

*Log Validation:*
- Required patterns: "9 effect sizes computed", "Power analysis complete for 6 tests"
- Required patterns: "Alpha corrected: 0.0083", "VALIDATION - PASS"
- Forbidden patterns: "ERROR", "power calculation failed", "undefined effect size"
- Acceptable warnings: "low power detected" (expected for exploratory study)

**Expected Behavior on Validation Failure:**
Raise error with specific calculation failure. For undefined effect sizes (identical groups), set d=0 with appropriate CI. Log to logs/step05_effect_sizes_power.log.

---

### Step 6: Sensitivity Analysis and Robustness Checks

**Dependencies:** Steps 1-5 (complete primary analysis)
**Complexity:** High (~12 minutes with re-analysis)

**Purpose:** Test robustness of findings through outlier exclusion and alternative calibration grouping methods

**Input:**
- data/step01_merged_data.csv (original merged data)
- data/step02_calibration_groups.csv (original grouping method)

**Processing:**
- Outlier Detection and Exclusion:
  - Method: Cook's distance > 4/n for each DV in Step 3 ANOVAs
  - Identify multivariate outliers using Mahalanobis distance
  - Document number and characteristics of outliers
  - Re-run Steps 3-5 with outliers excluded
  - Compare results: effect sizes, significance, group means
- Alternative Grouping Method:
  - Method: Tertile split instead of SD-based cutoffs
  - Create three equal-sized groups based on residual distribution
  - Re-run Steps 3-5 with tertile groups
  - Compare results with original SD-based grouping
- Cross-validation of group stability:
  - Bootstrap group membership 100 times (seed=42)
  - Assess how often participants remain in same group
  - Flag participants with unstable group membership
- Document sensitivity analysis results:
  - Which findings are robust across methods?
  - Which results are sensitive to outliers or grouping method?
  - Overall conclusion about robustness of primary findings

**Output:**
- data/step06_outlier_analysis.csv (outlier identification and exclusion results)
- data/step06_tertile_reanalysis.csv (results with tertile grouping)
- data/step06_robustness_summary.csv (comparison across methods)

**Validation Requirement:**
Validation tools MUST be used after sensitivity analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_outlier_analysis.csv: variable rows x 6 columns
- Contains outlier counts, Cook's D thresholds, exclusion decisions
- data/step06_tertile_reanalysis.csv: matches Step 3 format with tertile groups
- data/step06_robustness_summary.csv: comparison table across methods

*Value Ranges:*
- outlier_count in [0, 10] (reasonable range for N=80-100)
- cooks_d_threshold = 4/N (correct threshold calculation)
- Tertile groups each have n = total_n/3 +/- 2 (approximately equal)
- effect_size_change within [-1, 1] (reasonable stability range)

*Data Quality:*
- Outlier detection completed for all 3 DVs
- Tertile reanalysis produces valid group comparisons
- Robustness summary covers all key findings from primary analysis
- No undefined or missing sensitivity analysis results

*Log Validation:*
- Required patterns: "Outlier analysis complete", "Tertile reanalysis complete"
- Required patterns: "Robustness assessment complete", "VALIDATION - PASS"
- Forbidden patterns: "ERROR", "reanalysis failed", "undefined comparison"
- Acceptable warnings: "substantial outlier influence detected" (informs interpretation)

**Expected Behavior on Validation Failure:**
Log specific sensitivity analysis failure. If outlier exclusion fails, proceed with full sample but note limitation. If tertile grouping fails, document as limitation. Log to logs/step06_sensitivity_analysis.log.

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (dependency check results)
- data/step01_merged_data.csv (theta, confidence, cognitive reserve data)  
- data/step02_calibration_groups.csv (group assignments and residuals)
- data/step02_group_descriptives.csv (descriptive statistics by group)
- data/step03_anova_results.csv (group comparisons with dual p-values)
- data/step03_assumption_checks.csv (normality and homoscedasticity tests)
- data/step03_posthoc_comparisons.csv (Tukey HSD pairwise results)
- data/step04_correlations.csv (calibration-reserve correlations with bootstrap CIs)
- data/step04_bootstrap_distributions.csv (full bootstrap results)
- data/step05_effect_sizes.csv (Cohen's d for all group comparisons)
- data/step05_power_analysis.csv (achieved power analysis results)
- data/step06_outlier_analysis.csv (outlier detection and exclusion)
- data/step06_tertile_reanalysis.csv (alternative grouping results)
- data/step06_robustness_summary.csv (sensitivity analysis summary)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_merge.log
- logs/step02_create_groups.log
- logs/step03_anova_comparisons.log
- logs/step04_correlations_bootstrap.log
- logs/step05_effect_sizes_power.log
- logs/step06_sensitivity_analysis.log

### Plots (EMPTY until rq_plots runs)
Note: rq_plots will create visualization source CSVs in data/ folder:
- data/stepXX_calibration_groups_plot_data.csv (for group comparison plots)
- data/stepXX_correlation_scatter_plot_data.csv (for calibration-reserve scatter plots)

### Results (EMPTY until rq_results runs)
Note: rq_results will create results/calibration_reserve_summary.md

---

## Expected Data Formats

### Step-to-Step Transformations
- Step 0->1: Dependency validation ensures data availability
- Step 1->2: Merged data provides complete dataset for calibration analysis
- Step 2->3: Group assignments enable between-group comparisons
- Step 2->4: Continuous residuals enable correlation analysis  
- Step 3,4->5: Statistical results feed into effect size and power calculations
- Step 1-5->6: Complete primary analysis enables sensitivity testing

### Column Naming Conventions
- UID: participant identifier (consistent across all files)
- theta_all: overall episodic memory ability (IRT scale)
- confidence_theta: confidence ratings on IRT scale  
- residual: standardized confidence-accuracy residual (calibration quality)
- group: calibration group assignment (Well-calibrated/Overconfident/Underconfident)
- education: years of education (cognitive reserve indicator)
- rpm: RPM total score (fluid intelligence indicator)
- age: participant age in years
- p_uncorrected: uncorrected p-value (Decision D068)
- p_bonferroni: Bonferroni-corrected p-value (Decision D068)

### Data Type Constraints
- UID: string/object (non-nullable, unique)
- Continuous measures: float64 (nullable only during intermediate processing)
- Count measures (education, rpm, age): int64 (non-nullable in final datasets)
- Group assignments: categorical/string (non-nullable, limited values)
- Statistical results: float64 (non-nullable, specific ranges per measure type)

---

## Cross-RQ Dependencies

**Ch5 5.1.1 Dependency:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/theta_all_scores.csv  
- Fallback pattern: results/ch5/5.1.1/data/*theta*.csv
- Expected content: UID, theta_all columns with 100 participants
- Required for: Overall episodic memory accuracy measure

**Ch6 Confidence Dependency:**  
- Primary: results/ch6/*/data/*confidence*theta*.csv (multiple potential Ch6 RQs)
- Alternative: results/ch6/*/data/confidence_calibrated.csv
- Fallback: results/ch6/*/data/confidence_ratings.csv + local calibration
- Expected content: UID, confidence_theta columns with 100 participants  
- Required for: Confidence ratings on comparable IRT scale

**Master Data Dependency:**
- Path: data/cache/master.xlsx
- Required columns: UID, EDUC_YEARS, RPM_TOTAL, AGE
- Expected: 100 participants with complete cognitive test data
- Required for: Cognitive reserve indicators

**Dependency Validation:** Step 0 handles all cross-RQ validation with comprehensive fallback logic.

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
[Full 4-layer validation structure provided above]

#### Step 1: Extract and Merge Data  
[Full 4-layer validation structure provided above]

#### Step 2: Create Calibration Groups
[Full 4-layer validation structure provided above]

#### Step 3: One-Way ANOVA Comparisons
[Full 4-layer validation structure provided above]

#### Step 4: Correlation Analysis with Bootstrap CIs
[Full 4-layer validation structure provided above]

#### Step 5: Effect Size Calculations and Power Analysis  
[Full 4-layer validation structure provided above]

#### Step 6: Sensitivity Analysis and Robustness Checks
[Full 4-layer validation structure provided above]

---

## Summary

**Total Steps:** 7 (Step 0: validation + Steps 1-6: analysis)
**Estimated Runtime:** ~45 minutes (includes bootstrap and sensitivity analysis)
**Cross-RQ Dependencies:** Ch5 5.1.1 (theta scores), Ch6 (confidence ratings), master.xlsx (reserve indicators)
**Primary Outputs:** Calibration group comparisons on education/RPM/age with bootstrap CIs and sensitivity analysis
**Validation Coverage:** 100% (all 7 steps have 4-layer validation requirements)

**Key Hypothesis:** Well-calibrated individuals (high confidence matched with high accuracy) will show higher education and RPM scores compared to overconfident or underconfident groups, suggesting metacognitive awareness as a cognitive reserve indicator.

**Critical Methodological Notes:**
- Bonferroni correction for family of 6 tests (3 ANOVAs + 3 correlations): alpha = 0.0083
- Bootstrap CIs with 1000 iterations and seed=42 for reproducibility  
- Dual p-value reporting (Decision D068) for all significance tests
- Comprehensive assumption testing with remedial actions specified
- Sensitivity analysis addresses outliers and alternative grouping methods
- Power analysis acknowledges limitations for detecting small effects (f^2 < 0.10)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml  
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent with enhanced v5.1 specifications