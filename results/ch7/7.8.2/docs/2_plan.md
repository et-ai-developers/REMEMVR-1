# Analysis Plan: RQ 7.8.2 - Profile External Validation

**Research Question:** 7.8.2
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

**Research Question:** Do cognitive test profiles (e.g., verbal-dominant vs spatial-dominant) correspond to REMEMVR profiles?

This RQ examines correspondence between cognitive test latent profile analysis (LPA) and REMEMVR performance latent profiles from RQ 7.8.1. External validation using established cognitive tests (RAVLT, BVMT, RPM) to validate REMEMVR-derived individual difference patterns.

**Pipeline:** Latent Profile Analysis + Chi-square Association + Effect Size Analysis
**Steps:** 6 total analysis steps (Step 0: dependency validation + Steps 1-5: core analysis)  
**Estimated Runtime:** 45-60 minutes total

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni corrected)
- Statistical concerns addressed: CV misapplication removed, replaced with split-sample validation
- Sample size limitation acknowledged: Focus on 2-3 profile solutions (N=100 constraint)

**Critical Statistical Enhancements (v5.1):**
- Convergence diagnostics with 500 random starts, seed=42
- Split-sample validation (70/30) instead of inappropriate cross-validation
- Multiple model selection criteria (AIC, BIC, entropy, BLRT)
- Sparse cell handling with Fisher's exact test fallback
- Comprehensive assumption checking with remedial actions

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required RQ 7.8.1 outputs and master.xlsx cognitive test data exist before proceeding

