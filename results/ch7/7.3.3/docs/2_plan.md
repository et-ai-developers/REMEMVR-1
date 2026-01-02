# Analysis Plan: RQ 7.3.3 - Cognitive Predictors of High-Confidence Errors

**Research Question:** 7.3.3
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This analysis tests whether cognitive abilities predict individual differences in high-confidence error (HCE) rates using hierarchical multiple regression. HCE rates from Chapter 6 (6.6.x analyses) serve as the outcome, with cognitive test scores (RAVLT_T, BVMT_T, RPM_T) and demographics as predictors. Primary hypothesis: RPM (fluid intelligence) negatively predicts HCE rates, while memory capacity tests (RAVLT/BVMT) should not.

**Pipeline:** Multiple Linear Regression with Hierarchical Entry + Cross-Validation
**Steps:** 9 total analysis steps (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** ~45 minutes

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni + FDR)
- Chapter 7 Bonferroni correction: alpha = 0.05/28 = 0.00179 (chapter-level)
- Within-RQ correction: alpha = 0.00179/4 = 0.000448 (for 4 cognitive predictors)

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch6 HCE outputs and master.xlsx exist before proceeding

**Input:**
- Primary: results/ch6/6.6.1/data/step03_hce_rates.csv
- Alternative: results/ch6/6.6.*/data/*hce*.csv (search Ch6 6.6.x outputs)
- Fallback: results/ch6/6.6.*/data/step*_high_confidence_errors.csv
- Master data: data/cache/master.xlsx
- Expected: HCE rates per participant (N=100) from Ch6 episodic memory analyses

**Processing:**
- Check Ch6 6.6.x completion status in results/ch6/6.6.*/status.yaml
- Search for HCE rate files using multiple patterns
- Verify master.xlsx contains cognitive test columns (RAVLT_T, BVMT_T, RPM_T)
- Log all validation attempts and results
- If no HCE data found: QUIT with "Ch6 HCE analysis incomplete"

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- File size > 500 bytes (contains detailed validation log)

*Value Ranges:*
- HCE rates expected in [0.05, 0.35] (5-35% of errors are high-confidence)
- Cognitive T-scores in [20, 80] (standard T-score range)
- Participant count = 100 (full sample)

*Data Quality:*
- HCE data: All 100 participants present
- Master.xlsx: All required cognitive columns present
- No critical missing files

*Log Validation:*
- Required patterns: "Ch6 HCE data located", "Master.xlsx validated"
- Forbidden patterns: "ERROR", "QUIT", "not found"

**Expected Behavior on Validation Failure:**
Raise error with specific missing dependency, log to logs/step00_validate_dependencies.log, quit immediately and invoke g_debug.

### Step 1: Extract and Prepare HCE Data
**Dependencies:** Step 0 (validated dependencies)
**Complexity:** Low (<5 minutes)

**Purpose:** Load HCE rates from Ch6 and prepare for analysis

**Input:**
- Ch6 HCE data (from Step 0 validation)
- Expected format: UID, hce_rate (proportion of errors that were high-confidence)

**Processing:**
- Load HCE data using validated file path from Step 0
- Verify data structure: participant IDs and HCE rates
- Check for missing values and handle appropriately
- Compute descriptive statistics (mean, SD, range, distribution)
- Log HCE rate distribution characteristics
- Save cleaned HCE data

**Output:**
- data/step01_hce_rates.csv (UID, hce_rate, with descriptives)
- data/step01_hce_descriptives.csv (summary statistics)

**Validation Requirement:**
Validation tools MUST be used after HCE data extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_hce_rates.csv: 100 rows x 2 columns (UID, hce_rate)
- data/step01_hce_descriptives.csv: 1 row x 6 columns (N, mean, sd, min, max, skewness)

*Value Ranges:*
- hce_rate in [0.05, 0.40] (plausible HCE rate range)
- Mean HCE rate in [0.15, 0.25] (expected from Ch6 findings)
- Standard deviation in [0.05, 0.15] (reasonable individual variation)

*Data Quality:*
- All 100 participants present
- No missing HCE rates (complete data expected)
- No duplicate UIDs

*Log Validation:*
- Required patterns: "HCE data loaded: 100 participants", "Mean HCE rate"
- Forbidden patterns: "ERROR", "missing", "duplicate"

**Expected Behavior on Validation Failure:**
Raise error with specific data issue, log to logs/step01_extract_hce.log, quit immediately and invoke g_debug.

### Step 2: Extract and Prepare Cognitive Test Data
**Dependencies:** Step 1 (HCE data prepared)
**Complexity:** Medium (~8 minutes including standardization)

**Purpose:** Load cognitive test scores from master.xlsx and standardize to T-scores

**Input:**
- data/cache/master.xlsx (cognitive test raw scores)
- Required columns: UID, RAVLT_total, BVMT_total, RPM_total, Age, Sex, Education

**Processing:**
- Load master.xlsx using pandas read_excel
- Extract cognitive test raw scores for N=100 participants
- Transform to T-scores: T = 50 + 10 * ((raw - mean_raw) / sd_raw)
- Create standardized variables: RAVLT_T, BVMT_T, RPM_T, Age_centered
- Compute correlation matrix between cognitive tests (check multicollinearity)
- Save cleaned cognitive data with both raw and T-scored variables

**Output:**
- data/step02_cognitive_tests.csv (UID, raw scores, T-scores, demographics)
- data/step02_cognitive_correlations.csv (correlation matrix)

**Validation Requirement:**
Validation tools MUST be used after cognitive data extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_cognitive_tests.csv: 100 rows x 10 columns
- Columns: UID, RAVLT_raw, BVMT_raw, RPM_raw, RAVLT_T, BVMT_T, RPM_T, Age_centered, Sex, Education
- data/step02_cognitive_correlations.csv: 3 rows x 3 columns (RAVLT_T, BVMT_T, RPM_T correlations)

*Value Ranges:*
- T-scores in [25, 75] (approximately 2 SD from mean)
- Raw scores > 0 (positive performance measures)
- Correlations in [0.2, 0.8] (moderate positive correlations expected)

*Data Quality:*
- All 100 participants present
- No missing cognitive test scores
- T-score transformation successful (mean approximately 50, SD approximately 10)

*Log Validation:*
- Required patterns: "Cognitive data loaded: 100 participants", "T-scores computed"
- Forbidden patterns: "ERROR", "missing scores", "transformation failed"

**Expected Behavior on Validation Failure:**
Raise error with specific transformation issue, log to logs/step02_extract_cognitive.log, quit immediately and invoke g_debug.

### Step 3: Merge and Create Analysis Dataset
**Dependencies:** Steps 1-2 (HCE and cognitive data prepared)
**Complexity:** Low (<5 minutes)

**Purpose:** Merge HCE rates with cognitive test scores to create complete analysis dataset

**Input:**
- data/step01_hce_rates.csv (HCE outcome data)
- data/step02_cognitive_tests.csv (cognitive predictor data)

**Processing:**
- Merge datasets on UID using pandas merge (inner join)
- Verify complete data for all 100 participants
- Create final analysis dataset with outcome and predictors
- Compute additional derived variables if needed
- Save merged dataset for hierarchical regression

**Output:**
- data/step03_analysis_dataset.csv (complete data: UID, hce_rate, predictors)
- data/step03_merge_summary.txt (merge statistics and completeness check)

**Validation Requirement:**
Validation tools MUST be used after dataset merging.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_analysis_dataset.csv: 100 rows x 8 columns
- Columns: UID, hce_rate, RAVLT_T, BVMT_T, RPM_T, Age_centered, Sex, Education
- data/step03_merge_summary.txt: text file with merge results

*Value Ranges:*
- All variables within expected ranges from Steps 1-2
- No missing values in any analysis variables

