# Analysis Plan: RQ 7.5.2 - DASS Predict Memory Performance

**Research Question:** 7.5.2
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines whether psychological distress measures (DASS-21: Depression, Anxiety, Stress subscales) predict episodic memory performance as measured by mean theta scores across all WWW domains. The analysis uses multiple regression with hierarchical entry to test incremental variance explained by DASS subscales above and beyond demographic and cognitive controls.

**Pipeline:** Multiple Linear Regression with Hierarchical Entry and Cross-Validation
**Steps:** 8 total analysis steps (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** ~45 minutes (including bootstrap and CV)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Bonferroni family-wise correction (alpha = 0.00060 for 3 DASS predictors)
- Conservative multiple testing approach for Ch7

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies

**Dependencies:** Ch5 5.1.1 (theta_all scores)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 outputs exist before proceeding with DASS analysis

**Input:**
- results/ch5/5.1.1/status.yaml (verify rq_results: success)
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/theta_all_scores.csv
- Fallback: results/ch5/5.1.1/data/*theta*.csv
- data/cache/master.xlsx (DASS-21 and demographic data)

**Processing:**
- Check Ch5 5.1.1 completed successfully (status.yaml)
- Locate theta scores file (try multiple patterns)
- Verify file contains theta_all column and UID column
- Check master.xlsx accessibility
- Verify DASS columns exist: {UID}-DEM-X-DASS_Dep/Anx/Str
- Log all validation checks with pass/fail status

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- File size: >500 bytes (contains detailed validation log)

*Value Ranges:*
- Validation status: "PASS" or "FAIL" for each dependency
- File counts: positive integers for located files

*Data Quality:*
- All required dependencies validated (Ch5 output + master.xlsx)
- No missing critical files
- DASS columns verified present in master.xlsx

*Log Validation:*
- Required patterns: "Ch5 5.1.1 status: success", "theta file located", "DASS columns verified"
- Forbidden patterns: "ERROR", "FAIL", "not found", "missing"
- Acceptable warnings: "Alternative path used", "Pattern matching required"

**Expected Behavior on Validation Failure:**
If any dependency missing, quit immediately with specific error message and invoke g_debug.

### Step 1: Extract DASS-21 Subscale Scores

**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (~5 minutes)

**Purpose:** Extract Depression, Anxiety, and Stress subscale scores from master.xlsx

**Input:**
- data/cache/master.xlsx (DASS-21 raw data)

**Processing:**
- Load master.xlsx using pandas.read_excel
- Extract DASS subscale scores using tag patterns:
  - Depression: {UID}-DEM-X-DASS_Dep
  - Anxiety: {UID}-DEM-X-DASS_Anx
  - Stress: {UID}-DEM-X-DASS_Str
- Extract control variables:
  - Age: {UID}-DEM-X-Age
  - RAVLT Total: {UID}-COG-X-RAV-TotSc
- Convert to participant-level dataset (one row per UID)
- Check for missing data patterns
- Compute descriptive statistics (mean, SD, range, skewness)
- Check for floor/ceiling effects (>20% at min/max values)

**Output:**
- data/step01_dass_scores.csv (DASS subscales + demographics)

**Validation Requirement:**
Validation tools MUST be used after DASS extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_dass_scores.csv: ~97 rows x 6 columns
- Columns: UID, DASS_Dep, DASS_Anx, DASS_Str, Age, RAVLT_Total

*Value Ranges:*
- DASS subscales: 0 to 21 (DASS-21 scale range)
- Age: 18 to 85 (adult age range)
- RAVLT_Total: 0 to 75 (RAVLT scoring range)
- All values non-negative

*Data Quality:*
- Expected N: 90-100 participants (some missing DASS data expected)
- Missing data <10% per variable
- No duplicate UIDs
- DASS scores primarily in subclinical range (most <10)

*Log Validation:*
- Required patterns: "DASS scores extracted", "N = [90-100]", "Descriptives computed"
- Forbidden patterns: "ERROR", "invalid values", "negative scores"
- Acceptable warnings: "Missing data flagged", "Floor effects detected"

**Expected Behavior on Validation Failure:**
Log specific validation failure, attempt data cleaning if minor issues, quit if major data integrity problems.

### Step 2: Extract Mean Theta Scores

**Dependencies:** Step 0 (dependency validation)  
**Complexity:** Low (~5 minutes)

**Purpose:** Extract mean theta_all scores per participant from Ch5 5.1.1 results

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/theta_all_scores.csv
- Fallback: results/ch5/5.1.1/data/*theta*.csv

**Processing:**
- Load theta scores file using pandas.read_csv
- Verify contains required columns: UID, theta_all, SE
- Compute mean theta_all per participant across sessions/domains
- Handle any duplicate UID cases (average across sessions)
- Check theta score distribution (normality, outliers)
- Compute descriptive statistics for theta_all
- Flag participants with extreme theta values (>3 SD from mean)

**Output:**
- data/step02_theta_means.csv (mean theta_all per participant)

**Validation Requirement:**
Validation tools MUST be used after theta extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_theta_means.csv: ~100 rows x 3 columns
- Columns: UID, theta_all_mean, theta_all_se

*Value Ranges:*
- theta_all_mean: -3 to 3 (IRT ability scale range)
- theta_all_se: 0.1 to 1.0 (standard error range)
- No infinite or NaN values

*Data Quality:*
- Expected N: 95-105 participants
- All UIDs unique
- No missing theta values
- Distribution approximately normal (skewness <2)

*Log Validation:*
- Required patterns: "Theta scores loaded", "Mean computed per participant", "Distribution checked"
- Forbidden patterns: "ERROR", "NaN values", "infinite values"
- Acceptable warnings: "Outliers detected", "Slight skewness"

**Expected Behavior on Validation Failure:**
Log validation failure details, attempt outlier handling if needed, quit if data fundamentally corrupted.

### Step 3: Merge Analysis Dataset

**Dependencies:** Steps 1-2 (DASS + theta scores)
**Complexity:** Low (~5 minutes)

**Purpose:** Create complete analysis dataset by merging DASS scores with theta means

**Input:**
- data/step01_dass_scores.csv (DASS subscales + demographics)
- data/step02_theta_means.csv (mean theta scores)

**Processing:**
- Merge datasets on UID using pandas.merge (inner join)
- Check for unmatched participants
- Handle missing data using listwise deletion
- Compute final sample size
- Check merged dataset for completeness
- Compute correlation matrix for all variables
- Save complete case analysis dataset
- Log final sample characteristics

**Output:**
- data/step03_analysis_dataset.csv (merged complete case data)
- data/step03_correlation_matrix.csv (bivariate correlations)

**Validation Requirement:**
Validation tools MUST be used after dataset merging execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_analysis_dataset.csv: ~95 rows x 7 columns
- Columns: UID, DASS_Dep, DASS_Anx, DASS_Str, Age, RAVLT_Total, theta_all_mean
- data/step03_correlation_matrix.csv: 6 x 6 correlation matrix

*Value Ranges:*
- All variables within expected ranges from Steps 1-2
- Correlations: -1 to 1
- No missing values in final dataset

*Data Quality:*
- Final N: 90-100 (complete cases only)
- All participants have complete data
- Correlation matrix positive definite
- No perfect correlations (r != 1.0)

*Log Validation:*
- Required patterns: "Merge successful", "Complete cases: N = [90-100]", "Correlation matrix computed"
- Forbidden patterns: "ERROR", "merge failed", "missing values"
- Acceptable warnings: "Some participants dropped", "Moderate correlations detected"

**Expected Behavior on Validation Failure:**
Report merge issues, check for UID mismatches, quit if <80 complete cases available.

### Step 4: Hierarchical Multiple Regression

**Dependencies:** Step 3 (analysis dataset)
**Complexity:** Medium (~10 minutes including bootstrap)

**Purpose:** Test incremental variance in theta_all explained by DASS subscales above controls

**Input:**
- data/step03_analysis_dataset.csv (complete analysis dataset)

**Processing:**
- Fit hierarchical regression using statsmodels.api.OLS
- Model 1 (controls): theta_all ~ Age + RAVLT_Total
- Model 2 (full): theta_all ~ Age + RAVLT_Total + DASS_Dep + DASS_Anx + DASS_Str
- Compare models using F-test (statsmodels.stats.anova_lm)
- Extract R², adjusted R², F-statistics for both models
- Compute delta R² and significance test
- Bootstrap delta R² confidence interval:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Participant-level resampling with replacement
  - CI method: percentile (2.5th, 97.5th percentiles)
- Check model assumptions:
  - Independence: confirmed by design (cross-sectional)
  - Linearity: partial residual plots for each predictor
  - Homoscedasticity: Breusch-Pagan test
  - Normality: Shapiro-Wilk test on residuals
  - Multicollinearity: VIF for each predictor

**Output:**
- data/step04_hierarchical_regression.csv (model comparison results)
- data/step04_model_diagnostics.txt (assumption check results)

**Validation Requirement:**
Validation tools MUST be used after hierarchical regression execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_hierarchical_regression.csv: 2 rows x 8 columns
- Columns: model, r_squared, adj_r_squared, f_stat, p_value, delta_r2, delta_f, delta_p
- data/step04_model_diagnostics.txt: text file with assumption tests

*Value Ranges:*
- r_squared: 0 to 1
- adj_r_squared: 0 to r_squared
- f_stat: >0
- p_values: 0 to 1
- delta_r2: 0 to 1 (incremental R²)

*Data Quality:*
- Both models converged successfully
- VIF <5 for all predictors (multicollinearity check)
- Bootstrap completed 1000 iterations
- All F-statistics positive

*Log Validation:*
- Required patterns: "Model 1 fitted", "Model 2 fitted", "Bootstrap complete: 1000 iterations", "Assumptions checked"
- Forbidden patterns: "ERROR", "convergence failed", "singular matrix"
- Acceptable warnings: "Slight heteroscedasticity", "Minor assumption violations"

**Expected Behavior on Validation Failure:**
Check for multicollinearity issues, attempt robust standard errors if heteroscedasticity detected, quit if models fail to converge.

### Step 5: Individual DASS Predictor Analysis

**Dependencies:** Step 4 (hierarchical regression)
**Complexity:** Medium (~10 minutes including corrections)

**Purpose:** Analyze individual DASS predictor effects with multiple comparison corrections

**Input:**
- data/step03_analysis_dataset.csv (analysis data)
- data/step04_hierarchical_regression.csv (model results)

**Processing:**
- Extract individual predictor results from Model 2 (full model)
- For each DASS predictor (Depression, Anxiety, Stress):
  - Standardized beta coefficient
  - Standard error and 95% confidence interval
  - t-statistic and uncorrected p-value
  - Semi-partial correlation (sr²) for unique variance
- Multiple comparison corrections:
  - Family: Within-RQ DASS predictors (3 tests)
  - Bonferroni: alpha = 0.00179/3 = 0.00060 per test
  - FDR: Benjamini-Hochberg correction
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Bootstrap confidence intervals for beta coefficients:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Participant-level block bootstrap
  - CI method: percentile (2.5th, 97.5th percentiles)
- Effect size interpretation using Cohen's conventions
- Check for suppression effects (sign changes vs bivariate correlations)

**Output:**
- data/step05_individual_predictors.csv (predictor effects with dual p-values)
- data/step05_effect_sizes.csv (standardized effects and interpretations)

**Validation Requirement:**
Validation tools MUST be used after individual predictor analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_individual_predictors.csv: 3 rows x 10 columns
- Columns: predictor, beta, se, ci_lower, ci_upper, t_stat, p_uncorrected, p_bonferroni, p_fdr, sr_squared
- data/step05_effect_sizes.csv: 3 rows x 5 columns

*Value Ranges:*
- beta: -2 to 2 (standardized coefficients)
- se: >0 (positive standard errors)
- p_values: 0 to 1 (all three p-value types)
- sr_squared: 0 to 1 (unique variance explained)
- ci_lower < beta < ci_upper (valid confidence intervals)

*Data Quality:*
- All 3 DASS predictors present
- Bootstrap CIs contain point estimates
- Bonferroni p-values = uncorrected * 3 (when <1)
- FDR correction properly ordered by rank

*Log Validation:*
- Required patterns: "Individual effects extracted", "Multiple corrections applied", "Bootstrap CIs computed"
- Forbidden patterns: "ERROR", "invalid p-values", "CI inversion"
- Acceptable warnings: "All effects non-significant", "Small effect sizes"

**Expected Behavior on Validation Failure:**
Check bootstrap convergence, verify correction calculations, quit if fundamental statistical errors detected.

### Step 6: Cross-Validation Assessment

**Dependencies:** Step 5 (individual predictors)
**Complexity:** Medium (~10 minutes)

**Purpose:** Assess model generalizability and check for overfitting using k-fold cross-validation

**Input:**
- data/step03_analysis_dataset.csv (complete analysis dataset)

**Processing:**
- Implement 5-fold cross-validation using sklearn.model_selection.KFold
- Random seed: 42 for reproducibility
- Shuffle: True (randomize participants before splitting)
- Stratification: None (regression outcome)
- For each fold:
  - Fit both models (control and full) on training set (80%)
  - Evaluate on test set (20%)
  - Compute R² for both models on training and test sets
  - Calculate RMSE and MAE on test set
- Aggregate across folds:
  - Mean and SD of test set R² for both models
  - Mean and SD of training R² for comparison
  - Train-test gap = mean(train R²) - mean(test R²)
- Flag potential overfitting if train-test gap >0.10
- Compute 95% CI for cross-validated R² using t-distribution
- Compare CV performance of control vs full model

**Output:**
- data/step06_cross_validation.csv (k-fold CV results)
- data/step06_cv_summary.txt (overfitting assessment)

**Validation Requirement:**
Validation tools MUST be used after cross-validation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_cross_validation.csv: 10 rows x 6 columns (5 folds x 2 models)
- Columns: fold, model, train_r2, test_r2, test_rmse, test_mae
- data/step06_cv_summary.txt: text summary of overfitting assessment

*Value Ranges:*
- train_r2, test_r2: 0 to 1
- test_rmse: >0 (positive RMSE values)
- test_mae: >0 (positive MAE values)
- train_r2 >= test_r2 (expected pattern)

*Data Quality:*
- All 5 folds completed successfully
- Both models evaluated in each fold
- Train-test gap <0.20 (reasonable overfitting threshold)
- CV R² confidence intervals computed

*Log Validation:*
- Required patterns: "5-fold CV complete", "Mean test R² computed", "Overfitting check: PASS/FLAG"
- Forbidden patterns: "ERROR", "fold failed", "negative R²"
- Acceptable warnings: "Modest overfitting detected", "Wide confidence intervals"

**Expected Behavior on Validation Failure:**
Check fold completion, verify R² calculations, flag but continue if minor overfitting detected.

### Step 7: Power Analysis and Effect Size Assessment

**Dependencies:** Steps 4-6 (regression results and CV)
**Complexity:** Medium (~10 minutes)

**Purpose:** Conduct post-hoc power analysis and assess practical significance of findings

**Input:**
- data/step04_hierarchical_regression.csv (observed effect sizes)
- data/step05_individual_predictors.csv (individual effects)

**Processing:**
- Post-hoc power analysis for hierarchical regression:
  - Given: Final N (~95), 5 predictors, alpha = 0.00060 (Bonferroni corrected)
  - Calculate: Achieved power for observed delta R² using statsmodels.stats.power.ftest_power
  - Input: effect size f² = delta R²/(1 - R²_full), dfnum=3, dfden=N-6
- Sensitivity analysis:
  - Compute minimum detectable delta R² at 80% power
  - Compute minimum detectable individual beta at 80% power
- Individual predictor power:
  - Convert beta coefficients to Cohen's d equivalents
  - Calculate achieved power for each DASS predictor
- Effect size interpretation:
  - Cohen's conventions for r² (small: 0.01, medium: 0.13, large: 0.26)
  - Convert standardized betas to practical interpretation
  - Compare observed effects to meta-analytic benchmarks if available
- Null findings interpretation:
  - If power <0.80: acknowledge limitation
  - If power >=0.80: support for genuine null effects

**Output:**
- data/step07_power_analysis.csv (power calculations and effect sizes)
- data/step07_effect_interpretation.txt (practical significance assessment)

**Validation Requirement:**
Validation tools MUST be used after power analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_power_analysis.csv: 4 rows x 6 columns (overall + 3 predictors)
- Columns: test, effect_size, power, min_detectable_effect, cohen_interpretation, practical_significance
- data/step07_effect_interpretation.txt: text interpretation of findings

*Value Ranges:*
- effect_size: 0 to 1 (proportion of variance)
- power: 0 to 1 (probability)
- min_detectable_effect: >effect_size (sensitivity threshold)
- All values non-negative and finite

*Data Quality:*
- Power calculations completed for all tests
- Effect size interpretations provided
- Sensitivity analysis results reasonable
- Practical significance assessed

*Log Validation:*
- Required patterns: "Power analysis complete", "Effect sizes interpreted", "Sensitivity analysis done"
- Forbidden patterns: "ERROR", "power calculation failed", "invalid effect size"
- Acceptable warnings: "Low power detected", "Small effect sizes"

**Expected Behavior on Validation Failure:**
Check power calculation inputs, verify effect size computations, report warnings but continue if calculations reasonable.

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt
- data/step01_dass_scores.csv
- data/step02_theta_means.csv  
- data/step03_analysis_dataset.csv
- data/step03_correlation_matrix.csv
- data/step04_hierarchical_regression.csv
- data/step04_model_diagnostics.txt
- data/step05_individual_predictors.csv
- data/step05_effect_sizes.csv
- data/step06_cross_validation.csv
- data/step06_cv_summary.txt
- data/step07_power_analysis.csv
- data/step07_effect_interpretation.txt

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_dass.log
- logs/step02_extract_theta.log
- logs/step03_merge_dataset.log
- logs/step04_hierarchical_regression.log
- logs/step05_individual_predictors.log
- logs/step06_cross_validation.log
- logs/step07_power_analysis.log

### Plots (EMPTY until rq_plots runs)
- NOTE: Plot source CSVs created in data/ folder:
  - data/step04_*_plot_data.csv (diagnostic plots data)
  - data/step05_*_plot_data.csv (predictor effects plot data)

### Results (EMPTY until rq_results runs)
- NOTE: summary.md will be created by rq_results using above outputs

---

## Expected Data Formats

### Step-to-Step Transformations
1. Step 0: Validation only (no data transformation)
2. Step 1: Extract DASS scores -> wide format (1 row per UID, DASS subscales as columns)
3. Step 2: Extract theta means -> wide format (1 row per UID, mean theta)
4. Step 3: Merge -> wide format (1 row per UID, all variables)
5. Steps 4-7: Statistical analysis -> results in various formats (model summaries, effect tables)

### Column Naming Conventions
- UID: Participant identifier (consistent across all files)
- DASS_Dep, DASS_Anx, DASS_Str: DASS-21 subscale scores
- theta_all_mean: Mean theta score across sessions/domains
- Age, RAVLT_Total: Control variables
- Statistical outputs: standardized naming (beta, se, p_uncorrected, p_bonferroni, etc.)

### Data Type Constraints
- UID: string/object (non-nullable)
- DASS scores: float64 (0-21 range, nullable during extraction)
- theta_all_mean: float64 (-3 to 3 range, non-nullable in final dataset)
- Age: float64 (positive, non-nullable)
- Statistical results: float64 (ranges specified per step)

---

## Cross-RQ Dependencies

**Primary Dependency:** Ch5 5.1.1 (General omnibus analysis)
- **Required Output:** Mean theta_all scores per participant
- **File Patterns:** 
  - Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
  - Alternative: results/ch5/5.1.1/data/theta_all_scores.csv  
  - Fallback: results/ch5/5.1.1/data/*theta*.csv
- **Expected Content:** UID column, theta_all column, SE column
- **Format Verification:** CSV format, ~100 rows, numeric theta values in [-3, 3] range
- **Failure Handling:** Step 0 validates dependency; quit with specific error if not found

**Secondary Dependency:** master.xlsx (always required)
- **Required Content:** DASS-21 subscale scores and demographics
- **Column Patterns:** {UID}-DEM-X-DASS_Dep/Anx/Str, {UID}-DEM-X-Age, {UID}-COG-X-RAV-TotSc
- **Validation:** Step 0 checks column existence before extraction

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution. This is enforced through the 4-layer substance validation criteria specified for each step.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
**Validation Focus:** File existence, content verification, dependency completion status
**Critical Checks:** Ch5 5.1.1 status, theta file location, DASS columns in master.xlsx
**Failure Action:** Immediate quit with specific error if any dependency missing

#### Step 1: Extract DASS Scores  
**Validation Focus:** Data extraction accuracy, value ranges, missing data patterns
**Critical Checks:** DASS scores in 0-21 range, expected participant count, no negative values
**Failure Action:** Data cleaning if minor issues, quit if major integrity problems

#### Step 2: Extract Theta Scores
**Validation Focus:** Theta value validity, distribution characteristics, UID matching
**Critical Checks:** Theta values in [-3, 3] range, no NaN/infinite values, unique UIDs
**Failure Action:** Outlier flagging if extreme values, quit if fundamentally corrupted

#### Step 3: Merge Dataset
**Validation Focus:** Merge success, complete cases, correlation matrix validity  
**Critical Checks:** Final N >=80, no missing values, reasonable correlation magnitudes
**Failure Action:** Report merge issues, quit if insufficient complete cases

#### Step 4: Hierarchical Regression
**Validation Focus:** Model convergence, assumption checks, bootstrap completion
**Critical Checks:** VIF <5, model F-statistics positive, 1000 bootstrap iterations completed
**Failure Action:** Robust standard errors if assumptions violated, quit if convergence failed

#### Step 5: Individual Predictors
**Validation Focus:** Multiple comparison accuracy, bootstrap CI validity, effect size calculation
**Critical Checks:** Dual p-values computed, CIs contain point estimates, correction factors accurate
**Failure Action:** Recalculation if correction errors, quit if statistical errors detected

#### Step 6: Cross-Validation
**Validation Focus:** Fold completion, overfitting assessment, R² validity
**Critical Checks:** All 5 folds completed, train-test gap reasonable, positive R² values
**Failure Action:** Flag overfitting warnings, continue with caution if minor issues

#### Step 7: Power Analysis
**Validation Focus:** Power calculation accuracy, effect size interpretation, sensitivity analysis
**Critical Checks:** Power values in [0,1], effect sizes non-negative, interpretations reasonable
**Failure Action:** Warnings if low power, continue with limitations acknowledged

---

## Summary

**Total Steps:** 8 (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** ~45 minutes (including bootstrap, CV, and comprehensive diagnostics)
**Cross-RQ Dependencies:** Ch5 5.1.1 (theta_all scores)
**Primary Outputs:** Hierarchical regression results with comprehensive validation and effect size assessment
**Validation Coverage:** 100% (all 8 steps have 4-layer validation requirements)

**Key Hypothesis:** Small negative effects expected for all three DASS subscales predicting REMEMVR accuracy, with depression potentially showing strongest effect due to encoding motivation impairment.

**Critical Methodological Notes:**
- Extremely conservative multiple testing (alpha = 0.00060 per DASS predictor)
- Dual p-value reporting (Decision D068) for transparency
- Bootstrap confidence intervals for robust inference
- Cross-validation to assess generalizability  
- Comprehensive assumption checking with specified remedial actions
- Post-hoc power analysis for null findings interpretation
- Expected null findings due to subclinical sample characteristics

**Statistical Implementation Specifications:**
- Random seed: 42 for all randomized procedures (bootstrap, CV)
- Bootstrap: 1000 iterations, participant-level resampling, percentile CIs
- Cross-validation: 5-fold, shuffled, train-test gap threshold <0.10
- Multiple comparisons: Bonferroni (primary) + FDR (secondary) corrections
- Power analysis: statsmodels.stats.power for regression F-tests
- Assumption violations: HC3 robust SEs for heteroscedasticity, bootstrap CIs for non-normality

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml  
4. g_code reads analysis -> generates executable code
5. rq_inspect validates outputs using substance criteria from this plan

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent v5.1.0
- Enhanced statistical specifications: CV, bootstrap, power, corrections, remedial actions
- Comprehensive 4-layer validation requirements for all 8 steps
- Conservative multiple testing approach appropriate for Ch7 context