**Input:**
- Primary: results/ch7/7.8.1/status.yaml (verify rq_results: success)
- Primary: results/ch7/7.8.1/data/step03_rememvr_profile_classifications.csv
- Alternative: results/ch7/7.8.1/data/*profile*.csv
- Fallback: results/ch7/7.8.1/data/*lpa*.csv  
- Expected: REMEMVR profile assignments for N=100 participants
- Also verify: data/cache/master.xlsx accessibility (cognitive test scores)

**Processing:**
- Check RQ 7.8.1 completion status in status.yaml
- Locate REMEMVR profile classification file (try multiple patterns)
- Verify file contains participant IDs and profile assignments
- Check master.xlsx contains RAVLT, BVMT, RPM columns
- Log all validation results with specific file paths found
- If any dependency missing: QUIT with specific error message

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency validation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Expected content: Status of each dependency check with file paths

*Value Ranges:*
- N/A (text validation file)

*Data Quality:*
- All dependencies confirmed present
- File paths logged and accessible
- No missing critical components

*Log Validation:*
- Required patterns: "RQ 7.8.1 status: success", "REMEMVR profiles found", "Cognitive tests accessible"
- Forbidden patterns: "ERROR", "missing", "not found"
- Acceptable warnings: File path variations logged

**Expected Behavior on Validation Failure:**
Quit immediately with specific dependency error message, log to logs/step00_dependency_validation.log

### Step 1: Extract and Prepare Cognitive Test Data
**Dependencies:** Step 0 (validated dependencies)
**Complexity:** Low (<10 minutes)

**Purpose:** Extract cognitive test scores from dfnonvr.csv and standardize to T-scores for LPA analysis

**Input:**
- data/cache/master.xlsx (RAVLT, BVMT, RPM raw scores)
- Participant ID column for merging

**Processing:**
- Load cognitive test data: RAVLT_total, BVMT_total, RPM_total
- Check for missing data patterns and document exclusions
- Apply inclusion criteria: complete data on all three tests required  
- Standardize to T-scores (M=50, SD=10) for each test separately
- Calculate descriptive statistics (M, SD, range) for raw and T-scores
- Create correlation matrix among cognitive T-scores
- Random seed: 42 for any random operations (none expected in this step)
- Check for extreme outliers using IQR method (Q1-1.5*IQR, Q3+1.5*IQR)
- Document final sample size after exclusions

**Output:**
- data/step01_cognitive_lpa_input.csv (participant ID, RAVLT_T, BVMT_T, RPM_T)
- data/step01_cognitive_descriptives.csv (means, SDs, correlations, outlier info)

**Validation Requirement:**
Validation tools MUST be used after cognitive data extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_cognitive_lpa_input.csv: N rows x 4 columns (ID, RAVLT_T, BVMT_T, RPM_T)
- data/step01_cognitive_descriptives.csv: summary statistics with T-score validation
- All participants with complete cognitive data (expect N=95-100)

*Value Ranges:*
- T-scores approximately: M=50, SD=10 for each test (within ±2 due to rounding)
- Raw correlations: 0.20 to 0.70 range (typical cognitive test intercorrelations)
- No T-scores below 10 or above 90 (extreme standardization check)

*Data Quality:*
- No missing values in final dataset
- Sample size ≥95 (minimal exclusions expected)
- T-score standardization successful (M~50, SD~10)
- Correlation matrix positive definite (no perfect correlations)

*Log Validation:*
- Required patterns: "Cognitive data extracted", "T-score standardization complete", "Final N = XX"
- Forbidden patterns: "ERROR", "convergence", "missing data after exclusion"
- Acceptable warnings: "X participants excluded for missing cognitive data"

**Expected Behavior on Validation Failure:**
Log warning and document exclusions, continue if N≥90, quit if N<90 with sample size error

### Step 2: Fit Cognitive Test Latent Profile Analysis
**Dependencies:** Step 1 (standardized cognitive T-scores)
**Complexity:** High (~20 minutes including model comparison)

**Purpose:** Identify optimal number of cognitive profiles using LPA with comprehensive model selection

**Input:**
- data/step01_cognitive_lpa_input.csv (T-score matrix for LPA)

**Processing:**
- Fit LPA models for K=2, K=3, K=4 profiles using mixtures package
- **Convergence specifications (CRITICAL - addresses stats validation concern):**
  - Random seed: 42 for all random starts
  - Random starts: 500 with 50 final stage optimizations  
  - Convergence criterion: log-likelihood replication within 0.01
  - Maximum iterations: 5000 per model
  - If non-convergence: reduce K, increase iterations, try different start values
  - Document convergence status for each K value
- **Model selection criteria (multiple criteria per stats recommendation):**
  - Calculate: AIC, BIC, entropy, BLRT (bootstrapped likelihood ratio test)
  - Bootstrap iterations for BLRT: 100 (computational constraint)
  - Select optimal K using converging evidence across criteria (not BIC alone)
  - Entropy threshold: >0.70 for acceptable classification quality
  - Theoretical interpretability as tiebreaker for close statistical fits
- **Sample size consideration (addresses stats concern):**
  - Acknowledge N=100 is marginal for K=4+ solutions
  - If K=4 shows poor entropy (<0.70) or convergence issues, limit to K≤3
  - Report profile stability and classification uncertainty
- Extract profile classifications using modal assignment
- Calculate profile means, SDs, and posterior probabilities
- **Split-sample validation (replaces inappropriate CV per stats feedback):**
  - Randomly split sample 70%/30% (seed=42)
  - Fit optimal K model on training sample (70%)
  - Assess profile correspondence in test sample (30%)
  - Report classification agreement and profile mean stability

**Output:**
- data/step02_lpa_model_comparison.csv (fit statistics for K=2,3,4)
- data/step02_cognitive_profile_classifications.csv (optimal profile assignments)
- data/step02_profile_descriptives.csv (profile means and interpretation)
- data/step02_split_sample_validation.csv (stability assessment)

**Validation Requirement:**
Validation tools MUST be used after LPA model fitting execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_lpa_model_comparison.csv: 3 rows x 6 columns (K, AIC, BIC, entropy, BLRT_p, convergence)
- data/step02_cognitive_profile_classifications.csv: N rows x 3 columns (ID, profile, max_prob)
- data/step02_profile_descriptives.csv: K profiles x 4 columns (profile, RAVLT_M, BVMT_M, RPM_M)
- data/step02_split_sample_validation.csv: validation metrics

*Value Ranges:*
- Entropy: 0.70 to 1.00 (acceptable classification quality)
- Profile means: T-score range 35-65 (reasonable profile differentiation)
- Maximum probabilities: >0.70 for most participants (confident classification)
- AIC/BIC: decreasing then increasing pattern expected

*Data Quality:*
- All models converged successfully (convergence=TRUE in comparison file)
- Optimal K selected (2 or 3 profiles expected given sample size)
- Profile means interpretable and differentiated
- Split-sample agreement >0.70 (stable solution)

*Log Validation:*
- Required patterns: "LPA models fitted", "Optimal K = X selected", "Split-sample validation complete"
- Forbidden patterns: "non-convergence", "entropy < 0.70", "classification failure"
- Acceptable warnings: "K=4 model convergence unstable"

**Expected Behavior on Validation Failure:**
If convergence failure: retry with increased iterations, reduce K if persistent, document in validation log

### Step 3: Merge Profile Classifications and Create Cross-Tabulation
**Dependencies:** Steps 1-2 (cognitive profiles + REMEMVR profiles)
**Complexity:** Medium (~10 minutes)

**Purpose:** Merge cognitive and REMEMVR profile classifications and create contingency table

**Input:**
- data/step02_cognitive_profile_classifications.csv (cognitive profiles)
- results/ch7/7.8.1/data/step03_rememvr_profile_classifications.csv (REMEMVR profiles)
- Primary path pattern for REMEMVR profiles: results/ch7/7.8.1/data/*profile*.csv

**Processing:**
- Load both profile classification datasets
- Merge by participant ID (inner join to ensure matching participants only)
- Document any participants missing from either dataset
- Create contingency table: cognitive profile x REMEMVR profile
- Calculate observed frequencies, expected frequencies, row/column percentages
- Compute standardized residuals for each cell
- **Sparse cell handling (addresses stats validation concern):**
  - Check expected frequencies ≥5 per cell requirement
  - If any expected frequency <5: document cells, prepare Fisher's exact test
  - Calculate degrees of freedom for chi-square test
- Create comprehensive crosstab with marginal totals
- Calculate conditional probabilities: P(REMEMVR profile | cognitive profile)

**Output:**
- data/step03_merged_profile_data.csv (combined profile assignments)
- data/step03_profile_crosstab.csv (full contingency table with frequencies)
- data/step03_conditional_probabilities.csv (prediction patterns)

**Validation Requirement:**
Validation tools MUST be used after profile merging and cross-tabulation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_merged_profile_data.csv: N rows x 3 columns (ID, cognitive_profile, rememvr_profile)
- data/step03_profile_crosstab.csv: contingency table with observed/expected frequencies
- data/step03_conditional_probabilities.csv: prediction matrix

*Value Ranges:*
- Merged sample size: 90-100 participants (account for any exclusions)
- Cell frequencies: ≥1 in most cells (some may be 0 for sparse combinations)
- Expected frequencies: ideally ≥5 per cell, document if violated
- Conditional probabilities: 0.0 to 1.0, sum to 1.0 within cognitive profiles

*Data Quality:*
- All cognitive profiles represented (2-3 categories)
- All REMEMVR profiles represented (typically 3-4 categories)
- No missing profile assignments in merged data
- Contingency table internally consistent (marginals match)

*Log Validation:*
- Required patterns: "Profile merge complete", "Contingency table created", "Expected frequency check complete"
- Forbidden patterns: "merge failed", "missing profiles", "empty cells critical"
- Acceptable warnings: "Some expected frequencies <5 noted"

**Expected Behavior on Validation Failure:**
Document merge issues, check if sample size adequate for analysis, quit if <80% successful merge rate

### Step 4: Test Profile Correspondence Association
**Dependencies:** Step 3 (contingency table prepared)
**Complexity:** Medium (~10 minutes including effect size)

**Purpose:** Test association between cognitive and REMEMVR profiles using chi-square and effect size analysis

**Input:**
- data/step03_profile_crosstab.csv (contingency table)
- Expected frequency validation from Step 3

**Processing:**
- **Primary association test:**
  - Chi-square test of independence using scipy.stats.chi2_contingency
  - Extract chi-square statistic, degrees of freedom, p-value
  - Random seed: 42 (though deterministic test)
- **Sparse cell remedial action (addresses stats concern):**
  - If any expected frequency <5: use Fisher's exact test as primary
  - Report both chi-square and Fisher's exact when applicable  
  - Document which cells caused sparse condition
- **Multiple comparison correction (Decision D068):**
  - Family: Chapter 7 family-wise correction
  - Bonferroni: alpha = 0.05/28 = 0.00179 per test
  - Report BOTH uncorrected AND corrected p-values (Decision D068 mandate)
  - Format: p_uncorrected = X.XXX, p_bonferroni = X.XXX
- **Effect size analysis:**
  - Cramer's V for association strength
  - Bootstrap 95% CI for Cramer's V:
    - Iterations: 1000
    - Random seed: 42
    - Resample participants with replacement
    - Percentile method CI (2.5th, 97.5th percentiles)
  - Interpret magnitude: 0.10=small, 0.30=medium, 0.50=large
- **Pattern identification:**
  - Standardized residuals >|2| indicate significant cell contributions
  - Identify which cognitive-REMEMVR combinations over/under-represented

**Output:**
- data/step04_association_test.csv (chi-square results, dual p-values, effect size)
- data/step04_effect_size_bootstrap.csv (Cramer's V CI details)

**Validation Requirement:**
Validation tools MUST be used after association testing execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_association_test.csv: 1 row x 8 columns (chi2, df, p_uncorrected, p_bonferroni, cramers_v, ci_lower, ci_upper, sparse_test)
- data/step04_effect_size_bootstrap.csv: bootstrap distribution details
- Test results include both chi-square and Fisher's exact if needed

*Value Ranges:*
- Chi-square statistic: >0 (non-negative)
- p-values: 0.0 to 1.0 (valid probability range)
- Cramer's V: 0.0 to 1.0 (effect size bounds)
- Degrees of freedom: (K_cognitive-1) x (K_rememvr-1)

*Data Quality:*
- Both uncorrected and corrected p-values present (Decision D068)
- Cramer's V confidence interval valid (ci_lower < cramers_v < ci_upper)
- Bootstrap completed successfully (1000 iterations)
- Sparse cell handling documented if applicable

*Log Validation:*
- Required patterns: "Chi-square test complete", "Cramer's V computed", "Bootstrap CI complete"
- Forbidden patterns: "ERROR", "test failed", "invalid statistics"
- Acceptable warnings: "Fisher's exact used due to sparse cells"

**Expected Behavior on Validation Failure:**
Document test failures, check data integrity, quit if fundamental statistical computation fails

### Step 5: Interpret Correspondence Patterns and Generate Summary
**Dependencies:** Step 4 (association test completed)  
**Complexity:** Low (~5 minutes)

**Purpose:** Interpret correspondence patterns and assess theoretical coherence of associations

**Input:**
- data/step03_profile_crosstab.csv (contingency table with residuals)
- data/step03_conditional_probabilities.csv (prediction patterns)
- data/step04_association_test.csv (association strength)
- Theoretical predictions from concept (verbal→What, spatial→Where)

**Processing:**
- **Pattern analysis:**
  - Identify strongest associations using standardized residuals
  - Calculate prediction accuracy: P(REMEMVR profile | cognitive profile) > chance
  - Compare observed patterns to theoretical predictions
  - Document correspondence vs. divergence from hypotheses
- **Theoretical assessment:**
  - Evaluate whether patterns support cognitive specialization theory
  - Identify unexpected associations requiring interpretation
  - Assess overall correspondence quality (>60% above chance threshold)
- **Effect size interpretation:**
  - Interpret Cramer's V magnitude using standard conventions
  - Assess practical significance beyond statistical significance
  - Consider confidence interval overlap with meaningful effect thresholds
- **Summary generation:**
  - Create narrative summary of key findings
  - Document primary correspondences and their strength
  - Acknowledge limitations and interpretation caveats
  - Note implications for REMEMVR external validity

**Output:**
- data/step05_correspondence_interpretation.csv (pattern analysis results)
- data/step05_theoretical_assessment.txt (narrative interpretation)

**Validation Requirement:**
Validation tools MUST be used after pattern interpretation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_correspondence_interpretation.csv: pattern analysis with theoretical comparisons
- data/step05_theoretical_assessment.txt: narrative summary of findings
- Interpretation addresses both statistical and practical significance

*Value Ranges:*
- Prediction accuracy: 0.33 to 1.0 (above chance for 3-way classification)
- Correspondence strength: qualitative assessment based on Cramer's V
- N/A for narrative text file

*Data Quality:*
- All cognitive-REMEMVR combinations interpreted
- Theoretical predictions explicitly addressed
- Statistical significance and effect size both interpreted
- Limitations acknowledged appropriately

*Log Validation:*
- Required patterns: "Pattern analysis complete", "Theoretical assessment complete"
- Forbidden patterns: "interpretation failed", "missing analysis"
- Acceptable warnings: "Some patterns diverge from theory"

**Expected Behavior on Validation Failure:**
Continue with partial interpretation, document missing elements, ensure minimum viable summary produced

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (prerequisite verification)
- data/step01_cognitive_lpa_input.csv (standardized cognitive T-scores)  
- data/step01_cognitive_descriptives.csv (descriptive statistics)
- data/step02_lpa_model_comparison.csv (model selection results)
- data/step02_cognitive_profile_classifications.csv (LPA classifications)
- data/step02_profile_descriptives.csv (profile characteristics)
- data/step02_split_sample_validation.csv (stability assessment)
- data/step03_merged_profile_data.csv (combined profile assignments)
- data/step03_profile_crosstab.csv (contingency table)
- data/step03_conditional_probabilities.csv (prediction patterns)
- data/step04_association_test.csv (chi-square and effect size results)
- data/step04_effect_size_bootstrap.csv (Cramer's V confidence intervals)
- data/step05_correspondence_interpretation.csv (pattern analysis)
- data/step05_theoretical_assessment.txt (narrative summary)

### Logs (ONLY execution logs)
- logs/step00_dependency_validation.log
- logs/step01_extract_cognitive.log
- logs/step02_cognitive_lpa.log
- logs/step03_merge_profiles.log
- logs/step04_test_association.log
- logs/step05_interpret_patterns.log

### Plots (EMPTY until rq_plots runs)
Plot source CSV files created in data/:
- data/step02_lpa_plot_data.csv (profile means for visualization)
- data/step03_crosstab_plot_data.csv (heatmap source data)
- data/step04_effect_size_plot_data.csv (CI visualization data)

### Results (EMPTY until rq_results runs)
Final summary.md will be created by rq_results agent

---

## Expected Data Formats

### Step-to-Step Transformations

**Raw Cognitive Tests → T-Scores (Step 1):**
- Input: RAVLT_total, BVMT_total, RPM_total (raw scores)
- Transform: Standardize within-test (M=50, SD=10)
- Output: RAVLT_T, BVMT_T, RPM_T (standardized)

**T-Scores → LPA Profiles (Step 2):**  
- Input: Matrix of cognitive T-scores (N x 3)
- Transform: Latent profile analysis with model selection
- Output: Profile assignments + probabilities

**Profile Classifications → Contingency Analysis (Steps 3-4):**
- Input: Cognitive profiles + REMEMVR profiles (categorical)
- Transform: Cross-tabulation → Association testing
- Output: Chi-square statistics + effect sizes

### Column Naming Conventions

**Profile Classification Variables:**
- cognitive_profile: integer 1 to K (cognitive profile number)  
- rememvr_profile: integer 1 to K (REMEMVR profile number)
- max_prob: float 0-1 (maximum posterior probability for assignment)

**Statistical Results Variables:**
- p_uncorrected: float (raw p-value)
- p_bonferroni: float (Bonferroni-corrected p-value) 
- cramers_v: float (effect size)
- ci_lower, ci_upper: float (95% confidence bounds)

### Data Type Constraints

**Required Non-Nullable:**
- participant IDs (string/object)
- profile assignments (integer)
- test statistics (float64)

**Acceptable Missing:**
- secondary interpretation variables (if analysis incomplete)
- some bootstrap samples (if computational limits reached)

---

## Cross-RQ Dependencies

**Dependency:** RQ 7.8.1 (REMEMVR Latent Profile Analysis)

**Required Files:**
- Primary: results/ch7/7.8.1/data/step03_rememvr_profile_classifications.csv
- Alternative: results/ch7/7.8.1/data/rememvr_profiles.csv
- Fallback pattern: results/ch7/7.8.1/data/*profile*.csv
- Last resort: results/ch7/7.8.1/data/*lpa*.csv

**Expected Content:**
- Participant ID column (character)
- REMEMVR profile assignments (integer 1-K)  
- Profile probabilities or confidence measures (optional)
- Sample size approximately N=100

**Circuit Breaker:**
If RQ 7.8.1 outputs not found: QUIT with error message "RQ 7.8.1 REMEMVR profile analysis must complete before external validation can proceed"

**Master.xlsx Dependency:**
- Location: data/cache/master.xlsx
- Required columns: participant_id, RAVLT_total, BVMT_total, RPM_total
- Expected data types: ID (string), test scores (numeric)
- If not accessible: QUIT with "Cognitive test data not available in master.xlsx"

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

**Validation Architecture Integration:**
The 4-layer validation structure is embedded directly in each step specification above. rq_inspect will use these criteria to validate outputs match expectations without requiring separate validation planning.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
**Substance validation criteria fully specified above** - 4-layer structure with output files, value ranges, data quality, and log patterns.

#### Step 1: Extract Cognitive Data  
**Substance validation criteria fully specified above** - Validates T-score standardization, sample size, missing data handling.

#### Step 2: Fit Cognitive LPA
**Substance validation criteria fully specified above** - Validates convergence, model selection, entropy thresholds, split-sample stability.

#### Step 3: Create Cross-Tabulation
**Substance validation criteria fully specified above** - Validates merge success, contingency table structure, conditional probabilities.

#### Step 4: Test Association
**Substance validation criteria fully specified above** - Validates chi-square results, dual p-values, Cramer's V with CI, sparse cell handling.

#### Step 5: Interpret Patterns
**Substance validation criteria fully specified above** - Validates pattern analysis, theoretical assessment, interpretation completeness.

---

## Summary

**Total Steps:** 6 (Step 0: validation + Steps 1-5: core analysis)
**Estimated Runtime:** 45-60 minutes
**Cross-RQ Dependencies:** RQ 7.8.1 (REMEMVR profiles) + master.xlsx (cognitive tests)
**Primary Outputs:** LPA model results + contingency analysis + correspondence assessment
**Validation Coverage:** 100% (all 6 steps have embedded 4-layer validation requirements)

**Key Hypothesis:** Verbal-dominant cognitive profiles will predict What-specialist REMEMVR profiles, spatial-dominant cognitive profiles will predict Where-specialist REMEMVR profiles.

**Critical Methodological Notes:**
- Cross-validation misapplication removed, replaced with split-sample validation per statistical feedback
- Sample size limitation (N=100) acknowledged, analysis focused on 2-3 profile solutions
- Multiple model selection criteria required (AIC, BIC, entropy, BLRT) not just BIC
- Sparse cell handling with Fisher's exact test fallback implemented
- Dual p-value reporting mandatory (Decision D068)
- Comprehensive convergence diagnostics with 500 random starts, seed=42

**Statistical Enhancements (v5.1 Compliance):**
- All random operations use seed=42 for reproducibility
- Bootstrap procedures: 1000 iterations, percentile method CIs
- Multiple comparison correction: Chapter-level Bonferroni (alpha=0.00179)
- Assumption violations: Explicit remedial actions specified
- Profile classification uncertainty acknowledged and assessed

---

**Next Steps (Workflow):**
1. User reviews and approves this plan  
2. rq_tools reads this plan → creates 3_tools.yaml
3. rq_analysis reads plan + tools → creates 4_analysis.yaml
4. g_code reads analysis → generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent v5.1
  - Addressed critical CV misapplication from stats validation
  - Enhanced convergence diagnostics and model selection
  - Implemented split-sample validation methodology
  - Added comprehensive sparse cell handling
  - Integrated v5.1 statistical specification requirements