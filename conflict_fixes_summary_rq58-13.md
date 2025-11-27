# Conflict Fixes Summary - RQ 5.8-5.13

**Date:** 2025-11-28
**Status:** Conflicts identified, fixes documented
**Total Conflicts:** 50 across 6 RQs

---

## Executive Summary

All conflicts have been systematically identified via g_conflict agent for RQs 5.8-5.13. **RQ 5.10 has been fully fixed (8/8 conflicts resolved)**. The remaining 42 conflicts across 5 RQs break down as follows:

- **CRITICAL:** 18 conflicts (require immediate fixes before g_code execution)
- **HIGH:** 16 conflicts (should fix to prevent validation failures)
- **MODERATE:** 8 conflicts (documentation/clarity improvements)

---

## RQ 5.10 - ✅ COMPLETE (8/8 Fixed)

All fixes applied to [3_tools.yaml](results/ch5/rq10/docs/3_tools.yaml):

1. Line 94: Changed `results/step04_age_effects_by_domain.csv` → `data/step04_age_effects_by_domain.csv`
2. Line 118: Changed `Age` → `age`, `domain_name` → `domain`
3. Lines 129-130: Fixed columns (added CI_lower/upper_predicted, data_type), changed row count `36` → `~600`
4. Line 218: Changed function `validate_model_convergence` → `validate_model_selection`
5. Line 330: Changed `domain_name` → `domain`
6. Line 336: Changed `domain_name` → `domain`
7. Line 342: Changed row count `~36` → `~600`
8. Line 343: Changed `domain_name` → `domain`

**Status:** Ready for g_code execution

---

## RQ 5.8 - 8 Conflicts Remaining

### CRITICAL (3 fixes)

**CRITICAL-1: early_cutoff_hours Parameter Default**
- **File:** 3_tools.yaml line 73, 4_analysis.yaml line 149
- **Issue:** Function signature default is 24.0, but RQ needs 48.0
- **Fix:** Verify g_code uses explicit parameter `early_cutoff_hours=48.0` in Step 1
- **Impact:** If default used, wrong piecewise boundary (24h instead of 48h consolidation window)

**CRITICAL-2: Column Name Case - test vs TEST**
- **Files:** 1_concept.md line 139, multiple locations in 2_plan.md/3_tools.yaml/4_analysis.yaml
- **Issue:** 1_concept.md shows `TEST` (uppercase), all other docs use `test` (lowercase)
- **Fix:** Update 1_concept.md line 139 to use lowercase `test`
- **Impact:** Merge operations will fail if case mismatch

**CRITICAL-3: Row Count Validation Tolerance**
- **Files:** 2_plan.md lines 788, 806; 4_analysis.yaml line 606
- **Issue:** Exact count should be 33 rows, but validation allows 30-35
- **Fix:** Change validation criterion to `exactly 33 rows` (4+11+18 is deterministic)
- **Impact:** Masks data loss if 30-32 rows generated

### HIGH (4 fixes)

**HIGH-1: TSVR vs TSVR_hours Column Naming**
- **Issue:** Source file might use `TSVR`, RQ expects `TSVR_hours`
- **Fix:** Check RQ 5.7 actual output, update references consistently

**HIGH-2: Prediction Grid Size Mismatch**
- **Issue:** Explicit lists show 9+9=18 points, parameters show 20+60=80 points
- **Fix:** Use explicit grid lists from 4_analysis.yaml lines 325-326, ignore grid point parameters

**HIGH-3: File Path - Best Continuous Model**
- **Status:** RESOLVED (correct workflow, no actual conflict)

**HIGH-4: Missing Convergence Strategy for Step 4**
- **Fix:** Add note in Step 4 that assumption validation adapts to model random structure
- **Impact:** If model uses fallback convergence, validation needs to skip random slopes checks

### MODERATE (1 fix)

**MODERATE-1: Segment Boundary Clarity**
- **Fix:** Clarify that 48h belongs to Early segment (0-48h inclusive, >48h is Late)

---

## RQ 5.9 - 8 Conflicts Remaining

### CRITICAL (3 fixes)

