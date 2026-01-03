# Analysis Plan: RQ 7.1.4 - Unique REMEMVR variance unexplained by all predictors?

**Research Question:** 7.1.4
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines REMEMVR's incremental validity through hierarchical multiple regression to quantify what proportion of variance remains unexplained after accounting for ALL available predictors (demographics, cognitive tests, self-report measures). The analysis tests whether REMEMVR captures meaningful memory variance beyond traditional measures, supporting an "ecological validity gap" hypothesis.

**Pipeline:** Hierarchical Multiple Regression with Cross-Validation and Bootstrap
**Steps:** 9 total analysis steps (Step 0: dependency validation + Steps 1-8: analysis)
**Estimated Runtime:** 45-60 minutes

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Chapter-level alpha correction: 0.05/28 = 0.00179
- Conservative cross-validation with overfitting detection
- Comprehensive assumption checking with remedial actions

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 theta scores and master.xlsx accessibility before proceeding

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv (overall theta estimates)
- Alternative: results/ch5/5.1.1/data/*theta*.csv
- Fallback: results/ch5/5.1.1/data/*lmm*.{txt,rds,csv}
- Expected content: Mean theta scores per UID across T1-T4 sessions
- RAW source: data/cache/master.xlsx (cognitive tests, demographics, self-report)
- If Ch5 missing: QUIT with "Ch5 5.1.1 theta scores not found"
- If master.xlsx missing: QUIT with "master.xlsx not accessible"

**Processing:**
- Check Ch5 5.1.1 completed successfully (status.yaml: rq_results = success)
- Locate theta scores file using multiple search patterns
- Verify file contains UID column and theta estimates for 100 participants
- Test master.xlsx accessibility and required tag patterns
- Log all validation checks with success/failure status

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Content: Ch5 status check, theta file verification, master.xlsx access confirmation

*Value Ranges:*
- Validation status: "PASS" or "FAIL" for each dependency
- UID count in theta file: 100 participants expected
- File sizes: theta file > 1KB, master.xlsx > 10MB

*Data Quality:*
- All required file paths accessible
- No missing critical dependencies
- Validation log complete for all checks

*Log Validation:*
- Required: "Ch5 5.1.1 status: success"
- Required: "Theta file found with 100 UIDs"
- Required: "master.xlsx accessible"
- Required: "VALIDATION - PASS"
- Forbidden: "ERROR", "FAIL", "not found"

**Expected Behavior on Validation Failure:**
Quit immediately with specific error message indicating which dependency failed. Log failure to logs/step00_dependency_validation.log.

### Step 1: Extract and T-Score Cognitive Tests
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Medium (~8 minutes)

**Purpose:** Extract cognitive test raw scores from master.xlsx and convert to standardized T-scores for regression analysis

**Input:**
- data/cache/master.xlsx (verified accessible from Step 0)
- Tag patterns: 
  - RAVLT: {UID}-COG-X-RAV-T1Sc to T5Sc, {UID}-COG-X-RAV-DRSc
  - BVMT: {UID}-COG-X-BVM-TotR
  - NART: {UID}-COG-X-NAR-Scor
  - RPM: {UID}-COG-X-RPM-Scor

**Processing:**
- Extract cognitive test scores for all 100 participants
- Compute RAVLT_Total = sum(T1Sc + T2Sc + T3Sc + T4Sc + T5Sc)
- Use RAVLT_DRSc as delayed recall score
- Convert all cognitive scores to T-scores: T = 50 + 10 * (X - M) / SD
- T-score parameters: Mean = 50, SD = 10 (standardized across full sample)
- Generate correlation matrix of all cognitive predictors
- Check for missing data patterns and document exclusions
- Remedial actions:
  - Missing data >5%: Document exclusions, proceed with complete cases
  - Extreme outliers (>3 SD): Document but retain (clinical validity)
  - Non-normal distributions: Log successful T-score transformation

**Output:**
- data/step01_cognitive_tests.csv (UID, RAVLT_T, RAVLT_DR_T, BVMT_T, NART_T, RPM_T)
- data/step01_cognitive_correlation_matrix.csv (predictor intercorrelations)

**Validation Requirement:**
Validation tools MUST be used after cognitive test extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_cognitive_tests.csv: 100 rows x 6 columns
- Columns: UID (object), RAVLT_T (float64), RAVLT_DR_T (float64), BVMT_T (float64), NART_T (float64), RPM_T (float64)
- data/step01_cognitive_correlation_matrix.csv: 5 rows x 5 columns (cognitive test intercorrelations)

*Value Ranges:*
- All T-scores in [20, 80] range (within 3 SD of normative mean 50)
- T-score means approximately 50 (+/- 2) across sample
- T-score SDs approximately 10 (+/- 1) across sample
- Correlation coefficients in [-1, 1] range

*Data Quality:*
- All 100 UIDs present (no missing participants)
- No NaN values in T-scores (complete case analysis)
- Correlation matrix symmetric with 1.0 on diagonal
- Maximum pairwise correlation <0.90 (extreme multicollinearity check)

*Log Validation:*
- Required: "Cognitive tests extracted: 100 participants"
- Required: "T-score transformation complete"
- Required: "Correlation matrix computed"
- Required: "VALIDATION - PASS"
- Forbidden: "ERROR", "missing data >5%", "correlation >0.90"

**Expected Behavior on Validation Failure:**
Raise error with specific validation failure details. Log to logs/step01_extract_cognitive.log and invoke g_debug for troubleshooting.

### Step 2: Extract Demographics and Self-Report Variables
**Dependencies:** Step 1 (cognitive tests extracted)
**Complexity:** Medium (~6 minutes)

**Purpose:** Extract demographic and self-report predictors to complete hierarchical regression dataset

**Input:**
- data/cache/master.xlsx (same source as Step 1)
- Demographics: {UID}-DEM-X-Age, {UID}-DEM-X-Sex, {UID}-DEM-X-Education
- Self-report: {UID}-DEM-X-DASS_Dep, {UID}-DEM-X-DASS_Anx, {UID}-DEM-X-DASS_Str, {UID}-DEM-X-VR_Exp, {UID}-DEM-X-SLEEP

**Processing:**
- Extract demographic variables for all participants
- Code Sex as binary: Male=0, Female=1
- Extract DASS subscale scores (Depression, Anxiety, Stress)
- Extract VR experience rating and sleep quality rating
- Check for missing data in self-report measures (expect ~97 complete cases)
- Compute descriptive statistics for all predictors
- Remedial actions:
  - Missing demographics: Exclude participant from analysis
  - Missing DASS scores: Use available cases, document N
  - Outliers in continuous variables: Document but retain

**Output:**
- data/step02_demographics.csv (UID, Age, Sex, Education)
- data/step03_self_report.csv (UID, DASS_Dep, DASS_Anx, DASS_Str, VR_Exp, Sleep)

**Validation Requirement:**
Validation tools MUST be used after demographics and self-report extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_demographics.csv: ~100 rows x 4 columns
- Columns: UID (object), Age (int64), Sex (int64), Education (int64)
- data/step03_self_report.csv: ~97 rows x 6 columns
- Columns: UID (object), DASS_Dep (float64), DASS_Anx (float64), DASS_Str (float64), VR_Exp (float64), Sleep (float64)

*Value Ranges:*
- Age in [18, 85] range (adult participants)
- Sex coded as 0 (Male) or 1 (Female)
- Education in [8, 20] range (years of education)
- DASS scores in [0, 42] range per subscale
- VR_Exp and Sleep in [1, 7] Likert scale range

*Data Quality:*
- Demographics: >95 participants with complete data
- Self-report: >90 participants with complete data (tolerance for DASS missingness)
- No impossible values (negative ages, out-of-range ratings)
- Sex distribution approximately balanced (40-60% either gender)

*Log Validation:*
- Required: "Demographics extracted: N participants"
- Required: "Self-report extracted: N participants"
- Required: "Sex distribution: X% male, Y% female"
- Required: "VALIDATION - PASS"
- Forbidden: "ERROR", "impossible values", "extreme missingness"

**Expected Behavior on Validation Failure:**
Document specific data quality issues. Continue with available cases if >90 participants have complete data. Log warnings for high missingness.

### Step 3: Merge Predictors with REMEMVR Theta Scores
**Dependencies:** Steps 1-2 (predictors extracted), Step 0 (theta file located)
**Complexity:** Medium (~7 minutes)

**Purpose:** Create complete hierarchical regression dataset by merging all predictors with REMEMVR theta scores

**Input:**
- data/step01_cognitive_tests.csv (T-scored cognitive tests)
- data/step02_demographics.csv (demographic variables)
- data/step03_self_report.csv (DASS and other self-report measures)
- results/ch5/5.1.1/data/step03_theta_scores.csv (mean theta per UID)

**Processing:**
- Load REMEMVR theta scores (mean across T1, T2, T3, T4 sessions)
- Merge all predictor sets on UID (inner join to retain complete cases only)
- Create hierarchical regression blocks:
  - Block 1 (Demographics): Age, Sex, Education
  - Block 2 (Cognitive): RAVLT_T, RAVLT_DR_T, BVMT_T, NART_T, RPM_T
  - Block 3 (Self-report): DASS_Dep, DASS_Anx, DASS_Str, VR_Exp, Sleep
- Standardize all continuous predictors (z-scores: M=0, SD=1)
- Compute final sample size and check for complete cases
- Generate comprehensive descriptive statistics
- Remedial actions:
  - Final N <90: Document limitation but proceed
  - Extreme theta outliers: Check for data quality issues
  - Missing predictors: Use only complete cases

**Output:**
- data/step04_merged_predictors.csv (complete dataset for hierarchical regression)
- data/step04_descriptive_stats.csv (means, SDs, ranges for all variables)

**Validation Requirement:**
Validation tools MUST be used after data merging completion.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_merged_predictors.csv: ~95 rows x 14 columns
- Columns: UID, theta (DV), Age_z, Sex, Education_z, RAVLT_T_z, RAVLT_DR_T_z, BVMT_T_z, NART_T_z, RPM_T_z, DASS_Dep_z, DASS_Anx_z, DASS_Str_z, VR_Exp_z, Sleep_z
- data/step04_descriptive_stats.csv: 14 rows x 6 columns (variable, mean, sd, min, max, n)

*Value Ranges:*
- theta in [-3, 3] range (IRT ability scale)
- Standardized predictors approximately M=0, SD=1 (+/- 0.1 tolerance)
- Sex remains binary (0, 1)
- Final sample size >=90 participants

*Data Quality:*
- No missing values (complete cases only)
- All 14 variables present for each participant
- Standardization successful (z-score means near 0)
- Reasonable theta score distribution (not all extreme values)

*Log Validation:*
- Required: "Data merge complete: N=X participants"
- Required: "Hierarchical blocks created: 3, 5, 5 predictors"
- Required: "Standardization complete"
- Required: "VALIDATION - PASS"
- Forbidden: "ERROR", "missing values", "merge failure"

**Expected Behavior on Validation Failure:**
Identify specific merge or standardization issues. Log detailed error information and quit if fundamental data problems detected.

### Step 4: Fit Hierarchical Regression with Cross-Validation
**Dependencies:** Step 3 (complete merged dataset)
**Complexity:** High (~12 minutes including CV)

**Purpose:** Fit 3-block hierarchical regression with 5-fold cross-validation to assess model stability and prevent overfitting

**Input:**
- data/step04_merged_predictors.csv (complete regression dataset)

**Processing:**
- Implement 5-fold cross-validation using sklearn.model_selection.KFold
- Random seed: 42 for reproducibility
- Shuffle: True (randomize before splitting)
- For each fold: fit models on training (80%), evaluate on test (20%)
- Fit three nested models:
  - Model 1: theta ~ Age_z + Sex + Education_z
  - Model 2: theta ~ Model1 + RAVLT_T_z + RAVLT_DR_T_z + BVMT_T_z + NART_T_z + RPM_T_z
  - Model 3: theta ~ Model2 + DASS_Dep_z + DASS_Anx_z + DASS_Str_z + VR_Exp_z + Sleep_z
- For each model, compute R², adjusted R², MSE on both training and test sets
- Compute mean and std of R² across folds for each model
- Flag overfitting if train-test R² gap > 0.10 for any model
- Multiple comparison correction:
  - Family: Within-RQ model comparisons (3 models)
  - Bonferroni: alpha = 0.00179/3 = 0.00060 per model
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Check assumptions for final full-sample models:
  - Normality: Shapiro-Wilk test on residuals
  - Homoscedasticity: Breusch-Pagan test
  - Multicollinearity: VIF for each predictor
- Remedial actions if violated:
  - Normality p < 0.05: Report bootstrap CIs as primary inference method
  - Heteroscedasticity p < 0.05: Add HC3 robust SEs to output
  - VIF > 5: Document multicollinearity, consider ridge if VIF > 10

**Output:**
- data/step05_hierarchical_models.csv (R², adj R², F-statistics, p-values for all models)
- data/step05_cross_validation_results.csv (CV R² by fold and model)
- data/step05_assumption_diagnostics.txt (normality, homoscedasticity, VIF results)

**Validation Requirement:**
Validation tools MUST be used after hierarchical regression fitting.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_hierarchical_models.csv: 3 rows x 10 columns
- Columns: model, predictors, R2, adj_R2, F_stat, p_uncorrected, p_bonferroni, train_R2_mean, test_R2_mean, cv_gap
- data/step05_cross_validation_results.csv: 15 rows x 4 columns (3 models x 5 folds)
- Columns: model, fold, train_R2, test_R2
- data/step05_assumption_diagnostics.txt: text file with test results and p-values

*Value Ranges:*
- R² values in [0, 1] range
- F-statistics > 0 (positive test statistics)
- p-values in [0, 1] range
- CV gaps < 0.10 (overfitting threshold)
- VIF values typically in [1, 10] range

*Data Quality:*
- All 3 models successfully fitted
- Cross-validation completed for all models (15 total fits)
- Assumption tests completed with valid p-values
- Model 3 R² > Model 2 R² > Model 1 R² (hierarchical improvement)

*Log Validation:*
- Required: "Hierarchical regression complete: 3 models"
- Required: "Cross-validation complete: 5 folds per model"
- Required: "Model 1 R² = X.XX, Model 2 R² = X.XX, Model 3 R² = X.XX"
- Required: "CV gap check: all models < 0.10"
- Required: "Assumption checks complete"
- Required: "VALIDATION - PASS"
- Forbidden: "ERROR", "convergence failed", "CV gap > 0.10"

**Expected Behavior on Validation Failure:**
Document specific model fitting or assumption violation issues. If convergence fails, try standardizing predictors again or check for multicollinearity.

### Step 5: Calculate Incremental R² and Cohen's f² Effect Sizes
**Dependencies:** Step 4 (hierarchical models fitted)
**Complexity:** Medium (~8 minutes including bootstrap)

**Purpose:** Quantify incremental validity of each predictor block using R² increments and Cohen's f² effect sizes with bootstrap confidence intervals

**Input:**
- data/step05_hierarchical_models.csv (R² values for nested models)
- data/step04_merged_predictors.csv (original dataset for bootstrap)

**Processing:**
- Calculate incremental R² for each block:
  - Delta_R²_block1 = R²_model1 - 0 (demographics baseline)
  - Delta_R²_block2 = R²_model2 - R²_model1 (cognitive increment)
  - Delta_R²_block3 = R²_model3 - R²_model2 (self-report increment)
- F-test for significance of each increment
- Calculate Cohen's f² effect sizes for each block:
  - f²_block1 = R²_model1 / (1 - R²_model1)
  - f²_block2 = Delta_R²_block2 / (1 - R²_model2)
  - f²_block3 = Delta_R²_block3 / (1 - R²_model3)
- Bootstrap 95% CIs for all R² and f² estimates:
  - Iterations: 1000
  - Seed: 42
  - Method: Participant-level resampling with replacement
  - CI: Percentile method (2.5th, 97.5th)
- Post-hoc power analysis for hierarchical regression:
  - Given: Final N, 12 predictors, alpha=0.00179
  - Calculate: minimum detectable f² at 80% power
  - Use: statsmodels.stats.power.FTestAnovaPower()
  - Report: actual power for observed effect sizes
  - If power < 0.80: acknowledge limitation in interpretation
- Effect size interpretation using Cohen's guidelines:
  - f² < 0.02: Negligible effect
  - f² 0.02-0.14: Small effect
  - f² 0.15-0.34: Medium effect
  - f² ≥ 0.35: Large effect

**Output:**
- data/step06_incremental_validity.csv (Delta_R², f², CIs, power analysis)
- data/step06_effect_size_interpretation.csv (effect size categories and interpretation)

**Validation Requirement:**
Validation tools MUST be used after effect size calculation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_incremental_validity.csv: 3 rows x 12 columns
- Columns: block, delta_R2, delta_R2_ci_lower, delta_R2_ci_upper, f2, f2_ci_lower, f2_ci_upper, F_stat, p_uncorrected, p_bonferroni, power, min_detectable_f2
- data/step06_effect_size_interpretation.csv: 3 rows x 4 columns
- Columns: block, f2_observed, effect_size_category, interpretation

*Value Ranges:*
- Delta_R² in [0, 1] range (R² increments positive)
- f² values typically in [0, 2] range (effect sizes)
- CI bounds: ci_lower < observed < ci_upper
- Power values in [0, 1] range
- F-statistics > 0

*Data Quality:*
- Bootstrap CIs computed successfully (1000 iterations)
- All three blocks have valid effect size estimates
- Confidence intervals non-degenerate (ci_lower < ci_upper)
- Effect size interpretations assigned correctly

*Log Validation:*
- Required: "Incremental R² calculated for 3 blocks"
- Required: "Cohen's f² calculated for 3 blocks"
- Required: "Bootstrap complete: 1000 iterations"
- Required: "Power analysis complete"
- Required: "Block 2 (cognitive) f² = X.XX (category)"
- Required: "VALIDATION - PASS"
- Forbidden: "ERROR", "bootstrap failed", "degenerate CI"

**Expected Behavior on Validation Failure:**
Identify specific calculation or bootstrap issues. Regenerate bootstrap samples if convergence problems detected.

### Step 6: Quantify Unexplained Variance with Measurement Error Correction
**Dependencies:** Step 5 (effect sizes calculated)
**Complexity:** Medium (~7 minutes)

**Purpose:** Calculate residual variance after full model, separating measurement error from true incremental validity gap

**Input:**
- data/step05_hierarchical_models.csv (Model 3 R² value)
- results/ch5/5.1.1/data/*theta*se*.csv (theta standard errors if available)
- data/step04_merged_predictors.csv (for bootstrap residual variance)

**Processing:**
- Calculate residual variance from cross-validated Model 3:
  - Residual = 1 - R²_model3_cv_test (use test set R² to avoid overfitting)
- Compute 95% CI for residual using bootstrap:
  - Iterations: 1000
  - Seed: 42
  - Method: Participant-level resampling with replacement
  - For each iteration: fit Model 3, calculate 1 - R²
  - CI: Percentile method (2.5th, 97.5th)
- Separate measurement error from true residual (if theta SEs available):
  - Estimate reliability: r_theta = 1 - (mean(SE²) / var(theta))
  - True residual = Residual / r_theta (disattenuated for measurement error)
  - Report both observed and corrected residual variance
- Hypothesis test for residual variance:
  - H0: Residual ≤ 0.50 vs H1: Residual > 0.50
  - Use bootstrap distribution to calculate p-value
  - Apply Bonferroni correction if testing multiple thresholds
- Domain-specific variance patterns:
  - Note: Full domain analysis reserved for Step 7
  - Focus on overall theta residual variance

**Output:**
- data/step07_residual_variance.csv (residual estimates, CIs, hypothesis tests)
- data/step07_measurement_error_correction.csv (reliability estimates, true residual)

**Validation Requirement:**
Validation tools MUST be used after residual variance calculation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_residual_variance.csv: 1 row x 8 columns
- Columns: residual_observed, residual_ci_lower, residual_ci_upper, residual_true, reliability_theta, p_greater_50pct, interpretation, sample_size
- data/step07_measurement_error_correction.csv: 1 row x 6 columns
- Columns: var_theta, mean_se_squared, reliability, attenuation_factor, residual_corrected, residual_observed

*Value Ranges:*
- Residual variance in [0, 1] range
- Reliability estimates in [0.50, 0.95] range (reasonable for IRT theta)
- CI bounds: ci_lower < observed < ci_upper
- p-values in [0, 1] range

*Data Quality:*
- Bootstrap CI successfully computed (non-degenerate)
- Reliability estimate reasonable (not extreme values)
- True residual > observed residual (measurement error correction working)
- Hypothesis test result interpretable

*Log Validation:*
- Required: "Residual variance calculated: X.XX (XX% unexplained)"
- Required: "Bootstrap CI complete: 1000 iterations"
- Required: "Measurement error correction applied"
- Required: "Reliability estimate: X.XX"
- Required: "True residual: X.XX (XX% after correction)"
- Required: "VALIDATION - PASS"
- Forbidden: "ERROR", "impossible reliability", "bootstrap failed"

**Expected Behavior on Validation Failure:**
Check reliability estimation procedure and bootstrap convergence. Document any issues with measurement error correction.

### Step 7: Domain-Specific Residual Analysis
**Dependencies:** Step 6 (overall residual calculated)
**Complexity:** High (~10 minutes)

**Purpose:** Repeat hierarchical regression analysis for each REMEMVR domain (What, Where, When) to examine differential unexplained variance

**Input:**
- data/step04_merged_predictors.csv (predictor set)
- results/ch5/5.2.1/data/step03_theta_scores.csv (What domain theta)
- results/ch5/5.2.2/data/step03_theta_scores.csv (Where domain theta)
- results/ch5/5.2.3/data/step03_theta_scores.csv (When domain theta)

**Processing:**
- Load domain-specific theta scores for all three domains
- Merge each domain with the same predictor set from Step 3
- For each domain (What, Where, When):
  - Fit hierarchical regression (same 3-block structure as Step 4)
  - Use same cross-validation procedure (5-fold, seed=42)
  - Calculate final Model 3 R² and residual variance
  - Compute bootstrap CI for residual (1000 iterations, seed=42)
  - Check assumptions and apply same remedial actions
- Compare residual variance across domains:
  - Test H0: Residual_What = Residual_Where = Residual_When
  - Use bootstrap approach to test equality of residuals
  - Multiple comparison correction for 3 domains
  - Expected pattern: When domain shows highest residual (hypothesis)
- Domain-specific interpretation:
  - What domain: Expected moderate residual (object memory)
  - Where domain: Expected low residual (spatial memory)
  - When domain: Expected high residual (temporal memory - most challenging)

**Output:**
- data/step08_domain_residuals.csv (residual variance by domain with CIs)
- data/step08_domain_comparison.csv (statistical tests of domain differences)

**Validation Requirement:**
Validation tools MUST be used after domain-specific analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_domain_residuals.csv: 3 rows x 8 columns
- Columns: domain, theta_mean, theta_sd, model3_R2, residual_variance, residual_ci_lower, residual_ci_upper, sample_size
- data/step08_domain_comparison.csv: 3 rows x 6 columns
- Columns: comparison, difference, ci_lower, ci_upper, p_uncorrected, p_bonferroni

*Value Ranges:*
- Domain theta in [-3, 3] range (IRT ability scale)
- R² values in [0, 1] range
- Residual variance in [0, 1] range
- All domains should have similar sample sizes (~95 participants)

*Data Quality:*
- All 3 domains successfully analyzed
- Bootstrap CIs computed for each domain
- Domain comparison tests completed
- When domain shows highest residual (confirm hypothesis)

*Log Validation:*
- Required: "Domain analysis complete: 3 domains"
- Required: "What residual: X.XX, Where residual: X.XX, When residual: X.XX"
- Required: "When domain highest residual: confirmed/rejected"
- Required: "Domain comparison tests complete"
- Required: "VALIDATION - PASS"
- Forbidden: "ERROR", "domain analysis failed", "missing theta"

**Expected Behavior on Validation Failure:**
Identify which domain analysis failed and check Ch5 theta file availability. Log detailed error for missing domain data.

### Step 8: Create Variance Decomposition Visualization Data
**Dependencies:** Steps 6-7 (residual analysis complete)
**Complexity:** Medium (~6 minutes)

**Purpose:** Prepare comprehensive dataset for variance decomposition visualization showing explained vs unexplained variance

**Input:**
- data/step06_incremental_validity.csv (block-wise R² increments)
- data/step07_residual_variance.csv (overall residual variance)
- data/step08_domain_residuals.csv (domain-specific residuals)

**Processing:**
- Create overall variance decomposition:
  - Demographics proportion: Delta_R²_block1
  - Cognitive proportion: Delta_R²_block2  
  - Self-report proportion: Delta_R²_block3
  - Residual proportion: 1 - R²_model3
- Calculate percentages and prepare for stacked visualization
- Create domain comparison data:
  - Domain names: What, Where, When
  - Explained variance: R²_model3 for each domain
  - Unexplained variance: 1 - R²_model3 for each domain
- Format data for thesis summary:
  - Key statistics table: N, total R², block contributions, residual
  - Effect size summary: f² values with interpretations
  - Domain comparison summary: residual variance by domain
- Generate text summary for results section:
  - Statistical significance statements with corrected p-values
  - Effect size interpretations with confidence intervals
  - Hypothesis support evaluation (>50% residual hypothesis)

**Output:**
- data/step09_variance_decomposition_plot_data.csv (for rq_plots visualization)
- data/step09_domain_comparison_plot_data.csv (for domain comparison plots)
- data/step09_thesis_summary_statistics.csv (key numbers for thesis writing)

**Validation Requirement:**
Validation tools MUST be used after visualization data preparation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step09_variance_decomposition_plot_data.csv: 4 rows x 4 columns
- Columns: component, variance_proportion, percentage, label
- data/step09_domain_comparison_plot_data.csv: 3 rows x 5 columns
- Columns: domain, explained, unexplained, total_variance, residual_rank
- data/step09_thesis_summary_statistics.csv: 1 row x 15 columns
- Key statistics: N, model1_R2, model2_R2, model3_R2, cognitive_f2, residual_pct, when_residual, etc.

*Value Ranges:*
- All proportions sum to 1.0 (+/- 0.01 rounding tolerance)
- Percentages in [0, 100] range
- Variance components all positive
- Domain residuals in expected order (When ≥ What ≥ Where)

*Data Quality:*
- All output files contain expected number of rows/columns
- No missing values in plot data
- Summary statistics internally consistent
- Visualization data properly formatted for plotting

*Log Validation:*
- Required: "Variance decomposition data created"
- Required: "Total variance accounted: X.XX (XX% explained)"
- Required: "Residual variance: X.XX (XX% unexplained)"
- Required: "Domain ordering: When (X.XX) > What (X.XX) > Where (X.XX)"
- Required: "Plot data formatted for visualization"
- Required: "VALIDATION - PASS"
- Forbidden: "ERROR", "proportions don't sum to 1", "missing plot data"

**Expected Behavior on Validation Failure:**
Check data formatting and calculation consistency. Regenerate plot data if formatting issues detected.

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (dependency checks)
- data/step01_cognitive_tests.csv (T-scored cognitive measures)
- data/step01_cognitive_correlation_matrix.csv (predictor intercorrelations)
- data/step02_demographics.csv (age, sex, education variables)
- data/step03_self_report.csv (DASS subscales, VR experience, sleep)
- data/step04_merged_predictors.csv (complete hierarchical regression dataset)
- data/step04_descriptive_stats.csv (descriptive statistics for all variables)
- data/step05_hierarchical_models.csv (R², F-stats, p-values for 3 models)
- data/step05_cross_validation_results.csv (CV performance by fold)
- data/step05_assumption_diagnostics.txt (normality, homoscedasticity, VIF)
- data/step06_incremental_validity.csv (Delta_R², Cohen's f², CIs, power)
- data/step06_effect_size_interpretation.csv (effect size categories)
- data/step07_residual_variance.csv (unexplained variance estimates)
- data/step07_measurement_error_correction.csv (reliability, true residual)
- data/step08_domain_residuals.csv (What/Where/When residual analysis)
- data/step08_domain_comparison.csv (statistical tests of domain differences)
- data/step09_variance_decomposition_plot_data.csv (visualization source data)
- data/step09_domain_comparison_plot_data.csv (domain plot data)
- data/step09_thesis_summary_statistics.csv (key statistics for writing)

### Logs (ONLY execution logs)
- logs/step00_dependency_validation.log
- logs/step01_extract_cognitive.log
- logs/step02_extract_demographics.log
- logs/step03_extract_self_report.log
- logs/step04_merge_data.log
- logs/step05_hierarchical_regression.log
- logs/step06_effect_sizes.log
- logs/step07_residual_analysis.log
- logs/step08_domain_analysis.log
- logs/step09_visualization_prep.log

### Plots (EMPTY until rq_plots runs)
Note: Plot source CSV files created in data/ folder with prefix step09_*_plot_data.csv

### Results (EMPTY until rq_results runs)
Note: summary.md will be created by rq_results agent

---

## Expected Data Formats

### Step-to-Step Transformations
1. **Step 1:** Raw cognitive scores → T-scores (M=50, SD=10)
2. **Step 2-3:** Extract additional predictors → merge on UID
3. **Step 4:** Complete dataset → standardized predictors (z-scores) + hierarchical blocks
4. **Step 5:** Nested models → incremental R², Cohen's f² with bootstrap CIs
5. **Step 6:** Model 3 R² → residual variance with measurement error correction
6. **Step 7:** Domain-specific theta → domain residual comparisons
7. **Step 8:** All results → visualization data and thesis summary

### Column Naming Conventions
- **Standardized predictors:** {variable}_z (e.g., Age_z, RAVLT_T_z)
- **Effect sizes:** delta_R2, f2, f2_ci_lower, f2_ci_upper
- **Bootstrap results:** *_ci_lower, *_ci_upper (95% percentile CIs)
- **Domain identifiers:** domain (What, Where, When)
- **Model identifiers:** model (Model1, Model2, Model3)

### Data Type Constraints
- **UID:** object (string identifier)
- **Theta scores:** float64, range [-3, 3]
- **T-scores:** float64, range [20, 80]
- **Z-scores:** float64, approximately [-3, 3]
- **R² values:** float64, range [0, 1]
- **p-values:** float64, range [0, 1]
- **Sample sizes:** int64, positive integers

---

## Cross-RQ Dependencies

**Required Ch5 Results:**
- Ch5 5.1.1: Overall REMEMVR theta scores (primary DV)
- Ch5 5.2.1: What domain theta scores (for domain analysis)
- Ch5 5.2.2: Where domain theta scores (for domain analysis)  
- Ch5 5.2.3: When domain theta scores (for domain analysis)

**Expected File Patterns:**
- Primary: results/ch5/5.X.X/data/step03_theta_scores.csv
- Alternative: results/ch5/5.X.X/data/*theta*.csv
- Fallback: results/ch5/5.X.X/data/*lmm*.{txt,rds,csv}

**Circuit Breakers:**
- If Ch5 5.1.1 not complete: QUIT with "Overall theta scores required"
- If domain files missing: Proceed with overall analysis only, document limitation

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
**4-Layer Validation:** Output files (dependency log), Value ranges (validation status), Data quality (file accessibility), Log validation (success patterns)

#### Step 1: Extract Cognitive Tests  
**4-Layer Validation:** Output files (100x6 T-scores), Value ranges (T-scores 20-80), Data quality (no missing, correlation matrix), Log validation (extraction success)

#### Step 2-3: Extract Demographics/Self-Report
**4-Layer Validation:** Output files (demographics, self-report), Value ranges (age 18-85, DASS 0-42), Data quality (minimal missing), Log validation (extraction counts)

#### Step 4: Merge Data
**4-Layer Validation:** Output files (merged dataset), Value ranges (standardized predictors), Data quality (complete cases), Log validation (merge success)

#### Step 5: Hierarchical Regression
**4-Layer Validation:** Output files (models, CV results, diagnostics), Value ranges (R² 0-1, p-values 0-1), Data quality (3 models fitted), Log validation (R² progression)

#### Step 6: Effect Sizes
**4-Layer Validation:** Output files (f² estimates, CIs), Value ranges (f² typically 0-2), Data quality (bootstrap convergence), Log validation (effect size categories)

#### Step 7: Residual Analysis
**4-Layer Validation:** Output files (residual estimates), Value ranges (residual 0-1), Data quality (reliability reasonable), Log validation (measurement correction)

#### Step 8: Domain Analysis
**4-Layer Validation:** Output files (domain residuals), Value ranges (domain theta -3 to 3), Data quality (all domains analyzed), Log validation (When domain highest)

#### Step 9: Visualization Data
**4-Layer Validation:** Output files (plot data CSVs), Value ranges (proportions sum to 1), Data quality (complete formatting), Log validation (visualization ready)

---

## Summary

**Total Steps:** 9 (Step 0: validation + Steps 1-8: analysis)
**Estimated Runtime:** 45-60 minutes
**Cross-RQ Dependencies:** Ch5 5.1.1 (required), Ch5 5.2.1-3 (optional for domains)
**Primary Outputs:** Hierarchical regression results, incremental validity assessment, domain residual analysis
**Validation Coverage:** 100% (all 9 steps have 4-layer validation requirements)

**Key Hypothesis:** REMEMVR should show >50% unexplained variance after accounting for all predictors, supporting incremental validity and ecological validity gap

**Critical Methodological Notes:**
- Conservative alpha correction (0.00179) requires large effects for significance
- Cross-validation with overfitting detection prevents inflated R² estimates
- Bootstrap confidence intervals for all effect sizes
- Comprehensive assumption checking with specified remedial actions
- Measurement error correction separates true residual from reliability artifacts
- Domain-specific analysis tests differential ecological validity across memory types

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan → creates 3_tools.yaml
3. rq_analysis reads plan + tools → creates 4_analysis.yaml
4. g_code reads analysis → generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent with v5.1 statistical specifications