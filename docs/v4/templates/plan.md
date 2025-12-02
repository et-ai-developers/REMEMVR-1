# plan.md Template Specification

**Version:** 4.2
**Last Updated:** 2025-12-02
**Purpose:** Specification for 2_plan.md format (analysis plan created by rq_planner agent)
**Audience:** rq_planner agent when creating 2_plan.md for RQ workflow
**Status:** Current (v4.X architecture)

---

## CRITICAL - ASCII-Only Format

**Per universal.md Section 2.1:** ALL content in 2_plan.md must use ASCII-only characters for WSL2/Windows compatibility.

**Mathematical Notation - Use ASCII equivalents ONLY:**
- Multiplication: Use `x` not `×` (example: "100 x 4 tests")
- Set membership: Use `in` not `∈` (example: "theta in [-3, 3]")
- Comparisons: Use `>=` not `≥`, `<=` not `<=`
- Arrows: Use `->` not `→`
- Ranges: Write as words (example: "theta range: [-3, 3]" or "theta: -3 to 3")

**Why:** Unicode symbols (×, ∈, ≥, →) cause encoding issues in WSL2, displaying as � or backspace characters. ASCII ensures universal compatibility.

---

## Overview

### What is 2_plan.md?

The 2_plan.md file is the **master analysis plan** for an RQ. It is created by the **rq_planner agent** and consumed by downstream agents (rq_tools, rq_analysis, g_code, rq_inspect) to understand the step-by-step analysis workflow.

**Key Characteristics:**
- **Agent-to-agent specification** (not user-facing)
- **Numbered step structure** (step 1, step 2, ... step N)
- **Input/output contracts** per step (file paths, formats, columns)
- **Validation requirements** embedded (MANDATORY per step)
- **Dependencies documented** (cross-RQ data requirements if applicable)
- **Tool-agnostic language** (rq_tools determines exact tools, planner specifies what needs to happen)

### Workflow Context

```
Step 9 (Workflow): rq_planner creates 2_plan.md
                   ↓
Step 11 (Workflow): rq_tools reads 2_plan.md  ->  creates 3_tools.yaml
                   ↓
Step 12 (Workflow): rq_analysis reads 2_plan.md + 3_tools.yaml  ->  creates 4_analysis.yaml
                   ↓
Step 14 (Workflow): g_code reads 4_analysis.yaml (derived from plan)  ->  generates code
                   ↓
Step 14 (Workflow): rq_inspect reads 2_plan.md  ->  validates outputs match expectations
```

**Critical Role:** The plan is the **contract** between planning agents and execution agents. If plan is vague, downstream agents will fail or guess incorrectly.

---

## CRITICAL: Validation Requirements

### Global Validation Mandate

**EVERY analysis step in 2_plan.md MUST include validation requirements.**

This is not optional. This is not "nice to have." This is the **foundation of v4.X architecture** preventing cascading failures that plagued v3.0.

**⚠️ CRITICAL: This includes plot data preparation steps!** Plot data preparation IS an analysis step (executes in Step 14 CODE EXECUTION LOOP, validated by rq_inspect). Every plot data preparation step MUST have:
1. "Validation tools MUST be used after..." statement
2. All 4 substance criteria layers (Output Files, Value Ranges, Data Quality, Log Validation)

### Mandatory Text (From Specification)

The plan MUST state for each step:

> **"Validation tools MUST be used after analysis tool execution"**

**Rationale:**
- **v3.0 Problem:** Analysis errors cascaded to downstream steps (bad theta  ->  bad LMM  ->  bad plots  ->  bad results)
- **v4.X Solution:** Embedded validation catches errors immediately at source step
- **Architecture Dependency:** rq_tools reads plan  ->  specifies validation tools per step  ->  rq_analysis embeds validation calls  ->  g_code generates scripts with validation  ->  errors caught before cascade

### How rq_planner States This

**In each step's specification:**

```
### Step N: [Step Name]

**Purpose:** [What this step accomplishes]

**Input:**
- [Input files/data]

**Processing:**
- [What analysis happens]

**Output:**
- [Output files/data]

**Validation Requirement:**
Validation tools MUST be used after analysis tool execution. Specific validation
tools will be determined by rq_tools based on analysis type (IRT calibration
validation, LMM fit validation, data format validation, etc.). The rq_analysis
agent will embed validation tool calls after the analysis tool call for this step.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- [Exact file paths, expected row counts, expected column counts, data types]

*Value Ranges:*
- [Expected value ranges - e.g., theta in [-3, 3], p in [0, 1], scientifically reasonable bounds]

*Data Quality:*
- [Missing data tolerance, expected N, duplicate checks, distribution checks]

*Log Validation:*
- [Required log patterns (e.g., "Model converged: True"), forbidden patterns (e.g., "ERROR"), acceptable warnings]

**Expected Behavior on Validation Failure:**
[What should happen if validation fails - e.g., quit with error, log warning, etc.]
```

### Validation Architecture Flow

```
rq_planner (Step 9):
  ├─ Writes 2_plan.md
  └─ States "Validation tools MUST be used" per step
           ↓
rq_tools (Step 11):
  ├─ Reads 2_plan.md validation requirement
  ├─ Reads tool_inventory.md (validation tools section)
  ├─ Writes 3_tools.yaml
  └─ Specifies BOTH analysis tool + validation tool per step
           ↓
rq_analysis (Step 12):
  ├─ Reads 2_plan.md + 3_tools.yaml
  ├─ Writes 4_analysis.yaml
  └─ Embeds validation tool call AFTER analysis tool call per step
           ↓
g_code (Step 14):
  ├─ Reads 4_analysis.yaml
  ├─ Generates stepN_name.py
  └─ Includes validation function call at end of script
           ↓
bash execution (Step 14):
  ├─ Runs stepN_name.py
  ├─ Analysis tool executes  ->  produces output
  ├─ Validation tool executes  ->  checks output
  └─ If validation fails  ->  error raised  ->  g_debug invoked
```

**Result:** Errors caught immediately at source, not discovered 5 steps later when fixing is expensive.

---

## Required Sections

The 2_plan.md file MUST contain the following 6 sections:

### 1. Step-by-Step Analysis Plan (Numbered Steps)

**Purpose:** Define the complete analysis workflow from data extraction to final outputs.

**Format:**
- **Numbered steps** (Step 1, Step 2, ... Step N)
- **Descriptive names** (from names.md conventions if available, or create new)
- **Step dependencies** (which steps must complete before this one)
- **Estimated complexity** (optional - helps user gauge runtime)

**Note on Step Numbering:**
- **Documentation format:** "Step 0", "Step 1", "Step 2" (human-readable, no zero-padding)
- **File naming format:** "step00", "step01", "step02" (machine-readable, zero-padded for sorting per names.md)
- This distinction separates human-readable documentation from machine-readable filenames

**Example Structure:**

```markdown
## Analysis Plan

This RQ requires N steps:

### Step 1: Extract IRT Item Data

**Dependencies:** None (first step)
**Complexity:** Low (data extraction only)

[Input/Output/Processing/Validation sections - see below]

### Step 2: Calibrate IRT Model (Pass 1)

**Dependencies:** Step 1 (requires extracted item data)
**Complexity:** High (60+ minute model calibration)

[Input/Output/Processing/Validation sections]

### Step 3: Purify Items (2-Pass Methodology)

**Dependencies:** Step 2 (requires Pass 1 item parameters)
**Complexity:** Low (filtering based on thresholds)

[Input/Output/Processing/Validation sections]

[... continue for all N steps]
```

**Key Principles:**
- **Linear order** (step N cannot depend on step N+5)
- **Logical grouping** (data extraction  ->  calibration  ->  validation  ->  reporting)
- **Named clearly** (anyone reading plan understands what step does)
- **Realistic complexity** (don't claim "low" if 60-minute runtime expected)

---

### 2. Input Specifications Per Step

**Purpose:** Define exactly what data/files each step requires to execute.

**Format:**
- **File paths** (relative to RQ root: results/chX/X.Y.Z/)
- **File formats** (CSV, YAML, TXT, etc.)
- **Required columns** (if CSV/tabular data)
- **Data types** (string, int, float, bool)
- **Expected values** (ranges, categories, null handling)

**FOLDER STRUCTURE (v4.2 - Updated 2025-12-02):**
```
/code    = ALL .py code files for running analysis
/data    = ALL inputs AND outputs from analysis steps (intermediate + final)
/docs    = ALL planning documentation (1_concept.md, 2_plan.md, 3_tools.yaml, 4_analysis.yaml, validation reports)
/logs    = ONLY .log files (execution logs from each step - stdout/stderr capture)
/plots   = EMPTY until rq_plots generates PNG/PDF visualizations
/results = EMPTY until rq_results generates summary.md
```

**Example Structure:**

```markdown
### Step 1: Extract IRT Item Data

**Input:**

**File:** data/master.xlsx (project-level data source)

**Required Sheets:**
- `Data` sheet with columns:
  - `UID` (string, format: DDD-SSS-TTT, e.g., VRA-001-000)
  - Tags matching domain pattern `RVR-{domain}-*` where domain in {OBJ, LOC, SPA, TEM, ACT}

**Filters:**
- Paradigm: `V` (VR paradigm, not R for Reality Check)
- Domain codes: Specified in 1_concept.md (e.g., OBJ+LOC for object-location binding)

**Expected Data Volume:**
- ~100 participants x 4 test sessions x N items per domain = ~400 x N rows
```

**Example Structure (Mid-Workflow Step):**

```markdown
### Step 3: Purify Items (2-Pass Methodology)

**Input:**

**File 1:** data/pass1_item_params.csv
**Source:** Generated by Step 2 (IRT calibration)
**Format:** CSV with columns:
  - `item_code` (string, format: RVR-{domain}-{variant}-{subtype}, e.g., RVR-OBJ-F-MC)
  - `Difficulty` (float, range typically -3.0 to +3.0, extreme values indicate misfit)
  - `Discrimination` (float, range typically 0.0 to 4.0, values <0.4 indicate poor discrimination)
  - `Dimension` (string, e.g., "object", "location" for multivariate IRT)

**Expected Rows:** 102 items (example - actual count depends on 1_concept.md domain specification)

**File 2:** config/irt_purification_thresholds.yaml
**Source:** Created by rq_tools (Step 11 workflow) based on Decision D039
**Format:** YAML with keys:
  - `max_difficulty: 3.0` (items with |b| > 3.0 excluded)
  - `min_discrimination: 0.4` (items with a < 0.4 excluded)

**Filters:**
- Apply to pass1_item_params.csv to identify items meeting thresholds
- Exclusion logic: item retained if (|Difficulty| <= 3.0) AND (Discrimination >= 0.4)
```

**Key Principles:**
- **Specificity** (exact column names, not "item parameters")
- **Format documentation** (UID format examples, not just "string")
- **Expected values** (ranges help validation tools detect anomalies)
- **Source attribution** (which step produced this file, or is it external?)
- **Dependency clarity** (if file missing, which prior step failed?)

---

### 3. Output Specifications Per Step

**Purpose:** Define exactly what data/files each step produces.

**Format:**
- **File paths** (relative to RQ root)
- **File formats** (CSV, PNG, YAML, TXT, etc.)
- **Column schema** (if tabular)
- **Dimensions** (if plotting - PNG 800 x 600 @ 300 DPI)
- **Expected row counts** (if known - helps validation)

**CRITICAL - Folder Destinations:**
- **ALL analysis outputs** (CSV, TXT, etc.) go to `data/` folder
- **Execution logs** (.log files only) go to `logs/` folder
- `plots/` stays EMPTY until rq_plots runs (generates PNG/PDF there)
- `results/` stays EMPTY until rq_results runs (generates summary.md there)

**Example Structure:**

```markdown
### Step 1: Extract IRT Item Data

**Output:**

**File 1:** data/irt_items_wide.csv
**Format:** CSV, wide format (one row per participant-test combination)
**Columns:**
  - `composite_ID` (string, format: {UID}_{test}, e.g., VRA-001-000_0)
  - One column per item_code (e.g., `RVR-OBJ-F-MC`, `RVR-LOC-N-MC`, ...)
  - Values: {0, 1, NaN} (0=incorrect, 1=correct, NaN=missing/not administered)
**Expected Rows:** ~400 (100 participants x 4 tests)
**Expected Columns:** ~102 items + 1 composite_ID column = 103 total

**File 2:** data/item_metadata.csv
**Format:** CSV, one row per item
**Columns:**
  - `item_code` (string, unique identifier)
  - `domain` (string, e.g., "OBJ", "LOC")
  - `variant` (string, e.g., "F" for face, "N" for name)
  - `subtype` (string, e.g., "MC" for multiple choice)
**Expected Rows:** ~102 items
```

**Example Structure (Plot Data Preparation Step - creates source CSV in data/):**

```markdown
### Step 7: Prepare Trajectory Plot Data

**Output:**

**File 1:** data/step07_trajectory_theta_data.csv
**Format:** CSV, plot source data for theta-scale trajectory
**Columns:**
  - `time` (float): TSVR hours
  - `theta` (float): Mean theta per group per timepoint
  - `CI_lower` (float): Lower 95% confidence bound
  - `CI_upper` (float): Upper 95% confidence bound
  - `domain` (string): Memory domain grouping
**Expected Rows:** 12 (3 domains x 4 timepoints)
**Note:** This CSV is read by rq_plots later. PNG output goes to plots/ when rq_plots runs.

**File 2:** data/step07_trajectory_probability_data.csv
**Format:** CSV, plot source data for probability-scale trajectory (Decision D069 dual-scale)
**Columns:** Same as theta_data but with probability values (0-1 scale)
```

**Note:** Analysis steps create plot SOURCE CSVs in `data/`. The actual PNG/PDF plots are generated later by rq_plots and saved to `plots/`.

**Key Principles:**
- **Completeness** (list ALL outputs, not just primary files)
- **Format precision** (PNG 800 x 600 @ 300 DPI, not "image file")
- **Schema documentation** (column names prevent downstream API mismatches)
- **Expected counts** (row/column counts help validation detect errors)
- **Metadata files** (YAML metadata helps rq_results summarize plots)

**Example Structure (Plot Data Preparation Step - CRITICAL for Option B Architecture):**

```markdown
### Step 7: Prepare Trajectory Plot Data

**⚠️ CRITICAL NOTE:** Plot data preparation IS an analysis step. It:
- Gets executed in Step 14 CODE EXECUTION LOOP (g_code  ->  bash  ->  rq_inspect)
- MUST have validation requirements (same as any analysis step)
- Outputs to plots/*.csv (not data/*.csv) but still validated by rq_inspect
- Created by g_code during analysis (NOT by rq_plots during visualization)

**Purpose:** Aggregate analysis outputs for trajectory visualization (Option B: g_code creates plot source CSV)

**Dependencies:** Steps 3, 4 (requires theta_scores.csv, tsvr_mapping.csv from prior analysis)
**Complexity:** Low (data aggregation, no model fitting)

**Plot Description:** Trajectory over time with confidence bands showing theta decline across memory domains

**Required Data Sources:**
- data/theta_scores.csv (columns: composite_ID, theta, SE, domain)
- data/observed_means.csv (columns: test, domain, mean_theta, CI_lower, CI_upper)
- data/tsvr_mapping.csv (columns: composite_ID, TSVR_hours, test)

**Output (Plot Source CSV):** data/step07_trajectory_theta_data.csv

**Required Columns:**
- `time` (float): TSVR hours (0, 24, 72, 144 for T0-T3)
- `theta` (float): Mean theta per domain per timepoint
- `CI_lower` (float): Lower 95% confidence bound
- `CI_upper` (float): Upper 95% confidence bound
- `domain` (string): Memory domain (What/Where/When)

**Expected Rows:** 12 (3 domains x 4 timepoints)

**Aggregation Logic:**
1. Merge theta_scores with tsvr_mapping on composite_ID (adds TSVR_hours, test number)
2. Group by domain + test, compute mean(theta), 95% CI
3. Join with observed_means for confidence intervals
4. Select and rename columns to match required schema
5. Sort by domain, then time
6. Save to data/step07_trajectory_theta_data.csv

**Validation Requirement:**
Validation tools MUST be used after plot data preparation tool execution. Specific validation
tools determined by rq_tools based on plot data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_trajectory_theta_data.csv exists (exact path)
- Expected rows: 12 (3 domains x 4 timepoints)
- Expected columns: 5 (time, theta, CI_lower, CI_upper, domain)
- Data types: float (time, theta, CI bounds), string (domain)

*Value Ranges:*
- time in [0, 168] hours (0=encoding, 168=1 week)
- theta in [-3, 3] (typical IRT ability range)
- CI_lower in [-3, 3], CI_upper in [-3, 3] (confidence bounds)
- domain in {What, Where, When} (categorical)

*Data Quality:*
- No NaN values tolerated (all cells must have valid values)
- Expected N: Exactly 12 rows (no more, no less)
- No duplicate rows (domain x time combinations unique)
- Distribution check: CI_upper > CI_lower for all rows

*Log Validation:*
- Required pattern: "Plot data preparation complete: 12 rows created"
- Required pattern: "All domains represented: What, Where, When"
- Forbidden patterns: "ERROR", "NaN values detected", "Missing domain"
- Acceptable warnings: None expected for plot data preparation

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 12 rows, found 9")
- Log failure to logs/step07_prepare_plot_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- g_debug invoked to diagnose root cause

**Plotting Function (rq_plots will call):** Trajectory plot with confidence bands
- rq_plots agent maps this description to specific tools/plots.py function
- Plot reads data/step07_trajectory_theta_data.csv (created by this step)
- No data aggregation in rq_plots (visualization only per Option B)
- PNG output saved to plots/ folder by rq_plots
```

**CRITICAL NOTE:** Plot source CSVs created DURING ANALYSIS (by g_code), NOT during plotting (by rq_plots). This is Option B architecture - separation of data manipulation (analysis agents) from visualization (plotting agent).

---

### 4. Expected Data Formats Per Step

**Purpose:** Document data transformations and format expectations in detail.

This section provides **additional format details** beyond what fits in Input/Output specifications. Use for:
- **Complex transformations** (wide  ->  long, stacking, merging)
- **Column naming conventions** (from names.md if populated)
- **Data type constraints** (nullable vs non-nullable)
- **Value ranges** (valid ranges help validation)
- **Format migrations** (if step changes format for downstream compatibility)

**Example Structure:**

```markdown
### Step 5: Merge Theta Scores with TSVR

**Data Transformation:**

**Input Format (from Step 4):**
- File: data/theta_scores.csv
- Format: One row per composite_ID (participant-test combination)
- Columns: `composite_ID`, `theta`, `SE`

**Input Format (from master.xlsx):**
- File: data/master.xlsx (Sheet: TSVR_lookup)
- Format: One row per composite_ID
- Columns: `composite_ID`, `TSVR_hours` (time since VR session in hours)

**Merge Logic:**
- **Key:** composite_ID (must match exactly between files)
- **Type:** Left join (keep all theta scores, add TSVR_hours)
- **Null handling:** If TSVR_hours missing for a composite_ID, raise error (validation failure)

**Output Format:**
- File: data/theta_with_tsvr.csv
- Format: One row per composite_ID
- Columns: `composite_ID`, `theta`, `SE`, `TSVR_hours`
- **Expected Rows:** Same as input theta_scores.csv (~400 rows)
- **Expected Nulls:** None (all columns must be non-null after merge)

**Critical Decision (D070):**
TSVR (Time Since VR) in HOURS must be used as LMM time variable, NOT nominal days (0,1,3,6).
Nominal days assume fixed intervals, but actual time varies per participant schedule.
Using TSVR_hours (actual elapsed time) ensures accurate temporal modeling.
```

**Example Structure (Reshape Transformation):**

```markdown
### Step 6: Reshape Theta Data for LMM (Wide  ->  Long)

**Data Transformation:**

**Input Format (from Step 5):**
- File: data/theta_with_tsvr.csv
- Format: Wide (one row per composite_ID)
- Columns: `composite_ID` (format: {UID}_{test}), `theta`, `SE`, `TSVR_hours`
- Example row: `VRA-001-000_0, -0.52, 0.18, 0.0` (encoding session, 0 hours elapsed)

**Reshape Logic:**
- **Parse composite_ID:** Extract UID and test number (e.g., "VRA-001-000_0"  ->  UID="VRA-001-000", test=0)
- **Group by UID:** All 4 test sessions for same participant grouped together
- **Long format:** Each row represents one measurement occasion (test session) for one participant
- **Add test number column:** Extract from composite_ID suffix (_0, _1, _3, _6)

**Output Format:**
- File: data/theta_long.csv
- Format: Long (one row per measurement occasion)
- Columns:
  - `UID` (string, participant identifier, e.g., "VRA-001-000")
  - `test` (int, values: {0, 1, 3, 6}, represents nominal test session)
  - `theta` (float, estimated ability)
  - `SE` (float, standard error)
  - `TSVR_hours` (float, actual time since encoding)
- **Expected Rows:** ~400 rows (100 participants x 4 tests per participant)
- **Grouping:** 4 consecutive rows per UID (test 0, 1, 3, 6)

**Column Naming Convention:**
Per names.md (if populated during RQ 5.1):
- UID: participant identifier (no underscore)
- test: nominal session number (0=encoding, 1=immediate, 3=delay, 6=long-term)
- theta: IRT ability estimate (lowercase, not Theta)
- TSVR_hours: time variable for LMM (uppercase acronym + underscore + unit)
```

**Key Principles:**
- **Transformation clarity** (describe merge/reshape/filter logic step-by-step)
- **Before/after formats** (show input structure  ->  transformation  ->  output structure)
- **Critical decisions** (reference Decision D0XX if transformation based on project-specific requirement)
- **Naming conventions** (document column names, reference names.md if populated)
- **Validation hooks** (expected row counts, null handling, format constraints)

---

### 5. Dependencies on Other RQs (If Applicable)

**Purpose:** Document cross-RQ data dependencies to prevent execution order errors.

**When to Include This Section:**
- **RAW data only:** No dependencies (all RQs use master.xlsx independently)
- **DERIVED data from other RQs:** Dependencies exist (must document)

**Dependency Types:**

```markdown
## Cross-RQ Dependencies

### Dependency Type 1: RAW Data Only (No Dependencies)

**This RQ uses:** Only master.xlsx (project-level data source)
**No dependencies on other RQs:** Can be executed independently
**Execution order:** Flexible (any order within chapter)

**Data Sources:**
- master.xlsx (Sheet: Data) - participant responses
- master.xlsx (Sheet: TSVR_lookup) - timing data
- master.xlsx (Sheet: Demographics) - participant metadata

**Note:** All data extraction uses tools/data.py functions reading master.xlsx directly.
No intermediate outputs from other RQs required.
```

**Example Structure (RQ with Dependencies):**

```markdown
## Cross-RQ Dependencies

### Dependency Type 2: DERIVED Data from Other RQs (Dependencies Exist)

**This RQ requires outputs from:**
- **RQ 5.2.1** (IRT calibration baseline - Domain-Specific Trajectories)
  - File: results/ch5/5.2.1/data/item_parameters_calibrated.csv
  - Used in: Step 2 (apply baseline item parameters to new data)
  - Rationale: RQ 5.2.1 establishes item difficulty/discrimination parameters. This RQ uses those fixed parameters to estimate theta for different participant subgroups.

- **RQ 5.3.1** (Paradigm-Specific Trajectories - provides purification thresholds)
  - File: results/ch5/5.3.1/data/retained_items.csv
  - Used in: Step 1 (filter item set to only retained items)
  - Rationale: RQ 5.3.1 identifies well-performing items. This RQ analyzes only those items to avoid misfit contamination.

**Execution Order Constraint:**
1. RQ 5.2.1 must complete first (provides item_parameters_calibrated.csv)
2. RQ 5.3.1 must complete second (provides retained_items.csv)
3. This RQ executes third (uses both outputs)

**Data Source Boundaries (Per Specification 5.1.6):**
- **RAW data:** master.xlsx columns extracted directly (no RQ dependencies)
- **DERIVED data:** Outputs from other RQs (RQ 5.2.1 and RQ 5.3.1 above)
- **Scope:** This RQ does NOT re-calibrate IRT models (uses RQ 5.2.1 parameters as fixed)

**Validation:**
- Step 1: Check results/ch5/5.2.1/data/item_parameters_calibrated.csv exists (circuit breaker: FILE_MISSING if absent)
- Step 1: Check results/ch5/5.3.1/data/retained_items.csv exists (circuit breaker: FILE_MISSING if absent)
- If either file missing  ->  quit with error  ->  user must execute dependency RQs first

**Reference:** Specification section 5.1.6 (Data Source Boundaries)
```

**Key Principles:**
- **Explicit file paths** (exact location of dependency files)
- **Execution order** (which RQs must complete before this one)
- **Rationale** (WHY dependency exists, not just THAT it exists)
- **Circuit breakers** (what error triggers if dependency file missing)
- **Scope boundaries** (what this RQ does vs reuses from other RQs)

**Note:** Most RQs will have "No Dependencies" (RAW data only). Dependencies are exception, not rule.

---

### 6. Validation Requirements Per Step (MANDATORY)

**Purpose:** Ensure EVERY step has validation requirements stated explicitly with 4-layer substance criteria.

This section is **mandatory per specification**. It is the foundation of v4.X error prevention architecture.

**Required Structure Per Step:**
1. **Validation Requirement Statement:** "Validation tools MUST be used after [tool type] execution"
2. **Substance Validation Criteria (4 layers with explicit headers):**
   - *Output Files:* Exact paths, row counts, column counts, data types
   - *Value Ranges:* Expected value ranges (e.g., theta in [-3, 3], p in [0, 1])
   - *Data Quality:* Missing data tolerance, expected N, duplicate checks, distribution checks
   - *Log Validation:* Required patterns, forbidden patterns, acceptable warnings
3. **Expected Behavior on Validation Failure:** Error handling (quit, log, invoke g_debug)

**Global Statement:**

```markdown
## Validation Requirements

**CRITICAL MANDATE:**

Every analysis step in this plan MUST use validation tools after analysis tool execution.

This is not optional. This is the core architectural principle preventing cascading
failures observed in v3.0 (where analysis errors propagated undetected through 5+
downstream steps before discovery).

**Exact Specification Requirement:**

> "Validation tools MUST be used after analysis tool execution"

**Implementation:**
- rq_tools (Step 11 workflow) will read tool_inventory.md validation tools section
- rq_tools will specify BOTH analysis tool + validation tool per step in 3_tools.yaml
- rq_analysis (Step 12 workflow) will embed validation tool call AFTER analysis tool call in 4_analysis.yaml
- g_code (Step 14 workflow) will generate stepN_name.py scripts with validation function calls
- bash execution (Step 14 workflow) will run analysis  ->  validation  ->  error on validation failure

**Downstream Agent Requirements:**
- **rq_tools:** MUST specify validation tool for EVERY analysis step (no exceptions)
- **rq_analysis:** MUST embed validation tool call for EVERY analysis step (no exceptions)
- **g_code:** MUST generate code with validation function calls (no exceptions)
- **rq_inspect:** MUST verify validation ran successfully (checks logs/stepN_name.log for validation output)
```

**Per-Step Validation Details:**

```markdown
### Validation Requirements By Step

#### Step 1: Extract IRT Item Data

**Analysis Tool:** (determined by rq_tools - likely tools.data.extract_vr_items_wide)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_irt_extraction)

**What Validation Checks (TECHNICAL - rq_inspect scope):**
- Output file exists (data/irt_items_wide.csv)
- Expected column count (~103 columns: composite_ID + 102 items)
- Expected row count (~400 rows: 100 participants x 4 tests)
- No unexpected NaN patterns (>50% NaN per item suggests extraction error)
- composite_ID format correct ({UID}_{test} pattern)
- Item codes match expected domain pattern (RVR-{domain}-*)

**NOTE:** Technical validation (files exist, formats correct, values in bounds) checked by rq_inspect DURING analysis. Scientific plausibility (effect directions, theoretical coherence) checked by rq_results AFTER all analysis complete.

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 102 items, found 73")
- Log failure to logs/step01_extract.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked by master to diagnose root cause

---

#### Step 2: Calibrate IRT Model (Pass 1)

**Analysis Tool:** (determined by rq_tools - likely tools.analysis_irt.calibrate_grm)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_irt_calibration)

**What Validation Checks:**
- Output file exists (data/pass1_item_params.csv)
- Convergence achieved (log-likelihood improved, not NaN)
- Item parameters in valid ranges:
  - Discrimination (a): 0.0 to 10.0 (values >10.0 suggest estimation error)
  - Difficulty (b): -6.0 to +6.0 (extreme values suggest misfit, but not error)
- No NaN parameters (indicates estimation failure)
- Expected row count (102 items = 102 rows)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Item RVR-OBJ-F-MC has NaN discrimination")
- Log failure to logs/step02_calibrate_pass1.log
- Quit script immediately
- g_debug invoked to diagnose (common causes: insufficient data, model misspecification)

---

[Continue for ALL N steps in the plan - EVERY step has validation requirements]
```

**Key Principles:**
- **Global mandate stated upfront** (no ambiguity about requirement)
- **Per-step validation details** (what gets checked, what error triggers)
- **Tool specification deferred** (rq_tools determines exact validation tools, planner just states requirement)
- **Error behavior documented** (quit immediately, log error, invoke g_debug)
- **Architecture enforcement** (downstream agents MUST comply or circuit breaker triggers)

---

## Template Structure Summary

### Complete File Structure

A well-formed 2_plan.md contains:

```markdown
# Analysis Plan for RQ X.Y: [RQ Title]

**Created by:** rq_planner agent
**Date:** YYYY-MM-DD
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

[1-2 paragraphs describing the analysis approach, how many steps, what the workflow accomplishes]

---

## Analysis Plan

### Step 1: [Step Name]

**Dependencies:** [None, or list of prior steps]
**Complexity:** [Low/Medium/High with runtime estimate]

**Input:**
[Input specifications - files, formats, columns, expected values]

**Processing:**
[What happens in this step - transformation/analysis/plotting]

**Output:**
[Output specifications - files, formats, columns, dimensions]

**Validation Requirement:**
Validation tools MUST be used after analysis tool execution. [Details about what gets validated]

**Expected Behavior on Validation Failure:**
[What happens if validation fails - error/log/quit/g_debug]

---

### Step 2: [Step Name]

[Same structure as Step 1]

---

[... continue for all N steps]

---

## Expected Data Formats

[Additional format details not covered in per-step Input/Output sections]

### Step-to-Step Transformations

[Document complex transformations: wide -> long, merging, stacking, etc.]

### Column Naming Conventions

[Reference names.md if populated, or document conventions used]

### Data Type Constraints

[Nullable vs non-nullable, valid ranges, categorical values, etc.]

---

## Cross-RQ Dependencies

[If applicable - document DERIVED data dependencies on other RQs]
[If not applicable - state "No dependencies - RAW data only from master.xlsx"]

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

[Global validation statement + per-step validation details]

---

## Summary

**Total Steps:** N
**Estimated Runtime:** [X minutes/hours based on complexity assessments]
**Cross-RQ Dependencies:** [None, or list of dependency RQs]
**Primary Outputs:** [List of key final outputs - theta scores, LMM results, plots, etc.]
**Validation Coverage:** 100% (all N steps have validation requirements)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan  ->  creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml  ->  creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml  ->  generates stepN_name.py scripts

---

**Version History:**
- v1.0 (YYYY-MM-DD): Initial plan created by rq_planner agent
```

### Section Order

The sections MUST appear in this order:
1. Overview (context for reader)
2. Analysis Plan (numbered steps - CORE section)
3. Expected Data Formats (additional format details)
4. Cross-RQ Dependencies (if applicable)
5. Validation Requirements (global + per-step)
6. Summary (recap of plan)

**Rationale for Order:**
- Overview first (orient reader to what plan accomplishes)
- Analysis Plan second (core content - step-by-step workflow)
- Data Formats third (supports Analysis Plan with additional detail)
- Dependencies fourth (execution order constraints)
- Validation fifth (reinforces requirements stated in Analysis Plan)
- Summary last (recap for quick reference)

---

## How rq_planner Uses This Template

### Agent Workflow (Step 9)

The rq_planner agent follows this process:

1. **Read** this template (docs/v4/templates/plan.md)
2. **Read** 1_concept.md (user's RQ description)
3. **Read** status.yaml (rq_concept, rq_scholar, rq_stats context dumps)
4. **Read** data_structure.md (understand master.xlsx tag system)
5. **Read** tool_inventory.md (understand available analysis tools)
6. **Read** project_specific_stats_insights.md (understand mandatory requirements like D039, D068, D069, D070)
7. **Read** names.md (check if naming conventions exist - TDD so likely empty for RQ 5.1)
8. **Ultrathink** analysis approach:
   - How many steps needed?
   - What transformations per step?
   - What tools per step (from tool_inventory.md)?
   - What validation per step (state requirement, let rq_tools specify tools)?
   - Any cross-RQ dependencies?
9. **Write** 2_plan.md following this template structure
10. **Update** status.yaml (rq_planner: success, context_dump)
11. **Report** to master: "Successfully created 2_plan.md for chX/rqY"

### What rq_planner Does NOT Do

- **Does NOT specify exact validation tools** (that's rq_tools job in Step 11)
- **Does NOT ask user questions** (v4.X planning is automated, not interactive like v3.0)
- **Does NOT generate code** (that's g_code job in Step 14)
- **Does NOT execute analysis** (that's bash execution in Step 14)

rq_planner creates the **plan** (specification), downstream agents execute it.

---

## Validation Checklist (For Template Verification)

When template is complete, verify:

- [ ] File exists at docs/v4/templates/plan.md
- [ ] Overview section explains 2_plan.md purpose and workflow context
- [ ] Section 1: Step-by-step analysis plan structure documented (numbered steps, dependencies, complexity)
- [ ] Section 2: Input specifications structure documented (file paths, formats, columns, data types, expected values)
- [ ] Section 3: Output specifications structure documented (file paths, formats, columns, dimensions, expected counts)
- [ ] Section 4: Expected data formats structure documented (transformations, naming conventions, constraints)
- [ ] Section 5: Cross-RQ dependencies structure documented (RAW vs DERIVED, execution order, circuit breakers)
- [ ] Section 6: Validation requirements structure documented (global mandate + per-step details)
- [ ] **CRITICAL:** Exact quote from spec present: "Validation tools MUST be used after analysis tool execution"
- [ ] Complete file structure example provided (shows all sections in correct order)
- [ ] rq_planner workflow documented (what agent does, what agent does NOT do)
- [ ] v3.0 vs v4.X differences explained (historical context, architectural rationale)
- [ ] Template is comprehensive (500-700 lines per user requirement)
- [ ] Generic examples only (no v3.0-specific examples per user requirement)
- [ ] Validation documented 4 ways per user requirement:
  - [ ] Global statement in header/intro (Section 6 global mandate)
  - [ ] Per-step reminder in structure (each step example shows validation)
  - [ ] Dedicated validation section (Section 6 entire section)
  - [ ] Exact quote from spec highlighted (line 1006 quote present multiple times)

---

## Version History

- **v4.0** (2025-11-16): Initial template created for v4.X architecture
  - Comprehensive structure (500-700 lines)
  - Generic examples (no v3.0-specific content)
  - Extensive validation documentation (4 approaches per user requirement)
  - Agent-to-agent specification format
  - Aligned with specification section 4.2.2

---

**End of Template Specification**
