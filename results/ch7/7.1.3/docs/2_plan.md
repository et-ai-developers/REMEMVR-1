# Analysis Plan: RQ 7.1.3: Domain-Specific Prediction Patterns

**Research Question:** 7.1.3
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This analysis examines domain-specific prediction patterns by testing whether verbal tests (RAVLT) preferentially predict What memory, visuospatial tests (BVMT) predict Where memory, and neither predicts When memory. The analysis uses IRT-derived theta scores from Chapter 5 domain analyses and cognitive test scores to fit three domain-specific multiple linear regression models.

The analysis pipeline consists of 6 steps: domain theta extraction, three regression model fits (What/Where/When), cross-domain beta comparisons, and beta coefficient heatmap visualization. The primary hypothesis is that RAVLT beta coefficient for What domain should exceed RAVLT beta for Where domain, while BVMT beta for Where should exceed BVMT beta for What, demonstrating domain-specific prediction patterns.

**Pipeline:** Multiple Linear Regression with Steiger Z-tests for beta coefficient comparisons
**Steps:** 6 total analysis steps
**Estimated Runtime:** Medium (20-30 minutes total)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni corrected) for multiple comparisons
- Cross-RQ dependency: Requires completion of Ch5 domain analyses (5.2.1, 5.2.2, 5.2.3)

---

## Analysis Plan

### Step 0: Extract Domain Theta Scores

**Dependencies:** None (first step, depends on Ch5 RQ completion)
**Complexity:** Low (data extraction and aggregation)

**Input:**

**Files Required from Ch5 Domain Analyses:**
- results/ch5/5.2.1/data/step03_theta_scores.csv (What domain theta estimates)
- results/ch5/5.2.2/data/step03_theta_scores.csv (Where domain theta estimates) 
- results/ch5/5.2.3/data/step03_theta_scores.csv (When domain theta estimates)
- data/cache/master.xlsx (Sheet: CognitiveTests) (RAVLT_T, BVMT_T, RPM_T scores)

**Expected Input Format:**
- Each theta CSV: composite_ID (UID_test), theta (float), se_theta (float)
- Expected rows per domain: ~400 (100 participants x 4 tests)
- Cognitive tests sheet: UID (participant ID), RAVLT_T (total), BVMT_T (total), RPM_T (total)

**Processing:**
- Load theta scores from all three domain RQs
- Aggregate theta by UID (mean across 4 tests per participant)
- Merge with cognitive test scores on UID
- Create final dataset with columns: UID, Theta_What, Theta_Where, Theta_When, RAVLT_T, BVMT_T, RPM_T

**Output:**
- data/step00_domain_theta_scores.csv
- Format: One row per participant (UID), 7 columns (UID + 3 theta + 3 cognitive test scores)
- Expected rows: 100 participants
- Column types: UID (object), theta columns (float64), cognitive test columns (float64)

**Validation Requirement:**
Validation tools MUST be used after data extraction tool execution. Specific validation tools will be determined by rq_tools based on data extraction and merging requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_domain_theta_scores.csv: 100 rows x 7 columns
- Column types: UID (object), Theta_What/Where/When (float64), RAVLT_T/BVMT_T/RPM_T (float64)

*Value Ranges:*
- Theta values in [-3, 3] (standard IRT ability range)
- RAVLT_T in [0, 75] (sum of 5 trials, max 15 words per trial)
- BVMT_T in [0, 36] (sum of 3 trials, max 12 figures per trial)
- RPM_T in [0, 60] (total correct out of 60 matrices)

*Data Quality:*
- All 100 participants present (no missing UIDs)
- No NaN values in any column (complete cognitive data requirement)
- No duplicate UIDs (unique participants only)
- Theta values approximately normal distribution (ability estimates)

*Log Validation:*
- Required: "Domain theta merge complete: 100 participants"
- Required: "Cognitive tests merged: RAVLT, BVMT, RPM"
- Forbidden: "ERROR", "Missing theta scores", "Cognitive test data incomplete"
- Acceptable warnings: None expected for complete dataset

**Expected Behavior:**
Load and aggregate domain-specific theta scores from Ch5 outputs, merge with cognitive test predictors, create analysis-ready dataset for regression modeling.

---

### Step 1: Fit What Domain Regression Model

