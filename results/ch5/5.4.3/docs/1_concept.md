# RQ 5.4.3: Age × Schema Interactions

**Chapter:** 5
**Type:** Congruence
**Subtype:** Age × Schema Interactions
**Full ID:** 5.4.3

---

## Research Question

**Primary Question:**
Does the effect of age on forgetting rate vary by schema congruence (common, congruent, incongruent)?

**Scope:**
This RQ examines whether age-related forgetting effects differ across three schema congruence levels using IRT-derived ability estimates. Sample: N=100 participants (age 20-70 years) × 4 test sessions (nominal Days 0, 1, 3, 6) × 3 congruence levels = 1200 observations after reshaping from wide to long format. Time variable uses TSVR (actual hours since encoding). Age is grand-mean centered. Tests 3-way interaction (Age × Congruence × Time).

**Theoretical Framing:**
This RQ tests whether schema congruence moderates age-related memory decline. If older adults rely more on schema-based consolidation, age effects may be weakest for congruent items (schema support available) and strongest for incongruent items (schema interference). Explores individual differences in schema utilization across the lifespan.

---

## Theoretical Background

**Relevant Theories:**
- **Schema Theory:** Congruent items (schema-consistent) benefit from existing knowledge structures during encoding and consolidation, while incongruent items (schema-violating) lack this support and may show greater vulnerability to age-related decline.
- **Aging and Schema Reliance:** Older adults may rely more heavily on schema-based processing to compensate for declining hippocampal function. If true, age effects should be smallest for congruent items (greatest schema support) and largest for incongruent items (least schema support, most hippocampal-dependent).

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
Age × Time effects strongest for incongruent items (least schema support for consolidation). Age × Time effects weakest for congruent items (schema compensates for hippocampal aging). Common items fall between. 3-way Age × Congruence × Time interaction captures this pattern.

**Literature Gaps:**
[To be identified by rq_scholar]

---

## Hypothesis

**Primary Hypothesis:**
Age × Time effects will be strongest for incongruent items (least schema support for consolidation) and weakest for congruent items (greatest schema support). 3-way Age × Congruence × Time interaction will be significant at Bonferroni alpha = 0.025.

**Secondary Hypotheses:**
Common items (schema-neutral) will show intermediate age effects, falling between congruent and incongruent. Tukey HSD post-hoc tests will reveal significant differences in age effects across congruence levels at Day 3.

**Theoretical Rationale:**
Based on schema theory and aging literature, older adults may compensate for hippocampal decline by relying on schema-based consolidation. Congruent items benefit from this strategy, showing attenuated age effects. Incongruent items cannot leverage schema support, showing maximal age-related vulnerability. Common items lack strong schema associations, showing moderate age effects.

**Expected Effect Pattern:**
Significant 3-way interaction (Age × Congruence × Time) with p < 0.025 after Bonferroni correction for 2 time terms (linear and logarithmic). Post-hoc tests at Day 3 will show Age effect size: Incongruent > Common > Congruent. Dual p-values reported per Decision D068.

---

## Memory Domains

**Domains Examined:**

- [ ] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object identity / naming

- [ ] **Where** (Spatial Location)
  - [ ] `-L-` tags (general location, legacy)
  - [ ] `-U-` tags (pick-up location)
  - [ ] `-D-` tags (put-down location)
  - Disambiguation: Not examined in this RQ

- [ ] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order / sequence

**Congruence Levels (Schema Focus):**

- [x] **Common** (Schema-Neutral)
  - Tag Code: `-i1`, `-i2`
  - Description: Items present in both room types (no schema preference)

- [x] **Congruent** (Schema-Consistent)
  - Tag Code: `-i3`, `-i4`
  - Description: Items matching room schema expectations

- [x] **Incongruent** (Schema-Violating)
  - Tag Code: `-i5`, `-i6`
  - Description: Items violating room schema expectations

**Inclusion Rationale:**
This RQ focuses on schema congruence as the primary factor, aggregating across What/Where/When domains. Congruence tags capture schema-based memory effects independent of domain. All three congruence levels included to test linear and non-linear age effects across schema support gradient.

**Exclusion Rationale:**
Domain-specific analysis not conducted in this RQ (addressed in RQ 5.2.3). This analysis aggregates domains to isolate schema congruence effects on age-related forgetting.

---

## Analysis Approach

**Analysis Type:**
Linear Mixed Models (LMM) with 3-way interaction (Age × Congruence × Time)

**High-Level Workflow:**

**Step 0:** Load IRT theta scores from RQ 5.4.1 (400 rows: 100 participants × 4 tests, with theta_common, theta_congruent, theta_incongruent in wide format). Load Age variable from data/cache/dfData.csv. Validate dependency and data structure.

**Step 1:** Merge theta scores with Age and TSVR mapping. Reshape from wide to long format (1200 rows: 100 participants × 4 tests × 3 congruence levels). Grand-mean center Age (Age_c). Create time transformations: TSVR_hours (linear time), log_TSVR (logarithmic time based on RQ 5.4.1 best model selection).

**Step 2:** Fit LMM with full 3-way interaction structure:
theta ~ TSVR_hours + log_TSVR + Age_c + Congruence + (Age_c × TSVR_hours) + (Age_c × log_TSVR) + (Congruence × TSVR_hours) + (Congruence × log_TSVR) + (Age_c × Congruence) + (Age_c × Congruence × TSVR_hours) + (Age_c × Congruence × log_TSVR) + (TSVR_hours | UID)

Random effects: Random intercepts and slopes for TSVR_hours by participant (UID).

**Step 3:** Extract 4 three-way interaction terms (Age_c × Congruence_Congruent × TSVR_hours, Age_c × Congruence_Incongruent × TSVR_hours, Age_c × Congruence_Congruent × log_TSVR, Age_c × Congruence_Incongruent × log_TSVR). Test significance at Bonferroni alpha = 0.025 (correcting for 2 time terms). Report dual p-values (p_uncorrected and p_bonferroni) per Decision D068.

**Step 4:** Compute congruence-specific age effects at Day 3 (midpoint retention interval). Extract marginal slopes for each congruence level. Perform Tukey HSD post-hoc tests to compare age effect sizes across congruence levels. Report dual p-values.

**Step 5:** Prepare plot data by age tertiles (Young/Middle/Older) for visualization. Compute marginal means and confidence intervals for each age tertile × congruence level × test timepoint combination. Output data for 3-panel plot (one panel per congruence level).

**Expected Outputs:**
- data/step01_lmm_input.csv (1200 rows: UID, test, congruence, theta, Age_c, TSVR_hours, log_TSVR)
- data/step02_lmm_model.pkl (saved LMM model object)
- data/step03_interaction_terms.csv (4 rows: 3-way interaction coefficients, SE, z-statistic, p_uncorrected, p_bonferroni)
- data/step04_age_effects_by_congruence.csv (3 rows: age effect slope per congruence level with Tukey HSD results)
- plots/step05_age_effects_plot_data.csv (36 rows: 3 age tertiles × 3 congruence × 4 timepoints, with mean_theta, CI_lower, CI_upper)

**Success Criteria:**
- Model convergence confirmed (model.converged = True)
- All 1200 observations present in merged data
- Age_c grand-mean centered (mean approximately 0)
- 4 three-way interaction terms extracted with valid standard errors
- Dual p-values present for all hypothesis tests (Decision D068)
- Bonferroni correction applied correctly (alpha = 0.05/2 = 0.025)
- Tukey HSD post-hoc tests complete for 3 congruence levels
- Plot data structure correct: 36 rows, CI_upper > CI_lower, theta values in plausible range [-4, 4]
- All assumption validation checks documented (see Validation Procedures below)

---

## Validation Procedures

### LMM Assumption Checks

1. **Residual Normality:** Q-Q plot + Shapiro-Wilk test (accept if p > 0.01)
2. **Homoscedasticity:** Residuals vs fitted plot; Levene's test by congruence × age tertile
3. **Random Effects Normality:** Q-Q plot of random intercept and slope estimates
4. **Independence:** ACF plot of residuals (no significant autocorrelation)
5. **Linearity:** Residuals vs TSVR_hours and log_TSVR (no systematic patterns)
6. **Outliers:** Cook's distance < 4/N threshold

### Remedial Actions

- If normality violated: Report robust standard errors or use bootstrap confidence intervals
- If heteroscedasticity: Use weighted LMM or variance function by congruence level
- If outliers detected: Sensitivity analysis with/without outliers; report both results

### Convergence Contingency Plan

If the full model (random slopes for TSVR_hours) fails to converge:
1. Try alternative optimizers (bobyqa, nlminb)
2. Use likelihood ratio test (LRT) to compare random slopes vs intercept-only
3. If LRT p < 0.05, retain slopes with simplified correlation structure
4. If LRT p ≥ 0.05, use random intercepts-only model
5. Document which structure achieved convergence in results

Reference: Bates et al. (2015) parsimonious mixed models guidelines.

### Congruence Reference Category and Contrast Coding

**Reference Category:** Common (schema-neutral)
- This choice provides interpretable contrasts: Congruent vs Common, Incongruent vs Common
- Alternative: effect coding (deviation from grand mean) if comparing all pairwise differences

**Contrast Interpretation:**
- Congruent coefficient: Difference between Congruent and Common congruence effect on Age × Time interaction
- Incongruent coefficient: Difference between Incongruent and Common congruence effect on Age × Time interaction
- If Incongruent shows larger positive coefficient than Congruent: Age accelerates forgetting more for incongruent items

**Post-hoc Contrasts:**
Tukey HSD tests all three pairwise comparisons with family-wise error control:
1. Congruent vs Common
2. Incongruent vs Common
3. Incongruent vs Congruent

### Practice Effects Acknowledgment

The 4-session design creates potential practice effects that may interact with schema congruence:
- Schema-congruent items may show different practice effect trajectories than incongruent items
- IRT theta scoring partially mitigates item-level practice effects
- The Age × Congruence × Time interaction is interpretable relative to these confounds

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.4.1 outputs and master data)

### DERIVED Data Source:

**Source RQ:**
RQ 5.4.1 (Schema-Specific Trajectories)

**File Paths:**
- results/ch5/5.4.1/data/step03_theta_scores.csv (IRT ability estimates: 400 rows with theta_common, theta_congruent, theta_incongruent in wide format)
- results/ch5/5.4.1/data/step00_tsvr_mapping.csv (TSVR time variable: actual hours since encoding)
- data/cache/dfData.csv (Age variable: participant ages 20-70 years)

**Dependencies:**
RQ 5.4.1 must complete Step 3 (IRT calibration for congruence factors) before this RQ can run. Theta scores must be in wide format with separate columns for each congruence level to enable reshaping to long format.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants from RQ 5.4.1 (N=100, inherited inclusion criteria)
- Age range: 20-70 years (continuous variable, grand-mean centered)

**Items:**
- N/A (theta scores already aggregated by congruence level in RQ 5.4.1)
- Congruence levels derived from IRT calibration in RQ 5.4.1 (common/congruent/incongruent factors)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4 at nominal Days 0, 1, 3, 6)
- [x] Inherited from RQ 5.4.1 (all tests included)

**Time Variable:**
- TSVR (actual hours since encoding, not nominal days)
- Transformations: TSVR_hours (linear), log_TSVR (logarithmic, based on RQ 5.4.1 best model)

---
