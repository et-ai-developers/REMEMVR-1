# REMEMVR Agents System - Overview

**Last Updated:** 2025-11-11
**Purpose:** User-facing documentation of the agent-based automation pipeline

---

## Overview

The agents system coordinates modular analysis execution for research questions (RQs). Each agent is a specialized, stateless subprocess that performs a specific role in the analysis pipeline.

---

## Agent Architecture

**Location:** All agent prompts stored in `.claude/agents/` (per Anthropic specification)

**Invocation:** Via Claude Code Task tool with `subagent_type` parameter

**Communication:** File-based (agents read/write files, master coordinates)

---

## 7 RQ Pipeline Agents

### 1. rq_specification Agent
**Role:** Create RQ specification drafts OR finalize with validation feedback
**Status:** ✅ Production-ready (v2.0)
**Prompt:** `.claude/agents/rq_specification.md`

**Modes:**
- **Draft Phase:** Creates info.md, config.yaml, validation instructions
- **Finalization Phase:** Incorporates validation feedback, updates Status section

**Key Responsibilities:**
- Generate 11-section RQ specification (info.md)
- Create technical configuration (config.yaml)
- Write validation instructions for Scholar and Statistics Expert agents
- Incorporate feedback and finalize specifications

---

### 2. Scholar Agent
**Role:** Validate theoretical grounding using episodic memory literature
**Status:** ✅ Production-ready (v2.0)
**Prompt:** `.claude/agents/scholar.md`

**Key Responsibilities:**
- Validate hypothesis aligns with episodic memory theory
- Check theoretical citations (recent 2023-2024 literature via WebSearch)
- Assess interpretation guidelines and reviewer rebuttals
- Score theoretical grounding (0-10 scale)
- Suggest additional citations if needed

**Tools:** WebSearch MCP (for 2023-2024 literature)

---

### 3. Statistics Expert Agent
**Role:** Validate statistical methodology and enforce tool reuse
**Status:** ✅ Production-ready (v2.0)
**Prompt:** `.claude/agents/statistics_expert.md`

**Key Responsibilities:**
- Validate statistical approach (IRT/LMM/CTT appropriate for RQ?)
- Assess tool requirements (must use existing tools from `docs/tools_inventory.md`)
- Check complexity (unnecessary vs justified complexity)
- Score statistical rigor (0-10 scale)
- Update tool inventory with RQ usage

**Tools:** Context7 MCP (for package documentation)

**Documentation:** See `docs/tools_inventory.md` for complete tool reference

---

### 4. Data-Prep Agent
**Role:** Prepare input data for RQ analysis
**Status:** ✅ Production-ready (v3.0) - Critical bug fix applied
**Prompt:** `.claude/agents/data_prep.md`

**Key Responsibilities:**
- Extract tags directly from master.xlsx using data.py functions
- Compute derived scores (e.g., RAVLT_Total = sum of T1-T5)
- Load previous RQ outputs for dependent analyses
- Extract VR data with wildcard patterns
- Validate extracted data (dimensions, missingness, outliers)
- Generate comprehensive JSON report

**Output:** `results/chX/rqY/data/input.csv`

**Documentation:** See `docs/data_prep_agent_guide.md` for complete usage guide

**Critical Feature (v3.0):** 150-line tag system embedded in prompt to prevent data corruption

---

### 5. Analysis-Executor Agent
**Role:** Run analysis steps sequentially
**Status:** ⚠️ Stub only (needs development)
**Prompt:** `.claude/agents/analysis_executor.md`

**Key Responsibilities:**
- Execute IRT/LMM/CTT analyses step-by-step
- Validate outputs between steps
- Log all terminal output (Windows-compatible)
- Generate intermediate results (`output_1.csv`, `output_2.csv`, etc.)
- Save final results (`output.csv`)

**Documentation:** See `docs/tools_inventory.md` for available statistical tools

---

### 6. Results-Inspector Agent
**Role:** Validate statistical correctness and format results
**Status:** ⚠️ Stub only (needs development)
**Prompt:** `.claude/agents/results_inspector.md`

**Key Responsibilities:**
- Check statistical assumptions (normality, homoscedasticity)
- Validate model diagnostics
- Format results beautifully (publication-ready tables)
- Write scholarly summary (update info.md Results section)
- Act as "devil's advocate" for quality control

**Tools:** Context7 MCP, WebSearch

---

### 7. Debug Agent
**Role:** Fix bugs identified by other agents
**Status:** ⚠️ Stub only (needs development)
**Prompt:** `.claude/agents/debug.md`

**Key Responsibilities:**
- Diagnose errors from calling agent
- Research solutions (Context7, WebSearch)
- Implement fixes (Edit tool)
- Test fixes
- Report back to master with explanation

**Tools:** Context7 MCP, WebSearch, Read, Edit

---

## Supporting Agents (Memory Management)

### context-manager Agent
**Role:** Curate state.md to ≤20k tokens, archive old content
**Status:** ✅ Production-ready
**Prompt:** `.claude/agents/context_manager.md`

**Philosophy:** NEVER condenses, NEVER deletes - Only archives with zero information loss

---

### context-finder Agent
**Role:** Search archives/ + docs/ for historical context
**Status:** ✅ Production-ready
**Prompt:** `.claude/agents/context_finder.md`

**Key Feature:** Chronological awareness - Reports WHEN information was generated

---

## Agent Communication Protocol

### Core Principles
1. **Stateless Execution** - No persistent state between invocations
2. **JSON Reports** - Structured, parseable output format
3. **Master Coordination** - Master agent coordinates everything (no sub-agent nesting)
4. **No Guessing** - Ask master for clarification if unclear
5. **Immediate Error Reporting** - Report errors immediately, no retries without approval

### Report Format (JSON)

```json
{
  "agent": "agent_name",
  "status": "success|warning|failure",
  "timestamp": "2025-11-11T10:00:00Z",
  "files_created": ["path/to/file.csv"],
  "summary": "Brief description of what was done",
  "validation": {
    "checks_passed": 10,
    "checks_failed": 0,
    "issues": []
  },
  "next_steps": "Recommended next action",
  "error": null
}
```

---

## Invoking Agents

**Method:** Using Claude Code Task tool

```python
# Example: Invoke data-prep agent
Task(
    subagent_type="data_prep",
    description="Prepare data for RQ 5.1",
    prompt="Read RQ specification from results/ch5/rq1/info.md and extract required data"
)
```

**All agents automatically load:**
- Their prompt from `.claude/agents/[agent_name].md`
- Required documentation files (specified in prompt)
- RQ-specific files (info.md, config.yaml, etc.)

---

## 6-Step RQ Automation Pipeline

```
Step 1: rq_specification (draft)
├─ Creates info.md draft
├─ Creates config.yaml draft
└─ Writes validation instructions

Step 2: scholar
├─ Validates theoretical grounding
└─ Writes scholar_report.json (score/feedback)

Step 3: statistics_expert
├─ Validates statistical methodology
└─ Writes statistics_report.json (score/feedback)

Step 4: rq_specification (finalization)
├─ Incorporates feedback
├─ Updates info.md Status section
└─ Writes rq_specification_report.json

Step 5: data_prep
├─ Extracts data from master.xlsx
└─ Writes data/input.csv

Step 6: analysis_executor
├─ Runs IRT/LMM/CTT analyses
└─ Writes data/output.csv

(Future: Step 7: results_inspector - validate + format results)
```

---

## Current Status (2025-11-11)

**Completed:**
- ✅ Steps 1-4 (Specification Phase): 100% complete for 50 RQs (9.37/10 average quality)
- ✅ Data-Prep Agent v3.0: Production-ready with critical bug fix
- ✅ Tool Suite: 49/49 tests passing, all 5 modules production-ready

**In Progress:**
- ⏳ Steps 5-6 (Execution Phase): Agents ready but not yet automated

**Upcoming:**
- ⏳ Analysis-Executor development (expand stub to full agent)
- ⏳ Results-Inspector development
- ⏳ Full automation testing on real RQs

---

## Documentation

**Agent Prompts:**
- Location: `.claude/agents/*.md`
- Purpose: Executable agent instructions

**User Documentation:**
- `docs/agents_overview.md` (this file) - High-level overview
- `docs/data_prep_agent_guide.md` - Complete data-prep usage guide
- `docs/tools_inventory.md` - Statistical tools reference

**Technical Documentation:**
- See `.claude/CLAUDE.md` for complete agent system architecture
- See `docs/rq_workflow.md` for detailed 6-step pipeline specification

---

## References

For complete agent architecture, communication protocols, and memory system integration:
- `.claude/CLAUDE.md` - Trait memory (operating principles)
- `.claude/context/current/state.md` - Current work state
- `docs/docs_index.md` - Complete documentation index

---

**End of Agents Overview**
