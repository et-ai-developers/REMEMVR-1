# Statsmodels Pickle Workaround Pattern

**Topic:** statsmodels_pickle_workaround_pattern
**Created:** 2025-12-05 (context-manager archival)
**Description:** Workaround pattern for statsmodels/patsy pickle loading errors (f_locals eval_env failures).

---

## Patsy Eval_Env Error on Pickle Load - Export Coefficients CSV Instead (2025-12-05 13:30)

**Archived from:** state.md Session (2025-12-05 13:30)
**Original Date:** 2025-12-05 13:30
**Reason:** Pattern documented, applies to all LMM steps needing loaded models

### Problem

**Error:** patsy.eval.EvalEnvironment f_locals=None when loading pickled statsmodels MixedLM models

**Symptom:** Loading a previously fitted LMM model from pickle file fails with patsy evaluation error, preventing access to model attributes like coefficients, p-values, etc.

**Root Cause:** Patsy formula environment cannot be reconstructed from pickle (eval_env relies on execution context that doesn't survive serialization).

### Solution: Export Coefficients CSV Instead

**Pattern:** Instead of loading the pickled model to extract coefficients/statistics:

1. **During model fitting:** Immediately after fitting, extract and export all needed statistics to CSV:
   ```python
   # Right after model.fit()
   coef_df = pd.DataFrame({
       'term': model.model.exog_names,
       'coefficient': model.params,
       't_value': model.tvalues,
       'p_value': model.pvalues
   })
   coef_df.to_csv('step03_coefficients.csv', index=False)
   ```

2. **In downstream steps:** Read from CSV instead of loading pickle:
   ```python
   # INSTEAD OF: model = pickle.load(f)
   coef_df = pd.read_csv('step03_coefficients.csv')
   interaction_coef = coef_df[coef_df['term'].str.contains('Days_within:Segment:LocationType')]
   ```

### When This Applies

- **ALL LMM steps needing loaded models** for coefficient extraction
- Especially steps that:
  - Extract interaction terms (Step 6 in RQ 5.5.2)
  - Compute contrasts from model coefficients
  - Test specific hypothesis about fixed effects

### Alternative (Less Robust)

Monkey-patch the model's __setstate__ to bypass patsy formula re-evaluation:
```python
def custom_setstate(self, state):
    self.__dict__.update(state)
    # Skip patsy formula reconstruction

model.__class__.__setstate__ = custom_setstate
```

**Not recommended:** Fragile, only works for variance extraction, fails for coefficient access.

### Lessons Learned

- Pickle is NOT reliable for statsmodels LMM models with patsy formulas
- Export all needed information to CSV immediately after fitting
- CSV approach is cleaner, more transparent, and debugging-friendly
- This pattern emerged from RQ 5.5.2 Step 6 (test interaction) failure

### Related

- See also: `statsmodels_coefficient_extraction_pattern.md` for coefficient slicing
- See also: RQ 5.5.4 uses this pattern extensively

---
