# RQ 7.7.3: Alternative RAVLT Scoring

**Chapter:** 7
**Type:** Clinical Utility & Alternative Interpretation
**Subtype:** Alternative RAVLT Scoring
**Full ID:** 7.7.3

---

## Research Question

**Primary Question:**
Does RAVLT Learning Slope (T5-T1/T1) predict REMEMVR better than RAVLT Total? Can we suggest better RAVLT interpretation?

**Scope:**
This RQ compares multiple RAVLT scoring approaches to predict episodic memory performance measured via REMEMVR theta scores. Tests traditional Total score vs Learning gain vs proportional Learning Slope vs Recognition scores to determine which RAVLT metrics best predict ecological memory function. Analysis includes N=100 participants with complete RAVLT and REMEMVR data.

**Theoretical Framing:**
Clinical utility focus - if alternative RAVLT scoring methods predict ecological memory better than standard Total score, this provides evidence for revised clinical interpretation. Learning-based metrics may capture encoding efficiency while Total conflates learning speed with baseline performance.

---

## Theoretical Background

**Relevant Theories:**
- **Process-Specific Assessment Theory**: Different cognitive measures tap distinct memory processes. Learning slope may better isolate encoding efficiency compared to total recall which conflates multiple processes.
- **Ecological Validity Framework**: Traditional neuropsychological tests may not fully capture real-world memory function. Alternative scoring that better predicts ecological performance has greater clinical utility.

**Key Citations:**


**Theoretical Predictions:**
Learning-based metrics (Learning = T5-T1, Learning Slope = (T5-T1)/T1) should predict REMEMVR performance better than raw Total scores because they isolate encoding efficiency from baseline verbal recall ability. Recognition scores may add unique predictive value by isolating retrieval processes.

**Literature Gaps:**
Limited research comparing alternative RAVLT scoring methods for predicting ecological memory performance. Most clinical practice relies on Total score despite availability of process-specific metrics.

---

## Hypothesis

**Primary Hypothesis:**
Learning slope may better capture encoding efficiency, which should transfer to REMEMVR. Total conflates learning speed with baseline performance, making it a less pure measure of episodic memory function.

**Secondary Hypotheses:**
1. RAVLT Learning (T5-T1) will show incremental validity beyond Total score
2. Learning Slope ((T5-T1)/T1) will demonstrate unique predictive value
3. Recognition scores (Delayed Recognition) may add additional predictive power

**Theoretical Rationale:**
Learning-based metrics isolate encoding and consolidation processes that are central to episodic memory formation. Total score includes both these processes plus baseline verbal ability, creating measurement confounds. REMEMVR as an ecological measure should be better predicted by process-pure metrics.

**Expected Effect Pattern:**
Learning adds marginal unique variance beyond Total. Clinical recommendation: Report both Total and Learning for comprehensive assessment. Expected R² for Learning models between 0.15-0.26, with incremental models showing improvement.

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
Uses omnibus theta_all scores from Ch5 5.1.1 that aggregate across all episodic memory domains. This provides a comprehensive measure of episodic memory performance for comparison with RAVLT metrics.

**Exclusion Rationale:**
None - analysis requires overall episodic memory ability rather than domain-specific performance to match the omnibus nature of RAVLT Total scores.

---

## Analysis Approach

**Analysis Type:**
Multiple regression with hierarchical entry and cross-validation for alternative RAVLT scoring comparison

**High-Level Workflow:**

**Step 1:** Extract and prepare data
- Load mean theta_all scores from Ch5 5.1.1 results
- Extract RAVLT scores from master.xlsx (T1Sc, T2Sc, T3Sc, T4Sc, T5Sc, DRSc, FRSc)
- Compute alternative RAVLT metrics and standardize variables
- Check data quality and missingness patterns

**Step 2:** Compute alternative RAVLT scoring methods
- Learning = T5Sc - T1Sc (absolute learning gain)
- LearningSlope = (T5Sc - T1Sc) / T1Sc (proportional learning gain)
- Forgetting = T5Sc - DRSc (learning to delay decline)
- Recognition = FRSc (delayed recognition hits)

**Step 3:** Compare predictive validity models
- Model 1: `Theta_All ~ RAVLT_Total`
- Model 2: `Theta_All ~ RAVLT_Learning`
- Model 3: `Theta_All ~ RAVLT_LearningSlope`
- Model 4: `Theta_All ~ RAVLT_Recognition`
- Model 5: `Theta_All ~ RAVLT_Total + RAVLT_Learning` (incremental validity)

