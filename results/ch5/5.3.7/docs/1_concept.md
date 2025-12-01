# RQ 5.3.7: Paradigm-Specific Variance Decomposition

**Chapter:** 5
**Type:** Paradigms
**Subtype:** Paradigm-Specific Variance Decomposition
**Full ID:** 5.3.7

---

## Research Question

**Primary Question:**
What proportion of variance in forgetting rate is between-person versus within-person for each retrieval paradigm (Free Recall, Cued Recall, Recognition)?

**Scope:**
This RQ examines individual differences in forgetting trajectories stratified by retrieval paradigm. Sample: N=100 participants across 4 test sessions (T1, T2, T3, T4; nominal Days 0, 1, 3, 6) × 3 paradigms (Free Recall, Cued Recall, Recognition) = 1200 observations. Paradigm-specific variance components will be extracted from separate LMMs fitted per paradigm with random intercepts and slopes by participant.

**Theoretical Framing:**
Variance decomposition determines the extent to which forgetting rate represents a stable, trait-like individual difference (high between-person variance, high ICC) versus measurement error or state-dependent fluctuation (high within-person variance, low ICC). Paradigm-specific ICCs may differ if retrieval support moderates the stability of individual differences in forgetting.

---

## Theoretical Background

**Relevant Theories:**
- **Individual Differences Framework**: Forgetting rate as a stable individual difference trait (high between-person variance) versus unstable state (high within-person variance). ICC quantifies trait-like stability.
- **Retrieval Support Theory**: Paradigms vary in retrieval support (Free Recall = minimal, Cued Recall = moderate, Recognition = maximal). Retrieval support may moderate the magnitude of individual differences, with less supported paradigms (Free Recall) showing greater between-person variance due to reliance on self-initiated retrieval processes.
- **Trait Memory Stability**: If forgetting rate is a stable cognitive trait, ICC for slopes should be substantial (> 0.40) across paradigms, with possible differences reflecting paradigm-specific cognitive demands.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
Substantial between-person variance (ICC > 0.40) is expected within each paradigm, indicating forgetting rate is trait-like and replicable across paradigms. Paradigm differences in ICC magnitude may emerge, with Free Recall potentially showing highest between-person variance due to greater reliance on individual retrieval ability.

**Literature Gaps:**
[To be identified by rq_scholar]

---

## Hypothesis

**Primary Hypothesis:**
Substantial between-person variance (ICC for slopes > 0.40) exists within each paradigm (Free Recall, Cued Recall, Recognition), indicating forgetting rate is a stable, trait-like individual difference across retrieval contexts.

**Secondary Hypotheses:**
Paradigm differences in ICC magnitude may reflect differential trait-like stability. Free Recall may show highest ICC (most reliance on individual ability), Recognition may show lowest ICC (ceiling effects reduce individual variance), with Cued Recall intermediate.

**Theoretical Rationale:**
If forgetting rate is a stable cognitive trait, individual differences should be consistent across paradigms, yielding substantial ICCs. Paradigm differences in ICC would indicate that retrieval support moderates the expression of individual differences, with less supported paradigms (Free Recall) amplifying trait-based variance.

**Expected Effect Pattern:**
ICC for slopes > 0.40 for all three paradigms (substantial between-person variance). Possible paradigm ordering: ICC_FreeRecall > ICC_CuedRecall > ICC_Recognition. Intercept-slope correlations may be negative (high baseline ability associated with slower forgetting, preserving rank-order stability).

---

## Memory Domains

**Domains Examined:**

This RQ analyzes paradigm-specific variance across three retrieval paradigms, not memory content domains (What/Where/When). The paradigms are:

- **Free Recall (IFR)**: Self-initiated retrieval without external cues
- **Cued Recall (ICR)**: Retrieval with category or semantic cues
- **Recognition (IRE)**: Recognition memory with target-present/absent forced choice

**Inclusion Rationale:**
All three interactive paradigms (IFR, ICR, IRE) are included to decompose variance across the full range of retrieval support. Passive paradigms (RFR, TCR, RRE) are excluded per Chapter 5 focus on interactive VR experience.

**Exclusion Rationale:**
- Room Free Recall (RFR): Excluded (passive, non-interactive)
- Room Recognition (RRE): Excluded (passive, non-interactive)
- Test Cued Recall (TCR): Excluded (passive, non-interactive)

---

## Analysis Approach

**Analysis Type:**
Variance decomposition using Linear Mixed Models (LMM) with random effects extraction and Intraclass Correlation Coefficient (ICC) computation. Three separate LMMs fitted (one per paradigm) to isolate paradigm-specific variance components.

**High-Level Workflow:**

**Step 1:** Load RQ 5.3.1 best-fitting LMM model and theta scores per paradigm (Free Recall, Cued Recall, Recognition). Verify model convergence and extract paradigm categories.

**Step 2:** Fit paradigm-stratified LMMs with random slopes per participant. For each paradigm separately, fit: theta ~ Time + (Time | UID), where Time uses the functional form identified in RQ 5.3.1 (likely log-transformed based on Chapter 5 pattern). Extract variance components per paradigm: var_intercept, var_slope, cov_int_slope, var_residual from model.cov_re attribute.

**Step 3:** Compute Intraclass Correlation Coefficients (ICC) per paradigm. Calculate three ICC estimates for each paradigm: ICC_intercept (baseline ability), ICC_slope_simple (forgetting rate, unconditional), ICC_slope_conditional (forgetting rate at Day 6, conditional on time). Interpret ICC using standard thresholds: < 0.20 = Low, 0.20-0.40 = Moderate, >= 0.40 = Substantial between-person variance.

**Step 4:** Extract individual random effects for all 100 participants per paradigm (Total_Intercept, Total_Slope). This produces 300 rows total (100 participants × 3 paradigms). Random effects required for downstream clustering analysis (RQ 5.3.8).

**Step 5:** Test intercept-slope correlation per paradigm using Pearson correlation with Bonferroni correction (alpha = 0.0033 for 15 tests across paradigms). Report dual p-values (Decision D068: both p_uncorrected and p_bonferroni). Negative correlation expected (high baseline associated with slower forgetting).

**Step 6:** Compare ICC estimates across paradigms. Create paradigm ICC comparison table and barplot visualization showing ICC_slope_conditional for all three paradigms with 95% confidence intervals. Interpret paradigm ordering and magnitude differences.

**Expected Outputs:**
- data/step02_variance_components.csv (15 rows: 5 variance components × 3 paradigms)
- data/step03_icc_estimates.csv (9 rows: 3 ICC types × 3 paradigms)
- data/step04_random_effects.csv (300 rows: 100 participants × 3 paradigms, REQUIRED for RQ 5.3.8)
- data/step05_paradigm_icc_comparison.csv (3 rows: 1 per paradigm with ICC comparison)
- plots/step06_paradigm_icc_barplot.png (visual comparison of ICC across paradigms)

**Success Criteria:**
- All 3 paradigm-specific models converge (model.converged = True)
- All variance components positive (no negative variances or estimation failures)
- All ICC estimates in valid range [0, 1]
- 300 random effects extracted (100 participants × 3 paradigms, no missing data)
- Intercept-slope correlation tests include dual p-values (Decision D068 compliance)
- Paradigm ICC comparison interpretable (clear ordering or equivalence pattern)
- Barplot file size > 10KB (indicates successful rendering)
- All assumption validation checks documented (see Validation Procedures below)

---

## Validation Procedures

### LMM Assumption Checks (Per Paradigm Model)

1. **Residual Normality:** Q-Q plot + Shapiro-Wilk test (accept if p > 0.01)
2. **Homoscedasticity:** Residuals vs fitted plot; Levene's test by test session
3. **Random Effects Normality:** Q-Q plot of random intercept and slope estimates
4. **Independence:** ACF plot of residuals (no significant autocorrelation)
5. **Linearity:** Residuals vs Time predictor (no systematic patterns)
6. **Outliers:** Cook's distance < 4/N threshold

### Remedial Actions

- If normality violated: Report robust standard errors; note impact on variance component estimates
- If heteroscedasticity: Consider variance function by test session
- If outliers detected: Sensitivity analysis excluding influential participants; report ICC with and without outliers
- Document all violations and their potential impact on ICC interpretation

