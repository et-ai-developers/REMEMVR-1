# Analysis Plan: RQ 7.2.3 - Age x Cognitive Test Interaction

**Research Question:** 7.2.3
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

**Purpose:** Test whether cognitive tests (RAVLT, BVMT, NART, RPM) predict REMEMVR performance differently for younger vs older adults, examining Age x Cognitive Test interactions to assess compensatory processing models vs VR scaffolding effects.

**Pipeline:** Multiple Linear Regression with Interaction Terms
**Steps:** 8 total analysis steps (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** ~45 minutes (including bootstrap and cross-validation)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Bonferroni correction for within-RQ family (alpha = 0.05/4 = 0.0125)
- Bootstrap confidence intervals for interaction terms
- Simple slopes analysis for significant interactions

**Statistical Implementation Highlights:**
- Random seed=42 for all randomized procedures (bootstrap, CV)
- 2000 bootstrap iterations for stable CI estimation
- 5-fold cross-validation with gap threshold monitoring
- Cook's distance outlier detection (threshold: 4/n = 0.04)
- HC3 robust standard errors for heteroscedasticity

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies

**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 outputs and cognitive test data exist before proceeding

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv (IRT ability estimates)
- Alternative: results/ch5/5.1.1/data/*theta*.csv (pattern match)
- Fallback: results/ch5/5.1.1/status.yaml (verify rq_results: success)
- Expected content: Individual theta_all scores for 100 participants
- Master data: data/cache/master.xlsx (cognitive test T-scores)
- If Ch5 output not found: QUIT with "Ch5 5.1.1 theta output not found"

**Processing:**
- Check Ch5 5.1.1 completed successfully (status.yaml)
- Locate theta score file using multiple patterns
- Verify file contains 100 participants with theta_all scores
- Test master.xlsx accessibility and cognitive test columns
- Log all validation checks with pass/fail status

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Required sections: Ch5 Status, File Paths, Master.xlsx Access, Column Check

*Value Ranges:*
- Boolean validation results: PASS/FAIL for each check
- Participant count: exactly 100 in theta file
- Cognitive test columns: RAVLT_T, BVMT_T, NART_T, RPM_T present

*Data Quality:*
- All dependency files accessible
- No missing required columns in master.xlsx
- Theta file readable and non-empty

*Log Validation:*
- Required patterns: "VALIDATION - PASS", "Dependencies confirmed"
- Forbidden patterns: "ERROR", "FAIL", "not found"
- Acceptable warnings: None for dependency validation

**Expected Behavior on Validation Failure:**
- Raise error with specific missing dependency
- Log to logs/step00_validate_dependencies.log
- QUIT immediately, invoke g_debug

---

### Step 1: Extract and Prepare Cognitive Test Data

**Dependencies:** Step 0 (dependency validation)
**Complexity:** Medium (~8 minutes)

**Purpose:** Extract cognitive test T-scores and age from master.xlsx, merge with theta scores from Ch5

**Input:**
- data/cache/master.xlsx (cognitive tests: RAVLT_T, BVMT_T, NART_T, RPM_T)
- results/ch5/5.1.1/data/step03_theta_scores.csv (theta_all per participant)

**Processing:**
- Load master.xlsx, extract: UID, Age, RAVLT_T, BVMT_T, NART_T, RPM_T
- Verify all cognitive tests are T-scored (mean=50, SD=10 expected)
- Load Ch5 theta scores, extract: UID, theta_all (mean IRT ability)
- Merge datasets on UID with inner join (keep complete cases only)
- Check for missing data: exclude participants missing any cognitive test
- Compute descriptive statistics for all variables
- Document final sample size and any exclusions

**Output:**
- data/step01_cognitive_tests_raw.csv (extracted cognitive data)
- data/step01_theta_merged.csv (merged dataset)
- data/step01_descriptives.csv (means, SDs, ranges)

**Validation Requirement:**
Validation tools MUST be used after data extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_cognitive_tests_raw.csv: N rows x 6 columns (UID, Age, 4 tests)
- data/step01_theta_merged.csv: N rows x 7 columns (UID, Age, 4 tests, theta_all)
- data/step01_descriptives.csv: 6 rows x 4 columns (variable, mean, sd, range)

*Value Ranges:*
- Age in [18, 85] (REMEMVR age range)
- Cognitive T-scores in [20, 80] (reasonable T-score range)
- theta_all in [-3, 3] (IRT ability scale)
- Sample size: 85-100 participants (allowing for some missing data)

*Data Quality:*
- No duplicate UIDs
- All cognitive T-scores present (no NaN in final dataset)
- Merged dataset has all 7 required columns
- Descriptive statistics computed for all variables

*Log Validation:*
- Required: "Extraction complete: N participants"
- Required: "Merge successful: N complete cases"
- Forbidden: "ERROR", "merge failed", "missing required columns"
- Acceptable: "Excluded N participants due to missing cognitive data"

**Expected Behavior on Validation Failure:**
- Raise error with specific data quality issue
- Log to logs/step01_extract_cognitive_tests.log
- QUIT immediately, invoke g_debug

---

### Step 2: Center Predictors and Create Interaction Terms

**Dependencies:** Step 1 (cognitive test data)
**Complexity:** Low (~3 minutes)

**Purpose:** Center age and cognitive test predictors for interpretable interaction analysis

**Input:**
- data/step01_theta_merged.csv

**Processing:**
- Center Age: Age_c = Age - mean(Age) for interpretation at mean age
- Center cognitive tests: 
  - RAVLT_c = RAVLT_T - 50 (T-score deviation from population mean)
  - BVMT_c = BVMT_T - 50
  - NART_c = NART_T - 50  
  - RPM_c = RPM_T - 50
- Create interaction terms:
  - Age_c_x_RAVLT_c = Age_c * RAVLT_c
  - Age_c_x_BVMT_c = Age_c * BVMT_c
  - Age_c_x_NART_c = Age_c * NART_c
  - Age_c_x_RPM_c = Age_c * RPM_c
- Compute correlation matrix for all predictors (check multicollinearity)
- Document centering statistics (means, verification of centering)

**Output:**
- data/step02_centered_predictors.csv (full dataset with centered variables)
- data/step02_correlation_matrix.csv (predictor correlations)
- data/step02_centering_stats.csv (verification statistics)

**Validation Requirement:**
Validation tools MUST be used after predictor centering execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_centered_predictors.csv: N rows x 15 columns (original + centered + interactions)
- data/step02_correlation_matrix.csv: 9 rows x 9 columns (predictor correlation matrix)
- data/step02_centering_stats.csv: 5 rows x 4 columns (variable, original_mean, centered_mean, verification)

*Value Ranges:*
- Age_c: centered around 0 (mean approximately 0.0)
- Test_c: centered around 0 (mean approximately 0.0)
- Correlations in [-1, 1]
- Interaction terms: product of centered variables

*Data Quality:*
- All centered variables have mean approximately 0 (within 0.01)
- No missing values in interaction terms
- Correlation matrix symmetric with 1.0 on diagonal
- Sample size maintained from Step 1

*Log Validation:*
- Required: "Centering complete: means verified"
- Required: "Interaction terms created: 4 interactions"
- Forbidden: "ERROR", "centering failed", "missing data introduced"

**Expected Behavior on Validation Failure:**
- Raise error with specific centering issue
- Log to logs/step02_center_predictors.log
- QUIT immediately, invoke g_debug

---

### Step 3: Fit Age x Cognitive Test Interaction Models

**Dependencies:** Step 2 (centered predictors)
**Complexity:** High (~12 minutes including diagnostics)

**Purpose:** Fit separate regression models for each Age x Test interaction with comprehensive diagnostics

**Input:**
- data/step02_centered_predictors.csv

**Processing:**
- Fit 4 separate models using statsmodels.api.OLS:
  - Model 1: theta_all ~ Age_c + RAVLT_c + Age_c_x_RAVLT_c
  - Model 2: theta_all ~ Age_c + BVMT_c + Age_c_x_BVMT_c
  - Model 3: theta_all ~ Age_c + NART_c + Age_c_x_NART_c
  - Model 4: theta_all ~ Age_c + RPM_c + Age_c_x_RPM_c
- Extract for each model: R², F-statistic, coefficients, SEs, t-values
- Compute p-values: BOTH uncorrected AND Bonferroni corrected (Decision D068)
- Bonferroni correction: alpha = 0.05/4 = 0.0125 per interaction test
- Check assumptions for all models:
  - Normality: Shapiro-Wilk test on residuals (threshold: p > 0.05)
  - Homoscedasticity: Breusch-Pagan test (threshold: p > 0.05)
  - Multicollinearity: VIF for each predictor (threshold: VIF < 5)
  - Outliers: Cook's distance (threshold: > 4/n = 0.04)
- Remedial actions if assumptions violated:
  - Normality p < 0.05: Flag for bootstrap CIs as primary inference
  - Heteroscedasticity p < 0.05: Compute HC3 robust standard errors
  - VIF > 5: Document multicollinearity, proceed with caution
  - Outliers (Cook's D > 0.04): Document count, report with/without

**Output:**
- data/step03_interaction_models.csv (model summaries)
- data/step03_model_coefficients.csv (detailed coefficients with dual p-values)
- data/step03_assumption_checks.csv (diagnostic test results)
- data/step03_outlier_diagnostics.csv (Cook's distance, leverage)

**Validation Requirement:**
Validation tools MUST be used after model fitting execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_interaction_models.csv: 4 rows x 8 columns (model, R2, F_stat, p_F, etc.)
- data/step03_model_coefficients.csv: 12 rows x 9 columns (model, term, coef, se, t, p_uncorr, p_bonf, vif, cook_max)
- data/step03_assumption_checks.csv: 4 rows x 6 columns (model, shapiro_p, bp_p, max_vif, n_outliers, remedial)
- data/step03_outlier_diagnostics.csv: N rows x 5 columns (UID, model, cooks_d, leverage, outlier_flag)

*Value Ranges:*
- R² in [0, 1] (coefficient of determination)
- F-statistics > 0 (positive F-values)
- p-values in [0, 1] for both uncorrected and corrected
- VIF values > 1.0 (variance inflation factors)
- Cook's distance > 0 (positive influence measures)

*Data Quality:*
- All 4 models fitted successfully
- Both uncorrected AND corrected p-values present (Decision D068)
- Assumption checks completed for all models
- Cook's distance computed for all participants

*Log Validation:*
- Required: "All 4 interaction models fitted successfully"
- Required: "Assumption checks completed"
- Required: "Dual p-values computed (Decision D068)"
- Forbidden: "ERROR", "model convergence failed", "singular matrix"
- Acceptable: "Assumption violation detected: remedial action applied"

**Expected Behavior on Validation Failure:**
- Raise error with specific model fitting issue
- Log to logs/step03_fit_interaction_models.log
- QUIT immediately, invoke g_debug

---

### Step 4: Simple Slopes Analysis (If Interactions Significant)

**Dependencies:** Step 3 (interaction models)
**Complexity:** Medium (~8 minutes)

**Purpose:** For significant Age x Test interactions, compute test slopes at younger (-1SD) vs older (+1SD) age levels

**Input:**
- data/step03_interaction_models.csv
- data/step03_model_coefficients.csv
- data/step02_centered_predictors.csv (for age SD)

**Processing:**
- Identify significant interactions: p_bonferroni < 0.0125
- For each significant interaction:
  - Compute age levels: Age_low = -1*SD(Age_c), Age_high = +1*SD(Age_c)
  - Calculate simple slopes:
    - Slope_low = β_test + β_interaction * Age_low
    - Slope_high = β_test + β_interaction * Age_high
  - Compute standard errors using variance-covariance matrix
  - Test slope significance: t = slope / SE, p-value
  - Interpret direction: stronger/weaker prediction in older adults
- If no significant interactions: document null findings
- Create interaction plots preparation data (age x test grid)
- Document effect sizes: Cohen's f² for interaction terms

**Output:**
- data/step04_simple_slopes.csv (slopes at age levels)
- data/step04_interaction_summary.csv (significant interactions only)
- data/step04_plot_data.csv (data for interaction visualization)

**Validation Requirement:**
Validation tools MUST be used after simple slopes execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_simple_slopes.csv: Variable rows x 8 columns (interaction, age_level, slope, se, t, p, ci_lower, ci_upper)
- data/step04_interaction_summary.csv: Variable rows x 6 columns (test, interaction_p, sig_flag, interpretation, effect_size, cohen_f2)
- data/step04_plot_data.csv: Grid rows x 4 columns (age_c, test_c, predicted_theta, interaction_model)

*Value Ranges:*
- Simple slopes: reasonable values based on standardized predictors
- Standard errors > 0 (positive SEs)
- t-values: any real number
- p-values in [0, 1]
- Cohen's f² > 0 (positive effect sizes)

*Data Quality:*
- Simple slopes computed only for significant interactions
- All slopes have corresponding standard errors
- If no significant interactions: files may be empty but present
- Plot data covers full range of age and test scores

*Log Validation:*
- Required: "Simple slopes analysis complete"
- Required: "Found N significant interactions" (where N = 0-4)
- Forbidden: "ERROR", "slope calculation failed"
- Acceptable: "No significant interactions detected"

**Expected Behavior on Validation Failure:**
- Raise error with specific simple slopes issue
- Log to logs/step04_simple_slopes.log
- QUIT immediately, invoke g_debug

---

### Step 5: Bootstrap Confidence Intervals for Interaction Terms

**Dependencies:** Step 3 (interaction models)
**Complexity:** High (~15 minutes for 2000 iterations)

**Purpose:** Generate robust confidence intervals for interaction coefficients using participant-level bootstrap

**Input:**
- data/step02_centered_predictors.csv

**Processing:**
- Participant-level block bootstrap (preserves within-participant correlation if any)
- Iterations: 2000 (increased from 1000 per rq_stats recommendations)
- Random seed: 42 for reproducibility
- For each iteration:
  - Resample participants WITH replacement (maintain all observations per participant)
  - Fit all 4 interaction models on bootstrap sample
  - Extract interaction coefficients (β_interaction for each test)
- Compute 95% CI using percentile method (2.5th, 97.5th percentiles)
- Compare bootstrap CIs with model-based CIs
- Check CI stability: difference between model and bootstrap CIs
- Document bootstrap distribution properties (skewness, outliers)

**Output:**
- data/step05_bootstrap_coefficients.csv (interaction coefficients from all iterations)
- data/step05_bootstrap_cis.csv (95% CIs for interaction terms)
- data/step05_bootstrap_comparison.csv (model vs bootstrap CI comparison)

**Validation Requirement:**
Validation tools MUST be used after bootstrap execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_bootstrap_coefficients.csv: 2000 rows x 5 columns (iteration, ravlt_int, bvmt_int, nart_int, rpm_int)
- data/step05_bootstrap_cis.csv: 4 rows x 6 columns (test, coef_orig, ci_lower_boot, ci_upper_boot, ci_width, stable_flag)
- data/step05_bootstrap_comparison.csv: 4 rows x 8 columns (test, model_ci_lower, model_ci_upper, boot_ci_lower, boot_ci_upper, ci_diff, interpretation)

*Value Ranges:*
- Bootstrap coefficients: reasonable interaction effect sizes
- CI bounds: ci_lower < ci_upper for all tests
- Iteration count: exactly 2000 rows
- CI widths > 0 (positive interval widths)

*Data Quality:*
- All 2000 bootstrap iterations completed
- No missing coefficients in bootstrap samples
- CIs computed for all 4 interaction terms
- Stability flags computed (difference between model and bootstrap)

*Log Validation:*
- Required: "Bootstrap complete: 2000 iterations"
- Required: "Random seed: 42"
- Required: "CI computation successful for all interactions"
- Forbidden: "ERROR", "bootstrap failed", "sampling error"
- Acceptable: "Some iterations failed convergence (documented)"

**Expected Behavior on Validation Failure:**
- Raise error with specific bootstrap issue
- Log to logs/step05_bootstrap_cis.log
- QUIT immediately, invoke g_debug

---

### Step 6: Cross-Validation for Model Stability

**Dependencies:** Step 3 (interaction models)  
**Complexity:** Medium (~10 minutes)

**Purpose:** Assess generalizability of Age x Test interaction effects using k-fold cross-validation

**Input:**
- data/step02_centered_predictors.csv

**Processing:**
- Implement 5-fold cross-validation using sklearn.model_selection.KFold
- Random seed: 42 for reproducibility
- Shuffle: True (randomize before splitting)
- Stratification: None for regression (quantile-based if theta_all skewed)
- For each fold:
  - Fit all 4 interaction models on training set (80% of data)
  - Evaluate on test set (20% of data)
  - Compute R² for each model on training and test sets
  - Extract interaction coefficient and significance
- Compute mean and std of metrics across folds:
  - Mean R² (training and test) 
  - Mean interaction coefficient
  - Proportion of folds where interaction significant
- Assess overfitting: flag if train-test R² gap > 0.10
- Check interaction effect stability: SD of coefficients across folds

**Output:**
- data/step06_cv_results.csv (fold-by-fold results)
- data/step06_cv_summary.csv (cross-validation summary statistics)
- data/step06_overfitting_check.csv (train-test gap assessment)

**Validation Requirement:**
Validation tools MUST be used after cross-validation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_cv_results.csv: 20 rows x 8 columns (fold, model, train_r2, test_r2, interaction_coef, interaction_p, overfitting_flag)
- data/step06_cv_summary.csv: 4 rows x 10 columns (model, mean_train_r2, mean_test_r2, mean_gap, interaction_mean, interaction_sd, prop_significant, stability_flag)
- data/step06_overfitting_check.csv: 4 rows x 5 columns (model, max_gap, mean_gap, overfitting_detected, interpretation)

*Value Ranges:*
- R² values in [0, 1] (coefficients of determination)
- R² gaps in [0, 1] (train - test difference)
- Interaction coefficients: reasonable effect sizes  
- Proportions in [0, 1] (fraction significant)
- Standard deviations > 0 (positive variability measures)

*Data Quality:*
- Exactly 5 folds x 4 models = 20 rows in results
- All cross-validation iterations completed
- Train and test R² computed for all folds
- Overfitting assessment completed

*Log Validation:*
- Required: "Cross-validation complete: 5 folds"
- Required: "Random seed: 42" 
- Required: "Overfitting assessment completed"
- Forbidden: "ERROR", "CV failed", "fold creation failed"
- Acceptable: "Some models showed overfitting (train-test gap > 0.10)"

**Expected Behavior on Validation Failure:**
- Raise error with specific cross-validation issue
- Log to logs/step06_cross_validation.log
- QUIT immediately, invoke g_debug

---

### Step 7: Effect Size Computation and Power Analysis

**Dependencies:** Steps 3-6 (complete model results)
**Complexity:** Medium (~7 minutes)

**Purpose:** Compute standardized effect sizes and post-hoc power analysis for interaction detection

**Input:**
- data/step03_interaction_models.csv
- data/step03_model_coefficients.csv

**Processing:**
- Compute Cohen's f² for each interaction term:
  - f² = (R²_full - R²_reduced) / (1 - R²_full)
  - R²_full = model with interaction, R²_reduced = model without interaction
- Interpret effect sizes: small (0.02), medium (0.15), large (0.35)
- Compute semi-partial correlations (sr²) for interaction terms
- Post-hoc power analysis for interaction detection:
  - Given: N=sample_size, df=3 (Age + Test + Age:Test), alpha=0.0125 (Bonferroni corrected)
  - Calculate: achieved power for observed f²
  - Use: statsmodels.stats.power.FTestAnovaPower()
  - Compute: minimum detectable f² at 80% power
- Report power limitations if achieved power < 0.80
- Standardized beta coefficients for all predictors

**Output:**
- data/step07_effect_sizes.csv (f², sr², standardized betas)
- data/step07_power_analysis.csv (power calculations)
- data/step07_effect_interpretation.csv (effect size categories and interpretations)

**Validation Requirement:**
Validation tools MUST be used after effect size computation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_effect_sizes.csv: 4 rows x 8 columns (test, r2_full, r2_reduced, cohens_f2, sr2, std_beta_age, std_beta_test, std_beta_interaction)
- data/step07_power_analysis.csv: 4 rows x 7 columns (test, observed_f2, achieved_power, min_detectable_f2_80pct, power_adequate, interpretation)
- data/step07_effect_interpretation.csv: 4 rows x 5 columns (test, cohens_f2, effect_category, practical_significance, confidence_rating)

*Value Ranges:*
- Cohen's f² > 0 (positive effect sizes)
- Semi-partial correlations in [0, 1] 
- Power in [0, 1] (probability values)
- Standardized betas: reasonable values for standardized predictors
- R² values in [0, 1]

*Data Quality:*
- Effect sizes computed for all 4 interaction terms
- Power analysis completed for all models
- Effect size interpretations provided
- Minimum detectable effect sizes calculated

*Log Validation:*
- Required: "Effect size computation complete"
- Required: "Power analysis completed for all interactions" 
- Required: "Minimum detectable effects calculated"
- Forbidden: "ERROR", "power calculation failed", "division by zero"
- Acceptable: "Low power detected for small effect sizes"

**Expected Behavior on Validation Failure:**
- Raise error with specific effect size computation issue
- Log to logs/step07_effect_sizes.log
- QUIT immediately, invoke g_debug

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)

**Step 0 - Dependency Validation:**
- data/step00_dependency_validation.txt

**Step 1 - Data Extraction:**
- data/step01_cognitive_tests_raw.csv
- data/step01_theta_merged.csv  
- data/step01_descriptives.csv

**Step 2 - Predictor Centering:**
- data/step02_centered_predictors.csv
- data/step02_correlation_matrix.csv
- data/step02_centering_stats.csv

**Step 3 - Interaction Models:**
- data/step03_interaction_models.csv
- data/step03_model_coefficients.csv
- data/step03_assumption_checks.csv
- data/step03_outlier_diagnostics.csv

**Step 4 - Simple Slopes:**
- data/step04_simple_slopes.csv
- data/step04_interaction_summary.csv
- data/step04_plot_data.csv

**Step 5 - Bootstrap Analysis:**
- data/step05_bootstrap_coefficients.csv
- data/step05_bootstrap_cis.csv
- data/step05_bootstrap_comparison.csv

**Step 6 - Cross-Validation:**
- data/step06_cv_results.csv
- data/step06_cv_summary.csv
- data/step06_overfitting_check.csv

**Step 7 - Effect Sizes:**
- data/step07_effect_sizes.csv
- data/step07_power_analysis.csv
- data/step07_effect_interpretation.csv

### Logs (ONLY execution logs)

- logs/step00_validate_dependencies.log
- logs/step01_extract_cognitive_tests.log
- logs/step02_center_predictors.log
- logs/step03_fit_interaction_models.log
- logs/step04_simple_slopes.log
- logs/step05_bootstrap_cis.log
- logs/step06_cross_validation.log
- logs/step07_effect_sizes.log

### Plots (EMPTY until rq_plots runs)

Note: Plot source data created in data/ folder:
- data/step04_plot_data.csv (Age x Test interaction plots)

### Results (EMPTY until rq_results runs)

Note: summary.md created by rq_results

---

## Expected Data Formats

### Step-to-Step Transformations

1. **Raw Data → Merged Dataset:** Cognitive tests + theta scores joined on UID
2. **Merged → Centered:** Age and test predictors centered, interactions created
3. **Centered → Models:** Four separate interaction models fitted
4. **Models → Slopes:** Simple slopes computed for significant interactions
5. **Models → Bootstrap:** Robust CIs via resampling
6. **Models → CV:** Generalizability assessment via k-fold validation
7. **Models → Effect Sizes:** Standardized measures and power analysis

### Column Naming Conventions

- **UIDs:** UID (string identifier)
- **Raw variables:** Age, RAVLT_T, BVMT_T, NART_T, RPM_T, theta_all
- **Centered variables:** Age_c, RAVLT_c, BVMT_c, NART_c, RPM_c
- **Interactions:** Age_c_x_RAVLT_c, Age_c_x_BVMT_c, etc.
- **Model outputs:** model_name, coefficient, se, t_value, p_uncorrected, p_bonferroni
- **Effect sizes:** cohens_f2, sr2, std_beta

### Data Type Constraints

- **UID:** string (non-nullable)
- **Age:** float (18-85 range)
- **Cognitive tests:** float (T-scores, typically 20-80)
- **theta_all:** float (-3 to +3 IRT range)
- **p-values:** float (0-1 range, nullable if model fails)
- **Effect sizes:** float (>0, nullable if not computable)

---

## Cross-RQ Dependencies

**Required Dependency:**
- **Source RQ:** Ch5 5.1.1 (Functional Form Comparison)
- **Required Status:** rq_results = success
- **Required Files:** 
  - Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
  - Alternative: results/ch5/5.1.1/data/*theta*.csv
  - Fallback: Any file containing theta_all scores for 100 participants
- **Content:** Individual theta_all ability estimates
- **Validation:** Step 0 dependency check with circuit breaker

**Master Data Dependency:**
- **File:** data/cache/master.xlsx
- **Content:** UID, Age, RAVLT_T, BVMT_T, NART_T, RPM_T
- **Validation:** Step 0 accessibility check

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution. This ensures 100% validation coverage across the 8-step pipeline.

### Validation Strategy

- **Per-step validation:** Each step has 4-layer substance validation criteria
- **Circuit breakers:** Immediate QUIT on validation failure with g_debug invocation
- **Log validation:** Required patterns, forbidden patterns, acceptable warnings
- **File validation:** Exact paths, dimensions, data types, value ranges
- **Quality validation:** Missing data tolerance, duplicate checks, distribution checks

### Critical Validation Points

1. **Step 0:** Dependency availability (Ch5 outputs, master.xlsx access)
2. **Step 1:** Data extraction completeness (N participants, required columns)  
3. **Step 3:** Model fitting success (convergence, assumption checks)
4. **Step 5:** Bootstrap stability (2000 iterations, CI coverage)
5. **Step 6:** Cross-validation generalizability (overfitting detection)

---

## Summary

**Total Steps:** 8 (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** ~45 minutes
**Cross-RQ Dependencies:** Ch5 5.1.1 (theta scores) + master.xlsx (cognitive tests)
**Primary Outputs:** Age x Test interaction coefficients with dual p-values, simple slopes analysis
**Validation Coverage:** 100% (all 8 steps have 4-layer validation requirements)

**Key Hypothesis:** Cognitive tests may predict REMEMVR performance more strongly in older vs younger adults, supporting compensatory processing models. Alternative: No interaction (equal prediction across age range) supporting VR scaffolding effects.

**Critical Methodological Notes:**
- Bonferroni correction for within-RQ multiple comparisons (4 interactions)
- Bootstrap confidence intervals for robust inference (2000 iterations)
- Simple slopes analysis conditional on significant interactions
- Cross-validation for generalizability assessment
- Post-hoc power analysis acknowledges interaction detection limitations
- Dual p-value reporting per Decision D068

**Statistical Implementation Specifications:**
- Random seed=42 for all randomized procedures
- Cook's distance threshold: 4/n for outlier detection
- HC3 robust standard errors for heteroscedasticity
- 5-fold CV with train-test gap threshold: 0.10
- Bootstrap CI method: percentile (2.5th, 97.5th percentiles)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner v5.1 agent with enhanced statistical specifications