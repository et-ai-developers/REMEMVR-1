# Analysis Plan: Age x Paradigm Interaction for Confidence Decline

**Research Question:** 6.4.3
**Created:** 2025-12-06
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ tests whether age moderates the relationship between retrieval paradigm (Free Recall, Cued Recall, Recognition) and confidence decline trajectories over the 6-day retention interval. Analysis uses IRT-derived confidence theta scores from RQ 6.4.1 (3-factor GRM calibration for IFR/ICR/IRE paradigms) merged with age data to test the 3-way Age x Paradigm x Time interaction via Linear Mixed Models.

**Pipeline:** LMM only (theta scores inherited from RQ 6.4.1, no IRT calibration in this RQ)

**Steps:** 5 total analysis steps (Step 0: data preparation + Steps 1-4: LMM analysis and comparison)

**Estimated Runtime:** Low-Medium (approximately 10-20 minutes total)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (Wald and LRT p-values for all hypothesis tests)
- Decision D070: TSVR as time variable (log-transformed hours since encoding, not nominal days)

**Theoretical Context:**
This RQ extends Chapter 5 accuracy findings (RQ 5.3.4: Age x Paradigm x Time interaction for accuracy) to the metacognitive domain. If age-invariant forgetting patterns observed for accuracy generalize to confidence, the 3-way interaction should be NULL. Alternative hypothesis: Older adults may show differential metacognitive monitoring across paradigm difficulty levels despite equivalent accuracy decline.

**Cross-RQ Dependencies:**
- RQ 6.4.1 (Paradigm Confidence Trajectories) - provides theta_confidence scores
- Chapter 5 RQ 5.3.4 (Age x Paradigm interaction for accuracy) - provides comparison benchmark

---

## Analysis Plan

### Step 0: Data Preparation

**Purpose:** Load confidence theta scores from RQ 6.4.1, merge with age data, prepare LMM input structure

**Dependencies:** None (first step, but requires RQ 6.4.1 completion)

**Complexity:** Low (<5 minutes)

**Input:**

**File 1:** results/ch6/6.4.1/data/step03_theta_confidence_paradigm.csv
**Source:** RQ 6.4.1 Step 3 (IRT Pass 2 theta extraction)
**Format:** CSV with columns:
  - composite_ID (string, format: UID_test, e.g., "P001_T1")
  - Paradigm (string, values: IFR, ICR, IRE)
  - test (string, values: T1, T2, T3, T4)
  - TSVR_hours (float, actual hours since encoding)
  - log_TSVR (float, log-transformed TSVR per Decision D070)
  - theta_confidence (float, IRT ability estimate for confidence)
  - se_confidence (float, standard error of theta estimate)
**Expected Rows:** 1200 (100 participants x 4 tests x 3 paradigms)
**Note:** Time transformation (log_TSVR) already applied in RQ 6.4.1

