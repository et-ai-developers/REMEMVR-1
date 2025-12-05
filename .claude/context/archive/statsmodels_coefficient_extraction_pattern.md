# Statsmodels Coefficient Extraction Pattern

**Topic:** Documentation of statsmodels LMM coefficient extraction patterns and common errors

**Archive Created:** 2025-12-05 14:45 (context-manager curation)

---

## [Coefficient Extraction Pattern - Fixed Effects Only] (2025-12-05 14:30)

**Archived from:** state.md Session (2025-12-05 14:30)
**Original Date:** 2025-12-05 14:30
**Reason:** Pattern documented for tool development reference

### Problem

**Statsmodels MixedLM Coefficient Arrays Include Random Effects:**

When extracting coefficients from statsmodels `MixedLMResults` objects:
- `model.params`: ALL parameters (fixed + random effects)
- `model.tvalues`: ALL t-statistics (fixed + random effects)
- `model.pvalues`: ALL p-values (fixed + random effects)

**Example RQ 5.5.4:**
- Model has 8 fixed effects + 3 random effects = 11 total parameters
- `model.params` returns 11 values (NOT 8)
- Indexing [0:8] would miss the last fixed effect

### Solution Pattern

**Slice to Fixed Effects Only Using `n_fe` attribute:**

```python
# Get number of fixed effects
n_fe = len(model.model.exog_names)  # OR model.k_fe

# Extract ONLY fixed effects
fixed_params = model.params[:n_fe]
fixed_tvalues = model.tvalues[:n_fe]
fixed_pvalues = model.pvalues[:n_fe]
```

**Rationale:**
- Random effects appear AFTER fixed effects in params array
- Slicing `[:n_fe]` extracts only fixed effects
- Prevents mixing fixed and random effect statistics

### Alternative: Use CSV Coefficients

**To avoid pickle loading errors:**

```python
# Save coefficients to CSV during model fitting
coefficients_df = pd.DataFrame({
    'term': model.model.exog_names,
    'estimate': model.params[:n_fe],
    'se': model.bse[:n_fe],
    't_value': model.tvalues[:n_fe],
    'p_value': model.pvalues[:n_fe]
})
coefficients_df.to_csv('step03_lmm_coefficients.csv', index=False)

# Load from CSV in downstream steps (avoids pickle)
coefficients = pd.read_csv('step03_lmm_coefficients.csv')
```

**Benefits:**
- Avoids statsmodels/patsy pickle loading errors
- Explicit fixed effects only (no slicing needed)
- Human-readable CSV format for transparency

### RQ 5.5.4 Application

**Bug Fixed in Step 3:**
```python
# WRONG: Would include random effects
all_params = model.params  # 11 values (8 fixed + 3 random)

# CORRECT: Fixed effects only
n_fe = len(model.model.exog_names)  # 8
fixed_params = model.params[:n_fe]  # 8 values only
```

**Bug Fixed in Step 5:**
```python
# WRONG: Pickle loading fails with patsy formula error
model_irt = pickle.load('step03_lmm_irt.pkl')

# CORRECT: Use CSV coefficients
coefficients_irt = pd.read_csv('step03_lmm_irt_coefficients.csv')
```

### Cross-RQ Pattern

**Applies to ALL LMM analyses:**
- RQ 5.5.2: Step 4 coefficient extraction (segment-location slopes)
- RQ 5.5.3: Step 3 interaction term extraction
- RQ 5.5.4: Step 3 parallel LMM coefficient extraction
- Future RQs with LMM coefficient comparisons

**Common Error Patterns:**
1. Using `model.params` directly without slicing
2. Loading pickled models in downstream steps (patsy errors)
3. Assuming coefficient array length equals number of fixed effects

### Tool Development Implications

**For `compare_lmm_coefficients()` tool:**
```python
def compare_lmm_coefficients(model1, model2):
    """Compare fixed effects coefficients between two LMMs.

    IMPORTANT: Extracts ONLY fixed effects, excludes random effects.
    """
    # Get number of fixed effects
    n_fe_1 = len(model1.model.exog_names)
    n_fe_2 = len(model2.model.exog_names)

    # Extract fixed effects only
    coeffs1 = model1.params[:n_fe_1]
    coeffs2 = model2.params[:n_fe_2]

    # Compare...
```

**For CSV export pattern:**
- Always export coefficients to CSV immediately after fitting
- Use CSV in all downstream steps (avoid pickle loading)
- Include term names for transparency

### Files Referenced

**RQ 5.5.4 Evidence:**
- results/ch5/5.5.4/code/step03_fit_parallel_lmms.py (n_fe slicing applied)
- results/ch5/5.5.4/code/step05_compare_fixed_effects.py (CSV loading pattern)
- results/ch5/5.5.4/data/step03_lmm_irt_coefficients.csv (exported CSV)

**Cross-References:**
- Archive: rq_5.5.2_complete_pipeline_execution_null_finding.md (2025-12-05 13:30: vcov matrix extraction)
- Archive: statsmodels_pickle_workaround_pattern.md (2025-12-05 13:30: patsy eval_env error)

---
