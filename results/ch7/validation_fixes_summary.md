# Ch7 7.1.X Validation Fixes Summary

**Date:** 2026-01-02
**Context:** Addressed statistical validation issues identified by rq_stats for RQs 7.1.1, 7.1.2, and 7.1.4

## Issues Identified and Fixed

### RQ 7.1.1 (CONDITIONAL - Score 8.3/10)

**Issues:**
1. Missing regression tool specifications
2. No remedial actions for assumption violations

**Fixes Applied:**
- Added detailed remedial actions in Step 4 for each assumption violation type
- Specified tool requirements in Step 5 (statsmodels.OLS, assumption checking functions)
- Corrected Bonferroni to within-RQ family (α = 0.05/4 = 0.0125)
- Added 5-fold cross-validation in Step 8
- Added bootstrap CIs for all coefficients (1000 replications)

---

### RQ 7.1.2 (REJECTED - Score 7.9/10)

**Critical Issues:**
1. Bonferroni calculation error (was 0.000597, should consider 6 tests)
2. BLUP extraction bias not acknowledged
3. Missing bootstrap methodology details
4. Two-stage analysis limitations not discussed

**Fixes Applied:**
- **Step 3:** Corrected Bonferroni for 3 predictors × 2 models = 6 tests (α = 0.05/6 = 0.0083)
- **Step 4:** Added CRITICAL note about BLUP shrinkage bias and sensitivity analysis suggestion
- **Step 5:** Specified participant-level block bootstrap (1000 reps) preserving correlation structure
- **Step 5:** Added alternative simultaneous modeling approach to avoid two-stage bias
- **Step 6:** Added comprehensive limitations section documenting two-stage analysis bias (Hanusz & Tarasińska, 2015)
- Added Decision D068 compliance (dual p-value reporting)

---

### RQ 7.1.4 (REJECTED - Score 8.1/10)

**Critical Issues:**
1. Missing cross-validation strategy
2. No power analysis
3. No remedial actions for violations

**Fixes Applied:**
- **Step 3:** Added MANDATORY 5-fold cross-validation with train-test gap threshold (<0.10)
- **Step 4:** Added post-hoc power analysis and sensitivity analysis for f²
- **Step 6:** Added comprehensive remedial actions:
  - Robust SEs for normality violations
  - HC3 SEs for heteroscedasticity
  - Ridge regression for multicollinearity
  - Outlier reporting with/without influential points
- Updated critical notes to emphasize cross-validation and power analysis requirements

---

## Key Methodological Improvements

### 1. Bonferroni Correction Standardization
- Within-RQ families rather than extreme chapter-level correction
- Dual p-value reporting (Decision D068) emphasized throughout

### 2. BLUP/Two-Stage Analysis
- Acknowledged shrinkage bias inherent in BLUP extraction
- Suggested simultaneous modeling as primary analysis
- Referenced Hanusz & Tarasińska (2015) on two-stage bias

### 3. Cross-Validation
- 5-fold CV now mandatory for all predictive models
- Train-test gap threshold: <0.10 for acceptable generalization

### 4. Power Analysis
- Post-hoc power for each incremental block
- Sensitivity analysis for minimum detectable effects
- Acknowledgment when underpowered

### 5. Remedial Actions Framework
Standardized approach for assumption violations:
- Normality → Robust SEs or bootstrap
- Heteroscedasticity → HC3 SEs
- Multicollinearity → Ridge regression
- Outliers → Report with/without

---

## Implementation Notes

### Tools Required
The fixes assume availability of:
- `tools.analysis_regression` module (to be created)
- Bootstrap functions for CIs and p-values
- Cross-validation utilities
- Power analysis functions

### Data Flow
All Ch7 RQs now follow standardized output structure:
- CSV files in `data/` folder (step##_*.csv)
- Summary documents in `results/` folder (.md files)
- Plots in `plots/` folder
- No CSV files in `results/` folder

---

## Next Steps

1. Re-run rq_stats on the updated concept files to verify fixes
2. Proceed to rq_planner for 7.1.X RQs
3. Create remaining 24 concept files for Ch7 RQs
4. Implement tools.analysis_regression module before execution

---

## References from Context Research

Based on context_finder research of Ch5/Ch6 implementations:

- **Bonferroni:** Decision D068 requires dual p-value reporting (uncorrected AND corrected)
- **BLUP bias:** Known issue, addressed via model averaging in Ch5 (ICC from 0.05% to 21.61%)
- **Cross-validation:** Used successfully in Ch6 clustering (Jaccard >0.75 for stability)
- **Power analysis:** Ch6 null findings all adequately powered (84-97% for d=0.30)
- **Model averaging:** Burnham & Anderson (2002) approach when competitive models exist
- **TSVR:** Decision D070 - use actual delay periods, not nominal days

These precedents informed the systematic fixes applied to Ch7 concepts.