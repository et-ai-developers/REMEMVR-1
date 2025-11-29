# Analysis Plan for RQ 5.12: Does purified IRT item set change CTT conclusions?

**Created by:** rq_planner agent
**Date:** 2025-11-30
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This RQ examines methodological convergence between Classical Test Theory (CTT) and Item Response Theory (IRT) by comparing trajectory conclusions from three measurement approaches: (a) full CTT using all items, (b) purified CTT using only IRT-retained items, and (c) IRT theta scores. The analysis tests whether IRT item purification (removing poorly discriminating items with a < 0.5 or extreme difficulty |b| > 4.0 per RQ 5.1) improves CTT-IRT convergence, suggesting that purification removes measurement noise rather than signal.

**Pipeline:** CTT computation (full + purified) + Correlation analysis + Parallel LMM comparison

**Steps:** 9 total analysis steps (Step 0: data loading through Step 8: plot data preparation)

**Estimated Runtime:** Medium complexity (~30-45 minutes total)
- Data loading/mapping: Low (~2 min)
- CTT computation (2 passes): Low (~5 min)
- Reliability assessment: Low (~3 min)
- Correlation analysis: Low (~2 min)
- Standardization: Low (~1 min)
- Parallel LMM fitting (3 models): High (~20-30 min)
- Plot data preparation: Low (~2 min)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (Steiger's z-test for dependent correlations)
- Decision D070: TSVR as time variable (inherited from RQ 5.1 LMM inputs)
- Decision D069: Dual-scale trajectory plots NOT applicable (methodological comparison, not trajectory analysis per se)
- Project-specific: Cronbach's alpha with bootstrap CIs (reliability validation)
- Project-specific: Parallel LMM design with z-score standardization (valid AIC comparison per Burnham & Anderson)

**Critical Methodological Notes:**
- **Dependent Correlations:** Full CTT, Purified CTT, and IRT theta from same N=100 participants -> Steiger's z-test required (Fisher's r-to-z invalid)
- **AIC Comparison Validity:** Different scales (CTT [0,1] vs IRT theta [logit]) -> z-score standardization mandatory before LMM fitting
- **Purification Criteria from RQ 5.1:** Uses actual discrimination thresholds (0.5 <= a <= 4.0) applied in RQ 5.1 purification

---

## Analysis Plan

### Step 0: Load Data Sources

**Dependencies:** None (first step, but requires RQ 5.1 completion)

**Complexity:** Low (file reading, no computation)

**Purpose:** Load IRT item parameters, theta scores, TSVR mapping from RQ 5.1 and raw dichotomized scores from dfData.csv for CTT computation.

**Input:**

**File 1:** results/ch5/rq1/data/step02_purified_items.csv
**Source:** RQ 5.1 Step 2 (IRT purification output)
**Format:** CSV with columns:
  - `item_name` (string, format: TQ_{paradigm}-{tag}-i{N}, e.g., TQ_ICR-N-i1)
  - `factor` (string, domain: "what", "where", "when")
  - `a` (float, discrimination parameter, range: [0.5, 4.0] after purification)
  - `b` (float, difficulty parameter, unrestricted range)
**Expected Rows:** ~38 items (purified subset from full ~50 items)
**Note:** This file contains IRT-retained items. Items NOT in this list were excluded by RQ 5.1 purification.

**File 2:** results/ch5/rq1/data/step03_theta_scores.csv
**Source:** RQ 5.1 Step 3 (IRT Pass 2 theta extraction)
**Format:** CSV with columns:
  - `composite_ID` (string, format: {UID}_{test}, e.g., A010_1)
  - `theta_what` (float, IRT ability estimate for What domain)
  - `theta_where` (float, IRT ability estimate for Where domain)
  - `theta_when` (float, IRT ability estimate for When domain)
**Expected Rows:** ~400 (100 participants x 4 tests)

**File 3:** results/ch5/rq1/data/step00_tsvr_mapping.csv
**Source:** RQ 5.1 Step 0 (TSVR time variable extraction)
**Format:** CSV with columns:
  - `composite_ID` (string, format: {UID}_{test})
  - `UID` (string, participant identifier)
  - `test` (int, values: {1, 2, 3, 4})
  - `TSVR_hours` (float, actual hours since encoding)
**Expected Rows:** ~400 (100 participants x 4 tests)

**File 4:** data/cache/dfData.csv
**Source:** Project-level raw data cache (dichotomized scores)
**Format:** CSV with columns:
  - `UID` (string, participant identifier)
  - `TEST` (int, values: {1, 2, 3, 4})
  - `TQ_*` columns (int, dichotomized 0/1 item responses for all items)
**Expected Rows:** ~400 (100 participants x 4 tests)
**Note:** This is RAW data source for CTT computation (dichotomization already applied)

**Processing:**
- Load all 4 files using pd.read_csv()
- Verify expected column names match exactly (case-sensitive)
- Verify row counts in expected range (380-400 rows for files 2-4)
- Create composite_ID in dfData by merging UID and TEST (format: {UID}_{TEST})
- No transformations yet (just loading and validation)

**Output:**

**File 1:** data/step00_irt_purified_items.csv (copy of RQ 5.1 purified items for local reference)
**Format:** CSV, same schema as input File 1
**Expected Rows:** ~38 items

**File 2:** data/step00_theta_scores.csv (copy of RQ 5.1 theta for local reference)
**Format:** CSV, same schema as input File 2
**Expected Rows:** ~400

**File 3:** data/step00_tsvr_mapping.csv (copy of RQ 5.1 TSVR for local reference)
**Format:** CSV, same schema as input File 3
**Expected Rows:** ~400

**File 4:** data/step00_raw_scores.csv (dfData with composite_ID added)
**Format:** CSV with columns:
  - `composite_ID` (string, format: {UID}_{test})
  - `UID` (string)
  - `TEST` (int)
  - `TQ_*` columns (int, all item responses)
**Expected Rows:** ~400

**Validation Requirement:**
Validation tools MUST be used after data loading execution. Specific validation tools will be determined by rq_tools based on file existence and format checks.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_irt_purified_items.csv: 38 rows x 4 columns (item_name: object, factor: object, a: float64, b: float64)
- data/step00_theta_scores.csv: 400 rows x 4 columns (composite_ID: object, theta_what: float64, theta_where: float64, theta_when: float64)
- data/step00_tsvr_mapping.csv: 400 rows x 4 columns (composite_ID: object, UID: object, test: int64, TSVR_hours: float64)
- data/step00_raw_scores.csv: 400 rows x 53+ columns (composite_ID, UID, TEST, TQ_* items)

*Value Ranges:*
- a in [0.5, 4.0] (purified discrimination range from RQ 5.1)
- b unrestricted (difficulty can be extreme for temporal items)
- theta_* in [-3, 3] (typical IRT ability range)
- TSVR_hours in [0, 200] hours (max ~8 days)
- TQ_* in {0, 1} (dichotomized responses)
- test in {1, 2, 3, 4} (test sessions)

*Data Quality:*
- No NaN in item_name, factor, a, b columns (purified items complete)
- No NaN in composite_ID, theta_* columns (all participants estimated)
- No NaN in composite_ID, UID, test, TSVR_hours (complete TSVR mapping)
- Expected N: All 4 files have 380-400 rows (allowing for some exclusions)
- composite_ID format validation: matches {UID}_{test} pattern
- No duplicate composite_IDs within any file

*Log Validation:*
- Required: "Loaded 4 data sources successfully"
- Required: "Created composite_ID in dfData: {N} rows"
- Required: "VALIDATION - PASS: All files loaded with expected structure"
- Forbidden: "ERROR", "FileNotFoundError", "Missing columns"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "File not found: results/ch5/rq1/data/step02_purified_items.csv")
- Log failure to logs/step00_load_data.log
- Quit immediately (cannot proceed without RQ 5.1 outputs)
- User must ensure RQ 5.1 Steps 0-3 completed successfully before running this RQ

**Cross-RQ Dependency Check:**
This step MUST verify results/ch5/rq1/status.yaml shows step03_theta_scores = success before proceeding. If RQ 5.1 incomplete, QUIT with:
```
EXPECTATIONS ERROR: RQ 5.12 requires RQ 5.1 completion (Steps 0-3).
Current RQ 5.1 status: {status from status.yaml}
Required: rq_inspect.status = success (validates Step 3 theta extraction)
Action: Complete RQ 5.1 before running RQ 5.12
```

---

### Step 1: Map Items to Full vs Purified Sets

**Dependencies:** Step 0 (requires purified item list and raw scores)

**Complexity:** Low (set operations, no modeling)

**Purpose:** Identify which TQ_* items in dfData.csv were retained vs excluded by RQ 5.1 purification. Create full item list (all TQ_*) and purified item list (only items in step00_irt_purified_items.csv) for downstream CTT computation.

**Input:**

**File 1:** data/step00_irt_purified_items.csv
**Columns used:** `item_name`, `factor`
**Purpose:** List of IRT-retained items per domain

**File 2:** data/step00_raw_scores.csv
**Columns used:** Column names matching pattern `TQ_*`
**Purpose:** Extract full item list from dfData column names

**Processing:**
- Extract all column names from dfData matching pattern `TQ_*` -> full_item_list
- Extract item_name values from purified_items.csv -> purified_item_list
- Group purified items by domain (factor column): what_items, where_items, when_items
- Group full items by domain using tag patterns:
  - What (full): TQ_*-N-* items
  - Where (full): TQ_*-U-* + TQ_*-D-* items (RQ 5.1 used -U- and -D-, not -L-)
  - When (full): TQ_*-O-* items
- Compute removed items: full_item_list - purified_item_list (set difference)
- Count items per domain: full vs purified (for reporting)

**Output:**

**File 1:** data/step01_item_mapping.csv
**Format:** CSV with columns:
  - `item_name` (string, TQ_* item name)
  - `domain` (string, "what", "where", "when")
  - `retained` (bool, True if in purified set, False if removed)
