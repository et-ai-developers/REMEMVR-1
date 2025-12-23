# GLMM vs IRT → LMM Comparison: Age Effects (RQ 5.1.3)

## Research Question
**RQ 5.1.3:** Do older adults show lower baseline episodic memory (intercept) and/or faster forgetting (steeper slope)?

## Methods Comparison

| Aspect | IRT → LMM | GLMM (this analysis) |
|--------|-----------|---------------------|
| **Approach** | Two-stage (IRT → LMM) | Single-stage |
| **Outcome** | Theta scores (continuous) | Binary responses (0/1) |
| **Error structure** | Gaussian | Binomial |
| **N observations** | 400 (aggregated) | 42,000 (item-level) |
| **Time variable** | Time + Time_log | log(TSVR) |
| **Age variable** | Age_c (centered at 44.6) | Age_c (centered at 44.6) |

## Key Results

### Age Effect on Intercept (Baseline Memory)

| Method | β | p-value | Interpretation |
|--------|---|---------|----------------|
| IRT → LMM | -0.012 | .061 | Marginal, NS after Bonferroni |
| GLMM | -0.00679 | 0.0138 | Significant |

### Age × Time Interaction (Forgetting Rate)

| Method | β | p-value | Interpretation |
|--------|---|---------|----------------|
| IRT → LMM (linear) | 0.000015 | .831 | NOT significant |
| IRT → LMM (log) | 0.001 | .761 | NOT significant |
| GLMM | 0.000392 | 0.4596 | NOT significant |

### Main Effect of Time

| Method | β | p-value |
|--------|---|---------|
| IRT → LMM | -0.198 (log) | < .001 |
| GLMM | -0.11486 | 0.000000 |

## Accuracy by Age Tertile × Test

| Age Group | Test 1 | Test 2 | Test 3 | Test 4 |
|-----------|--------|--------|--------|--------|
| Young | 0.653 | 0.565 | 0.542 | 0.500 |
| Middle | 0.599 | 0.537 | 0.477 | 0.441 |
| Older | 0.589 | 0.528 | 0.489 | 0.452 |

## Conclusion

**Age effect on intercept (baseline memory):** SIGNIFICANT (p = 0.0138)

**Age × Time interaction (forgetting rate):** NOT SIGNIFICANT (p = 0.4596)

The GLMM approach confirms the IRT → LMM finding that age does not significantly modulate forgetting rate.
