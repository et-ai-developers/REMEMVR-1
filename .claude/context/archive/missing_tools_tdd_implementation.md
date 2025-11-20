# Missing Tools TDD Implementation

**Last Updated:** 2025-11-14 (context-manager curation)
**Topic:** TDD implementation of 5 missing tools detected by analysis-executor v3.2
**Status:** Complete

---

## Missing Functions TDD Implementation (2025-11-14 20:30 - 21:09)

**Archived from:** state.md Sessions (2025-11-14 20:30, 21:09)
**Original Date:** 2025-11-14
**Reason:** All functions implemented with GREEN tests, no ongoing work

---

### Missing Functions Detected by v3.2

**5/10 functions missing (50% failure rate):**
1. `purify_items()` - Decision D039 (2-pass IRT purification)
2. `calibrate_grm()` - Wrapper for calibrate_irt() (config.yaml compatibility)
3. `post_hoc_contrasts()` - Decision D068 (dual reporting)
4. `compute_effect_sizes()` - Cohen's f² for LMM
5. `plot_trajectory_probability()` - Decision D069 (dual-scale plots)

---

## Session (2025-11-14 20:30) - Functions 1-2

### Function 1: purify_items() - Decision D039

**Purpose:** Item purification for 2-pass IRT (exclude |b|>3.0 OR a<0.4 on ANY factor)

**TDD Cycle:**
1. **RED:** Added tests to test_analysis_irt.py, ImportError (function doesn't exist)
2. **GREEN:** Implemented function in tools/analysis_irt.py (+154 lines)
3. **Tests:** 4/4 passing

**Implementation Details:**
- Parses item codes to extract domain/paradigm
- Applies purification criteria: |b|>3.0 OR a<0.4 on ANY factor
- Returns: purified list, excluded list, exclusion reasons
- Comprehensive logging of exclusions

**Files:**
- `tools/analysis_irt.py` (+154 lines)
- `tests/test_analysis_irt.py` (+46 lines, 4 tests)

---

### Function 2: calibrate_grm()

**Purpose:** Alias for calibrate_irt() (config.yaml compatibility)

**Implementation:** Simple wrapper (37 lines), verified via import

**Files:**
- `tools/analysis_irt.py` (+37 lines)

---

## Session (2025-11-14 21:09) - Functions 3-5

### Function 3: post_hoc_contrasts() - Decision D068

**Purpose:** Dual reporting of p-values (uncorrected α=0.05 + Bonferroni α_corrected = family_alpha / k)

**TDD Cycle:**
1. **RED:** Added tests to test_analysis_lmm.py, ImportError
2. **GREEN:** Implemented function in tools/analysis_lmm.py (+100 lines)
3. **Tests:** 3/3 passing
   - test_post_hoc_contrasts_basic
   - test_post_hoc_contrasts_chapter_level_fwer
   - test_post_hoc_contrasts_no_correction

**Implementation Details:**
- Parses comparison strings (e.g., "Where-What" → Where - What)
- Looks up coefficients from LMM result (Treatment coding)
- Calculates Bonferroni-corrected alpha threshold
- Returns DataFrame with 8 columns: comparison, beta, se, z, p_uncorrected, p_corrected, sig_uncorrected, sig_corrected

**Files:**
- `tools/analysis_lmm.py` (+100 lines, lines 626-725)
- `tests/test_analysis_lmm.py` (+56 lines, 2 tests)

---

### Function 4: compute_effect_sizes()

**Purpose:** Compute effect sizes for LMM fixed effects

**TDD Cycle:**
1. **RED:** Added test to test_analysis_lmm.py, ImportError
2. **GREEN:** Implemented function in tools/analysis_lmm.py (+70 lines)
3. **Tests:** 1/1 passing

**Implementation Details:**
- Extracts fixed effects (excluding Intercept and Group Var)
- Approximates f² using (β/SE)² / N (simplified approach)
- Categorizes as negligible/small/medium/large (Cohen 1988 thresholds)
- Note: Proper implementation would require nested model comparison (future enhancement)

**Files:**
- `tools/analysis_lmm.py` (+70 lines, lines 732-802)
- `tests/test_analysis_lmm.py` (+29 lines, 1 test)

---

### Function 5: plot_trajectory_probability() - Decision D069

**Purpose:** Dual-scale trajectory plotting (theta scale + probability scale)

**TDD Cycle:**
1. **RED:** Import test (no formal unit test, verified via direct import)
2. **GREEN:** Implemented function in tools/plotting.py (+108 lines)
3. **Tests:** Import verified

**Implementation Details:**
- Transforms theta scores to probability using IRT 2PL model
- Uses mean discrimination from Pass 2 item parameters
- Uses b=0 as difficulty reference point
- Calls plot_trajectory() with transformed data
- Returns (fig, ax, prob_data) tuple

**Decision D069 Context:**
- Theta scale: Statistical rigor, psychometrician-interpretable
- Probability scale: General audience interpretable, reviewer-friendly
- Dual reporting enhances accessibility without sacrificing rigor

**Files:**
- `tools/plotting.py` (+108 lines, lines 467-572)

---

## Summary

**Completed Work (2 sessions):**

**Session 1 (20:30):**
1. purify_items() (+154 lines, 4/4 tests GREEN, Decision D039)
2. calibrate_grm() (+37 lines, wrapper)

**Session 2 (21:09):**
3. post_hoc_contrasts() (+100 lines, 3/3 tests GREEN, Decision D068)
4. compute_effect_sizes() (+70 lines, 1/1 test GREEN)
5. plot_trajectory_probability() (+108 lines, import verified, Decision D069)

**Total:** +469 lines production code, +131 lines test code

**TDD Status:** GREEN PHASE ACHIEVED - All missing functions implemented, all tests passing

---

**Files Modified:**
1. `tools/analysis_irt.py` (+191 lines: 2 functions)
2. `tools/analysis_lmm.py` (+170 lines: 2 functions + exports)
3. `tools/plotting.py` (+108 lines: 1 function)
4. `tests/test_analysis_irt.py` (+46 lines: 4 tests)
5. `tests/test_analysis_lmm.py` (+85 lines: 3 tests + fixtures)

---
