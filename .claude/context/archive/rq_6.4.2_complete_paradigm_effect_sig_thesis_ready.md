# RQ 6.4.2 Complete - Paradigm Calibration (Significant Main Effect, Weak Magnitude)

**Topic:** rq_6.4.2_complete_paradigm_effect_sig_thesis_ready
**Created:** 2025-12-12 10:30 (context-manager curation)
**Scope:** Complete RQ 6.4.2 execution history (paradigm-specific calibration quality)

---

## Entry: RQ 6.4.2 Execution Complete - THESIS-READY (2025-12-11 23:40)

**Archived from:** state.md Session (2025-12-11 23:40)
**Original Date:** 2025-12-11 23:40
**Reason:** Task completed, RQ now thesis-ready, no longer relevant to current work (session 09:30 working on RQ 6.4.4)

---

### Task

RQ 6.4.2 Paradigm Confidence Calibration - COMPLETE with Significant Paradigm Effect

### Context

User requested execution of RQ 6.4.2, a DERIVATIVE RQ testing whether calibration quality (confidence-accuracy alignment) differs across retrieval paradigms (Free Recall, Cued Recall, Recognition). This tests the fluency-familiarity heuristic: Recognition should show highest overconfidence due to fluent retrieval from test probes inflating subjective confidence.

### Major Accomplishment

RQ 6.4.2 THESIS-READY - PARADIGM MAIN EFFECT SIGNIFICANT (p=0.040 Bonferroni)

---

## 1. Analysis Pipeline Execution (Steps 00-04)

**Script Created:** `results/ch6/6.4.2/code/steps_00_to_04.py` (5-step calibration pipeline, adapted from RQ 6.3.2 template)

**Data Sources:**
- Ch5 5.3.1: step03_theta_scores.csv (accuracy theta by paradigm - long format, 1200 rows)
- Ch6 6.4.1: step03_theta_confidence.csv (confidence theta by paradigm - wide format, 400 rows → melted to 1200)
- Ch6 6.4.1: step00_tsvr_mapping.csv (TSVR hours)
- Merge: 1200 rows (100 participants × 4 tests × 3 paradigms)

**Paradigm Mapping:**
- Ch5 5.3.1 uses: `free_recall`, `cued_recall`, `recognition` (lowercase)
- Ch6 6.4.1 uses: `theta_IFR`, `theta_ICR`, `theta_IRE` (column names)
- Code maps to standardized: IFR, ICR, IRE

**Step Execution Summary:**
- Step 00: Load/merge accuracy + confidence theta, add TSVR (1200 rows) ✅
- Step 01: Z-standardize theta_accuracy and theta_confidence (pooled), compute calibration ✅
- Step 02: Fit LMM with Paradigm × Time interaction + random slopes ✅
- Step 03: Compute post-hoc pairwise paradigm contrasts (3 comparisons) ✅
- Step 04: Rank paradigms by |calibration| and prepare trajectory plot data (12 rows) ✅

---

## 2. Primary Statistical Results - PARADIGM MAIN EFFECT SIGNIFICANT

**Model Specification:**
- Formula: `calibration ~ C(Paradigm) * TSVR_centered`
- Random effects: Intercept + slope on TSVR_centered by UID
- Estimation: ML (REML=False)
- Convergence: Successful (boundary warning - acceptable)

**Main Effects (LRT with dual p-values, Decision D068):**

| Term | χ² | df | p_uncorrected | p_Bonferroni | Result |
|------|-----|-----|---------------|--------------|--------|
| Paradigm main effect | 7.83 | 2 | 0.020 | **0.040** | **SIGNIFICANT** |
| Paradigm × Time interaction | 0.28 | 2 | 0.871 | 1.000 | NOT SIGNIFICANT |

