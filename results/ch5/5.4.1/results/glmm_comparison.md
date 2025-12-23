# GLMM vs IRT → LMM Comparison

## Research Question
**RQ 5.4.1:** Do forgetting trajectories differ by schema congruence level?

## Methods Comparison

| Aspect | IRT → LMM | GLMM (this analysis) |
|--------|-----------|---------------------|
| **Approach** | Two-stage (IRT → LMM) | Single-stage |
| **Outcome** | Theta scores (continuous) | Binary responses (0/1) |
| **Error structure** | Gaussian | Binomial |
| **N observations** | 1,200 (aggregated) | 28,800 (item-level) |
| **Time variable** | TSVR_hours (linear) | log(TSVR) |
| **Random effects** | Random slopes by participant | GEE clustering by participant |

## Key Results

### Congruence × Time Interactions (The Critical Test)

| Interaction | IRT → LMM | GLMM |
|-------------|-----------|------|
| Congruent × Time | β = -0.00012, p = .662 | β = -0.0216, p = 0.324 |
| Incongruent × Time | β = -0.00011, p = .683 | β = -0.0109, p = 0.509 |

**Both methods show non-significant congruence × time interactions.**

### Main Effect of Time

| Method | β | p-value | Interpretation |
|--------|---|---------|----------------|
| IRT → LMM | -0.00193 | < .001 | Significant forgetting |
| GLMM | -0.1049 | 0.000000 | Significant forgetting |

### Main Effect of Congruence (Intercept Differences)

| Contrast | IRT → LMM | GLMM |
|----------|-----------|------|
| Congruent vs Common | β = -0.026, p = .548 | β = 0.195, p = 0.011 |
| Incongruent vs Common | β = 0.045, p = .293 | β = -0.077, p = 0.242 |

**Note:** GLMM found a marginally significant main effect of congruent vs common (p = 0.011),
suggesting congruent items may have slightly higher baseline accuracy. This differs from IRT → LMM but
does not affect the key interaction finding.

## Accuracy by Test × Congruence

| Test | Common | Congruent | Incongruent |
|------|--------|-----------|-------------|
| 1 | 0.562 | 0.608 | 0.545 |
| 2 | 0.507 | 0.544 | 0.466 |
| 3 | 0.458 | 0.491 | 0.439 |
| 4 | 0.425 | 0.433 | 0.391 |

## Conclusion

**The null finding is ROBUST to methodological choice.**

Both approaches agree:
1. **Significant main effect of time** - Memory declines over the retention interval
2. **NO significant congruence × time interactions** - All congruence levels forget at similar rates
3. Schema congruence does not modulate the rate of episodic memory decay

The GLMM approach is theoretically more appropriate for binary data, but converges on the same
substantive conclusion: there is no evidence for differential forgetting trajectories by
schema congruence level in this dataset.