*Data Quality:*
- Successful merge: 100 participants with complete data
- All required variables present for hierarchical regression
- Dataset ready for statistical analysis

*Log Validation:*
- Required patterns: "Merge successful: 100 complete cases", "Analysis dataset created"
- Forbidden patterns: "ERROR", "missing", "merge failed"

**Expected Behavior on Validation Failure:**
Raise error with merge specifics, log to logs/step03_merge_data.log, quit immediately and invoke g_debug.

### Step 4: Hierarchical Multiple Regression Analysis
**Dependencies:** Step 3 (analysis dataset ready)
**Complexity:** High (~10 minutes including diagnostics)

**Purpose:** Fit hierarchical regression models to test cognitive predictors of HCE rates

**Input:**
- data/step03_analysis_dataset.csv (complete analysis data)

**Processing:**
- Model 1 (Demographics): hce_rate ~ Age_centered + Sex + Education
- Model 2 (Full): hce_rate ~ Age_centered + Sex + Education + RAVLT_T + BVMT_T + RPM_T
- Fit using statsmodels.api.OLS with standardized predictors
- Extract R², adjusted R², F-statistics, coefficients with standard errors
- Compute model comparison: ΔR² and F-test for model improvement
- Bootstrap confidence intervals for all coefficients:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - CI: Percentile method (2.5th, 97.5th percentiles)
- Multiple comparison corrections:
  - Within-RQ family: 4 cognitive predictors
  - Bonferroni: alpha = 0.00179/4 = 0.000448 per test
  - FDR: Benjamini-Hochberg correction
  - Report BOTH uncorrected AND corrected p-values (Decision D068)

**Output:**
- data/step04_regression_models.csv (model summaries and comparisons)
- data/step04_coefficients.csv (betas, SEs, CIs, dual p-values)
- data/step04_model_comparison.csv (R², ΔR², F-tests)

**Validation Requirement:**
Validation tools MUST be used after regression analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_regression_models.csv: 2 rows x 6 columns (Model1, Model2 summaries)
- data/step04_coefficients.csv: 6 rows x 8 columns (predictors with stats)
- Columns: predictor, beta, se, ci_lower, ci_upper, p_uncorrected, p_bonferroni, p_fdr

*Value Ranges:*
- R² in [0.05, 0.50] (reasonable explanatory power)
- Beta coefficients in [-2, 2] (standardized predictors)
- P-values in [0, 1] (valid probability range)
- Bootstrap CIs: ci_lower < beta < ci_upper

*Data Quality:*
- All 6 predictors present (3 demographics + 3 cognitive)
- Bootstrap CIs successfully computed (1000 iterations)
- Dual p-values for all cognitive predictors (Decision D068)

*Log Validation:*
- Required patterns: "Model 1 R² =", "Model 2 R² =", "Bootstrap complete: 1000 iterations"
- Forbidden patterns: "ERROR", "convergence failed", "singular matrix"

**Expected Behavior on Validation Failure:**
Raise error with regression specifics, log to logs/step04_regression.log, quit immediately and invoke g_debug.

### Step 5: Model Diagnostics and Assumption Checks
**Dependencies:** Step 4 (regression models fitted)
**Complexity:** Medium (~8 minutes)

**Purpose:** Check regression assumptions and implement remedial actions if violated

**Input:**
- data/step04_regression_models.csv (fitted models)
- Model 2 residuals and fitted values for diagnostics

