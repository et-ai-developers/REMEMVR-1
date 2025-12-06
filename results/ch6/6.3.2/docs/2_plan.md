# Analysis Plan for RQ 6.3.2: Domain Confidence Calibration

**Created by:** rq_planner agent
**Date:** 2025-12-06
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This RQ examines whether confidence-accuracy calibration varies across episodic memory domains (What/Where/When). Calibration is computed as the difference between standardized confidence theta and standardized accuracy theta, with better calibration indicated by smaller absolute differences. The analysis uses DERIVED data from two upstream RQs: Ch5 5.2.1 (domain-stratified accuracy theta) and Ch6 6.3.1 (domain-stratified confidence theta).

**Pipeline:** LMM only (no IRT calibration - uses pre-computed theta from source RQs)

**Steps:** 5 total analysis steps (Step 0: data loading/merge + Steps 1-4: LMM analysis, post-hoc contrasts, ranking, plot preparation)

**Estimated Runtime:** Low (~5-10 minutes total - no IRT model fitting)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni) for Domain main effect and post-hoc contrasts
- Decision D070: TSVR as time variable (inherited from source RQs, used in LMM)

**Cross-RQ Dependencies:**
- Ch5 5.2.1: Domain-stratified accuracy trajectories (theta_accuracy by domain)
- Ch6 6.3.1: Domain-stratified confidence trajectories (theta_confidence by domain)

---

## Analysis Plan

### Step 0: Load and Merge Accuracy and Confidence Data

**Dependencies:** None (first step - but requires Ch5 5.2.1 and Ch6 6.3.1 complete)
**Complexity:** Low (<1 minute - data loading and merge only)

**Purpose:** Load domain-stratified accuracy theta from Ch5 5.2.1 and confidence theta from Ch6 6.3.1, merge by UID x TEST x Domain to create analysis dataset.

**Input:**

**File 1:** results/ch5/5.2.1/data/step03_theta_accuracy_domain.csv
**Source:** Ch5 5.2.1 (Domain-stratified IRT calibration, Pass 2 theta extraction)
**Format:** CSV with columns:
  - `UID` (string, format: P### with leading zeros, e.g., P001)
  - `TEST` (string, values: {T1, T2, T3, T4} for Days 0, 1, 3, 6)
  - `Domain` (string, values: {What, Where, When})
  - `theta_accuracy` (float, IRT ability estimate for accuracy, range typically -3 to +3)
  - `se_accuracy` (float, standard error, range typically 0.1 to 1.0)
**Expected Rows:** 1200 (100 participants x 4 tests x 3 domains)
**Note:** If When domain excluded in Ch5 5.2.1 due to purification issues (<10 items retained), file may have 800 rows (What/Where only). Circuit breaker if <800 rows.

**File 2:** results/ch6/6.3.1/data/step03_theta_confidence_domain.csv
**Source:** Ch6 6.3.1 (Domain-stratified confidence IRT calibration, Pass 2 theta extraction)
**Format:** CSV with columns:
  - `UID` (string, format: P### with leading zeros)
  - `TEST` (string, values: {T1, T2, T3, T4})
  - `Domain` (string, values: {What, Where, When})
  - `theta_confidence` (float, IRT ability estimate for confidence, range typically -3 to +3)
  - `se_confidence` (float, standard error, range typically 0.1 to 1.0)
**Expected Rows:** Should match File 1 row count (1200 or 800 depending on When domain availability)
**Note:** If When domain excluded in Ch6 6.3.1 but present in Ch5 5.2.1 (or vice versa), merge will reduce to intersection (likely What/Where only).

**Processing:**

1. **Load accuracy data:** Read results/ch5/5.2.1/data/step03_theta_accuracy_domain.csv
2. **Load confidence data:** Read results/ch6/6.3.1/data/step03_theta_confidence_domain.csv
3. **Check domain compatibility:** Verify both files have same Domain set (What/Where/When or subset)
4. **Merge datasets:** Inner join on (UID, TEST, Domain) - keeps only matching combinations
5. **Compute z-standardized theta:**
   - `theta_accuracy_z = (theta_accuracy - mean(theta_accuracy)) / sd(theta_accuracy)` (standardized across all observations)
   - `theta_confidence_z = (theta_confidence - mean(theta_confidence)) / sd(theta_confidence)` (standardized across all observations)
6. **Compute calibration:** `calibration = theta_confidence_z - theta_accuracy_z` per row
   - Positive calibration = overconfidence (confidence higher than accuracy)
   - Negative calibration = underconfidence (confidence lower than accuracy)
   - Calibration near zero = well-calibrated
7. **Compute absolute calibration:** `abs_calibration = |calibration|` (magnitude of miscalibration, domain ranking metric)
8. **Add TSVR_hours:** Load TSVR mapping from master.xlsx or Ch5 5.2.1 outputs, merge by UID x TEST
   - TSVR_hours values: T1=0 (encoding), T2~24 (Day 1), T3~72 (Day 3), T4~144 (Day 6)
   - Decision D070: Use actual hours, not nominal days

**Output:**

**File:** data/step00_calibration_by_domain.csv
**Format:** CSV, one row per participant-test-domain combination
**Columns:**
  - `UID` (string, participant identifier)
  - `TEST` (string, test session T1-T4)
  - `Domain` (string, What/Where/When)
  - `TSVR_hours` (float, time since VR encoding in hours)
  - `theta_accuracy` (float, raw accuracy theta from Ch5 5.2.1)
  - `se_accuracy` (float, accuracy SE)
  - `theta_confidence` (float, raw confidence theta from Ch6 6.3.1)
  - `se_confidence` (float, confidence SE)
  - `theta_accuracy_z` (float, z-standardized accuracy theta)
  - `theta_confidence_z` (float, z-standardized confidence theta)
  - `calibration` (float, theta_confidence_z - theta_accuracy_z, signed calibration)
  - `abs_calibration` (float, |calibration|, magnitude of miscalibration)
**Expected Rows:** 1200 (100 participants x 4 tests x 3 domains) OR 800 if When domain excluded from either source RQ
**Expected Nulls:** None (all columns non-null after merge - circuit breaker if any NaN detected)

**Validation Requirement:**

Validation tools MUST be used after data loading/merge execution. Specific validation tools will be determined by rq_tools based on data format requirements (likely validate_data_format, validate_numeric_range, check_missing_data).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_calibration_by_domain.csv exists (exact path)
- Expected rows: 1200 (ideal) OR 800 (acceptable if When domain excluded)
- Expected columns: 12 (UID, TEST, Domain, TSVR_hours, theta_accuracy, se_accuracy, theta_confidence, se_confidence, theta_accuracy_z, theta_confidence_z, calibration, abs_calibration)
- Data types: UID (string), TEST (string), Domain (string), all theta/SE/calibration (float64), TSVR_hours (float64)

*Value Ranges:*
- theta_accuracy in [-3, 3] (IRT ability scale from Ch5 5.2.1)
- theta_confidence in [-3, 3] (IRT ability scale from Ch6 6.3.1)
- se_accuracy in [0.1, 1.0] (above 1.0 = unreliable)
- se_confidence in [0.1, 1.0] (above 1.0 = unreliable)
- theta_accuracy_z: mean ~ 0, SD ~ 1 (z-standardized, tolerance +/- 0.1 for sampling variation)
- theta_confidence_z: mean ~ 0, SD ~ 1 (z-standardized, tolerance +/- 0.1)
- calibration: unrestricted range (signed difference), but |calibration| typically <3
- abs_calibration in [0, 3] (absolute difference, >3 suggests standardization error)
- TSVR_hours in [0, 168] (0=encoding, 168=1 week max)

*Data Quality:*
- No NaN values tolerated (merge must be complete)
- Expected N: 1200 rows (100 participants x 4 tests x 3 domains) OR 800 rows if When excluded
- If <800 rows: Circuit breaker (missing domain or participants)
- No duplicate rows (UID x TEST x Domain combinations unique)
- Domain values: {What, Where, When} OR {What, Where} subset acceptable
- TEST values: {T1, T2, T3, T4} complete for each UID x Domain
- Standardization check: mean(theta_accuracy_z) within [-0.1, 0.1], SD within [0.9, 1.1]
- Standardization check: mean(theta_confidence_z) within [-0.1, 0.1], SD within [0.9, 1.1]

*Log Validation:*
- Required pattern: "Loaded accuracy data: {N} rows from Ch5 5.2.1"
- Required pattern: "Loaded confidence data: {N} rows from Ch6 6.3.1"
- Required pattern: "Merge successful: {N} observations (UID x TEST x Domain)"
- Required pattern: "Z-standardization complete: theta_accuracy_z mean={M:.3f}, SD={S:.3f}"
- Required pattern: "Z-standardization complete: theta_confidence_z mean={M:.3f}, SD={S:.3f}"
- Required pattern: "Calibration computed: range [{min:.2f}, {max:.2f}]"
- Forbidden patterns: "ERROR", "KeyError", "Merge failed", "NaN values detected"
- Acceptable warnings: "When domain excluded from {source RQ}" (if applicable)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 1200 rows, found 750" or "NaN detected in calibration column")
- Log failure to logs/step00_load_merge_data.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause (likely: source RQ incomplete, domain mismatch, or TSVR merge failure)

---

### Step 1: Fit LMM with Domain x Time Interaction

**Dependencies:** Step 0 (requires step00_calibration_by_domain.csv)
**Complexity:** Low (~2-3 minutes - single LMM fit, no model comparison)

**Purpose:** Fit Linear Mixed Model to test whether calibration varies by Domain (main effect) and whether domain differences change over time (Domain x Time interaction).

**Input:**

**File:** data/step00_calibration_by_domain.csv
**Source:** Generated by Step 0
**Format:** Long format (one row per UID x TEST x Domain observation)
**Required Columns:** UID, TEST, Domain, TSVR_hours, calibration, abs_calibration
**Expected Rows:** 1200 (or 800 if When domain excluded)

**Processing:**

1. **Prepare LMM input:** Load data/step00_calibration_by_domain.csv
2. **Center TSVR_hours:** Create `TSVR_centered = TSVR_hours - mean(TSVR_hours)` for interpretability (intercept = calibration at mean time)
3. **Contrast coding for Domain:** Use effect coding (sum-to-zero contrasts) for Domain factor
   - What = reference (if 3 domains)
   - Coefficients represent deviation from grand mean
4. **Specify LMM formula:** `calibration ~ Domain * TSVR_centered + (TSVR_centered | UID)`
   - Fixed effects: Domain main effect, TSVR_centered main effect, Domain x TSVR_centered interaction
   - Random effects: Random intercept and random slope for TSVR_centered by participant (UID)
   - Decision D070: TSVR_hours used as time variable (actual elapsed time, not nominal days)
5. **Fit LMM:** Use statsmodels MixedLM or lme4-equivalent with REML estimation
6. **Check convergence:** Verify model converged without warnings
7. **Extract fixed effects table:** Coefficients, SE, z-values, p-values (uncorrected) for all terms
8. **Extract random effects:** Variance components for random intercept, random slope, residual variance
9. **Compute ICC:** Intraclass correlation coefficient from variance components
10. **Test Domain main effect:** F-test or chi-square LRT comparing full model vs model without Domain terms
11. **Test Domain x Time interaction:** F-test or chi-square LRT comparing full model vs model without interaction term
12. **Dual p-values (Decision D068):** Report BOTH uncorrected p-values AND Bonferroni-corrected p-values for:
    - Domain main effect
    - Domain x Time interaction
    - Individual Domain coefficients (What vs grand mean, Where vs grand mean, When vs grand mean)

**Output:**

**File 1:** data/step01_lmm_model_summary.txt
**Format:** Plain text summary of fitted LMM
**Contents:**
  - Model formula
  - Fixed effects table (coefficient, SE, z, p_uncorrected, p_bonferroni)
  - Random effects variance components
  - ICC value
  - Model fit statistics (AIC, BIC, log-likelihood)
  - Convergence status

**File 2:** data/step01_domain_effects.csv
**Format:** CSV with hypothesis test results
**Columns:**
  - `term` (string, e.g., "Domain_main", "Domain_x_Time_interaction")
  - `statistic` (float, F-statistic or chi-square)
  - `df_num` (int, numerator degrees of freedom)
  - `df_denom` (int, denominator degrees of freedom, if F-test)
  - `p_uncorrected` (float, uncorrected p-value)
  - `p_bonferroni` (float, Bonferroni-corrected p-value, Decision D068)
  - `interpretation` (string, "significant" if p_bonferroni < 0.05, else "not significant")
**Expected Rows:** 2 (Domain main effect, Domain x Time interaction)

**Validation Requirement:**

Validation tools MUST be used after LMM fitting execution. Specific validation tools determined by rq_tools based on LMM analysis type (likely validate_lmm_convergence, validate_lmm_residuals, validate_hypothesis_test_dual_pvalues per Decision D068).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_lmm_model_summary.txt exists (exact path)
- data/step01_domain_effects.csv exists
- step01_domain_effects.csv: 2 rows x 7 columns

*Value Ranges:*
- Fixed effects coefficients: unrestricted (calibration scale ~ z-scores, typically -1 to +1)
- SE values: >0 (standard errors must be positive)
- p_uncorrected in [0, 1] (valid probability)
- p_bonferroni in [0, 1] (valid probability, >= p_uncorrected due to correction)
- Variance components: >0 (random intercept variance, random slope variance, residual variance all positive)
- ICC in [0, 1] (intraclass correlation bounded)

*Data Quality:*
- Model converged: TRUE (convergence status in summary.txt)
- No NaN in fixed effects table (indicates estimation failure)
- No NaN in variance components (indicates boundary singularity)
- Dual p-values present: BOTH p_uncorrected AND p_bonferroni columns in domain_effects.csv (Decision D068 compliance)
- p_bonferroni >= p_uncorrected for all rows (correction should increase p-value)

*Log Validation:*
- Required pattern: "LMM fitting complete: Model converged successfully"
- Required pattern: "Domain main effect: F={stat:.2f}, p_uncorrected={p_u:.4f}, p_bonferroni={p_b:.4f}"
- Required pattern: "Domain x Time interaction: F={stat:.2f}, p_uncorrected={p_u:.4f}, p_bonferroni={p_b:.4f}"
- Required pattern: "ICC computed: {icc:.3f}"
- Required pattern: "VALIDATION - PASS: LMM convergence"
- Required pattern: "VALIDATION - PASS: Dual p-values (D068)"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "Singular fit", "NaN in fixed effects"
- Acceptable warnings: "Random slope variance near boundary (small variance)" (if participants show similar trajectories)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Model did not converge" or "NaN in Domain coefficient")
- Log failure to logs/step01_fit_lmm.log
- Quit script immediately
- g_debug invoked to diagnose (common causes: insufficient data, random structure too complex for data, standardization error in Step 0)

---

### Step 2: Compute Post-Hoc Domain Contrasts

**Dependencies:** Step 1 (requires step01_lmm_model_summary.txt and fitted LMM object)
**Complexity:** Low (~1 minute - pairwise contrasts computation)

**Purpose:** Perform pairwise post-hoc contrasts between domains (What vs Where, What vs When, Where vs When) to identify which specific domains differ in calibration.

**Input:**

**File:** data/step00_calibration_by_domain.csv (for contrast computation)
**Object:** Fitted LMM from Step 1 (stored in memory or pickled)
**Source:** Step 1 LMM fitting

**Processing:**

1. **Load fitted LMM:** Restore LMM object from Step 1 (or re-fit if not serialized)
2. **Specify contrasts:** Define pairwise comparisons:
   - What vs Where (coefficient: beta_Where - beta_What)
   - What vs When (coefficient: beta_When - beta_What)
   - Where vs When (coefficient: beta_When - beta_Where)
3. **Compute contrasts:** Use estimated marginal means (EMMs) or manual contrast computation
4. **Standard errors:** Compute SE for each contrast using variance-covariance matrix of fixed effects
5. **Test statistics:** z = contrast / SE
6. **Dual p-values (Decision D068):**
   - p_uncorrected: Two-tailed z-test p-value per contrast
   - p_bonferroni: Bonferroni correction for 3 comparisons (p_bonferroni = min(p_uncorrected * 3, 1.0))
7. **Effect sizes:** Compute Cohen's d for each contrast (difference in means / pooled SD)
8. **Interpretation:** Flag significant contrasts (p_bonferroni < 0.05)

**Output:**

**File 1:** data/step02_post_hoc_contrasts.csv
**Format:** CSV with pairwise contrast results
**Columns:**
  - `contrast` (string, e.g., "What vs Where", "What vs When", "Where vs When")
  - `estimate` (float, difference in calibration between domains)
  - `SE` (float, standard error of estimate)
  - `z` (float, test statistic)
  - `p_uncorrected` (float, uncorrected two-tailed p-value)
  - `p_bonferroni` (float, Bonferroni-corrected p-value for 3 comparisons, Decision D068)
  - `cohens_d` (float, standardized effect size)
  - `interpretation` (string, "significant" if p_bonferroni < 0.05, else "not significant")
**Expected Rows:** 3 (What vs Where, What vs When, Where vs When)
**Note:** If When domain excluded, only 1 row (What vs Where)

**Validation Requirement:**

Validation tools MUST be used after post-hoc contrasts computation. Specific validation tools determined by rq_tools based on contrast analysis type (likely validate_contrasts_dual_pvalues per Decision D068).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_post_hoc_contrasts.csv exists (exact path)
- Expected rows: 3 (all pairwise comparisons) OR 1 if When domain excluded
- Expected columns: 8 (contrast, estimate, SE, z, p_uncorrected, p_bonferroni, cohens_d, interpretation)

*Value Ranges:*
- estimate: unrestricted (calibration difference, typically -2 to +2)
- SE: >0 (standard errors positive)
- z: unrestricted (test statistic)
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1], >= p_uncorrected (correction should not decrease p-value)
- cohens_d: typically -2 to +2 (|d| > 5 suggests error)

*Data Quality:*
- Dual p-values present: BOTH p_uncorrected AND p_bonferroni columns (Decision D068)
- p_bonferroni = min(p_uncorrected * 3, 1.0) (Bonferroni correction for 3 comparisons)
- All 3 pairwise contrasts present (What vs Where, What vs When, Where vs When) OR subset if domain excluded
- No NaN values (all contrasts must be estimable)

*Log Validation:*
- Required pattern: "Post-hoc contrasts computed: 3 pairwise comparisons"
- Required pattern: "What vs Where: estimate={est:.3f}, p_uncorrected={p_u:.4f}, p_bonferroni={p_b:.4f}"
- Required pattern: "What vs When: estimate={est:.3f}, p_uncorrected={p_u:.4f}, p_bonferroni={p_b:.4f}"
- Required pattern: "Where vs When: estimate={est:.3f}, p_uncorrected={p_u:.4f}, p_bonferroni={p_b:.4f}"
- Required pattern: "VALIDATION - PASS: Dual p-values (D068)"
- Forbidden patterns: "ERROR", "Contrast not estimable", "NaN in p-value"
- Acceptable warnings: "When domain excluded: only What vs Where contrast available"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Missing p_bonferroni column" or "NaN in contrast estimate")
- Log failure to logs/step02_compute_contrasts.log
- Quit script immediately
- g_debug invoked to diagnose (common causes: LMM fitting issue in Step 1, missing domain factor levels)

---

### Step 3: Rank Domains by Calibration Quality

**Dependencies:** Step 0 (requires step00_calibration_by_domain.csv)
**Complexity:** Low (<1 minute - summary statistics only)

**Purpose:** Compute mean absolute calibration per domain and rank domains from best-calibrated (lowest |calibration|) to worst-calibrated (highest |calibration|).

**Input:**

**File:** data/step00_calibration_by_domain.csv
**Source:** Generated by Step 0
**Required Columns:** Domain, abs_calibration

**Processing:**

1. **Load data:** Read data/step00_calibration_by_domain.csv
2. **Group by Domain:** Aggregate abs_calibration by Domain factor
3. **Compute mean |calibration|:** Mean of abs_calibration column per domain
4. **Compute SD |calibration|:** SD of abs_calibration per domain
5. **Compute N:** Count observations per domain
6. **Rank domains:** Order by mean_abs_calibration ascending (lower = better calibrated)
7. **Assign ranks:** 1 = best calibrated (lowest mean |calibration|), 2 = middle, 3 = worst calibrated (highest mean |calibration|)
8. **Identify best/worst:** Flag best_calibrated_domain (rank 1) and worst_calibrated_domain (rank 3 or 2 if only 2 domains)

**Output:**

**File:** data/step03_domain_ranking.csv
**Format:** CSV with domain-level calibration summaries
**Columns:**
  - `Domain` (string, What/Where/When)
  - `mean_abs_calibration` (float, mean absolute calibration for domain)
  - `sd_abs_calibration` (float, SD of absolute calibration)
  - `N` (int, number of observations per domain)
  - `rank` (int, 1=best calibrated, 2=middle, 3=worst calibrated)
  - `interpretation` (string, "Best calibrated", "Middle", "Worst calibrated")
**Expected Rows:** 3 (What, Where, When) OR 2 if When excluded
**Sorted By:** rank ascending (best calibrated first)

**Validation Requirement:**

Validation tools MUST be used after domain ranking computation. Specific validation tools determined by rq_tools based on summary statistics format (likely validate_data_format, validate_numeric_range).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_domain_ranking.csv exists (exact path)
- Expected rows: 3 (all domains) OR 2 if When excluded
- Expected columns: 6 (Domain, mean_abs_calibration, sd_abs_calibration, N, rank, interpretation)

*Value Ranges:*
- mean_abs_calibration in [0, 3] (absolute calibration, >3 suggests standardization error)
- sd_abs_calibration in [0, 2] (SD of absolute values, must be non-negative)
- N in [300, 500] per domain (1200 total / 3 domains ~ 400, range allows for When exclusion or missing data)
- rank in {1, 2, 3} (consecutive integers, no gaps)

*Data Quality:*
- All domains present: {What, Where, When} OR {What, Where} subset
- No NaN values (all summary statistics must be computable)
- No duplicate ranks (each domain unique rank)
- Ranks consecutive: 1, 2, 3 (or 1, 2 if 2 domains)
- Interpretation matches rank: rank 1 = "Best calibrated", rank 3 = "Worst calibrated"
- N sum across domains = 1200 (or 800 if When excluded)

*Log Validation:*
- Required pattern: "Domain ranking computed: {N} domains ranked"
- Required pattern: "Best calibrated domain: {domain} (mean |calibration| = {val:.3f})"
- Required pattern: "Worst calibrated domain: {domain} (mean |calibration| = {val:.3f})"
- Forbidden patterns: "ERROR", "NaN in ranking", "Duplicate rank"
- Acceptable warnings: "When domain excluded from ranking"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Duplicate rank detected" or "N sum != 1200")
- Log failure to logs/step03_rank_domains.log
- Quit script immediately
- g_debug invoked to diagnose (common causes: missing domain, data filtering error)

---

### Step 4: Prepare Calibration Trajectory Plot Data

**Dependencies:** Step 0 (requires step00_calibration_by_domain.csv)
**Complexity:** Low (~1 minute - data aggregation only)

**Purpose:** Aggregate calibration data for visualization showing calibration trajectories by domain over time. This creates plot source CSV for rq_plots to generate trajectory visualization.

**Plot Description:** Trajectory showing calibration (signed difference: confidence - accuracy) over time (TSVR_hours), grouped by domain (What/Where/When), with error bars representing 95% confidence intervals. Y-axis = calibration (positive = overconfidence, negative = underconfidence, zero = well-calibrated). X-axis = TSVR_hours (0, ~24, ~72, ~144 for T1-T4).

**Required Data Sources:**
- data/step00_calibration_by_domain.csv (columns: UID, TEST, Domain, TSVR_hours, calibration)

**Processing:**

1. **Load data:** Read data/step00_calibration_by_domain.csv
2. **Group by Domain x TEST:** Aggregate calibration by Domain and TEST
3. **Compute mean calibration:** Mean of calibration column per Domain x TEST
4. **Compute SE:** Standard error of mean (SD / sqrt(N))
5. **Compute 95% CI:** CI_lower = mean - 1.96*SE, CI_upper = mean + 1.96*SE
6. **Map TEST to TSVR_hours:** Extract mean TSVR_hours per TEST (T1=0, T2~24, T3~72, T4~144)
7. **Select columns:** Domain, TSVR_hours, mean_calibration, CI_lower, CI_upper
8. **Sort:** By Domain, then TSVR_hours ascending

**Output (Plot Source CSV):**

**File:** data/step04_calibration_trajectory_data.csv
**Format:** CSV, plot source data for calibration trajectory
**Columns:**
  - `Domain` (string, What/Where/When)
  - `TSVR_hours` (float, mean time per TEST: 0, ~24, ~72, ~144)
  - `mean_calibration` (float, mean calibration per Domain x TEST)
  - `CI_lower` (float, lower 95% confidence bound)
  - `CI_upper` (float, upper 95% confidence bound)
**Expected Rows:** 12 (3 domains x 4 timepoints) OR 8 if When excluded
**Note:** This CSV is read by rq_plots later. PNG output goes to plots/ when rq_plots runs.

**Validation Requirement:**

Validation tools MUST be used after plot data preparation execution. Specific validation tools determined by rq_tools based on plot data format requirements (likely validate_plot_data_completeness, validate_numeric_range, validate_dataframe_structure).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_calibration_trajectory_data.csv exists (exact path)
- Expected rows: 12 (3 domains x 4 timepoints) OR 8 (2 domains x 4 timepoints if When excluded)
- Expected columns: 5 (Domain, TSVR_hours, mean_calibration, CI_lower, CI_upper)
- Data types: Domain (string), TSVR_hours (float), mean_calibration (float), CI bounds (float)

*Value Ranges:*
- TSVR_hours in [0, 168] (0=encoding, 168=1 week max)
- mean_calibration: unrestricted (signed difference, typically -2 to +2)
- CI_lower: unrestricted but < mean_calibration
- CI_upper: unrestricted but > mean_calibration
- CI_upper > CI_lower for all rows (confidence bounds properly ordered)

*Data Quality:*
- No NaN values tolerated (all cells must have valid values)
- Expected N: Exactly 12 rows (3 domains x 4 timepoints) OR 8 rows (2 domains x 4 timepoints)
- No duplicate rows (Domain x TSVR_hours combinations unique)
- All domains represented: {What, Where, When} OR {What, Where} subset
- All 4 timepoints per domain: TSVR_hours ~ {0, 24, 72, 144} (tolerance +/- 5 hours for actual variation)
- Distribution check: CI_upper > CI_lower for all rows

*Log Validation:*
- Required pattern: "Plot data preparation complete: {N} rows created"
- Required pattern: "Domains represented: {domain list}"
- Required pattern: "Timepoints per domain: 4 (T1, T2, T3, T4)"
- Forbidden patterns: "ERROR", "NaN values detected", "Missing domain", "Missing timepoint"
- Acceptable warnings: "When domain excluded: 8 rows created (What/Where only)"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 12 rows, found 9" or "CI_lower > CI_upper in row 3")
- Log failure to logs/step04_prepare_plot_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- g_debug invoked to diagnose root cause (common causes: missing TEST, grouping error, CI computation error)

**Plotting Function (rq_plots will call):** Trajectory plot with confidence bands
- rq_plots agent maps this description to specific tools/plots.py function (likely plot_trajectory)
- Plot reads data/step04_calibration_trajectory_data.csv (created by this step)
- No data aggregation in rq_plots (visualization only per Option B)
- PNG output saved to plots/ folder by rq_plots

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 Output -> Step 1 Input:**
- Format: Long format (one row per UID x TEST x Domain)
- Key columns: UID, TEST, Domain, TSVR_hours, calibration
- No transformation needed - Step 1 reads Step 0 output directly

**Step 0 Output -> Step 3 Input:**
- Format: Long format (same as Step 0 output)
- Transformation: Group by Domain, compute mean/SD/N of abs_calibration
- Output: Domain-level summary (3 rows)

**Step 0 Output -> Step 4 Input:**
- Format: Long format (same as Step 0 output)
- Transformation: Group by Domain x TEST, compute mean calibration + 95% CI
- Output: Domain x Timepoint summary (12 rows)

### Column Naming Conventions

Per names.md conventions:
- `UID` - Participant identifier (format: P### with leading zeros)
- `TEST` - Test session (T1, T2, T3, T4)
- `Domain` - Memory domain factor (What, Where, When)
- `TSVR_hours` - Time Since VR in hours (Decision D070 - actual time, not nominal days)
- `theta_accuracy` - Accuracy IRT ability estimate (from Ch5 5.2.1)
- `theta_confidence` - Confidence IRT ability estimate (from Ch6 6.3.1)
- `theta_accuracy_z` - Z-standardized accuracy theta (mean~0, SD~1)
- `theta_confidence_z` - Z-standardized confidence theta (mean~0, SD~1)
- `calibration` - Signed calibration (theta_confidence_z - theta_accuracy_z)
- `abs_calibration` - Absolute calibration (|calibration|, magnitude of miscalibration)
- `CI_lower` - Lower 95% confidence bound (for plots)
- `CI_upper` - Upper 95% confidence bound (for plots)

### Data Type Constraints

- Participant identifiers: String (UID format: P###)
- Test sessions: String (categorical: T1, T2, T3, T4)
- Domains: String (categorical: What, Where, When)
- Time variables: Float (TSVR_hours, TSVR_centered)
- Theta estimates: Float (theta_accuracy, theta_confidence, z-standardized versions)
- Calibration metrics: Float (calibration, abs_calibration)
- Statistical outputs: Float (p-values, SE, coefficients, effect sizes)
- Confidence intervals: Float (CI_lower, CI_upper)
- Counts: Integer (N, rank)

**Nullable vs Non-Nullable:**
- After Step 0 merge: NO NaN values tolerated (circuit breaker if any detected)
- All numeric columns non-nullable after merge
- All identifier columns (UID, TEST, Domain) non-nullable

---

## Cross-RQ Dependencies

### Dependency Type: DERIVED Data from Other RQs (Dependencies Exist)

**This RQ requires outputs from:**

**RQ 1: Ch5 5.2.1** (Domain-stratified accuracy trajectories)
- File: results/ch5/5.2.1/data/step03_theta_accuracy_domain.csv
- Used in: Step 0 (accuracy theta by domain for calibration computation)
- Rationale: Ch5 5.2.1 establishes domain-stratified accuracy theta estimates via 2-pass IRT calibration. This RQ uses those accuracy estimates as one component of calibration (difference between confidence and accuracy).

**RQ 2: Ch6 6.3.1** (Domain-stratified confidence trajectories)
- File: results/ch6/6.3.1/data/step03_theta_confidence_domain.csv
- Used in: Step 0 (confidence theta by domain for calibration computation)
- Rationale: Ch6 6.3.1 establishes domain-stratified confidence theta estimates via 2-pass IRT calibration on confidence ratings. This RQ uses those confidence estimates as the other component of calibration.

**Execution Order Constraint:**
1. Ch5 5.2.1 must complete through Step 3 (accuracy IRT calibration, theta extraction)
2. Ch6 6.3.1 must complete through Step 3 (confidence IRT calibration, theta extraction)
3. This RQ (6.3.2) executes after both dependencies complete (uses both theta outputs)

**Data Source Boundaries:**
- **RAW data:** None (this RQ uses only DERIVED data from other RQs)
- **DERIVED data:** Accuracy theta from Ch5 5.2.1, Confidence theta from Ch6 6.3.1
- **Scope:** This RQ does NOT re-calibrate IRT models (uses existing theta estimates from source RQs)
- **Calibration metric:** Computed as difference between z-standardized confidence and accuracy theta

**Validation:**
- Step 0: Check results/ch5/5.2.1/data/step03_theta_accuracy_domain.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch6/6.3.1/data/step03_theta_confidence_domain.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 0: Verify domain compatibility (if Ch5 5.2.1 has What/Where only and Ch6 6.3.1 has What/Where/When, merge reduces to What/Where intersection)
- If either file missing -> quit with error -> user must execute dependency RQs first

**When Domain Compatibility:**
- **Ideal scenario:** Both source RQs retain When domain (1200 observations = 100 participants x 4 tests x 3 domains)
- **Likely scenario:** When domain excluded from one or both source RQs due to purification issues (<10 items retained)
- **Acceptable scenario:** Analysis proceeds with What/Where only (800 observations)
- **Circuit breaker scenario:** If <2 domains available after merge, quit with CLARITY ERROR (need at least 2 domains for comparison)

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

#### Step 0: Load and Merge Accuracy and Confidence Data

**Analysis Tool:** (determined by rq_tools - likely pandas read_csv + merge operations + standardization)
**Validation Tool:** (determined by rq_tools - likely validate_data_format, validate_numeric_range, check_missing_data, validate_standardization)

**What Validation Checks:**
- Output file exists (data/step00_calibration_by_domain.csv)
- Expected row count (1200 OR 800 if When excluded)
- Expected column count (12 columns)
- No NaN values (merge must be complete)
- theta_accuracy in [-3, 3]
- theta_confidence in [-3, 3]
- se_accuracy in [0.1, 1.0]
- se_confidence in [0.1, 1.0]
- theta_accuracy_z: mean ~ 0, SD ~ 1 (z-standardized)
- theta_confidence_z: mean ~ 0, SD ~ 1 (z-standardized)
- calibration in [-3, 3] (typical range)
- abs_calibration in [0, 3]
- TSVR_hours in [0, 168]
- No duplicate rows (UID x TEST x Domain unique)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step00_load_merge_data.log
- Quit script immediately
- g_debug invoked to diagnose (likely: source RQ incomplete, domain mismatch, standardization error)

---

#### Step 1: Fit LMM with Domain x Time Interaction

**Analysis Tool:** (determined by rq_tools - likely fit_lmm_trajectory_tsvr)
**Validation Tool:** (determined by rq_tools - likely validate_lmm_convergence, validate_lmm_residuals, validate_hypothesis_test_dual_pvalues)

**What Validation Checks:**
- Output files exist (data/step01_lmm_model_summary.txt, data/step01_domain_effects.csv)
- Model converged (convergence status = TRUE)
- No NaN in fixed effects table
- No NaN in variance components
- Variance components > 0 (positive definite)
- ICC in [0, 1]
- Dual p-values present: p_uncorrected AND p_bonferroni columns (Decision D068)
- p_bonferroni >= p_uncorrected (correction should not decrease p-value)
- Residuals approximately normal (Kolmogorov-Smirnov test)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step01_fit_lmm.log
- Quit script immediately
- g_debug invoked to diagnose (common causes: insufficient data, random structure too complex, standardization error)

---

#### Step 2: Compute Post-Hoc Domain Contrasts

**Analysis Tool:** (determined by rq_tools - likely compute_contrasts_pairwise)
**Validation Tool:** (determined by rq_tools - likely validate_contrasts_dual_pvalues)

**What Validation Checks:**
- Output file exists (data/step02_post_hoc_contrasts.csv)
- Expected row count (3 contrasts OR 1 if When excluded)
- Expected column count (8 columns)
- Dual p-values present: p_uncorrected AND p_bonferroni columns (Decision D068)
- p_bonferroni >= p_uncorrected
- p_bonferroni = min(p_uncorrected * 3, 1.0) (Bonferroni correction for 3 comparisons)
- No NaN values (all contrasts estimable)
- SE > 0 (positive standard errors)
- cohens_d in [-5, 5] (extreme values suggest error)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step02_compute_contrasts.log
- Quit script immediately
- g_debug invoked to diagnose (common causes: LMM fitting issue in Step 1, missing domain levels)

---

#### Step 3: Rank Domains by Calibration Quality

**Analysis Tool:** (determined by rq_tools - likely pandas groupby + summary statistics)
**Validation Tool:** (determined by rq_tools - likely validate_data_format, validate_numeric_range)

**What Validation Checks:**
- Output file exists (data/step03_domain_ranking.csv)
- Expected row count (3 domains OR 2 if When excluded)
- Expected column count (6 columns)
- mean_abs_calibration in [0, 3]
- sd_abs_calibration in [0, 2]
- N in [300, 500] per domain
- Ranks consecutive: {1, 2, 3} OR {1, 2}
- No duplicate ranks
- Interpretation matches rank
- N sum across domains = 1200 (or 800 if When excluded)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step03_rank_domains.log
- Quit script immediately
- g_debug invoked to diagnose (common causes: missing domain, data filtering error)

---

#### Step 4: Prepare Calibration Trajectory Plot Data

**Analysis Tool:** (determined by rq_tools - likely pandas groupby + CI computation)
**Validation Tool:** (determined by rq_tools - likely validate_plot_data_completeness, validate_numeric_range, validate_dataframe_structure)

**What Validation Checks:**
- Output file exists (data/step04_calibration_trajectory_data.csv)
- Expected row count (12 OR 8 if When excluded)
- Expected column count (5 columns)
- No NaN values
- TSVR_hours in [0, 168]
- CI_upper > CI_lower for all rows
- All domains represented ({What, Where, When} OR {What, Where})
- All 4 timepoints per domain
- No duplicate rows (Domain x TSVR_hours unique)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step04_prepare_plot_data.log
- Quit script immediately
- g_debug invoked to diagnose (common causes: missing TEST, grouping error, CI computation error)

---

## Summary

**Total Steps:** 5 (Step 0: data loading/merge + Steps 1-4: analysis)
**Estimated Runtime:** Low (~5-10 minutes total - no IRT model fitting)
**Cross-RQ Dependencies:** 2 (Ch5 5.2.1 accuracy theta, Ch6 6.3.1 confidence theta)
**Primary Outputs:**
- data/step00_calibration_by_domain.csv (1200 rows: UID x TEST x Domain with calibration metrics)
- data/step01_lmm_model_summary.txt (LMM results with Domain x Time interaction)
- data/step01_domain_effects.csv (Hypothesis tests with dual p-values per D068)
- data/step02_post_hoc_contrasts.csv (Pairwise domain comparisons with dual p-values)
- data/step03_domain_ranking.csv (Domains ranked by calibration quality)
- data/step04_calibration_trajectory_data.csv (Plot source CSV for rq_plots)
**Validation Coverage:** 100% (all 5 steps have validation requirements)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent
