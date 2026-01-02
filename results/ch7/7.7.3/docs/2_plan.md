# Analysis Plan: RQ 7.7.3 - Alternative RAVLT Scoring

**Research Question:** 7.7.3
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ compares multiple RAVLT scoring approaches to predict episodic memory performance measured via REMEMVR theta scores. Tests traditional Total score vs Learning gain vs proportional Learning Slope vs Recognition scores to determine which RAVLT metrics best predict ecological memory function. The analysis addresses clinical utility by identifying optimal RAVLT interpretation methods.

**Pipeline:** Multiple regression with systematic model comparison and cross-validation
**Steps:** 9 total analysis steps (Step 0: dependency validation + Steps 1-8: main analysis)
**Estimated Runtime:** 45-60 minutes total

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Chapter 7 Bonferroni correction: alpha = 0.00179/5 = 0.000358 for 5 models
- Bootstrap 95% CIs for all effect size estimates
- 5-fold cross-validation for predictive validity assessment

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify Ch5 5.1.1 theta outputs and master.xlsx accessibility before proceeding

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv (omnibus theta estimates)
- Alternative: results/ch5/5.1.1/data/*theta*.csv (any theta output)
- Fallback: results/ch5/5.1.1/data/step*theta*.{csv,txt} (broader search)
- Expected content: Participant UIDs with theta_all scores
- Also verify: data/cache/master.xlsx accessibility
- RAVLT columns required: T1Sc, T2Sc, T3Sc, T4Sc, T5Sc, DRSc, FRSc

**Processing:**
- Check Ch5 5.1.1 status.yaml shows rq_results: success
- Locate theta score file using search patterns
- Verify file contains theta_all column (omnibus scores)
- Check master.xlsx exists and RAVLT columns present
- Log all validation checks with specific file paths found
- If primary dependencies missing: QUIT with clear error message

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file, minimum 10 lines
- Content: validation results for Ch5 outputs and master.xlsx

*Value Ranges:*
- File size validation: txt file should be 200-2000 bytes
- Required content: file paths, validation status (PASS/FAIL)

*Data Quality:*
- All dependency checks completed (Ch5 status, theta file, master.xlsx)
- Clear PASS/FAIL status for each dependency
- Specific file paths documented if found

*Log Validation:*
- Required patterns: "Ch5 5.1.1 status: success", "Theta file located", "RAVLT columns verified"
- Forbidden patterns: "ERROR", "dependency missing", "file not found"
- Acceptable warnings: none for this critical validation step

**Expected Behavior on Validation Failure:**
Raise error with specific missing dependency, log to logs/step00_validate_dependencies.log, quit immediately and invoke g_debug.

### Step 1: Extract and Merge Data
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Medium (~8 minutes including data quality checks)

**Purpose:** Extract theta_all scores from Ch5 and RAVLT scores from master.xlsx, create merged analysis dataset

**Input:**
- results/ch5/5.1.1/data/step03_theta_scores.csv (or pattern match from Step 0)
- data/cache/master.xlsx (RAVLT columns: T1Sc-T5Sc, DRSc, FRSc)

**Processing:**
- Load theta_all scores: extract UID and theta_all columns only
- Load RAVLT scores: extract UID, T1Sc, T2Sc, T3Sc, T4Sc, T5Sc, DRSc, FRSc
- Merge datasets on UID using inner join (complete data only)
- Check data quality:
  - Missing data patterns (require <5% missing per variable)
  - Outlier detection: theta_all in [-4, 4] range (IRT validity)
  - RAVLT range checks: T1-T5 in [0, 15], DR in [0, 15], FR in [0, 15]
- Document excluded participants and reasons
- Final dataset: N=100 participants with complete RAVLT and REMEMVR data

**Output:**
- data/step01_merged_data.csv
- data/step01_data_quality_report.txt

**Validation Requirement:**
Validation tools MUST be used after data extraction and merging execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_merged_data.csv: 100 rows × 8 columns minimum
- Columns: UID (object), theta_all (float64), T1Sc-T5Sc (int64), DRSc (int64), FRSc (int64)
- data/step01_data_quality_report.txt: text summary file

*Value Ranges:*
- theta_all in [-4, 4] (valid IRT range)
- T1Sc through T5Sc in [0, 15] (RAVLT trial score range)
- DRSc in [0, 15] (delayed recall range)
- FRSc in [0, 50] (false recognition range, different scale)

*Data Quality:*
- Exactly 100 participants (N=100 complete cases)
- No missing values in any column (complete data requirement)
- No duplicate UIDs
- All values within expected ranges

*Log Validation:*
- Required patterns: "Data merge complete: N=100", "Quality checks passed"
- Forbidden patterns: "ERROR", "missing data >5%", "invalid range"
- Acceptable warnings: "minor outliers identified" (if documented)

**Expected Behavior on Validation Failure:**
Raise error with specific data quality issue, log to logs/step01_extract_merge.log, quit immediately and invoke g_debug.

### Step 2: Compute Alternative RAVLT Metrics
**Dependencies:** Step 1 (merged data)
**Complexity:** Low (<5 minutes)

**Purpose:** Calculate alternative RAVLT scoring methods for comparison with traditional Total score

**Input:**
- data/step01_merged_data.csv

**Processing:**
- Compute RAVLT metrics:
  - Total = T1Sc + T2Sc + T3Sc + T4Sc + T5Sc (traditional total score)
  - Learning = T5Sc - T1Sc (absolute learning gain)
  - LearningSlope = (T5Sc - T1Sc) / T1Sc (proportional learning gain, handle T1Sc=0)
  - Forgetting = T5Sc - DRSc (learning to delay decline)
  - Recognition = FRSc (delayed recognition performance)
- Handle division by zero: if T1Sc = 0, set LearningSlope = T5Sc (equivalent to infinite slope)
- Standardize all variables (z-scores): theta_all, Total, Learning, LearningSlope, Forgetting, Recognition
- Compute correlation matrix between all RAVLT metrics (check multicollinearity)
- Document metric distributions and intercorrelations

**Output:**
- data/step02_ravlt_metrics.csv
- data/step02_correlation_matrix.csv

**Validation Requirement:**
Validation tools MUST be used after RAVLT metric computation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_ravlt_metrics.csv: 100 rows × 12 columns
- Columns: UID, theta_all, Total, Learning, LearningSlope, Forgetting, Recognition (raw + standardized versions)
- data/step02_correlation_matrix.csv: 6 × 6 correlation matrix

*Value Ranges:*
- Standardized variables (z-scores): mean ≈ 0 (±0.1), std ≈ 1 (±0.1)
- Raw Total: [15, 75] typical range (sum of 5 trials × 15 max)
- Raw Learning: [-10, 14] typical range (T5-T1 difference)
- LearningSlope: [0, 15] (handled division by zero appropriately)
- Correlations: [-1, 1] valid correlation range

*Data Quality:*
- All 100 participants present
- No NaN values except potentially in LearningSlope (documented if T1Sc=0)
- Standardized variables properly centered and scaled
- Correlation matrix symmetric with 1.0 on diagonal

*Log Validation:*
- Required patterns: "RAVLT metrics computed", "Standardization complete", "Correlation matrix created"
- Forbidden patterns: "ERROR", "division by zero", "NaN values"
- Acceptable warnings: "T1Sc=0 cases handled" (if applicable)

**Expected Behavior on Validation Failure:**
Raise error with specific computation issue, log to logs/step02_compute_metrics.log, quit immediately and invoke g_debug.

### Step 3: Fit Individual Prediction Models
**Dependencies:** Step 2 (RAVLT metrics)
**Complexity:** Medium (~10 minutes including diagnostics)

**Purpose:** Fit 5 separate regression models to compare predictive validity of different RAVLT scoring methods

**Input:**
- data/step02_ravlt_metrics.csv (standardized scores)

**Processing:**
- Fit 5 regression models using standardized variables:
  - Model 1: theta_all ~ Total (traditional approach)
  - Model 2: theta_all ~ Learning (absolute learning gain)
  - Model 3: theta_all ~ LearningSlope (proportional learning gain)
  - Model 4: theta_all ~ Recognition (recognition performance)
  - Model 5: theta_all ~ Total + Learning (incremental validity test)
- Implementation: statsmodels.api.OLS for each model
- Extract model statistics: R², adjusted R², F-statistic, AIC, BIC
- Extract coefficients with standard errors and 95% CIs
- Multiple comparison correction:
  - Family: 5 models within this RQ
  - Bonferroni: alpha = 0.00179/5 = 0.000358 per model
  - FDR correction using Benjamini-Hochberg
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Check basic assumptions for each model:
  - Normality: Shapiro-Wilk test on residuals
  - Homoscedasticity: Breusch-Pagan test
  - Multicollinearity: VIF for Model 5 (multiple predictors)

**Output:**
- data/step03_model_comparison.csv
- data/step03_model_coefficients.csv
- data/step03_assumption_checks.csv

**Validation Requirement:**
Validation tools MUST be used after regression model fitting.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_model_comparison.csv: 5 rows × 8 columns
- Columns: model, R2, adj_R2, F_stat, p_uncorrected, p_bonferroni, p_fdr, AIC, BIC
- data/step03_model_coefficients.csv: 6 rows × 7 columns (5 single + 1 multiple predictor)
- data/step03_assumption_checks.csv: 5 rows × 6 columns (normality, heteroscedasticity, VIF tests)

*Value Ranges:*
- R² in [0, 1] (proportion of variance explained)
- F-statistics > 0 (positive F-values)
- p-values in [0, 1] (valid probability range)
- Bonferroni p-values >= uncorrected p-values (correction increases p-values)
- Coefficients approximately [-2, 2] range for standardized predictors

*Data Quality:*
- All 5 models fitted successfully
- Dual p-value reporting present (Decision D068: uncorrected + corrected)
- Model 5 VIF values calculated (multiple predictors)
- No missing values in model statistics

*Log Validation:*
- Required patterns: "5 models fitted successfully", "Bonferroni correction applied", "Assumption checks complete"
- Forbidden patterns: "ERROR", "model convergence failed", "singular matrix"
- Acceptable warnings: "heteroscedasticity detected" (handled with robust SEs)

**Expected Behavior on Validation Failure:**
Raise error with specific model fitting issue, log to logs/step03_fit_models.log, quit immediately and invoke g_debug.

### Step 4: Bootstrap Confidence Intervals for Effect Sizes
**Dependencies:** Step 3 (fitted models)
**Complexity:** High (~12 minutes for 1000 bootstrap iterations)

**Purpose:** Generate robust 95% confidence intervals for R² and regression coefficients using bootstrap resampling

**Input:**
- data/step02_ravlt_metrics.csv (for bootstrap resampling)
- Model specifications from Step 3

**Processing:**
- Implement participant-level bootstrap resampling:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Sample participants WITH replacement, keep all their data
  - For each iteration: fit all 5 models, extract R² and coefficients
- Compute bootstrap statistics:
  - 95% CI for R² per model: percentile method (2.5th, 97.5th percentiles)
  - 95% CI for regression coefficients: percentile method
  - Bootstrap SE for each statistic
- Effect size calculations:
  - Cohen's f² = R²/(1-R²) for each model
  - Semi-partial correlations (sr²) for unique variance in Model 5
  - Bootstrap CIs for all effect sizes
- Compare bootstrap CIs with parametric CIs from Step 3
- Document bootstrap distribution characteristics (mean, SE, skewness)

**Output:**
- data/step04_bootstrap_results.csv
- data/step04_effect_sizes.csv
- data/step04_bootstrap_distributions.csv

**Validation Requirement:**
Validation tools MUST be used after bootstrap CI computation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_bootstrap_results.csv: 5 rows × 10 columns
- Columns: model, R2_mean, R2_ci_lower, R2_ci_upper, coef_mean, coef_ci_lower, coef_ci_upper, bootstrap_se
- data/step04_effect_sizes.csv: 5 rows × 6 columns (f², sr², CIs)
- data/step04_bootstrap_distributions.csv: 5000 rows × 6 columns (1000 iterations × 5 models)

*Value Ranges:*
- Bootstrap R² means close to original estimates (±0.02 tolerance)
- CI widths reasonable: typically 0.10-0.20 for R² CIs
- Cohen's f² values: small (0.02), medium (0.15), large (0.35) benchmarks
- Bootstrap SEs > 0 (positive standard errors)

*Data Quality:*
- Exactly 1000 bootstrap iterations completed
- All confidence intervals valid (lower < upper)
- No missing values in bootstrap statistics
- Bootstrap means approximate original model estimates

*Log Validation:*
- Required patterns: "Bootstrap complete: 1000 iterations", "Random seed: 42", "CI computation successful"
- Forbidden patterns: "ERROR", "bootstrap failed", "invalid CI"
- Acceptable warnings: "non-normal bootstrap distribution" (robust to non-normality)

**Expected Behavior on Validation Failure:**
Raise error with specific bootstrap issue, log to logs/step04_bootstrap_cis.log, quit immediately and invoke g_debug.

### Step 5: Cross-Validation for Predictive Performance
**Dependencies:** Step 2 (RAVLT metrics)
**Complexity:** Medium (~8 minutes for 5-fold CV)

**Purpose:** Assess generalizability of models through cross-validation and detect overfitting

**Input:**
- data/step02_ravlt_metrics.csv

**Processing:**
- Implement 5-fold cross-validation:
  - Method: sklearn.model_selection.KFold
  - Random seed: 42 for reproducibility
  - Shuffle: True (randomize before splitting)
  - Stratification: None (continuous outcome)
- For each fold and each model:
  - Split data: 80% training, 20% test (20 participants per test fold)
  - Fit model on training data
  - Evaluate on test data: compute R², RMSE, MAE
  - Store predictions and residuals
- Aggregate CV results:
  - Mean and SD of R² across 5 folds per model
  - Mean and SD of RMSE, MAE per model
  - Compute generalization gap: |training R² - test R²|
  - Flag overfitting if gap > 0.10 for any model
- Compare CV R² with original full-sample R² from Step 3
- Document prediction accuracy and model stability

**Output:**
- data/step05_cross_validation.csv
- data/step05_cv_predictions.csv
- data/step05_generalization_gaps.csv

**Validation Requirement:**
Validation tools MUST be used after cross-validation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_cross_validation.csv: 5 rows × 8 columns
- Columns: model, cv_R2_mean, cv_R2_sd, cv_RMSE_mean, cv_RMSE_sd, cv_MAE_mean, cv_MAE_sd, generalization_gap
- data/step05_cv_predictions.csv: 500 rows × 5 columns (100 participants × 5 models)
- data/step05_generalization_gaps.csv: 25 rows × 4 columns (5 folds × 5 models)

*Value Ranges:*
- CV R² typically 0.05-0.10 lower than full-sample R² (expected shrinkage)
- RMSE values > 0 (positive prediction errors)
- MAE values > 0 and typically smaller than RMSE
- Generalization gaps < 0.15 (reasonable overfitting threshold)

*Data Quality:*
- All 5 folds completed for all 5 models (25 total CV runs)
- CV statistics computed for all models
- Predictions available for all 100 participants across models
- No missing values in CV results

*Log Validation:*
- Required patterns: "5-fold CV complete", "Random seed: 42", "Generalization gaps computed"
- Forbidden patterns: "ERROR", "CV failed", "fold processing error"
- Acceptable warnings: "overfitting detected" (if gap > 0.10, flagged appropriately)

**Expected Behavior on Validation Failure:**
Raise error with specific CV issue, log to logs/step05_cross_validation.log, quit immediately and invoke g_debug.

### Step 6: Model Diagnostics and Assumption Testing
**Dependencies:** Step 3 (fitted models)
**Complexity:** Medium (~8 minutes including diagnostic plots)

**Purpose:** Comprehensive regression assumption testing and remedial actions for violations

**Input:**
- data/step02_ravlt_metrics.csv (for residual analysis)
- Fitted model objects from Step 3

**Processing:**
- Comprehensive assumption testing for each model:
  - Normality: Shapiro-Wilk test on residuals + Q-Q plot data
  - Homoscedasticity: Breusch-Pagan test + residual vs fitted plots
  - Linearity: Partial residual plots for each predictor
  - Independence: Design-based (satisfied by between-subjects design)
  - Multicollinearity: VIF for Model 5 (multiple predictors), threshold VIF < 5
  - Outlier detection: Cook's distance, threshold D < 4/100 = 0.04
- Identify assumption violations:
  - Count models failing each assumption test (p < 0.05)
  - Document outliers (participants with high Cook's D)
  - Assess severity of violations for interpretation impact
- Remedial actions based on violations:
  - Normality p < 0.05: Flag for bootstrap CI preference (Step 4)
  - Heteroscedasticity p < 0.05: Compute HC3 robust standard errors
  - VIF > 5: Document multicollinearity, consider ridge if VIF > 10
  - Outliers (Cook's D > 0.04): Document influence, sensitivity analysis
- Generate diagnostic summary with recommendations

**Output:**
- data/step06_diagnostics_summary.csv
- data/step06_assumption_tests.csv
- data/step06_outliers.csv
- data/step06_remedial_actions.txt

**Validation Requirement:**
Validation tools MUST be used after diagnostic testing execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_diagnostics_summary.csv: 5 rows × 8 columns
- Columns: model, normality_p, homoscedasticity_p, max_vif, outliers_count, violations, remedial_action
- data/step06_assumption_tests.csv: 5 rows × 6 columns (detailed test results)
- data/step06_outliers.csv: variable rows × 4 columns (participants with Cook's D > 0.04)
- data/step06_remedial_actions.txt: text summary of recommendations

*Value Ranges:*
- p-values in [0, 1] for all diagnostic tests
- VIF values > 1.0 (multicollinearity measure)
- Cook's D values in [0, 1] range (influence measure)
- Outlier count typically 0-5 participants (5% threshold)

*Data Quality:*
- All 5 models tested for all assumptions
- Clear PASS/FAIL designation for each assumption per model
- Outliers properly identified with specific UIDs
- Remedial actions specified for all violations

*Log Validation:*
- Required patterns: "Assumption testing complete", "Outliers identified", "Remedial actions documented"
- Forbidden patterns: "ERROR", "diagnostic test failed", "invalid VIF"
- Acceptable warnings: "normality violation detected" (handled with bootstrap)

**Expected Behavior on Validation Failure:**
Raise error with specific diagnostic issue, log to logs/step06_model_diagnostics.log, quit immediately and invoke g_debug.

### Step 7: Power Analysis and Sensitivity Testing
**Dependencies:** Step 3 (model results)
**Complexity:** Medium (~6 minutes)

**Purpose:** Assess statistical power for observed effects and conduct sensitivity analyses

**Input:**
- data/step03_model_comparison.csv (effect sizes)
- Study design parameters: N=100, alpha=0.000358 (Bonferroni corrected)

**Processing:**
- Post-hoc power analysis:
  - For each model: compute achieved power for observed R²
  - Use statsmodels.stats.power.FTestAnovaPower() or equivalent
  - Convert R² to Cohen's f² for power calculation: f² = R²/(1-R²)
  - Calculate minimum detectable effect at 80% power given N=100, alpha=0.000358
  - Report actual power for incremental validity (Model 5 vs Model 1 comparison)
- Sensitivity analysis for influential cases:
  - Rerun all 5 models excluding outliers (Cook's D > 0.04 from Step 6)
  - Compare conclusions with/without outliers
  - Assess robustness of model ranking (which RAVLT method best predicts)
  - Document changes in significance status after outlier removal
- Effect size interpretation:
  - Clinical significance thresholds: small (f² = 0.02), medium (f² = 0.15), large (f² = 0.35)
  - Incremental validity benchmark: ΔR² > 0.05 for meaningful improvement
  - Compare observed effects with these benchmarks

**Output:**
- data/step07_power_analysis.csv
- data/step07_sensitivity_analysis.csv
- data/step07_effect_benchmarks.csv

**Validation Requirement:**
Validation tools MUST be used after power and sensitivity analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_power_analysis.csv: 5 rows × 6 columns
- Columns: model, observed_f2, achieved_power, min_detectable_f2, adequate_power (>0.80), power_assessment
- data/step07_sensitivity_analysis.csv: 10 rows × 8 columns (5 models × 2 conditions: with/without outliers)
- data/step07_effect_benchmarks.csv: 5 rows × 5 columns (effect size classifications)

*Value Ranges:*
- Power values in [0, 1] range (probability)
- f² values > 0 (positive effect sizes)
- Typically: achieved power 0.20-0.95 for observed effects
- Min detectable f² typically 0.08-0.15 at 80% power with N=100

*Data Quality:*
- Power analysis completed for all 5 models
- Sensitivity analysis includes both full and outlier-excluded results
- Clear indication of adequate vs inadequate power (>0.80 threshold)
- Effect size benchmarks properly classified

*Log Validation:*
- Required patterns: "Power analysis complete", "Sensitivity analysis complete", "Effect benchmarks classified"
- Forbidden patterns: "ERROR", "power calculation failed", "invalid f-squared"
- Acceptable warnings: "low power detected" (acknowledged limitation)

**Expected Behavior on Validation Failure:**
Raise error with specific power/sensitivity issue, log to logs/step07_power_sensitivity.log, quit immediately and invoke g_debug.

### Step 8: Clinical Interpretation Summary
**Dependencies:** Steps 3-7 (all analysis results)
**Complexity:** Low (~5 minutes)

**Purpose:** Synthesize results into clinical recommendations for optimal RAVLT interpretation

**Input:**
- data/step03_model_comparison.csv (model performance)
- data/step04_effect_sizes.csv (effect size estimates)
- data/step05_cross_validation.csv (generalizability)
- data/step07_power_analysis.csv (statistical power)

**Processing:**
- Rank RAVLT methods by predictive validity:
  - Primary criterion: Cross-validated R² (Step 5)
  - Secondary criteria: Effect size significance, bootstrap CI exclusion of zero
  - Document best performing single predictor
  - Assess incremental validity: Does Learning add beyond Total?
- Clinical interpretation guidelines:
  - Identify RAVLT method with highest ecological validity (best REMEMVR prediction)
  - Quantify improvement over traditional Total score approach
  - Assess clinical meaningfulness: ΔR² > 0.05 threshold for practice change
  - Consider power limitations for non-significant findings
- Generate clinical recommendations:
  - Primary recommendation: Optimal RAVLT scoring method for ecological memory assessment
  - Secondary recommendation: Whether to include Learning metrics beyond Total
  - Qualification: Sample characteristics and generalizability limitations
  - Implementation guidance: How to compute and interpret recommended metrics
- Summarize statistical evidence quality:
  - Document assumption violations and remedial actions taken
  - Report cross-validation evidence for generalizability
  - Acknowledge power limitations where applicable

**Output:**
- data/step08_clinical_summary.csv
- data/step08_ravlt_recommendations.txt
- data/step08_evidence_quality.txt

**Validation Requirement:**
Validation tools MUST be used after clinical interpretation synthesis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_clinical_summary.csv: 5 rows × 8 columns
- Columns: ravlt_method, cv_R2, effect_size_f2, clinical_significance, power_adequate, recommendation_rank
- data/step08_ravlt_recommendations.txt: text file with clinical guidance
- data/step08_evidence_quality.txt: text summary of methodological strengths/limitations

*Value Ranges:*
- Recommendation ranks: 1-5 (ordinal ranking of RAVLT methods)
- Clinical significance: binary (meaningful/not meaningful based on ΔR² > 0.05)
- Power adequate: binary (>0.80 threshold)

*Data Quality:*
- All 5 RAVLT methods ranked from best to worst predictive validity
- Clear primary recommendation identified
- Evidence quality assessment includes all major methodological considerations
- Practical implementation guidance provided

*Log Validation:*
- Required patterns: "Clinical summary complete", "Recommendations generated", "Evidence quality assessed"
- Forbidden patterns: "ERROR", "ranking failed", "incomplete summary"
- Acceptable warnings: "limited generalizability" (acknowledged in evidence quality)

**Expected Behavior on Validation Failure:**
Raise error with specific interpretation issue, log to logs/step08_clinical_summary.log, quit immediately and invoke g_debug.

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (Ch5 and master.xlsx verification)
- data/step01_merged_data.csv (theta + RAVLT scores, N=100)
- data/step01_data_quality_report.txt (missing data and outlier summary)
- data/step02_ravlt_metrics.csv (computed alternative scoring methods)
- data/step02_correlation_matrix.csv (RAVLT metric intercorrelations)
- data/step03_model_comparison.csv (R², F-statistics, dual p-values)
- data/step03_model_coefficients.csv (regression betas with CIs)
- data/step03_assumption_checks.csv (normality, homoscedasticity tests)
- data/step04_bootstrap_results.csv (bootstrap CIs for R² and coefficients)
- data/step04_effect_sizes.csv (Cohen's f², semi-partial correlations)
- data/step04_bootstrap_distributions.csv (1000 bootstrap iterations)
- data/step05_cross_validation.csv (5-fold CV performance metrics)
- data/step05_cv_predictions.csv (out-of-sample predictions)
- data/step05_generalization_gaps.csv (overfitting assessment)
- data/step06_diagnostics_summary.csv (assumption test results)
- data/step06_assumption_tests.csv (detailed diagnostic statistics)
- data/step06_outliers.csv (influential cases identification)
- data/step06_remedial_actions.txt (violation handling recommendations)
- data/step07_power_analysis.csv (statistical power for observed effects)
- data/step07_sensitivity_analysis.csv (results with/without outliers)
- data/step07_effect_benchmarks.csv (clinical significance assessment)
- data/step08_clinical_summary.csv (RAVLT method rankings)
- data/step08_ravlt_recommendations.txt (clinical practice guidance)
- data/step08_evidence_quality.txt (methodological limitations summary)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_merge.log
- logs/step02_compute_metrics.log
- logs/step03_fit_models.log
- logs/step04_bootstrap_cis.log
- logs/step05_cross_validation.log
- logs/step06_model_diagnostics.log
- logs/step07_power_sensitivity.log
- logs/step08_clinical_summary.log

### Plots (EMPTY until rq_plots runs)
Note: Plot source CSVs created in data/ folder:
- step03_model_comparison.csv provides R² comparison plot data
- step04_effect_sizes.csv provides Cohen's f² comparison plot data
- step05_cross_validation.csv provides CV performance plot data
- step06_diagnostics_summary.csv provides assumption violation plot data

### Results (EMPTY until rq_results runs)
Note: summary.md created by rq_results will synthesize clinical recommendations

---

## Expected Data Formats

### Step-to-Step Transformations
1. **Ch5 theta scores + master.xlsx RAVLT → merged dataset** (Step 1)
2. **Merged data → alternative RAVLT metrics + standardized scores** (Step 2)
3. **Standardized data → 5 fitted regression models + diagnostics** (Step 3)
4. **Models → bootstrap CIs and effect sizes** (Step 4)
5. **Data → cross-validation performance metrics** (Step 5)
6. **Models → assumption tests and remedial actions** (Step 6)
7. **Results → power analysis and sensitivity tests** (Step 7)
8. **All results → clinical interpretation and recommendations** (Step 8)

### Column Naming Conventions
- **UIDs:** Consistent "UID" column across all datasets
- **RAVLT scores:** T1Sc, T2Sc, T3Sc, T4Sc, T5Sc, DRSc, FRSc (raw scores)
- **RAVLT metrics:** Total, Learning, LearningSlope, Forgetting, Recognition
- **Standardized:** Add "_std" suffix (e.g., Total_std, Learning_std)
- **Model results:** prefix with model number (e.g., model1_R2, model1_p_uncorrected)
- **Bootstrap:** Add "_boot_" infix (e.g., R2_boot_mean, R2_boot_ci_lower)
- **Cross-validation:** Add "cv_" prefix (e.g., cv_R2_mean, cv_RMSE_mean)

### Data Type Constraints
- **UIDs:** String/object type, unique identifier
- **Theta scores:** Float64, range [-4, 4], no missing values
- **RAVLT scores:** Int64, ranges [0, 15] for recall, [0, 50] for recognition
- **Model statistics:** Float64, R² in [0, 1], p-values in [0, 1]
- **Effect sizes:** Float64, Cohen's f² ≥ 0, CIs properly ordered
- **Boolean flags:** True/False for adequate power, clinical significance

---

## Cross-RQ Dependencies

**Primary Dependency:**
- **Source RQ:** Ch5 5.1.1 (Functional Form Comparison)
- **Required Status:** rq_results = success
- **File Paths:** 
  - Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
  - Alternative: results/ch5/5.1.1/data/*theta*.csv
  - Fallback: results/ch5/5.1.1/data/step*theta*.{csv,txt}
- **Required Content:** Participant UIDs with omnibus theta_all scores
- **If Missing:** QUIT with "Ch5 5.1.1 theta outputs not found"

**Secondary Dependency:**
- **Source:** Master data file
- **File Path:** data/cache/master.xlsx
- **Required Content:** RAVLT columns (T1Sc through FRSc)
- **If Missing:** QUIT with "Master.xlsx not accessible"

**Validation Strategy:**
Step 0 validates all dependencies before proceeding with analysis pipeline

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Architecture Integration
- **Agent Role:** rq_planner embeds validation requirements (this file)
- **Execution Role:** rq_inspect validates outputs match expectations
- **Validation Tools:** Determined by rq_tools based on analysis types
- **Failure Behavior:** Immediate quit with g_debug invocation

### Statistical Implementation Requirements
All statistical procedures specify:
- **Random seeds:** seed=42 for reproducibility (bootstrap, cross-validation)
- **Bootstrap:** 1000 iterations, participant-level resampling, percentile CIs
- **Cross-validation:** 5-fold, shuffled, gap threshold <0.10
- **Multiple comparisons:** Bonferroni + FDR, dual p-value reporting
- **Assumption violations:** Specific remedial actions for each violation type
- **Power analysis:** Post-hoc with effect size benchmarks

### Validation Coverage Summary
- **Step 0:** Dependency validation (Ch5 outputs + master.xlsx)
- **Step 1:** Data extraction and merging validation
- **Step 2:** RAVLT metric computation validation
- **Step 3:** Regression model fitting validation
- **Step 4:** Bootstrap CI computation validation
- **Step 5:** Cross-validation execution validation
- **Step 6:** Model diagnostics validation
- **Step 7:** Power and sensitivity analysis validation
- **Step 8:** Clinical interpretation synthesis validation

**Validation Percentage:** 100% (all 9 steps have 4-layer validation requirements)

---

## Summary

**Total Steps:** 9 (dependency validation + 8 analysis steps)
**Estimated Runtime:** 45-60 minutes
**Cross-RQ Dependencies:** Ch5 5.1.1 (theta outputs), master.xlsx (RAVLT scores)
**Primary Outputs:** Clinical recommendations for optimal RAVLT interpretation
**Validation Coverage:** 100% (all 9 steps have 4-layer validation requirements)

**Key Hypothesis:** Learning-based RAVLT metrics (Learning Slope, absolute Learning gain) will demonstrate superior predictive validity for ecological memory performance compared to traditional Total score, with incremental validity beyond 0.05 R² threshold justifying clinical practice recommendations.

**Critical Methodological Notes:**
- Bonferroni correction for 5-model comparison (alpha = 0.000358) addresses multiple testing
- Bootstrap confidence intervals provide robust effect size estimates
- 5-fold cross-validation assesses generalizability of predictive validity findings
- Comprehensive assumption testing with specified remedial actions ensures result validity
- Power analysis acknowledges limitations for non-significant incremental validity findings
- Clinical interpretation thresholds (ΔR² > 0.05) provide practical significance benchmarks

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan → creates 3_tools.yaml
3. rq_analysis reads plan + tools → creates 4_analysis.yaml
4. g_code reads analysis → generates executable code

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent