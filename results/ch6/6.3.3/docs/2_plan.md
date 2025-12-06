# Analysis Plan for RQ 6.3.3: Age x Domain Interaction in Confidence Decline

**Created by:** rq_planner agent
**Date:** 2025-12-06
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This RQ tests whether age interacts with memory domain (What/Where/When) for confidence decline trajectories over a 6-day retention interval. It parallels Chapter 5 RQ 5.2.3 (age x domain interaction for accuracy), testing whether confidence shows the same age-invariant forgetting pattern found for accuracy across all Chapter 5 analyses.

**Analysis Type:** Linear Mixed Models (LMM) only - no IRT calibration (uses theta scores from RQ 6.3.1)

**Total Steps:** 4 analysis steps

**Expected Result:** NULL 3-way interaction (Age x Domain x Time) expected based on Chapter 5 findings, indicating age-invariant confidence decline across all domains (replicating accuracy pattern).

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni for 3-way interaction test)
- Decision D070: TSVR as LMM time variable (actual hours, not nominal days)

---

## Analysis Plan

### Step 0: Load Confidence Theta Scores and Merge with Age

**Dependencies:** None (first step - loads outputs from RQ 6.3.1)

**Complexity:** Low (data loading and merging only, <5 minutes)

**Input:**

**File 1:** results/ch6/6.3.1/data/step03_theta_confidence_domain.csv
**Source:** RQ 6.3.1 Step 3 (IRT calibration with 3-factor GRM for What/Where/When confidence)
**Format:** CSV with columns:
  - `composite_ID` (string, format: UID_test, e.g., P001_T1)
  - `theta_what` (float, confidence ability estimate for What domain)
  - `theta_where` (float, confidence ability estimate for Where domain)
  - `theta_when` (float, confidence ability estimate for When domain)
  - `se_what` (float, standard error for What)
  - `se_where` (float, standard error for Where)
  - `se_when` (float, standard error for When)
**Expected Rows:** 400 (100 participants x 4 tests)

**File 2:** data/cache/dfData.csv
**Source:** Project-level participant data
**Columns Needed:**
  - `UID` (string, participant identifier)
  - `Age` (int, age in years at T1 encoding)
**Expected Rows:** 100 participants

**Processing:**

1. Load theta scores from RQ 6.3.1 (step03_theta_confidence_domain.csv)
2. Extract Age variable from dfData.csv (one row per participant)
3. Parse composite_ID to extract UID (e.g., "P001_T1" -> "P001")
4. Merge theta scores with Age on UID (left join to preserve all theta observations)
5. Validate all participants have Age values (no missing data expected)

**Output:**

**File:** data/step00_theta_with_age.csv
**Format:** CSV with columns:
  - `composite_ID` (string)
  - `UID` (string, extracted from composite_ID)
  - `Age` (int, age in years)
  - `theta_what` (float)
  - `theta_where` (float)
  - `theta_when` (float)
  - `se_what` (float)
  - `se_where` (float)
  - `se_when` (float)
**Expected Rows:** 400 (100 participants x 4 tests, all matched with Age)

**Validation Requirement:**

Validation tools MUST be used after data loading tool execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_theta_with_age.csv exists (exact path)
- Expected rows: 400 (100 participants x 4 tests)
- Expected columns: 9 (composite_ID, UID, Age, theta_what, theta_where, theta_when, se_what, se_where, se_when)
- Data types: string (composite_ID, UID), int (Age), float (all theta and se columns)

*Value Ranges:*
- Age in [18, 80] (typical adult participant range)
- theta_what in [-3, 3] (typical IRT ability range)
- theta_where in [-3, 3]
- theta_when in [-3, 3]
- se_what in [0.1, 1.0] (standard error range, >1.0 indicates unreliable estimates)
- se_where in [0.1, 1.0]
- se_when in [0.1, 1.0]

*Data Quality:*
- No NaN values tolerated in Age column (all participants must have age)
- No NaN values in theta columns (all theta estimates must be present from RQ 6.3.1)
- No NaN values in se columns (all standard errors must be present)
- Expected N: Exactly 400 rows (no data loss from merge)
- No duplicate composite_IDs (each participant-test combination unique)

