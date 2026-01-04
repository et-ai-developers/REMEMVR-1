# Analysis Plan: RQ 7.5.3 - Memory Strategies Predicting Performance

**Research Question:** 7.5.3
**Created:** 2026-01-04  
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines the relationship between self-reported memory strategies and overall REMEMVR performance. The analysis uses mean theta_all scores from RQ 5.1.1 as the outcome measure and strategy variables extracted from the "Describe your technique here" questionnaire responses in dfnonvr.csv. The analysis plan addresses the identified data availability concern by confirming that strategy questionnaire data IS available in column 100 of dfnonvr.csv.

**Pipeline:** Correlational analysis and t-test with hierarchical regression control variables  
**Steps:** 8 total analysis steps (Step 0: data extraction + Steps 1-7: analysis)  
**Estimated Runtime:** Medium (~45-60 minutes total, primarily from text coding and bootstrap procedures)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected and Bonferroni-corrected p-values for multiple comparisons)
- Bootstrap confidence intervals with 1000 replications and seed=42 for robust inference

---

## Analysis Plan

This RQ requires 8 steps:

### Step 0: Extract and Merge Data Sources

**Dependencies:** None (first step)  
**Complexity:** Low (data extraction and merging only, ~5 minutes)

**Input:**

**File 1:** /home/etai/projects/REMEMVR/results/ch5/5.1.1/data/step03_theta_scores.csv  
**Source:** RQ 5.1.1 (omnibus theta_all scores)  
**Format:** CSV with columns:
  - `UID` (string, participant identifier, e.g., "P001")  
  - `theta_all` (float, omnibus ability estimate across all domains)  
  - `se_all` (float, standard error of theta_all estimate)  
**Expected Rows:** 100 participants

**File 2:** /home/etai/projects/REMEMVR/data/dfnonvr.csv  
**Source:** Participant-level questionnaire and cognitive data  
**Required Columns:**
  - `UID` (string, participant identifier)  
  - `Describe your technique here` (string, strategy questionnaire responses)  
  - `Education level` (string, education categories for control variable)  
  - `Age in years` (numeric, age for control variable)  
**Expected Rows:** 100 participants

**Processing:**
- Load theta scores from RQ 5.1.1 dependency
- Load questionnaire responses from dfnonvr.csv  
- Merge datasets on UID (inner join to ensure complete cases only)
- Verify all 100 participants have both theta scores and strategy responses

**Output:**

**File 1:** data/step00_merged_data.csv  
**Format:** CSV, one row per participant  
**Columns:**
  - `UID` (string, participant identifier)
  - `theta_all` (float, ability estimate from RQ 5.1.1)  
  - `se_all` (float, standard error)  
  - `strategy_text` (string, raw strategy descriptions)  
  - `education_level` (string, education categories)  
  - `age_years` (numeric, age in years)  
**Expected Rows:** 100 participants (complete cases only)

**Validation Requirement:**  
Validation tools MUST be used after data extraction tool execution. Specific validation tools will be determined by rq_tools based on data merging requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_merged_data.csv: 100 rows x 6 columns (UID: object, theta_all: float64, se_all: float64, strategy_text: object, education_level: object, age_years: float64)

*Value Ranges:*  
- theta_all in [-3, 3] (typical IRT ability range)
- se_all in [0.1, 1.0] (reasonable standard error bounds)  
- age_years in [18, 80] (adult participants)  
- strategy_text: non-empty strings (no missing strategy responses)

*Data Quality:*
- All 100 participants present (no data loss from merge)  
- No NaN values in theta_all or strategy_text (required for analysis)  
- Strategy text responses have minimum 5 characters (meaningful responses only)

*Log Validation:*
- Required: "Merge completed: 100 participants with complete data"  
- Required: "Strategy responses verified: 100 non-empty strings"  
- Forbidden: "ERROR", "Missing theta scores", "Missing strategy data"

**Expected Behavior on Validation Failure:**  
Raise error with specific failure message, log to logs/step00_extract_and_merge_data.log, quit immediately, invoke g_debug

---

### Step 1: Code Strategy Variables from Text Responses

**Dependencies:** Step 0 (requires merged dataset)  
**Complexity:** Medium (text coding required, ~15 minutes)

**Input:**

**File:** data/step00_merged_data.csv  
**Required Columns:** `UID`, `strategy_text`  
**Expected Format:** One strategy text response per participant

**Processing:**
- Code rehearsal frequency from strategy text responses (quantitative scale 0-5)  
  - 0 = No mention of rehearsal/repetition  
  - 1 = Rare/minimal rehearsal mentioned  
  - 2 = Occasional rehearsal  
  - 3 = Regular rehearsal  
  - 4 = Frequent rehearsal  
  - 5 = Extensive/systematic rehearsal  
- Code mnemonic use from strategy text responses (binary 0/1)  
  - 0 = No mnemonic strategies mentioned  
  - 1 = Any mnemonic strategies mentioned (visualization, association, acronyms, etc.)  
