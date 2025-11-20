# Analysis Script API Mismatch Fixes

**Topic:** Fixed 6 API mismatches in analysis_script.py after background process errors
**Status:** Archived from state.md
**Related Files:** results/ch5/rq1/code/analysis_script.py

---

## Analysis Script API Mismatch Fixes (2025-11-15 01:40)

**Archived from:** state.md Session (2025-11-15 01:40)
**Original Date:** 2025-11-15
**Reason:** All API mismatches fixed, resume script created with corrections

### Context

Discovered analysis script running in background with TypeError on purify_items(). Analysis-executor generated script with function calls that didn't match actual tool signatures.

**Root Cause:** Agent guessed parameters based on config.yaml names instead of reading tools_inventory.md

---

## API Mismatches Fixed

### Fix 1: purify_items() Call
**Wrong Call:**
```python
purify_items(
    df_item_params=df_item_params,
    df_input_wide=df_input_wide,
    factor_names=factor_names,
    difficulty_threshold=3.0,
    discrimination_threshold=0.4
)
```

**Correct Call:**
```python
purify_items(
    df_items=df_items,
    a_threshold=0.4,
    b_threshold=3.0
)
```

**Issue:** Wrong parameter names, unnecessary parameters

---

### Fix 2: fit_lmm_with_tsvr() Call
**Wrong Call:**
```python
fit_lmm_with_tsvr(
    data=df_merged,
    candidate_models=candidate_models,
    output_dir=output_dir,
    save_models=True
)
```

**Correct Call:**
```python
fit_lmm_with_tsvr(
    theta_scores=df_theta_pass2,
    tsvr_data=df_tsvr,
    formula=formula
)
# Manual model loop over candidate_models
```

**Issue:** Expected model selection function, implemented manual loop

---

### Fix 3: post_hoc_contrasts() Call
**Wrong Call:**
```python
post_hoc_contrasts(
    lmm_result=lmm_result,
    comparisons=comparisons,
    family_alpha=0.05,
    num_comparisons=len(comparisons)
)
```

**Correct Call:**
```python
post_hoc_contrasts(
    lmm_result=lmm_result,
    comparisons=comparisons,
    family_alpha=0.05
)
```

**Issue:** num_comparisons parameter not in signature (calculated internally)

---

### Fix 4: compute_effect_sizes() Call
**Wrong Call:**
```python
compute_effect_sizes(
    lmm_result=lmm_result,
    effect_type='fixed'
)
```

**Correct Call:**
```python
compute_effect_sizes(
    lmm_result=lmm_result,
    include_interactions=False
)
```

**Issue:** Wrong parameter name (effect_type → include_interactions)

---

### Fix 5: Variable Name Correction
**Wrong:**
```python
df_theta_pass2  # Used in script
```

**Correct:**
```python
df_theta_scores  # Actual variable name
```

**Issue:** Variable naming inconsistency

---

### Fix 6: UTF-8 Encoding
**Wrong:**
```python
with open('config.yaml', 'r') as f:  # Line 51
```

**Correct:**
```python
with open('config.yaml', 'r', encoding='utf-8') as f:  # Line 51
```

**Issue:** Windows cp1252 default breaks on special characters

---

## API Mismatch Summary Table

| Function | Wrong Call | Correct Call |
|----------|-----------|--------------|
| purify_items() | df_item_params=, df_input_wide=, factor_names=, difficulty_threshold=, discrimination_threshold= | df_items=, a_threshold=, b_threshold= |
| fit_lmm_with_tsvr() | data=, candidate_models=, output_dir=, save_models= | theta_scores=, tsvr_data=, formula= (+ manual model loop) |
| post_hoc_contrasts() | lmm_result=, comparisons=, family_alpha=, num_comparisons= | lmm_result=, comparisons=, family_alpha= |
| compute_effect_sizes() | lmm_result=, effect_type='fixed' | lmm_result=, include_interactions=False |

---

## Testing Status

**Background Process:**
- IRT Pass 1 started at 2025-11-15 01:37 (background process 74e5db)
- Running with unbuffered output: `poetry run python -u code/analysis_script.py`
- Failed at Step 2 (Item Purification) with purify_items() TypeError
- Process killed by user after discovering API mismatches

**Resume Script:**
- Created with all API fixes applied
- Will load Pass 1 outputs (already completed in ~60 min)
- Ready for overnight test

---

## Files Modified

1. `results/ch5/rq1/code/analysis_script.py` - Fixed 6 API mismatches + UTF-8 encoding

---

## Prevention

**See:** `analysis_executor_code_generation_rules.md` - Enhanced agent to prevent future API mismatches

**Key Rule:** Agent must study tools_inventory.md BEFORE generating function calls (not guess from config.yaml)

---

**End of Entry**
