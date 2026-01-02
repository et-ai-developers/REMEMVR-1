# Analysis Plan: RQ 7.1.4 - Unique REMEMVR variance unexplained by all predictors?

**Research Question:** 7.1.4
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines the incremental validity of REMEMVR theta scores through hierarchical multiple regression with 3 blocks of predictors. The analysis determines what proportion of REMEMVR variance remains unexplained after accounting for demographics, cognitive tests, and self-report measures. This addresses the core question of whether REMEMVR captures meaningful memory variance beyond traditional neuropsychological assessments.

The pipeline involves extracting predictor data from master.xlsx (demographics, cognitive tests, self-report), merging with mean REMEMVR theta scores from Ch5 analyses, conducting hierarchical regression with cross-validation, computing effect sizes, and analyzing residual variance. Domain-specific analyses examine whether different memory domains (What/Where/When) show differential unexplained variance patterns.

**Pipeline:** Hierarchical regression with 5-fold cross-validation
**Steps:** 8 total analysis steps
**Estimated Runtime:** Medium complexity (~45-60 minutes total)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni-corrected)
- Chapter-level alpha: 0.00179 (Bonferroni correction for 28 RQs)
- Mandatory cross-validation to prevent overfitting
- Bootstrap confidence intervals for effect sizes

---

## Analysis Plan

### Step 0: Extract Cognitive Test Data

**Dependencies:** None (first step)
**Complexity:** Low (~5 minutes)

**Input:**
- File: data/cache/master.xlsx
- Required tags: `{UID}-COG-X-RAV-T1Sc` to `T5Sc`, `{UID}-COG-X-RAV-DRSc`, `{UID}-COG-X-BVM-TotR`, `{UID}-COG-X-NAR-Scor`, `{UID}-COG-X-RPM-Scor`
- Expected participants: N=100 with complete cognitive test data
- Missing data handling: Complete case analysis (exclude participants with missing cognitive data)

**Processing:**
- Extract raw RAVLT trial scores (T1-T5) and Delayed Recall (DR)
- Compute RAVLT_Total = T1 + T2 + T3 + T4 + T5 (learning trials sum)
- Extract BVMT Total Recall, NART score, RPM score
- Convert all cognitive test scores to T-scores (M=50, SD=10) for standardized interpretation
- Validate score ranges (RAVLT trials: 0-15, Total: 0-75; BVMT: 0-36; NART: 0-50; RPM: 0-60)

**Output:**
- File: data/step00_cognitive_tests.csv
- Format: One row per participant
- Columns: UID, RAVLT_T1 through T5, RAVLT_DR, RAVLT_Total, BVMT_TotalRecall, NART_Score, RPM_Score, RAVLT_Total_Tscore, BVMT_TotalRecall_Tscore, NART_Score_Tscore, RPM_Score_Tscore
- Expected rows: ~100 participants
- Expected columns: 13 total

**Validation Requirement:**
Validation tools MUST be used after analysis tool execution. Specific validation tools will be determined by rq_tools based on data extraction requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_cognitive_tests.csv: 100 rows x 13 columns
- Data types: UID (object), all scores (float64)

*Value Ranges:*
- RAVLT raw scores: T1-T5 in [0, 15], DR in [0, 15], Total in [0, 75]
- BVMT raw score in [0, 36], NART in [0, 50], RPM in [0, 60]
- T-scores approximately in [20, 80] (mean=50, SD=10 with normal variation)

*Data Quality:*
- All 100 participants present (complete cognitive test data required)
- No NaN values in computed scores
- UID format matches A### pattern

*Log Validation:*
- Required: "Cognitive test extraction complete: 100 participants"
- Required: "T-score conversion applied: M=50.0, SD=10.0"
- Forbidden: "ERROR", "NaN values detected"

**Expected Behavior:**
Extract and standardize cognitive test scores, creating T-score variables for regression analysis.

---

### Step 1: Extract Demographics Data

**Dependencies:** None (parallel to Step 0)
**Complexity:** Low (~3 minutes)

**Input:**
- File: data/cache/master.xlsx
- Required tags: `{UID}-DEM-X-Age`, `{UID}-DEM-X-Sex`, `{UID}-DEM-X-Education`
- Expected participants: N=100

