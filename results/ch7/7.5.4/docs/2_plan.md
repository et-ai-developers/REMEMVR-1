# Analysis Plan: RQ 7.5.4 - Per-Test Sleep Effects on Same-Test Performance

**Research Question:** 7.5.4
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

**Research Question:** Does sleep quality BEFORE each test predict THAT test's performance, demonstrating within-person state-dependent sleep effects?

**Analysis Approach:** Multilevel modeling of within-person sleep variability across four test sessions, decomposing state-dependent (acute) sleep effects from trait-dependent (chronic) individual differences.

**Pipeline:** Linear Mixed-Effects Model (LMM) with participant-level bootstrap and hierarchical cross-validation
**Steps:** 8 total analysis steps (Step 0: dependency validation + Steps 1-7: analysis)
**Estimated Runtime:** ~45 minutes total

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Ch7 Bonferroni: alpha = 0.05/28 = 0.00179 for chapter-level correction
- Bootstrap/CV seed: 42 for reproducibility

**Data Structure:**
- 400 observations (100 participants x 4 tests)
- DERIVED data from Ch5 5.1.1 theta scores + master.xlsx sleep tags
- Within-person design enables state-dependent effect isolation

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 outputs and master.xlsx exist before proceeding with sleep-memory analysis

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/*theta*.csv
- Fallback: results/ch5/5.1.1/data/*step03*.csv
- Master data: data/cache/master.xlsx
- Expected: 100 participants x 4 tests theta scores, SLP tag data

**Processing:**
- Check Ch5 5.1.1 status: results/ch5/5.1.1/status.yaml (rq_results = success)
- Locate theta score file using fallback patterns
- Verify file contains columns: UID, Test, theta_all
- Verify master.xlsx accessible and contains SLP tags
- Log all validation checks with specific patterns found

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file, 10-20 lines
- Content: validation status for each checked dependency

*Value Ranges:*
- N/A (text validation file)

*Data Quality:*
- All required dependencies found and validated
- Ch5 5.1.1 status confirmed as success
- Master.xlsx accessible with SLP tags present

*Log Validation:*
- Required patterns: "Ch5 5.1.1 status: success", "Theta scores found:", "Master.xlsx accessible", "SLP tags detected"
- Forbidden patterns: "ERROR", "not found", "missing", "FAIL"

**Expected Behavior on Validation Failure:**
QUIT immediately with specific error message identifying missing dependency

---

### Step 1: Extract Per-Test Sleep Data
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Medium (~5 minutes)

**Purpose:** Extract sleep hours and quality data per test session from master.xlsx using SLP tag patterns

**Input:**
- data/cache/master.xlsx (validated in Step 0)
- Tag patterns: {UID}-RVR-T{N}-SLP-X-HOUR- and {UID}-RVR-T{N}-SLP-X-QUAL-

**Processing:**
- Parse master.xlsx for sleep tags across all UIDs and tests (T1, T2, T3, T4)
- Extract sleep hours (continuous) and sleep quality (Likert scale)
- Create long-format dataset: UID, Test, Sleep_Hours, Sleep_Quality
- Handle missing values: flag if participant missing >1 test worth of sleep data
- Exclude sleep values >3 SD from person mean (likely data entry errors)
- Compute within-person sleep variability (SD within each UID)

**Output:**
- data/step01_sleep_per_test.csv

**Validation Requirement:**
Validation tools MUST be used after sleep data extraction.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_sleep_per_test.csv: 400 rows x 4 columns
- Columns: UID (object), Test (int), Sleep_Hours (float64), Sleep_Quality (float64)

*Value Ranges:*
- Sleep_Hours in [3, 12] (biologically plausible range)
- Sleep_Quality in [1, 7] (Likert scale)
- Test in [1, 2, 3, 4] (four test sessions)

*Data Quality:*
- All 100 UIDs represented
- Complete cases: >=75% (minimum 300/400 observations)
- Within-person variability: Sleep_Hours SD > 0.5 for majority of participants
- No duplicate UID-Test combinations

*Log Validation:*
- Required patterns: "Sleep extraction complete", "400 observations expected", "Missing data: X%"
- Forbidden patterns: "ERROR", "parsing failed", "no SLP tags found"

**Expected Behavior on Validation Failure:**
Log error with specific issue, proceed if >75% complete data, QUIT if <75%

---

### Step 2: Merge Sleep Data with Theta Scores
**Dependencies:** Step 1 (sleep data extraction)
**Complexity:** Low (~3 minutes)

**Purpose:** Create unified dataset merging per-test sleep variables with corresponding theta scores

**Input:**
- data/step01_sleep_per_test.csv (sleep data by test)
- results/ch5/5.1.1/data/step03_theta_scores.csv (theta scores by test)

**Processing:**
- Merge datasets on UID and Test
- Create 400-row longitudinal dataset
- Verify merge completeness (expect minimal data loss)
- Add test session variable (T1, T2, T3, T4) for practice effect control
- Compute person-mean sleep variables for between-person effect decomposition
- Center sleep variables within-person: Hours_centered = Hours - person_mean_Hours

**Output:**
- data/step02_theta_sleep_merged.csv

**Validation Requirement:**
Validation tools MUST be used after data merging.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_theta_sleep_merged.csv: 350-400 rows x 8 columns
- Columns: UID, Test, theta_all, Sleep_Hours, Sleep_Quality, Hours_mean, Quality_mean, Test_Session

*Value Ranges:*
- theta_all in [-3, 3] (IRT ability scale)
- Sleep_Hours in [3, 12] (unchanged from Step 1)
- Hours_mean in [5, 10] (person-level average)
- Test_Session in [1, 2, 3, 4]

*Data Quality:*
- Successful merge rate >90% (minimal loss from Ch5 data)
- All variables non-missing for merged cases
- Within-person centering: mean(Hours_centered) ≈ 0 within each UID

*Log Validation:*
- Required patterns: "Merge complete", "N merged observations:", "Person-mean centering applied"
- Forbidden patterns: "ERROR", "merge failed", "key columns missing"

**Expected Behavior on Validation Failure:**
Log specific merge issue, attempt alternative column names, QUIT if <300 observations

---

### Step 3: Descriptive Analysis and Data Quality Assessment
**Dependencies:** Step 2 (merged dataset)
**Complexity:** Medium (~5 minutes)

**Purpose:** Examine within-person sleep variability and data quality before multilevel modeling

**Input:**
- data/step02_theta_sleep_merged.csv

**Processing:**
- Compute descriptive statistics by person and overall
- Assess within-person sleep variability (require SD > 0.5 for meaningful analysis)
- Check for outliers using Cook's distance threshold (>4/n)
- Examine sleep-memory correlations at within and between-person levels
- Create correlation matrix decomposing within vs between-person effects
- Document participants with insufficient sleep variability for exclusion consideration

**Output:**
- data/step03_descriptive_stats.csv
- data/step03_correlation_matrix.csv
- data/step03_outlier_flagging.csv

**Validation Requirement:**
Validation tools MUST be used after descriptive analysis.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_descriptive_stats.csv: 100+ rows x 6 columns (person-level stats)
- data/step03_correlation_matrix.csv: 4 x 4 correlation matrix
- data/step03_outlier_flagging.csv: flagged cases with Cook's D > threshold

*Value Ranges:*
- Correlations in [-1, 1] (valid correlation bounds)
- Sleep variability SDs in [0.1, 3.0] (reasonable within-person variation)
- Outlier flags: binary 0/1

*Data Quality:*
- >=80% of participants with meaningful sleep variability (SD > 0.5)
- Outlier rate <10% (Cook's D flagging)
- Within-person correlations present and non-zero

*Log Validation:*
- Required patterns: "Descriptive analysis complete", "Within-person variability adequate", "Outliers detected: N"
- Forbidden patterns: "ERROR", "insufficient variability", "correlation failed"

**Expected Behavior on Validation Failure:**
Log specific data quality issues, proceed with available data, note limitations

---

### Step 4: Fit Multilevel Models for Sleep Effects
**Dependencies:** Step 3 (descriptive analysis)
**Complexity:** High (~10 minutes)

**Purpose:** Fit linear mixed-effects models to decompose within-person vs between-person sleep effects

**Input:**
- data/step02_theta_sleep_merged.csv (primary analysis dataset)
- data/step03_outlier_flagging.csv (for sensitivity analysis)

**Processing:**
- Model 1: `theta_all ~ Sleep_Hours_centered + Sleep_Quality_centered + Test_Session + (1|UID)`
- Model 2: Add between-person effects: `+ Hours_mean + Quality_mean`
- Implementation: statsmodels mixed linear model with REML estimation
- Random seed: 42 for any stochastic components
- Extract fixed effects: coefficients, SEs, t-statistics, p-values
- Extract random effects: participant-level intercepts, ICC
- Compute effect sizes: standardized betas, R² marginal and conditional
- Practice effect control: Test_Session as covariate per scholar/stats feedback

**Output:**
- data/step04_lmm_model1_summary.csv (within-person model)
- data/step04_lmm_model2_summary.csv (full decomposition model)
- data/step04_random_effects.csv (participant-level intercepts)

**Validation Requirement:**
Validation tools MUST be used after LMM fitting.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_lmm_model1_summary.csv: 4 rows x 6 columns (fixed effects table)
- data/step04_lmm_model2_summary.csv: 6 rows x 6 columns (full model)
- data/step04_random_effects.csv: 100 rows x 3 columns (UID, intercept, prediction)

*Value Ranges:*
- Coefficients in [-1, 1] (standardized predictors)
- p-values in [0, 1] (valid probabilities)
- R² in [0, 1] (variance explained)
- Random intercepts in [-2, 2] (centered around 0)

*Data Quality:*
- Model convergence successful (no convergence warnings)
- All coefficients finite (no NaN values)
- Standard errors positive and reasonable
- ICC between 0.1-0.8 (meaningful clustering)

*Log Validation:*
- Required patterns: "Model 1 converged successfully", "Model 2 fitted", "Random effects extracted"
- Forbidden patterns: "ERROR", "convergence failed", "singular fit"

**Expected Behavior on Validation Failure:**
Log convergence issues, try alternative optimization, QUIT if persistent convergence failure

---

### Step 5: Model Diagnostics and Assumption Checking
**Dependencies:** Step 4 (LMM models fitted)
**Complexity:** Medium (~8 minutes)

**Purpose:** Comprehensive validation of LMM assumptions with remedial actions if violated

**Input:**
- data/step04_lmm_model1_summary.csv (fitted models)
- Model objects from Step 4 (residuals, fitted values)

**Processing:**
- Check residual normality: Shapiro-Wilk test + Q-Q plots
- Test homoscedasticity: Breusch-Pagan test + residual vs fitted plots
- Examine random effects normality: Q-Q plots for random intercepts
- Test multicollinearity: VIF for sleep predictors
- Detect influential observations: Cook's distance for mixed models
- Remedial actions if violated:
  - Normality p < 0.05: Use bootstrap CIs (1000 iterations, seed=42)
  - Heteroscedasticity p < 0.05: Report HC3 robust SEs
  - VIF > 5: Document multicollinearity, consider ridge if VIF > 10
  - Outliers (Cook's D > 4/n): Report with/without outliers

**Output:**
- data/step05_assumption_tests.csv (diagnostic test results)
- data/step05_model_diagnostics.txt (summary + remedial actions)

**Validation Requirement:**
Validation tools MUST be used after model diagnostics.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_assumption_tests.csv: 5-8 rows x 3 columns (test, statistic, p_value)
- data/step05_model_diagnostics.txt: text summary, 20-40 lines

*Value Ranges:*
- Test statistics: context-dependent but finite
- p-values in [0, 1]
- VIF values in [1, 15] (higher values indicate multicollinearity)

*Data Quality:*
- All diagnostic tests completed successfully
- Remedial actions documented if assumptions violated
- Clear pass/fail determination for each assumption

*Log Validation:*
- Required patterns: "Assumption checking complete", "Normality test:", "Heteroscedasticity test:"
- Forbidden patterns: "ERROR", "diagnostic failed", "cannot compute"

**Expected Behavior on Validation Failure:**
Log specific diagnostic failure, attempt alternative tests, proceed with documented limitations

---

### Step 6: Effect Decomposition and Multiple Comparison Correction
**Dependencies:** Step 5 (diagnostics complete)
**Complexity:** Medium (~7 minutes)

**Purpose:** Decompose within vs between-person sleep effects with appropriate multiple comparison corrections

**Input:**
- data/step04_lmm_model2_summary.csv (full decomposition model)
- data/step05_assumption_tests.csv (for correction guidance)

**Processing:**
- Extract within-person effects: Sleep_Hours_centered, Sleep_Quality_centered coefficients
- Extract between-person effects: Hours_mean, Quality_mean coefficients
- Compare effect sizes: within vs between-person sleep effects
- Multiple comparison correction:
  - Family: Within-RQ (4 main effects: 2 within + 2 between-person)
  - Bonferroni: alpha = 0.05/4 = 0.0125 per test
  - Also compute FDR using Benjamini-Hochberg procedure
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Compute standardized effect sizes: Cohen's f² for model comparison
- Format results: p_uncorrected, p_bonferroni, p_fdr for each effect

**Output:**
- data/step06_effect_decomposition.csv
- data/step06_multiple_comparisons.csv

**Validation Requirement:**
Validation tools MUST be used after effect decomposition.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_effect_decomposition.csv: 4 rows x 8 columns (effect, estimate, se, ci_lower, ci_upper, p_uncorrected, p_bonferroni, p_fdr)
- data/step06_multiple_comparisons.csv: 4 rows x 5 columns (correction summary)

*Value Ranges:*
- Estimates in [-1, 1] (standardized effects)
- Standard errors > 0 (positive values)
- p-values in [0, 1] for all correction methods
- Confidence intervals: ci_lower < estimate < ci_upper

*Data Quality:*
- All 4 main effects represented
- Bonferroni corrections properly applied
- FDR adjustments computed
- Dual p-value reporting per Decision D068

*Log Validation:*
- Required patterns: "Effect decomposition complete", "Multiple corrections applied", "Within/between effects computed"
- Forbidden patterns: "ERROR", "correction failed", "invalid p-values"

**Expected Behavior on Validation Failure:**
Log specific correction issue, use uncorrected values, note limitation in results

---

### Step 7: Cross-Validation and Bootstrap Confidence Intervals
**Dependencies:** Step 6 (effect decomposition)
**Complexity:** High (~12 minutes including bootstrap)

**Purpose:** Assess model generalizability and provide robust confidence intervals for sleep effects

**Input:**
- data/step02_theta_sleep_merged.csv (for resampling)
- Model specifications from Steps 4-6

**Processing:**
- Participant-level 5-fold cross-validation:
  - Implementation: sklearn.model_selection.GroupKFold with groups=UID
  - Random seed: 42 for reproducibility
  - For each fold: fit LMM on training participants, evaluate on test participants
  - Compute R² marginal and conditional for each fold
  - Flag overfitting if train-test gap > 0.10
- Bootstrap confidence intervals for within-person effects:
  - Participant-level bootstrap (preserves within-participant correlation)
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Resample participants WITH replacement, keep all their observations
  - For each iteration: fit Model 1, extract sleep effect coefficients
  - 95% CI: percentile method (2.5th, 97.5th percentiles)
- Document bootstrap CI coverage and width

**Output:**
- data/step07_cross_validation_results.csv
- data/step07_bootstrap_CIs.csv

**Validation Requirement:**
Validation tools MUST be used after cross-validation and bootstrap.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_cross_validation_results.csv: 5 rows x 4 columns (fold, train_R2, test_R2, gap)
- data/step07_bootstrap_CIs.csv: 2 rows x 6 columns (effect, estimate, bootstrap_mean, ci_lower, ci_upper, ci_width)

*Value Ranges:*
- R² values in [0, 1] (proportion of variance)
- Bootstrap means close to original estimates (within 10%)
- CI bounds: ci_lower < estimate < ci_upper
- CI widths > 0 (positive intervals)

*Data Quality:*
- All 5 CV folds completed successfully
- Bootstrap: 1000 iterations completed
- No excessive overfitting (gaps < 0.10)
- Bootstrap CIs cover original estimates

*Log Validation:*
- Required patterns: "Cross-validation complete: 5 folds", "Bootstrap complete: 1000 iterations", "CI coverage validated"
- Forbidden patterns: "ERROR", "CV failed", "bootstrap convergence"

**Expected Behavior on Validation Failure:**
Log specific CV/bootstrap failure, attempt fewer iterations/folds, proceed with available results

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs in data/)
- data/step00_dependency_validation.txt
- data/step01_sleep_per_test.csv
- data/step02_theta_sleep_merged.csv
- data/step03_descriptive_stats.csv
- data/step03_correlation_matrix.csv
- data/step03_outlier_flagging.csv
- data/step04_lmm_model1_summary.csv
- data/step04_lmm_model2_summary.csv
- data/step04_random_effects.csv
- data/step05_assumption_tests.csv
- data/step05_model_diagnostics.txt
- data/step06_effect_decomposition.csv
- data/step06_multiple_comparisons.csv
- data/step07_cross_validation_results.csv
- data/step07_bootstrap_CIs.csv

### Logs (ONLY execution logs in logs/)
- logs/step00_validate_dependencies.log
- logs/step01_extract_sleep_data.log
- logs/step02_merge_data.log
- logs/step03_descriptive_analysis.log
- logs/step04_fit_lmm.log
- logs/step05_model_diagnostics.log
- logs/step06_effect_decomposition.log
- logs/step07_crossval_bootstrap.log

### Plots (EMPTY until rq_plots runs)
- Plot source CSVs will be created in data/ for visualization
- rq_plots will generate final PNG/PDF files in plots/

### Results (EMPTY until rq_results runs)
- rq_results will create summary.md with key findings

---

## Expected Data Formats

### Step-to-Step Transformations
1. **Steps 0-1:** Raw SLP tags -> structured per-test sleep data (wide to long)
2. **Step 2:** Sleep + theta merge -> unified longitudinal dataset (400 rows)
3. **Step 3:** Descriptive summaries -> quality assessment and outlier detection
4. **Step 4:** Longitudinal data -> multilevel models with random effects
5. **Steps 5-7:** Model validation -> robust inference with corrections and CIs

### Column Naming Conventions
- **ID variables:** UID (participant), Test (session 1-4)
- **Sleep variables:** Sleep_Hours, Sleep_Quality, Hours_centered, Hours_mean
- **Memory variable:** theta_all (IRT ability estimate)
- **Effects:** estimate, se, ci_lower, ci_upper, p_uncorrected, p_bonferroni, p_fdr

### Data Type Constraints
- UID: object (string identifiers, non-nullable)
- Test: int64 (1-4, non-nullable)
- Sleep_Hours: float64 (3-12 range, nullable <5%)
- Sleep_Quality: float64 (1-7 range, nullable <5%)
- theta_all: float64 (-3 to +3 range, non-nullable after merge)

---

## Cross-RQ Dependencies

**Source RQ:** Ch5 5.1.1 (Overall theta scores per test)

**Required Files:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/*theta*.csv
- Fallback: results/ch5/5.1.1/data/step03*.csv

**Expected Content:**
- 400 rows (100 UIDs x 4 tests)
- Columns: UID, Test, theta_all
- Data format: IRT ability estimates in [-3, +3] range

**Dependency Verification:**
- Step 0 validates Ch5 5.1.1 completion and file existence
- If missing: QUIT with "Ch5 5.1.1 theta scores not found"
- Alternative file discovery using pattern matching

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Architecture
- **4-layer validation** for each step: Output Files, Value Ranges, Data Quality, Log Validation
- **Substance criteria** embedded for rq_inspect post-execution validation
- **Circuit breakers** for critical failures (dependency missing, convergence failure)
- **Quality thresholds** for data completeness and model validity

### Key Validation Checkpoints
- **Step 0:** Dependency validation prevents pipeline failure
- **Step 2:** Merge validation ensures data integrity
- **Step 4:** Model convergence validation prevents invalid inference
- **Step 5:** Assumption validation triggers remedial actions
- **Step 7:** Bootstrap/CV validation ensures robust uncertainty quantification

---

## Summary

**Total Steps:** 8 (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** ~45 minutes
**Cross-RQ Dependencies:** Ch5 5.1.1 (theta scores)
**Primary Outputs:** Within-person sleep effects with robust statistical inference
**Validation Coverage:** 100% (all 8 steps have 4-layer validation requirements)

**Key Hypothesis:** Poor sleep before a specific test will impair that test's performance (within-person effect), independent of individual differences in overall sleep quality.

**Critical Methodological Notes:**
- Within-person design isolates state-dependent sleep effects from trait differences
- Multilevel modeling appropriately handles hierarchical data structure (400 observations nested in 100 participants)
- Bootstrap and cross-validation provide robust uncertainty quantification
- Multiple comparison corrections address family-wise error rate
- Practice effects controlled via Test_Session covariate per validation feedback
- All randomized procedures use seed=42 for reproducibility

**Statistical Implementation Highlights:**
- Random seed: 42 for all CV, bootstrap, and stochastic procedures
- Bootstrap: 1000 iterations, participant-level resampling, percentile CIs
- Cross-validation: 5-fold GroupKFold respecting participant clustering
- Multiple comparisons: Within-RQ family, Bonferroni + FDR, dual reporting (D068)
- Assumption violations: Specific remedial actions (bootstrap CIs, robust SEs, outlier handling)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml (specify tools from tool_inventory.md)
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable Python code

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner v5.1 agent
  - Enhanced statistical specifications (seeds, bootstrap, CV, corrections)
  - Comprehensive 4-layer validation for all 8 steps
  - Cross-RQ dependency validation with fallback paths
  - Practice effect control per validation feedback
  - Decision D068 dual p-value reporting integrated