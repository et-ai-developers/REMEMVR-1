# Analysis Plan: RQ 6.2.4 - Calibration by Accuracy Level

**Chapter:** 6
**Type:** Calibration
**Full ID:** 6.2.4
**Created:** 2025-12-06
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines whether high vs low baseline performers differ in calibration quality (metacognitive accuracy). Analysis approach: Merge calibration metrics from multiple prior RQs (6.2.1, 6.2.3, 6.1.1, Ch5 5.1.1), create accuracy tertiles (Low/Med/High performers), compare calibration quality across tertiles using ANOVA/Kruskal-Wallis, test Dunning-Kruger hypothesis (low performers overconfident), compute correlations between baseline accuracy and calibration metrics.

**Pipeline:** Cross-RQ derived data analysis (no IRT/LMM calibration in this RQ - uses pre-computed theta scores and calibration metrics)

**Steps:** 6 analysis steps (Step 0: merge derived data -> Step 1: create tertiles -> Step 2: tertile comparisons -> Step 3: Dunning-Kruger test -> Step 4: correlations -> Step 5: plot data preparation)

**Estimated Runtime:** Low (all inputs pre-computed, analysis is descriptive statistics and group comparisons, <10 minutes total)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni for multiple comparisons if applicable)
- Option B Architecture: Plot source CSVs created during analysis (Step 5), rq_plots generates PNG later

---

## Analysis Plan

### Step 0: Merge Calibration Metrics from Prior RQs

**Dependencies:** None (first step, but requires prior RQs complete)

**Complexity:** Low (<2 minutes - data merging only)

**Purpose:** Load and merge baseline accuracy (Ch5 5.1.1), baseline confidence (RQ 6.1.1), calibration scores (RQ 6.2.1), and gamma scores (RQ 6.2.3) into single dataset for N=100 participants.

**Input:**

**File 1:** results/ch5/5.1.1/data/step03_theta_scores.csv
**Source:** Ch5 5.1.1 (Accuracy Functional Form - omnibus "All" factor theta)
**Format:** CSV with columns:
- composite_ID (string, format: UID_test, e.g., P001_T1)
- theta_all (float, IRT ability estimate for omnibus accuracy)
- se_all (float, standard error)
**Filters:** Extract TEST = T1 (Day 0 baseline) only
**Expected Rows After Filter:** 100 (one per participant, baseline only)

**File 2:** results/ch6/6.1.1/data/step03_theta_confidence.csv
**Source:** RQ 6.1.1 (Confidence Model Selection - omnibus confidence theta)
**Format:** CSV with columns:
- composite_ID (string, format: UID_test)
- theta_confidence (float, IRT confidence estimate)
- se_confidence (float, standard error)
**Filters:** Extract TEST = T1 (Day 0 baseline) only
**Expected Rows After Filter:** 100

**File 3:** results/ch6/6.2.1/data/step02_calibration_scores.csv
**Source:** RQ 6.2.1 (Calibration Over Time)
**Format:** CSV with columns:
- composite_ID (string)
- calibration (float, theta_confidence - theta_accuracy standardized difference)
**Options:** Filter to TEST = T1 (baseline) OR compute mean calibration across all 4 tests (per concept.md flexibility)
**Expected Rows After Filter/Aggregation:** 100

**File 4:** results/ch6/6.2.3/data/step01_gamma_scores.csv
**Source:** RQ 6.2.3 (Resolution Over Time - Goodman-Kruskal gamma discrimination)
**Format:** CSV with columns:
- composite_ID (string)
- gamma (float, item-level confidence-accuracy discrimination)
**Options:** Filter to TEST = T1 (baseline) OR compute mean gamma across all 4 tests
**Expected Rows After Filter/Aggregation:** 100

**Processing:**

1. Load all 4 source files
2. Extract UID from composite_ID (parse format UID_test -> UID)
3. For Ch5 5.1.1 and RQ 6.1.1: Filter to TEST = T1 (Day 0) rows only
4. For RQ 6.2.1 and 6.2.3: EITHER filter to TEST = T1 OR compute mean per UID across all tests (document decision in log)
5. Merge all files on UID (left join: all participants must have all metrics)
6. Create final dataset with columns: UID, baseline_accuracy, baseline_confidence, mean_calibration, mean_gamma
7. Validate: 100 rows (all participants), no NaN values (missing data indicates source RQ issue)

**Output:**

