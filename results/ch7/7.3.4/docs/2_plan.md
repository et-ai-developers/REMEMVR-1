# Analysis Plan: RQ 7.3.4 - Does DASS predict metacognition more than memory?

**Research Question:** 7.3.4
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This analysis examines differential prediction patterns using DASS-21 scores (Depression, Anxiety, Stress) as predictors of three dependent variables: memory accuracy (theta scores), confidence scores, and calibration metrics. The core hypothesis tests whether anxiety/depression specifically impairs metacognitive monitoring (confidence, calibration) more than memory encoding (accuracy), reflecting domain-specific effects on executive monitoring rather than general memory deficits.

**Pipeline:** Multiple Linear Regression with Statistical Beta Coefficient Comparison
**Steps:** 9 total analysis steps (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** ~45 minutes

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Family-wise error control for cross-model comparisons
- Bootstrap confidence intervals for beta coefficient differences

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 theta scores and Ch6 confidence/calibration outputs exist before proceeding

**Input:**
- Primary: results/ch5/5.1.1/status.yaml (verify rq_results: success)
- Alternative: results/ch5/*/data/theta_all_scores.csv
- Fallback pattern: results/ch5/*/data/*theta*.{csv,txt}
- Primary: results/ch6/6.1.*/status.yaml (confidence analyses)
- Alternative: results/ch6/6.2.*/data/calibration_scores.csv
- Expected: Participant-level theta scores and confidence/calibration metrics
- Master file: data/cache/master.xlsx (DASS-21 scores)

**Processing:**
- Check Ch5 completion status (any theta estimation RQ)
- Verify Ch6 confidence and calibration analyses completed
- Locate theta scores file (aggregate across What/Where/When domains)
- Locate confidence and calibration scores files
- Verify master.xlsx accessible for DASS extraction
- Test file readability and basic format validation
- Log all dependency validation results

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with dependency status
- Contains: 5-6 dependency checks (Ch5, Ch6, master.xlsx paths)

*Value Ranges:*
- Check results: PASS/FAIL status for each dependency
- File sizes: > 0 bytes for located files
- Expected participants: ~100 for theta, ~100 for confidence, ~97 for DASS

*Data Quality:*
- All required source RQs completed (status = success)
- Source files readable and non-empty
- No critical missing dependencies

*Log Validation:*
- Required patterns: "DEPENDENCY CHECK", "Ch5 theta: PASS", "Ch6 confidence: PASS", "DASS available: PASS"
- Forbidden patterns: "CRITICAL FAILURE", "FILE NOT FOUND", "DEPENDENCY MISSING"
- Acceptable warnings: "Alternative path used", "File pattern matched"

**Expected Behavior on Validation Failure:**
- Quit with specific missing dependency error
- Log to logs/step00_validate_dependencies.log
- Invoke g_debug for dependency resolution

### Step 1: Extract and Merge Analysis Datasets
**Dependencies:** Step 0 (validated dependencies)
**Complexity:** Medium (~8 minutes including data quality checks)

**Purpose:** Extract DASS-21 scores from master.xlsx and merge with Ch5 theta scores and Ch6 confidence/calibration scores

**Input:**
- data/cache/master.xlsx: DASS-21 Depression, Anxiety, Stress subscales
- Ch5 theta file: results/ch5/5.1.1/data/step03_theta_scores.csv (or equivalent)
- Ch6 confidence file: results/ch6/6.1.*/data/confidence_scores.csv
- Ch6 calibration file: results/ch6/6.2.*/data/calibration_scores.csv

**Processing:**
- Extract DASS-21 scores from master.xlsx:
  - DASS_Depression: sum of 7 depression items * 2 (standard scoring)
  - DASS_Anxiety: sum of 7 anxiety items * 2 (standard scoring)
  - DASS_Stress: sum of 7 stress items * 2 (standard scoring)
- Load theta scores (omnibus memory accuracy measure)
- Load confidence scores (mean confidence per participant)
- Load calibration scores (confidence-accuracy correlation or gamma)
- Merge datasets on participant UID
- Handle missing data:
  - Complete case analysis (participants with all measures)
  - Document missingness patterns by variable
  - Expected N ~97 after DASS missingness exclusion
- Compute descriptive statistics for all variables
- Check DASS intercorrelations (expected r > 0.70 between subscales)

**Output:**
- data/step01_dass_scores.csv (extracted DASS subscales)
- data/step02_merged_dataset.csv (complete analysis dataset)
- data/step02_descriptive_stats.csv (means, SDs, correlations)

**Validation Requirement:**
Validation tools MUST be used after data extraction and merging.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_dass_scores.csv: ~97 rows x 4 columns (UID, DASS_Dep, DASS_Anx, DASS_Str)
- data/step02_merged_dataset.csv: ~97 rows x 7 columns (UID, theta, confidence, calibration, DASS_Dep, DASS_Anx, DASS_Str)
- data/step02_descriptive_stats.csv: summary statistics table

*Value Ranges:*
- DASS scores: 0-42 per subscale (standard DASS-21 range)
- Theta scores: [-3, 3] (IRT ability scale)
- Confidence: [0, 100] (percentage confidence scale)
- Calibration: [-1, 1] (correlation coefficient range)

*Data Quality:*
- Final N between 90-100 participants (after missingness exclusion)
- No missing values in merged dataset (complete case analysis)
- DASS intercorrelations > 0.60 (expected multicollinearity)
- All variables show reasonable variance (SD > 0)

*Log Validation:*
- Required patterns: "DASS extraction complete", "Merge successful", "N = [90-100] complete cases"
- Forbidden patterns: "ERROR", "MERGE FAILED", "No participants remaining"
- Acceptable warnings: "Missing data detected", "High DASS intercorrelations"

**Expected Behavior on Validation Failure:**
- Quit if N < 90 participants
- Log detailed missingness report
- Invoke g_debug for data quality issues

### Step 2: Fit Multiple Regression Models for Differential Prediction
**Dependencies:** Step 1 (merged analysis dataset)
**Complexity:** Medium (~10 minutes including diagnostics)

**Purpose:** Fit three separate regression models to test differential prediction hypothesis

**Input:**
- data/step02_merged_dataset.csv

**Processing:**
- Fit three regression models using statsmodels.api.OLS:
  - Model_Accuracy: theta ~ DASS_Dep + DASS_Anx + DASS_Str
  - Model_Confidence: confidence ~ DASS_Dep + DASS_Anx + DASS_Str
  - Model_Calibration: calibration ~ DASS_Dep + DASS_Anx + DASS_Str
- Extract standardized beta coefficients (using standardized predictors)
- Compute model fit statistics: R², adjusted R², F-statistic, AIC, BIC
- For each model, check basic assumptions:
  - Multicollinearity: VIF < 5 for each predictor
  - Normality: Shapiro-Wilk test on residuals (p > 0.05)
  - Homoscedasticity: Breusch-Pagan test (p > 0.05)
  - Independence: Durbin-Watson statistic (~2.0 expected)
  - Linearity: Partial residual plots (visual inspection)
  - Outliers: Cook's D < 4/N threshold
- Remedial actions if assumptions violated:
  - Multicollinearity VIF > 5: Document correlation structure, consider principal components
  - Normality p < 0.05: Use bootstrap CIs (1000 iterations, seed=42)
  - Heteroscedasticity p < 0.05: Report HC3 robust standard errors
  - Independence DW < 1.5 or > 2.5: Report clustered standard errors
  - Outliers Cook's D > 4/N: Report results with and without outliers

**Output:**
- data/step02_model_accuracy.csv (Model 1 results)
- data/step02_model_confidence.csv (Model 2 results)
- data/step02_model_calibration.csv (Model 3 results)
- data/step02_model_diagnostics.csv (assumption tests for all models)

**Validation Requirement:**
Validation tools MUST be used after model fitting and diagnostics.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_model_accuracy.csv: 3 rows x 8 columns (predictor, beta, se, t, p, ci_lower, ci_upper, vif)
- data/step02_model_confidence.csv: 3 rows x 8 columns (same structure)
- data/step02_model_calibration.csv: 3 rows x 8 columns (same structure)
- data/step02_model_diagnostics.csv: 3 rows x 6 columns (model, normality_p, homoscedasticity_p, dw_stat, outliers_n, remedial_actions)

*Value Ranges:*
- Beta coefficients: [-2, 2] (standardized predictors)
- Standard errors: > 0 (positive values)
- t-statistics: [-10, 10] (reasonable range for N~97)
- p-values: [0, 1] (valid probability range)
- VIF values: [1, 10] (multicollinearity check)
- R²: [0, 1] (proportion variance explained)

*Data Quality:*
- All three models converge successfully
- No NaN or infinite values in parameter estimates
- VIF values flagged if > 5 but < 10 (manageable multicollinearity)
- Diagnostic tests completed for all assumptions

*Log Validation:*
- Required patterns: "Model fitting complete", "Diagnostics complete", "3 models converged"
- Forbidden patterns: "CONVERGENCE FAILED", "SINGULAR MATRIX", "NaN parameters"
- Acceptable warnings: "High VIF detected", "Assumption violation detected"

**Expected Behavior on Validation Failure:**
- Log specific convergence or diagnostic failures
- Report assumption violations with remedial actions
- Continue with available results if 2+ models succeed

### Step 3: Statistical Comparison of Beta Coefficients Across Models
**Dependencies:** Step 2 (fitted regression models)
**Complexity:** High (~12 minutes including bootstrap)

**Purpose:** Test differential prediction hypothesis by statistically comparing DASS_Anxiety coefficients across accuracy, confidence, and calibration models

**Input:**
- data/step02_model_accuracy.csv
- data/step02_model_confidence.csv
- data/step02_model_calibration.csv
- data/step02_merged_dataset.csv (for bootstrap)

**Processing:**
- Extract DASS_Anxiety standardized beta coefficients from all three models
- Primary comparison: Test H0: β_Anxiety(Confidence) = β_Anxiety(Accuracy)
- Secondary comparison: Test H0: β_Anxiety(Calibration) = β_Anxiety(Accuracy)
- Statistical method: Bootstrap confidence intervals for beta differences
  - Bootstrap implementation: Participant-level block bootstrap
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - For each iteration:
    - Resample participants WITH replacement
    - Refit all three models on bootstrap sample
    - Compute beta coefficient differences (Confidence - Accuracy, Calibration - Accuracy)
  - CI computation: percentile method (2.5th, 97.5th percentiles for 95% CI)
- Multiple comparison correction:
  - Family: Cross-model comparisons (2 primary comparisons)
  - Bonferroni: alpha = 0.05/2 = 0.025 per comparison
  - Also compute FDR-adjusted p-values using Benjamini-Hochberg
  - Report BOTH uncorrected AND corrected intervals (Decision D068)
- Effect size interpretation:
  - Small difference: |Δβ| < 0.10
  - Medium difference: |Δβ| 0.10-0.30
  - Large difference: |Δβ| > 0.30

**Output:**
- data/step03_beta_comparisons.csv (statistical tests of differences)
- data/step03_bootstrap_results.csv (1000 bootstrap iterations)
- data/step03_differential_prediction.csv (final hypothesis test results)

**Validation Requirement:**
Validation tools MUST be used after beta coefficient comparison testing.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_beta_comparisons.csv: 2 rows x 8 columns (comparison, diff_estimate, ci_lower, ci_upper, p_uncorrected, p_bonferroni, p_fdr, effect_size)
- data/step03_bootstrap_results.csv: 1000 rows x 3 columns (iteration, diff_conf_acc, diff_cal_acc)
- data/step03_differential_prediction.csv: summary table with final conclusions

*Value Ranges:*
- Beta differences: [-1, 1] (reasonable range for standardized coefficients)
- Bootstrap differences: similar distribution across 1000 iterations
- p-values: [0, 1] (valid probability range)
- Effect sizes: categorical (small/medium/large)

*Data Quality:*
- Bootstrap completed 1000 iterations successfully
- No extreme outliers in bootstrap distribution (> 3 SD from median)
- Confidence intervals exclude infinity or NaN values
- Effect size categories correctly assigned

*Log Validation:*
- Required patterns: "Bootstrap complete: 1000 iterations", "Beta comparison testing complete", "Differential prediction results"
- Forbidden patterns: "BOOTSTRAP FAILED", "INFINITE VALUES", "CI computation error"
- Acceptable warnings: "Wide confidence intervals", "Non-significant difference detected"

**Expected Behavior on Validation Failure:**
- Report specific bootstrap or CI computation failures
- Log problematic iterations if bootstrap fails partially
- Provide fallback analysis with available iterations

### Step 4: Control for Cognitive Ability (Hierarchical Regression)
**Dependencies:** Step 3 (beta comparison results)
**Complexity:** Medium (~8 minutes)

**Purpose:** Test whether DASS differential effects remain significant when controlling for general cognitive ability

**Input:**
- data/step02_merged_dataset.csv
- data/cache/master.xlsx (RAVLT and RPM T-scores)

**Processing:**
- Extract cognitive ability measures from master.xlsx:
  - RAVLT_T: T-scored verbal memory (mean=50, SD=10)
  - RPM_T: T-scored non-verbal reasoning (mean=50, SD=10)
- Merge with existing analysis dataset
- Fit hierarchical regression models:
  - Step 1: theta ~ DASS_Dep + DASS_Anx + DASS_Str
  - Step 2: theta ~ DASS_Dep + DASS_Anx + DASS_Str + RAVLT_T + RPM_T
  - Repeat for confidence and calibration models
- Compute incremental R² (ΔR²) for DASS predictors beyond cognitive ability
- Test significance of ΔR² using F-test:
  - H0: ΔR² = 0 (no incremental validity)
  - Use standard F-change test with appropriate df
- Effect size interpretation:
  - Small ΔR²: < 0.02
  - Medium ΔR²: 0.02-0.13
  - Large ΔR²: > 0.13

**Output:**
- data/step04_hierarchical_accuracy.csv (hierarchical results for accuracy)
- data/step04_hierarchical_confidence.csv (hierarchical results for confidence)
- data/step04_hierarchical_calibration.csv (hierarchical results for calibration)
- data/step04_incremental_validity.csv (ΔR² and significance tests)

**Validation Requirement:**
Validation tools MUST be used after hierarchical regression analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_hierarchical_accuracy.csv: 2 rows x 7 columns (step, predictors, R2, adj_R2, delta_R2, F_change, p_change)
- data/step04_hierarchical_confidence.csv: same structure
- data/step04_hierarchical_calibration.csv: same structure
- data/step04_incremental_validity.csv: 3 rows x 5 columns (model, delta_R2, F_change, p_change, effect_size)

*Value Ranges:*
- R²: [0, 1] (proportion variance explained)
- ΔR²: [0, 0.5] (incremental variance, bounded by total)
- F-statistics: > 0 (positive test statistics)
- p-values: [0, 1] (valid probability range)

*Data Quality:*
- All hierarchical models converge
- ΔR² values non-negative (Step 2 R² ≥ Step 1 R²)
- Cognitive ability measures available for analysis participants
- No missing data after cognitive ability merge

*Log Validation:*
- Required patterns: "Hierarchical regression complete", "Incremental validity tested", "Cognitive controls included"
- Forbidden patterns: "HIERARCHICAL FAILED", "MISSING COGNITIVE DATA", "NEGATIVE DELTA R2"
- Acceptable warnings: "Small incremental validity", "Non-significant F-change"

**Expected Behavior on Validation Failure:**
- Report specific hierarchical model failures
- Document cognitive ability data availability issues
- Proceed with available models if partial success

### Step 5: Cross-Validation Assessment
**Dependencies:** Step 4 (hierarchical regression results)
**Complexity:** Medium (~10 minutes including all model variants)

**Purpose:** Assess generalizability of differential prediction findings using cross-validation

**Input:**
- data/step02_merged_dataset.csv (with cognitive controls)

**Processing:**
- Implement 5-fold cross-validation using sklearn.model_selection.KFold
- Random seed: 42 for reproducibility
- Shuffle: True (randomize before splitting)
- Stratification: Use quantile-based stratification on continuous outcomes
- For each fold:
  - Training set: 80% of participants (fit models)
  - Test set: 20% of participants (evaluate predictions)
  - Fit all three models (accuracy, confidence, calibration)
  - Compute test set predictions and performance metrics
- Cross-validation metrics:
  - R²_test: proportion variance explained on test set
  - RMSE: root mean square error
  - MAE: mean absolute error
  - Compute mean and standard deviation across 5 folds
- Overfitting assessment:
  - Generalization gap: R²_train - R²_test
  - Flag if gap > 0.10 (substantial overfitting)
- Bootstrap cross-validation:
  - Iterations: 100 (reduced for computational efficiency)
  - Random seed: 42
  - Compute 95% CI for CV performance metrics

**Output:**
- data/step05_cv_results.csv (cross-validation performance metrics)
- data/step05_cv_folds.csv (detailed results by fold)
- data/step05_overfitting_assessment.csv (generalization gap analysis)

**Validation Requirement:**
Validation tools MUST be used after cross-validation analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_cv_results.csv: 3 rows x 8 columns (model, cv_R2_mean, cv_R2_sd, cv_RMSE_mean, cv_RMSE_sd, cv_MAE_mean, cv_MAE_sd, generalization_gap)
- data/step05_cv_folds.csv: 15 rows x 5 columns (model, fold, train_R2, test_R2, test_RMSE)
- data/step05_overfitting_assessment.csv: summary of generalization findings

*Value Ranges:*
- CV R²: [0, 1] (cross-validated R-squared)
- RMSE: > 0 (positive error metric)
- MAE: > 0 (positive error metric)
- Generalization gap: [-0.2, 0.4] (reasonable range for small sample)

*Data Quality:*
- All 5 folds complete successfully
- No NaN values in CV metrics
- Standard deviations reasonable (not excessive variation across folds)
- Generalization gaps within expected range (< 0.20)

*Log Validation:*
- Required patterns: "Cross-validation complete: 5 folds", "CV metrics computed", "Generalization assessment complete"
- Forbidden patterns: "CV FAILED", "FOLD ERROR", "INFINITE CV METRICS"
- Acceptable warnings: "High CV variation", "Overfitting detected"

**Expected Behavior on Validation Failure:**
- Report specific CV fold failures
- Provide results for successful folds if partial completion
- Flag overfitting concerns for interpretation

### Step 6: Power Analysis and Effect Size Estimation
**Dependencies:** Step 5 (cross-validation complete)
**Complexity:** Medium (~8 minutes including sensitivity analysis)

**Purpose:** Conduct post-hoc power analysis and estimate effect sizes for differential prediction tests

**Input:**
- data/step03_differential_prediction.csv
- data/step04_incremental_validity.csv

**Processing:**
- Post-hoc power analysis for hierarchical regression:
  - Given: N~97, up to 5 predictors, alpha=0.05 (within-RQ family)
  - Multiple comparison adjustment: alpha = 0.05/2 = 0.025 for main comparisons
  - Calculate achieved power for observed ΔR² values
  - Use statsmodels.stats.power.FTestAnovaPower()
- Sensitivity analysis:
  - Compute minimum detectable ΔR² at 80% power
  - Given current sample size and design
  - Report whether study adequately powered for medium effects (ΔR² = 0.13)
- Cohen's f² calculation for each model:
  - f² = R² / (1 - R²)
  - Interpretation: small (0.02), medium (0.15), large (0.35)
- Bootstrap confidence intervals for effect sizes:
  - Iterations: 1000
  - Random seed: 42
  - Bootstrap f² and ΔR² estimates
  - 95% CI using percentile method
- Power curves:
  - Plot achieved power across range of effect sizes
  - Mark observed effect sizes and 80% power threshold

**Output:**
- data/step06_power_analysis.csv (achieved power for observed effects)
- data/step06_effect_sizes.csv (Cohen's f² with confidence intervals)
- data/step06_sensitivity_analysis.csv (minimum detectable effects)

**Validation Requirement:**
Validation tools MUST be used after power and effect size analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_power_analysis.csv: 6 rows x 5 columns (test, effect_size, power, alpha_used, sufficient_power)
- data/step06_effect_sizes.csv: 3 rows x 6 columns (model, cohens_f2, ci_lower, ci_upper, interpretation, bootstrap_se)
- data/step06_sensitivity_analysis.csv: 1 row x 4 columns (min_detectable_deltaR2, power_80pct, current_N, adequate_power)

*Value Ranges:*
- Power: [0, 1] (probability values)
- Cohen's f²: [0, 2] (effect size metric)
- Minimum detectable effects: [0, 0.5] (proportion variance)
- Bootstrap SE: > 0 (positive standard errors)

*Data Quality:*
- Power calculations complete for all tests
- Effect sizes computed for all models
- Bootstrap iterations complete (1000)
- Interpretive categories correctly assigned

*Log Validation:*
- Required patterns: "Power analysis complete", "Effect sizes computed", "Sensitivity analysis complete"
- Forbidden patterns: "POWER CALCULATION FAILED", "EFFECT SIZE ERROR", "BOOTSTRAP INCOMPLETE"
- Acceptable warnings: "Low power detected", "Large effect size"

**Expected Behavior on Validation Failure:**
- Report power calculation errors
- Provide partial results if some analyses succeed
- Document limitations in effect size interpretation

### Step 7: Final Model Summary and Interpretation
**Dependencies:** Step 6 (power analysis complete)
**Complexity:** Low (~5 minutes)

**Purpose:** Synthesize all analysis results into final interpretable summary

**Input:**
- data/step03_differential_prediction.csv
- data/step04_incremental_validity.csv
- data/step05_cv_results.csv
- data/step06_power_analysis.csv

**Processing:**
- Create comprehensive results summary:
  - Primary hypothesis test: DASS_Anxiety differential prediction
  - Effect sizes and confidence intervals
  - Statistical significance (dual p-values per Decision D068)
  - Incremental validity beyond cognitive ability
  - Cross-validation generalizability
  - Power and sensitivity analysis
- Generate interpretation framework:
  - Support for differential prediction hypothesis
  - Magnitude of effects (small/medium/large)
  - Practical significance assessment
  - Limitations and caveats
- Key findings summary:
  - Whether DASS_Anxiety more strongly predicts metacognition vs memory
  - Robustness to cognitive ability controls
  - Generalizability evidence from cross-validation
  - Adequacy of statistical power
- Prepare thesis-ready summary text

**Output:**
- data/step07_final_results_summary.csv (comprehensive findings table)
- results/dass_differential_prediction_summary.md (text interpretation for thesis)

**Validation Requirement:**
Validation tools MUST be used after final summary generation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_final_results_summary.csv: comprehensive table with all key statistics
- results/dass_differential_prediction_summary.md: formatted text summary (>500 words)

*Value Ranges:*
- All statistics within expected ranges from prior steps
- Interpretations consistent with statistical findings
- Effect size interpretations accurate per Cohen conventions

*Data Quality:*
- Summary includes all major analysis components
- No contradictory interpretations
- Statistical reporting follows APA format conventions
- Limitations appropriately acknowledged

*Log Validation:*
- Required patterns: "Final summary complete", "Interpretation generated", "Results synthesis complete"
- Forbidden patterns: "SUMMARY ERROR", "INTERPRETATION MISSING"
- Acceptable warnings: "Null findings reported", "Low power acknowledged"

**Expected Behavior on Validation Failure:**
- Report specific summary generation errors
- Ensure core results are preserved
- Flag incomplete synthesis for review

### Step 8: Generate Plot Data for Visualization
**Dependencies:** Step 7 (final summary complete)
**Complexity:** Low (~5 minutes)

**Purpose:** Prepare data for publication-quality plots showing differential prediction patterns

**Input:**
- data/step02_model_accuracy.csv
- data/step02_model_confidence.csv  
- data/step02_model_calibration.csv
- data/step03_bootstrap_results.csv

**Processing:**
- Create plot data for beta coefficient comparison:
  - Extract DASS_Anxiety betas and confidence intervals from all models
  - Format for side-by-side comparison plot
  - Include both uncorrected and corrected confidence intervals
- Create plot data for bootstrap distributions:
  - Histogram data for beta difference distributions
  - Mark observed differences and confidence intervals
  - Include effect size thresholds for interpretation
- Create plot data for model performance comparison:
  - R² values with confidence intervals for all models
  - Cross-validation performance metrics
  - Effect sizes with interpretation benchmarks
- Format all plot data according to REMEMVR plotting conventions:
  - Standardized column names
  - Color coding specifications
  - Statistical annotation data

**Output:**
- data/step08_beta_comparison_plot_data.csv
- data/step08_bootstrap_distributions_plot_data.csv
- data/step08_model_performance_plot_data.csv

**Validation Requirement:**
Validation tools MUST be used after plot data generation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_beta_comparison_plot_data.csv: formatted for side-by-side beta plot
- data/step08_bootstrap_distributions_plot_data.csv: histogram data for 1000 bootstrap iterations
- data/step08_model_performance_plot_data.csv: model comparison metrics

*Value Ranges:*
- All values consistent with previous analysis steps
- Plot formatting variables correctly specified
- Color and aesthetic mappings valid

*Data Quality:*
- All plot data files complete
- No missing values in key plotting variables
- Formatting consistent with REMEMVR conventions
- Statistical annotations accurately transferred

*Log Validation:*
- Required patterns: "Plot data generation complete", "Formatting validated"
- Forbidden patterns: "PLOT DATA ERROR", "FORMATTING FAILED"
- Acceptable warnings: None expected for this step

**Expected Behavior on Validation Failure:**
- Report specific plot data generation errors
- Ensure core visualization data preserved
- Document formatting issues for correction

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt: Prerequisite verification
- data/step01_dass_scores.csv: Extracted DASS-21 subscales 
- data/step02_merged_dataset.csv: Complete analysis dataset (~97 participants)
- data/step02_model_accuracy.csv: Accuracy model results (3 predictors)
- data/step02_model_confidence.csv: Confidence model results (3 predictors)
- data/step02_model_calibration.csv: Calibration model results (3 predictors)
- data/step02_model_diagnostics.csv: Assumption tests for all models
- data/step02_descriptive_stats.csv: Variable descriptives and correlations
- data/step03_beta_comparisons.csv: Statistical tests of coefficient differences
- data/step03_bootstrap_results.csv: Bootstrap iterations (1000 x 2 comparisons)
- data/step03_differential_prediction.csv: Primary hypothesis test results
- data/step04_hierarchical_accuracy.csv: Hierarchical regression for accuracy
- data/step04_hierarchical_confidence.csv: Hierarchical regression for confidence
- data/step04_hierarchical_calibration.csv: Hierarchical regression for calibration
- data/step04_incremental_validity.csv: ΔR² tests beyond cognitive ability
- data/step05_cv_results.csv: Cross-validation performance metrics
- data/step05_cv_folds.csv: Detailed results by fold (5-fold CV)
- data/step05_overfitting_assessment.csv: Generalization gap analysis
- data/step06_power_analysis.csv: Post-hoc power for observed effects
- data/step06_effect_sizes.csv: Cohen's f² with confidence intervals
- data/step06_sensitivity_analysis.csv: Minimum detectable effects
- data/step07_final_results_summary.csv: Comprehensive findings table
- data/step08_beta_comparison_plot_data.csv: Plot data for coefficient comparison
- data/step08_bootstrap_distributions_plot_data.csv: Plot data for bootstrap distributions
- data/step08_model_performance_plot_data.csv: Plot data for model comparison

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log: Dependency check execution
- logs/step01_extract_merge_data.log: Data extraction and merging
- logs/step02_fit_regression_models.log: Model fitting and diagnostics
- logs/step03_compare_beta_coefficients.log: Statistical comparisons with bootstrap
- logs/step04_hierarchical_regression.log: Cognitive ability controls
- logs/step05_cross_validation.log: CV analysis execution
- logs/step06_power_effect_sizes.log: Power analysis and effect size computation
- logs/step07_final_summary.log: Results synthesis
- logs/step08_generate_plot_data.log: Plot data generation

### Plots (EMPTY until rq_plots runs)
Plot source data created in data/ with step08_*_plot_data.csv files

### Results (EMPTY until rq_results runs)
results/dass_differential_prediction_summary.md created in Step 7

---

## Expected Data Formats

### Step-to-Step Transformations
1. **Step 0→1:** Dependency validation → DASS extraction from master.xlsx
2. **Step 1→2:** Individual datasets → merged analysis dataset with complete cases
3. **Step 2→3:** Individual model results → beta coefficient comparisons with bootstrap
4. **Step 3→4:** Basic models → hierarchical models with cognitive controls
5. **Step 4→5:** Single-sample results → cross-validated performance metrics
6. **Step 5→6:** Cross-validation → power analysis and effect size estimation
7. **Step 6→7:** Individual analyses → integrated summary and interpretation
8. **Step 7→8:** Final results → formatted plot data for visualization

### Column Naming Conventions
- **Participant ID:** UID (consistent across all datasets)
- **DASS scores:** DASS_Dep, DASS_Anx, DASS_Str (standardized naming)
- **Outcomes:** theta (accuracy), confidence, calibration
- **Cognitive controls:** RAVLT_T, RPM_T (T-scored measures)
- **Model results:** beta, se, t, p, ci_lower, ci_upper, vif (standard regression output)
- **Cross-validation:** cv_R2_mean, cv_R2_sd, generalization_gap
- **Effect sizes:** cohens_f2, delta_R2, effect_size_interpretation

### Data Type Constraints
- **Numeric measures:** float64 (theta, DASS scores, betas, effect sizes)
- **Count measures:** int64 (N, fold numbers, iteration numbers)
- **Categorical measures:** object/string (effect_size_interpretation, model names)
- **p-values:** float64 in range [0, 1]
- **Confidence intervals:** float64 with ci_lower < ci_upper
- **Missing data:** Complete case analysis (no NaN in final merged dataset)

---

## Cross-RQ Dependencies

### Primary Dependencies
- **Ch5 Theta Scores:** Omnibus memory accuracy measure (theta_all)
  - Required: Any Ch5 RQ producing overall theta estimates
  - Primary path: results/ch5/5.1.1/data/step03_theta_scores.csv
  - Alternative paths: results/ch5/*/data/*theta*all*.csv
  - Fallback: Any file matching results/ch5/*/data/*theta*.csv
- **Ch6 Confidence Scores:** Mean confidence per participant
  - Required: Any Ch6.1.x RQ producing confidence measures
  - Primary path: results/ch6/6.1.*/data/confidence_scores.csv
  - Alternative: results/ch6/*/data/*confidence*.csv
- **Ch6 Calibration Scores:** Metacognitive calibration metrics
  - Required: Any Ch6.2.x RQ producing calibration measures  
  - Primary path: results/ch6/6.2.*/data/calibration_scores.csv
  - Alternative: results/ch6/*/data/*calibration*.csv

### Master Data Dependencies
- **DASS-21 Scores:** From master.xlsx clinical measures
  - Path: data/cache/master.xlsx
  - Required sheets/columns: DASS-21 items (21 total items)
  - Expected: ~97 participants with complete DASS data

### Dependency Validation Strategy
- Step 0 validates ALL dependencies before proceeding
- Multiple path patterns attempted for each dependency
- Clear error messages if critical dependencies missing
- Graceful degradation if some dependencies partially available

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
**Validation Tools:** File existence, format validation, data quality checks
**4-Layer Structure:** As specified above with dependency-specific criteria

#### Step 1: Extract and Merge Data  
**Validation Tools:** Data integrity, missing data assessment, range validation
**4-Layer Structure:** As specified above with data quality criteria

#### Step 2: Fit Regression Models
**Validation Tools:** Model convergence, assumption validation, parameter reasonableness
**4-Layer Structure:** As specified above with regression-specific criteria

#### Step 3: Compare Beta Coefficients
**Validation Tools:** Statistical test validation, bootstrap assessment, effect size verification
**4-Layer Structure:** As specified above with comparison-specific criteria

#### Step 4: Hierarchical Regression
**Validation Tools:** Hierarchical model validation, incremental validity assessment
**4-Layer Structure:** As specified above with hierarchical-specific criteria

#### Step 5: Cross-Validation
**Validation Tools:** CV performance validation, overfitting assessment, metric verification
**4-Layer Structure:** As specified above with CV-specific criteria

#### Step 6: Power and Effect Size Analysis
**Validation Tools:** Power calculation validation, effect size verification, sensitivity analysis
**4-Layer Structure:** As specified above with power-specific criteria

#### Step 7: Final Summary
**Validation Tools:** Summary completeness, interpretation consistency, result synthesis
**4-Layer Structure:** As specified above with summary-specific criteria

#### Step 8: Plot Data Generation
**Validation Tools:** Plot data format validation, visualization readiness assessment
**4-Layer Structure:** As specified above with plot-specific criteria

---

## Summary

**Total Steps:** 9 (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** ~45 minutes
**Cross-RQ Dependencies:** Ch5 theta scores, Ch6 confidence and calibration scores, master.xlsx DASS
**Primary Outputs:** Statistical test of differential prediction hypothesis with comprehensive validation
**Validation Coverage:** 100% (all 9 steps have 4-layer validation requirements)

**Key Hypothesis:** DASS-Anxiety more strongly predicts metacognitive measures (confidence, calibration) than memory accuracy, reflecting domain-specific executive monitoring impairment rather than general memory deficits.

**Critical Methodological Notes:**
- Bootstrap confidence intervals address statistical comparison of regression coefficients across models
- Hierarchical entry controls for general cognitive ability confound
- Cross-validation assesses generalizability of differential prediction findings  
- Multiple comparison corrections applied for cross-model statistical tests
- Power analysis documents adequacy of sample size for detecting medium effects
- Complete assumption testing with specified remedial actions for violations

**Statistical Enhancements (v5.1):**
- Random seed=42 for all randomized procedures (bootstrap, cross-validation)
- Specific iteration counts (1000 bootstrap, 100 bootstrap CV, 5-fold CV)
- Comprehensive remedial actions for assumption violations
- Dual p-value reporting per Decision D068
- Family-wise error control for multiple comparisons

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan → creates 3_tools.yaml
3. rq_analysis reads plan + tools → creates 4_analysis.yaml
4. g_code reads analysis → generates executable code

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent with v5.1 statistical enhancements