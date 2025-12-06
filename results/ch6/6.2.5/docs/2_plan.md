# Analysis Plan: RQ 6.2.5 - Calibration Age Effects

**Research Question:** 6.2.5
**Created:** 2025-12-06
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines whether age moderates the relationship between confidence and accuracy alignment (calibration) across the 6-day retention interval. It extends the universal age null pattern from Chapter 5 (RQs 5.1.3, 5.2.3, 5.3.4, 5.4.3 all found no age x time interactions) to metacognitive monitoring. The primary hypothesis is that Age will NOT significantly moderate calibration trajectory, consistent with VR ecological encoding creating age-invariant forgetting trajectories.

**Pipeline:** LMM only (calibration scores already computed in RQ 6.2.1)

**Steps:** 6 total analysis steps (Step 0: data loading + age merging, Steps 1-5: LMM analysis + visualization)

**Estimated Runtime:** Low-Medium (5-15 minutes total)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni-corrected)
- Decision D070: TSVR as time variable (actual hours, not nominal days)

---

## Analysis Plan

This RQ requires 6 steps:

### Step 0: Load Calibration Data and Merge Age

**Dependencies:** None (first step, but requires RQ 6.2.1 completion)

**Complexity:** Low (data loading and merging only, <2 minutes)

**Purpose:** Load calibration scores from RQ 6.2.1 and merge with participant age from dfData.csv

**Input:**

**File 1:** results/ch6/6.2.1/data/step02_calibration_scores.csv
**Source:** RQ 6.2.1 (calibration computation from merged accuracy and confidence theta estimates)
**Format:** CSV with columns:
  - `UID` (string, participant identifier, format: P### with leading zeros)
  - `test` (string, test session identifier: T1, T2, T3, T4)
  - `composite_ID` (string, format: {UID}_{test})
  - `theta_accuracy` (float, IRT ability estimate from accuracy responses)
  - `theta_confidence` (float, IRT ability estimate from confidence ratings)
  - `calibration` (float, computed from theta_accuracy and theta_confidence alignment)
  - `TSVR_hours` (float, actual time since encoding in hours per Decision D070)

**Expected Rows:** 400 (100 participants x 4 tests)

**File 2:** data/cache/dfData.csv
**Source:** Project-level participant demographics file
**Format:** CSV with columns:
  - `UID` (string, participant identifier)
  - `Age` (int, participant age at enrollment in years)
  - [Other demographic columns not used in this analysis]

**Expected Rows:** 100 participants

**Processing:**

1. Load calibration scores from RQ 6.2.1 output file
2. Load participant demographics (Age) from dfData.csv
3. Merge calibration data with Age on UID (left join to preserve all 400 observations)
4. Validate merge: all 400 observations should have Age values (no missing)
5. Save merged dataset for Step 1

**Merge Logic:**
- **Key:** UID (must match exactly between files)
- **Type:** Left join (keep all calibration observations, add Age)
- **Null handling:** If Age missing for any UID, raise error (validation failure)

**Output:**

**File:** data/step00_calibration_age.csv
**Format:** CSV, one row per observation (participant-test combination)
**Columns:**
  - `UID` (string, participant identifier)
  - `test` (string, test session: T1, T2, T3, T4)
  - `composite_ID` (string, format: {UID}_{test})
  - `calibration` (float, outcome variable)
  - `TSVR_hours` (float, time variable per Decision D070)
  - `Age` (int, predictor variable in years)

**Expected Rows:** 400 (100 participants x 4 tests)
**Expected Nulls:** None (all columns must be non-null after merge)

**Validation Requirement:**

Validation tools MUST be used after data loading and merging execution. Specific validation tools will be determined by rq_tools based on data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_calibration_age.csv exists (exact path)
- Expected rows: 400 (100 participants x 4 tests)
- Expected columns: 6 (UID, test, composite_ID, calibration, TSVR_hours, Age)
- Data types: UID (string), test (string), composite_ID (string), calibration (float), TSVR_hours (float), Age (int)

*Value Ranges:*
- calibration: scientifically reasonable (range depends on metric from 6.2.1, typically -3 to +3 or 0 to 1)
- TSVR_hours in [0, 168] (0 = encoding, 168 = 1 week maximum)
- Age in [18, 85] (typical adult age range in REMEMVR study)

*Data Quality:*
- No NaN values tolerated (all cells must have valid values)
- Expected N: Exactly 400 rows (no data loss from merge)
- No duplicate composite_IDs (each participant-test combination unique)
- All 100 participants present (each UID appears exactly 4 times for 4 tests)

*Log Validation:*
- Required pattern: "Merge complete: 400 observations with Age values"
- Required pattern: "All 100 participants matched successfully"
- Forbidden patterns: "ERROR", "NaN values detected", "Age missing for UID"
- Acceptable warnings: None expected for data loading/merging

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Age missing for UID P042")
- Log failure to logs/step00_load_calibration_age.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause (likely RQ 6.2.1 incomplete or dfData.csv format changed)

---

### Step 1: Center Age Variable

**Dependencies:** Step 0 (requires merged calibration + age data)

**Complexity:** Low (simple transformation, <1 minute)

**Purpose:** Center Age variable (Age_c = Age - mean(Age)) for interpretable intercept estimates in LMM

**Input:**

**File:** data/step00_calibration_age.csv
**Source:** Step 0 (calibration data merged with Age)
**Columns:** UID, test, composite_ID, calibration, TSVR_hours, Age

**Processing:**

1. Compute mean Age across all 100 participants
2. Create centered Age variable: Age_c = Age - mean(Age)
3. Document mean Age for interpretation (e.g., "Mean Age = 45.3 years, Age_c = 0 represents 45.3-year-old")
4. Validate centering: mean(Age_c) should be approximately 0 (within floating-point tolerance)
5. Save dataset with Age_c added

**Centering Rationale:**
- Uncentered Age: intercept = calibration at Age = 0 years (meaningless)
- Centered Age_c: intercept = calibration at mean Age (interpretable as typical participant)
- Age_c coefficient = change in calibration per year above/below mean Age

**Output:**

**File:** data/step01_calibration_age_centered.csv
**Format:** CSV, one row per observation
**Columns:**
  - All columns from Step 0 input (UID, test, composite_ID, calibration, TSVR_hours, Age)
  - `Age_c` (float, centered age: Age - mean(Age))
  - `mean_Age` (float, constant column documenting mean Age for reference)

**Expected Rows:** 400 (same as input)

**Validation Requirement:**

Validation tools MUST be used after age centering execution. Specific validation tools will be determined by rq_tools based on variable transformation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_calibration_age_centered.csv exists (exact path)
- Expected rows: 400 (no data loss)
- Expected columns: 8 (original 6 + Age_c + mean_Age)
- Data types: Age_c (float), mean_Age (float)

*Value Ranges:*
- Age_c in [-50, 50] (max deviation from mean Age, typical range -30 to +30)
- mean_Age in [18, 85] (should be central value of Age distribution, typically 40-60)
- Relationship: Age = Age_c + mean_Age for all rows

*Data Quality:*
- No NaN values in Age_c (all participants must have centered age)
- Mean of Age_c approximately 0 (tolerance: abs(mean(Age_c)) < 0.001 for floating-point precision)
- SD of Age_c equals SD of Age (centering preserves variance)
- All rows have same mean_Age value (constant for reference)

*Log Validation:*
- Required pattern: "Age centering complete: mean(Age) = XX.X years"
- Required pattern: "Validation - mean(Age_c) = 0.000 (within tolerance)"
- Forbidden patterns: "ERROR", "NaN values in Age_c", "Centering failed"
- Acceptable warnings: "mean(Age_c) = 1e-15" (floating-point precision artifact, acceptable)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "mean(Age_c) = 2.3, expected ~0.0")
- Log failure to logs/step01_center_age.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose root cause

