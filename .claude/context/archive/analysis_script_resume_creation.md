# Analysis Script Resume Creation

**Topic:** Created resume script to skip completed Pass 1 IRT calibration
**Status:** Archived from state.md
**Related Files:** results/ch5/rq1/code/analysis_script_resume_v2.py

---

## Resume Script Creation (2025-11-14 23:40)

**Archived from:** state.md Session (2025-11-14 23:40)
**Original Date:** 2025-11-14
**Reason:** Resume script created and ready to use

### Context

After successfully completing IRT Pass 1 (60 minutes), created resume script to continue from Step 2 without re-running completed calibration.

---

## Resume Script Details

**File:** `results/ch5/rq1/code/analysis_script_resume_v2.py`

**Purpose:** Load Pass 1 outputs from CSV and continue execution from Step 2

**Skips:**
- Step 1: IRT Pass 1 calibration (saves ~60 minutes)

**Runs:**
- Steps 2-9: Item purification, Pass 2 calibration, theta extraction, TSVR merge, LMM, post-hoc, effect sizes, plotting

**Time Savings:** ~60 minutes per test run

---

## Implementation

**Pass 1 Outputs Loaded from CSV:**
1. `pass1_theta.csv` → df_theta_pass1
2. `pass1_item_params.csv` → df_item_params_pass1

**Execution Continues:** From Step 2 (Item Purification using purify_items())

---

## Files Created

1. `results/ch5/rq1/code/analysis_script_resume_v2.py` - Resume script

---

**End of Entry**
