# Analysis Plan: RQ 6.2.3 - Resolution Over Time

**Research Question:** 6.2.3
**Created:** 2025-12-06
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines metacognitive resolution (the ability to discriminate remembered from forgotten items) across a 6-day retention interval using Goodman-Kruskal gamma correlation between confidence and accuracy. The analysis uses item-level data from interactive paradigms (IFR, ICR, IRE) across all memory domains to test whether discrimination ability declines as memory fades.

**Pipeline:** Item-level correlational analysis (gamma computation) followed by Linear Mixed Model (LMM) trajectory analysis

**Steps:** 7 total analysis steps (Step 0: extraction + Steps 1-6: analysis + plot data preparation)

**Estimated Runtime:** Medium (Steps 0-1: Low complexity, Step 2: Medium complexity LMM, Steps 3-6: Low complexity)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni for multiple comparisons)
- Decision D070: TSVR as time variable (actual hours, not nominal days)

---

## Analysis Plan

This RQ requires 7 steps:

### Step 0: Extract Item-Level Data

**Dependencies:** None (first step)
**Complexity:** Low (data extraction only, <5 min)

**Purpose:** Extract item-level response data with paired accuracy (TQ_* tags) and confidence (TC_* tags) from interactive paradigms.

**Input:**

**File:** data/cache/dfData.csv (project-level data source)

**Required Columns:**
- `UID` (string, participant identifier)
- `TEST` (string, test session: T1, T2, T3, T4)
- `TQ_*` tags (dichotomous accuracy: 0 = incorrect, 1 = correct)
- `TC_*` tags (5-level confidence: 0, 0.25, 0.5, 0.75, 1.0)

**Filters:**
- Paradigm codes: Interactive paradigms only (IFR, ICR, IRE)
- Exclude: RFR (Room Free Recall), TCR (Timed Cued Recall), RRE (Room Recognition) - no confidence judgments
- All memory domains included (-N-, -L-/-U-/-D-, -O-)

**Expected Data Volume:**
- Approximately 68 items per participant per test session
- 100 participants x 4 tests x 68 items = 27,200 item-level responses

**Processing:**

1. Read dfData.csv
2. Filter to interactive paradigm items (IFR, ICR, IRE only)
3. Extract TQ_* and TC_* tag pairs for each item
4. Create long-format data: one row per item-level response
5. Columns: UID, TEST, ITEM, Accuracy (from TQ_*), Confidence (from TC_*)
6. Exclude rows where either Accuracy or Confidence is missing

**Output:**

**File:** data/step00_item_level.csv
**Format:** CSV, long format (one row per item-level response)
**Columns:**
  - `UID` (string, participant identifier, e.g., P001)
  - `TEST` (string, test session: T1, T2, T3, T4)
  - `ITEM` (string, item identifier from tag system)
  - `Accuracy` (int, values: 0 or 1)
  - `Confidence` (float, values: 0, 0.25, 0.5, 0.75, 1.0)
**Expected Rows:** Approximately 27,200 (68 items x 100 participants x 4 tests)

**Validation Requirement:**
Validation tools MUST be used after data extraction tool execution. Specific validation tools will be determined by rq_tools based on extraction type. The rq_analysis agent will embed validation tool calls after the extraction tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_item_level.csv exists (exact path)
- Expected rows: 25,000-29,000 (approximately 27,200, some missing data acceptable)
- Expected columns: 5 (UID, TEST, ITEM, Accuracy, Confidence)
- Data types: UID (string), TEST (string), ITEM (string), Accuracy (int64), Confidence (float64)

*Value Ranges:*
- Accuracy in {0, 1} (dichotomous)
- Confidence in {0, 0.25, 0.5, 0.75, 1.0} (5-level ordinal)
- UID format: P### (3-digit participant ID with leading zeros)
- TEST in {T1, T2, T3, T4}

*Data Quality:*
- No NaN values in Accuracy or Confidence columns (filtering during extraction)
- All 100 participants represented (UID count = 100)
- All 4 test sessions represented (TEST count = 4)
- Expected items per participant per test: 60-75 (approximately 68, some missing acceptable)

