# Data-Prep Agent Usage Guide

**Version:** 3.0
**Last Updated:** 2025-11-11
**Status:** PRODUCTION-READY (critical bug fix applied)

---

## Table of Contents

1. [Overview](#overview)
2. [When to Use Data-Prep Agent](#when-to-use-data-prep-agent)
3. [How to Invoke](#how-to-invoke)
4. [Input Specification](#input-specification)
5. [Expected Output](#expected-output)
6. [Workflow Examples](#workflow-examples)
7. [Troubleshooting](#troubleshooting)
8. [Testing Protocol](#testing-protocol)

---

## Overview

### What is the Data-Prep Agent?

The Data-Prep Agent is a specialized agent that autonomously prepares input data for research questions (RQs) by:
- Extracting tags from master.xlsx
- Computing derived scores (e.g., RAVLT_Total)
- Loading previous RQ outputs
- Validating data quality
- Saving prepared data to `results/chX/rqY/data/input.csv`

### Agent Characteristics

- **Stateless:** Each invocation is independent
- **Autonomous:** Executes full workflow without intermediate user input
- **Validated:** Always validates data before saving
- **Documented:** Returns detailed JSON report
- **Terminating:** Reports to master and quits (does NOT continue to analysis)

### Files & Documentation

| File | Purpose |
|------|---------|
| `.claude/agents/data_prep.md` | Agent prompt (comprehensive workflows with embedded tag system) |
| `data/README.md` | Data extraction API documentation (agent loads this) |
| `docs/data_structure.md` | Master.xlsx tag system (agent loads this) |
| `docs/cognitive_tests.md` | Cognitive test scoring (agent loads this) |
| `docs/data_prep_agent_guide.md` | This file - usage guide for master/user |

---

## When to Use Data-Prep Agent

### Use Cases

✅ **Use the agent when:**
- Starting a new RQ that needs data from master.xlsx
- Need to combine multiple data sources (tags + RQ outputs + computed scores)
- Want automated validation of extracted data
- Need documentation of data extraction process
- Working with VR data requiring wildcard patterns

❌ **Do NOT use the agent when:**
- RQ uses only previously prepared data (just copy/load existing file)
- Need exploratory data analysis before finalizing extraction
- Extraction logic is unclear or needs iteration
- User wants to manually inspect data during extraction

### Decision Tree

```
Does RQ need NEW data extraction from master.xlsx?
├─ YES → Does extraction logic require iteration/exploration?
│   ├─ YES → Manual extraction first, then document workflow
│   └─ NO → Use Data-Prep Agent ✅
└─ NO → Load existing data directly ⏩
```

---

## How to Invoke

### Method 1: Using Claude Code Task Tool (Recommended)

```python
Task(
    subagent_type="data_prep",
    description="Prepare data for RQ 5.1",
    prompt="Load the data-prep agent prompt and execute the workflow for RQ ch5/rq1. Read specification from results/ch5/rq1/info.md."
)
```

The agent will:
1. Load `.claude/agents/data_prep.md` automatically
2. Read RQ specification from `results/ch5/rq1/info.md`
3. Load required documentation (`data/README.md`, `docs/data_structure.md`, `docs/cognitive_tests.md`)
4. Execute extraction workflow
5. Return JSON report

---

## Input Specification

### Option 1: File-Based Specification (Preferred)

**Use when:** RQ already has an `info.md` file with requirements

**Agent reads:**
- `results/chX/rqY/info.md` - Parses Data Preparation section
- `results/chX/rqY/config.yaml` - Reads extraction parameters (if exists)

**What the agent does:**
1. Reads `results/ch5/rq1/info.md`
2. Parses requirements section
3. Identifies needed variables
4. Executes extraction
5. Validates data quality
6. Saves to `results/ch5/rq1/data/input.csv`

---

### Option 2: Inline Specification (Testing)

**Use when:** Testing or RQ doesn't have info.md yet

Provide detailed requirements in the Task prompt:

```
Extract the following data for RQ ch5/test_rq1:
- VR items: IFR paradigm, i1-i6, Name domain (-N-), all 4 test sessions
- Demographics: Age, Sex
- Cognitive: RAVLT_Total (computed from T1-T5)
- Expected shape: 400 rows × 9 cols
```

---

## Expected Output

### Success Report (status: "success")

```json
{
  "agent": "data-prep",
  "status": "success",
  "timestamp": "2025-11-11T10:30:00Z",
  "rq": "ch5/rq1",
  "files_created": [
    "results/ch5/rq1/data/input.csv",
    "results/ch5/rq1/logs/agent_data_prep.log"
  ],
  "variables_extracted": {
    "master_tags": ["Age", "Sex"],
    "computed_scores": ["RAVLT_Total"],
    "rq_outputs": [],
    "vr_tags": ["TQ-IFR-i1CM-N-ANS", "TQ-IFR-i2CM-N-ANS", ...]
  },
  "data_shape": {
    "rows": 400,
    "cols": 9,
    "description": "100 participants × 4 tests, 8 variables + UID"
  },
  "summary": "Extracted 6 IFR item scores + Age + Sex + RAVLT_Total. Data stacked in Composite_ID format for IRT calibration.",
  "validation": {
    "valid": true,
    "missing_data_pct": 1.8,
    "missing_by_column": {"RAVLT_T5": 7},
    "outliers_detected": 0,
    "checks_passed": 6,
    "checks_failed": 0,
    "warnings": ["RAVLT_T5 has 7 missing values (1.75%)"],
    "errors": []
  },
  "next_steps": "Ready for IRT calibration using deepirtools GRM",
  "error": null
}
```

### Warning Report (status: "warning")

```json
{
  "agent": "data-prep",
  "status": "warning",
  "summary": "Data extracted successfully but with warnings",
  "validation": {
    "valid": true,
    "warnings": [
      "NART_Score has 12 missing values (12%)",
      "Age has 2 outliers (> 3 SD from mean)"
    ]
  },
  "next_steps": "Review warnings and decide if acceptable. Consider imputation for NART_Score."
}
```

**Master agent should:**
1. Present warnings to user
2. Ask if acceptable to proceed
3. If yes → Continue to analysis step
4. If no → Investigate/fix data issues

### Failure Report (status: "failure")

```json
{
  "agent": "data-prep",
  "status": "failure",
  "error": {
    "type": "TagNotFoundError",
    "message": "Tag pattern '{UID}-COG-X-INVALID' not found in master.xlsx"
  },
  "next_steps": "Check tag name in docs/cognitive_tests.md or docs/data_structure.md. Correct tag pattern and retry."
}
```

**Master agent should:**
1. Present error to user
2. Suggest troubleshooting steps
3. DO NOT continue to analysis
4. Fix issue and re-invoke agent

---

## Workflow Examples

### Example 1: Simple Demographics RQ

**Scenario:** RQ needs Age, Sex, Education

**Master invokes:**
```python
Task(subagent_type="data_prep", prompt="Extract Age, Sex, Education for ch5/test_rq1. Expected: 100 rows × 4 cols.")
```

**Output:**
- `input.csv` with 100 rows × 4 cols (UID + Age + Sex + Education)
- Validation: All passed
- Next steps: Ready for analysis

---

### Example 2: VR Data for IRT

**Scenario:** RQ needs IFR items across all tests for IRT calibration

**Master invokes:**
```python
Task(subagent_type="data_prep", prompt="Extract IFR items (i1-i6) for Name domain across all 4 test sessions for ch5/rq1. Stack in Composite_ID format. Expected: 400 rows.")
```

**Output:**
- `input.csv` with 400 rows × 7 cols (UID + 6 items)
- Stacked format: 100 participants × 4 tests
- Ready for IRT calibration

---

### Example 3: Mixed Sources

**Scenario:** RQ needs VR data + demographics + cognitive scores + previous RQ theta

**Master invokes:**
```python
Task(subagent_type="data_prep", prompt="Extract for ch5/rq2: Load theta scores from ch5/rq1, extract Age, compute RAVLT_Total, merge all sources. Expected: 400 rows × 10 cols.")
```

**Output:**
- `input.csv` with 400 rows × 10 cols
- Combined: theta from RQ1 + Age + RAVLT_Total
- All sources merged on UID
- Ready for LMM analysis

---

## Troubleshooting

### Common Issues

#### Issue 1: Tag Not Found

**Error:**
```
TagNotFoundError: Tag pattern '{UID}-COG-X-INVALID' not found
```

**Causes:**
- Typo in tag pattern
- Using underscores instead of dashes
- Wrong tag name (check docs)

**Solutions:**
1. Check `docs/cognitive_tests.md` for exact tag names
2. Check `docs/data_structure.md` for tag patterns
3. Verify dashes throughout (NOT underscores)
4. Note truncated names (e.g., "Scor" not "Score")

---

#### Issue 2: Validation Failed (Wrong Dimensions)

**Error:**
```
ValidationError: Expected 400 rows, got 100
```

**Causes:**
- Forgot to use `test_wildcard='all'` (got 1 test instead of 4)
- Wrong expected dimensions in specification

**Solutions:**
1. If need all 4 tests: Set `test_wildcard='all'`
2. If need 1 test only: Set `test_wildcard='T0'` (or T1, T3, T6)
3. Verify expected_shape matches extraction logic

---

#### Issue 3: Excessive Missing Data

**Warning:**
```
NART_Score has 15 missing values (15%)
```

**Causes:**
- Genuine data quality issue (some participants didn't complete NART)
- Tag extraction error

**Solutions:**
1. Check if missing data is expected (e.g., NART has known missing data)
2. Set `missing_rules={'NART_Score': 15}` if acceptable
3. If NOT acceptable: Investigate master.xlsx data quality
4. Consider imputation strategies

---

#### Issue 4: Wrong Item Codes (CRITICAL)

**Error:**
```
ValidationError: 132 columns are 100% empty
```

**Cause:** Using wrong item codes (e.g., `i5IC` instead of `i5IN`)

**Solution:**
- Agent v3.0 has embedded tag system reference to prevent this
- If still occurs: Check item codes in agent output, compare to `docs/data_structure.md`
- Correct codes: i1CM, i2CM, i3CG, i4CG, **i5IN**, **i6IN** (NOT i5IC/i6IC!)

---

## Testing Protocol

### Phase 6: Agent Testing (Completed)

**Test Cases:**

#### Test RQ 1: Simple Demographics
- Extract Age, Sex, Education
- Expected: 100 rows × 4 cols
- Result: ✅ PASSED

#### Test RQ 2: VR Data (IRT Format)
- Extract IFR items across all tests
- Expected: 400 rows × 7 cols
- Result: ✅ PASSED (after v3.0 bug fix)

#### Test RQ 3: Mixed Sources
- Extract VR + demographics + cognitive + RQ output
- Expected: 400 rows × 10 cols
- Result: ✅ PASSED

### Version History

**v3.0 (2025-11-08) - CRITICAL BUG FIX:**
- ✅ Embedded 150-line tag system reference directly in agent prompt
- ✅ Added validation rule: 100% empty columns = ERROR
- ✅ Fixed item codes (i5IN not i5IC, i6IN not i6IC)
- ✅ Added paradigm-specific domain availability table
- ✅ **Impact:** Prevented corruption of all 50 RQs

**v2.0 (2025-11-05):**
- Initial production release
- ⚠️ **SUPERSEDED** - Had critical validation failure (accepted 73% empty data as "normal")

---

## Master Agent Responsibilities

**When invoking data-prep agent:**

1. **Before invocation:**
   - Verify RQ folder exists (`results/chX/rqY/`)
   - Verify data/ subfolder exists
   - Prepare input specification (preferably in info.md)

2. **During invocation:**
   - Monitor agent execution (no intervention needed)
   - Log agent actions

3. **After invocation:**
   - Read JSON report
   - Parse status (success/warning/failure)
   - IF success → Continue to analysis step
   - IF warning → Present to user, get approval
   - IF failure → Present error, troubleshoot, retry

4. **Always:**
   - Update `results/chX/rqY/status.json`
   - Log agent report to `results/chX/rqY/logs/agent_data_prep.log`

---

## References

**Agent Prompt:** `.claude/agents/data_prep.md`
**Tool Reference:** `docs/tools_inventory.md`
**Agents Overview:** `docs/agents_overview.md`
**Data Structure:** `docs/data_structure.md`
**Cognitive Tests:** `docs/cognitive_tests.md`

---

**End of Data-Prep Agent Usage Guide**
