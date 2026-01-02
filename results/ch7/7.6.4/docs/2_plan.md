# Analysis Plan: RQ 7.6.4 - Purification & Slope Predictors

**Research Question:** 7.6.4
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

**Brief Description:** Examines whether cognitive test predictors (RAVLT, BVMT, RPM) of forgetting slope differ between pre-purification (IRT Pass 1) and post-purification (IRT Pass 2) models. Tests the purification-trajectory paradox identified in Chapter 5.

**Pipeline:** Multiple Linear Regression with Pre/Post Comparison
**Steps:** 8 total analysis steps (Step 0: dependency validation + Steps 1-7: analysis)
**Estimated Runtime:** ~45 minutes including bootstrap procedures

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Dependent samples approach (addresses correlated pre/post slopes)
- Participant-level bootstrap resampling (preserves individual structure)

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies

**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 outputs exist and contain valid slope estimates before proceeding

**Input:**
- Primary: results/ch5/5.2.5/status.yaml (verify completion)
- Alternative: results/ch5/5.2.*/status.yaml (search pattern for slope analysis)
- Slope files: results/ch5/5.2.5/data/step*_pass*_slopes.csv
- Fallback: results/ch5/5.2.*/data/*slope*.{csv,txt}
- Master data: data/cache/master.xlsx
- Expected: Pre- and post-purification slope estimates for 100 participants

**Processing:**
- Check Ch5 status shows rq_results = success
- Locate pre-purification slope file (Pass 1 output)
- Locate post-purification slope file (Pass 2 output)  
- Verify master.xlsx contains cognitive test data
- Check slope files contain required columns: UID, slope_estimate
- Validate N=100 participants in both slope files
- Log all validation checks with timestamps

**Output:**
- data/step00_dependency_validation.txt (validation log)

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: Text file, >20 lines
- Content: Validation status for each dependency

*Value Ranges:*
- Participant count in [95, 105] (allowing minor exclusions)
- Slope estimates in [-2, 2] per day (reasonable forgetting rates)
- No extreme outliers (>|3| standard deviations)

*Data Quality:*
- All required files found and accessible
- Slope files contain UID + slope_estimate columns minimum
- Master.xlsx contains RAVLT, BVMT, RPM columns
- No critical missing dependencies

*Log Validation:*
- Required patterns: "VALIDATION PASS", "Files located successfully"
- Required patterns: "Participant count: 100" (or similar)
- Forbidden patterns: "ERROR", "File not found", "VALIDATION FAIL"

**Expected Behavior on Validation Failure:**
- Raise ValueError with specific missing dependency
- Log to logs/step00_validate_dependencies.log
- QUIT immediately, invoke g_debug agent

---

### Step 1: Extract and Standardize Data

**Dependencies:** Step 0 (dependency validation)
**Complexity:** Medium (~5 minutes)

**Purpose:** Load pre/post-purification slopes and cognitive test data, standardize to T-scores

**Input:**
- data/step00_dependency_validation.txt (confirmed file paths)
- Ch5 slope files: *pass1_slopes.csv, *pass2_slopes.csv
- data/cache/master.xlsx (sheet: demographics, cognitive tests)

**Processing:**
- Load pre-purification slopes (Pass 1) with columns: UID, slope_pass1
- Load post-purification slopes (Pass 2) with columns: UID, slope_pass2
- Extract cognitive tests: RAVLT_Total, BVMT_Total, RPM_Total
- Extract demographics: Age, Sex, Education
- Merge datasets on UID (inner join, require all data)
- Standardize cognitive tests to T-scores: T = 50 + 10 * (X - mean_X) / sd_X
- Standardize slopes to T-scores for comparison: T = 50 + 10 * (X - mean_X) / sd_X
- Check for missing data: exclude participants with >20% missing cognitive data
- Final dataset: N=100 (or excluded count) with complete data

**Output:**
- data/step01_merged_standardized.csv (analysis-ready dataset)
- data/step01_descriptive_stats.csv (means, SDs, correlations)

**Validation Requirement:**
Validation tools MUST be used after data extraction and standardization.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_merged_standardized.csv: 95-105 rows x 8+ columns
- Columns: UID, slope_pass1_T, slope_pass2_T, RAVLT_T, BVMT_T, RPM_T, Age, Sex, Education
- data/step01_descriptive_stats.csv: summary statistics

*Value Ranges:*
- T-scores in [20, 80] (allowing 3 SDs from mean=50)
- Age in [18, 80] years
- Sex in [0, 1] or ['M', 'F']
- Education in [8, 25] years

*Data Quality:*
- No missing values in cognitive T-scores
- Slope correlation r=0.3-0.8 between passes (some consistency expected)
- Standard deviations ~10 for T-scores (standardization check)
- Final N >= 95 participants

*Log Validation:*
- Required patterns: "Standardization complete", "Final N = [number]"
- Required patterns: "Correlation pass1-pass2 = [value]"
- Forbidden patterns: "ERROR", "Missing data >20%", "Merge failed"

**Expected Behavior on Validation Failure:**
- Report specific validation failure (range, missing data, correlation)
- Log to logs/step01_extract_standardize.log
- Continue to next step if N>=95, else QUIT

---

### Step 2: Fit Pre-Purification Prediction Model

**Dependencies:** Step 1 (standardized dataset)
**Complexity:** Medium (~8 minutes including diagnostics)

**Purpose:** Fit multiple regression predicting pre-purification slopes from cognitive tests

**Input:**
- data/step01_merged_standardized.csv (standardized data)

**Processing:**
- Fit model: slope_pass1_T ~ RAVLT_T + BVMT_T + RPM_T + Age + Sex + Education
- Implementation: statsmodels.api.OLS with add_constant=True
- Extract model statistics: R², adjusted R², F-statistic, AIC, BIC
- Extract coefficients with standard errors for all predictors
- Compute semi-partial correlations (sr²) for unique variance
- Bootstrap confidence intervals for coefficients:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Resampling unit: Participant-level (preserve individual structure)
  - Method: Resample participants WITH replacement
  - CI: Percentile method (2.5th, 97.5th percentiles)
- Check model assumptions:
  - Multicollinearity: VIF < 5 for all predictors
  - Normality: Shapiro-Wilk test on residuals (p > 0.05)
  - Homoscedasticity: Breusch-Pagan test (p > 0.05)
  - Linearity: Partial residual plots visual inspection
  - Outliers: Cook's D > 4/N threshold (0.04 for N=100)
- Remedial actions if assumptions violated:
  - Normality p < 0.05: Report bootstrap CIs as primary inference
  - Heteroscedasticity p < 0.05: Add HC3 robust standard errors
  - VIF > 5: Document multicollinearity, proceed with caution
  - VIF > 10: Consider dropping most collinear predictor
  - Outliers Cook's D > 0.04: Report results with/without outliers

**Output:**
- data/step02_pass1_model_results.csv (coefficients, stats, CIs)
- data/step02_pass1_diagnostics.csv (VIF, assumption tests)
- data/step02_pass1_residuals.csv (for plotting)

**Validation Requirement:**
Validation tools MUST be used after regression model fitting.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_pass1_model_results.csv: 6 rows x 8 columns (predictors + intercept)
- Columns: predictor, beta, se, ci_lower, ci_upper, p_value, sr_squared, vif
- data/step02_pass1_diagnostics.csv: assumption test results

*Value Ranges:*
- R² in [0.10, 0.70] (realistic for individual differences)
- Beta coefficients in [-1.0, 1.0] (standardized predictors)
- Standard errors > 0
- p-values in [0, 1]
- VIF in [1, 10] (acceptable multicollinearity)

*Data Quality:*
- All 6 predictors present (3 cognitive + 3 demographic)
- Bootstrap CIs valid (ci_lower < beta < ci_upper for significant predictors)
- F-statistic p < 0.05 (overall model significance expected)
- No convergence issues

*Log Validation:*
- Required patterns: "Model fitted successfully", "R² = [value]"
- Required patterns: "Bootstrap complete: 1000 iterations"
- Required patterns: "Assumption checks complete"
- Forbidden patterns: "Convergence failed", "Singular matrix", "ERROR"

**Expected Behavior on Validation Failure:**
- Log specific assumption violations or convergence issues
- Continue with robust methods if assumptions violated
- QUIT if model fails to converge after remedial attempts

---

### Step 3: Fit Post-Purification Prediction Model

**Dependencies:** Step 1 (standardized dataset)
**Complexity:** Medium (~8 minutes including diagnostics)

**Purpose:** Fit multiple regression predicting post-purification slopes from cognitive tests

**Input:**
- data/step01_merged_standardized.csv (standardized data)

**Processing:**
- Fit model: slope_pass2_T ~ RAVLT_T + BVMT_T + RPM_T + Age + Sex + Education
- Implementation: statsmodels.api.OLS with add_constant=True
- Extract model statistics: R², adjusted R², F-statistic, AIC, BIC
- Extract coefficients with standard errors for all predictors
- Compute semi-partial correlations (sr²) for unique variance
- Bootstrap confidence intervals for coefficients:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Resampling unit: Participant-level (preserve individual structure)
  - Method: Resample participants WITH replacement
  - CI: Percentile method (2.5th, 97.5th percentiles)
- Check model assumptions (identical procedures as Step 2):
  - Multicollinearity: VIF < 5 for all predictors
  - Normality: Shapiro-Wilk test on residuals
  - Homoscedasticity: Breusch-Pagan test
  - Linearity: Partial residual plots
  - Outliers: Cook's D > 4/N threshold
- Apply same remedial actions as Step 2 for assumption violations

**Output:**
- data/step03_pass2_model_results.csv (coefficients, stats, CIs)
- data/step03_pass2_diagnostics.csv (VIF, assumption tests)
- data/step03_pass2_residuals.csv (for plotting)

**Validation Requirement:**
Validation tools MUST be used after regression model fitting.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_pass2_model_results.csv: 6 rows x 8 columns (predictors + intercept)
- Columns: predictor, beta, se, ci_lower, ci_upper, p_value, sr_squared, vif
- data/step03_pass2_diagnostics.csv: assumption test results

*Value Ranges:*
- R² in [0.05, 0.70] (may be lower than Pass 1 if purification paradox)
- Beta coefficients in [-1.0, 1.0] (standardized predictors)
- Standard errors > 0
- p-values in [0, 1]
- VIF in [1, 10] (acceptable multicollinearity)

*Data Quality:*
- All 6 predictors present (3 cognitive + 3 demographic)
- Bootstrap CIs valid for all coefficients
- Model successfully fitted
- Comparable structure to Pass 1 model

*Log Validation:*
- Required patterns: "Model fitted successfully", "R² = [value]"
- Required patterns: "Bootstrap complete: 1000 iterations"
- Required patterns: "Assumption checks complete"
- Forbidden patterns: "Convergence failed", "Singular matrix", "ERROR"

**Expected Behavior on Validation Failure:**
- Log specific assumption violations or convergence issues
- Apply same remedial procedures as Step 2
- QUIT if model fails to converge after remedial attempts

---

### Step 4: Compare Overall Model Performance

**Dependencies:** Steps 2-3 (both fitted models)
**Complexity:** Medium (~8 minutes including bootstrap)

**Purpose:** Test differences in R² and overall predictive ability between pre/post-purification models

**Input:**
- data/step02_pass1_model_results.csv (Pass 1 model statistics)
- data/step03_pass2_model_results.csv (Pass 2 model statistics)
- data/step01_merged_standardized.csv (original data for resampling)

**Processing:**
- Extract R² values from both models
- Test R² difference using dependent samples approach:
  - Null hypothesis: R²_pass1 = R²_pass2
  - Alternative: R²_pass1 ≠ R²_pass2 (two-tailed test)
- Bootstrap significance test for R² difference:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - For each iteration:
    - Resample participants WITH replacement
    - Fit both models on resampled data
    - Compute R² difference (Pass1 - Pass2)
  - Significance: 95% CI for R² difference excludes zero
- Additional model comparisons:
  - AIC difference (lower is better)
  - BIC difference (lower is better)
  - F-statistic comparison
- Multiple comparison correction:
  - Family: Model-level comparisons (R², AIC, BIC = 3 tests)
  - Bonferroni correction: alpha = 0.05/3 = 0.0167 per test
  - Also compute FDR using Benjamini-Hochberg procedure
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Effect size for R² difference:
  - Cohen's f² for R² change
  - Interpretation: 0.02=small, 0.15=medium, 0.35=large

**Output:**
- data/step04_model_comparison.csv (R² differences, CIs, p-values)
- data/step04_bootstrap_r2_differences.csv (1000 bootstrap values)

**Validation Requirement:**
Validation tools MUST be used after model comparison analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_model_comparison.csv: 3 rows x 6 columns
- Columns: metric, pass1_value, pass2_value, difference, ci_lower, ci_upper, p_uncorrected, p_bonferroni, p_fdr
- data/step04_bootstrap_r2_differences.csv: 1000 rows x 2 columns

*Value Ranges:*
- R² values in [0, 1] (valid proportion of variance)
- R² difference in [-0.5, 0.5] (realistic range)
- p-values in [0, 1]
- Cohen's f² in [0, 2] (typical effect size range)

*Data Quality:*
- Bootstrap distribution roughly normal
- Bootstrap CI contains median difference
- All 3 model comparisons completed
- Dual p-values present (Decision D068)

*Log Validation:*
- Required patterns: "Model comparison complete", "Bootstrap iterations: 1000"
- Required patterns: "R² difference = [value]", "95% CI: [range]"
- Forbidden patterns: "Bootstrap failed", "Invalid R² values", "ERROR"

**Expected Behavior on Validation Failure:**
- Report specific comparison failure (bootstrap, CI calculation)
- Log to logs/step04_model_comparison.log
- Continue if CI calculation fails, QUIT if bootstrap completely fails

---

### Step 5: Compare Individual Predictor Coefficients

**Dependencies:** Steps 2-3 (fitted models)
**Complexity:** High (~12 minutes including bootstrap)

**Purpose:** Test differences in individual cognitive test coefficients between pre/post-purification models

**Input:**
- data/step02_pass1_model_results.csv (Pass 1 coefficients)
- data/step03_pass2_model_results.csv (Pass 2 coefficients)
- data/step01_merged_standardized.csv (data for dependent samples bootstrap)

**Processing:**
- Focus on cognitive predictors: RAVLT_T, BVMT_T, RPM_T (exclude demographics)
- For each cognitive predictor, compute coefficient difference:
  - Difference = beta_pass1 - beta_pass2
  - Null hypothesis: difference = 0
- Dependent samples bootstrap for coefficient differences:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - For each iteration:
    - Resample SAME participants for both models (preserve dependency)
    - Fit both models on resampled data
    - Compute coefficient difference for each predictor
  - 95% CI: Percentile method (2.5th, 97.5th percentiles)
  - Significance: CI excludes zero
- Multiple comparison correction:
  - Family: Within-RQ cognitive predictors (3 tests)
  - Bonferroni correction: alpha = 0.05/3 = 0.0167 per test
  - FDR correction using Benjamini-Hochberg procedure
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Effect size for coefficient differences:
  - Standardized difference = difference / pooled_SE
  - Interpretation using Cohen's d conventions: 0.2=small, 0.5=medium, 0.8=large
- Identify strongest purification effects:
  - Rank predictors by absolute coefficient difference
  - Note which predictors weaken vs strengthen

**Output:**
- data/step05_coefficient_differences.csv (differences, CIs, p-values)
- data/step05_bootstrap_coefficients.csv (1000 x 6 columns for 3 predictors x 2 passes)

**Validation Requirement:**
Validation tools MUST be used after coefficient comparison analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_coefficient_differences.csv: 3 rows x 9 columns
- Columns: predictor, beta_pass1, beta_pass2, difference, effect_size, ci_lower, ci_upper, p_uncorrected, p_bonferroni, p_fdr
- data/step05_bootstrap_coefficients.csv: 1000 rows x 6 columns

*Value Ranges:*
- Beta coefficients in [-1.0, 1.0] (standardized)
- Coefficient differences in [-1.0, 1.0] (reasonable change)
- Effect sizes in [-3, 3] (Cohen's d range)
- p-values in [0, 1]

*Data Quality:*
- All 3 cognitive predictors present
- Bootstrap distributions not excessively skewed
- Triple p-values present (uncorrected, Bonferroni, FDR)
- CI bounds logical (lower < upper)

*Log Validation:*
- Required patterns: "Coefficient comparison complete", "3 predictors analyzed"
- Required patterns: "Bootstrap complete: 1000 iterations"
- Required patterns: "Multiple correction applied"
- Forbidden patterns: "Bootstrap failed", "Invalid coefficients", "ERROR"

**Expected Behavior on Validation Failure:**
- Report specific predictor or bootstrap failure
- Log to logs/step05_coefficient_differences.log
- Continue with available predictors if some fail

---

### Step 6: Power Analysis and Effect Size Assessment

**Dependencies:** Steps 4-5 (comparison results)
**Complexity:** Low (~5 minutes)

**Purpose:** Assess power for detecting observed effects and interpret effect sizes

**Input:**
- data/step04_model_comparison.csv (R² differences)
- data/step05_coefficient_differences.csv (coefficient differences)
- N=100 participants

**Processing:**
- Post-hoc power analysis for R² difference test:
  - Given: N=100, 6 predictors, observed R² difference
  - Calculate: achieved power using F-test formulation
  - Use: statsmodels.stats.power.FTestAnovaPower()
  - Alpha level: 0.0167 (Bonferroni corrected for 3 model comparisons)
  - Effect size: Cohen's f² = |R²_diff| / (1 - max(R²_pass1, R²_pass2))
- Post-hoc power for coefficient differences:
  - Given: N=100, observed effect sizes (Cohen's d)
  - Calculate: achieved power for two-sample t-test
  - Alpha level: 0.0167 (Bonferroni corrected for 3 cognitive predictors)
  - Use: statsmodels.stats.power.ttest_power()
- Sensitivity analysis:
  - Minimum detectable effect size at 80% power
  - Given current N and alpha levels
  - Report whether observed effects meet detection threshold
- Effect size interpretation using established benchmarks:
  - Cohen's f² for R²: 0.02=small, 0.15=medium, 0.35=large
  - Cohen's d for coefficients: 0.2=small, 0.5=medium, 0.8=large
- Power adequacy assessment:
  - Flag analyses with power < 0.80
  - Acknowledge limitations for small effects

**Output:**
- data/step06_power_analysis.csv (achieved power, minimum detectable effects)
- data/step06_effect_size_interpretation.csv (effect categories, benchmarks)

**Validation Requirement:**
Validation tools MUST be used after power analysis completion.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_power_analysis.csv: 4 rows x 5 columns (R² + 3 coefficients)
- Columns: analysis, effect_size, power_achieved, min_detectable_80, adequate_power
- data/step06_effect_size_interpretation.csv: effect size categories and meanings

*Value Ranges:*
- Power values in [0, 1] (valid probability)
- Effect sizes >= 0 (absolute values)
- Minimum detectable effects > 0

*Data Quality:*
- All 4 power calculations completed (1 R² + 3 coefficients)
- Power adequacy flagged (TRUE/FALSE for >= 0.80)
- Effect size interpretations match Cohen's conventions
- Realistic minimum detectable effects

*Log Validation:*
- Required patterns: "Power analysis complete", "4 analyses conducted"
- Required patterns: "Minimum detectable effect calculated"
- Forbidden patterns: "Power calculation failed", "Invalid effect size", "ERROR"

**Expected Behavior on Validation Failure:**
- Report specific power calculation failure
- Log to logs/step06_power_analysis.log
- Continue without power estimates if calculations fail

---

### Step 7: Comprehensive Results Summary

**Dependencies:** Steps 1-6 (all analysis components)
**Complexity:** Medium (~8 minutes)

**Purpose:** Synthesize all results into comprehensive summary addressing purification paradox hypothesis

**Input:**
- data/step01_descriptive_stats.csv (sample characteristics)
- data/step04_model_comparison.csv (R² differences)
- data/step05_coefficient_differences.csv (coefficient changes)
- data/step06_power_analysis.csv (power adequacy)

**Processing:**
- Create comprehensive results summary:
  - Sample characteristics (N, demographics, cognitive test scores)
  - Pre-purification model: R², significant predictors
  - Post-purification model: R², significant predictors
  - Model comparison: R² difference with CI and significance
  - Strongest coefficient changes with effect sizes
  - Power adequacy for all tests
- Hypothesis evaluation:
  - Primary: "Predictor relationships will weaken after purification"
  - Evidence: R² comparison and individual coefficient changes
  - Strength: Effect sizes and confidence intervals
  - Statistical significance with multiple testing corrections
- Purification paradox assessment:
  - Consistent with Ch5 findings? (trajectory patterns changed)
  - Which predictors most affected by purification?
  - Implications for IRT methodology in longitudinal research
- Methodological quality indicators:
  - Assumption violation rates and remedial actions taken
  - Power adequacy for primary hypotheses
  - Effect size magnitudes and interpretability
- Limitations acknowledgment:
  - Dependency between pre/post slopes from same participants
  - Power limitations for small effect detection
  - Generalizability to other IRT purification approaches

**Output:**
- data/step07_comprehensive_summary.csv (all key statistics)
- data/step07_hypothesis_evaluation.txt (structured interpretation)

**Validation Requirement:**
Validation tools MUST be used after comprehensive summary creation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_comprehensive_summary.csv: summary table with all key statistics
- data/step07_hypothesis_evaluation.txt: structured text interpretation, >30 lines

*Value Ranges:*
- All previously validated ranges maintained
- Summary statistics consistent across files
- No contradictory results between steps

*Data Quality:*
- All analysis components represented
- Hypothesis evaluation directly addresses research question
- Limitations appropriately acknowledged
- Statistical significance properly interpreted with corrections

*Log Validation:*
- Required patterns: "Comprehensive summary complete"
- Required patterns: "Hypothesis evaluation: [conclusion]"
- Required patterns: "Power adequate for [N] tests"
- Forbidden patterns: "Inconsistent results", "Missing components", "ERROR"

**Expected Behavior on Validation Failure:**
- Report specific summary component failure
- Log to logs/step07_comprehensive_summary.log
- Generate partial summary if some components available

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (dependency checks)
- data/step01_merged_standardized.csv (analysis-ready dataset)
- data/step01_descriptive_stats.csv (sample characteristics)
- data/step02_pass1_model_results.csv (pre-purification model)
- data/step02_pass1_diagnostics.csv (assumption checks)
- data/step02_pass1_residuals.csv (residual values)
- data/step03_pass2_model_results.csv (post-purification model)
- data/step03_pass2_diagnostics.csv (assumption checks)
- data/step03_pass2_residuals.csv (residual values)
- data/step04_model_comparison.csv (R² differences)
- data/step04_bootstrap_r2_differences.csv (bootstrap results)
- data/step05_coefficient_differences.csv (predictor changes)
- data/step05_bootstrap_coefficients.csv (bootstrap coefficients)
- data/step06_power_analysis.csv (power calculations)
- data/step06_effect_size_interpretation.csv (effect size categories)
- data/step07_comprehensive_summary.csv (final results)
- data/step07_hypothesis_evaluation.txt (interpretation)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_standardize.log
- logs/step02_fit_pass1_model.log
- logs/step03_fit_pass2_model.log
- logs/step04_model_comparison.log
- logs/step05_coefficient_differences.log
- logs/step06_power_analysis.log
- logs/step07_comprehensive_summary.log

### Plots (EMPTY until rq_plots runs)
Plot source CSVs created in data/ for later visualization:
- data/step02_pass1_residuals.csv (diagnostic plots)
- data/step03_pass2_residuals.csv (diagnostic plots)
- data/step05_coefficient_differences.csv (comparison plots)

### Results (EMPTY until rq_results runs)
summary.md will be created by rq_results combining all analysis outputs

---

## Expected Data Formats

### Step-to-Step Transformations
1. **Step 0->1:** Dependency paths -> Merged standardized dataset
2. **Step 1->2:** Standardized data -> Pass 1 model with diagnostics
3. **Step 1->3:** Standardized data -> Pass 2 model with diagnostics  
4. **Step 2,3->4:** Both models -> R² comparison with bootstrap
5. **Step 2,3->5:** Both models -> Coefficient differences with bootstrap
6. **Step 4,5->6:** Effect sizes -> Power analysis and adequacy
7. **Step 1-6->7:** All components -> Comprehensive summary

### Column Naming Conventions
- **UIDs:** Consistent participant identifiers across all files
- **T-scores:** Variables ending in "_T" are standardized (M=50, SD=10)
- **P-values:** Triple format: p_uncorrected, p_bonferroni, p_fdr
- **CIs:** ci_lower, ci_upper for 95% confidence intervals
- **Effect sizes:** Cohen's conventions with interpretation labels

### Data Type Constraints
- **UIDs:** String/object type, no missing values
- **Numeric variables:** Float64, allow NaN only for derived calculations
- **Categorical variables:** String for sex, integer for education years
- **Boolean flags:** True/False for power adequacy, assumption violations

---

## Cross-RQ Dependencies

### Required Ch5 Outputs
- **Slope estimates:** Pre/post-purification individual slopes
- **File patterns:** results/ch5/5.2.*/data/*slope*.csv
- **Fallback strategy:** Multiple search patterns with error messages
- **Content requirements:** UID + slope columns minimum

### Master Data Requirements
- **File:** data/cache/master.xlsx
- **Required sheets:** Demographics, cognitive test scores
- **Critical variables:** RAVLT_Total, BVMT_Total, RPM_Total, Age, Sex, Education

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
- Output existence and accessibility
- File format verification (CSV structure, required columns)
- Sample size adequacy (N>=95 participants)
- Range validation for slope estimates

#### Step 1: Extract and Standardize
- Data merging success (inner join completion)
- T-score standardization (mean=50, SD=10 verification)
- Missing data tolerance (<20% per variable)
- Cross-correlation checks between passes

#### Step 2: Fit Pass 1 Model
- Model convergence and coefficient stability
- Assumption validation (normality, homoscedasticity, VIF)
- Bootstrap completion with valid confidence intervals
- R² within expected range for individual differences

#### Step 3: Fit Pass 2 Model
- Identical validation to Step 2
- Comparison with Pass 1 for consistency
- Assumption remedial actions if needed

#### Step 4: Compare Model Performance
- Bootstrap distribution validity
- R² difference calculation accuracy
- Multiple testing correction verification
- Effect size computation

#### Step 5: Compare Individual Coefficients
- Dependent samples bootstrap validation
- Multiple testing family definition
- Effect size interpretation alignment
- Coefficient stability across iterations

#### Step 6: Power Analysis Assessment
- Power calculation accuracy using established formulas
- Minimum detectable effect calculation
- Effect size benchmark application
- Adequacy threshold evaluation

#### Step 7: Comprehensive Summary
- Cross-step consistency verification
- Hypothesis evaluation completeness
- Statistical significance interpretation
- Limitation acknowledgment adequacy

---

## Summary

**Total Steps:** 8 (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** ~45 minutes (including bootstrap procedures)
**Cross-RQ Dependencies:** Ch5 slope analysis completion (5.2.5 or equivalent)
**Primary Outputs:** Model comparison results, coefficient differences, power assessment
**Validation Coverage:** 100% (all 8 steps have 4-layer validation requirements)

**Key Hypothesis:** Predictor relationships will weaken after purification, consistent with the Ch5 purification-trajectory paradox

**Critical Methodological Notes:**
- Dependent samples approach accounts for correlated pre/post slopes
- Participant-level bootstrap preserves individual structure
- Multiple testing corrections applied at both model and predictor levels
- Power limitations acknowledged for N=100 sample size
- Remedial actions specified for assumption violations

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent v5.1