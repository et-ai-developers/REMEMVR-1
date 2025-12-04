# Analysis Plan: RQ 5.5.6 - Source-Destination Variance Decomposition

**Research Question:** 5.5.6
**Created:** 2025-12-04
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines variance decomposition for source (-U-, pick-up locations) and destination (-D-, put-down locations) memory across 100 participants and 4 test sessions. The analysis quantifies the proportion of individual differences attributable to stable between-person traits (intercepts and slopes) versus within-person measurement error using Intraclass Correlation Coefficients (ICC).

**Pipeline:** LMM variance decomposition (location-stratified models)

**Steps:** 6 analysis steps

**Estimated Runtime:** Medium (15-30 minutes total - 2 LMM fits + variance component extraction + ICC computation + correlation tests + comparison)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni) for intercept-slope correlations
- Decision D070: TSVR as time variable (inherited from RQ 5.5.1 best-fit transformation)

**Critical Dependencies:**
- RQ 5.5.1 must be complete (all agents status = success)
- Requires RQ 5.5.1 LMM input data (theta scores + TSVR merged)
- Uses best-fit time transformation identified in RQ 5.5.1

**Critical Outputs:**
- 200 random effects (100 UID x 2 locations) REQUIRED for downstream RQ 5.5.7 (clustering analysis)

---

## Analysis Plan

This RQ requires 6 analysis steps:

### Step 1: Fit Location-Stratified LMMs with Random Slopes

**Dependencies:** None (first step, uses RQ 5.5.1 outputs)

**Complexity:** Medium (5-10 minutes per model, 2 models total)

**Purpose:** Fit separate Linear Mixed Models for Source (-U-) and Destination (-D-) locations, each with random intercepts and slopes to estimate variance components.

**Input:**

**File 1:** results/ch5/5.5.1/data/step04_lmm_input.csv
**Source:** RQ 5.5.1 Step 4 (theta scores merged with TSVR)
**Format:** CSV, long format (one row per observation)
**Columns:**
  - `UID` (string, participant identifier, format: P### with leading zeros)
  - `test` (string, test session: T1, T2, T3, T4)
  - `location` (string, categorical: Source, Destination)
  - `theta` (float, IRT ability estimate for location type)
  - `SE` (float, standard error of theta estimate)
  - `TSVR_hours` (float, actual time since encoding in hours)
  - `log_TSVR` (float, log-transformed TSVR if best-fit transformation from RQ 5.5.1)
**Expected Rows:** 800 (100 UID x 4 tests x 2 locations)
**Expected Values:**
  - location in {Source, Destination}
  - theta in [-3, 3] (IRT ability range)
  - TSVR_hours in [0, 168] (0 = encoding, 168 = 1 week)

**Processing:**

**Model Formula (per location):**
```
theta ~ time_variable + (time_variable | UID)
```

Where:
- `time_variable` = best-fit transformation from RQ 5.5.1 (e.g., log_TSVR, TSVR_hours, sqrt_TSVR)
- Random effects: `(time_variable | UID)` = random intercepts AND random slopes per participant
- Fixed effects: Single time predictor (no location interaction, models fitted separately)

**Stratification:**
- Filter data WHERE location == "Source" -> Fit Source LMM
- Filter data WHERE location == "Destination" -> Fit Destination LMM

**Statistical Method:**
- Linear Mixed Model using statsmodels.formula.api.mixedlm
- REML estimation (not ML, for unbiased variance component estimates)
- Convergence tolerance: default statsmodels settings
- Expected: Both models converge successfully (converged=True)

**Output:**

**File 1:** data/step01_model_metadata_source.yaml
**Format:** YAML metadata file
**Contents:**
  - model_converged: boolean (True/False)
  - n_observations: int (400 expected, 100 UID x 4 tests)
  - n_participants: int (100 expected)
  - time_variable_used: string (e.g., "log_TSVR")
  - formula: string (exact model formula used)

**File 2:** data/step01_model_metadata_destination.yaml
**Format:** Same as File 1, for Destination model

**File 3:** data/step01_source_lmm_model.pkl
**Format:** Pickled statsmodels MixedLM results object
**Purpose:** Saved Source model for downstream variance extraction

**File 4:** data/step01_destination_lmm_model.pkl
**Format:** Pickled statsmodels MixedLM results object
**Purpose:** Saved Destination model for downstream variance extraction

**Validation Requirement:**

Validation tools MUST be used after LMM fitting tool execution. Specific validation tools will be determined by rq_tools based on LMM convergence and model diagnostics requirements. The rq_analysis agent will embed validation tool calls after the analysis tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_model_metadata_source.yaml: exists, valid YAML structure
- data/step01_model_metadata_destination.yaml: exists, valid YAML structure
- data/step01_source_lmm_model.pkl: exists, size > 10 KB (non-empty model)
- data/step01_destination_lmm_model.pkl: exists, size > 10 KB (non-empty model)

*Value Ranges:*
- model_converged: True (both models)
- n_observations: 400 (100 UID x 4 tests per location)
- n_participants: 100
- time_variable_used: non-empty string matching RQ 5.5.1 specification

*Data Quality:*
- Both models must converge (no convergence failures tolerated)
- No singular fit warnings in metadata (indicates collinearity issues)
- Expected N: Exactly 100 participants per model (no data loss)

*Log Validation:*
- Required pattern: "Source model converged: True"
- Required pattern: "Destination model converged: True"
- Required pattern: "VALIDATION - PASS: LMM convergence"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "Singular fit detected"
- Acceptable warnings: None expected for well-specified models

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Source model did not converge")
- Log failure to logs/step01_fit_location_stratified_lmms.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked by master to diagnose root cause (common issues: insufficient data per location, time variable misspecification)

---

### Step 2: Extract Variance Components from LMMs

**Dependencies:** Step 1 (requires fitted Source and Destination models)

**Complexity:** Low (1-2 minutes, extraction from saved models)

**Purpose:** Extract variance-covariance components from random effects structure for both location types.

**Input:**

**File 1:** data/step01_source_lmm_model.pkl
**Source:** Step 1 output
**Format:** Pickled statsmodels MixedLM results object
**Contents:** Fitted Source LMM with random effects covariance matrix

**File 2:** data/step01_destination_lmm_model.pkl
**Source:** Step 1 output
**Format:** Pickled statsmodels MixedLM results object
**Contents:** Fitted Destination LMM with random effects covariance matrix

**Processing:**

**Extract 5 variance components per location:**

1. **var_intercept:** Variance of random intercepts (between-person baseline differences)
   - Extracted from: `model.cov_re.iloc[0, 0]` (intercept variance on diagonal)
   - Interpretation: Larger values indicate greater stable individual differences in baseline memory

2. **var_slope:** Variance of random slopes (between-person differences in forgetting rate)
   - Extracted from: `model.cov_re.iloc[1, 1]` (slope variance on diagonal)
   - Interpretation: Expected to be near zero per universal Chapter 5 pattern (ICC_slope ~0)

3. **cov_int_slope:** Covariance between random intercepts and slopes
   - Extracted from: `model.cov_re.iloc[0, 1]` (off-diagonal element)
   - Interpretation: Correlation tested in Step 5 (high baseline -> faster/slower decline?)

4. **var_residual:** Residual variance (within-person measurement error)
   - Extracted from: `model.scale` (residual variance parameter)
   - Interpretation: Unexplained variance after accounting for fixed + random effects

5. **correlation_int_slope:** Correlation between random intercepts and slopes
   - Computed from: `cov_int_slope / (sqrt(var_intercept) x sqrt(var_slope))`
   - Interpretation: Bounded in [-1, 1], tested for significance in Step 5

**Output:**

**File 1:** data/step02_variance_components.csv
**Format:** CSV, one row per component per location
**Columns:**
  - `location` (string, categorical: Source, Destination)
  - `component` (string, categorical: var_intercept, var_slope, cov_int_slope, var_residual, correlation_int_slope)
  - `value` (float, variance/covariance/correlation estimate)
**Expected Rows:** 10 (5 components x 2 locations)
**Expected Values:**
  - var_intercept > 0 (strictly positive)
  - var_slope >= 0 (non-negative, expected near zero)
  - var_residual > 0 (strictly positive)
  - correlation_int_slope in [-1, 1] (bounded correlation)

**Validation Requirement:**

Validation tools MUST be used after variance component extraction tool execution. Specific validation tools will be determined by rq_tools based on variance positivity checks and correlation bounds. The rq_analysis agent will embed validation tool calls after the analysis tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_variance_components.csv: exists
- Expected rows: 10 (5 components x 2 locations)
- Expected columns: 3 (location, component, value)
- Data types: location (object), component (object), value (float64)

*Value Ranges:*
- var_intercept > 0 (both locations)
- var_slope >= 0 (both locations, expected <0.05 per universal pattern)
- var_residual > 0 (both locations)
- correlation_int_slope in [-1, 1] (both locations)
- No NaN or inf values tolerated

*Data Quality:*
- All 10 rows present (no missing components)
- All 5 components present for BOTH locations
- No negative variances (Heywood cases indicate model misspecification)
- No duplicate location-component pairs

*Log Validation:*
- Required pattern: "Extracted 5 components for Source"
- Required pattern: "Extracted 5 components for Destination"
- Required pattern: "VALIDATION - PASS: Variance positivity"
- Forbidden patterns: "ERROR", "Negative variance detected", "NaN in variance components"
- Acceptable warnings: "var_slope near zero (expected per Chapter 5 pattern)"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Negative var_intercept for Source: -0.05")
- Log failure to logs/step02_extract_variance_components.log
- Quit script immediately (do NOT proceed to Step 3)
- g_debug invoked (common causes: model convergence issues, singular fit)

---

### Step 3: Compute ICC Estimates

**Dependencies:** Step 2 (requires variance components extracted)

**Complexity:** Low (1-2 minutes, arithmetic computation from variance components)

**Purpose:** Compute 3 Intraclass Correlation Coefficient estimates per location to quantify proportion of variance attributable to between-person differences.

**Input:**

**File 1:** data/step02_variance_components.csv
**Source:** Step 2 output
**Format:** CSV with columns: location, component, value
**Expected Rows:** 10 (5 components x 2 locations)

**Processing:**

**Compute 3 ICC estimates per location:**

1. **ICC_intercept:** Proportion of total variance in baseline ability attributable to stable between-person differences
   - Formula: `var_intercept / (var_intercept + var_residual)`
   - Interpretation: ICC > 0.40 indicates substantial trait-like stability (Cicchetti, 1994)
   - Expected range: 0.30-0.60 per hypothesis

2. **ICC_slope_simple:** Proportion of total variance in slopes attributable to between-person differences (simple calculation)
   - Formula: `var_slope / (var_slope + var_residual)`
   - Interpretation: Expected near zero (<0.02) per universal Chapter 5 pattern
   - Caveat: Denominator may be unstable if var_slope ~0

3. **ICC_slope_conditional:** Conditional ICC for slopes at specific timepoint (Day 6 post-encoding)
   - Formula: `(var_intercept + 2 x cov_int_slope x time + var_slope x time^2) / (var_intercept + 2 x cov_int_slope x time + var_slope x time^2 + var_residual)`
   - Where `time` = Day 6 timepoint in units of best-fit transformation
   - Interpretation: Accounts for intercept-slope covariance, more accurate than ICC_slope_simple
   - Expected: Similar to ICC_slope_simple (both near zero)

**Output:**

**File 1:** data/step03_icc_estimates.csv
**Format:** CSV, one row per ICC type per location
**Columns:**
  - `location` (string, categorical: Source, Destination)
  - `icc_type` (string, categorical: ICC_intercept, ICC_slope_simple, ICC_slope_conditional)
  - `value` (float, ICC estimate in [0, 1])
  - `interpretation` (string, categorical: Poor <0.40, Fair 0.40-0.59, Good 0.60-0.74, Excellent >=0.75 per Cicchetti 1994)
**Expected Rows:** 6 (3 ICC types x 2 locations)
**Expected Values:**
  - ICC_intercept in [0.30, 0.60] (moderate stability)
  - ICC_slope_simple in [0, 0.05] (near zero, expected <0.02)
  - ICC_slope_conditional in [0, 0.05] (near zero, similar to ICC_slope_simple)

**Validation Requirement:**

Validation tools MUST be used after ICC computation tool execution. Specific validation tools will be determined by rq_tools based on ICC bounds checking and interpretation thresholds. The rq_analysis agent will embed validation tool calls after the analysis tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_icc_estimates.csv: exists
- Expected rows: 6 (3 ICC types x 2 locations)
- Expected columns: 4 (location, icc_type, value, interpretation)
- Data types: location (object), icc_type (object), value (float64), interpretation (object)

*Value Ranges:*
- All ICC values in [0, 1] (by definition)
- ICC_intercept expected in [0.20, 0.70] (plausible range for episodic memory)
- ICC_slope_simple expected in [0, 0.05] (near zero per hypothesis)
- ICC_slope_conditional expected in [0, 0.05] (similar to ICC_slope_simple)

*Data Quality:*
- All 6 rows present (no missing ICC types)
- All 3 ICC types present for BOTH locations
- No NaN values (ICC undefined if variance components invalid)
- Interpretation categories match Cicchetti (1994) thresholds exactly

*Log Validation:*
- Required pattern: "ICC_intercept (Source): 0.XX (interpretation)"
- Required pattern: "ICC_intercept (Destination): 0.XX (interpretation)"
- Required pattern: "ICC_slope near zero for both locations (expected pattern)"
- Required pattern: "VALIDATION - PASS: ICC bounds"
- Forbidden patterns: "ERROR", "ICC out of bounds", "NaN in ICC estimates"
- Acceptable warnings: None expected

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "ICC_intercept > 1.0 for Source: 1.15")
- Log failure to logs/step03_compute_icc_estimates.log
- Quit script immediately (do NOT proceed to Step 4)
- g_debug invoked (common causes: variance component extraction error, formula implementation bug)

---

### Step 4: Extract Individual Random Effects (CRITICAL for RQ 5.5.7)

**Dependencies:** Step 1 (requires fitted LMM models with random effects)

**Complexity:** Low (1-2 minutes, extraction from saved models)

**Purpose:** Extract individual participant random intercepts and slopes for BOTH locations. These 200 random effects (100 UID x 2 locations) are REQUIRED inputs for RQ 5.5.7 (clustering analysis).

**Input:**

**File 1:** data/step01_source_lmm_model.pkl
**Source:** Step 1 output
**Format:** Pickled statsmodels MixedLM results object
**Contents:** Fitted Source LMM with random effects per UID

**File 2:** data/step01_destination_lmm_model.pkl
**Source:** Step 1 output
**Format:** Pickled statsmodels MixedLM results object
**Contents:** Fitted Destination LMM with random effects per UID

**Processing:**

**Extract random effects per location:**

For Source model:
- `model.random_effects` returns dict: {UID: [intercept, slope]} for all 100 participants
- Convert to DataFrame with columns: UID, intercept, slope, location="Source"

For Destination model:
- `model.random_effects` returns dict: {UID: [intercept, slope]} for all 100 participants
- Convert to DataFrame with columns: UID, intercept, slope, location="Destination"

**Concatenate both DataFrames:**
- Stack vertically (rbind)
- Result: 200 rows (100 UID x 2 locations)

**Output:**

**File 1:** data/step04_random_effects.csv
**Format:** CSV, one row per UID per location
**Columns:**
  - `UID` (string, participant identifier, format: P### with leading zeros)
  - `location` (string, categorical: Source, Destination)
  - `random_intercept` (float, participant-specific deviation from fixed intercept)
  - `random_slope` (float, participant-specific deviation from fixed slope)
**Expected Rows:** 200 (100 UID x 2 locations)
**Expected Values:**
  - random_intercept: approximately normal distribution centered at 0
  - random_slope: approximately normal distribution centered at 0, small variance (expected near zero per ICC_slope pattern)
  - UID: All 100 participants present for BOTH locations (no missing)

**CRITICAL NOTE:**
This file is a REQUIRED input for RQ 5.5.7 (K-means clustering on random effects). RQ 5.5.7 cannot proceed without this file. The 200 random effects represent individual participant memory profiles (baseline ability + forgetting rate) stratified by location type.

**Validation Requirement:**

Validation tools MUST be used after random effects extraction tool execution. Specific validation tools will be determined by rq_tools based on data completeness and random effects distribution checks. The rq_analysis agent will embed validation tool calls after the analysis tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_random_effects.csv: exists
- Expected rows: 200 (100 UID x 2 locations)
- Expected columns: 4 (UID, location, random_intercept, random_slope)
- Data types: UID (object), location (object), random_intercept (float64), random_slope (float64)

*Value Ranges:*
- random_intercept typically in [-2, 2] (participant deviations from mean baseline)
- random_slope typically in [-0.5, 0.5] (small deviations, expected low variance)
- No extreme outliers (|random_intercept| > 5 suggests model issue)
- No NaN or inf values tolerated

*Data Quality:*
- Exactly 200 rows (100 UID x 2 locations, no missing)
- All 100 UID present for Source (no data loss)
- All 100 UID present for Destination (no data loss)
- No duplicate UID-location pairs
- random_intercept approximately normal (Shapiro-Wilk p > 0.01 acceptable)
- random_slope approximately normal (Shapiro-Wilk p > 0.01 acceptable)

*Log Validation:*
- Required pattern: "Extracted 100 random effects for Source"
- Required pattern: "Extracted 100 random effects for Destination"
- Required pattern: "Total random effects: 200 (100 UID x 2 locations)"
- Required pattern: "VALIDATION - PASS: Random effects completeness"
- Forbidden patterns: "ERROR", "Missing UID", "Duplicate UID-location pair", "NaN in random effects"
- Acceptable warnings: "random_slope variance small (expected per ICC_slope pattern)"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Only 95 UID found for Source, expected 100")
- Log failure to logs/step04_extract_random_effects.log
- Quit script immediately (do NOT proceed to Step 5)
- g_debug invoked (common causes: model fitting excluded participants, data loss in Step 1)

**CRITICAL DEPENDENCY WARNING:**
If this step fails, RQ 5.5.7 CANNOT proceed. The 200 random effects are the PRIMARY inputs for clustering analysis. User must resolve validation failures before moving to RQ 5.5.7.

---

### Step 5: Test Intercept-Slope Correlations (Decision D068)

**Dependencies:** Step 4 (requires individual random effects extracted)

**Complexity:** Low (1-2 minutes, Pearson correlation tests with Bonferroni correction)

**Purpose:** Test whether random intercepts and random slopes are significantly correlated within each location, using dual p-value reporting per Decision D068.

**Input:**

**File 1:** data/step04_random_effects.csv
**Source:** Step 4 output
**Format:** CSV with columns: UID, location, random_intercept, random_slope
**Expected Rows:** 200 (100 UID x 2 locations)

**Processing:**

**Perform 2 Pearson correlation tests (one per location):**

For Source location:
- Filter data WHERE location == "Source" (100 rows)
- Compute Pearson correlation: `r = corr(random_intercept, random_slope)`
- Test significance: `t = r x sqrt((N-2) / (1 - r^2))` with df = N-2
- Compute p-value (two-tailed)
- Apply Bonferroni correction: `p_bonferroni = p_uncorrected x 2` (2 tests total)

For Destination location:
- Filter data WHERE location == "Destination" (100 rows)
- Same procedure as Source

**Interpretation:**
- Positive correlation: Higher baseline ability associated with SLOWER forgetting (random_slope less negative)
- Negative correlation: Higher baseline ability associated with FASTER forgetting (random_slope more negative)
- No strong directional prediction per concept.md (exploratory test)

**Decision D068 Requirement:**
Report BOTH uncorrected and Bonferroni-corrected p-values for transparency (exploratory thesis context).

**Output:**

**File 1:** data/step05_intercept_slope_correlations.csv
**Format:** CSV, one row per location
**Columns:**
  - `location` (string, categorical: Source, Destination)
  - `r` (float, Pearson correlation coefficient in [-1, 1])
  - `N` (int, sample size for correlation, expected 100 per location)
  - `t_statistic` (float, test statistic for significance)
  - `df` (int, degrees of freedom, N-2 = 98)
  - `p_uncorrected` (float, two-tailed p-value in [0, 1])
  - `p_bonferroni` (float, Bonferroni-corrected p-value in [0, 1])
  - `significant_bonferroni` (boolean, True if p_bonferroni < 0.025, Bonferroni alpha for 2 tests)
**Expected Rows:** 2 (Source, Destination)
**Expected Values:**
  - r in [-1, 1] (correlation coefficient bounds)
  - N = 100 (all participants per location)
  - p_bonferroni = p_uncorrected x 2 (capped at 1.0)

**Validation Requirement:**

Validation tools MUST be used after correlation test tool execution. Specific validation tools will be determined by rq_tools based on Decision D068 dual p-value validation and correlation bounds. The rq_analysis agent will embed validation tool calls after the analysis tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_intercept_slope_correlations.csv: exists
- Expected rows: 2 (Source, Destination)
- Expected columns: 8 (location, r, N, t_statistic, df, p_uncorrected, p_bonferroni, significant_bonferroni)
- Data types: location (object), r (float64), N (int64), t_statistic (float64), df (int64), p_uncorrected (float64), p_bonferroni (float64), significant_bonferroni (bool)

*Value Ranges:*
- r in [-1, 1] (correlation bounds)
- N = 100 (both locations)
- df = 98 (N-2 for both locations)
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1] (capped at 1.0 even if uncorrected x 2 > 1.0)
- p_bonferroni >= p_uncorrected (correction can only increase p-value)

*Data Quality:*
- Both locations present (no missing rows)
- No NaN values in any column
- significant_bonferroni correctly derived from p_bonferroni < 0.025 threshold
- Dual p-values present per Decision D068 (both uncorrected and Bonferroni columns exist)

*Log Validation:*
- Required pattern: "Intercept-slope correlation (Source): r = X.XX, p_uncorrected = X.XX, p_bonferroni = X.XX"
- Required pattern: "Intercept-slope correlation (Destination): r = X.XX, p_uncorrected = X.XX, p_bonferroni = X.XX"
- Required pattern: "VALIDATION - PASS: Dual p-values present (Decision D068)"
- Forbidden patterns: "ERROR", "Missing p-value column", "Correlation out of bounds"
- Acceptable warnings: "Correlation non-significant after Bonferroni correction"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Missing p_bonferroni column (Decision D068 violation)")
- Log failure to logs/step05_test_intercept_slope_correlations.log
- Quit script immediately (do NOT proceed to Step 6)
- g_debug invoked (common causes: Decision D068 implementation error, correlation computation bug)

---

### Step 6: Compare ICC Across Locations

**Dependencies:** Step 3 (requires ICC estimates computed)

**Complexity:** Low (1-2 minutes, descriptive comparison and hypothesis test)

**Purpose:** Compare ICC_intercept between Source and Destination locations to test whether destination memory shows lower stability (secondary hypothesis).

**Input:**

**File 1:** data/step03_icc_estimates.csv
**Source:** Step 3 output
**Format:** CSV with columns: location, icc_type, value, interpretation
**Expected Rows:** 6 (3 ICC types x 2 locations)

**Processing:**

**Extract ICC_intercept for comparison:**
- Filter data WHERE icc_type == "ICC_intercept" (2 rows: Source, Destination)
- Extract ICC_intercept(Source) and ICC_intercept(Destination)

**Descriptive Comparison:**
- Compute difference: `diff = ICC_intercept(Source) - ICC_intercept(Destination)`
- Interpretation:
  - diff > 0: Source shows higher stability (supports hypothesis)
  - diff < 0: Destination shows higher stability (contradicts hypothesis)
  - diff near 0: Equivalent stability (null finding)

**Statistical Test (Optional):**
Note: ICC confidence intervals not typically computed in standard LMM output. This step provides descriptive comparison ONLY. Formal inferential test would require bootstrap or likelihood ratio test (beyond scope of this RQ).

**Output:**

**File 1:** data/step06_location_icc_comparison.csv
**Format:** CSV, one row per ICC type
**Columns:**
  - `icc_type` (string, categorical: ICC_intercept, ICC_slope_simple, ICC_slope_conditional)
  - `source_value` (float, ICC estimate for Source location)
  - `destination_value` (float, ICC estimate for Destination location)
  - `difference` (float, source_value - destination_value)
  - `interpretation` (string, descriptive interpretation of difference)
**Expected Rows:** 3 (one per ICC type)
**Expected Values:**
  - ICC_intercept difference expected in [-0.30, 0.30] (plausible range)
  - ICC_slope differences near zero (both locations expected ~0)

**File 2 (Optional):** data/step06_location_icc_barplot.png
**Format:** PNG barplot comparing ICC across locations (if visualization helpful)
**Note:** This is an analysis-generated plot (not rq_plots responsibility). If created, save to data/ folder per v4.2 architecture.

**Validation Requirement:**

Validation tools MUST be used after ICC comparison tool execution. Specific validation tools will be determined by rq_tools based on comparison table completeness and difference bounds. The rq_analysis agent will embed validation tool calls after the analysis tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_location_icc_comparison.csv: exists
- Expected rows: 3 (one per ICC type)
- Expected columns: 5 (icc_type, source_value, destination_value, difference, interpretation)
- Data types: icc_type (object), source_value (float64), destination_value (float64), difference (float64), interpretation (object)

*Value Ranges:*
- source_value in [0, 1] (ICC bounds)
- destination_value in [0, 1] (ICC bounds)
- difference in [-1, 1] (max possible difference between two ICCs)
- ICC_intercept values expected in [0.20, 0.70] (plausible episodic memory range)

*Data Quality:*
- All 3 ICC types present (no missing rows)
- No NaN values in any column
- difference correctly computed as source_value - destination_value
- interpretation non-empty string for all rows

*Log Validation:*
- Required pattern: "ICC_intercept comparison: Source = X.XX, Destination = X.XX, Difference = X.XX"
- Required pattern: "ICC_slope_simple near zero for both locations (expected pattern)"
- Required pattern: "VALIDATION - PASS: ICC comparison complete"
- Forbidden patterns: "ERROR", "ICC out of bounds", "Missing location"
- Acceptable warnings: "ICC_intercept difference small (locations show similar stability)"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "source_value out of [0,1] bounds: 1.15")
- Log failure to logs/step06_compare_icc_across_locations.log
- Quit script immediately
- g_debug invoked (common causes: Step 3 ICC computation error propagated to comparison)

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs - intermediate and final)

- data/step01_model_metadata_source.yaml (from Step 1: Source LMM metadata)
- data/step01_model_metadata_destination.yaml (from Step 1: Destination LMM metadata)
- data/step01_source_lmm_model.pkl (from Step 1: Saved Source LMM model)
- data/step01_destination_lmm_model.pkl (from Step 1: Saved Destination LMM model)
- data/step02_variance_components.csv (from Step 2: 10 rows, 5 components x 2 locations)
- data/step03_icc_estimates.csv (from Step 3: 6 rows, 3 ICC types x 2 locations)
- data/step04_random_effects.csv (from Step 4: 200 rows, 100 UID x 2 locations, REQUIRED for RQ 5.5.7)
- data/step05_intercept_slope_correlations.csv (from Step 5: 2 rows, Source + Destination)
- data/step06_location_icc_comparison.csv (from Step 6: 3 rows, ICC comparison table)

### Logs (ONLY execution logs - .log files capturing stdout/stderr)

- logs/step01_fit_location_stratified_lmms.log
- logs/step02_extract_variance_components.log
- logs/step03_compute_icc_estimates.log
- logs/step04_extract_random_effects.log
- logs/step05_test_intercept_slope_correlations.log
- logs/step06_compare_icc_across_locations.log

### Plots (EMPTY until rq_plots runs)

- plots/ folder remains empty (no trajectory plots in this RQ)
- Note: If Step 6 creates barplot, it saves to data/step06_location_icc_barplot.png (analysis-generated, not rq_plots)

### Results (EMPTY until rq_results runs)

- results/ folder remains empty until rq_results generates summary.md

---

## Expected Data Formats

### step01 Output Format (LMM Models)

**Model Metadata YAML Structure:**
```yaml
model_converged: true
n_observations: 400
n_participants: 100
time_variable_used: "log_TSVR"
formula: "theta ~ log_TSVR + (log_TSVR | UID)"
```

**Pickled Model Object:**
- statsmodels.regression.mixed_linear_model.MixedLMResults
- Contains: fixed effects, random effects, variance-covariance matrix, convergence info
- Accessed via: `pickle.load(open("data/step01_source_lmm_model.pkl", "rb"))`

---

### step02 Output Format (Variance Components)

**File:** data/step02_variance_components.csv

**Format:** Long format, one row per component per location

**Example Structure:**
```csv
location,component,value
Source,var_intercept,0.45
Source,var_slope,0.01
Source,cov_int_slope,-0.02
Source,var_residual,0.35
Source,correlation_int_slope,-0.15
Destination,var_intercept,0.38
Destination,var_slope,0.008
Destination,cov_int_slope,-0.01
Destination,var_residual,0.42
Destination,correlation_int_slope,-0.10
```

**Column Details:**
- `location`: Categorical (Source, Destination)
- `component`: Categorical (var_intercept, var_slope, cov_int_slope, var_residual, correlation_int_slope)
- `value`: Float64 (variance/covariance/correlation estimate)

---

### step03 Output Format (ICC Estimates)

**File:** data/step03_icc_estimates.csv

**Format:** Long format, one row per ICC type per location

**Example Structure:**
```csv
location,icc_type,value,interpretation
Source,ICC_intercept,0.56,Fair
Source,ICC_slope_simple,0.015,Poor
Source,ICC_slope_conditional,0.018,Poor
Destination,ICC_intercept,0.48,Fair
Destination,ICC_slope_simple,0.012,Poor
Destination,ICC_slope_conditional,0.014,Poor
```

**Column Details:**
- `location`: Categorical (Source, Destination)
- `icc_type`: Categorical (ICC_intercept, ICC_slope_simple, ICC_slope_conditional)
- `value`: Float64 in [0, 1]
- `interpretation`: Categorical (Poor <0.40, Fair 0.40-0.59, Good 0.60-0.74, Excellent >=0.75 per Cicchetti 1994)

---

### step04 Output Format (Random Effects) - CRITICAL for RQ 5.5.7

**File:** data/step04_random_effects.csv

**Format:** Long format, one row per UID per location

**Example Structure:**
```csv
UID,location,random_intercept,random_slope
P001,Source,0.35,-0.02
P001,Destination,0.28,-0.01
P002,Source,-0.15,0.01
P002,Destination,-0.20,0.005
...
P100,Source,0.42,-0.03
P100,Destination,0.38,-0.025
```

**Column Details:**
- `UID`: String, participant identifier (format: P### with leading zeros)
- `location`: Categorical (Source, Destination)
- `random_intercept`: Float64, participant-specific deviation from fixed intercept
- `random_slope`: Float64, participant-specific deviation from fixed slope

**Expected Rows:** 200 (100 UID x 2 locations)

**CRITICAL NOTE:**
This file is a REQUIRED input for RQ 5.5.7 (K-means clustering). The 200 random effects represent individual memory profiles stratified by location type.

---

### step05 Output Format (Intercept-Slope Correlations)

**File:** data/step05_intercept_slope_correlations.csv

**Format:** One row per location

**Example Structure:**
```csv
location,r,N,t_statistic,df,p_uncorrected,p_bonferroni,significant_bonferroni
Source,-0.15,100,-1.52,98,0.13,0.26,False
Destination,-0.10,100,-1.01,98,0.31,0.62,False
```

**Column Details:**
- `location`: Categorical (Source, Destination)
- `r`: Float64, Pearson correlation coefficient in [-1, 1]
- `N`: Int64, sample size (100)
- `t_statistic`: Float64, test statistic
- `df`: Int64, degrees of freedom (N-2 = 98)
- `p_uncorrected`: Float64, two-tailed p-value in [0, 1]
- `p_bonferroni`: Float64, Bonferroni-corrected p-value (p_uncorrected x 2, capped at 1.0)
- `significant_bonferroni`: Boolean, True if p_bonferroni < 0.025

**Decision D068 Compliance:**
BOTH p_uncorrected and p_bonferroni columns present (dual p-value reporting).

---

### step06 Output Format (Location ICC Comparison)

**File:** data/step06_location_icc_comparison.csv

**Format:** One row per ICC type

**Example Structure:**
```csv
icc_type,source_value,destination_value,difference,interpretation
ICC_intercept,0.56,0.48,0.08,Source shows slightly higher baseline stability
ICC_slope_simple,0.015,0.012,0.003,Both locations show near-zero slope variance (expected pattern)
ICC_slope_conditional,0.018,0.014,0.004,Conditional ICC similar to simple ICC for both locations
```

**Column Details:**
- `icc_type`: Categorical (ICC_intercept, ICC_slope_simple, ICC_slope_conditional)
- `source_value`: Float64, ICC estimate for Source location in [0, 1]
- `destination_value`: Float64, ICC estimate for Destination location in [0, 1]
- `difference`: Float64, source_value - destination_value in [-1, 1]
- `interpretation`: String, descriptive interpretation of difference

---

## Cross-RQ Dependencies

**This RQ depends on:** RQ 5.5.1 (Source-Destination Trajectories - ROOT)

**Required Files from RQ 5.5.1:**
- results/ch5/5.5.1/data/step04_lmm_input.csv (800 rows: 100 UID x 4 tests x 2 locations)

**Best-Fit Time Transformation:**
- RQ 5.5.1 identifies best-fit time transformation (e.g., log_TSVR, TSVR_hours, sqrt_TSVR) via model selection
- This RQ uses same transformation for location-stratified LMMs
- Transformation name read from RQ 5.5.1 metadata or plan

**Status Check:**
- rq_planner should verify results/ch5/5.5.1/status.yaml shows ALL agents = success
- If RQ 5.5.1 incomplete: QUIT with "FAIL: RQ 5.5.1 must complete before this RQ (dependency)"

**Data Integration:**
- Step 1: Read RQ 5.5.1 LMM input data (theta + TSVR merged)
- Step 1: Filter by location (Source vs Destination)
- Step 1: Fit separate LMMs per location
- NO new data extraction from master.xlsx (all preprocessing done in RQ 5.5.1)

**Downstream Dependency:**
- RQ 5.5.7 depends on THIS RQ (requires data/step04_random_effects.csv)
- If Step 4 fails, RQ 5.5.7 cannot proceed

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

---

### Validation Requirements By Step

#### Step 1: Fit Location-Stratified LMMs

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.fit_lmm_trajectory_tsvr)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_lmm_convergence)

**What Validation Checks:**
- Both models converged (model.converged=True)
- No singular fit warnings (indicates collinearity)
- Expected N: 100 participants per model
- Expected observations: 400 per model (100 UID x 4 tests)
- Model metadata files created and valid YAML

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Source model did not converge")
- Log failure to logs/step01_fit_location_stratified_lmms.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked by master to diagnose (common causes: insufficient data, time variable misspecification)

---

#### Step 2: Extract Variance Components

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.extract_random_effects_from_lmm or custom function)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_variance_positivity)

**What Validation Checks:**
- Output file exists (data/step02_variance_components.csv)
- Expected rows: 10 (5 components x 2 locations)
- Expected columns: 3 (location, component, value)
- All variance components > 0 (no negative variances)
- correlation_int_slope in [-1, 1] bounds
- No NaN or inf values

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Negative var_intercept for Source: -0.05")
- Log failure to logs/step02_extract_variance_components.log
- Quit script immediately (do NOT proceed to Step 3)
- g_debug invoked (common causes: model convergence issues, singular fit)

---

#### Step 3: Compute ICC Estimates

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.compute_icc_from_variance_components)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_icc_bounds)

**What Validation Checks:**
- Output file exists (data/step03_icc_estimates.csv)
- Expected rows: 6 (3 ICC types x 2 locations)
- All ICC values in [0, 1] bounds
- Interpretation categories match Cicchetti (1994) thresholds
- No NaN values

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "ICC_intercept > 1.0 for Source: 1.15")
- Log failure to logs/step03_compute_icc_estimates.log
- Quit script immediately (do NOT proceed to Step 4)
- g_debug invoked (common causes: variance component extraction error, formula bug)

---

#### Step 4: Extract Random Effects (CRITICAL for RQ 5.5.7)

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.extract_random_effects_from_lmm)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure)

**What Validation Checks:**
- Output file exists (data/step04_random_effects.csv)
- Expected rows: 200 (100 UID x 2 locations)
- Expected columns: 4 (UID, location, random_intercept, random_slope)
- All 100 UID present for BOTH locations (no data loss)
- No duplicate UID-location pairs
- No NaN or inf values
- random_intercept approximately normal distribution
- random_slope approximately normal distribution

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Only 95 UID found for Source, expected 100")
- Log failure to logs/step04_extract_random_effects.log
- Quit script immediately (do NOT proceed to Step 5)
- g_debug invoked (common causes: model fitting excluded participants, data loss in Step 1)

**CRITICAL DEPENDENCY WARNING:**
If this step fails, RQ 5.5.7 CANNOT proceed. User must resolve validation failures.

---

#### Step 5: Test Intercept-Slope Correlations

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_lmm.test_intercept_slope_correlation_d068)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_correlation_test_d068)

**What Validation Checks:**
- Output file exists (data/step05_intercept_slope_correlations.csv)
- Expected rows: 2 (Source, Destination)
- Dual p-value columns present (p_uncorrected, p_bonferroni per Decision D068)
- r in [-1, 1] bounds
- p_bonferroni >= p_uncorrected
- N = 100 for both locations
- df = 98 for both locations

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Missing p_bonferroni column (Decision D068 violation)")
- Log failure to logs/step05_test_intercept_slope_correlations.log
- Quit script immediately (do NOT proceed to Step 6)
- g_debug invoked (common causes: Decision D068 implementation error, correlation bug)

---

#### Step 6: Compare ICC Across Locations

**Analysis Tool:** (determined by rq_tools - likely custom comparison function)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure)

**What Validation Checks:**
- Output file exists (data/step06_location_icc_comparison.csv)
- Expected rows: 3 (one per ICC type)
- source_value and destination_value in [0, 1] bounds
- difference correctly computed (source_value - destination_value)
- No NaN values

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "source_value out of bounds: 1.15")
- Log failure to logs/step06_compare_icc_across_locations.log
- Quit script immediately
- g_debug invoked (common causes: Step 3 ICC computation error propagated)

---

## Summary

**Total Steps:** 6

**Estimated Runtime:** Medium (15-30 minutes total)
- Step 1: 10-15 minutes (2 LMM fits)
- Steps 2-6: 5-10 minutes (extraction and computation)

**Cross-RQ Dependencies:** RQ 5.5.1 (Source-Destination Trajectories)

**Primary Outputs:**
- Variance components: 10 rows (5 components x 2 locations)
- ICC estimates: 6 rows (3 types x 2 locations)
- **Random effects: 200 rows (100 UID x 2 locations, REQUIRED for RQ 5.5.7)**
- Intercept-slope correlations: 2 rows (Source, Destination) with dual p-values
- Location ICC comparison: 3 rows (ICC comparison table)

**Validation Coverage:** 100% (all 6 steps have validation requirements)

**Critical Dependency Chain:**
- RQ 5.5.1 (complete) -> THIS RQ (Step 4 output) -> RQ 5.5.7 (clustering)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Naming Conventions:**

All file naming follows docs/v4/names.md conventions:
- Step names: step01_fit_location_stratified_lmms, step02_extract_variance_components, etc.
- Data files: data/stepNN_*.csv format (outputs to data/ per v4.2 architecture)
- Logs: logs/stepNN_*.log format (execution logs only)
- Variable names: UID, location, random_intercept, random_slope, ICC_intercept, etc. (consistent with Chapter 5 conventions)

**Validation Philosophy:**

Per-step validation ensures errors caught at source, not 5 steps later. Every step has embedded validation requirements to prevent cascading failures.

**Tool Selection:**

rq_tools agent reads this plan and specifies exact tools from tools_inventory.md based on analysis requirements.

**Code Generation:**

g_code agent generates Python scripts per rq_analysis instructions based on this plan.

---

**Version History:**
- v1.0 (2025-12-04): Initial plan created by rq_planner agent for RQ 5.5.6

---

**End of Analysis Plan**