**CRITICAL-1: Bonferroni Alpha Discrepancy**
- **Files:** 1_concept.md line 64 says α=0.0033, all implementation uses α=0.0167
- **Fix:** Update 1_concept.md line 64 to `α = 0.0167` (matches 3 tests)
- **Impact:** Significance threshold confusion, affects interpretation

**CRITICAL-2: se_all vs se Naming**
- **Status:** RETRACTED - These are different variables, correctly used

**CRITICAL-3: File Path Inconsistency**
- **Files:** 2_plan.md says `data/step03_age_effects.csv`, 3_tools.yaml says `results/`
- **Fix:** Change 3_tools.yaml lines 170, 203 and 4_analysis.yaml lines 361, 378, 403 to `data/`
- **Impact:** File not found errors

### HIGH (3 fixes)

**HIGH-4: se_all Column Preservation**
- **Fix:** Add note that se_all intentionally dropped after Step 1 (not needed for LMM)
- **Impact:** Documentation clarity

**HIGH-5: Time Column Triple-Naming**
- **Issue:** TSVR → TSVR_hours → Time (redundant)
- **Fix:** Document that Time is alias for TSVR_hours (kept for model clarity)
- **Impact:** Memory redundancy, but functionally correct

**HIGH-6: Plot Column Name**
- **Fix:** Change 2_plan.md line 525 from `time_hours` to `TSVR_hours`
- **Impact:** Column name mismatch

### MODERATE (2 fixes)

**MODERATE-7: Bonferroni Test Count**
- **Related to CRITICAL-1** - α=0.0033 implies 15 tests, only 3 documented
- **Fix:** Same as CRITICAL-1

**MODERATE-8: Missing Effect Size Direction Validation**
- **Fix:** Add check that theta_older < theta_avg (negative decline expected)
- **Impact:** Won't catch unexpected positive decline

---

## RQ 5.11 - 5 Conflicts Remaining

### CRITICAL (2 fixes)

**CRITICAL-1: Missing purified_items.csv in concept.md**
- **File:** 1_concept.md line 96
- **Fix:** Add explicit mention of `results/ch5/rq1/data/step02_purified_items.csv` to Step 0
- **Impact:** Implementation might use all items instead of purified subset

**CRITICAL-2: IRT Dimension Mapping Uncertainty**
- **Issue:** 2_plan.md uses "likely" qualifiers for theta_common→What, etc.
- **Fix:** Verify mapping against RQ 5.1 documentation, remove "likely" qualifiers
- **Impact:** If mapping wrong, all correlations invalid

### HIGH (1 fix)

**HIGH-3: composite_ID Format Ambiguity**
- **Fix:** Clarify that result is "P001_T1" format regardless of source column case
- **Impact:** Merge failures if format wrong

### MODERATE (2 fixes)

**MODERATE-4: Where Domain Tag Parsing**
- **Fix:** Add regex pattern specification (exact substring match for `-L-`, `-U-`, `-D-`)
- **Impact:** False matches with loose regex

**MODERATE-5: Function Signature Parameter Defaults**
- **Status:** Current spec is safe (explicit parameters), no change needed

---

## RQ 5.12 - 16 Conflicts Remaining

### CRITICAL (7 fixes)

**CRITICAL-1: File Path Discrepancies (data/ vs results/)**
- **Files:** 3_tools.yaml uses `results/` for Steps 4-7, plan/analysis use `data/`
- **Fix:** Update 3_tools.yaml lines 26, 54, 92 to use `data/` prefix
- **Impact:** File not found when validation reads outputs

**CRITICAL-2: Missing "test" Column in Step 6 Input**
- **Fix:** Add "test" to 2_plan.md lines 608, 611 and 4_analysis.yaml lines 434-442
- **Impact:** Step 8 will fail (needs test column to map TSVR_hours)

**CRITICAL-3: fit_lmm_trajectory_tsvr Signature Default**
- **Issue:** Default `re_formula='~Days'` conflicts with usage `~TSVR_hours`
- **Fix:** Ensure parameter override used in generated code
- **Impact:** Wrong random effects if default used

**CRITICAL-4: Row Count Specification**
- **Issue:** Ambiguous "50 original items" statement
- **Fix:** Clarify: "Full CTT uses 50 TQ_ items; purified uses 38 (12 removed)"
- **Impact:** Conceptual confusion

**CRITICAL-5: Missing Domain Mapping in Step 6**
- **Fix:** Add domain mapping to 2_plan.md Step 6 (already in 4_analysis.yaml)
- **Impact:** Documentation inconsistency only

**CRITICAL-6: Missing validate_lmm_assumptions_comprehensive**
- **Fix:** Add to Step 7 validation OR remove from tools catalog
- **Impact:** Only convergence checked, 6 other diagnostics skipped

**CRITICAL-7: Purified Items Filename**
- **Issue:** concept.md says `purified_item_params.csv`, plan says `purified_items.csv`
- **Fix:** Verify RQ 5.1 actual output, update to match
- **Impact:** File not found if name wrong

### HIGH (6 fixes)

**HIGH-8 through HIGH-13:** Row counts, column specifications, validation architecture, formula naming, step numbering

---

## RQ 5.13 - 5 Conflicts Remaining

### CRITICAL (3 fixes)

**CRITICAL-1: ICC Column Name**
- **Files:** 2_plan.md says `estimate`, tools/analysis say `icc_value`
- **Fix:** Change 2_plan.md line 251 from `estimate` to `icc_value`
- **Impact:** validate_icc_bounds will fail looking for wrong column

**CRITICAL-2: Variance Column Name Default**
- **Fix:** Change 3_tools.yaml line 190 signature default from `value_col='variance'` to `value_col='estimate'`
- **Impact:** Misleading default parameter

**CRITICAL-3: Intercept/Slope Column Defaults**
- **Fix:** Change 3_tools.yaml line 38 defaults from `'Group Var'` to `'random_intercept'` and `'Group x TSVR_hours Var'` to `'random_slope'`
- **Impact:** Function signature doesn't match actual data structure

### HIGH (2 fixes)

**HIGH-4: Missing Row Count in Validation**
- **Fix:** Add `expected_rows: 5` to 3_tools.yaml line 194
- **Impact:** Documentation consistency

**HIGH-5: Missing Column Specification**
- **Fix:** Add comment that file has 5 columns total, function uses 3
- **Impact:** Documentation clarity

---

## Systematic Fix Strategy

### Phase 1: CRITICAL Fixes (18 total)

**Priority Order:**
1. RQ 5.13 (3 CRITICAL) - Simple column name changes
2. RQ 5.9 (2 CRITICAL after retraction) - Alpha value + file path
3. RQ 5.11 (2 CRITICAL) - Add missing specs + verify mapping
4. RQ 5.8 (3 CRITICAL) - Parameter defaults + column case
5. RQ 5.12 (7 CRITICAL) - Multiple file path + column issues

**Estimated Time:** 2-3 hours

### Phase 2: HIGH Fixes (16 total)

**Priority Order:**
1. Column naming consistency
2. Missing column specifications
3. Documentation clarifications

**Estimated Time:** 1-2 hours

### Phase 3: MODERATE Fixes (8 total)

**Priority Order:**
1. Documentation improvements
2. Validation enhancements
3. Clarity additions

**Estimated Time:** 30-60 minutes

---

## Ready for Execution After Fixes

Once all CRITICAL conflicts are resolved:

1. **Re-run g_conflict** on all 6 RQs to verify fixes
2. **Execute g_code** to generate analysis scripts
3. **Run analyses** for validation

**Current Status:**
- ✅ RQ 5.10: Ready for g_code
- ⚠️ RQ 5.8-5.9, 5.11-5.13: Awaiting conflict fixes

---

## Notes

- All conflict reports saved in workflow_execution_report_rq58-13.md
- Individual g_conflict reports generated for each RQ
- Fix priority based on impact (CRITICAL = runtime failures, HIGH = validation issues, MODERATE = clarity)
- Some conflicts auto-fixed by g_code reading 4_analysis.yaml as authoritative source

**END OF SUMMARY**
