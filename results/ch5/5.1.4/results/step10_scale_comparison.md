# Scale Comparison: Theta vs Probability

**Date:** 2025-12-03 10:17

## Purpose

Test whether the anomalously low ICC_slope (0.0005) is an artifact of the IRT theta scale.

## Results

### Variance Components

| Component | Theta Scale | Probability Scale (TCC) | Ratio (Prob/Theta) |
|-----------|------------|------------------------|-------------------|
| var_intercept | 0.476431 | 0.006344 | 0.01× |
| var_slope | 0.000157 | 0.000011 | 0.07× |
| var_residual | 0.309863 | 0.006331 | 0.02× |
| cor_int_slope | -0.4515 | 0.9996 | - |

### ICC Estimates

| Metric | Theta Scale | Probability Scale (TCC) | Ratio | Literature |
|--------|------------|------------------------|-------|------------|
| ICC_intercept | 0.6059 | 0.5005 | 0.83× | 0.60-0.80 |
| ICC_slope | 0.000505 | 0.001747 | 3.5× | 0.30-0.50 |

## Interpretation

### NO SUPPORT for Scale Hypothesis

ICC_slope on probability scale (0.001747) remains similar to theta scale (0.000505).

**Conclusion:** The low ICC_slope is a REAL finding, not a scale artifact.
VR episodic memory may genuinely show homogeneous forgetting rates across individuals.

## Technical Details

### Model Specification
- Formula: Prob_TCC ~ Days + log(Days+1)
- Random effects: ~log_TSVR (intercepts and slopes on log time)
- Method: ML estimation via LBFGS

### Data
- Observations: 400
- Participants: 100
- Purified items for TCC: 68

### Boundary Check
- Near floor (<0.05): 0 observations
- Near ceiling (>0.95): 0 observations
