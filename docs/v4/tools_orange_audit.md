# ORANGE Tools Comprehensive Audit

**Date:** 2025-11-22
**Auditor:** Claude Code
**Scope:** 21 ORANGE-status tools in tools_status.tsv

---

## Executive Summary

| Category | Count | Status |
|----------|-------|--------|
| **ORANGE Tools Audited** | 21 | Complete |
| **Passing (Ready for YELLOW)** | 21 | 100% |
| **Critical Bugs Found** | 2 | **FIXED** |
| **Minor Issues Found** | 3 | Non-blocking |

### Critical Blocking Issues - ALL FIXED

| Bug | File | Line | Severity | Status | Description |
|-----|------|------|----------|--------|-------------|
| **BUG-001** | tools/validation.py | 161 | CRITICAL | **FIXED** | `validate_lineage()` calls `load_lineage()` -> changed to `load_lineage_from_file()` |
| **BUG-002** | tools/plotting.py | 511-661 | CRITICAL | **FIXED** | `plot_trajectory_probability()` rewritten as standalone function (no longer calls `plot_trajectory()`) |

---

## Audit Results by Module

### tools/analysis_irt.py (8 ORANGE tools)

| Function | Exists | Signature | Internal Calls | Docstring | Type Hints | Decision | Bugs |
|----------|--------|-----------|----------------|-----------|------------|----------|------|
| calibrate_grm | YES | OK | OK | Good | Full | N/A | None |
| calibrate_irt | YES | OK | OK | Excellent | Full | N/A | None |
| configure_irt_model | YES | OK | OK | Good | Full | N/A | None |
| extract_parameters_from_irt | YES | OK | OK | Good | Full | N/A | None |
| extract_theta_from_irt | YES | OK | OK | Good | Full | N/A | None |
| filter_items_by_quality | YES | OK | OK | Excellent | Full | D039 COMPLIANT | None |
| fit_irt_grm | YES | OK | OK | Good | Full | N/A | None |
| prepare_irt_input_from_long | YES | OK | OK | Excellent | Full | N/A | None |

**Status:** All 8 IRT tools PASS - Ready for YELLOW status

**Key Findings:**
- All internal function calls use correct renamed names
- D039 compliance verified (filter_items_by_quality: a>=0.4, |b|<=3.0)
- Good input validation throughout
- Proper GPU memory management

---

### tools/analysis_lmm.py (8 ORANGE tools)

| Function | Exists | Signature | Internal Calls | Docstring | Type Hints | Decision | Bugs |
|----------|--------|-----------|----------------|-----------|------------|----------|------|
| compare_lmm_models_by_aic | YES | OK | OK | Complete | Full | N/A | None |
| compute_contrasts_pairwise | YES | OK | OK | Complete | Partial | D068 COMPLIANT | None |
| compute_effect_sizes_cohens | YES | OK | OK | Complete | Partial | N/A | Minor |
| configure_candidate_models | YES | OK | N/A | Complete | Full | N/A | None |
| extract_fixed_effects_from_lmm | YES | OK | OK | Complete | Full | N/A | None |
| extract_random_effects_from_lmm | YES | OK | OK | Complete | Full | N/A | None |
| fit_lmm_trajectory_tsvr | YES | OK | OK | Complete | Full | D070 COMPLIANT | Minor |
| prepare_lmm_input_from_theta | YES | OK | OK | Complete | Full | D070 (deprecated) | None |

**Status:** All 8 LMM tools PASS - Ready for YELLOW status

**Key Findings:**
- D068 compliance verified (compute_contrasts_pairwise: dual p-value reporting)
- D070 compliance verified (fit_lmm_trajectory_tsvr: uses TSVR hours)
- Factor/Domain column handling FIXED (7 coefficient name options checked)
- DeprecationWarning implemented for prepare_lmm_input_from_theta

**Minor Issues (Non-blocking):**
- compute_effect_sizes_cohens uses simplified f^2 approximation (documented)
- fit_lmm_trajectory_tsvr prints emoji on line 956 (should use ASCII)
- Missing type hints for lmm_result parameter in 2 functions

---

### tools/validation.py (4 ORANGE tools)

| Function | Exists | Signature | Internal Calls | Docstring | Type Hints | Bugs |
|----------|--------|-----------|----------------|-----------|------------|------|
| validate_irt_convergence | YES | OK | OK | Good | Full | None |
| validate_irt_parameters | YES | OK | OK | Good | Full | None |
| validate_lmm_convergence | YES | OK | OK | Good | Partial | None |
| validate_lmm_residuals | YES | OK | OK | Good | Full | None (FIXED) |

**Status:** All 4 validation tools PASS - Ready for YELLOW status

**Key Findings:**
- KS test standardization BUG WAS FIXED (lines 414-416 now standardize residuals)
- Default thresholds match D039 (a_min=0.4, b_max=3.0)

**Critical Bug Found (Not in ORANGE list but blocking):**
- **BUG-001:** Line 161 `validate_lineage()` calls `load_lineage()` but should call `load_lineage_from_file()`

---

### tools/plotting.py (1 ORANGE tool)

| Function | Exists | Signature | Internal Calls | Docstring | Type Hints | Bugs |
|----------|--------|-----------|----------------|-----------|------------|------|
| convert_theta_to_probability | YES | OK | OK | Excellent | Partial | None |

**Status:** convert_theta_to_probability PASSES - Ready for YELLOW status

**IRT Formula Verified:**
```python
prob = 1 / (1 + np.exp(-(discrimination * (theta - difficulty))))
```
This is the correct IRT 2PL formula.

**Critical Bug Found (Not in ORANGE list but blocking):**
- **BUG-002:** `plot_trajectory_probability()` (lines 610-617) passes incorrect arguments to `plot_trajectory()`:
  - Passes: `df_long=prob_data_renamed, time_var=time_var, factors=factors`
  - Expected: `time_pred: np.ndarray, fitted_curves: Dict, observed_data: pd.DataFrame`
  - This is a complete API mismatch - function will crash at runtime

---

## Critical Bugs Detail

### BUG-001: validate_lineage() NameError

**Location:** tools/validation.py:161
**Severity:** CRITICAL (NameError on execution)

**Current Code:**
```python
metadata = load_lineage(lineage_file)  # Line 161
```

**Expected Code:**
```python
metadata = load_lineage_from_file(lineage_file)
```

**Root Cause:** Function was renamed in the v2.0 naming convention overhaul but this internal call was missed.

**Impact:** `validate_lineage()` will crash with NameError if called.

---

### BUG-002: plot_trajectory_probability() API Mismatch

**Location:** tools/plotting.py:610-617
**Severity:** CRITICAL (TypeError on execution)

**Current Code:**
```python
fig, ax = plot_trajectory(
    df_long=prob_data_renamed,
    time_var=time_var,
    factors=factors,
    title=title,
    ylabel="Probability Correct (%)",
    ylim=(0, 100),
    **kwargs
)
```

**plot_trajectory() Actual Signature:**
```python
def plot_trajectory(
    time_pred: np.ndarray,           # Required: 1D array
    fitted_curves: Dict[str, np.ndarray],  # Required: dict
    observed_data: pd.DataFrame,     # Required: DataFrame
    time_col: str = 'Time',
    value_col: str = 'Value',
    ...
)
```

**Root Cause:** `plot_trajectory_probability()` was written assuming a different `plot_trajectory()` signature than what exists.

**Impact:** D069 dual-scale trajectory plotting will crash with TypeError.

---

## Recommendations

### Immediate Actions (Before RQ 5.1 Execution)

1. **Fix BUG-001:** Change line 161 in tools/validation.py
   ```python
   metadata = load_lineage_from_file(lineage_file)
   ```

2. **Fix BUG-002:** Rewrite `plot_trajectory_probability()` to either:
   - Option A: Match `plot_trajectory()` signature (generate time_pred, fitted_curves)
   - Option B: Create standalone plotting without calling plot_trajectory()
   - Option C: Add new `plot_trajectory_from_df()` wrapper function

### Status Promotion

After fixing critical bugs:
- **Move to YELLOW:** All 21 ORANGE tools
- **Keep in ORANGE:** None

### Testing Priority

1. IRT Pipeline: calibrate_irt() end-to-end (Steps 1-3)
2. LMM Pipeline: fit_lmm_trajectory_tsvr() end-to-end (Steps 5-6)
3. Plotting: plot_trajectory_probability() after fix (D069)
4. Validation: validate_lineage() after fix

---

## Appendix: Full TSV Export

```tsv
module	function	status	exists	signature_ok	internal_calls_ok	docstring	type_hints	decision_compliance	bugs_found
analysis_irt	calibrate_grm	PASS	YES	OK	OK	Good	Full	N/A	None
analysis_irt	calibrate_irt	PASS	YES	OK	OK	Excellent	Full	N/A	None
analysis_irt	configure_irt_model	PASS	YES	OK	OK	Good	Full	N/A	None
analysis_irt	extract_parameters_from_irt	PASS	YES	OK	OK	Good	Full	N/A	None
analysis_irt	extract_theta_from_irt	PASS	YES	OK	OK	Good	Full	N/A	None
analysis_irt	filter_items_by_quality	PASS	YES	OK	OK	Excellent	Full	D039	None
analysis_irt	fit_irt_grm	PASS	YES	OK	OK	Good	Full	N/A	None
analysis_irt	prepare_irt_input_from_long	PASS	YES	OK	OK	Excellent	Full	N/A	None
analysis_lmm	compare_lmm_models_by_aic	PASS	YES	OK	OK	Complete	Full	N/A	None
analysis_lmm	compute_contrasts_pairwise	PASS	YES	OK	OK	Complete	Partial	D068	None
analysis_lmm	compute_effect_sizes_cohens	PASS	YES	OK	OK	Complete	Partial	N/A	Minor
analysis_lmm	configure_candidate_models	PASS	YES	OK	N/A	Complete	Full	N/A	None
analysis_lmm	extract_fixed_effects_from_lmm	PASS	YES	OK	OK	Complete	Full	N/A	None
analysis_lmm	extract_random_effects_from_lmm	PASS	YES	OK	OK	Complete	Full	N/A	None
analysis_lmm	fit_lmm_trajectory_tsvr	PASS	YES	OK	OK	Complete	Full	D070	Minor
analysis_lmm	prepare_lmm_input_from_theta	PASS	YES	OK	OK	Complete	Full	D070-dep	None
validation	validate_irt_convergence	PASS	YES	OK	OK	Good	Full	N/A	None
validation	validate_irt_parameters	PASS	YES	OK	OK	Good	Full	N/A	None
validation	validate_lmm_convergence	PASS	YES	OK	OK	Good	Partial	N/A	None
validation	validate_lmm_residuals	PASS	YES	OK	OK	Good	Full	N/A	None
plotting	convert_theta_to_probability	PASS	YES	OK	OK	Excellent	Partial	N/A	None
```

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-11-22 | 1.0 | Initial comprehensive audit of 21 ORANGE tools |
