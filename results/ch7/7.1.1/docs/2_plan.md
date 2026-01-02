# Analysis Plan: Do cognitive tests predict overall REMEMVR ability?

**Research Question:** 7.1.1
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This analysis examines the predictive relationship between four standardized cognitive tests (RAVLT, BVMT, NART, RPM) and overall episodic memory ability as measured by REMEMVR theta scores. The analysis addresses core convergent validity for the REMEMVR assessment by testing whether traditional neuropsychological tests predict ecological VR memory performance.

**Pipeline:** Multiple Linear Regression (cognitive tests as predictors)
**Steps:** 8 total analysis steps
**Estimated Runtime:** Medium (15-30 minutes total)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting for multiple comparisons (uncorrected + Bonferroni)
- Chapter 7 alpha correction: 0.05/28 RQs = 0.00179 per RQ
- Within-RQ Bonferroni: alpha = 0.00179/4 predictors = 0.000448 per predictor

---

## Analysis Plan

### Step 0: Extract Cognitive Test Data

**Dependencies:** None (first step)
**Complexity:** Low (data extraction only)

**Input:**
- File: data/cache/master.xlsx (project-level data source)
- Required sheets: Main data sheet with cognitive test columns
- Tag patterns:
  - RAVLT trials: {UID}-COG-X-RAV-T1Sc, T2Sc, T3Sc, T4Sc, T5Sc
  - RAVLT delayed: {UID}-COG-X-RAV-DRSc
  - BVMT total: {UID}-COG-X-BVM-TotR
  - NART score: {UID}-COG-X-NAR-Scor
  - RPM score: {UID}-COG-X-RPM-Scor

**Processing:**
- Extract cognitive test raw scores using master.xlsx tag patterns
- Compute RAVLT_Total = sum(T1Sc, T2Sc, T3Sc, T4Sc, T5Sc)
- Retain BVMT_TotR, NART_Scor, RPM_Scor as extracted
- Standardize all tests to T-scores (M=50, SD=10) for comparability
- Handle missing data with listwise deletion (report final n)

**Output:**
- File: data/step00_cognitive_tests.csv
- Format: CSV, one row per participant
- Columns:
  - UID (string, participant identifier)
  - RAVLT_T1Sc through T5Sc (int, 0-15 each)
  - RAVLT_Total (int, sum T1-T5, range 0-75)
  - BVMT_TotR (int, 0-36)
  - NART_Scor (int, 0-50)
  - RPM_Scor (int, 0-12)
  - RAVLT_T, BVMT_T, NART_T, RPM_T (float, T-scores M=50, SD=10)
- Expected Rows: 100 participants (or n after listwise deletion)

**Validation Requirement:**
Validation tools MUST be used after data extraction execution. Specific validation tools will be determined by rq_tools based on data extraction requirements. The rq_analysis agent will embed validation tool calls after the extraction tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_cognitive_tests.csv: 100 rows x 10 columns (UID: object, raw scores: int64, T-scores: float64)

