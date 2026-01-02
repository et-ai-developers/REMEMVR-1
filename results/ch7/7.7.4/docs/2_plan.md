# Analysis Plan: RQ 7.7.4 - Clinical Profiles: False Negatives

**Research Question:** 7.7.4
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

**Research Question:** Can we identify "false negatives" - individuals with low RAVLT but normal REMEMVR? These may have intact ecological memory despite poor lab performance.

**Pipeline:** Cross-sectional classification analysis with demographic characterization
**Steps:** 7 total analysis steps (Step 0: validation + Steps 1-6: analysis)
**Estimated Runtime:** 25-30 minutes

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni corrected)

**Methodological Notes:**
- Classification uses z-standardized scores for fair comparison between tests
- Small expected false negative group (6-10 cases) requires emphasis on effect sizes over significance testing
- Cross-RQ dependency on Ch5 5.1.1 for REMEMVR theta scores

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies

**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 outputs exist and master.xlsx is accessible before proceeding

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv (REMEMVR theta estimates)
- Alternative: results/ch5/5.1.1/data/*theta*.csv
- Fallback: results/ch5/5.1.1/data/step*_*.csv (search for any theta-related files)
- Master data: data/cache/master.xlsx (RAVLT, demographics, NART)
- Expected content: Participant theta estimates from IRT analysis
- If not found: QUIT with "Ch5 5.1.1 theta outputs not found - run Ch5 first"

**Processing:**
- Check Ch5 5.1.1 status.yaml for rq_results: success
- Verify theta scores file exists and contains UID, theta, SE columns
- Verify master.xlsx accessible with required sheets (Demographics, RAVLT, NART)
- Check for 100 participants in both sources
- Log all validation checks

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Expected content: "PASS" for all checks or specific failure messages

*Value Ranges:*
- Participant count: 100 in both sources
- Theta range: [-3, 3] (standard IRT scale)
- SE range: [0.1, 1.0] (positive standard errors)

*Data Quality:*
- All required files accessible
- No missing UIDs in theta file
- All required columns present in master.xlsx

*Log Validation:*
- Required pattern: "Dependency validation complete: PASS"
- Required pattern: "Ch5 5.1.1 status: success"
- Forbidden patterns: "ERROR", "FAIL", "not found"

**Expected Behavior on Validation Failure:**
- Raise error with specific missing dependency
- Log to logs/step00_validate_dependencies.log
- Quit immediately, invoke g_debug

### Step 1: Extract and Standardize Cognitive Scores

**Dependencies:** Step 0 (validated dependencies)
**Complexity:** Medium (~5 minutes)

**Purpose:** Load REMEMVR theta and RAVLT total scores, standardize both to z-scores for classification

**Input:**
- data/step00_dependency_validation.txt (confirmation of successful validation)
- results/ch5/5.1.1/data/step03_theta_scores.csv (REMEMVR theta estimates)
- data/cache/master.xlsx sheets: Demographics (UID), RAVLT (UID, Total_T1T5)

**Processing:**
- Load REMEMVR theta scores (UID, theta columns)
- Load RAVLT total scores from master.xlsx
- Merge datasets on UID, verify N=100 complete cases
- Standardize both measures to z-scores using scipy.stats.zscore
- Random seed: 42 for reproducibility
- Validate z-score distributions (mean ~0, std ~1)
- Check for outliers beyond +/- 3 SD

**Output:**
- data/step01_cognitive_scores.csv (UID, REMEMVR_theta, RAVLT_total, REMEMVR_z, RAVLT_z)

**Validation Requirement:**
Validation tools MUST be used after z-score standardization execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_cognitive_scores.csv: 100 rows x 5 columns
- Columns: UID (object), REMEMVR_theta (float64), RAVLT_total (int64), REMEMVR_z (float64), RAVLT_z (float64)

*Value Ranges:*
- REMEMVR_theta in [-3, 3] (IRT ability scale)
- RAVLT_total in [20, 80] (reasonable RAVLT range)
- REMEMVR_z mean: [-0.1, 0.1], std: [0.9, 1.1]
- RAVLT_z mean: [-0.1, 0.1], std: [0.9, 1.1]

*Data Quality:*
- All 100 participants present
- No missing values in z-score columns
- Z-score distributions approximately normal

*Log Validation:*
- Required pattern: "Standardization complete: N=100"
- Required pattern: "Z-scores validated: mean~0, std~1"
- Forbidden patterns: "ERROR", "missing", "NaN"

**Expected Behavior on Validation Failure:**
- Raise error with specific data quality issue
- Log to logs/step01_extract_standardize.log
- Quit immediately, invoke g_debug

### Step 2: Apply Classification Criteria

**Dependencies:** Step 1 (standardized cognitive scores)
**Complexity:** Low (<5 minutes)

**Purpose:** Apply classification criteria to identify false negatives and create 2x2 classification matrix

**Input:**
- data/step01_cognitive_scores.csv (z-standardized scores)

**Processing:**
- Apply classification criteria:
  - Low RAVLT: RAVLT_z < -1.0 (16th percentile, mild impairment)
  - Normal REMEMVR: REMEMVR_z > -0.5 (31st percentile)
  - False Negatives: RAVLT_z < -1.0 AND REMEMVR_z > -0.5
- Create binary classification variables
- Generate 2x2 contingency table using pandas.crosstab
- Count cases in each quadrant
- Calculate classification percentages

**Output:**
- data/step02_classification_matrix.csv (2x2 contingency table with counts and percentages)
- data/step02_classified_participants.csv (UID with classification flags)

**Validation Requirement:**
Validation tools MUST be used after classification execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_classification_matrix.csv: 2 rows x 2 columns
- data/step02_classified_participants.csv: 100 rows x 5 columns

*Value Ranges:*
- False negative count: 3-15 cases (expected 6-10 based on concept)
- Total classifications: 100 participants
- All percentages in [0, 100]

*Data Quality:*
- All 100 participants classified
- Matrix cells sum to 100
- No missing classification flags

*Log Validation:*
- Required pattern: "Classification complete: 100 participants"
- Required pattern: "False negatives identified: N cases"
- Forbidden patterns: "ERROR", "unclassified", "NaN"

**Expected Behavior on Validation Failure:**
- Raise error with classification inconsistency
- Log to logs/step02_apply_classification.log
- Quit immediately, invoke g_debug

### Step 3: Extract Demographics and Cognitive Measures

**Dependencies:** Step 2 (classified participants)
**Complexity:** Medium (~5 minutes)

**Purpose:** Extract demographics and NART scores for false negative characterization

**Input:**
- data/step02_classified_participants.csv (classification flags)
- data/cache/master.xlsx sheets: Demographics (Age, Education, VR_Experience), NART (NART_IQ)

**Processing:**
- Load demographic variables for all participants
- Load NART premorbid IQ estimates
- Merge with classification data on UID
- Create subset of false negative cases
- Calculate descriptive statistics for false negative group
- Handle missing data (listwise deletion, report N per variable)

**Output:**
- data/step03_demographics_full.csv (all participants with demographics)
- data/step03_false_negatives.csv (false negative cases only with all variables)
- data/step03_false_negative_descriptives.csv (descriptive statistics)

**Validation Requirement:**
Validation tools MUST be used after demographic extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_demographics_full.csv: 100 rows x 8+ columns
- data/step03_false_negatives.csv: 6-15 rows x 8+ columns
- data/step03_false_negative_descriptives.csv: 4 rows x 3+ columns (mean, std, N)

*Value Ranges:*
- Age in [18, 85] (adult sample)
- Education in [8, 20] (years of education)
- VR_Experience in [1, 5] (Likert scale)
- NART_IQ in [70, 130] (premorbid IQ range)

*Data Quality:*
- False negative N matches Step 2 count
- Missing data <10% per variable
- All demographic ranges plausible

*Log Validation:*
- Required pattern: "Demographics extracted: N=100"
- Required pattern: "False negatives characterized: N cases"
- Forbidden patterns: "ERROR", "missing demographics"

**Expected Behavior on Validation Failure:**
- Raise error with demographic data issue
- Log to logs/step03_extract_demographics.log
- Quit immediately, invoke g_debug

### Step 4: Statistical Group Comparisons

**Dependencies:** Step 3 (demographics with false negative identification)
**Complexity:** Medium (~10 minutes including assumption checking)

**Purpose:** Compare false negatives vs other participants on demographic variables with assumption validation

**Input:**
- data/step03_demographics_full.csv (all participants with classification)

**Processing:**
- Create comparison groups: False Negatives vs Others
- Check assumptions before parametric tests:
  - Normality: Shapiro-Wilk test for each variable (p > 0.05)
  - Equal variances: Levene's test for each comparison (p > 0.05)
- For continuous variables (Age, Education, NART_IQ):
  - If assumptions met: Independent samples t-test
  - If assumptions violated: Mann-Whitney U test
  - Calculate Cohen's d effect sizes with 95% CI
- For categorical variables (VR_Experience):
  - Chi-square test (if expected cell count >= 5)
  - Fisher's exact test (if small cell counts)
- Multiple comparison correction:
  - Family: Within-RQ (4 demographic variables)
  - Bonferroni: alpha = 0.05/4 = 0.0125 per test
  - Also compute FDR using Benjamini-Hochberg
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Bootstrap 95% CIs for group differences:
  - Iterations: 1000
  - Random seed: 42
  - Method: Participant-level resampling with replacement

**Output:**
- data/step04_assumption_checks.csv (normality and equal variance test results)
- data/step04_group_comparisons.csv (statistical comparisons with dual p-values)
- data/step04_effect_sizes.csv (Cohen's d with bootstrap CIs)

**Validation Requirement:**
Validation tools MUST be used after statistical comparison execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_assumption_checks.csv: 4 rows x 4 columns (variable, normality_p, equal_var_p, test_used)
- data/step04_group_comparisons.csv: 4 rows x 6 columns (variable, statistic, p_uncorrected, p_bonferroni, p_fdr, test_type)
- data/step04_effect_sizes.csv: 3 rows x 5 columns (variable, cohens_d, ci_lower, ci_upper, interpretation)

*Value Ranges:*
- All p-values in [0, 1]
- Cohen's d in [-2, 2] (reasonable effect size range)
- CI bounds: ci_lower < cohens_d < ci_upper
- Test statistics: reasonable values per test type

*Data Quality:*
- All 4 demographic variables tested
- Dual p-values present for all tests (Decision D068)
- Bootstrap CIs computed for all effect sizes
- Assumption check results guide test selection

*Log Validation:*
- Required pattern: "Assumption checks complete: 4 variables"
- Required pattern: "Group comparisons complete: dual p-values"
- Required pattern: "Bootstrap CIs computed: 1000 iterations"
- Forbidden patterns: "ERROR", "convergence failed"

**Expected Behavior on Validation Failure:**
- Raise error with statistical test failure
- Log to logs/step04_statistical_comparisons.log
- Quit immediately, invoke g_debug

### Step 5: Clinical Performance Metrics

**Dependencies:** Step 4 (group comparisons)
**Complexity:** Medium (~5 minutes)

**Purpose:** Calculate clinical utility metrics treating RAVLT as reference standard

**Input:**
- data/step02_classification_matrix.csv (2x2 contingency table)

**Processing:**
- Extract 2x2 classification matrix counts
- Calculate clinical performance metrics:
  - Sensitivity: True Positives / (True Positives + False Negatives)
  - Specificity: True Negatives / (True Negatives + False Positives)
  - Positive Predictive Value: True Positives / (True Positives + False Positives)
  - Negative Predictive Value: True Negatives / (True Negatives + False Negatives)
- Bootstrap 95% CIs for all metrics:
  - Iterations: 1000
  - Random seed: 42
  - Method: Participant-level resampling with replacement
  - CI: Percentile method (2.5th, 97.5th percentiles)
- Calculate base rates and prevalence estimates
- Frame false negatives as potential clinical reassurance cases

**Output:**
- data/step05_clinical_metrics.csv (sensitivity, specificity, PPV, NPV with CIs)
- data/step05_base_rates.csv (prevalence and classification base rates)

**Validation Requirement:**
Validation tools MUST be used after clinical metrics calculation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_clinical_metrics.csv: 4 rows x 4 columns (metric, value, ci_lower, ci_upper)
- data/step05_base_rates.csv: 3 rows x 2 columns (rate_type, percentage)

*Value Ranges:*
- All clinical metrics in [0, 1]
- Bootstrap CIs: ci_lower < value < ci_upper
- Base rates sum appropriately across categories

*Data Quality:*
- All 4 clinical metrics computed
- Bootstrap CIs valid for all metrics
- Base rates consistent with classification matrix

*Log Validation:*
- Required pattern: "Clinical metrics computed: sensitivity, specificity, PPV, NPV"
- Required pattern: "Bootstrap CIs complete: 1000 iterations"
- Forbidden patterns: "ERROR", "division by zero"

**Expected Behavior on Validation Failure:**
- Raise error with clinical metrics calculation issue
- Log to logs/step05_clinical_metrics.log
- Quit immediately, invoke g_debug

### Step 6: Clinical Interpretation Summary

**Dependencies:** Step 5 (clinical metrics)
**Complexity:** Low (<5 minutes)

**Purpose:** Synthesize findings into clinical interpretation and recommendations

**Input:**
- data/step04_group_comparisons.csv (demographic differences)
- data/step05_clinical_metrics.csv (diagnostic performance)
- data/step03_false_negative_descriptives.csv (false negative characteristics)

**Processing:**
- Compile key findings:
  - False negative rate and demographic profile
  - Significant demographic differences (corrected p-values)
  - Clinical performance metrics with interpretation
- Frame clinical implications:
  - Reassurance potential for false negative cases
  - Dual assessment approach recommendations
  - Limitations due to small false negative group
- Acknowledge power limitations:
  - Small false negative sample (6-10 cases) limits statistical power
  - Emphasize effect sizes and confidence intervals over significance
  - Frame as descriptive characterization rather than hypothesis testing
- Generate structured clinical summary with recommendations

**Output:**
- data/step06_clinical_interpretation.txt (structured clinical summary)
- data/step06_recommendations.txt (clinical practice recommendations)

**Validation Requirement:**
Validation tools MUST be used after clinical interpretation generation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_clinical_interpretation.txt: text file with structured summary
- data/step06_recommendations.txt: text file with clinical recommendations

*Value Ranges:*
- False negative percentage cited matches previous calculations
- Effect sizes and CIs accurately transcribed from prior steps

*Data Quality:*
- All key findings included in summary
- Power limitations explicitly acknowledged
- Clinical implications appropriately framed

*Log Validation:*
- Required pattern: "Clinical interpretation complete"
- Required pattern: "Recommendations generated"
- Forbidden patterns: "ERROR", "missing data"

**Expected Behavior on Validation Failure:**
- Raise error with interpretation generation issue
- Log to logs/step06_clinical_interpretation.log
- Quit immediately, invoke g_debug

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (prerequisite validation)
- data/step01_cognitive_scores.csv (z-standardized RAVLT and REMEMVR scores)
- data/step02_classification_matrix.csv (2x2 contingency table)
- data/step02_classified_participants.csv (all participants with classification flags)
- data/step03_demographics_full.csv (all participants with demographics)
- data/step03_false_negatives.csv (false negative cases only)
- data/step03_false_negative_descriptives.csv (descriptive statistics)
- data/step04_assumption_checks.csv (normality and equal variance results)
- data/step04_group_comparisons.csv (statistical tests with dual p-values)
- data/step04_effect_sizes.csv (Cohen's d with bootstrap CIs)
- data/step05_clinical_metrics.csv (sensitivity, specificity, PPV, NPV)
- data/step05_base_rates.csv (prevalence and classification rates)
- data/step06_clinical_interpretation.txt (structured clinical summary)
- data/step06_recommendations.txt (clinical practice recommendations)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_standardize.log
- logs/step02_apply_classification.log
- logs/step03_extract_demographics.log
- logs/step04_statistical_comparisons.log
- logs/step05_clinical_metrics.log
- logs/step06_clinical_interpretation.log

### Plots (EMPTY until rq_plots runs)
Plot source CSVs will be created in data/:
- data/step01_classification_scatter_plot_data.csv (for RAVLT vs REMEMVR scatter with quadrants)
- data/step04_demographic_comparisons_plot_data.csv (for false negatives vs others comparison plots)

### Results (EMPTY until rq_results runs)
summary.md will be created by rq_results summarizing false negative findings

---

## Expected Data Formats

### Step-to-Step Transformations
1. Raw scores (REMEMVR theta, RAVLT total) -> Standardized z-scores
2. Z-scores -> Binary classifications (Low/Normal)
3. Classifications -> 2x2 contingency matrix
4. Classifications + Demographics -> Group comparisons
5. Contingency matrix -> Clinical performance metrics
6. All results -> Clinical interpretation synthesis

### Column Naming Conventions
- UIDs: UID (consistent across all files)
- Raw scores: REMEMVR_theta, RAVLT_total
- Standardized: REMEMVR_z, RAVLT_z
- Classifications: RAVLT_low, REMEMVR_normal, False_Negative
- Demographics: Age, Education, VR_Experience, NART_IQ
- Statistical results: p_uncorrected, p_bonferroni, p_fdr, cohens_d, ci_lower, ci_upper

### Data Type Constraints
- UID: object (non-nullable)
- Scores: float64 (nullable for missing data)
- Classifications: bool (non-nullable)
- Demographics: Age (int64), Education (float64), VR_Experience (int64), NART_IQ (float64)
- Statistical results: float64 (nullable for non-applicable tests)

---

## Cross-RQ Dependencies

**Primary Dependency:** Ch5 5.1.1 (Functional Form Comparison)
- **Required file:** results/ch5/5.1.1/data/step03_theta_scores.csv
- **Content:** REMEMVR theta estimates from IRT calibration
- **Format:** UID, theta, SE columns with 100 participants
- **Fallback strategy:** Search for any *theta*.csv files in Ch5 5.1.1 data folder
- **Circuit breaker:** If not found, QUIT with clear error message

**Secondary Dependency:** master.xlsx (always available)
- **Location:** data/cache/master.xlsx
- **Required sheets:** Demographics, RAVLT, NART
- **Expected format:** UID column plus measurement columns per sheet

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

**All steps follow 4-layer validation structure as specified above:**
1. Output Files: Exact file paths, expected dimensions, data types
2. Value Ranges: Scientific bounds for all numeric variables
3. Data Quality: Missing data tolerance, expected N, plausible ranges
4. Log Validation: Required success patterns, forbidden error patterns

**Validation Coverage:** 100% (all 7 steps have 4-layer validation requirements)

**Key Validation Themes:**
- Cross-RQ dependency validation (Step 0)
- Z-score distribution validation (Step 1)
- Classification consistency validation (Step 2)
- Statistical assumption checking validation (Step 4)
- Bootstrap CI validity validation (Steps 4-5)
- Clinical metrics bounds validation (Step 5)

---

## Summary

**Total Steps:** 7 (Step 0: validation + Steps 1-6: analysis)
**Estimated Runtime:** 25-30 minutes
**Cross-RQ Dependencies:** Ch5 5.1.1 (REMEMVR theta scores)
**Primary Outputs:** 2x2 classification matrix, demographic characterization, clinical performance metrics
**Validation Coverage:** 100% (all 7 steps have 4-layer validation requirements)

**Key Hypothesis:** Some low-RAVLT individuals may show normal REMEMVR performance, suggesting traditional tests underestimate their real-world memory function. False negatives may be characterized by specific demographic profiles (older age, higher education, higher NART scores).

**Critical Methodological Notes:**
- Small expected false negative group (6-10 cases) requires emphasis on effect sizes over significance testing
- Asymmetric classification thresholds (-1.0 vs -0.5) based on clinical judgment, acknowledged as limitation
- Bootstrap methods used throughout for robust CI estimation with small groups
- Comprehensive assumption checking with non-parametric alternatives specified
- Decision D068 dual p-value reporting implemented for all comparisons

**Limitations Acknowledged:**
- Limited statistical power for group comparisons due to small false negative sample
- Classification thresholds require literature justification in future work
- Cross-sectional design limits causal inference about test performance differences

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent with v5.1 statistical specifications