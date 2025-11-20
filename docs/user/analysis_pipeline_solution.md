# V4.X ARCHITECTURE SPECIFICATION

**Version:** 4.0
**Status:** VALIDATED
**Last Updated:** 2025-11-15

---

## 🚨 CRITICAL: HOW TO USE THIS DOCUMENT

**This is a SPECIFICATION, not implementation.**

- Describes WHAT things should do, not HOW to implement them
- Templates sections specify required contents, not actual templates
- Agent sections specify behavior/requirements, not agent code
- When building implementations, reference relevant sections to ensure compliance

**Document Rules:**
1. **KEEP IT CONCISE** - Bullet points, not paragraphs
2. **NO CODE EXAMPLES** - Specifications only, no implementation
3. **NO LONG PROSE** - If section >20 lines, break into subsections
4. **ZERO REDUNDANCY** - State facts once, reference elsewhere
5. **EXPLICIT EVERYTHING** - No "etc.", no "as needed", no vagueness
6. **FORMAT CONSISTENCY** - All agents use same structure, all files use same schema

---

## TABLE OF CONTENTS

**Status Legend:**
- ✅ **FINALIZED** - Specification complete, ready for implementation
- ✨ **IMPLEMENTED** - Implementation complete (spec + actual files built)
- 🔄 **PENDING** - Specification complete, implementation not started
- ⚠️ **QUESTIONS** - Has unresolved questions/decisions
- 📝 **DRAFT** - Needs review/expansion

---

### 1. INTRODUCTION
- 1.1 Document Purpose & Rules ✅ FINALIZED
- 1.2 Architecture Overview ✅ FINALIZED
- 1.3 Key Concepts ✅ FINALIZED
- 1.4 Data Preprocessing Requirements ✅ FINALIZED

### 2. AGENT SPECIFICATIONS
- 2.1 RQ Setup Agents 🔄 PENDING
  - 2.1.1 rq_builder ✨ IMPLEMENTED
  - 2.1.2 rq_concept ✨ IMPLEMENTED
- 2.2 Validation Agents 🔄 PENDING
  - 2.2.1 rq_scholar ✨ IMPLEMENTED
  - 2.2.2 rq_stats ✨ IMPLEMENTED
- 2.3 Planning Agents 🔄 PENDING
  - 2.3.1 rq_planner ✨ IMPLEMENTED
  - 2.3.2 rq_tools ✨ IMPLEMENTED
  - 2.3.3 rq_analysis ✨ IMPLEMENTED
- 2.4 Execution Agents 🔄 PENDING
  - 2.4.1 g_code ✨ IMPLEMENTED
  - 2.4.2 rq_inspect ✨ IMPLEMENTED
- 2.5 Results Agents 🔄 PENDING
  - 2.5.1 rq_plots ✨ IMPLEMENTED
  - 2.5.2 rq_results ✨ IMPLEMENTED
- 2.6 General-Purpose Agents 🔄 PENDING
  - 2.6.1 g_conflict ✨ IMPLEMENTED
  - 2.6.2 g_debug ✨ IMPLEMENTED

### 3. WORKFLOW & ORCHESTRATION
- 3.1 Master Orchestration Workflow ✅ FINALIZED
- 3.2 Orchestration Modes ✅ FINALIZED
- 3.3 Status Tracking & Pseudo-Statefulness ✅ FINALIZED
- 3.4 Error Recovery Workflow ✅ FINALIZED

### 4. DOCUMENTATION TEMPLATES
- 4.1 Setup Templates 🔄 PENDING
  - 4.1.1 build_folder.md (folder structure specification) ✨ IMPLEMENTED
  - 4.1.2 build_status.md (status.yaml specification) ✨ IMPLEMENTED
- 4.2 RQ Documentation Templates 🔄 PENDING
  - 4.2.1 concept.md (1_concept.md specification) ✨ IMPLEMENTED
  - 4.2.2 plan.md (2_plan.md specification) ✨ IMPLEMENTED
  - 4.2.3 tools.md (3_tools.yaml specification) ✨ IMPLEMENTED
  - 4.2.4 analysis.md (4_analysis.yaml specification) ✨ IMPLEMENTED
- 4.3 Validation Templates ✅ COMPLETE
  - 4.3.1 scholar_report.md (scholarly feedback specification) ✨ IMPLEMENTED
  - 4.3.2 stats_report.md (statistical feedback specification) ✨ IMPLEMENTED
  - 4.3.3 inspect_criteria.md (validation checklist specification) ✨ IMPLEMENTED
- 4.4 Output Templates ✅ COMPLETE
  - 4.4.1 plots.md (plotting specification) ✨ IMPLEMENTED
  - 4.4.2 results.md (summary specification) ✨ IMPLEMENTED
- 4.5 Support Documentation ✅ COMPLETE
  - 4.5.1 names.md (naming registry specification) ✨ IMPLEMENTED
  - 4.5.2 orchestrator.md (Phase 2 automation specification) ✨ IMPLEMENTED
  - 4.5.3 thesis/ (ANALYSES_CHX.md specifications) ✨ IMPLEMENTED
  - 4.5.4 automation.md (master orchestration workflow) ✨ IMPLEMENTED

### 5. STANDARDS & CONVENTIONS
- 5.1 Agent Best Practices ✨ IMPLEMENTED
- 5.2 File Structure Schema ✅ FINALIZED
- 5.3 Naming Conventions ✨ IMPLEMENTED
- 5.4 Context Dump Format ✅ FINALIZED
- 5.5 Signature Enforcement ✅ FINALIZED

### 6. TECHNICAL SPECIFICATIONS
- 6.1 g_code Validation Protocol ✅ FINALIZED
- 6.2 Scope Boundaries ✅ FINALIZED
- 6.3 Cross-RQ Dependencies ✅ FINALIZED
- 6.4 Platform Requirements ✅ FINALIZED
- 6.5 Integration ✅ FINALIZED

### 7. QUICK REFERENCE
- 7.1 Agent Lookup Table ✅ FINALIZED
- 7.2 File Path Reference ✅ FINALIZED
- 7.3 Workflow Checklist ✅ FINALIZED
- 7.4 Legacy Information ✅ FINALIZED

---

# 1. INTRODUCTION

## 1.1 Document Purpose & Rules

**Purpose:** Ground truth for v4.X atomic agent architecture

**How to Read:**
- Each agent: Name → Goal → Expects → Steps → Report
- Each template: Purpose → Audience → Required Sections
- Each workflow: Step numbers → Agent invocations → Validation gates

**How to Use:**
- Before building ANY agent → Read section 2 (Agent Specifications)
- Before creating templates → Read section 4 (Documentation Templates)
- Before modifying workflow → Read section 3 (Workflow & Orchestration)
- Before implementing → Verify against section 5 (Standards & Conventions)

**Critical Instructions:**
- This document specifies WHAT things should do
- Actual implementations built separately, referencing this spec
- Templates described here, actual .md files created per these requirements
- Agent behaviors specified here, actual .md prompts written per these specs

---

## 1.2 Architecture Overview

**Transition:** v3.0 (7 monolithic agents) → v4.X (13 atomic agents)

**Reason for Redesign:**
- Context bloat in monolithic agents
- Caused hallucinations (e.g., "tests 1&2 same day" - never documented)
- API mismatches (guessing from config.yaml instead of reading tools_inventory.md)
- Cascading failures (1 error → 5+ downstream errors)

**v4.X Design Principles:**
- **Atomic agents:** Single task per agent, lean focused context
- **Task snipers:** Read exactly what's needed, execute, report, quit
- **No context bloat:** Max context per agent <5k tokens
- **Explicit everything:** No guessing, circuit breakers on uncertainty

**Communication Model:**
- **Flat architecture:** Master orchestrates all agents (no nesting)
- **File-based:** Pass file paths, not content (prevents context bloat)
- **Stateless agents:** Each invocation independent
- **Pseudo-statefulness:** Via status.yaml context_dumps (terse summaries)

**Master Orchestration:**
- **Master:** Main claude (not user, not sub-agent)
- **Invocation:** Claude Code's native sub-agent mechanism
- **Control:** Master reads workflow, invokes agents sequentially, handles errors
- **Phases:** Manual (Phase 1), Automated (Phase 2 - orchestrator script)

**State Tracking:**
- **status.yaml:** Machine-readable agent statuses
- **context_dump field:** Terse summaries per agent (max 5 lines)
- **Continuity:** Next agents read prior context_dumps
- **Prevents bloat:** Stateful behavior without context window bloat

**Validation Strategy:**
- **Circuit breakers:** All agents quit on uncertainty (5 types)
- **Pre-validation:** g_code validates BEFORE generating code
- **Multi-layer checks:** Import → Signature → Input files → Columns
- **Fail-fast:** Quit immediately on ANY validation failure

**Platform:**
- Windows with Poetry
- UTF-8 file encoding
- ASCII-only output (no Unicode)
- Bash commands (not PowerShell)

**Git Integration:**
- Handled by /save command
- Before and after context-manager curation
- Rollback points available

**Variables:**
- chX: {ch5, ch6, ch7}
- rqY: {rq1, rq2, ..., rq15} for ch5/ch6, {rq1, rq2, ..., rq20} for ch7

---

## 1.3 Key Concepts

### Pseudo-Statefulness

**Mechanism:**
- Agents read status.yaml at start
- Read prior agents' context_dumps
- Maintain continuity without loading full conversation history

**Benefits:**
- Context window stays lean (<5k per agent)
- Agents know what prior agents decided
- No context bloat from repeated information

### Context Dumps

**Format:**
- YAML field under agent name
- Multiline string
- Max 5 lines per agent

**Content:**
- Memory domains (What/Where/When)
- Analysis type (IRT, LMM, CTT)
- Key decisions made
- Critical information for downstream agents

**Purpose:**
- Terse summaries only
- Prevent file bloat
- Enable continuity

### Circuit Breakers

**Philosophy:** Quit on uncertainty, never guess

**Types:**
1. **EXPECTATIONS ERROR:** Missing expected input
2. **STEP ERROR:** Cannot complete step as prescribed
3. **TOOL ERROR:** Tool execution fails
4. **CLARITY ERROR:** Insufficient information to proceed
5. **SCOPE ERROR:** Required action outside agent scope

**Action:** QUIT immediately, report to master

### Validation Gates

**User Approval:**
- Single gate: After 1_concept.md creation (workflow step 7)
- User verifies concept before proceeding

**Automated Validation:**
- g_conflict: Document conflict detection (steps 10, 13)
- rq_inspect: Output validation (per analysis step)
- g_code: Pre-generation validation (before code creation)

### Scope Boundaries

**RAW Data:**
- Extractable from master.xlsx
- OR outputs from other completed RQs
- Created OUTSIDE analysis pipeline

**DERIVED Data:**
- Requires statistical analysis
- Created BY analysis step scripts
- Created INSIDE analysis pipeline

**Circuit Breaker:**
- If data source unclear → CLARITY ERROR

---

## 1.4 Data Preprocessing Requirements

**Note:** Thesis Chapter 4 (statistical methodology) will document v4.X implementation after RQ completion. V4.X serves as ground truth for Chapter 4 content.

### Accuracy Scores (-ANS Tags)

**Raw Data:**
- May contain partial scores: 0.25, 0.5, 1.0
- Partial scores given for spatial/ordinal adjacency per thesis methods

**Preprocessing Rule:**
- **Dichotomize before IRT:** 1 = 1, all <1 = 0
- Apply during data extraction OR as Step 1 of analysis pipeline

**Rationale:**
- Theoretically justified (no arbitrary partial credit)
- Preserves interpretability (correct vs incorrect binary)
- Matches dichotomous IRT assumption

**Implementation:**
- Document in 2_plan.md if RQ uses items with partial scores
- Validate dichotomization completed before IRT calibration

### Confidence Ratings

**Raw Data:**
- 5-point Likert scale (1 = Guess/No Memory → 5 = Absolutely Certain)

**Preprocessing Rule:**
- **Use as-is** (no dichotomization, no bias correction)
- Preserve raw 1-5 ratings throughout analysis

**Rationale:**
- Preserves direct interpretability
- Response style (cautious vs extreme) may be meaningful individual variance
- Bias correction reduces interpretability more than measurement quality

**Likert Response Bias:**
- **Known issue:** Some participants prefer extreme ratings (only 1s and 5s)
- **Decision:** Document patterns, do NOT correct
- **Implementation:** Report response style descriptives in rq_results summary
- **Justification:** Transparency >> algorithmic correction with arbitrary thresholds

### IRT Model Specification

**GRM (Graded Response Model):**
- Handles BOTH dichotomous and polytomous items in single calibration
- Accuracy (dichotomized): 2 categories (0, 1) → GRM reduces to 2PL
- Confidence (raw Likert): 5 categories (1, 2, 3, 4, 5) → Standard polytomous GRM

**Tool:**
- `calibrate_grm` used for all IRT calibrations
- Automatically handles variable number of categories per item

**Clarification:**
- Thesis references "dichotomous IRT" (correct for accuracy after preprocessing)
- V4.X uses GRM (correct, general model encompassing dichotomous as special case)
- No conflict - GRM with 2 categories = dichotomous IRT mathematically

---

# 2. AGENT SPECIFICATIONS

**Note:** All agents stored in `.claude/agents/` (per Anthropic specification)

**Common Pattern:**
- Frontmatter: name, description, tools
- Goal: One-sentence task description
- Expects: What master provides
- Steps: Numbered sequence
- Report: What agent tells master

---

## 2.1 RQ Setup Agents

### 2.1.1 rq_builder

**File:** `.claude/agents/rq_builder.md`

**Frontmatter Requirements:**
- name: rq_builder
- description: Builds blank RQ folder structure and status.yaml
- tools: Read, Write, Edit, Bash

**Goal:** Build blank chX/rqY folder structure per template

**Expects:** Master specifies chX/rqY to build

**Steps:**
1. Read: docs/v4/best_practices/universal.md
2. Read: docs/v4/templates/build_folder.md
3. Read: docs/v4/templates/build_status.md
4. Bash: Create results/chX/rqY/ if doesn't exist, verify empty if exists (ensures starting fresh)
5. Bash: Create subfolders per build_folder.md (docs/, data/, code/, logs/, plots/, results/)
6. Bash: Create status.yaml per build_status.md template
7. Report: Success and quit

**Report Format:** "Successfully built results/chX/rqY/ structure with status.yaml"

---

### 2.1.2 rq_concept

**File:** `.claude/agents/rq_concept.md`

**Frontmatter Requirements:**
- name: rq_concept
- description: Creates 1_concept.md from thesis analyses
- tools: Read, Write, Edit, Bash

**Goal:** Extract RQ concept from thesis, format per template

**Expects:** Master specifies chX/rqY to conceptualize

**Steps:**
1. Read: docs/v4/best_practices/universal.md
2. Read: docs/v4/best_practices/workflow.md
3. Read: results/chX/rqY/status.yaml
4. Check: All prior steps = success, this step onwards = pending (else FAIL)
5. Read: docs/v4/templates/concept.md
6. Read: docs/v4/thesis/ANALYSES_CHX.md (locate TABLE OF CONTENTS)
7. Read: docs/v4/thesis/ANALYSES_CHX.md (extract relevant section)
8. Ultrathink: Map thesis content → concept.md template format
9. Bash: Create results/chX/rqY/docs/1_concept.md
10. Write: Fill 1_concept.md with mapped content
11. Edit: status.yaml (update this step to success, write context_dump with terse summary)
12. Report: Success and quit

**Context Dump Content (Max 5 Lines):**
- Line 1: RQ ID and brief title
- Line 2: Memory domains examined
- Line 3: Analysis approach
- Line 4: Data source
- Line 5: Critical info for downstream agents

**Report Format:** "Successfully created 1_concept.md for chX/rqY"

---

## 2.2 Validation Agents

### 2.2.1 rq_scholar ✅ TESTED

**File:** `.claude/agents/rq_scholar.md`

**Frontmatter Requirements:**
- name: rq_scholar
- description: Validates 1_concept.md scholarly accuracy, writes 1_scholar.md
- tools: Read, Write, WebSearch

**Goal:** Verify concept.md claims are theoretically accurate

**Expects:** Master specifies chX/rqY to inspect

**Steps:**
1. Read: docs/v4/best_practices/universal.md
2. Read: docs/v4/best_practices/workflow.md
3. Read: results/chX/rqY/status.yaml (including prior context_dumps)
4. Check: All prior steps = success, this step onwards = pending (else FAIL)
5. Read: docs/v4/templates/scholar_report.md
6. Read: results/chX/rqY/docs/1_concept.md
7. Read: /home/etai/projects/REMEMVR/thesis/methods.md (experimental methodology for context)
8. Ultrathink: Extract claims, identify required evidence
9. WebSearch: Two-pass strategy (Pass 1: Verify claims, Pass 2: Challenge with counterevidence)
10. Write: Create results/chX/rqY/docs/1_scholar.md (standalone validation report)
11. Edit: status.yaml (update this step to success, write context_dump with terse summary)
12. Report: Success and quit

**Context Dump Format:**
- Single terse sentence including: score/status, key strengths, number of recommendations
- Example: "5.1 validated: 9.5/10 APPROVED. Theory excellent, literature strong, 4 suggested improvements. Ready for stats validation."

**Report Format:** "Successfully validated 1_concept.md for chX/rqY - [N] claims verified, wrote 1_scholar.md"

---

### 2.2.2 rq_stats ✅ TESTED

**File:** `.claude/agents/rq_stats.md`

**Frontmatter Requirements:**
- name: rq_stats
- description: Validates 1_concept.md statistical accuracy, writes 1_stats.md
- tools: Read, Write, WebSearch

**Goal:** Verify proposed statistical methods are valid

**Expects:** Master specifies chX/rqY to inspect

**Steps:**
1. Read: docs/v4/best_practices/universal.md
2. Read: docs/v4/best_practices/workflow.md
3. Read: results/chX/rqY/status.yaml (including prior context_dumps)
4. Check: All prior steps = success, this step onwards = pending (else FAIL)
5. Read: docs/v4/templates/stats_report.md
6. Read: results/chX/rqY/docs/1_concept.md
7. Read: /home/etai/projects/REMEMVR/thesis/methods.md (experimental methodology for context)
8. Ultrathink: Extract proposed methods, identify validity criteria
9. WebSearch: Two-pass strategy (Pass 1: Verify appropriateness, Pass 2: Challenge with limitations)
10. Write: Create results/chX/rqY/docs/1_stats.md (standalone validation report)
11. Edit: status.yaml (update this step to success, write context_dump with terse summary)
12. Report: Success and quit

**Context Dump Format:**
- Single terse sentence including: score/status, all 5 category scores, key strength or concern
- Example: "9.5/10 APPROVED. Cat1: 3.0/3. Cat2: 2.0/2 (100% reuse). Cat3: 2.0/2. Cat4: 2.0/2. Cat5: 0.5/1 (3 concerns)."

**Report Format:** "Successfully validated 1_concept.md for chX/rqY - methods appropriate, wrote 1_stats.md"

---

## 2.3 Planning Agents

### 2.3.1 rq_planner

**File:** `.claude/agents/rq_planner.md`

**Frontmatter Requirements:**
- name: rq_planner
- description: Creates step-by-step analysis plan (no code)
- tools: Read, Write, Edit, Bash

**Goal:** Transform concept → detailed analysis plan

**Expects:** Master specifies chX/rqY to plan

**Steps:**
1. Read: docs/v4/best_practices/universal.md
2. Read: docs/v4/best_practices/workflow.md
3. Read: docs/v4/best_practices/code.md
4. Read: results/chX/rqY/status.yaml (including prior context_dumps)
5. Check: All prior steps = success, this step onwards = pending (else FAIL)
6. Read: docs/v4/templates/plan.md
7. Read: results/chX/rqY/docs/1_concept.md
8. Read: docs/data_structure.md
9. Read: docs/tool_inventory.md
10. Read: docs/v4/names.md
11. Ultrathink: Map concept → analysis steps, specify inputs/outputs per step
12. Bash: Create results/chX/rqY/docs/2_plan.md
13. Write: Fill 2_plan.md with step specifications including:
    - Methodological validation criteria (convergence, fit indices - for validation tools during execution)
    - **Substance validation criteria** (for rq_inspect post-execution validation):
      - Output files (exact paths, row counts, column counts, data types)
      - Value ranges (theta ∈ [-3,3], p ∈ [0,1], scientifically reasonable bounds)
      - Data quality (missing data tolerance, expected N, duplicate checks)
      - Log patterns (required: "Model converged: True", forbidden: "ERROR")
    - **Plot source CSV preparation** (for each plot, document):
      - Plot description (general language: "trajectory over time with confidence bands")
      - Required data sources (which analysis outputs to aggregate)
      - Source CSV path (plots/PLOTNAME_data.csv)
      - Required columns (time, value, CI_lower, CI_upper, grouping vars)
      - Plotting function (general: "trajectory plot", rq_plots maps to specific function)
    - Statement: "Validation tools MUST be used after each analysis tool"
14. Edit: status.yaml (update this step to success, write context_dump with terse summary)
15. Report: Success and quit

**Context Dump Content:**
- Number of analysis steps
- Tool requirements identified
- Expected outputs specified

**Report Format:** "Successfully created 2_plan.md for chX/rqY - [N] steps planned"

---

### 2.3.2 rq_tools

**File:** `.claude/agents/rq_tools.md`

**Frontmatter Requirements:**
- name: rq_tools
- description: Creates 3_tools.yaml with exact tool specifications
- tools: Read, Write, Edit, Bash, mcp__context7__resolve-library-id, mcp__context7__get-library-docs

**Goal:** Specify exact tool usage (signatures, formats, names) AND validation procedures

**Expects:** Master specifies chX/rqY to work on

**Steps:**
1. Read: docs/v4/best_practices/universal.md
2. Read: docs/v4/best_practices/workflow.md
3. Read: docs/v4/best_practices/code.md
4. Read: results/chX/rqY/status.yaml (including prior context_dumps)
5. Check: All prior steps = success, this step onwards = pending (else FAIL)
6. Read: docs/v4/templates/tools.md
7. Read: results/chX/rqY/docs/2_plan.md
8. Read: docs/tool_inventory.md (analysis tools AND their corresponding validation tools)
9. Read: docs/v4/names.md
10. Ultrathink: Extract required tools, map exact data formats/naming conventions
11. Check: All tools/names exist in documentation (else FAIL with missing items)
12. Bash: Create results/chX/rqY/docs/3_tools.yaml
13. Write: Fill 3_tools.yaml with tool specifications (Tool Catalog Architecture):
    - Structure: Two top-level sections (analysis_tools, validation_tools)
    - Analysis tool specification: Full signature with type hints, validation_tool reference field
    - Validation tool specification: Corresponding validation tool signature (from tool_inventory.md)
    - Input/output formats for both analysis and validation
    - Validation criteria (what validation tool checks)
    - Each tool listed ONCE (deduplication across steps)
    - validation_tool field in each analysis tool links to validation_tools section
14. Edit: status.yaml (update this step to success, write context_dump with terse summary)
15. Report: Success and quit

**Context Dump Content:**
- Tools required
- Signature specifications complete
- Format requirements documented

**Report Format:** "Successfully created 3_tools.yaml for chX/rqY - [N] tools specified"

---

### 2.3.3 rq_analysis

**File:** `.claude/agents/rq_analysis.md`

**Frontmatter Requirements:**
- name: rq_analysis
- description: Creates 4_analysis.yaml with exact analysis recipe
- tools: Read, Write, Edit, Bash

**Goal:** Generate complete analysis recipe (inputs/outputs/formats per step) with validation

**Expects:** Master specifies chX/rqY to work on

**Steps:**
1. Read: docs/v4/best_practices/universal.md
2. Read: docs/v4/best_practices/workflow.md
3. Read: docs/v4/best_practices/code.md
4. Read: results/chX/rqY/status.yaml (including prior context_dumps)
5. Check: All prior steps = success, this step onwards = pending (else FAIL)
6. Read: docs/v4/templates/analysis.md
7. Read: results/chX/rqY/docs/2_plan.md
8. Read: results/chX/rqY/docs/3_tools.yaml (analysis tools AND validation tools)
9. Read: docs/v4/names.md
10. Ultrathink: Determine step order, exact variable/file names/formats
11. Bash: Create results/chX/rqY/docs/4_analysis.yaml
12. Write: Fill 4_analysis.yaml with step recipes:
    - Analysis tool call (inputs/outputs/parameters/formats/signature)
    - Validation tool call (at end of EACH step, using analysis outputs)
    - Both analysis and validation function signatures with type hints
    - **Plot data preparation steps** (create plots/*.csv before rq_plots runs):
      - For each plot: prepare_*_plot_data step (aggregates analysis outputs)
      - Inputs: Multiple data/*.csv files (theta_scores, observed_means, etc.)
      - Output: Single plots/PLOTNAME_data.csv with columns needed for plotting
      - Validation: validate_plot_data checks required columns, row counts, value ranges
13. Edit: status.yaml (add analysis_steps section with all steps = pending, write context_dump)
14. Report: Success and quit

**CRITICAL:** Each step in 4_analysis.yaml MUST end with validation tool call. g_code will generate scripts that run analysis THEN validation for each step.

**Critical Requirement:**
- 4_analysis.yaml MUST include full function signatures with type hints
- Forces reading tools_inventory.md (prevents API guessing)
- Enables g_code validation before generation

**Note:** Both 2_plan.md and 3_tools.yaml reads necessary
- 2_plan.md: Chronological order + validation criteria
- 3_tools.yaml: Tool specifications

**Context Dump Content:**
- Analysis steps count
- Input/output specifications complete
- Signature enforcement confirmed

**Report Format:** "Successfully created 4_analysis.yaml for chX/rqY - [N] steps specified"

---

## 2.4 Execution Agents

### 2.4.1 g_code

**File:** `.claude/agents/g_code.md`

**Frontmatter Requirements:**
- name: g_code
- description: Generates Python code from specifications with validation
- tools: Read, Write, Edit, Bash, WebSearch, mcp__context7__resolve-library-id, mcp__context7__get-library-docs

**Goal:** Generate Python script per exact specifications

**Expects:** Master specifies ALL required information:
- Documentation paths to read (e.g., results/chX/rqY/docs/4_analysis.yaml for step_N specification)
- Output code path (e.g., results/chX/rqY/code/stepN_name.py)
- Log file path (e.g., results/chX/rqY/logs/stepN_name.log)
- Any other required context (tools_inventory.md, data file paths for validation, etc.)

**Note:** g_code is general-purpose and does NOT read status.yaml. Master MUST provide complete information. If master doesn't provide required info → EXPECTATIONS ERROR. If provided info is incomplete/wrong → CLARITY ERROR.

**Steps:**
1. Read: docs/v4/best_practices/universal.md
2. Read: docs/v4/best_practices/code.md
3. Read: Specified documentation (e.g., 4_analysis.yaml step_N)
4. Check: Documentation provides all required information (else CLARITY ERROR)
5. **VALIDATE BEFORE GENERATING CODE:**
   - 5a. Import check: Tool module/function exists via importlib + hasattr (else TOOL ERROR)
   - 5b. Signature check: inspect.signature matches documented signature (else SIGNATURE ERROR)
   - 5c. Input file check (if step >1): Files exist via os.path.exists (else INPUT ERROR)
   - 5d. Column check (if CSV): pandas read columns match expected (else FORMAT ERROR)
6. Bash: Create Python file at specified path
7. Write: Generate code per documentation specifications WITH INLINE REASONING DOCUMENTATION:
   - Add header comment block documenting:
     - Step ID and purpose
     - Expected inputs (paths, columns, formats)
     - Expected outputs (paths, columns, formats)
     - Validation criteria
     - g_code's reasoning (why this approach, what the code does)
   - Add inline comments explaining each major section
   - Document expected data shapes (row counts, column counts)
   - This enables g_debug to understand intent when debugging failures
8. Check: Code prints output to specified log file (else FAIL)
9. Report: Success and quit

**CRITICAL:** ALL validation checks must pass before code generation. QUIT immediately on ANY failure.

**Validation Protocol Details:** See section 6.1

**Report Format:** "Successfully generated stepN_name.py - all validations passed"

---

### 2.4.2 rq_inspect

**File:** `.claude/agents/rq_inspect.md`

**Frontmatter Requirements:**
- name: rq_inspect
- description: Validates analysis step outputs
- tools: Read, Write, Edit, Bash

**Goal:** Verify step ran correctly (inputs correct, outputs match expectations)

**Expects:** Master specifies chX/rqY and files to inspect

**Steps:**
1. Read: docs/v4/best_practices/universal.md
2. Read: docs/v4/best_practices/workflow.md
3. Read: results/chX/rqY/status.yaml (including prior context_dumps)
4. Check: All prior ANALYSIS steps (step01...step(N-1)) in status.yaml analysis_steps section = success, current analysis step (stepN) = pending (else FAIL using STEP circuit breaker)
5. Read: docs/v4/templates/inspect_criteria.md
6. Read: results/chX/rqY/docs/2_plan.md (validation criteria per step)
7. Read/Bash: Specified files and execution logs (use pandas for CSV, grep/check logs for errors/warnings/convergence)
8. Ultrathink: Four-layer validation - (1) Existence: files exist, (2) Structure: correct formats/columns/dtypes/rows, (3) Substance: values scientifically reasonable per plan.md validation criteria, (4) Execution Log: no errors/warnings, convergence confirmed, embedded validation passed (else FAIL any layer)
9. Edit: status.yaml (update this analysis step to success, write context_dump with terse summary)
10. Report: Success and quit

**Context Dump Content:**
- Step validated
- Output format confirmed
- Validation criteria met

**Report Format:** "Successfully validated stepN outputs for chX/rqY"

---

## 2.5 Results Agents

### 2.5.1 rq_plots

**File:** `.claude/agents/rq_plots.md`

**Frontmatter Requirements:**
- name: rq_plots
- description: Generates plotting code
- tools: Read, Write, Bash

**Goal:** Generate plots.py per plan specifications

**Expects:** Master specifies chX/rqY to generate plots for

**Note:** rq_plots reads tools/plots.py SOURCE CODE directly (step 5) to understand how to CALL existing plotting functions. This is intentional - ensures consistent plot themes across all 50 RQs by using only pre-existing functions. If needed function doesn't exist in tools/plots.py → FAIL (master and user add function manually, then retry).

**Critical Design (Option B Architecture):**
- **Plot source CSVs created by g_code:** Analysis pipeline includes plot data preparation steps that create plots/*.csv files (aggregated from multiple analysis outputs)
- **rq_plots is visualization-only:** Reads plot source CSVs, generates plotting code calling tools/plots.py functions, NO data aggregation logic
- **Separation of concerns:** Data manipulation = analysis agents (g_code), Visualization = plotting agent (rq_plots)
- **Built-in validation:** If source CSV missing → rq_plots FAILS → signals analysis step incomplete

**Steps:**
1. Read: docs/v4/best_practices/universal.md
2. Read: docs/v4/best_practices/workflow.md
3. Read: results/chX/rqY/status.yaml (including prior context_dumps)
4. Check: All prior steps = success, this step onwards = pending (else FAIL)
5. Read: docs/v4/templates/plots.md
6. Read: tools/plots.py (source code - see existing functions and usage patterns)
7. Read: results/chX/rqY/docs/2_plan.md (plot specifications with source CSV paths)
8. Check: All plot source CSVs exist in plots/*.csv (else FAIL with missing file list - signals analysis incomplete)
9. Ultrathink: Map 2_plan.md plot descriptions → tools/plots.py functions (using source CSVs, no data aggregation)
10. Check: All required plotting functions exist in tools/plots.py (else FAIL with missing function list)
11. Bash: Create results/chX/rqY/plots/plots.py
12. Write: Add generated code:
    - Import statements (from tools.plots import ...)
    - setup_plot_style() call
    - For each plot: Read source CSV → call plotting function → save PNG
    - Absolute paths always
    - UTF-8 encoding
    - NO data aggregation/transformation logic
13. Edit: status.yaml (update this step to success, write context_dump with terse summary)
14. Report: Success and quit

**Context Dump Content:**
- Plots generated count
- Data sources used

**Report Format:** "Successfully generated plots.py for chX/rqY - [N] plots specified"

---

### 2.5.2 rq_results

**File:** `.claude/agents/rq_results.md`

**Frontmatter Requirements:**
- name: rq_results
- description: Validates scientific plausibility and creates results summary
- tools: Read, Write, Bash, WebSearch

**Goal:** Validate scientific plausibility of results, flag anomalies, generate summary.md

**Expects:** Master specifies chX/rqY to summarize

**Steps:**
1. Read: docs/v4/best_practices/universal.md
2. Read: docs/v4/best_practices/workflow.md
3. Read: results/chX/rqY/status.yaml (including prior context_dumps)
4. Check: All prior steps = success, this step onwards = pending (else FAIL)
5. Read: docs/v4/templates/results.md
6. Read: ALL result files + plots (multimodal inspection)
   - First check: All expected PNG files exist (from 2_plan.md plot specifications)
     - If any PNG missing → FAIL with "plots.py not executed successfully, missing: [list]"
   - Data files: Use Bash + pandas.head() for CSVs (theta_scores, item_parameters, lmm_results, etc.)
   - Plot files: Use Read tool on ALL PNG files (Read tool supports multimodal image inspection per Claude Code)
   - Log files: Check for warnings, convergence issues, validation messages
   - 1_concept.md: Read for theoretical context
   - 2_plan.md: Read for expectations and substance validation criteria
7. Ultrathink + WebSearch: Validate scientific plausibility THEN synthesize results
   - **Plausibility Checks (flag anomalies, don't fail):**
     - a) Value ranges scientifically reasonable (theta ∈ [-3,3], p ∈ [0,1], r ∈ [-1,1], effect sizes typically < 2.0)
     - b) Direction of effects match cognitive neuroscience (age: older worse, delay: memory decreases, use WebSearch if uncertain)
     - c) Sample characteristics reasonable (N matches plan.md, missing data within tolerance, exclusions justified, confidence rating response patterns documented - % using full range vs extremes only per section 1.4)
     - d) Model diagnostics acceptable (convergence confirmed in logs, fit indices reasonable, no fatal warnings)
     - e) Visual plot inspection coherent with statistics (trajectories decline, error bars match significance, residuals acceptable)
     - f) Cross-reference 2_plan.md expectations (outputs match expected files/rows/columns/ranges from substance criteria)
   - **Anomaly Flagging (document in summary Sections 3-4, don't trace root causes):**
     - Implausible values: "Theta scores exceed ±3 for N participants (investigate extraction?)"
     - Wrong direction: "Older adults show BETTER memory (β = +0.5, p < 0.01) - contradicts neurodegeneration, investigate coding?"
     - Impossible statistics: "Correlation r = 1.23 (mathematically impossible, check calculation)"
     - Contradictions: "p < 0.001 but Cohen's d = 0.05 (statistically significant but trivial effect, check N)"
     - Unexpected nulls: "Hypothesis predicted delay effect, found β = 0.01, p = 0.89 (power issue? measurement error?)"
   - **Synthesis:** Integrate findings from 6 sources (context_dumps, data files, plots visual, logs, concept.md, plan.md) and map to results.md template 5 sections
8. Bash: Create results/chX/rqY/results/summary.md
9. Write: Generate summary.md following results.md template
   - Section 1 (Statistical Findings): Key results with sample characteristics
   - Section 2 (Plot Descriptions): What each plot shows (based on visual inspection)
   - Section 3 (Interpretation): Domain-specific insights + Unexpected Patterns (INCLUDE ANOMALIES FLAGGED in Step 6 with investigation suggestions)
   - Section 4 (Limitations): Sample/methodological/technical limitations + confidence rating response patterns (per section 1.4) + PLAUSIBILITY CONCERNS from Step 6 (implausible values, wrong directions, contradictions)
   - Section 5 (Next Steps): Follow-up questions, future RQs
   - **Tone:** Healthy skepticism - results from automated pipeline, validation required before acceptance
10. Edit: status.yaml (update this step to success, write context_dump with terse summary)
11. Report: Success and quit

**Context Dump Content:**
- Results validated for scientific plausibility
- N anomalies flagged (details in summary.md Sections 3-4) OR plausibility acceptable
- Summary documented in results/summary.md

**Report Format:** "Successfully created summary.md for chX/rqY (N anomalies flagged)" or "Successfully created summary.md for chX/rqY (plausibility acceptable)"

---

## 2.6 General-Purpose Agents

### 2.6.1 g_conflict

**File:** `.claude/agents/g_conflict.md`

**Frontmatter Requirements:**
- name: g_conflict
- description: Detects conflicts within/between documents
- tools: Read

**Goal:** Report ALL conflicts between specified documents

**Expects:** Master provides document paths to compare

**Steps:**
1. Read: docs/v4/best_practices/universal.md
2. Circuit Breaker: Verify master provided document paths, verify all paths exist and are readable (QUIT if not)
3. Read: All specified documents (entire contents)
4. Ultrathink: Identify ALL conflicts (generic, structured, semantic) within/between documents
5. Report: Conflicts grouped by topic, ranked by severity (CRITICAL/MODERATE/MINOR) with line numbers, OR "No conflicts detected", quit

**Note:**
- General-purpose tool, not RQ-specific
- Does NOT use status.yaml (intentional design)
- Can compare ANY documents across entire codebase
- Used for validation at workflow steps 10 and 13
- Does NOT read agent_best_practices.md (too simple, hard-codes essential circuit breakers only)

**Report Format:**
```
[SEVERITY] Topic: Brief description
- Document: path/to/file.md, Line X: "quoted text"
- Document: path/to/other.md, Line Y: "conflicting text"
```
OR "No conflicts detected"

---

### 2.6.2 g_debug

**File:** `.claude/agents/g_debug.md`

**Frontmatter Requirements:**
- name: g_debug
- description: Debugs code with git safety, reports solution (doesn't fix original)
- tools: Read, Write, Edit, Bash, WebSearch, mcp__context7__resolve-library-id, mcp__context7__get-library-docs

**Goal:** Find root cause and solution (in-place debugging with git rollback, no permanent changes)

**Expects:** Master specifies ALL required information:
- code_path: Path to failing script (e.g., results/ch5/rq1/code/step03_irt_calibration.py)
- log_path: Path to error log (e.g., results/ch5/rq1/logs/step03_irt_calibration.log)
- instructions_path: Path to 4_analysis.yaml (e.g., results/ch5/rq1/docs/4_analysis.yaml)
- step_id: Step identifier (e.g., step03)

**Note:** g_debug edits files IN PLACE (not in sandbox) to avoid path/import issues. Safety is ensured via git commit + push to remote BEFORE any changes, then rollback after solution found.

**Steps:**
1. Read: docs/v4/best_practices/universal.md
2. Read: docs/v4/best_practices/code.md
3. **SAFETY PROTOCOL (Triple-Checked Remote Backup):**
   - 3a. Bash: `git status` (check working directory clean)
   - 3b. QUIT if uncommitted changes detected → master must run /save first
   - 3c. Bash: `git add -A && git commit -m "DEBUG START: [step_id] [timestamp]"`
   - 3d. Bash: `git push origin main` ← CRITICAL REMOTE BACKUP
   - 3e. Bash: Check push exit code (QUIT if push failed)
   - 3f. Report: "Remote backup confirmed at [commit_hash], safe to proceed with debugging"
4. Read: 4_analysis.yaml (instructions g_code used to generate code)
5. Read: Generated code (includes inline g_code reasoning from step 6 of g_code workflow)
6. Read: Log file (traceback/error message)
7. Read: Other suspected files if needed (data files, tool source code, etc.)
8. **Ultrathink - CLASSIFY ERROR TYPE:**
   - Syntax error? (g_code generated invalid Python)
   - Data error? (input CSV missing columns/wrong format/wrong values)
   - Instructions error? (4_analysis.yaml specified wrong column names/paths/parameters)
   - Logic error? (code is valid Python but wrong approach)
   - Import error? (function doesn't exist/wrong module/wrong signature)
   - Column error? (CSV columns don't match expectations documented in code header)
9. Edit: Fix code in place (actual location, not sandbox)
10. Bash: Run code in actual location
11. Check: If still failing, repeat steps 9-10 until code runs successfully (else continue)
   - **Circuit Breaker 1:** Same error message 3× in a row → QUIT with STEP ERROR (not making progress)
   - **Circuit Breaker 2:** Same error type 5× total → QUIT with STEP ERROR (fundamental design issue)
   - **Absolute Maximum:** 10 iterations → QUIT with STEP ERROR (bug too complex, manual intervention required)
12. **ROLLBACK (Safe because pushed to remote):**
   - 12a. Bash: `git reset --hard HEAD~1` (rollback to pre-debug state)
   - 12b. Bash: `git status` (verify clean rollback)
   - 12c. If rollback failed → Bash: `git pull origin main` (recover from remote backup)
13. **ENHANCED REPORT:**
   - Root cause: [detailed description]
   - Error type: [syntax|data|instructions|logic|import|column]
   - Solution: [exact fix to apply to which file]
   - Affected file: [file path that needs editing]
   - Suggested improvements:
     - g_code prompt: [if g_code should have caught this during 4-layer validation]
     - 4_analysis.yaml: [if rq_analysis generated bad instructions]
     - rq_planner: [if plan.md had wrong specifications]
     - validation: [if validation should have caught this]
     - tool_inventory.md: [if tool documentation was wrong/incomplete]

**Purpose:**
- Understand root cause with full context (instructions + reasoning + code + logs)
- Classify error type to identify which agent/process caused the bug
- Prevent black-box fixes (master applies, not agent) for user understanding
- Improve agent prompts/documentation based on findings
- Systematic improvement cycle with targeted fixes
- Safe experimentation via git remote backup + rollback

**Report Format Example:**
```markdown
## DEBUG REPORT: step03_irt_calibration.py

**Root Cause:** Column name mismatch - code expects 'theta_score' but CSV has 'theta'

**Error Type:** INSTRUCTIONS ERROR

**Solution:**
Edit results/ch5/rq1/code/step03_irt_calibration.py:
  Line 45: Change `df['theta_score']` → `df['theta']`

**Affected File:** results/ch5/rq1/code/step03_irt_calibration.py

**Why This Happened:**
- 4_analysis.yaml specified output column as 'theta_score'
- But calibrate_grm() actually outputs 'theta' (per tool_inventory.md)
- rq_analysis didn't verify column names against tool documentation

**Suggested Improvements:**
1. **rq_analysis prompt:** Add step to cross-reference output column names with tool_inventory.md signatures
2. **g_code 4d validation:** Enhance column check to validate OUTPUT columns match tool signatures (currently only checks INPUT columns)
3. **tool_inventory.md:** Add explicit output column documentation for calibrate_grm()

**Rollback Status:** ✓ Successfully rolled back to commit [hash] - codebase unchanged
```

**CRITICAL SAFETY RULES:**
- NEVER start debugging without remote git push (step 2d)
- NEVER skip rollback (step 11) - codebase MUST be identical to pre-debug state
- If rollback fails → recover from remote via git pull (step 11c)
- Master verifies codebase clean before applying reported solution

---

# 3. WORKFLOW & ORCHESTRATION

## 3.1 Master Orchestration Workflow

**Specification:** docs/v4/automation.md

**Purpose:** Master's orchestration workflow for RQ pipeline

**17-Step Workflow:**

1. User: "Begin chX/rqY"
2. Master reads: docs/v4/automation.md
3. Master invokes: rq_builder with "Build chX/rqY"
4. Master invokes: rq_concept with "Create 1_concept.md"
5. Master invokes: rq_scholar with "Inspect 1_concept.md"
6. Master invokes: rq_stats with "Inspect 1_concept.md"
7. Master asks user: "Verify results/chX/rqY/docs/1_concept.md" **(SINGLE USER APPROVAL GATE)**
8. User responds: "Looks good. Continue" (or requests changes)
9. Master invokes: rq_planner with "Create 2_plan.md"
10. Master invokes: g_conflict with "Compare 1_concept.md, 2_plan.md"
11. Master invokes: rq_tools with "Create 3_tools.yaml"
12. Master invokes: rq_analysis with "Create 4_analysis.yaml"
13. Master invokes: g_conflict with "Compare 2_plan.md, 3_tools.yaml, 4_analysis.yaml"
14. **CODE EXECUTION LOOP:** For each step in analysis_steps:
    - Master checks: status.yaml (which step next?)
    - Master invokes: g_code with "Generate code for step N"
    - Master runs: bash "poetry run python results/chX/rqY/code/stepN_name.py"
    - If traceback: Master invokes: g_debug with "Debug step N"
    - If g_debug reports solution: Master applies fix to code/templates
    - Master re-runs: bash "poetry run python results/chX/rqY/code/stepN_name.py" (verify fix works)
    - If still fails: Repeat g_debug → fix → re-run until success
    - Master invokes: rq_inspect with "Validate step N outputs" (only after successful execution)
    - Master updates: status.yaml (mark step N success, move to N+1)
15. Master invokes: rq_plots with "Create plots.py"
16. Master runs: bash "poetry run python results/chX/rqY/plots/plots.py"
17. Master invokes: rq_results with "Create summary.md"

**Invocation Format:**
- Master provides descriptive strings to agents
- Examples: "Build ch5/rq1", "Create 1_concept.md", "Debug step 3"
- Agents report informal text confirmations to master

**User Approval Gate:**
- Single gate: Step 7 (after 1_concept.md creation)
- User verifies concept before proceeding with planning/execution
- If user requests changes: Loop back to step 4 (rq_concept)

---

## 3.2 Orchestration Modes

**Phase 1: Manual (Initial)**
- Master = main claude
- Executes workflow steps 1-17 sequentially
- Handles each agent invocation individually
- Responds to errors immediately
- Used during v4.X development/testing

**Phase 2: Automated (After Stable)**
- Orchestrator script reads automation.md workflow
- Invokes agents sequentially per workflow
- Handles CODE EXECUTION LOOP logic automatically
- Integrates g_debug error recovery
- Specification: docs/v4/orchestrator.md

**Benefits of Both Modes:**
- Manual: Debugging flexibility, step-by-step control
- Automated: Efficiency after system stabilizes
- Both available for different use cases

---

## 3.3 Status Tracking & Pseudo-Statefulness

**status.yaml Structure:**
- Agent completion statuses (pending/success)
- Analysis step statuses (pending/success)
- Context dumps per agent (terse summaries)

**Status Checking Mechanism:**
- Agents read status.yaml file directly (using Read tool)
- Parse YAML structure using general LLM reasoning (no programmatic parser needed)
- Check: status.yaml[agent_name]['status'] == 'success' via pattern matching
- Read prior context_dumps for continuity
- Method: Look for lines like "rq_concept:\n  status: success" to determine completion
- If parsing unclear: Trigger CLARITY ERROR

**Pseudo-Statefulness Design:**
- Agents read status.yaml at invocation start
- See all prior agents' context_dumps
- Maintain continuity without loading full conversation
- Stateful behavior, stateless architecture

**Context Dump Requirements:**
- Written to status.yaml after agent completes
- YAML field under agent name
- Multiline string format
- Max 5 lines per agent
- Terse summaries only (prevent file bloat)

**Benefits:**
- Context continuity across agents
- No context window bloat
- Each agent <5k context
- Enables sequential workflow without master passing state

---

## 3.4 Error Recovery Workflow

**g_debug Integration:**
1. Analysis step script crashes (traceback in log)
2. Master invokes: g_debug with code/log/instructions paths
3. g_debug executes safety protocol (git commit + push to remote backup)
4. g_debug identifies root cause, tests fix in-place (actual file locations)
5. g_debug rolls back changes (git reset --hard to pre-debug state)
6. g_debug reports: Root cause + error type + solution + improvement suggestions

**Master Response:**
- Master applies fix to original code OR templates
- Master improves agent prompts if issue was agent-generated
- Master improves documentation if issue was spec ambiguity
- Prevents black-box changes (master understands fix before applying)

**Systematic Improvement:**
- Root causes documented
- Agent prompts updated to prevent recurrence
- Templates improved based on errors discovered
- Documentation enhanced based on confusion patterns

**Purpose:**
- Understand WHY errors occur
- Improve system systematically
- Prevent black-box fixes
- Build institutional knowledge

---

# 4. DOCUMENTATION TEMPLATES

**Note:** This section specifies WHAT templates should contain. Actual template files built separately in docs/v4/templates/.

---

## 4.1 Setup Templates

### 4.1.1 build_folder.md

**File:** docs/v4/templates/build_folder.md

**Purpose:** Specification for RQ folder structure

**Audience:** rq_builder agent when creating new RQ folders

**Required Content:**
- Exact folder names (docs/, data/, code/, logs/, plots/, results/)
- Creation order (which folders first)
- Verification steps (how to check folder exists and is empty)
- Folder purposes (what goes in each folder)

**Structure to Specify:**
```
results/chX/rqY/
  status.yaml
  docs/
  data/
  code/
  logs/
  plots/
  results/
```

**Implementation:** Template file contains detailed instructions for rq_builder

---

### 4.1.2 build_status.md

**File:** docs/v4/templates/build_status.md

**Purpose:** Specification for status.yaml initial structure

**Audience:** rq_builder agent when creating status.yaml file

**Required Content:**
- YAML structure format
- Agent names (10 RQ-specific agents - general-purpose agents excluded, see note below)
- Initial status values (all pending)
- context_dump field structure (empty initially)
- analysis_steps section structure (added later by rq_analysis)

**Structure to Specify:**
- Agent statuses: rq_builder, rq_concept, rq_scholar, rq_stats, rq_planner, rq_tools, rq_analysis, rq_inspect, rq_plots, rq_results (10 total)
- Fields per agent: status (pending/success), context_dump (multiline string)
- analysis_steps section: Added by rq_analysis, contains step-by-step statuses

**Note on Agent Count:**
- 10 RQ-specific agents appear in status.yaml (listed above)
- 3 general-purpose agents (g_code, g_conflict, g_debug) do NOT use status.yaml per their specifications and are excluded
- Total v4.X architecture has 13 agents (10 RQ-specific + 3 general-purpose)

**Implementation:** Template file contains YAML structure for rq_builder to create

---

## 4.2 RQ Documentation Templates

### 4.2.1 concept.md

**File:** docs/v4/templates/concept.md

**Purpose:** Specification for 1_concept.md format

**Audience:** rq_concept agent when creating 1_concept.md

**Required Sections:**
- RQ title and ID (e.g., "RQ 5.1: Trajectory of Forgetting - What Domain")
- Research question statement (clear, answerable question)
- Theoretical background (episodic memory theory grounding)
- Hypothesis (directional prediction)
- Memory domains (What/Where/When specification)
- Analysis approach (IRT, LMM, CTT, etc.)
- Data source (master.xlsx tags OR other RQ outputs with dependencies)

**Implementation:** Template file provides structure for rq_concept to fill

---

### 4.2.2 plan.md

**File:** docs/v4/templates/plan.md

**Purpose:** Specification for 2_plan.md format

**Audience:** rq_planner agent when creating 2_plan.md

**Required Sections:**
- Step-by-step analysis plan (numbered steps)
- Input specifications per step (file paths, formats)
- Output specifications per step (file paths, formats)
- Expected data formats per step (column names, data types)
- Validation requirement per step (MANDATORY: State "Validation tools MUST be used after analysis tool execution" - specific validation tools determined by rq_tools)
- Dependencies on other RQs (if applicable, which RQs provide input)

**Implementation:** Template file provides structure for rq_planner to fill

---

### 4.2.3 tools.md

**File:** docs/v4/templates/tools.md

**Purpose:** Specification for 3_tools.yaml format (Tool Catalog Architecture)

**Audience:** rq_tools agent when creating 3_tools.yaml

**Top-Level Structure:**
- analysis_tools: Dictionary of unique analysis tools (each tool listed once)
- validation_tools: Dictionary of unique validation tools (each tool listed once)
- summary: Metadata section (tool counts, decisions embedded)

**Required Fields Per Analysis Tool:**
- Tool module (e.g., tools.analysis_irt)
- Tool function (e.g., calibrate_grm)
- Full signature with type hints (e.g., "calibrate_grm(df: pd.DataFrame, dimensions: List[str]) -> Tuple[pd.DataFrame, pd.DataFrame]")
- **validation_tool:** Reference to validation_tools key (e.g., "validate_irt_calibration")
- Input formats (exact column names expected)
- Output formats (exact column names produced)
- Parameter specifications (values, types, constraints)

**Required Fields Per Validation Tool:**
- Validation module (e.g., tools.validation)
- Validation function (e.g., validate_irt_calibration)
- Full signature with type hints
- Input formats (uses analysis tool outputs)
- Validation criteria (what the validation tool checks)
- Expected validation outputs (pass/fail, error messages)

**Catalog Approach:** Each tool appears ONCE in catalog (deduplication). rq_analysis maps tools to steps via 2_plan.md + 3_tools.yaml catalog references.

**Implementation:** Template file provides YAML structure for rq_tools to fill

---

### 4.2.4 analysis.md

**File:** docs/v4/templates/analysis.md

**Purpose:** Specification for 4_analysis.yaml format

**Audience:** rq_analysis agent when creating 4_analysis.yaml

**Required Sections Per Step:**
- Step name (from docs/v4/names.md)
- Step number (zero-padded)

**Analysis Tool Call:**
- Tool module and function (from 3_tools.yaml)
- Full function signature (with type hints - CRITICAL for g_code validation)
- Input files (paths relative to results/chX/rqY/, expected columns)
- Output files (paths relative to results/chX/rqY/, expected columns)
- Parameters (values, types)

**Validation Tool Call:**
- Validation module and function (from 3_tools.yaml)
- Full function signature (with type hints)
- Input files (analysis tool outputs)
- Validation criteria (what to check)
- Expected behavior (raise error if validation fails)

**Log file path** (captures both analysis and validation output)

**Critical Requirements:**
- MUST include full function signatures with type hints for BOTH analysis and validation
- Each step MUST end with validation tool call
- g_code generates scripts that run analysis THEN validation
- Validation failures halt execution (prevents cascading errors)

**Implementation:** Template file provides YAML structure for rq_analysis to fill

---

## 4.3 Validation Templates

### 4.3.1 scholar_report.md

**File:** docs/v4/templates/scholar_report.md

**Purpose:** Specification for scholarly validation feedback format

**Audience:** rq_scholar agent when creating standalone 1_scholar.md validation report

**Required Sections:**
- Claims extracted from concept.md (numbered list)
- Evidence sources (literature, theory references)
- Validation results per claim (supported/unsupported)
- Recommendations (corrections, additions, clarifications)

**Implementation:** Template file provides structure for rq_scholar to write standalone 1_scholar.md file

---

### 4.3.2 stats_report.md

**File:** docs/v4/templates/stats_report.md

**Purpose:** Specification for statistical validation feedback format

**Audience:** rq_stats agent when creating standalone 1_stats.md validation report

**Required Sections:**
- Proposed methods from concept.md (numbered list)
- Method appropriateness per method (valid/invalid for this RQ)
- Alternative considerations (other methods to consider)
- Validation results (approved/rejected with rationale)

**Implementation:** Template file provides structure for rq_stats to write standalone 1_stats.md file

---

### 4.3.3 inspect_criteria.md

**File:** docs/v4/templates/inspect_criteria.md

**Purpose:** Validation checklist specification for rq_inspect

**Audience:** rq_inspect agent when validating step outputs

**Required Sections:**
- Input verification checks (files exist, correct formats)
- Output verification checks (files created, correct formats)
- Format verification checks (column names match expectations)
- Cross-reference with plan.md expectations (validation criteria from 2_plan.md)

**Implementation:** Template file provides checklist structure for rq_inspect

---

## 4.4 Output Templates

### 4.4.1 plots.md

**File:** docs/v4/templates/plots.md

**Purpose:** Plotting specifications and requirements

**Audience:** rq_plots agent when generating plots.py

**Required Sections:**
- Available plotting functions (from tools/plots.py)
- Required parameters per function
- Output formats (PNG, dimensions, DPI)
- File naming conventions (plot names from docs/v4/names.md)

**Implementation:** Template file provides plotting specifications for rq_plots

---

### 4.4.2 results.md

**File:** docs/v4/templates/results.md

**Purpose:** Results summary template specification

**Audience:** rq_results agent when creating summary.md

**Required Sections:**
- Statistical findings (key results from analysis)
- Plot descriptions (what each plot shows)
- Interpretation (what results mean theoretically)
- Limitations (acknowledged constraints)
- Next steps (follow-up questions, future RQs)

**Implementation:** Template file provides summary structure for rq_results

---

## 4.5 Support Documentation

### 4.5.1 names.md

**File:** docs/v4/names.md

**Purpose:** Naming convention registry specification (live document)

**Audience:** rq_planner, rq_tools, rq_analysis when needing step/file/variable names

**Required Content:**
- Category headers (step names, file names, variable names)
- Convention patterns (format specifications)
- Examples per convention
- RQ introduced (tracking where convention first used)

**Rules:**
- Never change existing conventions (only append new ones)
- Add naming conventions as needed per RQ
- All step names, file names, variable names registered here
- Cross-referenced from rq_planner, rq_tools, rq_analysis

**Implementation:** Live document following TDD philosophy

**TDD Initialization Approach:**
- names.md starts EMPTY (no pre-populated conventions)
- RQ 5.1 (first RQ) WILL FAIL at rq_tools step 9 (missing names in registry)
- Master and user MANUALLY add required naming conventions to names.md
- Subsequent RQs use existing conventions OR add new ones (with master+user approval)
- Ensures conventions emerge from actual needs, not speculation

**Header Structure (Design Decision F0a - 2025-11-16):**
1. **PURPOSE** - Explains naming registry role in v4.X workflow
2. **TDD APPROACH** - Empty start, RQ 5.1 expected failure at rq_tools step 9, manual population process
3. **USAGE INSTRUCTIONS** - Check registry before adding new conventions, never modify existing entries, only append new, document which RQ introduced convention
4. **CONVENTION RULES** - Never change existing conventions (breaks compatibility with past RQs), only append new conventions

**Convention Format (Design Decision F0b - 2025-11-16):**
- **Structure:** YAML format organized by category
- **Categories:** Four main sections
  - `step_names:` - Analysis step naming patterns
  - `file_names:` - Data file, script file, output file naming patterns
  - `variable_names:` - DataFrame column, variable naming patterns
  - `plot_names:` - Plot file naming patterns
- **Entry Fields:** Each convention entry contains
  - `name:` - Identifier for the convention type
  - `pattern:` - Format template with placeholders (e.g., `stepNN_<verb>_<noun>`)
  - `example:` - Concrete instance demonstrating pattern (e.g., `step01_calibrate_irt`)
  - `introduced:` - Which RQ first required this convention (e.g., `RQ 5.1`)
  - `notes:` - Optional clarifications or usage context
- **Organization:** Grouped by category (not chronologically) for easy scanning and reference

**Example Entry Structure:**
```
step_names:
  - name: calibration
    pattern: stepNN_<verb>_<noun>
    example: step01_calibrate_irt
    introduced: RQ 5.1
    notes: "IRT model calibration using GRM"
```

---

### 4.5.2 orchestrator.md

**File:** docs/v4/orchestrator.md

**Purpose:** Phase 2 automated orchestration specification

**Audience:** Developer building orchestrator script (future work)

**Status:** Not coded yet (Phase 2 feature)

**Required Content:**
- Automated script concept (reads automation.md workflow)
- Agent invocation mechanism (sequential per workflow)
- Loop logic (CODE EXECUTION LOOP handling)
- Error recovery (g_debug integration)
- Status tracking (reading/updating status.yaml)

**Implementation:** Conceptual reference, actual script built later

---

### 4.5.3 thesis/

**Files:**
- docs/v4/thesis/ANALYSES_CH5.md
- docs/v4/thesis/ANALYSES_CH6.md
- docs/v4/thesis/ANALYSES_CH7.md

**Purpose:** Chapter RQ specifications from thesis

**Location:** Moved from thesis/analyses/ to docs/v4/thesis/

**Required Content Per File:**
- TABLE OF CONTENTS with RQ list
- RQ specifications (one per section, extracted from thesis)
- Cross-RQ dependencies documented (which RQs depend on which)

**Audience:** rq_concept agent extracts relevant sections

**Implementation:** Existing files moved to new location, no format changes

---

### 4.5.4 automation.md

**File:** docs/v4/automation.md

**Purpose:** Master orchestration workflow specification (17-step RQ pipeline)

**Audience:** Master (main claude) reads before executing each RQ to refresh memory on workflow steps

**Required Content:**
- Complete 17-step workflow (from section 3.1)
- Agent invocation order and format
- User approval gate (step 7)
- CODE EXECUTION LOOP logic (step 14 with g_debug error recovery)
- Error handling procedures
- Status tracking checkpoints

**Usage:**
- Master reads this file at workflow step 2 (after user requests "Begin chX/rqY")
- Refreshes memory on exact orchestration sequence
- Ensures consistent workflow across all 50 RQs

**Implementation:** Created during v4.X implementation, contains workflow from specification section 3.1

---

# 5. STANDARDS & CONVENTIONS

## 5.1 Agent Best Practices

**Specification:** docs/v4/best_practices/ (3 files: universal.md, workflow.md, code.md)

**Purpose:** Universal error handling and platform rules for all agents

**Circuit Breakers (5 Types):**

1. **EXPECTATIONS ERROR**
   - Trigger: Missing expected input (file, parameter, prerequisite)
   - Format: "EXPECTATIONS ERROR: To perform {task} I expect {expected}, but missing {missing}"
   - Action: QUIT immediately

2. **STEP ERROR**
   - Trigger: Cannot complete step as prescribed
   - Format: "STEP ERROR: Trying to complete {step} but {problem}"
   - Action: QUIT immediately

3. **TOOL ERROR**
   - Trigger: Tool execution fails
   - Format: "TOOL ERROR: Tried to use {tool} but {problem}"
   - Action: QUIT immediately

4. **CLARITY ERROR**
   - Trigger: Insufficient information to proceed
   - Format: "CLARITY ERROR: Trying to complete {step} but need {missing_info}"
   - Action: QUIT immediately

5. **SCOPE ERROR**
   - Trigger: Required action outside agent scope
   - Format: "SCOPE ERROR: Trying to complete {step}, want to {action}, but not in scope"
   - Action: QUIT immediately

**Platform Compatibility:**
- ASCII-only output (no Unicode characters)
- Windows cp1252 compatibility
- UTF-8 file encoding for all writes
- Test before output: echo "test" in terminal before any Unicode
- Replace Unicode: arrows → with ->, checkmarks with [PASS], etc.

**Poetry Environment:**
- All script executions: poetry run python path/to/script.py
- Never use pip install
- Check dependencies: poetry show

**Context Dump Format:**
- Terse summaries only (prevent file bloat)
- Max 5 lines per agent
- Key decisions, domains, analysis type only
- Written to status.yaml after each agent completes

**Report Format:**
- Informal text to master
- Confirm task completion without errors
- If errors: Specify which circuit breaker triggered

**Data Source Boundaries:**
- RAW data: master.xlsx participant data OR outputs from other completed RQs
- DERIVED data: Created by analysis step scripts
- If source unclear: Trigger CLARITY ERROR

---

## 5.2 File Structure Schema

**Standard Schema:**

Visual representation of required folder/file structure:

```
results/chX/rqY/                    (root for specific RQ)
  status.yaml                       (agent statuses, context dumps)
  docs/                             (specifications)
    1_concept.md                    (RQ concept, validated)
    2_plan.md                       (analysis plan, step-by-step)
    3_tools.yaml                    (tool specifications)
    4_analysis.yaml                 (analysis recipe per step)
  data/                             (analysis outputs)
    stepN_name.csv                  (CSV outputs from steps)
  code/                             (generated scripts)
    stepN_name.py                   (Python scripts per step)
  logs/                             (execution logs)
    stepN_name.log                  (Log files per step)
  plots/                            (visualizations)
    plots.py                        (Plotting script)
    plot_name.png                   (Generated plots)
  results/                          (final summaries)
    summary.md                      (Results summary)
```

**Folder Purposes:**
- **docs/:** RQ specifications, planning documents
- **data/:** Analysis step outputs (CSV files)
- **code/:** Generated Python scripts per step
- **logs/:** Execution logs per step
- **plots/:** Plotting script and generated visualizations
- **results/:** Final summary and interpretation

---

## 5.3 Naming Conventions

**Step Naming:**
- Format: stepN (zero-padded step number)
- Examples: step01, step02, ..., step10
- Source: docs/v4/names.md (registry)

**File Naming:**
- Format: stepN_name.ext
- stepN: Zero-padded step number
- name: Descriptive step name from docs/v4/names.md
- ext: .py (code), .csv (data), .log (logs)
- Examples: step01_calibrate_irt.py, step02_purify_items.csv

**Variable Naming:**
- chX: {ch5, ch6, ch7} (chapter numbers)
- rqY: {rq1, rq2, ..., rq15} (RQ numbers per chapter)

**Enforcement:**
- All names registered in docs/v4/names.md (registry built via TDD)
- rq_tools/rq_analysis CHECK registry, FAIL if required name missing
- First RQ (5.1) expected to fail initially (registry empty)
- Master and user add required names when failures occur
- Subsequent RQs use existing names OR fail and add new ones
- Never change existing conventions (only append new ones)

---

## 5.4 Context Dump Format

**Location:** status.yaml, under agent name

**Structure:**
```
agent_name:
  status: success
  context_dump: |
    Line 1: Key information
    Line 2: Key information
    Line 3: Key information
    Line 4: Key information
    Line 5: Key information
```

**Requirements:**
- Max 5 lines per agent
- Terse summaries only (no verbose explanations)
- Key information only:
  - Memory domains (What/Where/When)
  - Analysis type (IRT/LMM/CTT)
  - Key decisions made
  - Critical information for downstream agents

**Purpose:**
- Enable pseudo-statefulness
- Maintain continuity without context bloat
- Next agents read prior context_dumps

**Benefits:**
- Context window stays lean (<5k per agent)
- Stateful behavior, stateless architecture
- Prevents file bloat (terse summaries)

---

## 5.5 Signature Enforcement

**Requirement:** 4_analysis.yaml MUST include full function signatures with type hints

**Format Example:**
```
signature: "purify_items(item_params: pd.DataFrame, thresholds: dict) -> pd.DataFrame"
```

**Purpose:**
- Forces rq_analysis to read tools_inventory.md before generating specs
- Prevents API guessing (v3.0 failure mode)
- Enables g_code pre-generation validation

**Benefits:**
- Catches API mismatches BEFORE code generation
- Documents expected types for debugging
- Prevents cascading errors (1 API error → 5+ downstream failures)

**Validation:**
- g_code uses inspect.signature to verify match
- QUIT on signature mismatch (SIGNATURE ERROR)

---

# 6. TECHNICAL SPECIFICATIONS

## 6.1 g_code Validation Protocol

**Purpose:** Validate BEFORE generating code (fail-fast strategy)

**4-Layer Validation:**

1. **Import Check**
   - Method: importlib.import_module(tool_module) + hasattr(module, tool_function)
   - Verifies: Tool module/function exists
   - Failure: TOOL ERROR

2. **Signature Check**
   - Method: inspect.signature(function) matches documented signature
   - Verifies: Function signature matches 4_analysis.yaml specification
   - Failure: SIGNATURE ERROR

3. **Input File Check** (if step >1)
   - Method: os.path.exists(input_file_path)
   - Verifies: Expected input files exist
   - Failure: INPUT ERROR

4. **Column Check** (if CSV)
   - Method: pd.read_csv(file, nrows=0).columns matches expected
   - Verifies: CSV column names match expected format
   - Failure: FORMAT ERROR

**Quit-on-Failure Policy:**
- ALL validation checks must pass
- QUIT immediately on ANY failure
- Report specific error to master
- Do NOT generate code if validation fails

**Benefits:**
- Catches errors pre-execution (saves 60+ minutes per IRT calibration)
- Prevents cascading failures
- Clear error messages (specific validation failure)

---

## 6.2 Scope Boundaries

**Purpose:** Prevent mock data catastrophe (v3.0 failure)

**RAW Data Definition:**
- Extractable from master.xlsx participant data
- OR outputs from other completed RQs
- Created OUTSIDE analysis pipeline
- Examples: VR item responses, demographic data, cognitive test scores, theta scores from prior RQ

**DERIVED Data Definition:**
- Requires statistical analysis
- Created BY analysis step scripts
- Created INSIDE analysis pipeline
- Examples: IRT theta scores, item parameters, LMM coefficients, purified item lists

**Circuit Breaker:**
- If data source unclear → CLARITY ERROR
- Agent MUST quit, report to master
- Master clarifies in 1_concept.md + 2_plan.md

**Specification:**
- 1_concept.md states data source explicitly
- 2_plan.md documents dependencies on other RQs
- If dependency: States which RQ provides which data

**Purpose:**
- Prevent agents from generating mock data
- Ensure data source is always clear
- Document dependencies explicitly

---

## 6.3 Cross-RQ Dependencies

**Specification Location:** docs/v4/thesis/ANALYSES_CHX.md

**Content:**
- States which RQs provide input data to which other RQs
- Documents data flow between RQs
- Examples: "RQ 5.2 uses theta scores from RQ 5.1"

**Tracking Mechanism:**
- 1_concept.md documents RQ dependencies
- 2_plan.md specifies which files from which RQs
- Example: "Input: results/ch5/rq1/data/step03_theta_scores.csv"

**Workflow:**
1. rq_concept extracts dependency info from ANALYSES_CHX.md
2. Writes to 1_concept.md "Data Source" section
3. rq_planner reads 1_concept.md dependencies
4. Specifies exact file paths in 2_plan.md
5. rq_analysis includes dependency files in 4_analysis.yaml

**Benefits:**
- Clear data provenance
- Explicit RQ execution order
- Prevents circular dependencies
- Documents data flow for thesis

---

## 6.4 Platform Requirements

**Operating System:** Windows

**Environment Manager:** Poetry (never pip install)

**File Encoding:** UTF-8 for all writes

**Output Encoding:** ASCII-only (no Unicode characters)
- Arrows: Use -> not →
- Checkmarks: Use [PASS] not ✓
- Test before output: echo "test" in terminal

**Shell:** Bash (not PowerShell)
- Use bash commands, not PowerShell cmdlets
- Example: ls -lah (not Get-ChildItem)

**Script Execution:** poetry run python path/to/script.py

**Path Format:**
- Absolute paths when needed
- Relative paths to results/chX/rqY/ in specifications

---

## 6.5 Integration

**Git Workflow:**
- Handled by /save command (unchanged from v3.0)
- Commits before context-manager curation (rollback point)
- Commits after context-manager curation (curated state)
- All uncommitted work saved (agents, tools, docs, tests)

**Poetry Dependency Management:**
- Add dependencies: poetry add package-name
- Add dev dependencies: poetry add --group dev package-name
- Install all: poetry install
- Check installed: poetry show
- Run scripts: poetry run python script.py

**MCP Tool Usage:**
- Context7 MCP: resolve-library-id, get-library-docs
- Used by: rq_tools, g_code, g_debug
- Purpose: Fetch up-to-date library documentation

**IDE Integration:**
- IDE MCP: getDiagnostics, executeCode
- Purpose: Language diagnostics, Jupyter code execution

---

# 7. QUICK REFERENCE

## 7.1 Agent Lookup Table

| Agent | Purpose | Reads | Writes | Reports to |
|-------|---------|-------|--------|------------|
| rq_builder | Build folder structure | agent_best_practices, build_folder, build_status | status.yaml, folders | Master: "Successfully built chX/rqY" |
| rq_concept | Extract RQ concept | agent_best_practices, status.yaml, concept template, thesis/ANALYSES_CHX | 1_concept.md, status.yaml context_dump | Master: "Successfully created 1_concept.md" |
| rq_scholar | Validate scholarly accuracy | agent_best_practices, status.yaml, scholar_report template, 1_concept.md, thesis/methods.md | 1_scholar.md, status.yaml context_dump | Master: "Validated - [N] claims verified, wrote 1_scholar.md" |
| rq_stats | Validate statistical methods | agent_best_practices, status.yaml, stats_report template, 1_concept.md, thesis/methods.md | 1_stats.md, status.yaml context_dump | Master: "Validated - methods appropriate, wrote 1_stats.md" |
| rq_planner | Create analysis plan | agent_best_practices, status.yaml, plan template, 1_concept, data_structure, tool_inventory, names | 2_plan.md, status.yaml context_dump | Master: "Created 2_plan.md - [N] steps" |
| rq_tools | Specify tool usage | agent_best_practices, status.yaml, tools template, 2_plan, tool_inventory, names | 3_tools.yaml, status.yaml context_dump | Master: "Created 3_tools.yaml - [N] tools" |
| rq_analysis | Create analysis recipe | agent_best_practices, status.yaml, analysis template, 2_plan, 3_tools, names | 4_analysis.yaml, status.yaml (add analysis_steps + context_dump) | Master: "Created 4_analysis.yaml - [N] steps" |
| g_code | Generate validated code | agent_best_practices, 4_analysis.yaml (step_N) | stepN_name.py | Master: "Generated stepN_name.py - validations passed" |
| rq_inspect | Validate step outputs | agent_best_practices, status.yaml, inspect_criteria, 2_plan, step outputs | status.yaml (step success + context_dump) | Master: "Validated stepN outputs" |
| rq_plots | Generate plotting code | agent_best_practices, status.yaml, plots template, tools/plots.py, data files | plots.py, status.yaml context_dump | Master: "Generated plots.py - [N] plots" |
| rq_results | Validate scientific plausibility + create summary | agent_best_practices, status.yaml, results template, result files, plots (multimodal), logs, concept.md, plan.md | summary.md with anomaly flags, status.yaml context_dump | Master: "Created summary.md - [N] anomalies flagged" OR "plausibility acceptable" |
| g_conflict | Detect document conflicts | agent_best_practices, specified documents | None | Master: "Found [N] conflicts" OR "No conflicts" |
| g_debug | Debug in sandbox | agent_best_practices, code/logs to debug | None (sandbox deleted) | Master: "Root cause: X. Solution: Y. Improvements: Z" |

---

## 7.2 File Path Reference

**v4.X Documentation Paths:**
- docs/v4/best_practices/universal.md (circuit breakers + platform rules for ALL agents)
- docs/v4/best_practices/workflow.md (status.yaml + context dumps for 10/13 workflow agents)
- docs/v4/best_practices/code.md (Poetry + data boundaries + MCP for 5/13 code-aware agents)
- docs/v4/templates/build_folder.md
- docs/v4/templates/build_status.md
- docs/v4/templates/concept.md
- docs/v4/templates/plan.md
- docs/v4/templates/tools.md
- docs/v4/templates/analysis.md
- docs/v4/templates/scholar_report.md
- docs/v4/templates/stats_report.md
- docs/v4/templates/inspect_criteria.md
- docs/v4/templates/plots.md
- docs/v4/templates/results.md
- docs/v4/names.md (naming registry - live document)
- docs/v4/orchestrator.md (Phase 2 concept)
- docs/v4/automation.md (master orchestration workflow - 17-step RQ pipeline)
- docs/v4/thesis/ANALYSES_CH5.md
- docs/v4/thesis/ANALYSES_CH6.md
- docs/v4/thesis/ANALYSES_CH7.md

**Existing Project Documentation:**
- docs/data_structure.md (master.xlsx tag system)
- docs/tool_inventory.md (statistical tool API reference)

**RQ Structure Paths (per RQ):**
- results/chX/rqY/status.yaml
- results/chX/rqY/docs/1_concept.md
- results/chX/rqY/docs/2_plan.md
- results/chX/rqY/docs/3_tools.yaml
- results/chX/rqY/docs/4_analysis.yaml
- results/chX/rqY/data/stepN_name.csv
- results/chX/rqY/code/stepN_name.py
- results/chX/rqY/logs/stepN_name.log
- results/chX/rqY/plots/plots.py
- results/chX/rqY/plots/plot_name.png
- results/chX/rqY/results/summary.md

**Legacy Paths (DO NOT USE):**
- _legacy/v3/agents/ (v3 agents archived here)

---

## 7.3 Workflow Checklist

**Steps 1-7: Setup & Concept Validation**
- [ ] Step 1: User requests "Begin chX/rqY"
- [ ] Step 2: Master reads docs/v4/automation.md
- [ ] Step 3: Master invokes rq_builder
- [ ] Step 4: Master invokes rq_concept
- [ ] Step 5: Master invokes rq_scholar
- [ ] Step 6: Master invokes rq_stats
- [ ] Step 7: **USER APPROVAL GATE** - Master asks user to verify 1_concept.md

**Steps 8-13: Planning & Specification**
- [ ] Step 8: User approves (or requests changes)
- [ ] Step 9: Master invokes rq_planner
- [ ] Step 10: Master invokes g_conflict (compare 1_concept.md, 2_plan.md)
- [ ] Step 11: Master invokes rq_tools
- [ ] Step 12: Master invokes rq_analysis
- [ ] Step 13: Master invokes g_conflict (compare 2_plan.md, 3_tools.yaml, 4_analysis.yaml)

**Step 14: Code Execution Loop**
For each step in analysis_steps:
- [ ] Master checks status.yaml (which step next?)
- [ ] Master invokes g_code (generate code for step N)
- [ ] Master runs bash "poetry run python results/chX/rqY/code/stepN_name.py"
- [ ] If traceback: Master invokes g_debug
- [ ] If g_debug reports solution: Master applies fix
- [ ] Master re-runs bash "poetry run python..." (verify fix works)
- [ ] If still fails: Repeat g_debug → fix → re-run until success
- [ ] Master invokes rq_inspect (validate step N outputs - only after successful execution)
- [ ] Master updates status.yaml (mark step N success, move to N+1)

**Steps 15-17: Results & Summary**
- [ ] Step 15: Master invokes rq_plots
- [ ] Step 16: Master runs bash "poetry run python results/chX/rqY/plots/plots.py"
- [ ] Step 17: Master invokes rq_results

**Common Failure Points:**
- Step 4: rq_concept can't find RQ in ANALYSES_CHX.md (check TABLE OF CONTENTS)
- Step 10/13: g_conflict finds contradictions (revise planning documents)
- Step 14 g_code: Validation failures (API mismatches, missing files, wrong columns)
- Step 14 execution: Script crashes (invoke g_debug for root cause)
- Step 14 rq_inspect: Outputs don't match plan.md expectations (check validation criteria)

---

## 7.4 Legacy Information

**v3 Agent Archival:**
- Location: _legacy/v3/agents/
- Agents moved: rq_specification, data_prep, analysis_executor, results_inspector, scholar, statistics_expert, debug
- Reason: Monolithic design caused context bloat → hallucinations → API mismatches

**v3.0 → v4.X Transition Rationale:**
- Context bloat in monolithic agents (50k+ context per agent)
- Hallucinations (e.g., invented "tests 1&2 same day" - never documented)
- API mismatches (guessed from config.yaml instead of reading tools_inventory.md)
- Cascading failures (1 error → 5+ downstream errors)
- No pre-validation (errors only discovered at runtime after 60+ minutes)

**Deprecated Files (DO NOT USE):**
- .claude/agents/rq_specification.md (use 4 agents: rq_concept, rq_planner, rq_tools, rq_analysis)
- .claude/agents/data_prep.md (RAW data extraction now specified in 1_concept.md)
- .claude/agents/analysis_executor.md (use 2 agents: g_code, rq_inspect)
- .claude/agents/results_inspector.md (use rq_inspect)
- .claude/agents/scholar.md (use rq_scholar)
- .claude/agents/statistics_expert.md (use rq_stats)
- .claude/agents/debug.md (use g_debug)

**Migration Notes:**
- All v3 prompts archived (historical reference)
- v4.X agents built from scratch (not edits of v3)
- Lessons learned from v3 failures inform v4.X design
- v3.0 documentation marked as historical in archives

---

# END OF SPECIFICATION

**Version History:**
- v4.0: Complete atomic agent redesign (2025-11-15)
  - Ultrathink validation: 40 issues identified and resolved
  - Post-ultrathink inspection: 10 additional issues identified and resolved (2025-11-16)
  - Status: VALIDATED (ready for implementation)

**Post-Ultrathink Fixes (2025-11-16):**
1. ✅ Added re-run step after g_debug fix (section 3.1 step 14)
2. ✅ TDD approach for names.md initialization (sections 4.5.1, 5.3)
3. ✅ Added automation.md specification (section 4.5.4)
4. ✅ Clarified rq_builder directory verification (section 2.1.1)
5. ✅ Added validation tools architecture (sections 2.3.1, 2.3.2, 2.3.3, 4.2.2, 4.2.3, 4.2.4)
6. ✅ Clarified g_code invocation format (section 2.4.1)
7. ✅ Clarified rq_inspect analysis steps check (section 2.4.2)
8. ✅ Added YAML parsing guidance (section 3.3)
9. ✅ Fixed variable definition for ch7 (section 1.2)
10. ✅ Clarified rq_plots source code reading rationale (section 2.5.1)

**Implementation Checklist:**
1. ✅ Specification complete and validated
2. ✅ Create docs/v4/ folder structure (completed 2025-11-16)
3. 🔄 Build template files (11 templates in docs/v4/templates/) - IN PROGRESS: agent_best_practices.md complete
4. 🔄 Build agent prompts (13 agents in .claude/agents/)
5. 🔄 Move thesis files (ANALYSES_CHX.md to docs/v4/thesis/)
6. 🔄 Archive v3 agents (_legacy/v3/agents/)
7. 🔄 Test v4.X workflow on RQ 5.1 (manual Phase 1)
8. 🔄 Iterate on agents based on testing
9. 🔄 Build orchestrator (Phase 2 automation)
10. 🔄 Complete all 50 RQs with v4.X

---

**END OF DOCUMENT**
