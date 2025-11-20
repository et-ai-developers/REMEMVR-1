# Status.yaml Structure Specification

**Last Updated:** 2025-11-16
**Version:** 4.0
**Purpose:** Defines the mandatory status.yaml structure for v4.X research questions
**Audience:** rq_builder agent when creating status.yaml file

---

## How to Use This Template

This template specifies the **exact YAML structure** that rq_builder agent must create for the `status.yaml` file. The status.yaml file tracks agent execution statuses and maintains context dumps for pseudo-stateful operation across all RQ-specific agents.

**Agent Implementation (rq_builder agent):**
- Reads this template in Step 3
- Creates `status.yaml` in Step 6 according to these specifications
- Reports success after status.yaml created

**Pseudo-Statefulness:**
- Each RQ-specific agent reads `status.yaml` in Step 2 of its workflow
- Agents check prior agents' statuses and read their context_dumps
- Agents update their own status + write context_dump in final step
- This enables continuity without persistent agent state

---

## File Location

**Path:** `results/chX/rqY/status.yaml` (root level of RQ directory)

**Created By:** rq_builder agent (workflow step 3, agent step 6)

**Updated By:** All 10 RQ-specific agents (each updates their section after execution)

**Read By:** All 10 RQ-specific agents (each reads prior context in Step 2)

---

## YAML Structure Overview

**Top-level sections:**
1. **Agent Statuses** - 10 RQ-specific agents (each with status + context_dump)
2. **analysis_steps** - Per-step execution tracking (added by rq_analysis agent, NOT by rq_builder)

**Status Values:** `pending` or `success` (only two valid values)

**Context Dump Format:** Multiline string (max 5 lines per agent_best_practices.md)

---

## Agent Sections (10 RQ-Specific Agents)

The following 10 agents MUST have sections in status.yaml:

### 1. rq_builder
**Created In:** Workflow Step 3
**Purpose:** Creates RQ folder structure and status.yaml
**Fields:**
- `status`: pending | success
- `context_dump`: Multiline string (max 5 lines)

### 2. rq_concept
**Created In:** Workflow Step 4
**Purpose:** Extracts RQ concept from thesis, creates 1_concept.md
**Fields:**
- `status`: pending | success
- `context_dump`: Multiline string (max 5 lines)

### 3. rq_scholar
**Created In:** Workflow Step 5
**Purpose:** Validates 1_concept.md scholarly accuracy
**Fields:**
- `status`: pending | success
- `context_dump`: Multiline string (max 5 lines)

### 4. rq_stats
**Created In:** Workflow Step 6
**Purpose:** Validates 1_concept.md statistical methods
**Fields:**
- `status`: pending | success
- `context_dump`: Multiline string (max 5 lines)

### 5. rq_planner
**Created In:** Workflow Step 9
**Purpose:** Creates 2_plan.md with analysis plan
**Fields:**
- `status`: pending | success
- `context_dump`: Multiline string (max 5 lines)

### 6. rq_tools
**Created In:** Workflow Step 11
**Purpose:** Creates 3_tools.yaml with tool specifications
**Fields:**
- `status`: pending | success
- `context_dump`: Multiline string (max 5 lines)

### 7. rq_analysis
**Created In:** Workflow Step 12
**Purpose:** Creates 4_analysis.yaml with analysis recipe
**Fields:**
- `status`: pending | success
- `context_dump`: Multiline string (max 5 lines)

**CRITICAL NOTE:** rq_analysis agent ALSO creates the `analysis_steps` section (see below). This is the ONLY agent that creates analysis_steps. rq_builder does NOT create analysis_steps initially.

### 8. rq_inspect
**Created In:** Workflow Step 14 (CODE EXECUTION LOOP)
**Purpose:** Validates analysis outputs after each step
**Fields:**
- `status`: pending | success
- `context_dump`: Multiline string (max 5 lines)

### 9. rq_plots
**Created In:** Workflow Step 15
**Purpose:** Creates plots.py script
**Fields:**
- `status`: pending | success
- `context_dump`: Multiline string (max 5 lines)

### 10. rq_results
**Created In:** Workflow Step 17
**Purpose:** Creates summary.md final results
**Fields:**
- `status`: pending | success
- `context_dump`: Multiline string (max 5 lines)

---

## General-Purpose Agents (EXCLUDED from status.yaml)

The following 3 agents are **intentionally EXCLUDED** from status.yaml:

### g_code (NOT in status.yaml)
**Why Excluded:** General-purpose code generation agent that does NOT read status.yaml per specification section 2.4.1, line 566. Master provides ALL information directly when invoking g_code (docs paths, output path, log path). No pseudo-statefulness needed.

### g_conflict (NOT in status.yaml)
**Why Excluded:** General-purpose conflict detection agent that does NOT use status.yaml per specification section 2.6.1, line 719. Intentional design - g_conflict can be used for ANY document comparison, not RQ-specific. Master provides documents to compare directly.

### g_debug (NOT in status.yaml)
**Why Excluded:** General-purpose debugging agent used for error recovery. Does NOT read status.yaml. Master provides error logs and code to debug directly.

**TOTAL v4.X AGENTS:** 13 total (10 RQ-specific in status.yaml + 3 general-purpose excluded)

**NOTE FOR rq_builder:** Create status.yaml with ONLY the 10 RQ-specific agents listed above. Do NOT create sections for g_code, g_conflict, or g_debug.

---

## Initial Values (Created by rq_builder)

**When rq_builder creates status.yaml:**

**All agent statuses:** `pending` (no agents have run yet)

**All context_dumps:** Empty multiline strings (no context yet)

**analysis_steps section:** NOT created by rq_builder (rq_analysis creates this later)

**Example initial state:**
```yaml
rq_builder:
  status: pending
  context_dump: |

rq_concept:
  status: pending
  context_dump: |

# ... all 10 agents start pending with empty context_dumps
```

**After rq_builder runs:** rq_builder updates its own section to `status: success` and writes its context_dump (5 lines max).

---

## Agent Update Pattern

**Every RQ-specific agent follows this pattern:**

**Step 2 (Read Status):**
- Read `status.yaml`
- Check prior agents' statuses (all should be `success`)
- Read prior agents' context_dumps (gather context)
- Check own status (should be `pending`, this agent is next)

**Final Step (Update Status):**
- Edit `status.yaml`
- Update own status to `success`
- Write own context_dump (max 5 lines per agent_best_practices.md)

**Example - rq_concept updates:**
```yaml
rq_concept:
  status: success
  context_dump: |
    RQ 5.1: Domain-specific forgetting trajectories
    Domains: What/Where/When
    Analysis: IRT (theta extraction) + LMM (trajectory modeling)
    Data source: REMEMVR test T1-T4 (composite_ID stacking)
    Critical: Temporal items may have extreme difficulty (purify via 2-pass)
```

---

## Context Dump Format (Max 5 Lines)

**Per agent_best_practices.md section "Context Dump Format":**

**Max 5 lines** - Terse summaries only (prevent file bloat)

**Content Guidelines:**
1. **Line 1:** RQ ID and title
2. **Line 2:** Memory domains (What/Where/When) or key variables
3. **Line 3:** Analysis type (IRT/LMM/CTT) or key methods
4. **Line 4:** Data source or critical parameters
5. **Line 5:** Critical info for downstream agents (warnings, dependencies, etc.)

**Format:** Multiline string using YAML pipe (`|`) notation

**Example:**
```yaml
agent_name:
  status: success
  context_dump: |
    RQ 5.1: Domain-specific forgetting trajectories
    Domains: What/Where/When
    Analysis: IRT + LMM
    Data: REMEMVR T1-T4 composite_ID stacking
    Critical: 2-pass IRT purification (temporal items extreme difficulty)
```

**IMPORTANT:** Context dumps are SUMMARIES not complete documentation. Agents read 1_concept.md, 2_plan.md, etc. for full details. Context dumps provide just enough info for downstream agents to understand RQ context without re-reading all prior documents.

---

## analysis_steps Section (Added Later)

**NOT created by rq_builder.** This section is created by **rq_analysis agent** in workflow step 12.

**Purpose:** Tracks per-step execution status during CODE EXECUTION LOOP (workflow step 14)

**Structure:**
```yaml
analysis_steps:
  step01:
    status: pending | success
    context_dump: |
      Brief validation summary (max 5 lines)
  step02:
    status: pending | success
    context_dump: |
      Brief validation summary (max 5 lines)
  # ... additional steps as defined in 4_analysis.yaml
```

**Created By:** rq_analysis agent when it writes `4_analysis.yaml` (workflow step 12)

**Updated By:** rq_inspect agent during CODE EXECUTION LOOP (workflow step 14) - marks each step `success` after validation passes

**Usage:** Master checks analysis_steps section to determine which step to execute next during CODE EXECUTION LOOP. If step01-stepN are `success` and step(N+1) is `pending`, execute step(N+1).

**NOTE FOR rq_builder:** Do NOT create the analysis_steps section in initial status.yaml. Leave it empty. rq_analysis will add it later.

---

## Complete YAML Structure Example

**Initial status.yaml (created by rq_builder):**

```yaml
rq_builder:
  status: pending
  context_dump: |

rq_concept:
  status: pending
  context_dump: |

rq_scholar:
  status: pending
  context_dump: |

rq_stats:
  status: pending
  context_dump: |

rq_planner:
  status: pending
  context_dump: |

rq_tools:
  status: pending
  context_dump: |

rq_analysis:
  status: pending
  context_dump: |

rq_inspect:
  status: pending
  context_dump: |

rq_plots:
  status: pending
  context_dump: |

rq_results:
  status: pending
  context_dump: |
```

**After rq_builder completes (status.yaml updated):**

```yaml
rq_builder:
  status: success
  context_dump: |
    Created results/ch5/rq1/ with 6 folders
    Folders: docs/, data/, code/, logs/, plots/, results/
    All folders empty, ready for agents
    status.yaml initialized with 10 RQ-specific agents
    Next: rq_concept extracts concept from thesis

rq_concept:
  status: pending
  context_dump: |

rq_scholar:
  status: pending
  context_dump: |

# ... rest remain pending
```

**After rq_analysis completes (analysis_steps section added):**

```yaml
rq_builder:
  status: success
  context_dump: |
    Created results/ch5/rq1/ with 6 folders
    # ...

# ... other agents ...

rq_analysis:
  status: success
  context_dump: |
    Created 4_analysis.yaml with 3 steps
    Step 1: IRT calibration (GRM, 2-pass purification)
    Step 2: Theta extraction + TSVR merge
    Step 3: LMM trajectory modeling (random slopes)
    Each step has analysis + validation tool calls
    Ready for CODE EXECUTION LOOP

rq_inspect:
  status: pending
  context_dump: |

# ... rest pending ...

analysis_steps:
  step01:
    status: pending
    context_dump: |
  step02:
    status: pending
    context_dump: |
  step03:
    status: pending
    context_dump: |
```

**During CODE EXECUTION LOOP (rq_inspect updates after each step):**

```yaml
# ... agents sections ...

analysis_steps:
  step01:
    status: success
    context_dump: |
      IRT calibration completed
      43/102 items retained (2-pass purification)
      Validation passed: all parameters |b| ≤ 3.0, a ≥ 0.4
      Outputs: step01_calibrate_irt.csv (item parameters)
      Ready for step 2 (theta extraction)
  step02:
    status: pending
    context_dump: |
  step03:
    status: pending
    context_dump: |
```

---

## Validation Architecture Integration

**status.yaml enables v4.X validation gates:**

1. **Sequential Execution Enforcement:** Agents check prior agents' statuses before running (circuit breaker if prior = pending)
2. **Context Continuity:** Context dumps prevent information loss between agents
3. **Step-by-Step Validation:** analysis_steps section enables CODE EXECUTION LOOP progress tracking
4. **Error Recovery:** If step fails, status stays `pending`, g_debug can diagnose, master applies fix, re-runs step
5. **Audit Trail:** Complete execution history preserved (who ran when with what results)

---

## Implementation Notes for rq_builder Agent

**What rq_builder Does (Step 6):**

1. Read this template `docs/v4/templates/build_status.md` (Step 3)
2. Create `results/chX/rqY/status.yaml` (Step 6)
3. Write YAML structure with 10 RQ-specific agents (all `status: pending`, all `context_dump` empty)
4. Do NOT create analysis_steps section (rq_analysis creates this later)
5. Update own section (rq_builder) to `status: success` with context_dump
6. Report success to master

**YAML Creation Method:**
- Template specifies WHAT to create (structure, agents, fields)
- rq_builder determines HOW to create (Write tool with YAML content)
- YAML must be valid (proper indentation, pipe notation for multiline strings)

**Verification:**
- Read back status.yaml
- Confirm 10 agent sections present (rq_builder through rq_results)
- Confirm NO g_code, g_conflict, or g_debug sections
- Confirm NO analysis_steps section initially
- Confirm all statuses = `pending`, all context_dumps empty (except rq_builder = success)

---

## Pseudo-Statefulness Design

**v4.X architectural innovation:**

**v3.0:** Only rq-specification agent was stateful (via logs/rq_spec_context.md)

**v4.X:** ALL 10 RQ-specific agents are pseudo-stateful (via status.yaml context_dumps)

**Benefits:**
1. **Continuity:** Agents remember prior work without persistent state
2. **Lean context:** Max 5 lines per dump prevents file bloat
3. **Coordination:** Agents know what prior agents decided/discovered
4. **Auditability:** Complete execution history in single file
5. **Error recovery:** Context preserved across g_debug iterations

**How it works:**
- Agent reads status.yaml → sees prior agents' context_dumps
- Agent processes RQ with full historical context
- Agent updates status.yaml → writes own context_dump for next agent
- File size stays manageable (10 agents × 5 lines = 50 lines max + analysis_steps)

---

## Common Patterns

### Pattern 1: Check Prior Agents
```yaml
# Every agent Step 2: Read status.yaml, verify prior agents = success

rq_planner reads:
- rq_builder: success? ✓
- rq_concept: success? ✓
- rq_scholar: success? ✓
- rq_stats: success? ✓
- rq_planner: pending? ✓ (this agent is next)

If ANY prior agent = pending → CIRCUIT BREAKER (quit, report error)
```

### Pattern 2: Read Prior Context
```yaml
# rq_planner reads context_dumps to understand RQ

rq_concept context_dump:
  "RQ 5.1: Domain-specific forgetting trajectories
   Domains: What/Where/When
   Analysis: IRT + LMM
   Data: REMEMVR T1-T4
   Critical: 2-pass purification"

rq_scholar context_dump:
  "Literature validated: domain-specific forgetting established
   Key citations: Tulving 1972, Baddeley 2000
   No conflicts found
   Recommendations: cite temporal tagging theory"

rq_stats context_dump:
  "IRT + LMM appropriate for longitudinal theta scores
   GRM suitable for 4-point Likert (0-3 certainty)
   2-pass purification statistically sound
   LMM random slopes justified (individual differences)"

# rq_planner uses this context to build 2_plan.md
```

### Pattern 3: Update Own Section
```yaml
# Every agent final step: Edit status.yaml

# Before (status.yaml):
rq_planner:
  status: pending
  context_dump: |

# After rq_planner completes (status.yaml):
rq_planner:
  status: success
  context_dump: |
    Created 2_plan.md with 3-step analysis workflow
    Step 1: IRT calibration (2-pass GRM)
    Step 2: Theta extraction + TSVR merge
    Step 3: LMM trajectory (random slopes)
    Validation tools specified (MUST be used per step)
```

---

## Version History

**Version 4.0 (2025-11-16):**
- Initial v4.X template specification
- YAML format (status.yaml replaces v3.0 status.md JSON)
- 10 RQ-specific agents tracked (g_code, g_conflict, g_debug excluded)
- Universal pseudo-statefulness via context_dumps (max 5 lines)
- analysis_steps section for CODE EXECUTION LOOP tracking
- Simplified status values (pending/success only)

**v3.0 → v4.0 Migration Notes:**
- v3.0: status.md (JSON format) at root, 7 monolithic agents
- v3.0: Only rq-specification had context dumps (logs/rq_spec_context.md)
- v3.0: Status values: complete/in_progress/not_started, success/failure, passed/failed
- v4.0: status.yaml (YAML format) at root, 10 atomic agents
- v4.0: ALL RQ-specific agents have context_dumps (embedded in status.yaml)
- v4.0: Status values simplified to pending/success (binary)
- v4.0: analysis_steps section NEW (enables step-by-step execution tracking)

---

**End of Template Specification**
