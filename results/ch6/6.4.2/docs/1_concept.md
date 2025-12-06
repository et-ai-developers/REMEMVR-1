# RQ 6.4.2: Paradigm Confidence Calibration

**Chapter:** 6
**Type:** Paradigm Confidence
**Subtype:** Calibration
**Full ID:** 6.4.2

---

## Research Question

**Primary Question:**
Are people better calibrated with more retrieval support? Does calibration quality differ across Free Recall, Cued Recall, and Recognition paradigms?

**Scope:**
This RQ examines calibration (confidence-accuracy alignment) across three retrieval paradigms using IRT-derived theta estimates. Sample: N=100 participants � 4 test sessions � 3 paradigms = 1200 observations. Paradigms: Free Recall (IFR), Cued Recall (ICR), Recognition (IRE). Time variable uses TSVR (actual hours since encoding), not nominal days.

**Theoretical Framing:**
Retrieval support (cues, recognition probes) may create fluent retrieval that inflates subjective confidence even when objective accuracy is only moderate. This fluency-familiarity heuristic could lead to calibration differences across paradigms, with Recognition showing the highest overconfidence due to false fluency from retrieval cues.

---

## Theoretical Background

**Relevant Theories:**
- **Fluency-Familiarity Heuristic:** Easy retrieval (high fluency) is misattributed to strong memory, inflating confidence ratings even when accuracy doesn't warrant it. Recognition provides maximal retrieval support, creating highest fluency and potentially spurious confidence.
- **Source Monitoring Framework (Johnson et al., 1993):** Distinguishing memory from imagination requires evaluating qualitative characteristics (perceptual detail, context). High retrieval support may reduce diagnostic value of these cues, leading to overconfidence.
- **Metacognitive Monitoring Theory:** Confidence judgments rely on retrieval fluency as a cue for memory strength. Paradigms differ in baseline fluency, creating calibration differences.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
Recognition paradigm should show highest overconfidence (fluent retrieval from recognition probes doesn't guarantee accurate discrimination). Free Recall should show best calibration (retrieval difficulty provides accurate cue for memory strength - if it's hard to recall, confidence appropriately lower).

**Literature Gaps:**
Most calibration research uses single paradigms. This RQ directly compares calibration across paradigms using matched IRT-scaled metrics, testing whether retrieval support systematically affects metacognitive accuracy.

---

## Hypothesis

**Primary Hypothesis:**
Recognition will show significantly more OVERCONFIDENCE (Calibration > 0, confidence exceeds accuracy) than Free Recall. Free Recall will show best calibration (lowest |Calibration| scores, confidence matches accuracy most closely). Tested via significant Paradigm � Calibration interaction in LMM.

**Secondary Hypotheses:**
1. Cued Recall calibration will fall intermediate between Free Recall and Recognition (moderate retrieval support).
2. Recognition overconfidence will be stable across time (paradigm effect on baseline calibration, not trajectory).

**Theoretical Rationale:**
Recognition provides maximal retrieval support (test probe re-presents encoded stimulus), creating fluent retrieval even for weakly encoded items. This fluency feels like "remembering," inflating confidence beyond what accuracy warrants. Free Recall requires self-generated retrieval with no external cues - retrieval difficulty provides accurate diagnostic cue for memory strength, supporting better calibration.

**Expected Effect Pattern:**
- Significant main effect of Paradigm on calibration: Recognition > Cued Recall > Free Recall (p < 0.05).
- Recognition calibration significantly > 0 (overconfidence).
- Free Recall calibration closest to 0 (good calibration).
- Paradigm ranking: Free Recall = best calibrated, Recognition = worst calibrated.

---

## Memory Domains

**Domains Examined:**

This RQ does NOT examine What/Where/When domains separately. Paradigm analysis uses ALL item types combined within each paradigm.

**Paradigms Examined:**

- [x] **Free Recall (IFR)**
  - Tag Code: IFR (Interactive Free Recall)
  - Description: Self-generated retrieval with no external cues
  - Expected Calibration: Best (lowest |Calibration|)

- [x] **Cued Recall (ICR)**
  - Tag Code: ICR (Interactive Cued Recall)
  - Description: Retrieval with semantic cues
  - Expected Calibration: Intermediate

- [x] **Recognition (IRE)**
  - Tag Code: IRE (Interactive Recognition)
  - Description: Forced-choice discrimination with test probes
  - Expected Calibration: Worst (highest overconfidence)

**Inclusion Rationale:**
All three interactive paradigms included to test full retrieval support gradient (none � cue � probe). Matches Ch5 5.3.1 paradigm analysis for direct accuracy-confidence comparison.

**Exclusion Rationale:**
Room Free Recall (RFR) and other non-interactive paradigms excluded to maintain consistency with Ch5 5.3.X analyses.

---

## Analysis Approach

**Analysis Type:**
Linear Mixed Models (LMM) testing Paradigm � Time effects on calibration metric (confidence - accuracy on theta scale)

**High-Level Workflow:**

**Step 0:** Merge accuracy theta from Ch5 5.3.1 and confidence theta from RQ 6.4.1 by UID � test � paradigm

**Step 1:** Compute calibration per paradigm: Calibration = theta_confidence - theta_accuracy. **Z-standardization strategy:** Standardize POOLED across all paradigms (not within-paradigm) to preserve cross-paradigm comparability. Both theta scores are standardized using grand mean/SD before computing difference. **Limitation acknowledged:** Difference scores inherit reliability limitations from both constituent measures; reliability of difference = (r_xx + r_yy - 2*r_xy) / (2 - 2*r_xy). This is acceptable given IRT-derived theta estimates have high reliability (typically r > 0.90)

**Step 1b: Empirical Difference Score Reliability Check (REQUIRED)**
- Extract test information curves from Ch5 5.3.1 and Ch6 6.4.1 IRT models
- Compute empirical r(theta_accuracy, theta_confidence) correlation
- Apply reliability formula: r_diff = (r_xx + r_yy - 2*r_xy) / (2 - 2*r_xy)
- Report empirical reliability estimate; if r_diff < 0.70, acknowledge limitation in results interpretation
- Document: IRT theta reliabilities (r_xx, r_yy), cross-measure correlation (r_xy), computed r_diff

**Step 2:** Fit LMM with Paradigm × Time interaction: `Calibration ~ Paradigm × Time + (Time | UID)`, test Paradigm main effect and interaction. **Random slopes convergence plan:** With N=100, random slopes may fail to converge. Strategy: (1) Attempt full model (Time | UID), (2) If singular fit, compare via LRT: (Time | UID) vs (Time || UID) vs (1 | UID), (3) Select most parsimonious model where ΔAICc < 2, (4) Document convergence diagnostics and final model selection rationale

**Step 3:** Extract paradigm-specific effects: contrasts for Recognition vs Free Recall, Cued Recall vs Free Recall, Recognition vs Cued Recall

**Step 4:** Test Recognition overconfidence hypothesis: Is Recognition calibration significantly > 0? One-sample t-test per timepoint.

**Step 5:** Rank paradigms by calibration quality: Mean |Calibration| per paradigm, identify best/worst calibrated

**Expected Outputs:**
- data/step01_calibration_by_paradigm.csv (1200 rows: UID, test, paradigm, theta_accuracy, theta_confidence, calibration)
- results/step02_lmm_summary.txt (model output with Paradigm � Time terms)
- results/step03_paradigm_effects.csv (contrasts: Recognition vs Free Recall, etc.)
- results/step04_recognition_overconfidence_test.csv (one-sample t-tests, 4 timepoints)
- plots/step05_calibration_by_paradigm.csv (plot data: paradigm trajectories)

**Success Criteria:**
- Merge successful: 1200 observations (100 participants � 4 tests � 3 paradigms)
- Calibration computed per paradigm (no missing values)
- LMM converged with finite estimates
- Recognition overconfidence hypothesis tested with statistical significance reported
- Paradigm ranking documented (best to worst calibration)

---

## Data Source

**Data Type:**
DERIVED (from Chapter 5 accuracy analysis and Chapter 6 confidence analysis)

### DERIVED Data Source:

**Source RQs:**
1. **Ch5 5.3.1 (Paradigm Accuracy Trajectories):** Accuracy theta estimates by paradigm
2. **Ch6 6.4.1 (Paradigm Confidence Trajectories):** Confidence theta estimates by paradigm

**File Paths:**
- Accuracy: `results/ch5/5.3.1/data/step03_theta_accuracy_paradigm.csv` (1200 rows: UID, test, paradigm, theta_accuracy)
- Confidence: `results/ch6/6.4.1/data/step03_theta_confidence_paradigm.csv` (1200 rows: UID, test, paradigm, theta_confidence)

**Dependencies:**
1. Ch5 5.3.1 must complete Steps 1-3 (IRT calibration for accuracy by paradigm)
2. Ch6 6.4.1 must complete Steps 1-3 (IRT calibration for confidence by paradigm)
3. Both RQs must use matching sample and paradigm definitions (IFR, ICR, IRE)

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants from Ch5 5.3.1 and Ch6 6.4.1 (inherited inclusion criteria)
- Expected: N=100 (no exclusions)

**Items:**
- [x] Items already aggregated to theta scale in source RQs
- Paradigm-specific item sets (IFR, ICR, IRE items as defined in source analyses)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4; nominal Days 0, 1, 3, 6)
- Inherited from source RQs

**Paradigms:**
- [x] Free Recall (IFR)
- [x] Cued Recall (ICR)
- [x] Recognition (IRE)
- [ ] Room Free Recall (RFR) - EXCLUDED (not in Ch5 5.3.X)
- [ ] Other non-interactive paradigms - EXCLUDED

---

## Limitations

### Lord's Paradox Risk

**Issue:** Pre-existing paradigm differences in baseline accuracy could create regression-to-mean artifacts when comparing calibration across paradigms. Paradigms with lower baseline accuracy may show artificially inflated calibration differences due to mathematical coupling between accuracy and calibration metrics.

**Mitigation Strategy:**
1. **Primary analysis:** Within-subject design (same participants across paradigms) naturally controls for between-person confounds
2. **Sensitivity check 1:** ANCOVA approach - model `Confidence ~ Paradigm + Accuracy` to partial out accuracy effects
3. **Sensitivity check 2:** Within-paradigm standardization - z-score calibration within each paradigm separately
4. **Interpretation guidance:** If ANCOVA results contradict primary LMM, prioritize within-subject comparisons as more robust to Lord's paradox
5. **Report:** Include both primary and sensitivity analyses; flag if conclusions diverge

**References:**
- Van Breukelen (2006): ANCOVA vs change scores for two-wave data
- Tennant et al. (2023): Lord's Paradox explained - causal inference perspective

---

**End of Concept Document**
