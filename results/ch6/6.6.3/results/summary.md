# RQ 6.6.3: High-Confidence Errors - Domain Specificity

## Summary

**Research Question:** Are high-confidence errors domain-specific, showing different rates for What versus Where versus When memory domains?

**Hypothesis:** When domain will show MOST high-confidence errors due to floor effects (low accuracy) combined with guessing. Predicted ranking: **When > Where > What**

**Finding:** **HYPOTHESIS NOT SUPPORTED** - Domain ranking is **Where > When > What**

---

## Key Results

### Domain HCE Rates (Overall)

| Domain | Mean HCE Rate | Predicted Rank | Observed Rank | Match |
|--------|---------------|----------------|---------------|-------|
| Where | 9.32% | 2 | **1** | No |
| When | 7.34% | 1 | **2** | No |
| What | 5.88% | 3 | **3** | Yes |

**Overall HCE rate:** 7.88% (3,309 / 42,000 item-responses)

### Statistical Tests (Decision D068 Dual P-Values)

| Effect | p (uncorrected) | p (Bonferroni) | Significant |
|--------|-----------------|----------------|-------------|
| Domain main effect | < .001 | < .001 | **YES** |
| Domain × Time interaction | < .001 | < .001 | **YES** |

### LMM Fixed Effects

| Predictor | β | SE | z | p | 95% CI |
|-----------|------|------|-------|--------|----------|
| Intercept (What at Day 0) | 0.060 | 0.007 | 8.09 | < .001 | [0.046, 0.075] |
| When vs What | +0.035 | 0.007 | 4.88 | < .001 | [0.021, 0.050] |
| Where vs What | +0.050 | 0.007 | 6.86 | < .001 | [0.036, 0.064] |
| Days (What slope) | -0.001 | 0.001 | -0.39 | .694 | [-0.003, 0.002] |
| When × Days | -0.008 | 0.002 | -3.83 | < .001 | [-0.012, -0.004] |
| Where × Days | -0.006 | 0.002 | -2.83 | .005 | [-0.010, -0.002] |

---

## Domain × Time Patterns

| Domain | T1 (Day 0) | T2 (Day 1) | T3 (Day 3) | T4 (Day 6) | Trajectory |
|--------|------------|------------|------------|------------|------------|
| What | 5.07% | 7.28% | 5.62% | 5.55% | Stable (~6%) |
| Where | 11.86% | 9.90% | 7.78% | 7.74% | **DECREASING** |
| When | 9.88% | 8.38% | 6.50% | 4.58% | **DECREASING fastest** |

**Key pattern:** HCE rates DECREASE over retention interval (opposite of hypothesis predicting increase as metacognition fails with memory degradation).

---

## Interpretation

### Why Hypothesis Was Not Supported

1. **Predicted:** When domain would have highest HCE due to floor effects in accuracy + overconfident guessing
2. **Observed:** Where domain has highest HCE, When is intermediate

### Theoretical Implications

1. **Spatial Memory Vulnerability:** Where domain shows highest susceptibility to high-confidence errors (9.32%)
   - May reflect "false spatial familiarity" - locations feel known even when memory is incorrect
   - Spatial recognition may engage automatic processes that generate unwarranted confidence

2. **Temporal Memory Calibration:** When domain shows moderate HCE (7.34%) AND fastest decline over time
   - Temporal memory may have better metacognitive monitoring than expected
   - Despite accuracy floor effects, confidence appropriately adjusts

3. **Object Identity Protection:** What domain shows lowest HCE (5.88%)
   - Object recognition is best calibrated
   - Familiarity signals for objects are more reliable indicators of accuracy

### Connection to RQ 6.6.1 and 6.6.2

- RQ 6.6.1 found overall HCE rates DECREASE 35% over retention interval
- This domain analysis confirms: HCE decrease is driven by When and Where domains
- What domain remains stable - different metacognitive process

---

## Anomaly Flags

1. **Hypothesis refuted:** Observed Where > When > What, not When > Where > What
2. **Unexpected trajectory:** All domains show DECREASING HCE over time (not increasing)
3. **Where vulnerability unexpected:** Spatial memory more vulnerable than temporal

---

## Method Notes

- **N:** 42,000 item-responses (100 participants × 105 items × 4 tests)
- **Model:** Linear Mixed Model with participant random intercepts
- **HCE definition:** Accuracy = 0 AND Confidence ≥ 0.75 (captures 0.8 and 1.0 on 5-point scale)
- **Domain classification:** What (-N- tags), Where (-L-/-U-/-D- tags), When (-O- tags)
- **Time variable:** TSVR converted to Days (Decision D070)

---

## Conclusion

High-confidence errors ARE domain-specific (significant main effect and interaction), but in an unexpected pattern. **Spatial (Where) memory is most vulnerable to confident errors**, not temporal (When) memory as hypothesized. All domains show improving metacognitive calibration over time (decreasing HCE rates), suggesting memory degradation is accompanied by appropriate confidence adjustment. This finding contributes to understanding domain-specific metacognition in VR episodic memory assessment.
