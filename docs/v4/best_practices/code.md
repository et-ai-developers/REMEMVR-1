# Agent Best Practices - Code

**Version:** 4.0
**Last Updated:** 2025-11-21
**Purpose:** Code-specific best practices for agents that generate/validate/debug Python code
**Audience:** 5/13 code-aware agents (rq_planner, rq_tools, rq_analysis, g_code, g_debug)

**NOT for:** rq_builder, rq_concept, rq_scholar, rq_stats, g_conflict, rq_inspect, rq_plots, rq_results (don't work with code generation/validation)

---

## CRITICAL: When to Read This File

**Code-Aware Agents:** Read this file AFTER universal.md (and workflow.md if RQ-specific)
- rq_planner: Specifies tool requirements (needs Poetry knowledge)
- rq_tools: Verifies tool signatures (needs Poetry + MCP)
- rq_analysis: Specifies function signatures (needs Poetry + MCP)
- g_code: Generates code (needs Poetry + MCP + data boundaries)
- g_debug: Debugs code (needs Poetry + MCP + data boundaries)

**Non-Code Agents:** DO NOT read this file
- No code generation/validation responsibilities
- Saves context budget

---

## 1. POETRY ENVIRONMENT

**CRITICAL:** ALL Python execution uses Poetry

### 1.1 Script Execution

**Format:**
```bash
poetry run python path/to/script.py
```

**NEVER:**
```bash
python script.py              # WRONG - doesn't use Poetry environment
pip install package           # WRONG - use Poetry for dependency management
```

---

### 1.2 Dependency Management

**Check Installed Packages:**
```bash
poetry show
```

**Add Package:**
```bash
poetry add package-name
```

**Add Dev Package:**
```bash
poetry add --group dev package-name
```

**Why Poetry:**
- Reproducibility (poetry.lock ensures exact versions)
- Dependency resolution (automatic conflict handling)
- Professional standard for PhD thesis reference

---

## 2. DATA SOURCE BOUNDARIES

**CRITICAL:** NEVER generate mock data

### 2.1 RAW Data (Allowed Sources)

**Definition:**
- Extractable from master.xlsx participant data
- OR outputs from other completed RQs
- Created OUTSIDE analysis pipeline

**Examples:**
- VR item responses (from master.xlsx)
- Demographic data (from master.xlsx)
- Cognitive test scores (from master.xlsx)
- Theta scores from prior RQ (from results/chX/rqY/data/)

---

### 2.2 DERIVED Data (Analysis Pipeline Outputs)

**Definition:**
- Requires statistical analysis
- Created BY analysis step scripts
- Created INSIDE analysis pipeline

**Examples:**
- IRT theta scores (created by calibrate_grm)
- Item parameters (created by IRT calibration)
- LMM coefficients (created by fit_lmm_with_tsvr)
- Purified item lists (created by purify_items)

---

### 2.3 Circuit Breaker for Unclear Sources

**If Data Source Unclear:**
- Trigger CLARITY ERROR
- Report: "Data source unclear - is this RAW (from master.xlsx or other RQ) or DERIVED (from analysis)?"
- QUIT immediately

**Why:**
- Prevents catastrophic mock data generation
- Ensures data provenance is always clear
- Documents dependencies explicitly

---

## 3. MCP TOOL USAGE

**Available MCP Tools:**
- `mcp__context7__resolve-library-id` - Find library documentation
- `mcp__context7__get-library-docs` - Fetch library documentation

**Used By:**
- rq_tools (when checking tool documentation)
- rq_analysis (when verifying signatures)
- g_code (when validating imports)
- g_debug (when investigating errors)

**Purpose:**
- Fetch up-to-date library documentation
- Verify tool signatures
- Check API compatibility

**Usage Pattern:**
1. Resolve library name to Context7 ID
2. Fetch documentation for specific topic
3. Verify function signatures match specifications
4. Use documentation to validate code generation

---

## END OF CODE BEST PRACTICES

**Remember:**
1. Read universal.md FIRST (all agents)
2. Read workflow.md if RQ-specific (rq_planner, rq_tools, rq_analysis)
3. Then read this file (code.md)
4. ALWAYS use Poetry for script execution
5. NEVER generate mock data (trigger CLARITY ERROR if data source unclear)
6. Use MCP tools to verify library APIs before generating code

**Version History:**
- v4.0.1: Extracted from agent_best_practices.md for targeted loading (2025-11-21)
