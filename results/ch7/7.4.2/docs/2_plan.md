# Analysis Plan: RQ 7.4.2 - BVMT predicts Where more than What

**Research Question:** 7.4.2
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This analysis tests domain-specificity in cognitive test prediction by examining whether BVMT (visuospatial memory test) shows stronger prediction for Where (spatial location) than What (object identity) domains. Uses bivariate correlations with Steiger's Z-test to compare dependent correlations r(BVMT, Where) vs r(BVMT, What) from the same 100 participants.

**Pipeline:** Bivariate Correlation Analysis + Steiger's Z-test
**Steps:** 7 total analysis steps (Step 0: validation + Steps 1-6: analysis)
**Estimated Runtime:** ~45 minutes total

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Chapter-level Bonferroni: alpha = 0.05/28 = 0.00179
- Random seed: 42 for all randomized procedures

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 domain outputs exist before proceeding with analysis

**Input:**
- Primary: results/ch5/5.2.1/data/*theta*.{csv,txt} (Where domain theta scores)
- Alternative: results/ch5/5.2.2/data/*theta*.{csv,txt} (What domain theta scores)
- Fallback: results/ch5/5.2.*/data/step*_theta_scores.csv (domain-specific analysis outputs)
- Expected content: Domain-specific theta scores per participant (UID, theta_mean, domain)
- Cognitive tests: data/cache/master.xlsx (BVMT_TotR column)
- If Ch5 domains not found: QUIT with "Ch5 5.2.x domain outputs not found"

**Processing:**
- Check Ch5 5.2.x completion status in status.yaml files
- Locate domain-specific theta files using wildcard patterns
- Verify files contain required columns: UID, theta values, domain indicators
- Check BVMT_TotR availability in master.xlsx
- Log all validation results with file sizes and column counts

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation summary
- Content: file paths found, row counts, column validation results

*Value Ranges:*
- File sizes > 0 bytes (non-empty files)
- Row counts >= 100 (all participants present)

*Data Quality:*
- All required files located successfully
- Required columns present in each file
- BVMT_TotR column accessible in master.xlsx

*Log Validation:*
- Required patterns: "Ch5 domain files located", "BVMT_TotR found", "VALIDATION - PASS"
- Forbidden patterns: "ERROR", "FAIL", "file not found"

**Expected Behavior on Validation Failure:**
- Raise error with specific missing file
- Log to logs/step00_validate_dependencies.log
- Quit immediately, invoke g_debug

### Step 1: Extract Domain-Specific Theta Scores
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Medium (~8 minutes)

**Purpose:** Extract and prepare Where and What domain-specific theta scores from Ch5 analyses

**Input:**
- Ch5 5.2.x domain analysis outputs (validated in Step 0)
- Expected format: CSV with UID, theta values, domain tags

**Processing:**
- Load domain-specific theta files from Ch5 5.2.x analyses
- Filter for Where domain tags: -L-, -U-, -D- (spatial location subtypes)
- Filter for What domain tags: -N- (object naming/identity)
- Compute mean theta per participant per domain (Where_mean, What_mean)
- Handle missing data: exclude participants with <50% domain coverage
- Standardize UID format for merging (ensure string consistency)
- Quality checks: verify N=100 participants, theta range [-3, 3]

**Output:**
- data/step01_domain_theta_scores.csv (UID, Where_mean, What_mean)

**Validation Requirement:**
Validation tools MUST be used after domain extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_domain_theta_scores.csv: 100 rows x 3 columns
- Columns: UID (object), Where_mean (float64), What_mean (float64)

*Value Ranges:*
- Where_mean in [-3, 3] (IRT theta scale)
- What_mean in [-3, 3] (IRT theta scale)
- Both domains non-missing for all participants

*Data Quality:*
- All 100 participants present (no missing UIDs)
- No duplicate UIDs
- Where_mean and What_mean both non-null
- Standard deviations > 0.1 (adequate variance)

