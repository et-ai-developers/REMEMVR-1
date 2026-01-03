# Analysis Plan: RQ 7.1.1 - Do cognitive tests predict overall REMEMVR ability?

**Research Question:** 7.1.1
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This analysis examines the predictive relationship between four standardized cognitive tests and overall episodic memory ability as measured by REMEMVR theta scores. The approach tests convergent validity between traditional neuropsychological measures and VR-based episodic memory assessment.

**Pipeline:** Multiple Linear Regression with comprehensive assumption checking
**Steps:** 9 total analysis steps (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** ~45 minutes

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Chapter 7 alpha adjustment: 0.05/28 = 0.00179 for family-wise error control

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies

**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (~3 minutes)

**Purpose:** Verify required Ch5 outputs exist and cognitive test data accessible before proceeding

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv (IRT theta estimates)
- Alternative: results/ch5/5.1.1/data/*theta*.{csv,txt}
- Fallback: results/ch5/5.1.1/data/step*theta*.csv
- Expected content: Participant-level theta scores across 4 test sessions
- Also check: master.xlsx accessibility for cognitive test data
- Verify: results/ch5/5.1.1/status.yaml shows rq_results = success

**Processing:**
- Check Ch5 5.1.1 completion status in status.yaml
- Search for theta score files using multiple patterns
- Verify theta file contains 100 participants x 4 sessions
- Check master.xlsx file exists and is readable
- Validate cognitive test columns present in master.xlsx
- Log all dependency validation results

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Should contain: file paths checked, existence status, participant counts

*Value Ranges:*
- Participant count should equal 100
- Session count should equal 4 (if theta file structured by session)
- File sizes should be >0 bytes

*Data Quality:*
- All required input files exist and are accessible
- No corrupted or empty files
- Theta file contains expected participant UIDs

*Log Validation:*
- Required patterns: "VALIDATION COMPLETE", "Dependencies verified"
- Required patterns: "Ch5 5.1.1 status: success", "master.xlsx accessible"
- Forbidden patterns: "ERROR", "FILE NOT FOUND", "DEPENDENCY MISSING"

**Expected Behavior on Validation Failure:**
Raise error with specific missing dependency and quit immediately

### Step 1: Extract and Prepare Cognitive Test Data

**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (~5 minutes)

**Purpose:** Extract cognitive test scores from master.xlsx and standardize to T-scores (M=50, SD=10)

**Input:**
- master.xlsx (cognitive test raw scores)
- Expected columns: RAVLT_Total, BVMT_TotR, NART_EstIQ, RPM_Total

**Processing:**
- Extract cognitive test raw scores for all 100 participants
- Compute derived scores: RAVLT_Total = sum of T1-T5 trials if needed
- Convert all tests to T-scores using sample statistics:
  - T-score = 50 + 10 * ((raw_score - sample_mean) / sample_sd)
  - Implementation: tools.analysis_regression.standardize_predictors()
- Handle missing data: exclude participants with missing cognitive tests
- Create participant-level dataset with UID and T-scored predictors
- Verify T-score distributions: mean ~= 50, sd ~= 10

**Output:**
- data/step01_cognitive_tests.csv (T-scored cognitive test data)

**Validation Requirement:**
Validation tools MUST be used after cognitive test extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_cognitive_tests.csv: ~100 rows x 5 columns
- Columns: UID (object), RAVLT_T (float64), BVMT_T (float64), NART_T (float64), RPM_T (float64)

*Value Ranges:*
- T-scores approximately in range [25, 75] (within 2.5 SDs)
- Sample means approximately 50 +/- 2.0
- Sample standard deviations approximately 10 +/- 1.5

*Data Quality:*
- 90-100 participants with complete cognitive test data
- No negative T-scores or extreme outliers (T > 100 or T < 0)
- No duplicate UIDs

*Log Validation:*
- Required patterns: "T-score standardization complete", "Mean RAVLT_T: 5X.X"
- Required patterns: "Missing data handled", "N = XX participants retained"
- Forbidden patterns: "ERROR", "FAIL", "NaN in T-scores"

**Expected Behavior on Validation Failure:**
Log error with specific test extraction failure, quit and invoke g_debug

### Step 2: Load Mean Theta Scores from Ch5

**Dependencies:** Steps 0-1 (validation + cognitive tests)
**Complexity:** Low (~3 minutes)

**Purpose:** Load IRT theta scores from Ch5 5.1.1 and compute mean theta per participant

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/*theta*.csv
- Expected format: Participant UIDs with theta estimates across sessions

**Processing:**
- Load theta scores from Ch5 5.1.1 output
- Verify data contains 100 participants x 4 sessions structure
- Compute mean theta per participant across test sessions
- Implementation: group by UID, compute mean(theta) across sessions
- Handle missing sessions: require minimum 3 of 4 sessions for inclusion
- Create participant-level theta means dataset

**Output:**
- data/step02_theta_means.csv (mean theta per participant)

**Validation Requirement:**
Validation tools MUST be used after theta loading execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_theta_means.csv: ~100 rows x 2 columns
- Columns: UID (object), theta_mean (float64)

*Value Ranges:*
- theta_mean in range [-3, 3] (IRT ability scale bounds)
- Distribution approximately normal, mean near 0

*Data Quality:*
- 90-100 participants with theta estimates
- No missing theta_mean values
- All UIDs from step01 represented (or documented exclusions)

*Log Validation:*
- Required patterns: "Theta means computed", "N = XX participants"
- Required patterns: "Mean theta_mean: X.XX", "SD theta_mean: X.XX"
- Forbidden patterns: "ERROR", "MISSING SESSIONS", "COMPUTATION FAILED"

**Expected Behavior on Validation Failure:**
Log specific theta computation failure, document data loss, consider quitting if >10% missing

### Step 3: Merge Datasets and Create Analysis File

**Dependencies:** Steps 1-2 (cognitive tests + theta means)
**Complexity:** Low (~3 minutes)

**Purpose:** Merge cognitive tests with theta means to create final analysis dataset

**Input:**
- data/step01_cognitive_tests.csv (T-scored predictors)
- data/step02_theta_means.csv (outcome variable)

**Processing:**
- Inner join on UID to retain participants with both cognitive and theta data
- Verify no participants excluded due to merge failures
- Create final analysis dataset with predictors and outcome
- Compute descriptive statistics for merged dataset
- Check for any remaining missing data patterns

**Output:**
- data/step03_analysis_dataset.csv (merged cognitive + theta data)

**Validation Requirement:**
Validation tools MUST be used after dataset merging execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_analysis_dataset.csv: ~90-100 rows x 6 columns
- Columns: UID, RAVLT_T, BVMT_T, NART_T, RPM_T, theta_mean

*Value Ranges:*
- Same ranges as previous steps maintained
- No missing values in any analysis variables

*Data Quality:*
- Final N >= 90 participants (acceptable retention rate)
- Complete cases only (no missing data)
- Participant UIDs consistent across merge

*Log Validation:*
- Required patterns: "Merge complete", "Final N = XX participants"
- Required patterns: "Complete cases only", "Analysis dataset ready"
- Forbidden patterns: "MERGE FAILURE", "MISSING DATA", "EMPTY DATASET"

**Expected Behavior on Validation Failure:**
Log merge failure details, check for systematic exclusion patterns, quit if N < 80

### Step 4: Comprehensive Regression Assumption Checking

**Dependencies:** Step 3 (analysis dataset)
**Complexity:** Medium (~10 minutes)

**Purpose:** Check all multiple regression assumptions with visual and statistical diagnostics

**Processing:**
- Fit preliminary regression: theta_mean ~ RAVLT_T + BVMT_T + NART_T + RPM_T
- Implementation: statsmodels.api.OLS for comprehensive diagnostics
- Check assumptions systematically:
  1. Normality of residuals: Shapiro-Wilk test + Q-Q plot
  2. Homoscedasticity: Breusch-Pagan test + residual vs fitted plot
  3. Linearity: Partial regression plots for each predictor + RESET test
  4. Multicollinearity: VIF for each predictor (threshold: VIF < 5)
  5. Independence: Verified by study design (participant-level data)
  6. Outliers: Cook's distance (threshold: D > 4/n = 0.04)

- Generate diagnostic plots and save assumption test results
- Implement remedial actions if assumptions violated:
  - Normality p < 0.05: Flag for bootstrap CIs (1000 iterations, seed=42)
  - Heteroscedasticity p < 0.05: Flag for HC3 robust standard errors
  - VIF > 5: Document multicollinearity, consider ridge if VIF > 10
  - Outliers (Cook's D > 0.04): Flag for sensitivity analysis with/without outliers

**Output:**
- data/step04_assumption_diagnostics.csv (test statistics and p-values)
- data/step04_diagnostic_plots_data.csv (plot source data for rq_plots)

**Validation Requirement:**
Validation tools MUST be used after assumption checking execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_assumption_diagnostics.csv: 6 rows x 4 columns
- Columns: assumption (str), test_statistic (float64), p_value (float64), remedial_action (str)
- data/step04_diagnostic_plots_data.csv: variable length, plot source data

*Value Ranges:*
- p_values in [0, 1]
- VIF values in [1, 20] (extreme multicollinearity would be >20)
- Cook's D values in [0, 1] (extreme influence would be >1)

*Data Quality:*
- All 6 assumptions tested and documented
- Remedial actions specified for any violations
- Plot data saved for visualization

*Log Validation:*
- Required patterns: "Assumption checking complete", "VIF range: X.X to X.X"
- Required patterns: "Outliers detected: X", "Remedial actions determined"
- Forbidden patterns: "ERROR", "COMPUTATION FAILED", "INVALID TEST"

**Expected Behavior on Validation Failure:**
Log specific assumption test failure, document which tests succeeded, attempt to continue with available diagnostics

### Step 5: Fit Multiple Regression with Bootstrap Confidence Intervals

**Dependencies:** Step 4 (assumption diagnostics)
**Complexity:** Medium (~8 minutes including bootstrap)

**Purpose:** Fit main multiple regression model with bootstrap CIs for robust inference

**Processing:**
- Fit main regression model: theta_mean ~ RAVLT_T + BVMT_T + NART_T + RPM_T
- Implementation: statsmodels.api.OLS for comprehensive output
- Extract core statistics: R², adjusted R², F-statistic, coefficients, standard errors
- Implement participant-level bootstrap for 95% CIs:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Resampling unit: Participants (preserves any residual dependencies)
  - Method: Sample participants with replacement, keep all their data
  - For each iteration: fit model, extract beta coefficients
  - CI computation: percentile method (2.5th, 97.5th percentiles)
- Check for convergence issues or bootstrap failures
- Apply remedial actions from Step 4 if needed:
  - If normality violated: Report bootstrap CIs as primary inference
  - If heteroscedasticity: Add HC3 robust standard errors

**Output:**
- data/step05_regression_results.csv (model coefficients and statistics)
- data/step05_bootstrap_results.csv (bootstrap CI details)

**Validation Requirement:**
Validation tools MUST be used after regression fitting execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_regression_results.csv: 5 rows x 7 columns
- Columns: predictor, beta, se, t_stat, p_value, ci_lower, ci_upper
- data/step05_bootstrap_results.csv: 1000 rows x 5 columns (bootstrap samples)

*Value Ranges:*
- beta coefficients in [-2, 2] (standardized predictors, reasonable bounds)
- se (standard errors) > 0 (positive values)
- p_values in [0, 1]
- ci_lower < beta < ci_upper (proper CI bounds)
- R² in [0, 1], typically expect 0.15-0.45

*Data Quality:*
- All 4 predictors plus intercept represented
- Bootstrap completed successfully (1000 iterations)
- CIs are valid (lower < upper bounds)
- No convergence failures or NaN results

*Log Validation:*
- Required patterns: "Regression fitted successfully", "R² = X.XXX"
- Required patterns: "Bootstrap complete: 1000 iterations", "CI coverage verified"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "BOOTSTRAP FAILURE"

**Expected Behavior on Validation Failure:**
Log specific regression failure, check for convergence issues, attempt standard errors if bootstrap fails

### Step 6: Multiple Comparison Corrections and Significance Testing

**Dependencies:** Step 5 (regression results)
**Complexity:** Low (~3 minutes)

**Purpose:** Apply Bonferroni correction for multiple predictors and implement dual p-value reporting

**Processing:**
- Multiple comparison correction within-RQ:
  - Family: 4 predictors (RAVLT_T, BVMT_T, NART_T, RPM_T)
  - Bonferroni: alpha = 0.05/4 = 0.0125 per predictor
  - Chapter-level correction: alpha = 0.05/28 = 0.00179
- Also compute FDR-adjusted p-values using Benjamini-Hochberg procedure
- Apply Decision D068: Report BOTH uncorrected AND corrected p-values
- Test specific hypotheses:
  1. Overall model significance at alpha = 0.00179 (Chapter 7 correction)
  2. Individual predictor significance at alpha = 0.0125 (within-RQ correction)
  3. Hypothesis test: RAVLT_beta > RPM_beta (episodic > intelligence)
- Format results with dual p-value reporting

**Output:**
- data/step06_corrected_results.csv (p-values with corrections)
- data/step06_hypothesis_tests.csv (specific hypothesis test results)

**Validation Requirement:**
Validation tools MUST be used after significance testing execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_corrected_results.csv: 4 rows x 6 columns
- Columns: predictor, p_uncorrected, p_bonferroni, p_fdr, significant_uncorrected, significant_corrected
- data/step06_hypothesis_tests.csv: 3 rows x 4 columns (model + 2 specific tests)

*Value Ranges:*
- All p_values in [0, 1]
- p_bonferroni >= p_uncorrected (correction makes more conservative)
- p_fdr between p_uncorrected and p_bonferroni

*Data Quality:*
- All correction methods applied consistently
- Significance flags consistent with alpha thresholds
- Dual reporting present for all predictors

*Log Validation:*
- Required patterns: "Corrections applied", "Dual p-values computed"
- Required patterns: "Bonferroni alpha = 0.0125", "Chapter alpha = 0.00179"
- Forbidden patterns: "ERROR", "CORRECTION FAILED", "INVALID P-VALUE"

**Expected Behavior on Validation Failure:**
Log specific correction failure, check p-value validity, continue with uncorrected if corrections fail

### Step 7: Cross-Validation and Model Stability Assessment

**Dependencies:** Step 5 (regression results)
**Complexity:** Medium (~8 minutes)

**Purpose:** Assess model generalizability and stability through cross-validation

**Processing:**
- Implement 5-fold cross-validation using sklearn.model_selection.KFold
- Random seed: 42 for reproducibility
- Shuffle: True (randomize before splitting)
- Stratification: Use quantile-based stratification for theta_mean (outcome)
- For each fold:
  - Fit model on training set (80% of data)
  - Evaluate on test set (20% of data)
  - Compute R² for both training and test sets
  - Extract beta coefficients for stability assessment
- Compute cross-validation statistics:
  - Mean and std of test R² across folds
  - Mean and std of training R² across folds
  - Generalization gap: mean(train_R²) - mean(test_R²)
  - Flag overfitting if gap > 0.10
- Assess coefficient stability across folds

**Output:**
- data/step07_cross_validation.csv (CV fold results)
- data/step07_stability_assessment.csv (coefficient stability metrics)

**Validation Requirement:**
Validation tools MUST be used after cross-validation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_cross_validation.csv: 5 rows x 6 columns
- Columns: fold, train_r2, test_r2, train_n, test_n, generalization_gap
- data/step07_stability_assessment.csv: 4 rows x 5 columns (coefficient stats)

*Value Ranges:*
- R² values in [0, 1]
- train_r2 >= test_r2 (expected pattern)
- generalization_gap typically 0.00-0.20, flag if > 0.10
- n_train ~ 80, n_test ~ 20 per fold

*Data Quality:*
- All 5 folds completed successfully
- Reasonable train/test splits achieved
- Coefficient stability assessment complete

*Log Validation:*
- Required patterns: "Cross-validation complete", "Mean test R² = X.XXX"
- Required patterns: "Generalization gap = X.XXX", "Stability assessed"
- Forbidden patterns: "CV FAILED", "FOLD ERROR", "UNSTABLE MODEL"

**Expected Behavior on Validation Failure:**
Log CV failure details, attempt with different fold strategy, continue with main model if CV completely fails

### Step 8: Sensitivity Analysis and Effect Size Computation

**Dependencies:** Steps 5-7 (main results + cross-validation)
**Complexity:** Medium (~8 minutes)

**Purpose:** Conduct sensitivity analyses and compute comprehensive effect sizes

**Processing:**
- Sensitivity analysis: Fit model excluding NART due to language validity concerns
  - Model: theta_mean ~ RAVLT_T + BVMT_T + RPM_T
  - Compare R² with and without NART (expect minimal change if NART weak)
  - Document R² change and coefficient stability
- Compute comprehensive effect sizes:
  - Overall R² and adjusted R² for sample size correction
  - Cohen's f² = R²/(1-R²) for effect size interpretation
  - Semi-partial correlations (sr²) for unique variance per predictor
  - Standardized beta coefficients for predictor importance ranking
- Implement predictor importance analysis:
  - Rank predictors by |standardized_beta| magnitude
  - Test hypothesis: RAVLT_beta > RPM_beta (episodic > intelligence)
  - Compute relative importance using sr² decomposition
- Post-hoc power analysis:
  - Given: N=90-100, 4 predictors, alpha=0.00179 (Chapter 7)
  - Calculate: observed power for detected effects using statsmodels.stats.power
  - Report: power for overall model and individual predictors

**Output:**
- data/step08_sensitivity_analysis.csv (model with/without NART)
- data/step08_effect_sizes.csv (comprehensive effect size metrics)
- data/step08_power_analysis.csv (post-hoc power calculations)

**Validation Requirement:**
Validation tools MUST be used after sensitivity analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_sensitivity_analysis.csv: 2 rows x 5 columns (full model + no NART)
- data/step08_effect_sizes.csv: 4 rows x 6 columns (predictor effect sizes)
- data/step08_power_analysis.csv: 1 row x 4 columns (power statistics)

*Value Ranges:*
- R² values in [0, 1], expect 0.15-0.45 range
- f² typically 0.02-0.80 (small to large effects)
- sr² values sum to approximately R²
- Power in [0, 1], interpret relative to 0.80 threshold

*Data Quality:*
- Sensitivity model converged successfully
- Effect sizes computed for all predictors
- Power analysis completed with valid statistics

*Log Validation:*
- Required patterns: "Sensitivity analysis complete", "Effect sizes computed"
- Required patterns: "Power analysis finished", "Predictor ranking determined"
- Forbidden patterns: "SENSITIVITY FAILED", "EFFECT SIZE ERROR", "POWER COMPUTATION FAILED"

**Expected Behavior on Validation Failure:**
Log specific analysis failures, continue with available results, document limitations in interpretation

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (prerequisite verification)
- data/step01_cognitive_tests.csv (T-scored predictors)
- data/step02_theta_means.csv (mean theta per participant)
- data/step03_analysis_dataset.csv (merged analysis file)
- data/step04_assumption_diagnostics.csv (assumption test results)
- data/step04_diagnostic_plots_data.csv (plot source data)
- data/step05_regression_results.csv (main model results)
- data/step05_bootstrap_results.csv (bootstrap samples)
- data/step06_corrected_results.csv (multiple comparison corrections)
- data/step06_hypothesis_tests.csv (specific hypothesis tests)
- data/step07_cross_validation.csv (CV results)
- data/step07_stability_assessment.csv (coefficient stability)
- data/step08_sensitivity_analysis.csv (model variants)
- data/step08_effect_sizes.csv (effect size metrics)
- data/step08_power_analysis.csv (power statistics)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_cognitive_tests.log
- logs/step02_load_theta_means.log
- logs/step03_merge_datasets.log
- logs/step04_check_assumptions.log
- logs/step05_fit_regression.log
- logs/step06_multiple_comparisons.log
- logs/step07_cross_validation.log
- logs/step08_sensitivity_analysis.log

### Plots (EMPTY until rq_plots runs)
Plot source data created in data/ with step##_*_plot_data.csv naming convention.
Actual visualizations created by rq_plots agent.

### Results (EMPTY until rq_results runs)
Final summary.md created by rq_results agent synthesizing all outputs.

---

## Expected Data Formats

### Step-to-Step Transformations
1. **Raw -> T-scores:** Cognitive tests standardized to M=50, SD=10
2. **Sessions -> Means:** Multiple theta sessions averaged per participant  
3. **Separate -> Merged:** Predictors and outcome combined for analysis
4. **Model -> Diagnostics:** Regression assumptions systematically checked
5. **Point -> Interval:** Bootstrap CIs for robust inference
6. **Single -> Multiple:** Corrections applied for family-wise error control
7. **Static -> Cross-validated:** Generalizability assessed through CV
8. **Main -> Sensitivity:** Alternative models tested for robustness

### Column Naming Conventions
- **Participant IDs:** UID (consistent across all files)
- **Predictors:** RAVLT_T, BVMT_T, NART_T, RPM_T (T-score suffix)
- **Outcome:** theta_mean (average episodic memory ability)
- **Statistics:** beta, se, t_stat, p_value, ci_lower, ci_upper
- **Corrections:** p_uncorrected, p_bonferroni, p_fdr
- **Effect sizes:** r2, adj_r2, cohens_f2, sr_squared

### Data Type Constraints
- **UIDs:** object/string, non-nullable, unique
- **Test scores:** float64, nullable during intermediate steps
- **Statistics:** float64, non-nullable in final outputs
- **Flags:** boolean for significance indicators
- **Sample sizes:** int64 for participant counts

---

## Cross-RQ Dependencies

**Source RQ:** Ch5 5.1.1 (Functional Form Comparison)

**Required Files:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/*theta*.csv  
- Fallback: Search pattern results/ch5/5.1.1/data/step*theta*.{csv,txt}

**Expected Content:**
IRT theta estimates for omnibus "All" factor across 100 participants and 4 test sessions.
Should contain participant UIDs and theta values in IRT ability scale (range -3 to +3).

**Contingency Plan:**
If Ch5 5.1.1 outputs not available, this RQ cannot proceed (DERIVED data dependency).
Must verify Ch5 status = success before execution begins.

**Independent Data:**
Cognitive test data extracted independently from master.xlsx regardless of Ch5 status.

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements Summary

All 9 steps (0-8) include comprehensive 4-layer validation criteria covering:
1. **Output Files:** Exact specifications with row/column counts and data types
2. **Value Ranges:** Scientific bounds based on measurement scales  
3. **Data Quality:** Missing data tolerance and distribution expectations
4. **Log Validation:** Required success patterns and forbidden error patterns

Each step specifies expected behavior on validation failure with specific actions:
- Log detailed failure information
- Attempt alternative approaches where applicable  
- Quit with informative error messages for critical failures
- Invoke g_debug for complex failures requiring investigation

**Post-execution validation coverage:** 100% (all 9 steps have mandatory validation requirements)

---

## Summary

**Total Steps:** 9 (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** ~45 minutes
**Cross-RQ Dependencies:** Ch5 5.1.1 theta scores (CRITICAL)
**Primary Outputs:** Multiple regression results with bootstrap CIs and cross-validation
**Validation Coverage:** 100% (all 9 steps have 4-layer validation requirements)

**Key Hypothesis:** Moderate predictive relationship (R² = 0.15-0.35) between cognitive tests and REMEMVR ability, with episodic memory tests (RAVLT, BVMT) predicting better than intelligence tests (NART, RPM).

**Critical Methodological Notes:**
- All randomized procedures use seed=42 for reproducibility
- Bootstrap CIs (1000 iterations) provide robust inference  
- 5-fold cross-validation assesses generalizability
- Dual p-value reporting per Decision D068
- Comprehensive assumption checking with remedial actions specified
- Multiple sensitivity analyses for robustness assessment

**Statistical Implementation Specifications:**
- Random seed=42 for ALL randomized procedures (bootstrap, CV)
- Bootstrap: 1000 iterations, participant-level resampling, percentile CIs
- Cross-validation: 5-fold KFold, shuffle=True, quantile stratification
- Power analysis: Post-hoc using statsmodels with observed effects
- Multiple comparisons: Bonferroni (within-RQ: alpha=0.0125, chapter: alpha=0.00179) + FDR
- Remedial actions: Bootstrap for normality, HC3 for heteroscedasticity, ridge for VIF>10

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml  
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent with v5.1 enhanced specifications