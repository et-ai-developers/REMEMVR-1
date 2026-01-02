# Analysis Plan: RQ 7.3.2 - Cognitive Predictors of Calibration Quality

**Research Question:** 7.3.2
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This analysis examines individual differences in calibration quality (how well confidence matches accuracy) using cognitive test scores as predictors. The research question tests whether metacognitive monitoring abilities correlate with specific cognitive capacities, particularly whether fluid intelligence (RPM) predicts calibration better than memory capacity measures (RAVLT, BVMT).

**Pipeline:** Multiple Linear Regression with Hierarchical Entry and Cross-Validation
**Steps:** 9 total analysis steps (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** ~45 minutes total

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Bonferroni correction: alpha = 0.05/3 = 0.0167 for 3 cognitive predictors
- Bootstrap confidence intervals with participant-level resampling

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies

**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch6 calibration outputs exist before proceeding

**Input:**
- results/ch6/6.2.*/status.yaml (verify Ch6 calibration RQs completion)
- results/ch6/6.2.*/data/*calibration*.csv (find calibration metrics)
- data/cache/master.xlsx (cognitive test scores)
- Expected Ch6 outputs: per-participant calibration quality measures

**Processing:**
- Check Ch6 6.2.x RQs completed successfully (status: success)
- Search for calibration metric files using pattern matching
- Verify master.xlsx contains RAVLT_T, BVMT_T, RPM_T columns
- Log dependency validation results
- If Ch6 outputs missing: QUIT with "Ch6 calibration analysis incomplete"

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file documenting validation results

*Value Ranges:*
- N/A (validation step produces text report only)

*Data Quality:*
- All required dependency files confirmed present
- Ch6 status verification successful
- Master.xlsx accessibility confirmed

*Log Validation:*
- Required patterns: "Ch6 dependencies verified", "master.xlsx accessible"
- Forbidden patterns: "ERROR", "FAIL", "missing", "not found"

**Expected Behavior on Validation Failure:**
Quit immediately with specific dependency error message. Do not proceed to data analysis steps.

### Step 1: Extract Calibration Metrics from Ch6

**Dependencies:** Step 0 (dependency validation)
**Complexity:** Medium (~5 minutes)

**Purpose:** Load and prepare per-participant calibration quality metrics from Ch6 outputs

**Input:**
- Primary: results/ch6/6.2.*/data/step*_calibration_metrics.csv
- Alternative: results/ch6/6.2.*/data/*calibration*.csv
- Fallback: results/ch6/6.2.*/data/participant_*_metrics.csv
- Expected content: Per-participant calibration measures (resolution, slope, or Brier reliability)

**Processing:**
- Locate calibration metric file using search patterns
- Extract per-participant calibration quality scores
- Standardize column names: UID, calibration_quality
- Handle different calibration metrics (resolution preferred, slope acceptable)
- Check for missing participants or invalid values
- Remove participants with NA calibration scores

**Output:**
- data/step01_calibration_metrics.csv

**Validation Requirement:**
Validation tools MUST be used after calibration extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_calibration_metrics.csv: 100 rows x 2 columns
- Columns: UID (object), calibration_quality (float64)

*Value Ranges:*
- calibration_quality in [0, 1] (calibration resolution bounds)
- UID format: consistent participant identifiers

*Data Quality:*
- All 100 participants present (or justified exclusions documented)
- No duplicate UIDs
- Missing calibration_quality < 5% (exclusion threshold)

*Log Validation:*
- Required patterns: "Calibration metrics extracted", "N participants: 100"
- Forbidden patterns: "ERROR", "FAIL", "no calibration data"

**Expected Behavior on Validation Failure:**
Log specific calibration extraction errors, check alternative Ch6 files, quit if no valid calibration data found.

### Step 2: Extract Cognitive Test Scores

**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (~5 minutes)

**Purpose:** Extract cognitive test T-scores from master.xlsx for regression predictors

**Input:**
- data/cache/master.xlsx (cognitive test scores)
- Required columns: UID, RAVLT_T, BVMT_T, RPM_T, Age, Sex, Education

**Processing:**
- Load master.xlsx, extract cognitive test section
- Verify T-score columns present and properly scaled
- Extract demographic controls: Age, Sex, Education
- Handle missing cognitive test data (exclude participants)
- Standardize column names and data types
- Check for outliers in T-scores (valid range: 20-80)

**Output:**
- data/step02_cognitive_tests.csv

**Validation Requirement:**
Validation tools MUST be used after cognitive test extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_cognitive_tests.csv: 100 rows x 6 columns
- Columns: UID (object), RAVLT_T (float64), BVMT_T (float64), RPM_T (float64), Age (int64), Sex (object), Education (int64)

*Value Ranges:*
- T-scores in [20, 80] (standard T-score range)
- Age in [18, 80] (adult participants)
- Education in [8, 20] (years of education)

*Data Quality:*
- All 100 participants present (or justified exclusions)
- No duplicate UIDs
- Missing cognitive scores < 5% per test

*Log Validation:*
- Required patterns: "Cognitive tests extracted", "T-scores validated"
- Forbidden patterns: "ERROR", "missing T-scores", "invalid range"

**Expected Behavior on Validation Failure:**
Log missing cognitive data, exclude affected participants, proceed if >= 90 participants remain.

### Step 3: Merge and Prepare Analysis Dataset

**Dependencies:** Steps 1-2 (calibration + cognitive data)
**Complexity:** Low (~5 minutes)

**Purpose:** Merge calibration metrics with cognitive tests, create final analysis dataset

**Input:**
- data/step01_calibration_metrics.csv (per-participant calibration)
- data/step02_cognitive_tests.csv (cognitive test T-scores)

**Processing:**
- Merge datasets on UID (inner join to retain complete cases only)
- Compute descriptive statistics for all variables
- Check data distribution (normality, skew, outliers)
- Standardize predictors (z-scores) for effect size interpretation
- Create analysis-ready dataset with complete cases
- Document final sample size and exclusions

**Output:**
- data/step03_analysis_input.csv
- data/step03_descriptive_stats.csv

**Validation Requirement:**
Validation tools MUST be used after data merging execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_analysis_input.csv: N rows x 7 columns (N >= 90)
- Columns: UID (object), calibration_quality (float64), RAVLT_T (float64), BVMT_T (float64), RPM_T (float64), Age (int64), Sex (object), Education (int64)
- data/step03_descriptive_stats.csv: summary statistics

*Value Ranges:*
- All variables within expected ranges (per previous steps)
- Standardized predictors approximately z-scored (mean ~0, SD ~1)

*Data Quality:*
- Complete cases only (no missing data)
- Final N >= 90 participants
- UID consistency verified across datasets

*Log Validation:*
- Required patterns: "Merge complete", "Final N = XX", "No missing data"
- Forbidden patterns: "ERROR", "merge failed", "missing values"

**Expected Behavior on Validation Failure:**
Check merge keys, investigate data quality issues, quit if final N < 90.

### Step 4: Hierarchical Multiple Regression Analysis

**Dependencies:** Step 3 (merged analysis dataset)
**Complexity:** High (~10 minutes including bootstrap)

**Purpose:** Fit hierarchical regression models to test cognitive predictors of calibration quality

**Input:**
- data/step03_analysis_input.csv (complete analysis dataset)

**Processing:**
- Model 1: calibration_quality ~ Age + Sex + Education (demographic controls)
- Model 2: calibration_quality ~ Age + Sex + Education + RAVLT_T + BVMT_T + RPM_T (+ cognitive predictors)
- Fit both models using statsmodels.api.OLS
- Extract R², adjusted R², F-statistics for model comparison
- Compute delta-R² and F-test for model improvement (Model 2 vs Model 1)
- Extract coefficients with standard errors and 95% confidence intervals
- Multiple comparison correction:
  - Family: Within-RQ cognitive predictors (3 tests: RAVLT, BVMT, RPM)
  - Bonferroni: alpha = 0.05/3 = 0.0167 per cognitive predictor
  - Also compute FDR using Benjamini-Hochberg
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Bootstrap 95% CIs for coefficients:
  - Iterations: 1000
  - Seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - CI: Percentile method (2.5th, 97.5th percentiles)

**Output:**
- data/step04_model1_demographics.csv (demographic model results)
- data/step04_model2_cognitive.csv (full model results)
- data/step04_model_comparison.csv (hierarchical comparison)
- data/step04_bootstrap_cis.csv (bootstrap confidence intervals)

**Validation Requirement:**
Validation tools MUST be used after hierarchical regression execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_model1_demographics.csv: 3 rows x 6 columns (demographic predictors)
- data/step04_model2_cognitive.csv: 6 rows x 8 columns (all predictors with dual p-values)
- data/step04_model_comparison.csv: 1 row x 5 columns (model comparison metrics)
- data/step04_bootstrap_cis.csv: 6 rows x 4 columns (bootstrap CIs for all predictors)

*Value Ranges:*
- R² in [0, 1] (proportion variance explained)
- F-statistics > 0 (test statistics)
- p-values in [0, 1] (valid probabilities)
- Beta coefficients approximately standardized (range: [-1, 1] for most predictors)

*Data Quality:*
- All models converged successfully
- No NaN values in coefficient estimates
- Bootstrap CIs valid (ci_lower < beta < ci_upper)
- Dual p-values present for cognitive predictors (D068)

*Log Validation:*
- Required patterns: "Model 1 fitted", "Model 2 fitted", "Bootstrap complete: 1000 iterations"
- Forbidden patterns: "ERROR", "convergence failed", "singular matrix"

**Expected Behavior on Validation Failure:**
Check model specification, investigate convergence issues, consider robust estimation methods.

### Step 5: Assumption Validation and Diagnostics

**Dependencies:** Step 4 (regression models)
**Complexity:** Medium (~8 minutes)

**Purpose:** Validate regression assumptions and compute diagnostic statistics

**Input:**
- data/step04_model2_cognitive.csv (full model results for residual extraction)
- Model 2 fitted object for residual analysis

**Processing:**
- Check assumptions with formal tests and visual diagnostics:
  - Multicollinearity: VIF for each cognitive predictor
  - Residual normality: Shapiro-Wilk test + Q-Q plot data
  - Homoscedasticity: Breusch-Pagan test + residual vs fitted data
  - Linearity: Partial residual plots for continuous predictors
  - Independence: Assumption met by cross-sectional design
  - Outliers: Cook's distance, leverage, standardized residuals
- Remedial actions if violated:
  - Normality p < 0.05: Report bootstrap CIs as primary (already computed)
  - Heteroscedasticity p < 0.05: Compute HC3 robust standard errors
  - VIF > 5: Document multicollinearity, consider ridge if VIF > 10
  - Outliers (Cook's D > 4/N): Report results with and without outliers

**Output:**
- data/step05_assumption_tests.csv (formal test results)
- data/step05_diagnostic_plots_data.csv (data for diagnostic plots)
- data/step05_outlier_analysis.csv (influential point analysis)
- data/step05_robust_ses.csv (HC3 standard errors if needed)

**Validation Requirement:**
Validation tools MUST be used after assumption validation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_assumption_tests.csv: 4 rows x 3 columns (test results)
- data/step05_diagnostic_plots_data.csv: N rows x 5 columns (plot data)
- data/step05_outlier_analysis.csv: N rows x 4 columns (diagnostic measures)
- data/step05_robust_ses.csv: 6 rows x 3 columns (robust SEs if computed)

*Value Ranges:*
- VIF in [1, 20] (multicollinearity measure, concern if > 5)
- Cook's D in [0, 1] (influence measure, concern if > 4/N)
- Standardized residuals in [-4, 4] (extreme outliers if |z| > 3)
- Test p-values in [0, 1]

*Data Quality:*
- All diagnostic tests completed
- Outlier identification systematic
- Remedial actions triggered appropriately

*Log Validation:*
- Required patterns: "Assumptions checked", "Diagnostics complete"
- Acceptable patterns: "Normality violated - bootstrap CIs reported", "Outliers detected: N cases"
- Forbidden patterns: "ERROR", "diagnostic failed"

**Expected Behavior on Validation Failure:**
Document assumption violations, apply remedial actions, proceed with appropriate statistical corrections.

### Step 6: Effect Size Calculation and Interpretation

**Dependencies:** Steps 4-5 (regression results + diagnostics)
**Complexity:** Medium (~5 minutes)

**Purpose:** Compute comprehensive effect sizes and importance measures for interpretation

**Input:**
- data/step04_model2_cognitive.csv (full model coefficients)
- data/step04_model_comparison.csv (model R² values)

**Processing:**
- Overall effect sizes:
  - Cohen's f² = R²/(1-R²) for Model 2
  - Interpretation: f² >= 0.02 small, >= 0.15 medium, >= 0.35 large
- Individual predictor importance:
  - Standardized beta coefficients (already computed)
  - Semi-partial correlations (sr²) for unique variance
  - Relative importance within cognitive predictors
- Effect size confidence intervals from bootstrap results
- Context interpretation:
  - Individual differences research: R² of 0.10-0.20 represents meaningful prediction
  - Compare to accuracy prediction from RQ 7.1.1 (if available)

**Output:**
- data/step06_effect_sizes.csv (comprehensive effect size measures)
- data/step06_importance_analysis.csv (predictor importance rankings)

**Validation Requirement:**
Validation tools MUST be used after effect size calculation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_effect_sizes.csv: 1 row x 6 columns (model effect sizes)
- data/step06_importance_analysis.csv: 3 rows x 5 columns (cognitive predictor importance)

*Value Ranges:*
- Cohen's f² in [0, 5] (effect size measure)
- R² in [0, 1] (variance explained)
- Semi-partial r² in [0, R²] (cannot exceed total variance)
- Standardized betas approximately in [-1, 1]

*Data Quality:*
- Effect size calculations mathematically consistent
- Importance rankings logical (sum of sr² <= R²)
- Bootstrap CIs properly integrated

*Log Validation:*
- Required patterns: "Effect sizes computed", "Importance analysis complete"
- Forbidden patterns: "ERROR", "invalid effect size"

**Expected Behavior on Validation Failure:**
Check computation logic, verify input data quality, ensure mathematical consistency.

### Step 7: Cross-Validation Analysis

**Dependencies:** Steps 3-4 (analysis dataset + regression models)
**Complexity:** High (~10 minutes)

**Purpose:** Assess model generalizability using k-fold cross-validation

**Input:**
- data/step03_analysis_input.csv (complete analysis dataset)

**Processing:**
- Implement 5-fold cross-validation using sklearn.model_selection.KFold
- Random seed: 42 for reproducibility
- Shuffle: True (randomize before splitting)
- Stratification: Use quantile-based stratification on calibration_quality (5 quantiles)
- For each fold:
  - Split data: 80% training, 20% testing
  - Fit Model 2 on training set
  - Predict on test set
  - Compute R², RMSE, MAE
- Aggregate results across folds:
  - Mean and standard deviation of test R²
  - Mean and standard deviation of RMSE
  - Compare training vs test performance
- Overfitting assessment:
  - Flag if train-test R² gap > 0.10
  - Compute generalization gap for each fold

**Output:**
- data/step07_cv_results.csv (cross-validation metrics by fold)
- data/step07_cv_summary.csv (aggregated CV performance)

**Validation Requirement:**
Validation tools MUST be used after cross-validation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_cv_results.csv: 5 rows x 6 columns (per-fold results)
- data/step07_cv_summary.csv: 1 row x 8 columns (aggregated metrics)

*Value Ranges:*
- Test R² in [0, 1] (cannot exceed training R²)
- RMSE > 0 (positive prediction errors)
- MAE > 0 (positive absolute errors)
- Generalization gap in [-1, 1] (train R² - test R²)

*Data Quality:*
- All 5 folds completed successfully
- No fold with extreme performance (outlier detection)
- Cross-validation metrics internally consistent

*Log Validation:*
- Required patterns: "5-fold CV complete", "Mean test R² = X.XX"
- Acceptable patterns: "Overfitting detected: gap = X.XX" (if gap > 0.10)
- Forbidden patterns: "ERROR", "fold failed", "convergence"

**Expected Behavior on Validation Failure:**
Check fold construction, investigate convergence issues, ensure data splitting integrity.

### Step 8: Comparison with Accuracy Prediction

**Dependencies:** Step 4-6 (calibration prediction results)
**Complexity:** Medium (~7 minutes)

**Purpose:** Compare calibration prediction with accuracy prediction from RQ 7.1.1

**Input:**
- data/step06_effect_sizes.csv (calibration prediction effect sizes)
- Primary: results/ch7/7.1.1/data/step06_effect_sizes.csv (accuracy prediction)
- Alternative: results/ch7/7.1.1/data/*effect*.csv
- Fallback: Proceed without comparison if 7.1.1 incomplete

**Processing:**
- Load accuracy prediction results from RQ 7.1.1 (if available)
- Compare R² values: calibration vs accuracy prediction
- Compare individual predictor effects:
  - Which tests predict calibration vs accuracy differently?
  - Identify divergent cognitive predictors
- Effect size comparison:
  - Expected: R²_calibration < R²_accuracy (calibration harder to predict)
  - Document magnitude of difference
- Theoretical interpretation:
  - Connect to confidence-accuracy dissociation from Ch6
  - Support for metacognitive vs performance distinction

**Output:**
- data/step08_calibration_vs_accuracy.csv (comparative analysis)
- data/step08_predictor_comparison.csv (predictor-specific comparisons)

**Validation Requirement:**
Validation tools MUST be used after comparison analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_calibration_vs_accuracy.csv: 1 row x 6 columns (R² comparison)
- data/step08_predictor_comparison.csv: 3 rows x 8 columns (predictor-wise comparison)

*Value Ranges:*
- R² differences in [-1, 1] (calibration vs accuracy)
- Beta coefficient differences approximately in [-2, 2]
- All p-values in [0, 1]

*Data Quality:*
- Comparison data properly aligned by predictor
- Missing 7.1.1 data handled gracefully
- Difference calculations mathematically correct

*Log Validation:*
- Required patterns: "Comparison analysis complete"
- Acceptable patterns: "RQ 7.1.1 data not available - comparison skipped"
- Forbidden patterns: "ERROR", "comparison failed"

**Expected Behavior on Validation Failure:**
Check file paths for 7.1.1 results, proceed with calibration analysis only if comparison data unavailable.

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)

- data/step00_dependency_validation.txt (prerequisite verification)
- data/step01_calibration_metrics.csv (Ch6 calibration extracts)
- data/step02_cognitive_tests.csv (master.xlsx cognitive scores)
- data/step03_analysis_input.csv (merged analysis dataset)
- data/step03_descriptive_stats.csv (descriptive statistics)
- data/step04_model1_demographics.csv (demographic model)
- data/step04_model2_cognitive.csv (full cognitive model)
- data/step04_model_comparison.csv (hierarchical comparison)
- data/step04_bootstrap_cis.csv (bootstrap confidence intervals)
- data/step05_assumption_tests.csv (assumption validation results)
- data/step05_diagnostic_plots_data.csv (diagnostic plot source data)
- data/step05_outlier_analysis.csv (influential point analysis)
- data/step05_robust_ses.csv (robust standard errors if computed)
- data/step06_effect_sizes.csv (comprehensive effect sizes)
- data/step06_importance_analysis.csv (predictor importance)
- data/step07_cv_results.csv (cross-validation by fold)
- data/step07_cv_summary.csv (aggregated CV metrics)
- data/step08_calibration_vs_accuracy.csv (comparison with 7.1.1)
- data/step08_predictor_comparison.csv (predictor-wise comparison)

### Logs (ONLY execution logs)

- logs/step00_validate_dependencies.log
- logs/step01_extract_calibration.log
- logs/step02_extract_cognitive.log
- logs/step03_merge_prepare.log
- logs/step04_hierarchical_regression.log
- logs/step05_assumption_validation.log
- logs/step06_effect_sizes.log
- logs/step07_cross_validation.log
- logs/step08_comparison_analysis.log

### Plots (EMPTY until rq_plots runs)

Note: Diagnostic plot source data created in data/step05_diagnostic_plots_data.csv for later visualization.

### Results (EMPTY until rq_results runs)

Note: summary.md created by rq_results will synthesize all analysis outputs.

---

## Expected Data Formats

### Step-to-Step Transformations

1. **Step 0 -> Step 1:** Dependency validation enables calibration extraction
2. **Step 1 -> Step 2:** Parallel extraction of calibration and cognitive data
3. **Step 2 -> Step 3:** Merge on UID creates analysis-ready dataset
4. **Step 3 -> Step 4:** Analysis dataset flows into hierarchical regression
5. **Step 4 -> Step 5:** Fitted models enable assumption validation
6. **Step 5 -> Step 6:** Validated models support effect size calculation
7. **Step 6 -> Step 7:** Effect sizes inform cross-validation interpretation
8. **Step 7 -> Step 8:** All results enable comparison with accuracy prediction

### Column Naming Conventions

- **Participant ID:** UID (consistent across all files)
- **Cognitive predictors:** RAVLT_T, BVMT_T, RPM_T (T-score standardized)
- **Outcome:** calibration_quality (per-participant calibration metric)
- **Demographics:** Age, Sex, Education
- **Statistics:** beta, se, ci_lower, ci_upper, p_uncorrected, p_bonferroni, p_fdr
- **Diagnostics:** vif, cooks_d, leverage, std_resid

### Data Type Constraints

- **UID:** object (string identifier, non-nullable)
- **Cognitive scores:** float64 (T-scores, range 20-80)
- **Calibration quality:** float64 (proportion, range 0-1)
- **Age, Education:** int64 (years, non-nullable)
- **Sex:** object (categorical, non-nullable)
- **Statistics:** float64 (nullable for failed computations)

---

## Cross-RQ Dependencies

### Required Dependencies

**Ch6 Calibration Analysis (6.2.x series):**
- **Purpose:** Per-participant calibration quality metrics
- **Primary path:** results/ch6/6.2.*/data/step*_calibration_metrics.csv
- **Alternative:** results/ch6/6.2.*/data/*calibration*.csv
- **Fallback:** results/ch6/6.2.*/data/participant_*_metrics.csv
- **Content:** Per-participant calibration measures (resolution, slope, Brier reliability)
- **If missing:** QUIT with "Ch6 calibration analysis incomplete, required for individual differences prediction"

### Optional Dependencies

**RQ 7.1.1 Accuracy Prediction:**
- **Purpose:** Comparison between calibration and accuracy prediction
- **Primary path:** results/ch7/7.1.1/data/step06_effect_sizes.csv
- **If missing:** Proceed with calibration analysis only, skip comparison

### Dependency Management Strategy

- **Step 0:** Verify all required dependencies exist before analysis
- **Graceful degradation:** Proceed without optional dependencies
- **Clear documentation:** Log all dependency checks and fallback actions

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
Full 4-layer validation structure ensures all required Ch6 outputs and master.xlsx are accessible before analysis begins.

#### Step 1: Extract Calibration Metrics  
4-layer validation confirms successful extraction of per-participant calibration measures with expected ranges and data quality.

#### Step 2: Extract Cognitive Tests
4-layer validation verifies cognitive test scores within T-score ranges and complete demographic data.

#### Step 3: Merge Analysis Dataset
4-layer validation ensures successful data merging with complete cases and expected sample size.

#### Step 4: Hierarchical Regression
4-layer validation confirms model convergence, coefficient ranges, and dual p-value reporting per Decision D068.

#### Step 5: Assumption Validation
4-layer validation verifies diagnostic test completion and appropriate remedial actions for violations.

#### Step 6: Effect Size Calculation
4-layer validation ensures mathematically consistent effect size computations and importance rankings.

#### Step 7: Cross-Validation
4-layer validation confirms successful k-fold completion with realistic performance metrics and overfitting assessment.

#### Step 8: Comparison Analysis  
4-layer validation verifies comparison calculations and handles missing 7.1.1 data gracefully.

---

## Summary

**Total Steps:** 9 (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** ~45 minutes total
**Cross-RQ Dependencies:** Ch6 6.2.x calibration analysis (required), RQ 7.1.1 accuracy prediction (optional)
**Primary Outputs:** Hierarchical regression results, effect sizes, cross-validation metrics, calibration vs accuracy comparison

**Key Hypothesis:** Fluid intelligence (RPM) will predict calibration quality more strongly than memory capacity tests (RAVLT, BVMT), supporting the theory that metacognitive monitoring requires executive reasoning abilities distinct from memory encoding processes.

**Critical Methodological Notes:**
- Conservative multiple comparison correction (Bonferroni alpha = 0.0167)
- Bootstrap confidence intervals with 1000 iterations and participant-level resampling
- Comprehensive assumption validation with specified remedial actions
- Cross-validation to assess generalizability (5-fold, seed=42)
- Decision D068 dual p-value reporting implemented throughout

**Validation Coverage:** 100% (all 9 steps have complete 4-layer validation requirements)

**Statistical Implementation Enhancements (v5.1):**
- All randomized procedures use seed=42 for reproducibility
- Bootstrap specifications include iteration count, resampling method, and CI calculation
- Cross-validation includes fold count, stratification, and overfitting thresholds
- Multiple comparison corrections explicitly calculated and dual-reported
- Assumption violation remedial actions specified for each diagnostic test

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent v5.1.0 with enhanced statistical specifications