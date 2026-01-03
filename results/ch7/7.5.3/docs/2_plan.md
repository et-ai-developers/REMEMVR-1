# Analysis Plan: RQ 7.5.3 - Memory Strategies Predicting Performance

**Research Question:** 7.5.3
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines relationships between self-reported memory strategies (rehearsal frequency, mnemonic use) and overall REMEMVR performance using theta_all scores. Analysis combines correlational analysis, group comparisons, and hierarchical regression with proper controls for individual differences.

**Pipeline:** Strategy-Performance Correlation + Hierarchical Regression
**Steps:** 8 total analysis steps (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** ~45 minutes (includes text coding, bootstrap CIs, cross-validation)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Enhanced v5.1 specifications: complete statistical implementation details
- Mandatory statistical procedures: CV, bootstrap, power analysis, remedial actions

**Critical Methodological Notes:**
- Text coding required for mnemonic strategy variables (inter-rater reliability check)
- Small expected effects (r ~ 0.18) with N=100 provide limited power (~50%)
- Bootstrap confidence intervals for robust inference when normality violated
- Cross-RQ dependency on Ch5 5.1.1 theta_all scores

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 5.1.1 outputs exist and master.xlsx accessible before proceeding

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/theta_all_scores.csv
- Fallback: results/ch5/5.1.1/data/*theta*.{csv,txt}
- Master data: data/cache/master.xlsx (STR questionnaire tags)
- Expected: theta_all scores for 100 participants

**Processing:**
- Check Ch5 5.1.1 status.yaml (rq_results = success)
- Locate theta_all file using pattern matching
- Verify file contains 100 participant records with theta_all column
- Check master.xlsx accessible and contains STR tags
- Test STR tag extraction for sample participant
- Log all dependency validation results

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Contains: Ch5 file path found, N participants verified, STR tag count

*Value Ranges:*
- Participant count = 100 (expected sample size)
- STR tags > 0 (questionnaire data exists)

*Data Quality:*
- Ch5 5.1.1 completed successfully (status = success)
- Theta file accessible and readable
- Master.xlsx contains expected STR questionnaire tags

*Log Validation:*
- Required patterns: "Ch5 dependency: PASS", "STR tags found: N"
- Forbidden patterns: "ERROR", "FAIL", "file not found"
- Acceptable warnings: "alternative path used"

**Expected Behavior on Validation Failure:**
If Ch5 5.1.1 incomplete or theta file missing: QUIT with specific error message.
If master.xlsx inaccessible: QUIT with "STR questionnaire data not available".

### Step 1: Extract Theta Scores and Demographics
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (~5 minutes)

**Purpose:** Load theta_all scores and basic demographic variables for analysis

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/theta_all_scores.csv
- Fallback: results/ch5/5.1.1/data/*theta*.{csv,txt}
- Expected columns: UID, theta_all
- Expected format: 100 rows x 2+ columns

**Processing:**
- Load theta_all scores using discovered file path from Step 0
- Extract UID and theta_all columns (primary analysis variables)
- Extract age and NART scores from master.xlsx for control analysis
- Verify all 100 participants have non-missing theta_all scores
- Compute basic descriptive statistics for theta_all distribution
- Check for extreme outliers (> 3 SD from mean)

**Output:**
- data/step01_theta_demographics.csv (UID, theta_all, age, nart_score)

**Validation Requirement:**
Validation tools MUST be used after theta extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_theta_demographics.csv: 100 rows x 4 columns
- Columns: UID (object), theta_all (float64), age (int64), nart_score (float64)

*Value Ranges:*
- theta_all in [-4, 4] (IRT ability scale, allowing for extreme scores)
- age in [18, 85] (adult participant range)
- nart_score in [0, 50] (NART vocabulary test scale)

*Data Quality:*
- All 100 participants present (no missing UIDs)
- No duplicate UIDs
- Missing data < 5% per variable
- No extreme outliers flagged initially

*Log Validation:*
- Required patterns: "Theta scores loaded: 100 participants", "Demographics merged successfully"
- Forbidden patterns: "ERROR", "missing data", "file corrupt"

**Expected Behavior on Validation Failure:**
Raise error with specific failure, log to logs/step01_extract_theta.log, quit immediately.

### Step 2: Extract and Code Strategy Variables
**Dependencies:** Step 1 (theta scores loaded)
**Complexity:** High (~15 minutes including text coding validation)

**Purpose:** Extract rehearsal frequency and mnemonic use variables from STR questionnaire responses with reliability checking

**Input:**
- data/cache/master.xlsx (STR questionnaire tags)
- Required tags: 
  - Rehearsal: {UID}-RVR-T{N}-STR-X-TNK1- (quantitative ratings)
  - Mnemonics: {UID}-RVR-T{N}-STR-X-MNE1- (text responses)
- Expected: 100 participants x 4 tests = 400 STR responses

**Processing:**
- Extract rehearsal frequency ratings from TNK1 tags (numeric scale)
- Compute mean rehearsal frequency across T1-T4 tests per participant
- Extract mnemonic strategy text responses from MNE1 tags
- Text coding for binary mnemonic use (yes/no):
  - Code random subsample (n=20, 20%) independently by two raters
  - Compute inter-rater reliability (Cohen's kappa)
  - Require kappa >= 0.80 for acceptable agreement
  - If kappa < 0.80: refine criteria and re-code until acceptable
- Apply validated coding scheme to all 100 participants
- Check for missing strategy data and compute prevalence statistics

**Output:**
- data/step02_strategy_variables.csv (UID, rehearsal_freq, mnemonic_use, reliability_kappa)
- data/step02_text_coding_validation.txt (inter-rater reliability results)

**Validation Requirement:**
Validation tools MUST be used after strategy variable extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_strategy_variables.csv: 100 rows x 4 columns
- Columns: UID (object), rehearsal_freq (float64), mnemonic_use (int64), reliability_kappa (float64)
- data/step02_text_coding_validation.txt: reliability report

*Value Ranges:*
- rehearsal_freq in [1, 7] (typical Likert scale range)
- mnemonic_use in [0, 1] (binary coding: 0=no, 1=yes)
- reliability_kappa >= 0.80 (acceptable inter-rater agreement)

*Data Quality:*
- All 100 participants have rehearsal frequency data
- Missing mnemonic responses < 10% (some participants may not respond)
- Inter-rater reliability meets threshold (kappa >= 0.80)
- Strategy use prevalence reported (N and % using mnemonics)

*Log Validation:*
- Required patterns: "Text coding kappa = X.XX", "Strategy extraction complete: 100 participants"
- Forbidden patterns: "ERROR", "reliability too low", "coding failed"

**Expected Behavior on Validation Failure:**
If kappa < 0.80: log warning, attempt coding refinement, proceed if kappa > 0.70.
If extraction fails: quit with specific STR tag parsing error.

### Step 3: Create Analysis Dataset
**Dependencies:** Steps 1-2 (theta scores + strategy variables)
**Complexity:** Low (~5 minutes)

**Purpose:** Merge theta scores with strategy variables and prepare final analysis dataset

**Input:**
- data/step01_theta_demographics.csv (theta scores and demographics)
- data/step02_strategy_variables.csv (strategy variables)

**Processing:**
- Merge datasets on UID (inner join to ensure complete cases)
- Verify successful merge for all participants with complete data
- Compute descriptive statistics for all variables
- Check correlations between rehearsal frequency and theta_all (preliminary)
- Check group sizes for mnemonic use comparison (minimum N=10 per group)
- Flag any extreme values or potential data quality issues

**Output:**
- data/step03_analysis_dataset.csv (UID, theta_all, age, nart_score, rehearsal_freq, mnemonic_use)

**Validation Requirement:**
Validation tools MUST be used after dataset creation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_analysis_dataset.csv: N rows x 6 columns (N <= 100 due to missing data)
- Columns: UID (object), theta_all (float64), age (int64), nart_score (float64), rehearsal_freq (float64), mnemonic_use (int64)

*Value Ranges:*
- Same ranges as Steps 1-2 (theta_all [-4,4], rehearsal_freq [1,7], etc.)
- N >= 90 (allow up to 10% missing data from strategy extraction)

*Data Quality:*
- No missing values in merged dataset (complete cases only)
- Both mnemonic groups have N >= 10 (adequate for t-test)
- Preliminary correlation r between rehearsal and theta computed

*Log Validation:*
- Required patterns: "Merge successful: N participants", "Mnemonic groups: N0=X, N1=Y"
- Forbidden patterns: "ERROR", "insufficient data", "empty groups"

**Expected Behavior on Validation Failure:**
If N < 80: quit with insufficient sample size error.
If either mnemonic group N < 10: proceed but flag underpowered t-test.

### Step 4: Primary Correlation Analysis
**Dependencies:** Step 3 (analysis dataset prepared)
**Complexity:** Medium (~8 minutes including bootstrap CIs)

**Purpose:** Examine correlation between rehearsal frequency and theta_all scores with robust confidence intervals

**Input:**
- data/step03_analysis_dataset.csv (complete analysis dataset)

**Processing:**
- Compute Pearson correlation between rehearsal_freq and theta_all
- Check normality assumptions (Shapiro-Wilk test for both variables)
- Compute Fisher's z-transformed 95% confidence interval
- Bootstrap confidence intervals:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Resample participants WITH replacement
  - CI computation: percentile method (2.5th, 97.5th percentiles)
- Test statistical significance (two-tailed test)
- Effect size interpretation using Cohen's conventions for correlations
- Create scatterplot data for visualization (saved to data/ folder)

**Output:**
- data/step04_correlation_results.csv (r, p_uncorrected, ci_lower, ci_upper, ci_lower_boot, ci_upper_boot)
- data/step04_correlation_plot_data.csv (rehearsal_freq, theta_all for plotting)

**Validation Requirement:**
Validation tools MUST be used after correlation analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_correlation_results.csv: 1 row x 6 columns
- Columns: r (float64), p_uncorrected (float64), ci_lower (float64), ci_upper (float64), ci_lower_boot (float64), ci_upper_boot (float64)
- data/step04_correlation_plot_data.csv: N rows x 2 columns (N = sample size)

*Value Ranges:*
- r in [-1, 1] (correlation coefficient bounds)
- p_uncorrected in [0, 1] (valid probability)
- CI bounds: ci_lower < r < ci_upper (valid confidence interval)
- Bootstrap CIs: reasonable overlap with parametric CIs

*Data Quality:*
- Single correlation result (no missing values)
- Bootstrap CIs computed successfully (1000 iterations)
- Plot data contains all analysis participants

*Log Validation:*
- Required patterns: "Correlation r = X.XX", "Bootstrap complete: 1000 iterations"
- Forbidden patterns: "ERROR", "convergence failed", "invalid correlation"

**Expected Behavior on Validation Failure:**
Raise error with specific correlation computation failure, log details, invoke g_debug for troubleshooting.

### Step 5: Mnemonic Use Group Comparison
**Dependencies:** Step 3 (analysis dataset prepared)
**Complexity:** Medium (~8 minutes including assumptions and effect sizes)

**Purpose:** Compare theta_all scores between mnemonic users and non-users using independent samples t-test

**Input:**
- data/step03_analysis_dataset.csv (analysis dataset with mnemonic_use groups)

**Processing:**
- Split dataset by mnemonic_use (0 = non-users, 1 = users)
- Check group sizes (minimum N=10 per group for adequate power)
- Test assumptions:
  - Normality: Shapiro-Wilk test per group
  - Homoscedasticity: Levene's test for variance equality
  - Independence: satisfied by design (between-subjects)
- Conduct independent samples t-test (equal variances assumed initially)
- If Levene p < 0.05: use Welch's t-test (unequal variances)
- If normality violated: report Mann-Whitney U as non-parametric alternative
- Compute effect size (Cohen's d) with 95% confidence interval
- Bootstrap confidence intervals for group difference:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Resample within groups, compute difference
  - CI: percentile method for mean difference

**Output:**
- data/step05_group_comparison.csv (t_stat, df, p_uncorrected, cohens_d, d_ci_lower, d_ci_upper, mean_diff_boot_ci_lower, mean_diff_boot_ci_upper)
- data/step05_group_descriptives.csv (group, N, mean, sd, se)

**Validation Requirement:**
Validation tools MUST be used after group comparison execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_group_comparison.csv: 1 row x 8 columns
- Columns: t_stat (float64), df (float64), p_uncorrected (float64), cohens_d (float64), d_ci_lower (float64), d_ci_upper (float64), mean_diff_boot_ci_lower (float64), mean_diff_boot_ci_upper (float64)
- data/step05_group_descriptives.csv: 2 rows x 5 columns (one per group)

*Value Ranges:*
- t_stat: any real number (t-statistic)
- df > 0 (degrees of freedom)
- p_uncorrected in [0, 1]
- cohens_d: any real number (effect size, typically [-3, 3])
- CIs: lower < upper (valid intervals)

*Data Quality:*
- Both groups present with adequate N
- All statistical tests completed successfully
- Effect sizes computed with confidence intervals
- Bootstrap completed (1000 iterations)

*Log Validation:*
- Required patterns: "T-test complete: t = X.XX", "Bootstrap group comparison: 1000 iterations"
- Forbidden patterns: "ERROR", "insufficient group size", "assumption violation unhandled"

**Expected Behavior on Validation Failure:**
If group sizes inadequate: proceed but flag underpowered analysis.
If statistical computation fails: quit with specific error, log details.

### Step 6: Hierarchical Regression with Controls
**Dependencies:** Steps 3-5 (primary analyses complete)
**Complexity:** Medium (~10 minutes including diagnostics and cross-validation)

**Purpose:** Test whether strategy effects remain significant after controlling for age and cognitive ability

**Input:**
- data/step03_analysis_dataset.csv (complete dataset with all variables)

**Processing:**
- Hierarchical regression approach:
  - Model 1 (demographics): theta_all ~ age + nart_score
  - Model 2 (add strategies): theta_all ~ age + nart_score + rehearsal_freq + mnemonic_use
- Fit both models using statsmodels.api.OLS
- Compare R-squared change with F-test for significance
- Extract standardized beta coefficients for all predictors in Model 2
- Check regression assumptions:
  - Normality: Shapiro-Wilk test on residuals
  - Homoscedasticity: Breusch-Pagan test
  - Multicollinearity: VIF for each predictor
  - Outliers: Cook's distance > 4/n
- Remedial actions if assumptions violated:
  - Normality p < 0.05: Report bootstrap CIs as primary inference
  - Heteroscedasticity p < 0.05: Add HC3 robust standard errors
  - VIF > 5: Document multicollinearity, consider ridge if VIF > 10
  - Outliers (Cook's D > 4/n): Report results with/without outliers
- Cross-validation assessment:
  - Implement 5-fold cross-validation using sklearn.model_selection.KFold
  - Random seed: 42 for reproducibility
  - Shuffle: True (randomize before splitting)
  - For each fold: fit Model 2 on training set (80%), evaluate on test (20%)
  - Compute mean and standard deviation of R-squared across folds
  - Flag overfitting if train-test R-squared gap > 0.10

**Output:**
- data/step06_hierarchical_regression.csv (model comparisons, R-squared change, F-test)
- data/step06_regression_coefficients.csv (predictors, beta, se, t, p_uncorrected, vif)
- data/step06_assumption_diagnostics.csv (assumption tests and remedial actions)
- data/step06_cross_validation.csv (fold-wise R-squared values and summary)

**Validation Requirement:**
Validation tools MUST be used after hierarchical regression execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_hierarchical_regression.csv: 2 rows x 5 columns (Model 1, Model 2)
- data/step06_regression_coefficients.csv: 5 rows x 6 columns (intercept + 4 predictors)
- data/step06_assumption_diagnostics.csv: 4 rows x 3 columns (test results)
- data/step06_cross_validation.csv: 6 rows (5 folds + summary)

*Value Ranges:*
- R-squared in [0, 1] (variance explained)
- F-statistic > 0 (model comparison)
- p-values in [0, 1]
- VIF >= 1 (variance inflation, 1 = no collinearity)
- Cross-validation R-squared reasonable (not negative, not > full-sample R²)

*Data Quality:*
- Both regression models converged successfully
- All assumption tests completed
- VIF computed for all predictors
- Cross-validation completed for all 5 folds

*Log Validation:*
- Required patterns: "Hierarchical regression complete", "5-fold CV complete", "Assumptions checked"
- Forbidden patterns: "ERROR", "convergence failed", "singular matrix"

**Expected Behavior on Validation Failure:**
If regression fails to converge: check for perfect multicollinearity, remove problematic predictors.
If assumptions severely violated: proceed with robust methods, flag limitations.

### Step 7: Multiple Comparisons Correction and Final Results
**Dependencies:** Steps 4-6 (all primary analyses complete)
**Complexity:** Low (~5 minutes)

**Purpose:** Apply multiple comparison corrections and compile final statistical results with dual p-value reporting

**Input:**
- data/step04_correlation_results.csv (correlation p-value)
- data/step05_group_comparison.csv (t-test p-value)
- Regression p-values from Step 6 (strategy predictors only)

**Processing:**
- Define analysis family: Within-RQ strategy comparisons
  - Test 1: Rehearsal frequency correlation
  - Test 2: Mnemonic use group comparison
  - Test 3: Rehearsal frequency in regression (controlling demographics)
  - Test 4: Mnemonic use in regression (controlling demographics)
  - Total: 4 tests
- Apply Bonferroni correction: alpha = 0.05/4 = 0.0125 per test
- Apply FDR correction using Benjamini-Hochberg procedure
- Compile results with Decision D068 dual reporting:
  - Report BOTH uncorrected AND corrected p-values
  - Format: p_uncorrected, p_bonferroni, p_fdr
- Effect size summary with confidence intervals
- Statistical power assessment:
  - Post-hoc power analysis for regression model
  - Given: N=sample_size, 4 predictors, alpha=0.0125 (Bonferroni)
  - Calculate: achieved power for observed R-squared
  - Use: statsmodels.stats.power.FTestAnovaPower()
  - Report: actual power for strategy effects

**Output:**
- data/step07_corrected_results.csv (all tests with dual p-values and corrections)
- data/step07_effect_sizes_summary.csv (consolidated effect sizes and CIs)
- data/step07_power_analysis.csv (post-hoc power calculations)

**Validation Requirement:**
Validation tools MUST be used after multiple comparisons correction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_corrected_results.csv: 4 rows x 6 columns (4 tests)
- Columns: test_name (object), p_uncorrected (float64), p_bonferroni (float64), p_fdr (float64), effect_size (float64), interpretation (object)
- data/step07_effect_sizes_summary.csv: 4 rows x 4 columns
- data/step07_power_analysis.csv: 1 row x 4 columns

*Value Ranges:*
- All p-values in [0, 1]
- p_bonferroni >= p_uncorrected (correction increases p-values)
- p_fdr between p_uncorrected and p_bonferroni (less conservative than Bonferroni)
- Power in [0, 1] (probability values)

*Data Quality:*
- All 4 tests represented in corrected results
- Dual p-value reporting complete (Decision D068)
- Effect sizes properly summarized with interpretations
- Power analysis successfully computed

*Log Validation:*
- Required patterns: "Multiple comparisons: 4 tests corrected", "Dual p-values computed (D068)"
- Forbidden patterns: "ERROR", "correction failed", "invalid p-values"

**Expected Behavior on Validation Failure:**
If correction computations fail: proceed with uncorrected results but flag limitation.
If power analysis fails: acknowledge limitation, proceed without power estimates.

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (dependency check results)
- data/step01_theta_demographics.csv (theta scores + demographics: 100x4)
- data/step02_strategy_variables.csv (strategy measures: 100x4)
- data/step02_text_coding_validation.txt (inter-rater reliability report)
- data/step03_analysis_dataset.csv (merged analysis data: ~90-100x6)
- data/step04_correlation_results.csv (correlation analysis: 1x6)
- data/step04_correlation_plot_data.csv (scatterplot data: Nx2)
- data/step05_group_comparison.csv (t-test results: 1x8)
- data/step05_group_descriptives.csv (group statistics: 2x5)
- data/step06_hierarchical_regression.csv (regression comparison: 2x5)
- data/step06_regression_coefficients.csv (predictor effects: 5x6)
- data/step06_assumption_diagnostics.csv (diagnostic tests: 4x3)
- data/step06_cross_validation.csv (CV results: 6 rows)
- data/step07_corrected_results.csv (multiple comparisons: 4x6)
- data/step07_effect_sizes_summary.csv (effect size compilation: 4x4)
- data/step07_power_analysis.csv (power calculations: 1x4)

### Logs (ONLY execution logs)
- logs/step01_extract_theta.log (data extraction)
- logs/step02_strategy_coding.log (text coding process)
- logs/step03_merge_datasets.log (data preparation)
- logs/step04_correlation_analysis.log (correlation computation)
- logs/step05_group_comparison.log (t-test analysis)
- logs/step06_hierarchical_regression.log (regression analysis)
- logs/step07_corrections.log (multiple comparisons)

### Plots (EMPTY until rq_plots runs)
Note: Step 4 creates step04_correlation_plot_data.csv in data/ folder for later plotting

### Results (EMPTY until rq_results runs)
Note: rq_results will create comprehensive summary.md using all step outputs

---

## Expected Data Formats

### Step-to-Step Transformations
1. **Step 0->1:** Dependency validation enables theta score extraction
2. **Step 1->2:** Theta scores provide participant list for strategy extraction
3. **Step 2->3:** Strategy variables merge with theta scores on UID
4. **Step 3->4:** Analysis dataset enables correlation analysis
5. **Step 3->5:** Analysis dataset enables group comparison
6. **Step 6:** Uses Step 3 dataset for hierarchical regression
7. **Step 7:** Consolidates p-values from Steps 4-6 for correction

### Column Naming Conventions
- **UID:** Participant identifier (consistent across all files)
- **theta_all:** Overall memory performance score (IRT scale)
- **rehearsal_freq:** Mean rehearsal frequency rating (1-7 scale)
- **mnemonic_use:** Binary mnemonic strategy use (0=no, 1=yes)
- **p_uncorrected, p_bonferroni, p_fdr:** Dual p-value reporting (Decision D068)

### Data Type Constraints
- **UID:** String/object (non-nullable)
- **Numeric scores:** Float64 with defined ranges
- **Group variables:** Integer (0/1 for binary)
- **P-values:** Float64 in [0,1], non-nullable
- **Missing data tolerance:** <10% except for complete-case analyses

---

## Cross-RQ Dependencies

**Primary Dependency:** Ch5 5.1.1 (theta_all scores)

**Required Files:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/theta_all_scores.csv
- Fallback pattern: results/ch5/5.1.1/data/*theta*.{csv,txt}

**Expected Content:**
- Theta_all scores for all 100 participants
- UID column for merging with strategy data
- Scores on IRT scale (approximately [-4, 4] range)

**Fallback Plan:**
- If Ch5 5.1.1 incomplete: QUIT with clear dependency error
- If file name differs: use pattern matching to locate theta scores
- If format differs: adapt extraction logic but verify content validity

**Verification Steps:**
- Check Ch5 5.1.1 status.yaml for completion
- Verify file accessibility and format
- Validate expected sample size and data ranges

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution. This is the foundation of v4.X architecture preventing cascading failures.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
- **Output verification:** Dependency check file created
- **Content validation:** Ch5 status confirmed, file paths verified
- **Quality checks:** Expected participant count, STR tag availability
- **Log patterns:** Success/failure patterns documented

#### Step 1: Extract Theta Scores
- **Output verification:** CSV with 100 participants, required columns
- **Range validation:** Theta scores in expected IRT range
- **Quality checks:** No missing UIDs, reasonable score distribution
- **Log patterns:** Successful extraction confirmation

#### Step 2: Strategy Variable Coding
- **Output verification:** Strategy variables extracted, reliability computed
- **Content validation:** Inter-rater kappa >= 0.80, binary coding correct
- **Quality checks:** Strategy prevalence reasonable, missing data < 10%
- **Log patterns:** Text coding completion, reliability achievement

#### Step 3: Analysis Dataset Creation
- **Output verification:** Merged dataset with complete cases
- **Content validation:** All required variables present
- **Quality checks:** Adequate group sizes, no missing values
- **Log patterns:** Successful merge, group size confirmation

#### Step 4: Correlation Analysis
- **Output verification:** Correlation results with confidence intervals
- **Statistical validation:** Bootstrap completed, CIs valid
- **Quality checks:** Correlation in valid range [-1,1]
- **Log patterns:** Analysis completion, bootstrap success

#### Step 5: Group Comparison
- **Output verification:** T-test results with effect sizes
- **Statistical validation:** Assumptions checked, remedial actions applied
- **Quality checks:** Group differences computed correctly
- **Log patterns:** T-test completion, assumption handling

#### Step 6: Hierarchical Regression
- **Output verification:** Regression models fit, cross-validation complete
- **Statistical validation:** Assumptions checked, VIF computed
- **Quality checks:** Model convergence, reasonable coefficients
- **Log patterns:** Regression success, CV completion

#### Step 7: Multiple Comparisons
- **Output verification:** Corrected p-values computed
- **Content validation:** Dual reporting (Decision D068) complete
- **Quality checks:** Corrections properly applied
- **Log patterns:** Correction completion, dual p-values confirmed

---

## Summary

**Total Steps:** 8 (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** ~45 minutes
**Cross-RQ Dependencies:** Ch5 5.1.1 (theta_all scores)
**Primary Outputs:** Strategy-performance correlations, group comparisons, hierarchical regression results
**Validation Coverage:** 100% (all 8 steps have 4-layer validation requirements)

**Key Hypothesis:** Small positive effects of memory strategy use on episodic memory performance, with rehearsal frequency showing correlation r ~ 0.18 and mnemonic users showing marginally higher performance.

**Critical Methodological Notes:**
- Text coding reliability mandatory for mnemonic variable (kappa >= 0.80)
- Small expected effects require careful interpretation of statistical power (~50% for r=0.18)
- Bootstrap confidence intervals provide robust inference when parametric assumptions violated
- Cross-validation assesses generalizability of regression model (gap threshold < 0.10)
- Decision D068 dual p-value reporting for all primary tests
- Multiple comparison family limited to 4 within-RQ strategy tests (Bonferroni alpha = 0.0125)

**Enhanced v5.1 Compliance:**
- Random seed=42 specified for ALL randomized procedures (bootstrap, CV)
- Complete statistical implementation details (iterations, methods, thresholds)
- Remedial actions specified for assumption violations
- Cross-RQ dependencies with fallback paths
- Power analysis with post-hoc calculations
- Multiple comparison corrections with explicit family definitions

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml (specify exact tools needed)
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml (execution sequence)
4. g_code reads analysis -> generates executable code with proper error handling

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent with v5.1 enhancements