*Value Ranges:*
- RAVLT_Total in [0, 75] (sum of 5 trials, 0-15 each)
- BVMT_TotR in [0, 36] (Brief Visuospatial Memory Test total)
- NART_Scor in [0, 50] (National Adult Reading Test)
- RPM_Scor in [0, 12] (Raven's Progressive Matrices)
- T-scores approximately M=50, SD=10 (standardization check)

*Data Quality:*
- All 100 participants present (or report n if exclusions)
- No NaN values in T-score columns (complete standardization)
- No duplicate UIDs (participant-level data)
- T-score distributions approximately normal (M H 50, SD H 10)

*Log Validation:*
- Required pattern: "Cognitive tests extracted: N participants"
- Required pattern: "T-scores computed: M=50.0, SD=10.0"
- Forbidden patterns: "ERROR", "Missing required columns", "Standardization failed"
- Acceptable warnings: "N participants excluded due to missing data"

**Expected Behavior:**
Successfully extract cognitive test data, compute derived scores, standardize to T-scores, and save processed data for regression analysis. File should contain standardized predictors ready for merging with theta scores.

---

### Step 1: Load REMEMVR Theta Scores

**Dependencies:** Step 0 (cognitive tests must be ready for merging)
**Complexity:** Low (file loading and aggregation)

**Input:**
- File: results/ch5/5.1.1/data/step03_theta_scores.csv
- Format: CSV with IRT theta estimates from Ch5 omnibus "All" factor analysis
- Expected columns:
  - composite_ID (string, format: UID_test)
  - theta (float, IRT ability estimate)
  - SE (float, standard error of theta)
- Expected structure: ~400 rows (100 participants x 4 test sessions)

**Processing:**
- Load theta scores from Ch5 5.1.1 analysis (omnibus "All" factor)
- Parse composite_ID to extract UID and test session number
- Group by UID and compute mean theta across 4 test sessions per participant
- Compute mean SE across sessions for measurement error assessment
- Validate that all participants have data from multiple sessions

**Output:**
- File: data/step01_theta_mean.csv
- Format: CSV, one row per participant
- Columns:
  - UID (string, participant identifier)
  - theta_mean (float, mean IRT ability across 4 sessions)
  - SE_mean (float, mean standard error across sessions)
  - n_sessions (int, number of sessions with data, should be 4)
- Expected Rows: 100 participants

**Validation Requirement:**
Validation tools MUST be used after theta aggregation execution. Specific validation tools will be determined by rq_tools based on IRT theta processing requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_theta_mean.csv: 100 rows x 4 columns (UID: object, theta_mean: float64, SE_mean: float64, n_sessions: int64)

*Value Ranges:*
- theta_mean in [-3, 3] (typical IRT ability range)
- SE_mean in [0.1, 1.0] (reasonable measurement precision)
- n_sessions = 4 for all participants (complete longitudinal data)

*Data Quality:*
- All 100 participants present from Ch5 analysis
- No NaN values in theta_mean (all participants have valid estimates)
- No duplicate UIDs (one mean per participant)
- theta_mean distribution approximately normal (population distribution)

*Log Validation:*
- Required pattern: "Theta scores aggregated: 100 participants"
- Required pattern: "Mean sessions per participant: 4.0"
- Forbidden patterns: "ERROR", "Missing theta data", "Aggregation failed"
- Acceptable warnings: None expected (Ch5 data should be complete)

**Expected Behavior:**
Load theta scores from Ch5, compute participant-level means across test sessions, and prepare dependent variable for regression analysis.

---

### Step 2: Merge Cognitive Tests with Theta Scores

**Dependencies:** Steps 0, 1 (both cognitive tests and theta scores ready)
**Complexity:** Low (data merging)

**Input:**
- File 1: data/step00_cognitive_tests.csv (cognitive predictors)
- File 2: data/step01_theta_mean.csv (REMEMVR dependent variable)
- Merge key: UID (participant identifier)

**Processing:**
- Merge cognitive tests and theta scores on UID using inner join
- Verify all participants have both cognitive and theta data
- Create analysis dataset with predictors and dependent variable
- Apply listwise deletion for any remaining missing data
- Save final analysis dataset for regression modeling

**Output:**
- File: data/step02_analysis_dataset.csv
- Format: CSV, one row per participant with complete data
- Columns:
  - UID (string)
  - theta_mean (float, dependent variable)
  - SE_mean (float, for measurement error assessment)
  - RAVLT_T, BVMT_T, NART_T, RPM_T (float, T-score predictors)
  - n_sessions (int, data quality check)
- Expected Rows: 100 participants (or n after listwise deletion)

**Validation Requirement:**
Validation tools MUST be used after data merging execution. Specific validation tools will be determined by rq_tools based on data integration requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_analysis_dataset.csv: N rows x 7 columns (complete cases only)

*Value Ranges:*
- theta_mean in [-3, 3] (preserved from Step 1)
- T-scores approximately M=50, SD=10 (preserved from Step 0)
- N >= 95 (minimal missing data expected)

*Data Quality:*
- No NaN values (complete cases only)
- No duplicate UIDs (one row per participant)
- All required columns present with correct data types

*Log Validation:*
- Required pattern: "Analysis dataset created: N participants with complete data"
- Required pattern: "Merge successful: 100% match rate"
- Forbidden patterns: "ERROR", "Merge failed", "Massive data loss"
- Acceptable warnings: "X participants excluded due to missing data"

**Expected Behavior:**
Merge cognitive tests and theta scores, apply listwise deletion for missing data, and create final analysis dataset ready for regression modeling.

---

### Step 3: Check Regression Assumptions

**Dependencies:** Step 2 (analysis dataset must be ready)
**Complexity:** Medium (multiple diagnostic tests)

**Input:**
- File: data/step02_analysis_dataset.csv
- Required columns: theta_mean (DV), RAVLT_T, BVMT_T, NART_T, RPM_T (IVs)

**Processing:**
- Test normality of residuals (Shapiro-Wilk test, Q-Q plots)
- Test homoscedasticity (Breusch-Pagan test, residual plots)
- Check multicollinearity (VIF calculations, correlation matrix)
- Identify outliers (Cook's D, leverage, studentized residuals)
- Generate diagnostic plots for visual inspection
- Apply remedial measures if assumptions violated:
  - Normality violation: Use robust standard errors or bootstrap CIs
  - Heteroscedasticity: Use HC3 heteroscedasticity-consistent SEs
  - Multicollinearity: Consider ridge regression or drop predictors (VIF > 5)
  - Outliers: Report analyses with and without influential points

**Output:**
- File: data/step03_regression_diagnostics.csv
- Format: CSV with diagnostic statistics
- Columns:
  - Test (string, diagnostic test name)
  - Statistic (float, test statistic value)
  - p_value (float, significance test)
  - Interpretation (string, pass/fail/concern)
  - Remedial_Action (string, action taken if violated)
- Additional files:
  - data/step03_vif_values.csv (variance inflation factors)
  - data/step03_outlier_analysis.csv (Cook's D, leverage values)

**Validation Requirement:**
Validation tools MUST be used after regression diagnostics execution. Specific validation tools will be determined by rq_tools based on assumption testing requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_regression_diagnostics.csv: Multiple rows x 5 columns (diagnostic results)
- data/step03_vif_values.csv: 4 rows x 2 columns (predictor: object, VIF: float64)

*Value Ranges:*
- VIF values in [1.0, 10.0] (multicollinearity check, prefer < 5.0)
- p_values in [0, 1] (statistical tests)
- Cook's D typically < 4/n (outlier threshold)

*Data Quality:*
- All required diagnostic tests completed (normality, homoscedasticity, VIF, outliers)
- No NaN values in diagnostic statistics (all tests executed)
- Interpretation column provides clear pass/fail assessment

*Log Validation:*
- Required pattern: "Assumption checks completed: X tests run"
- Required pattern: "VIF analysis: Max VIF = X.XX"
- Forbidden patterns: "ERROR", "Diagnostic test failed", "Cannot compute VIF"
- Acceptable warnings: "Assumption violated: [specific assumption]"

**Expected Behavior:**
Comprehensive regression diagnostics with specific remedial actions documented for any violations. Provides clear guidance for subsequent regression analysis approach.

---

### Step 4: Fit Multiple Linear Regression Model

**Dependencies:** Step 3 (diagnostics complete, remedial actions applied)
**Complexity:** Medium (regression analysis with effect sizes)

**Input:**
- File: data/step02_analysis_dataset.csv
- Diagnostic guidance: data/step03_regression_diagnostics.csv
- Model specification: theta_mean ~ RAVLT_T + BVMT_T + NART_T + RPM_T

**Processing:**
- Fit multiple linear regression model using appropriate method based on diagnostics
- Apply robust standard errors if heteroscedasticity detected
- Extract model summary: coefficients, standard errors, t-statistics, p-values
- Compute overall model fit: R-squared, adjusted R-squared, F-statistic
- Calculate effect sizes: standardized beta coefficients, semi-partial correlations (sr²)
- Generate 95% confidence intervals for all coefficients using bootstrap (1000 replications)
- Apply Chapter 7 significance threshold: alpha = 0.00179

**Output:**
- File: data/step04_regression_results.csv
- Format: CSV with comprehensive regression results
- Columns:
  - Predictor (string, variable name)
  - Beta (float, unstandardized coefficient)
  - SE (float, standard error)
  - Beta_std (float, standardized coefficient)
  - t_stat (float, t-statistic)
  - p_value (float, uncorrected p-value)
  - CI_lower (float, 95% CI lower bound)
  - CI_upper (float, 95% CI upper bound)
  - sr2 (float, semi-partial correlation squared)
- Additional file: data/step04_model_summary.txt (overall model statistics)

**Validation Requirement:**
Validation tools MUST be used after regression model fitting execution. Specific validation tools will be determined by rq_tools based on regression analysis requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_regression_results.csv: 4 rows x 9 columns (one row per predictor)
- data/step04_model_summary.txt: Text file with R², F-test, degrees of freedom

*Value Ranges:*
- Beta coefficients unrestricted (can be positive or negative)
- SE values > 0 (standard errors must be positive)
- p_values in [0, 1] (probability values)
- sr2 values in [0, 1] (proportion of variance)
- CI bounds: CI_lower < Beta < CI_upper (confidence interval consistency)

*Data Quality:*
- All 4 predictors present (RAVLT_T, BVMT_T, NART_T, RPM_T)
- No NaN values in coefficient estimates (model converged)
- Sum of sr2 values <= R² (semi-partial correlations additive property)

*Log Validation:*
- Required pattern: "Regression model fitted successfully"
- Required pattern: "Overall R² = X.XX, F(4,N) = X.XX, p = X.XXX"
- Forbidden patterns: "ERROR", "Model failed to converge", "Singular matrix"
- Acceptable warnings: "Robust standard errors applied due to heteroscedasticity"

**Expected Behavior:**
Successful regression model fitting with comprehensive output including coefficients, effect sizes, and confidence intervals. Model should explain moderate variance (R² = 0.25-0.50) with at least one significant predictor.

---

### Step 5: Apply Multiple Comparison Corrections

**Dependencies:** Step 4 (regression results must be available)
**Complexity:** Low (p-value corrections)

**Input:**
- File: data/step04_regression_results.csv
- Required: uncorrected p-values for 4 predictors

**Processing:**
- Apply Bonferroni correction for 4 predictors: alpha_corrected = 0.00179/4 = 0.000448
- Compute corrected p-values: p_corrected = p_uncorrected x 4
- Apply Chapter 7 alpha threshold (alpha = 0.00179) to overall model
- Flag significant predictors at both uncorrected and corrected levels
- Generate Decision D068 dual p-value reporting table
- Create significance summary with both correction levels

**Output:**
- File: data/step05_corrected_results.csv
- Format: CSV with dual p-value reporting per Decision D068
- Columns:
  - Predictor (string)
  - Beta_std (float, standardized coefficient)
  - p_uncorrected (float, original p-value)
  - p_bonferroni (float, Bonferroni-corrected p-value)
  - sig_uncorrected (boolean, p < 0.05)
  - sig_bonferroni (boolean, p < 0.000448)
  - sig_chapter (boolean, p < 0.00179 for overall model)
- Additional file: data/step05_significance_summary.txt

**Validation Requirement:**
Validation tools MUST be used after multiple comparison correction execution. Specific validation tools will be determined by rq_tools based on dual p-value reporting requirements (Decision D068).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_corrected_results.csv: 4 rows x 7 columns (dual p-values per predictor)

*Value Ranges:*
- p_uncorrected in [0, 1] (original probability values)
- p_bonferroni in [0, 4.0] (may exceed 1.0 after correction)
- Bonferroni p-values = uncorrected p-values x 4 (correction formula)

*Data Quality:*
- All 4 predictors present with dual p-values
- Boolean flags correctly assigned based on thresholds
- No NaN values in corrected results

*Log Validation:*
- Required pattern: "Bonferroni correction applied: alpha = 0.000448"
- Required pattern: "Chapter 7 threshold: alpha = 0.00179"
- Forbidden patterns: "ERROR", "Correction failed"
- Acceptable warnings: "No predictors survive Bonferroni correction"

**Expected Behavior:**
Apply multiple comparison corrections per Decision D068, generate dual p-value reporting table, and identify significant predictors at different alpha levels.

---

### Step 6: Compute Predictor Importance and Rankings

**Dependencies:** Step 5 (corrected results must be available)
**Complexity:** Medium (importance analysis)

**Input:**
- Files: data/step04_regression_results.csv, data/step05_corrected_results.csv
- Required: standardized betas, semi-partial correlations

**Processing:**
- Rank predictors by standardized beta magnitude (absolute values)
- Compute relative importance weights (semi-partial correlations squared)
- Test specific hypothesis: RAVLT_beta > RPM_beta (episodic memory > fluid intelligence)
- Perform dominance analysis or relative importance decomposition
- Calculate unique variance explained by each predictor (sr²)
- Generate predictor importance visualization data
- Test theoretical prediction about episodic vs intelligence tests

**Output:**
- File: data/step06_predictor_importance.csv
- Format: CSV with importance rankings
- Columns:
  - Predictor (string)
  - Beta_std (float, standardized coefficient)
  - Beta_abs (float, absolute standardized coefficient)
  - sr2 (float, unique variance explained)
  - Rank_Beta (int, rank by beta magnitude)
  - Rank_sr2 (int, rank by unique variance)
  - Test_Type (string, "Episodic" vs "Intelligence")
  - Dominance_Weight (float, relative importance weight)

**Validation Requirement:**
Validation tools MUST be used after predictor importance analysis execution. Specific validation tools will be determined by rq_tools based on importance ranking requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_predictor_importance.csv: 4 rows x 8 columns (importance metrics per predictor)

*Value Ranges:*
- Beta_abs >= 0 (absolute values)
- sr2 values in [0, 1] (proportion of variance)
- Ranks in [1, 4] (1=highest importance, 4=lowest)
- Dominance_Weight in [0, 1] (sum to approximately 1.0)

*Data Quality:*
- All predictors ranked (no ties in ranking columns)
- Sum of sr2 values <= R² from Step 4 (variance decomposition)
- Test_Type correctly assigned: RAVLT/BVMT = "Episodic", RPM/NART = "Intelligence"

*Log Validation:*
- Required pattern: "Predictor rankings computed successfully"
- Required pattern: "Hypothesis test: RAVLT vs RPM comparison"
- Forbidden patterns: "ERROR", "Ranking failed", "Invalid importance weights"
- Acceptable warnings: "Close ranking values may indicate similar importance"

**Expected Behavior:**
Rank predictors by importance, test theoretical hypotheses about predictor types, and quantify unique variance contributions for each cognitive test.

---

### Step 7: Sensitivity Analysis

**Dependencies:** Step 6 (predictor importance analysis complete)
**Complexity:** Medium (model comparison)

**Input:**
- File: data/step02_analysis_dataset.csv
- Comparison models:
  - Full model: theta_mean ~ RAVLT_T + BVMT_T + NART_T + RPM_T
  - Reduced model: theta_mean ~ RAVLT_T + BVMT_T + RPM_T (exclude NART)

**Processing:**
- Fit reduced model excluding NART (language validity concerns from concept.md)
- Compare full vs reduced model R-squared values
- Perform F-test for model comparison (incremental validity of NART)
- Implement 5-fold cross-validation for both models
- Assess train-test generalization gap (should be < 0.10)
- Report model stability and overfitting assessment
- Generate recommendations for final model selection

**Output:**
- File: data/step07_sensitivity_analysis.csv
- Format: CSV with model comparison results
- Columns:
  - Model (string, "Full" vs "Reduced")
  - R2_train (float, training R-squared)
  - R2_CV (float, cross-validated R-squared)
  - Shrinkage (float, R2_train - R2_CV)
  - AIC (float, Akaike Information Criterion)
  - F_test_p (float, incremental F-test p-value for NART)
  - Recommendation (string, preferred model)
- Additional file: data/step07_cv_results.csv (cross-validation details)

**Validation Requirement:**
Validation tools MUST be used after sensitivity analysis execution. Specific validation tools will be determined by rq_tools based on model comparison requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_sensitivity_analysis.csv: 2 rows x 7 columns (Full vs Reduced model)
- data/step07_cv_results.csv: 10 rows (5 folds x 2 models)

*Value Ranges:*
- R2 values in [0, 1] (proportion of variance explained)
- Shrinkage >= 0 (cross-validation R² <= training R²)
- Shrinkage < 0.10 (acceptable generalization gap)
- AIC values > 0 (information criterion)

*Data Quality:*
- Both models present (Full and Reduced)
- Cross-validation completed for both models (5 folds each)
- F-test p-value for NART incremental validity computed

*Log Validation:*
- Required pattern: "Sensitivity analysis completed: 2 models compared"
- Required pattern: "Cross-validation: 5 folds per model"
- Required pattern: "NART incremental validity: F-test p = X.XXX"
- Forbidden patterns: "ERROR", "Model comparison failed", "Cross-validation error"
- Acceptable warnings: "High shrinkage detected" (if > 0.10)

**Expected Behavior:**
Compare full vs reduced models, assess NART's incremental validity, and provide cross-validated model performance estimates with overfitting assessment.

---

### Step 8: Generate Summary Results

**Dependencies:** Step 7 (all analyses complete)
**Complexity:** Low (results compilation)

**Input:**
- Multiple data files from Steps 4-7
- Required files:
  - data/step04_model_summary.txt (overall model fit)
  - data/step05_corrected_results.csv (dual p-values)
  - data/step06_predictor_importance.csv (rankings)
  - data/step07_sensitivity_analysis.csv (model comparison)

**Processing:**
- Compile comprehensive results summary for thesis reporting
- Format results in APA style with effect sizes and confidence intervals
- Generate variance decomposition breakdown (explained vs unexplained)
- Create predictor comparison table with episodic vs intelligence tests
- Summarize success criteria achievement
- Generate recommendations for clinical interpretation
- Format for integration into Ch7 results section

**Output:**
- File: data/step08_final_summary.md
- Format: Markdown summary ready for thesis integration
- Contains:
  - Model equation with standardized coefficients
  - Variance decomposition (total R², residual variance)
  - Predictor rankings with dual p-values
  - Cross-validation results and model recommendations
  - Success criteria evaluation
  - Clinical interpretation guidance

**Validation Requirement:**
Validation tools MUST be used after summary generation execution. Specific validation tools will be determined by rq_tools based on results compilation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_final_summary.md: Markdown file with formatted results (minimum 100 lines)

*Value Ranges:*
- All numeric values consistent with prior steps (no transcription errors)
- R² values preserved from Step 4 analysis
- Rankings preserved from Step 6 analysis

*Data Quality:*
- All major results included (model fit, coefficients, rankings, cross-validation)
- APA formatting for statistical results (p-values, confidence intervals)
- Success criteria explicitly evaluated (pass/fail assessment)

*Log Validation:*
- Required pattern: "Summary compilation completed successfully"
- Required pattern: "All prior steps integrated into final summary"
- Forbidden patterns: "ERROR", "Missing results", "Compilation failed"
- Acceptable warnings: None expected for summary generation

**Expected Behavior:**
Generate comprehensive, publication-ready summary of all regression analyses with APA formatting and clear interpretation guidance for Ch7 integration.

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs - intermediate and final)
- data/step00_cognitive_tests.csv (from Step 0: cognitive test extraction and standardization)
- data/step01_theta_mean.csv (from Step 1: REMEMVR theta aggregation)
- data/step02_analysis_dataset.csv (from Step 2: merged cognitive + theta data)
- data/step03_regression_diagnostics.csv (from Step 3: assumption checks)
- data/step03_vif_values.csv (from Step 3: multicollinearity assessment)
- data/step03_outlier_analysis.csv (from Step 3: outlier detection)
- data/step04_regression_results.csv (from Step 4: regression coefficients)
- data/step04_model_summary.txt (from Step 4: overall model fit statistics)
- data/step05_corrected_results.csv (from Step 5: dual p-value reporting)
- data/step05_significance_summary.txt (from Step 5: correction summary)
- data/step06_predictor_importance.csv (from Step 6: importance rankings)
- data/step07_sensitivity_analysis.csv (from Step 7: model comparison)
- data/step07_cv_results.csv (from Step 7: cross-validation details)
- data/step08_final_summary.md (from Step 8: formatted results summary)

### Logs (ONLY execution logs - .log files capturing stdout/stderr)
- logs/step00_extract_cognitive_tests.log
- logs/step01_load_theta_scores.log
- logs/step02_merge_datasets.log
- logs/step03_check_assumptions.log
- logs/step04_fit_regression.log
- logs/step05_apply_corrections.log
- logs/step06_compute_importance.log
- logs/step07_sensitivity_analysis.log
- logs/step08_generate_summary.log

### Plots (EMPTY until rq_plots runs)
- plots/ (remains empty until rq_plots agent generates visualizations)

### Results (EMPTY until rq_results runs)
- results/ (remains empty until rq_results agent generates final summary)

---

## Expected Data Formats

### Cognitive Test Data Transformations

**Step 0 Output Format:**
- RAVLT_Total computed as sum(T1Sc + T2Sc + T3Sc + T4Sc + T5Sc)
- All test scores standardized to T-scores: T_score = 50 + 10 * ((raw - mean) / SD)
- Wide format: one row per participant, one column per test

**Step 1-2 Aggregation:**
- Theta scores aggregated from longitudinal (4 sessions) to cross-sectional (1 mean per UID)
- Merge performed on UID as primary key
- Analysis dataset in wide format for regression modeling

### Column Naming Conventions

Following established naming patterns from names.md:
- UID: participant identifier (no composite_ID needed for cross-sectional)
- theta_mean: dependent variable (aggregated IRT ability estimate)
- RAVLT_T, BVMT_T, NART_T, RPM_T: standardized predictor variables (T-score suffix)
- Beta_std: standardized regression coefficient (consistent with LMM naming)

### Data Type Constraints

**Required Data Types:**
- UID: string/object (participant identifiers)
- theta_mean: float64 (continuous dependent variable)
- T-score predictors: float64 (continuous standardized predictors)
- Beta coefficients: float64 (regression output)
- p_values: float64 (statistical significance testing)
- Boolean flags: bool (significance indicators)

**Missing Data Handling:**
- Listwise deletion applied at Step 2 (complete cases analysis)
- Missing data tolerance: Target N >= 95 (expect minimal missing cognitive data)
- Report final sample size after exclusions

---

## Cross-RQ Dependencies

### Dependency Type: DERIVED Data from Ch5

**This RQ requires outputs from:**
- **RQ 5.1.1** (Functional Form Comparison - General omnibus theta scores)
  - File: results/ch5/5.1.1/data/step03_theta_scores.csv
  - Used in: Step 1 (load REMEMVR dependent variable)
  - Rationale: RQ 5.1.1 provides the omnibus "All" factor theta scores representing overall episodic memory ability across all domains (What/Where/When) and paradigms (Free/Cued/Recognition)

**Execution Order Constraint:**
1. Ch5 RQ 5.1.1 must complete Steps 1-3 (IRT calibration with omnibus factor)
2. This RQ can then execute (uses theta scores as dependent variable)

**Data Source Boundaries:**
- **RAW data:** master.xlsx cognitive test scores (independent extraction)
- **DERIVED data:** Ch5 5.1.1 theta scores (dependent on prior IRT analysis)
- **Scope:** This RQ does NOT re-analyze REMEMVR items (uses Ch5 theta estimates as given)

**Validation:**
- Step 1: Check results/ch5/5.1.1/data/step03_theta_scores.csv exists
- Step 1: Verify theta scores contain omnibus "All" factor data (not domain-specific)
- If file missing -> quit with error -> user must execute Ch5 5.1.1 first
- Expected N: 400 rows (100 participants x 4 test sessions) -> aggregate to 100

---

## Validation Requirements

**CRITICAL MANDATE:**

Every analysis step in this plan MUST use validation tools after analysis tool execution.

This is not optional. This is the core architectural principle preventing cascading failures observed in v3.0 (where analysis errors propagated undetected through 5+ downstream steps before discovery).

**Exact Specification Requirement:**

> "Validation tools MUST be used after analysis tool execution"

**Implementation:**
- rq_tools (Step 11 workflow) will read tool_inventory.md validation tools section
- rq_tools will specify BOTH analysis tool + validation tool per step in 3_tools.yaml
- rq_analysis (Step 12 workflow) will embed validation tool call AFTER analysis tool call in 4_analysis.yaml
- g_code (Step 14 workflow) will generate stepN_name.py scripts with validation function calls
- bash execution (Step 14 workflow) will run analysis -> validation -> error on validation failure

**Downstream Agent Requirements:**
- **rq_tools:** MUST specify validation tool for EVERY analysis step (no exceptions)
- **rq_analysis:** MUST embed validation tool call for EVERY analysis step (no exceptions)
- **g_code:** MUST generate code with validation function calls (no exceptions)
- **rq_inspect:** MUST verify validation ran successfully (checks logs/stepN_name.log for validation output)

### Validation Requirements By Step

#### Step 0: Extract Cognitive Test Data

**Analysis Tool:** (determined by rq_tools - likely tools.data.extract_cognitive_tests)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_data_extraction)

**What Validation Checks:**
- Output file exists (data/step00_cognitive_tests.csv)
- Expected column count (10 columns: UID + raw scores + T-scores)
- Expected row count (~100 participants)
- T-score standardization correct (M H 50, SD H 10)
- No unexpected NaN patterns (complete standardization)
- UID format consistency (participant identifiers valid)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "T-scores not standardized: M=45.2, SD=12.3")
- Log failure to logs/step00_extract_cognitive_tests.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked by master to diagnose root cause

