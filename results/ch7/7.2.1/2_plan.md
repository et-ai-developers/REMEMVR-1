# Analysis Plan: RQ 7.2.1 - Age Moderation of Test-VR Relationship

**Research Question:** 7.2.1
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ tests whether age explains variance in REMEMVR performance beyond what cognitive tests predict. Uses hierarchical multiple regression with cross-validation to examine the VR scaffolding hypothesis - that contextual richness in VR compensates for age-related encoding deficits, leading to full mediation of age effects by cognitive ability.

**Pipeline:** Hierarchical Multiple Regression with Cross-Validation and Bootstrap Mediation Analysis
**Steps:** 11 total analysis steps (Step 0: validation + Steps 1-10: analysis)  
**Estimated Runtime:** 45-60 minutes

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Chapter 7 alpha correction: alpha = 0.05/28 = 0.00179 for family-wise error rate
- Bonferroni within-RQ: alpha = 0.05/4 = 0.0125 per predictor test
- Bootstrap resampling: seed=42, 1000 iterations, participant-level

**Key Enhancement:** Formal mediation analysis beyond hierarchical regression using proportion mediated and bootstrap confidence intervals

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies

**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 5.1.1 outputs and master.xlsx exist before proceeding

**Input:**
- Primary: results/ch5/5.1.1/status.yaml (verify rq_results: success)
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv (IRT theta_all estimates)
- Alternative: results/ch5/5.1.1/data/*theta*.csv (any theta output file)
- Fallback: results/ch5/5.1.1/data/*.csv (search all CSV files for theta data)
- Primary: data/cache/master.xlsx (cognitive test scores and demographics)
- Expected: Ch5 theta_all scores for 100 participants with columns UID, theta_all, SE

**Processing:**
- Check Ch5 5.1.1 status.yaml for rq_results: success
- Search for theta_all scores using multiple file patterns
- Verify master.xlsx contains RAVLT_T, BVMT_T, RPM_T, Age columns
- Log all validation checks with PASS/FAIL status
- If primary theta file missing: search alternatives and fallbacks
- If none found: QUIT with "Ch5 5.1.1 theta_all output not found"

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Expected structure: CH5_STATUS=PASS/FAIL, THETA_FILE=found/missing, MASTER_FILE=found/missing

*Value Ranges:*
- Status values: PASS or FAIL only
- File paths: valid absolute paths if found

*Data Quality:*
- All dependency checks logged (minimum 3: Ch5 status, theta file, master file)
- Clear PASS/FAIL determination for each dependency
- Full file paths recorded when files found

*Log Validation:*
- Required patterns: "Dependency validation complete", "Ch5 status: success"
- Required patterns: "Theta file located:", "Master file located:"
- Forbidden patterns: "ERROR", "File not found" (unless in fallback context)
- Acceptable warnings: "Using fallback file pattern"

**Expected Behavior on Validation Failure:**
Raise error with specific missing dependency, log to logs/step00_validate_dependencies.log, quit immediately and invoke g_debug.

---

### Step 1: Extract and Merge Data

**Dependencies:** Step 0 (dependency validation)
**Complexity:** Medium (~10 minutes)

**Purpose:** Extract theta_all scores from Ch5 and cognitive test scores from master.xlsx, merge into analysis dataset

**Input:**
- data/step00_dependency_validation.txt (file paths from Step 0)
- Ch5 5.1.1 theta_all scores (path from Step 0 validation)
- data/cache/master.xlsx (cognitive tests and demographics)

**Processing:**
- Load theta_all scores from Ch5 output file (columns: UID, theta_all, SE)
- Load cognitive tests from master.xlsx: RAVLT_T, BVMT_T, RPM_T (T-scores)
- Load demographics from master.xlsx: Age (continuous years)
- Verify 100 participants in both datasets
- Merge on UID with inner join (require complete data)
- Check for missing data: <5% missing allowed per variable
- Remove participants with any missing cognitive test scores
- Create standardized versions of all predictors (mean=0, sd=1)
- Random seed: 42 for any randomized procedures

**Output:**
- data/step01_analysis_dataset.csv (merged data for analysis)

**Validation Requirement:**
Validation tools MUST be used after data extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_analysis_dataset.csv: 100 rows x 7 columns minimum
- Columns: UID, theta_all, SE, Age, RAVLT_T, BVMT_T, RPM_T
- Additional: Age_std, RAVLT_T_std, BVMT_T_std, RPM_T_std (standardized versions)

*Value Ranges:*
- theta_all in [-3, 3] (IRT ability scale)
- SE in [0.1, 1.0] (positive standard errors)
- Age in [18, 85] (adult sample range)
- T-scores in [20, 80] (standardized cognitive test range)
- Standardized variables: approximately mean=0, sd=1

*Data Quality:*
- Exactly 100 participants (no exclusions due to missing data)
- No missing values in any column
- All UIDs unique (no duplicates)
- Merge successful: all UIDs from both datasets present

*Log Validation:*
- Required patterns: "Data merge complete: 100 participants"
- Required patterns: "Missing data check: 0% missing"
- Required patterns: "Standardization complete"
- Forbidden patterns: "ERROR", "Missing data >5%", "Merge failed"

**Expected Behavior on Validation Failure:**
Raise error with specific failure (missing data, merge failure, wrong dimensions), log to logs/step01_extract_merge_data.log, quit immediately and invoke g_debug.

---

### Step 2: Bivariate Correlations

**Dependencies:** Step 1 (merged analysis dataset)
**Complexity:** Low (~5 minutes)

**Purpose:** Compute correlation matrix for all variables, test bivariate relationships with uncorrected and corrected p-values

**Input:**
- data/step01_analysis_dataset.csv (merged data)

**Processing:**
- Compute Pearson correlations for all variable pairs
- Primary focus: r(Age, theta_all) - expect small negative correlation (r < -0.15)
- Secondary: r(Age, cognitive tests) - expect negative from literature
- Compute correlation matrix with 95% confidence intervals
- Bootstrap confidence intervals for correlations:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - CI: Percentile method (2.5th, 97.5th percentiles)
- Multiple comparison correction for correlation tests:
  - Family: Within-step correlation tests (6 correlations with theta_all)
  - Bonferroni: alpha = 0.05/6 = 0.0083 per test
  - Also compute FDR using Benjamini-Hochberg
  - Report BOTH uncorrected AND corrected p-values (Decision D068)

**Output:**
- data/step02_correlations.csv (correlation matrix with CIs and dual p-values)

**Validation Requirement:**
Validation tools MUST be used after correlation analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_correlations.csv: correlation results
- Structure: Variable1, Variable2, r, ci_lower, ci_upper, p_uncorrected, p_bonferroni, p_fdr

*Value Ranges:*
- Correlations in [-1, 1] (valid correlation range)
- p-values in [0, 1] (valid probability range)
- CIs: ci_lower < r < ci_upper (valid confidence interval)
- Age-theta correlation: expect r < -0.15 (theory prediction)

*Data Quality:*
- All correlation pairs computed (minimum 6 with theta_all)
- Bootstrap CIs computed for all correlations
- Dual p-values present for all tests (Decision D068)
- Bonferroni and FDR corrections applied

*Log Validation:*
- Required patterns: "Correlation analysis complete"
- Required patterns: "Bootstrap complete: 1000 iterations"
- Required patterns: "Multiple comparison correction applied"
- Forbidden patterns: "ERROR", "Failed to compute", "NaN correlation"

**Expected Behavior on Validation Failure:**
Raise error with specific correlation failure, log to logs/step02_bivariate_correlations.log, quit immediately and invoke g_debug.

---

### Step 3: Hierarchical Multiple Regression

**Dependencies:** Step 2 (correlations computed)
**Complexity:** Medium (~15 minutes including diagnostics)

**Purpose:** Fit hierarchical regression models to test age effects before and after controlling for cognitive tests

**Input:**
- data/step01_analysis_dataset.csv (standardized predictors)

**Processing:**
- Model 1: theta_all ~ Age_std (bivariate age effect)
- Model 2: theta_all ~ Age_std + RAVLT_T_std + BVMT_T_std + RPM_T_std (controlled age effect)
- Implementation: statsmodels.api.OLS with standardized predictors
- Extract for each model: R², adjusted R², F-statistic, beta coefficients with SEs
- Model comparison: Delta R² = R²_Model2 - R²_Model1
- F-test for model improvement: F_change with df1=3, df2=95
- Bootstrap 95% CIs for all regression coefficients:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - CI: Percentile method (2.5th, 97.5th percentiles)
- Multiple comparison correction within Model 2:
  - Family: Within-model predictor tests (4 predictors)
  - Bonferroni: alpha = 0.05/4 = 0.0125 per test
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Check statistical assumptions:
  - Normality: Shapiro-Wilk test on residuals
  - Homoscedasticity: Breusch-Pagan test
  - Multicollinearity: VIF for each predictor in Model 2
  - Outliers: Cook's D > 4/n threshold
- Remedial actions if violated:
  - Normality p < 0.05: Report bootstrap CIs as primary inference
  - Heteroscedasticity p < 0.05: Add HC3 robust standard errors
  - VIF > 5: Document multicollinearity, consider ridge if VIF > 10
  - Outliers Cook's D > 0.04: Report results with and without outliers

**Output:**
- data/step03_hierarchical_models.csv (model comparison results)
- data/step03_model_diagnostics.csv (assumption checks and remedial actions)

**Validation Requirement:**
Validation tools MUST be used after hierarchical regression execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_hierarchical_models.csv: 2 rows (Model 1, Model 2) x 8 columns minimum
- Columns: model, R2, R2_adj, F_stat, delta_R2, F_change, p_change, AIC
- data/step03_model_diagnostics.csv: assumption test results
- Columns: test, statistic, p_value, threshold, violated, remedial_action

*Value Ranges:*
- R² in [0, 1] (valid explained variance)
- F-statistics > 0 (valid test statistics)  
- p-values in [0, 1] (valid probabilities)
- VIF values: ideally < 5, flag if > 5
- Cook's D: flag if > 0.04 (4/100)

*Data Quality:*
- Model 1: 1 predictor (Age_std)
- Model 2: 4 predictors (Age_std + 3 cognitive tests)
- Bootstrap CIs computed for all coefficients
- All assumption tests completed
- Dual p-values for all coefficient tests (Decision D068)

*Log Validation:*
- Required patterns: "Model 1 fitted: R² = X.XX"
- Required patterns: "Model 2 fitted: R² = X.XX"
- Required patterns: "Bootstrap complete: 1000 iterations"
- Required patterns: "Assumption checks complete"
- Forbidden patterns: "ERROR", "Failed to converge", "Singular matrix"

**Expected Behavior on Validation Failure:**
Raise error with specific model failure (convergence, singularity, assumption violations), log to logs/step03_hierarchical_regression.log, quit immediately and invoke g_debug.

---

### Step 4: Formal Mediation Analysis

**Dependencies:** Step 3 (hierarchical models fitted)
**Complexity:** Medium (~10 minutes)

**Purpose:** Compute formal mediation statistics including proportion mediated and significance tests

**Input:**
- data/step03_hierarchical_models.csv (beta coefficients from both models)

**Processing:**
- Extract beta_Age from Model 1 (total effect = c path)
- Extract beta_Age from Model 2 (direct effect = c' path)
- Calculate mediation effect = beta_Age_Model1 - beta_Age_Model2
- Calculate proportion mediated = (c - c')/c = mediation_effect / beta_Age_Model1
- Bootstrap significance test for proportion mediated:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - For each iteration: fit both models, compute proportion mediated
  - 95% CI: percentile method (2.5th, 97.5th percentiles)
  - Mediation significant if CI excludes 0
- Effect size interpretation:
  - <0.25: Small mediation
  - 0.25-0.75: Medium mediation
  - >0.75: Large mediation
- Test mediation hypothesis: proportion mediated significantly > 0.50 (substantial mediation)

**Output:**
- data/step04_mediation_analysis.csv (mediation statistics with bootstrap CIs)

**Validation Requirement:**
Validation tools MUST be used after mediation analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_mediation_analysis.csv: 1 row x 8 columns
- Columns: beta_total, beta_direct, mediation_effect, proportion_mediated, ci_lower, ci_upper, p_mediation, effect_size_category

*Value Ranges:*
- Proportion mediated: can range (-inf, +inf) but expect [0, 1] for typical mediation
- Beta coefficients: standardized, typically [-1, 1]
- p-values in [0, 1] (valid probabilities)
- CIs: ci_lower < proportion_mediated < ci_upper

*Data Quality:*
- Single row with complete mediation statistics
- Bootstrap CI computed (1000 iterations)
- Effect size category assigned (small/medium/large)
- All calculations valid (no NaN or infinite values)

*Log Validation:*
- Required patterns: "Mediation analysis complete"
- Required patterns: "Proportion mediated = X.XX"
- Required patterns: "Bootstrap complete: 1000 iterations"
- Required patterns: "Effect size: small/medium/large"
- Forbidden patterns: "ERROR", "Division by zero", "NaN proportion"

**Expected Behavior on Validation Failure:**
Raise error with specific mediation calculation failure, log to logs/step04_mediation_analysis.log, quit immediately and invoke g_debug.

---

### Step 5: Cross-Validation Assessment

**Dependencies:** Step 3 (models fitted)
**Complexity:** Medium (~10 minutes)

**Purpose:** Assess model generalizability and check for overfitting using k-fold cross-validation

**Input:**
- data/step01_analysis_dataset.csv (full dataset for CV)

**Processing:**
- Implement 5-fold cross-validation using sklearn.model_selection.KFold
- Random seed: 42 for reproducibility
- Shuffle: True (randomize before splitting)
- Stratification: Use quantile-based stratification on theta_all (5 quantiles)
- For each fold:
  - Split: 80% training, 20% test
  - Fit Model 1 and Model 2 on training set
  - Evaluate on test set: compute R², RMSE, MAE
  - Store fold results
- Aggregate across folds: mean and SD for each metric
- Overfitting detection: train-test R² gap should be < 0.10
- Flag overfitting if train-test gap > 0.10 for either model
- Compare Model 1 vs Model 2 generalization performance
- Bootstrap confidence intervals for CV metrics:
  - Iterations: 1000 (resample fold results)
  - Random seed: 42
  - CI: percentile method for mean CV performance

**Output:**
- data/step05_cross_validation.csv (CV performance metrics with CIs)

**Validation Requirement:**
Validation tools MUST be used after cross-validation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_cross_validation.csv: 2 rows (Model 1, Model 2) x 12 columns
- Columns: model, cv_R2_mean, cv_R2_sd, cv_RMSE_mean, cv_RMSE_sd, cv_MAE_mean, cv_MAE_sd, train_R2, test_R2, overfitting_gap, overfitting_flag, ci_R2_lower, ci_R2_upper

*Value Ranges:*
- CV R² in [0, 1] (valid explained variance)
- RMSE > 0 (positive error metric)
- MAE > 0 (positive error metric)
- Overfitting gap: ideally < 0.10, flag if ≥ 0.10
- Standard deviations > 0 (positive variation)

*Data Quality:*
- Results for both models (2 rows)
- All 5 folds completed successfully
- CV metrics computed with bootstrap CIs
- Overfitting assessment completed
- No missing or invalid values

*Log Validation:*
- Required patterns: "5-fold CV complete"
- Required patterns: "Model 1 CV R² = X.XX ± X.XX"
- Required patterns: "Model 2 CV R² = X.XX ± X.XX"
- Required patterns: "Overfitting check: PASS/FLAG"
- Forbidden patterns: "ERROR", "Fold failed", "Invalid CV results"

**Expected Behavior on Validation Failure:**
Raise error with specific CV failure (fold error, invalid metrics), log to logs/step05_cross_validation.log, quit immediately and invoke g_debug.

---

### Step 6: Effect Size and Importance Analysis

**Dependencies:** Steps 3-4 (models and mediation)
**Complexity:** Low (~5 minutes)

**Purpose:** Compute comprehensive effect sizes and predictor importance measures

**Input:**
- data/step03_hierarchical_models.csv (model results)
- data/step04_mediation_analysis.csv (mediation statistics)

**Processing:**
- Cohen's f² for each model: f² = R²/(1-R²)
- Cohen's f² for model comparison: f²_change = ΔR²/(1-R²_Model2)
- Semi-partial correlations (sr²) for unique variance contribution of each predictor in Model 2
- Standardized beta coefficients with 95% bootstrap CIs (from Step 3)
- Predictor importance ranking based on |beta| in Model 2
- Effect size interpretations:
  - Cohen's f²: 0.02 small, 0.15 medium, 0.35 large
  - Semi-partial r²: proportion of unique variance explained
- Bootstrap confidence intervals for effect sizes:
  - Iterations: 1000 (from Step 3 bootstrap results)
  - Random seed: 42 consistency
  - All effect sizes with 95% CIs

**Output:**
- data/step06_effect_sizes.csv (comprehensive effect size summary)

**Validation Requirement:**
Validation tools MUST be used after effect size analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_effect_sizes.csv: 5 rows (1 for each predictor + model stats) x 8 columns
- Columns: predictor, beta, beta_ci_lower, beta_ci_upper, sr2, sr2_ci_lower, sr2_ci_upper, importance_rank

*Value Ranges:*
- Beta coefficients: standardized, typically [-1, 1]
- Semi-partial r² in [0, 1] (proportion of variance)
- Cohen's f² ≥ 0 (non-negative effect size)
- Importance ranks: integers 1-4 for Model 2 predictors

*Data Quality:*
- All 4 predictors from Model 2 included
- Bootstrap CIs computed for all effect sizes
- Importance ranking assigned (no ties, complete 1-4 ranking)
- Model-level statistics included (R², f²)

*Log Validation:*
- Required patterns: "Effect size analysis complete"
- Required patterns: "Predictor importance ranked"
- Required patterns: "Cohen's f² computed"
- Required patterns: "Semi-partial correlations computed"
- Forbidden patterns: "ERROR", "Ranking failed", "NaN effect size"

**Expected Behavior on Validation Failure:**
Raise error with specific effect size calculation failure, log to logs/step06_effect_sizes.log, quit immediately and invoke g_debug.

---

### Step 7: Power Analysis

**Dependencies:** Step 6 (effect sizes computed)
**Complexity:** Low (~5 minutes)

**Purpose:** Conduct post-hoc power analysis and assess sensitivity for detecting effects

**Input:**
- data/step06_effect_sizes.csv (observed effect sizes)

**Processing:**
- Post-hoc power analysis for hierarchical regression
- Given parameters: N=100, 4 predictors in Model 2, alpha=0.0125 (Bonferroni corrected)
- Calculate achieved power for observed effect sizes (Cohen's f²)
- Use: statsmodels.stats.power.FTestAnovaPower()
- Sensitivity analysis: minimum detectable f² at 80% power
- Power calculations for each predictor test (t-tests in regression)
- Power for model comparison (F-test for ΔR²)
- Mediation power assessment: N=100 limitations for small indirect effects
- Report actual power for observed effect sizes
- Flag if power < 0.80 for any critical test
- Acknowledge mediation power limitations (Fritz & MacKinnon, 2007: N=200+ recommended)

**Output:**
- data/step07_power_analysis.csv (power calculations and sensitivity analysis)

**Validation Requirement:**
Validation tools MUST be used after power analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_power_analysis.csv: multiple rows for different tests x 6 columns
- Columns: test_type, effect_size, power_achieved, power_adequate, min_detectable_effect, limitation_flag

*Value Ranges:*
- Power values in [0, 1] (valid probability range)
- Effect sizes ≥ 0 (non-negative)
- Minimum detectable effects > 0 (positive effect sizes)
- Power_adequate: TRUE/FALSE flags

*Data Quality:*
- Power computed for all major tests (model comparison, predictor tests, mediation)
- Sensitivity analysis completed (minimum detectable effects)
- Limitation flags assigned appropriately
- All calculations valid (no missing or infinite values)

*Log Validation:*
- Required patterns: "Power analysis complete"
- Required patterns: "Model power = X.XX"
- Required patterns: "Sensitivity analysis complete"
- Required patterns: "Mediation power limitation acknowledged"
- Forbidden patterns: "ERROR", "Power calculation failed", "Invalid parameters"

**Expected Behavior on Validation Failure:**
Raise error with specific power calculation failure, log to logs/step07_power_analysis.log, quit immediately and invoke g_debug.

---

### Step 8: Generate Plot Data

**Dependencies:** Steps 1-7 (all analyses complete)
**Complexity:** Low (~5 minutes)

**Purpose:** Create plot-ready datasets for visualization (actual plots generated later by rq_plots)

**Input:**
- data/step01_analysis_dataset.csv (raw data)
- data/step03_hierarchical_models.csv (model results)
- data/step04_mediation_analysis.csv (mediation results)
- data/step05_cross_validation.csv (CV results)

**Processing:**
- Create correlation heatmap data: correlation matrix with significance flags
- Create regression diagnostic plot data: residuals vs fitted, Q-Q plot data, Cook's D
- Create mediation visualization data: path diagram coordinates and effect sizes
- Create cross-validation plot data: train vs test performance across folds
- Create age effect visualization data: scatter plot with regression lines for Model 1 vs Model 2
- All plot data in CSV format with clearly labeled columns
- Include statistical annotations: R², p-values, effect sizes for plots

**Output:**
- data/step08_correlation_plot_data.csv (heatmap data)
- data/step08_diagnostic_plot_data.csv (residual plots)
- data/step08_mediation_plot_data.csv (path diagram)
- data/step08_cv_plot_data.csv (cross-validation results)
- data/step08_age_effect_plot_data.csv (age x VR relationship)

**Validation Requirement:**
Validation tools MUST be used after plot data generation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- 5 plot data CSV files as listed above
- Each file: appropriate dimensions for plot type
- Column headers clearly labeled for plotting
- Statistical annotations included where relevant

*Value Ranges:*
- All plot data within valid ranges for variables
- Coordinates: finite values, no NaN or infinite
- Statistical values: valid ranges (p in [0,1], R² in [0,1])

*Data Quality:*
- All 5 plot data files created successfully
- Complete data (no missing values in plot coordinates)
- Statistical annotations present
- Files ready for direct use by rq_plots agent

*Log Validation:*
- Required patterns: "Plot data generation complete"
- Required patterns: "5 plot datasets created"
- Required patterns: "Statistical annotations included"
- Forbidden patterns: "ERROR", "Plot data failed", "Missing coordinates"

**Expected Behavior on Validation Failure:**
Raise error with specific plot data failure, log to logs/step08_generate_plot_data.log, quit immediately and invoke g_debug.

---

### Step 9: Create Analysis Summary

**Dependencies:** Steps 1-8 (all analyses and plot data)
**Complexity:** Low (~5 minutes)

**Purpose:** Generate comprehensive summary of analysis results for thesis integration

**Input:**
- All analysis output files from Steps 1-8

**Processing:**
- Summarize key findings:
  - Bivariate age-VR relationship (correlation, significance)
  - Hierarchical regression results (Model 1 vs Model 2)
  - Mediation analysis (proportion mediated, significance)
  - Cross-validation performance (generalizability)
  - Power analysis (adequacy, limitations)
- Create interpretation based on VR scaffolding hypothesis
- Note any assumption violations and remedial actions taken
- Highlight dual p-value reporting compliance (Decision D068)
- Include statistical details: sample size, effect sizes, confidence intervals
- Format for thesis integration (clear, comprehensive prose)

**Output:**
- data/step09_analysis_summary.txt (comprehensive results summary)

**Validation Requirement:**
Validation tools MUST be used after summary generation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step09_analysis_summary.txt: comprehensive text summary
- Structure: Background, Methods, Results, Interpretation sections
- Length: substantive summary (minimum 50 lines)

*Value Ranges:*
- All statistical values cited correctly from analysis files
- P-values, effect sizes, CIs match source data exactly

*Data Quality:*
- Summary covers all major analyses (Steps 1-8)
- Interpretation addresses VR scaffolding hypothesis
- Dual p-value reporting mentioned (Decision D068 compliance)
- No statistical errors or inconsistencies

*Log Validation:*
- Required patterns: "Analysis summary complete"
- Required patterns: "VR scaffolding hypothesis addressed"
- Required patterns: "Decision D068 compliance noted"
- Forbidden patterns: "ERROR", "Summary failed", "Statistical inconsistency"

**Expected Behavior on Validation Failure:**
Raise error with specific summary generation failure, log to logs/step09_create_summary.log, quit immediately and invoke g_debug.

---

### Step 10: Final Validation and Archive

**Dependencies:** Steps 0-9 (complete analysis pipeline)
**Complexity:** Low (~5 minutes)

**Purpose:** Validate all analysis outputs and create archive-ready dataset

**Input:**
- All data files from Steps 0-9
- All log files from analysis execution

**Processing:**
- Validate file completeness: check all expected outputs exist
- Validate data integrity: spot-check key statistical results across files
- Create archive manifest: list all files with descriptions
- Verify reproducibility markers: all random seeds documented, bootstrap iterations confirmed
- Cross-check statistical consistency: ensure results align across files
- Generate execution report: success/failure for each step
- Create final status summary for rq_results integration

**Output:**
- data/step10_final_validation.txt (validation report)
- data/step10_archive_manifest.txt (file inventory)

**Validation Requirement:**
Validation tools MUST be used after final validation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step10_final_validation.txt: validation report
- data/step10_archive_manifest.txt: complete file inventory
- Both files: structured text with clear PASS/FAIL determinations

*Value Ranges:*
- Validation results: PASS or FAIL only
- File counts match expected output (minimum 20 data files)

*Data Quality:*
- All steps validated successfully
- Cross-file consistency confirmed
- Archive manifest complete
- No missing or corrupted outputs

*Log Validation:*
- Required patterns: "Final validation PASS"
- Required patterns: "Archive manifest complete"
- Required patterns: "Statistical consistency confirmed"
- Forbidden patterns: "ERROR", "FAIL", "Missing outputs", "Inconsistent results"

**Expected Behavior on Validation Failure:**
Raise error with specific validation failure, log to logs/step10_final_validation.log, quit immediately and invoke g_debug.

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)

**Step-by-Step Outputs:**
- data/step00_dependency_validation.txt: Prerequisite validation results
- data/step01_analysis_dataset.csv: Merged theta_all + cognitive tests + demographics (100 x 11)
- data/step02_correlations.csv: Correlation matrix with bootstrap CIs and dual p-values
- data/step03_hierarchical_models.csv: Model 1 and Model 2 comparison with diagnostics
- data/step03_model_diagnostics.csv: Assumption tests and remedial actions
- data/step04_mediation_analysis.csv: Formal mediation statistics with bootstrap CIs
- data/step05_cross_validation.csv: K-fold CV performance metrics
- data/step06_effect_sizes.csv: Comprehensive effect size analysis
- data/step07_power_analysis.csv: Power calculations and sensitivity analysis
- data/step08_correlation_plot_data.csv: Heatmap data for visualization
- data/step08_diagnostic_plot_data.csv: Residual plot data
- data/step08_mediation_plot_data.csv: Path diagram data
- data/step08_cv_plot_data.csv: Cross-validation visualization data
- data/step08_age_effect_plot_data.csv: Age x VR scatter plot data
- data/step09_analysis_summary.txt: Comprehensive results summary
- data/step10_final_validation.txt: Pipeline validation report
- data/step10_archive_manifest.txt: Complete file inventory

### Logs (ONLY execution logs)

- logs/step00_validate_dependencies.log
- logs/step01_extract_merge_data.log
- logs/step02_bivariate_correlations.log
- logs/step03_hierarchical_regression.log
- logs/step04_mediation_analysis.log
- logs/step05_cross_validation.log
- logs/step06_effect_sizes.log
- logs/step07_power_analysis.log
- logs/step08_generate_plot_data.log
- logs/step09_create_summary.log
- logs/step10_final_validation.log

### Plots (EMPTY until rq_plots runs)

Plot source data created in data/ folder:
- step08_correlation_plot_data.csv -> correlation heatmap
- step08_diagnostic_plot_data.csv -> regression diagnostics
- step08_mediation_plot_data.csv -> mediation path diagram
- step08_cv_plot_data.csv -> cross-validation performance
- step08_age_effect_plot_data.csv -> age moderation visualization

### Results (EMPTY until rq_results runs)

Summary results will be compiled by rq_results agent using:
- data/step09_analysis_summary.txt (primary text summary)
- All analysis outputs for integration

---

## Expected Data Formats

### Step-to-Step Transformations

1. **Ch5 5.1.1 theta_all** -> **Step 1** merged with cognitive tests -> **Step 2** correlation analysis
2. **Step 2** correlations -> **Step 3** hierarchical regression -> **Step 4** mediation analysis  
3. **Step 3** models -> **Step 5** cross-validation -> **Step 6** effect sizes
4. **Steps 1-7** -> **Step 8** plot data generation -> **Step 9** summary creation
5. **Steps 0-9** -> **Step 10** final validation and archiving

### Column Naming Conventions

- **UIDs:** UID (string, unique participant identifier)
- **Outcomes:** theta_all (continuous, IRT ability estimate)
- **Predictors:** Age_std, RAVLT_T_std, BVMT_T_std, RPM_T_std (standardized)
- **Statistics:** r, beta, SE, ci_lower, ci_upper, p_uncorrected, p_bonferroni, p_fdr
- **Model metrics:** R2, R2_adj, F_stat, AIC, delta_R2, F_change

### Data Type Constraints

- **Continuous variables:** float64, no missing values after Step 1
- **Categorical flags:** boolean (overfitting_flag, violation_flag)
- **P-values:** float64 in [0, 1] range
- **Effect sizes:** float64, non-negative for r², f²

---

## Cross-RQ Dependencies

**Primary Dependency:**
- **Source RQ:** Ch5 5.1.1 (Functional Form Comparison)
- **Required Status:** rq_results = success
- **Required Files:** theta_all scores for all 100 participants

**File Paths with Fallbacks:**
- **Primary:** results/ch5/5.1.1/data/step03_theta_scores.csv
- **Alternative:** results/ch5/5.1.1/data/*theta*.csv
- **Fallback:** results/ch5/5.1.1/data/*.csv (search for theta data)
- **Expected format:** UID, theta_all, SE columns

**Circuit Breaker:** If Ch5 5.1.1 not complete or theta files missing, QUIT Step 0 with error message.

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
- 4-layer validation ensuring Ch5 outputs and master.xlsx accessibility
- File path verification with multiple fallback options
- Status checking with clear PASS/FAIL determination

#### Steps 1-10: Analysis Pipeline
- Each step has comprehensive 4-layer validation criteria
- Output file validation (dimensions, columns, data types)
- Value range validation (statistical bounds, scientific validity)
- Data quality validation (completeness, consistency, accuracy)  
- Log validation (success patterns, error patterns, warnings)

**Validation Coverage:** 100% (all 11 steps have 4-layer validation requirements)

---

## Summary

**Total Steps:** 11 (Step 0: validation + Steps 1-10: analysis)
**Estimated Runtime:** 45-60 minutes
**Cross-RQ Dependencies:** Ch5 5.1.1 theta_all scores + master.xlsx cognitive tests  
**Primary Outputs:** Hierarchical regression with mediation analysis, cross-validation assessment, comprehensive effect sizes

**Key Hypothesis:** Age should NOT predict REMEMVR after controlling for cognitive tests, supporting VR scaffolding hypothesis

**Critical Methodological Notes:**
- Bootstrap confidence intervals with seed=42 for reproducibility (1000 iterations)
- 5-fold cross-validation with quantile stratification
- Dual p-value reporting (Decision D068): uncorrected + Bonferroni + FDR
- Formal mediation analysis beyond conceptual hierarchical regression  
- Comprehensive assumption checking with specified remedial actions
- Power analysis acknowledging N=100 limitations for mediation detection

**Statistical Implementation Requirements:**
- Random seed: 42 for ALL randomized procedures
- Bootstrap: 1000 iterations, participant-level resampling, percentile CIs
- Cross-validation: 5-fold, shuffle=True, quantile stratification, overfitting threshold <0.10
- Multiple comparisons: Bonferroni within-RQ (4 tests), dual p-value reporting
- Assumption violations: Specific remedial actions for normality, heteroscedasticity, multicollinearity

---

**Next Steps (Workflow):**
1. User reviews and approves this plan  
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent with enhanced v5.1 statistical specifications