*Log Validation:*
- Required pattern: "Loaded 400 observations from RQ 6.3.1"
- Required pattern: "Merged with Age: 400 rows, 0 missing"
- Forbidden patterns: "ERROR", "NaN detected", "Merge failed"
- Acceptable warnings: None expected for this step

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 400 rows, found 387")
- Log failure to logs/step00_load_data.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause (likely RQ 6.3.1 incomplete or missing participants)

---

### Step 1: Center Age and Reshape to Long Format

**Dependencies:** Step 0 (requires theta_with_age.csv)

**Complexity:** Low (data transformation only, <5 minutes)

**Input:**

**File:** data/step00_theta_with_age.csv (from Step 0)
**Format:** Wide format (one row per composite_ID with theta_what, theta_where, theta_when)

**Processing:**

1. Center Age variable: Age_c = Age - mean(Age)
   - Centering facilitates interpretation (Age_c=0 = mean age, not age=0)
   - Reduces multicollinearity in interaction terms
   - Preserves variance (SD unchanged)
2. Reshape from wide to long format:
   - Input: 400 rows x 9 columns (one row per participant-test, three theta columns)
   - Output: 1200 rows x 5 columns (one row per participant-test-domain)
   - Stack theta_what, theta_where, theta_when into single theta_confidence column
   - Add domain factor column (What/Where/When)
3. Parse test number from composite_ID (e.g., "P001_T1" -> test=1)
4. Add TSVR_hours from dfData.csv (merge on UID + test)
   - Per Decision D070: Use actual elapsed hours, not nominal days

**Output:**

**File:** data/step01_lmm_input.csv
**Format:** CSV, long format (one row per observation)
**Columns:**
  - `UID` (string, participant identifier)
  - `Age_c` (float, centered age: Age - mean(Age))
  - `Domain` (string, values: What, Where, When)
  - `test` (int, values: 1, 2, 3, 4 for T1-T4)
  - `TSVR_hours` (float, actual time since encoding in hours)
  - `theta_confidence` (float, confidence ability estimate)
  - `se_confidence` (float, standard error of theta estimate)
**Expected Rows:** 1200 (400 observations x 3 domains = 100 participants x 4 tests x 3 domains)

**Validation Requirement:**

Validation tools MUST be used after data transformation tool execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_lmm_input.csv exists
- Expected rows: 1200 (100 participants x 4 tests x 3 domains)
- Expected columns: 7 (UID, Age_c, Domain, test, TSVR_hours, theta_confidence, se_confidence)
- Data types: string (UID, Domain), int (test), float (Age_c, TSVR_hours, theta_confidence, se_confidence)

*Value Ranges:*
- Age_c: mean approximately 0 (±0.5 due to rounding), SD preserved from original Age
- Domain in {What, Where, When} (categorical, exactly 3 levels)
- test in {1, 2, 3, 4} (categorical, exactly 4 levels)
- TSVR_hours in [0, 168] (0=encoding, 168=1 week, based on 6-day retention)
- theta_confidence in [-3, 3] (typical IRT range)
- se_confidence in [0.1, 1.0]

*Data Quality:*
- No NaN values tolerated (all cells must have valid values)
- Expected N: Exactly 1200 rows
- Balanced design: 400 observations per domain (What, Where, When)
- All participants present: 100 unique UIDs
- Age_c standardization: mean(Age_c) approximately 0, abs(mean) < 0.5
- Distribution check: Each UID has exactly 12 rows (4 tests x 3 domains)

*Log Validation:*
- Required pattern: "Age centered: mean = [value close to 0], SD = [original SD]"
- Required pattern: "Reshaped to long: 1200 rows (400 obs x 3 domains)"
- Required pattern: "Balanced design: 400 What, 400 Where, 400 When"
- Forbidden patterns: "ERROR", "NaN detected", "Imbalanced design"
- Acceptable warnings: "TSVR varies by participant (expected per D070)"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step01_transform_data.log
- Quit immediately
- g_debug invoked

