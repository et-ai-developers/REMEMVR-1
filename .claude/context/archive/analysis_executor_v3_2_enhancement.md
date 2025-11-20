# Analysis-Executor v3.2 Enhancement

**Last Updated:** 2025-11-14 (context-manager curation)
**Topic:** Analysis-executor v3.2 tool validation enhancement
**Status:** Complete - Superseded by v3.3

---

## Analysis-Executor v3.2 Enhancement - Added Tool Validation (2025-11-14 20:30)

**Archived from:** state.md Session (2025-11-14 20:30)
**Original Date:** 2025-11-14
**Reason:** Enhancement complete, superseded by v3.3 (API signature understanding)

---

### Problem

Agent generated script using `calibrate_grm()` function that doesn't exist, crashed with ImportError. Agent had NO mechanism to validate functions exist before generating script.

**Root Cause:** Agent prompt missing Step 1.5 (Validate Tool Functions Exist)

---

### User Feedback

"Don't fix the script. The analysis-executor should have told us that it needs functions that don't exist!"

---

### Enhancement: v3.2

**Added:** Step 1.5: Validate Tool Functions Exist (Lines 252-324, +73 lines)

**Procedure:**
1. Reads tools/ source files
2. Parses function definitions
3. Validates each config.yaml function exists
4. QUITS with MissingTool error if ANY missing

---

### v3.2 Test - Successful Validation Failure

**Result:** Agent correctly QUIT with MissingTool error (as designed)

**Missing Functions (5/10, 50% failure):**
- **tools/analysis_irt.py:** calibrate_grm (alternative exists), purify_items (CRITICAL D039)
- **tools/analysis_lmm.py:** post_hoc_contrasts (D068), compute_effect_sizes
- **tools/plotting.py:** plot_trajectory_probability (D069)

---

### Files Modified

- `.claude/agents/analysis_executor.md` (559 → 644 lines, v3.1 → v3.2)

---

### Next Steps (from this session)

1. Implement missing 5 functions (TDD)
2. Re-run analysis_executor v3.2 (should pass validation)
3. User runs generated analysis script
4. Results validation

---

**Note:** v3.2 validated functions EXIST but didn't know HOW to call them. v3.3 added API signature understanding via tools_inventory.md loading.

---
