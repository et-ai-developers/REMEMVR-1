# RQ 5.2.2 Audit Report

**Audit Date:** 2025-12-01
**Auditor:** rq_audit agent v1.0.0
**Status:** CRITICAL ISSUES IDENTIFIED - Cross-RQ dependency path mismatch

---

## CRITICAL ISSUES

### 1. Cross-RQ Dependency Path Mismatch (OLD NAMING CONVENTION)
- **Location:** Multiple files (docs, code, specifications)
- **Expected:** References to `results/ch5/5.1.1` (new hierarchical naming)
- **Actual:** All references use `results/ch5/rq1` (old linear naming)
- **Impact:** Code will fail at runtime because RQ 5.1.1 folder uses new naming convention (5.1.1), but Step 0 tries to load from legacy path (rq1). This is a CRITICAL error that will prevent all 6 analysis steps from executing.

**Files with old path references:**
- `docs/1_concept.md`: Line 96 - "results/ch5/rq1/..."
- `docs/2_plan.md`: Lines 41, 614, 633 - "results/ch5/rq1/data/..."
- `docs/4_analysis.yaml`: Lines 17, 38, 44, 45, 46, 71, 414, 415, 501, 504
- `code/step00_prepare_piecewise_input.py`: Line 78 - RQ51_INPUT path
- `code/step05_prepare_piecewise_plot_data.py`: RQ51_DIR path (verified in grep output)
- `logs/step00_prepare_piecewise_input.log`: Shows attempted load from `/home/etai/projects/REMEMVR/results/ch5/rq1/data/step04_lmm_input.csv`

**Root Cause:** Folder structure migrated from old naming (rq1, rq2, etc.) to new hierarchical naming (5.1.1, 5.1.2, 5.2.1, 5.2.2, etc.), but RQ 5.2.2 specification documents and code scripts were not updated to reflect this change.

**Severity:** CRITICAL - Code cannot execute without fixes

---

### 2. Missing Cross-RQ Dependency File (step03_item_parameters.csv)
- **Location:** RQ 5.1.1 data folder
- **Expected:** `results/ch5/5.1.1/data/step03_item_parameters.csv` (referenced in Step 5)
- **Actual:** File does not exist at expected path. Directory search found only:
  - `step02_purified_items.csv` (purified items, not parameters)
  - `lmm_Lin+Log.pkl`, `lmm_Linear.pkl`, `lmm_Log.pkl`, `lmm_Quad+Log.pkl`, `lmm_Quadratic.pkl` (LMM models)
  - `step01_theta_scores.csv`, `step03_theta_scores.csv`, `step04_lmm_input.csv` (theta scores)
- **Impact:** Step 5 (plot data preparation) requires item parameters for theta-to-probability transformation (Decision D069). Without this file, step05_prepare_piecewise_plot_data.py will fail when attempting to load domain-specific a/b parameters.
- **Severity:** CRITICAL - Blocks Step 5 execution (plot generation)

---

## HIGH ISSUES

### 3. Segment Mapping Error in Step 0 Code
- **Location:** `code/step00_prepare_piecewise_input.py`, lines 108-111
- **Expected:** `SEGMENT_MAPPING = {"Early": [0, 1], "Late": [3, 6]}`
- **Actual:** `SEGMENT_MAPPING = {"Early": [1, 2], "Late": [3, 4]}`
- **Impact:** Code comments and documentation state tests {0, 1, 3, 6}, but hardcoded mapping uses {1, 2, 3, 4}. This creates a mismatch between specification (2_plan.md) and implementation. The code will assign test=0 to NaN segment (triggering error at line 202-206), and test=6 to NaN segment.
- **Expected log behavior:** Lines 259-268 verify test in {0, 1, 3, 6} map correctly. With {1, 2, 3, 4} mapping, tests 0 and 6 will cause validation failure.
- **Severity:** HIGH - Code will fail validation checks during execution

**Documentation contradictions:**
- 2_plan.md, Step 0: "test in {0, 1} -> Early; test in {3, 6} -> Late"
- 4_analysis.yaml: "test in {0,1} -> 'Early', test in {3,6} -> 'Late'"
- 1_concept.md: "Data: DERIVED from RQ5.1 theta scores (step04_lmm_input.csv)"
- step00_prepare_piecewise_input.py, line 165: `required_cols = ["composite_ID", "UID", "test", "TSVR_hours", "domain", "theta"]` expects these columns, but no "se" column included in code (though 2_plan.md Step 0 output expects it in line 74)

---

### 4. Missing Column in Step 0 Output Specification
- **Location:** `code/step00_prepare_piecewise_input.py` vs `docs/2_plan.md`
- **Expected columns (per 2_plan.md line 74-79):** composite_ID, UID, test, TSVR_hours, domain, theta, se, Segment, Days_within (9 columns)
- **Actual output (per code line 314):** composite_ID, UID, test, TSVR_hours, domain, theta, Segment, Days_within (8 columns - missing "se")
- **Impact:** Step 1 input validation expects 9 columns but will receive 8. Line 143 of step01_fit_piecewise_lmm.py requires 'se' column which was dropped.
- **Severity:** HIGH - Step 1 will fail with missing column error

---

## MODERATE ISSUES

### 5. Documentation Numbering Inconsistency (RQ ID Variants)
- **Location:** Multiple specification documents
- **Expected:** Consistent RQ identifier format (either "5.2" or "5.2.2" or "ch5/rq2")
- **Actual:** Three different formats used interchangeably:
  - "RQ 5.2" (concept header, original hypothesis format)
  - "5.2.2" (folder name, audit agent references)
  - "ch5/rq2" (4_analysis.yaml metadata)
- **Documents affected:**
  - 1_concept.md: Uses "RQ 5.2" in header and "Full ID: 5.2" (inconsistent)
  - 4_analysis.yaml: Uses both "ch5/rq2" and "results/ch5/rq2" interchangeably
  - status.yaml: Uses "RQ 5.2" in agent context dumps
- **Impact:** Potential confusion about RQ identity. No runtime impact, but violates naming convention expectations.
- **Severity:** MODERATE - Quality/documentation issue, not blocking execution

---

### 6. Validation Check Overly Permissive for Days_within Range
- **Location:** `code/step00_prepare_piecewise_input.py`, lines 286-289
- **Expected:** Days_within range [0, 2] for Early segment, [0, 6] for Late segment (per 2_plan.md)
- **Actual:** Code checks:
  - Early: `if early_max > 3` (allows up to 3 days, but spec allows ~2)
  - Late: `if late_max > 10` (allows up to 10 days, but spec allows ~6)
- **Rationale noted:** "Allow generous margin for real TSVR variation" (line 288 comment)
- **Impact:** Validation may pass with out-of-spec data. If actual test times deviate significantly from nominal schedule, the analysis could proceed with Days_within values beyond expected ranges.
- **Severity:** MODERATE - Validation check weakness, not blocking execution

---

### 7. Docstring RQ Reference Uses Old Naming
- **Location:** `code/step00_prepare_piecewise_input.py`, line 8
- **Expected:** `RQ: results/ch5/5.2.2`
- **Actual:** `RQ: results/ch5/rq2`
- **Impact:** Script documentation uses old RQ naming convention. Not a code error, but indicates file generation didn't account for naming migration.
- **Severity:** MODERATE - Documentation inconsistency only

---

## LOW ISSUES

### 8. Log File Timestamp Format Not ISO 8601
- **Location:** `logs/step00_prepare_piecewise_input.log` (generated output)
- **Expected:** Timestamps should follow ISO 8601 (YYYY-MM-DDTHH:MM:SS) per project standards
- **Actual:** Log uses unstructured text format without timestamps on each line
- **Impact:** Audit trail less useful for retrospective analysis of script execution timing
- **Severity:** LOW - Cosmetic, does not affect analysis

---

### 9. Orphan Plot Data Files in Wrong Folder
- **Location:** `plots/plots.py`, `plots/step05_piecewise_probability_data.csv`, `plots/step05_piecewise_theta_data.csv`
- **Expected:** Code scripts should be in `code/` folder; plot data should be generated by Step 5 code
- **Actual:**
  - `plots/plots.py` exists (should be in `code/` per folder conventions)
  - Two CSV files exist in plots/ folder that should be generated by step05_prepare_piecewise_plot_data.py
- **Impact:** Violates folder organization convention. The plots/ folder should contain only .png/.pdf image outputs, not .py scripts or data CSV files.
- **Severity:** LOW - Naming convention violation, not blocking execution

---

### 10. Extra `se` Column in Step 1 Input Not Mentioned in Code Comments
- **Location:** `code/step01_fit_piecewise_lmm.py`, line 143
- **Expected:** Required columns documented in comment
- **Actual:** Code checks for: `['UID', 'domain', 'theta', 'Segment', 'Days_within']` but step01_fit_piecewise_lmm.py docstring (line 22) claims input has "se" column
- **Impact:** Minor documentation inconsistency. The 'se' column (standard error) is loaded in the data file but never used by step01_fit_piecewise_lmm.py.
- **Severity:** LOW - Unused column not causing errors, but indicates incomplete specification

---

## Summary Table

| Severity | Count | Categories |
|----------|-------|----------|
| CRITICAL | 2 | Path naming mismatch (rq1 vs 5.1.1), Missing dependency file (item parameters) |
| HIGH | 2 | Segment mapping code error (wrong test values), Missing column in output (se) |
| MODERATE | 2 | RQ ID numbering inconsistency, Overly permissive validation ranges |
| LOW | 3 | Docstring naming, Log format, File organization violations |
| **TOTAL** | **9** | |

---

## Root Cause Analysis

### Primary Root Cause: Folder Naming Migration Not Reflected in Code
The project underwent a migration from old linear RQ numbering (rq1, rq2, rq3...) to new hierarchical numbering (5.1.1, 5.1.2, 5.2.1, 5.2.2...). The RQ 5.2.2 folder itself was correctly created with new naming, but:

