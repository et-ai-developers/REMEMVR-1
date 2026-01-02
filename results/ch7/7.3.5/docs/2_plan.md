# Analysis Plan: RQ 7.3.5 - Confidence-accuracy gap predicting cognitive reserve

**Research Question:** 7.3.5
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This analysis examines whether calibration quality (confidence-accuracy correspondence) predicts cognitive reserve indicators. Uses ANOVA to compare calibration groups (well-calibrated, overconfident, underconfident) on education, RPM scores, and age. Includes correlation analysis and sensitivity testing with comprehensive validation procedures.

**Pipeline:** ANOVA and correlation analysis with calibration groups
**Steps:** 7 total analysis steps (Step 0: validation + Steps 1-6: analysis)
**Estimated Runtime:** ~45 minutes including bootstrap procedures

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Bootstrap confidence intervals for robust inference
- Comprehensive assumption testing with remedial actions

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 and Ch6 outputs exist before proceeding with calibration analysis

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv (overall episodic memory theta)
- Alternative: results/ch5/5.1.1/data/*theta*.csv 
- Fallback: results/ch5/5.1.1/data/step*overall*.csv
- Ch6 confidence data: results/ch6/*/data/confidence_theta_scores.csv
- Master file: data/cache/master.xlsx (cognitive test scores)
- Expected content: theta_all scores for 100 participants, confidence ratings scaled to theta

**Processing:**
- Check Ch5 5.1.1 status: rq_results = success in status.yaml
- Locate theta score files using multiple patterns
- Verify Ch6 confidence analysis completed (any Ch6 RQ with confidence outputs)
- Check master.xlsx accessibility and required columns (Education, RPM, Age)
- Log all validation checks with file discovery details
- Set random seed: 42 for all subsequent randomized procedures

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Contains path verification for 3+ required data sources

*Value Ranges:*
- N/A (text file with boolean validation results)

*Data Quality:*
- All required dependencies confirmed available
- File paths logged for downstream steps
- No missing critical data sources

*Log Validation:*
- Required patterns: "Ch5 5.1.1: FOUND", "Ch6 confidence: FOUND", "Master file: FOUND"
- Required patterns: "Validation complete: ALL DEPENDENCIES AVAILABLE"
- Forbidden patterns: "ERROR", "MISSING", "not found"

**Expected Behavior on Validation Failure:**
Quit immediately with specific missing dependency error. Log to logs/step00_validate_dependencies.log and invoke g_debug.

### Step 1: Extract and Prepare Core Data
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Medium (~8 minutes including quality checks)

**Purpose:** Load theta scores, confidence ratings, and cognitive reserve indicators into unified analysis dataset

