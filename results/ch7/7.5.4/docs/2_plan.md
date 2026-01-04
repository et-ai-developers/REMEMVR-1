# Analysis Plan: RQ 7.5.4 - Per-Test Sleep Effects on Same-Test Performance

**Research Question:** 7.5.4
**Created:** 2026-01-03
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines within-person sleep variability across four REMEMVR test sessions using 400 observations (100 participants x 4 tests). Tests state-dependent effects of sleep hours and sleep quality on same-test episodic memory performance using multilevel modeling with comprehensive statistical validation.

**Pipeline:** Linear Mixed-Effects Model (LMM) with hierarchical cross-validation and bootstrap confidence intervals
**Steps:** 8 total analysis steps (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** ~45 minutes

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Bonferroni correction within-RQ (multiple sleep predictors)
- Participant-level bootstrap and cross-validation (hierarchical structure)
- Random seed=42 for all randomized procedures

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 outputs and master.xlsx accessibility before proceeding

**Input:**
- Primary: results/ch5/5.1.1/status.yaml (verify rq_results: success)
- Alternative: results/ch5/5.1.1/data/step03_theta_scores.csv
- Fallback: results/ch5/5.1.1/data/*theta*.{csv,txt}
- Expected: Theta scores per UID per test (400 rows expected)
- Master file: data/cache/master.xlsx (sleep tag access)
- If Ch5 not found: QUIT with "Ch5 5.1.1 theta output not found"

**Processing:**
- Check Ch5 5.1.1 completed successfully (status.yaml)
- Locate theta scores file (try multiple patterns)
- Verify theta file contains 400 rows (100 UIDs x 4 tests)
- Test master.xlsx accessibility and SLP tag patterns
- Log all validation results with timestamps

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Expected patterns: "Ch5 validation: PASS", "Master.xlsx access: PASS"

*Value Ranges:*
- N/A (validation step)

*Data Quality:*
- All dependency checks must pass
- Ch5 theta file must contain 400 rows
- Master.xlsx must be accessible

*Log Validation:*
- Required patterns: "Dependency validation complete", "All checks: PASS"
- Forbidden patterns: "ERROR", "FAIL", "not found"

**Expected Behavior on Validation Failure:**
Raise error with specific dependency issue, log to logs/step00_validate_dependencies.log, quit immediately

### Step 1: Extract Per-Test Sleep Data
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (~5 minutes)

**Purpose:** Extract sleep hours and quality data from dfnonvr.csv for each test session

**Input:**
- data/cache/master.xlsx (SLP tag patterns)
- Tag patterns: {UID}-RVR-T{N}-SLP-X-HOUR- and {UID}-RVR-T{N}-SLP-X-QUAL-
- Expected: 4 sleep entries per UID (T1, T2, T3, T4)

**Processing:**
- Extract sleep hours using pattern: {UID}-RVR-T{N}-SLP-X-HOUR-
- Extract sleep quality using pattern: {UID}-RVR-T{N}-SLP-X-QUAL-
- Create long-format dataset: columns UID, Test, Sleep_Hours, Sleep_Quality
- Handle missing data: exclude tests with missing sleep data
- Data validation: sleep hours in [0, 24], quality in [1, 10]
- Remove outliers: >3 SD from person-specific mean
- Calculate completeness: require >=3 tests per UID for inclusion

**Output:**
- data/step01_per_test_sleep.csv

**Validation Requirement:**
Validation tools MUST be used after sleep extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_per_test_sleep.csv: ~400 rows x 4 columns
- Columns: UID (object), Test (int), Sleep_Hours (float), Sleep_Quality (int)

*Value Ranges:*
- Sleep_Hours in [0, 24] (biologically plausible)
- Sleep_Quality in [1, 10] (Likert scale range)
- Test in [1, 2, 3, 4] (four sessions)
- UID format consistent with master pattern

*Data Quality:*
- At least 300 rows (>=75% data completion)
- No negative sleep values
- All UIDs have >=3 test sessions
- Missing data <25% per variable

*Log Validation:*
- Required patterns: "Sleep extraction complete", "N=XXX observations"
- Forbidden patterns: "ERROR", "parsing failed", "no data found"

**Expected Behavior on Validation Failure:**
Raise error with extraction issue, log to logs/step01_extract_sleep.log, invoke g_debug for data format issues

### Step 2: Merge Sleep and Theta Data
**Dependencies:** Step 1 (sleep extraction), Ch5 5.1.1 (theta scores)
**Complexity:** Low (~5 minutes)

**Purpose:** Create unified dataset combining per-test sleep and memory performance

**Input:**
- data/step01_per_test_sleep.csv (sleep data)
- results/ch5/5.1.1/data/step03_theta_scores.csv (or fallback pattern)
- Expected theta format: UID, Test, theta_all, SE

**Processing:**
- Load theta scores from Ch5 (theta_all omnibus scores)
- Merge sleep and theta data on UID and Test
- Exclude participants with <3 complete test sessions
- Create person-mean variables for between-person effects:
  - Sleep_Hours_PM = person mean sleep hours
  - Sleep_Quality_PM = person mean sleep quality
- Center within-person variables:
  - Sleep_Hours_WP = Sleep_Hours - Sleep_Hours_PM
  - Sleep_Quality_WP = Sleep_Quality - Sleep_Quality_PM
- Final dataset: 400 rows with complete sleep and theta data

**Output:**
- data/step02_theta_sleep_merged.csv

**Validation Requirement:**
Validation tools MUST be used after merging execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_theta_sleep_merged.csv: ~400 rows x 9 columns
- Columns: UID, Test, theta_all, SE, Sleep_Hours, Sleep_Quality, Sleep_Hours_PM, Sleep_Quality_PM, Sleep_Hours_WP, Sleep_Quality_WP

*Value Ranges:*
- theta_all in [-3, 3] (IRT ability scale)
- SE in [0.1, 1.0] (standard errors positive)
- Sleep_Hours_WP in [-12, 12] (within-person deviation)
- Sleep_Quality_WP in [-9, 9] (within-person deviation)

*Data Quality:*
- All 100 UIDs present (no exclusions expected)
- Person-mean centering: mean(WP variables) ≈ 0 for each UID
- Complete data: no missing theta or sleep values
- Reasonable within-person variability (SD_WP > 0)

*Log Validation:*
- Required patterns: "Merge complete", "N=400 observations", "100 participants"
- Forbidden patterns: "ERROR", "missing data", "merge failed"

**Expected Behavior on Validation Failure:**
Raise error with merge issue, log to logs/step02_merge_data.log, check data compatibility

### Step 3: Descriptive Analysis and Data Quality
**Dependencies:** Step 2 (merged dataset)
**Complexity:** Low (~5 minutes)

**Purpose:** Examine within-person sleep variability and data quality before modeling

**Input:**
- data/step02_theta_sleep_merged.csv

**Processing:**
- Calculate descriptive statistics by variable
- Compute within-person sleep variability (SD within each UID)
- Assess sleep range per person (max - min sleep hours/quality)
- Examine theta distribution and outliers (Cook's D > 4/n threshold)
- Check correlation between sleep variables (multicollinearity assessment)
- Summarize missing data patterns and participant exclusions
- Generate data quality flags for potential issues

**Output:**
- data/step03_descriptive_stats.csv

**Validation Requirement:**
Validation tools MUST be used after descriptive analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_descriptive_stats.csv: summary statistics table
- Expected sections: overall_stats, within_person_variability, correlations, outliers

*Value Ranges:*
- Within-person SD > 0 (variability required for analysis)
- Correlation between sleep variables <0.90 (multicollinearity check)
- Number of outliers <10% of sample

*Data Quality:*
- All 100 participants analyzed
- Sleep variability present (not all identical values)
- Theta scores follow expected IRT distribution
- Reasonable correlation structure

*Log Validation:*
- Required patterns: "Descriptive analysis complete", "Sleep variability confirmed"
- Forbidden patterns: "ERROR", "no variability", "excessive missing"

**Expected Behavior on Validation Failure:**
Log warning for data quality issues, proceed unless critical problems detected

### Step 4: Fit Multilevel Models
**Dependencies:** Step 3 (descriptive analysis)
**Complexity:** High (~15 minutes including diagnostics)

**Purpose:** Fit linear mixed-effects models to test within-person sleep effects

**Input:**
- data/step02_theta_sleep_merged.csv

**Processing:**
- Model 1 (within-person only): theta_all ~ Sleep_Hours_WP + Sleep_Quality_WP + Test_Session + (1|UID)
- Model 2 (decomposed effects): theta_all ~ Sleep_Hours_WP + Sleep_Quality_WP + Sleep_Hours_PM + Sleep_Quality_PM + Test_Session + (1|UID)
- Implementation: statsmodels MixedLM with REML estimation
- Extract fixed effects: coefficients, standard errors, t-statistics
- Extract random effects: participant-specific intercepts
- Compute model fit: AIC, BIC, log-likelihood, R² (marginal and conditional)
- Test session as covariate: controls for practice effects
- Multiple comparison correction:
  - Family: Within-RQ (4 sleep predictors in Model 2)
  - Bonferroni: alpha = 0.05/4 = 0.0125 per test
  - Report BOTH uncorrected AND corrected p-values (Decision D068)

**Output:**
- data/step04_multilevel_model_results.csv

**Validation Requirement:**
Validation tools MUST be used after model fitting execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_multilevel_model_results.csv: model results table
- Expected: 2 models x 5-6 predictors each, coefficients with CIs

*Value Ranges:*
- Coefficients in [-1, 1] (standardized scale expected)
- Standard errors > 0
- t-statistics in [-10, 10] (reasonable range)
- p-values in [0, 1]
- AIC/BIC positive, reasonable magnitude

*Data Quality:*
- Both models converged successfully
- Random effects variance > 0 (participant differences)
- Fixed effects reasonable magnitude
- No convergence warnings

*Log Validation:*
- Required patterns: "Model fitting complete", "REML converged"
- Required patterns: "Model 1 fitted", "Model 2 fitted"
- Forbidden patterns: "ERROR", "convergence failed", "singular fit"

**Expected Behavior on Validation Failure:**
Check convergence issues, try different optimizers, log to logs/step04_fit_models.log

### Step 5: Model Diagnostics and Assumptions
**Dependencies:** Step 4 (fitted models)
**Complexity:** Medium (~10 minutes)

**Purpose:** Validate LMM assumptions and check model adequacy

**Input:**
- data/step04_multilevel_model_results.csv (fitted models)
- data/step02_theta_sleep_merged.csv (for residual computation)

**Processing:**
- Extract residuals from both models
- Check normality: Shapiro-Wilk test on residuals
- Check homoscedasticity: Breusch-Pagan test
- Check multicollinearity: VIF for sleep predictors
- Examine influential observations: Cook's D > 4/n
- Test random effects normality: Q-Q plot of participant intercepts
- Residual vs fitted plots: visual inspection for patterns
- Remedial actions if violated:
  - Normality p < 0.05: Report bootstrap CIs as primary (see Step 6)
  - Heteroscedasticity p < 0.05: Add robust standard errors (HC3)
  - VIF > 5: Document multicollinearity, consider ridge if VIF > 10
  - Outliers (Cook's D > 4/n): Report results with/without outliers

**Output:**
- data/step05_model_diagnostics.csv

**Validation Requirement:**
Validation tools MUST be used after diagnostic execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_model_diagnostics.csv: diagnostic test results
- Expected tests: normality, homoscedasticity, VIF, Cook's D, random effects

*Value Ranges:*
- VIF values in [1, 10] (multicollinearity acceptable if <10)
- Cook's D values in [0, 1] (outlier detection)
- Shapiro-Wilk p-values in [0, 1]
- Number of outliers <10% of sample

*Data Quality:*
- All diagnostic tests completed
- Remedial actions documented if assumptions violated
- Residual patterns reasonable
- No critical assumption violations

*Log Validation:*
- Required patterns: "Diagnostics complete", "Assumption checks: COMPLETE"
- Required patterns: "Normality: [PASS/FAIL]", "Homoscedasticity: [PASS/FAIL]"
- Forbidden patterns: "ERROR", "test failed to run"

**Expected Behavior on Validation Failure:**
Document assumption violations, implement remedial actions, proceed with robust methods if needed

### Step 6: Cross-Validation and Bootstrap
**Dependencies:** Step 5 (model diagnostics)
**Complexity:** High (~15 minutes)

**Purpose:** Assess model generalizability and compute robust confidence intervals

**Input:**
- data/step02_theta_sleep_merged.csv

**Processing:**
- **Cross-Validation:**
  - Implement 5-fold participant-level cross-validation
  - Use GroupKFold from sklearn.model_selection (groups=UID)
  - Random seed: 42 for reproducibility
  - For each fold: fit Model 2 on training UIDs, evaluate on test UIDs
  - Compute R² for each fold (marginal and conditional)
  - Flag overfitting if train-test R² gap > 0.10
- **Bootstrap Confidence Intervals:**
  - Participant-level block bootstrap (preserves within-participant correlation)
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - For each iteration: resample 100 UIDs with replacement, keep all observations
  - Fit Model 2, extract fixed effects coefficients
  - 95% CI: percentile method (2.5th, 97.5th percentiles)
- **Sensitivity Analysis:**
  - Exclude outliers (Cook's D > 4/n) and refit models
  - Compare effect sizes with/without outliers

**Output:**
- data/step06_cross_validation.csv
- data/step06_bootstrap_CIs.csv

**Validation Requirement:**
Validation tools MUST be used after CV/bootstrap execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_cross_validation.csv: CV results (5 rows for folds)
- data/step06_bootstrap_CIs.csv: bootstrap CIs (4 rows for sleep predictors)

*Value Ranges:*
- CV R² in [0, 1] (reasonable model performance)
- Bootstrap CIs contain original estimates
- CV standard deviation <0.20 (stable performance)

*Data Quality:*
- All 5 CV folds completed successfully
- Bootstrap iterations: 1000 completed
- CIs have proper ordering (lower < estimate < upper)
- No convergence failures in bootstrap

*Log Validation:*
- Required patterns: "Cross-validation complete: 5 folds"
- Required patterns: "Bootstrap complete: 1000 iterations"
- Forbidden patterns: "ERROR", "convergence failed", "fold failed"

**Expected Behavior on Validation Failure:**
Retry with different CV strategy, reduce bootstrap iterations if memory issues, log problems

### Step 7: Power Analysis and Effect Size Interpretation
**Dependencies:** Step 6 (CV and bootstrap)
**Complexity:** Medium (~5 minutes)

**Purpose:** Evaluate statistical power and interpret effect sizes for sleep interventions

**Input:**
- data/step04_multilevel_model_results.csv
- data/step06_bootstrap_CIs.csv

**Processing:**
- **Post-hoc Power Analysis:**
  - Given: N=400 observations, ~100 level-2 units (participants)
  - Model: 4-6 fixed effects predictors
  - Alpha: 0.05/4 = 0.0125 (Bonferroni corrected within-RQ)
  - Calculate power for observed within-person sleep effects
  - Use Monte Carlo simulation or analytic approximation
  - Report power for each sleep predictor
- **Effect Size Interpretation:**
  - Convert standardized effects to practical units
  - Sleep hours: effect per 1-hour change in sleep
  - Sleep quality: effect per 1-point change in quality rating
  - Compare within-person vs between-person effect sizes
  - Clinical significance: meaningful for sleep interventions (>0.05 theta units)
- **Model Comparison:**
  - LRT test: Model 1 vs Model 2 (within vs decomposed effects)
  - AIC/BIC comparison for model selection

**Output:**
- data/step07_power_effect_sizes.csv

**Validation Requirement:**
Validation tools MUST be used after power analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_power_effect_sizes.csv: power and effect size results
- Expected: power estimates, practical interpretations, model comparisons

*Value Ranges:*
- Power estimates in [0, 1]
- Effect sizes in [-1, 1] (practical range)
- LRT p-values in [0, 1]

*Data Quality:*
- Power analysis completed for all predictors
- Effect size interpretations provided
- Model comparison results available

*Log Validation:*
- Required patterns: "Power analysis complete", "Effect sizes interpreted"
- Forbidden patterns: "ERROR", "calculation failed"

**Expected Behavior on Validation Failure:**
Use alternative power calculation method, document limitations if power cannot be computed

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
- data/step00_dependency_validation.txt (dependency check results)
- data/step01_per_test_sleep.csv (extracted sleep data per test)
- data/step02_theta_sleep_merged.csv (400 rows: UID x Test x Sleep x Theta)
- data/step03_descriptive_stats.csv (within-person sleep variability)
- data/step04_multilevel_model_results.csv (fixed effects, random effects, model fit)
- data/step05_model_diagnostics.csv (assumption checks, remedial actions)
- data/step06_cross_validation.csv (CV performance metrics)
- data/step06_bootstrap_CIs.csv (bootstrapped confidence intervals)
- data/step07_power_effect_sizes.csv (power analysis, effect interpretation)

### Logs (ONLY execution logs)
- logs/step00_validate_dependencies.log
- logs/step01_extract_sleep.log
- logs/step02_merge_data.log
- logs/step03_descriptive_analysis.log
- logs/step04_fit_models.log
- logs/step05_model_diagnostics.log
- logs/step06_cross_validation.log
- logs/step07_power_analysis.log

### Plots (EMPTY until rq_plots runs)
Note: Plot source CSVs created in data/ folder for rq_plots agent:
- data/step03_descriptive_plot_data.csv (for sleep variability plots)
- data/step05_diagnostic_plot_data.csv (for residual plots)
- data/step06_effect_plot_data.csv (for effect size visualization)

### Results (EMPTY until rq_results runs)
Note: summary.md created by rq_results agent using all data/ outputs

---

## Expected Data Formats

### Step-to-Step Transformations
1. **Step 1->2:** Sleep data (wide by test) merged with theta scores on UID+Test
2. **Step 2->3:** Long format maintained, person-mean variables added
3. **Step 3->4:** Same dataset used for model fitting with descriptive context
4. **Step 4->5:** Model objects converted to residuals for diagnostics
5. **Step 5->6:** Raw data resampled for CV/bootstrap procedures
6. **Step 6->7:** Effect estimates used for power and interpretation

### Column Naming Conventions
- **UID:** Participant identifier (consistent with master.xlsx)
- **Test:** Test session number (1, 2, 3, 4)
- **theta_all:** Omnibus ability estimate from Ch5 IRT analysis
- **Sleep_Hours:** Actual sleep hours before test
- **Sleep_Quality:** Subjective sleep quality rating (1-10)
- **Sleep_Hours_WP:** Within-person centered sleep hours
- **Sleep_Quality_WP:** Within-person centered sleep quality
- **Sleep_Hours_PM:** Person-mean sleep hours (between-person)
- **Sleep_Quality_PM:** Person-mean sleep quality (between-person)

### Data Type Constraints
- **UID:** object (string identifier)
- **Test:** int64 (1-4 range)
- **theta_all:** float64 (IRT scale, nullable=False)
- **Sleep variables:** float64 (nullable=False after cleaning)
- **Model results:** float64 for coefficients, p-values, CIs

---

## Cross-RQ Dependencies

### Dependency on Ch5 5.1.1
**Required Output:** Omnibus theta scores per participant per test
**File Location:** results/ch5/5.1.1/data/step03_theta_scores.csv
**Format Expected:** UID, Test, theta_all, SE (400 rows)
**Fallback Strategy:** Search for *theta*.{csv,txt} pattern in Ch5 5.1.1/data/
**Validation:** Step 0 checks Ch5 completion before proceeding

### No Dependencies on Other Ch7 RQs
This RQ uses derived data from Ch5 and master.xlsx only. Independent of other Ch7 analyses.

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
**Validation Requirement:** Dependency validation MUST pass before proceeding
**Validation Tools:** File existence checks, data format validation
**Failure Action:** QUIT with specific dependency error message

#### Step 1: Extract Sleep Data
**Validation Requirement:** Sleep extraction completeness and format validation
**Validation Tools:** Data range checks, missing data assessment
**Failure Action:** Retry extraction, log parsing errors, invoke g_debug if needed

#### Step 2: Merge Sleep and Theta Data
**Validation Requirement:** Merge completeness and person-mean centering validation
**Validation Tools:** Row count verification, centering accuracy checks
**Failure Action:** Check data compatibility, retry merge with different approaches

#### Step 3: Descriptive Analysis
**Validation Requirement:** Sleep variability confirmation, outlier detection
**Validation Tools:** Distribution checks, correlation validation
**Failure Action:** Log data quality warnings, proceed unless critical issues

#### Step 4: Fit Multilevel Models
**Validation Requirement:** Model convergence and parameter reasonableness
**Validation Tools:** Convergence status, effect size bounds checking
**Failure Action:** Try alternative optimizers, simplify random structure if needed

#### Step 5: Model Diagnostics
**Validation Requirement:** Assumption test completion and remedial action documentation
**Validation Tools:** Statistical test execution, threshold evaluation
**Failure Action:** Implement remedial actions, document assumption violations

#### Step 6: Cross-Validation and Bootstrap
**Validation Requirement:** CV/bootstrap completion with reasonable uncertainty estimates
**Validation Tools:** Iteration completion checks, CI bounds validation
**Failure Action:** Reduce iterations, try alternative resampling if memory constraints

#### Step 7: Power Analysis
**Validation Requirement:** Power calculation completion and effect interpretation
**Validation Tools:** Power estimate bounds, practical significance assessment
**Failure Action:** Use alternative power methods, document calculation limitations

---

## Summary

**Total Steps:** 8 (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** ~45 minutes
**Cross-RQ Dependencies:** Ch5 5.1.1 (theta scores)
**Primary Outputs:** Multilevel model results with within-person sleep effects
**Validation Coverage:** 100% (all 8 steps have 4-layer validation requirements)

**Key Hypothesis:** Poor sleep before a specific test will impair that test's performance (within-person effect), independent of individual differences in overall sleep quality.

**Critical Methodological Notes:**
- Within-person design controls for individual differences in chronic sleep patterns
- Participant-level CV and bootstrap respect hierarchical data structure
- Multiple comparison correction applied within-RQ (4 sleep predictors)
- Decision D068 ensures dual p-value reporting throughout
- Random seed=42 ensures full reproducibility
- Practice effects controlled via test session covariate

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-03): Initial plan created by rq_planner agent with v5.1 enhanced specifications