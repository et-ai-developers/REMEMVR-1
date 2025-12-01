# RQ 5.3.9: Paradigm × Item Difficulty Interaction

**Chapter:** 5
**Type:** Paradigms
**Subtype:** Paradigm × Item Difficulty Interaction
**Full ID:** 5.3.9

---

## Research Question

**Primary Question:**
Do easier items show faster forgetting than harder items, and does this differ by retrieval paradigm (Free Recall, Cued Recall, Recognition)?

**Scope:**
This RQ examines item-level response data from N=100 participants across 4 test sessions (T1, T2, T3, T4) using crossed random effects design (UID × Item). Analyzes how item difficulty (derived from IRT calibration in RQ 5.3.1) interacts with time and paradigm type (IFR = Item Free Recall, ICR = Item Cued Recall, IRE = Item Recognition) to predict forgetting trajectories. Uses TSVR (actual hours since encoding) as time variable.

**Theoretical Framing:**
Exploratory analysis testing whether the relationship between item difficulty and forgetting rate varies by retrieval support level. Recognition may show strongest difficulty effects due to item-dependent familiarity processes, while Free Recall's self-initiated retrieval may attenuate difficulty effects.

---

## Theoretical Background

**Relevant Theories:**

- **Dual-Process Theory (Yonelinas, 2002):** Recognition memory can rely on both familiarity (fast, automatic, item-dependent) and recollection (slow, effortful). Familiarity processes may show stronger item difficulty effects than recollection-based retrieval.

- **Retrieval Support Hypothesis:** Free Recall requires self-initiated retrieval (minimal external cues), Cued Recall provides partial retrieval support (category cues), and Recognition provides maximal support (item-specific probes). These paradigms may interact differently with item characteristics.

- **Initial Strength Predicts Decay:** Items with lower difficulty (higher endorsement probability) may represent weaker encoding and show faster forgetting. However, this relationship may be moderated by retrieval paradigm.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**

From hypothesis: Recognition paradigm may show strongest difficulty × time interaction because familiarity-based recognition is more item-dependent than recollection-based free recall. Competing predictions exist: (1) easier items = weaker encoding -> faster forgetting (positive interaction), (2) easier items = ceiling effects -> slower apparent forgetting (negative interaction), (3) no interaction (difficulty affects intercept only, uniform across paradigms).

**Literature Gaps:**
[To be identified by rq_scholar - specifically regarding paradigm-dependent item difficulty effects in longitudinal forgetting studies]

---

## Hypothesis

**Primary Hypothesis:**
Exploratory analysis with no directional prediction. Tests whether item difficulty × time interaction differs across Free Recall, Cued Recall, and Recognition paradigms using 3-way interaction term: Time × Difficulty_c × paradigm.

**Secondary Hypotheses:**
Recognition paradigm may show strongest difficulty effect (largest coefficient magnitude for Time × Difficulty_c interaction within Recognition) because recognition memory relies more heavily on item-specific familiarity processes compared to self-initiated retrieval in Free Recall.

**Theoretical Rationale:**
If item difficulty effects reflect encoding strength, all paradigms should show similar difficulty × time interactions. However, if difficulty effects reflect retrieval process characteristics, paradigms may differ: Recognition (familiarity-based) may be more item-dependent than Free Recall (recollection-based), leading to paradigm-stratified difficulty × time interactions.

**Expected Effect Pattern:**
3-way interaction (Time × Difficulty_c × paradigm) tested at Bonferroni-corrected alpha = 0.0033 (family-wise error rate across related RQ analyses). If significant, follow-up analysis will extract paradigm-specific difficulty × time slopes and compare magnitudes. Plot will show 6 trajectories (2 difficulty levels [easy = -1SD, hard = +1SD] × 3 paradigms).

---

## Memory Domains

**Domains Examined:**

- [x] **All Paradigms Combined** (analyzed separately by paradigm)
  - Paradigm Codes: IFR (Item Free Recall), ICR (Item Cued Recall), IRE (Item Recognition)
  - Description: Three retrieval paradigms differing in retrieval support level

**Paradigm Details:**

- [x] **IFR (Item Free Recall)**
  - Tag Pattern: Items with IFR paradigm code
  - Description: Self-initiated retrieval with minimal external support

- [x] **ICR (Item Cued Recall)**
  - Tag Pattern: Items with ICR paradigm code
  - Description: Category-cued retrieval with partial external support

- [x] **IRE (Item Recognition)**
  - Tag Pattern: Items with IRE paradigm code
  - Description: Item-specific probe with maximal external support

**Inclusion Rationale:**
Analyzes all three interactive paradigms to test whether item difficulty effects on forgetting rate vary by retrieval support level. Excludes room-level paradigms (RFR, TCR, RRE) which use different item structures.

**Exclusion Rationale:**
- Room Free Recall (RFR), Room Cued Recall (TCR), Room Recognition (RRE): Excluded because they assess room-level memory (different item structure from object-level interactive paradigms)
- What/Where/When domain decomposition not applicable (RQ analyzes paradigm effects, not domain effects)

---

## Analysis Approach

**Analysis Type:**
Cross-classified Linear Mixed Model (LMM) with crossed random effects for participants (UID) and items (Item). Tests 3-way interaction: Time × Difficulty_c × paradigm.

**High-Level Workflow:**

**Step 1:** Load item parameters from RQ 5.3.1 (data/step03_item_parameters.csv contains IRT-derived difficulty estimates per item)

**Step 2:** Load raw response data from data/cache/dfData.csv in long format (one row per UID × Test × Item observation). Merge item difficulty and paradigm assignment into response-level data.

**Step 3:** Grand-mean center item difficulty variable (Difficulty_c = Difficulty - mean[Difficulty]). Verify centering: mean(Difficulty_c) ~ 0. Create time variable from TSVR mapping (actual hours since encoding).

**Step 4:** Fit cross-classified LMM using pymer4 (supports crossed random effects):
```
Response ~ Time × Difficulty_c × paradigm + (Time | UID) + (1 | Item)
```

Fixed effects: Time, Difficulty_c, paradigm (3 levels: IFR/ICR/IRE), all 2-way interactions, and 3-way interaction (Time × Difficulty_c × paradigm). Random effects: random intercepts and slopes for Time by participant (UID), random intercepts by item (Item).

**Step 5:** Extract 3-way interaction terms (Time × Difficulty_c × paradigm). Test significance at Bonferroni alpha = 0.0033 (conservative threshold for family-wise error correction). Report dual p-values per Decision D068 (both uncorrected and Bonferroni-corrected).

**Step 6:** Create plot data for 6 trajectories: Easy items (-1SD difficulty) vs Hard items (+1SD difficulty) for each of 3 paradigms (IFR, ICR, IRE). Generate predicted forgetting curves from fitted model at Days 0, 1, 3, 6.

**Expected Outputs:**

- data/step00_item_difficulty_by_paradigm.csv (item-level difficulty estimates stratified by paradigm)
- data/step01_response_level_data.csv (long format: UID × Test × Item observations with response, time, difficulty, paradigm)
- data/step02_merged_data.csv (Step 1 data merged with difficulty and paradigm)
- results/step03_lmm_model_summary.txt (full model output from pymer4)
- results/step03_difficulty_paradigm_interaction.csv (3-way interaction coefficients, SE, z-values, dual p-values)
- plots/step04_difficulty_trajectories_by_paradigm.png (6 trajectories: 2 difficulty × 3 paradigms)
- plots/step04_difficulty_trajectories_by_paradigm_data.csv (plot source data)

**Success Criteria:**

- Model convergence: pymer4 model converges successfully (model.converged = True)
- Crossed random effects: Both (Time | UID) and (1 | Item) variance components positive and identifiable
- Difficulty centering: mean(Difficulty_c) within ±0.01 of zero
- 3-way interaction extracted: Time × Difficulty_c × paradigm terms present in fixed effects output with valid SE and p-values
- Paradigm-stratified interactions: If 3-way interaction significant, paradigm-specific difficulty × time slopes extracted and interpretable
- Dual p-values: Both p_uncorrected and p_bonferroni reported per Decision D068
- Plot data structure: 6 rows minimum (2 difficulty levels × 3 paradigms), each with 4 timepoints (Days 0, 1, 3, 6)
- Plot interpretability: Trajectories show clear divergence (if significant) or parallelism (if non-significant) between easy and hard items within each paradigm

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.3.1 item parameters) + RAW (response-level data from dfData.csv)

### DERIVED Data Source:

**Source RQ:**
RQ 5.3.1 (Paradigm-Specific Trajectories)

**File Paths:**
- results/ch5/5.3.1/data/step03_item_parameters.csv (IRT-derived difficulty estimates per item, post-purification)
- results/ch5/5.3.1/data/step00_tsvr_mapping.csv (TSVR time mapping: UID × Test -> actual hours since encoding)

**Dependencies:**
RQ 5.3.1 must complete Step 3 (IRT Pass 2 calibration on purified items) to generate item difficulty parameters. Item parameters required before this RQ can merge difficulty into response-level data.

### RAW Data Source:

**Source File:**
data/cache/dfData.csv

**Tag Patterns:**
- Paradigm codes: IFR (Item Free Recall), ICR (Item Cued Recall), IRE (Item Recognition)
- Excludes: RFR, TCR, RRE (room-level paradigms with different item structure)

**Extraction Method:**
Extract raw binary responses (0/1) at item level from dfData.csv in long format. Each row = one observation (UID × Test × Item). Merge with item difficulty from RQ 5.3.1 and paradigm assignment to create analysis-ready dataset.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions, inherited from RQ 5.3.1)

**Items:**
- [x] Only items retained after IRT purification in RQ 5.3.1 (typically 40-80 items post-purification per Decision D039: a >= 0.4, |b| <= 3.0)
- [ ] Items removed during RQ 5.3.1 purification - EXCLUDED (poor psychometric properties)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4) corresponding to nominal Days 0, 1, 3, 6 (actual time via TSVR mapping)

**Paradigms:**
- [x] IFR (Item Free Recall)
- [x] ICR (Item Cued Recall)
- [x] IRE (Item Recognition)
- [ ] RFR, TCR, RRE (room-level paradigms) - EXCLUDED (different item structure)

---
