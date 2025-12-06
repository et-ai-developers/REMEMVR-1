# RQ 6.4.1: Paradigm Confidence Trajectories

**Chapter:** 6
**Type:** Paradigm Confidence
**Subtype:** Trajectories
**Full ID:** 6.4.1

---

## Research Question

**Primary Question:**
Do Free Recall, Cued Recall, and Recognition paradigms show different confidence decline patterns over a 6-day retention interval?

**Scope:**
This RQ examines confidence trajectories across three retrieval paradigms (IFR, ICR, IRE) using IRT-derived ability estimates from TC_* (confidence) items. Sample: N=100 participants × 4 test sessions × 3 paradigms = 1200 observations. Compares paradigm-specific confidence decline rates from Day 0 (encoding) to Day 6 (nominal), using TSVR (actual hours since encoding) as time metric.

**Theoretical Framing:**
Examines whether retrieval support (free vs cued vs recognition) affects not only memory accuracy (Ch5 5.3.1-5.3.2 found NULL for slopes) but also subjective confidence in memory. Critical test: if confidence parallels accuracy, paradigm × time interaction should be NULL. Alternative: retrieval support may create confidence illusions independent of actual memory strength.

---

## Theoretical Background

**Relevant Theories:**
- **Transfer-Appropriate Processing** (Morris et al., 1977): Retrieval support (cues, recognition options) provides encoding-retrieval match that enhances performance. However, Ch5 findings showed paradigm effects on baseline only, not decay rates.
- **Retrieval Fluency Theory** (Kelley & Rhodes, 2002): Recognition may create fluent retrieval experiences that inflate confidence even when accuracy is only moderate. Multiple-choice format provides familiarity cues that feel like remembering.
- **Metacognitive Monitoring** (Koriat, 1997): Confidence judgments may be based on retrieval fluency rather than actual memory strength. Recognition's perceptual fluency may create overconfidence relative to free recall.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
NULL hypothesis expected: Paradigm differences were NULL for accuracy slopes in Ch5 5.3.1-5.3.2 (retrieval support affects baseline, not decay). If confidence parallels accuracy, paradigm × time interaction should be NULL. However, Recognition may show HIGHEST baseline confidence at Day 0 due to retrieval support creating illusion of remembering (fluency misattribution).

**Literature Gaps:**
[To be identified by rq_scholar]

---

## Hypothesis

**Primary Hypothesis:**
Paradigm × Time interaction will be NULL (no differential decline rates across Free Recall, Cued Recall, Recognition), paralleling Ch5 5.3.1-5.3.2 accuracy findings. Retrieval support affects baseline confidence but not confidence decay rate.

**Secondary Hypotheses:**
1. Recognition may show highest baseline confidence at Day 0 (retrieval support creates fluency-based confidence boost)
2. Free Recall may show lowest baseline confidence (minimal retrieval support, higher retrieval effort)
3. Confidence decline slopes will be parallel across paradigms (similar to accuracy pattern)

**Theoretical Rationale:**
Ch5 5.3.1-5.3.2 established that paradigm affects retrieval SUCCESS (baseline accuracy) but not forgetting RATE (slope invariant). If confidence is calibrated to memory, it should show same pattern: paradigm affects initial confidence but not decline trajectory. However, retrieval fluency theory predicts Recognition may show inflated baseline confidence due to familiarity cues from multiple-choice format (feels like remembering even when guessing).

**Expected Effect Pattern:**
- Paradigm main effect: Recognition > Cued Recall > Free Recall for baseline confidence (p < 0.05)
- Paradigm × Time interaction: NULL (p > 0.05) - parallel decline rates
- Time main effect: significant negative (p < 0.001) - universal confidence decline
- Effect size: Paradigm baseline differences d H 0.3-0.5, slope differences d < 0.2

---

## Memory Domains

**Domains Examined:**

- [ ] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: NOT examined separately in this RQ

- [ ] **Where** (Spatial Location)
  - [ ] `-L-` tags (general location, legacy)
  - [ ] `-U-` tags (pick-up location)
  - [ ] `-D-` tags (put-down location)
  - Disambiguation: NOT examined separately in this RQ

- [ ] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: NOT examined separately in this RQ

**Paradigm Focus Instead:**
This RQ examines confidence by RETRIEVAL PARADIGM, not episodic memory domain (What/Where/When):

- [x] **Free Recall (IFR)**: Minimal retrieval support, free recall of object identities
- [x] **Cued Recall (ICR)**: Spatial cues provided (object locations shown, participant recalls which object)
- [x] **Recognition (IRE)**: Multiple-choice recognition with foils

**Inclusion Rationale:**
Paradigm-based analysis tests whether retrieval support affects confidence trajectories. All interactive paradigm items included (IFR, ICR, IRE). This parallels Ch5 5.3.1 (accuracy by paradigm) to test if confidence shows same paradigm-invariant slope pattern.

**Exclusion Rationale:**
- Room-level paradigms EXCLUDED (RFR, TCR, RRE) - focuses on object-level interactive tasks only
- Domain-specific analysis conducted separately in RQ 6.3.1 (Domain Confidence Trajectories)