---

### Step 2: Fit LMM with Age x Time Interaction

**Dependencies:** Step 1 (requires centered age data)

**Complexity:** Medium (LMM model fitting, 5-10 minutes)

**Purpose:** Fit Linear Mixed Model testing whether age moderates calibration trajectory over time

**Input:**

**File:** data/step01_calibration_age_centered.csv
**Source:** Step 1 (calibration data with centered age)
**Required Columns:** UID, calibration, TSVR_hours, Age_c

**Processing:**

**Model Formula:**
```
calibration ~ TSVR_hours + Age_c + TSVR_hours:Age_c + (TSVR_hours | UID)
```

**Fixed Effects:**
- `TSVR_hours` (main effect of time - calibration trajectory averaged across all ages)
- `Age_c` (main effect of age - baseline calibration difference per year above/below mean)
- `TSVR_hours:Age_c` (interaction - tests if calibration trajectory slope differs by age)

**Random Effects:**
- Random intercepts by UID (participant-specific baseline calibration)
- Random slopes for TSVR_hours by UID (participant-specific calibration decline rates)
- Random intercept-slope correlation estimated

**Model Settings:**
- REML = False (maximum likelihood for model comparison if needed)
- Optimizer: Default statsmodels optimizer (LBFGS)
- Convergence tolerance: Default (1e-4)

**Time Variable (Decision D070):**
- Use TSVR_hours (actual elapsed time in hours since encoding)
- NOT nominal days (0, 1, 3, 6) - those assume fixed intervals which vary across participants

