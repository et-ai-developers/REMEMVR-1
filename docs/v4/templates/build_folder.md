# RQ Folder Structure Specification

**Last Updated:** 2025-11-16
**Version:** 4.0
**Purpose:** Defines the mandatory folder structure for all v4.X research questions
**Audience:** rq_builder agent when creating new RQ directories

---

## How to Use This Template

This template specifies the **exact folder structure** that rq_builder agent must create for every new research question. The rq_builder agent reads this template and implements the structure according to these specifications.

**Agent Implementation (rq_builder agent):**
- Reads this template in Step 2
- Creates root folder in Step 4
- Creates all 6 subfolders in Step 5 according to these specifications
- Verifies structure correctness before reporting success

---

## Folder Names (6 Required)

The following 6 folders MUST be created inside `results/chX/rqY/`:

1. **docs/**
2. **data/**
3. **code/**
4. **logs/**
5. **plots/**
6. **results/**

**Root Path Format:**
- `results/chX/rqY/` where:
  - `chX` = chapter number (ch5, ch6, or ch7)
  - `rqY` = research question number (rq1-rq15 for ch5/ch6, rq1-rq20 for ch7)

**Example:** `results/ch5/rq1/`

---

## Creation Order

**Step 1: Create Root Folder**
- Create `results/chX/rqY/` directory
- If directory already exists, verify it is EMPTY (see Verification Steps below)
- Root folder MUST exist before creating subfolders

**Step 2: Create Subfolders**
- Create all 6 subfolders inside `results/chX/rqY/`
- Subfolders can be created in any order (no dependencies between them)
- All 6 subfolders MUST be created (none are optional)

**Recommended Implementation:**
Create in this sequence for clarity:
1. `results/chX/rqY/docs/`
2. `results/chX/rqY/data/`
3. `results/chX/rqY/code/`
4. `results/chX/rqY/logs/`
5. `results/chX/rqY/plots/`
6. `results/chX/rqY/results/`

**Note:** The sequence above is recommended for logical grouping (specifications → outputs → summaries), but agents may create folders in any order as they are independent.

---

## Verification Steps

**Before Creating Folders:**

1. **Check if root folder exists:**
   - If `results/chX/rqY/` does NOT exist → Create it
   - If `results/chX/rqY/` DOES exist → Proceed to step 2

2. **Verify root folder is empty (if it exists):**
   - Check `results/chX/rqY/` contains NO files and NO subdirectories
   - **Why:** Ensures we're starting fresh and not overwriting existing RQ work
   - **If not empty:** FAIL and report error - do NOT overwrite existing work

3. **After creating all 6 subfolders:**
   - Verify all 6 folders exist inside `results/chX/rqY/`
   - Verify each subfolder is empty (ready to receive files from subsequent agents)

**Verification Commands (Bash examples for reference):**
```bash
# Check if root exists and is empty
ls -la results/chX/rqY/

# After creation, verify all 6 folders exist
ls -la results/chX/rqY/ | grep -E "docs|data|code|logs|plots|results"
```

**Expected Result:**
```
results/chX/rqY/
  docs/      (empty)
  data/      (empty)
  code/      (empty)
  logs/      (empty)
  plots/     (empty)
  results/   (empty)
```

---

## Folder Purposes (One-Line Summary)

1. **docs/** - RQ specifications and planning documents
2. **data/** - Analysis step outputs (CSV files)
3. **code/** - Generated Python scripts
4. **logs/** - Execution logs
5. **plots/** - Visualizations (scripts and images)
6. **results/** - Final summaries and interpretations

---

**End of Template Specification**
