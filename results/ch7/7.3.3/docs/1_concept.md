# RQ 7.3.3: Cognitive Predictors of High-Confidence Errors

**Chapter:** 7
**Type:** Metacognition Predictors
**Subtype:** HCE Rate Prediction
**Full ID:** 7.3.3

---

## Research Question

**Primary Question:**
Do cognitive tests predict who makes more high-confidence errors (HCE)? Ch6 found 15-20% stable HCE rate - do individual differences have cognitive predictors?

**Scope:**
This RQ examines predictors of high-confidence error rates using HCE data from Ch6 and cognitive test scores from dfnonvr.csv. Tests individual differences in metacognitive monitoring failure across N=100 participants. HCE rate defined as proportion of errors that are high-confidence (from Ch6 6.6.x analyses).

**Theoretical Framing:**
Tests whether executive functions (measured by RPM) predict better metacognitive monitoring, while memory capacity tests (RAVLT/BVMT) may not predict monitoring accuracy. HCE represents a specific monitoring failure where confidence exceeds accuracy.

---

## Theoretical Background

**Relevant Theories:**
- **Executive Control Theory**: Metacognitive monitoring requires executive resources to detect errors and calibrate confidence appropriately. Lower executive capacity should predict more monitoring failures (HCEs).
- **Dual-Process Theory**: Memory retrieval relies on familiarity (automatic) and recollection (controlled). Monitoring quality may depend on controlled processes measured by fluid intelligence tests.

**Key Citations:**

**Theoretical Predictions:**
RPM (fluid intelligence) should negatively predict HCE rate as it measures executive control needed for error detection. RAVLT/BVMT measure memory capacity which is theoretically orthogonal to monitoring accuracy - encoding ability does not guarantee monitoring accuracy.

**Literature Gaps:**
Limited research on individual differences in metacognitive monitoring failure, particularly in episodic memory contexts.

---

## Hypothesis

**Primary Hypothesis:**
Lower RPM scores predict higher HCE rates. RPM measures fluid intelligence and executive control necessary for metacognitive monitoring and error detection. Participants with lower RPM should show more monitoring failures (confident when wrong).

**Secondary Hypotheses:**
RAVLT and BVMT scores will not significantly predict HCE rates. Memory capacity (encoding ability) is theoretically orthogonal to monitoring accuracy - being able to encode information does not guarantee accurate confidence calibration.

**Theoretical Rationale:**
HCE represents monitoring failure - being confident when wrong. This requires executive control to detect errors before expressing confidence. If RPM measures executive capacity, lower RPM should predict more HCEs. Memory tests measure encoding capacity, not monitoring accuracy.

**Expected Effect Pattern:**
Significant negative correlation between RPM and HCE rate ( = -0.28, p < 0.01). RAVLT and BVMT effects should be non-significant (p > 0.05). Model R expected around 0.15, indicating individual differences in monitoring failure are partially predictable.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Included in HCE rate calculations from Ch6

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Description: Included in HCE rate calculations from Ch6

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Included in HCE rate calculations from Ch6

**Inclusion Rationale:**
Uses HCE rates from Ch6 6.6.x that aggregate across all episodic memory domains. Individual domain HCE rates may be examined in secondary analyses to test whether monitoring failure is domain-general or domain-specific.

**Exclusion Rationale:**
None - all episodic memory domains included in omnibus HCE rate calculations.

---

## Analysis Approach

**Analysis Type:**
Multiple regression with hierarchical entry and cross-validation

**High-Level Workflow:**

**Step 1:** Extract and prepare data
- Load HCE rates from Ch6 6.6.x results
- Extract cognitive tests from dfnonvr.csv (RAVLT_T, BVMT_T, RPM_T, Age)
- Compute derived scores and standardize to T-scores
- Check data quality and missingness

**Step 2:** Hierarchical regression
- Model 1: Demographics only (Age, Sex, Education)
- Model 2: + Cognitive tests (RAVLT_T, BVMT_T, RPM_T)
- Report R and F-test for model improvement

**Step 3:** Test individual predictors
- Extract standardized betas with 95% CIs
- Compute semi-partial correlations (sr)
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Primary: Bonferroni ( = 0.00179/4 = 0.000448)
- Secondary: FDR for comparison

**Step 4:** Effect sizes and importance
- Cohen's f = R/(1-R)
- Dominance analysis or relative weights
- Bootstrap CIs (1000 iterations)

**Step 5:** Model diagnostics
- Multicollinearity: VIF < 5
- Residual normality: Shapiro-Wilk test, Q-Q plot
- Homoscedasticity: Breusch-Pagan test
- Influential points: Cook's D < 4/N

**Step 6:** Cross-validation
- Method: 5-fold CV
- Metrics: Test R, RMSE, MAE
- Check for overfitting

**Step 7:** Power analysis
- Post-hoc power for observed effects
- Sensitivity: smallest detectable effect at 80% power

**Step 8:** Sensitivity analyses
- Exclude outliers, rerun
- Try robust regression if needed
- Compare Bonferroni vs FDR results

**Expected Outputs:**
- data/step01_cognitive_tests.csv (extracted test scores)
- data/step02_hce_rates.csv (HCE rates per participant from Ch6)
- data/step03_analysis_input.csv (merged analysis dataset)
- data/step04_regression_results.csv (coefficients, CIs, dual p-values)
- data/step05_model_diagnostics.csv (VIF, residuals, Cook's D)
- data/step06_effect_sizes.csv (R, f, sr, with 95% CIs)
- data/step07_cross_validation.csv (k-fold CV results)
- data/step08_power_analysis.csv (post-hoc and sensitivity)
- results/hce_prediction_summary.md (text summary for thesis)
- plots/diagnostic_plots.png (residuals, Q-Q, homoscedasticity)
- plots/hce_predictor_effects.png (visualization of effects)

**Success Criteria:**
- [ ] HCE rate has identifiable predictors (Model R > 0.10)
- [ ] RPM significantly predicts HCE rate ( < 0, p < 0.000448)
- [ ] Effect direction matches hypothesis (negative RPM-HCE correlation)
- [ ] VIF < 5 for all predictors (no multicollinearity)
- [ ] Residuals normally distributed (Shapiro-Wilk p > 0.05)
- [ ] Homoscedasticity confirmed (Breusch-Pagan p > 0.05)
- [ ] No influential outliers (Cook's D < 4/N)
- [ ] Cross-validation R within 10% of training R
- [ ] Connect findings to Ch6 HCE mechanism interpretation

---

## Data Source

**Data Type:**
DERIVED (from Ch6 6.6.x outputs + master.xlsx cognitive tests)

### DERIVED Data Sources:

**Source RQ:**
Ch6 6.6.1 or equivalent (HCE rate calculations)

**File Paths:**
- results/ch6/6.6.1/data/step03_hce_rates.csv (or equivalent HCE output)
- data/cache/master.xlsx (cognitive test scores: RAVLT_T, BVMT_T, RPM_T)

**Dependencies:**
Ch6 6.6.x must complete HCE rate calculations before this RQ can run

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants with HCE data
- [ ] Exclude: Participants with missing cognitive test scores (if any)

**Items:**
- N/A (HCE rates already computed per participant)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4) included in HCE rate calculations

---