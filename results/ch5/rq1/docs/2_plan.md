# Analysis Plan: RQ 5.1 - Domain-Specific Forgetting Trajectories (What/Where/When)

**Research Question:** 5.1
**Created:** 2025-11-20
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This analysis examines domain-specific forgetting trajectories for three episodic memory components (What, Where, When) using IRT-derived ability estimates across four test sessions spanning 6 days. The analysis tests whether familiarity-based object identity (What) shows greater resilience to forgetting than recollection-dependent spatial (Where) and temporal (When) information, consistent with dual-process theory predictions.

**Pipeline:** IRT  LMM (complete 2-pass purification pipeline with trajectory modeling)
**Steps:** 8 total analysis steps (Step 0: extraction + Steps 1-7: analysis)
**Estimated Runtime:** High (Step 1 and Step 3 IRT calibrations ~30-60 min each, others <5 min each)

**Key Decisions Applied:**
- Decision D039: 2-pass IRT purification (mandatory for all IRT analyses)
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni for post-hoc contrasts)
- Decision D069: Dual-scale trajectory plots (theta-scale + probability-scale)
- Decision D070: TSVR as time variable (actual hours since encoding, not nominal days)

---

## Analysis Plan

### Step 0: Data Extraction

**Dependencies:** None (first step)
**Complexity:** Low (<5 min, data extraction only)

**Purpose:** Extract VR item response data from master.xlsx via data/cache/dfData.csv for all three memory domains across all 4 test sessions.

**Input:**
- File: data/cache/dfData.csv (preprocessed from master.xlsx)
- Columns Required: UID, TEST, TSVR, TQ_* (all VR task items)
- Expected Dimensions: ~100 participants x 4 tests = ~400 rows

**Tag Patterns:**
- **What domain:** TQ_*-N-* (matches all items with -N- domain code for object identity)
- **Where domain:** TQ_*-L-*, TQ_*-U-*, TQ_*-D-* (matches all location items: general location, pick-up, put-down)
- **When domain:** TQ_*-O-* (matches all temporal order items)

**Processing:**
1. Load dfData.csv (columns: UID, TEST, TSVR, TQ_*)
2. Dichotomize TQ_* values: <1  0 (incorrect), e1  1 (correct) per 1_concept.md Step 2
3. Reshape to long format using standard pandas operations with:
 - composite = ["UID", "TEST"] (creates composite_ID = UID_test)
 - time = "TSVR" (preserve time variable for later merge)
 - items = ["TQ_*"] (all VR items)
 - factors = {what: ["*-N-*"], where: ["*-L-*", "*-U-*", "*-D-*"], when: ["*-O-*"]}
4. Save TSVR mapping separately for Step 4 merge

**Output:**
- File 1: data/step00_irt_input.csv
 - Format: Wide (composite_ID x item columns)
 - Dimensions: ~400 rows (100 participants x 4 tests) x ~103 cols (composite_ID + ~102 items)
 - Columns: composite_ID (string, format: UID_test), item codes as columns (TQ_*-domain-*), values 0/1
 - Data Types: composite_ID (object), items (int64 with 0/1 values)

- File 2: data/step00_tsvr_mapping.csv
 - Format: Long (one row per composite_ID)
 - Dimensions: ~400 rows x 3 cols
 - Columns: composite_ID (string), TEST (object, T1/T2/T3/T4), TSVR_hours (float64, actual hours since VR)
 - Purpose: Merge with theta scores in Step 4 per Decision D070

**Validation Requirement:**
Validation tools MUST be used after data extraction tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_irt_input.csv: ~400 rows x ~103 columns (composite_ID + ~102 items)
- data/step00_tsvr_mapping.csv: ~400 rows x 3 columns (composite_ID, TEST, TSVR_hours)
- Data types: composite_ID (object), TEST (object), TSVR_hours (float64), item columns (int64)

*Value Ranges:*
- Item responses {0, 1} (dichotomized, no partial credit)
- TSVR_hours [0, 200] hours (0 = encoding session T1, up to ~8 days for delayed participants)
- TEST {T1, T2, T3, T4} (categorical)

*Data Quality:*
- All 100 participants present across all 4 tests (no data loss, 400 total observations)
- Missing item responses acceptable (<30% per item, handled by IRT missing_mask)
- No NaN in composite_ID or TSVR_hours (critical for merging)
- No duplicate composite_IDs (each UID_test unique)
- Item columns: What (~51 items), Where (~51 items: L+U+D combined), When (~102 items temporal)

*Log Validation:*
- Required: "Data extraction complete: 400 observations x ~102 items"
- Required: "TSVR mapping saved: 400 observations"
- Required: "Dichotomization applied: TQ_ values converted to 0/1"
- Forbidden: "ERROR", "EXCEPTION", "Missing UID", "Missing TEST"
- Acceptable warnings: "Missing item responses for <30% of items" (IRT handles missing)

**Expected Behavior:**
Successfully extract all VR item responses in wide format for IRT calibration + TSVR time variable for later LMM merge.

---

### Step 1: IRT Calibration Pass 1 (All Items)

**Dependencies:** Step 0 (requires extracted IRT input data)
**Complexity:** High (30-60 min, GRM model calibration with 3 correlated factors)

**Purpose:** Calibrate IRT model on ALL items (before purification) to identify psychometrically problematic items for exclusion in Step 2.

**Input:**
- File: data/step00_irt_input.csv
- Format: Wide (composite_ID x item columns)
- Dimensions: ~400 rows x ~103 cols
- Required Columns: composite_ID, all TQ_* item columns

**Processing:**
1. Load IRT input data
2. Configure IRT model:
 - Model: Graded Response Model (GRM) - handles dichotomous items (2 categories: 0, 1)
 - Factors: 3 correlated factors (What, Where, When) per 1_concept.md
 - Factor groups: {what: [items with -N-], where: [items with -L-/-U-/-D-], when: [items with -O-]}
 - Device: CPU (or GPU if available)
3. Fit GRM model using deepirtools calibrate_irt function
4. Extract item parameters (discrimination a, difficulty b per item)
5. Extract theta scores (diagnostic only, not used in final analysis)
6. Save Pass 1 outputs to logs/ folder (not data/ - these are diagnostic, not final)

**Output:**
- File 1: logs/step01_pass1_item_params.csv
 - Dimensions: ~102 rows (items) x 4 cols
 - Columns: item_name (object), dimension (object: What/Where/When), a (float64, discrimination), b (float64, difficulty)
 - Purpose: Input for Step 2 purification

- File 2: logs/step01_pass1_theta.csv
 - Dimensions: ~400 rows x 7 cols
 - Columns: composite_ID (object), theta_what (float64), theta_where (float64), theta_when (float64), se_what (float64), se_where (float64), se_when (float64)
 - Purpose: Diagnostic only, verify model convergence

**Validation Requirement:**
Validation tools MUST be used after IRT Pass 1 calibration tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- logs/step01_pass1_item_params.csv: ~102 rows x 4 columns (item_name, dimension, a, b)
- logs/step01_pass1_theta.csv: ~400 rows x 7 columns (composite_ID, theta_*, se_*)
- Data types: item_name (object), dimension (object), a/b/theta/se (float64)

*Value Ranges:*
- Discrimination a > 0 (negative impossible, model constraint)
- Difficulty b unrestricted (temporal items can have |b| > 3.0 per 1_concept.md)
- Theta [-4, 4] typical range (outside = possible but rare, not error)
- SE [0.1, 2.0] (above 2.0 = unreliable estimates, below 0.1 = suspicious)

*Data Quality:*
- All ~102 items present (no items dropped due to non-convergence)
- All 400 observations present (all composite_IDs from Step 0)
- No NaN in item parameters (indicates estimation failure)
- No NaN in theta scores (IRT handles missing item responses internally)
- Q3 statistic <0.2 for >90% of item pairs within each dimension (local independence check per 1_concept.md)
- Eigenvalue ratio >3.0 for each dimension (unidimensionality check per 1_concept.md)

*Log Validation:*
- Required: "Model converged: True"
- Required: "VALIDATION - PASS: IRT convergence"
- Required: "VALIDATION - PASS: Q3 local independence"
- Required: "VALIDATION - PASS: Eigenvalue ratio unidimensionality"
- Required: "Fit indices: RMSEA <0.08, CFI >0.90" (relaxed thresholds for N=400 per 1_concept.md)
- Forbidden: "ERROR", "CONVERGENCE FAILED", "NaN parameters detected"
- Acceptable warnings: "Q3 >0.2 for <10% of item pairs" (minor local dependence expected)

**Expected Behavior:**
IRT model converges, produces item parameters for all items. Some items expected to have extreme difficulty (|b| > 3.0) or low discrimination (a < 0.4), which will be identified for purification in Step 2.

---

### Step 2: Item Purification (Decision D039)

**Dependencies:** Step 1 (requires Pass 1 item parameters)
**Complexity:** Low (<5 min, filtering based on thresholds)

**Purpose:** Identify psychometrically problematic items using Decision D039 thresholds (|b| > 3.0 OR a < 0.4) and create purified item list for Pass 2.

**Input:**
- File: logs/step01_pass1_item_params.csv
- Dimensions: ~102 rows x 4 cols
- Columns: item_name, dimension, a (discrimination), b (difficulty)

**Processing:**
1. Load Pass 1 item parameters
2. Apply Decision D039 purification thresholds:
 - Retain items where: (|b| d 3.0) AND (a e 0.4)
 - Exclude items where: (|b| > 3.0) OR (a < 0.4)
3. Expected retention: ~40-50% of items (temporal items particularly difficult per 1_concept.md)
4. Generate purification report listing excluded items with reasons
5. Ensure e10 items retained per dimension (minimum for reliable IRT estimation)

**Output:**
- File 1: data/step02_purified_items.csv
 - Dimensions: ~40-50 rows x 2 cols
 - Columns: item_name (object), dimension (object: What/Where/When)
 - Purpose: Filter for Pass 2 IRT input

- File 2: logs/step02_purification_report.txt
 - Format: Text file with exclusion summary
 - Content: Lists excluded items, reasons (extreme difficulty vs. low discrimination), retention rate per dimension

**Validation Requirement:**
Validation tools MUST be used after item purification tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_purified_items.csv: ~40-50 rows x 2 columns (item_name, dimension)
- logs/step02_purification_report.txt: Text file exists, non-empty
- Data types: item_name (object), dimension (object)

*Value Ranges:*
- Retention rate [30%, 70%] per dimension (40-50% expected per 1_concept.md, <30% = too aggressive, >70% = thresholds not applied)
- Minimum 10 items per dimension (lower = unreliable IRT)

*Data Quality:*
- All 3 dimensions represented (What, Where, When all have retained items)
- No NaN values in purified item list
- No duplicate item_names (each item unique)
- Item names match those in Step 0 IRT input (exact string match required for filtering)

