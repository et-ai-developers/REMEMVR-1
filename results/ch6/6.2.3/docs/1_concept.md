# RQ 6.2.3: Resolution Over Time

**Chapter:** 6
**Type:** Calibration
**Subtype:** Resolution Over Time
**Full ID:** 6.2.3

---

## Research Question

**Primary Question:**
Does discrimination ability (resolution/gamma) decline as memory fades over a 6-day retention interval?

**Scope:**
This RQ examines metacognitive resolution - the ability to discriminate remembered from forgotten items - using the Goodman-Kruskal gamma correlation between item-level confidence and accuracy. Analysis uses approximately 68 items × 100 participants × 4 test sessions = 27,200 item-level responses across Days 0, 1, 3, and 6. Resolution is computed per participant per timepoint, then modeled using Linear Mixed Models to test whether discrimination ability declines over time.

**Theoretical Framing:**
As episodic memories degrade, the signal-to-noise ratio decreases. If metacognitive monitoring has access to memory trace strength, resolution (the ability to discriminate strong from weak memories) should decline in parallel with memory fading. However, if metacognition relies on stable heuristics independent of trace strength, resolution may remain constant despite accuracy decline. This RQ tests whether metacognitive discrimination degrades alongside memory.

---

## Theoretical Background

**Relevant Theories:**
- **Signal Detection Theory:** Metacognitive judgments reflect discrimination between signal (correct memories) and noise (incorrect memories or guessing). Resolution is the area under the ROC curve for this discrimination. As memory traces fade, signal strength decreases, potentially reducing discriminability.
- **Cue-Utilization Framework (Koriat, 1997):** Confidence judgments are based on cues such as retrieval fluency, familiarity, and conscious recollection. If these cues become less diagnostic over time (e.g., all items feel equally unfamiliar), resolution should decline.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
If metacognitive monitoring tracks memory trace strength, resolution (gamma) should DECLINE from Day 0 to Day 6 as the signal-to-noise ratio decreases. The threshold gamma > 0.50 represents acceptable discrimination ability. If resolution falls below this threshold, participants can no longer reliably distinguish remembered from forgotten items based on their confidence judgments.

**Literature Gaps:**
Most metacognitive research examines resolution at single timepoints or within-session. This RQ extends resolution analysis across a longitudinal 6-day retention interval, testing whether discrimination ability degrades alongside memory consolidation and forgetting processes.

---

## Hypothesis

**Primary Hypothesis:**
Resolution (Goodman-Kruskal gamma) will DECLINE from Day 0 to Day 6 as memory becomes noisier. Expected pattern: significant negative Time effect on gamma (p < 0.05), indicating reduced discrimination ability over time.

**Secondary Hypotheses:**
Gamma will remain above the 0.50 threshold at all timepoints, indicating that participants retain some discriminative ability even as memories fade. However, the magnitude of gamma may decrease substantially (e.g., from gamma H 0.70 at Day 0 to gamma H 0.55 at Day 6).

**Theoretical Rationale:**
Memory fading reduces the signal-to-noise ratio, making it harder to discriminate strong from weak traces. If confidence judgments are based on trace strength (retrieval fluency, familiarity), resolution should decline. However, if participants use stable heuristics (e.g., "recognition feels easier than recall"), resolution may be more robust than expected.

**Expected Effect Pattern:**
Significant negative Time effect in the LMM (gamma ~ Time + (Time | UID)). Linear or logarithmic decline in mean gamma from Day 0 to Day 6. Gamma remains positive and above 0.50 at all timepoints, but magnitude decreases by 15-30% across the retention interval.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object naming and identity memory

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location, legacy)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Disambiguation: All location tags included (omnibus across all spatial memory types)

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order and sequence memory

**Inclusion Rationale:**
This RQ uses an omnibus "All" approach, aggregating across all memory domains (What, Where, When) to examine overall metacognitive resolution. All interactive paradigm items (IFR, ICR, IRE) are included, regardless of domain, to maximize item-level sample size (approximately 68 items per participant per test session).

**Exclusion Rationale:**
Room Free Recall (RFR), Timed Cued Recall (TCR), and Room Recognition (RRE) paradigms excluded as these do not have paired confidence judgments in the TC_* tag structure.

---

## Analysis Approach

**Analysis Type:**
Item-level correlational analysis (Goodman-Kruskal gamma) followed by Linear Mixed Models (LMM) for trajectory analysis

**High-Level Workflow:**

**Step 0:** Extract item-level data from data/cache/dfData.csv. Filter to interactive paradigm items (IFR, ICR, IRE). Extract both TQ_* tags (dichotomous accuracy: 0/1) and TC_* tags (5-level confidence: 0, 0.25, 0.5, 0.75, 1.0). Create long-format data: UID × TEST × ITEM × Accuracy × Confidence. Expected output: approximately 27,200 item-response rows (68 items × 100 participants × 4 tests).

**Step 1:** Compute Goodman-Kruskal gamma per participant per timepoint. Gamma measures the ordinal correlation between confidence (5 levels) and accuracy (2 levels). Gamma = (Nc - Nd) / (Nc + Nd), where Nc = number of concordant pairs, Nd = number of discordant pairs. Expected output: 400 gamma scores (100 participants × 4 tests).

**Step 2:** Fit Linear Mixed Model to gamma scores. Model specification: gamma ~ Time + (Time | UID), where Time is continuous (TSVR hours transformed to days or log-scaled). Random effects: random intercepts and slopes by participant (UID). Estimation: REML = True (variance estimation). Test whether Time coefficient is significantly negative (resolution declines).

**Step 3:** Extract Time effect statistics. Report coefficient, standard error, t-statistic, and dual p-values (per Decision D068). Test null hypothesis: Time coefficient = 0 (no change in resolution over time). Bonferroni correction if testing multiple time transformations (linear, log).

**Step 4:** Compute mean gamma by timepoint. Descriptive statistics: mean, SD, 95% CI for gamma at each of the 4 test sessions (Days 0, 1, 3, 6). Track whether mean gamma declines monotonically or shows non-linear pattern.

**Step 5:** Test gamma > 0.50 threshold at each timepoint. One-sample t-tests: gamma_mean > 0.50 at T1, T2, T3, T4. Report whether participants maintain acceptable discrimination ability throughout retention interval.

**Step 6:** Prepare plot data for resolution trajectory visualization. Output: mean gamma ± SE by timepoint, individual participant trajectories (spaghetti plot), model-predicted trajectory from LMM.

**Expected Outputs:**
- data/step00_item_level.csv (27,200 rows: UID, TEST, ITEM, Accuracy, Confidence)
- data/step01_gamma_scores.csv (400 rows: UID, TEST, gamma)
- results/step02_gamma_lmm.txt (LMM summary statistics)
- results/step03_time_effect.csv (Time coefficient, SE, t, dual p-values)
- results/step04_mean_gamma.csv (4 rows: mean, SD, 95% CI by timepoint)
- plots/step05_resolution_trajectory.csv (plot-ready data: observed means, model predictions)

**Success Criteria:**
- Item-level data extraction: 27,200 rows (all interactive items × all participants × all tests)
- Gamma computed per person-timepoint: 400 valid gamma scores (no missing values or computational errors)
- LMM convergence: model fit without singularity warnings, random effects variance > 0
- Time effect tested: coefficient estimate with dual p-values reported
- Threshold comparison: gamma > 0.50 tested at each timepoint, results documented
- Plot data complete: trajectory data ready for visualization

---

## Data Source

**Data Type:**
RAW (extracts directly from dfData.csv)

### RAW Data Extraction:

**Source File:**
data/cache/dfData.csv

**Tag Patterns:**
- **Accuracy tags:** TQ_* (dichotomous: 0 = incorrect, 1 = correct)
- **Confidence tags:** TC_* (5-level ordinal: 0, 0.25, 0.5, 0.75, 1.0)
- **Paradigm codes:** Interactive paradigms only (IFR = Immediate Free Recall, ICR = Immediate Cued Recall, IRE = Immediate Recognition)
- **Domain tags:** All domains included (-N-, -L-/-U-/-D-, -O-)

**Extraction Method:**
Step 0 extracts from dfData.csv using tag pattern matching. For each participant (UID) and test session (TEST), extract all item-level responses where both TQ_* and TC_* tags exist. Filter to interactive paradigms (exclude RFR, TCR, RRE). Create long-format data structure: one row per item-response with columns [UID, TEST, ITEM, Accuracy, Confidence]. Expected approximately 68 items per participant per test session.

**Output:**
- data/step00_item_level.csv (27,200 rows in long format)

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions)

**Items:**
- [x] Interactive paradigm items only (IFR, ICR, IRE)
- [ ] Room Free Recall (RFR) - EXCLUDED (no confidence judgments)
- [ ] Timed Cued Recall (TCR) - EXCLUDED (no confidence judgments)
- [ ] Room Recognition (RRE) - EXCLUDED (no confidence judgments)
- [x] All memory domains (What, Where, When) - INCLUDED for omnibus analysis

**Tests:**
- [x] All 4 test sessions (T1, T2, T3, T4 corresponding to Days 0, 1, 3, 6)

---
