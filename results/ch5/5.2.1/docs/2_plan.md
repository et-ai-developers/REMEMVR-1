# Analysis Plan for RQ 5.1: Domain-Specific Forgetting Trajectories (What/Where/When)

**Created by:** rq_planner agent
**Date:** 2025-11-22
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This plan specifies the complete analysis workflow for RQ 5.1, which examines domain-specific forgetting trajectories for three episodic memory components (What, Where, When) using IRT-derived theta ability estimates across four test sessions. The analysis uses 2-pass IRT purification (Decision D039) to obtain reliable ability estimates, followed by Linear Mixed Models with TSVR time variable (Decision D070) to model forgetting trajectories with Domain x Time interactions.

**Pipeline:** IRT (2-pass GRM purification) -> LMM (5 candidate trajectory models with model selection)

**Total Steps:** 8 steps (Step 0: data extraction + Steps 1-7: analysis and plot preparation)

**Estimated Runtime:** High (IRT calibration ~60 min per pass, LMM fitting ~5-10 min per model)

**Key Decisions Applied:**
- Decision D039: 2-pass IRT purification (|b| <= 3.0, a >= 0.4 thresholds)
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni) for post-hoc contrasts
- Decision D069: Dual-scale trajectory plots (theta + probability)
- Decision D070: TSVR (actual hours) as LMM time variable, not nominal days

---

## Analysis Plan

### Step 0: Extract VR Data for IRT Analysis

**Dependencies:** None (first step)
**Complexity:** Low (data extraction and dichotomization only, ~2 min)

**Input:**

**File:** data/cache/dfData.csv (project-level data source derived from master.xlsx)

**Required Columns:**
- `UID` (string): Participant unique identifier
- `TEST` (int): Test session (T1=0, T2=1, T3=3, T4=6)
- `TSVR` (float): Time Since VR in hours (actual elapsed time)
- `TQ_*` columns (float): All VR test question responses

**Domain Tag Patterns:**
- What: `*-N-*` in TQ_* column names (object identity)
- Where: `*-L-*`, `*-U-*`, `*-D-*` in TQ_* column names (spatial location)
- When: `*-O-*` in TQ_* column names (temporal order)

**Processing:**

1. Load data/cache/dfData.csv
2. Keep columns: UID, TEST, TSVR, and all TQ_* columns
3. Create composite_ID = UID + "_" + TEST (format: UID_test, e.g., "P001_0")
4. Dichotomize TQ_* values: values < 1 become 0, values >= 1 become 1
5. Assign items to domains based on tag patterns:
   - what_items = columns matching `*-N-*`
   - where_items = columns matching `*-L-*`, `*-U-*`, or `*-D-*`
   - when_items = columns matching `*-O-*`
6. Reshape to wide format: rows = composite_ID, columns = item tags
7. Create Q-matrix for multidimensional IRT (3 factors: what, where, when)
8. Save extraction outputs

**Output:**

**File 1:** data/step00_irt_input.csv
**Format:** CSV, wide format (one row per composite_ID)
**Columns:**
- `composite_ID` (string, format: UID_test)
- One column per item tag (values: 0, 1, or NaN for missing)
**Expected Rows:** ~400 (100 participants x 4 tests)
**Expected Columns:** ~100-200 item columns + 1 composite_ID column (exact count depends on TQ_* tag coverage)

**File 2:** data/step00_tsvr_mapping.csv
**Format:** CSV (one row per composite_ID)
**Columns:**
- `composite_ID` (string)
- `UID` (string)
- `test` (int: 0, 1, 3, 6)
- `TSVR_hours` (float: actual hours since encoding)
**Expected Rows:** ~400

**File 3:** data/step00_q_matrix.csv
**Format:** CSV (one row per item)
**Columns:**
- `item_name` (string: item tag)
- `what` (int: 1 if item loads on what, 0 otherwise)
- `where` (int: 1 if item loads on where, 0 otherwise)
- `when` (int: 1 if item loads on when, 0 otherwise)
**Expected Rows:** Same as number of items in step00_irt_input.csv

**Validation Requirement:**
Validation tools MUST be used after data extraction tool execution. Specific validation tools will be determined by rq_tools based on data extraction requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_irt_input.csv exists: ~400 rows x 100-200 columns (composite_ID + items)
- data/step00_tsvr_mapping.csv exists: ~400 rows x 4 columns
- data/step00_q_matrix.csv exists: ~100-200 rows x 4 columns

*Value Ranges:*
- Item values in {0, 1, NaN} only (binary after dichotomization)
- TSVR_hours in [0, 200] (reasonable range: 0 = encoding, ~168 = 1 week)
- test in {0, 1, 3, 6} (nominal test sessions)
- Q-matrix values in {0, 1} only

*Data Quality:*
- All 100 UIDs present (no participant loss during extraction)
- No unexpected NaN patterns (>80% NaN per item suggests extraction error)
- composite_ID format correct (UID_test pattern, e.g., "P001_0")
- Q-matrix: Each item loads on exactly 1 domain (row sum = 1)

*Log Validation:*
- Required pattern: "Extracted X items (what: W, where: S, when: T)"
- Required pattern: "Dichotomized values: 0/1 only"
- Forbidden patterns: "ERROR", "No items found", "Empty DataFrame"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step00_extract_vr_data.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause

---

### Step 1: IRT Calibration Pass 1 (All Items)

**Dependencies:** Step 0 (requires step00_irt_input.csv and step00_q_matrix.csv)
**Complexity:** High (IRT model calibration, ~30-60 min depending on convergence)

**Input:**

**File 1:** data/step00_irt_input.csv
**Format:** CSV, wide format (composite_ID x item columns)
**Columns:** composite_ID + item response columns (0/1/NaN)
**Expected Rows:** ~400

**File 2:** data/step00_q_matrix.csv
**Format:** CSV (item x dimension loading matrix)
**Columns:** item_name, what, where, when
**Expected Rows:** ~100-200 items

**Processing:**

1. Load IRT input data and Q-matrix
2. Configure 3-dimensional IRT model (GRM - Graded Response Model):
   - 3 correlated factors: what, where, when
   - Q-matrix specifies factor loadings (each item loads on one factor)
   - 2 response categories (0/1) -> 1 threshold parameter per item
3. Fit model using variational inference (IWAVE algorithm)
4. Extract Pass 1 item parameters (discrimination a, difficulty b)
5. Extract Pass 1 theta estimates (diagnostic only)
6. Save Pass 1 outputs to logs/ (not final outputs)

**Output:**

**File 1:** logs/step01_pass1_item_params.csv
**Format:** CSV (one row per item)
**Columns:**
- `item_name` (string): Item tag identifier
- `dimension` (string): Factor (what/where/when)
- `a` (float): Discrimination parameter (slope)
- `b` (float): Difficulty parameter (location) - single threshold for 2-category
**Expected Rows:** ~100-200 items

**File 2:** logs/step01_pass1_theta.csv
**Format:** CSV (one row per composite_ID)
**Columns:**
- `composite_ID` (string)
- `theta_what` (float): Ability estimate for what domain
- `theta_where` (float): Ability estimate for where domain
- `theta_when` (float): Ability estimate for when domain
- `se_what`, `se_where`, `se_when` (float): Standard errors
**Expected Rows:** ~400

**File 3:** logs/step01_pass1_convergence.txt
**Format:** Text file with convergence diagnostics
**Content:** Final loss, loss history, convergence status

**Validation Requirement:**
Validation tools MUST be used after IRT calibration tool execution. Specific validation tools will be determined by rq_tools based on IRT convergence and parameter validity requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- logs/step01_pass1_item_params.csv: ~100-200 rows x 4 columns
- logs/step01_pass1_theta.csv: ~400 rows x 7 columns
- logs/step01_pass1_convergence.txt: exists with content

*Value Ranges:*
- a (discrimination) in [0.01, 10.0] (negative impossible, >10 suspicious)
- b (difficulty) in [-6.0, 6.0] (extreme but possible for temporal items)
- theta in [-4.0, 4.0] (typical IRT ability range)
- se in [0.1, 2.0] (below 0.1 suspicious, above 2.0 unreliable)

*Data Quality:*
- No NaN in item parameters (all items must estimate)
- All composite_IDs present in theta output (no participant loss)
- Dimension column values in {what, where, when} only

*Log Validation:*
- Required pattern: "Model converged" or "Convergence achieved"
- Required pattern: "Final loss:" followed by numeric value
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "NaN loss"
- Acceptable warnings: "Some items near boundary" (expected for difficult temporal items)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step01_irt_calibration_pass1.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose (common causes: insufficient data, model misspecification)

---

### Step 2: Purify Items (Decision D039)

**Dependencies:** Step 1 (requires logs/step01_pass1_item_params.csv)
**Complexity:** Low (filtering based on thresholds, ~1 min)

**Input:**

**File:** logs/step01_pass1_item_params.csv
**Format:** CSV with columns: item_name, dimension, a, b
**Expected Rows:** ~100-200 items

**Processing:**

1. Load Pass 1 item parameters
2. Apply Decision D039 purification thresholds:
   - Retain if: |b| <= 3.0 (difficulty not extreme)
   - Retain if: a >= 0.4 (adequate discrimination)
   - Item retained only if BOTH conditions met
3. Perform WITHIN-DOMAIN filtering:
   - Apply thresholds separately for what, where, when items
   - Ensure at least 10 items retained per domain (circuit breaker if violated)
4. Generate purification report listing excluded items with reasons
5. Save purified item list

**Output:**

**File 1:** data/step02_purified_items.csv
**Format:** CSV (one row per retained item)
**Columns:**
- `item_name` (string): Item tag identifier
- `dimension` (string): Factor (what/where/when)
- `a` (float): Discrimination parameter
- `b` (float): Difficulty parameter
**Expected Rows:** 40-80% of original items (purification typically removes 20-60%)

**File 2:** logs/step02_purification_report.txt
**Format:** Text report
**Content:**
- Total items before: N
- Items excluded for |b| > 3.0: list
- Items excluded for a < 0.4: list
- Items retained per domain: what=W, where=S, when=T
- Total retained: M (P% retention)

**Validation Requirement:**
Validation tools MUST be used after item purification tool execution. Specific validation tools will be determined by rq_tools based on purification thresholds and domain coverage requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_purified_items.csv: 40-160 rows x 4 columns (expect 40-80% retention)
- logs/step02_purification_report.txt: exists with content

*Value Ranges:*
- All retained items have |b| <= 3.0 (strict threshold)
- All retained items have a >= 0.4 (strict threshold)
- Dimension values in {what, where, when} only

*Data Quality:*
- At least 10 items retained per domain (CRITICAL - circuit breaker if violated)
- No duplicate item_names
- Retention rate between 20% and 95% (too low = model problem, too high = threshold too lenient)

*Log Validation:*
- Required pattern: "Items retained per domain: what=W, where=S, when=T" (all >= 10)
- Required pattern: "Purification complete: M of N items retained"
- Forbidden patterns: "ERROR", "No items retained", "Domain eliminated"

**Expected Behavior on Validation Failure:**
- If any domain has < 10 items: CRITICAL ERROR (analysis cannot proceed)
- Log failure to logs/step02_purify_items.log
- Quit script immediately (do NOT proceed to Step 3)
- g_debug invoked to diagnose (likely D039 thresholds too strict for this data)

---

### Step 3: IRT Calibration Pass 2 (Purified Items)

**Dependencies:** Step 2 (requires data/step02_purified_items.csv), Step 0 (requires step00_irt_input.csv)
**Complexity:** High (IRT model calibration, ~30-60 min)

**Input:**

**File 1:** data/step00_irt_input.csv
**Format:** CSV, wide format (composite_ID x item columns)
**Columns:** composite_ID + all item response columns

**File 2:** data/step02_purified_items.csv
**Format:** CSV (retained items after purification)
**Columns:** item_name, dimension, a, b

**Processing:**

1. Load IRT input data
2. Load purified item list
3. Filter IRT input to include ONLY purified items (drop excluded columns)
4. Reconstruct Q-matrix from purified item list
5. Configure 3-dimensional IRT model (same as Pass 1)
6. Fit model using variational inference
7. Extract FINAL item parameters (a, b)
8. Extract FINAL theta estimates (ability scores for LMM)
9. Save to data/ folder (final outputs, not logs/)

**Output:**

**File 1:** data/step03_item_parameters.csv
**Format:** CSV (one row per purified item)
**Columns:**
- `item_name` (string): Item tag identifier
- `dimension` (string): Factor (what/where/when)
- `a` (float): Final discrimination parameter
- `b` (float): Final difficulty parameter
**Expected Rows:** Same as step02_purified_items.csv

**File 2:** data/step03_theta_scores.csv
**Format:** CSV (one row per composite_ID)
**Columns:**
- `composite_ID` (string)
- `theta_what` (float): Final ability estimate for what domain
- `theta_where` (float): Final ability estimate for where domain
- `theta_when` (float): Final ability estimate for when domain
- `se_what`, `se_where`, `se_when` (float): Standard errors
**Expected Rows:** ~400

**File 3:** logs/step03_pass2_convergence.txt
**Format:** Text file with convergence diagnostics

**Validation Requirement:**
Validation tools MUST be used after IRT calibration tool execution. Specific validation tools will be determined by rq_tools based on IRT convergence, parameter validity, and theta reliability requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_item_parameters.csv: Same row count as step02_purified_items.csv x 4 columns
- data/step03_theta_scores.csv: ~400 rows x 7 columns
- logs/step03_pass2_convergence.txt: exists with content

*Value Ranges:*
- a (discrimination) in [0.4, 10.0] (0.4 is minimum from purification)
- b (difficulty) in [-3.0, 3.0] (bounded by purification)
- theta in [-3.0, 3.0] (typical ability range, tighter than Pass 1)
- se in [0.1, 1.5] (should improve vs Pass 1 with purified items)

*Data Quality:*
- No NaN in item parameters
- All composite_IDs present in theta output (no participant loss)
- Theta SE values should be LOWER on average than Pass 1 (purification improves precision)
- Dimension column values in {what, where, when} only

*Log Validation:*
- Required pattern: "Model converged" or "Convergence achieved"
- Required pattern: "Using N purified items"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "NaN loss"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step03_irt_calibration_pass2.log
- Quit script immediately (do NOT proceed to Step 4)
- g_debug invoked to diagnose

---

### Step 4: Merge Theta Scores with TSVR (Decision D070)

**Dependencies:** Step 3 (requires data/step03_theta_scores.csv), Step 0 (requires data/step00_tsvr_mapping.csv)
**Complexity:** Low (data merge and reshape, ~1 min)

**Input:**

**File 1:** data/step03_theta_scores.csv
**Format:** CSV (wide format, one row per composite_ID)
**Columns:** composite_ID, theta_what, theta_where, theta_when, se_what, se_where, se_when

**File 2:** data/step00_tsvr_mapping.csv
**Format:** CSV (one row per composite_ID)
**Columns:** composite_ID, UID, test, TSVR_hours

**Processing:**

1. Load theta scores (wide format: 3 theta columns for 3 domains)
2. Load TSVR mapping
3. Merge on composite_ID (inner join - both must have data)
4. Reshape wide to long format:
   - Melt theta columns (theta_what, theta_where, theta_when) into single theta column
   - Create domain column (what, where, when)
   - Similarly melt SE columns
5. Result: One row per composite_ID x domain combination
6. Save LMM input with TSVR_hours as time variable (Decision D070)

**Output:**

**File:** data/step04_lmm_input.csv
**Format:** CSV, long format (one row per observation = composite_ID x domain)
**Columns:**
- `composite_ID` (string)
- `UID` (string): Participant identifier
- `test` (int): Nominal test session (0, 1, 3, 6)
- `TSVR_hours` (float): Actual time since encoding in hours (Decision D070)
- `domain` (string): Memory domain (what, where, when)
- `theta` (float): IRT ability estimate for this domain
- `se` (float): Standard error of theta estimate
**Expected Rows:** ~1200 (400 composite_IDs x 3 domains)
**Expected Columns:** 7

**Validation Requirement:**
Validation tools MUST be used after TSVR merge tool execution. Specific validation tools will be determined by rq_tools based on merge completeness and data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_lmm_input.csv: ~1200 rows x 7 columns

*Value Ranges:*
- TSVR_hours in [0, 200] (reasonable range for 6-day study)
- theta in [-3.0, 3.0] (bounded by IRT ability scale)
- se in [0.1, 1.5] (reasonable standard errors)
- test in {0, 1, 3, 6} (nominal test sessions)
- domain in {what, where, when} (categorical)

*Data Quality:*
- All composite_IDs from theta file present (no merge loss)
- Each composite_ID appears exactly 3 times (once per domain)
- No NaN in TSVR_hours (merge must succeed for all)
- No NaN in theta or se (IRT must have estimated all)
- ~100 unique UIDs present

