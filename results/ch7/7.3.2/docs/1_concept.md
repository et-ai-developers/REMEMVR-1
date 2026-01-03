# RQ 7.3.2: Cognitive Predictors of Calibration Quality

**Chapter:** 7
**Type:** Individual Differences in Metacognition
**Subtype:** Calibration Quality Prediction
**Full ID:** 7.3.2

---

## Research Question

**Primary Question:**
Do cognitive tests predict who is well-calibrated (confidence matches accuracy) vs overconfident (confidence exceeds accuracy)?

**Scope:**
This RQ examines individual differences in calibration quality using cognitive test scores as predictors. Calibration metrics are derived from Ch6 per-participant measures. Analysis includes 100 participants with standardized cognitive test scores from master.xlsx. Compares predictive validity of memory tests (RAVLT, BVMT) vs fluid intelligence (RPM).

**Theoretical Framing:**
Calibration quality represents metacognitive accuracy - the ability to match confidence judgments to actual performance. This requires executive control processes to monitor internal confidence signals and compare them to objective performance, which may be better predicted by reasoning ability than memory capacity.

---

## Theoretical Background

**Relevant Theories:**
- **Metacognitive Theory** (Flavell, 1979): Calibration requires metacognitive monitoring - awareness of one's own cognitive processes and performance. This executive function may be dissociated from memory encoding capacity.
- **Dual-Process Theory** applied to metacognition: Confidence judgments rely on both automatic retrieval fluency and controlled monitoring processes. Calibration quality may depend more on controlled processes.

**Key Citations:**

**Theoretical Predictions:**
Calibration requires comparing internal confidence signals to actual performance - a metacognitive executive function that should correlate with fluid reasoning (RPM) more than memory capacity (RAVLT, BVMT). This differs from memory encoding capacity which relies on domain-specific memory systems.

**Literature Gaps:**
Limited research on individual differences in calibration quality and their cognitive predictors, particularly in episodic memory contexts with rich confidence-accuracy data.

---

## Hypothesis

**Primary Hypothesis:**
RPM (fluid intelligence) will predict calibration quality more strongly than RAVLT or BVMT (memory tests). Metacognitive monitoring requires reasoning abilities to compare internal confidence states to performance, which should correlate with fluid intelligence measures.

**Secondary Hypotheses:**
RAVLT and BVMT will show minimal prediction of calibration quality, as memory encoding capacity is theoretically orthogonal to metacognitive monitoring accuracy.

**Theoretical Rationale:**
Calibration requires executive control to detect discrepancies between confidence and accuracy. Fluid intelligence (RPM) measures executive reasoning capacity that should support metacognitive monitoring, while memory capacity tests (RAVLT, BVMT) measure encoding/retrieval abilities that are distinct from monitoring processes.

**Expected Effect Pattern:**
Multiple regression model: Calibration ~ RAVLT_T + BVMT_T + RPM_T. Expected: RPM � > 0.20 (p < 0.05), RAVLT/BVMT � H 0 (p > 0.10). Overall R� modest (0.10-0.20) reflecting individual differences complexity.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Included in calibration metrics from Ch6

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Description: Included in calibration metrics from Ch6

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Included in calibration metrics from Ch6

**Inclusion Rationale:**
Uses calibration metrics derived from Ch6 analyses that aggregate across all episodic memory domains. Individual differences in calibration quality are computed as per-participant measures across the full range of episodic memory content.

**Exclusion Rationale:**
None - calibration quality is a domain-general metacognitive measure computed across all memory content types.

---

## Analysis Approach

**Analysis Type:**
Multiple regression with hierarchical entry, cross-validation, and comprehensive diagnostics

**High-Level Workflow:**

**Step 1:** Extract and prepare data
- Load calibration metrics from Ch6 6.2.x results (resolution, calibration slope, or Brier reliability)
- Extract cognitive tests from master.xlsx (RAVLT_T, BVMT_T, RPM_T)
- Compute per-participant calibration quality scores
- Check data quality and missingness patterns

**Step 2:** Hierarchical regression
- Model 1: Demographics only (Age, Sex, Education)
- Model 2: + Cognitive tests (RAVLT_T, BVMT_T, RPM_T)
- Report �R� and F-test for model improvement

**Step 3:** Test individual predictors
- Extract standardized beta coefficients with 95% CIs
- Compute semi-partial correlations (sr�) for unique variance
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Primary correction: Bonferroni (� = 0.00179/3 = 0.000597 for 3 cognitive tests)
- Secondary: FDR correction for comparison

