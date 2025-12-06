# RQ 6.3.3: Age × Domain Interaction in Confidence Decline

**Chapter:** 6
**Type:** Domain Confidence
**Subtype:** Age × Domain
**Full ID:** 6.3.3

---

## Research Question

**Primary Question:**
Does age interact with memory domain (What/Where/When) for confidence decline trajectories over a 6-day retention interval?

**Scope:**
This RQ examines 3-way interaction between Age × Domain × Time using IRT-derived confidence ability estimates from RQ 6.3.1. Sample: N=100 participants × 4 tests × 3 domains = 1200 observations. Age analyzed as continuous centered variable. Domain includes What (object identity), Where (spatial location), and When (temporal order).

**Theoretical Framing:**
Tests whether older adults show differential metacognitive decline across memory domains compared to younger adults. Parallels Chapter 5 RQ 5.2.3 which tested Age × Domain for accuracy. If confidence parallels accuracy (Ch5 showed age-invariant forgetting across all domains), the 3-way interaction should be NULL.

---

## Theoretical Background

**Relevant Theories:**
- **Age-Related Associative Deficit (ARAD):** Predicts older adults should show greater deficits for relational memory (Where, When) compared to item memory (What). However, VR ecological encoding may eliminate this effect (as found in Ch5).
- **Metacognitive Aging:** Older adults may show preserved metacognitive monitoring despite memory decline, leading to age-invariant confidence trajectories even if accuracy differs.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
Based on Chapter 5 findings (5.1.3, 5.2.3, 5.3.4, 5.4.3 all showed NULL age effects), age is expected to NOT interact with domain for confidence decline. VR ecological encoding creates age-invariant forgetting patterns that should extend to metacognitive judgments.

**Literature Gaps:**
[To be identified by rq_scholar]

---

## Hypothesis

**Primary Hypothesis:**
NULL expected: Age × Domain × Time 3-way interaction will be non-significant (p > 0.05), paralleling Chapter 5 RQ 5.2.3 null findings. Age will not moderate the relationship between domain type and confidence decline rate.

**Secondary Hypotheses:**
- Age main effect on intercept may be marginal (older adults potentially less confident overall)
- Age × Time interaction expected NULL (age-invariant decline rates, replicating Ch5 5.1.3)
- Domain × Time interaction expected NULL (replicating Ch5 5.2.1 and RQ 6.3.1)

**Theoretical Rationale:**
If VR ecological encoding eliminates age-related memory differences (as demonstrated across all Chapter 5 RQ types), and if confidence tracks memory accuracy, then metacognitive monitoring should show the same age-invariant pattern. Any preserved age × domain interaction would suggest dissociation between memory and metacognition.

**Expected Effect Pattern:**
3-way interaction p-value > 0.05 (Bonferroni corrected). All 2-way interactions involving Age expected NULL. Age effect only possible on baseline intercept, not slopes.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object identity / naming confidence

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location, legacy)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Disambiguation: All Where subtypes combined for omnibus domain analysis

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order / sequence confidence
  - Note: When domain may have limited items after purification (see RQ 6.3.1 status)

**Inclusion Rationale:**
All three episodic memory domains (What/Where/When) included to test comprehensive age × domain interaction. This matches Ch5 5.2.3 design for direct comparison.

**Exclusion Rationale:**
When domain items may be limited due to floor effects found in Chapter 5 accuracy analyses. RQ 6.3.1 documents When domain status after purification. If <10 items remain, When domain may need exclusion from interaction analysis.

---

## Analysis Approach

**Analysis Type:**
Linear Mixed Models (LMM) with 3-way interaction (Age × Domain × Time)

**High-Level Workflow:**

**Step 0:** Load domain-stratified confidence theta scores from RQ 6.3.1 (results/ch6/6.3.1/data/step03_theta_confidence_domain.csv) and merge with Age from data/cache/dfData.csv

**Step 1:** Center Age variable (Age_c = Age - mean(Age)) to facilitate interpretation of main effects and reduce multicollinearity

**Step 2:** Fit LMM: theta_confidence ~ (Time + Time_log) × Age_c × Domain + (Time | UID)
- Random intercept and slope by participant (UID)
- Fixed effects: All main effects, 2-way interactions, and 3-way interaction
- Time variables: linear Time and logarithmic Time_log (based on best functional form from RQ 6.1.1)

**Step 3:** Extract 3-way interaction terms (Age_c × Domain × Time and Age_c × Domain × Time_log) with Bonferroni-corrected alpha = 0.0167 (correcting for 3 interaction terms). Report dual p-values per Decision D068.

**Step 4:** Compare results to Chapter 5 RQ 5.2.3 (age × domain interaction for accuracy). Document whether confidence replicates accuracy null pattern.

**Expected Outputs:**
- data/step01_lmm_input.csv (1200 rows: UID, Age_c, Domain, Time, theta_confidence)
- results/step02_lmm_summary.txt (full model output with all coefficients)
- data/step03_interaction_terms.csv (3-way interaction coefficients with dual p-values)
- results/step04_ch5_comparison.csv (comparison to Ch5 5.2.3 findings)

**Success Criteria:**
- LMM converges successfully
- Age properly centered (mean H 0, SD preserved)
- 3-way interaction terms extracted and tested
- Bonferroni correction applied (alpha = 0.0167)
- Dual p-values reported (per Decision D068)
- Comparison to Ch5 5.2.3 documented (expected: both NULL)

---

## Data Source

**Data Type:**
DERIVED (from RQ 6.3.1 outputs + Age variable)

### DERIVED Data Source:

**Source RQ:**
RQ 6.3.1 (Domain Confidence Trajectories)

**File Paths:**
- results/ch6/6.3.1/data/step03_theta_confidence_domain.csv (1200 rows: domain-stratified confidence theta scores from 3-factor GRM)
- data/cache/dfData.csv (for Age variable extraction)

**Dependencies:**
RQ 6.3.1 must complete Steps 0-3 (data extraction, IRT calibration with 3-factor GRM for What/Where/When, theta score generation) before this RQ can run.

**Additional Context:**
- RQ 6.3.1 uses Graded Response Model (GRM) for 5-category confidence items (TC_* tags with Likert scale: 0, 0.25, 0.5, 0.75, 1.0)
- Three separate theta estimates per participant per timepoint (one per domain)
- When domain status depends on purification results (may have <10 items if floor effects severe)

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (inherited from RQ 6.3.1)
- [x] Age variable available for all participants

**Items:**
- N/A (theta scores already aggregated per domain)
- When domain inclusion conditional on RQ 6.3.1 purification results

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4; nominal Days 0, 1, 3, 6)
- Time variable uses TSVR (actual hours since encoding)

**Exclusions:**
- None expected unless RQ 6.3.1 excludes entire When domain (<10 items post-purification)

---
