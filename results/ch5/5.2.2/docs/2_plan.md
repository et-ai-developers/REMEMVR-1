# Analysis Plan for RQ 5.2: Differential Consolidation Across Memory Domains

**Created by:** rq_planner agent
**Date:** 2025-11-23
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This plan specifies the complete analysis workflow for RQ 5.2, which examines whether sleep-dependent consolidation (Day 0->1) differentially benefits memory domains (What/Where) compared to later decay (Day 1->6). The analysis uses piecewise LMM with a 3-way interaction (Days_within x Segment x Domain) to test whether forgetting slopes differ across consolidation and decay phases by memory domain.

**When Domain Exclusion (RQ 5.2.1 Floor Effect):**
When domain excluded from this analysis due to floor effect discovered in RQ 5.2.1:
- Performance at 6-9% probability throughout study (near 0% floor)
- 20/26 When items (77%) excluded for low discrimination
- Only 6 items retained, limiting reliability
- Per RQ 5.2.1: "Exclude When domain from subsequent RQs until resolved"

**Key Innovation:** Piecewise time structure assigns Day 1 to the Early segment only (no overlap), testing the theoretical prediction that hippocampal-dependent spatial memory (Where) benefits most from sleep consolidation.

**Pipeline:** Data preparation (from RQ 5.1 outputs) -> Filter to What/Where domains -> Piecewise LMM (3-way interaction) -> Slope extraction -> Planned contrasts

**Total Steps:** 6 steps (Step 0: data preparation + Steps 1-5: analysis and plot preparation)

**Estimated Runtime:** Medium (LMM fitting ~10-15 min, contrasts ~5 min)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni) for post-hoc contrasts
- Decision D069: Dual-scale trajectory plots (theta + probability) for piecewise visualization
- Decision D070: TSVR (actual hours) as LMM time variable, not nominal days

**Bonferroni Correction (per rq_stats feedback):**
- 3 planned comparisons: 2 domains x 2 segment-specific slope tests (reduced from 6 due to When exclusion)
- alpha = 0.05/3 = 0.0167

---

## Analysis Plan

### Step 0: Prepare Piecewise LMM Input from RQ 5.1

**Dependencies:** RQ 5.1 must be complete (requires RQ 5.1 theta scores and TSVR data)
**Complexity:** Low (data transformation only, ~2 min)

**Input:**

**File 1:** results/ch5/5.1.1/data/step04_lmm_input.csv
**Format:** CSV, long format (one row per observation = composite_ID x domain)
**Columns:** composite_ID, UID, test, TSVR_hours, domain, theta, se
**Expected Rows:** ~1200 (400 composite_IDs x 3 domains) -> filtered to ~800 (What/Where only)
**Source:** RQ 5.1 Step 4 output (theta scores merged with TSVR)

**Processing:**

1. Load RQ 5.1 LMM input data (long format with theta, domain, TSVR_hours, test)
2. **FILTER: Exclude When domain** (floor effect per RQ 5.2.1) - keep only What/Where
3. Create Segment variable based on test:
   - Early segment: test in {0, 1} (Day 0 encoding, Day 1 immediate retest - consolidation window)
   - Late segment: test in {3, 6} (Day 3, Day 6 - decay-dominated phase)
   - CRITICAL: Day 1 (test=1) assigned to Early segment ONLY (no overlap)
4. Create Days_within variable (time since segment start):
   - For Early segment: Days_within = TSVR_hours / 24 (ranges ~0-1 days)
   - For Late segment: Days_within = (TSVR_hours - TSVR_at_Day1) / 24 (ranges ~0-5 days)
   - Interpretation: Days elapsed within each segment, centered at segment start
5. Verify segment assignments:
   - Each observation belongs to exactly one segment
   - test=0,1 -> Early; test=3,6 -> Late
6. Create interaction-ready factors:
   - domain: Treatment coding with What as reference
   - Segment: Treatment coding with Early as reference
7. Save piecewise LMM input

**Output:**

**File:** data/step00_piecewise_lmm_input.csv
**Format:** CSV, long format (one row per observation)
**Columns:**
- `composite_ID` (string): UID + "_" + test
- `UID` (string): Participant identifier
- `test` (int): Nominal test session (0, 1, 3, 6)
- `TSVR_hours` (float): Actual time since encoding in hours
- `domain` (string): Memory domain (what, where) - **When excluded**
- `theta` (float): IRT ability estimate for this domain
- `se` (float): Standard error of theta estimate
- `Segment` (string): "Early" or "Late"
- `Days_within` (float): Days elapsed within segment (centered at segment start)
**Expected Rows:** ~800 (400 composite_IDs x 2 domains, What/Where only)
**Expected Columns:** 9

**Validation Requirement:**
Validation tools MUST be used after data preparation tool execution. Specific validation tools will be determined by rq_tools based on segment assignment and data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_piecewise_lmm_input.csv: ~800 rows x 9 columns (What/Where only, When excluded)

*Value Ranges:*
- TSVR_hours in [0, 200] (reasonable range for 6-day study)
- theta in [-3.0, 3.0] (bounded by IRT ability scale)
- se in [0.1, 1.5] (reasonable standard errors)
- test in {0, 1, 3, 6} (nominal test sessions)
- domain in {what, where} (categorical) - **When excluded due to floor effect**
- Segment in {Early, Late} (categorical)
- Days_within in [0, 6] for Late segment, [0, 2] for Early segment

*Data Quality:*
- All composite_IDs from RQ 5.1 present for What/Where domains (When filtered out)
- Each composite_ID appears exactly 2 times (once per retained domain: What, Where)
- test 0,1 -> Segment=Early (100%); test 3,6 -> Segment=Late (100%)
- No NaN in Segment or Days_within columns
- ~100 unique UIDs present

*Log Validation:*
- Required pattern: "Loaded X rows from RQ 5.1"
- Required pattern: "Segment assignment: Early=X, Late=Y observations"
- Required pattern: "Days_within computed: Early range [A, B], Late range [C, D]"
- Forbidden patterns: "ERROR", "RQ 5.1 file not found", "Missing TSVR"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step00_prepare_piecewise_input.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause

---

### Step 1: Fit Piecewise LMM with 3-Way Interaction

**Dependencies:** Step 0 (requires data/step00_piecewise_lmm_input.csv)
**Complexity:** Medium-High (~10-15 min for model fitting)

**Input:**

**File:** data/step00_piecewise_lmm_input.csv
**Format:** CSV, long format
**Columns:** composite_ID, UID, test, TSVR_hours, domain, theta, se, Segment, Days_within

**Processing:**

1. Load piecewise LMM input data
2. Set treatment coding:
   - domain: What as reference (coefficients for Where and When vs What)
   - Segment: Early as reference (coefficients for Late vs Early)
3. Fit piecewise LMM with 3-way interaction:
   - Formula: theta ~ Days_within * Segment * domain + (Days_within | UID)
   - Fixed effects: Main effects + all 2-way interactions + 3-way interaction
   - Random effects: Random intercepts and slopes by UID
   - Fit with REML=False for model comparison
4. Key effects to extract:
   - Days_within: Forgetting slope in Early segment for What domain (baseline)
   - Days_within:Segment[T.Late]: Slope difference (Late vs Early) for What domain
   - Days_within:domain[T.Where/When]: Domain slope differences in Early segment
   - Days_within:Segment[T.Late]:domain[T.Where/When]: 3-way interaction (key hypothesis test)
5. Save model summary and fitted model object

**Output:**

**File 1:** results/step01_piecewise_lmm_summary.txt
**Format:** Text file
**Content:** Full model summary including:
- Fixed effects table (coefficients, SE, z, p-values)
- Random effects variance components
- Model fit statistics (AIC, BIC, log-likelihood)

**File 2:** data/step01_piecewise_lmm_model.pkl
**Format:** Python pickle (statsmodels fitted model object)
**Purpose:** Store fitted model for slope extraction and contrasts

**Validation Requirement:**
Validation tools MUST be used after LMM fitting tool execution. Specific validation tools will be determined by rq_tools based on LMM convergence and residual diagnostic requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step01_piecewise_lmm_summary.txt: exists with content (>1KB)
- data/step01_piecewise_lmm_model.pkl: exists (binary pickle file)

*Value Ranges:*
- AIC value reasonable (typically 500-3000 for this data size)
- Fixed effect coefficients in reasonable range (|coef| < 5 typically)
- p-values in [0, 1]
- z-statistics in [-10, 10]

*Data Quality:*
- Model converged successfully
- All 7 fixed effect terms present (intercept + 6 interaction terms)
- Random effects variance > 0 (model estimated random slopes)
- No singular fit warning (random effects not at boundary)

*Log Validation:*
- Required pattern: "Model converged" or "Optimization terminated successfully"
- Required pattern: "Fixed effects: 7 terms estimated"
- Forbidden patterns: "ERROR", "CONVERGENCE FAILED", "Singular fit"
- Acceptable warnings: "Matrix near singular" (may occur but model valid)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step01_fit_piecewise_lmm.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose (common causes: multicollinearity, insufficient data per cell)

---

### Step 2: Extract Segment-by-Domain Slopes

**Dependencies:** Step 1 (requires data/step01_piecewise_lmm_model.pkl)
**Complexity:** Low (~2 min)

**Input:**

**File:** data/step01_piecewise_lmm_model.pkl
**Format:** Python pickle (statsmodels fitted model object)

**Processing:**

1. Load fitted piecewise LMM model
2. Extract fixed effects coefficients
3. Compute segment-specific slopes for each domain (What/Where only - When excluded):
   - **Early segment slopes (from coefficients directly):**
     - What (Early): beta[Days_within]
     - Where (Early): beta[Days_within] + beta[Days_within:domain[T.Where]]
   - **Late segment slopes (add Segment interaction):**
     - What (Late): beta[Days_within] + beta[Days_within:Segment[T.Late]]
     - Where (Late): beta[Days_within] + beta[Days_within:Segment[T.Late]] + beta[Days_within:domain[T.Where]] + beta[Days_within:Segment[T.Late]:domain[T.Where]]
4. Compute standard errors via delta method or linear combination SE
5. Compute 95% confidence intervals for each slope
6. Save slope summary table

**Output:**

**File:** results/step02_segment_domain_slopes.csv
**Format:** CSV (one row per segment x domain combination)
**Columns:**
- `segment` (string): Early or Late
- `domain` (string): what, where (When excluded due to floor effect)
- `slope` (float): Estimated forgetting slope (theta units per day)
- `se` (float): Standard error of slope estimate
- `CI_lower` (float): Lower 95% CI bound
- `CI_upper` (float): Upper 95% CI bound
- `z` (float): Z-statistic (slope / se)
- `p_value` (float): p-value for slope != 0
**Expected Rows:** 4 (2 segments x 2 domains)

**Validation Requirement:**
Validation tools MUST be used after slope extraction tool execution. Specific validation tools will be determined by rq_tools based on statistical validity requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step02_segment_domain_slopes.csv: 4 rows x 8 columns (What/Where only)

*Value Ranges:*
- slope in [-1, 0] typically (negative = forgetting, decline over time)
- se in [0.01, 0.5] (reasonable slope standard error)
- CI_lower < slope < CI_upper (valid interval structure)
- p_value in [0, 1]
- z in [-10, 10]

*Data Quality:*
- Exactly 4 rows (2 segments x 2 domains - When excluded)
- All segment-domain combinations present
- segment in {Early, Late}; domain in {what, where}
- No NaN in any column
- Early slopes should generally be steeper (more negative) or similar to Late slopes

*Log Validation:*
- Required pattern: "Extracted 4 segment-domain slopes"
- Required pattern: "SE computed via linear combination"
- Forbidden patterns: "ERROR", "Slope extraction failed", "NaN slope"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step02_extract_slopes.log
- Quit script immediately (do NOT proceed to Step 3)
- g_debug invoked to diagnose

---

### Step 3: Planned Contrasts with Bonferroni Correction (Decision D068)

**Dependencies:** Step 1 (requires data/step01_piecewise_lmm_model.pkl), Step 2 (for context)
**Complexity:** Low-Medium (~5 min)

**Input:**

**File 1:** data/step01_piecewise_lmm_model.pkl
**Format:** Python pickle (statsmodels fitted model object)

**File 2:** results/step02_segment_domain_slopes.csv
**Format:** CSV (slope estimates for reference)

**Processing:**

1. Load fitted piecewise LMM model
2. Define 3 planned contrasts (reduced from 6 due to When exclusion):

   **Within-segment domain comparisons (consolidation benefit tests):**
   - C1: Where vs What slope in Early segment (tests spatial consolidation advantage)
   - C2: Where vs What slope in Late segment (decay phase comparison)

   **Cross-segment comparisons (slope change tests):**
   - C3: Where (Late-Early) vs What (Late-Early) - does consolidation benefit differ?

3. Compute each contrast using linear combinations of fixed effects
4. Apply Bonferroni correction: alpha = 0.05/3 = 0.0167
5. Report BOTH uncorrected AND Bonferroni-corrected p-values (Decision D068)
6. Compute effect sizes (Cohen's d) for domain differences
7. Save contrast results

**Output:**

**File 1:** results/step03_planned_contrasts.csv
**Format:** CSV (one row per contrast)
**Columns:**
- `contrast` (string): Contrast description (e.g., "Where-What_Early")
- `estimate` (float): Coefficient difference (slope difference)
- `se` (float): Standard error of estimate
- `z` (float): Z-statistic
- `p_uncorrected` (float): Raw p-value
- `p_bonferroni` (float): Bonferroni-corrected p-value (Decision D068)
- `significant_uncorrected` (bool): p < 0.05
- `significant_bonferroni` (bool): p < 0.0167
**Expected Rows:** 3 (3 planned contrasts - When excluded)

**File 2:** results/step03_effect_sizes.csv
**Format:** CSV
**Columns:**
- `comparison` (string): Effect description
- `cohens_d` (float): Standardized effect size
- `ci_lower` (float): 95% CI lower bound
- `ci_upper` (float): 95% CI upper bound
- `interpretation` (string): Small/Medium/Large per Cohen's guidelines
**Expected Rows:** 3 (effect sizes for 3 contrasts)

**Validation Requirement:**
Validation tools MUST be used after contrast computation tool execution. Specific validation tools will be determined by rq_tools based on statistical validity and effect size computation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step03_planned_contrasts.csv: 3 rows x 8 columns (When excluded)
- results/step03_effect_sizes.csv: 3 rows x 5 columns (When excluded)

*Value Ranges:*
- p_uncorrected in [0, 1] (valid probability)
- p_bonferroni in [0, 1] (valid probability, >= p_uncorrected or capped at 1)
- z in [-10, 10] (reasonable z-statistic range)
- cohens_d in [-3, 3] (typical effect size range, |d| > 2 is very large)

*Data Quality:*
- Exactly 3 contrasts present (reduced from 6 due to When exclusion)
- p_bonferroni = min(1.0, p_uncorrected * 3) for each row
- Both uncorrected and Bonferroni p-values present (Decision D068)
- Effect size CI contains point estimate (ci_lower <= cohens_d <= ci_upper)

*Log Validation:*
- Required pattern: "Computed 3 planned contrasts"
- Required pattern: "Bonferroni correction applied (alpha = 0.0167)"
- Forbidden patterns: "ERROR", "Invalid contrast", "Effect size NaN"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step03_compute_contrasts.log
- Quit script immediately (do NOT proceed to Step 4)
- g_debug invoked to diagnose

---

### Step 4: Compute Consolidation Benefit Indices

**Dependencies:** Step 2 (requires results/step02_segment_domain_slopes.csv)
**Complexity:** Low (~2 min)

**Input:**

**File:** results/step02_segment_domain_slopes.csv
**Format:** CSV (segment-domain slopes)
**Columns:** segment, domain, slope, se, CI_lower, CI_upper, z, p_value

**Processing:**

1. Load segment-domain slopes
2. Compute consolidation benefit index per domain:
   - Consolidation benefit = Early slope - Late slope
   - Positive value: Less forgetting in Early (consolidation protected memory)
   - Negative value: More forgetting in Early (no consolidation benefit)
3. Interpret: Larger positive values indicate greater consolidation benefit
4. Rank domains by consolidation benefit
5. Generate summary interpretation:
   - Which domain benefited most from consolidation?
   - Does this support hippocampal replay hypothesis (Where > What)?
6. Save consolidation benefit summary

**Output:**

**File:** results/step04_consolidation_benefit.csv
**Format:** CSV (one row per domain)
**Columns:**
- `domain` (string): what, where (When excluded due to floor effect)
- `early_slope` (float): Forgetting slope in Early segment
- `late_slope` (float): Forgetting slope in Late segment
- `consolidation_benefit` (float): Early - Late (positive = protected)
- `benefit_se` (float): Standard error of benefit estimate
- `benefit_CI_lower` (float): Lower 95% CI
- `benefit_CI_upper` (float): Upper 95% CI
- `rank` (int): Rank by consolidation benefit (1 = most protected)
**Expected Rows:** 2 (What/Where only, When excluded)

**Validation Requirement:**
Validation tools MUST be used after consolidation benefit computation tool execution. Specific validation tools will be determined by rq_tools based on statistical validity requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step04_consolidation_benefit.csv: 2 rows x 8 columns (What/Where only)

*Value Ranges:*
- early_slope in [-1, 0] typically (forgetting = negative)
- late_slope in [-1, 0] typically
- consolidation_benefit in [-0.5, 0.5] (difference of slopes)
- rank in {1, 2} (unique ranks for 2 domains)

*Data Quality:*
- Exactly 2 rows (What/Where only, When excluded)
- All retained domains present (what, where)
- Ranks are unique (1, 2)
- benefit_CI_lower < consolidation_benefit < benefit_CI_upper

*Log Validation:*
- Required pattern: "Computed consolidation benefit for 2 domains"
- Required pattern: "Domain ranking by consolidation benefit: X > Y"
- Forbidden patterns: "ERROR", "Benefit computation failed"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/step04_compute_consolidation_benefit.log
- Quit script immediately (do NOT proceed to Step 5)
- g_debug invoked to diagnose

---

### Step 5: Prepare Piecewise Trajectory Plot Data (Decision D069)

**CRITICAL NOTE:** Plot data preparation IS an analysis step. It:
- Gets executed in Step 14 CODE EXECUTION LOOP (g_code -> bash -> rq_inspect)
- MUST have validation requirements (same as any analysis step)
- Outputs to plots/*.csv (not data/*.csv) but still validated by rq_inspect
- Created by g_code during analysis (NOT by rq_plots during visualization)

**Dependencies:** Step 0 (requires data/step00_piecewise_lmm_input.csv), Step 1 (model predictions)
**Complexity:** Low (data aggregation, ~2 min)

**Purpose:** Aggregate analysis outputs for piecewise trajectory visualization showing slope change at consolidation boundary (~24 hours).

**Plot Description:** Piecewise forgetting trajectory over time with 3 lines (What/Where/When domains) showing theta decline with distinct slopes for Early (0-24h) and Late (24h-144h) segments. Visual break at ~24 hours highlights consolidation boundary.

**Required Data Sources:**
- data/step00_piecewise_lmm_input.csv (observed data with segments)
- data/step01_piecewise_lmm_model.pkl (for model predictions per segment)
- results/ch5/5.1.1/data/step03_item_parameters.csv (for theta-to-probability conversion)

**Processing (Theta Scale Plot Data):**

1. Load piecewise LMM input data (long format with theta, domain, TSVR_hours, Segment)
2. Group by domain, Segment, and test
3. Compute observed statistics per group:
   - mean_theta = mean(theta) per domain x test
   - CI_lower = mean - 1.96 * (sd / sqrt(n))
   - CI_upper = mean + 1.96 * (sd / sqrt(n))
4. Add representative TSVR_hours per test (median or typical value)
5. Generate model predictions from fitted piecewise LMM:
   - Smooth trajectory within each segment
   - Discontinuity allowed at segment boundary
6. Combine observed means + model predictions
7. Save theta-scale plot data

**Processing (Probability Scale Plot Data - Decision D069):**

1. Load theta-scale plot data (from previous sub-step)
2. Load item parameters from RQ 5.1 (mean discrimination a, mean difficulty b per domain)
3. Apply reverse logit transformation: P = 1 / (1 + exp(-(a * (theta - b))))
4. Use domain-specific average a and b for transformation
5. Transform CI bounds similarly
6. Save probability-scale plot data

**Output (Plot Source CSVs):**

**File 1:** plots/step05_piecewise_theta_data.csv
**Format:** CSV (plot-ready data for theta scale)
**Columns:**
- `time` (float): TSVR_hours (representative time per test)
- `test` (int): Nominal test session (0, 1, 3, 6)
- `domain` (string): Memory domain (what, where) - **When excluded**
- `Segment` (string): Early or Late
- `mean_theta` (float): Observed mean theta per domain x test
- `CI_lower` (float): Lower 95% CI bound (theta scale)
- `CI_upper` (float): Upper 95% CI bound (theta scale)
- `predicted_theta` (float): Piecewise LMM model prediction at this time point
- `n_obs` (int): Number of observations in group
**Expected Rows:** 8 (2 domains x 4 time points)

**File 2:** plots/step05_piecewise_probability_data.csv
**Format:** CSV (plot-ready data for probability scale - Decision D069)
**Columns:**
- `time` (float): TSVR_hours
- `test` (int): Nominal test session
- `domain` (string): Memory domain (what, where) - **When excluded**
- `Segment` (string): Early or Late
- `mean_probability` (float): Mean theta transformed to probability scale
- `CI_lower` (float): Lower 95% CI bound (probability scale)
- `CI_upper` (float): Upper 95% CI bound (probability scale)
- `predicted_probability` (float): Model prediction on probability scale
- `n_obs` (int): Number of observations
**Expected Rows:** 8 (2 domains x 4 time points)

**Validation Requirement:**
Validation tools MUST be used after plot data preparation tool execution. Specific validation tools will be determined by rq_tools based on plot data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- plots/step05_piecewise_theta_data.csv: 8 rows x 9 columns (What/Where only)
- plots/step05_piecewise_probability_data.csv: 8 rows x 9 columns (What/Where only)

*Value Ranges:*
- time in [0, 200] hours (reasonable TSVR range)
- test in {0, 1, 3, 6} (nominal sessions)
- domain in {what, where} (categorical) - **When excluded**
- Segment in {Early, Late} (categorical)
- mean_theta in [-3, 3] (IRT ability scale)
- mean_probability in [0, 1] (probability scale)
- CI_upper > CI_lower for all rows (valid intervals)
- n_obs >= 80 per group (100 participants, some missing acceptable)

*Data Quality:*
- Exactly 8 rows per file (2 domains x 4 tests - When excluded)
- Both retained domains present (what, where)
- All 4 tests present (0, 1, 3, 6)
- Segment assignment correct: test 0,1 -> Early; test 3,6 -> Late
- No NaN values in any column
- Domain x test combinations unique (no duplicates)

*Log Validation:*
- Required pattern: "Plot data preparation complete: 8 rows created"
- Required pattern: "Domains represented: what, where"
- Required pattern: "Segment boundaries: Early (tests 0,1), Late (tests 3,6)"
- Required pattern: "Dual-scale conversion applied (Decision D069)"
- Forbidden patterns: "ERROR", "NaN values detected", "Missing domain"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 8 rows, found 6")
- Log failure to logs/step05_prepare_piecewise_plot_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- g_debug invoked to diagnose root cause

**Plotting Function (rq_plots will call):** Piecewise trajectory plot with confidence bands
- rq_plots agent maps this description to specific tools/plots.py function
- Plot reads plots/step05_piecewise_theta_data.csv and plots/step05_piecewise_probability_data.csv
- No data aggregation in rq_plots (visualization only per Option B)
- Decision D069: Generate BOTH theta-scale and probability-scale plots
- Special feature: Visual indicator at segment boundary (~24 hours)

---

## Expected Data Formats

### Step-to-Step Transformations

**RQ 5.1 -> Step 0:** Import LMM input from RQ 5.1 -> Add Segment and Days_within columns
**Step 0 -> Step 1:** Piecewise LMM input -> Fit 3-way interaction model
**Step 1 -> Step 2:** Fitted model -> Extract 6 segment-domain slopes
**Step 1,2 -> Step 3:** Fitted model + slopes -> Compute 6 planned contrasts
**Step 2 -> Step 4:** Segment slopes -> Compute consolidation benefit indices
**Step 0,1 -> Step 5:** Input data + model -> Aggregate for piecewise trajectory plot

### Column Naming Conventions (from names.md + RQ 5.2 additions)

| Variable | Pattern | Example | Notes |
|----------|---------|---------|-------|
| Participant ID | composite_ID | P001_0 | UID + "_" + test |
| Raw UID | UID | P001 | Participant identifier |
| Test session | test | 0, 1, 3, 6 | Nominal days |
| Time variable | TSVR_hours | 24.5 | Decision D070 - actual hours |
| Domain factor | domain | what, where, when | Categorical |
| Theta estimate | theta | 0.5 | Ability estimate (single column, domain as factor) |
| Standard error | se | 0.2 | SE of theta |
| Segment | Segment | Early, Late | Consolidation vs decay phase |
| Days within segment | Days_within | 0.5 | Time since segment start (days) |
| CI bounds | CI_lower, CI_upper | -0.3, 0.5 | 95% confidence interval |

### Data Type Constraints

| Column | Type | Nullable | Valid Range |
|--------|------|----------|-------------|
| composite_ID | string | No | Format: UID_test |
| UID | string | No | Format: P### |
| test | int | No | {0, 1, 3, 6} |
| TSVR_hours | float | No | [0, 200] |
| domain | string | No | {what, where, when} |
| theta | float | No | [-4, 4] typical |
| se | float | No | [0.05, 3.0] |
| Segment | string | No | {Early, Late} |
| Days_within | float | No | [0, 6] |

---

## Cross-RQ Dependencies

**Dependency Type: DERIVED Data from Other RQs (Dependencies Exist)**

**This RQ requires outputs from:**

**RQ 5.1** (Domain-Specific Forgetting Trajectories)
- **File:** results/ch5/5.1.1/data/step04_lmm_input.csv
  - Used in: Step 0 (base data for piecewise transformation)
  - Rationale: RQ 5.1 produces theta scores merged with TSVR in long format. RQ 5.2 adds segment structure.
  - Required columns: composite_ID, UID, test, TSVR_hours, domain, theta, se

- **File:** results/ch5/5.1.1/data/step03_item_parameters.csv
  - Used in: Step 5 (theta-to-probability transformation for Decision D069)
  - Rationale: Need domain-specific item parameters for probability scale conversion.
  - Required columns: item_name, dimension, a, b

**Execution Order Constraint:**
1. RQ 5.1 must complete successfully first (provides theta scores with TSVR)
2. RQ 5.2 executes second (uses RQ 5.1 outputs)

**Data Source Boundaries:**
- **DERIVED data:** Theta scores from RQ 5.1 IRT calibration
- **NO RAW data extraction:** RQ 5.2 does not read master.xlsx directly
- **Scope:** RQ 5.2 adds piecewise structure but does not re-estimate theta

**Validation (Step 0):**
- Check results/ch5/5.1.1/data/step04_lmm_input.csv exists
- Check results/ch5/5.1.1/data/step03_item_parameters.csv exists
- If either file missing -> QUIT with EXPECTATIONS ERROR -> user must execute RQ 5.1 first

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

### Validation Requirements By Step

| Step | Analysis Type | Key Validation Criteria |
|------|---------------|-------------------------|
| 0 | Data Preparation | RQ 5.1 files exist, Segment assignment correct, Days_within computed |
| 1 | Piecewise LMM | Model converged, 7 fixed effect terms present, random effects valid |
| 2 | Slope Extraction | 6 slopes computed, all segment-domain combinations present |
| 3 | Planned Contrasts | 6 contrasts computed, dual p-values present (D068), effect sizes valid |
| 4 | Consolidation Benefit | 3 domains computed, ranks assigned, benefit indices valid |
| 5 | Plot Data Prep | 12 rows exactly, all domains/tests/segments present, no NaN |

---

## Summary

**Total Steps:** 6 (Step 0 preparation + Steps 1-5 analysis)
**Estimated Runtime:** Medium (~30-45 min total, primarily LMM fitting)
**Cross-RQ Dependencies:** RQ 5.1 (theta scores and item parameters)
**Primary Outputs:**
- Piecewise LMM model: data/step01_piecewise_lmm_model.pkl
- Segment-domain slopes: results/step02_segment_domain_slopes.csv
- Planned contrasts: results/step03_planned_contrasts.csv
- Effect sizes: results/step03_effect_sizes.csv
- Consolidation benefit: results/step04_consolidation_benefit.csv
- Plot data: plots/step05_piecewise_theta_data.csv, plots/step05_piecewise_probability_data.csv
**Validation Coverage:** 100% (all 6 steps have validation requirements)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-11-23): Initial plan created by rq_planner agent
