# RQ 5.4.5: Purified CTT Effects

**Chapter:** 5
**Type:** Congruence
**Subtype:** Purified CTT Effects
**Full ID:** 5.4.5

---

## Research Question

**Primary Question:**
If we compute CTT scores using only IRT-retained items (post-purification), do conclusions differ from full-item CTT for congruence?

**Scope:**
This RQ examines measurement convergence between IRT theta scores and CTT mean scores computed using purified (IRT-retained) items versus full (all items) for three schema congruence levels (Common, Congruent, Incongruent). Sample: N=100 participants x 4 tests = 400 observations. CTT scores computed separately for Full (~50 items total) and Purified (~38 retained items after IRT purification).

**Theoretical Framing:**
Methodological validation study testing whether IRT-based item purification (removing items with poor discrimination or extreme difficulty) yields CTT scores that converge more strongly with IRT theta estimates. Demonstrates robustness of congruence findings to measurement approach and item selection.

---

## Theoretical Background

**Relevant Theories:**
- **Schema Theory** (Bartlett, 1932): Memory for schema-congruent information is enhanced compared to schema-incongruent information. Item purification may differentially affect congruence categories if poor items cluster within specific congruence levels.
- **Classical Test Theory vs IRT Convergence**: IRT purification removes items with low discrimination (a < 0.4) or extreme difficulty (|b| > 3.0). If these items contribute primarily noise rather than signal, purified CTT scores should show higher correlation with IRT theta compared to full CTT.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
IRT purification removes items that contribute measurement error (low discrimination) or psychometric irregularities (extreme difficulty). Purified CTT scores should correlate more strongly with IRT theta (delta_r ~ +0.02) compared to full CTT, demonstrating that purification removes noise. Effect should be consistent across all three congruence levels (Common, Congruent, Incongruent).

**Literature Gaps:**
[To be identified by rq_scholar]

---

## Hypothesis

**Primary Hypothesis:**
Purified CTT will show higher correlation with IRT theta (delta_r ~ +0.02) compared to full CTT, demonstrating item purification removes measurement noise.

**Secondary Hypotheses:**
Purified CTT yields better LMM fit (lower AIC) compared to full CTT when modeling congruence-specific forgetting trajectories.

**Theoretical Rationale:**
IRT purification (Decision D039) removes items with discrimination a < 0.4 (poor item-theta correlation) or difficulty |b| > 3.0 (extreme parameters indicating psychometric irregularities). These items contribute measurement error that inflates CTT score variance without improving construct validity. Removing them should strengthen CTT-IRT convergence. Hypothesis is consistent across congruence levels because purification criteria are psychometric (not content-based).

**Expected Effect Pattern:**
Correlation increase: Full-IRT r ~ 0.70-0.85, Purified-IRT r ~ 0.72-0.87, delta_r ~ +0.02 (small but consistent improvement). Steiger's z-test for dependent correlations significant at Bonferroni alpha = 0.0167 (3 congruence levels). AIC improvement: Purified CTT LMM shows lower AIC than Full CTT LMM by > 2 points (Burnham & Anderson threshold for meaningful difference).

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object identity / naming

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location, legacy)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Disambiguation: All Where tags included (general location plus pick-up and put-down)

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order / sequence

**Inclusion Rationale:**
This RQ uses data from RQ 5.4.1 which includes all three memory domains (What/Where/When) within interactive paradigms (IFR, ICR, IRE). All domains represented in congruence analysis because schema congruence (common/congruent/incongruent) is operationalized through item tags (i1/i2, i3/i4, i5/i6) that cross-cut all domain types.

**Exclusion Rationale:**
No domain exclusions. Room-based paradigms (RFR, TCR, RRE) excluded at RQ 5.4.1 level (inherited exclusion).

---

## Analysis Approach

**Analysis Type:**
Classical Test Theory (CTT) score computation with correlation analysis and Linear Mixed Models (LMM) for trajectory comparison

**High-Level Workflow:**

**Step 0:** Load RQ 5.4.1 outputs (purified items, IRT theta scores, TSVR mapping) and verify dependency
**Step 1:** Map retained vs removed items by congruence category (Common, Congruent, Incongruent)
**Step 2:** Compute Full CTT mean scores (all items per UID x test x congruence)
**Step 3:** Compute Purified CTT mean scores (retained items only per UID x test x congruence)
**Step 4:** Cronbach's alpha reliability assessment with bootstrap CIs for Full and Purified CTT per congruence
**Step 5:** Correlation analysis: Pearson r for Full-IRT and Purified-IRT per congruence, Steiger's z-test for dependent correlations, Bonferroni alpha = 0.0167. Report dual p-values (Decision D068)
**Step 6:** Z-standardize all measurements (IRT theta, Full CTT, Purified CTT) for model comparability
**Step 7:** Fit parallel LMMs on z-standardized scores (identical formula for IRT, Full CTT, Purified CTT); compare AIC per Burnham & Anderson (delta > 2 meaningful)
**Step 8:** Prepare correlation comparison plot data and AIC comparison plot data

**Expected Outputs:**
- data/step01_item_mapping.csv (retained vs removed items by congruence)
- data/step02_ctt_full_scores.csv (400 rows: UID x test, 3 congruence columns)
- data/step03_ctt_purified_scores.csv (400 rows: UID x test, 3 congruence columns)
- data/step04_reliability_assessment.csv (3 rows: congruence levels with alpha_full, alpha_purified, bootstrap CIs)
- data/step05_correlation_analysis.csv (3 rows: congruence levels with r_full, r_purified, delta_r, Steiger_z, p_uncorrected, p_bonferroni)
- data/step07_lmm_model_comparison.csv (3 rows: congruence levels with AIC_IRT, AIC_Full, AIC_Purified, delta_AIC_Full_Purified)
- plots/step08_correlation_comparison_data.csv (6 rows: 3 congruence x 2 CTT types)
- plots/step08_aic_comparison_data.csv (3 rows: congruence levels with AIC comparisons)

**Success Criteria:**
- Data loading verified (RQ 5.4.1 dependency resolved)
- Item mapping complete: 48-52 total items, 36-40 retained after purification
- CTT scores in valid range [0,1] for both Full and Purified
- Correlation analysis complete with dual p-values (p_uncorrected and p_bonferroni per Decision D068)
- Z-standardization correct (mean ~ 0, SD ~ 1 for all measurements)
- All 3 LMMs converge (IRT, Full CTT, Purified CTT) for each congruence level
- Plot data complete: 6 rows for correlation comparison (3 congruence x 2 CTT types), 3 rows for AIC comparison
- Steiger's z-test assumptions validated

---

## Z-Standardization Rationale

### Why Z-Standardize?

IRT theta scores and CTT mean scores are on different scales:
- **IRT theta:** Logit scale, typically ranging -3 to +3, mean = 0 at average ability
- **CTT mean:** Proportion correct scale, ranging 0 to 1

**For LMM Coefficient Comparison:**
Z-standardization (mean = 0, SD = 1 for each score type) enables:
1. Direct comparison of regression coefficients across measurement types
2. Effect sizes interpretable in standard deviation units
3. AIC comparison across models with identical scaling

**Procedure:**
- Grand-mean center each score type: score_c = score - mean(score)
- Scale to unit variance: score_z = score_c / SD(score_c)
- Verify: mean(score_z) ~ 0, SD(score_z) ~ 1

### Bivariate Normality Check for Steiger's Z-Test

Steiger's z-test for comparing dependent correlations assumes bivariate normality. To validate:

1. **Scatter Plot Inspection:** IRT theta vs CTT (Full and Purified) should show elliptical point clouds
2. **Mardia's Test:** Compute multivariate skewness and kurtosis; significant values indicate violation
3. **Sensitivity Analysis:** If violated, report bootstrap CIs for delta_r as alternative

### Missing Data Handling

**Specification:**
- Complete case analysis: Exclude any participant × test × congruence observation with missing IRT theta OR CTT score
- Expected missingness: 0% (all participants completed all tests, IRT provides estimates for all)
- If missingness occurs: Document count and pattern; assess whether MCAR/MAR/MNAR

**Reporting:**
- Report N for each correlation (should be ~400 per congruence if complete)
- Note any exclusions due to missing data

### Practice Effects Acknowledgment

Practice effects affect both Full and Purified CTT. The key comparison is:
- Does purification (removing poor-quality items) improve CTT convergence with IRT?
- This is independent of practice effect magnitude

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.4.1 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 5.4.1 (Schema-Specific Trajectories)

**File Paths:**
- results/ch5/5.4.1/data/step02_purified_items.csv (list of items retained after IRT purification)
- results/ch5/5.4.1/data/step03_theta_scores.csv (IRT ability estimates per UID x test x congruence)
- results/ch5/5.4.1/data/step00_tsvr_mapping.csv (TSVR time variable mapping)

**Raw Data Dependency:**
- data/cache/dfData.csv (raw binary responses for CTT score computation)

**Dependencies:**
RQ 5.4.1 must complete Steps 1-3 (IRT calibration Pass 1, item purification per Decision D039, IRT calibration Pass 2) before this RQ can run. Purification thresholds: exclude items with discrimination a < 0.4 OR difficulty |b| > 3.0.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (inherited from RQ 5.4.1, no additional exclusions)

**Items:**
- [x] Full CTT: All items from RQ 5.4.1 pre-purification (~48-52 items across three congruence levels)
- [x] Purified CTT: Only items retained after RQ 5.4.1 purification (~36-40 items, expected 70-80% retention)
- Congruence categories: Common (i1/i2 tags), Congruent (i3/i4 tags), Incongruent (i5/i6 tags)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4) inherited from RQ 5.4.1 (nominal Days 0, 1, 3, 6)

---
