# RQ 5.1.2 Audit Report

**Audit Date:** 2025-12-01
**Auditor:** rq_audit agent v1.0.0
**RQ ID:** 5.1.2 (Two-Phase Forgetting Test)
**Folder Path:** /home/etai/projects/REMEMVR/results/ch5/5.1.2
**Status:** 7 issues identified (3 CRITICAL, 3 HIGH, 1 MODERATE)

---

## CRITICAL ISSUES

### 1. Path References Use Old RQ Numbering (rq7 instead of 5.1.1)

**Location:**
- docs/1_concept.md: lines 95, 138, 140, 142
- docs/2_plan.md: multiple references throughout
- docs/4_analysis.yaml: lines 35-56 (all input file paths)
- code/step00_get_data.py: docstring mentions "results/ch5/rq7/"

**Expected:** All references should use new numbering format `results/ch5/5.1.1/` (the source RQ folder)

**Actual:** All documentation and code reference old path format `results/ch5/rq7/data/` which does NOT exist

**Impact:** CRITICAL - Analysis code will fail at runtime when attempting to load dependency files from non-existent paths. Step 0 validation will trigger EXPECTATIONS ERROR: "RQ 5.7 must complete before RQ 5.8" but the actual error is path mismatch, not missing files.

**Evidence:**
```
grep -r "results/ch5/rq7" /home/etai/projects/REMEMVR/results/ch5/5.1.2/
# Returns 12 matches across docs and code
# Path does not exist: ls /home/etai/projects/REMEMVR/results/ch5/rq7/ -> No such file or directory
# Correct path exists: ls /home/etai/projects/REMEMVR/results/ch5/5.1.1/ -> exists with data/
```

---

### 2. Source RQ 5.1.1 Missing Required Output Files

**Location:**
- RQ 5.1.1 folder: /home/etai/projects/REMEMVR/results/ch5/5.1.1/data/

**Expected:** RQ 5.1.2 Step 0 requires:
- results/ch5/5.1.1/data/step02_theta_long.csv (IRT theta scores, domain-collapsed)
- results/ch5/5.1.1/data/step00_tsvr_mapping.csv (Time Since VR hours)
- results/ch5/5.1.1/data/step03_best_model.pkl (pickled best continuous LMM model)

**Actual:** RQ 5.1.1 (labeled as "rq7" in status.yaml) contains IRT analysis outputs, NOT trajectory analysis outputs:
```
RQ 5.1.1 data files:
- step01_theta_scores.csv (IRT Pass 1 theta)
- step02_purified_items.csv (item purification)
- step03_theta_scores.csv (IRT Pass 2 theta)
- step04_lmm_input.csv (LMM input data)
- lmm_Linear.pkl, lmm_Quadratic.pkl, lmm_Log.pkl, ... (5 different candidate models)
```

**Impact:** CRITICAL - Even if paths are corrected to 5.1.1, the required files don't exist in the expected format. The source RQ outputs don't include the domain-collapsed theta and TSVR mapping that Step 0 expects. The best model pickle file would need to be identified from 5 different model files (no single "step03_best_model.pkl" exists).

**Root Cause:** RQ 5.1.2 specification (rq_audit agent comments: "RQ 5.7" which maps to 5.1.1 per TSV) expects RQ 5.1.1 to run a trajectory functional form comparison analysis (5 models: Linear, Quadratic, Log, Lin+Log, Quad+Log), but RQ 5.1.1's actual agent-generated code appears to have only performed IRT calibration without the LMM trajectory modeling step.

---

### 3. RQ 5.1.2 Specification References Wrong Source RQ Files in Concepts and Plans

**Location:**
- docs/1_concept.md: line 138-142 (Data Source section)
- rq_refactor.tsv: line 3 (Data_Required column)

**Expected:** Step 0 documentation specifies source RQ as "RQ 5.7" (mapped to 5.1.1) but references:
- results/ch5/rq7/data/step02_theta_long.csv
- results/ch5/rq7/data/step00_tsvr_mapping.csv
- results/ch5/rq7/data/step03_best_model.pkl

**Actual:** The naming inconsistency is bidirectional:
- Folder name is 5.1.2 (new hierarchical format)
- But documentation references rq7/rq8 (old sequential format)
- RQ 5.1.2 is correctly labeled as "old RQ 5.8" in rq_refactor.tsv
- RQ 5.1.1 is correctly labeled as "old RQ 5.7" in rq_refactor.tsv