**Processing:**
- Extract age in years (continuous variable)
- Extract sex (categorical: Male/Female) and create dummy variable (0=Male, 1=Female)
- Extract education level and convert to years of education scale
- Validate age range (20-70 years based on recruitment criteria)

**Output:**
- File: data/step01_demographics.csv
- Format: One row per participant
- Columns: UID, Age, Sex, Sex_Female_dummy, Education_years
- Expected rows: 100 participants
- Expected columns: 5 total

**Validation Requirement:**
Validation tools MUST be used after analysis tool execution. Specific validation tools will be determined by rq_tools based on demographic data extraction requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_demographics.csv: 100 rows x 5 columns
- Data types: UID (object), Age (float64), Sex (object), Sex_Female_dummy (int64), Education_years (float64)

*Value Ranges:*
- Age in [20, 70] (recruitment age range)
- Sex in {"Male", "Female"}
- Sex_Female_dummy in {0, 1}
- Education_years in [6, 25] (typical education range)

*Data Quality:*
- All 100 participants present
- No NaN values in any column
- Sex categories balanced (expect ~50% each)

*Log Validation:*
- Required: "Demographics extraction complete: 100 participants"
- Required: "Sex dummy variable created: Female=1, Male=0"
- Forbidden: "ERROR", "Missing age data"

**Expected Behavior:**
Extract demographic variables with proper coding for regression analysis.

---

### Step 2: Extract Self-Report Data

**Dependencies:** None (parallel to Steps 0-1)
**Complexity:** Low (~3 minutes)

**Input:**
- File: data/cache/master.xlsx
- Required tags: `{UID}-DEM-X-DASS_Dep`, `{UID}-DEM-X-DASS_Anx`, `{UID}-DEM-X-DASS_Str`, `{UID}-DEM-X-VR_Exp`, `{UID}-DEM-X-SLEEP`
- Expected participants: ~97 (some missing DASS data expected)

**Processing:**
- Extract DASS Depression, Anxiety, Stress subscale scores
- Extract VR Experience rating (self-reported familiarity)
- Extract Sleep quality rating
- Handle missing DASS data (note which participants have missing data)
- Validate DASS score ranges (0-42 for each subscale)

**Output:**
- File: data/step02_self_report.csv
- Format: One row per participant with complete data
- Columns: UID, DASS_Depression, DASS_Anxiety, DASS_Stress, VR_Experience, Sleep_Quality
- Expected rows: ~97 participants (some missing DASS)
- Expected columns: 6 total

**Validation Requirement:**
Validation tools MUST be used after analysis tool execution. Specific validation tools will be determined by rq_tools based on self-report data extraction requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_self_report.csv: 95-100 rows x 6 columns
- Data types: all numeric columns (float64), UID (object)

*Value Ranges:*
- DASS subscales in [0, 42] (standard DASS-21 range)
- VR_Experience in [1, 7] (Likert scale)
- Sleep_Quality in [1, 10] (quality rating scale)

*Data Quality:*
- 95-100 participants present (some DASS missing acceptable)
- No NaN values in retained participants
- Document participants excluded due to missing self-report

*Log Validation:*
- Required: "Self-report extraction complete: [N] participants with complete data"
- Required: "DASS missing data documented: [N] participants excluded"
- Forbidden: "ERROR", "Invalid DASS scores"

**Expected Behavior:**
Extract self-report measures, handling missing data appropriately for hierarchical regression.

---

### Step 3: Extract and Merge REMEMVR Theta Scores

**Dependencies:** Ch5 analyses (5.1.1 and 5.2.x must be complete)
**Complexity:** Medium (~10 minutes)

**Input:**
- File 1: results/ch5/5.1.1/data/step03_theta_scores.csv (overall theta)
- File 2: results/ch5/5.2.1/data/step03_theta_scores.csv (What domain theta)
- File 3: results/ch5/5.2.2/data/step03_theta_scores.csv (Where domain theta) 
- File 4: results/ch5/5.2.3/data/step03_theta_scores.csv (When domain theta)
- Expected format: composite_ID, theta estimates per domain
- Expected N: ~400 rows per file (100 participants x 4 tests)

**Processing:**
- Parse composite_ID to extract UID and test session
- Compute mean theta per UID across all 4 test sessions for each domain
- Handle missing test sessions (participants who missed tests)
- Merge overall theta with domain-specific theta scores
- Validate theta ranges (-3 to +3 typical IRT range)

**Output:**
- File: data/step03_rememvr_theta.csv
- Format: One row per participant
- Columns: UID, theta_overall_mean, theta_What_mean, theta_Where_mean, theta_When_mean, n_tests_completed
- Expected rows: 100 participants
- Expected columns: 6 total

**Validation Requirement:**
Validation tools MUST be used after analysis tool execution. Specific validation tools will be determined by rq_tools based on theta score aggregation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_rememvr_theta.csv: 100 rows x 6 columns
- Data types: UID (object), all theta means (float64), n_tests_completed (int64)

*Value Ranges:*
- All theta means in [-3, 3] (typical IRT ability range)
- n_tests_completed in [3, 4] (most participants complete 3-4 tests)

*Data Quality:*
- All 100 participants present
- No NaN values in theta means (computed from available tests)
- Most participants have n_tests_completed = 4

*Log Validation:*
- Required: "REMEMVR theta extraction complete: 100 participants"
- Required: "Mean theta computed across [N] test sessions per participant"
- Forbidden: "ERROR", "Theta values out of range"

**Expected Behavior:**
Extract and average REMEMVR theta scores across test sessions for hierarchical regression analysis.

---

### Step 4: Merge All Predictors with REMEMVR Theta

**Dependencies:** Steps 0, 1, 2, 3 (requires all extraction steps)
**Complexity:** Low (~5 minutes)

**Input:**
- File 1: data/step00_cognitive_tests.csv (cognitive test T-scores)
- File 2: data/step01_demographics.csv (age, sex, education)
- File 3: data/step02_self_report.csv (DASS, VR experience, sleep)
- File 4: data/step03_rememvr_theta.csv (mean theta scores)
- Merge key: UID (must be consistent across all files)

**Processing:**
- Left join all predictor files on UID with REMEMVR theta as base
- Handle participants with missing self-report data (complete case analysis)
- Create final analysis dataset with all predictors
- Verify no missing data in final dataset (hierarchical regression requires complete cases)
- Standardize predictors for effect size interpretation

**Output:**
- File: data/step04_merged_predictors.csv
- Format: One row per participant with complete data
- Columns: UID, Age, Sex_Female_dummy, Education_years, RAVLT_Total_Tscore, BVMT_TotalRecall_Tscore, NART_Score_Tscore, RPM_Score_Tscore, DASS_Depression, DASS_Anxiety, DASS_Stress, VR_Experience, Sleep_Quality, theta_overall_mean, theta_What_mean, theta_Where_mean, theta_When_mean
- Expected rows: ~95-97 participants (complete case analysis)
- Expected columns: 17 total

**Validation Requirement:**
Validation tools MUST be used after analysis tool execution. Specific validation tools will be determined by rq_tools based on data merging requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_merged_predictors.csv: 95-100 rows x 17 columns
- Data types: UID (object), all numeric predictors and outcomes (float64)

*Value Ranges:*
- All T-scores approximately in [20, 80]
- DASS scores in [0, 42]
- Theta scores in [-3, 3]

*Data Quality:*
- 95-100 participants with complete data
- No NaN values in any column
- All UIDs unique (no duplicates)

*Log Validation:*
- Required: "Predictor merge complete: [N] participants with complete data"
- Required: "Complete case analysis: [N] participants retained"
- Forbidden: "ERROR", "NaN values in final dataset"

**Expected Behavior:**
Create analysis-ready dataset with all predictors and outcomes for hierarchical regression.

---

### Step 5: Conduct Hierarchical Regression with Cross-Validation

**Dependencies:** Step 4 (requires merged predictor dataset)
**Complexity:** High (~20-30 minutes)

**Input:**
- File: data/step04_merged_predictors.csv
- Predictor blocks: Block 1 (demographics: Age, Sex, Education), Block 2 (cognitive: RAVLT, BVMT, NART, RPM T-scores), Block 3 (self-report: DASS subscales, VR experience, sleep)
- Outcome: theta_overall_mean
- Sample size: ~95-97 participants

**Processing:**
- Implement 5-fold cross-validation for model stability assessment
- Fit Model 1 (demographics only): theta ~ Age + Sex_Female_dummy + Education_years
- Fit Model 2 (+ cognitive tests): theta ~ Block1 + cognitive T-scores
- Fit Model 3 (+ self-report): theta ~ Block1 + Block2 + DASS + VR_Exp + Sleep
- Compute training and test R² for each model to detect overfitting
- Test significance of R² increments using F-tests with Chapter-level alpha (0.00179)
- Assess multicollinearity (VIF < 5 for all predictors)
- Check regression assumptions (normality, homoscedasticity, linearity)

**Output:**
- File 1: data/step05_hierarchical_models.csv (model comparison statistics)
- Format: One row per model
- Columns: Model, R2_train, R2_test, R2_increment, F_statistic, p_value, p_value_bonferroni, AIC, BIC, df_model, df_residual
- Expected rows: 3 models
- Expected columns: 11 total

- File 2: data/step05_model_diagnostics.csv (assumption checks)
- Format: One row per diagnostic test
- Columns: Test, Statistic, p_value, Interpretation, Remedial_action

**Validation Requirement:**
Validation tools MUST be used after analysis tool execution. Specific validation tools will be determined by rq_tools based on hierarchical regression requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_hierarchical_models.csv: 3 rows x 11 columns
- data/step05_model_diagnostics.csv: 6-10 rows x 5 columns
- Data types: Model (object), all statistics (float64)

*Value Ranges:*
- R² values in [0, 1]
- F-statistics > 0
- p-values in [0, 1]
- VIF < 5 for all predictors

*Data Quality:*
- All 3 models fitted successfully
- No NaN values in statistics
- Cross-validation completed (train-test R² gap < 0.10)

*Log Validation:*
- Required: "Hierarchical regression complete: 3 models fitted"
- Required: "Cross-validation complete: mean train-test R2 gap = [value]"
- Required: "Model assumptions checked: [N] diagnostics passed"
- Forbidden: "ERROR", "Model convergence failed"

**Expected Behavior:**
Fit hierarchical regression models with cross-validation and assumption checking.

---

### Step 6: Compute Effect Sizes and Variance Decomposition

**Dependencies:** Step 5 (requires fitted regression models)
**Complexity:** Medium (~10 minutes)

**Input:**
- File: data/step05_hierarchical_models.csv (R² values for each model)
- Model statistics: R² increments, F-statistics, p-values
- Sample size from Step 4 merge

**Processing:**
- Calculate Cohen's f² effect sizes for each block: f² = ”R² / (1 - R²_full)
- Interpret effect sizes: f² = 0.02 (small), 0.15 (medium), 0.35 (large)
- Compute 95% confidence intervals for f² using bootstrap (1000 iterations)
- Calculate residual variance: 1 - R²_Model3
- Separate measurement error from true residual using theta SEs from Ch5
- Compute power analysis: Given N and 12 predictors, what effect size detectable at 80% power?
- Test significance of R² increments with dual p-value reporting (Decision D068)

**Output:**
- File: data/step06_variance_decomposition.csv
- Format: One row per block plus residual
- Columns: Component, R2_contribution, R2_increment, Cohens_f2, f2_CI_lower, f2_CI_upper, Effect_size_interpretation, p_value_uncorrected, p_value_bonferroni
- Expected rows: 4 (demographics, cognitive, self-report, residual)
- Expected columns: 9 total

**Validation Requirement:**
Validation tools MUST be used after analysis tool execution. Specific validation tools will be determined by rq_tools based on effect size computation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_variance_decomposition.csv: 4 rows x 9 columns
- Data types: Component (object), all statistics (float64)

*Value Ranges:*
- R² values in [0, 1]
- Cohen's f² e 0
- Confidence intervals: CI_lower d f² d CI_upper
- p-values in [0, 1]

*Data Quality:*
- All 4 components present (3 blocks + residual)
- No NaN values in effect sizes
- Bootstrap CIs computed successfully

*Log Validation:*
- Required: "Effect size computation complete: Cohen's f² calculated"
- Required: "Bootstrap confidence intervals: 1000 iterations"
- Required: "Dual p-values reported per Decision D068"
- Forbidden: "ERROR", "Bootstrap failed"

**Expected Behavior:**
Compute effect sizes and decompose variance into predictor blocks and residual.

---

### Step 7: Domain-Specific Residual Analysis

**Dependencies:** Steps 4, 6 (requires merged data and variance decomposition methods)
**Complexity:** Medium (~15 minutes)

**Input:**
- File: data/step04_merged_predictors.csv (with domain-specific theta scores)
- Model specification from Step 5 (same 3-block predictor structure)
- Outcomes: theta_What_mean, theta_Where_mean, theta_When_mean

