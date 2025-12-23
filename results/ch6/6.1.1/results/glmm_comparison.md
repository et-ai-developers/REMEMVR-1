# GLMM vs IRT → LMM Comparison

## Research Question
**RQ 6.1.1:** Which functional form best describes confidence decline over a 6-day retention interval?

## Methods Comparison

| Aspect | IRT → LMM | GLMM (this analysis) |
|--------|-----------|---------------------|
| **Approach** | Two-stage (GRM → LMM) | Single-stage |
| **Outcome** | Theta scores (continuous) | Ordinal ratings (5-level) |
| **Error structure** | Gaussian | Quasi-continuous GEE / Binomial GEE |
| **N observations** | 400 (aggregated) | 28,800 (item-level) |
| **Time variable** | log_Days_plus1 | log(TSVR_hours) |
| **Random effects** | Random slopes by participant | GEE clustering by participant |

## Key Results

### Time Effect (The Critical Test)

| Method | β (time) | SE | p-value | Interpretation |
|--------|----------|----|---------| --------------|
| GLMM Continuous | -0.033595 | 0.002037 | 0.000000 | SIGNIFICANT |
| GLMM Binomial | -0.186146 | 0.012563 | 0.000000 | SIGNIFICANT |
| IRT → LMM | ~-0.058 | ~0.009 | <0.001 | SIGNIFICANT |

### GLMM Model Details

#### Quasi-Continuous GEE
- **Intercept**: 0.673491 (SE=0.013536)
- **log_TSVR**: -0.033595 (SE=0.002037, p=0.000000)
- Treating ordinal confidence (0.2-1.0) as interval scale

#### Binomial GEE (High vs Low Confidence)
- **Intercept**: 0.628848 (SE=0.088697)
- **log_TSVR**: -0.186146 (SE=0.012563, p=0.000000)
- **Odds Ratio**: 0.8302
- Dichotomized at ≥0.6 = high confidence

#### Cumulative Threshold Analysis
Testing time effect at each ordinal threshold (proportional odds check):

| Threshold | β(time) | SE | p |
|-----------|---------|----|----|
| >0.2 | -0.186236 | 0.018884 | 0.000000 |
| >0.4 | -0.186146 | 0.012563 | 0.000000 |
| >0.6 | -0.188325 | 0.011383 | 0.000000 |
| >0.8 | -0.189096 | 0.012868 | 0.000000 |

**Proportional Odds Check:** β range = -0.1891 to -0.1861
✓ Similar βs suggest proportional odds assumption holds

### Confidence by Test (Descriptive)

| Test | Mean | SD | N |
|------|------|----|---|
| T1 | 0.664 | 0.325 | 7,200 |
| T2 | 0.586 | 0.325 | 7,200 |
| T3 | 0.534 | 0.319 | 7,200 |
| T4 | 0.484 | 0.310 | 7,200 |

## Conclusion

**The time effect finding is ROBUST to methodological choice.**

Both GLMM approaches confirm the IRT→LMM result:
1. **Significant main effect of time** - Confidence declines over the retention interval
2. **Time effect is NEGATIVE** - Later tests show lower confidence
3. Confidence decline is consistent across item-level and aggregated approaches

The GLMM approach directly models ordinal confidence ratings at item-level,
providing a robustness check for the two-stage IRT→LMM methodology.