**Dependencies:** Step 0 (requires domain theta scores dataset)
**Complexity:** Low (standard multiple regression)

**Input:**
- data/step00_domain_theta_scores.csv
- Required columns: UID, Theta_What, RAVLT_T, BVMT_T, RPM_T

**Processing:**
- Fit multiple linear regression: Theta_What ~ RAVLT_T + BVMT_T + RPM_T
- Extract model summary (coefficients, standard errors, t-statistics, p-values)
- Compute model fit statistics (R-squared, adjusted R-squared, F-statistic)
- Generate residual diagnostics (normality tests, homoscedasticity)

**Output:**
- data/step01_what_model_results.csv
- Format: Model results with columns: term, estimate, std_error, t_value, p_value
- Expected rows: 4 (intercept + 3 predictors: RAVLT_T, BVMT_T, RPM_T)
- Additional file: data/step01_what_model_fit.csv (R2, adj_R2, F_stat, F_p_value)

**Validation Requirement:**
Validation tools MUST be used after regression tool execution. Specific validation tools will be determined by rq_tools based on multiple regression analysis requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_what_model_results.csv: 4 rows x 5 columns (term, estimate, std_error, t_value, p_value)
- data/step01_what_model_fit.csv: 1 row x 4 columns (R2, adj_R2, F_stat, F_p_value)

*Value Ranges:*
- estimate: unrestricted (can be positive or negative)
- std_error: > 0 (standard errors must be positive)
- t_value: unrestricted (test statistics)
- p_value in [0, 1] (probability values)
- R2, adj_R2 in [0, 1] (proportion variance explained)

*Data Quality:*
- All 4 predictors present (intercept + RAVLT_T + BVMT_T + RPM_T)
- No NaN values in estimates or standard errors (model convergence)
- Standard errors > 0 (valid estimation)
- Model fit statistics computed (R2, F-test)

*Log Validation:*
- Required: "What domain model converged successfully"
- Required: "Model fit: R2 = X.XXX, p < 0.XXX"
- Forbidden: "ERROR", "Singular matrix", "Convergence failed"
- Acceptable warnings: "Residual normality borderline" (common with N=100)

**Expected Behavior:**
Fit regression predicting What domain theta from three cognitive tests, extract parameter estimates and fit statistics for cross-domain comparison.

---

### Step 2: Fit Where Domain Regression Model

**Dependencies:** Step 0 (requires domain theta scores dataset)
**Complexity:** Low (standard multiple regression)

**Input:**
- data/step00_domain_theta_scores.csv
- Required columns: UID, Theta_Where, RAVLT_T, BVMT_T, RPM_T

**Processing:**
- Fit multiple linear regression: Theta_Where ~ RAVLT_T + BVMT_T + RPM_T
- Extract model summary (coefficients, standard errors, t-statistics, p-values)
- Compute model fit statistics (R-squared, adjusted R-squared, F-statistic)
- Generate residual diagnostics (normality tests, homoscedasticity)

**Output:**
- data/step02_where_model_results.csv
- Format: Model results with columns: term, estimate, std_error, t_value, p_value
- Expected rows: 4 (intercept + 3 predictors: RAVLT_T, BVMT_T, RPM_T)
- Additional file: data/step02_where_model_fit.csv (R2, adj_R2, F_stat, F_p_value)

**Validation Requirement:**
Validation tools MUST be used after regression tool execution. Specific validation tools will be determined by rq_tools based on multiple regression analysis requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_where_model_results.csv: 4 rows x 5 columns (term, estimate, std_error, t_value, p_value)
- data/step02_where_model_fit.csv: 1 row x 4 columns (R2, adj_R2, F_stat, F_p_value)

*Value Ranges:*
- estimate: unrestricted (can be positive or negative)
- std_error: > 0 (standard errors must be positive)
- t_value: unrestricted (test statistics)
- p_value in [0, 1] (probability values)
- R2, adj_R2 in [0, 1] (proportion variance explained)

*Data Quality:*
- All 4 predictors present (intercept + RAVLT_T + BVMT_T + RPM_T)
- No NaN values in estimates or standard errors (model convergence)
- Standard errors > 0 (valid estimation)
- Model fit statistics computed (R2, F-test)

*Log Validation:*
- Required: "Where domain model converged successfully"
- Required: "Model fit: R2 = X.XXX, p < 0.XXX"
- Forbidden: "ERROR", "Singular matrix", "Convergence failed"
- Acceptable warnings: "Residual normality borderline" (common with N=100)

**Expected Behavior:**
Fit regression predicting Where domain theta from three cognitive tests, extract parameter estimates and fit statistics for cross-domain comparison.

---

### Step 3: Fit When Domain Regression Model

**Dependencies:** Step 0 (requires domain theta scores dataset)
**Complexity:** Low (standard multiple regression)

**Input:**
- data/step00_domain_theta_scores.csv
- Required columns: UID, Theta_When, RAVLT_T, BVMT_T, RPM_T

**Processing:**
- Fit multiple linear regression: Theta_When ~ RAVLT_T + BVMT_T + RPM_T
- Extract model summary (coefficients, standard errors, t-statistics, p-values)
- Compute model fit statistics (R-squared, adjusted R-squared, F-statistic)
- Generate residual diagnostics (normality tests, homoscedasticity)

**Output:**
- data/step03_when_model_results.csv
- Format: Model results with columns: term, estimate, std_error, t_value, p_value
- Expected rows: 4 (intercept + 3 predictors: RAVLT_T, BVMT_T, RPM_T)
- Additional file: data/step03_when_model_fit.csv (R2, adj_R2, F_stat, F_p_value)

**Validation Requirement:**
Validation tools MUST be used after regression tool execution. Specific validation tools will be determined by rq_tools based on multiple regression analysis requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_when_model_results.csv: 4 rows x 5 columns (term, estimate, std_error, t_value, p_value)
- data/step03_when_model_fit.csv: 1 row x 4 columns (R2, adj_R2, F_stat, F_p_value)

*Value Ranges:*
- estimate: unrestricted (can be positive or negative)
- std_error: > 0 (standard errors must be positive)
- t_value: unrestricted (test statistics)  
- p_value in [0, 1] (probability values)
- R2, adj_R2 in [0, 1] (proportion variance explained)

*Data Quality:*
- All 4 predictors present (intercept + RAVLT_T + BVMT_T + RPM_T)
- No NaN values in estimates or standard errors (model convergence)
- Standard errors > 0 (valid estimation)
- Model fit statistics computed (R2, F-test)

*Log Validation:*
- Required: "When domain model converged successfully"
- Required: "Model fit: R2 = X.XXX, p < 0.XXX"
- Forbidden: "ERROR", "Singular matrix", "Convergence failed"
- Acceptable warnings: "Residual normality borderline" (common with N=100)

**Expected Behavior:**
Fit regression predicting When domain theta from three cognitive tests, extract parameter estimates and fit statistics for cross-domain comparison.

---

### Step 4: Cross-Domain Beta Coefficient Comparisons

**Dependencies:** Steps 1, 2, 3 (requires all three domain model results)
**Complexity:** Medium (Steiger Z-tests for dependent correlations)

**Input:**
- data/step01_what_model_results.csv
- data/step02_where_model_results.csv  
- data/step03_when_model_results.csv
- data/step00_domain_theta_scores.csv (raw data for correlation matrix)

**Processing:**
- Extract beta coefficients for RAVLT_T and BVMT_T from each domain model
- Compute correlation matrix between predictors (RAVLT_T, BVMT_T, RPM_T) and outcomes (Theta_What, Theta_Where, Theta_When)
- Perform Steiger Z-tests for dependent correlations:
  - Test H1: beta_RAVLT_What > beta_RAVLT_Where (verbal test predicts verbal domain better)
  - Test H2: beta_BVMT_Where > beta_BVMT_What (spatial test predicts spatial domain better)
- Apply Bonferroni correction for multiple comparisons (Decision D068)
- Extract R-squared values and compute bootstrap 95% confidence intervals

**Output:**
- data/step04_beta_comparison_matrix.csv
- Format: Beta coefficients matrix (rows=domains, cols=cognitive tests)
- Expected dimensions: 3 domains x 3 cognitive tests = 9 beta values
- Additional file: data/step04_steiger_z_tests.csv (comparison, z_stat, p_uncorrected, p_bonferroni)

