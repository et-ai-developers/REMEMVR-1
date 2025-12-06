# Analysis Plan: RQ 6.8.2 - Source-Destination Calibration

**Research Question:** 6.8.2
**Created:** 2025-12-06
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines metacognitive calibration differences between source (pick-up) and destination (put-down) spatial memories across a 6-day retention interval. Analysis merges IRT-derived accuracy estimates (from Ch5 5.5.1) with confidence estimates (from Ch6 6.8.1), computes calibration as the discrepancy between confidence and accuracy, and tests whether calibration quality differs by location type using Linear Mixed Models.

**Pipeline:** LMM only (no IRT - uses theta scores from prior RQs)
**Steps:** 3 analysis steps (Step 0: merge accuracy + confidence, Step 1: compute calibration, Step 2: test location effects, Step 3: prepare plot data)
**Estimated Runtime:** Low (data manipulation and LMM fitting only, no IRT calibration)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni for LocationType effects)
- Decision D070: TSVR as time variable (actual hours since encoding)

**Cross-RQ Dependencies:**
- Ch5 RQ 5.5.1: Source-destination accuracy theta scores
- Ch6 RQ 6.8.1: Source-destination confidence theta scores

---

## Analysis Plan

### Step 0: Merge Accuracy and Confidence by Location Type

**Dependencies:** None (first step - loads data from prior RQs)
**Complexity:** Low (data merging only)

**Purpose:** Combine IRT-derived accuracy estimates (Ch5 5.5.1) with confidence estimates (Ch6 6.8.1) to enable calibration computation.

**Input:**

**File 1:** results/ch5/5.5.1/data/step03_theta_accuracy_location.csv
**Source:** Ch5 RQ 5.5.1 (Source-Destination Accuracy Trajectories)
**Format:** CSV, long format (one row per UID x TEST x LocationType)
**Columns:**
  - `UID` (string, participant identifier, format: P### with leading zeros)
  - `TEST` (string, test session: T1, T2, T3, T4 for Days 0, 1, 3, 6)
  - `LocationType` (string, values: {Source, Destination})
  - `theta_accuracy` (float, IRT ability estimate for spatial accuracy)
  - `SE_accuracy` (float, standard error of theta_accuracy)
**Expected Rows:** 800 (100 participants x 4 tests x 2 location types)

**File 2:** results/ch6/6.8.1/data/step03_theta_confidence_location.csv
**Source:** Ch6 RQ 6.8.1 (Source-Destination Confidence Trajectories)
**Format:** CSV, long format (one row per UID x TEST x LocationType)
**Columns:**
  - `UID` (string, participant identifier)
  - `TEST` (string, test session)
  - `LocationType` (string, values: {Source, Destination})
  - `theta_confidence` (float, IRT ability estimate for confidence judgments)
  - `SE_confidence` (float, standard error of theta_confidence)
**Expected Rows:** 800 (100 participants x 4 tests x 2 location types)

**Processing:**

**Merge Logic:**
- **Key:** UID x TEST x LocationType (must match exactly between files)
- **Type:** Inner join (keep only matched observations)
- **Expected Match Rate:** 100% (both RQs use identical participant sets and location types)
- **Null Handling:** If any UID x TEST x LocationType missing from either file, log warning but proceed (LMM handles missing data via REML)

**Output:**

**File:** data/step00_accuracy_confidence_merged.csv
**Format:** CSV, long format (one row per UID x TEST x LocationType)
**Columns:**
  - `UID` (string, participant identifier)
  - `TEST` (string, test session: T1, T2, T3, T4)
  - `LocationType` (string, values: {Source, Destination})
  - `theta_accuracy` (float, IRT accuracy estimate)
  - `SE_accuracy` (float, standard error of accuracy)
  - `theta_confidence` (float, IRT confidence estimate)
  - `SE_confidence` (float, standard error of confidence)
**Expected Rows:** 800 (100 participants x 4 tests x 2 location types)

**Validation Requirement:**
Validation tools MUST be used after merge execution. Specific validation tools determined by rq_tools based on merge requirements (likely validate_dataframe_structure for row/column checks, validate_data_format for required columns).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_accuracy_confidence_merged.csv exists (exact path)
- Expected rows: 800 (100 UID x 4 tests x 2 LocationTypes)
- Expected columns: 7 (UID, TEST, LocationType, theta_accuracy, SE_accuracy, theta_confidence, SE_confidence)
- Data types: string (UID, TEST, LocationType), float (theta_accuracy, SE_accuracy, theta_confidence, SE_confidence)

*Value Ranges:*
- theta_accuracy in [-3, 3] (typical IRT ability range)
- theta_confidence in [-3, 3] (typical IRT ability range)
- SE_accuracy in [0.1, 2.0] (standard errors above 2.0 = unreliable estimates)
- SE_confidence in [0.1, 2.0] (standard errors above 2.0 = unreliable estimates)
- LocationType in {Source, Destination} (categorical)
- TEST in {T1, T2, T3, T4} (categorical)

*Data Quality:*
- All 800 observations present (no data loss during merge)
- No NaN values in theta columns (IRT must estimate for all)
- No duplicate UID x TEST x LocationType combinations
- Each UID has exactly 8 rows (4 tests x 2 location types)

*Log Validation:*
- Required pattern: "Merge complete: 800 rows created"
- Required pattern: "All UIDs matched: 100 participants"
- Forbidden patterns: "ERROR", "Missing UIDs", "Merge failed"
- Acceptable warnings: None expected for inner join with identical participant sets

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 800 rows, found 750 - check Ch5 5.5.1 and Ch6 6.8.1 completion")
- Log failure to logs/step00_merge_accuracy_confidence.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause (likely missing theta files or incomplete prior RQs)

---

### Step 1: Compute Calibration per Location Type

**Dependencies:** Step 0 (requires merged accuracy + confidence data)
**Complexity:** Low (standardization and subtraction only)

**Purpose:** Compute calibration = confidence - accuracy after z-standardization within location type.

**Input:**

**File:** data/step00_accuracy_confidence_merged.csv
**Source:** Generated by Step 0
**Format:** CSV, long format
**Columns:** UID, TEST, LocationType, theta_accuracy, SE_accuracy, theta_confidence, SE_confidence
**Expected Rows:** 800

**Processing:**

**Standardization Logic:**
- **Z-standardize theta_accuracy separately for each LocationType** (Source and Destination standardized independently)
  - Z_accuracy_Source = (theta_accuracy - mean_accuracy_Source) / SD_accuracy_Source
  - Z_accuracy_Dest = (theta_accuracy - mean_accuracy_Dest) / SD_accuracy_Dest
- **Z-standardize theta_confidence separately for each LocationType**
  - Z_confidence_Source = (theta_confidence - mean_confidence_Source) / SD_confidence_Source
  - Z_confidence_Dest = (theta_confidence - mean_confidence_Dest) / SD_confidence_Dest
- **Rationale:** Within-location standardization preserves calibration signal by ensuring accuracy and confidence are on same scale within each location type before comparing

**Calibration Computation:**
- **calibration = Z_confidence - Z_accuracy** (computed separately for Source and Destination using respective z-scores)
- **Interpretation:**
  - calibration > 0: Overconfidence (confidence exceeds accuracy)
  - calibration < 0: Underconfidence (accuracy exceeds confidence)
  - calibration ~= 0: Good calibration (confidence matches accuracy)

**Output:**

**File:** data/step01_calibration_by_location.csv
**Format:** CSV, long format
**Columns:**
  - `UID` (string, participant identifier)
  - `TEST` (string, test session)
  - `LocationType` (string, Source or Destination)
  - `theta_accuracy` (float, raw IRT accuracy)
  - `theta_confidence` (float, raw IRT confidence)
  - `Z_accuracy` (float, standardized accuracy within location type)
  - `Z_confidence` (float, standardized confidence within location type)
  - `calibration` (float, Z_confidence - Z_accuracy)
**Expected Rows:** 800

**Validation Requirement:**
Validation tools MUST be used after calibration computation. Specific validation tools determined by rq_tools (likely validate_standardization for z-score checks, validate_numeric_range for calibration bounds).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_calibration_by_location.csv exists
- Expected rows: 800
- Expected columns: 8 (UID, TEST, LocationType, theta_accuracy, theta_confidence, Z_accuracy, Z_confidence, calibration)
- Data types: string (UID, TEST, LocationType), float (theta_accuracy, theta_confidence, Z_accuracy, Z_confidence, calibration)

*Value Ranges:*
- Z_accuracy: mean ~= 0, SD ~= 1 (within each LocationType separately)
- Z_confidence: mean ~= 0, SD ~= 1 (within each LocationType separately)
- calibration typically in [-3, 3] (z-score difference, extreme values possible but rare)

*Data Quality:*
- All 800 rows present (no data loss)
- No NaN values in calibration column
- Standardization verified: For Source subset, mean(Z_accuracy) ~= 0, SD(Z_accuracy) ~= 1
- Standardization verified: For Destination subset, mean(Z_accuracy) ~= 0, SD(Z_accuracy) ~= 1
- Same verification for Z_confidence by location type

*Log Validation:*
- Required pattern: "Calibration computed: 800 observations"
- Required pattern: "Standardization check - Source: mean(Z_accuracy)=X, SD=Y"
- Required pattern: "Standardization check - Destination: mean(Z_accuracy)=X, SD=Y"
- Forbidden patterns: "ERROR", "NaN detected in calibration"
- Acceptable warnings: "Extreme calibration values detected" (if |calibration| > 3 for some observations - not error, just noteworthy)

**Expected Behavior on Validation Failure:**
- Raise error if standardization failed (mean != 0 or SD != 1 within tolerance)
- Log failure to logs/step01_compute_calibration.log
- Quit script immediately
- g_debug invoked to diagnose (likely insufficient variance in accuracy or confidence within location type)

---

### Step 2: Test Location Effects on Calibration

**Dependencies:** Step 1 (requires calibration scores)
**Complexity:** Medium (LMM fitting with 2-way interaction)

**Purpose:** Test whether source vs destination locations differ in calibration using Linear Mixed Model.

**Input:**

**File:** data/step01_calibration_by_location.csv
**Source:** Generated by Step 1
**Format:** CSV, long format
**Columns:** UID, TEST, LocationType, theta_accuracy, theta_confidence, Z_accuracy, Z_confidence, calibration
**Expected Rows:** 800

**Processing:**

**Add TSVR Time Variable (Decision D070):**
- Load TSVR_hours from data/master.xlsx or TSVR lookup table
- Merge with calibration data by UID x TEST
- TSVR_hours represents actual time since encoding (not nominal days 0/1/3/6)

**LMM Specification:**
- **Formula:** calibration ~ LocationType * TSVR_hours + (TSVR_hours | UID)
- **Fixed Effects:**
  - LocationType: Source vs Destination (within-subjects)
  - TSVR_hours: Continuous time variable (actual elapsed hours)
  - LocationType x TSVR_hours: Interaction (does calibration diverge over time by location type?)
- **Random Effects:** Random intercepts and random slopes for TSVR_hours by participant UID
- **Estimation:** REML=True (unbiased variance estimates for final model)

**Hypothesis Tests:**
- **LocationType main effect:** H0: calibration_Source = calibration_Destination (averaged across time)
- **LocationType x TSVR_hours interaction:** H0: calibration trajectories parallel for Source and Destination
- **Report dual p-values per Decision D068:** Uncorrected + Bonferroni correction

**Output:**

**File 1:** data/step02_lmm_calibration_summary.txt
**Format:** Plain text model summary
**Content:** Fixed effects table (coefficients, SE, t, p-values), random effects variance components, fit indices (AIC, BIC, log-likelihood)

**File 2:** data/step02_location_effects.csv
**Format:** CSV
**Columns:**
  - `Effect` (string, e.g., "LocationType", "LocationType:TSVR_hours")
  - `Estimate` (float, coefficient value)
  - `SE` (float, standard error)
  - `t` (float, t-statistic)
  - `p_uncorrected` (float, standard p-value)
  - `p_bonferroni` (float, Bonferroni-corrected p-value per Decision D068)
**Expected Rows:** 4 (Intercept, LocationType, TSVR_hours, LocationType:TSVR_hours)

**File 3:** data/step02_effect_sizes.csv
**Format:** CSV
**Columns:**
  - `Effect` (string)
  - `Cohens_f2` (float, effect size for fixed effects)
**Expected Rows:** 3 (LocationType, TSVR_hours, LocationType:TSVR_hours - excludes intercept)

**Validation Requirement:**
Validation tools MUST be used after LMM fitting. Specific validation tools determined by rq_tools (likely validate_lmm_convergence, validate_lmm_assumptions_comprehensive, validate_hypothesis_test_dual_pvalues per Decision D068).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_lmm_calibration_summary.txt exists
- data/step02_location_effects.csv: 4 rows x 6 columns
- data/step02_effect_sizes.csv: 3 rows x 2 columns
- Data types: string (Effect), float (Estimate, SE, t, p_uncorrected, p_bonferroni, Cohens_f2)

*Value Ranges:*
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1], p_bonferroni >= p_uncorrected (correction cannot decrease p-value)
- Cohens_f2 >= 0 (non-negative effect sizes)
- t-statistics unrestricted (can be positive or negative)

*Data Quality:*
- All 4 fixed effects present (Intercept, LocationType, TSVR_hours, interaction)
- Dual p-values present for ALL effects (Decision D068 compliance)
- No NaN values in coefficients or p-values (indicates convergence failure)
- Model summary includes convergence status ("Converged: True")

*Log Validation:*
- Required pattern: "LMM converged successfully"
- Required pattern: "VALIDATION - PASS: Dual p-values present (Decision D068)"
- Required pattern: "Fixed effects: 4 terms extracted"
- Forbidden patterns: "ERROR", "Convergence failed", "Singular fit"
- Acceptable warnings: "Random effects variance near boundary" (if variance components small but non-zero)

**Expected Behavior on Validation Failure:**
- If convergence fails: Log error, quit, invoke g_debug (likely insufficient data or overparameterized random effects)
- If dual p-values missing: Log error, quit (Decision D068 violation)
- Log all failures to logs/step02_fit_lmm_calibration.log

---

### Step 3: Prepare Calibration Plot Data

**Dependencies:** Steps 1, 2 (requires calibration scores + LMM predictions)
**Complexity:** Low (data aggregation for plotting)

**Purpose:** Aggregate calibration by LocationType x Time for trajectory visualization (Option B: g_code creates plot source CSV, rq_plots visualizes later).

**Plot Description:** Trajectory plot showing calibration over time with separate lines for Source and Destination locations, error bars for 95% CI, horizontal reference line at calibration = 0 (perfect calibration).

**Required Data Sources:**
- data/step01_calibration_by_location.csv (observed calibration scores)
- data/step02_lmm_calibration_summary.txt (fitted model for predictions - optional)

**Aggregation Logic:**
1. Group by LocationType x TEST
2. Compute mean(calibration), 95% CI for each group
3. Convert TEST to TSVR_hours (T1=0, T2=24, T3=72, T4=144 hours approximately - use TSVR lookup for exact values)
4. Select columns: LocationType, TSVR_hours, mean_calibration, CI_lower, CI_upper
5. Sort by LocationType, then TSVR_hours

**Output (Plot Source CSV):** data/step03_calibration_plot_data.csv

**Required Columns:**
- `LocationType` (string, values: Source, Destination)
- `TSVR_hours` (float, time since encoding)
- `mean_calibration` (float, mean calibration per location x time)
- `CI_lower` (float, lower 95% confidence bound)
- `CI_upper` (float, upper 95% confidence bound)

**Expected Rows:** 8 (2 LocationTypes x 4 timepoints)

**Validation Requirement:**
Validation tools MUST be used after plot data preparation. Specific validation tools determined by rq_tools (likely validate_plot_data_completeness, validate_dataframe_structure).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_calibration_plot_data.csv exists
- Expected rows: 8 (2 LocationTypes x 4 timepoints)
- Expected columns: 5 (LocationType, TSVR_hours, mean_calibration, CI_lower, CI_upper)
- Data types: string (LocationType), float (TSVR_hours, mean_calibration, CI_lower, CI_upper)

