# Analysis Plan: RQ 5.12 - Does Purified IRT Item Set Change CTT Conclusions?

**Research Question:** 5.12
**Created:** 2025-11-26
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines methodological convergence between Classical Test Theory (CTT) and Item Response Theory (IRT) by comparing trajectory conclusions from three measurement approaches: (a) Full CTT (all items), (b) Purified CTT (IRT-retained items only), and (c) IRT theta scores. The analysis tests whether IRT item purification removes noise (improving CTT-IRT convergence) or signal (degrading CTT validity).

**Pipeline:** Hybrid CTT-IRT methodological comparison
**Steps:** 9 analysis steps (Step 0: data loading, Steps 1-8: analyses)
**Estimated Runtime:** Medium (~45-60 minutes total)

**Key Decisions Applied:**
- Decision D039: Use RQ 5.1 purification criteria (0.5 <= a <= 4.0) to identify retained items
- Decision D068: Dual p-value reporting in post-hoc contrasts (uncorrected + Bonferroni)
- Decision D070: TSVR as time variable for LMM trajectories (actual hours, not nominal days)
- NEW: Z-score standardization for valid AIC comparison across different measurement scales (Burnham & Anderson requirement)
- NEW: Steiger's z-test for dependent correlations (correct method for overlapping samples)
- NEW: Cronbach's alpha with bootstrap 95% CIs for CTT reliability assessment

**Cross-RQ Dependencies:**
This RQ requires completed outputs from RQ 5.1 (IRT item parameters, theta scores, TSVR mapping). Execution order: RQ 5.1 must complete before RQ 5.12.

---

## Analysis Plan

### Step 0: Load Data from Multiple Sources

**Dependencies:** None (first step, but requires RQ 5.1 completion)
**Complexity:** Low (~2 minutes data loading)

**Purpose:** Load IRT outputs from RQ 5.1 and raw data for CTT computation

**Input:**

**File 1:** results/ch5/rq1/data/step02_purified_items.csv
**Source:** RQ 5.1 Step 2 (item purification)
**Format:** CSV with columns:
  - `item_name` (string, format: VR-{paradigm}-{test}-{domain}-ANS, e.g., VR-IFR-A01-N-ANS)
  - `dimension` (string, values: {common, congruent, incongruent} from RQ 5.1 3-factor model)
  - `a` (float, discrimination parameter, range: [0.5, 4.0] after purification)
  - `b` (float, difficulty parameter, unrestricted range)
**Expected Rows:** ~38 items (12 removed by purification, ~50 original)
**Circuit Breaker:** If file missing -> EXPECTATIONS ERROR "RQ 5.1 must complete Step 2 (purification) before RQ 5.12 can run"

**File 2:** results/ch5/rq1/data/step03_theta_scores.csv
**Source:** RQ 5.1 Step 3 (Pass 2 theta extraction)
**Format:** CSV with columns:
  - `composite_ID` (string, format: {UID}_{test}, e.g., P001_T1)
  - `theta_common` (float, range: [-3, 3] typical)
  - `se_common` (float, standard error, range: [0.1, 1.0])
  - `theta_congruent` (float, range: [-3, 3])
  - `se_congruent` (float, range: [0.1, 1.0])
  - `theta_incongruent` (float, range: [-3, 3])
  - `se_incongruent` (float, range: [0.1, 1.0])
**Expected Rows:** ~400 (100 participants x 4 tests)
**Circuit Breaker:** If file missing -> EXPECTATIONS ERROR "RQ 5.1 must complete Step 3 (theta extraction) before RQ 5.12 can run"

**File 3:** results/ch5/rq1/data/step00_tsvr_mapping.csv
**Source:** RQ 5.1 Step 0 (TSVR extraction)
**Format:** CSV with columns:
  - `composite_ID` (string, format: {UID}_{test})
  - `TSVR_hours` (float, range: [0, 300] hours typical, 0=encoding, 168=1 week)
  - `test` (string, values: {T1, T2, T3, T4})
  - `UID` (string, participant identifier)
**Expected Rows:** ~400
**Circuit Breaker:** If file missing -> EXPECTATIONS ERROR "RQ 5.1 must complete Step 0 (TSVR extraction) before RQ 5.12 can run"

**File 4:** data/cache/dfData.csv
**Source:** Project-level raw data cache (dichotomized item responses)
**Format:** CSV with columns:
  - `UID` (string, participant identifier)
  - `test` (string, values: {T1, T2, T3, T4})
  - Item response columns: TQ_{domain}_{variant}_{number} (int, values: {0, 1, NaN})
    - Example: TQ_N_F_01 (What domain, Face variant, item 1)
    - What domain: TQ_N_* (18 items expected)
    - Where domain: TQ_U_*, TQ_D_* (16 items expected - pick-up and put-down)
    - When domain: TQ_O_* (16 items expected)
**Expected Rows:** ~400 (100 participants x 4 tests)
**Expected Columns:** ~50 TQ_ item columns + identifier columns
**Circuit Breaker:** If file missing -> EXPECTATIONS ERROR "dfData.csv required for CTT computation (raw item responses)"

**Processing:**
1. Load RQ 5.1 purified items list -> extract item_name column as retained_items
2. Load RQ 5.1 theta scores -> keep all columns
3. Load RQ 5.1 TSVR mapping -> keep all columns
4. Load raw data (dfData.csv) -> filter to TQ_ columns only
5. Validate all composite_IDs match across files (theta, TSVR, raw data)
6. Merge TSVR with theta on composite_ID (left join - all theta rows retained)

**Output:**

**File 1:** data/step00_retained_items.csv
**Format:** CSV, one row per retained item
**Columns:**
  - `item_name` (string, VR tag format)
  - `dimension` (string, factor assignment)
  - `a` (float, discrimination)
  - `b` (float, difficulty)
**Expected Rows:** ~38 items
**Purpose:** Identify which items to include in purified CTT computation

**File 2:** data/step00_raw_ctt_data.csv
**Format:** CSV, wide format (composite_ID x TQ_ items)
**Columns:**
  - `composite_ID` (string)
  - `UID` (string)
  - `test` (string)
  - TQ_ item columns (int 0/1/NaN, ~50 columns)
**Expected Rows:** ~400
**Purpose:** Raw item responses for CTT scoring

**File 3:** data/step00_theta_with_tsvr.csv
**Format:** CSV, one row per composite_ID
**Columns:**
  - `composite_ID` (string)
  - `UID` (string)
  - `test` (string)
  - `TSVR_hours` (float)
  - `theta_common`, `se_common` (float)
  - `theta_congruent`, `se_congruent` (float)
  - `theta_incongruent`, `se_incongruent` (float)
**Expected Rows:** ~400
**Purpose:** IRT theta scores with time variable for later LMM comparison