**File 1:** data/step00_merged_metrics.csv
**Format:** CSV, one row per participant
**Columns:**
- UID (string, participant identifier, format: P###)
- baseline_accuracy (float, theta_all from Ch5 5.1.1 Day 0)
- baseline_confidence (float, theta_confidence from RQ 6.1.1 Day 0)
- mean_calibration (float, calibration from RQ 6.2.1 - baseline or mean)
- mean_gamma (float, gamma from RQ 6.2.3 - baseline or mean)
**Expected Rows:** 100 (one per participant)
**Expected Columns:** 5

**Validation Requirement:**

Validation tools MUST be used after data merging execution. Specific validation tools determined by rq_tools based on data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_merged_metrics.csv exists (exact path)
- Expected rows: 100 (all participants)
- Expected columns: 5 (UID, baseline_accuracy, baseline_confidence, mean_calibration, mean_gamma)
- Data types: string (UID), float (all metrics)

*Value Ranges:*
- baseline_accuracy in [-3, 3] (typical IRT theta range)
- baseline_confidence in [-3, 3] (typical IRT theta range)
- mean_calibration in [-6, 6] (difference of two thetas, can exceed [-3,3])
- mean_gamma in [-1, 1] (Goodman-Kruskal gamma bounds)

*Data Quality:*
- No NaN values tolerated (all participants must have all metrics)
- Expected N: Exactly 100 rows (no data loss acceptable)
- No duplicate UIDs (each participant appears once)
- Distribution check: baseline_accuracy approximately normal (visual inspection in log)

*Log Validation:*
- Required pattern: "Merged 100 participants successfully"
- Required pattern: "No missing values detected"
- Required pattern: "Source: Ch5 5.1.1 (100 rows), RQ 6.1.1 (100 rows), RQ 6.2.1 (N rows), RQ 6.2.3 (N rows)"
- Forbidden patterns: "ERROR", "NaN detected", "Merge failed"
- Acceptable warnings: None expected for merging

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 100 rows, found 87 - missing participants")
- Log failure to logs/step00_merge_metrics.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose (likely cause: source RQ incomplete or data loss in prior analysis)

---

### Step 1: Create Accuracy Tertiles

**Dependencies:** Step 0 (requires merged_metrics.csv)

**Complexity:** Low (<1 minute - tertile assignment only)

**Purpose:** Split participants into three equal groups (Low, Medium, High baseline performers) based on baseline_accuracy distribution for tertile comparison analysis.

**Input:**

**File:** data/step00_merged_metrics.csv
**Source:** Generated by Step 0
**Format:** CSV with 100 rows x 5 columns (UID, baseline_accuracy, baseline_confidence, mean_calibration, mean_gamma)

**Processing:**

1. Sort participants by baseline_accuracy (ascending)
2. Split into 3 approximately equal groups:
   - Low: Bottom 33% (approximately 33 participants)
   - Medium: Middle 34% (approximately 34 participants)
   - High: Top 33% (approximately 33 participants)
3. Assign tertile_label (Low/Med/High) to each participant
4. Compute tertile boundaries (min, max baseline_accuracy per tertile for interpretation)
5. Log tertile summary: N per tertile, accuracy range per tertile

**Output:**

**File 1:** data/step01_accuracy_tertiles.csv
**Format:** CSV, one row per participant
**Columns:**
- UID (string, participant identifier)
- baseline_accuracy (float, theta from Ch5 5.1.1)
- tertile_label (string, values: Low/Med/High)
- tertile_numeric (int, values: 1/2/3 for statistical tests)
**Expected Rows:** 100
**Expected Columns:** 4

**File 2:** data/step01_tertile_summary.txt
**Format:** Text report
**Contents:**
- Tertile boundaries (accuracy range per group)
- N per tertile (should be 33-34 each)
- Mean accuracy per tertile (sanity check: Low < Med < High)

**Validation Requirement:**

Validation tools MUST be used after tertile assignment execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_accuracy_tertiles.csv exists (exact path)
- data/step01_tertile_summary.txt exists (exact path)
- Expected rows (CSV): 100 (all participants assigned)
- Expected columns (CSV): 4 (UID, baseline_accuracy, tertile_label, tertile_numeric)
- Data types: string (UID, tertile_label), float (baseline_accuracy), int (tertile_numeric)

*Value Ranges:*
- baseline_accuracy in [-3, 3] (inherited from Step 0)
- tertile_label in {Low, Med, High} (categorical, no other values)
- tertile_numeric in {1, 2, 3} (ordinal, consecutive)

*Data Quality:*
- No NaN values tolerated (all participants assigned to tertile)
- Expected N: Exactly 100 rows
- Tertile distribution: 30-35 participants per tertile (approximately equal)
- No participants unassigned (all 100 must have tertile_label)
- Distribution check: Mean accuracy Low < Med < High (sanity check ordering)

*Log Validation:*
- Required pattern: "Tertile assignment complete: Low (N1), Med (N2), High (N3)"
- Required pattern: "Accuracy ranges: Low [-X to Y], Med [Y to Z], High [Z to W]"
- Forbidden patterns: "ERROR", "NaN in tertile assignment", "Unassigned participants"
- Acceptable warnings: "Tertile sizes unequal (33, 34, 33) due to divisibility" (expected)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Tertile Low has only 20 participants, expected ~33")
- Log failure to logs/step01_create_tertiles.log
- Quit script immediately
- g_debug invoked to diagnose (likely cause: data loss in Step 0 or tertile logic error)

---

### Step 2: Compare Calibration Metrics Across Tertiles

**Dependencies:** Steps 0, 1 (requires merged_metrics.csv + tertile assignments)

**Complexity:** Low (<2 minutes - ANOVA/Kruskal-Wallis tests)

**Purpose:** Test whether calibration quality (absolute calibration |calibration|, gamma) differs significantly across baseline accuracy tertiles (Low/Med/High performers).

**Input:**

**File 1:** data/step00_merged_metrics.csv
**Source:** Step 0
**Format:** 100 rows x 5 columns (UID, baseline_accuracy, baseline_confidence, mean_calibration, mean_gamma)

**File 2:** data/step01_accuracy_tertiles.csv
**Source:** Step 1
**Format:** 100 rows x 4 columns (UID, baseline_accuracy, tertile_label, tertile_numeric)

**Processing:**

1. Merge merged_metrics with tertiles on UID (inner join, 100 rows expected)
2. Compute absolute calibration: abs_calibration = |mean_calibration| (unsigned calibration error)
3. For EACH dependent variable (abs_calibration, mean_gamma):
   a. Test normality within tertiles (Shapiro-Wilk per group)
   b. Test homogeneity of variance (Levene's test)
   c. IF normality + homogeneity PASS: Use one-way ANOVA (parametric)
      ELSE: Use Kruskal-Wallis H-test (non-parametric)
4. Compute descriptive statistics per tertile:
   - Mean, SD, Median, IQR for abs_calibration and mean_gamma
5. Report F-statistic (ANOVA) or H-statistic (Kruskal-Wallis) with p-value
6. Decision D068 consideration: If significant (p < 0.05), proceed to post-hoc contrasts in separate analysis (not this step)

**Output:**

**File 1:** data/step02_tertile_comparison.csv
**Format:** CSV summarizing tertile comparison results
**Columns:**
- metric (string, values: abs_calibration, mean_gamma)
- test_used (string, values: ANOVA, Kruskal-Wallis)
- statistic (float, F or H value)
- p_value (float, significance)
- tertile (string, Low/Med/High - repeated rows for descriptives)
- mean (float, mean per tertile)
- sd (float, standard deviation per tertile)
- median (float, median per tertile)
- iqr (float, interquartile range per tertile)
**Expected Rows:** 2 metrics x 3 tertiles = 6 rows minimum (plus header rows for test results)

**File 2:** data/step02_normality_tests.csv
**Format:** CSV with normality test results
**Columns:**
- metric (string)
- tertile (string)
- shapiro_statistic (float)
- shapiro_p (float)
**Expected Rows:** 2 metrics x 3 tertiles = 6

**File 3:** data/step02_variance_tests.csv
**Format:** CSV with homogeneity of variance test results
**Columns:**
- metric (string)
- levene_statistic (float)
- levene_p (float)
**Expected Rows:** 2 (one per metric)

**Validation Requirement:**

Validation tools MUST be used after tertile comparison execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_tertile_comparison.csv exists (6+ rows x 9 columns)
- data/step02_normality_tests.csv exists (6 rows x 4 columns)
- data/step02_variance_tests.csv exists (2 rows x 3 columns)
- Data types: string (metric, test_used, tertile), float (all statistics and p-values)

*Value Ranges:*
- statistic > 0 (F and H statistics must be positive)
- p_value in [0, 1] (probability bounds)
- mean, sd, median, iqr all non-negative (absolute calibration unsigned)
- shapiro_statistic in [0, 1] (Shapiro-Wilk W bounds)
- shapiro_p in [0, 1]
- levene_statistic >= 0

*Data Quality:*
- No NaN values in test statistics (indicates test execution failure)
- Expected N: 6 rows in normality tests (2 metrics x 3 tertiles)
- Expected N: 2 rows in variance tests (2 metrics)
- Expected N: 6+ rows in tertile_comparison (3 tertiles x 2 metrics for descriptives)
- test_used in {ANOVA, Kruskal-Wallis} (no other test types)

*Log Validation:*
- Required pattern: "Tertile comparison complete: abs_calibration (test_type, p=X.XXX), mean_gamma (test_type, p=Y.YYY)"
- Required pattern: "Normality tests: [summary of Shapiro-Wilk results]"
- Required pattern: "Variance tests: [summary of Levene results]"
- Forbidden patterns: "ERROR", "Test failed", "NaN in test results"
- Acceptable warnings: "Normality violated for metric X, using Kruskal-Wallis" (expected)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "p_value = NaN for abs_calibration ANOVA")
- Log failure to logs/step02_tertile_comparison.log
- Quit script immediately
- g_debug invoked to diagnose (likely cause: insufficient data per tertile or test implementation error)

---

### Step 3: Test Dunning-Kruger Hypothesis (One-Sample t-Tests)

**Dependencies:** Steps 0, 1 (requires merged_metrics.csv + tertile assignments)

**Complexity:** Low (<1 minute - three one-sample t-tests)

**Purpose:** Test whether low performers exhibit overconfidence (Dunning-Kruger pattern: mean_calibration > 0) and whether high performers are accurately calibrated (mean_calibration near zero or negative).

**Input:**

**File 1:** data/step00_merged_metrics.csv (from Step 0)
**File 2:** data/step01_accuracy_tertiles.csv (from Step 1)

**Processing:**

1. Merge metrics with tertiles on UID
2. For EACH tertile (Low, Med, High):
   a. Extract mean_calibration values for that tertile
   b. Perform one-sample t-test against mu = 0 (H0: calibration = 0, no bias)
   c. Report: t-statistic, df, p-value (two-tailed), mean calibration, 95% CI
3. Interpret results:
   - Low tertile: Positive mean calibration with p < 0.05 supports Dunning-Kruger (overconfidence)
   - High tertile: Mean calibration near zero (not significantly different from 0) supports accurate calibration
4. Decision D068 note: Multiple comparisons (3 tertiles), consider Bonferroni correction (p_corrected = p_uncorrected x 3)

**Output:**

**File 1:** data/step03_dunning_kruger_test.csv
**Format:** CSV with one-sample t-test results
**Columns:**
- tertile (string, Low/Med/High)
- N (int, participants per tertile)
- mean_calibration (float, observed mean for tertile)
- sd_calibration (float, standard deviation)
- t_statistic (float, t-test statistic)
- df (int, degrees of freedom)
- p_uncorrected (float, uncorrected p-value)
- p_bonferroni (float, Bonferroni-corrected p-value = p_uncorrected x 3)
- CI_lower (float, 95% CI lower bound)
- CI_upper (float, 95% CI upper bound)
**Expected Rows:** 3 (one per tertile)

**Validation Requirement:**

Validation tools MUST be used after Dunning-Kruger test execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_dunning_kruger_test.csv exists (3 rows x 10 columns)
- Data types: string (tertile), int (N, df), float (all other columns)

*Value Ranges:*
- N in [30, 35] per tertile (approximately equal distribution from Step 1)
- mean_calibration in [-6, 6] (difference of two thetas)
- sd_calibration > 0 (standard deviation must be positive)
- t_statistic unrestricted (can be positive or negative)
- df = N - 1 (degrees of freedom check)
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1] (should be = p_uncorrected x 3, capped at 1.0)
- CI_lower < CI_upper (confidence interval ordering)

*Data Quality:*
- No NaN values tolerated (all tertiles must have valid t-test results)
- Expected N: Exactly 3 rows (Low, Med, High)
- No duplicate tertiles (each appears once)
- Distribution check: Low tertile mean_calibration expected positive (Dunning-Kruger hypothesis)

*Log Validation:*
- Required pattern: "Dunning-Kruger test complete: Low (mean=X, p=Y), Med (mean=A, p=B), High (mean=C, p=D)"
- Required pattern: "Bonferroni correction applied (alpha = 0.05 / 3 = 0.0167)"
- Forbidden patterns: "ERROR", "t-test failed", "NaN in results"
- Acceptable warnings: None expected for t-tests

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "p_bonferroni = NaN for Low tertile")
- Log failure to logs/step03_dunning_kruger_test.log
- Quit script immediately
- g_debug invoked to diagnose (likely cause: insufficient variance within tertile or test implementation error)

---

### Step 4: Compute Correlations (Baseline Accuracy vs Calibration Metrics)

**Dependencies:** Step 0 (requires merged_metrics.csv)

**Complexity:** Low (<1 minute - correlation tests)

**Purpose:** Test whether baseline accuracy correlates with calibration quality continuously (not just tertile differences): (1) baseline_accuracy vs |calibration|, (2) baseline_accuracy vs gamma.

**Input:**

**File:** data/step00_merged_metrics.csv (from Step 0)
**Format:** 100 rows x 5 columns (UID, baseline_accuracy, baseline_confidence, mean_calibration, mean_gamma)

**Processing:**

1. Compute abs_calibration = |mean_calibration| (unsigned calibration error)
2. For EACH correlation:
   a. Correlation 1: baseline_accuracy vs abs_calibration
      - Hypothesis: Negative correlation (higher accuracy -> lower calibration error)
   b. Correlation 2: baseline_accuracy vs mean_gamma
      - Hypothesis: Positive correlation (higher accuracy -> better discrimination)
3. For EACH correlation:
   a. Test normality (Shapiro-Wilk on both variables)
   b. IF normality PASS: Use Pearson correlation (parametric)
      ELSE: Use Spearman correlation (non-parametric)
   c. Report: r or rho, p-value, 95% CI (bootstrap if Spearman), N
4. Decision D068: Two comparisons, report BOTH uncorrected and Bonferroni p-values (p_corrected = p_uncorrected x 2)

**Output:**

**File 1:** data/step04_correlation.csv
**Format:** CSV with correlation results
**Columns:**
- comparison (string, values: "baseline_accuracy vs abs_calibration", "baseline_accuracy vs mean_gamma")
- method (string, values: Pearson, Spearman)
- r_or_rho (float, correlation coefficient)
- p_uncorrected (float, uncorrected p-value)
- p_bonferroni (float, Bonferroni-corrected p-value = p_uncorrected x 2)
- CI_lower (float, 95% CI lower bound)
- CI_upper (float, 95% CI upper bound)
- N (int, sample size = 100)
**Expected Rows:** 2 (one per correlation)

**File 2:** data/step04_normality_tests.csv
**Format:** CSV with normality test results for correlation variables
**Columns:**
- variable (string, values: baseline_accuracy, abs_calibration, mean_gamma)
- shapiro_statistic (float)
- shapiro_p (float)
**Expected Rows:** 3 (baseline_accuracy tested once, abs_calibration and mean_gamma each tested once)

**Validation Requirement:**

