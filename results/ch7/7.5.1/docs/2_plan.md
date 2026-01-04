# Analysis Plan: RQ 7.5.1 - Self-Report Predictors of REMEMVR Performance

**Research Question:** 7.5.1
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This analysis examines whether self-reported factors (education level, sleep duration, VR experience) predict REMEMVR performance using mean theta scores from Ch5. The approach uses multiple regression with hierarchical entry, cross-validation, and comprehensive model diagnostics to assess individual difference predictors while controlling for age confounding.

**Pipeline:** Multiple Linear Regression with Hierarchical Entry and Cross-Validation
**Steps:** 9 total analysis steps (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** 45-60 minutes

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Within-RQ Bonferroni correction for 3 main predictors (alpha = 0.05/3 = 0.0167)
- Bootstrap CIs for robust estimation with 1000 iterations

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 outputs and master.xlsx accessibility before proceeding with self-report predictor analysis

**Input:**
- Primary: results/ch5/5.1.1/status.yaml (verify rq_results: success)
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv (theta estimates)
- Alternative: results/ch5/5.1.1/data/*theta*.csv (fallback pattern)
- Primary: data/cache/master.xlsx (self-report measures)
- Alternative: /home/etai/projects/REMEMVR/data/cache/master.xlsx
- Expected content: Theta_all scores for 100 participants, self-report variables (Education, Typical_Sleep, VR_Experience, Age)

**Processing:**
- Check Ch5 5.1.1 completed successfully (status.yaml verification)
- Locate theta score file using multiple patterns
- Verify master.xlsx contains required self-report columns
- Check sample size alignment (N=100 expected in both sources)
- Log all validation checks with pass/fail status
- If dependencies missing: QUIT with specific error message

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- File size: >500 characters (comprehensive check results)

*Value Ranges:*
- Not applicable (text file validation)

*Data Quality:*
- Ch5 status confirmed as "success"
- Theta file located and verified (100 participants)
- Master.xlsx accessible with required columns
- No missing dependencies reported

*Log Validation:*
- Required pattern: "Ch5 5.1.1 dependency VALIDATED"
- Required pattern: "master.xlsx dependency VALIDATED"
- Required pattern: "Sample size N=100 CONFIRMED"
- Forbidden patterns: "MISSING", "FAIL", "not found"

**Expected Behavior on Validation Failure:**
- Raise error with specific missing dependency
- Log failure to logs/step00_validate_dependencies.log
- QUIT immediately, invoke g_debug

### Step 1: Extract Self-Report Measures
**Dependencies:** Step 0 complete
**Complexity:** Low (<5 minutes)

**Purpose:** Extract self-report and demographic variables from dfnonvr.csv for regression analysis

**Input:**
- data/cache/master.xlsx (verified in Step 0)
- Expected columns: UID, Education, Typical_Sleep, VR_Experience, Age
- Expected format: Education (years, continuous), Typical_Sleep (hours, continuous), VR_Experience (ordinal scale), Age (years, continuous)

**Processing:**
- Load master.xlsx using pandas.read_excel()
- Extract target columns: UID, Education, Typical_Sleep, VR_Experience, Age
- Check data types and ranges:
  - Education: 8-25 years (reasonable range for college-age adults)
  - Typical_Sleep: 4-12 hours (physiologically plausible)
  - VR_Experience: 0-5 scale (low to high familiarity)
  - Age: 18-35 years (young adult sample)
- Check missing data pattern (expect <5% missing per variable)
- Convert categorical VR_Experience to numeric if stored as text
- Document data quality issues

**Output:**
- data/step01_self_report_data.csv

**Validation Requirement:**
Validation tools MUST be used after data extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_self_report_data.csv: 100 rows x 5 columns
- Columns: UID (object), Education (float64), Typical_Sleep (float64), VR_Experience (int64), Age (float64)

*Value Ranges:*
- Education in [8, 25] years
- Typical_Sleep in [4, 12] hours  
- VR_Experience in [0, 5] ordinal scale
- Age in [18, 35] years
- No negative values in any measure

*Data Quality:*
- All 100 participants present (no missing UIDs)
- Missing data <5% per variable
- No duplicate UIDs
- Data types match specifications

*Log Validation:*
- Required pattern: "Self-report extraction complete: 100 participants"
- Required pattern: "Missing data check: <5% per variable"
- Forbidden patterns: "ERROR", "MISSING >5%", "duplicate UID"

**Expected Behavior on Validation Failure:**
- Raise error with specific data quality issue
- Log failure to logs/step01_extract_self_report.log
- QUIT immediately, invoke g_debug

### Step 2: Extract Theta Scores from Ch5
**Dependencies:** Step 0-1 complete
**Complexity:** Low (<5 minutes)

**Purpose:** Load mean theta_all scores from Ch5 5.1.1 IRT calibration results

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/*theta*.csv
- Expected content: UID, theta_all (mean across domains), theta_SE
- Expected format: 100 rows, theta in [-3, 3] range

**Processing:**
- Load Ch5 theta scores using identified file path from Step 0
- Extract UID and theta_all columns (dependent variable)
- Verify theta range in [-3, 3] (standard IRT metric)
- Check theta_SE values in [0.1, 1.0] (reasonable standard errors)
- Document any extreme values (|theta| > 2.5)
- Verify N=100 participants match expected sample

**Output:**
- data/step02_theta_scores.csv

**Validation Requirement:**
Validation tools MUST be used after theta extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_theta_scores.csv: 100 rows x 3 columns  
- Columns: UID (object), theta_all (float64), theta_SE (float64)

*Value Ranges:*
- theta_all in [-3, 3] (IRT ability scale)
- theta_SE in [0.1, 1.0] (standard errors positive, bounded)
- No NaN values in theta estimates

*Data Quality:*
- All 100 participants present
- No duplicate UIDs  
- Theta distribution approximately normal (Shapiro-Wilk p > 0.01)
- <5 participants with |theta| > 2.5 (extreme scores)

*Log Validation:*
- Required pattern: "Theta extraction complete: 100 participants"  
- Required pattern: "Theta range check: within [-3, 3]"
- Forbidden patterns: "ERROR", "NaN detected", "out of range"

**Expected Behavior on Validation Failure:**
- Raise error with specific theta data issue
- Log failure to logs/step02_extract_theta.log
- QUIT immediately, invoke g_debug

### Step 3: Merge and Prepare Analysis Dataset
**Dependencies:** Steps 1-2 complete
**Complexity:** Medium (<10 minutes)

**Purpose:** Combine self-report measures and theta scores into analysis-ready dataset with complete cases

**Input:**
- data/step01_self_report_data.csv (self-report measures)
- data/step02_theta_scores.csv (theta scores)

**Processing:**
- Merge datasets on UID using inner join (complete cases only)
- Standardize predictors (z-scores): Education, Typical_Sleep, VR_Experience, Age
- Center continuous predictors around sample means for interpretation
- Create correlation matrix for initial multicollinearity screening
- Check final sample size (expect N >= 95 complete cases)
- Document excluded cases due to missing data
- Verify no perfect collinearities (r < 0.90 between predictors)

**Output:**
- data/step03_analysis_dataset.csv
- data/step03_correlation_matrix.csv

**Validation Requirement:**
Validation tools MUST be used after dataset preparation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_analysis_dataset.csv: >=95 rows x 6 columns
- Columns: UID (object), theta_all (float64), Education_z (float64), Typical_Sleep_z (float64), VR_Experience_z (float64), Age_z (float64)
- data/step03_correlation_matrix.csv: 5 rows x 5 columns (predictor correlations)

*Value Ranges:*
- theta_all in [-3, 3] (unchanged dependent variable)
- All _z variables in [-3, 3] (standardized predictors)
- Correlations in [-1, 1]
- No correlations >0.90 (multicollinearity check)

*Data Quality:*
- Complete cases N >= 95 (maximum 5% attrition)
- No missing values in any column
- Standardized predictors have mean ~0, sd ~1
- No perfect multicollinearity detected

*Log Validation:*
- Required pattern: "Dataset merge complete: N="
- Required pattern: "Standardization complete: all predictors centered"
- Required pattern: "Multicollinearity check: max r <0.90"
- Forbidden patterns: "ERROR", "perfect correlation", "missing data"

**Expected Behavior on Validation Failure:**
- Raise error with specific data preparation issue  
- Log failure to logs/step03_prepare_dataset.log
- QUIT immediately, invoke g_debug

### Step 4: Hierarchical Multiple Regression
**Dependencies:** Step 3 complete  
**Complexity:** Medium (~15 minutes including bootstrap)

**Purpose:** Fit hierarchical regression models to test self-report predictors while controlling for age

**Input:**
- data/step03_analysis_dataset.csv (prepared analysis dataset)

**Processing:**
- Model 1 (Control): theta_all ~ Age_z
- Model 2 (Full): theta_all ~ Age_z + Education_z + Typical_Sleep_z + VR_Experience_z
- Implementation: statsmodels.api.OLS with robust standard errors
- Extract model statistics: R², adjusted R², F-statistic, AIC/BIC
- Compute hierarchical F-test for R² change (Model 2 vs Model 1)
- Bootstrap 95% CIs for all coefficients:
  - Iterations: 1000
  - Random seed: 42 for reproducibility  
  - Method: Participant-level resampling with replacement
  - CI computation: percentile method (2.5th, 97.5th percentiles)
- Multiple comparison correction for 3 main predictors:
  - Family: Within-RQ (Education, Typical_Sleep, VR_Experience)
  - Bonferroni: alpha = 0.05/3 = 0.0167 per test
  - FDR: Benjamini-Hochberg adjustment
  - Report BOTH uncorrected AND corrected p-values (Decision D068)

**Output:**
- data/step04_regression_models.csv
- data/step04_coefficients_ci.csv

**Validation Requirement:**  
Validation tools MUST be used after regression execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_regression_models.csv: 2 rows x 8 columns
- Columns: model, R2, adj_R2, F_stat, F_p, AIC, BIC, N
- data/step04_coefficients_ci.csv: 5 rows x 8 columns  
- Columns: predictor, beta, se, ci_lower, ci_upper, p_uncorrected, p_bonferroni, p_fdr

*Value Ranges:*
- R² in [0, 1] for both models
- Model 2 R² >= Model 1 R² (hierarchical improvement)
- Beta coefficients in [-2, 2] (standardized predictors)
- Standard errors > 0
- p-values in [0, 1]
- CI bounds: ci_lower < beta < ci_upper for most coefficients

*Data Quality:*
- Model 1: 1 predictor (Age), Model 2: 4 predictors  
- Bootstrap CIs valid (non-degenerate intervals)
- Dual p-values present for main predictors (Decision D068)
- Finite parameter estimates (no convergence failures)

*Log Validation:*
- Required pattern: "Hierarchical regression complete"
- Required pattern: "Bootstrap CIs computed: 1000 iterations"  
- Required pattern: "Multiple comparisons: Bonferroni + FDR"
- Forbidden patterns: "ERROR", "convergence failed", "singular matrix"

**Expected Behavior on Validation Failure:**
- Raise error with specific regression failure
- Log failure to logs/step04_hierarchical_regression.log  
- QUIT immediately, invoke g_debug

### Step 5: Model Diagnostics and Assumptions
**Dependencies:** Step 4 complete
**Complexity:** Medium (~10 minutes)

**Purpose:** Evaluate regression assumptions and identify potential violations requiring remedial action

**Input:**
- data/step03_analysis_dataset.csv (analysis data)
- data/step04_regression_models.csv (fitted models)

**Processing:**  
- Extract residuals and fitted values from Model 2 (full model)
- Normality tests:
  - Shapiro-Wilk test on standardized residuals
  - Q-Q plot data generation for visual assessment
- Homoscedasticity tests:
  - Breusch-Pagan test for constant variance
  - Scale-location plot data generation
- Multicollinearity assessment:
  - Variance Inflation Factor (VIF) for each predictor
  - Condition indices for multicollinearity diagnosis
- Outlier detection:
  - Cook's Distance for each observation
  - Threshold: D > 4/N = 4/100 = 0.04
  - Leverage values and studentized residuals
- Remedial actions if assumptions violated:
  - Normality p < 0.05: Report bootstrap CIs as primary (already computed)
  - Heteroscedasticity p < 0.05: Apply HC3 robust standard errors
  - VIF > 5: Document multicollinearity, consider ridge if VIF > 10  
  - Outliers (Cook's D > 0.04): Report results with/without outliers

**Output:**
- data/step05_diagnostics_summary.csv
- data/step05_residuals_data.csv  
- data/step05_outlier_analysis.csv

**Validation Requirement:**
Validation tools MUST be used after diagnostics execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_diagnostics_summary.csv: 6 rows x 4 columns
- Columns: test, statistic, p_value, interpretation  
- data/step05_residuals_data.csv: N rows x 5 columns
- Columns: UID, residual, fitted, leverage, cooks_d
- data/step05_outlier_analysis.csv: variable rows x 3 columns
- Columns: UID, cooks_d, outlier_flag (if any outliers detected)

*Value Ranges:*
- Shapiro-Wilk p-value in [0, 1]
- Breusch-Pagan p-value in [0, 1]  
- VIF values >= 1.0 (theoretical minimum)
- Cook's Distance >= 0
- Leverage in [0, 1]
- Residuals approximately centered around 0

*Data Quality:*
- All diagnostic tests completed successfully
- VIF computed for all 4 predictors in Model 2
- Cook's D computed for all N observations
- Remedial actions documented if violations detected

*Log Validation:*
- Required pattern: "Assumption checks complete"
- Required pattern: "VIF check: max VIF ="  
- Required pattern: "Cook's D: max value ="
- Forbidden patterns: "ERROR", "test failed", "computation error"

**Expected Behavior on Validation Failure:**
- Raise error with specific diagnostic failure
- Log failure to logs/step05_model_diagnostics.log
- QUIT immediately, invoke g_debug

### Step 6: Effect Size Analysis
**Dependencies:** Step 4-5 complete
**Complexity:** Medium (~10 minutes)

**Purpose:** Compute comprehensive effect size measures and confidence intervals for model and predictors

**Input:**
- data/step04_regression_models.csv (model fit statistics)
- data/step04_coefficients_ci.csv (regression coefficients)
- data/step03_analysis_dataset.csv (for semi-partial correlations)

**Processing:**
- Model-level effect sizes:
  - Cohen's f² = R²/(1-R²) for Model 2  
  - f² categories: small (0.02), medium (0.15), large (0.35)
  - R² change effect size: f²change = ΔR²/(1-R²Model2)
- Predictor-level effect sizes:
  - Semi-partial correlations (sr²) for unique variance explained
  - Standardized beta coefficients (already computed)
  - Part correlations for relative importance
- Bootstrap confidence intervals for effect sizes:
  - Iterations: 1000
  - Random seed: 42 for consistency with Step 4
  - Method: Resample participants, recompute all effect sizes  
  - CI computation: percentile method (2.5th, 97.5th percentiles)
- Relative importance analysis:
  - Rank predictors by sr² magnitude
  - Compute percentage of explained variance per predictor

**Output:**
- data/step06_effect_sizes.csv
- data/step06_relative_importance.csv

**Validation Requirement:**
Validation tools MUST be used after effect size analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_effect_sizes.csv: 6 rows x 6 columns
- Columns: measure, value, ci_lower, ci_upper, interpretation, bootstrap_se  
- data/step06_relative_importance.csv: 4 rows x 4 columns
- Columns: predictor, sr2, rank, percent_of_r2

*Value Ranges:*
- R² and sr² values in [0, 1]
- Cohen's f² >= 0
- Beta coefficients in [-2, 2] (standardized)
- CI bounds: ci_lower < value < ci_upper
- Ranks: integers 1-4 (for 4 predictors)

*Data Quality:*  
- All effect sizes non-negative where expected
- Bootstrap CIs non-degenerate (width > 0)
- Relative importance sums approximately equal model R²
- Interpretation categories assigned correctly

*Log Validation:*
- Required pattern: "Effect size analysis complete"
- Required pattern: "Cohen's f² computed:"
- Required pattern: "Relative importance computed"  
- Forbidden patterns: "ERROR", "negative effect size", "invalid CI"

**Expected Behavior on Validation Failure:**
- Raise error with specific effect size computation failure
- Log failure to logs/step06_effect_sizes.log
- QUIT immediately, invoke g_debug

### Step 7: Cross-Validation Analysis  
**Dependencies:** Step 3-4 complete
**Complexity:** Medium (~15 minutes)

**Purpose:** Assess model generalizability and check for overfitting using k-fold cross-validation

**Input:**
- data/step03_analysis_dataset.csv (analysis dataset)

**Processing:**
- Implement 5-fold cross-validation using sklearn.model_selection.KFold
- Random seed: 42 for reproducibility
- Shuffle: True (randomize before splitting)  
- Stratification: None for regression (use quantile-based if outcome severely skewed)
- For each fold:
  - Fit Model 2 on training set (80% of data)
  - Predict on test set (20% of data)
  - Compute test R², RMSE, MAE
- Aggregation across folds:
  - Mean and standard deviation of test metrics
  - Training-test gap: difference in R² between training and test
  - Flag overfitting if train-test R² gap > 0.10
- Stability assessment:
  - Coefficient stability across folds (standard deviation of betas)
  - Predictor significance consistency (% of folds with p < 0.05)

**Output:**
- data/step07_cv_results.csv
- data/step07_cv_stability.csv

**Validation Requirement:**
Validation tools MUST be used after cross-validation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_cv_results.csv: 5 rows x 6 columns
- Columns: fold, train_r2, test_r2, rmse, mae, gap
- data/step07_cv_stability.csv: 4 rows x 4 columns  
- Columns: predictor, mean_beta, sd_beta, sig_consistency

*Value Ranges:*
- All R² values in [0, 1]
- RMSE and MAE > 0  
- Train-test gap in [-0.5, 0.5] (reasonable range)
- Beta standard deviations >= 0
- Significance consistency in [0, 1] (proportion)

*Data Quality:*
- All 5 folds completed successfully  
- Test metrics computed for each fold
- Mean values within expected ranges
- No degenerate folds (extremely high/low performance)

*Log Validation:*
- Required pattern: "5-fold cross-validation complete"
- Required pattern: "Mean test R² ="
- Required pattern: "Overfitting check: train-test gap ="
- Forbidden patterns: "ERROR", "fold failed", "convergence error"

**Expected Behavior on Validation Failure:**
- Raise error with specific cross-validation failure
- Log failure to logs/step07_cross_validation.log  
- QUIT immediately, invoke g_debug

### Step 8: Power Analysis and Sensitivity Testing
**Dependencies:** Steps 4-7 complete
**Complexity:** Medium (~10 minutes)

**Purpose:** Assess statistical power for detected effects and compute minimum detectable effect sizes

**Input:**
- data/step04_regression_models.csv (observed effect sizes)
- data/step03_analysis_dataset.csv (sample size)

**Processing:**
- Post-hoc power analysis for hierarchical regression:
  - Given: N=100 (observed), 4 predictors in full model
  - Alpha: 0.05 (family-wise for overall model test)
  - Corrected alpha: 0.0167 (Bonferroni for individual predictors)
  - Observed effect: R² from Model 2
  - Convert to Cohen's f² = R²/(1-R²)
  - Use: statsmodels.stats.power.FTestAnovaPower()
  - Compute: Achieved power for observed f²
- Sensitivity analysis:
  - Minimum detectable f² at 80% power given N=100, alpha=0.05
  - Minimum detectable f² at 80% power given N=100, alpha=0.0167 (corrected)
  - Express as minimum detectable R² for interpretation
- Individual predictor power:
  - Post-hoc power for each significant predictor
  - Based on observed t-statistics and corrected alpha levels
- Power interpretation:
  - Adequate: power >= 0.80
  - Marginal: 0.60 <= power < 0.80  
  - Inadequate: power < 0.60

**Output:**
- data/step08_power_analysis.csv
- data/step08_sensitivity_analysis.csv

**Validation Requirement:**
Validation tools MUST be used after power analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_power_analysis.csv: 6 rows x 5 columns
- Columns: test, observed_effect, alpha, power, interpretation
- data/step08_sensitivity_analysis.csv: 2 rows x 4 columns  
- Columns: alpha_level, min_f2, min_r2, min_effect_label

*Value Ranges:*
- Power values in [0, 1]
- Cohen's f² >= 0
- R² values in [0, 1]
- Alpha levels: 0.05 and 0.0167

*Data Quality:*
- Power computed for overall model and individual predictors
- Sensitivity analysis for both uncorrected and corrected alphas
- Effect size interpretations assigned appropriately  
- All computations finite (no NaN or infinite values)

*Log Validation:*
- Required pattern: "Power analysis complete"
- Required pattern: "Post-hoc power for observed effects"
- Required pattern: "Sensitivity analysis: minimum detectable effects"
- Forbidden patterns: "ERROR", "power calculation failed", "invalid effect size"

**Expected Behavior on Validation Failure:**
- Raise error with specific power analysis failure
- Log failure to logs/step08_power_analysis.log
- QUIT immediately, invoke g_debug

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (prerequisite checks)
- data/step01_self_report_data.csv (extracted self-report measures)
- data/step02_theta_scores.csv (mean theta_all per participant) 
- data/step03_analysis_dataset.csv (merged analysis-ready data)
- data/step03_correlation_matrix.csv (initial predictor correlations)
- data/step04_regression_models.csv (hierarchical model comparison)
- data/step04_coefficients_ci.csv (coefficients with bootstrap CIs and dual p-values)
- data/step05_diagnostics_summary.csv (assumption test results)
- data/step05_residuals_data.csv (residual analysis data)
- data/step05_outlier_analysis.csv (outlier detection results)  
- data/step06_effect_sizes.csv (comprehensive effect size analysis)
- data/step06_relative_importance.csv (predictor importance rankings)
- data/step07_cv_results.csv (5-fold cross-validation results)
- data/step07_cv_stability.csv (coefficient stability across folds)
- data/step08_power_analysis.csv (post-hoc power for observed effects)
- data/step08_sensitivity_analysis.csv (minimum detectable effect sizes)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_self_report.log  
- logs/step02_extract_theta.log
- logs/step03_prepare_dataset.log
- logs/step04_hierarchical_regression.log
- logs/step05_model_diagnostics.log
- logs/step06_effect_sizes.log
- logs/step07_cross_validation.log
- logs/step08_power_analysis.log

### Plots (EMPTY until rq_plots runs)  
- Plot source CSVs created in data/ for downstream visualization:
  - data/step05_*_plot_data.csv (diagnostic plots)
  - data/step06_*_plot_data.csv (effect size visualization)

### Results (EMPTY until rq_results runs)
- summary.md will be created by rq_results summarizing key findings

---

## Expected Data Formats

### Step-to-Step Transformations
1. Raw extraction: master.xlsx -> standardized CSV with proper data types
2. Theta integration: Ch5 scores merged on UID for complete cases
3. Standardization: Predictors z-scored for interpretation and multicollinearity assessment
4. Model fitting: Hierarchical approach with bootstrap CIs and dual p-values
5. Diagnostics: Comprehensive assumption checking with remedial actions
6. Effect sizes: Multiple metrics with confidence intervals for interpretation
7. Validation: Cross-validation for generalizability assessment  
8. Power: Post-hoc analysis and sensitivity testing for adequacy

### Column Naming Conventions  
- UID: Participant identifier (consistent across all files)
- *_z: Standardized predictor variables (mean=0, sd=1)
- theta_all: Dependent variable from Ch5 (unstandardized)
- p_uncorrected: Raw p-values before correction
- p_bonferroni: Bonferroni-corrected p-values  
- p_fdr: FDR-corrected p-values
- ci_lower, ci_upper: Bootstrap confidence interval bounds
- cooks_d: Cook's Distance for outlier detection

### Data Type Constraints
- UID: object (string identifier), non-nullable
- Continuous measures: float64, nullable only in extraction phase
- Effect sizes: float64, non-negative where appropriate (R², f²)
- p-values: float64, range [0, 1], non-nullable
- Flags and interpretations: object (categorical), non-nullable

---

## Cross-RQ Dependencies

**Dependencies:**
- Ch5 5.1.1 (Functional Form Comparison) must complete successfully
- Required output: theta_all scores for all 100 participants
- Status verification: results/ch5/5.1.1/status.yaml shows rq_results: success

**Fallback Strategies:**
- Multiple file patterns for theta scores (step03, final, summary variations)
- Alternative master.xlsx locations (local cache vs project data)
- Graceful degradation: proceed with available complete cases if N >= 95

**Critical Dependencies:**
- If Ch5 incomplete: QUIT with "Ch5 5.1.1 required for DERIVED data"
- If master.xlsx missing: QUIT with "Self-report measures not accessible"
- If sample size <95: QUIT with "Insufficient complete cases for analysis"

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
[Full 4-layer validation structure as specified above]

#### Step 1: Extract Self-Report Measures
[Full 4-layer validation structure as specified above]

#### Step 2: Extract Theta Scores 
[Full 4-layer validation structure as specified above]

#### Step 3: Merge and Prepare Dataset
[Full 4-layer validation structure as specified above]

#### Step 4: Hierarchical Regression
[Full 4-layer validation structure as specified above]

#### Step 5: Model Diagnostics
[Full 4-layer validation structure as specified above]

#### Step 6: Effect Size Analysis
[Full 4-layer validation structure as specified above]

#### Step 7: Cross-Validation
[Full 4-layer validation structure as specified above]

#### Step 8: Power Analysis  
[Full 4-layer validation structure as specified above]

---

## Summary

**Total Steps:** 9 (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** 45-60 minutes
**Cross-RQ Dependencies:** Ch5 5.1.1 (theta_all scores) + master.xlsx (self-report measures)
**Primary Outputs:** Hierarchical regression results with bootstrap CIs, dual p-values, comprehensive diagnostics, cross-validation, and power analysis
**Validation Coverage:** 100% (all 9 steps have 4-layer validation requirements)

**Key Hypothesis:** Education level will significantly predict REMEMVR performance through cognitive reserve mechanisms, with effect size in medium range (f² ~ 0.15)

**Critical Methodological Notes:**
- Decision D068 compliance: ALL predictors report uncorrected AND corrected p-values
- Bootstrap CIs (1000 iterations, seed=42) for robust estimation
- Bonferroni correction for 3 main predictors (alpha=0.0167) plus FDR alternative
- Cross-validation with overfitting detection (train-test gap >0.10)
- Comprehensive assumption checking with specified remedial actions
- Post-hoc power analysis acknowledging potential underpowering for small effects

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml  
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent with v5.1 enhanced statistical specifications