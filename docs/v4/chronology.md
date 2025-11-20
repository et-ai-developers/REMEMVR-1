# V4.X Agent Document Chronology

**Version:** 4.0
**Last Updated:** 2025-11-21
**Purpose:** Complete chronological audit trail of ALL documents read by ALL 13 agents in execution order
**Audience:** Quality control - audit each document for bloat/hallucinations/contradictions
**Status:** VALIDATED (comprehensive mapping of solution.md workflow)

---

## HOW TO USE THIS DOCUMENT

**Purpose:** This chronology provides a complete audit trail of document dependencies for the v4.X atomic agent architecture.

**For Quality Control:**
- Trace which documents each agent reads
- Identify potential context bloat issues
- Detect circular dependencies
- Validate document scope (agents should read <5k tokens)

**For Debugging:**
- When agent fails, check what it should have read
- Verify all expected documents exist
- Confirm document contents match agent expectations

**For Development:**
- Update when modifying agent workflows
- Add new document reads when agent prompts change
- Verify changes don't violate <5k context constraint

**Legend:**
- [R] = Read by agent
- [W] = Written by agent
- [U] = Updated/edited by agent

---

## PHASE 1: MANUAL RQ SETUP (USER-DRIVEN)

### Agent 1: rq_builder
**Solution.md Reference:** Section 2.1.1
**Purpose:** Create blank RQ folder structure + status.yaml
**Context Budget:** ~2k tokens

**Documents Read (Execution Order):**
1. [R] .claude/agents/rq_builder.md - Agent prompt
2. [R] docs/v4/best_practices/universal.md - Circuit breakers, platform rules
3. [R] docs/v4/templates/build_folder.md - Folder structure specification
4. [R] docs/v4/templates/build_status.md - status.yaml template with 10 agent sections

**Documents Written:**
- [W] results/chX/rqY/status.yaml - Initial YAML with 10 agents (rq_builder, rq_concept, rq_scholar, rq_stats, rq_planner, rq_tools, rq_analysis, rq_inspect, rq_plots, rq_results)
- [W] results/chX/rqY/docs/.gitkeep
- [W] results/chX/rqY/data/.gitkeep
- [W] results/chX/rqY/code/.gitkeep
- [W] results/chX/rqY/logs/.gitkeep
- [W] results/chX/rqY/plots/.gitkeep
- [W] results/chX/rqY/results/.gitkeep

**Report:** "Successfully built results/chX/rqY/ structure with status.yaml"

---

### Agent 2: rq_concept
**Solution.md Reference:** Section 2.1.2
**Purpose:** Extract RQ concept from thesis, format per template
**Context Budget:** ~3-4k tokens

**Documents Read (Execution Order):**
1. [R] .claude/agents/rq_concept.md - Agent prompt
2. [R] docs/v4/best_practices/universal.md - Circuit breakers, platform rules
3. [R] docs/v4/best_practices/workflow.md - Status YAML, context dumps
4. [R] results/chX/rqY/status.yaml - Check prior steps (all should be pending except rq_builder = success)
5. [R] docs/v4/templates/concept.md - 1_concept.md structure specification
6. [R] docs/v4/thesis/ANALYSES_CHX.md - Table of contents (locate RQ section)
7. [R] docs/v4/thesis/ANALYSES_CHX.md - Relevant RQ section (extract concept)

**Documents Written:**
- [W] results/chX/rqY/docs/1_concept.md - RQ concept with 7 sections

**Documents Updated:**
- [U] results/chX/rqY/status.yaml - rq_concept.status = success, context_dump added (5 lines: RQ ID, domains, analysis approach, data source, critical info)

**Report:** "Successfully created 1_concept.md for chX/rqY"

---

### Agent 3: rq_scholar
**Solution.md Reference:** Section 2.2.1
**Purpose:** Validate 1_concept.md scholarly accuracy via literature search
**Context Budget:** ~3k tokens (before WebSearch)

**Documents Read (Execution Order):**
1. [R] .claude/agents/rq_scholar.md - Agent prompt
2. [R] docs/v4/best_practices/universal.md - Circuit breakers, platform rules
3. [R] docs/v4/best_practices/workflow.md - Status YAML, context dumps
4. [R] results/chX/rqY/status.yaml - Check prior steps + read context_dumps from rq_concept
5. [R] docs/v4/templates/scholar_report.md - Scholarly feedback format
6. [R] results/chX/rqY/docs/1_concept.md - Extract claims for validation