*Log Validation:*
- Required pattern: "Extracted item-level data: [N] rows"
- Required pattern: "Participants: 100, Tests: 4"
- Forbidden patterns: "ERROR", "No TQ_* tags found", "No TC_* tags found"
- Acceptable warnings: "Missing confidence for item X (excluded from analysis)"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected Accuracy in {0, 1}, found value 2")
- Log failure to logs/step00_extract_item_level.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause

---

### Step 1: Compute Goodman-Kruskal Gamma Per Participant-Timepoint

**Dependencies:** Step 0 (requires item-level data)
**Complexity:** Low (correlation computation, <5 min)

**Purpose:** Compute resolution (Goodman-Kruskal gamma) for each participant at each timepoint, measuring ability to discriminate correct from incorrect responses based on confidence.

**Input:**

**File:** data/step00_item_level.csv
**Source:** Generated by Step 0
**Format:** CSV, long format
**Columns:** UID, TEST, ITEM, Accuracy, Confidence
**Expected Rows:** Approximately 27,200

**Processing:**

1. Group data by UID and TEST (participant-timepoint combinations)
2. For each group, compute Goodman-Kruskal gamma:
   - Gamma = (Nc - Nd) / (Nc + Nd)
   - Nc = number of concordant pairs (higher confidence for correct vs incorrect)
   - Nd = number of discordant pairs (lower confidence for correct vs incorrect)
3. Handle edge cases:
   - If all responses same accuracy OR all same confidence: gamma undefined (NaN)
   - If Nc + Nd = 0 (no pairs to compare): gamma = 0
4. Create output with one row per participant-timepoint

**Output:**

**File:** data/step01_gamma_scores.csv
**Format:** CSV, one row per participant-timepoint
**Columns:**
  - `UID` (string, participant identifier)
  - `TEST` (string, test session)
  - `gamma` (float, Goodman-Kruskal gamma coefficient)
  - `n_items` (int, number of items used in computation)
**Expected Rows:** 400 (100 participants x 4 tests)

**Validation Requirement:**
Validation tools MUST be used after gamma computation tool execution. Specific validation tools will be determined by rq_tools based on correlational analysis type. The rq_analysis agent will embed validation tool calls after the gamma computation tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_gamma_scores.csv exists (exact path)
- Expected rows: 400 (100 participants x 4 tests)
- Expected columns: 4 (UID, TEST, gamma, n_items)
- Data types: UID (string), TEST (string), gamma (float64), n_items (int64)

*Value Ranges:*
- gamma in [-1, 1] (correlation coefficient bounds)
- n_items in [50, 80] (expected items per participant per test, approximately 68)
- Expected gamma range: [0.3, 0.9] (typical resolution values, <0 suggests coding error)

*Data Quality:*
- NaN gamma values acceptable if <5% of total (participants with no variance in accuracy/confidence)
- All 100 participants present (UID count = 100)
- All 4 test sessions present (TEST count = 4)
- n_items > 0 for all rows (must have data to compute gamma)

*Log Validation:*
- Required pattern: "Computed gamma for 400 participant-timepoints"
- Required pattern: "Mean gamma: [value], SD: [value]"
- Forbidden patterns: "ERROR", "Division by zero", "All gamma values NaN"
- Acceptable warnings: "Gamma undefined for [UID] at [TEST] due to no variance"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "gamma = 1.5 exceeds valid range [-1, 1]")
- Log failure to logs/step01_compute_gamma.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose root cause

---

### Step 2: Fit Linear Mixed Model to Gamma Scores

**Dependencies:** Step 1 (requires gamma scores)
**Complexity:** Medium (LMM fitting with random effects, 5-15 min)

**Purpose:** Model gamma trajectory over time using TSVR as time variable to test whether resolution declines across retention interval.

**Input:**

**File 1:** data/step01_gamma_scores.csv
**Source:** Generated by Step 1
**Format:** CSV, one row per participant-timepoint
**Columns:** UID, TEST, gamma, n_items
**Expected Rows:** 400

**File 2:** data/cache/dfData.csv (TSVR lookup)
**Source:** Project-level data
**Columns:** UID, TEST, TSVR_hours (time since encoding in hours)

**Processing:**

1. Merge gamma_scores with TSVR_hours on UID and TEST (Decision D070)
2. Convert TEST to numeric for mapping: T1=0, T2=1, T3=3, T4=6 (nominal days)
3. Transform TSVR_hours to days: TSVR_days = TSVR_hours / 24
4. Consider time transformations:
   - Linear: TSVR_days
   - Logarithmic: log(TSVR_days + 1) to handle Day 0
5. Fit LMM: gamma ~ TSVR_days + (TSVR_days | UID)
   - Fixed effect: Time (TSVR_days)
   - Random effects: Random intercepts and slopes by participant
   - Estimation: REML = True
6. Extract Time coefficient, SE, t-statistic, p-value
7. Test null hypothesis: Time coefficient = 0 (no change in resolution over time)

**Output:**

**File 1:** data/step02_gamma_lmm_input.csv
**Format:** CSV, long format for LMM
**Columns:**
  - `UID` (string)
  - `TEST` (string)
  - `gamma` (float)
  - `n_items` (int)
  - `TSVR_hours` (float, Decision D070)
  - `TSVR_days` (float, derived: TSVR_hours / 24)
**Expected Rows:** 400

**File 2:** data/step02_gamma_lmm_summary.txt
**Format:** Plain text LMM summary
**Content:** Model formula, fixed effects, random effects, AIC, BIC, log-likelihood

**Validation Requirement:**
Validation tools MUST be used after LMM fitting tool execution. Specific validation tools will be determined by rq_tools based on LMM analysis type. The rq_analysis agent will embed validation tool calls after the LMM fitting tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_gamma_lmm_input.csv exists (400 rows, 6 columns)
- data/step02_gamma_lmm_summary.txt exists (non-empty text file)

*Value Ranges:*
- TSVR_hours in [0, 168] (0 = encoding, 168 = 1 week max)
- TSVR_days in [0, 7] (derived from TSVR_hours)
- gamma in [-1, 1] (same as Step 1 output)

*Data Quality:*
- No NaN in TSVR_hours or TSVR_days (all participants have timing data)
- All 400 rows from Step 1 present after merge (no data loss)
- TSVR_days monotonic per participant (T1 < T2 < T3 < T4 for each UID)

*Log Validation:*
- Required pattern: "Model converged: True"
- Required pattern: "Fixed effects: TSVR_days coefficient = [value]"
- Required pattern: "Random effects variance > 0"
- Forbidden patterns: "ERROR", "Convergence failed", "Singular fit"
- Acceptable warnings: "Optimizer changed algorithm" (common in LMM)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "LMM did not converge after 200 iterations")
- Log failure to logs/step02_fit_gamma_lmm.log
- Quit script immediately (do NOT proceed to Step 3)
- g_debug invoked to diagnose root cause

---

### Step 3: Extract Time Effect Statistics

**Dependencies:** Step 2 (requires fitted LMM)
**Complexity:** Low (coefficient extraction, <2 min)

**Purpose:** Extract Time effect (TSVR_days coefficient) with dual p-values per Decision D068.

**Input:**

**File:** data/step02_gamma_lmm_summary.txt
**Source:** Generated by Step 2
**Content:** Fitted LMM results

**Processing:**

1. Parse LMM summary to extract Time coefficient
2. Extract: coefficient estimate, standard error, t-statistic, p-value
3. Compute Bonferroni-corrected p-value (Decision D068):
   - If testing single time transformation: no correction needed (1 test)
   - If testing multiple transformations (linear + log): Bonferroni correction p_corrected = p_uncorrected x 2
4. Create results table with BOTH uncorrected and corrected p-values

**Output:**

**File:** data/step03_time_effect.csv
**Format:** CSV, one row per time transformation tested
**Columns:**
  - `time_variable` (string, e.g., "TSVR_days")
  - `coefficient` (float, beta estimate)
  - `se` (float, standard error)
  - `t_statistic` (float, t-value)
  - `p_uncorrected` (float, p-value without correction)
  - `p_bonferroni` (float, Bonferroni-corrected p-value per Decision D068)
**Expected Rows:** 1 (testing TSVR_days linear transformation)

**Validation Requirement:**
Validation tools MUST be used after coefficient extraction tool execution. Specific validation tools will be determined by rq_tools based on statistical extraction type. The rq_analysis agent will embed validation tool calls after the extraction tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_time_effect.csv exists (exact path)
- Expected rows: 1 (single time transformation)
- Expected columns: 6 (time_variable, coefficient, se, t_statistic, p_uncorrected, p_bonferroni)
- Data types: time_variable (string), coefficient (float64), se (float64), t_statistic (float64), p_uncorrected (float64), p_bonferroni (float64)

*Value Ranges:*
- coefficient in [-2, 2] (typical LMM effect size range)
- se > 0 (standard error must be positive)
- t_statistic in [-10, 10] (extreme t-values rare)
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1]
- p_bonferroni >= p_uncorrected (correction cannot lower p-value)

*Data Quality:*
- No NaN values (all statistics must be computed)
- Dual p-values present (Decision D068 requirement)
- time_variable = "TSVR_days" (correct time variable used)

*Log Validation:*
- Required pattern: "Time effect extracted: coefficient = [value], p = [value]"
- Required pattern: "Dual p-values reported: uncorrected = [value], Bonferroni = [value]"
- Forbidden patterns: "ERROR", "Failed to extract coefficient"
- Acceptable warnings: None expected for coefficient extraction

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "p_bonferroni < p_uncorrected violates Decision D068")
- Log failure to logs/step03_extract_time_effect.log
- Quit script immediately (do NOT proceed to Step 4)
- g_debug invoked to diagnose root cause

---

### Step 4: Compute Mean Gamma by Timepoint

**Dependencies:** Step 1 (requires gamma scores)
**Complexity:** Low (descriptive statistics, <2 min)

**Purpose:** Compute descriptive statistics (mean, SD, 95% CI) for gamma at each timepoint to track trajectory pattern.

**Input:**

**File:** data/step01_gamma_scores.csv
**Source:** Generated by Step 1
**Format:** CSV, one row per participant-timepoint
**Columns:** UID, TEST, gamma, n_items
**Expected Rows:** 400

**Processing:**

1. Group data by TEST (T1, T2, T3, T4)
2. For each test session, compute:
   - Mean gamma
   - Standard deviation
   - 95% confidence interval (CI_lower, CI_upper) using t-distribution
   - Sample size N
3. Create summary table with one row per timepoint

**Output:**

**File:** data/step04_mean_gamma.csv
**Format:** CSV, one row per timepoint
**Columns:**
  - `TEST` (string, test session: T1, T2, T3, T4)
  - `mean_gamma` (float, mean resolution)
  - `sd_gamma` (float, standard deviation)
  - `CI_lower` (float, lower 95% confidence bound)
  - `CI_upper` (float, upper 95% confidence bound)
  - `N` (int, sample size per timepoint)
**Expected Rows:** 4 (one per test session)

**Validation Requirement:**
Validation tools MUST be used after descriptive statistics tool execution. Specific validation tools will be determined by rq_tools based on summary statistics type. The rq_analysis agent will embed validation tool calls after the statistics tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_mean_gamma.csv exists (exact path)
- Expected rows: 4 (one per test session)
- Expected columns: 6 (TEST, mean_gamma, sd_gamma, CI_lower, CI_upper, N)
- Data types: TEST (string), mean_gamma (float64), sd_gamma (float64), CI_lower (float64), CI_upper (float64), N (int64)

*Value Ranges:*
- mean_gamma in [0.3, 0.9] (typical resolution range, negative values suggest error)
- sd_gamma in [0.05, 0.3] (typical SD for gamma)
- CI_lower in [0, 1], CI_upper in [0, 1]
- CI_upper > CI_lower for all rows
- N = 100 (all participants present at each timepoint, or 95-100 acceptable)

*Data Quality:*
- No NaN values (all statistics must be computed)
- All 4 test sessions present (TEST in {T1, T2, T3, T4})
- Confidence intervals non-overlapping or overlapping (depends on effect size)

