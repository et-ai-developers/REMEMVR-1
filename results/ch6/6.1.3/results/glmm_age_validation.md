# GLMM Validation: Age Effects on Confidence

## Research Question
**RQ 6.1.3:** Does age affect baseline confidence or confidence decline rate?

## Methods Comparison

| Aspect | IRT → LMM | GLMM (this validation) |
|--------|-----------|------------------------|
| **Approach** | Two-stage (GRM → LMM) | Single-stage GEE |
| **Outcome** | Theta scores (continuous) | Ordinal ratings (5-level) |
| **Error structure** | Gaussian | Quasi-continuous + Binomial GEE |
| **N observations** | 400 (aggregated) | 28,800 (item-level) |
| **Time variable** | Time_log | log(TSVR_hours) |
| **Age predictor** | Age_c (centered) | Age_c (centered at 44.57) |

## Key Results

### Age x Time Interaction (The Critical Test)

| Method | β (Age×Time) | SE | p-value | Conclusion |
|--------|--------------|----|---------|-----------|
| GEE Continuous | 0.000186 | 0.000180 | 0.302142 | NULL |
| GEE Binomial | 0.001202 | 0.001089 | 0.269640 | NULL |
| IRT → LMM | 0.000675 | 0.000683 | 0.323176 | NULL |

### Age Main Effect

| Method | β (Age_c) | SE | p-value | Conclusion |
|--------|-----------|----|---------|-----------|
| GEE Continuous | -0.002102 | 0.001101 | 0.056157 | NULL |
| GEE Binomial | -0.015085 | 0.007380 | 0.040962 | SIGNIFICANT |
| IRT → LMM | -0.005246 | 0.003415 | 0.124524 | NULL |

## Conclusion

**The NULL Age x Time interaction is ROBUST to methodological choice.**

All three approaches (IRT→LMM, GEE Continuous, GEE Binomial) find:
- **No significant Age x Time interaction** - Confidence decline rate is age-invariant
- This validates the IRT→LMM result using a completely different methodology
- Direct item-level GLMM with 28,800 observations confirms the 400-observation IRT→LMM finding

**Theoretical Implication:** Metacognitive monitoring (confidence) parallels memory accuracy (Ch5).
Both show age-invariant decline under VR ecological encoding.
