# RQ 5.4.6: Schema-Specific Variance Decomposition

**Chapter:** 5
**Type:** Congruence
**Subtype:** Schema-Specific Variance Decomposition
**Full ID:** 5.4.6

---

## Research Question

**Primary Question:**
What proportion of variance in forgetting rate is between-person vs within-person for each congruence level (Common, Congruent, Incongruent)?

**Scope:**
This RQ examines variance decomposition of episodic memory forgetting trajectories across three schema congruence levels. Analysis uses IRT theta scores from RQ 5.4.1 for N=100 participants across 4 test sessions (nominal Days 0, 1, 3, 6). Data structure: 1200 observations (100 participants x 4 tests x 3 congruence levels). Stratified LMM analysis per congruence level to compute Intraclass Correlation Coefficients (ICC) for intercepts and slopes.

**Theoretical Framing:**
Individual differences in forgetting rate (slopes) may reflect stable trait-like characteristics that vary by schema support. If ICCs for slopes exceed 0.40 (substantial threshold), this indicates forgetting rate is a reliable individual difference variable rather than measurement noise. Congruence-specific ICCs may reveal whether schema-supported memory (congruent items) shows more stable individual differences compared to schema-neutral (common) or schema-violating (incongruent) items.

---

## Theoretical Background

**Relevant Theories:**
- **Schema Theory**: Schema-congruent information benefits from existing knowledge structures during encoding and consolidation, potentially creating more stable individual differences in memory performance
- **Individual Differences Framework**: Between-person variance in cognitive abilities reflects stable traits (e.g., working memory capacity, processing speed), while within-person variance reflects measurement error and state fluctuations
- **Trait-State Models**: Memory performance can be decomposed into trait (stable individual differences) and state (occasion-specific) components; schema support may differentially affect trait vs state variance

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
Schema-congruent items may show higher ICC for slopes (more stable individual differences) compared to incongruent items, as schema support creates consistent encoding/retrieval advantages across test sessions. Common items (schema-neutral) may fall between congruent and incongruent in ICC magnitude.

**Literature Gaps:**
Most episodic memory research focuses on mean differences (congruent vs incongruent) rather than individual differences. Variance decomposition by schema congruence has not been systematically examined in longitudinal forgetting paradigms.

---

## Hypothesis

**Primary Hypothesis:**
Substantial between-person variance exists in forgetting rate within each congruence level (ICC for slopes > 0.40), indicating forgetting rate is a stable, trait-like individual difference. Congruence levels may differ in ICC magnitude, reflecting differential stability of schema-based memory.

**Secondary Hypotheses:**
- Congruent items show highest ICC for slopes (most stable individual differences due to schema support)
- Incongruent items show lowest ICC for slopes (more state-dependent, less trait stability)
- Common items fall between congruent and incongruent
- Negative intercept-slope correlations within each congruence level (high baseline performers maintain advantage)

**Theoretical Rationale:**
Schema-congruent memory benefits from consistent encoding and retrieval support across occasions, creating stable individual differences. Schema-incongruent memory is more dependent on effortful processing that varies across occasions, creating larger within-person variance. Common items lack consistent schema bias, producing intermediate stability.

**Expected Effect Pattern:**
- ICC_slope for Congruent > 0.40 (substantial)
- ICC_slope for Common: 0.20-0.40 (moderate)
- ICC_slope for Incongruent < 0.40 (low-to-moderate)
- All intercept-slope correlations negative and significant at Bonferroni alpha = 0.0033 (familywise error rate across 3 congruence levels)

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object naming items from interactive paradigms (IFR/ICR/IRE)

- [x] **Where** (Spatial Location)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Disambiguation: Both pick-up and put-down locations included from interactive paradigms

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order items from interactive paradigms

**Congruence Factor (Primary Dimension):**
- **Common** (`-i1` / `-i2` tags): Schema-neutral items (neither congruent nor incongruent with room context)
- **Congruent** (`-i3` / `-i4` tags): Schema-consistent items (match room affordances and expectations)
- **Incongruent** (`-i5` / `-i6` tags): Schema-violating items (mismatch room context)

**Inclusion Rationale:**
This RQ focuses on schema congruence as the primary factor. All What/Where/When domain items from interactive paradigms are included and categorized by congruence level (Common/Congruent/Incongruent) for variance decomposition analysis.

**Exclusion Rationale:**
- Room Free Recall (RFR) excluded (not item-level)
- Tabletop Cued Recall (TCR) excluded (different paradigm structure)
- Recognition (RRE) excluded from interactive set

---

## Analysis Approach

**Analysis Type:**
Variance decomposition using Linear Mixed Models (LMM) with random slopes, stratified by schema congruence level. Intraclass Correlation Coefficient (ICC) computation for intercepts and slopes.

**High-Level Workflow:**

**Step 1:** Load best-fitting LMM model from RQ 5.4.1 and theta scores for Common, Congruent, and Incongruent congruence levels. Verify model convergence and data structure (1200 observations expected).

**Step 2:** Fit three separate LMMs, one per congruence level (Common, Congruent, Incongruent). Model formula: `theta ~ Time + (Time | UID)` with REML=True for unbiased variance estimates. Extract variance components per congruence level: var_intercept, var_slope, cov_int_slope (covariance between intercept and slope), var_residual.

**Step 3:** Compute three ICC types per congruence level:
- ICC_intercept = var_intercept / (var_intercept + var_residual)
- ICC_slope_simple = var_slope / (var_slope + var_residual)
- ICC_slope_conditional = computed at Day 6 timepoint accounting for intercept-slope covariance

Interpret ICC magnitude: <0.20 = Low, 0.20-0.40 = Moderate, >=0.40 = Substantial between-person variance.

**Step 4:** Extract individual random effects (intercepts and slopes) for all 100 participants, separately for each congruence level. Output: 300 rows (100 participants x 3 congruence levels) with Total_Intercept and Total_Slope per participant per congruence.

**Step 5:** Test intercept-slope correlation within each congruence level using Pearson correlation. Apply Bonferroni correction: alpha = 0.05 / 3 tests = 0.0167 (per congruence level). Report dual p-values per Decision D068 (p_uncorrected and p_bonferroni). Create histogram and Q-Q plot for random slopes per congruence.

**Step 6:** Compare ICC estimates across congruence levels. Rank congruence levels by ICC_slope magnitude. Test if differences are interpretable (descriptive comparison, no formal significance test unless requested).

**Expected Outputs:**
- data/step01_model_metadata_common.yaml
- data/step01_model_metadata_congruent.yaml
- data/step01_model_metadata_incongruent.yaml
- data/step02_variance_components.csv (15 rows: 5 variance components x 3 congruence levels)
- data/step03_icc_estimates.csv (9 rows: 3 ICC types x 3 congruence levels)
- results/step03_icc_summary.txt (interpretive text with magnitude classifications)
- data/step04_random_effects.csv (300 rows: 100 UID x 3 congruence levels, with Total_Intercept and Total_Slope)
- results/step04_random_slopes_descriptives.txt (descriptive statistics per congruence)
- data/step05_intercept_slope_correlation.csv (15 rows: 5 statistics x 3 congruence levels)
- results/step05_correlation_interpretation.txt
- plots/step05_random_slopes_histogram_common.png
- plots/step05_random_slopes_histogram_congruent.png
- plots/step05_random_slopes_histogram_incongruent.png
- plots/step05_random_slopes_qqplot_common.png
- plots/step05_random_slopes_qqplot_congruent.png
- plots/step05_random_slopes_qqplot_incongruent.png
- data/step06_congruence_icc_comparison.csv (3 rows: one per congruence level with all ICC estimates)
- plots/step06_congruence_icc_barplot.png

**Success Criteria:**
- All 3 congruence-stratified models converge (model.converged = True)
- Variance components all positive (var_intercept > 0, var_slope > 0, var_residual > 0)
- ICC estimates in valid range [0, 1] for all 9 estimates (3 ICC types x 3 congruence levels)
- 300 random effects extracted (100 participants x 3 congruence levels), no NaN values
- Intercept-slope correlation tests include both p_uncorrected and p_bonferroni per Decision D068
- PNG histogram and Q-Q plot files > 10KB (non-empty plots)
- Congruence comparison interpretable (ICC rankings make theoretical sense)
- RQ 5.4.1 dependency circuit breaker active: if RQ 5.4.1 data unavailable, QUIT with EXPECTATIONS ERROR

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.4.1 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 5.4.1 (Schema-Specific Trajectories)

**File Paths:**
- results/ch5/5.4.1/data/step03_theta_scores.csv (IRT theta ability estimates per UID x Test x Congruence, 400 rows with 7 columns expected)
- results/ch5/5.4.1/data/step05_lmm_fitted_model.pkl (best-fitting LMM model with Congruence x Time interaction, used for model structure reference)
- results/ch5/5.4.1/data/step04_lmm_input.csv (merged theta + TSVR data in long format, 1200 rows: 100 UID x 4 tests x 3 congruence levels)

**Dependencies:**
RQ 5.4.1 must complete Steps 1-5 successfully:
- Step 0: Extract congruence-specific items (Common/Congruent/Incongruent) from dfData.csv
- Step 1: IRT Pass 1 calibration (3-factor GRM for congruence levels)
- Step 2: Item purification (Decision D039: exclude items with |b| > 3.0 OR a < 0.4)
- Step 3: IRT Pass 2 re-calibration on purified items, producing theta scores per UID x Test x Congruence
- Step 4: Merge theta with TSVR, reshape to long format (1200 observations)
- Step 5: Fit LMMs with Congruence x Time interaction, select best model via AIC

If RQ 5.4.1 status != success in status.yaml, this RQ cannot proceed (circuit breaker: EXPECTATIONS ERROR).

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (inherited from RQ 5.4.1, no additional exclusions)

**Items:**
- N/A (theta scores are already aggregated across items per congruence level)
- Item-level inclusion handled by RQ 5.4.1 purification (Step 2)
- Expected: 50-90 items retained after purification (distributed across Common/Congruent/Incongruent)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4; nominal Days 0, 1, 3, 6)
- [x] Time variable: TSVR (actual hours since encoding, not nominal days)
- Inherited from RQ 5.4.1

**Congruence Levels:**
- [x] Common (schema-neutral, `-i1` / `-i2` tags)
- [x] Congruent (schema-consistent, `-i3` / `-i4` tags)
- [x] Incongruent (schema-violating, `-i5` / `-i6` tags)

---
