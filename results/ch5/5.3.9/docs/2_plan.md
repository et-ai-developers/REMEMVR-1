# Analysis Plan for RQ 5.3.9: Paradigm x Item Difficulty Interaction

**Created by:** rq_planner agent
**Date:** 2025-12-02
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This analysis examines whether the relationship between item difficulty and forgetting rate varies across retrieval paradigms (Free Recall, Cued Recall, Recognition). Uses cross-classified Linear Mixed Model with crossed random effects for participants (UID) and items (Item) to model item-level response data.

**Pipeline:** Cross-Classified LMM (response-level modeling with crossed random effects)

**Analysis Type:** LMM only (no IRT calibration - uses pre-calibrated item difficulty from RQ 5.3.1)

**Steps:** 5 analysis steps (Step 0: data extraction + Steps 1-4: analysis steps)

**Estimated Runtime:** High (60-120 minutes total)
- Step 0: Low (5 min - data extraction)
- Step 1: Medium (15 min - long-format preparation with item-level expansion)
- Step 2: Low (5 min - variable centering and TSVR merge)
- Step 3: High (45-90 min - cross-classified LMM with large dataset)
- Step 4: Medium (10 min - 3-way interaction extraction and plot data preparation)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni) for 3-way interaction test
- Decision D070: TSVR as time variable (actual hours since encoding, not nominal days)
- No Decision D039 (no IRT calibration in this RQ - reuses RQ 5.3.1 item parameters)
- No Decision D069 (no trajectory plots - this RQ produces interaction plot, not time series)

**Cross-RQ Dependencies:**
- RQ 5.3.1 must complete Step 3 (IRT Pass 2) to provide item difficulty parameters
- RQ 5.3.1 Step 0 provides TSVR mapping for time variable

**Data Structure:**
- Response-level (long format): One row per UID x Test x Item observation
- Expected N: ~100 participants x 4 tests x ~50 items (post-purification) = ~20,000 observations
- Crossed random effects: (Time | UID) allows participant-specific time slopes, (1 | Item) allows item-specific intercepts

**Analysis Focus:**
Tests 3-way interaction Time x Difficulty_c x paradigm at Bonferroni alpha = 0.0033. If significant, extracts paradigm-specific difficulty x time slopes to determine which paradigm shows strongest item difficulty effects on forgetting rate.

---

## Analysis Plan

### Step 0: Extract Item-Level Response Data and Dependencies

**Dependencies:** None (first step)
**Complexity:** Low (5 min - straightforward data extraction)

**Purpose:** Extract raw item-level responses from dfData.csv in long format (one row per UID x Test x Item) and merge with item difficulty parameters from RQ 5.3.1.

**Input:**

**File 1:** data/cache/dfData.csv (project-level raw data)
**Format:** Long format with item-level binary responses (0/1)
**Required Columns:**
  - `UID` (string, participant ID, format: P### with leading zeros)
  - `Test` (string, test session: T1, T2, T3, T4)
  - `Item` (string, item identifier matching RQ 5.3.1 item codes)
  - `Response` (int, binary: 0 = incorrect, 1 = correct, NaN = missing/not administered)
  - `paradigm` (string, values: IFR, ICR, IRE - excludes room-level paradigms RFR, TCR, RRE)

**File 2:** results/ch5/5.3.1/data/step03_item_parameters.csv (DERIVED from RQ 5.3.1 Pass 2)
**Format:** CSV with IRT item parameters post-purification
**Required Columns:**
  - `item_name` (string, item identifier)
  - `dimension` (string, factor name - may be paradigm-specific)
  - `a` (float, discrimination parameter - used for quality verification only)
  - `b` (float, difficulty parameter - PRIMARY predictor variable)

**File 3:** results/ch5/5.3.1/data/step00_tsvr_mapping.csv (DERIVED from RQ 5.3.1 Step 0)
**Format:** CSV mapping composite_ID to actual time
**Required Columns:**
  - `composite_ID` (string, format: UID_test, e.g., P001_T1)
  - `TSVR_hours` (float, actual hours since VR encoding session per Decision D070)

**Filters:**
- Paradigm: Include ONLY IFR, ICR, IRE (exclude RFR, TCR, RRE room-level paradigms)
- Items: Include ONLY items present in RQ 5.3.1 step03_item_parameters.csv (purified items only)
- Tests: All 4 tests (T1, T2, T3, T4)
- Participants: All 100 participants (no exclusions)

**Processing:**

1. Read dfData.csv and filter to item-level paradigms (IFR, ICR, IRE)
2. Read RQ 5.3.1 item_parameters.csv to get purified item list
3. Filter dfData to ONLY items present in item_parameters.csv (removes items excluded during RQ 5.3.1 purification)
4. Merge item difficulty (column `b`) from item_parameters.csv into response data by Item
5. Read TSVR mapping from RQ 5.3.1
6. Verify all required columns present and no unexpected NaN patterns

**Output:**

**File 1:** data/step00_response_level_data.csv
**Format:** Long format (one row per UID x Test x Item observation)
**Columns:**
  - `UID` (string, participant ID)
  - `Test` (string, test session T1/T2/T3/T4)
  - `Item` (string, item identifier)
  - `Response` (int, 0/1/NaN)
  - `paradigm` (string, IFR/ICR/IRE)
  - `Difficulty` (float, item difficulty parameter `b` from RQ 5.3.1)
**Expected Rows:** ~20,000 (100 participants x 4 tests x ~50 purified items)
**Expected Columns:** 6

**File 2:** data/step00_tsvr_mapping.csv
**Format:** Copy of RQ 5.3.1 TSVR mapping for reference
**Columns:** composite_ID, TSVR_hours
**Expected Rows:** 400 (100 participants x 4 tests)

**Validation Requirement:**

Validation tools MUST be used after data extraction tool execution. Specific validation tools will be determined by rq_tools based on extraction type (likely tools.validation.validate_data_format + tools.validation.check_missing_data).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_response_level_data.csv: ~20,000 rows x 6 columns
- Data types: UID (object), Test (object), Item (object), Response (float64 - allows NaN), paradigm (object), Difficulty (float64)
- data/step00_tsvr_mapping.csv: 400 rows x 2 columns
- Data types: composite_ID (object), TSVR_hours (float64)

*Value Ranges:*
- Response in {0, 1, NaN} (binary responses, NaN for missing/not administered)
- paradigm in {IFR, ICR, IRE} (categorical, 3 levels)
- Difficulty typically in [-3, 3] but unrestricted (temporal items may exceed |3.0| per RQ 5.3.1 findings)
- TSVR_hours in [0, 168] hours approximately (0 = encoding, 168 = 1 week)

*Data Quality:*
- All UID values present in data (100 unique participants)
- All Test values present (T1, T2, T3, T4)
- Item count matches RQ 5.3.1 purified items (~40-60 items expected post-purification per D039)
- No duplicate UID x Test x Item combinations (each observation unique)
- Missing data: NaN acceptable in Response column (<30% per item), zero NaN in Difficulty, paradigm, TSVR_hours

*Log Validation:*
- Required pattern: "Extracted {N} item-level observations from dfData.csv"
- Required pattern: "Merged difficulty for {M} items from RQ 5.3.1"
- Required pattern: "TSVR mapping loaded: 400 rows (100 participants x 4 tests)"
- Forbidden patterns: "ERROR", "Item mismatch", "Missing difficulty values"
- Acceptable warnings: "NaN responses detected in {K} observations" (expected for missing/not-administered items)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected IFR/ICR/IRE paradigms only, found RFR")
- Log failure to logs/step00_extract_data.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause (likely RQ 5.3.1 dependency issue or dfData.csv format change)

---

### Step 1: Create Composite ID and Expand to Analysis Format

**Dependencies:** Step 0 (requires response_level_data.csv)
**Complexity:** Medium (15 min - large dataset reshaping with item-level expansion)

**Purpose:** Create composite_ID identifier (UID_Test format) and verify data structure for cross-classified LMM modeling.

**Input:**

**File:** data/step00_response_level_data.csv
**Format:** Long format (UID x Test x Item observations)
**Columns:** UID, Test, Item, Response, paradigm, Difficulty
**Expected Rows:** ~20,000

**Processing:**

1. Create composite_ID column: Concatenate UID + "_" + Test (e.g., "P001_T1")
2. Verify paradigm assignment: Each Item should belong to ONLY one paradigm (IFR, ICR, or IRE)
3. Check for duplicate UID x Test x Item observations (should be none)
4. Create long-format analysis file ready for LMM (all columns present)
5. Sort by UID, Test, Item for reproducibility

**Output:**

**File:** data/step01_analysis_ready.csv
**Format:** Long format with composite_ID
**Columns:**
  - `composite_ID` (string, format: UID_Test, e.g., P001_T1)
  - `UID` (string, participant ID - for random effects grouping)
  - `Test` (string, test session - for later TSVR merge)
  - `Item` (string, item identifier - for random effects grouping)
  - `Response` (float, 0/1/NaN)
  - `paradigm` (string, IFR/ICR/IRE)
  - `Difficulty` (float, item difficulty from RQ 5.3.1)
**Expected Rows:** ~20,000 (unchanged from input)
**Expected Columns:** 7 (added composite_ID)

**Validation Requirement:**

Validation tools MUST be used after composite_ID creation tool execution. Specific validation tools determined by rq_tools (likely tools.validation.validate_data_format).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_analysis_ready.csv: ~20,000 rows x 7 columns
- Data types: composite_ID (object), UID (object), Test (object), Item (object), Response (float64), paradigm (object), Difficulty (float64)

*Value Ranges:*
- composite_ID format: "{UID}_{Test}" (e.g., P001_T1, P001_T2, etc.)
- All other columns: Same ranges as Step 0

*Data Quality:*
- composite_ID: 400 unique values (100 participants x 4 tests)
- No duplicate UID x Test x Item combinations
- Each Item belongs to exactly ONE paradigm (verify Item -> paradigm mapping is many-to-one)
- Row count unchanged from Step 0 input (~20,000)

*Log Validation:*
- Required pattern: "Created composite_ID for {N} observations"
- Required pattern: "Verified paradigm assignment: {M} items, 3 paradigms"
- Forbidden patterns: "ERROR", "Duplicate observations", "Item assigned to multiple paradigms"
- Acceptable warnings: None expected for this step

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Item X assigned to both IFR and ICR paradigms")
- Log failure to logs/step01_create_composite_id.log
- Quit script immediately
- g_debug invoked to diagnose

---

### Step 2: Center Difficulty Variable and Merge TSVR Time

**Dependencies:** Step 1 (requires analysis_ready.csv)
**Complexity:** Low (5 min - simple variable transformation and merge)

**Purpose:** Grand-mean center item difficulty predictor (Difficulty_c = Difficulty - mean[Difficulty]) and merge TSVR time variable per Decision D070.

**Input:**

**File 1:** data/step01_analysis_ready.csv
**Format:** Long format with composite_ID
**Columns:** composite_ID, UID, Test, Item, Response, paradigm, Difficulty
**Expected Rows:** ~20,000

**File 2:** data/step00_tsvr_mapping.csv
**Format:** CSV with TSVR hours per composite_ID
**Columns:** composite_ID, TSVR_hours
**Expected Rows:** 400 (100 participants x 4 tests)

**Processing:**

1. Compute grand mean of Difficulty across all items: mean_difficulty = mean(Difficulty)
2. Create centered variable: Difficulty_c = Difficulty - mean_difficulty
3. Verify centering: Check that mean(Difficulty_c) is approximately 0 (within ±0.01 tolerance)
4. Merge TSVR_hours from tsvr_mapping.csv by composite_ID (left join - keep all response observations)
5. Verify no missing TSVR_hours after merge (all composite_IDs should match)
6. Create Time variable from TSVR_hours (rename for LMM clarity: Time = TSVR_hours)

**Output:**

**File:** data/step02_lmm_input.csv
**Format:** Long format ready for cross-classified LMM
**Columns:**
  - `composite_ID` (string)
  - `UID` (string, for random effects grouping)
  - `Test` (string, retained for reference)
  - `Item` (string, for random effects grouping)
  - `Response` (float, 0/1/NaN - dependent variable)
  - `paradigm` (string, IFR/ICR/IRE - fixed effect factor)
  - `Difficulty` (float, raw difficulty - for reference)
  - `Difficulty_c` (float, centered difficulty - PRIMARY predictor)
  - `Time` (float, TSVR_hours - continuous time predictor per D070)
**Expected Rows:** ~20,000 (unchanged)
**Expected Columns:** 9 (added Difficulty_c and Time)

**Validation Requirement:**

Validation tools MUST be used after centering and merge tool execution. Specific validation tools determined by rq_tools (likely tools.validation.validate_standardization for centering + tools.validation.check_missing_data for merge).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_lmm_input.csv: ~20,000 rows x 9 columns
- Data types: All object/float64 as specified above

*Value Ranges:*
- Difficulty_c: Centered around 0 (mean within ±0.01 of zero)
- Time in [0, 168] hours approximately (actual TSVR per D070)
- All other columns: Same ranges as prior steps

*Data Quality:*
- mean(Difficulty_c) in [-0.01, 0.01] (successful centering)
- No NaN values in Difficulty_c column (centering should not introduce NaN)
- No NaN values in Time column (all composite_IDs matched in merge)
- Row count unchanged (~20,000)

*Log Validation:*
- Required pattern: "Grand mean difficulty: {value}"
- Required pattern: "Centered difficulty: mean(Difficulty_c) = {value near 0}"
- Required pattern: "Merged TSVR: {N} composite_IDs matched (100%)"
- Forbidden patterns: "ERROR", "Missing TSVR values", "Centering failed"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "mean(Difficulty_c) = 0.35, expected ~0")
- Log failure to logs/step02_center_merge.log
- Quit script immediately
- g_debug invoked to diagnose

---

### Step 3: Fit Cross-Classified LMM with 3-Way Interaction

**Dependencies:** Step 2 (requires lmm_input.csv)
**Complexity:** High (45-90 min - large dataset with crossed random effects computationally intensive)

**Purpose:** Fit cross-classified Linear Mixed Model testing 3-way interaction Time x Difficulty_c x paradigm with crossed random effects for participants (UID) and items (Item).

**Input:**

**File:** data/step02_lmm_input.csv
**Format:** Long format with centered predictors
**Columns:** composite_ID, UID, Test, Item, Response, paradigm, Difficulty_c, Time
**Expected Rows:** ~20,000
**Note:** NaN values in Response column are acceptable (missing data handled by statsmodels/pymer4)

**Processing:**

**Model Formula:**
```
Response ~ Time * Difficulty_c * paradigm + (Time | UID) + (1 | Item)
```

**Fixed Effects:**
- Time (continuous, hours since encoding per D070)
- Difficulty_c (continuous, centered item difficulty)
- paradigm (categorical, 3 levels: IFR, ICR, IRE - reference level determined by alphabetical order)
- All 2-way interactions: Time:Difficulty_c, Time:paradigm, Difficulty_c:paradigm
- 3-way interaction: Time:Difficulty_c:paradigm (PRIMARY hypothesis test)

**Random Effects:**
- (Time | UID): Random intercepts and slopes for Time by participant (allows individual forgetting rates)
- (1 | Item): Random intercepts by item (accounts for item-specific baseline difficulty beyond IRT parameters)

**Estimation Method:**
- Use pymer4 (supports crossed random effects via lme4 backend)
- REML estimation (default for variance component estimation)
- Convergence tolerance: Default (may require adjustment if convergence issues arise)

**Convergence Strategy:**
Per rq_stats validation feedback (11 concerns, 3 CRITICAL improvements):
1. Initial fit: Standard formula with full random effects structure
2. If convergence fails: Simplify random structure to (1 | UID) + (1 | Item) (intercepts only)
3. If still fails: Test uncorrelated random effects (Time || UID) instead of correlated (Time | UID)
4. If all fail: Report convergence failure, document attempted strategies, invoke g_debug

**Output:**

**File 1:** data/step03_lmm_model_summary.txt
**Format:** Text file with full model summary
**Contents:**
- Fixed effects table (coefficient, SE, z-value, p-value for each term)
- Random effects variance components (UID intercept, UID slope, Item intercept, residual)
- Model fit indices (AIC, BIC, log-likelihood)
- Convergence status and warnings
**Expected Size:** 5-10 KB text file

**File 2:** data/step03_fixed_effects.csv
**Format:** CSV with fixed effects coefficients
**Columns:**
  - `term` (string, predictor name)
  - `estimate` (float, coefficient)
  - `SE` (float, standard error)
  - `z_value` (float, z-statistic)
  - `p_uncorrected` (float, uncorrected p-value per D068)
  - `p_bonferroni` (float, Bonferroni-corrected p-value per D068)
**Expected Rows:** ~15 (intercept + 3 main effects + 3 two-way interactions + 1 three-way interaction + paradigm dummy coding = 10-15 terms)
**Note:** 3-way interaction terms (Time:Difficulty_c:paradigmICR, Time:Difficulty_c:paradigmIRE) are PRIMARY hypothesis tests

**File 3:** data/step03_random_effects.csv
**Format:** CSV with random effects variance components
**Columns:**
  - `component` (string, e.g., "UID_intercept", "UID_slope_Time", "Item_intercept", "Residual")
  - `variance` (float, variance estimate)
  - `SD` (float, standard deviation)
**Expected Rows:** 4 (UID intercept, UID slope, Item intercept, Residual)

**Validation Requirement:**

Validation tools MUST be used after LMM fitting tool execution. Specific validation tools determined by rq_tools (likely tools.validation.validate_lmm_convergence + tools.validation.validate_lmm_assumptions_comprehensive + tools.validation.validate_hypothesis_test_dual_pvalues per D068).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_lmm_model_summary.txt: 5-10 KB text file with readable model output
- data/step03_fixed_effects.csv: ~15 rows x 6 columns
- data/step03_random_effects.csv: 4 rows x 3 columns
- Data types: term/component (object), numeric columns (float64)

*Value Ranges:*
- Coefficients (estimate): Unrestricted (could be large for interaction terms)
- SE > 0 for all terms (negative SE indicates estimation failure)
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1]
- variance >= 0 for all random effects components (negative variance = convergence failure)

*Data Quality:*
- Model convergence: Check model_summary.txt for "converged successfully" or equivalent message
- No NaN in fixed_effects.csv (all terms estimated successfully)
- No negative variance in random_effects.csv
- 3-way interaction terms present: Time:Difficulty_c:paradigmICR and Time:Difficulty_c:paradigmIRE (or equivalent depending on reference level)
- Dual p-values: BOTH p_uncorrected AND p_bonferroni columns present per D068

*Log Validation:*
- Required pattern: "Model converged: True" (or pymer4 equivalent)
- Required pattern: "Fixed effects extracted: {N} terms"
- Required pattern: "Random effects extracted: 4 components"
- Required pattern: "Dual p-values computed: uncorrected + Bonferroni correction (alpha = 0.0033)"
- Forbidden patterns: "ERROR", "Convergence failed", "Singular fit", "NaN coefficients"
- Acceptable warnings: "boundary (singular) fit" IF convergence strategy applied and documented, "optimizer warnings" IF model still converged

**Expected Behavior on Validation Failure:**
- Convergence failure: Apply convergence strategy (simplify random structure), document in log, retry
- If all strategies exhausted: Raise error, log detailed convergence diagnostics to logs/step03_fit_lmm.log
- Quit script immediately, invoke g_debug with convergence diagnostics
- Assumption violations (e.g., severe non-normality): Log warning, continue (exploratory analysis tolerates minor violations)

---

### Step 4: Extract 3-Way Interaction and Prepare Plot Data

**Dependencies:** Step 3 (requires fitted LMM model outputs)
**Complexity:** Medium (10 min - post-hoc extraction and plot data aggregation)

**Purpose:** Extract 3-way interaction terms (Time x Difficulty_c x paradigm) from fitted model, test significance at Bonferroni alpha = 0.0033, and prepare plot data showing 6 trajectories (2 difficulty levels x 3 paradigms).

**Input:**

**File 1:** data/step03_fixed_effects.csv
**Format:** CSV with fixed effects coefficients
**Columns:** term, estimate, SE, z_value, p_uncorrected, p_bonferroni
**Expected Rows:** ~15

**File 2:** data/step02_lmm_input.csv (for observed means and plot data aggregation)
**Format:** Long format with centered predictors
**Columns:** composite_ID, UID, Test, Item, Response, paradigm, Difficulty_c, Time
**Expected Rows:** ~20,000

**Processing:**

**3-Way Interaction Extraction:**
1. Filter fixed_effects.csv to extract terms containing "Time:Difficulty_c:paradigm" (3-way interaction)
2. Extract coefficient estimates, SE, and dual p-values (uncorrected + Bonferroni) per D068
3. Compare p_bonferroni to alpha = 0.0033 (Bonferroni-corrected threshold from hypothesis)
4. Create interaction summary table with interpretation

**Plot Data Preparation:**
1. Define difficulty levels for plotting:
   - Easy items: Difficulty_c = -1 SD (1 standard deviation below mean)
   - Hard items: Difficulty_c = +1 SD (1 standard deviation above mean)
2. Create 6 trajectory groups: Easy/Hard x IFR/ICR/IRE
3. For each group, compute predicted Response at 4 timepoints (Days 0, 1, 3, 6):
   - Use fitted model coefficients to calculate predicted values
   - Convert TSVR_hours back to nominal days for plotting interpretability (Day 0 ~0 hours, Day 1 ~24 hours, Day 3 ~72 hours, Day 6 ~144 hours)
4. Compute observed means per group x timepoint from raw data for comparison
5. Format plot source CSV with columns: paradigm, difficulty_level, time_days, predicted_response, observed_mean

**Output:**

**File 1:** data/step04_3way_interaction_summary.csv
**Format:** CSV with 3-way interaction results
**Columns:**
  - `term` (string, interaction term name)
  - `estimate` (float, coefficient)
  - `SE` (float, standard error)
  - `z_value` (float, z-statistic)
  - `p_uncorrected` (float, uncorrected p-value)
  - `p_bonferroni` (float, Bonferroni-corrected p-value)
  - `significant_at_0.0033` (bool, TRUE if p_bonferroni < 0.0033)
**Expected Rows:** 2 (Time:Difficulty_c:paradigmICR, Time:Difficulty_c:paradigmIRE - comparing to reference paradigm IFR)

**File 2:** data/step04_difficulty_trajectories_data.csv
**Format:** Plot source CSV for interaction visualization
**Columns:**
  - `paradigm` (string, IFR/ICR/IRE)
  - `difficulty_level` (string, "Easy (-1SD)" or "Hard (+1SD)")
  - `time_days` (int, nominal days: 0, 1, 3, 6)
  - `predicted_response` (float, model-predicted response probability in [0, 1])
  - `observed_mean` (float, observed mean response for comparison)
  - `CI_lower` (float, 95% CI lower bound from model SE)
  - `CI_upper` (float, 95% CI upper bound from model SE)
**Expected Rows:** 24 (6 groups x 4 timepoints)

**Validation Requirement:**

Validation tools MUST be used after interaction extraction and plot data preparation tool execution. Specific validation tools determined by rq_tools (likely tools.validation.validate_hypothesis_test_dual_pvalues for interaction summary + tools.validation.validate_plot_data_completeness for plot CSV).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_3way_interaction_summary.csv: 2 rows x 7 columns
- data/step04_difficulty_trajectories_data.csv: 24 rows x 7 columns
- Data types: All numeric except term/paradigm/difficulty_level (object), significant_at_0.0033 (bool)

*Value Ranges:*
- p_uncorrected in [0, 1], p_bonferroni in [0, 1]
- predicted_response in [0, 1] (probability scale)
- observed_mean in [0, 1] (proportion correct)
- CI_lower in [0, 1], CI_upper in [0, 1]
- CI_upper > CI_lower for all rows

*Data Quality:*
- Interaction summary: Exactly 2 rows (ICR and IRE comparisons to IFR reference)
- Plot data: All 6 groups present (2 difficulty levels x 3 paradigms)
- Plot data: All 4 timepoints present per group (0, 1, 3, 6 days)
- No NaN in any columns (all groups estimated successfully)
- Dual p-values present in interaction summary per D068

*Log Validation:*
- Required pattern: "3-way interaction extracted: {N} terms"
- Required pattern: "Bonferroni alpha threshold: 0.0033"
- Required pattern: "Significant interactions: {K} of {N}" (could be 0, 1, or 2)
- Required pattern: "Plot data prepared: 24 rows (6 groups x 4 timepoints)"
- Forbidden patterns: "ERROR", "Missing interaction terms", "Incomplete factorial design"
- Acceptable warnings: "No significant 3-way interactions found" (null result is scientifically valid)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Expected 24 rows in plot data, found 18 - missing ICR x Easy combination")
- Log failure to logs/step04_extract_interaction.log
- Quit script immediately
- g_debug invoked to diagnose

---

## Expected Data Formats

### Wide vs Long Format Distinction

**This RQ uses LONG FORMAT throughout** (item-level response modeling, not participant-level theta scores).

**Long Format Structure:**
- One row per UID x Test x Item observation
- Response is dependent variable (0/1/NaN)
- Repeated measures nested within UID (4 tests per participant)
- Items crossed with UID (all participants respond to overlapping item sets)

**No wide-format transformations needed** (unlike IRT-based RQs that aggregate to composite_ID level).

---

### Composite ID Format

**Pattern:** `{UID}_{Test}`

**Examples:**
- P001_T1 (Participant P001, Test session T1)
- P001_T2 (Participant P001, Test session T2)
- P100_T4 (Participant P100, Test session T4)

**Purpose:** Links observations across steps while preserving UID and Test information for random effects grouping and TSVR merge.

---

### Difficulty Centering

**Raw Difficulty (from RQ 5.3.1):**
- Column name: `Difficulty`
- Range: Approximately [-3, 3] but unrestricted (temporal items may exceed |3.0|)
- Interpretation: Higher values = harder items (lower endorsement probability)

**Centered Difficulty (for LMM):**
- Column name: `Difficulty_c`
- Computation: `Difficulty_c = Difficulty - mean(Difficulty)`
- Expected mean: ~0 (within ±0.01 tolerance)
- Purpose: Centering improves interpretability of main effects and interactions (intercept represents average difficulty item)

---

### Time Variable (Decision D070)

**TSVR Format:**
- Column name: `TSVR_hours` (from RQ 5.3.1)
- Unit: Hours since VR encoding session
- Range: [0, 168] hours approximately (0 = encoding, 168 = 1 week)
- Source: Actual session timing (NOT nominal days)

**LMM Time Variable:**
- Column name: `Time` (renamed from TSVR_hours for LMM clarity)
- Same values as TSVR_hours
- Decision D070: Use actual time in hours, NOT nominal days (0, 1, 3, 6)

**Plot Time Variable:**
- Column name: `time_days` (in plot source CSV)
- Values: 0, 1, 3, 6 (nominal days for interpretability)
- Conversion: Approximate mapping from TSVR_hours to nearest nominal day

---

### Paradigm Coding

**Levels:** 3 retrieval paradigms
- IFR (Item Free Recall): Self-initiated retrieval, minimal support
- ICR (Item Cued Recall): Category-cued retrieval, partial support
- IRE (Item Recognition): Item-specific probe, maximal support

**Reference Level:** Alphabetically first = IFR (default in statsmodels/pymer4)

**Dummy Coding:** LMM will create 2 dummy variables (paradigmICR, paradigmIRE) comparing to IFR reference

---

## Cross-RQ Dependencies

### Dependency Type: DERIVED Data from RQ 5.3.1

**This RQ requires outputs from RQ 5.3.1 (Paradigm-Specific Trajectories):**

**File 1:** results/ch5/5.3.1/data/step03_item_parameters.csv
- Used in: Step 0 (merge item difficulty into response data)
- Required columns: item_name, dimension, a, b
- Purpose: RQ 5.3.1 calibrated IRT models and purified items per Decision D039. This RQ uses those difficulty estimates (`b` parameters) as item-level predictors.

**File 2:** results/ch5/5.3.1/data/step00_tsvr_mapping.csv
- Used in: Step 2 (merge TSVR time variable)
- Required columns: composite_ID, TSVR_hours
- Purpose: RQ 5.3.1 extracted TSVR timing data per Decision D070. This RQ uses actual time since encoding as continuous time predictor.

**Execution Order Constraint:**
1. RQ 5.3.1 must complete Step 3 (IRT Pass 2 calibration) to generate item_parameters.csv
2. RQ 5.3.1 must complete Step 0 (TSVR extraction) to generate tsvr_mapping.csv
3. This RQ (5.3.9) can then execute (uses both outputs)

**Data Source Boundaries:**
- **RAW data:** dfData.csv item-level responses extracted directly (no RQ dependencies for raw responses)
- **DERIVED data:** Item difficulty from RQ 5.3.1 (IRT parameters), TSVR from RQ 5.3.1 (timing data)
- **Scope:** This RQ does NOT calibrate IRT models (uses RQ 5.3.1 parameters as fixed item characteristics)

**Validation:**
- Step 0: Check results/ch5/5.3.1/data/step03_item_parameters.csv exists (EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch5/5.3.1/data/step00_tsvr_mapping.csv exists (EXPECTATIONS ERROR if absent)
- If either file missing -> quit with error -> user must execute RQ 5.3.1 first

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

---

### Validation Requirements By Step

#### Step 0: Extract Item-Level Response Data and Dependencies

**Analysis Tool:** (determined by rq_tools - likely tools.data extraction function + pandas merge operations)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_data_format + tools.validation.check_missing_data)

**What Validation Checks:**
- Output files exist (step00_response_level_data.csv, step00_tsvr_mapping.csv)
- Expected column count (6 for response data, 2 for TSVR)
- Expected row count (~20,000 for response data, 400 for TSVR)
- No unexpected NaN patterns (Response can have NaN, but Difficulty/paradigm/TSVR_hours should not)
- Paradigm values restricted to {IFR, ICR, IRE} (no room-level paradigms)
- Item codes match RQ 5.3.1 purified items (all Items present in item_parameters.csv)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Found RFR paradigm, expected only IFR/ICR/IRE")
- Log failure to logs/step00_extract_data.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked by master to diagnose root cause

---

#### Step 1: Create Composite ID and Expand to Analysis Format

**Analysis Tool:** (determined by rq_tools - likely pandas string concatenation + validation checks)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_data_format)

**What Validation Checks:**
- composite_ID format correct ({UID}_{Test} pattern)
- composite_ID uniqueness per UID x Test combination (400 unique composite_IDs)
- No duplicate UID x Test x Item observations (each observation unique)
- paradigm assignment consistent (each Item belongs to exactly one paradigm)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Item X assigned to multiple paradigms")
- Log failure to logs/step01_create_composite_id.log
- Quit script immediately
- g_debug invoked

---

#### Step 2: Center Difficulty Variable and Merge TSVR Time

**Analysis Tool:** (determined by rq_tools - likely pandas arithmetic + merge operations)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_standardization for centering + tools.validation.check_missing_data for merge)

**What Validation Checks:**
- Centering successful: mean(Difficulty_c) in [-0.01, 0.01]
- No NaN introduced by centering (Difficulty_c should have same non-NaN count as Difficulty)
- TSVR merge successful: No NaN in Time column (all composite_IDs matched)
- Time variable range reasonable: TSVR_hours in [0, 168] approximately

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "mean(Difficulty_c) = 0.35, expected ~0")
- Log failure to logs/step02_center_merge.log
- Quit script immediately
- g_debug invoked

---

#### Step 3: Fit Cross-Classified LMM with 3-Way Interaction

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.fit_lmm_trajectory_tsvr or pymer4 direct call)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_lmm_convergence + tools.validation.validate_lmm_assumptions_comprehensive + tools.validation.validate_hypothesis_test_dual_pvalues)

**What Validation Checks:**
- Model convergence: pymer4/statsmodels reports successful convergence (no singular fit warnings)
- Fixed effects: No NaN coefficients (all terms estimated)
- Random effects: All variance components positive (no negative variances)
- 3-way interaction present: Terms containing "Time:Difficulty_c:paradigm" exist in fixed effects
- Dual p-values: BOTH p_uncorrected AND p_bonferroni columns present per Decision D068
- Assumption checks (from validate_lmm_assumptions_comprehensive):
  - Residuals approximately normal (Kolmogorov-Smirnov test)
  - Homoscedasticity (scale-location plot shows random scatter)
  - No severe autocorrelation (ACF plot)
  - Linearity of residuals vs fitted values

**Expected Behavior on Validation Failure:**
- Convergence failure: Apply convergence strategy (simplify random structure), log decision, retry
- If all strategies exhausted: Raise error, log detailed convergence diagnostics
- Assumption violations (minor): Log warning, continue (exploratory analysis)
- Assumption violations (severe): Log error, recommend transformation/robustness checks
- Quit script only if critical failure (convergence exhausted or NaN coefficients)
- g_debug invoked with detailed diagnostics

---

#### Step 4: Extract 3-Way Interaction and Prepare Plot Data

**Analysis Tool:** (determined by rq_tools - likely pandas filtering + custom plot data aggregation function)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_hypothesis_test_dual_pvalues + tools.validation.validate_plot_data_completeness)

**What Validation Checks:**
- Interaction summary: Exactly 2 rows (ICR and IRE comparisons to IFR)
- Dual p-values: BOTH p_uncorrected AND p_bonferroni present per Decision D068
- Plot data: Complete factorial design (6 groups x 4 timepoints = 24 rows)
- Plot data: All paradigms present (IFR, ICR, IRE)
- Plot data: All difficulty levels present (Easy, Hard)
- Plot data: All timepoints present (0, 1, 3, 6 days)
- Value ranges: predicted_response in [0, 1], observed_mean in [0, 1], CI_upper > CI_lower

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Missing ICR x Easy x Day 3 combination in plot data")
- Log failure to logs/step04_extract_interaction.log
- Quit script immediately
- g_debug invoked

---

## Summary

**Total Steps:** 5 (Step 0: extraction + Steps 1-4: analysis steps)

**Estimated Runtime:**
- Total: High (60-120 minutes)
- Step 0: Low (5 min)
- Step 1: Medium (15 min)
- Step 2: Low (5 min)
- Step 3: High (45-90 min - crossed random effects on ~20,000 observations)
- Step 4: Medium (10 min)

**Cross-RQ Dependencies:**
- RQ 5.3.1 (IRT Pass 2 item parameters + TSVR mapping)
- Must complete before this RQ can execute

**Primary Outputs:**
- data/step03_lmm_model_summary.txt (full model results)
- data/step03_fixed_effects.csv (coefficients with dual p-values per D068)
- data/step04_3way_interaction_summary.csv (hypothesis test at alpha = 0.0033)
- data/step04_difficulty_trajectories_data.csv (plot source CSV for 6 trajectories)

**Validation Coverage:**
- 100% (all 5 steps have validation requirements)
- 4-layer substance criteria specified for each step
- Convergence strategy documented for LMM (per rq_stats feedback)

**Decision Compliance:**
- D068: Dual p-value reporting (uncorrected + Bonferroni) for 3-way interaction
- D070: TSVR as time variable (actual hours, not nominal days)
- No D039 (no IRT calibration in this RQ)
- No D069 (no trajectory plots - interaction plot instead)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-02): Initial plan created by rq_planner agent for RQ 5.3.9

---

**End of Analysis Plan**
