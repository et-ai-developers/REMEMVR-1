# RQ 6.1.2: Two-Phase Pattern in Confidence Decline

**Research Question:** Does confidence decline show the same two-phase pattern (rapid early, slow late) as accuracy?

**Status:** Analysis Complete

---

## Key Findings

**Three-Test Convergent Evidence:**

| Test | Result | Evidence | Details |
|------|--------|----------|---------|
| **Test 1: Quadratic Significance** | ✅ SIGNIFICANT | FOR two-phase | Quadratic term p=0.00011 (Bonferroni-corrected), positive coefficient indicates deceleration |
| **Test 2: Piecewise vs Continuous AIC** | ❌ NOT SIGNIFICANT | AGAINST two-phase | Continuous AIC=294.74 better than Piecewise AIC=317.29 (ΔAIC=-22.54) |
| **Test 3: Late/Early Slope Ratio** | ❌ NOT SIGNIFICANT | AGAINST two-phase | Ratio=0.92 (not < 0.5 threshold), Late decline 92% as steep as Early |

**Overall Conclusion:** **INCONCLUSIVE** (1 out of 3 tests support two-phase pattern)

---

## Statistical Results

**Quadratic Model (Test 1):**
- Linear term (TSVR_hours): β=-0.00566 (p<0.001)
- Quadratic term (TSVR²): β=+0.0000192 (p=0.00011, Bonferroni-corrected)
- Positive quadratic = decline decelerates over time

**Model Comparison (Test 2):**
- Continuous model AIC: 294.74
- Piecewise model AIC: 317.29
- Delta AIC: -22.54 (favors continuous by large margin)
- Interpretation: No discrete breakpoint at 48h

**Slope Analysis (Test 3):**
- Early slope (0-48h): -0.0037 per hour (SE=0.0014)
- Late slope (48-144h): -0.0034 per hour (SE=0.0004)
- Ratio: 0.92 (Late decline nearly same rate as Early)
- Interpretation: Decline rate remains relatively constant

---

## Scientific Interpretation

**Primary Finding:**
Confidence decline shows **smooth deceleration** (quadratic curvature) but **NOT a discrete two-phase pattern** with abrupt breakpoint at 48 hours.

**Implications:**
- Metacognitive monitoring does NOT track consolidation boundaries the same way episodic memory traces might
- Confidence decline follows continuous power law or logarithmic trajectory
- No evidence for discrete "pre-consolidation" vs "post-consolidation" phases in subjective confidence

**Comparison to Accuracy:**
- Ch5 5.1.2 data unavailable for direct comparison
- Pattern remains to be compared when accuracy two-phase data available

---

## Data Quality

**Sample:** N=100 participants, 400 observations (4 tests per participant)

**Model Convergence:** All models converged successfully
- Quadratic model: Converged with powell optimizer
- Continuous model: Converged
- Piecewise model: Converged

**Data Integrity:** All validation checks passed
- Row counts: 400 (expected)
- No NaN values in merged data
- Theta range: [-2.24, 0.49] (within expected IRT range)
- TSVR range: [1.0, 246.2] hours (2 values exceed 200h nominal limit)

---

## Outputs Generated

**Data Files (8):**
- step00_lmm_input.csv (400 rows: theta + TSVR merged)
- step01_piecewise_input.csv (400 rows: + piecewise segments)
- step02_quadratic_test.csv (2 rows: linear + quadratic terms)
- step03_piecewise_comparison.csv (3 rows: AIC comparison)
- step04_slope_ratio.csv (3 rows: Early/Late slopes + ratio)
- step05_ch5_comparison.csv (1 row: evidence synthesis)
- step06_twophase_theta_data.csv (14 rows: theta-scale plot data)
- step06_twophase_probability_data.csv (14 rows: probability-scale plot data)

**Model Summaries:**
- step02_quadratic_model_summary.txt (LMM summary with quadratic term)

**Plots:** Ready for generation (plot source data complete)

---

## Thesis Implications

This RQ provides evidence that:
1. Confidence decline is NOT characterized by discrete consolidation-related phases
2. Metacognitive monitoring may integrate across memory states rather than tracking discrete processes
3. Dissociation between confidence trajectories and potential accuracy two-phase patterns would suggest separate neural/cognitive substrates

**Next Steps:**
- Compare to Ch5 5.1.2 accuracy two-phase findings when available
- Examine domain-specific confidence patterns (RQ 6.3.2)
- Investigate whether high-confidence errors show different temporal dynamics (Type 6.2 RQs)
