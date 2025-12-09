# RQ 5.1.4: Variance Decomposition (MODEL-AVERAGED UPDATE)

**Date:** 2025-12-09
**Version:** v4.X (Model-Averaged, GOLD status)

---

## CRITICAL FINDING: Forgetting Rate IS Trait-Like

### Model-Averaged Results (65 models tested, 10 averaged)

**Variance Components:**
- `var_intercept_avg` = 0.422 (substantial between-person baseline variance)
- `var_slope_avg` = 0.098 (substantial between-person forgetting rate variance)
- `var_residual` = 0.319

**ICCs:**
- `ICC_intercept` = 56.95% (baseline ability is trait-like, as expected)
- **`ICC_slope_simple` = 21.61%** (forgetting rate IS trait-like, contrary to original finding!)

**Competitive Models (ΔAIC < 2.0):**
1. PowerLaw_04 (α=0.4): AIC=871.29, weight=5.7%
2. PowerLaw_05 (α=0.5): AIC=871.43, weight=5.3%
3. PowerLaw_03 (α=0.3): AIC=871.52, weight=5.1%
4. LogLog: AIC=871.58, weight=4.9%
5. Root_033 (α=0.33): AIC=871.74, weight=4.6%
6. CubeRoot: AIC=871.74, weight=4.6%
7. PowerLaw_06 (α=0.6): AIC=871.90, weight=4.2%
8. FourthRoot: AIC=871.99, weight=4.0%
9. PowerLaw_02 (α=0.2): AIC=872.13, weight=3.7%
10. PowerLaw_07 (α=0.7): AIC=872.67, weight=2.9%

**Effective N models:** 9.84 (high functional form uncertainty)

---

## Comparison to Single-Model Analysis (Lin+Log)

| Metric | Lin+Log (v3.0) | Model-Averaged (v4.X) | Fold Increase |
|--------|----------------|----------------------|---------------|
| **var_slope** | 0.000157 | 0.097874 | **430×** |
| **ICC_slope_simple** | 0.0005 (0.05%) | 0.216077 (21.61%) | **432×** |
| **Conclusion** | NOT trait-like | **IS trait-like** | - |

---

## Theoretical Implications

### Original Interpretation (REJECTED)

**Lin+Log single model:** ICC_slope=0.05% → Forgetting rate is NOT a stable cognitive trait, minimal between-person variance, primarily measurement error or state-dependent effects.

### Model-Averaged Interpretation (REVISED)

**Model averaging across power law variants:** ICC_slope=21.61% → Forgetting rate **IS a stable cognitive trait** with **moderate between-person variance** (20-40% range indicates meaningful individual differences).

**Why the discrepancy?**
- **Single-model bias:** Lin+Log functional form systematically underestimates slope variance
- **Power law variants** (α=0.2-0.7) capture individual differences in forgetting trajectories better than Log or Lin+Log
- **Model uncertainty was high:** Effective N=9.84 competitive models → NO SINGLE BEST MODEL
- **Model averaging is mandatory** when functional form uncertainty is this extreme

---

## Implications for RQ 5.1.5 (Clustering)

**Original concern (from ICC investigation 2025-12-03):**
"With ICC_slope=0.05%, clustering on slopes unjustified (LR test p=0.685)"

**Model-averaged finding:**
ICC_slope=21.61% **SUPPORTS** clustering analysis in RQ 5.1.5. Individuals DO differ meaningfully in forgetting rates, justifying person-centered analysis (fast vs slow forgetters).

**Action:** RQ 5.1.5 should be RE-EVALUATED using model-averaged random slopes (not single-model slopes).

---

## Methodological Lesson

**v3.0 Workflow (FLAWED):**
1. Test 5 basic models (Linear, Quadratic, Log, Lin+Log, Quad+Log)
2. Select "best" model by AIC
3. Extract variance components from single model
4. Interpret ICC as if functional form certain

**v4.X Workflow (ROBUST):**
1. Test 65+ models (including power law variants)
2. Identify competitive models (ΔAIC < 2.0)
3. Model-average variance components using Akaike weights
4. Acknowledge functional form uncertainty in interpretation

**When to use model averaging:**
- Effective N < 10 (high uncertainty)
- Best model weight < 30% (no clear winner)
- Theoretical ambiguity (power law vs logarithmic forgetting debate)
- Variance decomposition (variance components are functional-form sensitive)

---

## Files Generated (Step 06)

1. `data/step06_model_comparison.csv` - 65 models with AIC/weights
2. `data/step06_competitive_models_metadata.yaml` - 10 competitive models
3. `data/step06_averaged_variance_components.csv` - Model-averaged variance
4. `data/step06_averaged_iccs.csv` - Model-averaged ICCs
5. `data/step06_model_specific_variance.csv` - Transparency (per-model variance)
6. `data/step06_averaged_random_effects.csv` - 100 participants, model-averaged intercepts/slopes

---

## Status

**RQ 5.1.4:** ✅ **READY FOR GOLD** (pending final status update)

**Next Steps:**
1. Update rq_status.tsv (COMPLETE → GOLD)
2. Update RQ 5.1.5 to use model-averaged random slopes
3. Document in thesis Methods: "Model averaging mandatory for variance decomposition when functional form uncertain"

---

**Generated:** 2025-12-09
**Tool:** `tools/variance_decomposition.py::compute_model_averaged_variance_decomposition()`
**Architecture:** v4.X atomic agents