*Log Validation:*
- Required patterns: "Domain extraction complete: 100 participants", "Where domain: N items", "What domain: N items"
- Required patterns: "VALIDATION - PASS"
- Forbidden patterns: "ERROR", "FAIL", "insufficient domain coverage"

**Expected Behavior on Validation Failure:**
- Raise error with specific domain issue
- Log to logs/step01_extract_domains.log
- Quit immediately, invoke g_debug

### Step 2: Extract BVMT Cognitive Test Scores
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Medium (~5 minutes)

**Purpose:** Extract BVMT Total Recall scores from dfnonvr.csv cognitive test data

**Input:**
- data/cache/master.xlsx (BVMT_TotR column)
- Expected format: Excel with UID and BVMT_TotR scores

**Processing:**
- Load master.xlsx and extract BVMT_TotR column
- Standardize UID format to match domain theta file
- Check for missing BVMT scores, exclude if >5% missing
- Verify BVMT score range: typically 0-36 for Total Recall
- Check for outliers: values >3 SD from mean
- Document any range restrictions (floor/ceiling effects)

**Output:**
- data/step02_bvmt_scores.csv (UID, BVMT_TotR)

**Validation Requirement:**
Validation tools MUST be used after BVMT extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_bvmt_scores.csv: 100 rows x 2 columns
- Columns: UID (object), BVMT_TotR (float64 or int64)

*Value Ranges:*
- BVMT_TotR in [0, 36] (valid BVMT Total Recall range)
- No negative values
- Mean approximately 15-25 (healthy adult range)

*Data Quality:*
- All 100 participants present
- No duplicate UIDs
- Missing data < 5% (≤5 participants)
- Standard deviation > 2.0 (adequate variance, no ceiling/floor)

*Log Validation:*
- Required patterns: "BVMT extraction complete: 100 participants", "Score range: [min, max]"
- Required patterns: "VALIDATION - PASS"
- Forbidden patterns: "ERROR", "FAIL", "excessive missing data"

**Expected Behavior on Validation Failure:**
- Raise error with specific BVMT issue
- Log to logs/step02_extract_bvmt.log
- Quit immediately, invoke g_debug

### Step 3: Merge and Prepare Analysis Dataset
**Dependencies:** Steps 1-2 (domain theta + BVMT scores)
**Complexity:** Low (<5 minutes)

**Purpose:** Merge domain theta scores with BVMT scores to create analysis-ready dataset

**Input:**
- data/step01_domain_theta_scores.csv (Where_mean, What_mean)
- data/step02_bvmt_scores.csv (BVMT_TotR)

**Processing:**
- Inner join on UID to create complete analysis dataset
- Verify no participants lost in merge (expect N=100 final)
- Compute descriptive statistics for all variables
- Check for extreme outliers using IQR method (>1.5*IQR)
- Create analysis-ready dataset with standardized variable names
- Document final sample characteristics

**Output:**
- data/step03_analysis_dataset.csv (UID, BVMT_TotR, Where_mean, What_mean)

**Validation Requirement:**
Validation tools MUST be used after dataset merging execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_analysis_dataset.csv: 100 rows x 4 columns
- Columns: UID (object), BVMT_TotR (numeric), Where_mean (float64), What_mean (float64)

*Value Ranges:*
- BVMT_TotR in [0, 36]
- Where_mean in [-3, 3]
- What_mean in [-3, 3]
- All variables within expected ranges

*Data Quality:*
- Exactly 100 participants (no data loss in merge)
- No duplicate UIDs
- No missing values in any analysis variable
- Adequate variance in all variables (SD > threshold)

*Log Validation:*
- Required patterns: "Merge complete: 100 participants retained", "No missing data"
- Required patterns: "VALIDATION - PASS"
- Forbidden patterns: "ERROR", "FAIL", "participants lost in merge"

**Expected Behavior on Validation Failure:**
- Raise error with specific merge issue
- Log to logs/step03_merge_dataset.log
- Quit immediately, invoke g_debug

### Step 4: Compute Bivariate Correlations with Bootstrap CIs
**Dependencies:** Step 3 (analysis dataset)
**Complexity:** Medium (~10 minutes including bootstrap)

