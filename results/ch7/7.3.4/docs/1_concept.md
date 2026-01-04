# RQ 7.3.4: Does DASS predict metacognition more than memory?

**Chapter:** 7
**Type:** Age Moderation
**Subtype:** DASS Differential Prediction
**Full ID:** 7.3.4

---

## Research Question

**Primary Question:**
Does anxiety/depression predict metacognitive accuracy (confidence, calibration) more than memory accuracy?

**Scope:**
This RQ examines differential prediction patterns using DASS-21 scores (Depression, Anxiety, Stress) as predictors of three dependent variables: memory accuracy (theta scores), confidence scores, and calibration metrics. Analysis includes approximately 97 participants (some DASS missing) with comparison of standardized beta coefficients across models.

**Theoretical Framing:**
Tests whether anxiety/depression specifically impairs metacognitive monitoring (worry disrupts self-evaluation) without equally impairing memory encoding. If DASS selectively predicts confidence/calibration but not accuracy, this suggests domain-specific effects on executive monitoring rather than general memory deficits.

---

## Theoretical Background

**Relevant Theories:**
- **Executive Function Theory**: Anxiety impairs executive functions because worry occupies working memory resources. Metacognitive monitoring requires executive resources for self-evaluation and confidence assessment.
- **Processing Efficiency Theory** (Eysenck & Calvo, 1992): Anxiety affects processing efficiency (metacognitive monitoring) more than processing effectiveness (memory encoding), because encoding may be more automatic while monitoring requires controlled processing.
- **Dual-Process Theory**: Memory encoding can rely on automatic processes, while metacognitive assessment requires controlled, effortful evaluation that is more vulnerable to anxiety-related interference.

**Key Citations:**
- Eysenck & Calvo (1992): Processing efficiency vs effectiveness distinction
- Worry and working memory capacity interference literature
- Metacognitive monitoring as executive function

**Theoretical Predictions:**
Executive function theories predict DASS-Anxiety should more strongly impair metacognitive processes (confidence, calibration) that require controlled evaluation, while leaving more automatic memory encoding processes relatively intact.

**Literature Gaps:**
Limited research on differential effects of anxiety/depression on memory vs metacognitive accuracy in episodic memory tasks. Most studies examine either memory OR metacognition, not their relative vulnerability.

---

## Hypothesis

**Primary Hypothesis:**
DASS-Anxiety may impair metacognitive monitoring (worry disrupts self-evaluation) without impairing memory encoding. This would show as DASS predicting confidence/calibration but not accuracy.

**Secondary Hypotheses:**
DASS effects may persist even when controlling for cognitive ability (RAVLT, RPM), indicating specific anxiety effects rather than general cognitive impairment.

**Theoretical Rationale:**
Anxiety impairs executive functions because worry occupies working memory. Metacognitive monitoring requires executive resources. Memory encoding may be more automatic and less affected by anxiety.

**Expected Effect Pattern:**
Expected pattern: DASS_Anx shows stronger (more negative) beta coefficients for Confidence and Calibration models compared to Accuracy model. DASS_Dep and DASS_Str may show similar but weaker patterns.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Included in overall theta_all scores

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location)
  - [x] `-U-` tags (pick-up location) 
  - [x] `-D-` tags (put-down location)
  - Description: Included in overall theta_all scores

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Included in overall theta_all scores

**Inclusion Rationale:**
Uses omnibus theta_all scores from Ch5 and confidence/calibration scores from Ch6 that aggregate across all episodic memory domains to provide comprehensive measures of memory and metacognitive accuracy.

**Exclusion Rationale:**
None - uses aggregate scores across all domains for maximum statistical power and comprehensive assessment of general memory and metacognitive abilities.

---

## Analysis Approach

**Analysis Type:**
Multiple regression with hierarchical entry and cross-validation

**High-Level Workflow:**

**Step 1:** Extract and prepare data
- Load theta scores from Ch5 results (overall memory accuracy)
- Load confidence and calibration scores from Ch6 results
- Extract DASS-21 scores from dfnonvr.csv
- Check data quality and missingness patterns

**Step 2:** Fit models for each dependent variable
- Model_Accuracy: `Theta ~ DASS_Dep + DASS_Anx + DASS_Str`
- Model_Confidence: `Confidence ~ DASS_Dep + DASS_Anx + DASS_Str` 
- Model_Calibration: `Calibration ~ DASS_Dep + DASS_Anx + DASS_Str`

**Step 3:** Compare beta coefficients across models
- Extract standardized betas with 95% CIs
- Test differential prediction: Does DASS_Anx predict metacognition more than accuracy?
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Primary: Bonferroni correction for multiple comparisons

**Step 4:** Control for cognitive ability
- Add RAVLT, RPM as covariates to all models
- Test whether DASS effects remain significant
- Assess incremental validity of DASS beyond cognitive ability

**Step 5:** Model diagnostics
- Multicollinearity: VIF < 5 for all predictors
- Residual normality: Shapiro-Wilk test, Q-Q plot
- Homoscedasticity: Breusch-Pagan test
- Influential points: Cook's D < 4/N

**Step 6:** Cross-validation
- Method: 5-fold CV for each model
- Metrics: Test R, RMSE, MAE
- Check for overfitting across all three models

**Step 7:** Power analysis
- Post-hoc power for observed effects
- Sensitivity: smallest detectable effect at 80% power

**Expected Outputs:**
- data/step01_dass_scores.csv (extracted DASS-21 scores)
- data/step02_theta_confidence.csv (memory and metacognitive DVs)
- data/step03_analysis_input.csv (merged analysis dataset)
- data/step04_regression_results.csv (coefficients, CIs, dual p-values for all 3 models)
- data/step05_model_diagnostics.csv (VIF, residuals, Cook's D for each model)
- data/step06_effect_sizes.csv (R, f, sr with 95% CIs)
- data/step07_cross_validation.csv (k-fold CV results)
- data/step08_power_analysis.csv (post-hoc and sensitivity)
- data/step09_covariate_models.csv (results with RAVLT/RPM controls)
- results/dass_differential_prediction.md (text summary for thesis)
- plots/diagnostic_plots.png (residuals, Q-Q, homoscedasticity)
- plots/beta_comparison.png (side-by-side beta coefficients)

**Success Criteria:**
- [ ] All three models converge and meet diagnostic requirements
- [ ] Compare DASS effects on accuracy vs metacognition
- [ ] Report if DASS_Anx shows differential prediction
- [ ] Control for cognitive ability to rule out confound
- [ ] VIF < 5 for all predictors (no multicollinearity)
- [ ] Residuals normally distributed (Shapiro-Wilk p > 0.05)
- [ ] Cross-validation R within 10% of training R
- [ ] Power > 0.80 for medium effect (f = 0.15)

---

## Data Source

**Data Type:**
DERIVED (from Ch5 X.Y.Z outputs + Ch6 X.Y.Z outputs + master.xlsx DASS scores)

### DERIVED Data Sources:

**Source RQs:**
- Ch5: Overall theta scores (omnibus memory accuracy)
- Ch6: Confidence and calibration scores
- master.xlsx: DASS-21 Depression, Anxiety, Stress scores

**File Paths:**
- results/ch5/5.1.1/data/step03_theta_scores.csv (or equivalent omnibus theta scores)
- results/ch6/6.2.x/data/calibration_scores.csv (calibration metrics per participant)
- results/ch6/6.1.x/data/confidence_scores.csv (mean confidence per participant)
- data/cache/master.xlsx (DASS-21 scores)

**Dependencies:**
Ch5 overall theta estimation and Ch6 confidence/calibration analyses must complete before this RQ can run.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants with complete DASS-21 data (~97 participants)
- [ ] Exclude: Participants with missing DASS scores

**Items:**
- N/A (uses aggregate theta, confidence, and calibration scores)

**Tests:**
- [x] DASS-21 Depression subscale (7 items)
- [x] DASS-21 Anxiety subscale (7 items) 
- [x] DASS-21 Stress subscale (7 items)

---