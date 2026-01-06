# RQ 7.4.2 Results Summary

## Research Question
Does BVMT (visuospatial memory test) show stronger prediction for Where (spatial location) than What (object identity)?

## Key Findings

### Primary Result
**Hypothesis NOT Supported**: BVMT correlates slightly MORE with What domain than Where domain, contrary to expectations.

- **r(BVMT, Where)** = 0.348 [95% CI: 0.179, 0.512], p = 0.0004
- **r(BVMT, What)** = 0.373 [95% CI: 0.206, 0.536], p = 0.0001
- **Steiger's Z-test**: z = -0.961, p = 0.336 (non-significant difference)
- **Cohen's q effect size** = 0.029 (negligible)

### Secondary Findings
1. **Domain Correlation**: Where and What domains are highly correlated (r = 0.962), suggesting limited domain-specificity in REMEMVR
2. **Both Correlations Significant**: Both domains show medium effect sizes with BVMT
3. **Direction Opposite to Hypothesis**: What domain shows numerically stronger correlation, though not significantly different

## Sensitivity Analyses

### Outlier Analysis
- 1 outlier identified (1% of sample)
- Results unchanged after outlier removal: r_Where = 0.352, r_What = 0.378

### Alternative Methods
- **Spearman**: r_Where = 0.360, r_What = 0.385 (consistent pattern)
- **Kendall**: τ_Where = 0.254, τ_What = 0.268 (consistent pattern)

### Cross-Validation Stability
- Mean CV correlations: Where = 0.344, What = 0.379
- High variability across folds (SD ≈ 0.24)
- Pattern generally consistent but unstable in small subsamples

### Power Analysis
- Power for Where correlation: 67.6%
- Power for What correlation: 77.1%
- Minimum detectable correlation (80% power): r = 0.382

## Scientific Interpretation

### Theoretical Implications
1. **Domain-Specificity Not Supported**: BVMT does not preferentially predict spatial over object memory in VR
2. **VR Integration Effect**: The high correlation between domains (r = 0.96) suggests VR creates integrated episodic memories
3. **Process Overlap**: Both domains may engage similar cognitive processes in immersive VR context

### Potential Explanations
1. **Integrated Encoding**: VR may promote integrated object-location binding
2. **BVMT Complexity**: BVMT requires both spatial AND object memory (recognizing shapes and locations)
3. **Measurement Issue**: Domain separation may be insufficient in current paradigm

## Anomalies and Limitations

### Anomalies Detected
1. **Opposite Direction**: Result opposite to theoretical prediction (What > Where)
2. **Extreme Domain Correlation**: r = 0.96 between domains suggests multicollinearity
3. **CV Instability**: One fold showed negative correlations (Fold 3: r = -0.065)

### Methodological Limitations
1. **Domain Separation**: Where and What domains nearly perfectly correlated
2. **Sample Size**: N = 100 limits power for detecting small differences
3. **BVMT Measure**: Single cognitive test may not capture domain-specific processes

## Statistical Details

### Dual P-Values (Decision D068)
- **Uncorrected**: p = 0.336
- **Bonferroni**: p = 1.000 (α = 0.00179)
- **FDR**: Not computed (single comparison)

### Effect Sizes
- Cohen's q (correlation difference): 0.029
- Individual correlations: Medium effects (r ≈ 0.35-0.37)

## Conclusion

The hypothesis that BVMT would show domain-specific prediction favoring spatial (Where) over object (What) memory was **not supported**. Instead, BVMT showed equivalent prediction for both domains, with a non-significant trend toward stronger prediction of object memory. The extremely high correlation between domains (r = 0.96) suggests that REMEMVR may not adequately separate spatial and object memory processes, or that VR encoding naturally integrates these domains. Results were robust across sensitivity analyses, though power was marginal for detecting small differences.