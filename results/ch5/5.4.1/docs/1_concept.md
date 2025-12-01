# RQ 5.4.1: Do Congruent and Incongruent Items Show Different Forgetting Rates?

**Chapter:** 5
**RQ Number:** 4.1
**Full ID:** 5.4.1

---

## Research Question

**Primary Question:**
Does schema congruence (common, congruent, incongruent) affect the trajectory of episodic forgetting over 6 days?

**Scope:**
This RQ examines forgetting trajectories for three congruence categories using IRT-derived ability estimates across four test sessions (T1, T2, T3, T4). Time variable uses TSVR (actual hours since encoding). Congruence is operationalized via item codes:
- Common (schema-neutral): items i1, i2 (e.g., keys, phone, book - could appear in any room)
- Congruent (schema-consistent): items i3, i4 (e.g., toothbrush in bathroom, frying pan in kitchen)
- Incongruent (schema-violating): items i5, i6 (e.g., unexpected item-room pairings)

**Theoretical Framing:**
Schema theory predicts that schema-congruent information benefits from existing knowledge structures during both encoding and consolidation. This RQ tests whether congruence modulates forgetting rates, with implications for schema-mediated memory consolidation theories.

---

## Theoretical Background

**Relevant Theories:**
- **Schema Theory** (Bartlett, 1932): Memory is reconstructive, and schema-congruent information is better encoded and retained because it fits existing knowledge structures.
- **Schema-Mediated Consolidation** (Ghosh & Gilboa, 2014): Congruent information benefits from schema-based consolidation processes, leading to slower forgetting over time.
- **Von Restorff Effect:** Incongruent (schema-violating) items may have initial encoding advantage due to distinctiveness but lack consolidation support from existing schemas.

**Key Citations:**
- Bartlett (1932): Schema-based reconstruction of memory
- Ghosh & Gilboa (2014): Schema-mediated consolidation in hippocampal-neocortical systems

**Theoretical Predictions:**
Schema theory predicts congruent items will show slower forgetting than incongruent items due to schema-based consolidation support. The Von Restorff effect suggests incongruent items may have good initial encoding (T1) but steeper forgetting without schema support. Common (schema-neutral) items should fall between.

**Literature Gaps:**
Most schema-congruence studies examine encoding or single-session retrieval. Few studies test how congruence modulates forgetting trajectories over multiple days in immersive VR with real-world objects and spatial contexts.

---

## Hypothesis

**Primary Hypothesis:**
Congruent items (schema-consistent) will show slower forgetting than incongruent items (schema-violating), due to schema-based consolidation processes.

**Secondary Hypotheses:**
1. Common items (schema-neutral) will fall between congruent and incongruent in forgetting rate
2. Von Restorff effect may boost incongruent encoding (T1 performance) but not consolidation (steeper slopes)
3. By Day 6, ordering should be: Congruent > Common > Incongruent (theta values)

**Theoretical Rationale:**
Congruent information benefits from schema-based encoding and consolidation (Bartlett, 1932; Ghosh & Gilboa, 2014). Schema-consistent bindings (toothbrush-bathroom) are reinforced by prior knowledge, while schema-violating bindings (incongruent) lack this support. The interaction between Congruence and Time tests differential forgetting rates, the primary hypothesis.

**Expected Effect Pattern:**
Significant Congruence x Time interaction in LMM analysis. Post-hoc contrasts should show:
- Congruent slower forgetting than Common (positive interaction term)
- Incongruent faster forgetting than Common (negative interaction term, though may be ns after Bonferroni)
- Effect sizes at Day 6: d > 0.3 for Congruent vs Incongruent

---

## Memory Domains

**Note:** This RQ does NOT examine What/Where/When memory domains. Instead, it examines **Congruence** (a schema-based item property) across all interactive paradigm items.

**Congruence Categories Examined:**

- [x] **Common** (Schema-Neutral)
  - Item Codes: `*-i1`, `*-i2`
  - Description: Items that could plausibly appear in any room (keys, phone, book)
  - Role: Reference category for Treatment coding

- [x] **Congruent** (Schema-Consistent)
  - Item Codes: `*-i3`, `*-i4`
  - Description: Items with schema-specific room bindings (toothbrush in bathroom, frying pan in kitchen)
  - Role: Expected slowest forgetting

- [x] **Incongruent** (Schema-Violating)
  - Item Codes: `*-i5`, `*-i6`
  - Description: Items in unexpected room contexts (schema violations)
  - Role: Expected fastest forgetting (despite possible Von Restorff encoding boost)

**Inclusion Rationale:**
All three congruence categories included to test schema theory predictions about differential forgetting. Common serves as schema-neutral baseline for Treatment coding comparisons.

**Exclusion Rationale:**
- Room Free Recall (RFR) items excluded (different response format)
- Only Interactive paradigms (IFR, ICR, IRE) included (consistent with RQ 5.1-5.4)

---

## Analysis Approach

**Analysis Type:**
IRT (Item Response Theory) for ability estimation + LMM (Linear Mixed Models) for trajectory modeling

**High-Level Workflow:**

**Step 0:** Data Preparation
- Extract raw VR data from `data/cache/dfData.csv`
- Filter to keep only IFR, ICR, IRE columns (interactive paradigms)
- Dichotomize responses (>= 1 -> 1, < 1 -> 0)
- Create Q-matrix with congruence factor mapping:
  - common = `*-i1` and `*-i2`
  - congruent = `*-i3` and `*-i4`
  - incongruent = `*-i5` and `*-i6`
- Generate step00_irt_input.csv, step00_tsvr_mapping.csv, step00_q_matrix.csv

**Step 1:** IRT Analysis (Pass 1)
- Execute IRT pipeline for "Items by Congruence" analysis set
- Use correlated factors, 2-category GRM
- Extract theta scores and item parameters

**Step 2:** Item Purification
- Remove items with extreme difficulty (|b| > 3.0) or low discrimination (a < 0.4)
- Re-run IRT on purified item set (Pass 2)

**Step 3:** Data Preparation for LMM
- Reshape theta scores from wide to long format (Congruence as factor variable)
- Create time transformations: TSVR, TSVR^2, log(TSVR+1)
- Validate factor structure

**Step 4:** Model Fitting and Selection
- Fit 5 candidate LMMs with Congruence x Time interactions:
  - Linear: Time x Congruence
  - Quadratic: (Time + Time^2) x Congruence
  - Logarithmic: log(Time+1) x Congruence
  - Lin+Log: (Time + log(Time+1)) x Congruence
  - Quad+Log: (Time + Time^2 + log(Time+1)) x Congruence
- Treatment coding: Common as reference
- Random intercepts and slopes by UID
- Select best via AIC

**Step 5:** Post-hoc Contrasts
- Extract Time x Congruence interaction terms
- Test differences in forgetting slopes: Congruent-Common, Incongruent-Common
- Bonferroni correction: alpha = 0.0033/3 = 0.0011 (report with and without correction)

**Step 6:** Effect Size Computation
- Calculate Cohen's d for congruence differences at Day 6
- Report: d_Congruent_Common, d_Incongruent_Common, d_Congruent_Incongruent

**Step 7:** Visualization
- Generate trajectory plot: 3 lines (Common/Congruent/Incongruent) over Days 0-6
- Include observed means with 95% CIs and model predictions

**Data Preprocessing:**
- **Accuracy Scores:** Dichotomize before IRT (1 = 1, <1 = 0)
- **IRT Model:** GRM with 2 categories (dichotomous), correlated factors
- **Time Variable:** TSVR (actual hours since encoding)

**Special Methods:**
- **2-Pass IRT Purification:** Mandatory for all IRT analyses
- **Treatment Coding:** Common as reference (schema-neutral baseline)
- **TSVR Time Variable:** Actual hours since encoding, not nominal days

---

## Data Source

**Data Type:**
RAW (extracts directly from dfData.csv)

### RAW Data Source:

**Primary Source:**
`data/cache/dfData.csv` (VR test item responses)

**File Paths Generated (Step 0):**
- `data/step00_irt_input.csv` - Wide-format binary item responses (IFR/ICR/IRE items only)
- `data/step00_tsvr_mapping.csv` - Time mapping (composite_ID, UID, test, TSVR_hours)
- `data/step00_q_matrix.csv` - Q-matrix with congruence factors (common, congruent, incongruent)

**Dependencies:**
None. This is a ROOT RQ for the Congruence type (5.4.X). Extracts independently from raw data - no cross-type dependencies.

**Q-Matrix Configuration:**
Items mapped by congruence suffix (not by WWW domain):
- common = `*-i1` and `*-i2`
- congruent = `*-i3` and `*-i4`
- incongruent = `*-i5` and `*-i6`

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions)

**Items:**
- [x] Interactive paradigms only (IFR, ICR, IRE)
- [ ] Room Free Recall (RFR) - EXCLUDED (different response format)
- Items grouped by congruence code (i1-i6), not by memory domain

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4)
- Note: Time variable uses TSVR (actual hours since encoding)

---
