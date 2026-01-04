# Analysis Plan: RQ 7.3.1 - Do Cognitive Tests Predict Confidence Trajectories?

**Research Question:** 7.3.1
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This analysis examines whether cognitive tests predict IRT-derived confidence theta scores using multiple regression with hierarchical entry. The approach tests metacognitive dissociation by comparing cognitive predictors of confidence versus accuracy (from RQ 7.1.1).

**Pipeline:** Multiple Linear Regression with Hierarchical Entry
**Steps:** 10 total analysis steps (Step 0: validation + Steps 1-9: analysis)  
**Estimated Runtime:** 45 minutes

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Chapter 7 Bonferroni correction: alpha = 0.05/28 = 0.00179
- Within-RQ correction: 3 cognitive tests = 0.00179/3 = 0.000597

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch6 outputs and master.xlsx exist before proceeding

**Input:**
- Primary: results/ch6/6.1.1/data/step03_confidence_theta_scores.csv
- Alternative: results/ch6/6.1.1/data/*confidence*theta*.csv
- Fallback: results/ch6/6.1.1/data/irt_*.csv (any IRT output files)
- Master data: data/cache/master.xlsx
- Expected: Ch6 6.1.1 confidence theta scores from IRT analysis
- If not found: QUIT with "Ch6 6.1.1 confidence theta output not found"

**Processing:**
- Check Ch6 6.1.1 status.yaml shows rq_results: success
- Locate confidence theta file (try multiple patterns)
- Verify file contains 100 participants with theta scores
- Check master.xlsx accessibility for cognitive tests
- Validate expected columns: UID, confidence_theta, se_theta
- Log all validation checks with timestamps

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Expected size: 500-1000 bytes (detailed validation log)

*Value Ranges:*
- N/A (text validation log only)

*Data Quality:*
- Must confirm Ch6 6.1.1 completion
- Must confirm confidence theta file exists
- Must confirm master.xlsx accessible
- All validation checks must pass

*Log Validation:*
- Required patterns: "DEPENDENCY CHECK COMPLETE", "Ch6 6.1.1 VALIDATED", "master.xlsx ACCESSIBLE"
- Forbidden patterns: "NOT FOUND", "FAILED", "ERROR"

**Expected Behavior on Validation Failure:**
- Log specific missing dependency
- Quit immediately with clear error message
- No further steps attempted

---

### Step 1: Extract Confidence Theta Scores
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (<5 minutes)

**Purpose:** Load and validate Ch6-derived confidence theta scores for N=100 participants

**Input:**
- results/ch6/6.1.1/data/step03_confidence_theta_scores.csv
- Expected columns: UID, confidence_theta, se_theta
- Expected N: 100 participants

**Processing:**
- Load confidence theta scores from Ch6 6.1.1
- Validate UID format (participant identifiers)
- Check theta score distribution (expected range: -3 to 3)
- Verify SE values are positive and reasonable (0.1 to 1.0)
- Check for missing values or duplicates
- Compute descriptive statistics (mean, SD, range)
- Flag any unusual values for review

**Output:**
- data/step01_confidence_theta.csv

**Validation Requirement:**
Validation tools MUST be used after confidence extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_confidence_theta.csv: 100 rows x 3 columns
- Columns: UID (object), confidence_theta (float64), se_theta (float64)

*Value Ranges:*
- confidence_theta in [-3, 3] (IRT theta scale)
- se_theta in [0.1, 1.0] (positive standard errors)
- All values finite (no NaN, inf)

*Data Quality:*
- Exactly 100 unique UIDs
- No missing values in key columns
- Mean confidence_theta approximately 0 (standardized scale)
- SE values reasonable for IRT estimation

*Log Validation:*
- Required: "Confidence theta loaded: 100 participants"
- Required: "Theta range validation PASS"
- Forbidden: "ERROR", "missing", "duplicate"

**Expected Behavior on Validation Failure:**
- Raise error with specific data quality issue
- Log to logs/step01_confidence_extraction.log
- Quit immediately, invoke g_debug

---

### Step 2: Extract Cognitive Test Scores
**Dependencies:** Step 0 (dependency validation)  
**Complexity:** Medium (~8 minutes)

**Purpose:** Extract cognitive test raw scores and convert to T-scores (M=50, SD=10)

**Input:**
- data/cache/master.xlsx (cognitive test raw scores)
- Required tests: RAVLT Total, BVMT Total, RPM Total
- Expected N: 100 participants

**Processing:**
- Load cognitive test data from dfnonvr.csv
- Extract RAVLT Total, BVMT Total, RPM Total scores
- Compute T-score transformations: T = 50 + 10*(raw - M_raw)/SD_raw
- Handle missing data: exclude participants missing any cognitive test
- Validate T-score distributions (should approximate M=50, SD=10)
- Check for extreme outliers (>3 SD from mean)
- Merge with demographic variables (Age, Sex, Education)

**Output:**
- data/step02_cognitive_tests.csv

**Validation Requirement:**
Validation tools MUST be used after cognitive test extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_cognitive_tests.csv: ~100 rows x 6 columns
- Columns: UID, RAVLT_T, BVMT_T, RPM_T, Age, Sex, Education

*Value Ranges:*
- RAVLT_T, BVMT_T, RPM_T in [20, 80] (T-score range)
- Age in [18, 85] (adult range)
- Sex in ["M", "F"] (binary coding)
- Education in [8, 25] (years of education)

*Data Quality:*
- At least 95 participants (allow 5% exclusion for missing data)
- T-score means approximately 50 (+/- 5)
- T-score SDs approximately 10 (+/- 3)
- No impossible values (negative T-scores)

*Log Validation:*
- Required: "T-scores computed for N=XX participants"
- Required: "T-score validation PASS"
- Forbidden: "ERROR", "transformation failed"

**Expected Behavior on Validation Failure:**
- Document specific T-score computation issues
- Log to logs/step02_cognitive_extraction.log
- If >5% missing data, flag for review but continue

---

### Step 3: Merge Analysis Dataset
**Dependencies:** Steps 1-2 (confidence + cognitive data)
**Complexity:** Low (<5 minutes)

**Purpose:** Merge confidence theta scores with cognitive tests and demographics

**Input:**
- data/step01_confidence_theta.csv
- data/step02_cognitive_tests.csv
- Merge key: UID

**Processing:**
- Inner join on UID (keep participants with both datasets)
- Verify final sample size (expected N >= 90 after exclusions)
- Check for any remaining missing values
- Compute correlation matrix for all variables
- Standardize continuous predictors for regression
- Create analysis-ready dataset with complete cases

**Output:**
- data/step03_analysis_dataset.csv

**Validation Requirement:**
Validation tools MUST be used after dataset merging.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_analysis_dataset.csv: ~95 rows x 7 columns
- Columns: UID, confidence_theta, RAVLT_T, BVMT_T, RPM_T, Age, Sex, Education

*Value Ranges:*
- Final N >= 90 (allowing reasonable exclusions)
- All values within expected ranges from previous steps
- No missing values in analysis variables

*Data Quality:*
- Successful merge of confidence and cognitive data
- Correlation matrix computable for all variables
- No extreme correlations (>0.95) suggesting data errors

*Log Validation:*
- Required: "Analysis dataset created: N=XX participants"
- Required: "Complete cases validation PASS"
- Forbidden: "merge failed", "missing values"

**Expected Behavior on Validation Failure:**
- Document merge issues or excessive exclusions
- Log to logs/step03_dataset_creation.log
- If final N < 90, flag for review but continue

---

### Step 4: Hierarchical Multiple Regression
**Dependencies:** Step 3 (analysis dataset)
**Complexity:** Medium (~10 minutes including bootstrap)

**Purpose:** Test incremental prediction of cognitive tests beyond demographics

**Input:**
- data/step03_analysis_dataset.csv
- Outcome: confidence_theta
- Block 1: Age, Sex, Education
- Block 2: + RAVLT_T, BVMT_T, RPM_T

**Processing:**
- Fit Model 1: confidence_theta ~ Age + Sex + Education
- Fit Model 2: confidence_theta ~ Age + Sex + Education + RAVLT_T + BVMT_T + RPM_T
- Extract R², adjusted R², F-statistics for both models
- Compute hierarchical F-test: F_change = (R²_2 - R²_1) / (1 - R²_2) * (N - p_2 - 1) / (p_2 - p_1)
- Bootstrap 95% CIs for R² values:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - CI: Percentile method (2.5th, 97.5th percentiles)
- Multiple comparison correction:
  - Family: Hierarchical model comparison (1 test)
  - Use uncorrected alpha = 0.05 for hierarchical F-test
  - Report significance and effect size (Cohen's f²)

**Output:**
- data/step04_hierarchical_models.csv

**Validation Requirement:**
Validation tools MUST be used after hierarchical regression.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_hierarchical_models.csv: 2 rows x 8 columns
- Columns: model, R_squared, adj_R_squared, F_stat, p_value, ci_lower, ci_upper, cohens_f2

*Value Ranges:*
- R_squared in [0, 1] (proportion variance)
- adj_R_squared in [0, 1], <= R_squared
- F_stat > 0 (F-statistics positive)
- p_value in [0, 1]
- cohens_f2 >= 0 (effect size)

*Data Quality:*
- Model 2 R² >= Model 1 R² (nested models)
- Bootstrap CIs bracket point estimates
- F-statistics match degrees of freedom

*Log Validation:*
- Required: "Hierarchical regression complete"
- Required: "Bootstrap CIs computed: 1000 iterations"
- Forbidden: "convergence failed", "ERROR"

**Expected Behavior on Validation Failure:**
- Document specific model fitting issues
- Log to logs/step04_hierarchical_regression.log
- If convergence issues, try alternative starting values

---

### Step 5: Individual Predictor Analysis
**Dependencies:** Step 4 (hierarchical models)
**Complexity:** High (~12 minutes including bootstrap and corrections)

**Purpose:** Examine individual cognitive test predictors with corrected significance tests

**Input:**
- data/step03_analysis_dataset.csv
- Focus on Model 2 coefficients

**Processing:**
- Extract standardized beta coefficients for all predictors
- Compute semi-partial correlations (sr²) for unique variance explained
- Bootstrap 95% CIs for coefficients:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - For each iteration: fit model, extract coefficients
  - CI: Percentile method (2.5th, 97.5th percentiles)
- Multiple comparison correction:
  - Family: Within-RQ cognitive tests (3 predictors)
  - Bonferroni: alpha = 0.00179/3 = 0.000597 per test
  - Also compute FDR using Benjamini-Hochberg
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
  - Format: p_uncorrected, p_bonferroni, p_fdr
- Check assumption violations:
  - Normality: Shapiro-Wilk test on residuals
  - Homoscedasticity: Breusch-Pagan test
  - Multicollinearity: VIF for each predictor
- Remedial actions if violated:
  - Normality p < 0.05: Report bootstrap CIs as primary
  - Heteroscedasticity p < 0.05: Add HC3 robust standard errors
  - VIF > 5: Document multicollinearity, consider ridge if VIF > 10
  - Outliers (Cook's D > 4/n): Report with/without outliers

**Output:**
- data/step05_individual_predictors.csv
- data/step05_assumption_diagnostics.txt

**Validation Requirement:**
Validation tools MUST be used after predictor analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_individual_predictors.csv: 6 rows x 10 columns
- Columns: predictor, beta, se, ci_lower, ci_upper, sr2, p_uncorrected, p_bonferroni, p_fdr, vif
- data/step05_assumption_diagnostics.txt: text file with test results

*Value Ranges:*
- beta in [-2, 2] (standardized coefficients reasonable)
- se > 0 (positive standard errors)
- p_values in [0, 1] for all three p-value types
- vif in [1, 10] (multicollinearity check)
- sr2 in [0, 1] (proportion variance)

*Data Quality:*
- All 6 predictors present (3 demographics + 3 cognitive)
- Bootstrap CIs valid (ci_lower < beta < ci_upper for most)
- Dual p-values present (Decision D068 compliance)
- VIF values reasonable (most < 5)

*Log Validation:*
- Required: "Individual predictors analyzed: 6 coefficients"
- Required: "Assumption checks complete"
- Required: "VALIDATION - PASS"
- Forbidden: "ERROR", "FAIL", "convergence"

**Expected Behavior on Validation Failure:**
- Document specific coefficient or assumption issues
- Log to logs/step05_predictor_analysis.log
- If assumption violations severe, note need for remedial analysis

---

### Step 6: Cross-Validation Analysis
**Dependencies:** Step 5 (predictor analysis)
**Complexity:** Medium (~8 minutes)

**Purpose:** Assess model generalizability using k-fold cross-validation

**Input:**
- data/step03_analysis_dataset.csv
- Model specification from Step 4 (Model 2)

**Processing:**
- Implement 5-fold cross-validation using sklearn.model_selection.KFold
- Random seed: 42 for reproducibility
- Shuffle: True (randomize before splitting)
- Stratification: None for regression (use quantile-based if outcome skewed)
- For each fold: fit model on training (80%), evaluate on test (20%)
- Compute metrics for each fold:
  - Test R² (primary metric)
  - RMSE (root mean squared error)
  - MAE (mean absolute error)
- Aggregate across folds: mean and standard deviation
- Compute mean and std of R² across folds
- Flag overfitting if train-test R² gap > 0.10
- Compare training R² with cross-validated R²

**Output:**
- data/step06_cross_validation.csv

**Validation Requirement:**
Validation tools MUST be used after cross-validation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_cross_validation.csv: 5 rows x 5 columns
- Columns: fold, train_R2, test_R2, rmse, mae

*Value Ranges:*
- train_R2, test_R2 in [0, 1] (R-squared bounds)
- rmse, mae > 0 (positive error metrics)
- test_R2 typically < train_R2 (expected pattern)

*Data Quality:*
- All 5 folds completed successfully
- Mean cross-validated R² within 15% of training R²
- No extreme outlier folds (>2 SD from mean)

*Log Validation:*
- Required: "Cross-validation complete: 5 folds"
- Required: "Mean CV R² = X.XXX"
- Forbidden: "fold failed", "convergence error"

**Expected Behavior on Validation Failure:**
- Document specific fold failures or extreme overfitting
- Log to logs/step06_cross_validation.log
- If CV R² << training R², flag overfitting concern

---

### Step 7: Effect Size Analysis
**Dependencies:** Steps 4-6 (models and validation)
**Complexity:** Medium (~8 minutes)

**Purpose:** Compute comprehensive effect size measures with bootstrap confidence intervals

**Input:**
- data/step04_hierarchical_models.csv
- data/step05_individual_predictors.csv

**Processing:**
- Extract R² from final model (Model 2)
- Compute Cohen's f² = R²/(1-R²) for overall model
- Extract semi-partial r² for each cognitive predictor
- Bootstrap 95% CIs for effect sizes:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - For each iteration: compute f² and sr² values
  - CI: Percentile method (2.5th, 97.5th percentiles)
- Compute relative importance using dominance analysis:
  - Compare all possible subset models
  - Rank predictors by average contribution across models
- Interpret effect sizes using Cohen's conventions:
  - f² small = 0.02, medium = 0.15, large = 0.35

**Output:**
- data/step07_effect_sizes.csv

**Validation Requirement:**
Validation tools MUST be used after effect size analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_effect_sizes.csv: 4 rows x 6 columns
- Columns: predictor, sr2, cohens_f2, ci_lower, ci_upper, importance_rank

*Value Ranges:*
- sr2 in [0, 1] (semi-partial correlations)
- cohens_f2 >= 0 (Cohen's f² non-negative)
- ci_lower <= sr2/cohens_f2 <= ci_upper (valid CIs)
- importance_rank in [1, 4] (rankings for 3 cognitive + overall)

*Data Quality:*
- Sum of sr² values <= total R² (mathematical constraint)
- Bootstrap CIs reasonable width (not degenerate)
- Effect size interpretations consistent with values

*Log Validation:*
- Required: "Effect sizes computed with bootstrap CIs"
- Required: "Dominance analysis complete"
- Forbidden: "computation error", "invalid values"

**Expected Behavior on Validation Failure:**
- Document specific effect size computation issues
- Log to logs/step07_effect_sizes.log
- If bootstrap fails, compute asymptotic CIs as fallback

---

### Step 8: Power Analysis
**Dependencies:** Step 7 (effect sizes)
**Complexity:** Medium (~6 minutes)

**Purpose:** Compute post-hoc power and sensitivity analysis for effect detection

**Input:**
- data/step07_effect_sizes.csv (observed effect sizes)
- Analysis parameters: N=~95, 6 predictors, alpha=0.000597

**Processing:**
- Post-hoc power analysis for hierarchical regression:
  - Given: N=95 (approx), 6 predictors, alpha=0.000597 (bonferroni corrected)
  - Calculate: power for observed Cohen's f² values
  - Use: statsmodels.stats.power.FTestAnovaPower()
  - Method: F-test power for multiple regression
- Sensitivity analysis:
  - Calculate: minimum detectable f² at 80% power
  - Calculate: minimum detectable sr² at 80% power for individual tests
- Report actual power for observed effect sizes
- If power < 0.80 for any test: acknowledge limitation in interpretation
- Compare with prospective power estimates (if available)

**Output:**
- data/step08_power_analysis.csv

**Validation Requirement:**
Validation tools MUST be used after power analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_power_analysis.csv: 4 rows x 6 columns
- Columns: test, observed_f2, power_observed, min_detectable_f2, power_80, alpha_used

*Value Ranges:*
- power_observed, power_80 in [0, 1] (power bounds)
- observed_f2, min_detectable_f2 >= 0 (effect sizes)
- alpha_used = 0.000597 (bonferroni correction)

*Data Quality:*
- Power calculations mathematically consistent
- Minimum detectable effects > observed if power < 80%
- Alpha level matches correction from Step 5

*Log Validation:*
- Required: "Power analysis complete for 4 tests"
- Required: "Sensitivity analysis complete"
- Forbidden: "power calculation failed"

**Expected Behavior on Validation Failure:**
- Document power computation issues
- Log to logs/step08_power_analysis.log
- If power functions fail, compute manual approximations

---

### Step 9: Compare with Accuracy Prediction
**Dependencies:** Step 8 (power analysis) + RQ 7.1.1 outputs
**Complexity:** High (~10 minutes including cross-RQ integration)

**Purpose:** Compare confidence prediction with accuracy prediction from RQ 7.1.1

**Input:**
- data/step07_effect_sizes.csv (confidence prediction results)
- Primary: results/ch7/7.1.1/data/step07_effect_sizes.csv
- Alternative: results/ch7/7.1.1/data/*effect*.csv
- Fallback pattern: results/ch7/7.1.1/data/*regression*.csv
- Expected content: R² and predictor effects for accuracy prediction
- If not found: QUIT with "Ch7 7.1.1 accuracy prediction results not found"

**Processing:**
- Load accuracy prediction results from RQ 7.1.1
- Extract comparable metrics: overall R², individual predictor sr²
- Compute difference scores: R²_confidence - R²_accuracy for overall model
- Compare individual predictor patterns:
  - RAVLT: sr²_confidence vs sr²_accuracy
  - BVMT: sr²_confidence vs sr²_accuracy
  - RPM: sr²_confidence vs sr²_accuracy
- Test statistical significance of differences (bootstrap difference CIs):
  - Bootstrap both datasets jointly (1000 iterations, seed=42)
  - Compute difference in sr² for each predictor
  - 95% CI for differences using percentile method
- Create comparative summary:
  - Which predictors show similar patterns vs different
  - Overall model comparison (confidence < accuracy expected)
  - Evidence for metacognitive dissociation

**Output:**
- data/step09_accuracy_comparison.csv

**Validation Requirement:**
Validation tools MUST be used after accuracy comparison.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step09_accuracy_comparison.csv: 4 rows x 8 columns
- Columns: predictor, sr2_confidence, sr2_accuracy, difference, ci_lower, ci_upper, pattern, evidence

*Value Ranges:*
- sr2_confidence, sr2_accuracy in [0, 1] (semi-partial correlations)
- difference in [-1, 1] (difference of proportions)
- ci_lower <= difference <= ci_upper (valid bootstrap CIs)

*Data Quality:*
- Successful merge with RQ 7.1.1 data
- Bootstrap difference CIs computed for all predictors
- Pattern classification reasonable (similar/different/unclear)

*Log Validation:*
- Required: "Accuracy comparison complete"
- Required: "Bootstrap difference CIs computed"
- Required: "Metacognitive dissociation analysis complete"
- Forbidden: "Ch7 7.1.1 not found", "merge failed"

**Expected Behavior on Validation Failure:**
- Document specific cross-RQ integration issues
- Log to logs/step09_accuracy_comparison.log
- If RQ 7.1.1 outputs missing, note limitation but complete other analyses

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (prerequisite checks)
- data/step01_confidence_theta.csv (Ch6-derived confidence scores)
- data/step02_cognitive_tests.csv (T-scored cognitive tests + demographics)
- data/step03_analysis_dataset.csv (merged complete cases)
- data/step04_hierarchical_models.csv (demographic vs cognitive models)
- data/step05_individual_predictors.csv (coefficients with dual p-values)
- data/step05_assumption_diagnostics.txt (normality, homoscedasticity, VIF)
- data/step06_cross_validation.csv (5-fold CV results)
- data/step07_effect_sizes.csv (Cohen's f², sr², dominance analysis)
- data/step08_power_analysis.csv (post-hoc power and sensitivity)
- data/step09_accuracy_comparison.csv (confidence vs accuracy predictors)

### Logs (ONLY execution logs)
- logs/step01_confidence_extraction.log
- logs/step02_cognitive_extraction.log
- logs/step03_dataset_creation.log
- logs/step04_hierarchical_regression.log
- logs/step05_predictor_analysis.log
- logs/step06_cross_validation.log
- logs/step07_effect_sizes.log
- logs/step08_power_analysis.log
- logs/step09_accuracy_comparison.log

### Plots (EMPTY until rq_plots runs)
- Note: Plot source CSVs will be created in data/ folder
- data/step05_diagnostic_plots_source.csv (for residual plots)
- data/step09_comparison_plots_source.csv (for confidence vs accuracy comparison)

### Results (EMPTY until rq_results runs)
- Note: summary.md will be created by rq_results

---

## Expected Data Formats

### Step-to-Step Transformations
1. Raw Ch6 confidence theta -> validated confidence scores
2. Raw master.xlsx cognitive tests -> T-scored standardized tests  
3. Separate datasets -> merged analysis-ready dataset
4. Analysis dataset -> hierarchical model comparison
5. Model coefficients -> individual predictor analysis with corrections
6. Final model -> cross-validation assessment
7. All results -> effect size quantification
8. Effect sizes -> power analysis for interpretation
9. Confidence results + accuracy results -> comparative analysis

### Column Naming Conventions
- **UIDs:** UID (participant identifier)
- **Outcomes:** confidence_theta (IRT-derived confidence score)
- **Predictors:** RAVLT_T, BVMT_T, RPM_T (T-scored cognitive tests)
- **Demographics:** Age, Sex, Education
- **Statistics:** beta, se, ci_lower, ci_upper, p_uncorrected, p_bonferroni, p_fdr
- **Effect sizes:** sr2 (semi-partial r²), cohens_f2 (Cohen's f²)

### Data Type Constraints
- **UIDs:** string/object (nullable=False)
- **Theta scores:** float64, range [-3, 3] (nullable=False)
- **T-scores:** float64, range [20, 80] (nullable=False)
- **Demographics:** Age (int), Sex (string), Education (int)
- **Statistics:** float64, positive for SE/CI widths
- **P-values:** float64, range [0, 1] (nullable=False)

---

## Cross-RQ Dependencies

### Required Dependency: Ch6 6.1.1
- **Status check:** results/ch6/6.1.1/status.yaml (rq_results: success)
- **Primary data:** results/ch6/6.1.1/data/step03_confidence_theta_scores.csv
- **Alternative patterns:** results/ch6/6.1.1/data/*confidence*theta*.csv
- **Expected format:** 100 rows x 3+ columns (UID, confidence_theta, se_theta)
- **Fallback strategy:** Try multiple file naming patterns
- **Circuit breaker:** If not found, QUIT with clear error message

### Optional Dependency: Ch7 7.1.1
- **Status check:** results/ch7/7.1.1/status.yaml (rq_results: success)
- **Primary data:** results/ch7/7.1.1/data/step07_effect_sizes.csv
- **Alternative patterns:** results/ch7/7.1.1/data/*effect*.csv, *regression*.csv
- **Expected format:** Effect sizes for accuracy prediction with same cognitive tests
- **Fallback strategy:** If not available, note limitation and complete other analyses
- **Use case:** Step 9 comparative analysis (confidence vs accuracy predictors)

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
- **Primary validation:** File existence and accessibility checks
- **Secondary validation:** Content format verification for Ch6 outputs
- **Substance criteria:** All 4 layers as specified above
- **Failure action:** Immediate quit with dependency error

#### Step 1: Extract Confidence Data
- **Primary validation:** Data range and distribution checks
- **Secondary validation:** Sample size and completeness verification
- **Substance criteria:** Theta scores in valid IRT range, complete cases
- **Failure action:** Data quality error, invoke g_debug

#### Step 2: Extract Cognitive Data
- **Primary validation:** T-score transformation verification
- **Secondary validation:** Distribution and outlier checks
- **Substance criteria:** T-scores approximately M=50, SD=10, reasonable ranges
- **Failure action:** Transformation error, review raw data

#### Step 3: Merge Datasets
- **Primary validation:** Successful merge and sample size checks
- **Secondary validation:** Missing data patterns and correlation matrix
- **Substance criteria:** Final N >= 90, no excessive missing data
- **Failure action:** Merge error, check UID consistency

#### Step 4: Hierarchical Regression
- **Primary validation:** Model convergence and R² bounds
- **Secondary validation:** F-test results and bootstrap CI validity
- **Substance criteria:** Valid R² values, nested model property
- **Failure action:** Model fitting error, check data quality

#### Step 5: Individual Predictors
- **Primary validation:** Coefficient estimates and assumption checks
- **Secondary validation:** Multiple comparison corrections and VIF values
- **Substance criteria:** Reasonable betas, valid CIs, dual p-values
- **Failure action:** Assumption violation or coefficient error

#### Step 6: Cross-Validation
- **Primary validation:** CV completion and generalization assessment
- **Secondary validation:** Overfitting detection and fold consistency
- **Substance criteria:** All folds complete, reasonable CV R²
- **Failure action:** CV failure, check model stability

#### Step 7: Effect Sizes
- **Primary validation:** Effect size bounds and bootstrap CI validity
- **Secondary validation:** Dominance analysis and interpretation consistency
- **Substance criteria:** Valid effect sizes, reasonable confidence intervals
- **Failure action:** Effect size computation error

#### Step 8: Power Analysis
- **Primary validation:** Power calculation bounds and mathematical consistency
- **Secondary validation:** Alpha level verification and sensitivity analysis
- **Substance criteria:** Valid power values, correct alpha correction
- **Failure action:** Power computation error, check parameters

#### Step 9: Accuracy Comparison
- **Primary validation:** Cross-RQ data integration and bootstrap difference CIs
- **Secondary validation:** Pattern classification and evidence synthesis
- **Substance criteria:** Successful comparison, valid difference estimates
- **Failure action:** Cross-RQ integration error, note limitation

---

## Summary

**Total Steps:** 10 (Step 0: validation + Steps 1-9: analysis)
**Estimated Runtime:** 45 minutes
**Cross-RQ Dependencies:** Ch6 6.1.1 (required), Ch7 7.1.1 (optional for comparison)
**Primary Outputs:** Hierarchical regression results, effect sizes, cross-validation assessment, metacognitive dissociation evidence
**Validation Coverage:** 100% (all 10 steps have 4-layer validation requirements)

**Key Hypothesis:** Cognitive tests predict confidence theta scores weakly compared to accuracy prediction, supporting metacognitive dissociation theory.

**Critical Methodological Notes:**
- Enhanced v5.1 specifications: Complete statistical implementation details with seeds, iterations, corrections, remedial actions
- Bootstrap confidence intervals (1000 iterations, seed=42) for all effect size estimates
- Dual p-value reporting (uncorrected + Bonferroni + FDR) per Decision D068
- Cross-validation assessment of model generalizability
- Power analysis for effect size interpretation
- Comprehensive assumption violation remedial actions
- Cross-RQ dependency handling with fallback paths

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml  
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent with enhanced v5.1 specifications