*Log Validation:*
- Required pattern: "Merged X rows with TSVR"
- Required pattern: "Long format: Y rows (X composite_IDs x 3 domains)"
- Forbidden patterns: "ERROR", "Merge failed", "Missing TSVR"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step04_merge_theta_tsvr.log
- Quit script immediately (do NOT proceed to Step 5)
- g_debug invoked to diagnose

---

### Step 5: Fit LMM Trajectory Models

**Dependencies:** Step 4 (requires data/step04_lmm_input.csv)
**Complexity:** Medium-High (5 candidate models, ~5-10 min per model)

**Input:**

**File:** data/step04_lmm_input.csv
**Format:** CSV, long format
**Columns:** composite_ID, UID, test, TSVR_hours, domain, theta, se

**Processing:**

1. Load LMM input data
2. Configure 5 candidate trajectory models with Domain x Time interaction:
   - **Linear:** theta ~ TSVR_hours * domain + (TSVR_hours | UID)
   - **Quadratic:** theta ~ (TSVR_hours + TSVR_hours^2) * domain + (TSVR_hours | UID)
   - **Logarithmic:** theta ~ log(TSVR_hours + 1) * domain + (TSVR_hours | UID)
   - **Lin+Log:** theta ~ (TSVR_hours + log(TSVR_hours + 1)) * domain + (TSVR_hours | UID)
   - **Quad+Log:** theta ~ (TSVR_hours + TSVR_hours^2 + log(TSVR_hours + 1)) * domain + (TSVR_hours | UID)
3. Treatment coding: What domain as reference (Domain = what/where/when with what as baseline)
4. Fit all 5 models with REML=False (for valid AIC comparison)
5. Compare models by AIC, compute Akaike weights
6. Select best model (lowest AIC)
7. Refit best model with REML=True for final parameter estimates
8. Save model comparison and best model results

**Output:**

**File 1:** results/step05_lmm_model_comparison.csv
**Format:** CSV (one row per candidate model)
**Columns:**
- `model_name` (string): Linear, Quadratic, Logarithmic, Lin+Log, Quad+Log
- `AIC` (float): Akaike Information Criterion
- `delta_AIC` (float): Difference from best model
- `akaike_weight` (float): Relative model probability
- `converged` (bool): Whether model converged
**Expected Rows:** 5

**File 2:** results/step05_lmm_model_summary.txt
**Format:** Text file
**Content:** Full summary of best model (fixed effects, random effects, fit statistics)

**File 3:** data/step05_lmm_fitted_model.pkl
**Format:** Python pickle (statsmodels fitted model object)
**Purpose:** Store fitted model for downstream extraction and prediction

**Validation Requirement:**
Validation tools MUST be used after LMM fitting tool execution. Specific validation tools will be determined by rq_tools based on LMM convergence, model comparison, and residual diagnostic requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step05_lmm_model_comparison.csv: 5 rows x 5 columns
- results/step05_lmm_model_summary.txt: exists with content (>1KB)
- data/step05_lmm_fitted_model.pkl: exists (binary pickle file)

*Value Ranges:*
- AIC values reasonable (typically 500-3000 for this data size)
- delta_AIC >= 0 for all models (best model has delta_AIC = 0)
- akaike_weight in [0, 1], sum to 1.0 across models
- converged = True for at least 3 of 5 models (some may fail)

*Data Quality:*
- Best model MUST have converged = True
- At least one model has akaike_weight > 0.5 (clear winner) OR top 2 have combined weight > 0.8
- Model summary contains fixed effects table with coefficients, SE, z, p-values

*Log Validation:*
- Required pattern: "Best model: {model_name} (AIC = {value})"
- Required pattern: "Model converged" for best model
- Forbidden patterns: "ERROR", "All models failed", "Singular matrix"
- Acceptable warnings: "Model X did not converge" (for some candidates)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step05_fit_lmm.log
- Quit script immediately (do NOT proceed to Step 6)
- g_debug invoked to diagnose (common causes: random effects specification, data structure)

---

### Step 6: Post-Hoc Contrasts and Effect Sizes (Decision D068)

**Dependencies:** Step 5 (requires data/step05_lmm_fitted_model.pkl and results/step05_lmm_model_summary.txt)
**Complexity:** Low-Medium (contrast extraction and computation, ~2-5 min)

**Input:**

**File 1:** data/step05_lmm_fitted_model.pkl
**Format:** Python pickle (statsmodels fitted model object)

**File 2:** data/step04_lmm_input.csv
**Format:** CSV, long format (for effect size computation)

**Processing:**

1. Load fitted LMM model
2. Extract Domain x Time interaction terms (slope differences between domains)
3. Compute pairwise contrasts for forgetting slopes:
   - Where vs What (reference)
   - When vs What (reference)
   - When vs Where
4. Apply Bonferroni correction: alpha = 0.05 / 3 = 0.0167 (3 pairwise tests)
5. Report BOTH uncorrected AND corrected p-values (Decision D068)
6. Compute effect sizes:
   - Cohen's d for domain differences at each time point (T0, T1, T3, T6)
   - Partial eta-squared for Domain x Time interaction
7. Save contrast and effect size results

**Output:**

**File 1:** results/step06_post_hoc_contrasts.csv
**Format:** CSV (one row per contrast)
**Columns:**
- `contrast` (string): Comparison name (e.g., "where - what")
- `estimate` (float): Coefficient difference (slope difference)
- `se` (float): Standard error of estimate
- `z` (float): Z-statistic
- `p_uncorrected` (float): Raw p-value
- `p_bonferroni` (float): Bonferroni-corrected p-value (Decision D068)
- `significant_uncorrected` (bool): p < 0.05
- `significant_bonferroni` (bool): p < 0.0167
**Expected Rows:** 3 (three pairwise contrasts)

**File 2:** results/step06_effect_sizes.csv
**Format:** CSV
**Columns:**
- `comparison` (string): Effect description
- `cohens_d` (float): Standardized effect size
- `ci_lower` (float): 95% CI lower bound
- `ci_upper` (float): 95% CI upper bound
- `interpretation` (string): Small/Medium/Large per Cohen's guidelines
**Expected Rows:** Variable (contrasts + per-timepoint comparisons)

**Validation Requirement:**
Validation tools MUST be used after contrast computation tool execution. Specific validation tools will be determined by rq_tools based on statistical validity and effect size computation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step06_post_hoc_contrasts.csv: 3 rows x 8 columns
- results/step06_effect_sizes.csv: >3 rows x 5 columns

*Value Ranges:*
- p_uncorrected in [0, 1] (valid probability)
- p_bonferroni in [0, 1] (valid probability, >= p_uncorrected)
- z in [-10, 10] (reasonable z-statistic range)
- cohens_d in [-3, 3] (typical effect size range, |d| > 2 is very large)

*Data Quality:*
- Exactly 3 pairwise contrasts present (where-what, when-what, when-where)
- p_bonferroni = min(1.0, p_uncorrected * 3) for each row
- Both uncorrected and Bonferroni p-values present (Decision D068)
- Effect size CI contains point estimate (ci_lower <= cohens_d <= ci_upper)

*Log Validation:*
- Required pattern: "Computed 3 pairwise contrasts"
- Required pattern: "Bonferroni correction applied (alpha = 0.0167)"
- Forbidden patterns: "ERROR", "Invalid contrast", "Effect size NaN"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step06_compute_post_hoc_contrasts.log
- Quit script immediately (do NOT proceed to Step 7)
- g_debug invoked to diagnose

---

### Step 7: Prepare Trajectory Plot Data (Decision D069 Dual-Scale)

**CRITICAL NOTE:** Plot data preparation IS an analysis step. It:
- Gets executed in Step 14 CODE EXECUTION LOOP (g_code -> bash -> rq_inspect)
- MUST have validation requirements (same as any analysis step)
- Outputs to plots/*.csv (not data/*.csv) but still validated by rq_inspect
- Created by g_code during analysis (NOT by rq_plots during visualization)

**Dependencies:** Step 3 (theta scores), Step 4 (TSVR mapping), Step 5 (LMM predictions)
**Complexity:** Low (data aggregation, ~1-2 min)

**Purpose:** Aggregate analysis outputs for trajectory visualization (Option B: g_code creates plot source CSVs)

**Plot Description:** Forgetting trajectory over time with 3 lines (What/Where/When domains) showing theta decline, including observed means with 95% confidence intervals and model-predicted trajectories.

**Required Data Sources:**
- data/step03_theta_scores.csv (individual theta estimates)
- data/step04_lmm_input.csv (long format with TSVR, domain)
- data/step05_lmm_fitted_model.pkl (for model predictions)
- data/step03_item_parameters.csv (for theta-to-probability conversion)

**Processing (Theta Scale Plot Data):**

1. Load LMM input data (long format with theta, domain, TSVR_hours)
2. Group by domain and test (nominal time points: T0, T1, T3, T6)
3. Compute observed statistics per group:
   - mean_theta = mean(theta) per domain x test
   - CI_lower = mean - 1.96 * (sd / sqrt(n))
   - CI_upper = mean + 1.96 * (sd / sqrt(n))
4. Add representative TSVR_hours per test (median or typical value)
5. Generate model predictions from fitted LMM (smooth trajectory)
6. Combine observed means + model predictions
7. Save theta-scale plot data

**Processing (Probability Scale Plot Data - Decision D069):**

1. Load theta-scale plot data (from previous sub-step)
2. Load item parameters (mean discrimination a, mean difficulty b per domain)
3. Apply reverse logit transformation: P = 1 / (1 + exp(-(a * (theta - b))))
4. Use domain-specific average a and b for transformation
5. Transform CI bounds similarly (transform theta bounds to probability bounds)
6. Save probability-scale plot data

**Output (Plot Source CSVs):**

**File 1:** plots/step07_trajectory_theta_data.csv
**Format:** CSV (plot-ready data for theta scale)
**Columns:**
- `time` (float): TSVR_hours (representative time per test)
- `test` (int): Nominal test session (0, 1, 3, 6)
- `domain` (string): Memory domain (what, where, when)
- `mean_theta` (float): Observed mean theta per domain x test
- `CI_lower` (float): Lower 95% CI bound (theta scale)
- `CI_upper` (float): Upper 95% CI bound (theta scale)
- `predicted_theta` (float): LMM model prediction at this time point
- `n_obs` (int): Number of observations in group
**Expected Rows:** 12 (3 domains x 4 time points)

**File 2:** plots/step07_trajectory_probability_data.csv
**Format:** CSV (plot-ready data for probability scale - Decision D069)
**Columns:**
- `time` (float): TSVR_hours
- `test` (int): Nominal test session
- `domain` (string): Memory domain
- `mean_probability` (float): Mean theta transformed to probability scale
- `CI_lower` (float): Lower 95% CI bound (probability scale)
- `CI_upper` (float): Upper 95% CI bound (probability scale)
- `predicted_probability` (float): Model prediction on probability scale
- `n_obs` (int): Number of observations
**Expected Rows:** 12 (3 domains x 4 time points)

**Validation Requirement:**
Validation tools MUST be used after plot data preparation tool execution. Specific validation tools will be determined by rq_tools based on plot data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- plots/step07_trajectory_theta_data.csv: 12 rows x 8 columns
- plots/step07_trajectory_probability_data.csv: 12 rows x 8 columns

*Value Ranges:*
- time in [0, 200] hours (reasonable TSVR range)
- test in {0, 1, 3, 6} (nominal sessions)
- domain in {what, where, when} (categorical)
- mean_theta in [-3, 3] (IRT ability scale)
- mean_probability in [0, 1] (probability scale)
- CI_upper > CI_lower for all rows (valid intervals)
- n_obs >= 80 per group (100 participants, some missing acceptable)

*Data Quality:*
- Exactly 12 rows per file (3 domains x 4 tests, no more, no less)
- All 3 domains present (what, where, when)
- All 4 tests present (0, 1, 3, 6)
- No NaN values in any column
- Domain x test combinations unique (no duplicates)

*Log Validation:*
- Required pattern: "Plot data preparation complete: 12 rows created"
- Required pattern: "All domains represented: what, where, when"
- Required pattern: "Dual-scale conversion applied (Decision D069)"
- Forbidden patterns: "ERROR", "NaN values detected", "Missing domain"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 12 rows, found 9")
- Log failure to logs/step07_prepare_trajectory_plot_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- g_debug invoked to diagnose root cause

**Plotting Function (rq_plots will call):** Trajectory plot with confidence bands
- rq_plots agent maps this description to specific tools/plots.py function
- Plot reads plots/step07_trajectory_theta_data.csv and plots/step07_trajectory_probability_data.csv
- No data aggregation in rq_plots (visualization only per Option B)
- Decision D069: Generate BOTH theta-scale and probability-scale plots

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 -> Step 1:** Wide IRT input (composite_ID x items) + Q-matrix -> IRT model fitting
**Step 1 -> Step 2:** Pass 1 item parameters -> Apply purification thresholds -> Retained items list
**Step 2 -> Step 3:** Purified items list + original IRT input -> Filter columns -> Pass 2 IRT fitting
**Step 3 -> Step 4:** Wide theta scores -> Merge with TSVR -> Melt to long format
**Step 4 -> Step 5:** Long format LMM input -> Fit 5 candidate models -> Best model selection
**Step 5 -> Step 6:** Fitted model -> Extract contrasts and effect sizes
**Step 3-5 -> Step 7:** Multiple sources -> Aggregate for plotting -> Plot source CSVs

### Column Naming Conventions (from names.md)

| Variable | Pattern | Example | Notes |
|----------|---------|---------|-------|
| Participant ID | composite_ID | P001_0 | UID + "_" + test |
| Raw UID | UID | P001 | Participant identifier |
| Test session | test | 0, 1, 3, 6 | Nominal days |
| Time variable | TSVR_hours | 24.5 | Decision D070 - actual hours |
| Domain factor | domain | what, where, when | Categorical |
| Theta estimate | theta_<dim> | theta_what | Per-dimension ability |
| Standard error | se_<dim> | se_what | Per-dimension SE |
| Discrimination | a | 1.2 | IRT slope parameter |
| Difficulty | b | -0.5 | IRT location parameter |
| CI bounds | CI_lower, CI_upper | -0.3, 0.5 | 95% confidence interval |

### Data Type Constraints

| Column | Type | Nullable | Valid Range |
|--------|------|----------|-------------|
| composite_ID | string | No | Format: UID_test |
| UID | string | No | Format: P### |
| test | int | No | {0, 1, 3, 6} |
| TSVR_hours | float | No | [0, 200] |
| domain | string | No | {what, where, when} |
| theta | float | No | [-4, 4] typical |
| se | float | No | [0.05, 3.0] |
| a | float | No | [0.01, 10.0] |
| b | float | No | [-6, 6] |

---

## Cross-RQ Dependencies

**Dependency Type: RAW Data Only (No Dependencies)**

**This RQ uses:** Only data/cache/dfData.csv (derived from master.xlsx)
**No dependencies on other RQs:** Can be executed independently
**Execution order:** Flexible (first RQ in Chapter 5)

**Data Sources:**
- data/cache/dfData.csv - VR item responses, TSVR timing
- All data extraction uses standard pandas operations reading CSV directly

**Note:** RQ 5.1 is the baseline IRT analysis. Other RQs in Chapter 5 may depend on RQ 5.1 outputs (e.g., item parameters, theta scores), but RQ 5.1 itself has no dependencies.

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

| Step | Analysis Type | Key Validation Criteria |
|------|---------------|-------------------------|
| 0 | Data Extraction | File exists, row counts, item assignment to domains, Q-matrix validity |
| 1 | IRT Calibration (Pass 1) | Convergence achieved, parameter bounds, no NaN |
| 2 | Item Purification | Retention thresholds met, >= 10 items per domain |
| 3 | IRT Calibration (Pass 2) | Convergence achieved, improved precision vs Pass 1 |
| 4 | TSVR Merge | All IDs matched, no missing TSVR, long format correct |
| 5 | LMM Fitting | Best model converged, AIC comparison valid |
| 6 | Post-hoc Contrasts | 3 contrasts computed, dual p-values present, effect sizes valid |
| 7 | Plot Data Prep | 12 rows exactly, all domains/tests present, no NaN |

---

## Summary

**Total Steps:** 8 (Step 0 extraction + Steps 1-7 analysis)
**Estimated Runtime:** High (2-3 hours total, primarily IRT calibration)
**Cross-RQ Dependencies:** None (RAW data only from dfData.csv)
**Primary Outputs:**
- Final theta scores: data/step03_theta_scores.csv
- LMM model: data/step05_lmm_fitted_model.pkl
- Post-hoc contrasts: results/step06_post_hoc_contrasts.csv
- Effect sizes: results/step06_effect_sizes.csv
- Plot data: plots/step07_trajectory_theta_data.csv, plots/step07_trajectory_probability_data.csv
**Validation Coverage:** 100% (all 8 steps have validation requirements)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-11-22): Initial plan created by rq_planner agent