**Processing:**
- Repeat hierarchical regression for each memory domain separately
- Use identical 3-block structure: demographics ’ + cognitive ’ + self-report
- Compute residual variance for each domain after Model 3
- Compare residual percentages across domains (test hypothesis: When > Where > What)
- Calculate domain-specific R² and effect sizes
- Test domain differences in residual variance using bootstrap comparison

**Output:**
- File: data/step07_domain_residuals.csv
- Format: One row per domain
- Columns: Domain, R2_Model1, R2_Model2, R2_Model3, Residual_variance, Residual_percentage, Cohens_f2_cognitive, p_value_cognitive_uncorrected, p_value_cognitive_bonferroni
- Expected rows: 3 domains
- Expected columns: 9 total

**Validation Requirement:**
Validation tools MUST be used after analysis tool execution. Specific validation tools will be determined by rq_tools based on domain-specific regression requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_domain_residuals.csv: 3 rows x 9 columns
- Data types: Domain (object), all statistics (float64)

*Value Ranges:*
- R² values in [0, 1] for all models
- Residual percentages in [0, 100]
- Cohen's f² e 0

*Data Quality:*
- All 3 domains present (What, Where, When)
- No NaN values in residuals
- Residual percentages sum appropriately

*Log Validation:*
- Required: "Domain-specific analysis complete: 3 domains analyzed"
- Required: "Residual variance computed for What, Where, When domains"
- Forbidden: "ERROR", "Domain analysis failed"

**Expected Behavior:**
Analyze whether different memory domains show differential patterns of unexplained variance.

---

### Step 8: Prepare Incremental Validity Visualization Data

**Dependencies:** Steps 6, 7 (requires variance decomposition and domain results)
**Complexity:** Low (~5 minutes)

**Input:**
- File 1: data/step06_variance_decomposition.csv (overall variance decomposition)
- File 2: data/step07_domain_residuals.csv (domain-specific residuals)
- Model statistics from hierarchical regression

**Processing:**
- Combine variance decomposition data for overall theta and domain-specific theta
- Create plot source data for variance decomposition visualization
- Format data for stacked bar chart showing explained vs unexplained variance
- Prepare secondary plot data comparing residual variance across domains
- Include confidence intervals for visualization

**Output:**
- File 1: data/step08_incremental_validity_data.csv (plot source for overall variance decomposition)
- Format: Plot source CSV for variance decomposition visualization  
- Columns: Component, Variance_explained, CI_lower, CI_upper, Analysis_type
- Expected rows: 8 (4 components x 2 analysis types: overall + average domain)
- Expected columns: 5 total

- File 2: data/step08_domain_comparison_data.csv (plot source for domain residuals comparison)
- Format: Plot source CSV for domain residuals comparison
- Columns: Domain, Residual_variance, CI_lower, CI_upper
- Expected rows: 3 domains
- Expected columns: 4 total

**Validation Requirement:**
Validation tools MUST be used after analysis tool execution. Specific validation tools will be determined by rq_tools based on plot data preparation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_incremental_validity_data.csv: 8 rows x 5 columns
- data/step08_domain_comparison_data.csv: 3 rows x 4 columns
- Data types: categorical columns (object), numeric columns (float64)

*Value Ranges:*
- Variance_explained in [0, 1]
- Residual_variance in [0, 1]
- Confidence intervals: CI_lower d estimate d CI_upper

*Data Quality:*
- All expected rows present (8 and 3 respectively)
- No NaN values in plot data
- Confidence intervals valid (lower d upper)

*Log Validation:*
- Required: "Plot data preparation complete: variance decomposition"
- Required: "Domain comparison data prepared: 3 domains"
- Forbidden: "ERROR", "Missing plot data"

**Expected Behavior:**
Prepare plot source data for visualizing incremental validity results and domain comparisons.

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_cognitive_tests.csv (extracted and T-scored cognitive test data)
- data/step01_demographics.csv (age, sex, education with proper coding)
- data/step02_self_report.csv (DASS, VR experience, sleep quality)
- data/step03_rememvr_theta.csv (mean theta scores by domain from Ch5)
- data/step04_merged_predictors.csv (complete analysis dataset)
- data/step05_hierarchical_models.csv (model comparison statistics)
- data/step05_model_diagnostics.csv (regression assumption checks)
- data/step06_variance_decomposition.csv (R², Cohen's f², effect sizes by block)
- data/step07_domain_residuals.csv (residual analysis by memory domain)
- data/step08_incremental_validity_data.csv (plot source: overall variance decomposition)
- data/step08_domain_comparison_data.csv (plot source: domain residuals comparison)

### Logs (ONLY execution logs - .log files capturing stdout/stderr)
- logs/step00_extract_cognitive_tests.log
- logs/step01_extract_demographics.log
- logs/step02_extract_self_report.log
- logs/step03_extract_rememvr_theta.log
- logs/step04_merge_predictors.log
- logs/step05_hierarchical_regression.log
- logs/step06_compute_variance_decomposition.log
- logs/step07_domain_residuals_analysis.log
- logs/step08_prepare_incremental_validity_plot_data.log

### Plots (EMPTY until rq_plots runs)
- plots/variance_decomposition.png (created by rq_plots, NOT analysis steps)
- plots/domain_residuals_comparison.png (created by rq_plots)

### Results (EMPTY until rq_results runs)
- results/summary.md (created by rq_results, NOT analysis steps)

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 ’ 1-3: Parallel Extraction**
- All extraction steps run independently from master.xlsx
- Each creates participant-level (UID) summary data
- Consistent UID column enables merging in Step 4

**Step 4: Merge Transformation**
- Input: 4 separate files with UID as key
- Process: Left join on UID (REMEMVR theta as base)
- Output: Wide format analysis dataset
- Filtering: Complete case analysis (exclude participants with missing data)

**Step 5: Regression Analysis**
- Input: Wide format (one row per participant)
- Process: Hierarchical model fitting with cross-validation
- Output: Model statistics table + diagnostic results

**Step 6-7: Effect Size and Domain Analysis**
- Input: Model statistics from Step 5
- Process: Effect size calculations and domain-specific modeling  
- Output: Variance decomposition tables

**Step 8: Plot Data Preparation**
- Input: Results tables from Steps 6-7
- Process: Reshape for visualization
- Output: Plot source CSVs for rq_plots

### Column Naming Conventions

**Cognitive Tests (Step 0):**
- Raw scores: RAVLT_T1, RAVLT_T2, etc.
- Derived scores: RAVLT_Total (sum of learning trials)
- Standardized: RAVLT_Total_Tscore, BVMT_TotalRecall_Tscore

**Demographics (Step 1):**
- Age: continuous variable in years
- Sex: categorical variable + Sex_Female_dummy (0/1)
- Education_years: converted to years scale

**Regression Outputs (Steps 5-6):**
- R2_train, R2_test (cross-validation)
- R2_increment (hierarchical increments)
- Cohens_f2 (effect sizes)
- p_value_uncorrected, p_value_bonferroni (dual reporting per D068)

### Data Type Constraints

**Identifiers:**
- UID: object/string type (format A###)
- composite_ID: object/string (format UID_test)

**Continuous Variables:**
- All theta scores: float64, range [-3, 3]
- All test scores: float64, validated ranges per test
- All statistics: float64, appropriate ranges per statistic

**Categorical Variables:**
- Sex: object type {"Male", "Female"}
- Domain: object type {"What", "Where", "When"}
- Analysis_type: object type for plot grouping

---

## Cross-RQ Dependencies

**This RQ depends on:** Chapter 5 IRT analyses for REMEMVR theta scores

**Required Files from Ch5:**
- results/ch5/5.1.1/data/step03_theta_scores.csv (overall REMEMVR theta estimates)
- results/ch5/5.2.1/data/step03_theta_scores.csv (What domain theta)
- results/ch5/5.2.2/data/step03_theta_scores.csv (Where domain theta) 
- results/ch5/5.2.3/data/step03_theta_scores.csv (When domain theta)

**Status Check:**
- rq_planner should verify these Ch5 RQ results exist and contain theta scores
- If any Ch5 file missing: FAIL with "Ch5 analyses must complete before RQ 7.1.4"

**Data Integration:**
- Step 3: Parse composite_ID to extract UID and compute mean theta per participant
- Expected: 100 participants x 4 test sessions = 400 rows per Ch5 file
- Aggregation: Mean theta across test sessions for stable individual difference measures

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
- bash execution (Step 14 workflow) will run analysis ’ validation ’ error on validation failure

**Downstream Agent Requirements:**
- **rq_tools:** MUST specify validation tool for EVERY analysis step (no exceptions)
- **rq_analysis:** MUST embed validation tool call for EVERY analysis step (no exceptions)
- **g_code:** MUST generate code with validation function calls (no exceptions)
- **rq_inspect:** MUST verify validation ran successfully (checks logs/stepN_name.log for validation output)

### Validation Requirements By Step

#### Step 0-3: Data Extraction Steps

**Analysis Tools:** (determined by rq_tools - data extraction functions)
**Validation Tools:** (determined by rq_tools - data format validation)

**What Validation Checks:**
- Output files exist with expected dimensions
- No unexpected missing data patterns
- Value ranges within scientifically reasonable bounds
- UID formats consistent across extraction steps
- Sample sizes match expected N=100 (or documented exclusions)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to appropriate logs/stepNN_*.log
- Quit script immediately (do NOT proceed to next step)
- g_debug invoked by master to diagnose root cause

#### Step 4: Data Merge

**Analysis Tools:** (data merging and complete case analysis)
**Validation Tools:** (merge validation and missing data checks)

**What Validation Checks:**
- All UIDs matched successfully across files
- Complete case analysis documented (N participants retained)
- No duplicate UIDs in final dataset
- All required columns present post-merge

**Expected Behavior on Validation Failure:**
- Raise error with merge diagnostics
- Document which participants lost due to missing data
- Quit if critical merge failures occur

#### Step 5: Hierarchical Regression

**Analysis Tools:** (hierarchical model fitting with cross-validation)
**Validation Tools:** (regression model validation and assumption checking)

**What Validation Checks:**
- All 3 models fitted successfully
- Cross-validation completed (train-test R² gap < 0.10)
- Regression assumptions met (normality, homoscedasticity, linearity)
- Multicollinearity acceptable (VIF < 5)
- F-tests for R² increments computed correctly

**Expected Behavior on Validation Failure:**
- Report specific assumption violations
- Suggest remedial actions (robust SEs, transformations)
- Continue with robust analyses if assumptions violated

#### Step 6-7: Effect Size and Domain Analysis

**Analysis Tools:** (effect size computation and domain-specific modeling)
**Validation Tools:** (effect size validation and statistical range checks)

**What Validation Checks:**
- Cohen's f² values non-negative and reasonable (f² < 5.0)
- Bootstrap confidence intervals computed successfully
- Dual p-values reported correctly (Decision D068)
- Domain-specific models fitted without convergence issues

**Expected Behavior on Validation Failure:**
- Report effect size computation errors
- Document bootstrap failures if any
- Ensure dual p-value reporting maintained

#### Step 8: Plot Data Preparation

**Analysis Tools:** (plot data aggregation and formatting)
**Validation Tools:** (plot data completeness and format validation)

**What Validation Checks:**
- Plot source CSVs have expected dimensions
- All required columns present with correct data types
- Value ranges appropriate for plotting
- Complete factorial design (all domains/components represented)

**Expected Behavior on Validation Failure:**
- Report missing plot data elements
- Document which visualizations cannot be created
- Ensure plot data matches expected format for rq_plots

---

## Summary

**Total Steps:** 9 (Step 0-8: extraction through plot data preparation)
**Estimated Runtime:** Medium complexity (~45-60 minutes total)
**Cross-RQ Dependencies:** Ch5 IRT analyses (5.1.1, 5.2.1-5.2.3) must be complete
**Primary Outputs:** Hierarchical regression results, variance decomposition, domain residual analysis, plot source data
**Validation Coverage:** 100% (all 9 steps have validation requirements)

**Key Analysis Features:**
- 5-fold cross-validation to prevent overfitting
- Chapter-level alpha correction (0.00179)
- Dual p-value reporting per Decision D068
- Bootstrap confidence intervals for effect sizes
- Domain-specific residual analysis
- Complete assumption checking with remedial actions

**Success Criteria:**
- Cognitive tests block shows significant R² increment (p < 0.00179)
- Total explained variance < 55% (substantial residual remains)
- When domain shows highest residual variance
- Model diagnostics pass or remedial actions documented

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan ’ creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml ’ creates 4_analysis.yaml  
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml ’ generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent for hierarchical regression incremental validity analysis