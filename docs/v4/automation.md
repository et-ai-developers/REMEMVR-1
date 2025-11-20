# V4.X Master Orchestration Workflow

**File:** automation.md
**Location:** docs/v4/
**Last Updated:** 2025-11-16
**Purpose:** Complete 17-step RQ pipeline workflow for master orchestration
**Audience:** Master (main claude) reads at step 2 before executing each RQ
**Version:** 4.X (atomic agent architecture)

---

## Overview

This document specifies the complete 17-step workflow for executing any Research Question (RQ) using the v4.X atomic agent architecture. The workflow covers:

- **Setup & Structure:** Creating RQ folder and initial files (steps 1-3)
- **Concept Validation:** Extracting and validating RQ concept (steps 4-6)
- **User Approval Gate:** Single approval point after concept validation (step 7)
- **Planning & Specification:** Creating analysis plan and tool specifications (steps 8-13)
- **Code Execution Loop:** Systematic code generation, execution, debugging, and validation (step 14)
- **Results Generation:** Plotting and summary creation (steps 15-17)

**Critical Design Principles:**
- Single user approval gate (step 7) prevents workflow fragmentation
- status.yaml pseudo-statefulness enables continuity across agents
- CODE EXECUTION LOOP with g_debug integration provides systematic error recovery
- Validation gates at steps 10, 13, and embedded in step 14 prevent cascading errors

---

## Complete 17-Step Workflow

### Steps 1-7: Setup & Concept Validation

#### Step 1: User Request
**User:** "Begin chX/rqY"

**Master Actions:**
- User initiates new RQ
- Master prepares to orchestrate workflow

---

#### Step 2: Read Automation Workflow
**Master reads:** `docs/v4/automation.md` (this file)

**Purpose:**
- Refresh memory on complete 17-step workflow sequence
- Know agent invocation format (descriptive strings)
- Remember user approval gate location (step 7)
- Understand CODE EXECUTION LOOP logic
- Recall error handling procedures

**Master Actions:**
- Read this file completely
- Prepare to execute steps 3-17 sequentially

---

#### Step 3: Build RQ Folder Structure
**Master invokes:** rq_builder with "Build chX/rqY"

**Agent:** rq_builder
**Reads:** agent_best_practices.md, build_folder.md, build_status.md
**Writes:** results/chX/rqY/ folder structure, status.yaml

**Master Actions:**
- Invoke rq_builder agent with RQ identifier
- Wait for success report
- Verify folder structure created

**Expected Output:**
- results/chX/rqY/ folder with 6 subfolders (docs/, data/, code/, logs/, plots/, results/)
- status.yaml initialized with 10 RQ-specific agents (all pending)

---

#### Step 4: Create Concept Document
**Master invokes:** rq_concept with "Create 1_concept.md"

**Agent:** rq_concept
**Reads:** agent_best_practices.md, status.yaml, concept.md template, thesis/ANALYSES_CHX.md
**Writes:** 1_concept.md, status.yaml (rq_concept success + context_dump)

**Master Actions:**
- Invoke rq_concept agent
- Wait for success report
- Agent extracts RQ from thesis, maps to concept template

**Expected Output:**
- results/chX/rqY/docs/1_concept.md created
- status.yaml updated (rq_concept = success)

---

#### Step 5: Scholarly Validation
**Master invokes:** rq_scholar with "Inspect 1_concept.md"

**Agent:** rq_scholar
**Reads:** agent_best_practices.md, status.yaml, scholar_report.md template, 1_concept.md
**Writes:** 1_concept.md (appends scholarly feedback via Edit tool), status.yaml (rq_scholar success + context_dump)

**Master Actions:**
- Invoke rq_scholar agent
- Wait for validation report
- Agent uses WebSearch to validate theoretical claims

**Expected Output:**
- 1_concept.md updated with scholarly feedback appended
- status.yaml updated (rq_scholar = success)

---

#### Step 6: Statistical Validation
**Master invokes:** rq_stats with "Inspect 1_concept.md"

**Agent:** rq_stats
**Reads:** agent_best_practices.md, status.yaml, stats_report.md template, 1_concept.md
**Writes:** 1_concept.md (appends statistical feedback via Edit tool), status.yaml (rq_stats success + context_dump)

**Master Actions:**
- Invoke rq_stats agent
- Wait for validation report
- Agent validates statistical methods appropriateness

**Expected Output:**
- 1_concept.md updated with statistical feedback appended
- status.yaml updated (rq_stats = success)

---

#### Step 7: User Approval Gate
**Master asks user:** "Verify results/chX/rqY/docs/1_concept.md"

**Purpose:**
- Single approval point after concept validation
- User verifies scholarly and statistical feedback incorporated correctly
- User confirms RQ concept before proceeding to planning/execution

**Master Actions:**
- Prompt user to review 1_concept.md
- Wait for user response

**User Options:**
- **Approve:** "Looks good. Continue" → Proceed to step 9
- **Request Changes:** User specifies needed changes → Loop back to step 4 (rq_concept)

**Critical Design Note:**
- This is the ONLY user approval gate in the workflow
- v3.0 had multiple approval points, caused workflow fragmentation
- v4.X uses single gate at critical decision point + automated validation (g_conflict steps 10 & 13, rq_inspect per analysis step)

---

### Steps 8-13: Planning & Specification

#### Step 8: User Approval Response
**User responds:** "Looks good. Continue" (or requests changes)

**Master Actions:**
- If approved: Proceed to step 9
- If changes requested: Return to step 4 with user feedback

---

#### Step 9: Create Analysis Plan
**Master invokes:** rq_planner with "Create 2_plan.md"

**Agent:** rq_planner
**Reads:** agent_best_practices.md, status.yaml, plan.md template, 1_concept.md, data_structure.md, tool_inventory.md, names.md
**Writes:** 2_plan.md, status.yaml (rq_planner success + context_dump)

**Master Actions:**
- Invoke rq_planner agent
- Wait for plan creation report

**Expected Output:**
- results/chX/rqY/docs/2_plan.md created with step-by-step analysis plan
- Validation requirements stated: "Validation tools MUST be used after analysis tool execution"
- status.yaml updated (rq_planner = success)

---

#### Step 10: Conflict Detection (Concept vs Plan)
**Master invokes:** g_conflict with "Compare 1_concept.md, 2_plan.md"

**Agent:** g_conflict (general-purpose)
**Reads:** agent_best_practices.md, specified documents (1_concept.md, 2_plan.md)
**Writes:** None (report only)

**Master Actions:**
- Invoke g_conflict with document paths
- Review conflict report
- If conflicts found: Address conflicts (may require rq_planner re-run)
- If no conflicts: Proceed to step 11

**Expected Output:**
- Conflict report with count and line numbers
- 0 conflicts expected for well-formed concept and plan

---

#### Step 11: Create Tool Specifications
**Master invokes:** rq_tools with "Create 3_tools.yaml"

**Agent:** rq_tools
**Reads:** agent_best_practices.md, status.yaml, tools.md template, 2_plan.md, tool_inventory.md (with validation tools), names.md
**Writes:** 3_tools.yaml, status.yaml (rq_tools success + context_dump)

**Master Actions:**
- Invoke rq_tools agent
- Wait for tool specification report

**Expected Output:**
- results/chX/rqY/docs/3_tools.yaml created
- BOTH analysis and validation tool pairs specified per step
- Full signatures with type hints from tool_inventory.md
- status.yaml updated (rq_tools = success)

**Expected TDD Failure (First RQ Only):**
- names.md starts empty (TDD approach per spec section 4.5.1)
- rq_tools will fail at names.md lookup for step naming conventions
- Master and user manually add required naming conventions to names.md
- Retry rq_tools succeeds

---

#### Step 12: Create Analysis Specifications
**Master invokes:** rq_analysis with "Create 4_analysis.yaml"

**Agent:** rq_analysis
**Reads:** agent_best_practices.md, status.yaml, analysis.md template, 2_plan.md, 3_tools.yaml, names.md
**Writes:** 4_analysis.yaml, status.yaml (rq_analysis success + analysis_steps section + context_dump)

**Master Actions:**
- Invoke rq_analysis agent
- Wait for analysis specification report

**Expected Output:**
- results/chX/rqY/docs/4_analysis.yaml created
- BOTH analysis tool call AND validation tool call per step
- Each step MUST end with validation tool call (prevents cascading errors)
- status.yaml updated (rq_analysis = success, analysis_steps section created with all steps pending)

---

#### Step 13: Conflict Detection (Plan vs Tools vs Analysis)
**Master invokes:** g_conflict with "Compare 2_plan.md, 3_tools.yaml, 4_analysis.yaml"

**Agent:** g_conflict (general-purpose)
**Reads:** agent_best_practices.md, specified documents (2_plan.md, 3_tools.yaml, 4_analysis.yaml)
**Writes:** None (report only)

**Master Actions:**
- Invoke g_conflict with document paths
- Review conflict report
- If conflicts found: Address conflicts (may require agent re-runs)
- If no conflicts: Proceed to step 14

**Expected Output:**
- Conflict report with count and line numbers
- 0 conflicts expected for well-formed plan, tools, and analysis specifications

---

### Step 14: Code Execution Loop

**Purpose:** Generate, execute, debug, and validate all analysis steps systematically

**Overview:** For each step in status.yaml analysis_steps section (step01, step02, ..., stepN), master orchestrates a 9-sub-step process:

---

#### CODE EXECUTION LOOP (9 Sub-Steps Per Analysis Step)

**Loop Entry Condition:**
- status.yaml analysis_steps section has pending steps
- Previous step marked success (or first step)

**For Each Analysis Step N:**

##### Sub-Step 1: Status Check
**Master checks:** status.yaml analysis_steps section

**Purpose:**
- Determine which step is next (pending status)
- Verify previous steps marked success
- Track loop progress

**Master Actions:**
- Read status.yaml
- Identify next pending step (stepN)

---

##### Sub-Step 2: Code Generation
**Master invokes:** g_code with "Generate code for step N"

**Master Provides to g_code (General-Purpose Agent):**
- 4_analysis.yaml path (step_N specification)
- Output code path (results/chX/rqY/code/stepN_name.py)
- Log path (results/chX/rqY/logs/stepN_name.log)
- tool_inventory.md path (for validation of signatures)

**Agent:** g_code (general-purpose)
**Reads:** agent_best_practices.md, specified documentation (4_analysis.yaml step_N, tool_inventory.md, etc.)
**Writes:** stepN_name.py

**Critical 4-Layer Pre-Generation Validation:**
1. **4a: Import Check** - All imports available in environment
2. **4b: Signature Check** - All function signatures match tool_inventory.md exactly
3. **4c: Input File Check** - All input files exist at specified paths
4. **4d: Column Check** - All required columns present in input data

**Master Actions:**
- Invoke g_code with complete specification
- Wait for code generation report
- If g_code reports validation failure: QUIT with circuit breaker error, fix specification/data
- If g_code reports success: Proceed to sub-step 3

**Expected Output:**
- results/chX/rqY/code/stepN_name.py created
- Code includes BOTH analysis tool call AND validation tool call (per 4_analysis.yaml)
- All 4 validation layers passed

---

##### Sub-Step 3: Code Execution
**Master runs:** `bash "poetry run python results/chX/rqY/code/stepN_name.py"`

**Purpose:**
- Execute generated code in poetry environment
- Capture output and errors
- Detect execution failures (tracebacks)

**Master Actions:**
- Run bash command with poetry run prefix
- Monitor output for tracebacks
- If traceback detected: Proceed to sub-step 4 (debugging)
- If no traceback: Proceed to sub-step 8 (validation)

**Expected Outputs (Success Case):**
- Analysis step completes without errors
- Output files created per 4_analysis.yaml specification
- Validation tool passes (embedded at end of step)
- Log file written to results/chX/rqY/logs/stepN_name.log

**Expected Failures (TDD Philosophy):**
- Validation tool failures in early runs (TDD for validation tools)
- API mismatches despite g_code 4-layer validation (edge cases)
- Data format issues discovered at runtime
- 5-10 iterations normal for first RQ

---

##### Sub-Step 4: Error Detection & Debugging
**If traceback:** Master invokes: g_debug with "Debug step N"

**Master Provides to g_debug:**
- Code path (results/chX/rqY/code/stepN_name.py)
- Log path (results/chX/rqY/logs/stepN_name.log with traceback)
- Error context (which step, what failed)

**Agent:** g_debug (general-purpose)
**Reads:** agent_best_practices.md, code/logs to debug
**Writes:** Sandbox files (temporary, deleted after debugging)

**g_debug Process:**
1. Read code and log with traceback
2. Create sandbox copy (results/chX/rqY/code/.sandbox/)
3. Test fix in sandbox
4. Verify fix works in sandbox
5. Delete sandbox
6. Report: Root cause + solution + improvement suggestions

**Master Actions:**
- Invoke g_debug
- Wait for debugging report
- Review root cause and solution
- Proceed to sub-step 5

**Expected Output:**
- Debugging report with:
  - Root cause (what caused the error)
  - Solution (specific fix to apply)
  - Improvement suggestions (how to prevent recurrence)
- NO persistent changes (sandbox deleted, master applies fix)

---

##### Sub-Step 5: Fix Application
**If g_debug reports solution:** Master applies fix to code OR templates

**Purpose:**
- Apply g_debug's reported solution
- Master understands and implements fix (not black-box)
- Fix may be to code (stepN_name.py) OR templates (if specification error)

**Master Actions:**
- Read g_debug solution
- Determine fix location (code vs templates vs agent prompts)
- Apply fix using Edit tool
- Explain fix to user (learning opportunity)

**Fix Locations:**
- **Code:** results/chX/rqY/code/stepN_name.py (most common)
- **Templates:** 4_analysis.yaml, 3_tools.yaml, 2_plan.md (if specification error)
- **Agent Prompts:** .claude/agents/*.md (if agent made systematic error)
- **Data:** Input files (if data format issue)

**Expected Fixes:**
- API signature corrections (wrong parameter names/order)
- Column name corrections (typos in column references)
- File path corrections (wrong paths in code)
- Validation criteria adjustments (validation too strict/loose)

---

##### Sub-Step 6: Re-Run Verification (CRITICAL)
**Master re-runs:** `bash "poetry run python results/chX/rqY/code/stepN_name.py"` (verify fix works)

**Purpose:**
- Verify g_debug's fix actually resolves the error
- Confirm traceback gone before proceeding
- Prevent moving forward with unverified solutions

**Master Actions:**
- Run exact same bash command as sub-step 3
- Monitor output for tracebacks
- If traceback still present: Return to sub-step 4 (g_debug again)
- If no traceback: Proceed to sub-step 8 (validation)

**Critical Design Note (Added Post-Ultrathink Issue #1):**
- v3.0 didn't have this re-run verification step
- Led to cascading errors (moved forward with unverified fixes)
- v4.X REQUIRES re-run verification before invoking rq_inspect
- ONLY proceed to sub-step 8 after confirmed successful execution

---

##### Sub-Step 7: Iterative Debugging
**If still fails:** Repeat sub-steps 4-6 until success (g_debug → fix → re-run cycle)

**Purpose:**
- Handle complex errors requiring multiple iterations
- Systematic approach: debug → fix → verify → repeat if needed
- Eventually reach success (all errors resolvable)

**Master Actions:**
- If re-run still shows traceback: Return to sub-step 4
- Invoke g_debug with updated context (previous fixes attempted)
- Apply new fix
- Re-run verification
- Repeat until success

**Expected Iterations:**
- Simple errors: 1 iteration (single g_debug → fix → re-run succeeds)
- Complex errors: 2-3 iterations (multiple rounds)
- First RQ: 5-10 iterations total across all steps (TDD discovery process)
- Later RQs: 1-2 iterations total (system stabilized)

---

##### Sub-Step 8: Output Validation
**After successful execution:** Master invokes: rq_inspect with "Validate step N outputs"

**Agent:** rq_inspect
**Reads:** agent_best_practices.md, status.yaml, inspect_criteria.md template, 2_plan.md, step output files
**Writes:** status.yaml (analysis step N success + context_dump)

**Master Actions:**
- Invoke rq_inspect ONLY after successful code execution (no traceback)
- Wait for validation report
- rq_inspect validates outputs match 2_plan.md expectations

**Expected Output:**
- Validation report confirming outputs correct
- status.yaml updated (stepN marked success in analysis_steps section)
- rq_inspect context_dump updated

**Validation Checks:**
- Input files existed and correct format
- Output files created and correct format
- Data formats match expectations
- Results align with plan.md specifications

---

##### Sub-Step 9: Status Update & Loop Progress
**Master updates:** status.yaml (mark step N success, move to N+1)

**Purpose:**
- Track progress through analysis steps
- Determine loop continuation (more pending steps?) or exit (all success?)

**Master Actions:**
- Verify status.yaml updated by rq_inspect (stepN = success)
- Check for next pending step (stepN+1)
- If more pending steps: Return to sub-step 1 (next step)
- If all steps success: Exit loop, proceed to step 15

**Loop Exit Condition:**
- All steps in status.yaml analysis_steps section marked success
- No pending steps remaining

---

**End of CODE EXECUTION LOOP**

---

### Steps 15-17: Results Generation

#### Step 15: Create Plotting Script
**Master invokes:** rq_plots with "Create plots.py"

**Agent:** rq_plots
**Reads:** agent_best_practices.md, status.yaml, plots.md template, tools/plots.py (source code), data files
**Writes:** plots.py, status.yaml (rq_plots success + context_dump)

**Master Actions:**
- Invoke rq_plots agent
- Wait for plotting script creation report

**Expected Output:**
- results/chX/rqY/plots/plots.py created
- Script calls ONLY existing functions from tools/plots.py (NEVER creates new functions)
- Consistent plot themes across all RQs (rq_plots reads source code for this)
- status.yaml updated (rq_plots = success)

**Expected TDD Failure (First RQ Only):**
- Missing plot functions in tools/plots.py
- rq_plots will fail if needed function doesn't exist (per spec)
- Master and user manually add missing plot functions to tools/plots.py
- Retry rq_plots succeeds

---

#### Step 16: Execute Plotting Script
**Master runs:** `bash "poetry run python results/chX/rqY/plots/plots.py"`

**Purpose:**
- Generate all plots for RQ
- Save plots as PNG files

**Master Actions:**
- Run bash command with poetry run prefix
- Monitor output for errors
- Verify plots created

**Expected Output:**
- All plots saved to results/chX/rqY/plots/ (PNG format)
- Consistent formatting across plots (themes from tools/plots.py)

---

#### Step 17: Create Results Summary
**Master invokes:** rq_results with "Create summary.md"

**Agent:** rq_results
**Reads:** agent_best_practices.md, status.yaml, results.md template, result files (data/, plots/)
**Writes:** summary.md, status.yaml (rq_results success + context_dump)

**Master Actions:**
- Invoke rq_results agent
- Wait for summary creation report
- RQ complete

**Expected Output:**
- results/chX/rqY/results/summary.md created
- Contains: Statistical findings, plot descriptions, interpretation, limitations, next steps
- Publication-ready summary
- status.yaml updated (rq_results = success)

**RQ Complete:**
- All 17 steps executed successfully
- All agents in status.yaml marked success
- All analysis steps completed and validated
- Plots generated and summary written
- Ready for user review

---

## Error Handling Procedures

### g_debug Integration (CODE EXECUTION LOOP)

**When to Use g_debug:**
- Traceback detected during code execution (sub-step 3)
- Master invokes g_debug in sub-step 4
- g_debug creates sandbox, tests fix, reports solution
- Master applies fix in sub-step 5
- Master re-runs code in sub-step 6 to verify fix works

**g_debug Process:**
1. **Sandbox Creation:** g_debug copies code to .sandbox/ directory
2. **Debugging:** g_debug tests fix in sandbox (no changes to original files)
3. **Solution Report:** g_debug reports root cause + solution + improvement suggestions
4. **Sandbox Deletion:** g_debug deletes .sandbox/ (no persistent changes)
5. **Master Applies Fix:** Master implements solution in original code/templates (NOT black-box)

**Why This Approach:**
- Master understands every fix (learning opportunity for user)
- No black-box changes to code (prevents hidden bugs)
- Systematic error recovery (reproducible debugging process)
- Enables agent/template improvements (g_debug suggests improvements)

---

### Circuit Breakers (Agent Error Handling)

**5 Circuit Breaker Types (from agent_best_practices.md):**

1. **EXPECTATIONS:** Prior steps not success → QUIT
2. **STEP:** Can't determine step number → QUIT
3. **TOOL:** Function doesn't exist in tool_inventory.md → QUIT
4. **CLARITY:** Ambiguous specification → QUIT
5. **SCOPE:** Data source unclear (RAW vs DERIVED) → QUIT

**When Agent Reports Circuit Breaker:**
- Master identifies root cause (which circuit breaker triggered)
- Master fixes underlying issue (specification error, missing data, etc.)
- Master re-runs agent after fix applied
- System-level error (not code error) - requires master intervention

---

### Error Recovery Workflow

**For Code Execution Errors (Tracebacks):**
1. g_debug → fix → re-run → verify (iterative until success)
2. Update agent prompts/templates if systematic error discovered
3. Document lessons learned (prevents recurrence)

**For Circuit Breaker Errors (Agent Quits):**
1. Identify which circuit breaker triggered
2. Fix root cause (specification, data, clarity)
3. Re-run agent after fix
4. Update agent_best_practices.md if new circuit breaker pattern discovered

**For Validation Failures (rq_inspect Reports Error):**
1. Review outputs vs plan.md expectations
2. Determine if code error (fix code) or plan error (fix plan)
3. Re-run analysis step after fix
4. Update validation criteria if too strict/loose

---

## Status Tracking Checkpoints

### status.yaml Structure

**Agent Steps Section:**
- 10 RQ-specific agents (rq_builder, rq_concept, rq_scholar, rq_stats, rq_planner, rq_tools, rq_analysis, rq_inspect, rq_plots, rq_results)
- Each agent has: status (pending/success), context_dump (multiline string)
- General-purpose agents (g_code, g_conflict, g_debug) NOT tracked in status.yaml

**Analysis Steps Section:**
- Created by rq_analysis in step 12
- Contains: step01, step02, ..., stepN (one per analysis step)
- Each step has: status (pending/success)
- Updated by rq_inspect in CODE EXECUTION LOOP sub-step 8

---

### Master Reads status.yaml

**When Master Reads:**
- Before invoking each agent (verify prior steps success)
- CODE EXECUTION LOOP sub-step 1 (determine next pending step)
- After agent completes (verify agent updated status)

**What Master Checks:**
- Agent steps: Which agents completed (success), which pending
- Analysis steps: Which analysis steps completed, which next
- Continuity: Previous step success before starting next step

---

### Agents Update status.yaml

**When Agents Update:**
- After completing their work (mark self as success)
- Context dump: Terse 5-line summary of what was done

**Context Dump Format:**
```
context_dump: |
  RQ: ch5/rq1 - Trajectory of forgetting (Free Recall)
  Domains: Free Recall (FR)
  Approach: IRT→LMM with TSVR time variable
  Data: RVR-FR-D0-T{1-5}, RVR-FR-D{1,3,6}-T1 (purify→theta→LMM)
  Status: Plan created with 4 steps (calibration, purification, theta, trajectory)
```

**Pseudo-Statefulness:**
- Agents read status.yaml to know prior agent results
- Agents write context_dump for downstream agents
- Enables continuity without context bloat (stateless agents with state file)

---

## Usage Notes

### When Master Reads This File

**Frequency:** At step 2 of EVERY RQ (all 50 RQs)

**Purpose:**
- Refresh memory on complete workflow before starting RQ
- Ensure consistent orchestration across all RQs
- Prevent workflow drift or forgotten steps

**What to Focus On:**
- 17-step sequence (know what's next at each step)
- CODE EXECUTION LOOP 9 sub-steps (most complex part)
- User approval gate location (step 7 only)
- Error handling procedures (g_debug integration)

---

### Phase 1 vs Phase 2 Orchestration

**Phase 1: Manual (Current - Development/Testing)**
- Master (main claude) executes workflow steps 1-17 sequentially
- Master reads this file, invokes agents manually
- Handles each agent response individually
- Responds to errors immediately
- Used during v4.X development and RQ 5.1 testing

**Phase 2: Automated (Future - Production Efficiency)**
- Orchestrator script reads this file programmatically
- Invokes agents sequentially per workflow
- Handles CODE EXECUTION LOOP logic automatically
- Integrates g_debug error recovery
- Specified in: docs/v4/orchestrator.md

**Both Modes Available:**
- Manual: Debugging flexibility, step-by-step control (learning)
- Automated: Efficiency after system stabilizes (production)

---

### Expected Failures (TDD Philosophy)

**First RQ (RQ 5.1) Expected Failures:**

1. **Step 11 (rq_tools):** names.md empty → Fail at naming convention lookup → Master and user manually populate names.md → Retry succeeds

2. **Step 14 (CODE EXECUTION LOOP):**
   - g_code 4-layer validation may fail (API mismatches, missing files, wrong columns)
   - Script execution may fail (validation tool failures expected in early runs)
   - 5-10 g_debug iterations normal for first RQ
   - Validation criteria may need refinement

3. **Step 15 (rq_plots):** Missing plot functions in tools/plots.py → Fail per spec → Master and user add missing functions → Retry succeeds

**Subsequent RQs (After RQ 5.1):**
- names.md populated (no step 11 failure)
- Validation tools stabilized (fewer step 14 iterations)
- Plot functions complete (no step 15 failure)
- 1-2 iterations total (system learned from RQ 5.1)

**TDD Success Criteria:**
- Failures are EXPECTED and HEALTHY (discovery process)
- Each failure improves system (add conventions, fix validation, add functions)
- Iteration is SUCCESS not failure (learning and improvement)

---

### Workflow Consistency

**Critical for All 50 RQs:**
- Master MUST follow this workflow exactly for EVERY RQ
- No shortcuts, no skipped steps
- Consistent agent invocation format
- Consistent error handling procedures

**Benefits:**
- Prevents workflow drift across RQs
- Ensures quality consistency
- Enables systematic improvement (patterns visible across RQs)
- Facilitates debugging (predictable execution path)

---

**End of Master Orchestration Workflow**

**Version:** V4.X (atomic agent architecture)
**Specification Reference:** docs/user/analysis_pipeline_solution.md section 3.1 (17-step workflow), section 4.5.4 (automation.md spec)
**Last Updated:** 2025-11-16
