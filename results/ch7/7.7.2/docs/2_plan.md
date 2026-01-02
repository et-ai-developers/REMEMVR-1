# Analysis Plan: RQ 7.7.2 - Discrepancy Analysis - Who diverges?

**Research Question:** 7.7.2
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

**Pipeline:** Discrepancy Analysis with Group Comparisons (One-way ANOVA with post-hoc tests)
**Steps:** 8 total analysis steps (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** ~45 minutes

This analysis examines discrepancy patterns between REMEMVR (ecological) and RAVLT (traditional) memory assessments. Creates standardized discrepancy scores (REMEMVR_z - RAVLT_z) to identify individuals who perform better on one assessment versus the other, then characterizes these groups demographically to understand who diverges and why.

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Enhanced statistical specifications: random seeds, bootstrap CIs, power analysis, comprehensive remedial actions

**Primary Hypothesis:** VR-favored individuals (better REMEMVR than RAVLT) will be significantly older than RAVLT-favored individuals, reflecting age-related benefits from environmental scaffolding in VR assessment.

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 outputs and master.xlsx data exist before proceeding with discrepancy analysis

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv (omnibus theta_all scores)
- Alternative: results/ch5/5.1.1/data/*theta*.csv (Ch5 theta estimation outputs)
- Fallback pattern: results/ch5/5.1.1/data/*omnibus*.{csv,txt} (any omnibus analysis files)
- Master data: data/cache/master.xlsx (RAVLT Total + demographics)
- Expected content: 100 participants with theta_all scores from Ch5 IRT analysis

**Processing:**
- Check Ch5 5.1.1 completion status in status.yaml (rq_results: success required)
- Locate theta score file using multiple search patterns
- Verify file contains theta_all column and 100 participants
- Verify master.xlsx accessible with RAVLT_Total, Age, Education, VR_Experience columns
- Log all validation checks with specific file sizes and row counts
- If Ch5 outputs missing: QUIT with "Ch5 5.1.1 theta scores required for discrepancy analysis"

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- File size: >500 bytes (comprehensive validation log)

*Value Ranges:*
- N/A (validation step)

*Data Quality:*
- Validation log contains "Ch5 5.1.1: FOUND" for theta scores
- Validation log contains "master.xlsx: ACCESSIBLE" for demographics
- No "MISSING" or "ERROR" entries in critical validation checks

*Log Validation:*
- Required patterns: "Ch5 validation: PASS", "Master data: ACCESSIBLE"
- Required patterns: "100 participants confirmed"
- Forbidden patterns: "ERROR", "MISSING", "Ch5 incomplete"

**Expected Behavior on Validation Failure:**
- Raise error with specific missing file information
- Log to logs/step00_validate_dependencies.log
- Quit immediately with instructions to complete Ch5 first

---

### Step 1: Extract and Standardize Scores
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (~5 minutes)

**Purpose:** Load REMEMVR theta_all scores from Ch5 and RAVLT Total scores from master.xlsx, standardize both to z-scores for comparable discrepancy calculation

**Input:**
- results/ch5/5.1.1/data/step03_theta_scores.csv (or discovered equivalent from Step 0)
- data/cache/master.xlsx (RAVLT_Total column)
- Expected: 100 participants with complete data on both measures

**Processing:**
- Load theta_all scores from Ch5 output (omnibus IRT ability estimates)
- Load RAVLT_Total scores from master.xlsx
- Merge datasets on UID (participant identifier)
- Check for missing data: exclude participants missing either score
- Standardize both measures to z-scores using study sample (N=100):
  - REMEMVR_z = (theta_all - mean_theta) / sd_theta
  - RAVLT_z = (RAVLT_Total - mean_RAVLT) / sd_RAVLT
- Verify standardization: mean ~ 0, sd ~ 1 for both measures
- Report descriptive statistics and missing data patterns
- Flag any participants with extreme scores (|z| > 3) for outlier consideration

**Output:**
- data/step01_standardized_scores.csv (UID, theta_all, RAVLT_Total, REMEMVR_z, RAVLT_z)
- data/step01_descriptive_stats.txt (means, SDs, missing data summary)

**Validation Requirement:**
Validation tools MUST be used after score standardization execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_standardized_scores.csv: 100 rows × 5 columns
- Columns: UID (object), theta_all (float64), RAVLT_Total (float64), REMEMVR_z (float64), RAVLT_z (float64)
- data/step01_descriptive_stats.txt: text file with summary statistics

*Value Ranges:*
- theta_all in [-3, 3] (IRT ability scale)
- RAVLT_Total in [0, 80] (maximum possible RAVLT score)
- REMEMVR_z mean ~ 0, sd ~ 1 (standardized)
- RAVLT_z mean ~ 0, sd ~ 1 (standardized)

*Data Quality:*
- All 100 participants present (no missing UIDs)
- No NaN values in z-score columns
- |z-score means| < 0.1 (properly standardized)
- z-score SDs between 0.95-1.05 (properly standardized)

*Log Validation:*
- Required patterns: "Standardization complete: N=100"
- Required patterns: "REMEMVR_z: mean=X.XX, sd=X.XX"
- Required patterns: "RAVLT_z: mean=X.XX, sd=X.XX"
- Forbidden patterns: "ERROR", "missing data", "NaN"

**Expected Behavior on Validation Failure:**
- Raise error if standardization improper (means not ~0, SDs not ~1)
- Log missing data details to logs/step01_standardize_scores.log
- Quit if >5% missing data on either measure

---

### Step 2: Compute Discrepancy Scores
**Dependencies:** Step 1 (standardized scores)
**Complexity:** Low (~5 minutes)

**Purpose:** Calculate REMEMVR_z - RAVLT_z discrepancy scores to identify individuals who perform better on one assessment versus the other

**Input:**
- data/step01_standardized_scores.csv

**Processing:**
- Calculate discrepancy scores: Discrepancy = REMEMVR_z - RAVLT_z
- Positive values indicate VR-favored performance (better REMEMVR than RAVLT)
- Negative values indicate RAVLT-favored performance (better RAVLT than REMEMVR)
- Values near zero indicate concordant performance
- Compute descriptive statistics for discrepancy distribution:
  - Mean, median, SD, min, max, skewness, kurtosis
  - 25th, 50th, 75th percentiles
- Check for normality using Shapiro-Wilk test
- Identify extreme discrepancy cases (|discrepancy| > 2.5 SD) for potential outlier analysis

**Output:**
- data/step02_discrepancy_scores.csv (UID, REMEMVR_z, RAVLT_z, Discrepancy)
- data/step02_discrepancy_distribution.txt (descriptive statistics and normality test)

**Validation Requirement:**
Validation tools MUST be used after discrepancy calculation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_discrepancy_scores.csv: 100 rows × 4 columns
- Columns: UID (object), REMEMVR_z (float64), RAVLT_z (float64), Discrepancy (float64)
- data/step02_discrepancy_distribution.txt: text file with distribution statistics

*Value Ranges:*
- Discrepancy in [-6, 6] (theoretical range for z-score differences)
- Discrepancy mean ~ 0 (since both measures standardized to same sample)
- Discrepancy SD > 0 (variability in individual differences)

*Data Quality:*
- All 100 participants present
- No NaN values in Discrepancy column
- Discrepancy distribution approximately normal (Shapiro-Wilk p > 0.01)
- Range consistent with individual differences in cognitive abilities

*Log Validation:*
- Required patterns: "Discrepancy calculation complete: N=100"
- Required patterns: "Mean discrepancy: X.XX"
- Required patterns: "Normality test: W=X.XX, p=X.XX"
- Forbidden patterns: "ERROR", "infinite", "NaN"

**Expected Behavior on Validation Failure:**
- Log extreme discrepancy cases to logs/step02_compute_discrepancy.log
- Proceed with caution if discrepancy distribution severely non-normal (W < 0.90)
- Document outliers but continue analysis

---

### Step 3: Assign Discrepancy Groups
**Dependencies:** Step 2 (discrepancy scores)
**Complexity:** Medium (~10 minutes including sensitivity analysis)

**Purpose:** Classify participants into three groups based on discrepancy magnitude: VR-favored, RAVLT-favored, and Concordant, with sensitivity analysis for threshold robustness

**Input:**
- data/step02_discrepancy_scores.csv

**Processing:**
- Primary classification using ±1 SD cutoffs:
  - VR-favored: Discrepancy > +1 SD (better REMEMVR than RAVLT)
  - RAVLT-favored: Discrepancy < -1 SD (better RAVLT than REMEMVR)
  - Concordant: |Discrepancy| <= 1 SD (similar performance)
- Sensitivity analysis for threshold robustness:
  - Repeat classification with ±0.75 SD and ±1.25 SD cutoffs
  - Compare group assignments across thresholds
  - Report stability of group membership (% participants maintaining classification)
- Compute group sizes for each threshold:
  - Target: VR-favored n ≥ 16, RAVLT-favored n ≥ 16, Concordant n ≥ 68
- Post-hoc power analysis for group comparisons:
  - Calculate achieved power for detecting d=0.5 effects
  - Use statsmodels.stats.power.ttest_power()
  - Given: smallest group sizes, alpha=0.05/3 outcomes = 0.0167 (Bonferroni)
  - Report: power for VR-favored vs RAVLT-favored comparison (smallest groups)

**Output:**
- data/step03_group_assignments.csv (UID, Discrepancy, Group_1SD, Group_075SD, Group_125SD)
- data/step03_group_summary.txt (group sizes, sensitivity analysis, power calculations)

**Validation Requirement:**
Validation tools MUST be used after group assignment execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_group_assignments.csv: 100 rows × 5 columns
- Columns: UID (object), Discrepancy (float64), Group_1SD (category), Group_075SD (category), Group_125SD (category)
- data/step03_group_summary.txt: text file with group statistics and power analysis

*Value Ranges:*
- Group categories: "VR-favored", "RAVLT-favored", "Concordant"
- Group sizes: each group n ≥ 5 (minimum for statistical analysis)
- Power values in [0, 1] (valid probability range)

*Data Quality:*
- All 100 participants assigned to exactly one group per threshold
- Primary groups (1 SD): VR-favored n ≥ 10, RAVLT-favored n ≥ 10
- Group assignment consistency across thresholds ≥ 70%
- Power analysis shows achieved power values

*Log Validation:*
- Required patterns: "Group assignment complete: N=100"
- Required patterns: "VR-favored: n=XX", "RAVLT-favored: n=XX", "Concordant: n=XX"
- Required patterns: "Power analysis: VR vs RAVLT comparison power=0.XX"
- Forbidden patterns: "ERROR", "empty group", "invalid group"

**Expected Behavior on Validation Failure:**
- Warn if any group n < 10 (insufficient for analysis)
- Document power limitations if achieved power < 0.80
- Log group assignment issues to logs/step03_assign_groups.log

---

### Step 4: Extract Demographic Data
**Dependencies:** Step 3 (group assignments)
**Complexity:** Low (~5 minutes)

**Purpose:** Extract demographic and cognitive variables for group characterization: Age, Education, VR_Experience, plus validation cognitive tests

**Input:**
- data/step03_group_assignments.csv
- data/cache/master.xlsx (demographic and cognitive test data)

**Processing:**
- Merge group assignments with master.xlsx on UID
- Extract primary predictors: Age, Education, VR_Experience
- Extract validation variables: NART (premorbid IQ), BVMT (visual memory)
- Check for missing data patterns across groups
- Compute group-wise descriptive statistics (means, SDs) for each variable
- Flag outliers within each group (values > 3 SD from group mean)
- Transform variables if needed:
  - Age: use as continuous (years)
  - Education: use as continuous (years)
  - VR_Experience: convert to ordinal scale if categorical

**Output:**
- data/step04_demographic_data.csv (UID, Group_1SD, Age, Education, VR_Experience, NART, BVMT)
- data/step04_group_descriptives.txt (means, SDs, missing data by group)

**Validation Requirement:**
Validation tools MUST be used after demographic extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_demographic_data.csv: 100 rows × 7 columns
- Columns: UID (object), Group_1SD (category), Age (float64), Education (float64), VR_Experience (float64), NART (float64), BVMT (float64)
- data/step04_group_descriptives.txt: text file with group-wise statistics

*Value Ranges:*
- Age in [18, 80] (adult participant range)
- Education in [8, 25] (years of formal education)
- VR_Experience in [1, 7] (Likert scale range)
- NART in [70, 130] (standard score range)
- BVMT in [0, 36] (raw score range)

*Data Quality:*
- All 100 participants present with group assignments
- Missing data < 5% per variable per group
- No extreme outliers (>3 SD from group mean) flagged as problematic
- Reasonable between-group variability

*Log Validation:*
- Required patterns: "Demographic extraction complete: N=100"
- Required patterns: "Missing data check: <5% per variable"
- Required patterns: "Group descriptives computed"
- Forbidden patterns: "ERROR", "excessive missing", "merge failed"

**Expected Behavior on Validation Failure:**
- Warn if missing data >10% for any variable
- Flag participants with missing demographic data
- Log data quality issues to logs/step04_extract_demographics.log

---

### Step 5: Group Comparisons with ANOVA
**Dependencies:** Step 4 (demographic data)
**Complexity:** High (~15 minutes including comprehensive statistics)

**Purpose:** Compare discrepancy groups on demographic variables using one-way ANOVA with comprehensive post-hoc testing and effect size estimation

**Input:**
- data/step04_demographic_data.csv

**Processing:**
- For each outcome (Age, Education, VR_Experience):
  - Run one-way ANOVA comparing three groups (VR-favored vs RAVLT-favored vs Concordant)
  - Check ANOVA assumptions:
    - Normality: Shapiro-Wilk test on residuals
    - Homogeneity: Levene's test for equal variances
    - Independence: verified by between-subjects design
    - Outliers: Cook's distance (threshold: 4/n = 0.04)
  - If assumptions violated, apply remedial actions:
    - Normality p < 0.05: Use bootstrap confidence intervals
    - Heteroscedasticity p < 0.05: Apply Welch's ANOVA
    - Outliers Cook's D > 0.04: Report analyses with/without outliers
- Post-hoc pairwise comparisons using Tukey HSD
- Effect size calculations:
  - Eta-squared for omnibus ANOVA effect
  - Cohen's d for pairwise comparisons with 95% CIs
  - Bootstrap CIs for effect sizes (1000 iterations, seed=42)
- Multiple comparison corrections:
  - Family: Within-RQ (3 outcomes × 3 pairwise comparisons = 9 tests)
  - Bonferroni: alpha = 0.05/9 = 0.0056 per test
  - FDR correction using Benjamini-Hochberg procedure
  - Report BOTH uncorrected AND corrected p-values (Decision D068)

**Output:**
- data/step05_anova_results.csv (F-statistics, p-values, effect sizes with CIs)
- data/step05_posthoc_comparisons.csv (pairwise tests with dual p-values)
- data/step05_assumption_checks.txt (normality, homogeneity, outlier diagnostics)

**Validation Requirement:**
Validation tools MUST be used after ANOVA execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_anova_results.csv: 3 rows × 8 columns
- Columns: outcome (object), F_stat (float64), df_num (int), df_den (int), p_uncorrected (float64), p_bonferroni (float64), p_fdr (float64), eta_squared (float64)
- data/step05_posthoc_comparisons.csv: 9 rows × 6 columns (3 outcomes × 3 comparisons)
- Columns: outcome (object), comparison (object), cohens_d (float64), ci_lower (float64), ci_upper (float64), p_tukey (float64)
- data/step05_assumption_checks.txt: text file with diagnostic results

*Value Ranges:*
- F_stat ≥ 0 (F-statistics non-negative)
- p-values in [0, 1] (valid probability range)
- eta_squared in [0, 1] (proportion of variance explained)
- cohens_d in [-3, 3] (reasonable effect size range)

*Data Quality:*
- All 3 outcomes tested (Age, Education, VR_Experience)
- All 9 pairwise comparisons completed
- Bootstrap CIs are valid (ci_lower < cohens_d < ci_upper)
- Dual p-values present for all tests (Decision D068)

*Log Validation:*
- Required patterns: "ANOVA complete: 3 outcomes tested"
- Required patterns: "Assumption checks complete"
- Required patterns: "Post-hoc tests: 9 comparisons"
- Forbidden patterns: "ERROR", "convergence failed", "assumption severe violation"

**Expected Behavior on Validation Failure:**
- Document assumption violations in detail
- Report remedial actions applied
- Log comprehensive diagnostics to logs/step05_anova_comparisons.log

---

### Step 6: Bootstrap Confidence Intervals
**Dependencies:** Step 5 (ANOVA results)
**Complexity:** Medium (~10 minutes)

**Purpose:** Generate bootstrap confidence intervals for group differences to provide robust estimates independent of distributional assumptions

**Input:**
- data/step04_demographic_data.csv
- data/step05_anova_results.csv

**Processing:**
- Participant-level block bootstrap (preserves any within-participant dependencies):
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Resample participants WITH replacement
  - For each iteration: compute group means and pairwise differences
- Generate 95% bootstrap CIs for each pairwise comparison:
  - VR-favored vs RAVLT-favored (primary hypothesis)
  - VR-favored vs Concordant
  - RAVLT-favored vs Concordant
- Compare bootstrap CIs with parametric CIs from Step 5
- Flag significant discrepancies between methods (>20% CI width difference)
- Report bias-corrected and accelerated (BCa) confidence intervals if available

**Output:**
- data/step06_bootstrap_cis.csv (comparison, mean_diff, ci_lower_bootstrap, ci_upper_bootstrap)
- data/step06_bootstrap_summary.txt (method comparison, bias assessment)

**Validation Requirement:**
Validation tools MUST be used after bootstrap execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_bootstrap_cis.csv: 9 rows × 4 columns (3 outcomes × 3 comparisons)
- Columns: comparison (object), mean_diff (float64), ci_lower_bootstrap (float64), ci_upper_bootstrap (float64)
- data/step06_bootstrap_summary.txt: text file with method validation

*Value Ranges:*
- mean_diff values reasonable for demographic variables
- Bootstrap CIs encompass parametric estimates
- CI widths > 0 (non-degenerate intervals)

*Data Quality:*
- All 1000 bootstrap iterations completed successfully
- Bootstrap CIs are well-behaved (no infinite values)
- Method comparison shows consistency (<50% CI width difference)

*Log Validation:*
- Required patterns: "Bootstrap complete: 1000 iterations"
- Required patterns: "Seed set: 42"
- Required patterns: "CIs computed for 9 comparisons"
- Forbidden patterns: "ERROR", "convergence", "infinite CI"

**Expected Behavior on Validation Failure:**
- Report bootstrap failures in detail
- Compare successful iterations if some fail
- Log iteration diagnostics to logs/step06_bootstrap_cis.log

---

### Step 7: Clinical Profiling and Power Analysis
**Dependencies:** Step 6 (bootstrap CIs)
**Complexity:** Medium (~10 minutes)

**Purpose:** Create comprehensive clinical profiles of each discrepancy group and conduct post-hoc power analysis for observed effects

**Input:**
- data/step04_demographic_data.csv
- data/step05_anova_results.csv
- data/step06_bootstrap_cis.csv

**Processing:**
- Clinical group profiling:
  - Create detailed demographic profiles per group
  - Identify characteristic features of each discrepancy type
  - Compute effect size benchmarks (small: d=0.2, medium: d=0.5, large: d=0.8)
  - Flag clinically significant differences (d ≥ 0.5 AND p < corrected alpha)
- Post-hoc power analysis for observed effects:
  - Calculate achieved power for each significant comparison
  - Use observed effect sizes and actual group sizes
  - Alpha level: Bonferroni-corrected (α = 0.0056)
  - Power calculations using statsmodels.stats.power.ttest_power()
- Clinical interpretation guidance:
  - Identify which demographic factors best distinguish groups
  - Provide decision rules for clinical use
  - Acknowledge limitations of current sample size
- Validation cognitive tests analysis:
  - Compare groups on NART and BVMT as convergent validity check
  - Ensure group differences are not simply general cognitive ability

**Output:**
- data/step07_clinical_profiles.csv (group, variable, mean, sd, clinical_significance)
- data/step07_power_analysis.txt (achieved power for observed effects)
- data/step07_clinical_interpretation.txt (decision rules and limitations)

**Validation Requirement:**
Validation tools MUST be used after clinical profiling execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_clinical_profiles.csv: 15 rows × 5 columns (3 groups × 5 variables)
- Columns: group (category), variable (object), mean (float64), sd (float64), clinical_significance (bool)
- data/step07_power_analysis.txt: text file with power calculations
- data/step07_clinical_interpretation.txt: text file with decision rules

*Value Ranges:*
- Power values in [0, 1] (valid range)
- Clinical significance flags appropriate for observed effect sizes
- Group profiles internally consistent

*Data Quality:*
- All three groups characterized on all variables
- Power analysis matches observed effects from Step 5
- Clinical significance corresponds to statistical significance

*Log Validation:*
- Required patterns: "Clinical profiling complete: 3 groups"
- Required patterns: "Power analysis: X significant comparisons"
- Required patterns: "Interpretation guidelines generated"
- Forbidden patterns: "ERROR", "inconsistent profile"

**Expected Behavior on Validation Failure:**
- Report profiling inconsistencies in detail
- Validate power calculations against Step 5 results
- Log clinical interpretation issues to logs/step07_clinical_profiling.log

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt
- data/step01_standardized_scores.csv
- data/step01_descriptive_stats.txt
- data/step02_discrepancy_scores.csv
- data/step02_discrepancy_distribution.txt
- data/step03_group_assignments.csv
- data/step03_group_summary.txt
- data/step04_demographic_data.csv
- data/step04_group_descriptives.txt
- data/step05_anova_results.csv
- data/step05_posthoc_comparisons.csv
- data/step05_assumption_checks.txt
- data/step06_bootstrap_cis.csv
- data/step06_bootstrap_summary.txt
- data/step07_clinical_profiles.csv
- data/step07_power_analysis.txt
- data/step07_clinical_interpretation.txt

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_standardize_scores.log
- logs/step02_compute_discrepancy.log
- logs/step03_assign_groups.log
- logs/step04_extract_demographics.log
- logs/step05_anova_comparisons.log
- logs/step06_bootstrap_cis.log
- logs/step07_clinical_profiling.log

### Plots (EMPTY until rq_plots runs)
Plot source CSVs created in data/:
- data/step02_discrepancy_distribution_plot_data.csv (histogram data)
- data/step05_group_comparisons_plot_data.csv (box plot data)

### Results (EMPTY until rq_results runs)
summary.md created by rq_results summarizing discrepancy patterns and clinical implications

---

## Expected Data Formats

### Step-to-Step Transformations
1. Raw scores → Standardized z-scores (Step 1)
2. Z-scores → Discrepancy scores (Step 2)
3. Discrepancy → Group assignments (Step 3)
4. Groups → Demographics merged (Step 4)
5. Demographics → Statistical comparisons (Step 5)
6. Comparisons → Bootstrap validation (Step 6)
7. All results → Clinical profiles (Step 7)

### Column Naming Conventions
- UID: Participant identifier (consistent across all files)
- REMEMVR_z, RAVLT_z: Standardized scores
- Discrepancy: REMEMVR_z - RAVLT_z
- Group_1SD: Primary group assignment (VR-favored/RAVLT-favored/Concordant)
- p_uncorrected, p_bonferroni, p_fdr: Dual reporting per Decision D068

### Data Type Constraints
- UID: object (string identifier), non-nullable
- Scores: float64, nullable only during merge operations
- Groups: category with defined levels, non-nullable
- P-values: float64 in [0,1], non-nullable
- Effect sizes: float64, nullable if not computable

---

## Cross-RQ Dependencies

**Dependency:** Ch5 omnibus analysis for theta_all scores
- **Source RQ:** Ch5 5.1.1 (most likely source for omnibus theta estimation)
- **Required Files:** Theta scores for all 100 participants
- **File Patterns:** step03_theta_scores.csv, *theta*.csv, *omnibus*.csv
- **Content:** UID column + theta_all column (IRT ability estimates)
- **Status Check:** Ch5 5.1.1 status.yaml must show rq_results: success
- **Fallback:** If exact file not found, search all Ch5 subdirectories for theta outputs

**No Dependencies:** Master.xlsx assumed accessible (standard data source)

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
[Full 4-layer validation structure provided above]

#### Step 1: Extract and Standardize Scores
[Full 4-layer validation structure provided above]

#### Step 2: Compute Discrepancy Scores
[Full 4-layer validation structure provided above]

#### Step 3: Assign Discrepancy Groups
[Full 4-layer validation structure provided above]

#### Step 4: Extract Demographic Data
[Full 4-layer validation structure provided above]

#### Step 5: Group Comparisons with ANOVA
[Full 4-layer validation structure provided above]

#### Step 6: Bootstrap Confidence Intervals
[Full 4-layer validation structure provided above]

#### Step 7: Clinical Profiling and Power Analysis
[Full 4-layer validation structure provided above]

---

## Summary

**Total Steps:** 8 (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** ~45 minutes
**Cross-RQ Dependencies:** Ch5 5.1.1 (theta_all scores)
**Primary Outputs:** Group comparisons with demographic characterization
**Validation Coverage:** 100% (all 8 steps have 4-layer validation requirements)

**Key Hypothesis:** VR-favored individuals will be significantly older than RAVLT-favored individuals, reflecting age-related benefits from environmental scaffolding in VR assessment.

**Critical Methodological Notes:**
- Random seed=42 specified for all randomized procedures (bootstrap, power analysis)
- Dual p-value reporting per Decision D068 (uncorrected + Bonferroni + FDR)
- Sensitivity analysis for threshold robustness (±0.75, ±1.0, ±1.25 SD cutoffs)
- Comprehensive assumption checking with specified remedial actions
- Bootstrap validation for robust confidence intervals
- Post-hoc power analysis for observed effects
- Family-wise error correction across all outcome variables (α = 0.0056)

**Key Improvements from Validation Reports:**
- Added formal power analysis for group comparisons (addresses stats concern #2)
- Expanded multiple comparison correction to include all outcomes (addresses stats concern #1)
- Included sensitivity analysis for cutoff thresholds (addresses stats concern #1)
- Specified remedial actions for assumption violations (addresses stats concern #4)
- Added bootstrap validation as backup for parametric assumptions

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan → creates 3_tools.yaml
3. rq_analysis reads plan + tools → creates 4_analysis.yaml
4. g_code reads analysis → generates executable code

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent v5.1 with enhanced statistical specifications