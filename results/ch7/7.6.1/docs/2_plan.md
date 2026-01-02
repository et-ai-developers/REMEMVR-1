# Analysis Plan: RQ 7.6.1 - Cognitive Tests Predicting Individual Differences in Forgetting Rate

**Research Question:** 7.6.1
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This analysis tests whether traditional cognitive assessments (RAVLT, BVMT, RPM) predict individual differences in REMEMVR forgetting slopes, examining the theoretical hypothesis that cognitive tests predict encoding abilities (intercepts) but not consolidation processes (slopes). The analysis uses multiple regression with hierarchical entry, extensive diagnostics, cross-validation, and bootstrap procedures to comprehensively test the differential prediction hypothesis.

**Pipeline:** Multiple Linear Regression with Hierarchical Entry and Cross-Validation
**Steps:** 9 total analysis steps (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** ~45 minutes total

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Chapter 7 Bonferroni correction: alpha = 0.05/28 = 0.00179 for family-wise error control
- Standard multiple comparison corrections applied within RQ scope

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 5.1.4 outputs exist and master.xlsx is accessible before proceeding

**Input:**
- Primary: results/ch5/5.1.4/status.yaml (verify rq_results: success)
- Primary: results/ch5/5.1.4/data/step03_model_averaged_slopes.csv
- Alternative: results/ch5/5.1.4/data/*slope*.{csv,txt,rds}
- Fallback pattern: results/ch5/5.1.4/data/*model_avg*.{csv,txt,rds}
- Expected content: Per-participant slope estimates from model-averaged LMM
- Secondary: data/cache/master.xlsx (cognitive test scores)
- If Ch5 not found: QUIT with "Ch5 5.1.4 model-averaged outputs not found"
- If master.xlsx not found: QUIT with "master.xlsx cognitive data not accessible"

**Processing:**
- Check Ch5 5.1.4 completed successfully (status = success)
- Locate slope estimates file using multiple patterns
- Verify file contains UID and slope columns with N=100 participants
- Check master.xlsx accessibility and cognitive test columns (RAVLT_T, BVMT_T, RPM_T)
- Log all validation checks with success/failure status
- Document file paths found for subsequent steps

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Content: Ch5 status check, slope file location, master.xlsx access confirmation

*Value Ranges:*
- Ch5 status: must equal "success"
- Slope estimates: should exist for N=100 participants
- Cognitive columns: RAVLT_T, BVMT_T, RPM_T must be present

*Data Quality:*
- All required files accessible
- No permission errors
- File sizes reasonable (>1KB for slope data)

*Log Validation:*
- Required patterns: "Ch5 5.1.4 status: success", "Slope file located", "Cognitive data accessible"
- Forbidden patterns: "ERROR", "FAIL", "not found", "permission denied"

**Expected Behavior on Validation Failure:**
Raise error with specific missing dependency, log to logs/step00_validate_dependencies.log, quit immediately.

### Step 1: Extract and Prepare Cognitive Test Data
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (~5 minutes)

**Purpose:** Extract cognitive test scores (RAVLT_T, BVMT_T, RPM_T) from master.xlsx and prepare for analysis

**Input:**
- data/cache/master.xlsx (cognitive test sheet)
- Required columns: UID, RAVLT_T, BVMT_T, RPM_T

**Processing:**
- Load master.xlsx cognitive test data
- Extract UID and three cognitive test T-scores (already standardized)
- Check for missing data patterns and out-of-range values
- Verify T-scores are in reasonable range (T-scores typically 20-80)
- Compute basic descriptive statistics for each test
- Check for floor/ceiling effects in cognitive scores
- Document any participants with missing cognitive data
- Save clean cognitive dataset for merging

**Output:**
- data/step01_cognitive_tests.csv

**Validation Requirement:**
Validation tools MUST be used after cognitive data extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_cognitive_tests.csv: 100 rows × 4 columns
- Columns: UID (object), RAVLT_T (float64), BVMT_T (float64), RPM_T (float64)

*Value Ranges:*
- RAVLT_T in [20, 80] (typical T-score range)
- BVMT_T in [20, 80] (typical T-score range) 
- RPM_T in [20, 80] (typical T-score range)
- All T-scores > 0 (positive values required)

*Data Quality:*
- All 100 participants present (no missing UIDs)
- No duplicate UIDs
- Missing cognitive data < 10% per test (manageable attrition)
- No extreme outliers beyond 4 SDs from mean

*Log Validation:*
- Required patterns: "Cognitive data extracted: 100 participants", "T-scores in valid range"
- Forbidden patterns: "ERROR", "FAIL", "missing data >10%"

**Expected Behavior on Validation Failure:**
Raise error with specific data quality issue, log to logs/step01_extract_cognitive.log, invoke g_debug for data inspection.

### Step 2: Extract Model-Averaged Slopes from Ch5
**Dependencies:** Steps 0-1 (validation + cognitive data)
**Complexity:** Medium (~7 minutes)

**Purpose:** Extract per-participant slope estimates from Ch5 5.1.4 model-averaged forgetting trajectories

**Input:**
- Primary: results/ch5/5.1.4/data/step03_model_averaged_slopes.csv
- Alternative: results/ch5/5.1.4/data/*slope*.csv
- Fallback: Any file matching results/ch5/5.1.4/data/*model_avg*.csv
- Expected content: UID and slope estimate columns

**Processing:**
- Load model-averaged slope estimates from Ch5 5.1.4
- Identify slope column (may be named 'slope', 'random_slope', 'participant_slope')
- Verify N=100 participants match expected sample
- Compute descriptive statistics for slope distribution
- Check for extreme slope values (beyond ±3 SDs from mean)
- Verify slopes span reasonable range based on Ch5 ICC_slope = 21%
- Document any participants with extreme slope estimates
- Prepare slope data for merging with cognitive tests

**Output:**
- data/step02_slopes_extracted.csv

**Validation Requirement:**
Validation tools MUST be used after slope data extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_slopes_extracted.csv: 100 rows × 2 columns
- Columns: UID (object), slope (float64)

*Value Ranges:*
- slope in [-0.5, 0.5] (reasonable forgetting rate range)
- slope variance > 0 (individual differences exist)
- No NaN or infinite values

*Data Quality:*
- All 100 participants present
- No duplicate UIDs  
- Slope distribution approximately normal (Shapiro-Wilk p > 0.01)
- Standard deviation > 0.01 (meaningful individual differences)

*Log Validation:*
- Required patterns: "Slopes extracted: 100 participants", "Slope variance confirmed"
- Forbidden patterns: "ERROR", "FAIL", "no variance", "all identical"

**Expected Behavior on Validation Failure:**
Raise error with slope data quality issue, log to logs/step02_extract_slopes.log, invoke g_debug for data inspection.

### Step 3: Merge Data and Create Analysis Dataset
**Dependencies:** Steps 1-2 (cognitive tests + slopes)
**Complexity:** Low (~5 minutes)

**Purpose:** Merge cognitive test scores with slope estimates and prepare final analysis dataset

**Input:**
- data/step01_cognitive_tests.csv (T-scores)
- data/step02_slopes_extracted.csv (slope estimates)

**Processing:**
- Merge datasets on UID using inner join
- Verify complete data for N=100 participants
- Handle any missing data using listwise deletion
- Compute correlation matrix between all predictors
- Check for multicollinearity among cognitive tests (r > 0.90)
- Standardize predictors for regression (mean=0, SD=1)
- Create demographic variables if available (Age, Sex, Education)
- Document final sample characteristics
- Save analysis-ready dataset

**Output:**
- data/step03_analysis_input.csv

**Validation Requirement:**
Validation tools MUST be used after data merging.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_analysis_input.csv: 100 rows × 5+ columns
- Columns: UID (object), slope (float64), RAVLT_T_std (float64), BVMT_T_std (float64), RPM_T_std (float64), plus demographics if available

*Value Ranges:*
- slope in [-0.5, 0.5] (forgetting rate range)
- standardized predictors approximately mean=0, SD=1
- No missing values in analysis variables

*Data Quality:*
- Complete data for N=100 participants
- No participants excluded due to missing data
- Correlation matrix computed successfully
- Maximum correlation between predictors < 0.90 (acceptable multicollinearity)

*Log Validation:*
- Required patterns: "Data merged successfully: 100 complete cases", "Standardization complete"
- Forbidden patterns: "ERROR", "missing data", "exclusions"

**Expected Behavior on Validation Failure:**
Raise error with merging issue, log to logs/step03_merge_data.log, invoke g_debug for data inspection.

### Step 4: Hierarchical Multiple Regression Analysis
**Dependencies:** Step 3 (analysis dataset)
**Complexity:** High (~10 minutes including bootstrap)

**Purpose:** Fit hierarchical regression models to test incremental prediction of cognitive tests beyond demographics

**Input:**
- data/step03_analysis_input.csv (analysis dataset)

**Processing:**
- Model 1: Slope ~ Age + Sex + Education (if demographics available, otherwise intercept-only)
- Model 2: Slope ~ Age + Sex + Education + RAVLT_T_std + BVMT_T_std + RPM_T_std
- Fit both models using OLS regression
- Compute hierarchical F-test for Model 1 vs Model 2 (ΔR² significance)
- Extract standardized beta coefficients with standard errors
- Implementation: statsmodels.api.OLS with standardized predictors
- Bootstrap confidence intervals for all coefficients:
  - Iterations: 1000
  - Random seed: 42 for reproducibility  
  - Method: Participant-level resampling with replacement
  - CI: Percentile method (2.5th, 97.5th percentiles)
- Multiple comparison corrections:
  - Family: Within-RQ cognitive predictors (3 tests)
  - Bonferroni: alpha = 0.05/3 = 0.0167 per cognitive test
  - Also compute FDR-adjusted p-values using Benjamini-Hochberg
  - Report BOTH uncorrected AND corrected p-values (Decision D068)

**Output:**
- data/step04_hierarchical_regression.csv

**Validation Requirement:**
Validation tools MUST be used after hierarchical regression execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_hierarchical_regression.csv: 2 rows × 10 columns
- Columns: model, R_squared, adj_R_squared, F_stat, F_p, delta_R_squared, delta_F, delta_p, predictors_n, AIC
- Model rows: "Model1_Demographics", "Model2_Cognitive"

*Value Ranges:*
- R_squared in [0, 1] (proportion variance explained)
- adj_R_squared <= R_squared (adjusted version)
- F_stat > 0 (F-statistic positive)
- p-values in [0, 1] (valid probabilities)
- delta_R_squared >= 0 (incremental variance)

*Data Quality:*
- Both models fitted successfully
- Hierarchical F-test computed
- Bootstrap completed for all coefficients
- Dual p-values computed (uncorrected + corrected)

*Log Validation:*
- Required patterns: "Hierarchical models fitted", "Bootstrap complete: 1000 iterations", "Multiple corrections applied"
- Forbidden patterns: "ERROR", "convergence failed", "singular matrix"

**Expected Behavior on Validation Failure:**
Raise error with regression fitting issue, log to logs/step04_hierarchical_regression.log, invoke g_debug for model inspection.

### Step 5: Individual Predictor Analysis and Effect Sizes
**Dependencies:** Step 4 (hierarchical regression)
**Complexity:** Medium (~8 minutes)

**Purpose:** Extract individual predictor statistics, compute effect sizes, and conduct dominance analysis

**Input:**
- data/step04_hierarchical_regression.csv (model results)
- data/step03_analysis_input.csv (for predictor analysis)

**Processing:**
- Extract standardized beta coefficients for each cognitive test from Model 2
- Compute 95% confidence intervals using bootstrap results (1000 iterations, seed=42)
- Calculate semi-partial correlations (sr²) for unique variance contribution
- Compute Cohen's f² for overall model: f² = R²/(1-R²)
- Apply effect size interpretation: f² = 0.02 (small), 0.15 (medium), 0.35 (large)
- Dominance analysis to rank predictor importance:
  - Compute all possible subset models
  - Calculate average contribution across all model sizes
  - Rank predictors by dominance weights
- Multiple comparison corrections for individual predictors:
  - Bonferroni: p_corrected = p_uncorrected × 3
  - FDR: Benjamini-Hochberg procedure
  - Chapter-level correction: p_chapter = p_uncorrected × 28 (Ch7 total RQs)
- Report standardized effect sizes with practical interpretation

**Output:**
- data/step05_individual_predictors.csv
- data/step05_effect_sizes.csv

**Validation Requirement:**
Validation tools MUST be used after effect size analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_individual_predictors.csv: 3 rows × 8 columns
- Columns: predictor, beta_std, se, ci_lower, ci_upper, p_uncorrected, p_bonferroni, p_fdr
- data/step05_effect_sizes.csv: 1 row × 6 columns
- Columns: R_squared, adj_R_squared, cohens_f2, f2_interpretation, dominance_weights, sr2_sum

*Value Ranges:*
- beta_std in [-1, 1] (standardized coefficients)
- se > 0 (positive standard errors)
- ci_lower < beta_std < ci_upper (valid confidence intervals)
- p-values in [0, 1] (all correction levels)
- cohens_f2 >= 0 (effect size positive)

*Data Quality:*
- All 3 cognitive predictors analyzed
- Bootstrap CIs computed successfully
- Multiple correction methods applied
- Dominance analysis completed

*Log Validation:*
- Required patterns: "Effect sizes computed", "Dominance analysis complete", "Multiple corrections applied"
- Forbidden patterns: "ERROR", "FAIL", "invalid CI"

**Expected Behavior on Validation Failure:**
Raise error with effect size computation issue, log to logs/step05_effect_sizes.log, invoke g_debug for analysis inspection.

### Step 6: Comprehensive Model Diagnostics
**Dependencies:** Steps 4-5 (regression + predictors)
**Complexity:** Medium (~8 minutes)

**Purpose:** Comprehensive assumption checking for multiple regression with remedial actions if violated

**Input:**
- data/step03_analysis_input.csv (analysis dataset)
- Model 2 fitted object (cognitive predictors model)

**Processing:**
- Multicollinearity assessment:
  - Compute VIF (variance inflation factor) for each predictor
  - Threshold: VIF < 5 acceptable, VIF 5-10 concerning, VIF > 10 problematic
  - If VIF > 10: Consider ridge regression or predictor removal
- Residual normality:
  - Shapiro-Wilk test on standardized residuals
  - Q-Q plot visual inspection
  - If p < 0.05: Use bootstrap CIs as primary inference (already computed)
- Homoscedasticity:
  - Breusch-Pagan test for heteroscedasticity
  - Residual vs fitted plot inspection
  - If p < 0.05: Report HC3 heteroscedasticity-robust standard errors
- Linearity assessment:
  - Partial residual plots for each predictor
  - Visual inspection for non-linear patterns
  - Component-plus-residual plots
- Influential observations:
  - Cook's distance for each participant
  - Threshold: Cook's D > 4/N = 0.04 for N=100
  - If outliers present: Report results with and without influential cases
- Independence assumption:
  - Verify cross-sectional data structure (no clustering)
  - Document assumption satisfaction

**Output:**
- data/step06_model_diagnostics.csv
- data/step06_assumption_tests.csv

**Validation Requirement:**
Validation tools MUST be used after model diagnostics execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_model_diagnostics.csv: 100 rows × 5 columns
- Columns: UID, fitted_values, residuals, std_residuals, cooks_distance
- data/step06_assumption_tests.csv: 6 rows × 4 columns
- Columns: test_name, statistic, p_value, assumption_met

*Value Ranges:*
- fitted_values in [slope_min, slope_max] range
- residuals approximately mean=0
- std_residuals in [-3, 3] (standardized residuals)
- cooks_distance in [0, 1] (Cook's D range)
- p_values in [0, 1] for all tests

*Data Quality:*
- All 100 participants included in diagnostics
- All assumption tests completed
- VIF computed for each predictor
- Cook's distance identifies outliers if present

*Log Validation:*
- Required patterns: "Diagnostics complete", "VIF computed", "Assumption tests finished"
- Forbidden patterns: "ERROR", "FAIL", "infinite values"

**Expected Behavior on Validation Failure:**
Raise error with diagnostic computation issue, log to logs/step06_model_diagnostics.log, invoke g_debug for diagnostic inspection.

### Step 7: Cross-Validation and Overfitting Assessment
**Dependencies:** Steps 4-6 (regression + diagnostics)
**Complexity:** Medium (~7 minutes)

**Purpose:** Assess model generalizability using k-fold cross-validation and detect overfitting

**Input:**
- data/step03_analysis_input.csv (analysis dataset)
- Model 2 specification (cognitive predictors)

**Processing:**
- Implement 5-fold cross-validation using sklearn.model_selection.KFold
- Random seed: 42 for reproducibility
- Shuffle: True (randomize participants before splitting)
- Stratification: None for regression (use quantile-based if outcome skewed)
- For each fold:
  - Fit Model 2 on training data (80% of sample)
  - Predict slopes on test data (20% of sample) 
  - Compute test R², RMSE, MAE
- Aggregate cross-validation metrics:
  - Mean and standard deviation of R² across folds
  - Mean and standard deviation of RMSE and MAE
- Overfitting detection:
  - Compare training R² vs test R² across folds
  - Flag overfitting if mean gap > 0.10
  - Compute overfitting index: (train_R² - test_R²) / train_R²
- Generalizability assessment:
  - Test R² > 0 indicates some predictive validity
  - Test R² within 10% of training R² indicates good generalization

**Output:**
- data/step07_cross_validation.csv

**Validation Requirement:**
Validation tools MUST be used after cross-validation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_cross_validation.csv: 5 rows × 6 columns
- Columns: fold, train_R2, test_R2, RMSE, MAE, overfitting_gap

*Value Ranges:*
- train_R2 in [0, 1] (training R² bounds)
- test_R2 in [-1, 1] (test R² can be negative with poor fit)
- RMSE > 0 (positive root mean squared error)
- MAE > 0 (positive mean absolute error)
- overfitting_gap in [-1, 1] (difference metric)

*Data Quality:*
- All 5 folds completed successfully
- No fold with convergence failures
- Reasonable variation in metrics across folds
- Mean overfitting gap < 0.10 (acceptable generalization)

*Log Validation:*
- Required patterns: "Cross-validation complete: 5 folds", "Overfitting assessment finished"
- Forbidden patterns: "ERROR", "convergence failed", "fold failure"

**Expected Behavior on Validation Failure:**
Raise error with cross-validation issue, log to logs/step07_cross_validation.log, invoke g_debug for CV inspection.

### Step 8: Power Analysis and Sensitivity Testing
**Dependencies:** Steps 4-7 (complete regression analysis)
**Complexity:** Medium (~10 minutes)

**Purpose:** Conduct post-hoc power analysis and sensitivity testing for effect detection

**Input:**
- data/step04_hierarchical_regression.csv (observed effect sizes)
- Analysis parameters: N=100, predictors=6 (3 cognitive + 3 demographic), alpha=0.00179

**Processing:**
- Post-hoc power analysis for hierarchical regression:
  - Given: N=100, 6 predictors, alpha=0.00179 (Chapter 7 Bonferroni correction)
  - Calculate achieved power for observed R² using statsmodels.stats.power.FTestAnovaPower()
  - Report power for ΔR² (incremental cognitive prediction)
- Sensitivity analysis:
  - Minimum detectable effect size (Cohen's f²) at 80% power
  - Required sample size to detect f² = 0.10 (small-medium effect) at 80% power
  - Power curve: plot power vs effect size for current sample
- Effect size interpretation with power context:
  - If power < 0.80 for observed effects: acknowledge limitation
  - If power < 0.50: substantial risk of Type II error
- Alternative correction methods comparison:
  - Repeat power analysis with different alpha levels
  - Uncorrected alpha = 0.05: power for raw effects
  - FDR alpha = variable: power for discovery-based testing
  - Document impact of correction choice on power

**Output:**
- data/step08_power_analysis.csv

**Validation Requirement:**
Validation tools MUST be used after power analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_power_analysis.csv: 4 rows × 6 columns
- Columns: analysis_type, alpha_level, observed_effect, achieved_power, min_detectable_f2, required_N_80power

*Value Ranges:*
- alpha_level in (0, 1) (significance levels)
- observed_effect >= 0 (effect sizes non-negative)
- achieved_power in [0, 1] (power bounds)
- min_detectable_f2 > 0 (detectable effect size)
- required_N_80power > 0 (positive sample size)

*Data Quality:*
- All power calculations completed
- Multiple alpha levels analyzed
- Sensitivity thresholds computed
- Power interpretations provided

*Log Validation:*
- Required patterns: "Power analysis complete", "Sensitivity analysis finished", "Multiple alpha levels tested"
- Forbidden patterns: "ERROR", "invalid power", "computation failed"

**Expected Behavior on Validation Failure:**
Raise error with power computation issue, log to logs/step08_power_analysis.log, invoke g_debug for power inspection.

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (prerequisite verification)
- data/step01_cognitive_tests.csv (T-scores: RAVLT, BVMT, RPM)
- data/step02_slopes_extracted.csv (model-averaged slopes from Ch5)
- data/step03_analysis_input.csv (merged analysis dataset)
- data/step04_hierarchical_regression.csv (model comparison results)
- data/step05_individual_predictors.csv (coefficient table with dual p-values)
- data/step05_effect_sizes.csv (Cohen's f², dominance weights, sr²)
- data/step06_model_diagnostics.csv (residuals, Cook's D, fitted values)
- data/step06_assumption_tests.csv (VIF, normality, homoscedasticity tests)
- data/step07_cross_validation.csv (5-fold CV metrics and overfitting assessment)
- data/step08_power_analysis.csv (achieved power, sensitivity analysis)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_cognitive.log
- logs/step02_extract_slopes.log
- logs/step03_merge_data.log
- logs/step04_hierarchical_regression.log
- logs/step05_effect_sizes.log
- logs/step06_model_diagnostics.log
- logs/step07_cross_validation.log
- logs/step08_power_analysis.log

### Plots (EMPTY until rq_plots runs)
Plot source CSVs created in data/:
- data/step06_diagnostic_plots_data.csv (residual plots, Q-Q plots)
- data/step05_predictor_importance_plot_data.csv (dominance weights visualization)

### Results (EMPTY until rq_results runs)
Summary markdown file created by rq_results: results/summary.md

---

## Expected Data Formats

### Step-to-Step Transformations
1. Raw cognitive tests (master.xlsx) → standardized T-scores (step01)
2. Ch5 slopes → extracted participant slopes (step02)  
3. Separate datasets → merged analysis input (step03)
4. Analysis dataset → regression models and coefficients (step04)
5. Model results → effect sizes and predictor statistics (step05)
6. Fitted model → diagnostic metrics and assumption tests (step06)
7. Model specification → cross-validation metrics (step07)
8. Observed effects → power analysis and sensitivity (step08)

### Column Naming Conventions
- UID: Participant identifier (consistent across all files)
- slope: Outcome variable (forgetting rate from Ch5)
- *_T_std: Standardized cognitive test T-scores
- beta_std: Standardized regression coefficients
- p_uncorrected / p_bonferroni / p_fdr: Dual p-value reporting (Decision D068)
- ci_lower / ci_upper: Bootstrap confidence interval bounds
- R_squared / adj_R_squared: Model fit indices
- cohens_f2: Standardized effect size measure

### Data Type Constraints
- UID: string/object (no missing values)
- Continuous variables: float64 (slopes, T-scores, statistics)
- Logical/categorical: boolean or categorical where appropriate
- Missing data: explicitly coded as NaN, documented in validation

---

## Cross-RQ Dependencies

**Required Dependency:**
- Ch5 5.1.4 (Model-averaged forgetting trajectories) must complete successfully
- Specific requirement: Per-participant slope estimates from omnibus LMM analysis

**Expected Input Files:**
- Primary: results/ch5/5.1.4/data/step03_model_averaged_slopes.csv
- Alternative paths: results/ch5/5.1.4/data/*slope*.csv
- Fallback patterns: results/ch5/5.1.4/data/*model_avg*.{csv,txt,rds}

**Secondary Dependency:**
- master.xlsx cognitive test data (RAVLT_T, BVMT_T, RPM_T columns)

**Dependency Validation:**
- Step 0 validates all dependencies before analysis begins
- Circuit breaker: QUIT if Ch5 5.1.4 not successfully completed
- Circuit breaker: QUIT if cognitive test data not accessible

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
**Substance Validation Focus:** File accessibility and format verification
- Output Files: dependency validation text file with check results
- Value Ranges: Status values must indicate success/accessibility
- Data Quality: All required files present and readable
- Log Validation: Success patterns for each dependency check

#### Step 1: Extract Cognitive Data
**Substance Validation Focus:** T-score data quality and range validation
- Output Files: 100 × 4 cognitive test dataset with proper data types
- Value Ranges: T-scores in [20, 80] typical range, no extreme outliers
- Data Quality: Complete data, no missing UIDs, reasonable distributions
- Log Validation: Successful extraction with data quality confirmation

#### Step 2: Extract Slopes
**Substance Validation Focus:** Slope estimate quality and distribution
- Output Files: 100 × 2 slope dataset with variance confirmation
- Value Ranges: Slopes in reasonable forgetting rate range [-0.5, 0.5]
- Data Quality: Individual differences present (SD > 0.01), normal distribution
- Log Validation: Successful extraction with variance confirmation

#### Step 3: Merge Data
**Substance Validation Focus:** Complete case analysis and correlation structure
- Output Files: 100 × 5+ merged dataset ready for analysis
- Value Ranges: Standardized predictors with mean ≈ 0, SD ≈ 1
- Data Quality: No missing data, acceptable multicollinearity (r < 0.90)
- Log Validation: Successful merge with standardization completion

#### Step 4: Hierarchical Regression
**Substance Validation Focus:** Model fitting success and bootstrap completion
- Output Files: Model comparison table with hierarchical F-test results
- Value Ranges: R² in [0,1], valid F-statistics, proper p-value ranges
- Data Quality: Both models converged, bootstrap completed (1000 iterations)
- Log Validation: Model fitting success, bootstrap completion, corrections applied

#### Step 5: Effect Sizes
**Substance Validation Focus:** Effect size computation and multiple corrections
- Output Files: Predictor table + effect size summary with dual p-values
- Value Ranges: Standardized coefficients in [-1,1], valid confidence intervals
- Data Quality: All predictors analyzed, dominance analysis completed
- Log Validation: Effect computations successful, multiple corrections applied

#### Step 6: Model Diagnostics
**Substance Validation Focus:** Assumption test completion and diagnostic quality
- Output Files: Diagnostic metrics + assumption test results for all checks
- Value Ranges: VIF values computed, residuals standardized, Cook's D bounds
- Data Quality: All assumptions tested, outliers identified if present
- Log Validation: Diagnostic completion, assumption test success

#### Step 7: Cross-Validation
**Substance Validation Focus:** CV completion and overfitting assessment
- Output Files: 5-fold CV results with training/test metrics
- Value Ranges: R² values in valid bounds, positive error metrics
- Data Quality: All folds completed, overfitting gap < 0.10
- Log Validation: CV completion, overfitting assessment finished

#### Step 8: Power Analysis
**Substance Validation Focus:** Power computation and sensitivity analysis
- Output Files: Power analysis table with multiple alpha levels
- Value Ranges: Power in [0,1], positive effect sizes, valid sample sizes
- Data Quality: All power calculations completed, sensitivity thresholds set
- Log Validation: Power analysis complete, sensitivity analysis finished

---

## Summary

**Total Steps:** 9 (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** ~45 minutes total
**Cross-RQ Dependencies:** Ch5 5.1.4 (model-averaged slopes) + master.xlsx (cognitive tests)
**Primary Outputs:** Hierarchical regression results with comprehensive diagnostics
**Validation Coverage:** 100% (all 9 steps have 4-layer validation requirements)

**Key Hypothesis:** Traditional cognitive tests (RAVLT, BVMT, RPM) should NOT significantly predict REMEMVR forgetting slopes. Expected R² < 0.10 and non-significant hierarchical F-test (p > 0.00179).

**Critical Methodological Notes:**
- All randomized procedures use seed=42 for reproducibility
- Bootstrap confidence intervals (1000 iterations) for robust inference
- Comprehensive assumption checking with remedial actions specified
- Multiple comparison corrections at within-RQ and chapter levels
- Cross-validation to assess generalizability and overfitting
- Post-hoc power analysis to contextualize null findings
- Decision D068 compliance: dual p-value reporting throughout

**Statistical Implementation Enhancements:**
- Participant-level bootstrap resampling preserves data structure
- HC3 heteroscedasticity-robust standard errors if needed
- Ridge regression consideration for multicollinearity (VIF > 10)
- Comprehensive diagnostic plots for assumption verification
- Effect size interpretation with Cohen's f² benchmarks
- Sensitivity analysis for minimum detectable effects

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan → creates 3_tools.yaml
3. rq_analysis reads plan + tools → creates 4_analysis.yaml  
4. g_code reads analysis → generates executable code

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent v5.1.0
  - Enhanced statistical specifications with mandatory implementation details
  - Comprehensive validation requirements (4-layer structure)
  - Address rq_stats concerns: tool availability, remedial actions, power analysis
  - Cross-RQ dependency validation with fallback paths