**Validation Requirement:**
Validation tools MUST be used after data loading execution. Specific validation tools determined by rq_tools based on cross-RQ dependency checks.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_retained_items.csv: ~38 rows x 4 columns (item_name, dimension, a, b)
- data/step00_raw_ctt_data.csv: ~400 rows x ~53 columns (composite_ID, UID, test, ~50 TQ_ items)
- data/step00_theta_with_tsvr.csv: ~400 rows x 10 columns (composite_ID, UID, test, TSVR_hours, 6 theta/SE columns)
- All data types correct (string for IDs, float for numeric)

*Value Ranges:*
- a in [0.5, 4.0] (post-purification range)
- b unrestricted (temporal items can have |b| > 3.0)
- TQ_ items in {0, 1, NaN} (dichotomized responses)
- theta_* in [-3, 3] typical (allow [-5, 5] for outliers)
- se_* in [0.1, 1.0] (standard error bounds)
- TSVR_hours in [0, 300] (0=encoding, ~168=1 week, 300=upper bound)

*Data Quality:*
- Retained items count: 35-42 items acceptable (expected ~38, ±10% tolerance)
- Raw CTT data: All 400 composite_IDs present (100 participants x 4 tests, no data loss)
- Theta-TSVR merge: All 400 rows matched (no missing TSVR values)
- No duplicate composite_IDs in any file
- TQ_ item columns: Allow up to 30% NaN per item (missing data acceptable)

*Log Validation:*
- Required: "Loaded {N} retained items from RQ 5.1" where N in [35, 42]
- Required: "All 400 composite_IDs matched across theta and TSVR files"
- Required: "Loaded {M} TQ_ items from dfData.csv" where M in [48, 52]
- Forbidden: "ERROR", "TSVR merge failed", "composite_ID mismatch"
- Acceptable warnings: "Some TQ_ items have >30% missing data" (temporal items difficult)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Expected 38 retained items, found 25 - RQ 5.1 purification may have failed")
- Log failure to logs/step00_load_data.log
- Quit immediately (do NOT proceed to Step 1)
- Master investigates: Check RQ 5.1 status.yaml, verify RQ 5.1 completed successfully

---

### Step 1: Map IRT Items to CTT Items

**Dependencies:** Step 0 (requires retained_items and raw_ctt_data)
**Complexity:** Low (~5 minutes item mapping)

**Purpose:** Create mapping between IRT item names (VR tag format) and CTT item names (TQ_ prefix format) to identify which CTT items correspond to IRT-retained items

**Input:**

**File 1:** data/step00_retained_items.csv (from Step 0)
**Columns:** item_name, dimension, a, b
**Expected Rows:** ~38 items

**File 2:** data/step00_raw_ctt_data.csv (from Step 0)
**Columns:** composite_ID, UID, test, TQ_ item columns (~50)
**Expected Rows:** ~400

**Processing:**
1. Parse IRT item_name format: VR-{paradigm}-{test}-{domain}-ANS
   - Example: VR-IFR-A01-N-ANS -> paradigm=IFR, test=A01, domain=N (What)
2. Construct corresponding CTT item name: TQ_{domain}_{variant}_{number}
   - Domain mapping: N->N (What), U->U (Where-pickup), D->D (Where-putdown), O->O (When)
   - Variant mapping: Derived from paradigm (IFR=F for Face, etc.)
   - Number: Sequential within domain-variant combination
3. For each IRT retained item, identify matching TQ_ column in raw_ctt_data
4. Create two lists:
   - full_ctt_items: All TQ_ columns from raw_ctt_data (~50 items)
   - purified_ctt_items: Only TQ_ columns matching IRT retained items (~38 items)
5. Verify all purified_ctt_items exist in raw_ctt_data (circuit breaker if missing)

**Output:**

**File 1:** data/step01_full_ctt_items.csv
**Format:** CSV, one row per CTT item
**Columns:**
  - `ctt_item_name` (string, format: TQ_{domain}_{variant}_{number})
  - `domain` (string, values: {What, Where, When})
**Expected Rows:** ~50 items
**Purpose:** Full CTT item list for Step 2 scoring

**File 2:** data/step01_purified_ctt_items.csv
**Format:** CSV, one row per purified CTT item
**Columns:**
  - `ctt_item_name` (string, TQ_ format)
  - `irt_item_name` (string, VR tag format)
  - `domain` (string)
  - `a` (float, from IRT)
  - `b` (float, from IRT)
**Expected Rows:** ~38 items
**Purpose:** Purified CTT item list for Step 3 scoring

**Validation Requirement:**
Validation tools MUST be used after item mapping execution. Specific validation tools determined by rq_tools based on data format validation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_full_ctt_items.csv: ~50 rows x 2 columns (ctt_item_name, domain)
- data/step01_purified_ctt_items.csv: ~38 rows x 5 columns (ctt_item_name, irt_item_name, domain, a, b)
- Data types: string (item names, domain), float (a, b)

*Value Ranges:*
- domain in {What, Where, When} (categorical)
- a in [0.5, 4.0] (purified items only)
- b unrestricted (temporal items can have extreme difficulty)
- Item counts match Step 0: purified_ctt_items ~= retained_items count

*Data Quality:*
- All purified_ctt_items found in raw_ctt_data columns (no missing TQ_ items)
- Domain distribution reasonable: What ~14, Where ~12, When ~12 (±3 items per domain)
- No duplicate ctt_item_names in either file
- All purified items have corresponding IRT parameters (a, b non-null)

*Log Validation:*
- Required: "Mapped {N} IRT items to {M} CTT items" where N ~= M ~= 38
- Required: "All purified CTT items found in raw data"
- Required: "Domain distribution - What: {W}, Where: {X}, When: {Y}"
- Forbidden: "ERROR", "Missing TQ_ item", "Mapping failed"
- Acceptable warnings: None expected for item mapping

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "IRT item VR-IFR-A01-N-ANS has no matching TQ_ item in raw data")
- Log failure to logs/step01_map_items.log
- Quit immediately (do NOT proceed to Step 2)
- Master investigates: Check data/cache/dfData.csv structure, verify TQ_ column naming

---

### Step 2: Compute Full CTT Scores

**Dependencies:** Step 1 (requires full_ctt_items and raw_ctt_data)
**Complexity:** Low (~3 minutes CTT computation)

**Purpose:** Calculate mean accuracy scores per participant x test x domain using ALL available items (traditional CTT approach with equal weighting)

**Input:**

**File 1:** data/step01_full_ctt_items.csv (from Step 1)
**Columns:** ctt_item_name, domain
**Expected Rows:** ~50 items

**File 2:** data/step00_raw_ctt_data.csv (from Step 0)
**Columns:** composite_ID, UID, test, TQ_ item columns (~50)
**Expected Rows:** ~400

**Processing:**
1. For each domain (What, Where, When):
   - Filter full_ctt_items to domain-specific items
   - Extract corresponding TQ_ columns from raw_ctt_data
   - Compute mean accuracy per composite_ID (row-wise mean, ignore NaN)
