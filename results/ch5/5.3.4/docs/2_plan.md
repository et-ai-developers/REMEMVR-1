# Analysis Plan: RQ 5.3.4 - Age x Paradigm Interactions

**Research Question:** 5.3.4
**Created:** 2025-12-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines whether age-related differences in forgetting rates vary systematically across three retrieval paradigms differing in retrieval support: Free Recall (IFR - unsupported), Cued Recall (ICR - cued), and Recognition (IRE - recognition). The analysis tests a 3-way Age x Paradigm x Time interaction to determine if older adults show disproportionately greater deficits in self-initiated retrieval (Free Recall) compared to supported retrieval (Cued Recall, Recognition), consistent with hippocampal aging effects on recollection-dependent processes.

**Pipeline:** LMM only (uses DERIVED theta scores from RQ 5.3.1)

**Steps:** 6 analysis steps (Step 0: data loading -> Step 5: plot data preparation)

**Estimated Runtime:** Low-Medium (total ~15-25 minutes: data preparation 5-10 min, LMM fitting 5-10 min, post-hoc contrasts 5 min)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni) for interaction terms and post-hoc contrasts
- Decision D070: TSVR (actual hours since encoding) as time variable, not nominal days
- Convergence Contingency: Likelihood ratio test (LRT) to select random structure if full model fails to converge (per Bates et al. 2015)

**Data Dependencies:**
- RQ 5.3.1 outputs (theta scores for 3 paradigms: IFR, ICR, IRE)
- dfData.csv (Age variable)

---

## Analysis Plan

### Step 0: Load Theta Scores and Age Data

**Dependencies:** RQ 5.3.1 must complete through Step 3 (theta extraction)

**Complexity:** Low (5 minutes - data loading and merging only)

**Purpose:** Load paradigm-specific theta scores from RQ 5.3.1 and merge with participant Age from dfData.csv

**Input:**

**File 1:** results/ch5/5.3.1/data/step03_theta_scores.csv
**Source:** RQ 5.3.1 IRT calibration outputs
**Format:** CSV with columns:
  - `composite_ID` (string, format: UID_test_paradigm, e.g., P001_T1_IFR)
  - `theta` (float, IRT ability estimate for paradigm-specific factor)
  - `se` (float, standard error of theta estimate)
  - `paradigm` (string, values: {IFR, ICR, IRE})
**Expected Rows:** 1200 (100 participants x 4 tests x 3 paradigms)
**Note:** RQ 5.3.1 already completed 2-pass IRT purification per Decision D039