---

#### Step 1: Load REMEMVR Theta Scores

**Analysis Tool:** (determined by rq_tools - likely tools.data.load_and_aggregate_theta)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_theta_aggregation)

**What Validation Checks:**
- Output file exists (data/step01_theta_mean.csv)
- Theta aggregation successful (4 sessions -> 1 mean per UID)
- Expected participant count (100 UIDs)
- Theta values in valid range ([-3, 3])
- No missing data in aggregated theta_mean
- SE values reasonable (0.1 to 1.0 range)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Theta aggregation failed: only 3.2 mean sessions per UID")
- Log failure to logs/step01_load_theta_scores.log
- Quit script immediately
- g_debug invoked to diagnose (common causes: missing Ch5 data, aggregation error)

---

#### Step 2: Merge Cognitive Tests with Theta Scores

**Analysis Tool:** (determined by rq_tools - likely tools.data.merge_datasets)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_data_merge)

**What Validation Checks:**
- Merge successful (high match rate between cognitive and theta data)
- Final dataset completeness (minimal missing data after listwise deletion)
- All required columns present in analysis dataset
- No duplicate UIDs in final dataset
- Data ranges preserved from individual sources

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Merge failed: only 75% match rate")
- Log failure to logs/step02_merge_datasets.log
- Quit script immediately
- g_debug invoked to diagnose merge issues

