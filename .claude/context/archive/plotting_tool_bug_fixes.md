# Plotting Tool Bug Fixes

**Topic:** plotting_tool_bug_fixes
**Created:** 2025-12-05 (context-manager archival)
**Description:** Collection of bug fixes in tools/plotting.py discovered during RQ execution.

---

## pred_sorted UnboundLocalError + Data_Type Value Fix (2025-12-05 13:30)

**Archived from:** state.md Session (2025-12-05 13:30)
**Original Date:** 2025-12-05 13:30
**Reason:** Tool bugs fixed, production-validated

### Bug 1: pred_sorted UnboundLocalError

**Error:** UnboundLocalError: local variable 'pred_sorted' referenced before assignment

**Cause:** Variable pred_sorted was only created in certain conditional branches, but referenced outside those branches.

**Fix:** Ensured pred_sorted is always defined before use, likely through initialization or restructuring conditionals.

### Bug 2: Data_Type Value Mismatch

**Error:** Data_Type column expected 'predicted' but code generated 'prediction'

**Cause:** Inconsistent string literals used for Data_Type categorization.

**Fix:** Changed Data_Type value from 'prediction' to 'predicted' for consistency with downstream plotting code expectations.

### Context

These bugs were discovered during RQ 5.5.2 Step 7 (prepare plot data) execution. Both were in tools/plotting.py and affected piecewise trajectory plot generation.

### Files Modified

- tools/plotting.py

---

## vcov Matrix Extraction Fix (2025-12-05 13:30)

**Archived from:** state.md Session (2025-12-05 13:30)
**Original Date:** 2025-12-05 13:30
**Reason:** Correct matrix dimensions documented

### Bug: Wrong vcov Matrix Dimensions

**Error:** Extracted 11x11 matrix when only 8x8 (fixed effects only) was needed

**Cause:** model.cov_params() returns full covariance matrix including random effects, not just fixed effects.

**Fix:** Slice to fixed effects only using [:n_fixed, :n_fixed] where n_fixed = number of fixed effect terms.

**Context:** RQ 5.5.2 Step 4 (extract segment-location slopes with delta method SEs).

---