**Output:**

**File 1:** data/step02_lmm_model_summary.txt
**Format:** Text file with LMM model summary
**Contents:**
  - Model formula
  - Fixed effects table (coefficient, SE, z-value, p-value for Intercept, TSVR_hours, Age_c, TSVR_hours:Age_c)
  - Random effects variance components (Var(Intercept), Var(TSVR_hours), Cov(Intercept, TSVR_hours))
  - Model fit statistics (AIC, BIC, log-likelihood)
  - Convergence status

**File 2:** data/step02_lmm_fixed_effects.csv
**Format:** CSV with fixed effects estimates
**Columns:**
  - `term` (string, fixed effect name: Intercept, TSVR_hours, Age_c, TSVR_hours:Age_c)
  - `estimate` (float, coefficient value)
  - `se` (float, standard error)
  - `z_value` (float, z-statistic)
  - `p_value` (float, uncorrected p-value)

**Expected Rows:** 4 (one row per fixed effect term)

**File 3:** data/step02_lmm_random_effects.csv
**Format:** CSV with random effects variance components
**Columns:**
  - `component` (string, variance component name: Var(Intercept), Var(TSVR_hours), Cov(Intercept, TSVR_hours))
  - `value` (float, variance or covariance estimate)
  - `sd` (float, standard deviation if variance component, NA if covariance)

**Expected Rows:** 3 (intercept variance, slope variance, intercept-slope covariance)

**Validation Requirement:**

Validation tools MUST be used after LMM fitting execution. Specific validation tools will be determined by rq_tools based on LMM convergence and assumption checking requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_lmm_model_summary.txt exists (text file with model output)
- data/step02_lmm_fixed_effects.csv: 4 rows x 5 columns (term, estimate, se, z_value, p_value)
- data/step02_lmm_random_effects.csv: 3 rows x 3 columns (component, value, sd)

*Value Ranges:*
- Fixed effects estimates: scientifically reasonable (TSVR_hours effect likely negative for calibration decline, Age_c effect unknown, interaction likely NULL per hypothesis)
- Standard errors: positive, non-zero (se > 0)
- p-values in [0, 1]
- Random effects variances: positive (Var > 0)
- Covariance: any value (can be positive, negative, or zero)

*Data Quality:*
- No NaN values in fixed effects table (model must converge to estimates)
- All 4 fixed effect terms present (Intercept, TSVR_hours, Age_c, TSVR_hours:Age_c)
- Random effects variances > 0 (indicates participant heterogeneity)
- Model converged successfully (convergence flag = True in summary)

*Log Validation:*
- Required pattern: "Model converged: True"
- Required pattern: "VALIDATION - PASS: LMM convergence"
- Required pattern: "Fixed effects extracted: 4 terms"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "Singular matrix"
- Acceptable warnings: "Optimizer warning: max iterations" (if model converged despite warning)

**Expected Behavior on Validation Failure:**
- Methodological failure (convergence failed) -> Validation tool quits, logs error, master invokes g_debug
- Substance failure (NaN in estimates, wrong row count) -> rq_inspect quits with detailed report
- g_debug analyzes root cause: data issues, model misspecification, or numerical instability

---

### Step 3: Extract Age Effects with Bonferroni Correction

**Dependencies:** Step 2 (requires fitted LMM model outputs)

**Complexity:** Low (statistical inference, <2 minutes)

**Purpose:** Extract Age_c main effect and Age_c x TSVR_hours interaction with dual p-value reporting per Decision D068

**Input:**

**File:** data/step02_lmm_fixed_effects.csv
**Source:** Step 2 (LMM fixed effects table)
**Columns:** term, estimate, se, z_value, p_value

**Processing:**

1. Extract Age_c main effect row (term = "Age_c")
2. Extract Age_c x TSVR_hours interaction row (term = "TSVR_hours:Age_c")
3. Apply Bonferroni correction: alpha = 0.05 / 3 comparisons = 0.0167 (testing Intercept, Age_c, Age_c:TSVR_hours)
4. Compute Bonferroni-corrected p-values: p_bonferroni = min(p_uncorrected x 3, 1.0)
5. Add significance flags: p < 0.05 (uncorrected), p < 0.0167 (Bonferroni-corrected)
6. Save results table with dual p-values per Decision D068

**Bonferroni Correction (Decision D068):**
- Number of comparisons: 3 (Intercept not scientifically interesting but included for completeness)
- Corrected alpha: 0.05 / 3 = 0.0167
- Rationale: Control family-wise error rate for multiple hypothesis tests
- Dual reporting: Present BOTH uncorrected and corrected p-values for transparency

**Output:**

**File:** data/step03_age_effects.csv
**Format:** CSV with age effects and dual p-values
**Columns:**
  - `term` (string, effect name: Age_c, TSVR_hours:Age_c)
  - `estimate` (float, coefficient value)
  - `se` (float, standard error)
  - `z_value` (float, z-statistic)
  - `p_uncorrected` (float, original p-value from LMM)
  - `p_bonferroni` (float, Bonferroni-corrected p-value)
  - `sig_uncorrected` (bool, p_uncorrected < 0.05)
  - `sig_bonferroni` (bool, p_bonferroni < 0.0167)

**Expected Rows:** 2 (Age_c main effect, Age_c:TSVR_hours interaction)

**Validation Requirement:**

Validation tools MUST be used after age effects extraction execution. Specific validation tools will be determined by rq_tools based on dual p-value validation requirements (Decision D068).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_age_effects.csv exists (exact path)
- Expected rows: 2 (Age_c, TSVR_hours:Age_c)
- Expected columns: 8 (term, estimate, se, z_value, p_uncorrected, p_bonferroni, sig_uncorrected, sig_bonferroni)
- Data types: term (string), estimate/se/z_value/p_uncorrected/p_bonferroni (float), sig_uncorrected/sig_bonferroni (bool)

*Value Ranges:*
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1]
- p_bonferroni >= p_uncorrected (correction never decreases p-value)
- p_bonferroni <= min(p_uncorrected x 3, 1.0) (Bonferroni formula)

*Data Quality:*
- No NaN values in p-value columns
- Both terms present (Age_c, TSVR_hours:Age_c)
- sig_uncorrected = (p_uncorrected < 0.05) for all rows
- sig_bonferroni = (p_bonferroni < 0.0167) for all rows

*Log Validation:*
- Required pattern: "VALIDATION - PASS: Dual p-values present per Decision D068"
- Required pattern: "Age effects extracted: 2 terms"
- Required pattern: "Bonferroni correction applied: 3 comparisons"
- Forbidden patterns: "ERROR", "Missing p-value column", "Bonferroni correction failed"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "p_bonferroni missing for Age_c term")
- Log failure to logs/step03_extract_age_effects.log
- Quit script immediately (do NOT proceed to Step 4)
- g_debug invoked to diagnose root cause

---

### Step 4: Create Age Tertile Trajectories

**Dependencies:** Step 1 (requires centered age data)

**Complexity:** Low (data aggregation, <2 minutes)

**Purpose:** Split participants into age tertiles (Young/Middle/Older) and compute observed calibration means per tertile x test for visualization

**Input:**

**File:** data/step01_calibration_age_centered.csv
**Source:** Step 1 (calibration data with centered age)
**Columns:** UID, test, calibration, TSVR_hours, Age, Age_c

**Processing:**

1. Compute age tertiles based on Age distribution (not Age_c)
   - Tertile 1 (Young): Age <= 33rd percentile
   - Tertile 2 (Middle): 33rd percentile < Age <= 67th percentile
   - Tertile 3 (Older): Age > 67th percentile
2. Assign tertile labels to each participant
3. Group by tertile x test, compute:
   - Mean calibration per group
   - 95% confidence interval (mean +/- 1.96 x SE)
   - N observations per group
4. Add TSVR_hours (mean per test for plotting x-axis)
5. Save aggregated data for plotting

**Age Tertiles:**
- Based on Age distribution across 100 participants
- Equal-sized groups (approximately 33-34 participants per tertile)
- Labels: "Young" (lowest tertile), "Middle" (middle tertile), "Older" (highest tertile)

**Output:**

**File:** data/step04_age_tertile_trajectories.csv
**Format:** CSV with aggregated calibration by age tertile and test
**Columns:**
  - `age_tertile` (string, tertile label: Young, Middle, Older)
  - `test` (string, test session: T1, T2, T3, T4)
  - `TSVR_hours` (float, mean time since encoding for this test)
  - `mean_calibration` (float, mean calibration for this tertile x test)
  - `CI_lower` (float, lower 95% confidence bound)
  - `CI_upper` (float, upper 95% confidence bound)
  - `N` (int, number of observations in this group)

**Expected Rows:** 12 (3 tertiles x 4 tests)

**Validation Requirement:**

Validation tools MUST be used after age tertile aggregation execution. Specific validation tools will be determined by rq_tools based on plot data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_age_tertile_trajectories.csv exists (exact path)
- Expected rows: 12 (3 tertiles x 4 tests)
- Expected columns: 7 (age_tertile, test, TSVR_hours, mean_calibration, CI_lower, CI_upper, N)
- Data types: age_tertile (string), test (string), TSVR_hours/mean_calibration/CI_lower/CI_upper (float), N (int)

*Value Ranges:*
- TSVR_hours in [0, 168] (typical range: 0, 24, 72, 144 for T1-T4)
- mean_calibration: scientifically reasonable (depends on metric from 6.2.1)
- CI_lower < mean_calibration < CI_upper for all rows
- N per group approximately equal (33-34 participants per tertile x 4 tests = 132-136 observations per group)

*Data Quality:*
- No NaN values tolerated (all cells must have valid values)
- All 3 tertiles present (Young, Middle, Older)
- All 4 tests present per tertile (T1, T2, T3, T4)
- No duplicate tertile x test combinations
- Distribution check: CI_upper > CI_lower for all rows

*Log Validation:*
- Required pattern: "Age tertiles created: Young (N=XX), Middle (N=XX), Older (N=XX)"
- Required pattern: "Aggregation complete: 12 rows (3 tertiles x 4 tests)"
- Forbidden patterns: "ERROR", "Missing tertile", "NaN values detected"
- Acceptable warnings: None expected for aggregation

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 12 rows, found 9")
- Log failure to logs/step04_create_age_tertiles.log
- Quit script immediately (do NOT proceed to Step 5)
- g_debug invoked to diagnose root cause

---

### Step 5: Compare to Chapter 5 Age Null Findings

**Dependencies:** Step 3 (requires age effects with significance tests)

**Complexity:** Low (comparison and documentation, <2 minutes)

**Purpose:** Compare this RQ's age x time interaction finding to Chapter 5 universal age null pattern (RQs 5.1.3, 5.2.3, 5.3.4, 5.4.3)

**Input:**

**File:** data/step03_age_effects.csv
**Source:** Step 3 (age effects with dual p-values)
**Focus:** TSVR_hours:Age_c interaction term

**Processing:**

1. Extract TSVR_hours:Age_c interaction p-values (uncorrected and Bonferroni-corrected)
2. Determine significance: p < 0.05 (uncorrected) and p < 0.0167 (Bonferroni-corrected)
3. Document Chapter 5 age null pattern:
   - RQ 5.1.3 (General): Age x Time interaction NULL
   - RQ 5.2.3 (Domains): Age x Time interaction NULL
   - RQ 5.3.4 (Paradigms): Age x Time interaction NULL
   - RQ 5.4.3 (Congruence): Age x Time interaction NULL
4. Compare RQ 6.2.5 finding to Ch5 pattern:
   - Consistent: If TSVR_hours:Age_c interaction NULL (p > 0.05), metacognitive calibration replicates memory accuracy age-invariant trajectories
   - Inconsistent: If TSVR_hours:Age_c interaction significant (p < 0.05), metacognitive monitoring shows different age trajectory than memory performance
5. Interpret deviation (if any):
   - If interaction significant: Older adults may show faster calibration decline despite parallel memory decline (dissociable systems)
   - If interaction NULL: Metacognitive monitoring and memory performance show unified age-invariant pattern (consistent with ecological encoding hypothesis)
6. Save comparison summary

**Expected Pattern (Hypothesis):**
- Age_c:TSVR_hours interaction NULL (p > 0.05) - consistent with Ch5 universal age null
- Age_c main effect may be significant (baseline calibration differences) but interaction NULL (parallel trajectories)

**Output:**

**File:** data/step05_ch5_comparison.csv
**Format:** CSV documenting comparison to Chapter 5 age null findings
**Columns:**
  - `RQ` (string, RQ identifier: 5.1.3, 5.2.3, 5.3.4, 5.4.3, 6.2.5)
  - `Analysis_Type` (string, analysis category: General, Domains, Paradigms, Congruence, Calibration)
  - `Age_x_Time_p_uncorrected` (float, uncorrected p-value for interaction)
  - `Age_x_Time_p_corrected` (float, Bonferroni-corrected p-value)
  - `Significant_uncorrected` (bool, p < 0.05)
  - `Significant_corrected` (bool, p < 0.0167)
  - `Pattern` (string, "NULL" or "SIGNIFICANT")

**Expected Rows:** 5 (4 Chapter 5 RQs + this RQ 6.2.5)

**Note:** Chapter 5 p-values are documented from prior analyses (not re-computed here)

**Validation Requirement:**

Validation tools MUST be used after comparison documentation execution. Specific validation tools will be determined by rq_tools based on comparison table requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_ch5_comparison.csv exists (exact path)
- Expected rows: 5 (RQs 5.1.3, 5.2.3, 5.3.4, 5.4.3, 6.2.5)
- Expected columns: 7 (RQ, Analysis_Type, Age_x_Time_p_uncorrected, Age_x_Time_p_corrected, Significant_uncorrected, Significant_corrected, Pattern)
- Data types: RQ/Analysis_Type/Pattern (string), p-values (float), Significant flags (bool)

*Value Ranges:*
- p-values in [0, 1]
- Pattern in {"NULL", "SIGNIFICANT"}

*Data Quality:*
- No NaN values in p-value columns
- All 5 RQs present (5.1.3, 5.2.3, 5.3.4, 5.4.3, 6.2.5)
- RQ 6.2.5 row matches Step 3 Age_c:TSVR_hours interaction p-values exactly

*Log Validation:*
- Required pattern: "Comparison complete: 5 RQs documented"
- Required pattern: "RQ 6.2.5 Age x Time interaction: p = X.XXX"
- Required pattern: "Pattern consistency: X/5 RQs show NULL interaction"
- Forbidden patterns: "ERROR", "Missing RQ", "p-value mismatch"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "RQ 5.1.3 missing from comparison table")
- Log failure to logs/step05_compare_ch5_age_null.log
- Quit script immediately
- g_debug invoked to diagnose root cause

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs - intermediate and final)

- data/step00_calibration_age.csv (from Step 0: calibration + age merged)
- data/step01_calibration_age_centered.csv (from Step 1: Age_c variable added)
- data/step02_lmm_model_summary.txt (from Step 2: LMM full model output)
- data/step02_lmm_fixed_effects.csv (from Step 2: fixed effects table)
- data/step02_lmm_random_effects.csv (from Step 2: random effects variance components)
- data/step03_age_effects.csv (from Step 3: Age_c and Age_c:TSVR_hours with dual p-values)
- data/step04_age_tertile_trajectories.csv (from Step 4: plot source CSV for age tertile visualization)
- data/step05_ch5_comparison.csv (from Step 5: comparison to Chapter 5 age null pattern)

### Logs (ONLY execution logs - .log files capturing stdout/stderr)

- logs/step00_load_calibration_age.log
- logs/step01_center_age.log
- logs/step02_fit_lmm_age_interaction.log
- logs/step03_extract_age_effects.log
- logs/step04_create_age_tertiles.log
- logs/step05_compare_ch5_age_null.log

### Plots (EMPTY until rq_plots runs)

- plots/age_tertile_calibration_trajectories.png (created by rq_plots, NOT analysis steps)

### Results (EMPTY until rq_results runs)

- results/summary.md (created by rq_results, NOT analysis steps)

---

## Expected Data Formats

### Step 0 Output: Calibration with Age

**File:** data/step00_calibration_age.csv

**Format:** Long format (one row per participant-test observation)

**Columns:**
- `UID` (string, participant identifier: P001, P002, ..., P100)
- `test` (string, test session: T1, T2, T3, T4)
- `composite_ID` (string, UID_test format: P001_T1, P001_T2, etc.)
- `calibration` (float, outcome variable from RQ 6.2.1)
- `TSVR_hours` (float, time since encoding in hours: 0-168 range)
- `Age` (int, participant age in years: 18-85 range)

**Expected Rows:** 400 (100 participants x 4 tests)

**Merge Result:** All 400 observations from calibration data matched with Age from dfData.csv

---

### Step 1 Output: Centered Age

**File:** data/step01_calibration_age_centered.csv

**Format:** Long format (same structure as Step 0 with Age_c added)

**Transformation:**
- Input: Step 0 output (6 columns)
- Add: Age_c = Age - mean(Age)
- Add: mean_Age (constant documenting mean for reference)
- Output: 8 columns total

**New Columns:**
- `Age_c` (float, centered age: -30 to +30 typical range)
- `mean_Age` (float, constant value documenting centering point)

**Validation:** mean(Age_c) = 0.0 (within floating-point tolerance)

---

### Step 2 Output: LMM Model Results

**File 1:** data/step02_lmm_fixed_effects.csv

**Format:** CSV with one row per fixed effect term

**Columns:**
- `term` (string, effect name)
- `estimate` (float, coefficient)
- `se` (float, standard error)
- `z_value` (float, z-statistic)
- `p_value` (float, uncorrected p-value)

**Expected Rows:** 4
1. Intercept (baseline calibration at mean Age and time = 0)
2. TSVR_hours (time main effect)
3. Age_c (age main effect)
4. TSVR_hours:Age_c (age x time interaction - PRIMARY INTEREST)

---

### Step 3 Output: Age Effects with Dual P-Values

**File:** data/step03_age_effects.csv

**Format:** CSV with age-related terms only (subset of Step 2 fixed effects)

**Columns:**
- All columns from Step 2 fixed effects
- `p_uncorrected` (renamed from p_value for clarity)
- `p_bonferroni` (Bonferroni-corrected p-value)
- `sig_uncorrected` (bool, p < 0.05)
- `sig_bonferroni` (bool, p < 0.0167)

**Expected Rows:** 2
1. Age_c (main effect)
2. TSVR_hours:Age_c (interaction - tests hypothesis)

**Decision D068 Compliance:** Dual p-values present (uncorrected + Bonferroni)

---

### Step 4 Output: Age Tertile Trajectories

**File:** data/step04_age_tertile_trajectories.csv

**Format:** Aggregated data for plotting (wide format: tertile x test combinations)

**Columns:**
- `age_tertile` (string, categorical: Young, Middle, Older)
- `test` (string, T1, T2, T3, T4)
- `TSVR_hours` (float, mean time for this test)
- `mean_calibration` (float, mean calibration for this tertile x test)
- `CI_lower` (float, 95% CI lower bound)
- `CI_upper` (float, 95% CI upper bound)
- `N` (int, observations per group)

**Expected Rows:** 12 (3 tertiles x 4 tests)

**Use:** Plot source data for age tertile trajectory visualization (rq_plots reads this for plotting)

---

## Cross-RQ Dependencies

**This RQ depends on:** RQ 6.2.1 (calibration scores computed from accuracy and confidence theta estimates)

**Required Files from RQ 6.2.1:**
- results/ch6/6.2.1/data/step02_calibration_scores.csv (400 observations: calibration per participant-test)

**Status Check:**
- Step 0 should verify results/ch6/6.2.1/data/step02_calibration_scores.csv exists
- If RQ 6.2.1 incomplete: QUIT with "FAIL: RQ 6.2.1 must complete before this RQ (dependency)"

**Data Integration:**
- Step 0: Load calibration from RQ 6.2.1, merge with Age from dfData.csv
- Expected: 400 observations matched (no missing)

**Execution Order Constraint:**
1. RQ 6.2.1 must complete first (provides calibration scores)
2. This RQ executes second (analyzes age moderation of calibration trajectories)

**Data Source Boundaries:**
- **DERIVED data:** Calibration scores from RQ 6.2.1 (not re-computed here)
- **RAW data:** Age from dfData.csv (master demographics file)
- **Scope:** This RQ does NOT compute calibration (uses RQ 6.2.1 output as input)

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

#### Step 0: Load Calibration Data and Merge Age

**Analysis Tool:** (determined by rq_tools - likely pandas merge operations)
**Validation Tool:** (determined by rq_tools - likely validate_dataframe_structure, check_missing_data)

**What Validation Checks:**
- Output file exists (data/step00_calibration_age.csv)
- Expected row count (400 rows: 100 participants x 4 tests)
- Expected column count (6 columns: UID, test, composite_ID, calibration, TSVR_hours, Age)
- No NaN values in any column (all 400 observations must have Age values)
- All 100 participants present (each UID appears exactly 4 times)
- Value ranges: calibration (metric-dependent), TSVR_hours [0, 168], Age [18, 85]

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Age missing for UID P042")
- Log failure to logs/step00_load_calibration_age.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose (likely RQ 6.2.1 incomplete or dfData.csv format issue)

---

#### Step 1: Center Age Variable

**Analysis Tool:** (determined by rq_tools - likely pandas transform operations)
**Validation Tool:** (determined by rq_tools - likely validate_standardization with tolerance)

**What Validation Checks:**
- Output file exists (data/step01_calibration_age_centered.csv)
- Expected column count (8 columns: original 6 + Age_c + mean_Age)
- Age_c mean approximately 0 (tolerance: abs(mean(Age_c)) < 0.001)
- Age_c SD equals Age SD (centering preserves variance)
- Relationship holds: Age = Age_c + mean_Age for all rows
- No NaN values in Age_c

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "mean(Age_c) = 2.3, expected ~0.0")
- Log failure to logs/step01_center_age.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose (likely centering formula error)

---

#### Step 2: Fit LMM with Age x Time Interaction

**Analysis Tool:** (determined by rq_tools - likely fit_lmm_trajectory_tsvr)
**Validation Tool:** (determined by rq_tools - likely validate_lmm_convergence, validate_lmm_assumptions_comprehensive)

**What Validation Checks:**
- Model converged successfully (convergence flag = True)
- Fixed effects table: 4 rows (Intercept, TSVR_hours, Age_c, TSVR_hours:Age_c)
- No NaN values in coefficients or p-values
- Random effects variances > 0 (Var(Intercept), Var(TSVR_hours))
- Standard errors > 0 for all terms
- p-values in [0, 1]
- Residuals normality (Kolmogorov-Smirnov test, visual Q-Q plot)