### Convergence Contingency Plan

If any paradigm-specific model fails to converge with random slopes:
1. Try alternative optimizers (bobyqa, nlminb)
2. Use likelihood ratio test (LRT) to compare random slopes vs intercept-only
3. If LRT p < 0.05, retain slopes with simplified correlation structure
4. If LRT p ≥ 0.05, use random intercepts-only model
5. **Note:** If random slopes cannot be estimated for a paradigm, ICC_slope cannot be computed; report this limitation

Reference: Bates et al. (2015) parsimonious mixed models guidelines.

## Practice Effects Consideration

The 4-session design (Days 0, 1, 3, 6) creates potential practice effects:
- Practice effects contribute to within-person variance if they create session-specific performance fluctuations
- ICC estimates may underestimate trait-like stability if practice effects are large
- IRT theta scoring partially mitigates item-level practice effects
- The random slope variance captures both true individual differences in forgetting and individual differences in practice-related improvement

**Interpretation Guidance:** ICC values should be interpreted as lower bounds of trait-like stability, given potential practice effect confounds.

## ICC Scale Interpretation

**Which scale for ICC?**
- If Time uses log transformation (per RQ 5.3.1 best model): ICC computed on log-time scale
- Interpretation is for rate of forgetting on the log-transformed time scale
- This is appropriate because log-time is the scale on which linear forgetting assumptions hold

**Threshold Interpretation (Koo & Li, 2016):**
- ICC < 0.50: Poor reliability
- 0.50 ≤ ICC < 0.75: Moderate reliability
- 0.75 ≤ ICC < 0.90: Good reliability
- ICC ≥ 0.90: Excellent reliability

The ICC > 0.40 threshold used in this RQ is a lower standard reflecting substantial (not excellent) between-person variance, appropriate for exploratory individual differences research.

## Key Citations to Add

Recent literature (2020-2024) on variance decomposition in episodic memory:
- [rq_scholar to search and add 5-6 high-relevance citations]
- Focus areas: ICC in longitudinal memory studies, individual differences in forgetting, retrieval paradigm effects on variance components

## Limitations

1. **Ceiling Effects:** Recognition paradigm may show compressed variance due to ceiling performance, attenuating ICC estimates
2. **Dropout Bias:** If participants with poor memory are more likely to miss sessions, ICC may be biased upward (remaining participants more homogeneous)
3. **Practice Effects:** Cannot fully disentangle trait stability from differential practice effect magnitude

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.3.1 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 5.3.1 (Paradigm-Specific Trajectories)

**File Paths:**
- results/ch5/5.3.1/data/step05_lmm_fitted_model.pkl (best-fitting LMM model with paradigm factors)
- results/ch5/5.3.1/data/step04_lmm_input.csv (theta scores in long format: 1200 rows = 100 participants × 4 tests × 3 paradigms)
- results/ch5/5.3.1/data/step03_theta_scores.csv (IRT ability estimates per paradigm from 3-dimensional GRM calibration)

**Dependencies:**
RQ 5.3.1 must complete Steps 1-5 (IRT calibration on paradigm-specific items, LMM fitting with Paradigm × Time interaction, model selection via AIC) before this RQ can run. No new IRT calibration is performed in this RQ; variance decomposition uses existing theta scores from RQ 5.3.1.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants from RQ 5.3.1 (inherited inclusion criteria, no additional exclusions)

**Items:**
- N/A (theta scores are already aggregated per paradigm; item-level data not used in variance decomposition)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4) inherited from RQ 5.3.1 (Days 0, 1, 3, 6)

**Paradigms:**
- [x] Free Recall (IFR) - Self-initiated retrieval
- [x] Cued Recall (ICR) - Cued retrieval
- [x] Recognition (IRE) - Recognition memory
- [ ] Room Free Recall (RFR) - EXCLUDED (passive paradigm, not in RQ 5.3.1)
- [ ] Test Cued Recall (TCR) - EXCLUDED (passive paradigm, not in RQ 5.3.1)
- [ ] Room Recognition (RRE) - EXCLUDED (passive paradigm, not in RQ 5.3.1)

---
