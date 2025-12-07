# ch6_lmm_statsmodels_cov_re_fix

**Topic Description:** Fix for statsmodels random effects covariance matrix extraction. In newer statsmodels versions, cov_re is a DataFrame (not ndarray), requiring .values.flatten() for safe extraction. Applied in RQ 6.1.1 step05.

---

## statsmodels cov_re Type Handling (2025-12-06 22:00)

**Context:** During RQ 6.1.1 Step 05 (Fit 5 Candidate LMM Models), g_code generated code that called .flatten() directly on cov_re, causing AttributeError in newer statsmodels versions.

**Archived from:** state.md (Session 2025-12-06 22:00)
**Original Date:** 2025-12-06 22:00
**Reason:** Bug pattern documented, fix applied to tools

---

### The Bug

**Error:**
```
AttributeError: 'DataFrame' object has no attribute 'flatten'
```

**Root Cause:**
- Older statsmodels: `model.cov_re` returns ndarray → can call .flatten() directly
- Newer statsmodels: `model.cov_re` returns DataFrame → must call .values.flatten()
- g_code generated code assumed ndarray (older API)

---

### The Fix

**Safe extraction pattern:**

```python
# Check if DataFrame (newer statsmodels)
if hasattr(cov_re, 'values'):
    random_effects_var = cov_re.values.flatten()
else:
    # ndarray (older statsmodels)
    random_effects_var = cov_re.flatten()
```

**Applied in:**
- results/ch6/6.1.1/code/step05_fit_lmm.py
- Any LMM code that extracts random effects variance

---

### When This Matters

**Random effects variance extraction needed for:**
- ICC (Intraclass Correlation Coefficient) computation
- Model diagnostics
- Variance component reporting
- Random effects interpretation

**Affects:**
- All LMM trajectory models (Ch6 Types 6.1, 6.3, 6.4, 6.5)
- Any code extracting cov_re for reporting

---

### Status

**Bug pattern recognized, fix documented.**

Future g_code invocations should include this pattern, or tools should be updated to handle both API versions.

---