**Step 4:** Test incremental validity
- Extract standardized betas with 95% CIs
- Compute semi-partial correlations (sr²) for unique variance
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Primary: Bonferroni correction (± = 0.00179/5 = 0.000358 for 5 models)
- Secondary: FDR correction for comparison

**Step 5:** Effect sizes and model comparison
- Cohen's f² = R²/(1-R²) for each model
- AIC/BIC comparison for model selection
- Bootstrap CIs (1000 iterations) for effect size estimates
- Dominance analysis for predictor importance

**Step 6:** Model diagnostics
- Multicollinearity: VIF < 5 for all predictors
- Residual normality: Shapiro-Wilk test, Q-Q plot  
- Homoscedasticity: Breusch-Pagan test
- Influential points: Cook's D < 4/N threshold

**Step 7:** Cross-validation
- Method: 5-fold CV for all models
- Metrics: Test R², RMSE, MAE
- Check for overfitting (training vs test R² gap)

**Step 8:** Power analysis and sensitivity
- Post-hoc power for observed effect sizes
- Sensitivity analysis: smallest detectable effect at 80% power
- Alternative analyses: Exclude outliers and rerun models

**CRITICAL for Ch7 and multiple comparisons:**
- Report BOTH uncorrected AND Bonferroni-corrected p-values (Decision D068)
- Include model diagnostics step (VIF, residuals, homoscedasticity)
- Include cross-validation for predictive models
- Include power analysis for null findings
- Include effect sizes with 95% CIs (R², f², sr², ²)

**Expected Outputs:**
- data/step01_ravlt_scores.csv (extracted RAVLT metrics)
- data/step02_theta_means.csv (mean theta_all per participant)
- data/step03_alternative_metrics.csv (computed Learning, Slope, etc.)
- data/step04_analysis_input.csv (merged analysis dataset)
- data/step05_model_comparison.csv (R², AIC, BIC for all models)
- data/step06_regression_coefficients.csv (betas, CIs, dual p-values)
- data/step07_effect_sizes.csv (f², sr², dominance weights)
- data/step08_model_diagnostics.csv (VIF, residuals, Cook's D)
- data/step09_cross_validation.csv (k-fold CV results)
- data/step10_power_analysis.csv (post-hoc and sensitivity)
- results/ravlt_scoring_summary.md (clinical interpretation guidance)
- plots/model_comparison.png (R² comparison across models)
- plots/diagnostic_plots.png (residuals, Q-Q, homoscedasticity)

**Success Criteria:**
- At least one RAVLT model explains significant variance (p < 0.000358)
- R² range between 0.15-0.30 (meaningful but not redundant with REMEMVR)
- Incremental validity: Learning adds significant R² beyond Total
- Residual > 70% (substantial unique REMEMVR variance)
- VIF < 5 for all predictors (no multicollinearity)
- Residuals normally distributed (Shapiro-Wilk p > 0.05)
- Homoscedasticity confirmed (Breusch-Pagan p > 0.05)
- No influential outliers (Cook's D < 4/N)
- Cross-validation R² within 15% of training R²
- Power > 0.80 for medium effect (f² = 0.15)
- Clear clinical recommendations for optimal RAVLT interpretation

---

## Data Source

**Data Type:**
DERIVED (from Ch5 5.1.1 outputs + master.xlsx cognitive tests)

### DERIVED Data Sources:

**Source RQ:**
Ch5 5.1.1 (Functional Form Comparison - provides omnibus theta_all scores)

**File Paths:**
- results/ch5/5.1.1/data/step03_theta_scores.csv (IRT ability estimates)
- data/cache/master.xlsx (RAVLT test scores)

**Dependencies:**
Ch5 5.1.1 must complete Steps 1-3 (IRT calibration, purification, final theta estimation) before this RQ can run.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants with complete RAVLT and REMEMVR data
- [ ] Exclude: Participants with incomplete RAVLT trials (T1-T5, DR, FR)
- [ ] Exclude: Participants with theta scores outside ±4 range (IRT failure)

**Items:**
- [x] All omnibus factor items (aggregated across What/Where/When domains)
- [ ] Individual domain analysis not applicable for this RQ

**Tests:**
- [x] RAVLT complete battery (T1-T5, Delayed Recall, Delayed Recognition)
- [x] REMEMVR omnibus theta scores (aggregated across T1-T4 sessions)

**RAVLT Variables Required:**
- T1Sc through T5Sc: Trial scores for learning curve
- DRSc: Delayed recall score for forgetting metric
- FRSc: False recognition score for recognition analysis

---