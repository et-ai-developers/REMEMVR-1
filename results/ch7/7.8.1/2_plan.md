# Analysis Plan: RQ 7.8.1 - Distinct REMEMVR memory profiles?

**Research Question:** 7.8.1
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

**Pipeline:** Latent Profile Analysis (LPA) with external validation
**Steps:** 7 total analysis steps (Step 0: validation + Steps 1-6: analysis)
**Estimated Runtime:** ~45 minutes total

This RQ examines heterogeneity in episodic memory profiles using Latent Profile Analysis on standardized theta scores from three domains (What, Where, When) across 100 participants. Analysis compares K=1-4 profile solutions using BIC, AIC, entropy, and LMR-LRT to identify optimal number of distinct memory profiles with external validation using cognitive tests.

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies

**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 domain-specific outputs exist before proceeding

**Input:**
- Primary: results/ch5/5.2.1/data/step03_theta_scores.csv (What domain)
- Primary: results/ch5/5.2.2/data/step03_theta_scores.csv (Where domain)
- Primary: results/ch5/5.2.3/data/step03_theta_scores.csv (When domain)
- Alternative: results/ch5/5.2.1/data/*theta*.csv (What domain fallback)
- Alternative: results/ch5/5.2.2/data/*theta*.csv (Where domain fallback)
- Alternative: results/ch5/5.2.3/data/*theta*.csv (When domain fallback)
- Fallback: data/cache/master.xlsx (for cognitive validation variables)
- Expected content: Participant UIDs with mean theta scores per domain

**Processing:**
- Check Ch5 5.2.1, 5.2.2, 5.2.3 completed successfully (status.yaml verification)
- Locate domain-specific theta score files (try multiple patterns)
- Verify files contain 100 participants with UID and theta columns
- Check master.xlsx accessibility for cognitive test scores
- Log all validation checks with specific file paths found

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Contains: 6+ lines documenting each file check

*Value Ranges:*
- N/A (validation step, no numerical outputs)

*Data Quality:*
- All 3 domain files found and verified
- master.xlsx accessible
- 100 participants confirmed across all domain files

*Log Validation:*
- Required patterns: "Ch5 dependencies: VALIDATED", "Files found: 4/4"
- Forbidden patterns: "ERROR", "File not found", "FAILED"
- Expected warnings: None (should pass cleanly)

**Expected Behavior on Validation Failure:**
- Raise error with specific missing file
- Log to logs/step00_validate_dependencies.log
- Quit immediately with "DEPENDENCY VALIDATION FAILED"

### Step 1: Extract and Prepare Domain Theta Scores

**Dependencies:** Step 0 (validated dependencies)
**Complexity:** Low (~5 minutes)

**Purpose:** Extract and combine domain-specific theta scores into analysis-ready dataset

**Input:**
- results/ch5/5.2.1/data/step03_theta_scores.csv (What domain)
- results/ch5/5.2.2/data/step03_theta_scores.csv (Where domain)  
- results/ch5/5.2.3/data/step03_theta_scores.csv (When domain)

**Processing:**
- Load theta scores from all three domain files
- Extract columns: UID, mean_theta_across_time (aggregate T1-T4 performance)
- Merge datasets on UID to create wide-format LPA input
- Rename columns to: UID, theta_What, theta_Where, theta_When
- Apply z-score standardization (grand mean=0, SD=1) for comparable scaling
- Standardization method: (X - mean(X)) / sd(X) applied to each domain
- Check for missing data (should be none for compulsory items)
- Verify N=100 participants with complete data across all domains

**Output:**
- data/step01_domain_theta_scores.csv

**Validation Requirement:**
Validation tools MUST be used after data preparation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_domain_theta_scores.csv: 100 rows x 4 columns
- Columns: UID (object), theta_What (float64), theta_Where (float64), theta_When (float64)

*Value Ranges:*
- theta_What in [-4, 4] (standardized IRT scores)
- theta_Where in [-4, 4] (standardized IRT scores)
- theta_When in [-4, 4] (standardized IRT scores)
- All means approximately 0.0 (+/- 0.1)
- All standard deviations approximately 1.0 (+/- 0.1)

*Data Quality:*
- All 100 participants present (no missing UIDs)
- No duplicate UIDs
- No missing values in theta columns
- Standardization successful (mean~0, sd~1 per domain)

*Log Validation:*
- Required patterns: "Data merged: 100 participants", "Standardization complete: mean=0, sd=1"
- Forbidden patterns: "ERROR", "missing values", "merge failed"
- Expected warnings: None

**Expected Behavior on Validation Failure:**
- Raise error with specific data quality issue
- Log to logs/step01_prepare_theta_scores.log
- Quit immediately, invoke g_debug

### Step 2: Fit Latent Profile Analysis Models (K=1,2,3,4)

**Dependencies:** Step 1 (standardized domain theta scores)
**Complexity:** High (~15 minutes including model fitting)

**Purpose:** Fit LPA models with 1-4 profiles and compute fit indices for model selection

**Input:**
- data/step01_domain_theta_scores.csv

**Processing:**
- Implement LPA using R's mixtools or Python equivalent with standardized theta scores
- Fit models for K=1, 2, 3, 4 profile solutions
- Use multiple random starts for convergence: 100 random starts per model
- Random seed: 42 for reproducibility across all model fitting
- Extract fit indices for each model:
  - BIC (Bayesian Information Criterion) - lower is better
  - AIC (Akaike Information Criterion) - lower is better  
  - Entropy (classification uncertainty) - higher is better (>0.80 threshold)
  - LMR-LRT (Lo-Mendell-Rubin Likelihood Ratio Test) - test K vs K-1 profiles
- Check convergence: require consistent solutions across random starts
- Local independence check: profile-conditional correlations should be <0.2
- Bootstrap stability assessment: 100 bootstrap samples, seed=42
- For each bootstrap: resample participants with replacement, refit optimal model

**Output:**
- data/step02_lpa_fit_comparison.csv (fit indices by K)
- data/step02_lpa_convergence_diagnostics.txt
- data/step02_lpa_fitted_models.rds (model objects for later use)

**Validation Requirement:**
Validation tools MUST be used after LPA model fitting execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_lpa_fit_comparison.csv: 4 rows x 6 columns
- Columns: K, BIC, AIC, Entropy, LMR_LRT_p, Converged
- data/step02_lpa_convergence_diagnostics.txt: text file with convergence details

*Value Ranges:*
- K in [1, 2, 3, 4] (number of profiles)
- BIC > 0 (positive values, lower is better)
- AIC > 0 (positive values, lower is better)
- Entropy in [0, 1] (classification certainty)
- LMR_LRT_p in [0, 1] (p-values)
- Converged: TRUE/FALSE for each model

*Data Quality:*
- All 4 models (K=1,2,3,4) fitted successfully
- BIC shows clear minimum (identifiable best model)
- At least one model achieves Entropy > 0.80
- No convergence failures (Converged = TRUE for all models)

*Log Validation:*
- Required patterns: "LPA complete: 4 models fitted", "Bootstrap stability: 100 iterations"
- Required patterns: "Convergence achieved for K=1,2,3,4"
- Forbidden patterns: "convergence failed", "ERROR", "local maxima"

**Expected Behavior on Validation Failure:**
- Raise error with specific convergence issue
- Log to logs/step02_fit_lpa_models.log
- Quit immediately, invoke g_debug

### Step 3: Select Optimal Profile Solution

**Dependencies:** Step 2 (fitted LPA models)
**Complexity:** Low (~5 minutes)

**Purpose:** Select optimal number of profiles using multiple criteria and extract profile membership

**Input:**
- data/step02_lpa_fit_comparison.csv
- data/step02_lpa_fitted_models.rds

**Processing:**
- Model selection hierarchy:
  1. Primary criterion: BIC minimum (most parsimonious fit)
  2. Secondary criterion: LMR-LRT significance (K vs K-1 comparison)
  3. Tertiary criterion: Entropy > 0.80 (good classification quality)
  4. Interpretability criterion: Profiles must have n >= 20 participants
- Apply selection rules systematically:
  - Start with BIC minimum
  - Verify LMR-LRT supports additional profiles
  - Confirm entropy threshold met
  - Check minimum profile sizes
- Extract optimal model details:
  - Profile membership (most likely profile per participant)
  - Posterior probabilities (classification confidence)
  - Profile sizes (n per profile)
- Assign interpretable profile labels based on domain patterns

**Output:**
- data/step03_optimal_profiles.csv
- data/step03_model_selection_summary.txt

**Validation Requirement:**
Validation tools MUST be used after model selection execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_optimal_profiles.csv: 100 rows x 4 columns
- Columns: UID, Profile, Max_Posterior_Prob, Profile_Label
- data/step03_model_selection_summary.txt: text summary of selection process

*Value Ranges:*
- Profile in [1, 2, 3, 4] (profile numbers)
- Max_Posterior_Prob in [0.5, 1.0] (classification confidence >50%)
- Profile_Label: character strings (interpretable names)

*Data Quality:*
- All 100 participants assigned to profiles
- All profiles have n >= 20 participants (adequate sample sizes)
- Mean posterior probability > 0.80 (good classification quality)
- Profile sizes reasonably balanced (largest/smallest ratio < 4.0)

*Log Validation:*
- Required patterns: "Optimal model: K=X profiles", "Entropy = X.XX", "All profiles n >= 20"
- Forbidden patterns: "No optimal solution", "Small profile warning", "ERROR"

**Expected Behavior on Validation Failure:**
- Raise error with specific selection issue
- Log to logs/step03_select_optimal_profiles.log
- Quit immediately, invoke g_debug

### Step 4: Characterize Profile Domain Patterns

**Dependencies:** Step 3 (optimal profile solution) + Step 1 (domain theta scores)
**Complexity:** Medium (~5 minutes)

**Purpose:** Compute mean domain scores per profile and assign interpretable labels

**Input:**
- data/step03_optimal_profiles.csv
- data/step01_domain_theta_scores.csv

**Processing:**
- Merge profile assignments with original domain theta scores
- Compute descriptive statistics by profile:
  - Mean and SD for theta_What, theta_Where, theta_When per profile
  - 95% confidence intervals using bootstrap
  - Bootstrap: 1000 iterations, seed=42, participant-level resampling
  - CI method: percentile (2.5th, 97.5th percentiles)
- Profile interpretation based on domain patterns:
  - High/low cutoffs: +/- 0.5 SD from grand mean
  - Label profiles based on relative domain strengths
  - Example labels: "Generalists", "What-specialists", "Low-performers"
- Within-profile correlations between domains (check local independence)
- Effect sizes: Cohen's d for between-profile differences per domain

**Output:**
- data/step04_profile_characteristics.csv
- data/step04_profile_interpretation.txt

**Validation Requirement:**
Validation tools MUST be used after profile characterization execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_profile_characteristics.csv: K rows x 12 columns
- Columns: Profile, N, What_Mean, What_SD, What_CI_Low, What_CI_High, Where_Mean, Where_SD, Where_CI_Low, Where_CI_High, When_Mean, When_SD, When_CI_High
- data/step04_profile_interpretation.txt: text file with profile descriptions

*Value Ranges:*
- N in [20, 80] (profile sizes, minimum 20 required)
- Domain means in [-2, 2] (standardized theta scores)
- SDs in [0.3, 1.5] (reasonable within-profile variation)
- CIs should contain means and show non-overlapping differences between profiles

*Data Quality:*
- Sum of profile Ns = 100 (all participants accounted for)
- Profiles show distinct patterns (at least 0.5 SD differences)
- Bootstrap CIs computed successfully for all statistics
- Profile labels reflect actual domain patterns

*Log Validation:*
- Required patterns: "Profile characterization complete", "Bootstrap CIs: 1000 iterations"
- Required patterns: "Distinct profiles identified"
- Forbidden patterns: "Overlapping profiles", "ERROR", "CI computation failed"

**Expected Behavior on Validation Failure:**
- Raise error with specific characterization issue
- Log to logs/step04_characterize_profiles.log
- Quit immediately, invoke g_debug

### Step 5: External Validation with Cognitive Tests

**Dependencies:** Step 3 (profile assignments) + master.xlsx (cognitive data)
**Complexity:** Medium (~10 minutes including multiple comparisons)

**Purpose:** Validate profile distinctions using external cognitive test scores and demographic variables

**Input:**
- data/step03_optimal_profiles.csv
- data/cache/master.xlsx (Age, RAVLT_T, BVMT_T, RPM_T)

**Processing:**
- Load cognitive test data and merge with profile assignments
- External validation variables:
  - Age (demographic validator)
  - RAVLT_T (verbal memory, standardized T-score)
  - BVMT_T (visual memory, standardized T-score)  
  - RPM_T (fluid intelligence, standardized T-score)
- Statistical tests for profile differences:
  - Primary: One-way ANOVA per validator variable
  - Assumption checks: Shapiro-Wilk normality, Levene homogeneity
  - Remedial action for violations: Kruskal-Wallis non-parametric alternative
- Multiple comparison corrections:
  - Family: Within-RQ external validation (4 validators x 1 test = 4 tests)
  - Bonferroni correction: alpha = 0.05/4 = 0.0125 per test
  - Also compute FDR using Benjamini-Hochberg procedure
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Effect sizes: eta-squared for ANOVA, epsilon-squared for Kruskal-Wallis
- Post-hoc pairwise comparisons with Bonferroni correction

**Output:**
- data/step05_external_validation.csv
- data/step05_external_validation_posthoc.csv

**Validation Requirement:**
Validation tools MUST be used after external validation execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_external_validation.csv: 4 rows x 8 columns
- Columns: Variable, F_stat, p_uncorrected, p_bonferroni, p_fdr, eta_squared, Test_Type, Assumption_Met
- data/step05_external_validation_posthoc.csv: variable number of pairwise comparisons

*Value Ranges:*
- F_stat > 0 (ANOVA F-statistics)
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1] (should be >= p_uncorrected)
- p_fdr in [0, 1] (between uncorrected and Bonferroni)
- eta_squared in [0, 1] (effect sizes)

*Data Quality:*
- All 4 validation variables tested
- Dual p-value reporting complete (Decision D068)
- At least one significant profile difference (validates distinct profiles)
- Post-hoc tests completed for significant ANOVAs

*Log Validation:*
- Required patterns: "External validation: 4 tests complete", "Dual p-values reported"
- Required patterns: "Bonferroni correction: alpha = 0.0125"
- Forbidden patterns: "No profile differences", "ERROR", "validation failed"

**Expected Behavior on Validation Failure:**
- Raise error with specific validation issue
- Log to logs/step05_external_validation.log
- Quit immediately, invoke g_debug

### Step 6: Classification Quality and Model Diagnostics

**Dependencies:** Step 2 (fitted models) + Step 3 (optimal solution)
**Complexity:** Medium (~5 minutes)

**Purpose:** Assess LPA model quality, classification accuracy, and provide comprehensive diagnostics

**Input:**
- data/step02_lpa_fitted_models.rds
- data/step03_optimal_profiles.csv

**Processing:**
- Classification quality metrics:
  - Overall entropy (classification uncertainty)
  - Average posterior probabilities by profile
  - Minimum posterior probability (worst classification)
  - Proportion classified with >80% confidence
- Model diagnostics:
  - Local independence: profile-conditional correlations between domains
  - Convergence stability: consistency across random starts
  - Bootstrap profile stability: classification agreement across bootstrap samples
  - Sensitivity analysis: compare K-1 and K+1 solutions
- Profile separation assessment:
  - Mahalanobis distances between profile centroids
  - Overlap indices between profiles
  - Silhouette coefficients for profile coherence
- Final model summary with interpretation guidelines

**Output:**
- data/step06_classification_quality.csv
- data/step06_model_diagnostics.txt

**Validation Requirement:**
Validation tools MUST be used after classification quality assessment execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_classification_quality.csv: multiple rows with quality metrics
- data/step06_model_diagnostics.txt: comprehensive text summary

*Value Ranges:*
- Entropy in [0.6, 1.0] (acceptable classification quality)
- Mean_Posterior_Prob in [0.8, 1.0] (good classification confidence)
- Min_Posterior_Prob in [0.5, 1.0] (minimum acceptable classification)
- Profile_Separation > 1.0 (adequate separation)

*Data Quality:*
- Entropy > 0.80 achieved (good classification)
- >90% of participants classified with >80% confidence
- Local independence satisfied (correlations <0.2)
- Bootstrap stability demonstrates consistent profile recovery

*Log Validation:*
- Required patterns: "Classification quality: EXCELLENT", "Bootstrap stability: CONFIRMED"
- Required patterns: "Local independence: SATISFIED"
- Forbidden patterns: "Poor classification", "Unstable profiles", "ERROR"

**Expected Behavior on Validation Failure:**
- Raise error with specific quality issue
- Log to logs/step06_classification_quality.log
- Quit immediately, invoke g_debug

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt
- data/step01_domain_theta_scores.csv (100 x 4: UID + 3 standardized theta scores)
- data/step02_lpa_fit_comparison.csv (4 x 6: fit indices for K=1,2,3,4)
- data/step02_lpa_convergence_diagnostics.txt
- data/step02_lpa_fitted_models.rds
- data/step03_optimal_profiles.csv (100 x 4: profile assignments)
- data/step03_model_selection_summary.txt
- data/step04_profile_characteristics.csv (K x 12: domain means/CIs by profile)
- data/step04_profile_interpretation.txt
- data/step05_external_validation.csv (4 x 8: ANOVA results for validators)
- data/step05_external_validation_posthoc.csv (pairwise comparisons)
- data/step06_classification_quality.csv
- data/step06_model_diagnostics.txt
- data/lpa_plot_data.csv (plot source data for rq_plots)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_prepare_theta_scores.log
- logs/step02_fit_lpa_models.log
- logs/step03_select_optimal_profiles.log
- logs/step04_characterize_profiles.log
- logs/step05_external_validation.log
- logs/step06_classification_quality.log

### Plots (EMPTY until rq_plots runs)
Note: lpa_plot_data.csv created in data/ for profile visualization by domain

### Results (EMPTY until rq_results runs)
Note: summary.md will be created by rq_results summarizing optimal profiles and validation

---

## Expected Data Formats

### Step-to-Step Transformations
1. Step 0 → Step 1: Dependency validation enables data extraction
2. Step 1 → Step 2: Standardized domain scores become LPA indicators 
3. Step 2 → Step 3: Fit indices enable model selection and membership assignment
4. Step 3 → Step 4: Profile assignments enable domain pattern characterization
5. Step 4 → Step 5: Profiles enable external validation testing
6. Step 5 → Step 6: Complete solution enables quality assessment

### Column Naming Conventions
- **UIDs:** UID (consistent across all files)
- **Domain scores:** theta_What, theta_Where, theta_When (standardized)
- **Profile assignments:** Profile (1, 2, 3...), Max_Posterior_Prob, Profile_Label
- **Statistics:** F_stat, p_uncorrected, p_bonferroni, p_fdr, eta_squared
- **Quality metrics:** Entropy, Mean_Posterior_Prob, Min_Posterior_Prob

### Data Type Constraints
- **UIDs:** object (string identifiers)
- **Theta scores:** float64, nullable=False, range [-4, 4]
- **Profile assignments:** int64, range [1, K]
- **Probabilities:** float64, range [0, 1]
- **Statistics:** float64, nullable=False

---

## Cross-RQ Dependencies

**Source RQs:** Ch5 5.2.1, 5.2.2, 5.2.3 (domain-specific IRT analyses)

**Required Files:**
- results/ch5/5.2.1/data/step03_theta_scores.csv (What domain theta scores)
- results/ch5/5.2.2/data/step03_theta_scores.csv (Where domain theta scores)  
- results/ch5/5.2.3/data/step03_theta_scores.csv (When domain theta scores)
- data/cache/master.xlsx (cognitive test scores for external validation)

**File Format Expectations:**
- Domain theta files: UID column + domain-specific theta statistics
- master.xlsx: UID, Age, RAVLT_T, BVMT_T, RPM_T columns
- All files should contain exactly 100 participants

**Fallback Strategies:**
- Primary paths checked first, then wildcard patterns (*theta*.csv)
- Multiple format possibilities (CSV vs Excel)
- Graceful failure with specific error messages if dependencies missing

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
- **Purpose:** Verify Ch5 domain outputs and master.xlsx exist
- **Criteria:** All 4 required files found and accessible
- **Failure Action:** Quit with specific missing file error

#### Step 1: Extract Domain Scores  
- **Purpose:** Verify standardized domain scores extracted correctly
- **Criteria:** 100 participants, 3 domains, standardized (mean~0, sd~1)
- **Failure Action:** Debug data extraction and standardization

#### Step 2: Fit LPA Models
- **Purpose:** Verify all K models fitted with convergence
- **Criteria:** 4 models fitted, all converged, fit indices computed
- **Failure Action:** Debug LPA implementation and convergence

#### Step 3: Select Optimal Solution
- **Purpose:** Verify model selection succeeded with adequate profile sizes
- **Criteria:** Optimal K selected, all profiles n>=20, entropy>0.80
- **Failure Action:** Debug model selection criteria

#### Step 4: Characterize Profiles
- **Purpose:** Verify profile domain patterns computed with bootstrap CIs
- **Criteria:** Distinct profiles identified, bootstrap CIs computed successfully
- **Failure Action:** Debug profile characterization and bootstrap

#### Step 5: External Validation
- **Purpose:** Verify profile differences on external validators
- **Criteria:** ANOVA tests completed, dual p-values reported (D068)
- **Failure Action:** Debug external validation and corrections

#### Step 6: Classification Quality
- **Purpose:** Verify final model quality meets standards
- **Criteria:** Entropy>0.80, bootstrap stability confirmed
- **Failure Action:** Debug quality assessment and stability

---

## Summary

**Total Steps:** 7 (1 validation + 6 analysis)
**Estimated Runtime:** ~45 minutes
**Cross-RQ Dependencies:** Ch5 5.2.1, 5.2.2, 5.2.3 domain analyses
**Primary Outputs:** Optimal LPA profiles with external validation
**Validation Coverage:** 100% (all 7 steps have 4-layer validation requirements)

**Key Hypothesis:** 
Expect 2-4 distinct episodic memory profiles representing different patterns of What/Where/When domain performance, with external validation on cognitive tests confirming profile distinctions.

**Critical Methodological Notes:**
- LPA approach assumes categorical latent structure (vs continuous individual differences)
- Sample size N=100 may be marginal for 4-profile stability (minimum n=20 per profile)
- Bootstrap stability assessment will validate profile reliability
- External validation with cognitive tests provides convergent validity evidence
- Decision D068 compliance ensures appropriate multiple comparison handling

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml (NOTE: LPA tools need implementation)
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent with v5.1 enhanced statistical specifications