- Manual coding with systematic keywords and researcher judgment  
- Create coding reliability check on random 20% subset

**Output:**

**File 1:** data/step01_strategy_variables.csv  
**Format:** CSV, one row per participant  
**Columns:**
  - `UID` (string, participant identifier)  
  - `rehearsal_frequency` (int, 0-5 scale)  
  - `mnemonic_use` (int, binary 0/1)  
  - `strategy_text` (string, original text for verification)  
**Expected Rows:** 100 participants

**File 2:** data/step01_coding_reliability.txt  
**Format:** Text report  
**Content:** Inter-rater reliability statistics for coding subset, Cohen's kappa for mnemonic coding, correlation for rehearsal ratings

**Validation Requirement:**  
Validation tools MUST be used after strategy coding tool execution. Validation will check coding consistency and value ranges.

**Substance Validation Criteria:**

*Output Files:*
- data/step01_strategy_variables.csv: 100 rows x 4 columns (UID: object, rehearsal_frequency: int64, mnemonic_use: int64, strategy_text: object)  
- data/step01_coding_reliability.txt: text file with reliability statistics

*Value Ranges:*
- rehearsal_frequency in [0, 5] (defined ordinal scale)  
- mnemonic_use in [0, 1] (binary coding)  
- Distribution check: rehearsal_frequency should show variation (not all 0 or all 5)

*Data Quality:*
- All 100 participants coded (no missing strategy variables)  
- Coding reliability Cohen's kappa >= 0.60 (substantial agreement threshold)  
- Rehearsal frequency correlation with reliability coder >= 0.75

*Log Validation:*
- Required: "Strategy coding completed: 100 participants"  
- Required: "Reliability check: kappa = X.XX, correlation = X.XX"  
- Forbidden: "Coding reliability below threshold", "ERROR in text processing"

**Expected Behavior on Validation Failure:**  
Report coding reliability concerns, log detailed statistics, proceed with warning if reliability marginal (0.50-0.60), quit if reliability poor (<0.50)

---

### Step 2: Descriptive Statistics and Data Exploration

**Dependencies:** Step 1 (requires coded strategy variables)  
**Complexity:** Low (descriptive analysis only, ~5 minutes)

**Input:**

**Files:** data/step00_merged_data.csv + data/step01_strategy_variables.csv  
**Merge Key:** UID  
**Required Variables:** theta_all, rehearsal_frequency, mnemonic_use, age_years, education_level

**Processing:**
- Merge strategy variables with theta scores and demographics  
- Compute descriptive statistics for all variables  
- Check distributions (normality, outliers, missing data patterns)  
- Create frequency tables for categorical variables  
- Identify extreme values requiring sensitivity analysis

**Output:**

**File 1:** data/step02_descriptive_stats.csv  
**Format:** CSV with descriptive statistics table  
**Content:** Mean, SD, min, max, skewness, kurtosis for continuous variables; frequencies for categorical

**File 2:** data/step02_analysis_dataset.csv  
**Format:** CSV, analysis-ready dataset  
**Columns:**
  - `UID` (string)  
  - `theta_all` (float, outcome variable)  
  - `rehearsal_frequency` (int, primary predictor)  
  - `mnemonic_use` (int, secondary predictor)  
  - `age_years` (float, control variable)  
  - `education_numeric` (float, education coded as years)  
**Expected Rows:** 100 participants

**Validation Requirement:**  
Validation tools MUST be used after descriptive analysis execution to verify data quality and distribution assumptions.

**Substance Validation Criteria:**

*Output Files:*
- data/step02_descriptive_stats.csv: summary statistics table  
- data/step02_analysis_dataset.csv: 100 rows x 6 columns (complete analysis dataset)

*Value Ranges:*
- All variables within expected ranges from previous steps  
- No extreme outliers beyond 3 SDs from mean  
- Rehearsal frequency shows adequate variation (at least 3 different values used)

*Data Quality:*
- Analysis dataset complete: 100 rows, no NaN values  
- Education successfully converted to numeric years  
- Theta_all distribution approximately normal (Shapiro p > 0.01)

*Log Validation:*
- Required: "Descriptive analysis completed: 100 complete cases"  
- Required: "Distribution checks passed for primary variables"  
- Acceptable warnings: "Mild skewness detected in rehearsal_frequency"

**Expected Behavior on Validation Failure:**  
Document distributional concerns, proceed with non-parametric alternatives if normality severely violated, quit if data quality insufficient

---

### Step 3: Primary Correlational Analysis

**Dependencies:** Step 2 (requires analysis dataset)  
**Complexity:** Low (correlation and t-test, ~5 minutes)

**Input:**

**File:** data/step02_analysis_dataset.csv  
**Variables:** theta_all (outcome), rehearsal_frequency (continuous predictor), mnemonic_use (binary predictor)

