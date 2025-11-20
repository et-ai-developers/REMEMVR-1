# Agent Best Practices - Workflow

**Version:** 4.0
**Last Updated:** 2025-11-21
**Purpose:** Workflow-specific best practices for RQ-specific agents using status.yaml
**Audience:** 10/13 workflow agents (rq_builder, rq_concept, rq_scholar, rq_stats, rq_planner, rq_tools, rq_analysis, rq_inspect, rq_plots, rq_results)

**NOT for:** g_conflict, g_code, g_debug (general-purpose agents that don't use status.yaml)

---

## CRITICAL: When to Read This File

**RQ-Specific Agents:** Read this file AFTER universal.md
- You use status.yaml for continuity
- You write context_dumps
- You follow file path conventions

**General-Purpose Agents:** DO NOT read this file
- g_conflict: Minimal circuit breakers only
- g_code: General-purpose, master provides all context
- g_debug: Debugging-specific workflow

---

## 1. YAML PARSING & STATUS CHECKING

### 1.1 Reading status.yaml

**Method:**
1. Use Read tool to read status.yaml file
2. Parse YAML structure using general LLM reasoning
3. NO programmatic YAML parser needed

**Pattern Matching:**
```yaml
rq_concept:
  status: success
  context_dump: |
    RQ 5.1: Trajectory of Forgetting - What Domain
    Memory domains: What (object identity)
```

**How to Check:**
- Look for lines like `"rq_concept:\n  status: success"`
- Extract status value via pattern matching
- Read context_dump multiline string

**If Parsing Unclear:**
- Trigger CLARITY ERROR
- Report to master with specific parsing issue

---

### 1.2 Pseudo-Statefulness

**Reading Prior Context:**
1. Read status.yaml at agent invocation start
2. Check all prior agents' statuses
3. Read all prior agents' context_dumps
4. Use context_dumps for continuity

**Benefits:**
- Stateful behavior without context window bloat
- Each agent stays <5k tokens
- Maintains workflow continuity

**Example Usage:**
```
Agent rq_planner reads status.yaml:
- Sees rq_concept.status = success
- Reads rq_concept.context_dump: "Memory domains: What (object identity)"
- Uses this info to plan analysis steps
```

---

## 2. CONTEXT DUMP FORMAT

**Location:** status.yaml under agent name

**Structure:**
```yaml
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
- **Max 5 lines per agent** (strict limit)
- Terse summaries ONLY
- NO verbose explanations
- Prevent file bloat

**What to Include:**
- Memory domains (What/Where/When)
- Analysis type (IRT/LMM/CTT)
- Key decisions made
- Critical information for downstream agents

**What NOT to Include:**
- Detailed methodology
- Complete file contents
- Verbose explanations
- Redundant information

**Example - Good Context Dump:**
```yaml
rq_planner:
  status: success
  context_dump: |
    5 analysis steps planned
    IRT calibration -> purification -> LMM trajectory
    Validation tools specified for each step
```

**Example - Bad Context Dump (Too Verbose):**
```yaml
rq_planner:
  status: success
  context_dump: |
    Created detailed analysis plan for RQ 5.1 examining trajectory of forgetting
    Step 1 performs IRT calibration using GRM on what-domain items
    Step 2 purifies items using thresholds a >= 0.4 and |b| <= 3.0
    Step 3 runs Pass 2 IRT on purified items
    Step 4 extracts theta scores and merges with TSVR
    Step 5 fits LMM with random intercepts and slopes
    Validation tools will check outputs at each step
```
(7 lines, too verbose - VIOLATES 5-line limit)

---

## 3. FILE PATH CONVENTIONS

**Relative Paths:**
- Use paths relative to `results/chX/rqY/` in specifications

**Standard RQ Structure:**
```
results/chX/rqY/
  status.yaml                (agent statuses, context dumps)
  docs/                      (specifications)
    1_concept.md
    2_plan.md
    3_tools.yaml
    4_analysis.yaml
  data/                      (analysis outputs)
    stepN_name.csv
  code/                      (generated scripts)
    stepN_name.py
  logs/                      (execution logs)
    stepN_name.log
  plots/                     (visualizations)
    plots.py
    plot_name.png
  results/                   (final summaries)
    summary.md
```

**Absolute Paths:**
- Use when referencing files outside RQ folder
- Examples: `docs/v4/templates/`, `docs/data_structure.md`

---

## 4. VALIDATION GATES

### 4.1 When to Validate

**Before Any Step:**
- Read status.yaml
- Check prior steps = success
- Verify expected files exist
- Confirm required information present

**If Validation Fails:**
- Use appropriate circuit breaker
- Specify what failed
- QUIT immediately

---

### 4.2 How to Validate

**Status Check:**
```
1. Read status.yaml
2. Parse agent statuses
3. Verify all prior agents = success
4. Verify current agent onwards = pending
5. If ANY prior agent != success -> STEP ERROR
```

**File Check:**
```
1. List expected input files
2. Check each file exists
3. If ANY file missing -> EXPECTATIONS ERROR
```

**Information Check:**
```
1. Read required documents
2. Extract required information
3. If ANY information missing -> CLARITY ERROR
4. If ANY information ambiguous -> CLARITY ERROR
```

---

## END OF WORKFLOW BEST PRACTICES

**Remember:**
1. Read universal.md FIRST, then this file
2. ONLY RQ-specific agents read this (10/13 agents)
3. Use status.yaml for continuity (pseudo-statefulness)
4. Write terse context dumps (max 5 lines)
5. Follow file path conventions (relative to results/chX/rqY/)
6. Validate prior steps before proceeding

**Version History:**
- v4.0.1: Extracted from agent_best_practices.md for targeted loading (2025-11-21)
