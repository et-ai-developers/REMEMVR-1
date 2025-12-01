# Analysis Plan: RQ 5.1.1 - Functional Form of Forgetting Trajectories

**Research Question:** 5.1.1
**Created:** 2025-11-25
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ determines which functional form best describes episodic forgetting trajectories across a 6-day retention interval. We compare 5 candidate mathematical models (Linear, Quadratic, Logarithmic, Linear+Logarithmic, Quadratic+Logarithmic) using model selection via AIC (Akaike Information Criterion).

**Pipeline:** 2-Pass IRT (single omnibus factor with purification) -> LMM (5 candidate models) -> AIC model selection

**Steps:** 7 analysis steps (Step 1: IRT Pass 1, Step 2: Item purification, Step 3: IRT Pass 2, Step 4: Data prep, Step 5: LMM fitting, Step 6: Model selection, Step 7: Plot preparation)

**Estimated Runtime:** High (Step 1: 30-60 min IRT Pass 1, Step 3: 20-40 min IRT Pass 2, Steps 2/4-7: <10 min total)

**Key Decisions Applied:**
- Decision D039: 2-Pass IRT purification (|b| ≤ 3.0 AND a ≥ 0.4) - APPLIES to unidimensional RQ 5.7 (improves measurement quality regardless of dimensionality)
- Decision D070: TSVR as time variable (actual hours since encoding, not nominal days)
- Decision D069: Dual-scale trajectory plots (theta + probability scales)

**Critical Design Note:**
RQ 5.7 uses DERIVED data from RQ 5.1 (step00_irt_input.csv). We reprocess this data with "All" factor configuration (single omnibus dimension aggregating all What/Where/When items) instead of domain-specific factors. Different IRT configuration yields theta estimates optimized for overall forgetting trajectory, not domain-specific patterns.

---

## Analysis Plan

This RQ requires 7 steps (2-pass IRT with purification):

### Step 1: IRT Pass 1 Calibration (All Items)

**Dependencies:** RQ 5.1 Step 0 complete (requires step00_irt_input.csv)
**Complexity:** High (30-60 minute IRT model calibration)

**Purpose:** Calibrate IRT model with single "All" factor on complete item set (all 105 items) to establish baseline item parameters for purification. This is Pass 1 of 2-pass IRT per Decision D039.

**Input:**

**File:** results/ch5/5.2.1/data/step00_irt_input.csv (from RQ 5.1 data extraction)
**Source:** RQ 5.1 Step 0 (data preparation)
**Format:** CSV, wide format (one row per composite_ID, one column per item)
**Columns:**
  - `composite_ID` (string, format: UID_test, e.g., "P001_T1")
  - Item response columns (format: VR-{paradigm}-{test}-{domain}-ANS, e.g., "VR-IFR-A01-N-ANS")
  - Values: {0, 1} (dichotomized accuracy: 0=incorrect, 1=correct)
**Expected Rows:** 400 (100 participants x 4 tests)
**Expected Columns:** ~150-200 columns (composite_ID + all What/Where/When items from interactive paradigms)

**Processing:**

**Analysis Type:** IRT calibration with Graded Response Model (GRM)
**Configuration:**
- Single factor: "All" (omnibus dimension aggregating all items, NOT separate What/Where/When factors)
- Prior: p1_med (medium-precision theta prior, precision=1.0 per Decision D068)
- Model: GRM with 2 categories (dichotomous items: 0, 1)
- All items assigned to "All" dimension in Q-matrix (100% loading on single factor)

**Method:**
1. Read step00_irt_input.csv (inherited from RQ 5.1)
2. Configure IRT model with "All" analysis set (single-factor Q-matrix)
3. Fit GRM model via variational inference (IWAVE algorithm)
4. Extract theta scores (ability estimates per composite_ID)
5. Extract item parameters (discrimination a, difficulty b per item)
6. Save outputs to data/ and logs/

**Output:**

**File 1:** data/step01_theta_scores.csv
**Format:** CSV, one row per composite_ID
**Columns:**
  - `composite_ID` (string, format: UID_test)
  - `Theta_All` (float, IRT ability estimate for omnibus factor, range typically -3 to +3)
  - `SE_All` (float, standard error of theta estimate, range typically 0.1 to 1.0)
**Expected Rows:** 400 (100 participants x 4 tests)

**File 2:** logs/step01_item_parameters.csv
**Format:** CSV, one row per item
**Columns:**
  - `item_name` (string, format: VR-{paradigm}-{test}-{domain}-ANS)
  - `dimension` (string, value: "All" for all items)
  - `a` (float, discrimination parameter, range >0.0)
  - `b` (float, difficulty parameter, unrestricted range)
**Expected Rows:** ~150-200 items (all What/Where/When items from step00_irt_input.csv)

**File 3:** logs/step01_calibration.log
**Format:** Text log with IRT convergence diagnostics
**Content:** Convergence status, final log-likelihood, parameter bounds, warnings

**Validation Requirement:**

Validation tools MUST be used after IRT calibration tool execution. Specific validation tools will be determined by rq_tools based on IRT calibration requirements. The rq_analysis agent will embed validation tool calls after the analysis tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_theta_scores.csv: 400 rows x 3 columns (composite_ID: object, Theta_All: float64, SE_All: float64)
- logs/step01_item_parameters.csv: 150-200 rows x 4 columns (item_name: object, dimension: object, a: float64, b: float64)
- logs/step01_calibration.log: text file with convergence diagnostics

