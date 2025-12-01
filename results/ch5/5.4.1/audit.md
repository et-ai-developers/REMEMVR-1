# RQ 5.4.1 Audit Report

**Audit Date:** 2025-12-01
**Auditor:** rq_audit agent v1.0.0
**RQ Path:** results/ch5/5.4.1
**Status:** CRITICAL ISSUES DETECTED - 3 critical issues, 0 high, 1 moderate

---

## CRITICAL ISSUES

### 1. RQ ID Mismatch - Folder Name vs. Concept Document Header

- **Location:** Folder name vs. 1_concept.md (line 1)
- **Expected:** RQ folder name (5.4.1) should match RQ ID in documentation
- **Actual:** Folder named 5.4.1, but 1_concept.md header is "RQ 5.5: Do Congruent and Incongruent Items Show Different Forgetting Rates?"
- **Impact:** CRITICAL - Code and documentation refer to different RQ IDs (RQ 5.4.1 vs RQ 5.5). This causes confusion about which research question this folder actually implements. All downstream references and cross-RQ dependencies become ambiguous.
- **Evidence:**
  - Folder: `/home/etai/projects/REMEMVR/results/ch5/5.4.1`
  - Document header line 1: "# RQ 5.5: Do Congruent and Incongruent Items Show Different Forgetting Rates?"
  - status.yaml context_dump (lines 16-25): "RQ 5.5: Schema congruence effects on forgetting trajectories"
  - 4_analysis.yaml metadata (line 11): `rq_full: "5.5"`

### 2. Cross-RQ Dependency Path Reference - Wrong Folder Name Format

- **Location:** step00_extract_congruence_data.py (lines 85-87), 1_concept.md (lines 103, 105, 172-173), 2_plan.md (lines 40-42)
- **Expected:** `results/ch5/5.1.1/data/step00_irt_input.csv` (new hierarchical naming) or verify that `results/ch5/rq1/` exists
- **Actual:** Code/docs reference `results/ch5/rq1/data/step00_irt_input.csv` (old naming) which does NOT exist on filesystem. RQ 5.1 folder is now named 5.1.1, not rq1.
- **Impact:** CRITICAL - Step 00 will fail at runtime when step00_extract_congruence_data.py tries to load cross-RQ dependencies. FileNotFoundError will be raised because rq1 folder doesn't exist.
  ```
  FileNotFoundError: RQ 5.1 IRT input not found: results/ch5/rq1/data/step00_irt_input.csv
  ```
- **Evidence:**
  - step00_extract_congruence_data.py lines 85-87:
    ```python
    RQ1_DIR = PROJECT_ROOT / "results" / "ch5" / "rq1"
    RQ1_IRT_INPUT = RQ1_DIR / "data" / "step00_irt_input.csv"
    RQ1_TSVR_MAPPING = RQ1_DIR / "data" / "step00_tsvr_mapping.csv"
    ```
  - Actual filesystem:
    - `/home/etai/projects/REMEMVR/results/ch5/5.1.1/` exists (new naming)
    - `/home/etai/projects/REMEMVR/results/ch5/rq1/` does NOT exist (old naming removed)
  - 1_concept.md lines 172-173 reference same wrong path
  - 2_plan.md lines 40-42 reference same wrong path

### 3. Cross-RQ Dependency Files Missing - Data Source Does Not Exist

- **Location:** Dependency specification in 1_concept.md (lines 169-176), 2_plan.md (lines 36-58), code step00_extract_congruence_data.py (lines 85-87)
- **Expected:** Source RQ 5.1 (now 5.1.1) should have completed step00 extraction, producing:
  - `results/ch5/5.1.1/data/step00_irt_input.csv`
  - `results/ch5/5.1.1/data/step00_tsvr_mapping.csv`
- **Actual:** RQ 5.1.1 data folder contains different files (step01_theta_scores.csv, step02_purified_items.csv, step03_theta_scores.csv, step04_lmm_input.csv, lmm_*.pkl files) which are outputs from LATER steps, not Step 00 input files. Step00 output files don't exist in RQ 5.1.1.
- **Impact:** CRITICAL - Even if path is corrected, Step 00 execution will fail with FileNotFoundError because the actual source data files don't exist in RQ 5.1.1. The data present in RQ 5.1.1 is from later steps (likely a different RQ or incomplete RQ 5.1.1 run).
- **Evidence:**
  - RQ 5.1.1 data folder only contains: lmm_*.pkl, step01_theta_scores.csv, step02_purified_items.csv, step03_theta_scores.csv, step04_lmm_input.csv
  - Missing: step00_irt_input.csv, step00_tsvr_mapping.csv, step00_q_matrix.csv
  - These are the REQUIRED inputs specified in 2_plan.md Step 00 input section