Validation tools MUST be used after correlation computation execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_correlation.csv exists (2 rows x 8 columns)
- data/step04_normality_tests.csv exists (3 rows x 3 columns)
- Data types: string (comparison, method, variable), float (r_or_rho, p-values, CI bounds, shapiro stats), int (N)

*Value Ranges:*
- r_or_rho in [-1, 1] (correlation coefficient bounds)
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1] (should be = p_uncorrected x 2, capped at 1.0)
- CI_lower in [-1, 1]
- CI_upper in [-1, 1]
- CI_lower < CI_upper (confidence interval ordering)
- N = 100 (all participants)
- shapiro_statistic in [0, 1] (Shapiro-Wilk W bounds)
- shapiro_p in [0, 1]

*Data Quality:*
- No NaN values tolerated (all correlations must compute successfully)
- Expected N: Exactly 2 rows in correlation.csv (two comparisons)
- Expected N: Exactly 3 rows in normality_tests.csv (three variables)
- method in {Pearson, Spearman} (no other correlation types)
- Distribution check: Expected negative r for baseline_accuracy vs abs_calibration (hypothesis)

*Log Validation:*
- Required pattern: "Correlation 1: baseline_accuracy vs abs_calibration (method, r=X.XX, p_uncorrected=Y.YYY, p_bonferroni=Z.ZZZ)"
- Required pattern: "Correlation 2: baseline_accuracy vs mean_gamma (method, rho=A.AA, p_uncorrected=B.BBB, p_bonferroni=C.CCC)"
- Required pattern: "Bonferroni correction applied (alpha = 0.05 / 2 = 0.025)"
- Forbidden patterns: "ERROR", "Correlation failed", "NaN in results"
- Acceptable warnings: "Normality violated for variable X, using Spearman" (expected)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "r_or_rho = NaN for baseline_accuracy vs abs_calibration")
- Log failure to logs/step04_correlation.log
- Quit script immediately
- g_debug invoked to diagnose (likely cause: insufficient variance or correlation implementation error)

---

### Step 5: Prepare Calibration by Accuracy Plot Data

**Dependencies:** Steps 0, 1, 2, 3, 4 (requires all prior analysis outputs)

**Complexity:** Low (<2 minutes - data aggregation for plotting)

**Purpose:** Create plot source CSV for visualizing calibration metrics (abs_calibration, gamma) by baseline accuracy with tertile groupings and correlation trends.

**Plot Description:** Two-panel plot showing (1) scatterplot of baseline_accuracy vs abs_calibration with tertile coloring and regression line, (2) scatterplot of baseline_accuracy vs mean_gamma with tertile coloring and regression line.

**Required Data Sources:**
- data/step00_merged_metrics.csv (baseline_accuracy, mean_calibration, mean_gamma)
- data/step01_accuracy_tertiles.csv (tertile_label for coloring)
- data/step04_correlation.csv (r/rho values for annotation)

**Processing:**