**Validation Requirement:**
Validation tools MUST be used after statistical comparison tool execution. Specific validation tools will be determined by rq_tools based on Steiger Z-test and multiple comparison requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_beta_comparison_matrix.csv: 3 rows x 4 columns (domain + 3 cognitive test betas)
- data/step04_steiger_z_tests.csv: 2 rows x 4 columns (comparison, z_stat, p_uncorrected, p_bonferroni)

*Value Ranges:*
- beta coefficients: unrestricted (can be positive/negative)
- z_stat: unrestricted (Steiger Z-statistics)
- p_uncorrected in [0, 1] (uncorrected p-values)
- p_bonferroni in [0, 1] (Bonferroni-corrected p-values, should be >= uncorrected)

*Data Quality:*
- All 3 domains present (What, Where, When)
- All 3 cognitive tests present (RAVLT_T, BVMT_T, RPM_T)
- Exactly 2 Steiger Z-tests performed (primary hypotheses)
- Both uncorrected AND Bonferroni p-values provided (Decision D068)

*Log Validation:*
- Required: "Cross-domain comparisons complete: 2 tests performed"
- Required: "Decision D068: Dual p-values reported"
- Forbidden: "ERROR", "Correlation matrix singular", "Z-test failed"
- Acceptable warnings: "Large standard errors" (small effect sizes expected)

**Expected Behavior:**
Compare beta coefficients across domains using Steiger Z-tests to test domain-specificity hypotheses with dual p-value reporting.

---

### Step 5: Prepare Beta Coefficient Heatmap Data

**Dependencies:** Step 4 (requires beta comparison matrix)
**Complexity:** Low (data preparation for visualization)

**Purpose:** Aggregate model outputs for beta coefficient heatmap visualization (Option B: data preparation creates plot source CSV)

**Plot Description:** Heatmap showing beta coefficients with rows=domains (What/Where/When), columns=cognitive tests (RAVLT/BVMT/RPM), color intensity representing coefficient magnitude

**Required Data Sources:**
- data/step04_beta_comparison_matrix.csv (beta coefficients per domain x test)
- data/step04_steiger_z_tests.csv (significance markers for hypothesis tests)

**Processing:**
- Reshape beta coefficient matrix for heatmap format
- Add significance indicators for tested comparisons (RAVLT_What vs RAVLT_Where, BVMT_Where vs BVMT_What)
- Scale coefficients for color mapping (standardize or normalize if needed)
- Format data with required columns for plotting

**Output:**
- data/step05_heatmap_data.csv
- Format: Long format with columns: domain, cognitive_test, beta_coefficient, significance
- Expected rows: 9 (3 domains x 3 cognitive tests)
- Column types: domain (object), cognitive_test (object), beta_coefficient (float64), significance (object)

**Validation Requirement:**
Validation tools MUST be used after plot data preparation tool execution. Specific validation tools will be determined by rq_tools based on plot data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_heatmap_data.csv exists (exact path)
- Expected rows: 9 (3 domains x 3 cognitive tests)  
- Expected columns: 4 (domain, cognitive_test, beta_coefficient, significance)
- Data types: domain (object), cognitive_test (object), beta_coefficient (float64), significance (object)

*Value Ranges:*
- beta_coefficient: unrestricted (standardized coefficients)
- domain in {What, Where, When} (categorical)
- cognitive_test in {RAVLT_T, BVMT_T, RPM_T} (categorical)
- significance in {ns, *, **} (significance markers)

*Data Quality:*
- No NaN values tolerated (all cells must have valid values)
- Expected N: Exactly 9 rows (complete factorial design)
- No duplicate domain x cognitive_test combinations
- All domains and tests represented

*Log Validation:*
- Required: "Heatmap data preparation complete: 9 coefficients"
- Required: "All domains represented: What, Where, When"
- Forbidden: "ERROR", "Missing coefficients", "Incomplete data"
- Acceptable warnings: None expected for heatmap data

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 9 rows, found 6")
- Log failure to logs/step05_prepare_heatmap_data.log
- Quit script immediately (do NOT proceed to visualization)

**Plotting Function (rq_plots will call):** Beta coefficient heatmap
- rq_plots agent maps this description to specific tools/plots.py function
- Plot reads data/step05_heatmap_data.csv (created by this step)
- PNG output saved to plots/ folder by rq_plots

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs - intermediate and final)
- data/step00_domain_theta_scores.csv (aggregated theta scores + cognitive tests)
- data/step01_what_model_results.csv (What domain regression coefficients)
- data/step01_what_model_fit.csv (What domain R-squared, F-statistic)
- data/step02_where_model_results.csv (Where domain regression coefficients) 
- data/step02_where_model_fit.csv (Where domain R-squared, F-statistic)
- data/step03_when_model_results.csv (When domain regression coefficients)
- data/step03_when_model_fit.csv (When domain R-squared, F-statistic)
- data/step04_beta_comparison_matrix.csv (cross-domain beta coefficients)
- data/step04_steiger_z_tests.csv (cross-domain statistical comparisons)
- data/step05_heatmap_data.csv (plot source data for beta coefficient heatmap)

### Logs (ONLY execution logs - .log files capturing stdout/stderr)
- logs/step00_extract_domain_theta_scores.log
- logs/step01_fit_what_model.log
- logs/step02_fit_where_model.log
- logs/step03_fit_when_model.log
- logs/step04_cross_domain_comparisons.log
- logs/step05_prepare_heatmap_data.log

### Plots (EMPTY until rq_plots runs)
- plots/domain_prediction_heatmap.png (created by rq_plots, NOT analysis steps)

### Results (EMPTY until rq_results runs)
- results/summary.md (created by rq_results, NOT analysis steps)

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 - Domain Theta Aggregation:**
- Input Format: Three separate theta CSV files (one per domain), cognitive tests sheet
- Transformation: Aggregate theta by UID (mean across 4 tests), merge with cognitive scores
- Output Format: One row per participant (UID), 7 columns (identifiers + predictors + outcomes)

**Steps 1-3 - Regression Model Fitting:**
- Input Format: Wide format (UID x variables)
- Transformation: Fit separate multiple regression per domain
- Output Format: Model coefficients + fit statistics (separate files per domain)

**Step 4 - Cross-Domain Comparisons:**
- Input Format: Three separate model results files
- Transformation: Extract coefficients, perform Steiger Z-tests, apply Bonferroni correction
- Output Format: Beta matrix + statistical test results (Decision D068 dual p-values)

**Step 5 - Plot Data Preparation:**
- Input Format: Beta matrix (wide format)
- Transformation: Reshape to long format, add significance markers
- Output Format: Plot-ready data (domain x cognitive_test x beta_coefficient)

### Column Naming Conventions

**Following names.md patterns:**
- UID: participant identifier (object)
- Theta_What/Where/When: domain-specific ability estimates (float64)
- RAVLT_T/BVMT_T/RPM_T: cognitive test total scores (float64)
- term: regression coefficient name (object)
- estimate: regression coefficient value (float64)
- std_error: standard error of coefficient (float64)
- p_value: significance test p-value (float64)

### Data Type Constraints

**Non-nullable columns:** UID, all theta scores, all cognitive test scores
**Nullable allowed:** None (complete data requirement for regression)
**Valid ranges:** Theta in [-3, 3], cognitive tests per instrument norms
**Categorical values:** domain in {What, Where, When}, cognitive_test in {RAVLT_T, BVMT_T, RPM_T}

---

## Cross-RQ Dependencies

### Dependency Type 2: DERIVED Data from Other RQs (Dependencies Exist)

**This RQ requires outputs from:**
- **RQ 5.2.1** (What Domain Analysis)
  - File: results/ch5/5.2.1/data/step03_theta_scores.csv
  - Used in: Step 0 (What domain theta scores for regression outcome)
  - Rationale: RQ 5.2.1 provides IRT-calibrated theta estimates for What domain memory

- **RQ 5.2.2** (Where Domain Analysis)  
  - File: results/ch5/5.2.2/data/step03_theta_scores.csv
  - Used in: Step 0 (Where domain theta scores for regression outcome)
  - Rationale: RQ 5.2.2 provides IRT-calibrated theta estimates for Where domain memory

- **RQ 5.2.3** (When Domain Analysis)
  - File: results/ch5/5.2.3/data/step03_theta_scores.csv  
  - Used in: Step 0 (When domain theta scores for regression outcome)
  - Rationale: RQ 5.2.3 provides IRT-calibrated theta estimates for When domain memory

