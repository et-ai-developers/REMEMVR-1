# RQ 6.7.2 Robustness Analysis

**Generated:** 2025-12-13T16:02:49.999982
**Task:** T1.2 from rq_rework.md - Bootstrap robustness for marginal p-value

---

## Original Finding

| Metric | Value |
|--------|-------|
| Partial r | 0.2135 |
| p-value | 0.0329 |
| Finding | SD_confidence → SD_accuracy \| mean_accuracy |

---

## Robustness Tests

### 1. Bootstrap 95% CI (N=10,000)

| Metric | Value |
|--------|-------|
| CI Lower | 0.0213 |
| CI Upper | 0.4060 |
| CI Excludes 0 | Yes ✓ |
| Bootstrap Mean | 0.2146 |
| Bootstrap SD | 0.0998 |

### 2. Leave-One-Out (N=100)

| Metric | Value |
|--------|-------|
| LOO Mean | 0.2135 |
| LOO SD | 0.0105 |
| LOO Range | [0.1634, 0.2727] |
| N Positive | 100 |
| N Negative | 0 |
| All Same Direction | Yes ✓ |

Most influential observation: A100 (LOO r = 0.2727)

### 3. Permutation Test (N=1,000)

| Metric | Value |
|--------|-------|
| p_permutation | 0.0310 |
| p_parametric | 0.0329 |
| Confirms Parametric | Yes ✓ |
| Null Mean | -0.0021 |
| Null SD | 0.0958 |

### 4. Outlier Sensitivity

| Metric | Value |
|--------|-------|
| Threshold | 2.5 SD |
| N Outliers | 7 |
| Original r | 0.2135 |
| Clean r | 0.1495 |
| Delta r | -0.0640 |
| Robust | No ✗ |

---

## Overall Assessment

**Robustness Score:** 3/4 criteria passed

| Criterion | Status |
|-----------|--------|
| Bootstrap CI excludes 0 | ✓ |
| LOO all same direction | ✓ |
| Permutation p < 0.05 | ✓ |
| Robust to outliers | ✗ |

**Overall:** SUBSTANTIALLY ROBUST

**Interpretation:** Finding passes most checks. p=0.034 is reasonably trustworthy.

---

## Files Created

- `data/step06_bootstrap_results.csv`
- `data/step06_loo_results.csv`
- `data/step06_permutation_results.csv`
- `data/step06_outlier_sensitivity.csv`
- `results/robustness_analysis.md` (this file)
