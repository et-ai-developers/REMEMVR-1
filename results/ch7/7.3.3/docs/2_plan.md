# Analysis Plan: RQ 7.3.3 - Cognitive Predictors of High-Confidence Errors

**Research Question:** 7.3.3
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This analysis examines cognitive predictors of high-confidence error (HCE) rates using hierarchical multiple regression. The primary hypothesis tests whether fluid intelligence (RPM) negatively predicts HCE rates, while memory capacity tests (RAVLT, BVMT) show no significant prediction. HCE rates are derived from Ch6 6.6.x analyses and represent monitoring failures where confidence exceeds accuracy.

**Pipeline:** Hierarchical Multiple Regression with Cross-Validation
**Steps:** 9 total analysis steps (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** 35-45 minutes total

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni + FDR)
- Chapter 7 alpha correction: 0.05/28 = 0.00179 for family-wise control
- Within-RQ correction: 0.00179/4 = 0.000448 per cognitive predictor

**Statistical Specifications:**
- Random seed: 42 for all randomized procedures
- Bootstrap iterations: 1000 with percentile CIs
- Cross-validation: 5-fold with shuffle=True
- Power analysis: Post-hoc for observed effects
- Assumption remedial actions: Specified per violation type

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify Ch6 HCE rate outputs and master.xlsx accessibility before proceeding with analysis

**Input:**
- Primary: results/ch6/6.6.1/data/step03_hce_rates.csv
- Alternative: results/ch6/6.6.2/data/hce_rates_per_participant.csv
- Fallback: results/ch6/6.6.*/data/*hce*.csv
- Master data: data/cache/master.xlsx
- Expected: HCE rates (proportion) per participant, cognitive test scores

**Processing:**
- Check Ch6 6.6.x completion status in results/ch6/*/status.yaml
- Verify HCE rate file exists with expected format (UID, hce_rate columns)
- Verify master.xlsx contains cognitive tests (RAVLT_T, BVMT_T, RPM_T)
- Test file accessibility and basic data quality
- Log all validation checks with pass/fail status

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: Text file with validation results
- Contains: File paths checked, accessibility status, basic data dimensions

*Value Ranges:*
- File sizes > 0 bytes (files not empty)
- HCE rates in [0, 1] if data accessible
- Cognitive test scores reasonable range if data accessible

*Data Quality:*
- All required files identified (HCE rates + master.xlsx)
- No missing critical directories
- File format compatibility confirmed

*Log Validation:*
- Required patterns: "Ch6 HCE data: FOUND", "Master.xlsx: ACCESSIBLE"
- Forbidden patterns: "ERROR", "FILE NOT FOUND", "PERMISSION DENIED"
- Acceptable warnings: Path variation messages

**Expected Behavior on Validation Failure:**
If Ch6 HCE data not found, QUIT with specific missing file error. If master.xlsx not accessible, QUIT with data source error.

### Step 1: Extract and Prepare Cognitive Test Data
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (~5 minutes)

**Purpose:** Extract cognitive test scores from dfnonvr.csv and prepare for analysis

**Input:**
- data/cache/master.xlsx (cognitive test raw scores)
- Expected variables: RAVLT_total, BVMT_total, RPM_total, Age, Sex, Education

**Processing:**
- Load master.xlsx cognitive test sheet using pandas.read_excel
- Extract relevant variables: UID, RAVLT_total, BVMT_total, RPM_total, Age, Sex, Education
- Convert raw scores to T-scores using population norms:
  - RAVLT_T = 50 + 10 * (RAVLT_total - M_pop) / SD_pop
  - BVMT_T = 50 + 10 * (BVMT_total - M_pop) / SD_pop  
  - RPM_T = 50 + 10 * (RPM_total - M_pop) / SD_pop
- Handle missing data: listwise deletion for cognitive tests
- Create demographic dummy variables (Sex: 0=Male, 1=Female)
- Check data quality: ranges, outliers, distributions

**Output:**
- data/step01_cognitive_tests.csv (N=100 rows, 8 columns)

**Validation Requirement:**
Validation tools MUST be used after data extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_cognitive_tests.csv: 100 rows x 8 columns
- Columns: UID (object), RAVLT_T (float64), BVMT_T (float64), RPM_T (float64), Age (int64), Sex (int64), Education (int64)