*Log Validation:*
- Required pattern: "Computed mean gamma for 4 timepoints"
- Required pattern: "T1 mean = [value], T4 mean = [value]"
- Forbidden patterns: "ERROR", "NaN mean gamma"
- Acceptable warnings: None expected for descriptive statistics

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "CI_upper < CI_lower at T2")
- Log failure to logs/step04_compute_mean_gamma.log
- Quit script immediately (do NOT proceed to Step 5)
- g_debug invoked to diagnose root cause

---

### Step 5: Test Gamma > 0.50 Threshold at Each Timepoint

**Dependencies:** Step 4 (requires mean gamma by timepoint)
**Complexity:** Low (one-sample t-tests, <2 min)

**Purpose:** Test whether gamma exceeds the 0.50 threshold (acceptable discrimination ability) at each timepoint using one-sample t-tests.

**Input:**

**File:** data/step01_gamma_scores.csv
**Source:** Generated by Step 1
**Format:** CSV, one row per participant-timepoint
**Columns:** UID, TEST, gamma, n_items
**Expected Rows:** 400

**Processing:**

1. For each TEST (T1, T2, T3, T4):
   - Extract gamma values for that timepoint
   - Conduct one-sample t-test: H0: mean(gamma) = 0.50 vs H1: mean(gamma) > 0.50 (one-tailed)
   - Extract: t-statistic, degrees of freedom, p-value
2. Apply Bonferroni correction for 4 tests: p_corrected = p_uncorrected x 4 (Decision D068)
3. Create results table with dual p-values per timepoint

**Output:**

**File:** data/step05_gamma_threshold_tests.csv
**Format:** CSV, one row per timepoint
**Columns:**
  - `TEST` (string, test session)
  - `mean_gamma` (float, observed mean)
  - `threshold` (float, fixed at 0.50)
  - `t_statistic` (float, t-value)
  - `df` (int, degrees of freedom)
  - `p_uncorrected` (float, p-value without correction)
  - `p_bonferroni` (float, Bonferroni-corrected p-value, Decision D068)
**Expected Rows:** 4 (one per test session)

**Validation Requirement:**
Validation tools MUST be used after hypothesis testing tool execution. Specific validation tools will be determined by rq_tools based on statistical testing type. The rq_analysis agent will embed validation tool calls after the testing tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_gamma_threshold_tests.csv exists (exact path)
- Expected rows: 4 (one per test session)
- Expected columns: 7 (TEST, mean_gamma, threshold, t_statistic, df, p_uncorrected, p_bonferroni)
- Data types: TEST (string), mean_gamma (float64), threshold (float64), t_statistic (float64), df (int64), p_uncorrected (float64), p_bonferroni (float64)

*Value Ranges:*
- mean_gamma in [0.3, 0.9] (same as Step 4)
- threshold = 0.50 (fixed threshold value)
- t_statistic in [-10, 10] (typical range)
- df = 99 (100 participants - 1, or 94-99 acceptable if some missing data)
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1]
- p_bonferroni = p_uncorrected x 4 (Bonferroni correction for 4 tests)

*Data Quality:*
- No NaN values (all statistics must be computed)
- All 4 test sessions present
- Dual p-values present (Decision D068 requirement)
- threshold constant at 0.50 for all rows

*Log Validation:*
- Required pattern: "Threshold tests complete: 4 timepoints tested"
- Required pattern: "All timepoints gamma > 0.50" OR "Timepoint [X] gamma < 0.50"
- Forbidden patterns: "ERROR", "t-test failed"
- Acceptable warnings: None expected for t-tests

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "p_bonferroni != p_uncorrected x 4")
- Log failure to logs/step05_test_gamma_threshold.log
- Quit script immediately (do NOT proceed to Step 6)
- g_debug invoked to diagnose root cause

---

### Step 6: Prepare Plot Data for Resolution Trajectory Visualization

**Dependencies:** Steps 2, 4 (requires LMM model predictions and observed means)
**Complexity:** Low (data aggregation for plotting, <2 min)

**Purpose:** Aggregate analysis outputs into plot source CSV for resolution trajectory visualization.

**Input:**

**File 1:** data/step04_mean_gamma.csv
**Source:** Generated by Step 4
**Columns:** TEST, mean_gamma, sd_gamma, CI_lower, CI_upper, N