**Processing:**
- Check multicollinearity: Variance Inflation Factor (VIF) for each predictor
- Check normality: Shapiro-Wilk test on residuals + Q-Q plot data
- Check homoscedasticity: Breusch-Pagan test
- Check for outliers: Cook's distance > 4/N threshold
- Check linearity: Partial residual plots (component + residual plots)
- Remedial actions if assumptions violated:
  - Normality p < 0.05: Report bootstrap CIs as primary (1000 iterations, seed=42)
  - Heteroscedasticity p < 0.05: Add HC3 robust standard errors
  - VIF > 5: Document multicollinearity, consider ridge if VIF > 10
  - Outliers (Cook's D > 0.04): Report results with and without outliers
- Generate diagnostic plot data for visualization

**Output:**
- data/step05_diagnostics.csv (VIF, assumption tests, outlier flags)
- data/step05_diagnostic_plots_data.csv (residuals, fitted, Q-Q data)
- data/step05_remedial_actions.txt (assumption violations and responses)

**Validation Requirement:**
Validation tools MUST be used after assumption checking.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_diagnostics.csv: 6 rows x 4 columns (predictor, VIF, assumptions)
- data/step05_diagnostic_plots_data.csv: 100 rows x 4 columns (fitted, residuals, qq_theoretical, qq_sample)
- data/step05_remedial_actions.txt: text summary of violations and actions

*Value Ranges:*
- VIF in [1.0, 10.0] (multicollinearity check)
- Cook's D in [0.0, 0.20] (outlier detection)
- Residuals approximately normal distribution

*Data Quality:*
- All 6 predictors have VIF values
- All assumption tests completed
- Remedial actions documented for any violations

*Log Validation:*
- Required patterns: "VIF computed", "Assumption tests complete", "Diagnostics successful"
- Forbidden patterns: "ERROR", "test failed", "computation error"

**Expected Behavior on Validation Failure:**
Raise error with diagnostic specifics, log to logs/step05_diagnostics.log, quit immediately and invoke g_debug.

### Step 6: Effect Sizes and Importance Analysis
**Dependencies:** Step 5 (diagnostics complete)
**Complexity:** Medium (~7 minutes including bootstrap)

**Purpose:** Compute comprehensive effect sizes and predictor importance measures

**Input:**
- data/step04_regression_models.csv (model R² values)
- data/step04_coefficients.csv (standardized coefficients)

**Processing:**
- Compute Cohen's f² effect sizes: f² = R²/(1-R²) for each model
- Compute semi-partial correlations (sr²) for each predictor
- Calculate relative importance using dominance analysis or relative weights
- Bootstrap effect sizes for uncertainty quantification:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Bootstrap R², f², and sr² values
  - 95% CI using percentile method
- Interpret effect sizes using Cohen's conventions and context-specific benchmarks:
  - f² = 0.02 (small), 0.15 (medium), 0.35 (large)
  - Note: Individual differences in metacognitive monitoring may show smaller effects

**Output:**
- data/step06_effect_sizes.csv (f², sr², relative importance with CIs)
- data/step06_effect_interpretation.csv (Cohen classifications and practical significance)

**Validation Requirement:**
Validation tools MUST be used after effect size computation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_effect_sizes.csv: 8 rows x 6 columns (predictors + models, effect sizes, CIs)
- Columns: measure, effect_size, ci_lower, ci_upper, cohen_category, practical_significance
- data/step06_effect_interpretation.csv: 2 rows x 4 columns (model comparisons)

*Value Ranges:*
- f² in [0.01, 1.0] (realistic effect size range)
- sr² in [0.0, 0.5] (semi-partial correlation squared)
- Effect size CIs: ci_lower < effect_size < ci_upper

*Data Quality:*
- All effect sizes positive (appropriate for R² derivatives)
- Bootstrap CIs computed successfully
- Cohen classifications assigned appropriately

*Log Validation:*
- Required patterns: "Effect sizes computed", "Bootstrap complete: 1000 iterations", "Cohen classifications assigned"
- Forbidden patterns: "ERROR", "negative effect size", "bootstrap failed"

**Expected Behavior on Validation Failure:**
Raise error with effect size specifics, log to logs/step06_effect_sizes.log, quit immediately and invoke g_debug.

### Step 7: Cross-Validation Analysis
**Dependencies:** Step 6 (effect sizes computed)
**Complexity:** Medium (~8 minutes)

**Purpose:** Implement cross-validation to assess model generalization and detect overfitting

**Input:**
- data/step03_analysis_dataset.csv (complete analysis data)
- Model 2 specification from Step 4

**Processing:**
- Implement 5-fold cross-validation using sklearn.model_selection.KFold
- Random seed: 42 for reproducibility
- Shuffle: True (randomize before splitting)
- For each fold: fit Model 2 on training set (80%), evaluate on test set (20%)
- Compute cross-validation metrics:
  - Mean and SD of R² across folds
  - Mean and SD of RMSE across folds
  - Mean and SD of MAE across folds
- Check for overfitting: train-test R² difference > 0.10 indicates overfitting
- Compare CV R² to full-sample R² for generalization assessment

**Output:**
- data/step07_cross_validation.csv (CV metrics: R², RMSE, MAE by fold)
- data/step07_cv_summary.csv (mean, SD, and overfitting assessment)

**Validation Requirement:**
Validation tools MUST be used after cross-validation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_cross_validation.csv: 5 rows x 4 columns (fold, R2_train, R2_test, RMSE_test)
- data/step07_cv_summary.csv: 1 row x 6 columns (mean_R2, sd_R2, overfitting_flag, etc.)

*Value Ranges:*
- CV R² in [0.0, 0.8] (realistic cross-validation range)
- RMSE in [0.05, 0.20] (reasonable for HCE rate scale)
- Train-test gap in [-0.05, 0.15] (acceptable generalization)

*Data Quality:*
- All 5 folds completed successfully
- Consistent sample sizes across folds (19-21 per fold)
- Overfitting assessment completed

*Log Validation:*
- Required patterns: "Cross-validation complete: 5 folds", "Mean CV R²", "Overfitting check"
- Forbidden patterns: "ERROR", "fold failed", "convergence"

**Expected Behavior on Validation Failure:**
Raise error with CV specifics, log to logs/step07_cross_validation.log, quit immediately and invoke g_debug.

### Step 8: Power Analysis and Final Integration
**Dependencies:** Step 7 (cross-validation complete)
**Complexity:** Low (~5 minutes)

**Purpose:** Conduct post-hoc power analysis and integrate all results

**Input:**
- data/step06_effect_sizes.csv (observed effect sizes)
- Analysis parameters: N=100, alpha=0.000448 (Bonferroni corrected)

**Processing:**
- Post-hoc power analysis for hierarchical regression
- Given: N=100, 6 predictors total, alpha=0.000448 (Ch7 within-RQ correction)
- Calculate: achieved power for observed effect sizes
- Use: statsmodels.stats.power.FTestAnovaPower() or custom implementation
- Report: actual power for RPM effect and overall model
- Sensitivity analysis: minimum detectable f² at 80% power
- If power < 0.80: acknowledge limitation in interpretation
- Integrate key findings across all analysis steps
- Prepare summary of primary hypothesis test results

**Output:**
- data/step08_power_analysis.csv (achieved power, minimum detectable effects)
- data/step08_integrated_results.csv (key findings summary)
- data/step08_hypothesis_test_summary.txt (primary findings narrative)

**Validation Requirement:**
Validation tools MUST be used after power analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_power_analysis.csv: 4 rows x 4 columns (predictors, observed_f2, achieved_power, min_detectable_f2)
- data/step08_integrated_results.csv: 1 row x 10 columns (key statistics summary)
- data/step08_hypothesis_test_summary.txt: text file > 1000 characters

*Value Ranges:*
- Achieved power in [0.1, 1.0] (realistic power range)
- Minimum detectable f² in [0.05, 0.50] (sensitivity analysis)
- All integrated statistics consistent with prior steps

*Data Quality:*
- Power calculations completed for all cognitive predictors
- Sensitivity analysis provides meaningful thresholds
- Integrated results internally consistent

*Log Validation:*
- Required patterns: "Power analysis complete", "Integration successful", "Hypothesis test summary"
- Forbidden patterns: "ERROR", "power calculation failed", "inconsistent results"

**Expected Behavior on Validation Failure:**
Raise error with power analysis specifics, log to logs/step08_power_integration.log, quit immediately and invoke g_debug.

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (prerequisite validation)
- data/step01_hce_rates.csv (extracted HCE outcome data)
- data/step01_hce_descriptives.csv (HCE summary statistics)
- data/step02_cognitive_tests.csv (cognitive predictors with T-scores)
- data/step02_cognitive_correlations.csv (predictor intercorrelations)
- data/step03_analysis_dataset.csv (merged complete analysis data)
- data/step03_merge_summary.txt (merge validation results)
- data/step04_regression_models.csv (hierarchical model summaries)
- data/step04_coefficients.csv (coefficients with dual p-values)
- data/step04_model_comparison.csv (R² change and F-tests)
- data/step05_diagnostics.csv (assumption checks and VIF)
- data/step05_diagnostic_plots_data.csv (residual analysis data)
- data/step05_remedial_actions.txt (assumption violation responses)
- data/step06_effect_sizes.csv (f², sr², importance with CIs)
- data/step06_effect_interpretation.csv (Cohen classifications)
- data/step07_cross_validation.csv (5-fold CV results by fold)
- data/step07_cv_summary.csv (CV summary and overfitting check)
- data/step08_power_analysis.csv (achieved power and sensitivity)
- data/step08_integrated_results.csv (key findings summary)
- data/step08_hypothesis_test_summary.txt (primary results narrative)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_hce.log
- logs/step02_extract_cognitive.log
- logs/step03_merge_data.log
- logs/step04_regression.log
- logs/step05_diagnostics.log
- logs/step06_effect_sizes.log
- logs/step07_cross_validation.log
- logs/step08_power_integration.log

### Plots (EMPTY until rq_plots runs)
Note: Plot source data created in data/ folder with step##_*_plot_data.csv naming

### Results (EMPTY until rq_results runs)
Note: summary.md will be created by rq_results agent

---

## Expected Data Formats

### Step-to-Step Transformations
1. **Dependencies → HCE Data:** Ch6 HCE rates loaded and validated
2. **Master.xlsx → Cognitive:** Raw scores transformed to T-scores with standardization
3. **HCE + Cognitive → Analysis:** Complete merged dataset with all variables
4. **Analysis → Models:** Hierarchical regression with bootstrap CIs and dual p-values
5. **Models → Diagnostics:** Comprehensive assumption checking with remedial actions
6. **Diagnostics → Effects:** Effect sizes with bootstrap uncertainty quantification
7. **Effects → Validation:** Cross-validation for generalization assessment
8. **Validation → Integration:** Power analysis and final results summary

### Column Naming Conventions
- **UID:** Participant identifier (consistent across all files)
- **hce_rate:** Proportion of errors that were high-confidence (0-1 scale)
- **RAVLT_T, BVMT_T, RPM_T:** T-scored cognitive test variables (mean=50, SD=10)
- **Age_centered:** Age centered at sample mean
- **p_uncorrected, p_bonferroni, p_fdr:** Triple p-value reporting (Decision D068)

### Data Type Constraints
- **UIDs:** String/object type, no missing values
- **Rates/Proportions:** Float64, range [0,1], no missing values
- **T-scores:** Float64, approximately normal distribution
- **P-values:** Float64, range [0,1], no missing values
- **Effect sizes:** Float64, positive values for R²-based measures

---

## Cross-RQ Dependencies

**Primary Dependency:** Chapter 6 HCE analysis outputs

**Required Files:**
- Primary: results/ch6/6.6.1/data/step03_hce_rates.csv
- Alternative: results/ch6/6.6.*/data/*hce*.csv  
- Fallback: results/ch6/6.6.*/data/step*_high_confidence_errors.csv
- Expected content: Per-participant HCE rates (proportion scale)

**Master Data Dependency:**
- File: data/cache/master.xlsx
- Required columns: UID, RAVLT_total, BVMT_total, RPM_total, Age, Sex, Education
- Expected: Complete cognitive test data for N=100 participants

**Circuit Breaker:** If Ch6 HCE data not found, Step 0 will QUIT with dependency error

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
- **Files:** Dependency validation log
- **Ranges:** N/A (validation step)
- **Quality:** All required dependencies located
- **Logs:** Success confirmation patterns required

#### Step 1: Extract HCE Data  
- **Files:** HCE rates (100 x 2), descriptives (1 x 6)
- **Ranges:** HCE rate [0.05, 0.40], mean [0.15, 0.25]
- **Quality:** Complete data, no duplicates
- **Logs:** Load confirmation, no errors

#### Step 2: Extract Cognitive Data
- **Files:** Cognitive tests (100 x 10), correlations (3 x 3)
- **Ranges:** T-scores [25, 75], correlations [0.2, 0.8]  
- **Quality:** Successful T-score transformation
- **Logs:** Transformation success, no missing data

#### Step 3: Merge Analysis Dataset
- **Files:** Analysis dataset (100 x 8), merge summary
- **Ranges:** All previous ranges maintained
- **Quality:** 100 complete cases, successful merge
- **Logs:** Merge success confirmation

#### Step 4: Hierarchical Regression
- **Files:** Models, coefficients (6 x 8), comparisons
- **Ranges:** R² [0.05, 0.50], betas [-2, 2], p-values [0, 1]
- **Quality:** Bootstrap CIs valid, dual p-values present
- **Logs:** Model convergence, bootstrap completion

#### Step 5: Model Diagnostics
- **Files:** Diagnostics (6 x 4), plot data (100 x 4), remedial actions
- **Ranges:** VIF [1, 10], Cook's D [0, 0.20]
- **Quality:** All assumption tests completed
- **Logs:** Diagnostics success, assumption test completion

#### Step 6: Effect Sizes
- **Files:** Effect sizes (8 x 6), interpretations (2 x 4)
- **Ranges:** f² [0.01, 1.0], sr² [0.0, 0.5]
- **Quality:** Positive effect sizes, bootstrap CIs valid
- **Logs:** Effect size computation success, classification assignment

#### Step 7: Cross-Validation
- **Files:** CV results (5 x 4), CV summary (1 x 6)
- **Ranges:** CV R² [0.0, 0.8], RMSE [0.05, 0.20]
- **Quality:** All 5 folds successful, overfitting assessment
- **Logs:** CV completion, fold success confirmation

#### Step 8: Power Analysis
- **Files:** Power analysis (4 x 4), integrated results (1 x 10), summary text
- **Ranges:** Power [0.1, 1.0], min detectable f² [0.05, 0.50]
- **Quality:** Consistent integration, meaningful sensitivity
- **Logs:** Power calculation success, integration confirmation

---

## Summary

**Total Steps:** 9 (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** ~45 minutes
**Cross-RQ Dependencies:** Ch6 6.6.x HCE analysis + master.xlsx cognitive tests
**Primary Outputs:** Hierarchical regression results with comprehensive diagnostics and effect sizes
**Validation Coverage:** 100% (all 9 steps have 4-layer validation requirements)

**Key Hypothesis:** RPM (fluid intelligence) negatively predicts HCE rates (β < 0, p < 0.000448), while RAVLT/BVMT memory capacity tests do not significantly predict HCE rates.

**Critical Methodological Notes:**
- Random seed=42 used throughout for reproducibility
- Bootstrap CIs (1000 iterations) for all effect sizes and coefficients
- 5-fold cross-validation to assess generalization
- Comprehensive assumption checking with specified remedial actions
- Dual p-value reporting (uncorrected + Bonferroni + FDR) per Decision D068
- Chapter 7 multiple comparison correction: within-RQ Bonferroni alpha = 0.000448

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent with v5.1 statistical specifications