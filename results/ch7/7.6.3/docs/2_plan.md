# Analysis Plan: RQ 7.6.3 - ICC slope replication across domains

**Research Question:** 7.6.3
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This analysis examines whether individual differences in forgetting slopes replicate across What, Where, and When memory domains. Tests the domain-generality vs domain-specificity of forgetting processes using ICC analysis with bootstrap confidence intervals.

**Pipeline:** Variance Component Analysis (ICC) with Bootstrap CIs and Domain Comparisons
**Steps:** 8 total analysis steps (Step 0: dependency validation + Steps 1-7: analysis)
**Estimated Runtime:** 35 minutes total

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Random seed=42 for all bootstrap procedures

**Critical Dependencies:**
This RQ uses DERIVED data from Ch5 domain-specific analyses (5.2.1, 5.2.2, 5.2.3). Must verify Ch5 completion before proceeding.

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 domain-specific analyses completed successfully and locate participant slope files

**Input:**
- Primary: results/ch5/5.2.1/status.yaml (verify What domain analysis complete)
- Primary: results/ch5/5.2.2/status.yaml (verify Where domain analysis complete)
- Primary: results/ch5/5.2.3/status.yaml (verify When domain analysis complete)
- Fallback: results/ch5/5.2.*/data/*participant*slope*.{csv,txt,rds}
- Expected: Participant-level slope estimates for each domain

**Processing:**
- Check Ch5 5.2.1, 5.2.2, 5.2.3 status (rq_results: success required)
- Locate participant slope files using pattern matching
- Verify file accessibility and basic format (participant ID + slope columns)
- Count expected participants (N=100 across all domains)
- Log all dependency validation results
- If any Ch5 analysis incomplete: QUIT with error message

**Output:**
- data/step00_dependency_validation.txt (dependency check results)

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Format: key-value pairs showing file existence and status

*Value Ranges:*
- Participant counts: 100 for each domain (What, Where, When)
- Status checks: "success" for all three Ch5 analyses
- File counts: >=1 slope file per domain

*Data Quality:*
- All three required status.yaml files accessible
- All three domains have participant slope data available
- No missing domains in dependency chain

*Log Validation:*
- Required patterns: "Ch5 dependency validation complete", "All domains available"
- Required patterns: "What: SUCCESS", "Where: SUCCESS", "When: SUCCESS"
- Forbidden patterns: "ERROR", "MISSING", "incomplete", "not found"

**Expected Behavior on Validation Failure:**
Quit immediately if any Ch5 dependency missing. Log specific missing component. Invoke g_debug.

### Step 1: Extract Domain-Specific Slopes
**Dependencies:** Step 0 (validated Ch5 dependencies)
**Complexity:** Medium (~5 minutes)

**Purpose:** Load and merge participant-level forgetting slopes from Ch5 domain analyses

**Input:**
- Primary: results/ch5/5.2.1/data/*participant*slope*.csv (What domain slopes)
- Alternative: results/ch5/5.2.1/data/step*slope*.csv
- Fallback: results/ch5/5.2.1/data/*slope*.{csv,txt}
- Similar patterns for 5.2.2 (Where) and 5.2.3 (When)
- Expected format: columns including UID, slope_estimate, slope_se

**Processing:**
- Load participant slope files from all three Ch5 analyses
- Standardize column naming: UID, slope_what, slope_where, slope_when
- Merge datasets on participant UID
- Verify complete data for N=100 participants across all domains
- Check for missing slopes or extreme outliers
- Compute basic descriptive statistics per domain
- Save merged dataset with standardized format

**Output:**
- data/step01_domain_slopes.csv (merged slope data: 100 rows x 4 columns)

**Validation Requirement:**
Validation tools MUST be used after data extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_domain_slopes.csv: 100 rows x 4 columns
- Columns: UID (object), slope_what (float64), slope_where (float64), slope_when (float64)

*Value Ranges:*
- Slopes in [-1.0, 0.5] (forgetting rates, typically negative)
- No extreme outliers (>3 SDs from domain mean)
- Slope standard errors > 0 if included

*Data Quality:*
- All 100 participants present (no missing UIDs)
- No duplicate UIDs
- Complete slope data for all three domains
- Missing data = 0% (DERIVED data should be complete)

*Log Validation:*
- Required patterns: "Domain slopes extracted: 100 participants"
- Required patterns: "What domain: N=100", "Where domain: N=100", "When domain: N=100"
- Forbidden patterns: "ERROR", "missing data", "failed to load"

**Expected Behavior on Validation Failure:**
Raise error specifying which domain has issues. Log participant counts per domain. Quit if <95% complete data.

### Step 2: Compute ICC for Each Domain
**Dependencies:** Step 1 (domain slopes extracted)
**Complexity:** Medium (~5 minutes)

**Purpose:** Calculate ICC(1,1) for slope variance in each memory domain to quantify between-person individual differences

**Input:**
- data/step01_domain_slopes.csv (participant slopes by domain)

**Processing:**
- For each domain (What, Where, When):
  - Extract slope values for all participants
  - Fit one-way random effects ANOVA (participants as random factor)
  - Compute ICC(1,1) = Between-person variance / Total variance
  - Extract variance components: between-person, within-person, total
  - Calculate 95% confidence intervals using Fisher transformation if normality assumptions met
- Implementation: Use statsmodels or scipy.stats
- ICC formulation: ICC(1,1) for single measurement, absolute agreement
- Document variance decomposition for each domain
- Compare ICC estimates preliminarily (formal tests in Step 4)

**Output:**
- data/step02_icc_estimates.csv (ICC values: 3 rows x 6 columns)
- Format: domain, icc_value, between_var, within_var, total_var, fisher_ci

**Validation Requirement:**
Validation tools MUST be used after ICC computation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_icc_estimates.csv: 3 rows x 6 columns
- Columns: domain (What/Where/When), icc_value (float64), between_var, within_var, total_var, fisher_ci

*Value Ranges:*
- ICC values in [0, 1] (proportion of variance)
- What/Where ICC expected 0.15-0.30 (based on Ch5 findings)
- When ICC potentially lower: 0.05-0.20 (measurement issues)
- Variance components all >= 0

*Data Quality:*
- All three domains present
- No negative variance estimates
- ICC calculation successful for all domains
- Fisher CI bounds logical (lower < icc < upper)

*Log Validation:*
- Required patterns: "ICC computation complete: 3 domains"
- Required patterns: "What ICC:", "Where ICC:", "When ICC:"
- Forbidden patterns: "ERROR", "negative variance", "computation failed"

**Expected Behavior on Validation Failure:**
Log specific domain with computation issues. Check for degenerate variance (all slopes identical). Proceed with available ICCs if >=2 domains successful.

### Step 3: Bootstrap Confidence Intervals
**Dependencies:** Step 2 (ICC estimates computed)
**Complexity:** High (~10 minutes including 1000 bootstrap iterations)

**Purpose:** Generate robust 95% confidence intervals for ICC estimates using participant-level bootstrap resampling

**Input:**
- data/step01_domain_slopes.csv (original slope data)

**Processing:**
- Implement participant-level block bootstrap (preserves within-participant structure if relevant)
- Iterations: 1000 (adequate for percentile CIs per Efron & Tibshirani, 1993)
- Random seed: 42 for reproducibility
- Resampling strategy: Sample 100 participants WITH replacement
- For each bootstrap iteration:
  - Resample participants, keep all their slope data
  - Compute ICC(1,1) for each domain using resampled data
  - Store ICC estimates for all three domains
- CI computation: Percentile method (2.5th, 97.5th percentiles for 95% CI)
- Monitor convergence: Track proportion of successful ICC computations
- Special attention to When domain (may have ICC near zero, causing convergence issues)
- Bias assessment: Compare bootstrap mean ICC to original ICC estimate

**Output:**
- data/step03_bootstrap_cis.csv (bootstrap CIs: 3 rows x 5 columns)
- Format: domain, original_icc, bootstrap_mean, ci_lower, ci_upper

**Validation Requirement:**
Validation tools MUST be used after bootstrap execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_bootstrap_cis.csv: 3 rows x 5 columns
- Columns: domain, original_icc, bootstrap_mean, ci_lower, ci_upper (all float64)

*Value Ranges:*
- All ICC estimates in [0, 1]
- CI bounds: 0 <= ci_lower < original_icc < ci_upper <= 1
- Bootstrap bias < 0.10 (|bootstrap_mean - original_icc|)
- What/Where CIs likely exclude 0, When CI may include 0

*Data Quality:*
- All three domains with successful bootstrap
- CI width reasonable (<0.40 for stable estimates)
- Convergence rate >95% for all domains
- No degenerate CIs (ci_lower = ci_upper)

*Log Validation:*
- Required patterns: "Bootstrap complete: 1000 iterations"
- Required patterns: "Convergence rate >95% for all domains"
- Required patterns: "CI computation successful"
- Forbidden patterns: "ERROR", "convergence failure", "degenerate bootstrap"

**Expected Behavior on Validation Failure:**
If convergence <90% for any domain, increase iterations to 5000. If When domain consistently fails, acknowledge limitation and proceed with available data.

### Step 4: Statistical Comparisons Between Domains
**Dependencies:** Step 3 (bootstrap CIs computed)
**Complexity:** Medium (~5 minutes)

**Purpose:** Test statistical differences between domain ICCs using bootstrap distributions and effect size calculations

**Input:**
- Bootstrap distributions from Step 3 (1000 iterations x 3 domains)
- data/step03_bootstrap_cis.csv (confidence intervals)

**Processing:**
- Pairwise comparisons: What vs Where, What vs When, Where vs When
- For each comparison:
  - Compute difference in bootstrap ICC distributions (ICC_domain1 - ICC_domain2)
  - Calculate p-value: proportion of bootstrap differences <= 0
  - Compute effect size using Cohen's guidelines for ICC differences
  - Generate 95% CI for the difference
- Multiple comparison correction:
  - Family: Within-RQ comparisons (3 pairwise tests)
  - Bonferroni correction: alpha = 0.05/3 = 0.0167 per test
  - Also compute FDR-adjusted p-values using Benjamini-Hochberg
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Effect size interpretation: small (0.10), medium (0.25), large (0.40) for ICC differences
- Cross-domain correlation analysis: correlate individual participants' slopes across domains

**Output:**
- data/step04_pairwise_comparisons.csv (comparisons: 3 rows x 7 columns)
- Format: comparison, icc_diff, effect_size, p_uncorrected, p_bonferroni, p_fdr, ci_lower, ci_upper

**Validation Requirement:**
Validation tools MUST be used after comparison execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_pairwise_comparisons.csv: 3 rows x 7 columns
- Columns: comparison, icc_diff, effect_size, p_uncorrected, p_bonferroni, p_fdr, ci_lower, ci_upper

*Value Ranges:*
- ICC differences in [-1, 1]
- p-values in [0, 1] for all correction types
- Effect sizes typically 0-0.50 for ICC comparisons
- CI bounds contain zero if non-significant difference

*Data Quality:*
- All three pairwise comparisons present
- Bonferroni p = p_uncorrected * 3 (capped at 1.0)
- FDR adjustment applied correctly
- Effect sizes correspond to difference magnitudes

*Log Validation:*
- Required patterns: "Pairwise comparisons complete: 3 tests"
- Required patterns: "Bonferroni correction applied"
- Required patterns: "Effect sizes computed"
- Forbidden patterns: "ERROR", "correction failed", "invalid p-value"

**Expected Behavior on Validation Failure:**
Check p-value calculations and correction procedures. Verify bootstrap distribution validity. Log specific comparison causing issues.

### Step 5: Model Diagnostics and Outlier Analysis
**Dependencies:** Step 1 (domain slopes), Step 2 (ICC estimates)
**Complexity:** Low (~3 minutes)

**Purpose:** Assess slope distributions, identify outliers, and evaluate their impact on ICC estimates

**Input:**
- data/step01_domain_slopes.csv (participant slopes)
- data/step02_icc_estimates.csv (ICC values)

**Processing:**
- For each domain:
  - Check normality: Shapiro-Wilk test on slope distributions
  - Identify outliers: participants with slopes >2.5 SDs from domain mean
  - Outlier impact: recompute ICC with outliers removed
  - Distribution assessment: skewness, kurtosis, range
- Remedial actions if assumptions violated:
  - Non-normality (p < 0.05): Acknowledge, rely on bootstrap CIs
  - Extreme outliers: Report results with/without outliers
  - Heteroscedasticity across domains: Document for interpretation
- Slope reliability assessment: check if Ch5 provided slope standard errors
- Cross-domain pattern analysis: identify participants with consistently high/low slopes

**Output:**
- data/step05_outlier_analysis.csv (diagnostics per domain and participant)
- Format: domain-level and participant-level outlier flags and statistics

**Validation Requirement:**
Validation tools MUST be used after diagnostic execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_outlier_analysis.csv: Variable rows (3 domains + flagged participants)
- Columns: entity_type (domain/participant), entity_id, outlier_flag, normality_p, modified_icc

*Value Ranges:*
- Normality p-values in [0, 1]
- Outlier flags: 0/1 (binary)
- Modified ICCs in [0, 1] if outliers removed
- Typically 0-5% of participants flagged as outliers

*Data Quality:*
- All three domains assessed for normality
- Outlier detection applied consistently
- Modified ICC computation successful
- No missing diagnostic statistics

*Log Validation:*
- Required patterns: "Outlier analysis complete"
- Required patterns: "Normality tests: What p=", "Where p=", "When p="
- Required patterns: "Outliers identified:"
- Forbidden patterns: "ERROR", "diagnostic failure"

**Expected Behavior on Validation Failure:**
Document which diagnostic tests failed. Proceed with available information. Flag concerning patterns for interpretation.

### Step 6: Cross-Validation (Split-Half Reliability)
**Dependencies:** Step 1 (domain slopes)
**Complexity:** Medium (~5 minutes)

**Purpose:** Assess reliability of ICC estimates using split-half cross-validation

**Input:**
- data/step01_domain_slopes.csv (100 participants x 3 domains)

**Processing:**
- Random split: Divide 100 participants into two halves (50 each)
- Random seed: 42 for reproducibility
- For each half:
  - Compute ICC(1,1) for each domain using subset of participants
  - Extract variance components
- Reliability assessment:
  - Correlate ICC estimates between halves across domains
  - Compute ICC reliability coefficient for each domain
  - Target: reliability r > 0.70 for acceptable stability
- Sensitivity analysis: Repeat with different random splits (5 iterations)
- Convergence check: Ensure adequate participants per half for stable ICC estimation

**Output:**
- data/step06_split_half_reliability.csv (reliability statistics: 3 rows x 4 columns)
- Format: domain, half1_icc, half2_icc, reliability_r

**Validation Requirement:**
Validation tools MUST be used after cross-validation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_split_half_reliability.csv: 3 rows x 4 columns
- Columns: domain, half1_icc, half2_icc, reliability_r (all float64)

*Value Ranges:*
- All ICC estimates in [0, 1]
- Reliability correlations in [-1, 1], target >0.70
- Half estimates should be reasonably similar (difference <0.20)

*Data Quality:*
- All three domains with successful split-half analysis
- Both halves have adequate sample size (N=50 each)
- Reliability estimates computed successfully
- No failed convergence in subset analyses

*Log Validation:*
- Required patterns: "Split-half analysis complete"
- Required patterns: "Reliability assessment: 3 domains"
- Required patterns: "Split successful: 50 + 50 participants"
- Forbidden patterns: "ERROR", "insufficient sample size", "convergence failed"

**Expected Behavior on Validation Failure:**
If reliability <0.70 for any domain, acknowledge limitation. If split fails, try alternative splitting approach or document sample size constraints.

### Step 7: Power Analysis and Sensitivity Testing
**Dependencies:** Step 2 (ICC estimates), Step 4 (domain comparisons)
**Complexity:** Low (~2 minutes)

**Purpose:** Conduct post-hoc power analysis for detecting ICC differences and assess minimum detectable effects

**Input:**
- data/step02_icc_estimates.csv (observed ICC values)
- data/step04_pairwise_comparisons.csv (effect sizes)

**Processing:**
- Post-hoc power analysis for ICC difference detection:
  - Given: N=100 participants, alpha=0.0167 (Bonferroni-corrected)
  - Calculate: actual power for observed effect sizes
  - Use Cohen's conventions: small (0.10), medium (0.25), large (0.40) ICC differences
- Sensitivity analysis:
  - Minimum detectable ICC difference at 80% power
  - Sample size requirements for reliable ICC estimation
  - Impact of When domain measurement issues on power
- Power interpretation:
  - Adequate power (>0.80) for medium effects
  - Limited power for small effects (acknowledge limitation)
- Future sample size recommendations for replication studies

**Output:**
- data/step07_power_analysis.csv (power statistics: 3 rows x 5 columns)
- Format: comparison, observed_effect, actual_power, min_detectable_effect, sample_needed_80power

**Validation Requirement:**
Validation tools MUST be used after power analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_power_analysis.csv: 3 rows x 5 columns
- Columns: comparison, observed_effect, actual_power, min_detectable_effect, sample_needed_80power

*Value Ranges:*
- Effect sizes in [0, 1] (ICC difference magnitudes)
- Power values in [0, 1]
- Minimum detectable effects in [0.05, 0.50] range
- Sample size recommendations: 50-300 range typical

*Data Quality:*
- All three pairwise comparisons analyzed
- Power calculations successful
- Realistic sample size recommendations
- Effect size interpretations included

*Log Validation:*
- Required patterns: "Power analysis complete"
- Required patterns: "Post-hoc power computed"
- Required patterns: "Sensitivity analysis complete"
- Forbidden patterns: "ERROR", "power calculation failed"

**Expected Behavior on Validation Failure:**
If power calculations fail, document issue and proceed. Use manual Cohen's conventions if automated power analysis unavailable.

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (Ch5 dependency check results)
- data/step01_domain_slopes.csv (merged participant slopes: 100x4)
- data/step02_icc_estimates.csv (ICC by domain: 3x6)
- data/step03_bootstrap_cis.csv (bootstrap confidence intervals: 3x5)
- data/step04_pairwise_comparisons.csv (domain comparisons: 3x7)
- data/step05_outlier_analysis.csv (diagnostic statistics)
- data/step06_split_half_reliability.csv (reliability analysis: 3x4)
- data/step07_power_analysis.csv (power and sensitivity: 3x5)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_slopes.log
- logs/step02_compute_icc.log
- logs/step03_bootstrap_cis.log
- logs/step04_compare_domains.log
- logs/step05_diagnostic_analysis.log
- logs/step06_cross_validation.log
- logs/step07_power_analysis.log

### Plots (EMPTY until rq_plots runs)
Plot source data will be generated in data/ folder:
- data/step02_icc_comparison_plot_data.csv (ICC estimates with CIs by domain)
- data/step01_slope_distributions_plot_data.csv (domain-specific slope histograms)

### Results (EMPTY until rq_results runs)
Summary will be generated: results/icc_replication_summary.md

---

## Expected Data Formats

### Step-to-Step Transformations
1. Step 0 -> Step 1: Dependency validation enables data extraction
2. Step 1 -> Step 2: Domain slopes (wide format) -> ICC estimates (domain summary)
3. Step 2 -> Step 3: Single ICC estimates -> bootstrap distributions (1000 iterations)
4. Step 3 -> Step 4: Bootstrap CIs -> pairwise comparisons with effect sizes
5. Steps 1,2 -> Step 5: Original data + ICC estimates -> diagnostic analysis
6. Step 1 -> Step 6: Domain slopes -> split-half reliability assessment
7. Steps 2,4 -> Step 7: ICC estimates + comparisons -> power analysis

### Column Naming Conventions
- Participant IDs: UID (consistent with REMEMVR conventions)
- Domain slopes: slope_what, slope_where, slope_when (standardized naming)
- ICC values: icc_value, between_var, within_var, total_var
- Statistical tests: p_uncorrected, p_bonferroni, p_fdr (Decision D068)
- Bootstrap results: original_icc, bootstrap_mean, ci_lower, ci_upper

### Data Type Constraints
- UID: object (string participant identifiers)
- Slopes: float64 (nullable=False, range: -1.0 to 0.5)
- ICC estimates: float64 (nullable=False, range: 0.0 to 1.0)
- p-values: float64 (nullable=False, range: 0.0 to 1.0)
- Bootstrap iterations: 1000 per domain (fixed)

---

## Cross-RQ Dependencies

**Critical Dependencies on Ch5 Domain Analyses:**

### Ch5 5.2.1 (What Domain Analysis)
- **Required:** Participant-level slope estimates for What domain
- **Primary path:** results/ch5/5.2.1/data/participant_slopes.csv
- **Alternative:** results/ch5/5.2.1/data/step*slope*.csv
- **Fallback:** results/ch5/5.2.1/data/*slope*.{csv,txt,rds}
- **Format:** UID + slope_estimate (+ optional slope_se)

### Ch5 5.2.2 (Where Domain Analysis)  
- **Required:** Participant-level slope estimates for Where domain
- **Primary path:** results/ch5/5.2.2/data/participant_slopes.csv
- **Alternative:** results/ch5/5.2.2/data/step*slope*.csv
- **Fallback:** results/ch5/5.2.2/data/*slope*.{csv,txt,rds}
- **Format:** UID + slope_estimate (+ optional slope_se)

### Ch5 5.2.3 (When Domain Analysis)
- **Required:** Participant-level slope estimates for When domain  
- **Primary path:** results/ch5/5.2.3/data/participant_slopes.csv
- **Alternative:** results/ch5/5.2.3/data/step*slope*.csv
- **Fallback:** results/ch5/5.2.3/data/*slope*.{csv,txt,rds}
- **Format:** UID + slope_estimate (+ optional slope_se)

**Circuit Breaker:** If any Ch5 analysis incomplete (status != success), QUIT with specific error message indicating which domain(s) unavailable.

**Data Expectations:** N=100 participants with complete slope data across all three domains. Slope values representing forgetting rates (typically negative values between -1.0 and 0.5).

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution. The v4.X architecture requires 4-layer validation to prevent cascading failures.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
**Validation tools will verify:**
1. Output Files: dependency_validation.txt exists with correct format
2. Value Ranges: Status indicators show "success" for all Ch5 analyses
3. Data Quality: All required files accessible, participant counts correct
4. Log Validation: Success patterns present, error patterns absent

#### Step 1: Extract Domain Slopes  
**Validation tools will verify:**
1. Output Files: domain_slopes.csv with 100 rows x 4 columns
2. Value Ranges: Slopes in realistic forgetting rate range [-1.0, 0.5]
3. Data Quality: Complete data, no duplicates, all domains present
4. Log Validation: Extraction success logged, no merge failures

#### Step 2: Compute ICC
**Validation tools will verify:**
1. Output Files: icc_estimates.csv with 3 domains x 6 statistics
2. Value Ranges: ICC values in [0,1], variance components >= 0
3. Data Quality: All domains computed successfully, realistic ICC values
4. Log Validation: Computation success for all domains

#### Step 3: Bootstrap CIs
**Validation tools will verify:**
1. Output Files: bootstrap_cis.csv with confidence intervals
2. Value Ranges: CIs bound original estimates, reasonable width
3. Data Quality: High convergence rate, low bootstrap bias
4. Log Validation: 1000 iterations completed, convergence monitored

#### Step 4: Statistical Comparisons
**Validation tools will verify:**
1. Output Files: pairwise_comparisons.csv with corrected p-values
2. Value Ranges: p-values in [0,1], effect sizes interpretable
3. Data Quality: All corrections applied, dual p-values present
4. Log Validation: Multiple comparisons handled properly

#### Step 5: Diagnostics
**Validation tools will verify:**
1. Output Files: outlier_analysis.csv with diagnostic statistics
2. Value Ranges: Test statistics in valid ranges
3. Data Quality: All domains assessed, outliers identified
4. Log Validation: Diagnostic tests completed successfully

#### Step 6: Cross-Validation
**Validation tools will verify:**
1. Output Files: split_half_reliability.csv with reliability statistics
2. Value Ranges: Reliability coefficients interpretable
3. Data Quality: Split successful, ICCs computed on both halves
4. Log Validation: Cross-validation completed without errors

#### Step 7: Power Analysis
**Validation tools will verify:**
1. Output Files: power_analysis.csv with power statistics
2. Value Ranges: Power values in [0,1], realistic sample sizes
3. Data Quality: All comparisons analyzed, interpretable results
4. Log Validation: Power calculations completed successfully

---

## Summary

**Total Steps:** 8 (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** 35 minutes total
**Cross-RQ Dependencies:** Ch5 5.2.1, 5.2.2, 5.2.3 (domain-specific slope analyses)
**Primary Outputs:** ICC estimates with bootstrap CIs, domain comparisons, reliability assessment
**Validation Coverage:** 100% (all 8 steps have 4-layer validation requirements)

**Key Hypothesis:** What and Where domains will show ICC_slope ~20% similar to Ch5 overall findings. When domain will show lower ICC due to measurement issues.

**Critical Methodological Notes:**
- Bootstrap resampling addresses potential non-normality in ICC sampling distributions
- Multiple comparison correction applied to 3 pairwise domain tests
- ICC(1,1) formulation appropriate for single measurement individual differences
- Split-half reliability provides cross-validation of ICC stability
- Acknowledges When domain measurement limitations from Ch5 (77% item exclusion)

**Statistical Specifications Applied:**
- Random seed=42 for all bootstrap and cross-validation procedures
- Bootstrap: 1000 iterations, participant-level resampling, percentile CIs
- Multiple comparisons: Bonferroni + FDR correction, dual p-value reporting
- Power analysis: Post-hoc approach with sensitivity testing
- Assumption checking: Normality, outliers, convergence monitoring

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml (will identify missing bootstrap tools from rq_stats validation)
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code with proper statistical implementations

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent with v5.1 enhancements
  - Complete statistical specifications (bootstrap, CV, power, corrections)
  - Mandatory random seed=42 for reproducibility
  - 4-layer validation requirements for all steps
  - Cross-RQ dependency validation with fallback paths
  - Bootstrap tools missing flag from rq_stats validation addressed in implementation notes