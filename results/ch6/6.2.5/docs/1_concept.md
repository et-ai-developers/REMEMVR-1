# RQ 6.2.5: Calibration Age Effects

**Chapter:** 6
**Type:** Calibration
**Subtype:** Age Effects
**Full ID:** 6.2.5

---

## Research Question

**Primary Question:**
Does calibration decline faster for older adults?

**Scope:**
This RQ examines whether age moderates the relationship between confidence and accuracy alignment (calibration) across the 6-day retention interval. Sample: N=100 participants x 4 test sessions = 400 observations. Time variable uses TSVR (actual hours since encoding). Age is centered for interpretation.

**Theoretical Framing:**
Extends the universal age null pattern from Chapter 5 (RQs 5.1.3, 5.2.3, 5.3.4, 5.4.3 all found no age × time interactions) to metacognitive monitoring. If VR ecological encoding creates age-invariant forgetting trajectories, metacognitive calibration should similarly be age-invariant.

---

## Theoretical Background

**Relevant Theories:**
- **Metacognitive Monitoring Theory**: Accuracy of self-assessments may decline with age due to frontal lobe deterioration affecting metacognitive processes.
- **Age-Invariant Encoding Hypothesis** (from Chapter 5): VR ecological encoding eliminates typical age-related deficits, creating parallel forgetting trajectories across age groups.
- **Dissociable Systems**: Memory and metacognition may show different age trajectories if they rely on distinct neural substrates (medial temporal lobe vs prefrontal cortex).

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
If metacognitive monitoring parallels memory performance (both age-invariant), then Age × Time interaction should be NULL. Alternative: Older adults may show lower baseline calibration (overall less accurate memory) but same trajectory slope (parallel decline).

**Literature Gaps:**
[To be identified by rq_scholar]

---

## Hypothesis

**Primary Hypothesis:**
Age will NOT significantly moderate calibration trajectory (Age × Time interaction NULL, p > 0.05), consistent with Chapter 5 universal age null pattern across all RQ types.

**Secondary Hypotheses:**
Age_c main effect on intercept may be marginal (older adults may show lower baseline calibration due to lower overall accuracy), but interaction with Time should be non-significant.

**Theoretical Rationale:**
Chapter 5 found consistent null effects for age × time interactions across General (5.1.3), Domains (5.2.3), Paradigms (5.3.4), and Congruence (5.4.3) analyses. VR ecological encoding creates age-invariant forgetting rates. If metacognitive monitoring tracks memory performance, calibration trajectories should also be age-invariant. Any baseline differences in calibration would reflect age differences in baseline accuracy (already established in Ch5), not differential metacognitive decline.

**Expected Effect Pattern:**
- Age_c main effect: May be significant (p < 0.05), reflecting baseline accuracy differences
- Age_c × Time interaction: NULL (p > 0.05), paralleling Ch5 age null findings
- Age tertile trajectories: Parallel slopes, possibly different intercepts

---

## Memory Domains

**Domains Examined:**

- [x] **Omnibus "All" Factor**
  - Aggregates across all What/Where/When domains
  - Uses calibration scores derived from Chapter 5 (accuracy) and Chapter 6 (confidence) omnibus analyses
  - Domain-agnostic calibration metric

**Inclusion Rationale:**
This RQ uses calibration scores computed from omnibus theta estimates (aggregated across all domains). Domain-specific calibration analyses are addressed in separate RQs (6.3.2 for What/Where/When domains, 6.4.2 for paradigms, 6.5.2 for schema congruence).

**Exclusion Rationale:**
Individual domains excluded to maintain consistency with RQ 6.2.1 (omnibus calibration over time) and to maximize sample size for age interaction detection (400 observations vs 1200 domain-stratified observations that would reduce power per domain).

---

## Analysis Approach

**Analysis Type:**
Linear Mixed Model (LMM) with Age × Time interaction

**High-Level Workflow:**

**Step 0:** Load calibration scores from RQ 6.2.1 (results/ch6/6.2.1/data/step02_calibration_scores.csv) and merge with Age from data/cache/dfData.csv

**Step 1:** Center Age (Age_c = Age - mean(Age)) for interpretable intercept estimates

**Step 2:** Fit LMM: Calibration ~ Time × Age_c + (Time | UID)
- Fixed effects: Time (log_Days_plus1 or best functional form from 6.1.1), Age_c, Time × Age_c
- Random effects: Random intercepts and slopes by participant (UID)
- REML = False for nested model comparison if needed

**Step 3:** Extract Age_c main effect and Age_c × Time interaction terms
- Test with Bonferroni correction: alpha = 0.0167 (3 comparisons: main effect, interaction, intercept)
- Report dual p-values per Decision D068 (uncorrected + Bonferroni-corrected)

**Step 4:** Compute effect sizes
- Age effect at Day 6: predicted calibration difference between young (Age_c = -20) vs old (Age_c = +20) adults
- Interaction effect: difference in slopes (young vs old decline rates)

**Step 5:** Age tertile analysis
- Split participants into Low/Medium/High age tertiles
- Plot calibration trajectories by tertile
- Visual comparison of slopes and intercepts

**Step 6:** Compare to Chapter 5 age null findings
- Reference RQs 5.1.3, 5.2.3, 5.3.4, 5.4.3 (all found NULL age × time interactions)
- Document whether metacognitive calibration replicates accuracy age null pattern
- Interpret any deviations from Ch5 pattern

**Expected Outputs:**
- data/step01_calibration_age.csv (400 rows: UID, test, calibration, Age, Age_c, Time)
- results/step02_lmm_summary.txt (LMM output with Age × Time terms)
- data/step03_age_effects.csv (Age_c main effect and interaction with dual p-values per D068)
- plots/step04_age_tertile_calibration.csv (plot data: age tertile × timepoint trajectories)
- results/step05_ch5_comparison.csv (comparison to Ch5 5.1.3, 5.2.3, 5.3.4, 5.4.3 age null findings)

**Success Criteria:**
- Model converged successfully
- Age_c properly centered (mean = 0, SD documented)
- Dual p-values present (uncorrected + Bonferroni-corrected per D068)
- Age tertile plot has 12 rows (3 tertiles × 4 tests)
- Comparison to Ch5 age null pattern documented (expected: replication of NULL interaction)
- Interpretation clear: whether calibration trajectories are age-invariant or show differential aging effects

---

## Data Source

**Data Type:**
DERIVED (from RQ 6.2.1 outputs and dfData.csv)

### DERIVED Data Source:

**Source RQ:**
RQ 6.2.1 (Calibration Over Time)

**File Paths:**
- results/ch6/6.2.1/data/step02_calibration_scores.csv (400 rows: UID, test, theta_accuracy, theta_confidence, calibration)
- data/cache/dfData.csv (for Age variable)

**Dependencies:**
RQ 6.2.1 must complete Step 2 (calibration scores computed from merged accuracy and confidence theta estimates) before this RQ can run. Age variable extracted from dfData.csv participant demographics.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants from RQ 6.2.1 (inherited inclusion criteria)
- [x] Age range: ~18-80 years (documented in dfData.csv demographics)
- [ ] Exclude: No exclusions based on age (full age range analyzed)

**Items:**
- N/A (calibration scores already aggregated from theta estimates, not item-level)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4; nominal Days 0, 1, 3, 6)
- [x] Time variable: TSVR (actual hours since encoding) inherited from RQ 6.2.1

---
