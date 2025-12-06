# RQ 6.2.2: Over-Underconfidence Trajectory

**Chapter:** 6
**Type:** Calibration
**Subtype:** Over-Underconfidence
**Full ID:** 6.2.2

---

## Research Question

**Primary Question:**
Do people become overconfident as memories fade over the 6-day retention interval?

**Scope:**
This RQ examines calibration trajectories (confidence-accuracy alignment) across four test sessions (T1, T2, T3, T4; nominal Days 0, 1, 3, 6). Specifically tests whether overconfidence (Calibration > 0, confidence exceeds accuracy) INCREASES from Day 0 to Day 6 as accuracy declines faster than confidence adjusts. N=100 participants x 4 tests = 400 observations. Uses calibration scores derived from RQ 6.2.1.

**Theoretical Framing:**
Overconfidence may emerge over time as memories fade but metacognitive monitoring lags behind actual memory decline. This would indicate dissociation between memory performance and metacognitive awareness, suggesting confidence judgments rely on different (possibly slower-updating) memory signals than retrieval itself. Critical for understanding memory-metacognition coupling dynamics.

---

## Theoretical Background

**Relevant Theories:**
- **Metacognitive Monitoring Theory**: Confidence judgments may rely on different cues than actual memory retrieval (fluency, familiarity, schema consistency) that update more slowly than memory traces themselves.
- **Memory-Metacognition Dissociation**: Accuracy and confidence may follow different time courses, with confidence lagging behind actual memory decay, creating emergent overconfidence.
- **Dual-Process Theory**: Familiarity-based confidence (fast, automatic) may persist longer than recollection-based accuracy (effortful, decay-prone), producing overconfidence for degraded memories.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
If confidence and accuracy decline in parallel (coupled system), calibration should remain STABLE across time (no overconfidence emergence). If confidence lags behind accuracy decline (dissociated system), OVERCONFIDENCE should increase from Day 0 to Day 6. RQ 6.2.1 tests overall calibration trajectory; this RQ specifically tests directionality (over vs under).

**Literature Gaps:**
[To be identified by rq_scholar - longitudinal studies of confidence-accuracy calibration over retention intervals, dissociation dynamics]

---

## Hypothesis

**Primary Hypothesis:**
Overconfidence (Calibration > 0, confidence exceeds accuracy) will INCREASE from Day 0 to Day 6 as accuracy declines faster than confidence adjusts. Expected: significant positive Time effect on proportion overconfident, or significant positive Time effect on mean calibration (if mean calibration becomes more positive over time).

**Secondary Hypotheses:**
Secondary hypothesis: Compute proportion of participants who are overconfident at each timepoint and test for increasing trend. Threshold: overconfident if Calibration > 0 (confidence exceeds accuracy after z-standardization).

**Theoretical Rationale:**
Memory traces decay faster than metacognitive signals update. Confidence judgments may rely on residual familiarity or schema-based expectations that persist even when recollection fails. This creates lag between actual memory decline and subjective confidence decline, manifesting as emergent overconfidence. If confidence perfectly tracks accuracy, no overconfidence trend should emerge.

**Expected Effect Pattern:**
Expected: significant positive Time x Calibration interaction, indicating overconfidence worsens over time. Proportion overconfident at Day 0 may be ~33% (random variation), increasing to >50% by Day 6. Mean calibration shifts from near-zero (calibrated) at Day 0 to positive (overconfident) by Day 6. Trend test (proportion overconfident ~ Time) should show positive slope with p < 0.05.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Included in omnibus accuracy (Ch5 5.1.1) and omnibus confidence (6.1.1)

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location, legacy)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Disambiguation: All Where tags included in omnibus factor

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Included in omnibus factor (if sufficient items after purification)

**Inclusion Rationale:**
This RQ uses calibration scores derived from RQ 6.2.1, which merges omnibus accuracy (Ch5 5.1.1, single "All" factor) with omnibus confidence (6.1.1, single "All" factor). Therefore, all domains are included in the aggregated theta scores. Overconfidence analysis examines overall calibration trajectory, not domain-specific patterns (those addressed in 6.3.2).

**Exclusion Rationale:**
No domain exclusions. Analysis operates at person-timepoint level (400 observations), not item level. Domain decomposition handled separately in 6.3.X series.

---

## Analysis Approach

**Analysis Type:**
Descriptive statistics + trend analysis (logistic or linear regression of overconfidence proportions across time)

**High-Level Workflow:**

**Step 0:** Load calibration scores from RQ 6.2.1 (data/step02_calibration_scores.csv, 400 rows: UID x test x calibration metric)

**Step 1:** Classify each observation by sign of calibration:
- Overconfident: Calibration > 0 (confidence exceeds accuracy)
- Underconfident: Calibration < 0 (accuracy exceeds confidence)
- Calibrated: Calibration approximately 0 (within +/- epsilon, e.g., 0.1 SD units)

**Step 2:** Compute proportion overconfident at each timepoint:
- Group by TEST (T1, T2, T3, T4)
- Count N overconfident / N total per timepoint
- Expected pattern: increasing proportion from Day 0 to Day 6

**Step 3:** Trend test:
- Fit linear or logistic model: proportion_overconfident ~ Time (or TEST as ordinal predictor)
- Test if slope significantly positive (p < 0.05)
- Report effect size (change in proportion from Day 0 to Day 6)

**Step 4:** Compute mean calibration by timepoint:
- Mean(Calibration) per TEST
- Plot trajectory to visualize shift toward overconfidence
- Compare to RQ 6.2.1 overall calibration trajectory

**Step 5:** Plot overconfidence trajectory:
- X-axis: TEST (T1, T2, T3, T4)
- Y-axis: Proportion overconfident (or mean calibration)
- Expected: upward trend indicating emergent overconfidence

**Expected Outputs:**
- data/step01_calibration_classified.csv (400 rows: UID, test, calibration, classification)
- results/step02_proportion_overconfident.csv (4 rows: TEST, N_total, N_overconfident, proportion, CI)
- results/step03_trend_test.csv (trend model summary: slope, SE, p-value, effect size)
- results/step04_mean_calibration.csv (4 rows: TEST, mean_calibration, SD, SE)
- plots/step05_overconfidence_trajectory.csv (plot source data: TEST, proportion_overconfident, mean_calibration)

**Success Criteria:**
- Classification complete: all 400 observations assigned to overconfident/underconfident/calibrated categories
- Proportions sum to 1.0 per timepoint (within rounding error)
- Trend test converges and produces valid p-value
- Plot data shows clear trajectory pattern (increasing, decreasing, or stable)
- Interpretation documented: Does overconfidence emerge over time? (Yes/No/Inconclusive)

---

## Data Source

**Data Type:**
DERIVED (from RQ 6.2.1 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 6.2.1 (Calibration Over Time)

**File Paths:**
- results/ch6/6.2.1/data/step02_calibration_scores.csv (400 rows: UID x TEST x calibration metrics)

**Dependencies:**
RQ 6.2.1 must complete Steps 0-2 before this RQ can run. Specifically requires:
- Merged accuracy theta (from Ch5 5.1.1) and confidence theta (from 6.1.1)
- Computed calibration scores: Calibration = theta_confidence - theta_accuracy (z-standardized)

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (inherited from RQ 6.2.1, which inherits from Ch5 5.1.1 and 6.1.1)
- [ ] No participant exclusions

**Items:**
- N/A (analysis uses aggregated theta scores, not item-level data)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4; nominal Days 0, 1, 3, 6)
- [ ] No test exclusions

**Note:**
This is a person-timepoint analysis (400 observations). Does not require raw item-level data. All data dependencies flow through RQ 6.2.1 calibration scores, which themselves derive from omnibus theta scores (Ch5 5.1.1 accuracy + 6.1.1 confidence).

---
