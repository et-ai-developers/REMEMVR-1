# Analysis Plan: RQ 5.5.4 - IRT-CTT Convergence for Source-Destination Memory

**Research Question:** 5.5.4
**Created:** 2025-12-04
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ validates the measurement robustness of the source-destination memory dissociation discovered in RQ 5.5.1 by examining convergence between IRT theta scores and CTT mean scores. The analysis uses DERIVED data from RQ 5.5.1 (IRT theta scores, purified items, TSVR time mapping) and computes CTT mean scores on the same purified item set for fair comparison.

**Analysis Pipeline:** CTT Computation -> Correlation Analysis -> Parallel LMM Fitting -> Fixed Effects Comparison

**Total Steps:** 8 analysis steps (Step 0: dependency loading + Steps 1-8: analyses)

**Estimated Runtime:** Medium complexity (~30-60 minutes total)

**Key Decisions Applied:**
- **Decision D068:** Dual p-value reporting (uncorrected + Bonferroni) for all statistical tests
- **Decision D070:** TSVR (actual hours) as time variable in LMMs (inherited from RQ 5.5.1)
- **Purified items only:** CTT computed on same item set as IRT (Decision D039 quality criteria applied in RQ 5.5.1)

**Data Source:** DERIVED from RQ 5.5.1 - no new IRT calibration required

**Sample:** N=100 participants x 4 test sessions x 2 location types = 800 observations

**Success Criteria:**
- All three correlations (Source, Destination, Overall) exceed r > 0.70 threshold
- Cohen's kappa for LMM fixed effects agreement exceeds 0.60 (substantial agreement)
- Overall classification agreement >= 80%
- Both IRT-based and CTT-based LMMs converge with identical model structure

---

## Analysis Plan

### Step 0: Load Dependencies from RQ 5.5.1

**Dependencies:** None (first step)
**Complexity:** Low (<5 minutes - data loading only)

**Purpose:** Load IRT theta scores, purified items list, TSVR time mapping, and raw response data from RQ 5.5.1 and dfData.csv

**Input:**