---

### Step 2: Fit LMM with 3-Way Interaction (Age x Domain x Time)

**Dependencies:** Step 1 (requires lmm_input.csv)

**Complexity:** Medium (LMM fitting with interaction terms, 5-15 minutes depending on convergence)

**Input:**

**File:** data/step01_lmm_input.csv (from Step 1)
**Format:** Long format LMM input (1200 rows)

**Processing:**

1. Fit Linear Mixed Model using statsmodels MixedLM:
   - Formula: theta_confidence ~ (TSVR_hours + TSVR_log) * Age_c * Domain + (TSVR_hours | UID)
   - Fixed effects: All main effects, all 2-way interactions, 3-way interaction
   - Random effects: Random intercept and slope for TSVR_hours by participant (UID)
   - TSVR_log = log(TSVR_hours + 1) to capture potential logarithmic decline per RQ 6.1.1 best model
2. Extract 3-way interaction coefficients:
   - Age_c : Domain[Where] : TSVR_hours
   - Age_c : Domain[When] : TSVR_hours
   - Age_c : Domain[Where] : TSVR_log
   - Age_c : Domain[When] : TSVR_log
   - (Reference category: What domain)
3. Test 3-way interaction with Bonferroni correction:
   - Alpha = 0.05 / 3 = 0.0167 (correcting for 3 domains, though What is reference)
   - Report BOTH uncorrected and Bonferroni-corrected p-values per Decision D068
4. Validate convergence and residuals

**Output:**

**File 1:** data/step02_lmm_summary.txt
**Format:** Text file with full model summary
**Contents:**
  - Fixed effects table (coefficients, SE, z-values, p-values)
  - Random effects variance components
  - Model fit indices (AIC, BIC, log-likelihood)
  - Convergence status

**File 2:** data/step02_interaction_terms.csv
**Format:** CSV with 3-way interaction coefficients
**Columns:**
  - `term` (string, interaction term name)
  - `coef` (float, coefficient estimate)
  - `se` (float, standard error)
  - `z` (float, z-statistic)
  - `p_uncorrected` (float, uncorrected p-value)
  - `p_bonferroni` (float, Bonferroni-corrected p-value for alpha=0.0167)
**Expected Rows:** 4 (2 domains x 2 time variables: Where x TSVR_hours, Where x TSVR_log, When x TSVR_hours, When x TSVR_log, all interacting with Age_c)

**Validation Requirement:**

Validation tools MUST be used after LMM fitting tool execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_lmm_summary.txt exists (full model output)
- data/step02_interaction_terms.csv exists
- Expected rows in interaction_terms.csv: 4 (2 domains x 2 time variables)
- Expected columns: 6 (term, coef, se, z, p_uncorrected, p_bonferroni)
- Data types: string (term), float (all others)

*Value Ranges:*
- coef: unrestricted (can be positive or negative)
- se > 0 (standard errors must be positive)
- z: unrestricted (z-statistic can be any value)
- p_uncorrected in [0, 1] (probability range)
- p_bonferroni in [0, 1] (corrected p-value, typically larger than uncorrected)

*Data Quality:*
- No NaN values in interaction_terms.csv (model must converge and estimate all terms)
- Convergence achieved: lmm_summary.txt must contain "Converged: True" or equivalent
- Relationship check: p_bonferroni >= p_uncorrected for all rows (correction increases p-value)
- All 4 interaction terms present (no missing terms indicates successful estimation)

*Log Validation:*
- Required pattern: "Model converged: True"
- Required pattern: "3-way interaction tested: 4 terms extracted"
- Required pattern: "Bonferroni correction applied: alpha = 0.0167"
- Forbidden patterns: "ERROR", "Convergence failed", "Singular matrix"
- Acceptable warnings: "Hessian not positive definite (use with caution)"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step02_fit_lmm.log
- Quit immediately
- g_debug invoked (likely multicollinearity or insufficient variance)

---

### Step 3: Compare to Chapter 5 RQ 5.2.3 (Accuracy Results)

**Dependencies:** Step 2 (requires interaction_terms.csv from LMM)

**Complexity:** Low (file comparison and reporting, <5 minutes)

**Input:**

**File 1:** data/step02_interaction_terms.csv (from Step 2 - confidence 3-way interaction)

**File 2:** results/ch5/5.2.3/data/stepNN_interaction_terms.csv (from Ch5 RQ 5.2.3 - accuracy 3-way interaction)
**Note:** Exact step number depends on Ch5 5.2.3 analysis plan (likely step05 or step06)
**Expected Columns:** Same structure as this RQ (term, coef, se, z, p_uncorrected, p_bonferroni)

**Processing:**

1. Load confidence interaction terms (this RQ)
2. Load accuracy interaction terms (Ch5 5.2.3)
3. Compare p-values for 3-way interaction:
   - Expected: BOTH analyses show p > 0.05 (NULL interaction)
   - Check: Do confidence and accuracy replicate the same null pattern?
4. Create comparison table with side-by-side coefficients and p-values
5. Generate interpretation:
   - If both NULL: "Confidence replicates accuracy null pattern (age-invariant decline)"
   - If confidence NULL but accuracy significant: "Dissociation - metacognition age-invariant but memory age-sensitive"
   - If both significant: "Age moderates both accuracy and confidence across domains"

**Output:**

**File:** data/step03_ch5_comparison.csv
**Format:** CSV comparing confidence vs accuracy interaction results
**Columns:**
  - `term` (string, interaction term name)
  - `confidence_coef` (float, coefficient from this RQ)
  - `confidence_p_bonferroni` (float, corrected p-value from this RQ)
  - `accuracy_coef` (float, coefficient from Ch5 5.2.3)
  - `accuracy_p_bonferroni` (float, corrected p-value from Ch5 5.2.3)
  - `both_null` (bool, True if both p > 0.05)
  - `interpretation` (string, summary of comparison)
**Expected Rows:** 4 (2 domains x 2 time variables)

**Validation Requirement:**

Validation tools MUST be used after comparison tool execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_ch5_comparison.csv exists
- Expected rows: 4 (matching interaction_terms.csv from Step 2)
- Expected columns: 7 (term, confidence_coef, confidence_p_bonferroni, accuracy_coef, accuracy_p_bonferroni, both_null, interpretation)
- Data types: string (term, interpretation), float (coef and p columns), bool (both_null)

*Value Ranges:*
- confidence_coef: unrestricted
- accuracy_coef: unrestricted
- confidence_p_bonferroni in [0, 1]
- accuracy_p_bonferroni in [0, 1]
- both_null in {True, False}
- interpretation: non-empty string for each row

*Data Quality:*
- No NaN values except if Ch5 5.2.3 file not found (then skip comparison, document in log)
- Expected pattern (based on Ch5 findings): both_null = True for all 4 rows
- All 4 terms present (no missing rows)

*Log Validation:*
- Required pattern: "Loaded confidence interaction: 4 terms"
- Required pattern: "Loaded accuracy interaction: 4 terms"
- Required pattern: "Comparison complete: 4 terms matched"
- Forbidden patterns: "ERROR", "File not found" (unless Ch5 5.2.3 incomplete - then expected)
- Acceptable warnings: "Ch5 5.2.3 not found - skipping comparison (RQ may not be complete yet)"

**Expected Behavior on Validation Failure:**
- If Ch5 5.2.3 file missing: Log warning, create comparison.csv with only confidence columns, set accuracy columns to NaN, interpretation = "Ch5 5.2.3 not available for comparison"
- If structure mismatch: Raise error with specific mismatch details
- Log to logs/step03_compare_ch5.log
- g_debug invoked if structural error (not if Ch5 file missing)

---

## Expected Data Formats

### Wide to Long Transformation (Step 1)

