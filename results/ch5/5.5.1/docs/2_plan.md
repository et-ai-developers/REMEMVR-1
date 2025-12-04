# Analysis Plan: RQ 5.5.1 - Source-Destination Spatial Memory Trajectories

**Created by:** rq_planner agent
**Date:** 2025-12-04
**Status:** Ready for rq_tools (Step 11 workflow)
**RQ ID:** 5.5.1
**Type:** Source-Destination / Trajectories (ROOT)

---

## Overview

This analysis plan examines whether pick-up locations (source: -U-) and put-down locations (destination: -D-) show different forgetting trajectories in VR episodic spatial memory. The analysis uses a 2-factor IRT model to estimate source and destination memory abilities, followed by linear mixed models to test for LocationType main effects and LocationType x Time interactions across a 6-day retention interval.

**Pipeline:** IRT (2-factor GRM with 2-pass purification) -> LMM (trajectory analysis with 5 candidate time transformations)

**Total Steps:** 8 steps (Step 0: extraction, Steps 1-7: analysis)

**Estimated Runtime:** ~75-90 minutes
- Step 0: Low (~2 min)
- Step 1: High (~30-45 min, 2-factor GRM calibration)
- Step 2: Low (~1 min, purification filtering)
- Step 3: High (~30-45 min, 2-factor GRM re-calibration)
- Step 4: Low (~2 min, merge operations)
- Step 5: Medium (~5-10 min, 5 LMM fits)
- Step 6: Low (~2 min, contrasts)
- Step 7: Low (~2 min, plot data prep)

**Key Decisions Applied:**
- Decision D039: 2-pass IRT purification (Pass 1 all items -> Purify -> Pass 2 retained items)
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni for post-hoc contrasts)
- Decision D069: Dual-scale trajectory plots (theta scale + probability scale)
- Decision D070: TSVR_hours as LMM time variable (actual elapsed time, not nominal days)

**Data Source:** RAW (dfData.csv) - This is a ROOT RQ extracting directly from raw data

**Sample Size:** N=100 participants x 4 test sessions x 2 location types = 800 observations

---

## Analysis Plan

### Step 0: Extract Source and Destination Location Data

**Purpose:** Extract VR spatial memory data from dfData.csv for source (-U-) and destination (-D-) location items from interactive paradigms only

**Dependencies:** None (ROOT RQ, first step)

**Complexity:** Low (~2 minutes, data extraction only)

**Input:**

**File:** data/cache/dfData.csv (project-level raw data source)

**Required Columns:**
- `UID` (string, participant identifier, format: P### with leading zeros)
- `test` (string, test session identifier: T1, T2, T3, T4)
- Tag columns matching pattern: `TQ_VR_{IFR|ICR|IRE}_*_{U|D}` (source and destination location items from interactive paradigms only)
- TSVR columns for actual time since encoding

**Filters:**
- **Paradigms:** IFR (Item Free Recall), ICR (Item Cued Recall), IRE (Item Recognition) ONLY
- **Exclusions:** RFR (Room Free Recall), TCR (Template Cued Recall) - no interactive pick-up/put-down structure
- **Location Types:** -U- tags (source/pick-up, 18 items), -D- tags (destination/put-down, 18 items)
- **Exclusions:** -L- tags (static location, legacy items without source-destination manipulation)
- **Response Dichotomization:** TQ < 1 -> 0 (incorrect), TQ >= 1 -> 1 (correct)

**Expected Data Volume:**
- 36 total items (18 source + 18 destination)
- 100 participants x 4 test sessions = 400 composite_IDs
- 400 x 36 = 14,400 item-level binary responses

**Processing:**

1. **Load dfData.csv** and filter to VR episodic memory columns
2. **Filter columns** to interactive paradigms only (IFR, ICR, IRE)
3. **Further filter** to -U- and -D- location tags only (exclude -L-, -N-, -O- tags)
4. **Dichotomize responses:** TQ < 1 -> 0, TQ >= 1 -> 1
5. **Create composite_ID:** Concatenate UID + "_" + test (e.g., "P001_T1")
6. **Reshape to wide format:** Rows = composite_ID (400 rows), Columns = item tags (36 columns)
7. **Create Q-matrix:** 36 items x 2 factors (Factor 1: source = all *-U-* items, Factor 2: destination = all *-D-* items)
8. **Extract TSVR:** Create TSVR_hours column (actual time since VR encoding session in hours)
9. **Create TSVR mapping file:** composite_ID, UID, test, TSVR_hours (400 rows)

**Output:**

**File 1:** data/step00_irt_input.csv
**Format:** CSV, wide format (composite_ID x item columns)
**Columns:**
  - `composite_ID` (string, format: {UID}_{test}, e.g., "P001_T1")
  - 36 item columns (tag format: TQ_VR_{paradigm}_{item}_U or TQ_VR_{paradigm}_{item}_D)
  - Values: {0, 1} (binary responses, NaN for missing/not administered)
**Expected Rows:** 400 (100 participants x 4 tests)
**Expected Columns:** 37 (1 composite_ID + 36 items)

**File 2:** data/step00_q_matrix.csv
**Format:** CSV, item-by-factor loading matrix
**Columns:**
  - `item_tag` (string, item identifier matching column names in irt_input.csv)
  - `source` (int, 1 if item loads on source factor, 0 otherwise)
  - `destination` (int, 1 if item loads on destination factor, 0 otherwise)
**Expected Rows:** 36 items
**Expected Pattern:** Each item loads on exactly 1 factor (18 source items, 18 destination items)

**File 3:** data/step00_tsvr_mapping.csv
**Format:** CSV, time mapping file
**Columns:**
  - `composite_ID` (string, matches irt_input.csv primary key)
  - `UID` (string, participant identifier)
  - `test` (string, test session: T1, T2, T3, T4)
  - `TSVR_hours` (float, actual time since encoding in hours)
**Expected Rows:** 400 (one per composite_ID)

**Validation Requirement:**

Validation tools MUST be used after data extraction tool execution. Specific validation tools will be determined by rq_tools based on extraction type (wide-format IRT input validation, Q-matrix structure validation, TSVR mapping validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_irt_input.csv: 400 rows x 37 columns (composite_ID: object, 36 items: int64)
- data/step00_q_matrix.csv: 36 rows x 3 columns (item_tag: object, source: int64, destination: int64)
- data/step00_tsvr_mapping.csv: 400 rows x 4 columns (composite_ID: object, UID: object, test: object, TSVR_hours: float64)

*Value Ranges:*
- IRT input item values in {0, 1} (NaN acceptable for missing data)
- Q-matrix factor loadings in {0, 1} (binary indicators)
- TSVR_hours in [0, 168] (0 = encoding session, 168 = 1 week maximum retention)
- Each Q-matrix row sums to 1 (each item loads on exactly one factor)

*Data Quality:*
- All 400 composite_IDs present (100 participants x 4 tests, no data loss)
- All 36 items present (18 source + 18 destination)
- composite_IDs must be unique (no duplicates)
- Q-matrix: Exactly 18 items load on source factor, exactly 18 on destination factor
- TSVR_hours: All 400 composite_IDs matched (no missing time values)
- Missing item responses acceptable (<20% NaN per item), but >50% NaN indicates extraction error

*Log Validation:*
- Required patterns: "Extracted 36 items (18 source, 18 destination)", "Created 400 composite_IDs", "Q-matrix: 2 factors validated"
- Forbidden patterns: "ERROR", "EXTRACTION FAILED", "MISSING PARADIGM"
- Acceptable warnings: "Item {X} has >20% missing responses" (temporal items may have high missingness)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 36 items, found 29")
- Log failure to logs/step00_extract_vr_data.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause (common issues: tag pattern mismatch, paradigm filtering error)

---

### Step 1: IRT Calibration Pass 1 (All Items)

**Purpose:** Calibrate 2-dimensional Graded Response Model on all 36 items (source and destination factors) to obtain initial item parameters for purification

**Dependencies:** Step 0 (requires irt_input.csv, q_matrix.csv)

**Complexity:** High (~30-45 minutes, 2-factor GRM calibration with 36 items, 400 observations)

**Input:**

**File 1:** data/step00_irt_input.csv (from Step 0)
**Format:** Wide format (composite_ID x item columns)
**Expected:** 400 rows x 37 columns (1 ID + 36 items)

**File 2:** data/step00_q_matrix.csv (from Step 0)
**Format:** Item-by-factor loading matrix
**Expected:** 36 rows x 3 columns (item_tag, source, destination)

**Processing:**

**Model Specification:**
- **Model Type:** 2-dimensional Graded Response Model (GRM) with correlated factors
- **Factors:** Factor 1 = source memory (18 -U- items), Factor 2 = destination memory (18 -D- items)
- **Factor Correlation:** Estimated (allows for correlated source-destination abilities)
- **Prior:** p1_med (median difficulty prior per project standards)
- **Estimation:** Variational inference via IWAVE algorithm
- **Convergence:** Monitor ELBO (evidence lower bound), require stable convergence

**Minimal Settings Testing (CRITICAL per D039):**
Before production run, test pipeline with minimal settings:
- max_iter=50, mc_samples=10, iw_samples=10 (~5-10 min runtime)
- Validates pipeline integrity before committing to 30-45 min production run
- If minimal settings fail -> fix pipeline before production

**Production Settings:**
- max_iter=200, mc_samples=100, iw_samples=100 (~30-45 min runtime)
- Only run after minimal settings validation passes

**Outputs:**
1. **Item parameters:** Discrimination (a) and difficulty (b) for 36 items
2. **Theta estimates:** 2 dimensions x 400 composite_IDs (theta_source, theta_destination with SEs)
3. **Model diagnostics:** Convergence status, ELBO trajectory, factor correlation

**Output:**

**File 1:** data/step01_pass1_item_params.csv
**Format:** CSV, item parameters
**Columns:**
  - `item_tag` (string, item identifier matching irt_input.csv columns)
  - `factor` (string, "source" or "destination")
  - `a` (float, discrimination parameter, expected range: [0.4, 4.0])
  - `b` (float, difficulty parameter, unrestricted range but typically [-3, 3])
**Expected Rows:** 36 items

**File 2:** data/step01_pass1_theta.csv
**Format:** CSV, ability estimates (diagnostic only, used for purification decisions)
**Columns:**
  - `composite_ID` (string, matches irt_input.csv)
  - `theta_source` (float, source memory ability)
  - `theta_destination` (float, destination memory ability)
  - `se_source` (float, standard error for source theta)
  - `se_destination` (float, standard error for destination theta)
**Expected Rows:** 400 composite_IDs

**File 3:** data/step01_pass1_diagnostics.txt
**Format:** Plain text, model diagnostics
**Contents:**
  - Convergence status (True/False)
  - Final ELBO value
  - Factor correlation estimate
  - Runtime (minutes)

**Validation Requirement:**

Validation tools MUST be used after IRT calibration tool execution. Specific validation tools will be determined by rq_tools based on analysis type (IRT convergence validation, parameter bounds validation, theta reliability validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_pass1_item_params.csv: 36 rows x 4 columns (item_tag: object, factor: object, a: float64, b: float64)
- data/step01_pass1_theta.csv: 400 rows x 5 columns (composite_ID: object, theta_source/destination: float64, se_source/destination: float64)
- data/step01_pass1_diagnostics.txt: Text file with convergence info

*Value Ranges:*
- Discrimination (a) in [0.0, 10.0] (values >10.0 suggest estimation error, <0.0 impossible)
- Difficulty (b) in [-6.0, 6.0] (extreme values indicate potential misfit but not necessarily error)
- Theta (source, destination) in [-4, 4] (outside range indicates convergence issues)
- Standard errors (se_source, se_destination) in [0.1, 1.5] (below 0.1 suspicious, above 1.5 unreliable)

*Data Quality:*
- All 36 items present in item_params.csv (no items dropped during calibration)
- All 400 composite_IDs present in theta.csv (no participants excluded)
- No NaN values in item parameters (indicates estimation failure)
- No NaN values in theta estimates (model must estimate for all participants)
- Factor correlation between source and destination in [-1, 1]

*Log Validation:*
- Required patterns: "Model converged: True", "ELBO stabilized", "36 items calibrated", "400 participants estimated"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "NaN parameters detected"
- Acceptable warnings: "Item {X} has extreme difficulty (b > 3.0)" (temporal items may be difficult, but still estimated)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Model failed to converge after 200 iterations")
- Log failure to logs/step01_irt_calibration_pass1.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose (common causes: insufficient data, model misspecification, numerical instability)

---

### Step 2: Purify Items by Quality Thresholds (Decision D039)

**Purpose:** Filter items based on Decision D039 purification thresholds to retain only high-quality items for Pass 2 calibration

**Dependencies:** Step 1 (requires pass1_item_params.csv)

**Complexity:** Low (~1 minute, threshold-based filtering only)

**Input:**

**File:** data/step01_pass1_item_params.csv (from Step 1)
**Format:** CSV with columns: item_tag, factor, a, b
**Expected:** 36 rows (18 source + 18 destination items)

**Processing:**

**Purification Criteria (Decision D039):**
- **Retain items IF:** (|b| <= 3.0) AND (a >= 0.4)
- **Exclude items IF:** (|b| > 3.0) OR (a < 0.4)

**Rationale:**
- Items with extreme difficulty (|b| > 3.0) provide little information at typical ability levels
- Items with low discrimination (a < 0.4) fail to differentiate between ability levels

**Quality Check:**
- **Minimum requirement:** >= 10 items retained per factor (20 total minimum)
- **Expected retention:** 25-32 items (70-90% retention based on prior analyses)
- **If < 10 items per factor:** Raise error, model unreliable

**Output:**

**File 1:** data/step02_purified_items.csv
**Format:** CSV, list of retained items with Pass 1 parameters
**Columns:**
  - `item_tag` (string, item identifier)
  - `factor` (string, "source" or "destination")
  - `a` (float, discrimination from Pass 1)
  - `b` (float, difficulty from Pass 1)
  - `retention_reason` (string, "PASS" for all retained items)
**Expected Rows:** 25-32 items (70-90% of 36 original items)

**File 2:** data/step02_purification_report.txt
**Format:** Plain text report
**Contents:**
  - Total items analyzed: 36
  - Items retained: {N} ({percent}%)
  - Items excluded: {M} ({percent}%)
  - Breakdown by exclusion reason:
    - Low discrimination (a < 0.4): {count}
    - Extreme difficulty (|b| > 3.0): {count}
  - Factor-specific retention:
    - Source: {N_source} items retained (of 18)
    - Destination: {N_destination} items retained (of 18)
  - List of excluded items with reasons

**Validation Requirement:**

Validation tools MUST be used after item purification tool execution. Specific validation tools will be determined by rq_tools based on purification type (threshold validation, minimum items validation, factor balance validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_purified_items.csv: 25-32 rows x 5 columns (item_tag: object, factor: object, a: float64, b: float64, retention_reason: object)
- data/step02_purification_report.txt: Text file with retention statistics

*Value Ranges:*
- Retained item discrimination (a) >= 0.4 (threshold enforcement)
- Retained item difficulty (|b|) <= 3.0 (threshold enforcement)
- Retention rate in [0.70, 0.90] (25-32 items of 36 original)

*Data Quality:*
- Minimum 10 items per factor (source >= 10, destination >= 10)
- All retained items satisfy BOTH criteria: a >= 0.4 AND |b| <= 3.0
- No duplicates in purified_items.csv
- Factor column contains only "source" or "destination"

*Log Validation:*
- Required patterns: "Purification complete: {N} items retained", "Source: {N_source} items, Destination: {N_destination} items", "All factors meet minimum threshold (>= 10 items)"
- Forbidden patterns: "ERROR", "INSUFFICIENT ITEMS", "Factor below minimum threshold"
- Acceptable warnings: "Low retention rate: {percent}% (below typical 70-90% range)" if retention unusually low

**Expected Behavior on Validation Failure:**
- If < 10 items per factor: Raise error "Insufficient items for reliable measurement: Factor {X} has {N} items (minimum 10 required)"
- Log failure to logs/step02_purify_items.log
- Quit script immediately (do NOT proceed to Step 3)
- g_debug invoked to diagnose (common causes: overly strict thresholds, poor calibration in Pass 1, inherently difficult item set)

---

### Step 3: IRT Calibration Pass 2 (Purified Items Only)

**Purpose:** Re-calibrate 2-dimensional GRM on purified items to obtain final theta estimates for LMM analysis

**Dependencies:** Step 2 (requires purified_items.csv), Step 0 (requires irt_input.csv, q_matrix.csv)

**Complexity:** High (~30-45 minutes, 2-factor GRM calibration with 25-32 items, 400 observations)

**Input:**

**File 1:** data/step00_irt_input.csv (from Step 0, subset to retained items only)
**Format:** Wide format (composite_ID x item columns)
**Processing:** Filter columns to only items in purified_items.csv

**File 2:** data/step02_purified_items.csv (from Step 2)
**Format:** List of retained items
**Expected:** 25-32 rows

**File 3:** data/step00_q_matrix.csv (from Step 0, subset to retained items only)
**Format:** Item-by-factor loading matrix
**Processing:** Filter rows to only items in purified_items.csv

**Processing:**

**Model Specification:**
- **Identical to Step 1** except using purified item set only
- **Model Type:** 2-dimensional GRM with correlated factors
- **Factors:** Factor 1 = source memory (retained -U- items), Factor 2 = destination memory (retained -D- items)
- **Prior:** p1_med
- **Estimation:** Variational inference (IWAVE)

**Minimal Settings Testing (CRITICAL):**
- Same protocol as Step 1: Test with minimal settings first (max_iter=50, mc_samples=10, iw_samples=10)
- Validates pipeline before production run (max_iter=200, mc_samples=100, iw_samples=100)

**Expected Improvement:**
- Pass 2 theta estimates should have lower SEs than Pass 1 (better measurement with purified items)
- Factor correlation may differ from Pass 1 (removing poor items changes factor structure)

**Output:**

**File 1:** data/step03_item_parameters.csv
**Format:** CSV, final item parameters from Pass 2
**Columns:**
  - `item_tag` (string, item identifier)
  - `factor` (string, "source" or "destination")
  - `a` (float, discrimination parameter)
  - `b` (float, difficulty parameter)
**Expected Rows:** 25-32 items (purified set)

**File 2:** data/step03_theta_scores.csv (CRITICAL for downstream LMM)
**Format:** CSV, final ability estimates
**Columns:**
  - `composite_ID` (string, matches irt_input.csv)
  - `theta_source` (float, source memory ability, final estimates for LMM)
  - `theta_destination` (float, destination memory ability, final estimates for LMM)
  - `se_source` (float, standard error for source theta)
  - `se_destination` (float, standard error for destination theta)
**Expected Rows:** 400 composite_IDs

**File 3:** data/step03_pass2_diagnostics.txt
**Format:** Plain text, model diagnostics
**Contents:**
  - Convergence status
  - Final ELBO value
  - Factor correlation estimate
  - Comparison to Pass 1 (SE reduction, ELBO improvement)

**Validation Requirement:**

Validation tools MUST be used after IRT Pass 2 calibration tool execution. Specific validation tools will be determined by rq_tools based on analysis type (IRT convergence validation, parameter bounds validation, theta reliability validation, Pass 1 vs Pass 2 comparison).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_item_parameters.csv: 25-32 rows x 4 columns (item_tag: object, factor: object, a: float64, b: float64)
- data/step03_theta_scores.csv: 400 rows x 5 columns (composite_ID: object, theta_source/destination: float64, se_source/destination: float64)
- data/step03_pass2_diagnostics.txt: Text file with convergence info

*Value Ranges:*
- Discrimination (a) in [0.4, 10.0] (purified set should have a >= 0.4 by design)
- Difficulty (b) in [-6.0, 6.0] (purified set should have |b| <= 3.0 for most items)
- Theta (source, destination) in [-4, 4] (outside range indicates convergence issues)
- Standard errors (se_source, se_destination) in [0.1, 1.5] (Pass 2 SEs should be <= Pass 1 SEs)

*Data Quality:*
- All purified items present in item_parameters.csv (25-32 items, no items dropped)
- All 400 composite_IDs present in theta_scores.csv (no participants excluded)
- No NaN values in item parameters or theta estimates
- SE improvement: Mean(se_source_pass2) <= Mean(se_source_pass1), same for destination
- Factor correlation between source and destination in [-1, 1]

*Log Validation:*
- Required patterns: "Model converged: True", "Pass 2 complete: {N} items", "SE reduction vs Pass 1: source {X}%, destination {Y}%"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "NaN parameters detected"
- Acceptable warnings: "SE reduction modest (<10%)" (purification may not always improve precision dramatically)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Pass 2 SEs higher than Pass 1 - purification degraded measurement")
- Log failure to logs/step03_irt_calibration_pass2.log
- Quit script immediately (do NOT proceed to Step 4)
- g_debug invoked to diagnose (common causes: overly aggressive purification removed informative items, numerical instability)

---

### Step 4: Merge Theta Scores with TSVR Time Variable (Decision D070)

**Purpose:** Merge final theta estimates with TSVR_hours (actual time since encoding) and reshape to long format for LMM analysis

**Dependencies:** Step 3 (requires theta_scores.csv), Step 0 (requires tsvr_mapping.csv)

**Complexity:** Low (~2 minutes, merge and reshape operations only)

**Input:**

**File 1:** data/step03_theta_scores.csv (from Step 3)
**Format:** Wide format, 400 rows x 5 columns
**Columns:** composite_ID, theta_source, theta_destination, se_source, se_destination

**File 2:** data/step00_tsvr_mapping.csv (from Step 0)
**Format:** TSVR mapping, 400 rows x 4 columns
**Columns:** composite_ID, UID, test, TSVR_hours

**Processing:**

**Step 4a: Merge Theta with TSVR**
- **Merge Key:** composite_ID (must match exactly between files)
- **Merge Type:** Inner join (all 400 composite_IDs should match)
- **Null Handling:** If any composite_ID missing TSVR_hours, raise error (validation failure)

**Step 4b: Reshape Wide to Long for LocationType Factor**
- **Current Format:** Wide (1 row per composite_ID, 2 theta columns: theta_source, theta_destination)
- **Target Format:** Long (2 rows per composite_ID, 1 theta column, 1 LocationType column)
- **Reshape Logic:**
  - Each composite_ID becomes 2 rows (source, destination)
  - LocationType factor created: "source" (reference level, coded 0), "destination" (coded 1)
  - theta column created by stacking theta_source and theta_destination
  - se column created by stacking se_source and se_destination

**Step 4c: Create Time Transformations**
- **Days:** TSVR_hours / 24 (convert hours to days for interpretability)
- **log_Days_plus1:** log(Days + 1) (logarithmic time transformation, +1 to avoid log(0))
- **Days_squared:** Days^2 (quadratic time transformation)

**Step 4d: Treatment Coding**
- **LocationType factor:** Source = 0 (reference level), Destination = 1 (treatment level)
- **Rationale:** Tests hypothesis that destination memory differs from source memory (source as baseline)

**Output:**

**File:** data/step04_lmm_input.csv
**Format:** CSV, long format for LMM analysis
**Columns:**
  - `UID` (string, participant identifier)
  - `test` (string, test session: T1, T2, T3, T4)
  - `composite_ID` (string, original composite ID)
  - `TSVR_hours` (float, actual time since encoding in hours, Decision D070)
  - `Days` (float, TSVR_hours / 24)
  - `log_Days_plus1` (float, log(Days + 1))
  - `Days_squared` (float, Days^2)
  - `LocationType` (string, "source" or "destination")
  - `LocationType_coded` (int, 0=source, 1=destination, for LMM contrasts)
  - `theta` (float, ability estimate, stacked from theta_source and theta_destination)
  - `se` (float, standard error, stacked from se_source and se_destination)
**Expected Rows:** 800 (400 composite_IDs x 2 location types)

**Validation Requirement:**

Validation tools MUST be used after merge and reshape tool execution. Specific validation tools will be determined by rq_tools based on operation type (merge validation, reshape validation, time transformation validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_lmm_input.csv: 800 rows x 11 columns (UID: object, test: object, composite_ID: object, TSVR_hours: float64, Days: float64, log_Days_plus1: float64, Days_squared: float64, LocationType: object, LocationType_coded: int64, theta: float64, se: float64)

*Value Ranges:*
- TSVR_hours in [0, 168] (0=encoding, 168=1 week maximum)
- Days in [0, 7] (TSVR_hours / 24)
- log_Days_plus1 in [-inf, log(8)] (log(0+1)=0 at encoding, log(7+1)=2.08 at 1 week)
- Days_squared in [0, 49] (0^2 to 7^2)
- LocationType in {"source", "destination"} (categorical)
- LocationType_coded in {0, 1} (binary treatment coding)
- theta in [-4, 4] (inherited from IRT calibration)
- se in [0.1, 1.5] (inherited from IRT calibration)

*Data Quality:*
- Exactly 800 rows (400 composite_IDs x 2 location types, no data loss)
- All 400 composite_IDs matched between theta and TSVR files (no missing merges)
- Each UID appears exactly 8 times (4 tests x 2 location types)
- LocationType balanced: 400 source rows, 400 destination rows
- No NaN values in TSVR_hours, Days, time transformations, theta, se, LocationType
- All time transformations computed correctly (Days = TSVR_hours/24 verified by sampling)

*Log Validation:*
- Required patterns: "Merge complete: 400 composite_IDs matched", "Reshape complete: 800 rows created", "LocationType balanced: 400 source, 400 destination", "Time transformations validated"
- Forbidden patterns: "ERROR", "MERGE FAILED", "MISSING TSVR", "NaN values detected in time transformations"
- Acceptable warnings: None expected for merge/reshape operations

**Expected Behavior on Validation Failure:**
- If < 400 composite_IDs matched: Raise error "Merge incomplete: {N} composite_IDs missing TSVR_hours"
- If row count != 800: Raise error "Reshape failed: Expected 800 rows, got {N}"
- Log failure to logs/step04_merge_theta_tsvr.log
- Quit script immediately (do NOT proceed to Step 5)
- g_debug invoked to diagnose (common causes: composite_ID mismatch between files, reshape logic error)

---

### Step 5: Linear Mixed Model Selection (5 Candidate Time Transformations)

**Purpose:** Fit 5 candidate LMMs with LocationType x Time interactions, select best model via AIC comparison

**Dependencies:** Step 4 (requires lmm_input.csv)

**Complexity:** Medium (~5-10 minutes, 5 LMM fits with random slopes)

**Input:**

**File:** data/step04_lmm_input.csv (from Step 4)
**Format:** Long format, 800 rows x 11 columns
**Expected:** UID, test, TSVR_hours, Days, log_Days_plus1, Days_squared, LocationType, LocationType_coded, theta, se

**Processing:**

**Candidate Models (All with LocationType x Time Interactions):**

All models use TSVR_hours as time variable per Decision D070 (actual hours, not nominal days). Time transformations (Days, log_Days_plus1, Days_squared) are derived from TSVR_hours for interpretability.

**Random Effects Structure:**
- Random intercepts by UID (baseline individual differences)
- Random slopes for Days by UID (individual variation in forgetting rate)
- Random slopes estimated for ALL models (allows individual trajectories to vary)

**Fixed Effects Structures:**

1. **Linear Model:**
   - Formula: `theta ~ Days * LocationType + (Days | UID)`
   - Tests: LocationType main effect, Days main effect, LocationType x Days interaction

2. **Quadratic Model:**
   - Formula: `theta ~ (Days + Days_squared) * LocationType + (Days | UID)`
   - Tests: Nonlinear time trajectory (quadratic curvature) with LocationType moderation

3. **Logarithmic Model:**
   - Formula: `theta ~ log_Days_plus1 * LocationType + (log_Days_plus1 | UID)`
   - Tests: Logarithmic forgetting curve (rapid early decline, plateau) with LocationType moderation

4. **Linear + Logarithmic Model:**
   - Formula: `theta ~ (Days + log_Days_plus1) * LocationType + (Days | UID)`
   - Tests: Combined linear and logarithmic time effects with LocationType moderation

5. **Quadratic + Logarithmic Model:**
   - Formula: `theta ~ (Days + Days_squared + log_Days_plus1) * LocationType + (Days | UID)`
   - Tests: Comprehensive time model with all transformations

**Model Fitting:**
- **Estimation:** REML=False (for AIC comparison, REML not comparable across fixed effects)
- **Convergence:** Monitor convergence warnings, require successful convergence for all 5 models
- **AIC Computation:** Extract AIC from each fitted model

**Model Selection:**
- **Compute delta_AIC:** AIC_model - min(AIC) across all 5 models
- **Compute Akaike weights:** exp(-0.5 * delta_AIC) / sum(exp(-0.5 * delta_AIC)) across models
- **Best Model:** Model with lowest AIC (delta_AIC = 0, highest Akaike weight)
- **Quality Threshold:** Best model weight > 0.30 indicates clear winner (not merely least bad)

**Output:**

**File 1:** data/step05_model_comparison.csv
**Format:** CSV, model comparison table
**Columns:**
  - `model_name` (string, e.g., "Linear", "Quadratic", "Logarithmic", "Linear+Logarithmic", "Quadratic+Logarithmic")
  - `AIC` (float, Akaike Information Criterion)
  - `delta_AIC` (float, AIC - min(AIC))
  - `weight` (float, Akaike weight, evidence ratio)
**Expected Rows:** 5 (one per candidate model)
**Expected:** Weights sum to 1.0 +/- 0.01 (numerical precision check)

**File 2:** data/step05_lmm_fitted_model.pkl
**Format:** Pickle file (serialized statsmodels MixedLM result object)
**Contents:** Best-fitting LMM (lowest AIC) saved for downstream analysis
**Note:** Used in Step 6 for post-hoc contrasts

**File 3:** data/step05_lmm_summary.txt
**Format:** Plain text, best model summary
**Contents:**
  - Model formula
  - Fixed effects table (coefficients, SE, z, p-values)
  - Random effects variance components
  - Model fit indices (AIC, BIC, log-likelihood)
  - Convergence status

**Validation Requirement:**

Validation tools MUST be used after LMM model selection tool execution. Specific validation tools will be determined by rq_tools based on analysis type (LMM convergence validation, AIC comparison validation, Akaike weights validation, model assumptions validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_model_comparison.csv: 5 rows x 4 columns (model_name: object, AIC: float64, delta_AIC: float64, weight: float64)
- data/step05_lmm_fitted_model.pkl: Binary pickle file (statsmodels result object)
- data/step05_lmm_summary.txt: Text file with model summary

*Value Ranges:*
- AIC values: Positive real numbers (typical range: [1000, 3000] for N=800)
- delta_AIC in [0, inf] (best model has delta_AIC = 0)
- Akaike weights in [0, 1] (probabilities)
- Sum of Akaike weights = 1.0 +/- 0.01 (numerical precision)
- Best model weight > 0.30 (quality threshold for clear winner)

*Data Quality:*
- All 5 models converged successfully (no convergence warnings in logs)
- All 5 models have finite AIC values (no NaN or inf)
- Exactly one model has delta_AIC = 0 (best model identified uniquely)
- Weights monotonically decrease as delta_AIC increases (ordering check)

*Log Validation:*
- Required patterns: "5 models fitted successfully", "Best model: {model_name} (weight={weight:.3f})", "All models converged", "Akaike weights sum: 1.000 +/- 0.01"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "NaN AIC detected", "Model {X} did not converge"
- Acceptable warnings: "Model {X} has low weight (<0.05) - poor fit" (some models expected to fit poorly)

**Expected Behavior on Validation Failure:**
- If any model fails to converge: Raise error "Model {name} did not converge - check random effects structure"
- If best model weight <= 0.30: Raise warning "No clear winner: Best model weight = {weight:.3f} (threshold 0.30) - model uncertainty high"
- If Akaike weights sum != 1.0 +/- 0.01: Raise error "Akaike weight computation error: sum = {sum:.4f}"
- Log failure to logs/step05_fit_lmm.log
- Quit script immediately (do NOT proceed to Step 6)
- g_debug invoked to diagnose (common causes: singular fit, random effects misspecification, insufficient data for complex models)

---

### Step 6: Post-Hoc Hypothesis Tests with Dual P-Value Reporting (Decision D068)

**Purpose:** Test LocationType main effect and LocationType x Time interaction from best LMM with dual p-value reporting (uncorrected + Bonferroni)

**Dependencies:** Step 5 (requires lmm_fitted_model.pkl, model_comparison.csv)

**Complexity:** Low (~2 minutes, extract fixed effects and compute contrasts)

**Input:**

**File 1:** data/step05_lmm_fitted_model.pkl (from Step 5)
**Format:** Pickle file (statsmodels MixedLM result object)

**File 2:** data/step05_model_comparison.csv (from Step 5)
**Format:** CSV with best model identification

**Processing:**

**Hypothesis Tests:**

**Primary Test 1: LocationType Main Effect**
- **Null Hypothesis:** Source and destination memory do not differ (averaged across time)
- **Coefficient:** LocationType_coded main effect coefficient from best LMM
- **Interpretation:** Positive coefficient = destination > source, Negative = source > destination
- **Expected Direction:** Negative (source > destination per hypothesis)
- **Alpha:** 0.025 (Bonferroni-corrected for 2 primary tests: main effect + interaction)

**Primary Test 2: LocationType x Time Interaction**
- **Null Hypothesis:** Source and destination have same forgetting rate over time
- **Coefficient:** LocationType_coded x Time interaction coefficient (Time = Days, log_Days_plus1, or other depending on best model)
- **Interpretation:** Significant interaction = differential forgetting trajectories
- **Expected Direction:** Negative (destination forgetting faster than source per hypothesis)
- **Alpha:** 0.025 (Bonferroni-corrected)

**Effect Sizes:**
- **Compute effect sizes at Days 0, 1, 3, 6** using marginal means from best LMM
- **Cohen's d:** Standardized mean difference between source and destination at each timepoint
- **95% Confidence Intervals:** Delta method or bootstrap for CI estimation

**Dual P-Value Reporting (Decision D068):**
- **p_uncorrected:** Raw p-value from LMM fixed effects table
- **p_bonferroni:** Bonferroni-corrected p-value (p_uncorrected x 2 for 2 primary tests)
- **Rationale:** Exploratory thesis, transparent reporting of both uncorrected and corrected inferences

**Output:**

**File 1:** data/step06_post_hoc_contrasts.csv
**Format:** CSV, hypothesis test results
**Columns:**
  - `test_name` (string, e.g., "LocationType_main_effect", "LocationType_x_Time_interaction")
  - `coefficient` (float, fixed effect estimate from best LMM)
  - `SE` (float, standard error of coefficient)
  - `z` (float, z-statistic)
  - `p_uncorrected` (float, raw p-value)
  - `p_bonferroni` (float, Bonferroni-corrected p-value, p_uncorrected x 2)
  - `CI_lower` (float, 95% CI lower bound)
  - `CI_upper` (float, 95% CI upper bound)
**Expected Rows:** 2 (LocationType main effect, LocationType x Time interaction)

**File 2:** data/step06_effect_sizes.csv
**Format:** CSV, effect sizes at each timepoint
**Columns:**
  - `timepoint` (string, "Day0", "Day1", "Day3", "Day6")
  - `source_mean` (float, marginal mean theta for source at timepoint)
  - `destination_mean` (float, marginal mean theta for destination at timepoint)
  - `mean_difference` (float, source_mean - destination_mean)
  - `cohens_d` (float, standardized effect size)
  - `CI_lower` (float, 95% CI for mean difference)
  - `CI_upper` (float, 95% CI for mean difference)
**Expected Rows:** 4 (one per timepoint: Days 0, 1, 3, 6)

**Validation Requirement:**

Validation tools MUST be used after post-hoc contrasts tool execution. Specific validation tools will be determined by rq_tools based on analysis type (dual p-value validation per D068, effect size bounds validation, CI coverage validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_post_hoc_contrasts.csv: 2 rows x 8 columns (test_name: object, coefficient: float64, SE: float64, z: float64, p_uncorrected: float64, p_bonferroni: float64, CI_lower: float64, CI_upper: float64)
- data/step06_effect_sizes.csv: 4 rows x 7 columns (timepoint: object, source_mean: float64, destination_mean: float64, mean_difference: float64, cohens_d: float64, CI_lower: float64, CI_upper: float64)

*Value Ranges:*
- p-values (uncorrected, bonferroni) in [0, 1] (probabilities)
- p_bonferroni = p_uncorrected x 2 (capped at 1.0)
- z-statistics: Unrestricted real numbers
- Cohen's d typically in [-2, 2] (values >2 suggest very large effects or errors)
- CI_lower < CI_upper for all confidence intervals
- Marginal means (source_mean, destination_mean) in [-4, 4] (theta scale)

*Data Quality:*
- Exactly 2 hypothesis tests (main effect, interaction)
- Exactly 4 effect size rows (Days 0, 1, 3, 6)
- All p-values are non-NaN (statistical tests completed)
- Bonferroni correction applied correctly (p_bonferroni verified by sampling)
- Effect direction consistency: If hypothesis supported, mean_difference negative at all timepoints (source > destination)

*Log Validation:*
- Required patterns: "LocationType main effect: coefficient={coef:.3f}, p_uncorrected={p:.4f}, p_bonferroni={p_b:.4f}", "LocationType x Time interaction: coefficient={coef:.3f}, p_uncorrected={p:.4f}, p_bonferroni={p_b:.4f}", "Effect sizes computed for 4 timepoints", "Decision D068 dual p-values validated"
- Forbidden patterns: "ERROR", "NaN p-value detected", "CI computation failed"
- Acceptable warnings: "Interaction not significant (p_bonferroni > 0.05)" (interaction may or may not be present)

**Expected Behavior on Validation Failure:**
- If p-values NaN: Raise error "Hypothesis test failed: NaN p-value for {test_name}"
- If Bonferroni correction incorrect: Raise error "Bonferroni p-value mismatch: Expected {p_uncorrected x 2}, got {p_bonferroni}"
- If effect size computation fails: Raise error "Effect size computation failed at {timepoint}: NaN Cohen's d"
- Log failure to logs/step06_compute_post_hoc_contrasts.log
- Quit script immediately (do NOT proceed to Step 7)
- g_debug invoked to diagnose (common causes: model did not converge properly, marginal means extraction error, CI computation error)

---

### Step 7: Prepare Trajectory Plot Data (Decision D069 Dual-Scale)

**Purpose:** Create plot source CSVs on theta scale and probability scale for trajectory visualization (Decision D069 dual-scale requirement)

**Dependencies:** Step 5 (requires lmm_fitted_model.pkl), Step 6 (requires effect_sizes.csv for verification)

**Complexity:** Low (~2 minutes, data aggregation and transformation only)

**Input:**

**File 1:** data/step05_lmm_fitted_model.pkl (from Step 5)
**Format:** Pickle file (best LMM)

**File 2:** data/step06_effect_sizes.csv (from Step 6, contains marginal means)
**Format:** CSV with source_mean, destination_mean at Days 0, 1, 3, 6

**Processing:**

**Theta-Scale Plot Data:**
- Extract marginal means for source and destination at Days 0, 1, 3, 6 from best LMM
- Compute 95% confidence intervals using delta method or model predictions
- Structure: 8 rows (2 location types x 4 timepoints)

**Probability-Scale Plot Data (Decision D069):**
- Transform theta to probability scale using IRT 2PL formula: P(correct) = 1 / (1 + exp(-a * (theta - b)))
- Use average item difficulty (b_mean) and discrimination (a_mean) from Pass 2 item parameters
- Transform marginal means: theta -> P(correct)
- Transform confidence intervals: CI_lower_theta -> P(correct_lower), CI_upper_theta -> P(correct_upper)
- Structure: 8 rows (2 location types x 4 timepoints)

**Validation Checks:**
- Probability values must be in [0, 1]
- No NaN values tolerated
- All location types present (source, destination)
- All timepoints present (Days 0, 1, 3, 6)

**Output:**

**File 1:** data/step07_trajectory_theta_data.csv
**Format:** CSV, plot source data on theta scale
**Columns:**
  - `LocationType` (string, "source" or "destination")
  - `Days` (float, 0, 1, 3, 6)
  - `theta_mean` (float, marginal mean theta at timepoint)
  - `CI_lower` (float, lower 95% CI bound on theta scale)
  - `CI_upper` (float, upper 95% CI bound on theta scale)
**Expected Rows:** 8 (2 location types x 4 timepoints)

**File 2:** data/step07_trajectory_probability_data.csv
**Format:** CSV, plot source data on probability scale (Decision D069)
**Columns:**
  - `LocationType` (string, "source" or "destination")
  - `Days` (float, 0, 1, 3, 6)
  - `prob_mean` (float, transformed theta to P(correct))
  - `CI_lower` (float, lower 95% CI on probability scale)
  - `CI_upper` (float, upper 95% CI on probability scale)
**Expected Rows:** 8 (2 location types x 4 timepoints)

**Validation Requirement:**

Validation tools MUST be used after plot data preparation tool execution. Specific validation tools will be determined by rq_tools based on data type (theta range validation, probability bounds validation, completeness validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_trajectory_theta_data.csv: 8 rows x 5 columns (LocationType: object, Days: float64, theta_mean: float64, CI_lower: float64, CI_upper: float64)
- data/step07_trajectory_probability_data.csv: 8 rows x 5 columns (LocationType: object, Days: float64, prob_mean: float64, CI_lower: float64, CI_upper: float64)

*Value Ranges:*
- Theta scale: theta_mean in [-4, 4], CI_lower in [-4, 4], CI_upper in [-4, 4]
- Probability scale: prob_mean in [0, 1], CI_lower in [0, 1], CI_upper in [0, 1]
- Days in {0, 1, 3, 6} (exact timepoints)
- CI_lower < theta_mean < CI_upper (ordering on theta scale)
- CI_lower < prob_mean < CI_upper (ordering on probability scale)

*Data Quality:*
- Exactly 8 rows per file (2 location types x 4 timepoints)
- All location types present: "source" (4 rows), "destination" (4 rows)
- All timepoints present: Days 0, 1, 3, 6 (2 rows each)
- No NaN values in any column (complete data)
- No duplicate rows (LocationType x Days combinations unique)

*Log Validation:*
- Required patterns: "Plot data preparation complete: 8 rows created per file", "Theta scale validated: all values in [-4, 4]", "Probability scale validated: all values in [0, 1]", "Decision D069 dual-scale requirement satisfied"
- Forbidden patterns: "ERROR", "NaN values detected", "Probability out of bounds [0,1]", "Missing location type or timepoint"
- Acceptable warnings: None expected for plot data preparation

**Expected Behavior on Validation Failure:**
- If probability values out of [0, 1]: Raise error "Probability transformation error: {value} out of bounds [0,1]"
- If row count != 8: Raise error "Plot data incomplete: Expected 8 rows, found {N}"
- If NaN values present: Raise error "NaN values detected in plot data at {location}"
- Log failure to logs/step07_prepare_trajectory_plot_data.log
- Quit script immediately (plot source CSVs invalid, rq_plots cannot proceed)
- g_debug invoked to diagnose (common causes: marginal means extraction error, IRT transformation error, CI computation error)

---

## Expected Data Formats

### Step 0 Output Format

**IRT Input (Wide Format):**
```
composite_ID, TQ_VR_IFR_i1_U, TQ_VR_IFR_i2_U, ..., TQ_VR_IRE_i18_D
P001_T1,      1,               0,               ..., 1
P001_T2,      1,               1,               ..., 0
...
P100_T4,      0,               1,               ..., 1
```
- Rows: 400 (100 participants x 4 tests)
- Columns: 37 (1 composite_ID + 36 items)
- Values: {0, 1, NaN}

**Q-Matrix (Item-by-Factor):**
```
item_tag,             source, destination
TQ_VR_IFR_i1_U,       1,      0
TQ_VR_IFR_i2_U,       1,      0
...
TQ_VR_IRE_i18_D,      0,      1
```
- Rows: 36 items
- Columns: 3 (item_tag, source, destination)
- Values: Factor loadings {0, 1}

**TSVR Mapping:**
```
composite_ID, UID,  test, TSVR_hours
P001_T1,      P001, T1,   0.0
P001_T2,      P001, T2,   24.5
P001_T3,      P001, T3,   72.3
P001_T4,      P001, T4,   144.8
...
```
- Rows: 400
- Columns: 4
- TSVR_hours: Actual elapsed time (not nominal 0/24/72/144)

### Step 4 Output Format (LMM Input, Long Format)

**Transformation: Wide (Step 3, 400 rows) -> Long (Step 4, 800 rows)**

```
UID,  test, composite_ID, TSVR_hours, Days, log_Days_plus1, Days_squared, LocationType, LocationType_coded, theta, se
P001, T1,   P001_T1,      0.0,        0.0,  0.0,            0.0,          source,       0,                  -0.52, 0.18
P001, T1,   P001_T1,      0.0,        0.0,  0.0,            0.0,          destination,  1,                  -0.78, 0.20
P001, T2,   P001_T2,      24.5,       1.02, 0.71,           1.04,         source,       0,                  -0.61, 0.19
P001, T2,   P001_T2,      24.5,       1.02, 0.71,           1.04,         destination,  1,                  -0.85, 0.21
...
```
- Rows: 800 (400 composite_IDs x 2 location types)
- Columns: 11
- Each participant has 8 rows (4 tests x 2 location types)

### Step 7 Output Format (Plot Source CSVs)

**Theta Scale:**
```
LocationType, Days, theta_mean, CI_lower, CI_upper
source,       0,    -0.52,      -0.68,    -0.36
source,       1,    -0.61,      -0.77,    -0.45
source,       3,    -0.74,      -0.90,    -0.58
source,       6,    -0.89,      -1.05,    -0.73
destination,  0,    -0.78,      -0.94,    -0.62
destination,  1,    -0.95,      -1.11,    -0.79
destination,  3,    -1.18,      -1.34,    -1.02
destination,  6,    -1.42,      -1.58,    -1.26
```

**Probability Scale:**
```
LocationType, Days, prob_mean, CI_lower, CI_upper
source,       0,    0.63,      0.58,     0.68
source,       1,    0.59,      0.54,     0.64
source,       3,    0.54,      0.49,     0.59
source,       6,    0.48,      0.43,     0.53
destination,  0,    0.56,      0.51,     0.61
destination,  1,    0.50,      0.45,     0.55
destination,  3,    0.43,      0.38,     0.48
destination,  6,    0.36,      0.31,     0.41
```

---

## Cross-RQ Dependencies

**Dependency Type:** RAW Data Only (No Dependencies)

**This RQ uses:** Only dfData.csv (project-level raw data source)

**No dependencies on other RQs:** Can be executed independently as a ROOT RQ for Type 5.5 (Source-Destination)

**Execution Order:** Flexible (any order within chapter, independent of other RQ types)

**Data Sources:**
- data/cache/dfData.csv - Participant responses (VR episodic memory items)
- TSVR columns from dfData.csv - Timing data (actual hours since encoding)

**Note:** All data extraction uses project-level raw data directly. No intermediate outputs from other RQs required. This RQ establishes foundational source-destination trajectories that downstream RQs in Type 5.5 may reference.

---

## Validation Requirements

**CRITICAL MANDATE:**

Every analysis step in this plan MUST use validation tools after analysis tool execution. This is not optional. This is the core architectural principle preventing cascading failures observed in v3.0 (where analysis errors propagated undetected through 5+ downstream steps before discovery).

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

**Step 0: Extract Source and Destination Location Data**
- **Analysis Tool:** tools.data.extract_vr_items_wide (determined by rq_tools)
- **Validation Tool:** tools.validation.validate_data_format, validate_irt_extraction (determined by rq_tools)
- **Validation Criteria:** See Step 0 "Substance Validation Criteria" section above (4 layers: Output Files, Value Ranges, Data Quality, Log Validation)

**Step 1: IRT Calibration Pass 1**
- **Analysis Tool:** tools.analysis_irt.calibrate_grm (determined by rq_tools)
- **Validation Tool:** tools.validation.validate_irt_convergence, validate_irt_parameters (determined by rq_tools)
- **Validation Criteria:** See Step 1 "Substance Validation Criteria" section above

**Step 2: Purify Items**
- **Analysis Tool:** tools.analysis_irt.filter_items_by_quality (determined by rq_tools)
- **Validation Tool:** tools.validation.validate_irt_parameters, validate_dataframe_structure (determined by rq_tools)
- **Validation Criteria:** See Step 2 "Substance Validation Criteria" section above

**Step 3: IRT Calibration Pass 2**
- **Analysis Tool:** tools.analysis_irt.calibrate_grm (determined by rq_tools)
- **Validation Tool:** tools.validation.validate_irt_convergence, validate_irt_parameters (determined by rq_tools)
- **Validation Criteria:** See Step 3 "Substance Validation Criteria" section above

**Step 4: Merge Theta with TSVR**
- **Analysis Tool:** pandas merge + melt operations (standard library)
- **Validation Tool:** tools.validation.validate_data_format, validate_numeric_range (determined by rq_tools)
- **Validation Criteria:** See Step 4 "Substance Validation Criteria" section above

**Step 5: LMM Model Selection**
- **Analysis Tool:** tools.analysis_lmm.compare_lmm_models_by_aic (determined by rq_tools)
- **Validation Tool:** tools.validation.validate_lmm_convergence, validate_model_convergence (determined by rq_tools)
- **Validation Criteria:** See Step 5 "Substance Validation Criteria" section above

**Step 6: Post-Hoc Contrasts**
- **Analysis Tool:** tools.analysis_lmm.compute_contrasts_pairwise, compute_effect_sizes_cohens (determined by rq_tools)
- **Validation Tool:** tools.validation.validate_contrasts_dual_pvalues, validate_effect_sizes (determined by rq_tools)
- **Validation Criteria:** See Step 6 "Substance Validation Criteria" section above

**Step 7: Prepare Plot Data**
- **Analysis Tool:** tools.plotting.convert_theta_to_probability, pandas aggregation (determined by rq_tools)
- **Validation Tool:** tools.validation.validate_probability_range, validate_plot_data_completeness (determined by rq_tools)
- **Validation Criteria:** See Step 7 "Substance Validation Criteria" section above

**Error Handling Protocol:**
- Validation failure at ANY step -> Script quits immediately -> Error logged to logs/stepN_name.log -> Master invokes g_debug
- g_debug analyzes in sandbox -> Reports solution to master -> Master applies fix -> Re-runs step
- NO step proceeds to next step without validation passing (architectural enforcement)

---

## Summary

**Total Steps:** 8 (Step 0: extraction, Steps 1-7: analysis)

**Estimated Runtime:** ~75-90 minutes
- High-complexity steps: Step 1 (30-45 min), Step 3 (30-45 min) - 2-factor GRM calibrations
- Medium-complexity: Step 5 (5-10 min) - 5 LMM model comparisons
- Low-complexity: Steps 0, 2, 4, 6, 7 (10-15 min total) - Data operations and contrasts

**Cross-RQ Dependencies:** None (ROOT RQ, extracts from dfData.csv)

**Primary Outputs:**
- **IRT outputs:** data/step03_theta_scores.csv (400 rows: final theta estimates by participant x test x 2 dimensions)
- **LMM outputs:** data/step05_lmm_fitted_model.pkl (best-fitting trajectory model), data/step05_model_comparison.csv (5 candidate models with AIC)
- **Hypothesis tests:** data/step06_post_hoc_contrasts.csv (LocationType main effect, LocationType x Time interaction with dual p-values)
- **Effect sizes:** data/step06_effect_sizes.csv (source vs destination at Days 0, 1, 3, 6)
- **Plot source CSVs:** data/step07_trajectory_theta_data.csv, data/step07_trajectory_probability_data.csv (dual-scale per D069)

**Validation Coverage:** 100% (all 8 steps have mandatory validation requirements with 4-layer substance criteria)

**Key Decisions Applied:**
- D039: 2-pass IRT purification with quality thresholds (a >= 0.4, |b| <= 3.0)
- D068: Dual p-value reporting (uncorrected + Bonferroni for transparency)
- D069: Dual-scale trajectory plots (theta + probability for interpretability)
- D070: TSVR_hours as time variable (actual elapsed time, not nominal days)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate - implicit, already approved via concept/scholar/stats)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts
5. Workflow continues to Step 14: Bash executes scripts -> rq_inspect validates outputs
6. Workflow continues to Step 15: rq_plots reads plot source CSVs -> generates trajectory visualizations
7. Workflow continues to Step 16: rq_results summarizes findings -> creates summary.md

---

**Version History:**
- v1.0 (2025-12-04): Initial plan created by rq_planner agent for RQ 5.5.1

---

**End of Analysis Plan**