---

#### Step 3: Check Regression Assumptions

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_regression.check_assumptions)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_assumption_checks)

**What Validation Checks:**
- All assumption tests completed (normality, homoscedasticity, VIF, outliers)
- Diagnostic statistics in valid ranges
- VIF calculations successful (all VIF > 1.0)
- Outlier detection completed (Cook's D computed)
- Remedial action documentation present

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "VIF calculation failed: singular correlation matrix")
- Log failure to logs/step03_check_assumptions.log
- Quit script immediately
- g_debug invoked to diagnose assumption checking issues

---

#### Step 4: Fit Multiple Linear Regression Model

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_regression.fit_multiple_regression)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_regression_results)

**What Validation Checks:**
- Model convergence achieved (no singular matrix errors)
- All coefficients estimated (no NaN values)
- Standard errors computed (all SE > 0)
- R-squared in valid range (0 to 1)
- Bootstrap confidence intervals computed successfully
- Effect sizes calculated correctly

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Regression failed: predictor NART has NaN coefficient")
- Log failure to logs/step04_fit_regression.log
- Quit script immediately
- g_debug invoked to diagnose regression failures

---

#### Step 5: Apply Multiple Comparison Corrections

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_regression.apply_corrections)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_correction_d068)

**What Validation Checks (Decision D068 compliance):**
- Dual p-values present (uncorrected + Bonferroni)
- Bonferroni correction formula applied correctly (p_corrected = p_uncorrected * 4)
- Chapter 7 alpha threshold applied (0.00179)
- Boolean significance flags correctly assigned
- All predictors have dual p-value reporting

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "D068 violation: missing Bonferroni p-values")
- Log failure to logs/step05_apply_corrections.log
- Quit script immediately
- g_debug invoked to diagnose correction issues

