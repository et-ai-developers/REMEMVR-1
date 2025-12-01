# RQ 5.3.2 Audit Report

**Audit Date:** 2025-12-01
**Auditor:** rq_audit agent v1.0.0
**RQ ID:** 5.3.2 (Linear Trend in Forgetting Rate Across Paradigms)
**Status:** 4 issues identified

---

## CRITICAL ISSUES

### 1. Path Reference Mismatch - Old Naming Convention in Code and Documentation

- **Location:** Multiple files - documentation and code
  - `docs/1_concept.md`: line 134-135 (data source section)
  - `docs/2_plan.md`: lines 41, 46, 60 (file paths)
  - `docs/4_analysis.yaml`: lines 21, 55-72 (metadata and file paths)
  - `code/step00_load_rq53_outputs.py`: lines 76-77, 123-125 (file path construction)
  - `code/step01_extract_marginal_means.py`: lines 66-67 (file path construction)
  - `code/step02_compute_linear_trend_contrast.py`: lines 71-72 (file path construction)

- **Expected:** Paths should reference new RQ numbering: `results/ch5/5.3.1/data/` (actual folder)

- **Actual:** Documentation and code reference old naming: `results/ch5/rq3/data/` (non-existent folder)

- **Impact:**
  - **CRITICAL for execution:** Code will fail at runtime when attempting to load files from `results/ch5/rq3/` because this folder does NOT exist
  - Correct folder exists at `results/ch5/5.3.1/` with all required files:
    - `step05_lmm_fitted_model.pkl` (exists, 479KB)
    - `step04_lmm_input.csv` (exists, 87KB)
    - `step05_model_comparison.csv` (exists)
  - All Python scripts will fail at Step 0 with FileNotFoundError
  - Relative path references (`../rq3/data/`) in code will resolve to non-existent location

**Root Cause:** RQ numbering was refactored from old format (rq1, rq2, rq3...) to hierarchical format (5.1.1, 5.1.2, 5.3.1...) but documentation and code were not updated to match.

**Recommended Fix:**
1. Replace all references to `rq3` with `5.3.1` in:
   - `docs/1_concept.md` (Data Source section)
   - `docs/2_plan.md` (Step 0 input specification)
   - `docs/4_analysis.yaml` (metadata.dependencies section and all input_files paths)
   - All code files: `step00_load_rq53_outputs.py`, `step01_extract_marginal_means.py`, `step02_compute_linear_trend_contrast.py`

2. Update references from `results/ch5/rq3/` to `results/ch5/5.3.1/` (absolute paths)

3. Verify all relative path calculations still work correctly after update

---

## HIGH ISSUES

### 2. RQ ID Naming Inconsistency Across Documentation

- **Location:**
  - `docs/1_concept.md`: header "# RQ 5.4" vs folder name "5.3.2"
  - `docs/2_plan.md`: header "RQ 5.4" vs folder name "5.3.2"
  - `status.yaml`: references "rq4" (line 8)
  - `code/step00_load_rq53_outputs.py`: references "results/ch5/rq4" (line 8, docstring)
  - `code/step01_extract_marginal_means.py`: references "results/ch5/rq4" (line 8, docstring)
  - `code/step02_compute_linear_trend_contrast.py`: references "results/ch5/rq4" (line 8, docstring)
  - `code/step03_prepare_paradigm_plot_data.py`: references "results/ch5/rq4" (line 8, docstring)

- **Expected:** Consistent RQ naming across all documents:
  - Folder name: `5.3.2` indicates RQ 5.3.2 (subset of RQ 5.3)
  - Documents should reference "RQ 5.3.2" or "RQ 5.4" - currently mixing both

- **Actual:**
  - Folder name uses new numbering: `5.3.2`
  - Documents use mixed naming: some say "RQ 5.4", some say "RQ 5.3.2", code says "rq4"
  - This creates ambiguity about which RQ this is (5.3.2 vs 5.4)

- **Impact:**
  - **HIGH confusion potential:** Reader cannot definitively determine which RQ this is
  - Violates naming convention - folder name should match document RQ ID
  - Will cause maintenance issues when referencing this RQ in thesis or future work
  - Mapping table indicates: `rq4 -> 5.3.2` (from rq_refactor.tsv), confirming this is RQ 5.3.2

**Root Cause:** Incomplete refactoring from old single-number RQ system (rq1, rq2, rq3, rq4...) to new hierarchical system (5.1.1, 5.1.2, 5.3.2...). Some files updated, others not.

**Recommended Fix:**
1. Standardize all documents to use "RQ 5.3.2" consistently
2. Update headers in:
   - `docs/1_concept.md`: Change "RQ 5.4" → "RQ 5.3.2"
   - `docs/2_plan.md`: Change "RQ 5.4" → "RQ 5.3.2"
   - `docs/4_analysis.yaml`: Change `rq_id: "ch5/rq4"` → `rq_id: "ch5/5.3.2"` (line 11)
   - All Python scripts: Update docstring RQ references from `results/ch5/rq4` to `results/ch5/5.3.2`

3. Verify mapping in `rq_refactor.tsv` is correctly documented

---

### 3. Step 04 LMM Input Data Path Reference Mismatch

- **Location:**
  - `docs/2_plan.md`: lines 46-57 (Step 0 input specification)
  - `docs/4_analysis.yaml`: lines 60-66 (step00 input_files, second file)

- **Expected:** File should be named `step04_lmm_input.csv` (matching naming convention: stepXX_description)

- **Actual:** Documentation correctly references `step04_lmm_input.csv`
  - BUT: Folder reference is wrong: references `results/ch5/rq3/data/` (non-existent)
  - Correct path should be: `results/ch5/5.3.1/data/step04_lmm_input.csv`

- **Impact:** This is secondary to Issue #1 (path reference mismatch) - will be fixed by same correction

**Note:** This issue is subsumed by Issue #1 but flagged separately because it affects critical input data loading.

---

## MODERATE ISSUES

### 4. Status File References Old RQ Naming Convention

- **Location:** `status.yaml`
  - Line 8 (script metadata): `RQ: results/ch5/rq4`
  - Lines 14-26 (rq_concept context_dump): `RQ5.4:`
  - Line 59 (rq_planner context_dump): `Depends on RQ 5.3 complete`

- **Expected:**
  - RQ ID should be `ch5/5.3.2` (new hierarchical format)
  - References should say "RQ 5.3.2" or "RQ 5.3.2 (Linear Trend..."

- **Actual:**
  - References mix old and new: `rq4` (old), `RQ5.4` (semi-old), `RQ5.3` (partially new)
  - Creates version confusion

- **Impact:**
  - **MODERATE:** Status file is read by agents during workflow
  - Inconsistent RQ IDs in context_dump will cause confusion if agents reference this file
  - Does not prevent execution but violates documentation consistency standards

**Root Cause:** Partial update of status.yaml during refactoring

**Recommended Fix:**
1. Update all RQ references in `status.yaml`:
   - Line 8: Change `RQ: results/ch5/rq4` → `RQ: results/ch5/5.3.2`
   - All context_dump entries: Change `RQ5.4` → `RQ 5.3.2`
   - Ensure all RQ references use new hierarchical format consistently

---

## Summary Table

| Severity | Count | Category | Status |
|----------|-------|----------|--------|
| CRITICAL | 1 | Path references to non-existent folders (rq3 -> must be 5.3.1) | Will cause runtime failure |
| HIGH | 2 | RQ ID naming inconsistency (5.3.2 vs 5.4 mixing) | Confusion/maintenance issue |
| MODERATE | 1 | Status file outdated RQ references | Version tracking issue |
| LOW | 0 | N/A | N/A |
| **TOTAL** | **4** | **All related to RQ numbering refactoring** | **All actionable** |

---

## Root Cause Analysis

**Primary Cause:** Incomplete refactoring from old RQ naming (rq1, rq2, rq3, rq4...) to new hierarchical naming (5.1.1, 5.1.2, 5.3.2, 5.4.1...).

**Evidence:**
- Folder structure uses NEW naming: `5.3.2`
- Documentation/code mixes OLD and NEW naming: "rq4" and "5.3.2" and "RQ 5.4"
- Path references point to OLD location: `results/ch5/rq3/` (doesn't exist)
- Actual dependency is at NEW location: `results/ch5/5.3.1/` (exists)
- Mapping exists in `rq_refactor.tsv` confirming: `rq4 -> 5.3.2` and `rq3 -> 5.3.1`

**Likely Scenario:**
1. RQ numbering refactored at some point (dates suggest Nov 30, 2025)
2. Folders renamed successfully (`rq3` → `5.3.1`, `rq4` → `5.3.2`)
3. High-level documentation headers updated (`docs/*.md` files)
4. Low-level code and path references NOT updated (still reference `rq3`, `rq4`)
5. This RQ was not tested/executed since refactoring, so failures not detected

**Confirmation:**
- `results/ch5/5.3.1/data/step05_lmm_fitted_model.pkl` exists ✓
- `results/ch5/5.3.1/data/step04_lmm_input.csv` exists ✓
- `results/ch5/rq3/` does NOT exist ✗
- Code will fail when trying to load from non-existent location ✗

---

## Recommended Fixes

### Priority 1 (CRITICAL - Fix Before Execution)

**Update all path references to use new folder name:**

1. **docs/1_concept.md**
   - Line 134: Change `results/ch5/rq3/data/` → `results/ch5/5.3.1/data/`
   - Line 135: Change `results/ch5/rq3/code/` → `results/ch5/5.3.1/code/`

2. **docs/2_plan.md**
   - Line 41: Change `results/ch5/rq3/data/step05_lmm_fitted_model.pkl` → `results/ch5/5.3.1/data/step05_lmm_fitted_model.pkl`
   - Line 46: Change `results/ch5/rq3/data/step04_lmm_input.csv` → `results/ch5/5.3.1/data/step04_lmm_input.csv`
   - Line 60: Change `results/ch5/rq3/data/step05_model_comparison.csv` → `results/ch5/5.3.1/data/step05_model_comparison.csv`

3. **docs/4_analysis.yaml**
   - Line 18: Change `rq: "ch5/rq3"` → `rq: "ch5/5.3.1"`
   - Lines 21, 22, 23: Update all `results/ch5/rq3/data/` paths → `results/ch5/5.3.1/data/`
   - Lines 55, 60, 67: Update all absolute_path values to match

4. **code/step00_load_rq53_outputs.py**
   - Line 76-77: RQ_DIR path construction is OK (uses `parents[1]`)
   - Line 77: Change `RQ3_DIR = RQ_DIR.parent / "rq3"` → `RQ3_DIR = RQ_DIR.parent / "5.3.1"`
   - Lines 123-125: Verify paths construct correctly after above change

5. **code/step01_extract_marginal_means.py**
   - Line 67: Change `RQ3_DIR = RQ_DIR.parent / "rq3"` → `RQ3_DIR = RQ_DIR.parent / "5.3.1"`

6. **code/step02_compute_linear_trend_contrast.py**
   - Line 72: Change `RQ3_DIR = RQ_DIR.parent / "rq3"` → `RQ3_DIR = RQ_DIR.parent / "5.3.1"`

7. **code/step03_prepare_paradigm_plot_data.py**
   - No RQ3_DIR reference in this file (does not depend on RQ 5.3.1 directly)
   - But verify any path references don't include "rq3" or "rq4"

### Priority 2 (HIGH - Fix for Consistency)

**Standardize RQ ID naming across all documents:**

1. **docs/1_concept.md**
   - Line 1: Change `# RQ 5.4:` → `# RQ 5.3.2:`
   - Line 4: Change `**RQ Number:** 4` → `**RQ Number:** 5.3.2`
   - Line 5: Change `**Full ID:** 5.4` → `**Full ID:** 5.3.2`

2. **docs/2_plan.md**
   - Line 1: Change `# Analysis Plan for RQ 5.4:` → `# Analysis Plan for RQ 5.3.2:`
   - Line 11: Change `RQ 5.4 tests` → `RQ 5.3.2 tests`

3. **docs/4_analysis.yaml**
   - Line 11: Change `rq_id: "ch5/rq4"` → `rq_id: "ch5/5.3.2"`

4. **All code files:**
   - Update docstrings (lines 6-8) from `RQ: results/ch5/rq4` → `RQ: results/ch5/5.3.2`
   - Example: `step00_load_rq53_outputs.py` line 8

### Priority 3 (MODERATE - Fix for Completeness)

**Update status.yaml with new RQ naming:**

1. **status.yaml**
   - Line 8: `RQ: results/ch5/rq4` → `RQ: results/ch5/5.3.2`
   - All context_dump entries: `RQ5.4` → `RQ 5.3.2`

---

## Verification Checklist

After applying fixes, verify:

- [ ] All paths reference `results/ch5/5.3.1/` for RQ 5.3 dependency (not `rq3`)
- [ ] All RQ IDs standardized to "5.3.2" (not "5.4" or "rq4")
- [ ] Code can locate RQ 5.3.1 output files at correct path
- [ ] No references to non-existent folders remain
- [ ] Documentation and code RQ IDs match

---

## Notes

- **No data corruption detected:** All required input files exist at correct location
- **No logic errors detected:** Code and analysis specifications are scientifically sound
- **Execution blocker:** Code will fail at Step 0 due to path mismatch - MUST fix before running
- **Non-critical issues:** RQ naming inconsistency creates confusion but doesn't affect logic
- **Confidence level:** HIGH - root cause is clear, fixes are straightforward

---

**End of Audit Report**

**Next Steps:** Apply Priority 1 fixes before executing this RQ. Code will not run until path references are corrected.
