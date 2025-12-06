# RQ 6.1.3: Age Effects on Confidence

**Chapter:** 6
**Type:** Confidence
**Subtype:** Age Effects
**Full ID:** 6.1.3

---

## Research Question

**Primary Question:**
Does age affect baseline confidence or confidence decline rate in VR episodic memory tasks over a 6-day retention interval?

**Scope:**
This RQ examines age effects on confidence trajectories using IRT-derived ability estimates across four test sessions (T1, T2, T3, T4; nominal Days 0, 1, 3, 6). Time variable uses log-transformed TSVR (actual hours since encoding). Tests two hypotheses: (1) Age effect on intercept (baseline confidence), (2) Age x Time interaction (differential decline rate). N=100 participants x 4 tests = 400 observations.

**Theoretical Framing:**
This RQ tests whether age moderates metacognitive monitoring of episodic memory. VR ecological encoding has produced age-invariant forgetting rates in Chapter 5 (RQs 5.1.3, 5.2.3, 5.3.4, 5.4.3 all NULL). If confidence parallels accuracy, metacognitive monitoring should also be age-invariant. However, older adults may show lower baseline confidence overall (age-related metacognitive changes) even if decline rate is similar.

---

## Theoretical Background

**Relevant Theories:**
- **VR Ecological Encoding:** Immersive VR creates naturalistic encoding that may eliminate age-related memory deficits typically seen in laboratory tasks. Chapter 5 demonstrated age-invariant forgetting rates across multiple analysis types (General, Domains, Paradigms, Congruence).
- **Metacognitive Aging:** Older adults may show metacognitive changes (potentially reduced confidence) independent of memory performance, reflecting age-related differences in self-assessment or strategic monitoring.

**Key Citations:**
[To be added by rq_scholar - specifically addressing metacognitive monitoring across lifespan and whether monitoring accuracy changes with age]

**Theoretical Predictions:**
If metacognitive monitoring parallels memory performance, and VR ecological encoding produces age-invariant memory decline (Ch5 universal finding), then metacognitive confidence should also show age-invariant decline. However, baseline confidence may differ if age affects general self-assessment tendencies independent of actual memory performance.

**Literature Gaps:**
[To be identified by rq_scholar - specifically whether metacognitive monitoring in ecologically valid VR contexts shows age effects, and whether monitoring can be age-invariant even when traditional lab memory shows age effects]

---

## Hypothesis

**Primary Hypothesis:**
Age will NOT significantly affect confidence decline rate (Age_c x Time interaction NULL, p > 0.05), paralleling Chapter 5 null findings (5.1.3, 5.2.3, 5.3.4, 5.4.3 all NULL).

**Secondary Hypothesis:**
Age_c main effect on intercept may be marginal or significant (older adults may be less confident overall at baseline), but this effect should be independent of decline rate.

**Theoretical Rationale:**
VR ecological encoding creates age-invariant forgetting in Chapter 5 across all analysis types. Metacognitive monitoring should parallel actual memory performance. If forgetting rate is age-invariant, metacognitive tracking of that forgetting should also be age-invariant. However, general confidence levels (metacognitive bias) may differ by age as a stable trait independent of memory performance.

**Expected Effect Pattern:**
- Age_c x Time interaction: NULL (p > 0.05, Bonferroni alpha = 0.0167 for dual p-value reporting per Decision D068)
- Age_c main effect: possibly marginal or significant (but theoretically secondary to interaction null)
- Effect size at Day 6: minimal (if any) difference in confidence trajectories between younger and older adults

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `TC_*-N-*`
  - Description: Confidence ratings (5-level Likert: 0, 0.25, 0.5, 0.75, 1.0) for object identity memory

- [x] **Where** (Spatial Location)
  - [x] `TC_*-L-*` tags (general location, legacy)
  - [x] `TC_*-U-*` tags (pick-up location)
  - [x] `TC_*-D-*` tags (put-down location)
  - Disambiguation: All Where sub-tags included (no disambiguation needed for omnibus confidence analysis)

- [x] **When** (Temporal Order)
  - Tag Code: `TC_*-O-*`
  - Description: Confidence ratings for temporal order memory

**Inclusion Rationale:**
RQ 6.1.3 uses omnibus "All" factor confidence (all TC_* confidence items combined, paralleling accuracy analysis in Ch5 5.1.1-5.1.3). This tests age effects on general metacognitive monitoring across all episodic memory domains. Domain-specific age effects will be examined separately in RQ 6.3.3.

**Exclusion Rationale:**
None - all interactive paradigm items (IFR, ICR, IRE) confidence ratings included to maximize statistical power and mirror Ch5 omnibus accuracy analyses.

---

## Analysis Approach

**Analysis Type:**
Linear Mixed Model (LMM) with Age x Time interaction on IRT-derived theta confidence scores

**High-Level Workflow:**

**Step 0:** Load theta_confidence scores from RQ 6.1.1 (IRT-derived ability estimates from 5-category ordinal confidence data) and TSVR time mapping. Load Age from dfData.csv.

**Step 1:** Center Age variable (Age_c = Age - mean(Age)) to enable interpretation of intercept as "average-age participant" and reduce multicollinearity.

**Step 2:** Fit LMM: theta_confidence ~ (Time + Time_log) x Age_c + (Time | UID), where Time and Time_log are the time predictors identified as optimal in RQ 6.1.1 functional form analysis. Random slopes by participant (UID) allow individual variation in forgetting rates.

**Step 3:** Extract Age_c main effect (baseline confidence difference) and Age_c x Time interaction (differential decline rate). Report dual p-values per Decision D068 (both uncorrected and Bonferroni-corrected alpha = 0.0167 for three comparisons: main effect Time, main effect Age_c, interaction).

**Step 4:** Compute effect size at Day 6: predicted confidence difference between younger (-1 SD Age_c) and older (+1 SD Age_c) adults at final retention test. Quantifies practical significance.

**Step 5:** Create age tertile comparison plot data: split participants into Low/Medium/High age tertiles, extract predicted trajectories per group for visualization.

**Step 6:** Compare results to Chapter 5 RQ 5.1.3 (age effects on accuracy omnibus analysis). Document parallel pattern (expect both to show NULL interaction, validating age-invariant decline for both memory and metacognition).

**Expected Outputs:**
- data/step01_lmm_input.csv (400 rows: UID, test, theta_confidence, TSVR, Age, Age_c, time transformations)
- results/step02_lmm_summary.txt (full LMM output with coefficients, SE, t-values, dual p-values)
- data/step03_age_effects.csv (extracted Age_c main effect and interaction terms with uncorrected and Bonferroni p-values)
- results/step04_effect_size.csv (confidence difference at Day 6 between younger/older adults)
- plots/step05_age_tertile_data.csv (12 rows: 3 tertiles x 4 tests, predicted means for plotting)
- results/step06_ch5_comparison.csv (comparison to Ch5 5.1.3 age effect results)

**Success Criteria:**
- Model converged with no singularity warnings
- Age_c variable properly centered (mean H 0, verify in step01 output)
- Dual p-values present in step03 output (both uncorrected and Bonferroni-corrected)
- Comparison to Ch5 5.1.3 documented (expect NULL replication for interaction, validating age-invariant decline pattern)
- Plot data complete: 12 rows (3 age tertiles x 4 test sessions) with no missing values

---

## Data Source

**Data Type:**
DERIVED (from RQ 6.1.1 outputs and dfData.csv)

### DERIVED Data Source:

**Source RQ:**
RQ 6.1.1 (Functional Form Comparison for Confidence)

**File Paths:**
- results/ch6/6.1.1/data/step03_theta_confidence.csv (IRT-derived ability estimates for confidence, 400 rows)
- results/ch6/6.1.1/data/step00_tsvr_mapping.csv (time mapping: UID, test, TSVR hours)
- data/cache/dfData.csv (Age variable extraction)

**Dependencies:**
RQ 6.1.1 must complete Steps 1-3 (IRT Pass 1, purification, IRT Pass 2) before this RQ can run. Requires theta_confidence scores derived from 5-category ordinal confidence data using Graded Response Model (GRM).

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants from RQ 6.1.1 (inherited inclusion criteria)
- Age range inherited from master dataset (will be extracted from dfData.csv)
- No age-based exclusions (testing age as continuous predictor)

**Items:**
- N/A (theta_confidence scores already aggregated across items via IRT)
- Item-level purification completed in RQ 6.1.1 Step 2 (Decision D039: exclude items with |b| > 3.0 OR a < 0.4)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4; nominal Days 0, 1, 3, 6)
- Time variable = TSVR (actual hours since encoding), not nominal days
- Time transformations determined by RQ 6.1.1 functional form selection

---

## Notes for Downstream Agents

**Critical Design Elements:**
1. **Age Centering (Step 1):** MANDATORY before LMM fitting. Enables intercept interpretation as "average-age participant" and reduces multicollinearity in interaction terms.

2. **Dual P-Value Reporting (Step 3):** Per Decision D068, report both uncorrected p-values and Bonferroni-corrected threshold (alpha = 0.0167 for three comparisons). This addresses multiple comparison concerns while preserving transparency.

3. **Functional Form Dependency (Step 2):** Time predictors (Time + Time_log or alternative) determined by RQ 6.1.1 model selection. Do NOT assume linear time - use best functional form from 6.1.1.

4. **Chapter 5 Comparison (Step 6):** Direct comparison to Ch5 5.1.3 is CRITICAL for validating theoretical framework. If both accuracy and confidence show age-invariant decline, strengthens VR ecological encoding interpretation. If divergent, suggests dissociation between memory and metacognition aging effects.

5. **Null Hypothesis Significance:** NULL interaction is the EXPECTED and theoretically meaningful result (replicating Ch5 age-invariant pattern). Do not treat null as "failure" - it validates theoretical predictions.

**Potential Challenges:**
- If Age_c main effect is significant but interaction is null, interpretation is complex: older adults have different baseline confidence but same decline rate. Document carefully.
- Age range in sample may be limited (verify distribution in step01 descriptives). Restricted range reduces power to detect age effects.
- Random slope variance for Age x Time interaction may be near-zero (paralleling Ch5 ICC_slope H 0 findings). This is expected and theoretically meaningful.

---

**End of Concept Document**
