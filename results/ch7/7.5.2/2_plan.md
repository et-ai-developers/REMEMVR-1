# Analysis Plan: RQ 7.5.2 - DASS predict memory performance

**Research Question:** 7.5.2
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This analysis examines whether psychological distress measures (DASS-21 subscales: Depression, Anxiety, Stress) predict REMEMVR episodic memory performance using hierarchical multiple regression with cross-validation. The approach tests incremental variance explained by DASS subscales above demographic and cognitive controls.

**Pipeline:** Multiple Linear Regression with Hierarchical Entry
**Steps:** 8 total analysis steps (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** 45 minutes total

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Bonferroni correction: alpha = 0.00179/3 = 0.00060 for 3 DASS predictors
- Cross-validation to prevent overfitting
- Bootstrap CIs for robust effect size estimates

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies

**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 5.1.1 outputs and master.xlsx exist before proceeding

**Input:**
- Primary: results/ch5/5.1.1/status.yaml (verify rq_results: success)
- Alternative: results/ch5/5.1.1/data/step03_theta_scores.csv
- Fallback: results/ch5/5.1.1/data/*theta*.{csv,txt,rds}
- Master file: data/cache/master.xlsx (DASS subscales and covariates)

**Processing:**
- Check Ch5 5.1.1 completed successfully (status = success)
- Locate theta_all scores file (try multiple file patterns)
- Verify master.xlsx contains required DASS columns
- Log all validation checks with specific patterns found
- QUIT if Ch5 5.1.1 incomplete or theta file not found

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- File should contain status checks for Ch5 and master.xlsx

*Value Ranges:*
- Not applicable (text validation file)

*Data Quality:*
- Required dependency paths documented
- Clear PASS/FAIL status for each dependency
- No missing critical files

*Log Validation:*
- Required patterns: "Ch5 5.1.1 status: success", "master.xlsx accessible"
- Required patterns: "theta file found", "DASS columns verified"
- Forbidden patterns: "ERROR", "not found", "missing"

**Expected Behavior on Validation Failure:**
- QUIT immediately if Ch5 5.1.1 not complete
- QUIT if theta file not found with fallback patterns
- Log specific missing dependencies to logs/step00_validate_dependencies.log

### Step 1: Extract and Merge Data

**Dependencies:** Step 0 (dependencies validated)
**Complexity:** Medium (~10 minutes)

**Purpose:** Extract theta_all scores from Ch5 5.1.1 and merge with DASS subscales from master.xlsx

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/*theta*.csv
- Master file: data/cache/master.xlsx
- Required columns in master.xlsx:
  - DASS_Dep: {UID}-DEM-X-DASS_Dep
  - DASS_Anx: {UID}-DEM-X-DASS_Anx  
  - DASS_Str: {UID}-DEM-X-DASS_Str
  - Age: {UID}-DEM-X-Age
  - RAVLT_Total: {UID}-COG-X-RAV-TotSc

**Processing:**
- Extract mean theta_all scores per participant from Ch5 5.1.1 output
- Load DASS subscales, Age, and RAVLT from master.xlsx using tag patterns
- Merge datasets on UID (inner join to keep only complete cases)
- Check for missing DASS data (expected N approximately 97)
- Compute completeness statistics per variable
- Document sample size after exclusions
- Create analysis-ready dataset with standardized column names
- Transform DASS scores to T-scores if needed (retain raw for interpretation)

**Output:**
- data/step01_analysis_dataset.csv (merged data with complete cases)
- data/step01_extraction_log.txt (sample size documentation)

**Validation Requirement:**
Validation tools MUST be used after data extraction and merging.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_analysis_dataset.csv: 95-100 rows x 7 columns
- Columns: UID, theta_all, DASS_Dep, DASS_Anx, DASS_Str, Age, RAVLT_Total
- data/step01_extraction_log.txt: text file with sample size documentation

*Value Ranges:*
- theta_all in [-3, 3] (IRT ability scale)
- DASS_Dep in [0, 42] (DASS depression subscale range)
- DASS_Anx in [0, 42] (DASS anxiety subscale range)
- DASS_Str in [0, 42] (DASS stress subscale range)
- Age in [18, 85] (adult participant range)
- RAVLT_Total in [15, 75] (RAVLT total score range)

*Data Quality:*
- Sample size 95-100 participants (allowing for some missing DASS)
- No duplicate UIDs
- All variables non-missing (complete cases only)
- DASS scores primarily in subclinical range (means < 10)

*Log Validation:*
- Required patterns: "Data merged successfully", "N = [0-9]+ complete cases"
- Required patterns: "DASS variables extracted", "theta_all loaded"
- Forbidden patterns: "ERROR", "merge failed", "excessive missing"

**Expected Behavior on Validation Failure:**
- If N < 90: Log warning but proceed (some DASS missing expected)
- If N < 80: QUIT with insufficient sample size error
- If merge fails: QUIT with data structure mismatch error
- Log to logs/step01_extract_merge_data.log

### Step 2: Descriptive Statistics and Data Exploration

**Dependencies:** Step 1 (analysis dataset created)
**Complexity:** Low (~5 minutes)

**Purpose:** Generate descriptive statistics for all variables and check distributional assumptions

**Input:**
- data/step01_analysis_dataset.csv

**Processing:**
- Compute descriptive statistics for all variables: Mean, SD, Min, Max, Median, IQR
- Check DASS subscale distributions for floor/ceiling effects
- Test normality: Shapiro-Wilk for theta_all (primary outcome)
- Compute correlations between all variables
- Flag any extreme values or distributional concerns
- Generate standardized z-scores for all predictors
- Document any transformations needed

**Output:**
- data/step02_descriptives.csv (summary statistics table)
- data/step02_correlations.csv (correlation matrix)
- data/step02_normality_tests.txt (distribution assessment)

**Validation Requirement:**
Validation tools MUST be used after descriptive analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_descriptives.csv: 7 rows x 8 columns (7 variables x 8 statistics)
- data/step02_correlations.csv: 7 x 7 correlation matrix
- data/step02_normality_tests.txt: text file with Shapiro-Wilk results

*Value Ranges:*
- DASS means in [0, 20] range (subclinical sample)
- theta_all mean approximately 0 (standardized ability)
- All correlations in [-1, 1] range
- Standard deviations > 0 for all variables

*Data Quality:*
- All 7 variables represented in descriptives
- Correlation matrix symmetric with 1.0 on diagonal
- No extreme outliers (values > 3 SD from mean)
- DASS subscales show expected positive intercorrelations

*Log Validation:*
- Required patterns: "Descriptives computed", "Correlations calculated"
- Required patterns: "Normality tested", "N = [0-9]+"
- Forbidden patterns: "ERROR", "computation failed", "missing data"

**Expected Behavior on Validation Failure:**
- If extreme outliers detected: Document but proceed
- If normality severely violated: Flag for bootstrap CIs in later steps
- Log detailed diagnostics to logs/step02_descriptives.log

### Step 3: Hierarchical Multiple Regression

**Dependencies:** Step 2 (descriptives completed)
**Complexity:** High (~10 minutes including bootstrap)

**Purpose:** Fit hierarchical regression testing incremental variance explained by DASS subscales

**Input:**
- data/step01_analysis_dataset.csv
- data/step02_descriptives.csv (for standardized predictors)

**Processing:**
- Standardize all predictors (z-scores) for beta interpretation
- Fit Model 1: theta_all ~ Age_z + RAVLT_z (control model)
- Fit Model 2: theta_all ~ Age_z + RAVLT_z + DASS_Dep_z + DASS_Anx_z + DASS_Str_z
- Test model comparison: F-test for ΔR² significance
- Implementation: statsmodels.api.OLS with standardized predictors
- Extract: R², adjusted R², F-statistic, ΔR² for model comparison
- Bootstrap 95% CIs for ΔR²:
  - Iterations: 1000
  - Seed: 42
  - Method: Participant-level resampling with replacement
  - CI: Percentile method (2.5th, 97.5th percentiles)
- Post-hoc power analysis for ΔR²:
  - Given: N=97, df1=3 (DASS predictors), df2=91, alpha=0.05
  - Calculate: power for observed ΔR² using statsmodels.stats.power
  - Report: actual power and minimum detectable effect at 80% power

**Output:**
- data/step03_hierarchical_models.csv (model comparison results)
- data/step03_model_bootstrap.csv (bootstrap CIs for ΔR²)

**Validation Requirement:**
Validation tools MUST be used after hierarchical regression.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_hierarchical_models.csv: 2 rows x 8 columns (Model1, Model2 results)
- Columns: model, R2, adj_R2, F_stat, df1, df2, p_value, delta_R2
- data/step03_model_bootstrap.csv: 1 row x 5 columns (ΔR² bootstrap results)

*Value Ranges:*
- R² in [0, 1] for both models
- Model2 R² >= Model1 R² (nested models)
- ΔR² in [0, 0.5] (realistic range for psychological predictors)
- F-statistics > 0
- p-values in [0, 1]

*Data Quality:*
- Both models converged successfully
- Model 2 has 5 predictors, Model 1 has 2 predictors
- Bootstrap CIs computed successfully (1000 iterations)
- Confidence intervals valid (ci_lower ≤ point_estimate ≤ ci_upper)

*Log Validation:*
- Required patterns: "Model 1 fitted: R2 = X.XXX"
- Required patterns: "Model 2 fitted: R2 = X.XXX"
- Required patterns: "Bootstrap complete: 1000 iterations"
- Forbidden patterns: "ERROR", "convergence failed", "singular matrix"

**Expected Behavior on Validation Failure:**
- If model convergence fails: Check for multicollinearity, retry without problematic predictors
- If bootstrap fails: Report parametric CIs as fallback
- Log model diagnostics to logs/step03_hierarchical_regression.log

### Step 4: Individual Predictor Analysis with Dual P-Values

**Dependencies:** Step 3 (hierarchical models fitted)
**Complexity:** High (~10 minutes including corrections)

**Purpose:** Extract individual DASS predictor effects with corrected and uncorrected p-values per Decision D068

**Input:**
- data/step01_analysis_dataset.csv
- data/step03_hierarchical_models.csv

**Processing:**
- Re-fit Model 2 to extract detailed coefficient information
- Extract for each DASS predictor (Dep, Anx, Str):
  - Standardized beta coefficient
  - Standard error
  - t-statistic
  - Semi-partial correlation (sr²) for unique variance
- Bootstrap 95% CIs for each beta coefficient:
  - Iterations: 1000
  - Seed: 42
  - Method: Participant-level resampling with replacement
  - CI: Percentile method (2.5th, 97.5th percentiles)
- Multiple comparison corrections:
  - Family: Within-RQ (3 DASS predictors)
  - Bonferroni: alpha = 0.00179/3 = 0.00060 per test
  - FDR: Benjamini-Hochberg procedure
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
  - Format: p_uncorrected, p_bonferroni, p_fdr
- Effect size interpretation:
  - Small effect: |β| > 0.10
  - Medium effect: |β| > 0.30
  - Large effect: |β| > 0.50

**Output:**
- data/step04_individual_predictors.csv (detailed coefficient results)
- data/step04_multiple_corrections.txt (correction calculations)

**Validation Requirement:**
Validation tools MUST be used after individual predictor analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_individual_predictors.csv: 3 rows x 10 columns (3 DASS predictors)
- Columns: predictor, beta, se, t_stat, sr2, ci_lower, ci_upper, p_uncorrected, p_bonferroni, p_fdr
- data/step04_multiple_corrections.txt: text file with correction details

*Value Ranges:*
- beta in [-1, 1] (standardized coefficients)
- se > 0 (positive standard errors)
- sr² in [0, 1] (squared semi-partial correlations)
- All p-values in [0, 1]
- Bootstrap CIs reasonable width (not excessively wide)

*Data Quality:*
- All 3 DASS predictors present (Depression, Anxiety, Stress)
- Bootstrap CIs valid (ci_lower < beta < ci_upper for most cases)
- Bonferroni p-values = uncorrected p-values × 3
- FDR p-values ≤ uncorrected p-values
- No NaN values in coefficients

*Log Validation:*
- Required patterns: "Individual predictors extracted"
- Required patterns: "Bootstrap CIs computed: 1000 iterations"
- Required patterns: "Multiple corrections applied"
- Forbidden patterns: "ERROR", "coefficient extraction failed"

**Expected Behavior on Validation Failure:**
- If bootstrap fails: Report parametric CIs as backup
- If corrections fail: Report uncorrected p-values with warning
- Log coefficient details to logs/step04_individual_predictors.log

### Step 5: Model Diagnostics and Assumption Checks

**Dependencies:** Step 4 (individual predictors analyzed)
**Complexity:** Medium (~8 minutes)

**Purpose:** Check regression assumptions and identify remedial actions if violated

**Input:**
- data/step01_analysis_dataset.csv
- Model 2 from hierarchical regression

**Processing:**
- Check multicollinearity: Compute VIF for each predictor
- Test residual normality: Shapiro-Wilk test on standardized residuals
- Test homoscedasticity: Breusch-Pagan test for constant variance
- Identify influential observations: Cook's Distance > 4/N threshold
- Generate diagnostic values:
  - Standardized residuals
  - Leverage values
  - Cook's Distance
  - DFBETAS for each coefficient
- Remedial actions based on violations:
  - Normality p < 0.05: Flag for bootstrap CIs (already computed)
  - Heteroscedasticity p < 0.05: Compute HC3 robust standard errors
  - VIF > 5: Document multicollinearity concern
  - VIF > 10: Consider dropping most collinear predictor
  - Cook's D > 4/N: Document influential observations

**Output:**
- data/step05_model_diagnostics.csv (VIF, tests, influential points)
- data/step05_residual_analysis.csv (residuals, leverage, Cook's D)
- data/step05_assumption_checks.txt (violation summary and remedial actions)

**Validation Requirement:**
Validation tools MUST be used after model diagnostics.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_model_diagnostics.csv: 5 rows x 3 columns (5 predictors with VIF values)
- data/step05_residual_analysis.csv: N rows x 5 columns (participant-level diagnostics)
- data/step05_assumption_checks.txt: text file with test results and remedial actions

*Value Ranges:*
- VIF in [1, 15] range (values > 10 indicate severe multicollinearity)
- Cook's D in [0, 1] range (values > 4/N = 0.04 flagged as influential)
- Standardized residuals approximately in [-3, 3] range
- Leverage values in [0, 1] range

*Data Quality:*
- All 5 predictors have VIF values computed
- Residual analysis includes all N participants
- Test p-values computed for normality and homoscedasticity
- Clear documentation of any assumption violations

*Log Validation:*
- Required patterns: "VIF computed for all predictors"
- Required patterns: "Residual normality tested", "Homoscedasticity tested"
- Required patterns: "Influential observations identified"
- Forbidden patterns: "ERROR", "diagnostic computation failed"

**Expected Behavior on Validation Failure:**
- If VIF computation fails: Check for perfect multicollinearity
- If assumption tests fail: Document but proceed with appropriate caveats
- Log diagnostic details to logs/step05_model_diagnostics.log

### Step 6: Cross-Validation Analysis

**Dependencies:** Step 5 (diagnostics completed)
**Complexity:** Medium (~7 minutes)

**Purpose:** Assess model generalizability and check for overfitting using k-fold cross-validation

**Input:**
- data/step01_analysis_dataset.csv

**Processing:**
- Implement 5-fold cross-validation using sklearn.model_selection.KFold
- Random seed: 42 for reproducibility
- Shuffle: True (randomize before splitting)
- Stratification: None for regression (use quantile-based if outcome extremely skewed)
- For each fold:
  - Fit Model 2 on training set (80% of data)
  - Evaluate on test set (20% of data)
  - Compute: R², RMSE, MAE
- Aggregate across folds:
  - Mean and standard deviation of each metric
  - Training vs test R² gap assessment
- Overfitting assessment:
  - Flag if mean(train R²) - mean(test R²) > 0.10
  - Compute generalization gap with 95% CI
- Compare CV R² to full model R² for consistency check

**Output:**
- data/step06_cross_validation.csv (fold-by-fold results)
- data/step06_cv_summary.csv (aggregated CV metrics)
- data/step06_generalization_assessment.txt (overfitting evaluation)

**Validation Requirement:**
Validation tools MUST be used after cross-validation analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_cross_validation.csv: 5 rows x 6 columns (5 folds × metrics)
- Columns: fold, train_R2, test_R2, train_RMSE, test_RMSE, test_MAE
- data/step06_cv_summary.csv: 3 rows x 4 columns (R²/RMSE/MAE summary stats)
- data/step06_generalization_assessment.txt: text file with overfitting evaluation

*Value Ranges:*
- All R² values in [0, 1] range
- RMSE values > 0 (positive root mean squared error)
- MAE values > 0 (positive mean absolute error)
- Train R² generally ≥ test R² (some overfitting expected)

*Data Quality:*
- All 5 folds completed successfully
- Test R² reasonably consistent across folds (SD < 0.05)
- Generalization gap < 0.10 (minimal overfitting)
- CV metrics consistent with full model results

*Log Validation:*
- Required patterns: "5-fold cross-validation complete"
- Required patterns: "Mean test R2 = X.XXX"
- Required patterns: "Generalization gap = X.XXX"
- Forbidden patterns: "ERROR", "fold failed", "convergence"

**Expected Behavior on Validation Failure:**
- If fold fails: Retry with different random seed, document issues
- If excessive overfitting: Acknowledge limitation, consider regularization
- Log CV details to logs/step06_cross_validation.log

### Step 7: Power Analysis and Sensitivity Assessment

**Dependencies:** Step 6 (cross-validation completed)
**Complexity:** Medium (~5 minutes)

**Purpose:** Conduct post-hoc power analysis and determine minimum detectable effect sizes

**Input:**
- data/step03_hierarchical_models.csv (observed effect sizes)
- Sample size N from analysis dataset

**Processing:**
- Post-hoc power analysis for hierarchical regression:
  - Given: N=97, df1=3 (DASS predictors), df2=91
  - Alpha level: 0.00060 (Bonferroni-corrected for Ch7)
  - Effect size: Observed ΔR² from Step 3
  - Use: statsmodels.stats.power.FTestAnovaPower()
- Calculate actual power for observed ΔR² effect
- Sensitivity analysis:
  - Minimum detectable ΔR² at 80% power given N=97
  - Minimum detectable β coefficient at 80% power
  - Sample size needed for small effect (ΔR² = 0.02) at 80% power
- Individual predictor power:
  - Cohen's f² for each DASS predictor
  - Power for each predictor given observed effect size
- Effect size interpretation using Cohen's conventions

**Output:**
- data/step07_power_analysis.csv (power calculations and sensitivity)
- data/step07_effect_sizes.csv (Cohen's f² for each predictor)
- data/step07_power_summary.txt (interpretation and recommendations)

**Validation Requirement:**
Validation tools MUST be used after power analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_power_analysis.csv: 4 rows x 5 columns (power calculations)
- data/step07_effect_sizes.csv: 3 rows x 4 columns (DASS predictor effect sizes)
- data/step07_power_summary.txt: text file with interpretation

*Value Ranges:*
- Power values in [0, 1] range
- Effect sizes (f²) ≥ 0
- Minimum detectable effects reasonable for psychological research
- Sample size recommendations > current N if underpowered

*Data Quality:*
- Power calculations completed for all relevant tests
- Effect size classifications provided (small/medium/large)
- Clear recommendations for interpretation given power limitations
- Sensitivity analysis provides actionable information

*Log Validation:*
- Required patterns: "Power analysis complete"
- Required patterns: "Observed power = X.XXX"
- Required patterns: "Minimum detectable effect = X.XXX"
- Forbidden patterns: "ERROR", "power calculation failed"

**Expected Behavior on Validation Failure:**
- If power calculation fails: Use alternative Cohen's conventions approach
- If underpowered: Acknowledge limitations in interpretation
- Log power analysis details to logs/step07_power_analysis.log

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt
- data/step01_analysis_dataset.csv
- data/step01_extraction_log.txt
- data/step02_descriptives.csv
- data/step02_correlations.csv
- data/step02_normality_tests.txt
- data/step03_hierarchical_models.csv
- data/step03_model_bootstrap.csv
- data/step04_individual_predictors.csv
- data/step04_multiple_corrections.txt
- data/step05_model_diagnostics.csv
- data/step05_residual_analysis.csv
- data/step05_assumption_checks.txt
- data/step06_cross_validation.csv
- data/step06_cv_summary.csv
- data/step06_generalization_assessment.txt
- data/step07_power_analysis.csv
- data/step07_effect_sizes.csv
- data/step07_power_summary.txt

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_merge_data.log
- logs/step02_descriptives.log
- logs/step03_hierarchical_regression.log
- logs/step04_individual_predictors.log
- logs/step05_model_diagnostics.log
- logs/step06_cross_validation.log
- logs/step07_power_analysis.log

### Plots (EMPTY until rq_plots runs)
- Plot source CSVs created in data/ with step##_*_plot_data.csv format

### Results (EMPTY until rq_results runs)
- summary.md will be created by rq_results agent

---

## Expected Data Formats

### Step-to-Step Transformations
1. Step 0->1: Dependency validation enables data extraction
2. Step 1->2: Raw merged data standardized for descriptives
3. Step 2->3: Descriptives inform hierarchical model setup
4. Step 3->4: Model objects enable individual predictor extraction
5. Step 4->5: Fitted models enable diagnostic computation
6. Step 5->6: Validated models ready for cross-validation
7. Step 6->7: CV results inform power analysis context

### Column Naming Conventions
- UID: Participant identifier (consistent across files)
- theta_all: Omnibus IRT ability estimate (outcome variable)
- DASS_Dep: Depression subscale raw score
- DASS_Anx: Anxiety subscale raw score  
- DASS_Str: Stress subscale raw score
- Age: Participant age (control variable)
- RAVLT_Total: RAVLT total score (cognitive control)
- Standardized versions: append "_z" suffix

### Data Type Constraints
- UID: string/object (non-nullable)
- All numeric variables: float64 (nullable only during intermediate processing)
- Statistical results: float64 with appropriate precision
- Text summaries: UTF-8 encoded strings

---

## Cross-RQ Dependencies

**Primary Dependency:**
- Ch5 5.1.1: Requires completion through Step 3 (IRT theta estimation)
- Critical files: theta_all scores aggregated across all domains
- Expected format: CSV with UID and theta_all columns

**Fallback Strategies:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/theta_all_scores.csv  
- Pattern: results/ch5/5.1.1/data/*theta*.csv
- Last resort: Regenerate from Ch5 5.1.1 if outputs missing

**Master Data Dependencies:**
- File: data/cache/master.xlsx
- Required columns: DASS subscales, Age, RAVLT total score
- Tag patterns documented in concept (e.g., {UID}-DEM-X-DASS_Dep)

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
[Full 4-layer validation structure as specified above]

#### Step 1: Extract and Merge Data
[Full 4-layer validation structure as specified above]

#### Step 2: Descriptive Statistics
[Full 4-layer validation structure as specified above]

#### Step 3: Hierarchical Regression
[Full 4-layer validation structure as specified above]

#### Step 4: Individual Predictors
[Full 4-layer validation structure as specified above]

#### Step 5: Model Diagnostics
[Full 4-layer validation structure as specified above]

#### Step 6: Cross-Validation
[Full 4-layer validation structure as specified above]

#### Step 7: Power Analysis
[Full 4-layer validation structure as specified above]

---

## Summary

**Total Steps:** 8 (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** 45 minutes
**Cross-RQ Dependencies:** Ch5 5.1.1 theta_all scores
**Primary Outputs:** Hierarchical regression results, individual predictor effects with dual p-values, model diagnostics, cross-validation metrics, power analysis

**Validation Coverage:** 100% (all 8 steps have 4-layer validation requirements)

**Key Hypothesis:** DASS subscales (Depression, Anxiety, Stress) will show small negative relationships with episodic memory performance, with Depression expected to have strongest effect due to encoding motivation impairment.

**Critical Methodological Notes:**
- Bonferroni correction extremely conservative (α = 0.00060) may reduce power
- Bootstrap CIs provide robust effect size estimates given potential non-normality
- Cross-validation essential to prevent overfitting with small expected effects
- Post-hoc power analysis critical for interpreting null findings
- Decision D068 dual p-value reporting ensures transparency in multiple testing

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent with v5.1 enhancements