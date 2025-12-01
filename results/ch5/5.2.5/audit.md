# RQ 5.2.5 Audit Report

**Audit Date:** 2025-12-01
**Auditor:** rq_audit agent v1.0.0
**RQ Folder:** results/ch5/5.2.5
**Status:** 8 issues identified (5 CRITICAL, 2 HIGH, 1 MODERATE)

---

## CRITICAL ISSUES

### 1. Old RQ Numbering in Code Metadata
- **Location:** All 9 Python files in code/ folder (step00-step08)
- **Expected:** RQ ID should be `ch5/5.2.5` (hierarchical numbering matching folder name)
- **Actual:** All files reference `RQ: results/ch5/rq12` (old numeric naming)
- **Impact:** Code metadata contradicts folder structure, causing confusion about which RQ is executing. Cross-RQ dependencies reference wrong paths.
- **Severity:** CRITICAL (causes runtime path resolution errors when scripts calculate RQ_DIR relative to themselves)
- **Examples:**
  - `/home/etai/projects/REMEMVR/results/ch5/5.2.5/code/step00_load_data.py:8` - "RQ: results/ch5/rq12"
  - `/home/etai/projects/REMEMVR/results/ch5/5.2.5/code/step01_map_items.py:8` - "RQ: results/ch5/rq12"
  - All other stepNN_*.py files have same issue

### 2. Old RQ Numbering in Documentation Headers
- **Location:** Specification documents in docs/ folder
- **Expected:** Documentation headers should show `ch5/5.2.5` or `RQ 5.2.5` (hierarchical)
- **Actual:**
  - 1_concept.md line 1: "RQ 5.12" and "Full ID: 5.12"
  - 2_plan.md line 1: "RQ 5.12"
  - 4_analysis.yaml line 11: `rq_id: "ch5/rq12"`
- **Impact:** All documentation uses old naming system, contradicting folder structure (5.2.5)
- **Severity:** CRITICAL (misleading for users who check documentation)

### 3. Cross-RQ Dependency References Old Naming
- **Location:** 1_concept.md lines 97, 102, 177-186; 2_plan.md lines 52-78; 4_analysis.yaml lines 45-56
- **Expected:** All paths should reference `results/ch5/5.2.1/` (corresponding to old RQ 5.1 = new RQ 5.2.1)
- **Actual:** All references are to `results/ch5/rq1/` (non-existent path)
- **Impact:** CRITICAL - Code cannot execute because it tries to load files from non-existent folder
- **Examples:**
  - 1_concept.md line 97: "Load IRT item parameters and theta scores from results/ch5/rq1/"
  - 2_plan.md line 52: "File 1: results/ch5/rq1/data/step02_purified_items.csv"
  - 4_analysis.yaml line 45: "path: results/ch5/rq1/data/step02_purified_items.csv"
  - All step code files reference `results/ch5/rq1/` which doesn't exist
- **Verification:** `ls /home/etai/projects/REMEMVR/results/ch5/rq1/` returns "No such file or directory"
- **Correct Path:** `results/ch5/5.2.1/` exists and contains required files:
  - `/home/etai/projects/REMEMVR/results/ch5/5.2.1/data/step02_purified_items.csv` (exists, 3.9 KB)
  - `/home/etai/projects/REMEMVR/results/ch5/5.2.1/data/step03_theta_scores.csv` (exists, 16 KB)
  - `/home/etai/projects/REMEMVR/results/ch5/5.2.1/data/step00_tsvr_mapping.csv` (exists, 7.9 KB)

### 4. Status Document Inconsistent with New Numbering
- **Location:** status.yaml
- **Expected:** status.yaml should reference RQ by hierarchical numbering or new RQ path structure
- **Actual:** status.yaml shows completion of v3.0 agent workflow (rq_builder, rq_concept, rq_scholar, etc.)
- **Issue:** status.yaml was created with old v3.0 agents and shows "RQ: results/ch5/rq12" semantics
- **Impact:** CRITICAL - Workflow status unclear (appears to use old agent system)
- **Lines 1-12:** Shows rq_builder creating "results/ch5/rq12/" with old numbering

### 5. Mismatch: Data References Use Old Internal Numbering (rq12) Instead of New Folder (5.2.5)
- **Location:** Code files have hardcoded comments/docstrings mentioning "rq12"
- **Expected:** No internal references to "rq12", only to "5.2.5"
- **Actual:** Step code files document themselves as "RQ: results/ch5/rq12"
- **Impact:** CRITICAL for maintainability - when code is run, path resolution will fail because RQ_DIR calculated from file location will be "/results/ch5/5.2.5/" but code comments claim "/results/ch5/rq12/"
- **Example:** step00_load_data.py line 113:
  ```python
  RQ_DIR = Path(__file__).resolve().parents[1]  # results/ch5/rq12
  ```
  The comment is wrong. RQ_DIR will resolve to `/home/etai/projects/REMEMVR/results/ch5/5.2.5/` not `/results/ch5/rq12/`

---

## HIGH ISSUES

### 6. Dependencies Reference RQ via Old Naming Convention
- **Location:** 2_plan.md Step 0, lines 96-98; 4_analysis.yaml line 17
- **Expected:** Dependency statement should say "RQ 5.2.1" and check status via new path
- **Actual:**
  - 2_plan.md line 157-158: "Cross-RQ Dependency Check: ... results/ch5/rq1/status.yaml ..."
  - 4_analysis.yaml line 35: "Check RQ 5.1 completion: read results/ch5/rq1/status.yaml"
- **Issue:** Code will try to load `results/ch5/rq1/status.yaml` (doesn't exist) instead of `results/ch5/5.2.1/status.yaml`
- **Impact:** HIGH - Dependency validation will fail, blocking RQ execution
- **Correct Path:** `results/ch5/5.2.1/status.yaml` exists
- **Severity:** HIGH (prevents execution start)

### 7. Analysis Recipe Contains Incorrect Paths Throughout
- **Location:** 4_analysis.yaml, lines 44-56 (Step 0 input file paths)
- **Expected:** All paths in 4_analysis.yaml should use `results/ch5/5.2.1/` format
- **Actual:** Uses `results/ch5/rq1/` format (8 references across steps 0-7)
- **Impact:** HIGH - Step 0 data loading will fail immediately (FileNotFoundError)
- **Examples in 4_analysis.yaml:**
  - Line 45: "path: results/ch5/rq1/data/step02_purified_items.csv"
  - Line 49: "path: results/ch5/rq1/data/step03_theta_scores.csv"
  - Line 53: "path: results/ch5/rq1/data/step00_tsvr_mapping.csv"

---

## MODERATE ISSUES

### 8. Tool Catalog Reflects Old Path References
- **Location:** 3_tools.yaml, lines 24, 52, 56, 60
- **Expected:** Input file paths should reference correct RQ folder (5.2.1)
- **Actual:** Uses old notation `results/ch5/rq1/data/` (4 occurrences)
- **Impact:** MODERATE - When tools are invoked, they will have stale documentation
- **Note:** rq_tools (Step 11 agent) reads 2_plan.md and 3_tools.yaml. Since 3_tools.yaml is auto-generated from the plan, these stale references came from the plan's stale paths.

---

## Summary Table

| Severity | Count | Categories |
|----------|-------|-----------|
| CRITICAL | 5 | Path mismatch (rq12 vs 5.2.5, rq1 vs 5.2.1), dependency paths broken |
| HIGH | 2 | Dependency validation paths, analysis recipe paths |
| MODERATE | 1 | Tool catalog documentation |
| LOW | 0 | |
| **TOTAL** | **8** | Numbering consistency (RQ ID alignment) |

---

## Root Cause Analysis

**Primary Root Cause:** RQ folder naming migration from old system (rq1, rq12, etc.) to new hierarchical system (5.2.1, 5.2.5, etc.) was completed for FOLDERS but NOT for DOCUMENT/CODE CONTENT.

**Timeline:**
1. Old system: RQ folders named `results/ch5/rq1/`, `results/ch5/rq12/`, etc.
2. Migration decision: Implement hierarchical naming (5.2.1, 5.2.5, etc.)
3. Completed: Folder renaming (rq12 → 5.2.5, rq1 → 5.2.1)
4. NOT completed: Updating content in docs/ and code/ to reference new paths

**Why This Happened:**
- Content generation agents (rq_concept, rq_planner, rq_tools, rq_analysis) generated specifications and code using old naming system
- Generated files were never updated after folder migration
- The rq_refactor.tsv file shows mapping but wasn't used to update document/code content

**Why It's Critical:**
- Step 0 code attempts: `results/ch5/rq1/data/step02_purified_items.csv` → FileNotFoundError (folder doesn't exist)
- Dependency validation attempts: `results/ch5/rq1/status.yaml` → FileNotFoundError
- Code comments claim "RQ: results/ch5/rq12" but actual location is "results/ch5/5.2.5" → misleading for debugging

---

## Recommended Fixes

### Priority 1 (CRITICAL - Must Fix Before Execution)

1. **Update all cross-RQ paths in code files (step00-step08):**
   - Search: `results/ch5/rq1/`
   - Replace with: `results/ch5/5.2.1/`
   - Files: All 9 Python files in code/ folder
   - Approx: 8+ occurrences

2. **Update all cross-RQ paths in documentation:**
   - Update 1_concept.md: Replace `results/ch5/rq1/` with `results/ch5/5.2.1/` (4 occurrences, lines 97, 102, 180-182)
   - Update 2_plan.md: Replace `results/ch5/rq1/` with `results/ch5/5.2.1/` (18+ occurrences in Step 0)
   - Update 4_analysis.yaml: Replace `results/ch5/rq1/` with `results/ch5/5.2.1/` (3 file paths in steps 0)

3. **Update RQ numbering in document headers:**
   - Change 1_concept.md header from "RQ 5.12" → "RQ 5.2.5" (lines 1, 4, 5)
   - Change 2_plan.md header from "RQ 5.12" → "RQ 5.2.5" (line 1)
   - Change 4_analysis.yaml metadata from `rq_id: "ch5/rq12"` → `rq_id: "ch5/5.2.5"` (line 11)

4. **Update code metadata comments:**
   - Replace all "RQ: results/ch5/rq12" → "RQ: results/ch5/5.2.5" (9 occurrences, one per Python file)
   - Update RQ_DIR comments: "# results/ch5/rq12" → "# results/ch5/5.2.5" (9 occurrences)

5. **Update dependency references:**
   - Change "RQ 5.1" references to "RQ 5.2.1" for clarity (concept doc, plan doc)
   - Change "rq1" → "5.2.1" in all status.yaml path checks

### Priority 2 (HIGH - Before Using Documentation)

6. **Regenerate 3_tools.yaml:**
   - Since tool catalog is auto-generated from plan, regenerating it after fixing 2_plan.md will cascade corrections to tool paths
   - Or manually replace all `results/ch5/rq1/` → `results/ch5/5.2.1/` in 3_tools.yaml (4 occurrences, lines 24, 52, 56, 60)

### Priority 3 (MODERATE - Maintenance)

7. **Update status.yaml context dumps:**
   - Lines 3-8: Update rq_builder dump to reference new folder structure
   - This is mostly documentation but prevents confusion about workflow version

### Testing After Fixes

- [ ] Verify step00_load_data.py can load `results/ch5/5.2.1/data/step02_purified_items.csv`
- [ ] Verify step00 can load `results/ch5/5.2.1/status.yaml` for dependency check
- [ ] Grep all code/doc files for "rq1" and "rq12" - should find 0 results (except in audit.md)
- [ ] Run step00_load_data.py in isolation to confirm file loading works
- [ ] Run full analysis pipeline to confirm end-to-end execution

---

## Files Affected

**Code Files (9):**
- code/step00_load_data.py (RQ metadata + cross-RQ path)
- code/step01_map_items.py (RQ metadata)
- code/step02_compute_full_ctt.py (RQ metadata)
- code/step03_compute_purified_ctt.py (RQ metadata + path)
- code/step04_assess_reliability.py (RQ metadata + path)
- code/step05_correlation_analysis.py (RQ metadata + path)
- code/step06_standardize_outcomes.py (RQ metadata + path)
- code/step07_fit_parallel_lmms.py (RQ metadata + path)
- code/step08_prepare_plot_data.py (RQ metadata)

**Documentation Files (4):**
- docs/1_concept.md (RQ header, cross-RQ dependencies)
- docs/2_plan.md (RQ header, Step 0 input paths)
- docs/3_tools.yaml (input file paths)
- docs/4_analysis.yaml (RQ ID, Step 0 input paths, dependency checks)

**Other Files (1):**
- status.yaml (context dumps reference old naming)

---

## Audit Completion Notes

**Validation Performed:**
- Layer 1 (Path References): FAILED - 8 broken references to rq1, rq12
- Layer 2 (Numbering Consistency): FAILED - RQ ID mismatch (headers show 5.12, folder is 5.2.5)
- Layer 3 (Data Sources): FAILED - Cross-RQ dependency paths don't exist
- Layer 4 (Documentation Consistency): PARTIAL - Inconsistency between folder name and document headers
- Layer 5 (Step Completeness): PASS - All 9 steps present and documented
- Layer 6 (Naming Conventions): PASS - Step naming follows project standards (stepNN_description.py)

**Execution Blockers:** 2 CRITICAL
- RQ will fail at Step 0 when attempting to load from `results/ch5/rq1/` (folder doesn't exist)
- Dependency validation will fail when checking `results/ch5/rq1/status.yaml`

**Likelihood of Success Without Fixes:** 0% (Step 0 fails immediately due to FileNotFoundError)

---

**End of Audit Report**