2. Reshape from wide (composite_ID x domain columns) to long (composite_ID-domain rows)
3. Add metadata columns: UID (from composite_ID split), test (from composite_ID split)

**Output:**

**File 1:** data/step02_full_ctt_scores.csv
**Format:** CSV, long format (one row per composite_ID x domain)
**Columns:**
  - `composite_ID` (string)
  - `UID` (string)
  - `test` (string)
  - `domain` (string, values: {What, Where, When})
  - `ctt_score_full` (float, range: [0, 1], mean accuracy)
  - `n_items_full` (int, number of items used in mean)
**Expected Rows:** ~1200 (400 composite_IDs x 3 domains)

**Validation Requirement:**
Validation tools MUST be used after CTT scoring execution. Specific validation tools determined by rq_tools based on CTT computation validation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_full_ctt_scores.csv: ~1200 rows x 6 columns (composite_ID, UID, test, domain, ctt_score_full, n_items_full)
- Data types: string (IDs, domain), float (ctt_score_full), int (n_items_full)

*Value Ranges:*
- ctt_score_full in [0, 1] (mean accuracy, cannot exceed bounds)
- n_items_full in [10, 20] per domain (What ~18, Where ~16, When ~16, allow some missing)
- Expected mean scores: ~0.50-0.70 (episodic memory tasks moderately difficult)

*Data Quality:*
- All 1200 rows present (400 composite_IDs x 3 domains, no data loss)
- No NaN in ctt_score_full (if all items NaN for a participant-domain, score should be 0 or excluded)
- No duplicate composite_ID-domain combinations
- Domain distribution balanced: Each composite_ID appears exactly 3 times (What, Where, When)
- n_items_full reasonable: What ~18, Where ~16, When ~16 (±5 items tolerance for missing data)

*Log Validation:*
- Required: "Computed full CTT scores for 1200 composite_ID-domain combinations"
- Required: "Mean items per domain - What: {W}, Where: {X}, When: {Y}"
- Required: "Mean CTT scores - What: {A}, Where: {B}, When: {C}" where all in [0.3, 0.9]
- Forbidden: "ERROR", "NaN in ctt_score_full", "Missing domain"
- Acceptable warnings: "Some participants have <50% items for domain {X}" (temporal items difficult)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Expected 1200 rows, found 873 - some domains missing")
- Log failure to logs/step02_compute_full_ctt.log
- Quit immediately (do NOT proceed to Step 3)
- Master investigates: Check raw_ctt_data for missing TQ_ columns, verify domain mapping

---

### Step 3: Compute Purified CTT Scores

**Dependencies:** Step 1 (requires purified_ctt_items and raw_ctt_data)
**Complexity:** Low (~3 minutes CTT computation)

**Purpose:** Calculate mean accuracy scores per participant x test x domain using ONLY IRT-retained items (hybrid CTT-IRT approach testing purification benefit)

**Input:**

**File 1:** data/step01_purified_ctt_items.csv (from Step 1)
**Columns:** ctt_item_name, irt_item_name, domain, a, b
**Expected Rows:** ~38 items

**File 2:** data/step00_raw_ctt_data.csv (from Step 0)
**Columns:** composite_ID, UID, test, TQ_ item columns
**Expected Rows:** ~400

**Processing:**
1. For each domain (What, Where, When):
   - Filter purified_ctt_items to domain-specific items
   - Extract corresponding TQ_ columns from raw_ctt_data
   - Compute mean accuracy per composite_ID (row-wise mean, ignore NaN)
2. Reshape from wide to long format
3. Add metadata columns: UID, test (from composite_ID)
4. Expected item counts after purification: What ~14, Where ~12, When ~12 (from concept.md)

**Output:**

**File 1:** data/step03_purified_ctt_scores.csv
**Format:** CSV, long format (one row per composite_ID x domain)
**Columns:**
  - `composite_ID` (string)
  - `UID` (string)
  - `test` (string)
  - `domain` (string, values: {What, Where, When})
  - `ctt_score_purified` (float, range: [0, 1], mean accuracy)
  - `n_items_purified` (int, number of items used in mean)
**Expected Rows:** ~1200 (400 composite_IDs x 3 domains)

**Validation Requirement:**
Validation tools MUST be used after purified CTT scoring execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_purified_ctt_scores.csv: ~1200 rows x 6 columns (composite_ID, UID, test, domain, ctt_score_purified, n_items_purified)
- Data types: string (IDs, domain), float (ctt_score_purified), int (n_items_purified)

*Value Ranges:*
- ctt_score_purified in [0, 1] (mean accuracy)
- n_items_purified in [8, 18] per domain (What ~14, Where ~12, When ~12 expected, fewer than full CTT)
- Expected mean scores: ~0.52-0.72 (slightly higher than full CTT if purification removes noise)

*Data Quality:*
- All 1200 rows present (400 composite_IDs x 3 domains)
- No NaN in ctt_score_purified
- No duplicate composite_ID-domain combinations
- n_items_purified < n_items_full (purification removes items, never adds)
- Expected item reduction: ~20-30% fewer items than full CTT per domain

*Log Validation:*
- Required: "Computed purified CTT scores for 1200 composite_ID-domain combinations"
- Required: "Mean items per domain (purified) - What: {W}, Where: {X}, When: {Y}"
- Required: "Item reduction vs full CTT - What: {A}%, Where: {B}%, When: {C}%" where all in [15%, 35%]
- Required: "Mean purified CTT scores - What: {D}, Where: {E}, When: {F}"
- Forbidden: "ERROR", "n_items_purified > n_items_full", "Missing domain"
- Acceptable warnings: "Purified item counts lower than expected (aggressive purification)"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Purified item count exceeds full item count for What domain")
- Log failure to logs/step03_compute_purified_ctt.log
- Quit immediately (do NOT proceed to Step 4)
- Master investigates: Check purified_ctt_items mapping, verify IRT purification criteria applied correctly

---

### Step 4: Assess CTT Reliability (Cronbach's Alpha)

**Dependencies:** Step 1, 2, 3 (requires item lists and raw data for internal consistency)
**Complexity:** Medium (~10 minutes with bootstrap CIs)

**Purpose:** Compute Cronbach's alpha for both full and purified CTT item sets per domain to assess whether IRT purification maintains or improves CTT reliability

**Input:**

**File 1:** data/step01_full_ctt_items.csv (from Step 1)
**Columns:** ctt_item_name, domain
**Expected Rows:** ~50 items

**File 2:** data/step01_purified_ctt_items.csv (from Step 1)
**Columns:** ctt_item_name, irt_item_name, domain, a, b
**Expected Rows:** ~38 items

**File 3:** data/step00_raw_ctt_data.csv (from Step 0)
**Columns:** composite_ID, UID, test, TQ_ item columns
**Expected Rows:** ~400