**Purpose:** Compute primary correlations r(BVMT, Where) and r(BVMT, What) with robust confidence intervals

**Input:**
- data/step03_analysis_dataset.csv (merged analysis data)

**Processing:**
- Compute Pearson correlations:
  - r1 = cor(BVMT_TotR, Where_mean)
  - r2 = cor(BVMT_TotR, What_mean)
- Bootstrap 95% confidence intervals:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - CI computation: Percentile method (2.5th, 97.5th percentiles)
- Check correlation assumptions:
  - Normality: Shapiro-Wilk test on variables
  - Linearity: Visual inspection of scatter plots
  - Homoscedasticity: Residual variance assessment
- Remedial actions if assumptions violated:
  - Normality p < 0.05: Report bootstrap CIs as primary
  - Non-linearity detected: Document, consider Spearman rank correlation
  - Outliers identified: Compute with/without outliers
- Compute effect size interpretations (Cohen, 1988):
  - Small: r = 0.10, Medium: r = 0.30, Large: r = 0.50

**Output:**
- data/step04_correlations.csv (r1, r2, bootstrap CIs, assumption results)

**Validation Requirement:**
Validation tools MUST be used after correlation computation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_correlations.csv: 2 rows x 8 columns
- Columns: correlation, r, ci_lower, ci_upper, n, p_uncorrected, assumption_check, effect_size

*Value Ranges:*
- r in [-1, 1] (valid correlation range)
- ci_lower < r < ci_upper (valid confidence interval)
- p_uncorrected in [0, 1] (valid p-value)
- n = 100 (full sample)

*Data Quality:*
- Both correlations computed (Where and What)
- Bootstrap CIs non-overlapping with point estimates
- Assumption check results recorded
- Effect size classifications assigned

*Log Validation:*
- Required patterns: "Bootstrap complete: 1000 iterations", "r(BVMT,Where) = X.XX", "r(BVMT,What) = X.XX"
- Required patterns: "Assumption checks complete", "VALIDATION - PASS"
- Forbidden patterns: "ERROR", "FAIL", "bootstrap failed"

**Expected Behavior on Validation Failure:**
- Raise error with specific correlation issue
- Log to logs/step04_compute_correlations.log
- Quit immediately, invoke g_debug

### Step 5: Steiger's Z-test for Dependent Correlations
**Dependencies:** Step 4 (correlation results)
**Complexity:** Medium (~8 minutes)

**Purpose:** Test domain-specificity hypothesis: r(BVMT, Where) > r(BVMT, What) using Steiger's Z-test

**Input:**
- data/step04_correlations.csv (r1, r2 correlation coefficients)
- data/step03_analysis_dataset.csv (raw data for correlation between Where and What)

**Processing:**
- Compute correlation between domains: r_WW = cor(Where_mean, What_mean)
- Steiger's Z-test implementation:
  - H0: r(BVMT, Where) = r(BVMT, What)
  - H1: r(BVMT, Where) > r(BVMT, What) (one-tailed test)
  - Formula: Z = (z1 - z2) / sqrt(2(1-r_WW)/(n-3)) where z = Fisher's Z-transform
- Multiple comparison corrections:
  - Family: Within-RQ comparison (1 primary test)
  - Primary: Chapter-level Bonferroni alpha = 0.05/28 = 0.00179
  - Secondary: FDR correction using Benjamini-Hochberg
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Effect size for correlation difference:
  - Cohen's q = |z1 - z2| (difference in Fisher's Z-transforms)
  - Interpretation: q = 0.10 (small), 0.30 (medium), 0.50 (large)
- Bootstrap validation of Steiger's test:
  - Iterations: 1000, seed: 42
  - Resample participants, recompute Z-statistic
  - Report 95% CI for Z-statistic

**Output:**
- data/step05_steiger_test.csv (Z-statistic, p-values dual reporting, effect sizes)