**Input:**
- results/ch5/5.1.1/data/step03_theta_scores.csv (theta_all for overall ability)
- results/ch6/*/data/confidence_theta_scores.csv (theta-scaled confidence)
- data/cache/master.xlsx (Education, RPM, Age columns)

**Processing:**
- Load theta_all scores (overall episodic memory ability)
- Load confidence_theta scores (confidence scaled to theta metric)
- Extract cognitive reserve indicators: Education (years), RPM (raw scores), Age
- Merge datasets on UID with inner join (complete cases only)
- Compute missingness rates per variable (<5% acceptable)
- Create merged dataset: UID, theta_all, confidence_theta, Education, RPM, Age
- Random seed: 42 for any tie-breaking in data processing
- Log data quality: N participants, missing rates, descriptive statistics

**Output:**
- data/step01_merged_data.csv

**Validation Requirement:**
Validation tools MUST be used after data extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_merged_data.csv: 100 rows x 6 columns
- Columns: UID (object), theta_all (float64), confidence_theta (float64), Education (int64), RPM (int64), Age (int64)

*Value Ranges:*
- theta_all in [-3, 3] (IRT ability scale)
- confidence_theta in [-3, 3] (theta-scaled confidence)
- Education in [8, 25] (years of education)
- RPM in [10, 60] (raw score range)
- Age in [20, 70] (study age range)

*Data Quality:*
- Exactly 100 participants (complete cases)
- No missing values (inner join requirement)
- No duplicate UIDs
- All values within expected ranges

*Log Validation:*
- Required patterns: "Data merged: 100 participants", "Missing rate: 0.0%"
- Required patterns: "VALIDATION - PASS"
- Forbidden patterns: "ERROR", "missing values", "duplicate UIDs"

**Expected Behavior on Validation Failure:**
Raise error with specific data quality issue. Log to logs/step01_extract_data.log. Quit immediately and invoke g_debug.

### Step 2: Create Calibration Groups
**Dependencies:** Step 1 (merged data)
**Complexity:** Medium (~10 minutes including validation)

**Purpose:** Create calibration groups based on confidence-accuracy correspondence and validate group meaningfulness

**Input:**
- data/step01_merged_data.csv

**Processing:**
- Compute confidence-accuracy correlation residuals:
  - Pearson correlation: r = cor(theta_all, confidence_theta)
  - Residuals: residual_i = confidence_theta_i - (r * theta_all_i)
- Define calibration groups using 0.5 SD cutoffs:
  - Well-calibrated: -0.5 SD <= residual <= +0.5 SD
  - Overconfident: residual > +0.5 SD (confidence exceeds predicted)
  - Underconfident: residual < -0.5 SD (confidence below predicted)
- Validate group sizes: minimum n=20 per group required
- If imbalanced, use forced tertiles as backup grouping method
- Validate group meaningfulness:
  - Compute confidence-accuracy bias by group: bias = confidence_theta - theta_all
  - Expected ordering: underconfident < well-calibrated < overconfident
- Random seed: 42 for any tie-breaking in group assignment

**Output:**
- data/step02_calibration_groups.csv
- data/step02_group_validation.txt

**Validation Requirement:**
Validation tools MUST be used after calibration grouping execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_calibration_groups.csv: 100 rows x 8 columns
- Columns: UID, theta_all, confidence_theta, calibration_group, residual, bias, Education, RPM, Age
- data/step02_group_validation.txt: group descriptives and validation results

*Value Ranges:*
- calibration_group in ["well_calibrated", "overconfident", "underconfident"]
- residual in [-2, 2] (standardized residuals)
- bias in [-2, 2] (confidence - accuracy difference)
- Group sizes: each n >= 20

*Data Quality:*
- All 100 participants assigned to groups
- Group size balance: largest/smallest ratio < 2.0
- Bias ordering validated: underconfident < well_calibrated < overconfident
- No participants excluded due to group assignment

*Log Validation:*
- Required patterns: "Groups created:", "Well-calibrated: N=", "Validation PASS: bias ordering correct"
- Forbidden patterns: "ERROR", "group size < 20", "validation FAILED"

**Expected Behavior on Validation Failure:**
If group sizes < 20 or bias ordering wrong, switch to forced tertile grouping. Log all attempts. Quit if tertile method also fails validation.

### Step 3: One-Way ANOVA Comparisons
**Dependencies:** Step 2 (calibration groups)
**Complexity:** High (~12 minutes including assumption testing)

**Purpose:** Compare calibration groups on cognitive reserve indicators using ANOVA with comprehensive assumption testing

**Input:**
- data/step02_calibration_groups.csv

**Processing:**
- Conduct three one-way ANOVAs: Education ~ calibration_group, RPM ~ calibration_group, Age ~ calibration_group
- Implementation: scipy.stats.f_oneway with custom effect size calculation
- Test ANOVA assumptions for each outcome:
  - Normality: Shapiro-Wilk test per group (3 groups x 3 outcomes = 9 tests)
  - Homogeneity: Levene's test per outcome (3 tests)
  - Outliers: Box plot rule (>1.5 x IQR) with visualization
- Remedial actions if assumptions violated:
  - Normality p < 0.05: Report Kruskal-Wallis as backup, use bootstrap CIs
  - Heteroscedasticity p < 0.05: Report Welch's ANOVA
  - Outliers present: Report with/without outliers
- Multiple comparison correction:
  - Family: Within-RQ (3 ANOVAs = 3 tests)
  - Bonferroni: alpha = 0.05/3 = 0.0167 per test
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Effect sizes: eta-squared for each ANOVA with 95% CIs
- Post-hoc tests: Tukey HSD if significant group effects
- Random seed: 42 for bootstrap procedures if needed

**Output:**
- data/step03_anova_results.csv
- data/step03_assumption_tests.csv
- data/step03_posthoc_comparisons.csv

**Validation Requirement:**
Validation tools MUST be used after ANOVA execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_anova_results.csv: 3 rows x 8 columns
- Columns: outcome, F_stat, df1, df2, p_uncorrected, p_bonferroni, eta_squared, eta_ci_lower, eta_ci_upper
- data/step03_assumption_tests.csv: assumption test results for all ANOVAs
- data/step03_posthoc_comparisons.csv: pairwise group comparisons if significant

*Value Ranges:*
- F_stat > 0 (F-statistic positive)
- p_uncorrected, p_bonferroni in [0, 1] (valid probabilities)
- eta_squared in [0, 1] (proportion of variance)
- df1 = 2 (3 groups - 1), df2 = 97 (100 - 3)

*Data Quality:*
- All 3 ANOVAs completed (Education, RPM, Age)
- Dual p-values present (Decision D068)
- Effect size confidence intervals valid (lower <= eta_squared <= upper)
- Assumption test results for all outcomes

*Log Validation:*
- Required patterns: "ANOVA complete: 3 outcomes", "Assumption testing complete"
- Required patterns: "Dual p-values computed (D068)"
- Forbidden patterns: "ERROR", "convergence failed", "assumption FAILED without remedial"

**Expected Behavior on Validation Failure:**
Raise error with specific ANOVA failure. If assumption violations severe, switch to non-parametric alternatives and document. Log to logs/step03_anova_analysis.log.

### Step 4: Correlation Analysis with Bootstrap CIs
**Dependencies:** Step 2 (calibration groups)
**Complexity:** Medium (~10 minutes including bootstrap)

**Purpose:** Examine correlations between calibration quality (continuous) and cognitive reserve indicators with robust confidence intervals

**Input:**
- data/step02_calibration_groups.csv

**Processing:**
- Create continuous calibration quality measure: calibration_quality = -abs(residual) (higher = better calibrated)
- Compute Pearson correlations:
  - calibration_quality with Education
  - calibration_quality with RPM  
  - calibration_quality with Age
- Test correlation assumptions:
  - Linearity: Scatterplot inspection and visual assessment
  - Bivariate normality: Shapiro-Wilk test on both variables
  - Outliers: Leverage and influence measures (Cook's D > 4/n)
- Bootstrap 95% confidence intervals:
  - Iterations: 1000
  - Random seed: 42
  - Method: Participant-level resampling with replacement
  - CI computation: percentile method (2.5th, 97.5th percentiles)
- Remedial actions if assumptions violated:
  - Non-linearity detected: Report Spearman correlation as backup
  - Outliers present: Report with/without outliers
- Multiple comparison correction:
  - Family: Within-step (3 correlations)
  - Bonferroni: alpha = 0.05/3 = 0.0167 per test
  - Report BOTH uncorrected AND corrected p-values (Decision D068)

**Output:**
- data/step04_correlations.csv
- data/step04_scatterplots_data.csv
- data/step04_bootstrap_cis.csv

**Validation Requirement:**
Validation tools MUST be used after correlation analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_correlations.csv: 3 rows x 7 columns  
- Columns: outcome, r, p_uncorrected, p_bonferroni, ci_lower, ci_upper, n_bootstrap
- data/step04_bootstrap_cis.csv: 1000 bootstrap iterations x 3 correlations

*Value Ranges:*
- r in [-1, 1] (correlation coefficient range)
- p_uncorrected, p_bonferroni in [0, 1] (valid probabilities)
- ci_lower, ci_upper in [-1, 1] (correlation CI bounds)
- n_bootstrap = 1000 (iterations completed)

*Data Quality:*
- All 3 correlations computed (Education, RPM, Age)
- Bootstrap CIs valid (ci_lower <= r <= ci_upper typically)
- Dual p-values present (Decision D068)
- All 1000 bootstrap iterations completed successfully

*Log Validation:*
- Required patterns: "Correlations computed: 3", "Bootstrap complete: 1000 iterations"
- Required patterns: "Dual p-values computed (D068)"
- Forbidden patterns: "ERROR", "bootstrap failed", "CI computation failed"

**Expected Behavior on Validation Failure:**
If bootstrap fails, use analytical standard errors as backup. Log assumption violations and remedial actions taken. Raise error only if correlation computation fails entirely.

### Step 5: Effect Size Analysis and Interpretation
**Dependencies:** Steps 3-4 (ANOVA and correlations)
**Complexity:** Low (~5 minutes)

**Purpose:** Compute effect sizes for group comparisons and classify magnitude for interpretation

**Input:**
- data/step03_anova_results.csv
- data/step03_posthoc_comparisons.csv (if significant group effects)
- data/step04_correlations.csv

**Processing:**
- Compute Cohen's d for pairwise group comparisons:
  - Well-calibrated vs Overconfident on each outcome
  - Well-calibrated vs Underconfident on each outcome  
  - Overconfident vs Underconfident on each outcome
- Effect size classification:
  - Cohen's d: 0.2 (small), 0.5 (medium), 0.8 (large)
  - Correlation r: 0.1 (small), 0.3 (medium), 0.5 (large)
  - ANOVA eta-squared: 0.01 (small), 0.06 (medium), 0.14 (large)
- Practical significance assessment:
  - Flag effects meeting both statistical significance (corrected p < 0.0167) and meaningful size (d >= 0.3, r >= 0.25)
- Clinical significance evaluation:
  - Education differences: d >= 0.5 considered educationally meaningful
  - RPM differences: d >= 0.4 considered cognitively meaningful
- Random seed: 42 for any bootstrap effect size CIs if computed

**Output:**
- data/step05_effect_sizes.csv
- data/step05_interpretation_summary.txt

**Validation Requirement:**
Validation tools MUST be used after effect size analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_effect_sizes.csv: 9+ rows (3 pairwise x 3 outcomes minimum)
- Columns: comparison, outcome, cohens_d, magnitude, significant, meaningful
- data/step05_interpretation_summary.txt: text summary of findings

*Value Ranges:*
- cohens_d in [-3, 3] (reasonable effect size range)
- magnitude in ["small", "medium", "large", "negligible"]
- significant: boolean (TRUE/FALSE for statistical significance)
- meaningful: boolean (TRUE/FALSE for practical significance)

*Data Quality:*
- All pairwise comparisons included (minimum 9 rows)
- Effect size classifications consistent with standard thresholds
- Interpretation summary covers all major findings
- No missing effect size calculations

*Log Validation:*
- Required patterns: "Effect sizes computed:", "Interpretation complete"
- Required patterns: "Meaningful effects identified:"
- Forbidden patterns: "ERROR", "effect size failed", "division by zero"

**Expected Behavior on Validation Failure:**
Raise error with specific effect size calculation failure. If group variances zero (no variability), report as "insufficient variability for effect size calculation."

### Step 6: Sensitivity Analysis and Robustness Testing
**Dependencies:** Steps 2-5 (all main analyses)
**Complexity:** Medium (~8 minutes including re-analysis)

**Purpose:** Test robustness of findings through outlier exclusion and alternative grouping methods

**Input:**
- data/step02_calibration_groups.csv
- data/step03_anova_results.csv
- data/step04_correlations.csv

**Processing:**
- Outlier identification and exclusion:
  - Identify outliers using box plot rule (>1.5 x IQR) for each cognitive variable
  - Re-run ANOVAs and correlations excluding outliers
  - Compare results: document effect size changes
- Alternative calibration grouping:
  - Method 1: Forced tertiles (equal n per group)
  - Method 2: Confidence-accuracy difference scores (bias-based)
  - Re-run main analyses with alternative groupings
  - Compare effect sizes and significance patterns
- Power analysis:
  - Post-hoc power for observed effect sizes
  - Given: N=100, alpha=0.0167 (Bonferroni corrected)
  - Calculate: actual power for observed eta-squared values
  - Use: statsmodels.stats.power.FTestAnovaPower()
  - Report: power for each significant and non-significant effect
- Random seed: 42 for any randomized sensitivity procedures
- Document robustness: classify findings as robust/fragile based on consistency across analyses

**Output:**
- data/step06_sensitivity_outliers.csv
- data/step06_alternative_groupings.csv
- data/step06_power_analysis.csv
- data/step06_robustness_summary.txt

**Validation Requirement:**
Validation tools MUST be used after sensitivity analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_sensitivity_outliers.csv: comparison of main vs outlier-excluded results
- data/step06_alternative_groupings.csv: results with different calibration grouping methods  
- data/step06_power_analysis.csv: power calculations for all effects
- data/step06_robustness_summary.txt: overall robustness assessment

*Value Ranges:*
- Power values in [0, 1] (statistical power range)
- Effect size changes: document magnitude of differences
- Robustness classifications: "robust", "fragile", "inconclusive"

*Data Quality:*
- All sensitivity analyses completed successfully
- Outlier exclusion effects quantified
- Alternative grouping results documented
- Power analysis completed for all main effects

*Log Validation:*
- Required patterns: "Sensitivity analysis complete", "Power analysis complete"
- Required patterns: "Robustness classification:", "Alternative groupings tested"
- Forbidden patterns: "ERROR", "sensitivity failed", "power calculation error"

**Expected Behavior on Validation Failure:**
Document which sensitivity analyses failed and why. Continue with available results. Only quit if all sensitivity procedures fail, indicating fundamental data problems.

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt: Cross-RQ dependency verification
- data/step01_merged_data.csv: Combined theta, confidence, and cognitive reserve data
- data/step02_calibration_groups.csv: Group assignments and validation
- data/step02_group_validation.txt: Group meaningfulness validation results
- data/step03_anova_results.csv: One-way ANOVA results with dual p-values
- data/step03_assumption_tests.csv: ANOVA assumption test results
- data/step03_posthoc_comparisons.csv: Pairwise group comparisons
- data/step04_correlations.csv: Calibration-reserve correlations with bootstrap CIs
- data/step04_scatterplots_data.csv: Data for correlation visualizations
- data/step04_bootstrap_cis.csv: Bootstrap iteration results
- data/step05_effect_sizes.csv: Cohen's d and interpretation for group comparisons
- data/step05_interpretation_summary.txt: Effect size classification and meaningfulness
- data/step06_sensitivity_outliers.csv: Outlier exclusion sensitivity results
- data/step06_alternative_groupings.csv: Alternative calibration grouping results
- data/step06_power_analysis.csv: Post-hoc power calculations
- data/step06_robustness_summary.txt: Overall robustness assessment

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log: Dependency validation execution log
- logs/step01_extract_data.log: Data extraction and merging log
- logs/step02_create_groups.log: Calibration group creation and validation log
- logs/step03_anova_analysis.log: ANOVA analysis and assumption testing log
- logs/step04_correlation_analysis.log: Correlation and bootstrap analysis log
- logs/step05_effect_sizes.log: Effect size computation and interpretation log
- logs/step06_sensitivity_analysis.log: Sensitivity and robustness testing log

### Plots (EMPTY until rq_plots runs)
- Note: Step 4 creates scatterplot source data (step04_scatterplots_data.csv) in data/ folder
- Plot generation will be handled by rq_plots agent using this data

### Results (EMPTY until rq_results runs)
- Note: rq_results will create summary.md using outputs from all steps

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 -> Step 1:** Text validation file -> Core datasets loaded separately
**Step 1 -> Step 2:** Merged data (100 x 6) -> Merged data + groups (100 x 8) 
**Step 2 -> Step 3:** Group assignments -> ANOVA statistical results (3 x 8)
**Step 2 -> Step 4:** Group assignments -> Correlation results (3 x 7) + bootstrap samples
**Steps 3-4 -> Step 5:** Statistical results -> Effect sizes and interpretations
**Steps 2-5 -> Step 6:** All prior results -> Sensitivity analysis and robustness assessment

### Column Naming Conventions

**Core Variables:**
- UID: Participant identifier (string)
- theta_all: Overall episodic memory ability (float, IRT scale)
- confidence_theta: Confidence ratings scaled to theta metric (float)
- Education: Years of formal education (int)
- RPM: Ravens Progressive Matrices raw score (int)  
- Age: Chronological age in years (int)

**Derived Variables:**
- calibration_group: ["well_calibrated", "overconfident", "underconfident"] (string)
- residual: Confidence-accuracy correlation residual (float)
- bias: Simple confidence - accuracy difference (float)
- calibration_quality: Continuous calibration measure (float, -abs(residual))

### Data Type Constraints

**Non-nullable:** UID, theta_all, confidence_theta, Education, RPM, Age
**Nullable:** None (complete cases analysis)
**Range constraints:** All variables bounded to prevent outliers from corrupting analyses

---

## Cross-RQ Dependencies

**Required Ch5 Outputs:**
- results/ch5/5.1.1/data/step03_theta_scores.csv: Overall episodic memory theta scores
- Alternative paths: results/ch5/5.1.1/data/*theta*.csv, results/ch5/5.1.1/data/step*overall*.csv
- Expected format: UID column + theta_all column with IRT scale values [-3, 3]
- Fallback: If file not found, QUIT with "Ch5 5.1.1 theta scores not available"

**Required Ch6 Outputs:**
- results/ch6/*/data/confidence_theta_scores.csv: Confidence ratings scaled to theta
- Pattern search: results/ch6/*/data/*confidence*theta*.csv
- Expected format: UID column + confidence_theta column scaled to match theta metric
- Fallback: If file not found, QUIT with "Ch6 confidence data not available"

**Required Master Data:**
- data/cache/master.xlsx: Cognitive test scores and demographics
- Required columns: UID, Education, RPM, Age
- Expected ranges: Education [8, 25], RPM [10, 60], Age [20, 70]
- Fallback: If file not accessible, QUIT with "Master data file not available"

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
**4-Layer Validation Structure (Mandatory):**
- Output Files: step00_dependency_validation.txt with verification results
- Value Ranges: N/A (boolean validation flags)
- Data Quality: All dependencies confirmed available with logged paths
- Log Validation: Required success patterns, forbidden error patterns

#### Step 1: Extract and Prepare Data  
**4-Layer Validation Structure (Mandatory):**
- Output Files: step01_merged_data.csv with exact dimensions (100 x 6)
- Value Ranges: theta_all/confidence_theta [-3,3], Education [8,25], RPM [10,60], Age [20,70]
- Data Quality: Zero missing values, no duplicates, complete case analysis
- Log Validation: Required merge success patterns, forbidden missing data patterns

#### Step 2: Create Calibration Groups
**4-Layer Validation Structure (Mandatory):**  
- Output Files: step02_calibration_groups.csv (100 x 8), step02_group_validation.txt
- Value Ranges: Group sizes n>=20, residuals/bias [-2,2], bias ordering validated
- Data Quality: All participants grouped, balance ratio <2.0, meaningful group differences
- Log Validation: Required group creation patterns, forbidden validation failure patterns

#### Step 3: One-Way ANOVA Analysis
**4-Layer Validation Structure (Mandatory):**
- Output Files: Multiple CSV files with ANOVA results, assumption tests, post-hoc comparisons
- Value Ranges: F-statistics >0, p-values [0,1], eta-squared [0,1], valid degrees of freedom
- Data Quality: All 3 ANOVAs completed, dual p-values present, assumption tests conducted
- Log Validation: Required completion patterns, forbidden convergence failure patterns

#### Step 4: Correlation Analysis  
**4-Layer Validation Structure (Mandatory):**
- Output Files: Correlation results with bootstrap CIs and assumption diagnostics
- Value Ranges: Correlations [-1,1], p-values [0,1], CIs contain correlation typically
- Data Quality: 1000 bootstrap iterations completed, dual p-values present
- Log Validation: Required bootstrap success patterns, forbidden CI failure patterns

#### Step 5: Effect Size Analysis
**4-Layer Validation Structure (Mandatory):**
- Output Files: Effect sizes with classifications and interpretation summary
- Value Ranges: Cohen's d [-3,3], magnitude classifications consistent with thresholds
- Data Quality: All pairwise comparisons included, interpretations logically consistent
- Log Validation: Required computation patterns, forbidden calculation error patterns

#### Step 6: Sensitivity Analysis
**4-Layer Validation Structure (Mandatory):**
- Output Files: Multiple sensitivity analysis results and robustness summary
- Value Ranges: Power values [0,1], effect size changes documented
- Data Quality: All sensitivity procedures attempted, robustness classifications assigned
- Log Validation: Required completion patterns, acceptable partial failure patterns

---

## Summary

**Total Steps:** 7 (Step 0: validation + Steps 1-6: analysis)
**Estimated Runtime:** ~45 minutes including comprehensive bootstrap and sensitivity procedures
**Cross-RQ Dependencies:** Ch5 5.1.1 (theta scores), Ch6 confidence analysis, master.xlsx
**Primary Outputs:** ANOVA group comparisons, correlation analysis with bootstrap CIs, effect sizes
**Validation Coverage:** 100% (all 7 steps have 4-layer validation requirements)

**Key Hypothesis:** Well-calibrated individuals (accurate confidence-accuracy correspondence) show higher education and RPM scores compared to overconfident/underconfident groups, suggesting metacognitive awareness as cognitive reserve indicator.

**Critical Methodological Notes:**
- Novel residual-based calibration grouping requires validation for psychological meaningfulness
- Comprehensive assumption testing with non-parametric backups if violations detected
- Bootstrap confidence intervals provide robust inference under assumption violations
- Multiple comparison correction (Decision D068) controls family-wise error within RQ
- Post-hoc power analysis documents adequacy for detecting observed effect sizes
- Sensitivity analyses test robustness across different grouping methods and outlier handling

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml  
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent
  - Enhanced statistical specifications (v5.1): random seeds, bootstrap details, assumption testing
  - Comprehensive 4-layer validation for all steps
  - Cross-RQ dependency handling with fallback paths
  - Decision D068 dual p-value reporting throughout