**Processing:**
1. For each domain (What, Where, When):
   - Extract full CTT items for domain from raw_ctt_data
   - Compute Cronbach's alpha using tools.analysis_ctt.compute_cronbachs_alpha()
   - Bootstrap 95% confidence intervals (1000 resamples)
   - Extract purified CTT items for domain from raw_ctt_data
   - Compute Cronbach's alpha with bootstrap 95% CIs
2. Compare alpha_full vs alpha_purified per domain
3. Interpretation logic:
   - If alpha_purified >= alpha_full (or CIs overlap): Purification maintains/improves reliability
   - If alpha_purified < alpha_full with non-overlapping CIs: Purification reduces reliability (requires discussion)

**Output:**

**File 1:** data/step04_ctt_reliability.csv
**Format:** CSV, one row per domain x item_set
**Columns:**
  - `domain` (string, values: {What, Where, When})
  - `item_set` (string, values: {full, purified})
  - `alpha` (float, range: [0, 1], Cronbach's alpha point estimate)
  - `ci_lower` (float, 95% CI lower bound)
  - `ci_upper` (float, 95% CI upper bound)
  - `n_items` (int, number of items in set)
**Expected Rows:** 6 (3 domains x 2 item_sets)

**Validation Requirement:**
Validation tools MUST be used after Cronbach's alpha computation execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_ctt_reliability.csv: 6 rows x 6 columns (domain, item_set, alpha, ci_lower, ci_upper, n_items)
- Data types: string (domain, item_set), float (alpha, CIs), int (n_items)

*Value Ranges:*
- alpha in [0.5, 0.95] (episodic memory scales typically 0.7-0.9)
- ci_lower < alpha < ci_upper (CIs must bracket point estimate)
- CI width: (ci_upper - ci_lower) in [0.02, 0.15] (bootstrap CIs typically narrow for N=400)
- n_items matches Step 1 counts: full ~18/16/16, purified ~14/12/12 per domain

*Data Quality:*
- All 6 rows present (3 domains x 2 item_sets)
- No NaN values (all alphas computable)
- ci_lower >= 0 and ci_upper <= 1 (valid alpha bounds)
- Expected pattern: alpha_purified >= alpha_full OR CIs overlap (purification shouldn't drastically reduce reliability)

*Log Validation:*
- Required: "Computed Cronbach's alpha for 6 domain-itemset combinations"
- Required: "Full CTT alpha - What: {A} [{B}, {C}]" (format: point estimate [CI_lower, CI_upper])
- Required: "Purified CTT alpha - What: {D} [{E}, {F}]"
- Required: "Alpha comparison - What: {increase/decrease/stable}" (based on CI overlap)
- Forbidden: "ERROR", "Alpha computation failed", "Bootstrap failed"
- Acceptable warnings: "Alpha slightly lower for purified set (within 95% CI)" if CIs overlap

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Cronbach's alpha = 1.2 for What domain - exceeds valid range")
- Log failure to logs/step04_assess_reliability.log
- Quit immediately (do NOT proceed to Step 5)
- Master investigates: Check raw_ctt_data for data quality issues, verify bootstrap function

---

### Step 5: Correlation Analysis with Steiger's Z-Test

**Dependencies:** Steps 0, 2, 3 (requires full CTT, purified CTT, and IRT theta scores)
**Complexity:** Medium (~8 minutes with dependent correlation tests)

**Purpose:** Test whether purified CTT correlates more strongly with IRT theta than full CTT, using Steiger's z-test for dependent correlations (correct method for overlapping samples)

**Input:**

**File 1:** data/step02_full_ctt_scores.csv (from Step 2)
**Columns:** composite_ID, UID, test, domain, ctt_score_full, n_items_full
**Expected Rows:** ~1200

**File 2:** data/step03_purified_ctt_scores.csv (from Step 3)
**Columns:** composite_ID, UID, test, domain, ctt_score_purified, n_items_purified
**Expected Rows:** ~1200

**File 3:** data/step00_theta_with_tsvr.csv (from Step 0)
**Columns:** composite_ID, UID, test, TSVR_hours, theta_common, se_common, theta_congruent, se_congruent, theta_incongruent, se_incongruent
**Expected Rows:** ~400

**Processing:**
1. Map IRT theta dimensions to domains:
   - What domain: Use theta_common (object identity - common factor)
   - Where domain: Use theta_congruent (spatial congruent locations)
   - When domain: Use theta_incongruent (temporal incongruent sequences)
   - Rationale: Domain-dimension mapping from RQ 5.1 3-factor model
2. Reshape IRT theta to long format: composite_ID-domain rows matching CTT scores
3. Merge full CTT, purified CTT, IRT theta on composite_ID-domain
4. For each domain:
   - Compute r(Full CTT, IRT)
   - Compute r(Purified CTT, IRT)
   - Compute r(Full CTT, Purified CTT)
   - Test H0: r(Full CTT, IRT) = r(Purified CTT, IRT) using Steiger's z-test
   - Use tools.analysis_ctt.compare_correlations_dependent() with all three correlations
   - Report z-statistic, p-value (two-tailed), and delta_r = r(Purified, IRT) - r(Full, IRT)
5. Expected pattern: r(Purified CTT, IRT) > r(Full CTT, IRT) with small delta_r ~0.02-0.05

**Output:**

**File 1:** data/step05_correlations.csv
**Format:** CSV, one row per domain x correlation_pair
**Columns:**
  - `domain` (string)
  - `correlation_pair` (string, values: {Full_CTT-IRT, Purified_CTT-IRT, Full_CTT-Purified_CTT})
  - `r` (float, range: [-1, 1], Pearson correlation)
  - `n` (int, sample size)
**Expected Rows:** 9 (3 domains x 3 correlation_pairs)

**File 2:** data/step05_steiger_tests.csv
**Format:** CSV, one row per domain
**Columns:**
  - `domain` (string)
  - `r_full_irt` (float)
  - `r_purified_irt` (float)
  - `delta_r` (float, = r_purified_irt - r_full_irt)
  - `z_statistic` (float, Steiger's z)
  - `p_value` (float, range: [0, 1], two-tailed)
  - `interpretation` (string, "Purified > Full" if p < 0.05 and delta_r > 0, else "No difference")
**Expected Rows:** 3 (one per domain)

**Validation Requirement:**
Validation tools MUST be used after correlation analysis execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_correlations.csv: 9 rows x 4 columns (domain, correlation_pair, r, n)
- data/step05_steiger_tests.csv: 3 rows x 7 columns (domain, r_full_irt, r_purified_irt, delta_r, z_statistic, p_value, interpretation)
- Data types: string (domain, correlation_pair, interpretation), float (r, delta_r, z, p), int (n)

*Value Ranges:*
- r in [-1, 1] (correlation bounds)
- Expected r(Full CTT, IRT) in [0.90, 0.98] (high convergence expected)
- Expected r(Purified CTT, IRT) in [0.92, 0.99] (higher than full CTT)
- Expected delta_r in [-0.05, 0.10] (small improvement, could be negative if purification removes signal)
- z_statistic unrestricted (Steiger's z can be any real number)
- p_value in [0, 1]
- n in [390, 410] per domain (allowing some missing data)

*Data Quality:*
- All 9 correlation rows present
- All 3 Steiger test rows present
- No NaN in correlations or p-values
- r(Full CTT, Purified CTT) in [0.85, 0.99] (two CTT approaches should be highly correlated)
- delta_r sign matches hypothesis (expect positive, but negative acceptable if purification harmful)

*Log Validation:*
- Required: "Computed 9 pairwise correlations (3 domains x 3 pairs)"
- Required: "Steiger's z-tests completed for 3 domains"
- Required: "Mean delta_r across domains: {X}" where X in [-0.05, 0.10]
- Required: "Significant differences (p < 0.05): {N} domains" where N in [0, 3]
- Forbidden: "ERROR", "Correlation computation failed", "Singular covariance matrix"
- Acceptable warnings: "delta_r negative for {domain} (purification may have removed signal)"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Correlation r = 1.3 exceeds valid range [-1, 1]")
- Log failure to logs/step05_correlation_analysis.log
- Quit immediately (do NOT proceed to Step 6)
- Master investigates: Check merged data quality, verify all three measures aligned on composite_ID-domain

---

### Step 6: Standardize Outcomes for AIC Comparison

**Dependencies:** Steps 0, 2, 3 (requires full CTT, purified CTT, IRT theta)
**Complexity:** Low (~3 minutes z-score transformation)

**Purpose:** Standardize all three measurement approaches (Full CTT, Purified CTT, IRT theta) to z-scores to enable valid AIC comparison across different outcome scales per Burnham & Anderson

**Input:**

**File 1:** data/step02_full_ctt_scores.csv (from Step 2)
**Expected Rows:** ~1200

**File 2:** data/step03_purified_ctt_scores.csv (from Step 3)
**Expected Rows:** ~1200

**File 3:** data/step00_theta_with_tsvr.csv (from Step 0)
**Expected Rows:** ~400 (needs reshaping to ~1200)

**Processing:**
1. Reshape IRT theta to long format (composite_ID-domain rows) matching CTT scores
2. Merge Full CTT, Purified CTT, IRT theta on composite_ID-domain
3. For each measurement approach (Full CTT, Purified CTT, IRT):
   - Compute z-score: z = (score - mean) / SD
   - Compute within entire sample (not within domain, to preserve domain differences)
4. Verify z-score properties: mean ~= 0, SD ~= 1
5. Merge with TSVR_hours for LMM time variable

**Output:**

**File 1:** data/step06_standardized_scores.csv
**Format:** CSV, long format (one row per composite_ID x domain)
**Columns:**
  - `composite_ID` (string)
  - `UID` (string)
  - `test` (string)
  - `domain` (string)
  - `TSVR_hours` (float)
  - `z_full_ctt` (float, z-score of full CTT)
  - `z_purified_ctt` (float, z-score of purified CTT)
  - `z_irt_theta` (float, z-score of IRT theta)
**Expected Rows:** ~1200 (400 composite_IDs x 3 domains)

**Validation Requirement:**
Validation tools MUST be used after z-score standardization execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_standardized_scores.csv: ~1200 rows x 8 columns (composite_ID, UID, test, domain, TSVR_hours, 3 z-scores)
- Data types: string (IDs, domain), float (TSVR_hours, z-scores)

*Value Ranges:*
- z_full_ctt, z_purified_ctt, z_irt_theta in [-4, 4] (allow up to 4 SD for outliers)
- TSVR_hours in [0, 300] (same as Step 0)
- Expected z-score means: ~0 (within ±0.05)
- Expected z-score SDs: ~1 (within [0.95, 1.05])

*Data Quality:*
- All 1200 rows present (no data loss during merge)
- No NaN in z-scores (all participants have scores for all three approaches)
- No duplicate composite_ID-domain combinations
- Z-score distributions approximately normal (Shapiro-Wilk p > 0.01 acceptable)
- All three z-scores have mean ~0 and SD ~1 (verify standardization worked)

*Log Validation:*
- Required: "Standardized 3 measurement approaches to z-scores"
- Required: "Z-score diagnostics - Full CTT: mean={A}, SD={B}" where A in [-0.05, 0.05], B in [0.95, 1.05]
- Required: "Z-score diagnostics - Purified CTT: mean={C}, SD={D}"
- Required: "Z-score diagnostics - IRT theta: mean={E}, SD={F}"
- Required: "All 1200 rows retained (no missing values in z-scores)"
- Forbidden: "ERROR", "NaN in z-scores", "SD = 0 (no variance)"
- Acceptable warnings: "Some z-scores exceed ±3 SD (outliers present)"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Z-score mean = 0.5, expected ~0 - standardization failed")
- Log failure to logs/step06_standardize_outcomes.log
- Quit immediately (do NOT proceed to Step 7)
- Master investigates: Check score distributions, verify z-score formula applied correctly

---

### Step 7: Fit Parallel LMMs to Standardized Outcomes

**Dependencies:** Step 6 (requires standardized scores)
**Complexity:** High (~30 minutes - 3 LMM models)

**Purpose:** Fit identical LMM models to all three standardized measurement approaches (Full CTT, Purified CTT, IRT theta) to test whether purified CTT conclusions match IRT more closely than full CTT

**Input:**

**File 1:** data/step06_standardized_scores.csv (from Step 6)
**Columns:** composite_ID, UID, test, domain, TSVR_hours, z_full_ctt, z_purified_ctt, z_irt_theta
**Expected Rows:** ~1200

**Processing:**
1. For each measurement approach (Full CTT, Purified CTT, IRT):
   - Fit LMM using tools.lmm.fit_lmm_trajectory_tsvr()
   - Formula: z_Ability ~ (TSVR_hours + log(TSVR_hours+1)) * domain + (TSVR_hours | UID)
   - TSVR_hours is time variable (Decision D070 - actual hours, not nominal days)
   - Domain is categorical factor (What, Where, When)
   - Random slope for TSVR_hours per participant (accounts for individual differences in forgetting rate)
2. Extract model summaries:
   - Fixed effects table: coefficients, SE, z-values, p-values
   - Random effects: variance components, ICC
   - Model fit: AIC, BIC, log-likelihood
3. Compare AICs across three models:
   - ”AIC_full = AIC_full_ctt - AIC_irt_theta
   - ”AIC_purified = AIC_purified_ctt - AIC_irt_theta
   - Hypothesis: ”AIC_purified < ”AIC_full (purified CTT closer to IRT)
   - Interpret per Burnham & Anderson: ”AIC < 2 = equivalent, 2-10 = moderate support, > 10 = substantial support
4. Compare Domain × Time interactions:
   - Extract coefficients for domain:Where × TSVR_hours and domain:When × TSVR_hours
   - Test if purified CTT interaction patterns match IRT more closely than full CTT

**Output:**

**File 1:** data/step07_lmm_full_ctt_summary.txt
**Format:** Plain text LMM summary
**Content:** Fixed effects, random effects, AIC, BIC
**Purpose:** Full CTT model results

**File 2:** data/step07_lmm_purified_ctt_summary.txt
**Format:** Plain text LMM summary
**Content:** Fixed effects, random effects, AIC, BIC
**Purpose:** Purified CTT model results

**File 3:** data/step07_lmm_irt_theta_summary.txt
**Format:** Plain text LMM summary
**Content:** Fixed effects, random effects, AIC, BIC
**Purpose:** IRT theta model results (gold standard)

**File 4:** data/step07_lmm_comparison.csv
**Format:** CSV, one row per measurement approach
**Columns:**
  - `measurement_approach` (string, values: {Full_CTT, Purified_CTT, IRT_theta})
  - `AIC` (float)
  - `BIC` (float)
  - `delta_AIC_vs_IRT` (float, = AIC - AIC_irt_theta)
  - `interpretation` (string, per Burnham & Anderson thresholds)
**Expected Rows:** 3

**File 5:** data/step07_interaction_coefficients.csv
**Format:** CSV, one row per measurement approach x interaction term
**Columns:**
  - `measurement_approach` (string)
  - `interaction_term` (string, values: {domain:Where × TSVR_hours, domain:When × TSVR_hours})
  - `coefficient` (float)
  - `SE` (float)
  - `p_value` (float)
**Expected Rows:** 6 (3 approaches x 2 interaction terms)

**Validation Requirement:**
Validation tools MUST be used after LMM fitting execution. Specific validation tools determined by rq_tools based on LMM validation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_lmm_full_ctt_summary.txt: Text file, 50-100 lines
- data/step07_lmm_purified_ctt_summary.txt: Text file, 50-100 lines
- data/step07_lmm_irt_theta_summary.txt: Text file, 50-100 lines
- data/step07_lmm_comparison.csv: 3 rows x 5 columns
- data/step07_interaction_coefficients.csv: 6 rows x 5 columns
- Data types: string (approach, term, interpretation), float (AIC, BIC, delta_AIC, coef, SE, p)

*Value Ranges:*
- AIC unrestricted but positive (typically 1000-5000 for N=1200)
- BIC unrestricted but positive (typically slightly larger than AIC)
- delta_AIC_vs_IRT in [-50, 50] (purified and full CTT should be within ±50 AIC units of IRT)
- Expected: delta_AIC_purified < delta_AIC_full (purified closer to IRT)
- coefficient unrestricted (interaction effects can be positive or negative)
- p_value in [0, 1]

*Data Quality:*
- All 3 LMM summaries converged (no convergence warnings in logs)
- All 3 model comparison rows present
- All 6 interaction coefficient rows present
- delta_AIC_vs_IRT for IRT_theta = 0 (by definition, IRT compared to itself)
- Expected pattern: |delta_AIC_purified| < |delta_AIC_full|

*Log Validation:*
- Required: "Fitted 3 LMM models successfully"
- Required: "Model convergence - Full CTT: {converged/failed}"
- Required: "Model convergence - Purified CTT: {converged/failed}"
- Required: "Model convergence - IRT theta: {converged/failed}"
- Required: "AIC comparison - Full CTT: {A}, Purified CTT: {B}, IRT: {C}"
- Required: "Delta AIC (Purified vs IRT): {D}, Delta AIC (Full vs IRT): {E}"
- Required: "Interpretation: Purified CTT {closer to/farther from} IRT than Full CTT"
- Forbidden: "ERROR", "Convergence failed", "Singular fit"
- Acceptable warnings: "Model fit warning: boundary (singular)" if random effects variance near zero

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "LMM convergence failed for Full CTT model")
- Log failure to logs/step07_fit_parallel_lmms.log
- Quit immediately (do NOT proceed to Step 8)
- Master investigates: Check standardized scores distribution, verify LMM formula, check for singular fits

---

### Step 8: Prepare Comparison Plot Data

**Dependencies:** Steps 2, 3, 6 (requires full CTT, purified CTT, IRT scores with TSVR)
**Complexity:** Low (~5 minutes data aggregation)

**Purpose:** Aggregate observed means and confidence intervals for all three measurement approaches (Full CTT, Purified CTT, IRT) to create plot source CSV for 3-way trajectory comparison visualization

**Plot Description:** Three-panel trajectory plot showing forgetting curves for What/Where/When domains, with all three measurement approaches overlaid per panel to visualize methodological convergence

**Required Data Sources:**
- data/step02_full_ctt_scores.csv (Full CTT scores)
- data/step03_purified_ctt_scores.csv (Purified CTT scores)
- data/step06_standardized_scores.csv (IRT theta scores + TSVR mapping)

**Aggregation Logic:**
1. For each domain (What, Where, When) and measurement approach (Full CTT, Purified CTT, IRT):
   - Group by test (T1, T2, T3, T4)
   - Compute mean score, 95% CI (± 1.96 * SE)
   - Map test to TSVR_hours: T1->~0, T2->~24, T3->~72, T4->~144 (approximate means)
2. Combine all three approaches into single plot source CSV
3. Add approach identifier column for plotting (color/linetype grouping)

**Output (Plot Source CSV):** plots/step08_comparison_plot_data.csv

**Required Columns:**
- `domain` (string, values: {What, Where, When})
- `measurement_approach` (string, values: {Full_CTT, Purified_CTT, IRT_theta})
- `test` (string, values: {T1, T2, T3, T4})
- `time` (float, TSVR_hours mean per test)
- `mean_score` (float, mean across participants)
- `CI_lower` (float, 95% CI lower bound)
- `CI_upper` (float, 95% CI upper bound)
- `n` (int, number of participants)

**Expected Rows:** 36 (3 domains x 3 approaches x 4 tests)

**Validation Requirement:**
Validation tools MUST be used after plot data preparation execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- plots/step08_comparison_plot_data.csv: 36 rows x 8 columns (domain, measurement_approach, test, time, mean_score, CI_lower, CI_upper, n)
- Data types: string (domain, approach, test), float (time, mean_score, CIs), int (n)

*Value Ranges:*
- time in [0, 168] hours (0=encoding, ~168=1 week)
- mean_score: Full/Purified CTT in [0, 1], IRT theta in [-3, 3] (different scales OK - plot will handle)
- CI_lower < mean_score < CI_upper (CIs must bracket mean)
- n in [90, 100] per test (allowing some missing data)

*Data Quality:*
- All 36 rows present (3 domains x 3 approaches x 4 tests)
- No NaN in mean_score or CIs
- No duplicate domain-approach-test combinations
- Expected pattern: mean_score decreases across time (forgetting trajectory)
- CI width reasonable: (CI_upper - CI_lower) in [0.02, 0.30] depending on N and variance

*Log Validation:*
- Required: "Prepared plot data for 36 domain-approach-test combinations"
- Required: "All 3 measurement approaches represented per domain"
- Required: "Time range: [0, {max}] hours" where max in [140, 170]
- Required: "Mean participant count per test: {N}" where N in [95, 100]
- Forbidden: "ERROR", "NaN in plot data", "Missing approach"
- Acceptable warnings: None expected for plot data preparation

**Plotting Function (rq_plots will call):** Three-panel trajectory plot with confidence bands, grouped by measurement approach

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Expected 36 rows, found 30 - some domain-approach combinations missing")
- Log failure to logs/step08_prepare_plot_data.log
- Quit immediately (plot source CSV incomplete)
- Master investigates: Check input files (Steps 2, 3, 6), verify all domains and approaches present

---

## Expected Data Formats

### Wide to Long Transformations

**CTT Scores (Steps 2-3):**
- Input: Wide format (composite_ID x domain columns)
- Output: Long format (composite_ID-domain rows)
- Transformation: Reshape with composite_ID as key, domain as identifier variable

**IRT Theta (Step 6):**
- Input: Wide format (composite_ID with theta_common, theta_congruent, theta_incongruent columns)
- Output: Long format (composite_ID-domain rows with single theta column)
- Transformation: Map dimensions to domains, reshape to long

### Column Naming Conventions

Per names.md conventions established in RQ 5.1:

**Identifier Columns:**
- `composite_ID`: Primary key (UID_test format)
- `UID`: Participant identifier
- `test`: Test session (T1, T2, T3, T4)

**Time Variable:**
- `TSVR_hours`: Time Since VR in hours (Decision D070 - actual time, not nominal days)

**Score Columns:**
- `ctt_score_full`: Full CTT mean accuracy per domain
- `ctt_score_purified`: Purified CTT mean accuracy per domain
- `theta_*`: IRT ability estimates (dimension-specific)
- `z_full_ctt`, `z_purified_ctt`, `z_irt_theta`: Standardized z-scores

**Reliability Columns:**
- `alpha`: Cronbach's alpha point estimate
- `ci_lower`, `ci_upper`: 95% confidence interval bounds

**Correlation Columns:**
- `r`: Pearson correlation coefficient
- `z_statistic`: Steiger's z-test statistic
- `p_value`: Two-tailed significance

### Data Type Constraints

**Categorical Variables:**
- `domain`: Must be {What, Where, When} (no other values)
- `test`: Must be {T1, T2, T3, T4}
- `measurement_approach`: Must be {Full_CTT, Purified_CTT, IRT_theta}
- `item_set`: Must be {full, purified}

**Continuous Variables:**
- CTT scores: Non-nullable, range [0, 1]
- IRT theta: Non-nullable, range [-3, 3] typical (allow [-5, 5] for outliers)
- Z-scores: Non-nullable, range [-4, 4] (±4 SD maximum)
- Correlations: Non-nullable, range [-1, 1]
- P-values: Non-nullable, range [0, 1]
- TSVR_hours: Non-nullable, range [0, 300]

**Count Variables:**
- `n_items_full`, `n_items_purified`: Positive integers
- `n` (sample size): Positive integers, typically 90-100 per test

---

## Cross-RQ Dependencies

### Dependency Type 2: DERIVED Data from Other RQs

**This RQ requires outputs from:**
- **RQ 5.1** (Domain-Specific Forgetting Trajectories - IRT baseline)
  - Files required:
    - results/ch5/rq1/data/step02_purified_items.csv (IRT item parameters post-purification)
    - results/ch5/rq1/data/step03_theta_scores.csv (IRT theta ability estimates)
    - results/ch5/rq1/data/step00_tsvr_mapping.csv (Time Since VR mapping)
  - Used in: Step 0 (load IRT outputs for comparison)
  - Rationale: RQ 5.1 establishes IRT measurement baseline (item purification criteria, theta estimates). This RQ tests whether CTT can benefit from IRT item selection.

**Execution Order Constraint:**
1. RQ 5.1 must complete Steps 0-3 (IRT calibration, purification, theta extraction)
2. This RQ (5.12) executes after RQ 5.1 completes

**Data Source Boundaries (Per Best Practices):**
- **RAW data:** dfData.csv columns extracted directly for CTT computation (TQ_ items)
- **DERIVED data:** RQ 5.1 outputs (IRT item parameters, theta scores, TSVR mapping)
- **Scope:** This RQ does NOT re-run IRT calibration (uses RQ 5.1 purification criteria and theta scores as fixed)

**Validation:**
- Step 0: Check results/ch5/rq1/data/step02_purified_items.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch5/rq1/data/step03_theta_scores.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch5/rq1/data/step00_tsvr_mapping.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- If any file missing -> quit with error -> user must execute RQ 5.1 first

**No other RQ dependencies** - Only RQ 5.1 required.

---

## Validation Requirements

**CRITICAL MANDATE:**

Every analysis step in this plan MUST use validation tools after analysis tool execution.

This is not optional. This is the core architectural principle preventing cascading failures observed in v3.0 (where analysis errors propagated undetected through 5+ downstream steps before discovery).

**Exact Specification Requirement:**

> "Validation tools MUST be used after analysis tool execution"

**Implementation:**
- rq_tools (Step 11 workflow) will read tools_catalog.md validation tools section
- rq_tools will specify BOTH analysis tool + validation tool per step in 3_tools.yaml
- rq_analysis (Step 12 workflow) will embed validation tool call AFTER analysis tool call in 4_analysis.yaml
- g_code (Step 14 workflow) will generate stepNN_*.py scripts with validation function calls
- bash execution (Step 14 workflow) will run analysis -> validation -> error on validation failure

**Downstream Agent Requirements:**
- **rq_tools:** MUST specify validation tool for EVERY analysis step (no exceptions)
- **rq_analysis:** MUST embed validation tool call for EVERY analysis step (no exceptions)
- **g_code:** MUST generate code with validation function calls (no exceptions)
- **rq_inspect:** MUST verify validation ran successfully (checks logs/stepNN_*.log for validation output)

### Validation Requirements By Step

#### Step 0: Load Data from Multiple Sources

**Analysis Tool:** (determined by rq_tools - likely pandas read_csv + merge operations)
**Validation Tool:** (determined by rq_tools - likely custom cross-RQ dependency validation)

**What Validation Checks:**
- All RQ 5.1 dependency files exist (purified_items, theta_scores, tsvr_mapping)
- File row counts match expected (purified_items ~38, theta_scores ~400, tsvr_mapping ~400)
- dfData.csv contains expected TQ_ columns (~50 items)
- All composite_IDs matched across theta and TSVR files (no missing merges)
- Item counts reasonable: retained items 35-42, full CTT items 48-52

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "RQ 5.1 dependency missing: step02_purified_items.csv not found")
- Log failure to logs/step00_load_data.log
- Quit immediately (do NOT proceed to Step 1)
- Master investigates: Verify RQ 5.1 status.yaml shows rq_inspect: success

---

#### Step 1: Map IRT Items to CTT Items

**Analysis Tool:** (determined by rq_tools - likely pandas string parsing + filtering)
**Validation Tool:** (determined by rq_tools - likely custom item mapping validation)

**What Validation Checks:**
- All purified IRT items successfully mapped to TQ_ columns
- Full CTT item count ~50, purified CTT item count ~38
- No duplicate item names in either list
- Domain distribution reasonable (What ~14-18, Where ~12-16, When ~12-16)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "IRT item VR-IFR-A01-N-ANS has no matching TQ_ column")
- Log failure to logs/step01_map_items.log
- Quit immediately (do NOT proceed to Step 2)

---

#### Step 2: Compute Full CTT Scores

**Analysis Tool:** (determined by rq_tools - likely pandas groupby + mean)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_ctt_scores or custom)

**What Validation Checks:**
- Output row count = 1200 (400 composite_IDs x 3 domains)
- ctt_score_full in [0, 1] (mean accuracy bounds)
- n_items_full reasonable per domain (What ~18, Where ~16, When ~16)
- No NaN in ctt_score_full
- Domain balance: Each composite_ID appears exactly 3 times

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Expected 1200 rows, found 950 - some domains missing")
- Log failure to logs/step02_compute_full_ctt.log
- Quit immediately

---

#### Step 3: Compute Purified CTT Scores

**Analysis Tool:** (determined by rq_tools - likely pandas groupby + mean)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_ctt_scores or custom)

**What Validation Checks:**
- Output row count = 1200
- ctt_score_purified in [0, 1]
- n_items_purified < n_items_full (purification removes items)
- n_items_purified reasonable per domain (What ~14, Where ~12, When ~12)
- Item reduction 15-35% per domain

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Purified item count exceeds full item count for When domain")
- Log failure to logs/step03_compute_purified_ctt.log
- Quit immediately

---

#### Step 4: Assess CTT Reliability

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_ctt.compute_cronbachs_alpha)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_reliability_coefficients or custom)

**What Validation Checks:**
- Output row count = 6 (3 domains x 2 item_sets)
- alpha in [0.5, 0.95] (reasonable reliability range)
- ci_lower < alpha < ci_upper (CIs bracket estimate)
- CI width reasonable: [0.02, 0.15]
- n_items matches Step 1 counts

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Cronbach's alpha = 1.2 exceeds valid range [0, 1]")
- Log failure to logs/step04_assess_reliability.log
- Quit immediately