**Expected Behavior on Validation Failure:**
- Methodological failure (convergence failed) -> Validation tool quits, logs error, master invokes g_debug
- Substance failure (NaN in estimates, wrong row count) -> rq_inspect quits with detailed report
- g_debug analyzes root cause: data issues, model misspecification, numerical instability

---

#### Step 3: Extract Age Effects with Bonferroni Correction

**Analysis Tool:** (determined by rq_tools - likely pandas operations + bonferroni correction)
**Validation Tool:** (determined by rq_tools - likely validate_hypothesis_test_dual_pvalues per D068)

**What Validation Checks:**
- Output file exists (data/step03_age_effects.csv)
- Expected row count (2 rows: Age_c, TSVR_hours:Age_c)
- Dual p-values present (p_uncorrected, p_bonferroni columns exist)
- p_bonferroni >= p_uncorrected (correction never decreases p-value)
- p_bonferroni <= min(p_uncorrected x 3, 1.0) (Bonferroni formula correct)
- Significance flags match thresholds (sig_uncorrected = p < 0.05, sig_bonferroni = p < 0.0167)
- No NaN values in p-value columns

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "p_bonferroni missing for Age_c term")
- Log failure to logs/step03_extract_age_effects.log
- Quit script immediately (do NOT proceed to Step 4)
- g_debug invoked to diagnose (likely Decision D068 implementation error)

---

#### Step 4: Create Age Tertile Trajectories

**Analysis Tool:** (determined by rq_tools - likely pandas groupby + aggregation)
**Validation Tool:** (determined by rq_tools - likely validate_plot_data_completeness)

**What Validation Checks:**
- Output file exists (data/step04_age_tertile_trajectories.csv)
- Expected row count (12 rows: 3 tertiles x 4 tests)
- All 3 tertiles present (Young, Middle, Older)
- All 4 tests present per tertile (T1, T2, T3, T4)
- No NaN values in mean_calibration, CI_lower, CI_upper
- Distribution check: CI_lower < mean_calibration < CI_upper for all rows
- N approximately equal across groups (33-34 participants per tertile x 4 tests)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Expected 12 rows, found 9")
- Log failure to logs/step04_create_age_tertiles.log
- Quit script immediately (do NOT proceed to Step 5)
- g_debug invoked to diagnose (likely tertile assignment or aggregation error)

---

#### Step 5: Compare to Chapter 5 Age Null Findings

**Analysis Tool:** (determined by rq_tools - likely pandas operations for comparison table)
**Validation Tool:** (determined by rq_tools - likely validate_dataframe_structure)

**What Validation Checks:**
- Output file exists (data/step05_ch5_comparison.csv)
- Expected row count (5 rows: RQs 5.1.3, 5.2.3, 5.3.4, 5.4.3, 6.2.5)
- All 5 RQs present
- RQ 6.2.5 p-values match Step 3 Age_c:TSVR_hours interaction exactly
- p-values in [0, 1]
- Pattern values in {"NULL", "SIGNIFICANT"}
- No NaN values in p-value columns

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "RQ 5.1.3 missing from comparison table")
- Log failure to logs/step05_compare_ch5_age_null.log
- Quit script immediately
- g_debug invoked to diagnose (likely comparison logic error)

---

## Summary

**Total Steps:** 6 (Step 0: data loading + merge, Steps 1-5: LMM analysis + visualization prep)

**Estimated Runtime:** Low-Medium (5-15 minutes total)
- Step 0: <2 minutes (data loading/merging)
- Step 1: <1 minute (age centering)
- Step 2: 5-10 minutes (LMM fitting)
- Step 3: <2 minutes (age effects extraction)
- Step 4: <2 minutes (age tertile aggregation)
- Step 5: <2 minutes (comparison documentation)

**Cross-RQ Dependencies:** RQ 6.2.1 (calibration scores required)

**Primary Outputs:**
- data/step03_age_effects.csv (age x time interaction with dual p-values - PRIMARY RESULT)
- data/step04_age_tertile_trajectories.csv (plot source CSV for visualization)
- data/step05_ch5_comparison.csv (comparison to Chapter 5 age null pattern)

**Validation Coverage:** 100% (all 6 steps have validation requirements with 4-layer substance criteria)

**Hypothesis Test:**
- Primary: Age_c:TSVR_hours interaction NULL (p > 0.05) - consistent with Ch5 universal age null
- Secondary: Age_c main effect may be significant (baseline calibration differences)

**Theoretical Implication:**
- If interaction NULL: Metacognitive calibration replicates memory accuracy age-invariant trajectories (unified system)
- If interaction significant: Metacognitive monitoring shows different age trajectory than memory performance (dissociable systems)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent for RQ 6.2.5
