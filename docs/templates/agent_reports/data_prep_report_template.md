# Data Preparation Report

**RQ:** X.Y - [RQ Title]
**Execution Date:** YYYY-MM-DD HH:MM
**Agent:** data_prep v3.0
**Report Version:** 1.0

---

## Executive Summary

**Status:** ✅ SUCCESS / ❌ FAILURE

**Files Created:** [N] files (X CSVs + X companion .md + script)

**Execution Time:** [X minutes Y seconds]

**Data Quality:** ✅ PASS / ⚠️ WARNING / ❌ FAIL

---

## Execution Context

**Input Documents Read:**
- ✅ info.md (Section 3: Input Data)
- ✅ config.yaml (Not applicable - data-prep doesn't use config.yaml)
- ✅ master.xlsx (data source)

**Working Directory:** `results/chX/rqY/`

---

## Data Extraction Plan

### Variables Extracted

| **Variable** | **Tags in master.xlsx** | **Type** | **Expected N** |
|-------------|------------------------|----------|---------------|
| UID | UID | string | 400 |
| Test | Test | int | 400 |
| VR_Person_T1 | RVR-i1PO-T1, ..., RVR-i9PO-T1 | binary | 400 |
| VR_Place_T1 | RVR-i10PL-T1, ..., RVR-i18PL-T1 | binary | 400 |
| VR_Object_T1 | RVR-i19OB-T1, ..., RVR-i27OB-T1 | binary | 400 |
| [Repeat for T2, T3, T4] | | | |

**Total Variables:** [N]

**Total Tags:** [N] (from docs/data_structure.md tag system)

---

### Filters Applied

**Participant-Level Filters:**
- Exclude participants with <3 test sessions
- Result: [N] participants excluded, [N] retained

**Item-Level Filters:**
- Exclude items with >70% missing values across all participants
- Result: [N] items excluded, [N] retained

**Value-Level Filters:**
- Convert missing values to 0 (incorrect)
- Dichotomous coding: 1=correct, 0=incorrect/missing

---

### Expected Output Dimensions

**File:** data/irt_input.csv

**Expected Dimensions:**
- Rows: 400 (100 participants × 4 tests)
- Columns: 37 (UID + Test + 27 VR items + 8 covariates)

**Expected File Size:** ~25-35 KB

---

## Execution Steps

### Step 1: Load master.xlsx

**Action:** Read master.xlsx using `tools.data.load_master_data()`

**Result:** ✅ SUCCESS / ❌ FAILURE

**Details:**
- File path: `data/master.xlsx`
- Rows loaded: [N]
- Columns loaded: [N]
- Load time: [X seconds]

**Issues:** [None / List any warnings]

---

### Step 2: Extract Variables by Tags

**Action:** Extract variables using exact tags from info.md Section 3

**Tags Used:** [List all tags]

**Result:** ✅ SUCCESS / ❌ FAILURE

**Details:**
- Tags found: [N] / [N] ([X]%)
- Tags missing: [N] (if any, list them)
- Extraction method: `tools.data.extract_by_tags()`

**Tag Validation:**
- ✅ All tags follow format `RVR-{item_code}-T{test}`
- ✅ Item codes validated against docs/data_structure.md
- ✅ Test codes validated (T1, T2, T3, T4)

**Issues:** [None / List any missing tags or format errors]

---

### Step 3: Apply Filters

**Participant Filter:**
- **Criterion:** Participants with ≥3 test sessions
- **Before:** [N] participants
- **After:** [N] participants
- **Excluded:** [N] participants ([list UIDs if <10])

**Item Filter:**
- **Criterion:** Items with ≤70% missing values
- **Before:** [N] items
- **After:** [N] items
- **Excluded:** [N] items ([list item codes])

**Value Coding:**
- **Criterion:** 1=correct, 0=incorrect/missing
- **Missing values converted:** [N]
- **Already coded:** [N]

**Result:** ✅ SUCCESS / ❌ FAILURE

**Issues:** [None / List any concerns]

---

### Step 4: Validate Data Quality

**Quality Checks:**

| **Check** | **Threshold** | **Actual** | **Status** |
|-----------|--------------|-----------|-----------|
| Missing Values | <30% per column | [X]% | ✅ PASS / ❌ FAIL |
| Empty Columns | 0 columns | [N] columns | ✅ PASS / ❌ FAIL |
| Duplicate Rows | 0 duplicates | [N] duplicates | ✅ PASS / ❌ FAIL |
| Dimension Match | 400 rows × 37 cols | [N] rows × [N] cols | ✅ PASS / ❌ FAIL |
| UID Format | PXX_YY pattern | [X]% match | ✅ PASS / ❌ FAIL |
| Test Values | 1, 2, 3, 4 only | [X]% valid | ✅ PASS / ❌ FAIL |

**Overall Data Quality:** ✅ PASS / ⚠️ WARNING / ❌ FAIL

**Issues:** [None / List any quality concerns]

---

### Step 5: Save Output Files

**Files Created:**

**1. data/irt_input.csv**
- **Status:** ✅ CREATED / ❌ FAILED
- **Size:** [N] KB ([Expected: 25-35 KB])
- **Dimensions:** [N] rows × [N] columns
- **MD5 Hash:** [hash for reproducibility verification]

**2. data/irt_input.md**
- **Status:** ✅ CREATED / ❌ FAILED
- **Size:** [N] KB
- **Sections:** Data Structure, Methodology, Quality Summary, Next Steps, Critical Insights, Example Code
- **Keywords Check:** ❌ NO "mock", "placeholder", "temporary" found ✅

**3. code/data_prep_script.py**
- **Status:** ✅ CREATED / ❌ FAILED
- **Size:** [N] lines
- **Purpose:** Reproducible extraction script
- **Execution:** `poetry run python code/data_prep_script.py` (should recreate irt_input.csv)

**Result:** ✅ SUCCESS / ❌ FAILURE

---

## Safety Verification (CRITICAL)

### Mock Data Generation Check

**Question:** Did this agent generate any mock, fake, or placeholder data?

**Answer:** ❌ NO (REQUIRED - if YES, CATASTROPHIC FAILURE)

**Verification:**
1. ✅ All data extracted from master.xlsx (no calculations, no transformations except dichotomous coding)
2. ✅ No theta scores created (IRT outputs - analysis-executor creates these)
3. ✅ No LMM input created (derived from theta scores - analysis-executor creates this)
4. ✅ No item parameters created (IRT outputs - analysis-executor creates these)
5. ✅ Companion .md files contain NO keywords: "mock", "placeholder", "temporary", "fake", "simulated", "proxy"

**Prohibited Files Check:**
- ❌ theta_scores.csv does NOT exist ✅
- ❌ item_parameters.csv does NOT exist ✅
- ❌ lmm_input.csv does NOT exist (if RQ requires RAW lmm_input from master.xlsx, OK to create) ✅
- ❌ Any file with "mock" or "temp" in name does NOT exist ✅

**Result:** ✅ SAFE (no mock data) / ❌ CONTAMINATED (mock data detected)

---

## Data Summary

### Descriptive Statistics

**File:** data/irt_input.csv

**Participant Statistics:**
- Total participants: [N]
- Total observations: [N] (participants × tests)
- Tests per participant: Mean=[X], SD=[X], Range=[min-max]

**Item Statistics:**

| **Domain** | **Items** | **Mean Accuracy** | **SD** | **Range** |
|-----------|----------|------------------|--------|-----------|
| Person | 9 | [X]% | [X]% | [min-max]% |
| Place | 9 | [X]% | [X]% | [min-max]% |
| Object | 9 | [X]% | [X]% | [min-max]% |

**Missing Data:**
- Total missing values: [N] ([X]%)
- Columns with >10% missing: [N] (if any, list them)
- Patterns: [Random / Systematic - describe if systematic]

---

### Critical Insights

**Observation 1:** [Notable pattern in data]
- **Details:** [What was observed]
- **Implication:** [What this means for analysis]

**Observation 2:** [Notable pattern in data]
- **Details:** [What was observed]
- **Implication:** [What this means for analysis]

**Concerns:** [Any data quality issues that might affect analysis]

---

## Next Steps for Analysis-Executor

**Input File Ready:** data/irt_input.csv

**Recommended Actions:**
1. **Step 1:** Run IRT calibration using `tools.analysis_irt.calibrate_grm()`
   - Input: data/irt_input.csv
   - Config: config.yaml (irt section)
   - Expected outputs: item_parameters.csv, theta_scores.csv

2. **Step 2:** Validate IRT assumptions
   - Local independence (Q3 statistic)
   - Unidimensionality (eigenvalue ratio)
   - Model fit (M2, RMSEA, CFI)

3. **Step 3:** If IRT successful, reshape theta scores for LMM
   - Input: theta_scores.csv
   - Output: lmm_input.csv

**Warnings:**
- [Any data quality issues analysis-executor should be aware of]

---

## Failure Report (If Status = FAILURE)

[Only include this section if execution failed]

**Error Type:** [MissingData / CoreDocumentationBug / MissingTool / UnexpectedError]

**Error Message:** [Full error message]

**Failure Location:** [Which step failed]

**Root Cause:** [Analysis of what went wrong]

**Required Action:** [What needs to be fixed before re-running]

**Missing Data Details (if MissingData error):**
- **Missing Variables:** [List]
- **Required For:** [What analysis step needs these]
- **Data Source Expected:** [Where agent thought data would come from]
- **Why Missing:** [Explanation]
- **Fix Required:** [Update info.md to clarify data sources OR wait for prerequisite RQ to complete]

---

## Execution Metadata

**Agent Version:** data_prep v3.0 (with mock data prevention safety rules)
**Invocation Command:** [How agent was invoked]
**Execution Start:** YYYY-MM-DD HH:MM:SS
**Execution End:** YYYY-MM-DD HH:MM:SS
**Total Duration:** [X minutes Y seconds]
**Python Version:** [X.Y.Z]
**Poetry Environment:** [Environment name]
**Tools Package Version:** [X.Y.Z]

---

**End of Data Preparation Report**