**Processing:**
- Pearson correlation between rehearsal_frequency and theta_all  
- Independent samples t-test: mnemonic users (1) vs non-users (0)  
- Compute effect sizes (r for correlation, Cohen's d for t-test)  
- Apply Decision D068: Report BOTH uncorrected and Bonferroni-corrected p-values  
- Bootstrap confidence intervals (1000 replications, seed=42) for effect sizes

**Output:**

**File 1:** data/step03_correlation_results.csv  
**Format:** CSV with correlation analysis results  
**Columns:**
  - `analysis` (string: "rehearsal_theta_correlation")  
  - `r` (float, Pearson correlation coefficient)  
  - `p_uncorrected` (float, uncorrected p-value)  
  - `p_bonferroni` (float, Bonferroni-corrected p-value)  
  - `CI_lower` (float, 95% CI lower bound for r)  
  - `CI_upper` (float, 95% CI upper bound for r)  
  - `n` (int, sample size)

**File 2:** data/step03_group_comparison.csv  
**Format:** CSV with t-test results  
**Columns:**
  - `analysis` (string: "mnemonic_users_vs_nonusers")  
  - `mean_group1` (float, theta_all mean for non-users)  
  - `mean_group2` (float, theta_all mean for users)  
  - `t_statistic` (float, t-test statistic)  
  - `df` (int, degrees of freedom)  
  - `p_uncorrected` (float, uncorrected p-value)  
  - `p_bonferroni` (float, Bonferroni-corrected p-value)  
  - `cohens_d` (float, effect size)  
  - `CI_lower` (float, 95% CI for Cohen's d)  
  - `CI_upper` (float, 95% CI for Cohen's d)  
  - `n1` (int, non-users sample size)  
  - `n2` (int, users sample size)

**Validation Requirement:**  
Validation tools MUST be used after correlational analysis execution. Validation will verify Decision D068 dual p-value reporting and effect size calculations.

**Substance Validation Criteria:**

*Output Files:*
- data/step03_correlation_results.csv: 1 row with correlation analysis  
- data/step03_group_comparison.csv: 1 row with t-test analysis

*Value Ranges:*
- r in [-1, 1] (correlation bounds)  
- p_uncorrected in [0, 1], p_bonferroni in [0, 1]  
- p_bonferroni >= p_uncorrected (correction increases p-values)  
- cohens_d typically in [-2, 2] (reasonable effect size range)

*Data Quality:*
- Both analysis files contain exactly 1 row each  
- Confidence intervals properly bounded (CI_lower < CI_upper)  
- Sample sizes sum to 100 (n1 + n2 = 100 for t-test, n = 100 for correlation)

*Log Validation:*
- Required: "Correlation analysis: r = X.XX, p_uncorrected = X.XX, p_bonferroni = X.XX"  
- Required: "T-test analysis: t = X.XX, Cohen's d = X.XX"  
- Required: "Decision D068 compliance: dual p-values reported"  
- Forbidden: "Correlation out of bounds", "Missing p-values"

**Expected Behavior on Validation Failure:**  
Report statistical computation errors, verify bootstrap procedure completed successfully, quit if effect size calculations invalid

---

### Step 4: Control Variable Analysis

**Dependencies:** Step 3 (requires primary analysis results)  
**Complexity:** Medium (hierarchical regression, ~10 minutes)

**Input:**

**File:** data/step02_analysis_dataset.csv  
**Variables:** theta_all (outcome), rehearsal_frequency, mnemonic_use (predictors), age_years, education_numeric (controls)

**Processing:**
- Hierarchical multiple regression with block entry:  
  - Block 1: Demographics (age_years, education_numeric)  
  - Block 2: Add memory strategies (rehearsal_frequency, mnemonic_use)  
- Compute incremental R-squared for strategy block  
- Test significance of R-squared change  
- Extract final model coefficients with standard errors  
- Compute Cohen's f-squared effect sizes for strategy predictors  
- Apply Decision D068: Report dual p-values for all coefficients

**Output:**

**File 1:** data/step04_hierarchical_regression.csv  
**Format:** CSV with hierarchical regression results  
**Columns:**
  - `block` (int: 1 for demographics, 2 for full model)  
  - `r_squared` (float, proportion variance explained)  
  - `r_squared_change` (float, increment from adding block)  
  - `f_change` (float, F-statistic for change)  
  - `p_change_uncorrected` (float, uncorrected p for change)  
  - `p_change_bonferroni` (float, Bonferroni-corrected p)

**File 2:** data/step04_final_coefficients.csv  
**Format:** CSV with final model coefficients  
**Columns:**
  - `predictor` (string, variable names)  
  - `coefficient` (float, regression coefficient)  
  - `se` (float, standard error)  
  - `t_statistic` (float, t-value)  
  - `p_uncorrected` (float, uncorrected p-value)  
  - `p_bonferroni` (float, Bonferroni-corrected p-value)  
  - `cohens_f2` (float, effect size for strategy predictors)

**Validation Requirement:**  
Validation tools MUST be used after hierarchical regression execution to verify model fitting and Decision D068 compliance.

**Substance Validation Criteria:**

*Output Files:*
- data/step04_hierarchical_regression.csv: 2 rows (Block 1 and Block 2)  
- data/step04_final_coefficients.csv: 5 rows (intercept + 4 predictors)

*Value Ranges:*
- r_squared in [0, 1] (proportion variance)  
- r_squared_change >= 0 (incremental variance non-negative)  
- cohens_f2 >= 0 (effect sizes non-negative)  
- All p-values in [0, 1], p_bonferroni >= p_uncorrected

*Data Quality:*
- Block 2 R-squared >= Block 1 R-squared (adding predictors cannot decrease fit)  
- All predictors have finite coefficients (no convergence issues)  
- Standard errors positive and finite

*Log Validation:*
- Required: "Hierarchical regression completed: Block 1 R� = X.XX, Block 2 R� = X.XX"  
- Required: "Strategy block increment: 봕� = X.XX, p = X.XX"  
- Required: "Decision D068: dual p-values for all coefficients"  
- Forbidden: "Convergence failed", "Infinite coefficients"

**Expected Behavior on Validation Failure:**  
Report regression diagnostic issues, check for multicollinearity problems, quit if model unstable

---

### Step 5: Model Diagnostics and Assumptions

**Dependencies:** Step 4 (requires fitted regression model)  
**Complexity:** Medium (comprehensive diagnostics, ~10 minutes)

**Input:**

**File:** data/step02_analysis_dataset.csv (analysis data)  
**Fitted Model:** From Step 4 hierarchical regression

**Processing:**
- Check regression assumptions:  
  - Residuals normality (Shapiro-Wilk test)  
  - Homoscedasticity (Breusch-Pagan test)  
  - Linearity (residuals vs fitted plots)  
  - Independence (no systematic patterns)  
- Identify outliers and influential points:  
  - Standardized residuals > 3 SDs  
  - Cook's distance > 4/n threshold  
  - Leverage values > 2p/n threshold  
- Compute variance inflation factors (VIF) for multicollinearity  
- Create diagnostic plots for visual inspection

**Output:**

**File 1:** data/step05_assumption_tests.csv  
**Format:** CSV with assumption test results  
**Columns:**
  - `test` (string, test name)  
  - `statistic` (float, test statistic)  
  - `p_value` (float, significance)  
  - `interpretation` (string, assumption met/violated)

**File 2:** data/step05_outlier_analysis.csv  
**Format:** CSV with outlier identification  
**Columns:**
  - `UID` (string, participant identifier)  
  - `standardized_residual` (float)  
  - `cooks_distance` (float)  
  - `leverage` (float)  
  - `outlier_flag` (boolean, influential case indicator)

**File 3:** data/step05_vif_analysis.csv  
**Format:** CSV with multicollinearity check  
**Columns:**
  - `predictor` (string, variable name)  
  - `vif` (float, variance inflation factor)  
  - `multicollinearity_concern` (boolean, VIF > 5 threshold)

**Validation Requirement:**  
Validation tools MUST be used after diagnostic analysis to verify assumption testing completed successfully.

**Substance Validation Criteria:**

*Output Files:*
- data/step05_assumption_tests.csv: 4+ rows (normality, homoscedasticity, etc.)  
- data/step05_outlier_analysis.csv: 100 rows (all participants)  
- data/step05_vif_analysis.csv: 4 rows (excluding intercept)

*Value Ranges:*
- standardized_residual typically in [-3, 3] (majority within bounds)  
- cooks_distance in [0, 1] (most values near 0)  
- leverage in [0, 1] (bounded by definition)  
- vif >= 1.0 (minimum possible VIF)

*Data Quality:*
- Outlier flags identify <10% of cases as influential  
- VIF values reasonable (majority < 5.0)  
- Assumption test statistics finite and valid

*Log Validation:*
- Required: "Assumption testing completed: normality p = X.XX, homoscedasticity p = X.XX"  
- Required: "Outlier analysis: X outliers identified out of 100 cases"  
- Required: "VIF analysis: maximum VIF = X.XX"  
- Acceptable warnings: "Mild assumption violations detected"

**Expected Behavior on Validation Failure:**  
Document assumption violations but proceed with sensitivity analysis, note limitations for interpretation

---

### Step 6: Sensitivity Analysis and Robust Inference

**Dependencies:** Step 5 (requires diagnostic results)  
**Complexity:** Medium (bootstrap and outlier analysis, ~10 minutes)

**Input:**

**Files:** data/step02_analysis_dataset.csv, data/step05_outlier_analysis.csv  
**Outlier Identification:** Cases flagged as influential from Step 5

**Processing:**
- Bootstrap regression analysis (1000 replications, seed=42):  
  - Bootstrap confidence intervals for all coefficients  
  - Bootstrap R-squared distribution  
  - Percentile and bias-corrected confidence intervals  
- Outlier-robust analysis:  
  - Re-fit regression excluding influential outliers  
  - Compare coefficient stability  
  - Assess impact on significance conclusions  
- Cross-validation analysis:  
  - 5-fold cross-validation (seed=42) to assess generalization  
  - Mean cross-validated R-squared and standard error

**Output:**

**File 1:** data/step06_bootstrap_results.csv  
**Format:** CSV with bootstrap inference  
**Columns:**
  - `predictor` (string, variable name)  
  - `original_coefficient` (float, from Step 4)  
  - `bootstrap_mean` (float, mean across 1000 replications)  
  - `bootstrap_se` (float, bootstrap standard error)  
  - `CI_lower_percentile` (float, 2.5th percentile)  
  - `CI_upper_percentile` (float, 97.5th percentile)  
  - `CI_lower_bca` (float, bias-corrected lower)  
  - `CI_upper_bca` (float, bias-corrected upper)

**File 2:** data/step06_outlier_sensitivity.csv  
**Format:** CSV with outlier sensitivity analysis  
**Columns:**
  - `analysis` (string: "full_sample" or "outliers_excluded")  
  - `n_cases` (int, sample size)  
  - `r_squared` (float, model R-squared)  
  - `rehearsal_coefficient` (float)  
  - `mnemonic_coefficient` (float)  
  - `rehearsal_p_value` (float)  
  - `mnemonic_p_value` (float)

**File 3:** data/step06_cross_validation.csv  
**Format:** CSV with cross-validation results  
**Columns:**
  - `fold` (int, 1-5)  
  - `r_squared_cv` (float, cross-validated R-squared per fold)  
  - `mean_cv_r_squared` (float, average across folds)  
  - `se_cv_r_squared` (float, standard error across folds)

**Validation Requirement:**  
Validation tools MUST be used after sensitivity analysis to verify bootstrap procedure and cross-validation completed successfully.

**Substance Validation Criteria:**

*Output Files:*
- data/step06_bootstrap_results.csv: 5 rows (intercept + 4 predictors)  
- data/step06_outlier_sensitivity.csv: 2 rows (full vs reduced sample)  
- data/step06_cross_validation.csv: 6 rows (5 folds + summary statistics)

*Value Ranges:*
- Bootstrap confidence intervals should contain original coefficients  
- Cross-validated R-squared typically lower than original (shrinkage expected)  
- Mean CV R-squared should be positive and <1.0

*Data Quality:*
- Bootstrap replications completed successfully (1000 iterations)  
- Outlier-excluded analysis maintains reasonable sample size (>80 cases)  
- Cross-validation folds balanced (approximately equal sizes)

*Log Validation:*
- Required: "Bootstrap analysis: 1000 replications completed"  
- Required: "Cross-validation: mean CV R� = X.XX (SE = X.XX)"  
- Required: "Outlier sensitivity: X cases excluded, results stable/changed"  
- Forbidden: "Bootstrap failed", "Cross-validation error"

**Expected Behavior on Validation Failure:**  
Report bootstrap or cross-validation technical issues, verify random seed setting, quit if resampling procedures fail

---

### Step 7: Effect Size Interpretation and Final Summary

**Dependencies:** Step 6 (requires sensitivity analysis results)  
**Complexity:** Low (summary and interpretation, ~5 minutes)

**Input:**

**Files:** All previous analysis outputs (Steps 3-6)  
**Focus:** Integration of primary analysis, control analysis, and sensitivity results

**Processing:**
- Synthesize effect sizes across analyses:  
  - Primary correlation and t-test results  
  - Hierarchical regression incremental R-squared  
  - Bootstrap confidence interval interpretation  
- Apply conventional effect size benchmarks:  
  - Correlation: small r = 0.10, medium r = 0.30, large r = 0.50  
  - Cohen's d: small d = 0.20, medium d = 0.50, large d = 0.80  
  - Cohen's f-squared: small f� = 0.02, medium f� = 0.15, large f� = 0.35  
- Create interpretation summary considering:  
  - Statistical significance (Decision D068 dual p-values)  
  - Effect size magnitude and precision  
  - Sensitivity to outliers and assumptions  
  - Theoretical predictions from concept document

**Output:**

**File 1:** data/step07_effect_size_summary.csv  
**Format:** CSV with effect size interpretation  
**Columns:**
  - `analysis` (string, analysis type)  
  - `effect_size` (float, primary effect size estimate)  
  - `effect_size_type` (string: "correlation", "cohens_d", "cohens_f2")  
  - `magnitude` (string: "negligible", "small", "medium", "large")  
  - `CI_lower` (float, confidence interval lower)  
  - `CI_upper` (float, confidence interval upper)  
  - `interpretation` (string, practical significance)

**File 2:** data/step07_final_conclusions.txt  
**Format:** Text summary for thesis  
**Content:**
- Summary of strategy variable distributions  
- Primary analysis results with dual p-values  
- Control variable impact assessment  
- Sensitivity analysis conclusions  
- Effect size interpretations with confidence intervals  
- Limitations and future directions

**Validation Requirement:**  
Validation tools MUST be used after summary generation to verify completeness and accuracy of effect size interpretations.

**Substance Validation Criteria:**

*Output Files:*
- data/step07_effect_size_summary.csv: 3+ rows (correlation, t-test, regression)  
- data/step07_final_conclusions.txt: comprehensive text summary

*Value Ranges:*
- Effect sizes match values from previous steps (consistency check)  
- Confidence intervals preserve directionality from original analyses  
- Magnitude classifications align with conventional benchmarks

*Data Quality:*
- All primary analyses represented in summary table  
- Text summary addresses all research questions from concept  
- Confidence intervals and p-values reported consistently

*Log Validation:*
- Required: "Effect size summary completed: X analyses summarized"  
- Required: "Text conclusions generated: all research questions addressed"  
- Forbidden: "Inconsistent effect sizes", "Missing analyses"

**Expected Behavior on Validation Failure:**  
Report inconsistencies between summary and original analyses, verify all analyses included in final summary

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs - intermediate and final)
- data/step00_merged_data.csv (from Step 0: data extraction and merging)
- data/step01_strategy_variables.csv (from Step 1: strategy text coding)
- data/step01_coding_reliability.txt (from Step 1: reliability report)
- data/step02_descriptive_stats.csv (from Step 2: descriptive statistics)
- data/step02_analysis_dataset.csv (from Step 2: analysis-ready data)
- data/step03_correlation_results.csv (from Step 3: correlation analysis)
- data/step03_group_comparison.csv (from Step 3: t-test results)
- data/step04_hierarchical_regression.csv (from Step 4: regression models)
- data/step04_final_coefficients.csv (from Step 4: model coefficients)
- data/step05_assumption_tests.csv (from Step 5: diagnostic tests)
- data/step05_outlier_analysis.csv (from Step 5: outlier identification)
- data/step05_vif_analysis.csv (from Step 5: multicollinearity check)
- data/step06_bootstrap_results.csv (from Step 6: bootstrap inference)
- data/step06_outlier_sensitivity.csv (from Step 6: sensitivity analysis)
- data/step06_cross_validation.csv (from Step 6: cross-validation results)
- data/step07_effect_size_summary.csv (from Step 7: effect size interpretation)
- data/step07_final_conclusions.txt (from Step 7: thesis summary)

### Logs (ONLY execution logs - .log files capturing stdout/stderr)
- logs/step00_extract_and_merge_data.log
- logs/step01_code_strategy_variables.log
- logs/step02_descriptive_statistics.log
- logs/step03_correlational_analysis.log
- logs/step04_control_variable_analysis.log
- logs/step05_model_diagnostics.log
- logs/step06_sensitivity_analysis.log
- logs/step07_effect_size_summary.log

### Plots (EMPTY until rq_plots runs - no plots specified for this RQ)
- No plots specified for this correlational analysis RQ

### Results (EMPTY until rq_results runs)
- results/summary.md (created by rq_results, NOT analysis steps)

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 -> Step 1 Transformation:**
- Input: Separate files (theta scores, questionnaire responses)
- Processing: Inner join on UID, retain complete cases only
- Output: Single merged dataset with 6 columns, 100 rows

**Step 1 -> Step 2 Transformation:**  
- Input: Raw strategy text responses (string format)
- Processing: Manual text coding with systematic keyword identification
- Output: Quantitative strategy variables (rehearsal 0-5, mnemonic 0-1)

**Step 2 -> Step 3 Transformation:**
- Input: Analysis-ready dataset with all variables
- Processing: Statistical tests (correlation, t-test) with bootstrap CIs
- Output: Formatted results tables with dual p-values

**Step 4 -> Step 6 Transformation:**
- Input: Hierarchical regression results from Step 4
- Processing: Bootstrap resampling (1000 replications) and sensitivity analysis
- Output: Robust confidence intervals and outlier-adjusted results

### Column Naming Conventions

**Core Analysis Variables:**
- `UID`: Participant identifier (consistent across all files)
- `theta_all`: Outcome variable from RQ 5.1.1 (IRT ability estimate)
- `rehearsal_frequency`: Primary predictor (0-5 ordinal scale)
- `mnemonic_use`: Secondary predictor (0-1 binary)
- `age_years`: Control variable (continuous)
- `education_numeric`: Control variable (years of education)

**Statistical Output Variables:**
- `p_uncorrected`: Original p-value (Decision D068 requirement)
- `p_bonferroni`: Bonferroni-corrected p-value (Decision D068 requirement)
- `CI_lower`, `CI_upper`: 95% confidence interval bounds
- `cohens_d`: Standardized mean difference effect size
- `cohens_f2`: Regression effect size (for strategy predictors only)

### Data Type Constraints

**Participant Data:**
- UID: string (never nullable)
- theta_all: float64 (range [-3, 3], not nullable)
- se_all: float64 (range [0.1, 1.0], not nullable)
- age_years: float64 (range [18, 80], not nullable)

**Strategy Variables:**
- rehearsal_frequency: int64 (range [0, 5], not nullable)
- mnemonic_use: int64 (values {0, 1} only, not nullable)
- strategy_text: object/string (minimum 5 characters, not nullable)

**Statistical Results:**
- All p-values: float64 (range [0, 1], not nullable)
- All effect sizes: float64 (correlation: [-1, 1], Cohen's d/f�: [0, ], not nullable)
- All confidence intervals: float64 (CI_lower < CI_upper, not nullable)

---

## Cross-RQ Dependencies

### Dependency Type: DERIVED Data from Other RQs (Dependencies Exist)

**This RQ requires outputs from:**
- **RQ 5.1.1** (Omnibus IRT Calibration - Functional Form)
  - File: /home/etai/projects/REMEMVR/results/ch5/5.1.1/data/step03_theta_scores.csv
  - Used in: Step 0 (theta_all scores as outcome variable)
  - Rationale: RQ 5.1.1 provides omnibus ability estimates across all memory domains. This RQ examines whether self-reported memory strategies predict these overall ability estimates.

**Data Source Boundaries:**
- **RAW data:** dfnonvr.csv strategy questionnaire responses extracted directly (no RQ dependencies)
- **DERIVED data:** Theta scores from RQ 5.1.1 (dependency required)
- **Scope:** This RQ does NOT re-calibrate IRT models (uses RQ 5.1.1 theta scores as fixed outcome)

**Execution Order Constraint:**
1. RQ 5.1.1 must complete first (provides step03_theta_scores.csv)
2. This RQ executes second (uses theta scores as outcome measure)

**Validation:**
- Step 0: Check /home/etai/projects/REMEMVR/results/ch5/5.1.1/data/step03_theta_scores.csv exists (circuit breaker: FILE_MISSING if absent)
- Step 0: Verify theta scores contain expected 100 participants with theta_all column
- If dependency file missing -> quit with error -> user must execute RQ 5.1.1 first

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

#### Step 0: Extract and Merge Data Sources

**Analysis Tool:** (determined by rq_tools - likely tools.data.load_participant_data + merge operations)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_data_format + validate_merge_completeness)

**What Validation Checks:**
- Output files exist (data/step00_merged_data.csv)
- Expected column count (6 columns: UID, theta_all, se_all, strategy_text, education_level, age_years)
- Expected row count (100 participants, complete cases only)
- Merge completeness (all RQ 5.1.1 participants matched with dfnonvr.csv)
- Data quality (no NaN in critical columns, strategy text non-empty)
- Value ranges (theta_all in [-3, 3], age_years in [18, 80])

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 100 participants, found 87 after merge")
- Log failure to logs/step00_extract_and_merge_data.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked by master to diagnose root cause

---

#### Step 1: Code Strategy Variables from Text Responses

**Analysis Tool:** (determined by rq_tools - likely custom strategy coding function)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_categorical_coding + reliability checks)

**What Validation Checks:**
- Output files exist (data/step01_strategy_variables.csv, data/step01_coding_reliability.txt)
- Strategy variables in valid ranges (rehearsal_frequency 0-5, mnemonic_use 0-1)
- Coding reliability meets threshold (Cohen's kappa >= 0.60, correlation >= 0.75)
- Complete coding (no missing strategy variables)
- Distribution checks (adequate variation in rehearsal frequencies)

**Expected Behavior on Validation Failure:**
- Report coding reliability concerns with specific statistics
- Proceed with warning if reliability marginal (0.50-0.60)
- Quit if reliability poor (<0.50) or systematic coding errors detected
- Document coding limitations for interpretation

---

#### Step 2: Descriptive Statistics and Data Exploration

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_stats.compute_descriptive_statistics)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_distribution_assumptions + validate_data_completeness)