---

## HIGH ISSUES

(None identified)

---

## MODERATE ISSUES

### 1. Naming Convention - Code Comments Reference Old RQ ID Format

- **Location:** step00_extract_congruence_data.py (lines 8, 56, 57)
- **Expected:** Code should reference RQ by current hierarchical number (RQ 5.5 or RQ results/ch5/5.4.1)
- **Actual:** Code docstring references "results/ch5/rq5" (old naming format, mixed with folder name 5.4.1)
  - Line 8: `RQ: results/ch5/rq5 (RQ 5.5: Schema Congruence Effects on Forgetting Trajectories)`
  - Line 56: `path: "results/ch5/rq1/data/step00_irt_input.csv"`
  - Line 57: `path: "results/ch5/rq1/data/step00_tsvr_mapping.csv"`
- **Impact:** MODERATE - Code will still execute (paths are resolved correctly relative to PROJECT_ROOT), but comments are inconsistent with actual folder structure (5.4.1 not rq5). Could confuse future maintainers about actual RQ location.
- **Evidence:**
  - Code docstring consistently uses old "rqN" naming alongside new hierarchical naming
  - Folder structure uses new 5.X.X naming convention
  - Internal path construction uses PROJECT_ROOT correctly but documentation is misleading

---

## LOW ISSUES

(None identified)

---

## Summary Table

| Severity | Count | Categories |
|----------|-------|-----------|
| CRITICAL | 3 | RQ ID mismatch (5.4.1 vs 5.5), Cross-RQ path naming (rq1 doesn't exist), Missing source data files |
| HIGH | 0 | |
| MODERATE | 1 | Code comments reference old RQ format |
| LOW | 0 | |
| **TOTAL** | **4** | |

---

## Root Cause Analysis

### Primary Issue: RQ Folder Numbering Mismatch (CRITICAL)

**Root Cause:** This RQ folder was created with hierarchical naming 5.4.1 but implements RQ 5.5 (Schema Congruence Effects on Forgetting Trajectories). The naming is inconsistent across the hierarchy level.

**Evidence Chain:**
1. Folder structure shows: `results/ch5/5.4.1/` ← This implies RQ 5.4.1
2. But 1_concept.md line 1: "# RQ 5.5: ..." ← This is RQ 5.5
3. status.yaml rq_concept: "RQ 5.5: Schema congruence effects..." ← Confirms RQ 5.5
4. 4_analysis.yaml metadata rq_full: "5.5" ← Confirms RQ 5.5

**Conclusion:** The folder should be named `5.5.1` or `5.5.0` (depending on versioning scheme), NOT `5.4.1`. The content is RQ 5.5.

### Secondary Issue: Cross-RQ Path Migration (CRITICAL)

**Root Cause:** During RQ folder restructuring from old naming (rqN) to new hierarchical naming (5.X.X), paths in this RQ were not updated:
- Old name: `results/ch5/rq1/`
- New name: `results/ch5/5.1.1/` (or similar)
- This RQ still references old names in code and documentation

**Impact:** Step 00 execution will immediately fail because:
1. Path is wrong: points to `ch5/rq1/` which doesn't exist
2. Even if path corrected to `ch5/5.1.1/`, the data files don't exist there

### Tertiary Issue: Missing Source Data (CRITICAL)

**Root Cause:** RQ 5.1.1 data folder doesn't contain step00_irt_input.csv and step00_tsvr_mapping.csv. The files present (step01_*, step03_*, step04_*, etc.) suggest either:
1. RQ 5.1.1 is incomplete (step00 was deleted or never run)
2. Different data was copied into RQ 5.1.1 from another source
3. RQ 5.1.1 is actually a different analysis than expected

**Impact:** This RQ 5.4.1 cannot execute Step 00 until RQ 5.1.1 has been completed and verified to have step00_irt_input.csv and step00_tsvr_mapping.csv.

---

## Recommended Fixes

### Fix 1 (CRITICAL - Must Complete First)

**Action:** Verify RQ numbering and rename folder if necessary.

**Steps:**
1. Confirm with project lead: Should this RQ be numbered 5.4.1 or 5.5.X?
2. If RQ 5.5, rename folder: `mv results/ch5/5.4.1 results/ch5/5.5.0` (or appropriate version)
3. If RQ 5.4.1, update all documentation (1_concept.md, 2_plan.md, status.yaml, 4_analysis.yaml) to refer to 5.4.1 instead of 5.5
4. Update all code comments to match actual folder name

**Rationale:** All downstream work depends on correct RQ identification.

### Fix 2 (CRITICAL - Prerequisite)

**Action:** Complete RQ 5.1.1 execution to generate required step00 files OR identify alternate source for RQ 5.1 data.

**Steps:**
1. Check if RQ 5.1.1 folder should have step00_irt_input.csv and step00_tsvr_mapping.csv
2. If yes: Run RQ 5.1.1 step00 to generate these files
3. If no: Identify which RQ has the actual VR item extraction data and update this RQ's dependency references
4. Verify both files exist and have correct structure before proceeding

**Rationale:** This RQ's entire analysis depends on RQ 5.1 data. Without verified source data, analysis cannot proceed.

### Fix 3 (CRITICAL - Path Update)

**Action:** Update all path references from old naming to new naming.

**Files to Update:**
1. `step00_extract_congruence_data.py` (lines 85-87): Change `ch5/rq1` to `ch5/5.1.1`
2. `1_concept.md` (lines 103, 105, 172-173): Update cross-RQ references from `rq1` to `5.1.1`
3. `2_plan.md` (lines 40-42, 55-56): Update cross-RQ references from `rq1` to `5.1.1`
4. `4_analysis.yaml` (lines 19-23): Update cross_rq_dependencies paths from `rq1` to `5.1.1`

**Pattern to Replace:**
- Replace: `results/ch5/rq1/`
- With: `results/ch5/5.1.1/`

**Rationale:** Consistent path naming enables code execution without errors.

### Fix 4 (MODERATE - Cleanup)

**Action:** Update code comments to use consistent RQ naming format.

**Files to Update:**
1. `step00_extract_congruence_data.py` (lines 8, 18, 56-57): Standardize RQ references

**Pattern:**
- Current: Mix of `results/ch5/rq5`, `results/ch5/rq1`, folder name `5.4.1`
- Target: Use consistent format throughout (e.g., "results/ch5/5.4.1" or "results/ch5/5.5.0" depending on Fix 1 decision)

**Rationale:** Code clarity for maintenance.

---

## Audit Methodology

This audit performed 6-layer integrity validation per rq_audit agent specification:

1. **Path References:** Checked all file paths in code and documentation. Found references to non-existent RQ 5.1 folder (rq1).

2. **Numbering Consistency:** Compared folder name (5.4.1) against RQ IDs in documentation (5.5). Found critical mismatch.

3. **Data Sources:** Verified cross-RQ dependencies exist. Found that RQ 5.1.1 is missing required step00 output files.

4. **Documentation Consistency:** Checked specifications for contradictions. Found consistent references to RQ 5.5 across all docs, but folder is named 5.4.1.

5. **Step Completeness:** Verified status.yaml step entries. Found all 8 steps marked success (step00-step07), with supporting data files present. However, step00 input data is missing from source RQ.

6. **Naming Conventions:** Checked file and folder naming standards. Found code comments use old rqN format while folder uses new 5.X.X format.

---

## Files Audit Summary

### Core Documentation (4 files - all readable)
- ✓ 1_concept.md - RQ concept and hypothesis (readable, RQ ID = 5.5)
- ✓ 1_stats.md - Statistical validation report (readable)
- ✓ 1_scholar.md - Literature validation (readable)
- ✓ 2_plan.md - Analysis plan (readable, references RQ 5.1 which doesn't exist)

### Specification Files (2 files - all readable)
- ✓ 3_tools.yaml - Tool catalog (readable, 8 analysis + 4 validation tools)
- ✓ 4_analysis.yaml - Analysis recipe (readable, 8 steps specified)

### Code Files (8 files - all readable)
- ✓ step00_extract_congruence_data.py - Data preparation (readable, references rq1 path)
- ✓ step01_irt_calibration_pass1.py - IRT Pass 1 (partial read, appears intact)
- ✓ step02_purify_items.py - Item filtering (file exists)
- ✓ step03_irt_calibration_pass2.py - IRT Pass 2 (file exists)
- ✓ step04_merge_theta_tsvr.py - Data merge (file exists)
- ✓ step05_fit_lmm.py - LMM fitting (file exists)
- ✓ step06_compute_post_hoc_contrasts.py - Post-hoc contrasts (file exists)
- ✓ step07_prepare_trajectory_plot_data.py - Plot data prep (file exists)

### Data Files (15 files - all present)
- ✓ step00_irt_input.csv (117 KB) - Input data
- ✓ step00_q_matrix.csv (1.4 KB) - Q-matrix
- ✓ step00_tsvr_mapping.csv (7.8 KB) - Time mapping
- ✓ step02_purified_items.csv (4.9 KB) - Purified items
- ✓ step02_removed_items.csv (1.8 KB) - Removed items
- ✓ step03_item_parameters.csv (2.6 KB) - Item parameters
- ✓ step03_theta_scores.csv (40 KB) - Theta scores
- ✓ step04_lmm_input.csv (105 KB) - LMM input
- ✓ step05_lmm_*.pkl (5 files, 420-668 KB) - Fitted models
- Note: Files are present and sizeable, suggesting analysis has been run

### Results Files (6 files - all present)
- ✓ step05_model_comparison.csv - Model comparison
- ✓ step05_lmm_model_summary.txt - Model summary
- ✓ step06_post_hoc_contrasts.csv - Contrasts
- ✓ step06_effect_sizes.csv - Effect sizes
- ✓ summary.md - Results summary
- ✓ summary_new.md - Alternative summary

### Log Files (10 files - all present)
- ✓ step00_extract_congruence_data.log - Step 00 log
- ✓ step01_irt_calibration_pass1.log - Step 01 log
- ✓ step02_purify_items.log - Step 02 log
- ✓ step03_irt_calibration_pass2.log - Step 03 log
- ✓ step04_merge_theta_tsvr.log - Step 04 log
- ✓ step05_fit_lmm.log - Step 05 log
- ✓ step06_compute_post_hoc_contrasts.log - Step 06 log
- ✓ step07_prepare_trajectory_plot_data.log - Step 07 log
- ✓ step01_pass1_item_params.csv (stored as log reference)
- ✓ step01_pass1_theta.csv (stored as log reference)

### Plot Files (4 files - all present)
- ✓ trajectory_theta.png - Theta scale plot
- ✓ trajectory_probability.png - Probability scale plot
- ✓ step07_trajectory_theta_data.csv - Plot source data
- ✓ step07_trajectory_probability_data.csv - Plot source data

### Status File
- ✓ status.yaml - All agents report success (rq_builder, rq_concept, rq_scholar, rq_stats, rq_planner, rq_tools, rq_analysis, rq_inspect, rq_plots, rq_results)

---

## Folder Structure Verification

**Required Folders:** All present
- ✓ code/ (8 Python scripts)
- ✓ data/ (15 data files)
- ✓ docs/ (4 markdown/YAML files)
- ✓ logs/ (10 log/reference files)
- ✓ plots/ (4 plot files)
- ✓ results/ (6 results files)

**Folder Status:** Complete and functional (all expected subfolders present)

---

## Conclusion

This RQ folder has **CRITICAL issues that will prevent successful re-execution or validation** if steps are re-run from the beginning. The analysis appears to have completed (all steps marked success, all output files present), but the underlying data dependencies are not correctly configured.

**Blocking Issues:**
1. Folder is named 5.4.1 but implements RQ 5.5 (RQ ID ambiguity)
2. Code references rq1 folder which doesn't exist (path errors)
3. RQ 5.1.1 is missing required step00 output files (data missing)

**Audit Verdict:** CANNOT PASS without fixes to Issues #1, #2, and #3 above.

**Risk Level:** HIGH - If anyone re-runs this RQ from step00, all steps will fail due to missing source data and broken paths.

---

**Audit Completed:** 2025-12-01 by rq_audit agent v1.0.0
