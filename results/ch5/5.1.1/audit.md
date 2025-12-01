# RQ 5.1.1 Audit Report

**Audit Date:** 2025-12-01
**Auditor:** rq_audit agent v1.0.0
**RQ Folder:** results/ch5/5.1.1
**Status:** 6 issues identified (2 CRITICAL, 3 HIGH, 1 MODERATE)

---

## Executive Summary

RQ 5.1.1 folder was successfully migrated from old hierarchical numbering (rq7) to new numbering (5.1.1), but **cross-RQ dependency paths were not updated during migration**. This creates CRITICAL blocking issues for code execution:

1. **IRT input data path broken** - all steps referencing RQ 5.2.1 data use old path (results/ch5/rq1/)
2. **TSVR data filename changed** - documentation references step00a_tsvr_data.csv but actual file is step00_tsvr_mapping.csv
3. **RQ identity inconsistent** - documentation still labeled as RQ 5.7 instead of 5.1.1

Fixes are straightforward (path/filename corrections) but MUST be completed before execution.

---

## CRITICAL ISSUES

### 1. Cross-RQ IRT Input Data Path - Wrong Directory Reference

**Location:**
- docs/4_analysis.yaml (lines 36-37, 259)
- docs/2_plan.md (lines 42, 104, 161, 205, 258)
- code/step01_irt_calibration_omnibus.py (docstring line 18)
- code/step03_irt_calibration_pass2.py (docstring)

**Expected Path:** `results/ch5/5.2.1/data/step00_irt_input.csv`

**Actual Path in Code/Docs:** `results/ch5/rq1/data/step00_irt_input.csv`

**Impact:** CRITICAL - Code execution will fail
- Step 1 (IRT calibration Pass 1) attempts to load from non-existent path: results/ch5/rq1/data/
- Throws FileNotFoundError immediately, blocks all downstream steps
- File EXISTS at correct location (results/ch5/5.2.1/data/step00_irt_input.csv verified)

**Root Cause:** Folder migration (rq1 → 5.2.1) was not reflected in RQ 5.1.1 path references. Old numbering "rq1" hardcoded throughout.

**Verification:**
```
ls -la /home/etai/projects/REMEMVR/results/ch5/rq1/data/step00_irt_input.csv
  → File not found (rq1 directory doesn't exist)

ls -la /home/etai/projects/REMEMVR/results/ch5/5.2.1/data/step00_irt_input.csv
  → File exists (172,139 bytes, verified 2025-11-30)
```

---

### 2. Cross-RQ TSVR Data File - Filename Mismatch

**Location:**
- docs/4_analysis.yaml (lines 313, 389)
- docs/2_plan.md (lines 24, 313, 804)
- code/step04_prepare_lmm_input.py (docstring line 24)

**Expected Filename:** `step00a_tsvr_data.csv`

**Actual Filename:** `step00_tsvr_mapping.csv`

**Expected Path:** `results/ch5/rq1/data/step00a_tsvr_data.csv`

**Actual Path & File:** `results/ch5/5.2.1/data/step00_tsvr_mapping.csv`

**Impact:** CRITICAL - Code execution will fail at Step 4
- Step 4 (Prepare LMM Input) attempts to merge theta scores with TSVR data
- Looks for: results/ch5/rq1/data/step00a_tsvr_data.csv (doesn't exist)
- Cannot find file, throws FileNotFoundError
- Blocks Steps 4-7 (data prep, model fitting, selection, plotting)

**Root Cause:** During RQ 5.2.1 setup, TSVR file was renamed from "step00a_tsvr_data" to "step00_tsvr_mapping" for consistency. RQ 5.1.1 documentation not updated.

**Verification:**
```
ls -la /home/etai/projects/REMEMVR/results/ch5/5.2.1/data/step00_tsvr_mapping.csv
  → File exists (7,914 bytes, verified 2025-11-30)

ls -la /home/etai/projects/REMEMVR/results/ch5/5.2.1/data/step00a_tsvr_data.csv
  → File not found
```

---

## HIGH ISSUES

### 3. RQ Identity Inconsistency - Documentation Uses Old Numbering

**Location:**
- docs/1_concept.md (header line 1-5)
- docs/4_analysis.yaml (line 11: `rq_id: "ch5/rq7"`)
- code/step01_irt_calibration_omnibus.py (docstring line 8: `RQ: results/ch5/rq7`)
- code/step02_purify_items.py (docstring line 8: `RQ: results/ch5/rq7`)
- All other stepNN_*.py files similarly

**Expected:** RQ 5.1.1 (to match folder name)

**Actual:** RQ 5.7 and ch5/rq7 found throughout

**Impact:** HIGH - Creates confusion about RQ identity
- Future users see folder named "5.1.1" but documentation says "RQ 5.7"
- Maintenance burden: must cross-reference mapping table (rq7 → 5.1.1)
- No execution-blocking impact but poor user experience
- Makes git history harder to follow across versions

**Details:**
- docs/1_concept.md: First line "# RQ 5.7: Functional Form of Forgetting Trajectories"
- docs/4_analysis.yaml: metadata.rq_id = "ch5/rq7" (should be "ch5/5.1.1")
- All Python scripts: docstring RQ field says "results/ch5/rq7"
- Mapping reference: rq7 → 5.1.1 (per REMEMVR refactor schema)

---

### 4. Analysis Steps Incomplete - Steps 6-7 Skipped But Not Documented in Plan

**Location:**
- docs/2_plan.md (header line 4: `**Steps:** 7 analysis steps`)
- docs/2_plan.md (line 957: `**Total Steps:** 5`)
- status.yaml (lines 69-70: step06 and step07 marked skipped)

**Expected:** All 7 steps complete OR plan clearly documents why steps are optional

**Actual:**
- Plan specifies 7 steps with full detailed specifications for all 7
- status.yaml shows steps 6-7 marked as skipped
- Reason documented: "Pickle unpickling issues, outputs from step05 sufficient"
- But plan doesn't mention this conditional execution or provide rationale

**Impact:** HIGH - Execution ambiguity
- Unclear whether Step 6-7 are OPTIONAL or BLOCKING
- Scientific analysis questions: Is model selection (Step 6) completed? Are plots (Step 7) generated?
- status.yaml shows rq_plots generated plots manually (successful), so visualization exists
- But automated AIC comparison (Step 6) skipped, so model selection may be incomplete

**Details:**
- docs/2_plan.md section "## Summary": Lists "**Total Steps:** 5" but content shows Steps 1-7 documented
- status.yaml shows:
  - step05_fit_5_candidate_lmms: success
  - step06_aic_model_selection: skipped (comment: "Pickle unpickling issues, outputs from step05 sufficient")
  - step07_prepare_functional_form_plots: skipped (comment: "Pickle unpickling issues, rq_plots will generate plots directly")
- This is reasonable technical decision but not reflected in plan documentation

### 5. Output File Naming Convention Violations

**Location:**
- plots/trajectory_data.csv
- plots/trajectory_functional_form.png
- results/step05_model_comparison.csv

**Expected Naming:** stepNN_descriptive_name.(csv|pkl|png)
**Actual Naming:**
- trajectory_data.csv (missing step prefix, missing folder organization)
- trajectory_functional_form.png (missing step prefix)

**Impact:** HIGH - Files violate REMEMVR folder conventions
- Per code comment (all stepNN_*.py files):
  ```
  # FOLDER CONVENTIONS (MANDATORY - NO EXCEPTIONS):
  # data/   : ALL data outputs (.csv, .pkl) - ANY file produced by code
  # plots/  : ONLY image files (.png, .pdf, .svg) - actual plot images
  # NAMING CONVENTION (MANDATORY):
  # ALL files in data/ and logs/ MUST be prefixed with step number
  ```
- trajectory_data.csv should be in data/ folder and named step07_trajectory_data.csv
- trajectory_functional_form.png should be named step07_trajectory_functional_form.png

**Details:**
- Actual files found:
  - /home/etai/projects/REMEMVR/results/ch5/5.1.1/plots/trajectory_data.csv (should be data/)
  - /home/etai/projects/REMEMVR/results/ch5/5.1.1/plots/trajectory_functional_form.png (OK location, wrong name)
- results/step05_model_comparison.csv is correctly named (results/ folder exempt from step prefix requirement)

---

## MODERATE ISSUES

### 6. Decision D039 Documentation Contradiction

**Location:** docs/2_plan.md (line 982)

**Expected:** Documentation consistent with actual implementation

**Actual:**
- Line 982 states: "Decision D039: NOT applied (single-factor IRT, no purification needed for exploratory omnibus analysis)"
- But status.yaml shows: step02_purify_items: success
- And 2_plan.md explicitly documents Step 2 purification with D039 thresholds (|b| ≤ 3.0, a ≥ 0.4)

**Impact:** MODERATE - Contradictory statements create confusion
- Scientific rationale unclear: Is purification applied or not?
- Actual execution shows purification IS applied (Step 2 successful)
- But final summary says "D039: NOT applied"
- Reconciliation: RQ uses single factor but purification still improves measurement quality (legitimate approach)

**Details:**
- docs/2_plan.md Step 2 section clearly describes D039 item purification
- docs/2_plan.md Step 3 refers to "purified items" from Step 2
- status.yaml confirms: step02_purify_items: success (40-60% expected retention achieved)
- But summary contradicts: "Decision D039: NOT applied"
- Correct interpretation: Decision D039 IS APPLIED in RQ 5.1.1 (applied per 2-pass IRT best practice regardless of dimensionality)

---

## Summary Table

| Severity | Count | Category |
|----------|-------|----------|
| CRITICAL | 2 | Path References (cross-RQ dependencies with broken paths) |
| HIGH | 3 | RQ ID Consistency (numbering mismatch), Step Completeness (skipped steps), Naming Conventions (file violations) |
| MODERATE | 1 | Documentation Consistency (Decision D039 contradiction) |
| **TOTAL** | **6** | **Path + Numbering + Completeness** |

---

## Root Cause Analysis

**Primary Cause:** Hierarchical Numbering Refactor (November 2025)

RQ folders were migrated from flat numbering (rq1-rq50) to hierarchical numbering (5.X.X, 6.X.X, 7.X.X). During this refactor:

1. **Folder Structure:** Successfully migrated (rq7 → 5.1.1, rq1 → 5.2.1, etc.)
2. **Internal References:** PARTIALLY updated
   - status.yaml fields updated ✓
   - Document headers NOT updated ✗
   - Code paths NOT updated ✗
   - Cross-RQ dependencies NOT updated ✗

3. **File Organization:** Minor drift
   - TSVR file renamed during reorganization (step00a_tsvr_data.csv → step00_tsvr_mapping.csv)
   - References not updated to reflect new name
   - Plot output files created with generic names (trajectory_*) instead of step-prefixed names

4. **Documentation Inconsistency:**
   - Concept and Plan docs still reference old numbering
   - Analysis recipe (4_analysis.yaml) mixes old paths with new metadata
   - Status contradicts plan in D039 decision section

---

## Execution Impact Assessment

**Current State:** NOT READY TO EXECUTE
- **Blocking Issue:** CRITICAL path errors prevent code from loading input data
- **Affected Steps:** 1 (immediate), 3, 4 (cascade failures)
- **Why:** Code looks for results/ch5/rq1/ which doesn't exist

**After Priority 1 Fixes:** READY TO EXECUTE
- All path references corrected to 5.2.1 and 5.1.1
- TSVR filename corrected to step00_tsvr_mapping.csv
- Steps 1-5 will execute successfully
- Steps 6-7 will remain skipped (intentional, documented)
- rq_plots will complete visualization

**After Priority 2 Fixes:** FULLY COMPLIANT
- RQ identity consistent (5.1.1 throughout)
- Output files properly named and organized
- Documentation contradictions resolved
- Ready for publication/archival

---

## Recommended Fixes

### PRIORITY 1: Fix Blocking Path References

**Step 1a: Update docs/4_analysis.yaml**
```
Find & Replace ALL occurrences:
- results/ch5/rq1/ → results/ch5/5.2.1/
- results/ch5/rq7/ → results/ch5/5.1.1/
- step00a_tsvr_data.csv → step00_tsvr_mapping.csv

Lines affected: 36, 37, 113, 259, 313, 388, 389, 532
```

**Step 1b: Update docs/2_plan.md**
```
Find & Replace ALL occurrences:
- results/ch5/rq1/ → results/ch5/5.2.1/
- results/ch5/rq7/ → results/ch5/5.1.1/ (if present)
- step00a_tsvr_data.csv → step00_tsvr_mapping.csv

Lines affected: 24, 42, 104, 161, 205, 258, 313, 388, 389, 804, 818
```

**Step 1c: Update all Python code files**
```
Files to update:
- code/step01_irt_calibration_omnibus.py
- code/step03_irt_calibration_pass2.py
- code/step04_prepare_lmm_input.py

Find & Replace:
- results/ch5/rq1/ → results/ch5/5.2.1/
- step00a_tsvr_data.csv → step00_tsvr_mapping.csv
```

### PRIORITY 2: Update RQ Identity in Documentation

**Step 2a: Update docs/1_concept.md**
```
- Header: "# RQ 5.7:" → "# RQ 5.1.1:"
- All RQ references: 5.7 → 5.1.1, rq7 → 5.1.1
```

**Step 2b: Update docs/4_analysis.yaml**
```
- metadata.rq_id: "ch5/rq7" → "ch5/5.1.1"
```

**Step 2c: Update all Python code docstrings**
```
- RQ: results/ch5/rq7 → RQ: ch5/5.1.1 (or results/ch5/5.1.1)
```

### PRIORITY 3: Correct Output File Naming

**Step 3a: Rename plot output files**
```
plots/trajectory_data.csv
  → Option A: data/step07_trajectory_data.csv (if data file)
  → Option B: plots/step07_trajectory_data.csv (if staying in plots)

plots/trajectory_functional_form.png
  → plots/step07_trajectory_functional_form.png
```

**Step 3b: Update docs/4_analysis.yaml if needed**
```
- Verify intended output folders match actual output locations
- Update step07 output file specifications if paths changed
```

### PRIORITY 4: Resolve Documentation Contradictions

**Step 4a: Fix 2_plan.md Decision D039 section**
```
Current (line 982):
"Decision D039: NOT applied (single-factor IRT, no purification needed)"

Should be:
"Decision D039: Applied (2-pass IRT purification with |b|≤3.0, a≥0.4 thresholds per Step 2. Purification improves measurement quality regardless of dimensionality)"
```

**Step 4b: Fix 2_plan.md Total Steps statement**
```
Current (line 957):
"**Total Steps:** 5"

Should be:
"**Total Steps:** 7 (Steps 1-5 completed, Steps 6-7 skipped due to pickle unpickling issues; rq_plots generates visualizations directly)"
```

**Step 4c: Add RQ ID to status.yaml**
```
Add field after first line:
rq_id: "ch5/5.1.1"
```

---

## Validation Checklist

After applying fixes, verify:

- [ ] docs/4_analysis.yaml contains NO references to results/ch5/rq1/ or results/ch5/rq7/
- [ ] docs/4_analysis.yaml references step00_tsvr_mapping.csv (not step00a_tsvr_data.csv)
- [ ] docs/2_plan.md contains NO references to results/ch5/rq1/ (except in cross-RQ dependency explanation)
- [ ] All Python code files use correct paths (5.2.1 for input, 5.1.1 for output)
- [ ] 1_concept.md header says "RQ 5.1.1" not "RQ 5.7"
- [ ] 4_analysis.yaml metadata.rq_id = "ch5/5.1.1"
- [ ] Plot files properly named with step07_ prefix
- [ ] status.yaml includes rq_id field
- [ ] Decision D039 documentation clarified in 2_plan.md

---

## Files Requiring Correction

**Documentation:**
- /home/etai/projects/REMEMVR/results/ch5/5.1.1/docs/1_concept.md (RQ ID)
- /home/etai/projects/REMEMVR/results/ch5/5.1.1/docs/2_plan.md (paths, step count, D039 contradiction)
- /home/etai/projects/REMEMVR/results/ch5/5.1.1/docs/4_analysis.yaml (paths, TSVR filename, rq_id)

**Code:**
- /home/etai/projects/REMEMVR/results/ch5/5.1.1/code/step01_irt_calibration_omnibus.py (paths, RQ ID)
- /home/etai/projects/REMEMVR/results/ch5/5.1.1/code/step03_irt_calibration_pass2.py (paths)
- /home/etai/projects/REMEMVR/results/ch5/5.1.1/code/step04_prepare_lmm_input.py (paths, TSVR filename)

**Output Organization:**
- /home/etai/projects/REMEMVR/results/ch5/5.1.1/plots/trajectory_data.csv (rename/relocate)
- /home/etai/projects/REMEMVR/results/ch5/5.1.1/plots/trajectory_functional_form.png (rename)

**Metadata:**
- /home/etai/projects/REMEMVR/results/ch5/5.1.1/status.yaml (add rq_id field)

---

## Audit Complete

**Summary:** RQ 5.1.1 folder migration incomplete. Cross-RQ dependency paths not updated during refactor. 6 issues identified: 2 CRITICAL (path references), 3 HIGH (ID inconsistency, step incompleteness, naming violations), 1 MODERATE (D039 contradiction).

**Execution Status:** NOT READY - Critical path errors will cause FileNotFoundError on first execution.

**Effort to Fix:** LOW - All fixes are string replacements (paths/filenames). No code logic changes required.

**Timeline to Ready:** <30 minutes with script-based find-and-replace.

