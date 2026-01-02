# RQ 7.6.1: Cognitive Tests Predicting Individual Differences in Forgetting Rate

**Chapter:** 7
**Type:** Individual Differences in Forgetting
**Subtype:** Cognitive Test Prediction of Slope
**Full ID:** 7.6.1

---

## Research Question

**Primary Question:**
Do cognitive tests predict the rate of forgetting (slope), or only initial encoding (intercept)?

**Scope:**
This RQ examines whether traditional cognitive assessments (RAVLT, BVMT, RPM) predict individual differences in REMEMVR forgetting slopes estimated from model-averaged LMM results. Analysis uses per-participant slope estimates from Ch5 5.1.4 model-averaged random effects combined with cognitive test scores from master.xlsx. N=100 participants.

**Theoretical Framing:**
Tests differential prediction hypothesis that cognitive tests predict encoding abilities (intercepts) but not consolidation/forgetting processes (slopes). Builds on Ch5 finding that ICC_slope = 21% showing substantial individual differences in forgetting rates exist.

---

## Theoretical Background

**Relevant Theories:**
- **Encoding-Consolidation Dissociation Theory**: Traditional cognitive tests measure immediate recall/encoding capacity, which differs from multi-day consolidation processes that govern forgetting slopes.
- **Individual Differences Framework**: People vary in both encoding ability and consolidation efficiency, but these may be independent processes with different neural substrates.
- **Systems Consolidation Theory**: Forgetting over days reflects hippocampal-to-neocortical transfer efficiency, which may not be captured by standard neuropsychological assessments.

**Key Citations:**

**Theoretical Predictions:**
Cognitive tests should predict intercepts (initial encoding strength) but NOT slopes (forgetting rates). Consolidation processes that govern multi-day retention may be independent from encoding processes measured by traditional tests.

**Literature Gaps:**
Most research focuses on encoding prediction; few studies examine whether cognitive tests predict individual differences in forgetting rates across extended retention intervals.

---

## Hypothesis

**Primary Hypothesis:**
Cognitive tests (RAVLT_T, BVMT_T, RPM_T) should NOT significantly predict REMEMVR forgetting slopes. Model R² should be low (< 0.10) and non-significant.

**Secondary Hypotheses:**
R²_slope should be substantially lower than R²_intercept found in RQ 7.1.2, demonstrating differential prediction patterns for encoding vs. consolidation processes.

**Theoretical Rationale:**
Slopes reflect consolidation/forgetting processes occurring over days, which differ from encoding processes measured by traditional tests. Ch5 found ICC_slope = 21% indicating individual differences exist, but these may not be predicted by standard cognitive assessments.

**Expected Effect Pattern:**
Model: Slope ~ RAVLT_T + BVMT_T + RPM_T should show R² < 0.10, F(3,96) non-significant (p > 0.10). Individual predictors should all have p > 0.10 after multiple comparison correction.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Included in model-averaged slopes from Ch5 omnibus analysis

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Description: Included in model-averaged slopes from Ch5 omnibus analysis

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Included in model-averaged slopes from Ch5 omnibus analysis

**Inclusion Rationale:**
Uses model-averaged slopes from Ch5 5.1.4 that aggregate across all episodic memory domains, providing comprehensive measure of individual differences in forgetting rate.

**Exclusion Rationale:**
No domain exclusions. Analysis uses omnibus slopes that incorporate all WWW domains to maximize reliability of individual difference estimates.

---

## Analysis Approach

**Analysis Type:**
Multiple regression with hierarchical entry, cross-validation, and extensive diagnostics

**High-Level Workflow:**

**Step 1:** Extract and prepare data
- Load model-averaged slopes from Ch5 5.1.4 results
- Extract cognitive test scores from master.xlsx (RAVLT_T, BVMT_T, RPM_T)
- Standardize predictors to T-scores for interpretability
- Check data quality and missingness patterns

**Step 2:** Hierarchical regression
- Model 1: Demographics only (Age, Sex, Education)  
- Model 2: + Cognitive tests (RAVLT_T, BVMT_T, RPM_T)
- Report ”R² and F-test for model improvement

**Step 3:** Test individual predictors
- Extract standardized betas with 95% confidence intervals
- Compute semi-partial correlations (sr²) for unique variance
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Primary correction: Bonferroni (± = 0.00179/4 = 0.000448)
- Secondary: FDR correction for comparison

**Step 4:** Effect sizes and importance
- Cohen's f² = R²/(1-R²) for overall model
- Dominance analysis for predictor importance ranking
- Bootstrap confidence intervals (1000 iterations)

**Step 5:** Model diagnostics
- Multicollinearity: VIF < 5 for all predictors
- Residual normality: Shapiro-Wilk test, Q-Q plot
- Homoscedasticity: Breusch-Pagan test, residual vs fitted plot
- Influential points: Cook's D < 4/N threshold

**Step 6:** Cross-validation
- Method: 5-fold cross-validation
- Metrics: Test R², RMSE, MAE
- Check for overfitting (test R² << training R²)

**Step 7:** Power analysis
- Post-hoc power for observed effect sizes
- Sensitivity analysis: smallest detectable effect at 80% power
- Sample size adequacy for number of predictors

**Step 8:** Sensitivity analyses
- Exclude potential outliers, rerun analysis
- Try robust regression if outliers present
- Compare Bonferroni vs FDR correction results

**Expected Outputs:**
- data/step01_cognitive_tests.csv (extracted test scores)
- data/step02_slopes_extracted.csv (model-averaged slopes from Ch5)
- data/step03_analysis_input.csv (merged analysis dataset)
- data/step04_regression_results.csv (coefficients, CIs, dual p-values)
- data/step05_model_diagnostics.csv (VIF, residuals, Cook's D)
- data/step06_effect_sizes.csv (R², f², sr², with 95% CIs)
- data/step07_cross_validation.csv (5-fold CV results)
- data/step08_power_analysis.csv (post-hoc and sensitivity)
- results/slope_prediction_summary.md (text summary for thesis)
- plots/diagnostic_plots.png (residuals, Q-Q, homoscedasticity)
- plots/slope_prediction.png (predictor importance visualization)

**Success Criteria:**
- [ ] Model R² < 0.10 and non-significant (p > 0.00179)
- [ ] No individual predictor significant after Bonferroni correction
- [ ] R²_slope substantially < R²_intercept (from RQ 7.1.2)
- [ ] VIF < 5 for all predictors (no multicollinearity)
- [ ] Residuals normally distributed (Shapiro-Wilk p > 0.05)
- [ ] Homoscedasticity confirmed (Breusch-Pagan p > 0.05)
- [ ] No influential outliers (Cook's D < 4/N)
- [ ] Cross-validation R² within 10% of training R²
- [ ] Power analysis confirms adequate sample size

---

## Data Source

**Data Type:**
DERIVED (from Ch5 5.1.4 model-averaged outputs + master.xlsx cognitive tests)

### DERIVED Data Sources:

**Source RQ:**
Ch5 5.1.4 (Model-averaged forgetting trajectories) 

**File Paths:**
- results/ch5/5.1.4/data/step03_model_averaged_slopes.csv (per-participant slope estimates)
- data/cache/master.xlsx (cognitive test scores: RAVLT_T, BVMT_T, RPM_T)

**Dependencies:**
Ch5 5.1.4 must complete model averaging and extract individual slope estimates before this RQ can run. Requires successful completion of Ch5 omnibus trajectory analysis.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions)
- [ ] Subset criteria: N/A
- [ ] Exclude criteria: N/A

**Items:**
- N/A (uses aggregated slope estimates, not item-level data)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4) - slopes estimated from complete trajectory

---