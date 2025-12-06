# Analysis Plan: RQ 6.6.3 - High-Confidence Errors by Domain

**Research Question:** 6.6.3
**Created:** 2025-12-06
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines whether high-confidence errors (HCE: being confidently wrong) differ across episodic memory domains (What/Where/When). The analysis uses item-level confidence and accuracy data to compute HCE rates (Confidence >= 0.75 AND Accuracy = 0) and tests domain-specific patterns using Linear Mixed Models.

**Pipeline:** Item-level descriptive analysis -> LMM for Domain x Time interaction
**Steps:** 7 total analysis steps
**Estimated Runtime:** Medium (Step 3 LMM fitting is moderate complexity, all other steps low)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni) for domain effects
- Decision D070: TSVR as time variable (actual hours, not nominal days)

---

## Analysis Plan

### Step 0: Extract Item-Level Confidence and Accuracy Data

**Dependencies:** None (first step)
**Complexity:** Low (data extraction from dfData.csv)

**Input:**

**File:** data/cache/dfData.csv (master dataset)

**Required Columns:**
- `UID` (string, participant identifier, N=100)
- `TEST` (string, test session: T1, T2, T3, T4)
- `TQ_*` items (accuracy columns, dichotomous 0/1 for all VR memory items)
- `TC_*` items (confidence columns, 5-level ordinal: 0, 0.25, 0.5, 0.75, 1.0)

**Tag Patterns:**
- **What domain:** Items with `-N-` tag (object naming/identity)
- **Where domain:** Items with `-L-` (legacy location), `-U-` (pick-up location), or `-D-` (put-down location) tags
- **When domain:** Items with `-O-` tag (temporal order)

**Expected Data Volume:**
- ~27,200 item-responses (68 items x 100 participants x 4 tests)
- Interactive paradigms only (IFR/ICR/IRE, excluding RFR/TCR/RRE)

**Processing:**

Extract both TQ_* and TC_* columns for same items, reshape to long format (one row per item-response), tag each item by domain based on tag patterns.

**Output:**

**File:** data/step00_item_level.csv

**Format:** CSV, long format (one row per item-response)

**Columns:**
- `UID` (string): Participant identifier
- `TEST` (string): Test session (T1, T2, T3, T4)
- `item_id` (string): Item tag identifier
- `domain` (string): Memory domain (What, Where, When)
- `TQ_accuracy` (int): Dichotomous accuracy (0=incorrect, 1=correct)
- `TC_confidence` (float): 5-level confidence (0, 0.25, 0.5, 0.75, 1.0)

**Expected Rows:** ~27,200 (68 items x 100 participants x 4 tests)

**Validation Requirement:**

Validation tools MUST be used after data extraction tool execution. Specific validation tools determined by rq_tools based on extraction format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_item_level.csv exists (exact path)
- Expected rows: 27,000-27,500 (approximately 68 items x 100 participants x 4 tests)
- Expected columns: 6 (UID, TEST, item_id, domain, TQ_accuracy, TC_confidence)
- Data types: UID (string), TEST (string), item_id (string), domain (string), TQ_accuracy (int), TC_confidence (float)

*Value Ranges:*
- TQ_accuracy in {0, 1} (binary)
- TC_confidence in {0, 0.25, 0.5, 0.75, 1.0} (5-level ordinal)
- domain in {What, Where, When} (categorical)
- TEST in {T1, T2, T3, T4} (categorical)

*Data Quality:*
- No NaN in UID, TEST, item_id, domain columns (required identifiers)
- Missing data acceptable in TQ_accuracy, TC_confidence (<5% per domain)
- All 100 participants present
- All 4 tests present per participant
- All 3 domains represented

*Log Validation:*
- Required pattern: "Extracted [N] item-responses from dfData.csv"
- Required pattern: "Domains represented: What, Where, When"
- Forbidden patterns: "ERROR", "Missing domain", "No TQ_/TC_ columns found"
- Acceptable warnings: "Some items missing data (<5% per domain)"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step00_extract_item_level.log
- Quit script immediately
- g_debug invoked to diagnose root cause

---

### Step 1: Compute High-Confidence Error Flags

**Dependencies:** Step 0 (requires item-level data with accuracy and confidence)
**Complexity:** Low (simple boolean computation)

**Input:**

**File:** data/step00_item_level.csv (from Step 0)

**Required Columns:**
- `UID`, `TEST`, `item_id`, `domain` (identifiers)
- `TQ_accuracy` (int, 0/1)
- `TC_confidence` (float, 0/0.25/0.5/0.75/1.0)

**Processing:**

Compute high-confidence error flag per item-response: HCE = 1 if (TQ_accuracy = 0 AND TC_confidence >= 0.75), else HCE = 0. This creates binary HCE flag indicating confidently wrong responses.

**Output:**

**File:** data/step01_hce_by_domain.csv

**Format:** CSV, long format (one row per item-response, same as input plus HCE column)

**Columns:**
- All columns from step00_item_level.csv
- `HCE` (int): High-confidence error flag (0=not HCE, 1=HCE)

**Expected Rows:** ~27,200 (same as input)

**Validation Requirement:**

Validation tools MUST be used after HCE computation tool execution. Specific validation tools determined by rq_tools based on computation logic requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_hce_by_domain.csv exists (exact path)
- Expected rows: Match input row count (~27,200)
- Expected columns: 7 (input 6 columns + HCE)
- Data types: HCE (int, values 0 or 1)

*Value Ranges:*
- HCE in {0, 1} (binary)
- HCE = 1 only when TQ_accuracy = 0 AND TC_confidence >= 0.75 (logic check)

*Data Quality:*
- No NaN in HCE column (all item-responses must have HCE computed)
- HCE rate > 0 (at least some high-confidence errors present)
- HCE rate < 0.5 (sanity check - majority of responses should not be HCE)

*Log Validation:*
- Required pattern: "Computed HCE flags for [N] item-responses"
- Required pattern: "Overall HCE rate: [X]%" (sanity check value)
- Forbidden patterns: "ERROR", "NaN in HCE column", "HCE logic error"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step01_compute_hce_flags.log
- Quit script immediately
- g_debug invoked to diagnose root cause

---

### Step 2: Aggregate HCE Rates by Domain x Timepoint

**Dependencies:** Step 1 (requires HCE flags)
**Complexity:** Low (groupby aggregation)

**Input:**

**File:** data/step01_hce_by_domain.csv (from Step 1)

**Required Columns:**
- `domain` (string): What, Where, When
- `TEST` (string): T1, T2, T3, T4
- `HCE` (int): 0 or 1

**Processing:**

Group by domain x TEST, compute mean(HCE) to get HCE rate per cell. This produces 12 summary rows (3 domains x 4 tests) showing mean HCE rates.

**Output:**

**File:** data/step02_hce_rates_summary.csv

**Format:** CSV, summary statistics (one row per domain x test combination)

**Columns:**
- `domain` (string): Memory domain
- `TEST` (string): Test session
- `HCE_rate` (float): Mean HCE rate (proportion 0-1)
- `N_items` (int): Number of item-responses in this cell
- `N_HCE` (int): Count of high-confidence errors

**Expected Rows:** 12 (3 domains x 4 tests)

**Validation Requirement:**

Validation tools MUST be used after aggregation tool execution. Specific validation tools determined by rq_tools based on summary statistics requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_hce_rates_summary.csv exists (exact path)
- Expected rows: 12 (exactly 3 domains x 4 tests)
- Expected columns: 5 (domain, TEST, HCE_rate, N_items, N_HCE)
- Data types: HCE_rate (float), N_items (int), N_HCE (int)

*Value Ranges:*
- HCE_rate in [0, 1] (proportion)
- N_items > 0 (all cells must have data)
- N_HCE >= 0 (count)
- N_HCE <= N_items (sanity check)
- HCE_rate = N_HCE / N_items (consistency check)

*Data Quality:*
- All 3 domains present (What, Where, When)
- All 4 tests present (T1, T2, T3, T4)
- No NaN values
- Complete factorial design (no missing cells)

*Log Validation:*
- Required pattern: "Aggregated HCE rates: 12 cells (3 domains x 4 tests)"
- Required pattern: "Domain HCE rates - What: [X]%, Where: [Y]%, When: [Z]%"
- Forbidden patterns: "ERROR", "Missing domain", "Missing test", "NaN in summary"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step02_aggregate_hce_rates.log
- Quit script immediately
- g_debug invoked to diagnose root cause

---

### Step 3: Fit Linear Mixed Model Testing Domain x Time Interaction

**Dependencies:** Step 2 (requires aggregated HCE rates)
**Complexity:** Medium (LMM fitting with random effects)

**Input:**

**File 1:** data/step02_hce_rates_summary.csv (from Step 2)

**Required Columns:**
- `domain` (string): What, Where, When
- `TEST` (string): T1, T2, T3, T4
- `HCE_rate` (float): Mean HCE rate per cell

**File 2:** data/cache/dfData.csv (for TSVR_hours extraction per Decision D070)

**Required Columns:**
- `UID` (string): Participant identifier
- `TEST` (string): Test session
- `TSVR_hours` (float): Time Since VR in hours (actual elapsed time)

**Processing:**

Merge HCE_rates with TSVR_hours on TEST to add time variable (Decision D070). Fit Linear Mixed Model: HCE_rate ~ domain * TSVR_hours + (TSVR_hours | UID). Model tests whether HCE rate trajectories differ across domains. Random slopes by participant account for individual differences. REML=True for variance component estimation.

**Output:**

**File:** data/step03_domain_hce_lmm.txt

**Format:** Plain text, LMM summary output

**Contents:**
- Fixed effects table (coefficients, SE, t-statistics, p-values)
- Random effects variance components
- Model fit statistics (AIC, BIC, log-likelihood)
- Convergence status

**Validation Requirement:**

Validation tools MUST be used after LMM fitting tool execution. Specific validation tools determined by rq_tools based on LMM convergence and assumptions requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_domain_hce_lmm.txt exists (exact path)
- File size > 1 KB (substantial model output)

*Value Ranges:*
- Fixed effect coefficients: reasonable magnitudes (typically -1 to +1 for standardized predictors)
- Standard errors > 0 (all estimates must have SEs)
- p-values in [0, 1]
- Variance components >= 0 (cannot be negative)

*Data Quality:*
- Model converged (convergence status = True)
- No NaN in fixed effects table
- No singularity warnings (indicates random effects structure supported)
- Domain main effect present in fixed effects
- Domain x TSVR_hours interaction present in fixed effects

*Log Validation:*
- Required pattern: "Model converged: True"
- Required pattern: "Fixed effects: [N] terms"
- Required pattern: "Random effects: TSVR_hours | UID"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "Singular fit", "NaN in fixed effects"
- Acceptable warnings: "Gradient close to zero" (common in mixed models, acceptable if converged)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step03_fit_domain_hce_lmm.log
- Quit script immediately
- g_debug invoked to diagnose root cause (common causes: insufficient data, model misspecification)

---

### Step 4: Test Domain Main Effect and Domain x Time Interaction

**Dependencies:** Step 3 (requires fitted LMM)
**Complexity:** Low (hypothesis testing on fitted model)

**Input:**

**File:** data/step03_domain_hce_lmm.txt (from Step 3, but read model object from memory/pickle)

**Processing:**

Extract fixed effects for Domain main effect and Domain x Time interaction. Compute test statistics (F-tests or Wald chi-square tests). Report dual p-values per Decision D068: (1) uncorrected p-value, (2) Bonferroni-corrected p-value for 2 tests (alpha = 0.05/2 = 0.025).

**Output:**

**File:** data/step04_domain_effects.csv

**Format:** CSV, hypothesis test results

**Columns:**
- `effect` (string): Effect name ("Domain main effect", "Domain x Time interaction")
- `test_statistic` (float): F or chi-square value
- `df1` (int): Numerator degrees of freedom
- `df2` (int): Denominator degrees of freedom (if F-test)
- `p_uncorrected` (float): Uncorrected p-value (Decision D068)
- `p_bonferroni` (float): Bonferroni-corrected p-value (Decision D068)
- `significant_bonferroni` (bool): True if p_bonferroni < 0.025

**Expected Rows:** 2 (Domain main effect + Domain x Time interaction)

**Validation Requirement:**

Validation tools MUST be used after hypothesis testing tool execution. Specific validation tools determined by rq_tools based on Decision D068 dual p-value requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_domain_effects.csv exists (exact path)
- Expected rows: 2 (Domain main effect + Domain x Time interaction)
- Expected columns: 7 (effect, test_statistic, df1, df2, p_uncorrected, p_bonferroni, significant_bonferroni)
- Data types: test_statistic (float), df1 (int), df2 (int), p_uncorrected (float), p_bonferroni (float), significant_bonferroni (bool)

*Value Ranges:*
- test_statistic >= 0 (F and chi-square always non-negative)
- df1 > 0, df2 > 0 (degrees of freedom must be positive)
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1]
- p_bonferroni = min(1.0, p_uncorrected * 2) (Bonferroni formula for 2 tests)

*Data Quality:*
- Both effects present (no missing rows)
- No NaN values
- Decision D068 compliance: BOTH p_uncorrected AND p_bonferroni present

*Log Validation:*
- Required pattern: "Domain main effect: p_uncorrected = [X], p_bonferroni = [Y]"
- Required pattern: "Domain x Time interaction: p_uncorrected = [X], p_bonferroni = [Y]"
- Required pattern: "Decision D068: Dual p-values reported"
- Forbidden patterns: "ERROR", "Missing p-value", "NaN in results"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step04_test_domain_effects.log
- Quit script immediately
- g_debug invoked to diagnose root cause

---

### Step 5: Rank Domains by Mean HCE Rate

**Dependencies:** Step 2 (requires summary HCE rates)
**Complexity:** Low (simple aggregation and ranking)

**Input:**

**File:** data/step02_hce_rates_summary.csv (from Step 2)

**Required Columns:**
- `domain` (string): What, Where, When
- `HCE_rate` (float): Mean HCE rate per cell

**Processing:**

Compute overall mean HCE rate per domain (averaged across all timepoints). Rank domains from highest to lowest HCE rate. Compare observed ranking to hypothesis prediction (When > Where > What).

**Output:**

**File:** data/step05_domain_ranking.csv

**Format:** CSV, domain rankings

**Columns:**
- `domain` (string): Memory domain
- `mean_HCE_rate` (float): Overall mean HCE rate (averaged across all 4 tests)
- `rank` (int): Rank (1=highest HCE rate, 3=lowest HCE rate)
- `hypothesis_rank` (int): Predicted rank per hypothesis (When=1, Where=2, What=3)
- `matches_hypothesis` (bool): True if observed rank matches predicted rank

**Expected Rows:** 3 (What, Where, When)

**Validation Requirement:**

Validation tools MUST be used after ranking tool execution. Specific validation tools determined by rq_tools based on ranking computation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_domain_ranking.csv exists (exact path)
- Expected rows: 3 (exactly What, Where, When)
- Expected columns: 5 (domain, mean_HCE_rate, rank, hypothesis_rank, matches_hypothesis)
- Data types: mean_HCE_rate (float), rank (int), hypothesis_rank (int), matches_hypothesis (bool)

*Value Ranges:*
- mean_HCE_rate in [0, 1] (proportion)
- rank in {1, 2, 3} (exactly 3 ranks, no ties expected)
- hypothesis_rank in {1, 2, 3} (fixed: When=1, Where=2, What=3)

*Data Quality:*
- All 3 domains present
- No NaN values
- Ranks are unique (no duplicate ranks)
- Hypothesis ranks match specification (When=1, Where=2, What=3)

*Log Validation:*
- Required pattern: "Domain ranking: [domain1] (rank [N]), [domain2] (rank [N]), [domain3] (rank [N])"
- Required pattern: "Hypothesis prediction: When > Where > What"
- Required pattern: "Observed matches hypothesis: [True/False]"
- Forbidden patterns: "ERROR", "Duplicate ranks", "Missing domain"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step05_rank_domains.log
- Quit script immediately
- g_debug invoked to diagnose root cause

