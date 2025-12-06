# RQ 6.5.1: Schema Congruence Effects on Confidence Trajectories

**Chapter:** 6
**Type:** Schema Confidence
**Subtype:** Trajectories
**Full ID:** 6.5.1

---

## Research Question

**Primary Question:**
Do Common/Congruent/Incongruent items show different confidence decline patterns across a 6-day retention interval?

**Scope:**
This RQ examines confidence trajectories for schema-based item categories using IRT-derived ability estimates from 5-level Likert confidence ratings (TC_* tags: 0, 0.25, 0.5, 0.75, 1.0). Three congruence levels: Common (i1/i2 - everyday objects), Congruent (i3/i4 - schema-consistent placements), Incongruent (i5/i6 - schema-violating placements). Analysis uses Graded Response Model (GRM) for ordinal data across four test sessions (T1, T2, T3, T4; nominal Days 0, 1, 3, 6). Time variable uses TSVR (actual hours since encoding). N=100 participants x 4 tests x 3 congruence levels = 1200 observations.

**Theoretical Framing:**
Tests whether schema congruence affects metacognitive monitoring of episodic memories. If schema processes influence confidence independently of accuracy (which showed NULL effects in Ch5 5.4.1), this dissociation reveals that subjective experience of remembering diverges from objective memory performance. Congruent items may feel more familiar (higher confidence) even if not better remembered, due to schema-based fluency.

---

## Theoretical Background

**Relevant Theories:**
- **Schema Theory** (Bartlett, 1932; Ghosh & Gilboa, 2014): Pre-existing knowledge structures (schemas) influence both encoding and retrieval of episodic memories. Schema-consistent information is processed more fluently, which may be misattributed to memory strength.
- **Fluency Heuristic** (Kelley & Jacoby, 1996): Processing fluency (ease of retrieval) is used as a metacognitive cue for memory judgments. Schema-congruent items are processed more fluently, leading to higher confidence ratings even when accuracy is equivalent.
- **Dual-Process Theory** (Yonelinas, 2002): Familiarity-based recognition may be enhanced for schema-congruent items (fluent processing feels familiar), while recollection-based memory shows no schema advantage.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
Schema congruence may affect baseline confidence (congruent items feel more familiar at encoding) but NOT confidence decline rate (if Ch5 5.4.1 accuracy null pattern holds). Alternatively, schema-incongruent items may show faster confidence decline if schema violations create less stable memory traces that are also associated with lower metacognitive monitoring quality.

**Literature Gaps:**
Most schema research examines accuracy, not confidence. Dissociation between schema effects on confidence vs accuracy (if confidence shows effects where accuracy does not) would reveal fluency-based metacognitive biases independent of memory strength. VR ecological encoding with real-world schema violations (incongruent object placements) provides novel test case.

---

## Hypothesis

**Primary Hypothesis:**
NULL expected: Schema � Time interaction will be non-significant (p > 0.05), paralleling Ch5 5.4.1 accuracy findings. Congruence level does NOT affect confidence decline rate. Unitized encoding in immersive VR eliminates schema-based differences in forgetting trajectories.

**Secondary Hypotheses:**
Possible main effect of Congruence on baseline confidence (intercept): Congruent items may show HIGHER initial confidence than Common or Incongruent items due to schema-based fluency (feels familiar even at Day 0). Schema-consistent placements may be processed more fluently during encoding, creating subjective sense of "good memory" even if objective accuracy is equivalent.

**Theoretical Rationale:**
Ch5 5.4.1 found NULL schema effects on accuracy trajectories (congruence affected neither baseline nor slope). If confidence parallels accuracy, schema � time interaction should be NULL. However, if fluency heuristic operates independently of actual memory strength, congruent items may show elevated baseline confidence despite equivalent accuracy. This dissociation would reveal metacognitive bias: schema-congruent information FEELS better remembered even when it is NOT objectively better remembered.

**Expected Effect Pattern:**
- **Primary Test:** Schema � Time interaction p > 0.05 (NULL replicating Ch5 5.4.1)
- **Secondary Test:** Congruence main effect on intercept may be significant (p < 0.05) if fluency bias present
- **Post-hoc Contrasts:** If main effect significant, expect Congruent > Common = Incongruent at Day 0
- **Model Convergence:** GRM IRT calibration converges, LMM with random slopes converges
- **Effect Size:** If Congruence main effect present, Cohen's d for Congruent vs Incongruent baseline difference >= 0.30

---

## Memory Domains

**Domains Examined:**

- [ ] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: NOT examined independently in this RQ

- [ ] **Where** (Spatial Location)
  - [ ] `-L-` tags (general location, legacy)
  - [ ] `-U-` tags (pick-up location)
  - [ ] `-D-` tags (put-down location)
  - Disambiguation: NOT examined independently in this RQ

- [ ] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: NOT examined independently in this RQ

**Schema Congruence Factor:**

This RQ examines a DIFFERENT organizational factor than WWW domains:

- [x] **Common** (Everyday Objects)
  - Tag Pattern: `*-i1` or `*-i2`
  - Description: Common household objects (e.g., lamp, phone) placed in typical locations
  - Example: Lamp on desk, phone on table

- [x] **Congruent** (Schema-Consistent Placements)
  - Tag Pattern: `*-i3` or `*-i4`
  - Description: Objects placed in schema-consistent but non-everyday locations
  - Example: Umbrella near door, cooking utensils in kitchen area

- [x] **Incongruent** (Schema-Violating Placements)
  - Tag Pattern: `*-i5` or `*-i6`
  - Description: Objects placed in schema-violating locations
  - Example: Cooking pot in bathroom, umbrella in closet

**Inclusion Rationale:**
All VR interactive paradigm items (IFR, ICR, IRE) are tagged with congruence codes (i1-i6). These tags reflect item placement design: Common items have typical everyday placements, Congruent items have semantically appropriate placements, Incongruent items have schema-violating placements. This RQ tests whether schema congruence affects subjective confidence in remembering.

**Exclusion Rationale:**
Room Free Recall (RFR) and Test-Cued Recall (TCR) items excluded (no confidence ratings collected for room-level memory). Recognition paradigm (RRE) excluded (different item structure). Only IFR, ICR, IRE items with TC_* confidence ratings included.

---

## Analysis Approach

**Analysis Type:**
IRT (Item Response Theory) for ability estimation using Graded Response Model (GRM) for 5-category ordinal confidence data + LMM (Linear Mixed Models) for trajectory modeling with Schema � Time interaction

**High-Level Workflow:**

**Step 0:** Extract VR data from dfData.csv, filter to TC_* confidence items with congruence tags (i1-i6 patterns), create omnibus dataset with three schema factors (Common, Congruent, Incongruent)

**Step 1:** IRT Pass 1 calibration with 3-factor GRM (Common/Congruent/Incongruent factors) on all items, using p1_med prior. GRM used for 5-category ordinal data (0, 0.25, 0.5, 0.75, 1.0), NOT 2PL binary model.

**Step 2:** Item purification (Decision D039): exclude items with |b| > 3.0 OR a < 0.4 (same criteria as Ch5, applied separately per factor)

**Step 3:** IRT Pass 2 re-calibration on purified items using 3-factor GRM, estimate theta_confidence scores per congruence level per participant per test

**Step 4:** Merge theta scores with TSVR time variable, create time transformations (if needed based on RQ 6.1.1 functional form selection)

**Step 5:** Fit LMM with Congruence � Time interaction, random slopes by UID. Test primary hypothesis: Congruence � Time interaction. Test secondary hypothesis: Congruence main effect (baseline differences).

**Step 6:** Post-hoc contrasts if Congruence effects detected: Congruent vs Common, Congruent vs Incongruent, Common vs Incongruent. **Multiple testing correction:** Apply Bonferroni correction for 3 pairwise contrasts (alpha = 0.05/3 = 0.017) OR use Holm-Bonferroni sequential procedure for improved power while maintaining familywise error rate

**Step 7:** Compare results to Ch5 5.4.1 accuracy findings (document NULL replication or divergence)

**Expected Outputs:**
- data/step00_irt_input.csv (IRT input format, 3 factors)
- data/step00_tsvr_mapping.csv (time variable mapping)
- data/step00_q_matrix.csv (3-factor Q-matrix: Common/Congruent/Incongruent)
- data/step02_purified_items.csv (purified item list per factor, expect 30-70% retention)
- data/step03_theta_confidence_congruence.csv (1200 rows: 100 participants x 4 tests x 3 congruence levels)
- data/step04_lmm_input.csv (1200 rows with time transformations)
- results/step05_lmm_summary.txt (LMM output with Congruence � Time interaction test)
- results/step06_congruence_contrasts.csv (post-hoc pairwise comparisons if effects detected)
- results/step07_ch5_comparison.csv (comparison to Ch5 5.4.1 accuracy pattern)

**Success Criteria:**
- IRT convergence: theta_confidence in [-4,4], SE in [0.1,1.5]
- GRM calibration for 5-category ordinal data (NOT 2PL binary)
- Item purification: 30-70% retention per factor
- 1200 observations generated (100 participants x 4 tests x 3 congruence levels)
- LMM converges with random slopes
- Congruence � Time interaction tested with dual p-values (Decision D068)
- Comparison to Ch5 5.4.1 documented (NULL replication or divergence noted)
- If effects detected: post-hoc contrasts computed with Bonferroni correction (alpha = 0.017 for 3 contrasts)
- **Multiple testing strategy documented:** Report both uncorrected and corrected p-values, specify correction method used (Bonferroni or Holm-Bonferroni)
- Plot data prepared for visualization

---

## Data Source

**Data Type:**
RAW (extracts directly from dfData.csv)

### RAW Data Extraction:

**Source File:**
data/cache/dfData.csv

**Tag Patterns:**
- Confidence items: TC_* (5-level Likert scale: 0, 0.25, 0.5, 0.75, 1.0)
- Congruence tags embedded in item names:
  - Common: `*-i1` or `*-i2` patterns
  - Congruent: `*-i3` or `*-i4` patterns
  - Incongruent: `*-i5` or `*-i6` patterns
- Interactive paradigms only: IFR, ICR, IRE (excludes RFR, TCR, RRE)

**Extraction Method:**
Step 0 extracts from dfData.csv, filtering to:
1. TC_* columns (confidence ratings, 5-category ordinal)
2. Items with i1-i6 congruence tags in item names
3. Interactive paradigms (IFR, ICR, IRE) only

Creates three output files:
- data/step00_irt_input.csv (wide format with ordinal responses 0-4 representing 5 Likert levels)
- data/step00_tsvr_mapping.csv (UID x TEST time mapping)
- data/step00_q_matrix.csv (3 factors: Common items load on Factor 1, Congruent on Factor 2, Incongruent on Factor 3)

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions)

**Items:**
- [x] Interactive paradigms only (IFR, ICR, IRE)
- [x] TC_* confidence items (5-level Likert)
- [x] Items with i1-i6 congruence tags
- [ ] Room Free Recall (RFR) - EXCLUDED (no TC_* ratings)
- [ ] Test-Cued Recall (TCR) - EXCLUDED (no TC_* ratings)
- [ ] Recognition paradigm (RRE) - EXCLUDED (different structure)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4)
- Time variable: TSVR (actual hours since encoding), NOT nominal days

**Critical Note:**
This is a ROOT RQ for schema confidence analysis (extracts from RAW data). Confidence items use 5-level Likert scale (TC_* tags), requiring GRM (Graded Response Model) instead of 2PL binary IRT model used for accuracy (TQ_* tags in Ch5).

---
