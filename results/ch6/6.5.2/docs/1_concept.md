# RQ 6.5.2: Schema Confidence Calibration

**Chapter:** 6
**Type:** Schema Confidence
**Subtype:** Calibration
**Full ID:** 6.5.2

---

## Research Question

**Primary Question:**
Are people better calibrated for congruent items compared to common or incongruent items?

**Scope:**
This RQ examines calibration (confidence-accuracy alignment) across three schema congruence levels (Common, Congruent, Incongruent) over a 6-day retention interval. Sample: N=100 participants × 4 test sessions × 3 congruence levels = 1200 observations. Calibration computed as the difference between confidence theta and accuracy theta for each congruence level.

**Theoretical Framing:**
Schema congruence may affect metacognitive monitoring quality. Congruent items (schema-consistent) may feel familiar due to schema-driven processing, creating high confidence even when accuracy is not enhanced (Ch5 5.4.1 showed NULL schema effects on accuracy). This could produce overconfidence for congruent items. Incongruent items (schema-violating) may reduce false familiarity, potentially yielding better calibration.

---

## Theoretical Background

**Relevant Theories:**
- **Schema Theory** (Bartlett, 1932; Ghosh & Gilboa, 2014): Schema-consistent information benefits from pre-existing knowledge structures. However, this may create metacognitive illusions where schema-driven familiarity is mistaken for episodic recollection.
- **Fluency Misattribution** (Jacoby & Dallas, 1981): Fluent processing of schema-congruent items may be misattributed to strong episodic memory, inflating confidence without corresponding accuracy gains.
- **Dual-Process Theory** (Yonelinas, 2002): Familiarity-based recognition may be higher for schema-congruent items, but recollection-based accuracy may not differ (as found in Ch5 5.4.1).

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
Congruent items should show overconfidence (high confidence relative to accuracy) due to schema-driven familiarity signals that do not reflect actual episodic memory strength. Incongruent items should show better calibration because schema violations reduce false familiarity, forcing reliance on genuine episodic recollection for confidence judgments.

**Literature Gaps:**
Most schema research examines accuracy effects, not metacognitive calibration. VR episodic memory with schema manipulations provides unique opportunity to test whether schema effects are stronger for subjective confidence than objective accuracy.

---

## Hypothesis

**Primary Hypothesis:**
Congruent items will show OVERCONFIDENCE: schema-consistent items feel familiar (high confidence) but are not better remembered than common/incongruent items (Ch5 5.4.1 found NULL schema effects on accuracy). Expected pattern: Calibration_congruent > Calibration_common and Calibration_congruent > Calibration_incongruent (positive calibration = confidence exceeds accuracy).

**Secondary Hypotheses:**
Incongruent items may show better calibration (less false familiarity, more reliance on actual episodic memory for confidence judgments). Schema-violating items force metacognitive discrimination rather than schema-driven fluency.

**Theoretical Rationale:**
Ch5 5.4.1 found NO schema effect on accuracy (Common, Congruent, Incongruent showed equivalent forgetting trajectories). If confidence is driven by schema-induced familiarity while accuracy is not, this dissociation should manifest as overconfidence for congruent items. This would demonstrate that schema effects operate more strongly on metacognitive monitoring (System 2 metacognition) than on memory performance (System 1 retrieval).

**Expected Effect Pattern:**
Significant Congruence × Calibration interaction (p < 0.05). Post-hoc contrasts showing Congruent > Common and Congruent > Incongruent for calibration scores. Effect may be present at all timepoints (schema-driven familiarity persists even as memories fade) or emerge over time (as genuine episodic detail decays, schema-based judgments dominate).

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object identity is inherently linked to schema congruence (common/congruent/incongruent objects defined by What content)

- [ ] **Where** (Spatial Location)
  - Not examined in this RQ (schema manipulation is object-based, not spatial)

- [ ] **When** (Temporal Order)
  - Not examined in this RQ (schema effects on temporal memory not primary focus)

**Schema Congruence Levels:**

- [x] **Common** (Items i1, i2)
  - Items that appear in all room types (e.g., chair, table)
  - Schema-neutral baseline

- [x] **Congruent** (Items i3, i4)
  - Items that match room schema (e.g., bed in bedroom, stove in kitchen)
  - Expected to show schema-driven familiarity

- [x] **Incongruent** (Items i5, i6)
  - Items that violate room schema (e.g., toilet in kitchen, stove in bathroom)
  - Expected to reduce false familiarity

**Inclusion Rationale:**
All three congruence levels required to test hypothesis that congruent items show overconfidence relative to common (baseline) and incongruent items. What domain is inherent to schema manipulation (objects are schema-defined).

**Exclusion Rationale:**
Where and When domains excluded because schema congruence is defined at the object (What) level. Spatial and temporal processing are orthogonal to schema-object associations.

---

## Analysis Approach

**Analysis Type:**
LMM (Linear Mixed Models) for calibration comparison across schema congruence levels

**High-Level Workflow:**

**Step 0:** Merge accuracy theta (from Ch5 5.4.1) and confidence theta (from RQ 6.5.1) by UID × test × congruence level

**Step 1:** Compute calibration scores per congruence level: Calibration = theta_confidence - theta_accuracy (both z-standardized first within each congruence level)

**Step 2:** Fit LMM with Congruence × Time interaction: Calibration ~ Congruence × Time + (Time | UID), where Congruence has 3 levels (Common, Congruent, Incongruent)

**Step 3:** Test Congruence main effect and Congruence × Time interaction using dual p-value reporting (parametric and bootstrap, Decision D068)

**Step 4:** Test overconfidence hypothesis: Congruent > Common and Congruent > Incongruent via post-hoc contrasts (Bonferroni-corrected alpha = 0.025 for 2 contrasts)

**Expected Outputs:**
- data/step01_calibration_by_congruence.csv (1200 rows: UID, test, congruence, theta_accuracy, theta_confidence, calibration)
- results/step02_lmm_summary.txt (model convergence, coefficients, variance components)
- results/step03_congruence_effects.csv (Congruence main effect and Congruence × Time interaction with dual p-values)
- results/step04_congruent_overconfidence_test.csv (post-hoc contrasts: Congruent vs Common, Congruent vs Incongruent)

**Success Criteria:**
- Merge successful: 1200 observations (100 participants × 4 tests × 3 congruence levels)
- Calibration computed correctly (standardized theta difference)
- LMM converges with random slopes by UID
- Dual p-values reported for all effects (parametric and bootstrap)
- Post-hoc contrasts use Bonferroni-corrected alpha
- Interpretation addresses whether congruent items show overconfidence as predicted

---

## Data Source

**Data Type:**
DERIVED (from Ch5 RQ 5.4.1 and Ch6 RQ 6.5.1 outputs)

### DERIVED Data Source:

**Source RQs:**
- **Accuracy theta:** RQ 5.4.1 (Chapter 5 - Schema effects on accuracy trajectories)
- **Confidence theta:** RQ 6.5.1 (Chapter 6 - Schema effects on confidence trajectories)

**File Paths:**
- Accuracy: `results/ch5/5.4.1/data/step03_theta_scores_congruence.csv` (or equivalent theta output from 5.4.1)
- Confidence: `results/ch6/6.5.1/data/step03_theta_confidence_congruence.csv` (1200 rows: UID, test, congruence, theta_confidence)

**Dependencies:**
- Ch5 RQ 5.4.1 must complete IRT calibration (Steps 0-3) to produce accuracy theta scores by congruence level
- Ch6 RQ 6.5.1 must complete IRT calibration (Steps 0-3) to produce confidence theta scores by congruence level
- Both source RQs must use same 3-level congruence categorization (Common = i1/i2, Congruent = i3/i4, Incongruent = i5/i6)

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants from RQ 5.4.1 and 6.5.1 (inherited inclusion criteria)
- Expected N=100 (standard REMEMVR sample)

**Items:**
- [x] All items tagged for congruence analysis
  - Common: i1, i2 tags
  - Congruent: i3, i4 tags
  - Incongruent: i5, i6 tags
- Note: Exact item counts may vary after IRT purification in source RQs

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4 corresponding to Days 0, 1, 3, 6)
- Inherited from source RQs

**Schema Levels:**
- [x] All 3 congruence levels required (Common, Congruent, Incongruent)
- Cannot exclude any level (hypothesis requires 3-way comparison)

---