**What Validation Checks:**
- Analysis dataset complete (100 rows, 6 columns, no NaN)
- Descriptive statistics computed successfully
- Distribution assumptions evaluated (normality, outliers, skewness)
- Variable transformations valid (education converted to numeric)
- Value ranges preserved from previous steps

**Expected Behavior on Validation Failure:**
- Document distributional violations but proceed with appropriate adjustments
- Note need for non-parametric alternatives if normality severely violated
- Quit if data quality insufficient for analysis

---

#### Step 3: Primary Correlational Analysis

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_stats.t_test_d068 + correlation functions)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_correlation_test_d068 + validate_hypothesis_tests)

**What Validation Checks:**
- Decision D068 compliance (dual p-values present: p_uncorrected, p_bonferroni)
- Effect size calculations valid (r in [-1, 1], Cohen's d finite)
- Bootstrap confidence intervals computed (1000 replications, seed=42)
- Sample size preservation (n=100 for correlation, n1+n2=100 for t-test)
- Statistical results format consistency

**Expected Behavior on Validation Failure:**
- Report Decision D068 violations (missing corrected p-values)
- Verify bootstrap procedure completed successfully
- Quit if effect size calculations invalid or statistical tests failed

---

#### Step 4: Control Variable Analysis

**Analysis Tool:** (determined by rq_tools - likely tools.regression.fit_hierarchical_regression)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_regression_assumptions + validate_hypothesis_tests)

