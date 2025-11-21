# RQ 5.1 Tools Reality Check - Summary Report

**Date:** 2025-11-22
**Auditor:** Claude Code (context-finder agents x3)
**Scope:** 21 ORANGE-flagged tools required for RQ 5.1 execution
**Source:** Comparison of [2_plan.md](../../results/ch5/rq1/docs/2_plan.md) expectations vs actual code implementations

---

## Executive Summary

**Tools Audited:** 21 ORANGE tools
**Working as Expected:** 12 tools (57%)
**Minor Issues:** 5 tools (24%)
**Major Issues:** 4 tools (19%)

**BLOCKER ALERT:** `calibrate_irt` will fail on first execution (4 function name mismatches)

---

## Critical Issues (Must Fix Before Execution)

### 1. **`calibrate_irt` - WILL FAIL** ⛔
**Severity:** CRITICAL
**Issue:** Main IRT pipeline calls 4 non-existent functions:
- Line 457: `prepare_irt_data()` → Should be `prepare_irt_input_from_wide()`
- Line 510: `fit_irt_model()` → Should be `fit_irt_grm()`
- Line 520: `extract_theta_scores()` → Should be `extract_theta_from_irt()`
- Line 535: `extract_item_parameters()` → Should be `extract_parameters_from_irt()`

**Impact:** Step 1 & Step 3 will crash with `NameError` on first function call
**Fix:** Search-replace 4 function names in `calibrate_irt()` body

---

### 2. **`compute_contrasts_pairwise` - SILENT FAILURE** ⚠️
**Severity:** HIGH
**Issue:** Searches for `C(Domain, Treatment)` coefficient but `prepare_lmm_input_from_theta()` creates `Factor` column
**Impact:** Step 6 contrasts will skip silently (no results, no error)
**Fix:** Either:
- **Option A:** Update `prepare_lmm_input_from_theta()` line 78: `Factor` → `Domain`
- **Option B:** Update `compute_contrasts_pairwise()` line 689: search for `Factor` instead of `Domain`

---

### 3. **`prepare_lmm_input_from_theta` - WRONG WORKFLOW** 🚫
**Severity:** HIGH
**Issue:** Uses nominal days `{1:0, 2:1, 3:3, 4:6}` instead of TSVR (violates Decision D070)
**Impact:** Would produce systematically wrong temporal estimates if used
**Fix:** **DO NOT USE** this function for RQ 5.1. Use `fit_lmm_trajectory_tsvr()` instead (which correctly uses TSVR)

---

## Moderate Issues (Non-Blocking, Should Fix)

### 4. **`compute_effect_sizes_cohens` - MISNAMED** ⚠️
**Severity:** MODERATE
**Issue:** Uses `(β/SE)²/n` approximation, NOT true Cohen's f² (requires nested model R² comparison)
**Impact:** Effect sizes are approximations, may mislead interpretation
**Fix:** Either:
- Rename to `approximate_effect_size()` (honest naming)
- OR: Reimplement proper Cohen's f² via nested model comparison

---

### 5. **`fit_lmm_trajectory_tsvr` - FRAGILE** ⚠️
**Severity:** MODERATE
**Issue:** Multiple column name fallbacks (tsvr vs TSVR_hours, domain_name vs factor), silent warnings on missing data
**Impact:** Works but may mask data issues
**Fix:** Add input validation, standardize column names, fail loudly on missing TSVR

---

### 6. **`compare_lmm_models_by_aic` - SILENT FAILURES** ⚠️
**Severity:** MODERATE
**Issue:** Sets AIC=inf if model fails but continues (no error raised)
**Impact:** May select suboptimal model if best candidate failed to converge
**Fix:** Add convergence validation, optionally fail on any model convergence failure

---

## Minor Issues (Low Priority)

### 7. **`prepare_irt_input_from_wide` - NAMING CONFUSION** 📝
**Severity:** LOW
**Issue:** Function name says "from_wide" but actually converts long→wide
**Impact:** Confusing but works correctly
**Fix:** Rename to `prepare_irt_input_from_long()`

---

### 8. **`configure_candidate_models` - HARDCODED** 📝
**Severity:** LOW
**Issue:** Random effects structure hardcoded to `~Days` (cannot test alternatives)
**Impact:** Cannot compare random effects structures (only fixed effects trajectories)
**Fix:** Add `re_formula` parameter (low priority - current structure is sensible)

---

### 9. **`extract_random_effects_from_lmm` - ASSUMPTION** 📝
**Severity:** LOW
**Issue:** Assumes `cov_re[0,0]` is intercept variance (not validated)
**Impact:** Works for standard models but could break with exotic random effects
**Fix:** Add validation or documentation of assumption

---

### 10. **`validate_lmm_convergence` - OPTIMISTIC DEFAULT** 📝
**Severity:** LOW
**Issue:** Defaults to `converged=True` if attribute missing
**Impact:** Could mask convergence failures in non-statsmodels LMM implementations
**Fix:** Default to `converged=False` OR document assumption (statsmodels only)

---

### 11. **`validate_lmm_residuals` - KS TEST BUG** 📝
**Severity:** LOW
**Issue:** KS test doesn't standardize residuals before testing vs standard normal
**Impact:** Test will be overly conservative for n≥5000
**Fix:** Standardize residuals: `(resid - mean) / std` before KS test

---

## Tools Working Correctly (12/21)

✅ **IRT Tools (5):**
1. `calibrate_grm` - Clean wrapper
2. `configure_irt_model` - Correct IWAVE setup
3. `extract_parameters_from_irt` - Correct a/b extraction
4. `extract_theta_from_irt` - Correct batched scoring
5. `filter_items_by_quality` - Correct D039 purification

✅ **LMM Tools (3):**
6. `configure_candidate_models` - Generates 5 formulas correctly (hardcoded RE is minor)
7. `extract_fixed_effects_from_lmm` - Correct table extraction
8. `extract_random_effects_from_lmm` - Correct ICC calculation (assumption is minor)

✅ **Plotting Tools (1):**
9. `convert_theta_to_probability` - Perfect D069 implementation

✅ **Validation Tools (3):**
10. `validate_irt_convergence` - Correct convergence check
11. `validate_irt_parameters` - Correct quality flagging
12. `validate_lmm_convergence` - Works (optimistic default is minor)

---

## Recommended Fix Priority

### **MUST FIX (Before Any Execution):**
1. ⛔ **`calibrate_irt`** - Fix 4 function name mismatches (5 minutes)
2. ⚠️ **`compute_contrasts_pairwise`** - Fix Domain vs Factor mismatch (2 minutes)

### **SHOULD FIX (Before RQ 5.1):**
3. 🚫 **Document `prepare_lmm_input_from_theta` as DEPRECATED** - Add warning to not use with TSVR (1 minute)
4. ⚠️ **`compute_effect_sizes_cohens`** - Rename to `approximate_effect_size()` (honest naming) (2 minutes)
5. ⚠️ **`fit_lmm_trajectory_tsvr`** - Add input validation (10 minutes)

### **NICE TO HAVE (Low Priority):**
6. 📝 **Rename `prepare_irt_input_from_wide`** → `prepare_irt_input_from_long` (2 minutes)
7. 📝 **Fix `validate_lmm_residuals` KS test** - Standardize residuals (3 minutes)
8. 📝 **`compare_lmm_models_by_aic`** - Add convergence validation (5 minutes)

**Total Critical Fix Time:** ~7 minutes
**Total Should Fix Time:** ~13 minutes
**Total Nice to Have Time:** ~10 minutes

**GRAND TOTAL:** ~30 minutes to production-ready state

---

## Refactor Severity Summary

| Severity | Count | Tools |
|----------|-------|-------|
| **NONE** | 12 | All working correctly |
| **LOW** | 5 | Naming confusion, minor assumptions |
| **MODERATE** | 3 | Silent failures, fragile code, wrong formulas |
| **HIGH** | 2 | API mismatches, wrong workflow |
| **CRITICAL** | 1 | Will crash on execution |

---

## Next Steps

1. **Fix CRITICAL blocker:** Update `calibrate_irt()` function names (tools/analysis_irt.py)
2. **Fix HIGH priority:** Resolve Domain/Factor naming inconsistency
3. **Test critical path:** Run Steps 1-3 (IRT pipeline) with fixed code
4. **Fix remaining issues:** Address MODERATE and LOW severity issues
5. **Update tools_status.tsv:** Move fixed tools from ORANGE→YELLOW

---

## Files Generated

1. **Reality Check TSV:** `docs/v4/ch5rq1-tools-reality.tsv` (machine-readable audit)
2. **Summary Report:** `docs/v4/ch5rq1-tools-reality-summary.md` (this file)

---

**Audit Complete:** 2025-11-22
**Auditor Confidence:** High (all 21 tools inspected via context-finder agents)