**File 1:** results/ch5/5.5.1/data/step03_theta_scores.csv
**Source:** RQ 5.5.1 (IRT Pass 2 - final theta estimates)
**Format:** CSV, wide format
**Columns:**
  - `UID` (string, participant identifier, format: P### with leading zeros)
  - `test` (string, test session: T1, T2, T3, T4)
  - `theta_source` (float64, IRT ability estimate for pick-up locations -U-)
  - `se_source` (float64, standard error for source theta)
  - `theta_destination` (float64, IRT ability estimate for put-down locations -D-)
  - `se_destination` (float64, standard error for destination theta)
**Expected Rows:** 400 (100 participants x 4 tests)

**File 2:** results/ch5/5.5.1/data/step02_purified_items.csv
**Source:** RQ 5.5.1 (Item purification via Decision D039)
**Format:** CSV, list of retained items
**Columns:**
  - `item_code` (string, format: VR-{paradigm}-{test}-{domain}-ANS)
  - `location_type` (string, "source" or "destination")
  - `a` (float64, discrimination parameter from IRT)
  - `b` (float64, difficulty parameter from IRT)
**Expected Rows:** 25-32 items (items passing |b| <= 3.0 AND a >= 0.4 criteria)

**File 3:** results/ch5/5.5.1/data/step00_tsvr_mapping.csv
**Source:** RQ 5.5.1 (TSVR time variable extraction)
**Format:** CSV
**Columns:**
  - `UID` (string)
  - `test` (string)
  - `TSVR_hours` (float64, actual hours since VR encoding session per Decision D070)
**Expected Rows:** 400 (100 participants x 4 tests)

**File 4:** data/cache/dfData.csv
**Source:** Project-level master VR dataset
**Format:** CSV, long format (one row per participant-item-test combination)
**Columns:**
  - `UID` (string)
  - `test` (string)
  - Item response columns matching purified items list (binary 0/1)
**Filter:** Only rows for purified -U- and -D- items (from File 2)

**Processing:**
1. Load theta_scores.csv (400 rows)
2. Load purified_items.csv, extract item_code list (25-32 items)
3. Load tsvr_mapping.csv (400 rows)
4. Load dfData.csv, filter to:
   - UIDs present in theta_scores.csv (100 participants)
   - Tests present in theta_scores.csv (T1, T2, T3, T4)
   - Item columns matching purified_items item_code list only
5. Validate all files loaded successfully
6. Verify expected row counts match (400 for theta/tsvr, varies for dfData)
7. Create composite_ID column (UID_test format) for merging

**Output:**

**File 1:** data/step00_irt_theta_from_rq551.csv
**Format:** CSV, 800 rows (400 participant-test combinations x 2 location types, reshaped long)
**Columns:**
  - `composite_ID` (string, format: UID_test)
  - `UID` (string)
  - `test` (string)
  - `location_type` (string, "source" or "destination")
  - `irt_theta` (float64, theta score for location type)
  - `irt_se` (float64, standard error for theta)
  - `TSVR_hours` (float64, time variable from TSVR mapping)
**Expected Rows:** 800 (100 participants x 4 tests x 2 location types)

**File 2:** data/step00_purified_items_from_rq551.csv
**Format:** CSV, list of purified items
**Columns:**
  - `item_code` (string)
  - `location_type` (string)
**Expected Rows:** 25-32 items total (split between source/destination)

**File 3:** data/step00_raw_responses_filtered.csv
**Format:** CSV, raw binary responses filtered to purified items only
**Columns:**
  - `composite_ID` (string)
  - `UID` (string)
  - `test` (string)
  - One column per purified item_code (binary 0/1)
**Expected Rows:** 400 (100 participants x 4 tests)

**Validation Requirement:**
Validation tools MUST be used after data loading. Specific validation tools determined by rq_tools based on data loading requirements (file existence, row counts, column presence).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_irt_theta_from_rq551.csv: 800 rows x 7 columns (composite_ID, UID, test, location_type, irt_theta, irt_se, TSVR_hours)
- data/step00_purified_items_from_rq551.csv: 25-32 rows x 2 columns (item_code, location_type)
- data/step00_raw_responses_filtered.csv: 400 rows x (3 + N_items) columns where N_items in [25, 32]
- Data types: strings (IDs, test), float64 (theta, SE, TSVR, responses)

*Value Ranges:*
- irt_theta in [-3, 3] (typical IRT ability range)
- irt_se in [0.1, 1.5] (reasonable standard errors)
- TSVR_hours in [0, 168] hours (0=encoding, 168=1 week post-encoding)
- Binary responses in {0, 1, NaN} (0=incorrect, 1=correct, NaN=missing)
- location_type in {"source", "destination"}

*Data Quality:*
- No NaN in irt_theta, irt_se, TSVR_hours (all observations must have valid theta and time)
- Expected N: Exactly 800 rows in theta file (100 participants x 4 tests x 2 locations)
- Expected N: Exactly 400 rows in raw responses file (before location split)
- No duplicate composite_IDs in theta file
- Item count validation: 25-32 items total (post-purification, some items removed per Decision D039)
- Location type balance: Both "source" and "destination" present in purified items list

*Log Validation:*
- Required pattern: "Loaded theta_scores.csv: 400 rows"
- Required pattern: "Loaded purified_items.csv: {N} items" where N in [25, 32]
- Required pattern: "Loaded tsvr_mapping.csv: 400 rows"
- Required pattern: "Filtered dfData.csv to purified items: 400 rows x {N} item columns"
- Required pattern: "Reshaped to long format: 800 rows (2 location types)"
- Required pattern: "RQ 5.5.1 dependency verified: all required files exist"
- Forbidden patterns: "ERROR", "File not found", "Missing data in theta", "TSVR merge failed"
- Acceptable warnings: "NaN values in item responses" (some items may be missing for some participants)

**Expected Behavior on Validation Failure:**
- If RQ 5.5.1 files missing -> Raise EXPECTATIONS ERROR with message "RQ 5.5.1 must complete through Step 3 before RQ 5.5.4 can run"
- If row count mismatches -> Raise error with specific message (e.g., "Expected 400 theta rows, found 387")
- If item count outside [25, 32] -> Raise error (purification may have failed in RQ 5.5.1)
- Log failure to logs/step00_load_dependencies.log
- Quit script immediately (do NOT proceed to Step 1)
- Master invokes g_debug to diagnose root cause

---

### Step 1: Compute CTT Mean Scores per Location Type

**Dependencies:** Step 0 (requires raw responses filtered to purified items)
**Complexity:** Low (<5 minutes - simple aggregation)

**Purpose:** Compute Classical Test Theory (CTT) mean scores by averaging binary responses (0/1) across purified items for each participant x test x location type combination

**Input:**

**File 1:** data/step00_raw_responses_filtered.csv (from Step 0)
**Format:** CSV, wide format (composite_ID x item columns)
**Columns:**
  - `composite_ID` (string)
  - `UID` (string)
  - `test` (string)
  - Item columns (25-32 items, binary 0/1 or NaN)

**File 2:** data/step00_purified_items_from_rq551.csv (from Step 0)
**Format:** CSV, item metadata
**Columns:**
  - `item_code` (string)
  - `location_type` (string, "source" or "destination")

**Processing:**
1. Load raw responses and purified items metadata
2. For each unique location_type (source, destination):
   a. Filter purified_items to location_type
   b. Extract item_code list for that location
   c. Select corresponding columns from raw_responses
   d. For each composite_ID (UID x test):
      - Compute mean of binary responses across items (ignoring NaN)
      - Result is CTT score in [0, 1] range
3. Create long-format output: 800 rows (400 composite_IDs x 2 location types)
4. Merge with TSVR_hours from step00_irt_theta_from_rq551.csv

**Output:**

**File:** data/step01_ctt_scores.csv
**Format:** CSV, long format
**Columns:**
  - `composite_ID` (string, format: UID_test)
  - `UID` (string)
  - `test` (string)
  - `location_type` (string, "source" or "destination")
  - `ctt_mean_score` (float64, mean proportion correct in [0, 1])
  - `n_items` (int, number of items contributing to mean - varies by location type)
  - `TSVR_hours` (float64, time variable for LMM)
**Expected Rows:** 800 (100 participants x 4 tests x 2 location types)

**Validation Requirement:**
Validation tools MUST be used after CTT computation. Specific validation tools determined by rq_tools based on CTT score format requirements (bounded [0,1], no NaN, expected N).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_ctt_scores.csv: 800 rows x 7 columns
- Data types: composite_ID (string), UID (string), test (string), location_type (string), ctt_mean_score (float64), n_items (int64), TSVR_hours (float64)

*Value Ranges:*
- ctt_mean_score in [0, 1] (proportion correct, continuous)
- n_items > 0 for all rows (at least one item per location type)
- n_items in [10, 20] per location type (purified item count varies)
- TSVR_hours in [0, 168] (time range)

*Data Quality:*
- No NaN in ctt_mean_score (all participants must have valid CTT score)
- No NaN in n_items (item count must be computable)
- No NaN in TSVR_hours (time variable required for LMM)
- Expected N: Exactly 800 rows (100 participants x 4 tests x 2 locations)
- No duplicate composite_ID x location_type combinations
- Location balance: 400 rows for "source", 400 rows for "destination"
- n_items approximately equal within location type (same items used for all participants)

*Log Validation:*
- Required pattern: "Computed CTT scores: 800 rows"
- Required pattern: "Source items: {N_source}, Destination items: {N_destination}"
- Required pattern: "CTT score range: [0.0, 1.0]"
- Required pattern: "No missing values in ctt_mean_score column"
- Forbidden patterns: "ERROR", "NaN in ctt_mean_score", "Item count = 0"
- Acceptable warnings: "Some participants have NaN for specific items" (missing data acceptable, mean computed over available items)

**Expected Behavior on Validation Failure:**
- If ctt_mean_score outside [0, 1] -> Raise error (computation error, binary data should always yield [0,1] mean)
- If NaN in ctt_mean_score -> Raise error (indicates participant with zero valid items for a location type)
- If row count != 800 -> Raise error (missing data for some participants/tests/locations)
- Log failure to logs/step01_compute_ctt_scores.log
- Quit script immediately
- g_debug invoked to diagnose

---

### Step 2: Pearson Correlations between IRT and CTT Scores

**Dependencies:** Step 0 (IRT theta), Step 1 (CTT scores)
**Complexity:** Low (<5 minutes - correlation computation)

**Purpose:** Assess linear association between IRT theta scores and CTT mean scores, stratified by location type (source, destination) and overall, with significance testing and Bonferroni correction per Decision D068

**Input:**

**File 1:** data/step00_irt_theta_from_rq551.csv (from Step 0)
**Columns:** composite_ID, location_type, irt_theta

**File 2:** data/step01_ctt_scores.csv (from Step 1)
**Columns:** composite_ID, location_type, ctt_mean_score

**Processing:**
1. Merge IRT theta and CTT scores on composite_ID + location_type
2. For each stratification (Source, Destination, Overall):
   a. Subset data to location_type (or all rows for Overall)
   b. Compute Pearson r between irt_theta and ctt_mean_score
   c. Test significance with scipy.stats.pearsonr (two-tailed)
   d. Extract p_uncorrected
3. Apply Bonferroni correction for 3 comparisons: p_bonferroni = min(p_uncorrected x 3, 1.0)
4. Test convergence criteria:
   - Strong convergence: r > 0.70
   - Exceptional convergence: r > 0.90
5. Report dual p-values per Decision D068

**Output:**

**File:** data/step02_correlations.csv
**Format:** CSV, 3 rows (Source, Destination, Overall)
**Columns:**
  - `location_type` (string: "source", "destination", "overall")
  - `r` (float64, Pearson correlation coefficient in [-1, 1])
  - `p_uncorrected` (float64, uncorrected p-value from pearsonr test)
  - `p_bonferroni` (float64, Bonferroni-corrected p-value, min(p_uncorrected x 3, 1.0))
  - `n` (int, number of observations contributing to correlation)
  - `r_threshold_70` (bool, True if r > 0.70, False otherwise)
  - `r_threshold_90` (bool, True if r > 0.90, False otherwise)
  - `interpretation` (string: "Strong convergence" if r > 0.70, "Exceptional" if r > 0.90, "Moderate" if 0.50-0.70, "Weak" if <0.50)
**Expected Rows:** 3 (Source, Destination, Overall)

**Validation Requirement:**
Validation tools MUST be used after correlation computation. Specific validation tools determined by rq_tools based on Decision D068 dual p-value requirements and correlation bounds.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_correlations.csv: 3 rows x 8 columns
- Data types: location_type (string), r (float64), p_uncorrected (float64), p_bonferroni (float64), n (int64), r_threshold_70 (bool), r_threshold_90 (bool), interpretation (string)

*Value Ranges:*
- r in [-1, 1] (correlation coefficient bounds)
- p_uncorrected in [0, 1] (probability range)
- p_bonferroni in [0, 1] (corrected probability, may equal 1.0 if p_uncorrected x 3 > 1)
- n = 400 for "source" and "destination" (100 participants x 4 tests), n = 800 for "overall"
- r expected > 0.70 based on hypothesis (strong convergence)

*Data Quality:*
- No NaN in r, p_uncorrected, p_bonferroni (all correlations must be computable)
- p_bonferroni >= p_uncorrected (correction cannot reduce p-value)
- Bonferroni formula correct: p_bonferroni = min(p_uncorrected x 3, 1.0)
- All 3 location types present ("source", "destination", "overall")
- r_threshold_70 and r_threshold_90 flags match r values
- interpretation consistent with r value

*Log Validation:*
- Required pattern: "Computed Pearson correlations: 3 stratifications"
- Required pattern: "Source: r = {r:.3f}, p_uncorrected = {p:.4f}, p_bonferroni = {p:.4f}"
- Required pattern: "Destination: r = {r:.3f}, p_uncorrected = {p:.4f}, p_bonferroni = {p:.4f}"
- Required pattern: "Overall: r = {r:.3f}, p_uncorrected = {p:.4f}, p_bonferroni = {p:.4f}"
- Required pattern: "Decision D068 dual p-values reported: uncorrected + Bonferroni"
- Required pattern: "Bonferroni correction factor: 3 comparisons"
- Forbidden patterns: "ERROR", "NaN in correlation", "p_bonferroni < p_uncorrected"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- If r outside [-1, 1] -> Raise error (correlation computation error)
- If p_bonferroni < p_uncorrected -> Raise error (Bonferroni formula incorrect)
- If row count != 3 -> Raise error (missing stratification)
- If r < 0.70 for all stratifications -> Log warning "Convergence criterion NOT met: r <= 0.70" but continue (negative finding is valid result)
- Log failure to logs/step02_correlations.log
- Quit on computation errors, continue on negative findings
- g_debug invoked for computation errors only

---

### Step 3: Fit Parallel LMMs (IRT-based and CTT-based)

**Dependencies:** Step 0 (IRT theta + TSVR), Step 1 (CTT scores + TSVR)
**Complexity:** Medium (10-20 minutes - two LMM fits with convergence checks)

**Purpose:** Fit identical Linear Mixed Models to IRT theta scores and CTT mean scores to assess structural equivalence of trajectory patterns across measurement approaches

**Input:**

**File 1:** data/step00_irt_theta_from_rq551.csv
**Columns:** composite_ID, UID, location_type, irt_theta, TSVR_hours

**File 2:** data/step01_ctt_scores.csv
**Columns:** composite_ID, UID, location_type, ctt_mean_score, TSVR_hours

**Processing:**
1. **Model Formula (Identical for Both):**
   - score ~ LocationType x log_TSVR + (log_TSVR | UID)
   - Fixed effects: Intercept, LocationType (Treatment coded: Source as reference), log_TSVR, LocationType:log_TSVR
   - Random effects: Random intercept + random slope for log_TSVR by UID
   - REML: False (use ML for AIC comparison in Step 6)
   - Time variable: log(TSVR_hours + 1) to handle TSVR=0 at encoding

2. **Fit IRT-based LMM:**
   - Dependent variable: irt_theta
   - Fit using statsmodels.formula.api.mixedlm
   - Check convergence: model.converged == True

3. **Fit CTT-based LMM:**
   - Dependent variable: ctt_mean_score
   - Fit using statsmodels.formula.api.mixedlm
   - Check convergence: model.converged == True

4. **Convergence Failure Handling:**
   - If EITHER model fails convergence:
     a. Simplify BOTH models identically to: score ~ LocationType x log_TSVR + (1 | UID)
     b. Remove random slopes, keep random intercepts only
     c. Re-fit both models with simplified formula
     d. Document simplification in summary files

5. Save both fitted models as pickle files
6. Save model summaries as text files

**Output:**

**File 1:** data/step03_irt_lmm_model.pkl
**Format:** Pickle file containing fitted statsmodels MixedLM object
**Content:** IRT-based LMM model (irt_theta as DV)

**File 2:** data/step03_ctt_lmm_model.pkl
**Format:** Pickle file containing fitted statsmodels MixedLM object
**Content:** CTT-based LMM model (ctt_mean_score as DV)

**File 3:** data/step03_irt_lmm_summary.txt
**Format:** Text file, statsmodels summary output
**Content:**
  - Model formula
  - Fixed effects table (coefficient, SE, z-value, p-value)
  - Random effects variance components
  - Convergence status
  - Log-likelihood, AIC, BIC
  - Number of observations, groups

**File 4:** data/step03_ctt_lmm_summary.txt
**Format:** Text file, statsmodels summary output
**Content:** Same structure as File 3 for CTT-based model

**File 5:** data/step03_model_metadata.yaml
**Format:** YAML file documenting model specifications
**Content:**
  - model_formula: (full or simplified)
  - irt_converged: (bool)
  - ctt_converged: (bool)
  - simplification_applied: (bool)
  - n_observations: 800
  - n_participants: 100
  - random_structure: (full with slopes or intercepts-only)

**Validation Requirement:**
Validation tools MUST be used after LMM fitting. Specific validation tools determined by rq_tools based on LMM convergence requirements and model structure validation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_irt_lmm_model.pkl: Valid pickle file containing MixedLMResults object
- data/step03_ctt_lmm_model.pkl: Valid pickle file containing MixedLMResults object
- data/step03_irt_lmm_summary.txt: Text file with statsmodels summary output (>500 characters)
- data/step03_ctt_lmm_summary.txt: Text file with statsmodels summary output (>500 characters)
- data/step03_model_metadata.yaml: Valid YAML file with required keys

*Value Ranges:*
- Fixed effects coefficients: Unrestricted (can be positive/negative)
- Standard errors > 0 (always positive)
- p-values in [0, 1]
- Random variances >= 0 (variance cannot be negative)
- AIC, BIC: Finite values (not NaN, not inf)
- Log-likelihood: Finite value (not NaN, not inf)

*Data Quality:*
- Both models converged OR both simplified identically (no asymmetry)
- Model formula identical for IRT and CTT models
- n_observations = 800 for both models
- n_participants = 100 for both models
- Fixed effects count: 4 terms (Intercept, LocationType, log_TSVR, LocationType:log_TSVR)
- Random effects: Either 2 variances + 1 covariance (full) OR 1 variance (intercepts-only)

*Log Validation:*
- Required pattern: "Fitted IRT-based LMM: converged = {True/False}"
- Required pattern: "Fitted CTT-based LMM: converged = {True/False}"
- Required pattern: "Model formula: score ~ LocationType x log_TSVR + (...)"
- If simplification: Required pattern: "Convergence failure detected, simplified both models to random intercepts only"
- Required pattern: "Fixed effects: 4 terms"
- Required pattern: "AIC (IRT): {value}, AIC (CTT): {value}"
- Forbidden patterns: "ERROR", "Model fit failed", "NaN in coefficients", "Random variance negative"
- Acceptable warnings: "Convergence warning" (if models eventually converge)

**Expected Behavior on Validation Failure:**
- If BOTH models fail convergence even after simplification -> Raise error "Unable to fit LMMs even with simplified structure"
- If only ONE model fails (asymmetry) -> This should NOT happen (code simplifies both identically), raise error
- If NaN in coefficients or variances -> Raise error "Model estimation failed"
- Log failure to logs/step03_fit_parallel_lmms.log
- Quit script immediately
- g_debug invoked to diagnose

---

### Step 4: Validate LMM Assumptions for Both Models

**Dependencies:** Step 3 (fitted IRT and CTT LMMs)
**Complexity:** Medium (10-15 minutes - 7 assumption checks x 2 models)

**Purpose:** Comprehensive validation of LMM assumptions for both IRT-based and CTT-based models to ensure statistical validity of fixed effects comparisons in Step 5

**Input:**

**File 1:** data/step03_irt_lmm_model.pkl (from Step 3)
**File 2:** data/step03_ctt_lmm_model.pkl (from Step 3)
**File 3:** data/step00_irt_theta_from_rq551.csv (for residual extraction)
**File 4:** data/step01_ctt_scores.csv (for residual extraction)

**Processing:**

For EACH model (IRT-based, CTT-based), validate 7 assumptions:

1. **Linearity:** Residuals vs fitted values plot; expect random scatter around y=0
2. **Homoscedasticity:** Scale-location plot + Breusch-Pagan test (p > 0.05 indicates homoscedasticity)
3. **Normality of residuals:** Q-Q plot + Shapiro-Wilk test (p > 0.05 or visual assessment for n>50)
4. **Normality of random effects:** Q-Q plot for BLUPs + Shapiro-Wilk test
5. **Independence:** Residuals vs observation order plot + Durbin-Watson statistic (1.5-2.5 acceptable range)
6. **No multicollinearity:** VIF < 10 for all predictors (LocationType, log_TSVR, interaction)
7. **Influential observations:** Cook's distance < 1.0 for all observations

**Special Consideration for CTT Model (Bounded Outcome):**

CTT mean scores are bounded [0, 1], which MAY violate normality and homoscedasticity assumptions for standard LMM. If violations detected in CTT model:
- Document violations clearly
- Report that LMM results should be interpreted with caution
- Note: GLMM with logit link is alternative remedy (but not implemented here per 1_concept.md)

**Output:**

**File 1:** data/step04_assumptions_comparison.csv
**Format:** CSV, 14 rows (7 assumptions x 2 models)
**Columns:**
  - `model` (string: "IRT" or "CTT")
  - `assumption` (string: "Linearity", "Homoscedasticity", "Normality_residuals", "Normality_random_effects", "Independence", "Multicollinearity", "Influential_observations")
  - `test_statistic` (float64, if applicable: Breusch-Pagan chi-square, Shapiro W, Durbin-Watson, VIF max, Cook's D max)
  - `p_value` (float64, if applicable)
  - `threshold` (string, e.g., "p > 0.05", "VIF < 10", "Cook's D < 1.0")
  - `status` (string: "PASS" or "FAIL")
  - `notes` (string, additional context)
**Expected Rows:** 14 (7 assumptions x 2 models)

**File 2:** data/step04_assumption_diagnostics.txt
**Format:** Text file documenting detailed findings
**Content:**
  - Summary of violations per model
  - Recommendations (e.g., "CTT model violates homoscedasticity; interpret with caution")
  - Comparison of IRT vs CTT assumption performance

**Validation Requirement:**
Validation tools MUST be used after assumption validation. This is meta-validation (validation of the validation process). rq_tools will specify checks for: assumption_comparison.csv structure, all 14 rows present, status in {PASS, FAIL}.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_assumptions_comparison.csv: 14 rows x 7 columns
- data/step04_assumption_diagnostics.txt: Text file with interpretive summary (>200 characters)
- Data types: model (string), assumption (string), test_statistic (float64), p_value (float64), threshold (string), status (string), notes (string)

*Value Ranges:*
- test_statistic: Varies by test (chi-square >= 0, Shapiro W in [0,1], Durbin-Watson in [0,4], VIF >= 1, Cook's D >= 0)
- p_value in [0, 1] (when applicable)
- status in {"PASS", "FAIL"}

*Data Quality:*
- All 14 rows present (7 assumptions x 2 models)
- No NaN in test_statistic or p_value where applicable (some assumptions may not have p-values)
- Status correctly reflects test outcome (e.g., if p > 0.05 and threshold is "p > 0.05", status = PASS)
- Both models assessed on identical set of assumptions

*Log Validation:*
- Required pattern: "Validated 7 assumptions for IRT model"
- Required pattern: "Validated 7 assumptions for CTT model"
- Required pattern: "IRT model: {N_pass} PASS, {N_fail} FAIL"
- Required pattern: "CTT model: {N_pass} PASS, {N_fail} FAIL"
- If CTT violations: Required pattern: "CTT bounded outcome [0,1] may violate normality/homoscedasticity"
- Forbidden patterns: "ERROR", "Unable to compute assumption test"
- Acceptable warnings: "Shapiro-Wilk p < 0.05 for large sample (n=800) - visual Q-Q assessment recommended"

**Expected Behavior on Validation Failure:**
- If < 14 rows in assumption comparison table -> Raise error (incomplete validation)
- If major violations in BOTH models -> Log warning but continue (negative finding is valid)
- If unable to compute assumption tests -> Raise error (model fit issue)
- Log to logs/step04_validate_assumptions.log
- Continue to Step 5 even if assumptions violated (violations documented, not blockers)
- g_debug invoked only for computation errors, not assumption violations

---

### Step 5: Compare Fixed Effects between IRT and CTT Models

**Dependencies:** Step 3 (fitted models), Step 4 (assumption validation)
**Complexity:** Low (<5 minutes - coefficient extraction and comparison)

**Purpose:** Assess agreement between IRT-based and CTT-based LMM fixed effects to determine if both measurement approaches yield the same trajectory conclusions (convergent validity)

**Input:**

**File 1:** data/step03_irt_lmm_model.pkl (from Step 3)
**File 2:** data/step03_ctt_lmm_model.pkl (from Step 3)

**Processing:**

1. **Extract Fixed Effects from Both Models:**
   - For IRT model: Extract coefficient, SE, z-value, p-value for all 4 fixed effects
   - For CTT model: Extract coefficient, SE, z-value, p-value for all 4 fixed effects
   - Fixed effects: Intercept, LocationType[T.destination], log_TSVR, LocationType[T.destination]:log_TSVR

2. **Classify Agreement per Term:**
   - **Sign match:** Does coefficient have same sign (positive/negative) in both models? (bool)
   - **Significance match:** Are both significant at alpha=0.05 OR both non-significant? (bool)
   - **Agreement:** sign_match AND sig_match (bool)

3. **Compute Cohen's Kappa:**
   - Treat each fixed effect as a classification decision: {positive+sig, positive+nonsig, negative+sig, negative+nonsig}
   - Compute Cohen's kappa for agreement between IRT and CTT classifications
   - Threshold: kappa > 0.60 indicates "substantial agreement" per Landis & Koch (1977)

4. **Compute Overall Agreement Percentage:**
   - Percentage of fixed effects with sign_match = True AND sig_match = True
   - Threshold: >= 80% agreement expected

5. **Apply Decision D068 Dual P-Values:**
   - For each model, report both p_uncorrected and p_bonferroni (Bonferroni factor = 4 comparisons for 4 fixed effects)

**Output:**

**File 1:** data/step05_coefficient_comparison.csv
**Format:** CSV, 4 rows (one per fixed effect term)
**Columns:**
  - `term` (string: fixed effect name, e.g., "Intercept", "LocationType[T.destination]")
  - `irt_coef` (float64, coefficient from IRT model)
  - `irt_se` (float64, standard error from IRT model)
  - `irt_p_uncorrected` (float64, uncorrected p-value from IRT model)
  - `irt_p_bonferroni` (float64, Bonferroni-corrected p-value, min(irt_p x 4, 1.0))
  - `ctt_coef` (float64, coefficient from CTT model)
  - `ctt_se` (float64, standard error from CTT model)
  - `ctt_p_uncorrected` (float64, uncorrected p-value from CTT model)
  - `ctt_p_bonferroni` (float64, Bonferroni-corrected p-value, min(ctt_p x 4, 1.0))
  - `sign_match` (bool, True if both coefficients have same sign)
  - `sig_match` (bool, True if both significant at alpha=0.05 OR both non-significant)
  - `agreement` (bool, True if sign_match AND sig_match)
**Expected Rows:** 4 (fixed effects count)

**File 2:** data/step05_agreement_metrics.csv
**Format:** CSV, 1 row
**Columns:**
  - `cohens_kappa` (float64, Cohen's kappa statistic in [-1, 1], expected > 0.60)
  - `kappa_threshold_met` (bool, True if kappa > 0.60, False otherwise)
  - `overall_agreement_pct` (float64, percentage of terms with agreement=True, in [0, 100])
  - `agreement_threshold_met` (bool, True if overall_agreement_pct >= 80, False otherwise)
  - `n_terms` (int, number of fixed effects compared = 4)
  - `n_agreements` (int, count of terms with agreement=True)
**Expected Rows:** 1

**Validation Requirement:**
Validation tools MUST be used after fixed effects comparison. rq_tools will specify validation for: Decision D068 dual p-values present, Cohen's kappa in valid range, agreement percentage calculation correct.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_coefficient_comparison.csv: 4 rows x 12 columns
- data/step05_agreement_metrics.csv: 1 row x 6 columns
- Data types: term (string), coefficients (float64), p-values (float64), booleans (bool), kappa (float64), percentages (float64), counts (int64)

*Value Ranges:*
- irt_coef, ctt_coef: Unrestricted (can be positive/negative)
- irt_se, ctt_se > 0 (standard errors always positive)
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1], p_bonferroni >= p_uncorrected (correction cannot reduce p-value)
- cohens_kappa in [-1, 1] (correlation-like statistic)
- overall_agreement_pct in [0, 100]

*Data Quality:*
- Exactly 4 rows in coefficient comparison (4 fixed effects)
- All 4 terms present: Intercept, LocationType, log_TSVR, LocationType:log_TSVR (names may vary by coding)
- No NaN in coefficients, SE, p-values
- Bonferroni formula correct: p_bonferroni = min(p_uncorrected x 4, 1.0)
- agreement = (sign_match AND sig_match) computed correctly
- n_agreements = sum of agreement column
- overall_agreement_pct = (n_agreements / 4) x 100
- Cohen's kappa computed correctly (use sklearn.metrics.cohen_kappa_score or manual computation)

*Log Validation:*
- Required pattern: "Extracted fixed effects: 4 terms from IRT model, 4 terms from CTT model"
- Required pattern: "Cohen's kappa = {kappa:.3f} (threshold: > 0.60)"
- Required pattern: "Overall agreement = {pct:.1f}% (threshold: >= 80%)"
- Required pattern: "Decision D068 dual p-values reported: uncorrected + Bonferroni"
- Required pattern: "Bonferroni correction factor: 4 comparisons"
- If thresholds met: Required pattern: "Convergence criteria MET: kappa > 0.60 AND agreement >= 80%"
- If thresholds NOT met: Required pattern: "Convergence criteria NOT met"
- Forbidden patterns: "ERROR", "NaN in kappa", "p_bonferroni < p_uncorrected"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- If row count != 4 -> Raise error (fixed effects count mismatch)
- If p_bonferroni < p_uncorrected -> Raise error (Bonferroni formula incorrect)
- If kappa outside [-1, 1] -> Raise error (kappa computation error)
- If agreement_pct outside [0, 100] -> Raise error (percentage computation error)
- If kappa < 0.60 OR agreement_pct < 80 -> Log warning "Convergence thresholds NOT met" but continue (negative finding is valid result)
- Log failure to logs/step05_compare_fixed_effects.log
- Quit on computation errors, continue on negative findings
- g_debug invoked for computation errors only

---

### Step 6: Compare Model Fit (AIC, BIC)

**Dependencies:** Step 3 (fitted models with AIC/BIC)
**Complexity:** Low (<2 minutes - simple arithmetic comparison)

**Purpose:** Compare model fit indices (AIC, BIC) between IRT-based and CTT-based LMMs to assess whether both measurement approaches yield equivalent trajectory model quality

**Input:**

**File 1:** data/step03_irt_lmm_model.pkl (from Step 3)
**File 2:** data/step03_ctt_lmm_model.pkl (from Step 3)

**Processing:**

1. Extract AIC and BIC from both models
2. Compute �AIC = AIC_ctt - AIC_irt
3. Compute �BIC = BIC_ctt - BIC_irt
4. Interpret per Burnham & Anderson (2002):
   - |�| < 2: Models essentially equivalent
   - 2 <= |�| < 10: Some support for better model
   - |�| >= 10: Strong support for better model
5. Note: NEGATIVE � means IRT model fits better, POSITIVE � means CTT model fits better

**Output:**

**File:** data/step06_model_fit_comparison.csv
**Format:** CSV, 1 row
**Columns:**
  - `irt_aic` (float64, AIC for IRT-based model)
  - `irt_bic` (float64, BIC for IRT-based model)
  - `ctt_aic` (float64, AIC for CTT-based model)
  - `ctt_bic` (float64, BIC for CTT-based model)
  - `delta_aic` (float64, AIC_ctt - AIC_irt)
  - `delta_bic` (float64, BIC_ctt - BIC_irt)
  - `aic_interpretation` (string: "Equivalent" if |�| < 2, "Some support for IRT" if � < -2, "Some support for CTT" if � > 2, "Strong support for IRT" if � < -10, "Strong support for CTT" if � > 10)
  - `bic_interpretation` (string: same logic as AIC)
**Expected Rows:** 1

**Validation Requirement:**
Validation tools MUST be used after model fit comparison. rq_tools will specify validation for: AIC/BIC finite values, delta computation correct, interpretation logic valid.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_model_fit_comparison.csv: 1 row x 8 columns
- Data types: float64 for AIC/BIC/deltas, string for interpretations

*Value Ranges:*
- irt_aic, irt_bic, ctt_aic, ctt_bic: Finite values (not NaN, not inf)
- AIC and BIC typically negative for LMMs (log-likelihood based)
- delta_aic, delta_bic: Unrestricted (can be positive or negative)

*Data Quality:*
- All AIC/BIC values finite
- delta_aic = ctt_aic - irt_aic (formula correct)
- delta_bic = ctt_bic - irt_bic (formula correct)
- aic_interpretation matches delta_aic value per Burnham & Anderson thresholds
- bic_interpretation matches delta_bic value per Burnham & Anderson thresholds

*Log Validation:*
- Required pattern: "IRT model - AIC: {irt_aic:.2f}, BIC: {irt_bic:.2f}"
- Required pattern: "CTT model - AIC: {ctt_aic:.2f}, BIC: {ctt_bic:.2f}"
- Required pattern: "�AIC = {delta_aic:.2f}, �BIC = {delta_bic:.2f}"
- Required pattern: "AIC interpretation: {interpretation}"
- Required pattern: "BIC interpretation: {interpretation}"
- Forbidden patterns: "ERROR", "NaN in AIC", "Infinite BIC"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- If NaN or inf in AIC/BIC -> Raise error (model fit failed)
- If delta computation incorrect -> Raise error (arithmetic error)
- If interpretation doesn't match delta value -> Raise error (logic error)
- Log failure to logs/step06_compare_model_fit.log
- Quit script immediately
- g_debug invoked to diagnose

---

### Step 7: Prepare Scatterplot Data (IRT vs CTT)

**Dependencies:** Step 0 (IRT theta), Step 1 (CTT scores)
**Complexity:** Low (<2 minutes - data merging only)

**Purpose:** Create plot source CSV for scatterplot showing IRT theta vs CTT mean score for all 800 observations, colored by location type (source, destination)

**Input:**

**File 1:** data/step00_irt_theta_from_rq551.csv (from Step 0)
**Columns:** composite_ID, UID, test, location_type, irt_theta

**File 2:** data/step01_ctt_scores.csv (from Step 1)
**Columns:** composite_ID, location_type, ctt_mean_score

**Processing:**

1. Merge IRT theta and CTT scores on composite_ID + location_type
2. Select columns for plotting: UID, test, location_type, irt_theta, ctt_mean_score
3. Validate: 800 rows (100 participants x 4 tests x 2 location types)
4. Sort by location_type, then UID, then test (for consistent plotting order)

**Output:**

**File:** data/step07_scatterplot_data.csv
**Format:** CSV, plot source data
**Columns:**
  - `UID` (string)
  - `test` (string)
  - `location_type` (string: "source" or "destination")
  - `irt_theta` (float64, x-axis variable)
  - `ctt_mean_score` (float64, y-axis variable)
**Expected Rows:** 800 (100 participants x 4 tests x 2 location types)

**Note:** This CSV is read by rq_plots agent later. The actual PNG scatterplot is generated by rq_plots and saved to plots/ folder.

**Validation Requirement:**
Validation tools MUST be used after plot data preparation. rq_tools will specify validation for: row count (800), column presence, value ranges, no NaN in critical columns.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_scatterplot_data.csv: 800 rows x 5 columns
- Data types: UID (string), test (string), location_type (string), irt_theta (float64), ctt_mean_score (float64)

*Value Ranges:*
- irt_theta in [-3, 3] (typical IRT ability range)
- ctt_mean_score in [0, 1] (proportion correct)

*Data Quality:*
- Exactly 800 rows (100 participants x 4 tests x 2 location types)
- No NaN in irt_theta or ctt_mean_score (both required for scatterplot)
- Location type balance: 400 rows for "source", 400 rows for "destination"
- All UIDs present (100 unique participants)
- All tests present (T1, T2, T3, T4)

*Log Validation:*
- Required pattern: "Prepared scatterplot data: 800 rows"
- Required pattern: "Location types: source (400), destination (400)"
- Required pattern: "No missing values in irt_theta or ctt_mean_score"
- Forbidden patterns: "ERROR", "NaN detected", "Row count mismatch"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- If row count != 800 -> Raise error (missing data)
- If NaN in irt_theta or ctt_mean_score -> Raise error (incomplete data)
- If location type imbalance -> Raise error (data loss for one location type)
- Log failure to logs/step07_prepare_scatterplot_data.log
- Quit script immediately
- g_debug invoked to diagnose

---

### Step 8: Prepare Trajectory Comparison Data (IRT vs CTT Over Time)

**Dependencies:** Step 0 (IRT theta + TSVR), Step 1 (CTT scores + TSVR)
**Complexity:** Low (5 minutes - aggregation by location type x test x method)

**Purpose:** Create plot source CSV for trajectory comparison plot showing mean IRT theta and mean CTT score over time (4 tests) for both location types (source, destination), demonstrating whether IRT and CTT yield parallel forgetting trajectories

**Input:**

**File 1:** data/step00_irt_theta_from_rq551.csv (from Step 0)
**Columns:** location_type, test, irt_theta, TSVR_hours

**File 2:** data/step01_ctt_scores.csv (from Step 1)
**Columns:** location_type, test, ctt_mean_score, TSVR_hours

**Processing:**

1. **Aggregate IRT Data:**
   - Group by location_type + test
   - Compute mean(irt_theta), mean(TSVR_hours), 95% CI for theta
   - Create column: method = "IRT"

2. **Aggregate CTT Data:**
   - Group by location_type + test
   - Compute mean(ctt_mean_score), mean(TSVR_hours), 95% CI for ctt_mean_score
   - Create column: method = "CTT"

3. **Stack Both Datasets:**
   - Combine IRT and CTT aggregated data
   - Result: 16 rows (2 location types x 4 tests x 2 methods)

4. **Compute 95% Confidence Intervals:**
   - For IRT: CI based on SE(mean(theta)) = SD(theta) / sqrt(n)
   - For CTT: CI based on SE(mean(ctt)) = SD(ctt) / sqrt(n)
   - CI_lower = mean - 1.96 x SE
   - CI_upper = mean + 1.96 x SE

**Output:**

**File:** data/step08_trajectory_comparison_data.csv
**Format:** CSV, plot source data
**Columns:**
  - `location_type` (string: "source" or "destination")
  - `test` (string: T1, T2, T3, T4)
  - `method` (string: "IRT" or "CTT")
  - `mean_score` (float64, mean theta or mean CTT score)
  - `ci_lower` (float64, lower 95% confidence bound)
  - `ci_upper` (float64, upper 95% confidence bound)
  - `time` (float64, mean TSVR_hours for this location x test group)
  - `n` (int, number of observations contributing to mean = 100 participants)
**Expected Rows:** 16 (2 location types x 4 tests x 2 methods)

**Note:** This CSV is read by rq_plots agent later. The actual PNG trajectory comparison plot is generated by rq_plots and saved to plots/ folder.

**Validation Requirement:**
Validation tools MUST be used after plot data preparation. rq_tools will specify validation for: row count (16), all location x test x method combinations present, CI_upper > CI_lower, no NaN.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_trajectory_comparison_data.csv: 16 rows x 8 columns
- Data types: location_type (string), test (string), method (string), mean_score (float64), ci_lower (float64), ci_upper (float64), time (float64), n (int64)

*Value Ranges:*
- mean_score: Unrestricted (IRT: typically [-3, 3], CTT: [0, 1])
- ci_lower, ci_upper: Unrestricted but must satisfy ci_upper > ci_lower
- time in [0, 168] hours (0=encoding, 168=1 week)
- n = 100 for all rows (all participants contribute to all location x test aggregates)

*Data Quality:*
- Exactly 16 rows (2 locations x 4 tests x 2 methods)
- All combinations present: {"source", "destination"} x {T1, T2, T3, T4} x {"IRT", "CTT"}
- No NaN in mean_score, ci_lower, ci_upper, time (all required for trajectory plot)
- CI bounds valid: ci_upper > ci_lower for all rows
- n = 100 for all rows (no missing participants)
- IRT mean_score in [-3, 3] for all IRT rows
- CTT mean_score in [0, 1] for all CTT rows

*Log Validation:*
- Required pattern: "Aggregated IRT data: 8 groups (2 locations x 4 tests)"
- Required pattern: "Aggregated CTT data: 8 groups (2 locations x 4 tests)"
- Required pattern: "Stacked trajectory data: 16 rows"
- Required pattern: "All confidence intervals valid: CI_upper > CI_lower"
- Required pattern: "Sample size per group: n = 100"
- Forbidden patterns: "ERROR", "NaN in trajectory data", "CI_upper <= CI_lower", "Missing location x test x method combination"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- If row count != 16 -> Raise error (missing location x test x method combination)
- If NaN in mean_score, ci_lower, ci_upper, time -> Raise error (aggregation failed)
- If ci_upper <= ci_lower for any row -> Raise error (confidence interval computation error)
- If n != 100 for any row -> Raise error (participant data loss)
- If IRT mean_score outside [-4, 4] -> Raise warning "IRT theta outside typical range, check calibration"
- If CTT mean_score outside [0, 1] -> Raise error (CTT scores must be proportions)
- Log failure to logs/step08_prepare_trajectory_comparison_data.log
- Quit on errors, continue on warnings
- g_debug invoked for errors only

---

## Expected Data Formats

### Composite ID Format

**Pattern:** `{UID}_{test}`
**Example:** `P001_T1`, `P042_T3`
**Purpose:** Unique identifier for participant-test combination, used for merging across datasets

### Location Type Coding

**Values:** {"source", "destination"}
- `source` = Pick-up location memory (-U- tags)
- `destination` = Put-down location memory (-D- tags)
**Purpose:** Factor variable for location type comparisons in correlations and LMMs

### TSVR Time Variable (Decision D070)

**Column Name:** `TSVR_hours`
**Range:** [0, 168] hours (0 = encoding session, 168 = 1 week post-encoding)
**Purpose:** Actual elapsed time since VR session, NOT nominal days (0, 1, 3, 6)
**Transformation:** `log_TSVR = log(TSVR_hours + 1)` to handle TSVR=0 at encoding

### IRT Theta Scores

**Columns:** `theta_source`, `theta_destination` (wide format) OR `irt_theta` (long format)
**Range:** Typically [-3, 3] (standard normal scale for IRT abilities)
**Interpretation:** Higher theta = higher spatial memory ability for that location type

### CTT Mean Scores

**Column:** `ctt_mean_score`
**Range:** [0, 1] (proportion correct across purified items)
**Computation:** Mean of binary responses (0/1) across items, ignoring NaN
**Interpretation:** Higher score = higher accuracy for that location type

### LMM Fixed Effects Terms

**Standard Naming (statsmodels):**
- `Intercept` (reference group mean at time=0)
- `LocationType[T.destination]` (Treatment coding: difference from Source reference)
- `log_TSVR` (time slope)
- `LocationType[T.destination]:log_TSVR` (interaction: difference in slopes)

**Note:** Exact naming depends on pandas DataFrame column names and statsmodels formula parser

---

## Cross-RQ Dependencies

### Dependency Type: DERIVED Data from RQ 5.5.1

**This RQ requires outputs from:**
- **RQ 5.5.1** (Source-Destination Trajectories - ROOT RQ for Type 5.5)
  - File 1: results/ch5/5.5.1/data/step03_theta_scores.csv (IRT theta scores, 400 rows)
  - File 2: results/ch5/5.5.1/data/step02_purified_items.csv (list of items retained after Decision D039 purification)
  - File 3: results/ch5/5.5.1/data/step00_tsvr_mapping.csv (time-since-VR hours, 400 rows)
  - Used in: Step 0 (load IRT theta, purified items, TSVR)
  - Rationale: RQ 5.5.1 establishes source-destination memory dissociation using IRT. This RQ validates findings are robust to measurement approach by comparing IRT to CTT computed on the SAME purified item set.

**This RQ also requires:**
- **data/cache/dfData.csv** (project-level master VR dataset)
  - Used in: Step 0 (filter to purified items, compute CTT scores)
  - Rationale: Raw binary responses needed to compute CTT mean scores

**Execution Order Constraint:**
1. RQ 5.5.1 must complete through Step 3 (IRT Pass 2, theta extraction) before this RQ can run
2. This RQ does NOT require RQ 5.5.1 Steps 4-7 (LMM trajectory modeling) - only the IRT calibration outputs

**Data Source Boundaries:**
- **DERIVED data:** IRT theta scores, purified items list, TSVR mapping (from RQ 5.5.1)
- **RAW data:** Binary item responses (from dfData.csv, filtered to purified items)
- **Scope:** This RQ does NOT re-calibrate IRT models (uses RQ 5.5.1 theta as given)
- This RQ DOES perform new LMM fitting (parallel IRT-based and CTT-based models)

**Validation:**
- Step 0: Check results/ch5/5.5.1/data/step03_theta_scores.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch5/5.5.1/data/step02_purified_items.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 0: Check results/ch5/5.5.1/data/step00_tsvr_mapping.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- If any file missing -> quit with error -> user must execute RQ 5.5.1 first

---

## Validation Requirements

### CRITICAL MANDATE

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

| Step | Analysis | Validation Criteria (Summary) |
|------|----------|-------------------------------|
| 0 | Load dependencies from RQ 5.5.1 | Files exist, row counts match (theta: 400, items: 25-32, tsvr: 400), theta in [-3,3], TSVR in [0,168], no NaN |
| 1 | Compute CTT mean scores | Scores in [0,1], 800 rows, no NaN, location balance (400+400), item counts > 0 |
| 2 | Pearson correlations | r in [-1,1], p in [0,1], dual p-values (Decision D068), Bonferroni correct, 3 rows |
| 3 | Fit parallel LMMs | Both converge OR both simplified identically, AIC/BIC finite, 4 fixed effects, random variances >= 0 |
| 4 | Validate LMM assumptions | 14 rows (7 assumptions x 2 models), status in {PASS, FAIL}, test statistics valid |
| 5 | Compare fixed effects | 4 terms, dual p-values (Decision D068), kappa in [-1,1], agreement_pct in [0,100] |
| 6 | Compare model fit | AIC/BIC finite, delta computation correct, interpretation matches thresholds |
| 7 | Prepare scatterplot data | 800 rows, theta in [-3,3], ctt in [0,1], no NaN, location balance |
| 8 | Prepare trajectory data | 16 rows, CI_upper > CI_lower, n=100 for all, IRT in [-3,3], CTT in [0,1] |

**NOTE:** Technical validation (files exist, formats correct, values in bounds) checked by validation tools DURING analysis execution. Substance validation (all criteria above) checked by rq_inspect POST-execution.

---

## Summary

**Total Steps:** 8 analysis steps (Step 0: dependency loading + Steps 1-8: analyses)

**Estimated Runtime:** Medium complexity (~30-60 minutes total)
- Step 0: Low (<5 min)
- Step 1: Low (<5 min)
- Step 2: Low (<5 min)
- Step 3: Medium (10-20 min - two LMM fits)
- Step 4: Medium (10-15 min - 7 assumptions x 2 models)
- Step 5: Low (<5 min)
- Step 6: Low (<2 min)
- Step 7: Low (<2 min)
- Step 8: Low (5 min)

**Cross-RQ Dependencies:** RQ 5.5.1 (IRT theta scores, purified items, TSVR mapping)

**Primary Outputs:**
- data/step01_ctt_scores.csv (800 rows: CTT mean scores per participant x test x location type)
- data/step02_correlations.csv (3 rows: Source, Destination, Overall r > 0.70 convergence)
- data/step05_agreement_metrics.csv (Cohen's kappa > 0.60, agreement >= 80%)
- data/step06_model_fit_comparison.csv (AIC/BIC comparison for IRT vs CTT models)
- data/step07_scatterplot_data.csv (800 rows: IRT vs CTT scatterplot)
- data/step08_trajectory_comparison_data.csv (16 rows: trajectory comparison over time)

**Validation Coverage:** 100% (all 8 steps have validation requirements with 4-layer substance criteria)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni) for correlations, fixed effects comparisons
- Decision D070: TSVR (actual hours) as time variable in LMMs (inherited from RQ 5.5.1)
- Decision D039: CTT computed on purified item set only (items passing IRT quality criteria in RQ 5.5.1)

**Success Criteria:**
- All three correlations (Source, Destination, Overall) exceed r > 0.70 threshold
- Cohen's kappa for LMM fixed effects agreement exceeds 0.60 (substantial agreement)
- Overall classification agreement >= 80%
- Both IRT-based and CTT-based LMMs converge with identical model structure
- Dual p-values reported for all statistical tests (Decision D068)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-04): Initial plan created by rq_planner agent for RQ 5.5.4