1. Merge merged_metrics with tertiles on UID
2. Compute abs_calibration = |mean_calibration|
3. Create plot source CSV with columns:
   - UID (string)
   - baseline_accuracy (float)
   - abs_calibration (float)
   - mean_gamma (float)
   - tertile_label (string, Low/Med/High)
   - tertile_color (string, hex color codes for plotting - Low=#D62728, Med=#FF7F0E, High=#2CA02C)
4. Add regression fit data (optional, can compute in rq_plots):
   - For each metric: baseline_accuracy range, predicted values from linear fit
5. Log: N=100 rows, tertile distribution confirmed

**Output:**

**File 1:** data/step05_calibration_by_accuracy_plot_data.csv
**Format:** CSV, plot source data for scatterplots with tertile grouping
**Columns:**
- UID (string, participant identifier)
- baseline_accuracy (float, x-axis variable)
- abs_calibration (float, y-axis variable for panel 1)
- mean_gamma (float, y-axis variable for panel 2)
- tertile_label (string, Low/Med/High for color grouping)
- tertile_color (string, hex color codes)
**Expected Rows:** 100 (one per participant)
**Expected Columns:** 6

**Note:** This CSV is read by rq_plots agent later. PNG output saved to plots/ folder by rq_plots, NOT by this analysis step.

**Validation Requirement:**

Validation tools MUST be used after plot data preparation execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_calibration_by_accuracy_plot_data.csv exists (exact path)
- Expected rows: 100 (all participants)
- Expected columns: 6 (UID, baseline_accuracy, abs_calibration, mean_gamma, tertile_label, tertile_color)
- Data types: string (UID, tertile_label, tertile_color), float (baseline_accuracy, abs_calibration, mean_gamma)

*Value Ranges:*
- baseline_accuracy in [-3, 3] (IRT theta range)
- abs_calibration in [0, 6] (unsigned difference, max = 2 x 3)
- mean_gamma in [-1, 1] (Goodman-Kruskal gamma bounds)
- tertile_label in {Low, Med, High} (categorical)
- tertile_color in {#D62728, #FF7F0E, #2CA02C} (specific hex codes for consistency)

*Data Quality:*
- No NaN values tolerated (all participants must have all columns)
- Expected N: Exactly 100 rows (no data loss)
- No duplicate UIDs (each participant appears once)
- Tertile distribution: 30-35 participants per tertile (approximately equal)
- Distribution check: All 3 tertile_labels present (Low, Med, High all represented)

*Log Validation:*
- Required pattern: "Plot data preparation complete: 100 rows created"
- Required pattern: "Tertiles represented: Low (N1), Med (N2), High (N3)"
- Required pattern: "All columns validated: UID, baseline_accuracy, abs_calibration, mean_gamma, tertile_label, tertile_color"
- Forbidden patterns: "ERROR", "NaN values detected", "Missing tertile"
- Acceptable warnings: None expected for plot data preparation

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 100 rows, found 87")
- Log failure to logs/step05_prepare_plot_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- g_debug invoked to diagnose root cause (likely: merge failure or missing data from prior steps)

**Plotting Function (rq_plots will call):** Two-panel scatterplot with tertile coloring and regression lines
- rq_plots agent maps this description to tools/plots.py functions
- Plot reads data/step05_calibration_by_accuracy_plot_data.csv (created by this step)
- No data aggregation in rq_plots (visualization only per Option B)
- PNG output saved to plots/calibration_by_accuracy.png by rq_plots

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs - intermediate and final)

- data/step00_merged_metrics.csv (from Step 0: merge derived data from 4 source RQs)
- data/step01_accuracy_tertiles.csv (from Step 1: tertile assignments)
- data/step01_tertile_summary.txt (from Step 1: tertile boundaries and N)
- data/step02_tertile_comparison.csv (from Step 2: ANOVA/Kruskal-Wallis results)
- data/step02_normality_tests.csv (from Step 2: Shapiro-Wilk tests)
- data/step02_variance_tests.csv (from Step 2: Levene tests)
- data/step03_dunning_kruger_test.csv (from Step 3: one-sample t-tests)
- data/step04_correlation.csv (from Step 4: Pearson/Spearman correlations)
- data/step04_normality_tests.csv (from Step 4: Shapiro-Wilk tests for correlation variables)
- data/step05_calibration_by_accuracy_plot_data.csv (from Step 5: plot source CSV)

### Logs (ONLY execution logs - .log files capturing stdout/stderr)

- logs/step00_merge_metrics.log
- logs/step01_create_tertiles.log
- logs/step02_tertile_comparison.log
- logs/step03_dunning_kruger_test.log
- logs/step04_correlation.log
- logs/step05_prepare_plot_data.log

### Plots (EMPTY until rq_plots runs)

- plots/calibration_by_accuracy.png (created by rq_plots, NOT analysis steps)

### Results (EMPTY until rq_results runs)

- results/summary.md (created by rq_results, NOT analysis steps)

---

## Expected Data Formats

### Step 0 Output: merged_metrics.csv

**Format:** Wide (one row per participant)
**Dimensions:** 100 rows x 5 columns
**Key Column:** UID (string, participant identifier)
**Metric Columns:**
- baseline_accuracy: theta_all from Ch5 5.1.1 Day 0 (float, range [-3, 3])
- baseline_confidence: theta_confidence from RQ 6.1.1 Day 0 (float, range [-3, 3])
- mean_calibration: calibration from RQ 6.2.1 (float, range [-6, 6])
- mean_gamma: gamma from RQ 6.2.3 (float, range [-1, 1])

**Null Handling:** No NaN values acceptable (all participants must have all metrics)

### Step 1 Output: accuracy_tertiles.csv

**Format:** Wide (one row per participant)
**Dimensions:** 100 rows x 4 columns
**Grouping Variable:** tertile_label (string, Low/Med/High)
**Numeric Grouping:** tertile_numeric (int, 1/2/3 for statistical tests)

### Step 2 Output: tertile_comparison.csv

**Format:** Mixed (test results + descriptives by tertile)
**Dimensions:** 6+ rows x 9 columns
**Test Results:** F or H statistic, p-value, test type
**Descriptives:** Mean, SD, Median, IQR per tertile per metric

### Step 3 Output: dunning_kruger_test.csv

**Format:** Wide (one row per tertile)
**Dimensions:** 3 rows x 10 columns
**Key Result:** mean_calibration per tertile, p_uncorrected, p_bonferroni
**Interpretation:** Low tertile mean_calibration > 0 with p < 0.05 supports Dunning-Kruger

### Step 4 Output: correlation.csv

**Format:** Wide (one row per correlation)
**Dimensions:** 2 rows x 8 columns
**Key Results:** r_or_rho, p_uncorrected, p_bonferroni, 95% CI
**Interpretation:** Negative r for baseline_accuracy vs abs_calibration supports hypothesis

### Step 5 Output: calibration_by_accuracy_plot_data.csv

**Format:** Wide (one row per participant)
**Dimensions:** 100 rows x 6 columns
**Plot Variables:**
- X-axis: baseline_accuracy (continuous)
- Y-axis Panel 1: abs_calibration (continuous)
- Y-axis Panel 2: mean_gamma (continuous)
- Color grouping: tertile_label (categorical)
- Color codes: tertile_color (hex strings)

---

## Cross-RQ Dependencies

### Dependency Type 2: DERIVED Data from Other RQs (Dependencies Exist)

**This RQ requires outputs from:**

1. **Ch5 5.1.1** (Accuracy Functional Form - General "All" Factor)
   - File: results/ch5/5.1.1/data/step03_theta_scores.csv
   - Used in: Step 0 (baseline accuracy for tertile grouping)
   - Filter: TEST = T1 (Day 0 baseline only)
   - Rationale: Baseline performance metric for defining Low/Med/High performers

2. **RQ 6.1.1** (Confidence Model Selection)
   - File: results/ch6/6.1.1/data/step03_theta_confidence.csv
   - Used in: Step 0 (baseline confidence for descriptive purposes)
   - Filter: TEST = T1 (Day 0 baseline only)
   - Rationale: Confidence metric paired with accuracy for calibration analysis

3. **RQ 6.2.1** (Calibration Over Time)
   - File: results/ch6/6.2.1/data/step02_calibration_scores.csv
   - Used in: Step 0 (calibration metric = confidence - accuracy)
   - Filter: TEST = T1 OR compute mean across all tests
   - Rationale: Primary calibration outcome variable

4. **RQ 6.2.3** (Resolution Over Time - Gamma)
   - File: results/ch6/6.2.3/data/step01_gamma_scores.csv
   - Used in: Step 0 (gamma discrimination metric)
   - Filter: TEST = T1 OR compute mean across all tests
   - Rationale: Secondary calibration quality metric (item-level discrimination)

**Execution Order Constraint:**
1. Ch5 5.1.1 must complete (provides baseline_accuracy)
2. RQ 6.1.1 must complete (provides baseline_confidence)
3. RQ 6.2.1 must complete (provides calibration scores)
4. RQ 6.2.3 must complete (provides gamma scores)
5. This RQ (6.2.4) executes AFTER all 4 dependencies complete

**Data Source Boundaries (Per Specification 5.1.6):**
- **RAW data:** None (this RQ uses DERIVED data only)
- **DERIVED data:** All 4 source RQs listed above (theta scores, calibration, gamma)
- **Scope:** This RQ does NOT re-compute calibration or gamma (uses pre-computed metrics from prior RQs)

**Validation:**
- Step 0: Check all 4 source files exist (circuit breaker: FILE_MISSING if any absent)
- If any file missing -> quit with error -> user must execute dependency RQs first
- Log source file paths and row counts during merge

---

## Validation Requirements

**CRITICAL MANDATE:**

Every analysis step in this plan MUST use validation tools after analysis tool execution.

This is not optional. This is the core architectural principle preventing cascading failures observed in v3.0 (where analysis errors propagated undetected through 5+ downstream steps before discovery).

**Exact Specification Requirement:**

> "Validation tools MUST be used after analysis tool execution"

**Implementation:**
- rq_tools (Step 11 workflow) will read tool_inventory.md validation tools section
- rq_tools will specify BOTH analysis tool + validation tool per step in 3_tools.yaml
- rq_analysis (Step 12 workflow) will embed validation tool call AFTER analysis tool call in 4_analysis.yaml
- g_code (Step 14 workflow) will generate stepNN_name.py scripts with validation function calls
- bash execution (Step 14 workflow) will run analysis -> validation -> error on validation failure

**Downstream Agent Requirements:**
- **rq_tools:** MUST specify validation tool for EVERY analysis step (no exceptions)
- **rq_analysis:** MUST embed validation tool call for EVERY analysis step (no exceptions)
- **g_code:** MUST generate code with validation function calls (no exceptions)
- **rq_inspect:** MUST verify validation ran successfully (checks logs/stepNN_name.log for validation output)

### Validation Requirements By Step

#### Step 0: Merge Calibration Metrics from Prior RQs

**Analysis Tool:** (determined by rq_tools - likely pandas merge operations)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure)