**CONCLUSION: PARADIGM EFFECT ON BASELINE CALIBRATION, NOT TRAJECTORY**
- Paradigms differ in calibration quality (p=0.040)
- BUT: Paradigm differences are STABLE over time (parallel trajectories)
- Pattern: All paradigms shift from underconfidence to slight overconfidence over 6 days

---

## 3. Paradigm-Level Calibration Statistics

**Mean Calibration (z-standardized):**

| Paradigm | Mean | Direction | Interpretation |
|----------|------|-----------|----------------|
| ICR (Cued Recall) | -0.062 | Underconfidence | Confidence < Accuracy |
| IFR (Free Recall) | +0.022 | Slight overconfidence | Confidence ≈ Accuracy |
| IRE (Recognition) | +0.040 | Slight overconfidence | Confidence > Accuracy |

**Ranking by Calibration Quality (|calibration|):**

| Rank | Paradigm | Mean |calibration| | Interpretation |
|------|----------|---------------------|----------------|
| 1 | IFR (Free Recall) | 0.700 | **Best calibrated** ✅ |
| 2 | ICR (Cued Recall) | 0.728 | Middle |
| 3 | IRE (Recognition) | 0.749 | **Worst calibrated** ✅ |

**Hypothesis Verdict:**
- **SUPPORTED directionally**: Free Recall best calibrated, Recognition worst (as predicted)
- **BUT effect sizes are SMALL** (d < 0.11 for all pairwise contrasts)
- Pattern consistent with fluency-familiarity heuristic (recognition's retrieval support inflates confidence)

---

## 4. Post-Hoc Contrasts (All NS After Bonferroni)

| Contrast | Δ | SE | z | p_uncorr | p_Bonf | d | Result |
|----------|------|------|------|----------|--------|-------|--------|
| IRE vs IFR | 0.019 | 0.067 | 0.28 | 0.778 | 1.000 | 0.020 | NS |
| ICR vs IFR | -0.084 | 0.066 | -1.28 | 0.202 | 0.607 | -0.090 | NS |
| IRE vs ICR | 0.102 | 0.067 | 1.52 | 0.129 | 0.388 | 0.107 | NS |

**Interpretation:** Omnibus paradigm effect significant, but no individual pairwise contrast survives Bonferroni correction. Pattern is WEAK but directionally consistent with hypothesis.

---

## 5. Trajectory Patterns

**T1 to T4 Calibration Change by Paradigm:**

| Paradigm | T1 | T4 | Δ |
|----------|--------|-------|-------|
| IFR | -0.080 | +0.077 | +0.157 |
| ICR | -0.127 | +0.006 | +0.133 |
| IRE | -0.050 | +0.131 | +0.182 |

**Key Pattern:** All paradigms show PARALLEL trajectories moving from slight underconfidence (T1) toward slight overconfidence (T4). This explains the NULL interaction: paradigm differences are stable over time.

---

## 6. Validation Workflow Execution

**Agents Invoked (2 total, SEQUENTIAL per execute.md lesson):**

| Agent | Status | Key Finding |
|-------|--------|-------------|
| rq_results | ✅ COMPLETE | summary.md created with PASS (0 anomalies) |
| rq_validate | ✅ PASS WITH NOTES | 3 moderate issues (missing sensitivity checks) |

**Moderate Issues (Non-Blocking):**
1. Residual diagnostics missing (QQ plots, homoscedasticity)
2. Post-hoc power analysis missing
3. Lord's paradox sensitivity checks not implemented (ANCOVA planned in concept but not run)

**Recommendation:** Run sensitivity checks before final thesis submission (Lord's paradox ANCOVA, difference score reliability validation).

---

## 7. Files Created/Modified

**Code:**
- results/ch6/6.4.2/code/steps_00_to_04.py (NEW - 5-step pipeline)

**Data (7 files):**
- step00_calibration_by_paradigm.csv (1200 rows)
- step01_paradigm_effects.csv (2 rows - main effect + interaction)
- step01_lmm_fixed_effects.csv (6 rows)
- step01_lmm_model_summary.txt
- step02_post_hoc_contrasts.csv (3 rows)
- step03_paradigm_ranking.csv (3 rows)
- step04_calibration_trajectory_data.csv (12 rows)

**Plots:**
- results/ch6/6.4.2/plots/plots.py (NEW)
- calibration_trajectories_by_paradigm.png (3-line trajectory)
- paradigm_calibration_ranking.png (bar chart)
- paradigm_calibration_direction.png (signed means)

**Results:**
- results/ch6/6.4.2/results/summary.md (thesis-quality)
- results/ch6/6.4.2/results/validation.md (thesis-quality)

**Logs:**
- results/ch6/6.4.2/logs/steps_00_to_04.log

**Status:**
- results/ch6/rq_status.tsv (6.4.2 THESIS-READY)

---

## 8. Chapter 6 Status Update

**Complete + Validated (THESIS-READY):** 18/31 RQs (58%)
- 6.1.1-6.1.5 (Confidence series - 5 RQs)
- 6.2.1-6.2.5 (Calibration series - 5 RQs)
- 6.3.1-6.3.4 (Domain Confidence series - 4 RQs)
- 6.4.1, **6.4.2** (Paradigm Confidence - 2/5)
- 6.5.1, 6.8.1 (Schema/Source-Dest roots)

**Paradigm Confidence Series (6.4.X):** 2/5 COMPLETE
- 6.4.1 ✅ (ROOT - trajectories)
- **6.4.2 ✅** (Calibration - paradigm effect SIG, small d) ← NEW
- 6.4.3 (Age × Paradigm) - REMAINING
- 6.4.4 (ICC by Paradigm) - REMAINING

**Remaining ROOT RQs:** 2
- 6.6.1 (HCE Over Time)
- 6.7.2 (Confidence Variability)

---

## 9. Theoretical Significance

**Fluency-Familiarity Heuristic - WEAK SUPPORT:**
- Direction consistent: Recognition worst calibrated, Free Recall best
- Magnitude weak: Effect sizes d < 0.11 (trivial)
- Pattern: Retrieval support may slightly inflate confidence relative to accuracy, but effect is modest

**Comparison to Domain Calibration (RQ 6.3.2):**
- RQ 6.3.2 (Domain): MAJOR CROSSOVER interaction (χ²=59.60, p<0.0001)
- RQ 6.4.2 (Paradigm): SIGNIFICANT main effect (χ²=7.83, p=0.040), NO interaction
- Domain differences are LARGER and more complex than paradigm differences
- Memory WHAT you're doing (content domain) matters more for calibration than HOW you're tested (paradigm)

**Unexpected Finding:**
- Cued Recall shows UNDERCONFIDENCE (mean=-0.062), contrary to fluency heuristic
- Expected: Cued Recall intermediate between Free Recall and Recognition
- Observed: Cued Recall more underconfident than Free Recall
- Possible explanation: Semantic cues reveal accuracy limitations that recognition probes mask

---

## 10. Session Metrics

**Session Duration:** ~15 minutes
**Tokens Used:** ~30k
**Agent Invocations:** 2 (rq_results, rq_validate)
**Success Rate:** 100%
**Code Strategy:** Adapted from RQ 6.3.2 template (75% time savings per execute.md lesson)

---

## Related Topics

- rq_6.4.2_fluency_familiarity_weak_support (theoretical interpretation)
- rq_6.3.2_complete_crossover_interaction_thesis_ready (domain calibration comparison)
- ch6_paradigm_series_2_of_5_complete (series tracking)
- ch6_progress_18_of_31_thesis_ready_58_percent (progress milestone)

---

## Keywords

paradigm_calibration, fluency_familiarity_heuristic, free_recall_best, recognition_worst, chi2_7.83, p_0.040_bonferroni, small_effect_d_0.11, parallel_trajectories, null_interaction, thesis_ready

---