**File 2:** data/cache/dfData.csv
**Source:** Project-level demographics
**Required Columns:**
  - `UID` (string, participant identifier, format: P### with leading zeros)
  - `Age` (int, participant age in years, range: 20-70)
**Expected Rows:** 100 participants

**Processing:**
1. Load theta scores from RQ 5.3.1 (step03_theta_scores.csv)
2. Parse composite_ID to extract UID component (UID_test_paradigm -> UID)
3. Load Age variable from dfData.csv
4. Merge theta with Age on UID (left join, keep all theta observations)
5. Validate all 1200 theta observations matched with Age (no missing)
6. Save merged data

**Output:**

**File:** data/step00_theta_age_merged.csv
**Format:** CSV with columns:
  - `composite_ID` (string, from theta file)
  - `UID` (string, participant identifier)
  - `test` (int, test session: 1, 2, 3, 4)
  - `paradigm` (string, {IFR, ICR, IRE})
  - `theta` (float)
  - `Age` (float, years)
**Expected Rows:** 1200 (100 participants x 4 tests x 3 paradigms)
**Expected Columns:** 6
**Note:** RQ 5.3.1 theta file does not contain `se` (standard error) column

**Validation Requirement:**
Validation tools MUST be used after data loading and merging. Specific validation tools will be determined by rq_tools based on data format requirements. The rq_analysis agent will embed validation tool calls after the analysis tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_theta_age_merged.csv: 1200 rows x 6 columns
- Columns: composite_ID (object), UID (object), test (int64), paradigm (object), theta (float64), Age (float64)
- Format: CSV, UTF-8 encoding, no index column

*Value Ranges:*
- theta in [-3, 3] (typical IRT ability range)
- Age in [20, 70] (study inclusion criteria)
- paradigm in {IFR, ICR, IRE} (categorical)
- test in {1, 2, 3, 4} (int)

*Data Quality:*
- Exactly 1200 rows (no data loss from merge)
- No NaN values in any column (all theta observations must have Age)
- No duplicate composite_ID values (unique participant x test x paradigm combinations)
- 100 unique UIDs (all participants present)
- 400 observations per paradigm (balanced design)

*Log Validation:*
- Required pattern: "Loaded theta scores: 1200 rows"
- Required pattern: "Loaded Age data: 100 participants"
- Required pattern: "Merge complete: 1200 rows, 0 missing Age values"
- Forbidden patterns: "ERROR", "NaN detected in Age column", "Missing participants after merge"
- Acceptable warnings: None expected for data loading

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 1200 rows, found 1150 - data loss during merge")
- Log failure to logs/step00_load_theta_age.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause (likely RQ 5.3.1 incomplete or dfData.csv missing Age)

---

### Step 1: Merge TSVR and Transform Variables

**Dependencies:** Step 0 (requires theta_age_merged.csv)

**Complexity:** Low (5 minutes - transformations and merging)

**Purpose:** Merge TSVR time variable and create Age centering + log time transformation for LMM

**Input:**

**File 1:** data/step00_theta_age_merged.csv (from Step 0)

**File 2:** results/ch5/5.3.1/data/step00_tsvr_mapping.csv
**Source:** RQ 5.3.1 extraction outputs
**Format:** CSV with columns:
  - `composite_ID` (string, format: UID_test_paradigm)
  - `TSVR_hours` (float, actual hours since VR encoding session)
**Expected Rows:** 1200 (matches theta file row count)
**Note:** Decision D070 requires using actual TSVR_hours, not nominal days (0, 1, 3, 6)

**Processing:**
1. Load theta_age_merged.csv from Step 0
2. Load TSVR_mapping.csv from RQ 5.3.1
3. Merge on composite_ID (inner join, expect perfect match)
4. Grand-mean center Age: `Age_c = Age - mean(Age)`
5. Create log time transformation: `log_TSVR = log(TSVR_hours + 1)`
   - The +1 constant ensures log is defined at Day 0 (TSVR_hours = 0)
   - Logarithmic time captures non-linear forgetting (early rapid, later asymptotic)
6. Validate Age_c mean approximately 0 (tolerance +/- 0.1)
7. Save LMM input data

**Output:**

**File:** data/step01_lmm_input.csv
**Format:** CSV, long format (one row per observation)
**Columns:**
  - `composite_ID` (string)
  - `UID` (string)
  - `test` (int, {1, 2, 3, 4})
  - `paradigm` (string, {IFR, ICR, IRE})
  - `theta` (float)
  - `Age` (float, original age in years)
  - `Age_c` (float, grand-mean centered age)
  - `TSVR_hours` (float, actual time since encoding)
  - `log_TSVR` (float, log-transformed time)
**Expected Rows:** 1200
**Expected Columns:** 9

**Validation Requirement:**
Validation tools MUST be used after variable transformation. Specific validation tools will be determined by rq_tools based on transformation requirements (centering validation, log transformation validation). The rq_analysis agent will embed validation tool calls after the analysis tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_lmm_input.csv: 1200 rows x 9 columns
- Columns: composite_ID (object), UID (object), test (int64), paradigm (object), theta (float64), Age (float64), Age_c (float64), TSVR_hours (float64), log_TSVR (float64)
- Format: CSV, UTF-8 encoding, no index column

*Value Ranges:*
- theta in [-3, 3]
- Age in [20, 70]
- Age_c in [-25, 25] (approximately, depends on sample age distribution)
- TSVR_hours in [1, 250] (actual study data - some delayed tests)
- log_TSVR in [0.7, 5.6] (log(1+1)~0.69, log(246+1)~5.51)

*Data Quality:*
- Exactly 1200 rows (no data loss from TSVR merge)
- No NaN values in any column
- Age_c mean approximately 0 (tolerance: -0.1 to 0.1)
- Age_c standard deviation approximately equal to Age standard deviation (centering preserves variance)
- log_TSVR monotonically increasing with TSVR_hours (no transformation errors)
- No duplicate composite_ID values

*Log Validation:*
- Required pattern: "TSVR merge complete: 1200 rows matched"
- Required pattern: "Age centering: mean(Age_c) = [value close to 0]"
- Required pattern: "Log transformation complete: min=0, max~5.13"
- Forbidden patterns: "ERROR", "NaN in Age_c", "Age_c mean exceeds tolerance", "TSVR merge incomplete"
- Acceptable warnings: "Age_c mean = 0.03 (within tolerance)" (slight deviation acceptable due to rounding)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Age_c mean = 2.1, exceeds tolerance of 0.1 - centering failed")
- Log failure to logs/step01_merge_tsvr_transform.log
- Quit script immediately
- g_debug invoked to diagnose (likely incorrect centering formula or data type issues)

---

### Step 2: Fit LMM with 3-Way Age x Paradigm x Time Interaction

**Dependencies:** Step 1 (requires lmm_input.csv)

**Complexity:** Medium (10-15 minutes - LMM fitting with random slopes and convergence checks)

**Purpose:** Fit Linear Mixed Model testing full 3-way Age x Paradigm x Time interaction structure with random slopes for time by participant

**Input:**

**File:** data/step01_lmm_input.csv (from Step 1)

**Processing:**

**Model Formula:**
```
theta ~ TSVR_hours + log_TSVR + Age_c + paradigm +
        TSVR_hours:Age_c + log_TSVR:Age_c +
        TSVR_hours:paradigm + log_TSVR:paradigm +
        Age_c:paradigm +
        TSVR_hours:Age_c:paradigm + log_TSVR:Age_c:paradigm +
        (TSVR_hours | UID)
```

**Fixed Effects Structure:**
- Main effects: TSVR_hours, log_TSVR, Age_c, paradigm (IFR = reference level)
- 2-way interactions: Time x Age, Time x Paradigm, Age x Paradigm
- 3-way interactions: Age_c:paradigm:TSVR_hours, Age_c:paradigm:log_TSVR
  - These 3-way terms test whether age effects on forgetting rate differ by paradigm
  - 4 total 3-way coefficients: 2 paradigm contrasts (ICR-IFR, IRE-IFR) x 2 time transformations (linear, log)

**Random Effects Structure:**
- Random slopes: `(TSVR_hours | UID)` allows forgetting rate to vary by participant
- Includes random intercept + random slope + their correlation

**Model Settings:**
- REML = False (for model comparison if needed)
- Optimizer: default (lbfgs)
- Convergence tolerance: default

**Convergence Contingency Plan (per concept.md Section "Convergence Contingency Plan"):**
If full model (random slopes) fails to converge:
1. Try alternative optimizers (bobyqa, nlminb)
2. Use likelihood ratio test (LRT) to compare random slopes vs intercept-only
3. If LRT p < 0.05, retain slopes with simplified correlation structure (uncorrelated)
4. If LRT p >= 0.05, use random intercepts-only model
5. Document which structure achieved convergence in step02_lmm_summary.txt

Reference: Bates et al. (2015) parsimonious mixed models guidelines

**Assumption Validation (per concept.md Section "Validation Procedures"):**
6 diagnostic checks MUST be performed:
1. Residual normality: Q-Q plot + Shapiro-Wilk test (accept if p > 0.01)
2. Homoscedasticity: Residuals vs fitted plot, Levene's test by paradigm x age tertile
3. Random effects normality: Q-Q plot of random intercepts and slopes
4. Independence: ACF plot of residuals (no significant autocorrelation)
5. Linearity: Residuals vs TSVR_hours and log_TSVR (no systematic patterns)
6. Outliers: Cook's distance < 4/N threshold (4/1200 = 0.0033)

**Remedial Actions (if assumptions violated):**
- Normality violated -> Report robust standard errors or bootstrap confidence intervals
- Heteroscedasticity -> Use weighted LMM or variance function by paradigm
- Outliers detected -> Sensitivity analysis with/without outliers

**Output:**

**File 1:** data/step02_lmm_model.pkl
**Format:** Pickle file (serialized statsmodels LMM object)
**Purpose:** Save fitted model for downstream extraction steps

**File 2:** data/step02_lmm_summary.txt
**Format:** Plain text summary
**Contents:**
- Model formula
- Fixed effects table (coefficients, SE, z-values, p-values)
- Random effects variance components
- Model fit indices (AIC, BIC, log-likelihood)
- Convergence status
- Which random structure was used (if contingency plan invoked)
- Assumption validation results (6 diagnostic checks with pass/fail/concern)

**Validation Requirement:**
Validation tools MUST be used after LMM fitting. Specific validation tools will be determined by rq_tools based on LMM validation requirements (convergence checks, assumption diagnostics, variance component checks). The rq_analysis agent will embed validation tool calls after the analysis tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_lmm_model.pkl: Pickle file containing statsmodels MixedLM object
- data/step02_lmm_summary.txt: Text file with model summary (estimated 200-400 lines)

*Value Ranges (from summary.txt parsing):*
- Fixed effects coefficients: No universal bounds (depends on theta scale), but magnitudes typically < 5.0
- Fixed effects SE: Positive values, typically 0.01 to 1.0
- Random effects variances: Positive values (variance > 0 required)
- AIC, BIC: Positive values (lower = better fit)
- Log-likelihood: Negative value (higher = better fit)

*Data Quality:*
- Model converged: model.converged = True (or convergence status documented if contingency plan used)
- All 1200 observations used (no missing data exclusions)
- Random slopes variance > 0 (indicates between-person variability in time effects)
- No NaN coefficients or SE values (estimation must succeed)
- No perfect multicollinearity warnings (VIF checks if logged)

*Log Validation:*
- Required pattern: "Model converged: True" OR "Convergence achieved via [optimizer] after contingency plan"
- Required pattern: "VALIDATION - PASS: Residual normality" (or document violation + remedial action)
- Required pattern: "VALIDATION - PASS: Homoscedasticity" (or document violation + remedial action)
- Required pattern: "Fixed effects extracted: [N] coefficients" (N >= 12 for full 3-way interaction model)
- Forbidden patterns: "ERROR", "Model failed to converge after all optimizers", "NaN coefficients detected"
- Acceptable warnings: "Convergence warning: model fitted with random intercepts only (LRT p = 0.12)" (documents contingency plan use)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Model failed to converge after trying 3 optimizers")
- Log failure to logs/step02_fit_lmm.log
- Quit script immediately
- g_debug invoked to diagnose (likely model overparameterization, insufficient data, or multicollinearity)

---

### Step 3: Extract 3-Way Interaction Terms

**Dependencies:** Step 2 (requires fitted LMM model)

**Complexity:** Low (2-3 minutes - coefficient extraction and p-value adjustment)

**Purpose:** Extract and test the 4 three-way interaction terms (Age_c:paradigm:Time) with Bonferroni correction for 2 time transformations

**Input:**

**File:** data/step02_lmm_model.pkl (from Step 2)

**Processing:**
1. Load fitted LMM model from pickle file
2. Extract fixed effects table (coefficients, SE, z-values, p-values)
3. Identify 4 three-way interaction terms:
   - `Age_c:paradigm[ICR]:TSVR_hours` (linear time, Cued vs Free)
   - `Age_c:paradigm[IRE]:TSVR_hours` (linear time, Recognition vs Free)
   - `Age_c:paradigm[ICR]:log_TSVR` (log time, Cued vs Free)
   - `Age_c:paradigm[IRE]:log_TSVR` (log time, Recognition vs Free)
4. Apply Bonferroni correction: alpha = 0.025 (correcting for 2 time transformation terms: linear and log)
   - Adjusted alpha per term = 0.025 / 2 = 0.0125
5. Report BOTH uncorrected and Bonferroni-corrected p-values per Decision D068
6. Save interaction terms table

**Output:**

**File:** data/step03_interaction_terms.csv
**Format:** CSV with columns:
  - `term` (string, interaction term name)
  - `coefficient` (float, estimated effect)
  - `SE` (float, standard error)
  - `z` (float, z-statistic)
  - `p_uncorrected` (float, uncorrected p-value)
  - `p_bonferroni` (float, Bonferroni-corrected p-value = p_uncorrected x 2)
  - `significant_bonferroni` (bool, p_bonferroni < 0.025)
**Expected Rows:** 4 (one row per three-way interaction term)
**Expected Columns:** 7

**Validation Requirement:**
Validation tools MUST be used after interaction term extraction. Specific validation tools will be determined by rq_tools based on dual p-value requirements (Decision D068 validation). The rq_analysis agent will embed validation tool calls after the analysis tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_interaction_terms.csv: 4 rows x 7 columns
- Columns: term (object), coefficient (float64), SE (float64), z (float64), p_uncorrected (float64), p_bonferroni (float64), significant_bonferroni (bool)
- Format: CSV, UTF-8 encoding, no index column

*Value Ranges:*
- coefficient: Unrestricted (depends on theta scale and age range), typical magnitude < 1.0
- SE: Positive values, typically 0.01 to 0.5
- z: Unrestricted (coefficient / SE), typical range -5 to +5
- p_uncorrected in [0, 1] (probability)
- p_bonferroni in [0, 2] (can exceed 1.0 after Bonferroni correction, capped at 1.0 by convention)
- significant_bonferroni: {True, False}

*Data Quality:*
- Exactly 4 rows (no missing interaction terms)
- No NaN values in any column
- p_bonferroni = p_uncorrected x 2 (or capped at 1.0)
- Dual p-values present (both uncorrected and Bonferroni) per Decision D068
- All 4 term names contain "Age_c" AND "paradigm" AND ("TSVR_hours" OR "log_TSVR")

*Log Validation:*
- Required pattern: "VALIDATION - PASS: Dual p-values present (uncorrected + bonferroni)"
- Required pattern: "Extracted 4 three-way interaction terms"
- Required pattern: "Bonferroni correction applied: family-wise alpha = 0.025"
- Forbidden patterns: "ERROR", "Missing p-value columns", "Interaction terms not found in model"
- Acceptable warnings: None expected for extraction

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 4 interaction terms, found 2 - model may not have converged properly")
- Log failure to logs/step03_extract_interactions.log
- Quit script immediately
- g_debug invoked to diagnose (likely Step 2 model fitting issue or term naming mismatch)

---

### Step 4: Compute Paradigm-Specific Age Effects and Post-Hoc Contrasts

**Dependencies:** Step 3 (requires fitted LMM model and interaction terms)

**Complexity:** Low-Medium (5-8 minutes - marginal effects computation and post-hoc contrasts)

**Purpose:** Extract paradigm-specific age effects at Day 3 midpoint and test ordered pattern (Free > Cued > Recognition) with Tukey HSD post-hoc contrasts

**Input:**

**File:** data/step02_lmm_model.pkl (from Step 2)

**Processing:**
1. Load fitted LMM model
2. Compute marginal age effects at Day 3 midpoint (~TSVR_hours = 72):
   - For each paradigm (IFR, ICR, IRE):
     - Extract slope of theta with respect to Age_c at TSVR_hours = 72
     - Marginal effect = beta_Age_c + beta_Age_c:paradigm + 72 x (beta_Age_c:TSVR_hours + beta_Age_c:paradigm:TSVR_hours) + log(73) x (beta_Age_c:log_TSVR + beta_Age_c:paradigm:log_TSVR)
   - Use delta method to propagate SE from coefficient covariance matrix
3. Compute pairwise comparisons using Tukey HSD:
   - IFR vs ICR (expect IFR > ICR: Free Recall shows stronger age effects)
   - IFR vs IRE (expect IFR > IRE: Free Recall shows strongest age effects)
   - ICR vs IRE (expect ICR > IRE: Cued Recall intermediate)
4. Report BOTH uncorrected and Tukey-adjusted p-values per Decision D068
5. Save age effects and contrasts

**Output:**

**File 1:** data/step04_age_effects.csv
**Format:** CSV with columns:
  - `paradigm` (string, {IFR, ICR, IRE})
  - `age_effect` (float, simple slope of Age_c on theta)
  - `SE` (float, standard error)
  - `z` (float, z-statistic)
  - `p_uncorrected` (float, uncorrected p-value)
  - `p_bonferroni` (float, Bonferroni-adjusted p-value)
  - `significant_bonferroni` (bool, p_bonferroni < 0.05)
**Expected Rows:** 3 (one per paradigm)
**Expected Columns:** 7

**File 2:** data/step04_contrasts.csv
**Format:** CSV with columns:
  - `contrast` (string, e.g., "IFR vs ICR")
  - `difference` (float, difference in age effects)
  - `SE` (float, standard error of difference)
  - `z` (float, z-statistic)
  - `p_uncorrected` (float, uncorrected p-value)
  - `p_bonferroni` (float, Bonferroni-adjusted p-value)
  - `significant_bonferroni` (bool, p_bonferroni < 0.05)
**Expected Rows:** 3 (pairwise comparisons: IFR vs ICR, IFR vs IRE, ICR vs IRE)
**Expected Columns:** 7

**Validation Requirement:**
Validation tools MUST be used after marginal effects and contrasts computation. Specific validation tools will be determined by rq_tools based on dual p-value requirements (Decision D068 contrast validation). The rq_analysis agent will embed validation tool calls after the analysis tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_age_effects.csv: 3 rows x 7 columns
- data/step04_contrasts.csv: 3 rows x 7 columns
- Format: CSV, UTF-8 encoding, no index column

*Value Ranges:*
- age_effect: Typically negative (theta declines with age), range approximately -0.05 to 0 (theta units per year)
- SE (age effects): Positive, typically 0.001 to 0.02
- difference (contrasts): Difference in age effects, typically -0.01 to 0.01
- SE (contrasts): Positive, typically 0.001 to 0.02
- z: Unrestricted, typical range -5 to +5
- p_uncorrected, p_bonferroni in [0, 1]

*Data Quality:*
- Exactly 3 rows in age_effects (IFR, ICR, IRE all present)
- Exactly 3 rows in contrasts (all pairwise comparisons present)
- No NaN values in either file
- Dual p-values present in both files (both uncorrected and Bonferroni-adjusted) per Decision D068
- contrast column contains all 3 pairs: "IFR vs ICR", "IFR vs IRE", "ICR vs IRE"

*Log Validation:*
- Required pattern: "Age effects by paradigm"
- Required pattern: "Pairwise contrasts"
- Forbidden patterns: "ERROR", "Missing paradigm"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step04_age_effects_posthoc.log
- Quit script immediately

---

### Step 5: Prepare Plot Data by Age Tertiles

**Dependencies:** Step 4 (requires paradigm-specific age effects), Step 1 (requires lmm_input.csv for tertile assignment)

**Complexity:** Low (3-5 minutes - tertile assignment and aggregation)

**Purpose:** Create age tertiles (Young/Middle/Older) and aggregate observed means + model predictions for Age x Paradigm x Time visualization

**Input:**

**File 1:** data/step01_lmm_input.csv (from Step 1)
**File 2:** data/step02_lmm_model.pkl (from Step 2)

**Processing:**
1. Load lmm_input.csv to get Age distribution
2. Create age tertiles:
   - Compute Age quantiles: q33 = 33rd percentile, q67 = 67th percentile
   - Assign tertile labels:
     - Young: Age <= q33
     - Middle: q33 < Age <= q67
     - Older: Age > q67
3. For each paradigm x age tertile x timepoint combination:
   - Compute observed mean theta + 95% CI
   - Compute model predicted theta (marginal means from LMM)
4. Create plot data CSV with columns: paradigm, age_tertile, TSVR_hours, observed_mean, observed_CI_lower, observed_CI_upper, predicted_mean
5. Expected: 3 paradigms x 3 tertiles x 4 timepoints = 36 rows

**Output:**

**File 1:** data/step05_plot_data.csv
**Format:** CSV with columns:
  - `age_tertile` (string, {Young, Middle, Older})
  - `paradigm` (string, {IFR, ICR, IRE})
  - `test` (int, {1, 2, 3, 4})
  - `theta_mean` (float, mean theta from raw data)
  - `theta_SE` (float, standard error of mean)
  - `N` (int, sample size per group)
  - `TSVR_hours_mean` (float, mean TSVR_hours for that test)
**Expected Rows:** 36 (3 age tertiles x 3 paradigms x 4 tests)
**Expected Columns:** 7

**File 2:** data/step05_age_tertiles.csv
**Format:** CSV with columns:
  - `tertile` (int, {1, 2, 3})
  - `label` (string, {Young, Middle, Older})
  - `age_min` (float, minimum age in tertile)
  - `age_max` (float, maximum age in tertile)
  - `N` (int, participants per tertile)
**Expected Rows:** 3 (one per tertile)
**Expected Columns:** 5

**Validation Requirement:**
Validation tools MUST be used after plot data preparation. Specific validation tools will be determined by rq_tools based on plot data format requirements (completeness of factorial design, valid value ranges). The rq_analysis agent will embed validation tool calls after the analysis tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_plot_data.csv: 36 rows x 7 columns
- data/step05_age_tertiles.csv: 3 rows x 5 columns
- Format: CSV, UTF-8 encoding, no index column

*Value Ranges:*
- age_tertile in {Young, Middle, Older}
- paradigm in {IFR, ICR, IRE}
- test in {1, 2, 3, 4}
- theta_mean in [-3, 3] (theta scale)
- theta_SE > 0 (positive standard errors)
- N > 0 (sample sizes)
- TSVR_hours_mean in [1, 250]

*Data Quality:*
- Exactly 36 rows in plot_data (complete factorial design: 3 x 3 x 4)
- Exactly 3 rows in age_tertiles (3 tertile definitions)
- No NaN values in any column
- All 3 paradigms represented (12 rows each)
- All 3 age tertiles represented (12 rows each)
- All 4 tests represented per paradigm x tertile combination
- N >= 10 for all groups (sufficient sample size per cell)

*Log Validation:*
- Required pattern: "Age tertile distribution"
- Required pattern: "Aggregated data: 36 rows"
- Forbidden patterns: "ERROR", "Missing"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step05_plot_data_age_tertiles.log
- Quit script immediately
- g_debug invoked to diagnose (likely incomplete aggregation or missing data for some combinations)

---

## Expected Data Formats

### Folder Structure (v4.2 - Updated 2025-12-02)

```
results/ch5/5.3.4/
  /code    = ALL .py code files for running analysis
  /data    = ALL inputs AND outputs from analysis steps (intermediate + final)
  /docs    = ALL planning documentation (1_concept.md, 2_plan.md, 3_tools.yaml, 4_analysis.yaml)
  /logs    = ONLY .log files (execution logs from each step - stdout/stderr capture)
  /plots   = EMPTY until rq_plots generates PNG/PDF visualizations (not used in this RQ)
  /results = EMPTY until rq_results generates summary.md
```

### Data Files (ALL analysis inputs and outputs)

**Step 0 Output:**
- data/step00_theta_age_merged.csv: 1200 rows x 7 columns (composite_ID, UID, test, paradigm, theta, se, Age)

**Step 1 Output:**
- data/step01_lmm_input.csv: 1200 rows x 10 columns (adds Age_c, TSVR_hours, log_TSVR)

**Step 2 Outputs:**
- data/step02_lmm_model.pkl: Pickle file (statsmodels MixedLM object)
- data/step02_lmm_summary.txt: Text file (200-400 lines, model summary + diagnostics)

**Step 3 Output:**
- data/step03_interaction_terms.csv: 4 rows x 7 columns (3-way interaction coefficients with dual p-values)

**Step 4 Outputs:**
- data/step04_age_effects_by_paradigm.csv: 3 rows x 5 columns (paradigm-specific age slopes)
- data/step04_posthoc_contrasts.csv: 3 rows x 7 columns (pairwise comparisons with dual p-values)

**Step 5 Output:**
- data/step05_age_paradigm_plot_data.csv: 36 rows x 7 columns (observed + predicted means for plotting)

### Logs (ONLY execution logs - .log files capturing stdout/stderr)

- logs/step00_load_theta_age.log
- logs/step01_merge_tsvr_transform.log
- logs/step02_fit_lmm.log
- logs/step03_extract_interactions.log
- logs/step04_compute_age_effects_contrasts.log
- logs/step05_prepare_plot_data.log

### Plots (EMPTY - no plotting in this RQ per concept.md)

No plot files generated. Plot data prepared in Step 5 (data/step05_age_paradigm_plot_data.csv) is available for future visualization if needed, but rq_plots is not invoked for this RQ.

### Results (EMPTY until rq_results runs)

- results/summary.md (created by rq_results, NOT analysis steps)

---

## Cross-RQ Dependencies

**Dependency Type:** DERIVED Data from Other RQs

**This RQ requires outputs from:**

**RQ 5.3.1** (Paradigm-Specific Trajectories - provides theta scores for 3 paradigms)
- File 1: results/ch5/5.3.1/data/step03_theta_scores.csv
  - Used in: Step 0 (load theta estimates for IFR, ICR, IRE)
  - Expected: 1200 rows (100 participants x 4 tests x 3 paradigms)
  - Rationale: RQ 5.3.1 calibrates IRT models for each paradigm and extracts theta scores. This RQ uses those theta estimates as the outcome variable in LMM to test Age x Paradigm x Time interactions.

- File 2: results/ch5/5.3.1/data/step00_tsvr_mapping.csv
  - Used in: Step 1 (merge actual time since encoding)
  - Expected: 1200 rows (composite_ID x TSVR_hours mapping)
  - Rationale: Decision D070 requires using actual TSVR_hours, not nominal days. RQ 5.3.1 created this mapping during extraction.

**dfData.csv** (Project-level demographics - RAW data source)
- File: data/cache/dfData.csv
  - Used in: Step 0 (load Age variable)
  - Required Column: Age (int, range 20-70)
  - Expected: 100 participants
  - Rationale: Age is the key predictor variable for this RQ. Not derived from other RQs, extracted directly from project demographics file.

**Execution Order Constraint:**
1. RQ 5.3.1 must complete through Step 3 (theta extraction)
2. This RQ can then execute (uses RQ 5.3.1 theta + TSVR mapping)

**Data Source Boundaries:**
- **RAW data:** Age from dfData.csv (project-level demographics)
- **DERIVED data:** Theta scores and TSVR mapping from RQ 5.3.1 (paradigm-specific IRT calibration)
- **Scope:** This RQ does NOT calibrate IRT models (reuses RQ 5.3.1 theta estimates)

**Validation:**
- Step 0: Check results/ch5/5.3.1/data/step03_theta_scores.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 1: Check results/ch5/5.3.1/data/step00_tsvr_mapping.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 0: Check data/cache/dfData.csv exists and has Age column (circuit breaker: EXPECTATIONS ERROR if absent or missing column)
- If any file missing -> quit with error -> user must execute RQ 5.3.1 first or verify dfData.csv availability

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

### Validation Requirements By Step

#### Step 0: Load Theta Scores and Age Data

**Analysis Tool:** (determined by rq_tools - likely pandas merge operations)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure + validate_numeric_range)