**What Validation Checks:**
- Output file exists (data/step00_merged_metrics.csv)
- Expected column count (5 columns: UID, baseline_accuracy, baseline_confidence, mean_calibration, mean_gamma)
- Expected row count (100 rows: all participants)
- No unexpected NaN patterns (0% NaN acceptable for complete case analysis)
- UID format correct (P### pattern)
- Value ranges: baseline_accuracy in [-3, 3], baseline_confidence in [-3, 3], mean_calibration in [-6, 6], mean_gamma in [-1, 1]

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 100 rows, found 87")
- Log failure to logs/step00_merge_metrics.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked by master to diagnose root cause

---

#### Step 1: Create Accuracy Tertiles

**Analysis Tool:** (determined by rq_tools - likely pandas quantile-based grouping)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure)

**What Validation Checks:**
- Output files exist (data/step01_accuracy_tertiles.csv, data/step01_tertile_summary.txt)
- Expected column count (4 columns: UID, baseline_accuracy, tertile_label, tertile_numeric)
- Expected row count (100 rows)
- Tertile distribution: 30-35 participants per tertile (approximately equal)
- No NaN values (all participants assigned)
- tertile_label in {Low, Med, High} (categorical validation)
- tertile_numeric in {1, 2, 3} (ordinal validation)
- Mean accuracy ordering: Low < Med < High (sanity check)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Tertile Low has only 20 participants, expected ~33")
- Log failure to logs/step01_create_tertiles.log
- Quit script immediately
- g_debug invoked to diagnose (likely: data loss or tertile logic error)