**External Searches:**
- [WebSearch] Two-pass strategy (Pass 1: verify claims, Pass 2: challenge with counterevidence)

**Documents Updated:**
- [U] results/chX/rqY/docs/1_concept.md - Append rq_scholar feedback section
- [U] results/chX/rqY/status.yaml - rq_scholar.status = success, context_dump added (1 line: score/status, strengths, recommendations count)

**Report:** "Successfully validated 1_concept.md for chX/rqY - [N] claims verified"

---

### Agent 4: rq_stats
**Solution.md Reference:** Section 2.2.2
**Purpose:** Validate 1_concept.md statistical accuracy
**Context Budget:** ~3k tokens (before WebSearch)

**Documents Read (Execution Order):**
1. [R] .claude/agents/rq_stats.md - Agent prompt
2. [R] docs/v4/best_practices/universal.md - Circuit breakers, platform rules
3. [R] docs/v4/best_practices/workflow.md - Status YAML, context dumps
4. [R] results/chX/rqY/status.yaml - Check prior steps + read context_dumps from rq_concept, rq_scholar
5. [R] docs/v4/templates/stats_report.md - Statistical feedback format
6. [R] results/chX/rqY/docs/1_concept.md - Extract proposed methods

**External Searches:**
- [WebSearch] Two-pass strategy (Pass 1: verify appropriateness, Pass 2: challenge with limitations)

**Documents Updated:**
- [U] results/chX/rqY/docs/1_concept.md - Append rq_stats feedback section
- [U] results/chX/rqY/status.yaml - rq_stats.status = success, context_dump added (1 line: score, 5 category scores, key strength/concern)

**Report:** "Successfully validated 1_concept.md for chX/rqY - methods appropriate"

---

**USER APPROVAL GATE (Workflow Step 7):**
Master asks user to verify results/chX/rqY/docs/1_concept.md before proceeding.

---

### Agent 5: rq_planner
**Solution.md Reference:** Section 2.3.1
**Purpose:** Create step-by-step analysis plan (2_plan.md)
**Context Budget:** ~4-5k tokens

**Documents Read (Execution Order):**
1. [R] .claude/agents/rq_planner.md - Agent prompt
2. [R] docs/v4/best_practices/universal.md - Circuit breakers, platform rules
3. [R] docs/v4/best_practices/workflow.md - Status YAML, context dumps
4. [R] docs/v4/best_practices/code.md - Poetry, data boundaries
5. [R] results/chX/rqY/status.yaml - Check prior steps + read context_dumps from rq_concept, rq_scholar, rq_stats
6. [R] docs/v4/templates/plan.md - 2_plan.md structure specification
7. [R] results/chX/rqY/docs/1_concept.md - RQ concept with validated feedback
8. [R] docs/data_structure.md - master.xlsx tag system, UID format, TSVR documentation
9. [R] docs/tool_inventory.md - Available analysis/validation tools (NOTE: tool_inventory.md does not exist yet, will be created)
10. [R] docs/v4/names.md - Naming convention registry

**Documents Written:**
- [W] results/chX/rqY/docs/2_plan.md - Step-by-step plan with validation criteria + plot source CSV specs

**Documents Updated:**
- [U] results/chX/rqY/status.yaml - rq_planner.status = success, context_dump added (3 lines: step count, tool requirements, outputs specified)

**Report:** "Successfully created 2_plan.md for chX/rqY - [N] steps planned"

**NOTE:** RQ 5.1 expected to fail here due to missing tool_inventory.md - TDD approach requires building documentation from actual needs.

---

### Agent 6: g_conflict (Validation Gate)
**Solution.md Reference:** Section 2.6.1, Workflow Step 10
**Purpose:** Detect conflicts between 1_concept.md and 2_plan.md
**Context Budget:** ~3k tokens

**Documents Read (Execution Order):**
1. [R] docs/v4/best_practices/universal.md - Circuit breakers, platform rules
2. [R] Documents specified by master
   - results/chX/rqY/docs/1_concept.md
   - results/chX/rqY/docs/2_plan.md

**Documents Written:** None