**What Validation Checks:**
- Hierarchical regression completed successfully (2 blocks fitted)
- Decision D068 compliance (dual p-values for all coefficients)
- R-squared change computed correctly (Block 2 >= Block 1)
- Cohen's f-squared effect sizes calculated for strategy predictors
- Model convergence achieved (finite coefficients, positive standard errors)

**Expected Behavior on Validation Failure:**
- Report regression fitting issues (convergence problems, infinite coefficients)
- Check for multicollinearity concerns affecting stability
- Quit if model fundamentally unstable or decision D068 violated

---

#### Step 5: Model Diagnostics and Assumptions

**Analysis Tool:** (determined by rq_tools - likely tools.validation.validate_regression_assumptions)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_diagnostic_completeness)

**What Validation Checks:**
- Assumption tests completed (normality, homoscedasticity, linearity, independence)
- Outlier analysis performed (standardized residuals, Cook's distance, leverage)
- VIF analysis for multicollinearity (values typically <5.0)
- Diagnostic statistics within reasonable bounds
- Outlier identification criteria applied consistently

**Expected Behavior on Validation Failure:**
- Document assumption violations but proceed with sensitivity analysis
- Note diagnostic concerns for interpretation limitations
- Continue analysis with appropriate caveats

---

#### Step 6: Sensitivity Analysis and Robust Inference

**Analysis Tool:** (determined by rq_tools - likely tools.bootstrap.bootstrap_regression_ci + cross-validation functions)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_bootstrap_stability + validate_cross_validation)

