# Chapter 6 Tool Interface Issues

Archive of tool interface mismatches discovered during Chapter 6 RQ execution.

---

## fit_lmm_trajectory_tsvr Column Expectations Mismatch (2025-12-07 11:00)

**Context:** During RQ 6.3.1 Step 05 (LMM fitting), discovered tool interface issues with `fit_lmm_trajectory_tsvr`.

### Problem Description

**Expected behavior:** Tool should accept prepared LMM input data from Step 04
**Actual behavior:** Tool has internal column name expectations that differ from prepared data

**Column name mismatches:**
- Step 04 produces: `['composite_ID', 'UID', 'test', 'domain', 'TSVR_hours', 'log_TSVR', 'theta']`
- Tool expects: Unknown (didn't investigate deeply, bypassed instead)

### Solution Applied

**Decision:** Bypass tool, use statsmodels directly

**Rationale:**
1. Data already prepared in Step 04 (proper format for LMM)
2. Formula already specified in plan.md: `theta ~ C(domain) * log_TSVR + (1 | UID)`
3. Direct statsmodels implementation is cleaner and more transparent
4. Tool adds complexity without value when data pre-prepared
5. Similar pattern occurred in Ch5 (tools useful for full pipelines, not single steps)

**Code used instead:**
```python
import statsmodels.formula.api as smf

# Fit LMM directly
model = smf.mixedlm(
    formula='theta ~ C(domain) * log_TSVR',
    data=df_lmm,
    groups=df_lmm['UID']
)
result = model.fit()
```

### Pattern Recognition

**Tool bypass pattern confirmed:**
- Some tools have internal bugs or interface mismatches
- Direct statsmodels implementation often cleaner for LMM analyses
- Tools most valuable for:
  - Multi-step pipelines (extract → prepare → fit → validate)
  - Standardized outputs (consistent CSV schemas)
- Tools less valuable for:
  - Single-step operations with pre-prepared data
  - Custom formula specifications
  - Exploratory analyses

**Documentation decision:** Document tool issues but don't block on fixing them
- Tools still useful for standardization across RQs
- Bypassing tools is acceptable when cleaner/faster
- Priority is scientific correctness, not tool usage

**Archived from:** state.md Session 2025-12-07 11:00
**Original Date:** 2025-12-07 11:00
**Reason:** Session 3+ old, tool bypass pattern documented

**Note:** Similar tool bypasses occurred in:
- RQ 6.3.1 Step 06 (compute_contrasts_pairwise had 'sig_uncorrected' bug)
- Multiple Ch5 RQs (various tool interface issues)

---