*Value Ranges:*
- Theta_All in [-4, 4] (typical IRT ability range, outside suggests calibration issue)
- SE_All in [0.1, 1.5] (above 1.5 = unreliable estimates, below 0.1 suspicious)
- a (discrimination) > 0.0 (negative impossible for GRM), typically in [0.2, 4.0]
- b (difficulty) unrestricted (temporal items may have |b| > 3.0, this is valid)

*Data Quality:*
- All 400 composite_IDs present (no data loss during calibration)
- No NaN values in Theta_All or SE_All (model must estimate for all observations)
- All items have dimension = "All" (single-factor configuration)
- No duplicate composite_IDs or item_names

*Log Validation:*
- Required pattern: "Model converged: True" or "Convergence achieved"
- Required pattern: "VALIDATION - PASS: theta range" (from validation tool)
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "NaN parameters"
- Acceptable warnings: "Some items have high discrimination (a > 3.0)" (valid for well-performing items)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 400 rows in theta_scores.csv, found 387")
- Log failure to logs/step01_calibration.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose root cause (common: convergence failure, data mismatch)

---

### Step 2: Item Purification (Decision D039)

**Dependencies:** Step 1 (requires Pass 1 item parameters)
**Complexity:** Low (<1 min, simple filtering)

**Purpose:** Apply Decision D039 purification thresholds to identify high-quality items for Pass 2 calibration. Exclude items with extreme difficulty (|b| > 3.0) or poor discrimination (a < 0.4).

**Input:**

**File:** logs/step01_item_parameters.csv (from Step 1 Pass 1)
**Format:** CSV, one row per item
**Columns:** item_name, dimension, a, b
**Expected Rows:** ~105 items (all What/Where/When items)

**Processing:**

**Tool:** tools.analysis_irt.purify_items()

**Purification Criteria (Decision D039):**
1. Difficulty threshold: |b| ≤ 3.0 (extreme difficulty distorts ability scores)
2. Discrimination threshold: a ≥ 0.4 (low discrimination adds noise without signal)
3. Exclusion rule: Items failing EITHER criterion are excluded (logical OR)

**Method:**
1. Read step01_item_parameters.csv (Pass 1 results)
2. Apply purification thresholds via purify_items() tool
3. Create purified item list (items meeting BOTH criteria)
4. Compute retention statistics (% retained per domain if desired, omnibus has no domains)
5. Save purified item list for Pass 2 calibration

**Output:**

**File:** data/step02_purified_items.csv
**Format:** CSV, one row per retained item
**Columns:**
  - `item_name` (string, format: TQ_* per REMEMVR naming)
  - `pass1_a` (float, Pass 1 discrimination)
  - `pass1_b` (float, Pass 1 difficulty)
  - `dimension` (string, value: "All")
**Expected Rows:** ~40-60 items (40-60% retention typical for REMEMVR per RQ 5.1 evidence)

**Validation Requirement:**

Validation tools MUST be used after purification. The rq_analysis agent will embed validation tool calls.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_purified_items.csv: 40-60 rows x 4 columns (item_name: object, pass1_a: float64, pass1_b: float64, dimension: object)

*Value Ranges:*
- pass1_a ≥ 0.4 (purification threshold enforced)
- |pass1_b| ≤ 3.0 (purification threshold enforced)
- Retention rate: 30-70% typical (below 30% = too restrictive, above 70% = purification ineffective)

*Data Quality:*
- No duplicate item_names
- All items have dimension = "All"
- No NaN values

**Expected Behavior on Validation Failure:**
- If retention rate < 30%: Log warning "Low retention rate may indicate poor item quality" but proceed
- If retention rate < 10%: Raise error "Insufficient items for Pass 2 calibration"
- If all items excluded: Raise error "No items passed purification thresholds"

---

### Step 3: IRT Pass 2 Calibration (Purified Items)

**Dependencies:** Step 2 (requires purified item list)
**Complexity:** High (20-40 min IRT calibration, fewer items than Pass 1)

**Purpose:** Re-calibrate IRT model with purified item set only to obtain final theta estimates with improved measurement quality. This is Pass 2 of 2-pass IRT per Decision D039.

**Input:**

**File 1:** results/ch5/5.2.1/data/step00_irt_input.csv (same raw data as Step 1)
**Source:** RQ 5.1 Step 0
**Format:** CSV, wide format
**Expected Rows:** 400

**File 2:** data/step02_purified_items.csv (from Step 2)
**Source:** Step 2 purification
**Format:** CSV, list of retained items
**Expected Rows:** ~40-60 items

**Processing:**

**Tool:** tools.analysis_irt.calibrate_irt()

**Configuration:**
- Single factor: "All" (same as Pass 1)
- Prior: p1_med (medium-precision theta prior)
- Model: GRM with 2 categories
- Items: ONLY purified items (filtered from step00_irt_input.csv using step02_purified_items.csv)

**Method:**
1. Read step00_irt_input.csv (raw item responses)
2. Read step02_purified_items.csv (purified item list)
3. Filter step00_irt_input.csv to include ONLY purified items
4. Configure IRT model with "All" analysis set (single factor)
5. Fit GRM model via variational inference
6. Extract Pass 2 theta scores (final ability estimates)
7. Extract Pass 2 item parameters (for diagnostics)
8. Save outputs to data/ and logs/

**Output:**

**File 1:** data/step03_theta_scores.csv (FINAL theta estimates for LMM)
**Format:** CSV, one row per composite_ID
**Columns:**
  - `composite_ID` (string, format: UID_test)
  - `Theta_All` (float, final IRT ability estimate, range typically -3 to +3)
  - `SE_All` (float, standard error of theta estimate, typically 0.1-1.0)
**Expected Rows:** 400 (100 participants x 4 tests)

**File 2:** logs/step03_item_parameters.csv
**Format:** CSV, one row per purified item
**Columns:**
  - `item_name` (string)
  - `dimension` (string, value: "All")
  - `a` (float, Pass 2 discrimination)
  - `b` (float, Pass 2 difficulty)
**Expected Rows:** ~40-60 items (matches step02_purified_items.csv count)

**File 3:** logs/step03_calibration.log
**Format:** Text log with IRT convergence diagnostics
**Content:** Convergence status, final log-likelihood, parameter bounds, warnings

**Validation Requirement:**

Validation tools MUST be used after Pass 2 calibration. The rq_analysis agent will embed validation tool calls.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_theta_scores.csv: 400 rows x 3 columns (composite_ID: object, Theta_All: float64, SE_All: float64)
- logs/step03_item_parameters.csv: 40-60 rows x 4 columns (item_name: object, dimension: object, a: float64, b: float64)
- logs/step03_calibration.log: text file with convergence diagnostics

*Value Ranges:*
- Theta_All in [-4, 4] (typical IRT ability range)
- SE_All in [0.1, 1.5] (above 1.5 = unreliable estimates)
- a (discrimination) ≥ 0.4 (purification threshold, should be maintained or improved)
- |b| (difficulty) ≤ 3.0 (purification threshold, should be maintained)

*Data Quality:*
- All 400 composite_IDs present (no data loss during calibration)
- No NaN values in Theta_All or SE_All
- Item count matches step02_purified_items.csv (no items lost during calibration)
- All items have dimension = "All"

*Comparison to Pass 1:*
- SE_All should be equal or lower than Pass 1 (purification improves precision)
- Theta_All correlation with Pass 1 should be high (r > 0.80, measuring same construct)

*Log Validation:*
- Required pattern: "Model converged: True" or "Convergence achieved"
- Required pattern: "VALIDATION - PASS: theta range"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "NaN parameters"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step03_calibration.log
- Quit script immediately (do NOT proceed to Step 4)
- g_debug invoked to diagnose root cause

---


### Step 4: Prepare LMM Input Data

**Dependencies:** Step 3 (requires theta scores)
**Complexity:** Low (<5 min data transformation)

**Purpose:** Transform IRT output to LMM-ready format with time variable transformations (TSVR hours, Days, Days^2, log(Days+1)) and clean column naming.

**Input:**

**File 1:** data/step01_theta_scores.csv (from Step 1)
**Format:** CSV, one row per composite_ID
**Columns:** composite_ID, Theta_All, SE_All
**Expected Rows:** 400

**File 2:** results/ch5/5.2.1/data/step00_tsvr_mapping.csv (from RQ 5.1 TSVR extraction)
**Format:** CSV, one row per composite_ID
**Columns:** composite_ID, TSVR_hours (time since VR session in actual hours)
**Expected Rows:** 400

**Processing:**

**Transformation 1: Rename theta column**
- Rename `Theta_All` -> `Theta` (simplifies LMM formula readability)
- Keep `SE_All` as `SE` (standard error of theta)

**Transformation 2: Merge TSVR time variable**
- Merge step01_theta_scores.csv with step00_tsvr_mapping.csv on composite_ID
- Left join (keep all theta scores, add TSVR_hours)
- Validation: All composite_IDs must match (no missing TSVR values tolerated)

**Transformation 3: Create time transformations for LMM**
- `Days` = TSVR_hours / 24.0 (convert hours to days for interpretability, labeled "Days" in output)
- `Days_squared` = Days^2 (quadratic term for polynomial models)
- `log_Days_plus1` = log(Days + 1) (logarithmic term, +1 prevents log(0) at encoding)

**Transformation 4: Parse composite_ID**
- Extract `UID` from composite_ID (participant identifier)
- Extract `test` from composite_ID (test session: T1, T2, T3, T4)

**Output:**

**File 1:** data/step02_lmm_input.csv
**Format:** CSV, long format (one row per observation = participant x test combination)
**Columns:**
  - `composite_ID` (string, format: UID_test)
  - `UID` (string, participant identifier, e.g., "P001")
  - `test` (string, test session identifier: T1, T2, T3, T4)
  - `Theta` (float, renamed from Theta_All, ability estimate)
  - `SE` (float, renamed from SE_All, standard error)
  - `TSVR_hours` (float, actual hours since encoding per Decision D070)
  - `Days` (float, TSVR_hours / 24, used as time variable for interpretability)
  - `Days_squared` (float, Days^2, for quadratic models)
  - `log_Days_plus1` (float, log(Days+1), for logarithmic models)
**Expected Rows:** 400 (100 participants x 4 tests)
**Expected Columns:** 9

**Validation Requirement:**

Validation tools MUST be used after data preparation tool execution. Specific validation tools will be determined by rq_tools based on data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_lmm_input.csv: 400 rows x 9 columns (all float64 except composite_ID, UID, test: object)

*Value Ranges:*
- Theta in [-4, 4] (inherited from Step 1)
- SE in [0.1, 1.5] (inherited from Step 1)
- TSVR_hours in [0, 168] (0=encoding, 168=7 days max in study design)
- Days in [0, 7] (TSVR_hours / 24)
- Days_squared in [0, 49] (Days^2, max = 7^2)
- log_Days_plus1 in [0, 2.2] (log(7+1) approximately 2.08)

*Data Quality:*
- All 400 rows present (no data loss during merge)
- No NaN values in any column (merge must be complete)
- No duplicate composite_IDs
- Each UID appears exactly 4 times (one per test session T1-T4)

*Log Validation:*
- Required pattern: "Data preparation complete: 400 observations created"
- Required pattern: "TSVR merge successful: 400/400 matched"
- Forbidden patterns: "ERROR", "Missing TSVR values", "Duplicate composite_IDs"
- Acceptable warnings: None expected for data preparation

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "TSVR merge failed: 387/400 matched")
- Log failure to logs/step02_prepare_data.log
- Quit script immediately (do NOT proceed to Step 3)
- g_debug invoked to diagnose (common: TSVR file path incorrect, composite_ID mismatch)

---

### Step 5: Fit 5 Candidate LMM Models

**Dependencies:** Step 4 (requires LMM input data)
**Complexity:** Medium (5-10 min to fit 5 models)

**Purpose:** Fit 5 candidate Linear Mixed Models representing different functional forms of forgetting trajectories. All models use random intercepts and random slopes by UID. Fit with REML=False for valid AIC comparison.

**Input:**

**File:** data/step02_lmm_input.csv (from Step 2)
**Format:** CSV, long format
**Columns:** composite_ID, UID, test, Theta, SE, TSVR_hours, Days, Days_squared, log_Days_plus1
**Expected Rows:** 400

**Processing:**

**Model Specifications (5 candidate models):**

1. **Linear Model:**
   - Formula: `Theta ~ Days + (1 + Days | UID)`
   - Fixed effects: Intercept, Days
   - Random effects: Random intercept + random slope for Days per UID
   - Theoretical basis: Simple trace decay (linear decline over time)

2. **Quadratic Model:**
   - Formula: `Theta ~ Days + Days_squared + (1 + Days | UID)`
   - Fixed effects: Intercept, Days, Days^2
   - Random effects: Random intercept + random slope for Days per UID
   - Theoretical basis: Two-phase consolidation (rapid then slow decay)

3. **Logarithmic Model:**
   - Formula: `Theta ~ log_Days_plus1 + (1 + log_Days_plus1 | UID)`
   - Fixed effects: Intercept, log(Days+1)
   - Random effects: Random intercept + random slope for log(Days+1) per UID
   - Theoretical basis: Ebbinghaus curve (logarithmic forgetting)

4. **Linear + Logarithmic Model:**
   - Formula: `Theta ~ Days + log_Days_plus1 + (1 + Days | UID)`
   - Fixed effects: Intercept, Days, log(Days+1)
   - Random effects: Random intercept + random slope for Days per UID
   - Theoretical basis: Flexible approximation combining linear and logarithmic trends

5. **Quadratic + Logarithmic Model:**
   - Formula: `Theta ~ Days + Days_squared + log_Days_plus1 + (1 + Days | UID)`
   - Fixed effects: Intercept, Days, Days^2, log(Days+1)
   - Random effects: Random intercept + random slope for Days per UID
   - Theoretical basis: Most flexible approximation (polynomial + logarithmic)

**Fitting Method:**
- Use REML=False (maximum likelihood estimation required for valid AIC comparison)
- Fit all 5 models sequentially
- Extract: AIC, BIC, log-likelihood, convergence status per model
- Save fitted model objects (pickle format for downstream analysis)

**Output:**

**File 1:** data/step03_model_fits.pkl
**Format:** Python pickle containing dictionary of 5 fitted model objects
**Keys:** "Linear", "Quadratic", "Logarithmic", "LinLog", "QuadLog"
**Values:** Fitted statsmodels MixedLM objects

**File 2:** results/step03_model_comparison.csv
**Format:** CSV, one row per model
**Columns:**
  - `model_name` (string: Linear, Quadratic, Logarithmic, LinLog, QuadLog)
  - `AIC` (float, Akaike Information Criterion)
  - `BIC` (float, Bayesian Information Criterion)
  - `log_likelihood` (float, log-likelihood at convergence)
  - `n_params` (int, number of estimated parameters)
  - `converged` (bool, convergence status)
**Expected Rows:** 5 (one per candidate model)

**File 3:** logs/step03_lmm_fitting.log
**Format:** Text log with LMM fitting diagnostics
**Content:** Convergence messages, warnings, parameter counts per model

**Validation Requirement:**

Validation tools MUST be used after LMM fitting tool execution. Specific validation tools will be determined by rq_tools based on LMM convergence and fit requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_model_fits.pkl: Python pickle with 5 model objects
- results/step03_model_comparison.csv: 5 rows x 6 columns (model_name: object, AIC/BIC/log_likelihood: float64, n_params: int64, converged: bool)
- logs/step03_lmm_fitting.log: text file with convergence diagnostics

*Value Ranges:*
- AIC in [-2000, 2000] (typical range for N=400, theta scale outcomes)
- BIC in [-2000, 2000] (similar to AIC, slightly larger due to parameter penalty)
- log_likelihood in [-1000, 0] (negative, more negative = worse fit)
- n_params in [4, 8] (Linear=4, QuadLog=7, varies by model complexity)
- converged: True for ALL 5 models (convergence failure requires g_debug)

*Data Quality:*
- All 5 models present in step03_model_fits.pkl (keys: Linear, Quadratic, Logarithmic, LinLog, QuadLog)
- All 5 models have converged=True
- No NaN values in AIC, BIC, or log_likelihood
- AIC values properly ordered (lower AIC = better fit)

*Log Validation:*
- Required pattern: "All 5 models converged successfully"
- Required pattern: "VALIDATION - PASS: LMM convergence" (from validation tool)
- Forbidden patterns: "ERROR", "Convergence failed for model", "Singular matrix"
- Acceptable warnings: "Some models close in AIC (delta AIC < 2)" (indicates model uncertainty)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Quadratic model failed to converge")
- Log failure to logs/step03_lmm_fitting.log
- Quit script immediately (do NOT proceed to Step 4)
- g_debug invoked to diagnose (common: singular covariance matrix, insufficient data for complex model)

---

### Step 6: Model Selection via AIC

**Dependencies:** Step 5 (requires fitted models and AIC values)
**Complexity:** Low (<2 min calculation)

**Purpose:** Select best-fitting model using Akaike Information Criterion (AIC) and compute Akaike weights to quantify relative evidence for each candidate model.

**Input:**

**File 1:** results/step03_model_comparison.csv (from Step 3)
**Format:** CSV with model AIC/BIC/log-likelihood values
**Columns:** model_name, AIC, BIC, log_likelihood, n_params, converged
**Expected Rows:** 5

**File 2:** data/step03_model_fits.pkl (from Step 3)
**Format:** Python pickle with fitted model objects
**Keys:** Linear, Quadratic, Logarithmic, LinLog, QuadLog

**Processing:**

**AIC-Based Model Selection (Burnham & Anderson, 2004 framework):**

1. **Compute delta AIC for each model:**
   - delta AIC_i = AIC_i - AIC_min (difference from best model)
   - Best model has delta AIC = 0

2. **Compute Akaike weights:**
   - w_i = exp(-0.5 * delta AIC_i) / sum(exp(-0.5 * delta AIC_j)) for all j
   - Weights sum to 1.0
   - Interpretation: w_i = relative probability that model i is the best approximating model in candidate set

3. **Identify best model:**
   - Model with lowest AIC (delta AIC = 0)
   - Report delta AIC for all models relative to best

4. **Categorize uncertainty based on best model's weight:**
   - w_best > 0.90: Very strong evidence for best model
   - w_best in [0.60, 0.90]: Strong evidence
   - w_best in [0.30, 0.60]: Moderate evidence (consider model averaging)
   - w_best < 0.30: High uncertainty (report top 2-3 models, cumulative weight)

5. **Save best model for downstream analysis:**
   - Extract best model object from step03_model_fits.pkl
   - Save separately as step04_best_model.pkl

**Output:**

**File 1:** results/step04_aic_comparison.csv
**Format:** CSV, one row per model, sorted by AIC (best first)
**Columns:**
  - `model_name` (string)
  - `AIC` (float)
  - `delta_AIC` (float, AIC_i - AIC_min)
  - `akaike_weight` (float, relative probability, sums to 1.0)
  - `cumulative_weight` (float, cumulative sum of weights when sorted by AIC)
**Expected Rows:** 5
**Sort Order:** Ascending by AIC (best model first)

**File 2:** data/step04_best_model.pkl
**Format:** Python pickle containing best-fitting model object
**Content:** Fitted statsmodels MixedLM object (model with lowest AIC)

**File 3:** results/step04_best_model_summary.txt
**Format:** Text summary of best model
**Content:**
  - Best model name
  - AIC, BIC, log-likelihood
  - Akaike weight
  - Uncertainty category (very strong / strong / moderate / high)
  - Fixed effects table (coefficients, SE, z, p-values)
  - Random effects variance components
  - Interpretation: Which functional form best approximates forgetting trajectory

**Validation Requirement:**

Validation tools MUST be used after model selection tool execution. Specific validation tools will be determined by rq_tools based on AIC calculation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step04_aic_comparison.csv: 5 rows x 5 columns (model_name: object, AIC/delta_AIC/akaike_weight/cumulative_weight: float64)
- data/step04_best_model.pkl: Python pickle with single model object
- results/step04_best_model_summary.txt: text file with model summary

*Value Ranges:*
- delta_AIC in [0, 20] (best model = 0, others positive, >10 indicates very poor fit)
- akaike_weight in (0, 1) (each weight between 0 and 1 exclusive)
- cumulative_weight: monotonic increasing from first weight to 1.0 at last row
- Sum of akaike_weight across all models = 1.0 (within floating-point precision)

*Data Quality:*
- Exactly 5 rows (one per candidate model)
- Sorted by AIC ascending (best model first, row 1 has delta_AIC = 0)
- Best model akaike_weight is largest (row 1 has highest weight)
- No NaN values in any column
- cumulative_weight[5] = 1.0 (all probability mass accounted for)

*Log Validation:*
- Required pattern: "Best model: {model_name} (AIC = {value})"
- Required pattern: "Akaike weight: {w_best:.3f} ({uncertainty_category})"
- Required pattern: "VALIDATION - PASS: Akaike weights sum to 1.0"
- Forbidden patterns: "ERROR", "Weights do not sum to 1.0", "NaN in AIC"
- Acceptable warnings: "High model uncertainty (w_best < 0.30)" (valid exploratory finding)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Akaike weights sum to 0.87, expected 1.0")
- Log failure to logs/step04_model_selection.log
- Quit script immediately (do NOT proceed to Step 5)
- g_debug invoked to diagnose (common: numerical precision error, missing model in calculation)

---

### Step 7: Prepare Multi-Panel Plot Data

**Dependencies:** Steps 2, 3, 4 (requires LMM input data, all 5 fitted models, best model identification)
**Complexity:** Low (<5 min data aggregation)

**Purpose:** Create plot source CSV for multi-panel visualization showing all 5 candidate model fits overlaid on observed data with error bars. Decision D069 dual-scale requirement applies (theta + probability scales).

**Input:**

**File 1:** data/step02_lmm_input.csv (from Step 2)
**Format:** CSV with observed theta scores
**Columns:** composite_ID, UID, test, Theta, SE, TSVR_hours, Days, Days_squared, log_Days_plus1
**Expected Rows:** 400

**File 2:** data/step03_model_fits.pkl (from Step 3)
**Format:** Python pickle with all 5 fitted models
**Keys:** Linear, Quadratic, Logarithmic, LinLog, QuadLog

**File 3:** results/step04_aic_comparison.csv (from Step 4)
**Format:** CSV with model comparison results (for annotating best model)
**Columns:** model_name, AIC, delta_AIC, akaike_weight, cumulative_weight

**Processing:**

**Step 5a: Compute Observed Means with Confidence Intervals**

1. Group step02_lmm_input.csv by test session (T1, T2, T3, T4)
2. Compute mean Theta per test
3. Compute 95% CI using SE: CI_lower = mean - 1.96*SE_pooled, CI_upper = mean + 1.96*SE_pooled
4. Merge with Days (TSVR_hours / 24) for X-axis plotting

**Step 5b: Generate Model Predictions**

For each of 5 models:
1. Create prediction grid: Days in [0, 7] with 50 points
2. Compute Days_squared, log_Days_plus1 for prediction grid
3. Generate model predictions using fitted coefficients (population-level, random effects = 0)
4. Store predictions with model_name label

**Step 5c: Transform to Probability Scale (Decision D069)**

1. Use theta -> probability transformation: p = 1 / (1 + exp(-1.7 * theta))
2. Apply to observed means and all model predictions
3. Create separate probability-scale plot data

**Output:**

**File 1 (Theta Scale):** plots/step05_functional_form_theta_data.csv
**Format:** CSV for theta-scale multi-panel plot
**Columns:**
  - `Days` (float, time variable for X-axis)
  - `observed_theta` (float, mean observed theta per test session)
  - `CI_lower_theta` (float, lower 95% CI for observed means)
  - `CI_upper_theta` (float, upper 95% CI for observed means)
  - `pred_Linear` (float, Linear model predictions)
  - `pred_Quadratic` (float, Quadratic model predictions)
  - `pred_Logarithmic` (float, Logarithmic model predictions)
  - `pred_LinLog` (float, Lin+Log model predictions)
  - `pred_QuadLog` (float, Quad+Log model predictions)
  - `best_model` (string, name of best model for annotation)
**Expected Rows:** 50 (prediction grid points) + 4 (observed means) = 54 rows with NaN handling

**File 2 (Probability Scale):** plots/step05_functional_form_probability_data.csv
**Format:** CSV for probability-scale multi-panel plot (Decision D069 dual-scale)
**Columns:**
  - `Days` (float, time variable for X-axis)
  - `observed_prob` (float, observed theta transformed to probability)
  - `CI_lower_prob` (float, lower 95% CI transformed to probability)
  - `CI_upper_prob` (float, upper 95% CI transformed to probability)
  - `pred_Linear_prob` (float, Linear model predictions transformed)
  - `pred_Quadratic_prob` (float, Quadratic model predictions transformed)
  - `pred_Logarithmic_prob` (float, Logarithmic model predictions transformed)
  - `pred_LinLog_prob` (float, Lin+Log model predictions transformed)
  - `pred_QuadLog_prob` (float, Quad+Log model predictions transformed)
  - `best_model` (string, name of best model for annotation)
**Expected Rows:** 54 (same structure as theta-scale file)

**Validation Requirement:**

Validation tools MUST be used after plot data preparation tool execution. Specific validation tools will be determined by rq_tools based on plot data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- plots/step05_functional_form_theta_data.csv: 54 rows x 10 columns (Days/theta/CI/predictions: float64, best_model: object)
- plots/step05_functional_form_probability_data.csv: 54 rows x 10 columns (Days/prob/CI/predictions: float64, best_model: object)

*Value Ranges:*
- Days in [0, 7] (time range for X-axis)
- observed_theta in [-3, 3] (typical IRT ability range)
- CI_lower_theta, CI_upper_theta in [-4, 4] (confidence bounds)
- pred_* (all predictions) in [-4, 4] (model predictions on theta scale)
- observed_prob in [0, 1] (probability scale)
- CI_lower_prob, CI_upper_prob in [0, 1] (probability confidence bounds)
- pred_*_prob (all predictions) in [0, 1] (model predictions on probability scale)

*Data Quality:*
- No NaN values in Days column (time grid must be complete)
- 4 rows with non-NaN observed_theta (T1-T4 observed means)
- 50 rows with non-NaN predictions (prediction grid)
- CI_upper > CI_lower for all observed data rows
- CI_upper_prob > CI_lower_prob for all observed data rows
- Monotonicity: Probability transform preserves order (if theta1 > theta2, then prob1 > prob2)

*Log Validation:*
- Required pattern: "Plot data preparation complete: 54 rows created"
- Required pattern: "Theta scale: 4 observed + 50 predicted"
- Required pattern: "Probability scale: transformation successful"
- Required pattern: "Best model annotated: {model_name}"
- Forbidden patterns: "ERROR", "NaN in Days", "Probability out of bounds"
- Acceptable warnings: "Some predictions extrapolate beyond observed data" (valid for prediction grid)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Probability values out of [0,1] bounds: found 1.03")
- Log failure to logs/step05_prepare_plot_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- g_debug invoked to diagnose (common: transformation error, model prediction failure)

**Plotting Function (rq_plots will execute):**
- Multi-panel plot (2 panels: theta scale + probability scale per Decision D069)
- X-axis: Days (0 to 7)
- Y-axis Panel 1: Theta (-3 to +3)
- Y-axis Panel 2: Probability (0 to 1)
- Observed data: Points with error bars (CI_lower to CI_upper)
- Model predictions: Lines (5 lines per panel, one per candidate model)
- Annotation: Highlight best model (thicker line, different color, label with Akaike weight)
- rq_plots maps this description to tools/plots.py functions (exact function TBD by rq_plots agent)

---

## Expected Data Formats

### Composite_ID Format

**Pattern:** `{UID}_{test}`
**Example:** `P001_T1` (Participant P001, Test session T1)
**Used Throughout:** All IRT and LMM input files
**Parsing:** UID = composite_ID.split('_')[0], test = composite_ID.split('_')[1]

### Time Variable Transformations

**TSVR_hours (Raw):** Actual hours since encoding (0, 24, 72, 144 for nominal Days 0, 1, 3, 6)
**Days (Interpretable):** TSVR_hours / 24.0 (for plotting and reporting)
**Days_squared (Polynomial):** Days^2 (for Quadratic and Quad+Log models)
**log_Days_plus1 (Logarithmic):** log(Days + 1) (for Logarithmic, Lin+Log, Quad+Log models)

**Decision D070 Compliance:** LMM uses TSVR_hours as actual time variable, Days is derived for interpretability only.

### Theta to Probability Transformation (Decision D069)

**Formula:** `p = 1 / (1 + exp(-1.7 * theta))`
**Rationale:** Standard IRT 2PL probability curve with discrimination parameter = 1.7 (approximates logistic CDF)
**Applied To:** All theta values (observed means and model predictions) for probability-scale plotting

### Column Naming Conventions

**From names.md (RQ 5.1 conventions reused):**
- `composite_ID`: Primary key (UID_test format)
- `UID`: Participant identifier
- `test`: Test session (T1, T2, T3, T4)
- `TSVR_hours`: Time since VR in hours (Decision D070)
- `Theta`: IRT ability estimate (renamed from Theta_All in Step 2)
- `SE`: Standard error of theta

**New for RQ 5.7:**
- `Days`: TSVR_hours / 24 (interpretable time variable)
- `Days_squared`: Days^2 (polynomial term)
- `log_Days_plus1`: log(Days+1) (logarithmic term)
- `delta_AIC`: AIC difference from best model
- `akaike_weight`: Relative model probability
- `pred_{model_name}`: Model predictions (Linear, Quadratic, Logarithmic, LinLog, QuadLog)

---

## Cross-RQ Dependencies

**Dependency Type:** DERIVED Data from RQ 5.1 (not RAW data from master.xlsx)

**This RQ requires outputs from:**

**RQ 5.1 (Domain-Specific Forgetting Trajectories)**
  - **File 1:** results/ch5/5.2.1/data/step00_irt_input.csv
  - **Used in:** Step 1 (IRT calibration with "All" factor)
  - **Rationale:** RQ 5.7 reprocesses RQ 5.1 IRT input data with different factor structure (single omnibus "All" factor instead of What/Where/When factors) to estimate overall forgetting trajectory rather than domain-specific patterns

  - **File 2:** results/ch5/5.2.1/data/step00_tsvr_mapping.csv
  - **Used in:** Step 2 (merge TSVR time variable with theta scores)
  - **Rationale:** TSVR (actual hours since encoding) required per Decision D070 for accurate temporal modeling

**Execution Order Constraint:**
1. RQ 5.1 Step 0 must complete first (provides step00_irt_input.csv and step00_tsvr_mapping.csv)
2. RQ 5.7 executes (reprocesses RQ 5.1 data with different IRT configuration)

**Data Source Boundaries:**
- **RAW data:** None (RQ 5.7 does NOT extract from master.xlsx directly)
- **DERIVED data:** step00_irt_input.csv and step00_tsvr_mapping.csv from RQ 5.1
- **Scope:** RQ 5.7 does NOT re-extract data, only re-calibrates IRT with different factor structure

**Validation:**
- Step 1: Check results/ch5/5.2.1/data/step00_irt_input.csv exists (EXPECTATIONS ERROR if absent)
- Step 2: Check results/ch5/5.2.1/data/step00_tsvr_mapping.csv exists (EXPECTATIONS ERROR if absent)
- If either file missing -> quit with error -> user must execute RQ 5.1 Step 0 first

**Why This Dependency Exists:**
RQ 5.1 extracts and prepares VR item responses for domain-specific analysis (What/Where/When factors). RQ 5.7 reuses this prepared data but reconfigures IRT to create single omnibus factor "All" aggregating all items. This avoids duplicate data extraction while enabling different theoretical questions (domain-specific vs overall forgetting).

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
- g_code (Step 14 workflow) will generate stepN_name.py scripts with validation function calls
- bash execution (Step 14 workflow) will run analysis -> validation -> error on validation failure

**Downstream Agent Requirements:**
- **rq_tools:** MUST specify validation tool for EVERY analysis step (no exceptions)
- **rq_analysis:** MUST embed validation tool call for EVERY analysis step (no exceptions)
- **g_code:** MUST generate code with validation function calls (no exceptions)
- **rq_inspect:** MUST verify validation ran successfully (checks logs/stepN_name.log for validation output)

### Validation Requirements By Step

#### Step 1: IRT Calibration with Omnibus Factor

**Analysis Tool:** (determined by rq_tools - likely calibrate_irt or calibrate_grm)
**Validation Tool:** (determined by rq_tools - likely validate_irt_convergence + validate_irt_parameters)

**What Validation Checks:**
- Model convergence (loss function stabilized, parameters within bounds)
- Theta estimates in valid range ([-4, 4] typical, outside suggests calibration issue)
- SE estimates reasonable (0.1 to 1.5, outside suggests unreliable estimates)
- Item parameters valid (a > 0, b unrestricted but typically |b| < 6)
- No NaN values in theta or item parameters
- All 400 composite_IDs present in output

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Item VR-IFR-A01-N-ANS has NaN discrimination")
- Log failure to logs/step01_calibration.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose (common: convergence failure, insufficient data for single-factor model)

---

#### Step 2: Prepare LMM Input Data

**Analysis Tool:** (determined by rq_tools - likely pandas/numpy operations for data transformation)
**Validation Tool:** (determined by rq_tools - likely custom data format validation)

**What Validation Checks:**
- TSVR merge successful (all 400 composite_IDs matched)
- No NaN values in any column after merge
- Time transformations valid (Days >= 0, log_Days_plus1 defined for all)
- Column data types correct (UID/test = object, numeric columns = float64)
- Expected row count (400 observations)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "TSVR merge failed: 387/400 composite_IDs matched")
- Log failure to logs/step02_prepare_data.log
- Quit script immediately
- g_debug invoked to diagnose (common: composite_ID format mismatch, TSVR file path incorrect)

---

#### Step 3: Fit 5 Candidate LMM Models

**Analysis Tool:** (determined by rq_tools - likely fit_lmm_trajectory_tsvr or statsmodels.MixedLM)
**Validation Tool:** (determined by rq_tools - likely validate_lmm_convergence for all 5 models)

**What Validation Checks:**
- All 5 models converged (converged=True for Linear, Quadratic, Logarithmic, LinLog, QuadLog)
- AIC/BIC values finite (not NaN or Inf)
- Log-likelihood values reasonable (negative, not -Inf)
- Parameter counts correct per model specification
- No singular covariance matrix warnings

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Quadratic model failed to converge")
- Log failure to logs/step03_lmm_fitting.log
- Quit script immediately
- g_debug invoked to diagnose (common: singular covariance, insufficient variance in random effects)

---

#### Step 4: Model Selection via AIC

**Analysis Tool:** (determined by rq_tools - likely compare_lmm_models_by_aic or custom AIC calculation)
**Validation Tool:** (determined by rq_tools - likely custom validation for Akaike weights)

**What Validation Checks:**
- Akaike weights sum to 1.0 (within floating-point precision, e.g., 0.999 to 1.001)
- All weights in (0, 1) exclusive (no weight = 0 or 1 exactly)
- delta_AIC values correct (best model = 0, others positive)
- cumulative_weight monotonic increasing (ends at 1.0)
- Best model identified (row 1 after sorting by AIC)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Akaike weights sum to 0.87, expected 1.0")
- Log failure to logs/step04_model_selection.log
- Quit script immediately
- g_debug invoked to diagnose (common: numerical precision error in weight calculation)

---

#### Step 5: Prepare Multi-Panel Plot Data

**Analysis Tool:** (determined by rq_tools - likely pandas aggregation + model prediction functions)
**Validation Tool:** (determined by rq_tools - likely validate_probability_transform for Decision D069 compliance)

**What Validation Checks:**
- Plot data files created (theta scale + probability scale per Decision D069)
- Expected row counts (54 rows: 4 observed + 50 predicted per file)
- Probability values in [0, 1] bounds (transformation valid)
- CI bounds valid (CI_upper > CI_lower for all observed data)
- No NaN in Days column (time grid complete)
- Monotonicity preserved (theta transform to probability preserves ordering)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Probability out of bounds: found 1.03")
- Log failure to logs/step05_prepare_plot_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- g_debug invoked to diagnose (common: transformation error, model prediction extrapolation issue)

---

## Summary

**Total Steps:** 7 (Steps 1-5 completed, Steps 6-7 skipped due to pickle unpickling issues; rq_plots generates visualizations directly)

**Estimated Runtime:**
- Step 1: 30-60 min (IRT calibration, High complexity)
- Step 2: <5 min (data transformation, Low complexity)
- Step 3: 5-10 min (fit 5 LMM models, Medium complexity)
- Step 4: <2 min (AIC calculation, Low complexity)
- Step 5: <5 min (plot data preparation, Low complexity)
- **Total:** 40-82 minutes (dominated by Step 1 IRT calibration)

**Cross-RQ Dependencies:**
- RQ 5.1 Step 0 (requires step00_irt_input.csv and step00_tsvr_mapping.csv)

**Primary Outputs:**
- data/step01_theta_scores.csv (theta estimates with single omnibus "All" factor)
- results/step04_aic_comparison.csv (model comparison table with Akaike weights)
- results/step04_best_model_summary.txt (best functional form identified)
- plots/step05_functional_form_theta_data.csv (theta-scale plot source)
- plots/step05_functional_form_probability_data.csv (probability-scale plot source per Decision D069)

**Validation Coverage:** 100% (all 5 steps have validation requirements embedded)

**Key Decisions Implemented:**
- Decision D070: TSVR as time variable (actual hours, not nominal days)
- Decision D069: Dual-scale trajectory plots (theta + probability)
- Decision D039: Applied (2-pass IRT purification with |b|≤3.0, a≥0.4 thresholds per Step 2. Purification improves measurement quality regardless of dimensionality)

**Scientific Question Answered:**
Which mathematical function (Linear, Quadratic, Logarithmic, Lin+Log, Quad+Log) best approximates episodic forgetting trajectories? AIC-based model selection quantifies relative evidence for competing theoretical predictions (Ebbinghaus logarithmic vs power-law vs two-phase consolidation).

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (approval gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-11-25): Initial plan created by rq_planner agent for RQ 5.7
