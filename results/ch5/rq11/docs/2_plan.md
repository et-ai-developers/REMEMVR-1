# Analysis Plan: RQ 5.11 - IRT-CTT Convergent Validity

**Research Question:** 5.11
**Created:** 2025-11-26
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines convergent validity between IRT (Item Response Theory) and CTT (Classical Test Theory) measurement approaches for episodic memory ability across three domains (What, Where, When) and four test sessions. The analysis compares whether IRT theta scores and CTT mean scores yield identical conclusions about domain-specific forgetting trajectories.

**Pipeline:** Correlation Analysis + Parallel LMM Comparison (IRT vs CTT)
**Steps:** 8 analysis steps (Step 0: data extraction + Steps 1-7: analysis)
**Estimated Runtime:** Medium (correlation + dual LMM fitting + validation, ~20-40 minutes total)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (Holm-Bonferroni corrected + uncorrected for correlation tests)
- Decision D070: TSVR as LMM time variable (actual hours since encoding)

**Cross-RQ Dependency:**
This RQ requires RQ 5.1 completion (IRT theta scores, TSVR mapping, purified item list). CTT scores computed fresh from raw data using same purified item set for fair comparison.

---

## Analysis Plan

### Step 0: Data Extraction

**Dependencies:** None (first step, but requires RQ 5.1 completion)
**Complexity:** Low (file loading and merging, <5 minutes)

**Purpose:** Load IRT scores from RQ 5.1, compute CTT scores from raw data, merge with TSVR

**Input:**

**File 1:** results/ch5/rq1/data/step03_theta_scores.csv (from RQ 5.1)
**Source:** RQ 5.1 Step 3 (IRT calibration Pass 2 theta extraction)
**Format:** CSV with columns:
  - composite_ID (string, format: UID_test, e.g., P001_T1)
  - theta_common (float, IRT ability estimate for common memory dimension)
  - theta_congruent (float, IRT ability estimate for congruent memory dimension)
  - theta_incongruent (float, IRT ability estimate for incongruent memory dimension)
  - se_common (float, standard error for theta_common)
  - se_congruent (float, standard error for theta_congruent)
  - se_incongruent (float, standard error for theta_incongruent)
**Expected Rows:** ~400 (100 participants x 4 tests)

**File 2:** results/ch5/rq1/data/step00_tsvr_mapping.csv (from RQ 5.1)
**Source:** RQ 5.1 Step 0 (TSVR extraction)
**Format:** CSV with columns:
  - UID (string, participant identifier, e.g., P001)
  - test (string, test session identifier: T1, T2, T3, T4)
  - TSVR_hours (float, actual hours since encoding)
**Expected Rows:** ~400 (100 participants x 4 tests)

**File 3:** results/ch5/rq1/data/step02_purified_items.csv (from RQ 5.1)
**Source:** RQ 5.1 Step 2 (item purification)
**Format:** CSV with columns:
  - item_name (string, item identifier from master.xlsx)
  - dimension (string, memory dimension: common, congruent, incongruent)
  - a (float, item discrimination from Pass 1)
  - b (float, item difficulty from Pass 1)
**Expected Rows:** ~40-50 items (purified subset after Decision D039 thresholds)
**Purpose:** Identify which items to use for CTT score computation (fair comparison requires same item set)

**File 4:** data/cache/dfData.csv (project-level raw data)
**Source:** Master dataset with all participant responses
**Format:** CSV with columns including:
  - UID (string, participant identifier)
  - TEST (string, test session: T1, T2, T3, T4)
  - TQ_* columns (item responses, 0/1 for incorrect/correct)
**Expected Rows:** ~400 (100 participants x 4 tests)

**Processing:**

1. Load IRT theta scores from RQ 5.1 (step03_theta_scores.csv)
2. Load TSVR mapping from RQ 5.1 (step00_tsvr_mapping.csv)
3. Load purified item list from RQ 5.1 (step02_purified_items.csv)
4. Load raw item responses from dfData.csv
5. Filter dfData to ONLY purified items (item_name in purified_items.csv) for fair comparison
6. Map RQ 5.1 dimensions to WWW domains:
   - Common dimension -> What domain (-N- tags)
   - Congruent dimension -> Where domain (-L-/-U-/-D- tags)
   - Incongruent dimension -> When domain (-O- tags)
7. Compute CTT mean scores per UID x test x domain from filtered raw data:
   - CTT_What = mean(all -N- items in purified list)
   - CTT_Where = mean(all -L-/-U-/-D- items in purified list)
   - CTT_When = mean(all -O- items in purified list)
8. Reshape IRT theta scores from wide to long format:
   - One row per UID x test x domain
   - Columns: UID, test, domain (What/Where/When), IRT_score (theta value)
9. Reshape CTT scores to long format (same structure):
   - Columns: UID, test, domain, CTT_score (mean value)
10. Merge IRT and CTT scores on UID + test + domain (paired comparison)
11. Merge TSVR_hours on UID + test
12. Final format: UID, test, domain, TSVR_hours, IRT_score, CTT_score

**Output:**

**File 1:** data/step00_irt_ctt_paired.csv
**Format:** CSV, long format (one row per measurement: UID x test x domain)
**Columns:**
  - UID (string, participant identifier)
  - test (string, test session: T1, T2, T3, T4)
  - domain (string, memory domain: What, Where, When)
  - TSVR_hours (float, time since encoding in hours)
  - IRT_score (float, theta estimate from RQ 5.1)
  - CTT_score (float, mean accuracy score computed from purified items, range: 0-1)
**Expected Rows:** ~1200 (100 participants x 4 tests x 3 domains)

**File 2:** logs/step00_extraction_report.txt
**Format:** Plain text report
**Content:**
  - Number of purified items per domain
  - Number of participants with complete data
  - TSVR range per test session
  - IRT score range per domain
  - CTT score range per domain

**Validation Requirement:**
Validation tools MUST be used after data extraction tool execution. Specific validation tools will be determined by rq_tools based on data format requirements (likely validate_data_extraction or custom validation for paired format).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_irt_ctt_paired.csv exists (exact path)
- Expected rows: 1200 (100 participants x 4 tests x 3 domains)
- Expected columns: 6 (UID, test, domain, TSVR_hours, IRT_score, CTT_score)
- Data types: UID (object), test (object), domain (object), TSVR_hours (float64), IRT_score (float64), CTT_score (float64)

*Value Ranges:*
- TSVR_hours in [0, 200] hours (0 = encoding, ~168 = 1 week, allow buffer)
- IRT_score in [-3, 3] (typical IRT ability range from RQ 5.1)
- CTT_score in [0, 1] (proportion correct, cannot exceed bounds)
- domain in {What, Where, When} (categorical, exactly 3 levels)
- test in {T1, T2, T3, T4} (categorical, exactly 4 levels)

*Data Quality:*
- No NaN values tolerated in IRT_score or CTT_score (indicates merge failure)
- TSVR_hours may have NaN if participant missing session (document tolerance)
- Expected N: Exactly 1200 rows (100 participants x 4 tests x 3 domains)
- Balance check: Each UID should have exactly 12 rows (4 tests x 3 domains)
- No duplicate rows (UID x test x domain combinations unique)

*Log Validation:*
- Required pattern: "Extraction complete: 1200 rows created"
- Required pattern: "Purified items loaded: [N] items"
- Required pattern: "All domains mapped: What, Where, When"
- Forbidden patterns: "ERROR", "Merge failed", "Missing domain"
- Acceptable warnings: "Participant [UID] missing test [T] (data loss documented)"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 1200 rows, found 950")
- Log failure to logs/step00_extract_data.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause (likely RQ 5.1 incomplete or purified items missing)

---

### Step 1: Correlation Analysis

**Dependencies:** Step 0 (requires paired IRT-CTT scores)
**Complexity:** Low (correlation computation, <5 minutes)

**Purpose:** Compute Pearson correlations between IRT and CTT scores for each domain + overall

**Input:**

**File:** data/step00_irt_ctt_paired.csv (from Step 0)
**Format:** Long format with columns: UID, test, domain, TSVR_hours, IRT_score, CTT_score
**Expected Rows:** ~1200 (100 participants x 4 tests x 3 domains)

**Processing:**

1. Compute Pearson correlations for each domain separately:
   - r_What: correlation(IRT_score, CTT_score) for domain == "What"
   - r_Where: correlation(IRT_score, CTT_score) for domain == "Where"
   - r_When: correlation(IRT_score, CTT_score) for domain == "When"
2. Compute overall correlation (all domains pooled):
   - r_Overall: correlation(IRT_score, CTT_score) for all rows
3. For each correlation, compute:
   - Pearson r coefficient
   - 95% confidence interval (Fisher z-transformation method)
   - Uncorrected p-value (two-tailed test of r != 0)
4. Apply Holm-Bonferroni correction across 4 tests (per Decision D068 philosophy):
   - Rank p-values from smallest to largest (k = 1 to 4)
   - Adjusted alpha_k = 0.05 / (4 - k + 1)
   - Compare p_k to alpha_k, reject if p_k < alpha_k
   - Report both uncorrected AND corrected p-values for transparency
5. Test convergence thresholds:
   - Primary threshold: r > 0.70 (strong convergence per psychometric standards)
   - Secondary threshold: r > 0.90 (exceptional convergence)
   - Report which domains meet each threshold

**Output:**

**File 1:** results/step01_correlations.csv
**Format:** CSV with correlation results
**Columns:**
  - domain (string: What, Where, When, Overall)
  - r (float, Pearson correlation coefficient)
  - CI_lower (float, lower bound 95% CI)
  - CI_upper (float, upper bound 95% CI)
  - p_uncorrected (float, uncorrected p-value)
  - p_holm_bonferroni (float, Holm-Bonferroni corrected p-value)
  - meets_r70 (bool, TRUE if r > 0.70)
  - meets_r90 (bool, TRUE if r > 0.90)
**Expected Rows:** 4 (3 domains + 1 overall)

**File 2:** logs/step01_correlation_report.txt
**Format:** Plain text summary
**Content:**
  - Interpretation of correlations (strong/moderate/weak per Cohen's standards)
  - Which domains meet r > 0.70 and r > 0.90 thresholds
  - Holm-Bonferroni correction details (adjusted alphas per rank)

**Validation Requirement:**
Validation tools MUST be used after correlation analysis tool execution. Specific validation tools will be determined by rq_tools (likely validate_hypothesis_tests for correlation format validation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step01_correlations.csv exists
- Expected rows: 4 (What, Where, When, Overall)
- Expected columns: 8 (domain, r, CI_lower, CI_upper, p_uncorrected, p_holm_bonferroni, meets_r70, meets_r90)
- Data types: domain (object), r (float64), CI bounds (float64), p-values (float64), boolean flags (bool)

*Value Ranges:*
- r in [-1, 1] (correlation bounds)
- CI_lower in [-1, 1], CI_upper in [-1, 1], CI_lower < CI_upper
- p_uncorrected in [0, 1], p_holm_bonferroni in [0, 1]
- For convergent validity, expect r > 0 (negative would indicate serious construct validity issue)

*Data Quality:*
- No NaN values allowed (all correlations must compute)
- All 4 domains present (What, Where, When, Overall)
- CI intervals must contain r value (CI_lower < r < CI_upper)
- Holm-Bonferroni p-values >= uncorrected p-values (correction never decreases p)

*Log Validation:*
- Required pattern: "Correlations computed: 4 tests"
- Required pattern: "Holm-Bonferroni correction applied"
- Forbidden patterns: "ERROR", "Correlation undefined", "Insufficient data"
- Acceptable warnings: None expected for correlation computation

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Correlation r = -0.15 for What domain (expected positive)")
- Log failure to logs/step01_correlation.log
- Quit script immediately
- g_debug invoked (likely data quality issue in Step 0)

---

### Step 2: Fit Parallel LMMs (IRT Model)

**Dependencies:** Step 0 (requires paired scores with TSVR)
**Complexity:** Medium (LMM fitting, 5-10 minutes per model)

**Purpose:** Fit LMM using IRT scores as outcome to establish baseline trajectory

**Input:**

**File:** data/step00_irt_ctt_paired.csv (from Step 0)
**Format:** Long format
**Columns:** UID, test, domain, TSVR_hours, IRT_score, CTT_score
**Expected Rows:** ~1200

**Processing:**

1. Filter to IRT scores only (select UID, test, domain, TSVR_hours, IRT_score)
2. Create time transformations:
   - time_linear = TSVR_hours
   - time_log = log(TSVR_hours + 1) (add 1 to handle TSVR = 0 at encoding)
3. Fit LMM with formula:
   - IRT_score ~ (time_linear + time_log) x domain + (time_linear | UID)
   - Fixed effects: time_linear, time_log, domain, time_linear:domain, time_log:domain
   - Random effects: random slopes for time_linear per UID (allows individual trajectories)
   - Method: REML (Restricted Maximum Likelihood)
4. Model selection strategy (per 1_concept.md):
   - Attempt full random slopes model (time_linear | UID) first
   - If convergence fails, simplify to random intercepts only (1 | UID)
   - Document convergence decision in log
5. Extract outputs:
   - Fixed effects table (coefficients, SE, t-values, p-values)
   - Random effects variance components
   - Model fit indices (AIC, BIC, log-likelihood)
   - Convergence status

**Output:**

**File 1:** data/step02_irt_lmm_fitted.pkl
**Format:** Pickle file (statsmodels MixedLM fitted model object)
**Purpose:** Save fitted model for later comparison (Step 5)

**File 2:** results/step02_irt_fixed_effects.csv
**Format:** CSV with fixed effects
**Columns:**
  - term (string, coefficient name)
  - estimate (float, beta coefficient)
  - se (float, standard error)
  - t_value (float, t-statistic)
  - p_value (float, two-tailed p-value)
**Expected Rows:** ~11 (intercept + 2 time terms + 2 domains + 4 interactions)

**File 3:** results/step02_irt_random_effects.csv
**Format:** CSV with random effects variances
**Columns:**
  - component (string, variance component name)
  - variance (float, estimated variance)
  - sd (float, standard deviation)
**Expected Rows:** ~2-3 (random intercept variance, random slope variance if used, residual variance)

**File 4:** results/step02_irt_model_fit.csv
**Format:** CSV with fit indices
**Columns:**
  - metric (string: AIC, BIC, logLik, convergence_status)
  - value (float or string)
**Expected Rows:** 4

**File 5:** logs/step02_irt_lmm_log.txt
**Format:** Plain text log
**Content:**
  - Model formula used
  - Convergence status (TRUE/FALSE)
  - Random effects structure (full slopes or intercepts only)
  - Rationale if model simplified

**Validation Requirement:**
Validation tools MUST be used after LMM fitting tool execution. Specific validation tools will be determined by rq_tools (likely validate_lmm_convergence to check model convergence status).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_irt_lmm_fitted.pkl exists (fitted model object)
- results/step02_irt_fixed_effects.csv: 11 rows x 5 columns
- results/step02_irt_random_effects.csv: 2-3 rows x 3 columns
- results/step02_irt_model_fit.csv: 4 rows x 2 columns

*Value Ranges:*
- Fixed effects estimates: no strict bounds (domain-dependent), but expect |estimate| < 5 for IRT scale
- Standard errors: se > 0 (must be positive)
- p_value in [0, 1]
- AIC, BIC > 0 (fit indices always positive)
- Convergence_status == "TRUE" (string, model must converge)

*Data Quality:*
- No NaN values in fixed effects table (indicates convergence failure)
- All expected terms present (intercept, time_linear, time_log, domain, interactions)
- Random effects variances > 0 (negative variance = model misspecification)

*Log Validation:*
- Required pattern: "Model converged: TRUE"
- Required pattern: "Random effects structure: [slopes|intercepts]"
- Forbidden patterns: "Convergence failed", "Singular fit", "NaN coefficients"
- Acceptable warnings: "Random slopes caused convergence issues, simplified to intercepts" (documented decision)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Model convergence failed despite simplification")
- Log failure to logs/step02_irt_lmm.log
- Quit script immediately
- g_debug invoked (check data quality, model specification)

---

### Step 3: Fit Parallel LMMs (CTT Model)

**Dependencies:** Step 0 (requires paired scores with TSVR)
**Complexity:** Medium (LMM fitting, 5-10 minutes)

**Purpose:** Fit identical LMM using CTT scores as outcome for parallel comparison

**Input:**

**File:** data/step00_irt_ctt_paired.csv (from Step 0)
**Format:** Long format
**Columns:** UID, test, domain, TSVR_hours, IRT_score, CTT_score
**Expected Rows:** ~1200

**Processing:**

1. Filter to CTT scores only (select UID, test, domain, TSVR_hours, CTT_score)
2. Create IDENTICAL time transformations as Step 2:
   - time_linear = TSVR_hours
   - time_log = log(TSVR_hours + 1)
3. Fit LMM with IDENTICAL formula as Step 2:
   - CTT_score ~ (time_linear + time_log) x domain + (time_linear | UID)
   - Fixed effects: same as IRT model
   - Random effects: MUST match IRT model structure (if IRT simplified to intercepts, CTT also uses intercepts)
   - Method: REML
4. Model selection MUST match Step 2:
   - If IRT model used random slopes: CTT also uses random slopes
   - If IRT model simplified to intercepts: CTT also uses intercepts
   - Ensures identical structure for fair comparison
5. Extract same outputs as Step 2

**Output:**

**File 1:** data/step03_ctt_lmm_fitted.pkl
**File 2:** results/step03_ctt_fixed_effects.csv (same structure as step02)
**File 3:** results/step03_ctt_random_effects.csv (same structure as step02)
**File 4:** results/step03_ctt_model_fit.csv (same structure as step02)
**File 5:** logs/step03_ctt_lmm_log.txt

**All files have identical structure to Step 2 outputs, substituting CTT for IRT.**

**Validation Requirement:**
Validation tools MUST be used after LMM fitting tool execution. Specific validation tools will be determined by rq_tools (likely validate_lmm_convergence, identical to Step 2).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- Same file existence checks as Step 2
- Same row/column counts as Step 2

*Value Ranges:*
- Fixed effects estimates: expect |estimate| < 2 for CTT scale (0-1 range, smaller than IRT)
- Standard errors: se > 0
- p_value in [0, 1]
- AIC, BIC > 0
- Convergence_status == "TRUE"

*Data Quality:*
- Same checks as Step 2
- CRITICAL: Random effects structure MUST match Step 2 (parallel models requirement)

*Log Validation:*
- Same patterns as Step 2
- CRITICAL CHECK: "Random effects structure: [X]" MUST match Step 2 log

**Expected Behavior on Validation Failure:**
- Same as Step 2
- Additional check: If CTT converges but IRT didn't (or vice versa), flag mismatch

---

### Step 4: Validate LMM Assumptions (Both Models)

**Dependencies:** Steps 2 and 3 (requires fitted IRT and CTT models)
**Complexity:** Low (diagnostic plotting and tests, <5 minutes)

**Purpose:** Comprehensive assumption checking for both LMMs to ensure valid inference

**Input:**

**File 1:** data/step02_irt_lmm_fitted.pkl (IRT model from Step 2)
**File 2:** data/step03_ctt_lmm_fitted.pkl (CTT model from Step 3)

**Processing:**

For EACH model (IRT and CTT), perform 6 assumption checks:

1. **Residual Normality:**
   - Extract residuals from fitted model
   - Generate Q-Q plot (quantile-quantile plot vs normal distribution)
   - Shapiro-Wilk test (H0: residuals normally distributed, p > 0.05 threshold)

2. **Homoscedasticity:**
   - Plot residuals vs fitted values
   - Visual inspection for constant variance (no funnel pattern)
   - No formal test (visual assessment sufficient per Gelman & Hill 2007)

3. **Random Effects Normality:**
   - Extract random intercepts (and slopes if used) per UID
   - Generate Q-Q plots for random effects
   - Shapiro-Wilk test for random effects (p > 0.05)

4. **Independence (Autocorrelation):**
   - Compute autocorrelation function (ACF) for residuals
   - Plot ACF with 95% confidence bands
   - Check Lag-1 ACF < 0.1 threshold (minimal autocorrelation for repeated measures)

5. **Outlier Detection:**
   - Identify observations with |residual| > 3 SD
   - Report count and percentage of outliers
   - Document outlier UIDs for inspection

6. **Multicollinearity (Fixed Effects):**
   - Compute Variance Inflation Factors (VIF) for fixed effects predictors
   - VIF < 10 threshold (no severe multicollinearity)

**Remedial Actions (if violations detected):**
- If EITHER model violates assumptions, apply SAME remediation to BOTH:
  - Robust standard errors (if heteroscedasticity detected)
  - AR(1) correlation structure (if autocorrelation detected, ACF > 0.1)
- Document all remedial actions in log
- Re-fit models with remediation if needed

**Output:**

**File 1:** plots/step04_irt_assumptions.png
**Format:** Multi-panel diagnostic plot (4 panels: Q-Q residuals, residuals vs fitted, Q-Q random effects, ACF)
**Dimensions:** 1200 x 1200 pixels @ 300 DPI

**File 2:** plots/step04_ctt_assumptions.png
**Format:** Same as File 1, for CTT model

**File 3:** results/step04_assumption_tests.csv
**Format:** CSV with test results
**Columns:**
  - model (string: IRT, CTT)
  - test (string: Shapiro-Wilk Residuals, Shapiro-Wilk Random Effects, ACF Lag-1, Outliers %, Max VIF)
  - value (float, test statistic or metric value)
  - p_value (float, p-value if applicable, NA for metrics)
  - threshold (float, decision threshold)
  - passes (bool, TRUE if assumption met)
**Expected Rows:** 10 (5 tests x 2 models)

**File 4:** logs/step04_assumption_report.txt
**Format:** Plain text summary
**Content:**
  - Which assumptions met/violated per model
  - Remedial actions applied (if any)
  - Comparison: Do both models show same assumption violations?

**Validation Requirement:**
Validation tools MUST be used after assumption validation tool execution. Specific validation tools will be determined by rq_tools (likely validate_lmm_assumptions_comprehensive to verify all 6 checks performed).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- plots/step04_irt_assumptions.png exists (diagnostic plots)
- plots/step04_ctt_assumptions.png exists
- results/step04_assumption_tests.csv: 10 rows x 6 columns

*Value Ranges:*
- p_value in [0, 1] (for Shapiro-Wilk tests)
- ACF Lag-1 in [-1, 1] (autocorrelation bounds)
- VIF >= 1 (always >= 1, severe if > 10)
- Outliers % in [0, 100]

*Data Quality:*
- All 5 tests present for BOTH models (10 rows total)
- No NaN in value column (all tests must run)
- passes column must be boolean (TRUE/FALSE)

*Log Validation:*
- Required pattern: "Assumption checks complete: IRT and CTT models"
- Required pattern: "Remedial actions: [none|robust SE|AR(1)|etc.]"
- Forbidden patterns: "Test failed to run", "Insufficient data for ACF"
- Acceptable warnings: "Assumption violated: [test name] (remediation applied)"

**Expected Behavior on Validation Failure:**
- Raise error if assumptions cannot be tested (e.g., model object corrupted)
- Log failure to logs/step04_assumptions.log
- Quit script immediately
- g_debug invoked (check fitted model integrity)

---

### Step 5: Compare LMM Significance Patterns

**Dependencies:** Steps 2 and 3 (requires fixed effects from both models)
**Complexity:** Low (table comparison, <5 minutes)

**Purpose:** Assess agreement on statistical significance for Time x Domain interaction terms

**Input:**

**File 1:** results/step02_irt_fixed_effects.csv (IRT model fixed effects)
**File 2:** results/step03_ctt_fixed_effects.csv (CTT model fixed effects)

**Processing:**

1. Extract interaction terms from both models:
   - time_linear:domainWhere
   - time_linear:domainWhen
   - time_log:domainWhere
   - time_log:domainWhen
   - (4 interaction terms per model)
2. For each term, classify significance:
   - Significant: p < 0.05
   - Non-significant: p >= 0.05
3. Create 2x2 contingency table:
   - Both Sig: IRT p < 0.05 AND CTT p < 0.05
   - Both Non-Sig: IRT p >= 0.05 AND CTT p >= 0.05
   - IRT Only: IRT p < 0.05 AND CTT p >= 0.05
   - CTT Only: IRT p >= 0.05 AND CTT p < 0.05
4. Compute agreement metrics:
   - Raw agreement %: (Both Sig + Both Non-Sig) / 4 x 100
   - Cohen's kappa: Chance-corrected agreement statistic (kappa > 0.60 = substantial agreement per Landis & Koch 1977)
5. Compare effect size magnitudes:
   - Compute beta_IRT / beta_CTT ratio for each term
   - Note: Ratios will vary due to scale differences (IRT unbounded, CTT 0-1), but signs should match
6. Identify discrepancies:
   - Terms where IRT and CTT disagree on significance
   - Terms where signs differ (serious construct validity issue if found)

**Output:**

**File 1:** results/step05_significance_agreement.csv
**Format:** CSV with agreement analysis
**Columns:**
  - term (string, interaction term name)
  - irt_estimate (float, IRT beta coefficient)
  - irt_p (float, IRT p-value)
  - irt_sig (bool, TRUE if p < 0.05)
  - ctt_estimate (float, CTT beta coefficient)
  - ctt_p (float, CTT p-value)
  - ctt_sig (bool, TRUE if p < 0.05)
  - agreement (string: Both Sig, Both Non-Sig, IRT Only, CTT Only)
  - estimate_ratio (float, irt_estimate / ctt_estimate)
**Expected Rows:** 4 (4 interaction terms)

**File 2:** results/step05_agreement_metrics.csv
**Format:** CSV with summary metrics
**Columns:**
  - metric (string: Raw Agreement %, Cohen's Kappa, Meets Kappa Threshold)
  - value (float or bool)
**Expected Rows:** 3

**File 3:** logs/step05_agreement_report.txt
**Format:** Plain text summary
**Content:**
  - Which terms show agreement vs discrepancy
  - Interpretation of Cohen's kappa (substantial/moderate/fair agreement)
  - Flag any sign discrepancies (critical if found)

**Validation Requirement:**
Validation tools MUST be used after agreement analysis tool execution. Specific validation tools will be determined by rq_tools (likely custom validation for agreement table format).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step05_significance_agreement.csv: 4 rows x 9 columns
- results/step05_agreement_metrics.csv: 3 rows x 2 columns

*Value Ranges:*
- irt_p, ctt_p in [0, 1]
- Cohen's Kappa in [-1, 1] (typically [0, 1] for agreement data)
- Raw Agreement % in [0, 100]
- estimate_ratio: no strict bounds, but expect positive ratios (same sign)

*Data Quality:*
- All 4 interaction terms present
- No NaN in agreement column (all terms must classify)
- agreement values in {Both Sig, Both Non-Sig, IRT Only, CTT Only}
- If estimate_ratio is negative: FLAG SERIOUS ISSUE (sign discrepancy)

*Log Validation:*
- Required pattern: "Agreement analysis complete: 4 terms compared"
- Required pattern: "Cohen's kappa = [value]"
- Forbidden patterns: "Sign discrepancy detected" (indicates construct validity failure)
- Acceptable warnings: "Low agreement for term [X] (investigate further)"

**Expected Behavior on Validation Failure:**
- Raise error if agreement cannot be computed (e.g., missing terms)
- Log failure to logs/step05_agreement.log
- Quit script immediately
- g_debug invoked

---

### Step 6: Compare Model Fit (AIC/BIC)

**Dependencies:** Steps 2 and 3 (requires fit indices from both models)
**Complexity:** Low (simple arithmetic comparison, <1 minute)

**Purpose:** Compare overall model fit between IRT and CTT LMMs

**Input:**

**File 1:** results/step02_irt_model_fit.csv (IRT model fit indices)
**File 2:** results/step03_ctt_model_fit.csv (CTT model fit indices)

**Processing:**

1. Extract AIC and BIC from both models
2. Compute differences:
   - DELTA_AIC = AIC_CTT - AIC_IRT (negative = IRT better, positive = CTT better)
   - DELTA_BIC = BIC_CTT - BIC_IRT
3. Interpret DELTA_AIC per Burnham & Anderson (2002):
   - |DELTA_AIC| < 2: Equivalent fit (no clear winner)
   - 2 <= |DELTA_AIC| < 10: Moderate difference (better model has some support)
   - |DELTA_AIC| >= 10: Substantial difference (better model strongly favored)
4. Apply same interpretation to DELTA_BIC
5. Document conclusion:
   - Which model fits better (or equivalent)?
   - Is difference meaningful (>10) or trivial (<2)?

**Output:**

**File 1:** results/step06_model_comparison.csv
**Format:** CSV with comparison results
**Columns:**
  - metric (string: AIC_IRT, AIC_CTT, DELTA_AIC, BIC_IRT, BIC_CTT, DELTA_BIC)
  - value (float)
**Expected Rows:** 6

**File 2:** results/step06_fit_interpretation.txt
**Format:** Plain text interpretation
**Content:**
  - DELTA_AIC interpretation (equivalent/moderate/substantial)
  - DELTA_BIC interpretation
  - Overall conclusion (which model preferred, or equivalent)
  - Theoretical implications (does psychometric optimization improve fit?)

**Validation Requirement:**
Validation tools MUST be used after model comparison tool execution. Specific validation tools will be determined by rq_tools (likely simple format validation for comparison table).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step06_model_comparison.csv: 6 rows x 2 columns

*Value Ranges:*
- AIC, BIC > 0 (fit indices always positive)
- DELTA values: no strict bounds (can be positive or negative)

*Data Quality:*
- All 6 metrics present
- No NaN values
- DELTA_AIC = AIC_CTT - AIC_IRT (verify arithmetic correct)

*Log Validation:*
- Required pattern: "Model comparison complete"
- Required pattern: "DELTA_AIC interpretation: [equivalent|moderate|substantial]"
- Forbidden patterns: "Negative AIC", "Undefined BIC"

**Expected Behavior on Validation Failure:**
- Raise error if fit indices missing or invalid
- Log failure to logs/step06_comparison.log
- Quit script immediately

---

### Step 7: Generate Comparison Plots

**Dependencies:** Steps 0, 2, 3 (requires paired data and model predictions)
**Complexity:** Low (plotting, <5 minutes)

**Purpose:** Visualize IRT vs CTT trajectories for each domain

**Input:**

**File 1:** data/step00_irt_ctt_paired.csv (observed data)
**File 2:** data/step02_irt_lmm_fitted.pkl (IRT model for predictions)
**File 3:** data/step03_ctt_lmm_fitted.pkl (CTT model for predictions)

**Processing:**

1. Generate model predictions:
   - Create prediction grid: TSVR_hours from 0 to 168 hours (7 days), 50 points
   - Predict IRT scores from IRT model across grid for each domain
   - Predict CTT scores from CTT model across grid for each domain
2. Compute observed means per domain x test:
   - Group data by domain and test
   - Compute mean IRT_score and mean CTT_score per group
   - Compute 95% CI for each mean
3. **Scale transformation for visual comparison:**
   - CTT scores (0-1) and IRT scores (-3 to +3) on different scales
   - Option 1: Dual y-axes (left = IRT, right = CTT)
   - Option 2: Z-score both scales (mean = 0, SD = 1)
   - Option 3: Leave raw scales, plot separately
   - Document which scaling used in plot metadata
4. Create comparison plots:
   - **Plot Type 1:** Three-panel plot (What, Where, When)
     - Each panel: TSVR_hours (x-axis), Ability (y-axis)
     - Solid line: IRT model predictions
     - Dashed line: CTT model predictions
     - Points with error bars: Observed means (IRT and CTT)
   - **Plot Type 2:** Scatterplots from Step 1 (IRT vs CTT, one per domain)
     - Already created in Step 1, reference here

**Output:**

**File 1:** plots/step07_comparison_trajectories.png
**Format:** PNG, three-panel plot (What, Where, When)
**Dimensions:** 1200 x 400 pixels @ 300 DPI
**Content:** IRT (solid) vs CTT (dashed) trajectories with observed means

**File 2:** plots/step07_scatterplots.png
**Format:** PNG, four-panel plot (What, Where, When, Overall)
**Dimensions:** 800 x 800 pixels @ 300 DPI
**Content:** IRT (x-axis) vs CTT (y-axis) scatterplots with regression lines (from Step 1 correlations)

**File 3:** plots/step07_plot_metadata.yaml
**Format:** YAML metadata
**Keys:**
  - scaling_method (string: dual_axes / z_score / raw)
  - irt_range (list: [min, max] observed IRT scores)
  - ctt_range (list: [min, max] observed CTT scores)
  - tsvr_range (list: [0, 168] hours plotted)
  - created_by (string: step07_generate_plots.py)

**Validation Requirement:**
Validation tools MUST be used after plotting tool execution. Specific validation tools will be determined by rq_tools (likely validate_plot_outputs for file existence and format checks).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- plots/step07_comparison_trajectories.png exists
- plots/step07_scatterplots.png exists
- plots/step07_plot_metadata.yaml exists

*Value Ranges:*
- irt_range: expect approximately [-2, 2] (typical range for ability estimates)
- ctt_range: [0, 1] (proportion correct bounds)
- tsvr_range: [0, 168] (hours, 0 = encoding, 168 = 1 week)

*Data Quality:*
- PNG files readable (not corrupted)
- Metadata YAML valid (parseable)
- Scaling method documented in metadata

*Log Validation:*
- Required pattern: "Plots generated: comparison_trajectories, scatterplots"
- Required pattern: "Scaling method applied: [method]"
- Forbidden patterns: "Plot generation failed", "Empty figure"

**Expected Behavior on Validation Failure:**
- Raise error if plots cannot be generated
- Log failure to logs/step07_plots.log
- Quit script immediately

---

## Expected Data Formats

### Data Transformations

**Step 0 -> Step 1:** No transformation (correlation uses long format directly)

**Step 0 -> Steps 2-3:** No transformation (LMM uses long format directly)

**Steps 2-3 -> Step 4:** Extract fitted model residuals and random effects for assumption checks

**Steps 2-3 -> Step 5:** Extract fixed effects tables for agreement analysis

**Steps 2-3 -> Step 7:** Generate model predictions across TSVR grid for plotting

### Column Naming Conventions

Per names.md registry (from RQ 5.1):

- **UID:** Participant identifier (no underscore, format: P###)
- **test:** Test session (T1, T2, T3, T4)
- **domain:** Memory domain factor (What, Where, When)
- **TSVR_hours:** Time Since VR in hours (actual elapsed time per Decision D070)
- **IRT_score:** IRT theta estimate (unbounded, typically -3 to +3)
- **CTT_score:** CTT mean accuracy score (0-1 range)

### Data Type Constraints

- **UID, test, domain:** Categorical (object dtype in pandas)
- **TSVR_hours, IRT_score, CTT_score:** Continuous (float64)
- **p_value, CI bounds:** Continuous (float64), constrained to [0, 1] or [-1, 1]
- **Boolean flags:** bool dtype (meets_r70, passes, irt_sig, ctt_sig)

---

## Cross-RQ Dependencies

### Dependency Type: DERIVED Data from RQ 5.1 (Dependencies Exist)

**This RQ requires outputs from:**

- **RQ 5.1** (Domain-Specific Forgetting Trajectories - IRT baseline)
  - File 1: results/ch5/rq1/data/step03_theta_scores.csv
    - Used in: Step 0 (IRT scores for comparison)
    - Rationale: RQ 5.1 establishes IRT theta estimates via GRM calibration (2-pass purified). This RQ uses those theta scores as one measurement approach.
  - File 2: results/ch5/rq1/data/step00_tsvr_mapping.csv
    - Used in: Step 0 (time variable for LMM per Decision D070)
    - Rationale: TSVR (actual hours since encoding) required for accurate temporal modeling. Same time variable used in RQ 5.1 LMM.
  - File 3: results/ch5/rq1/data/step02_purified_items.csv
    - Used in: Step 0 (identify which items to use for CTT computation)
    - Rationale: Fair comparison requires same item set for IRT and CTT. CTT computed from purified items only (not all raw items).

**Execution Order Constraint:**
1. RQ 5.1 must complete Steps 0-3 first (TSVR extraction, IRT Pass 1, purification, IRT Pass 2, theta extraction)
2. This RQ executes after RQ 5.1 completion (uses RQ 5.1 outputs)

**Data Source Boundaries (Per Best Practices):**
- **RAW data:** dfData.csv (raw VR item responses for CTT computation)
- **DERIVED data:** RQ 5.1 outputs (IRT theta scores, TSVR mapping, purified item list)
- **Scope:** This RQ does NOT re-calibrate IRT models (uses RQ 5.1 theta scores as fixed). This RQ DOES compute fresh CTT scores from raw data using purified item set.

**Validation:**
- Step 0: Check results/ch5/rq1/data/step03_theta_scores.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch5/rq1/data/step00_tsvr_mapping.csv exists
- Step 0: Check results/ch5/rq1/data/step02_purified_items.csv exists
- If ANY file missing -> quit with error -> user must execute RQ 5.1 first

**Reference:** Best practices code.md section 2 (Data Source Boundaries)

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

#### Step 0: Data Extraction
**Analysis Tool:** (determined by rq_tools - likely custom extraction from multiple sources)
**Validation Tool:** (determined by rq_tools - likely custom validation for paired format)
**What Validation Checks:** See Step 0 Substance Validation Criteria section above
**Expected Behavior on Failure:** Quit immediately, log error, invoke g_debug

#### Step 1: Correlation Analysis
**Analysis Tool:** (determined by rq_tools - likely scipy.stats.pearsonr or pandas.corr)
**Validation Tool:** (determined by rq_tools - likely validate_hypothesis_tests)
**What Validation Checks:** See Step 1 Substance Validation Criteria section above
**Expected Behavior on Failure:** Quit immediately, log error, invoke g_debug

#### Step 2: Fit IRT LMM
**Analysis Tool:** (determined by rq_tools - likely fit_lmm_trajectory_tsvr)
**Validation Tool:** (determined by rq_tools - likely validate_lmm_convergence)
**What Validation Checks:** See Step 2 Substance Validation Criteria section above
**Expected Behavior on Failure:** Quit immediately, log error, invoke g_debug

#### Step 3: Fit CTT LMM
**Analysis Tool:** (determined by rq_tools - likely fit_lmm_trajectory_tsvr)
**Validation Tool:** (determined by rq_tools - likely validate_lmm_convergence)
**What Validation Checks:** See Step 3 Substance Validation Criteria section above
**Expected Behavior on Failure:** Quit immediately, log error, invoke g_debug

#### Step 4: Validate LMM Assumptions (Both Models)
**Analysis Tool:** (determined by rq_tools - likely validate_lmm_assumptions_comprehensive)
**Validation Tool:** (determined by rq_tools - likely same tool validates its own outputs)
**What Validation Checks:** See Step 4 Substance Validation Criteria section above
**Expected Behavior on Failure:** Quit immediately, log error, invoke g_debug

#### Step 5: Compare Significance Patterns
**Analysis Tool:** (determined by rq_tools - likely custom agreement analysis function)
**Validation Tool:** (determined by rq_tools - likely custom validation for agreement table format)
**What Validation Checks:** See Step 5 Substance Validation Criteria section above
**Expected Behavior on Failure:** Quit immediately, log error, invoke g_debug

#### Step 6: Compare Model Fit
**Analysis Tool:** (determined by rq_tools - likely simple arithmetic function)
**Validation Tool:** (determined by rq_tools - likely simple format validation)
**What Validation Checks:** See Step 6 Substance Validation Criteria section above
**Expected Behavior on Failure:** Quit immediately, log error, invoke g_debug

#### Step 7: Generate Comparison Plots
**Analysis Tool:** (determined by rq_tools - likely matplotlib plotting functions)
**Validation Tool:** (determined by rq_tools - likely validate_plot_outputs)
**What Validation Checks:** See Step 7 Substance Validation Criteria section above
**Expected Behavior on Failure:** Quit immediately, log error, invoke g_debug

---

## Summary

**Total Steps:** 8 (Step 0: extraction + Steps 1-7: analysis)
**Estimated Runtime:** Medium (~20-40 minutes total)
  - Step 0: <5 min (data loading and merging)
  - Step 1: <5 min (correlation computation)
  - Step 2: 5-10 min (IRT LMM fitting)
  - Step 3: 5-10 min (CTT LMM fitting)
  - Step 4: <5 min (assumption checks)
  - Step 5: <5 min (agreement analysis)
  - Step 6: <1 min (fit comparison)
  - Step 7: <5 min (plotting)

**Cross-RQ Dependencies:** RQ 5.1 (3 files: theta_scores, tsvr_mapping, purified_items)

**Primary Outputs:**
- Correlation results (4 tests: What, Where, When, Overall) with dual p-values
- Parallel LMM results (IRT and CTT models with identical structure)
- Significance agreement metrics (raw % and Cohen's kappa)
- Model fit comparison (AIC/BIC differences)
- Comparison plots (trajectories and scatterplots)

**Validation Coverage:** 100% (all 8 steps have validation requirements with 4-layer substance criteria)

**Key Theoretical Question:**
Do IRT and CTT converge on same conclusions about domain-specific forgetting? High correlations (r > 0.70) and significance agreement (kappa > 0.60) support construct validity. Divergence indicates method-specific artifacts requiring careful interpretation.

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_*.py scripts

---

**Version History:**
- v1.0 (2025-11-26): Initial plan created by rq_planner agent
