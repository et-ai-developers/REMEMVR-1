# RQ 5.2.6: Domain-Specific Variance Decomposition

**Chapter:** 5
**Type:** Domains
**Subtype:** Domain-Specific Variance Decomposition
**Full ID:** 5.2.6

---

## ⚠️ WHEN DOMAIN EXCLUSION

**Critical:** When domain is EXCLUDED from this analysis due to floor effect discovered in RQ 5.2.1.

**Exclusion Rationale:**
- 77% item attrition (26→6 items) after IRT purification
- 6-9% floor effect (participants scoring at chance)
- Only What (29 items) and Where (50 items) domains provide reliable theta estimates

**Impact on Analysis:**
- Original: 3 domains × 100 participants × 4 tests = 1200 rows
- Revised: 2 domains × 100 participants × 4 tests = 800 rows
- Random effects: 200 rows (100 UID × 2 domains) instead of 300

---

## Research Question

**Primary Question:**
What proportion of variance in forgetting rate is between-person versus within-person for each memory domain (What, Where)?

**Scope:**
This RQ examines variance decomposition in forgetting trajectories across two episodic memory domains. Sample: N=100 participants x 4 test sessions x 2 domains = 800 observations. Analysis uses IRT-derived theta scores from domain-specific calibrations (RQ 5.2.1). Focus on random slope variance (forgetting rate) as indicator of trait-like individual differences versus measurement error.

**Theoretical Framing:**
Variance decomposition addresses whether forgetting rate is a stable individual difference (between-person variance) or primarily measurement noise (within-person variance). High between-person variance (ICC > 0.40) suggests forgetting rate is a trait-like characteristic. Domain differences in ICC magnitude may reflect differential stability of domain-specific memory systems (dual-process theory: familiarity-based What memory vs recollection-based Where/When memory).

---

## Theoretical Background

**Relevant Theories:**
- **Dual-Process Theory** (Yonelinas, 2002): Memory retrieval relies on familiarity (fast, automatic, supports What memory) and recollection (slow, effortful, supports Where/When memory). Domain-specific forgetting rates may show different stability profiles reflecting different neural substrates.
- **Individual Differences in Memory Aging**: Between-person variance in forgetting may differ by domain if some memory systems are more vulnerable to individual differences in aging, consolidation, or hippocampal function.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
If forgetting rate is a stable individual difference, ICC for slopes should exceed 0.40. Domain differences in ICC magnitude may emerge: Where/When memory (hippocampal-dependent) may show greater between-person variance than What memory (perirhinal-dependent) due to greater vulnerability to individual differences in hippocampal aging and consolidation efficiency.

**Literature Gaps:**
[To be identified by rq_scholar]

---

## Hypothesis

**Primary Hypothesis:**
Substantial between-person variance (ICC for slopes > 0.40) exists within each domain, indicating forgetting rate is a trait-like individual difference rather than measurement noise.

**Secondary Hypotheses:**
Potential domain differences in ICC magnitude reflecting differential trait-like stability of forgetting. Where and When domains (hippocampal-dependent, recollection-based) may show higher ICC than What domain (perirhinal-dependent, familiarity-based) if hippocampal aging effects vary more across individuals.

**Theoretical Rationale:**
If forgetting rate were purely measurement error, ICC would approach 0. High ICC (>0.40) indicates stable individual differences. Domain-specific ICC patterns test whether memory systems differ in their susceptibility to stable individual differences versus transient noise. Dual-process theory predicts recollection-based domains (Where/When) may show greater individual variability due to hippocampal aging effects.

**Expected Effect Pattern:**
- ICC_slope (conditional at Day 6) > 0.40 for at least one domain
- Interpretation thresholds: ICC < 0.20 = Low, 0.20-0.40 = Moderate, >= 0.40 = Substantial
- Potential rank order: ICC_When >= ICC_Where > ICC_What (if hippocampal aging effects dominate)
- Negative intercept-slope correlation (high baseline performers maintain advantage over time)

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object identity / naming (29 items from RQ 5.2.1)
  - Theoretical Basis: Familiarity-based, perirhinal cortex-dependent

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location, legacy)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Disambiguation: All Where tags included (50 items from RQ 5.2.1)
  - Theoretical Basis: Recollection-based, hippocampal-dependent

- [ ] **When** (Temporal Order) - EXCLUDED
  - Tag Code: `-O-`
  - Description: Temporal order / sequence
  - **EXCLUSION REASON:** Floor effect discovered in RQ 5.2.1 (77% item attrition, 6-9% floor)

**Inclusion Rationale:**
What and Where domains included to test domain-specific variance patterns. Variance decomposition requires domain-stratified models (separate LMM per domain) to isolate domain-specific between-person and within-person variance components.

**Exclusion Rationale:**
When domain excluded due to floor effect (RQ 5.2.1): 77% item attrition after IRT purification (26→6 items), 6-9% participants at floor. Theta estimates unreliable with only 6 items.

---

## Analysis Approach

**Analysis Type:**
Linear Mixed Models (LMM) with random intercepts and slopes for variance decomposition. Intraclass Correlation Coefficient (ICC) computation for between-person vs within-person variance.

**High-Level Workflow:**

**Step 1:** Fit domain-stratified LMMs with random slopes
- Three separate models: theta ~ Time + (Time | UID) for What, Where, When
- REML=False for model comparison (consistent with RQ 5.2.1 approach)
- Random slopes allow individual-specific forgetting rates

**Step 2:** Extract variance components per domain
- var_intercept (between-person variance in baseline ability)
- var_slope (between-person variance in forgetting rate)
- cov_int_slope (intercept-slope covariance)
- var_residual (within-person variance / measurement error)
- Total: 5 components x 3 domains = 15 rows

**Step 3:** Compute ICC estimates per domain
- ICC_intercept: var_intercept / (var_intercept + var_residual)
- ICC_slope_simple: var_slope / (var_slope + var_residual)
- ICC_slope_conditional: ICC at Day 6 accounting for intercept-slope correlation
- Interpretation: <0.20=Low, 0.20-0.40=Moderate, >=0.40=Substantial
- Total: 3 ICC types x 3 domains = 9 rows

**Step 4:** Extract individual random effects per domain
- Total_Intercept and Total_Slope for 100 participants x 3 domains
- Output: 300 rows (100 UID x 3 domains)
- These serve as input for RQ 5.2.7 (domain-based clustering)

**Step 5:** Test intercept-slope correlations per domain
- Pearson correlation between Total_Intercept and Total_Slope
- Bonferroni alpha = 0.0033 (for 3 domains: 0.01 / 3)
- Report dual p-values (Decision D068: p_uncorrected and p_bonferroni)
- Negative correlation indicates high performers maintain advantage

**Step 6:** Compare ICC across domains
- Rank domains by ICC_slope_conditional
- Characterize domain differences in variance decomposition
- Prepare barplot data comparing ICC estimates

**Expected Outputs:**
- data/step01_model_metadata_what.yaml (model convergence and structure)
- data/step01_model_metadata_where.yaml
- data/step01_model_metadata_when.yaml
- data/step02_variance_components.csv (15 rows: 5 components x 3 domains)
- data/step03_icc_estimates.csv (9 rows: 3 ICC types x 3 domains)
- data/step04_random_effects.csv (300 rows: 100 UID x 3 domains) [REQUIRED for RQ 5.2.7]
- data/step05_domain_icc_comparison.csv (domain rankings and interpretations)
- plots/step06_domain_icc_barplot.png (visual comparison of ICC estimates)

**Success Criteria:**
- All 3 domain models converge (model.converged = True)
- Variance components positive (no Heywood cases)
- ICC in [0,1] (valid probability range)
- 300 random effects extracted (100 participants x 3 domains, no missing)
- Dual p-values for correlations (Decision D068: p_uncorrected and p_bonferroni)
- Domain comparison interpretable (clear ranking, ICC thresholds applied)

---

## Validation Procedures

### LMM Assumption Checks

1. **Residual Normality:** Q-Q plot + Shapiro-Wilk test (accept if p > 0.01)
2. **Homoscedasticity:** Residuals vs fitted plot; Levene's test by domain
3. **Random Effects Normality:** Q-Q plot of random intercept and slope estimates
4. **Independence:** ACF plot of residuals (no significant autocorrelation)
5. **Linearity:** Residuals vs TSVR_hours (no systematic curvature)
6. **Outliers:** Cook's distance < 4/N threshold

### Convergence Contingency Plan

If any domain-stratified model fails to converge with random slopes:
1. Try alternative optimizers (bobyqa, nlminb)
2. Use likelihood ratio test (LRT) to compare random slopes vs intercept-only
3. If LRT p < 0.05, retain slopes with simplified correlation structure (uncorrelated random effects)
4. If LRT p ≥ 0.05, use random intercepts-only model for that domain
5. Document which structure achieved per domain in model metadata

Reference: Bates et al. (2015) parsimonious mixed models guidelines.

### Remedial Actions

- If normality violated: Report robust standard errors or transform theta scores
- If heteroscedasticity detected: Use weighted LMM or variance function by domain
- If outliers detected (Cook's d > 4/N): Sensitivity analysis with/without outliers

### ICC Threshold Justification

ICC interpretation thresholds follow Koo & Li (2016) guidelines for reliability research:
- ICC < 0.50 = Poor reliability
- ICC 0.50-0.75 = Moderate reliability
- ICC 0.75-0.90 = Good reliability
- ICC > 0.90 = Excellent reliability

For this RQ, we use a more lenient threshold (ICC > 0.40 = "substantial") following individual differences literature conventions, acknowledging that forgetting rate reliability is typically lower than test-retest reliability. This threshold is justified by McGraw & Wong (1996) ICC(2,1) guidelines for single-measurement reliability.

### Practice Effects Consideration

The 4-session design (Days 0, 1, 3, 6) creates potential practice effects:
- Literature documents 13.3% improvement in episodic memory with repeated testing (BMC Neuroscience)
- IRT theta scoring partially mitigates item-level practice effects through latent trait estimation
- Domain-stratified analysis assumes practice effects are similar across What/Where/When domains
- If practice effects differ by domain, ICC estimates may partially reflect practice variability rather than pure forgetting trait variance

Limitation acknowledged; future sensitivity analysis could include Test Session as fixed effect covariate.

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.2.1 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 5.2.1 (Domain-Specific Trajectories)

**File Paths:**
- results/ch5/5.2.1/data/step04_lmm_input.csv (1200 rows: theta scores reshaped to long format)
  - Columns: composite_ID, UID, test, TSVR_hours, domain, theta, se
  - 100 participants x 4 tests x 3 domains = 1200 observations

**Dependencies:**
RQ 5.2.1 must complete Steps 1-4 (IRT calibration with 3-factor What/Where/When model, item purification, theta score extraction, merge with TSVR and reshape to long format) before this RQ can run.

**Note:** This RQ does NOT use the best-fitting LMM model from RQ 5.2.1. Instead, it fits NEW domain-stratified models (separate LMM per domain) to isolate domain-specific variance components. The "best-fitting LMM model with random slopes by domain" mentioned in Data_Required refers to the modeling approach (random slopes structure), not a saved model object.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants from RQ 5.2.1 (inherited inclusion criteria)
- No exclusions

**Items:**
- [x] Purified items from RQ 5.2.1 IRT calibration (approximately 70 items retained)
  - What: ~25 items (after purification from 29)
  - Where: ~40 items (after purification from 50)
  - When: ~22 items (after purification from 26)
- Theta scores already aggregated per participant x test x domain

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4; nominal Days 0, 1, 3, 6)
- [x] Time variable: TSVR_hours (actual hours since encoding, not nominal days)
- Inherited from RQ 5.2.1

---
