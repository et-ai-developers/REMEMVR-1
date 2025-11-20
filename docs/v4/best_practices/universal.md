# Agent Best Practices - Universal

**Version:** 4.0
**Last Updated:** 2025-11-21
**Purpose:** Universal error handling and platform rules for ALL 13 v4.X agents
**Audience:** ALL 13 agents (rq_builder, rq_concept, rq_scholar, rq_stats, rq_planner, g_conflict, rq_tools, rq_analysis, g_code, g_debug, rq_inspect, rq_plots, rq_results)

---

## 1. CIRCUIT BREAKERS (5 Types)

**Philosophy:** Quit on uncertainty, never guess. ALWAYS use appropriate circuit breaker when encountering ANY issue.

**Format Note:** The templates below are guidance. Agents may adapt message format for clarity while preserving the circuit breaker TYPE (EXPECTATIONS ERROR, STEP ERROR, etc.).

### 1.1 EXPECTATIONS ERROR

**When to Use:**
- Missing expected input file
- Missing required parameter
- Missing prerequisite from prior step

**Format:**
```
EXPECTATIONS ERROR: To perform {task} I expect {expected}, but missing {missing}
```

**Examples:**
```
EXPECTATIONS ERROR: To perform step 3 I expect 1_concept.md, but file missing
EXPECTATIONS ERROR: To create 2_plan.md I expect status.yaml with rq_concept = success, but rq_concept = pending
EXPECTATIONS ERROR: To generate code I expect documentation path parameter, but master didn't provide
```

**Action:** QUIT immediately, report to master

---

### 1.2 STEP ERROR

**When to Use:**
- Cannot complete step as prescribed in agent workflow
- Step preconditions not met
- Step execution blocked by external factor

**Format:**
```
STEP ERROR: Trying to complete {step} but {problem}
```

**Examples:**
```
STEP ERROR: Trying to complete step 5 (create 2_plan.md) but cannot determine analysis approach from 1_concept.md
STEP ERROR: Trying to complete step 8 but prior analysis steps not all marked success in status.yaml
STEP ERROR: Trying to update status.yaml but file is read-only
```

**Action:** QUIT immediately, report to master

---

### 1.3 TOOL ERROR

**When to Use:**
- Tool module/function doesn't exist (import fails)
- Tool execution raises exception
- Tool returns unexpected format

**Format:**
```
TOOL ERROR: Tried to use {tool} but {problem}
```

**Examples:**
```
TOOL ERROR: Tried to use tools.analysis_irt.calibrate_grm but module not found
TOOL ERROR: Tried to import pandas but ImportError raised
TOOL ERROR: Tried to use tools.validation.validate_irt but function doesn't exist
```

**Action:** QUIT immediately, report to master

---

### 1.4 CLARITY ERROR

**When to Use:**
- Insufficient information to proceed
- Ambiguous instructions
- Unclear data source
- Missing critical details

**Format:**
```
CLARITY ERROR: Trying to complete {step} but need {missing_info}
```

**Examples:**
```
CLARITY ERROR: Trying to specify validation criteria but don't know which analysis type (IRT/LMM/CTT)
CLARITY ERROR: Trying to extract data but 1_concept.md doesn't specify data source (master.xlsx or other RQ)
CLARITY ERROR: Trying to parse status.yaml but structure unclear (no agent_name fields found)
```

**Action:** QUIT immediately, report to master

---

### 1.5 SCOPE ERROR

**When to Use:**
- Required action outside agent's defined scope
- Task requires capabilities agent doesn't have
- Attempting to perform another agent's task

**Format:**
```
SCOPE ERROR: Trying to complete {step}, want to {action}, but not in scope
```

**Examples:**
```
SCOPE ERROR: Trying to create validation criteria, want to run statistical tests, but not in scope (that's rq_stats agent)
SCOPE ERROR: Trying to generate code, want to fix bugs in existing code, but not in scope (that's g_debug agent)
SCOPE ERROR: Trying to extract data, want to generate mock data, but not in scope (NEVER generate mock data)
```

**Action:** QUIT immediately, report to master

---

## 2. PLATFORM COMPATIBILITY

### 2.1 Output Encoding

**ASCII-Only Output:**
- Windows cp1252 compatibility
- NO Unicode characters in output
- Test before using: `echo "test"` in terminal

**Character Replacements:**
- Arrows: Use `->` NOT `→`
- Checkmarks: Use `[PASS]` NOT `✓`
- Cross marks: Use `[FAIL]` NOT `✗`
- Bullets: Use `-` or `*` NOT `•`

**Why:** Windows terminal may not support Unicode, causing UnicodeEncodeError

---

### 2.2 File Encoding

**All File Writes:**
- UTF-8 encoding MANDATORY
- Specify encoding explicitly in write operations
- Prevents character encoding issues

**Why:** Ensures cross-platform compatibility and handles international characters correctly

---

### 2.3 Shell Environment

**Use Bash Commands:**
- `ls -lah` NOT `Get-ChildItem`
- `find . -name "*.py"` NOT `Get-ChildItem -Recurse -Filter "*.py"`
- `grep -r "pattern"` NOT `Select-String`

**Why:** Project uses Bash on Windows, not PowerShell

---

### 2.4 Operating System

**Windows Environment:**
- Path separators: Use forward slashes `/` or `os.path.join()`
- Line endings: LF (`\n`) preferred, CRLF (`\r\n`) acceptable
- Case sensitivity: Assume case-insensitive file system

---

## 3. REPORT FORMAT TO MASTER

**Purpose:** Inform master of task completion or error

### 3.1 Success Reports

**Format:** Informal text confirming task completion

**Examples:**
```
Successfully built results/ch5/rq1/ structure with status.yaml
Successfully created 1_concept.md for ch5/rq1
Validated - 3 claims verified with evidence sources
Created 2_plan.md - 5 steps planned
Generated step01_calibrate_irt.py - all validations passed
```

---

### 3.2 Error Reports

**Format:** Specify which circuit breaker triggered + details

**Examples:**
```
EXPECTATIONS ERROR: To perform step 3 I expect 1_concept.md, but file missing
STEP ERROR: Trying to complete step 8 but prior analysis steps not all success
TOOL ERROR: Tried to use tools.analysis_irt.calibrate_grm but module not found
CLARITY ERROR: Trying to specify data source but 1_concept.md doesn't indicate master.xlsx or other RQ
SCOPE ERROR: Trying to fix code bugs, want to modify original files, but not in scope
```

---

**End of Universal Best Practices**