**Validation Requirement:**
Validation tools MUST be used after Steiger's test execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_steiger_test.csv: 1 row x 9 columns
- Columns: z_statistic, p_uncorrected, p_bonferroni, p_fdr, cohens_q, ci_lower, ci_upper, direction, n

*Value Ranges:*
- z_statistic: real number (can be positive or negative)
- p_uncorrected, p_bonferroni, p_fdr in [0, 1]
- cohens_q >= 0 (absolute difference measure)
- direction: "Where > What" or "What > Where"

*Data Quality:*
- Single test result (1 row)
- All p-values calculated and non-missing
- Bootstrap CI computed successfully
- Direction consistent with z_statistic sign

*Log Validation:*
- Required patterns: "Steiger Z-test complete", "Z = X.XX", "Bootstrap CI: [X.XX, X.XX]"
- Required patterns: "Dual p-values: uncorrected = X.XX, bonferroni = X.XX"
- Required patterns: "VALIDATION - PASS"
- Forbidden patterns: "ERROR", "FAIL", "matrix singular"

**Expected Behavior on Validation Failure:**
- Raise error with specific test issue
- Log to logs/step05_steiger_test.log
- Quit immediately, invoke g_debug

### Step 6: Sensitivity Analysis and Diagnostics
**Dependencies:** Steps 4-5 (correlations + Steiger test)
**Complexity:** Medium (~9 minutes)

**Purpose:** Conduct sensitivity analyses to assess robustness of domain-specificity findings

**Input:**
- data/step03_analysis_dataset.csv (complete dataset)
- data/step05_steiger_test.csv (primary test results)

**Processing:**
- Outlier sensitivity analysis:
  - Identify outliers: standardized residuals > 3.29, Cook's D > 4/n
  - Recompute correlations and Steiger's test excluding outliers
  - Compare results: document effect of outliers on conclusions
- Alternative correlation methods:
  - Spearman rank correlations (non-parametric)
  - Kendall's tau (alternative non-parametric)
  - Compare with Pearson results for consistency
- Range restriction assessment:
  - Check BVMT score distribution for ceiling/floor effects
  - Compute variance ratio tests between domains
  - Apply range restriction corrections if SD < 2.0
- Cross-validation robustness:
  - Implement 5-fold cross-validation, seed: 42
  - Compute correlations in each fold
  - Report mean CV-correlations and standard deviations
  - Flag if CV-correlation gap from full sample > 0.10
- Power analysis validation:
  - Post-hoc power for observed effect sizes
  - Given: N=100, alpha=0.00179 (corrected), observed correlations
  - Report: actual power achieved for detected effects
  - Acknowledge: limitation if power < 0.80

**Output:**
- data/step06_sensitivity_analysis.csv (outlier analysis, alternative methods, power)

**Validation Requirement:**
Validation tools MUST be used after sensitivity analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_sensitivity_analysis.csv: Variable rows x 6 columns
- Sections: outlier_analysis, alternative_methods, range_restriction, cv_results, power_analysis
- Columns: analysis_type, method, result, confidence_interval, n_used, notes

*Value Ranges:*
- All correlation values in [-1, 1]
- Power values in [0, 1]
- CV standard deviations >= 0
- Sample sizes <= 100

*Data Quality:*
- All planned sensitivity analyses completed
- Results documented with effect on conclusions
- Range restriction assessment performed
- Power analysis includes actual achieved power

*Log Validation:*
- Required patterns: "Outlier analysis complete", "CV analysis complete", "Power analysis complete"
- Required patterns: "Sensitivity conclusions documented", "VALIDATION - PASS"
- Forbidden patterns: "ERROR", "FAIL", "analysis incomplete"