---

### Step 6: Prepare Plot Data for Domain x Time HCE Visualization

**Dependencies:** Steps 2, 3 (requires observed HCE rates + LMM predictions)
**Complexity:** Low (data aggregation for plotting)

**Plot Description:** Line plot showing HCE rates over time (TSVR_hours) grouped by domain (What/Where/When), with observed means as points and LMM predictions as fitted lines.

**Required Data Sources:**
- data/step02_hce_rates_summary.csv (observed HCE rates by domain x test)
- data/step03_domain_hce_lmm.txt (LMM model object for predictions, read from memory/pickle)
- data/cache/dfData.csv (TSVR_hours mapping for time axis per Decision D070)

**Input:**

**File 1:** data/step02_hce_rates_summary.csv

**Columns:** domain, TEST, HCE_rate, N_items, N_HCE

**File 2:** LMM model object (from Step 3, in memory or pickled)

**File 3:** data/cache/dfData.csv (TSVR_hours extraction)

**Columns:** TEST, TSVR_hours

**Processing:**

1. Merge observed HCE rates with TSVR_hours on TEST (adds time variable)
2. Generate LMM predictions for all domain x TSVR_hours combinations using fitted model from Step 3
3. Compute 95% confidence intervals for predictions
4. Combine observed means (for point plotting) + predicted values (for line plotting) into single plot source CSV
5. Sort by domain, then time

**Output:**

**File:** data/step06_hce_by_domain_plot_data.csv

**Format:** CSV, plot source data for domain x time HCE visualization

**Columns:**
- `time` (float): TSVR_hours (actual time since VR session)
- `domain` (string): Memory domain (What, Where, When)
- `HCE_rate_observed` (float): Observed mean HCE rate (from step02)
- `HCE_rate_predicted` (float): LMM predicted HCE rate (from step03 model)
- `CI_lower` (float): Lower 95% confidence bound for prediction
- `CI_upper` (float): Upper 95% confidence bound for prediction

**Expected Rows:** 12 (3 domains x 4 timepoints)

**Validation Requirement:**

Validation tools MUST be used after plot data preparation tool execution. Specific validation tools determined by rq_tools based on plot data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_hce_by_domain_plot_data.csv exists (exact path)
- Expected rows: 12 (3 domains x 4 timepoints)
- Expected columns: 6 (time, domain, HCE_rate_observed, HCE_rate_predicted, CI_lower, CI_upper)
- Data types: time (float), domain (string), HCE_rate_observed (float), HCE_rate_predicted (float), CI_lower (float), CI_upper (float)

*Value Ranges:*
- time in [0, 168] hours (0=encoding, 168=1 week, maximum retention interval)
- HCE_rate_observed in [0, 1] (proportion)
- HCE_rate_predicted in [0, 1] (proportion)
- CI_lower in [0, 1], CI_upper in [0, 1]
- CI_lower <= HCE_rate_predicted <= CI_upper (consistency check)
- domain in {What, Where, When} (categorical)

*Data Quality:*
- No NaN values tolerated (all cells must have valid values)
- Expected N: Exactly 12 rows (no more, no less)
- All 3 domains represented (What, Where, When)
- All 4 timepoints represented (T1, T2, T3, T4 corresponding to TSVR_hours)
- No duplicate rows (domain x time combinations unique)
- Distribution check: CI_upper > CI_lower for all rows

*Log Validation:*
- Required pattern: "Plot data preparation complete: 12 rows created"
- Required pattern: "All domains represented: What, Where, When"
- Required pattern: "Time range: [min] to [max] hours"
- Forbidden patterns: "ERROR", "NaN values detected", "Missing domain", "Missing timepoint"
- Acceptable warnings: None expected for plot data preparation

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 12 rows, found 9")
- Log failure to logs/step06_prepare_hce_plot_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- g_debug invoked to diagnose root cause

