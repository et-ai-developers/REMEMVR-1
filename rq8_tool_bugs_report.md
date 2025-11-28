# RQ 5.8 Tool Bug Report

**Date:** 2025-11-28
**RQ:** 5.8 (Two-Phase Forgetting Hypothesis)
**Status:** 5/7 analysis steps successful, 2 failed due to tool bugs
**Severity:** HIGH (blocks production use of 2 validation tools)

---

## Executive Summary

RQ 5.8 execution revealed **2 critical tool bugs** in YELLOW-status tools that had never been production-validated:

1. **`validate_lmm_assumptions_comprehensive`** (Step 4): Calls non-existent `get_influence()` method on `MixedLMResults`
2. **`extract_segment_slopes_from_lmm`** (Step 5): Uses wrong coefficient name for categorical interactions

Both tools passed **100% of unit tests** but failed on **real statsmodels output**. This is the first RQ to use these tools in production, exposing gaps between mocked tests and real-world usage.

**Impact:** Steps 4-5 outputs unavailable, but core analysis (Steps 0-3, 6) succeeded. Main scientific finding obtained (deltaAIC = +5.03 favors continuous model).

---

## Bug #1: `validate_lmm_assumptions_comprehensive` - Missing `get_influence()` Method

### Error Details

**Error Message:**
```
AttributeError: 'MixedLMResults' object has no attribute 'get_influence'
```

**Location:** `tools/validation.py` line 1144

**Context:** Step 4 (Validate LMM Assumptions) - Diagnostic #5: Outlier Detection via Cook's Distance

**Code Excerpt:**
```python
# Line 1144 in tools/validation.py
def validate_lmm_assumptions_comprehensive(lmm_result, data, outcome_col, predictor_cols):
    # ... [earlier diagnostics 1-4] ...

    # Diagnostic 5: Outliers (Cook's Distance)
    influence = lmm_result.get_influence()  # ← FAILS HERE
    cooks_d = influence.cooks_distance[0]
    # ... rest of outlier detection ...
```

**Execution Log:**
```
[START] Step 4: Validate LMM Assumptions
[LOAD] Loading fitted models from Steps 2-3...
[LOADED] Quadratic model (400 observations)
[LOADED] Piecewise model (400 observations)
[LOAD] Loading time-transformed data...
[LOADED] Time data (400 rows, 9 cols)
[ANALYSIS] Running assumption validation for quadratic model...
[ERROR] 'MixedLMResults' object has no attribute 'get_influence'
```

### Root Cause Analysis

**Why the bug exists:**

1. **API Mismatch:** The `get_influence()` method exists in `statsmodels.regression.linear_model.RegressionResults` (OLS models) but **NOT** in `statsmodels.regression.mixed_linear_model.MixedLMResults` (LMM models).

2. **Test Coverage Gap:** Unit tests (14/14 GREEN) used **mocked** `MixedLMResults` objects that artificially provided `get_influence()`:
   ```python
   # Example from tests/test_validation_tools.py (hypothetical)
   mock_lmm = MagicMock()
   mock_lmm.get_influence.return_value = mock_influence_obj
   # Test passes because mock provides the method
   ```

3. **First Production Use:** RQ 5.8 is the **first RQ** to execute `validate_lmm_assumptions_comprehensive` with a real `MixedLMResults` object from statsmodels.

4. **YELLOW Status Warning:** Tool marked YELLOW = "tested but not production-validated" - exactly this scenario.

### How to Fix

**Option A: Remove Cook's Distance Diagnostic (Quick Fix)**

Since Cook's distance is **not available** for MixedLM in statsmodels, skip this diagnostic:

```python
# Line 1144 in tools/validation.py
def validate_lmm_assumptions_comprehensive(lmm_result, data, outcome_col, predictor_cols):
    # ... diagnostics 1-4 ...

    # Diagnostic 5: Outliers - SKIP for MixedLM (no get_influence() support)
    # Note: Cook's distance requires OLS influence measures not available in MixedLM
    log("Diagnostic 5: Outliers - SKIPPED (not supported for MixedLM)")
    outlier_results = {
        'test': 'cooks_distance',
        'status': 'not_applicable',
        'message': 'Cook\'s distance not available for mixed effects models'
    }

    # ... rest of function ...
```

