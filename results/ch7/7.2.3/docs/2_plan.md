# Analysis Plan: RQ 7.2.3 - Age x Cognitive Test Interaction

**Research Question:** 7.2.3
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This analysis examines Age x Cognitive Test interactions across 100 participants to determine whether cognitive tests predict REMEMVR performance differently for younger vs older adults. Tests individual Age x Test interactions for RAVLT, BVMT, NART, and RPM cognitive assessments using mean theta_all scores from Ch5 as the dependent variable.

**Pipeline:** Multiple Linear Regression with Interaction Terms
**Steps:** 8 total analysis steps (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** ~45 minutes total (including bootstrap, CV, diagnostics)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Within-RQ Bonferroni correction: alpha = 0.05/4 = 0.0125 per interaction test
- Bootstrap stabilization: 2000 iterations for reliable interaction CIs
- Cross-validation: 5-fold for generalization assessment

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 5.1.1 outputs exist and cognitive test data accessible before proceeding

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/*theta*.csv
- Fallback: results/ch5/5.1.1/data/analysis_results.csv
- Expected content: 100 rows with UID, theta_all (mean scores)
- Cognitive tests: data/cache/master.xlsx
- If Ch5 not found: QUIT with "Ch5 5.1.1 theta scores not available"

**Processing:**
- Check Ch5 5.1.1 status: verify rq_results = success in status.yaml
- Locate theta_all scores using multiple path patterns
- Verify master.xlsx exists and contains cognitive test columns
- Log all validation results
- Test read access to both data sources

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Content: Ch5 status, file paths found, access test results

*Value Ranges:*
- Ch5 status: "success" required
- File sizes: theta file > 1KB, master.xlsx > 50KB
- Access: read permissions confirmed

*Data Quality:*
- Ch5 5.1.1 completed successfully
- Theta scores file exists and readable
- Master.xlsx contains required cognitive test columns
- No critical access errors

*Log Validation:*
- Required patterns: "Ch5 5.1.1 validation PASS", "Files accessible"
- Forbidden patterns: "ERROR", "FAIL", "not found", "access denied"

**Expected Behavior on Validation Failure:**
Quit immediately with specific error message, log to step00_dependency_validation.log

---

### Step 1: Extract and Prepare Data
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (~5 minutes)

**Purpose:** Extract mean theta_all scores and cognitive test data, merge datasets

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/*theta*.csv (first match)
- Cognitive tests: data/cache/master.xlsx
- Expected: UID, theta_all columns from Ch5; UID, Age, RAVLT_T, BVMT_T, NART_T, RPM_T from master.xlsx

**Processing:**
- Load theta_all scores from Ch5 output (use mean values)
- Extract cognitive test data from master.xlsx sheets
- Variables needed: UID, Age, RAVLT_T, BVMT_T, NART_T, RPM_T
- Merge datasets on UID
- Check for missing data: exclude participants missing cognitive tests
- Compute descriptive statistics for all variables
- Create data quality report (N, missing data patterns)

**Output:**
- data/step01_merged_data.csv (complete dataset for analysis)
- data/step01_descriptives.csv (means, SDs, ranges for all variables)

**Validation Requirement:**
Validation tools MUST be used after data extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_merged_data.csv: 100 rows x 7 columns
- Columns: UID (object), Age (float), theta_all (float), RAVLT_T (float), BVMT_T (float), NART_T (float), RPM_T (float)
- data/step01_descriptives.csv: 7 rows x 5 columns (variable stats)

*Value Ranges:*
- Age in [18, 80] (REMEMVR age range)
- theta_all in [-3, 3] (IRT ability scale)
- Cognitive T-scores in [20, 80] (T-score range)
- All theta_all values non-null (required for analysis)

*Data Quality:*
- Exactly 100 participants with complete data
- No duplicate UIDs
- Missing cognitive tests <5% (acceptable threshold)
- Age distribution spans young to old adults

*Log Validation:*
- Required patterns: "Data merge successful: 100 participants", "Missing data <5%"
- Forbidden patterns: "ERROR", "missing theta_all", "duplicate UID"

**Expected Behavior on Validation Failure:**
Log error details, attempt alternative theta file path, quit if no valid data source

---

### Step 2: Center Predictors and Create Interaction Terms
**Dependencies:** Step 1 (merged data)
**Complexity:** Low (~5 minutes)

**Purpose:** Center predictors for interpretable interactions and create Age x Test interaction terms

**Input:**
- data/step01_merged_data.csv (complete dataset)

**Processing:**
- Center Age: Age_c = Age - mean(Age) for meaningful zero point
- Center cognitive tests: Test_c = Test_T - 50 (T-score mean = 50)
- Create interaction terms:
  - Age_c_x_RAVLT_c = Age_c * RAVLT_c
  - Age_c_x_BVMT_c = Age_c * BVMT_c
  - Age_c_x_NART_c = Age_c * NART_c
  - Age_c_x_RPM_c = Age_c * RPM_c
- Compute correlation matrix of all predictors
- Check for multicollinearity concerns (|r| > 0.70)

**Output:**
- data/step02_centered_predictors.csv (centered vars + interactions)
- data/step02_correlation_matrix.csv (predictor correlations)

**Validation Requirement:**
Validation tools MUST be used after predictor centering execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_centered_predictors.csv: 100 rows x 15 columns
- Includes: original vars, centered vars, 4 interaction terms
- data/step02_correlation_matrix.csv: 11 x 11 correlation matrix

*Value Ranges:*
- Age_c: mean approximately 0 (+/- 0.01)
- Test_c variables: mean approximately 0 (+/- 0.01)
- Correlations in [-1, 1] (valid correlation range)
- Age_c range: approximately [-30, +30] (age span)

*Data Quality:*
- All centered variables have mean near 0
- No |correlations| > 0.95 (extreme multicollinearity)
- Interaction terms show appropriate variance
- No computational errors in centering

*Log Validation:*
- Required patterns: "Centering complete", "Interaction terms created", "Correlation matrix computed"
- Forbidden patterns: "ERROR", "infinite values", "centering failed"

**Expected Behavior on Validation Failure:**
Log specific centering errors, check for division by zero, quit if computation fails

---

### Step 3: Fit Age x Cognitive Test Interaction Models
**Dependencies:** Step 2 (centered predictors)
**Complexity:** Medium (~10 minutes including diagnostics)

**Purpose:** Fit 4 separate interaction models testing Age x Test effects on theta_all

**Input:**
- data/step02_centered_predictors.csv (centered predictors and interactions)

**Processing:**
- Fit 4 regression models:
  1. theta_all ~ Age_c + RAVLT_c + Age_c_x_RAVLT_c
  2. theta_all ~ Age_c + BVMT_c + Age_c_x_BVMT_c
  3. theta_all ~ Age_c + NART_c + Age_c_x_NART_c
  4. theta_all ~ Age_c + RPM_c + Age_c_x_RPM_c
- Implementation: statsmodels.api.OLS for each model
- Extract: R², adjusted R², F-statistic, all coefficients with SEs
- Multiple comparison correction:
  - Family: Within-RQ (4 interaction tests)
  - Bonferroni: alpha = 0.05/4 = 0.0125 per interaction test
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Check VIF for all predictors in each model
- Extract interaction coefficient statistics for effect size computation

**Output:**
- data/step03_interaction_models.csv (all model results)
- data/step03_interaction_coefficients.csv (interaction terms only with dual p-values)

**Validation Requirement:**
Validation tools MUST be used after regression model fitting execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_interaction_models.csv: 4 rows x 12 columns
- Columns: model, R2, adj_R2, F_stat, F_p, interaction_coef, interaction_se, interaction_p_uncorr, interaction_p_bonf, VIF_age, VIF_test, VIF_interaction
- data/step03_interaction_coefficients.csv: 4 rows x 6 columns

*Value Ranges:*
- R² in [0, 1] (valid proportion of variance)
- F-statistics > 0 (positive test statistics)
- p-values in [0, 1] (valid probability range)
- VIF in [1, 10] (multicollinearity check)
- Bonferroni p = uncorrected p * 4 (correction verification)

*Data Quality:*
- All 4 models fitted successfully
- No convergence failures or numerical issues
- Dual p-values present for all interactions (Decision D068)
- VIF < 5 for all predictors (no problematic multicollinearity)

*Log Validation:*
- Required patterns: "4 interaction models fitted", "VIF check complete", "Dual p-values computed"
- Forbidden patterns: "ERROR", "convergence failed", "singular matrix"

**Expected Behavior on Validation Failure:**
Log specific model fitting errors, check for data quality issues, quit if models cannot converge

---

### Step 4: Simple Slopes Analysis (If Interactions Significant)
**Dependencies:** Step 3 (interaction models)
**Complexity:** Medium (~8 minutes including plots)

**Purpose:** Conduct simple slopes analysis for significant Age x Test interactions

**Input:**
- data/step03_interaction_coefficients.csv (interaction results)
- data/step02_centered_predictors.csv (for slope computation)

**Processing:**
- Check which interactions significant: p_bonferroni < 0.0125
- For significant interactions only:
  - Compute test slope at Age = -1SD (younger adults)
  - Compute test slope at Age = +1SD (older adults)  
  - Test significance of each simple slope
  - Compute slope difference and confidence interval
  - Create interaction plot data (Age x Test predictions)
- If no significant interactions: create summary stating null findings
- Implementation: manual slope computation using interaction coefficients
- Format results for visualization and interpretation

**Output:**
- data/step04_simple_slopes.csv (slopes at Age +/-1SD if applicable)
- data/step04_interaction_plots.csv (plot data for significant interactions)
- data/step04_slopes_summary.txt (interpretation summary)

**Validation Requirement:**
Validation tools MUST be used after simple slopes analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_simple_slopes.csv: N rows x 7 columns (N = number of significant interactions)
- Columns: test_name, age_level, slope, se, t_value, p_value, CI_lower, CI_upper
- data/step04_slopes_summary.txt: text interpretation summary

*Value Ranges:*
- Slopes: reasonable range based on theta_all scale (approximately -1 to 1)
- Standard errors > 0 (positive values)
- p-values in [0, 1] (valid probability range)
- Confidence intervals: CI_lower < slope < CI_upper

*Data Quality:*
- Only significant interactions analyzed (p_bonferroni < 0.0125)
- Both age levels (-1SD, +1SD) represented for each significant test
- Slope calculations mathematically correct
- No computational errors in simple slope derivation

*Log Validation:*
- Required patterns: "Simple slopes analysis complete", "X significant interactions found"
- Acceptable: "No significant interactions found" (if null results)
- Forbidden patterns: "ERROR", "slope computation failed"

**Expected Behavior on Validation Failure:**
Log slope computation errors, verify interaction coefficient inputs, quit if mathematical errors

---

### Step 5: Effect Sizes and Model Diagnostics
**Dependencies:** Step 3 (fitted models)
**Complexity:** Medium (~10 minutes including assumption checks)

**Purpose:** Compute effect sizes for interactions and check regression assumptions

**Input:**
- data/step03_interaction_models.csv (model results)
- data/step02_centered_predictors.csv (for diagnostics)

**Processing:**
- Compute Cohen's f² for each interaction term:
  - f² = (R²_full - R²_reduced) / (1 - R²_full)
  - Compare full model to model without interaction
- Effect size interpretation: f² = 0.02 (small), 0.15 (medium), 0.35 (large)
- Check regression assumptions for each model:
  - Normality: Shapiro-Wilk test on residuals
  - Homoscedasticity: Breusch-Pagan test
  - Multicollinearity: VIF for each predictor
  - Outliers: Cook's D > 4/n threshold (0.04 for n=100)
- Remedial actions if assumptions violated:
  - Normality p < 0.05: Use bootstrap CIs as primary (Step 6)
  - Heteroscedasticity p < 0.05: Report HC3 robust SEs
  - VIF > 5: Document multicollinearity concern
  - Cook's D > 0.04: Report with/without influential cases

**Output:**
- data/step05_effect_sizes.csv (Cohen's f² for each interaction)
- data/step05_diagnostics.csv (assumption test results)
- data/step05_diagnostics_summary.txt (interpretation of violations)

**Validation Requirement:**
Validation tools MUST be used after effect size and diagnostic execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_effect_sizes.csv: 4 rows x 4 columns
- Columns: test_name, R2_full, R2_reduced, cohens_f2
- data/step05_diagnostics.csv: 4 rows x 8 columns
- Columns: model, shapiro_p, breusch_pagan_p, max_vif, n_outliers, normality_ok, homosced_ok, multicollin_ok

*Value Ranges:*
- Cohen's f² ≥ 0 (non-negative effect sizes)
- R² values in [0, 1] (valid proportions)
- p-values in [0, 1] (valid probability range)
- VIF ≥ 1 (minimum possible VIF)
- N_outliers: 0 to 10 (reasonable outlier count)

*Data Quality:*
- All 4 models have effect sizes computed
- All assumption tests completed successfully
- Diagnostic flags (normality_ok, etc.) are boolean
- No mathematical errors in f² computation

*Log Validation:*
- Required patterns: "Effect sizes computed", "Assumption checks complete", "4 models diagnosed"
- Forbidden patterns: "ERROR", "computation failed", "invalid VIF"

**Expected Behavior on Validation Failure:**
Log specific diagnostic failures, continue with available results, note limitations in summary

---

### Step 6: Bootstrap Confidence Intervals
**Dependencies:** Step 3 (fitted models)
**Complexity:** High (~15 minutes for 2000 iterations)

**Purpose:** Generate robust bootstrap confidence intervals for interaction coefficients

**Input:**
- data/step02_centered_predictors.csv (complete dataset)
- Models from Step 3 (interaction specifications)

**Processing:**
- Participant-level block bootstrap (preserves any within-participant correlation)
- Iterations: 2000 (increased from 1000 for stable CIs per stats validation)
- Random seed: 42 for reproducibility
- For each iteration:
  - Resample participants WITH replacement
  - Fit all 4 interaction models on bootstrap sample
  - Extract interaction coefficients
- Compute 95% CIs using percentile method (2.5th, 97.5th percentiles)
- Compare bootstrap CIs to normal-theory CIs
- Flag interactions where bootstrap CI excludes zero (robust significance)
- Document bootstrap distribution characteristics (skewness, outliers)

**Output:**
- data/step06_bootstrap_coefficients.csv (2000 x 4 matrix of interaction coefs)
- data/step06_bootstrap_CIs.csv (95% CIs for each interaction)
- data/step06_bootstrap_summary.txt (distribution characteristics)

**Validation Requirement:**
Validation tools MUST be used after bootstrap analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_bootstrap_coefficients.csv: 2000 rows x 4 columns
- Columns: iter_1_RAVLT, iter_1_BVMT, iter_1_NART, iter_1_RPM (interaction coefficients)
- data/step06_bootstrap_CIs.csv: 4 rows x 4 columns
- Columns: test_name, bootstrap_coef_mean, CI_2.5, CI_97.5

*Value Ranges:*
- Bootstrap coefficients: reasonable range around original estimates
- CI bounds: CI_2.5 < CI_97.5 (proper ordering)
- Bootstrap means approximately equal to original coefficients (+/- 0.05)
- All values finite (no infinite or NaN results)

*Data Quality:*
- Exactly 2000 bootstrap iterations completed
- All bootstrap samples yielded valid coefficient estimates
- No convergence failures across bootstrap iterations
- Bootstrap distributions show reasonable properties

*Log Validation:*
- Required patterns: "Bootstrap complete: 2000 iterations", "CIs computed successfully"
- Forbidden patterns: "ERROR", "convergence failed", "infinite bootstrap"

**Expected Behavior on Validation Failure:**
Log specific bootstrap failures, reduce iterations if memory issues, quit if systematic convergence problems

---

### Step 7: Cross-Validation Analysis
**Dependencies:** Step 2 (centered predictors)
**Complexity:** Medium (~7 minutes for 5-fold CV)

**Purpose:** Assess generalizability of Age x Test interaction effects using cross-validation

**Input:**
- data/step02_centered_predictors.csv (complete dataset)

**Processing:**
- Implement 5-fold cross-validation using sklearn.model_selection.KFold
- Random seed: 42 for reproducibility
- Shuffle: True (randomize before splitting)
- For each fold: fit interaction models on training (80%), evaluate on test (20%)
- Metrics per fold: R², interaction coefficient, interaction p-value
- Compute mean and std of interaction effects across folds
- Flag overfitting if train-test R² gap > 0.10 for any model
- Assess stability: CV coefficient within 1 SE of full-sample coefficient
- Document cross-validation performance for each interaction test

**Output:**
- data/step07_cv_results.csv (CV metrics for each fold and test)
- data/step07_cv_summary.csv (mean, std, stability assessment)

**Validation Requirement:**
Validation tools MUST be used after cross-validation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_cv_results.csv: 20 rows x 6 columns (5 folds x 4 tests)
- Columns: fold, test_name, train_R2, test_R2, interaction_coef, interaction_p
- data/step07_cv_summary.csv: 4 rows x 5 columns
- Columns: test_name, mean_interaction_coef, std_interaction_coef, mean_test_R2, overfitting_flag

*Value Ranges:*
- R² values in [0, 1] (valid proportions)
- Train R² ≥ test R² (expected pattern)
- Interaction coefficients: consistent with full-sample estimates
- p-values in [0, 1] (valid probability range)

*Data Quality:*
- All 5 folds completed successfully for all 4 tests
- No fold shows extreme overfitting (train-test gap > 0.20)
- CV coefficients within reasonable range of full-sample estimates
- No systematic convergence failures across folds

*Log Validation:*
- Required patterns: "5-fold CV complete", "Stability assessment complete"
- Acceptable warnings: "Overfitting detected in fold X" (if train-test gap > 0.10)
- Forbidden patterns: "ERROR", "CV failed", "fold convergence error"

**Expected Behavior on Validation Failure:**
Log CV failures by fold, attempt alternative random seeds, note instability limitations

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt
- data/step01_merged_data.csv
- data/step01_descriptives.csv
- data/step02_centered_predictors.csv
- data/step02_correlation_matrix.csv
- data/step03_interaction_models.csv
- data/step03_interaction_coefficients.csv
- data/step04_simple_slopes.csv (if significant interactions)
- data/step04_interaction_plots.csv (plot source data)
- data/step04_slopes_summary.txt
- data/step05_effect_sizes.csv
- data/step05_diagnostics.csv
- data/step05_diagnostics_summary.txt
- data/step06_bootstrap_coefficients.csv
- data/step06_bootstrap_CIs.csv
- data/step06_bootstrap_summary.txt
- data/step07_cv_results.csv
- data/step07_cv_summary.csv

### Logs (ONLY execution logs)
- logs/step00_dependency_validation.log
- logs/step01_extract_data.log
- logs/step02_center_predictors.log
- logs/step03_fit_interactions.log
- logs/step04_simple_slopes.log
- logs/step05_diagnostics.log
- logs/step06_bootstrap.log
- logs/step07_cross_validation.log

### Plots (EMPTY until rq_plots runs)
- Plot source CSVs created in data/ folder: step04_interaction_plots.csv

### Results (EMPTY until rq_results runs)
- summary.md will be created by rq_results agent

---

## Expected Data Formats

### Step-to-Step Transformations
1. **Step 1:** Raw Ch5 + master.xlsx → merged dataset (100 x 7)
2. **Step 2:** Merged data → centered predictors + interactions (100 x 15)
3. **Step 3:** Centered data → 4 fitted regression models
4. **Step 4:** Model results → simple slopes (if interactions significant)
5. **Step 5:** Models → effect sizes + diagnostics
6. **Step 6:** Models → bootstrap CIs (2000 iterations)
7. **Step 7:** Centered data → cross-validation results

### Column Naming Conventions
- **Original variables:** Age, theta_all, RAVLT_T, BVMT_T, NART_T, RPM_T
- **Centered variables:** Age_c, RAVLT_c, BVMT_c, NART_c, RPM_c
- **Interaction terms:** Age_c_x_[TEST]_c (e.g., Age_c_x_RAVLT_c)
- **P-values:** p_uncorrected, p_bonferroni (Decision D068)

### Data Type Constraints
- **UID:** object (string identifiers)
- **Age, cognitive tests:** float64 (continuous measures)
- **theta_all:** float64 (IRT ability estimates, range [-3, 3])
- **p-values:** float64, range [0, 1]
- **Effect sizes:** float64, range [0, infinity for f²]

---

## Cross-RQ Dependencies

**Primary Dependency:** Ch5 5.1.1 (Functional Form Comparison)
- **Required:** Mean theta_all scores (omnibus VR memory performance)
- **Status Check:** Ch5 5.1.1 rq_results = "success" in status.yaml
- **File Patterns:** 
  - Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
  - Alternative: results/ch5/5.1.1/data/*theta*.csv
  - Fallback: Manual extraction if standard paths missing

**Secondary Dependency:** Master dataset
- **Required:** Cognitive test T-scores and demographic data
- **Source:** data/cache/master.xlsx
- **Variables:** RAVLT_T, BVMT_T, NART_T, RPM_T, Age

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

All validation requirements are embedded within each step specification above, following the 4-layer validation structure:
1. **Output Files:** Exact paths, dimensions, column specifications
2. **Value Ranges:** Scientific bounds for all numeric variables
3. **Data Quality:** Missing data thresholds, distribution requirements
4. **Log Validation:** Required success patterns, forbidden error patterns

Each step includes specific validation criteria appropriate for the analysis type and expected outcomes.

---

## Summary

**Total Steps:** 8 (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** ~45 minutes (including 2000 bootstrap iterations)
**Cross-RQ Dependencies:** Ch5 5.1.1 (theta scores) + master.xlsx (cognitive tests)
**Primary Outputs:** Interaction coefficients with dual p-values, simple slopes (if significant), bootstrap CIs
**Validation Coverage:** 100% (all 8 steps have 4-layer validation requirements)

**Key Hypothesis:** Age x Cognitive Test interactions may show stronger test prediction in older adults due to compensatory processing, OR no interaction if VR scaffolding eliminates age differences in predictive utility.

**Critical Methodological Notes:**
- Enhanced v5.1 specifications: 2000 bootstrap iterations, seed=42, dual p-values
- Multiple comparison correction within RQ: Bonferroni alpha = 0.0125
- Remedial actions specified for all assumption violations
- Cross-validation assesses interaction effect stability
- Statistical power adequate for medium interactions (f² ≥ 0.15) but limited for small effects

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan → creates 3_tools.yaml
3. rq_analysis reads plan + tools → creates 4_analysis.yaml
4. g_code reads analysis → generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent with v5.1 enhancements