# V4.X Validation Tools Migration Audit

**Task:** V1 - Phase 4 Validation Tools Migration
**Created:** 2025-11-17
**Purpose:** Inventory existing v3 validation capabilities and design v4.X migration strategy
**Status:** Complete

---

## Executive Summary

**v3 Validation Foundation:** 14 production-ready functions in `tools/validation.py` with 49/49 tests passing. Covers lineage tracking, IRT validation, LMM validation, and general data validation.

**v4.X Enhancements Needed:**
1. Add standardized `validation_passed` field to all validation tools (hybrid interface)
2. Change error reporting from dict-return to exception-with-dict pattern
3. Build 4 new plotting validation functions (D069 dual-scale, DPI, content, existing checks)
4. Defer CTT validation until RQ 5.1 testing reveals need (TDD approach)

**Migration Strategy:** Port existing 14 functions with interface enhancements (V2a-V2b), build new plotting validation (V2d), skip CTT unless needed (V2c deferred).

---

## 1. Existing v3 Validation Tools

**Location:** `tools/validation.py` (650 lines)
**Tests:** `tests/test_validation.py` (362 lines, 49/49 passing)
**Status:** Production-ready (used in RQ 5.1 v3.0 attempts)

### 1.1 Data Lineage Tracking (4 functions)

**Purpose:** Prevent critical errors like using Pass 1 data for Pass 2 plots (RQ 5.1 v3.0 failure)

| Function | What It Validates | Returns | Test Coverage |
|----------|-------------------|---------|---------------|
| `create_lineage_metadata(source_file, output_file, operation, parameters, description)` | N/A (creates metadata) | `dict` with source/output/operation/timestamp | ✅ test_create_lineage_metadata |
| `save_lineage(metadata, lineage_file)` | N/A (saves to JSON) | None | ✅ test_save_and_load_lineage |
| `load_lineage(lineage_file)` | N/A (loads from JSON) | `dict` | ✅ test_save_and_load_lineage |
| `validate_lineage(lineage_file, expected_source, expected_pass)` | Data comes from expected source file and pass number | `{"valid": bool, "message": str, "metadata": dict}` | ✅ test_validate_lineage |

**Key Features:**
- Tracks complete data provenance (source → operation → output)
- Validates expected source (partial string match)
- Validates expected pass number (1 or 2)
- JSON storage for human inspection

**v4.X Migration:** Port as-is, add `validation_passed` field, convert to exception pattern

---

### 1.2 IRT Validation (3 functions)

**Purpose:** Validate IRT model quality per Decision D039 (2-pass purification methodology)

| Function | What It Validates | Returns | Test Coverage |
|----------|-------------------|---------|---------------|
| `validate_irt_convergence(results)` | Model converged flag, final loss, epochs | `{"converged": bool, "message": str, "final_loss": float, "epochs_run": int}` | ✅ test_validate_irt_convergence |
| `validate_irt_parameters(df_items, a_min=0.4, b_max=3.0, a_col="a", b_col="b")` | Discrimination ≥ a_min, \|Difficulty\| ≤ b_max | `{"valid": bool, "n_flagged": int, "flagged_items": list, "total_items": int}` | ✅ test_validate_irt_parameters |
| `check_missing_data(df)` | Missing values in DataFrame | `{"has_missing": bool, "total_missing": int, "percent_missing": float, "missing_by_column": dict}` | ✅ test_check_missing_data |

**Key Features:**
- Convergence: Checks `model_converged` flag from deepirtools
- Parameters: Flags items failing D039 thresholds (a<0.4 or \|b\|>3.0)
- Missing data: Column-by-column breakdown with percentages

**v4.X Migration:** Port as-is, add `validation_passed` field, convert to exception pattern

---

### 1.3 LMM Validation (2 functions)

**Purpose:** Validate LMM assumptions and convergence

| Function | What It Validates | Returns | Test Coverage |
|----------|-------------------|---------|---------------|
| `validate_lmm_convergence(lmm_result)` | Model converged attribute from statsmodels | `{"converged": bool, "message": str}` | ✅ test_validate_lmm_convergence |
| `validate_lmm_residuals(residuals, alpha=0.05)` | Residual normality (Shapiro-Wilk if n<5000, KS if n≥5000) | `{"n_residuals": int, "normality_test": {"passed": bool, "p_value": float, ...}, "residual_stats": {...}}` | ✅ test_validate_lmm_residuals |

**Key Features:**
- Convergence: Checks `converged` attribute from `MixedLMResults`
- Residuals: Adaptive test selection based on sample size
- Residual stats: Mean, std, min, max for diagnostic purposes

**v4.X Migration:** Port as-is, add `validation_passed` field, convert to exception pattern

---

### 1.4 General Validation (3 functions)

**Purpose:** Common validation checks reusable across analysis types

| Function | What It Validates | Returns | Test Coverage |
|----------|-------------------|---------|---------------|
| `validate_data_columns(df, required_columns)` | Required columns exist in DataFrame | `{"valid": bool, "missing_columns": list, "existing_columns": list, "n_required": int, "n_missing": int}` | ✅ test_validate_data_columns |
| `validate_file_exists(file_path)` | File exists at path | `{"exists": bool, "file_path": str, "message": str}` | ✅ test_validate_file_exists |
| `validate_numeric_range(data, min_val, max_val, column_name)` | Numeric data within expected range | `{"valid": bool, "n_out_of_range": int, "total_values": int, "data_min": float, "data_max": float}` | ✅ test_validate_numeric_range |

**Key Features:**
- Columns: Set-based difference detection (handles extra columns gracefully)
- File: Uses Path.exists() with full path in response
- Range: Optional min/max bounds, reports actual data range

**v4.X Migration:** Port as-is, add `validation_passed` field, convert to exception pattern

---

### 1.5 Validation Reporting (2 functions)

**Purpose:** Aggregate multiple validation checks into comprehensive reports

| Function | What It Validates | Returns | Test Coverage |
|----------|-------------------|---------|---------------|
| `generate_validation_report(validation_checks, report_title)` | Aggregates multiple checks, determines overall status | `{"report_title": str, "timestamp": str, "overall_status": "PASSED"\|"FAILED", "n_checks": int, "checks": dict}` | ✅ test_generate_validation_report |
| `save_validation_report(report, report_file)` | N/A (saves to JSON) | None | ✅ test_save_validation_report |

**Key Features:**
- Overall status: Checks `valid`, `converged`, `has_missing` fields across all checks
- JSON storage: Full report saved for audit trail
- Timestamp: ISO format for chronological tracking

**v4.X Migration:** Port as-is, add `validation_passed` field to report, keep exception pattern for component checks

---

## 2. Gaps Identified

### 2.1 CTT Validation - DEFERRED

**User Decision:** Build only if RQ 5.1 testing reveals need (TDD approach)

**Rationale:**
- No CTT analysis tools in v3 `tools_inventory.md`
- No CTT-based RQs identified in thesis chapters 5-7
- If needed during RQ 5.1 execution, build then with TDD

**Potential Functions (if needed):**
- `validate_cronbach_alpha()` - Reliability coefficient
- `validate_item_total_correlation()` - Item-scale correlation
- `validate_sample_size_adequacy()` - Minimum n for reliability

**Task V2c Status:** Pending (will mark as "not needed" or build during RQ 5.1)

---

### 2.2 Plotting Validation - BUILD NEW

**User Decision:** Build 4 categories of plotting validation

**Existing Coverage:**
- ✅ Lineage tracking (via `validate_lineage()`)
- ✅ File existence (via `validate_file_exists()`)

**New Functions Needed:**

#### 2.2.1 D069 Dual-Scale Validation
```python
validate_d069_dual_scale_plots(
    plot_dir: str,
    plot_basename: str,
    theta_suffix: str = "_theta",
    prob_suffix: str = "_probability"
) -> dict
```
**Purpose:** Validate Decision D069 requirement for ~40 trajectory RQs (both theta + probability plots must exist)

**Validates:**
- Theta-scale plot exists (e.g., `trajectory_theta.png`)
- Probability-scale plot exists (e.g., `trajectory_probability.png`)
- Both required per D069 (REJECT if either missing)

**Returns:** `{"validation_passed": bool, "theta_exists": bool, "prob_exists": bool, "theta_path": str, "prob_path": str, "message": str}`

---

#### 2.2.2 DPI/Dimensions Validation
```python
validate_plot_technical_specs(
    plot_file: str,
    expected_dpi: int = 300,
    expected_width: Optional[int] = None,
    expected_height: Optional[int] = None
) -> dict
```
**Purpose:** Validate technical plot specifications from `plots.md` template (PNG 300 DPI compliance)

**Validates:**
- File is PNG format
- DPI matches expected (default 300 per spec)
- Dimensions match expected (if specified)

**Returns:** `{"validation_passed": bool, "actual_dpi": int, "actual_width": int, "actual_height": int, "format": str, "message": str}`

**Dependencies:** Requires `Pillow` (PIL) library for PNG metadata extraction

---

#### 2.2.3 Plot Content Validation
```python
validate_plot_content(
    plot_file: str,
    required_elements: List[str],
    check_labels: bool = True,
    check_legend: bool = False
) -> dict
```
**Purpose:** Verify plot has expected visual elements (deeper inspection)

**Validates:**
- Required axes labels present (if `check_labels=True`)
- Legend present (if `check_legend=True`)
- Custom elements via `required_elements` parameter

**Returns:** `{"validation_passed": bool, "missing_elements": list, "found_elements": list, "message": str}`

**Dependencies:** Requires image processing (Pillow) + OCR (pytesseract) OR matplotlib figure inspection (if plots saved as pickle)

**Note:** Content validation may be computationally expensive. Consider optional/deferred implementation if RQ 5.1 doesn't require deep inspection.

---

#### 2.2.4 Composite Plotting Validation
```python
validate_plots(
    plot_dir: str,
    expected_plots: List[Dict[str, Any]],
    check_lineage: bool = True,
    check_d069: bool = False,
    check_technical: bool = True,
    check_content: bool = False
) -> dict
```
**Purpose:** Convenience wrapper combining all plotting validation checks

**Parameters:**
- `plot_dir`: Directory containing plots
- `expected_plots`: List of plot specifications (name, type, requirements)
- `check_lineage`: Validate data lineage (default True)
- `check_d069`: Validate dual-scale plots (default False, enable for trajectory RQs)
- `check_technical`: Validate DPI/dimensions (default True)
- `check_content`: Validate plot content (default False, expensive)

**Returns:** Aggregated validation report

---

### 2.3 Interface Standardization - ENHANCE EXISTING

**User Decision:** Hybrid approach - Keep existing fields + add standardized `validation_passed` field

**Current v3 Pattern:**
```python
# Different field names across functions
result = validate_irt_convergence(...)  # Returns {"converged": bool, ...}
result = validate_data_columns(...)     # Returns {"valid": bool, ...}
result = validate_file_exists(...)      # Returns {"exists": bool, ...}
result = check_missing_data(...)        # Returns {"has_missing": bool, ...} (inverted!)
```

**v4.X Enhanced Pattern:**
```python
# All functions include standardized field + existing fields
result = validate_irt_convergence(...)
# Returns {"validation_passed": bool, "converged": bool, ...}

result = validate_data_columns(...)
# Returns {"validation_passed": bool, "valid": bool, ...}

result = validate_file_exists(...)
# Returns {"validation_passed": bool, "exists": bool, ...}

result = check_missing_data(...)
# Returns {"validation_passed": bool, "has_missing": bool, ...}
```

**Standardization Rules:**
- `validation_passed = True` → Validation succeeded (analysis can proceed)
- `validation_passed = False` → Validation failed (MUST NOT proceed with analysis)

**Field Mapping:**
- For `valid`, `converged`, `exists`: `validation_passed = <field_value>`
- For `has_missing`: `validation_passed = not has_missing` (inverted)
- For nested `passed` (LMM residuals): `validation_passed = normality_test["passed"]`

---

### 2.4 Error Reporting - BREAKING CHANGE FROM v3

**User Decision:** Raise exception containing dict (prevents silent fails, provides detailed reason)

**Current v3 Pattern:**
```python
# Returns dict, never raises
result = validate_irt_convergence(irt_results)
if not result["converged"]:
    print(f"Warning: {result['message']}")
    # Analysis continues anyway (SILENT FAIL possible)
```

**v4.X Enhanced Pattern:**
```python
# Raises ValidationError with dict attached
try:
    result = validate_irt_convergence(irt_results)
    # If validation_passed=False, raises immediately
except ValidationError as e:
    # e.details contains full validation dict
    log.error(f"IRT validation failed: {e.details['message']}")
    raise  # Stop execution (NO SILENT FAILS)
```

**Implementation:**
1. Create custom `ValidationError` exception class in `tools/validation.py`
2. Add `details` attribute containing full validation dict
3. All validation functions check `validation_passed` field after computing result
4. If `validation_passed=False`, raise `ValidationError(details=result)`
5. If `validation_passed=True`, return result dict normally

**Benefits:**
- **Fail-fast:** Execution stops immediately on validation failure (prevents cascading errors)
- **Detailed logs:** Exception message + dict details logged for debugging
- **No silent fails:** Impossible to ignore validation failures
- **Backward compatible (partial):** Can catch exception and access `.details` dict if needed

**Example Implementation:**
```python
class ValidationError(Exception):
    """Raised when validation check fails."""
    def __init__(self, message: str, details: Dict[str, Any]):
        super().__init__(message)
        self.details = details

def validate_irt_convergence(results: Dict[str, Any]) -> Dict[str, Any]:
    """Validate IRT convergence (v4.X enhanced)."""
    converged = results.get("model_converged", False)

    result = {
        "converged": converged,
        "validation_passed": converged,  # NEW: standardized field
        "message": "Model converged successfully" if converged else "Model did not converge",
        "final_loss": results.get("final_loss"),
        "epochs_run": results.get("epochs_run")
    }

    # NEW: Raise exception if validation failed
    if not result["validation_passed"]:
        raise ValidationError(result["message"], details=result)

    return result
```

---

## 3. Migration Plan

### 3.1 Overview

**Total Tasks:** 4 (V2a, V2b, V2c, V2d)

| Task | Scope | Functions | Approach | Priority |
|------|-------|-----------|----------|----------|
| V2a: IRT | Migrate IRT validation | 3 existing | Port + enhance interface | CRITICAL |
| V2b: LMM | Migrate LMM validation | 2 existing | Port + enhance interface | CRITICAL |
| V2c: CTT | Migrate CTT validation | 0 existing | DEFERRED (build if RQ 5.1 needs) | LOW |
| V2d: Plotting | Migrate + build plotting validation | 0 specific (2 general) + 4 new | Port general + build 4 new | HIGH |

**Total Functions:**
- Port from v3: 14 (lineage + IRT + LMM + general + reporting)
- Build new: 4-5 (plotting validation, maybe CTT)
- **Total v4.X validation functions:** 18-19

---

### 3.2 V2a: Migrate IRT Validation Tools

**Functions to Migrate:**
1. `validate_irt_convergence()`
2. `validate_irt_parameters()`
3. `check_missing_data()`

**Migration Steps (TDD):**
1. Copy existing tests from `tests/test_validation.py` to new test file (or same file, mark as v4.X)
2. Enhance tests to check for `validation_passed` field
3. Enhance tests to expect `ValidationError` on failure
4. Update function implementations:
   - Add `validation_passed` field calculation
   - Add `if not validation_passed: raise ValidationError(...)` logic
5. Run tests until GREEN
6. Verify 100% coverage on migrated functions

**Estimated Effort:** 30-60 minutes (straightforward enhancement)

---

### 3.3 V2b: Migrate LMM Validation Tools

**Functions to Migrate:**
1. `validate_lmm_convergence()`
2. `validate_lmm_residuals()`

**Migration Steps (TDD):**
1. Copy existing tests
2. Enhance tests for `validation_passed` + `ValidationError`
3. Update implementations (same pattern as V2a)
4. Run tests until GREEN
5. Verify 100% coverage

**Estimated Effort:** 20-40 minutes

---

### 3.4 V2c: Migrate CTT Validation Tools

**Status:** DEFERRED

**Decision:** Build only if RQ 5.1 testing reveals need

**If Needed:**
1. Design CTT validation functions based on RQ requirements
2. Follow TDD (tests first)
3. Add to tools/validation.py
4. Document in tool_inventory.md
5. 100% coverage required

**Estimated Effort (if needed):** 1-2 hours (unknown requirements)

---

### 3.5 V2d: Migrate Plotting Validation Tools

**Functions to Build:**
1. `validate_d069_dual_scale_plots()` - NEW
2. `validate_plot_technical_specs()` - NEW (requires Pillow dependency)
3. `validate_plot_content()` - NEW (requires Pillow + optional pytesseract, may defer)
4. `validate_plots()` - NEW (composite wrapper)

**Functions to Migrate:**
- `validate_lineage()` - Already exists (port from V2a)
- `validate_file_exists()` - Already exists (port from V2a)

**Migration Steps (TDD):**
1. **Dependency check:** Verify Pillow installed (`poetry show pillow` or add if missing)
2. **D069 validation (high priority):**
   - Write tests for dual-scale plot validation
   - Implement function (simple file existence checks)
   - GREEN tests
3. **Technical specs validation (high priority):**
   - Write tests for DPI/dimensions (mock PNG metadata)
   - Implement using Pillow.Image.open() to read PNG metadata
   - GREEN tests
4. **Content validation (deferred if complex):**
   - Assess complexity during RQ 5.1
   - Build only if needed for publication quality
5. **Composite wrapper:**
   - Write tests combining all checks
   - Implement orchestration logic
   - GREEN tests
6. Verify 100% coverage

**Estimated Effort:** 2-3 hours (new functions, dependency management)

---

### 3.6 General Functions (Lineage, General, Reporting)

**Functions to Migrate:**
1. `create_lineage_metadata()` - Port as-is (no validation, just metadata creation)
2. `save_lineage()` - Port as-is (no validation)
3. `load_lineage()` - Port as-is (no validation)
4. `validate_lineage()` - Enhance with `validation_passed` + `ValidationError`
5. `validate_data_columns()` - Enhance
6. `validate_file_exists()` - Enhance
7. `validate_numeric_range()` - Enhance
8. `generate_validation_report()` - Enhance (report includes `validation_passed` for each check)
9. `save_validation_report()` - Port as-is (no validation)

**Migration Steps:**
- Same TDD pattern as V2a/V2b
- Focus on functions that return validation results (4-8)
- Keep utility functions as-is (1-3, 9)

**Estimated Effort:** 1-1.5 hours

---

## 4. Validation Tool Interface Design

### 4.1 Function Signature Pattern

**All validation functions follow this pattern:**

```python
def validate_<aspect>(
    data: <InputType>,
    *,  # Force keyword arguments after this
    threshold_params: Optional[<Type>] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Validate <aspect> of <data type>.

    Parameters
    ----------
    data : <InputType>
        Data to validate
    threshold_params : <Type>, optional
        Validation thresholds (e.g., a_min=0.4 for IRT)

    Returns
    -------
    dict
        Validation result with standardized fields

    Raises
    ------
    ValidationError
        If validation fails (validation_passed=False)
        Contains details dict with full validation info

    Example
    -------
    >>> try:
    ...     result = validate_irt_convergence(irt_results)
    ...     print("Validation passed!")
    ... except ValidationError as e:
    ...     print(f"Failed: {e.details['message']}")
    """
    # Implementation
```

---

### 4.2 Return Dict Structure

**All validation functions return dict with standardized fields:**

```python
{
    # REQUIRED STANDARDIZED FIELD (NEW in v4.X)
    "validation_passed": bool,  # True = validation succeeded, False = failed

    # EXISTING v3 FIELDS (preserved for backward compatibility)
    "valid": bool,          # OR "converged", "exists", "has_missing", etc.
    "message": str,         # Human-readable explanation

    # DETAILS (function-specific)
    "n_flagged": int,       # Number of flagged items (if applicable)
    "flagged_items": list,  # Specific items that failed (if applicable)
    "test_statistic": float,  # Statistical test results (if applicable)
    # ... other function-specific fields
}
```

**Field Mapping Rules:**

| v3 Field Name | v4.X `validation_passed` Value | Notes |
|---------------|-------------------------------|-------|
| `"valid": True` | `True` | Direct mapping |
| `"valid": False` | `False` | Direct mapping |
| `"converged": True` | `True` | Direct mapping |
| `"converged": False` | `False` | Direct mapping |
| `"exists": True` | `True` | Direct mapping |
| `"exists": False` | `False` | Direct mapping |
| `"has_missing": False` | `True` | **INVERTED** (no missing = passed) |
| `"has_missing": True` | `False` | **INVERTED** (has missing = failed) |
| `"passed": True` (nested) | `True` | Nested in `normality_test`, promote to top level |
| `"passed": False` (nested) | `False` | Nested in `normality_test`, promote to top level |

---

### 4.3 Error Reporting Pattern

**v4.X uses exception-with-dict pattern:**

```python
class ValidationError(Exception):
    """
    Raised when validation check fails.

    Attributes
    ----------
    details : dict
        Full validation result dict containing diagnostic information
    """
    def __init__(self, message: str, details: Dict[str, Any]):
        super().__init__(message)
        self.details = details
```

**Usage in validation functions:**

```python
def validate_irt_convergence(results: Dict[str, Any]) -> Dict[str, Any]:
    """Validate IRT convergence."""
    converged = results.get("model_converged", False)

    result = {
        "validation_passed": converged,
        "converged": converged,
        "message": "Model converged" if converged else "Model did not converge",
        "final_loss": results.get("final_loss"),
        "epochs_run": results.get("epochs_run")
    }

    # Raise if failed
    if not result["validation_passed"]:
        raise ValidationError(result["message"], details=result)

    return result
```

**Usage in generated code:**

```python
# Option 1: Let exception propagate (fail-fast)
result = validate_irt_convergence(irt_results)
# If we reach here, validation passed

# Option 2: Catch and log (if need to continue)
try:
    result = validate_irt_convergence(irt_results)
except ValidationError as e:
    log.error(f"IRT validation failed: {e}")
    log.error(f"Details: {e.details}")
    # Decide whether to continue or re-raise
    raise
```

---

### 4.4 Integration with v4.X Architecture

**Layer 1: Tool Inventory**
- Document all validation functions in `tool_inventory.md`
- Include full signatures with type hints
- Document which analysis tool each validation pairs with
- Document `validation_passed` field + `ValidationError` behavior

**Layer 2: rq_tools Agent**
- Reads `tool_inventory.md` validation section
- Specifies validation tool per analysis step in `3_tools.yaml`
- Includes validation function signature (prevents API guessing)

**Layer 3: rq_planner Agent**
- States validation MUST be used in `2_plan.md`
- Documents validation requirements per step

**Layer 4: rq_analysis Agent**
- Generates `4_analysis.yaml` with validation calls embedded
- Each step ends with validation call (MANDATORY)

**Layer 5: g_code Agent**
- Generates Python code with try/except blocks around validation calls
- Logs `ValidationError` details on failure
- Execution stops immediately if validation fails (fail-fast)

**Example generated code:**

```python
# Step 01: IRT Calibration
from tools.analysis_irt import calibrate_grm
from tools.validation import validate_irt_convergence, ValidationError

log.info("Step 01: Calibrate IRT model (Pass 1)")

# Run analysis tool
irt_results = calibrate_grm(
    response_matrix=response_df,
    item_mapping=item_map,
    n_factors=3,
    max_epochs=3000
)

# Run validation tool
try:
    validation_result = validate_irt_convergence(irt_results)
    log.info(f"Validation passed: {validation_result['message']}")
except ValidationError as e:
    log.error(f"Step 01 validation FAILED: {e}")
    log.error(f"Convergence status: {e.details['converged']}")
    log.error(f"Final loss: {e.details['final_loss']}")
    log.error(f"Epochs run: {e.details['epochs_run']}")
    raise  # Stop execution, trigger g_debug
```

---

## 5. Dependencies

### 5.1 Existing Dependencies (v3)

**From v3 `tools/validation.py`:**
- `pandas` - DataFrame operations
- `numpy` - Numeric operations
- `scipy.stats` - Statistical tests (Shapiro-Wilk, KS)
- `pathlib` - Path operations
- `json` - JSON serialization
- `typing` - Type hints

**Status:** All satisfied in current environment

---

### 5.2 New Dependencies (v4.X)

**For plotting validation (V2d):**

| Package | Purpose | Installation | Priority |
|---------|---------|--------------|----------|
| `Pillow` (PIL) | PNG metadata extraction (DPI, dimensions) | `poetry add Pillow` | HIGH (V2d critical) |
| `pytesseract` | OCR for plot content validation | `poetry add pytesseract` (+ system Tesseract install) | LOW (deferred) |
| `matplotlib` | Alternative: Inspect figure objects if plots saved as pickle | Already installed | OPTIONAL |

**Action Items:**
1. Check if Pillow already installed: `poetry show pillow`
2. If not, add: `poetry add Pillow`
3. Defer pytesseract until RQ 5.1 reveals content validation need
4. Consider matplotlib-based content validation (if figures saved as pickle) as alternative to OCR

---

## 6. Testing Strategy

### 6.1 Test Coverage Requirements

**User Requirement:** 100% coverage (not ≥80%, EXACTLY 100% per Issue #22)

**Verification Command:**
```bash
poetry run pytest tests/test_validation.py --cov=tools.validation --cov-report=term-missing
```

**Expected Output:**
```
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
tools/validation.py       XXX      0   100%
```

**Acceptance Criteria:**
- `Cover` column shows exactly `100%`
- `Missing` column is empty
- All tests GREEN (no failures, no skips)

---

### 6.2 Test Organization

**Existing v3 Tests:** `tests/test_validation.py` (362 lines, 49/49 passing)

**v4.X Test Enhancement Strategy:**

**Option 1: Enhance existing test file**
- Keep same file structure
- Add v4.X-specific assertions to existing tests:
  - Check `validation_passed` field present
  - Check `ValidationError` raised on failure
- Pros: Continuity, single source
- Cons: Mixing v3 and v4.X test logic

**Option 2: Create new v4.X test file**
- Create `tests/test_validation_v4x.py`
- Copy relevant tests from v3
- Enhance for v4.X interface
- Keep v3 tests for backward compatibility testing
- Pros: Clean separation, easy comparison
- Cons: Duplication, maintenance overhead

**Recommendation:** Option 1 (enhance existing file)
- Mark v3-specific tests with `pytest.mark.v3`
- Mark v4.X-specific tests with `pytest.mark.v4x`
- Can run separately if needed: `pytest -m v4x`

---

### 6.3 TDD Workflow Per Function

**For each validation function (e.g., `validate_irt_convergence`):**

1. **RED: Write failing tests**
   ```python
   def test_validate_irt_convergence_v4x_interface():
       """Test v4.X interface enhancements."""
       from tools.validation import validate_irt_convergence, ValidationError

       # Test 1: Success case has validation_passed field
       converged_results = {"model_converged": True, "final_loss": 25.5}
       result = validate_irt_convergence(converged_results)
       assert "validation_passed" in result
       assert result["validation_passed"] is True

       # Test 2: Failure case raises ValidationError
       non_converged_results = {"model_converged": False, "final_loss": 45.0}
       with pytest.raises(ValidationError) as exc_info:
           validate_irt_convergence(non_converged_results)

       # Test 3: Exception contains details dict
       assert "converged" in exc_info.value.details
       assert exc_info.value.details["converged"] is False
   ```

2. **GREEN: Enhance implementation**
   - Add `validation_passed` field calculation
   - Add `if not validation_passed: raise ValidationError(...)` logic
   - Run tests: `pytest tests/test_validation.py::test_validate_irt_convergence_v4x_interface -v`

3. **REFACTOR: Clean up**
   - Verify existing v3 tests still pass
   - Check coverage: 100%
   - Commit with message: "V2a: Migrate validate_irt_convergence to v4.X interface"

---

## 7. Timeline Estimate

**Total Phase 4 Effort:** 5-7 hours

| Task | Effort | Notes |
|------|--------|-------|
| V1: Audit (this document) | **1 hour** | ✅ Complete |
| V2a: Migrate IRT validation (3 functions) | 30-60 min | TDD, straightforward |
| V2b: Migrate LMM validation (2 functions) | 20-40 min | TDD, straightforward |
| V2c: Migrate CTT validation (deferred) | 0 min | Skip unless RQ 5.1 needs |
| V2d: Migrate plotting validation (4 new functions) | 2-3 hours | New code, dependencies |
| V2d: Migrate general validation (9 functions) | 1-1.5 hours | TDD, straightforward |
| V3: Update tool_inventory.md | 30-45 min | Documentation |
| V4: Test all validation tools (100% coverage) | 15-30 min | Verification |
| **Buffer (unexpected issues)** | 30-60 min | First time with v4.X patterns |

**Critical Path:** V1 → V2a/V2b/V2d (parallel) → V3 → V4

**Parallelization:** V2a, V2b, V2d can be done in any order (independent)

---

## 8. Success Criteria

**V1 (Audit) Success:**
- ✅ Audit document created (this file)
- ✅ Existing v3 tools inventoried (14 functions, locations, tests)
- ✅ Gaps identified (CTT deferred, plotting new)
- ✅ Migration plan documented (port vs build vs defer)
- ✅ Interface design specified (hybrid + exception pattern)
- ✅ User decisions documented (4 questions answered)

**V2a-V2d (Migration) Success:**
- All validation functions enhanced with v4.X interface
- `validation_passed` field present in all return dicts
- `ValidationError` raised on all failures
- Tests updated and passing
- 100% coverage per function group

**V3 (Documentation) Success:**
- `tool_inventory.md` updated with validation section
- All validation functions documented:
  - Full signatures with type hints
  - Input/output specifications
  - Validation criteria
  - Error types raised
  - Usage examples

**V4 (Testing) Success:**
- `pytest tests/test_validation.py --cov=tools.validation --cov-report=term-missing`
- Output shows 100% coverage (not ≥80%)
- All tests GREEN
- Zero missing lines in coverage report

---

## 9. Next Steps

1. ✅ **V1 Complete** - Review audit with user, get approval
2. **V2a Start** - Migrate IRT validation tools (TDD)
3. **V2b Start** - Migrate LMM validation tools (TDD)
4. **V2d Start** - Build plotting validation tools (check Pillow dependency first)
5. **V2c Decision** - Mark as deferred or build during RQ 5.1
6. **V3 Start** - Update tool_inventory.md with migrated tools
7. **V4 Start** - Run coverage tests, verify 100%
8. **Mark V1 complete** - Update todo.yaml status to completed

---

## Appendices

### Appendix A: v3 Validation Function Signatures (Complete Reference)

```python
# Lineage
def create_lineage_metadata(source_file: str, output_file: str, operation: str,
                           parameters: Optional[Dict[str, Any]] = None,
                           description: str = "") -> Dict[str, Any]

def save_lineage(metadata: Dict[str, Any], lineage_file: str) -> None

def load_lineage(lineage_file: str) -> Dict[str, Any]

def validate_lineage(lineage_file: str, expected_source: Optional[str] = None,
                    expected_pass: Optional[int] = None) -> Dict[str, Any]

# IRT
def validate_irt_convergence(results: Dict[str, Any]) -> Dict[str, Any]

def validate_irt_parameters(df_items: pd.DataFrame, a_min: float = 0.4,
                           b_max: float = 3.0, a_col: str = "a",
                           b_col: str = "b") -> Dict[str, Any]

def check_missing_data(df: pd.DataFrame) -> Dict[str, Any]

# LMM
def validate_lmm_convergence(lmm_result) -> Dict[str, Any]

def validate_lmm_residuals(residuals: Union[np.ndarray, pd.Series],
                          alpha: float = 0.05) -> Dict[str, Any]

# General
def validate_data_columns(df: pd.DataFrame, required_columns: List[str]) -> Dict[str, Any]

def validate_file_exists(file_path: str) -> Dict[str, Any]

def validate_numeric_range(data: Union[pd.Series, np.ndarray],
                          min_val: Optional[float] = None,
                          max_val: Optional[float] = None,
                          column_name: str = "data") -> Dict[str, Any]

# Reporting
def generate_validation_report(validation_checks: Dict[str, Dict[str, Any]],
                              report_title: str = "Validation Report") -> Dict[str, Any]

def save_validation_report(report: Dict[str, Any], report_file: str) -> None
```

### Appendix B: v4.X Enhanced Function Signatures (Proposed)

```python
# NEW: Exception class
class ValidationError(Exception):
    """Raised when validation fails."""
    def __init__(self, message: str, details: Dict[str, Any]):
        super().__init__(message)
        self.details = details

# All validation functions enhanced (same signatures, different behavior):
# - Add validation_passed field to return dict
# - Raise ValidationError if validation_passed=False

# NEW: Plotting validation
def validate_d069_dual_scale_plots(plot_dir: str, plot_basename: str,
                                   theta_suffix: str = "_theta",
                                   prob_suffix: str = "_probability") -> Dict[str, Any]

def validate_plot_technical_specs(plot_file: str, expected_dpi: int = 300,
                                  expected_width: Optional[int] = None,
                                  expected_height: Optional[int] = None) -> Dict[str, Any]

def validate_plot_content(plot_file: str, required_elements: List[str],
                         check_labels: bool = True,
                         check_legend: bool = False) -> Dict[str, Any]

def validate_plots(plot_dir: str, expected_plots: List[Dict[str, Any]],
                  check_lineage: bool = True, check_d069: bool = False,
                  check_technical: bool = True,
                  check_content: bool = False) -> Dict[str, Any]
```

---

**End of V1 Audit Document**