**File 2:** data/step02_gamma_lmm_input.csv
**Source:** Generated by Step 2
**Columns:** UID, TEST, gamma, TSVR_hours, TSVR_days

**File 3:** data/step02_gamma_lmm_summary.txt (for extracting model-predicted trajectory)
**Source:** Generated by Step 2

**Processing:**

1. Extract observed means from step04_mean_gamma.csv
2. Map TEST to TSVR_days nominal values: T1=0, T2=1, T3=3, T4=6
3. Extract model-predicted trajectory from LMM:
   - Use fixed effects coefficients (Intercept + TSVR_days x Time)
   - Generate predicted gamma for each nominal day: 0, 1, 3, 6
4. Merge observed means with model predictions
5. Create plot source CSV with columns: time (days), observed_mean, CI_lower, CI_upper, predicted_mean

**Output:**

**File:** data/step06_resolution_trajectory_data.csv
**Format:** CSV, plot source data
**Columns:**
  - `time` (float, TSVR_days: 0, 1, 3, 6)
  - `observed_mean` (float, mean gamma from Step 4)
  - `CI_lower` (float, lower 95% confidence bound)
  - `CI_upper` (float, upper 95% confidence bound)
  - `predicted_mean` (float, model-predicted gamma from LMM)
**Expected Rows:** 4 (one per timepoint)

**Validation Requirement:**
Validation tools MUST be used after plot data preparation tool execution. Specific validation tools will be determined by rq_tools based on plot data format requirements. The rq_analysis agent will embed validation tool calls after the preparation tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_resolution_trajectory_data.csv exists (exact path)
- Expected rows: 4 (one per timepoint: 0, 1, 3, 6 days)
- Expected columns: 5 (time, observed_mean, CI_lower, CI_upper, predicted_mean)
- Data types: time (float64), observed_mean (float64), CI_lower (float64), CI_upper (float64), predicted_mean (float64)

*Value Ranges:*
- time in {0, 1, 3, 6} (nominal days)
- observed_mean in [0.3, 0.9] (same as Step 4)
- CI_lower in [0, 1], CI_upper in [0, 1]
- predicted_mean in [0.3, 0.9] (model predictions should be in similar range)
- CI_upper > CI_lower for all rows

*Data Quality:*
- No NaN values (all cells must have valid values)
- Exactly 4 rows (no more, no less)
- time values in ascending order: 0, 1, 3, 6
- Distribution check: observed_mean approximately equals predicted_mean (model fit reasonable)

*Log Validation:*
- Required pattern: "Plot data preparation complete: 4 timepoints"
- Required pattern: "Observed and predicted means computed"
- Forbidden patterns: "ERROR", "NaN values detected", "Missing timepoint"
- Acceptable warnings: None expected for plot data preparation

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 4 rows, found 3")
- Log failure to logs/step06_prepare_plot_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- g_debug invoked to diagnose root cause

**Plotting Function (rq_plots will call):** Trajectory plot with observed means and model-predicted curve
- rq_plots agent maps this description to plot_trajectory function
- Plot reads data/step06_resolution_trajectory_data.csv (created by this step)
- No data aggregation in rq_plots (visualization only per Option B)
- PNG output saved to plots/ folder by rq_plots

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 -> Step 1:** Long-format item-level data to aggregated gamma scores
- Input: 27,200 rows (item-level responses)
- Output: 400 rows (participant-timepoint gamma scores)
- Transformation: Group by UID and TEST, compute Goodman-Kruskal gamma

**Step 1 -> Step 2:** Gamma scores merged with TSVR time variable
- Input: 400 rows (gamma scores)
- Merge: Add TSVR_hours from dfData.csv
- Output: 400 rows (gamma scores + TSVR_hours + TSVR_days)
- Critical Decision: D070 requires TSVR (actual hours), not nominal days

**Step 2 -> Step 3:** LMM results to extracted coefficients
- Input: LMM summary text
- Output: 1 row (Time effect with dual p-values)
- Transformation: Parse fixed effects table, apply Bonferroni correction

