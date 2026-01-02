# RQ Planner Improvements Summary

**Date:** 2026-01-02
**Context:** Based on review of Ch7 7.1.X plans, systematic issues were identified and fixed

## Issues Identified in Current Plans

### 1. Statistical Implementation Details Missing

**Problem:** Plans were vague about implementation specifics
- No random seeds specified → reproducibility issues
- Bootstrap iterations not specified → inconsistent results  
- Cross-validation details missing → implementation guesswork
- Power analysis parameters unclear → incorrect calculations

**Solution:** Mandatory specification requirements added for:
- Random seeds (always seed=42)
- Bootstrap iterations (default 1000)
- CV folds and strategy (5-fold with shuffle=True)
- Power analysis software and parameters

### 2. Remedial Actions Not Specified

**Problem:** Plans checked assumptions but didn't say what to do if violated
- Normality violations → ?
- Heteroscedasticity → ?
- Multicollinearity → ?
- Outliers → ?

**Solution:** Standard remedial action framework:
- Normality: Bootstrap CIs or transformation
- Heteroscedasticity: HC3 robust standard errors
- Multicollinearity: Ridge regression if VIF > 10
- Outliers: Report with/without if Cook's D > 4/n

### 3. Cross-RQ Dependencies Too Rigid

**Problem:** Hard-coded file paths that might not exist
- Assumed Ch5 outputs have specific names
- No fallback if naming convention different
- Would fail if file structure varies

**Solution:** Flexible dependency specification:
```markdown
- Primary: results/ch5/5.1.1/data/step05_lmm_model.txt
- Alternative: results/ch5/5.1.1/data/lmm_fitted.rds
- Fallback: results/ch5/5.1.1/data/*lmm*.{txt,rds,csv}
```

### 4. Multiple Comparison Corrections Inconsistent

**Problem:** Confusion about correction levels
- Some used within-RQ families
- Some used chapter-level
- Bonferroni calculations varied

**Solution:** Explicit family definition required:
- State family scope (within-RQ, within-theme, chapter)
- Show calculation (e.g., 3 predictors × 2 models = 6 tests)
- Always report dual p-values (Decision D068)

### 5. Validation Requirements Incomplete

**Problem:** Not all steps had full 4-layer validation
- Some missing value ranges
- Some missing log patterns
- Inconsistent structure

**Solution:** Mandatory 4-layer structure with exact headers:
1. *Output Files:* (paths, dimensions, types)
2. *Value Ranges:* (scientific bounds)
3. *Data Quality:* (missing data, duplicates)
4. *Log Validation:* (required/forbidden patterns)

### 6. Step 0 Often Missing

**Problem:** Plans jumped straight into analysis without checking prerequisites
- Dependencies not validated
- Missing files discovered late
- Wasted computation time

**Solution:** Step 0 now mandatory for all plans:
- Validates cross-RQ dependencies
- Checks prerequisites
- Verifies data accessibility
- Fails fast if requirements not met

## Files Created/Updated

### 1. docs/v4/templates/plan_v4.3.md (NEW)
Enhanced template with:
- Statistical implementation requirements section
- Mandatory specification checklists
- Example implementations for CV, bootstrap, power
- Remedial action framework
- Cross-RQ dependency patterns

### 2. .claude/agents/rq_planner_v5.1.md (NEW)
Updated agent specification with:
- Mandatory statistical specifications
- Common issues to avoid section
- Complete example of properly specified step
- Success criteria checklist
- Enhanced workflow instructions

### 3. docs/v4/rq_planner_improvements_summary.md (THIS FILE)
Documentation of:
- Issues identified
- Solutions implemented
- Examples of proper specifications
- Migration guide for existing plans

## Examples of Improved Specifications

### Before (Vague):
```markdown
**Processing:**
- Implement cross-validation
- Bootstrap confidence intervals
- Check assumptions
```

### After (Specific):
```markdown
**Processing:**
- Implement 5-fold cross-validation:
  - sklearn.model_selection.KFold
  - Random seed: 42
  - Shuffle: True
  - Train-test split: 80/20 per fold
  - Flag if train-test R² gap > 0.10
- Bootstrap 95% CIs:
  - Iterations: 1000
  - Seed: 42
  - Participant-level resampling
  - Percentile method (2.5th, 97.5th)
- Check assumptions:
  - Normality: Shapiro-Wilk (p > 0.05)
  - If violated: Use bootstrap CIs
  - Homoscedasticity: Breusch-Pagan
  - If violated: Report HC3 robust SEs
```

## Impact on Downstream Agents

### rq_tools
- Can now select exact implementation functions
- Knows which packages to import
- Can specify exact parameters

### rq_analysis
- Can generate precise function calls
- Knows iteration counts and seeds
- Can implement remedial logic

### g_code
- Can generate reproducible code
- Implements consistent error handling
- Applies remedial actions automatically

### rq_inspect
- Has clear validation criteria
- Knows expected patterns
- Can verify reproducibility

## Migration Guide for Existing Plans

To update existing plans to v5.1 standard:

1. **Add Step 0** for dependency validation
2. **For each statistical procedure, add:**
   - Random seed (42)
   - Iteration count (bootstrap: 1000, CV: 5-fold)
   - Specific implementation (package.function)
3. **For each assumption check, add:**
   - Test to use (Shapiro-Wilk, Breusch-Pagan, VIF)
   - Threshold (p > 0.05, VIF < 10)
   - Remedial action if violated
4. **For cross-RQ dependencies, add:**
   - Fallback paths or search patterns
5. **For each step, ensure:**
   - 4-layer validation with exact headers
   - Expected behavior on failure

## Benefits of These Improvements

1. **Reproducibility:** Seed=42 ensures identical results across runs
2. **Robustness:** Remedial actions handle real-world data issues
3. **Flexibility:** Fallback paths prevent dependency failures
4. **Clarity:** Downstream agents know exactly what to implement
5. **Quality:** 4-layer validation catches issues early
6. **Efficiency:** Step 0 fails fast if prerequisites missing

## Next Steps

1. Re-run rq_planner on any RQs that need updated plans
2. New RQs will automatically use enhanced template
3. Downstream agents already compatible with enhanced format
4. No code changes needed in rq_tools/rq_analysis/g_code

---

**Conclusion:** The enhanced rq_planner (v5.1) and plan template (v4.3) address all systematic issues found in Ch7 plans, ensuring complete and reproducible statistical specifications for all future analysis plans.