*Log Validation:*
- Required: "Purification complete: ~40-50 items retained from ~102 items"
- Required: "Items per dimension: What ~15, Where ~15, When ~15" (approximate)
- Required: "Exclusion reasons: {N} extreme difficulty, {M} low discrimination"
- Required: "Minimum threshold met: e10 items per dimension"
- Forbidden: "ERROR", "No items retained", "Dimension eliminated"
- Acceptable warnings: "Retention rate <50% for temporal domain" (expected per 1_concept.md)

**Expected Behavior:**
~40-50% item retention, all 3 dimensions preserved with e10 items each. Temporal domain expected to show lower retention due to high difficulty.

---

### Step 3: IRT Calibration Pass 2 (Purified Items Only)

**Dependencies:** Steps 0 and 2 (requires original IRT input + purified item list)
**Complexity:** High (30-60 min, GRM model calibration on subset of items)

**Purpose:** Re-calibrate IRT model using ONLY purified items to obtain final theta scores for LMM analysis. This is the definitive IRT calibration per Decision D039.

**Input:**
- File 1: data/step00_irt_input.csv (original wide-format IRT data)
- File 2: data/step02_purified_items.csv (items to retain)
- Dimensions: ~400 rows x ~40-50 purified item columns (after filtering)

**Processing:**
1. Load original IRT input data
2. Load purified item list
3. Filter IRT input to ONLY include purified items (column subset)
4. Configure IRT model (same settings as Pass 1: GRM, 3 correlated factors)
5. Fit GRM model using deepirtools calibrate_irt function
6. Extract FINAL item parameters (for reporting, validation)
7. Extract FINAL theta scores (for LMM analysis in Steps 4-6)
8. Expect improved fit indices vs. Pass 1 (RMSEA lower, CFI higher due to item purification)

**Output:**
- File 1: data/step03_item_parameters.csv
 - Dimensions: ~40-50 rows x 4 cols
 - Columns: item_name (object), dimension (object), a (float64), b (float64)
 - Purpose: Final item parameters for reporting

- File 2: data/step03_theta_scores.csv
 - Dimensions: ~400 rows x 7 cols
 - Columns: composite_ID (object), theta_what (float64), theta_where (float64), theta_when (float64), se_what (float64), se_where (float64), se_when (float64)
 - Purpose: PRIMARY OUTPUT - theta scores for LMM analysis

**Validation Requirement:**
Validation tools MUST be used after IRT Pass 2 calibration tool execution. Specific validation tools same as Pass 1 (IRT convergence, fit indices, local independence) but expect improved fit.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_item_parameters.csv: ~40-50 rows x 4 columns
- data/step03_theta_scores.csv: ~400 rows x 7 columns
- Data types: Same as Pass 1

*Value Ranges:*
- Item parameters: Same ranges as Pass 1 BUT all items now meet purification thresholds (|b| d 3.0, a e 0.4)
- Theta scores: Same ranges as Pass 1 ( [-4, 4] typical)
- SE: Same ranges as Pass 1 ( [0.1, 2.0])

*Data Quality:*
- All ~40-50 purified items present (matches Step 2 output)
- All 400 observations present (no participant loss)
- No NaN in item parameters or theta scores
- Improved fit vs. Pass 1: RMSEA_pass2 < RMSEA_pass1, CFI_pass2 > CFI_pass1
- Theta reliability: Correlation between theta estimates and observed scores >0.7 per dimension

*Log Validation:*
- Required: "Model converged: True"
- Required: "VALIDATION - PASS: IRT convergence"
- Required: "VALIDATION - PASS: Improved fit vs Pass 1 (RMSEA <0, CFI >0)"
- Required: "Fit indices: RMSEA <0.08, CFI >0.90"
- Required: "Theta reliability >0.7 for all dimensions"
- Forbidden: "ERROR", "CONVERGENCE FAILED", "Worse fit than Pass 1"

**Expected Behavior:**
IRT model converges with better fit than Pass 1. Final theta scores ready for LMM trajectory analysis.

---

### Step 4: Merge Theta Scores with TSVR (Decision D070)

**Dependencies:** Steps 0 and 3 (requires TSVR mapping + Pass 2 theta scores)
**Complexity:** Low (<5 min, data merging and reshaping)

**Purpose:** Merge theta scores with TSVR time variable (actual hours since encoding) and reshape to long format for LMM input per Decision D070.

**Input:**
- File 1: data/step03_theta_scores.csv (~400 rows x 7 cols: composite_ID, theta_*, se_*)
- File 2: data/step00_tsvr_mapping.csv (~400 rows x 3 cols: composite_ID, TEST, TSVR_hours)

**Processing:**
1. Load theta scores (wide format)
2. Load TSVR mapping
3. Merge on composite_ID (left join, keep all theta scores, add TSVR_hours)
4. Parse composite_ID to extract UID and TEST (format: UID_test  UID="...", TEST="T#")
5. Reshape wide  long format:
 - One row per observation (participant x test x domain combination)
 - Create domain factor column (What, Where, When)
 - Create theta column (ability estimate for that domain)
 - Create SE column (standard error for that domain)
6. Convert TSVR_hours to TSVR_days (divide by 24) for interpretability
7. Save long-format LMM input

**Output:**
- File: data/step04_lmm_input.csv
 - Dimensions: ~1200 rows (400 observations x 3 domains) x 6 cols
 - Columns: UID (object), test (object: T1/T2/T3/T4), domain (object: What/Where/When), theta (float64), SE (float64), TSVR_days (float64)
 - Format: Long (one row per observation x domain)

**Expected Data Transformation:**

*Input (wide):*
```
composite_ID theta_what theta_where theta_when TSVR_hours
P001_T1 0.52 0.34 0.68 0.0
P001_T2 0.45 0.28 0.55 24.3
```

*Output (long):*
```
UID test domain theta SE TSVR_days
P001 T1 What 0.52 0.18 0.00
P001 T1 Where 0.34 0.22 0.00
P001 T1 When 0.68 0.25 0.00
P001 T2 What 0.45 0.19 1.01
P001 T2 Where 0.28 0.23 1.01
P001 T2 When 0.55 0.26 1.01
```

**Validation Requirement:**
Validation tools MUST be used after TSVR merge and reshape tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_lmm_input.csv: ~1200 rows x 6 columns (UID, test, domain, theta, SE, TSVR_days)
- Data types: UID (object), test (object), domain (object), theta/SE/TSVR_days (float64)

*Value Ranges:*
- Theta [-4, 4] (same as IRT output)
- SE [0.1, 2.0] (same as IRT output)
- TSVR_days [0, 8] days (0 = encoding T1, up to ~8 days for delayed T4 sessions)
- test {T1, T2, T3, T4}
- domain {What, Where, When}

*Data Quality:*
- All 400 composite_IDs from theta scores matched with TSVR (no missing TSVR values)
- Expected N: 1200 rows exactly (400 observations x 3 domains)
- No NaN in any column (all merges successful)
- No duplicate (UID x test x domain) combinations
- TSVR_days monotonically increasing within each UID (T1 < T2 < T3 < T4)

*Log Validation:*
- Required: "TSVR merge complete: All 400 composite_IDs matched"
- Required: "Reshape complete: 1200 rows (400 observations x 3 domains)"
- Required: "TSVR_days range: [0.0, ~8.0] days"
- Required: "No missing TSVR values"
- Forbidden: "ERROR", "Merge failed", "Missing TSVR for composite_ID"
- Acceptable warnings: "TSVR_days >7 for <5% of T4 observations" (scheduling variance expected)

**Expected Behavior:**
Successfully merge theta scores with actual time variable (TSVR) and reshape to long format ready for LMM trajectory fitting.

---

### Step 5: LMM Trajectory Fitting (5 Candidate Models)

**Dependencies:** Step 4 (requires LMM input with theta + TSVR_days)
**Complexity:** Medium (10-20 min, fit 5 models + compare via AIC)

**Purpose:** Fit 5 candidate LMM models with different time structures (linear, quadratic, logarithmic, hybrids) and select best via AIC/AICc comparison per 1_concept.md Step 7.

**Input:**
- File: data/step04_lmm_input.csv
- Dimensions: ~1200 rows x 6 cols
- Columns: UID, test, domain, theta, SE, TSVR_days

**Processing:**
1. Load LMM input data
2. Configure 5 candidate models using Domain x Time interactions with Treatment coding (What as reference):
 - **Model 1 - Linear:** `theta ~ TSVR_days * C(domain, Treatment('What')) + (1 + TSVR_days | UID)`
 - **Model 2 - Quadratic:** `theta ~ (TSVR_days + I(TSVR_days**2)) * C(domain, Treatment('What')) + (1 + TSVR_days | UID)`
 - **Model 3 - Logarithmic:** `theta ~ np.log(TSVR_days + 1) * C(domain, Treatment('What')) + (1 + TSVR_days | UID)`
 - **Model 4 - Lin+Log:** `theta ~ (TSVR_days + np.log(TSVR_days + 1)) * C(domain, Treatment('What')) + (1 + TSVR_days | UID)`
 - **Model 5 - Quad+Log:** `theta ~ (TSVR_days + I(TSVR_days**2) + np.log(TSVR_days + 1)) * C(domain, Treatment('What')) + (1 + TSVR_days | UID)`
3. Fit all 5 models using statsmodels MixedLM with REML=False (for AIC comparison)
4. Apply convergence strategy per 1_concept.md: If random slopes fail (singular fit), compare random intercept-only via LRT. Only retain random slopes if LRT p<0.05 AND converges without warnings.
5. Compare models via AIC and AICc (small-sample corrected)
6. Select best model (lowest AIC; if AIC and AICc disagree, favor AICc per 1_concept.md)
7. Extract fixed effects, random effects, fit indices from best model

**Output:**
- File 1: logs/step05_model_comparison.csv
 - Dimensions: 5 rows (models) x 6 cols
 - Columns: model_name (object), formula (object), AIC (float64), AICc (float64), delta_AIC (float64), AIC_weight (float64)
 - Purpose: Model selection comparison table

- File 2: results/step05_lmm_model_summary.txt
 - Format: Text file with best model summary
 - Content: Fixed effects table (², SE, z, p), random effects variances, fit indices (AIC, BIC, log-likelihood)

- File 3: data/step05_best_model_predictions.csv
 - Dimensions: ~1200 rows x 3 cols
 - Columns: composite_ID (object), domain (object), predicted_theta (float64)
 - Purpose: Model predictions for plotting in Step 7

**Validation Requirement:**
Validation tools MUST be used after LMM fitting tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- logs/step05_model_comparison.csv: 5 rows x 6 columns
- results/step05_lmm_model_summary.txt: Text file exists, non-empty
- data/step05_best_model_predictions.csv: ~1200 rows x 3 columns
- Data types: AIC/AICc/delta_AIC/AIC_weight (float64), model_name/formula (object)

*Value Ranges:*
- AIC [reasonable range - model-dependent, no universal bound]
- AIC_weight [0, 1] (sum to 1 across 5 models)
- delta_AIC e 0 (best model has delta_AIC = 0)
- predicted_theta [-4, 4] (same range as observed theta)

*Data Quality:*
- All 5 models attempted (some may fail to converge - acceptable if e2 converge)
- Best model converged without singular fit warnings (or random intercept-only if slopes don't converge)
- AIC comparison table sorted by AIC (best model first)
- Best model shows significant Domain x Time interaction (p < 0.05) per hypothesis

*Log Validation:*
- Required: "LMM fitting complete: {N} of 5 models converged"
- Required: "Best model selected: {model_name} (AIC={X.X}, AICc={Y.Y})"
- Required: "VALIDATION - PASS: Residual normality (Shapiro-Wilk p>0.05)"
- Required: "VALIDATION - PASS: Homoscedasticity (visual inspection)"
- Required: "VALIDATION - PASS: No autocorrelation (ACF lag-1 <0.1)"
- Required: "VALIDATION - PASS: No influential outliers (Cook's D <0.04)"
- Forbidden: "ERROR", "All models failed", "Convergence failed for best model"
- Acceptable warnings: "Singular fit for random slopes - using random intercept-only" (if LRT justifies simplification)

**Expected Behavior:**
Best model selected via AIC, Domain x Time interaction significant (supports hypothesis of differential forgetting), LMM assumptions met.

---

### Step 6: Post-Hoc Contrasts and Effect Sizes (Decision D068)

**Dependencies:** Step 5 (requires best fitted LMM model)
**Complexity:** Low (<5 min, extract contrasts and compute effect sizes)

**Purpose:** Test pairwise domain differences in forgetting slopes and compute effect sizes, reporting BOTH uncorrected and Bonferroni-corrected p-values per Decision D068.

**Input:**
- Best LMM model from Step 5 (in memory or loaded from .pkl file)
- Model summary with fixed effects (Domain x TSVR_days interaction terms)

**Processing:**
1. Extract Domain x TSVR_days interaction coefficients from best model:
 - Where x TSVR_days coefficient (forgetting slope difference: Where vs. What)
 - When x TSVR_days coefficient (forgetting slope difference: When vs. What)
2. Compute pairwise contrasts:
 - **Contrast 1:** Where - What (test if Where forgetting slope ` What forgetting slope)
 - **Contrast 2:** When - What (test if When forgetting slope ` What forgetting slope)
 - **Contrast 3:** When - Where (test if When forgetting slope ` Where forgetting slope)
3. Report p-values TWO ways per Decision D068:
 - **Uncorrected:** +/- = 0.05 (exploratory threshold)
 - **Bonferroni-corrected:** +/-_corrected = 0.05 / 3 = 0.0167 (3 pairwise comparisons)
4. Compute effect sizes:
 - **Cohen's d:** Standardized mean difference for pairwise comparisons at each timepoint
 - **Partial *²:** Variance explained by Domain x Time interaction

**Output:**
- File 1: results/step06_post_hoc_contrasts.csv
 - Dimensions: 3 rows (contrasts) x 7 cols
 - Columns: comparison (object: "Where-What", "When-What", "When-Where"), beta (float64), se (float64), z (float64), p_uncorrected (float64), p_bonferroni (float64), sig_uncorrected (object: "*" or "ns"), sig_bonferroni (object: "*" or "ns")

- File 2: results/step06_effect_sizes.csv
 - Dimensions: Variable (depends on effect size type) x 4 cols
 - Columns: effect (object: contrast name or interaction term), value (float64: Cohen's d or *²), interpretation (object: "small", "medium", "large"), threshold (object: Cohen's d e0.2, *² e0.01)

**Validation Requirement:**
Validation tools MUST be used after post-hoc contrast tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step06_post_hoc_contrasts.csv: 3 rows x 7 columns
- results/step06_effect_sizes.csv: Variable rows x 4 columns
- Data types: beta/se/z/p (float64), comparison/sig/interpretation (object)

*Value Ranges:*
- p_uncorrected [0, 1]
- p_bonferroni [0, 1], p_bonferroni e p_uncorrected (Bonferroni more conservative)
- z unrestricted (test statistic)
- beta unrestricted (slope difference)
- Cohen's d typically [-2, 2] (>5 = probably wrong)
- Partial *² [0, 1]

*Data Quality:*
- Exactly 3 contrasts (all pairwise comparisons: Where-What, When-What, When-Where)
- No NaN in any column
- sig_uncorrected correctly marks significance: "*" if p_uncorrected <0.05, "ns" otherwise
- sig_bonferroni correctly marks significance: "*" if p_bonferroni <0.0167, "ns" otherwise
- Expected pattern: At least one contrast significant (supports hypothesis of domain differences)

*Log Validation:*
- Required: "Post-hoc contrasts complete: 3 pairwise comparisons"
- Required: "Bonferroni correction applied: +/-_corrected = 0.0167"
- Required: "Effect sizes computed: Cohen's d, partial *²"
- Forbidden: "ERROR", "EXCEPTION", "Invalid p-value"

**Expected Behavior:**
Pairwise contrasts reveal domain differences in forgetting slopes. What expected to show resilience (slowest forgetting), When fastest forgetting per hypothesis.

---

### Step 7: Prepare Trajectory Plot Data (Option B Architecture - Decision D069)

**Dependencies:** Steps 4 and 5 (requires LMM input + best model predictions)
**Complexity:** Low (<5 min, data aggregation for plotting)

**Purpose:** Aggregate LMM results into plot source CSVs for dual-scale trajectory visualization (theta + probability scales) per Decision D069. This is plot DATA PREPARATION (executed during analysis), NOT plotting (rq_plots handles visualization later).

**Plot Description:** Trajectory over time with confidence bands showing theta/probability decline across memory domains (What/Where/When).

**Required Data Sources:**
- data/step04_lmm_input.csv (observed theta scores)
- data/step05_best_model_predictions.csv (model-predicted theta)
- data/step00_tsvr_mapping.csv (time variable)

**Processing:**

**For Theta-Scale Plot Source CSV:**
1. Load LMM input (observed theta + TSVR_days)
2. Load best model predictions (predicted theta)
3. Group by domain + test, compute:
 - mean_theta (observed mean per domain per timepoint)
 - CI_lower, CI_upper (95% confidence intervals using SE from LMM input)
 - predicted_theta (from best model)
4. Merge with TSVR_days (actual time variable)
5. Create columns: time (TSVR_days), theta (mean observed), CI_lower, CI_upper, domain, predicted_theta
6. Save to plots/step07_trajectory_theta_data.csv

**For Probability-Scale Plot Source CSV (Decision D069):**
1. Load theta-scale plot data
2. Convert theta to probability using IRT response function:
 - `probability = 1 / (1 + exp(-(discrimination * (theta - difficulty))))`
 - Use average discrimination (a=1.0) and difficulty (b=0.0) for transformation
3. Apply same transformation to CI_lower, CI_upper, predicted_theta
4. Create columns: time (TSVR_days), probability (mean observed), CI_lower, CI_upper, domain, predicted_probability
5. Save to plots/step07_trajectory_probability_data.csv

**Output:**

- File 1: plots/step07_trajectory_theta_data.csv
 - Dimensions: 12 rows (3 domains x 4 timepoints) x 6 cols
 - Columns: time (float64: TSVR_days), theta (float64: observed mean), CI_lower (float64), CI_upper (float64), domain (object: What/Where/When), predicted_theta (float64)
 - Purpose: Theta-scale trajectory plot source (for psychometricians)

- File 2: plots/step07_trajectory_probability_data.csv
 - Dimensions: 12 rows (3 domains x 4 timepoints) x 6 cols
 - Columns: time (float64: TSVR_days), probability (float64: observed mean), CI_lower (float64), CI_upper (float64), domain (object: What/Where/When), predicted_probability (float64)
 - Purpose: Probability-scale trajectory plot source (for general audience per Decision D069)

**Validation Requirement:**
Validation tools MUST be used after plot data preparation tool execution. This is an ANALYSIS STEP (creates plot source CSVs during Step 14 CODE EXECUTION LOOP), validated by rq_inspect like any other analysis step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- plots/step07_trajectory_theta_data.csv: 12 rows x 6 columns
- plots/step07_trajectory_probability_data.csv: 12 rows x 6 columns
- Data types: time/theta/probability/CI (float64), domain (object)

*Value Ranges:*
- Theta-scale: time [0, 8] days, theta [-3, 3], CI_lower/CI_upper [-3, 3]
- Probability-scale: time [0, 8] days, probability [0, 1], CI_lower/CI_upper [0, 1]
- domain {What, Where, When}

*Data Quality:*
- Exactly 12 rows (3 domains x 4 timepoints: T1/T2/T3/T4 nominal days 0, 1, 3, 6)
- No NaN values (all cells valid)
- No duplicate (domain x time) combinations
- CI_upper > CI_lower for all rows (confidence intervals valid)
- Probability transformation valid: all values [0, 1]

*Log Validation:*
- Required: "Plot data preparation complete: 12 rows created (theta-scale)"
- Required: "Plot data preparation complete: 12 rows created (probability-scale)"
- Required: "All domains represented: What, Where, When"
- Required: "VALIDATION - PASS: Probability transformation (all [0, 1])"
- Forbidden: "ERROR", "NaN values detected", "Missing domain", "Invalid probability (outside [0,1])"

**Expected Behavior:**
Plot source CSVs created with aggregated data ready for visualization by rq_plots agent (Phase 2). Dual-scale requirement satisfied per Decision D069.

**Plotting Function (for rq_plots agent):**
- Plot type: Trajectory plot with confidence bands
- Theta-scale: tools/plots.py function (trajectory plot)
- Probability-scale: tools/plots.py function (trajectory plot with probability Y-axis)
- rq_plots reads plots/step07_*_data.csv and calls plotting functions (NO data aggregation in rq_plots per Option B)

---

## Expected Data Formats

### IRT Data Format (Step 0 Output)

**Wide Format (composite_ID x items):**
```
composite_ID TQ_RVR-IFR-N-i1CM-*-ANS TQ_RVR-IFR-U-i1CM-*-ANS ...
P001_T1 1 0 ...
P001_T2 1 1 ...
P001_T3 0 1 ...
P001_T4 1 0 ...
```

- Rows: composite_ID (format: UID_test)
- Columns: Item codes (TQ_* tags from master.xlsx)
- Values: 0/1 (dichotomized accuracy)
- Missing: NaN (IRT handles missing internally via missing_mask)

### TSVR Mapping Format (Step 0 Output, Step 4 Input)

```
composite_ID TEST TSVR_hours
P001_T1 T1 0.0
P001_T2 T2 24.3
P001_T3 T3 73.1
P001_T4 T4 146.8
```

- composite_ID: Matches IRT data composite_ID
- TEST: Categorical (T1, T2, T3, T4)
- TSVR_hours: Continuous (actual hours since VR encoding)

### Theta Scores Format (Step 3 Output, Step 4 Input)

```
composite_ID theta_what theta_where theta_when se_what se_where se_when
P001_T1 0.52 0.34 0.68 0.18 0.22 0.25
P001_T2 0.45 0.28 0.55 0.19 0.23 0.26
```

- composite_ID: Same as IRT input
- theta_*: Ability estimates per dimension (What, Where, When)
- se_*: Standard errors per dimension

### LMM Input Format (Step 4 Output, Step 5 Input)

**Long Format (one row per observation x domain):**
```
UID test domain theta SE TSVR_days
P001 T1 What 0.52 0.18 0.00
P001 T1 Where 0.34 0.22 0.00
P001 T1 When 0.68 0.25 0.00
P001 T2 What 0.45 0.19 1.01
P001 T2 Where 0.28 0.23 1.01
P001 T2 When 0.55 0.26 1.01
```

- UID: Participant identifier (parsed from composite_ID)
- test: Test session (T1, T2, T3, T4)
- domain: Factor (What, Where, When)
- theta: Ability estimate for that domain
- SE: Standard error for that domain
- TSVR_days: Actual time since encoding (continuous, NOT nominal days 0/1/3/6)

### Plot Source CSV Format (Step 7 Output, rq_plots Input)

**Theta-Scale:**
```
time theta CI_lower CI_upper domain predicted_theta
0.00 0.52 0.34 0.70 What 0.54
0.00 0.34 0.12 0.56 Where 0.36
0.00 0.68 0.43 0.93 When 0.66
1.01 0.45 0.26 0.64 What 0.48
1.01 0.28 0.05 0.51 Where 0.29
1.01 0.55 0.29 0.81 When 0.52
...
```

**Probability-Scale (same structure, different scale):**
```
time probability CI_lower CI_upper domain predicted_probability
0.00 0.63 0.58 0.68 What 0.64
0.00 0.58 0.53 0.64 Where 0.59
0.00 0.66 0.61 0.71 When 0.65
1.01 0.61 0.56 0.66 What 0.62
1.01 0.57 0.51 0.63 Where 0.57
1.01 0.63 0.57 0.69 When 0.61
...
```

---

## Cross-RQ Dependencies

**Dependency Type:** RAW Data Only (No Dependencies)

**This RQ uses:** Only master.xlsx via data/cache/dfData.csv (project-level data source)

**No dependencies on other RQs:** Can be executed independently

**Execution order:** Flexible (any order within chapter)

**Data Sources:**
- data/cache/dfData.csv (preprocessed from master.xlsx Sheet: Data) - participant VR item responses
- master.xlsx tags: TQ_* columns with domain codes -N-, -L-, -U-, -D-, -O-
- TSVR extracted from dfData.csv TEST and TSVR columns

**Note:** All data extraction uses direct loading from dfData.csv (no tools/data.py functions needed per 1_concept.md). No intermediate outputs from other RQs required.

---

## Validation Requirements

**CRITICAL MANDATE:**

Every analysis step in this plan MUST use validation tools after analysis tool execution.

This is not optional. This is the core architectural principle preventing cascading failures observed in v3.0 (where analysis errors propagated undetected through 5+ downstream steps before discovery).

**Exact Specification Requirement:**

> "Validation tools MUST be used after analysis tool execution"

**Implementation:**
- rq_tools (Step 11 workflow) will read tools_inventory.md validation tools section
- rq_tools will specify BOTH analysis tool + validation tool per step in 3_tools.yaml
- rq_analysis (Step 12 workflow) will embed validation tool call AFTER analysis tool call in 4_analysis.yaml
- g_code (Step 14 workflow) will generate stepN_*.py scripts with validation function calls
- bash execution (Step 14 workflow) will run analysis  validation  error on validation failure

**Downstream Agent Requirements:**
- **rq_tools:** MUST specify validation tool for EVERY analysis step (no exceptions)
- **rq_analysis:** MUST embed validation tool call for EVERY analysis step (no exceptions)
- **g_code:** MUST generate code with validation function calls (no exceptions)
- **rq_inspect:** MUST verify validation ran successfully (checks logs/stepN_*.log for validation output)

### Validation Requirements By Step

#### Step 0: Extract VR Data
**Analysis Tool:** TBD (determined by rq_tools)
**Validation Tool:** TBD (determined by rq_tools)

**What Validation Checks:**
- Output files exist (step00_irt_input.csv, step00_tsvr_mapping.csv)
- Expected column count (~103 for IRT input: composite_ID + ~102 items)
- Expected row count (~400: 100 participants x 4 tests)
- Item response values {0, 1} (dichotomized correctly)
- TSVR_hours [0, 200] (reasonable time range)
- composite_ID format correct (UID_test pattern)
- No unexpected NaN patterns (missing item responses <30% per item acceptable)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected ~102 items, found 73")
- Log failure to logs/step00_extract.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked by master to diagnose root cause

---

#### Step 1: IRT Calibration Pass 1
**Analysis Tool:** TBD (determined by rq_tools)
**Validation Tool:** TBD (determined by rq_tools)

**What Validation Checks:**
- Model convergence achieved (log-likelihood improved, not NaN)
- Item parameters in valid ranges (a > 0, b unrestricted but finite)
- No NaN parameters (indicates estimation failure)
- Q3 statistic <0.2 for >90% of item pairs within each dimension (local independence)
- Eigenvalue ratio >3.0 for each dimension (unidimensionality)
- Fit indices: RMSEA <0.08, CFI >0.90 (relaxed for N=400 per 1_concept.md)
- Expected row count (logs/step01_pass1_item_params.csv: ~102 items)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Q3 >0.2 for 30% of item pairs - local dependence violation")
- Log failure to logs/step01_irt_pass1.log
- Quit script immediately
- g_debug invoked to diagnose (common causes: insufficient data, model misspecification, local dependence)

---

#### Step 2: Item Purification
**Analysis Tool:** TBD (determined by rq_tools)
**Validation Tool:** TBD (determined by rq_tools)

**What Validation Checks:**
- Output file exists (step02_purified_items.csv)
- Retention rate [30%, 70%] per dimension (~40-50% expected)
- Minimum 10 items per dimension (lower = unreliable IRT)
- All 3 dimensions represented (What, Where, When all have retained items)
- Item names match Step 0 IRT input (exact string match)
- No NaN values in purified item list

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "When domain: only 5 items retained (minimum 10 required)")
- Log failure to logs/step02_purify.log
- Quit script immediately
- g_debug invoked to diagnose (common causes: overly aggressive thresholds, dimension-specific difficulty)

---

#### Step 3: IRT Calibration Pass 2
**Analysis Tool:** TBD (determined by rq_tools)
**Validation Tool:** TBD (determined by rq_tools)

**What Validation Checks:**
- Same as Step 1 PLUS:
- Improved fit vs. Pass 1 (RMSEA <0, CFI >0)
- Theta reliability >0.7 for all dimensions (correlation between theta and observed scores)
- All purified items from Step 2 present in item_parameters.csv

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Pass 2 fit WORSE than Pass 1: RMSEA_pass2=0.10 > RMSEA_pass1=0.08")
- Log failure to logs/step03_irt_pass2.log
- Quit script immediately
- g_debug invoked to diagnose (common causes: purification removed too many items, remaining items problematic)

---

#### Step 4: TSVR Merge and Reshape
**Analysis Tool:** TBD (determined by rq_tools)
**Validation Tool:** TBD (determined by rq_tools)

**What Validation Checks:**
- All composite_IDs from theta scores matched with TSVR (no missing TSVR values)
- Expected N: 1200 rows exactly (400 observations x 3 domains)
- No NaN in any column
- No duplicate (UID x test x domain) combinations
- TSVR_days monotonically increasing within each UID (T1 < T2 < T3 < T4)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Missing TSVR for 12 composite_IDs")
- Log failure to logs/step04_merge.log
- Quit script immediately
- g_debug invoked to diagnose (common causes: TSVR extraction incomplete, merge key mismatch)

---

#### Step 5: LMM Fitting
**Analysis Tool:** TBD (determined by rq_tools)
**Validation Tool:** TBD (determined by rq_tools)

**What Validation Checks:**
- At least 2 of 5 candidate models converged
- Best model converged without singular fit warnings (or random intercept-only if slopes don't converge per convergence strategy)
- Residual normality (Shapiro-Wilk p>0.05)
- Homoscedasticity (visual inspection of residual vs fitted plot)
- No autocorrelation (ACF lag-1 <0.1)
- No influential outliers (Cook's D <0.04 = 4/N)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Best model failed convergence")
- Log failure to logs/step05_lmm.log
- Quit script immediately
- g_debug invoked to diagnose (common causes: random slopes overparameterized, multicollinearity, outliers)

---

#### Step 6: Post-Hoc Contrasts
**Analysis Tool:** TBD (determined by rq_tools)
**Validation Tool:** TBD (determined by rq_tools)

**What Validation Checks:**
- Exactly 3 contrasts (Where-What, When-What, When-Where)
- No NaN in any column
- p-values [0, 1]
- p_bonferroni e p_uncorrected (Bonferroni more conservative)
- Significance markers correct ("*" if p<threshold, "ns" otherwise)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "p_bonferroni < p_uncorrected for contrast When-What")
- Log failure to logs/step06_contrasts.log
- Quit script immediately
- g_debug invoked to diagnose (common causes: contrast computation error, incorrect Bonferroni factor)

---

#### Step 7: Plot Data Preparation
**Analysis Tool:** TBD (determined by rq_tools)
**Validation Tool:** TBD (determined by rq_tools)

**What Validation Checks:**
- Both output files exist (step07_trajectory_theta_data.csv, step07_trajectory_probability_data.csv)
- Exactly 12 rows each (3 domains x 4 timepoints)
- No NaN values (all cells valid)
- CI_upper > CI_lower for all rows
- Probability values [0, 1] (transformation valid)
- All domains represented (What, Where, When)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Probability transformation invalid: value 1.2 outside [0,1]")
- Log failure to logs/step07_plot_prep.log
- Quit script immediately (do NOT proceed to rq_plots)
- g_debug invoked to diagnose (common causes: IRT transformation parameters incorrect, data aggregation error)

---

## Summary

**Total Steps:** 8 (Step 0: extraction + Steps 1-7: analysis)
**Estimated Runtime:** High (~90-120 min total: 2 IRT calibrations ~30-60 min each, others <5 min each)
**Cross-RQ Dependencies:** None (RAW data only from master.xlsx via dfData.csv)
**Primary Outputs:**
- data/step03_theta_scores.csv (IRT ability estimates for 3 domains)
- results/step05_lmm_model_summary.txt (best LMM model for trajectory)
- results/step06_post_hoc_contrasts.csv (domain differences in forgetting slopes)
- results/step06_effect_sizes.csv (Cohen's d, partial *²)
- plots/step07_trajectory_theta_data.csv (theta-scale plot source)
- plots/step07_trajectory_probability_data.csv (probability-scale plot source)

**Validation Coverage:** 100% (all 8 steps have validation requirements with 4-layer substance criteria)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate per v4.X workflow)
2. Workflow continues to Step 11: rq_tools reads this plan  creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml  creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml  generates step00_*.py through step07_*.py scripts

---

**Version History:**
- v1.0 (2025-11-20): Initial plan created by rq_planner agent for RQ 5.1
