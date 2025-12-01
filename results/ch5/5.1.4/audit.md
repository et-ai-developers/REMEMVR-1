# RQ 5.1.4 Audit Report

**Audit Date:** 2025-12-01
**Auditor:** rq_audit agent v1.0.0
**RQ ID:** 5.1.4 (formerly RQ 5.13)
**Status:** 8 issues identified (1 CRITICAL, 2 HIGH, 4 MODERATE, 1 LOW)

---

## CRITICAL ISSUES

### 1. Incorrect Path References to Parent RQ (Old Numbering)
- **Location:** code/step01_load_rq57_dependencies.py, code/step02_extract_variance_components.py, code/step04_extract_random_effects.py (lines 107-109, 172, and similar)
- **Expected:** Path references should use new RQ numbering (5.1.1) instead of old numbering (rq7)
- **Actual:** Code references `../rq7/data/lmm_Lin+Log.pkl` and similar paths. The folder `../rq7` does not exist. Correct path is `../5.1.1/data/lmm_Lin+Log.pkl`
- **Impact:** CRITICAL - When steps execute, circuit breaker validation will fail with "EXPECTATIONS ERROR: RQ 5.7 dependencies missing" even though RQ 5.1.1 (the correct parent) exists. Step 1 will immediately exit with code 1, blocking all downstream analysis.
- **Root Cause:** Code was generated when the RQ folder naming still used old numbering (rq1-rq15). The new hierarchical numbering (5.X.Y) replaced the old system, but code generation did not update relative paths.
- **Evidence:**
  - File exists at: `/home/etai/projects/REMEMVR/results/ch5/5.1.1/data/lmm_Lin+Log.pkl` (563 KB)
  - File NOT at: `/home/etai/projects/REMEMVR/results/ch5/5.1.4/../rq7/data/` (path does not resolve)
  - Code line 107: `RQ57_LMM_MODEL = RQ_DIR / "../rq7/data/lmm_Lin+Log.pkl"`

---

## HIGH ISSUES

### 1. RQ ID Inconsistency Between Folder and Documentation
- **Location:** Folder name `5.1.4` vs documentation stating RQ 5.13
- **Expected:** All RQ identification should use new numbering system consistently: 5.1.4 (not 5.13)
- **Actual:** status.yaml and code docstrings reference old RQ number "5.13" or "results/ch5/rq13":
  - step01_load_rq57_dependencies.py line 8: `RQ: results/ch5/rq13`
  - step02_extract_variance_components.py line 8: `RQ: results/ch5/rq13`
  - All 5 code files have this issue
  - 1_concept.md header correctly says "5.13" but should say "5.1.4"
- **Impact:** HIGH - Creates confusion about RQ identity. Master scripts or downstream processes relying on new numbering will not find this RQ if they search for "5.1.4" in code. Causes mismatch between folder structure and code documentation.
- **Root Cause:** Documents and docstrings were generated before the numbering migration was complete. Subsequent updates to folder names did not update code docstrings.

### 2. Missing Data Output File (step05_intercept_slope_correlation.csv Location Ambiguity)
- **Location:** 2_plan.md and 4_analysis.yaml specify conflicting output locations
- **Expected:** Output should be in `data/` folder with step prefix (standard convention)
- **Actual:**
  - 2_plan.md lines 595-605 specifies: `results/step05_intercept_slope_correlation.csv`
  - 4_analysis.yaml line 388 specifies: `data/step05_intercept_slope_correlation.csv`
  - Code (step05_test_correlation.py line 218) writes to: `RQ_DIR / "data" / "step05_intercept_slope_correlation.csv"`
- **Impact:** HIGH - Folder convention violation. CSV output data should be in `data/` folder, not `results/`. The `results/` folder is reserved for summary reports (.md, .txt, .html). This violates the project's MANDATORY folder convention documented in every code file's header comments (lines 94-125 of step*.py files).
- **Evidence:** All code files contain identical comment block stating "data/ : ALL data outputs (.csv, .pkl, .txt)"

---

## MODERATE ISSUES

### 1. Documentation Inconsistency: Model File Name References
- **Location:** 1_concept.md line 150, 2_plan.md lines 45-46, 4_analysis.yaml lines 44-46
- **Expected:** File name should match actual saved model file: either `lmm_Lin+Log.pkl` (preferred) or `lmm_Log.pkl` (fallback)
- **Actual:**
  - 1_concept.md line 150: References `results/ch5/rq7/data/step05_lmm_all_bestmodel.pkl` (does not exist)
  - 2_plan.md line 45: References `results/ch5/rq7/data/lmm_Log.pkl` (exists but outdated naming)
  - 4_analysis.yaml line 44: References `../rq7/data/lmm_Log.pkl` (relative path to non-existent folder)
  - Code actually uses: `lmm_Lin+Log.pkl` (preferred, better convergence)
- **Impact:** MODERATE - Documentation and code disagree on which model file to load. While code successfully loads the correct file (`lmm_Lin+Log.pkl`), readers of documentation will be confused about which file is actually used. Creates maintenance risk for future updates.
- **Evidence:** step01_load_rq57_dependencies.py line 107 loads `lmm_Lin+Log.pkl`; code comments line 106 explain "CHANGED: Using Lin+Log model instead of Log"

### 2. Cross-RQ Dependency Documentation Mismatch
- **Location:** 1_concept.md lines 95-98 vs 2_plan.md lines 44-46 vs 4_analysis.yaml lines 44-46
- **Expected:** All references to RQ 5.7 (now RQ 5.1.1) dependency files should use consistent path format
- **Actual:** Three different path references across documents:
  - 1_concept.md: Uses "results/ch5/rq7/" (old numbering)
  - 2_plan.md: Uses "results/ch5/rq7/" (old numbering) AND "step05_lmm_all_bestmodel.pkl" (non-existent file)
  - 4_analysis.yaml: Uses "../rq7/" (old numbering, relative path) AND "lmm_Log.pkl" (exists but not preferred model)
- **Impact:** MODERATE - Different documents give different information about where files are located. This creates ambiguity for someone reading docs without examining code. Complicates understanding of RQ structure.

### 3. Folder Convention Violation in Multiple Output Paths
- **Location:** 2_plan.md specifications for results/step03_icc_summary.txt, results/step04_random_slopes_descriptives.txt, results/step05_correlation_interpretation.txt
- **Expected:** .txt files with step prefix could go in either `results/` (summary reports) or `data/` (processed data), but convention should be consistent
- **Actual:** Code correctly places these in `results/` folder (step03_compute_icc.py line 278, step04_extract_random_effects.py line 344, step05_test_correlation.py line 232), which is appropriate for summary/interpretation documents
- **Impact:** MODERATE - Minor violation is actually handled correctly by code. However, 2_plan.md refers to `step03_icc_summary.txt` location inconsistently with other summary files. Not a critical issue since code does the right thing, but creates documentation confusion.

### 4. Missing Specification for step05_intercept_slope_correlation.csv Format
- **Location:** 2_plan.md lines 595-605 vs 4_analysis.yaml lines 388-394
- **Expected:** Documentation should specify whether this is "wide" (1 row, many columns) or "long" (multiple rows, 2 columns) format
- **Actual:**
  - 2_plan.md implies wide format (5 rows for 5 statistics) but location says `results/`
  - 4_analysis.yaml specifies columns: statistic, value (long format with 5 rows)
  - Code (step05_test_correlation.py lines 219-227) actually writes wide format (1 row, 7 columns): r, p_uncorrected, p_bonferroni, df, alpha_corrected, significant_uncorrected, significant_bonferroni
