# Standard Procedure for Building Research Questions (RQs)

**Version:** 3.0
**Last Updated:** 2025-11-12
**Status:** Current (Production-Ready)
**Replaces:** v2.0 (lacked stateful agent design, used JSON reports)

---

## Purpose

This document defines the **mandatory 8-step procedure** for building, validating, and executing each of the 50 research questions (RQs) in the REMEMVR PhD thesis. Each step includes safety gates, verification checkpoints, and user approval requirements to prevent catastrophic failures like mock data generation.

**Key Improvements in v3.0:**
- Stateful rq-spec agent via context dumps (maintains continuity across invocations)
- Markdown reports (human-readable, thesis-appropriate)
- Hybrid safety audits (automated + user approval)
- Universal templates (not locked to IRT/LMM)

---

## Prerequisites

Before starting ANY RQ:

1. ✅ **Tools validated:** `poetry run pytest tests/` shows 49/49 passing
2. ✅ **Agents in place:** All agents in `.claude/agents/` directory
3. ✅ **Templates available:** `docs/templates/` contains info_template.md, config_schema.yaml, all agent report templates
4. ✅ **master.xlsx accessible:** Data file at `data/master.xlsx`
5. ✅ **Git clean state:** `git status` shows no uncommitted changes
6. ✅ **Context budget healthy:** <100k tokens before starting

---

## The 8-Step Procedure

### Step 1: Specification (Draft Phase)

**Agent:** `rq_specification` (stateful)
**Input:** RQ number (e.g., "ch5/rq1"), thesis context
**Output:**
- `info.md` (10 sections - universal template, adapted to RQ's analysis type)
- `config.yaml` (machine-readable parameters)
- `status.md` (phase tracking)
- `logs/rq_spec_context.md` (agent context dump for continuity)
- Empty directories: `validation/`, `data/`, `code/`, `plots/`

---

#### Agent Behavior (Draft Phase)

**On Invocation:**
1. **Scan RQ folder structure:**
   - Check if `logs/rq_spec_context.md` exists (prior invocations?)
   - Check if `validation/scholar_report.md` and `validation/statistics_report.md` exist

2. **Determine phase:**
   - No validation reports found → **DRAFT PHASE** (first invocation)
   - Both reports exist → **FINALIZATION PHASE** (second invocation)

3. **If Draft Phase:**
   - Read RQ number and thesis context from master
   - Generate complete RQ specification (10 sections)
   - Create config.yaml with analysis parameters
   - Create status.md with initial state
   - Write `logs/rq_spec_context.md` documenting all decisions, rationale, open questions

4. **If Finalization Phase:**
   - Read `logs/rq_spec_context.md` (recall prior decisions)
   - Read `validation/scholar_report.md` and `validation/statistics_report.md`
   - Incorporate feedback into info.md
   - Append to `logs/rq_spec_context.md` with finalization reasoning
   - Create `logs/rq_specification_report.md` documenting all changes made

---

#### info.md Structure (Universal - 10 Sections)

**Template:** `docs/templates/info_template.md`

**Sections:**
1. **Status** - Phase tracking table (updated by all agents)
2. **Research Question** - Verbatim RQ
3. **Hypotheses** - With references (scholar agent provides citations)
4. **Input Data** - EXECUTABLE specifications for data-prep agent:
   - Exact master.xlsx tags
   - Expected dimensions (rows × columns)
   - Filters to apply
   - Quality thresholds
5. **Method** - Tool-by-tool procedure for analysis-executor agent:
   - Step-by-step instructions
   - Tool function names (e.g., `tools.analysis_irt.calibrate_grm`)
   - Input/output files for each step
   - Parameters (references config.yaml)
6. **Validation** - Procedures + Results:
   - Validation procedures (for analysis-executor to follow)
   - Results section (analysis-executor appends after execution)
7. **Plots** - Specifications for each visualization
8. **Statistical Audit #2** - Placeholder for post-analysis statistics-expert report
9. **Results** - Added by results-inspector agent
10. **Theoretical Implications** - Added by scholar agent after verified results

**IMPORTANT:** Template shows IRT+LMM as EXAMPLE. Adapt based on RQ's analysis type (CTT, correlation, ANOVA, regression, descriptive, etc.)

---

#### config.yaml Structure (Universal)

**Template:** `docs/templates/config_schema.yaml`

**Key Sections:**
- **Metadata:** RQ ID, analysis types
- **Analysis Parameters:** (adapt based on analysis_types)
  - IRT parameters (if using IRT)
  - LMM parameters (if using LMM)
  - CTT parameters (if using CTT)
  - etc.
- **Tool Function Mapping:** CRITICAL - explicit step-by-step pipeline:
  ```yaml
  tool_functions:
    step_1_[analysis_name]:
      function: "tools.module.function_name"
      input_file: "data/input.csv"
      output_files: ["data/output1.csv", "data/output2.csv"]
      config_section: "section_name"
  ```

**Purpose:** Eliminates ambiguity for analysis-executor - agent knows exactly which tool to call, what inputs to use, what outputs to create.

---

#### Master Actions

1. Invoke rq-spec agent with RQ number
2. Read `info.md` for overview
3. Read `logs/rq_spec_context.md` to understand agent's reasoning
4. **DO NOT proceed to validation yet**

**User Approval Gate:** None (draft only, validation comes next)

---

### Step 2: Scholar Validation

**Agent:** `scholar`
**Input:** RQ folder path (agent reads info.md directly)
**Output:** `validation/scholar_report.md`

---

#### What Happens

**Agent reads:**
- `info.md` (all sections)
- Searches literature (WebSearch, Context7) for 2020-2024 papers

**Agent validates:**
1. **Theoretical Grounding (3 pts):** Hypothesis aligns with episodic memory theory?
2. **Literature Support (2 pts):** Claims supported by recent literature?
3. **Interpretation Guidelines (2 pts):** Clear guidance for both confirmatory and null results?
4. **Theoretical Implications (2 pts):** RQ contributes to theory?
5. **Reviewer Rebuttals (1 pt):** Anticipated objections addressed?

**Agent outputs:**
- `validation/scholar_report.md` with:
  - Overall score (0-10)
  - Detailed feedback on each rubric item
  - Required changes (if score <9.25)
  - Suggested improvements
  - Citations to add (with full references)
  - Literature search results
  - Decision: APPROVED (≥9.25) / CONDITIONAL (9.0-9.24) / REJECTED (<9.0)

---

#### Master Actions

1. Invoke scholar agent with RQ folder path
2. Read `validation/scholar_report.md`
3. Check score:
   - **≥9.25:** Approved, proceed to Step 3
   - **9.0-9.24:** Conditional, minor changes needed, proceed to Step 3
   - **<9.0:** Rejected, iterate (return to Step 1)

4. **If iteration needed (<9.0):**
   - Present scholar feedback to user
   - Ask: "Iterate (rq-spec agent addresses issues) or Abort?"
   - If iterate: Re-invoke rq-spec agent (it will re-enter draft phase with feedback context)
   - Max 2 iterations, then user manual review

**User Approval Gate:** If score <9.0 and iteration required

**Quality Threshold:** ≥9.25/10 (gold standard), ≥9.0/10 (acceptable), <9.0 (rework required)

---

### Step 3: Statistics Expert Validation

**Agent:** `statistics_expert`
**Input:** RQ folder path (agent reads info.md and config.yaml)
**Output:**
- `validation/statistics_report.md`
- Updates `docs/tools_inventory.md` with RQ-tool mapping

---

#### What Happens

**Agent reads:**
- `info.md` (Method section, Validation section)
- `config.yaml` (all parameters)
- `docs/tools_inventory.md` (cross-reference available tools)

**Agent validates:**
1. **Statistical Appropriateness (3 pts):** Method matches research question and data structure?
2. **Tool Availability (2 pts):** All required tools exist in `tools/` package?
3. **Parameter Specification (2 pts):** Parameters clearly specified and justified?
4. **Validation Procedures (2 pts):** Assumptions explicitly checked, remedial actions specified?
5. **Complexity Assessment (1 pt):** Complexity justified by RQ, or unnecessarily complex?

**Agent outputs:**
- `validation/statistics_report.md` with:
  - Overall score (0-10)
  - Tool availability checklist (✅ Available / ⚠️ Missing)
  - Parameter appropriateness assessment
  - Validation procedure gaps
  - Complexity justification review
  - Required changes (if score <9.25)
  - Suggested improvements
  - Missing tools (if any - for master to implement)
  - Decision: APPROVED / CONDITIONAL / REJECTED

**Agent updates:**
- `docs/tools_inventory.md` appends RQ entry:
  ```markdown
  ### RQ X.Y - [RQ Title]
  **Tools Used:** tools.module.function1, tools.module.function2
  **Novel Usage:** [Any unique configurations]
  ```

---

#### Master Actions

1. Invoke statistics-expert agent with RQ folder path
2. Read `validation/statistics_report.md`
3. Check score (same logic as Step 2)
4. **If missing tools identified:**
   - Report to user: "Tool X needs implementation before proceeding"
   - User decides: Implement tool now, or modify RQ to use available tools
5. Verify `docs/tools_inventory.md` was updated

**User Approval Gate:** If score <9.0, or if missing tools require decision

---

### Step 4: Specification (Finalization Phase)

**Agent:** `rq_specification` (stateful - second invocation)
**Input:** RQ folder path (agent scans structure, reads prior context)
**Output:**
- Updated `info.md` (incorporates scholar/statistics feedback)
- Updated `logs/rq_spec_context.md` (appends finalization reasoning)
- `logs/rq_specification_report.md` (documents all changes made)
- Updated `status.md` (specification: complete, validation scores added)

---

#### Agent Behavior (Finalization Phase)

**On Invocation:**
1. **Scan folder structure:**
   - `logs/rq_spec_context.md` exists → Read prior context
   - Both validation reports exist → This is FINALIZATION phase

2. **Read prior context:**
   - Recall all decisions made in draft phase
   - Recall rationale for each choice
   - Recall open questions

3. **Review validation feedback:**
   - Read `validation/scholar_report.md` (score, required changes, suggestions)
   - Read `validation/statistics_report.md` (score, required changes, suggestions)

4. **Check for conflicts:**
   - Do scholar and statistics-expert give conflicting recommendations?
   - **If YES:** Report conflict to master → Master asks user to resolve
   - **If NO:** Proceed with incorporating all feedback

5. **Incorporate feedback:**
   - Make required changes to info.md
   - Make suggested improvements (if they enhance quality without major methodology changes)
   - Update config.yaml if parameters need adjustment
   - Update status.md with validation scores

6. **Document changes:**
   - Create `logs/rq_specification_report.md` listing all changes made
   - Append to `logs/rq_spec_context.md` with finalization reasoning
   - Explain why each change was made

---

#### Master Actions

1. Invoke rq-spec agent (it self-discovers this is finalization phase)
2. Read `logs/rq_specification_report.md` (review all changes)
3. Read updated `info.md` Status section (verify both scores ≥9.25)
4. **If conflicting feedback reported:**
   - Present conflict to user
   - User decides which recommendation to follow
   - Re-invoke rq-spec agent with decision
5. Prepare for Step 5 (safety audit)

**User Approval Gate:** If conflicting feedback requires manual resolution

---

### Step 5: Safety Audit (CRITICAL GATE)

**Phase:** Master performs hybrid validation (automated + user approval)
**Input:** Finalized `info.md`
**Output:** Audit report (ephemeral, presented to user)

---

#### What Happens (Hybrid Approach)

**Master performs automated checks on info.md Section 4 (Input Data):**

**Check 1: Data Preparation Section Structure**
- ✅ PASS: Section clearly separates:
  - A. "Data Sources for Data-Prep Agent" (RAW data from master.xlsx)
  - B. "Files Data-Prep Should Create" (input CSVs only)
  - C. "Files Data-Prep Should NOT Create" (derived data - analysis-executor creates)
- ❌ FAIL: Section lists IRT/LMM outputs as data-prep scope

**Check 2: Primary Source Declaration**
- ✅ PASS: "Primary Source: master.xlsx" with exact tags/columns
- ❌ FAIL: "Primary Source: IRT analysis output" or "LMM fitted values" or any DERIVED data

**Check 3: Variables Required List**
- ✅ PASS: All variables extractable from master.xlsx (DEM-*, COG-*, RVR-* tags)
- ❌ FAIL: Variables like "Theta_*", "ItemParameters", "ResidualMemory", "FittedValues" (require prior analysis)

**Check 4: Expected Dimensions Specified**
- ✅ PASS: info.md states expected dimensions explicitly (e.g., "400 rows, 37 columns")
- ❌ FAIL: No dimensions specified (can't validate data-prep outputs)

**Check 5: Analysis Pipeline Clear**
- ✅ PASS: Clear Step 1 (data-prep) → Step 2 (IRT/LMM/etc.) sequence in info.md Section 5 (Method)
- ❌ FAIL: Ambiguous workflow where data-prep creates analysis outputs

---

#### Master Actions

1. Run all 5 automated checks on info.md
2. Generate audit report:
   ```markdown
   ## Safety Audit Report: RQ X.Y
   **Status:** PROCEED / BLOCK
   **Checks Passed:** X/5

   **Check 1 (Data Prep Structure):** PASS/FAIL - [explanation]
   **Check 2 (Primary Source):** PASS/FAIL - [explanation]
   **Check 3 (Variables Required):** PASS/FAIL - [explanation]
   **Check 4 (Dimensions Specified):** PASS/FAIL - [explanation]
   **Check 5 (Analysis Pipeline):** PASS/FAIL - [explanation]

   **Recommendation:** [PROCEED - Safe to invoke data-prep] / [BLOCK - Fix info.md]
   **Rationale:** [Why]
   ```

3. Present audit report to user
4. **User reviews and decides:**
   - "PROCEED" → Continue to Step 6 (data-prep)
   - "BLOCK" → Fix info.md (return to Step 1 for iteration 3), or override with explanation

**User Approval Gate:** MANDATORY - User must confirm PROCEED or request fixes

**Purpose:** Prevent data-prep agent from generating mock theta scores, placeholder values, or other fake data

---

### Step 6: Data Preparation

**Agent:** `data_prep` v3.0 (with mock data prevention safety rules)
**Input:** RQ folder path (agent reads info.md Section 4, config.yaml not used)
**Output:**
- Input CSV(s) in `data/` (RAW data from master.xlsx)
- Companion .md for EVERY CSV
- `code/data_prep_script.py` (reproducible extraction script)
- `logs/data_prep_report.md`
- Updated `status.md`

---

#### What Happens

**Agent reads:**
- `info.md` Section 4 (Input Data) - executable specifications
- master.xlsx data file

**Agent executes:**
1. **Load master.xlsx**
2. **Extract variables by exact tags** (from info.md)
3. **Apply filters** (participant-level, item-level, value-level)
4. **Validate data quality:**
   - No empty columns (>30% missing)
   - Correct dimensions (matches info.md expected dimensions)
   - Proper UIDs (PXX_YY format)
   - Proper Test values (1, 2, 3, 4)
5. **Save outputs:**
   - CSV file(s) in `data/`
   - Companion .md for EACH CSV (6 required sections)
   - Extraction script in `code/data_prep_script.py`
   - Report in `logs/data_prep_report.md`

**CRITICAL SAFETY RULES (Embedded in Agent):**
- ❌ NEVER generate mock theta scores (logit transforms, calculations)
- ❌ NEVER create placeholder values for missing variables
- ❌ NEVER create "temporary" files "to be replaced later"
- ❌ NEVER simulate, randomize, or compute proxy data
- ✅ ONLY extract data from master.xlsx
- ✅ If required data doesn't exist → QUIT with status "failure", error type "MissingData"

**Agent outputs:**
- `logs/data_prep_report.md` with:
  - Status: SUCCESS / FAILURE
  - Execution steps (load, extract, filter, validate, save)
  - Data summary (descriptive statistics)
  - **Safety Verification section:** Did agent generate mock data? (MUST be NO)
  - Files created (list all CSVs + companion .md + script)
  - Next steps for analysis-executor

---

#### Master Actions

1. Invoke data-prep agent with RQ folder path
2. Wait for completion
3. Read `logs/data_prep_report.md`
4. Check status:
   - **SUCCESS:** Proceed to Step 7 (output verification)
   - **FAILURE:** Read error, determine fix:
     - Error type "MissingData" → Info.md confusion? Wait for prerequisite RQ?
     - Error type "CoreDocumentationBug" → Fix info.md tags, re-run
     - Error type "MissingTool" → Implement tool, re-run

**User Approval Gate:** None (unless failure requires decision)

**Circuit Breakers (Agent Quits If):**
- Required tags missing from master.xlsx
- Wrong tag format in info.md
- >30% empty values in extracted columns
- info.md requests DERIVED data (theta scores, fitted values, etc.)
- Tool function missing or raises unexpected error

---

### Step 7: Output Verification (CRITICAL GATE)

**Phase:** Master performs forensic inspection (automated + user approval)
**Input:** `logs/data_prep_report.md` + all files in `data/`
**Output:** Verification report (ephemeral, presented to user)

---

#### What Happens (Forensic Inspection)

**Master inspects all data-prep outputs:**

**Check 1: Files Created Match Report**
- ✅ PASS: All files listed in data_prep_report.md exist in `data/`
- ✅ PASS: No unexpected CSV files (no undocumented outputs)
- ❌ FAIL: Extra files found that aren't in report

**Check 2: Companion .md Files Exist**
- ✅ PASS: Every CSV has companion .md (e.g., irt_input.csv + irt_input.md)
- ❌ FAIL: Bare CSV without documentation

**Check 3: No Mock Data Keywords in .md Files**
- Master reads ALL .md files in `data/`
- Searches for: "mock", "placeholder", "temporary", "fake", "to be replaced", "simulated", "proxy"
- ✅ CLEAN: No suspicious keywords found
- ❌ CONTAMINATED: Keywords detected → MOCK DATA ALERT

**Check 4: Data Provenance Clear**
- ✅ PASS: .md files document extraction from master.xlsx with exact tags
- ❌ FAIL: .md files mention "calculated", "generated", "transformed" without clear master.xlsx source

**Check 5: File Sizes Reasonable**
- ✅ PASS: CSV dimensions match info.md expected dimensions (from Section 4)
- ❌ FAIL: File sizes inconsistent with extraction scope

---

#### Master Actions

1. Run all 5 forensic checks
2. Generate verification report:
   ```markdown
   ## Output Verification Report: RQ X.Y
   **Status:** CLEAN / CONTAMINATED
   **Checks Passed:** X/5
   **Files Inspected:** [list]

   **Check 1 (Files Match Report):** PASS/FAIL - [details]
   **Check 2 (Companion .md Files):** PASS/FAIL - [details]
   **Check 3 (No Mock Keywords):** PASS/FAIL - [keywords found, if any]
   **Check 4 (Data Provenance):** PASS/FAIL - [details]
   **Check 5 (File Sizes):** PASS/FAIL - [details]

   **Recommendation:** [PROCEED - Outputs clean] / [DELETE - Contamination detected]
   **Evidence:** [If contaminated, show specific examples]
   ```

3. Present verification report to user
4. **User reviews and confirms:**
   - "CLEAN" → Continue to Step 8 (analysis-executor)
   - "CONTAMINATED" → Delete all files in `data/`, fix info.md (return to Step 5), re-run data-prep

**User Approval Gate:** MANDATORY - User must confirm outputs are clean before analysis

**Purpose:** Detect mock data generation that safety audit missed, prevent fake data from entering analysis pipeline

---

### Step 8: Analysis Execution

**Agent:** `analysis_executor` v2.0 (strict tool-only, no improvisation)
**Input:** RQ folder path (agent reads info.md Section 5, config.yaml, data files)
**Output:**
- Output CSV(s) in `data/` (theta scores, item parameters, LMM coefficients, etc.)
- Companion .md for EVERY CSV
- Plots in `plots/` (with _data.csv for each plot)
- `code/analysis_script.py` (reproducible analysis script)
- `logs/analysis_executor_report.md`
- Updated `status.md`
- Updated `info.md` Section 6 (appends validation results)

---

#### What Happens

**Agent reads:**
- `info.md` Section 5 (Method) - step-by-step tool procedures
- `config.yaml` - parameters + tool_functions mapping
- Input files from `data/` (created by data-prep)

**Agent executes pipeline from config.yaml tool_functions:**

**Example (IRT + LMM pipeline):**
```yaml
tool_functions:
  step_1_irt_calibration:
    function: "tools.analysis_irt.calibrate_grm"
    input_file: "data/irt_input.csv"
    output_files: ["data/item_parameters.csv", "data/theta_scores.csv"]
    config_section: "irt"
```

**For each step:**
1. Load tool function (e.g., `tools.analysis_irt.calibrate_grm`)
2. Load input file
3. Load parameters from config_section
4. Execute function
5. Validate results (convergence, quality checks from info.md Section 6)
6. Save outputs (CSVs + companion .md)
7. If validation fails → Check if remedial action specified in info.md
8. If error occurs → Check if error is "expected" (handled) or "unexpected" (quit)

**After all analysis steps complete:**
- Generate plots (from config.yaml plots section)
- Save plots + plot_data.csv for each
- Append validation results to info.md Section 6
- Save analysis_script.py
- Save logs/analysis_executor_report.md

**CRITICAL SAFETY RULES (Embedded in Agent):**
- ❌ NEVER write custom functions (strict tool-only)
- ❌ NEVER improvise if tool missing (quit with "MissingTool" error)
- ❌ NEVER skip validation checks
- ✅ ONLY use functions from `tools/` package
- ✅ If unexpected error → QUIT, report to master

**Agent outputs:**
- `logs/analysis_executor_report.md` with:
  - Status: SUCCESS / FAILURE
  - Step-by-step execution log (each analysis step, convergence, quality checks)
  - Tool usage summary (which functions, versions, duration)
  - Validation results (assumptions tested, violations found)
  - Files created (all CSVs + plots + script)
  - Next steps for results-inspector

---

#### Master Actions

1. Invoke analysis-executor agent with RQ folder path
2. Wait for completion (IRT/LMM can take 2-10 minutes)
3. Read `logs/analysis_executor_report.md`
4. Check status:
   - **SUCCESS:** Proceed to Step 9 (results inspection) - but present results to user first
   - **FAILURE:** Read error, determine fix:
     - "MissingTool" → Implement tool, re-run
     - "ConvergenceFailure" → Check if fallback specified in info.md, or adjust parameters
     - "DataError" → Investigate data quality issue

**User Approval Gate:** User reviews final outputs before results-inspector validation

**Circuit Breakers (Agent Quits If):**
- Required tool doesn't exist in `tools/` package
- Tool raises unexpected error (not in expected_errors list)
- Input data malformed or missing required columns
- Model fails to converge after max iterations (and no fallback specified)
- Validation check fails critically (e.g., all assumptions violated)

---

### Step 9: Results Validation (Future Implementation)

**Agent:** `results_inspector` v1.0
**Input:** RQ folder path (agent reads all outputs)
**Output:**
- `logs/results_inspector_report.md`
- Updated `info.md` Section 9 (adds Results section)
- Updated `status.md`

---

#### What Happens (Planned)

**Agent inspects:**
- All data files (item_parameters, theta_scores, lmm_coefficients, etc.)
- All plots
- `logs/analysis_executor_report.md`
- `info.md` Section 6 (validation results)

**Agent validates:**
1. **Statistical Correctness:** Parameter ranges, p-values, effect sizes reasonable?
2. **Completeness:** All required outputs present?
3. **Interpretation Quality:** Answer to RQ aligns with results?
4. **Assumption Violations:** Were violations handled appropriately?
5. **Publication Readiness:** Results meet PhD thesis standards?

**Agent outputs:**
- `logs/results_inspector_report.md` with:
  - Status: APPROVED / CONDITIONAL / REJECTED
  - Statistical correctness validation
  - Completeness check
  - Interpretation quality assessment
  - Scholarly summary
  - Recommendations (required changes vs suggested improvements)
  - Decision on publication readiness

**Agent updates:**
- `info.md` Section 9 (Results) - adds scholarly summary of findings

---

#### Master Actions

**Status:** Not yet implemented (stub only)

**When implemented:**
1. Invoke results-inspector agent
2. Read report
3. If APPROVED → Proceed to Step 10 (theoretical implications)
4. If CONDITIONAL / REJECTED → Fix issues, re-run

**User Approval Gate:** User reviews results-inspector assessment

---

### Step 10: Theoretical Implications (Future)

**Agent:** `scholar` (second invocation)
**Input:** RQ folder path with completed results
**Output:**
- Updates `info.md` Section 10 (Theoretical Implications)
- `validation/scholar_theoretical_implications_report.md`

---

#### What Happens (Planned)

**Agent reads:**
- `info.md` Section 9 (Results) - verified findings
- `logs/results_inspector_report.md`
- All validation reports

**Agent writes:**
- Theoretical interpretation of results
- Alignment with episodic memory theory
- Contribution to literature
- Implications for REMEMVR assessment tool
- Future research directions
- Full citations

**Agent outputs:**
- `validation/scholar_theoretical_implications_report.md`
- Updates `info.md` Section 10

---

#### Master Actions

**Status:** Not yet implemented

**When implemented:**
1. Invoke scholar agent with "theoretical implications" mode
2. Read updated Section 10
3. User reviews for accuracy

---

### Step 11: Final Statistical Audit (Future)

**Agent:** `statistics_expert` (second invocation)
**Input:** RQ folder path with completed analysis
**Output:**
- `info.md` Section 8 (Statistical Audit #2) - appends report
- `validation/statistics_audit_post_analysis_report.md`

---

#### What Happens (Planned)

**Agent reads:**
- All analysis outputs
- `logs/analysis_executor_report.md`
- `info.md` Section 6 (validation results)

**Agent validates:**
- IRT convergence and item flagging correct?
- LMM assumption testing complete?
- Effect size calculations correct?
- Interpretation aligns with results?

**Agent outputs:**
- Post-analysis audit report
- Approval status: APPROVED / CONDITIONAL / REJECTED
- Conditions (if any) before results can be used

**Agent updates:**
- `info.md` Section 8 (Statistical Audit #2)

---

#### Master Actions

**Status:** Not yet implemented

**When implemented:**
1. Invoke statistics-expert agent with "post-analysis audit" mode
2. Read report
3. If APPROVED → RQ complete
4. If issues → Address before finalizing

---

## Safety Gates Summary

| **Gate** | **Type** | **When** | **Who Validates** | **Failure Action** |
|----------|----------|----------|-------------------|-------------------|
| Scholar Validation | Quality | After Step 1 | scholar agent | Iterate (max 2x) or user review |
| Statistics Validation | Quality | After Step 1 | statistics_expert agent | Iterate (max 2x) or user review |
| Safety Audit | Risk | After Step 4, before Step 6 | Master (hybrid) + User | User confirms PROCEED/BLOCK |
| Output Verification | Risk | After Step 6, before Step 8 | Master (forensic) + User | User confirms CLEAN/CONTAMINATED |
| User Confirmation | Control | After Steps 5, 7, 8 | User | Proceed or abort/fix |

---

## Output Validation Checklist

Use this checklist after EVERY RQ to verify completeness:

### Specification Phase (Steps 1-4)
- [ ] `info.md` exists with all 10 sections
- [ ] `config.yaml` exists with parameters + tool_functions mapping
- [ ] `status.md` exists with phase tracking
- [ ] `validation/scholar_report.md` exists with score ≥9.25
- [ ] `validation/statistics_report.md` exists with score ≥9.25
- [ ] `logs/rq_spec_context.md` exists (both draft and finalization sections)
- [ ] `logs/rq_specification_report.md` exists
- [ ] info.md Status section shows both validation scores

### Data Preparation Phase (Steps 5-7)
- [ ] Safety audit passed (5/5 checks)
- [ ] User confirmed PROCEED
- [ ] `data/` directory has input CSV(s)
- [ ] Every CSV has companion .md file
- [ ] `code/data_prep_script.py` exists
- [ ] `logs/data_prep_report.md` exists with status "success"
- [ ] Output verification passed (5/5 checks)
- [ ] User confirmed CLEAN
- [ ] No "mock", "placeholder", "temporary" keywords in any .md file

### Analysis Phase (Step 8)
- [ ] `data/` directory has output CSVs (theta_scores, item_parameters, lmm_coefficients, etc.)
- [ ] `plots/` directory has all required plots
- [ ] Every output CSV has companion .md file
- [ ] Every plot has _data.csv file
- [ ] `code/analysis_script.py` exists
- [ ] `logs/analysis_executor_report.md` exists with status "success"
- [ ] info.md Section 6 has validation results appended
- [ ] User reviewed and confirmed analysis complete

### Results Phase (Steps 9-11) - Future
- [ ] `logs/results_inspector_report.md` exists with status "approved"
- [ ] info.md Section 9 (Results) complete
- [ ] info.md Section 10 (Theoretical Implications) complete
- [ ] info.md Section 8 (Statistical Audit #2) complete

---

## Status Tracking Schema

**File:** `status.md` (Markdown format, human-readable)

**Structure:**
```markdown
# RQ Status: X.Y - [RQ Title]

**Last Updated:** YYYY-MM-DD HH:MM

## Phase Status

| **Phase** | **Status** | **Score** | **Date** |
|-----------|-----------|----------|----------|
| Specification | complete / in_progress / not_started | - | YYYY-MM-DD |
| Scholar Validation | passed / failed / not_started | 9.5/10 | YYYY-MM-DD |
| Statistics Validation | passed / failed / not_started | 9.3/10 | YYYY-MM-DD |
| Safety Audit | proceed / block / not_started | - | YYYY-MM-DD |
| Data Preparation | success / failure / not_started | - | YYYY-MM-DD |
| Output Verification | clean / contaminated / not_started | - | YYYY-MM-DD |
| Analysis Execution | success / failure / not_started | - | YYYY-MM-DD |
| Results Validation | complete / not_started | - | YYYY-MM-DD |

## Notes

[Any issues, decisions, or blockers]
```

---

## Quality Metrics

Track these metrics across all 50 RQs:

**Specification Quality:**
- Average scholar score (target: ≥9.37 from Phase 7)
- Average statistics score (target: ≥9.37 from Phase 7)
- % RQs requiring iteration (target: <20%)
- % RQs achieving gold standard ≥9.25 (target: ≥93%)

**Data Preparation Quality:**
- % RQs where data-prep succeeds first attempt (target: ≥90%)
- % RQs requiring info.md fixes (target: <10%)
- % RQs blocked by safety audit (target: <5% after initial fixes)
- % RQs with contaminated outputs (target: 0% - ZERO TOLERANCE)

**Analysis Execution Quality:**
- % RQs where analysis-executor succeeds first attempt (target: ≥80%)
- % RQs requiring tool additions (target: <5%)
- % RQs with convergence issues (target: <10%)

---

## File Format Standards

### All Reports: Markdown (.md)

**Why Markdown:**
- Human-readable (thesis-appropriate)
- Version control friendly (git diffs work)
- Easy to search (grep, text editors)
- Can embed tables, code blocks, math
- Thesis examiners can read directly

**NOT JSON:**
- JSON is machine-readable but human-hostile
- Poor for documentation and audit trails
- Hard to review in git diffs
- Inappropriate for PhD thesis artifacts

### All Data: CSV with Companion .md

**CSV:** Actual data values
**Companion .md:** Documents data structure, methodology, quality, provenance

**Example:**
- `theta_scores.csv` - The actual theta values
- `theta_scores.md` - How they were calculated, what they mean, quality checks, next steps

---

## Version History

**v3.0 (2025-11-12):**
- Added stateful rq-spec agent with context dumps (logs/rq_spec_context.md)
- Changed all reports from JSON to Markdown
- Added hybrid safety audits (automated checks + user approval)
- Added forensic output verification (keyword scanning, provenance checks)
- Clarified analysis-executor instructions via config.yaml tool_functions
- Made templates universal (not locked to IRT/LMM)
- Added explicit file format standards
- Incorporated all ultrathink analysis clarifications

**v2.0 (2025-11-12):**
- Added Step 5: Safety Audit
- Added Step 7: Output Verification
- Added user approval gates at critical risk points
- Added contamination detection with zero-tolerance policy
- Updated to reflect data-prep v3.0 safety rules

**v1.0 (2025-01-11):**
- Original 6-step workflow (docs/rq_workflow.md)
- No safety audits or output verification
- Led to RQ 5.5 mock data catastrophe (2025-11-12)

---

**End of Standard Procedure v3.0**
