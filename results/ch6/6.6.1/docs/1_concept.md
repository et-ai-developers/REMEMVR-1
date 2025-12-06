# RQ 6.6.1: High-Confidence Errors Over Time

**Chapter:** 6
**Type:** HCE (High-Confidence Errors)
**Subtype:** Over Time
**Full ID:** 6.6.1

---

## Research Question

**Primary Question:**
Do high-confidence errors (HCE: Confidence >= 0.75 AND Accuracy = 0) increase from Day 0 to Day 6?

**Scope:**
This RQ examines high-confidence error rates across a 6-day retention interval using item-level data from N=100 participants × 4 test sessions × ~68 items = ~27,200 item-responses. Each item has paired confidence (TC_* tags, 5-level Likert: 0, 0.25, 0.5, 0.75, 1.0) and accuracy (TQ_* tags, dichotomous correct/incorrect) data. HCE rate computed per participant per timepoint (T1, T2, T3, T4; nominal Days 0, 1, 3, 6).

**Theoretical Framing:**
This RQ addresses metacognitive failure: the dissociation between memory quality and subjective confidence. As memories degrade over time, metacognitive monitoring may not fully adjust, leading to increased high-confidence errors. This reflects both memory distortion (inaccurate memory traces) and metacognitive failure (confidence does not track accuracy decline). HCE is a critical metric for real-world memory function where overconfidence in false memories has practical consequences.

---

## Theoretical Background

**Relevant Theories:**
- **Metacognitive Monitoring Theory** (Nelson & Narens, 1990): Memory system includes both object-level (memory traces) and meta-level (monitoring of memory quality). HCE reflects failures at the meta-level - the monitoring system does not accurately track object-level degradation.
- **Memory Distortion Theory** (Schacter, 1999): As memory traces decay, they become susceptible to reconstruction errors and schema-based intrusions. Combined with maintained confidence, this produces high-confidence false memories.
- **Signal Detection Framework**: Confidence reflects decision criterion placement. High-confidence errors occur when liberal criterion placement combines with noisy memory signals. Over time, signal degradation may not shift criterion appropriately.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
If memories degrade faster than metacognitive monitoring adjusts, HCE rate should INCREASE over time. Alternative: if metacognitive monitoring tracks memory quality accurately, HCE rate remains stable (both accuracy and confidence decline in parallel, maintaining calibration).

**Literature Gaps:**
Most HCE research examines single timepoints or immediate/delayed dichotomy. Few studies track HCE trajectories across multiple retention intervals in the same participants, particularly in ecologically valid VR episodic memory.

---

## Hypothesis

**Primary Hypothesis:**
High-confidence errors (HCE rate) may INCREASE over time as memories degrade but confidence doesn't fully adjust. This reflects memory distortion (inaccurate traces) combined with metacognitive failure (confidence not tracking accuracy decline). Expected: significant positive Time effect on HCE rate (p < 0.05).

**Secondary Hypotheses:**
None specified - primary focus is on detecting Time effect on HCE rate.

**Theoretical Rationale:**
Memory traces degrade continuously from encoding to Day 6. If metacognitive monitoring lags behind this degradation, participants will maintain higher confidence than warranted by actual memory quality. This dissociation manifests as increased HCE rate over time. The 5-level confidence scale provides granular measurement of subjective certainty, allowing detection of high-confidence (>= 0.75) responses that are incorrect.

**Expected Effect Pattern:**
Significant positive Time effect on HCE rate (dual p-values per Decision D068). HCE rate should increase monotonically from Day 0 to Day 6, or show two-phase pattern (stable early, increasing late) if metacognitive monitoring adapts during initial consolidation but fails during long-term retention.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object identity items with paired confidence (TC_*-N-*) and accuracy (TQ_*-N-*) data

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location, legacy)
  - [x] `-U-` tags (pick-up location/source)
  - [x] `-D-` tags (put-down location/destination)
  - Disambiguation: All Where tags included (legacy -L-, source -U-, destination -D-) with paired confidence and accuracy data

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order items with paired confidence (TC_*-O-*) and accuracy (TQ_*-O-*) data

**Inclusion Rationale:**
All WWW episodic memory domains included (omnibus analysis across all item types). This RQ examines HCE as a general metacognitive phenomenon not specific to any single domain. Domain-specific HCE analysis conducted in RQ 6.6.3.

**Exclusion Rationale:**
None - all interactive paradigm items (IFR, ICR, IRE) included. Room Free Recall (RFR) and Text-based paradigms (TCR, RRE) excluded as they lack VR episodic memory context.

---

## Analysis Approach

**Analysis Type:**
Linear Mixed Model (LMM) for HCE rate trajectories

**High-Level Workflow:**

**Step 0:** Extract item-level data from dfData.csv
- Extract paired TQ_* (accuracy, dichotomous) and TC_* (confidence, 5-level Likert) for all items
- Filter to interactive paradigms (IFR, ICR, IRE)
- Create item-level dataset: ~27,200 rows (100 participants × 4 tests × ~68 items)
- Output: data/step00_item_level.csv

**Step 1:** Compute HCE rate per participant per timepoint
- Define HCE: Confidence >= 0.75 AND Accuracy = 0
- Count HCE instances per participant per test
- Compute HCE_rate = n_HCE / n_total_items per participant per timepoint
- Output: data/step01_hce_rates.csv (400 rows: 100 participants × 4 tests)

**Step 2:** Fit LMM for HCE trajectory
- Model: HCE_rate ~ Time + (Time | UID)
- Time variable: TSVR (hours since encoding) or transformed (log, days)
- Random effects: Random intercepts and slopes by participant (UID)
- Method: REML=True for variance estimation
- Output: results/step02_hce_lmm.txt

**Step 3:** Test Time effect on HCE rate
- Extract Time coefficient and significance
- Report dual p-values (Wald and LRT per Decision D068)
- Interpret: Does HCE rate increase over time?
- Output: results/step03_time_effect.csv

**Step 4:** Compute mean HCE rate by timepoint
- Aggregate HCE_rate by test (T1, T2, T3, T4)
- Compute mean, SE, 95% CI per timepoint
- Prepare plot data for HCE trajectory visualization
- Output: plots/step04_hce_trajectory.csv

**Expected Outputs:**
- data/step00_item_level.csv (~27,200 rows)
- data/step01_hce_rates.csv (400 rows: 100 participants × 4 tests)
- results/step02_hce_lmm.txt (model summary)
- results/step03_time_effect.csv (Time effect test with dual p-values)
- plots/step04_hce_trajectory.csv (mean HCE rate by timepoint for plotting)

**Success Criteria:**
- HCE rate computed correctly (range [0,1], count-based)
- LMM converged successfully
- Time effect tested with dual p-values (Wald and LRT per D068)
- Mean HCE rate computed per timepoint for visualization
- No missing data in HCE_rate variable (all 400 participant-timepoint observations present)

---

## Data Source

**Data Type:**
RAW (extracts directly from dfData.csv)

### RAW Data Extraction:

**Source File:**
data/cache/dfData.csv

**Tag Patterns:**
- Confidence items: TC_* tags (5-level Likert: 0, 0.25, 0.5, 0.75, 1.0)
- Accuracy items: TQ_* tags (dichotomous: 0=incorrect, 1=correct)
- Domain tags: -N- (What), -L-/-U-/-D- (Where), -O- (When)
- Paradigm codes: IFR (Immediate Free Recall), ICR (Immediate Cued Recall), IRE (Immediate Recognition)
- Exclude: RFR (Room Free Recall), TCR (Text Cued Recall), RRE (Text Recognition)

**Extraction Method:**
Step 0 extracts paired confidence-accuracy data from dfData.csv:
1. Filter to TC_* and TQ_* columns (confidence and accuracy items)
2. Filter to interactive paradigms (IFR, ICR, IRE) - exclude RFR, TCR, RRE
3. Reshape to long format: one row per item-response
4. Merge UID, TEST, TSVR metadata
5. Output: data/step00_item_level.csv (~27,200 rows)

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions)
- No participant-level filtering

**Items:**
- [x] All VR episodic memory items with paired TC_*/TQ_* data
- [x] Interactive paradigms only: IFR, ICR, IRE
- [ ] Room Free Recall (RFR) - EXCLUDED (no paired confidence data)
- [ ] Text paradigms (TCR, RRE) - EXCLUDED (not VR episodic memory)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4 / nominal Days 0, 1, 3, 6)
- Time variable: TSVR (actual hours since encoding) used for analysis

**Critical Notes:**
- TC_* items are 5-category ordinal (0, 0.25, 0.5, 0.75, 1.0), NOT dichotomous like TQ_*
- HCE definition: Confidence >= 0.75 (high confidence) AND Accuracy = 0 (incorrect)
- This threshold (0.75) represents top 2 confidence levels (0.75 and 1.0)
- Item-level analysis (~27,200 rows) aggregated to participant-level HCE rates (400 rows) for LMM

---
