# Analysis Plan: RQ 7.4.3 - RPM Predicts Temporal Integration Performance

**Research Question:** 7.4.3
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This analysis examines whether fluid intelligence (RPM) differentially predicts performance on complex temporal integration items versus simple single-domain items. Uses multiple correlation analysis with Steiger's Z-test to compare dependent correlations between RPM and different complexity levels of episodic memory performance.

**Pipeline:** Multiple Correlation Analysis with Dependent Comparison Testing
**Steps:** 8 total analysis steps (Step 0: dependency validation + Steps 1-7: analysis)
**Estimated Runtime:** ~45 minutes including bootstrap (1000 iterations) and cross-validation

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Multiple comparison correction: Bonferroni alpha = 0.05/2 = 0.025 per correlation test
- Bootstrap confidence intervals: 1000 iterations with seed=42
- Cross-validation: 5-fold with seed=42 for generalization assessment

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 outputs and master.xlsx exist before proceeding with analysis

**Input:**
- Primary: results/ch5/5.2.1/data/step03_theta_scores.csv (What domain theta)
- Alternative: results/ch5/5.2.1/data/*theta*.csv (search pattern)
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv (Overall omnibus theta)  
- Alternative: results/ch5/5.1.1/data/*theta*.csv (search pattern)
- Primary: data/cache/master.xlsx (RPM_Scor column)
- Fallback: data/dfnonvr.csv (alternative location)
- Expected: Ch5 analyses completed (status = success)

**Processing:**
- Check Ch5 5.2.1 and 5.1.1 completion status in status.yaml files
- Locate theta score files using primary paths, fall back to search patterns
- Verify master.xlsx exists and contains RPM_Scor column
- Test file readability and basic format verification
- Log all dependency validation results with PASS/FAIL status

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Expected patterns: "Ch5 5.2.1: FOUND", "Ch5 5.1.1: FOUND", "master.xlsx: FOUND"

*Value Ranges:*
- File sizes: theta files should be >1KB, master.xlsx should be >100KB
- Row counts: theta files should reference ~100 participants

*Data Quality:*
- All required dependencies found and readable
- No critical files missing
- Log entries confirm file accessibility

*Log Validation:*
- Required patterns: "DEPENDENCY CHECK COMPLETE", "ALL DEPENDENCIES: PASS"
- Forbidden patterns: "ERROR", "MISSING", "FAIL", "not found"

**Expected Behavior on Validation Failure:**
Raise error with specific missing dependency, log to logs/step00_dependency_validation.log, quit immediately.

### Step 1: Extract RPM Scores from Master Data
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (~3 minutes)

**Purpose:** Extract Raven's Progressive Matrices scores from dfnonvr.csv for all 100 participants

**Input:**
- data/cache/master.xlsx (primary) or data/dfnonvr.csv (fallback)
- Target column: RPM_Scor 
- Expected format: Participant ID + RPM score

**Processing:**
- Load master.xlsx using pandas.read_excel()
- Extract columns: UID, RPM_Scor
- Check for missing values in RPM_Scor column
- Validate RPM scores are in reasonable range (0-60 for standard RPM)
- Remove participants with missing RPM scores
- Create standardized participant ID format for merging
- Log data extraction summary (N participants, missing data rate)

**Output:**
- data/step01_rpm_scores.csv (columns: UID, RPM_Scor, RPM_standardized)

**Validation Requirement:**
Validation tools MUST be used after RPM extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_rpm_scores.csv: ~100 rows x 3 columns
- Columns: UID (object), RPM_Scor (int64), RPM_standardized (float64)

*Value Ranges:*
- RPM_Scor: [0, 60] (standard RPM range)
- RPM_standardized: approximately [-3, 3] (z-scores)
- No negative raw scores

*Data Quality:*
- All participant UIDs present (expected N ~95-100)
- No missing values in RPM_Scor after cleaning
- No duplicate UIDs
- RPM scores within plausible range

*Log Validation:*
- Required patterns: "RPM extraction complete", "N participants: [90-100]"
- Required patterns: "Missing RPM scores: [0-5]"
- Forbidden patterns: "ERROR", "invalid range", "duplicate"

**Expected Behavior on Validation Failure:**
Raise error with specific data quality issue, log to logs/step01_rpm_extraction.log, invoke g_debug for data inspection.

### Step 2: Extract Overall Theta Scores (Complex Integration)
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (~3 minutes)

**Purpose:** Extract overall omnibus theta scores representing complex integration performance requiring What+Where+When

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/*theta*.csv (search pattern)
- Expected format: UID + theta estimate + standard error

**Processing:**
- Load overall theta scores from Ch5 5.1.1 omnibus analysis
- Extract columns: UID, theta, SE (or equivalent column names)
- Standardize participant ID format for merging consistency
- Check for missing theta estimates and exclude if necessary
- Validate theta values are in IRT-appropriate range (-4 to +4)
- Log theta extraction summary (N participants, range, missing rate)

**Output:**
- data/step02_overall_theta.csv (columns: UID, theta_overall, se_overall)

**Validation Requirement:**
Validation tools MUST be used after theta extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_overall_theta.csv: ~100 rows x 3 columns  
- Columns: UID (object), theta_overall (float64), se_overall (float64)

*Value Ranges:*
- theta_overall: [-4, 4] (IRT theta scale)
- se_overall: [0.1, 2.0] (positive standard errors)

*Data Quality:*
- All participant UIDs match Step 1 format
- No missing values in theta_overall
- Standard errors all positive
- Theta estimates in plausible IRT range

*Log Validation:*
- Required patterns: "Overall theta extraction complete", "Theta range: [-X.X, X.X]"
- Required patterns: "N participants with valid theta: [90-100]"
- Forbidden patterns: "ERROR", "invalid theta", "missing theta"

**Expected Behavior on Validation Failure:**
Raise error with theta range or missing data issue, log to logs/step02_overall_theta.log, invoke g_debug.

### Step 3: Extract What-Only Theta Scores (Simple Single-Domain)
**Dependencies:** Step 0 (dependency validation)  
**Complexity:** Low (~3 minutes)

**Purpose:** Extract What-domain theta scores representing simple single-domain object identification performance

**Input:**
- Primary: results/ch5/5.2.1/data/step03_theta_scores.csv  
- Alternative: results/ch5/5.2.1/data/*theta*.csv (search pattern)
- Expected format: What domain theta estimates from -N- tagged items

**Processing:**
- Load What domain theta scores from Ch5 5.2.1 analysis
- Extract columns: UID, theta, SE (What domain specific)
- Standardize participant ID format for merging consistency
- Check for missing What theta estimates and exclude if necessary  
- Validate What theta values are in IRT-appropriate range (-4 to +4)
- Compare N participants to overall theta to ensure matching sample
- Log What theta extraction summary (N participants, range, missing rate)

**Output:**
- data/step03_what_theta.csv (columns: UID, theta_what, se_what)

**Validation Requirement:**
Validation tools MUST be used after What theta extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_what_theta.csv: ~100 rows x 3 columns
- Columns: UID (object), theta_what (float64), se_what (float64)

*Value Ranges:*
- theta_what: [-4, 4] (IRT theta scale)
- se_what: [0.1, 2.0] (positive standard errors)

*Data Quality:*
- Participant UIDs match Steps 1-2 format
- N participants matches overall theta (within 5 participants)
- No missing values in theta_what
- Standard errors all positive

*Log Validation:*
- Required patterns: "What theta extraction complete", "N participants match: [YES/NO]"
- Required patterns: "What theta range: [-X.X, X.X]"
- Forbidden patterns: "ERROR", "mismatch", "missing what"

**Expected Behavior on Validation Failure:**
Raise error with What theta issue or sample mismatch, log to logs/step03_what_theta.log, invoke g_debug.

### Step 4: Merge Data and Compute Correlations
**Dependencies:** Steps 1-3 (all data extraction steps)
**Complexity:** Medium (~8 minutes including bootstrap)

**Purpose:** Merge all data sources and compute correlations between RPM and both complexity levels with bootstrap confidence intervals

**Input:**
- data/step01_rpm_scores.csv (RPM data)
- data/step02_overall_theta.csv (complex integration performance)
- data/step03_what_theta.csv (simple single-domain performance)

**Processing:**
- Merge all datasets on UID using inner join to keep complete cases only
- Check final sample size (should be ~90-95 participants with complete data)
- Compute correlations with bootstrap confidence intervals:
  - r1 = correlation(RPM_Scor, theta_overall) - complex integration
  - r2 = correlation(RPM_Scor, theta_what) - simple single-domain
- Bootstrap specifications:
  - Iterations: 1000
  - Random seed: 42 for reproducibility  
  - Method: Participant-level resampling with replacement
  - CI computation: percentile method (2.5th, 97.5th percentiles for 95% CI)
- Multiple comparison correction:
  - Family: Within-RQ (2 correlation tests)
  - Bonferroni: alpha = 0.05/2 = 0.025 per test
  - Also compute FDR using Benjamini-Hochberg
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Cross-validation assessment:
  - Implement 5-fold cross-validation using sklearn.model_selection.KFold
  - Random seed: 42 for reproducibility
  - For each fold: compute correlations on training set, test on held-out set  
  - Assess generalization gap: |train_r - test_r| should be <0.15 for correlations
- Extract correlation statistics: r, p_uncorrected, p_bonferroni, p_fdr, CI_lower, CI_upper

**Output:**
- data/step04_correlation_results.csv (correlation statistics with dual p-values)

**Validation Requirement:**
Validation tools MUST be used after correlation computation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_correlation_results.csv: 2 rows x 8 columns
- Columns: correlation_type, r, p_uncorrected, p_bonferroni, p_fdr, ci_lower, ci_upper, n_participants

*Value Ranges:*
- r: [-1, 1] (valid correlation range)
- p-values: [0, 1] (valid probability range)
- ci_lower < r < ci_upper (valid confidence intervals)
- n_participants: [85, 100] (reasonable complete case sample)

*Data Quality:*
- Both correlations computed (complex and simple)
- Bootstrap CIs valid (lower < point estimate < upper)
- All p-values present (uncorrected, Bonferroni, FDR per Decision D068)
- No NaN values in results

*Log Validation:*
- Required patterns: "Correlations computed successfully", "Bootstrap complete: 1000 iterations"
- Required patterns: "Final N with complete data: [85-100]"
- Required patterns: "Cross-validation gap: <0.15"
- Forbidden patterns: "ERROR", "convergence", "invalid correlation"

**Expected Behavior on Validation Failure:**
Raise error with specific correlation issue, log to logs/step04_correlations.log, invoke g_debug for data inspection.

### Step 5: Test Differential Prediction with Steiger's Z-test
**Dependencies:** Step 4 (correlation results)
**Complexity:** Medium (~5 minutes)

**Purpose:** Test whether RPM shows differential prediction for complex vs simple episodic memory performance using Steiger's Z-test

**Input:**
- data/step04_correlation_results.csv (r1, r2, sample size)
- Extracted values: r1 (RPM-overall), r2 (RPM-what), N (complete cases)

**Processing:**
- Extract correlation coefficients for Steiger's test:
  - r12 = correlation(theta_overall, theta_what) - shared variance between outcomes
  - r1y = correlation(RPM, theta_overall) - complex integration prediction
  - r2y = correlation(RPM, theta_what) - simple domain prediction
- Implement Steiger's Z-test for dependent correlations:
  - Use formula for correlations sharing common variable (RPM as predictor)
  - Test H0: r1y = r2y vs H1: r1y ≠ r2y (two-tailed test)
  - Implementation: tools.analysis_extensions.compare_correlations_dependent()
  - Random seed: 42 if any randomization involved
- Multiple comparison correction:
  - Family: Within-RQ differential prediction test (1 comparison)
  - No correction needed for single comparison
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Effect size computation:
  - Cohen's q for correlation difference: q = 0.5 * log((1+r1)/(1-r1)) - 0.5 * log((1+r2)/(1-r2))
  - Interpretation: small q = 0.10, medium q = 0.30, large q = 0.50
- Bootstrap confidence interval for correlation difference:
  - Iterations: 1000
  - Seed: 42
  - Method: Bootstrap both correlations, compute difference distribution
  - CI: percentile method for difference distribution

**Output:**
- data/step05_steiger_test.csv (Z-statistic, p-values, effect size, CI for difference)

**Validation Requirement:**
Validation tools MUST be used after Steiger's test execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_steiger_test.csv: 1 row x 8 columns
- Columns: z_statistic, p_uncorrected, p_bonferroni, p_fdr, cohens_q, diff_ci_lower, diff_ci_upper, n_participants

*Value Ranges:*
- z_statistic: typical range [-5, 5] (test statistic)
- p_values: [0, 1] (valid probabilities)  
- cohens_q: typical range [-1, 1] (effect size for correlation difference)
- CI bounds: should bracket Cohen's q value

*Data Quality:*
- Z-statistic finite and non-NaN
- Confidence interval valid (lower < point estimate < upper)
- All p-values present (Decision D068 compliance)
- Effect size interpretable and reasonable

*Log Validation:*
- Required patterns: "Steiger test complete", "Z = X.XX, p = X.XXX"
- Required patterns: "Effect size (Cohen's q) = X.XX"
- Required patterns: "Bootstrap difference CI computed"
- Forbidden patterns: "ERROR", "undefined", "infinite Z"

**Expected Behavior on Validation Failure:**
Raise error with Steiger test computation issue, log to logs/step05_steiger_test.log, invoke g_debug.

### Step 6: Check Statistical Assumptions and Diagnostics
**Dependencies:** Step 4 (merged data and correlations)
**Complexity:** Medium (~8 minutes including tests)

**Purpose:** Validate assumptions for correlation analysis and identify potential outliers or violations

**Input:**
- Data from Step 4 merge: RPM_Scor, theta_overall, theta_what
- Expected: Complete cases dataset for assumption checking

**Processing:**
- Check correlation analysis assumptions:
  - Normality: Shapiro-Wilk test for each variable (alpha = 0.05)
  - Bivariate normality: Visual inspection via Q-Q plots, consider Henze-Zirkler test
  - Linearity: Scatterplot inspection with lowess curves
  - Homoscedasticity: Residual plots for heteroscedasticity assessment
  - Independence: Confirmed by study design (between-participants)
- Outlier detection:
  - Mahalanobis distance for multivariate outliers (p < 0.001)
  - Univariate outliers: |z-score| > 3.29 (p < 0.001, two-tailed)
  - Influential points: leverage values > 2k/n where k = number of variables
- Remedial actions if assumptions violated:
  - Normality p < 0.05: Report bootstrap CIs as primary (already computed)
  - Severe non-normality: Consider Spearman rank correlations as backup
  - Outliers identified: Report results with and without outliers
  - Linearity violations: Consider polynomial or robust correlation methods
- Power analysis:
  - Post-hoc power for observed correlation difference
  - Given: N = [actual N], alpha = 0.05, observed effect size
  - Use: statsmodels.stats.power or manual calculation
  - Report: actual power for detecting observed difference

**Output:**
- data/step06_assumption_checks.csv (test results, outlier flags, remedial actions)

**Validation Requirement:**
Validation tools MUST be used after assumption checking execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_assumption_checks.csv: variable-specific test results
- Expected columns: variable, normality_p, outlier_count, assumption_met, remedial_action

*Value Ranges:*
- normality_p: [0, 1] (Shapiro-Wilk p-values)
- outlier_count: [0, 10] (reasonable outlier range)
- assumption_met: TRUE/FALSE (logical)

*Data Quality:*
- All variables tested for normality
- Outlier detection completed
- Remedial actions specified for any violations
- Power analysis completed with reasonable values

*Log Validation:*
- Required patterns: "Assumption checks complete", "Outliers detected: [0-10]"
- Required patterns: "Normality tests: [variable] p = X.XXX"
- Required patterns: "Power analysis: power = X.XX"
- Forbidden patterns: "ERROR", "test failed", "unable to compute"

**Expected Behavior on Validation Failure:**
Raise error with assumption checking issue, log to logs/step06_assumptions.log, invoke g_debug.

### Step 7: Sensitivity Analyses and Robustness Checks  
**Dependencies:** Steps 5-6 (Steiger test and assumptions)
**Complexity:** High (~12 minutes)

**Purpose:** Conduct sensitivity analyses to assess robustness of differential prediction findings

**Input:**
- data/step04_correlation_results.csv (primary correlation results)
- data/step06_assumption_checks.csv (outlier flags, assumption violations)
- Complete case dataset: RPM_Scor, theta_overall, theta_what

**Processing:**
- Sensitivity Analysis 1: Outlier exclusion
  - Remove identified outliers from Step 6
  - Recompute correlations and Steiger's test
  - Compare results to main analysis
  - Assess robustness: |difference| < 0.10 considered robust
- Sensitivity Analysis 2: Robust correlation methods
  - Compute Spearman rank correlations as alternative
  - Test differential prediction using Spearman coefficients
  - Compare rank-based vs Pearson results
- Sensitivity Analysis 3: Alternative integration definition
  - If available: Use When domain theta as alternative temporal integration measure
  - Compare r(RPM, When_theta) vs r(RPM, What_theta)
  - Assess consistency of differential prediction pattern
- Cross-validation robustness:
  - 5-fold CV correlation stability across folds
  - Random seed: 42 for reproducible splits
  - Compute correlation difference stability across folds
  - Flag if CV standard deviation > 0.15 (unstable pattern)
- Bootstrap stability assessment:
  - Additional bootstrap with different seed (seed = 123) for stability
  - Compare CI overlap between seed=42 and seed=123 bootstrap runs
  - Assess bootstrap stability: >90% CI overlap expected
- Statistical power sensitivity:
  - Power curves for range of effect sizes
  - Minimum detectable effect given N and alpha
  - Assessment of whether study adequately powered for observed effects

**Output:**
- data/step07_sensitivity_analyses.csv (robustness test results across methods)

**Validation Requirement:**
Validation tools MUST be used after sensitivity analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_sensitivity_analyses.csv: multiple rows for different sensitivity tests
- Expected columns: sensitivity_test, correlation_difference, p_value, robust_result, interpretation

*Value Ranges:*
- correlation_difference: reasonable range [-0.5, 0.5] for robustness
- p_value: [0, 1] for all sensitivity tests
- robust_result: TRUE/FALSE for robustness assessment

*Data Quality:*
- All planned sensitivity analyses completed
- Robustness assessments provided for each test
- Consistent pattern interpretation across methods
- Cross-validation stability metrics within acceptable ranges

*Log Validation:*
- Required patterns: "Sensitivity analyses complete", "Outlier exclusion: N=[X] removed"
- Required patterns: "Robustness assessment: [ROBUST/NOT ROBUST]"
- Required patterns: "Cross-validation stability: SD = X.XX"
- Forbidden patterns: "ERROR", "sensitivity failed", "unable to assess"

**Expected Behavior on Validation Failure:**
Raise error with sensitivity analysis issue, log to logs/step07_sensitivity.log, invoke g_debug.

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (dependency check results)
- data/step01_rpm_scores.csv (RPM extracted from dfnonvr.csv)
- data/step02_overall_theta.csv (complex integration theta scores)
- data/step03_what_theta.csv (simple single-domain theta scores) 
- data/step04_correlation_results.csv (correlations with bootstrap CIs and dual p-values)
- data/step05_steiger_test.csv (differential prediction test results)
- data/step06_assumption_checks.csv (assumption validation and outlier detection)
- data/step07_sensitivity_analyses.csv (robustness checks across multiple methods)

### Logs (ONLY execution logs)
- logs/step00_dependency_validation.log
- logs/step01_rpm_extraction.log  
- logs/step02_overall_theta.log
- logs/step03_what_theta.log
- logs/step04_correlations.log
- logs/step05_steiger_test.log
- logs/step06_assumptions.log
- logs/step07_sensitivity.log

### Plots (EMPTY until rq_plots runs)
Note: Plot source CSVs created in data/ folder by analysis steps

### Results (EMPTY until rq_results runs)
Note: summary.md will be created by rq_results agent

---

## Expected Data Formats

### Step-to-Step Transformations
1. **Step 1 -> Step 4:** RPM_Scor (raw) -> RPM_standardized (z-score) for correlation analysis
2. **Steps 2,3 -> Step 4:** Domain-specific theta -> merged complete cases dataset
3. **Step 4 -> Step 5:** Individual correlations -> correlation difference for Steiger's test  
4. **Step 5 -> Step 6:** Correlation results -> assumption checking on underlying variables
5. **Step 6 -> Step 7:** Assumption results -> inform sensitivity analysis approaches

### Column Naming Conventions  
- **Participant ID:** UID (consistent across all files)
- **RPM variables:** RPM_Scor (raw), RPM_standardized (z-score)
- **Theta variables:** theta_overall, theta_what, se_overall, se_what
- **Statistics:** r, p_uncorrected, p_bonferroni, p_fdr, ci_lower, ci_upper, n_participants

### Data Type Constraints
- **UID:** object (string) - not nullable
- **RPM scores:** int64 (raw), float64 (standardized) - range [0,60] raw, [-3,3] standardized  
- **Theta estimates:** float64 - range [-4,4], not nullable after complete cases
- **Standard errors:** float64 - range [0.1,2.0], positive values only
- **Correlations:** float64 - range [-1,1], finite values only
- **P-values:** float64 - range [0,1], finite values only

---

## Cross-RQ Dependencies

**Source RQs Required:**
- **Ch5 5.1.1:** Overall omnibus theta scores (complex integration measure)
- **Ch5 5.2.1:** What domain theta scores (simple single-domain measure)

**File Dependencies:**
- **Primary paths:** results/ch5/5.1.1/data/step03_theta_scores.csv, results/ch5/5.2.1/data/step03_theta_scores.csv
- **Alternative paths:** results/ch5/5.X.X/data/*theta*.csv (search patterns)
- **Fallback strategy:** If exact files not found, search for any theta score files in Ch5 directories
- **Critical requirement:** Both overall and What domain theta estimates needed for analysis
- **Circuit breaker:** If Ch5 analyses not complete, QUIT with dependency error

**Master Data Dependencies:**
- **File:** data/cache/master.xlsx or data/dfnonvr.csv
- **Column:** RPM_Scor (Raven's Progressive Matrices scores)
- **Format:** Numeric scores in reasonable range (0-60)
- **Requirement:** Must be accessible and contain RPM data for >90 participants

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
**Validation Type:** File existence and accessibility check
**4-Layer Requirements:** Documented above in Step 0 specification

#### Step 1: Extract RPM Scores  
**Validation Type:** Data extraction and range validation
**4-Layer Requirements:** Documented above in Step 1 specification

#### Step 2: Extract Overall Theta
**Validation Type:** IRT theta range and format validation
**4-Layer Requirements:** Documented above in Step 2 specification

#### Step 3: Extract What Theta
**Validation Type:** Domain-specific theta validation and sample matching
**4-Layer Requirements:** Documented above in Step 3 specification

#### Step 4: Compute Correlations
**Validation Type:** Statistical computation validation with bootstrap verification
**4-Layer Requirements:** Documented above in Step 4 specification

#### Step 5: Steiger's Z-test
**Validation Type:** Dependent correlation comparison test validation
**4-Layer Requirements:** Documented above in Step 5 specification

#### Step 6: Assumption Checks
**Validation Type:** Statistical assumption and diagnostic validation
**4-Layer Requirements:** Documented above in Step 6 specification

#### Step 7: Sensitivity Analyses
**Validation Type:** Robustness assessment and stability validation
**4-Layer Requirements:** Documented above in Step 7 specification

---

## Summary

**Total Steps:** 8 (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** ~45 minutes
**Cross-RQ Dependencies:** Ch5 5.1.1 (overall theta), Ch5 5.2.1 (What theta), master.xlsx (RPM)
**Primary Outputs:** Correlation comparison with differential prediction test, bootstrap CIs, sensitivity analyses
**Validation Coverage:** 100% (all 8 steps have 4-layer validation requirements)

**Key Hypothesis:** RPM should predict complex integration (overall theta) more strongly than simple single-domain (What theta) performance, tested via Steiger's Z-test for dependent correlations.

**Critical Methodological Notes:**
- Uses dependent correlation comparison (appropriate for shared predictor design)
- Bootstrap confidence intervals (1000 iterations, seed=42) for robust inference
- Decision D068 compliance: dual p-value reporting (uncorrected + corrected)
- Comprehensive sensitivity analyses to assess robustness across methods
- Cross-validation assessment for generalization evaluation
- All randomized procedures use seed=42 for reproducibility

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml  
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent