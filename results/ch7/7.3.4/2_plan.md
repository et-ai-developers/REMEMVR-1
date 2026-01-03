# Analysis Plan: RQ 7.3.4 - Does DASS predict metacognition more than memory?

**Research Question:** 7.3.4
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ tests differential prediction patterns using DASS-21 scores (Depression, Anxiety, Stress) as predictors of three dependent variables: memory accuracy (theta scores), confidence scores, and calibration metrics. The core hypothesis tests whether anxiety/depression specifically impairs metacognitive monitoring (confidence, calibration) more than memory encoding (accuracy), based on executive function and processing efficiency theories.

**Pipeline:** Multiple Linear Regression with Cross-Model Beta Comparison
**Steps:** 8 total analysis steps (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** ~45 minutes

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Chapter 7 Bonferroni correction: alpha = 0.05/28 = 0.00179 for family-wise correction
- Within-RQ Bonferroni: alpha = 0.05/9 = 0.0056 for 9 coefficient comparisons (3 predictors x 3 models)

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 and Ch6 outputs exist before proceeding with DASS analysis

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv (omnibus theta scores)
- Alternative: results/ch5/5.1.1/data/*theta*.csv (theta score patterns)
- Primary: results/ch6/6.1.1/data/confidence_scores.csv (confidence metrics)
- Alternative: results/ch6/6.2.1/data/calibration_scores.csv (calibration metrics)
- Fallback: results/ch6/*/data/*confidence*.csv or *calibration*.csv
- Required: data/cache/master.xlsx (DASS-21 scores)

**Processing:**
- Check Ch5 5.1.1 and Ch6 completion status in status.yaml files
- Locate theta scores file (try multiple naming patterns)
- Locate confidence and calibration files (try multiple Ch6 RQs)
- Verify master.xlsx contains DASS_Dep, DASS_Anx, DASS_Str columns
- Log all dependency validation results with specific paths found
- If any critical file missing: QUIT with specific error message

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: Text file with validation results
- Contains: File paths found, status checks, data dimensions verified

*Value Ranges:*
- Dependencies found: TRUE/FALSE for each required file
- Status checks: "success" for prerequisite RQs

*Data Quality:*
- All 4 required data sources accessible
- No missing critical files
- Consistent participant UIDs across datasets

*Log Validation:*
- Required patterns: "Dependency validation complete", "All files accessible"
- Forbidden patterns: "ERROR", "MISSING", "QUIT"
- Acceptable warnings: None (all dependencies must exist)

**Expected Behavior on Validation Failure:**
Quit immediately with specific missing file error, log to logs/step00_validate_dependencies.log

---

### Step 1: Extract and Prepare DASS Scores
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (~5 minutes)

**Purpose:** Extract DASS-21 subscale scores from master.xlsx and prepare for analysis

**Input:**
- data/cache/master.xlsx (DASS_Dep, DASS_Anx, DASS_Str columns)
- Participant UID list from dependency validation

**Processing:**
- Load master.xlsx, extract columns: UID, DASS_Dep, DASS_Anx, DASS_Str
- Filter to participants with complete DASS data (expect ~97 participants)
- Check for missing data patterns and outliers (z-score > 3.29)
- Transform DASS scores to z-scores for standardization
- Compute descriptive statistics: mean, SD, range, skewness per subscale
- Check intercorrelations between DASS subscales (expect r > 0.70)
- Save extracted data with original and standardized scores

**Output:**
- data/step01_dass_scores.csv (UID, DASS_Dep, DASS_Anx, DASS_Str, plus z-scored versions)

**Validation Requirement:**
Validation tools MUST be used after DASS extraction tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_dass_scores.csv: ~97 rows x 7 columns
- Columns: UID (object), DASS_Dep (float64), DASS_Anx (float64), DASS_Str (float64), z_Dep (float64), z_Anx (float64), z_Str (float64)

*Value Ranges:*
- DASS raw scores in [0, 42] (DASS-21 subscales range 0-21, doubled for severity)
- z-scores in [-3.29, 3.29] (standard outlier range)
- Correlations between subscales in [0.5, 0.9] (expected high correlation)

*Data Quality:*
- N = 95-99 participants (expect ~97 with complete DASS data)
- No missing values in DASS columns
- No duplicate UIDs
- z-scores properly centered (mean ~0, SD ~1)

*Log Validation:*
- Required patterns: "DASS extraction complete", "N=XX participants with complete data"
- Required patterns: "Intercorrelations computed", "z-scores standardized"
- Forbidden patterns: "ERROR", "missing data", "correlation > 0.95"

**Expected Behavior on Validation Failure:**
Log warning if <95 participants, quit if <90 participants or intercorrelation >0.95 (multicollinearity concern)

---

### Step 2: Load and Merge Dependent Variables
**Dependencies:** Step 1 (DASS scores extracted)
**Complexity:** Medium (~10 minutes)

**Purpose:** Load theta scores, confidence scores, and calibration metrics; merge into analysis dataset

**Input:**
- data/step01_dass_scores.csv (DASS predictors)
- From Step 0 validation: Ch5 theta file path, Ch6 confidence file path, Ch6 calibration file path
- Expected formats: UID column plus outcome measures

**Processing:**
- Load theta scores (memory accuracy measure)
- Load confidence scores (mean confidence per participant)  
- Load calibration scores (confidence-accuracy correlation or calibration metric)
- Merge all datasets on UID (inner join to keep complete cases only)
- Check for outliers in DVs using IQR method (Q3 + 1.5*IQR threshold)
- Compute descriptive statistics for all three outcomes
- Check bivariate correlations between accuracy, confidence, calibration
- Ensure sufficient variance in each outcome (CV > 0.10)

**Output:**
- data/step02_analysis_dataset.csv (UID, DASS predictors, 3 outcome measures)

**Validation Requirement:**
Validation tools MUST be used after data merging tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_analysis_dataset.csv: ~95 rows x 7-10 columns  
- Columns: UID, z_Dep, z_Anx, z_Str, theta_accuracy, confidence, calibration (plus descriptive stats)

*Value Ranges:*
- theta_accuracy in [-3, 3] (IRT ability scale)
- confidence in [1, 4] or [0, 100] (depends on Ch6 scaling)
- calibration in [-1, 1] (correlation-based) or [0, 1] (calibration index)
- All predictors z-scored: mean ~0, SD ~1

*Data Quality:*
- N = 90-97 participants (complete cases after merge)
- No missing values in analysis variables
- No duplicate UIDs
- CV > 0.10 for all outcome variables (sufficient variance)
- No extreme outliers (>3 SD) in outcomes

*Log Validation:*
- Required patterns: "Merge complete: N=XX participants", "All variables have CV > 0.10"
- Required patterns: "Outlier check complete", "Descriptives computed"
- Forbidden patterns: "ERROR", "merge failed", "insufficient variance"

**Expected Behavior on Validation Failure:**
Quit if N < 90, log warning if CV < 0.10 for any outcome, proceed with outlier flagging if detected

---

### Step 3: Fit Multiple Regression Models
**Dependencies:** Step 2 (merged analysis dataset)
**Complexity:** Medium (~10 minutes including diagnostics)

**Purpose:** Fit three separate regression models to test differential prediction patterns

**Input:**
- data/step02_analysis_dataset.csv (complete analysis dataset)

**Processing:**
- Fit Model 1: Accuracy ~ z_Dep + z_Anx + z_Str
- Fit Model 2: Confidence ~ z_Dep + z_Anx + z_Str  
- Fit Model 3: Calibration ~ z_Dep + z_Anx + z_Str
- Implementation: statsmodels.api.OLS with standardized predictors
- For each model extract: R², adjusted R², F-statistic, standardized betas, SEs
- Bootstrap 95% CIs for all coefficients:
  - Iterations: 1000
  - Random seed: 42
  - Method: Participant-level resampling with replacement
  - CI: Percentile method (2.5th, 97.5th percentiles)
- Multiple comparison correction within each model:
  - Family: Within-model (3 predictors per model)
  - Bonferroni: alpha = 0.05/3 = 0.0167 per test within model
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Check assumptions for each model:
  - Normality: Shapiro-Wilk test on residuals (p > 0.05)
  - Homoscedasticity: Breusch-Pagan test (p > 0.05)
  - Multicollinearity: VIF for each predictor (VIF < 5)
  - Independence: Durbin-Watson test (statistic ~2.0)
  - Linearity: Partial residual plots visual inspection
- Remedial actions if violated:
  - Normality p < 0.05: Report bootstrap CIs as primary, log transformation if severe
  - Heteroscedasticity p < 0.05: Add HC3 robust SEs
  - VIF > 5: Document multicollinearity concern, consider principal components if VIF > 10
  - Independence DW < 1.5 or > 2.5: Report concern, consider clustered SEs
  - Linearity violations: Report with acknowledgment, consider polynomial terms

**Output:**
- data/step03_model_results.csv (coefficients, CIs, dual p-values for all 3 models)
- data/step03_model_diagnostics.csv (assumption tests for all 3 models)

**Validation Requirement:**
Validation tools MUST be used after regression model fitting tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_model_results.csv: 9 rows x 10 columns (3 models x 3 predictors each)
- Columns: model, predictor, beta, se, ci_lower, ci_upper, p_uncorrected, p_bonferroni, vif, r_squared
- data/step03_model_diagnostics.csv: 3 rows x 8 columns (1 per model)  
- Columns: model, shapiro_p, bp_p, dw_stat, min_vif, max_vif, r_squared, adj_r_squared

*Value Ranges:*
- beta in [-1, 1] (standardized predictors and reasonable effect sizes)
- se > 0 (positive standard errors)
- p-values in [0, 1]
- VIF in [1, 10] (multicollinearity acceptable range)
- R² in [0, 1], adj_R² <= R²
- Durbin-Watson in [1, 3] (independence acceptable range)

*Data Quality:*
- All 9 coefficient estimates present (3 models x 3 predictors)
- Bootstrap CIs valid (ci_lower < beta < ci_upper for most coefficients)
- Dual p-values present for all coefficients (Decision D068)
- All assumption tests completed without errors

*Log Validation:*
- Required: "Model 1 fitted: R² = X.XX", "Model 2 fitted: R² = X.XX", "Model 3 fitted: R² = X.XX"
- Required: "Bootstrap complete: 1000 iterations", "Assumption checks complete"
- Required: "Diagnostics: normality p=X.XX, homoscedasticity p=X.XX"
- Forbidden: "ERROR", "convergence failed", "bootstrap failed"

**Expected Behavior on Validation Failure:**
Log assumption violations but proceed, quit only if model fitting fails or bootstrap fails completely

---

### Step 4: Compare Beta Coefficients Across Models
**Dependencies:** Step 3 (fitted regression models)
**Complexity:** High (~10 minutes with statistical tests)

**Purpose:** Test differential prediction hypothesis by comparing standardized beta coefficients across models

**Input:**
- data/step03_model_results.csv (fitted model coefficients)
- Fitted model objects for statistical comparison tests

**Processing:**
- Extract standardized betas for each DASS predictor from all 3 models
- Primary comparison: DASS_Anxiety coefficient differences
  - Compare: beta_Anx_Confidence vs beta_Anx_Accuracy
  - Compare: beta_Anx_Calibration vs beta_Anx_Accuracy  
  - Compare: beta_Anx_Confidence vs beta_Anx_Calibration
- Statistical tests for beta differences using bootstrap approach:
  - Bootstrap coefficient differences (1000 iterations, seed=42)
  - Compute 95% CI for difference: (beta_meta - beta_memory)
  - If CI excludes 0: significant differential prediction
- Secondary comparisons: DASS_Depression and DASS_Stress patterns
- Multiple comparison correction across all 9 comparisons:
  - Family: All within-RQ coefficient comparisons (3 predictors x 3 model pairs = 9 tests)
  - Bonferroni: alpha = 0.05/9 = 0.0056 per test
  - FDR correction using Benjamini-Hochberg method
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Effect size interpretation using Cohen (1988) guidelines:
  - Small effect: |difference| > 0.10
  - Medium effect: |difference| > 0.30
  - Large effect: |difference| > 0.50

**Output:**
- data/step04_beta_comparisons.csv (all pairwise coefficient differences with tests)

**Validation Requirement:**
Validation tools MUST be used after beta comparison tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_beta_comparisons.csv: 9 rows x 9 columns  
- Columns: comparison, predictor, model1, model2, beta_diff, ci_lower, ci_upper, p_uncorrected, p_bonferroni, p_fdr

*Value Ranges:*
- beta_diff in [-2, 2] (reasonable range for standardized coefficient differences)
- p-values in [0, 1]
- CIs valid: ci_lower < beta_diff < ci_upper
- Effect size categories: small/medium/large based on |beta_diff|

*Data Quality:*
- All 9 comparisons present (3 predictors x 3 model pairs)
- Bootstrap CIs computed successfully
- Triple p-value reporting (uncorrected, Bonferroni, FDR) per Decision D068
- Consistent predictor labeling across comparisons

*Log Validation:*
- Required: "Beta comparisons complete: 9 tests", "Bootstrap differences: 1000 iterations"
- Required: "Multiple corrections applied: Bonferroni and FDR"
- Required: "Differential prediction test complete"
- Forbidden: "ERROR", "bootstrap failed", "comparison failed"

**Expected Behavior on Validation Failure:**
Log specific comparison failures but continue, quit only if all comparisons fail

---

### Step 5: Cross-Validation Assessment
**Dependencies:** Step 3 (fitted models)
**Complexity:** Medium (~10 minutes)

**Purpose:** Assess model generalizability and check for overfitting using cross-validation

**Input:**
- data/step02_analysis_dataset.csv (complete data for CV)
- Model specifications from Step 3

**Processing:**
- Implement 5-fold cross-validation for all three models:
  - Random seed: 42 for reproducibility
  - Stratification: None (continuous outcomes)
  - Shuffle: True (randomize before splitting)
  - For each fold: fit on training (80%), evaluate on test (20%)
- Cross-validation metrics per model:
  - Test R²: Mean and SD across 5 folds
  - RMSE: Root mean squared error on test sets
  - MAE: Mean absolute error on test sets
- Overfitting assessment:
  - Compute train-test R² gap for each fold
  - Flag overfitting if mean gap > 0.10
  - Compute shrinkage: (train_R² - test_R²) / train_R²
- Bootstrap 95% CIs for CV metrics:
  - Iterations: 200 (lighter for CV)
  - Random seed: 42
  - Resample folds WITH replacement
  - CI: Percentile method for mean test R²

**Output:**
- data/step05_cross_validation.csv (CV metrics for all 3 models)

**Validation Requirement:**
Validation tools MUST be used after cross-validation tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_cross_validation.csv: 3 rows x 8 columns
- Columns: model, test_r2_mean, test_r2_sd, rmse_mean, mae_mean, train_test_gap, shrinkage, overfitting_flag

*Value Ranges:*
- test_r2_mean in [0, 1], typically [0.05, 0.40] for this analysis
- test_r2_sd > 0 (variability across folds)
- RMSE > 0, MAE > 0 (positive error metrics)  
- train_test_gap in [0, 0.30] (reasonable overfitting range)
- shrinkage in [0, 1] (proportion of training performance lost)

*Data Quality:*
- All 3 models successfully cross-validated
- No NaN values in CV metrics
- Overfitting flags properly assigned (gap > 0.10)
- Consistent metrics across models

*Log Validation:*
- Required: "5-fold CV complete for all models", "Overfitting assessment complete"
- Required: "Model 1: test R² = X.XX ± X.XX", "Model 2: test R² = X.XX ± X.XX", "Model 3: test R² = X.XX ± X.XX"
- Forbidden: "ERROR", "CV failed", "fold failed"
- Acceptable warnings: "Model X shows overfitting (gap > 0.10)"

**Expected Behavior on Validation Failure:**
Log CV failures per model but continue, quit only if all 3 models fail CV

---

### Step 6: Effect Size and Power Analysis
**Dependencies:** Step 3 (model results)  
**Complexity:** Medium (~5 minutes)

**Purpose:** Compute effect sizes and conduct post-hoc power analysis for interpretation

**Input:**
- data/step03_model_results.csv (R², F-statistics, sample size)
- Model specifications for power calculations

**Processing:**
- Effect size computation for each model:
  - Cohen's f² = R² / (1 - R²)
  - Partial η² for each predictor = sr² (squared semi-partial correlation)  
  - Interpretation guidelines: f² small = 0.02, medium = 0.15, large = 0.35
- Post-hoc power analysis for each model:
  - Given: N=~95, 3 predictors per model
  - Alpha: 0.0056 (within-RQ Bonferroni corrected)
  - Use: statsmodels.stats.power.FTestAnovaPower()
  - Compute: Power achieved for observed f²
  - Sensitivity: Minimum detectable f² at 80% power
- Bootstrap 95% CIs for effect sizes:
  - Iterations: 1000
  - Random seed: 42
  - Method: Bootstrap resampling with model refitting
  - CI: Percentile method for f² and partial η²

**Output:**
- data/step06_effect_sizes.csv (f², partial η², power analysis per model)

**Validation Requirement:**
Validation tools MUST be used after effect size computation tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_effect_sizes.csv: 3 rows x 8 columns
- Columns: model, cohens_f2, f2_ci_lower, f2_ci_upper, power_observed, min_detectable_f2, power_80pct, effect_interpretation

*Value Ranges:*
- cohens_f2 in [0, 2] (reasonable range for behavioral data)
- Power in [0, 1], typically [0.05, 0.95] for this sample size
- min_detectable_f2 > 0 (positive minimum effect)
- CIs valid: ci_lower < cohens_f2 < ci_upper

*Data Quality:*
- All 3 models have effect sizes computed
- Power calculations successful for corrected alpha level
- Effect interpretation labels: small/medium/large based on Cohen (1988)
- Bootstrap CIs converged

*Log Validation:*
- Required: "Effect sizes computed for all models", "Power analysis complete"
- Required: "Model 1: f² = X.XX (EFFECT_SIZE), power = X.XX"
- Required: "Minimum detectable effect at 80% power: f² = X.XX"  
- Forbidden: "ERROR", "power calculation failed", "effect size failed"

**Expected Behavior on Validation Failure:**
Log specific calculation failures, proceed with available results, quit only if all effect sizes fail

---

### Step 7: Generate Analysis Summary
**Dependencies:** Steps 1-6 (all analysis results)
**Complexity:** Low (~5 minutes)

**Purpose:** Synthesize results and create interpretable summary of differential prediction findings

**Input:**
- data/step04_beta_comparisons.csv (key differential prediction results)
- data/step03_model_results.csv (individual model results)  
- data/step05_cross_validation.csv (generalizability assessment)
- data/step06_effect_sizes.csv (effect magnitude and power)

**Processing:**
- Synthesize primary hypothesis test:
  - Extract DASS_Anxiety differential prediction results
  - Compare beta coefficients: Confidence vs Accuracy, Calibration vs Accuracy
  - Summarize statistical significance with Bonferroni correction
  - Interpret effect sizes using Cohen guidelines
- Secondary hypothesis assessment:
  - DASS_Depression and DASS_Stress patterns
  - Overall DASS differential prediction strength
- Model quality summary:
  - R² and cross-validated R² for each model
  - Assumption violations and remedial actions taken
  - Power achieved and minimum detectable effects
- Clinical/theoretical interpretation:
  - Support for executive function theory predictions
  - Practical significance of differential effects
  - Limitations and boundary conditions

**Output:**
- data/step07_analysis_summary.csv (key findings in tabular format)
- results/differential_prediction_summary.txt (narrative interpretation)

**Validation Requirement:**
Validation tools MUST be used after summary generation tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_analysis_summary.csv: 5-10 rows x 6 columns
- Columns: finding, statistic, p_value, effect_size, interpretation, support_hypothesis
- results/differential_prediction_summary.txt: Text file 100-500 lines

*Value Ranges:*
- All p-values in [0, 1]
- Effect sizes correspond to Cohen guidelines
- Statistical values consistent with prior steps

*Data Quality:*
- Primary hypothesis clearly addressed
- All models summarized  
- Consistent statistical reporting across summary
- Clear support/non-support conclusions

*Log Validation:*
- Required: "Analysis summary complete", "Primary hypothesis: [SUPPORTED/NOT SUPPORTED]"
- Required: "Differential prediction test: [SIGNIFICANT/NON-SIGNIFICANT]"
- Forbidden: "ERROR", "summary failed", "inconsistent results"

**Expected Behavior on Validation Failure:**
Log summary generation issues, provide partial summary if possible, quit only if critical synthesis fails

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (prerequisite verification)
- data/step01_dass_scores.csv (extracted and standardized DASS predictors)
- data/step02_analysis_dataset.csv (merged data for all analyses)
- data/step03_model_results.csv (regression coefficients with dual p-values)
- data/step03_model_diagnostics.csv (assumption tests for all models)
- data/step04_beta_comparisons.csv (differential prediction statistical tests)
- data/step05_cross_validation.csv (generalizability assessment)
- data/step06_effect_sizes.csv (Cohen's f², power analysis)
- data/step07_analysis_summary.csv (key findings synthesis)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_dass.log
- logs/step02_merge_datasets.log  
- logs/step03_fit_models.log
- logs/step04_compare_betas.log
- logs/step05_cross_validation.log
- logs/step06_effect_sizes.log
- logs/step07_generate_summary.log

### Plots (EMPTY until rq_plots runs)
Plot source CSVs created in data/:
- data/step03_diagnostic_plots_data.csv (residual plots, Q-Q plots)
- data/step04_beta_comparison_plots_data.csv (coefficient comparison visuals)

### Results (EMPTY until rq_results runs)
- results/differential_prediction_summary.txt (created in Step 7)
- results/summary.md (created later by rq_results)

---

## Expected Data Formats

### Step-to-Step Transformations
1. **Step 1:** master.xlsx DASS columns → standardized z-scores
2. **Step 2:** Independent datasets → merged analysis dataset via UID
3. **Step 3:** Analysis dataset → 3 fitted regression models with diagnostics
4. **Step 4:** Model coefficients → statistical comparison of beta differences
5. **Step 5:** Models + data → cross-validation performance metrics
6. **Step 6:** Model statistics → effect sizes and power analysis
7. **Step 7:** All results → synthesized findings and interpretation

### Column Naming Conventions
- **Predictors:** z_Dep, z_Anx, z_Str (standardized DASS scores)
- **Outcomes:** theta_accuracy, confidence, calibration  
- **Coefficients:** beta, se, ci_lower, ci_upper, p_uncorrected, p_bonferroni, p_fdr
- **Models:** accuracy_model, confidence_model, calibration_model

### Data Type Constraints
- **UIDs:** Non-nullable strings, consistent across all files
- **DASS scores:** Float64, allow standardized negative values
- **Outcomes:** Float64, ranges depend on Ch5/Ch6 scaling
- **Statistics:** Float64, p-values in [0,1], effect sizes >= 0

---

## Cross-RQ Dependencies

**Required Dependencies:**
1. **Ch5 5.1.1:** Omnibus theta scores (overall memory accuracy measure)
   - Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
   - Alternative: results/ch5/5.1.1/data/*theta*.csv
   - Format: UID, theta_all (or similar omnibus accuracy score)

2. **Ch6 6.1.1:** Confidence scores (metacognitive confidence measure)  
   - Primary: results/ch6/6.1.1/data/confidence_scores.csv
   - Alternative: results/ch6/*/data/*confidence*.csv
   - Format: UID, mean_confidence (or participant-level confidence metric)

3. **Ch6 6.2.1:** Calibration scores (confidence-accuracy relationship)
   - Primary: results/ch6/6.2.1/data/calibration_scores.csv
   - Alternative: results/ch6/*/data/*calibration*.csv
   - Format: UID, calibration (correlation or calibration index)

4. **Master Data:** DASS-21 psychological measures
   - Required: data/cache/master.xlsx
   - Columns: UID, DASS_Dep, DASS_Anx, DASS_Str

**Dependency Validation Strategy:**
- Step 0 implements comprehensive file discovery with multiple fallback paths
- Flexible naming to accommodate Ch6 RQ variations
- Circuit breakers if critical data missing (N < 90 participants)

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
- **File existence:** All 4 data sources accessible
- **Data consistency:** Participant UIDs match across sources  
- **Completeness:** Sufficient data for N=90+ participants

#### Step 1: Extract DASS Scores
- **Data quality:** ~97 participants with complete DASS data
- **Range validation:** DASS scores in [0,42], z-scores properly standardized
- **Correlation check:** DASS subscales intercorrelated but VIF < 10

#### Step 2: Merge Datasets  
- **Merge success:** N=90+ complete cases after inner join
- **Outcome variance:** CV > 0.10 for all three outcome measures
- **Outlier detection:** Flag but retain extreme values (>3 SD)

#### Step 3: Fit Regression Models
- **Model convergence:** All 3 models fit successfully
- **Assumption checks:** Normality, homoscedasticity, independence, linearity, multicollinearity
- **Bootstrap success:** 1000 iterations complete for coefficient CIs
- **Dual p-values:** Both uncorrected and Bonferroni corrected (Decision D068)

#### Step 4: Compare Beta Coefficients
- **Statistical tests:** Bootstrap-based comparison of standardized betas
- **Multiple corrections:** Bonferroni and FDR for 9 comparisons  
- **Effect interpretation:** Cohen guidelines for coefficient differences

#### Step 5: Cross-Validation
- **CV completion:** 5-fold CV successful for all models
- **Overfitting detection:** Train-test gap < 0.10 preferred
- **Generalizability:** Test R² within reasonable range of training R²

#### Step 6: Effect Sizes
- **Power analysis:** Post-hoc power computed with corrected alpha
- **Effect interpretation:** Cohen's f² guidelines applied
- **Sensitivity:** Minimum detectable effects reported

#### Step 7: Analysis Summary
- **Hypothesis conclusion:** Clear support/non-support statement
- **Statistical consistency:** Results align across all prior steps
- **Interpretability:** Clinical and theoretical implications addressed

---

## Summary

**Total Steps:** 8 (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** ~45 minutes
**Cross-RQ Dependencies:** Ch5 5.1.1 (theta), Ch6 6.1.1 (confidence), Ch6 6.2.1 (calibration), master.xlsx (DASS)
**Primary Outputs:** Beta coefficient comparisons testing differential prediction hypothesis
**Validation Coverage:** 100% (all 8 steps have 4-layer validation requirements)

**Key Hypothesis:** DASS-Anxiety predicts metacognitive accuracy (confidence, calibration) more strongly than memory accuracy, supporting executive function theory predictions.

**Critical Methodological Notes:**
- Random seed=42 used throughout for reproducibility
- Bootstrap CIs (1000 iterations) for robust inference  
- Multiple comparison corrections at within-RQ level (9 tests) and within-model level (3 tests)
- Cross-validation (5-fold) to assess generalizability
- Comprehensive assumption testing with specified remedial actions
- Statistical comparison of beta coefficients using bootstrap approach
- Post-hoc power analysis with Bonferroni-corrected alpha levels
- Decision D068 compliance: dual p-value reporting throughout

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml  
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent (v5.1.0 specifications)
  - Enhanced statistical implementation details
  - Mandatory random seeds (42) and iteration counts
  - Comprehensive remedial actions for assumption violations  
  - Statistical comparison of beta coefficients with bootstrap tests
  - Multiple comparison corrections at appropriate levels
  - Cross-validation with overfitting assessment
  - Post-hoc power analysis with corrected alpha levels