**Impact:** CRITICAL - This bidirectional naming inconsistency creates confusion about which RQ is the source. While the mapping TSV clarifies old-to-new, the inconsistency means users/agents could look in either location and find nothing in the old format paths.

---

## HIGH ISSUES

### 4. Numbering Inconsistency: Document Headers vs Folder Name

**Location:**
- Folder name: 5.1.2
- docs/1_concept.md: "RQ 5.8: Evidence for Two-Phase Forgetting" (line 1)
- status.yaml: rq_builder context shows "created results/ch5/rq8/" (line 3)
- docs/4_analysis.yaml: metadata rq_id: "ch5/rq8" (line 11)

**Expected:** All RQ identifiers should use hierarchical format (5.1.2 = new, rq8 = old)

**Actual:**
- Folder: 5.1.2 (new)
- Concept document title: "RQ 5.8" (mixed notation - says "5.8" but RQ 5.8 is not the same as 5.1.2 structurally)
- status.yaml and analysis recipe: use "rq8" and "ch5/rq8" (old format)
- rq_refactor.tsv: correctly maps "5.8 (old) -> 5.1.2 (new)"

**Impact:** HIGH - Documentation ambiguity could cause misunderstandings. Someone reading "RQ 5.8" might think it's a different RQ in the Chapter 5 quantitative section (which has 15 RQs numbered 5.1-5.15 in the mapping TSV). The new hierarchical system (5.1.2) makes the parent-child relationship explicit (5=Chapter, 1=Section, 2=RQ within section).

**Evidence:**
```
rq_refactor.tsv line 3: "5.1.2	General	Two-Phase Forgetting Test	5.8"
               mapping:  New numbering  Category  Description         Old numbering
```

---

### 5. Domain Collapse Output Missing in Step 0 Specification

**Location:**
- docs/2_plan.md: Step 0 section (lines 74-204)
- docs/4_analysis.yaml: step00_get_data operations (lines 33-46)

**Expected:** Step 0 output file data/step00_theta_tsvr.csv documented as:
- Source: "Merged theta + TSVR, domain-collapsed"
- Rows: ~400 (100 participants x 4 tests - collapsed across 3 domains)
- Process: "Group by (UID, test, TSVR_hours), compute mean(theta) across 3 domains"

**Actual:**
- The source RQ 5.1.1 produces step03_theta_scores.csv and step04_lmm_input.csv
- RQ 5.1.1 status shows IRT Pass 2 calibration but NOT explicit domain-collapse operation
- The TSVR_mapping file expected doesn't exist with that name in RQ 5.1.1
- The "collapsed across domains" operation is specified in Step 0 plan but source file format is unclear

**Impact:** HIGH - The domain-collapse step assumes input has 3 domain columns (What, Where, When), but RQ 5.1.1 outputs are structured differently. The aggregate theta (mean across domains) is a fundamental transformation, and if the source data structure doesn't match, Step 0 will fail with data shape mismatch error.

---

### 6. Inconsistent Step Numbering in File Outputs

**Location:**
- docs/2_plan.md: Output files for Step 2 (line 360) show path "results/step02_quadratic_model_summary.txt"
- docs/4_analysis.yaml: Step 2 output (line 218) shows path "data/step02_quadratic_model_summary.txt"

**Expected:** Consistent folder location for model summaries

**Actual:**
- 2_plan.md: Step 2 output -> "results/step02_quadratic_model_summary.txt"
- 4_analysis.yaml: Step 2 output -> "data/step02_quadratic_model_summary.txt"
- Actual files in folder: results/step02_quadratic_model_summary.txt (matches 2_plan.md)

**Impact:** HIGH - The analysis recipe (4_analysis.yaml) specifies output path as "data/" but actual generated files are in "results/". The code likely follows the analysis recipe, creating files in wrong location. Validation tools would look for files in "results/" (per 2_plan.md) but code might write to "data/", creating a validation failure.

**Resolution Status:** The execution appears to have used "results/" location (correct per 2_plan.md), but the specification in 4_analysis.yaml is wrong.

---

## MODERATE ISSUES

### 7. No Explicit Dependency Status Documentation in Status.yaml

**Location:**
- status.yaml: rq_concept section (lines 16-27)

**Expected:** Explicit circuit-breaker status: "Dependency on RQ 5.7 COMPLETE" or "Dependency on RQ 5.7 INCOMPLETE - cannot proceed"

**Actual:**
```yaml
rq_concept:
  status: success
  context_dump: |
    ...
    Data: DERIVED from RQ 5.7 (theta scores, TSVR mapping, best continuous model)
    Critical: Tests consolidation theory inflection at Day 1 (48h TSVR).
    Requires RQ 5.7 complete.
```

The dependency is mentioned but not formally validated. The status.yaml shows all downstream agents (rq_scholar, rq_stats, rq_planner, rq_tools, rq_analysis, g_code, rq_inspect, rq_plots, rq_results) with status: success, but this success is based on analysis of RQ 5.1.1 outputs which may not be complete for this RQ's needs.

**Impact:** MODERATE - Anyone reviewing status.yaml would assume RQ 5.1.2 is fully ready for execution, but the dependency check may not have caught the missing domain-collapsed theta file. Future audits should explicitly validate RQ 5.1.1 output structure matches RQ 5.1.2 input expectations.

---

## Summary Table

| Severity | Count | Issues |
|----------|-------|--------|
| CRITICAL | 3 | Path reference format mismatch (rq7→5.1.1), source files missing, naming ambiguity |
| HIGH | 3 | Numbering inconsistency (5.8 vs 5.1.2), domain collapse assumption, output path inconsistency |
| MODERATE | 1 | Dependency status not formally documented |
| LOW | 0 | |
| **TOTAL** | **7** | |

---

## Root Cause Analysis

### Pattern 1: Naming System Transition (v3.0 → v4.X Architecture)

The codebase is mid-transition from v3.0 (7-agent monolithic, rqN sequential numbering) to v4.X (13-agent atomic, hierarchical numbering). This RQ folder shows:

- **v4.X features present:**
  - Folder structure: results/ch5/5.1.2/ (hierarchical parent.child.number format)
  - 10 RQ-specific agents in status.yaml (rq_builder, rq_concept, rq_scholar, etc.)
  - Modular agent workflow (7 independent agents)

- **v3.0 remnants:**
  - Document text: "RQ 5.8" instead of "RQ 5.1.2"
  - status.yaml: "rq_builder: created results/ch5/rq8/" (old path format)
  - Analysis recipe: rq_id: "ch5/rq8" (old format)
  - All file paths: results/ch5/rq7/ (old format)

**Root Cause:** The rq_builder and rq_concept agents generated folder and documentation using the old RQ numbering scheme (5.8) before the numbering system migration was complete. Agents should have detected the migration status and used the new format (5.1.2).

### Pattern 2: Circular Dependency on Incomplete Source RQ

RQ 5.1.2 was specified to depend on RQ 5.1.1 (old 5.7) outputs, but:
- RQ 5.1.1 appears to have completed only IRT calibration (steps 1-3: calibration, purification, re-calibration)
- RQ 5.1.2 expects RQ 5.1.1 to have completed IRT + trajectory LMM analysis (steps 4-6: LMM fitting, model comparison, plot prep)
- The specification planning happened, but execution may have stopped after IRT calibration

**Root Cause:** Missing explicit validation in status.yaml that RQ 5.1.1 outputs include LMM trajectory model results, not just IRT calibration results.

### Pattern 3: Analysis Specification Files Diverged

The specification documents were created in sequence:
1. 1_concept.md (rq_concept agent) - uses "rq7" paths
2. 2_plan.md (rq_planner agent) - uses "rq7" paths, outputs in "results/"
3. 3_tools.yaml (rq_tools agent) - inherits paths from 2_plan.md
4. 4_analysis.yaml (rq_analysis agent) - specifies outputs in "data/" (INCONSISTENT with 2_plan.md)

**Root Cause:** rq_analysis agent may have auto-mapped output folders incorrectly, or the tool specifications didn't propagate correctly to the analysis recipe.

---

## Recommended Fixes

### CRITICAL - Fix Path References (Must complete before execution)

1. **Search and replace in all files:**
   ```bash
   # In docs/:
   sed -i 's|results/ch5/rq7|results/ch5/5.1.1|g' *.md *.yaml

   # In code/:
   sed -i 's|results/ch5/rq7|results/ch5/5.1.1|g' *.py

   # In status.yaml:
   sed -i 's|results/ch5/rq8|results/ch5/5.1.2|g' status.yaml
   sed -i "s|'ch5/rq8'|'ch5/5.1.2'|g" status.yaml
   ```

2. **Verify source RQ 5.1.1 has required outputs:**
   - Check if results/ch5/5.1.1/data/step04_lmm_input.csv or step03_theta_scores.csv has the expected format
   - If domain column exists, verify Step 0 domain-collapse code handles it correctly
   - If domain column doesn't exist, check if theta scores are already aggregated (no collapse needed)
   - Identify which of the 5 model pickle files (lmm_Linear.pkl, etc.) is the "best model" based on AIC
   - If AIC comparison file doesn't exist, Step 0 must create it from the model files

3. **Update Step 0 to handle actual RQ 5.1.1 structure:**
   - Read the actual step03_theta_scores.csv or step04_lmm_input.csv structure
   - Verify if domain columns (What/Where/When) exist
   - If they don't, domain-collapse operation may be unnecessary
   - If AIC file missing, extract AIC from the 5 best-fitting models and save as required

### HIGH - Standardize RQ Numbering in Specifications

4. **Update all document headers to use new hierarchical format:**
   - 1_concept.md: Change "RQ 5.8" to "RQ 5.1.2" in title and throughout
   - 2_plan.md: Change references from "RQ 5.8" to "RQ 5.1.2"
   - 4_analysis.yaml: Change rq_id from "ch5/rq8" to "ch5/5.1.2"
   - status.yaml: Update context dumps to reference "5.1.2" instead of "rq8"

5. **Fix output folder inconsistency:**
   - Verify all step outputs should go to "results/" folder (per 2_plan.md and actual files)
   - Update 4_analysis.yaml to change output paths from "data/" to "results/" for model summaries
   - Ensure code generation follows corrected specification

6. **Document Dependency Status Explicitly:**
   - Add to status.yaml:
     ```yaml
     dependency_check:
       status: "NEEDS_VALIDATION"
       rq_51: "5.1.1"
       required_files:
         - path: "results/ch5/5.1.1/data/step03_theta_scores.csv"
           status: "EXISTS_VERIFY_STRUCTURE"
       notes: "Need to confirm theta domain structure matches Step 0 expectations"
     ```

### MODERATE - Add Validation Layer

7. **Create Step 0 circuit-breaker validation:**
   - Before attempting any file loading, validate:
     - RQ 5.1.1 folder exists
     - Data files exist (regardless of exact naming)
     - File structure matches expected schema (columns, dtypes)
     - If structure mismatch detected, provide detailed error message rather than generic "file not found"

---

## Validation Checklist (Post-Fix)

- [ ] All path references updated from rq7 to 5.1.1
- [ ] All path references updated from rq8 to 5.1.2 in documentation and code
- [ ] Step 0 code tested with actual RQ 5.1.1 output files
- [ ] Domain-collapse operation verified or removed based on actual data structure
- [ ] All output folders match specification (results/ for summaries, data/ for data)
- [ ] Status.yaml dependency status explicitly documented
- [ ] Execution test: Step 0 loads data successfully without errors
- [ ] Execution test: Step 0 outputs match specification (400 rows, 4 columns, no NaN)

---

## Affected Components

**Files needing updates:**
- docs/1_concept.md (8 instances)
- docs/2_plan.md (20+ instances)
- docs/3_tools.yaml (2 instances)
- docs/4_analysis.yaml (9 instances)
- code/step00_get_data.py (docstring + code)
- status.yaml (context dumps and metadata)

**Dependencies to verify:**
- RQ 5.1.1 (source): /home/etai/projects/REMEMVR/results/ch5/5.1.1/
  - Verify: data/step03_theta_scores.csv OR step04_lmm_input.csv
  - Verify: TSVR mapping file exists (name may vary)
  - Verify: Best-fitting LMM model pickle (may be 1 of 5 files)

**Downstream Impact:**
- Steps 1-6 depend on Step 0 completing successfully
- All 7 agent statuses (rq_planner, rq_tools, rq_analysis, g_code, rq_inspect, rq_plots, rq_results) show "success" but execution may fail when code is actually run

---

## Notes for Future Audits

1. **Naming System Migration:** Add check for bidirectional format consistency (old rqN ↔ new X.Y.Z) using rq_refactor.tsv mapping table
2. **Dependency Validation:** Validate not just file existence but file structure (schema matching) for cross-RQ dependencies
3. **Agent Consistency:** Check that all agents update RQ metadata to consistent format (all new format or all old format, but not mixed)
4. **Specification Evolution:** Track when specifications were created (timestamps in agent context_dumps) and note if any part of spec older than source RQ completion

---

**Audit Status:** COMPLETE
**Recommendation:** DO NOT EXECUTE until CRITICAL issues 1-3 are resolved
**Next Step:** Fix path references, verify source RQ structure, run Step 0 test

---

**End of Audit Report**
