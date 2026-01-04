# Analysis Plan: RQ 7.1.3 - Domain-Specific Prediction Patterns

**Research Question:** 7.1.3
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ tests domain-specific prediction patterns using multiple linear regression with cross-domain beta coefficient comparisons. Tests whether verbal tests (RAVLT) preferentially predict What memory, visuospatial tests (BVMT) predict Where memory, and neither predicts When memory, consistent with Baddeley's working memory model.

**Pipeline:** Multiple Linear Regression with Steiger Z-tests for cross-domain comparisons
**Steps:** 6 total analysis steps (Step 0: validation + Steps 1-5: analysis)
**Estimated Runtime:** 45-60 minutes

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Chapter 7 Bonferroni correction: alpha = 0.05/28 = 0.00179 for chapter-level
- Within-RQ Bonferroni: alpha = 0.05/6 = 0.0083 for 6 key tests (3 domains x 2 main comparisons)

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies

**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 domain-specific outputs exist before proceeding

**Input:**
- Primary: results/ch5/5.2.1/data/step03_theta_what.csv (What domain theta scores)
- Primary: results/ch5/5.2.2/data/step03_theta_where.csv (Where domain theta scores)
- Primary: results/ch5/5.2.3/data/step03_theta_when.csv (When domain theta scores)
- Alternative: results/ch5/5.2.{1,2,3}/data/*theta*.csv (flexible naming patterns)
- Fallback: results/ch5/5.2.{1,2,3}/data/step*_theta_*.csv (step-prefixed patterns)
- Local: data/cache/master.xlsx (cognitive test T-scores)
- Expected content: Theta scores per composite_ID with domain labeling

**Processing:**
- Check Ch5 5.2.x completion status in their respective status.yaml files
- Verify theta files exist and contain expected columns (composite_ID, theta, SE, domain)
- Test read access to master.xlsx for cognitive test scores (RAVLT_T, BVMT_T, RPM_T)
- Verify N=100 participants with complete data across all sources
- Log validation results with specific file paths found

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with dependency status
- File content: 3 domain theta files confirmed, master.xlsx accessible

*Value Ranges:*
- Participant count: 100 participants expected across all files
- Domain files: 3 files minimum (What, Where, When)
- Required columns: composite_ID, theta, domain verified

*Data Quality:*
- All 3 domain files accessible
- Master.xlsx contains RAVLT_T, BVMT_T, RPM_T columns
- No file access errors logged

*Log Validation:*
- Required: "Ch5 dependencies verified: 3 domain files found"
- Required: "Master.xlsx cognitive tests accessible"
- Forbidden: "ERROR", "file not found", "access denied"

**Expected Behavior on Validation Failure:**
Quit immediately with specific missing dependency error message.

---

### Step 1: Extract and Prepare Domain-Specific Data

**Dependencies:** Step 0 (dependencies validated)
**Complexity:** Low (<10 minutes)

**Purpose:** Extract domain-specific theta scores from Ch5 outputs and merge with cognitive test data

**Input:**
- results/ch5/5.2.1/data/step03_theta_what.csv (What domain)
- results/ch5/5.2.2/data/step03_theta_where.csv (Where domain)
- results/ch5/5.2.3/data/step03_theta_when.csv (When domain)
- data/cache/master.xlsx (cognitive test T-scores: RAVLT_T, BVMT_T, RPM_T)

**Processing:**
- Read domain-specific theta files from Ch5 5.2.x results
- Aggregate theta scores by UID per domain (mean across items within domain)
- Extract cognitive test T-scores from dfnonvr.csv for N=100 participants
- Merge datasets on UID to create complete analysis dataset
- Verify complete data: all participants have theta scores for all 3 domains
- Calculate descriptive statistics by domain
- Check for outliers using IQR method (Q1 - 1.5*IQR, Q3 + 1.5*IQR)
- Log data preparation steps and missing data patterns

**Output:**
- data/step01_domain_theta_scores.csv (theta scores by UID and domain)
- data/step01_merged_dataset.csv (complete analysis dataset)
- data/step01_descriptive_stats.csv (descriptive statistics by domain)

**Validation Requirement:**
Validation tools MUST be used after data extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_domain_theta_scores.csv: 300 rows x 4 columns (100 UIDs x 3 domains)
- Columns: UID (object), domain (object), theta_mean (float64), theta_se (float64)
- data/step01_merged_dataset.csv: 300 rows x 7 columns (domain data + cognitive tests)
- data/step01_descriptive_stats.csv: 3 rows x 8 columns (summary stats per domain)

*Value Ranges:*
- theta_mean in [-4, 4] (IRT ability scale, 99% of values)
- theta_se in [0.1, 2.0] (standard errors positive, reasonable bounds)
- RAVLT_T, BVMT_T, RPM_T in [20, 80] (T-score range)
- domain: exactly "What", "Where", "When" (3 levels)

*Data Quality:*
- All 100 UIDs present across all 3 domains (300 total rows)
- No missing values in theta_mean, domain, or UID columns
- Missing cognitive test data < 5% (max 5 participants missing any test)
- No duplicate UID-domain combinations

*Log Validation:*
- Required: "Data extraction complete: 100 participants x 3 domains"
- Required: "Merge successful: complete data for N participants"
- Forbidden: "ERROR", "merge failed", "missing domains"

**Expected Behavior on Validation Failure:**
Log error details and quit with data preparation failure message.

---

### Step 2: Fit Domain-Specific Regression Models

**Dependencies:** Step 1 (merged dataset)
**Complexity:** Medium (~15 minutes including diagnostics)

**Purpose:** Fit separate multiple regression models for each memory domain to test domain-specific prediction patterns

**Input:**
- data/step01_merged_dataset.csv (complete analysis dataset)

**Processing:**
- Fit three domain-specific regression models using statsmodels.api.OLS:
  - Model_What: theta_What ~ RAVLT_T + BVMT_T + RPM_T
  - Model_Where: theta_Where ~ RAVLT_T + BVMT_T + RPM_T  
  - Model_When: theta_When ~ RAVLT_T + BVMT_T + RPM_T
- Standardize all predictors (z-score) before fitting for comparable beta coefficients
- Extract model summary statistics: R², adjusted R², F-statistic, AIC, BIC
- Extract beta coefficients with standard errors and 95% confidence intervals
- Check regression assumptions for each model:
  - Normality: Shapiro-Wilk test + Q-Q plots (visual primary, test supplemental)
  - Homoscedasticity: Breusch-Pagan test + residual plots
  - Independence: ACF plots + Durbin-Watson statistic
  - Multicollinearity: VIF for each predictor (threshold VIF < 5.0)
  - Outliers: Cook's distance > 4/n (n=100, threshold = 0.04)
- Remedial actions if assumptions violated:
  - Normality p < 0.05: Use bootstrap CIs as primary inference (1000 iterations, seed=42)
  - Heteroscedasticity p < 0.05: Report HC3 robust standard errors
  - VIF > 5.0: Document multicollinearity, consider ridge regression if VIF > 10
  - Cook's D > 0.04: Report results with and without outliers
- Bootstrap 95% CIs for regression coefficients:
  - Iterations: 1000
  - Random seed: 42
  - Method: Participant-level resampling with replacement
  - CI: Percentile method (2.5th, 97.5th percentiles)

**Output:**
- data/step02_what_model_results.csv (What domain regression results)
- data/step02_where_model_results.csv (Where domain regression results)
- data/step02_when_model_results.csv (When domain regression results)
- data/step02_model_diagnostics.csv (assumption check results)
- data/step02_bootstrap_coefficients.csv (bootstrap CIs for all models)

**Validation Requirement:**
Validation tools MUST be used after regression modeling execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_what_model_results.csv: 4 rows x 8 columns (intercept + 3 predictors)
- Columns: predictor, beta, se, ci_lower, ci_upper, p_value, vif, cooks_d_max
- data/step02_where_model_results.csv: same structure as What model
- data/step02_when_model_results.csv: same structure as What/Where models
- data/step02_model_diagnostics.csv: 3 rows x 6 columns (1 per model)
- data/step02_bootstrap_coefficients.csv: 12 rows x 5 columns (4 coeff x 3 models)

*Value Ranges:*
- beta in [-2, 2] (standardized coefficients, reasonable range)
- se > 0 (positive standard errors)
- p_value in [0, 1] (valid probability range)
- vif in [1, 10] (multicollinearity check, VIF >= 1 always)
- R² in [0, 1] (coefficient of determination bounds)
- ci_lower < beta < ci_upper (valid confidence intervals)

*Data Quality:*
- All 3 models converged successfully
- All 12 coefficients present (4 per model: intercept + 3 predictors)
- No NaN or infinite values in any coefficient
- Bootstrap CIs non-degenerate (ci_lower != ci_upper)

*Log Validation:*
- Required: "Model fitting complete: 3 domains, all converged"
- Required: "Bootstrap complete: 1000 iterations"
- Required: "Assumption checks complete: normality, homoscedasticity, VIF"
- Forbidden: "ERROR", "convergence failed", "singular matrix"

**Expected Behavior on Validation Failure:**
Log specific model failure details and quit with regression modeling error.

---

### Step 3: Extract and Compare Beta Coefficients

**Dependencies:** Step 2 (regression models fitted)
**Complexity:** Medium (~10 minutes)

**Purpose:** Extract beta coefficients from all models and create comparison matrix for cross-domain analysis

**Input:**
- data/step02_what_model_results.csv (What domain results)
- data/step02_where_model_results.csv (Where domain results)
- data/step02_when_model_results.csv (When domain results)

**Processing:**
- Extract standardized beta coefficients for each predictor across all domains
- Create beta coefficient matrix (rows = domains, columns = predictors)
- Calculate effect sizes using Cohen's conventions:
  - Small effect: |beta| >= 0.1
  - Medium effect: |beta| >= 0.3
  - Large effect: |beta| >= 0.5
- Identify largest beta coefficient for each predictor across domains
- Compute cross-domain beta differences for key hypotheses:
  - RAVLT_beta_What - RAVLT_beta_Where (expect positive)
  - BVMT_beta_Where - BVMT_beta_What (expect positive)
  - RPM_beta_consistency across domains (expect similar magnitudes)
- Create visualization data for heatmap (beta coefficients with significance)
- Prepare data for statistical tests of beta differences

**Output:**
- data/step03_beta_coefficient_matrix.csv (matrix format for analysis)
- data/step03_cross_domain_comparisons.csv (key hypothesis tests data)
- data/step03_effect_sizes.csv (effect size classifications)
- data/step03_heatmap_plot_data.csv (visualization data)

**Validation Requirement:**
Validation tools MUST be used after beta coefficient extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_beta_coefficient_matrix.csv: 3 rows x 4 columns (3 domains x 4 coefficients)
- Columns: domain, RAVLT_beta, BVMT_beta, RPM_beta, intercept_beta
- data/step03_cross_domain_comparisons.csv: 3 rows x 4 columns (key comparisons)
- data/step03_effect_sizes.csv: 9 rows x 3 columns (3 predictors x 3 domains)
- data/step03_heatmap_plot_data.csv: 9 rows x 5 columns (visualization format)

*Value Ranges:*
- All beta coefficients in [-2, 2] (standardized, reasonable bounds)
- effect_size_magnitude in ["small", "medium", "large", "negligible"]
- cross_domain_differences in [-4, 4] (beta difference bounds)
- domain exactly ["What", "Where", "When"]

*Data Quality:*
- All 9 beta coefficients present (3 predictors x 3 domains)
- No missing values in coefficient matrix
- Effect size classifications complete for all coefficients
- Cross-domain differences computed for all key hypotheses

*Log Validation:*
- Required: "Beta extraction complete: 9 coefficients extracted"
- Required: "Effect sizes classified using Cohen's conventions"
- Required: "Cross-domain comparisons prepared"
- Forbidden: "ERROR", "missing coefficients", "NaN values"

**Expected Behavior on Validation Failure:**
Log specific extraction error and quit with beta coefficient processing failure.

---

### Step 4: Perform Steiger Z-Tests for Cross-Domain Comparisons

**Dependencies:** Step 3 (beta coefficient comparisons)
**Complexity:** Medium (~10 minutes including corrections)

**Purpose:** Test statistical significance of cross-domain beta coefficient differences using Steiger's Z-tests for dependent correlations

**Input:**
- data/step03_cross_domain_comparisons.csv (beta differences)
- data/step02_*_model_results.csv (model results for correlation matrix)
- data/step01_merged_dataset.csv (raw data for correlation calculations)

**Processing:**
- Compute correlation matrix among all variables (3 domains + 3 predictors)
- Perform Steiger's Z-tests for dependent correlations using tools.analysis_ctt.compare_correlations_dependent:
  - Test 1: RAVLT correlation with What vs RAVLT correlation with Where
  - Test 2: BVMT correlation with Where vs BVMT correlation with What
  - Test 3: RPM correlation consistency across all domains (omnibus test)
- Extract Z-statistics, p-values, and 95% confidence intervals for differences
- Apply multiple comparison corrections:
  - Within-RQ family: 3 primary tests
  - Bonferroni correction: alpha = 0.05/3 = 0.0167 per test
  - FDR correction: Benjamini-Hochberg procedure
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Bootstrap confidence intervals for correlation differences:
  - Iterations: 1000
  - Random seed: 42
  - Method: Participant-level resampling with replacement
  - CI: Percentile method for correlation differences
- Classify significance levels:
  - p < 0.001: "***" (highly significant)
  - p < 0.01: "**" (very significant)  
  - p < 0.05: "*" (significant)
  - p >= 0.05: "ns" (not significant)

**Output:**
- data/step04_steiger_z_tests.csv (statistical test results)
- data/step04_correlation_matrix.csv (full correlation matrix)
- data/step04_corrected_pvalues.csv (multiple comparison corrections)
- data/step04_bootstrap_correlation_diffs.csv (bootstrap CIs)

**Validation Requirement:**
Validation tools MUST be used after Steiger Z-test execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_steiger_z_tests.csv: 3 rows x 8 columns (3 primary tests)
- Columns: comparison, z_statistic, p_uncorrected, p_bonferroni, p_fdr, ci_lower, ci_upper, significance
- data/step04_correlation_matrix.csv: 6 rows x 6 columns (symmetric correlation matrix)
- data/step04_corrected_pvalues.csv: 3 rows x 4 columns (correction methods)
- data/step04_bootstrap_correlation_diffs.csv: 3 rows x 3 columns (bootstrap CIs)

*Value Ranges:*
- z_statistic in [-10, 10] (reasonable Z-test range)
- p_values in [0, 1] (valid probability range)
- correlation coefficients in [-1, 1] (correlation bounds)
- ci_lower < ci_upper (valid confidence intervals)
- significance in ["***", "**", "*", "ns"]

*Data Quality:*
- All 3 Steiger tests completed successfully
- Full 6x6 correlation matrix computed (no missing correlations)
- Both Bonferroni and FDR corrections applied
- Bootstrap CIs computed for all comparisons

*Log Validation:*
- Required: "Steiger Z-tests complete: 3 comparisons"
- Required: "Multiple comparison corrections applied"
- Required: "Bootstrap correlation differences computed"
- Forbidden: "ERROR", "test failed", "correlation computation failed"

**Expected Behavior on Validation Failure:**
Log specific test failure and quit with statistical comparison error.

---

### Step 5: Compare Model Performance Across Domains

**Dependencies:** Step 4 (statistical comparisons complete)
**Complexity:** Medium (~10 minutes)

**Purpose:** Compare R² values across domains to assess differential predictability and test hypothesis that When domain is least predictable

**Input:**
- data/step02_*_model_results.csv (R² values from all models)
- data/step01_merged_dataset.csv (raw data for bootstrap)

**Processing:**
- Extract R² and adjusted R² values from all three domain models
- Compare model performance:
  - What vs Where domain R²
  - What vs When domain R²  
  - Where vs When domain R²
- Bootstrap 95% confidence intervals for R² values:
  - Iterations: 1000
  - Random seed: 42
  - Method: Participant-level resampling with replacement
  - For each iteration: refit all 3 models, extract R² values
  - Compute R² differences and percentile CIs
- Test hypothesis that R²_When < R²_What and R²_When < R²_Where using:
  - Overlapping confidence intervals assessment
  - Bootstrap distribution of R² differences
  - One-sided tests for R² differences (When predicted to be lowest)
- Compute effect sizes for R² differences using Cohen's conventions:
  - Small R²: 0.01-0.09
  - Medium R²: 0.09-0.25  
  - Large R²: >= 0.25
- Calculate variance explained by each predictor (semi-partial R²)

**Output:**
- data/step05_model_comparison.csv (R² comparisons with CIs)
- data/step05_bootstrap_r_squared.csv (bootstrap R² distributions)
- data/step05_r_squared_differences.csv (pairwise R² comparisons)
- data/step05_predictor_contributions.csv (semi-partial R² by predictor)

**Validation Requirement:**
Validation tools MUST be used after model comparison execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_model_comparison.csv: 3 rows x 6 columns (model performance)
- Columns: domain, r_squared, adj_r_squared, r2_ci_lower, r2_ci_upper, effect_size
- data/step05_bootstrap_r_squared.csv: 1000 rows x 3 columns (bootstrap distributions)
- data/step05_r_squared_differences.csv: 3 rows x 5 columns (pairwise comparisons)
- data/step05_predictor_contributions.csv: 9 rows x 3 columns (semi-partial R²)

*Value Ranges:*
- r_squared in [0, 1] (coefficient of determination bounds)
- r2_ci_lower < r_squared < r2_ci_upper (valid confidence intervals)
- effect_size in ["small", "medium", "large", "negligible"]
- r_squared_difference in [-1, 1] (difference bounds)
- semi_partial_r2 >= 0 (non-negative variance explained)

*Data Quality:*
- All 3 domain R² values present
- Bootstrap distributions contain 1000 values each
- All pairwise R² comparisons computed (3 comparisons)
- Semi-partial R² sums to total R² within rounding error

*Log Validation:*
- Required: "Model comparison complete: R² extracted for 3 domains"
- Required: "Bootstrap R² complete: 1000 iterations"
- Required: "R² differences computed with confidence intervals"
- Forbidden: "ERROR", "R² calculation failed", "bootstrap failed"

**Expected Behavior on Validation Failure:**
Log specific comparison error and quit with model comparison failure.

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (dependency status)
- data/step01_domain_theta_scores.csv (extracted domain scores)
- data/step01_merged_dataset.csv (complete analysis dataset)
- data/step01_descriptive_stats.csv (domain descriptive statistics)
- data/step02_what_model_results.csv (What domain regression)
- data/step02_where_model_results.csv (Where domain regression)
- data/step02_when_model_results.csv (When domain regression)
- data/step02_model_diagnostics.csv (assumption checks)
- data/step02_bootstrap_coefficients.csv (bootstrap coefficient CIs)
- data/step03_beta_coefficient_matrix.csv (coefficient comparison matrix)
- data/step03_cross_domain_comparisons.csv (hypothesis test data)
- data/step03_effect_sizes.csv (effect size classifications)
- data/step03_heatmap_plot_data.csv (visualization data for rq_plots)
- data/step04_steiger_z_tests.csv (statistical test results)
- data/step04_correlation_matrix.csv (full correlation matrix)
- data/step04_corrected_pvalues.csv (multiple comparison corrections)
- data/step04_bootstrap_correlation_diffs.csv (bootstrap correlation CIs)
- data/step05_model_comparison.csv (R² comparisons)
- data/step05_bootstrap_r_squared.csv (bootstrap R² distributions)
- data/step05_r_squared_differences.csv (pairwise R² comparisons)
- data/step05_predictor_contributions.csv (semi-partial R² contributions)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_data.log
- logs/step02_fit_models.log  
- logs/step03_extract_coefficients.log
- logs/step04_steiger_tests.log
- logs/step05_compare_models.log

### Plots (EMPTY until rq_plots runs)
Note: step03_heatmap_plot_data.csv created in data/ for domain prediction heatmap

### Results (EMPTY until rq_results runs)
Note: summary.md will be created by rq_results summarizing domain-specific prediction findings

---

## Expected Data Formats

### Step-to-Step Transformations
1. **Step 0 -> 1:** Dependency validation enables data extraction
2. **Step 1 -> 2:** Merged dataset flows into regression modeling
3. **Step 2 -> 3:** Model results enable beta coefficient extraction
4. **Step 3 -> 4:** Beta coefficients enable statistical comparisons
5. **Step 4 -> 5:** Statistical tests completed before model performance comparison

### Column Naming Conventions
- **UID:** participant identifier (consistent across all files)
- **domain:** ["What", "Where", "When"] (categorical, consistent naming)
- **theta_mean:** mean IRT theta score per domain per participant
- **predictor:** ["RAVLT_T", "BVMT_T", "RPM_T"] (standardized cognitive test scores)
- **beta:** standardized regression coefficient
- **p_uncorrected:** raw p-value before multiple comparison correction
- **p_bonferroni:** Bonferroni-corrected p-value
- **p_fdr:** FDR-corrected p-value using Benjamini-Hochberg

### Data Type Constraints
- **UID:** object/string (non-nullable)
- **theta_mean, beta, r_squared:** float64 (nullable only if computation failed)
- **domain, predictor:** categorical/object (non-nullable, specific levels only)
- **p_values:** float64 in [0, 1] (non-nullable for completed tests)
- **significance:** object ["***", "**", "*", "ns"] (non-nullable)

---

## Cross-RQ Dependencies

**Required Ch5 Outputs:**
- Ch5 5.2.1 (What domain IRT analysis) -> theta scores for What domain
- Ch5 5.2.2 (Where domain IRT analysis) -> theta scores for Where domain  
- Ch5 5.2.3 (When domain IRT analysis) -> theta scores for When domain

**Dependency Validation:**
- Step 0 validates all Ch5 outputs exist and are accessible
- Fallback file path patterns accommodate naming variations
- Graceful failure with specific error messages if dependencies missing

**Data Integration:**
- Domain theta scores merged on composite_ID -> UID mapping
- Cognitive test scores from dfnonvr.csv merged on UID
- Complete case analysis (participants with all domain scores + cognitive tests)

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
- **Output validation:** All Ch5 dependency files accessible
- **Content validation:** Required columns present in each file
- **Quality validation:** Expected participant count across files
- **Log validation:** No file access errors or missing dependencies

#### Step 1: Extract Data  
- **Output validation:** 300 rows (100 UIDs x 3 domains) in theta scores
- **Value validation:** Theta values within IRT scale bounds [-4, 4]
- **Quality validation:** Complete data for 95+ participants, <5% missing
- **Log validation:** Successful merge operations, no critical errors

#### Step 2: Fit Models
- **Output validation:** 3 models converged, 12 coefficients extracted
- **Value validation:** Beta coefficients within reasonable bounds [-2, 2]
- **Quality validation:** Assumption checks completed, diagnostics available
- **Log validation:** Model convergence confirmed, bootstrap completion

#### Step 3: Extract Coefficients
- **Output validation:** Beta coefficient matrix complete (3x4)
- **Value validation:** All coefficients finite, effect sizes classified
- **Quality validation:** Cross-domain comparisons prepared
- **Log validation:** Coefficient extraction successful

#### Step 4: Statistical Tests
- **Output validation:** Steiger Z-tests completed (3 comparisons)
- **Value validation:** Z-statistics and p-values valid ranges
- **Quality validation:** Multiple comparison corrections applied
- **Log validation:** Test completion, no statistical failures

#### Step 5: Model Comparison
- **Output validation:** R² values and bootstrap CIs computed
- **Value validation:** R² within [0,1], valid confidence intervals
- **Quality validation:** Bootstrap distributions complete (1000 iterations)
- **Log validation:** Comparison computations successful

---

## Summary

**Total Steps:** 6 (Step 0: validation + Steps 1-5: analysis)
**Estimated Runtime:** 45-60 minutes
**Cross-RQ Dependencies:** Ch5 5.2.1, 5.2.2, 5.2.3 (domain theta scores)
**Primary Outputs:** 21 data files, 6 log files, 1 plot data file
**Validation Coverage:** 100% (all 6 steps have 4-layer validation requirements)

**Key Hypothesis:** Domain-specific prediction patterns expected - RAVLT predicts What domain more than Where domain, BVMT predicts Where domain more than What domain, When domain least predictable overall.

**Critical Methodological Notes:**
- All models use standardized predictors for comparable beta coefficients
- Bootstrap confidence intervals (1000 iterations, seed=42) provide robust uncertainty quantification  
- Steiger's Z-tests appropriate for dependent correlation comparisons within same sample
- Multiple comparison corrections (Bonferroni + FDR) control Type I error inflation
- Decision D068 compliance: dual p-value reporting throughout analysis
- Assumption violation remedies specified for each potential issue

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml  
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent with v5.1 enhanced specifications