# Analysis Plan: RQ 7.5.1 - Self-Report Predictors of REMEMVR Performance

**Research Question:** 7.5.1
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

**Research Question:** Do self-reported factors (typical sleep, education level, VR experience) predict REMEMVR performance?

**Analysis Approach:** Multiple regression with hierarchical entry, cross-validation, and comprehensive statistical validation. Tests whether lifestyle and experiential factors contribute unique variance to episodic memory performance beyond chronological age.

**Pipeline:** Multiple Linear Regression with Bootstrap Validation
**Steps:** 9 total analysis steps (Step 0: dependency validation + Steps 1-8: analysis)
**Estimated Runtime:** ~45 minutes (including bootstrap and cross-validation procedures)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni corrected)
- Ch7 Bonferroni correction: alpha = 0.05/28 = 0.00179 (chapter-level)
- Within-RQ correction: alpha = 0.05/4 = 0.0125 (for 4 predictors)

**Data Source:** DERIVED from Ch5 5.1.1 theta_all scores + master.xlsx self-report measures

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify Ch5 5.1.1 outputs exist and master.xlsx accessible before proceeding

**Input:**
- Primary: results/ch5/5.1.1/status.yaml (verify rq_results: success)
- Alternative: results/ch5/5.1.1/data/*theta*.{csv,txt,rds}
- Fallback: results/ch5/5.1.1/data/step*theta*.csv
- Expected: Ch5 5.1.1 theta_all scores per participant (N=100)
- Master data: data/cache/master.xlsx (self-report measures)

**Processing:**
- Check Ch5 5.1.1 completion status (rq_results = success)
- Locate theta score files using multiple patterns
- Verify master.xlsx contains required columns: Education, Typical_Sleep, VR_Experience, Age
- Test file accessibility and basic format validation
- Log all validation checks with pass/fail status

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Contains: Ch5 status check, file path verification, master.xlsx column check

*Value Ranges:*
- Status check: "success" or "failure" entries only
- File counts: theta files >= 1, master.xlsx = 1 file
- Column verification: 4 required columns present in master.xlsx

*Data Quality:*
- Ch5 5.1.1 status must be "success"
- At least 1 theta file found with expected naming pattern
- master.xlsx accessible and contains Education, Typical_Sleep, VR_Experience, Age

*Log Validation:*
- Required patterns: "Ch5 5.1.1 validation: PASS", "master.xlsx validation: PASS"
- Forbidden patterns: "ERROR", "FAIL", "file not found", "missing columns"
- Acceptable warnings: "Multiple theta files found" (choose most appropriate)

**Expected Behavior on Validation Failure:**
Quit immediately with specific error message. Log failure to logs/step00_dependency_validation.log.

### Step 1: Extract and Merge Data Sources
**Dependencies:** Step 0 (dependencies verified)
**Complexity:** Medium (~8 minutes)

**Purpose:** Load theta_all scores from Ch5 5.1.1 and self-report measures from master.xlsx, merge on UID

**Input:**
- Primary: results/ch5/5.1.1/data/*theta_scores*.csv (Ch5 IRT ability estimates)
- Alternative: results/ch5/5.1.1/data/*theta*.csv
- Expected format: UID, domain, theta_all, se_all columns
- Master: data/cache/master.xlsx, sheet: participant_data
- Expected columns: UID, Education, Typical_Sleep, VR_Experience, Age

**Processing:**
- Load Ch5 theta scores, compute mean theta_all per participant across domains
- Load self-report data from master.xlsx
- Merge datasets on UID (inner join for complete cases only)
- Check for missing values in predictors and outcome
- Log participant counts at each merge step
- Create complete case analysis dataset
- Standardize continuous predictors (z-scores) for interpretability

**Output:**
- data/step01_theta_means_by_participant.csv (aggregated Ch5 data)
- data/step01_self_report_measures.csv (extracted master.xlsx data)
- data/step01_analysis_dataset.csv (merged complete cases)

**Validation Requirement:**
Validation tools MUST be used after data extraction and merging execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_theta_means_by_participant.csv: ~100 rows x 3 columns (UID, mean_theta_all, se_theta_all)
- data/step01_self_report_measures.csv: ~100 rows x 5 columns (UID, Education, Typical_Sleep, VR_Experience, Age)
- data/step01_analysis_dataset.csv: 90-100 rows x 6 columns (merged complete cases)

*Value Ranges:*
- mean_theta_all in [-2, 2] (IRT ability scale, standardized)
- Education in [8, 25] years (reasonable range for adults)
- Typical_Sleep in [4, 12] hours (physiologically plausible)
- VR_Experience in [0, 5] (ordinal scale)
- Age in [18, 65] years (adult sample)

*Data Quality:*
- No missing values in final analysis dataset
- UID column unique (no duplicates)
- Merged N >= 90 (allowing up to 10% exclusion for missing data)
- All continuous variables finite (no inf/-inf)

*Log Validation:*
- Required patterns: "Theta aggregation complete: N=", "Merge successful: N=", "Complete cases: N="
- Forbidden patterns: "ERROR", "FAIL", "merge failed", "no matches"
- Acceptable warnings: "Missing data excluded: n=" (if < 10%)

**Expected Behavior on Validation Failure:**
If merged N < 90, raise error with diagnostic info. Log to logs/step01_extract_merge_data.log.

### Step 2: Descriptive Statistics and Data Quality Assessment
**Dependencies:** Step 1 (merged dataset)
**Complexity:** Low (~5 minutes)

**Purpose:** Generate comprehensive descriptive statistics and assess data quality before regression analysis

**Input:**
- data/step01_analysis_dataset.csv (complete cases)

**Processing:**
- Compute descriptive statistics: mean, SD, min, max, skew, kurtosis for all variables
- Generate correlation matrix among all predictors and outcome
- Assess data distributions with Shapiro-Wilk normality tests
- Identify potential outliers using IQR method (values > Q3 + 1.5*IQR or < Q1 - 1.5*IQR)
- Check for restricted ranges that might attenuate correlations
- Document any data transformation needs

**Output:**
- data/step02_descriptive_statistics.csv (means, SDs, distributions)
- data/step02_correlation_matrix.csv (bivariate correlations among all variables)
- data/step02_normality_tests.csv (Shapiro-Wilk results)
- data/step02_outlier_detection.csv (outlier identification)

**Validation Requirement:**
Validation tools MUST be used after descriptive statistics computation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_descriptive_statistics.csv: 6 rows x 8 columns (variables x statistics)
- data/step02_correlation_matrix.csv: 6 x 6 correlation matrix
- data/step02_normality_tests.csv: 6 rows x 3 columns (variable, statistic, p_value)
- data/step02_outlier_detection.csv: variable number of rows x 3 columns (UID, variable, outlier_type)

*Value Ranges:*
- Correlations in [-1, 1] (valid correlation range)
- p_values in [0, 1] (valid probability range)
- Skewness in [-3, 3] (reasonable for psychological data)
- Kurtosis in [-2, 10] (reasonable excess kurtosis range)

*Data Quality:*
- All statistics finite (no NaN/inf)
- Correlation matrix symmetric with 1.0 on diagonal
- Normality test results present for all 6 variables
- Outlier detection identifies < 15% of cases as outliers

*Log Validation:*
- Required patterns: "Descriptive statistics complete", "Correlation matrix computed", "Normality tests complete"
- Forbidden patterns: "ERROR", "FAIL", "computation failed"
- Acceptable warnings: "Outliers detected: n=" (if reasonable number)

**Expected Behavior on Validation Failure:**
Document any severe data quality issues. Continue with warnings if outliers < 15% and no missing data.

### Step 3: Hierarchical Multiple Regression Analysis
**Dependencies:** Step 2 (descriptive statistics)
**Complexity:** High (~15 minutes including bootstrap)

**Purpose:** Fit hierarchical regression models to test unique contributions of self-report predictors

**Input:**
- data/step01_analysis_dataset.csv (predictor and outcome data)

**Processing:**
- Model 1 (Demographics): mean_theta_all ~ Age
- Model 2 (Full): mean_theta_all ~ Age + Education + Typical_Sleep + VR_Experience
- Implementation: statsmodels.api.OLS with standardized predictors
- Extract R², adjusted R², F-statistics for both models
- Compute incremental R² (Model 2 - Model 1) with F-test for significance
- Bootstrap 95% CIs for regression coefficients:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - CI: Percentile method (2.5th, 97.5th percentiles)
- Multiple comparison corrections:
  - Within-RQ family: 4 predictors (Age, Education, Sleep, VR_Experience)
  - Bonferroni: alpha = 0.05/4 = 0.0125 per test
  - FDR: Benjamini-Hochberg correction
  - Report BOTH uncorrected AND corrected p-values (Decision D068)

**Output:**
- data/step03_model_summaries.csv (R², F-tests, model comparisons)
- data/step03_regression_coefficients.csv (betas, SEs, CIs, dual p-values)
- data/step03_bootstrap_results.csv (1000 bootstrap coefficient estimates)

**Validation Requirement:**
Validation tools MUST be used after hierarchical regression execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_model_summaries.csv: 2 rows x 6 columns (model1, model2 statistics)
- data/step03_regression_coefficients.csv: 4 rows x 8 columns (predictors x stats)
- Columns: predictor, beta, se, ci_lower, ci_upper, p_uncorrected, p_bonferroni, p_fdr
- data/step03_bootstrap_results.csv: 1000 rows x 4 columns (bootstrap replicates)

*Value Ranges:*
- R² in [0, 1] (valid R² range)
- beta coefficients in [-1, 1] (standardized predictors)
- Standard errors > 0 (positive SEs)
- p-values in [0, 1]
- Bootstrap CIs valid: ci_lower < beta < ci_upper (for most cases)

*Data Quality:*
- All 4 predictors present in coefficients file
- Bootstrap completed 1000 iterations
- No NaN values in coefficient estimates
- Dual p-values present (uncorrected + corrected)
- F-test for model comparison computed

*Log Validation:*
- Required patterns: "Model 1 fitted: R² =", "Model 2 fitted: R² =", "Bootstrap complete: 1000 iterations"
- Required patterns: "Bonferroni correction applied", "FDR correction applied"
- Forbidden patterns: "ERROR", "FAIL", "convergence failed", "singular matrix"

**Expected Behavior on Validation Failure:**
If convergence fails or R² > 0.8 (overfitting), raise error. Log to logs/step03_hierarchical_regression.log.

### Step 4: Model Diagnostics and Assumption Checking
**Dependencies:** Step 3 (regression models fitted)
**Complexity:** Medium (~8 minutes)

**Purpose:** Comprehensive validation of regression assumptions and model diagnostics

**Input:**
- data/step03_regression_coefficients.csv (fitted model results)
- data/step01_analysis_dataset.csv (original data for residual analysis)

**Processing:**
- Residual analysis for Model 2 (full model):
  - Extract residuals and fitted values
  - Normality: Shapiro-Wilk test on residuals, Q-Q plot data
  - Homoscedasticity: Breusch-Pagan test, residual vs fitted plot data
  - Linearity: Partial residual plots for each predictor
- Multicollinearity assessment:
  - Variance Inflation Factor (VIF) for each predictor
  - Condition indices and variance proportions
- Influential observations:
  - Cook's distance for each observation (threshold: 4/n = 0.04)
  - Leverage values (hat values)
  - Studentized residuals
- Remedial actions if assumptions violated:
  - Normality p < 0.05: Flag for bootstrap inference primacy
  - Heteroscedasticity p < 0.05: Compute HC3 robust standard errors
  - VIF > 5: Document multicollinearity concern
  - VIF > 10: Consider predictor removal or ridge regression
  - Cook's D > 0.04: Identify influential cases for sensitivity analysis

**Output:**
- data/step04_residual_analysis.csv (normality and homoscedasticity tests)
- data/step04_multicollinearity.csv (VIF values and condition indices)
- data/step04_influential_observations.csv (Cook's D, leverage, studentized residuals)
- data/step04_diagnostic_plot_data.csv (data for residual plots)

**Validation Requirement:**
Validation tools MUST be used after diagnostic analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_residual_analysis.csv: 2 rows x 4 columns (normality, homoscedasticity test results)
- data/step04_multicollinearity.csv: 4 rows x 3 columns (predictor, VIF, condition_index)
- data/step04_influential_observations.csv: N rows x 4 columns (UID, cooks_d, leverage, studentized_resid)
- data/step04_diagnostic_plot_data.csv: N rows x 3 columns (fitted, residuals, standardized_residuals)

*Value Ranges:*
- VIF values >= 1.0 (lower bound for VIF)
- Cook's distance >= 0 (non-negative)
- Leverage in [0, 1] (valid leverage range)
- Studentized residuals in [-4, 4] (reasonable range for N~100)
- p-values in [0, 1]

*Data Quality:*
- VIF computed for all 4 predictors
- Diagnostic statistics for all N participants
- No missing values in diagnostic measures
- Test statistics and p-values finite

*Log Validation:*
- Required patterns: "Residual analysis complete", "VIF computed", "Influential cases identified"
- Required patterns: "Normality test p =", "Homoscedasticity test p ="
- Forbidden patterns: "ERROR", "FAIL", "computation failed"
- Acceptable warnings: "VIF > 5 detected" (if multicollinearity present)

**Expected Behavior on Validation Failure:**
Document assumption violations but continue analysis. Flag serious violations (VIF > 10, many influential cases) for interpretation caveats.

### Step 5: Effect Sizes and Confidence Intervals
**Dependencies:** Step 3 (regression results), Step 4 (diagnostics)
**Complexity:** Medium (~8 minutes)

**Purpose:** Compute comprehensive effect size measures with robust confidence intervals

**Input:**
- data/step03_model_summaries.csv (R² values)
- data/step03_regression_coefficients.csv (beta coefficients)
- data/step03_bootstrap_results.csv (bootstrap estimates)

**Processing:**
- Overall model effect sizes:
  - Cohen's f² = R²/(1-R²) for both models
  - Effect size interpretation: small (f² = 0.02), medium (f² = 0.15), large (f² = 0.35)
- Individual predictor effect sizes:
  - Semi-partial correlations (sr²) for unique variance explained
  - Standardized beta coefficients with bootstrap 95% CIs
- Confidence intervals:
  - Bootstrap percentile method: 2.5th and 97.5th percentiles from 1000 replicates
  - Bias-corrected bootstrap CIs if bias detected
- Relative importance analysis:
  - Rank predictors by absolute beta coefficient magnitude
  - Proportion of total R² explained by each predictor (approximate)

**Output:**
- data/step05_effect_sizes.csv (Cohen's f², sr², relative importance)
- data/step05_confidence_intervals.csv (bootstrap CIs for all effects)
- data/step05_predictor_rankings.csv (relative importance ordering)

**Validation Requirement:**
Validation tools MUST be used after effect size computation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_effect_sizes.csv: 4 rows x 5 columns (predictors x effect size metrics)
- Columns: predictor, beta, sr_squared, cohens_f_squared, effect_size_interpretation
- data/step05_confidence_intervals.csv: 4 rows x 4 columns (predictor, ci_lower, ci_upper, ci_width)
- data/step05_predictor_rankings.csv: 4 rows x 3 columns (rank, predictor, relative_importance)

*Value Ranges:*
- Cohen's f² >= 0 (non-negative effect sizes)
- Semi-partial correlations sr² in [0, 1] (valid proportion range)
- Beta coefficients in [-1, 1] (standardized predictors)
- CI width > 0 (positive interval widths)

*Data Quality:*
- All 4 predictors present in all files
- Effect size interpretations provided (small/medium/large)
- CIs properly ordered: ci_lower < ci_upper
- Rankings from 1 to 4 (all predictors ranked)

*Log Validation:*
- Required patterns: "Effect sizes computed", "Bootstrap CIs extracted", "Relative importance ranked"
- Forbidden patterns: "ERROR", "FAIL", "negative effect size"
- Acceptable warnings: "Small effect sizes detected" (if f² < 0.02)

**Expected Behavior on Validation Failure:**
If effect sizes unreasonable (f² > 1.0) or CIs malformed, raise error with diagnostic information.

### Step 6: Cross-Validation Assessment
**Dependencies:** Step 3 (regression models)
**Complexity:** High (~10 minutes)

**Purpose:** Assess model generalizability through cross-validation to detect overfitting

**Input:**
- data/step01_analysis_dataset.csv (complete analysis dataset)

**Processing:**
- Implement 5-fold cross-validation using sklearn.model_selection.KFold:
  - Random seed: 42 for reproducibility
  - Shuffle: True (randomize before splitting)
  - For each fold: fit Model 2 on training set (80%), evaluate on test set (20%)
- Compute cross-validation metrics:
  - R² on training and test sets for each fold
  - Root Mean Square Error (RMSE) on test sets
  - Mean Absolute Error (MAE) on test sets
- Assess generalizability:
  - Mean and standard deviation of test R² across folds
  - Generalization gap: difference between mean training and test R²
  - Flag overfitting if gap > 0.10 (10% R² loss)
- Bootstrap cross-validation:
  - Iterations: 1000
  - Random seed: 42
  - For each iteration: random 5-fold split, compute mean test R²
  - 95% CI for cross-validated R²

**Output:**
- data/step06_cv_fold_results.csv (R², RMSE, MAE for each fold)
- data/step06_cv_summary.csv (mean performance across folds)
- data/step06_cv_bootstrap.csv (1000 bootstrap CV estimates)

**Validation Requirement:**
Validation tools MUST be used after cross-validation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_cv_fold_results.csv: 5 rows x 5 columns (fold, train_r2, test_r2, rmse, mae)
- data/step06_cv_summary.csv: 1 row x 6 columns (mean_train_r2, mean_test_r2, generalization_gap, etc.)
- data/step06_cv_bootstrap.csv: 1000 rows x 2 columns (iteration, bootstrap_test_r2)

*Value Ranges:*
- R² values in [0, 1] (valid R² range)
- RMSE > 0 (positive error measures)
- MAE > 0 (positive error measures)
- Generalization gap >= 0 (training usually >= test performance)

*Data Quality:*
- Exactly 5 folds completed
- All performance metrics finite
- Bootstrap completed 1000 iterations
- Generalization gap < 0.20 (reasonable for N=100)

*Log Validation:*
- Required patterns: "5-fold CV complete", "Mean test R² =", "Generalization gap =", "Bootstrap CV: 1000 iterations"
- Forbidden patterns: "ERROR", "FAIL", "fold failed", "negative R²"
- Acceptable warnings: "Generalization gap > 0.10" (moderate overfitting)

**Expected Behavior on Validation Failure:**
If CV fails or generalization gap > 0.20, document overfitting concern. Proceed with interpretation caveats.

### Step 7: Power Analysis
**Dependencies:** Step 3 (regression results)
**Complexity:** Medium (~5 minutes)

**Purpose:** Conduct post-hoc power analysis for observed effects and sensitivity analysis

**Input:**
- data/step03_model_summaries.csv (observed R² values)
- data/step03_regression_coefficients.csv (observed effect sizes)

**Processing:**
- Post-hoc power analysis for hierarchical regression:
  - Given: N=100, 4 predictors, observed R²
  - Alpha level: 0.05 (uncorrected) and 0.0125 (Bonferroni within-RQ)
  - Use: statsmodels.stats.power.FTestAnovaPower()
  - Compute: power for observed incremental R² (Model 2 - Model 1)
- Individual predictor power:
  - Convert beta coefficients to Cohen's f² for each predictor
  - Compute post-hoc power for each predictor at alpha = 0.0125
- Sensitivity analysis:
  - Minimum detectable effect size (Cohen's f²) at 80% power
  - Minimum detectable R² increment at 80% power
  - Sample size needed for 80% power to detect observed effects

**Output:**
- data/step07_power_analysis.csv (post-hoc power for observed effects)
- data/step07_sensitivity_analysis.csv (minimum detectable effects)

**Validation Requirement:**
Validation tools MUST be used after power analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_power_analysis.csv: 5 rows x 4 columns (overall + 4 predictors)
- Columns: effect_type, observed_effect_size, power_uncorrected, power_bonferroni
- data/step07_sensitivity_analysis.csv: 1 row x 4 columns (min_f2, min_r2_increment, n_needed_80power, etc.)

*Value Ranges:*
- Power values in [0, 1] (valid probability range)
- Effect sizes f² >= 0 (non-negative)
- Sample size estimates > 0 (positive integers)
- Minimum detectable effects > 0

*Data Quality:*
- Power computed for overall model and each predictor
- Both uncorrected and Bonferroni-corrected power reported
- Sensitivity analysis completed
- All estimates finite and reasonable

*Log Validation:*
- Required patterns: "Power analysis complete", "Sensitivity analysis complete"
- Forbidden patterns: "ERROR", "FAIL", "power computation failed"
- Acceptable warnings: "Power < 0.80 detected" (underpowered effects)

**Expected Behavior on Validation Failure:**
If power computation fails, document limitation but continue. Note underpowered effects in interpretation.

### Step 8: Sensitivity Analyses and Robustness Checks
**Dependencies:** Step 4 (diagnostics), Step 5 (effect sizes)
**Complexity:** Medium (~8 minutes)

**Purpose:** Conduct sensitivity analyses to assess robustness of findings

**Input:**
- data/step01_analysis_dataset.csv (original data)
- data/step04_influential_observations.csv (outlier identification)
- data/step04_residual_analysis.csv (assumption violations)

**Processing:**
- Outlier exclusion analysis:
  - Identify participants with Cook's D > 0.04 (4/n threshold)
  - Re-fit Model 2 excluding influential cases
  - Compare coefficient estimates and significance levels
- Assumption violation remediation:
  - If normality violated (Shapiro-Wilk p < 0.05): emphasize bootstrap CIs over t-tests
  - If heteroscedasticity detected: compute HC3 robust standard errors using statsmodels
  - Report both original and robust results
- Alternative significance thresholds:
  - Compare results using uncorrected p < 0.05, Bonferroni p < 0.0125, and FDR correction
  - Document how conclusions change with different correction approaches
- Missing data sensitivity:
  - If any participants excluded for missing data, document characteristics
  - Assess whether exclusions might bias results

**Output:**
- data/step08_outlier_exclusion_results.csv (results without influential cases)
- data/step08_robust_standard_errors.csv (HC3 robust SEs if needed)
- data/step08_correction_comparisons.csv (results under different alpha levels)
- data/step08_sensitivity_summary.csv (overall robustness assessment)

**Validation Requirement:**
Validation tools MUST be used after sensitivity analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_outlier_exclusion_results.csv: 4 rows x 4 columns (predictors, coefficients with/without outliers)
- data/step08_robust_standard_errors.csv: 4 rows x 6 columns (original vs robust SEs)
- data/step08_correction_comparisons.csv: 4 rows x 5 columns (uncorrected, bonferroni, fdr results)
- data/step08_sensitivity_summary.csv: 1 row x 8 columns (robustness indicators)

*Value Ranges:*
- All coefficient estimates finite
- Standard errors > 0 (both original and robust)
- p-values in [0, 1]
- Coefficient differences within reasonable bounds (not wildly different)

*Data Quality:*
- Sensitivity analyses completed for all major concerns identified in diagnostics
- Robust estimates provided if assumption violations detected
- Multiple correction comparisons available
- Summary indicates overall robustness level

*Log Validation:*
- Required patterns: "Outlier exclusion complete", "Sensitivity analyses complete"
- Required patterns: "Robustness assessment complete"
- Forbidden patterns: "ERROR", "FAIL", "analysis failed"
- Acceptable warnings: "Assumption violations detected" (documented and addressed)

**Expected Behavior on Validation Failure:**
Document which sensitivity analyses could not be completed. Proceed with available robustness information.

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs in data/ folder)
- step00_dependency_validation.txt (dependency verification)
- step01_theta_means_by_participant.csv (aggregated Ch5 theta scores)
- step01_self_report_measures.csv (extracted master.xlsx data)
- step01_analysis_dataset.csv (merged complete cases, N~95)
- step02_descriptive_statistics.csv (means, SDs, distributions)
- step02_correlation_matrix.csv (6x6 correlation matrix)
- step02_normality_tests.csv (Shapiro-Wilk results)
- step02_outlier_detection.csv (outlier identification)
- step03_model_summaries.csv (R², F-tests, model comparisons)
- step03_regression_coefficients.csv (betas, SEs, CIs, dual p-values)
- step03_bootstrap_results.csv (1000 bootstrap replicates)
- step04_residual_analysis.csv (assumption test results)
- step04_multicollinearity.csv (VIF values)
- step04_influential_observations.csv (Cook's D, leverage)
- step04_diagnostic_plot_data.csv (residual plot data)
- step05_effect_sizes.csv (Cohen's f², sr², importance)
- step05_confidence_intervals.csv (bootstrap CIs)
- step05_predictor_rankings.csv (relative importance)
- step06_cv_fold_results.csv (5-fold CV performance)
- step06_cv_summary.csv (mean CV results)
- step06_cv_bootstrap.csv (1000 bootstrap CV estimates)
- step07_power_analysis.csv (post-hoc power for effects)
- step07_sensitivity_analysis.csv (minimum detectable effects)
- step08_outlier_exclusion_results.csv (sensitivity to outliers)
- step08_robust_standard_errors.csv (HC3 robust SEs if needed)
- step08_correction_comparisons.csv (multiple correction approaches)
- step08_sensitivity_summary.csv (overall robustness)

### Logs (ONLY execution logs in logs/ folder)
- step00_dependency_validation.log
- step01_extract_merge_data.log
- step02_descriptive_statistics.log
- step03_hierarchical_regression.log
- step04_model_diagnostics.log
- step05_effect_sizes.log
- step06_cross_validation.log
- step07_power_analysis.log
- step08_sensitivity_analyses.log

### Plots (EMPTY until rq_plots runs)
Note: Plot source data created in data/ folder:
- step04_diagnostic_plot_data.csv (residual plots)
- step02_correlation_matrix.csv (correlation heatmap)

### Results (EMPTY until rq_results runs)
Summary.md will be created by rq_results based on analysis outputs

---

## Expected Data Formats

### Step-to-Step Transformations
1. Ch5 theta scores -> aggregated means per participant
2. master.xlsx extraction -> standardized self-report measures
3. Merge -> complete case analysis dataset (~95 participants)
4. Regression analysis -> coefficients with dual p-values
5. Bootstrap -> robust confidence intervals
6. Cross-validation -> generalizability assessment

### Column Naming Conventions
- UID: Unique participant identifier (consistent across all files)
- mean_theta_all: Aggregated IRT ability estimate from Ch5
- Education, Typical_Sleep, VR_Experience, Age: Self-report predictors (standardized)
- beta, se, ci_lower, ci_upper: Regression coefficient estimates
- p_uncorrected, p_bonferroni, p_fdr: Dual p-value reporting (Decision D068)
- cooks_d, leverage, studentized_resid: Diagnostic measures

### Data Type Constraints
- UID: object/string (non-nullable)
- All numeric measures: float64 (nullable=False after complete case selection)
- p_values: float64 in [0, 1] range
- Effect sizes: float64 >= 0 (non-negative)

---

## Cross-RQ Dependencies

**Dependency:** Ch5 5.1.1 (Functional Form Comparison)

**Required Files:**
- Primary: results/ch5/5.1.1/data/*theta_scores*.csv
- Alternative: results/ch5/5.1.1/data/step*theta*.csv
- Fallback: Any CSV in Ch5 5.1.1 data/ containing "theta" and having UID, theta_all columns

**Expected Content:**
- N=100 participants with IRT ability estimates (theta_all)
- Domain-specific estimates to be aggregated into mean score
- Standard errors for uncertainty quantification

**Circuit Breaker:**
If Ch5 5.1.1 status != success OR no theta files found, QUIT with error: "Ch5 5.1.1 theta outputs not available for RQ 7.5.1 analysis"

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements Summary

All 9 steps (0-8) have comprehensive 4-layer validation:
1. **Output Files:** Exact file specifications with row/column counts
2. **Value Ranges:** Scientific bounds for all measures
3. **Data Quality:** Missing data tolerance, expected N, finite values
4. **Log Validation:** Required success patterns, forbidden error patterns

### Key Validation Thresholds
- Merged dataset: N >= 90 participants (allowing 10% exclusion)
- VIF threshold: < 5.0 (multicollinearity concern), < 10.0 (serious concern)
- Generalization gap: < 0.10 acceptable, < 0.20 concerning
- Cook's distance: > 4/n = 0.04 for influential case identification
- Bootstrap iterations: exactly 1000 for all procedures
- Cross-validation: exactly 5 folds with seed=42

---

## Summary

**Total Steps:** 9 (Step 0: dependency validation + Steps 1-8: analysis)
**Estimated Runtime:** ~45 minutes (including bootstrap and cross-validation)
**Cross-RQ Dependencies:** Ch5 5.1.1 theta_all scores required
**Primary Outputs:** Hierarchical regression with dual p-values, bootstrap CIs, cross-validation
**Validation Coverage:** 100% (all 9 steps have 4-layer validation requirements)

**Key Hypothesis:** Education level will significantly predict REMEMVR performance through cognitive reserve mechanisms (Beta = 0.20-0.25, p < 0.0125 Bonferroni-corrected)

**Critical Methodological Notes:**
- Bootstrap CIs (1000 iterations, seed=42) for robust inference
- 5-fold cross-validation (seed=42) for generalizability assessment
- Comprehensive assumption checking with remedial actions
- Dual p-value reporting (uncorrected + Bonferroni) per Decision D068
- Power analysis acknowledges potential underpowering for small effects
- Sensitivity analyses assess robustness to outliers and assumption violations

**Statistical Specifications Applied:**
- Random seed=42 for ALL randomized procedures (bootstrap, CV, fold assignment)
- Bootstrap: 1000 iterations, participant-level resampling, percentile CIs
- Cross-validation: 5-fold, shuffled, generalization gap threshold=0.10
- Multiple comparisons: Within-RQ Bonferroni (alpha=0.0125), also FDR
- Assumption violations: Shapiro-Wilk, Breusch-Pagan, VIF with specific remedial actions
- Power analysis: Post-hoc using statsmodels for regression context

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml  
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent v5.1.0