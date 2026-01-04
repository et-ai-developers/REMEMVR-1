# Analysis Plan: RQ 7.3.2 - Cognitive Predictors of Calibration Quality

**Research Question:** 7.3.2
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This analysis examines individual differences in calibration quality using cognitive test scores as predictors. Multiple regression with hierarchical entry will test whether fluid intelligence (RPM) predicts calibration quality better than memory tests (RAVLT, BVMT), reflecting the theoretical distinction between memory capacity and metacognitive monitoring processes.

**Pipeline:** Multiple Linear Regression with Cross-Validation and Comprehensive Diagnostics
**Steps:** 8 total analysis steps (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** 45-60 minutes total

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Chapter-level Bonferroni correction: alpha = 0.05/28 = 0.00179 per RQ
- Within-RQ Bonferroni for 3 cognitive tests: alpha = 0.00179/3 = 0.000597 per test

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies

**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch6 calibration outputs exist before proceeding with analysis

**Input:**
- Primary: results/ch6/6.2.*/status.yaml (check for rq_results: success)
- Alternative: results/ch6/*/data/*calibration*.csv (find calibration files)
- Fallback: results/ch6/*/data/*.csv (search all Ch6 data outputs)
- Expected content: Per-participant calibration quality metrics
- If not found: QUIT with "Ch6 calibration metrics not available"
- Also check: data/cache/master.xlsx (cognitive test scores)

**Processing:**
- Scan results/ch6/ for completed calibration analyses
- Verify calibration output files contain per-participant metrics
- Check master.xlsx accessibility for cognitive test extraction
- Log all dependency validation results
- Document which Ch6 RQ provides calibration data

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Expected size: 5-20 lines of validation log entries

*Value Ranges:*
- N/A (text validation file)

*Data Quality:*
- Must confirm Ch6 calibration data source identified
- Must confirm master.xlsx accessibility
- No critical dependency failures

*Log Validation:*
- Required pattern: "Ch6 calibration source: results/ch6/6.2.X"
- Required pattern: "master.xlsx: ACCESSIBLE"
- Required pattern: "Dependency validation: PASS"
- Forbidden patterns: "ERROR", "FAIL", "not found"

**Expected Behavior on Validation Failure:**
- Raise error with specific missing dependency
- Log to logs/step00_validate_dependencies.log
- Quit immediately, invoke g_debug

---

### Step 1: Extract Calibration Metrics from Ch6

**Dependencies:** Step 0 (dependency validation)
**Complexity:** Medium (~8 minutes including data validation)

**Purpose:** Extract per-participant calibration quality metrics from Ch6 outputs

**Input:**
- Primary: results/ch6/6.2.*/data/*calibration*.csv (from Step 0 discovery)
- Alternative: results/ch6/*/data/*resolution*.csv or *brier*.csv
- Expected format: UID (participant), calibration_score (numeric)
- Expected N: 100 participants with valid calibration metrics

**Processing:**
- Load calibration dataset identified in Step 0
- Extract per-participant calibration quality scores
- Standardize calibration metric if multiple scales present
- Check for missing data patterns
- Verify participant IDs match expected format
- Apply exclusions: remove participants with missing calibration scores
- Log data quality summary (N, missing, range, distribution)

**Output:**
- data/step01_calibration_metrics.csv (UID, calibration_quality)

**Validation Requirement:**
Validation tools MUST be used after calibration data extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_calibration_metrics.csv: 90-100 rows x 2 columns
- Columns: UID (object), calibration_quality (float64)

*Value Ranges:*
- calibration_quality: expected range depends on metric type
- If resolution: [0, 1] (proportion correct)
- If calibration slope: [-2, 2] (regression coefficient)
- If Brier reliability: [0, 1] (reliability component)
- UID: valid participant identifiers

*Data Quality:*
- N >= 90 participants (max 10% exclusions)
- No duplicate UIDs
- No missing values in calibration_quality
- Distribution approximately normal or slightly skewed

*Log Validation:*
- Required pattern: "Calibration data loaded: N=XX participants"
- Required pattern: "Calibration metric: [resolution|slope|brier]"
- Required pattern: "Data range: [min, max]"
- Forbidden patterns: "ERROR", "missing", "invalid"

**Expected Behavior on Validation Failure:**
- Raise error with specific data quality issue
- Log to logs/step01_extract_calibration.log
- Quit immediately, invoke g_debug

---

### Step 2: Extract Cognitive Test Scores

**Dependencies:** Step 1 (calibration metrics)
**Complexity:** Medium (~8 minutes including T-score computation)

**Purpose:** Extract and standardize cognitive test scores from dfnonvr.csv

**Input:**
- data/cache/master.xlsx (RAVLT, BVMT, RPM raw scores)
- data/step01_calibration_metrics.csv (for participant matching)

**Processing:**
- Load master.xlsx, extract cognitive test columns
- Convert raw scores to T-scores (mean=50, SD=10) within sample
- Implementation: T = 50 + 10 * (X - mean(X)) / sd(X)
- Create standardized scores: RAVLT_T, BVMT_T, RPM_T
- Match to participants with calibration data
- Apply exclusions: remove participants missing cognitive test data
- Check for outliers: flag T-scores beyond 20-80 range (±3 SD)
- Compute intercorrelations between cognitive tests
- Log cognitive test descriptives and correlations

**Output:**
- data/step02_cognitive_tests.csv (UID, RAVLT_T, BVMT_T, RPM_T, Age, Sex, Education)

**Validation Requirement:**
Validation tools MUST be used after cognitive test extraction and standardization.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_cognitive_tests.csv: 90-100 rows x 7 columns
- Columns: UID (object), RAVLT_T (float64), BVMT_T (float64), RPM_T (float64), Age (int64), Sex (object), Education (int64)

*Value Ranges:*
- RAVLT_T, BVMT_T, RPM_T in [20, 80] (T-score range, approximately ±3 SD)
- Age in [18, 85] (adult sample)
- Education in [8, 20] (years of education)
- Sex in ['M', 'F'] or [0, 1]

*Data Quality:*
- N >= 90 participants (max 10% exclusions from calibration sample)
- No missing values in cognitive tests for included participants
- T-score means approximately 50 (±2), SDs approximately 10 (±2)
- Intercorrelations between tests: r < 0.80 (no extreme multicollinearity)

*Log Validation:*
- Required pattern: "Cognitive tests extracted: N=XX participants"
- Required pattern: "T-score means: RAVLT=XX, BVMT=XX, RPM=XX"
- Required pattern: "Correlation matrix computed"
- Forbidden patterns: "ERROR", "invalid", "extreme correlation"

**Expected Behavior on Validation Failure:**
- Raise error with specific cognitive test issue
- Log to logs/step02_extract_cognitive.log
- Quit immediately, invoke g_debug

---

### Step 3: Merge Data and Check Assumptions

**Dependencies:** Steps 1-2 (calibration + cognitive data)
**Complexity:** Medium (~10 minutes including assumption checks)

**Purpose:** Create analysis dataset and perform comprehensive assumption testing

**Input:**
- data/step01_calibration_metrics.csv
- data/step02_cognitive_tests.csv

**Processing:**
- Merge datasets on UID (inner join to keep complete cases only)
- Create final analysis dataset with all variables
- Check sample size adequacy: minimum N=80 for 3 predictors + covariates
- Preliminary assumption checks:
  - Linearity: scatterplots of predictors vs calibration quality
  - Normality: Shapiro-Wilk test on calibration quality
  - Multicollinearity: correlation matrix of all predictors
  - Outliers: identify cases beyond ±3 SD on any variable
- Descriptive statistics for all variables
- Correlation matrix with significance tests

**Output:**
- data/step03_analysis_dataset.csv (complete cases for regression)
- data/step03_assumption_checks.csv (linearity, normality, correlation results)

**Validation Requirement:**
Validation tools MUST be used after data merging and assumption checking.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_analysis_dataset.csv: 80-100 rows x 7 columns
- data/step03_assumption_checks.csv: assumption test results

*Value Ranges:*
- All variables within expected ranges from previous steps
- Correlations between predictors: r < 0.80 (multicollinearity check)
- Normality p-values in [0, 1]

*Data Quality:*
- Final N >= 80 (adequate for regression with 6 predictors)
- No missing values in analysis dataset
- Correlation matrix symmetric and complete
- Outliers documented if present

*Log Validation:*
- Required pattern: "Analysis dataset: N=XX complete cases"
- Required pattern: "Assumption checks completed"
- Required pattern: "Multicollinearity: acceptable"
- Forbidden patterns: "ERROR", "insufficient", "extreme"

**Expected Behavior on Validation Failure:**
- Raise error with specific data preparation issue
- Log to logs/step03_merge_data.log
- Quit immediately, invoke g_debug

---

### Step 4: Hierarchical Multiple Regression

**Dependencies:** Step 3 (analysis dataset)
**Complexity:** High (~15 minutes including bootstrap CIs)

**Purpose:** Fit hierarchical regression models to test cognitive predictors of calibration quality

**Input:**
- data/step03_analysis_dataset.csv

**Processing:**
- Model 1: Calibration_Quality ~ Age + Sex + Education (demographic controls)
- Model 2: Calibration_Quality ~ Age + Sex + Education + RAVLT_T + BVMT_T + RPM_T
- Implementation: statsmodels.api.OLS with standardized predictors
- Extract: R², adjusted R², F-statistics, AIC, BIC
- Model comparison: ΔR², F-test for model improvement
- Individual coefficients: β, SE, t-statistics, p-values
- Bootstrap 95% CIs for all coefficients:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Case resampling with replacement
  - CI: Percentile method (2.5th, 97.5th percentiles)
- Multiple comparison corrections:
  - Family: Within-step cognitive tests (3 tests: RAVLT, BVMT, RPM)
  - Bonferroni: alpha = 0.00179/3 = 0.000597 per test
  - FDR: Benjamini-Hochberg correction
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Effect sizes:
  - Cohen's f² = R²/(1-R²) for full model
  - Semi-partial correlations (sr²) for unique variance
  - Standardized betas with interpretation

**Output:**
- data/step04_regression_results.csv (model coefficients, CIs, dual p-values)
- data/step04_model_comparison.csv (model fit statistics, R² change)

**Validation Requirement:**
Validation tools MUST be used after regression analysis completion.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_regression_results.csv: 6 rows x 10 columns
- Rows: Age, Sex, Education, RAVLT_T, BVMT_T, RPM_T
- Columns: predictor, beta, se, ci_lower, ci_upper, p_uncorrected, p_bonferroni, p_fdr, sr_squared, vif
- data/step04_model_comparison.csv: 2 rows x 8 columns
- Rows: Model1_demographics, Model2_full

*Value Ranges:*
- beta in [-2, 2] (standardized coefficients)
- se > 0 (positive standard errors)
- p_values in [0, 1]
- sr_squared in [0, 1] (proportion of variance)
- R_squared in [0, 1]
- vif in [1, 10] (multicollinearity check)

*Data Quality:*
- All 6 predictors present with complete results
- Bootstrap CIs valid: ci_lower < beta < ci_upper
- Dual p-values computed (Decision D068)
- VIF < 5 for cognitive tests (multicollinearity acceptable)

*Log Validation:*
- Required pattern: "Hierarchical regression completed"
- Required pattern: "Bootstrap CIs computed: 1000 iterations"
- Required pattern: "Model 2 R² = X.XXX"
- Required pattern: "Multiple corrections applied"
- Forbidden patterns: "ERROR", "convergence failed", "singular"

**Expected Behavior on Validation Failure:**
- Raise error with specific regression issue
- Log to logs/step04_regression.log
- Quit immediately, invoke g_debug

---

### Step 5: Comprehensive Model Diagnostics

**Dependencies:** Step 4 (regression results)
**Complexity:** Medium (~12 minutes including remedial actions)

**Purpose:** Perform comprehensive regression diagnostics and implement remedial actions

**Input:**
- data/step04_regression_results.csv
- data/step03_analysis_dataset.csv (for residual analysis)

**Processing:**
- Assumption testing with explicit thresholds and remedial actions:
  - Normality: Shapiro-Wilk test on residuals
    - If p < 0.05: Report bootstrap CIs as primary inference
  - Homoscedasticity: Breusch-Pagan test
    - If p < 0.05: Compute HC3 robust standard errors
  - Multicollinearity: VIF for each predictor
    - If VIF > 5: Document concern, consider ridge if VIF > 10
  - Linearity: Rainbow test for specification
    - If p < 0.05: Add polynomial terms or transformations
  - Independence: Durbin-Watson statistic (expect ~2.0)
  - Outliers: Studentized residuals beyond ±3, Cook's D > 4/n
    - If outliers present: Report results with and without
- Influential points analysis:
  - Cook's D threshold: 4/n (approximately 0.04-0.05)
  - Leverage threshold: 2(k+1)/n where k=6 predictors
  - Document influential cases and their characteristics
- Residual analysis:
  - Standardized residuals vs fitted values
  - Q-Q plot for normality assessment
  - Distribution of residuals (histogram, skewness, kurtosis)

**Output:**
- data/step05_diagnostics.csv (assumption test results and remedial actions)
- data/step05_outliers.csv (influential points and leverage)

**Validation Requirement:**
Validation tools MUST be used after diagnostic analysis completion.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_diagnostics.csv: assumption tests and remedial actions
- data/step05_outliers.csv: outlier analysis results

*Value Ranges:*
- Shapiro-Wilk p in [0, 1]
- Breusch-Pagan p in [0, 1]
- VIF values in [1, 10] (acceptable multicollinearity)
- Cook's D in [0, 1] (influence measure)
- Durbin-Watson in [1, 3] (independence)

*Data Quality:*
- All assumption tests completed
- Remedial actions documented if triggered
- Outlier identification complete
- Diagnostic plots feasible from data

*Log Validation:*
- Required pattern: "Assumption testing completed"
- Required pattern: "Outlier analysis: X cases identified"
- Required pattern: "Remedial actions: [list or none]"
- Forbidden patterns: "ERROR", "failed", "invalid"

**Expected Behavior on Validation Failure:**
- Raise error with specific diagnostic issue
- Log to logs/step05_diagnostics.log
- Quit immediately, invoke g_debug

---

### Step 6: Cross-Validation and Overfitting Assessment

**Dependencies:** Step 5 (diagnostic results)
**Complexity:** Medium (~10 minutes including CV iterations)

**Purpose:** Assess model generalizability and detect overfitting using cross-validation

**Input:**
- data/step03_analysis_dataset.csv (for CV splitting)
- Model specification from Step 4

**Processing:**
- Implement 5-fold cross-validation:
  - Random seed: 42 for reproducibility
  - Stratification: Quantile-based on calibration_quality (if skewed)
  - Shuffle: True (randomize before splitting)
  - For each fold: fit full model on training (80%), evaluate on test (20%)
- Cross-validation metrics:
  - Test R² for each fold
  - RMSE (Root Mean Square Error)
  - MAE (Mean Absolute Error)
  - Prediction intervals
- Overfitting assessment:
  - Training R² vs Test R² gap
  - Flag if gap > 0.10 (overfitting threshold)
  - Report mean and SD of CV metrics
- Stability analysis:
  - Coefficient stability across folds
  - Identify predictors with inconsistent signs
  - Bootstrap model selection: frequency of predictor significance

**Output:**
- data/step06_cross_validation.csv (CV results by fold)
- data/step06_overfitting_assessment.csv (training vs test comparison)

**Validation Requirement:**
Validation tools MUST be used after cross-validation analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_cross_validation.csv: 5 rows x 6 columns
- Columns: fold, train_r2, test_r2, rmse, mae, n_train, n_test
- data/step06_overfitting_assessment.csv: summary statistics

*Value Ranges:*
- train_r2, test_r2 in [0, 1]
- rmse, mae > 0 (positive error metrics)
- Overfitting gap = train_r2 - test_r2 should be < 0.10

*Data Quality:*
- All 5 folds completed successfully
- CV metrics within reasonable bounds
- No extreme overfitting detected
- Coefficient stability documented

*Log Validation:*
- Required pattern: "5-fold CV completed"
- Required pattern: "Mean test R² = X.XXX"
- Required pattern: "Overfitting gap: X.XXX"
- Forbidden patterns: "ERROR", "failed", "extreme"

**Expected Behavior on Validation Failure:**
- Raise error with specific CV issue
- Log to logs/step06_cross_validation.log
- Quit immediately, invoke g_debug

---

### Step 7: Power Analysis and Effect Size Interpretation

**Dependencies:** Step 6 (cross-validation results)
**Complexity:** Medium (~8 minutes including power calculations)

**Purpose:** Perform post-hoc power analysis and interpret effect sizes

**Input:**
- data/step04_regression_results.csv
- data/step06_cross_validation.csv

**Processing:**
- Post-hoc power analysis for hierarchical regression:
  - Given: Final N from CV analysis, 6 predictors total, alpha=0.000597 (Bonferroni)
  - Calculate: Actual power for observed R² and ΔR²
  - Software: statsmodels.stats.power.FTestAnovaPower()
  - Report: Power for overall model and for R² increment
- Sensitivity analysis:
  - Minimum detectable effect (f²) at 80% power
  - Sample size needed for small (f²=0.02), medium (f²=0.15), large (f²=0.35) effects
  - Power curves for range of effect sizes
- Effect size interpretation:
  - Cohen's conventions for f² (small=0.02, medium=0.15, large=0.35)
  - Semi-partial correlations with practical significance thresholds
  - Confidence interval interpretation for practical vs statistical significance
- Comparison to accuracy prediction (RQ 7.1.1):
  - Load results from results/ch7/7.1.1/data/*regression*.csv if available
  - Compare R² for calibration vs accuracy prediction
  - Identify differential predictors

**Output:**
- data/step07_power_analysis.csv (power calculations and sensitivity analysis)
- data/step07_effect_sizes.csv (interpreted effect sizes with practical significance)

**Validation Requirement:**
Validation tools MUST be used after power and effect size analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_power_analysis.csv: power analysis results
- data/step07_effect_sizes.csv: effect size interpretations

*Value Ranges:*
- Power values in [0, 1]
- Effect sizes (f²) >= 0
- Confidence intervals: lower < estimate < upper

*Data Quality:*
- Power analysis completed for all tests
- Effect size interpretations provided
- Comparison to 7.1.1 attempted (may fail if not available)

*Log Validation:*
- Required pattern: "Power analysis completed"
- Required pattern: "Effect sizes interpreted"
- Required pattern: "Overall model power: X.XX"
- Acceptable warnings: "7.1.1 comparison: data not found"
- Forbidden patterns: "ERROR", "invalid", "calculation failed"

**Expected Behavior on Validation Failure:**
- Raise error with specific power analysis issue
- Log to logs/step07_power_analysis.log
- Quit immediately, invoke g_debug

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt
- data/step01_calibration_metrics.csv
- data/step02_cognitive_tests.csv
- data/step03_analysis_dataset.csv
- data/step03_assumption_checks.csv
- data/step04_regression_results.csv
- data/step04_model_comparison.csv
- data/step05_diagnostics.csv
- data/step05_outliers.csv
- data/step06_cross_validation.csv
- data/step06_overfitting_assessment.csv
- data/step07_power_analysis.csv
- data/step07_effect_sizes.csv

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_calibration.log
- logs/step02_extract_cognitive.log
- logs/step03_merge_data.log
- logs/step04_regression.log
- logs/step05_diagnostics.log
- logs/step06_cross_validation.log
- logs/step07_power_analysis.log

### Plots (EMPTY until rq_plots runs)
Note: Plot source CSV files created in data/ folder:
- data/step05_diagnostic_plots_data.csv (residuals, Q-Q, leverage)
- data/step07_predictor_importance_plot_data.csv (coefficient comparison)

### Results (EMPTY until rq_results runs)
Note: summary.md will be created by rq_results agent

---

## Expected Data Formats

### Step-to-Step Transformations
1. Step 0 → Step 1: Dependency validation identifies Ch6 calibration source
2. Step 1 → Step 2: Per-participant calibration metrics extracted
3. Step 2 → Step 3: Cognitive test T-scores computed and merged
4. Step 3 → Step 4: Complete analysis dataset for regression
5. Step 4 → Step 5: Regression coefficients for diagnostic testing
6. Step 5 → Step 6: Validated model for cross-validation
7. Step 6 → Step 7: CV results for power analysis

### Column Naming Conventions
- UID: Participant identifier (consistent across all files)
- calibration_quality: Standardized calibration metric
- RAVLT_T, BVMT_T, RPM_T: T-scored cognitive tests (mean=50, SD=10)
- Age, Sex, Education: Demographic controls
- beta, se, ci_lower, ci_upper: Regression coefficients with CIs
- p_uncorrected, p_bonferroni, p_fdr: Dual p-value reporting (Decision D068)

### Data Type Constraints
- UID: object (non-nullable)
- Numeric variables: float64 (nullable for intermediate processing, non-nullable in final dataset)
- Categorical variables: object for Sex, int64 for Education
- P-values: float64 in [0, 1]
- Effect sizes: float64 >= 0

---

## Cross-RQ Dependencies

**Ch6 Calibration Analysis (Required):**
- Primary: results/ch6/6.2.*/data/*calibration*.csv
- Alternative: results/ch6/*/data/*resolution*.csv or *brier*.csv
- Fallback: Any Ch6 analysis with per-participant calibration metrics
- Format: UID, calibration_score (or similar metric)
- Validation: Step 0 verifies availability and format

**Ch7 7.1.1 Accuracy Prediction (Optional):**
- For comparison: results/ch7/7.1.1/data/*regression*.csv
- Used in Step 7 for calibration vs accuracy predictor comparison
- Not required for core analysis completion

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
- Verifies Ch6 calibration data availability
- Checks master.xlsx accessibility
- Documents data sources for downstream steps

#### Step 1: Extract Calibration Metrics
- Validates calibration data quality and range
- Ensures adequate sample size (N >= 90)
- Checks for missing data patterns

#### Step 2: Extract Cognitive Tests
- Validates T-score transformations (mean≈50, SD≈10)
- Checks correlation matrix for multicollinearity
- Ensures complete cognitive test data

#### Step 3: Merge Data and Check Assumptions
- Validates merged dataset completeness
- Checks preliminary assumption satisfaction
- Ensures adequate sample size for regression

#### Step 4: Hierarchical Multiple Regression
- Validates regression convergence and coefficients
- Ensures bootstrap CI computation
- Verifies dual p-value reporting (Decision D068)

#### Step 5: Comprehensive Model Diagnostics
- Validates assumption test completion
- Ensures remedial actions implemented if needed
- Checks outlier identification accuracy

#### Step 6: Cross-Validation and Overfitting Assessment
- Validates CV fold completion
- Checks overfitting threshold compliance
- Ensures stability assessment completion

#### Step 7: Power Analysis and Effect Size Interpretation
- Validates power calculation accuracy
- Ensures effect size interpretation completeness
- Checks comparison to 7.1.1 if data available

---

## Summary

**Total Steps:** 8 (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** 45-60 minutes
**Cross-RQ Dependencies:** Ch6 calibration analysis (required), Ch7 7.1.1 (optional comparison)
**Primary Outputs:** Hierarchical regression results with comprehensive diagnostics and cross-validation

**Key Hypothesis:** RPM (fluid intelligence) will predict calibration quality more strongly than RAVLT/BVMT (memory tests), reflecting the distinction between memory capacity and metacognitive monitoring processes.

**Critical Methodological Notes:**
- Bootstrap CIs with 1000 iterations for robust inference with N=100
- Comprehensive remedial actions for assumption violations
- Dual p-value reporting (Decision D068) with Bonferroni correction (alpha=0.000597)
- Cross-validation to assess generalizability and overfitting
- Comparison to accuracy prediction (7.1.1) for theoretical interpretation

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent v5.1