**Plotting Function (rq_plots will call):** Line plot with observed points and fitted trajectories
- rq_plots agent maps this description to specific tools/plots.py function
- Plot reads data/step06_hce_by_domain_plot_data.csv (created by this step)
- No data aggregation in rq_plots (visualization only per Option B architecture)
- PNG output saved to plots/ folder by rq_plots

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs - intermediate and final)

- data/step00_item_level.csv (~27,200 rows: item-level TQ_ accuracy + TC_ confidence with domain tags)
- data/step01_hce_by_domain.csv (~27,200 rows: item-level with HCE flag added)
- data/step02_hce_rates_summary.csv (12 rows: 3 domains x 4 tests with mean HCE rates, N_items, N_HCE)
- data/step03_domain_hce_lmm.txt (LMM summary output with fixed effects, random effects, fit statistics)
- data/step04_domain_effects.csv (2 rows: Domain main effect + Domain x Time interaction with dual p-values)
- data/step05_domain_ranking.csv (3 rows: domains ranked by mean HCE rate with hypothesis comparison)
- data/step06_hce_by_domain_plot_data.csv (12 rows: observed + predicted HCE rates by domain x time for plotting)

### Logs (ONLY execution logs - .log files capturing stdout/stderr)

- logs/step00_extract_item_level.log
- logs/step01_compute_hce_flags.log
- logs/step02_aggregate_hce_rates.log
- logs/step03_fit_domain_hce_lmm.log
- logs/step04_test_domain_effects.log
- logs/step05_rank_domains.log
- logs/step06_prepare_hce_plot_data.log

### Plots (EMPTY until rq_plots runs)

- plots/hce_by_domain.png (created by rq_plots, NOT analysis steps)

### Results (EMPTY until rq_results runs)

- results/summary.md (created by rq_results, NOT analysis steps)

---

## Expected Data Formats

### Item-Level Format (Steps 0-1)

**Wide -> Long Transformation:**
- dfData.csv stores TQ_* and TC_* as wide format (one row per participant-test, columns are items)
- Step 0 reshapes to long format (one row per item-response)
- Each row represents single item response with accuracy + confidence + domain tag

**Column Schema:**
- Identifiers: UID (string), TEST (string), item_id (string)
- Grouping: domain (string, values: What/Where/When)
- Measurements: TQ_accuracy (int, 0/1), TC_confidence (float, 0/0.25/0.5/0.75/1.0)
- Derived: HCE (int, 0/1, added in Step 1)

### Summary Format (Steps 2, 5)

**Aggregation Level:** Domain x Test (12 cells)

**Column Schema:**
- Grouping: domain (string), TEST (string)
- Summary statistics: HCE_rate (float, mean), N_items (int, count), N_HCE (int, sum)

### LMM Format (Steps 3-4)

**Input for LMM:** Long format with TSVR_hours merged (Decision D070)

**Model Formula:** `HCE_rate ~ domain * TSVR_hours + (TSVR_hours | UID)`

**Fixed Effects:** Domain main effect (2 df), TSVR_hours main effect (1 df), Domain x TSVR_hours interaction (2 df)

**Random Effects:** Random intercepts + random slopes for TSVR_hours by participant (UID)

### Plot Data Format (Step 6)

**Merge Logic:**
1. Start with observed HCE rates (step02_hce_rates_summary.csv)
2. Merge with TSVR_hours on TEST (adds time variable from dfData.csv)
3. Generate LMM predictions using fitted model (step03)
4. Combine observed + predicted + confidence intervals
5. Output: 12 rows (3 domains x 4 timepoints) plot-ready

**Required Columns:** time (float), domain (string), HCE_rate_observed (float), HCE_rate_predicted (float), CI_lower (float), CI_upper (float)

---

## Cross-RQ Dependencies

**Data Type:** RAW (from dfData.csv item-level data)

**No dependencies on other RQs:** Can be executed independently

**Execution order:** Flexible (any order within Chapter 6)

**Data Sources:**
- data/cache/dfData.csv (master dataset) - TQ_* accuracy columns, TC_* confidence columns, TEST, UID
- Item tag structure for domain classification (-N-, -L-/-U-/-D-, -O-)

**Note:** All data extraction uses direct reading from dfData.csv. No intermediate outputs from other RQs required. This RQ is conceptually related to RQ 6.1.1 (establishes confidence measurement) and RQ 6.6.1 (establishes HCE definition), but does NOT require their outputs as inputs.

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
- g_code (Step 14 workflow) will generate stepN_name.py scripts with validation function calls
- bash execution (Step 14 workflow) will run analysis -> validation -> error on validation failure

**Downstream Agent Requirements:**
- **rq_tools:** MUST specify validation tool for EVERY analysis step (no exceptions)
- **rq_analysis:** MUST embed validation tool call for EVERY analysis step (no exceptions)
- **g_code:** MUST generate code with validation function calls (no exceptions)
- **rq_inspect:** MUST verify validation ran successfully (checks logs/stepN_name.log for validation output)

### Validation Requirements By Step

**Step 0: Extract Item-Level Data**
- Output file exists (data/step00_item_level.csv)
- Expected row count (~27,200)
- Expected column count (6)
- No unexpected NaN patterns (>50% NaN per domain suggests extraction error)
- Domain values valid (What, Where, When only)
- TEST values valid (T1, T2, T3, T4 only)
- TQ_accuracy in {0, 1}, TC_confidence in {0, 0.25, 0.5, 0.75, 1.0}

**Step 1: Compute HCE Flags**
- Output file exists (data/step01_hce_by_domain.csv)
- Row count matches input
- HCE column added with values {0, 1} only
- HCE logic correct: HCE=1 only when TQ_accuracy=0 AND TC_confidence>=0.75
- No NaN in HCE column

**Step 2: Aggregate HCE Rates**
- Output file exists (data/step02_hce_rates_summary.csv)
- Exactly 12 rows (3 domains x 4 tests)
- All domains present (What, Where, When)
- All tests present (T1, T2, T3, T4)
- HCE_rate in [0, 1]
- N_HCE <= N_items (consistency)
- HCE_rate = N_HCE / N_items (arithmetic check)

**Step 3: Fit LMM**
- Output file exists (data/step03_domain_hce_lmm.txt)
- Model converged (convergence status True)
- No NaN in fixed effects table
- No singularity warnings
- Domain main effect present in fixed effects
- Domain x TSVR_hours interaction present in fixed effects
- Variance components >= 0

**Step 4: Test Domain Effects**
- Output file exists (data/step04_domain_effects.csv)
- Exactly 2 rows (Domain main effect + Domain x Time interaction)
- Both p_uncorrected and p_bonferroni present (Decision D068 compliance)
- p_bonferroni = min(1.0, p_uncorrected * 2) (Bonferroni formula for 2 tests)
- test_statistic >= 0, df > 0, p-values in [0, 1]

**Step 5: Rank Domains**
- Output file exists (data/step05_domain_ranking.csv)
- Exactly 3 rows (What, Where, When)
- Ranks in {1, 2, 3}, unique (no ties)
- Hypothesis ranks correct (When=1, Where=2, What=3)
- mean_HCE_rate in [0, 1]

**Step 6: Prepare Plot Data**
- Output file exists (data/step06_hce_by_domain_plot_data.csv)
- Exactly 12 rows (3 domains x 4 timepoints)
- All domains present (What, Where, When)
- All required columns present (time, domain, HCE_rate_observed, HCE_rate_predicted, CI_lower, CI_upper)
- All values in valid ranges (HCE rates in [0,1], time in [0,168], CI_lower <= predicted <= CI_upper)
- No NaN values

---

## Summary

**Total Steps:** 7 (Step 0: extraction + Steps 1-6: analysis)
**Estimated Runtime:** Medium (30-60 minutes total - Step 3 LMM fitting is moderate complexity, all other steps low)
**Cross-RQ Dependencies:** None - RAW data only from dfData.csv
**Primary Outputs:** Item-level HCE flags, domain x time HCE rates, LMM domain effects with dual p-values, domain ranking, plot data
**Validation Coverage:** 100% (all 7 steps have validation requirements with 4-layer substance criteria)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent for RQ 6.6.3
