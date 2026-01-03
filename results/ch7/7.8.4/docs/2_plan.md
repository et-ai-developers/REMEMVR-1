# Analysis Plan: RQ 7.8.4 - Multivariate vs Univariate Prediction

**Research Question:** 7.8.4
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ compares multivariate versus univariate approaches for predicting episodic memory performance across What/Where/When domains using cognitive test batteries. The analysis examines whether joint modeling of all three domains provides efficiency gains over separate domain-specific models.

**Pipeline:** Multiple regression with model comparison and cross-validation
**Steps:** 9 total analysis steps (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** ~45 minutes

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Cross-validation design for overfitting detection
- AIC-based model comparison with caveats

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 outputs exist before proceeding with domain theta score extraction

**Input:**
- Primary: results/ch5/5.2.1/status.yaml (verify Ch5 What domain completion)
- Primary: results/ch5/5.2.2/status.yaml (verify Ch5 Where domain completion)  
- Primary: results/ch5/5.2.3/status.yaml (verify Ch5 When domain completion)
- Alternative: results/ch5/5.2.*/data/*theta*.csv (find theta score outputs)
- Fallback pattern: results/ch5/5.2.*/data/step*theta*.{csv,txt,rds}
- Verification: data/cache/master.xlsx accessibility for cognitive tests

**Processing:**
- Check all three Ch5 5.2.X RQs completed successfully (rq_results: success)
- Locate domain-specific theta score files using multiple search patterns
- Verify theta score files contain expected columns (UID, theta, SE)
- Test master.xlsx accessibility and cognitive test column availability
- Log all validation checks with clear pass/fail status

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Expected content: status checks for 3 Ch5 RQs + file discovery results

*Value Ranges:*
- Status checks: "success" or "pending/failed"
- File counts: 3 domain theta files expected
- Cognitive test availability: 4 tests minimum (RAVLT, BVMT, NART, RPM)

*Data Quality:*
- All 3 Ch5 5.2.X RQs must show rq_results: success
- Theta files must exist and be non-empty
- master.xlsx must be accessible with cognitive test columns

*Log Validation:*
- Required pattern: "Dependency validation complete"
- Required pattern: "Ch5 5.2.1: PASS", "Ch5 5.2.2: PASS", "Ch5 5.2.3: PASS"
- Required pattern: "Theta files found: 3"
- Forbidden patterns: "ERROR", "FAIL", "file not found"

**Expected Behavior on Validation Failure:**
- Raise error with specific missing dependency
- Log to logs/step00_validate_dependencies.log
- Quit immediately, invoke g_debug

### Step 1: Extract Domain-Specific Theta Scores
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Medium (~8 minutes)

**Purpose:** Extract participant-level theta scores from Ch5 5.2.X domain-specific analyses

**Input:**
- Primary: results/ch5/5.2.1/data/step03_theta_scores.csv (What domain)
- Primary: results/ch5/5.2.2/data/step03_theta_scores.csv (Where domain)
- Primary: results/ch5/5.2.3/data/step03_theta_scores.csv (When domain)
- Alternative: results/ch5/5.2.*/data/*theta*.csv
- Expected format: columns [UID, theta, SE] with N=100 rows per domain

**Processing:**
- Load domain-specific theta scores from Ch5 5.2.X outputs
- Verify column structure: UID (string), theta (numeric), SE (numeric)
- Check for complete data: all 100 participants in each domain
- Merge domains into single dataset with columns: UID, What_theta, Where_theta, When_theta
- Compute domain correlation matrix for multivariate modeling assessment
- Check correlation range: expect 0.20-0.70 for viable multivariate modeling
- Handle missing data: complete case analysis (exclude if any domain missing)

**Output:**
- data/step01_domain_theta_scores.csv
- data/step01_domain_correlations.csv

**Validation Requirement:**
Validation tools MUST be used after theta score extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_domain_theta_scores.csv: N=100 rows x 4 columns
- Columns: UID (object), What_theta (float64), Where_theta (float64), When_theta (float64)
- data/step01_domain_correlations.csv: 3x3 correlation matrix

*Value Ranges:*
- theta values in [-3, 3] (standard IRT ability scale)
- correlations in [-1, 1] with expected range [0.20, 0.70]
- No extreme correlations (>0.90) suggesting domain redundancy

*Data Quality:*
- Exactly 100 participants with complete domain data
- No missing theta values (complete case analysis)
- All UIDs present from master participant list
- Domain correlations statistically significant but moderate

*Log Validation:*
- Required pattern: "Domain theta extraction complete: 100 participants"
- Required pattern: "Domain correlations in expected range"
- Required pattern: "VALIDATION - PASS"
- Forbidden patterns: "ERROR", "missing data exceeds threshold"

**Expected Behavior on Validation Failure:**
- Raise error with specific data quality issue
- Log to logs/step01_extract_domain_theta.log
- Quit immediately, invoke g_debug

### Step 2: Extract Cognitive Test Scores
**Dependencies:** Step 1 (domain theta scores)
**Complexity:** Low (~5 minutes)

**Purpose:** Extract cognitive test battery scores for multivariate prediction modeling

**Input:**
- Primary: data/cache/master.xlsx (cognitive test battery)
- Target tests: RAVLT, BVMT, NART, RPM, Age
- Expected participants: same 100 UIDs from Step 1

**Processing:**
- Load master.xlsx and extract cognitive test columns
- Target predictors: RAVLT total, BVMT total, NART errors, RPM correct, Age
- Verify data completeness for target predictors
- Handle missing data: complete case analysis (exclude participants missing any predictor)
- Standardize cognitive test scores (z-scores) for regression analysis
- Compute predictor correlation matrix for multicollinearity assessment
- Check VIF preconditions: expect correlations <0.80 for stable regression

**Output:**
- data/step02_cognitive_tests.csv
- data/step02_predictor_correlations.csv

**Validation Requirement:**
Validation tools MUST be used after cognitive test extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_cognitive_tests.csv: N=100 rows x 6 columns
- Columns: UID (object), RAVLT_z (float64), BVMT_z (float64), NART_z (float64), RPM_z (float64), Age_z (float64)
- data/step02_predictor_correlations.csv: 5x5 correlation matrix

*Value Ranges:*
- Standardized scores in [-3, 3] (z-score range)
- Age_z in [-2, 2] (reasonable age distribution)
- Predictor correlations in [-0.80, 0.80] (avoiding multicollinearity)

*Data Quality:*
- Complete cognitive test data for 100 participants
- No missing values after standardization
- Predictor correlations suggest independence (no r > 0.80)
- Z-score standardization successful (mean~0, sd~1)

*Log Validation:*
- Required pattern: "Cognitive test extraction complete: 100 participants"
- Required pattern: "Standardization complete: z-scores computed"
- Required pattern: "Multicollinearity check: all correlations < 0.80"
- Forbidden patterns: "ERROR", "excessive missingness", "perfect correlation"

**Expected Behavior on Validation Failure:**
- Raise error with specific data quality issue
- Log to logs/step02_extract_cognitive_tests.log
- Quit immediately, invoke g_debug

### Step 3: Merge Analysis Dataset
**Dependencies:** Steps 1-2 (domain theta + cognitive tests)
**Complexity:** Low (~3 minutes)

**Purpose:** Create complete analysis dataset merging domain theta scores with cognitive predictors

**Input:**
- data/step01_domain_theta_scores.csv (dependent variables)
- data/step02_cognitive_tests.csv (independent variables)

**Processing:**
- Inner join datasets on UID to ensure complete cases only
- Final dataset structure: UID, What_theta, Where_theta, When_theta, RAVLT_z, BVMT_z, NART_z, RPM_z, Age_z
- Verify complete data: no missing values in merged dataset
- Compute descriptive statistics for all variables
- Generate data quality summary: N, means, SDs, ranges
- Split dataset conceptually for cross-validation preparation (seed=42)

**Output:**
- data/step03_analysis_dataset.csv
- data/step03_descriptive_stats.csv

**Validation Requirement:**
Validation tools MUST be used after dataset merging.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_analysis_dataset.csv: N=100 rows x 9 columns
- Columns: UID (object), 3 theta scores (float64), 5 predictors (float64)
- data/step03_descriptive_stats.csv: summary statistics

*Value Ranges:*
- Complete dataset with no missing values
- Theta scores in [-3, 3]
- Standardized predictors in [-3, 3]
- All variables have valid numeric ranges

*Data Quality:*
- Exactly 100 complete cases after merging
- No duplicate UIDs
- All variables have reasonable distributions
- No extreme outliers (>4 SDs from mean)

*Log Validation:*
- Required pattern: "Dataset merge complete: 100 complete cases"
- Required pattern: "No missing data in final dataset"
- Required pattern: "Descriptive statistics computed"
- Forbidden patterns: "ERROR", "missing data", "duplicate UIDs"

**Expected Behavior on Validation Failure:**
- Raise error with specific merge issue
- Log to logs/step03_merge_dataset.log
- Quit immediately, invoke g_debug

### Step 4: Fit Univariate Models
**Dependencies:** Step 3 (complete analysis dataset)
**Complexity:** Medium (~10 minutes including diagnostics)

**Purpose:** Fit separate regression models for each domain to establish baseline prediction performance

**Input:**
- data/step03_analysis_dataset.csv

**Processing:**
- Fit three separate multiple regression models:
  - Model 1: What_theta ~ RAVLT_z + BVMT_z + NART_z + RPM_z + Age_z
  - Model 2: Where_theta ~ RAVLT_z + BVMT_z + NART_z + RPM_z + Age_z
  - Model 3: When_theta ~ RAVLT_z + BVMT_z + NART_z + RPM_z + Age_z
- Implementation: statsmodels.api.OLS with standardized predictors
- Extract model statistics: R², adjusted R², F-statistic, AIC, BIC
- Extract coefficient statistics: beta, SE, t-value, p-value for each predictor
- Sum univariate AIC values for model comparison baseline
- Cross-validation for each model:
  - Implement 5-fold cross-validation using sklearn.model_selection.KFold
  - Random seed: 42 for reproducibility
  - Shuffle: True (randomize before splitting)
  - For each fold: fit on training (80%), evaluate on test (20%)
  - Compute mean and std of R² across folds
  - Flag overfitting if train-test R² gap > 0.10
- Assumption checking for each model:
  - Normality: Shapiro-Wilk test on residuals
  - Homoscedasticity: Breusch-Pagan test
  - Multicollinearity: VIF for each predictor
- Remedial actions if violated:
  - Normality p < 0.05: Use bootstrap CIs (1000 iterations, seed=42)
  - Heteroscedasticity p < 0.05: Report HC3 robust SEs
  - VIF > 5: Document, consider ridge if VIF > 10
  - Outliers (Cook's D > 4/n): Report with/without

**Output:**
- data/step04_univariate_models.csv
- data/step04_univariate_coefficients.csv
- data/step04_univariate_cv_results.csv
- data/step04_univariate_diagnostics.csv

**Validation Requirement:**
Validation tools MUST be used after univariate model fitting.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_univariate_models.csv: 3 rows x 8 columns
- Columns: domain, R2, adj_R2, F_stat, p_value, AIC, BIC, df_resid
- data/step04_univariate_coefficients.csv: 15 rows x 7 columns (5 predictors x 3 domains)
- data/step04_univariate_cv_results.csv: 3 rows x 4 columns (CV performance)
- data/step04_univariate_diagnostics.csv: assumption test results

*Value Ranges:*
- R² in [0, 1]
- AIC values positive and reasonable for sample size
- p-values in [0, 1]
- VIF values in [1, 10] (acceptable multicollinearity)
- CV R² should be within 0.10 of training R² (overfitting check)

*Data Quality:*
- All 3 models converged successfully
- No convergence warnings or errors
- Assumption tests completed for all models
- CV results stable across folds (SD < 0.15)

*Log Validation:*
- Required pattern: "Univariate models fitted: 3 domains"
- Required pattern: "Cross-validation complete: 5 folds"
- Required pattern: "Assumption checks complete"
- Required pattern: "VIF values acceptable: all < 5"
- Forbidden patterns: "convergence failed", "ERROR", "singular matrix"

**Expected Behavior on Validation Failure:**
- Raise error with specific model fitting issue
- Log to logs/step04_fit_univariate_models.log
- Quit immediately, invoke g_debug

### Step 5: Fit Multivariate Model
**Dependencies:** Step 4 (univariate baseline)
**Complexity:** Medium (~10 minutes including diagnostics)

**Purpose:** Fit joint multivariate model predicting all three domains simultaneously

**Input:**
- data/step03_analysis_dataset.csv

**Processing:**
- Fit multivariate regression (MANOVA framework):
  - DVs: [What_theta, Where_theta, When_theta] ~ RAVLT_z + BVMT_z + NART_z + RPM_z + Age_z
  - Implementation: statsmodels.multivariate.manova.MANOVA
- Extract multivariate statistics:
  - Pillai's trace, Wilks' lambda, Hotelling's T², Roy's largest root
  - Overall multivariate F-statistic and p-value
  - Multivariate effect sizes: partial eta-squared
- Compute multivariate AIC for model comparison
- Extract individual coefficient matrices for each domain
- Cross-validation for multivariate model:
  - Implement 5-fold cross-validation using sklearn.model_selection.KFold
  - Random seed: 42 for reproducibility
  - Shuffle: True (randomize before splitting)
  - For each fold: fit multivariate model, predict all domains
  - Compute mean and std of overall prediction accuracy across folds
  - Compare multivariate CV performance to univariate CV average
- Multivariate assumption checking:
  - Multivariate normality: Mardia's test on residuals
  - Homoscedasticity: Box's M test for equality of covariance matrices
  - Multicollinearity: condition number of design matrix
- Remedial actions if violated:
  - Multivariate normality p < 0.05: Use bootstrap CIs (1000 iterations, seed=42)
  - Heteroscedasticity p < 0.05: Report robust multivariate SEs
  - High condition number (>30): Document multicollinearity concerns

**Output:**
- data/step05_multivariate_model.csv
- data/step05_multivariate_coefficients.csv
- data/step05_multivariate_cv_results.csv
- data/step05_multivariate_diagnostics.csv

**Validation Requirement:**
Validation tools MUST be used after multivariate model fitting.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_multivariate_model.csv: 1 row x 8 columns
- Columns: Pillai_trace, Wilks_lambda, Hotelling_T2, F_stat, p_value, AIC, partial_eta2, df
- data/step05_multivariate_coefficients.csv: coefficient matrix (5 predictors x 3 domains)
- data/step05_multivariate_cv_results.csv: CV performance summary
- data/step05_multivariate_diagnostics.csv: multivariate assumption results

*Value Ranges:*
- Pillai's trace in [0, 3] (3 DVs maximum)
- Wilks' lambda in [0, 1]
- F-statistic > 0 with reasonable p-value
- AIC positive and comparable to univariate sum
- Partial eta-squared in [0, 1]

*Data Quality:*
- Multivariate model converged successfully
- All test statistics computed without error
- CV performance stable and interpretable
- Assumption tests completed successfully

*Log Validation:*
- Required pattern: "Multivariate model fitted successfully"
- Required pattern: "MANOVA statistics computed"
- Required pattern: "Cross-validation complete: multivariate design"
- Required pattern: "Assumption checks: multivariate normality tested"
- Forbidden patterns: "convergence failed", "singular covariance", "ERROR"

**Expected Behavior on Validation Failure:**
- Raise error with specific multivariate modeling issue
- Log to logs/step05_fit_multivariate_model.log
- Quit immediately, invoke g_debug

### Step 6: Model Comparison
**Dependencies:** Steps 4-5 (both univariate and multivariate models)
**Complexity:** Medium (~8 minutes)

**Purpose:** Compare efficiency and performance of univariate vs multivariate approaches

**Input:**
- data/step04_univariate_models.csv
- data/step05_multivariate_model.csv
- data/step04_univariate_cv_results.csv
- data/step05_multivariate_cv_results.csv

**Processing:**
- AIC comparison:
  - Sum univariate AIC values (baseline approach)
  - Compare to multivariate AIC (joint modeling)
  - Compute ΔAIC = AIC_multivariate - AIC_univariate_sum
  - Interpret: ΔAIC > 10 (strong evidence), 4-10 (moderate), <4 (weak)
  - Note limitations: summed univariate AIC as theoretical baseline
- Cross-validation comparison:
  - Compare univariate average CV R² to multivariate CV performance
  - Test for overfitting: training vs test performance gaps
  - Assess model stability: CV standard deviations
  - Compute efficiency ratio: multivariate performance / univariate average
- Effect size comparison:
  - Compare univariate R² values to multivariate partial eta-squared
  - Convert to Cohen's f² for standardized effect size comparison
  - Bootstrap confidence intervals for effect size differences:
    - Iterations: 1000
    - Random seed: 42
    - Method: Participant-level resampling with replacement
    - CI: Percentile method (2.5th, 97.5th percentiles)
- Statistical significance testing:
  - Test whether multivariate approach significantly outperforms univariate
  - Use nested F-test comparing full multivariate vs constrained univariate models
  - Family: Model comparison tests (AIC, CV, effect sizes)
  - Bonferroni correction: alpha = 0.05/3 = 0.0167 per test
  - Report BOTH uncorrected AND corrected p-values (Decision D068)

**Output:**
- data/step06_model_comparison.csv
- data/step06_effect_size_comparison.csv
- data/step06_significance_tests.csv

**Validation Requirement:**
Validation tools MUST be used after model comparison analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_model_comparison.csv: 1 row x 10 columns
- Columns: AIC_univariate, AIC_multivariate, delta_AIC, CV_univariate, CV_multivariate, efficiency_ratio, interpretation
- data/step06_effect_size_comparison.csv: effect sizes with bootstrap CIs
- data/step06_significance_tests.csv: statistical test results with dual p-values

*Value Ranges:*
- AIC values positive and reasonable
- ΔAIC in reasonable range (typically -50 to +50)
- CV R² values in [0, 1]
- Efficiency ratio in [0.5, 2.0] (reasonable performance range)
- p-values in [0, 1] with both uncorrected and corrected versions

*Data Quality:*
- Model comparison completed without computational errors
- Bootstrap CIs successfully computed (1000 iterations)
- Statistical tests converged properly
- Dual p-value reporting consistent with Decision D068

*Log Validation:*
- Required pattern: "Model comparison complete"
- Required pattern: "AIC difference computed: delta_AIC = X"
- Required pattern: "Bootstrap CIs computed: 1000 iterations"
- Required pattern: "Dual p-values reported (Decision D068)"
- Forbidden patterns: "ERROR", "bootstrap failed", "invalid comparison"

**Expected Behavior on Validation Failure:**
- Raise error with specific comparison issue
- Log to logs/step06_model_comparison.log
- Quit immediately, invoke g_debug

### Step 7: Individual Predictor Analysis
**Dependencies:** Steps 4-6 (complete model comparison)
**Complexity:** Medium (~10 minutes)

**Purpose:** Examine individual predictor contributions in both univariate and multivariate contexts

**Input:**
- data/step04_univariate_coefficients.csv
- data/step05_multivariate_coefficients.csv

**Processing:**
- Extract standardized coefficients for each predictor:
  - Univariate context: beta coefficients from separate domain models
  - Multivariate context: beta coefficients from joint model
- Compute effect sizes:
  - Standardized beta coefficients as primary effect size measure
  - Cohen's f² for each predictor: f² = R²_change / (1 - R²_full)
  - Bootstrap confidence intervals for all coefficients:
    - Iterations: 1000
    - Random seed: 42
    - Method: Participant-level resampling with replacement
    - CI: Percentile method (2.5th, 97.5th percentiles)
- Multiple comparison corrections:
  - Family: Within-RQ predictor tests (5 predictors × 2 contexts = 10 tests)
  - Bonferroni: alpha = 0.05/10 = 0.005 per test
  - Also compute FDR using Benjamini-Hochberg procedure
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Predictor importance ranking:
  - Rank predictors by absolute standardized beta within each context
  - Compare rankings between univariate and multivariate approaches
  - Assess consistency: Spearman correlation between rankings
- Predictor-domain specificity analysis:
  - Identify domain-specific vs general predictors
  - Test differential effects across domains using interaction contrasts
  - Assess whether multivariate modeling reveals different patterns

**Output:**
- data/step07_predictor_coefficients.csv
- data/step07_predictor_effect_sizes.csv
- data/step07_predictor_rankings.csv
- data/step07_predictor_significance.csv

**Validation Requirement:**
Validation tools MUST be used after predictor analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_predictor_coefficients.csv: 5 predictors × 2 contexts = 10 rows
- Columns: predictor, context, domain, beta, se, ci_lower, ci_upper
- data/step07_predictor_effect_sizes.csv: Cohen's f² values with CIs
- data/step07_predictor_rankings.csv: importance rankings by context
- data/step07_predictor_significance.csv: p-values (uncorrected and corrected)

*Value Ranges:*
- Standardized betas in [-2, 2] (reasonable range for standardized predictors)
- Standard errors > 0
- Bootstrap CIs valid (ci_lower < beta < ci_upper)
- p-values in [0, 1]
- Cohen's f² in [0, 2] (small to large effects)

*Data Quality:*
- All 5 predictors analyzed in both contexts
- Bootstrap CIs successfully computed for all coefficients
- Rankings consistent and interpretable
- Dual p-values present for all tests (Decision D068)

*Log Validation:*
- Required pattern: "Predictor analysis complete: 5 predictors"
- Required pattern: "Bootstrap CIs computed: 1000 iterations"
- Required pattern: "Multiple comparison corrections applied"
- Required pattern: "Dual p-values reported (Decision D068)"
- Forbidden patterns: "ERROR", "convergence failed", "invalid coefficients"

**Expected Behavior on Validation Failure:**
- Raise error with specific predictor analysis issue
- Log to logs/step07_predictor_analysis.log
- Quit immediately, invoke g_debug

### Step 8: Power Analysis and Effect Size Summary
**Dependencies:** Steps 4-7 (complete analysis)
**Complexity:** Low (~5 minutes)

**Purpose:** Conduct post-hoc power analysis and summarize effect sizes for interpretation

**Input:**
- data/step06_model_comparison.csv
- data/step07_predictor_effect_sizes.csv

**Processing:**
- Post-hoc power analysis for univariate models:
  - Given: N=100, 5 predictors, observed R² values
  - Calculate: achieved power for observed effect sizes
  - Use: statsmodels.stats.power.FTestAnovaPower()
  - Alpha level: 0.05 (individual model level)
  - Report: power for each domain model
- Post-hoc power analysis for multivariate model:
  - Given: N=100, 5 predictors, 3 DVs, observed multivariate effect size
  - Calculate: achieved power for multivariate F-test
  - Alpha level: 0.05
  - Report: power for overall multivariate test
- Effect size interpretation:
  - Cohen's conventions for R² and f²
  - Small (f² = 0.02), medium (f² = 0.15), large (f² = 0.35)
  - Practical significance thresholds for cognitive prediction
- Sensitivity analysis:
  - Minimum detectable effect sizes given N=100 and alpha levels
  - Power curves for different sample sizes
  - Implications for future research design

**Output:**
- data/step08_power_analysis.csv
- data/step08_effect_size_summary.csv

**Validation Requirement:**
Validation tools MUST be used after power analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_power_analysis.csv: power calculations for all models
- Columns: model_type, effect_size, power, minimum_detectable_effect
- data/step08_effect_size_summary.csv: effect size interpretations

*Value Ranges:*
- Power values in [0, 1]
- Effect sizes (f²) in [0, 2]
- R² values in [0, 1]
- Minimum detectable effects reasonable for sample size

*Data Quality:*
- Power calculations completed for all models
- Effect size interpretations follow Cohen's conventions
- Sensitivity analysis results reasonable and interpretable

*Log Validation:*
- Required pattern: "Power analysis complete: all models"
- Required pattern: "Effect size summary generated"
- Required pattern: "Sensitivity analysis complete"
- Forbidden patterns: "ERROR", "power calculation failed"

**Expected Behavior on Validation Failure:**
- Raise error with specific power analysis issue
- Log to logs/step08_power_analysis.log
- Quit immediately, invoke g_debug

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (prerequisite checks)
- data/step01_domain_theta_scores.csv (What/Where/When theta scores)
- data/step01_domain_correlations.csv (domain intercorrelations)
- data/step02_cognitive_tests.csv (standardized cognitive predictors)
- data/step02_predictor_correlations.csv (predictor intercorrelations)
- data/step03_analysis_dataset.csv (complete merged dataset)
- data/step03_descriptive_stats.csv (descriptive statistics)
- data/step04_univariate_models.csv (3 separate model results)
- data/step04_univariate_coefficients.csv (univariate predictor effects)
- data/step04_univariate_cv_results.csv (cross-validation performance)
- data/step04_univariate_diagnostics.csv (assumption test results)
- data/step05_multivariate_model.csv (joint model results)
- data/step05_multivariate_coefficients.csv (multivariate predictor effects)
- data/step05_multivariate_cv_results.csv (multivariate CV performance)
- data/step05_multivariate_diagnostics.csv (multivariate assumptions)
- data/step06_model_comparison.csv (AIC and CV comparisons)
- data/step06_effect_size_comparison.csv (effect size differences with CIs)
- data/step06_significance_tests.csv (statistical comparison tests)
- data/step07_predictor_coefficients.csv (predictor effects both contexts)
- data/step07_predictor_effect_sizes.csv (Cohen's f² with bootstrap CIs)
- data/step07_predictor_rankings.csv (importance rankings)
- data/step07_predictor_significance.csv (dual p-values per Decision D068)
- data/step08_power_analysis.csv (achieved power calculations)
- data/step08_effect_size_summary.csv (effect size interpretations)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_domain_theta.log
- logs/step02_extract_cognitive_tests.log
- logs/step03_merge_dataset.log
- logs/step04_fit_univariate_models.log
- logs/step05_fit_multivariate_model.log
- logs/step06_model_comparison.log
- logs/step07_predictor_analysis.log
- logs/step08_power_analysis.log

### Plots (EMPTY until rq_plots runs)
- Plot source CSVs created in data/ folder for:
  - step04_univariate_model_comparison_plot_data.csv
  - step05_multivariate_diagnostics_plot_data.csv
  - step06_model_performance_comparison_plot_data.csv
  - step07_predictor_importance_plot_data.csv

### Results (EMPTY until rq_results runs)
- results/summary.md (created by rq_results agent)

---

## Expected Data Formats

### Step-to-Step Transformations
1. **Ch5 theta scores → Domain matrix:** Individual domain files merged into single dataset
2. **Master.xlsx → Standardized predictors:** Cognitive tests extracted and z-scored
3. **Domain + predictors → Analysis dataset:** Complete case merging for regression
4. **Analysis dataset → Model outputs:** Statistical model fitting and extraction
5. **Model outputs → Comparisons:** AIC, CV, and effect size comparisons
6. **Comparisons → Interpretations:** Effect sizes and power analysis

### Column Naming Conventions
- **Participant IDs:** UID (consistent across all files)
- **Domain scores:** What_theta, Where_theta, When_theta
- **Predictors:** RAVLT_z, BVMT_z, NART_z, RPM_z, Age_z (z-score suffix)
- **Statistics:** R2, adj_R2, AIC, BIC, F_stat, p_value
- **Effect sizes:** cohens_f2, partial_eta2, beta, se
- **CIs:** ci_lower, ci_upper (bootstrap percentile method)
- **Corrections:** p_uncorrected, p_bonferroni, p_fdr (Decision D068)

### Data Type Constraints
- **UID:** object/string (no missing values)
- **Theta scores:** float64 in [-3, 3] (no missing in final dataset)
- **Predictors:** float64, standardized (no missing in final dataset)
- **Statistics:** float64, positive where applicable (R², AIC, etc.)
- **p-values:** float64 in [0, 1] (dual reporting required)

---

## Cross-RQ Dependencies

**Ch5 Domain-Specific Analyses:**
- **5.2.1:** What domain IRT calibration and theta estimation
- **5.2.2:** Where domain IRT calibration and theta estimation  
- **5.2.3:** When domain IRT calibration and theta estimation

**Expected Ch5 Outputs:**
- Domain-specific theta scores for all 100 participants
- IRT model parameters and fit statistics
- Standard errors for theta estimates

**Dependency Validation:**
Step 0 checks Ch5 5.2.X completion status and locates required theta score files using multiple fallback patterns to accommodate potential naming variations.

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
- **Files:** Dependency validation text file
- **Ranges:** Status checks and file counts
- **Quality:** All Ch5 RQs complete, theta files accessible
- **Logs:** Required success patterns, forbidden error patterns

#### Step 1: Domain Theta Extraction  
- **Files:** Domain theta scores (100x4) and correlation matrix (3x3)
- **Ranges:** Theta in [-3,3], correlations in [0.2,0.7]
- **Quality:** Complete cases, no missing data, moderate correlations
- **Logs:** Success extraction patterns, correlation validation

#### Step 2: Cognitive Test Extraction
- **Files:** Standardized cognitive tests (100x6) and correlation matrix (5x5)
- **Ranges:** Z-scores in [-3,3], predictor correlations <0.8
- **Quality:** Complete standardization, multicollinearity check passed
- **Logs:** Standardization success, correlation bounds validated

#### Step 3: Dataset Merging
- **Files:** Complete analysis dataset (100x9) and descriptive stats
- **Ranges:** All variables in expected ranges, no missing values
- **Quality:** Perfect merge success, no duplicates or missing cases
- **Logs:** Merge completion, data quality confirmation

#### Step 4: Univariate Models
- **Files:** Model results, coefficients, CV results, diagnostics
- **Ranges:** R² in [0,1], VIF <5, reasonable AIC values
- **Quality:** All models converged, assumptions checked, CV stable
- **Logs:** Model convergence, assumption tests, CV completion

#### Step 5: Multivariate Model
- **Files:** MANOVA results, coefficients, CV results, diagnostics
- **Ranges:** Test statistics in valid ranges, AIC comparable
- **Quality:** Model convergence, multivariate assumptions checked
- **Logs:** MANOVA success, assumption validation, CV completion

#### Step 6: Model Comparison
- **Files:** AIC comparison, effect sizes, significance tests
- **Ranges:** Valid comparison metrics, bootstrap CIs, dual p-values
- **Quality:** Bootstrap success (1000 iterations), valid statistical tests
- **Logs:** Comparison completion, bootstrap success, dual reporting

#### Step 7: Predictor Analysis
- **Files:** Coefficients, effect sizes, rankings, significance tests
- **Ranges:** Valid effect sizes, bootstrap CIs, corrected p-values
- **Quality:** All predictors analyzed, multiple corrections applied
- **Logs:** Analysis completion, corrections applied, dual reporting

#### Step 8: Power Analysis
- **Files:** Power calculations and effect size summary
- **Ranges:** Power in [0,1], effect sizes reasonable
- **Quality:** All models analyzed, interpretations provided
- **Logs:** Power calculations complete, summary generated

---

## Summary

**Total Steps:** 9 (1 validation + 8 analysis)
**Estimated Runtime:** ~45 minutes
**Cross-RQ Dependencies:** Ch5 5.2.1, 5.2.2, 5.2.3 (domain theta scores)
**Primary Outputs:** Model comparison results with efficiency assessment
**Validation Coverage:** 100% (all 9 steps have 4-layer validation requirements)

**Key Hypothesis:** Multivariate model should fit training data better due to modeling cross-domain covariances, but efficiency gain may not persist in cross-validation due to increased complexity and potential overfitting.

**Critical Methodological Notes:**
- AIC comparison uses summed univariate as theoretical baseline with caveats
- Cross-validation serves as primary performance comparison metric
- Bootstrap confidence intervals provide robust effect size estimation
- Dual p-value reporting (Decision D068) applied throughout
- Random seed=42 ensures reproducibility across all randomized procedures
- Comprehensive assumption checking with specified remedial actions

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan → creates 3_tools.yaml
3. rq_analysis reads plan + tools → creates 4_analysis.yaml  
4. g_code reads analysis → generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent v5.1 with enhanced statistical specifications