- **Impact:** MODERATE - Format mismatch between specification and implementation. The validation tool (validate_correlation_test_d068) expects a specific format, and current code output (1 row × 7 columns wide format) is correct per D068 requirements, but documentation in 2_plan.md and 4_analysis.yaml suggests different format (5 rows × 2 columns).

---

## LOW ISSUES

### 1. Docstring RQ Path Uses Old Convention
- **Location:** All 5 code files (step01-step05) have docstring line ~8 saying `RQ: results/ch5/rq13`
- **Expected:** Should say `RQ: results/ch5/5.1.4` to match new folder naming
- **Actual:** All code files reference `results/ch5/rq13` in metadata docstring
- **Impact:** LOW - Docstrings are read-only comments that don't affect execution. But they mislead developers about RQ identity. Future code maintainers might search for "rq13" and not find it in the folder structure.

---

## Summary Table

| Severity | Count | Category |
|----------|-------|----------|
| CRITICAL | 1 | Path References (old RQ numbering) |
| HIGH | 2 | Numbering Consistency, Folder Convention |
| MODERATE | 4 | Documentation Inconsistency, Dependency Specs, Format Mismatch |
| LOW | 1 | Docstring Convention |
| **TOTAL** | **8** | |

---

## Root Cause Analysis

**Primary Root Cause:** Numbering System Migration (Old rq1-rq15 → New 5.X.Y)

The RQ folder structure was refactored from old numbering (rq1, rq2, ..., rq15) to hierarchical numbering (5.1.1, 5.1.2, ..., 5.3.X). This migration was **partially incomplete**:

1. **Folder names updated:** Results folder renamed from `rq13/` to `5.1.4/` ✓
2. **Specification documents updated:** 1_concept.md headers changed to "5.1.4" ✓
3. **Code generated with OLD paths:** Code generation (via g_code agent) hardcoded paths using old numbering (`../rq7/data/`) ✗
4. **Docstrings not updated:** Code docstrings still reference old RQ numbers ✗

**Secondary Root Causes:**
- Model file naming changed (lmm_Log.pkl → lmm_Lin+Log.pkl) but documentation not fully updated
- Folder convention rules (data/ vs results/) not strictly enforced during documentation creation
- No validation that generated code paths match actual folder structure

---

## Recommended Fixes

### CRITICAL (Must fix before execution)

1. **Update all code path references to new RQ numbering (5.1.1):**
   ```
   BEFORE: RQ57_LMM_MODEL = RQ_DIR / "../rq7/data/lmm_Lin+Log.pkl"
   AFTER:  RQ57_LMM_MODEL = RQ_DIR / "../5.1.1/data/lmm_Lin+Log.pkl"
   ```
   - Files: code/step01_load_rq57_dependencies.py (lines 107-109)
   - Files: code/step02_extract_variance_components.py (line 156)
   - Files: code/step04_extract_random_effects.py (line 172)
   - This is THE critical fix that must be done first

### HIGH (Fix before next documentation update)

2. **Update all RQ ID references from 5.13 to 5.1.4:**
   - code/step01_load_rq57_dependencies.py line 8: Change docstring to `RQ: results/ch5/5.1.4`
   - Repeat for step02, step03, step04, step05 code files
   - Rationale: Consistency with folder naming and future searchability