**Expected Behavior on Validation Failure:**
- Raise error with specific sensitivity analysis failure
- Log to logs/step06_sensitivity_analysis.log
- Quit immediately, invoke g_debug

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt: Cross-RQ dependency verification
- data/step01_domain_theta_scores.csv: Where and What domain means per participant
- data/step02_bvmt_scores.csv: BVMT Total Recall scores per participant  
- data/step03_analysis_dataset.csv: Merged dataset for analysis
- data/step04_correlations.csv: Bootstrap correlation results with CIs
- data/step05_steiger_test.csv: Dependent correlation comparison results
- data/step06_sensitivity_analysis.csv: Robustness checks and power analysis
- data/step04_correlation_scatterplot_data.csv: Plot source data (Where vs BVMT)
- data/step04_correlation_scatterplot_what_data.csv: Plot source data (What vs BVMT)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log: Dependency validation execution log
- logs/step01_extract_domains.log: Domain extraction execution log
- logs/step02_extract_bvmt.log: BVMT extraction execution log
- logs/step03_merge_dataset.log: Dataset merging execution log
- logs/step04_compute_correlations.log: Correlation computation execution log
- logs/step05_steiger_test.log: Steiger's Z-test execution log
- logs/step06_sensitivity_analysis.log: Sensitivity analysis execution log

### Plots (EMPTY until rq_plots runs)
Note: Plot source CSV files created in data/ during Step 4 for visualization

### Results (EMPTY until rq_results runs)
Note: summary.md will be created by rq_results agent

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 -> Step 1:** Dependency validation provides file paths for domain extraction
**Step 1:** Domain-specific theta scores -> per-participant domain means
**Step 2:** Master.xlsx BVMT column -> standardized BVMT scores  
**Step 3:** Domain means + BVMT -> merged analysis dataset (N=100)
**Step 4:** Analysis dataset -> correlation coefficients with bootstrap CIs
**Step 5:** Correlations -> Steiger's Z-test with dual p-value reporting
**Step 6:** All results -> sensitivity analyses and robustness checks

### Column Naming Conventions

**Standardized columns across steps:**
- UID: Participant identifier (consistent string format)
- Where_mean: Mean theta score for Where domain (spatial location)
- What_mean: Mean theta score for What domain (object identity)
- BVMT_TotR: BVMT Total Recall score (raw score, not T-scored)
- r, ci_lower, ci_upper: Correlation point estimate and 95% confidence interval
- p_uncorrected, p_bonferroni, p_fdr: Dual p-value reporting per Decision D068

### Data Type Constraints

**Required data types:**
- UID: object (string)
- Theta scores: float64 (allows negative values, precise to 3 decimals)
- BVMT scores: numeric (int64 or float64)
- Correlations: float64 (precision to 3 decimals)
- P-values: float64 (full precision for small values)
- Sample sizes: int64 (whole numbers only)

**Nullable vs Non-nullable:**
- UID: Non-nullable (required for all rows)
- Theta scores: Non-nullable after Step 1 processing
- BVMT scores: Non-nullable after Step 2 processing
- Statistical results: Non-nullable (computed values)

---

## Cross-RQ Dependencies

**Source RQ:** Ch5 5.2.x (Domain-specific analyses)

