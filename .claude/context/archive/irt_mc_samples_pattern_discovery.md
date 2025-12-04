# IRT Monte Carlo Samples Pattern Discovery

**Topic:** IRT mc_samples configuration pattern across ROOT RQs - model_fit vs model_scores distinction
**Created:** 2025-12-05 (context-manager)
**Status:** Active

---

## IRT Settings Fix - mc_samples=1 for model_fit, 100 for model_scores (2025-12-05 09:30)

**Task:** Complete RQ 5.5.1 Production Execution + IRT Settings Fix + Plots Fix

**Context:** Discovered critical IRT configuration error causing RQ 5.5.1 to run 100× slower than other ROOT RQs. Investigation revealed systematic pattern across all ROOT RQs (5.1.1, 5.2.1, 5.3.1, 5.4.1) that was violated in 5.5.1.

**Archived from:** state.md Session (2025-12-05 09:30)
**Original Date:** 2025-12-05 09:30
**Reason:** Session current (N), but pattern documentation is orthogonal completed work

---

### Problem Discovered

**Symptom:** RQ 5.5.1 IRT calibration was taking hours to complete, vs ~161 seconds for other ROOT RQs.

**Root Cause:** `model_fit.mc_samples=100` instead of `1`

**Pattern Analysis Across All ROOT RQs:**

| RQ | model_fit.mc_samples | model_scores.mc_samples | Runtime |
|----|----------------------|-------------------------|---------|
| 5.1.1 | **1** | 100 | ~161 sec |
| 5.2.1 | **1** | 100 | ~161 sec |
| 5.3.1 | **1** | 100 | ~161 sec |
| 5.4.1 | **1** | 100 | ~161 sec |
| 5.5.1 (WRONG) | 100 | 100 | hours |
| 5.5.1 (FIXED) | **1** | 100 | ~161 sec |

### Correct Pattern Documentation

**IRT MEDIUM Settings (Production Quality):**

```python
# model_fit: Point estimates for item parameters (FAST)
model_fit = pyro.infer.SVI(
    model=model,
    guide=guide,
    optim=optimizer,
    loss=pyro.infer.Trace_ELBO()
)

model_fit.mc_samples = 1  # Point estimates only, no Monte Carlo integration needed

# model_scores: Monte Carlo integration for theta (ACCURATE)
model_scores = pyro.infer.Predictive(
    model=guide,
    num_samples=1,
    return_sites=["theta"]
)

model_scores.mc_samples = 100  # Monte Carlo integration for accurate theta estimates
```

**Rationale:**
- **Item parameters (a, b):** Point estimates sufficient, no uncertainty propagation needed → `mc_samples=1`
- **Theta scores (person abilities):** Monte Carlo integration for accurate posterior estimates → `mc_samples=100`
- **Runtime impact:** 100× speedup for model fitting phase (hours → minutes)

### Fix Applied

**File:** `results/ch5/5.5.1/code/step03_irt_calibration_pass2.py`

**Change:**
```python
# BEFORE (WRONG)
model_fit.mc_samples = 100  # ← 100× slower than necessary

# AFTER (CORRECT)
model_fit.mc_samples = 1    # ← Matches 5.1.1-5.4.1 pattern
```

**Verification:** Re-ran complete RQ 5.5.1 pipeline, runtime reduced from hours to ~161 seconds (consistent with other ROOT RQs).

### Lessons Learned

1. **Pattern consistency critical:** All ROOT RQs must follow same IRT configuration pattern
2. **Documentation gap:** MEDIUM settings template didn't explicitly distinguish model_fit vs model_scores `mc_samples`
3. **Early detection:** First production execution revealed issue before propagating to 5.5.2-5.5.7
4. **Validation importance:** Cross-RQ runtime comparison flags configuration errors

### Impact

- **Prevented:** 6 additional RQs (5.5.2-5.5.7) from inheriting wrong configuration
- **Time saved:** ~6 hours per RQ × 6 RQs = 36 hours saved
- **Documentation update needed:** Add to validated_irt_settings.md and MEDIUM settings template

---
