# Analysis Plan: RQ 7.5.3 - Memory Strategies Predicting Performance

**Research Question:** 7.5.3
**Created:** 2026-01-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

**Brief Description:** Examine relationships between self-reported memory strategies (rehearsal frequency, mnemonic use) and REMEMVR performance using correlational analysis and group comparisons with hierarchical regression controls.

**Pipeline:** Correlational Analysis + Independent Samples t-test + Hierarchical Regression
**Steps:** 8 total analysis steps (Step 0: validation + Steps 1-7: analysis)  
**Estimated Runtime:** ~45-60 minutes

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- Cross-RQ dependency on Ch5 5.1.1 for theta_all scores
- Text coding reliability requirements for mnemonic strategies
- Bootstrap CI procedures for robust inference

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 5.1.1 outputs exist and master.xlsx accessibility before proceeding with strategy analysis

**Input:**
- Check Ch5 5.1.1 status: results/ch5/5.1.1/status.yaml (verify rq_results: success)
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/*theta*.{csv,txt}
- Fallback pattern: results/ch5/5.1.1/data/*scores*.csv
- Expected content: Participant theta_all scores (omnibus memory performance)
- STR data source: data/cache/master.xlsx (STR questionnaire tags)
- If Ch5 not found: QUIT with "Ch5 5.1.1 theta outputs not found"

**Processing:**
- Check Ch5 5.1.1 completed successfully (status.yaml)
- Locate theta score file using multiple search patterns
- Verify file contains theta_all column and 100 participants
- Check master.xlsx accessibility and STR tag patterns
- Log all validation results with file paths found
- Verify expected STR tag patterns: {UID}-RVR-T{N}-STR-X-TNK1- and {UID}-RVR-T{N}-STR-X-MNE1-

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt: text file with validation results
- Expected format: Key-value pairs showing file paths and validation status

*Value Ranges:*
- N/A (validation step only)

*Data Quality:*
- All required file paths identified or missing status documented
- Ch5 5.1.1 completion status verified
- STR tag pattern accessibility confirmed

*Log Validation:*
- Required pattern: "VALIDATION COMPLETE - Dependencies verified"
- Required pattern: "Ch5 5.1.1 status: success"
- Required pattern: "Theta file located:"
- Forbidden patterns: "ERROR", "FAIL", "not found"

**Expected Behavior on Validation Failure:**
- Quit with specific missing file error
- Log to logs/step00_validate_dependencies.log
- Provide clear dependency resolution guidance

### Step 1: Extract Participant Performance Data
**Dependencies:** Step 0 (dependency validation)
**Complexity:** Low (<5 minutes)

**Purpose:** Load theta_all scores from Ch5 5.1.1 outputs to serve as outcome measure

**Input:**
- Primary: results/ch5/5.1.1/data/step03_theta_scores.csv
- Alternative: results/ch5/5.1.1/data/*theta*.{csv,txt}
- Expected columns: UID, theta_all (omnibus episodic memory performance)
- Expected format: 100 rows (participants), UID as string, theta_all as float

**Processing:**
- Load theta score data using pandas
- Verify all 100 participants present with valid UIDs
- Check theta_all column exists and is numeric
- Verify theta range reasonable for IRT scale (typically -3 to 3)
- Remove any duplicate UIDs (keep first occurrence)
- Log summary statistics: mean, SD, range of theta_all scores

**Output:**
- data/step01_theta_scores.csv

**Validation Requirement:**
Validation tools MUST be used after data extraction execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_theta_scores.csv: 100 rows x 2 columns (UID, theta_all)
- Data types: UID (object), theta_all (float64)

*Value Ranges:*
- theta_all in [-4, 4] (IRT ability scale with tolerance)
- No NaN values in theta_all column
- All theta_all values finite (no inf values)

*Data Quality:*
- Exactly 100 unique UIDs
- No missing data in either column
- UIDs match expected format pattern
- Theta values follow approximate normal distribution

*Log Validation:*
- Required pattern: "Loaded theta scores: 100 participants"
- Required pattern: "Theta range: [min_val, max_val]"
- Required pattern: "VALIDATION - PASS"
- Forbidden patterns: "ERROR", "duplicate", "missing"

**Expected Behavior on Validation Failure:**
- Raise error with specific data quality issue
- Log to logs/step01_extract_theta.log
- Quit immediately, invoke g_debug

### Step 2: Extract and Code Strategy Variables
**Dependencies:** Step 1 (theta scores loaded)
**Complexity:** High (~15-20 minutes including text coding)

**Purpose:** Extract rehearsal frequency and mnemonic strategy variables from STR questionnaire, including reliability validation for text coding

**Input:**
- data/cache/master.xlsx (STR questionnaire responses)
- STR tag patterns: {UID}-RVR-T{N}-STR-X-TNK1- (rehearsal frequency)
- STR tag patterns: {UID}-RVR-T{N}-STR-X-MNE1- (mnemonic strategy text)
- Expected: 4 tests per participant (T1-T4)

**Processing:**
- Extract rehearsal frequency ratings from TNK1 tags (quantitative)
- Compute mean rehearsal frequency across T1-T4 per participant
- Extract mnemonic strategy text responses from MNE1 tags
- Develop binary coding scheme for mnemonic use (present/absent):
  - Code random subsample (n=20, 20%) independently by two raters
  - Operational definitions: Any mention of memory aids, associations, imagery, or organizational strategies = present
  - Compute inter-rater reliability (Cohen's kappa)
  - Require k >= 0.80 for acceptable agreement
  - If k < 0.80: refine coding criteria and re-code until acceptable reliability achieved
- Apply final coding scheme to all participants
- Handle missing STR data (exclude participants with <2 tests of data)
- Create final dataset with UID, rehearsal_freq_mean, mnemonic_use_binary

**Output:**
- data/step02_strategy_variables.csv
- data/step02_coding_reliability.txt (inter-rater statistics)

**Validation Requirement:**
Validation tools MUST be used after strategy coding execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_strategy_variables.csv: <= 100 rows x 3 columns (UID, rehearsal_freq_mean, mnemonic_use_binary)
- data/step02_coding_reliability.txt: text file with kappa statistics
- Data types: UID (object), rehearsal_freq_mean (float64), mnemonic_use_binary (int64)

*Value Ranges:*
- rehearsal_freq_mean in [1, 10] (Likert scale range with tolerance)
- mnemonic_use_binary in [0, 1] (binary coding)
- kappa in reliability file >= 0.80 (acceptable agreement)

*Data Quality:*
- At least 90 participants included (allow for some missing STR data)
- No NaN values in strategy variables
- Mnemonic use distribution reasonable (5-50% using strategies)
- Rehearsal frequency shows variation (not all same value)

*Log Validation:*
- Required pattern: "Strategy extraction complete"
- Required pattern: "Inter-rater reliability: kappa = X.XX"
- Required pattern: "Final sample: N participants"
- Forbidden patterns: "ERROR", "coding failed", "reliability < 0.80"

**Expected Behavior on Validation Failure:**
- If reliability < 0.80: refine coding, re-validate
- If missing data > 10%: document but proceed
- Log detailed coding issues to logs/step02_code_strategies.log

### Step 3: Merge Data and Descriptive Analysis
**Dependencies:** Steps 1-2 (theta scores + strategy variables)
**Complexity:** Low (~5 minutes)

**Purpose:** Combine performance and strategy data, compute descriptive statistics and check distributions

**Input:**
- data/step01_theta_scores.csv
- data/step02_strategy_variables.csv

**Processing:**
- Inner join datasets on UID (only participants with both theta and strategy data)
- Verify successful merge (expect >= 90 participants)
- Compute descriptive statistics for all variables:
  - theta_all: mean, SD, range, skewness, kurtosis
  - rehearsal_freq_mean: mean, SD, range, distribution
  - mnemonic_use_binary: frequency counts, percentages
- Check for extreme values using boxplot criteria (IQR method)
- Test distributions for normality using Shapiro-Wilk test
- Create correlation matrix between continuous variables
- Generate summary statistics table

**Output:**
- data/step03_merged_analysis_dataset.csv
- data/step03_descriptive_statistics.csv

**Validation Requirement:**
Validation tools MUST be used after descriptive analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_merged_analysis_dataset.csv: >= 90 rows x 4 columns (UID, theta_all, rehearsal_freq_mean, mnemonic_use_binary)
- data/step03_descriptive_statistics.csv: summary statistics table
- Data types: UID (object), theta_all (float64), rehearsal_freq_mean (float64), mnemonic_use_binary (int64)

*Value Ranges:*
- theta_all in [-4, 4] (IRT scale)
- rehearsal_freq_mean in [1, 10] (Likert scale)
- mnemonic_use_binary in [0, 1] (binary)

*Data Quality:*
- At least 90 participants in merged dataset
- No missing data in analysis variables
- Reasonable distributions (no all-zeros variables)
- Descriptive statistics within expected ranges

*Log Validation:*
- Required pattern: "Merge complete: N participants"
- Required pattern: "Descriptive statistics computed"
- Required pattern: "VALIDATION - PASS"
- Forbidden patterns: "ERROR", "merge failed", "empty dataset"

**Expected Behavior on Validation Failure:**
- Raise error with merge diagnostics
- Log detailed merge results to logs/step03_merge_descriptives.log
- Quit immediately if < 80 participants remain

### Step 4: Primary Correlation Analysis
**Dependencies:** Step 3 (merged dataset)
**Complexity:** Medium (~10 minutes including bootstrap)

**Purpose:** Examine correlation between rehearsal frequency and theta_all performance with confidence intervals

**Input:**
- data/step03_merged_analysis_dataset.csv

**Processing:**
- Test normality assumptions for both variables (Shapiro-Wilk test)
- Compute Pearson correlation between rehearsal_freq_mean and theta_all
- Calculate 95% confidence intervals using Fisher z-transformation
- Bootstrap 95% confidence intervals for robust inference:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Method: Participant-level resampling with replacement
  - CI computation: percentile method (2.5th, 97.5th percentiles)
- Apply multiple comparison correction:
  - Family: Within-RQ strategy analyses (2 tests: correlation + t-test)
  - Bonferroni correction: alpha = 0.05/2 = 0.025 per test
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Remedial actions if normality violated:
  - If Shapiro-Wilk p < 0.05: Use Spearman correlation as alternative
  - Report both Pearson and Spearman results if normality violated
  - Emphasize bootstrap CIs as primary inference

**Output:**
- data/step04_correlation_results.csv
- data/step04_correlation_diagnostics.txt

**Validation Requirement:**
Validation tools MUST be used after correlation analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_correlation_results.csv: 1 row x 8 columns (r, ci_lower, ci_upper, p_uncorrected, p_bonferroni, bootstrap_ci_lower, bootstrap_ci_upper, n)
- data/step04_correlation_diagnostics.txt: normality tests and remedial actions
- Data types: All correlation statistics as float64

*Value Ranges:*
- r in [-1, 1] (correlation coefficient bounds)
- p-values in [0, 1] (valid probability range)
- CI bounds: ci_lower < r < ci_upper
- Bootstrap CIs reasonable (similar to parametric if normality holds)

*Data Quality:*
- All confidence intervals valid (lower < upper)
- Bootstrap CIs computed from 1000 iterations
- Both uncorrected and corrected p-values present
- Normality test results documented

*Log Validation:*
- Required pattern: "Correlation analysis complete: r = X.XX"
- Required pattern: "Bootstrap CI computed: 1000 iterations"
- Required pattern: "Multiple testing correction applied"
- Forbidden patterns: "ERROR", "convergence failed", "invalid correlation"

**Expected Behavior on Validation Failure:**
- Raise error with specific statistical issue
- Log detailed diagnostics to logs/step04_correlation.log
- Check for computational problems (infinite values, etc.)

### Step 5: Group Comparison Analysis (Mnemonic Use)
**Dependencies:** Step 3 (merged dataset)
**Complexity:** Medium (~10 minutes including diagnostics)

**Purpose:** Compare theta_all performance between mnemonic users and non-users using independent samples t-test

**Input:**
- data/step03_merged_analysis_dataset.csv

**Processing:**
- Split participants by mnemonic_use_binary (0 = no use, 1 = use)
- Check group sizes (ensure both groups have n >= 5 for valid t-test)
- Test normality assumptions for each group (Shapiro-Wilk test)
- Test variance equality assumption (Levene's test)
- Perform independent samples t-test:
  - Use Welch's t-test if variance equality violated (Levene p < 0.05)
  - Use standard t-test if assumptions met
- Calculate Cohen's d effect size with 95% confidence intervals
- Apply multiple comparison correction:
  - Family: Within-RQ strategy analyses (2 tests: correlation + t-test)  
  - Bonferroni correction: alpha = 0.05/2 = 0.025 per test
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Bootstrap 95% confidence intervals for group difference:
  - Iterations: 1000
  - Random seed: 42 for reproducibility
  - Resample participants within groups, compute mean difference each iteration
  - CI: percentile method (2.5th, 97.5th percentiles)
- Remedial actions if assumptions violated:
  - If normality violated: Report bootstrap CIs as primary
  - If unequal variances: Use Welch's t-test

**Output:**
- data/step05_group_comparison_results.csv
- data/step05_group_diagnostics.txt

**Validation Requirement:**
Validation tools MUST be used after group comparison execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_group_comparison_results.csv: 1 row x 12 columns (mean_no_use, mean_use, mean_diff, t_stat, df, p_uncorrected, p_bonferroni, cohens_d, d_ci_lower, d_ci_upper, bootstrap_ci_lower, bootstrap_ci_upper)
- data/step05_group_diagnostics.txt: assumption tests and group summaries
- Data types: All statistics as float64 except df (int64)

*Value Ranges:*
- mean values in reasonable theta range [-3, 3]
- t_stat finite value (not infinite)
- p-values in [0, 1] (valid probability range)
- Cohen's d typically in [-2, 2] for behavioral data
- df > 0 (valid degrees of freedom)

*Data Quality:*
- Both groups have n >= 5 participants
- Effect size CIs valid (lower < d < upper)
- Bootstrap CIs computed from 1000 iterations
- Assumption test results documented (normality, variance equality)

*Log Validation:*
- Required pattern: "Group comparison complete: t = X.XX"
- Required pattern: "Effect size: Cohen's d = X.XX"
- Required pattern: "Bootstrap CI computed: 1000 iterations"
- Forbidden patterns: "ERROR", "insufficient group size", "invalid t-test"

**Expected Behavior on Validation Failure:**
- Raise error with specific group comparison issue
- Log detailed diagnostics to logs/step05_group_comparison.log
- Check for unbalanced groups or assumption violations

### Step 6: Hierarchical Regression with Controls
**Dependencies:** Step 3 (merged dataset)
**Complexity:** Medium (~10 minutes)

**Purpose:** Test whether strategy effects remain significant after controlling for demographic and cognitive variables

**Input:**
- data/step03_merged_analysis_dataset.csv
- Need to add control variables: age, cognitive ability (NART scores)

**Processing:**
- Extract control variables from master.xlsx:
  - Age from demographic tags
  - NART scores (cognitive ability proxy)
- Fit hierarchical regression models:
  - Model 1 (Controls): theta_all ~ age + NART_score
  - Model 2 (Full): theta_all ~ age + NART_score + rehearsal_freq_mean + mnemonic_use_binary
- Compute R-squared change and significance test (F-test)
- Extract standardized beta coefficients with confidence intervals
- Check regression assumptions:
  - Normality of residuals (Shapiro-Wilk test)
  - Homoscedasticity (Breusch-Pagan test)  
  - Multicollinearity (VIF for each predictor)
- Apply multiple comparison correction within model:
  - Strategy predictors: 2 tests (rehearsal + mnemonic)
  - Bonferroni: alpha = 0.05/2 = 0.025 per strategy test
  - Report BOTH uncorrected AND corrected p-values (Decision D068)
- Remedial actions if assumptions violated:
  - Normality violation: Report HC3 robust standard errors
  - Heteroscedasticity: Use HC3 heteroscedasticity-consistent SEs
  - VIF > 5: Document multicollinearity, proceed with caution
  - VIF > 10: Consider removing collinear predictors

**Output:**
- data/step06_hierarchical_regression.csv
- data/step06_regression_diagnostics.txt

**Validation Requirement:**
Validation tools MUST be used after hierarchical regression execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_hierarchical_regression.csv: Model comparison and coefficient table
- data/step06_regression_diagnostics.txt: Assumption tests and VIF values
- Expected columns: model, predictor, beta, se, t_stat, p_uncorrected, p_corrected, vif, r2, r2_change

*Value Ranges:*
- beta coefficients in [-2, 2] (standardized predictors)
- se > 0 (positive standard errors)
- p-values in [0, 1]
- VIF values >= 1 (variance inflation factor bounds)
- R-squared in [0, 1]

*Data Quality:*
- Both models fitted successfully
- All coefficients finite (no NaN or infinite values)
- VIF values computed for all predictors
- R-squared change test performed

*Log Validation:*
- Required pattern: "Hierarchical regression complete"
- Required pattern: "Model 1 R² = X.XX, Model 2 R² = X.XX"
- Required pattern: "R² change significance test: F = X.XX"
- Forbidden patterns: "ERROR", "convergence failed", "singular matrix"

**Expected Behavior on Validation Failure:**
- Raise error with specific regression issue
- Log detailed model diagnostics to logs/step06_regression.log
- Check for perfect multicollinearity or model specification problems

### Step 7: Sensitivity Analysis and Effect Size Summary
**Dependencies:** Steps 4-6 (all primary analyses)
**Complexity:** Medium (~10 minutes)

**Purpose:** Conduct sensitivity analyses, outlier assessment, and compile final effect size summary with power analysis

**Input:**
- data/step03_merged_analysis_dataset.csv
- Results from steps 4-6 (correlation, t-test, regression)

**Processing:**
- Identify outliers using multiple criteria:
  - Leverage values > 2(p+1)/n for regression
  - Cook's distance > 4/n for regression influence
  - z-scores > 3.29 (p < 0.001) for univariate outliers
- Conduct sensitivity analyses:
  - Remove participants with extreme strategy scores (>3 SD from mean)
  - Remove participants with extreme theta scores (>3 SD)
  - Re-run key analyses (correlation, t-test) without outliers
  - Use robust correlation methods (Spearman, Kendall's tau)
- Post-hoc power analysis for main effects:
  - Correlation: Power to detect r = 0.18 with N, alpha = 0.025
  - T-test: Power to detect Cohen's d with observed group sizes
  - Report actual power for observed effect sizes
  - Use G*Power calculations or statsmodels.stats.power
- Compile effect size summary table:
  - All correlations with 95% CIs (parametric + bootstrap)
  - Group differences with Cohen's d and CIs
  - Regression coefficients with standardized betas
- Assess effect stability across analytical decisions
- Document limitations and interpretive cautions

**Output:**
- data/step07_sensitivity_analysis.csv
- data/step07_effect_size_summary.csv
- data/step07_power_analysis.txt

**Validation Requirement:**
Validation tools MUST be used after sensitivity analysis execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_sensitivity_analysis.csv: Outlier identification and robust analysis results
- data/step07_effect_size_summary.csv: Comprehensive effect size table
- data/step07_power_analysis.txt: Power calculations for main effects

*Value Ranges:*
- Effect sizes within reasonable bounds for behavioral data
- Power values in [0, 1] (valid probability range)
- Outlier statistics: leverage < 1, Cook's D < 1
- z-scores for outlier detection finite values

*Data Quality:*
- Outlier identification criteria applied consistently
- Sensitivity analyses show comparable patterns
- Power calculations based on appropriate effect size metrics
- Effect size CIs all valid (lower < effect < upper)

*Log Validation:*
- Required pattern: "Sensitivity analysis complete"
- Required pattern: "Outlier detection: N outliers identified"
- Required pattern: "Power analysis: correlation power = X.XX"
- Forbidden patterns: "ERROR", "power calculation failed"

**Expected Behavior on Validation Failure:**
- Raise error with specific sensitivity analysis issue
- Log detailed outlier and power diagnostics to logs/step07_sensitivity.log
- Proceed with warnings if minor computational issues

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs in data/ folder)
- data/step00_dependency_validation.txt
- data/step01_theta_scores.csv
- data/step02_strategy_variables.csv  
- data/step02_coding_reliability.txt
- data/step03_merged_analysis_dataset.csv
- data/step03_descriptive_statistics.csv
- data/step04_correlation_results.csv
- data/step04_correlation_diagnostics.txt
- data/step05_group_comparison_results.csv
- data/step05_group_diagnostics.txt
- data/step06_hierarchical_regression.csv
- data/step06_regression_diagnostics.txt
- data/step07_sensitivity_analysis.csv
- data/step07_effect_size_summary.csv
- data/step07_power_analysis.txt

### Logs (ONLY execution logs in logs/ folder)
- logs/step00_validate_dependencies.log
- logs/step01_extract_theta.log
- logs/step02_code_strategies.log
- logs/step03_merge_descriptives.log
- logs/step04_correlation.log
- logs/step05_group_comparison.log
- logs/step06_regression.log
- logs/step07_sensitivity.log

### Plots (EMPTY until rq_plots runs)
- Plot source CSVs created in data/ folder:
  - data/step04_correlation_plot_data.csv (for scatter plot)
  - data/step05_group_plot_data.csv (for box plot comparison)

### Results (EMPTY until rq_results runs)
- results/summary.md will be created by rq_results

---

## Expected Data Formats

### Step-to-Step Transformations
1. **Step 0 -> Step 1:** Dependency validation -> Theta score extraction
2. **Step 1 -> Step 2:** Theta scores -> Strategy variable coding
3. **Step 2 -> Step 3:** Separate datasets -> Merged analysis dataset  
4. **Step 3 -> Steps 4-6:** Merged data feeds all primary analyses
5. **Steps 4-6 -> Step 7:** Analysis results -> Sensitivity and effect size summary

### Column Naming Conventions
- **UID:** Participant identifier (object type)
- **theta_all:** Omnibus memory performance (float64)
- **rehearsal_freq_mean:** Mean rehearsal frequency across tests (float64)
- **mnemonic_use_binary:** Binary mnemonic strategy use (int64: 0/1)
- **age:** Participant age in years (int64)
- **NART_score:** Cognitive ability proxy (float64)

### Data Type Constraints
- **UID:** Non-nullable string identifier
- **theta_all:** Nullable float, typically [-3, 3] range
- **rehearsal_freq_mean:** Non-nullable float, [1, 10] range
- **mnemonic_use_binary:** Non-nullable integer, {0, 1} values only
- **Statistical outputs:** Non-nullable float64 for coefficients, p-values, effect sizes

---

## Cross-RQ Dependencies

**Primary Dependency:** Ch5 5.1.1 (Omnibus Theta Scores)
- **Status Requirement:** rq_results: success in Ch5 5.1.1
- **File Required:** Participant theta_all scores (omnibus performance measure)
- **Primary Path:** results/ch5/5.1.1/data/step03_theta_scores.csv
- **Alternative Paths:** results/ch5/5.1.1/data/*theta*.{csv,txt}
- **Fallback Pattern:** results/ch5/5.1.1/data/*scores*.csv
- **Content Expected:** UID column + theta_all scores for 100 participants
- **Circuit Breaker:** If no valid theta file found, QUIT with error message

**Secondary Dependency:** master.xlsx STR Data
- **File Required:** data/cache/master.xlsx
- **Tag Patterns:** {UID}-RVR-T{N}-STR-X-TNK1- (rehearsal), {UID}-RVR-T{N}-STR-X-MNE1- (mnemonics)
- **Content Expected:** Strategy questionnaire responses for 4 tests per participant
- **Circuit Breaker:** If STR data missing for >50% participants, QUIT with warning

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution. This includes both substantive validation (data quality, value ranges) and methodological validation (assumption checking, effect size reasonableness).

### Validation Requirements By Step

#### Step 0: Validate Dependencies
- **4-Layer Validation:** File existence + Ch5 status + STR accessibility + log patterns
- **Critical Checks:** Dependency resolution before proceeding
- **Failure Action:** Quit immediately with dependency guidance

#### Step 1: Extract Theta Scores
- **4-Layer Validation:** File format + value ranges + data quality + log validation
- **Critical Checks:** N=100 participants, theta range [-4, 4], no missing data
- **Failure Action:** Quit with data quality diagnostics

#### Step 2: Code Strategy Variables  
- **4-Layer Validation:** Coding reliability + value ranges + data completeness + log validation
- **Critical Checks:** Inter-rater kappa >= 0.80, reasonable strategy distributions
- **Failure Action:** Refine coding if reliability insufficient

#### Step 3: Merge and Descriptives
- **4-Layer Validation:** Merge success + descriptive ranges + data quality + log validation
- **Critical Checks:** >= 90 participants merged, no missing analysis variables
- **Failure Action:** Quit if < 80 participants remain

#### Step 4: Correlation Analysis
- **4-Layer Validation:** Statistical results + assumption checks + CI validity + log validation  
- **Critical Checks:** Valid correlation range [-1, 1], bootstrap CI computed
- **Failure Action:** Report assumption violations, use robust methods

#### Step 5: Group Comparison
- **4-Layer Validation:** T-test results + group diagnostics + effect sizes + log validation
- **Critical Checks:** Both groups n >= 5, finite test statistics, valid Cohen's d
- **Failure Action:** Use robust methods if assumptions violated

#### Step 6: Hierarchical Regression
- **4-Layer Validation:** Model results + assumption diagnostics + VIF checks + log validation
- **Critical Checks:** Model convergence, VIF < 10, finite coefficients
- **Failure Action:** Report robust SEs if assumptions violated

#### Step 7: Sensitivity Analysis
- **4-Layer Validation:** Outlier detection + power analysis + effect stability + log validation
- **Critical Checks:** Outlier criteria applied, power calculated, effects stable
- **Failure Action:** Document limitations if substantial sensitivity

---

## Summary

**Total Steps:** 8 (Step 0: validation + Steps 1-7: analysis)
**Estimated Runtime:** 45-60 minutes
**Cross-RQ Dependencies:** Ch5 5.1.1 (theta_all scores) + master.xlsx (STR data)
**Primary Outputs:** Correlation analysis + group comparison + hierarchical regression with controls
**Validation Coverage:** 100% (all 8 steps have 4-layer validation requirements)

**Key Hypothesis:** Self-reported memory strategy use predicts REMEMVR performance, with small positive effects for rehearsal frequency (r ~ 0.18) and mnemonic use (Cohen's d ~ 0.3).

**Critical Methodological Notes:**
- Text coding reliability critical for mnemonic variable validity (kappa >= 0.80 required)
- Bootstrap confidence intervals for robust inference when normality violated
- Decision D068 dual p-value reporting applied throughout
- Multiple comparison corrections within strategy analysis family (2 tests)
- Power limitations acknowledged for small expected effects with N=100
- Cross-domain strategy effects may be attenuated in incidental encoding paradigm

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml  
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (2026-01-02): Initial plan created by rq_planner agent