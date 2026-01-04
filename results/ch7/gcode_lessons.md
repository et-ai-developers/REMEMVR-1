# G_CODE LESSONS LEARNED - CHAPTER 7

**Purpose:** Capture bugs found during Ch7 execution and their fixes for g_code agent to avoid repeating mistakes
**Usage:** g_code MUST read this file before generating any Ch7 code
**Last Updated:** 2026-01-04 (fully updated with all 7.1.2 bugs)

---

## CRITICAL BUGS AND FIXES

### 1. Function Signature Mismatches (RQ 7.1.1 Step 01)

**BUG:** 4_analysis.yaml specified `extract_cognitive_tests(df, tests)` but actual function has `extract_cognitive_tests(uid_list, data_path)`

**SYMPTOM:** g_code refuses to generate code due to signature mismatch

**FIX:** 
- Check actual function signatures in tools/*.py before using
- If mismatch found, write custom code instead of using mismatched function
- Update 4_analysis.yaml in future to match actual signatures

**PREVENTION:**
```python
# Instead of assuming function signature, verify first:
# grep -n "def extract_cognitive_tests" tools/data.py
# Then use actual signature or write custom code
```

---

### 2. Column Name Case Sensitivity (RQ 7.1.1 Step 01)

**BUG:** tools.data.extract_cognitive_tests looks for 'uid' but dfnonvr.csv has 'UID'

**SYMPTOM:** KeyError: "None of [Index(['uid'], dtype='object')] are in the [columns]"

**FIX:**
```python
# Always check actual column names first:
df = pd.read_csv('data/dfnonvr.csv')
print(df.columns.tolist())  # Shows 'UID' not 'uid'
```

**PREVENTION:** Never assume column names - always verify with actual data file

---

### 3. Wrong Parent Path Calculation (RQ 7.1.1 Step 01)

**BUG:** Used `parents[3]` to find project root from code file, but need `parents[4]`

**SYMPTOM:** FileNotFoundError: /home/etai/projects/REMEMVR/results/data/dfnonvr.csv (wrong path)

**FIX:**
```python
# From: results/ch7/7.1.1/code/step01.py
# Count carefully: code -> 7.1.1 -> ch7 -> results -> REMEMVR
PROJECT_ROOT = Path(__file__).resolve().parents[4]  # Not parents[3]
```

**PREVENTION:** Count directory levels carefully from script location to project root

---

### 4. Validation Logic Inversion (RQ 7.1.1 Step 00)

**BUG:** check_file_exists returns dict with 'valid' key, not 'exists' and 'size_ok'

**SYMPTOM:** Files marked as FAIL when they actually exist and pass validation

**FIX:**
```python
# WRONG - assuming specific keys:
if result.get('exists', False) and result.get('size_ok', False):

# RIGHT - use actual return value:
if result.get('valid', False):
```

**PREVENTION:** Check actual return values of validation functions before using

---

### 5. Status.yaml Structure Assumptions (RQ 7.1.1 Step 00)

**BUG:** Ch5 status.yaml has `rq_results: {status: 'success', ...}` not just `rq_results: 'success'`

**SYMPTOM:** Validation fails even though Ch5 is complete

**FIX:**
```python
# Handle both dict and string formats:
rq_results_status = status_data.get('rq_results', {})
if isinstance(rq_results_status, dict):
    actual_status = rq_results_status.get('status')
elif isinstance(rq_results_status, str):
    actual_status = rq_results_status
else:
    actual_status = 'unknown'
```

**PREVENTION:** Handle multiple possible data structures gracefully

---

### 6. RAVLT Total Calculation Error (RQ 7.1.1 Step 01)

**BUG:** Initially included distraction trial in RAVLT_Total sum

**SYMPTOM:** RAVLT_Total incorrectly high (included 6 trials instead of 5)

**FIX:**
```python
# WRONG - includes distraction trial:
ravlt_cols = [col for col in df.columns if 'RAVLT' in col and 'trial' in col.lower()]
trial_cols = sorted(ravlt_cols)[:5]  # Could include distraction

# RIGHT - explicitly select trials 1-5:
ravlt_trial_cols = []
for i in range(1, 6):
    col = f'RAVLT trial {i} score'
    if col in df.columns:
        ravlt_trial_cols.append(col)
```

**PREVENTION:** Be explicit about which columns to use, don't rely on sorting

---

### 7. Missing PYTHONPATH for Tool Imports (All Steps)

**BUG:** ModuleNotFoundError: No module named 'tools' when running scripts

**SYMPTOM:** Scripts fail immediately on import

**FIX:**
```bash
# Always set PYTHONPATH when running Ch7 scripts:
PYTHONPATH=/home/etai/projects/REMEMVR poetry run python -u script.py
```

**PREVENTION:** Either set PYTHONPATH in environment or add to sys.path in script

---

### 8. Statsmodels conf_int() Returns numpy array, not DataFrame (RQ 7.1.1 Step 05)

**BUG:** Trying to use .iloc on model.conf_int() output

**SYMPTOM:** AttributeError: 'numpy.ndarray' object has no attribute 'iloc'

**FIX:**
```python
# WRONG - assumes DataFrame:
'ci_lower': model.conf_int().iloc[i, 0],
'ci_upper': model.conf_int().iloc[i, 1],

# RIGHT - conf_int() returns (n_params, 2) numpy array:
conf_int = model.conf_int()
'ci_lower': conf_int[i, 0],  # i-th parameter, lower bound
'ci_upper': conf_int[i, 1],  # i-th parameter, upper bound
```

**PREVENTION:** Check return types of statsmodels methods before indexing

---

### 9. Regression Function Signature Mismatch (RQ 7.1.2 Step 04)

**BUG:** 4_analysis.yaml specifies `fit_multiple_regression(X, y, add_constant, return_diagnostics)` but actual function has `fit_multiple_regression(X, y, feature_names)`

**SYMPTOM:** g_code Layer 4b validation fails due to parameter name mismatch

**FIX:**
```python
# Create custom regression function with expected signature:
def fit_multiple_regression_custom(X, y, add_constant=True, return_diagnostics=True):
    # Custom implementation using statsmodels directly
    if add_constant:
        X_reg = sm.add_constant(X)
    else:
        X_reg = X
    
    model = sm.OLS(y, X_reg).fit()
    # Extract coefficients, VIF, etc. manually
    return results_dict
```

**PREVENTION:** Always verify function signatures match 4_analysis.yaml before generating code. Write custom implementations when mismatches found.

---

## DATA SOURCE REMINDERS FOR CH7

1. **NEVER use master.xlsx** - All Ch7 data is in dfnonvr.csv and dfdata.csv
2. **NART is in column 2** of dfnonvr.csv (not column 34 as old docs suggested)
3. **Column names are UPPERCASE** (UID not uid)
4. **STR questionnaire is in column 100** of dfnonvr.csv
5. **All cognitive test data is already extracted** - no need to parse master.xlsx

---

## VALIDATION BEST PRACTICES

1. **Always check actual files first** - Don't trust documentation blindly
2. **Verify function signatures** before using tools functions
3. **Check return value structure** of validation functions
4. **Handle multiple data formats** (dict vs string, uppercase vs lowercase)
5. **Use hierarchical paths** (results/ch7/7.X.Y/...) never flat paths

---

## COMMON CODE PATTERNS THAT WORK

### Loading Ch7 Data:
```python
# Cognitive test data
cognitive_df = pd.read_csv(PROJECT_ROOT / 'data' / 'dfnonvr.csv')

# Test-level data
test_df = pd.read_csv(PROJECT_ROOT / 'data' / 'dfdata.csv')

# Ch5 dependencies
theta_df = pd.read_csv(PROJECT_ROOT / 'results' / 'ch5' / '5.1.1' / 'data' / 'step03_theta_scores.csv')
```

### Path Setup:
```python
from pathlib import Path
import sys

# Project root from code file
PROJECT_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(PROJECT_ROOT))

# RQ directory
RQ_DIR = Path(__file__).resolve().parents[1]
LOG_FILE = RQ_DIR / "logs" / f"step{step_num:02d}_{step_name}.log"
OUTPUT_DIR = RQ_DIR / "data"
```

### Logging Pattern:
```python
def log(msg):
    """Write to both log file and console."""
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{msg}\n")
        f.flush()  # Critical for real-time monitoring
    print(msg, flush=True)  # -u flag compatibility
```

---

### 10. Regression Results Dictionary vs DataFrame Confusion (RQ 7.1.2 Step 03)

**BUG:** Code assumed regression results['coefficients'] returns DataFrame but it returns dict

**SYMPTOM:** AttributeError: 'dict' object has no attribute 'shape'

**FIX:** 
```python
# Wrong: assumes DataFrame
coefficients_df = regression_results['coefficients']
for idx, row in coefficients_df.iterrows():

# Correct: handle dict
coefficients = regression_results['coefficients']
for predictor in coefficients.keys():
    coef = coefficients[predictor]
```

**PREVENTION:** Check return types before processing

---

### 11. Incorrect Regression Results Key Names (RQ 7.1.2 Step 03)

**BUG:** Used wrong key names for regression results dictionary

**SYMPTOM:** KeyError when accessing 'r2', 'adj_r2', 'f_statistic', 'p_value'

**FIX:**
```python
# Wrong keys:
results['r2'], results['adj_r2'], results['f_statistic'], results['p_value']

# Correct keys:
results['rsquared'], results['rsquared_adj'], results['fvalue'], results['f_pvalue']
```

**PREVENTION:** Print available keys first: `print(regression_results.keys())`

---

### 12. DataFrame conf_int Indexing Error (RQ 7.1.2 Step 04)

**BUG:** Tried to index conf_int as numpy array when it's a DataFrame

**SYMPTOM:** KeyError: (0, 0) when accessing conf_int[i, 0]

**FIX:**
```python
# Wrong: conf_int[i, 0]
# Correct: conf_int.iloc[i, 0]
```

**PREVENTION:** Always use .iloc for positional DataFrame indexing

---

### 13. Missing Validation Function (RQ 7.1.2 Step 06)

**BUG:** 4_analysis.yaml specifies validate_hypothesis_test_dual_pvalues but function doesn't exist

**SYMPTOM:** ImportError or AttributeError

**FIX:** Either create custom validation or simplify:
```python
# Simple validation when function doesn't exist
expected_predictors = ['RAVLT_T', 'BVMT_T', 'RPM_T']
actual_predictors = df['predictor'].unique()
all_present = all(p in actual_predictors for p in expected_predictors)
```

**PREVENTION:** Check if validation functions exist before using

---

### 14. Validation Function Expects 'term' not 'predictor' Column (RQ 7.1.2 Step 06)

**BUG:** Validation function looks for 'term' column but dataframe has 'predictor' column

**SYMPTOM:** Validation fails with "Missing required terms"

**FIX:** Add compatibility column:
```python
significance_results['term'] = significance_results['predictor']
```

**PREVENTION:** Check what columns validation functions expect

---

## TO ADD AS YOU FIND MORE BUGS

When you encounter a new bug pattern:
1. Add it to the appropriate section above
2. Include: BUG description, SYMPTOM, FIX, and PREVENTION
3. Update the Last Updated date
4. Inform g_code to re-read this file for the latest lessons

This document grows with each RQ executed, making g_code increasingly effective.