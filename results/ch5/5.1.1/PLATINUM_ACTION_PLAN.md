# RQ 5.1.1 - PLATINUM Finalization Action Plan

**Generated:** 2025-12-27
**Agent:** rq_platinum
**Current Status:** NEAR-PLATINUM (validation.md: PASS WITH NOTES)

---

## Priority: HIGH (Mandatory Before PLATINUM)

### 1. LMM Diagnostic Plots (Section 5.1) - **BLOCKER**
- **Issue:** Residual diagnostics missing (validation.md M1)
- **Action:** Generate 3 diagnostic plots from step05c_averaged_predictions.csv
  1. Q-Q plot (test normality of residuals)
  2. Residuals vs Fitted (test homoscedasticity)
  3. Cook's Distance (identify influential observations)
- **Time:** 30-45 minutes
- **Output:** plots/diagnostics_model_averaged.png
- **Success Criteria:**
  - Q-Q plot shows residuals approximately normal
  - Residuals vs fitted shows no funnel pattern
  - No Cook's D > 1.0 (no extreme outliers)

### 2. Formal Effect Size with CI (Section 3.3) - **HIGH**
- **Issue:** Effect size CIs missing (validation.md M2)
- **Action:** Compute Cohen's d for Day 0 → Day 6 decline
  - Extract theta means and SDs from step04_lmm_input.csv
  - Compute d = (M_T1 - M_T4) / SD_pooled
  - Bootstrap 95% CI (1000 iterations)
- **Time:** 20-30 minutes
- **Output:** Update summary.md Section 1 with "Cohen's d = X.XX [95% CI: X.XX, X.XX]"
- **Success Criteria:** Formal effect size with uncertainty quantified

---

## Priority: MEDIUM (Recommended Enhancements)

### 3. Model-Averaged Residual Diagnostics (Section 5.1)
- **Issue:** Diagnostics should be for model-averaged predictions (not single model)
- **Action:** Verify step05d_model_averaged_residuals.csv exists
  - If yes: Generate plots from this file
  - If no: Compute residuals = observed - MA_predictions
- **Time:** 15-20 minutes
- **Output:** Residual diagnostic plots using MA predictions

### 4. Add Uncertainty Bands to Plots (Section 7.3)
- **Issue:** Current plots show MA predictions but no ±SE shading
- **Action:** Regenerate plots with uncertainty shading
  - Use step05c_averaged_predictions.csv SE column
  - Add shaded ±1.96*SE region around MA trajectory
- **Time:** 20-30 minutes
- **Output:** Update functional_form_theta.png and functional_form_probability.png
- **Success Criteria:** Plots show between-model uncertainty visually

---

## Priority: LOW (Optional Polish)

### 5. Verify Random Slopes Model (Section 4.4)
- **Issue:** concept.md specifies random slopes, code implements intercepts only
- **Action:** Document rationale OR test random slopes model
  - Option A: Document "Random intercepts only appropriate for functional form comparison (4 time points insufficient for stable slope estimation)"
  - Option B: Fit random slopes model, compare AIC (expect overfitting)
- **Time:** 30-40 minutes if testing, 5 minutes if documenting only
- **Output:** Update summary.md Section 4 (Limitations) OR validation.md

### 6. Cross-Validate Model Averaging α_eff (Section 4.1)
- **Issue:** Effective α=0.410 is weighted mean, no CI reported
- **Action:** Compute 95% CI for α_eff
  - Bootstrap model selection (resample data, refit 66 models, extract α_eff)
  - Report α_eff = 0.410 [95% CI: X.XX, X.XX]
- **Time:** 1-2 hours (computationally intensive)
- **Output:** Update summary.md Section 1 with α_eff CI
- **Success Criteria:** Quantifies parameter uncertainty of effective exponent

---

## Estimated Total Time

**HIGH Priority (Mandatory):** 50-75 minutes
**MEDIUM Priority (Recommended):** 35-50 minutes
**LOW Priority (Optional):** 35 minutes - 2.5 hours

**TOTAL FOR PLATINUM STATUS:** 1.5-3 hours

---

## PLATINUM Certification Checklist

After completing HIGH priority items:

- ✅ Statistical rigor: Assumptions validated (diagnostics), effect sizes with CIs
- ✅ Methodological soundness: Model averaging (66 models → 16 competitive)
- ✅ Documentation excellence: Dual p-values N/A (AIC not NHST), dual scales ✅, plots current ✅
- ✅ Data quality: IRT purification documented (64.8% retention)
- ✅ Theoretical coherence: Power-law theory (Wixted & Ebbesen 1991), mechanisms explained
- ✅ Zero critical issues: No convergence failures, no missing analyses, outputs current

---

## Implementation Order

**Phase 1 (BLOCKER resolution, 50-75 min):**
1. Generate LMM diagnostic plots (30-45 min)
2. Compute Cohen's d with bootstrap CI (20-30 min)

**Phase 2 (Recommended enhancements, 35-50 min):**
3. Verify/generate MA residual diagnostics (15-20 min)
4. Add uncertainty bands to plots (20-30 min)

**Phase 3 (Optional polish, as time allows):**
5. Document random effects rationale (5 min) OR test random slopes (30-40 min)
6. Bootstrap α_eff CI (1-2 hours, optional)

---

**Next Step:** Execute Phase 1, Task 1 - Generate LMM diagnostic plots
