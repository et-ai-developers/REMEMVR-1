# RQ 6.2.1: Calibration Over Time

**Chapter:** 6
**Type:** Calibration
**Subtype:** Over Time
**Full ID:** 6.2.1

---

## Research Question

**Primary Question:**
Does calibration (confidence-accuracy alignment) change from Day 0 to Day 6?

**Scope:**
This RQ examines calibration trajectories across four test sessions (T1, T2, T3, T4; nominal Days 0, 1, 3, 6). Calibration is defined as the difference between confidence and accuracy, computed at the person-timepoint level. Sample: N=100 participants x 4 tests = 400 observations. Merges IRT-derived theta scores from both accuracy (Ch5 5.1.1) and confidence (Ch6 6.1.1) domains.

**Theoretical Framing:**
If confidence and accuracy decline in parallel, calibration should remain stable across the retention interval (no significant Time effect). However, if confidence lags behind accuracy decline, overconfidence may emerge over time, indicating a dissociation between metacognitive monitoring and actual memory performance. This RQ provides foundational evidence for understanding the relationship between memory decay and metacognitive awareness in episodic VR memory.

---

## Theoretical Background

**Relevant Theories:**
- **Metacognitive Monitoring Theory**: Accurate calibration requires real-time monitoring of memory trace strength. If monitoring processes fail to track memory decay, calibration worsens over time.
- **Dual-Process Theory**: Familiarity-based processes may maintain subjective confidence even as recollection-based accuracy declines, leading to calibration drift.
- **Memory Trace Decay Theory**: If both memory traces and metacognitive signals decay at similar rates, calibration should remain stable. Differential decay rates would produce calibration changes.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
If metacognitive monitoring accurately tracks memory strength, calibration should remain stable across the 6-day interval. If confidence is less sensitive to memory decay than accuracy, overconfidence should increase over time (positive Time effect on calibration metric).

**Literature Gaps:**
[To be identified by rq_scholar]

---

## Hypothesis

**Primary Hypothesis:**
Calibration may show either STABILITY (confidence and accuracy decline in parallel, no Time effect) or WORSENING (confidence lags behind accuracy, positive Time effect indicating increasing overconfidence). Multiple calibration metrics are computed to triangulate the pattern: difference score (theta_confidence - theta_accuracy), Brier score (item-level squared error), and Expected Calibration Error (ECE, binned by confidence levels).

**Secondary Hypotheses:**
None - exploratory analysis of calibration trajectory pattern.

**Theoretical Rationale:**
Stable calibration would suggest that metacognitive monitoring processes accurately track memory trace decay. Worsening calibration (increasing overconfidence) would indicate that confidence judgments are less sensitive to forgetting than actual memory performance, potentially due to familiarity-based confidence that persists despite recollection failure.

**Expected Effect Pattern:**
LMM testing Time effect on calibration metric. If Time effect is significant (p < 0.05 with dual p-values per Decision D068), indicates calibration changes over retention interval. Direction of Time coefficient determines whether calibration improves (negative) or worsens (positive). Brier score and ECE provide converging evidence for calibration trajectory pattern.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: All interactive VR items (omnibus "All" factor)

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location, legacy)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Disambiguation: All spatial tags included in omnibus factor

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order items included in omnibus factor

**Inclusion Rationale:**
This RQ uses omnibus theta scores from both Ch5 5.1.1 (accuracy) and Ch6 6.1.1 (confidence), which aggregate across all WWW domains. Calibration is computed as the alignment between these two omnibus scores, reflecting overall episodic memory calibration rather than domain-specific patterns.

**Exclusion Rationale:**
No exclusions - all interactive paradigm items (IFR, ICR, IRE) included via omnibus factor. Room Free Recall (RFR) and Test Cued Recall (TCR) excluded as per Ch5/Ch6 standard extraction protocol.

---

## Analysis Approach

**Analysis Type:**
Linear Mixed Models (LMM) for calibration trajectory analysis + Brier score and Expected Calibration Error (ECE) for item-level calibration metrics

**High-Level Workflow:**

**Step 0:** Load accuracy theta from Ch5 5.1.1 (results/ch5/5.1.1/data/step03_theta_scores.csv) and confidence theta from Ch6 6.1.1 (results/ch6/6.1.1/data/step03_theta_confidence.csv)

**Step 1:** Merge accuracy and confidence theta scores by UID x TEST. Verify 400 observations (N=100 participants x 4 tests). Both theta scores must be z-standardized before computing calibration difference.

**Step 2:** Compute calibration metric: Calibration = theta_confidence - theta_accuracy (after z-standardization). Positive values indicate overconfidence (confidence exceeds accuracy), negative values indicate underconfidence.

**Step 3:** Compute Brier score at item level. Requires raw item-level confidence (0, 0.25, 0.5, 0.75, 1.0) and accuracy (0/1). Brier = mean((confidence - accuracy)^2). Lower Brier indicates better calibration.

**Step 4:** Compute Expected Calibration Error (ECE). Bin item-level responses by confidence level (5 bins: 0, 0.25, 0.5, 0.75, 1.0). Within each bin, compute mean(confidence) - mean(accuracy). ECE = weighted average of absolute bin errors. Compute ECE per timepoint.

**Step 5:** Fit LMM for calibration trajectory: Calibration ~ Time + (Time | UID). Time variable is TSVR (hours since encoding) or transformed time from Step 4 data. Random slopes allow individual differences in calibration change.

**Step 6:** Test Time effect on calibration using dual p-values (Decision D068: Wald p-value and Likelihood Ratio Test p-value). Significant positive Time effect indicates worsening calibration (increasing overconfidence). Null Time effect indicates stable calibration.

**Step 7:** Prepare plot data for calibration trajectory visualization. Output theta-scale and probability-scale data showing how calibration evolves from Day 0 to Day 6.

**Expected Outputs:**
- data/step01_merged_theta.csv (400 rows: UID, TEST, TSVR, theta_accuracy, theta_confidence)
- data/step02_calibration_scores.csv (400 rows: UID, TEST, TSVR, calibration)
- data/step03_brier_scores.csv (item-level Brier scores per person-timepoint)
- data/step04_ece_by_time.csv (4 rows: ECE computed per test/timepoint)
- results/step05_calibration_lmm.txt (LMM summary output)
- results/step06_time_effect.csv (Time coefficient, dual p-values, interpretation)
- plots/step07_calibration_trajectory.csv (plot data for visualization)

**Success Criteria:**
- Merge successful: 400 observations (N=100 x 4 tests)
- Both theta scores z-standardized before computing calibration
- Calibration metric computed per person-timepoint
- Brier score computed at item level
- ECE computed per timepoint (4 values)
- LMM converged with Time effect tested
- Dual p-values reported per Decision D068
- Plot data complete with both theta-scale and probability-scale representations

---

## Data Source

**Data Type:**
DERIVED (from Chapter 5 and Chapter 6 root RQ outputs)

### DERIVED Data Source:

**Source RQs:**
1. **RQ 5.1.1** (Ch5 Functional Form Comparison - Accuracy)
2. **RQ 6.1.1** (Ch6 Confidence Model Selection)

**File Paths:**
- results/ch5/5.1.1/data/step03_theta_scores.csv (accuracy theta: N=100 x 4 tests = 400 rows)
- results/ch6/6.1.1/data/step03_theta_confidence.csv (confidence theta: N=100 x 4 tests = 400 rows)
- results/ch6/6.1.1/data/step00_tsvr_mapping.csv (TSVR time variable mapping)

**Additional Data (for Brier and ECE):**
- data/cache/dfData.csv (raw item-level TQ_* accuracy and TC_* confidence for Brier/ECE computation)

**Dependencies:**
- RQ 5.1.1 must complete Steps 1-3 (IRT calibration of accuracy) before this RQ can run
- RQ 6.1.1 must complete Steps 1-3 (IRT calibration of confidence) before this RQ can run
- Both source RQs must use same participant sample and test structure (N=100, 4 tests)

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (inherited from Ch5 5.1.1 and Ch6 6.1.1 - no exclusions)

**Items:**
- N/A (theta scores are already aggregated person-level estimates)
- For Brier/ECE: All interactive paradigm items (IFR, ICR, IRE) from omnibus "All" factor
- Excludes: Room Free Recall (RFR), Test Cued Recall (TCR), Recognition (RRE)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4; nominal Days 0, 1, 3, 6)
- Time variable: TSVR (actual hours since encoding), not nominal days

**Critical Note:**
This RQ requires exact alignment between Ch5 accuracy theta and Ch6 confidence theta. Both must be derived from same participant sample, same test sessions, and same omnibus "All" factor structure. Merge key is UID x TEST. Any mismatch in sample or structure will trigger merge failure.

---
