# Analysis Plan: RQ 5.3.3 - Paradigm Consolidation Window

**Research Question:** 5.3.3
**Created:** 2025-12-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines whether retrieval paradigms (Free Recall, Cued Recall, Recognition) show different consolidation benefits during the early consolidation window (Day 0->1) versus later decay period (Day 1->6). The analysis uses a piecewise Linear Mixed Model (LMM) approach to model forgetting trajectories across two temporal segments: Early consolidation (tests 0-1, approximately 0-24 hours) and Late decay (tests 3-6, approximately 24-168 hours).

**Pipeline:** LMM only (NO IRT - uses DERIVED theta scores from RQ 5.3.1)
**Steps:** 7 total analysis steps (Step 0: dependency loading, Steps 1-6: analysis and visualization preparation)
**Estimated Runtime:** Medium (~30-45 minutes total)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni correction for 6 planned contrasts at alpha=0.0083)
- Decision D069: Dual-scale trajectory plots (theta scale + probability scale for interpretability)
- Decision D070: TSVR as time variable (actual hours since encoding, not nominal days)

**Data Source:**
This RQ uses DERIVED data from RQ 5.3.1 (Paradigm-Specific Trajectories). RQ 5.3.1 must complete Steps 1-4 before this RQ can execute. This RQ adds temporal segmentation analysis (piecewise modeling) to examine consolidation effects.

---

## Analysis Plan

This RQ requires 7 steps:

### Step 0: Load Theta Scores from RQ 5.3.1

**Dependencies:** None (first step, but requires RQ 5.3.1 completion)
**Complexity:** Low (data loading and validation only, <5 minutes)

**Purpose:** Load paradigm-specific theta scores from RQ 5.3.1 and verify data structure for piecewise LMM analysis.

**Input:**

**File:** results/ch5/5.3.1/data/step04_lmm_input.csv (DERIVED from RQ 5.3.1)
**Format:** CSV, long format (one row per participant-test-paradigm observation)
**Required Columns:**
- `UID` (string, participant identifier, format: P### with leading zeros)
- `test` (string, test session: T1, T2, T3, T4 for Days 0, 1, 3, 6)
- `paradigm` (string, retrieval paradigm: IFR, ICR, IRE)
- `theta` (float, IRT ability estimate from RQ 5.3.1)
- `SE` (float, standard error of theta estimate)
- `TSVR_hours` (float, time since VR encoding in hours per Decision D070)
**Expected Rows:** 1200 (100 participants x 4 tests x 3 paradigms)

**Processing:**
- Read CSV file from RQ 5.3.1 output directory
- Verify all required columns present (case-sensitive check)
- Verify expected row count (1200 rows)
- Verify paradigm levels (IFR, ICR, IRE - exactly 3 levels)
- Verify test levels (T1, T2, T3, T4 - exactly 4 levels)
- Verify no missing theta values (NaN check)
- Verify TSVR_hours present and non-missing (Decision D070 requirement)

**Output:**

**File:** data/step00_theta_from_rq531.csv
**Format:** CSV, long format (copy of input with validation metadata added)
**Columns:** Same as input + `loaded_timestamp` (datetime when file was loaded)
**Expected Rows:** 1200 (no filtering at this step)

**Validation Requirement:**
Validation tools MUST be used after data loading tool execution. Specific validation tools will be determined by rq_tools based on cross-RQ dependency validation requirements (file exists, structure matches, no data corruption). The rq_analysis agent will embed validation tool calls after the data loading tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_theta_from_rq531.csv exists (exact path)
- Expected rows: 1200 (100 participants x 4 tests x 3 paradigms)
- Expected columns: 7 (UID, test, paradigm, theta, SE, TSVR_hours, loaded_timestamp)
- Data types: UID (object), test (object), paradigm (object), theta (float64), SE (float64), TSVR_hours (float64), loaded_timestamp (object)

*Value Ranges:*
- theta in [-3, 3] (typical IRT ability range)
- SE in [0.1, 1.0] (above 1.0 = unreliable, below 0.1 = suspicious)
- TSVR_hours in [0, 168] (0 = encoding, 168 = 1 week)
- paradigm in {IFR, ICR, IRE} (categorical, exactly 3 levels)
- test in {T1, T2, T3, T4} (categorical, exactly 4 levels)

*Data Quality:*
- No NaN values in theta column (all ability estimates required)
- No NaN values in TSVR_hours column (time variable required)
- Expected N: Exactly 1200 rows (no data loss from RQ 5.3.1)
- No duplicate rows (UID x test x paradigm combinations unique)
- Balanced design: 400 rows per paradigm (100 participants x 4 tests)

*Log Validation:*
- Required pattern: "Data loaded successfully: 1200 rows"
- Required pattern: "Paradigms present: IFR, ICR, IRE"
- Required pattern: "Tests present: T1, T2, T3, T4"
- Forbidden patterns: "ERROR", "File not found", "Missing required column"
- Acceptable warnings: None expected for data loading

**Expected Behavior on Validation Failure:**
- If file missing: Raise error "RQ 5.3.1 dependency not met - file not found at results/ch5/5.3.1/data/step04_lmm_input.csv"
- If row count != 1200: Raise error "Expected 1200 rows, found {actual} rows"
- If paradigm levels != 3: Raise error "Expected 3 paradigms (IFR, ICR, IRE), found {actual}"
- Log failure to logs/step00_load_theta_from_rq531.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked by master to diagnose dependency issue

---

### Step 1: Assign Temporal Segments and Compute Days_within

**Dependencies:** Step 0 (requires theta scores loaded from RQ 5.3.1)
**Complexity:** Low (data transformation only, <5 minutes)

**Purpose:** Create piecewise data structure by assigning temporal segments (Early vs Late) and computing Days_within (time recentered within each segment to start at 0).

**Input:**

**File:** data/step00_theta_from_rq531.csv
**Source:** Generated by Step 0
**Format:** CSV, long format
**Columns:** UID, test, paradigm, theta, SE, TSVR_hours, loaded_timestamp
**Expected Rows:** 1200

**Processing:**
- Assign Segment variable based on test session:
  - Early segment: T1, T2 (tests 0-1, approximately 0-24 hours post-encoding)
  - Late segment: T3, T4 (tests 3-6, approximately 24-168 hours post-encoding)
- Compute Days_within for each segment:
  - Early segment: Days_within = (TSVR_hours - min(TSVR_hours for T1, T2)) / 24 (rescale to days, start at 0)
  - Late segment: Days_within = (TSVR_hours - min(TSVR_hours for T3, T4)) / 24 (rescale to days, start at 0)
- Verify Days_within starts at 0 within each segment
- Retain all original columns for downstream analysis

**Output:**

**File:** data/step01_piecewise_lmm_input.csv
**Format:** CSV, long format
**Columns:**
- All columns from Step 0 (UID, test, paradigm, theta, SE, TSVR_hours)
- `Segment` (string, categorical: Early, Late)
- `Days_within` (float, time recentered within segment, starts at 0)
**Expected Rows:** 1200 (no filtering)

**Validation Requirement:**
Validation tools MUST be used after segment assignment tool execution. Specific validation tools will be determined by rq_tools based on piecewise data structure requirements (Segment variable created correctly, Days_within computed correctly, no negative values). The rq_analysis agent will embed validation tool calls after the segment assignment tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_piecewise_lmm_input.csv exists (exact path)
- Expected rows: 1200 (no filtering)
- Expected columns: 8 (UID, test, paradigm, theta, SE, TSVR_hours, Segment, Days_within)
- Data types: Segment (object), Days_within (float64), others as in Step 0

*Value Ranges:*
- Segment in {Early, Late} (categorical, exactly 2 levels)
- Days_within in [0, max_days] where max_days approximately 0.04-1.0 for Early, 0.5-5.0 for Late (depends on actual TSVR variation)
- Days_within >= 0 for all rows (no negative values, starts at 0 within each segment)
- theta, SE, TSVR_hours same ranges as Step 0

*Data Quality:*
- No NaN values in Segment column (all rows assigned to segment)
- No NaN values in Days_within column (all rows have recentered time)
- Expected N: Exactly 1200 rows
- Balanced design: 600 rows per segment (100 participants x 2 tests x 3 paradigms per segment)
- Days_within minimum = 0 within each segment (verify recentering worked)

*Log Validation:*
- Required pattern: "Segment assignment complete: 600 Early, 600 Late"
- Required pattern: "Days_within computed: min=0.0 for both segments"
- Forbidden patterns: "ERROR", "Negative Days_within", "Missing Segment assignment"
- Acceptable warnings: "TSVR variation detected within test sessions" (expected due to individual scheduling)

**Expected Behavior on Validation Failure:**
- If Segment levels != 2: Raise error "Expected 2 segments (Early, Late), found {actual}"
- If Days_within < 0: Raise error "Negative Days_within detected (recentering failed)"
- If segment counts unbalanced: Raise warning "Segment counts unbalanced: Early={n1}, Late={n2} (expected 600 each)"
- Log failure to logs/step01_assign_piecewise_segments.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose transformation logic

---

### Step 2: Fit Piecewise LMM

**Dependencies:** Step 1 (requires piecewise data structure with Segment and Days_within)
**Complexity:** Medium (model fitting, 10-20 minutes depending on convergence)

**Purpose:** Fit piecewise Linear Mixed Model with 3-way interaction (Days_within x Segment x paradigm) to test whether consolidation benefits differ across retrieval paradigms.

**Input:**

**File:** data/step01_piecewise_lmm_input.csv
**Source:** Generated by Step 1
**Format:** CSV, long format
**Columns:** UID, test, paradigm, theta, SE, TSVR_hours, Segment, Days_within
**Expected Rows:** 1200

**Processing:**
- Fit LMM using statsmodels MixedLM
- Formula: `theta ~ Days_within * Segment * paradigm + (1 + Days_within | UID)`
- Fixed effects:
  - Main effects: Days_within, Segment, paradigm
  - 2-way interactions: Days_within:Segment, Days_within:paradigm, Segment:paradigm
  - 3-way interaction: Days_within:Segment:paradigm
- Random effects:
  - Random intercept by UID (participant-specific baseline)
  - Random slope for Days_within by UID (participant-specific forgetting rate)
- Estimation: REML=False (for AIC-based model comparison if needed)
- Convergence tolerance: default (maxiter=100)
- Optimizer: default (scipy.optimize)
- Save fitted model object as pickle for downstream analysis
- Save model summary as text for inspection

**Output:**

**File 1:** data/step02_piecewise_lmm_model.pkl
**Format:** Pickle (serialized statsmodels MixedLMResults object)
**Purpose:** Fitted model for downstream analysis (slope extraction, contrasts)

**File 2:** data/step02_lmm_model_summary.txt
**Format:** Text file
**Content:**
- Model formula
- Fixed effects table (coefficient, SE, z, p, CI)
- Random effects variance components
- Model fit indices (AIC, BIC, log-likelihood)
- Convergence status
- Number of observations, groups

**Validation Requirement:**
Validation tools MUST be used after LMM fitting tool execution. Specific validation tools will be determined by rq_tools based on LMM convergence and assumption checks (convergence achieved, residuals normal, homoscedasticity, no autocorrelation, random effects normally distributed). The rq_analysis agent will embed validation tool calls after the LMM fitting tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_piecewise_lmm_model.pkl exists (exact path)
- data/step02_lmm_model_summary.txt exists (exact path)
- Model summary file > 1 KB (contains full summary output)

*Value Ranges:*
- Fixed effect coefficients typically in [-2, 2] for standardized predictors (extreme values >5 suggest estimation issues)
- Standard errors > 0 (SE = 0 indicates non-estimability)
- p-values in [0, 1]
- Random effect variance components > 0 (negative variance impossible, 0 indicates convergence failure)

*Data Quality:*
- Model converged: True (check convergence flag in model object)
- No NaN in fixed effects table (all effects estimable)
- No NaN in random effects variance components
- Expected fixed effects: 8 terms (3 main effects + 3 two-way interactions + 1 three-way interaction + intercept)
- Expected random effects: 2 variance components (intercept, Days_within slope) + 1 covariance

*Log Validation:*
- Required pattern: "Model converged: True"
- Required pattern: "VALIDATION - PASS: LMM convergence"
- Required pattern: "VALIDATION - PASS: Residuals normality"
- Required pattern: "VALIDATION - PASS: Homoscedasticity"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "Singular covariance matrix"
- Acceptable warnings: "Optimizer warning (gradient issues)" IF convergence still achieved

**Expected Behavior on Validation Failure:**
- If convergence failed: Invoke convergence contingency plan from 1_concept.md (try alternative optimizers, simplify random effects structure via LRT)
- If residuals non-normal (Shapiro-Wilk p < 0.01): Report robust standard errors via sandwich estimator
- If heteroscedasticity detected: Use weighted LMM or variance function by segment
- Log all validation results to logs/step02_fit_piecewise_lmm.log
- If critical failures (non-convergence, singular covariance): Quit and invoke g_debug
- If assumption violations (non-normality, heteroscedasticity): Proceed with remedial actions documented in log

---

### Step 3: Extract 6 Segment-Paradigm Slopes

**Dependencies:** Step 2 (requires fitted piecewise LMM model)
**Complexity:** Low (linear combination computation, <5 minutes)

**Purpose:** Extract 6 segment-paradigm-specific slopes (Early IFR, Early ICR, Early IRE, Late IFR, Late ICR, Late IRE) via linear combinations of fixed effects with delta method standard errors.

**Input:**

**File:** data/step02_piecewise_lmm_model.pkl
**Source:** Generated by Step 2
**Format:** Pickle (statsmodels MixedLMResults object)

**Processing:**
- Extract fixed effects coefficients and variance-covariance matrix from fitted model
- Compute 6 linear combinations representing segment-paradigm slopes:
  - Early IFR slope = beta(Days_within) + beta(Days_within:Segment[Early]) + beta(Days_within:paradigm[IFR]) + beta(Days_within:Segment[Early]:paradigm[IFR])
  - Early ICR slope = beta(Days_within) + beta(Days_within:Segment[Early]) + beta(Days_within:paradigm[ICR]) + beta(Days_within:Segment[Early]:paradigm[ICR])
  - Early IRE slope = beta(Days_within) + beta(Days_within:Segment[Early]) + beta(Days_within:paradigm[IRE]) + beta(Days_within:Segment[Early]:paradigm[IRE])
  - Late IFR slope = beta(Days_within) + beta(Days_within:Segment[Late]) + beta(Days_within:paradigm[IFR]) + beta(Days_within:Segment[Late]:paradigm[IFR])
  - Late ICR slope = beta(Days_within) + beta(Days_within:Segment[Late]) + beta(Days_within:paradigm[ICR]) + beta(Days_within:Segment[Late]:paradigm[ICR])
  - Late IRE slope = beta(Days_within) + beta(Days_within:Segment[Late]) + beta(Days_within:paradigm[IRE]) + beta(Days_within:Segment[Late]:paradigm[IRE])
- Compute delta method standard errors for each slope (propagate uncertainty from variance-covariance matrix)
- Compute z-statistics (slope / SE)
- Compute p-values (two-tailed z-test)
- Compute 95% confidence intervals (slope +/- 1.96 * SE)
- Add interpretation column (significant decline if p < 0.05 and slope < 0, significant improvement if p < 0.05 and slope > 0)

**Output:**

**File:** data/step03_segment_paradigm_slopes.csv
**Format:** CSV, one row per segment-paradigm combination
**Columns:**
- `Segment` (string, categorical: Early, Late)
- `paradigm` (string, categorical: IFR, ICR, IRE)
- `slope` (float, forgetting rate per day within segment)
- `SE` (float, delta method standard error)
- `z_statistic` (float, slope / SE)
- `p_value` (float, two-tailed test)
- `CI_lower` (float, 95% CI lower bound)
- `CI_upper` (float, 95% CI upper bound)
- `interpretation` (string, significance and direction)
**Expected Rows:** 6 (2 segments x 3 paradigms)

**Validation Requirement:**
Validation tools MUST be used after slope extraction tool execution. Specific validation tools will be determined by rq_tools based on statistical output validation (all slopes computed, no NaN, SE > 0, p-values in [0,1]). The rq_analysis agent will embed validation tool calls after the slope extraction tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_segment_paradigm_slopes.csv exists (exact path)
- Expected rows: 6 (2 segments x 3 paradigms)
- Expected columns: 9 (Segment, paradigm, slope, SE, z_statistic, p_value, CI_lower, CI_upper, interpretation)
- Data types: Segment (object), paradigm (object), slope (float64), SE (float64), z_statistic (float64), p_value (float64), CI_lower (float64), CI_upper (float64), interpretation (object)

*Value Ranges:*
- slope typically in [-1, 0] for forgetting (positive slope = improvement, unusual for episodic memory decay)
- SE in [0.01, 0.5] (above 0.5 = very imprecise, below 0.01 = suspiciously precise)
- z_statistic typically in [-10, 0] (negative for forgetting, magnitude > 10 suggests very strong effect)
- p_value in [0, 1]
- CI_lower < CI_upper for all rows
- Segment in {Early, Late}
- paradigm in {IFR, ICR, IRE}

*Data Quality:*
- No NaN values in any column (all slopes estimable)
- Expected N: Exactly 6 rows (no missing segment-paradigm combinations)
- No duplicate rows (Segment x paradigm combinations unique)
- SE > 0 for all rows (0 indicates delta method failure)
- Complete factorial design: 2 segments x 3 paradigms = 6 rows

*Log Validation:*
- Required pattern: "Slope extraction complete: 6 segment-paradigm slopes computed"
- Required pattern: "Delta method SEs propagated successfully"
- Forbidden patterns: "ERROR", "NaN slope detected", "Delta method failed"
- Acceptable warnings: None expected for slope extraction

**Expected Behavior on Validation Failure:**
- If row count != 6: Raise error "Expected 6 slopes (2 segments x 3 paradigms), found {actual}"
- If NaN in slope column: Raise error "NaN slope detected for Segment={seg}, paradigm={par} (linear combination failed)"
- If SE = 0: Raise error "SE = 0 for Segment={seg}, paradigm={par} (delta method failed)"
- Log failure to logs/step03_extract_segment_slopes.log
- Quit script immediately (do NOT proceed to Step 4)
- g_debug invoked to diagnose linear combination or delta method issue

---

### Step 4: Compute 6 Planned Contrasts with Bonferroni Correction

**Dependencies:** Step 3 (requires segment-paradigm slopes)
**Complexity:** Low (contrast computation, <5 minutes)

**Purpose:** Test 6 planned contrasts comparing consolidation benefits (Late slope - Early slope) across paradigms with Bonferroni correction (alpha = 0.0083) and dual p-value reporting per Decision D068.

**Input:**

**File 1:** data/step03_segment_paradigm_slopes.csv
**Source:** Generated by Step 3
**Format:** CSV, 6 rows (2 segments x 3 paradigms)

**File 2:** data/step02_piecewise_lmm_model.pkl
**Source:** Generated by Step 2
**Format:** Pickle (statsmodels MixedLMResults object)
**Purpose:** Needed for variance-covariance matrix to compute contrast SEs

**Processing:**
- Define 6 planned contrasts:
  1. IFR consolidation benefit: Late IFR slope - Early IFR slope (tests if IFR forgetting differs between segments)
  2. ICR consolidation benefit: Late ICR slope - Early ICR slope (tests if ICR forgetting differs between segments)
  3. IRE consolidation benefit: Late IRE slope - Early IRE slope (tests if IRE forgetting differs between segments)
  4. IFR vs ICR benefit difference: (Late IFR - Early IFR) - (Late ICR - Early ICR) (tests if consolidation benefit differs between paradigms)
  5. IFR vs IRE benefit difference: (Late IFR - Early IFR) - (Late IRE - Early IRE)
  6. ICR vs IRE benefit difference: (Late ICR - Early ICR) - (Late IRE - Early IRE)
- Compute contrast estimates (linear combinations of slopes)
- Compute delta method standard errors (propagate uncertainty from variance-covariance matrix)
- Compute z-statistics (contrast / SE)
- Compute UNCORRECTED p-values (two-tailed z-test)
- Compute BONFERRONI-CORRECTED p-values (uncorrected p * 6, capped at 1.0)
- Bonferroni alpha = 0.0083 (0.05 / 6 comparisons)
- Compute 95% confidence intervals (contrast +/- 1.96 * SE)
- Compute effect sizes (Cohen's d or f^2 depending on contrast type)
- Add significance column (significant if Bonferroni p < 0.0083)

**Output:**

**File 1:** data/step04_planned_contrasts.csv
**Format:** CSV, one row per contrast
**Columns:**
- `contrast_name` (string, descriptive label for contrast)
- `estimate` (float, contrast value)
- `SE` (float, delta method standard error)
- `z_statistic` (float, estimate / SE)
- `p_uncorrected` (float, two-tailed uncorrected p-value per Decision D068)
- `p_bonferroni` (float, Bonferroni-corrected p-value per Decision D068)
- `alpha_bonferroni` (float, always 0.0083 for this RQ)
- `significant` (bool, True if p_bonferroni < 0.0083)
- `CI_lower` (float, 95% CI lower bound)
- `CI_upper` (float, 95% CI upper bound)
**Expected Rows:** 6 (6 planned contrasts)

**File 2:** data/step04_effect_sizes.csv
**Format:** CSV, one row per contrast
**Columns:**
- `contrast_name` (string, matches contrast_name in contrasts CSV)
- `effect_size` (float, Cohen's d or f^2)
- `effect_type` (string, "cohens_d" or "f_squared")
- `interpretation` (string, small/medium/large based on Cohen's thresholds)
**Expected Rows:** 6 (6 planned contrasts)

**Validation Requirement:**
Validation tools MUST be used after contrast computation tool execution. Specific validation tools will be determined by rq_tools based on Decision D068 dual p-value requirements (uncorrected AND Bonferroni p-values present, alpha correct, effect sizes computed). The rq_analysis agent will embed validation tool calls after the contrast computation tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_planned_contrasts.csv exists (exact path)
- data/step04_effect_sizes.csv exists (exact path)
- Expected rows: 6 in both files (6 planned contrasts)
- Expected columns: 10 in contrasts CSV, 4 in effect sizes CSV
- Data types: contrast_name (object), estimate (float64), SE (float64), z_statistic (float64), p_uncorrected (float64), p_bonferroni (float64), alpha_bonferroni (float64), significant (bool), CI_lower (float64), CI_upper (float64)

*Value Ranges:*
- estimate typically in [-1, 1] for consolidation benefit contrasts (outside suggests extreme effect)
- SE in [0.01, 0.5] (above 0.5 = very imprecise)
- z_statistic typically in [-5, 5] (magnitude > 10 suggests very strong effect)
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1] (capped at 1.0 even if uncorrected * 6 > 1)
- alpha_bonferroni = 0.0083 for ALL rows (constant for this RQ)
- CI_lower < CI_upper for all rows
- effect_size typically in [0, 2] for Cohen's d (>2 = very large effect), [0, 1] for f^2

*Data Quality:*
- No NaN values in contrasts CSV (all contrasts estimable)
- No NaN values in effect sizes CSV (all effect sizes computable)
- Expected N: Exactly 6 rows in both files
- Dual p-values present: p_uncorrected AND p_bonferroni columns exist with non-NaN values (Decision D068 requirement)
- SE > 0 for all contrasts (0 indicates delta method failure)
- p_bonferroni >= p_uncorrected for all rows (Bonferroni correction cannot decrease p-value)

*Log Validation:*
- Required pattern: "VALIDATION - PASS: Dual p-values present (uncorrected + bonferroni)"
- Required pattern: "Bonferroni alpha = 0.0083 for 6 contrasts"
- Required pattern: "Effect sizes computed for all 6 contrasts"
- Forbidden patterns: "ERROR", "Missing p_uncorrected column", "Missing p_bonferroni column", "NaN contrast detected"
- Acceptable warnings: None expected for contrast computation

**Expected Behavior on Validation Failure:**
- If row count != 6: Raise error "Expected 6 contrasts, found {actual}"
- If p_uncorrected column missing: Raise error "Decision D068 violation: p_uncorrected column missing"
- If p_bonferroni column missing: Raise error "Decision D068 violation: p_bonferroni column missing"
- If NaN in estimate column: Raise error "NaN contrast for {contrast_name} (linear combination failed)"
- Log failure to logs/step04_compute_planned_contrasts.log
- Quit script immediately (do NOT proceed to Step 5)
- g_debug invoked to diagnose contrast computation or D068 compliance issue

---

### Step 5: Compute Consolidation Benefit Index

**Dependencies:** Step 3 (requires segment-paradigm slopes)
**Complexity:** Low (simple arithmetic, <5 minutes)

**Purpose:** Compute consolidation benefit index (Late slope - Early slope) for each paradigm, rank paradigms by benefit magnitude, and interpret pattern relative to hypothesis.

**Input:**

**File:** data/step03_segment_paradigm_slopes.csv
**Source:** Generated by Step 3
**Format:** CSV, 6 rows (2 segments x 3 paradigms)

**Processing:**
- For each paradigm (IFR, ICR, IRE):
  - Extract Early segment slope
  - Extract Late segment slope
  - Compute consolidation benefit = Late slope - Early slope
  - Interpretation: Positive benefit = consolidation effect (slower forgetting in Early vs Late), Negative benefit = consolidation detriment (faster forgetting in Early vs Late)
- Rank paradigms by consolidation benefit magnitude (largest to smallest)
- Interpret pattern relative to hypothesis:
  - Expected pattern: IFR > ICR > IRE (Free Recall shows greatest consolidation benefit due to deeper encoding)
  - Actual pattern: Compare observed ranking to expected
- Add interpretation column (matches hypothesis / contradicts hypothesis)

**Output:**

**File:** data/step05_consolidation_benefit.csv
**Format:** CSV, one row per paradigm
**Columns:**
- `paradigm` (string, categorical: IFR, ICR, IRE)
- `Early_slope` (float, forgetting rate during Early segment)
- `Late_slope` (float, forgetting rate during Late segment)
- `consolidation_benefit` (float, Late slope - Early slope)
- `rank` (int, 1 = largest benefit, 3 = smallest benefit)
- `interpretation` (string, matches/contradicts hypothesis based on ranking)
**Expected Rows:** 3 (3 paradigms)

**Validation Requirement:**
Validation tools MUST be used after consolidation benefit computation tool execution. Specific validation tools will be determined by rq_tools based on output format validation (all paradigms present, ranks 1-3 assigned, benefit computed correctly). The rq_analysis agent will embed validation tool calls after the consolidation benefit computation tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_consolidation_benefit.csv exists (exact path)
- Expected rows: 3 (3 paradigms: IFR, ICR, IRE)
- Expected columns: 6 (paradigm, Early_slope, Late_slope, consolidation_benefit, rank, interpretation)
- Data types: paradigm (object), Early_slope (float64), Late_slope (float64), consolidation_benefit (float64), rank (int64), interpretation (object)

*Value Ranges:*
- Early_slope typically in [-1, 0] (forgetting rate)
- Late_slope typically in [-1, 0] (forgetting rate)
- consolidation_benefit typically in [-0.5, 0.5] (difference in forgetting rates)
- rank in {1, 2, 3} (exactly one paradigm per rank)
- paradigm in {IFR, ICR, IRE}

*Data Quality:*
- No NaN values in any column (all benefits computable)
- Expected N: Exactly 3 rows (all paradigms present)
- No duplicate paradigms
- Ranks 1, 2, 3 all assigned (no ties, no missing ranks)
- consolidation_benefit = Late_slope - Early_slope for all rows (verify arithmetic)

*Log Validation:*
- Required pattern: "Consolidation benefit computed for 3 paradigms"
- Required pattern: "Ranking: {rank_1_paradigm} > {rank_2_paradigm} > {rank_3_paradigm}"
- Required pattern: "Hypothesis comparison: {matches/contradicts} expected pattern (IFR > ICR > IRE)"
- Forbidden patterns: "ERROR", "NaN benefit detected", "Duplicate rank"
- Acceptable warnings: "Pattern contradicts hypothesis" (data-driven finding, not an error)

**Expected Behavior on Validation Failure:**
- If row count != 3: Raise error "Expected 3 paradigms, found {actual}"
- If NaN in consolidation_benefit: Raise error "NaN benefit for paradigm={par} (arithmetic failed)"
- If ranks not {1, 2, 3}: Raise error "Ranks incomplete: found {actual_ranks} (expected [1, 2, 3])"
- Log failure to logs/step05_compute_consolidation_benefit.log
- Quit script immediately (do NOT proceed to Step 6)
- g_debug invoked to diagnose arithmetic or ranking logic

---

### Step 6: Prepare Piecewise Plot Data

**Dependencies:** Steps 1, 2, 3 (requires piecewise data, fitted model, segment slopes)
**Complexity:** Low (data aggregation, <5 minutes)

**Purpose:** Aggregate observed means and model predictions per paradigm x segment x timepoint for two-panel piecewise trajectory visualization (Early segment vs Late segment) with dual-scale plots (theta + probability scales per Decision D069).

**Plot Description:** Two-panel piecewise trajectory plot with confidence bands showing forgetting rates across paradigms during Early consolidation window vs Late decay period. Left panel: Early segment (tests 0-1), Right panel: Late segment (tests 3-6). Each panel shows 3 paradigm trajectories (IFR, ICR, IRE) with observed means and model-predicted lines.

**Required Data Sources:**
- data/step01_piecewise_lmm_input.csv (columns: UID, test, paradigm, theta, SE, TSVR_hours, Segment, Days_within)
- data/step02_piecewise_lmm_model.pkl (fitted model for predictions)
- data/step03_segment_paradigm_slopes.csv (slopes for annotating plot)

**Aggregation Logic:**
1. Group by Segment + paradigm + test, compute mean(theta), 95% CI
2. Generate model predictions using fitted LMM across Days_within range per segment
3. Merge observed means with model predictions
4. Convert theta to probability scale using IRT transformation (Decision D069 dual-scale requirement)
5. Create two separate CSVs: theta scale + probability scale
6. Include slope annotations for each segment-paradigm line

**Output (Plot Source CSVs):**

**File 1:** data/step06_piecewise_theta_data.csv
**Format:** CSV, plot source data for theta-scale piecewise trajectory
**Columns:**
- `Segment` (string, categorical: Early, Late)
- `paradigm` (string, categorical: IFR, ICR, IRE)
- `Days_within` (float, time within segment for predictions)
- `test` (string, test session for observed data: T1, T2, T3, T4)
- `theta_observed` (float, observed mean theta per segment x paradigm x test)
- `theta_predicted` (float, model-predicted theta)
- `CI_lower` (float, 95% CI lower bound for observed mean)
- `CI_upper` (float, 95% CI upper bound for observed mean)
- `slope` (float, segment-paradigm slope from Step 3)
**Expected Rows:** Approximately 48 (2 segments x 3 paradigms x 8 timepoints for predictions) + 24 observed points (2 segments x 3 paradigms x 4 tests total, but 2 tests per segment)

**File 2:** data/step06_piecewise_probability_data.csv
**Format:** CSV, plot source data for probability-scale piecewise trajectory (Decision D069 dual-scale)
**Columns:** Same as theta_data but with probability values (theta converted to [0,1] scale via IRT transformation)
- `Segment`, `paradigm`, `Days_within`, `test` (same as theta_data)
- `prob_observed` (float, observed mean converted to probability)
- `prob_predicted` (float, model prediction converted to probability)
- `CI_lower` (float, CI lower bound converted to probability)
- `CI_upper` (float, CI upper bound converted to probability)
- `slope` (float, same as theta_data for reference)
**Expected Rows:** Same as theta_data (approximately 48 + 24)

**Validation Requirement:**
Validation tools MUST be used after plot data preparation tool execution. Specific validation tools will be determined by rq_tools based on plot data format requirements (all segments present, all paradigms present, observed + predicted data aligned, dual-scale files created per D069). The rq_analysis agent will embed validation tool calls after the plot data preparation tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_piecewise_theta_data.csv exists (exact path)
- data/step06_piecewise_probability_data.csv exists (exact path)
- Expected rows: Approximately 72 total per file (48 prediction points + 24 observed points)
- Expected columns: 9 in theta_data, 9 in probability_data
- Data types: Segment (object), paradigm (object), Days_within (float64), test (object), theta_observed (float64), theta_predicted (float64), CI_lower (float64), CI_upper (float64), slope (float64)

*Value Ranges:*
- Days_within in [0, max_days] where max varies by segment (Early: 0-1 day, Late: 0-5 days)
- theta_observed in [-3, 3] (typical IRT ability range)
- theta_predicted in [-3, 3]
- CI_lower in [-3, 3], CI_upper in [-3, 3]
- CI_lower < CI_upper for all observed points
- prob_observed in [0, 1] (probability scale per D069)
- prob_predicted in [0, 1]
- Segment in {Early, Late}
- paradigm in {IFR, ICR, IRE}

*Data Quality:*
- No NaN in theta_predicted column (all predictions generated)
- NaN acceptable in theta_observed for prediction-only rows (not all Days_within values have observed data)
- Expected N: Complete factorial design for observed data (2 segments x 3 paradigms x 2 tests per segment = 12 observed points)
- All segment-paradigm combinations present (6 combinations: Early x IFR, Early x ICR, Early x IRE, Late x IFR, Late x ICR, Late x IRE)
- Dual-scale files both present (Decision D069 requirement)
- Probability data matches theta data structure (same Segment, paradigm, Days_within values)

*Log Validation:*
- Required pattern: "Plot data preparation complete: theta scale + probability scale"
- Required pattern: "Observed data: 12 segment-paradigm-test combinations"
- Required pattern: "Predicted data: 48 timepoints across 6 segment-paradigm combinations"
- Required pattern: "VALIDATION - PASS: Dual-scale plot data created (Decision D069)"
- Forbidden patterns: "ERROR", "Missing segment", "Missing paradigm", "NaN in predictions"
- Acceptable warnings: "NaN in observed data for prediction-only rows" (expected)

**Expected Behavior on Validation Failure:**
- If theta_data file missing: Raise error "Theta-scale plot data not created"
- If probability_data file missing: Raise error "Decision D069 violation: probability-scale plot data not created"
- If segment-paradigm combinations incomplete: Raise error "Expected 6 combinations (2 segments x 3 paradigms), found {actual}"
- If NaN in predictions: Raise error "Model predictions contain NaN (prediction failed)"
- Log failure to logs/step06_prepare_piecewise_plot_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- g_debug invoked to diagnose aggregation or prediction logic

**Plotting Function (rq_plots will call):** Two-panel piecewise trajectory plot with confidence bands
- rq_plots agent maps this description to specific tools/plots.py function (likely plot_trajectory or custom piecewise variant)
- Plot reads data/step06_piecewise_theta_data.csv and data/step06_piecewise_probability_data.csv (created by this step)
- NO data aggregation in rq_plots (visualization only per Option B architecture)
- PNG output saved to plots/ folder by rq_plots

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs - intermediate and final)

- data/step00_theta_from_rq531.csv (from Step 0: dependency loading, 1200 rows)
- data/step01_piecewise_lmm_input.csv (from Step 1: segment assignment, 1200 rows)
- data/step02_piecewise_lmm_model.pkl (from Step 2: fitted LMM model)
- data/step02_lmm_model_summary.txt (from Step 2: model summary text)
- data/step03_segment_paradigm_slopes.csv (from Step 3: 6 slopes)
- data/step04_planned_contrasts.csv (from Step 4: 6 contrasts with dual p-values)
- data/step04_effect_sizes.csv (from Step 4: effect sizes for contrasts)
- data/step05_consolidation_benefit.csv (from Step 5: 3 paradigm benefits ranked)
- data/step06_piecewise_theta_data.csv (from Step 6: theta-scale plot source)
- data/step06_piecewise_probability_data.csv (from Step 6: probability-scale plot source)

### Logs (ONLY execution logs - .log files capturing stdout/stderr)

- logs/step00_load_theta_from_rq531.log
- logs/step01_assign_piecewise_segments.log
- logs/step02_fit_piecewise_lmm.log
- logs/step03_extract_segment_slopes.log
- logs/step04_compute_planned_contrasts.log
- logs/step05_compute_consolidation_benefit.log
- logs/step06_prepare_piecewise_plot_data.log

### Plots (EMPTY until rq_plots runs)

- plots/piecewise_theta_scale.png (created by rq_plots, NOT analysis steps)
- plots/piecewise_probability_scale.png (created by rq_plots)

### Results (EMPTY until rq_results runs)

- results/summary.md (created by rq_results, NOT analysis steps)

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 -> Step 1:** Load theta scores (1200 rows, long format) -> Assign segments (1200 rows, add Segment + Days_within columns)

**Step 1 -> Step 2:** Piecewise LMM input (1200 rows) -> Fitted model (pkl) + summary (txt)

**Step 2 -> Step 3:** Fitted model -> 6 segment-paradigm slopes (6 rows, extracted via linear combinations)

**Step 3 -> Step 4:** 6 slopes -> 6 contrasts + effect sizes (6 rows each, contrast differences)

**Step 3 -> Step 5:** 6 slopes -> 3 consolidation benefits (3 rows, ranked paradigms)

**Steps 1, 2, 3 -> Step 6:** Piecewise input + model + slopes -> Plot data (theta + probability scales, ~72 rows each)

### Column Naming Conventions

**Per names.md:**
- `UID`: Participant unique identifier (format: P### with leading zeros)
- `test`: Test session identifier (T1, T2, T3, T4 for Days 0, 1, 3, 6)
- `paradigm`: Retrieval paradigm (IFR, ICR, IRE)
- `theta`: IRT ability estimate (lowercase)
- `SE`: Standard error of theta
- `TSVR_hours`: Time Since VR in hours (Decision D070)
- `Segment`: Temporal segment (Early, Late)
- `Days_within`: Time recentered within segment (starts at 0)
- `CI_lower`, `CI_upper`: 95% confidence interval bounds

### Data Type Constraints

**Categorical Variables:**
- `UID`: string (object)
- `test`: string (object), levels = {T1, T2, T3, T4}
- `paradigm`: string (object), levels = {IFR, ICR, IRE}
- `Segment`: string (object), levels = {Early, Late}

**Numeric Variables:**
- `theta`: float64, range [-3, 3]
- `SE`: float64, range [0.1, 1.0]
- `TSVR_hours`: float64, range [0, 168]
- `Days_within`: float64, range [0, max_days]
- `slope`: float64, typically [-1, 0]
- `p_value`: float64, range [0, 1]

**Boolean Variables:**
- `significant`: bool (True/False)

**Null Handling:**
- No NaN allowed in: theta, SE, TSVR_hours, Segment, Days_within, paradigm, UID, test
- NaN acceptable in: theta_observed for prediction-only rows in plot data

---

## Cross-RQ Dependencies

### Dependency Type: DERIVED Data from Other RQs (Dependencies Exist)

**This RQ requires outputs from:**
- **RQ 5.3.1** (Paradigm-Specific Trajectories)
  - File: results/ch5/5.3.1/data/step04_lmm_input.csv
  - Used in: Step 0 (load paradigm-specific theta scores as starting point)
  - Rationale: RQ 5.3.1 calibrates IRT models for 3 paradigms (IFR, ICR, IRE), extracts theta scores, and reshapes to long format (1200 rows: 100 participants x 4 tests x 3 paradigms). This RQ uses those theta scores and adds temporal segmentation analysis (piecewise modeling) to examine consolidation effects.

**Execution Order Constraint:**
1. RQ 5.3.1 must complete Steps 1-4 (IRT calibration, theta extraction, TSVR merge, reshape to long)
2. This RQ executes after RQ 5.3.1 completion (uses theta scores as input)

**Data Source Boundaries:**
- **RAW data:** None (this RQ does not access master.xlsx directly)
- **DERIVED data:** results/ch5/5.3.1/data/step04_lmm_input.csv (theta scores from RQ 5.3.1)
- **Scope:** This RQ does NOT re-calibrate IRT models (reuses theta scores from RQ 5.3.1)

**Validation:**
- Step 0: Check results/ch5/5.3.1/data/step04_lmm_input.csv exists (circuit breaker: FILE_MISSING if absent)
- Step 0: Verify file structure (1200 rows, required columns present)
- If file missing -> quit with error "RQ 5.3.1 dependency not met - file not found"
- User must execute RQ 5.3.1 first before running this RQ

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
- g_code (Step 14 workflow) will generate stepNN_name.py scripts with validation function calls
- bash execution (Step 14 workflow) will run analysis -> validation -> error on validation failure

**Downstream Agent Requirements:**
- **rq_tools:** MUST specify validation tool for EVERY analysis step (no exceptions)
- **rq_analysis:** MUST embed validation tool call for EVERY analysis step (no exceptions)
- **g_code:** MUST generate code with validation function calls (no exceptions)
- **rq_inspect:** MUST verify validation ran successfully (checks logs/stepNN_name.log for validation output)

### Validation Requirements By Step

**Step 0: Load Theta Scores from RQ 5.3.1**
- **Analysis Tool:** (determined by rq_tools - likely pandas.read_csv with validation wrapper)
- **Validation Tool:** (determined by rq_tools - likely validate_dataframe_structure + validate_data_columns)
- **What Validation Checks:** File exists, structure matches (1200 rows x 7 columns), required columns present, no NaN in theta/TSVR_hours, paradigm levels = {IFR, ICR, IRE}, test levels = {T1, T2, T3, T4}
- **Expected Behavior on Failure:** Quit with cross-RQ dependency error, invoke g_debug

**Step 1: Assign Temporal Segments**
- **Analysis Tool:** (determined by rq_tools - likely assign_piecewise_segments from tools_catalog.md)
- **Validation Tool:** (determined by rq_tools - likely validate_dataframe_structure + custom segment validation)
- **What Validation Checks:** Segment variable created (2 levels: Early, Late), Days_within computed (>= 0 within each segment), balanced design (600 rows per segment), no NaN
- **Expected Behavior on Failure:** Quit with transformation error, invoke g_debug

**Step 2: Fit Piecewise LMM**
- **Analysis Tool:** (determined by rq_tools - likely statsmodels.MixedLM or custom wrapper)
- **Validation Tool:** (determined by rq_tools - likely validate_lmm_assumptions_comprehensive from tools_catalog.md)
- **What Validation Checks:** Convergence (True), residuals normality (Shapiro-Wilk p > 0.01 or report robust SEs), homoscedasticity (Levene's test), random effects normality, no autocorrelation, no singular covariance
- **Expected Behavior on Failure:** If convergence failed, invoke contingency plan (alternative optimizers, simplify random structure via LRT per 1_concept.md); if assumptions violated, apply remedial actions (robust SEs, weighted LMM); log all diagnostics

**Step 3: Extract 6 Segment-Paradigm Slopes**
- **Analysis Tool:** (determined by rq_tools - likely extract_segment_slopes_from_lmm from tools_catalog.md)
- **Validation Tool:** (determined by rq_tools - likely validate_dataframe_structure + validate_numeric_range)
- **What Validation Checks:** 6 rows created (2 segments x 3 paradigms), all slopes computed (no NaN), SE > 0 (delta method successful), p-values in [0,1], CI_lower < CI_upper
- **Expected Behavior on Failure:** Quit with linear combination error, invoke g_debug

**Step 4: Compute 6 Planned Contrasts**
- **Analysis Tool:** (determined by rq_tools - likely compute_contrasts_pairwise from tools_catalog.md with custom contrast definitions)
- **Validation Tool:** (determined by rq_tools - likely validate_contrasts_dual_pvalues from tools_catalog.md for D068 compliance)
- **What Validation Checks:** 6 contrasts computed, BOTH p_uncorrected AND p_bonferroni columns present (D068 requirement), alpha_bonferroni = 0.0083, effect sizes computed, no NaN
- **Expected Behavior on Failure:** If dual p-values missing, quit with D068 violation error; if NaN contrasts, quit with computation error; invoke g_debug

**Step 5: Compute Consolidation Benefit Index**
- **Analysis Tool:** (determined by rq_tools - likely custom pandas arithmetic)
- **Validation Tool:** (determined by rq_tools - likely validate_dataframe_structure)
- **What Validation Checks:** 3 paradigms present, consolidation_benefit = Late_slope - Early_slope verified, ranks {1, 2, 3} assigned uniquely, no NaN
- **Expected Behavior on Failure:** Quit with arithmetic error, invoke g_debug

**Step 6: Prepare Piecewise Plot Data**
- **Analysis Tool:** (determined by rq_tools - likely prepare_piecewise_plot_data from tools_catalog.md)
- **Validation Tool:** (determined by rq_tools - likely validate_plot_data_completeness + validate_probability_range)
- **What Validation Checks:** BOTH theta_data AND probability_data CSVs created (D069 dual-scale requirement), all 6 segment-paradigm combinations present, no NaN in predictions, probability values in [0,1], CI_lower < CI_upper
- **Expected Behavior on Failure:** If probability_data missing, quit with D069 violation error; if NaN predictions, quit with model prediction error; invoke g_debug

---

## Summary

**Total Steps:** 7 (Step 0: dependency loading, Steps 1-6: analysis and visualization preparation)
**Estimated Runtime:** Medium (~30-45 minutes total: Step 0 <5 min, Step 1 <5 min, Step 2 10-20 min, Step 3 <5 min, Step 4 <5 min, Step 5 <5 min, Step 6 <5 min)
**Cross-RQ Dependencies:** RQ 5.3.1 (Paradigm-Specific Trajectories) MUST complete first
**Primary Outputs:**
- Piecewise LMM model (pkl + summary)
- 6 segment-paradigm slopes (Early/Late x IFR/ICR/IRE)
- 6 planned contrasts with dual p-values (D068 compliant)
- 3 consolidation benefit indices (ranked paradigms)
- Plot data (theta + probability scales, D069 dual-scale compliant)
**Validation Coverage:** 100% (all 7 steps have validation requirements)

**Key Architectural Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni-corrected p-values for all contrasts)
- Decision D069: Dual-scale trajectory plots (theta scale + probability scale for interpretability)
- Decision D070: TSVR as LMM time variable (actual hours since encoding, not nominal days)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-02): Initial plan created by rq_planner agent for RQ 5.3.3 (Paradigm Consolidation Window)