**Report:** "[SEVERITY] Topic: description" OR "No conflicts detected"

**NOTE:** g_conflict does NOT use status.yaml (general-purpose agent, not RQ-specific)

---

### Agent 7: rq_tools
**Solution.md Reference:** Section 2.3.2
**Purpose:** Create 3_tools.yaml with exact tool specifications (Tool Catalog Architecture)
**Context Budget:** ~4-5k tokens

**Documents Read (Execution Order):**
1. [R] .claude/agents/rq_tools.md - Agent prompt
2. [R] docs/v4/best_practices/universal.md - Circuit breakers, platform rules
3. [R] docs/v4/best_practices/workflow.md - Status YAML, context dumps
4. [R] docs/v4/best_practices/code.md - Poetry, data boundaries, MCP
5. [R] results/chX/rqY/status.yaml - Check prior steps + read context_dumps from rq_planner
6. [R] docs/v4/templates/tools.md - 3_tools.yaml structure specification (Tool Catalog format)
7. [R] results/chX/rqY/docs/2_plan.md - Extract required tools from analysis steps
8. [R] docs/tool_inventory.md - Analysis tools AND validation tools with full signatures
9. [R] docs/v4/names.md - Naming conventions

**External Tool Calls:**
- [MCP] mcp__context7__resolve-library-id - Resolve library names to IDs
- [MCP] mcp__context7__get-library-docs - Fetch up-to-date library documentation

**Documents Written:**
- [W] results/chX/rqY/docs/3_tools.yaml - Tool catalog with analysis_tools + validation_tools sections

**Documents Updated:**
- [U] results/chX/rqY/status.yaml - rq_tools.status = success, context_dump added (3 lines: tools required, signatures complete, formats documented)

**Report:** "Successfully created 3_tools.yaml for chX/rqY - [N] tools specified"

**NOTE:** Step 9 checks all tools/names exist in documentation - FAILS if missing, triggering manual addition to docs.

---

### Agent 8: rq_analysis
**Solution.md Reference:** Section 2.3.3
**Purpose:** Create 4_analysis.yaml with exact analysis recipe per step
**Context Budget:** ~4-5k tokens

**Documents Read (Execution Order):**
1. [R] .claude/agents/rq_analysis.md - Agent prompt
2. [R] docs/v4/best_practices/universal.md - Circuit breakers, platform rules
3. [R] docs/v4/best_practices/workflow.md - Status YAML, context dumps
4. [R] docs/v4/best_practices/code.md - Poetry, data boundaries
5. [R] results/chX/rqY/status.yaml - Check prior steps + read context_dumps from rq_planner, rq_tools
6. [R] docs/v4/templates/analysis.md - 4_analysis.yaml structure specification
7. [R] results/chX/rqY/docs/2_plan.md - Chronological order + validation criteria
8. [R] results/chX/rqY/docs/3_tools.yaml - Tool specifications (analysis + validation)
9. [R] docs/v4/names.md - Naming conventions

**Documents Written:**
- [W] results/chX/rqY/docs/4_analysis.yaml - Complete recipe with analysis + validation per step + plot data prep

**Documents Updated:**
- [U] results/chX/rqY/status.yaml - Add analysis_steps section (all steps = pending), rq_analysis.status = success, context_dump added (3 lines: step count, I/O specs complete, signatures enforced)

**Report:** "Successfully created 4_analysis.yaml for chX/rqY - [N] steps specified"

---

### Agent 9: g_conflict (Validation Gate)
**Solution.md Reference:** Section 2.6.1, Workflow Step 13
**Purpose:** Detect conflicts between 2_plan.md, 3_tools.yaml, 4_analysis.yaml
**Context Budget:** ~4k tokens

**Documents Read (Execution Order):**
1. [R] docs/v4/best_practices/universal.md - Circuit breakers, platform rules
2. [R] Documents specified by master
   - results/chX/rqY/docs/2_plan.md
   - results/chX/rqY/docs/3_tools.yaml
   - results/chX/rqY/docs/4_analysis.yaml

**Documents Written:** None

**Report:** "[SEVERITY] Topic: description" OR "No conflicts detected"

---

## PHASE 2: AUTOMATED CODE EXECUTION (LOOP PER STEP)

### Agent 10: g_code (Code Generation)
**Solution.md Reference:** Section 2.4.1, Workflow Step 14
**Purpose:** Generate Python script with 4-layer pre-validation
**Context Budget:** ~3-4k tokens per invocation

**Documents Read (Execution Order):**
1. [R] .claude/agents/g_code.md - Agent prompt
2. [R] docs/v4/best_practices/universal.md - Circuit breakers, platform rules
3. [R] docs/v4/best_practices/code.md - Poetry, data boundaries, MCP
4. [R] Documentation specified by master:
   - results/chX/rqY/docs/4_analysis.yaml (step_N specification)
   - docs/tool_inventory.md (for signature validation - step 5b)
   - [IF step >1] Prior step output files (for input file validation - step 5c)

**Validation Checks (Step 5 - BEFORE code generation):**
- 5a. Import check: importlib.import_module + hasattr
- 5b. Signature check: inspect.signature matches 4_analysis.yaml
- 5c. Input file check: os.path.exists (if step >1)
- 5d. Column check: pandas read columns (if CSV)

**External Tool Calls:**
- [MCP] mcp__context7__resolve-library-id - Resolve library names
- [MCP] mcp__context7__get-library-docs - Fetch library docs
- [WebSearch] If validation unclear

**Documents Written:**
- [W] results/chX/rqY/code/stepN_name.py - Generated script with inline reasoning documentation

**Documents Updated:** None (g_code does NOT update status.yaml - master does after execution + validation)

**Report:** "Successfully generated stepN_name.py - all validations passed"

**NOTE:** g_code is general-purpose, does NOT read status.yaml. Master provides all required context.

---

### Master Execution (Between g_code and rq_inspect)
**Solution.md Reference:** Workflow Step 14
**Purpose:** Execute generated script, handle errors with g_debug

**Action:** Master runs: `poetry run python results/chX/rqY/code/stepN_name.py`

**If Success:** Proceed to rq_inspect (Agent 11)

**If Failure (traceback):** Invoke g_debug (Agent 12)

---

### Agent 11: rq_inspect (Output Validation)
**Solution.md Reference:** Section 2.4.2, Workflow Step 14
**Purpose:** Validate analysis step outputs (4-layer validation)
**Context Budget:** ~3-4k tokens

**Documents Read (Execution Order):**
1. [R] .claude/agents/rq_inspect.md - Agent prompt
2. [R] docs/v4/best_practices/universal.md - Circuit breakers, platform rules
3. [R] docs/v4/best_practices/workflow.md - Status YAML, context dumps
4. [R] results/chX/rqY/status.yaml - Check prior ANALYSIS steps (step01...step(N-1) = success, stepN = pending) + read context_dumps
5. [R] docs/v4/templates/inspect_criteria.md - Validation checklist
6. [R] results/chX/rqY/docs/2_plan.md - Validation criteria per step (substance criteria from step 11)
7. [R] results/chX/rqY/logs/stepN_name.log - Execution log (check errors/warnings/convergence)
8. [R] results/chX/rqY/data/stepN_*.csv - Output data files (pandas read, check columns/rows/dtypes/values)

**Validation Layers (Step 7):**
1. Existence: Files exist
2. Structure: Correct formats/columns/dtypes/rows
3. Substance: Values scientifically reasonable (per plan.md validation criteria)
4. Execution Log: No errors/warnings, convergence confirmed, embedded validation passed

**Documents Updated:**
- [U] results/chX/rqY/status.yaml - analysis_steps.stepN.status = success, stepN context_dump added (3 lines: step validated, format confirmed, criteria met)

**Report:** "Successfully validated stepN outputs for chX/rqY"

---

### Agent 12: g_debug (Error Recovery)
**Solution.md Reference:** Section 2.6.2, Workflow Step 14
**Purpose:** Debug failed script with git safety, report solution (in-place debugging with rollback)
**Context Budget:** ~4-5k tokens

**Documents Read (Execution Order):**
1. [R] .claude/agents/g_debug.md - Agent prompt
2. [R] docs/v4/best_practices/universal.md - Circuit breakers, platform rules
3. [R] docs/v4/best_practices/code.md - Poetry, data boundaries, MCP

**Safety Protocol (Step 3):**
- 3a. Bash: `git status` (check clean)
- 3b. QUIT if uncommitted changes (master must run /save first)
- 3c. Bash: `git add -A && git commit -m "DEBUG START: [step_id] [timestamp]"`
- 3d. Bash: `git push origin main` (CRITICAL REMOTE BACKUP)
- 3e. Check push exit code (QUIT if failed)

4. [R] results/chX/rqY/docs/4_analysis.yaml - Instructions g_code used (step 4)
5. [R] results/chX/rqY/code/stepN_name.py - Generated code with inline g_code reasoning (step 5)
6. [R] results/chX/rqY/logs/stepN_name.log - Error traceback (step 6)
7. [R] Other files as needed (data files, tool source code, etc.) (step 7)

**Debugging Process (Steps 8-11):**
- Step 8: Ultrathink - Classify error type (syntax/data/instructions/logic/import/column)
- Step 9: Edit code in-place (actual location, not sandbox)
- Step 10: Run code in actual location
- Step 11: Repeat 9-10 until success (Circuit breakers: same error 3x = QUIT, same type 5x = QUIT, 10 iterations max = QUIT)

**Rollback (Step 12):**
- 12a. Bash: `git reset --hard HEAD~1`
- 12b. Bash: `git status` (verify clean)
- 12c. If rollback failed: `git pull origin main` (recover from remote backup)

**External Tool Calls:**
- [WebSearch] If error type unclear

**Documents Written:** None (sandbox work, all changes rolled back)

**Report (Step 12):** Enhanced report with:
- Root cause (detailed description)
- Error type (syntax|data|instructions|logic|import|column)
- Solution (exact fix to apply to which file)
- Affected file (path)
- Suggested improvements (g_code prompt, 4_analysis.yaml, rq_planner, validation, tool_inventory.md)

**NOTE:** g_debug does NOT update status.yaml. Master applies reported solution, then re-runs execution.

---

### Master Post-Debug (After g_debug reports solution)
**Solution.md Reference:** Workflow Step 14
**Purpose:** Apply fix, re-run script, verify success

**Actions:**
1. Master applies fix to code OR templates (based on error type from g_debug report)
2. Master re-runs: `poetry run python results/chX/rqY/code/stepN_name.py`
3. If still fails: Repeat g_debug → fix → re-run until success
4. On success: Proceed to rq_inspect (Agent 11)

---

## PHASE 3: RESULTS GENERATION

### Agent 13: rq_plots (Plotting Code Generation)
**Solution.md Reference:** Section 2.5.1, Workflow Step 15
**Purpose:** Generate plots.py using pre-existing plotting functions (Option B architecture)
**Context Budget:** ~3-4k tokens

**Documents Read (Execution Order):**
1. [R] .claude/agents/rq_plots.md - Agent prompt
2. [R] docs/v4/best_practices/universal.md - Circuit breakers, platform rules
3. [R] docs/v4/best_practices/workflow.md - Status YAML, context dumps
4. [R] results/chX/rqY/status.yaml - Check prior steps + read context_dumps
5. [R] docs/v4/templates/plots.md - Plotting specifications
6. [R] tools/plots.py - SOURCE CODE (step 6 - understand existing functions, usage patterns)
7. [R] results/chX/rqY/docs/2_plan.md - Plot specifications with source CSV paths
8. [R] results/chX/rqY/plots/*.csv - Check all plot source CSVs exist (step 8 - if missing = FAIL, signals analysis incomplete)

**Documents Written:**
- [W] results/chX/rqY/plots/plots.py - Plotting script calling tools/plots.py functions

**Documents Updated:**
- [U] results/chX/rqY/status.yaml - rq_plots.status = success, context_dump added (2 lines: plot count, data sources)

**Report:** "Successfully generated plots.py for chX/rqY - [N] plots specified"

**CRITICAL:** rq_plots does NO data aggregation - only reads plot source CSVs created by analysis pipeline (g_code plot data prep steps). If source CSV missing, rq_plots FAILS, signaling analysis step incomplete.

---

### Master Execution (After rq_plots)
**Solution.md Reference:** Workflow Step 16
**Purpose:** Execute plotting script, generate PNG files

**Action:** Master runs: `poetry run python results/chX/rqY/plots/plots.py`

**Expected Outputs:**
- results/chX/rqY/plots/*.png files (per 2_plan.md plot specifications)

---

### Agent 14: rq_results (Scientific Plausibility + Summary)
**Solution.md Reference:** Section 2.5.2, Workflow Step 17
**Purpose:** Validate scientific plausibility, flag anomalies, generate summary.md
**Context Budget:** ~4-5k tokens

**Documents Read (Execution Order):**
1. [R] .claude/agents/rq_results.md - Agent prompt
2. [R] docs/v4/best_practices/universal.md - Circuit breakers, platform rules
3. [R] docs/v4/best_practices/workflow.md - Status YAML, context dumps
4. [R] results/chX/rqY/status.yaml - Check prior steps + read ALL context_dumps
5. [R] docs/v4/templates/results.md - Summary template (5 sections)
6. [R] results/chX/rqY/docs/2_plan.md - Expectations + substance validation criteria (for cross-reference in step 7f)
7. [R] results/chX/rqY/plots/*.png - ALL plot files (multimodal Read tool - visual inspection, step 6 checks existence first)
8. [R] results/chX/rqY/data/*.csv - ALL data files (pandas.head())
9. [R] results/chX/rqY/logs/*.log - ALL log files (check warnings, convergence, validation messages)
10. [R] results/chX/rqY/docs/1_concept.md - Theoretical context

**Validation Process (Step 7):**
- Ultrathink: Plausibility checks (6 types: value ranges, effect directions, sample characteristics, model diagnostics, visual coherence, plan.md cross-reference)
- Anomaly flagging: Document in summary Sections 3-4 (don't trace root causes, suggest investigations)
- Synthesis: Integrate 6 sources (context_dumps, data, plots visual, logs, concept.md, plan.md) → results.md 5 sections

**External Tool Calls:**
- [WebSearch] Validate scientific plausibility (effect directions match cognitive neuroscience literature)

**Documents Written:**
- [W] results/chX/rqY/results/summary.md - 5-section summary with anomaly flags

**Documents Updated:**
- [U] results/chX/rqY/status.yaml - rq_results.status = success, context_dump added (3 lines: plausibility validated, anomaly count OR acceptable, summary documented)

**Report:** "Successfully created summary.md for chX/rqY (N anomalies flagged)" OR "Successfully created summary.md for chX/rqY (plausibility acceptable)"

---

## SUMMARY STATISTICS

**Total Agents:** 13 (10 RQ-specific + 3 general-purpose)

**RQ-Specific Agents (Use status.yaml):**
1. rq_builder
2. rq_concept
3. rq_scholar
4. rq_stats
5. rq_planner
6. rq_tools
7. rq_analysis
8. rq_inspect
9. rq_plots
10. rq_results

**General-Purpose Agents (Do NOT use status.yaml):**
11. g_code (invoked per analysis step)
12. g_debug (invoked on execution errors)
13. g_conflict (invoked at validation gates)

**Document Categories:**
- Agent prompts: 13 files (.claude/agents/*.md)
- Agent best practices: 3 files (docs/v4/best_practices/universal.md, workflow.md, code.md)
  - universal.md: Read by ALL 13 agents
  - workflow.md: Read by 10/13 workflow agents (rq_builder, rq_concept, rq_scholar, rq_stats, rq_planner, rq_tools, rq_analysis, rq_inspect, rq_plots, rq_results)
  - code.md: Read by 5/13 code-aware agents (rq_planner, rq_tools, rq_analysis, g_code, g_debug)
- Templates: 11 files (docs/v4/templates/*.md)
- Thesis analyses: 3 files (docs/v4/thesis/ANALYSES_CHX.md)
- Project documentation: 2 files (docs/data_structure.md, docs/tool_inventory.md)
- Naming registry: 1 file (docs/v4/names.md)
- RQ outputs: Variable per RQ (status.yaml, 1_concept.md, 2_plan.md, 3_tools.yaml, 4_analysis.yaml, data/*.csv, logs/*.log, plots/*.png, results/summary.md)

**Total Document Reads (Per Complete RQ):**
- Phase 1 (Setup): ~35-40 document reads
- Phase 2 (Execution): ~(10-15 reads per step) × (N analysis steps)
- Phase 3 (Results): ~15-20 document reads
- **Grand Total:** 50-60 base reads + (10-15 × N) execution reads

**Context Window Usage:**
- Individual agents: <5k tokens each (per design goal)
- g_code validation: ~3-4k tokens per step
- rq_inspect validation: ~3-4k tokens per step
- rq_results synthesis: ~4-5k tokens (highest in pipeline)

---

## VALIDATION GATES

**User Approval Gate (Step 7):** After 1_concept.md creation, before planning
- User verifies concept before proceeding
- If changes requested: Loop back to rq_concept

**Automated Validation Gates:**
1. **Step 10:** g_conflict compares 1_concept.md + 2_plan.md
2. **Step 13:** g_conflict compares 2_plan.md + 3_tools.yaml + 4_analysis.yaml
3. **Per Analysis Step:** rq_inspect validates outputs (4-layer validation)
4. **Pre-Code Generation:** g_code validates tools/imports/files/columns (4-layer validation)
5. **Post-Execution:** rq_results validates scientific plausibility (6-type checks)

---

## CRITICAL DESIGN NOTES

### Context Window Management
- **Agent best practices:** Split into 3 files for targeted loading
  - universal.md: Read by ALL 13 agents (~1.5k tokens)
  - workflow.md: Read by 10/13 workflow agents (~1k tokens)
  - code.md: Read by 5/13 code-aware agents (~0.7k tokens)
- **status.yaml:** Read by RQ-specific agents for continuity (<1k tokens, max 5 lines per agent context_dump)
- **Template files:** Read once per agent, lean specifications (~500-1000 tokens each)
- **Thesis files:** Read selectively (rq_concept extracts ONLY relevant RQ section, not entire chapter)

### Document Reuse Pattern
- **High reuse:** universal.md (read 13 times per RQ), workflow.md (read 10 times per RQ), status.yaml (read 10 times per RQ)
- **Moderate reuse:** code.md (read 5 times per RQ), templates (read 1-2 times each), data_structure.md (read 1 time), tool_inventory.md (read 3 times)
- **Low reuse:** thesis files (read 1 time), names.md (read 3 times)

### TDD Approach
- **names.md:** Starts EMPTY, RQ 5.1 expected to fail at rq_tools step 9, manual population required
- **tool_inventory.md:** Does NOT exist yet (TDD), will be created when first RQ requires it
- **Philosophy:** Build documentation from actual needs, not speculation

### Error Recovery Loop
1. g_code generates script with 4-layer pre-validation
2. Master executes script
3. If fails: g_debug creates remote git backup, debugs in-place, rolls back, reports solution
4. Master applies fix based on error type classification
5. Master re-runs script
6. Loop until success, then rq_inspect validates outputs

### Multimodal Inspection
- **rq_results:** Uses Read tool on PNG files (multimodal capability) for visual plot inspection
- **Purpose:** Verify plots match statistical findings, detect visual anomalies

---

## QUALITY CONTROL AUDIT CHECKLIST

**For Each Agent:**
- [ ] Context budget <5k tokens? (Check total size of all documents read)
- [ ] All documents specified in solution.md? (Verify against sections 2.1-2.6)
- [ ] Reading order matches workflow steps? (Check against agent prompt step numbers)
- [ ] Circuit breakers documented? (Verify EXPECTATIONS/STEP/TOOL/CLARITY/SCOPE errors defined)
- [ ] Context dumps terse? (Max 5 lines per agent in status.yaml)

**For Each Document:**
- [ ] Purpose clear? (One responsibility per document)
- [ ] Audience clear? (Which agents read it)
- [ ] No redundancy? (Information stated once, referenced elsewhere)
- [ ] No bloat? (Concise specifications, no long prose)
- [ ] No contradictions? (Cross-reference with g_conflict validation)

**For Workflow:**
- [ ] Sequential dependencies correct? (Each agent reads only prior agents' outputs)
- [ ] No circular dependencies? (No agent reads its own output)
- [ ] Validation gates present? (g_conflict at steps 10 & 13, rq_inspect per step, g_code pre-validation)
- [ ] Error recovery clear? (g_debug rollback protocol, master fix application)

---

## CHANGE LOG

**2025-11-21:**
- Initial creation
- Mapped all 13 agents against solution.md sections 2.1-2.6
- Documented complete chronology for Phase 1 (manual), Phase 2 (automated loop), Phase 3 (results)
- Added validation gates, quality control checklist, summary statistics

---

**END OF CHRONOLOGY**
