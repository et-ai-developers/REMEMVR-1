# Analysis Plan: RQ 7.8.3 - Parsimonious Predictive Model with Cross-Validation

**Research Question:** 7.8.3
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ compares 4 nested multiple regression models with increasing complexity to identify the most parsimonious model for predicting REMEMVR episodic memory performance. Uses 5-fold cross-validation to assess generalization and quantify overfitting through training-to-CV shrinkage analysis.

**Pipeline:** Nested Multiple Regression with 5-fold Cross-Validation and Model Comparison
**Steps:** 9 total analysis steps (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** 45-60 minutes

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Enhanced v5.1: Complete statistical specifications with seeds, iterations, corrections, remedial actions

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify Ch5 5.1.1 outputs and master.xlsx are accessible before proceeding

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/*theta*.csv
- Fallback: results/ch5/5.1.1/data/step*theta*all*.{csv,txt}
- Expected content: theta_all scores for 100 participants
- If not found: QUIT with "Ch5 5.1.1 theta outputs not found"
- Also verify: data/cache/master.xlsx accessible

**Processing:**
- Check Ch5 5.1.1 status.yaml shows rq_results: success
- Locate theta_all file using multiple patterns
- Verify file contains 100 rows with UID and theta_all columns
- Check master.xlsx has required cognitive test columns
- Log all validation checks with timestamps

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Expected patterns: "Ch5 5.1.1 FOUND", "master.xlsx ACCESSIBLE"

*Value Ranges:*
- N/A (validation step)

*Data Quality:*
- All required files must exist and be readable
- theta_all file must have 100 rows
- master.xlsx must have cognitive test columns

*Log Validation:*
- Required patterns: "Dependency validation COMPLETE"
- Required patterns: "Ch5 5.1.1 outputs FOUND"
- Forbidden patterns: "ERROR", "not found", "MISSING"

**Expected Behavior on Validation Failure:**
Raise error with specific missing dependency, quit immediately, log to logs/step00_dependency_validation.log

### Step 1: Extract and Prepare Cognitive Test Data
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Medium (~10 minutes)

**Purpose:** Extract cognitive test scores from master.xlsx and compute T-score transformations

**Input:**
- data/cache/master.xlsx (cognitive test raw scores)
- Required columns: UID, Age, Sex, Education, RAVLT_Total, BVMT_Total, RPM_Score, NART_Score, DASS_Total, Sleep

**Processing:**
- Load master.xlsx cognitive test data
- Check for missing data patterns (flag if >5% missing per variable)
- Compute T-score transformations: T = 50 + 10*(raw - mean)/sd
- Apply T-score transformation to: RAVLT_Total, BVMT_Total, RPM_Score, NART_Score
- Keep raw scores for: Age, Education, DASS_Total, Sleep, Sex
- Sex coding: standardize as 0=Male, 1=Female
- Round T-scores to 1 decimal place
- Report descriptive statistics for all variables

**Output:**
- data/step01_cognitive_tests.csv (N=100, 10 columns: UID + 9 predictor variables)
- data/step01_descriptive_stats.csv (means, SDs, ranges, missing counts)

**Validation Requirement:**
Validation tools MUST be used after data extraction tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_cognitive_tests.csv: 100 rows x 10 columns
- Columns: UID (object), Age (float64), Sex (int64), Education (float64), RAVLT_T, BVMT_T, RPM_T, NART_T (all T-scores float64), DASS_Total (float64), Sleep (float64)

*Value Ranges:*
- Age in [18, 85] (adult participants)
- T-scores in [20, 80] (reasonable T-score range)
- Education in [8, 20] (years of education)
- DASS_Total in [0, 126] (depression/anxiety scale)
- Sleep in [3, 12] (hours per night)
- Sex in [0, 1] (binary coding)

*Data Quality:*
- All 100 participants present (no missing UIDs)
- No duplicate UIDs
- Missing data < 5% per variable
- T-scores approximately M=50, SD=10

*Log Validation:*
- Required patterns: "Cognitive tests extracted: 100 participants"
- Required patterns: "T-score transformations complete"
- Forbidden patterns: "ERROR", "missing >5%", "transformation failed"

**Expected Behavior on Validation Failure:**
Raise error with specific validation failure, log to logs/step01_extract_cognitive.log, quit immediately, invoke g_debug

### Step 2: Extract Theta-All Scores from Ch5
**Dependencies:** Step 1 (cognitive test extraction)
**Complexity:** Medium (~8 minutes)

**Purpose:** Load theta_all scores from Ch5 5.1.1 results and merge with cognitive tests

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/*theta*.csv
- Expected format: UID, theta_all columns with 100 participants

**Processing:**
- Load theta_all scores using primary path, fall back to search pattern
- Verify theta_all column exists and contains numeric values
- Check for extreme values: flag theta_all outside [-4, 4] range
- Compute theta_all descriptive statistics
- Merge with cognitive test data on UID
- Verify merge completeness: all 100 participants matched
- Create final analysis dataset

**Output:**
- data/step02_theta_all_scores.csv (theta scores only, 100 rows x 2 columns)
- data/step02_analysis_input.csv (merged dataset, 100 rows x 11 columns)

**Validation Requirement:**
Validation tools MUST be used after theta extraction tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_theta_all_scores.csv: 100 rows x 2 columns (UID, theta_all)
- data/step02_analysis_input.csv: 100 rows x 11 columns (UID + 9 predictors + theta_all)

*Value Ranges:*
- theta_all in [-4, 4] (IRT ability scale range)
- All predictors within ranges from Step 1

*Data Quality:*
- All 100 participants present in both files
- Perfect merge: no missing data post-merge
- theta_all approximately normal distribution
- No duplicate UIDs

*Log Validation:*
- Required patterns: "Theta scores loaded: 100 participants"
- Required patterns: "Merge complete: 100 participants matched"
- Required patterns: "Analysis dataset ready"
- Forbidden patterns: "ERROR", "merge failed", "missing data"

**Expected Behavior on Validation Failure:**
Raise error with merge details, log to logs/step02_extract_theta.log, quit immediately, invoke g_debug

### Step 3: Define Nested Model Specifications
**Dependencies:** Step 2 (analysis dataset ready)
**Complexity:** Low (~5 minutes)

**Purpose:** Specify 4 nested regression models with increasing complexity

**Input:**
- data/step02_analysis_input.csv (complete analysis dataset)

**Processing:**
- Define 4 nested models with explicit predictor lists:
  - Model 1 (Minimal): Age + RAVLT_T (2 predictors)
  - Model 2 (Core): Age + RAVLT_T + BVMT_T (3 predictors)
  - Model 3 (Extended): Age + RAVLT_T + BVMT_T + RPM_T + Education (5 predictors)
  - Model 4 (Full): Age + RAVLT_T + BVMT_T + RPM_T + Education + NART_T + DASS_Total + Sleep + Sex (9 predictors)
- Save model specifications as structured data
- Document theoretical rationale for each model
- Check all specified predictors exist in dataset

**Output:**
- data/step03_nested_models.csv (4 rows x 3 columns: model_name, num_predictors, predictor_list)
- data/step03_model_specs.txt (detailed specifications with rationale)

**Validation Requirement:**
Validation tools MUST be used after model specification tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_nested_models.csv: 4 rows x 3 columns
- Columns: model_name (object), num_predictors (int64), predictor_list (object)
- data/step03_model_specs.txt: text file with model details

*Value Ranges:*
- num_predictors: [2, 3, 5, 9] (nested progression)
- Model names: ["Minimal", "Core", "Extended", "Full"]

*Data Quality:*
- 4 models specified (no missing)
- Nested structure: each model contains all predictors from simpler models
- All specified predictors exist in analysis dataset
- Predictor counts match expectations

*Log Validation:*
- Required patterns: "4 nested models defined"
- Required patterns: "Model nesting verified"
- Required patterns: "All predictors exist in dataset"
- Forbidden patterns: "ERROR", "predictor not found", "nesting violated"

**Expected Behavior on Validation Failure:**
Raise error with model specification issue, log to logs/step03_model_specs.log, quit immediately, invoke g_debug

### Step 4: Implement 5-Fold Cross-Validation
**Dependencies:** Step 3 (model specifications)
**Complexity:** High (~15 minutes including bootstrap)

**Purpose:** Perform 5-fold cross-validation for all 4 models and compute training vs CV performance

**Input:**
- data/step02_analysis_input.csv (analysis dataset)
- data/step03_nested_models.csv (model specifications)

**Processing:**
- Implement 5-fold cross-validation using sklearn.model_selection.KFold
- Random seed: 42 for reproducibility
- Shuffle: True (randomize before splitting)
- Stratification: Use QuantileStratifiedKFold based on age (maintain age distribution)
- For each model and each fold:
  - Split data into train (80%) and test (20%)
  - Fit model on training data
  - Compute training R² and test R²
  - Store coefficients for stability analysis
- Compute mean and std of R² across 5 folds for each model
- Calculate shrinkage = mean(Training R²) - mean(CV R²) for each model
- Flag overfitting if shrinkage > 0.10 for any model
- Bootstrap confidence intervals for CV-R² estimates:
  - Iterations: 1000
  - Random seed: 42
  - Participant-level resampling with replacement
  - CI: Percentile method (2.5th, 97.5th percentiles)

**Output:**
- data/step04_cv_results.csv (4 models x 7 columns: model, train_r2_mean, train_r2_sd, cv_r2_mean, cv_r2_sd, shrinkage, overfitting_flag)
- data/step04_cv_bootstrap_cis.csv (4 models x 4 columns: model, cv_r2_mean, ci_lower, ci_upper)
- data/step04_fold_details.csv (20 rows: 4 models x 5 folds with individual R² values)

**Validation Requirement:**
Validation tools MUST be used after cross-validation tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_cv_results.csv: 4 rows x 7 columns
- data/step04_cv_bootstrap_cis.csv: 4 rows x 4 columns
- data/step04_fold_details.csv: 20 rows x 5 columns (model, fold, train_r2, cv_r2, shrinkage)

*Value Ranges:*
- R² values in [0, 1] (valid R² range)
- Shrinkage in [-0.5, 0.5] (reasonable shrinkage range)
- Bootstrap CIs: ci_lower < cv_r2_mean < ci_upper
- CV-R² generally < Training R² (expected pattern)

*Data Quality:*
- All 4 models have complete results
- 5 folds per model (20 total rows in fold_details)
- No NaN values in R² calculations
- Bootstrap CIs non-degenerate (ci_upper > ci_lower)

*Log Validation:*
- Required patterns: "5-fold CV complete: 4 models"
- Required patterns: "Bootstrap CIs complete: 1000 iterations"
- Required patterns: "Cross-validation analysis finished"
- Forbidden patterns: "ERROR", "convergence failed", "NaN detected"

**Expected Behavior on Validation Failure:**
Raise error with CV implementation details, log to logs/step04_cross_validation.log, quit immediately, invoke g_debug

### Step 5: Compare Models and Select Optimal
**Dependencies:** Step 4 (cross-validation results)
**Complexity:** Medium (~10 minutes)

**Purpose:** Compare models using cross-validated R² and apply parsimony criterion for selection

**Input:**
- data/step04_cv_results.csv (CV performance for 4 models)
- data/step04_cv_bootstrap_cis.csv (CV confidence intervals)

**Processing:**
- Rank models by CV-R² performance (highest to lowest)
- Apply parsimony criterion: prefer simpler model if CV-R² within 0.02 of more complex
- Statistical comparison between nested models:
  - Compute F-test for nested model comparison
  - Bonferroni correction for multiple comparisons
  - Family: Within-RQ (3 nested comparisons: 1vs2, 2vs3, 3vs4)
  - Corrected alpha = 0.05/3 = 0.0167 per comparison
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Identify optimal model based on:
  - Best CV-R² with parsimony consideration
  - Acceptable shrinkage (< 0.10)
  - Stable bootstrap confidence intervals
- Document model selection rationale

**Output:**
- data/step05_model_comparison.csv (4 models ranked with selection metrics)
- data/step05_nested_comparisons.csv (3 F-tests with dual p-values)
- data/step05_optimal_model.txt (selected model with rationale)

**Validation Requirement:**
Validation tools MUST be used after model comparison tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_model_comparison.csv: 4 rows x 6 columns (model, cv_r2, rank, parsimony_selected, shrinkage, selected_as_optimal)
- data/step05_nested_comparisons.csv: 3 rows x 5 columns (comparison, f_stat, p_uncorrected, p_bonferroni, significant_corrected)
- data/step05_optimal_model.txt: text file with selection rationale

*Value Ranges:*
- cv_r2 in [0, 1] (valid R² range)
- rank in [1, 4] (ranking positions)
- F-statistics > 0 (valid F-test results)
- p-values in [0, 1] (valid probability range)
- parsimony_selected in [0, 1] (binary selection)

*Data Quality:*
- All 4 models ranked (no ties unless truly identical)
- 3 nested comparisons present (1vs2, 2vs3, 3vs4)
- Dual p-values present (Decision D068 compliance)
- One model clearly identified as optimal

*Log Validation:*
- Required patterns: "Model comparison complete: 4 models ranked"
- Required patterns: "Optimal model selected"
- Required patterns: "Bonferroni correction applied"
- Forbidden patterns: "ERROR", "no optimal model", "comparison failed"

**Expected Behavior on Validation Failure:**
Raise error with model selection issue, log to logs/step05_model_comparison.log, quit immediately, invoke g_debug

### Step 6: Fit Final Model and Extract Coefficients
**Dependencies:** Step 5 (optimal model selected)
**Complexity:** Medium (~12 minutes including bootstrap)

**Purpose:** Fit optimal model on full dataset and extract detailed coefficient information

**Input:**
- data/step02_analysis_input.csv (full analysis dataset)
- data/step05_optimal_model.txt (selected model specification)

**Processing:**
- Fit optimal model using full dataset (N=100)
- Extract standardized beta coefficients
- Compute bootstrap confidence intervals for coefficients:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Participant-level resampling with replacement
  - Extract coefficients from each bootstrap sample
  - CI: Percentile method (2.5th, 97.5th percentiles)
- Compute semi-partial correlations (sr²) for unique variance contribution
- Statistical significance testing:
  - t-tests for each coefficient
  - Bonferroni correction within optimal model
  - Family size = number of predictors in optimal model
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Extract model fit statistics: R², adjusted R², F-statistic

**Output:**
- data/step06_final_model_summary.csv (R², adj-R², F-stat, p-values)
- data/step06_coefficients.csv (predictors x 7 columns: predictor, beta, se, ci_lower, ci_upper, p_uncorrected, p_bonferroni)
- data/step06_semipartial_correlations.csv (predictors x 3 columns: predictor, sr2, percent_unique_variance)

**Validation Requirement:**
Validation tools MUST be used after final model fitting tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_final_model_summary.csv: 1 row x 4 columns (r2, adj_r2, f_stat, model_p_value)
- data/step06_coefficients.csv: N predictors x 7 columns (based on optimal model)
- data/step06_semipartial_correlations.csv: N predictors x 3 columns

*Value Ranges:*
- R² in [0, 1] and adj_R² <= R² (valid relationship)
- F-statistic > 0 (valid F-test)
- Beta coefficients in [-3, 3] (reasonable standardized range)
- Standard errors > 0 (positive SEs)
- p-values in [0, 1] (valid probabilities)
- sr² in [0, 1] (valid proportion)

*Data Quality:*
- Number of predictors matches optimal model
- Bootstrap CIs valid: ci_lower < beta < ci_upper
- Dual p-values present for all predictors
- sr² values sum to total R² (within rounding)

*Log Validation:*
- Required patterns: "Final model fitted successfully"
- Required patterns: "Bootstrap CIs computed: 1000 iterations"
- Required patterns: "Semi-partial correlations complete"
- Forbidden patterns: "ERROR", "convergence failed", "degenerate CI"

**Expected Behavior on Validation Failure:**
Raise error with model fitting details, log to logs/step06_final_model.log, quit immediately, invoke g_debug

### Step 7: Diagnostic Validation and Assumption Checks
**Dependencies:** Step 6 (final model fitted)
**Complexity:** Medium (~10 minutes)

**Purpose:** Validate regression assumptions and check model diagnostics for optimal model

**Input:**
- data/step02_analysis_input.csv (analysis dataset)
- data/step06_coefficients.csv (fitted model coefficients)

**Processing:**
- Fit optimal model and extract residuals
- Check regression assumptions with formal tests:
  - Normality: Shapiro-Wilk test on residuals
  - Homoscedasticity: Breusch-Pagan test
  - Multicollinearity: VIF for each predictor
  - Independence: verified by study design (cross-sectional)
- Outlier detection:
  - Cook's distance > 4/N = 0.04
  - Leverage values > 2*(p+1)/N
  - Studentized residuals > |3|
- Residual distribution analysis:
  - Q-Q plot data for normality assessment
  - Residuals vs fitted plot data for homoscedasticity
  - Histogram data for residual distribution
- Remedial actions if assumptions violated:
  - Normality p < 0.05: Report bootstrap CIs as primary (already computed)
  - Heteroscedasticity p < 0.05: Compute HC3 robust standard errors
  - VIF > 5: Document multicollinearity concern
  - VIF > 10: Flag for potential predictor removal
  - Cook's D > 0.04: Report results with and without outliers

**Output:**
- data/step07_assumption_tests.csv (4 tests x 3 columns: test_name, statistic, p_value)
- data/step07_vif_results.csv (N predictors x 2 columns: predictor, vif)
- data/step07_outlier_analysis.csv (100 participants x 4 columns: UID, cooks_d, leverage, studentized_residual)
- data/step07_diagnostic_data.csv (residual and fitted values for plotting)

**Validation Requirement:**
Validation tools MUST be used after diagnostic validation tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_assumption_tests.csv: 3 rows x 3 columns (Shapiro-Wilk, Breusch-Pagan, + overall summary)
- data/step07_vif_results.csv: N predictors x 2 columns (matches optimal model)
- data/step07_outlier_analysis.csv: 100 rows x 4 columns
- data/step07_diagnostic_data.csv: 100 rows x 3 columns (UID, residual, fitted)

*Value Ranges:*
- p-values in [0, 1] (valid probabilities)
- VIF >= 1.0 (theoretical minimum)
- Cook's D >= 0 (non-negative)
- Leverage in [0, 1] (theoretical range)
- Studentized residuals approximately in [-4, 4] (reasonable range)

*Data Quality:*
- All 100 participants in outlier analysis
- No missing values in diagnostic statistics
- VIF computed for all predictors in optimal model
- Residual analysis data complete

*Log Validation:*
- Required patterns: "Assumption checks complete"
- Required patterns: "Outlier analysis finished"
- Required patterns: "VIF analysis complete"
- Forbidden patterns: "ERROR", "test failed", "computation error"

**Expected Behavior on Validation Failure:**
Raise error with diagnostic details, log to logs/step07_diagnostics.log, quit immediately, invoke g_debug

### Step 8: Sensitivity Analysis and Robustness Checks
**Dependencies:** Step 7 (diagnostics complete)
**Complexity:** High (~15 minutes)

**Purpose:** Perform sensitivity analyses including outlier exclusion and alternative CV approaches

**Input:**
- data/step02_analysis_input.csv (analysis dataset)
- data/step05_optimal_model.txt (optimal model specification)
- data/step07_outlier_analysis.csv (outlier identification)

**Processing:**
- Outlier sensitivity analysis:
  - Identify influential outliers: Cook's D > 4/N = 0.04
  - If outliers found: refit optimal model excluding outliers
  - Compare coefficient stability with/without outliers
  - Document impact on R² and coefficient significance
- Leave-one-out cross-validation (LOO-CV):
  - Implement LOO-CV for optimal model comparison with 5-fold CV
  - Random seed: 42 for any randomization
  - Compute LOO-CV R² and compare with 5-fold CV R²
  - Assess consistency between CV approaches
- Alternative stratification approach:
  - Repeat 5-fold CV with theta_all stratification instead of age
  - Compare CV-R² stability across stratification methods
  - Random seed: 42 for reproducibility
- Bootstrap stability analysis:
  - Additional 1000 bootstrap iterations with seed=43 for comparison
  - Assess CI stability across different random seeds
  - Compute coefficient of variation for bootstrap estimates

**Output:**
- data/step08_outlier_sensitivity.csv (model comparison with/without outliers)
- data/step08_loo_cv_results.csv (LOO-CV vs 5-fold CV comparison)
- data/step08_alternative_cv.csv (age vs theta stratification comparison)
- data/step08_bootstrap_stability.csv (seed=42 vs seed=43 comparison)

**Validation Requirement:**
Validation tools MUST be used after sensitivity analysis tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_outlier_sensitivity.csv: 2 rows x 5 columns (full_sample, outliers_excluded with R², coefficients, significance)
- data/step08_loo_cv_results.csv: 1 row x 4 columns (loo_cv_r2, fold5_cv_r2, difference, correlation)
- data/step08_alternative_cv.csv: 2 rows x 3 columns (age_stratified, theta_stratified with CV-R²)
- data/step08_bootstrap_stability.csv: N predictors x 4 columns (predictor, seed42_ci_width, seed43_ci_width, stability_ratio)

*Value Ranges:*
- R² values in [0, 1] (valid range)
- CV-R² difference in [-0.5, 0.5] (reasonable sensitivity range)
- Correlation between LOO and 5-fold in [0, 1] (positive expected)
- Stability ratio in [0.5, 2.0] (reasonable stability range)

*Data Quality:*
- Outlier analysis compares exactly 2 conditions
- CV comparisons show reasonable agreement (difference < 0.10)
- Bootstrap stability demonstrates convergence
- All sensitivity analyses complete without errors

*Log Validation:*
- Required patterns: "Sensitivity analysis complete"
- Required patterns: "LOO-CV comparison finished"
- Required patterns: "Bootstrap stability confirmed"
- Forbidden patterns: "ERROR", "sensitivity failed", "instability detected"

**Expected Behavior on Validation Failure:**
Raise error with sensitivity analysis details, log to logs/step08_sensitivity.log, quit immediately, invoke g_debug

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt: Cross-RQ dependency check results
- data/step01_cognitive_tests.csv: Extracted and T-scored cognitive predictors (100x10)
- data/step01_descriptive_stats.csv: Cognitive test descriptive statistics
- data/step02_theta_all_scores.csv: theta_all scores from Ch5 (100x2)
- data/step02_analysis_input.csv: Complete merged analysis dataset (100x11)
- data/step03_nested_models.csv: 4 model specifications (4x3)
- data/step03_model_specs.txt: Detailed model documentation
- data/step04_cv_results.csv: Cross-validation results for 4 models (4x7)
- data/step04_cv_bootstrap_cis.csv: Bootstrap CIs for CV-R² (4x4)
- data/step04_fold_details.csv: Individual fold results (20x5)
- data/step05_model_comparison.csv: Model ranking and selection (4x6)
- data/step05_nested_comparisons.csv: F-test comparisons with dual p-values (3x5)
- data/step05_optimal_model.txt: Selected model rationale
- data/step06_final_model_summary.csv: Final model R², F-statistics (1x4)
- data/step06_coefficients.csv: Beta coefficients with bootstrap CIs (Nx7)
- data/step06_semipartial_correlations.csv: Unique variance contributions (Nx3)
- data/step07_assumption_tests.csv: Shapiro-Wilk, Breusch-Pagan results (3x3)
- data/step07_vif_results.csv: Variance inflation factors (Nx2)
- data/step07_outlier_analysis.csv: Cook's D, leverage, residuals (100x4)
- data/step07_diagnostic_data.csv: Residuals and fitted values (100x3)
- data/step08_outlier_sensitivity.csv: Sensitivity to outlier exclusion (2x5)
- data/step08_loo_cv_results.csv: LOO vs 5-fold CV comparison (1x4)
- data/step08_alternative_cv.csv: Alternative stratification comparison (2x3)
- data/step08_bootstrap_stability.csv: Bootstrap seed stability (Nx4)

### Logs (ONLY execution logs)
- logs/step00_dependency_validation.log: Dependency check execution
- logs/step01_extract_cognitive.log: Cognitive test extraction
- logs/step02_extract_theta.log: Theta extraction and merging
- logs/step03_model_specs.log: Model specification creation
- logs/step04_cross_validation.log: Cross-validation execution
- logs/step05_model_comparison.log: Model selection process
- logs/step06_final_model.log: Final model fitting
- logs/step07_diagnostics.log: Assumption checking
- logs/step08_sensitivity.log: Sensitivity analysis execution

### Plots (EMPTY until rq_plots runs)
- Plot source CSVs created in data/ with step##_*_plot_data.csv naming:
  - data/step04_cv_performance_plot_data.csv: Training vs CV R² by model
  - data/step05_shrinkage_comparison_plot_data.csv: Overfitting visualization
  - data/step06_coefficient_plot_data.csv: Beta coefficients with CIs
  - data/step07_diagnostic_plots_data.csv: Residual diagnostic plots

### Results (EMPTY until rq_results runs)
- results/summary.md will be created by rq_results agent

---

## Expected Data Formats

### Step-to-Step Transformations
1. **Raw to T-scores:** Convert RAVLT, BVMT, RPM, NART to T-scores (M=50, SD=10)
2. **Data merging:** Combine cognitive tests + theta_all on UID
3. **Model specification:** Nested predictor lists with increasing complexity
4. **Cross-validation:** Split data into train/test, fit models, compute R²
5. **Model selection:** Rank by CV-R², apply parsimony, select optimal
6. **Final fitting:** Full dataset fit with bootstrap CIs and diagnostics

### Column Naming Conventions
- **IDs:** UID (consistent across all files)
- **Predictors:** Age, Sex, Education, RAVLT_T, BVMT_T, RPM_T, NART_T, DASS_Total, Sleep
- **Outcome:** theta_all (from Ch5 5.1.1)
- **Models:** Minimal, Core, Extended, Full
- **Statistics:** r2, adj_r2, cv_r2, shrinkage, beta, se, p_uncorrected, p_bonferroni

### Data Type Constraints
- **UIDs:** object (string identifiers, non-nullable)
- **Numeric variables:** float64 (Age, T-scores, theta_all, statistics)
- **Binary variables:** int64 (Sex as 0/1)
- **Model results:** float64 for all statistics, object for model names
- **Missing data:** Only allowed in initial extraction, not in final analyses

---

## Cross-RQ Dependencies

**Source RQ:** Ch5 5.1.1 (Functional Form Comparison)
**Dependency Type:** theta_all scores aggregated across all memory domains
**Required Status:** Ch5 5.1.1 must complete through rq_results phase

**File Dependencies:**
- **Primary:** results/ch5/5.1.1/data/step03_theta_scores.csv
- **Alternatives:** results/ch5/5.1.1/data/*theta*.csv, results/ch5/5.1.1/data/step*theta_all*.{csv,txt}
- **Expected Format:** UID (object) + theta_all (float64) for 100 participants
- **Fallback Strategy:** Search patterns for theta files, verify content before proceeding

**Master Data Dependencies:**
- **Source:** data/cache/master.xlsx
- **Required Sheets:** Main participant data with cognitive tests
- **Columns:** UID, Age, Sex, Education, RAVLT_Total, BVMT_Total, RPM_Score, NART_Score, DASS_Total, Sleep
- **Format:** Standard Excel format with header row

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

All steps include comprehensive 4-layer validation as specified in individual step descriptions above.

**Validation Architecture:**
- **Layer 1:** Output Files (exact paths, dimensions, data types)
- **Layer 2:** Value Ranges (scientific bounds, expected ranges)
- **Layer 3:** Data Quality (missing data, duplicates, distributions)
- **Layer 4:** Log Validation (required success patterns, forbidden error patterns)

**Post-Validation Actions:**
- **On Success:** Continue to next step
- **On Failure:** Quit immediately, log specific failure, invoke g_debug for troubleshooting

---

## Summary

**Total Steps:** 9 (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** 45-60 minutes
**Cross-RQ Dependencies:** Ch5 5.1.1 theta_all scores + master.xlsx cognitive tests
**Primary Outputs:** 4 nested model comparisons, optimal model selection, comprehensive diagnostics
**Validation Coverage:** 100% (all 9 steps have complete 4-layer validation requirements)

**Key Hypothesis:** Core 3-predictor model (Age + RAVLT + BVMT) should achieve optimal CV-R² (~0.20-0.30) with minimal overfitting (shrinkage < 0.10), outperforming both simpler and more complex alternatives.

**Critical Methodological Notes:**
- Random seed=42 used throughout for reproducibility
- Bootstrap iterations=1000 for all CI estimation
- 5-fold stratified CV with age distribution maintenance
- Decision D068 compliance: dual p-value reporting throughout
- Complete assumption checking with specified remedial actions
- Comprehensive sensitivity analyses for robustness assessment

**Statistical Implementation Enhancements (v5.1):**
- All cross-validation procedures specify exact parameters (seed, folds, stratification)
- Bootstrap methods detail resampling unit, iterations, CI computation
- Multiple comparison corrections explicitly calculated and applied
- Remedial actions specified for all assumption violations
- Power considerations acknowledged through effect size expectations

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent with v5.1 enhanced statistical specifications