# Analysis Plan: RQ 7.7.4 - Clinical Profiles: False Negatives

**Research Question:** 7.7.4
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

**Pipeline:** Cross-sectional classification with demographic characterization
**Steps:** 7 total analysis steps (Step 0: validation + Steps 1-6: analysis)
**Estimated Runtime:** ~25 minutes total

This analysis identifies "false negatives" - individuals with low RAVLT performance but normal REMEMVR performance, suggesting traditional tests may underestimate real-world memory function. Uses z-score classification to create 2x2 matrix and characterizes false negatives demographically.

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Multiple comparison correction: Bonferroni for demographic comparisons
- Small group handling: Non-parametric alternatives for assumption violations

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 outputs and master.xlsx exist before proceeding

**Input:**
- results/ch5/5.1.1/status.yaml (verify rq_results: success)
- results/ch5/5.1.1/data/step03_theta_scores.csv (REMEMVR theta estimates)
- Alternative: results/ch5/5.1.1/data/*theta*.{csv,txt}
- Fallback: results/ch5/5.1.1/data/*scores*.csv
- data/cache/master.xlsx (RAVLT total, demographics, NART)
- Expected: Ch5 5.1.1 IRT theta estimates for 100 participants

**Processing:**
- Check Ch5 5.1.1 completed successfully (status.yaml)
- Locate theta score file (try multiple patterns)
- Verify file contains participant UIDs and theta estimates
- Verify master.xlsx accessible with required columns
- Log validation results with specific file paths found

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file documenting validation results
- Expected content: file paths found, participant counts verified
- Required entries: Ch5 status, theta file path, master.xlsx access

*Value Ranges:*
- N/A (validation log only)

*Data Quality:*
- Validation must confirm 100 participants in theta data
- Validation must confirm master.xlsx accessible
- All required columns present in both sources

*Log Validation:*
- Required patterns: "Ch5 5.1.1 status: success", "Theta file found:", "master.xlsx accessible"
- Forbidden patterns: "ERROR", "FAIL", "file not found"

**Expected Behavior on Validation Failure:**
- Quit immediately with specific missing dependency
- Log to logs/step00_validate_dependencies.log
- Invoke g_debug for troubleshooting

### Step 1: Extract and Prepare Cognitive Data
**Dependencies:** Step 0 (dependency validation complete)
**Complexity:** Medium (~5 minutes)

**Purpose:** Load REMEMVR theta scores from Ch5 and RAVLT data from master.xlsx

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/*theta*.csv
- Expected columns: UID, theta (REMEMVR ability estimates)
- data/cache/master.xlsx, sheet: 'RAVLT' or 'Cognitive'
- Required columns: UID, RAVLT_Total, Age, Education, VR_Experience
- NART sheet: UID, NART_FSIQ

**Processing:**
- Load REMEMVR theta scores (IRT ability estimates from Ch5)
- Load RAVLT total learning scores (T1-T5 sum)
- Load demographics: age, education, VR experience
- Load NART premorbid IQ estimates
- Merge all data on UID (inner join to ensure complete cases)
- Verify N=100 participants after merge
- Handle missing data: exclude participants with missing RAVLT or theta

**Output:**
- data/step01_cognitive_scores.csv (merged dataset)
- Required columns: UID, REMEMVR_theta, RAVLT_Total, Age, Education, VR_Experience, NART_FSIQ

**Validation Requirement:**
Validation tools MUST be used after data extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_cognitive_scores.csv: 100 rows x 7 columns
- Data types: UID (object), REMEMVR_theta (float64), RAVLT_Total (int64)
- Age (float64), Education (float64), VR_Experience (int64), NART_FSIQ (float64)

*Value Ranges:*
- REMEMVR_theta in [-3, 3] (IRT ability scale)
- RAVLT_Total in [15, 75] (sum of T1-T5, theoretical max 15 words x 5 trials)
- Age in [18, 89] (participant eligibility criteria)
- Education in [8, 25] (years of formal education)
- VR_Experience in [1, 5] (Likert scale)
- NART_FSIQ in [70, 130] (premorbid IQ estimate range)

*Data Quality:*
- Exactly 100 participants after merge
- No duplicate UIDs
- Missing data <5% per variable
- All participants have both RAVLT and REMEMVR data

*Log Validation:*
- Required patterns: "Data merge complete: 100 participants", "No missing values in primary variables"
- Forbidden patterns: "ERROR", "merge failed", "duplicate UIDs"

**Expected Behavior on Validation Failure:**
- Log specific data quality issues
- Report missing data patterns
- Quit if <95 participants remain after exclusions

### Step 2: Standardize Scores for Classification
**Dependencies:** Step 1 (cognitive data extracted)
**Complexity:** Low (~3 minutes)

**Purpose:** Convert RAVLT and REMEMVR scores to z-scores for fair comparison

**Input:**
- data/step01_cognitive_scores.csv (raw cognitive scores)

**Processing:**
- Compute z-scores for RAVLT_Total using sample mean/SD
- Compute z-scores for REMEMVR_theta (already standardized but verify)
- Implementation: scipy.stats.zscore with nan_policy='omit'
- Random seed: Not applicable (deterministic transformation)
- Verify z-score distributions: mean=0, SD=1
- Check for extreme outliers: |z| > 3.0

**Output:**
- data/step02_standardized_scores.csv
- Required columns: UID, RAVLT_z, REMEMVR_z, plus original scores and demographics

**Validation Requirement:**
Validation tools MUST be used after standardization execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_standardized_scores.csv: 100 rows x 9 columns
- Additional columns: RAVLT_z (float64), REMEMVR_z (float64)

*Value Ranges:*
- RAVLT_z approximately in [-3, 3] (standardized scores)
- REMEMVR_z approximately in [-3, 3] (standardized scores)
- Mean of each z-score ≈ 0.0 (±0.1 tolerance)
- SD of each z-score ≈ 1.0 (±0.1 tolerance)

*Data Quality:*
- 100 participants with z-scores computed
- No NaN values in z-scores (unless input was missing)
- Extreme outliers (|z| > 3) flagged but retained

*Log Validation:*
- Required patterns: "Z-scores computed", "RAVLT_z: mean=X.XX, SD=X.XX", "REMEMVR_z: mean=X.XX, SD=X.XX"
- Forbidden patterns: "ERROR", "NaN values introduced"

**Expected Behavior on Validation Failure:**
- Report standardization diagnostics
- Flag extreme outliers for review
- Continue if means/SDs within tolerance

### Step 3: Create Classification Matrix
**Dependencies:** Step 2 (scores standardized)
**Complexity:** Medium (~5 minutes)

**Purpose:** Apply classification criteria to create 2x2 matrix identifying false negatives

**Input:**
- data/step02_standardized_scores.csv (standardized cognitive scores)

**Processing:**
- Apply classification criteria:
  - Low RAVLT: z-score < -1.0 (16th percentile, mild impairment threshold)
  - Normal REMEMVR: z-score > -0.5 (31st percentile, above mild impairment)
- Create binary variables: RAVLT_low, REMEMVR_normal
- Generate 2x2 contingency table using pandas.crosstab
- Identify false negative cases: RAVLT_low=1 AND REMEMVR_normal=1
- Compute cell counts and percentages
- Assumption checking for chi-square test:
  - Expected cell count ≥ 5 per cell (if planning statistical test)
  - Use Fisher's exact test if cell counts <5

**Output:**
- data/step03_classification_matrix.csv (2x2 contingency table)
- data/step03_false_negatives.csv (identified false negative cases with full data)
- Required classification_matrix columns: RAVLT_low_0, RAVLT_low_1, row totals
- Required false_negatives: All original columns plus classification flags

**Validation Requirement:**
Validation tools MUST be used after classification execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_classification_matrix.csv: 2 rows x 3 columns (2x2 + totals)
- data/step03_false_negatives.csv: ~6-10 rows x 11 columns (false negative cases)

*Value Ranges:*
- Cell counts sum to 100 (all participants classified)
- False negative count in [3, 15] (expected 6-10% = 6-10 cases)
- No negative counts
- Percentages sum to 100%

*Data Quality:*
- All 100 participants classified into matrix
- False negative cases have RAVLT_z < -1.0 AND REMEMVR_z > -0.5
- No missing values in classification variables
- Matrix mathematically consistent (row sums = column sums)

*Log Validation:*
- Required patterns: "Classification complete: 100 participants", "False negatives identified: N cases"
- Required pattern: "Matrix validation: PASS"
- Forbidden patterns: "ERROR", "classification failed", "inconsistent totals"

**Expected Behavior on Validation Failure:**
- Report classification diagnostics
- Verify threshold application
- Check matrix arithmetic consistency

### Step 4: Characterize False Negative Demographics
**Dependencies:** Step 3 (false negatives identified)
**Complexity:** Low (~3 minutes)

**Purpose:** Compute descriptive statistics for false negative group

**Input:**
- data/step03_false_negatives.csv (identified false negative cases)
- data/step02_standardized_scores.csv (all participants for comparison)

**Processing:**
- Compute descriptive statistics for false negative group:
  - Demographics: Age, Education, VR_Experience (mean, SD, range)
  - Cognitive: NART_FSIQ, RAVLT_Total, REMEMVR_theta (mean, SD, range)
- Compute same statistics for all other participants (comparison group)
- Create true positive group: RAVLT_z < -1.0 AND REMEMVR_z <= -0.5
- Random seed: Not applicable (descriptive statistics only)
- Handle small sample sizes: report exact N for each statistic

**Output:**
- data/step04_demographic_summary.csv
- Required columns: Variable, False_Neg_N, False_Neg_Mean, False_Neg_SD, Other_N, Other_Mean, Other_SD

**Validation Requirement:**
Validation tools MUST be used after demographic characterization execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_demographic_summary.csv: 6 rows x 7 columns (6 variables characterized)
- Variables: Age, Education, VR_Experience, NART_FSIQ, RAVLT_Total, REMEMVR_theta

*Value Ranges:*
- False_Neg_N in [3, 15] (expected false negative count)
- Other_N in [85, 97] (remaining participants)
- Means within plausible ranges for each variable
- SDs > 0 (non-zero variability)

*Data Quality:*
- False_Neg_N + Other_N = 100 (all participants accounted for)
- No NaN values except for variables with missing data
- Statistics computed only for cases with valid data

*Log Validation:*
- Required patterns: "Demographics computed for N false negatives", "Comparison group: N participants"
- Forbidden patterns: "ERROR", "division by zero", "invalid statistics"

**Expected Behavior on Validation Failure:**
- Report sample size warnings if groups very small
- Flag unusual demographic patterns
- Continue with available statistics

### Step 5: Compare Groups Statistically
**Dependencies:** Step 4 (demographics characterized)
**Complexity:** High (~7 minutes including bootstrap)

**Purpose:** Test statistical differences between false negatives and other participants

**Input:**
- data/step03_false_negatives.csv (false negative cases)
- data/step02_standardized_scores.csv (all participants for group assignment)

**Processing:**
- Create comparison groups:
  - False negatives: RAVLT_z < -1.0 AND REMEMVR_z > -0.5
  - True positives: RAVLT_z < -1.0 AND REMEMVR_z <= -0.5
  - Controls: RAVLT_z >= -1.0
- Statistical testing approach:
  - Continuous variables (Age, Education, NART_FSIQ): t-tests with assumption checking
  - Categorical variables (VR_Experience if treated as ordinal): chi-square or exact tests
- Assumption checking for t-tests:
  - Normality: Shapiro-Wilk test (p > 0.05)
  - Equal variances: Levene's test (p > 0.05)
  - Remedial actions if violated:
    - Normality p < 0.05: Use Mann-Whitney U test (non-parametric)
    - Equal variances p < 0.05: Use Welch's t-test (unequal variances)
- Bootstrap confidence intervals for group differences:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - CI: Percentile method (2.5th, 97.5th percentiles)
- Multiple comparison correction:
  - Family: Within-RQ demographic comparisons (6 variables)
  - Bonferroni: alpha = 0.05/6 = 0.0083 per test
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
  - Format: p_uncorrected, p_bonferroni

**Output:**
- data/step05_group_comparisons.csv
- Required columns: Variable, Test_Type, N1, N2, Statistic, p_uncorrected, p_bonferroni, CI_lower, CI_upper

**Validation Requirement:**
Validation tools MUST be used after statistical comparison execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_group_comparisons.csv: 6 rows x 9 columns (6 demographic variables tested)
- Test types: t-test, Welch t-test, Mann-Whitney U, chi-square, or Fisher exact

*Value Ranges:*
- p_uncorrected in [0, 1] (valid probability range)
- p_bonferroni in [0, 1] and >= p_uncorrected (correction increases p-values)
- CI ranges appropriate for each variable's scale
- Sample sizes N1, N2 sum to relevant comparison group totals

*Data Quality:*
- All 6 demographic variables tested
- Bootstrap CIs computed for all comparisons
- Assumption test results documented
- Dual p-values present for all comparisons (Decision D068)

*Log Validation:*
- Required patterns: "Group comparisons complete: 6 variables", "Bootstrap complete: 1000 iterations"
- Required pattern: "Assumption checks documented"
- Forbidden patterns: "ERROR", "convergence failed", "bootstrap error"

**Expected Behavior on Validation Failure:**
- Report assumption violation details and remedial actions used
- Flag non-convergent bootstrap iterations
- Continue with available valid comparisons

### Step 6: Compute Clinical Performance Metrics
**Dependencies:** Step 3 (classification matrix created)
**Complexity:** Low (~2 minutes)

**Purpose:** Calculate diagnostic performance metrics for clinical interpretation

**Input:**
- data/step03_classification_matrix.csv (2x2 contingency table)
- data/step02_standardized_scores.csv (for base rate calculations)

**Processing:**
- Extract 2x2 matrix cells for diagnostic calculations
- Compute clinical metrics with 95% confidence intervals:
  - Sensitivity: True positives / (True positives + False negatives)
  - Specificity: True negatives / (True negatives + False positives)
  - Positive Predictive Value (PPV): True positives / (True positives + False positives)
  - Negative Predictive Value (NPV): True negatives / (True negatives + False negatives)
- CI computation: Wilson score method for proportions
- Base rates:
  - RAVLT impairment rate: proportion with RAVLT_z < -1.0
  - REMEMVR normal rate: proportion with REMEMVR_z > -0.5
  - False negative rate: false negatives / total sample
- Clinical interpretation guidelines:
  - False negative rate: <5% excellent, 5-10% acceptable, >10% concerning

**Output:**
- data/step06_clinical_metrics.csv
- Required columns: Metric, Value, CI_Lower, CI_Upper, Interpretation

**Validation Requirement:**
Validation tools MUST be used after clinical metrics computation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_clinical_metrics.csv: 7 rows x 5 columns (7 metrics computed)
- Metrics: Sensitivity, Specificity, PPV, NPV, RAVLT_Impairment_Rate, REMEMVR_Normal_Rate, False_Negative_Rate

*Value Ranges:*
- All metric values in [0, 1] (proportions)
- CI_Lower <= Value <= CI_Upper (valid confidence intervals)
- False_Negative_Rate expected in [0.03, 0.15] (3-15% based on predictions)

*Data Quality:*
- All 7 metrics computed successfully
- CIs computed using Wilson score method
- No impossible values (proportions outside [0,1])
- Interpretations provided for key metrics

*Log Validation:*
- Required patterns: "Clinical metrics computed: 7 measures", "Wilson CIs computed"
- Forbidden patterns: "ERROR", "invalid proportions", "CI computation failed"

**Expected Behavior on Validation Failure:**
- Report matrix cell counts used in calculations
- Flag impossible metric values
- Verify CI computation methodology

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (prerequisite validation log)
- data/step01_cognitive_scores.csv (merged cognitive data: 100 x 7)
- data/step02_standardized_scores.csv (z-scores added: 100 x 9)
- data/step03_classification_matrix.csv (2x2 contingency table: 2 x 3)
- data/step03_false_negatives.csv (identified cases: ~6-10 x 11)
- data/step04_demographic_summary.csv (descriptive statistics: 6 x 7)
- data/step05_group_comparisons.csv (statistical tests: 6 x 9)
- data/step06_clinical_metrics.csv (diagnostic performance: 7 x 5)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_cognitive_data.log
- logs/step02_standardize_scores.log
- logs/step03_create_classification.log
- logs/step04_characterize_demographics.log
- logs/step05_compare_groups.log
- logs/step06_compute_clinical_metrics.log

### Plots (EMPTY until rq_plots runs)
Plot source CSVs created in data/:
- data/step02_standardized_scores.csv (for scatter plot: RAVLT_z vs REMEMVR_z with quadrants)
- data/step04_demographic_summary.csv (for group comparison plots)

### Results (EMPTY until rq_results runs)
- results/summary.md (created by rq_results)

---

## Expected Data Formats

### Step-to-Step Transformations
- Step 1: Raw scores -> merged dataset (100 participants, 7 variables)
- Step 2: Raw scores -> z-scores (same structure + 2 z-score columns)
- Step 3: Continuous z-scores -> binary classification + case identification
- Step 4: Cases -> descriptive statistics (group summaries)
- Step 5: Groups -> statistical comparisons with dual p-values
- Step 6: Matrix -> clinical performance metrics

### Column Naming Conventions
- Primary keys: UID (consistent across all files)
- Original scores: RAVLT_Total, REMEMVR_theta
- Standardized: RAVLT_z, REMEMVR_z
- Classifications: RAVLT_low, REMEMVR_normal
- Statistics: _Mean, _SD, _N suffixes
- P-values: p_uncorrected, p_bonferroni (Decision D068)

### Data Type Constraints
- UID: object (string identifiers, not nullable)
- Scores: float64 (allow decimals, missing = NaN)
- Demographics: Age, Education (float64), VR_Experience (int64)
- Classifications: bool (True/False)
- P-values: float64 in [0, 1]

---

## Cross-RQ Dependencies

**Dependencies:**
- Ch5 5.1.1: IRT theta estimates (REMEMVR ability scores)
- master.xlsx: RAVLT total scores, demographics, NART premorbid IQ

**File Discovery Patterns:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/*theta*.csv
- Fallback: results/ch5/5.1.1/data/*scores*.csv
- Circuit breaker: If no Ch5 theta files found, QUIT with dependency error

**Format Expectations:**
- Theta files: UID column + theta column (N=100 participants)
- master.xlsx: Multiple sheets with UID-linked data

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
- Output files: dependency validation text
- Value ranges: N/A (validation log)
- Data quality: confirms 100 participants, file accessibility
- Log validation: required success patterns, forbidden error patterns

#### Step 1: Extract Cognitive Data
- Output files: merged dataset (100 x 7)
- Value ranges: cognitive scores within expected clinical ranges
- Data quality: complete cases only, no duplicates
- Log validation: merge success, data quality confirmation

#### Step 2: Standardize Scores
- Output files: dataset with z-scores (100 x 9)
- Value ranges: z-scores approximately normal distribution
- Data quality: mean≈0, SD≈1 for z-scores
- Log validation: standardization success, distribution parameters

#### Step 3: Create Classification
- Output files: classification matrix (2 x 3), false negative cases (~6-10 x 11)
- Value ranges: cell counts sum to 100, false negatives in expected range
- Data quality: matrix consistency, classification criteria correctly applied
- Log validation: classification success, matrix validation

#### Step 4: Characterize Demographics
- Output files: demographic summary (6 x 7)
- Value ranges: statistics within plausible demographic ranges
- Data quality: complete statistics for available data
- Log validation: computation success, valid statistics

#### Step 5: Compare Groups
- Output files: group comparisons (6 x 9)
- Value ranges: p-values in [0,1], dual p-value compliance
- Data quality: assumption checking documented, bootstrap CIs valid
- Log validation: statistical test success, bootstrap completion

#### Step 6: Compute Clinical Metrics
- Output files: clinical metrics (7 x 5)
- Value ranges: all metrics as proportions [0,1]
- Data quality: valid confidence intervals, clinical interpretations
- Log validation: metric computation success, CI validity

---

## Summary

**Total Steps:** 7 (Step 0: validation + Steps 1-6: analysis)
**Estimated Runtime:** ~25 minutes
**Cross-RQ Dependencies:** Ch5 5.1.1 (theta scores)
**Primary Outputs:** Classification matrix, false negative characterization, group comparisons
**Validation Coverage:** 100% (all 7 steps have 4-layer validation requirements)

**Key Hypothesis:** Some individuals with low RAVLT performance may show normal REMEMVR performance, representing false negatives where traditional tests underestimate real-world memory function. These false negatives may be characterized by specific demographic profiles.

**Critical Methodological Notes:**
- Small expected false negative sample (6-10 cases) requires careful statistical handling
- Non-parametric alternatives specified for assumption violations
- Bootstrap CIs provide robust inference for small groups
- Multiple comparison correction maintains family-wise error rate
- Decision D068 ensures dual p-value reporting throughout

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent v5.1.0