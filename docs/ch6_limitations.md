# Chapter 6 Statistical Limitations & Caveats

**Created:** 2025-12-14
**Purpose:** Consolidated documentation of statistical limitations discovered during Ch6 validity rework
**Source:** results/ch6/rq_rework.md validity enhancement audit (TIER 1-4)

---

## Summary of Issues

| Issue | Severity | RQ(s) | Impact | Status |
|-------|----------|-------|--------|--------|
| ICC ratio attenuated by model averaging | MODERATE | 6.1.4 | 824× → 221× | DOCUMENTED |
| Difference score reliability marginal | MODERATE | 6.4.2 | r_diff = 0.66 | DOCUMENTED |
| ERS inflates confidence theta | MODERATE | 6.1.1, 6.8.1 | 11% affected, d=1.89 | DOCUMENTED |
| Domain ICC convergence artifacts | HIGH | 6.3.4 | What/Where UNSTABLE | DOCUMENTED |
| HCE congruence effect marginal | LOW | 6.5.3 | p=0.043 → 0.056 (GEE) | CORRECTED |
| LMM heteroscedasticity | LOW | Multiple | N>100 robust | DOCUMENTED |

---

## Issue 001: ICC Ratio Attenuated by Model Averaging

**RQ:** 6.1.4 (Confidence vs Accuracy ICC Comparison)
**Severity:** MODERATE
**Discovery Date:** 2025-12-14

### Original Finding
- ICC ratio = **824×** (confidence slope variance 824 times greater than accuracy slope variance)
- Computed from single "best" model (Recip_sq, 21.7% Akaike weight)

### Model-Averaged Finding
- ICC ratio = **221×** (73% reduction from original)
- MA ICC_slope = 0.111 (vs original 0.412)
- Computed from 48 competitive models (Eff_N = 31.1)

### Thesis Recommendation
- Report ~220× ratio with model uncertainty caveat
- Finding still ROBUST (>100× threshold, ICC > 0.10)
- Acknowledge that single-model selection inflated original estimate

### Files
- `results/ch6/6.1.4/code/step06b_icc_ma_validation.py`
- `results/ch6/6.1.4/data/step06b_icc_ma_validation.csv`

---

## Issue 002: Difference Score Reliability Below Threshold

**RQ:** 6.4.2 (Paradigm Calibration Differences)
**Severity:** MODERATE
**Discovery Date:** 2025-12-14

### Finding
- Calibration = z(confidence) - z(accuracy) (difference score)
- r_diff = **0.66** (below 0.70 threshold for adequate reliability)
- Components: r_xx=0.87 (confidence), r_yy=0.83 (accuracy), r_xy=0.56

### Impact
- High accuracy-confidence correlation (r=0.56) reduces difference reliability
- Effect sizes (d=0.09-0.11 for paradigm differences) may be attenuated
- True effects could be larger than observed

### Thesis Recommendation
- Document as LIMITATION in Methods section
- Report effect sizes with caveat about potential attenuation
- Sensitivity analysis: Only 2/5 reliability scenarios meet 0.70 threshold

### Files
- `results/ch6/6.4.2/code/step06_difference_score_reliability.py`
- `results/ch6/6.4.2/data/step06_reliability_*.csv`

---

## Issue 003: Extreme Response Style Inflates Confidence Theta

**RQ:** 6.1.1, 6.8.1 (and potentially all confidence RQs)
**Severity:** MODERATE
**Discovery Date:** 2025-12-14

### Finding
- **11%** of participants (11/100) show Extreme Response Style (>50% at endpoints)
- ERS participants have systematically HIGHER confidence theta
- ERS mean theta = -0.16, Non-ERS mean theta = -0.69
- t(98) = 5.90, p < 0.0001, **Cohen's d = 1.89 (MASSIVE effect)**

### Scale Structure
- 6-point scale: {0.0, 0.2, 0.4, 0.6, 0.8, 1.0}
- Level 1 (0.0) NEVER used by any participant (floor effect)
- Level 6 (1.0) most common response (31.1%)

### Thesis Recommendation
- Document as LIMITATION: ERS inflates individual confidence estimates
- Note that 89% of sample unaffected (full scale usage)
- Group-level findings remain valid
- Consider sensitivity analysis excluding ERS participants for individual-difference findings

### Files
- `results/ch6/code/confidence_response_patterns.py`
- `results/ch6/diagnostics/confidence_response_metrics.csv`
- `results/ch6/diagnostics/confidence_response_patterns.png`

---

## Issue 004: Domain ICC Convergence Artifacts (CRITICAL)

**RQ:** 6.3.4 (Domain-Specific ICC Analysis)
**Severity:** HIGH
**Discovery Date:** 2025-12-14

### Finding
- What/Where domains: Default optimizer FAILS TO CONVERGE
- Non-converged ICC_slope = 0.59 (ARTIFACT)
- Converged ICC_slope (Powell optimizer) ≈ 0.00
- Only "When" domain has STABLE estimates across optimizers

### Convergence Results

| Domain | M1 (Default) | M3 (Powell) | Stability |
|--------|--------------|-------------|-----------|
| What   | 0.590*       | 0.000       | UNSTABLE  |
| Where  | 0.590*       | 0.000       | UNSTABLE  |
| When   | 0.000        | 0.000       | STABLE    |

*M1 did NOT converge

### Thesis Recommendation
- **CRITICAL:** Original claims of "domain-specific slope variance" for What/Where may be ARTIFACTS
- Options:
  1. Report only When domain findings (converged)
  2. Flag What/Where as tentative/exploratory
  3. Re-specify model with simpler random effects
- Document convergence issues explicitly in Methods section

### Files
- `results/ch6/code/lmm_convergence_sensitivity.py`
- `results/ch6/diagnostics/lmm_convergence_sensitivity.csv`

---

## Issue 005: HCE Congruence Effect Becomes Non-Significant with GEE

**RQ:** 6.5.3 (High-Confidence Errors by Schema Congruence)
**Severity:** LOW
**Discovery Date:** 2025-12-14

### Finding
- Original (LPM): Incongruent vs Common p = **0.043** (SIGNIFICANT)
- GEE (proper clustering): p = **0.056** (NON-SIGNIFICANT)
- Effect was marginal and becomes n.s. with proper within-person correlation

### Technical Details
- Original used Linear Probability Model (MixedLM on binary outcome)
- GEE with logistic link and exchangeable correlation is more appropriate
- Within-person correlation estimated at 0.030

### Thesis Recommendation
- Report GEE result (p = 0.056) as primary finding
- Note effect is "marginally non-significant" or "trending"
- Do not claim significant congruence effect on HCE rate

### Files
- `results/ch6/code/glmm_refit_non_independence.py`
- `results/ch6/diagnostics/glmm_refit_non_independence.csv`

---

## Issue 006: LMM Residual Heteroscedasticity (Minor)

**RQs:** 6.2.1, 6.3.2, 6.4.2, 6.6.3, 6.8.2
**Severity:** LOW
**Discovery Date:** 2025-12-14

### Finding
- Breusch-Pagan test significant (p < 0.05) for ALL 5 RQs
- Indicates heteroscedasticity in residuals
- However, N > 100 provides robustness (Maas & Hox, 2004)

### Impact Assessment

| RQ | N | Normality | Homoscedasticity | Cook's D | Overall |
|----|---|-----------|------------------|----------|---------|
| 6.2.1 | 400 | FAIL | FAIL | PASS | REVIEW |
| 6.3.2 | 1200 | FAIL | FAIL | PASS | REVIEW |
| 6.4.2 | 1200 | FAIL | FAIL | PASS | REVIEW |
| 6.6.3 | 1200 | FAIL | FAIL | PASS | REVIEW |
| 6.8.2 | 800 | MARGINAL | FAIL | PASS | ADEQUATE |

### Thesis Recommendation
- Document in Methods: "LMM diagnostics revealed heteroscedasticity. However, with N=100 participants and 400-1200 observations, estimates remain robust per simulation studies (Maas & Hox, 2004; Schielzeth et al., 2020)."
- No re-analysis required
- Consider robust standard errors for presentation

### Files
- `results/ch6/code/lmm_residual_diagnostics.py`
- `results/ch6/diagnostics/lmm_diagnostics_summary.csv`

---

## ROBUST Findings (No Issues)

These findings passed validity checks and are ROBUST:

### Bootstrap Robustness (6.7.2)
- Partial r = 0.21 (metacognitive sensitivity)
- 3/4 robustness criteria passed
- Bootstrap 95% CI excludes 0
- Caveat: Outlier-sensitive (7 participants)

### Lord's Paradox Check (6.4.2)
- NOT a concern - accuracy does not differ by paradigm
- ANCOVA confirms non-significant paradigm effect

### Power Analysis for NULL Findings
- ALL 8 null findings adequately powered (84-97% for d=0.30)
- Can claim genuine null effects

### IRT Purification Sensitivity
- 98.6% retention even with stricter thresholds (a≥0.6)
- Item selection ROBUST

### K-means Clustering Stability
- Both 6.1.5 and 6.8.4 pass cross-validation
- Train-test gap < 0.10 (STABLE)

---

## Methods Section Template

**Suggested text for thesis Methods chapter:**

> Statistical limitations were systematically assessed through a comprehensive validity audit. Key caveats include: (1) ICC comparisons between confidence and accuracy trajectories should be interpreted with model uncertainty—model-averaged estimates (221×) are more conservative than single-model estimates (824×); (2) difference score reliability for calibration comparisons is marginal (r = 0.66), potentially attenuating effect sizes; (3) approximately 11% of participants showed extreme response style (ERS) on confidence ratings, which inflates individual theta estimates; (4) domain-specific ICC estimates for What/Where memory domains showed convergence instability and should be interpreted cautiously; (5) LMM residuals showed heteroscedasticity, though estimates remain robust with N > 100 participants (Maas & Hox, 2004).
>
> For binary outcomes with repeated measures, Generalized Estimating Equations (GEE) with exchangeable correlation structure were used to account for within-participant clustering (Zeger & Liang, 1986). K-means clustering solutions were validated using 10-fold cross-validation with 70/30 train-test splits to assess stability.

---

## References

- Burnham, K. P., & Anderson, D. R. (2002). Model selection and multimodel inference. Springer.
- Maas, C. J. M., & Hox, J. J. (2004). Robustness issues in multilevel regression analysis. Statistica Neerlandica, 58(2), 127-137.
- Schielzeth, H., et al. (2020). Robustness of linear mixed‐effects models to violations of distributional assumptions. Methods in Ecology and Evolution, 11(9), 1141-1152.
- Zeger, S. L., & Liang, K. Y. (1986). Longitudinal data analysis for discrete and continuous outcomes. Biometrics, 42(1), 121-130.