*Value Ranges:*
- T-scores in [20, 80] (reasonable range for cognitive tests)
- Age in [18, 85] (adult participants)
- Sex in [0, 1] (binary encoding)
- Education in [8, 20] (years of education)

*Data Quality:*
- All 100 participants present (no missing UIDs)
- No NaN values in T-score columns after conversion
- Reasonable distributions (not all identical values)

*Log Validation:*
- Required patterns: "Cognitive tests extracted: N=100", "T-score conversion complete"
- Forbidden patterns: "ERROR", "NaN values detected", "conversion failed"
- Acceptable warnings: "outlier detected" (document but proceed)

**Expected Behavior on Validation Failure:**
If T-score conversion fails, log specific error and quit. If excessive missing data (>5%), document and proceed with available cases.

### Step 2: Extract HCE Rate Data
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (~5 minutes)

**Purpose:** Load HCE rates from Ch6 analyses and prepare participant-level data

**Input:**
- Primary: results/ch6/6.6.1/data/step03_hce_rates.csv
- Alternative paths from Step 0 validation
- Expected format: UID, hce_rate (proportion of errors that are high-confidence)

**Processing:**
- Load HCE rate file using pandas.read_csv
- Verify column names and data types (UID: object, hce_rate: float)
- Check HCE rate range: should be in [0, 1] as proportions
- Handle potential missing values (exclude participants if HCE rate missing)
- Compute descriptive statistics (mean, SD, min, max, distribution)
- Check for outliers using IQR method
- Verify N matches expected participant count

**Output:**
- data/step02_hce_rates.csv (N=100 rows, 2 columns)

**Validation Requirement:**
Validation tools MUST be used after HCE data extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_hce_rates.csv: 100 rows x 2 columns
- Columns: UID (object), hce_rate (float64)

*Value Ranges:*
- hce_rate in [0, 1] (valid proportions)
- Mean HCE rate approximately 0.15-0.20 (expected from Ch6 findings)
- No negative values or values > 1.0

*Data Quality:*
- All 100 participants present with valid HCE rates
- No NaN values in hce_rate column
- Distribution appears reasonable (not all identical)

*Log Validation:*
- Required patterns: "HCE rates loaded: N=100", "Mean HCE rate = X.XX"
- Forbidden patterns: "ERROR", "invalid proportion", "data corruption"
- Acceptable warnings: "outlier participant detected"

**Expected Behavior on Validation Failure:**
If HCE rates invalid or missing, QUIT with data quality error. If participant count mismatch, document and proceed with intersection.

### Step 3: Merge and Prepare Analysis Dataset
**Dependencies:** Steps 1-2 (cognitive tests + HCE rates)
**Complexity:** Low (~5 minutes)

**Purpose:** Combine cognitive tests and HCE rates into single analysis dataset

**Input:**
- data/step01_cognitive_tests.csv (T-scored predictors)
- data/step02_hce_rates.csv (HCE rate outcome)

**Processing:**
- Merge datasets on UID using pandas.merge (inner join)
- Verify merge successful: check for missing participants after merge
- Center continuous predictors for interpretation:
  - Age_c = Age - mean(Age)
  - RAVLT_T_c = RAVLT_T - 50 (T-score center)
  - BVMT_T_c = BVMT_T - 50
  - RPM_T_c = RPM_T - 50
- Standardize predictors for effect size interpretation
- Compute correlation matrix for multicollinearity screening
- Check final data quality: missing values, outliers, distributions

**Output:**
- data/step03_analysis_dataset.csv (N=100 rows, 12 columns)

**Validation Requirement:**
Validation tools MUST be used after dataset preparation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_analysis_dataset.csv: 100 rows x 12 columns
- Columns: UID, hce_rate (outcome), RAVLT_T, BVMT_T, RPM_T, Age, Sex, Education (raw), plus centered/standardized versions

*Value Ranges:*
- hce_rate in [0, 1] (outcome variable)
- Centered predictors centered around 0
- Standardized predictors approximately N(0,1)
- Correlations between predictors < 0.8 (multicollinearity screen)