**File 2:** data/cache/dfData.csv
**Source:** Master data cache (participant-level demographics)
**Format:** CSV with columns including:
  - UID (string, participant identifier, format: P###)
  - Age (int, participant age in years at enrollment)
**Expected Rows:** 100 participants

**Processing:**

1. **Load confidence theta scores:**
   - Read results/ch6/6.4.1/data/step03_theta_confidence_paradigm.csv
   - Verify expected structure: 1200 rows, required columns present
   - Extract UID from composite_ID (split on underscore: "P001_T1" -> "P001")

2. **Load age data:**
   - Read data/cache/dfData.csv
   - Extract Age column by UID
   - Verify no missing age values (all 100 participants have age)

3. **Merge datasets:**
   - Left join: theta data + age data on UID
   - Verify merge success: all 1200 rows have valid Age (no NaN)

4. **Center age variable:**
   - Compute grand mean: Age_mean = mean(Age across all participants)
   - Create Age_c = Age - Age_mean (mean-centered age for LMM)
   - Verify centering: mean(Age_c) approximately 0 (within rounding error)

5. **Structure LMM input:**
   - Final columns: UID, Age, Age_c, Paradigm, test, TSVR_hours, log_TSVR, theta_confidence, se_confidence
   - Sort by UID, then Paradigm, then test (facilitates inspection)
   - Save to data/step00_lmm_input.csv

**Output:**

**File:** data/step00_lmm_input.csv
**Format:** CSV, long format (one row per observation)
**Columns:**
  - UID (string): Participant identifier
  - Age (int): Participant age in years (raw, uncentered)
  - Age_c (float): Mean-centered age (Age - grand mean)
  - Paradigm (string): Retrieval paradigm (IFR, ICR, IRE)
  - test (string): Test session (T1, T2, T3, T4)
  - TSVR_hours (float): Actual hours since encoding
  - log_TSVR (float): Log-transformed TSVR (time variable for LMM)
  - theta_confidence (float): IRT confidence ability estimate
  - se_confidence (float): Standard error of theta estimate
**Expected Rows:** 1200 (100 participants x 4 tests x 3 paradigms)
**Expected Dimensions:** 1200 rows x 9 columns

**Validation Requirement:**
Validation tools MUST be used after data preparation tool execution. Specific validation tools will be determined by rq_tools based on data merging and transformation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_lmm_input.csv exists (exact path)
- Expected rows: 1200 (100 participants x 4 tests x 3 paradigms)
- Expected columns: 9 (UID, Age, Age_c, Paradigm, test, TSVR_hours, log_TSVR, theta_confidence, se_confidence)
- Data types: UID (string), Age (int), Age_c (float), Paradigm (string), test (string), TSVR_hours (float), log_TSVR (float), theta_confidence (float), se_confidence (float)

*Value Ranges:*
- Age in [18, 90] years (typical REMEMVR sample range)
- Age_c in [-40, 40] (centered on grand mean, expect approximately +/- 2SD)
- Age_c mean approximately 0 (within 0.01 tolerance for rounding)
- Paradigm in {IFR, ICR, IRE} (categorical, exactly 3 levels)
- test in {T1, T2, T3, T4} (categorical, exactly 4 levels)
- TSVR_hours in [0, 168] hours (0=encoding, 168=1 week maximum)
- log_TSVR in [-5, 6] (log scale, expect approximately 0 to 5)
- theta_confidence in [-3, 3] (typical IRT ability range)
- se_confidence in [0.1, 1.5] (standard errors, above 1.5 suggests unreliable estimates)

*Data Quality:*
- No NaN values allowed in any column (merge must be complete)
- Expected N: Exactly 1200 rows (no data loss from merge)
- No duplicate composite_ID values (UID x test x Paradigm combinations unique)
- All 100 unique UIDs present (no participant dropout)
- Each UID has exactly 12 rows (4 tests x 3 paradigms)
- Paradigm distribution: exactly 400 rows per paradigm (IFR=400, ICR=400, IRE=400)
- Test distribution: exactly 300 rows per test (T1=300, T2=300, T3=300, T4=300)

*Log Validation:*
- Required pattern: "Data preparation complete: 1200 rows created"
- Required pattern: "Age centering successful: mean(Age_c) = 0.000"
- Required pattern: "All participants present: 100 unique UIDs"
- Forbidden patterns: "ERROR", "NaN values detected", "Merge failed", "Missing age data"
- Acceptable warnings: None expected for data preparation step

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 1200 rows, found 1150 - merge incomplete")
- Log failure to logs/step00_prepare_lmm_input.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause (likely merge key mismatch or missing RQ 6.4.1 outputs)

---

### Step 1: Fit LMM with 3-Way Interaction

**Purpose:** Fit Linear Mixed Model testing Age x Paradigm x Time 3-way interaction for confidence decline

**Dependencies:** Step 0 (requires prepared LMM input)

**Complexity:** Medium (5-15 minutes, depending on convergence)

**Input:**

**File:** data/step00_lmm_input.csv
**Source:** Generated by Step 0
**Format:** Long format LMM input (1200 rows x 9 columns)
**Required Columns:** UID, Age_c, Paradigm, log_TSVR, theta_confidence

**Processing:**

**LMM Model Specification:**

**Formula:**
```
theta_confidence ~ log_TSVR * Paradigm * Age_c + (log_TSVR | UID)
```

**Fixed Effects:**
- log_TSVR (time main effect: confidence decline over retention interval)
- Paradigm (paradigm main effect: baseline confidence differences across IFR/ICR/IRE)
- Age_c (age main effect: baseline confidence differences by age)
- log_TSVR x Paradigm (2-way interaction: paradigm-specific decline rates)
- log_TSVR x Age_c (2-way interaction: age-specific decline rates)
- Paradigm x Age_c (2-way interaction: age differences in baseline by paradigm)
- log_TSVR x Paradigm x Age_c (3-way interaction: PRIMARY TEST - does age moderate paradigm-specific decline)

**Random Effects:**
- Random intercepts by UID (participant-specific baseline confidence)
- Random slopes for log_TSVR by UID (participant-specific decline rates)
- Unstructured covariance (allows intercept-slope correlation)

**Estimation Method:** REML = True (Restricted Maximum Likelihood for unbiased variance component estimation)

**Model Fitting:**
1. Prepare data with proper categorical encoding (Paradigm: IFR as reference level)
2. Fit model using statsmodels MixedLM
3. Check convergence status (model.converged = True)
4. Extract full model summary (fixed effects table, random effects variance components)
5. Save model summary to data/step01_lmm_model_summary.txt

**Output:**

**File:** data/step01_lmm_model_summary.txt
**Format:** Plain text, statsmodels summary output
**Contents:**
- Fixed effects table: coefficients, SE, z-values, p-values for all 8 effects (3 main + 3 two-way + 1 three-way)
- Random effects: variance components for intercepts and slopes
- Model fit indices: log-likelihood, AIC, BIC
- Convergence status

**Validation Requirement:**
Validation tools MUST be used after LMM fitting tool execution. Specific validation tools will be determined by rq_tools based on LMM convergence and assumption requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_lmm_model_summary.txt exists (exact path)
- File size > 1KB (non-empty summary)

*Value Ranges:*
- Fixed effect coefficients: no extreme values (expect range approximately [-2, 2] for centered predictors)
- Standard errors: all SE > 0 (negative SE indicates estimation failure)
- Z-values: computed correctly (coefficient / SE)
- P-values: all in [0, 1] range
- Random effect variances: all > 0 (negative variance impossible)
- Log-likelihood: negative value (typical for MLE)
- AIC/BIC: finite positive values (not NaN or inf)

*Data Quality:*
- Model converged = True (convergence flag must be set)
- No singularity warnings (perfect multicollinearity would cause singularity)
- All 8 fixed effects estimated (no missing terms from formula)
- Random effects present for both intercepts and slopes
- Observations used = 1200 (no data loss during fitting)
- Groups (UIDs) = 100 (all participants included)

*Log Validation:*
- Required pattern: "Model converged: True"
- Required pattern: "Fixed effects: 8 terms estimated"
- Required pattern: "Random effects: intercepts and slopes"
- Required pattern: "Observations: 1200, Groups: 100"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "Singular", "Non-positive definite"
- Acceptable warnings: "ConvergenceWarning" if model still converges (common for complex random structures)

**Expected Behavior on Validation Failure:**
- If convergence fails: Log warning, save partial summary, proceed to g_debug with recommendation to simplify random structure
- If singularity detected: Quit with error, recommend random intercepts only (no slopes)
- If estimation errors: Quit with error, check for perfect multicollinearity or insufficient data

---

### Step 2: Extract Interaction Terms with Dual P-Values

**Purpose:** Extract Age_c main effect, Age_c x Time 2-way interaction, and Age_c x Paradigm x Time 3-way interaction with dual p-value reporting (Decision D068)

**Dependencies:** Step 1 (requires fitted LMM model)

**Complexity:** Low (<5 minutes, extraction from fitted model)

**Input:**

**File:** data/step01_lmm_model_summary.txt
**Source:** Generated by Step 1
**Format:** Statsmodels summary text
**Note:** Python script will re-load fitted model object (not parse text file) to extract statistics

**Processing:**

**Extract 3 Critical Terms:**

1. **Age_c Main Effect:**
   - Term: "Age_c" (baseline age effect on confidence, averaged across paradigms and time)
   - Extract: coefficient, SE, Wald z-value, Wald p-value
   - Compute LRT p-value: Fit reduced model without Age_c, compare via likelihood ratio test
   - Bonferroni correction: alpha = 0.0167 (0.05 / 3 tests)

2. **Age_c x Time 2-Way Interaction:**
   - Term: "log_TSVR:Age_c" (does age affect confidence decline rate, averaged across paradigms)
   - Extract: coefficient, SE, Wald z-value, Wald p-value
   - Compute LRT p-value: Fit reduced model without log_TSVR:Age_c, compare via LRT
   - Bonferroni correction: alpha = 0.0167

3. **Age_c x Paradigm x Time 3-Way Interaction (PRIMARY TEST):**
   - Terms: "log_TSVR:Paradigm[ICR]:Age_c" and "log_TSVR:Paradigm[IRE]:Age_c" (2 dummy codes for 3-level Paradigm)
   - Extract: coefficients, SEs, Wald z-values, Wald p-values for both terms
   - Compute omnibus Wald test: Joint test of both 3-way terms (chi-square, df=2)
   - Compute omnibus LRT: Fit reduced model without both 3-way terms, compare via LRT (chi-square, df=2)
   - Bonferroni correction: alpha = 0.0167

**Dual P-Value Reporting (Decision D068):**
- Report BOTH Wald and LRT p-values for all 3 tests
- Include uncorrected p-values AND Bonferroni-corrected decision (reject if p < 0.0167)
- Rationale: Exploratory thesis context, transparent reporting of both test types

**Output:**

**File:** data/step02_interaction_terms.csv
**Format:** CSV with dual p-values
**Columns:**
  - term (string): Effect name (Age_c, Age_c:log_TSVR, Age_c:log_TSVR:Paradigm)
  - coef (float): Coefficient estimate
  - se (float): Standard error
  - z_wald (float): Wald z-value
  - p_wald_uncorrected (float): Wald p-value (uncorrected)
  - p_wald_bonferroni (float): Wald p-value with Bonferroni correction (p * 3)
  - chi2_lrt (float): LRT chi-square statistic
  - df_lrt (int): LRT degrees of freedom
  - p_lrt_uncorrected (float): LRT p-value (uncorrected)
  - p_lrt_bonferroni (float): LRT p-value with Bonferroni correction (p * 3)
  - significant_bonferroni (bool): True if p_bonferroni < 0.05 (after correction)
**Expected Rows:** 3 (Age_c main, Age_c:log_TSVR 2-way, Age_c:log_TSVR:Paradigm 3-way omnibus)

**Note:** For 3-way interaction, coef/se/z_wald represent omnibus test (joint test of ICR and IRE terms), not individual dummy codes. Individual dummy coefficients saved separately for interpretation if interaction significant.

**Validation Requirement:**
Validation tools MUST be used after hypothesis testing extraction tool execution. Specific validation tools will be determined by rq_tools based on dual p-value reporting requirements (Decision D068).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_interaction_terms.csv exists (exact path)
- Expected rows: 3 (Age_c main, Age_c:Time 2-way, Age_c:Paradigm:Time 3-way)
- Expected columns: 11 (term, coef, se, z_wald, p_wald_uncorrected, p_wald_bonferroni, chi2_lrt, df_lrt, p_lrt_uncorrected, p_lrt_bonferroni, significant_bonferroni)
- Data types: term (string), coef (float), se (float), z_wald (float), p_wald_uncorrected (float), p_wald_bonferroni (float), chi2_lrt (float), df_lrt (int), p_lrt_uncorrected (float), p_lrt_bonferroni (float), significant_bonferroni (bool)

*Value Ranges:*
- coef: unbounded (expect approximately [-2, 2] for centered predictors)
- se: all > 0 (negative SE impossible)
- z_wald: unbounded (expect approximately [-5, 5] for typical effects)
- p_wald_uncorrected in [0, 1]
- p_wald_bonferroni in [0, 3] (correction can push above 1, clipped at 1 for reporting)
- chi2_lrt > 0 (chi-square statistic always positive)
- df_lrt in {1, 2} (1 for main/2-way, 2 for 3-way omnibus)
- p_lrt_uncorrected in [0, 1]
- p_lrt_bonferroni in [0, 3]

*Data Quality:*
- No NaN values in p-value columns (all tests must execute successfully)
- All 3 terms present: exactly 1 row with "Age_c", 1 row with "Age_c:log_TSVR", 1 row with "Age_c:log_TSVR:Paradigm"
- Bonferroni correction factor = 3 (verify p_bonferroni = p_uncorrected * 3, clipped at 1)
- significant_bonferroni consistent with p_bonferroni < 0.05

*Log Validation:*
- Required pattern: "Dual p-values computed: Wald and LRT"
- Required pattern: "Bonferroni correction applied: alpha = 0.0167"
- Required pattern: "3 terms extracted: Age_c, Age_c:log_TSVR, Age_c:log_TSVR:Paradigm"
- Forbidden patterns: "ERROR", "NaN p-value", "Missing term", "LRT failed"
- Acceptable warnings: "LRT convergence slow" (acceptable if LRT completes successfully)

**Expected Behavior on Validation Failure:**
- If LRT fails to converge: Log warning, use Wald p-values only, set LRT columns to NaN
- If Wald test missing: Quit with error, check model summary for term presence
- If Bonferroni correction incorrect: Quit with error, verify correction factor = 3

---

### Step 3: Compute Effect Sizes

**Purpose:** Compute Cohen's f-squared effect sizes for Age_c terms to quantify practical significance

**Dependencies:** Step 1 (requires fitted LMM model)

**Complexity:** Low (<5 minutes)

**Input:**

**File:** Fitted LMM model object from Step 1 (re-loaded from Python environment, not from text file)

**Processing:**

**Effect Size Computation:**

1. **Cohen's f-squared for fixed effects:**
   - Formula: f^2 = R^2_partial / (1 - R^2_partial)
   - Compute R^2_partial for each Age_c term by comparing full model vs reduced model (without term)
   - For 3-way interaction: Compare full model vs model without both Age_c:log_TSVR:Paradigm[ICR] and Age_c:log_TSVR:Paradigm[IRE] terms

2. **Interpretation thresholds (Cohen, 1988):**
   - f^2 = 0.02: Small effect
   - f^2 = 0.15: Medium effect
   - f^2 = 0.35: Large effect

**Output:**

**File:** data/step03_effect_sizes.csv
**Format:** CSV
**Columns:**
  - term (string): Effect name
  - f_squared (float): Cohen's f-squared effect size
  - interpretation (string): "negligible", "small", "medium", "large"
**Expected Rows:** 3 (Age_c main, Age_c:log_TSVR, Age_c:log_TSVR:Paradigm)

**Validation Requirement:**
Validation tools MUST be used after effect size computation tool execution. Specific validation tools will be determined by rq_tools based on effect size range requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_effect_sizes.csv exists (exact path)
- Expected rows: 3
- Expected columns: 3 (term, f_squared, interpretation)

*Value Ranges:*
- f_squared >= 0 (effect sizes cannot be negative)
- f_squared typically < 1.0 (values > 1.0 suggest very large effects, rare in observational data)
- interpretation in {"negligible", "small", "medium", "large"} (categorical)

*Data Quality:*
- No NaN values (all effect sizes must compute successfully)
- All 3 terms present
- interpretation consistent with f_squared thresholds (e.g., f^2 = 0.10 -> "small")

*Log Validation:*
- Required pattern: "Effect sizes computed: 3 terms"
- Forbidden patterns: "ERROR", "Negative f-squared", "NaN effect size"

**Expected Behavior on Validation Failure:**
- If negative f-squared: Quit with error (indicates model comparison error)
- If NaN effect size: Quit with error, check reduced model convergence

---

### Step 4: Compare to Chapter 5 RQ 5.3.4 Results

**Purpose:** Compare Ch6 confidence interaction results to Ch5 accuracy interaction results to test generalization hypothesis

**Dependencies:** Step 2 (requires Ch6 interaction terms), external dependency on Ch5 5.3.4 completion

**Complexity:** Low (<5 minutes, data loading and comparison table creation)

**Input:**

**File 1:** data/step02_interaction_terms.csv
**Source:** Generated by Step 2 (this RQ)
**Format:** Ch6 confidence interaction terms with dual p-values

**File 2:** results/ch5/5.3.4/data/step02_interaction_terms.csv (or equivalent)
**Source:** Chapter 5 RQ 5.3.4 (Age x Paradigm interaction for accuracy)
**Format:** Ch5 accuracy interaction terms with dual p-values
**Note:** Exact file path may vary depending on Ch5 5.3.4 structure - adapt as needed

**Processing:**

**Comparison Table Creation:**

1. **Load both datasets:**
   - Ch6 confidence: data/step02_interaction_terms.csv
   - Ch5 accuracy: results/ch5/5.3.4/data/step02_interaction_terms.csv

2. **Align terms:**
   - Match Age_c main effect (Ch5 vs Ch6)
   - Match Age_c x Time 2-way interaction (Ch5 vs Ch6)
   - Match Age_c x Paradigm x Time 3-way interaction (Ch5 vs Ch6)

3. **Create comparison table:**
   - Columns: term, domain (Accuracy/Confidence), p_wald_bonferroni, p_lrt_bonferroni, significant_bonferroni, interpretation
   - Interpretation logic:
     - Both NULL (p > 0.0167): "Consistent age-invariance across accuracy and confidence"
     - Both significant (p < 0.0167): "Consistent age effects across accuracy and confidence"
     - Divergent (one NULL, one significant): "Dissociation between accuracy and confidence"

**Output:**

**File:** data/step04_ch5_comparison.csv
**Format:** CSV
**Columns:**
  - term (string): Effect name
  - domain (string): "Accuracy" or "Confidence"
  - p_wald_bonferroni (float): Wald p-value with Bonferroni correction
  - p_lrt_bonferroni (float): LRT p-value with Bonferroni correction
  - significant_bonferroni (bool): True if p < 0.05 after correction
  - interpretation (string): Consistency assessment
**Expected Rows:** 6 (3 terms x 2 domains)

**Note:** If Ch5 5.3.4 file not found or has different structure, create comparison table with Ch6 results only and document "Ch5 comparison pending RQ 5.3.4 completion" in interpretation column.

**Validation Requirement:**
Validation tools MUST be used after comparison table creation tool execution. Specific validation tools will be determined by rq_tools based on data merging requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_ch5_comparison.csv exists (exact path)
- Expected rows: 6 (3 terms x 2 domains) if Ch5 data available, 3 rows if Ch5 pending
- Expected columns: 6 (term, domain, p_wald_bonferroni, p_lrt_bonferroni, significant_bonferroni, interpretation)

*Value Ranges:*
- p_wald_bonferroni in [0, 3] (correction can push above 1, clipped at 1)
- p_lrt_bonferroni in [0, 3]
- domain in {"Accuracy", "Confidence"}
- interpretation: free text (consistency assessment)

*Data Quality:*
- No NaN values in p-value columns (unless Ch5 data unavailable)
- All 3 terms present for Confidence domain
- If Ch5 data available: All 3 terms present for Accuracy domain
- significant_bonferroni consistent with p-values

*Log Validation:*
- Required pattern: "Comparison table created: Ch5 Accuracy vs Ch6 Confidence"
- If Ch5 unavailable: Acceptable pattern: "Ch5 data not found - comparison pending"
- Forbidden patterns: "ERROR", "Merge failed"

**Expected Behavior on Validation Failure:**
- If Ch5 file missing: Log warning, create comparison table with Ch6 only, document pending comparison
- If file structure mismatch: Log warning, attempt manual alignment, document assumptions

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs - intermediate and final)

- data/step00_lmm_input.csv (Step 0: LMM input preparation - 1200 rows, 9 columns)
- data/step01_lmm_model_summary.txt (Step 1: Fitted LMM model summary)
- data/step02_interaction_terms.csv (Step 2: Age_c terms with dual p-values - 3 rows)
- data/step03_effect_sizes.csv (Step 3: Cohen's f-squared effect sizes - 3 rows)
- data/step04_ch5_comparison.csv (Step 4: Ch5 accuracy vs Ch6 confidence comparison - 6 rows)

### Logs (ONLY execution logs - .log files capturing stdout/stderr)

- logs/step00_prepare_lmm_input.log (Step 0: data preparation execution log)
- logs/step01_fit_lmm_3way.log (Step 1: LMM fitting execution log)
- logs/step02_extract_interaction_terms.log (Step 2: hypothesis testing execution log)
- logs/step03_compute_effect_sizes.log (Step 3: effect size computation execution log)
- logs/step04_compare_to_ch5.log (Step 4: cross-chapter comparison execution log)

### Plots (EMPTY until rq_plots runs)

No plots generated during analysis steps. Visualization (if needed) will be handled by rq_plots agent in later workflow step.

### Results (EMPTY until rq_results runs)

No summary files generated during analysis steps. Final interpretation and summary will be created by rq_results agent.

---

## Expected Data Formats

### Step 0: Data Preparation

**Input Format (RQ 6.4.1 theta scores):**
- File: results/ch6/6.4.1/data/step03_theta_confidence_paradigm.csv
- Format: Long format (one row per observation)
- Key columns: composite_ID, Paradigm, test, log_TSVR, theta_confidence

**Input Format (Age data):**
- File: data/cache/dfData.csv
- Format: One row per participant
- Key columns: UID, Age

**Merge Logic:**
- Extract UID from composite_ID (split on underscore)
- Left join theta data + age data on UID
- Verify no missing Age values after merge

**Output Format:**
- File: data/step00_lmm_input.csv
- Format: Long format (1200 rows x 9 columns)
- Sorting: UID, Paradigm, test (ascending)

### Step 1-4: LMM Analysis

**Data Transformations:**
No major transformations after Step 0. Steps 1-4 operate on data/step00_lmm_input.csv structure.

**Column Naming Conventions:**
- Age_c: Mean-centered age (NOT Age_centered, NOT age_c)
- log_TSVR: Log-transformed TSVR (NOT log_tsvr, NOT logTSVR)
- theta_confidence: Confidence ability estimate (NOT theta_conf, NOT confidence_theta)
- Paradigm: IFR/ICR/IRE (NOT paradigm, NOT Paradigm_type)

All column names follow conventions from names.md and RQ 6.4.1 upstream source.

---

## Cross-RQ Dependencies

**This RQ depends on:**

**RQ 6.4.1 (Paradigm Confidence Trajectories):**
- File required: results/ch6/6.4.1/data/step03_theta_confidence_paradigm.csv
- Content: IRT-derived confidence theta scores by paradigm (IFR/ICR/IRE) with time transformation (log_TSVR)
- Usage: Primary dependent variable for LMM analysis
- Status check: Verify RQ 6.4.1 status.yaml shows rq_results: success before running this RQ
- If missing: QUIT with error "RQ 6.4.1 must complete before RQ 6.4.3 (dependency)"

**Chapter 5 RQ 5.3.4 (Age x Paradigm interaction for accuracy):**
- File required: results/ch5/5.3.4/data/step02_interaction_terms.csv (or equivalent)
- Content: Age x Paradigm x Time interaction results for accuracy domain
- Usage: Comparison benchmark for Step 4 (test generalization hypothesis)
- Status check: Verify RQ 5.3.4 completion (if available) before Step 4
- If missing: Proceed with Step 4 creating comparison table with Ch6 only, document "Ch5 comparison pending"

**Execution Order Constraint:**
1. RQ 6.4.1 MUST complete fully (Steps 0-3) before this RQ begins
2. RQ 5.3.4 completion recommended but not required (Step 4 can defer comparison if Ch5 not ready)

**Data Source Boundaries:**
- DERIVED data only: No direct extraction from master.xlsx in this RQ
- All inputs come from RQ 6.4.1 theta scores + dfData.csv age variable
- No IRT calibration in this RQ (inherited from RQ 6.4.1)

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
- rq_tools: MUST specify validation tool for EVERY analysis step (no exceptions)
- rq_analysis: MUST embed validation tool call for EVERY analysis step (no exceptions)
- g_code: MUST generate code with validation function calls (no exceptions)
- rq_inspect: MUST verify validation ran successfully (checks logs/stepN_name.log for validation output)

### Validation Requirements By Step

#### Step 0: Data Preparation

**Analysis Tool:** (determined by rq_tools - likely custom data merging function)
**Validation Tool:** (determined by rq_tools - likely validate_dataframe_structure + validate_standardization for Age_c)

**What Validation Checks:**
- Output file exists (data/step00_lmm_input.csv)
- Expected row count (1200 rows)
- Expected column count (9 columns)
- No NaN values in any column (complete merge)
- Age_c properly centered (mean approximately 0)
- All 100 unique UIDs present
- Paradigm and test distributions correct (balanced design)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step00_prepare_lmm_input.log
- Quit immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose merge issues

---

#### Step 1: LMM Fitting

**Analysis Tool:** (determined by rq_tools - likely fit_lmm_trajectory_tsvr)
**Validation Tool:** (determined by rq_tools - likely validate_lmm_convergence + validate_model_convergence)

**What Validation Checks:**
- Model converged successfully (model.converged = True)
- No singularity warnings
- All 8 fixed effects estimated (no missing terms)
- Random effects variance components > 0
- Expected observations (1200) and groups (100)

**Expected Behavior on Validation Failure:**
- If convergence fails: Log warning, proceed to g_debug with recommendation to simplify random structure
- If singularity: Quit with error, recommend random intercepts only
- Log failure to logs/step01_fit_lmm_3way.log

---

#### Step 2: Hypothesis Testing Extraction

**Analysis Tool:** (determined by rq_tools - likely custom extraction function)
**Validation Tool:** (determined by rq_tools - likely validate_hypothesis_test_dual_pvalues per Decision D068)

**What Validation Checks:**
- All 3 terms extracted (Age_c main, Age_c:Time, Age_c:Paradigm:Time)
- Dual p-values present (Wald and LRT)
- Bonferroni correction applied correctly (factor = 3)
- No NaN p-values

**Expected Behavior on Validation Failure:**
- If LRT fails: Log warning, use Wald only, set LRT columns to NaN
- If term missing: Quit with error
- Log failure to logs/step02_extract_interaction_terms.log

---

#### Step 3: Effect Size Computation

**Analysis Tool:** (determined by rq_tools - likely compute_effect_sizes_cohens or custom f-squared function)
**Validation Tool:** (determined by rq_tools - likely validate_effect_sizes)

**What Validation Checks:**
- All 3 effect sizes computed (no NaN)
- f-squared values >= 0 (non-negative)
- Interpretation consistent with thresholds

**Expected Behavior on Validation Failure:**
- If negative f-squared: Quit with error (model comparison error)
- Log failure to logs/step03_compute_effect_sizes.log

---

#### Step 4: Cross-Chapter Comparison

**Analysis Tool:** (determined by rq_tools - likely custom comparison table function)
**Validation Tool:** (determined by rq_tools - likely validate_dataframe_structure)

**What Validation Checks:**
- Comparison table created (6 rows if Ch5 available, 3 if pending)
- All required columns present
- No NaN in p-value columns (unless Ch5 unavailable)

**Expected Behavior on Validation Failure:**
- If Ch5 file missing: Log warning, create Ch6-only table, document pending
- If structure mismatch: Log warning, document assumptions
- Log to logs/step04_compare_to_ch5.log

---

## Notes

**Naming Conventions:**

All file naming follows conventions established in docs/v4/names.md:
- Step numbers: step00, step01, step02, step03, step04 (zero-padded for sorting)
- Data files: data/stepNN_<description>.csv pattern
- Log files: logs/stepNN_<description>.log pattern
- Variable names: Age_c (centered), log_TSVR (transformed time), theta_confidence (ability estimate)

**Validation Philosophy:**

Per-step validation ensures errors caught at source, not 5 steps later. Every step has explicit validation requirements embedded in 2_plan.md, specified in 3_tools.yaml by rq_tools, and executed in stepNN_name.py scripts generated by g_code.

**Tool Selection:**

rq_tools agent reads this plan and specifies exact tools from tool_inventory.md. This plan documents WHAT analyses are needed (LMM with 3-way interaction, dual p-value extraction, effect sizes) at method-specific level, not function-specific level. Tool selection is rq_tools' responsibility.

**Code Generation:**

g_code agent generates Python scripts per rq_analysis instructions based on this plan. Scripts will implement the processing logic documented in each step, call appropriate analysis tools from tools/ modules, and embed validation function calls as specified by rq_tools in 3_tools.yaml.

**Theoretical Context:**

This RQ tests a critical hypothesis: Does the age-invariant forgetting pattern observed for accuracy (Ch5 RQ 5.3.4 found NULL Age x Paradigm x Time interaction) generalize to metacognitive confidence? If yes, the 3-way interaction should be NULL for confidence. If no, older adults may show differential metacognitive monitoring across paradigm difficulty levels (e.g., more conservative in Free Recall, more liberal in Recognition) despite equivalent accuracy decline. The cross-chapter comparison (Step 4) provides direct empirical test of this generalization hypothesis.

---

**End of Analysis Plan**