**Execution Order Constraint:**
1. RQ 5.2.1, 5.2.2, 5.2.3 must complete first (provide domain-specific theta scores)
2. This RQ executes after Ch5 domain analyses complete (uses theta as regression outcomes)

**Data Source Boundaries:**
- **RAW data:** master.xlsx cognitive test scores extracted directly (no RQ dependencies)
- **DERIVED data:** Domain theta scores from Ch5 analyses (cross-chapter dependency)
- **Scope:** This RQ does NOT re-estimate theta (uses Ch5 outputs as fixed predictors)

**Validation:**
- Step 0: Check results/ch5/5.2.1/data/step03_theta_scores.csv exists (circuit breaker: FILE_MISSING if absent)
- Step 0: Check results/ch5/5.2.2/data/step03_theta_scores.csv exists (circuit breaker: FILE_MISSING if absent) 
- Step 0: Check results/ch5/5.2.3/data/step03_theta_scores.csv exists (circuit breaker: FILE_MISSING if absent)
- If any file missing -> quit with error -> user must execute Ch5 domain RQs first

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

#### Step 0: Extract Domain Theta Scores

**Analysis Tool:** (determined by rq_tools - likely tools.data extraction + aggregation functions)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_data_format + validate_numeric_range)

**What Validation Checks:**
- Output file exists (data/step00_domain_theta_scores.csv)
- Expected column count (7 columns: UID + 3 theta + 3 cognitive tests)
- Expected row count (100 participants)
- No missing values (complete data requirement)
- Theta values in valid ranges ([-3, 3])
- Cognitive test scores in instrument ranges

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Missing cognitive test data for 5 participants")
- Log failure to logs/step00_extract_domain_theta_scores.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked by master to diagnose root cause

#### Step 1-3: Domain Regression Models

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_stats.fit_linear_regression)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_lmm_convergence + validate_numeric_range)

**What Validation Checks:**
- Model convergence successful (no singular matrix errors)
- Output files exist (model_results.csv, model_fit.csv)
- Expected parameters (intercept + 3 predictors)
- Standard errors > 0 (valid estimation)  
- P-values in [0, 1]
- R-squared in [0, 1]

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Where domain model failed to converge")
- Log failure to logs/stepN_fit_domain_model.log
- Quit script immediately 
- g_debug invoked to diagnose (common causes: multicollinearity, insufficient variation)

#### Step 4: Cross-Domain Beta Comparisons

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_ctt.compare_correlations_dependent)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_contrasts_dual_pvalues)

**What Validation Checks:**
- Steiger Z-tests computed successfully
- Both uncorrected AND Bonferroni p-values present (Decision D068)
- Z-statistics are finite (not NaN/inf)
- Correlation matrix positive definite (required for Steiger test)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Correlation matrix singular for Steiger test")
- Log failure to logs/step04_cross_domain_comparisons.log
- Quit script immediately
- g_debug invoked to diagnose root cause

#### Step 5: Prepare Heatmap Data

**Analysis Tool:** (determined by rq_tools - likely pandas reshape + aggregation functions)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_plot_data_completeness)

**What Validation Checks:**
- Output file exists (data/step05_heatmap_data.csv)
- Complete factorial design (3 domains x 3 tests = 9 rows)
- Required columns present (domain, cognitive_test, beta_coefficient, significance)
- No missing values in data
- Domain and cognitive test categories complete

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Missing beta coefficient for BVMT_T x When")
- Log failure to logs/step05_prepare_heatmap_data.log
- Quit script immediately
- g_debug invoked to diagnose data aggregation issues

---

## Summary

**Total Steps:** 6 (Step 0: extraction + Steps 1-5: analysis/preparation)
**Estimated Runtime:** Medium (20-30 minutes total)
**Cross-RQ Dependencies:** Ch5 5.2.1, 5.2.2, 5.2.3 (domain theta scores required)
**Primary Outputs:** Domain regression models, cross-domain beta comparisons, heatmap visualization data  
**Validation Coverage:** 100% (all 6 steps have validation requirements)

**Key Hypotheses Testing:**
- RAVLT_beta_What > RAVLT_beta_Where (verbal test predicts verbal domain better)
- BVMT_beta_Where > BVMT_beta_What (spatial test predicts spatial domain better)
- R²_When < R²_What and R²_When < R²_Where (temporal domain less predictable)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)  
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent