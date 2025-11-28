# Analysis Plan for RQ 5.13: Between-Person Variance in Forgetting Rates

**Created by:** rq_planner agent
**Date:** 2025-11-27
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This RQ examines the variance decomposition of forgetting trajectories from RQ 5.7's best-fitting mixed model. The primary goal is to quantify how much variation in forgetting rates reflects stable individual differences (between-person variance) versus measurement noise or within-person fluctuation (residual variance).

**Analysis Type:** Variance Decomposition of LMM Random Effects (from RQ 5.7 saved model)

**Pipeline:** Load RQ 5.7 outputs -> Extract variance components -> Compute ICCs -> Extract individual random effects -> Test intercept-slope correlation -> Visualize distribution

**Total Steps:** 5 analysis steps (no IRT calibration, no new LMM fitting - reuses RQ 5.7 model)

**Estimated Runtime:** Low (~5-10 minutes total - all steps are data extraction/computation, no model fitting)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting for intercept-slope correlation test (uncorrected + Bonferroni)

**Critical Dependency:**
RQ 5.7 MUST complete all 5 steps before this RQ can execute. Specifically requires:
- Saved LMM model object with random slopes (step05_lmm_all_bestmodel.pkl)
- IRT theta scores (step04_theta_scores_allitems.csv)
- TSVR mapping (step00_tsvr_mapping.csv)

---

## Analysis Plan

This RQ requires 5 analysis steps:

### Step 1: Load RQ 5.7 Dependencies

**Dependencies:** None (first step, but requires RQ 5.7 completed)
**Complexity:** Low (file loading only, <1 minute)

**Purpose:** Load saved LMM model object and data files from RQ 5.7 to enable variance decomposition analysis.

**Input:**

**File 1:** results/ch5/rq7/data/step05_lmm_all_bestmodel.pkl
**Source:** RQ 5.7 Step 5 (LMM trajectory modeling with random slopes)
**Format:** Python pickle file (statsmodels MixedLMResults object)
**Expected Content:** Fitted LMM with random intercepts and random slopes for time variable, converged model with variance-covariance matrix