**Expected Rows:** ~50 items (all TQ_* items from dfData)
**Column Details:**
  - item_name: exact match to TQ_* column names in dfData
  - domain: derived from tag pattern (*-N-* = what, *-U-*/*-D-* = where, *-O-* = when)
  - retained: True for ~38 items, False for ~12 items

**File 2:** logs/step01_item_counts.txt
**Format:** Text report
**Content:**
```
Item Mapping Summary
--------------------
Full CTT Item Counts:
  What: {N} items
  Where: {N} items
  When: {N} items
  Total: {N} items

Purified CTT Item Counts:
  What: {N} items (retained)
  Where: {N} items (retained)
  When: {N} items (retained)
  Total: {N} items (retained)

Removed Items:
  What: {N} items ({percent}%)
  Where: {N} items ({percent}%)
  When: {N} items ({percent}%)
  Total: {N} items ({percent}%)

Expected Counts (from thesis):
  Full: 50 items (18 What, 16 Where, 16 When)
  Purified: ~38 items (14 What, 12 Where, 12 When)
  Removed: ~12 items (24% removal rate)
```

**Validation Requirement:**
Validation tools MUST be used after item mapping execution. Specific validation tools determined by rq_tools based on set operation validation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_item_mapping.csv: 50 rows x 3 columns (item_name: object, domain: object, retained: bool)
- logs/step01_item_counts.txt: Text file with counts per domain

*Value Ranges:*
- domain in {"what", "where", "when"} (categorical)
- retained in {True, False} (boolean)
- Total items: 48-52 (allowing for slight variation)
- Retained items: 36-40 (~75% retention expected)
- Removed items: 10-14 (~25% removal expected)

*Data Quality:*
- No NaN in any column (complete mapping)
- All item_name values match TQ_* pattern
- All purified items from step00_irt_purified_items.csv have retained=True
- No duplicate item_name values
- All three domains represented (what, where, when)

*Log Validation:*
- Required: "Item mapping complete: {N} full items, {N} purified items"
- Required: "Retention rate: {percent}% (expected ~75%)"
- Required: "VALIDATION - PASS: Item mapping"
- Forbidden: "ERROR", "Unexpected domain", "Missing items"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Retention rate 45% far below expected 75%")
- Log failure to logs/step01_map_items.log
- Quit immediately (incorrect mapping will cascade to CTT computation)

---

### Step 2: Compute Full CTT Scores

**Dependencies:** Step 0, Step 1 (requires raw scores and full item list)

**Complexity:** Low (simple mean computation, no modeling)

**Purpose:** Calculate Classical Test Theory scores using ALL items (full item set) per UID x Test x Domain. CTT score = mean of dichotomized item responses (0/1) within domain.

**Input:**

**File 1:** data/step00_raw_scores.csv
**Columns used:** composite_ID, UID, TEST, TQ_* (all item columns)

**File 2:** data/step01_item_mapping.csv
**Columns used:** item_name, domain (all items, not filtered by retained)

**Processing:**
- For each domain (what, where, when):
  - Select all items matching domain pattern (all items, not just retained)
  - Group by composite_ID
  - Compute mean of dichotomized responses (0/1) -> CTT_full_{domain}
  - CTT score range: [0, 1] (proportion correct)
- Merge domain scores into single DataFrame
- Add UID and TEST columns from composite_ID parsing

**Output:**

**File:** data/step02_ctt_full_scores.csv
**Format:** CSV with columns:
  - `composite_ID` (string, format: {UID}_{test})
  - `UID` (string, participant identifier)
  - `TEST` (int, values: {1, 2, 3, 4})
  - `CTT_full_what` (float, range: [0, 1], mean score for What domain all items)
  - `CTT_full_where` (float, range: [0, 1], mean score for Where domain all items)
  - `CTT_full_when` (float, range: [0, 1], mean score for When domain all items)
**Expected Rows:** ~400 (100 participants x 4 tests)

**Validation Requirement:**
Validation tools MUST be used after CTT computation execution. Specific validation tools determined by rq_tools based on numeric range validation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_ctt_full_scores.csv: 400 rows x 6 columns (composite_ID: object, UID: object, TEST: int64, CTT_full_what: float64, CTT_full_where: float64, CTT_full_when: float64)

*Value Ranges:*
- CTT_full_* in [0, 1] (proportion correct range)
- TEST in {1, 2, 3, 4} (test sessions)
- No negative values (CTT is proportion)
- No values > 1.0 (maximum proportion)

*Data Quality:*
- No NaN in composite_ID, UID, TEST (complete participant data)
- NaN acceptable in CTT_full_* ONLY if participant missing all items for domain (rare)
- Expected N: 400 rows (100 participants x 4 tests)
- No duplicate composite_IDs
- Distribution check: CTT_full_* approximately normal or slightly skewed (typical for ability measures)

*Log Validation:*
- Required: "Computed full CTT scores for {N} observations"
- Required: "Mean CTT_full_what: {value}, SD: {value}"
- Required: "Mean CTT_full_where: {value}, SD: {value}"
- Required: "Mean CTT_full_when: {value}, SD: {value}"
- Required: "VALIDATION - PASS: CTT full scores in valid range"
- Forbidden: "ERROR", "Values outside [0,1]", "All NaN for domain"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "CTT_full_what contains values > 1.0")
- Log failure to logs/step02_compute_full_ctt.log
- Quit immediately (invalid CTT scores cannot be compared to IRT)

---

### Step 3: Compute Purified CTT Scores

**Dependencies:** Step 0, Step 1 (requires raw scores and purified item list)

**Complexity:** Low (filtered mean computation, no modeling)

**Purpose:** Calculate Classical Test Theory scores using ONLY IRT-retained items (purified item set) per UID x Test x Domain. Same computation as Step 2, but filtered item list.

**Input:**

**File 1:** data/step00_raw_scores.csv
**Columns used:** composite_ID, UID, TEST, TQ_* (all item columns)

**File 2:** data/step01_item_mapping.csv
**Columns used:** item_name, domain, retained
**Filter:** retained == True (only purified items)

**Processing:**
- For each domain (what, where, when):
  - Select ONLY items with retained=True from item_mapping
  - Group by composite_ID
  - Compute mean of dichotomized responses (0/1) -> CTT_purified_{domain}
  - CTT score range: [0, 1] (proportion correct, but fewer items than full CTT)
- Merge domain scores into single DataFrame
- Add UID and TEST columns from composite_ID parsing

**Output:**

**File:** data/step03_ctt_purified_scores.csv
**Format:** CSV with columns:
  - `composite_ID` (string, format: {UID}_{test})
  - `UID` (string, participant identifier)
  - `TEST` (int, values: {1, 2, 3, 4})
  - `CTT_purified_what` (float, range: [0, 1], mean score for What domain purified items)
  - `CTT_purified_where` (float, range: [0, 1], mean score for Where domain purified items)
  - `CTT_purified_when` (float, range: [0, 1], mean score for When domain purified items)
**Expected Rows:** ~400 (100 participants x 4 tests)

**Validation Requirement:**
Validation tools MUST be used after purified CTT computation execution. Specific validation tools determined by rq_tools based on numeric range validation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_ctt_purified_scores.csv: 400 rows x 6 columns (composite_ID: object, UID: object, TEST: int64, CTT_purified_what: float64, CTT_purified_where: float64, CTT_purified_when: float64)

*Value Ranges:*
- CTT_purified_* in [0, 1] (proportion correct range)
- TEST in {1, 2, 3, 4} (test sessions)
- No negative values
- No values > 1.0

*Data Quality:*
- No NaN in composite_ID, UID, TEST
- NaN acceptable in CTT_purified_* ONLY if participant missing all purified items for domain (rare)
- Expected N: 400 rows (same as full CTT)
- No duplicate composite_IDs
- Distribution check: CTT_purified_* similar to CTT_full_* (correlation r > 0.95 expected)

*Log Validation:*
- Required: "Computed purified CTT scores for {N} observations"
- Required: "Using {N} purified items (vs {N} full items)"
- Required: "Mean CTT_purified_what: {value}, SD: {value}"
- Required: "Mean CTT_purified_where: {value}, SD: {value}"
- Required: "Mean CTT_purified_when: {value}, SD: {value}"
- Required: "VALIDATION - PASS: CTT purified scores in valid range"
- Forbidden: "ERROR", "Values outside [0,1]", "No purified items for domain"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "CTT_purified_when all NaN - no retained items")
- Log failure to logs/step03_compute_purified_ctt.log
- Quit immediately (cannot compare full vs purified if purified computation fails)

---

### Step 4: CTT Reliability Assessment

**Dependencies:** Step 0, Step 1, Step 2, Step 3 (requires raw item responses and item mappings)

**Complexity:** Low (Cronbach's alpha with bootstrap, ~3 min)

**Purpose:** Compute Cronbach's alpha internal consistency for both full and purified CTT item sets per domain. Bootstrap 95% confidence intervals validate whether purification maintains or improves reliability. Uses tools.analysis_ctt.compute_cronbachs_alpha() per 1_concept.md specification.

**Input:**

**File 1:** data/step00_raw_scores.csv
**Columns used:** TQ_* item columns (dichotomized 0/1 responses)

**File 2:** data/step01_item_mapping.csv
**Columns used:** item_name, domain, retained

**Processing:**
- For each domain (what, where, when):
  - **Full CTT reliability:**
    - Select all items for domain (retained=True OR False)
    - Extract item responses from raw_scores (rows x items matrix)
    - Call tools.analysis_ctt.compute_cronbachs_alpha(items_matrix, n_bootstrap=1000)
    - Returns: alpha_full, CI_lower_full, CI_upper_full
  - **Purified CTT reliability:**
    - Select only retained items for domain (retained=True)
    - Extract item responses from raw_scores (rows x items matrix)
    - Call tools.analysis_ctt.compute_cronbachs_alpha(items_matrix, n_bootstrap=1000)
    - Returns: alpha_purified, CI_lower_purified, CI_upper_purified
- Compare alpha_full vs alpha_purified per domain (interpretation below)

**Output:**

**File:** results/step04_reliability_assessment.csv
**Format:** CSV with columns:
  - `domain` (string, "what", "where", "when")
  - `alpha_full` (float, Cronbach's alpha for full item set)
  - `CI_lower_full` (float, bootstrap 95% CI lower bound)
  - `CI_upper_full` (float, bootstrap 95% CI upper bound)
  - `alpha_purified` (float, Cronbach's alpha for purified item set)
  - `CI_lower_purified` (float, bootstrap 95% CI lower bound)
  - `CI_upper_purified` (float, bootstrap 95% CI upper bound)
  - `delta_alpha` (float, alpha_purified - alpha_full, positive = improvement)
**Expected Rows:** 3 (one per domain: what, where, when)

**Interpretation Logic (documented in log):**
- If alpha_purified > alpha_full AND CIs non-overlapping -> "Purification improved reliability"
- If alpha_purified >= alpha_full - 0.05 AND CIs overlapping -> "Purification maintained reliability (no significant decline)"
- If alpha_purified < alpha_full - 0.05 AND CIs non-overlapping -> "Purification reduced reliability (removed meaningful variance from CTT perspective)"

**Validation Requirement:**
Validation tools MUST be used after reliability assessment execution. Specific validation tools determined by rq_tools based on alpha value validation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step04_reliability_assessment.csv: 3 rows x 8 columns (domain: object, alpha_full: float64, CI_lower_full: float64, CI_upper_full: float64, alpha_purified: float64, CI_lower_purified: float64, CI_upper_purified: float64, delta_alpha: float64)

*Value Ranges:*
- alpha_* in [0, 1] (Cronbach's alpha bounds)
- CI_lower_* in [0, 1] and <= alpha_* (lower bound)
- CI_upper_* in [0, 1] and >= alpha_* (upper bound)
- delta_alpha in [-1, 1] (difference bounded by alpha range)
- Typical alpha values: [0.70, 0.95] (acceptable to excellent internal consistency)

*Data Quality:*
- Exactly 3 rows (what, where, when)
- No NaN values (all domains must have computable alpha)
- CI_lower < alpha < CI_upper for all domains (valid bootstrap CIs)
- domain in {"what", "where", "when"}
- Bootstrap completed: 1000 iterations per domain (documented in log)

*Log Validation:*
- Required: "Computing Cronbach's alpha with 1000 bootstrap iterations"
- Required: "Domain what: alpha_full={value} [{CI_lower}, {CI_upper}], alpha_purified={value} [{CI_lower}, {CI_upper}]"
- Required: "Domain where: alpha_full={value} [{CI_lower}, {CI_upper}], alpha_purified={value} [{CI_lower}, {CI_upper}]"
- Required: "Domain when: alpha_full={value} [{CI_lower}, {CI_upper}], alpha_purified={value} [{CI_lower}, {CI_upper}]"
- Required: "Interpretation: {interpretation per logic above}"
- Required: "VALIDATION - PASS: All alpha values in [0,1]"
- Forbidden: "ERROR", "Alpha outside [0,1]", "Bootstrap failed"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Alpha computation failed for domain what")
- Log failure to logs/step04_assess_reliability.log
- Quit immediately (reliability validation is critical for CTT interpretation)

---

### Step 5: Correlation Analysis with Steiger's z-test

**Dependencies:** Step 0, Step 2, Step 3 (requires theta scores, full CTT, purified CTT)

**Complexity:** Low (correlation + hypothesis test, ~2 min)

**Purpose:** Test primary hypothesis that purified CTT correlates more strongly with IRT theta than full CTT. Uses Steiger's z-test for dependent correlations (Decision D068 principle applied to correlation testing). Computes three pairwise correlations per domain and tests H0: r(Full CTT, IRT) = r(Purified CTT, IRT).

**Input:**

**File 1:** data/step00_theta_scores.csv
**Columns used:** composite_ID, theta_what, theta_where, theta_when

**File 2:** data/step02_ctt_full_scores.csv
**Columns used:** composite_ID, CTT_full_what, CTT_full_where, CTT_full_when

**File 3:** data/step03_ctt_purified_scores.csv
**Columns used:** composite_ID, CTT_purified_what, CTT_purified_where, CTT_purified_when

**Processing:**
- Merge all three DataFrames on composite_ID
- For each domain (what, where, when):
  - Compute three Pearson correlations:
    - r12 = corr(Full CTT, IRT theta)
    - r13 = corr(Full CTT, Purified CTT)
    - r23 = corr(Purified CTT, IRT theta)
  - Call tools.analysis_ctt.compare_correlations_dependent(r12, r13, r23, n=400)
    - Tests H0: r12 = r23 (Full CTT-IRT vs Purified CTT-IRT)
    - Uses Steiger's (1980) formula for dependent correlations
    - Returns: z_statistic, p_uncorrected, p_bonferroni (3 domains -> correction factor 3)
  - Interpret: If p_bonferroni < 0.05 -> significant improvement from purification

**Output:**

**File:** results/step05_correlation_analysis.csv
**Format:** CSV with columns:
  - `domain` (string, "what", "where", "when")
  - `r_full_irt` (float, correlation between full CTT and IRT theta)
  - `r_purified_irt` (float, correlation between purified CTT and IRT theta)
  - `r_full_purified` (float, correlation between full CTT and purified CTT)
  - `delta_r` (float, r_purified_irt - r_full_irt, positive = improvement)
  - `steiger_z` (float, z-statistic for dependent correlation test)
  - `p_uncorrected` (float, uncorrected p-value)
  - `p_bonferroni` (float, Bonferroni-corrected p-value for 3 comparisons)
  - `interpretation` (string, "Significant improvement", "No significant difference", or "Significant decline")
**Expected Rows:** 3 (one per domain)

**Validation Requirement:**
Validation tools MUST be used after correlation analysis execution. Specific validation tools determined by rq_tools based on correlation validation (uses validate_correlation_test_d068 for dual p-value validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step05_correlation_analysis.csv: 3 rows x 9 columns (domain: object, r_full_irt: float64, r_purified_irt: float64, r_full_purified: float64, delta_r: float64, steiger_z: float64, p_uncorrected: float64, p_bonferroni: float64, interpretation: object)

*Value Ranges:*
- r_* in [-1, 1] (correlation bounds)
- Expected r_* in [0.85, 0.98] (high convergence expected between methods)
- delta_r in [-0.5, 0.5] (difference in correlations)
- Expected delta_r in [0, 0.05] (modest improvement hypothesis)
- steiger_z unrestricted (z-statistic)
- p_uncorrected in [0, 1] (p-value range)
- p_bonferroni in [0, 1] (corrected p-value)
- interpretation in {"Significant improvement", "No significant difference", "Significant decline"}

*Data Quality:*
- Exactly 3 rows (what, where, when)
- No NaN in correlation values (all computable)
- r_purified_irt >= r_full_irt expected (hypothesis direction)
- r_full_purified > 0.90 expected (high overlap between full and purified CTT)
- Dual p-values present: BOTH p_uncorrected AND p_bonferroni (Decision D068)

*Log Validation:*
- Required: "Domain what: r(Full,IRT)={value}, r(Purified,IRT)={value}, delta_r={value}"
- Required: "Steiger's z-test: z={value}, p_uncorrected={value}, p_bonferroni={value}"
- Required: "Domain where: r(Full,IRT)={value}, r(Purified,IRT)={value}, delta_r={value}"
- Required: "Steiger's z-test: z={value}, p_uncorrected={value}, p_bonferroni={value}"
- Required: "Domain when: r(Full,IRT)={value}, r(Purified,IRT)={value}, delta_r={value}"
- Required: "Steiger's z-test: z={value}, p_uncorrected={value}, p_bonferroni={value}"
- Required: "VALIDATION - PASS: Dual p-values present for all domains"
- Forbidden: "ERROR", "Correlation undefined", "Missing p-value"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Missing p_bonferroni for domain what")
- Log failure to logs/step05_correlation_analysis.log
- Quit immediately (correlation test is primary hypothesis test)

**Decision D068 Application:**
This step applies Decision D068 (dual p-value reporting) to correlation testing. Although D068 primarily addresses post-hoc contrasts, the principle extends to all hypothesis tests: report BOTH uncorrected and corrected p-values for transparent exploratory analysis. Steiger's z-test used because correlations are DEPENDENT (same N=100 participants contribute to all three correlations per domain).

---

### Step 6: Standardize Outcomes for Parallel LMM

**Dependencies:** Step 0, Step 2, Step 3 (requires theta, full CTT, purified CTT)

**Complexity:** Low (z-score transformation, ~1 min)

**Purpose:** Standardize all three measurement approaches (Full CTT, Purified CTT, IRT theta) to z-scores to enable valid AIC comparison per Burnham & Anderson. Different outcome scales (CTT [0,1] vs IRT theta [logit]) violate AIC identical-data requirement. Standardization ensures all three LMMs fit to comparable scales.

**Input:**

**File 1:** data/step00_theta_scores.csv
**Columns used:** composite_ID, theta_what, theta_where, theta_when

**File 2:** data/step02_ctt_full_scores.csv
**Columns used:** composite_ID, CTT_full_what, CTT_full_where, CTT_full_when

**File 3:** data/step03_ctt_purified_scores.csv
**Columns used:** composite_ID, CTT_purified_what, CTT_purified_where, CTT_purified_when

**File 4:** data/step00_tsvr_mapping.csv
**Columns used:** composite_ID, UID, TSVR_hours

**Processing:**
- Merge all files on composite_ID
- Reshape to long format (one row per observation):
  - Variables: composite_ID, UID, TSVR_hours, domain, measurement_type, value
  - measurement_type in {"Full CTT", "Purified CTT", "IRT theta"}
  - domain in {"what", "where", "when"}
- For each measurement_type x domain combination:
  - Compute z-score: z = (value - mean(value)) / sd(value)
  - Save as z_{measurement_type}_{domain}
- Verify standardization: mean(z) approximately 0, sd(z) approximately 1 (tolerance: ±0.01 for sampling variation)

**Output:**

**File:** data/step06_standardized_outcomes.csv
**Format:** CSV, long format with columns:
  - `composite_ID` (string, format: {UID}_{test})
  - `UID` (string, participant identifier)
  - `TSVR_hours` (float, time variable for LMM)
  - `domain` (string, "what", "where", "when")
  - `z_full_ctt` (float, z-scored full CTT)
  - `z_purified_ctt` (float, z-scored purified CTT)
  - `z_irt_theta` (float, z-scored IRT theta)
**Expected Rows:** ~1200 (400 composite_IDs x 3 domains)

**Validation Requirement:**
Validation tools MUST be used after standardization execution. Specific validation tools determined by rq_tools based on standardization validation (uses validate_standardization tool).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_standardized_outcomes.csv: 1200 rows x 7 columns (composite_ID: object, UID: object, TSVR_hours: float64, domain: object, z_full_ctt: float64, z_purified_ctt: float64, z_irt_theta: float64)

*Value Ranges:*
- z_* approximately in [-3, 3] (typical z-score range, outliers possible)
- TSVR_hours in [0, 200] (inherited from step 0)
- domain in {"what", "where", "when"}

*Data Quality:*
- Exactly 1200 rows (400 composite_IDs x 3 domains)
- No NaN in z_* columns (all values standardizable)
- Standardization validation per domain x measurement:
  - mean(z_full_ctt | domain) approximately 0 (tolerance: ±0.01)
  - sd(z_full_ctt | domain) approximately 1 (tolerance: ±0.01)
  - Same for z_purified_ctt and z_irt_theta
- No duplicate composite_ID x domain combinations

*Log Validation:*
- Required: "Standardizing Full CTT: domain what (mean={value}, sd={value})"
- Required: "Standardizing Purified CTT: domain what (mean={value}, sd={value})"
- Required: "Standardizing IRT theta: domain what (mean={value}, sd={value})"
- Required: "Post-standardization validation: all means within ±0.01 of 0, SDs within ±0.01 of 1"
- Required: "VALIDATION - PASS: Standardization successful"
- Forbidden: "ERROR", "Mean far from 0", "SD far from 1"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "z_full_ctt mean = 0.15 (exceeds tolerance ±0.01)")
- Log failure to logs/step06_standardize_outcomes.log
- Quit immediately (invalid standardization breaks AIC comparison validity)

**Critical Methodological Note:**
Per Burnham & Anderson (2002, *Model Selection and Multimodel Inference*), AIC comparison requires identical data across models. Comparing LMMs with different outcome scales (CTT [0,1] vs IRT theta [logit]) violates this requirement because likelihood values are on different scales. Z-score standardization maps all three measurements to same scale (mean=0, SD=1), enabling valid AIC comparison while preserving relative differences within each measurement approach.

---

### Step 7: Fit Parallel LMMs to Standardized Outcomes

**Dependencies:** Step 6 (requires standardized outcomes)

**Complexity:** High (3 LMM models, ~20-30 min)

**Purpose:** Fit identical LMM formulas to three standardized measurement approaches (Full CTT, Purified CTT, IRT theta) and compare AIC to test which measurement approach provides best model fit. Uses LMM formula from RQ 5.1 with TSVR time variable (Decision D070). Parallel design isolates measurement method effects by holding model structure constant.

**Input:**

**File:** data/step06_standardized_outcomes.csv
**Columns used:** UID, TSVR_hours, domain, z_full_ctt, z_purified_ctt, z_irt_theta

**Processing:**
- For each measurement approach (Full CTT, Purified CTT, IRT theta):
  - Fit LMM: z_outcome ~ (TSVR_hours + log(TSVR_hours+1)) x domain + (TSVR_hours | UID)
  - Formula breakdown:
    - Fixed effects: Main effects of time (linear + log), domain, and Time x Domain interaction
    - Random effects: Random intercepts and slopes for TSVR_hours per participant (UID)
  - Extract AIC, BIC, log-likelihood
  - Extract fixed effects table (coefficients, SE, z, p-values)
  - Extract random effects variance components
- Compare AICs: delta_AIC = AIC_measurement - AIC_IRT (IRT as reference)
- Interpret per Burnham & Anderson:
  - delta_AIC < 2: Equivalent fit
  - delta_AIC 2-10: Moderate support for lower AIC model
  - delta_AIC > 10: Substantial support for lower AIC model

**Output:**

**File 1:** results/step07_lmm_model_comparison.csv
**Format:** CSV with columns:
  - `measurement` (string, "Full CTT", "Purified CTT", "IRT theta")
  - `AIC` (float, Akaike Information Criterion)
  - `BIC` (float, Bayesian Information Criterion)
  - `logLik` (float, log-likelihood)
  - `delta_AIC` (float, AIC - AIC_IRT, where IRT is reference)
  - `interpretation` (string, "Equivalent", "Moderate support", "Substantial support" per Burnham & Anderson)
**Expected Rows:** 3 (one per measurement approach)

**File 2:** results/step07_lmm_full_ctt_summary.txt
**Format:** Statsmodels LMM summary text (fixed effects, random effects, fit indices)

**File 3:** results/step07_lmm_purified_ctt_summary.txt
**Format:** Statsmodels LMM summary text (fixed effects, random effects, fit indices)

**File 4:** results/step07_lmm_irt_theta_summary.txt
**Format:** Statsmodels LMM summary text (fixed effects, random effects, fit indices)

**File 5:** results/step07_lmm_full_ctt_fixed_effects.csv
**Format:** CSV with columns: term, coef, se, z, p (fixed effects table)

**File 6:** results/step07_lmm_purified_ctt_fixed_effects.csv
**Format:** CSV with columns: term, coef, se, z, p (fixed effects table)

**File 7:** results/step07_lmm_irt_theta_fixed_effects.csv
**Format:** CSV with columns: term, coef, se, z, p (fixed effects table)

**Validation Requirement:**
Validation tools MUST be used after LMM fitting execution. Specific validation tools determined by rq_tools based on LMM convergence and fit validation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step07_lmm_model_comparison.csv: 3 rows x 6 columns (measurement: object, AIC: float64, BIC: float64, logLik: float64, delta_AIC: float64, interpretation: object)
- results/step07_lmm_*_summary.txt: Text files (3 total, one per measurement)
- results/step07_lmm_*_fixed_effects.csv: 3 CSV files with ~9 rows each (terms: intercept, time, log(time), domain[where], domain[when], time:domain, logtime:domain)

*Value Ranges:*
- AIC unrestricted (lower is better, typical range: 3000-5000)
- BIC unrestricted (lower is better, typical range: 3100-5100)
- logLik unrestricted (higher is better, typical range: -1400 to -1600)
- delta_AIC: Expected order: IRT (0.0, reference), Purified CTT (+10 to +20), Full CTT (+30 to +40)
- Coefficients unrestricted (on z-score scale)
- SE > 0 (all standard errors positive)
- p in [0, 1] (p-value range)

*Data Quality:*
- All 3 models converged successfully (check summary files for convergence warnings)
- No NaN in AIC, BIC, logLik (all models fitted)
- delta_AIC for IRT theta = 0.0 exactly (reference model)
- delta_AIC for Full CTT >= delta_AIC for Purified CTT (hypothesis: purification improves fit)
- Fixed effects tables have ~9 terms each (intercept + time + log(time) + 2 domains + 4 interactions)

*Log Validation:*
- Required: "Fitting LMM: Full CTT (z-standardized)"
- Required: "Model converged: True"
- Required: "AIC={value}, BIC={value}, logLik={value}"
- Required: "Fitting LMM: Purified CTT (z-standardized)"
- Required: "Model converged: True"
- Required: "AIC={value}, BIC={value}, logLik={value}"
- Required: "Fitting LMM: IRT theta (z-standardized)"
- Required: "Model converged: True"
- Required: "AIC={value}, BIC={value}, logLik={value}"
- Required: "Model comparison: delta_AIC(Full CTT)={value}, delta_AIC(Purified CTT)={value}"
- Required: "VALIDATION - PASS: All models converged, AIC comparison valid"
- Forbidden: "ERROR", "Convergence failed", "Singular covariance"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "LMM Full CTT failed to converge")
- Log failure to logs/step07_fit_parallel_lmms.log
- Quit immediately (non-convergent models cannot be compared via AIC)

**Decision D070 Application:**
This step uses TSVR_hours as time variable (actual hours since encoding) per Decision D070, not nominal days (0, 1, 3, 6). TSVR ensures accurate temporal modeling given participant session scheduling variability.

**Methodological Notes:**
- **Parallel LMM design:** Identical formula across all three measurements isolates measurement method effects (Full CTT vs Purified CTT vs IRT) by holding model structure constant
- **Z-score standardization:** Enables valid AIC comparison per Burnham & Anderson (identical data requirement)
- **Expected AIC pattern:** IRT best fit (lowest AIC), Purified CTT intermediate (delta_AIC ~10-20), Full CTT worst fit (delta_AIC ~30-40), validating that IRT purification improves measurement precision and CTT-IRT convergence

---

### Step 8: Prepare Plot Data (Methodological Comparison Visualization)

**Dependencies:** Step 2, Step 3, Step 4, Step 5, Step 7 (requires all CTT scores, correlations, LMM results)

**Complexity:** Low (data aggregation for plotting, ~2 min)

**Purpose:** Create plot source CSVs for methodological comparison visualizations per Option B architecture. Two plots planned: (1) Correlation comparison showing r(Full CTT, IRT) vs r(Purified CTT, IRT) per domain, (2) AIC comparison showing model fit across three measurement approaches.

**Input:**

**File 1:** results/step05_correlation_analysis.csv
**Columns used:** domain, r_full_irt, r_purified_irt, delta_r, p_bonferroni

**File 2:** results/step07_lmm_model_comparison.csv
**Columns used:** measurement, AIC, delta_AIC, interpretation

**Processing:**
- **Plot 1 Data (Correlation Comparison):**
  - Reshape correlation_analysis.csv to long format:
    - Columns: domain, measurement_type, correlation, significance
    - measurement_type in {"Full CTT", "Purified CTT"}
    - correlation = r_full_irt or r_purified_irt
    - significance = "Significant" if p_bonferroni < 0.05 else "Not significant"
  - Save to plots/step08_correlation_comparison_data.csv

- **Plot 2 Data (AIC Comparison):**
  - Use lmm_model_comparison.csv directly
  - Add significance marker: delta_AIC > 10 = "Substantial", 2-10 = "Moderate", <2 = "Equivalent"
  - Save to plots/step08_aic_comparison_data.csv

**Output:**

**File 1:** plots/step08_correlation_comparison_data.csv
**Format:** CSV with columns:
  - `domain` (string, "what", "where", "when")
  - `measurement_type` (string, "Full CTT", "Purified CTT")
  - `correlation` (float, r with IRT theta)
  - `significance` (string, "Significant improvement" if Steiger's test p_bonferroni < 0.05, else "Not significant")
**Expected Rows:** 6 (3 domains x 2 measurement types)
**Plot Description:** Grouped bar chart comparing Full CTT-IRT vs Purified CTT-IRT correlations per domain. Y-axis: correlation (r), X-axis: domain, grouped by measurement type. Error bars not needed (point estimates). Significance markers (* if p_bonferroni < 0.05).

**File 2:** plots/step08_aic_comparison_data.csv
**Format:** CSV with columns:
  - `measurement` (string, "Full CTT", "Purified CTT", "IRT theta")
  - `AIC` (float, Akaike Information Criterion)
  - `delta_AIC` (float, difference from IRT reference)
  - `interpretation` (string, "Equivalent", "Moderate support", "Substantial support")
**Expected Rows:** 3 (one per measurement approach)
**Plot Description:** Bar chart showing AIC values for three measurement approaches. Y-axis: delta_AIC (IRT as reference = 0), X-axis: measurement type. Lower delta_AIC = better fit. Include Burnham & Anderson thresholds (dashed lines at delta_AIC = 2 and 10).

**Validation Requirement:**
Validation tools MUST be used after plot data preparation execution. Specific validation tools determined by rq_tools based on plot data completeness validation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- plots/step08_correlation_comparison_data.csv: 6 rows x 4 columns (domain: object, measurement_type: object, correlation: float64, significance: object)
- plots/step08_aic_comparison_data.csv: 3 rows x 4 columns (measurement: object, AIC: float64, delta_AIC: float64, interpretation: object)

*Value Ranges:*
- correlation in [0.85, 0.98] (expected high convergence)
- AIC unrestricted (typical range: 3000-5000)
- delta_AIC in [0, 100] (IRT = 0, others positive)
- significance in {"Significant improvement", "Not significant"}
- interpretation in {"Equivalent", "Moderate support", "Substantial support"}
- measurement_type in {"Full CTT", "Purified CTT"} (Plot 1)
- measurement in {"Full CTT", "Purified CTT", "IRT theta"} (Plot 2)

*Data Quality:*
- Plot 1: Exactly 6 rows (3 domains x 2 types)
- Plot 2: Exactly 3 rows (3 measurements)
- All domains represented in Plot 1: what, where, when
- All measurements represented in Plot 2: Full CTT, Purified CTT, IRT theta
- No NaN values
- No duplicate domain x measurement_type combinations (Plot 1)
- No duplicate measurement values (Plot 2)

*Log Validation:*
- Required: "Prepared correlation comparison data: 6 rows (3 domains x 2 types)"
- Required: "Prepared AIC comparison data: 3 rows (3 measurements)"
- Required: "All domains represented: what, where, when"
- Required: "All measurements represented: Full CTT, Purified CTT, IRT theta"
- Required: "VALIDATION - PASS: Plot data complete"
- Forbidden: "ERROR", "Missing domain", "Missing measurement", "NaN detected"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Missing domain when in correlation comparison data")
- Log failure to logs/step08_prepare_plot_data.log
- Quit immediately (incomplete plot data cannot generate valid visualizations)

**Plotting Function (rq_plots will call):**
- Plot 1: Grouped bar chart (compare correlations)
- Plot 2: Bar chart with reference line (compare AIC with delta_AIC = 0 as baseline)
- rq_plots agent maps these descriptions to tools/plots.py functions
- No data aggregation in rq_plots (visualization only per Option B)

**Note:** Decision D069 (dual-scale trajectory plots) NOT applicable here. This RQ is methodological comparison (not trajectory analysis per se). Plots show method convergence, not temporal trajectories.

---

## Expected Data Formats

### Data Transformations

**Step 0 -> Step 1:** File loading + composite_ID creation
- Input: 4 separate files (RQ 5.1 outputs + dfData.csv)
- Output: Local copies with composite_ID standardized

**Step 1 -> Steps 2-3:** Item filtering
- Input: Full item list from dfData column names
- Output: Retained (purified) vs removed item mapping
- Transformation: Set operations (retained = items in purified_items.csv)

**Steps 2-3 -> Step 4:** CTT score computation
- Input: Raw dichotomized responses (0/1) from dfData
- Output: Mean scores per domain (proportion correct)
- Transformation: Group by composite_ID, compute mean within domain

**Steps 2-3 -> Step 5:** Correlation testing
- Input: CTT scores (full + purified) + IRT theta
- Output: Pairwise correlations + Steiger's z-test
- Transformation: Merge on composite_ID, compute correlations, test dependent correlation differences

**Steps 0, 2-3 -> Step 6:** Z-score standardization
- Input: CTT scores (full + purified) + IRT theta (different scales)
- Output: Z-scored outcomes (mean=0, SD=1)
- Transformation: (value - mean) / SD per measurement_type x domain

**Step 6 -> Step 7:** Parallel LMM fitting
- Input: Standardized outcomes (long format)
- Output: 3 fitted LMMs with identical formula
- Transformation: statsmodels MixedLM fitting per measurement approach

**Steps 5, 7 -> Step 8:** Plot data preparation
- Input: Correlation analysis + LMM comparison results
- Output: Plot source CSVs (reshaped for visualization)
- Transformation: Reshape to plotting format, add significance markers

### Column Naming Conventions

Per names.md (populated from RQ 5.1):

**Core Identifiers:**
- `composite_ID` (format: {UID}_{test}, e.g., A010_1)
- `UID` (participant identifier)
- `TEST` or `test` (test session: {1, 2, 3, 4})

**Time Variable:**
- `TSVR_hours` (actual hours since encoding per Decision D070)

**IRT Outputs:**
- `theta_what`, `theta_where`, `theta_when` (IRT ability estimates per domain)
- `a` (item discrimination), `b` (item difficulty)

**CTT Outputs (new for RQ 5.12):**
- `CTT_full_{domain}` (full item set scores)
- `CTT_purified_{domain}` (purified item set scores)
- `z_full_ctt`, `z_purified_ctt`, `z_irt_theta` (standardized outcomes)

**Analysis Outputs:**
- `alpha_full`, `alpha_purified` (Cronbach's alpha)
- `r_full_irt`, `r_purified_irt` (correlations)
- `delta_r` (correlation difference)
- `delta_AIC` (AIC difference)

### Data Type Constraints

**Nullable vs Non-Nullable:**
- composite_ID, UID, domain: Non-nullable (required for all rows)
- CTT_*, theta_*: Non-nullable after computation (NaN only if missing all items, rare)
- TSVR_hours: Non-nullable (time variable required)
- Correlations, AIC: Non-nullable (all computable)

**Valid Ranges:**
- CTT scores: [0, 1] (proportion correct)
- IRT theta: [-3, 3] (typical ability range)
- Z-scores: approximately [-3, 3] (outliers possible)
- Cronbach's alpha: [0, 1] (typical: [0.70, 0.95])
- Correlations: [-1, 1] (expected: [0.85, 0.98])
- p-values: [0, 1]
- AIC: unrestricted (lower is better)

**Categorical Values:**
- domain: {"what", "where", "when"}
- measurement: {"Full CTT", "Purified CTT", "IRT theta"}
- test: {1, 2, 3, 4}

---

## Cross-RQ Dependencies

### Dependency Type 2: DERIVED Data from Other RQs (Dependencies Exist)

**This RQ requires outputs from:**
- **RQ 5.1** (Domain-Specific Forgetting Trajectories)
  - File 1: results/ch5/rq1/data/step02_purified_items.csv
    - Used in: Step 0 (load purified item list), Step 1 (identify retained items)
    - Rationale: RQ 5.1 IRT purification identified high-quality items (0.5 <= a <= 4.0). This RQ tests whether CTT computed on those items converges toward IRT conclusions.
  - File 2: results/ch5/rq1/data/step03_theta_scores.csv
    - Used in: Step 0 (load theta), Step 5 (correlation analysis), Step 6 (standardization), Step 7 (parallel LMM)
    - Rationale: IRT theta serves as gold standard for convergent validity testing.
  - File 3: results/ch5/rq1/data/step00_tsvr_mapping.csv
    - Used in: Step 0 (load TSVR), Step 6 (merge time variable), Step 7 (LMM time predictor)
    - Rationale: TSVR (actual hours since encoding) per Decision D070 ensures accurate temporal modeling in parallel LMMs.

**Execution Order Constraint:**
1. RQ 5.1 must complete Steps 0-3 first (provides purified items, theta scores, TSVR mapping)
2. This RQ executes after RQ 5.1 validation complete (rq_inspect.status = success for RQ 5.1)

**Data Source Boundaries (Per Specification 5.1.6):**
- **RAW data:** data/cache/dfData.csv (dichotomized TQ_* item responses for CTT computation)
- **DERIVED data:** Outputs from RQ 5.1 (purified items, theta, TSVR)
- **Scope:** This RQ does NOT re-run IRT calibration (uses RQ 5.1 purification criteria as fixed). This RQ does NOT modify RQ 5.1 outputs (read-only access).

**Validation:**
- Step 0: Check results/ch5/rq1/data/step02_purified_items.csv exists (EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch5/rq1/data/step03_theta_scores.csv exists (EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch5/rq1/data/step00_tsvr_mapping.csv exists (EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch5/rq1/status.yaml shows step03_theta_scores = success (EXPECTATIONS ERROR if not complete)
- If any file missing -> quit with error -> user must execute RQ 5.1 first

**Reference:** Specification section 5.1.6 (Data Source Boundaries)

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

**Step 0: Load Data Sources**
- Validation Tool: validate_data_columns, check_file_exists
- Checks: All 4 files exist, expected columns present, row counts in range
- Failure -> QUIT: "File missing or malformed"

**Step 1: Map Items to Full vs Purified Sets**
- Validation Tool: validate_dataframe_structure
- Checks: 50 items total, ~38 retained, all domains present
- Failure -> QUIT: "Item mapping incomplete"

**Step 2: Compute Full CTT Scores**
- Validation Tool: validate_numeric_range
- Checks: CTT_full_* in [0, 1], no NaN except if all items missing
- Failure -> QUIT: "CTT full scores out of range"

**Step 3: Compute Purified CTT Scores**
- Validation Tool: validate_numeric_range
- Checks: CTT_purified_* in [0, 1], similar to full CTT (r > 0.95)
- Failure -> QUIT: "CTT purified scores invalid"

**Step 4: CTT Reliability Assessment**
- Validation Tool: validate_numeric_range (alpha in [0,1])
- Checks: alpha_* in [0, 1], CI_lower < alpha < CI_upper
- Failure -> QUIT: "Cronbach's alpha computation failed"

**Step 5: Correlation Analysis with Steiger's z-test**
- Validation Tool: validate_correlation_test_d068 (dual p-values)
- Checks: Correlations in [-1, 1], dual p-values present, r_purified >= r_full expected
- Failure -> QUIT: "Correlation test missing dual p-values or out of range"

**Step 6: Standardize Outcomes**
- Validation Tool: validate_standardization
- Checks: mean(z) approximately 0, sd(z) approximately 1 per measurement x domain
- Failure -> QUIT: "Standardization failed (mean or SD out of tolerance)"

**Step 7: Fit Parallel LMMs**
- Validation Tool: validate_model_convergence, validate_lmm_convergence
- Checks: All 3 models converged, no singular covariance, AIC computable
- Failure -> QUIT: "LMM convergence failed"

**Step 8: Prepare Plot Data**
- Validation Tool: validate_plot_data_completeness
- Checks: All domains present, all measurements present, no NaN
- Failure -> QUIT: "Plot data incomplete"

---

## Summary

**Total Steps:** 9 (Step 0 through Step 8)

**Estimated Runtime:** Medium complexity (~30-45 minutes total)
- Data loading: ~2 min
- Item mapping: ~1 min
- CTT computation (2 passes): ~5 min
- Reliability assessment: ~3 min
- Correlation analysis: ~2 min
- Standardization: ~1 min
- Parallel LMM fitting: ~20-30 min (3 models)
- Plot data preparation: ~2 min

**Cross-RQ Dependencies:** RQ 5.1 (must complete Steps 0-3 before this RQ can run)

**Primary Outputs:**
- CTT scores (full + purified) per domain: data/step02_ctt_full_scores.csv, data/step03_ctt_purified_scores.csv
- Reliability assessment: results/step04_reliability_assessment.csv
- Correlation analysis with Steiger's z-test: results/step05_correlation_analysis.csv
- Parallel LMM comparison: results/step07_lmm_model_comparison.csv + 7 additional files
- Plot source CSVs: plots/step08_correlation_comparison_data.csv, plots/step08_aic_comparison_data.csv

**Validation Coverage:** 100% (all 9 steps have validation requirements with 4-layer substance criteria)

**Key Methodological Innovations:**
- Steiger's z-test for dependent correlations (3 overlapping correlations per domain)
- Z-score standardization for valid AIC comparison across different outcome scales
- Parallel LMM design isolating measurement method effects
- Cronbach's alpha with bootstrap CIs for reliability validation
- Hybrid CTT-IRT approach testing whether CTT benefits from IRT item selection

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-11-30): Initial plan created by rq_planner agent for RQ 5.12 (methodological CTT-IRT convergence analysis)