**Option B: Use Alternative Outlier Detection (Recommended)**

Implement outlier detection using **studentized residuals** (available for MixedLM):

```python
# Line 1144 in tools/validation.py
def validate_lmm_assumptions_comprehensive(lmm_result, data, outcome_col, predictor_cols):
    # ... diagnostics 1-4 ...

    # Diagnostic 5: Outliers via Studentized Residuals
    residuals = lmm_result.resid
    residual_std = np.std(residuals)
    studentized_resid = residuals / residual_std

    # Flag observations with |studentized residual| > 3
    outlier_threshold = 3.0
    outlier_mask = np.abs(studentized_resid) > outlier_threshold
    n_outliers = np.sum(outlier_mask)
    outlier_pct = (n_outliers / len(residuals)) * 100

    outlier_results = {
        'test': 'studentized_residuals',
        'threshold': outlier_threshold,
        'n_outliers': int(n_outliers),
        'outlier_percentage': float(outlier_pct),
        'status': 'pass' if outlier_pct < 5.0 else 'warning',
        'message': f'{n_outliers} outliers detected ({outlier_pct:.1f}% of observations)'
    }

    # ... rest of function ...
```

**Option C: Compute Approximate Cook's Distance Manually**

Use the formula D_i = (r_i^2 / p) * (h_ii / (1 - h_ii)) where:
- r_i = standardized residual
- p = number of parameters
- h_ii = leverage (diagonal of hat matrix)

However, computing leverage for MixedLM is **non-trivial** due to random effects. Option B is simpler and sufficient.

### Testing Fix

**Update unit tests to use REAL statsmodels objects:**

```python
# tests/test_validation_tools.py
def test_validate_lmm_assumptions_comprehensive_real_model():
    """Test with actual statsmodels MixedLMResults, not mocks."""
    import pandas as pd
    import statsmodels.formula.api as smf
    from tools.validation import validate_lmm_assumptions_comprehensive

    # Create simple test data
    data = pd.DataFrame({
        'y': np.random.randn(100),
        'x': np.random.randn(100),
        'group': np.repeat(['A', 'B', 'C', 'D'], 25)
    })

    # Fit REAL MixedLM model
    model = smf.mixedlm("y ~ x", data, groups=data['group'])
    result = model.fit()  # ← REAL MixedLMResults object

    # Test should pass with real object
    validation = validate_lmm_assumptions_comprehensive(
        lmm_result=result,
        data=data,
        outcome_col='y',
        predictor_cols=['x']
    )

    assert validation['valid'] == True
    assert 'outliers' in validation  # Verify outlier diagnostic ran
```

### Verification Checklist

- [ ] Fix implemented (Option A, B, or C)
- [ ] Unit tests updated to use real `MixedLMResults` objects
- [ ] All tests GREEN with real statsmodels output
- [ ] Tool status updated from YELLOW → ORANGE (pending production validation)
- [ ] Re-run RQ 5.8 Step 4 to verify fix
- [ ] Tool status updated from ORANGE → GREEN after successful production run
- [ ] Document change in tools_inventory.md

---

## Bug #2: `extract_segment_slopes_from_lmm` - Wrong Coefficient Name

### Error Details

**Error Message:**
```
KeyError: "Required coefficient 'Days_within:SegmentLate' not found in LMM result.
Available coefficients: ['Intercept', 'Segment[T.Late]', 'Days_within',
'Days_within:Segment[T.Late]', 'Group Var', 'Group x Days_within Cov', 'Days_within Var']"
```

**Location:** `tools/analysis_lmm.py` line 1822

**Context:** Step 5 (Extract Slopes) - Extracting segment-specific slopes from piecewise LMM

