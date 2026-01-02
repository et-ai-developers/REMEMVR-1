# Analysis Plan: RQ 7.3.1 - Do cognitive tests predict confidence trajectories?

**Research Question:** 7.3.1
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

**Purpose:** Test whether cognitive tests (RAVLT-T, BVMT-T, RPM-T) predict IRT-scaled confidence theta scores with similar patterns as accuracy prediction, addressing metacognitive monitoring vs memory performance dissociation.

**Pipeline:** Multiple Linear Regression with Hierarchical Entry
**Steps:** 9 total analysis steps (Step 0: dependency validation + Steps 1-8: analysis)
**Estimated Runtime:** 45-60 minutes

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Chapter 7 Bonferroni correction: alpha = 0.05/28 = 0.00179 per RQ
- Standard cross-validation: 5-fold with seed=42
- Bootstrap CIs: 1000 iterations with seed=42

**Critical Dependencies:**
- DERIVED data from Ch6 6.1.1 (confidence theta scores)
- RAW data from master.xlsx (cognitive test scores)

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify Ch6 6.1.1 confidence outputs and master.xlsx accessibility before proceeding

**Input:**
- Primary: results/ch6/6.1.1/data/step03_confidence_theta_scores.csv
- Alternative: results/ch6/6.1.1/data/*confidence*theta*.csv
- Fallback: results/ch6/6.1.1/data/*confidence*.csv
- Expected content: UID, confidence_theta, SE columns for 100 participants
- Check: data/cache/master.xlsx (cognitive test scores)
- If Ch6 output not found: QUIT with "Ch6 6.1.1 confidence theta output not found"
- If master.xlsx not found: QUIT with "master.xlsx cognitive test data not accessible"

**Processing:**
- Verify Ch6 6.1.1 status.yaml shows rq_results: success
- Locate confidence theta file using pattern matching
- Check file contains required columns (UID, confidence_theta, SE)
- Verify 100 participants present
- Check master.xlsx contains cognitive test columns (RAVLT, BVMT, RPM)
- Log all validation results

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Content: Ch6 status check, file discovery results, column verification

*Value Ranges:*
- File size > 0 bytes (non-empty validation log)
- Validation status: PASS or FAIL with specific reasons

*Data Quality:*
- All required files located or specific failure reasons logged
- No ambiguous validation states (clear pass/fail per dependency)

*Log Validation:*
- Required patterns: "Ch6 6.1.1 status: success", "Confidence theta file located", "master.xlsx accessible"
- Forbidden patterns: "ERROR", "FAIL", "not found" (unless in failure context)

**Expected Behavior on Validation Failure:**
- Raise error with specific missing dependency
- Log to logs/step00_validate_dependencies.log
- Quit immediately, invoke g_debug for missing file investigation

---

### Step 1: Extract Confidence Theta Scores
**Dependencies:** Step 0 (Ch6 dependency validated)
**Complexity:** Low (<5 minutes)

**Purpose:** Load IRT-derived confidence theta scores from Ch6 6.1.1 for all participants

**Input:**
- Primary: results/ch6/6.1.1/data/step03_confidence_theta_scores.csv
- Expected format: UID (object), confidence_theta (float64), SE (float64)
- Expected N: 100 participants from Ch6 analysis

**Processing:**
- Load confidence theta scores using pandas
- Verify all 100 participants present (no missing UIDs)
- Check confidence_theta values in reasonable IRT range [-4, 4]
- Check SE values positive and bounded [0.1, 2.0]
- Remove any duplicate UIDs (keep first occurrence if found)
- Standardize UID format for merging
- Log data quality metrics

**Output:**
- data/step01_confidence_theta.csv (100 rows x 3 columns)

**Validation Requirement:**
Validation tools MUST be used after confidence extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_confidence_theta.csv: 100 rows x 3 columns
- Columns: UID (object), confidence_theta (float64), SE (float64)

*Value Ranges:*
- confidence_theta in [-4, 4] (IRT ability scale reasonable bounds)
- SE in [0.1, 2.0] (positive, bounded standard errors)
- UID non-null for all rows

*Data Quality:*
- Exactly 100 participants (no missing data)
- No duplicate UIDs
- No NaN values in critical columns

*Log Validation:*
- Required patterns: "100 participants loaded", "Confidence range validated", "No duplicates found"
- Forbidden patterns: "ERROR", "missing data", "duplicate UID"

**Expected Behavior on Validation Failure:**
- Raise error with specific data quality issue
- Log to logs/step01_extract_confidence.log
- Quit immediately, invoke g_debug for data investigation

---

### Step 2: Extract Cognitive Test Scores
**Dependencies:** Step 0 (master.xlsx validated)
**Complexity:** Low (<10 minutes)

**Purpose:** Extract and T-score standardize cognitive test scores (RAVLT, BVMT, RPM) for prediction analysis

**Input:**
- data/cache/master.xlsx (raw cognitive test scores)
- Required columns: UID, RAVLT_Total, BVMT_Total, RPM_Total, Age, Sex, Education

**Processing:**
- Load master.xlsx using pandas read_excel
- Extract cognitive test scores for 100 participants
- Compute T-scores: T = 50 + 10 x (raw - mean)/sd
- Standardization for each test separately
- Create T-scored variables: RAVLT_T, BVMT_T, RPM_T
- Extract demographic variables: Age (years), Sex (M/F), Education (years)
- Handle missing cognitive data: exclude participant if >1 test missing
- Log descriptive statistics for each test

**Output:**
- data/step02_cognitive_tests.csv (100 rows x 7 columns)

**Validation Requirement:**
Validation tools MUST be used after cognitive test extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_cognitive_tests.csv: 100 rows x 7 columns
- Columns: UID, RAVLT_T, BVMT_T, RPM_T, Age, Sex, Education

*Value Ranges:*
- T-scores in [20, 80] (reasonable T-score range, mean=50, sd=10)
- Age in [18, 90] (adult participants)
- Education in [8, 25] (years of education)
- Sex: M or F only

*Data Quality:*
- All 100 participants present (matched to confidence data)
- Missing cognitive data <5% per test
- No impossible values (negative T-scores, extreme ages)

*Log Validation:*
- Required patterns: "T-scores computed", "100 participants processed", "Descriptives calculated"
- Forbidden patterns: "ERROR", "missing all tests", "invalid T-score"

**Expected Behavior on Validation Failure:**
- Raise error with specific data quality issue
- Log to logs/step02_extract_cognitive.log
- Quit immediately, invoke g_debug for data investigation

---

### Step 3: Merge Analysis Dataset
**Dependencies:** Steps 1-2 (confidence theta + cognitive tests)
**Complexity:** Low (<5 minutes)

**Purpose:** Create complete analysis dataset by merging confidence theta scores with cognitive test T-scores

**Input:**
- data/step01_confidence_theta.csv
- data/step02_cognitive_tests.csv

**Processing:**
- Merge datasets on UID using pandas merge (inner join)
- Verify complete cases: both confidence theta and all cognitive tests present
- Create final analysis variables:
  - Outcome: confidence_theta (continuous)
  - Demographics: Age, Sex_coded (0=F, 1=M), Education  
  - Cognitive predictors: RAVLT_T, BVMT_T, RPM_T
- Check for outliers: confidence_theta beyond +-3 SD
- Log final sample size and missingness patterns

**Output:**
- data/step03_analysis_input.csv (N rows x 8 columns)

**Validation Requirement:**
Validation tools MUST be used after dataset merging.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_analysis_input.csv: 95-100 rows x 8 columns
- Columns: UID, confidence_theta, RAVLT_T, BVMT_T, RPM_T, Age, Sex_coded, Education

*Value Ranges:*
- confidence_theta in [-4, 4] (IRT theta range)
- T-scores in [20, 80] (standardized test scores)
- Age in [18, 90], Education in [8, 25]
- Sex_coded: 0 or 1 only

*Data Quality:*
- Complete cases only (no missing data in analysis variables)
- Final N >= 95 (allowing minimal exclusion for missing data)
- No extreme outliers flagged as problematic

*Log Validation:*
- Required patterns: "Merge complete", "N=XX participants", "Complete cases only"
- Forbidden patterns: "ERROR", "merge failed", "extensive missingness"

**Expected Behavior on Validation Failure:**
- Raise error with specific merge issue
- Log to logs/step03_merge_dataset.log
- Quit immediately, invoke g_debug for merge investigation

---

### Step 4: Hierarchical Regression Analysis  
**Dependencies:** Step 3 (merged analysis dataset)
**Complexity:** Medium (~15 minutes including bootstrap)

**Purpose:** Fit hierarchical regression models to test incremental prediction of cognitive tests beyond demographics

**Input:**
- data/step03_analysis_input.csv

**Processing:**
- Fit hierarchical models using statsmodels OLS:
  - Model 1 (Demographics): confidence_theta ~ Age + Sex_coded + Education
  - Model 2 (+ Cognitive): confidence_theta ~ Age + Sex_coded + Education + RAVLT_T + BVMT_T + RPM_T
- Compute model comparison:
  - Delta R-squared = R2_model2 - R2_model1  
  - F-test for R-squared change using anova_lm
  - Effect size: Cohen's f-squared = Delta_R2/(1 - R2_model2)
- Extract coefficients with 95% confidence intervals:
  - Bootstrap CIs for all coefficients:
    - Iterations: 1000
    - Random seed: 42 for reproducibility  
    - Method: Participant-level resampling with replacement
    - CI computation: percentile method (2.5th, 97.5th percentiles)
- Multiple comparison correction:
  - Family: Within-RQ cognitive tests (3 predictors)
  - Bonferroni: alpha = 0.00179/3 = 0.000597 per test
  - Also compute FDR using Benjamini-Hochberg
  - Report BOTH uncorrected AND corrected p-values (Decision D068)

**Output:**
- data/step04_hierarchical_regression.csv (model comparison results)
- data/step04_regression_coefficients.csv (coefficients with dual p-values)

**Validation Requirement:**
Validation tools MUST be used after regression analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_hierarchical_regression.csv: 1 row x 6 columns
- Columns: R2_model1, R2_model2, Delta_R2, F_statistic, p_value, cohens_f2
- data/step04_regression_coefficients.csv: 6 rows x 8 columns  
- Columns: predictor, beta, se, ci_lower, ci_upper, p_uncorrected, p_bonferroni, p_fdr

*Value Ranges:*
- R-squared values in [0, 1] 
- F-statistic > 0, p-values in [0, 1]
- Cohen's f-squared >= 0 (effect size bounded)
- Beta coefficients in [-2, 2] (reasonable for standardized predictors)
- Bootstrap CIs: ci_lower < beta < ci_upper

*Data Quality:*
- Model convergence successful (no convergence warnings)
- Bootstrap completed full 1000 iterations
- All 6 predictors present with valid coefficients
- Dual p-values computed (Decision D068)

*Log Validation:*
- Required patterns: "Model 1 fitted", "Model 2 fitted", "Bootstrap complete: 1000 iterations", "Bonferroni correction applied"
- Forbidden patterns: "ERROR", "convergence failed", "singular matrix", "bootstrap failed"

**Expected Behavior on Validation Failure:**
- Raise error with specific regression failure
- Log to logs/step04_hierarchical_regression.log
- Quit immediately, invoke g_debug for model investigation

---

### Step 5: Effect Size Analysis
**Dependencies:** Step 4 (regression coefficients)  
**Complexity:** Medium (~10 minutes)

**Purpose:** Compute comprehensive effect sizes including semi-partial correlations and dominance analysis

**Input:**
- data/step04_regression_coefficients.csv
- data/step03_analysis_input.csv (for semi-partial correlations)

**Processing:**
- Compute semi-partial correlations (sr) for each cognitive predictor:
  - sr = correlation between predictor and outcome, controlling for all other predictors
  - sr-squared = unique variance explained by each predictor
- Compute relative importance using dominance analysis:
  - Fit all possible subset models (2^3 = 8 models for 3 cognitive tests)
  - Average contribution across all model subsets
  - Rank predictors by average contribution
- Bootstrap 95% CIs for effect sizes:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Resample participants with replacement, recompute sr and dominance
  - CI method: percentile (2.5th, 97.5th)
- Overall model effect size:
  - Cohen's f-squared = R2/(1-R2) 
  - Interpret: 0.02 = small, 0.15 = medium, 0.35 = large

**Output:**
- data/step05_effect_sizes.csv (effect size summary with CIs)

**Validation Requirement:**
Validation tools MUST be used after effect size computation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_effect_sizes.csv: 4 rows x 6 columns
- Columns: predictor, sr, sr_squared, dominance_weight, ci_lower, ci_upper
- Includes 3 cognitive tests + overall model row

*Value Ranges:*
- Semi-partial correlations in [-1, 1] 
- sr_squared in [0, 1] (proportion of variance)
- Dominance weights in [0, 1], sum to total R-squared
- Bootstrap CIs valid (ci_lower <= point_estimate <= ci_upper)

*Data Quality:*
- All 3 cognitive predictors present
- Dominance weights sum approximately to Delta_R2 from Step 4
- Bootstrap CIs computed successfully
- Effect size interpretations appropriate for context

*Log Validation:*
- Required patterns: "Semi-partial correlations computed", "Dominance analysis complete", "Bootstrap CIs: 1000 iterations"
- Forbidden patterns: "ERROR", "dominance failed", "negative sr_squared"

**Expected Behavior on Validation Failure:**
- Raise error with specific effect size computation failure  
- Log to logs/step05_effect_sizes.log
- Quit immediately, invoke g_debug for effect size investigation

---

### Step 6: Model Diagnostics
**Dependencies:** Step 4 (fitted regression model)
**Complexity:** Medium (~10 minutes)

**Purpose:** Comprehensive regression assumption testing with remedial actions for violations

**Input:**
- data/step03_analysis_input.csv
- Model 2 residuals and fitted values from Step 4

**Processing:**
- Check regression assumptions:
  - Multicollinearity: VIF for each predictor using statsmodels
  - Residual normality: Shapiro-Wilk test on standardized residuals  
  - Homoscedasticity: Breusch-Pagan test
  - Linearity: Partial residual plots for each cognitive predictor
  - Independence: Design-based (cross-sectional data, assumed independent)
  - Influential points: Cook's distance > 4/n threshold (0.04 for n=100)
- Remedial actions for assumption violations:
  - Multicollinearity (VIF > 5): Document, consider ridge if VIF > 10
  - Normality violation (p < 0.05): Use bootstrap CIs as primary (already computed)
  - Heteroscedasticity (p < 0.05): Report HC3 robust standard errors
  - Linearity violation: Test polynomial terms for non-linear relationships
  - Outliers (Cook's D > 0.04): Report results with and without outliers
- Generate diagnostic plots data for later plotting:
  - Residuals vs fitted
  - Q-Q plot coordinates  
  - Partial residual plots
  - Cook's distance values

**Output:**
- data/step06_model_diagnostics.csv (assumption test results)
- data/step06_diagnostic_plots_data.csv (plot coordinates)

**Validation Requirement:**
Validation tools MUST be used after diagnostic testing.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_model_diagnostics.csv: 1 row x 8 columns
- Columns: vif_max, shapiro_p, breusch_pagan_p, outliers_n, normality_ok, homosced_ok, multicollin_ok, overall_assumptions
- data/step06_diagnostic_plots_data.csv: 100+ rows x 6 columns

*Value Ranges:*
- VIF values in [1, 15] (1 = no collinearity, >10 concerning)
- p-values in [0, 1] for normality and homoscedasticity tests
- Cook's distance in [0, 1] (bounded influence measure)
- Binary assumption flags: 0 (violated) or 1 (satisfied)

*Data Quality:*  
- All assumption tests completed successfully
- VIF computed for all 6 predictors (including demographics)
- Outlier detection completed for all observations
- Remedial actions documented if assumptions violated

*Log Validation:*
- Required patterns: "VIF computed", "Normality tested", "Homoscedasticity tested", "Cook's distance computed"
- Forbidden patterns: "ERROR", "VIF failed", "test statistic undefined"

**Expected Behavior on Validation Failure:**
- Raise error with specific diagnostic failure
- Log to logs/step06_model_diagnostics.log  
- Quit immediately, invoke g_debug for diagnostic investigation

---

### Step 7: Cross-Validation Analysis
**Dependencies:** Step 4 (regression models fitted)
**Complexity:** Medium (~15 minutes)

**Purpose:** Assess model generalizability using k-fold cross-validation to detect overfitting

**Input:**
- data/step03_analysis_input.csv

**Processing:**
- Implement 5-fold cross-validation using sklearn.model_selection.KFold:
  - Random seed: 42 for reproducibility
  - Shuffle: True (randomize before splitting)
  - Stratification: Use quantile-based stratification on confidence_theta (outcome) 
- For each fold:
  - Split data: 80% training, 20% test
  - Fit both Model 1 (demographics) and Model 2 (+ cognitive) on training data
  - Evaluate on test data: compute R-squared, RMSE, MAE
  - Store fold-specific results
- Compute cross-validation metrics:
  - Mean and standard deviation of R-squared across folds
  - Mean and standard deviation of RMSE and MAE
  - Generalization gap: mean(train_R2) - mean(test_R2)
  - Flag overfitting if gap > 0.10
- Compare models:
  - Test Model 1 vs Model 2 R-squared in CV  
  - Wilcoxon signed-rank test on fold-wise R-squared differences

**Output:**
- data/step07_cross_validation.csv (CV results summary)

**Validation Requirement:**
Validation tools MUST be used after cross-validation analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_cross_validation.csv: 2 rows x 8 columns  
- Columns: model, mean_train_r2, sd_train_r2, mean_test_r2, sd_test_r2, rmse, mae, overfitting_flag
- Row 1: Model 1 (demographics), Row 2: Model 2 (+ cognitive)

*Value Ranges:*
- R-squared values in [0, 1] 
- RMSE, MAE > 0 (positive error metrics)
- Standard deviations >= 0
- Overfitting flag: 0 (no) or 1 (yes) based on gap > 0.10

*Data Quality:*
- All 5 folds completed successfully  
- Both models evaluated in CV
- Metrics computed for all folds
- Generalization gap assessed

*Log Validation:*
- Required patterns: "5-fold CV complete", "Model 1 CV", "Model 2 CV", "Generalization gap computed"
- Forbidden patterns: "ERROR", "CV failed", "fold fitting failed"

**Expected Behavior on Validation Failure:**
- Raise error with specific CV failure
- Log to logs/step07_cross_validation.log
- Quit immediately, invoke g_debug for CV investigation

---

### Step 8: Accuracy Prediction Comparison  
**Dependencies:** Step 4-7 (regression results complete)
**Complexity:** Medium (~10 minutes)

**Purpose:** Compare cognitive test prediction patterns between confidence (current RQ) and accuracy (RQ 7.1.1)

**Input:**
- data/step04_regression_coefficients.csv (current RQ confidence results)
- Primary: results/ch7/7.1.1/data/step04_regression_coefficients.csv (accuracy prediction)
- Alternative: results/ch7/7.1.1/data/*regression*coefficients*.csv
- Fallback: results/ch7/7.1.1/data/*coefficients*.csv
- If not found: Log warning and skip comparison (proceed with current results only)

**Processing:**
- Load accuracy prediction results from RQ 7.1.1 (if available)
- Align predictor names and merge on predictor column
- Compare prediction patterns:
  - R-squared comparison: confidence vs accuracy overall model fit
  - Individual predictor comparison: beta coefficients for RAVLT_T, BVMT_T, RPM_T
  - Effect size comparison: which tests predict which outcome more strongly
  - Statistical significance patterns: corrected p-values
- Compute difference scores:
  - Delta_beta = beta_confidence - beta_accuracy for each predictor
  - Delta_R2 = R2_confidence - R2_accuracy  
- Identify metacognitive dissociation pattern:
  - Tests that predict accuracy but not confidence
  - Tests that predict confidence but not accuracy
  - Overall R-squared pattern (expected: confidence < accuracy)

**Output:**
- data/step08_accuracy_comparison.csv (comparison results)

**Validation Requirement:**
Validation tools MUST be used after comparison analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_accuracy_comparison.csv: 4 rows x 8 columns
- Columns: predictor, beta_confidence, beta_accuracy, delta_beta, p_conf_corr, p_acc_corr, sig_confidence, sig_accuracy
- Includes 3 cognitive tests + overall model comparison

*Value Ranges:*
- Beta coefficients in [-2, 2] (standardized predictors)
- Delta beta in [-4, 4] (difference between outcomes)
- Corrected p-values in [0, 1] 
- Significance flags: 0 (non-sig) or 1 (significant) 

*Data Quality:*
- Comparison completed if accuracy data available
- All 3 cognitive predictors compared
- Missing accuracy data handled gracefully (skip comparison)
- Dissociation patterns clearly identified

*Log Validation:*
- Required patterns: "Accuracy data located" or "Accuracy data not found - skipping comparison", "Comparison complete"
- Forbidden patterns: "ERROR", "comparison failed", "merge error"

**Expected Behavior on Validation Failure:**
- If accuracy data missing: Log warning, create comparison file with confidence data only
- If other errors: Raise error with specific comparison failure
- Log to logs/step08_accuracy_comparison.log  
- Quit immediately on non-missing-data errors, invoke g_debug

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
1. `data/step00_dependency_validation.txt` - Cross-RQ dependency validation results
2. `data/step01_confidence_theta.csv` - Extracted confidence theta scores (100 x 3)
3. `data/step02_cognitive_tests.csv` - T-scored cognitive tests + demographics (100 x 7)  
4. `data/step03_analysis_input.csv` - Merged analysis dataset (95-100 x 8)
5. `data/step04_hierarchical_regression.csv` - Model comparison results (1 x 6)
6. `data/step04_regression_coefficients.csv` - Coefficients with dual p-values (6 x 8)
7. `data/step05_effect_sizes.csv` - Effect sizes with bootstrap CIs (4 x 6)
8. `data/step06_model_diagnostics.csv` - Assumption test results (1 x 8)
9. `data/step06_diagnostic_plots_data.csv` - Diagnostic plot coordinates (100+ x 6)
10. `data/step07_cross_validation.csv` - CV results with overfitting assessment (2 x 8)
11. `data/step08_accuracy_comparison.csv` - Confidence vs accuracy comparison (4 x 8)

### Logs (ONLY execution logs)
- `logs/step00_validate_dependencies.log` - Dependency validation log
- `logs/step01_extract_confidence.log` - Confidence extraction log  
- `logs/step02_extract_cognitive.log` - Cognitive test extraction log
- `logs/step03_merge_dataset.log` - Dataset merging log
- `logs/step04_hierarchical_regression.log` - Regression analysis log
- `logs/step05_effect_sizes.log` - Effect size computation log
- `logs/step06_model_diagnostics.log` - Diagnostic testing log
- `logs/step07_cross_validation.log` - Cross-validation log
- `logs/step08_accuracy_comparison.log` - Comparison analysis log

### Plots (EMPTY until rq_plots runs)
Plot source CSV files created in data/:
- `data/step06_diagnostic_plots_data.csv` contains coordinates for:
  - Residuals vs fitted values plot
  - Q-Q normality plot  
  - Partial residual plots for each cognitive predictor
  - Cook's distance plot

### Results (EMPTY until rq_results runs)  
- `results/summary.md` will be created by rq_results summarizing key findings

---

## Expected Data Formats

### Step-to-Step Transformations

**Steps 1-2:** Data extraction and standardization
- Raw confidence theta scores -> cleaned/validated confidence data
- Raw cognitive test scores -> T-scored standardized tests + demographics

**Step 3:** Data integration  
- Separate confidence and cognitive datasets -> merged analysis-ready dataset
- Inner join on UID, complete cases only

**Steps 4-5:** Primary analysis
- Analysis dataset -> hierarchical regression models + effect sizes
- Bootstrap resampling for robust confidence intervals  

**Steps 6-7:** Model validation
- Fitted models -> assumption diagnostics + cross-validation assessment  
- Remedial actions applied if assumptions violated

**Step 8:** Cross-RQ integration
- Current results + RQ 7.1.1 accuracy results -> comparative analysis
- Identifies metacognitive dissociation patterns

### Column Naming Conventions

**Analysis Variables:**
- Outcome: `confidence_theta` (continuous IRT ability scale)
- Demographics: `Age` (years), `Sex_coded` (0=F, 1=M), `Education` (years)
- Cognitive predictors: `RAVLT_T`, `BVMT_T`, `RPM_T` (T-scores, mean=50, sd=10)

**Statistical Results:**
- Coefficients: `beta` (standardized), `se` (standard error), `ci_lower`, `ci_upper`
- p-values: `p_uncorrected`, `p_bonferroni`, `p_fdr` (Decision D068)
- Effect sizes: `sr` (semi-partial correlation), `sr_squared`, `dominance_weight`

### Data Type Constraints

**Identifiers:** UID as string/object (consistent across datasets)
**Outcomes:** confidence_theta as float64, bounded [-4, 4]
**Predictors:** All T-scores as float64, Age/Education as int64
**Statistics:** All statistical results as float64
**Flags:** Binary indicators as int64 (0/1)

---

## Cross-RQ Dependencies

### Ch6 6.1.1 Dependency (CRITICAL)
- **Required File:** results/ch6/6.1.1/data/step03_confidence_theta_scores.csv
- **Content:** IRT-derived confidence theta scores for all participants  
- **Format:** UID, confidence_theta, SE columns
- **Circuit Breaker:** If missing, QUIT with dependency error

### RQ 7.1.1 Dependency (OPTIONAL)
- **Required File:** results/ch7/7.1.1/data/step04_regression_coefficients.csv  
- **Content:** Accuracy prediction results for comparison
- **Format:** Same coefficient structure as current analysis
- **Fallback:** If missing, proceed with confidence analysis only, skip comparison

### Master Data Dependency (CRITICAL)  
- **Required File:** data/cache/master.xlsx
- **Content:** Raw cognitive test scores and demographics
- **Format:** UID, RAVLT_Total, BVMT_Total, RPM_Total, Age, Sex, Education
- **Circuit Breaker:** If missing, QUIT with data access error

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

All 9 steps include comprehensive 4-layer validation structure as specified above, covering:
1. **Output Files:** Exact dimensions, columns, data types
2. **Value Ranges:** Scientific bounds appropriate for each measure  
3. **Data Quality:** Missing data tolerance, expected N, completeness
4. **Log Validation:** Required success patterns, forbidden error patterns

### Assumption Violation Handling
- **Multicollinearity (VIF > 5):** Document, proceed with caution, consider ridge if VIF > 10
- **Non-normality (Shapiro p < 0.05):** Bootstrap CIs as primary (already computed)  
- **Heteroscedasticity (Breusch-Pagan p < 0.05):** Report HC3 robust standard errors
- **Outliers (Cook's D > 0.04):** Report results with and without outliers
- **Overfitting (CV gap > 0.10):** Emphasize CV results over training R-squared

---

## Summary

**Total Steps:** 9 (Step 0 + Steps 1-8)
**Estimated Runtime:** 45-60 minutes
**Cross-RQ Dependencies:** Ch6 6.1.1 (critical), RQ 7.1.1 (optional), master.xlsx (critical)
**Primary Outputs:** Hierarchical regression results, effect sizes, model diagnostics, CV assessment, accuracy comparison

**Key Hypothesis:** Cognitive tests will predict confidence more weakly than accuracy (lower R-squared), with potential dissociation where memory tests (RAVLT, BVMT) predict accuracy more strongly than confidence, while fluid intelligence (RPM) may show relatively stronger confidence prediction.

**Critical Methodological Notes:**
- Bootstrap CIs provide robust inference given potential assumption violations
- Cross-validation assesses generalizability for potentially small effects  
- Dual p-value reporting (D068) ensures both liberal and conservative inference
- Chapter 7 Bonferroni correction addresses multiple cognitive prediction RQs
- Comparison with RQ 7.1.1 tests core metacognitive dissociation hypothesis

**Statistical Specifications Complete:**
- Random seeds: 42 for all procedures (bootstrap, CV)
- Bootstrap: 1000 iterations, participant-level resampling  
- Cross-validation: 5-fold with stratification and overfitting detection
- Multiple comparisons: Bonferroni + FDR with dual reporting
- Power considerations: Post-hoc analysis for interpreting null effects
- Remedial actions: Specified for all assumption violations

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml  
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code
5. rq_inspect validates outputs against plan specifications

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent with enhanced v5.1 statistical specifications