# RQ 6.7.3: Calibration Predicts Trajectory Stability

**Chapter:** 6
**Type:** Predictive
**Subtype:** Calibration Predicts
**Full ID:** 6.7.3

---

## Research Question

**Primary Question:**
Are well-calibrated people more stable forgetters? Does good metacognitive skill at Day 0 predict more predictable (less variable) forgetting trajectories?

**Scope:**
This RQ examines the relationship between initial calibration quality (Day 0 confidence-accuracy alignment) and forgetting trajectory stability (variability of residuals around individual forgetting curves). Sample: N=100 participants, using calibration metrics from Day 0 (T1) and trajectory variability computed from 4-timepoint forgetting curves (400 observations from Ch5 5.1.1).

**Theoretical Framing:**
Explores whether metacognitive skill (good calibration) reflects or predicts stable consolidation processes. Well-calibrated individuals may have more reliable encoding and consolidation mechanisms, producing more predictable forgetting trajectories. Alternatively, calibration may be independent of consolidation stability if metacognitive monitoring operates separately from memory trace formation.

---

## Theoretical Background

**Relevant Theories:**
- **Metacognitive Monitoring Theory**: Good calibration reflects accurate monitoring of memory trace strength. If monitoring accuracy correlates with encoding quality, well-calibrated individuals should show more stable (less noisy) memory consolidation.
- **Consolidation Stability**: Individual differences in consolidation stability may reflect neurobiological factors (e.g., sleep quality, hippocampal integrity). If calibration taps into these factors, it should predict trajectory variability.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
If calibration reflects encoding quality: Good Day 0 calibration should predict LOW trajectory variability (stable, predictable forgetting). If calibration is independent of consolidation: No relationship between calibration and trajectory variability (NULL hypothesis).

**Literature Gaps:**
[To be identified by rq_scholar]

---

## Hypothesis

**Primary Hypothesis:**
Good calibration at Day 0 predicts lower trajectory variability. Specifically, individuals with better calibration (lower |Confidence - Accuracy| at Day 0) will show more stable forgetting trajectories (lower SD of residuals from individual LMM fits in Ch5 5.1.1). Expected correlation: Day0_calibration vs trajectory_variability, negative correlation if hypothesis supported (r < 0, p < 0.05).

**Secondary Hypotheses:**
None - single correlation test.

**Theoretical Rationale:**
Metacognitive skill may reflect stable, reliable memory encoding. Well-calibrated individuals have accurate access to memory trace strength, which may correlate with consistent consolidation processes. Poor calibration may reflect encoding noise or unstable metacognitive monitoring, both of which would increase trajectory variability.

**Expected Effect Pattern:**
Negative correlation between Day 0 calibration quality (absolute calibration error) and trajectory variability. Threshold: |r| > 0.20 for small effect, |r| > 0.30 for moderate effect. Direction: Better calibration (lower error) -> Lower variability (more stable).

---

## Memory Domains

**Domains Examined:**

- [x] **Omnibus "All" Factor**
  - Description: Uses aggregated theta scores from Ch5 5.1.1 (all interactive paradigm items combined)
  - Rationale: General memory ability, not domain-specific

**Inclusion Rationale:**
RQ uses theta scores from Ch5 5.1.1, which aggregated across all domains (What, Where, When) into single "All" factor. Calibration from 6.2.1 similarly uses omnibus factor. Analysis focuses on general metacognitive skill predicting general memory stability, not domain-specific effects.

**Exclusion Rationale:**
No domain decomposition needed for this predictive analysis. Domain-specific calibration-stability relationships would be separate RQs.

---

## Analysis Approach

**Analysis Type:**
Correlation analysis (Pearson r) with dual p-values (D068: one-tailed and two-tailed)

**High-Level Workflow:**

**Step 0:** Load Day 0 calibration from RQ 6.2.1 (theta_confidence - theta_accuracy at T1, both z-standardized)
**Step 1:** Load trajectory residuals from Ch5 5.1.1 best LMM (individual-level deviations from predicted forgetting curve)
**Step 2:** Compute individual trajectory variability: SD of residuals across 4 timepoints per participant (100 values)
**Step 3:** Compute correlation: Day0_calibration vs trajectory_variability (absolute calibration error vs SD of residuals)
**Step 4:** Test significance with dual p-values (one-tailed: negative correlation expected; two-tailed: any relationship)
**Step 5:** Effect size interpretation (small/moderate/large)
**Step 6:** Create scatterplot with regression line

**Expected Outputs:**
- data/step01_calibration_variability.csv (100 rows: UID, Day0_calibration, trajectory_variability)
- results/step02_correlation.csv (correlation coefficient, dual p-values, effect size)
- plots/step03_calibration_predicts_stability.csv (plot data)

**Success Criteria:**
- 100 participants with complete data (no missing calibration or variability values)
- Correlation computed with dual p-values (Decision D068)
- Direction of effect documented (positive, negative, or NULL)
- Effect size classification (small: |r| > 0.20, moderate: |r| > 0.30, large: |r| > 0.50)
- Scatterplot data prepared

---

## Data Source

**Data Type:**
DERIVED (from RQ 6.2.1 and Ch5 5.1.1 outputs)

### DERIVED Data Source:

**Source RQs:**
- RQ 6.2.1 (Calibration Over Time): Day 0 calibration scores
- Ch5 5.1.1 (Functional Form Comparison): Trajectory residuals from best LMM

**File Paths:**
- results/ch6/6.2.1/data/step02_calibration_scores.csv (400 rows, filter to T1/Day 0 for 100 rows)
- results/ch5/5.1.1/data/step04_lmm_input.csv (400 rows with fitted values from best model)
  - OR: results/ch5/5.1.1/data/step06_best_model.pkl (saved LMM model to extract residuals)

**Dependencies:**
- RQ 6.2.1 must complete Step 2 (calibration scores computed)
- Ch5 5.1.1 must complete Step 6 (best LMM fitted, residuals available)

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (inherited from Ch5 5.1.1 and RQ 6.2.1)
- Must have complete data: Day 0 calibration + all 4 timepoint residuals

**Items:**
- N/A (theta scores and calibration already aggregated)

**Tests:**
- [x] Day 0 (T1) for calibration predictor
- [x] All 4 tests (T1, T2, T3, T4) for trajectory variability computation

---
