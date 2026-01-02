# Analysis Plan: RQ 7.8.2 - Profile External Validation

**Research Question:** 7.8.2
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines correspondence between cognitive test profiles (RAVLT, BVMT, RPM) and REMEMVR performance profiles from RQ 7.8.1. External validation using latent profile analysis for cognitive tests followed by chi-square association testing and Cramer's V effect size calculation. Key methodological focus on dual p-value reporting (Decision D068) and comprehensive statistical specifications for reproducibility.

**Pipeline:** LPA + Chi-square Association + Effect Size Analysis
**Steps:** 6 total analysis steps (Step 0: validation + Steps 1-5: analysis)
**Estimated Runtime:** ~45 minutes total

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni corrected)
- Random seed=42 for all randomized procedures (LPA, bootstrap)
- Bootstrap validation with 1000 iterations for profile stability
- Comprehensive remedial actions for assumption violations

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required RQ 7.8.1 outputs exist and master.xlsx cognitive test data is accessible

**Input:**
- Primary: results/ch7/7.8.1/status.yaml (verify rq_planner: success)
- Alternative: results/ch7/7.8.1/data/step03_rememvr_profile_classifications.csv
- Fallback: results/ch7/7.8.1/data/*profile*.{csv,txt,rds}
- Master data: data/cache/master.xlsx (cognitive test scores)
- Expected: REMEMVR profile classifications for N=100 participants

**Processing:**
- Check RQ 7.8.1 completed through rq_planner stage minimum
- Locate REMEMVR profile classification file (try multiple patterns)
- Verify file contains profile assignments for full sample
- Test master.xlsx access for cognitive test columns (RAVLT, BVMT, RPM)
- If RQ 7.8.1 incomplete: QUIT with "RQ 7.8.1 not sufficiently complete"
- If master.xlsx inaccessible: QUIT with "Cognitive test data not accessible"
- Log all validation checks with success/failure status

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Contains: RQ status, file paths found, sample size verification
- Format: structured text with PASS/FAIL for each dependency

*Value Ranges:*
- Sample sizes: N=100 expected (95-105 acceptable range)
- Profile assignments: categorical values (1 to K profiles)
- Cognitive test scores: positive values expected

*Data Quality:*
- All dependency files located successfully
- No missing critical data sources
- Consistent participant IDs across sources

*Log Validation:*
- Required: "Dependency validation complete"
- Required: "RQ 7.8.1 status: success" or "RQ 7.8.1 rq_planner: success"
- Required: "REMEMVR profiles found: N=XXX participants"
- Required: "Cognitive test data accessible"
- Forbidden: "ERROR", "FAIL", "not found"

**Expected Behavior on Validation Failure:**
Quit immediately with specific error message. Log failure reason. Do not proceed to analysis steps.

### Step 1: Extract and Prepare Cognitive Test Data
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (<5 minutes)

**Purpose:** Load and standardize cognitive test scores to T-scores for LPA input

**Input:**
- data/cache/master.xlsx (cognitive test raw scores)
- Expected columns: UID, RAVLT_total, BVMT_total, RPM_total
- Expected: N=100 participants with complete cognitive data

**Processing:**
- Load cognitive test scores from master.xlsx
- Apply exclusion criteria: participants missing any cognitive test score
- Calculate T-score standardization (M=50, SD=10) for each test:
  - RAVLT_T = 50 + 10 * ((RAVLT_total - mean_RAVLT) / sd_RAVLT)
  - BVMT_T = 50 + 10 * ((BVMT_total - mean_BVMT) / sd_BVMT)
  - RPM_T = 50 + 10 * ((RPM_total - mean_RPM) / sd_RPM)
- Check normality of T-scores using Shapiro-Wilk tests and Q-Q plots
- Descriptive statistics: means, SDs, ranges for both raw and T-scores
- Document any participants excluded for missing data
- Verify T-score transformations: mean ~50, SD ~10 for each measure

**Output:**
- data/step01_cognitive_lpa_input.csv
- data/step01_standardization_diagnostics.txt

**Validation Requirement:**
Validation tools MUST be used after data extraction and standardization.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_cognitive_lpa_input.csv: N rows x 4 columns (UID, RAVLT_T, BVMT_T, RPM_T)
- Data types: UID (object), T-scores (float64)
- data/step01_standardization_diagnostics.txt: normality test results and descriptives

*Value Ranges:*
- T-scores approximately in [20, 80] range (within 3 SDs of mean=50)
- T-score means close to 50.0 (+/- 2.0 acceptable)
- T-score SDs close to 10.0 (+/- 1.0 acceptable)
- No extreme outliers (T-scores outside [10, 90])

*Data Quality:*
- Complete data: no missing values in T-score columns
- Expected sample size: 95-105 participants after exclusions
- All UIDs unique (no duplicates)
- T-score correlation matrix reasonable (|r| < 0.90 to avoid perfect collinearity)

*Log Validation:*
- Required: "T-score standardization complete"
- Required: "Final sample: N=XXX with complete cognitive data"
- Required: "Normality checks complete"
- Forbidden: "ERROR", "infinite", "NaN values detected"

**Expected Behavior on Validation Failure:**
Log specific validation failure. If severe (e.g., <80 participants), quit with error. If minor, document limitation and proceed.

### Step 2: Fit Cognitive Test Latent Profile Analysis
**Dependencies:** Step 1 (standardized cognitive data)
**Complexity:** Medium (~10 minutes including bootstrap)

**Purpose:** Identify optimal number of cognitive ability profiles using LPA

**Input:**
- data/step01_cognitive_lpa_input.csv (standardized T-scores)
- Variables: RAVLT_T, BVMT_T, RPM_T

**Processing:**
- Fit LPA models for K=2, 3, 4, 5 profiles using mixtures package
- Model specifications:
  - Random seed: 42 for reproducibility
  - Multiple random starts: 100 per model to ensure global solution
  - Maximum iterations: 1000
  - Convergence criterion: log-likelihood change < 0.001
- Model selection criteria:
  - BIC (Bayesian Information Criterion) - lower is better
  - BLRT (Bootstrap Likelihood Ratio Test) - p<0.05 favors K over K-1
  - VLMR (Vuong-Lo-Mendell-Rubin) - p<0.05 favors K over K-1
  - Entropy - >0.70 required for clear classification
  - Theoretical interpretability of profile patterns
- For optimal K model:
  - Extract profile assignments and posterior probabilities
  - Calculate average posterior probability per profile (>0.80 desired)
  - Generate profile descriptions (mean T-scores per profile)
- Bootstrap stability assessment:
  - Bootstrap iterations: 1000
  - Random seed: 42
  - Participant-level resampling with replacement
  - Calculate classification stability across bootstrap samples

**Output:**
- data/step02_cognitive_lpa_fit_summary.csv
- data/step02_cognitive_profile_classifications.csv
- data/step02_lpa_model_comparison.txt
- data/step02_bootstrap_stability.txt

**Validation Requirement:**
Validation tools MUST be used after LPA model fitting and selection.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_cognitive_lpa_fit_summary.csv: K rows x 8 columns (model_k, BIC, AIC, BLRT_p, VLMR_p, entropy, avg_posterior_prob, selected)
- data/step02_cognitive_profile_classifications.csv: N rows x 5 columns (UID, profile, posterior_prob_1, posterior_prob_2, ...)
- data/step02_lpa_model_comparison.txt: text summary of model selection
- data/step02_bootstrap_stability.txt: bootstrap validation results

*Value Ranges:*
- Entropy in [0, 1] with selected model >0.70
- Average posterior probabilities >0.70 for all profiles
- Profile assignments: integers 1 to K
- BIC values: decreasing with better fit
- Bootstrap stability >0.80 for acceptable classification consistency

*Data Quality:*
- All models converged successfully (100% convergence rate)
- Clear optimal model identified by convergent criteria
- Profile sizes reasonable (each profile ≥10% of sample)
- No degenerate solutions (profiles with <5 participants)

*Log Validation:*
- Required: "LPA model fitting complete: K=2 to K=5"
- Required: "Optimal model selected: K=X profiles"
- Required: "Entropy = X.XX (threshold: >0.70)"
- Required: "Bootstrap stability assessment complete"
- Forbidden: "convergence failed", "degenerate solution", "boundary parameter"

**Expected Behavior on Validation Failure:**
If no model meets entropy threshold, document limitation but proceed with best available model. If convergence failures >10%, quit with error.

### Step 3: Load REMEMVR Profile Classifications
**Dependencies:** Steps 0, 2 (validated dependencies + cognitive profiles)
**Complexity:** Low (<5 minutes)

**Purpose:** Load REMEMVR profile assignments from RQ 7.8.1 and merge with cognitive profiles

**Input:**
- Primary: results/ch7/7.8.1/data/step03_rememvr_profile_classifications.csv
- Alternative: results/ch7/7.8.1/data/*profile*classification*.csv
- Fallback: results/ch7/7.8.1/data/*rememvr*profile*.{csv,txt}
- Expected: Profile assignments for N=100 participants

**Processing:**
- Load REMEMVR profile classifications from RQ 7.8.1 output
- Verify file format: UID, rememvr_profile columns minimum
- Match participants between cognitive and REMEMVR profiles
- Create merged dataset: UID, cognitive_profile, rememvr_profile
- Handle any participant mismatches:
  - Document participants in one dataset but not the other
  - Use intersection of both samples for analysis
  - Minimum N=90 required to proceed
- Generate cross-tabulation preview: cognitive profile x REMEMVR profile
- Calculate preliminary sample sizes per cell

**Output:**
- data/step03_merged_profile_data.csv
- data/step03_merge_diagnostics.txt

**Validation Requirement:**
Validation tools MUST be used after data merging and participant matching.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_merged_profile_data.csv: N rows x 3 columns (UID, cognitive_profile, rememvr_profile)
- Data types: UID (object), profile variables (integers)
- data/step03_merge_diagnostics.txt: merge statistics and sample size info

*Value Ranges:*
- Cognitive profiles: integers 1 to K_cognitive
- REMEMVR profiles: integers 1 to K_rememvr
- Final sample size: ≥90 participants (90% retention minimum)

*Data Quality:*
- No missing values in profile assignments
- All UIDs unique in merged dataset
- Profile distributions reasonable (no profiles <5 participants)
- Successful merge rate ≥95% of participants

*Log Validation:*
- Required: "REMEMVR profiles loaded successfully"
- Required: "Merge complete: N=XXX participants with both profiles"
- Required: "Cross-tabulation preview generated"
- Forbidden: "merge failed", "insufficient overlap", "missing profile data"

**Expected Behavior on Validation Failure:**
If merged sample <90 participants, quit with error. If 90-95, proceed with limitation note. If any profile has <5 participants, consider profile combining.

### Step 4: Cross-tabulation and Chi-square Association Test
**Dependencies:** Step 3 (merged profile data)
**Complexity:** Medium (~10 minutes including remedial actions)

**Purpose:** Test association between cognitive and REMEMVR profiles using chi-square test with dual p-value reporting

**Input:**
- data/step03_merged_profile_data.csv
- Variables: cognitive_profile, rememvr_profile

**Processing:**
- Create contingency table: cognitive profile (rows) x REMEMVR profile (columns)
- Calculate observed frequencies, expected frequencies, cell percentages
- Calculate standardized residuals: (observed - expected) / sqrt(expected)
- Chi-square assumption checking:
  - Expected cell counts ≥5 in all cells (critical requirement)
  - If any cell <5: use Fisher's exact test as alternative
  - If >20% cells <5: consider profile combining if theoretically justified
- Chi-square test of independence:
  - Test statistic: χ² = Σ[(observed - expected)² / expected]
  - Degrees of freedom: (rows-1) * (columns-1)
  - Uncorrected p-value from chi-square distribution
- Multiple comparison correction (Decision D068):
  - Family: Chapter 7 (28 RQs total)
  - Bonferroni correction: α = 0.05/28 = 0.00179
  - Report BOTH uncorrected AND corrected p-values
- Cramer's V effect size with 95% confidence interval:
  - V = sqrt(χ² / (N * (min(rows,columns) - 1)))
  - Bootstrap 95% CI:
    - Iterations: 1000
    - Random seed: 42
    - Participant-level resampling with replacement
    - CI: percentile method (2.5th, 97.5th percentiles)
- Effect size interpretation:
  - Small: V = 0.10-0.30
  - Medium: V = 0.30-0.50
  - Large: V > 0.50

**Output:**
- data/step04_profile_crosstab.csv
- data/step04_association_test_results.csv
- data/step04_chi_square_diagnostics.txt

**Validation Requirement:**
Validation tools MUST be used after association testing and effect size calculation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_profile_crosstab.csv: contingency table with observed/expected frequencies
- data/step04_association_test_results.csv: 1 row with chi-square, df, p_uncorrected, p_bonferroni, cramers_v, v_ci_lower, v_ci_upper
- data/step04_chi_square_diagnostics.txt: assumption checks and remedial actions taken

*Value Ranges:*
- Chi-square statistic ≥0
- p-values in [0, 1]
- Cramer's V in [0, 1]
- Expected cell counts documented (all ≥5 for valid chi-square)
- Degrees of freedom = (rows-1) * (columns-1)

*Data Quality:*
- Contingency table sums to total sample size
- Expected frequencies calculated correctly
- All statistical tests completed successfully
- Bootstrap CI bounds valid: v_ci_lower ≤ cramers_v ≤ v_ci_upper

*Log Validation:*
- Required: "Contingency table created: X rows x Y columns"
- Required: "Chi-square assumption check complete"
- Required: "Association test complete: χ²=X.XX, p=X.XXX"
- Required: "Dual p-values (D068): uncorrected=X.XXX, corrected=X.XXX"
- Required: "Cramer's V bootstrap CI complete: 1000 iterations"
- Forbidden: "assumption violated", "invalid test", "convergence failed"

**Expected Behavior on Validation Failure:**
If expected cell count assumption violated but Fisher's exact test available, use alternative test and document. If neither test valid, quit with error.

### Step 5: Calculate Conditional Probabilities and Interpretation
**Dependencies:** Step 4 (association test results)
**Complexity:** Low (<5 minutes)

**Purpose:** Extract conditional probabilities and interpret correspondence patterns

**Input:**
- data/step04_profile_crosstab.csv (contingency table)
- data/step04_association_test_results.csv (test results)

**Processing:**
- Calculate conditional probabilities P(REMEMVR profile | Cognitive profile):
  - For each cognitive profile, compute probability of each REMEMVR profile
  - Express as percentages for interpretability
- Identify correspondence patterns:
  - Strongest associations (highest conditional probabilities)
  - Theoretical coherence assessment (verbal→What, spatial→Where patterns)
  - Classification accuracy above chance level
- Generate interpretation summary:
  - Statistical significance assessment (p-value interpretation)
  - Effect size interpretation (Cramer's V magnitude and CI)
  - Correspondence pattern description
  - Theoretical coherence evaluation
- Success criteria evaluation:
  - Chi-square significant after correction (p < 0.00179)
  - Cramer's V > 0.20 (minimum meaningful association)
  - At least 60% correct classification rate above chance
  - Theoretically coherent patterns (verbal profiles→What specialists, etc.)

**Output:**
- data/step05_conditional_probabilities.csv
- data/step05_correspondence_interpretation.txt
- results/profile_correspondence_summary.md

**Validation Requirement:**
Validation tools MUST be used after probability calculation and interpretation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_conditional_probabilities.csv: conditional probability matrix
- data/step05_correspondence_interpretation.txt: structured interpretation text
- results/profile_correspondence_summary.md: formatted summary for thesis

*Value Ranges:*
- Conditional probabilities in [0, 1], sum to 1.0 within each cognitive profile
- Classification accuracy rates in [0, 1]
- Expected chance accuracy = 1/K_rememvr profiles

*Data Quality:*
- Probability matrix sums correctly (rows sum to 1.0)
- All required interpretive elements present
- Theoretical coherence assessment completed
- Success criteria evaluated against thresholds

*Log Validation:*
- Required: "Conditional probabilities calculated"
- Required: "Correspondence patterns identified"
- Required: "Success criteria evaluation complete"
- Required: "Theoretical coherence assessment complete"
- Forbidden: "probability error", "invalid interpretation"

**Expected Behavior on Validation Failure:**
Log specific calculation error. If probability matrix invalid, recalculate from contingency table. If interpretation incomplete, flag for manual review.

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- step00_dependency_validation.txt: Prerequisite verification
- step01_cognitive_lpa_input.csv: T-scored cognitive test data
- step01_standardization_diagnostics.txt: T-score transformation validation
- step02_cognitive_lpa_fit_summary.csv: LPA model comparison results
- step02_cognitive_profile_classifications.csv: Final profile assignments
- step02_lpa_model_comparison.txt: Model selection narrative
- step02_bootstrap_stability.txt: Classification stability assessment
- step03_merged_profile_data.csv: Combined cognitive + REMEMVR profiles
- step03_merge_diagnostics.txt: Data merging statistics
- step04_profile_crosstab.csv: Contingency table with frequencies
- step04_association_test_results.csv: Chi-square and Cramer's V results
- step04_chi_square_diagnostics.txt: Assumption checking documentation
- step05_conditional_probabilities.csv: P(REMEMVR | Cognitive) matrix
- step05_correspondence_interpretation.txt: Pattern analysis
- step05_cramers_v_plot_data.csv: Effect size visualization data

### Logs (ONLY execution logs)
- step00_validate_dependencies.log
- step01_extract_cognitive_data.log
- step02_fit_cognitive_lpa.log
- step03_merge_profile_data.log
- step04_test_associations.log
- step05_interpret_patterns.log

### Plots (EMPTY until rq_plots runs)
- Plot source CSV created: step05_cramers_v_plot_data.csv (effect size CI visualization)
- Future plots: profile_correspondence_heatmap.png, cognitive_profile_means.png

### Results (EMPTY until rq_results runs)
- Future file: summary.md (comprehensive external validation summary)

---

## Expected Data Formats

### Step-to-Step Transformations
1. Raw cognitive scores → T-standardized scores (M=50, SD=10)
2. T-scores → LPA profile assignments with probabilities
3. Cognitive profiles + REMEMVR profiles → merged dataset
4. Profile assignments → contingency table with frequencies
5. Contingency table → chi-square test results + effect sizes
6. Test results → conditional probabilities and interpretation

### Column Naming Conventions
- Participant identifiers: UID (consistent across all files)
- T-scored cognitive tests: RAVLT_T, BVMT_T, RPM_T
- Profile assignments: cognitive_profile, rememvr_profile (integer codes)
- Statistical results: chi_square, df, p_uncorrected, p_bonferroni
- Effect sizes: cramers_v, v_ci_lower, v_ci_upper
- Probabilities: posterior_prob_1, posterior_prob_2, etc.

### Data Type Constraints
- UIDs: object/string, non-nullable, unique
- T-scores: float64, non-nullable, range [10, 90] typical
- Profile assignments: integer, non-nullable, range 1 to K
- Test statistics: float64, non-nullable, chi-square ≥0
- P-values: float64, non-nullable, range [0, 1]
- Effect sizes: float64, non-nullable, Cramer's V in [0, 1]

---

## Cross-RQ Dependencies

**Primary Dependency:** RQ 7.8.1 (REMEMVR Latent Profile Analysis)

**Required Files:**
- Primary: results/ch7/7.8.1/data/step03_rememvr_profile_classifications.csv
- Alternative: results/ch7/7.8.1/data/lpa_profile_assignments.csv
- Fallback: results/ch7/7.8.1/data/*profile*.csv

**Expected Content:**
- REMEMVR profile assignments for N=100 participants
- Columns: UID, rememvr_profile (integer profile code)
- Complete latent profile analysis with entropy >0.70

**Contingency Plan:**
- If RQ 7.8.1 incomplete: QUIT with dependency error
- If file format differs: attempt multiple naming patterns
- If sample size mismatch: use intersection, document limitation

**Master Data Dependency:**
- File: data/cache/master.xlsx
- Required columns: UID, RAVLT_total, BVMT_total, RPM_total
- Expected: Complete cognitive test data for N=100 participants

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
- **Post-execution validation required**
- **4-layer criteria:** Output files, value ranges, data quality, log patterns
- **Circuit breaker:** Quit if RQ 7.8.1 incomplete or master.xlsx inaccessible

#### Step 1: Extract Cognitive Data
- **Post-execution validation required**
- **4-layer criteria:** CSV format, T-score ranges, normality checks, complete data
- **Remedial action:** Document exclusions, proceed if N≥90

#### Step 2: Fit Cognitive LPA
- **Post-execution validation required**
- **4-layer criteria:** Convergence rates, entropy thresholds, classification quality, bootstrap stability
- **Remedial action:** Accept best model if entropy ≥0.60, document limitation

#### Step 3: Merge Profile Data
- **Post-execution validation required**
- **4-layer criteria:** Merge success rate, sample size retention, profile distributions
- **Remedial action:** Proceed if merged N≥90, document participant losses

#### Step 4: Test Associations
- **Post-execution validation required**
- **4-layer criteria:** Chi-square assumptions, dual p-values, effect size CIs, bootstrap completion
- **Remedial action:** Use Fisher's exact test if cell count assumption violated

#### Step 5: Interpret Patterns
- **Post-execution validation required**
- **4-layer criteria:** Probability matrix validity, interpretation completeness, theoretical coherence
- **Remedial action:** Flag incomplete patterns for manual review

---

## Summary

**Total Steps:** 6 (Step 0: validation + Steps 1-5: analysis)
**Estimated Runtime:** ~45 minutes
**Cross-RQ Dependencies:** RQ 7.8.1 (REMEMVR profiles) + master.xlsx (cognitive tests)
**Primary Outputs:** Cognitive LPA classifications, association test results, correspondence patterns
**Validation Coverage:** 100% (all 6 steps have 4-layer validation requirements)

**Key Hypothesis:** Verbal-dominant cognitive profiles (high RAVLT, low BVMT) predict What-specialist REMEMVR profiles, spatial-dominant cognitive profiles (high BVMT, low RAVLT) predict Where-specialist REMEMVR profiles

**Critical Methodological Notes:**
- Bootstrap stability assessment ensures robust profile assignments
- Chi-square expected cell count checking prevents invalid test usage
- Decision D068 dual p-value reporting addresses multiple testing
- Comprehensive remedial actions for assumption violations
- Random seed=42 ensures reproducibility across all randomized procedures

**Statistical Specifications Summary:**
- Random seeds: 42 for all procedures (LPA fitting, bootstrap)
- Bootstrap iterations: 1000 for stability and CI estimation
- LPA model selection: BIC + BLRT + VLMR + entropy convergent criteria
- Multiple comparisons: Chapter-level Bonferroni (α=0.00179)
- Effect size thresholds: Cramer's V >0.20 for meaningful association
- Assumption violations: Fisher's exact test if cell counts <5

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent with v5.1 enhanced statistical specifications