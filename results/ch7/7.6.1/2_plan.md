# Analysis Plan: RQ 7.6.1 - Cognitive Tests Predicting Individual Differences in Forgetting Rate

**Research Question:** 7.6.1
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This analysis examines whether traditional cognitive assessments (RAVLT, BVMT, RPM) predict individual differences in REMEMVR forgetting slopes estimated from Ch5 5.1.4 model-averaged results. The central hypothesis predicts that cognitive tests should NOT significantly predict forgetting slopes, as consolidation processes differ from encoding abilities measured by traditional tests.

**Pipeline:** Multiple Linear Regression with Hierarchical Entry
**Steps:** 8 total analysis steps (Step 0: validation + Steps 1-7: analysis)  
**Estimated Runtime:** ~45 minutes

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Enhanced v5.1: Complete statistical specifications (CV, bootstrap, power, corrections)
- Random seed=42 for all randomized procedures

**Critical Dependencies:**
- Ch5 5.1.4 model-averaged slope estimates must be available
- master.xlsx cognitive test scores must be accessible

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 5.1.4 outputs exist and cognitive test data is accessible before proceeding

**Input:**
- Primary: results/ch5/5.1.4/status.yaml (verify rq_results: success)
- Alternative: results/ch5/5.1.4/data/step03_model_averaged_slopes.csv
- Fallback: results/ch5/5.1.4/data/*slope*.{csv,txt,rds}
- Expected: Per-participant slope estimates from model-averaged LMM
- Cognitive: data/cache/master.xlsx (RAVLT_T, BVMT_T, RPM_T scores)
- If missing: QUIT with "Ch5 5.1.4 slope outputs not found"

**Processing:**
- Check Ch5 5.1.4 completion status in status.yaml
- Search for slope estimate files using multiple patterns
- Verify master.xlsx contains required cognitive test columns
- Test file readability and expected data structure
- Log all validation checks with specific success/failure messages

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Content structure: "Ch5 5.1.4 status: [success/failed]", "Slope file found: [path]", "Cognitive tests available: [Y/N]"

*Value Ranges:*
- Status checks: binary success/failure indicators
- File existence: boolean true/false values
- Path validity: accessible file system paths

*Data Quality:*
- All required dependencies identified (Ch5 slopes + cognitive tests)
- No broken file paths or permission issues
- Expected file formats confirmed (CSV for slopes, XLSX for cognitive)

*Log Validation:*
- Required patterns: "VALIDATION COMPLETE", "All dependencies available"
- Required patterns: "Ch5 5.1.4: SUCCESS", "master.xlsx: ACCESSIBLE"
- Forbidden patterns: "ERROR", "MISSING", "FAILED", "INACCESSIBLE"

**Expected Behavior on Validation Failure:**
Raise error with specific missing dependency, log to logs/step00_validate_dependencies.log, quit immediately with clear error message for user action.

### Step 1: Extract and Prepare Cognitive Test Data
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (~5 minutes)

**Purpose:** Extract cognitive test scores from master.xlsx and prepare for analysis

**Input:**
- data/cache/master.xlsx (cognitive test raw scores)
- Expected columns: UID, RAVLT_raw, BVMT_raw, RPM_raw, age, sex, education

**Processing:**
- Load master.xlsx using pandas.read_excel() 
- Extract cognitive test columns: RAVLT_raw, BVMT_raw, RPM_raw
- Convert raw scores to T-scores for interpretability:
  - T-score = 50 + 10 * (raw - mean) / std
  - Apply per-test transformation to create RAVLT_T, BVMT_T, RPM_T
- Extract demographic controls: age, sex, education
- Check for missing data patterns and document
- Standardize sex coding (M=0, F=1) and education (years numeric)
- Create analysis-ready dataset with UID as key

**Output:**
- data/step01_cognitive_tests.csv

**Validation Requirement:**
Validation tools MUST be used after cognitive test extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_cognitive_tests.csv: 100 rows x 8 columns
- Columns: UID (object), RAVLT_T (float64), BVMT_T (float64), RPM_T (float64), age (float64), sex (int64), education (float64), missing_data_count (int64)

*Value Ranges:*
- T-scores range: [20, 80] (2-3 SD from population mean of 50)
- Age range: [18, 85] years (adult participants)
- Sex coding: [0, 1] (M=0, F=1)
- Education range: [8, 20] years (elementary through graduate school)
- Missing data per participant: [0, 3] (maximum across 3 cognitive tests)

*Data Quality:*
- All 100 participants present (no missing UIDs)
- No duplicate UIDs
- T-scores normally distributed (mean ~50, SD ~10)
- Missing data <10% per cognitive test
- All demographic variables within expected ranges

*Log Validation:*
- Required patterns: "T-score conversion complete", "100 participants processed"
- Required patterns: "Missing data check: [N]% missing per test"
- Forbidden patterns: "ERROR", "conversion failed", "invalid scores"

**Expected Behavior on Validation Failure:**
Raise error with specific data quality issue, log to logs/step01_extract_cognitive_tests.log, investigate master.xlsx data integrity.

### Step 2: Extract Individual Slope Estimates
**Dependencies:** Steps 0-1 (validation + cognitive tests)
**Complexity:** Medium (~7 minutes)

**Purpose:** Extract per-participant slope estimates from Ch5 5.1.4 model-averaged results

**Input:**
- Primary: results/ch5/5.1.4/data/step03_model_averaged_slopes.csv
- Alternative: results/ch5/5.1.4/data/participant_slopes.csv
- Fallback: results/ch5/5.1.4/data/*slope*.csv
- Expected: UID + slope estimate + slope SE for each participant

**Processing:**
- Load slope estimates using pandas.read_csv()
- Verify file contains required columns: UID, slope, slope_SE (or similar)
- Check data quality: 100 participants, no missing UIDs
- Validate slope ranges: [-0.5, 0.1] per day (forgetting = negative slopes)
- Validate slope SEs: [0.001, 0.1] (positive, bounded standard errors)
- Remove any duplicates or invalid entries
- Log summary statistics: mean slope, SD, range
- Create clean dataset ready for regression analysis

**Output:**
- data/step02_slopes_extracted.csv

**Validation Requirement:**
Validation tools MUST be used after slope extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_slopes_extracted.csv: 100 rows x 3 columns
- Columns: UID (object), slope (float64), slope_SE (float64)

*Value Ranges:*
- Slopes in [-0.5, 0.1] per day (forgetting rates, negative values expected)
- Slope SEs in [0.001, 0.1] (positive standard errors, bounded)
- Mean slope approximately -0.1 to -0.2 per day (typical forgetting)

*Data Quality:*
- All 100 participants present (no missing UIDs)
- No duplicate UIDs
- No NaN values in slope estimates
- Slope SE > 0 for all participants (valid uncertainty estimates)
- Distribution roughly normal for slope estimates

*Log Validation:*
- Required patterns: "Slope extraction complete: 100 participants"
- Required patterns: "Mean slope = [value], SD = [value]"
- Required patterns: "Slope range: [min] to [max]"
- Forbidden patterns: "ERROR", "missing slopes", "invalid estimates"

**Expected Behavior on Validation Failure:**
Raise error with specific slope data issue, log to logs/step02_extract_slopes.log, check Ch5 5.1.4 completion status.

### Step 3: Merge Datasets and Create Analysis Input
**Dependencies:** Steps 1-2 (cognitive tests + slopes)
**Complexity:** Low (~3 minutes)

**Purpose:** Merge cognitive test scores with slope estimates to create complete analysis dataset

**Input:**
- data/step01_cognitive_tests.csv
- data/step02_slopes_extracted.csv

**Processing:**
- Merge datasets on UID using pandas.merge(on="UID", how="inner")
- Verify merge completeness: expect 100 participants in final dataset
- Check for any participants missing from either dataset
- Standardize all predictors to mean=0, SD=1 for regression interpretation
- Create hierarchical predictor sets:
  - Demographics: age_std, sex, education_std
  - Cognitive: RAVLT_T_std, BVMT_T_std, RPM_T_std
- Final columns: UID, slope, slope_SE, age_std, sex, education_std, RAVLT_T_std, BVMT_T_std, RPM_T_std
- Document final sample characteristics and missing data summary

**Output:**
- data/step03_analysis_input.csv

**Validation Requirement:**
Validation tools MUST be used after dataset merging.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_analysis_input.csv: 100 rows x 9 columns
- Columns: UID, slope, slope_SE, age_std, sex, education_std, RAVLT_T_std, BVMT_T_std, RPM_T_std
- Data types: UID (object), slope (float64), all others (float64 or int64)

*Value Ranges:*
- Standardized predictors: approximately [-3, 3] (z-scores)
- Mean of standardized variables: approximately 0.0
- SD of standardized variables: approximately 1.0
- Sex coding: [0, 1] unchanged from Step 1
- Slopes: unchanged from Step 2 validation

*Data Quality:*
- Complete merge: 100 participants retained
- No missing values in standardized predictors
- All UIDs unique and present in both source datasets
- Standardization successful (means ~0, SDs ~1)

*Log Validation:*
- Required patterns: "Merge complete: 100 participants retained"
- Required patterns: "Standardization complete: means ~0, SDs ~1"
- Required patterns: "No missing values in final dataset"
- Forbidden patterns: "ERROR", "merge failed", "missing participants"

**Expected Behavior on Validation Failure:**
Raise error with merge issue details, log to logs/step03_merge_datasets.log, check UID consistency between datasets.

### Step 4: Hierarchical Multiple Regression Analysis
**Dependencies:** Step 3 (analysis input dataset)
**Complexity:** High (~15 minutes including bootstrap)

**Purpose:** Fit hierarchical regression models to test cognitive prediction of slope with comprehensive statistical specifications

**Input:**
- data/step03_analysis_input.csv

**Processing:**
- Hierarchical regression with statsmodels.api.OLS:
  - Model 1 (Demographics): slope ~ age_std + sex + education_std
  - Model 2 (Full): slope ~ age_std + sex + education_std + RAVLT_T_std + BVMT_T_std + RPM_T_std
- Extract model comparison statistics:
  - Delta R² = R²_model2 - R²_model1
  - F-test for model improvement: F(3, 93) for adding 3 cognitive predictors
  - Report hierarchical F-test p-value
- Extract individual predictor results:
  - Standardized betas with 95% CIs
  - Semi-partial correlations (sr²) for unique variance
  - t-statistics and uncorrected p-values
- Bootstrap confidence intervals for all coefficients:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling WITH replacement
  - CI computation: percentile method (2.5th, 97.5th percentiles)
- Multiple comparison corrections:
  - Family: Within-step (3 cognitive predictors)
  - Bonferroni: alpha = 0.05/3 = 0.0167 per cognitive test
  - Chapter correction: alpha = 0.00179 (Ch7 global correction)
  - FDR: Benjamini-Hochberg correction for comparison
  - Report BOTH uncorrected AND corrected p-values (Decision D068)

**Output:**
- data/step04_regression_results.csv

**Validation Requirement:**
Validation tools MUST be used after regression analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_regression_results.csv: 8 rows x 12 columns (6 predictors + 2 model summary rows)
- Columns: predictor, beta, se, ci_lower, ci_upper, t_stat, p_uncorrected, p_bonferroni, p_chapter, p_fdr, sr_squared, model
- Model summary rows: R²_demographics, R²_full with delta_R², F_test_p

*Value Ranges:*
- Standardized betas: [-1.0, 1.0] (standardized predictors and outcome)
- Standard errors: [0.01, 0.5] (positive, reasonable for N=100)
- p-values: [0, 1] (valid probability range)
- R² values: [0, 1] (proportion variance explained)
- F-statistics: [0, 50] (reasonable for regression context)

*Data Quality:*
- All 6 predictors present with complete results
- Bootstrap CIs valid: ci_lower < beta < ci_upper for all predictors
- Hierarchical model comparison included
- Dual p-values present for all tests (Decision D068)
- Model fit statistics reasonable (no perfect multicollinearity)

*Log Validation:*
- Required patterns: "Hierarchical regression complete"
- Required patterns: "Bootstrap complete: 1000 iterations, seed=42"
- Required patterns: "Model 1 R² = [value], Model 2 R² = [value], Delta R² = [value]"
- Required patterns: "Multiple corrections applied: Bonferroni, Chapter, FDR"
- Forbidden patterns: "ERROR", "convergence failed", "singular matrix"

**Expected Behavior on Validation Failure:**
Raise error with specific regression issue, log to logs/step04_hierarchical_regression.log, check for multicollinearity or data quality problems.

### Step 5: Model Diagnostics and Assumption Validation
**Dependencies:** Step 4 (regression results)
**Complexity:** Medium (~8 minutes)

**Purpose:** Comprehensive validation of regression assumptions with remedial action specifications

**Input:**
- data/step03_analysis_input.csv (original data)
- data/step04_regression_results.csv (fitted model results)

**Processing:**
- Assumption checks with specific tests and remedial actions:
- Multicollinearity assessment:
  - Compute Variance Inflation Factors (VIF) for all predictors
  - Threshold: VIF < 5.0 (moderate), VIF < 10.0 (severe)
  - Remedial action if VIF > 10: Document, consider ridge regression
- Normality of residuals:
  - Shapiro-Wilk test on residuals (H0: normal distribution)
  - Q-Q plot visual inspection
  - Remedial action if p < 0.05: Use bootstrap CIs as primary inference
- Homoscedasticity:
  - Breusch-Pagan test for heteroscedasticity
  - Residual vs fitted values plot
  - Remedial action if p < 0.05: Report HC3 robust standard errors
- Linearity assessment:
  - Partial residual plots for each continuous predictor
  - Visual inspection for systematic deviations from linearity
  - Remedial action: Document non-linear patterns, consider transformations
- Outlier detection:
  - Cook's Distance with threshold D > 4/n = 4/100 = 0.04
  - Leverage values > 2p/n = 12/100 = 0.12 (hat values)
  - Remedial action: Report results with and without influential points
- Generate diagnostic plots for visual assessment

**Output:**
- data/step05_model_diagnostics.csv
- data/step05_diagnostic_plots_data.csv (source data for plots)

**Validation Requirement:**
Validation tools MUST be used after diagnostic analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_model_diagnostics.csv: 6 rows x 6 columns (one per predictor)
- Columns: predictor, vif, normality_p, bp_test_p, cooks_d_max, leverage_max
- data/step05_diagnostic_plots_data.csv: 100 rows x 8 columns (residual analysis data)

*Value Ranges:*
- VIF values: [1.0, 10.0] (lower better, >10 indicates severe multicollinearity)
- p-values: [0, 1] for normality and BP tests
- Cook's D: [0, 0.2] (influential if >0.04 for this sample)
- Leverage: [0, 0.3] (high if >0.12 for this model)
- Residuals: approximately normal distribution around 0

*Data Quality:*
- All 6 predictors have diagnostic results
- No missing diagnostic statistics
- Cook's D and leverage computed for all 100 observations
- Residual statistics within reasonable bounds

*Log Validation:*
- Required patterns: "Assumption checks complete: normality, homoscedasticity, multicollinearity"
- Required patterns: "VIF assessment: max VIF = [value]"
- Required patterns: "Outlier analysis: [N] participants exceed Cook's D threshold"
- Required patterns: "Remedial actions: [list of applied corrections]"
- Forbidden patterns: "ERROR", "diagnostic failed", "invalid residuals"

**Expected Behavior on Validation Failure:**
Raise error with specific diagnostic issue, log to logs/step05_model_diagnostics.log, examine residual patterns for systematic issues.

### Step 6: Cross-Validation Analysis
**Dependencies:** Steps 4-5 (regression + diagnostics)
**Complexity:** Medium (~8 minutes)

**Purpose:** Assess model generalizability through cross-validation with comprehensive specifications

**Input:**
- data/step03_analysis_input.csv

**Processing:**
- Implement 5-fold cross-validation with specifications:
  - Method: sklearn.model_selection.KFold
  - Number of folds: 5 (20% test, 80% train per fold)
  - Random seed: 42 for reproducibility
  - Shuffle: True (randomize before splitting)
  - Stratification: None (regression outcome, not classification)
- For each fold:
  - Fit Model 2 (full model) on training set (80% of data)
  - Predict on test set (20% of data)
  - Compute metrics: R², RMSE, MAE
  - Track individual fold performance
- Cross-validation metrics:
  - Mean CV R² ± standard deviation across 5 folds
  - Mean CV RMSE ± standard deviation
  - Mean CV MAE ± standard deviation
- Overfitting assessment:
  - Training R² vs test R² comparison
  - Flag if train-test R² gap > 0.10 (overfitting threshold)
  - Compute generalization gap: mean(train R²) - mean(test R²)
- Model stability:
  - Coefficient stability across folds
  - SD of beta coefficients across CV folds

**Output:**
- data/step06_cross_validation.csv

**Validation Requirement:**
Validation tools MUST be used after cross-validation analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_cross_validation.csv: 5 rows x 8 columns (one per fold)
- Columns: fold, train_r2, test_r2, rmse, mae, n_train, n_test, overfitting_flag
- Summary statistics: mean_cv_r2, sd_cv_r2, generalization_gap, stability_index

*Value Ranges:*
- R² values: [0, 1] for both training and test sets
- RMSE: [0, 0.5] (reasonable for slope outcome scale)
- MAE: [0, 0.3] (mean absolute error for slopes)
- Generalization gap: [-0.2, 0.3] (test R² can exceed train R² by chance)
- Sample sizes: n_train ~80, n_test ~20 per fold

*Data Quality:*
- All 5 folds completed successfully
- No extreme outliers in CV metrics (>3 SD from mean)
- Reasonable stability across folds (CV SD < 0.10)
- Overfitting assessment completed for all folds

*Log Validation:*
- Required patterns: "5-fold cross-validation complete, seed=42"
- Required patterns: "Mean CV R² = [value] ± [SD]"
- Required patterns: "Generalization gap = [value] (threshold = 0.10)"
- Required patterns: "Overfitting detected: [Y/N]"
- Forbidden patterns: "ERROR", "fold failed", "convergence issues"

**Expected Behavior on Validation Failure:**
Raise error with CV issue details, log to logs/step06_cross_validation.log, check for data splitting or convergence problems.

### Step 7: Power Analysis and Effect Size Assessment
**Dependencies:** Steps 4-6 (regression + validation)
**Complexity:** Medium (~7 minutes)

**Purpose:** Comprehensive power analysis with sensitivity assessment for effect size interpretation

**Input:**
- data/step04_regression_results.csv (observed effect sizes)
- Analysis parameters: N=100, p=6 predictors, alpha levels

**Processing:**
- Post-hoc power analysis for hierarchical regression:
  - Given: N=100, 6 predictors total, 3 cognitive predictors of interest
  - Observed effect size: Cohen's f² = R²_full/(1-R²_full)
  - Alpha levels: 0.05 (standard), 0.00179 (Ch7 chapter correction)
  - Power calculation: statsmodels.stats.power.FTestAnovaPower()
  - Compute power for: (1) overall model, (2) incremental cognitive prediction
- A priori power analysis:
  - Target power: 0.80 (standard threshold)
  - Calculate minimum detectable effect sizes:
    - f² for overall model at 80% power
    - f² for incremental R² (cognitive tests) at 80% power
  - Sample size adequacy assessment
- Effect size interpretation:
  - Cohen's f² benchmarks: 0.02 (small), 0.15 (medium), 0.35 (large)
  - Practical significance thresholds for slope prediction
  - Compare observed effects to interpretation benchmarks
- Sensitivity analysis:
  - Power curves: effect size by power relationship
  - Sample size requirements for detecting small effects (f² = 0.02)
  - Impact of multiple comparison corrections on power

**Output:**
- data/step07_power_analysis.csv

**Validation Requirement:**
Validation tools MUST be used after power analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_power_analysis.csv: 4 rows x 8 columns (overall, incremental, sensitivity analyses)
- Columns: analysis_type, effect_size_f2, power_standard, power_corrected, min_detectable_f2, interpretation, adequate_power, sample_size_needed

*Value Ranges:*
- Cohen's f²: [0, 1] (practical upper bound ~0.5 for regression)
- Power values: [0, 1] (probability scale)
- Sample size estimates: [50, 500] (reasonable range for this design)
- Effect size interpretations: categorical (small/medium/large)

*Data Quality:*
- All power calculations completed successfully
- Effect size interpretations assigned appropriately
- Sensitivity analyses cover relevant parameter ranges
- Sample size recommendations practical and justified

*Log Validation:*
- Required patterns: "Power analysis complete: post-hoc and sensitivity"
- Required patterns: "Observed f² = [value], Power = [value] at alpha = 0.00179"
- Required patterns: "Minimum detectable f² = [value] for 80% power"
- Required patterns: "Sample adequacy: [adequate/inadequate] for small effects"
- Forbidden patterns: "ERROR", "power calculation failed", "invalid parameters"

**Expected Behavior on Validation Failure:**
Raise error with power analysis issue, log to logs/step07_power_analysis.log, check effect size calculations and parameter validity.

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (prerequisite check results)
- data/step01_cognitive_tests.csv (T-scored cognitive test data)
- data/step02_slopes_extracted.csv (individual slope estimates from Ch5)
- data/step03_analysis_input.csv (merged dataset for regression)
- data/step04_regression_results.csv (hierarchical regression coefficients + dual p-values)
- data/step05_model_diagnostics.csv (assumption validation results)
- data/step05_diagnostic_plots_data.csv (source data for diagnostic plots)
- data/step06_cross_validation.csv (5-fold CV performance metrics)
- data/step07_power_analysis.csv (post-hoc and sensitivity power analyses)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log (dependency checking)
- logs/step01_extract_cognitive_tests.log (cognitive test processing)
- logs/step02_extract_slopes.log (slope data extraction)
- logs/step03_merge_datasets.log (dataset merging)
- logs/step04_hierarchical_regression.log (regression analysis)
- logs/step05_model_diagnostics.log (assumption validation)
- logs/step06_cross_validation.log (CV analysis)
- logs/step07_power_analysis.log (power calculations)

### Plots (EMPTY until rq_plots runs)
- Plot source CSVs created in data/ folder:
  - data/step05_diagnostic_plots_data.csv (residual analysis plots)

### Results (EMPTY until rq_results runs)
- summary.md will be created by rq_results agent

---

## Expected Data Formats

### Step-to-Step Transformations
1. **Step 0→1**: Dependency validation → Raw cognitive test extraction
2. **Step 1→2**: Cognitive tests → Ch5 slope estimates → Combined for merging
3. **Step 2→3**: Separate datasets → Merged analysis input with standardized predictors
4. **Step 3→4**: Analysis input → Hierarchical regression results with dual p-values
5. **Step 4→5**: Regression model → Diagnostic validation results
6. **Step 5→6**: Validated model → Cross-validation performance assessment
7. **Step 6→7**: CV results → Power analysis and effect size interpretation

### Column Naming Conventions
- **UIDs**: Always "UID" (string/object type)
- **Slopes**: "slope" (per-day forgetting rate, negative values)
- **Cognitive T-scores**: "RAVLT_T", "BVMT_T", "RPM_T" (T-score scale, mean=50, SD=10)
- **Standardized predictors**: "_std" suffix (z-scores, mean=0, SD=1)
- **Statistical results**: "beta", "se", "ci_lower", "ci_upper", "p_uncorrected", "p_bonferroni", "p_chapter", "p_fdr"

### Data Type Constraints
- **UIDs**: Non-nullable object type, unique values required
- **Slopes**: Float64, range [-0.5, 0.1], no missing values allowed
- **Test scores**: Float64, T-scores in range [20, 80], standardized versions [-3, 3]
- **Statistical results**: Float64, p-values in [0, 1], CIs well-ordered (lower < upper)

---

## Cross-RQ Dependencies

### Ch5 5.1.4: Model-Averaged Slope Estimates
- **Required Status**: Ch5 5.1.4 rq_results: success
- **Primary Files**: 
  - results/ch5/5.1.4/data/step03_model_averaged_slopes.csv
  - Alternative patterns: results/ch5/5.1.4/data/*slope*.csv
- **Expected Content**: Per-participant slope estimates with standard errors
- **Failure Action**: QUIT with "Ch5 5.1.4 model-averaged slopes not available"

### Master Data: Cognitive Test Scores  
- **Required File**: data/cache/master.xlsx
- **Expected Columns**: UID, RAVLT_raw, BVMT_raw, RPM_raw, age, sex, education
- **Content Validation**: 100 participants with valid cognitive test scores
- **Failure Action**: QUIT with "master.xlsx cognitive test data inaccessible"

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
**Validation Type**: File existence and accessibility validation
**Tools**: File system validation, status.yaml parsing
**Criteria**: 4-layer validation as specified in step details above

#### Step 1: Extract Cognitive Tests
**Validation Type**: Data extraction and transformation validation
**Tools**: Data range validation, missing data assessment
**Criteria**: T-score conversion accuracy, participant completeness

#### Step 2: Extract Slopes
**Validation Type**: Cross-RQ data extraction validation  
**Tools**: Data range validation, Ch5 output verification
**Criteria**: Slope estimate ranges, participant matching

#### Step 3: Merge Datasets
**Validation Type**: Data integration validation
**Tools**: Merge completeness, standardization verification
**Criteria**: Complete participant retention, standardization accuracy

#### Step 4: Hierarchical Regression
**Validation Type**: Statistical analysis validation
**Tools**: Regression output validation, bootstrap verification
**Criteria**: Model convergence, coefficient reasonableness, dual p-value presence

#### Step 5: Model Diagnostics
**Validation Type**: Assumption validation assessment
**Tools**: Diagnostic statistic validation, threshold checking
**Criteria**: Complete diagnostic coverage, remedial action documentation

#### Step 6: Cross-Validation
**Validation Type**: Model generalization validation
**Tools**: CV metric validation, overfitting assessment
**Criteria**: Fold completeness, metric reasonableness, overfitting detection

#### Step 7: Power Analysis
**Validation Type**: Statistical power validation
**Tools**: Power calculation verification, effect size validation
**Criteria**: Power estimate accuracy, effect size interpretation appropriateness

---

## Summary

**Total Steps:** 8 (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** ~45 minutes
**Cross-RQ Dependencies:** Ch5 5.1.4 (slope estimates), master.xlsx (cognitive tests)
**Primary Outputs:** Hierarchical regression results with dual p-value reporting
**Validation Coverage:** 100% (all 8 steps have 4-layer validation requirements)

**Key Hypothesis:** Cognitive tests (RAVLT_T, BVMT_T, RPM_T) should NOT significantly predict REMEMVR forgetting slopes. Expected results: Model R² < 0.10, p > 0.00179 (Ch7 corrected), individual predictors non-significant after Bonferroni correction.

**Critical Methodological Notes:**
- Enhanced v5.1 specifications ensure complete statistical implementation details
- Random seed=42 specified for all randomized procedures (bootstrap, CV)
- Comprehensive remedial actions specified for assumption violations
- Dual p-value reporting per Decision D068 (uncorrected + corrected)
- Bootstrap confidence intervals provide robust inference beyond normality assumptions
- Cross-validation assesses generalizability and overfitting
- Power analysis addresses sample size adequacy for detecting meaningful effects

**Expected Theoretical Contribution:**
Null prediction results would support encoding-consolidation dissociation theory, demonstrating that traditional cognitive assessments capture encoding abilities but not consolidation processes that govern forgetting over extended retention intervals.

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml  
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent v5.1
- Enhanced v5.1 specifications: Complete statistical implementation details, random seeds, remedial actions, 4-layer validation requirements