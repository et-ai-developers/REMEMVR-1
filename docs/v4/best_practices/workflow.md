# Agent Best Practices - Workflow

**Version:** 5.0
**Last Updated:** 2025-12-01
**Purpose:** Workflow-specific best practices for RQ-specific agents using status.yaml
**Audience:** 10/13 workflow agents (rq_builder, rq_concept, rq_scholar, rq_stats, rq_planner, rq_tools, rq_analysis, rq_inspect, rq_plots, rq_results)

**NOT for:** g_conflict, g_code, g_debug (general-purpose agents that don't use status.yaml)

---

## 1. RQ NUMBERING FORMAT

### 1.1 Hierarchical Numbering (Chapter 5)

**Format:** `X.Y.Z` where:
- X = chapter number (5, 6, 7)
- Y = type number within chapter (1-4 for ch5)
- Z = RQ number within type (1-9)

**Chapter 5 Types:**
| Type | Y | Name | Description |
|------|---|------|-------------|
| General | 1 | 5.1.X | Omnibus "All" factor analysis |
| Domains | 2 | 5.2.X | What/Where/When analysis |
| Paradigms | 3 | 5.3.X | Free/Cued/Recognition analysis |
| Congruence | 4 | 5.4.X | Common/Congruent/Incongruent analysis |

**Examples:**
- `5.1.1` = Chapter 5, General type, RQ 1 (Functional Form)
- `5.2.3` = Chapter 5, Domains type, RQ 3 (Age x Domain)
- `5.3.1` = Chapter 5, Paradigms type, RQ 1 (Trajectories)
- `5.4.2` = Chapter 5, Congruence type, RQ 2 (Consolidation)

### 1.2 Invocation Format

**When invoking agents, use:** `chX/X.Y.Z`

**Examples:**
- `ch5/5.1.1` = Chapter 5, RQ 5.1.1
- `ch5/5.2.3` = Chapter 5, RQ 5.2.3

**NOT:** `ch5/rq1` (old format - deprecated)

---

## 2. YAML PARSING & STATUS CHECKING

### 2.1 Reading status.yaml

**Method:**
1. Use Read tool to read status.yaml file
2. Parse YAML structure using general LLM reasoning
3. NO programmatic YAML parser needed

**Pattern Matching:**
```yaml
rq_concept:
  status: success
  context_dump: |
    RQ 5.1.1: Functional Form Comparison
    Type: General / Functional Form
```

**How to Check:**
- Look for lines like `"rq_concept:\n  status: success"`
- Extract status value via pattern matching
- Read context_dump multiline string

**If Parsing Unclear:**
- Trigger CLARITY ERROR
- Report to master with specific parsing issue

---

## 3. CONTEXT DUMP FORMAT

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
- RQ ID and title (e.g., "RQ 5.1.1: Functional Form")
- Type/Subtype (e.g., "Type: General / Functional Form")
- Analysis type (IRT/LMM/CTT)
- Key decisions made
- Critical information for downstream agents

**What NOT to Include:**
- Detailed methodology
- Complete file contents
- Verbose explanations
- Redundant information

**Example:**
```yaml
rq_concept:
  status: success
  context_dump: |
    RQ 5.1.1: Functional Form Comparison
    Type: General / Functional Form
    Analysis: IRT (2-pass GRM) + LMM (5 models)
    Data: RAW from dfData.csv, All omnibus factor
    Critical: 5 candidate LMMs, Akaike weight selection
```

---

## 4. FILE PATH CONVENTIONS

### 4.1 RQ Folder Path Format

**Format:** `results/chX/X.Y.Z/`

**Examples:**
- `results/ch5/5.1.1/` - Chapter 5, General type, RQ 1
- `results/ch5/5.2.3/` - Chapter 5, Domains type, RQ 3
- `results/ch5/5.3.1/` - Chapter 5, Paradigms type, RQ 1

**NOT:** `results/ch5/rq1/` (old format - deprecated)

### 4.2 Standard RQ Structure

```
results/chX/X.Y.Z/
  status.yaml                (agent statuses, context dumps)
  audit.md                   (audit results from rq_audit)
  fix_report.md              (fix results from rq_fixer)
  docs/                      (specifications)
    1_concept.md
    2_plan.md
    3_tools.yaml
    4_analysis.yaml
  data/                      (analysis outputs)
    step00_*.csv             (Step 0 extraction outputs)
    stepN_*.csv              (Step N data outputs)
  code/                      (generated scripts)
    step00_*.py              (Step 0 extraction code)
    stepN_*.py               (Step N analysis code)
  logs/                      (execution logs)
    stepN_*.log
  plots/                     (visualizations)
    plots.py
    stepN_*.png
    stepN_*_data.csv         (plot source data)
  results/                   (final summaries)
    summary.md
```

### 4.3 Cross-RQ References

**When referencing other RQs, use full hierarchical path:**

```
results/ch5/5.1.1/data/step03_theta_scores.csv
results/ch5/5.2.1/data/step00_irt_input.csv
```

**NOT:** `results/ch5/rq1/...` (old format)

### 4.4 Relative vs Absolute Paths

**Relative Paths:**
- Use paths relative to `results/chX/X.Y.Z/` within that RQ's specifications

**Absolute Paths:**
- Use when referencing files outside RQ folder
- Examples: `docs/v4/templates/`, `data/cache/dfData.csv`

---

## 5. DATA SOURCE CONVENTIONS

### 5.1 Root RQs (Extract from Raw Data)

**Root RQs by type:**
- **5.1.1** - General ROOT (extracts from dfData.csv with "All" factor)
- **5.2.1** - Domains ROOT (extracts from dfData.csv with What/Where/When)
- **5.3.1** - Paradigms ROOT (extracts from dfData.csv with IFR/ICR/IRE)
- **5.4.1** - Congruence ROOT (extracts from dfData.csv with Common/Congruent/Incongruent)

**Root RQs have:**
- Step 0 that extracts from `data/cache/dfData.csv`
- No dependencies on other RQs
- Create foundational outputs for downstream RQs

### 5.2 Derived RQs (Use Outputs from Root/Prior RQs)

**Derived RQs:**
- Source data from root RQ or prior RQ outputs
- Reference using full hierarchical path: `results/ch5/5.1.1/data/...`
- Must specify dependencies in 1_concept.md

**Example Dependencies:**
```
RQ 5.1.2 depends on RQ 5.1.1 outputs:
- results/ch5/5.1.1/data/step03_theta_scores.csv
- results/ch5/5.1.1/data/step06_best_model.pkl
```

---

## 6. VALIDATION GATES

### 6.1 When to Validate

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

### 6.2 How to Validate

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

## 7. TSV REFERENCE

### 7.1 rq_refactor.tsv Location

**File:** `results/ch5/rq_refactor.tsv`

**Purpose:** Authoritative specification database for all Chapter 5 RQs

### 7.2 TSV Columns

| Column | Description |
|--------|-------------|
| Number | Hierarchical RQ ID (e.g., "5.1.1") |
| Type | Analysis category (General, Domains, Paradigms, Congruence) |
| Subtype | Specific analysis focus |
| Old | Old RQ number (for migration reference) |
| Audited | Whether RQ has been audited |
| Title | Full RQ title/question |
| Hypothesis | Directional predictions with rationale |
| Data_Required | Data source specifications |
| Analysis_Specification | Step-by-step workflow |
| Expected_Output | Output files and structure |
| Success_Criteria | Validation requirements |

### 7.3 Using rq_refactor.tsv

**Agents should:**
1. Read entire TSV file
2. Parse as tab-separated values
3. Find row where `Number` column matches target RQ
4. Extract relevant columns for their task

**Circuit Breaker:**
- If RQ number not found in Number column -> CLARITY ERROR

---

**End of Workflow Best Practices**
