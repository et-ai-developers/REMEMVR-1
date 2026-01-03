# Analysis Plan: RQ 7.6.2 - RAVLT Delayed Forgetting Predicts REMEMVR Slope

**Research Question:** 7.6.2
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This analysis tests whether short-term forgetting on the RAVLT (delayed recall after 20-30 minutes) predicts long-term forgetting on REMEMVR (slope over 6 days). The study examines cross-temporal scale correlations using bivariate and partial correlation analysis with N=100 participants.

**Pipeline:** Correlation Analysis (Bivariate + Partial with Cross-Validation)
**Steps:** 9 total analysis steps (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** 45-60 minutes

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Chapter 7 family-wise correction (alpha = 0.05/28 = 0.00179)
- Cross-RQ dependency on Ch5 5.1.1 omnibus slopes

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 outputs exist before proceeding with correlation analysis

**Input:**
- Primary: /home/etai/projects/REMEMVR/results/ch5/5.1.1/status.yaml (verify rq_results: success)
- Alternative: /home/etai/projects/REMEMVR/results/ch5/5.1.1/data/step06_best_model.pkl
- Fallback: /home/etai/projects/REMEMVR/results/ch5/5.1.1/data/*lmm*.{pkl,csv,txt}
- Expected content: Individual participant slope estimates from omnibus LMM
- If not found: QUIT with "Ch5 5.1.1 omnibus outputs not found for slope extraction"

**Processing:**
- Check Ch5 5.1.1 completion status (must be 'success')
- Locate LMM output files using multiple path patterns
- Verify files contain per-participant slope estimates (not just group-level)
- Test file accessibility and format validity
- Log all validation checks with timestamps

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Must contain status checks and file discovery results

*Value Ranges:*
- N/A (text file with status information)

*Data Quality:*
- All required Ch5 files must be found and accessible
- Validation must pass for all dependencies

*Log Validation:*
- Required pattern: "Ch5 5.1.1 status: success"
- Required pattern: "LMM output files found"
- Required pattern: "VALIDATION - PASS"
- Forbidden patterns: "ERROR", "FAIL", "not found"

**Expected Behavior on Validation Failure:**
Raise error with specific missing dependency, log to logs/step00_validate_dependencies.log, quit immediately.

### Step 1: Extract and Prepare Data
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Medium (~10 minutes including data merging)

**Purpose:** Extract REMEMVR slopes from Ch5 analysis and RAVLT scores from master.xlsx, prepare analysis dataset

**Input:**
- Primary: /home/etai/projects/REMEMVR/results/ch5/5.1.1/data/step06_best_model.pkl (LMM with individual slopes)
- Alternative: /home/etai/projects/REMEMVR/results/ch5/5.1.1/data/step04_lmm_input.csv
- Fallback: /home/etai/projects/REMEMVR/results/ch5/5.1.1/data/*slope*.csv
- RAVLT source: /home/etai/projects/REMEMVR/data/cache/master.xlsx
- Required RAVLT columns: UID, RAV_T5Sc (Trial 5 score), RAV_DRSc (Delayed Recall score)

**Processing:**
- Load Ch5 LMM model and extract individual participant slopes
- Alternative: Load pre-computed slope values from CSV if available
- Load RAVLT data from master.xlsx, extract T5 and Delayed Recall scores
- Filter to participants with complete RAVLT + REMEMVR data
- Create merged dataset with UID, REMEMVR_Slope, RAV_T5Sc, RAV_DRSc
- Check for missing data, document exclusions
- Verify N=100 expected sample size (allow ±5 for missing data)

**Output:**
- data/step01_extracted_data.csv (merged REMEMVR slopes + RAVLT scores)

**Validation Requirement:**
Validation tools MUST be used after data extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_extracted_data.csv: N rows x 5 columns (95-100 participants expected)
- Columns: UID (object), REMEMVR_Slope (float64), RAV_T5Sc (float64), RAV_DRSc (float64), complete_case (bool)

*Value Ranges:*
- REMEMVR_Slope in [-0.5, 0.5] (theta change per day, negative = forgetting)
- RAV_T5Sc in [0, 15] (RAVLT T-scores, typically 20-80 but using raw)
- RAV_DRSc in [0, 15] (delayed recall raw scores)
- All slopes should be negative (forgetting over time)

*Data Quality:*
- Final N >= 95 participants (allowing for missing RAVLT data)
- No duplicate UIDs
- Missing data < 5% per variable
- Complete cases flagged appropriately

*Log Validation:*
- Required pattern: "Data merged successfully: N=XX participants"
- Required pattern: "Missing data summary: RAV_T5Sc: X%, RAV_DRSc: X%"
- Required pattern: "VALIDATION - PASS"
- Forbidden patterns: "ERROR", "FAIL", "merge failed"

**Expected Behavior on Validation Failure:**
Raise error with specific data quality issue, log to logs/step01_extract_data.log, invoke g_debug for data inspection.

### Step 2: Compute RAVLT Forgetting Index
**Dependencies:** Step 1 (extracted data)
**Complexity:** Low (~5 minutes)

**Purpose:** Calculate RAVLT forgetting index and standardize variables for effect size interpretation

**Input:**
- data/step01_extracted_data.csv (REMEMVR slopes + RAVLT scores)

**Processing:**
- Compute RAVLT_Forgetting = RAV_T5Sc - RAV_DRSc
- Higher values indicate more forgetting (worse delayed recall relative to T5)
- Standardize all variables (z-scores) for correlation interpretation
- Variables: RAVLT_Forgetting_z, REMEMVR_Slope_z, RAV_T5Sc_z, RAV_DRSc_z
- Compute descriptive statistics for all variables
- Check for extreme outliers (>3 SD from mean)

**Output:**
- data/step02_forgetting_computed.csv (standardized analysis variables)

**Validation Requirement:**
Validation tools MUST be used after forgetting computation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_forgetting_computed.csv: N rows x 9 columns
- Original columns plus: RAVLT_Forgetting, RAVLT_Forgetting_z, REMEMVR_Slope_z, RAV_T5Sc_z, RAV_DRSc_z

*Value Ranges:*
- RAVLT_Forgetting in [-15, 15] (T5 minus delayed, can be negative if delayed > T5)
- All z-score variables approximately in [-3, 3] (standardized)
- Mean of z-scores approximately 0, SD approximately 1

*Data Quality:*
- No NaN values in computed variables
- RAVLT_Forgetting distribution reasonable (not all zero)
- Standardization successful (z-score properties)

*Log Validation:*
- Required pattern: "Forgetting index computed: mean=X.XX, SD=X.XX"
- Required pattern: "Standardization complete: all variables z-scored"
- Required pattern: "VALIDATION - PASS"
- Forbidden patterns: "ERROR", "division by zero", "NaN values"

**Expected Behavior on Validation Failure:**
Raise error with specific computation issue, log to logs/step02_compute_forgetting.log, check for data quality problems.

### Step 3: Bivariate Correlation Analysis
**Dependencies:** Step 2 (computed forgetting index)
**Complexity:** Medium (~10 minutes including bootstrap)

**Purpose:** Compute primary bivariate correlation between RAVLT forgetting and REMEMVR slope with confidence intervals

**Input:**
- data/step02_forgetting_computed.csv (standardized variables)

**Processing:**
- Compute Pearson correlation: r(RAVLT_Forgetting_z, REMEMVR_Slope_z)
- Extract correlation coefficient, confidence interval, sample size
- Bootstrap 95% confidence intervals:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - CI: Percentile method (2.5th, 97.5th percentiles)
- Compute significance tests:
  - Uncorrected p-value (standard α = 0.05)
  - Bonferroni-corrected p-value (α = 0.05/28 = 0.00179 for Chapter 7 family)
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Effect size interpretation using Cohen's guidelines (r: 0.10 small, 0.30 medium, 0.50 large)

**Output:**
- data/step03_bivariate_correlation.csv (correlation results with dual p-values)

**Validation Requirement:**
Validation tools MUST be used after bivariate correlation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_bivariate_correlation.csv: 1 row x 8 columns
- Columns: r, ci_lower, ci_upper, p_uncorrected, p_bonferroni, n, effect_size, bootstrap_iterations

*Value Ranges:*
- r in [-1, 1] (valid correlation range)
- p-values in [0, 1] (valid probability range)
- ci_lower < r < ci_upper (valid confidence interval)
- n approximately 95-100 (expected sample size)
- bootstrap_iterations = 1000 exactly

*Data Quality:*
- No NaN or infinite correlation values
- Bootstrap CI encompasses correlation estimate
- Both p-values present (Decision D068 compliance)

*Log Validation:*
- Required pattern: "Bivariate correlation computed: r=X.XXX"
- Required pattern: "Bootstrap complete: 1000 iterations, seed=42"
- Required pattern: "Dual p-values: uncorrected=X.XXX, bonferroni=X.XXX"
- Required pattern: "VALIDATION - PASS"
- Forbidden patterns: "ERROR", "FAIL", "correlation failed"

**Expected Behavior on Validation Failure:**
Raise error with specific correlation computation issue, log to logs/step03_bivariate_correlation.log, check for numerical problems.

### Step 4: Partial Correlation Analysis
**Dependencies:** Step 3 (bivariate correlation)
**Complexity:** Medium (~10 minutes including bootstrap)

**Purpose:** Compute partial correlation controlling for initial encoding levels (RAVLT T5 and REMEMVR intercept)

**Input:**
- data/step02_forgetting_computed.csv (standardized variables)
- Note: REMEMVR intercept from Ch5 analysis (if available) or use RAV_T5Sc as encoding proxy

**Processing:**
- Compute partial correlation: r(RAVLT_Forgetting_z, REMEMVR_Slope_z | RAV_T5Sc_z)
- Control variables: RAV_T5Sc_z (RAVLT initial encoding level)
- Additional control if available: REMEMVR_Intercept_z (from Ch5 analysis)
- Implementation: pingouin.partial_corr() or statsmodels regression residuals
- Bootstrap partial correlation:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - For each iteration: compute partial correlation on resampled data
  - CI: Percentile method (2.5th, 97.5th percentiles)
- Multiple comparison correction:
  - Within-RQ family: 2 main correlations (bivariate + partial)
  - Bonferroni: α = 0.05/2 = 0.025 within RQ, α = 0.00179 chapter-level
  - Report BOTH uncorrected AND corrected p-values (Decision D068)

**Output:**
- data/step04_partial_correlation.csv (partial correlation results with controls)

**Validation Requirement:**
Validation tools MUST be used after partial correlation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_partial_correlation.csv: 1 row x 10 columns
- Columns: partial_r, ci_lower, ci_upper, p_uncorrected, p_bonferroni, p_chapter, n, controls, effect_size, bootstrap_iterations

*Value Ranges:*
- partial_r in [-1, 1] (valid partial correlation range)
- p-values in [0, 1] (valid probability range)
- ci_lower < partial_r < ci_upper (valid confidence interval)
- n approximately 95-100 (expected sample size after controlling)

*Data Quality:*
- No NaN or infinite partial correlation values
- Bootstrap CI encompasses partial correlation estimate
- Control variables properly specified and applied
- Both within-RQ and chapter-level corrections present

*Log Validation:*
- Required pattern: "Partial correlation computed: r=X.XXX (controlling for: controls_list)"
- Required pattern: "Bootstrap complete: 1000 iterations, seed=42"
- Required pattern: "Dual corrections: within_RQ=X.XXX, chapter=X.XXX"
- Required pattern: "VALIDATION - PASS"
- Forbidden patterns: "ERROR", "FAIL", "partial correlation failed"

**Expected Behavior on Validation Failure:**
Raise error with specific partial correlation issue, log to logs/step04_partial_correlation.log, check control variable problems.

### Step 5: Assumption Validation and Diagnostics
**Dependencies:** Step 4 (partial correlation)
**Complexity:** Medium (~10 minutes including plots)

**Purpose:** Check correlation assumptions and identify outliers using standardized diagnostic procedures

**Input:**
- data/step02_forgetting_computed.csv (standardized variables)

**Processing:**
- Check correlation assumptions:
  - Linearity: Scatterplot visual inspection + correlation linearity
  - Normality: Shapiro-Wilk test on both variables
  - Homoscedasticity: Breusch-Pagan test on residuals (if applicable)
  - Independence: Design-based assumption (N=100 independent participants)
- Outlier detection:
  - Cook's Distance calculation for bivariate relationship
  - Threshold: D > 4/n = 4/100 = 0.04 for outlier flagging
  - Mahalanobis distance for multivariate outliers
  - Document outlier characteristics without removing
- Remedial actions if assumptions violated:
  - Normality p < 0.05: Report bootstrap CIs as primary (already computed)
  - Non-linearity detected: Add Spearman correlation as secondary analysis
  - Extreme outliers: Sensitivity analysis excluding outliers

**Output:**
- data/step05_assumption_diagnostics.csv (test results and outlier flags)
- data/step05_diagnostic_plot_data.csv (scatterplot coordinates for plotting)

**Validation Requirement:**
Validation tools MUST be used after assumption diagnostic execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_assumption_diagnostics.csv: multiple rows x 6 columns
- Rows for: normality_ravlt, normality_rememvr, linearity_check, outlier_summary
- Columns: test, statistic, p_value, threshold, result, interpretation
- data/step05_diagnostic_plot_data.csv: N rows x 6 columns for scatterplot

*Value Ranges:*
- test statistics: varies by test (W for Shapiro-Wilk, etc.)
- p_values in [0, 1] (valid probability range)
- Cook's D in [0, 1] typically (distance metric)
- Outlier flags: boolean (0/1)

*Data Quality:*
- All assumption tests completed successfully
- Outlier detection thresholds properly calculated
- No missing test results or diagnostics

*Log Validation:*
- Required pattern: "Assumption checks complete: linearity OK, normality"
- Required pattern: "Outlier detection: X participants flagged (Cook's D > 0.04)"
- Required pattern: "Diagnostic plots prepared for visualization"
- Required pattern: "VALIDATION - PASS"
- Forbidden patterns: "ERROR", "FAIL", "assumption check failed"

**Expected Behavior on Validation Failure:**
Raise error with specific diagnostic failure, log to logs/step05_assumption_diagnostics.log, investigate data distribution problems.

### Step 6: Cross-Validation and Sensitivity Analysis
**Dependencies:** Step 5 (assumption diagnostics)
**Complexity:** Medium (~15 minutes including resampling)

**Purpose:** Assess correlation stability through bootstrap cross-validation and sensitivity analyses

**Input:**
- data/step02_forgetting_computed.csv (standardized variables)
- data/step05_assumption_diagnostics.csv (outlier flags)

**Processing:**
- Implement 5-fold cross-validation:
  - Random seed: 42 for reproducibility
  - Shuffle: True (randomize before splitting)
  - For each fold: compute correlation on training set, evaluate stability
  - No stratification needed (regression context)
  - Report correlation stability across folds
- Bootstrap stability assessment:
  - Additional 1000 bootstrap iterations (seed: 42)
  - Track correlation distribution stability
  - Assess CI convergence and outlier sensitivity
- Sensitivity analyses:
  - Exclude outliers (Cook's D > 0.04): recompute bivariate and partial correlations
  - Pearson vs Spearman comparison if normality violated
  - Proportional forgetting alternative: (T5-Delayed)/T5 vs raw difference
- Flag overfitting if cross-validation correlation variance > 0.10

**Output:**
- data/step06_cross_validation.csv (fold-wise correlation results)
- data/step06_sensitivity_analysis.csv (outlier exclusion and alternative metrics)

**Validation Requirement:**
Validation tools MUST be used after cross-validation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_cross_validation.csv: 5 rows x 6 columns (one per fold)
- Columns: fold, training_n, test_n, correlation, ci_lower, ci_upper
- data/step06_sensitivity_analysis.csv: multiple rows x 8 columns (various analyses)

*Value Ranges:*
- correlations in [-1, 1] across all folds
- training_n approximately 80, test_n approximately 20 per fold
- Cross-fold correlation SD < 0.10 (stability check)

*Data Quality:*
- All 5 folds completed successfully
- Sensitivity analyses completed without errors
- Alternative metrics computed where applicable

*Log Validation:*
- Required pattern: "Cross-validation complete: 5 folds, mean r=X.XXX (SD=X.XXX)"
- Required pattern: "Sensitivity analysis: outlier exclusion, alternative metrics"
- Required pattern: "Overfitting check: correlation variance < 0.10"
- Required pattern: "VALIDATION - PASS"
- Forbidden patterns: "ERROR", "FAIL", "cross-validation failed"

**Expected Behavior on Validation Failure:**
Raise error with specific cross-validation issue, log to logs/step06_cross_validation.log, check fold generation problems.

### Step 7: Effect Size and Power Analysis
**Dependencies:** Step 6 (cross-validation)
**Complexity:** Medium (~10 minutes)

**Purpose:** Interpret effect sizes and conduct post-hoc power analysis for observed correlations

**Input:**
- data/step03_bivariate_correlation.csv (primary correlation)
- data/step04_partial_correlation.csv (partial correlation)

**Processing:**
- Effect size interpretation:
  - Apply Cohen's guidelines: r = 0.10 (small), 0.30 (medium), 0.50 (large)
  - Consider cross-domain context: different memory systems may limit correlation
  - Compare to encoding-encoding correlations (reference from other Ch7 RQs if available)
- Post-hoc power analysis:
  - Given: N approximately 100, observed effect size, alpha = 0.00179 (Chapter 7 correction)
  - Calculate: achieved power for observed correlation
  - Use: scipy.stats or statsmodels power calculation
  - Sensitivity: minimum detectable correlation at 80% power
- Theoretical significance assessment:
  - Practical importance for consolidation theory
  - Cross-time scale validation implications
  - Individual differences framework contribution

**Output:**
- data/step07_effect_size_power.csv (effect size classification and power analysis)

**Validation Requirement:**
Validation tools MUST be used after effect size and power analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_effect_size_power.csv: 2 rows x 8 columns (bivariate + partial)
- Columns: analysis_type, correlation, effect_size_category, cohen_classification, achieved_power, min_detectable_80power, practical_significance, theoretical_importance

*Value Ranges:*
- correlations in [-1, 1] (copied from previous steps)
- achieved_power in [0, 1] (power probability)
- min_detectable_80power approximately 0.25-0.30 for N=100, alpha=0.00179

*Data Quality:*
- Power calculations completed successfully
- Effect size categories assigned appropriately
- Both bivariate and partial analyses included

*Log Validation:*
- Required pattern: "Effect size analysis complete: bivariate=X (category), partial=Y (category)"
- Required pattern: "Power analysis: achieved=X.XX, minimum_detectable=X.XX"
- Required pattern: "VALIDATION - PASS"
- Forbidden patterns: "ERROR", "FAIL", "power calculation failed"

**Expected Behavior on Validation Failure:**
Raise error with specific power analysis issue, log to logs/step07_effect_size_power.log, check sample size or parameter problems.

### Step 8: Comprehensive Results Summary
**Dependencies:** Step 7 (effect size and power)
**Complexity:** Low (~5 minutes)

**Purpose:** Consolidate all analysis results into comprehensive summary with theoretical interpretation

**Input:**
- data/step03_bivariate_correlation.csv (primary results)
- data/step04_partial_correlation.csv (controlled results)
- data/step05_assumption_diagnostics.csv (validity checks)
- data/step06_sensitivity_analysis.csv (robustness assessment)
- data/step07_effect_size_power.csv (interpretation framework)

**Processing:**
- Consolidate key findings:
  - Primary result: bivariate correlation with 95% CI and dual p-values
  - Secondary result: partial correlation controlling for encoding
  - Assumption validity: diagnostic summary and remedial actions taken
  - Stability: cross-validation and sensitivity analysis summary
  - Interpretation: effect size classification and theoretical implications
- Format results for downstream use:
  - Statistical significance: both uncorrected and corrected (Decision D068)
  - Practical significance: effect size and confidence interval interpretation
  - Methodological notes: assumptions, outliers, limitations acknowledged
- Prepare for plotting: correlation data with scatterplot coordinates

**Output:**
- data/step08_comprehensive_summary.csv (final consolidated results)
- data/step08_plot_data_bivariate.csv (scatterplot data for rq_plots)
- data/step08_plot_data_partial.csv (partial correlation residual plot data)

**Validation Requirement:**
Validation tools MUST be used after comprehensive summary execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_comprehensive_summary.csv: 1 row x 15 columns (consolidated findings)
- data/step08_plot_data_bivariate.csv: N rows x 4 columns (x, y, outlier_flag, participant_id)
- data/step08_plot_data_partial.csv: N rows x 4 columns (residual plot coordinates)

*Value Ranges:*
- All correlations in [-1, 1] (consolidated from previous steps)
- All p-values in [0, 1] (dual reporting maintained)
- Plot coordinates: standardized z-scores approximately in [-3, 3]

*Data Quality:*
- All key results consolidated without missing values
- Plot data prepared with appropriate coordinates
- Statistical and practical significance properly interpreted

*Log Validation:*
- Required pattern: "Results consolidation complete: bivariate r=X.XXX, partial r=X.XXX"
- Required pattern: "Plot data prepared: bivariate (N=XX), partial residuals (N=XX)"
- Required pattern: "VALIDATION - PASS"
- Forbidden patterns: "ERROR", "FAIL", "consolidation failed"

**Expected Behavior on Validation Failure:**
Raise error with specific consolidation issue, log to logs/step08_comprehensive_summary.log, check data integration problems.

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (Ch5 requirement verification)
- data/step01_extracted_data.csv (merged REMEMVR slopes + RAVLT scores)
- data/step02_forgetting_computed.csv (standardized analysis variables)
- data/step03_bivariate_correlation.csv (primary correlation with bootstrap CIs)
- data/step04_partial_correlation.csv (encoding-controlled correlation)
- data/step05_assumption_diagnostics.csv (validity checks and outlier detection)
- data/step05_diagnostic_plot_data.csv (assumption diagnostic coordinates)
- data/step06_cross_validation.csv (5-fold stability assessment)
- data/step06_sensitivity_analysis.csv (outlier and metric sensitivity)
- data/step07_effect_size_power.csv (effect interpretation and power analysis)
- data/step08_comprehensive_summary.csv (consolidated final results)
- data/step08_plot_data_bivariate.csv (scatterplot coordinates for rq_plots)
- data/step08_plot_data_partial.csv (partial correlation residual plots)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_data.log
- logs/step02_compute_forgetting.log
- logs/step03_bivariate_correlation.log
- logs/step04_partial_correlation.log
- logs/step05_assumption_diagnostics.log
- logs/step06_cross_validation.log
- logs/step07_effect_size_power.log
- logs/step08_comprehensive_summary.log

### Plots (EMPTY until rq_plots runs)
Plot source data created in data/ folder:
- step05_diagnostic_plot_data.csv (assumption diagnostics)
- step08_plot_data_bivariate.csv (main correlation scatterplot)
- step08_plot_data_partial.csv (partial correlation residual plots)

### Results (EMPTY until rq_results runs)
summary.md will be created by rq_results using data/step08_comprehensive_summary.csv

---

## Expected Data Formats

### Step-to-Step Transformations
1. **Raw Data (Step 1):** Ch5 slopes + master.xlsx RAVLT → merged dataset
2. **Computed Variables (Step 2):** Raw scores → forgetting index + standardized variables
3. **Correlation Results (Steps 3-4):** Standardized variables → correlation coefficients + CIs + p-values
4. **Diagnostics (Step 5):** Variables → assumption tests + outlier detection
5. **Validation (Steps 6-7):** Correlations → stability + sensitivity + power assessment
6. **Summary (Step 8):** All components → consolidated results + plot data

### Column Naming Conventions
- **Identifiers:** UID (string, participant identifier)
- **Raw Variables:** RAV_T5Sc, RAV_DRSc, REMEMVR_Slope
- **Computed Variables:** RAVLT_Forgetting (raw), *_z (standardized versions)
- **Results:** r, ci_lower, ci_upper, p_uncorrected, p_bonferroni, p_chapter
- **Diagnostics:** test, statistic, p_value, threshold, result, interpretation
- **Plot Data:** x, y, outlier_flag, participant_id

### Data Type Constraints
- **Correlations:** float64, range [-1, 1], no NaN values
- **P-values:** float64, range [0, 1], dual reporting mandatory
- **Sample Sizes:** int64, range [95, 100], document any exclusions
- **Flags:** boolean (outlier_flag, complete_case)
- **IDs:** object/string (UID, test names)

---

## Cross-RQ Dependencies

**Dependency:** Ch5 5.1.1 (REMEMVR omnibus LMM analysis)

**Required Outputs:**
- Individual participant slope estimates from fitted LMM
- File sources (in priority order):
  1. results/ch5/5.1.1/data/step06_best_model.pkl (preferred)
  2. results/ch5/5.1.1/data/step04_lmm_input.csv (if slopes pre-computed)
  3. results/ch5/5.1.1/data/*slope*.csv (search pattern)

**Fallback Strategy:**
If Ch5 outputs not found, QUIT immediately with clear error message identifying missing dependency. Do not attempt to recompute slopes independently.

**Format Requirements:**
Expected slope data format: UID (string) + slope estimate (float, negative values for forgetting)

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
- **Output validation:** Dependency check completion
- **Value validation:** All required files found and accessible
- **Data validation:** Ch5 status confirmed as success
- **Log validation:** Clear pass/fail status with specific missing items if any

#### Step 1: Extract and Prepare Data
- **Output validation:** Merged dataset with expected dimensions (N≥95 x 5 columns)
- **Value validation:** REMEMVR slopes negative, RAVLT scores in valid ranges
- **Data validation:** <5% missing data per variable, no duplicate UIDs
- **Log validation:** Successful merge confirmation, missing data documentation

#### Step 2: Compute Forgetting Index
- **Output validation:** Forgetting index computed, standardized variables added
- **Value validation:** Z-scores have mean≈0, SD≈1, forgetting index reasonable range
- **Data validation:** No NaN values, standardization successful
- **Log validation:** Computation success, descriptive statistics reported

#### Step 3: Bivariate Correlation
- **Output validation:** Correlation results with bootstrap CIs and dual p-values
- **Value validation:** Correlation in [-1,1], p-values in [0,1], valid CI
- **Data validation:** Bootstrap completed 1000 iterations, seed=42 used
- **Log validation:** Correlation computed, bootstrap successful, dual p-values reported

#### Step 4: Partial Correlation
- **Output validation:** Partial correlation with controls specified
- **Value validation:** Partial correlation in [-1,1], controls properly applied
- **Data validation:** Multiple corrections computed, bootstrap CIs included
- **Log validation:** Partial correlation success, control variables documented

#### Step 5: Assumption Diagnostics
- **Output validation:** Diagnostic tests completed, outliers identified
- **Value validation:** Test statistics reasonable, thresholds properly calculated
- **Data validation:** All assumptions checked, outlier flags accurate
- **Log validation:** Diagnostic completion, assumption violations documented

#### Step 6: Cross-Validation and Sensitivity
- **Output validation:** Cross-validation folds completed, sensitivity analyses run
- **Value validation:** Fold correlations stable (SD<0.10), sensitivity results reasonable
- **Data validation:** All folds successful, alternative analyses completed
- **Log validation:** Cross-validation stability confirmed, sensitivity documented

#### Step 7: Effect Size and Power
- **Output validation:** Effect sizes classified, power analysis completed
- **Value validation:** Power calculations reasonable, effect size categories appropriate
- **Data validation:** Cohen's guidelines applied, minimum detectable effects computed
- **Log validation:** Effect size analysis success, power calculations documented

#### Step 8: Comprehensive Summary
- **Output validation:** Results consolidated, plot data prepared
- **Value validation:** All key findings integrated, no inconsistencies
- **Data validation:** Plot coordinates appropriate for visualization
- **Log validation:** Consolidation success, interpretation framework applied

---

## Summary

**Total Steps:** 9 (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** 45-60 minutes
**Cross-RQ Dependencies:** Ch5 5.1.1 omnibus LMM (REMEMVR slopes)
**Primary Outputs:** Bivariate and partial correlations with bootstrap CIs and dual p-values
**Validation Coverage:** 100% (all 9 steps have 4-layer validation requirements)

**Key Hypothesis:** Weak positive correlation (r≈0.15) between RAVLT forgetting (20-30 minute delay) and REMEMVR forgetting slope (6-day span), reflecting stable individual differences in consolidation efficiency across time scales.

**Critical Methodological Notes:**
- Decision D068 compliance: dual p-value reporting throughout
- Chapter 7 family-wise correction: α = 0.05/28 = 0.00179
- Bootstrap stability with seed=42 for reproducibility
- Cross-time scale limitation acknowledged in interpretation
- Encoding quality controls through partial correlation analysis

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan → creates 3_tools.yaml
3. rq_analysis reads plan + tools → creates 4_analysis.yaml
4. g_code reads analysis → generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent following v5.1 specifications