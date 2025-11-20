# fit_lmm_with_tsvr Defensive Programming Enhancements

## Defensive Programming Added to fit_lmm_with_tsvr (2025-11-15 17:00)

**Context:** During resume script v5 debugging, discovered fit_lmm_with_tsvr() function had multiple API assumptions causing cascading errors. Added defensive programming to handle column naming variations.

**Archived from:** state.md Session (2025-11-15 17:00)
**Original Date:** 2025-11-15 17:00
**Reason:** v3.0 defensive programming approach, v4.X prevents need via validation gates, historical record

---

## Function Location

**File:** `tools/analysis_lmm.py`
**Function:** `fit_lmm_with_tsvr()`
**Purpose:** Fit Linear Mixed Model with TSVR (Time Since VR) as time variable per Decision D070

---

## Defensive Enhancements Added

### 1. test vs Test Auto-Detection (lines 903-907)

**Problem:** Function hardcoded `tsvr_data['test']` but input CSV has 'Test' (uppercase)

**Fix:**
```python
# Auto-detect test column (handles both 'test' and 'Test')
test_col = 'test' if 'test' in tsvr_data.columns else 'Test'
if test_col not in tsvr_data.columns:
    raise ValueError("tsvr_data missing both 'test' and 'Test' columns")
```

**Result:** Handles case sensitivity variations

---

### 2. Conditional composite_ID Creation for tsvr_data (lines 910-912)

**Problem:** Function assumed tsvr_data has composite_ID column, but data-prep output only has UID, Test, TSVR_hours

**Fix:**
```python
# Create composite_ID if not present
if 'composite_ID' not in tsvr_data.columns:
    tsvr_data['composite_ID'] = tsvr_data['UID'] + '_' + tsvr_data[test_col].astype(str)
```

**Result:** Function creates required merge key if missing

---

### 3. tsvr vs TSVR_hours Auto-Detection (lines 914-917)

**Problem:** Function expected 'tsvr' column but data-prep output has 'TSVR_hours'

**Fix:**
```python
# Auto-detect TSVR column (handles both 'tsvr' and 'TSVR_hours')
tsvr_col = 'tsvr' if 'tsvr' in tsvr_data.columns else 'TSVR_hours'
if tsvr_col not in tsvr_data.columns:
    raise ValueError("tsvr_data missing both 'tsvr' and 'TSVR_hours' columns")
tsvr_data['tsvr'] = tsvr_data[tsvr_col]  # Normalize to 'tsvr'
```

**Result:** Handles column naming variations, normalizes to standard name

---

## Files Modified

**Tool Functions:**
- `tools/analysis_lmm.py` (lines 903-917)
  - Line 903-907: test/Test auto-detection
  - Line 910-912: composite_ID conditional creation
  - Line 914-917: tsvr/TSVR_hours auto-detection

---

## Defensive Programming Philosophy

### What It Solves
- **Case sensitivity issues** - Handles test/Test variations
- **Missing columns** - Creates composite_ID if absent
- **Naming inconsistencies** - Handles tsvr/TSVR_hours variations

### What It Doesn't Solve
- **Root cause** - Agent still doesn't read tools_inventory.md
- **Wide vs long format** - Data structure mismatch requires reshaping, not auto-detection
- **Validation before execution** - Still discovers errors at runtime, not validation phase

---

## Limitations of Approach

### Band-Aid, Not Solution
- Defensive programming patches symptoms, not root cause
- Every function needs defensive code (increases complexity)
- New API mismatches require new defensive patches
- No systematic prevention

### Still Runtime Errors
- Errors discovered during execution (60-minute IRT calibration wasted)
- No pre-execution validation
- Cascading failures still possible (Error 6 - wide/long format)

---

## V4.X Prevention Strategy

### Instead of Defensive Programming
**v4.X uses validation gates (g_code agent):**

1. **Signature Enforcement** - Read tools_inventory.md, verify exact signatures
2. **Column Schema Validation** - Check expected columns BEFORE execution
3. **Format Validation** - Verify wide vs long format matches expectations
4. **Circuit Breakers** - QUIT on ANY mismatch, never guess

### Result
- **Zero defensive code needed** - Functions assume valid inputs (validated upstream)
- **Zero runtime errors** - All validation happens before 60-minute calibration
- **Systematic prevention** - Root cause (API ignorance) eliminated
- **Cleaner code** - Functions do their job, validation is separate concern

---

## Lessons Learned

1. **Defensive Programming Has Costs** - Increases complexity, doesn't solve root cause
2. **Runtime Error Discovery Is Expensive** - 60+ minutes wasted on IRT calibration
3. **Validation Gates Superior** - Catch errors before execution, not during
4. **API Documentation Must Be Enforced** - Reading tools_inventory.md prevents need for defensive code
5. **V4.X Design Is Correct** - Atomic agents + validation gates > monolithic agents + defensive programming

---

**Archive Entry Complete**
