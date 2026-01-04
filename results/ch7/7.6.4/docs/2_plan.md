# Analysis Plan: RQ 7.6.4 - Purification & Slope Predictors

**Research Question:** 7.6.4
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This analysis examines whether cognitive test predictors of forgetting slopes change after IRT purification, investigating the "purification-trajectory paradox" discovered in Chapter 5. The analysis compares multiple regression models predicting slopes from pre-purification (IRT Pass 1) vs post-purification (IRT Pass 2) data, testing whether predictor relationships weaken after purification.

**Pipeline:** Comparative Multiple Linear Regression
**Steps:** 8 total analysis steps (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** 45-60 minutes

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Bonferroni correction for multiple model comparisons
- Bootstrap confidence intervals for robust inference

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 outputs exist before proceeding with slope extraction

**Input:**
- Primary: results/ch5/5.2.5/status.yaml (verify rq_results: success)
- Alternative: results/ch5/5.2.*/ directories for slope analysis variations
- Fallback: results/ch5/*/data/*slope*.{csv,txt,rds} (find any slope output)
- Master data: data/cache/master.xlsx (cognitive test scores)

**Processing:**
- Check Ch5 5.2.5 completed successfully (or alternative slope analysis)
- Locate pre-purification slope files (Pass 1 outputs)
- Locate post-purification slope files (Pass 2 outputs) 
- Verify master.xlsx contains RAVLT, BVMT, RPM columns
- Test file accessibility and basic format validation
- Log all validation results

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with 20-50 lines
- Content: Pass/fail status for each dependency check

*Value Ranges:*
- All checks must show "PASS" status
- File sizes > 0 bytes for required inputs
- Master.xlsx row count = 100 participants

*Data Quality:*
- Ch5 slope files must exist for both passes
- Master.xlsx must be readable
- No corrupted file reports

*Log Validation:*
- Required patterns: "Ch5 dependency: PASS", "Master data: PASS"
- Forbidden patterns: "ERROR", "NOT FOUND", "CORRUPTED"
- If any dependency fails: "DEPENDENCY CHECK FAILED - STOPPING ANALYSIS"

**Expected Behavior on Validation Failure:**
Quit immediately with specific dependency error message and invoke g_debug

### Step 1: Extract Pre-Purification Slopes (IRT Pass 1)
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Medium (~8 minutes)

**Purpose:** Extract individual forgetting slopes from pre-purification IRT analysis

**Input:**
- Primary: results/ch5/5.2.5/data/step03_pass1_slopes.csv
- Alternative: results/ch5/5.2.*/data/*pass1*slope*.csv
- Fallback: results/ch5/*/data/*irt*pass*1*.{csv,txt}
- Expected format: UID, slope_estimate, slope_se columns minimum

**Processing:**
- Load pre-purification slope file using pandas.read_csv
- Verify contains UID and slope estimate columns
- Extract individual participant slopes (N=100 expected)
- Standardize slope values to T-scores: M=50, SD=10
- Handle missing slopes: document count, exclude from analysis
- Quality checks:
  - Slope range: typically [-2, 2] for IRT ability scale slopes
  - No extreme outliers: |z| < 4 for standardized slopes
  - Minimum N=90 participants for adequate power
- Save extracted data with metadata

**Output:**
- data/step01_pass1_slopes.csv (UID, slope_raw, slope_tscore, slope_se)

**Validation Requirement:**
Validation tools MUST be used after slope extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_pass1_slopes.csv: 90-100 rows x 4 columns
- Data types: UID (object), slope_raw (float64), slope_tscore (float64), slope_se (float64)

*Value Ranges:*
- slope_raw in [-3, 3] (IRT slope scale)
- slope_tscore: M=50, SD=10 (T-score standardization)
- slope_se > 0 (positive standard errors)
- All values finite (no inf, -inf, NaN)

*Data Quality:*
- N >= 90 participants (minimum for power)
- No duplicate UIDs
- Standardized slopes: mean approximately 50, SD approximately 10
- Missing data < 10% of expected N=100

*Log Validation:*
- Required: "Pass 1 slopes extracted: N=XX participants"
- Required: "T-score standardization: M=XX, SD=XX"
- Required: "Quality checks passed"
- Forbidden: "ERROR", "EXTRACTION FAILED"

**Expected Behavior on Validation Failure:**
Log detailed error, attempt data recovery if partial success, quit if <90 participants

### Step 2: Extract Post-Purification Slopes (IRT Pass 2)
**Dependencies:** Step 1 (pre-purification slopes)
**Complexity:** Medium (~8 minutes)

**Purpose:** Extract individual forgetting slopes from post-purification IRT analysis

**Input:**
- Primary: results/ch5/5.2.5/data/step06_pass2_slopes.csv
- Alternative: results/ch5/5.2.*/data/*pass2*slope*.csv
- Fallback: results/ch5/*/data/*irt*pass*2*.{csv,txt}
- Expected format: Same UIDs as Step 1, slope estimates

**Processing:**
- Load post-purification slope file using pandas.read_csv
- Verify contains same UIDs as pre-purification (Step 1 output)
- Extract individual participant slopes matching Step 1 UIDs
- Standardize slope values to T-scores: M=50, SD=10 (independent standardization)
- Handle missing slopes: document, require overlap with Step 1
- Quality checks:
  - Same range requirements as Step 1
  - Verify UID overlap >= 90 participants with Step 1
  - Check for systematic differences in slope SE between passes
- Save matched dataset

**Output:**
- data/step02_pass2_slopes.csv (UID, slope_raw, slope_tscore, slope_se)

**Validation Requirement:**
Validation tools MUST be used after slope extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_pass2_slopes.csv: 90-100 rows x 4 columns
- Data types: UID (object), slope_raw (float64), slope_tscore (float64), slope_se (float64)

*Value Ranges:*
- slope_raw in [-3, 3] (IRT slope scale)
- slope_tscore: M=50, SD=10 (T-score standardization)
- slope_se > 0 (positive standard errors)
- All values finite (no inf, -inf, NaN)

*Data Quality:*
- N >= 90 participants overlapping with Step 1
- UIDs match Step 1 (same participants)
- Independent standardization: mean approximately 50, SD approximately 10
- Missing data < 10% of Step 1 participants

*Log Validation:*
- Required: "Pass 2 slopes extracted: N=XX participants"
- Required: "UID overlap with Pass 1: N=XX participants"
- Required: "T-score standardization: M=XX, SD=XX"
- Forbidden: "ERROR", "UID MISMATCH", "EXTRACTION FAILED"

**Expected Behavior on Validation Failure:**
Log UID mismatches, attempt intersection recovery, quit if <90 overlapping participants

### Step 3: Extract Cognitive Test Predictors
**Dependencies:** Steps 1-2 (slope data)
**Complexity:** Medium (~8 minutes)

**Purpose:** Extract and standardize cognitive test scores for regression predictors

**Input:**
- data/cache/master.xlsx (RAVLT, BVMT, RPM scores + demographics)
- data/step01_pass1_slopes.csv and data/step02_pass2_slopes.csv (UID lists)

**Processing:**
- Load master.xlsx using pandas.read_excel
- Extract cognitive test scores: RAVLT_Total, BVMT_Total, RPM_Total
- Extract demographics: Age, Sex, Education for covariates
- Filter to participants with slope data from Steps 1-2
- Standardize cognitive tests to T-scores: M=50, SD=10 for each test
- Handle missing cognitive data:
  - Missing RAVLT: exclude participant (primary predictor)
  - Missing BVMT or RPM: use available predictors, note in analysis
  - Missing demographics: use mean imputation for Age/Education, indicator for missing Sex
- Quality checks:
  - Cognitive scores in plausible ranges (T-scores: 20-80 typical)
  - No impossible values (negative raw scores)
  - Verify final N >= 85 participants for analysis

**Output:**
- data/step03_cognitive_predictors.csv (UID, RAVLT_T, BVMT_T, RPM_T, Age, Sex, Education)

**Validation Requirement:**
Validation tools MUST be used after cognitive data extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_cognitive_predictors.csv: 85-100 rows x 7 columns
- Data types: UID (object), cognitive T-scores (float64), Age (int64), Sex (object), Education (int64)

*Value Ranges:*
- RAVLT_T, BVMT_T, RPM_T in [20, 80] (plausible T-score range)
- Age in [18, 85] (adult participants)
- Sex in ["M", "F"] or similar coding
- Education in [8, 25] (years of education)

*Data Quality:*
- N >= 85 participants (minimum for 3 predictors + covariates)
- T-score means approximately 50, SDs approximately 10
- Missing RAVLT < 5% (primary predictor)
- Missing BVMT/RPM < 15% each (acceptable for secondary predictors)

*Log Validation:*
- Required: "Cognitive tests extracted: N=XX participants"
- Required: "T-score standardization completed"
- Required: "Missing data handled: RAVLT N=XX, BVMT N=XX, RPM N=XX"
- Forbidden: "ERROR", "STANDARDIZATION FAILED"

**Expected Behavior on Validation Failure:**
Report missing data patterns, attempt analysis with available predictors if N>=85, quit if insufficient power

### Step 4: Merge and Prepare Analysis Dataset
**Dependencies:** Steps 1-3 (slopes and predictors)
**Complexity:** Low (~5 minutes)

**Purpose:** Create final merged dataset for regression analysis

**Input:**
- data/step01_pass1_slopes.csv (pre-purification slopes)
- data/step02_pass2_slopes.csv (post-purification slopes)
- data/step03_cognitive_predictors.csv (predictors and covariates)

**Processing:**
- Inner join all datasets on UID (only participants with complete slope data)
- Create analysis variables:
  - Slope_Pass1_T: Pre-purification T-scored slopes
  - Slope_Pass2_T: Post-purification T-scored slopes
  - RAVLT_T, BVMT_T, RPM_T: Cognitive predictors
  - Age, Sex_coded, Education: Demographics (dummy code Sex)
- Calculate descriptive statistics for all variables
- Check correlations between predictors for multicollinearity screening
- Verify final sample size adequate for planned analyses
- Export analysis-ready dataset

**Output:**
- data/step04_analysis_dataset.csv (merged, analysis-ready data)
- data/step04_descriptives.csv (means, SDs, correlations)

**Validation Requirement:**
Validation tools MUST be used after data merging execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_analysis_dataset.csv: 85-100 rows x 9 columns minimum
- data/step04_descriptives.csv: 9 rows x 4 columns (variable, mean, sd, n)
- Data types: All numeric except UID (object)

*Value Ranges:*
- Slope variables: T-scores with M~50, SD~10
- Cognitive variables: T-scores with M~50, SD~10
- Age: [18, 85], Sex_coded: [0, 1], Education: [8, 25]
- Correlations: [-1, 1] with reasonable magnitude (<0.90 between predictors)

*Data Quality:*
- No missing values in final dataset (complete cases only)
- N >= 85 participants for adequate power
- Correlations between cognitive predictors < 0.80 (multicollinearity check)
- Equal Ns for both slope outcomes (same participants)

*Log Validation:*
- Required: "Analysis dataset created: N=XX participants"
- Required: "Correlation check passed"
- Required: "Descriptives computed"
- Forbidden: "MERGE FAILED", "MISSING VALUES", "HIGH CORRELATION WARNING"

**Expected Behavior on Validation Failure:**
Report merge issues, check UID consistency, quit if final N < 85 participants

### Step 5: Pre-Purification Regression Model (Pass 1)
**Dependencies:** Step 4 (analysis dataset)
**Complexity:** Medium (~10 minutes including diagnostics)

**Purpose:** Fit multiple regression predicting pre-purification slopes with cognitive tests

**Input:**
- data/step04_analysis_dataset.csv (merged analysis data)

**Processing:**
- Fit regression model: Slope_Pass1_T ~ RAVLT_T + BVMT_T + RPM_T + Age + Sex_coded + Education
- Implementation: statsmodels.api.OLS with standardized predictors
- Extract model results:
  - Overall R², Adjusted R², F-statistic, p-value
  - Individual coefficients (beta), standard errors, t-values, p-values
  - Semi-partial correlations (sr²) for unique variance
- Bootstrap 95% CIs for coefficients:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - CI computation: percentile method (2.5th, 97.5th percentiles)
- Check assumptions:
  - Multicollinearity: VIF for each predictor
  - Normality: Shapiro-Wilk test on residuals
  - Homoscedasticity: Breusch-Pagan test
  - Linearity: Partial residual plots (visual inspection)
  - Outliers: Cook's distance > 4/N threshold
- Remedial actions if assumptions violated:
  - VIF > 5: Document multicollinearity, consider ridge if VIF > 10
  - Normality p < 0.05: Report bootstrap CIs as primary inference
  - Heteroscedasticity p < 0.05: Add HC3 robust standard errors
  - Cook's D > 4/N: Report results with and without outliers
- Multiple comparison correction:
  - Family: Within-model (3 cognitive predictors)
  - Bonferroni: alpha = 0.05/3 = 0.0167 per test
  - Also compute FDR-adjusted p-values
  - Report BOTH uncorrected AND corrected p-values (Decision D068)

**Output:**
- data/step05_pass1_regression.csv (model results with CIs)
- data/step05_pass1_diagnostics.csv (assumption test results)

**Validation Requirement:**
Validation tools MUST be used after regression model execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_pass1_regression.csv: 6 rows x 10 columns (predictors x metrics)
- data/step05_pass1_diagnostics.csv: 5 rows x 4 columns (tests x results)
- Columns in regression: predictor, beta, se, ci_lower, ci_upper, p_uncorrected, p_bonferroni, p_fdr, vif, sr_squared

*Value Ranges:*
- beta in [-2, 2] (standardized predictors)
- se > 0 (positive standard errors)
- p-values in [0, 1]
- VIF in [1, 10] (multicollinearity acceptable)
- R² in [0, 1], typically [0.10, 0.60] for individual differences

*Data Quality:*
- All 6 predictors present (3 cognitive + 3 demographic)
- Bootstrap CIs valid (ci_lower < beta < ci_upper for most)
- Dual p-values present (Decision D068 compliance)
- VIF < 5 for acceptable multicollinearity

*Log Validation:*
- Required: "Pass 1 regression fitted: R² = X.XX"
- Required: "Bootstrap complete: 1000 iterations, seed=42"
- Required: "Assumption checks completed"
- Required: "Multiple comparison correction applied"
- Forbidden: "ERROR", "CONVERGENCE FAILED", "BOOTSTRAP FAILED"

**Expected Behavior on Validation Failure:**
Log specific regression failure, check data quality, attempt simplified model, invoke g_debug if persistent failure

### Step 6: Post-Purification Regression Model (Pass 2)
**Dependencies:** Step 5 (Pass 1 model for comparison)
**Complexity:** Medium (~10 minutes including diagnostics)

**Purpose:** Fit identical multiple regression predicting post-purification slopes

**Input:**
- data/step04_analysis_dataset.csv (merged analysis data)

**Processing:**
- Fit identical model: Slope_Pass2_T ~ RAVLT_T + BVMT_T + RPM_T + Age + Sex_coded + Education
- Implementation: statsmodels.api.OLS with same predictors as Step 5
- Extract identical model results as Step 5:
  - Overall R², Adjusted R², F-statistic, p-value
  - Individual coefficients (beta), SEs, t-values, p-values
  - Semi-partial correlations (sr²) for unique variance
- Bootstrap 95% CIs for coefficients:
  - Iterations: 1000
  - Random seed: 42 (same as Step 5)
  - Method: Identical to Step 5 (participant-level resampling)
  - CI computation: percentile method
- Check identical assumptions as Step 5:
  - Same VIF, normality, homoscedasticity, linearity, outlier checks
  - Apply identical remedial actions if violations detected
- Multiple comparison correction:
  - Identical family definition and correction as Step 5
  - Bonferroni: alpha = 0.05/3 = 0.0167 per test
  - FDR-adjusted p-values
  - Report BOTH uncorrected AND corrected p-values (Decision D068)

**Output:**
- data/step06_pass2_regression.csv (model results with CIs)
- data/step06_pass2_diagnostics.csv (assumption test results)

**Validation Requirement:**
Validation tools MUST be used after regression model execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_pass2_regression.csv: 6 rows x 10 columns (identical structure to Step 5)
- data/step06_pass2_diagnostics.csv: 5 rows x 4 columns (tests x results)
- Identical column structure to Step 5 outputs

*Value Ranges:*
- Identical value range requirements as Step 5
- beta in [-2, 2], se > 0, p-values in [0, 1]
- VIF in [1, 10], R² in [0, 1]

*Data Quality:*
- Identical quality requirements as Step 5
- All 6 predictors present with valid statistics
- Bootstrap CIs and dual p-values present
- VIF acceptable for all predictors

*Log Validation:*
- Required: "Pass 2 regression fitted: R² = X.XX"
- Required: "Bootstrap complete: 1000 iterations, seed=42"
- Required: "Assumption checks completed"
- Required: "Multiple comparison correction applied"
- Forbidden: "ERROR", "CONVERGENCE FAILED", "BOOTSTRAP FAILED"

**Expected Behavior on Validation Failure:**
Identical failure handling as Step 5, compare failure patterns between passes for systematic issues

### Step 7: Compare Regression Models (Purification Effect Analysis)
**Dependencies:** Steps 5-6 (both regression models)
**Complexity:** High (~15 minutes including power analysis)

**Purpose:** Compare pre- vs post-purification models to test purification paradox hypothesis

**Input:**
- data/step05_pass1_regression.csv (pre-purification model results)
- data/step06_pass2_regression.csv (post-purification model results)
- data/step04_analysis_dataset.csv (for dependent correlation tests)

**Processing:**
- Model comparison tests:
  - R² difference test: F-test for nested models (if same predictors)
  - Alternative: Bootstrap confidence interval for R² difference
  - Effect size: Cohen's f² for each model and difference
- Individual coefficient comparisons:
  - Compute coefficient differences: beta_Pass1 - beta_Pass2 for each predictor
  - Test significance using bootstrap confidence intervals
  - Calculate z-tests for dependent correlations (Williams-Steiger test)
  - Effect sizes: Standardized mean difference for coefficient changes
- Bootstrap analysis for model comparison:
  - Iterations: 1000
  - Random seed: 42
  - Method: Participant-level block bootstrap
  - For each iteration: fit both models, compute R² difference and coefficient differences
  - CI computation: percentile method for differences
- Multiple comparison correction for model comparison:
  - Family: Between-pass comparisons (1 R² test + 3 cognitive coefficient tests = 4 tests)
  - Bonferroni: alpha = 0.05/4 = 0.0125 per test
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Cross-validation for model stability:
  - Implement 5-fold cross-validation using sklearn.model_selection.KFold
  - Random seed: 42 for reproducibility
  - Shuffle: True (randomize before splitting)
  - For each fold: fit both models on training (80%), evaluate on test (20%)
  - Compute mean and SD of R² across folds for both passes
  - Flag if train-test R² gap > 0.10 (overfitting detected)
- Power analysis:
  - Post-hoc power for observed coefficient differences
  - Use: statsmodels.stats.power for regression coefficient tests
  - Given: N=actual, predictors=6, alpha=0.0125 (corrected)
  - Calculate: achieved power for observed effect sizes
  - Report: minimum detectable effect at 80% power

**Output:**
- data/step07_model_comparison.csv (R² and coefficient differences with CIs)
- data/step07_cross_validation.csv (CV results for both models)
- data/step07_power_analysis.csv (power calculations)

**Validation Requirement:**
Validation tools MUST be used after model comparison execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_model_comparison.csv: 4 rows x 8 columns (R² + 3 cognitive predictors)
- data/step07_cross_validation.csv: 2 rows x 6 columns (Pass1/Pass2 x CV metrics)
- data/step07_power_analysis.csv: 4 rows x 5 columns (tests x power metrics)
- Columns: comparison_type, difference, ci_lower, ci_upper, p_uncorrected, p_bonferroni, effect_size, interpretation

*Value Ranges:*
- R² differences in [-1, 1] (practically [-0.5, 0.5])
- Coefficient differences in [-4, 4] (standardized)
- p-values in [0, 1]
- Effect sizes (Cohen's f²) in [0, 2] (practically [0, 0.5])
- CV R² values in [0, 1]
- Power values in [0, 1]

*Data Quality:*
- All comparisons have valid CIs (ci_lower < ci_upper)
- Dual p-values present (Decision D068 compliance)
- CV results show both passes with reasonable performance
- Power analysis results interpretable

*Log Validation:*
- Required: "Model comparison completed: ΔR² = X.XXX"
- Required: "Bootstrap comparison: 1000 iterations, seed=42"
- Required: "Cross-validation completed: 5-fold, seed=42"
- Required: "Power analysis completed"
- Required: "Multiple comparison correction applied"
- Forbidden: "ERROR", "COMPARISON FAILED", "CV FAILED"

**Expected Behavior on Validation Failure:**
Log specific comparison failure, check input model validity, attempt simplified comparison, report partial results if possible

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (prerequisite check results)
- data/step01_pass1_slopes.csv (pre-purification individual slopes)
- data/step02_pass2_slopes.csv (post-purification individual slopes) 
- data/step03_cognitive_predictors.csv (standardized cognitive test scores)
- data/step04_analysis_dataset.csv (merged, analysis-ready data)
- data/step04_descriptives.csv (descriptive statistics)
- data/step05_pass1_regression.csv (pre-purification regression results)
- data/step05_pass1_diagnostics.csv (Pass 1 assumption checks)
- data/step06_pass2_regression.csv (post-purification regression results)
- data/step06_pass2_diagnostics.csv (Pass 2 assumption checks)
- data/step07_model_comparison.csv (comparative analysis results)
- data/step07_cross_validation.csv (model stability assessment)
- data/step07_power_analysis.csv (power analysis results)

### Logs (ONLY execution logs)
- logs/step01_extract_pass1_slopes.log
- logs/step02_extract_pass2_slopes.log
- logs/step03_extract_cognitive_predictors.log
- logs/step04_merge_datasets.log
- logs/step05_pass1_regression.log
- logs/step06_pass2_regression.log
- logs/step07_model_comparison.log

### Plots (EMPTY until rq_plots runs)
Plot source CSVs for rq_plots agent:
- data/step07_coefficient_comparison_plot_data.csv (before/after coefficients)
- data/step07_diagnostic_plots_data.csv (residuals, Q-Q plot data)

### Results (EMPTY until rq_results runs)
Summary markdown file created by rq_results:
- results/purification_comparison_summary.md (thesis interpretation)

---

## Expected Data Formats

### Step-to-Step Transformations
1. **Step 0->1:** Ch5 slope files -> individual pre-purification slopes
2. **Step 1->2:** Pre-purification slopes -> matched post-purification slopes
3. **Step 2->3:** Slope UIDs -> cognitive test scores for same participants
4. **Step 3->4:** Separate datasets -> merged analysis-ready dataset
5. **Step 4->5:** Analysis data -> fitted pre-purification regression model
6. **Step 5->6:** Model 1 -> fitted post-purification regression model
7. **Step 6->7:** Both models -> comparative analysis with differences

### Column Naming Conventions
- **UIDs:** Consistent "UID" column across all files
- **Slopes:** slope_raw, slope_tscore, slope_se
- **Cognitive:** RAVLT_T, BVMT_T, RPM_T (T-score standardized)
- **Demographics:** Age, Sex_coded, Education
- **Regression:** beta, se, ci_lower, ci_upper, p_uncorrected, p_bonferroni, p_fdr
- **Comparison:** difference, effect_size, interpretation

### Data Type Constraints
- **UIDs:** object (string identifiers)
- **Slopes:** float64 (allow decimals, nullable for missing)
- **Cognitive scores:** float64 (T-scores, non-nullable in analysis dataset)
- **Demographics:** Age/Education = int64, Sex_coded = int64 (0/1)
- **Statistics:** All float64, non-nullable after computation

---

## Cross-RQ Dependencies

### Required Ch5 Outputs
- **Dependency:** Ch5 5.2.5 (or equivalent slope analysis with dual IRT passes)
- **Required files:**
  - Pre-purification slopes (Pass 1): *pass1*slope*.csv
  - Post-purification slopes (Pass 2): *pass2*slope*.csv
- **Format requirements:** UID column + slope estimates (± standard errors)
- **Minimum overlap:** 85 participants with slopes from both passes

### Master Data Requirements
- **Source:** data/cache/master.xlsx
- **Required columns:** UID, RAVLT_Total, BVMT_Total, RPM_Total, Age, Sex, Education
- **Quality requirements:** <5% missing on RAVLT (primary predictor)

**Circuit Breaker:** If Ch5 dependencies not met, QUIT with specific error and recommend completing Ch5 slope analysis first.

---

## Summary

**Total Steps:** 8 (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** 45-60 minutes
**Cross-RQ Dependencies:** Ch5 5.2.5 or equivalent (dual-pass slope analysis)
**Primary Outputs:** Regression comparison testing purification paradox hypothesis
**Validation Coverage:** 100% (all 8 steps have 4-layer validation requirements)

**Key Hypothesis:** Predictor relationships will weaken after purification (Pre-purification R² > Post-purification R²), consistent with the Ch5 purification-trajectory paradox.

**Critical Methodological Notes:**
- All randomized procedures use seed=42 for reproducibility
- Bootstrap confidence intervals provide robustness against non-normality
- Multiple comparison corrections control family-wise error rate
- Cross-validation assesses model stability and overfitting
- Dependent samples design (same participants) acknowledged and addressed through bootstrap resampling
- Power analysis provides context for coefficient difference interpretation

**Success Criteria:**
- Reliable detection of R² differences between purification passes
- Interpretable coefficient changes with bootstrap confidence intervals
- Valid assumption checks for both regression models
- Adequate power (>0.80) for medium effect size detection

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml  
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent with v5.1 specifications