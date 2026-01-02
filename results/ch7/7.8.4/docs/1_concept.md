# RQ 7.8.4: Multivariate vs univariate prediction

**Chapter:** 7
**Type:** Predictive simplification
**Subtype:** Model simplification
**Full ID:** 7.8.4

---

## Research Question

**Primary Question:**
Does predicting all three domains jointly (multivariate) outperform separate domain predictions?

**Scope:**
This RQ compares multivariate vs univariate approaches for predicting episodic memory performance across What/Where/When domains. Examines N=100 participants using theta scores from Ch5 domain-specific analyses (5.2.X) as dependent variables and cognitive tests (RAVLT, BVMT, NART, RPM) plus Age as independent variables. Cross-sectional design comparing model efficiency and prediction accuracy.

**Theoretical Framing:**
Tests whether joint modeling leverages cross-domain correlations for improved prediction efficiency. Addresses model simplification question: can simpler univariate models achieve equivalent predictive performance to complex multivariate approaches?

---

## Theoretical Background

**Relevant Theories:**
- **Episodic Memory Network Theory**: What/Where/When domains share common neural substrates and memory processes, suggesting correlations that multivariate models could exploit
- **Cognitive Efficiency Principle**: Simpler models often generalize better than complex models (bias-variance trade-off)

**Key Citations:**
Research on multivariate vs univariate prediction in cognitive domains

**Theoretical Predictions:**
Multivariate models should capitalize on cross-domain correlations to improve prediction efficiency. However, increased model complexity may lead to overfitting, potentially negating efficiency gains in cross-validation.

**Literature Gaps:**
Limited research comparing multivariate vs univariate approaches for predicting episodic memory domain performance from cognitive test batteries.

---

## Hypothesis

**Primary Hypothesis:**
Multivariate model should fit training data better due to modeling cross-domain covariances, but efficiency gain may not persist in cross-validation due to increased complexity.

**Secondary Hypotheses:**
Cross-domain covariances will be moderate (.30-.60), providing sufficient correlation for multivariate modeling benefits but not so high as to indicate redundancy.

**Theoretical Rationale:**
Domains share neural substrates (hippocampal formation) but recruit partially distinct networks (perirhinal for What, parahippocampal for Where), creating moderate correlations that multivariate models can exploit.

**Expected Effect Pattern:**
Multivariate model: lower AIC on training data, higher R-squared. Cross-validation: Similar or slightly worse performance due to increased parameter count and overfitting risk.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Uses domain-specific theta scores from Ch5 5.2.X analyses

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Disambiguation: Uses aggregated Where theta scores from Ch5 5.2.X

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Uses domain-specific theta scores from Ch5 5.2.X analyses

**Inclusion Rationale:**
All three episodic memory domains included as dependent variables to test multivariate vs univariate prediction approaches. Domain-specific theta scores capture purified domain performance for comparative modeling.

**Exclusion Rationale (if applicable):**
N/A - all domains required for multivariate comparison.

---

## Analysis Approach

**Analysis Type:**
Multiple regression with model comparison and cross-validation

**High-Level Workflow:**

**Step 1:** Extract and prepare data
- Load domain-specific theta scores from Ch5 5.2.X results
- Extract cognitive tests from master.xlsx (RAVLT, BVMT, NART, RPM)
- Include Age as covariate
- Check data quality and compute correlations

**Step 2:** Fit univariate models
- What ~ Age + RAVLT + BVMT + NART + RPM
- Where ~ Age + RAVLT + BVMT + NART + RPM  
- When ~ Age + RAVLT + BVMT + NART + RPM
- Extract individual R-squared values
- Sum univariate AIC values

**Step 3:** Fit multivariate model
- MANOVA or multivariate regression
- DVs: [What, Where, When] ~ Age + RAVLT + BVMT + NART + RPM
- Extract overall R-squared (Pillai's trace or similar)
- Compute multivariate AIC

**Step 4:** Model comparison
- Compare AIC: univariate sum vs multivariate
- Cross-validation: k-fold CV for both approaches
- Test performance gap: training vs test R-squared

**Step 5:** Model diagnostics
- Multicollinearity: VIF < 5 for all predictors
- Residual normality: Shapiro-Wilk test, Q-Q plots
- Homoscedasticity: Breusch-Pagan test
- Cross-domain correlations and covariance structure

**Step 6:** Test individual predictors
- Extract standardized coefficients for both approaches
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Primary: Bonferroni correction (± = 0.05/28 = 0.00179)
- Secondary: FDR correction for comparison

**Step 7:** Cross-validation
- Method: 5-fold CV
- Metrics: Test R-squared, RMSE, MAE for both approaches
- Check for overfitting (training vs test performance gap)

**Step 8:** Power analysis and effect sizes
- Post-hoc power for observed effects
- Effect sizes: R-squared, Cohen's f-squared, standardized betas with 95% CIs
- Sensitivity analysis for smallest detectable effects

**Expected Outputs:**
- data/step01_theta_domains.csv (What/Where/When theta scores)
- data/step02_cognitive_tests.csv (extracted cognitive predictors)
- data/step03_analysis_input.csv (merged dataset)
- data/step04_univariate_results.csv (3 separate model results)
- data/step05_multivariate_results.csv (joint model results)
- data/step06_model_comparison.csv (AIC, R-squared comparison)
- data/step07_cross_validation.csv (CV performance metrics)
- data/step08_effect_sizes.csv (effect sizes with CIs)
- results/model_comparison_summary.md (interpretation for thesis)
- plots/model_comparison.png (visualization)
- plots/diagnostic_plots.png (residuals, assumptions)

**Success Criteria:**
- [ ] Both univariate and multivariate models converge successfully
- [ ] Model comparison completed with valid AIC values
- [ ] Cross-validation shows stable performance (test R-squared within 10% of training)
- [ ] Model diagnostics pass: VIF < 5, residuals normally distributed
- [ ] Effect sizes reported with 95% confidence intervals
- [ ] Dual p-value reporting (uncorrected and Bonferroni-corrected)
- [ ] Cross-domain correlations between 0.20-0.70 (supports multivariate approach)
- [ ] Clear interpretation of efficiency gains or lack thereof

---

## Data Source

**Data Type:**
DERIVED (from Ch5 5.2.X outputs + master.xlsx cognitive tests)

### DERIVED Data Sources:

**Source RQ:**
Ch5 5.2.X (Domain-specific analyses for What/Where/When theta scores)

**File Paths:**
- results/ch5/5.2.1/data/step03_theta_scores.csv (or appropriate domain RQ)
- results/ch5/5.2.2/data/step03_theta_scores.csv (or appropriate domain RQ)
- results/ch5/5.2.3/data/step03_theta_scores.csv (or appropriate domain RQ)
- data/cache/master.xlsx (cognitive test scores: RAVLT, BVMT, NART, RPM)

**Dependencies:**
Ch5 5.2.X domain analyses must complete (IRT calibration for domain-specific theta estimation) before this RQ can run.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions)
- Complete cognitive test data required
- Domain-specific theta scores available from Ch5

**Items:**
- N/A (theta scores already aggregated at participant level)

**Tests:**
- [x] Cognitive tests: RAVLT, BVMT, NART, RPM
- [x] Demographics: Age as covariate
- [ ] DASS-21 excluded (not part of core cognitive battery for this analysis)

---