---

#### Step 6: Compute Predictor Importance and Rankings

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_regression.compute_importance)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_importance_analysis)

**What Validation Checks:**
- All predictors ranked (1-4 ranking with no ties)
- Semi-partial correlations sum <= total R²
- Dominance analysis completed successfully
- Test type assignments correct (Episodic vs Intelligence)
- Hypothesis test conducted (RAVLT vs RPM comparison)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Ranking error: multiple predictors tied at rank 2")
- Log failure to logs/step06_compute_importance.log
- Quit script immediately
- g_debug invoked to diagnose importance calculation issues

---

#### Step 7: Sensitivity Analysis

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_regression.sensitivity_analysis)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_model_comparison)

**What Validation Checks:**
- Both models fitted successfully (Full and Reduced)
- Cross-validation completed (5 folds for both models)
- F-test for incremental validity computed
- Shrinkage values reasonable (< 0.20)
- AIC values computed correctly

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Cross-validation failed: fold 3 singular matrix")
- Log failure to logs/step07_sensitivity_analysis.log
- Quit script immediately
- g_debug invoked to diagnose model comparison issues

---

#### Step 8: Generate Summary Results

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_regression.generate_summary)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_results_compilation)

**What Validation Checks:**
- All prior steps integrated successfully
- Summary file generated (minimum content requirements)
- No transcription errors (values match source files)
- APA formatting applied correctly
- Success criteria evaluation included

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Summary incomplete: missing cross-validation results")
- Log failure to logs/step08_generate_summary.log
- Quit script immediately
- g_debug invoked to diagnose summary generation issues

