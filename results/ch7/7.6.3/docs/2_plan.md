# Analysis Plan: RQ 7.6.3 - ICC slope replication across domains

**Research Question:** 7.6.3
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines individual differences in forgetting slopes computed separately for What, Where, and When domains. Tests whether between-person variance in forgetting rates (ICC_slope) is consistent across episodic memory domains, providing a replication analysis to determine domain-generality versus domain-specificity of individual differences in forgetting.

**Pipeline:** Variance component analysis (ICC computation) with bootstrap confidence intervals and domain comparisons
**Steps:** 8 total analysis steps (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** ~45 minutes (including 1000-iteration bootstrap procedures)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Statistical specifications enhanced per v5.1 requirements

**Critical Dependencies:**
- Ch5 5.2.1 (What domain slopes)
- Ch5 5.2.2 (Where domain slopes) 
- Ch5 5.2.3 (When domain slopes)

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 domain analysis outputs exist before proceeding with ICC analysis

**Input:**
- Primary: results/ch5/5.2.1/data/*slopes*.csv (What domain slopes)
- Primary: results/ch5/5.2.2/data/*slopes*.csv (Where domain slopes)
- Primary: results/ch5/5.2.3/data/*slopes*.csv (When domain slopes)
- Alternative: results/ch5/5.2.X/data/step##_participant_slopes.csv
- Fallback: results/ch5/5.2.X/data/*participant*.{csv,txt,rds}
- Expected content: N=100 participant-level slope estimates with UIDs
- If none found: QUIT with "Ch5 domain analyses (5.2.1, 5.2.2, 5.2.3) outputs not found"

**Processing:**
- Verify Ch5 5.2.1, 5.2.2, 5.2.3 status = success in respective status.yaml files
- Search for slope files using multiple patterns
- Verify file format contains UID and slope columns
- Check participant overlap across domains (expect N=100 common participants)
- Verify modeling consistency (identical LMM specifications across domains)
- Log all validation results with file paths found

**Output:**
- data/step00_dependency_validation.txt (validation summary)

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation summary
- Contains paths to 3 slope files (What, Where, When)
- File size >500 bytes (sufficient detail)

*Value Ranges:*
- Found files: 3 (one per domain)
- Participant overlap: 100 (complete overlap required)
- File formats: consistent across domains

*Data Quality:*
- All 3 domains successfully located
- No missing domain files
- Consistent participant IDs across domains
- Modeling specifications identical per validation

*Log Validation:*
- Required: "Dependency validation PASS"
- Required: "Found 3 domain slope files"
- Required: "100 participants verified across domains"
- Forbidden: "ERROR", "MISSING", "inconsistent"

**Expected Behavior on Validation Failure:**
Raise error specifying which domain files missing, log to logs/step00_validate_dependencies.log, quit immediately and invoke g_debug for manual file location.

---

### Step 1: Extract and Merge Domain-Specific Slopes
**Dependencies:** Step 0 (validated Ch5 outputs)
**Complexity:** Low (~5 minutes)

**Purpose:** Load participant-level slopes from Ch5 domain analyses and create unified dataset for ICC analysis

**Input:**
- data/step00_dependency_validation.txt (file path references)
- Ch5 slope files as identified in Step 0
- Expected format: UID, slope, se_slope (minimum columns)

**Processing:**
- Load slope data from all 3 domain files
- Standardize column names: UID, slope_what, slope_where, slope_when
- Merge datasets on UID (inner join to ensure complete cases)
- Add slope standard errors if available: se_what, se_where, se_when
- Verify N=100 participants with complete slope data
- Check for duplicate UIDs within domains
- Compute descriptive statistics for each domain's slopes
- Flag participants with extreme slopes (|z| > 3.29, p < 0.001) for diagnostics

**Output:**
- data/step01_domain_slopes.csv (merged slope dataset)

**Validation Requirement:**
Validation tools MUST be used after slope extraction and merging.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_domain_slopes.csv: 100 rows x 4+ columns
- Columns: UID (object), slope_what (float64), slope_where (float64), slope_when (float64)
- Optional columns: se_what, se_where, se_when if available

*Value Ranges:*
- slope_what in [-0.8, 0.2] (typical forgetting slopes)
- slope_where in [-0.8, 0.2] (typical forgetting slopes)
- slope_when in [-0.8, 0.2] (typical forgetting slopes)
- All slopes negative (forgetting over time)

*Data Quality:*
- Exactly 100 participants (complete cases only)
- No missing slope values (NaN count = 0)
- No duplicate UIDs
- Standard errors positive if included

*Log Validation:*
- Required: "Merged slopes: 100 participants"
- Required: "Complete cases verified"
- Required: "Domain slopes loaded successfully"
- Forbidden: "ERROR", "missing", "duplicate UID"

**Expected Behavior on Validation Failure:**
Report specific data quality issues, log to logs/step01_extract_slopes.log, quit if <100 participants or missing data detected.

---

### Step 2: Compute ICC for Each Domain
**Dependencies:** Step 1 (merged slope data)
**Complexity:** Medium (~8 minutes including variance component analysis)

**Purpose:** Calculate ICC(1,1) values for each domain's slope variance to quantify between-person variance

**Input:**
- data/step01_domain_slopes.csv (participant slope data)

**Processing:**
- For each domain (What, Where, When):
  - Extract slope values for N=100 participants
  - Compute total variance: var_total = var(slopes)
  - Estimate between-person variance using variance component analysis
  - Use ICC(1,1) formulation (single measurement, absolute agreement model)
  - Implementation: tools.variance_decomposition.compute_icc_from_variance_components
  - Extract ICC value and confidence bounds if available
- Compute descriptive statistics for each domain's ICC
- Document which ICC formulation used (ICC(1,1))
- Store raw variance components for bootstrap resampling

**Output:**
- data/step02_icc_estimates.csv (ICC values by domain)
- data/step02_variance_components.csv (raw variance estimates)

**Validation Requirement:**
Validation tools MUST be used after ICC computation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_icc_estimates.csv: 3 rows x 4 columns
- Columns: domain, icc_value, variance_between, variance_total
- data/step02_variance_components.csv: 3 rows x 5 columns

*Value Ranges:*
- icc_value in [0, 1] (valid ICC range)
- icc_what expected 0.15-0.30 (realistic individual differences)
- icc_where expected 0.15-0.30 (realistic individual differences)
- icc_when expected 0.05-0.20 (potentially lower due to measurement issues)
- variance_between > 0, variance_total > 0

*Data Quality:*
- All 3 domains present (What, Where, When)
- No NaN ICC values
- variance_between <= variance_total (mathematical constraint)
- ICC calculations consistent with variance ratios

*Log Validation:*
- Required: "ICC computed: 3 domains"
- Required: "ICC formulation: ICC(1,1)"
- Required: "Variance components extracted"
- Forbidden: "ERROR", "negative variance", "ICC > 1"

**Expected Behavior on Validation Failure:**
Report invalid ICC values or variance estimates, log to logs/step02_compute_icc.log, check for degenerate variance cases.

---

### Step 3: Bootstrap Confidence Intervals for ICC Estimates
**Dependencies:** Step 2 (ICC estimates and variance components)
**Complexity:** High (~15 minutes for 1000-iteration bootstrap)

**Purpose:** Compute 95% confidence intervals for ICC estimates using participant-level bootstrap resampling

**Input:**
- data/step01_domain_slopes.csv (original slope data)
- data/step02_variance_components.csv (baseline variance estimates)

**Processing:**
- Implement participant-level block bootstrap (preserves within-participant correlation)
- Bootstrap specifications per v5.1 requirements:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Resampling unit: participants WITH replacement
  - For each bootstrap iteration:
    - Resample 100 participants from original dataset with replacement
    - Compute ICC(1,1) for each domain using resampled data
    - Store ICC estimates for distribution analysis
- CI computation: percentile method (2.5th, 97.5th percentiles for 95% CI)
- Consider bias-corrected accelerated (BCa) method if available
- Monitor bootstrap convergence:
  - Track successful iterations (expect >95% success rate)
  - Flag When domain if ICC near zero causes convergence issues
  - Report bootstrap bias (difference between bootstrap mean and original ICC)
- Sensitivity analysis: increase to 5000 iterations if ICC estimates near boundaries (0 or 1)

**Output:**
- data/step03_bootstrap_cis.csv (confidence intervals by domain)
- data/step03_bootstrap_distributions.csv (raw bootstrap samples)

**Validation Requirement:**
Validation tools MUST be used after bootstrap completion.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_bootstrap_cis.csv: 3 rows x 6 columns
- Columns: domain, icc_original, icc_boot_mean, ci_lower, ci_upper, boot_bias
- data/step03_bootstrap_distributions.csv: 3000 rows x 2 columns (1000 iterations x 3 domains)

*Value Ranges:*
- ci_lower in [0, 1], ci_upper in [0, 1]
- ci_lower < icc_original < ci_upper (confidence interval contains original estimate)
- boot_bias in [-0.1, 0.1] (acceptable bootstrap bias)
- Bootstrap success rate >95% for all domains

*Data Quality:*
- All 1000 bootstrap iterations completed successfully
- No NaN values in confidence intervals
- CI widths reasonable (0.05-0.30 typical for ICC)
- Bootstrap distributions approximately normal

*Log Validation:*
- Required: "Bootstrap complete: 1000 iterations"
- Required: "Success rate >95% all domains"
- Required: "CIs computed: percentile method"
- Forbidden: "convergence failed", "too many NaN"

**Expected Behavior on Validation Failure:**
Report failed bootstrap iterations or invalid CIs, check for When domain convergence issues due to low ICC, increase iteration count if needed.

---

### Step 4: Statistical Comparisons Between Domains
**Dependencies:** Step 3 (bootstrap confidence intervals)
**Complexity:** Medium (~8 minutes including effect size calculations)

**Purpose:** Test pairwise differences between domain ICC estimates and compute effect sizes

**Input:**
- data/step03_bootstrap_distributions.csv (raw bootstrap samples by domain)
- data/step02_icc_estimates.csv (original ICC values)

**Processing:**
- Pairwise comparisons using bootstrap samples:
  - What vs Where: compute difference distribution (ICC_what - ICC_where)
  - What vs When: compute difference distribution (ICC_what - ICC_when)  
  - Where vs When: compute difference distribution (ICC_where - ICC_when)
- For each comparison:
  - Calculate difference for each bootstrap iteration
  - Compute 95% CI for difference using percentile method
  - Test H0: difference = 0 by checking if 95% CI excludes zero
  - Calculate p-value as proportion of bootstrap differences crossing zero
- Effect size calculation:
  - Cohen's d for ICC differences (standardized difference)
  - Use pooled variance estimate from bootstrap distributions
  - Implementation: tools.analysis_lmm.compute_effect_sizes_cohens
- Multiple comparison correction per v5.1 requirements:
  - Family: Within-RQ (3 pairwise comparisons)
  - Bonferroni: alpha = 0.05/3 = 0.0167 per test
  - Also compute FDR using Benjamini-Hochberg procedure
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
  - Format: p_uncorrected, p_bonferroni, p_fdr

**Output:**
- data/step04_pairwise_comparisons.csv (domain comparison statistics)

**Validation Requirement:**
Validation tools MUST be used after statistical comparisons.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_pairwise_comparisons.csv: 3 rows x 8 columns
- Columns: comparison, diff_mean, diff_ci_lower, diff_ci_upper, cohens_d, p_uncorrected, p_bonferroni, p_fdr

*Value Ranges:*
- diff_mean in [-1, 1] (valid ICC difference range)
- cohens_d in [-3, 3] (reasonable effect size range)
- p_uncorrected, p_bonferroni, p_fdr in [0, 1] (valid probability range)
- p_bonferroni >= p_uncorrected (mathematical constraint)

*Data Quality:*
- All 3 pairwise comparisons present
- Confidence intervals symmetric around difference means
- Effect sizes consistent with difference magnitudes
- Multiple comparison corrections applied appropriately

*Log Validation:*
- Required: "Pairwise comparisons: 3 tests completed"
- Required: "Multiple corrections applied"
- Required: "Effect sizes computed"
- Forbidden: "ERROR", "invalid p-value"

**Expected Behavior on Validation Failure:**
Report invalid test statistics or effect sizes, verify bootstrap difference calculations, check multiple comparison logic.

---

### Step 5: Outlier Analysis and Robustness Checks
**Dependencies:** Steps 1-4 (slope data and ICC estimates)
**Complexity:** Medium (~6 minutes)

**Purpose:** Identify outliers in domain-specific slopes and assess impact on ICC estimates

**Input:**
- data/step01_domain_slopes.csv (original slope data)
- data/step02_icc_estimates.csv (baseline ICC estimates)

**Processing:**
- Outlier detection for each domain's slopes:
  - Z-score method: |z| > 3.29 (p < 0.001 threshold)
  - Robust outlier detection: modified z-score using MAD
  - Document outlier participants by UID and domain
- Impact assessment:
  - Re-compute ICC estimates excluding identified outliers
  - Compare original vs outlier-excluded ICC values
  - Calculate change in ICC (delta_ICC) for each domain
  - Determine if conclusions change with/without outliers
- Assumption checking:
  - Normality: Shapiro-Wilk test on slope distributions by domain
  - Equal variance: Levene's test across domains
  - Independence: acknowledge within-participant dependencies
- Remedial actions if violations detected:
  - Normality p < 0.05: report bootstrap CIs as primary (already implemented)
  - Heteroscedasticity detected: acknowledge in limitations
  - Severe outliers (delta_ICC > 0.05): report both estimates

**Output:**
- data/step05_outlier_analysis.csv (outlier diagnostics and impact)
- data/step05_robustness_checks.csv (ICC estimates with/without outliers)

**Validation Requirement:**
Validation tools MUST be used after outlier analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_outlier_analysis.csv: variable rows x 4 columns
- Columns: domain, UID, z_score, outlier_type (z-score or MAD)
- data/step05_robustness_checks.csv: 3 rows x 4 columns
- Columns: domain, icc_original, icc_no_outliers, delta_icc

*Value Ranges:*
- z_score with |z| > 3.29 for flagged outliers
- delta_icc in [-0.2, 0.2] (reasonable ICC change)
- icc_no_outliers in [0, 1] (valid ICC range)

*Data Quality:*
- Outlier count reasonable (<10% of participants per domain)
- Delta ICC values consistent with outlier magnitude
- All domains represented in robustness checks

*Log Validation:*
- Required: "Outlier analysis complete"
- Required: "Robustness checks performed"
- Required: "Assumption checks completed"
- Forbidden: "ERROR", "too many outliers"

**Expected Behavior on Validation Failure:**
Report excessive outliers or invalid robustness calculations, review outlier detection thresholds if >20% flagged.

---

### Step 6: Split-Half Reliability Analysis
**Dependencies:** Step 1 (merged slope data)
**Complexity:** Medium (~8 minutes)

**Purpose:** Assess reliability of ICC estimates using split-half cross-validation

**Input:**
- data/step01_domain_slopes.csv (complete slope dataset)

**Processing:**
- Cross-validation implementation per v5.1 requirements:
  - Random split of N=100 participants into two halves (n=50 each)
  - Random seed: 42 for reproducibility
  - Stratification: None (simple random split for reliability assessment)
  - For each half: compute ICC(1,1) for each domain
  - Repeat split-half procedure 100 times with different random splits
- Reliability calculation:
  - Correlation between Half1 and Half2 ICC estimates across splits
  - Report Pearson r and 95% CI for reliability
  - Target: r > 0.70 for acceptable reliability
  - Calculate split-half reliability separately for each domain
- Stability assessment:
  - Mean ICC difference between halves
  - Standard deviation of ICC estimates across splits
  - Flag domains with poor reliability (r < 0.50)

**Output:**
- data/step06_split_half_reliability.csv (reliability statistics by domain)

**Validation Requirement:**
Validation tools MUST be used after reliability analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_split_half_reliability.csv: 3 rows x 6 columns
- Columns: domain, reliability_r, reliability_ci_lower, reliability_ci_upper, mean_diff, sd_icc

*Value Ranges:*
- reliability_r in [-1, 1] (valid correlation range)
- Expected reliability_r > 0.50 for What/Where domains
- mean_diff in [-0.2, 0.2] (small systematic bias)
- sd_icc > 0 (positive standard deviation)

*Data Quality:*
- All 3 domains analyzed for reliability
- Reliability estimates based on 100 random splits
- Confidence intervals exclude impossible values

*Log Validation:*
- Required: "Split-half reliability: 100 splits completed"
- Required: "Reliability computed: 3 domains"
- Required: "Cross-validation analysis complete"
- Forbidden: "ERROR", "failed split"

**Expected Behavior on Validation Failure:**
Report poor reliability estimates, check for degenerate splits with insufficient variance, verify random splitting procedure.

---

### Step 7: Power Analysis and Sensitivity Assessment
**Dependencies:** Steps 2-4 (ICC estimates and comparisons)
**Complexity:** Medium (~5 minutes)

**Purpose:** Conduct post-hoc power analysis for ICC comparisons and sensitivity analysis for effect detection

**Input:**
- data/step02_icc_estimates.csv (observed ICC values)
- data/step04_pairwise_comparisons.csv (observed effect sizes)

**Processing:**
- Power analysis per v5.1 requirements:
  - Type: Post-hoc power analysis for ICC differences
  - Given: N=100 participants, observed effect sizes from Step 4
  - Alpha level: 0.0167 (Bonferroni-corrected per-test alpha)
  - Calculate achieved power for observed ICC differences
  - Use bootstrap-based power estimation (Monte Carlo approach)
  - Target: power > 0.80 for medium effect sizes (Cohen's d = 0.5)
- Sensitivity analysis:
  - Minimum detectable ICC difference at 80% power
  - Sample size required for detecting small differences (d = 0.2)
  - Effect of ICC magnitude on power (low vs high ICC values)
- Power assessment by comparison:
  - What vs Where: power for detecting observed difference
  - What vs When: power for detecting observed difference  
  - Where vs When: power for detecting observed difference
- Interpretation guidance:
  - If power < 0.80: acknowledge limitation in detecting small differences
  - Report confidence in null findings based on achieved power

**Output:**
- data/step07_power_analysis.csv (power and sensitivity results)

**Validation Requirement:**
Validation tools MUST be used after power analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_power_analysis.csv: 3 rows x 5 columns  
- Columns: comparison, observed_d, achieved_power, min_detectable_d, required_n_d02

*Value Ranges:*
- achieved_power in [0, 1] (valid power range)
- min_detectable_d > 0 (positive effect size)
- required_n_d02 > 100 (larger N needed for small effects)
- observed_d consistent with Step 4 calculations

*Data Quality:*
- Power calculations for all 3 pairwise comparisons
- Sensitivity analysis provides realistic estimates
- Required sample sizes reasonable for effect detection

*Log Validation:*
- Required: "Power analysis complete: 3 comparisons"
- Required: "Sensitivity analysis performed"
- Required: "Effect detection thresholds calculated"
- Forbidden: "ERROR", "impossible power"

**Expected Behavior on Validation Failure:**
Report invalid power calculations, verify effect size inputs from Step 4, check power analysis assumptions.

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (dependency verification)
- data/step01_domain_slopes.csv (merged slope dataset: 100 x 4+ columns)
- data/step02_icc_estimates.csv (ICC values: 3 x 4 columns)
- data/step02_variance_components.csv (variance estimates: 3 x 5 columns)
- data/step03_bootstrap_cis.csv (confidence intervals: 3 x 6 columns)
- data/step03_bootstrap_distributions.csv (bootstrap samples: 3000 x 2 columns)
- data/step04_pairwise_comparisons.csv (domain comparisons: 3 x 8 columns)
- data/step05_outlier_analysis.csv (outlier diagnostics: variable x 4 columns)
- data/step05_robustness_checks.csv (robustness results: 3 x 4 columns)
- data/step06_split_half_reliability.csv (reliability statistics: 3 x 6 columns)
- data/step07_power_analysis.csv (power results: 3 x 5 columns)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_slopes.log
- logs/step02_compute_icc.log
- logs/step03_bootstrap_cis.log
- logs/step04_pairwise_comparisons.log
- logs/step05_outlier_analysis.log
- logs/step06_split_half_reliability.log
- logs/step07_power_analysis.log

### Plots (EMPTY until rq_plots runs)
- Plot source CSVs created in data/ with prefix step##_*_plot_data.csv
- ICC comparison plot data: data/step##_icc_comparison_plot_data.csv
- Slope distribution plot data: data/step##_slope_distributions_plot_data.csv

### Results (EMPTY until rq_results runs)
- results/summary.md created by rq_results agent

---

## Expected Data Formats

### Step-to-Step Transformations
- **Step 0 -> Step 1:** File path validation -> Slope data loading
- **Step 1 -> Step 2:** Merged slopes -> ICC computation
- **Step 2 -> Step 3:** ICC estimates -> Bootstrap confidence intervals
- **Step 3 -> Step 4:** Bootstrap samples -> Statistical comparisons
- **Steps 1-4 -> Step 5:** Combined data -> Outlier analysis
- **Step 1 -> Step 6:** Original slopes -> Reliability assessment
- **Steps 2-4 -> Step 7:** ICC estimates -> Power analysis

### Column Naming Conventions
- **Participant IDs:** UID (consistent across all files)
- **Domain slopes:** slope_what, slope_where, slope_when  
- **ICC estimates:** icc_value, variance_between, variance_total
- **Confidence intervals:** ci_lower, ci_upper
- **Effect sizes:** cohens_d
- **P-values:** p_uncorrected, p_bonferroni, p_fdr (Decision D068)

### Data Type Constraints
- **UIDs:** object/string (non-nullable)
- **Slopes:** float64, nullable=False (required for ICC)
- **ICC values:** float64 in [0,1], nullable=False
- **P-values:** float64 in [0,1], nullable=False
- **Effect sizes:** float64, nullable=True (may be undefined)

---

## Cross-RQ Dependencies

**Required Ch5 Outputs:**
- Ch5 5.2.1: What domain slope estimates (results/ch5/5.2.1/data/*slopes*.csv)
- Ch5 5.2.2: Where domain slope estimates (results/ch5/5.2.2/data/*slopes*.csv)
- Ch5 5.2.3: When domain slope estimates (results/ch5/5.2.3/data/*slopes*.csv)

**Dependency Requirements:**
- All 3 source RQs must have rq_results status = success
- Participant-level slope files must contain UID and slope columns
- N=100 participants required with complete slope data across domains
- Modeling consistency verified (identical LMM specifications)

**Fallback Strategy:**
- Primary: Look for files with "slopes" in filename
- Secondary: Search for "participant" files with slope data  
- Tertiary: Extract slopes from LMM model objects if raw data unavailable
- Circuit breaker: QUIT if <100 participants or <3 domains available

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
**Output Files:** dependency_validation.txt with file paths
**Value Ranges:** Found files = 3, participants = 100
**Data Quality:** All domains located, consistent participants
**Log Validation:** Required "PASS", forbidden "MISSING"

#### Step 1: Extract Slopes  
**Output Files:** domain_slopes.csv (100 x 4+ columns)
**Value Ranges:** slopes in [-0.8, 0.2], all negative
**Data Quality:** No missing values, no duplicates
**Log Validation:** Required "100 participants", forbidden "missing"

#### Step 2: Compute ICC
**Output Files:** icc_estimates.csv (3 x 4), variance_components.csv (3 x 5) 
**Value Ranges:** ICC in [0,1], variance_between > 0
**Data Quality:** 3 domains, no NaN values
**Log Validation:** Required "ICC computed", forbidden "negative variance"

#### Step 3: Bootstrap CIs
**Output Files:** bootstrap_cis.csv (3 x 6), bootstrap_distributions.csv (3000 x 2)
**Value Ranges:** CI bounds [0,1], bootstrap bias [-0.1, 0.1]
**Data Quality:** 1000 iterations, >95% success rate
**Log Validation:** Required "1000 iterations", forbidden "convergence failed"

#### Step 4: Statistical Comparisons
**Output Files:** pairwise_comparisons.csv (3 x 8)
**Value Ranges:** p-values [0,1], Cohen's d [-3,3]
**Data Quality:** 3 comparisons, dual p-values present
**Log Validation:** Required "3 tests completed", forbidden "invalid p-value"

#### Step 5: Outlier Analysis
**Output Files:** outlier_analysis.csv, robustness_checks.csv (3 x 4)
**Value Ranges:** |z-score| > 3.29 for outliers, delta_ICC [-0.2, 0.2]
**Data Quality:** <10% outliers per domain, reasonable ICC changes
**Log Validation:** Required "analysis complete", forbidden "too many outliers"

#### Step 6: Split-Half Reliability
**Output Files:** split_half_reliability.csv (3 x 6)  
**Value Ranges:** reliability_r [-1,1], expected >0.50
**Data Quality:** 100 splits completed, 3 domains analyzed
**Log Validation:** Required "100 splits completed", forbidden "failed split"

#### Step 7: Power Analysis
**Output Files:** power_analysis.csv (3 x 5)
**Value Ranges:** achieved_power [0,1], min_detectable_d > 0
**Data Quality:** 3 comparisons analyzed, realistic estimates
**Log Validation:** Required "analysis complete", forbidden "impossible power"

---

## Summary

**Total Steps:** 8 (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** ~45 minutes (bootstrap procedures are time-intensive)
**Cross-RQ Dependencies:** Ch5 5.2.1, 5.2.2, 5.2.3 (domain-specific slope analyses)
**Primary Outputs:** ICC estimates with bootstrap CIs, domain comparisons, reliability assessment
**Validation Coverage:** 100% (all 8 steps have 4-layer validation requirements)

**Key Hypothesis:** What and Where domains will show ICC_slope ~20% similar to overall Ch5 findings. When domain will show lower ICC_slope due to measurement issues with 77% item exclusion rate.

**Critical Methodological Notes:**
- Bootstrap CIs handle non-normal ICC sampling distributions
- Participant-level resampling preserves within-subject dependencies  
- ICC(1,1) formulation appropriate for individual differences analysis
- Multiple comparison corrections applied within-RQ (3 pairwise tests)
- Power analysis acknowledges limitations for detecting small effect sizes
- Split-half reliability validates ICC stability with current sample size

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml  
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent v5.1
- Enhanced statistical specifications per v5.1 requirements
- Addresses rq_stats validation concerns (ICC formulation, bootstrap parameters)
- Incorporates 4-layer validation structure for all steps