**Step 4:** Effect sizes and importance
- Cohen's f� = R�/(1-R�) for overall model
- Standardized betas with 95% confidence intervals
- Semi-partial correlations for unique variance explained
- Bootstrap CIs (1000 iterations) for robust estimates

**Step 5:** Model diagnostics
- Multicollinearity: VIF < 5 for all predictors
- Residual normality: Shapiro-Wilk test, Q-Q plot
- Homoscedasticity: Breusch-Pagan test, residual vs fitted plot
- Influential points: Cook's D < 4/N threshold
- Outliers: Standardized residuals within ±3

**Remedial Actions for Assumption Violations:**
- If multicollinearity (VIF > 5): Use ridge regression or remove correlated predictors
- If non-normal residuals: Apply robust standard errors (HC3) or bootstrap inference
- If heteroscedasticity detected: Use weighted least squares or heteroscedasticity-consistent (HC3) standard errors
- If influential points (Cook's D > 4/N): Run sensitivity analysis with/without influential cases
- If outliers present: Report results with and without outliers, or use robust regression (Huber M-estimator)

**Step 6:** Cross-validation
- Method: 5-fold cross-validation
- Metrics: Test R�, RMSE, MAE
- Check for overfitting (test R� vs training R�)

**Step 7:** Power analysis
- Post-hoc power for observed effect sizes
- Sensitivity analysis: smallest detectable effect at 80% power
- Sample size adequacy assessment

**Step 8:** Compare to accuracy prediction
- Compare R� for calibration vs accuracy prediction (from 7.1.1)
- Identify which tests predict calibration vs accuracy differently
- Connect findings to Ch6 confidence-accuracy dissociation

**Expected Outputs:**
- data/step01_calibration_metrics.csv (per-participant calibration scores)
- data/step02_cognitive_tests.csv (extracted test scores from master.xlsx)
- data/step03_analysis_input.csv (merged dataset for regression)
- data/step04_regression_results.csv (coefficients, CIs, dual p-values)
- data/step05_model_diagnostics.csv (VIF, residuals, Cook's D)
- data/step06_effect_sizes.csv (R�, f�, sr� with 95% CIs)
- data/step07_cross_validation.csv (k-fold CV results)
- data/step08_power_analysis.csv (post-hoc and sensitivity analysis)
- data/step09_accuracy_comparison.csv (comparison with 7.1.1 results)
- results/calibration_prediction_summary.md (text summary for thesis)
- plots/diagnostic_plots.png (residuals, Q-Q, homoscedasticity)
- plots/predictor_importance.png (calibration vs accuracy prediction comparison)

**Success Criteria:**
- R� for calibration prediction < R� for accuracy prediction (calibration is harder to predict)
- At least modest prediction: R� > 0.05, p < 0.05
- Identify which cognitive test(s) predict calibration quality after correction
- VIF < 5 for all predictors (no multicollinearity)
- Residuals normally distributed (Shapiro-Wilk p > 0.05)
- Homoscedasticity confirmed (Breusch-Pagan p > 0.05)
- No influential outliers (Cook's D < 4/N = 0.04)
- Cross-validation R� within 10% of training R�
- Power > 0.60 for small-medium effect (f� = 0.10)
- Theoretical interpretation connecting to metacognition literature

---

## Data Source

**Data Type:**
DERIVED (from Ch6 calibration outputs + master.xlsx cognitive tests)

### DERIVED Data Sources:

**Source RQ:**
Ch6 6.2.x (Calibration Quality Analysis - specific RQ to be determined based on best calibration metric)

**File Paths:**
- results/ch6/6.2.x/data/step##_calibration_metrics.csv (per-participant calibration measures)
- data/cache/master.xlsx (cognitive test scores: RAVLT_T, BVMT_T, RPM_T)

**Dependencies:**
Ch6 6.2.x must complete calibration analysis before this RQ can run. Requires per-participant calibration quality metrics (resolution, calibration slope, or Brier reliability component).

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (those with complete cognitive test data)
- [x] Exclude: Participants missing calibration metrics from Ch6
- [x] Exclude: Participants missing cognitive test scores in master.xlsx

**Items:**
- N/A (calibration metrics are participant-level aggregates)

**Tests:**
- [x] Calibration metrics aggregate across all 4 tests (T1, T2, T3, T4)
- [x] Cognitive tests: Baseline administration (not time-dependent)

---