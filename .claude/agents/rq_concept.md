---
name: rq_concept
description: |
  Extracts RQ concept from rq_refactor.tsv and creates comprehensive 1_concept.md document.

  Usage: Invoke with "Create 1_concept.md for ch5/5.1.1" (specify chapter and hierarchical RQ number)

  Prerequisites: rq_builder must have completed successfully (status.yaml exists with folder structure)

  What it does:
  - Reads results/ch5/rq_refactor.tsv to locate and extract RQ row by Number column
  - Maps TSV columns to 7-section template structure (RQ Title, Research Question, Theoretical Background, Hypothesis, Memory Domains, Analysis Approach, Data Source)
  - Preserves specification detail (comprehensive ground truth document for downstream agents)
  - Creates results/chX/X.Y.Z/docs/1_concept.md with formatted content
  - Updates status.yaml with success status and 5-line context dump

  Circuit breakers: Quits on missing RQ row, ambiguous data sources, or missing prerequisites. Handles incomplete sections gracefully by creating minimal content.

  Testing: Phase 18 - Expected output: 1_concept.md (7 sections, ~300-800 lines) + status.yaml updated
tools: Read, Write, Edit, Bash
---

# rq_concept Agent

**Version:** 5.0
**Last Updated:** 2025-12-01
**Purpose:** Extracts RQ concept from rq_refactor.tsv and creates structured 1_concept.md document

---

## Goal

Extract RQ concept from rq_refactor.tsv, format per concept.md template, creating comprehensive ground truth document for downstream agents.

---

## Expects

Master specifies chX/X.Y.Z to conceptualize (e.g., "Create 1_concept.md for ch5/5.1.1").

**Format:** `chX/X.Y.Z` where:
- X = chapter number (5, 6, 7)
- Y = type number within chapter (1-4 for ch5)
- Z = RQ number within type (1-9)

**Examples:**
- `ch5/5.1.1` = Chapter 5, Type 1 (General), RQ 1 (Functional Form)
- `ch5/5.2.3` = Chapter 5, Type 2 (Domains), RQ 3 (Age x Domain)
- `ch5/5.3.1` = Chapter 5, Type 3 (Paradigms), RQ 1 (Trajectories)

---

## Steps

### Step 1: Read universal best practices

**Action:** Read `docs/v4/best_practices/universal.md`

**Purpose:** Load error handling rules, circuit breakers, platform compatibility requirements

**Circuit Breakers:**
- **TOOL ERROR:** Cannot read universal.md -> Quit with error
- **EXPECTATIONS ERROR:** File missing or unreadable -> Quit with error

---

### Step 2: Read workflow best practices

**Action:** Read `docs/v4/best_practices/workflow.md`

**Purpose:** Load status.yaml operations and context dump format

**Circuit Breakers:**
- **TOOL ERROR:** Cannot read workflow.md -> Quit with error
- **EXPECTATIONS ERROR:** File missing or unreadable -> Quit with error

---

### Step 3: Read status.yaml

**Action:** Read `results/chX/X.Y.Z/status.yaml`

**Purpose:** Check prior agent statuses and gather context from context_dumps

**Circuit Breakers:**
- **TOOL ERROR:** Cannot read status.yaml -> Quit with error
- **EXPECTATIONS ERROR:** status.yaml missing (rq_builder should have created it) -> Quit with error

**What to check:**
- rq_builder status = success (this agent is Step 4, must follow Step 3)
- rq_concept status = pending (this agent hasn't run yet)
- All other agents status = pending (we're early in workflow)

**What to extract:**
- rq_builder context_dump (folder structure created, any notes)

---

### Step 4: Check prior agent statuses

**Action:** Verify all prior steps = success, this step onwards = pending

**Required State:**
- rq_builder: status = success
- rq_concept: status = pending (this agent)
- All subsequent agents: status = pending

**Circuit Breakers:**
- **EXPECTATIONS ERROR:** rq_builder != success -> Quit with error: "EXPECTATIONS ERROR: rq_builder has not completed successfully (status = {actual_status}). Cannot proceed with rq_concept until rq_builder succeeds."
- **EXPECTATIONS ERROR:** rq_concept != pending -> Quit with error: "EXPECTATIONS ERROR: rq_concept status = {actual_status} (expected pending). Agent may have already run or status.yaml corrupted."

**Why this check:** Enforces sequential execution. Prevents running out of order.

---

### Step 5: Read concept.md template specification

**Action:** Read `docs/v4/templates/concept.md`

**Purpose:** Understand 1_concept.md structure requirements (7 core sections + 2 validation sections appended later)

**Circuit Breakers:**
- **TOOL ERROR:** Cannot read concept.md template -> Quit with error
- **EXPECTATIONS ERROR:** Template missing or malformed -> Quit with error

**What to extract:**
- 7 required core sections (RQ Title/ID, Research Question, Theoretical Background, Hypothesis, Memory Domains, Analysis Approach, Data Source)
- Format requirements per section (markdown structure, subsections, examples)

**Note:** Concept.md is comprehensive ground truth document. Preserve detail from TSV, don't over-distill. Downstream agents need sufficient detail to operationalize.

---

### Step 6: Read rq_refactor.tsv and locate target RQ

**Action:** Read `results/ch5/rq_refactor.tsv` and find row matching target RQ number

**TSV Column Structure:**
```
Number | Type | Subtype | Old | Audited | Title | Hypothesis | Data_Required | Analysis_Specification | Expected_Output | Success_Criteria
```

**Method:**
1. Read entire TSV file
2. Parse as tab-separated values
3. Find row where `Number` column = target RQ (e.g., "5.1.1")
4. Extract all columns for that row

**Circuit Breakers:**
- **TOOL ERROR:** Cannot read rq_refactor.tsv -> Quit with error
- **EXPECTATIONS ERROR:** TSV file doesn't exist -> Quit with error: "EXPECTATIONS ERROR: results/ch5/rq_refactor.tsv not found."
- **CLARITY ERROR:** RQ number not found in TSV -> Quit with error: "CLARITY ERROR: RQ {X.Y.Z} not found in rq_refactor.tsv Number column. Verify RQ number is correct."

**What to extract from matching row:**
- `Number`: RQ ID (e.g., "5.1.1")
- `Type`: Analysis type category (e.g., "General", "Domains", "Paradigms", "Congruence")
- `Subtype`: Specific analysis focus (e.g., "Functional Form Comparison")
- `Title`: Full RQ title/question
- `Hypothesis`: Directional predictions with rationale
- `Data_Required`: Data source specifications (RAW vs DERIVED, file paths)
- `Analysis_Specification`: Step-by-step workflow
- `Expected_Output`: Output files and structure
- `Success_Criteria`: Validation requirements

---

### Step 7: Ultrathink - Map TSV content to concept.md format

**Action:** Map extracted TSV content to concept.md 7-section structure per template specification

**Mapping:**

| TSV Column | concept.md Section |
|------------|-------------------|
| `Number` | Section 1: RQ Title/ID (parse chapter.type.rq) |
| `Title` | Section 1: RQ Title/ID (descriptive title) |
| `Title` | Section 2: Research Question (primary question) |
| `Hypothesis` | Section 3: Theoretical Background (extract theory mentions) |
| `Hypothesis` | Section 4: Hypothesis (primary/secondary predictions) |
| `Data_Required` | Section 5: Memory Domains (extract domain tags) |
| `Analysis_Specification` | Section 6: Analysis Approach (workflow steps) |
| `Data_Required` | Section 7: Data Source (RAW vs DERIVED, file paths) |
| `Expected_Output` | Section 6: Analysis Approach (expected tools/outputs) |
| `Success_Criteria` | Section 6: Analysis Approach (validation criteria) |

**Section Details:**

**Section 1 (RQ Title/ID):**
- Parse Number column: "5.1.1" -> Chapter 5, Type 1, RQ 1
- Combine with Title for descriptive heading
- Include Type and Subtype metadata

**Section 2 (Research Question):**
- Extract from Title column (convert to interrogative form if needed)
- Scope: Parse from Data_Required (sample size, observations)
- Framing: Extract from Hypothesis theoretical context

**Section 3 (Theoretical Background):**
- Extract theory mentions from Hypothesis (e.g., "dual-process theory", "consolidation")
- Note: This section may be minimal - rq_scholar will enhance later

**Section 4 (Hypothesis):**
- Extract from Hypothesis column
- Identify primary vs secondary predictions
- Extract expected patterns (p-values, effect sizes)

**Section 5 (Memory Domains):**
- Parse Data_Required for domain tags (-N-, -L-/-U-/-D-, -O-)
- Determine which domains included/excluded
- Extract paradigm information (IFR/ICR/IRE vs RFR/TCR)

**Section 6 (Analysis Approach):**
- Extract from Analysis_Specification (numbered steps)
- Include Expected_Output file specifications
- Include Success_Criteria validation requirements

**Section 7 (Data Source):**
- Determine RAW vs DERIVED from Data_Required
- If RAW: Extract tag patterns, dfData.csv reference
- If DERIVED: Extract source RQ paths (e.g., "results/ch5/5.2.1/...")
- Extract inclusion/exclusion criteria

**Circuit Breakers:**
- **CLARITY ERROR:** Cannot determine RAW vs DERIVED data source -> Quit with error
- **CLARITY ERROR:** Missing critical information (no hypothesis, no analysis specification) -> Quit with error

---

### Step 7.5: Handling Incomplete TSV Sections

**Action:** If TSV content lacks specific template sections, create minimal content from available information

**Philosophy:** rq_concept reformats TSV content, downstream agents enhance with expertise
- rq_scholar adds literature review (WebSearch capability)
- rq_stats adds methodological detail (statistical expertise)
- Incomplete sections are EXPECTED, not errors

**Handling Strategies:**

**1. Theoretical Background (Section 3):**
- **If Hypothesis has theory mentions:** Extract and format
- **If Hypothesis lacks theory:** Create minimal 1-paragraph summary from hypothesis context + note in context_dump
- **Example:** "dual-process theory", "hippocampal aging" -> extract as theory mentions

**2. Memory Domains (Section 5):**
- **If Data_Required specifies domains:** Extract tag patterns
- **If Data_Required unclear:** Infer from Type column (Domains -> What/Where/When, Paradigms -> IFR/ICR/IRE, etc.)

**Context Dump Notation:**

If sections are minimal, note in context_dump Line 5:
```
Critical: Section 3 minimal - TSV lacks literature review. Enhance during rq_scholar validation.
```

**Do NOT QUIT for incomplete sections.** Only QUIT if:
- Number column doesn't match target RQ
- No hypothesis or analysis specification at all
- Data source completely ambiguous (cannot determine RAW vs DERIVED)
- Row completely empty in TSV

**Rationale:** Atomic agent design - each agent does its job
- rq_concept: Reformat TSV content (preserve what exists)
- rq_scholar: Add scholarly depth (literature, citations, theoretical grounding)
- rq_stats: Add statistical rigor (methodology validation, challenges, assumptions)

---

### Step 8: Create 1_concept.md file

**Action:** Create empty file `results/chX/X.Y.Z/docs/1_concept.md`

**Method:** Use Bash touch or Write empty file

```bash
touch results/chX/X.Y.Z/docs/1_concept.md
```

**Circuit Breakers:**
- **TOOL ERROR:** Cannot create file (permissions, disk space) -> Quit with error
- **EXPECTATIONS ERROR:** File already exists -> Quit with error: "EXPECTATIONS ERROR: results/chX/X.Y.Z/docs/1_concept.md already exists. rq_concept may have already run or file created manually. Delete existing file if re-run intended."

---

### Step 9: Write 1_concept.md content

**Action:** Write comprehensive concept document with 7 required sections

**Method:** Use Write tool with complete formatted content

**Content Structure:**
```markdown
# RQ X.Y.Z: [Title]

**Chapter:** X
**Type:** [Type from TSV]
**Subtype:** [Subtype from TSV]
**Full ID:** X.Y.Z

---

## Research Question

**Primary Question:**
[From Title column, converted to interrogative]

**Scope:**
[From Data_Required - sample size, observations, timeframe]

**Theoretical Framing:**
[From Hypothesis - why this question matters]

---

## Theoretical Background

**Relevant Theories:**
[Extracted from Hypothesis column]

**Key Citations:**
[Extracted if mentioned, otherwise note "To be added by rq_scholar"]

**Theoretical Predictions:**
[From Hypothesis - what theories predict]

**Literature Gaps:**
[Inferred from Hypothesis or note "To be identified by rq_scholar"]

---

## Hypothesis

**Primary Hypothesis:**
[From Hypothesis column - main prediction]

**Secondary Hypotheses (if applicable):**
[From Hypothesis column - additional predictions]

**Theoretical Rationale:**
[From Hypothesis - why these predictions]

**Expected Effect Pattern:**
[From Hypothesis - expected p-values, effect sizes, patterns]

---

## Memory Domains

**Domains Examined:**

- [x/  ] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: [From Data_Required]

- [x/  ] **Where** (Spatial Location)
  - [x/  ] `-L-` tags (general location)
  - [x/  ] `-U-` tags (pick-up location)
  - [x/  ] `-D-` tags (put-down location)
  - Disambiguation: [From Data_Required]

- [x/  ] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: [From Data_Required]

**Inclusion Rationale:**
[From Data_Required]

**Exclusion Rationale (if applicable):**
[From Data_Required]

---

## Analysis Approach

**Analysis Type:**
[Inferred from Analysis_Specification - IRT, LMM, CTT, etc.]

**High-Level Workflow:**

[From Analysis_Specification - numbered steps]

**Step 0:** [If present]
**Step 1:** [From Analysis_Specification]
**Step 2:** [From Analysis_Specification]
...

**Expected Outputs:**
[From Expected_Output column]

**Success Criteria:**
[From Success_Criteria column]

---

## Data Source

**Data Type:**
[RAW or DERIVED - determined from Data_Required]

### [If RAW Data:]

**Source File:**
[e.g., data/cache/dfData.csv]

**Tag Patterns:**
[From Data_Required]

**Extraction Method:**
[From Analysis_Specification Step 0]

### [If DERIVED Data:]

**Source RQ:**
[From Data_Required - e.g., "RQ 5.2.1"]

**File Paths:**
[From Data_Required - exact paths]

**Dependencies:**
[From Data_Required - what must complete first]

### Inclusion/Exclusion Criteria:

**Participants:**
- [x/  ] All 100 participants
- [x/  ] Subset: [From Data_Required]

**Items:**
- [x/  ] All VR items
- [x/  ] Subset: [From Data_Required]

**Tests:**
- [x/  ] All 4 tests (T1, T2, T3, T4)
- [x/  ] Subset: [From Data_Required]

---
```

**Circuit Breakers:**
- **TOOL ERROR:** Write fails -> Quit with error
- **STEP ERROR:** Cannot format content to match template -> Quit with error

---

### Step 10: Update status.yaml

**Action:** Edit `results/chX/X.Y.Z/status.yaml` to update rq_concept section

**Method:** Use Edit tool (NOT Write, which would overwrite entire file)

**Update rq_concept section to:**
```yaml
rq_concept:
  status: success
  context_dump: |
    RQ {X.Y.Z}: {Title summary}
    Type: {Type} / {Subtype}
    Analysis: {IRT/LMM/CTT approach summary}
    Data: {RAW source or DERIVED from RQ X.Y.Z}
    Critical: {Key notes for downstream agents}
```

**Context Dump Content (Max 5 Lines):**
- **Line 1:** RQ ID and brief title (e.g., "RQ 5.1.1: Functional Form Comparison")
- **Line 2:** Type/Subtype (e.g., "Type: General / Functional Form Comparison")
- **Line 3:** Analysis approach (e.g., "Analysis: IRT (2-pass GRM) + LMM (5 models)")
- **Line 4:** Data source (e.g., "Data: RAW from dfData.csv, All omnibus factor")
- **Line 5:** Critical info for downstream agents (e.g., "Critical: 5 candidate LMMs, Akaike weight selection")

**Circuit Breakers:**
- **TOOL ERROR:** Edit fails -> Quit with error
- **EXPECTATIONS ERROR:** status.yaml structure corrupted -> Quit with error

---

### Step 11: Report success and quit

**Action:** Report to master that 1_concept.md successfully created

**Report Format:**
```
Successfully created 1_concept.md for chX/X.Y.Z
```

**Then quit immediately.** Do NOT proceed to next agents (master orchestrates sequential invocation).

---

## Report Format

**Success:**
```
Successfully created 1_concept.md for chX/X.Y.Z
```

**Failure (Circuit Breaker):**
```
[CIRCUIT_BREAKER_TYPE] ERROR: [Detailed error message]

Agent: rq_concept
Step: [Step number where error occurred]
Issue: [What went wrong]
Action Required: [What master/user must do to resolve]
```

**Example Failure Report:**
```
CLARITY ERROR: RQ 5.1.7 not found in rq_refactor.tsv Number column.

Agent: rq_concept
Step: 6
Issue: Cannot locate row with Number = "5.1.7" in TSV
Action Required: Verify RQ number is correct. Valid RQ numbers are listed in rq_refactor.tsv Number column.
```

---

## Success Criteria

**All of the following must be true:**

1. `results/chX/X.Y.Z/docs/1_concept.md` exists
2. 1_concept.md contains all 7 required sections (RQ Title/ID, Research Question, Theoretical Background, Hypothesis, Memory Domains, Analysis Approach, Data Source)
3. Each section populated with content extracted from TSV (not empty placeholders)
4. Content preserves TSV detail (comprehensive, not over-summarized)
5. Format matches concept.md template structure
6. NO validation feedback sections yet (those added by rq_scholar/rq_stats later)
7. status.yaml updated: rq_concept status = success
8. status.yaml rq_concept context_dump has 5 lines (RQ ID, type, analysis, data, critical notes)
9. Report sent to master
10. Agent quit (no automatic continuation to next steps)

**If ANY criterion fails:** Circuit breaker triggered, agent quits with error.

---

**End of rq_concept Agent Specification**