3. **Clarify data output location for step05_intercept_slope_correlation.csv:**
   - Confirm intended location: `data/` folder (current code correct) or `results/` folder (documentation says)
   - If `data/` (recommended): Update 2_plan.md lines 595-605 to say "data/step05_intercept_slope_correlation.csv"
   - If `results/`: Move output in code step05_test_correlation.py line 218
   - Recommendation: Keep in `data/` (it's a CSV data file, not a summary report)

### MODERATE (Fix during next documentation refresh)

4. **Update dependency path references to use new numbering consistently:**
   - 1_concept.md line 150: Change "results/ch5/rq7/" to "results/ch5/5.1.1/"
   - 2_plan.md lines 44-46: Change "results/ch5/rq7/" to "results/ch5/5.1.1/"
   - 4_analysis.yaml lines 44-46: Change "../rq7/" to "../5.1.1/"

5. **Standardize model file references:**
   - Update 1_concept.md to reference "step05_lmm_Lin+Log.pkl" (not step05_lmm_all_bestmodel.pkl)
   - Update 2_plan.md to reference "lmm_Lin+Log.pkl" (not lmm_Log.pkl)
   - Add comment: "Lin+Log model selected for superior convergence (ΔAIC=0.8 vs Log)"

6. **Fix step05 output format documentation:**
   - 4_analysis.yaml lines 388-394: Clarify that output is 1 row × 7 columns (wide format)
   - Add columns list: r, p_uncorrected, p_bonferroni, df, alpha_corrected, significant_uncorrected, significant_bonferroni

---

## Step Completeness Status

All 5 analysis steps present and marked as `success` in status.yaml:

| Step | Name | Status | Output Files | Issue |
|------|------|--------|--------------|-------|
| 01 | Load RQ 5.1.1 Dependencies | success | step01_model_metadata.yaml | Path reference uses old numbering (CRITICAL) |
| 02 | Extract Variance Components | success | step02_variance_components.csv | Path reference uses old numbering (CRITICAL) |
| 03 | Compute ICC | success | step03_icc_estimates.csv | None |
| 04 | Extract Random Effects | success | step04_random_effects.csv | Path reference uses old numbering (CRITICAL) |
| 05 | Test Correlation | success | step05_*.csv, plots | Output folder convention issue (HIGH) |

All output files present and correctly named (with step prefix).

---

## Validation Tools Coverage

Per audit checklist, all 5 analysis steps have validation tools specified:

- Step 01: validate_model_convergence ✓
- Step 02: validate_variance_positivity ✓
- Step 03: validate_icc_bounds ✓
- Step 04: validate_data_columns ✓
- Step 05: validate_correlation_test_d068 ✓

Status: All validation coverage complete.

---

## Files Checked During Audit

**Specification Documents (6 files):**
- docs/1_concept.md (172 lines)
- docs/1_scholar.md
- docs/1_stats.md
- docs/2_plan.md (840 lines)
- docs/3_tools.yaml (299 lines)
- docs/4_analysis.yaml (465 lines)
- status.yaml

**Code Files (5 files):**
- code/step01_load_rq57_dependencies.py (532 lines)
- code/step02_extract_variance_components.py (336 lines)
- code/step03_compute_icc.py (319 lines)
- code/step04_extract_random_effects.py (425 lines)
- code/step05_test_correlation.py (373 lines)

**Output Files (13 files):**
- data/: step01_model_metadata.yaml, step02_variance_components.csv, step03_icc_estimates.csv, step04_random_effects.csv, step05_intercept_slope_correlation.csv (5 files)
- results/: step03_icc_summary.txt, step04_random_slopes_descriptives.txt, step05_correlation_interpretation.txt, summary.md (4 files)
- plots/: step05_random_slopes_histogram.png, step05_random_slopes_qqplot.png (2 plots)
- logs/: 5 log files (complete)

---

## Audit Conclusion

**Overall Status:** Issues identified but not blocking execution

**Critical Issue:** Path references use old RQ numbering (rq7 instead of 5.1.1). This WILL cause Step 1 to fail with circuit breaker error "EXPECTATIONS ERROR" during next execution. **Requires immediate fix before running RQ.**

**Action Required:**
1. Fix path references in 3 code files (step01, step02, step04) to use `../5.1.1/` instead of `../rq7/`
2. Update RQ ID references from 5.13 to 5.1.4 in all code docstrings
3. Clarify output folder conventions in documentation

**Execution Risk:** HIGH without critical fix. Code will fail at Step 1 circuit breaker validation.

---

**Audit completed by rq_audit agent v1.0.0**
**Date: 2025-12-01**