---

#### Step 5: Correlation Analysis with Steiger's Z-Test

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_ctt.compare_correlations_dependent)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_hypothesis_tests)

**What Validation Checks:**
- Correlations output: 9 rows (3 domains x 3 pairs)
- Steiger tests output: 3 rows (one per domain)
- r in [-1, 1]
- p_value in [0, 1]
- Expected high correlations: r(CTT, IRT) in [0.90, 0.98]
- delta_r in [-0.05, 0.10]

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Correlation r = 1.5 exceeds valid range")
- Log failure to logs/step05_correlation_analysis.log
- Quit immediately

---

#### Step 6: Standardize Outcomes for AIC Comparison

**Analysis Tool:** (determined by rq_tools - likely pandas z-score transformation)
**Validation Tool:** (determined by rq_tools - likely custom z-score validation)

**What Validation Checks:**
- Output row count = 1200
- z-score means ~= 0 (within ±0.05)
- z-score SDs ~= 1 (within [0.95, 1.05])
- z-scores in [-4, 4] (allow outliers up to ±4 SD)
- No NaN in z-scores

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Z-score mean = 0.5, expected ~0")
- Log failure to logs/step06_standardize_outcomes.log
- Quit immediately

---

#### Step 7: Fit Parallel LMMs to Standardized Outcomes

**Analysis Tool:** (determined by rq_tools - likely tools.lmm.fit_lmm_trajectory_tsvr)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_lmm_convergence + validate_lmm_assumptions_comprehensive)

**What Validation Checks:**
- All 3 LMM models converged (no singular fits)
- AIC, BIC positive (typical 1000-5000 for N=1200)
- delta_AIC_vs_IRT for IRT model = 0 (by definition)
- Expected: |delta_AIC_purified| < |delta_AIC_full|
- Interaction coefficients have valid SE and p-values

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "LMM convergence failed for Full CTT model")
- Log failure to logs/step07_fit_parallel_lmms.log
- Quit immediately

---

#### Step 8: Prepare Comparison Plot Data

**Analysis Tool:** (determined by rq_tools - likely pandas groupby + agg)
**Validation Tool:** (determined by rq_tools - likely custom plot data validation)

**What Validation Checks:**
- Output row count = 36 (3 domains x 3 approaches x 4 tests)
- time in [0, 168] hours
- CI_lower < mean_score < CI_upper
- n in [90, 100] per test
- All domain-approach-test combinations present

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Expected 36 rows, found 30")
- Log failure to logs/step08_prepare_plot_data.log
- Quit immediately

---

## Summary

**Total Steps:** 9 (Step 0: data loading, Steps 1-8: analyses)
**Estimated Runtime:** Medium (~60 minutes total)
  - Step 0: ~2 min (data loading)
  - Step 1: ~5 min (item mapping)
  - Step 2: ~3 min (full CTT scoring)
  - Step 3: ~3 min (purified CTT scoring)
  - Step 4: ~10 min (Cronbach's alpha with bootstrap)
  - Step 5: ~8 min (correlation analysis + Steiger's z-test)
  - Step 6: ~3 min (z-score standardization)
  - Step 7: ~30 min (3 parallel LMM models)
  - Step 8: ~5 min (plot data preparation)

**Cross-RQ Dependencies:** RQ 5.1 (requires Steps 0-3 completion)

**Primary Outputs:**
- CTT reliability assessment (Cronbach's alpha, 95% CIs)
- Correlation analysis (Full CTT vs Purified CTT vs IRT, Steiger's z-tests)
- AIC comparison (Full CTT vs Purified CTT vs IRT on standardized outcomes)
- Domain × Time interaction comparison (do purified CTT conclusions match IRT?)
- Three-way comparison plot source CSV (Full/Purified/IRT trajectories)

**Validation Coverage:** 100% (all 9 steps have validation requirements with 4-layer substance criteria)

**Key Hypotheses Tested:**
1. Purified CTT shows higher correlation with IRT theta than full CTT (Steiger's z-test)
2. Purified CTT yields better model fit (lower AIC) than full CTT
3. Purified CTT trajectory conclusions (Domain × Time interactions) match IRT more closely than full CTT
4. Purified CTT maintains or improves Cronbach's alpha vs full CTT (reliability validation)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate in workflow)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_*.py scripts

---

**Version History:**
- v1.0 (2025-11-26): Initial plan created by rq_planner agent for RQ 5.12