**What Validation Checks:**
- Output file exists (data/step00_theta_age_merged.csv)
- Expected row count (1200 rows: 100 participants x 4 tests x 3 paradigms)
- Expected column count (7 columns)
- Required columns present (composite_ID, UID, test, paradigm, theta, se, Age)
- theta values in valid range [-3, 3]
- se values in valid range [0.1, 1.0]
- Age values in valid range [20, 70]
- No NaN values in any column
- 100 unique UIDs (all participants matched)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step00_load_theta_age.log
- Quit script immediately
- g_debug invoked to diagnose (likely RQ 5.3.1 incomplete or dfData.csv missing Age)

---

#### Step 1: Merge TSVR and Transform Variables

**Analysis Tool:** (determined by rq_tools - likely pandas merge + custom transformation functions)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_standardization for Age_c centering)

**What Validation Checks:**
- Output file exists (data/step01_lmm_input.csv)
- Expected row count (1200 rows, no data loss from TSVR merge)
- Age_c mean approximately 0 (tolerance: -0.1 to 0.1)
- Age_c SD approximately equal to Age SD (centering preserves variance)
- log_TSVR values valid (no NaN, no negative values)
- log_TSVR monotonically related to TSVR_hours (log transformation correct)
- No NaN values in any column

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step01_merge_tsvr_transform.log
- Quit script immediately
- g_debug invoked to diagnose (likely centering formula error or TSVR merge issue)

---

#### Step 2: Fit LMM with 3-Way Age x Paradigm x Time Interaction

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.fit_lmm_trajectory_tsvr)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_lmm_assumptions_comprehensive)

**What Validation Checks:**
- Model convergence (model.converged = True, or convergence contingency plan documented)
- 6 assumption diagnostics (per concept.md):
  1. Residual normality (Shapiro-Wilk p > 0.01)
  2. Homoscedasticity (Levene's test, residuals vs fitted plot)
  3. Random effects normality (Q-Q plots of random intercepts and slopes)
  4. Independence (ACF plot, no significant autocorrelation)
  5. Linearity (residuals vs TSVR_hours and log_TSVR)
  6. Outliers (Cook's distance < 4/1200 = 0.0033)
- Random slopes variance > 0 (between-person variability present)
- No NaN coefficients or SE values
- Expected number of fixed effects (>=12 for full 3-way model)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step02_fit_lmm.log
- Quit script immediately
- g_debug invoked to diagnose (likely model overparameterization or convergence issue)

---

#### Step 3: Extract 3-Way Interaction Terms

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.extract_fixed_effects_from_lmm)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_hypothesis_test_dual_pvalues)

**What Validation Checks:**
- Output file exists (data/step03_interaction_terms.csv)
- Expected row count (4 three-way interaction terms)
- Dual p-values present (both p_uncorrected and p_bonferroni) per Decision D068
- p_bonferroni = p_uncorrected x 2 (or capped at 1.0)
- All term names contain "Age_c" AND "paradigm" AND ("TSVR_hours" OR "log_TSVR")
- No NaN values

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step03_extract_interactions.log
- Quit script immediately
- g_debug invoked to diagnose (likely term naming mismatch or model fitting issue)

---

#### Step 4: Compute Paradigm-Specific Age Effects and Post-Hoc Contrasts

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.extract_marginal_age_slopes_by_domain + compute_contrasts_pairwise)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_contrasts_dual_pvalues)

**What Validation Checks:**
- Output files exist (age_effects_by_paradigm.csv, posthoc_contrasts.csv)
- Age effects: 3 rows (IFR, ICR, IRE), no NaN, CI_upper > CI_lower
- Contrasts: 3 rows (IFR-ICR, IFR-IRE, ICR-IRE)
- Dual p-values present in contrasts (p_uncorrected and p_tukey) per Decision D068
- No NaN values

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step04_compute_age_effects_contrasts.log
- Quit script immediately
- g_debug invoked to diagnose (likely delta method SE propagation issue)

---

#### Step 5: Prepare Plot Data by Age Tertiles

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.prepare_age_effects_plot_data)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_plot_data_completeness)

**What Validation Checks:**
- Output file exists (data/step05_age_paradigm_plot_data.csv)
- Expected row count (36 rows: 3 paradigms x 3 tertiles x 4 timepoints)
- Complete factorial design (all combinations present)
- All 3 paradigms represented
- All 3 age tertiles represented
- All 4 timepoints represented
- observed_CI_upper > observed_CI_lower for all rows
- No NaN values

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step05_prepare_plot_data.log
- Quit script immediately
- g_debug invoked to diagnose (likely incomplete aggregation or missing combinations)

---

## Summary

**Total Steps:** 6 (Step 0 through Step 5)

**Estimated Runtime:**
- Low-Medium total: 25-40 minutes
- Step 0: 5 min (data loading)
- Step 1: 5 min (transformations)
- Step 2: 10-15 min (LMM fitting with convergence checks)
- Step 3: 2-3 min (interaction extraction)
- Step 4: 5-8 min (marginal effects + contrasts)
- Step 5: 3-5 min (plot data preparation)

**Cross-RQ Dependencies:**
- RQ 5.3.1 (theta scores + TSVR mapping)
- dfData.csv (Age variable)

**Primary Outputs:**
- data/step02_lmm_model.pkl (fitted 3-way interaction model)
- data/step03_interaction_terms.csv (4 three-way terms with dual p-values)
- data/step04_age_effects_by_paradigm.csv (paradigm-specific age slopes)
- data/step04_posthoc_contrasts.csv (Tukey HSD contrasts with dual p-values)
- data/step05_age_paradigm_plot_data.csv (plot source data: 36 rows)

**Validation Coverage:** 100% (all 6 steps have validation requirements)

**Key Features:**
- Tests 3-way Age x Paradigm x Time interaction (primary research question)
- Bonferroni correction for 2 time transformations (alpha = 0.025)
- Dual p-value reporting per Decision D068 (uncorrected + Bonferroni/Tukey)
- TSVR (actual hours) as time variable per Decision D070
- Convergence contingency plan (LRT-based random structure selection)
- 6 comprehensive assumption diagnostics per concept.md specifications

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-02): Initial plan created by rq_planner agent for RQ 5.3.4 (Age x Paradigm Interactions)