*Data Quality:*
- N=100 participants (no loss during merge)
- No missing values in analysis variables
- Correlation matrix symmetric and valid

*Log Validation:*
- Required patterns: "Merge successful: N=100", "Data preparation complete"
- Forbidden patterns: "ERROR", "merge failed", "missing data detected"
- Acceptable warnings: "high correlation detected" (document but proceed)

**Expected Behavior on Validation Failure:**
If merge fails or substantial data loss, QUIT with merge error. If high multicollinearity detected (r > 0.8), document and flag for diagnostics.

### Step 4: Fit Hierarchical Regression Models
**Dependencies:** Step 3 (analysis dataset)
**Complexity:** Medium (~10 minutes including diagnostics)

**Purpose:** Fit hierarchical regression testing incremental validity of cognitive predictors

**Input:**
- data/step03_analysis_dataset.csv (prepared predictors and outcome)

**Processing:**
- Fit Model 1 (Demographics): hce_rate ~ Age_c + Sex + Education
- Fit Model 2 (+ Cognitive): hce_rate ~ Age_c + Sex + Education + RAVLT_T_c + BVMT_T_c + RPM_T_c
- Implementation: statsmodels.api.OLS with heteroscedasticity-robust standard errors (HC3)
- Extract model statistics:
  - R², Adjusted R², F-statistic, AIC for both models
  - ΔR² and F-change test for model improvement
  - Individual coefficients with 95% CIs
  - Semi-partial correlations (sr²) for each predictor
- Multiple comparison corrections:
  - Family: 4 cognitive predictors (3 tests + model improvement)
  - Bonferroni: alpha = 0.00179/4 = 0.000448 per test
  - FDR: Benjamini-Hochberg procedure
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Bootstrap confidence intervals:
  - Iterations: 1000
  - Seed: 42
  - Method: Participant-level resampling with replacement
  - CI: Percentile method (2.5th, 97.5th percentiles)

**Output:**
- data/step04_regression_results.csv (model comparison and coefficients)
- data/step04_bootstrap_cis.csv (bootstrap confidence intervals)

**Validation Requirement:**
Validation tools MUST be used after regression model execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_regression_results.csv: 8 rows x 10 columns (2 models + 6 predictors)
- Columns: model, predictor, beta, se, t_stat, p_uncorrected, p_bonferroni, p_fdr, ci_lower, ci_upper
- data/step04_bootstrap_cis.csv: 6 rows x 5 columns (bootstrap CIs for predictors)

*Value Ranges:*
- R² in [0, 1] for both models
- p-values in [0, 1]
- Beta coefficients reasonable range [-2, 2] for standardized predictors
- Bootstrap CIs: ci_lower < beta < ci_upper

*Data Quality:*
- All predictors present with valid coefficients
- No NaN values in regression results
- Bootstrap CIs computed successfully for all predictors
- Model 2 R² >= Model 1 R² (nesting requirement)

*Log Validation:*
- Required patterns: "Model 1 R² = X.XX", "Model 2 R² = X.XX", "Bootstrap complete: 1000 iterations"
- Forbidden patterns: "ERROR", "convergence failed", "singular matrix"
- Acceptable warnings: "multicollinearity detected" (document in diagnostics)

**Expected Behavior on Validation Failure:**
If model fitting fails, QUIT with convergence error. If bootstrap fails, proceed with regular CIs and document limitation.

### Step 5: Comprehensive Model Diagnostics
**Dependencies:** Step 4 (fitted models)
**Complexity:** Medium (~10 minutes)

**Purpose:** Check regression assumptions and identify potential violations

**Input:**
- data/step04_regression_results.csv (fitted models)
- data/step03_analysis_dataset.csv (for residual analysis)

**Processing:**
- Assumption checks for Model 2 (full model):
  - Multicollinearity: VIF for each predictor using statsmodels.stats.outliers_influence.variance_inflation_factor
  - Normality: Shapiro-Wilk test on residuals (scipy.stats.shapiro)
  - Homoscedasticity: Breusch-Pagan test (statsmodels.stats.diagnostic.het_breuschpagan)
  - Linearity: Partial residual plots (visual inspection + statistical tests)
  - Independence: Design-based assumption (cross-sectional data)
  - Outliers: Cook's distance (statsmodels.stats.outliers_influence.OLSInfluence)
- Remedial actions if assumptions violated:
  - Normality p < 0.05: Use bootstrap CIs as primary inference
  - Heteroscedasticity p < 0.05: Report HC3 robust standard errors
  - VIF > 5: Document multicollinearity, consider ridge if VIF > 10
  - Outliers (Cook's D > 4/n = 0.04): Report results with and without outliers
- Generate diagnostic plots data for visualization:
  - Residuals vs fitted values
  - Q-Q plot coordinates
  - Cook's distance per observation

**Output:**
- data/step05_model_diagnostics.csv (assumption test results)
- data/step05_diagnostic_plot_data.csv (plot coordinates for rq_plots)

**Validation Requirement:**
Validation tools MUST be used after diagnostic execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_model_diagnostics.csv: 6 rows x 4 columns (assumption tests)
- Columns: assumption, test_statistic, p_value, interpretation
- data/step05_diagnostic_plot_data.csv: varies by plot type

*Value Ranges:*
- VIF values > 1.0 (mathematical constraint)
- p-values in [0, 1] for statistical tests
- Cook's distance >= 0 (non-negative)
- Residuals approximately centered around 0

*Data Quality:*
- All 6 assumptions tested (multicollinearity, normality, homoscedasticity, linearity, independence, outliers)
- Clear pass/fail interpretation for each assumption
- Plot data complete for visualization

*Log Validation:*
- Required patterns: "Assumption checks complete", "VIF computed for N predictors"
- Forbidden patterns: "ERROR", "diagnostic failed", "invalid residuals"
- Acceptable warnings: "assumption violated" (document remedial action taken)

**Expected Behavior on Validation Failure:**
If diagnostic computation fails, document specific failure and proceed. If severe assumption violations detected, apply remedial actions and document.

### Step 6: Effect Size Computation and Interpretation
**Dependencies:** Step 4 (regression results)
**Complexity:** Medium (~8 minutes including bootstrap)

**Purpose:** Compute comprehensive effect sizes with confidence intervals

**Input:**
- data/step04_regression_results.csv (R², beta coefficients)

**Processing:**
- Effect size calculations:
  - Cohen's f² for models: f² = R²/(1-R²)
  - Individual predictor f²: f²_partial = sr²/(1-sr²)
  - Cohen's conventions: f² = 0.02 (small), 0.15 (medium), 0.35 (large)
  - Practical significance thresholds for HCE prediction context
- Bootstrap effect size confidence intervals:
  - Iterations: 1000
  - Seed: 42
  - Resample participants with replacement
  - Compute R², f², sr² for each bootstrap sample
  - CI: Percentile method (2.5th, 97.5th percentiles)
- Dominance analysis or relative importance:
  - Relative weights analysis for predictor importance ranking
  - Document which cognitive test contributes most to HCE prediction
- Context-specific interpretation:
  - Individual differences in metacognitive monitoring typically show smaller effects
  - Interpret f² ≥ 0.02 as meaningful for this research domain

**Output:**
- data/step06_effect_sizes.csv (f², relative weights, interpretations)
- data/step06_effect_size_cis.csv (bootstrap confidence intervals)

**Validation Requirement:**
Validation tools MUST be used after effect size computation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_effect_sizes.csv: varies by analysis (models + predictors)
- Columns: effect_type, value, interpretation, relative_importance
- data/step06_effect_size_cis.csv: bootstrap CIs for effect sizes

*Value Ranges:*
- Cohen's f² >= 0 (non-negative by definition)
- Relative weights sum to 1.0 (proportion constraint)
- R² in [0, 1] for bootstrap samples

*Data Quality:*
- Effect sizes computed for both models and individual predictors
- Bootstrap CIs valid (ci_lower <= value <= ci_upper)
- Relative importance rankings sum to 100%

*Log Validation:*
- Required patterns: "Effect sizes computed", "Bootstrap effect sizes: 1000 iterations"
- Forbidden patterns: "ERROR", "invalid effect size", "bootstrap failed"
- Acceptable warnings: "small effect detected" (interpretable in context)

**Expected Behavior on Validation Failure:**
If effect size computation fails, log error and proceed with available statistics. If bootstrap fails, use analytical methods for CIs.

### Step 7: Cross-Validation Analysis
**Dependencies:** Step 3 (analysis dataset)
**Complexity:** Medium (~10 minutes)

**Purpose:** Assess model generalizability and check for overfitting

**Input:**
- data/step03_analysis_dataset.csv (full analysis dataset)

**Processing:**
- Implement 5-fold cross-validation:
  - Method: sklearn.model_selection.KFold
  - Folds: 5 (balance bias-variance for N=100)
  - Random seed: 42 for reproducibility
  - Shuffle: True (randomize before splitting)
  - Stratification: None for regression (use quantile-based if HCE rate skewed)
- For each fold:
  - Fit Model 2 on training set (80% of data)
  - Evaluate on test set (20% of data)
  - Compute R², RMSE, MAE on test set
  - Extract predicted vs actual HCE rates
- Aggregate cross-validation metrics:
  - Mean and SD of R² across 5 folds
  - Mean and SD of RMSE across 5 folds
  - Generalization gap: training R² - test R²
  - Flag if gap > 0.10 (overfitting threshold)
- Model comparison across folds:
  - Consistency of predictor significance
  - Stability of effect size estimates

**Output:**
- data/step07_cross_validation.csv (CV metrics per fold)
- data/step07_cv_summary.csv (aggregated CV performance)

**Validation Requirement:**
Validation tools MUST be used after cross-validation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_cross_validation.csv: 5 rows x 6 columns (one per fold)
- Columns: fold, train_r2, test_r2, rmse, mae, generalization_gap
- data/step07_cv_summary.csv: 1 row x 8 columns (summary statistics)

*Value Ranges:*
- R² values in [0, 1] for all folds
- RMSE >= 0 (non-negative error measure)
- MAE >= 0 (non-negative error measure)
- Generalization gap should be < 0.10 (overfitting threshold)

*Data Quality:*
- All 5 folds completed successfully
- No NaN values in CV metrics
- Reasonable consistency across folds (SD not excessive)

*Log Validation:*
- Required patterns: "Cross-validation complete: 5 folds", "Mean CV R² = X.XX"
- Forbidden patterns: "ERROR", "fold failed", "convergence error"
- Acceptable warnings: "high generalization gap" (flag overfitting)

**Expected Behavior on Validation Failure:**
If CV computation fails, document fold-specific errors and proceed with available folds. If severe overfitting detected (gap > 0.20), recommend model simplification.

### Step 8: Power Analysis and Sensitivity
**Dependencies:** Steps 4, 6 (regression results and effect sizes)
**Complexity:** Low (~7 minutes)

**Purpose:** Conduct post-hoc power analysis and sensitivity testing

**Input:**
- data/step04_regression_results.csv (observed effect sizes)
- data/step06_effect_sizes.csv (Cohen's f² values)

**Processing:**
- Post-hoc power analysis for hierarchical regression:
  - Given: N=100, 6 predictors (Model 2), alpha=0.000448 (Bonferroni corrected)
  - Observed effect size: f² from Model 2
  - Use: statsmodels.stats.power.FTestAnovaPower() for F-change test
  - Calculate: achieved power for observed ΔR²
  - Individual predictors: power for each beta coefficient
- Sensitivity analysis - minimum detectable effects:
  - Calculate: smallest f² detectable with 80% power
  - Calculate: smallest beta detectable for RPM (primary hypothesis)
  - Compare to observed effects: adequate power assessment
- Power interpretation:
  - If power < 0.80: acknowledge limitation in interpretation
  - If power > 0.95: note high sensitivity to small effects
  - Document implications for null findings (especially RAVLT/BVMT)

**Output:**
- data/step08_power_analysis.csv (power calculations)
- data/step08_sensitivity.csv (minimum detectable effects)

**Validation Requirement:**
Validation tools MUST be used after power analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_power_analysis.csv: varies by test (model + predictors)
- Columns: test_type, effect_size, alpha, power, interpretation
- data/step08_sensitivity.csv: minimum detectable effect sizes

*Value Ranges:*
- Power in [0, 1] (probability range)
- Effect sizes >= 0 (Cohen's f² constraint)
- Alpha levels match specified corrections

*Data Quality:*
- Power computed for all relevant tests
- Sensitivity thresholds reasonable for sample size
- Clear interpretation of power adequacy

*Log Validation:*
- Required patterns: "Power analysis complete", "Achieved power for RPM = X.XX"
- Forbidden patterns: "ERROR", "power calculation failed"
- Acceptable warnings: "low power detected" (acknowledge limitation)

**Expected Behavior on Validation Failure:**
If power calculation fails, document specific computational issue. If power extremely low (<0.20), recommend interpretation caution.

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (prerequisite verification)
- data/step01_cognitive_tests.csv (T-scored predictors, N=100 x 8)
- data/step02_hce_rates.csv (outcome variable, N=100 x 2)
- data/step03_analysis_dataset.csv (merged analysis data, N=100 x 12)
- data/step04_regression_results.csv (hierarchical regression coefficients)
- data/step04_bootstrap_cis.csv (bootstrap confidence intervals)
- data/step05_model_diagnostics.csv (assumption test results)
- data/step05_diagnostic_plot_data.csv (plot coordinates for visualization)
- data/step06_effect_sizes.csv (Cohen's f², relative importance)
- data/step06_effect_size_cis.csv (bootstrap effect size CIs)
- data/step07_cross_validation.csv (CV performance per fold)
- data/step07_cv_summary.csv (aggregated CV metrics)
- data/step08_power_analysis.csv (post-hoc power calculations)
- data/step08_sensitivity.csv (minimum detectable effects)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_cognitive_tests.log
- logs/step02_extract_hce_rates.log
- logs/step03_merge_datasets.log
- logs/step04_hierarchical_regression.log
- logs/step05_model_diagnostics.log
- logs/step06_effect_sizes.log
- logs/step07_cross_validation.log
- logs/step08_power_analysis.log

### Plots (EMPTY until rq_plots runs)
Note: Plot source CSVs created in data/ folder:
- data/step05_diagnostic_plot_data.csv (residual plots, Q-Q plots)
- data/step06_effect_plot_data.csv (effect size visualization)
- data/step07_cv_plot_data.csv (cross-validation performance)

### Results (EMPTY until rq_results runs)
Note: summary.md will be created by rq_results agent

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 1 → Step 3:** Raw cognitive scores converted to T-scores (M=50, SD=10)
**Step 2 → Step 3:** HCE rates (proportions) merged with cognitive predictors
**Step 3 → Step 4:** Centered and standardized predictors for regression analysis
**Step 4 → Steps 5-8:** Model objects and residuals flow to diagnostics and validation

### Column Naming Conventions

**Standardized Variables:**
- UID: Participant identifier (object type)
- hce_rate: High-confidence error proportion (float, 0-1)
- RAVLT_T, BVMT_T, RPM_T: T-scored cognitive tests (float, ~20-80)
- Age_c: Age centered on sample mean (float)
- Sex: Binary (0=Male, 1=Female)

**Statistical Results:**
- beta: Standardized regression coefficients
- se: Standard errors
- p_uncorrected, p_bonferroni, p_fdr: Multiple p-value formats (Decision D068)
- ci_lower, ci_upper: 95% confidence interval bounds

### Data Type Constraints

**Nullable Constraints:**
- UID: Never null (primary key)
- hce_rate: Never null (outcome required)
- Cognitive tests: Null allowed pre-imputation, never null post-processing
- Bootstrap results: Never null (1000 iterations ensures stability)

**Range Constraints:**
- hce_rate: [0, 1] (proportion bounds)
- T-scores: [20, 80] (reasonable range for adult samples)
- p-values: [0, 1] (probability bounds)
- R²: [0, 1] (variance explained bounds)

---

## Cross-RQ Dependencies

**Ch6 HCE Rate Calculations (DERIVED DATA):**
- **Source RQ:** Ch6 6.6.1, 6.6.2, or equivalent HCE analysis
- **Required Files:** HCE rates per participant (proportion of errors that are high-confidence)
- **File Patterns:** results/ch6/6.6.*/data/*hce*.csv
- **Fallback Strategy:** Search multiple Ch6 6.6.x results for HCE output
- **Expected Format:** UID (object), hce_rate (float 0-1)
- **Critical Dependency:** Analysis cannot proceed without Ch6 HCE calculations

**Master Cognitive Test Data (RAW DATA):**
- **Source:** data/cache/master.xlsx
- **Required Variables:** RAVLT_total, BVMT_total, RPM_total, Age, Sex, Education
- **Processing:** Convert raw scores to T-scores using population norms
- **Quality Requirements:** Valid scores for ≥95 participants (allow 5% missing)

**Dependency Validation Strategy:**
1. Check Ch6 completion status in status.yaml files
2. Search for HCE rate files using multiple path patterns
3. Verify master.xlsx accessibility and required variables
4. Document all dependency checks in Step 0 validation
5. QUIT with specific error if critical dependencies missing

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
**Validation Type:** File existence and accessibility validation
**4-Layer Requirements:** File accessibility, basic data quality, log patterns, error handling
**Tools Required:** Basic file system validation tools

#### Step 1: Extract Cognitive Tests
**Validation Type:** Data extraction and T-score conversion validation  
**4-Layer Requirements:** Output dimensions, T-score ranges, data quality, extraction logs
**Tools Required:** Data validation tools for pandas operations

#### Step 2: Extract HCE Rates
**Validation Type:** HCE rate data quality validation
**4-Layer Requirements:** Proportion ranges, participant counts, distribution checks, loading logs
**Tools Required:** Data validation tools for CSV operations

#### Step 3: Merge Datasets  
**Validation Type:** Data merging and preparation validation
**4-Layer Requirements:** Merge success, variable types, correlation matrices, preparation logs
**Tools Required:** Data merging validation tools

#### Step 4: Hierarchical Regression
**Validation Type:** Statistical model fitting validation
**4-Layer Requirements:** Model convergence, coefficient ranges, bootstrap success, regression logs
**Tools Required:** Regression model validation tools

#### Step 5: Model Diagnostics
**Validation Type:** Assumption testing validation
**4-Layer Requirements:** Test completion, diagnostic values, remedial actions, diagnostic logs
**Tools Required:** Statistical diagnostic validation tools

#### Step 6: Effect Sizes
**Validation Type:** Effect size computation validation
**4-Layer Requirements:** Effect size ranges, bootstrap CIs, interpretation validity, computation logs
**Tools Required:** Effect size validation tools

#### Step 7: Cross-Validation
**Validation Type:** Model generalization validation
**4-Layer Requirements:** Fold completion, CV metrics, overfitting detection, CV logs
**Tools Required:** Cross-validation performance tools

#### Step 8: Power Analysis
**Validation Type:** Statistical power computation validation
**4-Layer Requirements:** Power calculation ranges, sensitivity analysis, interpretation accuracy, power logs
**Tools Required:** Power analysis validation tools

**Validation Coverage:** 100% (all 9 steps have comprehensive 4-layer validation requirements)

---

## Summary

**Total Steps:** 9 (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** 35-45 minutes
**Cross-RQ Dependencies:** Ch6 6.6.x HCE rates (DERIVED) + master.xlsx cognitive tests (RAW)
**Primary Outputs:** Hierarchical regression results with comprehensive diagnostics and validation
**Validation Coverage:** 100% (all steps have 4-layer validation requirements)

**Key Hypothesis:** RPM (fluid intelligence) negatively predicts HCE rates; RAVLT/BVMT show no significant prediction

**Critical Methodological Notes:**
- Multiple comparison correction: Bonferroni within-RQ (α = 0.000448 per test)
- Bootstrap confidence intervals: 1000 iterations, seed=42, percentile method
- Cross-validation: 5-fold with shuffle, generalization gap threshold <0.10
- Assumption remedial actions: HC3 robust SEs, bootstrap CIs for violations
- Power analysis: Post-hoc for observed effects with sensitivity analysis

**Statistical Implementation Standards (v5.1):**
- All randomized procedures use seed=42 for reproducibility
- Bootstrap procedures: participant-level resampling, 1000 iterations
- Cross-validation: 5-fold stratified, train-test gap monitoring
- Power analysis: post-hoc with minimum detectable effect calculation
- Multiple comparisons: family-wise control with dual reporting (Decision D068)
- Assumption violations: specific remedial actions for each violation type

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml  
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent with enhanced v5.1 specifications