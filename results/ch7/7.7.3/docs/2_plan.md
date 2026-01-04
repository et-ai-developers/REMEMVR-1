# Analysis Plan: RQ 7.7.3 - Alternative RAVLT Scoring

**Research Question:** 7.7.3
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This analysis compares alternative RAVLT scoring methods to determine which best predicts episodic memory performance measured via REMEMVR theta scores. Tests traditional Total score vs Learning gain vs proportional Learning Slope vs Recognition scores through multiple regression with comprehensive validation.

**Pipeline:** Multiple regression with hierarchical model comparison
**Steps:** 9 total analysis steps (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** 45-60 minutes

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Chapter 7 Bonferroni: alpha = 0.05/28 = 0.00179 for within-chapter tests
- Within-RQ correction: alpha = 0.00179/5 = 0.000358 for 5 models tested

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 5.1.1 outputs and master.xlsx accessibility before proceeding

**Input:**
- results/ch5/5.1.1/status.yaml (verify rq_results: success)
- results/ch5/5.1.1/data/step03_theta_scores.csv (primary theta source)
- results/ch5/5.1.1/data/*theta*.csv (fallback pattern)
- data/cache/master.xlsx (RAVLT test scores)

**Processing:**
- Check Ch5 5.1.1 completed successfully (status = success)
- Locate theta_all scores file (try multiple patterns)
- Verify master.xlsx contains required RAVLT columns (T1Sc-T5Sc, DRSc, FRSc)
- Log all validation checks
- Document exact file paths found for downstream steps

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- File size: >500 bytes (comprehensive validation log)

*Value Ranges:*
- Status codes: 0 (success) or 1 (failure) for each check
- File counts: Ch5 files >= 1, master.xlsx = 1

*Data Quality:*
- All required dependencies documented
- Exact file paths recorded for found files
- Clear pass/fail status for each requirement

*Log Validation:*
- Required: "Ch5 5.1.1 status: success"
- Required: "Theta scores file found"
- Required: "RAVLT columns verified"
- Required: "VALIDATION - PASS"
- Forbidden: "ERROR", "FAIL", "not found"

**Expected Behavior on Validation Failure:**
- Raise error with specific missing dependency
- Log to logs/step00_validate_dependencies.log
- Quit immediately with dependency error

### Step 1: Extract and Prepare RAVLT Scores
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (<5 minutes)

**Purpose:** Extract RAVLT test scores from dfnonvr.csv and compute alternative scoring metrics

**Input:**
- data/cache/master.xlsx (RAVLT columns: T1Sc, T2Sc, T3Sc, T4Sc, T5Sc, DRSc, FRSc)

**Processing:**
- Load master.xlsx using pandas.read_excel()
- Extract participant UIDs and RAVLT columns
- Verify data completeness (no missing RAVLT scores)
- Compute alternative RAVLT metrics:
  - Total = sum(T1Sc + T2Sc + T3Sc + T4Sc + T5Sc)
  - Learning = T5Sc - T1Sc (absolute learning gain)
  - LearningSlope = (T5Sc - T1Sc) / T1Sc (proportional learning gain)
  - Forgetting = T5Sc - DRSc (learning to delay decline)
  - Recognition = FRSc (delayed recognition hits)
- Handle division by zero: if T1Sc = 0, set LearningSlope = NA
- Apply z-score standardization to all metrics
- Document data quality: N, missing values, outliers (>3 SD)

**Output:**
- data/step01_ravlt_scores.csv (UID, all RAVLT metrics, standardized versions)

**Validation Requirement:**
Validation tools MUST be used after RAVLT extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_ravlt_scores.csv: 100 rows x 15 columns
- Columns: UID, T1Sc-T5Sc, DRSc, FRSc, Total, Learning, LearningSlope, Forgetting, Recognition, z-scored versions

*Value Ranges:*
- T1-T5 scores in [0, 15] (RAVLT trial limits)
- DRSc in [0, 15] (delayed recall limit)
- FRSc in [0, 50] (recognition hits limit)
- Learning in [-15, 15] (T5-T1 difference)
- LearningSlope in [-1, 14] (proportional gain, allowing for T1=1)
- Z-scores approximately in [-3, 3] (standardized range)

*Data Quality:*
- All 100 participants present
- No missing values in raw RAVLT scores
- LearningSlope missing only if T1Sc = 0
- Z-scores have mean ~0, SD ~1

*Log Validation:*
- Required: "RAVLT extraction complete: 100 participants"
- Required: "Alternative metrics computed: 5 scoring methods"
- Required: "Standardization complete"
- Forbidden: "ERROR", "division by zero", "missing data"

**Expected Behavior on Validation Failure:**
- Raise error with specific data quality issue
- Log to logs/step01_extract_ravlt.log
- Quit immediately, invoke g_debug

### Step 2: Extract REMEMVR Theta Scores
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (<5 minutes)

**Purpose:** Load omnibus theta_all scores from Ch5 5.1.1 outputs

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/*theta*.csv
- Expected content: Participant UIDs with theta_all ability estimates

**Processing:**
- Load theta scores file using pandas.read_csv()
- Extract UID and theta_all columns (omnibus episodic memory ability)
- Verify theta range within IRT bounds [-4, 4]
- Check for missing theta values
- Apply outlier detection: theta outside [-3, 3] flagged but retained
- Compute descriptive statistics (mean, SD, range)
- Document any extreme theta values (> |3|)

**Output:**
- data/step02_theta_scores.csv (UID, theta_all, theta_standardized)

**Validation Requirement:**
Validation tools MUST be used after theta extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_theta_scores.csv: 100 rows x 3 columns
- Columns: UID (object), theta_all (float64), theta_standardized (float64)

*Value Ranges:*
- theta_all in [-4, 4] (IRT ability scale bounds)
- theta_standardized approximately in [-3, 3] (z-scored)
- No infinite or NaN values

*Data Quality:*
- All 100 participants present
- No missing theta values
- UIDs match expected format
- Mean theta approximately 0 (centered)

*Log Validation:*
- Required: "Theta extraction complete: 100 participants"
- Required: "Theta range: [min, max]"
- Required: "No missing theta values"
- Forbidden: "ERROR", "outside bounds", "NaN detected"

**Expected Behavior on Validation Failure:**
- Raise error with specific theta data issue
- Log to logs/step02_extract_theta.log
- Quit immediately, invoke g_debug

### Step 3: Merge and Prepare Analysis Dataset
**Dependencies:** Steps 1-2 (RAVLT + theta extraction)
**Complexity:** Low (<5 minutes)

**Purpose:** Combine RAVLT and theta data into final analysis dataset with quality checks

**Input:**
- data/step01_ravlt_scores.csv (RAVLT metrics)
- data/step02_theta_scores.csv (theta scores)

**Processing:**
- Merge datasets on UID using pandas.merge()
- Verify all participants have both RAVLT and theta data
- Create final predictor set: Total_z, Learning_z, LearningSlope_z, Recognition_z
- Handle LearningSlope missing values: document count, consider listwise deletion
- Compute correlation matrix for multicollinearity screening
- Check VIF prereq: pairwise correlations should be < 0.9
- Final dataset: standardized predictors + theta_all outcome
- Document final N after any exclusions

**Output:**
- data/step03_analysis_dataset.csv (UID, all standardized predictors, theta_all outcome)
- data/step03_correlation_matrix.csv (predictor intercorrelations)

**Validation Requirement:**
Validation tools MUST be used after dataset preparation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_analysis_dataset.csv: N rows x 6 columns (where N <= 100)
- Columns: UID, Total_z, Learning_z, LearningSlope_z, Recognition_z, theta_all
- data/step03_correlation_matrix.csv: 4 rows x 4 columns (predictor correlations)

*Value Ranges:*
- All _z predictors approximately in [-3, 3] (standardized)
- theta_all in [-4, 4] (IRT bounds)
- Correlations in [-1, 1]
- No correlations > |0.9| (multicollinearity check)

*Data Quality:*
- N >= 95 participants (allowing minimal exclusions)
- No missing values in final dataset
- All predictors properly standardized (mean ~0, SD ~1)
- Correlation matrix symmetric

*Log Validation:*
- Required: "Dataset merged: N participants"
- Required: "Multicollinearity check: all r < 0.9"
- Required: "Final dataset ready for analysis"
- Forbidden: "ERROR", "merge failed", "high correlation"

**Expected Behavior on Validation Failure:**
- Raise error with specific merge issue
- Log to logs/step03_prepare_dataset.log
- Quit immediately, invoke g_debug

### Step 4: Fit Multiple Regression Models
**Dependencies:** Step 3 (analysis dataset)
**Complexity:** Medium (~10 minutes including bootstrap)

**Purpose:** Fit 5 regression models comparing RAVLT scoring methods

**Input:**
- data/step03_analysis_dataset.csv (standardized predictors + theta outcome)

**Processing:**
- Fit 5 regression models using statsmodels.api.OLS:
  - Model 1: theta_all ~ Total_z
  - Model 2: theta_all ~ Learning_z  
  - Model 3: theta_all ~ LearningSlope_z
  - Model 4: theta_all ~ Recognition_z
  - Model 5: theta_all ~ Total_z + Learning_z (incremental validity)
- Extract model statistics: R², adjusted R², F-statistic, AIC, BIC
- Bootstrap 95% CIs for R² values:
  - Iterations: 1000
  - Seed: 42
  - Method: Participant-level resampling with replacement
  - CI: Percentile method (2.5th, 97.5th percentiles)
- Extract standardized coefficients (beta) with CIs
- Multiple comparison correction:
  - Family: Within-RQ (5 models)
  - Bonferroni: alpha = 0.00179/5 = 0.000358 per model
  - Report BOTH uncorrected AND corrected p-values (Decision D068)

**Output:**
- data/step04_model_results.csv (model statistics with dual p-values)
- data/step04_regression_coefficients.csv (betas, SEs, CIs, dual p-values)

**Validation Requirement:**
Validation tools MUST be used after regression modeling execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_model_results.csv: 5 rows x 10 columns
- Columns: model, R2, adj_R2, F_stat, p_uncorrected, p_bonferroni, AIC, BIC, R2_CI_lower, R2_CI_upper
- data/step04_regression_coefficients.csv: up to 6 rows x 8 columns (depends on predictors)
- Columns: model, predictor, beta, se, ci_lower, ci_upper, p_uncorrected, p_bonferroni

*Value Ranges:*
- R² in [0, 1] (variance explained)
- F-statistics > 0
- p-values in [0, 1]
- Beta coefficients approximately in [-2, 2] (standardized predictors)
- AIC/BIC finite values
- Bootstrap CIs valid (ci_lower < R² < ci_upper)

*Data Quality:*
- All 5 models fitted successfully
- Bootstrap completed 1000 iterations
- All confidence intervals valid
- Dual p-values present (Decision D068)
- Bonferroni correction properly applied (alpha = 0.000358)

*Log Validation:*
- Required: "5 regression models fitted"
- Required: "Bootstrap complete: 1000 iterations"
- Required: "Bonferroni correction: alpha = 0.000358"
- Required: "Dual p-values computed"
- Forbidden: "ERROR", "convergence failed", "singular matrix"

**Expected Behavior on Validation Failure:**
- Raise error with specific modeling issue
- Log to logs/step04_fit_models.log
- Quit immediately, invoke g_debug

### Step 5: Effect Size Analysis and Model Comparison
**Dependencies:** Step 4 (regression results)
**Complexity:** Medium (~8 minutes)

**Purpose:** Compute effect sizes, incremental validity tests, and model selection metrics

**Input:**
- data/step04_model_results.csv (model statistics)
- data/step04_regression_coefficients.csv (coefficients)

**Processing:**
- Compute Cohen's f² = R²/(1-R²) for each model
- Calculate semi-partial correlations (sr²) for unique variance explained
- Test incremental validity: Model 5 vs Model 1 (Total alone)
  - ΔR² = R²_Model5 - R²_Model1
  - F-test for ΔR² significance
  - Bootstrap CI for ΔR² (1000 iterations, seed=42)
- Model comparison using AIC weights:
  - Compute ΔAIC relative to best model
  - Calculate Akaike weights (wi)
  - Rank models by predictive performance
- Bootstrap effect sizes (1000 iterations, seed=42):
  - CI for Cohen's f² values
  - CI for semi-partial correlations
  - CI for incremental R²

**Output:**
- data/step05_effect_sizes.csv (f², sr², AIC weights with CIs)
- data/step05_incremental_validity.csv (ΔR² tests with significance)

**Validation Requirement:**
Validation tools MUST be used after effect size analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_effect_sizes.csv: 5 rows x 8 columns
- Columns: model, f2, f2_CI_lower, f2_CI_upper, sr2, sr2_CI_lower, sr2_CI_upper, AIC_weight
- data/step05_incremental_validity.csv: 1 row x 7 columns
- Columns: delta_R2, F_stat, df1, df2, p_uncorrected, p_bonferroni, delta_R2_CI

*Value Ranges:*
- Cohen's f² >= 0 (effect size metric)
- sr² in [0, 1] (proportion of unique variance)
- AIC weights sum to 1.0 across models
- ΔR² in [0, 1] (incremental variance)
- F-statistics > 0
- Bootstrap CIs valid (lower < point estimate < upper)

*Data Quality:*
- All 5 models have effect sizes computed
- Bootstrap completed successfully for all metrics
- AIC weights properly normalized
- Incremental validity test completed
- All confidence intervals valid

*Log Validation:*
- Required: "Effect sizes computed for 5 models"
- Required: "Incremental validity test complete"
- Required: "Bootstrap effect sizes: 1000 iterations"
- Required: "AIC weights sum to 1.0"
- Forbidden: "ERROR", "negative effect size", "invalid CI"

**Expected Behavior on Validation Failure:**
- Raise error with specific effect size issue
- Log to logs/step05_effect_sizes.log
- Quit immediately, invoke g_debug

### Step 6: Model Diagnostics and Assumption Checks
**Dependencies:** Step 4 (regression results)
**Complexity:** Medium (~10 minutes)

**Purpose:** Comprehensive assumption checking with remedial actions for violations

**Input:**
- data/step03_analysis_dataset.csv (analysis data)
- Model objects from Step 4 (for residual extraction)

**Processing:**
- For each of the 5 models, check assumptions:
  - **Normality:** Shapiro-Wilk test on standardized residuals
  - **Homoscedasticity:** Breusch-Pagan test
  - **Multicollinearity:** VIF for each predictor (Model 5 only)
  - **Independence:** Durbin-Watson test
  - **Outliers:** Cook's distance (threshold = 4/N)
- Remedial actions if assumptions violated:
  - Normality p < 0.05: Report bootstrap CIs as primary (already computed)
  - Heteroscedasticity p < 0.05: Compute HC3 robust standard errors
  - VIF > 5: Flag high multicollinearity, proceed with caution
  - VIF > 10: Drop most collinear predictor, refit model
  - Outliers (Cook's D > 4/N): Report results with/without outliers
- Generate diagnostic plots data:
  - Residuals vs fitted values
  - Q-Q plot coordinates
  - Histogram of residuals
  - Cook's distance values

**Output:**
- data/step06_assumption_tests.csv (test statistics and p-values)
- data/step06_diagnostic_data.csv (residuals, fitted values, Cook's D)
- data/step06_robust_results.csv (HC3 robust SEs if needed)

**Validation Requirement:**
Validation tools MUST be used after diagnostic analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_assumption_tests.csv: 5 rows x 8 columns
- Columns: model, shapiro_stat, shapiro_p, bp_stat, bp_p, dw_stat, max_vif, outlier_count
- data/step06_diagnostic_data.csv: N*5 rows x 5 columns (residuals for each model)
- Columns: model, fitted, residuals, std_residuals, cooks_d

*Value Ranges:*
- Test statistics finite and non-negative where applicable
- p-values in [0, 1]
- VIF >= 1 (variance inflation factor)
- Cook's D >= 0 (influence measure)
- Durbin-Watson approximately in [1.5, 2.5] (independence)

*Data Quality:*
- All 5 models have complete diagnostic results
- No infinite or NaN test statistics
- Outlier counts reasonable (< 10% of sample)
- VIF computed only for models with multiple predictors

*Log Validation:*
- Required: "Assumption checks complete: 5 models"
- Required: "Normality tests: Shapiro-Wilk"
- Required: "Homoscedasticity: Breusch-Pagan"
- Required: "Outlier detection: Cook's D"
- Required: "VIF computed for Model 5"
- Acceptable warnings: "Normality assumption violated", "Heteroscedasticity detected"
- Forbidden: "ERROR", "test failed", "infinite statistic"

**Expected Behavior on Validation Failure:**
- Raise error with specific diagnostic issue
- Log to logs/step06_model_diagnostics.log
- Document assumption violations as warnings, not errors

### Step 7: Cross-Validation Analysis
**Dependencies:** Steps 3-4 (dataset and models)
**Complexity:** Medium (~10 minutes)

**Purpose:** Evaluate model generalizability through 5-fold cross-validation

**Input:**
- data/step03_analysis_dataset.csv (full dataset)

**Processing:**
- Implement 5-fold cross-validation using sklearn.model_selection.KFold:
  - Random seed: 42 for reproducibility
  - Shuffle: True (randomize before splitting)
  - Stratification: None (continuous outcome)
- For each fold and each model:
  - Fit on training set (80% of data)
  - Predict on test set (20% of data)
  - Compute test set R², RMSE, MAE
- Aggregate across folds:
  - Mean and SD of test R² for each model
  - Mean and SD of RMSE for each model
  - Training-test R² gap = mean(train_R²) - mean(test_R²)
- Overfitting detection:
  - Flag if train-test R² gap > 0.10 for any model
  - Compute shrinkage = (train_R² - test_R²) / train_R²
- Rank models by cross-validated R² performance

**Output:**
- data/step07_cv_results.csv (fold-wise results for all models)
- data/step07_cv_summary.csv (aggregated CV performance metrics)

**Validation Requirement:**
Validation tools MUST be used after cross-validation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_cv_results.csv: 25 rows x 6 columns (5 folds × 5 models)
- Columns: fold, model, train_R2, test_R2, RMSE, MAE
- data/step07_cv_summary.csv: 5 rows x 7 columns
- Columns: model, mean_test_R2, sd_test_R2, mean_RMSE, train_test_gap, shrinkage, overfitting_flag

*Value Ranges:*
- R² values in [0, 1]
- RMSE > 0 (prediction error)
- MAE > 0 (absolute error)
- Train-test gap in [0, 1]
- Shrinkage approximately in [0, 1]

*Data Quality:*
- Exactly 25 CV results (5 folds × 5 models)
- All models completed CV successfully
- No missing CV statistics
- Overfitting flags properly computed
- Random seed 42 used consistently

*Log Validation:*
- Required: "5-fold CV complete: 5 models"
- Required: "Random seed: 42"
- Required: "CV performance computed"
- Acceptable warnings: "Overfitting detected: train-test gap > 0.10"
- Forbidden: "ERROR", "CV failed", "infinite RMSE"

**Expected Behavior on Validation Failure:**
- Raise error with specific CV issue
- Log to logs/step07_cross_validation.log
- Quit immediately, invoke g_debug

### Step 8: Power Analysis and Sensitivity Testing
**Dependencies:** Steps 4-5 (model results and effect sizes)
**Complexity:** Medium (~8 minutes)

**Purpose:** Post-hoc power analysis and sensitivity tests for observed effects

**Input:**
- data/step04_model_results.csv (observed R² values)
- data/step05_effect_sizes.csv (observed Cohen's f²)

**Processing:**
- Post-hoc power analysis for each model:
  - Given: N=100, alpha=0.000358 (Bonferroni-corrected)
  - Observed effect sizes (f²) from Step 5
  - Compute: achieved power using statsmodels.stats.power.FTestAnovaPower()
  - For Model 5: hierarchical F-test power (ΔR² significance)
- Sensitivity analysis:
  - Minimum detectable f² at 80% power given N=100, alpha=0.000358
  - Required N for 80% power to detect small (f²=0.02), medium (f²=0.15), large (f²=0.35) effects
- Effect interpretation guidelines:
  - f² < 0.02: trivial effect
  - f² 0.02-0.15: small effect  
  - f² 0.15-0.35: medium effect
  - f² > 0.35: large effect
- Document power limitations for non-significant findings

**Output:**
- data/step08_power_analysis.csv (achieved power for observed effects)
- data/step08_sensitivity.csv (minimum detectable effects and required N)

**Validation Requirement:**
Validation tools MUST be used after power analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_power_analysis.csv: 5 rows x 6 columns
- Columns: model, observed_f2, alpha, achieved_power, interpretation, adequate_power_flag
- data/step08_sensitivity.csv: 3 rows x 4 columns
- Columns: effect_size, f2_threshold, required_N_80pct, current_N_power

*Value Ranges:*
- Power values in [0, 1]
- f² values >= 0
- Alpha = 0.000358 (Bonferroni-corrected)
- Required N >= 1 (sample size calculations)

*Data Quality:*
- All 5 models have power calculations
- Sensitivity analysis for 3 effect size categories
- Power adequacy flags properly computed (>= 0.80)
- Effect size interpretations assigned correctly

*Log Validation:*
- Required: "Power analysis complete: 5 models"
- Required: "Sensitivity analysis: 3 effect sizes"
- Required: "Alpha level: 0.000358 (Bonferroni)"
- Acceptable warnings: "Low power detected: power < 0.80"
- Forbidden: "ERROR", "invalid power", "negative f2"

**Expected Behavior on Validation Failure:**
- Raise error with specific power analysis issue
- Log to logs/step08_power_analysis.log
- Quit immediately, invoke g_debug

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (prerequisite checks)
- data/step01_ravlt_scores.csv (extracted RAVLT metrics)
- data/step02_theta_scores.csv (REMEMVR theta abilities)
- data/step03_analysis_dataset.csv (merged analysis data)
- data/step03_correlation_matrix.csv (predictor correlations)
- data/step04_model_results.csv (regression statistics)
- data/step04_regression_coefficients.csv (betas with dual p-values)
- data/step05_effect_sizes.csv (f², sr², AIC weights)
- data/step05_incremental_validity.csv (ΔR² tests)
- data/step06_assumption_tests.csv (diagnostic results)
- data/step06_diagnostic_data.csv (residuals, Cook's D)
- data/step06_robust_results.csv (HC3 robust SEs if needed)
- data/step07_cv_results.csv (cross-validation fold results)
- data/step07_cv_summary.csv (CV performance summary)
- data/step08_power_analysis.csv (achieved power)
- data/step08_sensitivity.csv (minimum detectable effects)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_ravlt.log
- logs/step02_extract_theta.log  
- logs/step03_prepare_dataset.log
- logs/step04_fit_models.log
- logs/step05_effect_sizes.log
- logs/step06_model_diagnostics.log
- logs/step07_cross_validation.log
- logs/step08_power_analysis.log

### Plots (EMPTY until rq_plots runs)
- Plot source CSVs created in data/ folder:
  - data/step04_model_comparison_plot_data.csv
  - data/step06_diagnostic_plots_plot_data.csv
  - data/step07_cv_performance_plot_data.csv

### Results (EMPTY until rq_results runs)
- results/summary.md (created by rq_results agent)

---

## Expected Data Formats

### Step-to-Step Transformations
- Step 1: Raw RAVLT scores -> computed metrics -> standardized scores
- Step 2: Ch5 theta estimates -> standardized theta_all
- Step 3: RAVLT + theta merge -> analysis-ready dataset
- Steps 4-8: Sequential analysis building on core dataset

### Column Naming Conventions
- Predictors: Total_z, Learning_z, LearningSlope_z, Recognition_z (standardized)
- Outcome: theta_all (original IRT scale)
- Model IDs: "Model_1" through "Model_5"
- P-values: p_uncorrected, p_bonferroni (dual reporting per D068)

### Data Type Constraints
- UIDs: object (string identifiers)
- Scores: float64 (continuous measures)
- Flags: bool (True/False indicators)
- Model names: object (categorical labels)

---

## Cross-RQ Dependencies

**Dependency:** Ch5 5.1.1 (Functional Form Comparison)
- **Required Output:** Omnibus theta_all scores from IRT calibration
- **File Pattern:** results/ch5/5.1.1/data/*theta*.csv
- **Format:** UID, theta_all columns required
- **Status Check:** results/ch5/5.1.1/status.yaml (rq_results: success)
- **Circuit Breaker:** If Ch5 5.1.1 incomplete, QUIT with dependency error

**Master Data:** RAVLT test scores
- **Required File:** data/cache/master.xlsx  
- **Columns:** T1Sc, T2Sc, T3Sc, T4Sc, T5Sc, DRSc, FRSc
- **Circuit Breaker:** If RAVLT columns missing, QUIT with data error

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
- **Requirement:** Validation tools MUST be used after dependency check
- **4-layer criteria:** File existence, status verification, column checks, path documentation

#### Step 1: Extract RAVLT Scores  
- **Requirement:** Validation tools MUST be used after RAVLT extraction
- **4-layer criteria:** Row/column counts, value ranges, standardization verification, missing data checks

#### Step 2: Extract Theta Scores
- **Requirement:** Validation tools MUST be used after theta extraction  
- **4-layer criteria:** Theta bounds, IRT scale validation, missing value checks, UID verification

#### Step 3: Prepare Analysis Dataset
- **Requirement:** Validation tools MUST be used after dataset merge
- **4-layer criteria:** Merge success, final N, correlation bounds, standardization verification

#### Step 4: Fit Regression Models
- **Requirement:** Validation tools MUST be used after regression modeling
- **4-layer criteria:** Model convergence, dual p-values, bootstrap completion, correction verification

#### Step 5: Effect Size Analysis
- **Requirement:** Validation tools MUST be used after effect size computation
- **4-layer criteria:** Effect size bounds, CI validity, AIC weight normalization, incremental tests

#### Step 6: Model Diagnostics  
- **Requirement:** Validation tools MUST be used after diagnostic analysis
- **4-layer criteria:** Assumption test completion, outlier detection, VIF computation, remedial action triggers

#### Step 7: Cross-Validation
- **Requirement:** Validation tools MUST be used after CV analysis
- **4-layer criteria:** CV completion, overfitting detection, performance metrics, random seed verification

#### Step 8: Power Analysis
- **Requirement:** Validation tools MUST be used after power analysis
- **4-layer criteria:** Power calculation bounds, sensitivity thresholds, effect interpretation, adequacy flags

---

## Summary

**Total Steps:** 9 (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** 45-60 minutes  
**Cross-RQ Dependencies:** Ch5 5.1.1 (theta scores), master.xlsx (RAVLT scores)
**Primary Outputs:** 5 regression models comparing RAVLT scoring methods with comprehensive validation
**Validation Coverage:** 100% (all 9 steps have 4-layer validation requirements)

**Key Hypothesis:** Learning-based RAVLT metrics (Learning, LearningSlope) will predict REMEMVR theta scores better than traditional Total score, providing evidence for alternative clinical interpretation.

**Critical Methodological Notes:**
- Bonferroni correction within-RQ: alpha = 0.000358 for 5 models tested
- Bootstrap CIs (1000 iterations, seed=42) for all effect sizes
- 5-fold cross-validation to assess generalizability  
- Comprehensive assumption checking with remedial actions
- Dual p-value reporting (Decision D068: uncorrected + corrected)
- Post-hoc power analysis for observed and minimal detectable effects

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml  
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent