# Analysis Execution Report

**RQ:** X.Y - [RQ Title]
**Execution Date:** YYYY-MM-DD HH:MM
**Agent:** analysis_executor v2.0
**Report Version:** 1.0

---

## Executive Summary

**Status:** ✅ SUCCESS / ❌ FAILURE

**Analysis Steps Completed:** [N] / [N]

**Files Created:** [N] files (X CSVs + X companion .md + X plots + script)

**Execution Time:** [X minutes Y seconds]

**Convergence:** ✅ ALL MODELS CONVERGED / ⚠️ PARTIAL / ❌ NON-CONVERGENCE

---

## Execution Context

**Input Documents Read:**
- ✅ info.md (Section 4: Method)
- ✅ config.yaml (all sections)
- ✅ data/irt_input.csv (from data-prep agent)

**Working Directory:** `results/chX/rqY/`

---

## Analysis Pipeline Execution

### Step 1: IRT Calibration

**Status:** ✅ SUCCESS / ❌ FAILURE

**Tool Function:** `tools.analysis_irt.calibrate_grm()`

**Input:**
- File: data/irt_input.csv
- Dimensions: [N] rows × [N] columns
- Participants: [N]
- Items: [N]

**Parameters (from config.yaml):**
```yaml
model: "2PL-C"
dimensions: 3
purification: true
threshold_b: 3.0
threshold_a: 0.4
max_iterations: 200
convergence_tolerance: 0.001
```

**Execution:**
- **Pass 1:** Calibrate with all items
  - Iterations: [N] / 200
  - Convergence: ✅ YES (gradient < 0.001) / ❌ NO
  - Flagged items: [N] items ([list item codes])

- **Pass 2:** Re-calibrate without flagged items
  - Items included: [N] items
  - Iterations: [N] / 200
  - Convergence: ✅ YES / ❌ NO
  - Final item count: [N]

**Outputs Created:**
1. ✅ data/item_parameters.csv ([N] rows × [cols: item_code, dimension, a, b, flagged])
2. ✅ data/item_parameters.md
3. ✅ data/theta_scores.csv ([N] rows × [cols: UID, Test, Theta_Person, Theta_Place, Theta_Object])
4. ✅ data/theta_scores.md

**Quality Checks:**
| **Check** | **Threshold** | **Actual** | **Status** |
|-----------|--------------|-----------|-----------|
| Convergence | gradient < 0.001 | [X] | ✅ PASS / ❌ FAIL |
| Iterations | < 200 | [N] | ✅ PASS / ❌ FAIL |
| Discrimination Range | 0.4 ≤ a ≤ 3.0 | [min-max] | ✅ PASS / ❌ FAIL |
| Difficulty Range | -3.0 ≤ b ≤ 3.0 | [min-max] | ✅ PASS / ❌ FAIL |
| Flagging Rate | 5-15% | [X]% | ✅ PASS / ⚠️ WARNING |

**Execution Time:** [X minutes Y seconds]

**Issues:** [None / List any warnings or errors]

---

### Step 1a: IRT Validation

**Status:** ✅ COMPLETE / ⚠️ PARTIAL / ❌ FAILED

**Validation Tests:**

| **Assumption** | **Test** | **Threshold** | **Actual** | **Status** |
|---------------|---------|--------------|-----------|-----------|
| Local Independence | Q3 statistic | <0.2 | Max=[X] | ✅ PASS / ❌ FAIL |
| Unidimensionality | Eigenvalue ratio | >3.0 | [X] | ✅ PASS / ❌ FAIL |
| Model Fit (RMSEA) | M2 statistic | <0.08 | [X] | ✅ PASS / ❌ FAIL |
| Model Fit (CFI) | M2 statistic | >0.90 | [X] | ✅ PASS / ❌ FAIL |
| Item Fit | S-X² | p>0.01 | [N]/[N] pass | ✅ PASS / ❌ FAIL |

**Assumption Violations:** [None / List violations and how they were handled]

**Validation Results Appended to:** info.md - Section 5 (Validation)

---

### Step 2: Data Reshaping

**Status:** ✅ SUCCESS / ❌ FAILURE

**Tool Function:** `tools.data.reshape_wide_to_long()`

**Input:**
- File: data/theta_scores.csv
- Format: Wide (1 row per participant × test)
- Dimensions: [N] rows × [N] columns

**Parameters (from config.yaml):**
```yaml
id_var: "UID"
time_var: "Test"
value_vars: ["Theta_Person", "Theta_Place", "Theta_Object"]
var_name: "Domain"
value_name: "Theta"
```

**Process:**
1. Reshape theta_scores from wide to long format
2. Create Domain factor variable (Person, Place, Object)
3. Add Day variable (map Test → Day: 1→0, 2→0, 3→1, 4→7)

**Output Created:**
1. ✅ data/lmm_input.csv ([N] rows × [cols: UID, Test, Day, Domain, Theta])
2. ✅ data/lmm_input.md

**Quality Checks:**
| **Check** | **Expected** | **Actual** | **Status** |
|-----------|------------|-----------|-----------|
| Rows | 1,200 (400 × 3) | [N] | ✅ PASS / ❌ FAIL |
| Columns | 5 | [N] | ✅ PASS / ❌ FAIL |
| Missing Values | 0 | [N] | ✅ PASS / ⚠️ WARNING |
| Domain Levels | 3 | [N] | ✅ PASS / ❌ FAIL |

**Execution Time:** [X seconds]

**Issues:** [None / List any warnings]

---

### Step 3: LMM Analysis

**Status:** ✅ SUCCESS / ❌ FAILURE

**Tool Function:** `tools.analysis_lmm.fit_lmm()`

**Input:**
- File: data/lmm_input.csv
- Dimensions: [N] rows × [N] columns

**Parameters (from config.yaml):**
```yaml
formula: "Theta ~ Domain * Day + (1 + Day | UID)"
method: "REML"
optimizer: "lbfgs"
max_iterations: 100
```

**Execution:**
- Iterations: [N] / 100
- Convergence: ✅ YES / ❌ NO
- Fallback used: ❌ NO (original model converged) / ⚠️ YES (used random intercepts only)

**Fixed Effects Results:**

| **Effect** | **Coefficient** | **SE** | **t** | **p** | **95% CI** |
|-----------|----------------|--------|-------|-------|------------|
| Intercept | [X] | [X] | [X] | [X] | [[lower], [upper]] |
| Domain_Place | [X] | [X] | [X] | [X] | [[lower], [upper]] |
| Domain_Object | [X] | [X] | [X] | [X] | [[lower], [upper]] |
| Day | [X] | [X] | [X] | [X] | [[lower], [upper]] |
| Domain_Place × Day | [X] | [X] | [X] | [X] | [[lower], [upper]] |
| Domain_Object × Day | [X] | [X] | [X] | [X] | [[lower], [upper]] |

**Random Effects Results:**
- Intercept SD: [X]
- Slope SD: [X]
- Intercept-Slope Correlation: [X]

**Model Fit:**
- AIC: [X]
- BIC: [X]
- Log-likelihood: [X]
- ICC: [X]

**Effect Sizes:**
- Domain×Day interaction: Cohen's f² = [X], 95% CI [[lower], [upper]]
- Interpretation: [small/medium/large effect]

**Outputs Created:**
1. ✅ data/lmm_coefficients.csv
2. ✅ data/lmm_coefficients.md
3. ✅ data/lmm_random_effects.csv
4. ✅ data/lmm_random_effects.md

**Execution Time:** [X minutes Y seconds]

**Issues:** [None / List any convergence issues or fallback usage]

---

### Step 3a: LMM Validation

**Status:** ✅ COMPLETE / ⚠️ PARTIAL / ❌ FAILED

**Validation Tests:**

| **Assumption** | **Test** | **Threshold** | **Actual** | **Status** |
|---------------|---------|--------------|-----------|-----------|
| Residual Normality | Shapiro-Wilk | p>0.05 | p=[X] | ✅ PASS / ❌ FAIL |
| Homoscedasticity | Levene's test | p>0.05 | p=[X] | ✅ PASS / ❌ FAIL |
| Independence | Durbin-Watson | 1.5-2.5 | [X] | ✅ PASS / ❌ FAIL |
| Multicollinearity | VIF | <10.0 | Max=[X] | ✅ PASS / ❌ FAIL |

**Diagnostic Plots Created:**
- ✅ Residuals vs Fitted (saved in plots/lmm_diagnostics_residuals.png)
- ✅ Q-Q Plot (saved in plots/lmm_diagnostics_qq.png)

**Assumption Violations:** [None / List violations and how they were handled]

**Validation Results Appended to:** info.md - Section 5 (Validation)

---

### Step 4: Plot Generation

**Status:** ✅ SUCCESS / ❌ FAILURE

**Plot 1: IRT Item Characteristic Curves**
- **Tool:** `tools.plotting.plot_icc()`
- **Input:** data/item_parameters.csv
- **Output:** ✅ plots/irt_icc_by_domain.png, plots/irt_icc_by_domain_data.csv
- **Execution Time:** [X seconds]

**Plot 2: LMM Forgetting Trajectories**
- **Tool:** `tools.plotting.plot_lmm_trajectories()`
- **Input:** data/lmm_coefficients.csv, data/lmm_input.csv
- **Output:** ✅ plots/lmm_trajectories_by_domain.png, plots/lmm_trajectories_by_domain_data.csv
- **Execution Time:** [X seconds]

**Plot 3: LMM Random Effects**
- **Tool:** `tools.plotting.plot_random_effects()`
- **Input:** data/lmm_random_effects.csv
- **Output:** ✅ plots/lmm_random_effects.png, plots/lmm_random_effects_data.csv
- **Execution Time:** [X seconds]

**Issues:** [None / List any plotting errors]

---

## Tool Usage Summary

**Tools Used:**

| **Step** | **Tool Function** | **Version** | **Status** | **Duration** |
|----------|-------------------|-----------|-----------|-------------|
| 1 | tools.analysis_irt.calibrate_grm | [X.Y.Z] | ✅ SUCCESS | [X]min |
| 2 | tools.data.reshape_wide_to_long | [X.Y.Z] | ✅ SUCCESS | [X]sec |
| 3 | tools.analysis_lmm.fit_lmm | [X.Y.Z] | ✅ SUCCESS | [X]min |
| 4a | tools.plotting.plot_icc | [X.Y.Z] | ✅ SUCCESS | [X]sec |
| 4b | tools.plotting.plot_lmm_trajectories | [X.Y.Z] | ✅ SUCCESS | [X]sec |
| 4c | tools.plotting.plot_random_effects | [X.Y.Z] | ✅ SUCCESS | [X]sec |

**Custom Functions Used:** ❌ NONE (all tools from tools/ package) ✅

**Improvisation:** ❌ NONE (strict tool-only execution) ✅

---

## Files Created Summary

**Total Files:** [N]

**Data Files (data/):**
1. ✅ item_parameters.csv + item_parameters.md
2. ✅ theta_scores.csv + theta_scores.md
3. ✅ lmm_input.csv + lmm_input.md
4. ✅ lmm_coefficients.csv + lmm_coefficients.md
5. ✅ lmm_random_effects.csv + lmm_random_effects.md

**Plot Files (plots/):**
1. ✅ irt_icc_by_domain.png + irt_icc_by_domain_data.csv
2. ✅ lmm_trajectories_by_domain.png + lmm_trajectories_by_domain_data.csv
3. ✅ lmm_random_effects.png + lmm_random_effects_data.csv
4. ✅ lmm_diagnostics_residuals.png + lmm_diagnostics_residuals_data.csv
5. ✅ lmm_diagnostics_qq.png + lmm_diagnostics_qq_data.csv

**Code Files (code/):**
1. ✅ analysis_script.py (reproducible analysis script)

**Companion .md Files:** ✅ ALL CSVs have companion .md ✅

---

## Next Steps for Results-Inspector

**Analysis Complete:** All steps executed successfully

**Validation Complete:** All assumptions checked, violations documented

**Ready for Results Validation:** ✅ YES

**Recommended Actions:**
1. Review all outputs for statistical correctness
2. Verify effect sizes and confidence intervals
3. Check interpretation aligns with results
4. Update info.md Section 8 (Results) with findings
5. Invoke scholar agent for Section 9 (Theoretical Implications)

**Warnings:**
- [Any issues results-inspector should be aware of]

---

## Failure Report (If Status = FAILURE)

[Only include this section if execution failed]

**Error Type:** [ConvergenceFailure / MissingTool / DataError / UnexpectedError]

**Error Message:** [Full error message]

**Failure Location:** [Which step failed]

**Root Cause:** [Analysis of what went wrong]

**Required Action:** [What needs to be fixed before re-running]

**Tool Missing Details (if MissingTool error):**
- **Missing Tool:** [Function name]
- **Required For:** [Which step]
- **Specifications:** [What the tool should do]
- **Recommendation:** Implement tool, then re-run analysis-executor

---

## Execution Metadata

**Agent Version:** analysis_executor v2.0 (strict tool-only, no improvisation)
**Invocation Command:** [How agent was invoked]
**Execution Start:** YYYY-MM-DD HH:MM:SS
**Execution End:** YYYY-MM-DD HH:MM:SS
**Total Duration:** [X minutes Y seconds]
**Python Version:** [X.Y.Z]
**Poetry Environment:** [Environment name]
**Tools Package Version:** [X.Y.Z]
**Tests Passing:** 49/49 ✅

---

**End of Analysis Execution Report**
