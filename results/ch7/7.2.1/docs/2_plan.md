# Analysis Plan: RQ 7.2.1 - Age Moderation of Test-VR Relationship

**Research Question:** 7.2.1
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ tests the VR scaffolding hypothesis using hierarchical regression to examine whether age effects on REMEMVR performance are mediated by cognitive tests (RAVLT, BVMT, RPM). If VR provides environmental scaffolding, age should not predict REMEMVR after controlling for cognitive ability.

**Pipeline:** Hierarchical Multiple Regression with Cross-Validation
**Steps:** 11 total analysis steps (Step 0: dependency validation + Steps 1-10: analysis)
**Estimated Runtime:** 45-60 minutes total

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni corrected)
- Ch7 alpha correction: 0.05/28 = 0.00179 for chapter-level family
- Within-RQ Bonferroni: alpha = 0.05/4 = 0.0125 for 4 predictors

**Key Methodological Enhancements:**
- Formal mediation analysis with proportion mediated calculation
- Participant-level bootstrap (1000 iterations, seed=42) for all CIs
- 5-fold cross-validation with overfitting detection
- Comprehensive assumption checking with remedial actions
- Post-hoc power analysis for mediation effects

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 outputs exist before proceeding with analysis

**Input:**
- Primary: results/ch5/5.1.1/status.yaml (verify rq_results = success)
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/*theta*.csv
- Fallback: results/ch5/5.1.1/data/step*theta*.csv
- Expected content: theta_all scores (IRT ability estimates) for 100 participants
- Local: data/cache/master.xlsx (cognitive test scores)

**Processing:**
- Check Ch5 5.1.1 status.yaml shows rq_results: success
- Locate theta scores file using pattern matching
- Verify file contains UID and theta_all columns
- Check master.xlsx accessibility for cognitive tests
- Verify N=100 participants with complete data
- Log all validation checks with success/failure status

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Expected format: tab-delimited with columns: check_name, status, details

*Value Ranges:*
- status values: "PASS" or "FAIL" only
- N participants: exactly 100
- theta values: range [-4, 4] (IRT scale)

*Data Quality:*
- All dependency checks documented
- Clear PASS/FAIL status for each check
- No ambiguous validation results

*Log Validation:*
- Required: "Dependency validation complete"
- Required: "Ch5 5.1.1 outputs verified"
- Required: "master.xlsx accessible"
- Forbidden: "ERROR", "not found", "missing"

**Expected Behavior on Validation Failure:**
Log specific missing dependency, quit with clear error message, invoke g_debug for troubleshooting.

### Step 1: Extract Theta Scores from Ch5 Results
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (<5 minutes)

**Purpose:** Extract theta_all scores from Ch5 5.1.1 IRT calibration results

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/*theta*.csv
- Expected columns: UID, theta_all, SE_theta
- Expected N: 100 participants

**Processing:**
- Load theta scores using pandas.read_csv()
- Filter to theta_all column only (omnibus scores across all memory domains)
- Verify 100 unique participants present
- Check for missing values (expect none from Ch5 calibration)
- Convert UID to string for merging consistency
- Sort by UID for reproducible ordering
- Log extraction summary (N participants, theta range, missing data)

**Output:**
- data/step01_theta_scores.csv

**Validation Requirement:**
Validation tools MUST be used after theta extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_theta_scores.csv: 100 rows x 2 columns
- Columns: UID (object), theta_all (float64)

*Value Ranges:*
- theta_all in [-4, 4] (IRT ability scale bounds)
- No NaN values allowed (complete IRT calibration)
- UID values: 100 unique string identifiers

*Data Quality:*
- Exactly 100 participants
- No duplicate UIDs
- All theta values finite (no inf, -inf)
- theta standard deviation > 0.5 (adequate individual differences)

*Log Validation:*
- Required: "Theta extraction complete: 100 participants"
- Required: "theta_all range: [-X.X, X.X]"
- Forbidden: "ERROR", "missing", "NaN detected"

**Expected Behavior on Validation Failure:**
Log data quality issue, check Ch5 calibration status, quit if fundamental data problem.

### Step 2: Extract Cognitive Test Scores
**Dependencies:** Step 1 (theta scores available)
**Complexity:** Low (<5 minutes)

**Purpose:** Extract cognitive test T-scores and age from master.xlsx

**Input:**
- data/cache/master.xlsx (participant demographics and test scores)
- Required columns: UID, Age, RAVLT_T, BVMT_T, RPM_T

**Processing:**
- Load master.xlsx using pandas.read_excel()
- Extract UID, Age, RAVLT_T, BVMT_T, RPM_T columns
- Convert UID to string for merge consistency
- Check for missing values in cognitive tests (flag if >5%)
- Verify age range reasonable (expect 18-80 years)
- Verify T-scores in expected range (20-80 for standardized tests)
- Filter to N=100 participants matching theta data
- Sort by UID for consistent ordering

**Output:**
- data/step02_cognitive_tests.csv

**Validation Requirement:**
Validation tools MUST be used after cognitive test extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_cognitive_tests.csv: 100 rows x 5 columns
- Columns: UID (object), Age (float64), RAVLT_T (float64), BVMT_T (float64), RPM_T (float64)

*Value Ranges:*
- Age in [18, 80] (reasonable participant age range)
- RAVLT_T in [20, 80] (standardized T-score range)
- BVMT_T in [20, 80] (standardized T-score range)
- RPM_T in [20, 80] (standardized T-score range)

*Data Quality:*
- Exactly 100 participants
- Missing data <5% per cognitive test
- Age standard deviation >10 (adequate age range)
- Test score standard deviations >8 (adequate individual differences)

*Log Validation:*
- Required: "Cognitive extraction complete: 100 participants"
- Required: "Age range: [XX-XX years]"
- Required: "Missing data check: <5% threshold"
- Forbidden: "ERROR", "missing file", "insufficient range"

**Expected Behavior on Validation Failure:**
Log missing data patterns, check if sufficient for analysis, proceed if <5% missing per variable.

### Step 3: Merge Analysis Dataset
**Dependencies:** Steps 1-2 (theta scores + cognitive tests)
**Complexity:** Low (<5 minutes)

**Purpose:** Combine theta scores with cognitive tests and age into single analysis dataset

**Input:**
- data/step01_theta_scores.csv (theta_all scores)
- data/step02_cognitive_tests.csv (cognitive tests + age)

**Processing:**
- Merge datasets on UID using pandas.merge(how='inner')
- Verify N=100 participants in merged dataset
- Check no participants lost in merge (expect 100% match)
- Compute descriptive statistics for all variables
- Check for outliers using interquartile range (IQR) method
- Flag extreme outliers beyond 3*IQR but retain for analysis
- Create analysis-ready dataset with standardized variable names
- Log merge summary and descriptive statistics

**Output:**
- data/step03_analysis_dataset.csv
- data/step03_descriptive_stats.csv

**Validation Requirement:**
Validation tools MUST be used after dataset merge execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_analysis_dataset.csv: 100 rows x 6 columns
- Columns: UID (object), theta_all (float64), Age (float64), RAVLT_T (float64), BVMT_T (float64), RPM_T (float64)
- data/step03_descriptive_stats.csv: 5 rows x 8 columns (mean, sd, min, max, Q1, median, Q3, n_valid)

*Value Ranges:*
- All previous range constraints maintained
- Descriptive statistics: means within expected ranges
- Standard deviations: adequate variability (>0.5 for theta, >8 for tests, >10 for age)

*Data Quality:*
- No participants lost in merge (100% match rate)
- No duplicate UIDs in final dataset
- All variables have complete data (0% missing after merge)
- Outliers flagged but retained

*Log Validation:*
- Required: "Merge complete: 100 participants retained"
- Required: "Descriptive statistics computed"
- Required: "Outlier check: X extreme values flagged"
- Forbidden: "ERROR", "merge failure", "participants lost"

**Expected Behavior on Validation Failure:**
Check merge keys, verify no systematic missingness, quit if participants lost unexpectedly.

### Step 4: Compute Bivariate Correlations
**Dependencies:** Step 3 (merged analysis dataset)
**Complexity:** Medium (~10 minutes)

**Purpose:** Compute correlation matrix to examine bivariate relationships before hierarchical regression

**Input:**
- data/step03_analysis_dataset.csv

**Processing:**
- Compute Pearson correlations between all variables
- Primary focus: r(Age, theta_all) - expect small negative correlation (r < -0.15)
- Secondary: r(Age, RAVLT_T), r(Age, BVMT_T), r(Age, RPM_T) - expect negative
- Tertiary: r(cognitive tests, theta_all) - expect positive correlations
- Use scipy.stats.pearsonr for p-values and confidence intervals
- Apply within-RQ Bonferroni correction: alpha = 0.05/10 = 0.005 for correlation matrix
- Bootstrap 95% CIs for all correlations:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - CI: Percentile method (2.5th, 97.5th percentiles)
- Format correlation matrix with dual p-values (Decision D068)

**Output:**
- data/step04_correlation_matrix.csv
- data/step04_correlation_bootstrap_cis.csv

**Validation Requirement:**
Validation tools MUST be used after correlation analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_correlation_matrix.csv: 5 rows x 5 columns (correlation matrix)
- data/step04_correlation_bootstrap_cis.csv: 10 rows x 6 columns (var1, var2, r, ci_lower, ci_upper, p_uncorrected, p_bonferroni)

*Value Ranges:*
- Correlations in [-1, 1] (valid correlation bounds)
- p_uncorrected in [0, 1] (valid probability range)
- p_bonferroni <= 1 (corrected p-values)
- Bootstrap CIs: ci_lower < r < ci_upper for each correlation

*Data Quality:*
- All 10 unique correlations computed (5x5 matrix, exclude diagonal)
- No NaN correlations (complete data assumed)
- Bootstrap CIs cover true correlation in >95% of cases
- Expected pattern: r(Age, theta_all) negative, r(tests, theta_all) positive

*Log Validation:*
- Required: "Correlation matrix complete: 10 correlations"
- Required: "Bootstrap CIs computed: 1000 iterations"
- Required: "Primary correlation r(Age, theta_all) = -X.XX"
- Forbidden: "ERROR", "NaN correlation", "bootstrap failed"

**Expected Behavior on Validation Failure:**
Check for perfect correlations (multicollinearity), verify bootstrap convergence, proceed if correlations reasonable.

### Step 5: Hierarchical Regression Models
**Dependencies:** Step 4 (correlations computed)
**Complexity:** Medium (~10 minutes)

**Purpose:** Fit hierarchical regression to test age mediation by cognitive tests

**Input:**
- data/step03_analysis_dataset.csv

**Processing:**
- Standardize all continuous predictors (Age, RAVLT_T, BVMT_T, RPM_T) using z-scores
- Model 1: theta_all ~ Age (bivariate age effect)
- Model 2: theta_all ~ Age + RAVLT_T + BVMT_T + RPM_T (controlled age effect)
- Implementation: statsmodels.api.OLS with standardized predictors
- Extract for each model: R², adjusted R², F-statistic, AIC, BIC
- Extract coefficients with standard errors and t-statistics
- Test model improvement: F-test for R² increase from Model 1 to Model 2
- Dual p-value reporting (Decision D068):
  - Uncorrected p-values for individual coefficients
  - Bonferroni correction within-RQ: alpha = 0.05/4 = 0.0125 for 4 predictors
- Bootstrap 95% CIs for all coefficients:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - CI: Percentile method (2.5th, 97.5th percentiles)

**Output:**
- data/step05_hierarchical_models.csv
- data/step05_model_comparison.csv
- data/step05_coefficient_bootstrap_cis.csv

**Validation Requirement:**
Validation tools MUST be used after hierarchical regression execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_hierarchical_models.csv: 2 rows x 8 columns (model, R2, adj_R2, F_stat, p_value, AIC, BIC, df_resid)
- data/step05_model_comparison.csv: 1 row x 4 columns (F_change, p_change, R2_change, df_change)
- data/step05_coefficient_bootstrap_cis.csv: 5 rows x 8 columns (model, variable, beta, se, t_stat, p_uncorrected, p_bonferroni, ci_lower, ci_upper)

*Value Ranges:*
- R² in [0, 1] (valid proportion variance explained)
- F_stat > 0 (positive F-statistic for significant models)
- p_values in [0, 1] (valid probability range)
- Standardized beta in [-3, 3] (reasonable range for standardized coefficients)
- Bootstrap CIs: ci_lower < beta < ci_upper

*Data Quality:*
- Model 1: 1 predictor (Age), df_resid = 98
- Model 2: 4 predictors (Age + 3 tests), df_resid = 95
- No convergence failures (successful model fits)
- Expected pattern: Age beta decreases from Model 1 to Model 2 (mediation hypothesis)

*Log Validation:*
- Required: "Hierarchical regression complete: 2 models fitted"
- Required: "Model 1 R² = X.XX, Model 2 R² = X.XX"
- Required: "Age coefficient: Model 1 = X.XX, Model 2 = X.XX"
- Required: "Bootstrap CIs: 1000 iterations completed"
- Forbidden: "ERROR", "convergence failed", "singular matrix"

**Expected Behavior on Validation Failure:**
Check for multicollinearity, verify model specification, examine bootstrap convergence.

### Step 6: Formal Mediation Analysis
**Dependencies:** Step 5 (hierarchical models fitted)
**Complexity:** Medium (~10 minutes)

**Purpose:** Compute formal mediation statistics beyond hierarchical regression framework

**Input:**
- data/step05_coefficient_bootstrap_cis.csv (model coefficients)
- data/step03_analysis_dataset.csv (raw data for mediation paths)

**Processing:**
- Extract key coefficients from hierarchical regression:
  - c: Total effect of Age on theta_all (Model 1)
  - c': Direct effect of Age on theta_all controlling for tests (Model 2)
- Compute proportion mediated: (c - c') / c
- Fit auxiliary regressions for indirect paths:
  - Path a: Age -> RAVLT_T, Age -> BVMT_T, Age -> RPM_T
  - Path b: RAVLT_T -> theta_all, BVMT_T -> theta_all, RPM_T -> theta_all (from Model 2)
- Compute indirect effects: a × b for each cognitive test
- Total indirect effect: sum of individual indirect effects
- Bootstrap mediation analysis:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - Compute bias-corrected 95% CI for indirect effect
  - Test significance: CI excludes zero indicates significant mediation
- Sobel test for indirect effect (supplementary to bootstrap)
- Effect size: proportion of total effect mediated

**Output:**
- data/step06_mediation_paths.csv
- data/step06_mediation_effects.csv
- data/step06_mediation_bootstrap.csv

**Validation Requirement:**
Validation tools MUST be used after mediation analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_mediation_paths.csv: 6 rows x 5 columns (path_name, a_coefficient, b_coefficient, indirect_effect, se)
- data/step06_mediation_effects.csv: 1 row x 8 columns (total_effect, direct_effect, total_indirect, proportion_mediated, sobel_z, sobel_p, ci_lower, ci_upper)
- data/step06_mediation_bootstrap.csv: 1000 rows x 4 columns (iteration, total_indirect, proportion_mediated, direct_effect)

*Value Ranges:*
- Proportion mediated in [0, 2] (can exceed 1 for complete mediation with suppression)
- Indirect effects in [-2, 2] (reasonable range for standardized effects)
- Sobel z-statistic: any real number
- Bootstrap CI: ci_lower < total_indirect < ci_upper

*Data Quality:*
- All 3 cognitive tests have computed indirect effects
- Bootstrap converged (1000 successful iterations)
- Proportion mediated interpretable (negative indicates suppression)
- No computational failures in path analysis

*Log Validation:*
- Required: "Mediation analysis complete: 3 indirect paths"
- Required: "Proportion mediated = X.XX"
- Required: "Bootstrap CI for indirect effect: [X.XX, X.XX]"
- Required: "Sobel test: z = X.XX, p = X.XX"
- Forbidden: "ERROR", "convergence failed", "undefined proportion"

**Expected Behavior on Validation Failure:**
Check path coefficients for reasonableness, verify bootstrap stability, examine for suppression effects.

### Step 7: Model Diagnostics and Assumptions
**Dependencies:** Step 5 (hierarchical models fitted)
**Complexity:** Medium (~15 minutes)

**Purpose:** Comprehensive assumption checking for hierarchical regression models

**Input:**
- data/step03_analysis_dataset.csv (original data)
- Model objects from Step 5 (for residual extraction)

**Processing:**
- Extract residuals and fitted values from Model 2 (full model)
- Multicollinearity check:
  - Compute VIF for each predictor using statsmodels
  - Threshold: VIF < 5 acceptable, VIF 5-10 caution, VIF > 10 problematic
  - Action if VIF > 10: Consider ridge regression or drop predictors
- Normality of residuals:
  - Shapiro-Wilk test: scipy.stats.shapiro
  - Threshold: p > 0.05 for normality
  - Supplementary: Q-Q plot data points for visualization
  - Action if p < 0.05: Use bootstrap CIs as primary inference
- Homoscedasticity:
  - Breusch-Pagan test: statsmodels.stats.diagnostic.het_breuschpagan
  - Threshold: p > 0.05 for homoscedasticity
  - Action if p < 0.05: Report HC3 robust standard errors
- Influential observations:
  - Cook's Distance: statsmodels.influence.OLSInfluence
  - Threshold: Cook's D > 4/n = 0.04 for influential points
  - Action if exceeded: Report results with and without outliers
- Linearity:
  - Residual plots: residuals vs fitted, residuals vs each predictor
  - Action if non-linear: Consider polynomial terms or transformations

**Remedial Actions Implementation:**
- Normality violation: Re-run bootstrap with 2000 iterations for robust CIs
- Heteroscedasticity: Compute HC3 robust standard errors using statsmodels
- High VIF (>10): Fit ridge regression as sensitivity analysis
- Outliers: Re-fit models excluding Cook's D > 0.04 observations

**Output:**
- data/step07_assumption_tests.csv
- data/step07_vif_results.csv
- data/step07_diagnostic_data.csv (residuals, fitted values, Cook's D)
- data/step07_robust_results.csv (if heteroscedasticity detected)

**Validation Requirement:**
Validation tools MUST be used after diagnostic analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_assumption_tests.csv: 3 rows x 3 columns (test_name, statistic, p_value)
- data/step07_vif_results.csv: 4 rows x 2 columns (variable, VIF)
- data/step07_diagnostic_data.csv: 100 rows x 5 columns (UID, residual, fitted, cooks_d, standardized_residual)
- data/step07_robust_results.csv: conditional file (only if heteroscedasticity p < 0.05)

*Value Ranges:*
- VIF values: typically [1, 10], flag if any >5
- p_values in [0, 1] (Shapiro-Wilk, Breusch-Pagan)
- Cook's D: typically [0, 0.2], flag if any >0.04
- Standardized residuals: typically [-3, 3], flag if any >±3

*Data Quality:*
- All assumption tests completed (no failed computations)
- VIF computed for all 4 predictors
- Cook's D computed for all 100 observations
- Robust results generated only if heteroscedasticity detected

*Log Validation:*
- Required: "Assumption checking complete"
- Required: "VIF max = X.XX (threshold: 5.0)"
- Required: "Normality: Shapiro-Wilk p = X.XX"
- Required: "Homoscedasticity: Breusch-Pagan p = X.XX"
- Required: "Outliers: X observations with Cook's D > 0.04"
- Forbidden: "ERROR", "computation failed", "undefined VIF"

**Expected Behavior on Validation Failure:**
Document assumption violations, implement appropriate remedial actions, proceed with adjusted inference.

### Step 8: Cross-Validation Analysis
**Dependencies:** Step 5 (hierarchical models fitted)
**Complexity:** Medium (~10 minutes)

**Purpose:** Assess model generalizability and detect overfitting using cross-validation

**Input:**
- data/step03_analysis_dataset.csv

**Processing:**
- Implement 5-fold cross-validation using sklearn.model_selection.KFold:
  - Random seed: 42 for reproducibility
  - Shuffle: True (randomize before splitting)
  - Stratification: None for regression (quantile-based if outcome skewed)
- For each fold:
  - Split: 80% training, 20% test (20 participants per test fold)
  - Fit both Model 1 and Model 2 on training data
  - Predict on test set, compute R² and RMSE
  - Store fold-specific results
- Aggregate across folds:
  - Mean and standard deviation of test R² for both models
  - Mean and standard deviation of RMSE for both models
  - Training vs test R² gap (overfitting indicator)
- Overfitting assessment:
  - Gap threshold: train-test R² difference should be < 0.10
  - If gap > 0.10: flag potential overfitting
- Model stability:
  - CV standard deviation should be < 0.05 for stable models
  - Large SD indicates model instability across folds

**Output:**
- data/step08_cv_fold_results.csv
- data/step08_cv_summary.csv

**Validation Requirement:**
Validation tools MUST be used after cross-validation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_cv_fold_results.csv: 10 rows x 6 columns (fold, model, train_r2, test_r2, rmse, mae)
- data/step08_cv_summary.csv: 2 rows x 8 columns (model, mean_train_r2, sd_train_r2, mean_test_r2, sd_test_r2, mean_rmse, sd_rmse, overfitting_gap)

*Value Ranges:*
- R² values in [0, 1] (valid proportion variance)
- RMSE > 0 (positive root mean squared error)
- Overfitting gap in [0, 0.5] (reasonable train-test difference)
- Standard deviations: typically [0, 0.1] for stable models

*Data Quality:*
- All 5 folds completed successfully (10 total model fits: 2 models × 5 folds)
- No failed convergence across folds
- Test sets are non-overlapping (proper CV implementation)
- Mean test R² less than full-sample R² (expected for honest CV)

*Log Validation:*
- Required: "Cross-validation complete: 5 folds"
- Required: "Model 1 mean test R² = X.XX ± X.XX"
- Required: "Model 2 mean test R² = X.XX ± X.XX"
- Required: "Overfitting gap: X.XX (threshold: 0.10)"
- Forbidden: "ERROR", "fold failed", "convergence error"

**Expected Behavior on Validation Failure:**
Check fold balance, verify no data leakage, examine convergence across folds.

### Step 9: Effect Size Analysis
**Dependencies:** Steps 5-6 (regression + mediation results)
**Complexity:** Medium (~10 minutes)

**Purpose:** Compute comprehensive effect sizes for regression and mediation effects

**Input:**
- data/step05_hierarchical_models.csv
- data/step06_mediation_effects.csv
- data/step03_analysis_dataset.csv

**Processing:**
- Cohen's f² for hierarchical regression:
  - f² = R²/(1-R²) for each model
  - f²change = (R²2 - R²1)/(1-R²2) for model improvement
  - Interpretation: 0.02 small, 0.15 medium, 0.35 large
- Semi-partial correlations (sr²):
  - Unique variance explained by each predictor
  - sr² = (R²full - R²reduced) for each predictor
  - Sum of sr² values should approximate R²full
- Standardized effect sizes:
  - Standardized beta coefficients (already computed in Step 5)
  - Interpretation: 0.1 small, 0.3 medium, 0.5 large for standardized betas
- Mediation effect sizes:
  - Proportion mediated: (total - direct) / total
  - Kappa-squared (κ²): standardized indirect effect
  - Bootstrap 95% CIs for all effect sizes:
    - Iterations: 1000
    - Random seed: 42 for reproducibility
    - Method: Participant-level resampling with replacement
- Effect size benchmarking:
  - Compare against Cohen's conventions
  - Context-specific interpretation for memory research

**Output:**
- data/step09_effect_sizes.csv
- data/step09_effect_size_bootstrap.csv
- data/step09_effect_size_interpretation.csv

**Validation Requirement:**
Validation tools MUST be used after effect size analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step09_effect_sizes.csv: 6 rows x 5 columns (effect_type, variable, effect_size, ci_lower, ci_upper)
- data/step09_effect_size_bootstrap.csv: 1000 rows x 6 columns (iteration, f2_change, sr2_age, sr2_ravlt, sr2_bvmt, sr2_rpm)
- data/step09_effect_size_interpretation.csv: 6 rows x 4 columns (effect_type, variable, magnitude, interpretation)

*Value Ranges:*
- Cohen's f² in [0, 5] (typical range, can be higher for strong effects)
- Semi-partial r² in [0, 1] (proportion variance)
- Proportion mediated in [-1, 2] (can be negative for suppression, >1 for complete mediation)
- Kappa-squared in [0, 1] (standardized indirect effect)

*Data Quality:*
- All effect sizes finite (no NaN or infinite values)
- Bootstrap CIs computed for all effect sizes
- Semi-partial r² sum approximately equals full model R²
- Effect size interpretations follow standard conventions

*Log Validation:*
- Required: "Effect size analysis complete"
- Required: "Cohen's f² for model improvement = X.XX"
- Required: "Proportion mediated = X.XX (interpretation: XXX)"
- Required: "Bootstrap CIs computed: 1000 iterations"
- Forbidden: "ERROR", "NaN effect size", "bootstrap failed"

**Expected Behavior on Validation Failure:**
Check effect size calculations, verify bootstrap convergence, examine for computational issues.

### Step 10: Power Analysis
**Dependencies:** Step 9 (effect sizes computed)
**Complexity:** Medium (~10 minutes)

**Purpose:** Compute post-hoc power analysis for regression and mediation effects

**Input:**
- data/step09_effect_sizes.csv (observed effect sizes)
- Analysis parameters: N=100, 4 predictors, alpha levels

**Processing:**
- Post-hoc power for hierarchical regression:
  - Use statsmodels.stats.power.FTestAnovaPower()
  - Given: N=100, numerator df=3 (added predictors), denominator df=95
  - Alpha levels: 0.05 (uncorrected), 0.0125 (within-RQ Bonferroni), 0.00179 (chapter-level)
  - Compute power for observed f²change from Step 9
  - Interpretation: power ≥0.80 considered adequate
- Power for individual predictors:
  - Use statsmodels.stats.power.ttest_power() adapted for t-tests
  - Convert standardized betas to Cohen's d equivalent
  - Compute power for each predictor at different alpha levels
- Sensitivity analysis:
  - Minimum detectable effect size (f²) at 80% power
  - Required sample size for 80% power given observed effects
- Mediation power assessment:
  - Literature-based: Fritz & MacKinnon (2007) suggest N≥200 for small indirect effects
  - Monte Carlo simulation:
    - Iterations: 1000
    - Random seed: 42
    - Simulate data with observed effect structure
    - Compute power to detect significant indirect effect
- Power limitations acknowledgment:
  - N=100 may be limited for small mediation effects
  - Interpretation should consider power constraints

**Output:**
- data/step10_power_analysis.csv
- data/step10_sensitivity_analysis.csv
- data/step10_mediation_power.csv

**Validation Requirement:**
Validation tools MUST be used after power analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step10_power_analysis.csv: 4 rows x 6 columns (effect_type, variable, effect_size, alpha, power, adequate_power)
- data/step10_sensitivity_analysis.csv: 3 rows x 4 columns (alpha_level, min_detectable_f2, required_n_80power, interpretation)
- data/step10_mediation_power.csv: 1 row x 5 columns (observed_indirect, literature_n_required, monte_carlo_power, power_adequate, limitations)

*Value Ranges:*
- Power values in [0, 1] (valid probability range)
- Minimum detectable f² > 0 (positive effect sizes)
- Required N > current N (typically 100-500 for adequate power)
- Monte Carlo power in [0, 1] (simulated power estimate)

*Data Quality:*
- All power calculations completed successfully
- Sensitivity analysis provides interpretable benchmarks
- Mediation power assessment addresses literature recommendations
- Power limitations documented appropriately

*Log Validation:*
- Required: "Power analysis complete"
- Required: "Hierarchical regression power = X.XX at alpha = 0.00179"
- Required: "Minimum detectable f² = X.XX at 80% power"
- Required: "Mediation power assessment: N=100 vs recommended N≥200"
- Forbidden: "ERROR", "power calculation failed", "undefined power"

**Expected Behavior on Validation Failure:**
Check power calculation inputs, verify effect size values, examine simulation convergence for mediation power.

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (dependency check results)
- data/step01_theta_scores.csv (extracted theta_all scores)
- data/step02_cognitive_tests.csv (extracted cognitive tests + age)
- data/step03_analysis_dataset.csv (merged analysis dataset)
- data/step03_descriptive_stats.csv (descriptive statistics)
- data/step04_correlation_matrix.csv (bivariate correlations)
- data/step04_correlation_bootstrap_cis.csv (bootstrap CIs for correlations)
- data/step05_hierarchical_models.csv (Model 1 and Model 2 results)
- data/step05_model_comparison.csv (hierarchical F-test results)
- data/step05_coefficient_bootstrap_cis.csv (bootstrap CIs for coefficients)
- data/step06_mediation_paths.csv (mediation pathway results)
- data/step06_mediation_effects.csv (formal mediation analysis)
- data/step06_mediation_bootstrap.csv (bootstrap distribution for indirect effects)
- data/step07_assumption_tests.csv (normality, homoscedasticity tests)
- data/step07_vif_results.csv (multicollinearity diagnostics)
- data/step07_diagnostic_data.csv (residuals, Cook's D)
- data/step07_robust_results.csv (robust SEs if needed)
- data/step08_cv_fold_results.csv (cross-validation fold results)
- data/step08_cv_summary.csv (cross-validation summary)
- data/step09_effect_sizes.csv (comprehensive effect sizes)
- data/step09_effect_size_bootstrap.csv (bootstrap distribution for effect sizes)
- data/step09_effect_size_interpretation.csv (effect size interpretations)
- data/step10_power_analysis.csv (post-hoc power analysis)
- data/step10_sensitivity_analysis.csv (minimum detectable effects)
- data/step10_mediation_power.csv (mediation-specific power analysis)

### Logs (ONLY execution logs)
- logs/step00_dependency_validation.log
- logs/step01_extract_theta_scores.log
- logs/step02_extract_cognitive_tests.log
- logs/step03_merge_dataset.log
- logs/step04_bivariate_correlations.log
- logs/step05_hierarchical_regression.log
- logs/step06_mediation_analysis.log
- logs/step07_model_diagnostics.log
- logs/step08_cross_validation.log
- logs/step09_effect_sizes.log
- logs/step10_power_analysis.log

### Plots (EMPTY until rq_plots runs)
Plot source CSVs will be created in data/ folder:
- data/step04_correlation_plot_data.csv (for correlation matrix heatmap)
- data/step07_diagnostic_plot_data.csv (for Q-Q plots, residual plots)
- data/step05_mediation_plot_data.csv (for mediation pathway diagram)

### Results (EMPTY until rq_results runs)
summary.md will be created by rq_results based on all data outputs

---

## Expected Data Formats

### Step-to-Step Transformations
1. **Ch5 theta extraction** → standardized UID format for merging
2. **Cognitive test extraction** → T-scored variables on common scale
3. **Dataset merge** → complete cases analysis (N=100)
4. **Variable standardization** → z-scored predictors for regression
5. **Model fitting** → hierarchical structure preserving mediation framework
6. **Bootstrap procedures** → participant-level resampling throughout
7. **Effect size computation** → standardized metrics for comparison
8. **Power analysis** → multiple alpha levels for chapter integration

### Column Naming Conventions
- **UID:** String identifier (consistent across all files)
- **theta_all:** Continuous outcome variable (IRT ability)
- **Age:** Continuous predictor (years)
- **RAVLT_T, BVMT_T, RPM_T:** Continuous predictors (T-scores)
- **beta, se, t_stat:** Regression coefficients and statistics
- **p_uncorrected, p_bonferroni:** Dual p-value format (Decision D068)
- **ci_lower, ci_upper:** Bootstrap confidence intervals
- **f2, sr2:** Effect size metrics

### Data Type Constraints
- **UID:** object (string, nullable=False)
- **Continuous variables:** float64 (nullable=True for intermediate steps)
- **Statistical results:** float64 (nullable=False after computation)
- **p-values:** float64 in [0, 1] range
- **Effect sizes:** float64, can be negative for suppression effects

---

## Cross-RQ Dependencies

### Ch5 5.1.1 Dependency
**Required Status:** rq_results: success
**Required Outputs:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative patterns: results/ch5/5.1.1/data/*theta*.csv
- Expected content: theta_all scores for 100 participants
- Format verification: UID (string), theta_all (float), SE_theta (float)

**Fallback Strategy:**
If primary file not found, search for files matching *theta*.csv pattern in results/ch5/5.1.1/data/
If no theta files found, QUIT with error: "Ch5 5.1.1 theta estimation not completed"

**Data Quality Dependencies:**
- All 100 participants must have theta_all scores
- Theta values must be in reasonable IRT range [-4, 4]
- No missing values accepted (complete IRT calibration assumed)

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
- **Output validation:** Dependency check file with clear PASS/FAIL status
- **Value validation:** All required files accessible, proper format verified
- **Quality validation:** N=100 participants confirmed, no missing key files
- **Log validation:** Success messages for each dependency check

#### Step 1: Extract Theta Scores
- **Output validation:** 100 rows × 2 columns (UID, theta_all)
- **Value validation:** theta_all in [-4, 4], no missing values
- **Quality validation:** 100 unique UIDs, adequate theta variability
- **Log validation:** Extraction success, theta range reported

#### Step 2: Extract Cognitive Tests
- **Output validation:** 100 rows × 5 columns (UID, Age, tests)
- **Value validation:** Age [18-80], T-scores [20-80]
- **Quality validation:** <5% missing per variable, adequate ranges
- **Log validation:** Extraction success, missing data summary

#### Step 3: Merge Analysis Dataset
- **Output validation:** 100 rows preserved, no merge failures
- **Value validation:** All range constraints maintained
- **Quality validation:** Complete merge (100% match rate)
- **Log validation:** Merge success, descriptive statistics

#### Step 4: Compute Bivariate Correlations
- **Output validation:** 10 correlations + bootstrap CIs
- **Value validation:** Correlations [-1, 1], valid p-values
- **Quality validation:** Expected correlation pattern observed
- **Log validation:** Correlation computation success, bootstrap completion

#### Step 5: Hierarchical Regression Models
- **Output validation:** 2 models + coefficients + bootstrap CIs
- **Value validation:** R² [0, 1], reasonable betas
- **Quality validation:** Model convergence, expected mediation pattern
- **Log validation:** Model fitting success, bootstrap completion

#### Step 6: Formal Mediation Analysis
- **Output validation:** Mediation paths + indirect effects + bootstrap
- **Value validation:** Proportion mediated interpretable, valid CIs
- **Quality validation:** All paths computed, bootstrap convergence
- **Log validation:** Mediation analysis success, effect interpretation

#### Step 7: Model Diagnostics and Assumptions
- **Output validation:** Assumption tests + VIF + diagnostics
- **Value validation:** VIF reasonable, test statistics valid
- **Quality validation:** All assumptions tested, remedial actions documented
- **Log validation:** Diagnostic completion, assumption status summary

#### Step 8: Cross-Validation Analysis
- **Output validation:** 5 folds completed + CV summary
- **Value validation:** CV R² reasonable, overfitting gap acceptable
- **Quality validation:** Stable performance across folds
- **Log validation:** CV completion, stability assessment

#### Step 9: Effect Size Analysis
- **Output validation:** Effect sizes + bootstrap CIs + interpretations
- **Value validation:** Effect sizes in reasonable ranges
- **Quality validation:** Consistent effect size metrics, valid interpretations
- **Log validation:** Effect size completion, magnitude assessment

#### Step 10: Power Analysis
- **Output validation:** Power estimates + sensitivity + mediation power
- **Value validation:** Power [0, 1], reasonable minimum detectable effects
- **Quality validation:** Power assessment comprehensive, limitations noted
- **Log validation:** Power analysis completion, adequacy assessment

---

## Summary

**Total Steps:** 11 (Step 0: validation + Steps 1-10: analysis)
**Estimated Runtime:** 45-60 minutes
**Cross-RQ Dependencies:** Ch5 5.1.1 (theta_all scores)
**Primary Outputs:** Hierarchical regression results with formal mediation analysis
**Validation Coverage:** 100% (all 11 steps have 4-layer validation requirements)

**Key Hypothesis:** Age should NOT predict REMEMVR after controlling for cognitive tests, consistent with VR scaffolding hypothesis and Ch5's age-invariant VR forgetting finding.

**Critical Methodological Notes:**
- Bootstrap resampling at participant level preserves data structure
- Dual p-value reporting addresses multiple comparison concerns
- Formal mediation analysis goes beyond standard hierarchical regression
- Cross-validation assesses model generalizability
- Power analysis acknowledges limitations for mediation detection with N=100
- Comprehensive assumption checking with specified remedial actions
- All random processes use seed=42 for reproducibility

**Expected Result Pattern (VR Scaffolding Hypothesis):**
1. **Bivariate:** r(Age, theta_all) = small negative correlation (r < -0.15)
2. **Model 1:** Age significantly predicts REMEMVR (establishes total effect)
3. **Model 2:** Age becomes non-significant after controlling for cognitive tests
4. **Mediation:** Significant indirect effect through cognitive tests
5. **Interpretation:** VR scaffolding compensates for age-related decline

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan → creates 3_tools.yaml
3. rq_analysis reads plan + tools → creates 4_analysis.yaml
4. g_code reads analysis → generates executable code

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent v5.1.0