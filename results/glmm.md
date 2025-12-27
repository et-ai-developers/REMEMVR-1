# GLMM Validation Summary

Cross-validation of IRT→LMM findings using single-stage GLMM on item-level data.

## RQs Validated

| RQ | Question | IRT→LMM | GLMM | Agreement |
|----|----------|---------|------|-----------|
| **5.1.3** | Age × Time (slope) | NULL (p=.76) | NULL (p=.46) | ✓ |
| **5.1.3** | Age intercept | Marginal (p=.06) | **SIG (p=.01)** | ⚠️ GLMM stronger |
| **5.4.1** | Congruence × Time | NULL | NULL | ✓ |
| **5.4.1** | Congruent intercept | NULL (p=.55) | **SIG (p=.01)** | ⚠️ GLMM stronger |
| **5.4.3** | Age × Congruence × Time | NULL | NULL | ✓ |
| **6.1.1** | Time effect | SIG | SIG | ✓ |
| **6.1.3** | Age × Time (slope) | NULL (p=.32) | NULL (p=.27-.30) | ✓ |
| **6.1.3** | Age intercept | NULL (p=.12) | Marginal (p=.04-.06) | ⚠️ GLMM stronger |

## Key Discrepancies

**Pattern:** GLMM consistently finds *stronger* intercept effects than IRT→LMM, while trajectory (slope) findings always agree.

| Effect Type | IRT→LMM vs GLMM |
|-------------|-----------------|
| **Slopes/interactions** | Always agree |
| **Intercepts** | GLMM sometimes stronger |

### Specific Discrepancies

1. **Age intercept (5.1.3):** IRT→LMM p=.061, GLMM p=.014
2. **Congruent intercept (5.4.1):** IRT→LMM p=.548, GLMM p=.011
3. **Age intercept (6.1.3):** IRT→LMM p=.125, GLMM-Binomial p=.041

## Interpretation

The discrepancies are in **intercepts, not slopes**. This likely reflects:
- IRT aggregation smooths out baseline differences
- GLMM with 28,800+ observations has more power for intercept detection
- Slope effects require detecting *change over time*, which both methods capture similarly

**Bottom line:** All trajectory-related hypotheses (Age×Time, Congruence×Time) are robust. Some baseline effects may be real but small.
