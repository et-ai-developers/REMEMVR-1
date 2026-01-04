# Analysis Plan: RQ 7.7.2 - Discrepancy Analysis - Who diverges?

**Research Question:** 7.7.2
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

**Pipeline:** Discrepancy Analysis with Group Comparison ANOVA
**Steps:** 8 total analysis steps (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** ~45 minutes

This analysis examines discrepancy patterns between REMEMVR (VR-based memory assessment) and RAVLT (traditional list learning) across 100 participants. Creates standardized discrepancy scores (REMEMVR_z - RAVLT_z) to identify divergent cases and characterizes them demographically using one-way ANOVA with post-hoc comparisons.

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Ch7 family-wise correction: alpha = 0.05/28 = 0.00179 for chapter-level analyses
- Within-RQ family: 3 demographic variables x 3 pairwise comparisons = 9 tests

**Primary Hypothesis:** VR-favored individuals (REMEMVR > RAVLT) will be significantly older than RAVLT-favored individuals, reflecting age-related benefits from environmental scaffolding in VR assessment.

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies

**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 outputs and master.xlsx data exist before proceeding

**Input:**
- Primary: results/ch5/5.1.1/status.yaml (verify rq_results: success)
- Alternative: results/ch5/5.1.1/data/step03_theta_scores.csv (omnibus theta scores)
- Fallback: results/ch5/5.1.1/data/*theta*.{csv,txt} (find theta output files)
- Master data: data/cache/master.xlsx (RAVLT scores + demographics)
- Expected: Omnibus theta_all scores for 100 participants

**Processing:**
- Check Ch5 5.1.1 completed successfully via status.yaml
- Locate omnibus theta scores file (try multiple patterns)
- Verify master.xlsx accessible and contains RAVLT_Total column
- Check for required demographic variables (Age, Education, VR_Experience)
- Log validation results with file paths found
- If Ch5 incomplete: QUIT with "Ch5 5.1.1 theta estimation not complete"
- If master.xlsx missing: QUIT with "Prepared participant data file not accessible"

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Must contain paths to located files and verification status

*Value Ranges:*
- Validation status: "PASS" or "FAIL" for each dependency
- File paths: valid absolute paths to located files
- Participant count: exactly 100 in theta file

*Data Quality:*
- All required dependencies located and verified
- No missing critical files
- File format validation confirms CSV/XLSX structure

*Log Validation:*
- Required patterns: "Dependency validation complete", "Ch5 5.1.1: SUCCESS"
- Required patterns: "master.xlsx: ACCESSIBLE", "RAVLT_Total: FOUND"
- Forbidden patterns: "ERROR", "FAIL", "not found", "missing"

**Expected Behavior on Validation Failure:**
Quit immediately with specific missing dependency, log to logs/step00_validate_dependencies.log

---

### Step 1: Extract and Standardize Scores

**Dependencies:** Step 0 (dependency validation)
**Complexity:** Medium (~8 minutes including bootstrap)

**Purpose:** Load theta scores from Ch5 omnibus analysis and RAVLT scores from dfnonvr.csv, standardize both to z-scores

**Input:**
- results/ch5/5.1.1/data/step03_theta_scores.csv (or located file from Step 0)
- data/cache/master.xlsx (RAVLT_Total scores)
- Expected format: UID, theta_all for REMEMVR; UID, RAVLT_Total for RAVLT

**Processing:**
- Load omnibus theta scores (theta_all column) from Ch5 output
- Extract RAVLT Total scores from dfnonvr.csv
- Merge datasets on UID (participant identifier)
- Standardize REMEMVR scores: REMEMVR_z = (theta - mean(theta)) / sd(theta)
- Standardize RAVLT scores: RAVLT_z = (RAVLT_Total - mean(RAVLT_Total)) / sd(RAVLT_Total)
- Both standardizations based on study sample (N=100) for comparable z-scores
- Verify no missing data for either measure
- Bootstrap 95% CIs for standardization parameters:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Resample participants WITH replacement
  - Extract mean and SD for each iteration
  - CI: percentile method (2.5th, 97.5th percentiles)
- Check normality of both raw and standardized scores (Shapiro-Wilk test)
- Remedial actions if violated:
  - Normality p < 0.05: Note deviation, proceed (z-scores still valid for discrepancy)
  - Outliers (|z| > 3): Document count, report with/without outliers

**Output:**
- data/step01_standardized_scores.csv (UID, theta_raw, RAVLT_raw, REMEMVR_z, RAVLT_z)
- data/step01_standardization_stats.csv (means, SDs, bootstrap CIs)

**Validation Requirement:**
Validation tools MUST be used after score standardization execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_standardized_scores.csv: 100 rows x 5 columns
- Columns: UID (object), theta_raw (float64), RAVLT_raw (float64), REMEMVR_z (float64), RAVLT_z (float64)
- data/step01_standardization_stats.csv: summary statistics with bootstrap CIs

*Value Ranges:*
- Raw theta in [-3, 3] (IRT ability scale)
- Raw RAVLT in [0, 75] (total score across trials)
- Z-scores approximately N(0,1): mean near 0, SD near 1
- Bootstrap CIs: valid intervals (lower < point estimate < upper)

*Data Quality:*
- All 100 participants present (no missing UIDs)
- No missing values in any column
- Z-score distributions approximately normal (mean ± 0.1 of 0, SD ± 0.1 of 1)
- No extreme outliers (|z| > 4)

*Log Validation:*
- Required patterns: "Standardization complete: 100 participants"
- Required patterns: "Bootstrap CI complete: 1000 iterations"
- Required patterns: "REMEMVR_z: mean = 0.00, SD = 1.00"
- Forbidden patterns: "ERROR", "missing data", "convergence failed"

**Expected Behavior on Validation Failure:**
Raise error with specific failure type, log to logs/step01_standardize_scores.log, invoke g_debug

---

### Step 2: Compute Discrepancy Scores

**Dependencies:** Step 1 (standardized scores)
**Complexity:** Low (<5 minutes)

**Purpose:** Calculate discrepancy scores (REMEMVR_z - RAVLT_z) and examine distribution

**Input:**
- data/step01_standardized_scores.csv (standardized z-scores)

**Processing:**
- Calculate discrepancy: Discrepancy = REMEMVR_z - RAVLT_z
- Positive values = VR-favored (better REMEMVR than RAVLT)
- Negative values = RAVLT-favored (better RAVLT than REMEMVR)
- Compute descriptive statistics: mean, SD, range, skewness, kurtosis
- Check discrepancy distribution normality (Shapiro-Wilk test)
- Identify extreme discrepancies (|Discrepancy| > 2 SD) for flagging
- Bootstrap 95% CI for discrepancy mean:
  - Iterations: 1000
  - Random seed: 42
  - Resample participants WITH replacement
  - Extract discrepancy mean for each iteration
  - CI: percentile method (2.5th, 97.5th percentiles)
- Remedial actions if needed:
  - Extreme skewness (|skew| > 2): Document, consider transformation
  - Outliers: Document extreme cases for clinical interpretation

**Output:**
- data/step02_discrepancy_scores.csv (UID, REMEMVR_z, RAVLT_z, Discrepancy)
- data/step02_discrepancy_descriptives.csv (mean, SD, range, bootstrap CIs)

**Validation Requirement:**
Validation tools MUST be used after discrepancy calculation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_discrepancy_scores.csv: 100 rows x 4 columns
- Columns: UID (object), REMEMVR_z (float64), RAVLT_z (float64), Discrepancy (float64)
- data/step02_discrepancy_descriptives.csv: descriptive statistics summary

*Value Ranges:*
- Discrepancy scores in [-4, 4] (difference of z-scores)
- Discrepancy mean near 0 (no systematic bias expected)
- Discrepancy SD in [0.5, 2.0] (reasonable spread for difference scores)

*Data Quality:*
- All 100 participants present
- No missing discrepancy values
- Discrepancy = REMEMVR_z - RAVLT_z verified for all rows
- No computational errors in difference calculation

*Log Validation:*
- Required patterns: "Discrepancy calculation complete: 100 scores"
- Required patterns: "Discrepancy mean = X.XX, SD = X.XX"
- Required patterns: "Bootstrap CI: [X.XX, X.XX]"
- Forbidden patterns: "ERROR", "invalid calculation", "missing values"

**Expected Behavior on Validation Failure:**
Raise error with specific calculation issue, log to logs/step02_compute_discrepancy.log

---

### Step 3: Create Discrepancy Groups

**Dependencies:** Step 2 (discrepancy scores)
**Complexity:** Low (<5 minutes)

**Purpose:** Classify participants into three groups based on discrepancy magnitude using ±1 SD cutoffs

**Input:**
- data/step02_discrepancy_scores.csv (discrepancy scores and descriptives)

**Processing:**
- Extract discrepancy SD from descriptives
- Apply classification criteria:
  - VR-favored: Discrepancy > +1 SD (better REMEMVR than RAVLT)
  - RAVLT-favored: Discrepancy < -1 SD (better RAVLT than REMEMVR)  
  - Concordant: |Discrepancy| <= 1 SD (similar performance)
- Calculate actual group sizes and compare to expected (16, 16, 68)
- Compute group-specific descriptive statistics for discrepancy scores
- Flag if any group has n < 10 (inadequate for group comparisons)
- Sensitivity analysis with alternative cutoffs:
  - 0.75 SD cutoff: calculate alternative group assignments
  - 1.25 SD cutoff: calculate alternative group assignments
  - Document robustness of group differences across thresholds
- Cross-validation of group stability:
  - 5-fold CV with seed=42
  - For each fold: compute group assignments, check consistency
  - Report mean group size stability across folds

**Output:**
- data/step03_group_assignments.csv (UID, Discrepancy, Group)
- data/step03_group_descriptives.csv (group sizes, means, SDs)
- data/step03_sensitivity_analysis.csv (alternative cutoff results)

**Validation Requirement:**
Validation tools MUST be used after group assignment execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_group_assignments.csv: 100 rows x 3 columns
- Columns: UID (object), Discrepancy (float64), Group (object)
- Group values: exactly "VR-favored", "RAVLT-favored", "Concordant"
- data/step03_group_descriptives.csv: 3 rows x 5 columns (group stats)

*Value Ranges:*
- Group sizes: VR-favored and RAVLT-favored >= 10 each
- Concordant group: largest group (expected ~60-80% of sample)
- Total group assignments: exactly 100 participants

*Data Quality:*
- All participants assigned to exactly one group
- No missing group assignments
- Group assignment logic verified (cutoff criteria applied correctly)
- Adequate sample sizes for statistical comparisons

*Log Validation:*
- Required patterns: "Group assignment complete: 100 participants"
- Required patterns: "VR-favored: n=XX", "RAVLT-favored: n=XX", "Concordant: n=XX"
- Required patterns: "Sensitivity analysis complete: 3 cutoffs tested"
- Forbidden patterns: "ERROR", "insufficient group size", "missing assignments"

**Expected Behavior on Validation Failure:**
If any group n < 10: log warning, continue with reduced power acknowledgment

---

### Step 4: Extract Demographic Predictors

**Dependencies:** Steps 0, 3 (group assignments + master.xlsx)
**Complexity:** Low (<5 minutes)

**Purpose:** Extract demographic variables from dfnonvr.csv and merge with group assignments

**Input:**
- data/step03_group_assignments.csv (group classifications)
- data/cache/master.xlsx (demographic variables)

**Processing:**
- Load master.xlsx and extract required variables:
  - Age (years)
  - Education (years)  
  - VR_Experience (self-reported scale)
- Additional cognitive tests for characterization:
  - NART (National Adult Reading Test)
  - BVMT (Brief Visuospatial Memory Test)
- Merge with group assignments on UID
- Check for missing demographic data and report missingness patterns
- Compute descriptive statistics by group for each variable
- Check normality within each group (Shapiro-Wilk test)
- Identify outliers within each group (z > 2.5) for potential exclusion
- Missing data handling:
  - If missingness < 5%: listwise deletion with documentation
  - If missingness 5-15%: multiple imputation consideration
  - If missingness > 15%: exclude variable from primary analysis

**Output:**
- data/step04_demographic_data.csv (UID, Group, Age, Education, VR_Experience, NART, BVMT)
- data/step04_demographic_descriptives.csv (by-group means, SDs, ranges)
- data/step04_missing_data_report.csv (missingness patterns)

**Validation Requirement:**
Validation tools MUST be used after demographic extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_demographic_data.csv: <=100 rows x 7+ columns (may be <100 if missing data)
- Required columns: UID, Group, Age, Education, VR_Experience
- Optional columns: NART, BVMT (if available in master.xlsx)
- data/step04_demographic_descriptives.csv: 3 groups x variables matrix

*Value Ranges:*
- Age in [18, 85] years (adult participants)
- Education in [8, 25] years (realistic education range)
- VR_Experience in [1, 7] (if Likert scale) or [0, 100] (if percentage)
- NART in [0, 50] (standard scoring)
- BVMT in [0, 36] (standard total score)

*Data Quality:*
- Missing data < 15% per variable (acceptable for group comparisons)
- No impossible values (negative ages, extreme outliers)
- Group assignments preserved from Step 3
- Adequate sample sizes maintained after missing data handling

*Log Validation:*
- Required patterns: "Demographic extraction complete"
- Required patterns: "Missing data summary: Age XX%, Education XX%"
- Required patterns: "Final sample size: XX participants"
- Forbidden patterns: "ERROR", "excessive missing data", "merge failed"

**Expected Behavior on Validation Failure:**
If excessive missing data (>15%): exclude variable, proceed with available predictors

---

### Step 5: Group Comparisons with ANOVA

**Dependencies:** Step 4 (demographic data)
**Complexity:** High (~15 minutes including all corrections and bootstrap)

**Purpose:** Compare three groups on demographic variables using one-way ANOVA with comprehensive post-hoc testing

**Input:**
- data/step04_demographic_data.csv (complete demographic data by group)

**Processing:**
- For each demographic variable (Age, Education, VR_Experience):
  
**Primary ANOVA:**
- Implement one-way ANOVA using scipy.stats.f_oneway
- Extract F-statistic, p-value, degrees of freedom
- Compute eta-squared effect size: eta² = SS_between / SS_total
- Bootstrap 95% CI for eta-squared:
  - Iterations: 1000
  - Random seed: 42
  - Resample participants WITH replacement within groups
  - Recompute ANOVA for each iteration
  - CI: percentile method (2.5th, 97.5th percentiles)

**Post-hoc Comparisons:**
- Tukey HSD for all pairwise comparisons:
  - VR-favored vs RAVLT-favored (primary comparison)
  - VR-favored vs Concordant
  - RAVLT-favored vs Concordant
- Cohen's d for each pairwise comparison with bootstrap CIs:
  - Iterations: 1000, seed: 42
  - CI: percentile method
- Report BOTH uncorrected AND corrected p-values (Decision D068)

**Multiple Comparison Corrections:**
- Family: Within-RQ (3 demographic variables x 3 pairwise comparisons = 9 tests)
- Bonferroni: alpha = 0.05/9 = 0.0056 per test
- Also compute FDR using Benjamini-Hochberg procedure
- Report format: p_uncorrected, p_bonferroni, p_fdr for each test

**Assumption Checking:**
- Normality: Shapiro-Wilk test on residuals within each group
- Homoscedasticity: Levene's test for equality of variances
- Independence: Verified by design (between-subjects)
- Outliers: Cook's D > 4/n flagged and reported

**Remedial Actions:**
- Normality p < 0.05: Use bootstrap CIs as primary inference
- Heteroscedasticity p < 0.05: Apply Welch's ANOVA with Games-Howell post-hoc
- Outliers detected: Report results with and without outliers
- If multiple violations: Use non-parametric Kruskal-Wallis with Dunn's post-hoc

**Cross-Validation:**
- 5-fold CV to assess stability of group differences
- Random seed: 42, shuffle: True
- For each fold: fit ANOVA, extract effect sizes
- Report mean and SD of effect sizes across folds
- Flag if CV effect size differs by >0.2 from full sample (instability)

**Power Analysis:**
- Post-hoc power analysis using statsmodels.stats.power
- Given: group sizes, observed effect sizes, alpha = 0.0056
- Calculate: achieved power for each comparison
- Report: minimum detectable effect size at 80% power

**Output:**
- data/step05_anova_results.csv (F-stats, p-values, effect sizes with CIs)
- data/step05_posthoc_comparisons.csv (pairwise comparisons with dual p-values)
- data/step05_assumption_checks.csv (normality, homoscedasticity test results)
- data/step05_power_analysis.csv (achieved power, minimum detectable effects)

**Validation Requirement:**
Validation tools MUST be used after ANOVA analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_anova_results.csv: 3 rows x 8+ columns (one row per variable)
- Columns: variable, F_stat, df1, df2, p_uncorrected, p_bonferroni, eta_squared, eta_CI_lower, eta_CI_upper
- data/step05_posthoc_comparisons.csv: 9 rows (3 variables x 3 comparisons each)
- data/step05_assumption_checks.csv: assumption test results per variable

*Value Ranges:*
- F-statistics > 0 (valid test statistics)
- p-values in [0, 1] (valid probability range)
- eta-squared in [0, 1] (proportion of variance explained)
- Cohen's d in [-3, 3] (reasonable effect size range)
- Power estimates in [0, 1] (valid power range)

*Data Quality:*
- All planned comparisons completed (3 variables x 3 pairwise = 9 tests)
- Dual p-values present for ALL tests (Decision D068)
- Bootstrap CIs valid (lower < point estimate < upper)
- No computational errors or missing results

*Log Validation:*
- Required patterns: "ANOVA complete: 3 demographic variables"
- Required patterns: "Post-hoc complete: 9 pairwise comparisons"
- Required patterns: "Bonferroni correction: alpha = 0.0056"
- Required patterns: "Bootstrap CI complete: 1000 iterations"
- Forbidden patterns: "ERROR", "convergence failed", "insufficient data"

**Expected Behavior on Validation Failure:**
If assumption violations detected: apply remedial procedures, document in logs, continue with robust methods

---

### Step 6: Effect Size Analysis and Clinical Interpretation

**Dependencies:** Step 5 (ANOVA results)
**Complexity:** Medium (~10 minutes including interpretation framework)

**Purpose:** Compute comprehensive effect sizes with clinical interpretation thresholds and generate actionable clinical guidance

**Input:**
- data/step05_anova_results.csv (ANOVA results)
- data/step05_posthoc_comparisons.csv (pairwise comparisons)
- data/step04_demographic_data.csv (raw data for interpretation)

**Processing:**
**Effect Size Computation:**
- For significant ANOVAs (p_bonferroni < 0.0056):
  - Compute omega-squared (unbiased effect size): ω² = (SS_between - df1*MS_error) / (SS_total + MS_error)
  - Bootstrap 95% CI for omega-squared (1000 iterations, seed=42)
- For pairwise comparisons:
  - Hedges' g (bias-corrected Cohen's d) with exact CI formula
  - Glass's delta (using pooled SD from control group = Concordant)
  - Probability of superiority: P(X₁ > X₂) using rank-based calculation

**Clinical Interpretation Framework:**
- Cohen's conventions applied: d < 0.2 (trivial), 0.2-0.5 (small), 0.5-0.8 (medium), >0.8 (large)
- Clinical significance thresholds:
  - Age difference: >5 years considered clinically meaningful
  - Education difference: >2 years considered meaningful  
  - VR Experience: Effect size >0.5 considered meaningful for technology familiarity
- Confidence interval interpretation:
  - CI excludes zero: evidence for group difference
  - CI includes clinically meaningful threshold: practical significance assessment
  
**Group Characterization:**
- Create clinical profiles for each group:
  - VR-favored group: median age, education, VR experience with IQRs
  - RAVLT-favored group: demographic profile and cognitive characteristics
  - Concordant group: baseline reference profile
- Flag extreme cases within groups (>2 SD from group mean) for individual interpretation

**Cross-Validation of Effect Sizes:**
- 5-fold CV assessment (seed=42) of effect size stability
- Report mean effect size and SD across folds
- Flag unstable effects (CV SD > 0.3) as requiring larger samples

**Power Retrospective Analysis:**
- For non-significant results: compute minimum N needed to detect observed effect at 80% power
- For significant results: compute confidence that effect would replicate in new sample
- Document adequacy of current sample for conclusions drawn

**Output:**
- data/step06_effect_sizes.csv (comprehensive effect size metrics with CIs)
- data/step06_clinical_profiles.csv (group characterization data)
- data/step06_clinical_interpretation.txt (actionable interpretation guide)

**Validation Requirement:**
Validation tools MUST be used after effect size analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_effect_sizes.csv: comprehensive effect size results
- Columns: comparison, cohens_d, hedges_g, omega_squared, prob_superiority, CI_lower, CI_upper, clinical_significance
- data/step06_clinical_profiles.csv: 3 rows x demographic summary (one per group)
- data/step06_clinical_interpretation.txt: text file with interpretation framework

*Value Ranges:*
- Effect sizes (d, g) in [-3, 3] (reasonable range)
- Omega-squared in [0, 1] (proportion variance)
- Probability of superiority in [0, 1] (valid probability)
- Clinical significance flags: "Yes", "No", "Unclear" based on thresholds

*Data Quality:*
- Effect sizes computed for all significant comparisons
- CIs properly constructed (lower < point estimate < upper)
- Clinical significance thresholds consistently applied
- No computational errors in effect size formulas

*Log Validation:*
- Required patterns: "Effect size analysis complete"
- Required patterns: "Clinical profiles generated: 3 groups"
- Required patterns: "Interpretation framework applied"
- Forbidden patterns: "ERROR", "invalid effect size", "computation failed"

**Expected Behavior on Validation Failure:**
Document specific failure, attempt alternative effect size calculations, proceed with available metrics

---

### Step 7: Model Diagnostics and Assumptions

**Dependencies:** Steps 5-6 (ANOVA results and effect sizes)
**Complexity:** Medium (~8 minutes including comprehensive checking)

**Purpose:** Comprehensive assumption checking, outlier analysis, and model adequacy assessment with remedial actions

**Input:**
- data/step05_anova_results.csv (ANOVA results)
- data/step04_demographic_data.csv (raw data)
- Residuals and fitted values from ANOVA models

**Processing:**
**Comprehensive Assumption Checking:**
- Normality Assessment (per group, per variable):
  - Shapiro-Wilk test (p > 0.05 for normality)
  - Q-Q plots quantitative assessment (correlation with theoretical quantiles > 0.95)
  - Skewness and kurtosis statistics (|skew| < 2, |kurtosis| < 7 acceptable)
- Homoscedasticity Assessment:
  - Levene's test (p > 0.05 for equal variances)
  - Bartlett's test (if normality met)
  - Visual inspection: ratio of largest to smallest group variance < 4
- Independence Verification:
  - Design structure confirmation (between-subjects)
  - Durbin-Watson test if sequential IDs suggest ordering

**Outlier Detection and Analysis:**
- Univariate outliers (per group, per variable):
  - Z-scores > |3| flagged as extreme
  - Tukey's fences: Q1 - 1.5*IQR and Q3 + 1.5*IQR
  - Document outlier count and group membership
- Multivariate outliers:
  - Mahalanobis distance > critical chi-square value
  - Cook's distance > 4/n for influential cases
- Impact analysis: 
  - Rerun primary ANOVAs with outliers removed
  - Compare effect sizes with and without outliers
  - Document influence on conclusions

**Sample Size Adequacy Assessment:**
- Post-hoc power analysis using actual group sizes and effect sizes:
  - Alpha: 0.0056 (Bonferroni-corrected)
  - Effect size: observed from Step 5
  - Software: statsmodels.stats.power.FTestAnovaPower()
- Minimum detectable effect size at 80% power given current sample
- Adequacy assessment: power ≥ 0.80 considered adequate

**Remedial Actions (Applied as Needed):**
- For normality violations (p < 0.05):
  - Mild violation: Robust standard errors, bootstrap CIs (primary)
  - Severe violation: Transform data (log, sqrt) or use Kruskal-Wallis
- For heteroscedasticity (p < 0.05):
  - Apply Welch's ANOVA (unequal variances assumed)
  - Use Games-Howell post-hoc (no equal variance assumption)
- For influential outliers (Cook's D > 4/n):
  - Report results WITH and WITHOUT outliers
  - Use robust methods (trimmed means, Winsorizing)
- For low power (< 0.80):
  - Acknowledge limitation in interpretation
  - Report minimum detectable effect for adequacy assessment

**Robustness Assessment:**
- Non-parametric alternatives:
  - Kruskal-Wallis test for each variable
  - Dunn's test for post-hoc comparisons
  - Compare parametric vs non-parametric conclusions
- Bootstrap validation:
  - 1000 iterations (seed=42) of entire analysis pipeline
  - Report stability of significant findings
  - Flag results that lose significance in >10% of bootstrap samples

**Output:**
- data/step07_assumption_checks.csv (detailed assumption test results)
- data/step07_outlier_analysis.csv (outlier identification and impact)
- data/step07_power_analysis.csv (sample adequacy assessment)
- data/step07_robustness_tests.csv (non-parametric alternatives)
- data/step07_remedial_actions.txt (applied corrections and rationale)

**Validation Requirement:**
Validation tools MUST be used after diagnostic analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_assumption_checks.csv: assumption test results per variable per group
- Columns: variable, group, n, shapiro_W, shapiro_p, levene_F, levene_p, skewness, kurtosis
- data/step07_outlier_analysis.csv: outlier identification results
- data/step07_power_analysis.csv: power calculations per comparison
- data/step07_robustness_tests.csv: non-parametric test results

*Value Ranges:*
- Test statistics: appropriate ranges per test type
- p-values in [0, 1]
- Power estimates in [0, 1]
- Outlier counts: 0 to reasonable percentage (<10% of sample)
- Effect size comparisons: reasonable stability (difference <0.3)

*Data Quality:*
- Assumption tests completed for all variables and groups
- Outlier analysis systematic and documented
- Power analysis matches sample sizes used
- Remedial actions clearly documented with rationale

*Log Validation:*
- Required patterns: "Assumption checking complete: normality, homoscedasticity"
- Required patterns: "Outlier analysis complete: XX outliers detected"
- Required patterns: "Power analysis: achieved power = X.XX"
- Required patterns: "Robustness assessment complete"
- Forbidden patterns: "ERROR", "test failed", "insufficient data"

**Expected Behavior on Validation Failure:**
Document specific assumption violations, apply appropriate remedial actions, continue with robust methods

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)

**Step-wise progression:**
- data/step00_dependency_validation.txt: Prerequisite verification
- data/step01_standardized_scores.csv: Z-score transformations (100 rows x 5 cols)
- data/step01_standardization_stats.csv: Bootstrap CIs for standardization
- data/step02_discrepancy_scores.csv: Discrepancy calculations (100 rows x 4 cols)
- data/step02_discrepancy_descriptives.csv: Discrepancy distribution summary
- data/step03_group_assignments.csv: Tri-categorical groups (100 rows x 3 cols)
- data/step03_group_descriptives.csv: Group characterization (3 rows x stats)
- data/step03_sensitivity_analysis.csv: Alternative cutoff validation
- data/step04_demographic_data.csv: Merged demographics (≤100 rows x 7+ cols)
- data/step04_demographic_descriptives.csv: By-group demographic summaries
- data/step04_missing_data_report.csv: Missingness patterns
- data/step05_anova_results.csv: Primary ANOVA results (3 rows x 8+ cols)
- data/step05_posthoc_comparisons.csv: Pairwise comparisons (9 rows x multiple cols)
- data/step05_assumption_checks.csv: ANOVA assumption test results
- data/step05_power_analysis.csv: Power calculations per comparison
- data/step06_effect_sizes.csv: Comprehensive effect size metrics
- data/step06_clinical_profiles.csv: Group characterization data (3 rows)
- data/step06_clinical_interpretation.txt: Clinical interpretation framework
- data/step07_assumption_checks.csv: Detailed assumption validation
- data/step07_outlier_analysis.csv: Outlier identification and impact
- data/step07_power_analysis.csv: Final sample adequacy assessment
- data/step07_robustness_tests.csv: Non-parametric alternative results
- data/step07_remedial_actions.txt: Applied corrections documentation

### Logs (ONLY execution logs)

- logs/step00_validate_dependencies.log
- logs/step01_standardize_scores.log
- logs/step02_compute_discrepancy.log
- logs/step03_create_groups.log
- logs/step04_extract_demographics.log
- logs/step05_group_comparisons.log
- logs/step06_effect_sizes.log
- logs/step07_model_diagnostics.log

### Plots (EMPTY until rq_plots runs)

**Note:** Plot source CSVs created in data/ folder for rq_plots consumption:
- data/step02_discrepancy_plot_data.csv: For discrepancy distribution histogram
- data/step04_demographic_plot_data.csv: For group comparison box plots
- data/step05_anova_plot_data.csv: For effect size forest plots
- data/step07_diagnostic_plot_data.csv: For assumption checking plots

### Results (EMPTY until rq_results runs)

**Note:** summary.md will be created by rq_results synthesizing all analysis outputs

---

## Expected Data Formats

### Step-to-Step Transformations

**Data Flow:**
1. Ch5 theta scores + master.xlsx RAVLT → standardized z-scores
2. Z-scores → discrepancy scores (difference)
3. Discrepancy scores → tri-categorical groups (±1 SD cutoffs)
4. Groups + master.xlsx → demographic characterization
5. Groups + demographics → ANOVA comparisons
6. ANOVA results → effect sizes and clinical interpretation
7. All outputs → diagnostic validation and robustness checks

### Column Naming Conventions

**Standardized Identifiers:**
- UID: Participant identifier (consistent across all files)
- Group: "VR-favored", "RAVLT-favored", "Concordant" (exact strings)

**Score Variables:**
- theta_raw: Raw omnibus theta from Ch5 (IRT scale)
- RAVLT_raw: Raw RAVLT Total score
- REMEMVR_z, RAVLT_z: Standardized z-scores
- Discrepancy: REMEMVR_z - RAVLT_z

**Statistical Results:**
- F_stat, p_uncorrected, p_bonferroni, p_fdr: ANOVA results with dual reporting
- cohens_d, hedges_g, omega_squared: Effect size metrics
- CI_lower, CI_upper: Bootstrap confidence intervals

### Data Type Constraints

**Identifier Variables:**
- UID: object (string), non-nullable
- Group: object (categorical), non-nullable, limited to 3 values

**Score Variables:**
- All score variables: float64, nullable only if missing data documented
- Z-scores: approximately N(0,1) distribution expected
- Discrepancy: reasonable range [-4, 4] for difference of z-scores

**Statistical Variables:**
- p-values: float64 in [0, 1], non-nullable
- Effect sizes: float64, reasonable ranges per metric type
- CIs: float64, lower < upper constraint

---

## Cross-RQ Dependencies

### Primary Dependencies

**Ch5 5.1.1 Omnibus Theta Scores:**
- Required: Completed IRT calibration with omnibus theta_all scores
- Expected file: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative paths: results/ch5/5.1.1/data/*theta*.csv
- Content: UID and omnibus theta scores for 100 participants
- Verification: Check status.yaml shows rq_results: success

**Master Dataset:**
- Required: data/cache/master.xlsx with RAVLT and demographic data
- Expected variables: RAVLT_Total, Age, Education, VR_Experience
- Optional variables: NART, BVMT for additional characterization
- Verification: File exists and contains required columns

### Fallback Strategies

**If Ch5 5.1.1 incomplete:**
- Check for alternative Ch5 omnibus analyses (5.1.2, 5.2.1)
- Look for theta_all scores in any Ch5 output
- QUIT if no omnibus scores available with clear error message

**If master.xlsx inaccessible:**
- Check alternative paths: data/raw/master.xlsx, cache/master_backup.xlsx
- QUIT if demographic data unavailable (core requirement for RQ)

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
[4-layer validation structure as specified above]

#### Step 1: Extract and Standardize Scores
[4-layer validation structure as specified above]

#### Step 2: Compute Discrepancy Scores  
[4-layer validation structure as specified above]

#### Step 3: Create Discrepancy Groups
[4-layer validation structure as specified above]

#### Step 4: Extract Demographic Predictors
[4-layer validation structure as specified above]

#### Step 5: Group Comparisons with ANOVA
[4-layer validation structure as specified above]

#### Step 6: Effect Size Analysis
[4-layer validation structure as specified above]

#### Step 7: Model Diagnostics
[4-layer validation structure as specified above]

### Validation Coverage Summary

**Statistical Implementation Requirements (v5.1):**
- ✅ Random seed=42 specified for ALL randomized procedures
- ✅ Bootstrap: 1000 iterations, participant-level resampling, percentile CIs
- ✅ Cross-validation: 5-fold, seed=42, shuffle=True, stability assessment
- ✅ Power analysis: Post-hoc with actual parameters, minimum detectable effects
- ✅ Multiple comparisons: Family-wise Bonferroni + FDR, dual reporting (D068)
- ✅ Assumption violations: Comprehensive remedial actions specified
- ✅ Cross-RQ dependencies: Primary + fallback paths with verification

**4-Layer Validation Architecture:**
- ✅ ALL 8 steps have mandatory validation requirements
- ✅ Output Files: Exact paths, dimensions, data types specified
- ✅ Value Ranges: Scientific bounds with justification
- ✅ Data Quality: Missing data tolerance, distribution checks
- ✅ Log Validation: Required/forbidden patterns per step

---

## Summary

**Total Steps:** 8 (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** ~45 minutes total
**Cross-RQ Dependencies:** Ch5 5.1.1 omnibus theta scores (primary), master.xlsx demographics
**Primary Outputs:** Group characterization via ANOVA with comprehensive effect size analysis
**Validation Coverage:** 100% (all 8 steps have 4-layer validation requirements)

**Key Hypothesis:** VR-favored individuals (REMEMVR > RAVLT) will be significantly older than RAVLT-favored individuals (RAVLT > REMEMVR), reflecting age-related benefits from environmental scaffolding in VR assessment.

**Critical Methodological Notes:**
- Standardization uses study sample (N=100) to ensure comparable z-scores between measures
- ±1 SD cutoffs create clinically interpretable groups with adequate sample sizes
- Sensitivity analysis validates robustness across alternative cutoff thresholds  
- Comprehensive assumption checking with specified remedial actions ensures methodological rigor
- Dual p-value reporting (uncorrected + corrected) per Decision D068
- Bootstrap CIs provide robust inference under assumption violations
- Cross-validation assesses stability and generalizability of group differences

**Statistical Rigor (v5.1 Enhanced):**
- All randomized procedures use seed=42 for reproducibility
- Multiple comparison corrections applied at within-RQ level (9 tests)
- Power analysis validates sample adequacy for detecting medium effects
- Remedial actions specified for each assumption violation type
- Non-parametric alternatives computed for robustness validation

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan → creates 3_tools.yaml (specify discrepancy analysis tools)
3. rq_analysis reads plan + tools → creates 4_analysis.yaml
4. g_code reads analysis → generates executable code with statistical specifications

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent with enhanced v5.1 specifications