---

#### Step 2: Compare Calibration Metrics Across Tertiles

**Analysis Tool:** (determined by rq_tools - likely scipy ANOVA/Kruskal-Wallis)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_hypothesis_test_dual_pvalues per D068)

**What Validation Checks:**
- Output files exist (data/step02_tertile_comparison.csv, data/step02_normality_tests.csv, data/step02_variance_tests.csv)
- Test statistics non-NaN (F or H must compute successfully)
- p-values in [0, 1]
- Descriptives per tertile: mean, sd, median, iqr all non-negative (for abs_calibration)
- Normality test results: shapiro_statistic in [0, 1], shapiro_p in [0, 1]
- Variance test results: levene_statistic >= 0, levene_p in [0, 1]

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "p_value = NaN for abs_calibration ANOVA")
- Log failure to logs/step02_tertile_comparison.log
- Quit script immediately
- g_debug invoked to diagnose (likely: insufficient variance or test implementation error)

---

#### Step 3: Test Dunning-Kruger Hypothesis (One-Sample t-Tests)

**Analysis Tool:** (determined by rq_tools - likely scipy one-sample t-test)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_hypothesis_test_dual_pvalues per D068)

**What Validation Checks:**
- Output file exists (data/step03_dunning_kruger_test.csv)
- Expected rows: 3 (Low, Med, High tertiles)
- Expected columns: 10 (tertile, N, mean_calibration, sd_calibration, t_statistic, df, p_uncorrected, p_bonferroni, CI_lower, CI_upper)
- N per tertile in [30, 35]
- df = N - 1 (degrees of freedom validation)
- p_uncorrected in [0, 1]
- p_bonferroni = p_uncorrected x 3 (capped at 1.0) per D068
- CI_lower < CI_upper

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "p_bonferroni = NaN for Low tertile")
- Log failure to logs/step03_dunning_kruger_test.log
- Quit script immediately
- g_debug invoked to diagnose (likely: t-test failure or insufficient variance)

---

#### Step 4: Compute Correlations

**Analysis Tool:** (determined by rq_tools - likely scipy Pearson/Spearman correlation)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_correlation_test_d068 per D068)

**What Validation Checks:**
- Output files exist (data/step04_correlation.csv, data/step04_normality_tests.csv)
- Expected rows: 2 correlations in correlation.csv, 3 variables in normality_tests.csv
- r_or_rho in [-1, 1]
- p_uncorrected in [0, 1]
- p_bonferroni = p_uncorrected x 2 (capped at 1.0) per D068
- CI_lower < CI_upper
- N = 100 (all participants)
- method in {Pearson, Spearman}

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "r_or_rho = NaN for baseline_accuracy vs abs_calibration")
- Log failure to logs/step04_correlation.log
- Quit script immediately
- g_debug invoked to diagnose (likely: correlation implementation error)

---

#### Step 5: Prepare Calibration by Accuracy Plot Data

**Analysis Tool:** (determined by rq_tools - likely pandas merge + compute)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_plot_data_completeness)

**What Validation Checks:**
- Output file exists (data/step05_calibration_by_accuracy_plot_data.csv)
- Expected rows: 100 (all participants)
- Expected columns: 6 (UID, baseline_accuracy, abs_calibration, mean_gamma, tertile_label, tertile_color)
- No NaN values (all participants complete)
- tertile_label in {Low, Med, High} (all 3 represented)
- tertile_color in {#D62728, #FF7F0E, #2CA02C} (specific hex codes)
- Value ranges: baseline_accuracy in [-3, 3], abs_calibration in [0, 6], mean_gamma in [-1, 1]
- Tertile distribution: 30-35 participants per tertile

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Expected 100 rows, found 87")
- Log failure to logs/step05_prepare_plot_data.log
- Quit script immediately
- g_debug invoked to diagnose (likely: merge failure or missing tertile labels)

---

## Summary

**Total Steps:** 6 (Step 0: merge -> Step 5: plot data preparation)

**Estimated Runtime:** Low (<10 minutes total - all inputs pre-computed, analysis is descriptive/inferential statistics)

**Cross-RQ Dependencies:** 4 source RQs (Ch5 5.1.1, RQ 6.1.1, RQ 6.2.1, RQ 6.2.3) - all must complete before this RQ executes

**Primary Outputs:**
- data/step00_merged_metrics.csv (100 participants x 5 metrics)
- data/step01_accuracy_tertiles.csv (tertile assignments)
- data/step02_tertile_comparison.csv (ANOVA/Kruskal-Wallis results)
- data/step03_dunning_kruger_test.csv (one-sample t-tests)
- data/step04_correlation.csv (Pearson/Spearman correlations)
- data/step05_calibration_by_accuracy_plot_data.csv (plot source CSV)

**Validation Coverage:** 100% (all 6 steps have validation requirements with 4-layer substance criteria)

**Key Hypotheses Tested:**
1. High performers better calibrated than low performers (tertile comparison)
2. Low performers exhibit Dunning-Kruger overconfidence (one-sample t-test)
3. Baseline accuracy negatively correlates with calibration error (correlation)
4. Baseline accuracy positively correlates with gamma discrimination (correlation)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent for RQ 6.2.4
