# Context-Finder Search Results: RQ 6.2.5 (Calibration Age Effects)

**Search Date:** 2025-12-11
**Search Query:** Age effects on calibration, calibration series (6.2.1 through 6.2.5), Chapter 5 age effects for comparison

**Total Findings:** 7 major archive entries + documentation references

---

## I. CALIBRATION SERIES FOUNDATION (ROOT RQ 6.2.1 & DERIVATIVES)

### Finding 1: RQ 6.2.1 - Calibration Worsens Over Time (ROOT RQ)
**Source:** `.claude/context/archive/rq_6.2.1_calibration_worsens_thesis_ready.md`
**Timestamp:** 2025-12-11 19:45
**Status:** THESIS-READY
**Relevance Score:** 0.99 (Direct parent RQ)

**Key Content (Lines 1-100):**
- **Analysis Pipeline:** Steps 00a-07 (data merge, z-standardization, calibration computation, Brier scores, ECE, LMM, trajectory)
- **Finding:** CALIBRATION WORSENS SIGNIFICANTLY over retention interval
  - **Wald p=0.042** (significant at α=0.05)
  - **LRT p=0.004** (highly significant)
  - **Effect:** +0.146 calibration units per 100 hours
- **Trajectory:** T1=-0.116 (underconfident) → T4=+0.111 (overconfident), total change=+0.227
- **Zero-crossing:** Calibration shifts from underconfidence to overconfidence between Days 1-3
- **Interpretation:** Dual-process hypothesis supported - familiarity-based confidence persists while accuracy declines, metacognitive monitoring fails
- **Data:** 400 rows (100 participants × 4 tests), three calibration metrics converge (theta difference primary, Brier mean=0.167, ECE stable 0.090-0.102)
- **Validation:** 4-agent workflow, 0 critical/high/moderate issues

**Critical for 6.2.5:** This ROOT RQ establishes that calibration CHANGES with time. RQ 6.2.5 tests whether AGE MODERATES this change.

---

### Finding 2: RQ 6.2.2 - Overconfidence Proportion Trend (DERIVATIVE)
**Source:** `.claude/context/archive/rq_6.2.2_complete_overconfidence_trend_nonsig_thesis_ready.md`
**Timestamp:** 2025-12-11 20:15
**Status:** THESIS-READY
**Relevance Score:** 0.85 (Related derivative on calibration direction)

**Key Content (Lines 1-96):**
- **Finding:** Overconfidence PROPORTION increases descriptively (+10%, from 41% to 51%) BUT trend is NON-SIGNIFICANT (p=0.230)
- **Classification:** Overconfident >0.1, Underconfident <-0.1, Calibrated ±0.1
  - T1: 41% overconfident | T4: 51% overconfident
  - Overall distribution: 46.8% over, 44.2% under, 9.0% calibrated
- **Logistic Trend Test:** β=0.053 (log-odds per day), p=0.230 (NON-SIG), OR=1.054 [0.967, 1.149]
- **Integration with 6.2.1:**
  - **Magnitude worsens significantly** (p=0.004, 6.2.1)
  - **Direction trend NOT significant** (p=0.230, 6.2.2)
  - **Interpretation:** Miscalibration increases SYMMETRICALLY (both over/under), not discrete category flip
- **Validation:** 4-agent workflow, 0 critical/high/moderate, 3 moderate (non-independence, diagnostics, multiple comparisons) documented

**Critical for 6.2.5:** Shows calibration change is CONTINUOUS not categorical. Age effects should use continuous calibration metric (like 6.2.1) not classification.

---

### Finding 3: Chapter 6 Calibration Series Progress (11/31 RQs at snapshot)
**Source:** `.claude/context/archive/ch6_progress_11_of_31_thesis_ready_35_percent.md`
**Timestamp:** 2025-12-11 20:15
**Status:** PROGRESS SNAPSHOT
**Relevance Score:** 0.70 (Planning context)

**Key Content (Lines 43-52):**
- **Ready-to-Execute:** After 6.2.1 completion
  - **6.2.5 (Age Effects on Calibration)** - depends on 6.2.1 ✅
  - **6.7.3 (Calibration Predicts Forgetting)** - depends on 6.2.1 ✅
- **Total Executable Derivatives:** ~15 RQs with dependencies satisfied
- **Execution Velocity:** 25 min/RQ, 2-3 RQs/session

---

## II. AGE EFFECTS PATTERN (CROSS-CHAPTER VALIDATION)

### Finding 4: RQ 6.1.3 - Age × Confidence Trajectory NULL
**Source:** `.claude/context/archive/rq_6.1.3_complete_age_effects_null_thesis_ready_zero_anomalies.md`
**Timestamp:** 2025-12-11 16:45
**Status:** THESIS-READY, ZERO ANOMALIES
**Relevance Score:** 0.95 (Directly parallel - calibration is confidence difference)

**Key Content (Lines 1-100):**
- **RQ 6.1.3 Finding:** Age × Time interaction NULL (p=0.323, Bonferroni α=0.0167)
  - **Interaction coefficient:** β=0.001, SE=0.001, z=0.99, p=0.323
  - **Interpretation:** Confidence decline rate is AGE-INVARIANT
  - **Effect size at Day 6:** -0.045 theta units (negligible, older 59y vs younger 30y)
- **Model:** theta_confidence ~ Time_log * Age_c, (1 + Time_log | UID), random slopes included
- **Age Centering:** Age_c = Age - 44.57 (mean-centered)
- **Parallel Pattern to Chapter 5:**
  - RQ 5.1.3: Age × Time NULL (accuracy decline)
  - RQ 6.1.3: Age × Time NULL (confidence decline)
  - RQ 5.2.3: Age × Domain NULL (accuracy)
  - RQ 5.3.4: Age × Paradigm NULL (accuracy)
  - RQ 5.4.3: Age × Schema NULL (accuracy)
- **Validation:** 4-agent workflow with ZERO ANOMALIES

**Critical for 6.2.5:**
- Age does NOT moderate confidence decline (6.1.3)
- Age does NOT moderate accuracy decline (5.1.3)
- Therefore: Age likely does NOT moderate CALIBRATION (confidence-accuracy difference)
- This predicts RQ 6.2.5 will also find NULL age effect

---

### Finding 5: RQ 5.5.3 - Age × Source-Destination NULL (with Power Analysis)
**Source:** `.claude/context/archive/rq_5.5.3_complete_age_effects_null_hypothesis_supported.md`
**Timestamp:** 2025-12-05 14:00
**Status:** THESIS-READY, 100% POWER
**Relevance Score:** 0.75 (Methodological - power analysis for null results)

**Key Content (Lines 1-100):**
- **3-Way Interaction Test:** Age × LocationType × Time NULL
  - TSVR_hours:Age_c:LocationType: β=-0.0002, p=0.160 (NON-SIG)
  - log_TSVR:Age_c:LocationType: β=0.0052, p=0.329 (NON-SIG)
- **Power Analysis:** Power=1.00 (100%) [95% CI: 0.97-1.00]
  - Null finding is completely interpretable (not Type II error)
  - Study well-powered to detect small effects (β=0.01)
- **Age Effects at Day 3:**
  - Destination slope: -0.005 θ/year, p=0.74
  - Source slope: -0.005 θ/year, p=0.78
  - Contrast: p=0.99, Cohen's d=-0.02 (negligible)
- **Pattern:** 6/7 assumption checks passed (only residual normality failed due to Shapiro-Wilk sensitivity, LMM robust)

**Critical for 6.2.5:**
- Shows methodology for properly documenting null age effects
- Power analysis provides confidence that null findings are interpretable
- RQ 6.2.5 should similarly document power if finding age-invariance

---

## III. METHODOLOGICAL CONTEXT (TIME TRANSFORMATION & INTERACTION TESTING)

### Finding 6: Age Tertile Visualization Standard
**Source:** `.claude/context/archive/age_tertile_plot_methodology.md`
**Timestamp:** [Found in grep results, not fully read]
**Status:** METHODOLOGY REFERENCE
**Relevance Score:** 0.80 (Visualization)

**Key Context:**
- Age tertile cutoffs: Young ≤37y, Middle 37-52y, Older >52y (roughly balanced)
- Used consistently in RQ 5.5.3, 6.1.3, and likely RQ 6.2.5
- Dual-scale plots required per Decision D069 (theta + probability scales)

### Finding 7: Current Status - 13/31 RQs Thesis-Ready (42%)
**Source:** `.claude/context/current/state.md`
**Timestamp:** 2025-12-11 21:00
**Status:** CURRENT WORK STATUS
**Relevance Score:** 0.60 (Planning context)

**Key Content:**
- **Complete:** 6.1.1, 6.1.2, 6.1.3, 6.1.4, 6.1.5, 6.2.1, 6.2.2, 6.2.3, 6.2.4, 6.3.1, 6.4.1, 6.5.1, 6.8.1
- **Remaining ROOT:** 6.6.1 (HCE Over Time), 6.7.2 (Confidence Variability)
- **RQ 6.2.5:** Next in calibration series (4/5 complete after 6.2.4)
- **Execution Protocol:** 4-agent validation workflow (rq_inspect, rq_plots, rq_results, rq_validate)
- **Velocity:** 25 min/RQ, 2-3 RQs/session

---

## IV. SUMMARY FOR STATE.MD REFERENCE

**Timestamped Archive Topics for RQ 6.2.5 Context:**

1. **rq_6.2.1_calibration_worsens_thesis_ready.md** (2025-12-11 19:45)
   - ROOT RQ showing calibration worsens with time
   - Data merge procedures for theta/TSVR/confidence
   - LMM specification with random slopes
   - Calibration = z_theta_confidence - z_theta_accuracy

2. **rq_6.2.2_complete_overconfidence_trend_nonsig_thesis_ready.md** (2025-12-11 20:15)
   - Derivative showing direction shift is continuous, not categorical
   - Classification thresholds (±0.1) for robustness check
   - Related topic: rq_6.2.2_calibration_classification_epsilon_0.1.md

3. **rq_6.1.3_complete_age_effects_null_thesis_ready_zero_anomalies.md** (2025-12-11 16:45)
   - Age × Time NULL for CONFIDENCE (predicts age-invariant calibration)
   - Parallel RQs: 5.1.3, 5.2.3, 5.3.4, 5.4.3 all show age-invariant effects
   - Age centering: Age_c = Age - 44.57
   - Zero anomalies achieved with correct methodology

4. **rq_5.5.3_complete_age_effects_null_hypothesis_supported.md** (2025-12-05 14:00)
   - Shows how to document null age effects with power analysis
   - 100% statistical power demonstrates null finding is real, not Type II error

---

## V. PREDICTION FOR RQ 6.2.5

**Based on Archive Evidence (6 independent RQs):**

1. **Age × Time on Calibration likely NULL** (p>0.05)
   - Both components (confidence 6.1.3 and accuracy 5.1.3) show age-invariant decline
   - Their difference (calibration) should also be age-invariant

2. **Expected Pattern:** Similar to RQ 6.1.3
   - Age × Time interaction: p~0.30+ (non-significant)
   - Effect size negligible: ≤±0.05 theta units difference (older vs younger)
   - Supports age-invariant metacognitive monitoring hypothesis

3. **Cross-Validation:** Parallel structure with Chapter 5 age effects
   - RQ 5.1.3 (Age × Accuracy trajectory): NULL ✅
   - RQ 5.2.3 (Age × Domain): Pending confirmation
   - RQ 5.3.4 (Age × Paradigm): Pending confirmation
   - RQ 5.4.3 (Age × Schema): Pending confirmation
   - RQ 6.1.3 (Age × Confidence trajectory): NULL ✅
   - **RQ 6.2.5 (Age × Calibration trajectory): PREDICTED NULL**

4. **Data Source:** Continue from RQ 6.2.1 output
   - calibration scores: z_theta_confidence - z_theta_accuracy
   - TSVR mapping with composite_ID format conversion
   - Age from demographic data merged at Step 00

5. **Methodology:** Replicate RQ 6.1.3 structure
   - LMM: calibration ~ Time_log * Age_c + (1 + Time_log | UID)
   - Age centering at 44.57 (sample mean)
   - Decision D068: Dual p-values (Wald + LRT)
   - Decision D069: Age tertile plots (theta + probability scales)
   - Decision D039: If component accuracy data available, may need TSVR-specific IRT consideration

---

## VI. RECOMMENDATIONS FOR USER

**Before Starting RQ 6.2.5:**

1. **Review RQ 6.2.1 code** to understand calibration computation
   - Location: `results/ch6/6.2.1/code/steps_00_to_07.py`
   - Critical: z-standardization across all 400 observations

2. **Replicate RQ 6.1.3 structure** for age moderation
   - Location: `results/ch6/6.1.3/code/steps_00_to_06.py`
   - Time variable: Time_log (not TSVR raw)
   - Age variable: Age_c (centered at 44.57)
   - Interaction: Time_log × Age_c

3. **Prepare for likely NULL result**
   - Have power analysis ready (per RQ 5.5.3 methodology)
   - Document why null finding is interpretable
   - Integrate with age-invariant hypothesis across both accuracy and confidence

4. **Validation workflow**
   - Use 4-agent sequence: rq_inspect → rq_plots → rq_results → rq_validate
   - Target: ZERO ANOMALIES (as achieved in 6.1.3)
   - Expected time: ~25 minutes

---

**Search completed:** 2025-12-11 21:15
**Files searched:** 25+ archives
**Documentation cross-referenced:** docs/docs_index.md (data structure, irt/lmm methodology)
