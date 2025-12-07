# rq_6.4.1_step01_five_systematic_bug_fixes

**Topic Description:** RQ 6.4.1 Step 01 IRT calibration - 5 systematic bug fixes applied iteratively (UID/test parsing, return unpacking, n_cats list format, MIRT columns), all bugs repeatable across GRM RQs

**Related Topics:**
- `rq_6.4.1_step00_complete_paradigm_extraction` (Session 2025-12-07 19:45)
- `g_code_multidimensional_irt_bug_pattern` (Session 2025-12-07 19:45)
- `rq_6.1.1_complete_execution_logarithmic_best` (archived earlier - first occurrence of bugs)
- `rq_6.3.1_complete_execution_when_domain_steeper_decline` (archived earlier - second occurrence)

---

## RQ 6.4.1 Step 01 - IRT Calibration Pass 1 Debugging (2025-12-07 19:45)

**Archived from:** state.md Session (2025-12-07 19:45)
**Original Date:** 2025-12-07 19:45
**Reason:** Step 01 debugging complete, IRT running successfully, subsequent steps moved forward

### Generated Code

**File:** step01_irt_calibration_pass1.py (546 lines)
**Status:** Running with 5 systematic bug fixes applied
**Expected completion:** ~7 minutes (2 min fitting + 5 min scoring)

### Bug Fix #1: Missing UID/test Columns in Long Format

**Error:** `ValueError: Missing required columns: ['UID', 'test']`

**Root cause:** `prepare_irt_input_from_long` expects UID/test/item_name/score columns, but wide format only has composite_ID

**Fix:** Parse composite_ID to extract UID and test before melt():
```python
df_wide['UID'] = df_wide['composite_ID'].str.rsplit('_', n=1).str[0]
df_wide['test'] = df_wide['composite_ID'].str.rsplit('_', n=1).str[1].str.replace('T', '')
df_long = df_wide.melt(id_vars=['composite_ID', 'UID', 'test'], ...)
```

**Pattern source:** RQ 6.3.1 Step 01 lines 227-243 (same fix)

---

### Bug Fix #2: Wrong Return Value Unpacking Order

**Error:** `ValueError: Q_matrix shape torch.Size([400, 72]) doesn't match expected (400, 3)`

**Root cause:** `prepare_irt_input_from_long` returns `(response_matrix, Q_matrix, missing_mask, item_list, composite_ids)` but code unpacked in wrong order

**Fix:** Correct unpacking order:
```python
response_matrix, Q_matrix, missing_mask, item_list, composite_ids = \
    prepare_irt_input_from_long(df_long, groups)
```

**Pattern source:** tools/analysis_irt.py docstring (canonical signature)

---

### Bug Fix #3: n_cats Must Be List (configure_irt_model)

**Error:** `TypeError: object of type 'int' has no len()`

**Root cause:** `configure_irt_model` expects n_cats as list (one value per item), not scalar int

**Fix:** Convert to list before passing:
```python
n_cats_list = [IRT_CONFIG['n_cats']] * n_items  # [5, 5, 5, ..., 5] (72 times)
model = configure_irt_model(..., n_cats=n_cats_list, ...)
```

**Pattern source:** RQ 6.3.1 Step 01 lines 285-292

---

### Bug Fix #4: n_cats Must Be List (extract_parameters_from_irt)

**Error:** `TypeError: 'int' object is not iterable` (in extract_parameters loop)

**Root cause:** `extract_parameters_from_irt` also expects n_cats as list (consistent with configure)

**Fix:** Pass same n_cats_list to extraction:
```python
df_item_params = extract_parameters_from_irt(..., n_cats=n_cats_list)
```

**Pattern source:** RQ 6.3.1 Step 01 (consistent with configure_irt_model)

---

### Bug Fix #5: MIRT Column Format Mismatch

**Error:** `KeyError: "['factor', 'a', 'b1', 'b2', 'b3', 'b4'] not in index"`

**Root cause:** `extract_parameters_from_irt` returns MIRT format for multidimensional models: `(item_name, Difficulty, Overall_Discrimination, Discrim_IFR, Discrim_ICR, Discrim_IRE)`, NOT `(item_name, factor, a, b1-b4)`

**Fix:** Keep MIRT format as-is (don't rename columns):
```python
# Note: extract_parameters_from_irt returns MIRT format for multidimensional models
# Keep as-is since this is the tool's native output format (same as RQ 6.3.1)
log(f"[INFO] Parameter columns: {list(df_item_params.columns)}")
```

**Pattern source:** RQ 6.3.1 Step 01 lines 326-332, verified against actual output file

**Validation updated:** Changed validation to use 'Overall_Discrimination' and 'Difficulty' columns

---

### Bug Pattern Analysis

**Critical Finding:** ALL 5 bugs are systematic issues with g_code's handling of multidimensional IRT models

**Pattern Repeatability:**
- Same bugs occurred in RQ 6.1.1 (single-factor GRM, subset of issues)
- Same bugs occurred in RQ 6.3.1 (domain-based 3-factor GRM)
- Same bugs occurred in RQ 6.4.1 (paradigm-based 3-factor GRM)

**Root Cause:** g_code doesn't have examples of multidimensional IRT in training data

**Solution:** Document pattern fixes for future RQs (already in archived topics)

**Implication:** Pattern will recur in ALL future GRM-based RQs (6.5.1, 6.6.1, etc.)

---

### Current IRT Status (at time of archiving)

**Model fitting:** COMPLETE (~34k epochs, converged at loss ~27.54)
**Theta scoring:** IN PROGRESS (mc_samples=100, expected ~5 min)
**Settings:** MINIMUM (mc_samples=1/iw_samples=1 for fitting per mc_samples pattern from archived topics)

**All 5 bugs fixed, code running successfully**

---

### Execution Metrics

**Execution time:** ~4 hours (mostly iterative debugging)
**g_code invocations:** 2 (Step 00, Step 01)
**Code fixes applied:** 5 systematic bug fixes (all documented with pattern sources)
**Context-finder searches:** 1 (found 8 relevant archived topics, 98-70% relevance scores)

---