---

## Summary

**Total Steps:** 8
**Estimated Runtime:** 15-30 minutes (mostly low-complexity steps)
**Cross-RQ Dependencies:** Ch5 RQ 5.1.1 (theta scores as dependent variable)
**Primary Outputs:** Regression coefficients, predictor importance rankings, cross-validated model performance
**Validation Coverage:** 100% (all 8 steps have validation requirements)

**Success Criteria Evaluation:**
- [ ] Model explains significant variance (p < 0.00179)
- [ ] R² between 0.25 and 0.50 (convergent but not redundant)
- [ ] At least one episodic test (RAVLT or BVMT) significant after Bonferroni correction
- [ ] Residual > 50% (substantial unique REMEMVR variance)
- [ ] All VIF values < 5.0 (no severe multicollinearity)
- [ ] Model diagnostics pass (normality, homoscedasticity within acceptable limits)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 10 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Notes:**

**Naming Conventions:** Standard naming patterns from names.md (step##_description format, UID for participants, theta_mean for aggregated ability, T-score suffix for standardized tests)

**Validation Philosophy:** Per-step validation ensures errors caught at source, not 5 steps later. Regression diagnostics are especially critical given assumption-sensitive nature of multiple linear regression.

**Tool Selection:** rq_tools agent reads this plan and specifies exact tools from tool_inventory.md. This plan provides method specifications (multiple linear regression, Bonferroni correction, cross-validation) without prescribing specific function names.

**Code Generation:** g_code agent generates Python scripts per rq_analysis instructions based on this plan. Expected heavy use of tools.analysis_regression module for multiple regression pipeline.

**Chapter 7 Context:** This RQ provides foundational convergent validity evidence for REMEMVR. Results inform subsequent Ch7 analyses examining age effects, domain-specific prediction, and clinical utility applications.

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent for Ch7 RQ 7.1.1