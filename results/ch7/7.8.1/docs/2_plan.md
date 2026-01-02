# Analysis Plan: RQ 7.8.1 - Distinct REMEMVR memory profiles?

**Research Question:** 7.8.1
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines heterogeneity in episodic memory performance using Latent Profile Analysis (LPA) on standardized domain theta scores (What, Where, When) across 100 participants. The analysis systematically compares 1-4 profile solutions using multiple fit indices (BIC, AIC, entropy, LMR-LRT) to identify optimal number of distinct memory profiles, followed by external validation using cognitive tests.

**Pipeline:** Latent Profile Analysis with external validation
**Steps:** 7 total analysis steps (Step 0: validation + Steps 1-6: analysis)
**Estimated Runtime:** 45-60 minutes total

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- BIC as primary criterion for model selection
- Entropy > 0.80 threshold for classification quality
- Minimum n > 20 per profile for stability

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 domain theta score outputs exist before proceeding

**Input:**
- Primary: results/ch5/5.2.1/data/step03_theta_scores.csv (What domain)
- Primary: results/ch5/5.2.2/data/step03_theta_scores.csv (Where domain)
- Primary: results/ch5/5.2.3/data/step03_theta_scores.csv (When domain)
- Alternative: results/ch5/5.2.1/data/*theta*.csv (fallback pattern)
- Alternative: results/ch5/5.2.2/data/*theta*.csv (fallback pattern)
- Alternative: results/ch5/5.2.3/data/*theta*.csv (fallback pattern)
- Fallback: results/ch5/5.2.x/data/step*_domain_scores.csv
- Expected content: UID, theta_mean, se_mean columns for domain scores
- Validator: data/cache/master.xlsx (age, cognitive tests for external validation)
- If not found: QUIT with "Ch5 5.2.x domain outputs not found"

**Processing:**
- Check Ch5 5.2.1, 5.2.2, 5.2.3 status.yaml files (rq_results: success)
- Locate domain theta score files (try multiple patterns)
- Verify files contain theta estimates for all 100 participants
- Verify master.xlsx contains cognitive test scores (RAVLT, BVMT, RPM)
- Test file accessibility and format compatibility
- Log all validation checks with pass/fail status

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Expected lines: 8-12 lines of validation checks

*Value Ranges:*
- All validation checks should return "PASS" status
- File existence checks: 0 (missing) or 1 (found)
- Participant counts: 100 (expected N)

*Data Quality:*
- All 3 domain files accessible and readable
- Master.xlsx contains required columns
- No critical missing dependencies

*Log Validation:*
- Required pattern: "Dependency validation complete"
- Required pattern: "Ch5 domain outputs: FOUND"
- Required pattern: "Master.xlsx validation: PASS"
- Forbidden patterns: "CRITICAL ERROR", "FILE NOT FOUND"

**Expected Behavior on Validation Failure:**
- Raise error with specific missing dependency
- Log to logs/step00_validate_dependencies.log
- Quit immediately, invoke g_debug for missing files

### Step 1: Extract and Prepare Domain Theta Scores
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (<5 minutes)

**Purpose:** Load domain-specific theta scores from Ch5 outputs and prepare for LPA analysis

**Input:**
- results/ch5/5.2.1/data/step03_theta_scores.csv (What domain theta scores)
- results/ch5/5.2.2/data/step03_theta_scores.csv (Where domain theta scores)
- results/ch5/5.2.3/data/step03_theta_scores.csv (When domain theta scores)
- Expected format: UID, theta_mean, se_mean columns per domain

**Processing:**
- Load three domain theta score files
- Merge on UID to create single dataset
- Rename columns: theta_What, theta_Where, theta_When
- Check for missing participants (expect N=100)
- Apply z-score standardization (grand mean=0, SD=1) for comparable scaling
- Implementation: scipy.stats.zscore for each domain
- Verify standardization: check means ~0, SDs ~1
- Handle any missing data (listwise deletion if <5% missing)
- Export standardized scores for LPA input

**Output:**
- data/step01_domain_theta_scores.csv (standardized scores ready for LPA)
- data/step01_standardization_summary.txt (means, SDs, missing data report)

**Validation Requirement:**
Validation tools MUST be used after data extraction and standardization.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_domain_theta_scores.csv: 100 rows x 4 columns (UID, theta_What, theta_Where, theta_When)
- Data types: UID (object), theta_* (float64)
- data/step01_standardization_summary.txt: summary statistics

*Value Ranges:*
- Standardized theta scores approximately in [-3, 3] range (99% within)
- Means approximately 0.0 (+/- 0.1 tolerance)
- Standard deviations approximately 1.0 (+/- 0.1 tolerance)

*Data Quality:*
- All 100 participants present (no missing UIDs)
- No duplicate UIDs
- Missing data < 5% per domain (prefer 0% for compulsory items)
- No extreme outliers (|z| > 4) without documentation

*Log Validation:*
- Required pattern: "Standardization complete: means ~0, SDs ~1"
- Required pattern: "N=100 participants with complete data"
- Forbidden patterns: "ERROR", "FAIL", "Missing data >5%"

**Expected Behavior on Validation Failure:**
- Raise error with specific data quality issue
- Log to logs/step01_extract_prepare_data.log
- Quit if critical issues, continue with warnings for minor issues

### Step 2: Fit LPA Models for K=1,2,3,4 Profiles
**Dependencies:** Step 1 (standardized domain scores)
**Complexity:** High (~15 minutes including multiple random starts)

**Purpose:** Fit Latent Profile Analysis models with 1-4 profiles to identify optimal number of distinct memory profiles

**Input:**
- data/step01_domain_theta_scores.csv (standardized What, Where, When scores)
- Expected format: UID + 3 standardized domain scores

**Processing:**
- Implement LPA using mixture models (sklearn.mixture.GaussianMixture or R mclust interface)
- Fit models for K=1, 2, 3, 4 profiles
- Multiple random starts per model:
  - Iterations: 100 random starts per K
  - Random seed: 42 for reproducibility
  - Convergence criterion: log-likelihood change < 1e-6
- Extract fit indices for each K:
  - Log-likelihood, AIC, BIC
  - Entropy for classification quality
  - Sample sizes per profile
- Model selection criteria:
  - Primary: BIC minimum (lower is better)
  - Secondary: LMR-LRT test (if available)
  - Tertiary: Entropy > 0.80 and interpretability
- Check convergence across random starts (consistent solutions)
- Export model comparison table and selected optimal K

**Output:**
- data/step02_lpa_fit_comparison.csv (fit indices for K=1,2,3,4)
- data/step02_optimal_model_selection.txt (selection rationale and optimal K)
- data/step02_model_objects.pkl (fitted model objects for downstream use)

**Validation Requirement:**
Validation tools MUST be used after LPA model fitting and comparison.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_lpa_fit_comparison.csv: 4 rows x 6 columns (K, LogLik, AIC, BIC, Entropy, ProfileSizes)
- Data types: K (int), fit indices (float64)
- data/step02_optimal_model_selection.txt: text summary with selected K

*Value Ranges:*
- K values: 1, 2, 3, 4 (all models fitted)
- BIC values: decreasing then increasing pattern expected
- Entropy values in [0, 1] range (higher is better)
- Log-likelihood: negative values, increasing with K

*Data Quality:*
- All 4 models converged successfully
- Entropy > 0.80 for optimal model (classification quality threshold)
- No profiles with n < 10 (avoid degenerate solutions)
- Consistent solutions across random starts

*Log Validation:*
- Required pattern: "LPA models fitted for K=1,2,3,4"
- Required pattern: "Optimal model selected: K=X"
- Required pattern: "Convergence achieved: 100 random starts"
- Forbidden patterns: "Convergence failed", "Degenerate solution"

**Expected Behavior on Validation Failure:**
- Raise error with specific convergence issue
- Log to logs/step02_fit_lpa_models.log
- Retry with different starting values if convergence fails

### Step 3: Extract and Characterize Optimal Profiles
**Dependencies:** Step 2 (optimal LPA model)
**Complexity:** Medium (~8 minutes)

**Purpose:** Extract profile membership and characterize profiles using domain score patterns

**Input:**
- data/step01_domain_theta_scores.csv (standardized domain scores)
- data/step02_model_objects.pkl (optimal fitted LPA model)
- data/step02_optimal_model_selection.txt (selected K value)

**Processing:**
- Load optimal LPA model (selected K)
- Extract profile membership for each participant
- Extract posterior probabilities for profile assignment
- Compute profile characteristics:
  - Mean theta scores per domain per profile
  - Standard deviations per domain per profile
  - Profile sizes and proportions
- Label profiles based on domain patterns:
  - High/medium/low thresholds: +0.5, -0.5 standardized units
  - Example labels: "Generalists", "What-specialists", "Low-performers"
- Assess classification quality:
  - Average posterior probability per profile
  - Entropy calculation verification
  - Profile separation assessment
- Export profile membership and characteristics

**Output:**
- data/step03_profile_membership.csv (UID, assigned_profile, posterior_probs)
- data/step03_profile_characteristics.csv (profile means, SDs, sizes, labels)
- data/step03_classification_quality.txt (entropy, separation metrics)

**Validation Requirement:**
Validation tools MUST be used after profile extraction and characterization.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_profile_membership.csv: 100 rows x 4+ columns (UID, profile, prob_profile1, prob_profile2, etc.)
- data/step03_profile_characteristics.csv: K rows x 8 columns (profile, label, mean_What, mean_Where, mean_When, SD_What, SD_Where, SD_When, n_size)
- Data types: profile (int), probabilities (float64), means/SDs (float64)

*Value Ranges:*
- Profile numbers: 1 to K (sequential numbering)
- Posterior probabilities in [0, 1] range, sum to 1.0 per participant
- Mean domain scores in standardized units (approximately [-2, 2])
- Profile sizes: all n > 20 (minimum for stability)

*Data Quality:*
- All 100 participants assigned to profiles
- Sum of profile sizes equals 100
- Average posterior probability > 0.80 (classification quality)
- Profile labels theoretically meaningful

*Log Validation:*
- Required pattern: "Profile extraction complete: K profiles"
- Required pattern: "Classification quality: entropy > 0.80"
- Required pattern: "All profiles n > 20"
- Forbidden patterns: "Degenerate profile", "Poor classification"

**Expected Behavior on Validation Failure:**
- Raise error with specific classification issue
- Log to logs/step03_extract_characterize_profiles.log
- Document profile quality concerns for interpretation

### Step 4: Prepare External Validation Data
**Dependencies:** Step 3 (profile membership) 
**Complexity:** Low (~5 minutes)

**Purpose:** Load cognitive test scores and demographic data for external validation of profiles

**Input:**
- data/step03_profile_membership.csv (profile assignments)
- data/cache/master.xlsx (cognitive tests, age data)
- Expected validators: age, RAVLT_T, BVMT_T, RPM_T scores

**Processing:**
- Load master.xlsx and extract validation variables
- Merge with profile membership data on UID
- Check for missing validator data
- Compute descriptive statistics per profile:
  - Age: mean, SD, range per profile
  - Cognitive tests: mean, SD per profile per test
- Test assumptions for group comparisons:
  - Normality: Shapiro-Wilk test per validator per profile
  - Homogeneity: Levene test for equal variances
- Document assumption violations for remedial actions
- Prepare data for ANOVA/Kruskal-Wallis tests

**Output:**
- data/step04_validation_data.csv (merged profile + validator data)
- data/step04_descriptives_by_profile.csv (means, SDs per profile per validator)
- data/step04_assumption_checks.txt (normality, homogeneity test results)

**Validation Requirement:**
Validation tools MUST be used after external validation data preparation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_validation_data.csv: 100 rows x 7+ columns (UID, profile, age, RAVLT_T, BVMT_T, RPM_T, etc.)
- Data types: UID (object), profile (int), validators (float64)
- data/step04_descriptives_by_profile.csv: K profiles x validators summary

*Value Ranges:*
- Age in [18, 89] range (study inclusion criteria)
- Cognitive T-scores approximately [20, 80] (standard T-score range)
- All validators should have valid numeric values

*Data Quality:*
- All 100 participants with profile assignments
- Cognitive test data available for all participants
- Missing validator data < 5% (prefer 0% for key validators)
- Age distribution balanced across profiles

*Log Validation:*
- Required pattern: "External validation data merged successfully"
- Required pattern: "Assumption checks completed"
- Required pattern: "N=100 with complete validator data"
- Forbidden patterns: "Critical missing data", "Merge failed"

**Expected Behavior on Validation Failure:**
- Raise error with specific data quality issue
- Log to logs/step04_prepare_validation_data.log
- Document missing data patterns for interpretation

### Step 5: Test Profile Differences on External Validators
**Dependencies:** Step 4 (validation data with assumption checks)
**Complexity:** Medium (~10 minutes including corrections)

**Purpose:** Test whether profiles differ significantly on age and cognitive test performance

**Input:**
- data/step04_validation_data.csv (profiles + validators)
- data/step04_assumption_checks.txt (normality, homogeneity results)

**Processing:**
- For each validator (age, RAVLT_T, BVMT_T, RPM_T):
  - If assumptions met: One-way ANOVA
  - If assumptions violated: Kruskal-Wallis test
  - Report BOTH parametric and non-parametric results
- Implementation details:
  - ANOVA: scipy.stats.f_oneway
  - Kruskal-Wallis: scipy.stats.kruskal
  - Effect size: eta-squared for ANOVA, epsilon-squared for Kruskal-Wallis
- Post-hoc comparisons (if overall test significant):
  - Parametric: Tukey HSD for pairwise comparisons
  - Non-parametric: Dunn test with Bonferroni correction
- Multiple comparison corrections:
  - Family: Within-RQ (4 validators x K*(K-1)/2 pairwise comparisons)
  - Bonferroni: alpha = 0.05 / total_tests
  - Also compute FDR using Benjamini-Hochberg
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Effect size interpretations:
  - Small: eta² = 0.01, Medium: eta² = 0.06, Large: eta² = 0.14

**Output:**
- data/step05_profile_differences_omnibus.csv (ANOVA/KW results per validator)
- data/step05_profile_differences_pairwise.csv (post-hoc comparisons)
- data/step05_external_validation_summary.txt (interpretation of profile differences)

**Validation Requirement:**
Validation tools MUST be used after external validation testing.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_profile_differences_omnibus.csv: 4 rows x 8 columns (validator, statistic, df, p_uncorrected, p_bonferroni, p_fdr, effect_size, test_type)
- data/step05_profile_differences_pairwise.csv: K*(K-1)/2 rows per validator
- Data types: statistics (float64), p-values (float64), effect sizes (float64)

*Value Ranges:*
- All p-values in [0, 1] range
- Effect sizes in [0, 1] range for eta² and epsilon²
- Test statistics should be non-negative for F and H statistics

*Data Quality:*
- All 4 validators tested (age, RAVLT_T, BVMT_T, RPM_T)
- Both uncorrected and corrected p-values present (Decision D068)
- Effect size estimates provided for all significant tests
- Test type documented (parametric vs non-parametric)

*Log Validation:*
- Required pattern: "External validation complete: 4 validators tested"
- Required pattern: "Dual p-value reporting: uncorrected + corrected"
- Required pattern: "Post-hoc tests: pairwise comparisons complete"
- Forbidden patterns: "Test failed", "Assumption violation unhandled"

**Expected Behavior on Validation Failure:**
- Raise error with specific statistical test failure
- Log to logs/step05_test_profile_differences.log
- Document assumption violations and remedial actions taken

### Step 6: Model Diagnostics and Classification Quality Assessment
**Dependencies:** Steps 3, 5 (profile characteristics and validation results)
**Complexity:** Medium (~8 minutes including bootstrap)

**Purpose:** Comprehensive assessment of LPA model quality and profile stability

**Input:**
- data/step02_model_objects.pkl (fitted LPA models)
- data/step03_profile_membership.csv (profile assignments)
- data/step01_domain_theta_scores.csv (original standardized data)

**Processing:**
- Convergence diagnostics:
  - Check log-likelihood stability across random starts
  - Identify any local maxima issues
  - Report convergence rate across 100 starts
- Classification quality assessment:
  - Entropy calculation verification (formula: -sum(p*log(p)))
  - Average posterior probability per participant
  - Confusion matrix for hard vs soft classification
- Local independence testing:
  - Compute profile-conditional correlations between domains
  - Threshold: correlations < 0.2 within profiles
  - Report any violations of local independence assumption
- Profile stability assessment:
  - Bootstrap stability (if computationally feasible):
    - Iterations: 100 bootstrap samples
    - Random seed: 42 for reproducibility
    - Resampling unit: participant-level with replacement
    - Track profile solution consistency across samples
- Model comparison robustness:
  - Sensitivity analysis: BIC differences between models
  - BIC weight calculation for model uncertainty
  - Report model selection confidence

**Output:**
- data/step06_model_diagnostics.csv (convergence, entropy, correlations)
- data/step06_classification_quality.txt (posterior probabilities, confusion matrix)
- data/step06_bootstrap_stability.csv (profile stability across bootstrap samples)

**Validation Requirement:**
Validation tools MUST be used after model diagnostics and quality assessment.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_model_diagnostics.csv: diagnostic metrics summary
- data/step06_classification_quality.txt: classification assessment report
- data/step06_bootstrap_stability.csv: bootstrap stability results

*Value Ranges:*
- Entropy values in [0, 1] range, optimal model > 0.80
- Posterior probabilities in [0, 1] range per participant
- Profile-conditional correlations in [-1, 1], preferably < 0.2
- Bootstrap stability proportions in [0, 1]

*Data Quality:*
- All convergence checks completed successfully
- Local independence assumption evaluated
- Classification quality meets entropy threshold
- Bootstrap stability assessment (if computed) shows consistent solutions

*Log Validation:*
- Required pattern: "Model diagnostics complete"
- Required pattern: "Classification quality: entropy = X.XX"
- Required pattern: "Local independence: correlations < 0.2"
- Forbidden patterns: "Convergence failure", "Poor classification quality"

**Expected Behavior on Validation Failure:**
- Raise error with specific diagnostic failure
- Log to logs/step06_model_diagnostics.log
- Document model quality concerns for interpretation

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (prerequisite checks)
- data/step01_domain_theta_scores.csv (standardized What/Where/When scores)
- data/step01_standardization_summary.txt (standardization diagnostics)
- data/step02_lpa_fit_comparison.csv (model fit indices K=1,2,3,4)
- data/step02_optimal_model_selection.txt (model selection rationale)
- data/step02_model_objects.pkl (fitted LPA models)
- data/step03_profile_membership.csv (participant profile assignments)
- data/step03_profile_characteristics.csv (profile domain score patterns)
- data/step03_classification_quality.txt (entropy, posterior probabilities)
- data/step04_validation_data.csv (profiles + cognitive tests + age)
- data/step04_descriptives_by_profile.csv (validator means/SDs per profile)
- data/step04_assumption_checks.txt (ANOVA/KW assumption tests)
- data/step05_profile_differences_omnibus.csv (overall group differences)
- data/step05_profile_differences_pairwise.csv (post-hoc pairwise comparisons)
- data/step05_external_validation_summary.txt (profile difference interpretation)
- data/step06_model_diagnostics.csv (convergence, entropy, correlations)
- data/step06_classification_quality.txt (classification assessment)
- data/step06_bootstrap_stability.csv (profile stability assessment)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_prepare_data.log
- logs/step02_fit_lpa_models.log
- logs/step03_extract_characterize_profiles.log
- logs/step04_prepare_validation_data.log
- logs/step05_test_profile_differences.log
- logs/step06_model_diagnostics.log

### Plots (EMPTY until rq_plots runs)
- Note: Profile visualization CSVs created in data/ folder for subsequent plotting
- step03_profile_characteristics.csv (for profile pattern plots)
- step04_descriptives_by_profile.csv (for validator comparison plots)

### Results (EMPTY until rq_results runs)
- Note: summary.md will be created by rq_results agent

---

## Expected Data Formats

### Step-to-Step Transformations
1. Step 0→1: Dependency validation → Raw domain theta scores
2. Step 1→2: Standardized theta scores → LPA model inputs
3. Step 2→3: Fitted models → Profile assignments and characteristics
4. Step 3→4: Profile membership → Merged with validators
5. Step 4→5: Validation dataset → Statistical test results
6. Step 5→6: Test results → Model diagnostics and stability

### Column Naming Conventions
- **Participant ID:** UID (consistent across all files)
- **Domain scores:** theta_What, theta_Where, theta_When (standardized)
- **Profile variables:** profile (1 to K), prob_profile1, prob_profile2, etc.
- **Validators:** age, RAVLT_T, BVMT_T, RPM_T
- **Statistics:** p_uncorrected, p_bonferroni, p_fdr (dual reporting per D068)

### Data Type Constraints
- **UID:** object (string), non-nullable, unique
- **Theta scores:** float64, nullable only if <5% missing
- **Profile assignments:** int, range 1 to K, non-nullable
- **Probabilities:** float64, range [0,1], sum to 1.0 per participant
- **Test statistics:** float64, non-negative for F and H statistics
- **P-values:** float64, range [0,1], non-nullable

---

## Cross-RQ Dependencies

**Primary Dependencies:**
- Ch5 5.2.1: What domain theta scores (results/ch5/5.2.1/data/step03_theta_scores.csv)
- Ch5 5.2.2: Where domain theta scores (results/ch5/5.2.2/data/step03_theta_scores.csv)  
- Ch5 5.2.3: When domain theta scores (results/ch5/5.2.3/data/step03_theta_scores.csv)

**File Discovery Strategy:**
- Primary paths as listed above
- Fallback patterns: results/ch5/5.2.x/data/*theta*.{csv,txt}
- Alternative patterns: results/ch5/5.2.x/data/step*_domain_scores.csv
- Must contain: UID, theta_mean, se_mean columns

**External Data:**
- data/cache/master.xlsx: cognitive test scores and demographics
- Required columns: UID, age, RAVLT_T, BVMT_T, RPM_T

**Dependency Validation:**
All dependencies verified in Step 0 with circuit breaker if critical files missing.

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
- 4-layer validation for dependency verification
- File existence, accessibility, format validation
- Circuit breaker for missing critical dependencies

#### Step 1: Extract and Prepare Data
- 4-layer validation for data extraction and standardization
- Participant counts, missing data, standardization quality
- Value range and distribution checks

#### Step 2: Fit LPA Models
- 4-layer validation for model fitting and selection
- Convergence verification, fit index validation
- Model selection criteria and optimal K verification

#### Step 3: Extract and Characterize Profiles
- 4-layer validation for profile extraction and characterization
- Classification quality, profile sizes, posterior probabilities
- Theoretical interpretability of profile patterns

#### Step 4: Prepare External Validation Data
- 4-layer validation for validator data preparation
- Merge success, missing data assessment, assumption testing
- Validator variable distributions and quality

#### Step 5: Test Profile Differences
- 4-layer validation for external validation testing
- Statistical test execution, dual p-value reporting
- Effect size calculation and interpretation

#### Step 6: Model Diagnostics and Quality
- 4-layer validation for comprehensive model assessment
- Convergence diagnostics, classification quality verification
- Local independence and stability assessment

---

## Summary

**Total Steps:** 7 (Step 0: validation + Steps 1-6: analysis)
**Estimated Runtime:** 45-60 minutes total
**Cross-RQ Dependencies:** Ch5 5.2.1, 5.2.2, 5.2.3 (domain theta scores)
**Primary Outputs:** Profile membership, characteristics, external validation results
**Validation Coverage:** 100% (all 7 steps have 4-layer validation requirements)

**Key Hypothesis:** Expect 2-4 distinct memory profiles representing different patterns of strength/weakness across episodic memory domains (What/Where/When)

**Critical Methodological Notes:**
- LPA assumes local independence within profiles (will be tested)
- Sample size N=100 may limit stability for 4-profile solutions
- BIC primary criterion with entropy >0.80 secondary threshold
- Bootstrap stability assessment for profile reliability
- Decision D068 compliance: dual p-value reporting throughout
- Random seed=42 for all randomized procedures (reproducibility)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan → creates 3_tools.yaml (specify LPA tools needed)
3. rq_analysis reads plan + tools → creates 4_analysis.yaml
4. g_code reads analysis → generates executable code

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent
  - Enhanced v5.1 specifications with statistical implementation details
  - Random seeds, bootstrap parameters, assumption testing
  - Cross-validation approach adapted for LPA methodology
  - Comprehensive 4-layer validation requirements