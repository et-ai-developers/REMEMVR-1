# RQ 5.2.1 Audit Report

**Audit Date:** 2025-12-01
**Auditor:** rq_audit agent v1.0.0
**Status:** 4 issues identified

---

## CRITICAL ISSUES

### 1. RQ ID Numbering Inconsistency (Folder vs Documents)
- **Location:** Multiple files across docs/, code/
- **Expected:** All RQ IDs should reference "5.2.1" (new hierarchical naming per refactor)
- **Actual:** Documents and code reference old "5.1" or "ch5/rq1" formats
- **Impact:** Creates confusion about RQ identity; downstream RQs (5.2.2, 5.2.3, etc.) will struggle to reference this RQ correctly; git history shows refactor completed but RQ 5.2.1 not fully updated
- **Details:**
  - Folder name: `5.2.1` (correct new format)
  - Concept doc header: "RQ 5.1: Domain-Specific..." (OLD format)
  - Analysis YAML: `rq_id: "ch5/rq1"` (OLD format)
  - Code files: `RQ: results/ch5/rq1` (OLD format)
  - Code paths: `RQ_DIR = Path("/home/etai/projects/REMEMVR/results/ch5/rq1")` (OLD path)
  - Count: 15+ occurrences across code files, 8+ in docs/

---

### 2. Code File Hardcoded Path References (May Break on Execution)
- **Location:** code/step02_purify_items.py, code/step04_merge_theta_tsvr.py, code/step05_fit_lmm.py
- **Expected:** Code should use relative paths or `Path(__file__).resolve().parents[1]` pattern
- **Actual:** Hardcoded absolute paths like `Path("/home/etai/projects/REMEMVR/results/ch5/rq1")`
- **Impact:** If RQ folder is renamed or moved, code will reference non-existent path and fail at runtime
- **Example Code References Found:**
  - `step02_purify_items.py` line: `RQ_DIR = Path("/home/etai/projects/REMEMVR/results/ch5/rq1")`
  - `step04_merge_theta_tsvr.py` line: `RQ_DIR = Path("/home/etai/projects/REMEMVR/results/ch5/rq1")`
  - `step05_fit_lmm.py` line: `RQ_DIR = Path("/home/etai/projects/REMEMVR/results/ch5/rq1")`

---

## HIGH ISSUES

### 3. Documentation Inconsistency: RQ ID in Analysis Recipe
- **Location:** docs/4_analysis.yaml, lines 5-11
- **Expected:** `rq_id: "ch5/5.2.1"` (hierarchical format to match folder structure)
- **Actual:** `rq_id: "ch5/rq1"` (old sequential format)
- **Impact:** When g_code reads 4_analysis.yaml, it will use wrong RQ identifier for logging and error messages; makes it harder to trace which RQ produced which outputs in multi-RQ runs
- **Evidence:** rq_refactor.tsv line 8 shows correct mapping: "5.2.1" <-> "5.1" (old)

---

### 4. Concept Document Missing RQ ID Update
- **Location:** docs/1_concept.md, lines 1-5
- **Expected:**
  ```
  # RQ 5.2.1: Domain-Specific Forgetting Trajectories (What/Where/When)
  **Chapter:** 5
  **RQ Number:** 2.1
  **Full ID:** 5.2.1
  ```
- **Actual:**
  ```
  # RQ 5.1: Domain-Specific Forgetting Trajectories (What/Where/When)
  **Chapter:** 5
  **RQ Number:** 1
  **Full ID:** 5.1
  ```
- **Impact:** Users reading concept.md will believe this is RQ 5.1, not 5.2.1; creates potential for cross-RQ dependency errors (when downstream RQs try to reference this RQ using folder name 5.2.1)

---

## MODERATE ISSUES

### 5. Status.yaml Contains Legacy Folder References
- **Location:** status.yaml, line 4
- **Expected:** `Created results/ch5/5.2.1/ with 6 folders` (to match current folder)
- **Actual:** `Created results/ch5/rq1/ with 6 folders`
- **Impact:** Status document is historical record; inconsistency suggests refactor was incomplete or status.yaml was not updated during migration
- **Note:** This is informational only (not executed) but creates confusion in git history

---

## Summary Table

| Severity | Count | Category |
|----------|-------|----------|
| CRITICAL | 2 | RQ ID numbering, Path references |
| HIGH | 2 | Analysis YAML RQ ID, Concept doc mismatch |
| MODERATE | 1 | Status documentation |
| **TOTAL** | **5** | |

---

## Root Cause Analysis

**Likely Cause:** RQ refactor from sequential (rq1, rq2, ...) to hierarchical (5.1.1, 5.2.1, 5.3.1, ...) was executed at the folder level but the RQ 5.2.1 folder was not fully migrated.