---

## Analysis Approach

**Analysis Type:**
IRT (Item Response Theory) for ability estimation using Graded Response Model (GRM) for 5-category ordinal confidence data + LMM (Linear Mixed Models) for paradigm × time trajectory analysis

**High-Level Workflow:**

**Step 0:** Extract TC_* confidence items from dfData.csv, filter to paradigm-specific items (IFR, ICR, IRE tags)

**Step 1:** IRT Pass 1 calibration using 3-factor GRM (separate factor per paradigm: IFR/ICR/IRE) on all 5-category ordinal confidence items, p1_med prior

**Step 2:** Item purification (Decision D039): exclude items with |b| > 3.0 OR a < 0.4 (applies to GRM threshold parameters)

**Step 3:** IRT Pass 2 re-calibration on purified items (final theta_confidence estimates per paradigm)

**Step 4:** Merge theta_confidence with TSVR, create time transformations (Days = TSVR/24, log_Days_plus1)

**Step 5:** Fit LMM with Paradigm × Time interaction: theta_confidence ~ Paradigm × (Time + Time_log) + (Time + Time_log | UID), test paradigm slope differences

**Step 6:** Post-hoc contrasts: Free Recall vs Cued Recall vs Recognition baseline and slope comparisons

**Step 7:** Compare to Ch5 5.3.1 accuracy paradigm analysis (test if confidence replicates accuracy NULL slope findings)

**Step 8:** Note if Recognition shows highest baseline confidence (retrieval support hypothesis)

**Expected Outputs:**
- data/step00_irt_input.csv (paradigm-tagged confidence items)
- data/step00_tsvr_mapping.csv (time mapping)
- data/step00_q_matrix.csv (3-factor structure: IFR/ICR/IRE)
- data/step02_purified_items.csv (retained items after purification)
- data/step03_theta_confidence_paradigm.csv (1200 rows: 100 participants × 4 tests × 3 paradigms)
- data/step04_lmm_input.csv (1200 rows with time transformations)
- results/step05_lmm_summary.txt (Paradigm × Time interaction test)
- results/step06_paradigm_contrasts.csv (post-hoc comparisons)
- results/step07_ch5_comparison.csv (accuracy vs confidence paradigm effects)
- results/step08_recognition_baseline_test.csv (if Recognition highest baseline)

**Success Criteria:**
- IRT convergence: theta_confidence in [-4,4], SE in [0.1,1.5]
- GRM model appropriate for 5-category ordinal data (NOT 2PL which assumes dichotomous)
- Item purification: 30-70% retention per paradigm
- LMM convergence with 1200 observations
- Paradigm × Time interaction tested with dual p-values (Decision D068: likelihood ratio + Wald)
- Post-hoc contrasts Bonferroni-corrected (3 comparisons: alpha=0.0167)
- Ch5 5.3.1 comparison documented (expect NULL slope replication)
- Recognition baseline hypothesis tested (expect highest Day 0 confidence)

---

## Data Source

**Data Type:**
RAW (extracts directly from dfData.csv)

### RAW Data Extraction:

**Source File:**
data/cache/dfData.csv

**Tag Patterns:**
- Paradigm codes: IFR (Interactive Free Recall), ICR (Interactive Cued Recall), IRE (Interactive Recognition)
- Confidence items: TC_* tags (5-category ordinal: 0, 0.25, 0.5, 0.75, 1.0)
- Excludes room-level paradigms: RFR, TCR, RRE
- Excludes accuracy items: TQ_* (dichotomous 0/1)

**Extraction Method:**
Step 0 extracts from dfData.csv using paradigm tag filters, creates:
- data/step00_irt_input.csv (wide format: rows=participants×tests, columns=TC_* items by paradigm, values=0/0.25/0.5/0.75/1.0 confidence ratings)
- data/step00_tsvr_mapping.csv (participant × test ’ TSVR hours mapping)
- data/step00_q_matrix.csv (3-factor structure: Factor1=IFR confidence, Factor2=ICR confidence, Factor3=IRE confidence)

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions)

**Items:**
- [x] Interactive paradigm confidence items ONLY (TC_* with IFR/ICR/IRE tags)
- [ ] Room-level paradigms EXCLUDED (RFR, TCR, RRE - not object-level tasks)
- [ ] Accuracy items EXCLUDED (TQ_* - analyzed in Ch5, not relevant for confidence)
- [x] All three retrieval paradigms included (IFR, ICR, IRE)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4)
- Timepoints: T1=Day 0 (encoding), T2HDay 1, T3HDay 3, T4HDay 6 (nominal), actual timing via TSVR

**Critical Note:**
Confidence items (TC_*) are 5-category ordinal (0, 0.25, 0.5, 0.75, 1.0), NOT dichotomous like accuracy items (TQ_* are 0/1). Must use Graded Response Model (GRM) for IRT calibration, NOT 2-parameter logistic (2PL). This is CRITICAL methodological distinction from Ch5 accuracy analyses.

---
