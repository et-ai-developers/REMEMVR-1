# RQ 6.5.3: High-Confidence Errors (Schema-Incongruent Effects)

**Chapter:** 6
**Type:** Schema Confidence
**Subtype:** High-Confidence Errors
**Full ID:** 6.5.3

---

## Research Question

**Primary Question:**
Do schema-incongruent items produce more high-confidence errors than schema-congruent or common items?

**Scope:**
This RQ examines high-confidence errors (HCE) at the item level across ~27,200 item-responses (N=100 participants × 4 test sessions × ~68 items). HCE = P(Accuracy=0 | Confidence >= 0.75). Compares HCE rates across three schema congruence levels: Common (items i1/i2), Congruent (items i3/i4), and Incongruent (items i5/i6). Time variable uses TSVR (actual hours since encoding), examining change from Days 0 to 6.

**Theoretical Framing:**
High-confidence errors represent a dissociation between metacognitive judgments (confidence) and actual memory accuracy. Schema-incongruent items may be particularly vulnerable to this dissociation due to schema-based intrusionsparticipants may remember what "should" be there (schema-consistent details) rather than what actually was (schema-violating details), creating a DRM-like effect where false memories feel highly familiar.

---

## Theoretical Background

**Relevant Theories:**
- **Schema Theory** (Bartlett, 1932): Memory encoding and retrieval are influenced by pre-existing cognitive frameworks (schemas). Schema-inconsistent information is more difficult to encode and more vulnerable to distortion during retrieval, as schemas fill in gaps with expected information.
- **DRM Paradigm** (Deese-Roediger-McDermott): False memories for schema-consistent lures can be accompanied by high confidence, demonstrating that familiarity-based processes can create strong but incorrect memory signals.
- **Source Monitoring Framework** (Johnson et al., 1993): High-confidence errors may result from source confusionparticipants may confuse schema-based inferences (internally generated) with actual perceptual experiences (externally sourced).

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
Incongruent items violate room schemas (e.g., a toilet in the kitchen), making them both harder to encode accurately AND more vulnerable to schema-based reconstruction errors during retrieval. When memory trace is weak, participants may retrieve schema-consistent details ("remembering" what should be there), creating false confidence. Congruent and common items should show lower HCE rates because schema-support aids both encoding and retrieval accuracy.

**Literature Gaps:**
Most schema research examines accuracy effects, not confidence dissociations. Few studies have examined high-confidence errors in ecological VR episodic memory with schema manipulations. This RQ tests whether immersive VR can replicate DRM-like confidence-accuracy dissociations using naturalistic room schemas rather than word lists.

---

## Hypothesis

**Primary Hypothesis:**
Incongruent items will produce MORE high-confidence errors than congruent or common items. Expected pattern: HCE_rate_incongruent > HCE_rate_congruent H HCE_rate_common. Statistical test: significant Congruence main effect in LMM predicting HCE rate, with post-hoc contrasts showing incongruent > others.

**Secondary Hypotheses:**
HCE rates may INCREASE over time (Day 0 to Day 6) as memory traces degrade and schema-based reconstruction increases. Expected: Congruence × Time interaction, where incongruent items show steeper HCE rate increase than congruent/common items (faster schema intrusion as memory fades).

**Theoretical Rationale:**
Schema-incongruent items create encoding difficulty (schema violation) combined with retrieval vulnerability (schema fills gaps). When participants encounter weak memory traces, schema-consistent details feel familiar even if incorrect, creating high confidence in wrong answers. This is analogous to DRM false memories, where semantically related lures produce high-confidence false recognitions.

**Expected Effect Pattern:**
- Main effect of Congruence on HCE rate: F(2, df) significant at p < 0.05 (Bonferroni correction if testing multiple contrasts)
- Post-hoc contrast: Incongruent vs (Congruent + Common) significant at p < 0.05
- Possible interaction: Congruence × Time if incongruent HCE rate increases faster over retention interval
- HCE rates expected range: 5-20% (moderate false alarms, as HCE requires BOTH error AND high confidence)

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object identity/naming is the primary domain affected by schema congruence manipulation

- [ ] **Where** (Spatial Location)
  - [ ] `-L-` tags (general location, legacy)
  - [ ] `-U-` tags (pick-up location)
  - [ ] `-D-` tags (put-down location)
  - Disambiguation: Not directly examined in this RQ (focus is on object-schema congruence)

- [ ] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Not examined in this RQ

**Inclusion Rationale:**
Schema congruence is manipulated via object-room fit (What domain). Items are tagged with congruence level:
- **Common items** (i1/i2): Objects expected in ALL room types (e.g., trash can)
- **Congruent items** (i3/i4): Objects expected in SPECIFIC room types (e.g., toilet in bathroom)
- **Incongruent items** (i5/i6): Objects violating room schemas (e.g., toilet in kitchen)

All items are from interactive VR paradigms (IFR, ICR, IRE), as these involve active exploration and encoding. Congruence manipulation is specific to What domain object identity.

**Exclusion Rationale:**
Where and When domains not examined because schema congruence is an object-level manipulation. Spatial and temporal memory are not directly manipulated by schema violations (though they may be correlated with object memory performance).

---

## Analysis Approach

**Analysis Type:**
Item-level analysis of high-confidence errors (HCE) using mixed-effects logistic or linear models

**High-Level Workflow:**

**Step 0:** Extract item-level accuracy (TQ_*) and confidence (TC_*) from dfData.csv for all VR items. Filter to congruence-tagged items (i1/i2/i3/i4/i5/i6). ~27,200 item-responses (100 participants × 4 tests × ~68 items).

**Step 1:** Identify high-confidence errors for each item-response. HCE flag = 1 if (Accuracy=0 AND Confidence >= 0.75), else 0. Confidence threshold of 0.75 corresponds to "4" on 5-point Likert scale (0, 0.25, 0.5, 0.75, 1.0).

**Step 2:** Compute HCE rates per congruence level per timepoint. Aggregate by Congruence (Common/Congruent/Incongruent) × Test (T1/T2/T3/T4). Output: 12 rows (3 congruence levels × 4 tests) with HCE rate = mean(HCE_flag).

**Step 3:** Fit mixed-effects model to test Congruence × Time effect on HCE rate. Model: HCE_flag ~ Congruence × Time + (Time | UID) + (1 | ItemID). Test main effect of Congruence and interaction Congruence × Time.

**Step 4:** Post-hoc comparisons if Congruence effect significant. Contrasts: Incongruent vs Congruent, Incongruent vs Common, Congruent vs Common. Bonferroni correction if multiple contrasts tested.

**Expected Outputs:**
- data/step00_item_level.csv (~27,200 rows: UID, ItemID, Test, TQ_accuracy, TC_confidence, Congruence, TSVR)
- data/step01_hce_flags.csv (~27,200 rows with HCE_flag column added)
- results/step02_hce_rates.csv (12 rows: 3 congruence × 4 tests, mean HCE rate per cell)
- results/step03_congruence_hce_test.csv (Congruence main effect, interaction, post-hoc contrasts with p-values)
- plots/step04_hce_by_congruence.csv (plot data: HCE rate by Congruence × Time, with error bars)

**Success Criteria:**
- Item-level data extraction successful (~27,200 rows, no missing TQ_/TC_ pairs)
- HCE definition correct (Accuracy=0 AND Confidence >= 0.75)
- HCE rates computed per congruence level (12 cells, all non-negative)
- Mixed-effects model converges (random effects for both UID and ItemID)
- Congruence effect tested with appropriate corrections (Bonferroni if multiple comparisons)
- Results interpretable: If incongruent > others, supports schema intrusion hypothesis; if NULL, suggests schema effects do not extend to confidence-accuracy dissociation

---

## Data Source

**Data Type:**
RAW (extracts directly from dfData.csv)

### RAW Data Extraction:

**Source File:**
data/cache/dfData.csv

**Tag Patterns:**
- **Accuracy tags:** TQ_* (dichotomous 0/1 accuracy for all VR items)
- **Confidence tags:** TC_* (5-level Likert: 0, 0.25, 0.5, 0.75, 1.0 for all VR items)
- **Congruence tags:** Items tagged with congruence level (i1/i2 = Common, i3/i4 = Congruent, i5/i6 = Incongruent)
- **Paradigm codes:** IFR, ICR, IRE (interactive VR paradigms only, excludes RFR/TCR/RRE)

**Extraction Method:**
Step 0 extracts item-level raw data from dfData.csv:
1. Filter to VR items with both TQ_* (accuracy) and TC_* (confidence) measurements
2. Extract congruence level from item tags (i1/i2/i3/i4/i5/i6 embedded in column names)
3. Extract test session (T1, T2, T3, T4) and TSVR (hours since encoding)
4. Create long-format item-level dataset: one row per UID × ItemID × Test
5. Output: data/step00_item_level.csv (~27,200 rows)

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions)

**Items:**
- [x] Interactive VR paradigm items only (IFR, ICR, IRE)
- [ ] Room Free Recall (RFR) - EXCLUDED (no congruence tags)
- [ ] Total Cued Recall (TCR) - EXCLUDED (no congruence tags)
- [ ] Room Recognition (RRE) - EXCLUDED (no congruence tags)
- [x] Only items with BOTH TQ_* (accuracy) AND TC_* (confidence) measurements
- [x] Only items with congruence tags (i1/i2/i3/i4/i5/i6)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4; nominal Days 0, 1, 3, 6)

**Note:** This is item-level analysis (NOT IRT-aggregated). Each item-response is analyzed independently to identify HCE dissociations. Total sample size ~27,200 item-responses enables sufficient power to detect HCE rate differences across congruence levels even if HCE is rare (~5-20% base rate expected).

---
