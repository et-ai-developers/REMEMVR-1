# Analysis Plan: RQ 5.5.5 - Purified CTT Effects for Source-Destination Memory

**Research Question:** 5.5.5
**Created:** 2025-12-04
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ tests the **purification-trajectory paradox** for source (-U-, pick-up locations) and destination (-D-, put-down locations) memory. The paradoxdiscovered in RQ 5.2.5 (Domains), replicated in 5.3.6 (Paradigms) and 5.4.5 (Congruence)suggests that IRT-based item purification (removing items with extreme difficulty |b| > 3.0 or low discrimination a < 0.4) creates a psychometric tension:

- **Cross-sectional improvement:** Purified CTT shows HIGHER correlation with IRT theta (improved measurement precision)
- **Longitudinal degradation:** Purified CTT shows WORSE LMM trajectory fit (higher AIC)

This RQ provides the **4th independent replication**, extending the paradox to source-destination spatial memory. Success would establish this as a general measurement principle rather than domain/paradigm/congruence-specific artifact.

**Analysis Approach:**

Classical Test Theory (CTT) sum score computation with two versions:
1. **Full CTT:** All items (18 source + 18 destination = 36 total items)
2. **Purified CTT:** IRT-retained items only (expected 25-32 items after purification per Decision D039)

Compare Full vs Purified CTT across three measurement dimensions:
- **Reliability:** Cronbach's alpha with bootstrap 95% CIs (10,000 resamples)
- **Correlation:** Pearson r with IRT theta, tested via Steiger's z-test for dependent correlations
- **Trajectory Fit:** Parallel LMMs on z-standardized scores, compared via AIC (Burnham & Anderson, 2002)

**Pipeline:** 9 analysis steps (Step 0: dependency validation, Steps 1-7.5: analysis, Step 8: plot data preparation)

**Estimated Runtime:** Medium (~30-45 minutes total)
- Low complexity: Steps 0-4, 6, 8 (data loading, CTT computation, reliability, plot prep)
- Medium complexity: Steps 5, 7, 7.5 (correlations, LMM fitting, assumption validation)

**Key Decisions Applied:**
- Decision D039: 2-pass IRT purification (inherited from RQ 5.5.1)
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni correction)
- Decision D069: NOT applicable (no trajectory plots, only comparison plots)
- Decision D070: NOT applicable (no new LMM fitting with TSVR, reuses RQ 5.5.1 structure)

---

## Analysis Plan

### Step 0: Load and Validate RQ 5.5.1 Dependencies

**Dependencies:** None (first step)
**Complexity:** Low (file loading and validation checks only)

**Purpose:** Verify RQ 5.5.1 completed successfully and load required outputs for downstream analysis.

**Input:**

**File 1:** results/ch5/5.5.1/status.yaml
**Purpose:** Verify RQ 5.5.1 completion status
**Required:** rq_results.status = "success"

**File 2:** results/ch5/5.5.1/data/step02_purified_items.csv
**Format:** CSV with item-level purification results
**Required Columns:**
  - item_name (string): Item tag (e.g., VR-IFR-A01-U-ANS-i1)
  - location_type (string): "source" or "destination"
  - a (float): Discrimination parameter (>= 0.4 for retained items)
  - b (float): Difficulty parameter (|b| <= 3.0 for retained items)
  - retained (boolean): True if item passed purification thresholds
**Expected Rows:** ~36 items (18 source + 18 destination)

**File 3:** results/ch5/5.5.1/data/step03_theta_scores.csv
**Format:** CSV with IRT ability estimates per participant-test-location
**Required Columns:**
  - UID (string): Participant identifier
  - test (string): Test session (T1, T2, T3, T4)
  - theta_source (float): Source memory ability estimate
  - se_source (float): Standard error for source theta
  - theta_destination (float): Destination memory ability estimate
  - se_destination (float): Standard error for destination theta
**Expected Rows:** 400 (100 participants x 4 tests)

**File 4:** results/ch5/5.5.1/data/step00_tsvr_mapping.csv
**Format:** CSV with TSVR time variable per participant-test
**Required Columns:**
  - UID (string): Participant identifier
  - test (string): Test session
  - TSVR_hours (float): Actual hours since VR encoding
**Expected Rows:** 400 (100 participants x 4 tests)

**File 5:** data/cache/dfData.csv
**Format:** CSV with raw binary responses for all VR items
**Purpose:** Compute Full CTT scores on complete item set (before purification)
**Required Columns:**
  - UID (string): Participant identifier
  - TEST (string): Test session
  - Item tags matching VR-{paradigm}-{test}-{location}-ANS pattern
**Filter:** IFR, ICR, IRE paradigms; -U- and -D- location tags only

**Processing:**

1. Read status.yaml, verify rq_results.status = "success"
2. Load all 5 input files
3. Validate purified_items structure:
   - 36 items present (18 source + 18 destination)
   - All items have location_type, a, b, retained columns
   - Retention rate 55-85% (20-30 items retained)
4. Validate theta_scores structure:
   - 400 rows (100 participants x 4 tests)
   - No NaN in theta columns
   - theta values in scientifically reasonable range [-4, 4]
5. Validate TSVR mapping:
   - 400 rows matching theta_scores
   - All UIDs and tests present in both files
6. Validate dfData.csv contains required source/destination items

**Output:**

**File 1:** data/step00_dependency_validation.txt
**Format:** Text report documenting validation results
**Contents:**
  - RQ 5.5.1 status check result
  - Item counts (total, retained, removed) per location type
  - Participant count, test count validation
  - Any warnings or missing data flagged

**Validation Requirement:**

Validation tools MUST be used after dependency loading. Specific validation tools will be determined by rq_tools based on file existence checks and data structure validation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_dependency_validation.txt exists
- File size > 500 bytes (sufficient detail documented)

*Value Ranges:*
- Item retention rate in [0.55, 0.85] (55-85% retention expected per Chapter 5 patterns)
- Theta values in [-4, 4] (extreme values suggest calibration issues)
- TSVR_hours in [0, 168] (0 hours = encoding, 168 hours = 7 days max)

*Data Quality:*
- All 400 UID x test combinations present in theta and TSVR files
- No duplicate UID x test rows
- No NaN values in critical columns (theta, TSVR_hours)
- Item mapping: 18 source items, 18 destination items identified

*Log Validation:*
- Required pattern: "RQ 5.5.1 status: success"
- Required pattern: "Items loaded: 36 total (18 source, 18 destination)"
- Required pattern: "Items retained: [20-30]" (specific count)
- Forbidden patterns: "ERROR", "RQ 5.5.1 incomplete", "Missing required file"

**Expected Behavior on Validation Failure:**

If RQ 5.5.1 status != success:
- Raise EXPECTATIONS ERROR with message "RQ 5.5.1 must complete before RQ 5.5.5"
- QUIT immediately, do NOT proceed to Step 1

If any required file missing:
- Raise EXPECTATIONS ERROR with specific missing file path
- QUIT immediately

If item counts or retention rates outside expected ranges:
- Raise CLARITY ERROR with details
- QUIT immediately (may indicate RQ 5.5.1 analysis issues)

---

### Step 1: Map Retained vs Removed Items by Location Type

**Dependencies:** Step 0 (requires purified_items.csv loaded)
**Complexity:** Low (filtering and categorization only)

**Purpose:** Create item mapping showing which items were retained vs removed during IRT purification, separately for source and destination memory.

**Input:**

**File:** data/step00_purified_items_from_rq551.csv (loaded in Step 0)
**Structure:** 36 rows, one per item
**Columns:** item_name, location_type, a, b, retained

**Processing:**

1. Group items by location_type (source vs destination)
2. Within each location type:
   - Count total items
   - Count retained items (retained = True)
   - Count removed items (retained = False)
   - Compute retention rate (retained / total)
3. Create summary table with location-specific retention statistics
4. List removed item names per location type (for transparency)

**Output:**

**File:** data/step01_item_mapping.csv
**Format:** CSV with item-level retention status
**Columns:**
  - item_name (string): Full item tag
  - location_type (string): "source" or "destination"
  - a (float): IRT discrimination parameter
  - b (float): IRT difficulty parameter
  - retained (boolean): True if passed purification thresholds
  - removal_reason (string): "low_discrimination" if a < 0.4, "extreme_difficulty" if |b| > 3.0, "both" if both, "retained" if kept
**Expected Rows:** 36 (18 source + 18 destination)

**Validation Requirement:**

Validation tools MUST be used after item mapping creation. Specific validation tools will be determined by rq_tools based on categorical distribution checks and retention rate validation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_item_mapping.csv: 36 rows x 6 columns
- Columns: item_name (object), location_type (object), a (float64), b (float64), retained (bool), removal_reason (object)

*Value Ranges:*
- a in [0.0, 4.0] (discrimination must be non-negative, extreme values > 4.0 rare)
- b unrestricted (temporal items can have |b| > 3.0 before purification)
- Retention rate per location type in [0.55, 0.85]

*Data Quality:*
- All 36 items present (18 source, 18 destination)
- location_type in {"source", "destination"} (no other values)
- removal_reason in {"retained", "low_discrimination", "extreme_difficulty", "both"}
- No NaN values in a, b, or retained columns
- At least 10 retained items per location type (minimum for reliable analysis)

*Log Validation:*
- Required pattern: "Source items: 18 total, [X] retained, [Y] removed"
- Required pattern: "Destination items: 18 total, [X] retained, [Y] removed"
- Required pattern: "Retention rates: Source [55-85]%, Destination [55-85]%"
- Forbidden patterns: "ERROR", "No items retained", "All items removed"

**Expected Behavior on Validation Failure:**

If retention rate < 55%:
- Raise WARNING: "Low retention rate may reduce measurement reliability"
- Proceed with analysis (document limitation)

If < 10 items retained per location type:
- Raise CLARITY ERROR: "Insufficient retained items for reliable CTT computation"
- QUIT immediately (analysis not viable)

---

### Step 2: Compute Full CTT Sum Scores

**Dependencies:** Step 1 (requires item mapping)
**Complexity:** Low (sum score computation from raw data)

**Purpose:** Compute Classical Test Theory (CTT) sum scores using ALL source and destination items (before purification) to establish baseline measurement.

**Input:**

**File:** data/cache/dfData.csv (raw binary responses)
**Structure:** Wide format, 100 participants x 4 tests = 400 rows
**Required Columns:**
  - UID (string): Participant identifier
  - TEST (string): Test session
  - Source item columns (18 items): VR-{IFR|ICR|IRE}-{A01|R03|R06}-U-ANS-{i1-i6}
  - Destination item columns (18 items): VR-{IFR|ICR|IRE}-{A01|R03|R06}-D-ANS-{i1-i6}

**Processing:**

1. Filter dfData.csv to source items (-U- tags), extract binary responses (0/1)
2. Compute source CTT score per UID x test: mean of binary responses across 18 source items
3. Filter dfData.csv to destination items (-D- tags), extract binary responses
4. Compute destination CTT score per UID x test: mean of binary responses across 18 destination items
5. Reshape to long format: UID, test, location_type, ctt_full_score
6. Expected: 800 rows (100 participants x 4 tests x 2 location types)

**Dichotomization Rule (from concept):**
- TQ < 1 -> 0 (incorrect)
- TQ >= 1 -> 1 (correct)
- NaN -> NaN (missing, excluded from mean computation)

**Output:**

**File:** data/step02_ctt_full_scores.csv
**Format:** CSV, long format
**Columns:**
  - UID (string): Participant identifier
  - test (string): Test session (T1, T2, T3, T4)
  - location_type (string): "source" or "destination"
  - ctt_full_score (float): Mean proportion correct across all items for that location type
**Expected Rows:** 800 (100 participants x 4 tests x 2 location types)

**Validation Requirement:**

Validation tools MUST be used after CTT score computation. Specific validation tools will be determined by rq_tools based on probability range validation (scores in [0,1]) and missing data checks.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_ctt_full_scores.csv: 800 rows x 4 columns
- Columns: UID (object), test (object), location_type (object), ctt_full_score (float64)

*Value Ranges:*
- ctt_full_score in [0, 1] (proportion correct, bounded scale)
- No values outside [0, 1] (indicates computation error)

*Data Quality:*
- All 800 observations present (100 UID x 4 test x 2 location_type)
- No NaN values tolerated (all participants completed all tests per design)
- location_type in {"source", "destination"}
- test in {"T1", "T2", "T3", "T4"}
- All UIDs from RQ 5.5.1 theta_scores present

*Log Validation:*
- Required pattern: "Full CTT computed: 800 observations (source: 400, destination: 400)"
- Required pattern: "Score range: [0.0, 1.0]"
- Required pattern: "Missing values: 0"
- Forbidden patterns: "ERROR", "NaN detected", "Score out of bounds"

**Expected Behavior on Validation Failure:**

If any ctt_full_score > 1.0 or < 0.0:
- Raise TOOL ERROR: "CTT computation error - scores outside [0,1]"
- QUIT immediately (likely coding error)

If NaN values present:
- Raise CLARITY ERROR: "Missing CTT scores - expected 800 complete observations"
- QUIT immediately (data quality issue)

---

### Step 3: Compute Purified CTT Sum Scores

**Dependencies:** Steps 1-2 (requires item mapping and Full CTT computed)
**Complexity:** Low (filtered sum score computation)

**Purpose:** Compute CTT sum scores using ONLY IRT-retained items (post-purification) to test whether item purification improves measurement precision.

**Input:**

**File 1:** data/step01_item_mapping.csv
**Structure:** 36 rows with retention status per item
**Use:** Identify which items to include in Purified CTT computation

**File 2:** data/cache/dfData.csv (raw binary responses)
**Structure:** Same as Step 2
**Use:** Extract responses for retained items only

**Processing:**

1. Filter item_mapping to retained items only (retained = True)
2. Extract retained source item names (expected 12-16 items, 67-89% retention)
3. Extract retained destination item names (expected 12-16 items)
4. Filter dfData.csv to retained source items only, compute purified source CTT score per UID x test
5. Filter dfData.csv to retained destination items only, compute purified destination CTT score per UID x test
6. Reshape to long format: UID, test, location_type, ctt_purified_score
7. Expected: 800 rows (same structure as Full CTT)

**Output:**

**File:** data/step03_ctt_purified_scores.csv
**Format:** CSV, long format
**Columns:**
  - UID (string): Participant identifier
  - test (string): Test session
  - location_type (string): "source" or "destination"
  - ctt_purified_score (float): Mean proportion correct across RETAINED items only for that location type
**Expected Rows:** 800 (100 participants x 4 tests x 2 location types)

**Validation Requirement:**

Validation tools MUST be used after Purified CTT computation. Specific validation tools determined by rq_tools based on probability range validation and consistency checks with Full CTT.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_ctt_purified_scores.csv: 800 rows x 4 columns
- Columns: UID (object), test (object), location_type (object), ctt_purified_score (float64)

*Value Ranges:*
- ctt_purified_score in [0, 1] (proportion correct)
- Scores may differ from Full CTT (expected correlation r ~ 0.90-0.95)

*Data Quality:*
- All 800 observations present (identical structure to Full CTT)
- No NaN values tolerated
- location_type and test values match Full CTT exactly
- UID set matches Full CTT exactly

*Log Validation:*
- Required pattern: "Purified CTT computed: 800 observations"
- Required pattern: "Retained items used: [20-30] total ([10-16] source, [10-16] destination)"
- Required pattern: "Score range: [0.0, 1.0]"
- Required pattern: "Correlation with Full CTT: r > 0.85" (high convergence expected)
- Forbidden patterns: "ERROR", "No retained items", "NaN detected"

**Expected Behavior on Validation Failure:**

If correlation between Full and Purified CTT < 0.85:
- Raise WARNING: "Low convergence between Full and Purified CTT suggests large purification effect"
- Proceed with analysis (expected pattern if many items removed)

If any ctt_purified_score out of [0,1]:
- Raise TOOL ERROR: "Purified CTT computation error"
- QUIT immediately

---

### Step 4: Reliability Assessment (Cronbach's Alpha)

**Dependencies:** Steps 2-3 (requires both Full and Purified CTT scores)
**Complexity:** Low (reliability computation with bootstrap CIs)

**Purpose:** Assess internal consistency reliability for Full vs Purified CTT scores per location type, testing whether item purification improves reliability.

**Input:**

**File 1:** data/cache/dfData.csv (raw item-level responses)
**Purpose:** Compute Cronbach's alpha at item level (not from sum scores)

**File 2:** data/step01_item_mapping.csv
**Purpose:** Identify retained vs full item sets per location type

**Processing:**

1. **Full CTT Reliability (Source):**
   - Extract all 18 source items from dfData.csv for all 400 source observations
   - Compute Cronbach's alpha using all source items
   - Bootstrap 95% CI (10,000 resamples)

2. **Purified CTT Reliability (Source):**
   - Extract retained source items only (12-16 items)
   - Compute Cronbach's alpha on retained items
   - Bootstrap 95% CI (10,000 resamples)

3. **Full CTT Reliability (Destination):**
   - Extract all 18 destination items for all 400 destination observations
   - Compute Cronbach's alpha
   - Bootstrap 95% CI

4. **Purified CTT Reliability (Destination):**
   - Extract retained destination items only
   - Compute Cronbach's alpha
   - Bootstrap 95% CI

5. Test alpha improvement: Purified alpha > Full alpha per location type

**Bootstrap Method:**
- n_iter = 10,000
- Resample participants (UID) with replacement
- Compute alpha on each bootstrap sample
- 95% CI from percentile method (2.5th, 97.5th percentiles)

**Output:**

**File:** data/step04_reliability_assessment.csv
**Format:** CSV with 4 rows (2 location types x 2 versions)
**Columns:**
  - location_type (string): "source" or "destination"
  - version (string): "full" or "purified"
  - n_items (int): Number of items used for alpha computation
  - alpha (float): Cronbach's alpha point estimate
  - CI_lower (float): Lower 95% confidence bound
  - CI_upper (float): Upper 95% confidence bound
  - alpha_improvement (float): Purified alpha - Full alpha (computed after all 4 alphas obtained)
**Expected Rows:** 4

**Validation Requirement:**

Validation tools MUST be used after reliability computation. Specific validation tools determined by rq_tools based on alpha range checks and CI non-overlap with zero.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_reliability_assessment.csv: 4 rows x 7 columns
- Columns: location_type (object), version (object), n_items (int64), alpha (float64), CI_lower (float64), CI_upper (float64), alpha_improvement (float64)

*Value Ranges:*
- alpha in [0.60, 0.95] (acceptable to excellent internal consistency)
- CI_lower, CI_upper in [0, 1] (alpha bounded)
- CI_upper > CI_lower for all rows
- alpha_improvement in [-0.20, +0.20] (typical purification effect)

*Data Quality:*
- All 4 rows present (source/destination x full/purified)
- No NaN values in alpha or CI columns
- n_items matches expected counts (18 for full, 12-16 for purified)
- Bootstrap CIs non-overlapping with 0 (reliable alpha estimates)

*Log Validation:*
- Required pattern: "Reliability computed: 4 conditions (source/destination x full/purified)"
- Required pattern: "Bootstrap iterations: 10000"
- Required pattern: "All alphas in acceptable range [0.60, 0.95]"
- Forbidden patterns: "ERROR", "Alpha out of bounds", "Bootstrap failed"

**Expected Behavior on Validation Failure:**

If any alpha < 0.60:
- Raise WARNING: "Low reliability detected - alpha < 0.60 suggests weak internal consistency"
- Proceed with analysis (document limitation)

If any alpha > 0.95:
- Raise WARNING: "Extremely high reliability - alpha > 0.95 may indicate item redundancy"
- Proceed with analysis

If bootstrap fails:
- Raise TOOL ERROR: "Bootstrap CI computation failed"
- QUIT immediately

---

### Step 5: Correlation Analysis with Steiger's Z-Test

**Dependencies:** Steps 0, 2-3 (requires IRT theta and both CTT versions)
**Complexity:** Medium (dependent correlation testing)

**Purpose:** Test whether Purified CTT shows higher correlation with IRT theta compared to Full CTT, using Steiger's z-test for dependent correlations (Decision D068 dual p-values).

**Input:**

**File 1:** data/step03_theta_scores_from_rq551.csv (loaded in Step 0)
**Columns:** UID, test, theta_source, theta_destination

**File 2:** data/step02_ctt_full_scores.csv
**Columns:** UID, test, location_type, ctt_full_score

**File 3:** data/step03_ctt_purified_scores.csv
**Columns:** UID, test, location_type, ctt_purified_score

**Processing:**

1. **Source Memory Correlations:**
   - Merge theta_source with ctt_full_score (source only)
   - Compute r_full_source = corr(theta_source, ctt_full_source)
   - Merge theta_source with ctt_purified_score (source only)
   - Compute r_purified_source = corr(theta_source, ctt_purified_source)
   - Steiger's z-test for dependent correlations:
     - Tests if r_purified_source differs from r_full_source
     - Both correlations share theta_source (dependent)
   - Bonferroni correction: alpha = 0.05 / 2 = 0.025 (2 location types)
   - Report BOTH p_uncorrected and p_bonferroni (Decision D068)

2. **Destination Memory Correlations:**
   - Same procedure for theta_destination
   - Compute r_full_destination, r_purified_destination
   - Steiger's z-test
   - Report dual p-values

3. **Effect Size:** Compute delta_r = r_purified - r_full per location type

**Steiger's Z-Test Formula:**

Tests if corr(X, Y1) differs from corr(X, Y2) when both share variable X.

```
Z = (r_XY1 - r_XY2) / sqrt(2 * (1 - r_Y1Y2) / n)
```

Where:
- r_XY1 = corr(theta, ctt_full)
- r_XY2 = corr(theta, ctt_purified)
- r_Y1Y2 = corr(ctt_full, ctt_purified)
- n = sample size (400 per location type)

**Output:**

**File:** data/step05_correlation_analysis.csv
**Format:** CSV with 2 rows (source, destination)
**Columns:**
  - location_type (string): "source" or "destination"
  - r_full (float): Correlation between IRT theta and Full CTT
  - r_purified (float): Correlation between IRT theta and Purified CTT
  - delta_r (float): r_purified - r_full (positive = purification improved correlation)
  - r_full_purified (float): Correlation between Full and Purified CTT (used in Steiger's formula)
  - steiger_z (float): Z-statistic from Steiger's test
  - p_uncorrected (float): Uncorrected p-value (Decision D068)
  - p_bonferroni (float): Bonferroni-corrected p-value (alpha = 0.025, Decision D068)
  - n (int): Sample size (400 per location type)
**Expected Rows:** 2 (source, destination)

**Validation Requirement:**

Validation tools MUST be used after correlation analysis. Specific validation tools determined by rq_tools based on correlation range validation and Decision D068 dual p-value compliance.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_correlation_analysis.csv: 2 rows x 9 columns
- Columns: location_type (object), r_full (float64), r_purified (float64), delta_r (float64), r_full_purified (float64), steiger_z (float64), p_uncorrected (float64), p_bonferroni (float64), n (int64)

*Value Ranges:*
- r_full, r_purified in [0.50, 1.00] (moderate to exceptional convergence expected)
- delta_r in [-0.20, +0.20] (typical purification effect)
- r_full_purified in [0.85, 1.00] (high convergence between Full and Purified CTT)
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1]
- p_bonferroni >= p_uncorrected (correction cannot reduce p-value)
- n = 400 for both location types

*Data Quality:*
- All 2 rows present (source, destination)
- No NaN values in any column
- Dual p-values present per Decision D068 (both p_uncorrected and p_bonferroni)
- All correlations positive (CTT and IRT should agree on ability ordering)

*Log Validation:*
- Required pattern: "Correlation analysis: 2 location types"
- Required pattern: "Full CTT correlations: source r = [0.XX], destination r = [0.XX]"
- Required pattern: "Purified CTT correlations: source r = [0.XX], destination r = [0.XX]"
- Required pattern: "Steiger's z-tests: dual p-values reported (Decision D068)"
- Required pattern: "VALIDATION - PASS: Decision D068 dual p-values"
- Forbidden patterns: "ERROR", "Correlation out of bounds", "Negative correlation"

**Expected Behavior on Validation Failure:**

If any correlation < 0.50:
- Raise WARNING: "Low CTT-IRT convergence detected (r < 0.50)"
- Proceed with analysis (document as measurement quality concern)

If p_bonferroni < p_uncorrected:
- Raise TOOL ERROR: "Bonferroni correction logic error"
- QUIT immediately (indicates bug in correction implementation)

If dual p-values missing:
- Raise SCOPE ERROR: "Decision D068 violated - must report BOTH uncorrected and Bonferroni p-values"
- QUIT immediately

---

### Step 6: Z-Standardize All Measurements

**Dependencies:** Steps 0, 2-3 (requires IRT theta, Full CTT, Purified CTT)
**Complexity:** Low (linear transformation)

**Purpose:** Standardize all measurements (IRT theta, Full CTT, Purified CTT) to z-scores (mean=0, SD=1) within location type to enable valid AIC comparison across different measurement scales in Step 7.

**Methodological Justification for Z-Standardization AIC Comparison:**

Z-standardization is a monotonic linear transformation that preserves rank-order relationships between observations. AIC comparison across z-standardized variables is valid for comparing relative model fit within the same dataset because:

1. **Likelihood preservation:** Monotonic transformations preserve maximum likelihood ordering (Pawitan, 2001)
2. **Rank-order preservation:** AIC rankings are preserved because log-likelihood differences remain constant under linear transformations
3. **Scale equalization:** Z-standardization ensures model coefficients and residuals are on comparable scales, preventing scale-driven AIC differences

Alternative approaches (raw AIC without transformation) would conflate scale differences with model fit differences. The z-standardization approach isolates trajectory structure from measurement scale.

**Input:**

**File 1:** data/step03_theta_scores_from_rq551.csv
**Columns:** UID, test, theta_source, theta_destination

**File 2:** data/step02_ctt_full_scores.csv
**Columns:** UID, test, location_type, ctt_full_score

**File 3:** data/step03_ctt_purified_scores.csv
**Columns:** UID, test, location_type, ctt_purified_score

**Processing:**

1. **Z-standardize IRT theta per location type:**
   - Compute mean(theta_source), sd(theta_source) across all 400 source observations
   - irt_z_source = (theta_source - mean) / sd
   - Repeat for theta_destination

2. **Z-standardize Full CTT per location type:**
   - Compute mean(ctt_full_source), sd(ctt_full_source) across 400 source observations
   - ctt_full_z_source = (ctt_full_source - mean) / sd
   - Repeat for destination

3. **Z-standardize Purified CTT per location type:**
   - Compute mean(ctt_purified_source), sd(ctt_purified_source)
   - ctt_purified_z_source = (ctt_purified_source - mean) / sd
   - Repeat for destination

4. Merge all z-scores into single file with location_type factor

5. Validate standardization: mean H 0 (±0.05), SD H 1 (±0.05) for all 6 z-score columns

**Output:**

**File:** data/step06_standardized_scores.csv
**Format:** CSV, long format
**Columns:**
  - UID (string): Participant identifier
  - test (string): Test session
  - location_type (string): "source" or "destination"
  - irt_z (float): Z-standardized IRT theta
  - ctt_full_z (float): Z-standardized Full CTT score
  - ctt_purified_z (float): Z-standardized Purified CTT score
**Expected Rows:** 800 (100 participants x 4 tests x 2 location types)

**Validation Requirement:**

Validation tools MUST be used after z-standardization. Specific validation tools determined by rq_tools based on standardization validation (mean H 0, SD H 1).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_standardized_scores.csv: 800 rows x 6 columns
- Columns: UID (object), test (object), location_type (object), irt_z (float64), ctt_full_z (float64), ctt_purified_z (float64)

*Value Ranges:*
- irt_z typically in [-3, 3] (z-scores, extreme values possible but rare)
- ctt_full_z typically in [-3, 3]
- ctt_purified_z typically in [-3, 3]
- No hard limits (z-scores can exceed ±3 for extreme participants)

*Data Quality:*
- All 800 observations present
- No NaN values tolerated
- Standardization validation per location type:
  - mean(irt_z | location_type) H 0 (±0.05 tolerance)
  - sd(irt_z | location_type) H 1 (±0.05 tolerance)
  - Repeat for ctt_full_z, ctt_purified_z
- All 6 z-score columns must pass standardization validation

*Log Validation:*
- Required pattern: "Z-standardization complete: 6 variables (3 measurements x 2 location types)"
- Required pattern: "VALIDATION - PASS: Standardization check (mean H 0, SD H 1)"
- Required pattern: "Source IRT z: mean = [±0.05], SD = [0.95-1.05]"
- Required pattern: "Destination IRT z: mean = [±0.05], SD = [0.95-1.05]"
- Forbidden patterns: "ERROR", "Standardization failed", "Mean far from 0"

**Expected Behavior on Validation Failure:**

If standardization check fails (mean not H 0 or SD not H 1):
- Raise TOOL ERROR: "Z-standardization computation error"
- QUIT immediately (indicates bug in transformation)

If any z-score column has NaN:
- Raise CLARITY ERROR: "Missing values in z-standardized scores"
- QUIT immediately (upstream data issue)

---

### Step 7: Fit Parallel LMMs and Compare AIC

**Dependencies:** Step 6 (requires z-standardized scores)
**Complexity:** Medium (LMM fitting on 6 models)

**Purpose:** Fit parallel Linear Mixed Models on z-standardized measurements (IRT, Full CTT, Purified CTT) for both location types, then compare trajectory fit via AIC to test purification-trajectory paradox.

**Input:**

**File:** data/step06_standardized_scores.csv
**Columns:** UID, test, location_type, irt_z, ctt_full_z, ctt_purified_z

**File:** data/step00_tsvr_mapping.csv (from Step 0)
**Columns:** UID, test, TSVR_hours

**Processing:**

1. **Merge z-scores with TSVR:**
   - Left join standardized_scores with TSVR on (UID, test)
   - Create Time variable (TSVR_hours / 24 = Days)

2. **Fit 6 parallel LMMs:**

   All models use identical formula structure (parallel design):
   ```
   score ~ Time + (Time | UID)
   ```

   Where:
   - Time = TSVR_hours / 24 (continuous days)
   - Random intercepts and slopes per participant (UID)
   - REML = False (required for AIC comparison)

   **Models to fit:**
   - Model 1: Source IRT (outcome = irt_z, filter location_type = "source")
   - Model 2: Source Full CTT (outcome = ctt_full_z, filter location_type = "source")
   - Model 3: Source Purified CTT (outcome = ctt_purified_z, filter location_type = "source")
   - Model 4: Destination IRT (outcome = irt_z, filter location_type = "destination")
   - Model 5: Destination Full CTT (outcome = ctt_full_z, filter location_type = "destination")
   - Model 6: Destination Purified CTT (outcome = ctt_purified_z, filter location_type = "destination")

3. **Extract AIC per model:**
   - All 6 models should converge (z-standardization improves convergence)
   - Extract AIC from fitted model object

4. **Compare AIC within location type:**
   - Source: Compare AIC(IRT), AIC(Full CTT), AIC(Purified CTT)
   - Destination: Compare AIC(IRT), AIC(Full CTT), AIC(Purified CTT)
   - Compute ”AIC = AIC(Purified CTT) - AIC(Full CTT) per location type
   - Interpret per Burnham & Anderson (2002):
     - ”AIC > 2: Substantial evidence favoring lower-AIC model
     - ”AIC > 10: Decisive evidence

5. **Paradox Test:**
   - Expected: ”AIC > +2 (Purified CTT has HIGHER AIC than Full CTT)
   - Indicates Full CTT provides better trajectory fit despite lower correlation with IRT

**Output:**

**File:** data/step07_lmm_model_comparison.csv
**Format:** CSV with 2 rows (source, destination)
**Columns:**
  - location_type (string): "source" or "destination"
  - aic_irt (float): AIC for IRT z-scores
  - aic_ctt_full (float): AIC for Full CTT z-scores
  - aic_ctt_purified (float): AIC for Purified CTT z-scores
  - delta_aic_full_purified (float): AIC(Purified) - AIC(Full), positive = worse fit for Purified
  - interpretation (string): "Full CTT favored" if ”AIC > 2, "No difference" if |”AIC| <= 2, "Purified CTT favored" if ”AIC < -2
  - n_observations (int): Number of observations per location type (400)
  - converged_all (bool): True if all 3 models converged successfully
**Expected Rows:** 2

**Validation Requirement:**

Validation tools MUST be used after LMM fitting. Specific validation tools determined by rq_tools based on LMM convergence checks and AIC finite value validation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_lmm_model_comparison.csv: 2 rows x 8 columns
- Columns: location_type (object), aic_irt (float64), aic_ctt_full (float64), aic_ctt_purified (float64), delta_aic_full_purified (float64), interpretation (object), n_observations (int64), converged_all (bool)

*Value Ranges:*
- AIC values finite (not NaN, not infinite)
- AIC typically in [-1000, 1000] for z-standardized data with n=400
- delta_aic_full_purified typically in [-50, +50]
- n_observations = 400 for both location types

*Data Quality:*
- All 2 rows present (source, destination)
- converged_all = True for both location types (all 6 models must converge)
- No NaN or infinite AIC values
- interpretation matches delta_aic sign and magnitude

*Log Validation:*
- Required pattern: "LMM fitting: 6 models (3 measurements x 2 location types)"
- Required pattern: "All models converged: True"
- Required pattern: "Source ”AIC (Purified - Full): [value]"
- Required pattern: "Destination ”AIC (Purified - Full): [value]"
- Required pattern: "VALIDATION - PASS: All AICs finite"
- Forbidden patterns: "ERROR", "Model convergence failed", "AIC = NaN"

**Expected Behavior on Validation Failure:**

If any model fails to converge:
- Raise WARNING: "Model convergence issue for [model name]"
- Attempt model simplification (remove random slopes)
- If still fails: QUIT with TOOL ERROR

If any AIC is NaN or infinite:
- Raise TOOL ERROR: "AIC computation failed - model did not fit properly"
- QUIT immediately

---

### Step 7.5: Validate LMM Assumptions

**Dependencies:** Step 7 (requires fitted LMM models)
**Complexity:** Medium (comprehensive assumption testing)

**Purpose:** Validate Linear Mixed Model assumptions for all 6 fitted models using comprehensive diagnostic procedures. Document violations for CTT models (expected due to bounded [0,1] scale) but proceed with AIC comparison (consistent with prior Chapter 5 RQs).

**CTT Bounded Scale Limitations:**

Unlike IRT theta (unbounded continuous scale), CTT sum scores are bounded [0,1], creating potential ceiling/floor effects that violate LMM normality assumptions. If destination memory shows low accuracy (predicted based on goal discounting and proactive interference), floor effects may restrict variance and create left-skewed distributions.

This step assesses:
- (1) Linearity
- (2) Homoscedasticity
- (3) Normality of residuals
- (4) Normality of random effects
- (5) Independence
- (6) No multicollinearity (N/A for single predictor)
- (7) Influential observations

If CTT models show assumption violations, this represents an inherent limitation of bounded scales for trajectory modeling (Cogn-IQ, 2024). The z-standardization (Step 6) partially mitigates scale differences by equalizing variance, but does not resolve distributional shape issues.

**CRITICAL:** Bounded-scale limitation applies to BOTH Full and Purified CTT, suggesting that relative AIC differences (Purified vs Full) remain interpretable even if absolute AIC values are elevated due to scale constraints.

**Input:**

**File 1:** Fitted LMM model objects from Step 7 (6 models in memory or saved as .pkl)
**File 2:** data/step06_standardized_scores.csv (for residual extraction)

**Processing:**

For EACH of the 6 fitted models:

1. **Linearity Check:**
   - Plot: Residuals vs fitted values
   - Expected: Random scatter around y=0 with no systematic pattern
   - Violation: Curved pattern (indicates nonlinear relationship)

2. **Homoscedasticity Check:**
   - Plot: Scale-location plot (sqrt(|residuals|) vs fitted)
   - Test: Breusch-Pagan test (p > 0.05 = homoscedastic)
   - Violation: Funnel shape or significant BP test

3. **Normality of Residuals:**
   - Plot: Q-Q plot of residuals
   - Test: Shapiro-Wilk test (p > 0.05 = normal) OR visual assessment for n>50
   - Violation: Deviation from diagonal line, significant SW test

4. **Normality of Random Effects:**
   - Plot: Q-Q plot of BLUPs (intercepts and slopes)
   - Test: Shapiro-Wilk test per random effect
   - Violation: Heavy tails or skewness

5. **Independence Check:**
   - Plot: Residuals vs observation order
   - Test: Durbin-Watson test (1.5-2.5 acceptable)
   - Violation: DW < 1.5 or > 2.5 (autocorrelation)

6. **Multicollinearity Check:**
   - N/A (single predictor Time only)

7. **Influential Observations:**
   - Compute Cook's distance per observation
   - Threshold: Cook's D < 1.0
   - Violation: Any observation with D > 1.0

**Document violations:** Create assumption_validation.csv with pass/fail per criterion per model.

**Output:**

**File:** data/step07.5_assumption_validation.csv
**Format:** CSV with 42 rows (6 models x 7 assumption tests)
**Columns:**
  - model (string): Model identifier (e.g., "Source_IRT", "Destination_Full_CTT")
  - assumption (string): Assumption name (Linearity, Homoscedasticity, Normality_Residuals, Normality_RandomEffects, Independence, Multicollinearity, Influential_Observations)
  - test_statistic (float): Test statistic value if applicable (e.g., Breusch-Pagan chi-square, Shapiro-Wilk W, Durbin-Watson)
  - p_value (float): p-value if applicable (NaN for visual checks)
  - threshold (string): Decision threshold (e.g., "p > 0.05", "DW in [1.5, 2.5]", "Cook's D < 1.0")
  - result (string): "PASS" or "FAIL"
  - notes (string): Additional context (e.g., "Mild floor effect observed", "CTT bounded scale limitation")
**Expected Rows:** 42

**Validation Requirement:**

Validation tools MUST be used after assumption validation. Specific validation tools determined by rq_tools based on assumption test result patterns.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07.5_assumption_validation.csv: 42 rows x 7 columns
- Columns: model (object), assumption (object), test_statistic (float64), p_value (float64), threshold (object), result (object), notes (object)

*Value Ranges:*
- test_statistic: unrestricted (depends on test)
- p_value in [0, 1] where applicable
- result in {"PASS", "FAIL"}

*Data Quality:*
- All 42 rows present (6 models x 7 assumptions)
- model in {"Source_IRT", "Source_Full_CTT", "Source_Purified_CTT", "Destination_IRT", "Destination_Full_CTT", "Destination_Purified_CTT"}
- assumption in {Linearity, Homoscedasticity, Normality_Residuals, Normality_RandomEffects, Independence, Multicollinearity, Influential_Observations}
- No NaN in result column (PASS/FAIL must be determined)

*Log Validation:*
- Required pattern: "Assumption validation: 42 tests (6 models x 7 assumptions)"
- Required pattern: "IRT models: [X/7] assumptions passed"
- Required pattern: "CTT Full models: [X/7] assumptions passed"
- Required pattern: "CTT Purified models: [X/7] assumptions passed"
- Required pattern: "CTT bounded scale limitations documented"
- Forbidden patterns: "ERROR", "Assumption validation failed to complete"

**Expected Behavior on Validation Failure:**

If IRT models show violations:
- Raise WARNING: "IRT theta scale showing assumption violations - investigate"
- Proceed with analysis (document limitation)

If CTT models show violations:
- **EXPECTED OUTCOME** (bounded [0,1] scale)
- Log: "CTT models show assumption violations due to bounded scale - this is expected and documented"
- Proceed with analysis (relative AIC comparison remains valid)

If >50% of assumptions fail across all models:
- Raise CLARITY ERROR: "Widespread assumption violations suggest fundamental modeling issue"
- QUIT immediately (investigate upstream data quality or model specification)

---

### Step 8: Prepare Plot Data

**Dependencies:** Steps 4-5, 7 (requires reliability, correlations, AIC comparison)
**Complexity:** Low (data aggregation for plotting)

**Purpose:** Create plot source CSV files for visualization of correlation comparison and AIC comparison results.

**Input:**

**File 1:** data/step04_reliability_assessment.csv
**File 2:** data/step05_correlation_analysis.csv
**File 3:** data/step07_lmm_model_comparison.csv

**Processing:**

**Plot 1: Correlation Comparison**

Create data for plotting Full vs Purified CTT correlations with IRT theta, separately for source and destination memory.

Reshape correlation data to plot-friendly format:
- 4 rows: (Source, Full), (Source, Purified), (Destination, Full), (Destination, Purified)
- Columns: location_type, version, r, CI_lower, CI_upper

For CI computation:
- Use Fisher's z-transformation: z = 0.5 * ln((1+r)/(1-r))
- SE(z) H 1 / sqrt(n-3)
- 95% CI for z: z ± 1.96 * SE(z)
- Back-transform to r scale

**Plot 2: AIC Comparison**

Create data for plotting AIC values across measurement types, separately for source and destination.

Reshape AIC data:
- 6 rows: (Source, IRT), (Source, Full CTT), (Source, Purified CTT), (Destination, IRT), (Destination, Full CTT), (Destination, Purified CTT)
- Columns: location_type, model, aic, delta_aic_interpretation

For delta_aic_interpretation:
- Reference model = Full CTT per location type
- ”AIC = AIC(model) - AIC(Full CTT)
- Interpretation: "”AIC = +X.X (substantial)" if ”AIC > 2, etc.

**Output:**

**File 1:** plots/step08_correlation_comparison_data.csv
**Format:** CSV for correlation comparison plot
**Columns:**
  - location_type (string): "source" or "destination"
  - version (string): "full" or "purified"
  - r (float): Pearson correlation with IRT theta
  - CI_lower (float): Lower 95% confidence bound for r
  - CI_upper (float): Upper 95% confidence bound for r
**Expected Rows:** 4 (2 location types x 2 versions)

**File 2:** plots/step08_aic_comparison_data.csv
**Format:** CSV for AIC comparison plot
**Columns:**
  - location_type (string): "source" or "destination"
  - model (string): "IRT", "Full_CTT", or "Purified_CTT"
  - aic (float): AIC value from LMM
  - delta_aic (float): AIC - AIC(Full CTT) per location type
  - interpretation (string): Evidence strength per Burnham & Anderson (2002)
**Expected Rows:** 6 (2 location types x 3 models)

**Validation Requirement:**

Validation tools MUST be used after plot data preparation. Specific validation tools determined by rq_tools based on plot data completeness checks.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- plots/step08_correlation_comparison_data.csv: 4 rows x 5 columns
- plots/step08_aic_comparison_data.csv: 6 rows x 5 columns

*Value Ranges:*
- r in [0.50, 1.00] (correlations)
- CI_lower, CI_upper in [0, 1] (correlation bounds)
- CI_upper > CI_lower for all rows
- aic values finite
- delta_aic finite

*Data Quality:*
- All rows present (4 for correlation, 6 for AIC)
- No NaN values in critical columns
- All location_type and version/model combinations present
- Correlation plot: CI bands non-overlapping with 0

*Log Validation:*
- Required pattern: "Plot data prepared: 2 files"
- Required pattern: "Correlation plot: 4 rows (2 locations x 2 versions)"
- Required pattern: "AIC plot: 6 rows (2 locations x 3 models)"
- Required pattern: "All CIs valid (CI_upper > CI_lower)"
- Forbidden patterns: "ERROR", "Missing plot data", "NaN in plot data"

**Expected Behavior on Validation Failure:**

If any CI_upper <= CI_lower:
- Raise TOOL ERROR: "Confidence interval computation error"
- QUIT immediately

If any row missing:
- Raise CLARITY ERROR: "Incomplete plot data - missing location type or version"
- QUIT immediately

---

## Expected Data Formats

### data/step01_item_mapping.csv

**Format:** CSV, one row per item
**Dimensions:** 36 rows x 6 columns
**Purpose:** Document which items retained vs removed during purification

**Column Schema:**
- item_name (string): Full tag (VR-{paradigm}-{test}-{location}-ANS-{item})
- location_type (string): "source" or "destination"
- a (float): IRT discrimination parameter
- b (float): IRT difficulty parameter
- retained (bool): True if passed Decision D039 thresholds
- removal_reason (string): "retained" | "low_discrimination" | "extreme_difficulty" | "both"

**Value Constraints:**
- a >= 0 (discrimination non-negative)
- b unrestricted (difficulty can be extreme before purification)
- Retention rate per location type in [0.55, 0.85]

---

### data/step02_ctt_full_scores.csv

**Format:** CSV, long format (UID x test x location_type)
**Dimensions:** 800 rows x 4 columns
**Purpose:** CTT sum scores using all items (before purification)

**Column Schema:**
- UID (string): Participant identifier
- test (string): Test session (T1, T2, T3, T4)
- location_type (string): "source" or "destination"
- ctt_full_score (float): Mean proportion correct across all items

**Value Constraints:**
- ctt_full_score in [0, 1] (bounded scale)
- No NaN values (all participants completed all tests)

---

### data/step05_correlation_analysis.csv

**Format:** CSV, summary table
**Dimensions:** 2 rows x 9 columns
**Purpose:** Correlation comparison with Steiger's z-test results

**Column Schema:**
- location_type (string): "source" or "destination"
- r_full (float): Correlation(IRT theta, Full CTT)
- r_purified (float): Correlation(IRT theta, Purified CTT)
- delta_r (float): r_purified - r_full
- r_full_purified (float): Correlation(Full CTT, Purified CTT)
- steiger_z (float): Z-statistic from Steiger's test
- p_uncorrected (float): Uncorrected p-value (Decision D068)
- p_bonferroni (float): Bonferroni-corrected p-value (alpha=0.025)
- n (int): Sample size (400)

**Value Constraints:**
- All correlations in [0, 1] (positive convergence expected)
- p_bonferroni >= p_uncorrected (correction cannot reduce p-value)
- Dual p-values MANDATORY per Decision D068

---

### data/step07_lmm_model_comparison.csv

**Format:** CSV, summary table
**Dimensions:** 2 rows x 8 columns
**Purpose:** AIC comparison across measurement types

**Column Schema:**
- location_type (string): "source" or "destination"
- aic_irt (float): AIC for IRT z-scores
- aic_ctt_full (float): AIC for Full CTT z-scores
- aic_ctt_purified (float): AIC for Purified CTT z-scores
- delta_aic_full_purified (float): AIC(Purified) - AIC(Full)
- interpretation (string): Evidence strength per Burnham & Anderson (2002)
- n_observations (int): 400
- converged_all (bool): True if all 3 models converged

**Value Constraints:**
- All AIC values finite (no NaN or infinite)
- delta_aic typically in [-50, +50]
- converged_all = True (required for valid comparison)

---

## Cross-RQ Dependencies

**Dependency Type:** DERIVED Data from RQ 5.5.1 (Source-Destination Trajectories, ROOT)

**This RQ requires outputs from RQ 5.5.1:**

**File 1:** results/ch5/5.5.1/data/step02_purified_items.csv
**Used in:** Step 1 (item mapping)
**Rationale:** RQ 5.5.1 performs IRT calibration and purification. This RQ uses those purification results to compare Full vs Purified CTT.

**File 2:** results/ch5/5.5.1/data/step03_theta_scores.csv
**Used in:** Steps 0, 5, 6 (correlation analysis, z-standardization)
**Rationale:** RQ 5.5.1 generates IRT theta estimates. This RQ correlates CTT scores with those theta values to test measurement convergence.

**File 3:** results/ch5/5.5.1/data/step00_tsvr_mapping.csv
**Used in:** Step 7 (LMM time variable)
**Rationale:** TSVR (Time Since VR) provides actual elapsed time per participant-test for trajectory modeling.

**File 4:** data/cache/dfData.csv (project-level raw data)
**Used in:** Steps 2-3 (CTT computation)
**Rationale:** Raw binary item responses needed to compute CTT sum scores on full and purified item sets.

**Execution Order Constraint:**

1. RQ 5.5.1 must complete first (status = success in results/ch5/5.5.1/status.yaml)
2. This RQ (5.5.5) executes second (uses RQ 5.5.1 outputs)

**Data Source Boundaries:**

- **RAW data:** dfData.csv (project-level, created outside analysis pipeline)
- **DERIVED data:** All RQ 5.5.1 outputs (theta, purified items, TSVR mapping)
- **Scope:** This RQ does NOT re-calibrate IRT models (reuses RQ 5.5.1 theta and purification results)

**Validation:**

Step 0 validates RQ 5.5.1 completion:
- Check results/ch5/5.5.1/status.yaml: rq_results.status = "success"
- If status != success: QUIT with EXPECTATIONS ERROR
- If any required file missing: QUIT with EXPECTATIONS ERROR

**Reference:** Per workflow.md Section 5, DERIVED data RQs must document dependencies explicitly with execution order constraints and circuit breakers.

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

---

### Validation Requirements By Step

#### Step 0: Load and Validate RQ 5.5.1 Dependencies

**Analysis Tool:** (determined by rq_tools - likely tools.validation.check_file_exists + custom dependency validator)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_data_format for theta/TSVR structure)

**What Validation Checks:**
- RQ 5.5.1 status.yaml: rq_results.status = "success"
- All 5 input files exist
- purified_items.csv: 36 rows, retention rate 55-85%
- theta_scores.csv: 400 rows, theta in [-4,4], no NaN
- TSVR_mapping.csv: 400 rows, matches theta_scores UIDs/tests
- dfData.csv: contains required -U- and -D- item columns

**Expected Behavior on Validation Failure:**
- Missing file: EXPECTATIONS ERROR -> QUIT
- RQ 5.5.1 incomplete: EXPECTATIONS ERROR -> QUIT
- Retention rate out of bounds: CLARITY ERROR -> QUIT

---

#### Step 1: Map Retained vs Removed Items

**Analysis Tool:** (determined by rq_tools - likely pandas filtering + categorization)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure for item mapping)

**What Validation Checks:**
- 36 rows (18 source + 18 destination)
- Retention rate per location type in [0.55, 0.85]
- removal_reason values valid
- At least 10 retained items per location type

**Expected Behavior on Validation Failure:**
- Retention < 55%: WARNING -> proceed
- Retention < 28% (<10 items): CLARITY ERROR -> QUIT

---

#### Step 2: Compute Full CTT Sum Scores

**Analysis Tool:** (determined by rq_tools - likely custom CTT computation function)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_probability_range for CTT scores in [0,1])

**What Validation Checks:**
- 800 rows (400 per location type)
- ctt_full_score in [0, 1]
- No NaN values
- All UIDs from theta_scores present

**Expected Behavior on Validation Failure:**
- Score out of [0,1]: TOOL ERROR -> QUIT
- NaN detected: CLARITY ERROR -> QUIT

---

#### Step 3: Compute Purified CTT Sum Scores

**Analysis Tool:** (determined by rq_tools - likely custom CTT computation on filtered items)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_probability_range)

**What Validation Checks:**
- 800 rows matching Full CTT structure
- ctt_purified_score in [0, 1]
- No NaN values
- High correlation with Full CTT (r > 0.85 expected)

**Expected Behavior on Validation Failure:**
- Score out of [0,1]: TOOL ERROR -> QUIT
- Low correlation with Full CTT: WARNING -> proceed

---

#### Step 4: Reliability Assessment

**Analysis Tool:** (determined by rq_tools - likely tools.ctt.compute_cronbachs_alpha with bootstrap)
**Validation Tool:** (determined by rq_tools - likely custom alpha range validator)

**What Validation Checks:**
- 4 rows (2 locations x 2 versions)
- alpha in [0.60, 0.95]
- Bootstrap CIs non-overlapping with 0
- CI_upper > CI_lower

**Expected Behavior on Validation Failure:**
- alpha < 0.60: WARNING -> proceed (document limitation)
- alpha > 0.95: WARNING -> proceed (item redundancy)
- Bootstrap failure: TOOL ERROR -> QUIT

---

#### Step 5: Correlation Analysis with Steiger's Z-Test

**Analysis Tool:** (determined by rq_tools - likely tools.ctt.compare_correlations_dependent)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_correlation_test_d068 for dual p-values)

**What Validation Checks:**
- 2 rows (source, destination)
- All correlations in [0.50, 1.00]
- Dual p-values present (p_uncorrected, p_bonferroni) per Decision D068
- p_bonferroni >= p_uncorrected

**Expected Behavior on Validation Failure:**
- Correlation < 0.50: WARNING -> proceed
- p_bonferroni < p_uncorrected: TOOL ERROR -> QUIT (logic error)
- Missing dual p-values: SCOPE ERROR -> QUIT (Decision D068 violation)

---

#### Step 6: Z-Standardize All Measurements

**Analysis Tool:** (determined by rq_tools - likely custom z-score transformation)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_standardization)

**What Validation Checks:**
- 800 rows
- All 6 z-score columns: mean H 0 (±0.05), SD H 1 (±0.05) per location type
- No NaN values

**Expected Behavior on Validation Failure:**
- Standardization incorrect: TOOL ERROR -> QUIT
- NaN detected: CLARITY ERROR -> QUIT

---

#### Step 7: Fit Parallel LMMs and Compare AIC

**Analysis Tool:** (determined by rq_tools - likely tools.lmm.fit_lmm_trajectory_tsvr for 6 models)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_model_convergence + custom AIC validator)

**What Validation Checks:**
- 2 rows (source, destination)
- All 6 models converged (converged_all = True)
- All AIC values finite
- delta_aic_full_purified finite

**Expected Behavior on Validation Failure:**
- Model convergence failed: WARNING -> attempt simplification -> QUIT if still fails
- AIC NaN or infinite: TOOL ERROR -> QUIT

---

#### Step 7.5: Validate LMM Assumptions

**Analysis Tool:** (determined by rq_tools - likely tools.validation.validate_lmm_assumptions_comprehensive for 6 models)
**Validation Tool:** (determined by rq_tools - likely custom assumption result aggregator)

**What Validation Checks:**
- 42 rows (6 models x 7 assumptions)
- All assumptions evaluated (no missing rows)
- result in {"PASS", "FAIL"}
- CTT bounded scale violations documented

**Expected Behavior on Validation Failure:**
- IRT model violations: WARNING -> proceed (investigate)
- CTT model violations: EXPECTED -> proceed (document bounded scale limitation)
- >50% failures across all models: CLARITY ERROR -> QUIT

---

#### Step 8: Prepare Plot Data

**Analysis Tool:** (determined by rq_tools - likely custom plot data aggregation)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_plot_data_completeness)

**What Validation Checks:**
- Correlation plot: 4 rows, CI_upper > CI_lower
- AIC plot: 6 rows, all location_type x model combinations present
- No NaN values

**Expected Behavior on Validation Failure:**
- Missing rows: CLARITY ERROR -> QUIT
- CI inversion: TOOL ERROR -> QUIT

---

## Summary

**Total Steps:** 9 (Step 0 + Steps 1-7.5 + Step 8)
**Estimated Runtime:** ~30-45 minutes
- Low complexity: Steps 0-4, 6, 8 (~15 minutes)
- Medium complexity: Steps 5, 7, 7.5 (~15-30 minutes)

**Cross-RQ Dependencies:** RQ 5.5.1 (must complete before this RQ)

**Primary Outputs:**
- Item mapping with retention status (data/step01_item_mapping.csv)
- Full and Purified CTT scores (data/step02_ctt_full_scores.csv, data/step03_ctt_purified_scores.csv)
- Reliability comparison (data/step04_reliability_assessment.csv)
- Correlation comparison with Steiger's z-test (data/step05_correlation_analysis.csv)
- LMM AIC comparison (data/step07_lmm_model_comparison.csv)
- Assumption validation results (data/step07.5_assumption_validation.csv)
- Plot source data (plots/step08_correlation_comparison_data.csv, plots/step08_aic_comparison_data.csv)

**Validation Coverage:** 100% (all 9 steps have validation requirements with substance criteria)

**Paradox Test:**
If paradox replicates (expected):
- Purified CTT r > Full CTT r (Steiger's z p < 0.025 Bonferroni)
- Purified CTT AIC > Full CTT AIC + 2 (substantial evidence favoring Full CTT for trajectories)

If paradox fails (unexpected):
- Report null correlation difference OR Purified CTT shows equal/better AIC
- Interpret: Source-destination memory may have different psychometric properties vs Domains/Paradigms/Congruence

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate - manual approval)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts
5. Workflow continues to Step 14: bash executes scripts -> rq_inspect validates outputs
6. Workflow continues to Step 15: rq_plots generates visualizations (reads plots/*.csv)
7. Workflow continues to Step 16: rq_results generates summary.md

---

**Version History:**
- v1.0 (2025-12-04): Initial plan created by rq_planner agent for RQ 5.5.5 (Purified CTT Effects for Source-Destination)
