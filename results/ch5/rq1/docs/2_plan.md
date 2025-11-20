# Analysis Plan for RQ 5.1: Domain-Specific Forgetting Trajectories (What/Where/When)

**Created by:** rq_planner agent
**Date:** 2025-11-19
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This analysis examines domain-specific differences in episodic forgetting trajectories across three memory domains (What, Where, When) over 6 days. The workflow uses a two-stage IRT → LMM pipeline:

1. **IRT Stage:** 2-pass Graded Response Model (GRM) calibration with 3 correlated factors (What, Where, When) to derive ability estimates (theta scores) per domain for each participant-test combination
2. **LMM Stage:** Linear Mixed Model trajectory analysis with Domain × Time interaction to test differential forgetting rates

**Total Steps:** 8 (step00 through step07)

**Estimated Runtime:** High (~180-240 minutes total across all steps)

**Key Decisions Applied:**
- **Decision D039:** 2-pass IRT purification (Pass 1: all items → purification → Pass 2: retained items)
- **Decision D068:** Dual p-value reporting (uncorrected AND Bonferroni-corrected)
- **Decision D069:** Dual-scale trajectory plots (theta scale AND probability scale)
- **Decision D070:** TSVR as LMM time variable (actual hours since encoding, NOT nominal days 0/1/3/6)

---

## Analysis Plan

### Step 00: Extract VR Item Data

**Dependencies:** None (first step)

**Complexity:** Low (5-10 minutes - data extraction only)

**Input:**

**File:** data/master.xlsx (project-level data source)

**Required Tags:**
- What domain: `*-N-*ANS` (object identity items)
- Where domain: `*-L-*ANS | *-U-*ANS | *-D-*ANS` (spatial location items - ALL three location types)
- When domain: `*-O-*ANS` (temporal order items)

**Paradigms:** All paradigms included (IFR, ICR, IRE, RFR, RRE, TCR)

**Tests:** All 4 tests (T1, T2, T3, T4 = Days 0, 1, 3, 6)

**Expected Data Volume:** ~100 participants × 4 tests = 400 composite observations

**Processing:**

**Method:** Extract VR item responses from master.xlsx using domain-specific tag patterns

**Tag Pattern Details:**
- What tags: `-N-` domain marker (object naming/identity)
- Where tags: `-L-` (legacy general location), `-U-` (pick-up location), `-D-` (put-down location)
- When tags: `-O-` domain marker (temporal order)
- Response suffix: All tags end with `ANS` (answer column)

**Composite ID Construction:**
- Format: `{UID}_{test}` (e.g., `A010_T1`)
- Treats 100 participants × 4 tests as 400 pseudo-participants for IRT calibration
- Standard IRT input format for longitudinal data

**Output:**

**File:** data/step00_irt_input.csv

**Format:** Wide format (composite_ID × item columns)

**Columns:**
- `composite_ID` (string, format: UID_test, e.g., `A010_T1`)
- Item response columns: One column per VR item tag
- Column naming: Full tag retained (e.g., `A010-RVR-T1-IFR-N-i1CM-n1so1fiA-ANS`)

**Expected Dimensions:**
- Rows: ~400 (100 participants × 4 tests)
- Columns: ~103 total (composite_ID + ~102 VR items across all three domains)

**Data Types:**
- composite_ID: object (string)
- Item responses: int64 (ordinal values 0-3, where 0=incorrect, 1-3=correct with varying confidence)

**Validation Requirements (MANDATORY):**

**Methodological Criteria (for validation tools during execution):**
- All 100 participants present (no participants excluded)
- All 4 tests extracted per participant
- Expected item count per domain:
  - What domain (~34 items)
  - Where domain (~34 items - combined -L-, -U-, -D- tags)
  - When domain (~34 items)
- No unexpected NaN patterns (>80% NaN per item suggests extraction error)
- Validation tools MUST be used after extraction tool execution

**Substance Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- step00_irt_input.csv: 400 rows × ~103 columns (composite_ID: object, item columns: int64)

*Value Ranges:*
- Item responses ∈ {0, 1, 2, 3} (ordinal scale, 0=incorrect, 1-3=correct)
- composite_ID format matches `{UID}_{test}` pattern (e.g., A010_T1, A053_T3)

*Data Quality:*
- All 400 composite_IDs present (100 participants × 4 tests, no data loss)
- Item response columns have <20% missing data (some items not administered to all participants is expected)
- No duplicate composite_IDs (data integrity check)
- Column count 100-110 (expected ~103, small variation acceptable due to counterbalancing)

*Log Validation:*
- Log file: logs/step00_extract_vr_data.log must exist
- Required pattern: "Extraction complete: 400 composite_IDs, [N] items extracted"
- Forbidden patterns: "ERROR", "EXTRACTION FAILED"
- Acceptable warnings: "Some items have >20% missing data (expected due to counterbalancing)"

**On Failure:**
- Methodological failure (missing participants, wrong item count) → Validation tool quits, logs error, master invokes g_debug
- Substance failure (rq_inspect detects) → rq_inspect quits with detailed report, master investigates

**Expected Behavior:**
- Extraction completes in <10 minutes
- 400 composite_IDs created (100 participants × 4 tests)
- ~102 item columns extracted across three domains
- Some missing data expected (counterbalancing means not all items administered to all participants)

---

### Step 01: IRT Calibration Pass 1 (All Items)

**Dependencies:** Step 00 complete (requires step00_irt_input.csv)

**Complexity:** High (60-90 minutes for N=400, ~102 items, 3 correlated factors)

**Input:**

**File:** data/step00_irt_input.csv

**Format:** Wide (composite_ID × item columns)

**Required Columns:** composite_ID + ~102 item response columns

**Expected Dimensions:** 400 rows × ~103 columns

**Processing:**

**Method:** Graded Response Model (GRM) calibration