**Required Files:**
- results/ch5/5.2.1/data/*theta*.csv OR results/ch5/5.2.2/data/*theta*.csv
- Pattern variations: step*_theta_scores.csv, domain_theta_summary.csv, theta_estimates.csv
- Content: Domain-specific theta scores with Where (-L-, -U-, -D-) and What (-N-) tags

**Fallback Strategy:**
1. Try results/ch5/5.2.1/data/ and results/ch5/5.2.2/data/ directories
2. Search for files matching *theta*.{csv,txt} pattern
3. Look for step*_theta* files in any Ch5 5.2.x subdirectory
4. If none found: QUIT with clear error message

**Expected Format (regardless of filename):**
- CSV format with UID, theta values, domain indicators
- Minimum 100 participants with Where and What domain coverage
- Theta values in IRT scale range [-3, 3]

**Circuit Breaker:**
If Ch5 domain analyses incomplete or files missing, this RQ cannot proceed. Dependencies must be resolved before rq_tools stage.

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
**Validation Type:** Dependency verification
**Tools Required:** File existence, format validation
**Success Criteria:** All required Ch5 domain files located, BVMT column accessible
**Failure Action:** Quit with specific missing file error

#### Step 1: Domain Extraction  
**Validation Type:** Data extraction verification
**Tools Required:** Range validation, completeness check
**Success Criteria:** 100 participants, theta values in [-3, 3], adequate domain coverage
**Failure Action:** Quit with domain coverage error

#### Step 2: BVMT Extraction
**Validation Type:** Cognitive test data verification  
**Tools Required:** Range validation, missing data assessment
**Success Criteria:** 100 participants, BVMT scores in [0, 36], <5% missing
**Failure Action:** Quit with BVMT data quality error

#### Step 3: Dataset Merge
**Validation Type:** Data integration verification
**Tools Required:** Merge completeness, variable validation
**Success Criteria:** No participants lost, no missing values, all variables within range
**Failure Action:** Quit with merge failure error

#### Step 4: Correlation Computation
**Validation Type:** Statistical computation verification
**Tools Required:** Assumption checking, bootstrap validation
**Success Criteria:** Valid correlations, successful bootstrap, assumptions documented
**Failure Action:** Quit with correlation computation error

#### Step 5: Steiger's Z-test
**Validation Type:** Hypothesis test verification
**Tools Required:** Test statistic validation, dual p-value verification
**Success Criteria:** Valid Z-statistic, both p-values computed, effect size calculated
**Failure Action:** Quit with statistical test error

#### Step 6: Sensitivity Analysis
**Validation Type:** Robustness assessment verification
**Tools Required:** Alternative method validation, power computation
**Success Criteria:** All sensitivity analyses complete, conclusions documented
**Failure Action:** Quit with sensitivity analysis error

---

## Summary

**Total Steps:** 7 (Step 0: validation + Steps 1-6: analysis)
**Estimated Runtime:** ~45 minutes total
**Cross-RQ Dependencies:** Ch5 5.2.x domain-specific theta scores + master.xlsx BVMT
**Primary Outputs:** Correlation coefficients, Steiger's Z-test results, sensitivity analyses
**Validation Coverage:** 100% (all 7 steps have comprehensive validation requirements)

**Key Hypothesis:** r(BVMT, Where) > r(BVMT, What) - Domain-specificity in visuospatial test prediction

**Critical Methodological Notes:**
- Uses Steiger's Z-test (gold standard for dependent correlation comparison)
- Bootstrap validation (1000 iterations, seed=42) provides non-parametric robustness
- Dual p-value reporting per Decision D068 (uncorrected + Bonferroni corrected)
- Comprehensive sensitivity analyses assess outlier influence and alternative methods
- Power analysis documents achievable effect detection with N=100
- Range restriction assessment addresses potential ceiling/floor effects in cognitive tests

**Statistical Implementation Specifications (v5.1 Enhanced):**

**Cross-Validation:**
- 5-fold cross-validation with seed=42, shuffle=True
- Mean CV-correlations compared to full-sample correlations  
- Gap threshold: <0.10 for adequate generalization

**Bootstrap:**
- Participant-level resampling with replacement (preserves correlation structure)
- 1000 iterations with seed=42 for reproducibility
- 95% CI using percentile method (2.5th, 97.5th percentiles)

**Power Analysis:**
- Post-hoc power for observed correlation effect sizes
- Given: N=100, alpha=0.00179 (Chapter-level correction)
- Target: 80% power threshold for adequate detection

**Multiple Comparisons:**
- Family: Within-RQ (1 primary Steiger's test)
- Bonferroni: alpha=0.05/28=0.00179 (Chapter 7 correction)
- FDR: Benjamini-Hochberg alternative correction
- Dual reporting: p_uncorrected, p_bonferroni, p_fdr (Decision D068)

**Assumption Violations:**
- Normality p < 0.05: Use bootstrap CIs as primary inference
- Outliers detected: Report results with/without outliers
- Range restriction: Apply corrections if BVMT SD < 2.0
- Non-linearity: Document, consider Spearman alternative

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml  
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent v5.1 with enhanced statistical specifications