**File 2:** results/ch5/rq7/data/step04_theta_scores_allitems.csv
**Source:** RQ 5.7 Step 4 (theta extraction after Pass 2 IRT calibration)
**Format:** CSV with columns:
  - UID (string, participant identifier, format: P###)
  - TEST (string, test session: T1, T2, T3, T4)
  - theta (float, IRT ability estimate for "All" factor)
  - SE (float, standard error of theta estimate)
**Expected Rows:** ~400 (100 participants x 4 tests)

**File 3:** results/ch5/rq7/data/step00_tsvr_mapping.csv
**Source:** RQ 5.7 Step 0 (TSVR extraction from master.xlsx)
**Format:** CSV with columns:
  - UID (string, participant identifier)
  - TEST (string, test session)
  - TSVR (float, time since VR session in hours per Decision D070)
**Expected Rows:** ~400 (100 participants x 4 tests)

**Circuit Breaker Check:**
If ANY of the three required files from RQ 5.7 are missing, trigger EXPECTATIONS ERROR:
```
EXPECTATIONS ERROR: To perform Step 1 (Load RQ 5.7 Dependencies) I expect:
  - results/ch5/rq7/data/step05_lmm_all_bestmodel.pkl (saved LMM model)
  - results/ch5/rq7/data/step04_theta_scores_allitems.csv (theta scores)
  - results/ch5/rq7/data/step00_tsvr_mapping.csv (TSVR mapping)

But missing: [list missing files]

Action: RQ 5.7 must complete Steps 0-5 before RQ 5.13 can execute.
Run RQ 5.7 workflow first, then retry RQ 5.13.
```

**Processing:**
- Load pickle file using Python pickle.load() or joblib.load()
- Load CSV files using pandas.read_csv()
- Validate model object is statsmodels MixedLMResults with random effects
- Validate CSV files have expected columns and row counts

**Output:**

**File 1:** data/step01_model_metadata.yaml
**Format:** YAML metadata documenting loaded model
**Content:**
  - model_source: "results/ch5/rq7/data/step05_lmm_all_bestmodel.pkl"
  - model_type: "MixedLM"
  - n_participants: 100
  - n_observations: ~400
  - random_effects: ["intercept", "slope"]
  - converged: True/False

**File 2:** logs/step01_load_dependencies.log
**Format:** Text log
**Content:** Loading confirmation messages, file sizes, row counts, validation checks

**Validation Requirement:**
Validation tools MUST be used after data loading. Specific validation tools will be determined by rq_tools based on file format requirements (check_file_exists, validate_data_columns, validate_model_convergence).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_model_metadata.yaml exists (exact path)
- Expected keys: model_source, model_type, n_participants, n_observations, random_effects, converged
- Data types: strings (paths), integers (counts), boolean (converged), list (random_effects)
- logs/step01_load_dependencies.log exists

*Value Ranges:*
- n_participants: exactly 100 (all participants from RQ 5.7)
- n_observations: 380-400 (100x4=400 minus any missing data tolerated in RQ 5.7)
- converged: must be True (if False, RQ 5.7 model failed)

*Data Quality:*
- All three dependency files successfully loaded (no FileNotFoundError)
- Model object is MixedLMResults type (not None, not corrupted pickle)
- CSV files have expected column names (UID, TEST, theta/SE or TSVR)
- No NaN in key columns (UID, TEST must be complete)

*Log Validation:*
- Required pattern: "Successfully loaded model from results/ch5/rq7/data/step05_lmm_all_bestmodel.pkl"
- Required pattern: "Model converged: True"
- Required pattern: "Loaded theta scores: 400 rows" (or actual count)
- Required pattern: "Loaded TSVR mapping: 400 rows"
- Forbidden patterns: "ERROR", "FileNotFoundError", "Model converged: False"

**Expected Behavior on Validation Failure:**
- Raise EXPECTATIONS ERROR with specific missing file(s)
- Log failure to logs/step01_load_dependencies.log
- Quit script immediately (do NOT proceed to Step 2)
- Master reports to user: "RQ 5.7 incomplete - run RQ 5.7 first"

---

### Step 2: Extract Variance Components from LMM

**Dependencies:** Step 1 (requires loaded LMM model object)
**Complexity:** Low (mathematical extraction from fitted model, <1 minute)

**Purpose:** Extract variance-covariance matrix from random effects and residual variance to enable ICC computation and individual differences quantification.

**Input:**

**Python Object:** Loaded MixedLMResults model from Step 1
**Required Attributes:**
  - cov_re (pandas DataFrame, random effects covariance matrix)
  - scale (float, residual variance estimate)
  - random_effects (dict, participant-specific random intercepts and slopes)

**Processing:**
- Extract variance components from model.cov_re:
  - var_intercept: Variance of random intercepts (diagonal element [0,0])
  - var_slope: Variance of random slopes (diagonal element [1,1])
  - cov_int_slope: Covariance between intercepts and slopes (off-diagonal element [0,1])
- Extract residual variance: var_residual = model.scale
- Compute correlation between intercepts and slopes: cor_int_slope = cov_int_slope / sqrt(var_intercept x var_slope)
- Store all components in structured format

**Output:**

**File:** data/step02_variance_components.csv
**Format:** CSV with columns:
  - component (string): "var_intercept", "var_slope", "cov_int_slope", "var_residual", "cor_int_slope"
  - estimate (float): variance/covariance/correlation value
**Expected Rows:** 5 (one per variance component)

**File:** logs/step02_variance_extraction.log
**Format:** Text log
**Content:** Extracted values, formulas used, validation checks

**Validation Requirement:**
Validation tools MUST be used after variance component extraction. Specific validation tools will be determined by rq_tools based on LMM variance requirements (validate_variance_positivity, validate_numeric_range for correlation).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_variance_components.csv exists (exact path)
- Expected rows: exactly 5 (one per component)
- Expected columns: 2 (component: string, estimate: float)
- Data types: component (string), estimate (float64)

*Value Ranges:*
- var_intercept > 0 (variance must be positive)
- var_slope > 0 (variance must be positive)
- var_residual > 0 (variance must be positive)
- cov_int_slope: unrestricted (can be negative, zero, or positive)
- cor_int_slope in [-1, 1] (correlation bounds)

*Data Quality:*
- No NaN values (all variance components must be estimated)
- No infinite values (indicates computation error)
- Variance components positive (validates model convergence quality)
- Correlation mathematically valid: |cor_int_slope| <= 1.0

*Log Validation:*
- Required pattern: "Extracted variance components from LMM random effects"
- Required pattern: "var_intercept = [value] (positive check: PASS)"
- Required pattern: "var_slope = [value] (positive check: PASS)"
- Required pattern: "var_residual = [value] (positive check: PASS)"
- Required pattern: "cor_int_slope = [value] (range check: PASS)"
- Forbidden patterns: "ERROR", "NaN detected", "Negative variance", "Correlation out of bounds"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "var_slope = -0.02, expected positive")
- Log failure to logs/step02_variance_extraction.log
- Quit script immediately (do NOT proceed to Step 3)
- g_debug invoked to diagnose (likely cause: RQ 5.7 model convergence issue or pickle corruption)