**What Validation Checks:**
- Bootstrap analysis completed (1000 replications, seed=42)
- Cross-validation performed successfully (5 folds, balanced samples)
- Outlier sensitivity analysis conducted (comparison with/without influential cases)
- Bootstrap confidence intervals contain original estimates
- Cross-validated R-squared shows expected shrinkage

**Expected Behavior on Validation Failure:**
- Report bootstrap or cross-validation technical failures
- Verify random seed settings for reproducibility
- Quit if resampling procedures fundamentally failed

---

#### Step 7: Effect Size Interpretation and Final Summary

**Analysis Tool:** (determined by rq_tools - likely custom summary generation function)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_summary_completeness)

**What Validation Checks:**
- Effect size summary includes all primary analyses
- Magnitude classifications align with conventional benchmarks
- Text summary addresses all research questions from concept
- Confidence intervals and interpretations consistent across steps
- Final conclusions supported by analysis results

**Expected Behavior on Validation Failure:**
- Report inconsistencies between summary and original analyses
- Verify completeness of effect size interpretations
- Ensure all research questions addressed in conclusions

---

## Summary

**Total Steps:** 8 (Step 0: extraction + Steps 1-7: analysis)  
**Estimated Runtime:** Medium (~45-60 minutes, primarily text coding and bootstrap procedures)  
**Cross-RQ Dependencies:** RQ 5.1.1 (theta_all scores required)  
**Primary Outputs:** Correlation results, hierarchical regression, bootstrap confidence intervals, sensitivity analysis  
**Validation Coverage:** 100% (all 8 steps have validation requirements)

**Key Methodological Features:**
- Decision D068 compliance: Dual p-value reporting throughout
- Bootstrap inference: 1000 replications with seed=42 for robust confidence intervals
- Hierarchical regression: Control for demographics before testing strategy effects
- Comprehensive diagnostics: Assumptions, outliers, cross-validation, sensitivity analysis
- Text coding with reliability checks: Systematic strategy variable extraction

**Data Availability Confirmation:**
- STR questionnaire data IS available in dfnonvr.csv column 100 ("Describe your technique here")
- RQ 5.1.1 theta scores ARE available at expected dependency path
- Education and age controls available for hierarchical regression
- Analysis proceeds as originally planned with full dataset (N=100)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2026-01-04): Initial plan created by rq_planner agent
  - Confirmed data availability: STR questionnaire data exists in dfnonvr.csv
  - Verified RQ 5.1.1 dependency: theta scores available
  - 8-step analysis plan: data extraction, text coding, correlational analysis, hierarchical regression, diagnostics, sensitivity analysis, summary
  - Decision D068 compliance: dual p-value reporting throughout
  - Bootstrap inference and cross-validation for robust statistical inference