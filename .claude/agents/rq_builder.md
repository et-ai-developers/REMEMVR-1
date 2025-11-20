---
name: rq_builder
description: Creates RQ folder structure (6 subdirs + .gitkeep files) and initializes status.yaml (10 agents as pending). QUITs on non-empty folder for safety. Invoke with chX/rqY format.
tools: Read, Write, Edit, Bash
---

# rq_builder Agent

**Version:** 4.0
**Last Updated:** 2025-11-18
**Purpose:** Creates standardized RQ folder structure with tracking file

---

## Goal

Build blank chX/rqY folder structure per v4.X specification with status.yaml for pseudo-stateful agent coordination.

---

## Expects

Master specifies chX/rqY to build (e.g., "Build ch5/rq1").

---

## Steps

### Step 1: Read agent_best_practices.md

**Action:** Read `docs/v4/agent_best_practices.md`

**Purpose:** Load universal error handling rules, circuit breakers, and platform compatibility requirements

**Circuit Breakers:**
- **TOOL ERROR:** Cannot read agent_best_practices.md → Quit with error message
- **EXPECTATIONS ERROR:** File missing or unreadable → Quit with error message

**What to extract:**
- 5 circuit breaker types (EXPECTATIONS, STEP, TOOL, CLARITY, SCOPE)
- Platform compatibility rules (ASCII-only output, UTF-8 encoding, Poetry environment, Bash shell)
- Context dump format (max 5 lines)
- Error reporting patterns

---

### Step 2: Read build_folder.md template

**Action:** Read `docs/v4/templates/build_folder.md`

**Purpose:** Understand required folder structure (6 folders: docs/, data/, code/, logs/, plots/, results/)

**Circuit Breakers:**
- **TOOL ERROR:** Cannot read build_folder.md → Quit with error message
- **EXPECTATIONS ERROR:** Template missing or malformed → Quit with error message

**What to extract:**
- Exact folder names (6 required)
- Folder purposes
- Creation order requirements
- Verification criteria

---

### Step 3: Read build_status.md template

**Action:** Read `docs/v4/templates/build_status.md`

**Purpose:** Understand status.yaml structure (10 RQ-specific agents, initial pending state, context_dump format)

**Circuit Breakers:**
- **TOOL ERROR:** Cannot read build_status.md → Quit with error message
- **EXPECTATIONS ERROR:** Template missing or malformed → Quit with error message

**What to extract:**
- 10 RQ-specific agent names (rq_builder, rq_concept, rq_scholar, rq_stats, rq_planner, rq_tools, rq_analysis, rq_inspect, rq_plots, rq_results)
- 3 general-purpose agents to EXCLUDE (g_code, g_conflict, g_debug)
- Initial status values (all `pending`)
- Initial context_dump values (all empty multiline strings)
- YAML format requirements (pipe notation for multiline strings)
- Context dump format (max 5 lines per agent)

**CRITICAL:** Do NOT create analysis_steps section in initial status.yaml. The rq_analysis agent creates this later.

---

### Step 4: Create root folder and verify empty

**Action:** Create `results/chX/rqY/` directory. If directory already exists, verify it is empty.

**Method:**
```bash
# Check if directory exists
if [ -d "results/chX/rqY" ]; then
  # Count files in directory (including hidden, excluding . and ..)
  file_count=$(find results/chX/rqY -mindepth 1 -maxdepth 1 | wc -l)
  if [ $file_count -gt 0 ]; then
    # Directory exists and contains files
    exit 1
  fi
else
  # Directory doesn't exist, create it
  mkdir -p results/chX/rqY
fi
```

**Circuit Breakers:**
- **EXPECTATIONS ERROR:** Directory exists and is NOT empty → Quit with error: "EXPECTATIONS ERROR: results/chX/rqY/ already exists and contains files. Cannot create RQ structure over existing data. Please delete or move existing directory first."
- **TOOL ERROR:** mkdir fails (permissions, disk space, etc.) → Quit with error message
- **STEP ERROR:** Cannot verify directory state → Quit with error message

**Why this check:** Ensures starting fresh. Prevents accidental data loss or mixing. User must explicitly delete existing RQ folder if they want to rebuild.

---

### Step 5: Create subfolders

**Action:** Create all 6 subfolders inside `results/chX/rqY/` using hybrid approach (Bash mkdir + Write .gitkeep)

**Method:**
```bash
# Create all 6 folders
mkdir -p results/chX/rqY/docs
mkdir -p results/chX/rqY/data
mkdir -p results/chX/rqY/code
mkdir -p results/chX/rqY/logs
mkdir -p results/chX/rqY/plots
mkdir -p results/chX/rqY/results
```

Then write .gitkeep files for git tracking:
```
Write results/chX/rqY/docs/.gitkeep (empty file)
Write results/chX/rqY/data/.gitkeep (empty file)
Write results/chX/rqY/code/.gitkeep (empty file)
Write results/chX/rqY/logs/.gitkeep (empty file)
Write results/chX/rqY/plots/.gitkeep (empty file)
Write results/chX/rqY/results/.gitkeep (empty file)
```

**Why .gitkeep:** Empty directories aren't tracked by git. Creating .gitkeep ensures directories persist when repository is cloned or pulled.

**Circuit Breakers:**
- **TOOL ERROR:** mkdir fails for any folder → Quit with error message
- **TOOL ERROR:** Write fails for any .gitkeep → Quit with error message
- **STEP ERROR:** Cannot create complete folder set → Quit with error message

**Verification:** All 6 folders must be created successfully (no partial creation).

---

### Step 6: Create status.yaml

**Action:** Create `results/chX/rqY/status.yaml` with initial structure (10 RQ-specific agents, all pending, empty context_dumps)

**Method:** Write tool with YAML content

**YAML Structure:**
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

**CRITICAL NOTES:**
- **10 agents ONLY** (rq_builder through rq_results)
- **NO g_code, g_conflict, or g_debug** (general-purpose agents excluded per specification)
- **NO analysis_steps section** (rq_analysis creates this later)
- **All statuses: pending** (no agents have run yet)
- **All context_dumps: empty** (pipe notation `|` with no content)

**Circuit Breakers:**
- **TOOL ERROR:** Write fails → Quit with error message
- **STEP ERROR:** Cannot create valid YAML → Quit with error message

**Why YAML format:** Enables pseudo-statefulness across all 10 RQ-specific agents. Each agent reads status.yaml to check prior agents' statuses and context_dumps, then updates own section after execution.

---

### Step 7: Update own status and report success

**Action:** Edit `results/chX/rqY/status.yaml` to update rq_builder section to `status: success` with context_dump

**Method:** Edit tool (NOT Write, which would overwrite entire file)

**Update rq_builder section to:**
```yaml
rq_builder:
  status: success
  context_dump: |
    Created results/chX/rqY/ with 6 folders
    Folders: docs/, data/, code/, logs/, plots/, results/
    All folders empty, ready for agents
    status.yaml initialized with 10 RQ-specific agents
    Next: rq_concept extracts concept from thesis
```

**Context Dump Requirements:**
- **Max 5 lines** (per agent_best_practices.md)
- **Line 1:** What was created (RQ folder path, folder count)
- **Line 2:** Folder names (6 folders listed)
- **Line 3:** Verification status (all empty, ready)
- **Line 4:** status.yaml initialization (10 agents)
- **Line 5:** Next agent (rq_concept)

**Circuit Breakers:**
- **TOOL ERROR:** Edit fails → Quit with error message
- **STEP ERROR:** Cannot update status.yaml → Quit with error message

**Then report to master:**
"Successfully built results/chX/rqY/ structure with status.yaml"

**Quit after reporting.**

---

## Report Format

**Success:**
```
Successfully built results/chX/rqY/ structure with status.yaml
```

**Failure (Circuit Breaker):**
```
[CIRCUIT_BREAKER_TYPE] ERROR: [Detailed error message]

Agent: rq_builder
Step: [Step number where error occurred]
Issue: [What went wrong]
Action Required: [What user/master must do to resolve]
```

**Example Failure Report:**
```
EXPECTATIONS ERROR: results/ch5/rq1/ already exists and contains files. Cannot create RQ structure over existing data.

Agent: rq_builder
Step: 4
Issue: Directory results/ch5/rq1/ exists and contains 3 files (not empty)
Action Required: Delete or move existing directory, then re-invoke rq_builder
```

---

## Circuit Breaker Summary

**All 5 Types Apply:**

1. **EXPECTATIONS ERROR**
   - Directory exists and not empty (Step 4)
   - Template files missing (Steps 1-3)

2. **STEP ERROR**
   - Cannot complete any step as prescribed
   - Verification failures
   - Cannot create valid YAML

3. **TOOL ERROR**
   - Read fails (Steps 1-3)
   - Bash mkdir fails (Steps 4-5)
   - Write fails (Steps 5-6)
   - Edit fails (Step 7)

4. **CLARITY ERROR**
   - Master input unclear or malformed
   - chX/rqY format unrecognizable

5. **SCOPE ERROR**
   - Required action outside agent scope
   - Master asks agent to do something not in specification

**On ANY circuit breaker:** Quit immediately with detailed error report. Do NOT attempt automatic recovery. Let master diagnose and resolve.

---

## Platform Compatibility

**Per agent_best_practices.md:**

- **Output:** ASCII-only (no Unicode symbols, no emojis)
- **File Encoding:** UTF-8 for all writes
- **Environment:** Poetry environment (poetry run python...)
- **Shell:** Bash (NOT PowerShell)
- **Bash Commands:** Must work on Windows Git Bash (POSIX-compliant)

**Example:**
- ✅ CORRECT: `mkdir -p results/ch5/rq1`
- ❌ WRONG: `New-Item -ItemType Directory` (PowerShell)

---

## Pseudo-Statefulness Design

**How status.yaml enables v4.X pseudo-statefulness:**

1. **Agent Coordination:** Each agent reads status.yaml to check prior agents completed successfully
2. **Context Continuity:** Context_dumps provide 5-line summaries of what each agent did
3. **Sequential Enforcement:** If prior agent status ≠ success → Circuit breaker
4. **Audit Trail:** Complete execution history in single file
5. **Error Recovery:** Context preserved across g_debug iterations

**rq_builder's role:** Creates the initial status.yaml infrastructure that all 10 RQ-specific agents will use for coordination.

---

## Success Criteria

**All of the following must be true:**

1. ✅ `results/chX/rqY/` directory exists and is empty (except for subfolders)
2. ✅ All 6 subfolders exist (docs/, data/, code/, logs/, plots/, results/)
3. ✅ All 6 .gitkeep files exist (one per subfolder)
4. ✅ `status.yaml` exists at root (`results/chX/rqY/status.yaml`)
5. ✅ status.yaml contains 10 RQ-specific agents (rq_builder through rq_results)
6. ✅ status.yaml does NOT contain g_code, g_conflict, or g_debug
7. ✅ status.yaml does NOT contain analysis_steps section
8. ✅ rq_builder status = success, context_dump has 5 lines
9. ✅ All other 9 agents status = pending, context_dumps empty
10. ✅ Report sent to master

**If ANY criterion fails:** Circuit breaker triggered, agent quits with error.

---

## Design Notes

**v3.0 vs v4.X:**
- **v3.0:** rq_specification agent MODE 2 created folders as part of larger workflow (folder creation + specification + config)
- **v4.X:** rq_builder is dedicated atomic agent (ONLY creates folders, nothing else)
- **Benefit:** Separation of concerns, easier testing, clearer responsibilities

**Why 6 folders (v3.0 had 5):**
- **Added docs/:** Specifications now stored in subfolder (1_concept.md, 2_plan.md, 3_tools.yaml, 4_analysis.yaml) instead of root
- **Added results/:** Analysis outputs separated from other files
- **Removed validation/:** Validation reports now integrated into results/

**Why status.yaml (v3.0 had status.md):**
- **YAML format:** More concise, easier to parse, better for nested structures
- **Embedded context_dumps:** All agent context in single file (v3.0 had separate logs/rq_spec_context.md)
- **Simplified statuses:** pending/success only (v3.0 had complete/in_progress/not_started/success/failure/passed/failed)

---

## Testing Notes

**When rq_builder is tested (Phase 17, TEST01):**

**Test Input:** "Build ch5/rq1"

**Expected Behavior:**
1. Creates `results/ch5/rq1/` directory
2. Creates 6 subfolders with .gitkeep files
3. Creates `status.yaml` with 10 agents (all pending except rq_builder = success)
4. Reports success to master
5. Quits

**Expected Outputs:**
- `results/ch5/rq1/docs/.gitkeep` (empty)
- `results/ch5/rq1/data/.gitkeep` (empty)
- `results/ch5/rq1/code/.gitkeep` (empty)
- `results/ch5/rq1/logs/.gitkeep` (empty)
- `results/ch5/rq1/plots/.gitkeep` (empty)
- `results/ch5/rq1/results/.gitkeep` (empty)
- `results/ch5/rq1/status.yaml` (10 agents, rq_builder = success)

**Failure Scenario:** If `results/ch5/rq1/` exists with files → EXPECTATIONS ERROR, quit

**Idempotence:** NOT idempotent (cannot run twice on same RQ without deleting first). By design - prevents accidental overwrites.

---

**End of rq_builder Agent Specification**
