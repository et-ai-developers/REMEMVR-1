# RQ 7.5.1: Self-Report Predictors of REMEMVR Performance

**Chapter:** 7
**Type:** Self-Report & Contextual
**Subtype:** Education Effects Analysis
**Full ID:** 7.5.1

---

## Research Question

**Primary Question:**
Do self-reported factors (typical sleep, education level, VR experience) predict REMEMVR performance?

**Scope:**
This RQ examines individual difference predictors using mean theta scores aggregated across all memory domains from Ch5. Analysis includes 100 participants with self-report measures from master.xlsx. Model includes age as covariate to control for developmental confounding.

**Theoretical Framing:**
Tests whether lifestyle and experiential factors contribute unique variance to episodic memory performance beyond chronological age. Key question for ecological validity of REMEMVR assessment.

---

## Theoretical Background

**Relevant Theories:**
- **Cognitive Reserve Theory**: Higher education provides neural resilience and compensatory mechanisms that protect against age-related memory decline
- **Sleep Consolidation Theory**: Adequate sleep supports memory consolidation processes, particularly hippocampal-dependent episodic memories
- **Novelty and Familiarity Effects**: Prior VR experience may reduce cognitive load from novel interface, improving task-relevant memory performance

**Key Citations:**
Stern, Y. (2002) - Cognitive reserve framework
Walker, M. P. (2008) - Sleep and memory consolidation
Diekelmann & Born (2010) - Sleep's role in memory processing

**Theoretical Predictions:**
- Education should positively predict performance through cognitive reserve mechanisms
- Sleep may predict consolidation-related processes but effect may be small in young healthy sample
- VR experience may reduce interface-related performance decrements

**Literature Gaps:**
Limited research on self-report lifestyle predictors of complex spatial-temporal episodic memory in virtual environments

---

## Hypothesis

**Primary Hypothesis:**
Education level will significantly predict REMEMVR performance, with higher education associated with better episodic memory scores.

**Secondary Hypotheses:**
- Typical sleep duration may show positive but weak association with performance
- VR experience may show positive association by reducing novelty effects
- Age will show negative association requiring statistical control

**Theoretical Rationale:**
Cognitive reserve theory predicts that higher education provides compensatory mechanisms for complex memory tasks. Sleep effects may be attenuated in healthy young adults with sufficient baseline sleep. VR familiarity reduces extraneous cognitive load.

**Expected Effect Pattern:**
Education: Beta = 0.20-0.25, p < 0.05; Sleep: Beta = 0.10-0.15, likely non-significant; VR_Experience: Beta = 0.05-0.15, likely non-significant; Age: Beta = -0.10 to -0.20 (control variable)

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
Uses omnibus theta_all scores from Ch5 5.1.1 that aggregate across all episodic memory domains. Self-report predictors tested against general memory ability rather than domain-specific performance.

**Exclusion Rationale:**
Domain-specific analysis not appropriate for this RQ focus on global individual differences in self-report lifestyle factors.

---

## Analysis Approach

**Analysis Type:**
Multiple regression with hierarchical entry and cross-validation

**High-Level Workflow:**

**Step 1:** Extract and prepare data
- Load mean theta_all scores from Ch5 5.1.1 results
- Extract self-report measures from master.xlsx (Education, Sleep, VR_Experience)
- Extract Age covariate for statistical control
- Check data quality and missingness patterns

**Step 2:** Hierarchical regression
- Model 1: Demographics only (Age)
- Model 2: + Self-report predictors (Education, Sleep, VR_Experience)
- Report ”R² and F-test for model improvement

**Step 3:** Test individual predictors
- Extract standardized beta coefficients with 95% CIs
- Compute semi-partial correlations (sr²) for unique variance
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Primary correction: Bonferroni (± = 0.00179/4 = 0.000448)
- Secondary: FDR correction for comparison

**Step 4:** Effect sizes and importance
- Cohen's f² = R²/(1-R²) for overall model
- Bootstrap CIs (1000 iterations) for robust estimates
- Relative importance analysis for predictor rankings

**Step 5:** Model diagnostics
- Multicollinearity: VIF < 5 for all predictors
- Residual normality: Shapiro-Wilk test, Q-Q plot
- Homoscedasticity: Breusch-Pagan test, residual vs fitted plot
- Influential points: Cook's D < 4/N threshold

**Step 6:** Cross-validation
- Method: 5-fold CV to assess generalizability
- Metrics: Test R², RMSE, MAE
- Check for overfitting if test R² << training R²

**Step 7:** Power analysis
- Post-hoc power for observed effect sizes
- Sensitivity analysis: smallest detectable effect at 80% power

**Step 8:** Sensitivity analyses
- Exclude potential outliers, rerun analysis
- Compare Bonferroni vs FDR correction results
- Bootstrap CIs for non-normal distributions if needed

**Expected Outputs:**
- data/step01_self_report_data.csv (extracted measures from master.xlsx)
- data/step02_theta_means.csv (mean theta per participant from Ch5)
- data/step03_analysis_input.csv (merged analysis dataset)
- data/step04_regression_results.csv (coefficients, CIs, dual p-values)
- data/step05_model_diagnostics.csv (VIF, residuals, Cook's D)
- data/step06_effect_sizes.csv (R², f², sr², with 95% CIs)
- data/step07_cross_validation.csv (5-fold CV results)
- data/step08_power_analysis.csv (post-hoc and sensitivity)
- results/self_report_regression_summary.md (text summary for thesis)
- plots/diagnostic_plots.png (residuals, Q-Q, homoscedasticity)
- plots/predictor_importance.png (beta coefficients with CIs)

**Success Criteria:**
- Model converges with finite parameter estimates
- Education shows significant association (primary hypothesis)
- R² between 0.10 and 0.40 (modest but meaningful prediction)
- VIF < 5 for all predictors (no multicollinearity)
- Residuals normally distributed (Shapiro-Wilk p > 0.05)
- Homoscedasticity confirmed (Breusch-Pagan p > 0.05)
- No influential outliers (Cook's D < 4/N)
- Cross-validation R² within 15% of training R²
- Power > 0.80 for medium effect (f² = 0.15) if effects detected

---

## Data Source

**Data Type:**
DERIVED (from Ch5 5.1.1 outputs + master.xlsx self-report measures)

### DERIVED Data Sources:

**Source RQ:**
Ch5 5.1.1 (Functional Form Comparison) for omnibus theta scores

**File Paths:**
- results/ch5/5.1.1/data/step03_theta_scores.csv (IRT ability estimates)
- data/cache/master.xlsx (self-report and demographic measures)

**Dependencies:**
Ch5 5.1.1 must complete IRT calibration and theta estimation before this RQ can run

**Data Extraction Details:**
- From Ch5: Mean theta_all per participant (N=100)
- From master.xlsx: Education, Typical_Sleep, VR_Experience, Age variables
- Merge on UID for complete case analysis

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants with complete theta scores from Ch5 5.1.1
- [ ] Exclude: Participants missing self-report measures (if any)

**Items:**
- N/A (uses aggregated theta scores across all domains)

**Tests:**
- N/A (theta scores already aggregated across T1-T4 timepoints)

**Variable Specifications:**
- DV: Mean theta_all per participant from Ch5 5.1.1
- IVs: Education (years), Typical_Sleep (hours), VR_Experience (ordinal scale)
- Covariate: Age (years) for statistical control
- Expected N: 100 (complete cases only)

---