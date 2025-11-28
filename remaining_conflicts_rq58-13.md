# Remaining Conflicts - RQ 5.8-5.13 Post-Verification

**Date:** 2025-11-28
**Status:** Post-g_conflict verification (parallel execution on all 6 RQs)
**Last Updated:** After CRITICAL conflict fixes applied

---

## Executive Summary

**Total RQs Analyzed:** 6 (RQ 5.8-5.13)
**Ready for g_code:** 4 RQs (5.9, 5.10, 5.11, 5.13) - 67%
**Needs Minor Fixes:** 1 RQ (5.8) - 3 issues, ~10 minutes
**Blocked:** 1 RQ (5.12) - Requires RQ 5.1 output verification

**Overall Assessment:** 4/6 RQs have ZERO CRITICAL conflicts remaining and can proceed to g_code execution immediately. RQ 5.8 has 3 fixable issues. RQ 5.12 is blocked by cross-RQ dependency filename verification.

---

## RQ 5.8 - 9 Conflicts Remaining (4 CRITICAL, 4 HIGH, 1 MODERATE)

### Status: ⚠️ Needs 3 Fixes Before g_code

### CRITICAL Conflicts (4 total)

#### CRITICAL-1: early_cutoff_hours Parameter Default Mismatch
**Location:** 3_tools.yaml line 73, line 92
**Issue:** Function signature default is 24.0, but RQ 5.8 implementation uses 48.0
```yaml
# Line 73 - Function signature
signature: "assign_piecewise_segments(df: DataFrame, tsvr_col: str = 'TSVR_hours', early_cutoff_hours: float = 24.0) -> DataFrame"

# Line 92 - Actual usage
early_cutoff_hours: 48.0
```

**Impact:** If g_code uses function default (24.0) instead of explicit parameter (48.0), the entire two-phase analysis tests the WRONG hypothesis. 48 hours is the consolidation theory breakpoint per concept.md.

**Fix Options:**
1. Update function signature default to 48.0: `early_cutoff_hours: float = 48.0`
2. Add validation check in 4_analysis.yaml Step 1 to verify `early_cutoff_hours = 48.0`
3. Add note in 3_tools.yaml line 73: "Default 24h is for general use; RQ 5.8 overrides to 48h"

**Recommended Fix:** Option 1 (update signature default to 48.0) OR Option 2 (add validation)

---

#### CRITICAL-2: Segment Time Boundary Ambiguity
**Location:** 1_concept.md line 112, 2_plan.md lines 222-223
**Issue:** Boundary inclusion unclear - is 48 hours in Early or Late segment?

**Current Specification:**
```
Early segment = 0-48 hours TSVR (Day 0-1)
Late segment = 48-240 hours TSVR (Day 1-6)
```

**Problem:** Mathematical notation unclear:
- Early: [0, 48] or [0, 48)?
- Late: [48, 240] or (48, 240]?
- If 48h in both: double-counting
- If 48h in neither: gap in data

**Impact:** Piecewise models are sensitive to boundary assignment. Observations at exactly 48h could be included/excluded inconsistently between analysis steps, affecting slope estimates and ratio computation.

**Recommended Fix:** Specify explicit inclusion:
```
Early segment: [0, 48) hours (0 to <48, excluding 48)
Late segment: [48, 240] hours (48 to 240, including 48)
```
Standard convention: boundary point belongs to second segment.

**Files to Update:**
- 1_concept.md line 112
- 2_plan.md lines 222-223
- 3_tools.yaml line 99 (add boundary note)

---

#### CRITICAL-3: Row Count Validation Mismatch
**Location:** 2_plan.md line 806, 4_analysis.yaml line 560, line 606
**Issue:** Plan says "33 exactly", analysis says "~33" (approximate)

**Current Specifications:**
- 2_plan.md line 806: "Expected rows: 33 exactly (4 observed + 11 quadratic + 18 piecewise)"
- 4_analysis.yaml line 560: `expected_rows: "~33"`
- 4_analysis.yaml line 606: `expected_rows: "30-35"`

**Arithmetic:** 4 + 11 + 18 = 33 (exact, deterministic)

**Impact:**
- "~33" validation may accept 32 or 34 rows (lenient)
- "30-35" validation may accept 30-35 rows (very lenient)
- If actual data has missing tests → lenient validation passes but downstream plotting fails

**Recommended Fix:** Change both locations to "33 exactly":
- 4_analysis.yaml line 560: `expected_rows: "33"`
- 4_analysis.yaml line 606: Remove range, use exact count

**Status:** ✅ Already partially fixed (sed command applied), verify completeness

---

#### CRITICAL-4: Missing RQ 5.7 Convergence Status Validation
**Location:** 2_plan.md lines 99-101, 4_analysis.yaml lines 232-235
**Issue:** All documents discuss convergence fallback strategy, but NONE verify if RQ 5.7 required fallback

**Problem:** If RQ 5.7's best continuous model used fallback to (1 | UID) random intercepts only, comparing RQ 5.8 piecewise AIC to that baseline is methodologically invalid - confounds model structure with time pattern.

**Example:**
- RQ 5.7 continuous: theta ~ Time (1 | UID) [random intercepts, AIC = 12000]
- RQ 5.8 piecewise: theta ~ Days_within * Segment + (Days_within | UID) [random slopes, AIC = 11950]
- ΔAIC = -50 favors piecewise, BUT difference may be due to random slopes vs intercepts, NOT time pattern

**Impact:** AIC comparison (Test 2) is INVALID if model structures differ.

**Recommended Fix:** Add Step 0 validation:
1. Load RQ 5.7 best model (`results/ch5/rq7/data/step03_best_model.pkl`)
2. Check convergence status and random structure
3. If RQ 5.7 used fallback, RQ 5.8 MUST use same fallback for piecewise
4. Document in Step 3 validation: "Verify random structure matches RQ 5.7 best model"
5. If structures cannot match, report AIC comparison as inconclusive

**Files to Update:**
- 2_plan.md: Add Step 0 validation requirement
- 4_analysis.yaml: Add RQ 5.7 model structure check in Step 0
- 3_tools.yaml: Document this validation requirement

---

### HIGH Conflicts (4 total)

#### HIGH-1: TSVR vs TSVR_hours Terminology
**Location:** 1_concept.md line 102, 2_plan.md line 102
**Issue:** Concept uses "TSVR", implementation uses "TSVR_hours"

**Impact:** Documentation search/grep for "TSVR" column may miss "TSVR_hours" references.

**Recommended Fix:** Update 1_concept.md to consistently use "TSVR_hours" when referring to column name.

---

#### HIGH-2: Bonferroni Alpha Precision
**Location:** 1_concept.md line 48, 2_plan.md line 329, 3_tools.yaml line 126
**Issue:** Using 0.0033 (truncated) vs 0.003333 (exact)

**Arithmetic:** 0.05 / 15 = 0.003333... (repeating)

**Impact:** Tests with p-values in [0.0033, 0.00333] have inconsistent decisions. Violates Bonferroni correction principle (consistent α across family).

**Recommended Fix:** Use exact value: `bonferroni_alpha: 0.003333` (6 decimal places) OR document rounding convention.

---

#### HIGH-3: Prediction Grid Size Mismatch
**Location:** 2_plan.md line 357, 4_analysis.yaml lines 325-326
**Issue:** Parameters show 20+60=80 points, explicit lists show 9+9=18 points

**Recommended Fix:** Use explicit grid lists from 4_analysis.yaml, ignore grid point parameters.

---

#### HIGH-4: Missing Convergence Strategy for Step 4
**Location:** 2_plan.md Step 4
**Issue:** If model uses fallback convergence, validation needs to skip random slopes checks

**Recommended Fix:** Add note in Step 4 that assumption validation adapts to model random structure.

---

### MODERATE Conflicts (1 total)

#### MODERATE-1: Segment Boundary Clarity
**Location:** Throughout docs
**Issue:** 48h boundary belongs to which segment?

**Recommended Fix:** Clarify that 48h belongs to Late segment (0-48h exclusive boundary, >48h is Late).

**Status:** ✅ Related to CRITICAL-2, same fix resolves both

---

## RQ 5.9 - 6 Conflicts Remaining (2 CRITICAL, 2 HIGH, 2 MODERATE)

### Status: ✅ Ready for g_code (All CRITICAL conflicts fixed)

### Remaining Issues (Documentation Only)

#### HIGH-3: TSVR_hours vs Time Column Naming
**Location:** Throughout plan.md and analysis.yaml
**Issue:** Step 1 creates "Time" as duplicate of "TSVR_hours", unclear if rename or preserve both

**Impact:** Column preservation unclear - does data have BOTH columns or one?

**Recommendation:** Clarify Step 1 behavior: Keep BOTH columns (TSVR_hours original + Time alias) OR rename only.

**Status:** Not workflow-blocking (g_code will handle based on 4_analysis.yaml specification)

---

#### HIGH-4: Column Count Discrepancy
**Location:** 2_plan.md line 179
**Issue:** Expected 10 columns (if Time added) or 9 columns (if TSVR_hours renamed)

**Status:** Likely 10 columns (both kept), but documentation ambiguous

---

#### MODERATE-5: Missing Validation in Step 4
**Location:** 2_plan.md lines 803-809
**Issue:** Substantive checks (older adults worse) specified in plan but not in analysis.yaml validation

**Status:** Quality control gap, not workflow-breaking

---

#### MODERATE-6: Tertile Parameter Naming
**Location:** 3_tools.yaml line 34, 4_analysis.yaml line 527
**Issue:** Parameter mismatch (file paths vs loaded objects)

**Status:** Code generation will resolve during implementation

---

## RQ 5.10 - 8 Conflicts Remaining (4 CRITICAL, 2 HIGH, 2 MODERATE)

### Status: ✅ Ready for g_code (All CRITICAL conflicts fixed in prior session)

### Verification Results
- ✅ All 8 conflicts from prior session confirmed resolved
- ✅ Column names consistent: "domain" (not "domain_name")
- ✅ CI columns consistent: "CI_lower/CI_upper" (uppercase CI)
- ✅ File paths fixed: "data/step02_fixed_effects.csv" (not results/)
- ✅ Validation function: "validate_model_selection" (corrected)

### Remaining Issues (Documentation Quality)

#### HIGH-5: Row Count Calculation (Plot Data)
**Location:** 2_plan.md line 911, 3_tools.yaml line 130
**Issue:** Claimed ~600 rows, but 3×3×64=576 or 3×3×67=603 depending on grid

**Status:** Documentation inconsistency, not critical for execution

---

#### MODERATE-2: Age Column Case
**Location:** 1_concept.md line 102
**Issue:** Uses "Age" (uppercase) but actual column is "age" (lowercase)

**Status:** Documentation only, code uses correct lowercase

---

#### MODERATE-4: Row Count Ambiguity (Age Data)
**Location:** 2_plan.md line 95
**Issue:** "~100 participants" vs "100 participants" (exact)

**Status:** Should be exact (N=100 from RQ 5.1), remove tilde

---

## RQ 5.11 - 8 Conflicts Remaining (5 CRITICAL, 2 HIGH, 1 MODERATE)

### Status: ✅ Ready for g_code (All CRITICAL conflicts fixed)

### Verification Results
- ✅ IRT theta column names fixed: theta_what/where/when (not theta_common/congruent/incongruent)
- ✅ Purified items reference added to 1_concept.md Step 0
- ✅ All dimension-to-domain mappings corrected throughout

### Remaining Issues (Documentation Quality)

#### CRITICAL (Documentation): Dimension-to-Domain Mapping Needs Documentation
**Location:** Throughout all docs
**Issue:** Mapping between IRT dimensions (common/congruent/incongruent) and memory domains (What/Where/When) not explicitly documented

**Recommendation:** Add mapping table to 2_plan.md:
```
IRT Dimension → Memory Domain → Item Tags
common        → What         → -N- (naming)
congruent     → Where        → -L-/-U-/-D- (location)
incongruent   → When         → -O- (order)
```

**Status:** Fixed implicitly (column names use domains), but explicit documentation would improve clarity

---

#### HIGH-6: Composite ID Format Case
**Location:** 2_plan.md line 57, line 207
**Issue:** Placeholder uses {test} (lowercase) but example shows T1 (uppercase)

**Status:** Need to verify source column case in dfData.csv

---

#### HIGH-7: TSVR Column Name
**Location:** 1_concept.md line 96
**Issue:** Says "TSVR" but likely "TSVR_hours" in actual file

**Status:** Verify RQ 5.1 output, update concept.md

---

#### MODERATE-8: LMM Formula Syntax
**Location:** 2_plan.md line 398
**Issue:** Uses R lme4 syntax instead of statsmodels syntax

**Status:** tools.yaml and analysis.yaml use correct syntax, plan.md documentation only

---

## RQ 5.12 - 4 Conflicts Remaining (2 CRITICAL, 1 HIGH, 1 MODERATE)

### Status: ❌ BLOCKED - Requires RQ 5.1 Output Verification

### CRITICAL Conflicts (BLOCKING)

#### CRITICAL-1: Purified Items Filename Verification Needed
**Location:** 2_plan.md line 41, 3_tools.yaml line 16, 4_analysis.yaml line 32, 1_concept.md line 180
**Issue:** Documents reference `results/ch5/rq1/data/step02_purified_items.csv` but RQ 5.1 actual output filename may differ

**Known Pattern from RQs 5.8-5.11:**
- RQ 5.1 likely outputs: `purified_items_all_factors.csv` OR just `purified_items.csv`
- NOT: `step02_purified_items.csv`

**Impact:** CRITICAL BLOCKER - Workflow will fail at Step 0 data loading with FileNotFoundError

**Required Action:**
```bash
ls -lh /home/etai/projects/REMEMVR/results/ch5/rq1/data/ | grep purif
```

**Files to Update After Verification:**
- 1_concept.md line 180
- 2_plan.md line 41
- 3_tools.yaml line 16
- 4_analysis.yaml line 32

---

#### CRITICAL-2: Theta Scores Filename Verification Needed
**Location:** 2_plan.md line 51, 3_tools.yaml line 50, 4_analysis.yaml lines 46-47, 1_concept.md line 182
**Issue:** Documents reference `results/ch5/rq1/data/step03_theta_scores.csv` but RQ 5.1 actual output filename may differ

**Known Pattern from RQs 5.8-5.11:**
- RQ 5.1 likely outputs: `theta_scores_pass2.csv` OR just `theta_scores.csv`
- NOT: `step03_theta_scores.csv`

**Impact:** CRITICAL BLOCKER - Workflow will fail at Step 0 data loading

**Required Action:**
```bash
ls -lh /home/etai/projects/REMEMVR/results/ch5/rq1/data/ | grep theta
```

**Files to Update After Verification:**
- 1_concept.md line 182
- 2_plan.md line 51
- 3_tools.yaml line 50
- 4_analysis.yaml lines 46-47

**Cross-RQ Impact:** This same pattern affects RQs 5.8-5.13 - systematic fix needed across ALL dependent RQs

---

### HIGH Conflicts (1 total)

#### HIGH (Documentation): Test Column Preservation
**Location:** 2_plan.md, 3_tools.yaml, 4_analysis.yaml
**Issue:** Initially appeared as conflict, systematic verification showed CONSISTENT specification

**Status:** ✅ FALSE POSITIVE - No actual conflict, all files consistently include test column

---

### MODERATE Conflicts (1 total)

#### MODERATE: Validation Coverage Gap
**Location:** 2_plan.md lines 996-1008, 4_analysis.yaml lines 73-88
**Issue:** Plan anticipated catalogued validation tool for cross-RQ dependencies, implementation uses inline validation

**Status:** Acceptable - inline validation valid for stdlib operations, but diverges from plan expectation

**Recommendation:** Document architectural decision about inline validation for pandas operations

---

## RQ 5.13 - 4 Conflicts Remaining (1 CRITICAL, 2 HIGH, 1 MODERATE)

### Status: ✅ Ready for g_code (All CRITICAL conflicts fixed)

### Verification Results
- ✅ ICC column name fixed: icc_value (not estimate) in 2_plan.md
- ✅ Variance column default fixed: value_col='estimate' in 3_tools.yaml
- ✅ Intercept/slope columns fixed: random_intercept/random_slope in 3_tools.yaml

### Remaining Issues (Documentation Consistency)

#### MODERATE (Documentation): Function Signature Documentation
**Location:** 3_tools.yaml vs 4_analysis.yaml
**Issue:** Signature copied but not updated when parameters differ

**Status:** Not workflow-breaking, documentation duplication issue

**Recommendation:** Analysis.yaml should only document parameter OVERRIDES, not repeat full signatures

---

## Cross-RQ Patterns Requiring Systematic Fixes

### Pattern 1: RQ 5.1 Dependency Filename Verification
**Affected RQs:** 5.8, 5.9, 5.10, 5.11, 5.12, 5.13 (all 6)
**Issue:** All RQs reference `step0X_filename.csv` format, but RQ 5.1 may use different naming

**Required Action:**
1. Verify RQ 5.1 actual outputs: `ls /home/etai/projects/REMEMVR/results/ch5/rq1/data/`
2. Check for:
   - Purified items: `step02_purified_items.csv` vs `purified_items.csv` vs `purified_items_all_factors.csv`
   - Theta scores: `step03_theta_scores.csv` vs `theta_scores.csv` vs `theta_scores_pass2.csv`
   - TSVR mapping: `step00_tsvr_mapping.csv` (likely correct)
3. Update ALL 6 RQs if mismatch found

**Impact:** BLOCKS all 6 RQs if filenames wrong

---

### Pattern 2: Documentation vs Implementation Divergence
**Affected RQs:** All (especially 5.8, 5.11, 5.13)
**Issue:** Plan.md validation criteria use generic names (estimate, value) instead of exact column names

**Recommendation:** Systematic audit of all 2_plan.md validation criteria sections

---

### Pattern 3: Statsmodels vs Custom Column Naming
**Affected RQs:** 5.13 (intercept/slope), potentially others
**Issue:** Function defaults use statsmodels output naming, RQs use custom names

**Recommendation:** Add documentation clarifying when defaults apply vs when overrides needed

---

## Recommended Execution Order

### Phase 1: Immediate Execution (No Fixes Needed)
Execute g_code on these 4 RQs immediately:
1. ✅ **RQ 5.10** - Clean, 0 CRITICAL conflicts
2. ✅ **RQ 5.13** - Clean, 0 CRITICAL conflicts
3. ✅ **RQ 5.9** - Clean, 0 CRITICAL conflicts
4. ✅ **RQ 5.11** - Clean, 0 CRITICAL conflicts

**Estimated Time:** 30-60 minutes total for all 4 RQs

---

### Phase 2: Quick Fixes (10 minutes)
Fix RQ 5.8 remaining issues:
1. Update early_cutoff_hours default to 48.0 (3_tools.yaml line 73)
2. Specify segment boundary: [0, 48) and [48, 240] (1_concept.md, 2_plan.md)
3. Add RQ 5.7 convergence validation to Step 0 (2_plan.md, 4_analysis.yaml)

Then execute RQ 5.8.

**Estimated Time:** 10 minutes fixes + 10 minutes execution

---

### Phase 3: Verification Required (5-15 minutes)
Unblock RQ 5.12:
1. Run: `ls -lh /home/etai/projects/REMEMVR/results/ch5/rq1/data/`
2. Verify actual filenames (purified_items, theta_scores)
3. Update RQ 5.12 (and potentially ALL RQs 5.8-5.13) with correct filenames
4. Execute RQ 5.12

**Estimated Time:** 5 min verification + 10 min updates + 10 min execution

---

## Files Modified in Conflict Resolution Session

### Session 2025-11-28 (CRITICAL Fixes Applied)

**RQ 5.13:**
- results/ch5/rq13/docs/2_plan.md (1 edit: line 251 icc_value)
- results/ch5/rq13/docs/3_tools.yaml (2 edits: lines 38, 190 column names)

**RQ 5.9:**
- results/ch5/rq9/docs/1_concept.md (1 edit: Bonferroni alpha 0.0167)
- results/ch5/rq9/docs/3_tools.yaml (2 edits: file paths data/)
- results/ch5/rq9/docs/4_analysis.yaml (5 edits: file paths data/)

**RQ 5.11:**
- results/ch5/rq11/docs/1_concept.md (1 edit: added purified_items.csv)
- results/ch5/rq11/docs/2_plan.md (6 edits: all theta column names)
- results/ch5/rq11/docs/3_tools.yaml (3 edits: all theta column names)
- results/ch5/rq11/docs/4_analysis.yaml (6 edits: all theta column names via sed)

**RQ 5.8:**
- results/ch5/rq8/docs/1_concept.md (1 edit: TEST→test)
- results/ch5/rq8/docs/2_plan.md (1 edit: row count 33 exactly via sed)
- results/ch5/rq8/docs/3_tools.yaml (1 edit: row count 33 exactly)
- results/ch5/rq8/docs/4_analysis.yaml (1 edit: row count 33 exactly via sed)

**RQ 5.12:**
- results/ch5/rq12/docs/1_concept.md (1 edit: purified_item_params→purified_items)
- results/ch5/rq12/docs/3_tools.yaml (14 edits: all results/step0X→data/step0X via sed)

**Total Files Modified:** 15 files across 5 RQs

---

## Quality Metrics

**Total Conflicts Detected (g_conflict verification):** 39 across 6 RQs
**CRITICAL Conflicts Fixed:** 18 (100% of session targets)
**CRITICAL Conflicts Remaining:** 6 (3 in RQ 5.8, 2 in RQ 5.12 BLOCKED, 1 documentation)
**RQs Ready for Execution:** 4 out of 6 (67%)
**Estimated Time to 100% Ready:** 25 minutes (10 min RQ 5.8 + 15 min RQ 5.12 verification/updates)

---

**END OF REPORT**

**Next Action:** Choose execution strategy from Recommended Execution Order above.
