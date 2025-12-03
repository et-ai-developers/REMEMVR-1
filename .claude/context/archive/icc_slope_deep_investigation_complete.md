# ICC Slope Deep Investigation - Design Limitation Confirmed

**Topic:** icc_slope_deep_investigation_complete
**Created:** 2025-12-03 (context-manager archival)
**Description:** Complete 6-hypothesis investigation explaining ICC_slope = 0.0005 anomaly as sparse design limitation (4 timepoints, 93% shrinkage, random slopes don't improve fit) rather than analysis error or biological reality.

---

## Session (2025-12-03 14:30) - Deep Investigation Complete

**Archived from:** state.md
**Original Date:** 2025-12-03 14:30
**Reason:** 3+ sessions old, complete work archived

**Task:** DEEP INVESTIGATION - Why Can't We Detect Individual Slope Differences?

**Context:** User challenged the ICC_slope = 0.0005 finding, refusing to accept it as a real biological effect. Conducted comprehensive investigation testing 6 different hypotheses.

**Major Accomplishments:**

**1. Investigation 1: Scale Transformation (Theta → Probability)**

Converted theta to probability via Test Characteristic Curve (TCC), re-fit LMM.

| Scale | ICC_slope |
|-------|-----------|
| Theta (original) | 0.0005 |
| Probability (TCC) | 0.0017 |

**Verdict:** Only 3.5× improvement. ICC still 200× below literature. **NOT the primary cause.**

**2. Investigation 2: Model Specification (Wrong Random Slope Variable)**

Discovered Lin+Log model had random slopes on `Days`, not `log_TSVR`.

| Model | var_slope | ICC_slope |
|-------|-----------|-----------|
| Lin+Log with Days slopes | 0.000157 | 0.0005 |
| Lin+Log with log_TSVR slopes | 0.003346 | 0.011 |

**Verdict:** 22× improvement with correct specification. Still far below literature. **Partial explanation.**

**3. Investigation 3: Shrinkage from Sparse Design (THE KEY FINDING)**

With only 4 timepoints per participant, individual slopes are estimated with massive uncertainty.

| Metric | Raw OLS | LMM BLUP | Shrinkage |
|--------|---------|----------|-----------|
| Slope SD | 0.209 | 0.017 | **92%** |
| Slope variance | 0.044 | 0.003 | **93%** |

**Critical insight:** The model shrinks slope variance by 93%! This is **not bias** - it's the LMM correctly handling unreliable estimates.

**Reliability of individual slopes:**
- With n=4 timepoints, df for slope estimation = 2
- Estimated reliability = 14-51% depending on calculation
- Half or more of apparent "individual slope differences" is measurement error

**4. Investigation 4: Likelihood Ratio Test for Random Slopes**

**Critical test:** Do random slopes significantly improve model fit?

```
Full model (intercepts + slopes): LL = -429.65
Reduced model (intercepts only): LL = -430.02
LR statistic = 0.76, p = 0.685
```

**Verdict:** Random slopes do NOT significantly improve fit. The simpler random-intercepts-only model is preferred (lower AIC: 870.05 vs 873.29).

**5. Investigation 5: Time-Varying Covariates (Sleep, Tiredness)**

Extracted sleep hygiene data from master.xlsx for all 4 tests per participant:
- hours_slept (mean = 7.09, SD = 1.36)
- hours_awake (mean = 8.07, SD = 4.02)
- sleep_quality (mean = -0.02, SD = 0.43)
- tiredness (mean = -0.16, SD = 0.44)

| Model | var_residual | ICC_slope |
|-------|--------------|-----------|
| Without sleep covariates | 0.3106 | 0.0107 |
| With sleep covariates | 0.3104 | 0.0104 |

**Fixed effects of sleep:**
- hours_slept: b = 0.023, t = 0.70 (NOT significant)
- tiredness: b = -0.044, t = -0.44 (NOT significant)

**LR test after covariates:** p = 0.694 (still not significant)

**Verdict:** Sleep variables explain 0% of within-person variance. **Covariates do not help.**

**6. Investigation 6: Extended Model Comparison**

Tested additional functional forms beyond original 5 candidates:

| Model | AIC | ΔAIC | ICC_slope |
|-------|-----|------|-----------|
| Quad+Log | 872.92 | 0.00 | 0.012 |
| Lin+Log | 873.29 | 0.37 | 0.011 |
| Log(days+1) | 873.71 | 0.79 | ~0 (boundary) |
| Exp decay (τ=3d) | 873.78 | 0.85 | ~0 (boundary) |
| Power -0.2 | 891.04 | 18.11 | 0.317 |
| Power -0.3 | 896.85 | 23.93 | 0.215 |

**Observation:** Power law models show higher ICC_slope (0.22-0.32) but fit much worse (ΔAIC > 18). No well-fitting model shows substantial slope variance.

**7. Dichotomous Data Information Loss Analysis**

| Metric | Value |
|--------|-------|
| Items per test | 68 (after purification) |
| Binomial SE of sum score | 3.17 items |
| Binomial SE of change score | 4.49 items |
| Observed SD of T1→T4 change | 10.28 items |
| Signal-to-noise ratio | 2.29 |
| Reliability of change scores | 81% maximum |

Even with perfect analysis, dichotomous data limits slope reliability to ~80%.

**Key Finding: Summary**

**The finding is NOT an artifact of:**
- ❌ Scale (theta vs probability) - only 3.5× improvement
- ❌ Model specification (after correction) - only 22× improvement
- ❌ Sleep/state covariates - no effect

**The finding IS explained by:**
- ✅ **Sparse design:** 4 timepoints → 14-51% reliability for slopes
- ✅ **Appropriate shrinkage:** LMM correctly downweights unreliable estimates
- ✅ **LR test:** Random slopes don't improve model fit (p = 0.69)
- ✅ **Raw data:** Even unshrunk, raw ICC = 0.12 (still below literature 0.30-0.50)

**Files Created/Modified:**

| File | Action |
|------|--------|
| `results/ch5/story.md` | UPDATED - Added "Deep Investigation" section (~190 lines) |
| `results/ch5/5.1.4/code/step06_theta_to_prob_investigation.py` | CREATED - Scale transformation analysis |
| `results/ch5/5.1.4/data/step06_probability_trajectories.csv` | CREATED - Theta→probability conversion |
| `results/ch5/5.1.4/data/step07_prob_lmm_input.csv` | CREATED - LMM input on probability scale |
| `results/ch5/5.1.4/data/step08_prob_variance_components.csv` | CREATED - Probability-scale variance |
| `results/ch5/5.1.4/data/step09_prob_icc_estimates.csv` | CREATED - Probability-scale ICC |
| `results/ch5/5.1.4/results/step10_scale_comparison.md` | CREATED - Theta vs probability comparison |
| `results/ch5/5.1.4/data/step10_lmm_with_sleep.csv` | CREATED - LMM input merged with sleep covariates |

**Thesis Framing Recommendation:**

**You CANNOT claim:**
- "People don't differ in forgetting rates" (design lacks power to detect)
- "VR memory has homogeneous forgetting" (unfalsifiable with this design)
- "Forgetting is a universal process" (overgeneralization)

**You CAN claim:**
- "This design was optimized for group-level trajectory modeling, not individual slope estimation"
- "ICC for intercepts (0.57) confirms reliable between-person baseline differences"
- "Random slopes did not improve model fit, though this may reflect insufficient timepoints (n=4) rather than absence of true differences"
- "Future studies with more intensive longitudinal sampling are needed to characterize individual forgetting rates"

**Recommendation: Do NOT Report ICC_slope**

Instead:
1. Report **fixed effects** (population-level forgetting curve) - well-powered, robust
2. Report **ICC_intercept** (0.57) - reliable individual differences in baseline
3. Note in limitations: "Individual forgetting rates could not be reliably estimated with 4 timepoints per participant"
4. Recommend future work: "Intensive longitudinal designs (8+ timepoints) needed for individual trajectory analysis"

**The One Hope: Confidence Data (Chapter 6)**

Confidence ratings (1-5 scale) may reveal individual slope differences that dichotomous accuracy cannot:
- Continuous, not dichotomous → higher reliability
- Each item provides 5× more information
- If confidence shows ICC_slope ≈ 0.30 while accuracy shows 0.01, points to accuracy measurement limitation

**Session Metrics:**

**Tokens:**
- Session start: ~8k (after /refresh)
- Session end: ~180k (at /save)
- Delta: ~172k consumed

**Investigations completed:** 6 major analyses
**Scripts written:** 1 (theta→probability investigation)
**Data files created:** 5
**story.md updated:** Yes (~190 lines added)

**End of Session (2025-12-03 14:30)**

---
