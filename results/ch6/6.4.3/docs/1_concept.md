# RQ 6.4.3: Age × Paradigm Interaction for Confidence Decline

**Chapter:** 6
**Type:** Paradigm Confidence
**Subtype:** Age × Paradigm
**Full ID:** 6.4.3

---

## Research Question

**Primary Question:**
Does age interact with paradigm (Free Recall, Cued Recall, Recognition) in determining confidence decline trajectories over the 6-day retention interval?

**Scope:**
This RQ examines whether age moderates the relationship between retrieval paradigm and confidence decline rates. Analysis uses IRT-derived confidence ability estimates (theta) from three paradigms across four test sessions (T1, T2, T3, T4; nominal Days 0, 1, 3, 6). Sample: N=100 participants × 4 tests × 3 paradigms = 1200 observations. Time variable uses log-transformed TSVR (hours since encoding).

**Theoretical Framing:**
Extends Chapter 5 findings on accuracy (RQ 5.3.4) to metacognitive domain. If age-invariant forgetting patterns observed for accuracy generalize to confidence, the Age × Paradigm × Time 3-way interaction should be NULL. Alternative: Older adults may show differential metacognitive monitoring across paradigm difficulty levels despite equivalent accuracy decline.

---

## Theoretical Background

**Relevant Theories:**
- **Dual-Process Theory (Yonelinas, 2002):** Free Recall relies on recollection (effortful retrieval), Cued Recall provides partial support, Recognition can rely on familiarity. If metacognitive monitoring differs between automatic (familiarity) and controlled (recollection) processes, age may interact with paradigm for confidence even if not for accuracy.
- **Age-Invariant VR Encoding Hypothesis (Chapter 5):** Ecological immersive VR creates age-invariant encoding quality, eliminating typical age × difficulty interactions. If this extends to metacognition, confidence decline should show the same age-invariance as accuracy.
- **Metacognitive Aging Literature:** Older adults may show preserved or even enhanced metacognitive monitoring in some contexts (e.g., better judgment-of-learning calibration), potentially creating age × paradigm interactions for confidence that don't exist for accuracy.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
If confidence parallels accuracy (Ch5 5.3.4 found NULL Age × Paradigm × Time interaction), expect NULL 3-way interaction for confidence. However, if metacognitive processes dissociate from memory processes with age, older adults may show differential confidence decline across paradigms despite equivalent accuracy decline (e.g., more conservative confidence in Free Recall, more liberal in Recognition).

**Literature Gaps:**
Few studies examine age × retrieval support interactions for metacognitive confidence in ecologically-valid episodic memory tasks. Most metacognitive aging research uses recognition paradigms exclusively. This RQ tests whether VR-induced age-invariance extends from accuracy to confidence across full paradigm spectrum.

---

## Hypothesis

**Primary Hypothesis:**
NULL hypothesis expected: The Age × Paradigm × Time 3-way interaction will be non-significant (p > 0.05 with Bonferroni correction), paralleling Chapter 5 accuracy findings (RQ 5.3.4). Age will NOT differentially moderate confidence decline across Free Recall, Cued Recall, and Recognition paradigms.

**Secondary Hypotheses:**
- Age main effect on baseline confidence may be marginal (older adults may show lower overall confidence due to age-related metacognitive conservatism), but this will not interact with paradigm type or time.
- Age × Time 2-way interaction should be NULL (consistent with Ch5 RQ 5.1.3, 5.2.3, 5.4.3 universal age null pattern).
- Paradigm × Time 2-way interaction may be NULL (per Ch5 5.3.1-5.3.2 findings that retrieval support affects baseline but not decay rate).

**Theoretical Rationale:**
VR ecological encoding creates age-invariant memory traces (Ch5 universal finding). If metacognitive monitoring reflects underlying memory trace quality, confidence should show the same age-invariance. The immersive encoding context provides rich retrieval cues that may eliminate typical age × difficulty interactions for both accuracy and confidence.

**Expected Effect Pattern:**
- Age_c × Paradigm × Time 3-way interaction: p > 0.05 (Bonferroni ± = 0.0167 for 3 tests: Age_c main, Age_c × Time, Age_c × Paradigm × Time)
- Dual p-value reporting per Decision D068 (Wald and LRT)
- If NULL confirmed: Effect size at Day 6 should be negligible (Cohen's d < 0.2 for age difference within any paradigm)
- Comparison to Ch5 5.3.4 should show consistent null pattern across accuracy and confidence domains

---

## Memory Domains

**Domains Examined:**

- [ ] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Not domain-stratified in this RQ

- [ ] **Where** (Spatial Location)
  - [ ] `-L-` tags (general location, legacy)
  - [ ] `-U-` tags (pick-up location)
  - [ ] `-D-` tags (put-down location)
  - Disambiguation: Not domain-stratified in this RQ

- [ ] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Not domain-stratified in this RQ

**Paradigm Focus:**
This RQ stratifies by **retrieval paradigm**, not memory domain:
- **Free Recall (IFR):** No retrieval support beyond context
- **Cued Recall (ICR):** Partial cue support (e.g., object name cues location)
- **Recognition (IRE):** Full retrieval support (forced choice among alternatives)

All three paradigms include What/Where/When domains, but analysis is collapsed across domains to focus on paradigm × age interaction.

**Inclusion Rationale:**
All interactive paradigm items (IFR, ICR, IRE) included to maximize power for detecting Age × Paradigm interactions. Room Free Recall (RFR) excluded as not interactive VR task (per Ch5 convention).

**Exclusion Rationale:**
No domain-based exclusions. Focus is on paradigm-level effects. Any items excluded during IRT purification (Step 2) based on psychometric criteria (Decision D039: |b| > 3.0 OR a < 0.4), not theoretical grounds.

---

## Analysis Approach

**Analysis Type:**
Linear Mixed Models (LMM) with 3-way interaction (Age × Paradigm × Time), using IRT-derived confidence theta scores from RQ 6.4.1 as dependent variable.

**High-Level Workflow:**

**Step 0:** Load confidence theta scores by paradigm from RQ 6.4.1 (data/step03_theta_confidence_paradigm.csv) and merge with age data from dfData.csv

**Step 1:** Prepare LMM input data:
- Center Age (Age_c) on grand mean
- Verify time transformation (log_TSVR from RQ 6.4.1)
- Structure: UID, Age, Age_c, Paradigm (3 levels: IFR/ICR/IRE), test, TSVR, log_TSVR, theta_confidence
- 1200 rows (100 participants × 4 tests × 3 paradigms)

**Step 2:** Fit LMM with 3-way interaction:
- Model: theta_confidence ~ (log_TSVR × Paradigm × Age_c) + (log_TSVR | UID)
- Random effects: Random intercepts and slopes by participant (nested within participant, not within paradigm)
- REML = True for variance component estimation
- Extract full model summary with all main effects, 2-way interactions, and 3-way interaction

**Step 3:** Extract interaction terms with dual p-value reporting (Decision D068):
- Age_c main effect (baseline age effect on confidence, averaged across paradigms)
- Age_c × Time 2-way interaction (does age affect confidence decline rate, averaged across paradigms)
- Age_c × Paradigm × Time 3-way interaction (PRIMARY TEST: does age differentially affect decline across paradigms)
- Report both Wald p-values and Likelihood Ratio Test (LRT) p-values
- Bonferroni correction: ± = 0.0167 for 3 tests

**Step 4:** Compare to Chapter 5 RQ 5.3.4:
- Load Ch5 5.3.4 Age × Paradigm × Time interaction results
- Create comparison table: Accuracy (Ch5) vs Confidence (Ch6) interaction terms
- Document whether null pattern replicates (both NULL) or diverges (one NULL, one significant)
- If both NULL: Strengthens age-invariance claim across both memory and metacognition
- If divergent: Suggests metacognitive processes dissociate from memory with age

**Expected Outputs:**
- data/step01_lmm_input.csv (1200 rows: UID, Age, Age_c, Paradigm, test, TSVR, log_TSVR, theta_confidence)
- results/step02_lmm_summary.txt (full model output including all effects)
- data/step03_interaction_terms.csv (Age_c terms with dual p-values, effect sizes)
- results/step04_ch5_comparison.csv (side-by-side comparison of Ch5 accuracy vs Ch6 confidence interaction terms)

**Success Criteria:**
- Model converges without singularity warnings
- Age_c properly centered (mean H 0)
- 1200 observations successfully analyzed
- All 3 critical terms extracted (Age_c main, Age_c × Time, Age_c × Paradigm × Time)
- Dual p-values computed for all terms (Wald and LRT)
- Bonferroni correction applied (± = 0.0167)
- Comparison to Ch5 5.3.4 documented with interpretation of consistency/divergence
- If 3-way interaction NULL: Confirms age-invariance extends to confidence across paradigms

---

## Data Source

**Data Type:**
DERIVED (from RQ 6.4.1 outputs and raw age data)

### DERIVED Data Source:

**Source RQ:**
RQ 6.4.1 (Paradigm Confidence Trajectories)

**File Paths:**
- results/ch6/6.4.1/data/step03_theta_confidence_paradigm.csv (IRT-derived confidence theta scores by paradigm, 1200 rows)
- data/cache/dfData.csv (Age variable)

**Dependencies:**
RQ 6.4.1 must complete Steps 0-3 (data extraction, IRT Pass 1, purification, IRT Pass 2, theta score generation) before this RQ can run. Specifically requires the 3-factor GRM calibration for IFR/ICR/IRE paradigms with 5-category ordinal confidence data (TC_* items).

**Additional Context from Ch5:**
- Chapter 5 RQ 5.3.4 results (Age × Paradigm × Time interaction for accuracy) required for comparison in Step 4
- File: results/ch5/5.3.4/data/step03_interaction_terms.csv or equivalent

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants from RQ 6.4.1 (inherited inclusion criteria)
- Age range preserved from source (expect approximately 18-80 years based on REMEMVR sample)
- No age-based exclusions

**Items:**
- Inherited from RQ 6.4.1 post-purification item set
- Only TC_* confidence items (5-category ordinal: 0, 0.25, 0.5, 0.75, 1.0)
- Only interactive paradigms: IFR, ICR, IRE
- Excluded: Room Free Recall (RFR), TCR (Temporal Cued Recall), RRE (not interactive VR)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4; nominal Days 0, 1, 3, 6)
- Time variable: TSVR (actual hours since encoding, log-transformed)

**Note:**
Age variable must be extracted fresh from dfData.csv and merged with theta scores by UID. Centering (Age_c) performed in Step 1 of this RQ's analysis, not inherited from source.

---