**Evidence:**
1. Folder structure renamed correctly: `/results/ch5/5.2.1/` exists (new format)
2. However, internal files still reference old naming: "rq1", "ch5/rq1"
3. Git history shows refactor commitment (commit 6029c03: "Context save: rq_refactor.tsv extended with 6 columns, path migration rqN→5.X.X complete") but this RQ was missed
4. rq_refactor.tsv shows mapping exists: 5.2.1 <-> 5.1, indicating refactor planning was done but not executed for this RQ

**Severity:** The CRITICAL issues will cause problems when:
- Downstream RQs (5.2.2, 5.2.3) try to reference this RQ's outputs using folder name 5.2.1 but code/docs say 5.1
- Code is executed in a different directory or after folder migration
- Users or agents search the codebase for "5.2.1" and find nothing due to old ID references

---

## Recommended Fixes

1. **Update docs/1_concept.md (Header and Full ID)**
   - Line 1: Change `# RQ 5.1:` to `# RQ 5.2.1:`
   - Line 4: Change `**RQ Number:** 1` to `**RQ Number:** 2.1`
   - Line 5: Change `**Full ID:** 5.1` to `**Full ID:** 5.2.1`

2. **Update docs/4_analysis.yaml (RQ ID)**
   - Line 5: Change `# RQ: ch5/rq1` to `# RQ: ch5/5.2.1`
   - Line 11: Change `rq_id: "ch5/rq1"` to `rq_id: "ch5/5.2.1"`

3. **Update all code files (Use relative paths instead of hardcoded absolute paths)**
   - Files affected: step02_purify_items.py, step04_merge_theta_tsvr.py, step05_fit_lmm.py
   - Replace: `RQ_DIR = Path("/home/etai/projects/REMEMVR/results/ch5/rq1")`
   - With: `RQ_DIR = Path(__file__).resolve().parents[1]`
   - Also update inline comments: `# results/ch5/rq1` → `# results/ch5/5.2.1`

4. **Update all code file headers and docstrings**
   - Files: All 8 Python files in code/
   - Update: `RQ: results/ch5/rq1` → `RQ: results/ch5/5.2.1`
   - Update: `RQ: ch5/rq1` → `RQ: ch5/5.2.1`

5. **Update status.yaml (Historical record)**
   - Line 4: Change `Created results/ch5/rq1/` to `Created results/ch5/5.2.1/`
   - Add note: `migrated_from: "rq1"` (for git history tracking)

---

## Verification Checklist

After applying fixes, verify:

- [ ] `grep -r "rq1" /results/ch5/5.2.1/` returns ZERO matches (except in .gitkeep/comments about old numbering)
- [ ] `grep -r "ch5/rq1" /results/ch5/5.2.1/` returns ZERO matches
- [ ] `grep -r "5\.1[^.]" /results/ch5/5.2.1/docs/` returns ZERO matches (except "5.1." for hierarchical references if applicable)
- [ ] All RQ ID references use either "5.2.1" or "ch5/5.2.1" format consistently
- [ ] All code paths use relative path calculation via `Path(__file__).resolve().parents[1]` instead of hardcoded absolute paths
- [ ] `git diff` shows clean migration with no orphaned old references

---

## Impact on Downstream RQs

**Affected RQs (per rq_refactor.tsv):**
- 5.2.2 (Consolidation Window) - DERIVED from RQ 5.2.1 - Will reference via folder path `results/ch5/5.2.1/`
- 5.2.3 (Age × Domain Interactions) - DERIVED from RQ 5.2.1 - Will reference via folder path
- 5.2.4 (IRT-CTT Convergence) - DERIVED from RQ 5.2.1
- 5.2.5 (Purified CTT Effects) - DERIVED from RQ 5.2.1

**Risk:** If these downstream RQs are already generated, their input specifications will be broken (they'll try to read from `results/ch5/5.2.1/data/` but code says `results/ch5/rq1/data/`)

---

## Notes

- **All subfolder structure correct:** docs/, code/, data/, logs/, plots/, results/ all present and properly organized
- **File inventory complete:** 56 files across 6 subfolders, consistent with planned structure
- **Data files exist:** All referenced input files (step00_irt_input.csv, step00_q_matrix.csv, etc.) present with correct row counts
- **Analysis execution appears complete:** All 8 steps have log files, output files, and status=success in status.yaml
- **No missing dependencies:** Source data file `/data/cache/dfData.csv` exists and is readable
- **Only issue is naming/documentation:** The analysis itself executed correctly; the problem is that internal references use old RQ ID while folder uses new ID

---

**Audit Completed:** All 6 layers checked. 5 issues identified (2 CRITICAL, 2 HIGH, 1 MODERATE). No CRITICAL path corruption detected, but RQ identity inconsistency requires immediate correction before downstream RQs consume outputs.

