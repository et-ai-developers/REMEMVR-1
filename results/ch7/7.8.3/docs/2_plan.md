# Analysis Plan: RQ 7.8.3 - Parsimonious Predictive Model with Cross-Validation

**Research Question:** 7.8.3
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

**Purpose:** Determine the most parsimonious model to predict REMEMVR episodic memory performance and assess generalization through rigorous cross-validation.

**Pipeline:** Nested multiple regression with 5-fold cross-validation and model comparison
**Steps:** 9 total analysis steps (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** ~45 minutes total

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Random seed=42 for all randomized procedures (reproducibility)
- Bootstrap CIs with 1000 iterations for stability assessment
- 5-fold cross-validation with age stratification

**Analysis Overview:**
Compare 4 nested regression models (Minimal: Age+RAVLT -> Core: +BVMT -> Extended: +RPM+Education -> Full: all predictors) using cross-validation to identify optimal complexity for predicting theta_all scores. Focus on training vs CV R-squared to quantify overfitting and identify parsimonious model with best generalization.

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 outputs and master.xlsx exist before proceeding with analysis

**Input:**
- Primary: results/ch5/5.1.1/status.yaml (verify rq_results: success)
- Alternative: results/ch5/5.1.1/data/step03_theta_scores.csv
- Fallback pattern: results/ch5/5.1.1/data/*theta*.csv
- Master data: data/cache/master.xlsx
- Expected content: theta_all scores from IRT calibration, cognitive test raw scores

**Processing:**
- Check Ch5 5.1.1 completed successfully (status=success)
- Locate theta scores file (try multiple naming patterns)
- Verify master.xlsx accessibility and cognitive test columns
- Verify expected N=100 participants in both datasets
- Log all validation checks with specific file sizes and formats

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- File size: >500 bytes (comprehensive check results)

*Value Ranges:*
- Participant counts: N=100 in both Ch5 and master.xlsx data
- File sizes: theta file >5KB, master.xlsx >100KB

*Data Quality:*
- Both dependency files exist and accessible
- No file corruption or access errors
- Expected data structures present

*Log Validation:*
- Required patterns: "Ch5 5.1.1: SUCCESS", "master.xlsx: ACCESSIBLE", "N=100 confirmed"
- Forbidden patterns: "ERROR", "FILE NOT FOUND", "ACCESS DENIED"
- Acceptable warnings: path variations, alternative file naming

**Expected Behavior on Validation Failure:**
- Raise error with specific missing dependency
- Log to logs/step00_validate_dependencies.log
- QUIT immediately with clear dependency requirements

### Step 1: Extract and Prepare Cognitive Test Data
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (~5 minutes)

**Purpose:** Extract and standardize cognitive test scores from master.xlsx for model predictors

**Input:**
- data/cache/master.xlsx
- Required columns: UID, Age, RAVLT_Total, BVMT_Total, RPM_Score, Education, NART_Score, DASS_Total, Sleep, Sex

**Processing:**
- Load master.xlsx and extract cognitive test columns
- Convert categorical variables: Sex to dummy code (Male=1, Female=0)
- Handle missing data: document missingness patterns, exclude participants with >50% missing predictors
- Standardize continuous predictors to T-scores: mean=50, SD=10
- Transform: T = 50 + 10 * (X - mean(X)) / SD(X)
- Verify data quality: check ranges, outliers (>3 SDs), distributions
- Create 4 nested predictor sets:
  - Minimal: Age, RAVLT_Total
  - Core: Age, RAVLT_Total, BVMT_Total  
  - Extended: Core + RPM_Score, Education
  - Full: Extended + NART_Score, DASS_Total, Sleep, Sex

**Output:**
- data/step01_cognitive_tests.csv (raw scores with UID)
- data/step01_predictors_standardized.csv (T-scored predictors)
- data/step01_model_specifications.csv (4 nested models with predictor lists)

**Validation Requirement:**
Validation tools MUST be used after cognitive test extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_cognitive_tests.csv: 100 rows x 10 columns
- data/step01_predictors_standardized.csv: 100 rows x 10 columns  
- data/step01_model_specifications.csv: 4 rows x 3 columns (model_name, predictors, n_predictors)

*Value Ranges:*
- Age: 18-80 years (valid adult range)
- T-scores: 20-80 (3 SDs from mean=50)
- RAVLT_Total: 0-75 (test maximum)
- BVMT_Total: 0-36 (test maximum)
- Sex: 0,1 (binary dummy coding)

*Data Quality:*
- All 100 participants present
- Missing data <10% per variable
- No impossible values (negative ages, out-of-range test scores)
- T-score distributions: mean ≈ 50, SD ≈ 10

*Log Validation:*
- Required patterns: "Cognitive tests extracted: 100 participants", "T-score standardization complete"
- Forbidden patterns: "ERROR", "MISSING REQUIRED COLUMNS", ">50% missing"

**Expected Behavior on Validation Failure:**
- Log specific missing columns or excessive missingness
- Document which participants excluded and why
- Quit if <80 participants remain after exclusions

### Step 2: Extract REMEMVR Theta Scores
**Dependencies:** Step 0-1 (dependencies + cognitive tests)
**Complexity:** Low (~3 minutes)

**Purpose:** Extract theta_all scores from Ch5 5.1.1 IRT calibration results

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/*theta*.csv
- Expected format: UID, theta_all (mean across 4 tests)

**Processing:**
- Load theta scores from Ch5 5.1.1 results
- Verify expected format: UID (character), theta_all (numeric)
- Check data quality: theta_all in reasonable IRT range [-4, +4]
- Calculate descriptive statistics: mean, SD, range, quartiles
- Identify any extreme outliers (>3 SDs from mean)
- Document theta score distribution for later interpretation

**Output:**
- data/step02_theta_scores.csv (UID, theta_all)
- data/step02_theta_descriptives.csv (descriptive statistics)

**Validation Requirement:**
Validation tools MUST be used after theta extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_theta_scores.csv: 100 rows x 2 columns (UID, theta_all)
- data/step02_theta_descriptives.csv: 1 row x 7 columns (n, mean, sd, min, q25, q75, max)

*Value Ranges:*
- theta_all: [-4, +4] (reasonable IRT ability range)
- mean theta_all: [-1, +1] (centered around average ability)
- SD theta_all: [0.5, 2.0] (reasonable variability)

*Data Quality:*
- All 100 participants present
- No missing theta_all values
- No duplicate UIDs
- Distribution approximately normal (visual check)

*Log Validation:*
- Required patterns: "Theta scores loaded: 100 participants", "IRT range validated"
- Forbidden patterns: "ERROR", "OUTSIDE IRT RANGE", "MISSING THETA"

**Expected Behavior on Validation Failure:**
- Document out-of-range theta values
- Check for UID mismatches with cognitive data
- Quit if fundamental data integrity issues detected

### Step 3: Merge Analysis Dataset
**Dependencies:** Steps 1-2 (cognitive tests + theta scores)
**Complexity:** Low (~3 minutes)

**Purpose:** Create complete analysis dataset merging cognitive predictors with theta_all outcome

**Input:**
- data/step01_predictors_standardized.csv (T-scored predictors)
- data/step02_theta_scores.csv (theta_all outcome)

**Processing:**
- Merge datasets on UID using inner join
- Verify complete case analysis: no missing data in merged dataset
- Calculate correlation matrix among all predictors to assess multicollinearity
- Create final analysis dataset with columns: UID, theta_all, all predictors
- Generate descriptive statistics for full analysis dataset
- Document final sample size and any exclusions

**Output:**
- data/step03_analysis_input.csv (complete analysis dataset)
- data/step03_predictor_correlations.csv (correlation matrix)
- data/step03_final_descriptives.csv (descriptive statistics)

**Validation Requirement:**
Validation tools MUST be used after dataset merging.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_analysis_input.csv: N rows x 11 columns (UID + theta_all + 9 predictors)
- data/step03_predictor_correlations.csv: 9 rows x 9 columns (predictor correlation matrix)
- data/step03_final_descriptives.csv: 10 rows x 6 columns (variable stats)

*Value Ranges:*
- Final N: 95-100 (minimal exclusions expected)
- Correlations: [-1, +1] (valid correlation range)
- Highest correlation: <0.80 (avoid extreme multicollinearity)

*Data Quality:*
- No missing values in analysis dataset
- All UIDs unique
- Correlation matrix symmetric with 1.0 on diagonal
- No impossible correlation values

*Log Validation:*
- Required patterns: "Merge complete: N=XX participants", "No missing data confirmed"
- Forbidden patterns: "ERROR", "MISSING VALUES DETECTED", "CORRELATION >0.90"

**Expected Behavior on Validation Failure:**
- Document specific missing data patterns
- Check for extreme multicollinearity (r>0.90)
- Proceed with reduced N if >95 participants available

### Step 4: Fit Nested Regression Models
**Dependencies:** Step 3 (analysis dataset)
**Complexity:** Medium (~8 minutes)

**Purpose:** Fit 4 nested multiple regression models predicting theta_all with increasing complexity

**Input:**
- data/step03_analysis_input.csv (complete analysis dataset)
- data/step01_model_specifications.csv (nested model definitions)

**Processing:**
- Implement 4 nested regression models using sklearn.linear_model.LinearRegression:
  - Model 1 (Minimal): theta_all ~ Age + RAVLT_Total
  - Model 2 (Core): theta_all ~ Age + RAVLT_Total + BVMT_Total
  - Model 3 (Extended): theta_all ~ Age + RAVLT_Total + BVMT_Total + RPM_Score + Education
  - Model 4 (Full): theta_all ~ Age + RAVLT_Total + BVMT_Total + RPM_Score + Education + NART_Score + DASS_Total + Sleep + Sex

- For each model extract:
  - R-squared (training performance)
  - Adjusted R-squared
  - F-statistic and p-value
  - Standardized beta coefficients
  - Standard errors for coefficients
  - VIF for multicollinearity check (if VIF >5, flag concern)

- Statistical significance testing:
  - Within-RQ family: 4 models x 2-9 predictors = multiple comparison consideration
  - Bonferroni correction: alpha = 0.05/maximum_predictors = 0.05/9 = 0.0056
  - Report BOTH uncorrected AND corrected p-values (Decision D068)

**Output:**
- data/step04_nested_models.csv (model summaries with R², F-stats)
- data/step04_model_coefficients.csv (betas, SEs, VIFs for all models)
- data/step04_model_diagnostics.csv (assumption check results per model)

**Validation Requirement:**
Validation tools MUST be used after model fitting.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_nested_models.csv: 4 rows x 6 columns (model_name, n_predictors, r_squared, adj_r_squared, f_stat, p_value)
- data/step04_model_coefficients.csv: 28 rows x 7 columns (model, predictor, beta, se, t_stat, p_uncorrected, p_bonferroni)
- data/step04_model_diagnostics.csv: 4 rows x 4 columns (model, max_vif, shapiro_p, cook_max)

*Value Ranges:*
- R-squared: [0, 1] (valid R² range)
- R-squared progression: increasing with model complexity
- Standardized betas: [-3, +3] (reasonable for standardized predictors)
- VIF: [1, 10] (multicollinearity acceptable if <10)
- p-values: [0, 1] (valid probability range)

*Data Quality:*
- All 4 models fitted successfully
- R-squared increases or stays constant across nested models
- No convergence failures
- Dual p-values present for all coefficients (Decision D068)

*Log Validation:*
- Required patterns: "4 models fitted successfully", "VIF checks complete", "Dual p-values computed"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "VIF >10", "SINGULAR MATRIX"

**Expected Behavior on Validation Failure:**
- Document specific fitting failures
- Check for perfect multicollinearity if singular matrix error
- Proceed with successfully fitted models if partial failure

### Step 5: Cross-Validation Analysis
**Dependencies:** Step 4 (fitted models)
**Complexity:** High (~15 minutes including bootstrap)

**Purpose:** Implement 5-fold cross-validation to assess generalization performance and quantify overfitting

**Input:**
- data/step03_analysis_input.csv (analysis dataset)
- data/step01_model_specifications.csv (model definitions)

**Processing:**
- Implement 5-fold cross-validation using sklearn.model_selection.KFold:
  - Random seed: 42 for reproducibility
  - Shuffle: True (randomize before splitting)
  - Stratification: Use quantile-based stratification on Age (maintain age distribution across folds)
  - For each fold: fit on training (80%), evaluate on test (20%)

- For each model x fold combination:
  - Fit model on training data
  - Predict on test data
  - Calculate test R-squared

- Compute across-fold statistics:
  - Mean CV R-squared ± SE across 5 folds
  - Training R-squared (from full dataset)
  - Shrinkage = Training R² - CV R²
  - Flag overfitting if shrinkage >0.10

- Bootstrap confidence intervals for CV R-squared:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Participant-level resampling with replacement
  - For each iteration: 5-fold CV, compute mean CV R²
  - 95% CI: percentile method (2.5th, 97.5th percentiles)

- Model comparison:
  - Identify best CV R-squared
  - Apply parsimony criterion: prefer simpler model if CV R² within 0.02
  - Test significance of R² improvements between nested models

**Output:**
- data/step05_cv_results.csv (training vs CV R² by model with shrinkage)
- data/step05_cv_bootstrap_cis.csv (bootstrap 95% CIs for CV R²)
- data/step05_fold_details.csv (R² for each model x fold combination)

**Validation Requirement:**
Validation tools MUST be used after cross-validation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_cv_results.csv: 4 rows x 7 columns (model, train_r2, cv_r2_mean, cv_r2_se, shrinkage, overfitting_flag, rank)
- data/step05_cv_bootstrap_cis.csv: 4 rows x 5 columns (model, cv_r2_mean, ci_lower, ci_upper, ci_width)
- data/step05_fold_details.csv: 20 rows x 4 columns (model, fold, train_r2, test_r2)

*Value Ranges:*
- CV R-squared: [0, 1] (valid range)
- CV R² < Training R² (expected shrinkage)
- Shrinkage: [0, 0.30] (reasonable range)
- Bootstrap CIs: contain point estimates
- SE values: >0 (positive standard errors)

*Data Quality:*
- All 20 model x fold combinations present
- CV R² bootstrap CIs are valid (ci_lower < mean < ci_upper)
- Fold sample sizes ±2 participants (balanced folds)
- No failed CV iterations

*Log Validation:*
- Required patterns: "5-fold CV complete: 20 model-fold combinations", "Bootstrap complete: 1000 iterations", "Optimal model identified"
- Forbidden patterns: "ERROR", "CV FAILED", "BOOTSTRAP CONVERGENCE", "NEGATIVE R-SQUARED"

**Expected Behavior on Validation Failure:**
- Document specific CV failures
- Check for numerical instability in fold assignment
- Proceed with available folds if partial failure (minimum 3 folds required)

### Step 6: Model Selection and Optimal Model Analysis
**Dependencies:** Step 5 (cross-validation results)
**Complexity:** Medium (~8 minutes)

**Purpose:** Identify optimal model based on parsimony-performance trade-off and conduct detailed analysis

**Input:**
- data/step05_cv_results.csv (CV performance rankings)
- data/step04_model_coefficients.csv (coefficient estimates)
- data/step03_analysis_input.csv (full dataset for optimal model refit)

**Processing:**
- Model selection criteria:
  - Primary: highest CV R-squared
  - Parsimony rule: prefer simpler model if CV R² difference <0.02
  - Overfitting penalty: avoid models with shrinkage >0.15

- Refit optimal model on full dataset for final coefficients:
  - Extract standardized beta coefficients with 95% CIs
  - Calculate semi-partial correlations (sr²) for unique variance decomposition
  - Compute predictor importance rankings

- Bootstrap confidence intervals for optimal model:
  - Iterations: 1000
  - Random seed: 42
  - Participant-level resampling with replacement
  - For each iteration: fit model, extract coefficients
  - 95% CI: percentile method for each coefficient

- Power analysis:
  - Post-hoc power analysis for optimal model
  - Given: Final N, number of predictors, observed R²
  - Calculate: achieved power for detected effect size
  - Use: statsmodels.stats.power.FTestAnovaPower()
  - Alpha level: 0.05 (not corrected at model level)

**Output:**
- data/step06_optimal_model.csv (selected model with coefficients and CIs)
- data/step06_semipartial_correlations.csv (unique variance decomposition)
- data/step06_power_analysis.csv (post-hoc power calculation)

**Validation Requirement:**
Validation tools MUST be used after optimal model analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_optimal_model.csv: N_predictors rows x 8 columns (predictor, beta, se, ci_lower, ci_upper, sr2, t_stat, p_value)
- data/step06_semipartial_correlations.csv: N_predictors rows x 4 columns (predictor, sr2, sr2_pct, rank)
- data/step06_power_analysis.csv: 1 row x 6 columns (model, n, k, r2_obs, f2, power)

*Value Ranges:*
- Standardized betas: [-2, +2] (reasonable for T-scored predictors)
- Semi-partial r²: [0, 1] (valid unique variance range)
- Sum of sr² ≤ total R² (mathematical constraint)
- Power: [0, 1] (valid probability range)
- Confidence intervals: non-degenerate (ci_lower < ci_upper)

*Data Quality:*
- Bootstrap CIs stable (not excessively wide)
- Semi-partial correlations sum to ≤ total R²
- Power analysis results reasonable for sample size
- No undefined or infinite values

*Log Validation:*
- Required patterns: "Optimal model selected", "Bootstrap CIs computed", "Power analysis complete"
- Forbidden patterns: "ERROR", "BOOTSTRAP FAILURE", "POWER CALCULATION FAILED"

**Expected Behavior on Validation Failure:**
- Document model selection logic if unclear
- Check bootstrap stability if CIs unreasonably wide
- Verify power calculation inputs if results implausible

### Step 7: Model Diagnostics and Assumption Validation
**Dependencies:** Step 6 (optimal model)
**Complexity:** Medium (~7 minutes)

**Purpose:** Comprehensive assumption checking for optimal model with remedial actions if violations detected

**Input:**
- data/step06_optimal_model.csv (optimal model specification)
- data/step03_analysis_input.csv (full dataset)

**Processing:**
- Refit optimal model for diagnostic analysis
- Assumption validation:
  - Normality: Shapiro-Wilk test on residuals (p >0.05 acceptable)
  - Homoscedasticity: Breusch-Pagan test (p >0.05 acceptable)  
  - Linearity: Partial residual plots (visual inspection)
  - Multicollinearity: VIF for each predictor (<5 acceptable)
  - Outliers: Cook's distance (>4/n flagged for investigation)

- Remedial actions if assumptions violated:
  - Normality p <0.05: Use bootstrap CIs (1000 iterations, seed=42) as primary inference
  - Heteroscedasticity p <0.05: Report HC3 robust standard errors alongside regular SEs
  - VIF >5: Document multicollinearity, consider ridge regression if VIF >10
  - Outliers (Cook's D >4/n): Report results with and without outliers

- Sensitivity analysis:
  - Exclude influential points (Cook's D >4/n) and refit
  - Compare coefficient stability
  - Document impact on R² and significance

**Output:**
- data/step07_assumption_tests.csv (formal test results)
- data/step07_diagnostic_plots_data.csv (data for residual plots)
- data/step07_robust_results.csv (robust SEs and outlier-excluded results)

**Validation Requirement:**
Validation tools MUST be used after diagnostic analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_assumption_tests.csv: 4 rows x 5 columns (assumption, test_statistic, p_value, threshold, violation_flag)
- data/step07_diagnostic_plots_data.csv: N rows x 5 columns (observation, fitted, residual, standardized_resid, cooks_d)
- data/step07_robust_results.csv: N_predictors rows x 6 columns (predictor, beta_regular, se_regular, beta_robust, se_robust, beta_no_outliers)

*Value Ranges:*
- Test statistics: appropriate ranges for each test
- p-values: [0, 1] (valid probability range)
- Cook's D: [0, 1] typically (larger values possible but rare)
- VIF: [1, inf] but flag if >5
- Residuals: approximately normal distribution

*Data Quality:*
- All assumption tests completed
- Diagnostic data complete for all observations
- Robust results provided if heteroscedasticity detected
- Outlier analysis complete if influential points present

*Log Validation:*
- Required patterns: "Assumption validation complete", "Diagnostic plots data ready"
- Forbidden patterns: "ERROR", "TEST FAILED", "DIAGNOSTIC COMPUTATION FAILED"
- Acceptable warnings: "Normality violated - using bootstrap", "Heteroscedasticity detected - robust SEs reported"

**Expected Behavior on Validation Failure:**
- Document specific assumption violations clearly
- Ensure remedial actions taken if violations detected
- Proceed with robust methods if classical assumptions fail

### Step 8: Sensitivity Analysis and Final Summary
**Dependencies:** Step 7 (diagnostics)
**Complexity:** Medium (~6 minutes)

**Purpose:** Conduct sensitivity analyses and create comprehensive summary of parsimony analysis

**Input:**
- data/step05_cv_results.csv (all model comparisons)
- data/step06_optimal_model.csv (selected model)
- data/step07_assumption_tests.csv (diagnostic results)

**Processing:**
- Leave-one-out cross-validation comparison:
  - Implement LOOCV for optimal model
  - Compare LOOCV R² with 5-fold CV R²
  - Assess consistency of CV estimates

- Bootstrap stability assessment:
  - Model selection stability: In what % of bootstrap samples is the same model optimal?
  - Coefficient stability: Bootstrap 95% CIs for optimal model coefficients
  - CV R² stability: Bootstrap distribution of CV R² estimates

- Effect size interpretation:
  - Convert R² to Cohen's f² (f² = R²/(1-R²))
  - Classify effect sizes: small (f² =0.02), medium (f² =0.15), large (f² =0.35)
  - Calculate practical significance thresholds

- Comprehensive summary statistics:
  - Model comparison table with all 4 models
  - Optimal model coefficient summary with interpretations
  - Cross-validation performance summary
  - Assumption validation summary with remedial actions taken

**Output:**
- data/step08_sensitivity_analysis.csv (LOOCV and bootstrap stability)
- data/step08_effect_sizes.csv (R² to f² conversions with interpretations)
- data/step08_comprehensive_summary.csv (final analysis summary)

**Validation Requirement:**
Validation tools MUST be used after sensitivity analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_sensitivity_analysis.csv: 3 rows x 6 columns (analysis_type, metric, estimate, ci_lower, ci_upper, stability_pct)
- data/step08_effect_sizes.csv: 4 rows x 6 columns (model, r2, f2, effect_size_category, cohen_interpretation, practical_significance)
- data/step08_comprehensive_summary.csv: 1 row x 15 columns (optimal_model, cv_r2, train_r2, shrinkage, n_predictors, key_predictors, assumptions_met, remedial_actions, interpretation)

*Value Ranges:*
- LOOCV R²: within ±0.05 of 5-fold CV R² (reasonable consistency)
- Bootstrap stability: >50% (modest stability expected)
- Cohen's f²: [0, inf] with category assignments
- Confidence intervals: valid ranges for all estimates

*Data Quality:*
- Sensitivity analyses complete for all planned comparisons
- Effect size categorizations appropriate
- Comprehensive summary captures key findings
- No contradictory results between analyses

*Log Validation:*
- Required patterns: "Sensitivity analysis complete", "Effect sizes categorized", "Final summary generated"
- Forbidden patterns: "ERROR", "SENSITIVITY FAILED", "INCONSISTENT RESULTS"

**Expected Behavior on Validation Failure:**
- Document specific sensitivity analysis failures
- Check for numerical instability in bootstrap procedures
- Ensure comprehensive summary reflects all completed analyses

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)

**Step 0: Dependencies**
- data/step00_dependency_validation.txt (dependency check results)

**Step 1: Cognitive Tests**
- data/step01_cognitive_tests.csv (raw cognitive test scores)
- data/step01_predictors_standardized.csv (T-scored predictors)
- data/step01_model_specifications.csv (4 nested model definitions)

**Step 2: Theta Scores**
- data/step02_theta_scores.csv (REMEMVR theta_all scores)
- data/step02_theta_descriptives.csv (descriptive statistics)

**Step 3: Merged Dataset**
- data/step03_analysis_input.csv (complete analysis dataset)
- data/step03_predictor_correlations.csv (correlation matrix)
- data/step03_final_descriptives.csv (descriptive statistics)

**Step 4: Model Fitting**
- data/step04_nested_models.csv (4 model summaries)
- data/step04_model_coefficients.csv (betas, SEs, dual p-values)
- data/step04_model_diagnostics.csv (VIF, assumption checks)

**Step 5: Cross-Validation**
- data/step05_cv_results.csv (training vs CV R² with shrinkage)
- data/step05_cv_bootstrap_cis.csv (bootstrap CIs for CV R²)
- data/step05_fold_details.csv (detailed fold-by-fold results)

**Step 6: Optimal Model**
- data/step06_optimal_model.csv (selected model coefficients with CIs)
- data/step06_semipartial_correlations.csv (unique variance decomposition)
- data/step06_power_analysis.csv (post-hoc power calculations)

**Step 7: Diagnostics**
- data/step07_assumption_tests.csv (formal assumption test results)
- data/step07_diagnostic_plots_data.csv (residual data for plotting)
- data/step07_robust_results.csv (robust SEs, outlier-excluded results)

**Step 8: Sensitivity**
- data/step08_sensitivity_analysis.csv (LOOCV, bootstrap stability)
- data/step08_effect_sizes.csv (R² to Cohen's f² conversions)
- data/step08_comprehensive_summary.csv (final analysis summary)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_cognitive_tests.log
- logs/step02_extract_theta_scores.log
- logs/step03_merge_analysis_dataset.log
- logs/step04_fit_nested_models.log
- logs/step05_cross_validation_analysis.log
- logs/step06_optimal_model_analysis.log
- logs/step07_model_diagnostics.log
- logs/step08_sensitivity_analysis.log

### Plots (EMPTY until rq_plots runs)
Plot source CSVs created in data/ for later visualization:
- data/step05_fold_details.csv (for training vs CV R² plots)
- data/step07_diagnostic_plots_data.csv (for residual diagnostic plots)
- data/step08_effect_sizes.csv (for effect size comparison plots)

### Results (EMPTY until rq_results runs)
- results/summary.md will be created by rq_results agent

---

## Expected Data Formats

### Step-to-Step Transformations

1. **Raw Cognitive → Standardized Predictors**
   - Transform: T = 50 + 10 * (X - mean(X)) / SD(X)
   - Categorical: Sex dummy coded (Male=1, Female=0)

2. **Individual Models → Nested Comparison**
   - Progressive complexity: 2 → 3 → 5 → 8 predictors
   - Consistent outcome: theta_all standardized scores

3. **Training Performance → Cross-Validation Performance**
   - 5-fold CV with age stratification
   - Shrinkage = Training R² - CV R²

4. **Point Estimates → Bootstrap CIs**
   - 1000 iterations, participant-level resampling
   - Percentile method: 2.5th and 97.5th percentiles

### Column Naming Conventions

- **Identifiers:** UID (character, consistent across all files)
- **Outcomes:** theta_all (numeric, IRT ability scale)
- **Predictors:** Original names (Age, RAVLT_Total, etc.) preserved
- **Statistics:** r_squared, cv_r2_mean, shrinkage, beta, se, p_uncorrected, p_bonferroni
- **Confidence Intervals:** ci_lower, ci_upper (95% CIs unless specified)

### Data Type Constraints

- **UID:** character, no missing, no duplicates
- **Continuous variables:** numeric, finite values only
- **Test statistics:** positive for F-stats, VIF; [0,1] for R², p-values
- **Effect sizes:** non-negative for R², f²; [-inf,+inf] for standardized betas

---

## Cross-RQ Dependencies

**Dependency RQ:** Ch5 5.1.1 (Functional Form Comparison - IRT calibration)

**Required Files:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/theta_scores.csv
- Fallback pattern: results/ch5/5.1.1/data/*theta*.csv

**Expected Content:** 
- UID column (character) matching master.xlsx
- theta_all column (numeric, IRT scale) representing mean episodic memory ability
- N=100 rows (complete sample)

**Dependency Validation:**
- Ch5 5.1.1 status must be "success" in status.yaml
- Theta file must contain expected columns and sample size
- If files not found: QUIT with "Ch5 5.1.1 theta output not found - run Ch5 5.1.1 first"

**Master Data Dependency:**
- File: data/cache/master.xlsx
- Required columns: UID, Age, RAVLT_Total, BVMT_Total, RPM_Score, Education, NART_Score, DASS_Total, Sleep, Sex
- If missing: QUIT with "Master cognitive test data not found"

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Cross-RQ Dependency Handling

When Ch5 5.1.1 outputs are required:
- **Step 0:** Validates Ch5 completion before proceeding
- **Fallback strategy:** Multiple file name patterns attempted
- **Circuit breaker:** Analysis stops if dependencies unavailable
- **Error messaging:** Clear instructions for completing Ch5 5.1.1 first

### Statistical Specification Validation

Each statistical procedure includes:
- **Random seeds:** seed=42 for all randomized procedures
- **Iteration counts:** 1000 for bootstrap, 5 for cross-validation folds
- **Threshold criteria:** VIF <5, Cook's D >4/n, shrinkage <0.10 acceptable
- **Multiple comparisons:** Bonferroni correction with dual p-value reporting
- **Remedial actions:** Specific steps for assumption violations

### Validation Requirements By Step

#### Step 0: Validate Dependencies
- **File existence:** Ch5 outputs and master.xlsx accessible
- **Format verification:** Expected columns and data types present
- **Sample size:** N=100 confirmed in both sources

#### Step 1: Extract Cognitive Tests
- **Data quality:** <10% missing, reasonable value ranges
- **Standardization:** T-score distributions (mean≈50, SD≈10)
- **Model specifications:** 4 nested models properly defined

#### Step 2: Extract Theta Scores
- **IRT validity:** theta_all in [-4, +4] range
- **Completeness:** All 100 participants with non-missing theta
- **Distribution:** Approximately normal theta distribution

#### Step 3: Merge Analysis Dataset
- **Successful merge:** Inner join produces 95-100 complete cases
- **Correlation validity:** Predictor correlations <0.90 (avoid extreme multicollinearity)
- **Final quality:** No missing values in analysis dataset

#### Step 4: Fit Nested Models
- **Convergence:** All 4 models fit successfully
- **R² progression:** Non-decreasing R² across nested models
- **Dual p-values:** Both uncorrected and Bonferroni-corrected reported

#### Step 5: Cross-Validation
- **Fold balance:** 5 folds with ±2 participant difference
- **CV completion:** All 20 model×fold combinations successful
- **Bootstrap stability:** 1000 iterations complete with valid CIs

#### Step 6: Optimal Model Analysis
- **Selection logic:** Model chosen by parsimony-performance criteria
- **Semi-partial R²:** Sum of sr² ≤ total R² (mathematical constraint)
- **Power analysis:** Reasonable power estimates for sample size

#### Step 7: Model Diagnostics
- **Assumption tests:** All formal tests completed
- **Remedial actions:** Applied if violations detected
- **Diagnostic data:** Complete residual analysis dataset

#### Step 8: Sensitivity Analysis
- **LOOCV consistency:** Within ±0.05 of 5-fold CV estimates
- **Bootstrap stability:** Model selection stable >50% of samples
- **Comprehensive summary:** All key findings documented

---

## Summary

**Total Steps:** 9 (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** 45 minutes
**Cross-RQ Dependencies:** Ch5 5.1.1 (theta scores) + master.xlsx (cognitive tests)
**Primary Outputs:** Optimal parsimonious model with cross-validation performance assessment

**Key Hypothesis:** Core model (Age + RAVLT + BVMT) will achieve optimal balance of predictive performance (CV R² >0.20) and generalizability (shrinkage <0.10), outperforming both minimal and full models in cross-validation.

**Critical Methodological Notes:**
- All randomized procedures use seed=42 for reproducibility
- Cross-validation with age stratification prevents bias in fold assignment
- Bootstrap confidence intervals provide stability assessment for all key estimates
- Multiple comparison corrections applied within-RQ family (Decision D068)
- Comprehensive assumption validation with specified remedial actions
- Sensitivity analyses ensure robustness of conclusions

**Success Criteria:**
- [ ] Complete 5-fold cross-validation for all 4 nested models
- [ ] Identify optimal model using parsimony-performance trade-off
- [ ] Core model achieves CV R² >0.20 with shrinkage <0.10  
- [ ] All assumption violations addressed with appropriate remedial actions
- [ ] Bootstrap confidence intervals demonstrate estimate stability
- [ ] Comprehensive sensitivity analysis confirms robustness

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan → creates 3_tools.yaml (specifies exact tools needed)
3. rq_analysis reads plan + tools → creates 4_analysis.yaml (step-by-step execution)
4. g_code reads analysis → generates executable code for each step

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent with v5.1 statistical specifications