*Value Ranges:*
- TSVR_hours in [0, 168] (0 = encoding, 168 = 1 week)
- mean_calibration typically in [-2, 2] (z-score scale, extreme values possible but rare)
- CI_lower in [-3, 3], CI_upper in [-3, 3]
- CI_upper > CI_lower for all rows (confidence interval logic)

*Data Quality:*
- Exactly 8 rows (no missing LocationType x Time combinations)
- Both LocationTypes present: Source and Destination
- All 4 timepoints present per location type
- No NaN values in any column
- No duplicate LocationType x TSVR_hours combinations

*Log Validation:*
- Required pattern: "Plot data preparation complete: 8 rows created"
- Required pattern: "All location types represented: Source, Destination"
- Forbidden patterns: "ERROR", "Missing location type", "NaN detected"
- Acceptable warnings: None expected for plot data aggregation

**Expected Behavior on Validation Failure:**
- Raise error if rows != 8 (e.g., "Expected 8 rows, found 6 - missing timepoints for Destination")
- Log failure to logs/step03_prepare_calibration_plot_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- g_debug invoked to diagnose (likely missing data in Step 1 calibration file)

**Plotting Function (rq_plots will call):** Trajectory plot with horizontal reference line at y=0
- rq_plots agent maps this description to tools/plotting.py function (likely plot_trajectory or custom calibration plot)
- Plot reads data/step03_calibration_plot_data.csv
- No data aggregation in rq_plots (visualization only per Option B)
- PNG output saved to plots/ folder by rq_plots

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs - intermediate and final)
- data/step00_accuracy_confidence_merged.csv (from Step 0: merge accuracy + confidence)
- data/step01_calibration_by_location.csv (from Step 1: compute calibration)
- data/step02_lmm_calibration_summary.txt (from Step 2: LMM fit)
- data/step02_location_effects.csv (from Step 2: hypothesis tests with dual p-values)
- data/step02_effect_sizes.csv (from Step 2: Cohen's f-squared)
- data/step03_calibration_plot_data.csv (from Step 3: plot source CSV)

### Logs (ONLY execution logs - .log files capturing stdout/stderr)
- logs/step00_merge_accuracy_confidence.log
- logs/step01_compute_calibration.log
- logs/step02_fit_lmm_calibration.log
- logs/step03_prepare_calibration_plot_data.log

### Plots (EMPTY until rq_plots runs)
- plots/calibration_by_location.png (created by rq_plots, NOT analysis steps)

### Results (EMPTY until rq_results runs)
- results/summary.md (created by rq_results, NOT analysis steps)

---

## Expected Data Formats

### Step 0 Output (Merged Accuracy + Confidence)
**Format:** Long format (one row per UID x TEST x LocationType)
**Example Row:** P001, T1, Source, -0.32, 0.15, 0.41, 0.18
**Column Interpretation:**
- UID: Participant identifier
- TEST: Test session (T1/T2/T3/T4)
- LocationType: Source or Destination
- theta_accuracy: IRT accuracy estimate
- SE_accuracy: Standard error of accuracy
- theta_confidence: IRT confidence estimate
- SE_confidence: Standard error of confidence

### Step 1 Output (Calibration Scores)
**Format:** Long format (one row per UID x TEST x LocationType)
**Example Row:** P001, T1, Source, -0.32, 0.41, -0.15, 0.22, 0.37
**Additional Columns:**
- Z_accuracy: Standardized accuracy (within location type)
- Z_confidence: Standardized confidence (within location type)
- calibration: Z_confidence - Z_accuracy (positive = overconfidence)

### Step 2 Output (LMM Results)
**Location Effects CSV Format:**
| Effect | Estimate | SE | t | p_uncorrected | p_bonferroni |
|--------|----------|----|----|---------------|--------------|
| LocationType | -0.15 | 0.08 | -1.87 | 0.062 | 0.248 |
| TSVR_hours | 0.002 | 0.001 | 2.00 | 0.046 | 0.184 |
| LocationType:TSVR_hours | 0.003 | 0.002 | 1.50 | 0.134 | 0.536 |

**Interpretation:**
- Negative LocationType coefficient: Source shows lower calibration than Destination (less overconfidence)
- Positive interaction: Calibration diverges over time (effect magnifies)

### Step 3 Output (Plot Source CSV)
**Format:** Aggregated means by LocationType x Time
**Example Rows:**
| LocationType | TSVR_hours | mean_calibration | CI_lower | CI_upper |
|--------------|------------|------------------|----------|----------|
| Source | 0 | -0.05 | -0.25 | 0.15 |
| Source | 24 | -0.08 | -0.28 | 0.12 |
| Source | 72 | -0.12 | -0.35 | 0.11 |
| Source | 144 | -0.18 | -0.42 | 0.06 |
| Destination | 0 | 0.10 | -0.12 | 0.32 |
| Destination | 24 | 0.15 | -0.08 | 0.38 |
| Destination | 72 | 0.22 | -0.02 | 0.46 |
| Destination | 144 | 0.30 | 0.05 | 0.55 |

**Pattern Interpretation:**
- Source calibration near 0 or negative (slight underconfidence or good calibration)
- Destination calibration positive and increasing (overconfidence worsens over time)
- Hypothesis supported if this pattern emerges

---

## Cross-RQ Dependencies

**This RQ requires outputs from:**

**RQ 5.5.1** (Source-Destination Accuracy Trajectories)
- File: results/ch5/5.5.1/data/step03_theta_accuracy_location.csv
- Used in: Step 0 (merge accuracy with confidence)
- Rationale: RQ 5.5.1 provides IRT-derived accuracy estimates for source and destination locations. This RQ uses those accuracy scores to compute calibration.

**RQ 6.8.1** (Source-Destination Confidence Trajectories)
- File: results/ch6/6.8.1/data/step03_theta_confidence_location.csv
- Used in: Step 0 (merge confidence with accuracy)
- Rationale: RQ 6.8.1 provides IRT-derived confidence estimates for source and destination locations. This RQ uses those confidence scores to compute calibration.

**Execution Order Constraint:**
1. RQ 5.5.1 must complete first (provides accuracy theta)
2. RQ 6.8.1 must complete second (provides confidence theta)
3. This RQ executes third (merges both to compute calibration)

**Data Source Boundaries:**
- **RAW data:** None (no direct master.xlsx extraction)
- **DERIVED data:** Both inputs are theta scores from prior RQ IRT calibrations
- **Scope:** This RQ does NOT re-calibrate IRT models, uses RQ 5.5.1 and 6.8.1 outputs as fixed inputs

**Validation:**
- Step 0: Check results/ch5/5.5.1/data/step03_theta_accuracy_location.csv exists (EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch6/6.8.1/data/step03_theta_confidence_location.csv exists (EXPECTATIONS ERROR if absent)
- If either file missing -> quit with error -> user must execute dependency RQs first

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

#### Step 0: Merge Accuracy and Confidence

**Analysis Tool:** (determined by rq_tools - likely pandas merge operations)
**Validation Tool:** (determined by rq_tools - likely validate_dataframe_structure, validate_data_format)

**What Validation Checks:**
- Output file exists (data/step00_accuracy_confidence_merged.csv)
- Expected row count (800 rows: 100 UID x 4 tests x 2 LocationTypes)
- Expected column count (7 columns: UID, TEST, LocationType, theta_accuracy, SE_accuracy, theta_confidence, SE_confidence)
- All required columns present with correct data types
- No unexpected NaN patterns (all theta and SE values non-null)
- Value ranges: theta in [-3, 3], SE in [0.1, 2.0]
- All UIDs matched (no data loss during merge)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step00_merge_accuracy_confidence.log
- Quit script immediately
- g_debug invoked to diagnose (likely missing dependency files or incomplete prior RQs)

---

#### Step 1: Compute Calibration

**Analysis Tool:** (determined by rq_tools - likely pandas operations for standardization and subtraction)
**Validation Tool:** (determined by rq_tools - likely validate_standardization, validate_numeric_range)

**What Validation Checks:**
- Output file exists (data/step01_calibration_by_location.csv)
- Expected row count (800 rows)
- Expected column count (8 columns including calibration)
- Standardization verified: mean(Z_accuracy) ~= 0, SD(Z_accuracy) ~= 1 within each LocationType
- Standardization verified: mean(Z_confidence) ~= 0, SD(Z_confidence) ~= 1 within each LocationType
- Calibration values computed (no NaN)
- Calibration typically in [-3, 3] (extreme values logged but not error)

**Expected Behavior on Validation Failure:**
- Raise error if standardization failed
- Log failure to logs/step01_compute_calibration.log
- Quit script immediately
- g_debug invoked to diagnose

---

#### Step 2: Test Location Effects

**Analysis Tool:** (determined by rq_tools - likely fit_lmm_trajectory_tsvr from tools_catalog.md)
**Validation Tool:** (determined by rq_tools - likely validate_lmm_convergence, validate_lmm_assumptions_comprehensive, validate_hypothesis_test_dual_pvalues per Decision D068)

**What Validation Checks:**
- Output files exist (lmm_summary.txt, location_effects.csv, effect_sizes.csv)
- Model converged successfully (log-likelihood not NaN)
- Dual p-values present for ALL effects (Decision D068 compliance)
- Fixed effects table complete (4 rows: Intercept, LocationType, TSVR_hours, interaction)
- Effect sizes non-negative (Cohens_f2 >= 0)
- p-values in [0, 1], p_bonferroni >= p_uncorrected
- LMM assumptions checked: residuals normality, homoscedasticity

**Expected Behavior on Validation Failure:**
- If convergence fails: Log error, quit, invoke g_debug
- If dual p-values missing: Log error, quit (Decision D068 violation)
- Log all failures to logs/step02_fit_lmm_calibration.log

---

#### Step 3: Prepare Plot Data

**Analysis Tool:** (determined by rq_tools - likely pandas groupby and aggregation)
**Validation Tool:** (determined by rq_tools - likely validate_plot_data_completeness, validate_dataframe_structure)

**What Validation Checks:**
- Output file exists (data/step03_calibration_plot_data.csv)
- Expected row count (8 rows: 2 LocationTypes x 4 timepoints)
- Expected column count (5 columns: LocationType, TSVR_hours, mean_calibration, CI_lower, CI_upper)
- Both LocationTypes present (Source, Destination)
- All 4 timepoints present per location type
- No NaN values
- CI_upper > CI_lower for all rows

**Expected Behavior on Validation Failure:**
- Raise error if rows != 8 or missing location types
- Log failure to logs/step03_prepare_calibration_plot_data.log
- Quit script immediately
- g_debug invoked to diagnose

---

## Summary

**Total Steps:** 3 (Step 0: merge, Step 1: calibration, Step 2: LMM, Step 3: plot prep)
**Estimated Runtime:** Low (< 10 minutes total - no IRT calibration, only LMM fitting)
**Cross-RQ Dependencies:** RQ 5.5.1 (accuracy theta), RQ 6.8.1 (confidence theta)
**Primary Outputs:** Calibration scores by location type, LMM results testing LocationType effects, plot data for visualization
**Validation Coverage:** 100% (all 3 analysis steps + 1 plot prep step have validation requirements)

**Key Hypothesis Test:**
- LocationType main effect on calibration (Source vs Destination)
- Expected pattern: Source better calibrated (calibration closer to 0), Destination overconfident (calibration > 0)
- Dual p-values reported per Decision D068 (uncorrected + Bonferroni)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent
