# Schema Baseline-Trajectory Framework - Cross-Chapter Validated

**Purpose:** Established framework distinguishing schema effects on BASELINE (encoding strength) vs TRAJECTORY (forgetting dynamics), validated across Ch5 accuracy and Ch6 confidence

**Status:** Framework established 2025-12-30, cross-chapter validation complete 2025-12-31

**Key Principle:** Schema congruence affects HOW WELL memories are encoded (baseline), NOT how fast they are forgotten (trajectory)

---

## Framework Established via GLMM Validation (2025-12-30)

**Archived from:** state.md Session (2025-12-30)
**Original Date:** 2025-12-30
**Reason:** Major thesis framework shift from "Quadruple NULL" to "Baseline effects, trajectory nulls"

---

### Discovery Context

**Original Narrative (Pre-GLMM):**
- "Quadruple NULL": Schema congruence has NO effect on memory performance
- Based on: 4 RQs all showed NULL findings (5.4.1, 6.5.1, 6.5.2, and congruence × time interactions)
- Interpretation: Schema congruence irrelevant to episodic memory in VR contexts

**GLMM Validation Findings:**

**RQ 5.4.1 (Accuracy Baseline):**
- IRT→LMM: Congruent vs Common p=0.548 (NULL)
- GLMM (N=28,800): Congruent vs Common p=0.011 (SIGNIFICANT)
- Effect: Congruent > Common > Incongruent
- Date: 2025-12-27 (GLMM validation)

**RQ 6.5.1 (Confidence Baseline):**
- IRT→LMM: Congruent vs Common p=0.660, Incongruent vs Common p=0.921 (both NULL)
- GLMM (N=28,800): Congruent p=0.003, Incongruent p<0.001 (both SIGNIFICANT)
- Pattern: Congruent > Common > Incongruent (β=+0.025, -0.053)
- Date: 2025-12-27 (GLMM run), 2025-12-30 (blocker documented)

**Trajectory Interactions (Unchanged):**
- Schema × Time interactions remain NULL across all RQs
- Forgetting curves are PARALLEL regardless of congruence
- Decline rates do NOT differ by schema type

---

### Revised Framework

**Baseline Effects (GLMM-Validated):**
- Schema congruence affects INITIAL encoding strength
- Congruent > Common > Incongruent pattern robust
- Detected at item-level (N=28,800) but obscured by aggregation (N=400)
- Applies to BOTH accuracy and confidence

**Trajectory Nulls (Interaction Tests):**
- Schema × Time interactions consistently NULL
- Forgetting dynamics INDEPENDENT of schema congruence
- Parallel decline curves across congruence types
- Applies to BOTH accuracy and confidence

**Interpretation:**
- Schema provides "encoding boost" at test time (better initial performance)
- BUT does NOT protect against forgetting (same decay rate)
- Congruent memories start higher, decline at same rate → maintain advantage over time

---

### Cross-Chapter Validation

**Accuracy (Ch5):**
- RQ 5.4.1: Baseline effect validated (GLMM p=0.011)
- Schema × Time interactions: NULL (5.4.x series)
- **Convergent evidence:** Baseline effects, trajectory nulls

**Confidence (Ch6):**
- RQ 6.5.1: Baseline effect validated (GLMM p=0.003)
- Schema × Time interactions: NULL (6.5.2, 6.5.x series)
- **Convergent evidence:** Baseline effects, trajectory nulls

**Metacognitive Monitoring:**
- Schema effects detected in BOTH memory and metacognition
- Suggests schema influences subjective confidence at encoding
- Monitoring system has access to schema congruence information

---

### Theoretical Significance

**Schema Theory Implications:**
- Schemas facilitate encoding (baseline) via spreading activation
- BUT do NOT alter forgetting dynamics (trajectory)
- Challenges "schema protection" hypothesis (no trajectory effects)

**Memory Systems:**
- Encoding vs consolidation/retrieval dissociation
- Schema congruence = encoding-stage phenomenon
- Forgetting rate = consolidation/retrieval-stage invariant

**VR Context Specificity:**
- Schema effects present despite immersive VR encoding
- Congruence boosts encoding even in highly contextualized environments
- VR scaffolding does NOT override schema congruence effects

---

### Thesis Narrative Revision

**FROM: "Quadruple NULL"**
- Schema congruence has NO effect on episodic memory
- VR contexts override schema influences
- Congruence irrelevant to memory performance

**TO: "Baseline Effects, Trajectory Nulls"**
- Schema congruence affects ENCODING STRENGTH (baseline)
- BUT does NOT affect FORGETTING DYNAMICS (trajectory)
- Encoding boost persists across retention interval (parallel decline)

**Impact on Thesis:**
- More nuanced theoretical contribution
- Distinguishes encoding vs forgetting mechanisms
- Aligns with dual-process memory models
- Strengthens VR episodic memory contribution

---

### Methodological Contribution

**GLMM Critical for Detection:**
- IRT→LMM (N=400): NULL findings (aggregation obscures small effects)
- GLMM (N=28,800): SIGNIFICANT findings (item-level power detects baseline differences)
- Without GLMM: Would have concluded "no schema effects" (incorrect)
- With GLMM: Correct conclusion "schema affects encoding, not forgetting"

**Aggregation vs Item-Level:**
- Aggregation loses statistical power for small baseline effects
- Item-level analysis provides 72× more observations
- Critical for detecting subtle encoding advantages

---

### User Decision Documented

**RQ 6.5.1 Status: CONDITIONAL PLATINUM**
- Statistical work complete
- GLMM finding robust (real effect, not artifact like RQ 6.3.3)
- Effect sizes detectable (β=+0.025, -0.053)
- Thesis narrative revision required

**Options Presented:**
- **Option A:** Accept GLMM finding, revise "Quadruple NULL" narrative (RECOMMENDED)
- **Option B:** Mark as caveat/limitation (NOT recommended, ignores stronger evidence)
- **Option C:** Defer to advisor consultation

**File:** `results/ch6/6.5.1/CONDITIONAL_PLATINUM_BLOCKER_2025-12-30.md` (300 lines)

---

### Implementation in Thesis

**Chapter 5 (Accuracy):**
- Section 5.4: Schema baseline effects validated
- Discussion: Encoding boost interpretation
- Cross-reference Ch6 convergent findings

**Chapter 6 (Confidence):**
- Section 6.5: Schema baseline effects validated
- Discussion: Metacognitive access to schema congruence
- Cross-reference Ch5 accuracy patterns

**General Discussion:**
- Schema encoding-forgetting dissociation
- Theoretical implications for dual-process models
- VR episodic memory contributions

---

**Last Updated:** 2025-12-30 (framework established), 2025-12-31 (cross-chapter validation)
**Status:** FRAMEWORK VALIDATED - THESIS NARRATIVE REVISION PENDING USER DECISION
**Related Topics:** platinum_batch_aggressive_parallel_strategy, glmm_candidates_documentation_updates
