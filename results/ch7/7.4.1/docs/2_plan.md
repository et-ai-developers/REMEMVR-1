# Analysis Plan: RQ 7.4.1 - RAVLT Free Recall > Recognition Process-Specificity

**Research Question:** 7.4.1
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ tests process-specific transfer between RAVLT (verbal free recall) and REMEMVR paradigms, examining whether RAVLT shows stronger correlation with VR Free Recall than Recognition, consistent with Transfer-Appropriate Processing theory. The analysis uses bivariate correlations with Steiger's Z-test for dependent correlation comparison.

**Pipeline:** Bivariate Correlation Analysis with Dependent Correlation Testing
**Steps:** 6 total analysis steps (Step 0: validation + Steps 1-5: analysis)
**Estimated Runtime:** ~45 minutes total

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Chapter-level Bonferroni correction: alpha = 0.05/28 = 0.00179
- Process-specificity hypothesis: r(RAVLT, FreeRecall) > r(RAVLT, Recognition)

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 paradigm outputs exist before proceeding

**Input:**
- Primary: results/ch5/5.3.1/status.yaml (verify rq_results: success)
- Alternative: results/ch5/5.3.2/status.yaml or results/ch5/5.3.3/status.yaml
- Fallback: results/ch5/5.3.*/status.yaml (any paradigm analysis)
- Expected: theta scores separated by Free Recall vs Recognition paradigms
- Secondary: data/cache/master.xlsx (RAVLT cognitive test scores)

**Processing:**
- Check at least one Ch5 5.3.x RQ completed successfully
- Verify paradigm-specific theta files exist in data/ folder
- Try multiple file patterns: *theta*, *paradigm*, *IFR*, *IRE*
- Locate RAVLT_Total scores in master.xlsx
- Log all validation checks with specific file paths found

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Content: file paths found, success/failure status for each dependency

*Value Ranges:*
- N/A (validation log only)

*Data Quality:*
- All required dependencies successfully located
- No broken file paths
- Master.xlsx accessible

*Log Validation:*
- Required: "Dependency validation COMPLETE"
- Required: "Ch5 paradigm data FOUND"
- Required: "RAVLT data ACCESSIBLE"
- Forbidden: "ERROR", "MISSING", "FAILED"

**Expected Behavior on Validation Failure:**
- Raise error with specific missing dependency
- Log to logs/step00_validate_dependencies.log
- Quit immediately with descriptive message

### Step 1: Extract and Prepare Cognitive Test Data
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (~5 minutes)

**Purpose:** Extract RAVLT Total scores and basic descriptive statistics from master.xlsx

**Input:**
- data/cache/master.xlsx (RAVLT cognitive assessment data)
- Expected columns: UID, RAVLT_Total (raw scores, not T-scored)

**Processing:**
- Read master.xlsx sheet with cognitive test data
- Extract UID and RAVLT_Total columns for all 100 participants
- Convert RAVLT_Total to numeric, handling any missing values
- Compute descriptive statistics (mean, std, min, max, skew, kurtosis)
- Check for restriction of range (variance adequacy)
- Document missing data patterns and participant exclusions
- Test normality using Shapiro-Wilk test (alpha = 0.05)
- Flag potential outliers using z-score threshold |z| > 3.0

**Output:**
- data/step01_ravlt_scores.csv (UID, RAVLT_Total, z_score, outlier_flag)
- data/step01_ravlt_descriptives.txt (summary statistics)

**Validation Requirement:**
Validation tools MUST be used after cognitive test extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_ravlt_scores.csv: 100 rows x 4 columns (UID, RAVLT_Total, z_score, outlier_flag)
- data/step01_ravlt_descriptives.txt: text file with summary statistics
- Data types: UID (object), RAVLT_Total (float64), z_score (float64), outlier_flag (bool)

*Value Ranges:*
- RAVLT_Total in [20, 75] (typical range for healthy adults)
- z_score in [-4, 4] (standardized scores)
- Missing data < 5% (95+ participants with valid RAVLT)

*Data Quality:*
- All 100 participant UIDs present
- No duplicate UIDs
- RAVLT_Total values non-negative and realistic
- Outlier flags consistent with |z| > 3.0 threshold