**Model Specification:**
- Model: Multidimensional IRT with 3 correlated factors (What, Where, When)
- Item response format: Polytomous (ordinal values 0-3)
- Factor correlation: Estimated (correlated factors GRM, not orthogonal)
- Dimension mapping:
  - Dimension 1 (What): Items with `-N-` tag
  - Dimension 2 (Where): Items with `-L-`, `-U-`, or `-D-` tags
  - Dimension 3 (When): Items with `-O-` tag
- Epochs: 1000 (standard for GRM convergence with correlated factors)

**Output:**

**File 1:** logs/step01_pass1_item_params.csv

**Columns:**
- `item_name` (object): Full item tag
- `dimension` (object): Factor assignment (What, Where, When)
- `a` (float64): Discrimination parameter
- `b` (float64): Difficulty parameter
- `se_a` (float64): Standard error of discrimination
- `se_b` (float64): Standard error of difficulty

**Dimensions:** ~102 rows (one per item) × 6 columns

**File 2:** logs/step01_pass1_theta.csv

**Columns:**
- `composite_ID` (object)
- `theta_What` (float64): Ability estimate for What dimension
- `theta_Where` (float64): Ability estimate for Where dimension
- `theta_When` (float64): Ability estimate for When dimension
- `se_What` (float64): Standard error for What
- `se_Where` (float64): Standard error for Where
- `se_When` (float64): Standard error for When

**Dimensions:** 400 rows × 7 columns

**Validation Requirements (MANDATORY):**

**Methodological Criteria (for validation tools during execution):**
- Model convergence (gradient norm < 0.01, log-likelihood improved across epochs)
- Fit indices: RMSEA < 0.08, CFI > 0.90, TLI > 0.90
- Local independence: Q3 statistic < 0.2 for all item pairs within dimension
- Factor correlations: All correlations ∈ [-1, 1] (valid correlation matrix)
- Validation tools MUST be used after calibration tool execution

**Substance Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- step01_pass1_item_params.csv: ~102 rows × 6 columns (item_name: object, dimension: object, a: float64, b: float64, se_a: float64, se_b: float64)
- step01_pass1_theta.csv: 400 rows × 7 columns (composite_ID: object, theta_What: float64, theta_Where: float64, theta_When: float64, se_What: float64, se_Where: float64, se_When: float64)

*Value Ranges:*
- theta values ∈ [-4, 4] (outside range indicates calibration problem, typical range is [-3, 3])
- se (standard errors) ∈ [0.1, 1.5] (above 1.5 = unreliable estimates, below 0.1 = suspiciously low)
- discrimination (a) > 0 (negative discrimination impossible in GRM)
- difficulty (b): unrestricted (temporal items can have |b| > 5.0, this is expected)

*Data Quality:*
- All 400 composite_IDs present (100 participants × 4 tests, no data loss)
- No NaN values in theta or se columns (model must estimate for all observations)
- No duplicate composite_IDs (data integrity check)
- Item count: 100-105 items in item_params (expected ~102, some variation acceptable)
- All three dimensions represented in dimension column (What, Where, When)

*Log Validation:*
- Log file: logs/step01_irt_calibration_pass1.log must exist
- Required pattern: "Model converged: True" OR "Convergence achieved"
- Required pattern: "VALIDATION - PASS: theta range check"
- Required pattern: "VALIDATION - PASS: se range check"
- Forbidden patterns: "ERROR", "EXCEPTION", "CONVERGENCE FAILED", "VALIDATION - FAIL"
- Acceptable warnings: "Some items have extreme difficulty |b| > 3.0 (expected for temporal domain per D039)"

**On Failure:**
- Methodological failure (convergence, fit) → Validation tool quits, logs error, master invokes g_debug
- Substance failure (rq_inspect detects) → rq_inspect quits with detailed report, master investigates

**Expected Behavior:**
- GRM calibration converges within 1000 epochs (typical: 400-700 epochs for correlated factors model)
- Item parameters estimated for all ~102 items (no missing)
- Theta scores estimated for all 400 observations (composite_IDs)
- Some temporal items (When domain) show extreme difficulty (|b| > 3.0) - expected, documented in D039
- Factor correlations positive and moderate (0.3-0.7 typical for episodic memory domains)
- Standard errors reasonable (median se_theta ~0.3-0.6 typical for N=400)

---

### Step 02: Item Purification (Decision D039)

**Dependencies:** Step 01 complete (requires logs/step01_pass1_item_params.csv)

**Complexity:** Low (<5 minutes - filtering operation)

**Input:**

**File:** logs/step01_pass1_item_params.csv

**Required Columns:** item_name, dimension, a (discrimination), b (difficulty)

**Expected Dimensions:** ~102 rows × 6 columns

**Processing:**

**Method:** 2-Pass IRT purification per Decision D039

**Thresholds:**
- Discrimination: a ≥ 0.4 (items must discriminate ability levels)
- Difficulty: |b| ≤ 3.0 (exclude extremely easy or extremely hard items)

**Exclusion Logic:**
- Items failing EITHER threshold are removed
- Retain items where (a ≥ 0.4) AND (|b| ≤ 3.0)

**Expected Retention Rate:** 40-60% (temporal items challenging, many exceed |b| > 3.0 per D039 documentation)

**Output:**

**File 1:** data/step02_purified_items.csv

**Columns:**
- `item_name` (object): Full item tag
- `dimension` (object): Factor assignment (What, Where, When)
- `a` (float64): Discrimination parameter (≥0.4 by definition)
- `b` (float64): Difficulty parameter (|b|≤3.0 by definition)

**Expected Dimensions:** ~43-62 rows (42-60% of 102 items) × 4 columns

**File 2:** logs/step02_purification_report.txt

**Content:** Text file listing excluded items with reasons (low discrimination OR extreme difficulty)

**Format Example:**
```
EXCLUDED ITEMS (Decision D039 - 2-Pass Purification)

Total Items: 102
Retained: 51 (50%)
Excluded: 51 (50%)

EXCLUSION REASONS:

Low Discrimination (a < 0.4):
- A010-RVR-T1-IFR-N-i1CM-n1so1fiA-ANS: a=0.32
- [... more items ...]

Extreme Difficulty (|b| > 3.0):
- A010-RVR-T1-TCR-O-o1A-ANS: b=4.2 (temporal item, expected)
- [... more items ...]
```

**Validation Requirements (MANDATORY):**

**Methodological Criteria (for validation tools during execution):**
- At least 10 items retained PER dimension (minimum for stable IRT estimation in Pass 2)
- No dimension completely eliminated (all 3 dimensions must have items)
- Retention rate within expected bounds (30-70% acceptable per D039)
- Validation tools MUST be used after purification

**Substance Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- step02_purified_items.csv: 43-62 rows × 4 columns (item_name: object, dimension: object, a: float64, b: float64)
- step02_purification_report.txt: text file with exclusion summary

*Value Ranges:*
- discrimination (a) ≥ 0.4 (by definition - purification threshold enforced)
- difficulty (b): |b| ≤ 3.0 (by definition - purification threshold enforced)
- Retention rate: 30-70% (outside range may indicate problem with thresholds or data)

*Data Quality:*
- Row count: 43-62 items (42-60% of 102 expected, based on D039 documentation)
- All retained items have valid a and b (no NaN values)
- No duplicate item_names (each item appears once)
- Dimension distribution: At least 10 items per dimension (What ≥10, Where ≥10, When ≥10)

*Log Validation:*
- Log file: logs/step02_purify_items.log must exist
- Required pattern: "Purification complete: [N] items retained, [M] items excluded"
- Required pattern: "Dimension distribution: What=[N1], Where=[N2], When=[N3]"
- Required pattern: "All dimensions have ≥10 items" (dimension balance check)
- Forbidden patterns: "ERROR", "Dimension eliminated (0 items)", "Retention rate <30% or >70%"
- Acceptable warnings: "Temporal domain (When) has lower retention [X]% due to extreme difficulty (expected per D039)"

**On Failure:**
- Methodological failure (<10 items per dimension) → Validation tool quits, master may need to relax thresholds
- Substance failure (rq_inspect detects) → rq_inspect quits with detailed report, master investigates

**Expected Behavior:**
- Temporal items (When domain) have lowest retention rate (~30-40% typical due to high difficulty)
- Spatial items (Where domain) have moderate retention (~50-60% typical)
- Object items (What domain) have highest retention (~60-70% typical)
- Overall retention ~50% (51 items retained from 102 items)
- All 3 dimensions have sufficient items (minimum 10 per dimension, typical 14-20 per dimension)
- Excluded items documented in purification_report.txt with reasons

---

### Step 03: IRT Calibration Pass 2 (Purified Items)

**Dependencies:** Step 02 complete (requires data/step02_purified_items.csv)

**Complexity:** High (45-75 minutes for N=400, ~51 items, 3 correlated factors)

**Input:**

**File 1:** data/step00_irt_input.csv (original wide-format data)

**File 2:** data/step02_purified_items.csv (list of items to include in Pass 2)

**Processing:**

**Method:** Graded Response Model (GRM) calibration on purified item set

**Model Specification:**
- Same as Pass 1: Multidimensional IRT with 3 correlated factors
- Item set: ONLY items listed in step02_purified_items.csv
- Expected items: ~51 items (50% retention from Pass 1)
- Filter step00_irt_input.csv to include only purified item columns
- Epochs: 1000 (same as Pass 1)

**Output:**

**File 1:** data/step03_item_parameters.csv

**Columns:**
- `item_name` (object): Full item tag
- `dimension` (object): Factor assignment (What, Where, When)
- `a` (float64): Discrimination parameter (final)
- `b` (float64): Difficulty parameter (final)
- `se_a` (float64): Standard error of discrimination
- `se_b` (float64): Standard error of difficulty

**Dimensions:** ~51 rows (one per purified item) × 6 columns

**File 2:** data/step03_theta_scores.csv

**Columns:**
- `composite_ID` (object)
- `theta_What` (float64): Final ability estimate for What dimension
- `theta_Where` (float64): Final ability estimate for Where dimension
- `theta_When` (float64): Final ability estimate for When dimension
- `se_What` (float64): Standard error for What
- `se_Where` (float64): Standard error for Where
- `se_When` (float64): Standard error for When

**Dimensions:** 400 rows × 7 columns

**Validation Requirements (MANDATORY):**

**Methodological Criteria (for validation tools during execution):**
- Model convergence (same criteria as Pass 1)
- Fit indices: RMSEA ≤ Pass 1 (improved or equal), CFI ≥ Pass 1, TLI ≥ Pass 1
- Improved fit vs Pass 1 expected (purification removes misfitting items)
- Theta reliability: se_theta < 0.7 for 90% of observations (reasonable precision)
- Validation tools MUST be used after calibration

**Substance Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- step03_item_parameters.csv: ~51 rows × 6 columns (item_name: object, dimension: object, a: float64, b: float64, se_a: float64, se_b: float64)
- step03_theta_scores.csv: 400 rows × 7 columns (composite_ID: object, theta_What: float64, theta_Where: float64, theta_When: float64, se_What: float64, se_Where: float64, se_When: float64)

*Value Ranges:*
- theta values ∈ [-4, 4] (same as Pass 1)
- se (standard errors) ∈ [0.1, 1.0] (tighter than Pass 1 due to purified items)
- discrimination (a) ≥ 0.4 (by definition - purification threshold)
- difficulty (b): |b| ≤ 3.0 (by definition - purification threshold)

*Data Quality:*
- All 400 composite_IDs present (same as Pass 1, no data loss)
- No NaN values in theta or se columns
- No duplicate composite_IDs
- Item count matches purified items (~51 items)
- All three dimensions represented

*Log Validation:*
- Log file: logs/step03_irt_calibration_pass2.log must exist
- Required pattern: "Model converged: True"
- Required pattern: "Fit improved vs Pass 1: RMSEA decreased by [X]"
- Required pattern: "VALIDATION - PASS: theta range check"
- Required pattern: "90% of observations have se_theta < 0.7"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "Fit worse than Pass 1"

**On Failure:**
- Methodological failure (convergence, fit worse than Pass 1) → Validation tool quits, master invokes g_debug
- Substance failure (rq_inspect detects) → rq_inspect quits with detailed report

**Expected Behavior:**
- Convergence faster than Pass 1 (~300-500 epochs typical for purified items)
- Improved model fit (RMSEA decreased by 0.01-0.03 typical)
- Lower standard errors (median se_theta ~0.25-0.45, vs 0.3-0.6 in Pass 1)
- Final theta scores ready for LMM analysis
- Factor correlations similar to Pass 1 (0.3-0.7 range maintained)

---

### Step 04: Merge Theta Scores with TSVR (Decision D070)

**Dependencies:** Step 03 complete (requires data/step03_theta_scores.csv)

**Complexity:** Low (5-10 minutes - data merging and reshaping)

**Input:**

**File 1:** data/step03_theta_scores.csv

**Format:** Wide format (one row per composite_ID)

**Columns:** composite_ID, theta_What, theta_Where, theta_When, se_What, se_Where, se_When

**Expected Dimensions:** 400 rows × 7 columns

**File 2:** data/master.xlsx (TSVR lookup)

**Required Tags:** `{UID}-RVR-{T1|T2|T3|T4}-STA-X-TSVR` (Time Since VR in hours)

**Processing:**

**Method:** Merge theta scores with TSVR time variable per Decision D070

**TSVR Extraction:**
1. Extract `{UID}-RVR-{test}-STA-X-TSVR` tags from master.xlsx for each UID × test combination
2. Parse composite_ID to extract UID and test (e.g., `A010_T1` → UID=`A010`, test=`T1`)
3. Lookup TSVR_hours per UID × test combination
4. CRITICAL: Use TSVR_hours (actual elapsed time), NOT nominal days (0, 1, 3, 6)

**Reshape Logic:**
1. Merge theta_scores.csv with TSVR lookup on composite_ID (adds TSVR_hours column)
2. Reshape wide → long format for LMM:
   - Wide: One row per composite_ID (theta_What, theta_Where, theta_When in separate columns)
   - Long: Three rows per composite_ID (one per domain), with `domain` and `theta` columns
3. Parse composite_ID to create UID and test columns
4. Add domain factor column (What, Where, When)

**Output:**

**File:** data/step04_lmm_input.csv

**Format:** Long format (one row per measurement occasion × domain)

**Columns:**
- `UID` (object): Participant identifier (e.g., `A010`)
- `test` (object): Test session (T1, T2, T3, T4)
- `TSVR_hours` (float64): Time Since VR in hours (actual elapsed time)
- `domain` (object): Memory domain factor (What, Where, When)
- `theta` (float64): IRT ability estimate for given domain
- `se` (float64): Standard error of theta estimate

**Expected Dimensions:** 1200 rows (400 composite_IDs × 3 domains) × 6 columns

**Validation Requirements (MANDATORY):**

**Methodological Criteria (for validation tools during execution):**
- All 400 composite_IDs successfully matched to TSVR (no missing TSVR values)
- TSVR range check: 0-200 hours (7-day study, allowing some variation)
- No NaN values in TSVR_hours column (merge must be complete)
- Reshape verification: 1200 rows = 400 composite_IDs × 3 domains
- Validation tools MUST be used after merge/reshape

**Substance Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- step04_lmm_input.csv: 1200 rows × 6 columns (UID: object, test: object, TSVR_hours: float64, domain: object, theta: float64, se: float64)

*Value Ranges:*
- TSVR_hours ∈ [0, 200] (typical range 0-168 for 7-day study, allowing buffer)
- theta ∈ [-4, 4] (same range as IRT output)
- se ∈ [0.1, 1.0] (same range as IRT output)
- test ∈ {T1, T2, T3, T4} (four test sessions)
- domain ∈ {What, Where, When} (three domains)

*Data Quality:*
- Exactly 1200 rows (400 composite_IDs × 3 domains)
- All 100 participants present (100 unique UIDs)
- All 4 tests present per participant (4 tests per UID)
- No NaN values in TSVR_hours, theta, or se columns
- No duplicate UID × test × domain combinations

*Log Validation:*
- Log file: logs/step04_merge_theta_tsvr.log must exist
- Required pattern: "Merge successful: 400/400 composite_IDs matched to TSVR"
- Required pattern: "Reshape complete: 1200 rows created (400 × 3 domains)"
- Required pattern: "VALIDATION - PASS: TSVR range check [0-200 hours]"
- Forbidden patterns: "ERROR", "Missing TSVR values", "Data loss during merge/reshape"

**On Failure:**
- Methodological failure (missing TSVR, merge failure) → Validation tool quits, master invokes g_debug
- Substance failure (rq_inspect detects) → rq_inspect quits with detailed report

**Expected Behavior:**
- All 400 composite_IDs match to TSVR (100% merge success)
- TSVR_hours range: 0 (T1, immediate) to ~144-168 hours (T4, 6-7 days)
- Reshape to long format creates 1200 rows (3× original composite_IDs)
- Domain factor ready for LMM Domain × Time interaction
- TSVR_hours used as continuous time variable (NOT nominal days 0/1/3/6)

---

### Step 05: Fit LMM with TSVR Time Variable (Decision D070)

**Dependencies:** Step 04 complete (requires data/step04_lmm_input.csv)

**Complexity:** Medium (20-40 minutes for model fitting and comparison)

**Input:**

**File:** data/step04_lmm_input.csv

**Format:** Long format (one row per observation × domain)

**Required Columns:** UID, test, TSVR_hours, domain, theta, se

**Expected Dimensions:** 1200 rows × 6 columns

**Processing:**

**Method:** Fit Linear Mixed Model with Domain × Time interaction

**Model Specification:**

**Fixed Effects:**
- TSVR_hours (continuous time variable - Decision D070)
- domain (categorical factor with 3 levels: What, Where, When)
- TSVR_hours × domain interaction (tests differential forgetting rates)

**Coding Scheme:**
- Treatment coding with What as reference domain
- When domain compared to What: tests if temporal memory forgetting differs from object memory
- Where domain compared to What: tests if spatial memory forgetting differs from object memory

**Random Effects:**
- Random intercept per participant: (1 | UID)
- Random slope per participant for TSVR_hours: (TSVR_hours | UID)
- Allows individual differences in baseline ability and forgetting rate

**Model Fitting:**
- Use REML=False for model comparison (AIC requires ML estimation)
- Fit 5 candidate models (linear, quadratic, logarithmic, linear+log, quadratic+log)
- Compare via AIC, select best model
- Compute Akaike weights for model selection confidence

**Output:**

**File 1:** results/step05_lmm_model_summary.txt

**Content:**
- Fixed effects estimates (coefficients, SE, t-statistics, p-values)
- Random effects variance components
- Model fit indices (AIC, BIC, log-likelihood)
- Sample size and degrees of freedom
- R² (marginal and conditional)

**File 2:** results/step05_lmm_model_comparison.csv

**Columns:**
- `model` (object): Model name (linear, quadratic, log, linear+log, quadratic+log)
- `AIC` (float64): Akaike Information Criterion
- `delta_AIC` (float64): AIC difference from best model
- `Akaike_weight` (float64): Model selection weight (sums to 1.0)
- `selected` (bool): Best model flag (True for lowest AIC)

**Dimensions:** 5 rows (one per candidate model) × 5 columns

**File 3:** data/step05_lmm_residuals.csv

**Columns:**
- `UID` (object)
- `test` (object)
- `domain` (object)
- `fitted` (float64): Model-predicted theta
- `residual` (float64): Observed - predicted theta

**Dimensions:** 1200 rows × 5 columns

**Validation Requirements (MANDATORY):**

**Methodological Criteria (for validation tools during execution):**
- Model convergence: All 5 candidate models converge successfully
- Residual normality: Shapiro-Wilk test p > 0.05 for best model residuals
- Homoscedasticity: Levene test p > 0.05 (equal variance across groups)
- No autocorrelation: Durbin-Watson statistic 1.5-2.5 for best model
- Best model selection: delta_AIC > 2 for non-selected models (clear winner)
- Validation tools MUST be used after LMM fitting

**Substance Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- step05_lmm_model_summary.txt: text file with model output
- step05_lmm_model_comparison.csv: 5 rows × 5 columns (model: object, AIC: float64, delta_AIC: float64, Akaike_weight: float64, selected: bool)
- step05_lmm_residuals.csv: 1200 rows × 5 columns (UID: object, test: object, domain: object, fitted: float64, residual: float64)

*Value Ranges:*
- Fixed effect coefficients: -2 to +2 (typical range for standardized theta outcomes)
- p-values ∈ [0, 1]
- AIC: positive values (lower is better)
- delta_AIC ≥ 0 (by definition, best model has delta_AIC=0)
- Akaike_weight ∈ [0, 1], sum across models = 1.0
- Residuals approximately N(0, σ²) (mean ~0, SD <1 typical)

*Data Quality:*
- All 5 models converged (no convergence failures)
- Exactly 1 model marked as selected (selected=True)
- Best model has delta_AIC = 0.0
- Residuals have no extreme outliers (|residual| < 4 for 99% of observations)
- N = 1200 observations used in model (no data loss)

*Log Validation:*
- Log file: logs/step05_fit_lmm.log must exist
- Required pattern: "All 5 candidate models converged successfully"
- Required pattern: "Best model: [model_name] (AIC=[value])"
- Required pattern: "VALIDATION - PASS: Residual normality (Shapiro-Wilk p=[value])"
- Required pattern: "VALIDATION - PASS: Homoscedasticity (Levene p=[value])"
- Forbidden patterns: "ERROR", "Model failed to converge", "Assumption violation: autocorrelation detected"

**On Failure:**
- Methodological failure (convergence, assumptions violated) → Validation tool quits, master invokes g_debug
- Substance failure (rq_inspect detects) → rq_inspect quits with detailed report

**Expected Behavior:**
- All 5 models converge within 20-40 minutes total
- Best model likely linear+log or quadratic (non-linear forgetting typical)
- Significant Domain × TSVR_hours interaction (p < 0.001 expected per hypothesis)
- Random effects show individual variability in forgetting rates
- Residuals normally distributed with no patterns (assumptions met)
- Clear model selection (best model delta_AIC=0, others delta_AIC>2)

---

### Step 06: Compute Post-Hoc Contrasts (Decision D068)

**Dependencies:** Step 05 complete (requires fitted LMM model)

**Complexity:** Low (5-10 minutes - contrast computation and correction)

**Input:**

**File:** Best LMM model from Step 05 (loaded from memory/results)

**Required:** Fitted model object with Domain × TSVR_hours interaction terms

**Processing:**

**Method:** Post-hoc pairwise contrasts with dual p-value reporting per Decision D068

**Contrasts:**
1. When vs What: Tests if temporal memory forgetting differs from object memory
2. Where vs What: Tests if spatial memory forgetting differs from object memory
3. When vs Where: Tests if temporal memory forgetting differs from spatial memory

**Multiple Testing Correction:**
- Bonferroni correction: α = 0.05 / 3 = 0.0167 (3 pairwise comparisons)
- Report BOTH uncorrected AND Bonferroni-corrected p-values (Decision D068)
- Rationale: Exploratory thesis, transparent reporting of both significance criteria

**Effect Sizes:**
- Cohen's d for domain differences at each time point (Days 0, 1, 3, 6)
- Partial η² for Domain × Time interaction term
- Compute for both theta scale and probability scale (dual-scale per D069)

**Output:**

**File 1:** results/step06_post_hoc_contrasts.csv

**Columns:**
- `contrast` (object): Comparison name (e.g., "When vs What", "Where vs What", "When vs Where")
- `estimate` (float64): Contrast estimate (difference in slopes)
- `SE` (float64): Standard error of estimate
- `t_statistic` (float64): t-statistic for test
- `p_uncorrected` (float64): Uncorrected p-value
- `p_bonferroni` (float64): Bonferroni-corrected p-value (p_uncorrected × 3)
- `significant_uncorrected` (bool): p_uncorrected < 0.05
- `significant_bonferroni` (bool): p_bonferroni < 0.05

**Dimensions:** 3 rows (one per contrast) × 8 columns

**File 2:** results/step06_effect_sizes.csv

**Columns:**
- `domain_pair` (object): Domain comparison (e.g., "When vs What")
- `timepoint` (object): Test session (T1, T2, T3, T4)
- `cohens_d_theta` (float64): Effect size on theta scale
- `cohens_d_probability` (float64): Effect size on probability scale
- `interpretation` (object): Effect size interpretation (small/medium/large)

**Dimensions:** 12 rows (3 contrasts × 4 timepoints) × 5 columns

**Validation Requirements (MANDATORY):**

**Methodological Criteria (for validation tools during execution):**
- All 3 contrasts computed successfully
- Both p-value columns present (uncorrected AND Bonferroni)
- Bonferroni correction applied correctly (p_bonferroni = p_uncorrected × 3, capped at 1.0)
- Effect sizes computed for all 12 domain × timepoint combinations
- Validation tools MUST be used after contrast computation

**Substance Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- step06_post_hoc_contrasts.csv: 3 rows × 8 columns (contrast: object, estimate: float64, SE: float64, t_statistic: float64, p_uncorrected: float64, p_bonferroni: float64, significant_uncorrected: bool, significant_bonferroni: bool)
- step06_effect_sizes.csv: 12 rows × 5 columns (domain_pair: object, timepoint: object, cohens_d_theta: float64, cohens_d_probability: float64, interpretation: object)

*Value Ranges:*
- estimate: -2 to +2 (typical range for theta scale differences)
- SE > 0 (standard errors must be positive)
- t_statistic: unrestricted (can be large for strong effects)
- p_uncorrected ∈ [0, 1]
- p_bonferroni ∈ [0, 1] (capped at 1.0 even if uncorrected × 3 > 1.0)
- cohens_d_theta: -3 to +3 (typical range, |d| > 0.8 = large effect)
- cohens_d_probability: -3 to +3

*Data Quality:*
- Exactly 3 contrasts present (When vs What, Where vs What, When vs Where)
- Both p-value columns have valid values (no NaN)
- p_bonferroni ≥ p_uncorrected (correction increases p-values)
- Exactly 12 effect size rows (3 contrasts × 4 timepoints)
- interpretation matches Cohen's d thresholds (|d| < 0.2 = small, 0.2-0.8 = medium, >0.8 = large)

*Log Validation:*
- Log file: logs/step06_compute_post_hoc_contrasts.log must exist
- Required pattern: "All 3 contrasts computed successfully"
- Required pattern: "Dual p-value reporting: uncorrected AND Bonferroni (Decision D068)"
- Required pattern: "Effect sizes computed: 12 domain × timepoint combinations"
- Forbidden patterns: "ERROR", "Contrast computation failed"

**On Failure:**
- Methodological failure (contrast computation error) → Validation tool quits, master invokes g_debug
- Substance failure (rq_inspect detects) → rq_inspect quits with detailed report

**Expected Behavior:**
- All 3 contrasts computed successfully
- Significant When vs What contrast expected (p < 0.001 uncorrected, likely p < 0.05 Bonferroni)
- Significant Where vs What contrast possible (moderate effect expected)
- When vs Where contrast may be non-significant (smaller difference expected)
- Effect sizes increase over time (divergence hypothesis: larger d at T4 than T1)
- Dual p-value columns enable transparent reporting (Decision D068)

---

### Step 07: Prepare Trajectory Plot Data (Option B Architecture, Decision D069)

**⚠️ CRITICAL NOTE:** Plot data preparation IS an analysis step. It:
- Gets executed in Step 14 CODE EXECUTION LOOP (g_code → bash → rq_inspect)
- Has validation requirements (same as any analysis step)
- Outputs to plots/*.csv (not data/*.csv) but still validated by rq_inspect
- Created by g_code during analysis (NOT by rq_plots during visualization)

**Dependencies:** Step 05 complete (LMM fitted), Step 03 complete (theta scores)

**Complexity:** Low (5-10 minutes - data aggregation)

**Input:**

**File 1:** data/step03_theta_scores.csv (theta estimates per composite_ID)

**File 2:** data/step04_lmm_input.csv (includes TSVR_hours per observation)

**File 3:** results/step05_lmm_residuals.csv (model-predicted values)

**Processing:**

**Method:** Aggregate analysis outputs for trajectory visualization per Option B architecture

**Plot Description:**
- Trajectory plot showing memory ability (theta) over time with 95% confidence bands
- Three lines: What domain, Where domain, When domain
- X-axis: TSVR_hours (time since encoding, 0-168 hours typical)
- Y-axis: theta (ability scale, -3 to +3 typical range)
- Confidence bands: 95% CI computed from observed data (SE-based)

**Aggregation Logic:**
1. Group step04_lmm_input.csv by domain + test
2. Compute mean(theta), SE(theta), 95% CI per group
3. Join with TSVR_hours per test (average TSVR across participants per nominal test)
4. Select required columns: time, theta, CI_lower, CI_upper, domain
5. Create TWO source CSVs per Decision D069 (dual-scale trajectory plots):
   - Theta-scale data: plots/step07_trajectory_theta_data.csv (ability scale)
   - Probability-scale data: plots/step07_trajectory_probability_data.csv (interpretability scale)

**Probability Transformation (for probability-scale CSV):**
- Use inverse logit: `probability = 1 / (1 + exp(-(a * (theta - b))))`
- Apply transformation using item parameters from step03_item_parameters.csv
- Average across items within domain to get domain-level probability

**Output:**

**File 1:** plots/step07_trajectory_theta_data.csv

**Columns:**
- `time` (float64): TSVR hours (average per nominal test, e.g., T1≈0, T2≈24, T3≈72, T4≈144)
- `theta` (float64): Mean theta per domain per timepoint
- `CI_lower` (float64): Lower 95% confidence bound
- `CI_upper` (float64): Upper 95% confidence bound
- `domain` (object): Memory domain (What, Where, When)

**Expected Dimensions:** 12 rows (3 domains × 4 timepoints) × 5 columns

**File 2:** plots/step07_trajectory_probability_data.csv

**Columns:** Same as theta_data.csv, but theta transformed to probability scale (0-1 range)

**Expected Dimensions:** 12 rows × 5 columns

**Validation Requirements (MANDATORY):**

**Methodological Criteria (for validation tools during execution):**
- All domain × test combinations present (12 total: 3 domains × 4 tests)
- TSVR_hours within expected range per test (T1≈0, T2≈20-30, T3≈70-80, T4≈140-150)
- CI_lower < CI_upper for all rows (confidence interval consistency)
- Probability transformation valid (all probabilities ∈ [0, 1])
- Validation tools MUST be used after plot data preparation tool execution

**Substance Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- step07_trajectory_theta_data.csv: 12 rows × 5 columns (time: float64, theta: float64, CI_lower: float64, CI_upper: float64, domain: object)
- step07_trajectory_probability_data.csv: 12 rows × 5 columns (same schema, probability scale)

*Value Ranges:*
- time ∈ [0, 200] (TSVR hours, typical 0-168 for 7-day study)
- theta ∈ [-3, 3] (typical ability range)
- CI_lower ≥ -4, CI_upper ≤ 4 (within plausible theta range)
- CI_lower < CI_upper (consistency check)
- Probability ∈ [0, 1] (by definition)

*Data Quality:*
- Exactly 12 rows per file (3 domains × 4 timepoints)
- All domains present: What, Where, When (3 unique values)
- All timepoints present: 4 unique time values corresponding to T1-T4
- No NaN values in time, theta, CI columns
- Time values increase monotonically per domain (T1 < T2 < T3 < T4)

*Log Validation:*
- Log file: logs/step07_prepare_trajectory_plot_data.log must exist
- Required pattern: "Aggregation successful: 12 rows created (3 domains × 4 timepoints)"
- Required pattern: "Dual-scale CSVs created: theta_data.csv + probability_data.csv (Decision D069)"
- Required pattern: "VALIDATION - PASS: time range check [0-200 hours]"
- Required pattern: "VALIDATION - PASS: CI consistency (lower < upper for all rows)"
- Forbidden patterns: "ERROR", "Data loss during aggregation", "NaN values detected"

**On Failure:**
- Methodological failure (aggregation error, invalid transformation) → Validation tool quits, master invokes g_debug
- Substance failure (rq_inspect detects) → rq_inspect quits with detailed report

**Expected Behavior:**
- 12 rows created (3 domains × 4 timepoints)
- Time values: T1≈0 hrs, T2≈24 hrs, T3≈72 hrs, T4≈144 hrs (averages, some variation)
- Theta decreases over time (forgetting trajectory: What > Where > When expected)
- Confidence intervals widen over time (fewer participants at later sessions, or greater variability)
- Dual-scale CSVs ready for rq_plots agent (Option B: visualization separate from data prep)
- NOTE: PNG generation happens later when rq_plots reads these CSVs (not in this step)

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 00 → Step 01:**
- Input: master.xlsx tags → Output: Wide-format CSV (composite_ID × items)
- Transformation: Tag extraction, composite ID creation (UID_test format)

**Step 01 → Step 02:**
- Input: Pass 1 item parameters → Output: Filtered item list
- Transformation: Apply thresholds (|b|≤3.0, a≥0.4), exclude failing items

**Step 02 → Step 03:**
- Input: Purified item list + original data → Output: Pass 2 IRT results
- Transformation: Re-calibrate GRM on purified item subset

**Step 03 → Step 04:**
- Input: Theta scores (wide) + TSVR lookup → Output: Long-format LMM input
- Transformation: Merge TSVR, reshape wide → long (one row per domain)

**Step 04 → Step 05:**
- Input: Long-format LMM input → Output: Fitted LMM model + residuals
- Transformation: Statistical modeling (no data format change)

**Step 05 → Step 06:**
- Input: Fitted LMM model → Output: Contrasts + effect sizes
- Transformation: Compute pairwise comparisons, apply Bonferroni correction

**Step 05 → Step 07:**
- Input: LMM residuals + theta scores + TSVR → Output: Plot source CSVs
- Transformation: Aggregate by domain × timepoint, compute means + CIs

### Column Naming Conventions

Per names.md (RQ 5.1 conventions):

- `composite_ID` - Primary key for IRT (format: UID_test)
- `UID` - Participant identifier (format: A### with leading zeros)
- `test` - Test session (T1, T2, T3, T4)
- `TSVR_hours` - Time Since VR in hours (Decision D070)
- `theta_<dimension>` - IRT ability estimate (e.g., theta_What, theta_Where, theta_When)
- `se_<dimension>` - Standard error of theta (e.g., se_What)
- `a` - Item discrimination parameter
- `b` - Item difficulty parameter
- `domain` - Memory domain factor (What, Where, When)
- `CI_lower`, `CI_upper` - 95% confidence interval bounds

### Data Type Constraints

**Nullable vs Non-Nullable:**
- composite_ID: Non-nullable (required for all rows)
- UID: Non-nullable (required for all rows)
- TSVR_hours: Non-nullable after Step 04 (merge must succeed)
- theta, se: Non-nullable after IRT calibration (model must estimate)
- Item responses: Nullable in Step 00 (counterbalancing → not all items administered to all participants)

**Valid Ranges:**
- Item responses: {0, 1, 2, 3} (ordinal scale)
- theta: [-4, 4] (typical -3 to +3, allowing buffer)
- se: [0.1, 1.5] (standard errors must be positive, upper limit for quality)
- TSVR_hours: [0, 200] (7-day study, typical 0-168)
- Probability: [0, 1] (by definition)
- p-values: [0, 1] (by definition)

**Categorical Values:**
- test: {T1, T2, T3, T4} (four test sessions)
- domain: {What, Where, When} (three memory domains)
- dimension: {What, Where, When} (IRT factors)

---

## Cross-RQ Dependencies

**This RQ uses:** Only master.xlsx (RAW data extraction)

**No dependencies on other RQs:** Can be executed independently

**Execution order:** Flexible (any order within Chapter 5)

**Data Sources:**
- master.xlsx (Sheet: Data) - VR item responses with domain tags
- master.xlsx (TSVR lookup) - Time Since VR timing data per UID × test

**Note:** All data extraction uses tools reading master.xlsx directly. No intermediate outputs from other RQs required.

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
- g_code (Step 14 workflow) will generate stepNN_*.py scripts with validation function calls
- bash execution (Step 14 workflow) will run analysis → validation → error on validation failure

**Downstream Agent Requirements:**
- **rq_tools:** MUST specify validation tool for EVERY analysis step (no exceptions)
- **rq_analysis:** MUST embed validation tool call for EVERY analysis step (no exceptions)
- **g_code:** MUST generate code with validation function calls (no exceptions)
- **rq_inspect:** MUST verify validation ran successfully (checks logs/stepNN_*.log for validation output)

### Validation Requirements By Step

| Step | Analysis | Methodological Validation | Substance Validation |
|------|----------|---------------------------|----------------------|
| 00 | Extract VR data | 100 participants, 4 tests, ~102 items, <20% missing | File exists, 400 rows, ~103 cols, valid composite_IDs |
| 01 | IRT Pass 1 | Convergence, fit (RMSEA<0.08, CFI>0.90), Q3<0.2 | theta ∈ [-4,4], se ∈ [0.1,1.5], 400 rows, ~102 items |
| 02 | Purification | ≥10 items per dimension, 30-70% retention | File exists, 43-62 rows, a≥0.4, \|b\|≤3.0, all domains present |
| 03 | IRT Pass 2 | Convergence, fit improved vs Pass 1, se<0.7 for 90% | theta ∈ [-4,4], se ∈ [0.1,1.0], 400 rows, ~51 items |
| 04 | TSVR merge | All composite_IDs matched, TSVR ∈ [0,200] | 1200 rows, no NaN in TSVR/theta/se, all UIDs/tests present |
| 05 | LMM fitting | 5 models converge, residual normality, homoscedasticity | Model summary exists, 5 rows in comparison, 1200 residuals |
| 06 | Post-hoc | 3 contrasts, dual p-values, Bonferroni correct | 3 contrasts, 12 effect sizes, p ∈ [0,1], p_bonf ≥ p_uncorr |
| 07 | Plot data prep | 12 rows (3×4), CI_lower < CI_upper, time ∈ [0,200] | 12 rows per CSV, theta ∈ [-3,3], prob ∈ [0,1], no NaN |

**Error Handling Protocol:**
- Validation failure → Step quits → Logs error → Invokes g_debug
- g_debug analyzes in sandbox → Reports solution to master
- Master applies fix → Re-runs step
- NO cascading failures (errors caught at source step)

---

## Summary

**Total Steps:** 8 (step00 through step07)

**Estimated Runtime:** 180-240 minutes total
- Step 00: 5-10 min (extraction)
- Step 01: 60-90 min (Pass 1 IRT)
- Step 02: <5 min (purification)
- Step 03: 45-75 min (Pass 2 IRT)
- Step 04: 5-10 min (TSVR merge)
- Step 05: 20-40 min (LMM fitting)
- Step 06: 5-10 min (contrasts)
- Step 07: 5-10 min (plot data prep)

**Cross-RQ Dependencies:** None (RAW data only from master.xlsx)

**Primary Outputs:**
- data/step03_item_parameters.csv (final IRT item parameters, ~51 items)
- data/step03_theta_scores.csv (final theta scores, 400 observations × 3 domains)
- results/step05_lmm_model_summary.txt (best LMM model with Domain × Time interaction)
- results/step06_post_hoc_contrasts.csv (3 contrasts with dual p-values per D068)
- results/step06_effect_sizes.csv (12 domain × timepoint Cohen's d values)
- plots/step07_trajectory_theta_data.csv (plot source CSV, theta scale)
- plots/step07_trajectory_probability_data.csv (plot source CSV, probability scale per D069)

**Validation Coverage:** 100% (all 8 steps have validation requirements)

**Key Decisions Applied:**
- D039: 2-pass IRT purification (mandatory for all IRT analyses)
- D068: Dual p-value reporting (uncorrected + Bonferroni)
- D069: Dual-scale trajectory plots (theta + probability)
- D070: TSVR as time variable (actual hours, not nominal days)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate - NOTE: This is Step 7 in the v4.X workflow document, not Step 07 in this analysis plan)
2. Workflow continues to Step 11: rq_tools reads this plan → creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml → creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml → generates stepNN_*.py scripts

---

**Version History:**
- v1.0 (2025-11-19): Initial plan created by rq_planner agent for RQ 5.1
