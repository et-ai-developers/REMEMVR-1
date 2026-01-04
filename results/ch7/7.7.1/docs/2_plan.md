# Analysis Plan: RQ 7.7.1 - Reverse Inference - Can REMEMVR predict RAVLT?

**Research Question:** 7.7.1
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines reverse prediction from REMEMVR theta scores to cognitive test scores (RAVLT, BVMT). Uses bidirectional comparison testing whether REMEMVR contains the construct measured by traditional tests. If REMEMVR fully encompasses traditional test constructs, reverse prediction should be strong while maintaining asymmetry with forward prediction.

**Pipeline:** Multiple Linear Regression with bidirectional comparison and cross-validation
**Steps:** 9 total analysis steps (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** ~45 minutes total

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Standard regression methodology with enhanced v5.1 statistical specifications

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 5.1.1 outputs exist before proceeding and validate master.xlsx accessibility

**Input:**
- Primary: results/ch5/5.1.1/status.yaml (verify rq_results: success)
- Alternative: results/ch5/5.1.1/data/step03_theta_scores.csv (theta_all estimates)
- Fallback: results/ch5/5.1.1/data/*theta*.{csv,txt} (theta file patterns)
- Expected content: N=100 participants with theta_all scores
- Raw data: data/cache/master.xlsx (RAVLT_Total, BVMT_TotR cognitive test scores)

**Processing:**
- Check Ch5 5.1.1 completed successfully (status.yaml confirmation)
- Locate theta_all file (try multiple patterns if needed)
- Verify file contains 100 participants with theta_all scores
- Verify master.xlsx accessibility with required cognitive test columns
- Log validation results with success/failure status
- If Ch5 not complete: QUIT with "Ch5 5.1.1 theta output required for analysis"

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Expected content: "DEPENDENCY CHECK - PASS" or "DEPENDENCY CHECK - FAIL"
- File size: >100 characters (meaningful validation content)

*Value Ranges:*
- Dependency status: binary (PASS/FAIL)
- File count checks: integer >= 0
- Expected N=100 participants in validation report

*Data Quality:*
- All dependency paths attempted and logged
- Clear success/failure status for each dependency
- Specific error messages if failures detected
- No ambiguous validation results

*Log Validation:*
- Required patterns: "Dependency validation complete"
- Required patterns: "Ch5 5.1.1 status confirmed"
- Required patterns: "master.xlsx accessible"
- Forbidden patterns: "ERROR", "FAIL", "dependency not found"

**Expected Behavior on Validation Failure:**
Raise error with specific dependency missing, log to logs/step00_validate_dependencies.log, quit immediately

---

### Step 1: Extract and Prepare Data
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (<5 minutes)

**Purpose:** Load theta_all scores from Ch5 5.1.1 and cognitive test scores from dfnonvr.csv, merge and prepare analysis dataset

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv (theta_all estimates)
- Alternative: results/ch5/5.1.1/data/*theta_all*.csv (alternative theta patterns)
- Raw data: data/cache/master.xlsx (RAVLT_Total, BVMT_TotR columns)
- Expected: N=100 participants with complete data on both measures

**Processing:**
- Load theta_all scores by participant UID
- Extract RAVLT_Total and BVMT_TotR from dfnonvr.csv
- Merge datasets on UID (inner join)
- Check for missing data patterns and document exclusions
- Verify N>=95 participants with complete data (allow 5% missingness)
- Log data extraction summary (N loaded, N merged, N excluded)
- Export merged dataset for analysis

**Output:**
- data/step01_merged_dataset.csv (theta + cognitive scores)

**Validation Requirement:**
Validation tools MUST be used after data extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_merged_dataset.csv: 95-100 rows x 4 columns minimum
- Columns: UID (object), theta_all (float64), RAVLT_Total (float64), BVMT_TotR (float64)
- Data types: UID string, theta/cognitive scores numeric

*Value Ranges:*
- theta_all in [-3, 3] (IRT ability scale)
- RAVLT_Total in [0, 80] (sum of 5 learning trials, max 16 per trial)
- BVMT_TotR in [0, 36] (sum of 3 trials, max 12 per trial)
- All scores positive where applicable

*Data Quality:*
- N >= 95 participants (allow max 5% missing)
- No duplicate UIDs
- No NaN values in analysis columns
- All numeric columns have finite values

*Log Validation:*
- Required patterns: "Data extraction complete: N=[95-100] participants"
- Required patterns: "Merge successful"
- Required patterns: "Missing data check complete"
- Forbidden patterns: "ERROR", "merge failed", "insufficient data"

**Expected Behavior on Validation Failure:**
Raise error with specific data issue, log to logs/step01_extract_data.log, quit with debug information

---

### Step 2: Standardize Variables
**Dependencies:** Step 1 (merged dataset)
**Complexity:** Low (<5 minutes)

**Purpose:** Convert all variables to T-scores (M=50, SD=10) to enable meaningful comparison between REMEMVR and traditional measures

**Input:**
- data/step01_merged_dataset.csv (raw scores)

**Processing:**
- Compute T-scores for each variable: T = 50 + 10 * ((X - M) / SD)
- Apply transformation to theta_all, RAVLT_Total, BVMT_TotR
- Verify T-score properties (M=50, SD=10 for each variable)
- Check for extreme outliers (T-scores beyond [20, 80] range)
- Document transformation parameters (original M, SD for back-transformation)
- Create correlation matrix for T-scored variables

**Output:**
- data/step02_standardized_data.csv (T-scored variables)

**Validation Requirement:**
Validation tools MUST be used after standardization execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_standardized_data.csv: 95-100 rows x 4 columns
- Columns: UID, REMEMVR_T, RAVLT_T, BVMT_T (all T-scores)
- Data types: UID (object), T-scores (float64)

*Value Ranges:*
- All T-scores approximately M=50, SD=10 (within rounding error)
- T-scores typically in [20, 80] range (extreme outliers flagged if beyond)
- Correlation coefficients in [-1, 1]

*Data Quality:*
- Exact participant count preserved from Step 1
- No missing values introduced during transformation
- T-score means within 0.1 of target (50.0)
- T-score SDs within 0.1 of target (10.0)

*Log Validation:*
- Required patterns: "T-score transformation complete"
- Required patterns: "Verification: M=50, SD=10"
- Required patterns: "Correlation matrix computed"
- Forbidden patterns: "ERROR", "transformation failed", "invalid T-scores"

**Expected Behavior on Validation Failure:**
Raise error with specific transformation issue, log to logs/step02_standardize_variables.log, provide transformation diagnostics

---

### Step 3: Fit Reverse Prediction Models
**Dependencies:** Step 2 (standardized data)
**Complexity:** Medium (~10 minutes including bootstrap)

**Purpose:** Fit regression models predicting cognitive tests from REMEMVR T-scores (reverse prediction direction)

**Input:**
- data/step02_standardized_data.csv (T-scored variables)

**Processing:**
- Model 1: RAVLT_T ~ REMEMVR_T (reverse prediction for verbal memory)
- Model 2: BVMT_T ~ REMEMVR_T (reverse prediction for visual memory)
- Implementation: statsmodels.api.OLS with robust standard errors
- Extract: R², adjusted R², F-statistic, beta coefficients, standard errors
- Bootstrap 95% CIs for all coefficients:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - CI computation: percentile method (2.5th, 97.5th percentiles)
- Multiple comparison correction:
  - Family: Within-RQ (2 regression models)
  - Bonferroni: alpha = 0.05/2 = 0.025 per model
  - Also compute FDR using Benjamini-Hochberg
  - Report BOTH uncorrected AND corrected p-values (Decision D068)

**Output:**
- data/step03_reverse_models.csv (model results with CIs and dual p-values)

**Validation Requirement:**
Validation tools MUST be used after regression execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_reverse_models.csv: 2 rows x 10 columns
- Columns: model, outcome, predictor, R2, adj_R2, beta, se, ci_lower, ci_upper, p_uncorrected, p_bonferroni, p_fdr
- Data types: model (object), numeric columns (float64)

*Value Ranges:*
- R² in [0, 1] (coefficient of determination bounds)
- beta in [-2, 2] (reasonable range for standardized predictors)
- se > 0 (positive standard errors)
- p-values in [0, 1] (valid probability range)
- CI bounds: ci_lower < beta < ci_upper

*Data Quality:*
- Exactly 2 models (RAVLT and BVMT predictions)
- All 1000 bootstrap iterations completed successfully
- Bootstrap CIs valid (lower < estimate < upper)
- Dual p-values present (Decision D068 compliance)

*Log Validation:*
- Required patterns: "Model 1 fitted: RAVLT ~ REMEMVR"
- Required patterns: "Model 2 fitted: BVMT ~ REMEMVR"
- Required patterns: "Bootstrap complete: 1000 iterations"
- Required patterns: "Bonferroni correction applied"
- Forbidden patterns: "ERROR", "convergence failed", "bootstrap failed"

**Expected Behavior on Validation Failure:**
Raise error with specific regression failure, log to logs/step03_reverse_models.log, provide model diagnostics

---

### Step 4: Extract Forward Prediction Results
**Dependencies:** Step 3 (reverse models) + RQ 7.1.1 completion
**Complexity:** Medium (~8 minutes)

**Purpose:** Extract forward prediction results from RQ 7.1.1 for bidirectional comparison

**Input:**
- Primary: results/ch7/7.1.1/data/step03_forward_models.csv (forward prediction results)
- Alternative: results/ch7/7.1.1/data/*forward*.csv (alternative forward patterns)
- Fallback: results/ch7/7.1.1/data/*regression*.csv (general regression files)
- Expected content: Forward R² values for RAVLT and BVMT predicting REMEMVR
- Current reverse: data/step03_reverse_models.csv

**Processing:**
- Attempt to load forward prediction results from RQ 7.1.1
- If RQ 7.1.1 not complete: proceed with reverse analysis only, note limitation
- If available: extract forward R² values for comparison
- Compute asymmetry ratios: Forward R² / Reverse R²
- Create bidirectional comparison table
- Test statistical difference in prediction strength using Williams' test for dependent correlations
- Bootstrap confidence intervals for asymmetry ratios:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling preserving paired structure

**Output:**
- data/step04_bidirectional_comparison.csv (forward vs reverse R² comparison)

**Validation Requirement:**
Validation tools MUST be used after comparison execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_bidirectional_comparison.csv: 2 rows x 8 columns
- Columns: test, forward_R2, reverse_R2, asymmetry_ratio, williams_t, williams_p, asymmetry_ci_lower, asymmetry_ci_upper
- Data types: test (object), numeric columns (float64)

*Value Ranges:*
- R² values in [0, 1] for both directions
- Asymmetry ratio > 0 (positive ratio of R² values)
- Williams t-statistic: any real number
- p-values in [0, 1]
- Asymmetry CIs: lower < ratio < upper

*Data Quality:*
- 2 comparisons (RAVLT and BVMT bidirectional)
- Forward data successfully matched to reverse results
- Williams test computed for both comparisons
- Bootstrap CIs valid for asymmetry ratios

*Log Validation:*
- Required patterns: "Forward results extracted from 7.1.1"
- Required patterns: "Bidirectional comparison complete"
- Required patterns: "Williams test computed"
- Acceptable warnings: "7.1.1 not available, reverse only"
- Forbidden patterns: "ERROR", "comparison failed"

**Expected Behavior on Validation Failure:**
If 7.1.1 unavailable: log warning, continue with reverse only; If extraction fails: raise error with specifics

---

### Step 5: Compute Effect Sizes
**Dependencies:** Step 3 (reverse models)
**Complexity:** Medium (~10 minutes including bootstrap)

**Purpose:** Compute effect sizes for reverse prediction with bootstrap confidence intervals

**Input:**
- data/step03_reverse_models.csv (regression results)
- data/step02_standardized_data.csv (for effect size calculations)

**Processing:**
- Cohen's f² calculation: f² = R² / (1 - R²)
- Semi-partial correlation computation for unique variance contribution
- Effect size interpretation using Cohen's benchmarks:
  - f² = 0.02 (small), f² = 0.15 (medium), f² = 0.35 (large)
- Bootstrap effect size confidence intervals:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - Compute f² and semi-partial r for each iteration
  - CI computation: percentile method (2.5th, 97.5th percentiles)
- Practical significance assessment alongside statistical significance

**Output:**
- data/step05_effect_sizes.csv (Cohen's f², semi-partial r, with CIs)

**Validation Requirement:**
Validation tools MUST be used after effect size computation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_effect_sizes.csv: 2 rows x 8 columns
- Columns: model, cohens_f2, f2_ci_lower, f2_ci_upper, semipartial_r, sr_ci_lower, sr_ci_upper, effect_interpretation
- Data types: model (object), numeric columns (float64), interpretation (object)

*Value Ranges:*
- Cohen's f² >= 0 (non-negative effect size)
- Semi-partial r in [-1, 1] (correlation bounds)
- f² typically < 2.0 (extremely large effects rare)
- CI bounds: lower < estimate < upper

*Data Quality:*
- Effect sizes computed for both models (RAVLT, BVMT)
- Bootstrap CIs valid (1000 successful iterations)
- Effect interpretations accurate (small/medium/large)
- No NaN or infinite values in effect sizes

*Log Validation:*
- Required patterns: "Effect sizes computed for 2 models"
- Required patterns: "Bootstrap complete: 1000 iterations"
- Required patterns: "Effect size interpretation assigned"
- Forbidden patterns: "ERROR", "invalid effect size", "bootstrap failed"

**Expected Behavior on Validation Failure:**
Raise error with specific computation failure, log to logs/step05_effect_sizes.log, provide effect size diagnostics

---

### Step 6: Model Diagnostics and Assumptions
**Dependencies:** Step 3 (reverse models)
**Complexity:** Medium (~12 minutes)

**Purpose:** Comprehensive regression assumption validation with remedial actions for violations

**Input:**
- data/step02_standardized_data.csv (for residual analysis)
- Fitted regression models from Step 3

**Processing:**
- Assumption checks with specific tests and thresholds:
  - Multicollinearity: VIF for predictors (single predictor, but check for future extensions)
  - Residual normality: Shapiro-Wilk test (p > 0.05) + Q-Q plots
  - Homoscedasticity: Breusch-Pagan test (p > 0.05)
  - Influential points: Cook's D < 4/n threshold (n=95-100, D < 0.04-0.042)
  - Linearity: Partial residual plots and LOESS trends
- Remedial actions for assumption violations:
  - Normality p < 0.05: Report bootstrap CIs as primary (already computed)
  - Heteroscedasticity p < 0.05: Compute HC3 robust standard errors
  - Outliers (Cook's D > threshold): Report sensitivity analysis with/without outliers
  - Non-linearity detected: Document and consider polynomial terms
- Create comprehensive diagnostics report with pass/fail for each assumption

**Output:**
- data/step06_model_diagnostics.csv (assumption test results with remedial actions)

**Validation Requirement:**
Validation tools MUST be used after diagnostics execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_model_diagnostics.csv: 2 rows x 10 columns  
- Columns: model, normality_p, bp_test_p, max_cooks_d, outlier_count, assumptions_met, remedial_action, robust_se_applied, outlier_analysis
- Data types: model (object), p-values/diagnostics (float64), flags (boolean), actions (object)

*Value Ranges:*
- p-values in [0, 1] (Shapiro-Wilk, Breusch-Pagan tests)
- Cook's D >= 0 (distance measure, non-negative)
- Outlier count >= 0 (integer count of flagged observations)
- Boolean flags: TRUE/FALSE for assumptions met

*Data Quality:*
- Diagnostic tests completed for both models
- Clear pass/fail status for each assumption
- Remedial actions specified when violations detected
- Outlier analysis completed with specific participant flags

*Log Validation:*
- Required patterns: "Assumption testing complete for 2 models"
- Required patterns: "Remedial actions evaluated"
- Required patterns: "Cook's D analysis complete"
- Acceptable warnings: "Assumption violation detected", "Robust SE applied"
- Forbidden patterns: "ERROR", "diagnostic failed", "unable to compute"

**Expected Behavior on Validation Failure:**
Report specific diagnostic failure, apply available remedial actions, log to logs/step06_diagnostics.log

---

### Step 7: Cross-Validation
**Dependencies:** Step 3 (reverse models)
**Complexity:** Medium (~10 minutes)

**Purpose:** Assess model generalizability and check for overfitting using k-fold cross-validation

**Input:**
- data/step02_standardized_data.csv (for CV procedure)

**Processing:**
- Implement 5-fold cross-validation using sklearn.model_selection.KFold:
  - Random seed: 42 for reproducibility
  - Shuffle: True (randomize before splitting)
  - Stratification: None for regression (consider quantile-based if outcome skewed)
- For each fold: fit model on training set (80%), evaluate on test set (20%)
- Compute cross-validation metrics:
  - Test R² for each fold (out-of-sample prediction accuracy)
  - RMSE and MAE for each fold
  - Mean and standard deviation across 5 folds
- Overfitting assessment:
  - Compare training R² vs mean test R²
  - Flag if train-test gap > 0.10 (overfitting threshold)
- Model stability assessment: SD of test R² across folds

**Output:**
- data/step07_cross_validation.csv (CV metrics and overfitting assessment)

**Validation Requirement:**
Validation tools MUST be used after cross-validation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_cross_validation.csv: 2 rows x 8 columns
- Columns: model, mean_test_R2, sd_test_R2, train_R2, generalization_gap, rmse_mean, mae_mean, overfitting_flag
- Data types: model (object), metrics (float64), flag (boolean)

*Value Ranges:*
- R² values in [0, 1] (coefficient bounds)
- RMSE, MAE >= 0 (error metrics non-negative)
- Generalization gap: any real number (can be negative if test > train)
- SD values >= 0 (standard deviation non-negative)

*Data Quality:*
- CV completed for both models (RAVLT and BVMT)
- All 5 folds completed successfully for each model
- Generalization gap computed (training vs test performance)
- Overfitting flags accurate (gap > 0.10 threshold)

*Log Validation:*
- Required patterns: "5-fold CV complete for 2 models"
- Required patterns: "Generalization assessment complete"
- Required patterns: "Model stability evaluated"
- Acceptable warnings: "Overfitting detected", "High CV variance"
- Forbidden patterns: "ERROR", "CV failed", "fold error"

**Expected Behavior on Validation Failure:**
Report specific CV failure, provide available partial results, log to logs/step07_cross_validation.log

---

### Step 8: Statistical Significance and Power Analysis
**Dependencies:** Steps 3, 5 (models and effect sizes)
**Complexity:** Medium (~8 minutes)

**Purpose:** Comprehensive significance testing with multiple comparison corrections and power analysis

**Input:**
- data/step03_reverse_models.csv (regression results with p-values)
- data/step05_effect_sizes.csv (observed effect sizes)

**Processing:**
- Multiple comparison correction summary:
  - Family: Within-RQ (2 regression models for reverse prediction)
  - Bonferroni: alpha = 0.05/2 = 0.025 per test (already computed in Step 3)
  - Chapter-level: alpha = 0.05/28 = 0.00179 (for Ch7 context)
  - FDR adjustment using Benjamini-Hochberg procedure
- Post-hoc power analysis:
  - Given: N=95-100, 1 predictor per model, alpha levels above
  - Calculate: achieved power for observed effect sizes
  - Use: statsmodels.stats.power.FTestAnovaPower()
  - Sensitivity: minimum detectable f² at 80% power
- Power interpretation:
  - If power < 0.80: acknowledge limitation in interpretation
  - Report confidence that null effects are true nulls vs underpowered

**Output:**
- data/step08_significance_power.csv (corrected p-values and power analysis)

**Validation Requirement:**
Validation tools MUST be used after significance testing execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_significance_power.csv: 2 rows x 8 columns
- Columns: model, p_uncorrected, p_bonferroni, p_chapter, p_fdr, achieved_power, min_detectable_f2, power_adequate
- Data types: model (object), p-values/power (float64), flag (boolean)

*Value Ranges:*
- All p-values in [0, 1] (valid probability range)
- Power in [0, 1] (probability bounds)
- Minimum detectable f² >= 0 (effect size threshold)
- Corrected p-values >= uncorrected p-values

*Data Quality:*
- Power analysis completed for both models
- Multiple correction methods applied correctly
- Power adequacy flags accurate (>= 0.80 threshold)
- Minimum detectable effects realistic

*Log Validation:*
- Required patterns: "Multiple comparisons corrected"
- Required patterns: "Power analysis complete for 2 models"
- Required patterns: "Sensitivity analysis complete"
- Acceptable warnings: "Low power detected", "Large correction applied"
- Forbidden patterns: "ERROR", "power computation failed"

**Expected Behavior on Validation Failure:**
Report specific significance testing failure, provide partial results, log to logs/step08_significance_power.log

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
1. **data/step00_dependency_validation.txt** - Dependency check results
2. **data/step01_merged_dataset.csv** - Theta scores + cognitive test scores merged  
3. **data/step02_standardized_data.csv** - T-score transformed variables (M=50, SD=10)
4. **data/step03_reverse_models.csv** - Reverse regression results with bootstrap CIs
5. **data/step04_bidirectional_comparison.csv** - Forward vs reverse R² comparison
6. **data/step05_effect_sizes.csv** - Cohen's f², semi-partial correlations with CIs
7. **data/step06_model_diagnostics.csv** - Assumption tests and remedial actions
8. **data/step07_cross_validation.csv** - 5-fold CV results and overfitting assessment  
9. **data/step08_significance_power.csv** - Corrected p-values and power analysis

### Logs (ONLY execution logs)
1. **logs/step00_validate_dependencies.log** - Dependency validation execution
2. **logs/step01_extract_data.log** - Data extraction and merging
3. **logs/step02_standardize_variables.log** - T-score transformation
4. **logs/step03_reverse_models.log** - Regression model fitting
5. **logs/step04_bidirectional_comparison.log** - Forward vs reverse comparison
6. **logs/step05_effect_sizes.log** - Effect size computation
7. **logs/step06_diagnostics.log** - Model diagnostics and assumptions
8. **logs/step07_cross_validation.log** - Cross-validation execution
9. **logs/step08_significance_power.log** - Significance testing and power

### Plots (EMPTY until rq_plots runs)
Plot source data will be created in data/ folder:
- **data/step03_reverse_scatter_plot_data.csv** - REMEMVR predicting cognitive tests
- **data/step04_bidirectional_plot_data.csv** - Forward vs reverse R² comparison
- **data/step06_diagnostics_plot_data.csv** - Residual plots and Q-Q plots

### Results (EMPTY until rq_results runs)
Will contain **results/summary.md** created by rq_results agent

---

## Expected Data Formats

### Step-to-Step Transformations
1. **Raw to Merged (Steps 0-1):** Extract theta_all from Ch5 5.1.1, merge with cognitive tests by UID
2. **Raw to T-scores (Step 2):** Transform all variables to M=50, SD=10 for comparability
3. **T-scores to Models (Step 3):** Fit reverse regression models with bootstrap CIs
4. **Models to Effects (Steps 4-5):** Extract R², compute effect sizes with interpretations
5. **Models to Validation (Steps 6-8):** Comprehensive assumption testing, CV, and power analysis

### Column Naming Conventions
- **UIDs:** Consistent participant identification across all files
- **T-scores:** REMEMVR_T, RAVLT_T, BVMT_T (standardized scores)
- **Model Results:** R2, adj_R2, beta, se, ci_lower, ci_upper (regression output)
- **Effect Sizes:** cohens_f2, semipartial_r (standardized effect measures)
- **P-values:** p_uncorrected, p_bonferroni, p_fdr (Decision D068 compliance)

### Data Type Constraints
- **Participant UIDs:** string/object type, no missing values
- **Numeric Measures:** float64, finite values only
- **Model Flags:** boolean type for binary indicators
- **Test Results:** float64 p-values in [0,1], effect sizes appropriately bounded

---

## Cross-RQ Dependencies

**Required Dependency:**
- **Ch5 5.1.1:** theta_all scores from omnibus IRT model (MUST complete through Step 3)
- **Primary Path:** results/ch5/5.1.1/data/step03_theta_scores.csv
- **Status Check:** results/ch5/5.1.1/status.yaml (rq_results: success)

**Optional Dependency:**
- **Ch7 7.1.1:** Forward prediction results for bidirectional comparison
- **Primary Path:** results/ch7/7.1.1/data/step03_forward_models.csv
- **Fallback:** Proceed with reverse analysis only if 7.1.1 unavailable

**Raw Data Dependencies:**
- **data/cache/master.xlsx:** RAVLT_Total and BVMT_TotR cognitive test scores
- **Required Columns:** UID, RAVLT_Total, BVMT_TotR
- **Expected N:** 100 participants with cognitive test data

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
[Complete 4-layer validation structure provided above]

#### Step 1: Extract Data
[Complete 4-layer validation structure provided above]

#### Step 2: Standardize Variables
[Complete 4-layer validation structure provided above]

#### Step 3: Fit Reverse Models  
[Complete 4-layer validation structure provided above]

#### Step 4: Bidirectional Comparison
[Complete 4-layer validation structure provided above]

#### Step 5: Effect Sizes
[Complete 4-layer validation structure provided above]

#### Step 6: Model Diagnostics
[Complete 4-layer validation structure provided above]

#### Step 7: Cross-Validation
[Complete 4-layer validation structure provided above]

#### Step 8: Significance and Power
[Complete 4-layer validation structure provided above]

---

## Summary

**Total Steps:** 9 (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** ~45 minutes total
**Cross-RQ Dependencies:** Ch5 5.1.1 (required), Ch7 7.1.1 (optional for comparison)
**Primary Outputs:** Reverse prediction models with comprehensive validation

**Key Hypothesis:** Moderate reverse prediction (R² = 0.25-0.35) suggesting shared but not identical constructs between REMEMVR and traditional cognitive tests

**Critical Methodological Notes:**
- Enhanced v5.1 specifications: All randomized procedures use seed=42 for reproducibility
- Bootstrap procedures: 1000 iterations, participant-level resampling for robust inference
- Multiple comparison corrections: Within-RQ Bonferroni + chapter-level context
- Cross-validation: 5-fold CV with overfitting detection (train-test R² gap > 0.10)
- Remedial actions: Specified for all assumption violations with robust alternatives
- Decision D068: Dual p-value reporting (uncorrected + corrected) throughout

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent with enhanced v5.1 statistical specifications