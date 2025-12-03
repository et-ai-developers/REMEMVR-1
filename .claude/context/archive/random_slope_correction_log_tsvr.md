# Random Slope Correction - Log TSVR Specification Fix

**Topic:** random_slope_correction_log_tsvr
**Created:** 2025-12-03 (context-manager archival)
**Description:** Critical model correction fixing random slope specification across 3 RQs (5.2.4, 5.3.4, 5.4.3) from TSVR_hours to log_TSVR per ROOT RQ model selection, revealing meaningful individual differences previously masked.

---

## Session (2025-12-03 06:00) - CRITICAL MODEL CORRECTION

**Archived from:** state.md
**Original Date:** 2025-12-03 06:00
**Reason:** 3+ sessions old, complete work archived

**Task:** CRITICAL MODEL CORRECTION - Fix Random Slope Specification in 3 RQs

**Context:** User discovered RQ 5.2.4 was using wrong random slope specification (TSVR_hours instead of log_TSVR). Investigation revealed same error in RQ 5.3.4 and 5.4.3. ROOT RQ analyses (5.2.1, 5.3.1, 5.4.1) ALL selected Log model as best fit, meaning random slopes should be on log-transformed time.

**Major Accomplishments:**

**1. CRITICAL ERROR DISCOVERY**

**The Problem:**
- RQ 5.2.4, 5.3.4, 5.4.3 all had `re_formula="~TSVR_hours"` (linear time)
- But ROOT RQ analyses established Log model as best:
  - RQ 5.2.1: Log (AIC weight=61.9%)
  - RQ 5.3.1: Log (AIC weight=99.99%)
  - RQ 5.4.1: Log (AIC weight=100%)
- Random slope should align with dominant fixed effects time transformation

**The Symptom:**
- All three RQs showed TSVR_hours Var = 0.000 (boundary estimate)
- This MASKED individual differences in forgetting rates
- Models "converged" but estimated wrong variance components

**2. FIXES APPLIED TO 3 RQs**

| RQ | File Modified | Previous (WRONG) | Corrected |
|----|---------------|------------------|-----------|
| 5.2.4 | step03_fit_lmm.py | `re_formula="TSVR_hours"` | `re_formula="log_TSVR"` |
| 5.3.4 | step02_fit_lmm.py | `re_formula="~TSVR_hours"` | `re_formula="~log_TSVR"` |
| 5.4.3 | step02_fit_lmm.py | `re_formula='~TSVR_hours'` | `re_formula='~log_TSVR'` |

**3. RE-EXECUTION RESULTS**

| RQ | Previous Var | Corrected Var | Improvement |
|----|--------------|---------------|-------------|
| **5.2.4 IRT** | 0.000 | **0.021** | IRT detects individual forgetting rates |
| **5.2.4 CTT** | 0.000 | 0.000 (boundary) | CTT still can't detect (key finding!) |
| **5.3.4** | 0.0004 | **0.031** | 7.75× more variance detected |
| **5.4.3** | 0.000 | **0.019** | Meaningful individual differences |

**4. KEY FINDINGS FROM CORRECTED MODELS**

**RQ 5.2.4 (IRT-CTT Convergent Validity):**
- **CRITICAL FINDING:** IRT detects individual forgetting rate variance (0.021), CTT cannot (0.000)
- Static convergence exceptional: What r=0.906, Where r=0.970
- **Dynamic divergence:** IRT enables person-specific trajectories, CTT limited to group-average
- This supports hypothesis that IRT superior for individual trajectory modeling

**RQ 5.3.4 (Age × Paradigm):**
- NULL finding ROBUST: No significant 3-way interactions (all p > 0.7)
- Age effects uniform across IFR, ICR, IRE paradigms
- Model fit improved: AIC 2427 → 2209 (ΔAIC = -218)

**RQ 5.4.3 (Age × Congruence):**
- NULL finding ROBUST: No significant 3-way interactions (all p > 0.15)
- Age effects uniform across Common, Congruent, Incongruent items

**5. METHODOLOGICAL LESSON DOCUMENTED**

**Rule:** Random slopes must align with dominant fixed effects time transformation.
- If log_TSVR is dominant fixed effect, random slopes should be on log_TSVR
- Using TSVR_hours random slopes when forgetting is logarithmic underestimates variance
- Always check ROOT RQ model selection before specifying random slopes in derivative RQs

**6. RQ 5.4.1 VERIFIED CORRECT**

- Log model uses `re_formula="~TSVR_log"` (line 94) - CORRECT
- Other models (Linear, Quadratic, Lin+Log, Quad+Log) use TSVR_hours but those aren't selected
- Since Log model was selected and has correct spec, RQ 5.4.1 is fine

**7. VALIDATION PIPELINE COMPLETED**

All 3 corrected RQs validated via finisher agents:

| RQ | rq_inspect | rq_plots | rq_results |
|----|------------|----------|------------|
| 5.2.4 | ✅ PASS | ✅ PASS | ✅ PASS |
| 5.3.4 | ✅ PASS | ✅ Already existed | ✅ PASS |
| 5.4.3 | ✅ PASS | ✅ Already existed | ✅ PASS |

**8. Files Modified**

**Code Files Updated (3):**
- `results/ch5/5.2.4/code/step03_fit_lmm.py` (lines 312-317, 72-82)
- `results/ch5/5.3.4/code/step02_fit_lmm.py` (lines 26-32, 122-138)
- `results/ch5/5.4.3/code/step02_fit_lmm.py` (lines 7-11, 28, 137-154)

**Documentation Updated:**
- `results/ch5/5.2.4/docs/2_plan.md` (When exclusion patterns)

**Data/Results Regenerated:**
- All step03+ outputs for 5.2.4
- All step02+ outputs for 5.3.4 and 5.4.3
- Model summaries, fixed effects, plots

**Session Metrics:**

**Tokens:**
- Session start: ~5k (after /refresh)
- Session end: ~125k (at /save)
- Delta: ~120k consumed

**Critical Fixes:** 3 RQs corrected (5.2.4, 5.3.4, 5.4.3)

**Key Insights:**

**1. Silent Model Specification Errors:**
- Models "converge" even with wrong random effects
- Boundary estimates (Var=0.000) are the symptom
- Without knowing ROOT RQ model selection, error is invisible

**2. IRT vs CTT Dynamic Divergence:**
- With CORRECT model, IRT shows Var=0.021 (individual differences)
- CTT still shows Var=0.000 (boundary) - CTT genuinely can't detect slope variation
- This is key thesis finding: IRT superior for individual trajectory modeling

**3. Consistency of Random Slope Specification:**
- ROOT RQ model selection determines appropriate random effects for ALL derivative RQs
- Log model best → random slopes on log_TSVR
- Must propagate this consistently through pipeline

**End of Session (2025-12-03 06:00)**

---
