# GLMM vs IRT → LMM Comparison: Age × Congruence Interactions (RQ 5.4.3)

## Research Question
**RQ 5.4.3:** Does the effect of age on forgetting rate vary by schema congruence level?

## Methods Comparison

| Aspect | IRT → LMM | GLMM (this analysis) |
|--------|-----------|---------------------|
| **Approach** | Two-stage (IRT → LMM) | Single-stage |
| **Outcome** | Theta scores | Binary responses (0/1) |
| **N observations** | 1,200 | 28,800 |
| **Time model** | Recip + Log | Log only |
| **Age variable** | Age_c (M = 44.6) | Age_c (M = 44.6) |

## Key Results: 3-Way Age × Congruence × Time Interactions

| Interaction | IRT → LMM | GLMM |
|-------------|-----------|------|
| Age × Congruent × Time (recip) | β = -0.067, p = .124 | — |
| Age × Congruent × Time (log) | β = -0.007, p = .179 | β = 0.001707, p = 0.2445 |
| Age × Incongruent × Time (recip) | β = 0.022, p = .609 | — |
| Age × Incongruent × Time (log) | β = 0.004, p = .526 | β = 0.001619, p = 0.1293 |

## 2-Way Interactions

| Effect | GLMM β | GLMM p |
|--------|--------|--------|
| Age × Time (overall) | -0.000441 | 0.6658 |
| Time × Congruent | -0.021704 | 0.3201 |
| Time × Incongruent | -0.010954 | 0.5023 |
| Age × Congruent | -0.003964 | 0.4624 |
| Age × Incongruent | -0.006032 | 0.1694 |

## Main Effects

| Effect | GLMM β | GLMM p |
|--------|--------|--------|
| Time (log_TSVR) | -0.10509 | 0.000000 |
| Age (Age_c) | -0.003205 | 0.4669 |
| Congruent (vs Common) | 0.19576 | 0.0105 |
| Incongruent (vs Common) | -0.07651 | 0.2427 |

## Accuracy by Age Tertile × Congruence

| Age Group | Common | Congruent | Incongruent |
|-----------|--------|-----------|-------------|
| Young | 0.522 | 0.544 | 0.491 |
| Middle | 0.466 | 0.497 | 0.447 |
| Older | 0.476 | 0.516 | 0.443 |

## Conclusion

**3-Way Age × Congruence × Time Interactions:**
- Congruent: p = 0.2445 (NOT significant)
- Incongruent: p = 0.1293 (NOT significant)

**The GLMM CONFIRMS the IRT → LMM null findings:**
Age effects on forgetting rate do NOT vary significantly by schema congruence level.