**Step 1 -> Step 4:** Gamma scores to descriptive statistics by timepoint
- Input: 400 rows (gamma scores)
- Output: 4 rows (mean, SD, 95% CI per timepoint)
- Transformation: Group by TEST, compute summary statistics

**Step 1 -> Step 5:** Gamma scores to threshold tests
- Input: 400 rows (gamma scores)
- Output: 4 rows (one-sample t-tests vs 0.50 threshold)
- Transformation: One-sample t-test per TEST with Bonferroni correction

**Steps 2, 4 -> Step 6:** LMM predictions + observed means to plot data
- Input: 4 rows (observed means) + LMM coefficients
- Output: 4 rows (time, observed, CIs, predicted)
- Transformation: Merge observed with model-predicted trajectory

### Column Naming Conventions

**From names.md (existing conventions):**
- `UID` - Participant unique identifier (format: P### with leading zeros)
- `TEST` - Test session identifier (T1, T2, T3, T4 for Days 0, 1, 3, 6)
- `TSVR_hours` - Time Since VR in hours (Decision D070 requirement)
- `CI_lower`, `CI_upper` - 95% confidence interval bounds

**New conventions for this RQ (to be added to names.md):**
- `gamma` - Goodman-Kruskal gamma coefficient (resolution measure)
- `n_items` - Number of items used in gamma computation
- `TSVR_days` - Time Since VR in days (derived: TSVR_hours / 24)
- `threshold` - Fixed threshold value (0.50 for acceptable discrimination)

### Data Type Constraints

**Nullable vs Non-Nullable:**
- Step 0: Accuracy and Confidence must be non-null (rows with missing values excluded during extraction)
- Step 1: gamma can be NaN if no variance in accuracy/confidence (<5% acceptable)
- Steps 2-6: All outputs must be non-null (analysis requires complete data)

**Valid Ranges:**
- Accuracy: {0, 1} (dichotomous)
- Confidence: {0, 0.25, 0.5, 0.75, 1.0} (5-level ordinal)
- gamma: [-1, 1] (correlation coefficient bounds)
- TSVR_hours: [0, 168] (0 = encoding, 168 = 1 week)
- TSVR_days: [0, 7] (derived from TSVR_hours)
- p-values: [0, 1]

---

## Cross-RQ Dependencies

**Dependency Type:** RAW Data Only (No Dependencies)

**This RQ uses:** Only data/cache/dfData.csv (project-level data source)

**No dependencies on other RQs:** Can be executed independently

**Execution order:** Flexible (any order within Chapter 6)

**Data Sources:**
- dfData.csv - Participant item-level responses (TQ_* and TC_* tags)
- dfData.csv - TSVR timing data (Time Since VR in hours)

**Note:** All data extraction uses tag filtering directly from dfData.csv. No intermediate outputs from other RQs required.

---

## Validation Requirements

**CRITICAL MANDATE:**

Every analysis step in this plan MUST use validation tools after analysis tool execution.

This is not optional. This is the core architectural principle preventing cascading failures observed in v3.0 (where analysis errors propagated undetected through multiple downstream steps before discovery).

**Exact Specification Requirement:**

> "Validation tools MUST be used after analysis tool execution"

**Implementation:**
- rq_tools (Step 11 workflow) will read tools_catalog.md validation tools section
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

#### Step 0: Extract Item-Level Data

**Analysis Tool:** (determined by rq_tools - likely custom extraction function)
**Validation Tool:** (determined by rq_tools - likely validate_data_format + validate_numeric_range)

**What Validation Checks:**
- Output file exists (data/step00_item_level.csv)
- Expected row count (25,000-29,000 rows)
- Expected column count (5 columns)
- Accuracy values in {0, 1}
- Confidence values in {0, 0.25, 0.5, 0.75, 1.0}
- No NaN in Accuracy or Confidence columns
- All 100 participants represented
- All 4 test sessions represented

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step00_extract_item_level.log
- Quit script immediately
- g_debug invoked by master

---

#### Step 1: Compute Goodman-Kruskal Gamma

**Analysis Tool:** (determined by rq_tools - likely custom gamma computation function)
**Validation Tool:** (determined by rq_tools - likely validate_numeric_range + validate_data_format)

**What Validation Checks:**
- Output file exists (data/step01_gamma_scores.csv)
- Expected row count (400 rows)
- gamma in [-1, 1] range
- n_items > 0 for all rows
- <5% NaN gamma values
- All 100 participants present
- All 4 test sessions present

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step01_compute_gamma.log
- Quit script immediately
- g_debug invoked

---

#### Step 2: Fit Linear Mixed Model

**Analysis Tool:** (determined by rq_tools - likely fit_lmm_trajectory_tsvr)
**Validation Tool:** (determined by rq_tools - likely validate_lmm_convergence + validate_model_convergence)

**What Validation Checks:**
- Output files exist (data/step02_gamma_lmm_input.csv, data/step02_gamma_lmm_summary.txt)
- Model converged successfully
- Random effects variance > 0
- Fixed effects table present
- TSVR_hours merge successful (no data loss)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step02_fit_gamma_lmm.log
- Quit script immediately
- g_debug invoked

---

#### Step 3: Extract Time Effect Statistics

**Analysis Tool:** (determined by rq_tools - likely extract_fixed_effects_from_lmm)
**Validation Tool:** (determined by rq_tools - likely validate_hypothesis_test_dual_pvalues per Decision D068)

**What Validation Checks:**
- Output file exists (data/step03_time_effect.csv)
- Dual p-values present (p_uncorrected and p_bonferroni)
- p_bonferroni >= p_uncorrected
- coefficient, se, t_statistic in valid ranges
- No NaN values

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step03_extract_time_effect.log
- Quit script immediately
- g_debug invoked

---

#### Step 4: Compute Mean Gamma by Timepoint

**Analysis Tool:** (determined by rq_tools - likely custom descriptive statistics function)
**Validation Tool:** (determined by rq_tools - likely validate_numeric_range + validate_data_format)

**What Validation Checks:**
- Output file exists (data/step04_mean_gamma.csv)
- Expected row count (4 rows)
- mean_gamma, sd_gamma in valid ranges
- CI_upper > CI_lower for all rows
- N approximately 100 per timepoint
- All 4 test sessions present

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step04_compute_mean_gamma.log
- Quit script immediately
- g_debug invoked

---

#### Step 5: Test Gamma > 0.50 Threshold

**Analysis Tool:** (determined by rq_tools - likely custom t-test function)
**Validation Tool:** (determined by rq_tools - likely validate_hypothesis_test_dual_pvalues per Decision D068)

**What Validation Checks:**
- Output file exists (data/step05_gamma_threshold_tests.csv)
- Dual p-values present (p_uncorrected and p_bonferroni)
- p_bonferroni = p_uncorrected x 4 (Bonferroni correction for 4 tests)
- threshold = 0.50 for all rows
- t_statistic, df in valid ranges

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step05_test_gamma_threshold.log
- Quit script immediately
- g_debug invoked

---

#### Step 6: Prepare Plot Data

**Analysis Tool:** (determined by rq_tools - likely custom plot data preparation function)
**Validation Tool:** (determined by rq_tools - likely validate_plot_data_completeness + validate_numeric_range)

**What Validation Checks:**
- Output file exists (data/step06_resolution_trajectory_data.csv)
- Expected row count (4 rows)
- time values in {0, 1, 3, 6}
- observed_mean, predicted_mean in valid ranges [0.3, 0.9]
- CI_upper > CI_lower for all rows
- No NaN values

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step06_prepare_plot_data.log
- Quit script immediately
- g_debug invoked

---

## Summary

**Total Steps:** 7 (Step 0: extraction + Steps 1-6: analysis + plot data preparation)
**Estimated Runtime:** 15-30 minutes (Low complexity for most steps, Medium for LMM fitting)
**Cross-RQ Dependencies:** None (RAW data only from dfData.csv)
**Primary Outputs:**
- data/step01_gamma_scores.csv (resolution per participant-timepoint)
- data/step03_time_effect.csv (Time effect with dual p-values)
- data/step05_gamma_threshold_tests.csv (threshold tests at each timepoint)
- data/step06_resolution_trajectory_data.csv (plot source data)
**Validation Coverage:** 100% (all 7 steps have validation requirements with 4-layer substance criteria)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent
