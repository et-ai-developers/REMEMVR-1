# RQ 5.4.8: Congruence × Item Difficulty Interaction

**Chapter:** 5
**Type:** Congruence
**Subtype:** Congruence × Item Difficulty Interaction
**Full ID:** 5.4.8

---

## Research Question

**Primary Question:**
Do easier items show faster forgetting than harder items, and does this interaction differ by schema congruence level (Common, Congruent, Incongruent)?

**Scope:**
This RQ examines item-level forgetting trajectories using crossed random effects analysis. Data structure: N=100 participants × 4 test sessions × ~60-80 items (post-purification from RQ 5.4.1) = ~24,000-32,000 item-level response observations. Analysis tests whether the relationship between item difficulty (IRT difficulty parameter b) and forgetting rate varies across three schema congruence categories. Time variable uses TSVR (actual hours since encoding). Item difficulty quantified as IRT difficulty parameter from RQ 5.4.1 Pass 2 calibration.

**Theoretical Framing:**
This is an exploratory analysis examining whether schema congruence moderates the item difficulty × forgetting interaction. If easier items show faster forgetting (consistent with initial strength hypothesis), this effect may be strongest for incongruent items where schema support is absent. Alternatively, the difficulty effect may be minimal for congruent items where schema provides retrieval scaffolding regardless of item-specific difficulty. This RQ extends individual-level congruence effects (RQ 5.4.1, 5.4.2) to item-level variance, testing whether schema effects operate uniformly across difficulty ranges or interact with item-specific characteristics.

---

## Theoretical Background

**Relevant Theories:**

- **Schema Theory (Bartlett, 1932; Alba & Hasher, 1983):** Schema-congruent information is better remembered because it fits existing knowledge structures, providing retrieval cues and organizational support. Schema incongruence creates encoding/retrieval obstacles, potentially amplified for difficult items.

- **Initial Strength Hypothesis (Slamecka & McElree, 1983; Lohnas & Kahana, 2013):** Easier items (lower difficulty) may reflect weaker initial encoding, leading to faster forgetting compared to harder items which require deeper processing. This predicts a positive difficulty × time interaction (easier items show steeper forgetting slopes).

- **Levels of Processing (Craik & Lockhart, 1972):** Difficulty may correlate with processing depth. Harder items requiring more effortful encoding may show more durable memory traces. Schema congruence may reduce this effect by providing automatic organizational support.

- **Dual-Process Theory (Yonelinas, 2002):** Schema-congruent items may rely more on familiarity (gist-based retrieval), making difficulty less relevant. Incongruent items require recollection (item-specific retrieval), amplifying difficulty effects.

**Key Citations:**
[To be added by rq_scholar agent during validation]

**Theoretical Predictions:**

Competing predictions exist:

1. **Stronger difficulty effect for incongruent items:** Schema incongruence removes organizational scaffolding, making item-specific difficulty more critical. Easy incongruent items (weakly encoded + no schema support) show fastest forgetting.

2. **Minimal difficulty effect for congruent items:** Schema congruence provides retrieval support regardless of item difficulty, attenuating the difficulty × time interaction.

3. **Uniform difficulty effect:** Item difficulty operates independently of schema processes, showing similar interactions across all congruence levels.

This RQ does not make a directional prediction but tests which pattern emerges.

**Literature Gaps:**
Most schema research examines congruence main effects, not interactions with item-level psychometric properties. IRT difficulty parameters provide precise, standardized difficulty quantification unavailable in prior schema literature. This RQ bridges psychometric modeling (IRT) with schema theory, testing whether schema effects are uniform across difficulty distributions or concentrated at specific difficulty ranges.

---

## Hypothesis

**Primary Hypothesis:**
Exploratory analysis. No directional prediction. Tests whether the Time × Difficulty interaction differs across Common, Congruent, and Incongruent schema conditions. Primary test: 3-way Time × Difficulty_c × Congruence interaction significant at Bonferroni alpha = 0.0033 (15 pairwise comparisons across workflow).

**Secondary Hypotheses:**
If 3-way interaction is significant, post-hoc tests will determine:
- Which congruence level(s) show significant Time × Difficulty_c interactions
- Whether interaction direction is consistent (positive = easier items forget faster) or varies by congruence
- Whether congruence ordering (Common < Congruent < Incongruent) applies uniformly across difficulty ranges

**Theoretical Rationale:**
Schema theory predicts congruence modulates forgetting rates (RQ 5.4.1, 5.4.2). Initial strength hypothesis predicts difficulty modulates forgetting rates. This RQ tests whether these two factors interact. If schema provides retrieval scaffolding that compensates for weak encoding (low difficulty), the difficulty effect should be attenuated for congruent items. If schema incongruence amplifies encoding/retrieval obstacles, difficulty effects should be strongest for incongruent items.

**Expected Effect Pattern:**

- **Model convergence:** Cross-classified LMM (participants × items) with 3-way interaction converges without singularity warnings
- **Interaction term:** Time × Difficulty_c × Congruence interaction p-value (with Bonferroni correction alpha = 0.0033)
- **Congruence-stratified slopes:** Extract Time × Difficulty_c interaction coefficient for each congruence level separately; compare magnitudes and directions
- **Plot validation:** 6-line trajectory plot (2 difficulty levels [easy = -1SD, hard = +1SD] × 3 congruence levels) shows divergence pattern consistent with interaction statistics

**Interpretation Criteria:**
- Significant 3-way interaction (p < 0.0033) with congruence-specific difficulty effects -> schema moderates difficulty-forgetting relationship
- Non-significant 3-way interaction -> difficulty and schema operate independently
- Post-hoc pattern determines theoretical mechanism (incongruent amplification vs congruent attenuation)

---

## Memory Domains

**Domains Examined:**

This RQ uses schema congruence categories, not WWW memory domains. Schema congruence is orthogonal to domain structure.

**Schema Congruence Categories:**

- [x] **Common** (Schema-Neutral Items)
  - Tag Code: `*-i1`, `*-i2`
  - Description: Items present across all 3 room types (Kitchen, Office, Bathroom), providing no schema-diagnostic information
  - Example: Lamp (present in all rooms)

- [x] **Congruent** (Schema-Consistent Items)
  - Tag Code: `*-i3`, `*-i4`
  - Description: Items matching room schema (e.g., Stove in Kitchen, Desk in Office)
  - Example: Stove in Kitchen, Bathtub in Bathroom

- [x] **Incongruent** (Schema-Violating Items)
  - Tag Code: `*-i5`, `*-i6`
  - Description: Items violating room schema (e.g., Bathtub in Kitchen)
  - Example: Stove in Bathroom, Bathtub in Office

**Inclusion Rationale:**
All three congruence levels must be included to test the 3-way interaction hypothesis. The RQ examines whether the difficulty × time relationship differs across these schema conditions. Item-level analysis uses IRT difficulty parameters from RQ 5.4.1, which performed separate calibrations for Common, Congruent, and Incongruent factors.

**Exclusion Rationale:**
- WWW domains (What/Where/When) are not the focus of this RQ; schema congruence is the grouping variable
- Paradigm categories (Free/Cued/Recognition) are implicitly included (interactive paradigms: IFR, ICR, IRE) as inherited from RQ 5.4.1
- RFR, TCR, RRE paradigms excluded (non-interactive; not part of RQ 5.4.1 analysis chain)

**Item Difficulty Operationalization:**
Item difficulty quantified as IRT difficulty parameter (b) from RQ 5.4.1 Pass 2 calibration. Difficulty is grand-mean centered (Difficulty_c) to facilitate interaction interpretation. Participants with extreme difficulty values or items with extreme parameters are retained (no further purification beyond RQ 5.4.1's item exclusions based on a >= 0.4, |b| <= 3.0 criteria).

---

## Analysis Approach

**Analysis Type:**
Cross-classified Linear Mixed Model (LMM) with item-level responses as dependent variable. Crossed random effects for participants (UID) and items (ItemID). Primary method: pymer4 package for crossed random effects support in Python (alternative: lme4 in R if Python implementation encounters convergence issues).

**High-Level Workflow:**

**Step 1:** Load item parameters from RQ 5.4.1
- Source: `results/ch5/5.4.1/data/step03_item_parameters.csv` (Post-purification IRT parameters)
- Extract: ItemID, Congruence, Difficulty (b parameter), Discrimination (a parameter)
- Validate: 60-80 items retained after RQ 5.4.1 purification, all items have valid difficulty estimates

**Step 2:** Load raw response data and merge with item difficulty
- Source: `data/cache/dfData.csv` (raw binary responses for VR items)
- Filter: Retain only items present in RQ 5.4.1 purified item set
- Structure: Long format (UID × Test × ItemID), binary response (0/1)
- Merge: Join item difficulty and congruence onto response-level data
- Validate: ~24,000-32,000 response observations (100 participants × 4 tests × 60-80 items)

**Step 3:** Prepare analysis variables
- Time: Load TSVR mapping from RQ 5.4.1 (`results/ch5/5.4.1/data/step00_tsvr_mapping.csv`); merge TSVR_hours onto response data
- Difficulty centering: Grand-mean center difficulty (Difficulty_c = Difficulty - mean(Difficulty)); verify mean(Difficulty_c) ~ 0
- Congruence coding: Categorical factor (Common, Congruent, Incongruent); set reference level = Common
- Validate: No missing values in Time, Difficulty_c, Congruence, Response

**Step 4:** Fit cross-classified LMM with 3-way interaction
- Formula: `Response ~ Time × Difficulty_c × Congruence + (Time | UID) + (1 | ItemID)`
- Estimation: Use pymer4.Lmer (wraps lme4 via rpy2) for crossed random effects
- Random effects: By-participant random slopes for Time; by-item random intercepts only (item difficulty is item-level predictor, cannot have random slope)
- Convergence: Check model.converged, singularity warnings, variance component positivity
- If convergence fails: Simplify random effects to (1 | UID) + (1 | ItemID) and re-fit

**Step 5:** Extract 3-way interaction and congruence-stratified difficulty effects
- Primary test: Time × Difficulty_c × Congruence interaction term
- Bonferroni correction: alpha = 0.05 / 15 comparisons = 0.0033 (15 = all pairwise tests across workflow steps)
- Report dual p-values (Decision D068): p_uncorrected and p_bonferroni
- Congruence-stratified models: Fit separate models for Common, Congruent, Incongruent to extract Time × Difficulty_c interaction per level
- Compare interaction magnitudes: Test whether slopes differ across congruence levels

**Step 6:** Prepare trajectory plot data
- Difficulty levels: Easy (-1SD below mean difficulty), Hard (+1SD above mean difficulty)
- Congruence levels: Common, Congruent, Incongruent
- Time points: T1 (Day 0), T2 (Day 1), T3 (Day 3), T4 (Day 6) using actual TSVR means
- Generate predicted probabilities: 2 difficulty × 3 congruence × 4 timepoints = 24 predicted values
- Include confidence intervals (95% CI)
- Validate: Predicted probabilities in [0, 1], no NaN values

**Expected Outputs:**

- `data/step00_item_difficulty_by_congruence.csv`: Item parameters with congruence labels (~60-80 rows, columns: ItemID, Congruence, Difficulty, Discrimination)
- `data/step01_response_level_data.csv`: Raw response data in long format (~24,000-32,000 rows, columns: UID, Test, ItemID, Response, TSVR_hours)
- `data/step02_merged_data.csv`: Response data merged with item difficulty (~24,000-32,000 rows, added columns: Difficulty, Difficulty_c, Congruence)
- `results/step03_lmm_model_summary.txt`: Full model output including fixed effects table, random effects variance components, convergence diagnostics
- `results/step03_difficulty_congruence_interaction.csv`: 3-way interaction term with coefficient, SE, z-value, p_uncorrected, p_bonferroni (1 row)
- `results/step04_congruence_stratified_slopes.csv`: Time × Difficulty_c interaction coefficient per congruence level (3 rows: Common, Congruent, Incongruent)
- `plots/step04_difficulty_trajectories_by_congruence.png`: 6-line plot (2 difficulty × 3 congruence)
- `plots/step04_difficulty_trajectories_by_congruence_data.csv`: Plot source data (24 rows: 2 difficulty × 3 congruence × 4 timepoints, columns: Congruence, Difficulty_Level, Time, Predicted_Probability, CI_lower, CI_upper)

**Success Criteria:**

- **Model convergence:** pymer4 model converges without singularity warnings; if convergence fails with random slopes, simplified model (random intercepts only) converges
- **Difficulty centering:** Difficulty_c mean within ±0.01 of zero
- **Congruence-stratified interactions extracted:** 3 interaction coefficients (one per congruence level) with valid SE and p-values
- **Dual p-values reported:** Both p_uncorrected and p_bonferroni present for 3-way interaction (Decision D068 compliance)
- **Plot validation:** 6 distinct trajectories visible; if interaction significant, trajectories show divergence (easy vs hard items separate over time); if interaction non-significant, trajectories parallel
- **Predicted probabilities valid:** All values in [0, 1], no NaN or infinite values
- **Replicability:** Results replicate with same data inputs (no random seed dependency beyond model initialization)

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.4.1 outputs) combined with RAW (item-level response data from dfData.csv)

### DERIVED Data Source:

**Source RQ:**
RQ 5.4.1 (Schema-Specific Trajectories)

**File Paths:**
- `results/ch5/5.4.1/data/step03_item_parameters.csv`: IRT item parameters (difficulty b, discrimination a) from Pass 2 calibration on purified items; includes ItemID and Congruence labels
- `results/ch5/5.4.1/data/step02_purified_items.csv`: List of retained items after Decision D039 purification (a >= 0.4, |b| <= 3.0); used to filter raw response data
- `results/ch5/5.4.1/data/step00_tsvr_mapping.csv`: Time mapping (UID, Test, TSVR_hours) for merging actual time-since-encoding onto response data

**Dependencies:**
RQ 5.4.1 must complete through Step 3 (IRT Pass 2 calibration) before this RQ can run. Specifically:
- Step 2: Item purification completed, `step02_purified_items.csv` exists with 60-80 items
- Step 3: IRT Pass 2 re-calibration on purified items completed, `step03_item_parameters.csv` exists with valid difficulty (b) and discrimination (a) estimates

If RQ 5.4.1 has not completed these steps, this RQ cannot proceed (circuit breaker: EXPECTATIONS ERROR).

### RAW Data Source:

**Source File:**
`data/cache/dfData.csv`

**Tag Patterns:**
- Congruence tags: `*-i1`, `*-i2` (Common), `*-i3`, `*-i4` (Congruent), `*-i5`, `*-i6` (Incongruent)
- Paradigm codes: IFR, ICR, IRE (interactive paradigms; RFR, TCR, RRE excluded as in RQ 5.4.1)
- Response coding: TQ < 1 -> 0 (incorrect), TQ >= 1 -> 1 (correct) [dichotomization inherited from RQ 5.4.1]

**Extraction Method:**
Step 1 filters dfData.csv to retain only items present in RQ 5.4.1's purified item set. Response data extracted in long format (one row per UID × Test × ItemID combination). TSVR_hours merged from RQ 5.4.1's time mapping file. Item difficulty and congruence merged from RQ 5.4.1's item parameters file.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions; inherited from RQ 5.4.1)

**Items:**
- [x] Only items retained after RQ 5.4.1 purification (a >= 0.4, |b| <= 3.0)
- Expected: 60-80 items across 3 congruence categories (20-27 items per category)
- [ ] Items excluded by RQ 5.4.1 purification (removed due to poor discrimination or extreme difficulty)

**Tests:**
- [x] All 4 test sessions (T1, T2, T3, T4; Days 0, 1, 3, 6)
- Time variable: TSVR_hours (actual hours since encoding, accounts for individual variation in test timing)

**Paradigms:**
- [x] Interactive paradigms only (IFR, ICR, IRE; inherited from RQ 5.4.1)
- [ ] Room Free Recall (RFR), Total Cued Recall (TCR), Room Recognition (RRE) excluded

**Response Format:**
- Binary responses (0 = incorrect, 1 = correct)
- Dichotomization: TQ < 1 -> 0, TQ >= 1 -> 1 (inherited from RQ 5.4.1 Step 0)

---