**Input Format (Step 0 output):**
```
composite_ID, UID, Age, theta_what, theta_where, theta_when, se_what, se_where, se_when
P001_T1, P001, 25, -0.5, 0.2, 0.8, 0.3, 0.4, 0.5
P001_T2, P001, 25, -0.3, 0.1, 0.6, 0.3, 0.4, 0.5
...
```

**Output Format (Step 1 output):**
```
UID, Age_c, Domain, test, TSVR_hours, theta_confidence, se_confidence
P001, -10.5, What, 1, 0.0, -0.5, 0.3
P001, -10.5, Where, 1, 0.0, 0.2, 0.4
P001, -10.5, When, 1, 0.0, 0.8, 0.5
P001, -10.5, What, 2, 24.0, -0.3, 0.3
P001, -10.5, Where, 2, 24.0, 0.1, 0.4
P001, -10.5, When, 2, 24.0, 0.6, 0.5
...
```

**Transformation Logic:**
- Each composite_ID row (400 total) expands to 3 rows (one per domain)
- theta_what, theta_where, theta_when stack into theta_confidence column
- Domain column indicates which theta value (What/Where/When)
- Age_c computed as Age - mean(Age) across all participants
- TSVR_hours added from dfData.csv lookup
- se_what, se_where, se_when stack into se_confidence column

---

## Cross-RQ Dependencies

**This RQ requires outputs from:**

### RQ 6.3.1 (Domain Confidence Trajectories - 3-Factor GRM)

**File:** results/ch6/6.3.1/data/step03_theta_confidence_domain.csv
**Used in:** Step 0 (load confidence theta scores stratified by domain)
**Rationale:** RQ 6.3.1 calibrates 3-factor GRM (What/Where/When) for confidence items. This RQ uses those domain-stratified theta estimates to test age x domain interaction.

**Execution Order Constraint:**
1. RQ 6.3.1 must complete Steps 0-3 (data extraction, IRT calibration, theta extraction) BEFORE this RQ can run
2. This RQ (6.3.3) uses RQ 6.3.1 outputs as starting point

**Data Source Boundaries:**
- **DERIVED data:** Theta scores from RQ 6.3.1 (no IRT calibration in this RQ)
- **RAW data:** Age variable from dfData.csv (participant metadata)
- **Scope:** This RQ does NOT calibrate IRT models (uses RQ 6.3.1 theta scores directly), ONLY fits LMM with age interaction

**Validation:**
- Step 0: Check results/ch6/6.3.1/data/step03_theta_confidence_domain.csv exists
- If file missing -> EXPECTATIONS ERROR: "RQ 6.3.1 must complete before RQ 6.3.3 (dependency)"
- Expected: 400 rows (100 participants x 4 tests), 7 columns (composite_ID + 3 theta + 3 se)

---

### Chapter 5 RQ 5.2.3 (Age x Domain Interaction for Accuracy - Optional Comparison)

**File:** results/ch5/5.2.3/data/stepNN_interaction_terms.csv
**Used in:** Step 3 (compare confidence vs accuracy interaction results)
**Rationale:** Direct comparison to accuracy findings tests whether confidence replicates age-invariant pattern found for memory performance.

**Execution Order Constraint:**
- RQ 5.2.3 completion NOT required for this RQ to execute (comparison is optional validation step)
- If RQ 5.2.3 incomplete, Step 3 logs warning and creates comparison.csv with confidence-only data

**Validation:**
- Step 3: Check if results/ch5/5.2.3/data/stepNN_interaction_terms.csv exists
- If missing: Log warning "Ch5 5.2.3 not available - skipping comparison", continue without error
- If present: Load and compare to confidence interaction terms

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

#### Step 0: Load Confidence Theta Scores and Merge with Age

**Analysis Tool:** (determined by rq_tools - likely pandas read_csv + merge operations)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure)

