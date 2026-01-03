# Analysis Plan: RQ 7.1.2 - Intercept vs Slope Prediction

**Research Question:** 7.1.2
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines differential prediction of LMM random effects (intercept and slope) using cognitive tests. The key hypothesis is that traditional neuropsychological tests should predict baseline ability (Day 0 intercept) more strongly than forgetting rate (slope), since tests measure encoding but not consolidation processes.

**Pipeline:** Mixed-effects modeling with simultaneous predictor testing (primary) and two-stage random effects extraction (secondary comparison)
**Steps:** 7 total analysis steps (Step 0: validation + Steps 1-6: analysis)
**Estimated Runtime:** ~45 minutes

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Simultaneous modeling PRIMARY to avoid BLUP bias
- Participant-level block bootstrap for correlation preservation
- Bonferroni correction within-RQ (6 tests: 3 predictors x 2 models)

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 outputs exist before proceeding with analysis

**Input:**
- Primary: results/ch5/5.1.1/data/step06_best_model.pkl
- Alternative: results/ch5/5.1.1/data/*lmm*.pkl
- Fallback pattern: results/ch5/5.1.1/data/step*_model*.{pkl,rds,csv}
- Expected content: Fitted LMM with random intercepts and slopes
- Status check: results/ch5/5.1.1/status.yaml (rq_results: success)
- Master data: master.xlsx (cognitive test scores)

**Processing:**
- Check Ch5 5.1.1 completion status
- Locate LMM model file using multiple patterns
- Verify model contains random effects for intercepts and slopes
- Verify master.xlsx accessibility and cognitive test columns
- Log all validation checks with specific file paths found
- If Ch5 incomplete: QUIT with "Ch5 5.1.1 not complete - required for DERIVED data"
- If master.xlsx missing: QUIT with "master.xlsx not accessible for cognitive tests"

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Expected content: "Ch5 5.1.1: FOUND", "LMM model: FOUND", "master.xlsx: FOUND"

*Value Ranges:*
- No numeric values in this step

*Data Quality:*
- All 3 required dependencies confirmed found
- File paths logged for downstream steps
- Status confirmations present

*Log Validation:*
- Required patterns: "Ch5 5.1.1: FOUND", "LMM model: FOUND", "master.xlsx: FOUND"
- Required patterns: "VALIDATION - PASS"
- Forbidden patterns: "QUIT", "NOT FOUND", "ERROR"

**Expected Behavior on Validation Failure:**
- Raise error with specific missing dependency
- Log to logs/step00_validate_dependencies.log
- Quit immediately, invoke g_debug

### Step 1: Extract Episodic Memory Data for LMM
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Medium (~8 minutes)

**Purpose:** Extract 400 observations (100 participants x 4 tests) for simultaneous modeling approach

**Input:**
- master.xlsx: episodic memory theta scores from IRT calibration
- Tag patterns: 'ch5_episodic_theta_*' (all domains combined into omnibus factor)
- Expected format: UID column + theta values + test identifiers

**Processing:**
- Extract theta scores using tag pattern matching
- Create long format: UID, Test (T1/T2/T3/T4), log_Days (0, 0.693, 1.386, 1.792), theta
- Verify 100 participants x 4 tests = 400 total observations
- Check theta range: [-3, 3] (IRT ability scale bounds)
- Create log_Days variable: log(1), log(2), log(4), log(6) for T1, T2, T3, T4
- Handle missing data: Document missingness pattern, exclude if >5% missing per participant
- Standardize participant IDs for merging

**Output:**
- data/step01_episodic_memory_data.csv

**Validation Requirement:**
Validation tools MUST be used after data extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_episodic_memory_data.csv: 400 rows x 4 columns
- Columns: UID (object), Test (object), log_Days (float64), theta (float64)

*Value Ranges:*
- theta in [-3, 3] (IRT ability scale)
- log_Days in [0, 1.8] (log(1) to log(6))
- Test in ['T1', 'T2', 'T3', 'T4']
- UID: 100 unique participants

*Data Quality:*
- Exactly 400 observations (100 x 4 tests)
- No duplicate UID-Test combinations
- Missing theta < 5% overall
- All UIDs present across 4 tests

*Log Validation:*
- Required patterns: "400 observations extracted", "100 participants confirmed"
- Required patterns: "theta range: [-3, 3]"
- Forbidden patterns: "ERROR", "missing data >5%"

**Expected Behavior on Validation Failure:**
- Raise error with specific data quality issue
- Log to logs/step01_extract_episodic_data.log
- Quit immediately, invoke g_debug

### Step 2: Extract and Standardize Cognitive Tests
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Medium (~7 minutes)

**Purpose:** Extract cognitive test raw scores and convert to T-scores (M=50, SD=10)

**Input:**
- master.xlsx: cognitive test raw scores
- Tests: RAVLT Total (T1-T5 sum), BVMT Total Recognition, RPM total score
- Exclusion: NART (language validity concerns per concept)

**Processing:**
- Extract raw scores for RAVLT, BVMT, RPM by UID
- Calculate T-scores: T = 50 + 10 * (X - M) / SD
- Use sample-based means and SDs (not normative data)
- Verify T-score properties: sample mean ~50, sample SD ~10
- Handle missing data: Document pattern, exclude participants with >1 missing test
- Create standardized predictor names: RAVLT_T, BVMT_T, RPM_T
- Verify 100 participants retained after exclusions

**Output:**
- data/step02_cognitive_tests.csv

**Validation Requirement:**
Validation tools MUST be used after cognitive test processing execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_cognitive_tests.csv: 100 rows x 4 columns
- Columns: UID (object), RAVLT_T (float64), BVMT_T (float64), RPM_T (float64)

*Value Ranges:*
- T-scores approximately in [20, 80] (reasonable range for T-scores)
- Sample means approximately 50 (±2) for each test
- Sample SDs approximately 10 (±2) for each test

*Data Quality:*
- Exactly 100 participants
- No duplicate UIDs
- Missing data <10% per test
- All T-scores finite (no NaN, Inf)

*Log Validation:*
- Required patterns: "T-scores calculated: RAVLT, BVMT, RPM"
- Required patterns: "Sample means ~50, SDs ~10"
- Forbidden patterns: "ERROR", "missing >10%", "NaN values"

**Expected Behavior on Validation Failure:**
- Raise error with specific data quality issue
- Log to logs/step02_cognitive_tests.log
- Quit immediately, invoke g_debug

### Step 3: Simultaneous LMM with Cognitive Predictors (PRIMARY APPROACH)
**Dependencies:** Steps 1-2 (episodic data and cognitive tests)
**Complexity:** High (~15 minutes including bootstrap)

**Purpose:** Fit simultaneous LMM to test differential prediction without BLUP bias

**Input:**
- data/step01_episodic_memory_data.csv (400 observations)
- data/step02_cognitive_tests.csv (100 participants with T-scores)

**Processing:**
- Merge datasets on UID to create analysis file
- Standardize cognitive predictors for interpretation
- Fit LMM: theta ~ log_Days + (1 + log_Days | UID) + RAVLT_T*log_Days + BVMT_T*log_Days + RPM_T*log_Days
- Implementation: Use statsmodels.regression.mixed_linear_model.MixedLM or R lmer
- Random seed: 42 for any optimization randomization
- Extract key results:
  - Main effects (intercept prediction): RAVLT_T, BVMT_T, RPM_T coefficients
  - Interaction effects (slope prediction): RAVLT_T:log_Days, BVMT_T:log_Days, RPM_T:log_Days
- Calculate pseudo-R² for main effects vs interactions
- Bootstrap confidence intervals:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Participant-level block resampling (preserves correlation structure)
  - For each iteration: refit model, extract main/interaction effect sizes
  - CI: Percentile method (2.5th, 97.5th percentiles)
- Multiple comparison correction:
  - Family: Within-RQ (6 effects: 3 main + 3 interactions)
  - Bonferroni: alpha = 0.05/6 = 0.0083 per test
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Check model assumptions:
  - Residual normality: Shapiro-Wilk test on Level-1 residuals
  - Random effects normality: Q-Q plots for random intercepts/slopes
  - Homoscedasticity: Plot residuals vs fitted
- Remedial actions if violated:
  - Normality p < 0.05: Report bootstrap CIs as primary inference
  - Heteroscedasticity detected: Consider variance modeling (unequal variances by time)
  - Convergence issues: Try different optimizers, report sensitivity

**Output:**
- data/step03_simultaneous_lmm_results.csv
- data/step03_model_diagnostics.txt

**Validation Requirement:**
Validation tools MUST be used after simultaneous LMM execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_simultaneous_lmm_results.csv: 6 rows x 8 columns
- Columns: effect, estimate, se, ci_lower, ci_upper, p_uncorrected, p_bonferroni, effect_type
- data/step03_model_diagnostics.txt: text file with assumption checks

*Value Ranges:*
- Estimates in [-2, 2] (standardized predictors)
- Standard errors > 0
- p-values in [0, 1]
- CI bounds: ci_lower < estimate < ci_upper

*Data Quality:*
- All 6 effects present (3 main + 3 interactions)
- No NaN values in estimates or CIs
- Bootstrap CIs valid (lower < upper)
- Dual p-values present (Decision D068)

*Log Validation:*
- Required patterns: "LMM converged successfully"
- Required patterns: "Bootstrap complete: 1000 iterations"
- Required patterns: "Assumption checks complete"
- Forbidden patterns: "ERROR", "convergence failed", "singular fit"

**Expected Behavior on Validation Failure:**
- Raise error with specific model fitting issue
- Log to logs/step03_simultaneous_lmm.log
- Quit immediately, invoke g_debug

### Step 4: Extract Random Effects for Two-Stage Comparison (SECONDARY APPROACH)
**Dependencies:** Step 3 (simultaneous LMM baseline model)
**Complexity:** Medium (~8 minutes)

**Purpose:** Extract BLUPs for comparison with simultaneous approach (acknowledge shrinkage bias)

**Input:**
- data/step01_episodic_memory_data.csv
- Need to fit baseline LMM: theta ~ log_Days + (1 + log_Days | UID)

**Processing:**
- Fit baseline LMM without cognitive predictors: theta ~ log_Days + (1 + log_Days | UID)
- Implementation: Same package as Step 3 for consistency
- Extract Best Linear Unbiased Predictors (BLUPs) for random effects
- Calculate shrinkage factors: BLUP_variance / empirical_variance
- Document bias: BLUPs pull extreme values toward population mean
- Extract per-participant intercepts and slopes
- Check BLUP properties:
  - Intercepts: Mean ~0 (centered), range depends on shrinkage
  - Slopes: Mean ~population slope, variance reduced by shrinkage
- Verify 100 participants have both intercept and slope BLUPs
- Calculate empirical Bayes shrinkage quantification

**Output:**
- data/step04_random_effects_blups.csv
- data/step04_shrinkage_analysis.txt

**Validation Requirement:**
Validation tools MUST be used after BLUP extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_random_effects_blups.csv: 100 rows x 3 columns
- Columns: UID (object), intercept (float64), slope (float64)
- data/step04_shrinkage_analysis.txt: text file with shrinkage statistics

*Value Ranges:*
- Intercept in [-1, 1] (typical range after shrinkage)
- Slope in [-0.5, 0.5] (typical range for log-days)
- Shrinkage factors in [0, 1] (0=no shrinkage, 1=complete shrinkage)

*Data Quality:*
- Exactly 100 participants
- No missing intercepts or slopes
- No duplicate UIDs
- Shrinkage factors computed and reasonable

*Log Validation:*
- Required patterns: "BLUPs extracted: 100 participants"
- Required patterns: "Shrinkage analysis complete"
- Forbidden patterns: "ERROR", "missing BLUPs", "convergence failed"

**Expected Behavior on Validation Failure:**
- Raise error with specific BLUP extraction issue
- Log to logs/step04_extract_blups.log
- Quit immediately, invoke g_debug

### Step 5: Two-Stage Regression on BLUPs (Sensitivity Analysis)
**Dependencies:** Steps 2, 4 (cognitive tests and BLUPs)
**Complexity:** Medium (~10 minutes including bootstrap)

**Purpose:** Predict intercepts and slopes separately for comparison with simultaneous approach

**Input:**
- data/step04_random_effects_blups.csv (intercepts and slopes)
- data/step02_cognitive_tests.csv (T-scored predictors)

**Processing:**
- Merge datasets on UID
- Model 1 - Predict intercepts: Intercept ~ RAVLT_T + BVMT_T + RPM_T
- Model 2 - Predict slopes: Slope ~ RAVLT_T + BVMT_T + RPM_T
- Implementation: statsmodels.api.OLS with standardized predictors
- Extract R², adjusted R², F-statistics for both models
- Bootstrap 95% CIs for R² values and coefficients:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Participant-level resampling WITH replacement
  - For each iteration: fit both models, extract R² and coefficients
  - CI: Percentile method (2.5th, 97.5th percentiles)
- Multiple comparison correction:
  - Family: Within-step (6 tests: 3 predictors x 2 models)
  - Bonferroni: alpha = 0.05/6 = 0.0083
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Check assumptions for both models:
  - Normality: Shapiro-Wilk test on residuals
  - Homoscedasticity: Breusch-Pagan test
  - Multicollinearity: VIF for each predictor
- Remedial actions if violated:
  - Normality p < 0.05: Report bootstrap CIs as primary
  - Heteroscedasticity p < 0.05: Add HC3 robust SEs
  - VIF > 5: Document, consider ridge if VIF > 10
- CRITICAL CAVEAT: Acknowledge BLUP bias affects these results

**Output:**
- data/step05_intercept_regression.csv
- data/step05_slope_regression.csv
- data/step05_two_stage_diagnostics.txt

**Validation Requirement:**
Validation tools MUST be used after two-stage regression execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_intercept_regression.csv: 4 rows x 8 columns (R² + 3 predictors)
- data/step05_slope_regression.csv: 4 rows x 8 columns (R² + 3 predictors)
- Columns: term, estimate, se, ci_lower, ci_upper, p_uncorrected, p_bonferroni, vif
- data/step05_two_stage_diagnostics.txt: assumption check results

*Value Ranges:*
- R² in [0, 1]
- Beta coefficients in [-2, 2] (standardized)
- Standard errors > 0
- VIF in [1, 10] (multicollinearity check)
- p-values in [0, 1]

*Data Quality:*
- Both models converged successfully
- All coefficients finite (no NaN)
- Bootstrap CIs valid (lower < upper)
- Dual p-values present (Decision D068)

*Log Validation:*
- Required patterns: "Both models fitted successfully"
- Required patterns: "Bootstrap complete: 1000 iterations"
- Required patterns: "Assumption checks complete"
- Forbidden patterns: "ERROR", "convergence failed", "VIF > 10"

**Expected Behavior on Validation Failure:**
- Raise error with specific regression issue
- Log to logs/step05_two_stage_regression.log
- Quit immediately, invoke g_debug

### Step 6: Compare R² Values and Test Primary Hypothesis
**Dependencies:** Steps 3, 5 (simultaneous and two-stage results)
**Complexity:** Medium (~7 minutes)

**Purpose:** Test hypothesis that R²_intercept > R²_slope using multiple approaches

**Input:**
- data/step03_simultaneous_lmm_results.csv (main vs interaction effects)
- data/step05_intercept_regression.csv (R² for intercept model)
- data/step05_slope_regression.csv (R² for slope model)

**Processing:**
- Extract R² values from both approaches:
  - Simultaneous: pseudo-R² for main effects vs interactions
  - Two-stage: R² from separate intercept/slope regressions
- Test primary hypothesis: R²_intercept > R²_slope
- Bootstrap difference test:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Participant-level block bootstrap
  - For each iteration: compute R²_intercept - R²_slope difference
  - Test: Does 95% CI exclude 0?
- Effect size interpretation:
  - Large effect: R² > 0.25
  - Medium effect: R² = 0.09-0.25
  - Small effect: R² = 0.01-0.09
- Power analysis (post-hoc):
  - Given: N=100, 3 predictors, alpha=0.0083 (Bonferroni corrected)
  - Calculate: minimum detectable f² at 80% power
  - Use: statsmodels.stats.power.FTestAnovaPower()
  - Report: actual power for observed effect sizes
- Document bias considerations:
  - Simultaneous approach: Unbiased estimates
  - Two-stage approach: BLUP shrinkage may affect results
- Create summary comparison table

**Output:**
- data/step06_r_squared_comparison.csv
- data/step06_hypothesis_test_results.txt

**Validation Requirement:**
Validation tools MUST be used after hypothesis testing execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_r_squared_comparison.csv: 4 rows x 6 columns
- Columns: approach, outcome_type, r_squared, ci_lower, ci_upper, interpretation
- data/step06_hypothesis_test_results.txt: statistical test results

*Value Ranges:*
- R² values in [0, 1]
- CI bounds valid: ci_lower < r_squared < ci_upper
- Power values in [0, 1]
- Effect sizes: small/medium/large categories

*Data Quality:*
- Both approaches represented
- Bootstrap CIs computed successfully
- Hypothesis test conclusion present
- Power analysis complete

*Log Validation:*
- Required patterns: "R² comparison complete"
- Required patterns: "Bootstrap hypothesis test: 1000 iterations"
- Required patterns: "Power analysis complete"
- Forbidden patterns: "ERROR", "invalid CI", "power calculation failed"

**Expected Behavior on Validation Failure:**
- Raise error with specific comparison issue
- Log to logs/step06_compare_r_squared.log
- Quit immediately, invoke g_debug

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt: Dependency check results
- data/step01_episodic_memory_data.csv: 400 observations (100 x 4 tests)
- data/step02_cognitive_tests.csv: T-scored predictors (100 participants)
- data/step03_simultaneous_lmm_results.csv: Main/interaction effects (6 effects)
- data/step03_model_diagnostics.txt: LMM assumption checks
- data/step04_random_effects_blups.csv: Extracted BLUPs (100 participants)
- data/step04_shrinkage_analysis.txt: BLUP bias documentation
- data/step05_intercept_regression.csv: Intercept prediction results
- data/step05_slope_regression.csv: Slope prediction results
- data/step05_two_stage_diagnostics.txt: OLS assumption checks
- data/step06_r_squared_comparison.csv: R² comparison across approaches
- data/step06_hypothesis_test_results.txt: Primary hypothesis test
- data/step06_intercept_slope_plot_data.csv: Plot source CSV

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_episodic_data.log
- logs/step02_cognitive_tests.log
- logs/step03_simultaneous_lmm.log
- logs/step04_extract_blups.log
- logs/step05_two_stage_regression.log
- logs/step06_compare_r_squared.log

### Plots (EMPTY until rq_plots runs)
Note: step06_intercept_slope_plot_data.csv created in data/ for downstream plotting

### Results (EMPTY until rq_results runs)
Note: summary.md will be created by rq_results

---

## Expected Data Formats

### Step-to-Step Transformations
1. **master.xlsx** -> **step01**: Wide to long format (100 -> 400 observations)
2. **master.xlsx** -> **step02**: Raw scores to T-scores (M=50, SD=10)
3. **step01 + step02** -> **step03**: Merged data for simultaneous LMM
4. **step01** -> **step04**: Baseline LMM -> BLUPs (shrinkage applied)
5. **step04 + step02** -> **step05**: BLUPs -> separate regressions
6. **step03 + step05** -> **step06**: R² extraction and comparison

### Column Naming Conventions
- **UIDs:** Consistent participant identifiers across all files
- **Tests:** T1, T2, T3, T4 (episodic memory tests)
- **Predictors:** RAVLT_T, BVMT_T, RPM_T (T-scored cognitive tests)
- **Effects:** main_effect, interaction_effect (simultaneous approach)
- **Models:** intercept_model, slope_model (two-stage approach)

### Data Type Constraints
- **UID:** object (string identifier, not nullable)
- **theta:** float64 (range: [-3, 3], nullable <5%)
- **T-scores:** float64 (approximate range: [20, 80], not nullable)
- **R²:** float64 (range: [0, 1], not nullable)
- **p-values:** float64 (range: [0, 1], not nullable)

---

## Cross-RQ Dependencies

### Required from Ch5 5.1.1:
- **Status:** rq_results must show success
- **Model file:** LMM with random intercepts and slopes
- **Data structure:** 100 participants x 4 tests = 400 observations
- **Format:** Fitted model object (PKL or RDS) or processed random effects

### Required from master.xlsx:
- **Cognitive tests:** RAVLT, BVMT, RPM raw scores
- **Episodic memory:** IRT-calibrated theta scores (omnibus factor)
- **Participant IDs:** Consistent with Ch5 data

### Fallback Strategy:
If Ch5 outputs unavailable, this RQ cannot proceed (DERIVED data dependency).

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
**Substance validation criteria included above in step specification**

#### Step 1: Extract Episodic Memory Data
**Substance validation criteria included above in step specification**

#### Step 2: Extract and Standardize Cognitive Tests
**Substance validation criteria included above in step specification**

#### Step 3: Simultaneous LMM with Cognitive Predictors
**Substance validation criteria included above in step specification**

#### Step 4: Extract Random Effects for Two-Stage Comparison
**Substance validation criteria included above in step specification**

#### Step 5: Two-Stage Regression on BLUPs
**Substance validation criteria included above in step specification**

#### Step 6: Compare R² Values and Test Primary Hypothesis
**Substance validation criteria included above in step specification**

---

## Summary

**Total Steps:** 7 (Step 0: validation + Steps 1-6: analysis)
**Estimated Runtime:** ~45 minutes
**Cross-RQ Dependencies:** Ch5 5.1.1 (LMM results) + master.xlsx (cognitive tests)
**Primary Outputs:** 13 data files + 1 plot source CSV
**Validation Coverage:** 100% (all 7 steps have 4-layer validation requirements)

**Key Hypothesis:** Cognitive tests predict intercept (R² > 0.30) more than slope (R² < 0.10)

**Critical Methodological Notes:**
1. **BLUP bias acknowledged:** Two-stage approach for comparison only, simultaneous primary
2. **Multiple comparisons:** Bonferroni correction (alpha = 0.05/6 = 0.0083)
3. **Dual reporting:** Both uncorrected AND corrected p-values (Decision D068)
4. **Bootstrap validity:** Participant-level block resampling preserves correlation
5. **Power analysis:** Post-hoc power reported for observed effects
6. **Random seeds:** seed=42 throughout for reproducibility

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent with v5.1 enhancements