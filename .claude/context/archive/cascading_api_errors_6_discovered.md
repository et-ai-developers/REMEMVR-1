# Cascading API Errors - 6 Discovered Sequentially

## Sequential Error Discovery During Resume Script v5 Execution (2025-11-15 17:00)

**Context:** While creating and testing resume script v5, discovered 6 cascading API errors in sequence. Each error only appeared after fixing previous error. Demonstrates Pattern 2 (Cascading Failures) from 24-problem list.

**Archived from:** state.md Session (2025-11-15 17:00)
**Original Date:** 2025-11-15 17:00
**Reason:** v3.0 cascading errors documented, v4.X validation gates prevent this pattern, historical record

---

## Error 1: Unicode Arrow (Step 5 line 462)

**Error:** `UnicodeEncodeError: 'charmap' codec can't encode character '\u2192'`
**Cause:** Script used Unicode arrow (→) in print statements for "wide → long"
**Location:** `print("\n[4/5] Reshaping wide → long format...")`
**Fix:** `sed -i 's/→/->/g'` replaced all 5 Unicode arrows with ASCII equivalents
**Files Changed:** `analysis_script_resume_from_step5.py`

**Pattern:** Platform Assumptions (Problem #16) - Agent generates UTF-8 code, breaks on Windows cp1252

---

## Error 2: Missing composite_ID Creation (Step 5 line 230)

**Error:** `KeyError: "None of [Index(['composite_ID'], dtype='object')] are in the [columns]"`
**Cause:** df_merged expected composite_ID column but theta_scores.csv has UID, test (no composite_ID)
**Root Issue:** Script used composite_ID without creating it first
**Fix:** Added `df_theta_scores['composite_ID'] = df_theta_scores['UID'] + '_' + df_theta_scores['Test'].astype(str)`
**Files Changed:** `analysis_script_resume_from_step5.py:206`

**Pattern:** API Documentation Ignorance (Problem #6) - Agent guesses data structure instead of reading IRT output schema

---

## Error 3: test vs Test Case Mismatch (fit_lmm_with_tsvr line 903)

**Error:** `KeyError: 'test'` in fit_lmm_with_tsvr function
**Cause:** Function hardcoded `tsvr_data['test']` but tsvr_data.csv has 'Test' (uppercase)
**Location:** `tools/analysis_lmm.py:903`
**Fix:** Added auto-detection `test_col = 'test' if 'test' in tsvr_data.columns else 'Test'`
**Files Changed:** `tools/analysis_lmm.py:903-907`

**Pattern:** Case Sensitivity Issues (Problem #10) - Inconsistent capitalization between CSV outputs and function expectations

---

## Error 4: Missing composite_ID in tsvr_data (fit_lmm_with_tsvr line 917)

**Error:** `KeyError: "None of [Index(['composite_ID', 'tsvr'], dtype='object')] are in the [columns]"`
**Cause:** Function expected tsvr_data to have composite_ID but it only has UID, Test, TSVR_hours
**Root Issue:** Function assumed composite_ID exists instead of creating it
**Fix:** Added conditional creation:
```python
if 'composite_ID' not in tsvr_data.columns:
    tsvr_data['composite_ID'] = tsvr_data['UID'] + '_' + tsvr_data['Test']
```
**Files Changed:** `tools/analysis_lmm.py:910-912`

**Pattern:** Missing Column Handling (Problem #11) - Function expects columns without defensive checks

---

## Error 5: tsvr vs TSVR_hours Column Name (fit_lmm_with_tsvr line 917)

**Error:** Same KeyError as Error 4 but for 'tsvr' column
**Cause:** Function expected 'tsvr' but tsvr_data.csv has 'TSVR_hours'
**Fix:** Added auto-detection:
```python
tsvr_col = 'tsvr' if 'tsvr' in tsvr_data.columns else 'TSVR_hours'
tsvr_data['tsvr'] = tsvr_data[tsvr_col]
```
**Files Changed:** `tools/analysis_lmm.py:914-917`

**Pattern:** Naming Inconsistency (Problem #17) - Column name mismatch between data prep output and LMM function input

---

## Error 6: Wide vs Long Format (fit_lmm_with_tsvr expects long, receives wide)

**Error:** `KeyError: "['Theta'] not in index"` + "WARNING: 400 rows missing TSVR data (100.0%)"
**Cause:** fit_lmm_with_tsvr expects theta_scores in LONG format (composite_ID, Domain, Theta) but receives WIDE format (UID, test, Theta_What, Theta_Where, Theta_When)
**Root Issue:** No data reshaping between IRT Pass 2 output (wide) and LMM input (long)
**Status:** ERROR DISCOVERED but NOT YET FIXED (script crashed at this point)
**Impact:** 100% merge failure, catastrophic data loss

**Pattern:** Wide vs Long Format Mismatch (Problem #12) - Architectural data structure incompatibility between pipeline steps

---

## Cascading Pattern Analysis

### Discovery Sequence
1. Fix Error 1 (Unicode) → Reveals Error 2
2. Fix Error 2 (composite_ID creation) → Reveals Error 3
3. Fix Error 3 (test/Test) → Reveals Error 4
4. Fix Error 4 (tsvr composite_ID) → Reveals Error 5
5. Fix Error 5 (tsvr/TSVR_hours) → Reveals Error 6
6. Error 6 (wide/long) → CATASTROPHIC, script stops

### Root Cause
**Single architectural decision:** analysis-executor doesn't read tools_inventory.md before generating function calls
**Result:** 1 root error → 6 downstream failures discovered sequentially
**Time Cost:** 60+ minutes debugging, script still not working

### Why Cascading?
- **No validation layer** between script generation and execution
- **Monolithic design** means errors only discovered at runtime
- **Sequential dependencies** mean Error N+1 hidden until Error N fixed
- **API ignorance** means every function call is a potential failure point

---

## Defensive Programming Added

### fit_lmm_with_tsvr Enhancements
1. **test vs Test auto-detection** (lines 903-907)
2. **Conditional composite_ID creation for tsvr_data** (lines 910-912)
3. **tsvr vs TSVR_hours auto-detection** (lines 914-917)

**Result:** Function now robust to column naming variations
**Limitation:** Doesn't solve root cause (API documentation ignorance)

---

## Lessons Learned

1. **Cascading Errors Are Predictable** - Static analysis could catch all 6 errors before runtime
2. **Defensive Programming Is Band-Aid** - Auto-detection helps but doesn't solve architecture
3. **Monolithic Design Amplifies Impact** - Single script means cascading failures block all work
4. **Validation Gates Are Critical** - v4.X multi-layer validation prevents this pattern
5. **API Documentation Must Be Enforced** - v4.X forces agents to read tools_inventory.md

---

## V4.X Prevention Strategy

### Multi-Layer Validation (g_code agent)
1. **Import check** - Verify all imports exist
2. **Signature check** - Verify function signatures match tools_inventory.md
3. **Input file check** - Verify input files exist and have expected structure
4. **Column check** - Verify expected columns present in DataFrames
5. **QUIT on ANY failure** - Never guess, always circuit-break

### Result
- Catches Error 1 (encoding rule violation)
- Catches Error 2-6 (column mismatch before execution)
- Zero runtime errors, all failures at validation phase
- No cascading (all errors reported simultaneously)

---

**Archive Entry Complete**