*Log Validation:*
- Required: "RAVLT extraction complete: N=XX participants"
- Required: "Normality test: Shapiro-Wilk p=X.XXX"
- Required: "Outliers detected: X participants"
- Forbidden: "ERROR", "missing RAVLT", "conversion failed"

**Expected Behavior on Validation Failure:**
- Raise error with specific data quality issue
- Log to logs/step01_extract_ravlt.log
- Quit immediately, invoke g_debug

### Step 2: Extract Paradigm-Specific Theta Scores
**Dependencies:** Steps 0-1 (validation + RAVLT data)
**Complexity:** Medium (~10 minutes including file discovery)

**Purpose:** Extract mean theta scores per participant for Free Recall and Recognition paradigms from Ch5 outputs

**Input:**
- Primary: results/ch5/5.3.1/data/*theta*paradigm*.csv
- Alternative: results/ch5/5.3.2/data/step03_theta_scores.csv
- Fallback: results/ch5/5.3.*/data/*theta*.csv (search all 5.3.x outputs)
- Expected content: UID, paradigm, theta scores (Free Recall/IFR vs Recognition/IRE)

**Processing:**
- Search for paradigm-specific theta files using file patterns
- Load theta data with UID, paradigm, and theta columns
- Filter for Free Recall (IFR) and Recognition (IRE) paradigms only
- Exclude Cued Recall paradigm (intermediate process complexity)
- Compute mean theta per participant for each paradigm across all tests/items
- Verify all 100 participants have both Free Recall and Recognition theta values
- Test normality for both theta distributions using Shapiro-Wilk (alpha = 0.05)
- Check for outliers using |z| > 3.0 threshold
- Document missing data patterns by paradigm

**Output:**
- data/step02_paradigm_theta.csv (UID, theta_FreeRecall, theta_Recognition, both_available)
- data/step02_theta_descriptives.txt (summary by paradigm)

**Validation Requirement:**
Validation tools MUST be used after paradigm theta extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_paradigm_theta.csv: 100 rows x 4 columns (UID, theta_FreeRecall, theta_Recognition, both_available)
- data/step02_theta_descriptives.txt: text file with descriptive statistics by paradigm
- Data types: UID (object), theta scores (float64), both_available (bool)

*Value Ranges:*
- theta_FreeRecall in [-3, 3] (IRT ability scale)
- theta_Recognition in [-3, 3] (IRT ability scale)
- both_available = True for >=95% of participants

*Data Quality:*
- All 100 participant UIDs present
- No duplicate UIDs
- Theta values within reasonable IRT bounds
- Missing paradigm data < 5% per participant

*Log Validation:*
- Required: "Paradigm theta extraction complete: N=XX participants"
- Required: "Free Recall theta: mean=X.XX, std=X.XX"
- Required: "Recognition theta: mean=X.XX, std=X.XX"
- Required: "Both paradigms available: XX participants"
- Forbidden: "ERROR", "paradigm not found", "empty theta"

**Expected Behavior on Validation Failure:**
- Raise error with specific paradigm data issue
- Log to logs/step02_extract_theta.log
- Quit immediately, invoke g_debug

### Step 3: Create Analysis Dataset and Test Assumptions
**Dependencies:** Steps 1-2 (RAVLT + theta data)
**Complexity:** Low (~5 minutes)

**Purpose:** Merge RAVLT and theta data, test correlation assumptions

**Input:**
- data/step01_ravlt_scores.csv (RAVLT Total scores)
- data/step02_paradigm_theta.csv (paradigm-specific theta scores)

**Processing:**
- Merge datasets on UID using inner join (complete cases only)
- Create analysis dataset with RAVLT_Total, theta_FreeRecall, theta_Recognition
- Document final sample size after complete case analysis
- Test statistical assumptions for correlation analysis:
  - Normality: Shapiro-Wilk tests for all 3 variables (alpha = 0.05)
  - Linearity: Scatter plot inspection and correlation with squared terms
  - Independence: Verify participant-level data (design assumption)
  - Range restriction: Check variance adequacy for all variables
- Flag assumption violations for remedial actions
- Identify outliers using standardized residuals |z| > 3.0

**Output:**
- data/step03_analysis_dataset.csv (UID, RAVLT_Total, theta_FreeRecall, theta_Recognition)
- data/step03_assumption_tests.txt (assumption test results)

**Validation Requirement:**
Validation tools MUST be used after dataset creation and assumption testing.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_analysis_dataset.csv: >=95 rows x 4 columns
- data/step03_assumption_tests.txt: text file with assumption test results
- Data types: UID (object), all scores (float64)

*Value Ranges:*
- RAVLT_Total in [20, 75]
- theta_FreeRecall in [-3, 3]
- theta_Recognition in [-3, 3]
- Final N >= 95 participants (5% missing data tolerance)

*Data Quality:*
- No missing values in analysis dataset (complete cases only)
- No duplicate UIDs
- All values within expected ranges
- Assumption test results clearly documented

*Log Validation:*
- Required: "Analysis dataset created: N=XX participants"
- Required: "Normality tests complete: RAVLT p=X.XXX, FreeRecall p=X.XXX, Recognition p=X.XXX"
- Required: "Linearity assessment complete"
- Required: "Outlier detection: X participants flagged"
- Forbidden: "ERROR", "merge failed", "empty dataset"

**Expected Behavior on Validation Failure:**
- Raise error with specific dataset issue
- Log to logs/step03_create_dataset.log
- Quit immediately, invoke g_debug

### Step 4: Compute Correlations and Steiger's Z-Test
**Dependencies:** Steps 1-3 (complete analysis dataset)
**Complexity:** Medium (~15 minutes including bootstrap)

**Purpose:** Compute bivariate correlations and test process-specificity hypothesis using Steiger's Z-test for dependent correlations

**Input:**
- data/step03_analysis_dataset.csv (RAVLT and paradigm theta scores)
- data/step03_assumption_tests.txt (assumption test results for method selection)

**Processing:**
- Select correlation method based on normality tests:
  - If all variables normal (p > 0.05): Use Pearson correlations
  - If any variable non-normal (p <= 0.05): Use Spearman correlations
- Compute r1 = cor(RAVLT_Total, theta_FreeRecall)
- Compute r2 = cor(RAVLT_Total, theta_Recognition)
- Calculate 95% confidence intervals for both correlations using Fisher transformation
- Perform Steiger's Z-test for dependent correlations:
  - H0: r1 = r2 (no difference in correlations)
  - H1: r1 > r2 (Free Recall correlation stronger)
  - Use one-tailed test for directional hypothesis
- Apply multiple comparison correction:
  - Family: Chapter-level (28 RQs in Ch7)
  - Bonferroni: alpha = 0.05/28 = 0.00179 per test
  - Also compute FDR using Benjamini-Hochberg
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Compute effect size: r1 - r2 (correlation difference)
- Bootstrap confidence intervals for correlation difference:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - CI: Percentile method (2.5th, 97.5th percentiles)
  - Assess whether bootstrap CI excludes zero

**Output:**
- data/step04_correlations.csv (r1, r2, CIs, p-values, Steiger Z-test results)
- data/step04_bootstrap_results.csv (bootstrap distribution and CIs)

**Validation Requirement:**
Validation tools MUST be used after correlation analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_correlations.csv: 2 rows x 10 columns (paradigm, r, ci_lower, ci_upper, p_uncorrected, p_bonferroni, p_fdr, n, method)
- data/step04_bootstrap_results.csv: 1000 rows x 3 columns (iteration, r_diff, valid)
- Additional fields: Steiger_Z, Steiger_p_uncorrected, Steiger_p_bonferroni

*Value Ranges:*
- Correlations r in [-1, 1] (valid correlation bounds)
- p-values in [0, 1]
- Steiger Z statistic typically in [-5, 5]
- Bootstrap r_diff should center around observed difference

*Data Quality:*
- Both correlations computed successfully
- Confidence intervals valid (lower < r < upper)
- Bootstrap iterations = 1000 exactly
- All p-values properly calculated (dual reporting per D068)

*Log Validation:*
- Required: "Correlations computed: r_FreeRecall=X.XXX, r_Recognition=X.XXX"
- Required: "Correlation method: Pearson/Spearman based on normality"
- Required: "Steiger Z-test: Z=X.XXX, p=X.XXX"
- Required: "Bootstrap complete: 1000 iterations, seed=42"
- Required: "Effect size: r_diff=X.XXX"
- Forbidden: "ERROR", "correlation failed", "bootstrap failed"

**Expected Behavior on Validation Failure:**
- Raise error with specific correlation issue
- Log to logs/step04_compute_correlations.log
- Quit immediately, invoke g_debug

### Step 5: Sensitivity Analyses and Robustness Checks
**Dependencies:** Steps 1-4 (correlation results)
**Complexity:** Medium (~10 minutes)

**Purpose:** Perform sensitivity analyses to assess robustness of findings

**Input:**
- data/step03_analysis_dataset.csv (complete dataset)
- data/step04_correlations.csv (primary correlation results)

**Processing:**
- Outlier sensitivity analysis:
  - Identify outliers using Cook's distance > 4/n threshold
  - Re-compute correlations excluding outliers
  - Compare results with/without outliers
- Alternative correlation methods:
  - If Pearson was used: compute Spearman for comparison
  - If Spearman was used: compute Pearson for comparison
  - Document method agreement
- Assumption violation remedies:
  - If normality violated (p < 0.05): Report bootstrap CIs as primary
  - If linearity concerns: Report with acknowledgment
  - If range restriction detected: Document as limitation
- Sample size sensitivity:
  - Compute minimum N for 80% power to detect observed effect
  - Use G*Power or statsmodels.stats.power for correlation difference
  - Report adequacy of current sample size
- Cross-validation of results:
  - Random split-half replication (if N adequate)
  - Compare correlation patterns across subsamples

**Output:**
- data/step05_sensitivity_analyses.csv (outlier effects, method comparisons)
- data/step05_robustness_summary.txt (interpretive summary)

**Validation Requirement:**
Validation tools MUST be used after sensitivity analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_sensitivity_analyses.csv: 4-6 rows x 8 columns (analysis_type, r_FreeRecall, r_Recognition, r_diff, CI_lower, CI_upper, n, notes)
- data/step05_robustness_summary.txt: text summary of robustness findings

*Value Ranges:*
- All correlations in [-1, 1]
- Effect sizes should be similar across sensitivity analyses
- Sample sizes vary by analysis type (full sample vs outlier exclusion)

*Data Quality:*
- Multiple sensitivity analyses completed
- Clear documentation of outlier effects
- Method comparisons provide convergent evidence
- Sample size adequacy assessed

*Log Validation:*
- Required: "Sensitivity analyses complete: X analyses performed"
- Required: "Outlier analysis: X participants excluded, effect on correlations"
- Required: "Method comparison: Pearson vs Spearman agreement"
- Required: "Sample size adequacy: power=X.XX for observed effect"
- Forbidden: "ERROR", "sensitivity failed", "power calculation error"

**Expected Behavior on Validation Failure:**
- Raise error with specific sensitivity analysis issue
- Log to logs/step05_sensitivity_analyses.log
- Quit immediately, invoke g_debug

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (prerequisite check)
- data/step01_ravlt_scores.csv (RAVLT Total scores + descriptives)
- data/step01_ravlt_descriptives.txt (RAVLT summary statistics)
- data/step02_paradigm_theta.csv (Free Recall + Recognition theta scores)
- data/step02_theta_descriptives.txt (theta summary by paradigm)
- data/step03_analysis_dataset.csv (merged dataset for correlations)
- data/step03_assumption_tests.txt (correlation assumption checks)
- data/step04_correlations.csv (primary correlation results + Steiger test)
- data/step04_bootstrap_results.csv (bootstrap distribution for difference)
- data/step05_sensitivity_analyses.csv (robustness checks)
- data/step05_robustness_summary.txt (interpretive summary)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_ravlt.log
- logs/step02_extract_theta.log
- logs/step03_create_dataset.log
- logs/step04_compute_correlations.log
- logs/step05_sensitivity_analyses.log

### Plots (EMPTY until rq_plots runs)
- Note: Scatter plot source data will be created in data/ folder for later visualization

### Results (EMPTY until rq_results runs)
- Note: summary.md created by rq_results will synthesize process-specificity findings

---

## Expected Data Formats

### Step-to-Step Transformations
1. **Step 1 -> 2:** RAVLT scores (wide format) + theta scores (paradigm-specific)
2. **Step 2 -> 3:** Merge on UID, complete cases only
3. **Step 3 -> 4:** Analysis-ready dataset -> correlation matrix + Steiger test
4. **Step 4 -> 5:** Primary results -> sensitivity/robustness analyses

### Column Naming Conventions
- **UID:** Consistent participant identifier across all files
- **RAVLT_Total:** Raw RAVLT Total score (not T-scored)
- **theta_FreeRecall:** Mean IRT theta for Free Recall paradigm
- **theta_Recognition:** Mean IRT theta for Recognition paradigm
- **r, ci_lower, ci_upper:** Correlation with 95% confidence interval
- **p_uncorrected, p_bonferroni, p_fdr:** Dual p-value reporting (Decision D068)

### Data Type Constraints
- **UID:** string/object (non-nullable)
- **All scores:** float64 (nullable for missing data documentation)
- **p-values:** float64 in [0, 1] range
- **Correlations:** float64 in [-1, 1] range

---

## Cross-RQ Dependencies

**Primary Dependency:** Ch5 5.3.x (Paradigm-specific IRT analyses)
- **Required Status:** At least one Ch5 5.3.x RQ must have status: success
- **Required Files:** Paradigm-specific theta scores separated by Free Recall vs Recognition
- **File Patterns:** results/ch5/5.3.*/data/*theta*paradigm*.csv
- **Fallback Strategy:** Search multiple 5.3.x outputs if primary not found
- **Content Validation:** Verify Free Recall (IFR) and Recognition (IRE) paradigms available

**Secondary Dependency:** Master.xlsx cognitive assessment data
- **Required File:** data/cache/master.xlsx
- **Required Content:** RAVLT_Total scores for all 100 participants
- **Format:** Standard Excel sheet with UID and RAVLT_Total columns

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
**Validation Method:** File existence and accessibility checks
**Criteria:** All required files found and readable
**Failure Action:** Quit with specific missing dependency message

#### Step 1: Extract RAVLT Data
**Validation Method:** Data quality and range checks
**Criteria:** 95+ participants, RAVLT scores in [20, 75], normality test results
**Failure Action:** Error with specific data quality issue, invoke g_debug

#### Step 2: Extract Paradigm Theta
**Validation Method:** Paradigm completeness and theta range validation
**Criteria:** Both paradigms available for 95+ participants, theta in [-3, 3]
**Failure Action:** Error with paradigm extraction issue, invoke g_debug

#### Step 3: Create Analysis Dataset
**Validation Method:** Merge success and assumption test completion
**Criteria:** >=95 complete cases, assumption tests documented
**Failure Action:** Error with dataset creation issue, invoke g_debug

#### Step 4: Compute Correlations
**Validation Method:** Correlation bounds and Steiger test validity
**Criteria:** r in [-1, 1], valid CIs, bootstrap complete, dual p-values
**Failure Action:** Error with correlation computation, invoke g_debug

#### Step 5: Sensitivity Analyses
**Validation Method:** Robustness check completion and consistency
**Criteria:** Multiple analyses performed, convergent results documented
**Failure Action:** Error with sensitivity analysis, invoke g_debug

---

## Summary

**Total Steps:** 6 (Step 0: validation + Steps 1-5: analysis)
**Estimated Runtime:** ~45 minutes
**Cross-RQ Dependencies:** Ch5 5.3.x (paradigm-specific theta scores) + master.xlsx (RAVLT)
**Primary Outputs:** Bivariate correlations, Steiger's Z-test, bootstrap CIs, sensitivity analyses
**Validation Coverage:** 100% (all 6 steps have 4-layer validation requirements)

**Key Hypothesis:** r(RAVLT, FreeRecall) > r(RAVLT, Recognition) due to shared generative retrieval processes

**Critical Methodological Notes:**
- Chapter-level Bonferroni correction (alpha = 0.00179) applied
- Dual p-value reporting mandatory (Decision D068)
- Bootstrap sensitivity with 1000 iterations (seed=42) for robustness
- Method selection (Pearson vs Spearman) based on normality tests
- Complete case analysis for missing data handling
- Outlier sensitivity using Cook's distance threshold

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent with v5.1 enhanced statistical specifications