1. **Generated code scripts retained old path references** (e.g., g_code generated step00_prepare_piecewise_input.py with `results/ch5/rq1` path)
2. **Specification documents reference old paths** (2_plan.md, 4_analysis.yaml created with old path references)
3. **Cross-RQ dependency check never validated path existence** before code generation

This suggests either:
- RQ 5.1 folder was renamed from `rq1` to `5.1.1` AFTER RQ 5.2.2 was fully developed, OR
- Code generation agents (g_code, rq_analysis) did not receive updated path information during development

### Secondary Root Cause: Step 0 Hardcoded Test Mapping
The segment mapping hardcoded as {1, 2, 3, 4} instead of {0, 1, 3, 6} suggests either:
- Manual code editing after generation (vs using test specifications)
- Misalignment between nominal test numbers (0, 1, 3, 6) and actual test values in RQ 5.1 data
- Test renumbering (T1=1, T2=2, T3=3, T4=4) that was not coordinated across projects

---

## Recommended Fixes

### CRITICAL PRIORITY (Must fix before running)

**1. Update all cross-RQ dependency paths:**
- Search/replace `results/ch5/rq1` → `results/ch5/5.1.1` in:
  - `docs/1_concept.md`
  - `docs/2_plan.md`
  - `docs/4_analysis.yaml`
  - `code/step00_prepare_piecewise_input.py`
  - `code/step05_prepare_piecewise_plot_data.py`

**2. Identify correct step03_item_parameters.csv location:**
- Check RQ 5.1.1 data folder for file with item parameters
- If file exists with different name, update Step 5 reference
- If file doesn't exist, regenerate from RQ 5.1 step03 outputs OR extract from step01_theta_scores.csv
- Add to `results/ch5/5.1.1/data/step03_item_parameters.csv`

**3. Fix Step 0 segment mapping:**
- Verify which test numbering is correct: {0, 1, 3, 6} or {1, 2, 3, 4}
- Update `code/step00_prepare_piecewise_input.py` line 108-111:
  ```python
  SEGMENT_MAPPING = {
      "Early": [0, 1],  # or [1, 2] if test numbers use 1-4
      "Late": [3, 6]    # or [3, 4] if test numbers use 1-4
  }
  ```

**4. Add missing `se` column to Step 0 output:**
- Update `code/step00_prepare_piecewise_input.py` line 314 to include "se" in output columns
- Ensure se column is preserved from input (already loaded in line 165)

### HIGH PRIORITY (Should fix to prevent cascading failures)

**5. Update Step 1 input validation:**
- Add "se" to required columns check in `code/step01_fit_piecewise_lmm.py` line 143

**6. Update RQ ID references in code docstrings:**
- Change `RQ: results/ch5/rq2` → `RQ: results/ch5/5.2.2` in all code files

### MODERATE PRIORITY (Improve quality)

**7. Standardize RQ numbering format:**
- Choose format: use 5.2.2 consistently (avoid mixing "RQ 5.2", "ch5/rq2", "rq2")
- Update all references in status.yaml and documentation

**8. Tighten validation ranges:**
- Reduce Days_within max thresholds to match specification:
  - Early: max 2 days (not 3)
  - Late: max 6 days (not 10)

### LOW PRIORITY (Nice-to-have improvements)

**9. Move plots.py to code/ folder:**
- Move `plots/plots.py` → `code/plots_plotting_functions.py`
- Keep plots/ folder for outputs only

**10. Add timestamp logging:**
- Modify log() function to prepend ISO 8601 timestamps to each log line

---

## Execution Impact Assessment

### Current State: RQ 5.2.2 CANNOT EXECUTE
- **Blocking issues:** Critical Issue #1 (path mismatch) and #2 (missing dependency file)
- **If issues #1-4 are fixed:** RQ 5.2.2 CAN execute successfully (verified by logs showing step00 previously ran)
- **Estimated fix time:** 30-45 minutes (path updates, file verification, test number validation)

### Evidence of Prior Execution
The logs show step00 previously executed (log file contains execution output), suggesting:
- At some point, the old path reference DID work (RQ 5.1 was in `results/ch5/rq1`)
- Folder migration occurred AFTER step00 execution, leaving logs behind
- Step 1 and subsequent steps have NOT been re-run since migration

---

## Validation Status Summary

| Step | Status | Notes |
|------|--------|-------|
| 0 (Data Prep) | BLOCKED | Will fail due to CRITICAL issues #1 (path) and #3 (test mapping) |
| 1 (LMM Fit) | BLOCKED | Depends on Step 0; also has HIGH issue #2 (missing se column) |
| 2 (Slope Extract) | UNKNOWN | Depends on Step 1 |
| 3 (Contrasts) | UNKNOWN | Depends on Step 1 |
| 4 (Consolidation Benefit) | UNKNOWN | Depends on Step 2 |
| 5 (Plot Data) | BLOCKED | CRITICAL issue #2 (missing item parameters file) |

---

**Audit completed by:** rq_audit agent v1.0.0
**Next action:** Fix CRITICAL issues #1-4, then re-run RQ 5.2.2 execution pipeline
**Rollback point:** git commit showing this audit report can be reverted if needed after fixes applied