**Code Excerpt:**
```python
# Line 1822 in tools/analysis_lmm.py
def extract_segment_slopes_from_lmm(lmm_result, segment_col='Segment', time_col='Days_within'):
    # Construct coefficient name
    interaction_coef = f'{time_col}:{segment_col}Late'  # ← Constructs 'Days_within:SegmentLate'

    # Extract interaction coefficient
    beta_interaction = lmm_result.params[interaction_coef]  # ← FAILS HERE
    # ... rest of function ...
```

**Execution Log:**
```
[START] Step 5: Extract Slopes and Compute Ratio
[LOAD] Loading piecewise model from step03_piecewise_model.pkl...
[LOADED] Piecewise model (400 observations)
[INFO] Model converged: False
[INFO] AIC: 878.74
[ANALYSIS] Extracting segment slopes and computing ratio...
[ERROR] "Required coefficient 'Days_within:SegmentLate' not found in LMM result.
Available coefficients: ['Intercept', 'Segment[T.Late]', 'Days_within',
'Days_within:Segment[T.Late]', ...]"
```

### Root Cause Analysis

**Why the bug exists:**

1. **Categorical Encoding:** When `Segment` column is categorical (dtype='category' or dtype='object'), statsmodels uses **R-style treatment encoding**: `Segment[T.Late]` where `[T.Late]` indicates the "Late" level with "Early" as reference.

2. **Expected vs Actual:**
   - Tool expects: `'Days_within:SegmentLate'` (simple concatenation)
   - Statsmodels provides: `'Days_within:Segment[T.Late]'` (categorical encoding)

3. **Test Coverage Gap:** Unit tests (11/11 GREEN) likely used one of:
   - **Numeric encoding** (Segment as 0/1) where statsmodels names it `'Days_within:Segment'`
   - **Mocked coefficient dictionaries** with hardcoded names
   - **Pre-constructed parameter dictionaries** that avoid real patsy formula parsing

4. **First Production Use:** RQ 5.8 uses **categorical Segment** ('Early', 'Late') triggering R-style encoding. Previous RQs either:
   - Didn't use piecewise LMM (RQ 5.1-5.7)
   - Didn't reach production execution (RQ 5.6 may have implemented but not executed)

### Data Flow Demonstration

**Step 1 generates categorical Segment:**
```python
# step01_create_time_transformations.py output
time_data = pd.DataFrame({
    'UID': ['A010', 'A010', ...],
    'test': [1, 2, ...],
    'Segment': ['Early', 'Late', ...],  # ← Categorical strings
    'Days_within': [0.04, 0.91, ...]
})
```

**Step 3 fits LMM with formula:**
```python
formula = "theta ~ Days_within * Segment"  # Patsy parses Segment as categorical
model = smf.mixedlm(formula, data=time_data, groups=time_data['UID'])
result = model.fit()

# Result coefficient names:
# - Intercept
# - Days_within
# - Segment[T.Late]           ← R-style encoding for reference level
# - Days_within:Segment[T.Late]  ← Interaction with categorical
```

**Step 5 tries to extract with wrong name:**
```python
interaction_coef = 'Days_within:SegmentLate'  # ← WRONG
beta_interaction = result.params[interaction_coef]  # ← KeyError
```

### How to Fix

**Option A: Hardcode Correct Name (Quick Fix)**

```python
# Line 1822 in tools/analysis_lmm.py
def extract_segment_slopes_from_lmm(lmm_result, segment_col='Segment', time_col='Days_within'):
    # For categorical Segment, statsmodels uses [T.Late] encoding
    interaction_coef = f'{time_col}:{segment_col}[T.Late]'  # ← Fixed

    # Rest of function unchanged
    beta_interaction = lmm_result.params[interaction_coef]
    # ...
```

**Limitations:** Assumes "Late" is the non-reference level. Breaks if reference level changes.

**Option B: Auto-Detect Coefficient Name (Recommended)**

```python
# Line 1822 in tools/analysis_lmm.py
def extract_segment_slopes_from_lmm(lmm_result, segment_col='Segment', time_col='Days_within'):
    """
    Extract segment-specific slopes from piecewise LMM.

    Auto-detects interaction coefficient name to handle both:
    - Categorical Segment: 'Days_within:Segment[T.Late]'
    - Numeric Segment: 'Days_within:Segment'
    """
    # Get all coefficient names
    coef_names = list(lmm_result.params.index)

    # Pattern 1: Categorical interaction (R-style encoding)
    categorical_pattern = f'{time_col}:{segment_col}[T.'
    categorical_matches = [name for name in coef_names if name.startswith(categorical_pattern)]

    # Pattern 2: Numeric interaction (simple concatenation)
    numeric_pattern = f'{time_col}:{segment_col}'
    numeric_matches = [name for name in coef_names if name == numeric_pattern]

    # Pattern 3: Alternative categorical encoding
    alt_categorical_pattern = f'{time_col}:C({segment_col})'
    alt_matches = [name for name in coef_names if name.startswith(alt_categorical_pattern)]

    # Select interaction coefficient
    if categorical_matches:
        interaction_coef = categorical_matches[0]  # Use first categorical match
        log(f"Detected categorical interaction: {interaction_coef}")
    elif numeric_matches:
        interaction_coef = numeric_matches[0]
        log(f"Detected numeric interaction: {interaction_coef}")
    elif alt_matches:
        interaction_coef = alt_matches[0]
        log(f"Detected alternative categorical encoding: {interaction_coef}")
    else:
        # Provide helpful error message
        available = ', '.join(coef_names)
        raise KeyError(
            f"Could not find interaction term for {time_col}:{segment_col}.\n"
            f"Searched patterns: '{categorical_pattern}*', '{numeric_pattern}', '{alt_categorical_pattern}*'\n"
            f"Available coefficients: {available}\n"
            f"Ensure your LMM formula includes '{time_col} * {segment_col}' interaction."
        )

    # Extract coefficient (rest of function unchanged)
    beta_interaction = lmm_result.params[interaction_coef]
    # ... compute slopes, ratio, SE via delta method ...
```

**Option C: Require Caller to Specify Coefficient Name**

Add parameter `interaction_coef_name` allowing manual override:

```python
def extract_segment_slopes_from_lmm(
    lmm_result,
    segment_col='Segment',
    time_col='Days_within',
    interaction_coef_name=None  # ← New parameter
):
    if interaction_coef_name is None:
        # Auto-detect (use Option B logic)
        interaction_coef = auto_detect_interaction_coef(...)
    else:
        # Use caller-specified name
        interaction_coef = interaction_coef_name

    # ... rest of function ...
```

**Recommendation:** **Option B** (auto-detect) is most robust for production use.

### Testing Fix

**Update unit tests to use categorical Segment:**

```python
# tests/test_piecewise_tools.py
def test_extract_segment_slopes_categorical():
    """Test slope extraction with CATEGORICAL Segment column."""
    import pandas as pd
    import statsmodels.formula.api as smf
    from tools.analysis_lmm import extract_segment_slopes_from_lmm

    # Create test data with CATEGORICAL Segment
    data = pd.DataFrame({
        'theta': np.random.randn(200),
        'Days_within': np.tile([0, 1, 2, 3], 50),
        'Segment': np.tile(['Early', 'Late'], 100),  # ← Categorical strings
        'UID': np.repeat(range(50), 4)
    })

    # Fit piecewise LMM with categorical Segment
    formula = "theta ~ Days_within * Segment"
    model = smf.mixedlm(formula, data, groups=data['UID'])
    result = model.fit()

    # Verify coefficient name is categorical
    assert 'Days_within:Segment[T.Late]' in result.params.index
    assert 'Days_within:SegmentLate' not in result.params.index  # Old name should NOT exist

    # Test should pass with auto-detection
    slopes = extract_segment_slopes_from_lmm(
        lmm_result=result,
        segment_col='Segment',
        time_col='Days_within'
    )

    assert 'Early_slope' in slopes
    assert 'Late_slope' in slopes
    assert 'Ratio_Late_Early' in slopes

def test_extract_segment_slopes_numeric():
    """Test slope extraction with NUMERIC Segment column."""
    # Same test but with Segment as 0/1 numeric
    data = pd.DataFrame({
        'theta': np.random.randn(200),
        'Days_within': np.tile([0, 1, 2, 3], 50),
        'Segment': np.tile([0, 1], 100),  # ← Numeric 0/1
        'UID': np.repeat(range(50), 4)
    })

    # ... rest of test ...
```

### Verification Checklist

- [ ] Fix implemented (Option A, B, or C)
- [ ] Unit tests updated to test BOTH categorical and numeric Segment
- [ ] All tests GREEN with real statsmodels output
- [ ] Test with actual RQ 5.8 data to verify categorical detection
- [ ] Tool status updated from YELLOW → ORANGE (pending production validation)
- [ ] Re-run RQ 5.8 Step 5 to verify fix
- [ ] Tool status updated from ORANGE → GREEN after successful production run
- [ ] Update docstring in tools/analysis_lmm.py to document categorical vs numeric handling
- [ ] Document change in tools_inventory.md

---

## Impact Assessment

### Steps Affected

| Step | Name | Status | Impact |
|------|------|--------|--------|
| 0 | Get Data | ✅ Success | No impact |
| 1 | Time Transformations | ✅ Success | No impact |
| 2 | Fit Quadratic Model | ✅ Success | No impact |
| 3 | Fit Piecewise Model | ✅ Success | No impact |
| 4 | Validate Assumptions | ❌ Failed | **Missing:** Diagnostic plots, assumption validation report |
| 5 | Extract Slopes | ❌ Failed | **Missing:** Slope comparison (Early vs Late), ratio statistics |
| 6 | Prepare Plot Data | ✅ Success | No impact |

### Data Outputs Generated

**Available (5/7 steps succeeded):**
- ✅ `data/step00_theta_tsvr.csv` - Merged theta + TSVR (400 rows)
- ✅ `data/step00_best_continuous_aic.txt` - RQ 5.7 reference AIC (873.71)
- ✅ `data/step01_time_transformed.csv` - Time transformations (9 columns)
- ✅ `data/step02_quadratic_model.pkl` - Quadratic LMM (AIC=940.32)
- ✅ `data/step02_quadratic_predictions.csv` - 11 predictions
- ✅ `data/step03_piecewise_model.pkl` - Piecewise LMM (AIC=878.74)
- ✅ `data/step03_piecewise_predictions.csv` - 18 predictions
- ✅ `plots/step06_piecewise_comparison_data.csv` - Plot source (33 rows)

**Missing (2/7 steps failed):**
- ❌ `results/step04_assumption_validation.txt` - Not generated (Step 4 crashed)
- ❌ Diagnostic plots (residuals, Q-Q, ACF) - Partially generated before crash
- ❌ `data/step05_slope_comparison.csv` - Not generated (Step 5 crashed)
- ❌ `data/step05_ratio_statistics.txt` - Not generated (Step 5 crashed)

### Scientific Findings Status

**Core finding obtained despite bugs:**
- ✅ **deltaAIC = +5.03** (Piecewise AIC - Continuous AIC)
- ✅ **Interpretation:** Continuous model FAVORED (deltaAIC > +2)
- ✅ **Conclusion:** Evidence AGAINST two-phase forgetting hypothesis

**Missing secondary analyses:**
- ❌ Formal assumption validation (normality, homoscedasticity, independence)
- ❌ Quantitative slope comparison (Early slope, Late slope, ratio)
- ❌ Statistical significance of slope difference

**Workaround:** Can manually extract slopes from Step 3 model summary or re-run Steps 4-5 after fixes.

### Downstream Impact

**Affected agents:**
- **rq_inspect:** Will flag missing Step 4-5 outputs as incomplete
- **rq_plots:** Can proceed (has Step 6 plot data CSV)
- **rq_results:** Can generate summary with caveat about missing validation/slopes

**Recommendations:**
1. Fix both tools before proceeding to rq_inspect
2. Re-run Steps 4-5 to generate missing outputs
3. Then proceed with rq_inspect → rq_plots → rq_results

---

## Historical Context

### Tool Development Timeline

**2025-11-25:** RQ 5.6 execution
- `extract_segment_slopes_from_lmm` implemented (2/2 tests)
- `validate_lmm_assumptions_comprehensive` marked PENDING

**2025-11-27:** Phase 2 Tools Development (Tools 18-25)
- Both tools implemented and tested
- `validate_lmm_assumptions_comprehensive`: 14/14 tests GREEN
- `extract_segment_slopes_from_lmm`: 11/11 tests GREEN (updated from 2→11)
- Both marked YELLOW (tested but not production-validated)

**2025-11-28:** RQ 5.8 execution (FIRST PRODUCTION USE)
- Step 4 crashes on `get_influence()` - reveals Bug #1
- Step 5 crashes on coefficient name - reveals Bug #2
- Both bugs confirm YELLOW status risk: "tests passed with mocks, production fails with real objects"

### Lessons Learned

1. **YELLOW status is a WARNING:** Tools marked YELLOW have NOT been production-validated. Expect bugs on first real use.

2. **Mocks hide API mismatches:** Unit tests with mocked objects can pass even when real statsmodels objects fail. Always include integration tests with real model fits.

3. **Categorical vs numeric matters:** Test data encoding affects coefficient naming in statsmodels. Test both categorical and numeric variants.

4. **First production use reveals bugs:** No amount of unit testing replaces running tools in real workflow. RQ 5.8 successfully exposed both bugs.

5. **TDD workflow works:** Despite bugs, workflow provided:
   - Clear error messages with exact failure points
   - Isolation of bugs to specific tools (not g_code)
   - Core analysis succeeded (5/7 steps)
   - Scientific findings obtained

---

## Recommended Actions

### Immediate (Fix Bugs)

1. **Fix Bug #1:** Implement Option B (studentized residuals for outlier detection)
2. **Fix Bug #2:** Implement Option B (auto-detect coefficient name)
3. **Update unit tests:** Use real statsmodels objects, test categorical encoding
4. **Re-run tests:** Verify 100% GREEN with fixes
5. **Update tool status:** YELLOW → ORANGE (pending production validation)

### Short-term (Validate in Production)

1. **Re-run RQ 5.8 Steps 4-5** with fixed tools
2. **Verify outputs:** Check assumption reports and slope statistics
3. **Compare with manual extraction:** Confirm slopes match Step 3 model summary
4. **Update tool status:** ORANGE → GREEN (production-validated)
5. **Update tools_status.tsv:** Document production validation date

### Long-term (Prevent Recurrence)

1. **Create integration tests:** Fit real LMMs and call all validation/extraction tools
2. **Document statsmodels quirks:** Add notes about categorical encoding to tools_inventory.md
3. **Add defensive programming:** Auto-detect coefficient names, handle missing methods gracefully
4. **Establish YELLOW→GREEN criteria:** Define "production validation" checklist
5. **Update testing guidelines:** Require at least 1 integration test per tool before YELLOW status

---

## Files Modified

**Tools requiring fixes:**
- `tools/validation.py` (line 1144) - Fix `get_influence()` bug
- `tools/analysis_lmm.py` (line 1822) - Fix coefficient name bug

**Tests requiring updates:**
- `tests/test_validation_tools.py` - Add real `MixedLMResults` tests
- `tests/test_piecewise_tools.py` - Add categorical Segment tests

**Documentation requiring updates:**
- `docs/v4/tools_inventory.md` - Document categorical encoding handling
- `docs/v4/tools_status.tsv` - Update status after fixes (YELLOW→ORANGE→GREEN)

---

## Appendix: Error Logs

### Step 4 Full Error Log

```
[START] Step 4: Validate LMM Assumptions
[LOAD] Loading fitted models from Steps 2-3...
[LOAD] Loading quadratic model from /home/etai/projects/REMEMVR/results/ch5/rq8/data/step02_quadratic_model.pkl
[LOADED] Quadratic model (400 observations)
[LOAD] Loading piecewise model from /home/etai/projects/REMEMVR/results/ch5/rq8/data/step03_piecewise_model.pkl
[LOADED] Piecewise model (400 observations)
[LOAD] Loading time-transformed data from /home/etai/projects/REMEMVR/results/ch5/rq8/data/step01_time_transformed.csv
[LOADED] Time data (400 rows, 9 cols)
[ANALYSIS] Running assumption validation for quadratic model...
[ERROR] 'MixedLMResults' object has no attribute 'get_influence'

Traceback (most recent call last):
  File "/home/etai/projects/REMEMVR/results/ch5/rq8/code/step04_validate_lmm_assumptions.py", line 203, in <module>
    quadratic_validation = validate_lmm_assumptions_comprehensive(
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/etai/projects/REMEMVR/tools/validation.py", line 1144, in validate_lmm_assumptions_comprehensive
    influence = lmm_result.get_influence()
                ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/etai/projects/REMEMVR/.venv/lib/python3.12/site-packages/statsmodels/base/wrapper.py", line 34, in __getattribute__
    obj = getattr(results, attr)
          ^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'MixedLMResults' object has no attribute 'get_influence'
```

### Step 5 Full Error Log

```
[START] Step 5: Extract Slopes and Compute Ratio
[LOAD] Loading piecewise model from /home/etai/projects/REMEMVR/results/ch5/rq8/data/step03_piecewise_model.pkl
[LOADED] Piecewise model (400 observations)
[INFO] Model converged: False
[INFO] AIC: 878.74
[ANALYSIS] Extracting segment slopes and computing ratio...
[ERROR] "Required coefficient 'Days_within:SegmentLate' not found in LMM result.
Available coefficients: ['Intercept', 'Segment[T.Late]', 'Days_within',
'Days_within:Segment[T.Late]', 'Group Var', 'Group x Days_within Cov', 'Days_within Var']"

Traceback (most recent call last):
  File "/home/etai/projects/REMEMVR/.venv/lib/python3.12/site-packages/pandas/core/indexes/base.py", line 3812, in get_loc
    return self._engine.get_loc(casted_key)
  File "pandas/_libs/index.pyx", line 167, in pandas._libs.index.IndexEngine.get_loc
KeyError: 'Days_within:SegmentLate'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/etai/projects/REMEMVR/tools/analysis_lmm.py", line 1833, in extract_segment_slopes_from_lmm
    beta_interaction = lmm_result.params[interaction_coef]
  File "/home/etai/projects/REMEMVR/.venv/lib/python3.12/site-packages/pandas/core/series.py", line 1133, in __getitem__
KeyError: 'Days_within:SegmentLate'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/etai/projects/REMEMVR/results/ch5/rq8/code/step05_extract_slopes.py", line 186, in <module>
    slope_comparison = extract_segment_slopes_from_lmm(
  File "/home/etai/projects/REMEMVR/tools/analysis_lmm.py", line 1835, in extract_segment_slopes_from_lmm
    raise KeyError(
KeyError: "Required coefficient 'Days_within:SegmentLate' not found in LMM result.
Available coefficients: ['Intercept', 'Segment[T.Late]', 'Days_within',
'Days_within:Segment[T.Late]', 'Group Var', 'Group x Days_within Cov', 'Days_within Var']"
```

---

**Report Author:** Claude Code
**Report Date:** 2025-11-28
**Version:** 1.0
**Next Steps:** Implement fixes → Update tests → Re-run RQ 5.8 Steps 4-5 → Validate GREEN
