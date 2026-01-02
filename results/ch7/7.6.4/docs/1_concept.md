# RQ 7.6.4: Purification & Slope Predictors (NEW)

**Chapter:** 7
**Type:** Individual Differences in Forgetting Trajectories
**Subtype:** Purification & Slope predictors
**Full ID:** 7.6.4

---

## Research Question

**Primary Question:**
Do predictors of slope CHANGE after IRT purification? Ch5 found purification-trajectory paradox.

**Scope:**
This RQ examines whether cognitive test predictors (RAVLT, BVMT, RPM) of forgetting slope differ between pre-purification (IRT Pass 1) and post-purification (IRT Pass 2) models. Investigates the purification paradox found in Chapter 5 where purification improved static fit but worsened dynamic fit. N=100 participants.

**Theoretical Framing:**
Explores the purification-trajectory paradox from Ch5, where item purification improved model fit but changed trajectory patterns. Understanding whether predictors change after purification informs the paradox and has implications for IRT methodology in longitudinal research.

---

## Theoretical Background

**Relevant Theories:**
- **IRT Purification Theory**: Removing poorly-performing items should improve measurement precision and enhance construct validity
- **Individual Differences in Forgetting**: Cognitive abilities predict individual differences in memory decay trajectories
- **Measurement Invariance**: Item set changes may alter construct representation and predictor relationships

**Key Citations:**


**Theoretical Predictions:**
IRT theory predicts that purification should strengthen predictor relationships by removing measurement noise. However, the Ch5 purification paradox suggests that removing items may fundamentally change what is being measured longitudinally.

**Literature Gaps:**
Limited research on how IRT purification affects predictor relationships in longitudinal designs. The purification-trajectory paradox identified in Ch5 requires investigation of its implications for individual differences research.

---

## Hypothesis

**Primary Hypothesis:**
Predictor relationships will weaken after purification, consistent with the Ch5 purification-trajectory paradox. Post-purification slopes will show reduced R² and weaker standardized betas for cognitive test predictors.

**Secondary Hypotheses:**
The pattern will be strongest for BVMT (spatial memory) given Where domain's sensitivity to purification effects observed in Ch5.

**Theoretical Rationale:**
The purification paradox suggests that purification may remove items that are diagnostic of individual differences in trajectory patterns. If purification changes what items contribute to scores over time, predictors of those trajectories should also change.

**Expected Effect Pattern:**
Pre-purification R² > Post-purification R² for cognitive test prediction models. Individual predictor betas expected to be attenuated after purification, with some predictors potentially losing significance.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Included in overall slope estimates from Ch5 omnibus analysis

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location)
  - [x] `-U-` tags (pick-up location)  
  - [x] `-D-` tags (put-down location)
  - Description: Included in overall slope estimates from Ch5 omnibus analysis

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Included in overall slope estimates from Ch5 omnibus analysis

**Inclusion Rationale:**
Uses omnibus slope estimates from Ch5 that aggregate across all episodic memory domains to examine the purification effect on individual differences predictors.

**Exclusion Rationale:**
No domain-specific exclusions. Analysis uses aggregated slopes from Ch5 omnibus factor.

---

## Analysis Approach

**Analysis Type:**
Multiple regression with hierarchical entry, comparing prediction models before and after IRT purification

**High-Level Workflow:**

**Step 1:** Extract pre- and post-purification slopes
- Load IRT Pass 1 slopes (pre-purification) from Ch5 analysis
- Load IRT Pass 2 slopes (post-purification) from Ch5 analysis  
- Extract cognitive test scores from master.xlsx
- Standardize all variables to T-scores (M=50, SD=10)

**Step 2:** Fit prediction models for each purification pass
- Model_Pass1: `Slope_Pass1 ~ RAVLT_Total + BVMT_Total + RPM_Total`
- Model_Pass2: `Slope_Pass2 ~ RAVLT_Total + BVMT_Total + RPM_Total`
- Include demographics as covariates: Age, Sex, Education

**Step 3:** Compare model performance
- Extract R² and Adjusted R² for each model
- Test difference in R² between passes using F-test
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Primary correction: Bonferroni (± = 0.05/2 = 0.025 for two models)

**Step 4:** Compare individual predictors
- Extract standardized betas with 95% CIs for each predictor
- Compute semi-partial correlations (sr²) for unique variance
- Test coefficient differences using z-tests for dependent correlations
- Report effect sizes: Cohen's f² for each model

**Step 5:** Model diagnostics
- Multicollinearity: VIF < 5 for all predictors
- Residual normality: Shapiro-Wilk test, Q-Q plots
- Homoscedasticity: Breusch-Pagan test  
- Influential points: Cook's D < 4/N threshold

**Step 6:** Bootstrap confidence intervals
- Bootstrap coefficient differences (1000 iterations)
- Robust estimation of coefficient change significance
- Address potential non-normality in slope distributions

**Step 7:** Power analysis
- Post-hoc power for observed coefficient differences
- Sensitivity analysis: smallest detectable difference at 80% power

**Expected Outputs:**
- data/step01_slope_data.csv (extracted pre/post-purification slopes)
- data/step02_cognitive_tests.csv (standardized cognitive test scores)
- data/step03_analysis_input.csv (merged dataset for analysis)
- data/step04_pass1_regression.csv (pre-purification model results)
- data/step05_pass2_regression.csv (post-purification model results)
- data/step06_coefficient_comparison.csv (coefficient differences with CIs)
- data/step07_model_diagnostics.csv (VIF, residuals, diagnostics)
- data/step08_bootstrap_results.csv (bootstrapped coefficient CIs)
- data/step09_power_analysis.csv (power calculations)
- results/purification_comparison_summary.md (text summary for thesis)
- plots/coefficient_comparison.png (before/after visualization)
- plots/diagnostic_plots.png (residuals, Q-Q plots)

**Success Criteria:**
- [ ] Both prediction models converge successfully
- [ ] Coefficient differences detectable with 95% CIs not overlapping zero
- [ ] Consistent pattern across multiple predictors (not just random variation)
- [ ] Model diagnostics satisfied for both models (VIF < 5, normality, homoscedasticity)
- [ ] Bootstrap CIs confirm coefficient difference significance
- [ ] Power > 0.80 for detecting medium effect size differences (”² e 0.30)
- [ ] Results interpretable in context of Ch5 purification paradox

---

## Data Source

**Data Type:**
DERIVED (from Ch5 IRT slope analyses + master.xlsx cognitive tests)

### DERIVED Data Sources:

**Source RQ:**
Ch5 5.2.5 or equivalent slope analysis (pre- and post-purification IRT passes)

**File Paths:**
- results/ch5/5.2.5/data/step03_pass1_slopes.csv (pre-purification individual slopes)
- results/ch5/5.2.5/data/step06_pass2_slopes.csv (post-purification individual slopes)
- data/cache/master.xlsx (cognitive test scores: RAVLT, BVMT, RPM)

**Dependencies:**
Ch5 5.2.5 (or equivalent slope analysis) must complete both IRT passes before this RQ can run. Requires both pre- and post-purification slope estimates.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants with valid slope estimates from both IRT passes
- [ ] Exclude: Participants with failed IRT estimation in either pass

**Measures:**
- [x] IRT-derived forgetting slopes (individual random slopes from LMM)
- [x] RAVLT Total Score (sum of T1-T5 learning trials)
- [x] BVMT Total Recall Score (sum of T1-T3 learning trials)  
- [x] RPM Total Score (fluid intelligence)
- [x] Demographics: Age, Sex, Education as covariates

**Tests:**
- [x] Slope estimates from all 4 test sessions (T1, T2, T3, T4)
- [ ] Single time-point analyses excluded (not relevant for slopes)

---