**What Validation Checks:**
- Output file exists (data/step00_theta_with_age.csv)
- Expected row count (400 rows: 100 participants x 4 tests)
- Expected column count (9 columns: composite_ID, UID, Age, 3 theta, 3 se)
- No NaN in Age column (all participants must have age data)
- No NaN in theta or se columns (all estimates must be present from RQ 6.3.1)
- Age range scientifically reasonable (18-80 years)
- Theta range typical (-3 to 3)
- SE range reasonable (0.1 to 1.0, values >1.0 indicate unreliable estimates)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 400 rows, found 387 - check RQ 6.3.1 completion")
- Log failure to logs/step00_load_data.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause

---

#### Step 1: Center Age and Reshape to Long Format

**Analysis Tool:** (determined by rq_tools - likely pandas transform + melt operations)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_standardization + validate_dataframe_structure)

**What Validation Checks:**
- Output file exists (data/step01_lmm_input.csv)
- Expected row count (1200 rows: 400 obs x 3 domains)
- Expected column count (7 columns: UID, Age_c, Domain, test, TSVR_hours, theta_confidence, se_confidence)
- Age centering successful (mean(Age_c) approximately 0, SD preserved)
- Balanced design (400 rows per domain: What, Where, When)
- No NaN values (complete data required for LMM)
- Domain factor has exactly 3 levels (What, Where, When)
- TSVR_hours range valid (0 to 168 hours for 6-day retention)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step01_transform_data.log
- Quit immediately
- g_debug invoked

---

#### Step 2: Fit LMM with 3-Way Interaction

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.fit_lmm_trajectory_tsvr)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_lmm_convergence + validate_hypothesis_test_dual_pvalues)

**What Validation Checks:**
- Output files exist (lmm_summary.txt, interaction_terms.csv)
- Model converged successfully (no singular matrix warnings)
- 3-way interaction terms extracted (4 rows in interaction_terms.csv)
- Dual p-values present (uncorrected + Bonferroni columns)
- p_bonferroni >= p_uncorrected (correction increases p-value)
- No NaN in coefficients or p-values (successful estimation)
- Residuals approximately normal (Kolmogorov-Smirnov test)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step02_fit_lmm.log
- Quit immediately
- g_debug invoked (likely multicollinearity or convergence issue)

---

#### Step 3: Compare to Chapter 5 RQ 5.2.3

**Analysis Tool:** (determined by rq_tools - likely pandas comparison operations)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure)

**What Validation Checks:**
- Output file exists (ch5_comparison.csv)
- Expected row count (4 rows matching interaction_terms.csv)
- All required columns present (term, confidence_coef, confidence_p, accuracy_coef, accuracy_p, both_null, interpretation)
- If Ch5 file found: No NaN in accuracy columns
- If Ch5 file missing: NaN in accuracy columns acceptable, interpretation documents this

**Expected Behavior on Validation Failure:**
- If Ch5 file missing: Log warning (not error), create comparison with confidence-only data
- If structural mismatch: Raise error
- Log to logs/step03_compare_ch5.log
- g_debug invoked only if structural error (not if Ch5 missing)

---

## Summary

**Total Steps:** 4 (Step 0: load data, Step 1: transform, Step 2: fit LMM, Step 3: compare to Ch5)

**Estimated Runtime:** Low-Medium (15-25 minutes total: 5 min load, 5 min transform, 10-15 min LMM fit, <5 min comparison)

**Cross-RQ Dependencies:**
- **Required:** RQ 6.3.1 (domain-stratified confidence theta scores)
- **Optional:** Ch5 5.2.3 (accuracy interaction results for comparison)

**Primary Outputs:**
- data/step00_theta_with_age.csv (400 rows: theta scores + age)
- data/step01_lmm_input.csv (1200 rows: long format LMM input)
- data/step02_lmm_summary.txt (full LMM output)
- data/step02_interaction_terms.csv (4 rows: 3-way interaction coefficients with dual p-values)
- data/step03_ch5_comparison.csv (4 rows: confidence vs accuracy comparison)

**Validation Coverage:** 100% (all 4 steps have validation requirements with 4-layer substance criteria)

**Expected Result:** NULL 3-way interaction (p > 0.05 Bonferroni-corrected), replicating Chapter 5 age-invariant forgetting pattern for confidence judgments.

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent for RQ 6.3.3
