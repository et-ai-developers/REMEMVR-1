# Analysis Plan: RQ 7.2.4 - VR Scaffolding Validation

**Research Question:** 7.2.4
**Created:** 2026-01-03  
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This analysis plan tests the VR scaffolding hypothesis by comparing age-related decline patterns between traditional episodic memory testing (RAVLT) and VR-based episodic memory testing (REMEMVR) within the same sample of 100 participants. The analysis uses bivariate correlations and Steiger's Z-test for dependent correlation comparison to test whether VR context provides compensatory scaffolding that traditional tests lack.

**Pipeline:** Correlation Analysis with Dependent Correlation Comparison (Steiger's Z-test)
**Steps:** 8 total analysis steps (Step 0: validation + Steps 1-7: analysis)  
**Estimated Runtime:** 45-60 minutes

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni corrected)

**Key Methodological Features:**
- Within-subjects design controls for individual differences
- Steiger's Z-test handles dependent correlations (both share Age variable)
- Bootstrap confidence intervals for robust effect size estimation
- Multiple sensitivity analyses to test robustness

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies

**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 5.1.1 outputs exist and validate data accessibility before proceeding

**Input:**
- Primary: results/ch5/5.1.1/status.yaml (verify rq_results: success)
- Alternative: results/ch5/5.1.1/data/step03_theta_scores.csv
- Fallback: results/ch5/5.1.1/data/*theta*.{csv,txt}
- Expected content: REMEMVR theta_all scores for 100 participants
- Also verify: data/cache/master.xlsx accessibility

**Processing:**
- Check Ch5 5.1.1 completed successfully in status.yaml
- Locate theta score file using multiple path patterns
- Verify file contains theta_all column for 100 participants
- Check master.xlsx contains RAVLT and Age data
- Log validation results with specific file paths found
- If Ch5 incomplete: QUIT with "Ch5 5.1.1 required for REMEMVR theta scores"

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Contains: file paths found, data dimensions, validation status

*Value Ranges:*
- Validation status: "PASS" or "FAIL" 
- File counts: At least 1 theta file found from Ch5
- Participant counts: 100 participants in both REMEMVR and master data

*Data Quality:*
- All required files accessible
- No critical dependencies missing
- REMEMVR theta file contains theta_all column
- Master file contains RAVLT_Total and Age columns

*Log Validation:*
- Required patterns: "Dependency validation: PASS", "Ch5 5.1.1: SUCCESS"
- Required patterns: "Files found: [specific paths]", "N participants: 100"
- Forbidden patterns: "FAIL", "not found", "missing"

**Expected Behavior on Validation Failure:**
Raise error with specific missing dependency, log to logs/step00_validate_dependencies.log, invoke g_debug

### Step 1: Extract and Prepare REMEMVR Data

**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (~5 minutes)

**Purpose:** Extract REMEMVR theta_all scores from Ch5 5.1.1 outputs and prepare for correlation analysis

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/*theta*all*.csv
- Expected format: UID, theta_all, se_theta_all columns

**Processing:**
- Load REMEMVR theta score file from Ch5 5.1.1
- Extract UID and theta_all columns
- Remove any participants with missing theta_all values
- Standardize theta_all scores (z-score transformation): z = (x - mean) / sd
- Random seed: 42 for any randomized operations (placeholder for consistency)
- Compute descriptive statistics: N, mean, SD, min, max, skewness
- Check for potential ceiling/floor effects: % participants at ±2 SD from mean
- Flag if >5% participants at extreme values (range restriction concern)

**Output:**
- data/step01_rememvr_theta_data.csv (UID, theta_all, theta_all_z)

**Validation Requirement:**
Validation tools MUST be used after REMEMVR data extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_rememvr_theta_data.csv: 100 rows x 3 columns
- Columns: UID (object), theta_all (float64), theta_all_z (float64)

*Value Ranges:*
- theta_all in [-3, 3] (typical IRT theta range)
- theta_all_z approximately N(0,1) distribution (mean ≈ 0, SD ≈ 1)
- No infinite or NaN values

*Data Quality:*
- Exactly 100 participants (no missing UIDs)
- No duplicate UIDs
- All theta_all values finite and reasonable
- Standardized scores properly computed (mean ≈ 0, SD ≈ 1)

*Log Validation:*
- Required patterns: "REMEMVR data extracted: 100 participants"
- Required patterns: "Descriptives: mean=X.XX, sd=X.XX"
- Required patterns: "Range restriction check: X.X% extreme values"
- Forbidden patterns: "ERROR", "missing", "NaN values"

**Expected Behavior on Validation Failure:**
Raise error with specific data issue, log to logs/step01_extract_rememvr.log, invoke g_debug

### Step 2: Extract and Prepare RAVLT Data

**Dependencies:** Step 1 (REMEMVR data prepared)
**Complexity:** Low (~5 minutes)

**Purpose:** Extract RAVLT total scores and age data from master.xlsx for correlation analysis

**Input:**
- data/cache/master.xlsx
- Expected sheets: participant data with RAVLT_Total and Age columns

**Processing:**
- Load master.xlsx and locate participant data sheet
- Extract UID, RAVLT_Total, and Age columns
- Remove participants with missing RAVLT or Age data
- Standardize RAVLT_Total scores (z-score transformation): z = (x - mean) / sd
- Random seed: 42 for any randomized operations (consistency)
- Compute descriptive statistics for both RAVLT and Age
- Check age distribution: mean, SD, range, confirm adequate variance for correlation
- Flag if age range <20 years (insufficient variance concern)
- Check for potential ceiling/floor effects in RAVLT scores

**Output:**
- data/step02_ravlt_age_data.csv (UID, RAVLT_Total, RAVLT_Total_z, Age)

**Validation Requirement:**
Validation tools MUST be used after RAVLT data extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_ravlt_age_data.csv: 100 rows x 4 columns  
- Columns: UID (object), RAVLT_Total (float64), RAVLT_Total_z (float64), Age (float64)

*Value Ranges:*
- RAVLT_Total in [0, 80] (typical RAVLT scoring range)
- RAVLT_Total_z approximately N(0,1) distribution
- Age in [18, 80] (adult lifespan range)
- Age variance >100 (adequate range for correlation)

*Data Quality:*
- Exactly 100 participants (matching REMEMVR data)
- No duplicate UIDs
- No missing values in any column
- Age distribution adequate for correlation (range >20 years)
- RAVLT scores show normal distribution pattern

*Log Validation:*
- Required patterns: "RAVLT data extracted: 100 participants"
- Required patterns: "Age range: XX-XX years (adequate variance)"
- Required patterns: "RAVLT descriptives: mean=XX.X, sd=XX.X"
- Forbidden patterns: "ERROR", "insufficient variance", "missing"

**Expected Behavior on Validation Failure:**
Raise error with specific data issue, log to logs/step02_extract_ravlt.log, invoke g_debug

### Step 3: Merge Datasets and Compute Correlations

**Dependencies:** Steps 1-2 (both datasets prepared)
**Complexity:** Medium (~10 minutes)

**Purpose:** Merge REMEMVR and RAVLT datasets and compute age correlations with bootstrap confidence intervals

**Input:**
- data/step01_rememvr_theta_data.csv
- data/step02_ravlt_age_data.csv

**Processing:**
- Merge datasets on UID (inner join to ensure matched participants)
- Verify final N=100 participants with complete data
- Compute correlations using scipy.stats.pearsonr:
  - r(Age, RAVLT_Total): Age-RAVLT correlation
  - r(Age, theta_all): Age-REMEMVR correlation
- Extract correlation coefficients, p-values, and 95% CIs
- Bootstrap 95% confidence intervals:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - CI computation: percentile method (2.5th, 97.5th percentiles)
- Multiple comparison correction:
  - Family: Within-RQ (2 correlations)
  - Bonferroni: alpha = 0.05/2 = 0.025 per test
  - Report BOTH uncorrected AND Bonferroni-corrected p-values (Decision D068)
- Effect size: Cohen's r-to-d conversion where applicable

**Output:**
- data/step03_merged_data.csv (complete dataset)
- data/step03_correlations.csv (correlation results with bootstrap CIs)

**Validation Requirement:**
Validation tools MUST be used after correlation computation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_merged_data.csv: 100 rows x 6 columns
- Columns: UID, theta_all, RAVLT_Total, Age, theta_all_z, RAVLT_Total_z
- data/step03_correlations.csv: 2 rows x 8 columns
- Columns: variable_pair, r, p_uncorrected, p_bonferroni, ci_lower, ci_upper, n_bootstrap, interpretation

*Value Ranges:*
- Correlations r in [-1, 1]
- P-values in [0, 1]
- Bootstrap CIs: ci_lower < r < ci_upper
- Age-RAVLT r expected < -0.20 (negative correlation)
- Age-REMEMVR r expected near 0 ± 0.20 (minimal correlation)

*Data Quality:*
- Exactly 100 participants in merged dataset
- No missing values in final dataset
- All correlation values finite and reasonable
- Bootstrap CIs properly computed (1000 iterations completed)
- Both uncorrected and corrected p-values present (Decision D068)

*Log Validation:*
- Required patterns: "Correlations computed: Age-RAVLT r=X.XX, Age-REMEMVR r=X.XX"
- Required patterns: "Bootstrap complete: 1000 iterations"
- Required patterns: "Bonferroni correction applied: alpha=0.025"
- Forbidden patterns: "ERROR", "NaN", "bootstrap failed"

**Expected Behavior on Validation Failure:**
Raise error with correlation computation failure, log to logs/step03_compute_correlations.log, invoke g_debug

### Step 4: Steiger's Z-test for Dependent Correlations

**Dependencies:** Step 3 (correlations computed)
**Complexity:** Medium (~10 minutes)

**Purpose:** Test whether age-related decline differs significantly between RAVLT and REMEMVR using Steiger's Z-test for dependent correlations

**Input:**
- data/step03_correlations.csv
- data/step03_merged_data.csv

**Processing:**
- Extract correlation values: r(Age,RAVLT) and r(Age,REMEMVR)
- Compute correlation between RAVLT and REMEMVR: r(RAVLT,REMEMVR)
- Apply Steiger's Z-test for dependent correlations:
  - Implementation: tools.analysis_ctt.compare_correlations_dependent
  - Formula: Z = (z1 - z2) / sqrt(var(z1-z2)) where z = Fisher's z-transform
  - Random seed: 42 (if any randomized components)
- Compute effect size for correlation difference:
  - Raw difference: |r_RAVLT| - |r_REMEMVR|
  - Standardized difference with pooled standard error
- One-tailed test: H1: |r_RAVLT| > |r_REMEMVR| (directional hypothesis)
- Bootstrap confidence interval for correlation difference:
  - Iterations: 1000
  - Random seed: 42
  - Method: participant-level resampling
  - CI for difference score
- Power analysis:
  - Post-hoc power for observed correlation difference
  - Given: N=100, alpha=0.05 (one-tailed)
  - Calculate: actual power achieved for observed effect size

**Output:**
- data/step04_steiger_test.csv (Z-test results)
- data/step04_effect_sizes.csv (effect size calculations)

**Validation Requirement:**
Validation tools MUST be used after Steiger's test execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_steiger_test.csv: 1 row x 7 columns
- Columns: z_statistic, p_value_one_tailed, r_ravlt, r_rememvr, r_correlation, n_participants, interpretation
- data/step04_effect_sizes.csv: 1 row x 6 columns  
- Columns: correlation_difference, ci_lower, ci_upper, power_achieved, minimum_detectable, effect_size_category

*Value Ranges:*
- Z-statistic: finite numeric value (typically 0-5 range)
- P-value in [0, 1] (one-tailed test)
- Correlation difference in [-2, 2] (difference of correlations)
- Power in [0, 1] (achieved statistical power)

*Data Quality:*
- All test statistics finite and reasonable
- P-value properly computed for one-tailed test
- Bootstrap CI for difference excludes NaN
- Power analysis completed successfully
- Effect size interpretation matches statistical significance

*Log Validation:*
- Required patterns: "Steiger's Z-test: Z=X.XX, p=X.XXX (one-tailed)"
- Required patterns: "Correlation difference: X.XX [CI: X.XX, X.XX]"
- Required patterns: "Power achieved: X.XX for observed effect"
- Forbidden patterns: "ERROR", "convergence failed", "invalid"

**Expected Behavior on Validation Failure:**
Raise error with Steiger test failure, log to logs/step04_steiger_test.log, invoke g_debug

### Step 5: Assumption Checks and Diagnostics

**Dependencies:** Steps 3-4 (correlations and test completed)
**Complexity:** Medium (~10 minutes)

**Purpose:** Check linearity assumptions, identify outliers, and test normality for both correlation relationships

**Input:**
- data/step03_merged_data.csv

**Processing:**
- Linearity assessment via scatterplots:
  - Age vs RAVLT_Total: visual inspection of linear pattern
  - Age vs theta_all: visual inspection of linear pattern
  - Test for non-linear patterns using polynomial regression (quadratic)
- Outlier detection:
  - Standardized residuals: |z| > 3.0 flagged as outliers
  - Cook's distance: D > 4/n = 0.04 for influential points
  - Mahalanobis distance for multivariate outliers
- Normality testing:
  - Shapiro-Wilk test for residuals from each correlation
  - Q-Q plots for visual assessment
  - Alpha = 0.05 threshold for normality assumption
- Homoscedasticity:
  - Visual inspection of residuals vs fitted plots
  - Breusch-Pagan test if regression models fitted
- Remedial actions if assumptions violated:
  - Normality p < 0.05: Report bootstrap CIs as primary (already computed)
  - Non-linearity detected: Report Spearman correlations as sensitivity analysis
  - Outliers present: Report results with and without outliers
  - Document all assumption violations and remedial actions taken

**Output:**
- data/step05_diagnostics.csv (assumption test results)
- data/step05_outliers.csv (flagged outliers with UIDs)

**Validation Requirement:**
Validation tools MUST be used after diagnostic procedures.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_diagnostics.csv: 4 rows x 5 columns
- Rows: linearity_age_ravlt, linearity_age_rememvr, normality_residuals, homoscedasticity
- Columns: assumption, test_statistic, p_value, threshold, status
- data/step05_outliers.csv: variable rows x 4 columns
- Columns: UID, outlier_type, distance_value, threshold

*Value Ranges:*
- Test statistics: finite values appropriate for each test
- P-values in [0, 1]
- Distance values >0 for outlier measures
- Status: "PASS" or "FAIL" for each assumption

*Data Quality:*
- All assumption tests completed
- Outlier detection applied consistently
- Clear documentation of violations
- Remedial actions specified for failures

*Log Validation:*
- Required patterns: "Assumption checks completed: X/4 passed"
- Required patterns: "Outliers detected: X participants"
- Required patterns: "Remedial actions: [specific actions]"
- Forbidden patterns: "ERROR", "test failed to run"

**Expected Behavior on Validation Failure:**
Log diagnostic failures, continue analysis with noted limitations, log to logs/step05_diagnostics.log

### Step 6: Sensitivity Analyses

**Dependencies:** Step 5 (diagnostics completed)
**Complexity:** Medium (~15 minutes)

**Purpose:** Test robustness of findings through outlier exclusion, non-parametric alternatives, and different correlation methods

**Input:**
- data/step03_merged_data.csv
- data/step05_outliers.csv

**Processing:**
- Outlier exclusion analysis:
  - Remove participants flagged as outliers in Step 5
  - Recompute correlations with reduced sample
  - Re-run Steiger's Z-test with outliers excluded
  - Compare results to main analysis
- Non-parametric alternatives:
  - Spearman rank correlations: rs(Age,RAVLT) and rs(Age,REMEMVR)
  - Bootstrap confidence intervals for Spearman correlations
  - Random seed: 42 for bootstrap resampling
  - Iterations: 1000
- Age range sensitivity:
  - Split sample by median age (younger vs older adults)
  - Compute correlations within each age group
  - Test if correlation patterns consistent across age ranges
- Robust correlation methods:
  - Winsorized correlations (5% trim on each end)
  - Compare with Pearson results
- Document consistency across sensitivity analyses:
  - Primary conclusion robust if same pattern across methods
  - Note any method-dependent results

**Output:**
- data/step06_sensitivity_outliers.csv (outlier-excluded results)
- data/step06_sensitivity_spearman.csv (non-parametric correlations)
- data/step06_sensitivity_age_groups.csv (age-stratified results)

**Validation Requirement:**
Validation tools MUST be used after sensitivity analyses.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_sensitivity_outliers.csv: 2 rows x 6 columns (N may be <100)
- data/step06_sensitivity_spearman.csv: 2 rows x 6 columns
- data/step06_sensitivity_age_groups.csv: 4 rows x 7 columns
- All files contain correlation results with confidence intervals

*Value Ranges:*
- All correlation values in [-1, 1]
- Sample sizes reasonable after exclusions (N ≥ 90 expected)
- Spearman correlations similar magnitude to Pearson (robust finding)
- Age group Ns approximately equal (45-55 per group)

*Data Quality:*
- Outlier exclusions properly documented
- Non-parametric alternatives computed correctly
- Age stratification yields balanced groups
- Consistency assessment clearly documented

*Log Validation:*
- Required patterns: "Sensitivity analyses: X/3 methods support main conclusion"
- Required patterns: "Outlier exclusion: N=XX, correlations remain significant"
- Required patterns: "Spearman correlations: rs_RAVLT=X.XX, rs_REMEMVR=X.XX"
- Forbidden patterns: "ERROR", "insufficient data"

**Expected Behavior on Validation Failure:**
Document sensitivity limitations, proceed with available analyses, log to logs/step06_sensitivity.log

### Step 7: Power Analysis and Effect Size Interpretation

**Dependencies:** Steps 4, 6 (main results and sensitivity complete)
**Complexity:** Low (~10 minutes)

**Purpose:** Conduct comprehensive power analysis and provide effect size interpretation for correlation differences

**Input:**
- data/step04_steiger_test.csv
- data/step04_effect_sizes.csv

**Processing:**
- Post-hoc power analysis:
  - Given: N=100, observed correlation difference, alpha=0.05 (one-tailed)
  - Use: correlation difference power formulas or simulation
  - Calculate: actual power achieved for observed effect
  - Random seed: 42 for any simulation-based power calculations
- Sensitivity power analysis:
  - Minimum detectable correlation difference at 80% power
  - Required sample size for 80% power given observed effect
  - Power curves across range of effect sizes
- Effect size interpretation:
  - Raw correlation difference with 95% CI
  - Cohen's conventions adaptation for correlation differences
  - Practical significance assessment for VR scaffolding hypothesis
- Clinical significance evaluation:
  - RAVLT decline magnitude compared to normative expectations
  - REMEMVR age-invariance magnitude relative to measurement error
  - Theoretical implications for scaffolding hypothesis support
- Report limitations:
  - Power limitations if <0.80
  - Confidence interval interpretation
  - Cross-sectional vs longitudinal age effect caveats

**Output:**
- data/step07_power_analysis.csv (comprehensive power calculations)
- data/step07_effect_interpretation.csv (effect size summary)

**Validation Requirement:**
Validation tools MUST be used after power analysis completion.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_power_analysis.csv: 1 row x 6 columns
- Columns: achieved_power, minimum_detectable_difference, required_n_80_power, alpha_level, effect_observed, interpretation
- data/step07_effect_interpretation.csv: 1 row x 8 columns
- Columns: correlation_difference, ci_lower, ci_upper, cohen_category, practical_significance, clinical_relevance, limitation_notes, scaffolding_support

*Value Ranges:*
- Power values in [0, 1]
- Effect sizes appropriate for correlation differences
- Required N reasonable (50-500 range)
- All confidence intervals properly bounded

*Data Quality:*
- Power calculations completed successfully
- Effect size interpretations theoretically grounded
- Limitations honestly acknowledged
- Clinical significance assessment appropriate

*Log Validation:*
- Required patterns: "Power analysis: achieved power = X.XX"
- Required patterns: "Effect interpretation: correlation difference = X.XX"
- Required patterns: "Scaffolding support: [STRONG/MODERATE/WEAK/NONE]"
- Forbidden patterns: "ERROR", "invalid power"

**Expected Behavior on Validation Failure:**
Document power calculation limitations, provide qualitative interpretation, log to logs/step07_power_analysis.log

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)

**Step-by-step data flow:**
- data/step00_dependency_validation.txt: Dependency check results
- data/step01_rememvr_theta_data.csv: REMEMVR theta scores (100 rows x 3 columns)
- data/step02_ravlt_age_data.csv: RAVLT and age data (100 rows x 4 columns)  
- data/step03_merged_data.csv: Combined dataset (100 rows x 6 columns)
- data/step03_correlations.csv: Age correlations with bootstrap CIs (2 rows x 8 columns)
- data/step04_steiger_test.csv: Dependent correlation test results (1 row x 7 columns)
- data/step04_effect_sizes.csv: Effect size calculations (1 row x 6 columns)
- data/step05_diagnostics.csv: Assumption test results (4 rows x 5 columns)
- data/step05_outliers.csv: Flagged outliers (variable rows x 4 columns)
- data/step06_sensitivity_outliers.csv: Outlier-excluded analysis
- data/step06_sensitivity_spearman.csv: Non-parametric correlations  
- data/step06_sensitivity_age_groups.csv: Age-stratified results
- data/step07_power_analysis.csv: Power calculations
- data/step07_effect_interpretation.csv: Effect size summary

### Logs (ONLY execution logs)

- logs/step00_validate_dependencies.log: Dependency validation log
- logs/step01_extract_rememvr.log: REMEMVR data extraction log
- logs/step02_extract_ravlt.log: RAVLT data extraction log  
- logs/step03_compute_correlations.log: Correlation computation log
- logs/step04_steiger_test.log: Steiger's test execution log
- logs/step05_diagnostics.log: Assumption checking log
- logs/step06_sensitivity.log: Sensitivity analysis log
- logs/step07_power_analysis.log: Power analysis log

### Plots (EMPTY until rq_plots runs)

**Plot source CSVs created in data/:**
- data/step03_merged_data.csv: Source for age correlation scatterplots
- data/step06_sensitivity_age_groups.csv: Source for age-stratified plots

### Results (EMPTY until rq_results runs)

**summary.md will be created by rq_results agent**

---

## Expected Data Formats

### Step-to-Step Transformations

**Data Flow:**
1. Raw REMEMVR theta scores (Ch5) → Standardized theta scores (Step 1)
2. Raw RAVLT scores (master.xlsx) → Standardized RAVLT + Age data (Step 2)  
3. Separate datasets → Merged analysis dataset (Step 3)
4. Merged data → Correlation results with bootstrap CIs (Step 3)
5. Correlations → Steiger's test results (Step 4)
6. Merged data → Diagnostic test results (Step 5)
7. Main results + diagnostics → Sensitivity analyses (Step 6)
8. All results → Power analysis and interpretation (Step 7)

### Column Naming Conventions

**Standardized naming:**
- UID: Unique participant identifier (consistent across all files)
- theta_all: Raw REMEMVR theta scores from Ch5
- theta_all_z: Standardized theta scores (z-score)
- RAVLT_Total: Raw RAVLT total score from master.xlsx
- RAVLT_Total_z: Standardized RAVLT scores (z-score)
- Age: Participant age in years
- r: Pearson correlation coefficient
- rs: Spearman rank correlation coefficient
- p_uncorrected: Uncorrected p-value
- p_bonferroni: Bonferroni-corrected p-value (Decision D068)
- ci_lower, ci_upper: 95% confidence interval bounds

### Data Type Constraints

**Required data types:**
- UID: object (string identifier)
- All score variables: float64 (continuous measures)
- All statistical results: float64 (correlation values, p-values, CIs)
- Categorical results: object (interpretation categories)
- No nullable integers (use float64 for numeric with possible missing)

---

## Cross-RQ Dependencies

**Dependency Summary:**
This RQ requires completed Ch5 5.1.1 analysis for REMEMVR theta_all scores. The dependency is DERIVED data from prior RQ execution.

**Critical Path:**
Ch5 5.1.1 (IRT Calibration) → RQ 7.2.4 (VR Scaffolding Validation)

**File Dependencies:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/*theta*.csv  
- Fallback: Search results/ch5/5.1.1/data/ for any theta score file
- Required content: UID and theta_all columns for 100 participants

**Validation Strategy:**
Step 0 validates Ch5 5.1.1 completion and locates theta score file before proceeding with analysis. Multiple path patterns ensure robustness to file naming variations.

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Architecture

**Per-step validation embedded with 4-layer substance criteria:**
- Output Files: Exact paths, dimensions, column specifications
- Value Ranges: Scientific bounds for all variables
- Data Quality: Missing data limits, distribution checks, consistency requirements
- Log Validation: Required success patterns, forbidden error patterns

**Post-execution validation:**
- rq_inspect agent reads this plan and validates each step's outputs against specified criteria
- Validation failures trigger g_debug for immediate troubleshooting
- 100% validation coverage across all 8 analysis steps

### Statistical Implementation Standards

**Reproducibility requirements:**
- Random seed: 42 for ALL randomized procedures (bootstrap, resampling)
- Bootstrap iterations: 1000 (standard for N=100)
- Confidence intervals: 95% using percentile method
- Multiple comparisons: Bonferroni correction with dual reporting (Decision D068)

**Assumption violation remedies:**
- Normality violations: Bootstrap CIs as primary method
- Outlier detection: Cook's D > 0.04, report with/without exclusion
- Non-linearity: Spearman correlations as sensitivity analysis
- Range restriction: Document and acknowledge in limitations

---

## Summary

**Total Steps:** 8 (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** 45-60 minutes  
**Cross-RQ Dependencies:** Ch5 5.1.1 (REMEMVR theta scores)
**Primary Outputs:** Age-correlation comparison via Steiger's Z-test
**Validation Coverage:** 100% (all 8 steps have 4-layer validation requirements)

**Key Hypothesis:** RAVLT should show significant age decline while REMEMVR shows minimal age decline, with significant difference between correlations supporting VR scaffolding hypothesis

**Critical Methodological Notes:**
- Within-subjects design controls for individual differences between RAVLT and REMEMVR
- Steiger's Z-test appropriately handles dependent correlations sharing Age variable
- Bootstrap confidence intervals provide robust effect size estimation
- Multiple sensitivity analyses test robustness to outliers, non-parametric methods, and age stratification
- Power analysis evaluates adequacy of N=100 for detecting meaningful correlation differences

**Expected Pattern (if scaffolding hypothesis confirmed):**
- RAVLT: r(Age) < -0.30, p < 0.05 (traditional age decline)
- REMEMVR: r(Age) ≈ 0, p > 0.10 (age-invariance) 
- Steiger's Z > 2.0, p < 0.05 (significant difference)
- Bootstrap CI for difference excludes 0

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan → creates 3_tools.yaml (specific tool assignments)
3. rq_analysis reads plan + tools → creates 4_analysis.yaml (execution sequence)
4. g_code reads analysis → generates executable Python/R code
5. rq_inspect validates outputs against this plan's substance criteria

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent with v5.1 statistical specifications