---

### Step 3: Compute Intraclass Correlation Coefficients (ICC)

**Dependencies:** Step 2 (requires variance components)
**Complexity:** Low (mathematical computation, <1 minute)

**Purpose:** Quantify proportion of variance that is between-person (stable individual differences) vs within-person (measurement error) for both intercepts and slopes.

**Input:**

**File:** data/step02_variance_components.csv
**Format:** CSV with component names and estimates (from Step 2)
**Required Components:** var_intercept, var_slope, var_residual, cov_int_slope

**Processing:**
- Compute ICC for intercepts (simple):
  ICC_intercept = var_intercept / (var_intercept + var_residual)

- Compute ICC for slopes (Method 1 - simple ratio):
  ICC_slope_simple = var_slope / (var_slope + var_residual)

- Compute ICC for slopes (Method 2 - conditional at Day 6):
  Per Raudenbush & Bryk methodology, account for intercept-slope covariance
  ICC_slope_conditional = [var_intercept + 2 x cov_int_slope x time + var_slope x time^2] / [var_intercept + 2 x cov_int_slope x time + var_slope x time^2 + var_residual]
  where time = maximum TSVR value (Day 6, approximately 144 hours)

- Interpret ICC magnitude per conventional thresholds:
  - ICC < 0.20: Low between-person variance (measurement noise dominates)
  - 0.20 <= ICC < 0.40: Moderate between-person variance
  - ICC >= 0.40: Substantial between-person variance (trait-like)

**Output:**

**File:** data/step03_icc_estimates.csv
**Format:** CSV with columns:
  - icc_type (string): "intercept", "slope_simple", "slope_conditional"
  - icc_value (float): ICC value in [0, 1]
  - interpretation (string): "Low (<0.20)", "Moderate (0.20-0.40)", "Substantial (>=0.40)"
**Expected Rows:** 3 (one per ICC type)

**File:** results/step03_icc_summary.txt
**Format:** Plain text summary
**Content:** ICC estimates with interpretations, comparison to hypothesis (ICC_slope > 0.40 predicted), implications for individual differences

**File:** logs/step03_icc_computation.log
**Format:** Text log
**Content:** Computation formulas, intermediate values, validation checks

**Validation Requirement:**
Validation tools MUST be used after ICC computation. Specific validation tools will be determined by rq_tools based on ICC requirements (validate_icc_bounds, validate_numeric_range).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_icc_estimates.csv exists (exact path)
- Expected rows: exactly 3 (intercept, slope_simple, slope_conditional)
- Expected columns: 3 (icc_type: string, estimate: float, interpretation: string)
- results/step03_icc_summary.txt exists
- Data types: icc_type (string), estimate (float64), interpretation (string)

*Value Ranges:*
- estimate in [0, 1] for ALL three ICC types (mathematical constraint)
- ICC_intercept expected > 0.40 (high stability in baseline per hypothesis)
- ICC_slope_simple expected 0.30-0.60 (moderate-to-high stability per hypothesis)
- ICC_slope_conditional typically close to ICC_slope_simple (unless strong intercept-slope covariance)

*Data Quality:*
- No NaN values (all ICCs must be computed)
- No values outside [0, 1] (indicates computation error)
- interpretation strings match expected categories exactly: "Low (<0.20)" OR "Moderate (0.20-0.40)" OR "Substantial (>=0.40)"
- All three ICC types present (no missing rows)

*Log Validation:*
- Required pattern: "Computed ICC for intercepts: [value]"
- Required pattern: "Computed ICC for slopes (simple): [value]"
- Required pattern: "Computed ICC for slopes (conditional at Day 6): [value]"
- Required pattern: "ICC bounds validation: PASS (all in [0,1])"
- Forbidden patterns: "ERROR", "ICC out of bounds", "NaN detected", "Division by zero"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "ICC_slope_simple = 1.23, expected in [0,1]")
- Log failure to logs/step03_icc_computation.log
- Quit script immediately (do NOT proceed to Step 4)
- g_debug invoked to diagnose (likely cause: variance component extraction error in Step 2)

---

### Step 4: Extract Individual Random Effects

**Dependencies:** Step 1 (requires loaded LMM model object)
**Complexity:** Low (data extraction from fitted model, <1 minute)

**Purpose:** Extract participant-specific random intercepts and slopes for use in descriptive statistics, visualization (Step 5), and downstream clustering analysis (RQ 5.14).

**Input:**

**Python Object:** Loaded MixedLMResults model from Step 1
**Required Attribute:** model.random_effects (dict mapping UID to random effects DataFrame)

**Processing:**
- Extract random_effects dictionary from model
- For each participant (UID):
  - Extract random intercept (Intercept column)
  - Extract random slope (slope column for time variable)
  - Compute total intercept = fixed intercept + random intercept
  - Compute total slope = fixed slope + random slope
- Create DataFrame with one row per participant
- Compute descriptive statistics for random slopes distribution:
  - Mean, SD, min, max, Q1, median, Q3
  - Check normality assumption (for later Q-Q plot in Step 5)

**Output:**

**File:** data/step04_random_effects.csv
**Format:** CSV with columns:
  - UID (string, participant identifier, format: P###)
  - random_intercept (float, deviation from population mean intercept)
  - random_slope (float, deviation from population mean slope)
  - total_intercept (float, fixed + random intercept)
  - total_slope (float, fixed + random slope)
**Expected Rows:** 100 (one per participant)

**File:** results/step04_random_slopes_descriptives.txt
**Format:** Plain text descriptive statistics
**Content:** Mean, SD, min, max, quartiles for random slopes distribution

**File:** logs/step04_random_effects_extraction.log
**Format:** Text log
**Content:** Extraction confirmation, participant count, descriptive statistics, normality checks

**CRITICAL NOTE FOR RQ 5.14:**
The file data/step04_random_effects.csv is a REQUIRED INPUT for RQ 5.14 (K-means clustering to identify fast vs slow forgetters). RQ 5.14 will use random_slope column as clustering input. This file MUST be saved to enable downstream dependency.

**Validation Requirement:**
Validation tools MUST be used after random effects extraction. Specific validation tools will be determined by rq_tools based on data format requirements (validate_data_columns, validate_dataframe_structure, validate_numeric_range).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_random_effects.csv exists (exact path)
- Expected rows: exactly 100 (one per participant)
- Expected columns: 5 (UID, random_intercept, random_slope, total_intercept, total_slope)
- Data types: UID (string), all others (float64)
- results/step04_random_slopes_descriptives.txt exists

*Value Ranges:*
- random_intercept: typically in [-2, 2] (extreme values >3 SD from mean are rare but possible)
- random_slope: typically in [-0.5, 0.5] (forgetting rate deviations, negative = faster forgetting)
- total_intercept: typically in [-1, 2] (baseline ability range on theta scale)
- total_slope: typically in [-0.3, 0.1] (negative = forgetting over time, positive = rare improvement)

*Data Quality:*
- No NaN values in random_intercept or random_slope (model must estimate for all participants)
- No duplicate UIDs (each participant appears exactly once)
- All 100 participants present (no data loss from RQ 5.7)
- Random effects approximately normally distributed (will be validated visually in Step 5)

*Log Validation:*
- Required pattern: "Extracted random effects for 100 participants"
- Required pattern: "Random slopes: mean = [value], SD = [value]"
- Required pattern: "Random slopes range: [min] to [max]"
- Required pattern: "Descriptive statistics saved to results/step04_random_slopes_descriptives.txt"
- Forbidden patterns: "ERROR", "NaN detected", "Missing participants", "Duplicate UID"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 100 participants, found 87")
- Log failure to logs/step04_random_effects_extraction.log
- Quit script immediately (do NOT proceed to Step 5)
- g_debug invoked to diagnose (likely cause: RQ 5.7 data loss or model object corruption)

---

### Step 5: Test Intercept-Slope Correlation and Visualize Distribution

**Dependencies:** Step 4 (requires individual random effects)
**Complexity:** Low (statistical test + plotting, <2 minutes)

**Purpose:** Test hypothesis that baseline ability and forgetting rate are correlated (negative correlation = high performers maintain advantage). Visualize random slopes distribution and assess normality assumption for LMM.

**Input:**

**File:** data/step04_random_effects.csv
**Format:** CSV with random_intercept and random_slope columns (from Step 4)
**Required Columns:** UID, random_intercept, random_slope

**Processing:**

**Part A: Intercept-Slope Correlation Test (Decision D068)**
- Compute Pearson correlation between random_intercept and random_slope
- Test significance using t-test (two-tailed)
- Apply Bonferroni correction: alpha_corrected = 0.05 / 15 = 0.0033 (15 tests across Chapter 5 per D068)
- Report BOTH p-values per Decision D068:
  - p_uncorrected: raw p-value from correlation test
  - p_bonferroni: Bonferroni-corrected p-value (p_uncorrected x 15)
- Interpret direction:
  - Negative r: High baseline ability associated with slower forgetting (maintains advantage)
  - Positive r: High baseline ability associated with faster forgetting (regression to mean)
  - Near-zero r: Baseline and forgetting rate independent

**Part B: Visualization**
- Generate histogram of random slopes distribution
  - X-axis: random_slope (forgetting rate deviation)
  - Y-axis: Frequency (count of participants)
  - Include vertical line at mean (population average forgetting rate)
  - Include normal distribution overlay (theoretical vs observed)

- Generate Q-Q plot (quantile-quantile plot)
  - Tests normality assumption for random effects
  - Points should fall on diagonal if normally distributed
  - Deviations indicate skewness or heavy tails

**Output:**

**File:** results/step05_intercept_slope_correlation.csv
**Format:** CSV with columns:
  - statistic (string): "correlation", "p_uncorrected", "p_bonferroni", "df", "alpha_corrected"
  - value (float): correlation coefficient r, p-values, degrees of freedom (98), significance threshold (0.0033)
**Expected Rows:** 5 (one per statistic)

**File:** results/step05_correlation_interpretation.txt
**Format:** Plain text interpretation
**Content:** Correlation magnitude, direction, significance (at both alpha levels per D068), theoretical implications

**File:** plots/step05_random_slopes_histogram.png
**Format:** PNG image
**Dimensions:** 800 x 600 pixels @ 300 DPI
**Content:** Histogram of random slopes with normal overlay and mean reference line

**File:** plots/step05_random_slopes_qqplot.png
**Format:** PNG image
**Dimensions:** 800 x 600 pixels @ 300 DPI
**Content:** Q-Q plot assessing normality of random slopes distribution

**File:** logs/step05_correlation_test.log
**Format:** Text log
**Content:** Correlation test results, Bonferroni correction applied, plotting confirmation

**Validation Requirement:**
Validation tools MUST be used after correlation test and plotting. Specific validation tools will be determined by rq_tools based on D068 requirements (validate_correlation_test_d068) and plot data requirements (check_file_exists for PNG files).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step05_intercept_slope_correlation.csv exists (exact path)
- Expected rows: exactly 5 (correlation, p_uncorrected, p_bonferroni, df, alpha_corrected)
- Expected columns: 2 (statistic: string, value: float)
- results/step05_correlation_interpretation.txt exists
- plots/step05_random_slopes_histogram.png exists (file size > 10 KB)
- plots/step05_random_slopes_qqplot.png exists (file size > 10 KB)
- Data types: statistic (string), value (float64)

*Value Ranges:*
- correlation in [-1, 1] (Pearson r bounds)
- p_uncorrected in [0, 1] (p-value bounds)
- p_bonferroni in [0, 1] (corrected p-value, capped at 1.0)
- df = 98 (degrees of freedom for N=100 participants)
- alpha_corrected = 0.0033 (Bonferroni threshold: 0.05/15)

*Data Quality:*
- Exactly 5 rows in correlation CSV (all statistics present)
- No NaN values (correlation and p-values must be computed)
- p_bonferroni = min(p_uncorrected x 15, 1.0) (capped at 1.0 per convention)
- Both PNG files successfully created (file size > 10 KB indicates non-empty plots)
- Q-Q plot contains diagonal reference line (visual check)

*Log Validation:*
- Required pattern: "Intercept-slope correlation: r = [value], p = [p_uncorrected]"
- Required pattern: "Bonferroni-corrected p-value: [p_bonferroni] (alpha = 0.0033)"
- Required pattern: "Decision D068: Dual p-values reported"
- Required pattern: "Histogram saved to plots/step05_random_slopes_histogram.png"
- Required pattern: "Q-Q plot saved to plots/step05_random_slopes_qqplot.png"
- Forbidden patterns: "ERROR", "NaN correlation", "Invalid p-value", "Plotting failed"

**Expected Behavior on Validation Failure:**
- If correlation out of bounds or NaN: Raise error, log failure, quit (g_debug diagnoses)
- If Bonferroni correction wrong: Raise error "Expected p_bonferroni = min(p_uncorrected x 15, 1.0), found [value]"
- If dual p-values missing: Raise error "Decision D068 violation: Missing p_bonferroni column"
- If PNG files missing: Raise error "Plotting failed, check matplotlib/seaborn installation"
- All failures log to logs/step05_correlation_test.log

---

## Expected Data Formats

### Variance Components Format (Step 2 Output)

**File:** data/step02_variance_components.csv

**Structure:**
```
component,estimate
var_intercept,0.45
var_slope,0.12
cov_int_slope,-0.08
var_residual,0.23
cor_int_slope,-0.36
```

**Details:**
- var_intercept: Between-person variance in baseline ability (theta at encoding)
- var_slope: Between-person variance in forgetting rate (theta change per hour)
- cov_int_slope: Covariance between baseline and slope (negative = high baseline -> slower forgetting)
- var_residual: Within-person variance (measurement error + unexplained variation)
- cor_int_slope: Correlation derived from covariance (standardized version for interpretability)

**Usage:** This format enables ICC computation in Step 3 by providing numerators and denominators for ICC formulas.

---

### ICC Estimates Format (Step 3 Output)

**File:** data/step03_icc_estimates.csv

**Structure:**
```
icc_type,estimate,interpretation
intercept,0.66,Substantial (>=0.40)
slope_simple,0.34,Moderate (0.20-0.40)
slope_conditional,0.38,Moderate (0.20-0.40)
```

**Details:**
- intercept: Proportion of variance in baseline ability that is between-person (vs within-person error)
- slope_simple: Simple ICC for slopes (var_slope / (var_slope + var_residual))
- slope_conditional: Conditional ICC accounting for intercept-slope covariance at Day 6

**Interpretation Thresholds:**
- ICC < 0.20: Low (forgetting rate mostly noise)
- 0.20 <= ICC < 0.40: Moderate (mixed trait/state)
- ICC >= 0.40: Substantial (forgetting rate is trait-like)

**Usage:** These estimates directly answer RQ 5.13's primary question about stable individual differences in forgetting.

---

### Random Effects Format (Step 4 Output)

**File:** data/step04_random_effects.csv

**Structure:**
```
UID,random_intercept,random_slope,total_intercept,total_slope
P001,-0.42,0.08,-0.18,0.02
P002,0.67,-0.15,0.91,-0.21
P003,-0.13,-0.05,0.11,-0.11
...
```

**Details:**
- UID: Participant identifier (P### format, one per participant)
- random_intercept: Deviation from population mean baseline ability (positive = above average)
- random_slope: Deviation from population mean forgetting rate (negative = faster forgetting than average)
- total_intercept: Fixed effect + random effect (participant's actual baseline ability)
- total_slope: Fixed effect + random effect (participant's actual forgetting rate)

**Expected Rows:** 100 (one per participant)

**Usage:**
- This file is a REQUIRED INPUT for RQ 5.14 (K-means clustering analysis)
- RQ 5.14 will use random_slope column to identify fast vs slow forgetters
- Also used within this RQ for correlation test (Step 5) and visualization

---

### Correlation Test Format (Step 5 Output)

**File:** results/step05_intercept_slope_correlation.csv

**Structure:**
```
statistic,value
correlation,-0.32
p_uncorrected,0.001
p_bonferroni,0.015
df,98
alpha_corrected,0.0033
```

**Details:**
- correlation: Pearson r between random_intercept and random_slope
- p_uncorrected: Raw p-value from correlation test (before multiple testing correction)
- p_bonferroni: Bonferroni-corrected p-value (p_uncorrected x 15, capped at 1.0)
- df: Degrees of freedom (N - 2 = 100 - 2 = 98)
- alpha_corrected: Significance threshold after Bonferroni correction (0.05 / 15 = 0.0033)

**Decision D068 Requirement:**
BOTH p_uncorrected and p_bonferroni MUST be reported. This enables transparent reporting of results under both lenient (uncorrected) and conservative (Bonferroni) criteria. Per D068, Chapter 5 has 15 hypothesis tests total, hence divisor = 15.

**Usage:** Tests secondary hypothesis that high baseline ability predicts slower forgetting (negative correlation expected).

---

## Cross-RQ Dependencies

### Dependency Type: DERIVED Data from RQ 5.7 (Critical Dependency)

**This RQ requires outputs from:**
- **RQ 5.7** (Which functional form best describes forgetting trajectories?)

  **Files Required:**
  1. results/ch5/rq7/data/step05_lmm_all_bestmodel.pkl
     - Used in: Step 1 (load saved LMM model object)
     - Rationale: RQ 5.7 fits LMM with random slopes for forgetting trajectories. This RQ decomposes variance from that model.

  2. results/ch5/rq7/data/step04_theta_scores_allitems.csv
     - Used in: Step 1 (load theta scores for context, not actively analyzed but validates dependency)
     - Rationale: Provides participant ability estimates that fed into RQ 5.7's LMM

  3. results/ch5/rq7/data/step00_tsvr_mapping.csv
     - Used in: Step 1 (load TSVR time variable for documentation, not actively analyzed)
     - Rationale: Documents time variable used in RQ 5.7's LMM (Decision D070 - actual hours)

**Execution Order Constraint:**
1. RQ 5.7 must complete Steps 0-5 (IRT calibration, purification, theta extraction, TSVR merge, LMM trajectory fitting with random slopes)
2. This RQ (5.13) executes after RQ 5.7 completes
3. RQ 5.14 executes after this RQ (uses data/step04_random_effects.csv from Step 4 of this RQ)

**Data Source Boundaries:**
- **RAW data:** None directly used (all analysis uses RQ 5.7 outputs)
- **DERIVED data:** LMM model object + theta scores + TSVR mapping (all from RQ 5.7)
- **Scope:** This RQ does NOT fit new models. It extracts variance components from RQ 5.7's saved model.

**Circuit Breaker:**
- Step 1: Check results/ch5/rq7/data/step05_lmm_all_bestmodel.pkl exists
- Step 1: Check results/ch5/rq7/data/step04_theta_scores_allitems.csv exists
- Step 1: Check results/ch5/rq7/data/step00_tsvr_mapping.csv exists
- If ANY file missing -> trigger EXPECTATIONS ERROR -> quit with error message:
  ```
  EXPECTATIONS ERROR: RQ 5.13 requires RQ 5.7 to complete first.
  Missing file(s): [list missing files]
  Action: Run RQ 5.7 workflow (Steps 0-5) before attempting RQ 5.13.
  ```

**Validation:**
Step 1 validates all dependency files exist and are readable before proceeding to variance decomposition steps.

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

#### Step 1: Load RQ 5.7 Dependencies

**Analysis Tools:** pandas.read_csv, pickle.load (standard library)
**Validation Tools:** (determined by rq_tools - likely check_file_exists, validate_data_columns, validate_model_convergence)

**What Validation Checks:**
- Output files exist (data/step01_model_metadata.yaml, logs/step01_load_dependencies.log)
- Model metadata has expected keys (model_source, model_type, n_participants, n_observations, random_effects, converged)
- Converged flag is True (model from RQ 5.7 must have converged)
- Expected participant count (n_participants = 100)
- Expected observation count (n_observations = 380-400, allowing for minor data loss)
- CSV files have expected columns (UID, TEST, theta/SE or TSVR)

**Expected Behavior on Validation Failure:**
- If dependency file missing: Raise EXPECTATIONS ERROR, log failure, quit (master reports "RQ 5.7 incomplete")
- If model.converged = False: Raise error "RQ 5.7 model failed to converge, fix RQ 5.7 before running RQ 5.13"
- If participant count != 100: Raise error "Expected 100 participants, found [N]"
- All failures log to logs/step01_load_dependencies.log

---

#### Step 2: Extract Variance Components from LMM

**Analysis Tools:** pandas operations, numpy operations (standard library)
**Validation Tools:** (determined by rq_tools - likely validate_variance_positivity, validate_numeric_range)

**What Validation Checks:**
- Output file exists (data/step02_variance_components.csv)
- Expected row count (exactly 5 rows: var_intercept, var_slope, cov_int_slope, var_residual, cor_int_slope)
- Variance positivity: var_intercept > 0, var_slope > 0, var_residual > 0
- Correlation bounds: cor_int_slope in [-1, 1]
- No NaN values (all variance components must be estimated)
- No infinite values (indicates computation error)

**Expected Behavior on Validation Failure:**
- If variance negative: Raise error "Negative variance detected: [component] = [value], expected positive"
- If correlation out of bounds: Raise error "Correlation out of bounds: cor_int_slope = [value], expected in [-1,1]"
- If NaN detected: Raise error "NaN variance component: [component], indicates model extraction error"
- All failures log to logs/step02_variance_extraction.log, g_debug invoked

---

#### Step 3: Compute Intraclass Correlation Coefficients (ICC)

**Analysis Tools:** pandas operations, numpy operations (standard library), compute_icc_from_variance_components (tools.analysis_lmm)
**Validation Tools:** (determined by rq_tools - likely validate_icc_bounds, validate_numeric_range)

**What Validation Checks:**
- Output files exist (data/step03_icc_estimates.csv, results/step03_icc_summary.txt)
- Expected row count (exactly 3 rows: intercept, slope_simple, slope_conditional)
- ICC bounds: all estimates in [0, 1]
- No NaN values (all ICCs must be computed)
- Interpretation strings match expected categories: "Low (<0.20)" OR "Moderate (0.20-0.40)" OR "Substantial (>=0.40)"

**Expected Behavior on Validation Failure:**
- If ICC out of bounds: Raise error "ICC out of bounds: [icc_type] = [value], expected in [0,1]"
- If NaN detected: Raise error "NaN ICC: [icc_type], check Step 2 variance components"
- If interpretation string wrong: Raise error "Invalid interpretation: [string], expected Low/Moderate/Substantial"
- All failures log to logs/step03_icc_computation.log, g_debug invoked

---

#### Step 4: Extract Individual Random Effects

**Analysis Tools:** pandas operations (standard library)
**Validation Tools:** (determined by rq_tools - likely validate_data_columns, validate_dataframe_structure, validate_numeric_range)

**What Validation Checks:**
- Output files exist (data/step04_random_effects.csv, results/step04_random_slopes_descriptives.txt)
- Expected row count (exactly 100 rows, one per participant)
- Expected column count (5 columns: UID, random_intercept, random_slope, total_intercept, total_slope)
- No NaN values in random_intercept or random_slope (model must estimate for all participants)
- No duplicate UIDs (each participant appears exactly once)
- Random effects approximately in expected ranges (random_intercept: [-2,2], random_slope: [-0.5,0.5])

**Expected Behavior on Validation Failure:**
- If row count != 100: Raise error "Expected 100 participants, found [N]"
- If NaN detected: Raise error "NaN random effects for participant [UID]"
- If duplicate UID: Raise error "Duplicate participant: [UID] appears [N] times"
- If extreme outliers: Log warning "Extreme random effect detected: [UID] has [component] = [value]"
- All failures log to logs/step04_random_effects_extraction.log, g_debug invoked

---

#### Step 5: Test Intercept-Slope Correlation and Visualize Distribution

**Analysis Tools:** scipy.stats.pearsonr (standard library), matplotlib/seaborn (plotting)
**Validation Tools:** (determined by rq_tools - likely validate_correlation_test_d068, check_file_exists)

**What Validation Checks:**
- Output files exist (results/step05_intercept_slope_correlation.csv, results/step05_correlation_interpretation.txt, plots/step05_random_slopes_histogram.png, plots/step05_random_slopes_qqplot.png)
- Expected row count (exactly 5 rows: correlation, p_uncorrected, p_bonferroni, df, alpha_corrected)
- Correlation bounds: r in [-1, 1]
- P-value bounds: p_uncorrected in [0, 1], p_bonferroni in [0, 1]
- Bonferroni correction correct: p_bonferroni = min(p_uncorrected x 15, 1.0)
- Degrees of freedom correct: df = 98
- Alpha threshold correct: alpha_corrected = 0.0033
- Decision D068 compliance: BOTH p_uncorrected and p_bonferroni columns present
- PNG files successfully created (file size > 10 KB)

**Expected Behavior on Validation Failure:**
- If correlation out of bounds: Raise error "Correlation out of bounds: r = [value], expected in [-1,1]"
- If Bonferroni correction wrong: Raise error "Bonferroni correction error: expected [correct_value], found [value]"
- If dual p-values missing: Raise error "Decision D068 violation: Missing p_bonferroni column"
- If PNG files missing: Raise error "Plotting failed, check matplotlib installation"
- All failures log to logs/step05_correlation_test.log, g_debug invoked

---

## Summary

**Total Steps:** 5 analysis steps

**Estimated Runtime:** 5-10 minutes total (all steps are data extraction/computation, no model fitting)

**Cross-RQ Dependencies:** RQ 5.7 (MUST complete Steps 0-5 before this RQ can execute)

**Primary Outputs:**
- Variance components (var_intercept, var_slope, cov_int_slope, var_residual)
- ICC estimates (intercept, slope_simple, slope_conditional)
- Individual random effects (100 participants x 5 columns, REQUIRED INPUT for RQ 5.14)
- Intercept-slope correlation test (with dual p-values per Decision D068)
- Visualizations (histogram + Q-Q plot of random slopes distribution)

**Validation Coverage:** 100% (all 5 steps have validation requirements with 4-layer substance criteria)

**Key Decision Applied:**
- Decision D068: Dual p-value reporting for intercept-slope correlation (uncorrected + Bonferroni)

**Downstream Dependencies:**
- RQ 5.14 requires data/step04_random_effects.csv from Step 4 of this RQ for K-means clustering analysis

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (approval gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts
5. Workflow continues to Step 14: bash execution runs scripts -> rq_inspect validates outputs

---

**Version History:**
- v1.0 (2025-11-27): Initial plan created by rq_planner agent for RQ 5.13 (Between-Person Variance in Forgetting Rates)
