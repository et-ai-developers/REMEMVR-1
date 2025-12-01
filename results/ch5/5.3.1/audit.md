# RQ 5.3.1 Audit Report

**Audit Date:** 2025-12-01
**Auditor:** rq_audit agent v1.0.0
**RQ ID:** 5.3.1 (Paradigm-Specific Forgetting Trajectories)
**Status:** CRITICAL ISSUES IDENTIFIED

---

## CRITICAL ISSUES

### 1. Cross-RQ Path References Use Old Naming Convention (rq1 instead of 5.2.1)

- **Location:**
  - `code/step00_prepare_paradigm_data.py` line 85, 139, 144
  - `docs/1_concept.md` lines 102, 104, 175
  - `docs/2_plan.md` lines 38, 47, 50, 65, 102, 823
  - `docs/4_analysis.yaml` lines 24, 26, 45, 50, 56, 65, 73

- **Expected:** Path should reference `results/ch5/5.2.1/data/step00_irt_input.csv` (and step00_tsvr_mapping.csv)
- **Actual:** References use `results/ch5/rq1/data/step00_irt_input.csv` (old naming convention)
- **Impact:** **CRITICAL** - Code will fail at runtime because `results/ch5/rq1/` folder does not exist. The actual folder is `results/ch5/5.2.1/`. This affects:
  - `step00_prepare_paradigm_data.py` (line 85): `SOURCE_RQ_DIR = RQ_DIR.parents[1] / "ch5" / "rq1"`
  - Runtime error will occur when trying to load `/home/etai/projects/REMEMVR/results/ch5/rq1/data/step00_irt_input.csv` (path does not exist)
- **Verification:** Folder listing shows 5.2.1 exists, rq1 does not exist in /results/ch5/
- **Root Cause:** Documentation and code generated with old RQ naming scheme (rq1-rq15) before migration to hierarchical numbering (5.X.Y). Refactor mapping exists in `rq_refactor.tsv` showing `rq3 -> 5.3.1`, but corresponding backward mapping shows `5.2.1 -> rq1` was not reflected in these files.

---

### 2. Step 8 Referenced in Documentation But Not Implemented in Status

- **Location:**
  - `docs/2_plan.md` line 147 mentions "Step 8: Visualization"
  - `docs/2_plan.md` step count header (line 16): "Steps: 8 total"
  - `docs/4_analysis.yaml` metadata (line 12): `total_steps: 8`

- **Expected:** Either 8 analysis steps (Step 0-7 = 8 steps) OR documentation clarifies that Step 7 is final (Step 8 not executed)
- **Actual:**
  - Documentation describes 8 steps (Step 0 through Step 7 = 8 total)
  - `status.yaml` shows 8 steps listed: `step00_prepare_paradigm_data` through `step07_prepare_trajectory_plot_data`
  - No `step08_plot_trajectories` in code folder or data outputs
  - `logs/step08_plot_trajectories.log` EXISTS (empty or minimal content)

- **Impact:** **HIGH** - Inconsistency between documentation (8 steps) and implementation (8 steps but Step 7 is final analysis, Step 8 appears to be plotting which was not included in formal 8-step count). The log file suggests attempt to run step 8 but no corresponding code file or output data.
- **Note:** Upon review, status.yaml shows 8 steps complete (step00-step07), which is correct (8 steps total: 0,1,2,3,4,5,6,7). The mention of "Step 8" in docs/2_plan.md line 147 appears to be documentation error (should say "Step 7").

---

## HIGH ISSUES

### 3. Discrepancy in Numbering Between Folder Name and Documentation Headers

- **Location:**
  - Folder name: `5.3.1`
  - `docs/1_concept.md` line 4: `RQ Number: 3` (should be `5.3.1` or at least `3.1`)
  - `docs/1_concept.md` line 5: `Full ID: 5.3` (should be `5.3.1`)
  - `docs/2_plan.md` line 1: "RQ 5.3" (should be `5.3.1`)
  - `docs/4_analysis.yaml` line 11: `rq_id: "ch5/rq3"` (should be `ch5/5.3.1`)

- **Expected:** All documentation should consistently reference RQ ID as `5.3.1` to match folder name and hierarchical numbering scheme
- **Actual:** Some files use old naming (`5.3` or `rq3`) while folder is `5.3.1`
- **Impact:** **HIGH** - Inconsistency may confuse cross-references and makes it unclear if this is the complete RQ 5.3 or a subcomponent (5.3.1). The hierarchical naming suggests this is subquestion 1 under RQ 5.3, but documentation doesn't clarify this structure.
- **Note:** This is a documentation clarity issue, not a functional error. Code appears to handle paths correctly despite naming confusion.

---

### 4. RQ ID Inconsistency in Code Comments

- **Location:** Multiple code files contain hardcoded RQ references:
  - `code/step00_prepare_paradigm_data.py` line 8: `RQ: results/ch5/rq3`
  - `code/step01_irt_calibration_pass1.py`: `RQ: results/ch5/rq3`
  - `code/step03_irt_calibration_pass2.py`: `RQ: results/ch5/rq3`
  - `code/step05_fit_lmm.py`: `RQ: results/ch5/rq3`

- **Expected:** Comments should use new naming `results/ch5/5.3.1` to match folder structure
- **Actual:** Comments reference old naming `results/ch5/rq3`
- **Impact:** **HIGH** - While code uses correct relative paths (parents[1]), comments reference wrong paths that don't exist, causing confusion for code maintenance and debugging
- **Severity:** Comment error only (not runtime-affecting) but reduces code clarity

---

### 5. Cross-RQ Dependency Validation Missing from Step 0

- **Location:** `code/step00_prepare_paradigm_data.py` lines 138-146
- **Expected:** Step 0 should validate that source RQ 5.2.1 files exist BEFORE attempting to load them (circuit breaker pattern)
- **Actual:** Code attempts to load from source RQ without error checking for existence
- **Impact:** **HIGH** - If RQ 5.2.1 is missing or incomplete, this step will fail with cryptic "file not found" error rather than clear "dependency missing" message. No error message guides user to complete RQ 5.2.1 first.
- **Recommendation:** Add explicit check at step start:
  ```python
  if not irt_input_path.exists():
      raise FileNotFoundError(f"RQ 5.2.1 dependency missing. Please complete results/ch5/5.2.1 Step 0 first.")
  ```

---

## MODERATE ISSUES

### 6. Paradigm-Domain Confound Not Explicitly Documented in Methodology

- **Location:** `docs/1_concept.md` lines 63-91, `docs/2_plan.md` (entire file)
- **Expected:** Specification should explicitly note that this RQ collapses across What/Where/When domains within each paradigm, and that domain differences from RQ 5.2.1 may confound paradigm effects
- **Actual:** Specification mentions "Within each paradigm, items span What (-N-), Where (-L-/-U-/-D-), and When (-O-) domains. Domain is not a factor in this analysis" (1_concept.md line 89-90) but does NOT flag potential confound
- **Impact:** **MODERATE** - Future readers may not realize that paradigm-specific forgetting rates could reflect domain composition differences rather than pure paradigm effects. The summary.md documents this limitation (Section 4, line 469) but it should be elevated to methodology.
- **Recommendation:** Add to 1_concept.md or 2_plan.md: "Potential Confound: Paradigm factors may include domain effects if item distributions differ across paradigms (e.g., Recognition has more What items, fewer When items). Future RQ 5.3.7-5.3.8 will cross Paradigm × Domain to disentangle."

---

### 7. Item Imbalance Not Reflected in Specification Planning

- **Location:** `docs/2_plan.md` (entire specification), `results/summary.md` lines 461-466
- **Expected:** Plan should note that IRT purification may result in unequal items per paradigm, and specify minimum items required per paradigm
- **Actual:**
  - Specification assumes "at least 10 items per paradigm" (Step 2 line 267)
  - Actual result: Free Recall = 12 items, Cued Recall = 19 items, Recognition = 14 items (62.5% retention overall, disproportionate Recognition exclusion at 46.4%)
  - This imbalance is noted in summary.md as methodological limitation but NOT flagged in specification planning
- **Impact:** **MODERATE** - Item imbalance affects theta reliability and comparison power, but was not explicitly considered during power/sample size planning. The specification treats items as equivalent.
- **Recommendation:** Sensitivity analysis suggested in summary.md (Section 5, lines 600-603) should be documented as planned follow-up in specification.

---

### 8. Two-Phase Decision Point Not Documented (Step 7 vs Step 8 Plotting)

- **Location:** `docs/2_plan.md` lines 630-743 (Step 7 description), lines 147-150 (reference to Step 8)
- **Expected:** Clear decision rule: Should Step 7 (plot data preparation) and Step 8 (actual plotting) be separate? Documentation should clarify.
- **Actual:**
  - Step 7 generates CSV files for plotting (theta and probability scale data)
  - Step 8 references "Visualization" but Step 7 specification says "Plot data preparation IS an analysis step" with validation requirements
  - The architectural decision (Option B: g_code creates plot source CSV, rq_plots creates actual images) is documented but execution unclear
  - `plots/plots.py` exists (plotting functions) but no corresponding `step08_plot_trajectories.py`
- **Impact:** **MODERATE** - Architectural clarity issue. The specification says Step 7 is final analysis step with validation. Step 8 appears to be visualization (plotting), which may or may not be considered part of "analysis". No explicit execution flowchart.
- **Note:** Status.yaml shows all 8 steps (including step00-step07) as successful, suggesting 8 steps were planned but step naming may be off by one in documentation.

---

## LOW ISSUES

### 9. Naming Inconsistency: "paradigm" vs "factor" Terminology

- **Location:**
  - `code/step00_prepare_paradigm_data.py` lines 170, 219-222: Uses `factor` in comments but `free_recall`, `cued_recall`, `recognition` in code
  - `docs/2_plan.md` lines 105-108: "Q-matrix with paradigm factor structure" (mixing terminology)
  - `docs/4_analysis.yaml` line 174: `domain_name` (should be `paradigm_name` per specification)

- **Expected:** Consistent terminology throughout codebase: either "paradigm" (primary term in RQ 5.3) or "factor" (statistical term), not interchanged
- **Actual:** Mixed usage of "paradigm" and "factor" depending on context
- **Impact:** **LOW** - Inconsistent terminology may confuse readers but does not affect functionality. IRT literature uses "factor" for dimensions, so some mixing is acceptable.
- **Recommendation:** Adopt convention: "paradigm" for conceptual (Free Recall paradigm), "factor" for statistical (free_recall factor in IRT model)

---

### 10. Missing Expected Intermediate Output File

- **Location:** `logs/step01_pass1_item_params.csv` and `logs/step01_pass1_theta.csv` exist but are not referenced in final results summary
- **Expected:** Specification says these are "diagnostic" outputs (Step 1, lines 157-165) but they should be listed in final output manifest
- **Actual:** Files exist in logs/ but are not documented in results/summary.md outputs section
- **Impact:** **LOW** - These are intermediate diagnostic files, not required for final analysis, but their existence suggests they were generated for debugging/validation purposes. Not an error, just a documentation omission.

---

## Summary Table

| Severity | Count | Categories |
|----------|-------|----------|
| CRITICAL | 1 | Path references (rq1 vs 5.2.1) |
| HIGH | 4 | Step numbering inconsistency, RQ ID clarity, RQ ID in comments, Dependency validation |
| MODERATE | 3 | Paradigm-domain confound documentation, Item imbalance planning, Step 7/8 decision clarity |
| LOW | 2 | Terminology consistency, Output file documentation |
| **TOTAL** | **10** | |

---

## Root Cause Analysis

### Primary Root Cause: Naming Scheme Migration (rq1-rq15 → 5.X.X.X)

The project underwent migration from old RQ naming (rq1, rq2, ..., rq15) to hierarchical numbering (5.1.1, 5.1.2, ..., 5.4.8) as documented in `rq_refactor.tsv`.

**What went wrong:**
1. RQ 5.3.1 specification documents and code were generated with knowledge that this RQ depends on RQ 5.2.1 (old name: rq1)
2. The refactor mapping file shows `5.2.1 -> rq1` but this backward mapping was not used to update all cross-references in 5.3.1 files
3. Some files (documentation) retained old naming (`rq1`), while others (code structure via relative paths) used new naming (folder structure)
4. Result: Documentation and comments reference non-existent paths that would fail at runtime

**Why this matters:** This RQ cannot execute Step 0 because it cannot find the source data from RQ 5.2.1 due to incorrect path naming.

### Secondary Root Cause: Specification Generation Timing

The 8-step plan, 4_analysis.yaml, and 3_tools.yaml were likely generated DURING or AFTER the naming migration, creating inconsistency:
- Documentation headers show mixed naming (5.3 vs 5.3.1 vs rq3)
- Code paths use relative navigation (works around naming) but comments hardcode old names
- Folder structure (5.3.1) is newer than some documentation content

---

## Recommended Fixes

### Priority 1: Critical (Fix Before Execution)

1. **Update all cross-RQ path references in code:**
   - File: `code/step00_prepare_paradigm_data.py` line 85
   - Change: `SOURCE_RQ_DIR = RQ_DIR.parents[1] / "ch5" / "rq1"`
   - To: `SOURCE_RQ_DIR = RQ_DIR.parents[1] / "ch5" / "5.2.1"`

2. **Update all cross-RQ path references in documentation:**
   - File: `docs/1_concept.md` lines 102, 104, 175
   - File: `docs/2_plan.md` lines 38, 47, 50, 65, 102, 823
   - File: `docs/4_analysis.yaml` lines 24, 26, 45, 50, 56, 65, 73
   - Change all: `results/ch5/rq1/` → `results/ch5/5.2.1/`
   - Change all: `ch5/rq1` → `ch5/5.2.1`

3. **Add dependency validation to Step 0:**
   - File: `code/step00_prepare_paradigm_data.py` after line 139
   - Add explicit file existence checks with helpful error messages

### Priority 2: High (Fix Before Publication)

4. **Standardize RQ ID across all documentation:**
   - Change all `RQ 5.3` → `RQ 5.3.1` in documentation headers
   - Change all `rq_id: "ch5/rq3"` → `rq_id: "ch5/5.3.1"` in YAML

5. **Update all RQ ID comments in code:**
   - Change all `RQ: results/ch5/rq3` → `RQ: results/ch5/5.3.1` in code comments

6. **Add dependency validation error messaging:**
   - Implement circuit breaker pattern in step00 to check RQ 5.2.1 completion
   - Provide user-friendly error message directing completion of RQ 5.2.1

### Priority 3: Moderate (Improve Clarity)

7. **Document potential paradigm-domain confound:**
   - Add "Potential Confound" section to 1_concept.md methodology
   - Reference future RQ 5.3.7-5.3.8 for disentangling

8. **Clarify step count and Step 7/8 boundary:**
   - Verify if Step 8 is actual plotting (rq_plots agent) or part of Step 7
   - Update documentation to clarify 8-step total (including or excluding plotting?)

9. **Add item imbalance acknowledgment to specification:**
   - Note in 2_plan.md that purification may produce unequal items per paradigm
   - Reference RQ 5.3.6 sensitivity analysis as planned follow-up

### Priority 4: Low (Polish)

10. **Standardize terminology:** "paradigm" vs "factor" usage
11. **Document intermediate outputs:** Add `logs/step01_*.csv` files to outputs manifest

---

## Verification Checklist

After fixes, verify:

- [ ] All `results/ch5/rq1/` references changed to `results/ch5/5.2.1/`
- [ ] All `ch5/rq1` references changed to `ch5/5.2.1` in YAML
- [ ] All `RQ: results/ch5/rq3` comments changed to `RQ: results/ch5/5.3.1`
- [ ] All RQ ID headers show `5.3.1` consistently (not `5.3` or `rq3`)
- [ ] Step 0 includes explicit file existence check for RQ 5.2.1 files
- [ ] Error message for missing RQ 5.2.1 dependency is user-friendly
- [ ] Documentation explains paradigm-domain confound (cross-reference to RQ 5.3.7)
- [ ] Item imbalance mentioned in specification as expected outcome
- [ ] Step 7 vs Step 8 boundary clearly defined in documentation

---

## Summary

This RQ folder is **FUNCTIONALLY INCOMPLETE** due to CRITICAL path reference errors that will cause runtime failure. The specification is well-structured (8 steps with validation requirements) and execution is mostly complete (status shows all steps as success), but the cross-RQ dependency uses outdated naming that doesn't match actual folder structure.

**Immediate Action Required:** Update line 85 in `code/step00_prepare_paradigm_data.py` from `"rq1"` to `"5.2.1"` and corresponding changes in all documentation files before attempting execution. Without these fixes, Step 0 will fail when trying to load RQ 5.2.1 data.

The root cause is the naming scheme migration from rq-based to hierarchical numbering. The fix is straightforward but requires updating 13+ path references across 4 files (1 code, 3 docs).

---

**Audit completed by:** rq_audit agent v1.0.0
**Date:** 2025-12-01
**Next steps:** User should review CRITICAL issues and apply Priority 1 fixes before attempting to execute this RQ

