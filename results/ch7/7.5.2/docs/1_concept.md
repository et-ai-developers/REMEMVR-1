# RQ 7.5.2: Does DASS predict memory performance?

**Chapter:** 7
**Type:** Psychological/Individual Differences
**Subtype:** Depression, Anxiety, Stress Scales (DASS-21)
**Full ID:** 7.5.2

---

## Research Question

**Primary Question:**
Do depression, anxiety, or stress (DASS-21 subscales) predict REMEMVR episodic memory accuracy?

**Scope:**
This RQ examines whether psychological distress measures (DASS-21: Depression, Anxiety, Stress subscales) predict episodic memory performance as measured by mean theta scores across all WWW domains. Analysis includes approximately 97 participants (some missing DASS data). Uses mean Theta_All per participant aggregated across all test sessions and memory domains.

**Theoretical Framing:**
Psychological distress may impair episodic memory through multiple mechanisms: depression reducing encoding motivation, anxiety consuming working memory resources during retrieval, and stress interfering with hippocampal consolidation processes. Small negative effects expected based on cognitive-emotional interaction literature.

---

## Theoretical Background

**Relevant Theories:**
- **Depression-Memory Model**: Depression may reduce encoding motivation and effortful processing, particularly affecting elaborative encoding strategies required for episodic memory formation
- **Anxiety-Working Memory Theory**: Anxiety consumes working memory resources during retrieval, reducing available capacity for episodic memory reconstruction
- **Stress-Hippocampal Theory**: Chronic stress and elevated cortisol impair hippocampal function, which is critical for episodic memory binding and consolidation

**Key Citations:**
Empirical literature on depression-memory relationships and anxiety effects on working memory during retrieval tasks

**Theoretical Predictions:**
Depression subscale: Negative relationship with memory accuracy due to reduced encoding motivation
Anxiety subscale: Negative relationship due to working memory interference during retrieval
Stress subscale: Negative relationship due to hippocampal dysfunction

**Literature Gaps:**
Most studies examine clinical populations or laboratory stressors; fewer studies examine subclinical psychological distress effects on complex spatial-temporal episodic memory in virtual environments

---

## Hypothesis

**Primary Hypothesis:**
Small negative effects expected for all three DASS subscales predicting REMEMVR accuracy, with depression showing the strongest effect due to encoding motivation impairment.

**Secondary Hypotheses:**
Effects will remain significant after controlling for age and cognitive ability (RAVLT), indicating unique psychological contribution beyond general cognitive functioning.

**Theoretical Rationale:**
Depression may impair encoding motivation and effortful processing. Anxiety may impair working memory during retrieval. Stress may interfere with hippocampal consolidation processes. All three mechanisms predict negative relationships with episodic memory performance.

**Expected Effect Pattern:**
Model: Theta ~ DASS_Dep + DASS_Anx + DASS_Str, Expected R² = 0.06 (small effect). No DASS subscale significantly predicts accuracy (all p > 0.10) due to subclinical levels in healthy sample.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Included in omnibus theta_all scores from Ch5 5.1.1

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location)
  - [x] `-U-` tags (pick-up location)  
  - [x] `-D-` tags (put-down location)
  - Description: Included in omnibus theta_all scores from Ch5 5.1.1

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Included in omnibus theta_all scores from Ch5 5.1.1

**Inclusion Rationale:**
Uses omnibus theta_all scores from Ch5 5.1.1 that aggregate across all episodic memory domains. Tests whether psychological distress affects general episodic memory ability rather than domain-specific effects.

**Exclusion Rationale:**
Not examining domain-specific effects since DASS measures represent general psychological distress rather than domain-specific cognitive mechanisms.

---

## Analysis Approach

**Analysis Type:**
Multiple regression with hierarchical entry and cross-validation

**High-Level Workflow:**

**Step 1:** Extract and prepare data
- Load mean theta_all scores from Ch5 5.1.1 results
- Extract DASS-21 subscale scores from master.xlsx: DASS_Dep, DASS_Anx, DASS_Str
- Extract control variables: Age, RAVLT total score
- Check for missing data (expected N H 97)

**Step 2:** Descriptive statistics for DASS
- Mean, SD, range for each subscale (Depression, Anxiety, Stress)
- Check for floor/ceiling effects
- Examine distribution normality

**Step 3:** Hierarchical regression
- Model 1: Theta ~ Age + RAVLT (control model)
- Model 2: Theta ~ Age + RAVLT + DASS_Dep + DASS_Anx + DASS_Str
- Test ”R² significance between models

**Step 4:** Test individual predictors
- Extract standardized beta coefficients with 95% CIs
- Compute semi-partial correlations (sr²) for unique variance
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Primary: Bonferroni correction (± = 0.00179/3 = 0.00060 for 3 DASS predictors)
- Secondary: FDR correction for comparison

**Step 5:** Model diagnostics
- Multicollinearity: VIF < 5 for all predictors
- Residual normality: Shapiro-Wilk test, Q-Q plot
- Homoscedasticity: Breusch-Pagan test
- Influential points: Cook's D < 4/N threshold

**Step 6:** Cross-validation
- Method: 5-fold CV
- Metrics: Test R², RMSE, MAE
- Check for overfitting (test R² vs training R²)

**Step 7:** Power analysis
- Post-hoc power for observed effect sizes
- Sensitivity analysis: smallest detectable effect at 80% power

**CRITICAL for Ch7 and multiple comparisons:**
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Include model diagnostics step (VIF, residuals, homoscedasticity)
- Include cross-validation for predictive models
- Include power analysis for null findings
- Include effect sizes with 95% CIs (R², f², sr², ²)

**Expected Outputs:**
- data/step01_dass_scores.csv (DASS subscale scores extracted)
- data/step02_theta_means.csv (mean theta_all per participant)
- data/step03_analysis_input.csv (merged analysis dataset)
- data/step04_hierarchical_regression.csv (model comparison results)
- data/step05_individual_predictors.csv (coefficients, CIs, dual p-values)
- data/step06_model_diagnostics.csv (VIF, residuals, Cook's D)
- data/step07_cross_validation.csv (k-fold CV results)
- data/step08_power_analysis.csv (post-hoc and sensitivity)
- results/dass_summary.md (text summary for thesis)
- plots/dass_diagnostic_plots.png (residuals, Q-Q, homoscedasticity)
- plots/dass_predictor_plot.png (visualization of predictor effects)

**Success Criteria:**
- Report DASS effects on accuracy (all three subscales)
- Compare to metacognition effects (from 7.3.4)
- Control for cognitive ability (age, RAVLT)
- Model convergence with all predictors included
- VIF < 5 for all predictors (no multicollinearity)
- Residuals normally distributed (Shapiro-Wilk p > 0.05)
- Homoscedasticity confirmed (Breusch-Pagan p > 0.05)
- No influential outliers (Cook's D < 4/N)
- Cross-validation R² within 10% of training R²
- Power analysis for null findings
- DASS descriptives: M, SD, range for all subscales

---

## Data Source

**Data Type:**
DERIVED (from Ch5 5.1.1 outputs + master.xlsx DASS scores)

### DERIVED Data Sources:

**Source RQ:**
Ch5 5.1.1 (General omnibus analysis providing theta_all scores)

**File Paths:**
- results/ch5/5.1.1/data/step03_theta_scores.csv (IRT ability estimates)
- data/cache/master.xlsx (DASS-21 subscale scores and covariates)

**Dependencies:**
Ch5 5.1.1 must complete Steps 1-3 (IRT calibration and theta estimation) before this RQ can run

### Predictor Variables from master.xlsx:

**DASS-21 Subscales:**
- Depression: {UID}-DEM-X-DASS_Dep
- Anxiety: {UID}-DEM-X-DASS_Anx  
- Stress: {UID}-DEM-X-DASS_Str

**Control Variables:**
- Age: {UID}-DEM-X-Age
- RAVLT Total: {UID}-COG-X-RAV-TotSc

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] Participants with complete DASS-21 data (expected N H 97)
- [ ] Exclude participants missing DASS subscale scores
- [x] Include participants with complete theta_all scores from Ch5 5.1.1

**Items:**
- N/A (uses aggregated theta_all scores, not item-level data)

**Tests:**
- [x] Uses mean theta_all aggregated across all test sessions (T1, T2, T3, T4)

---