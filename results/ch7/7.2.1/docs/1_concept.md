# RQ 7.2.1: Age Moderation of Test-VR Relationship

**Chapter:** 7
**Type:** Theme 2 (Age x VR Scaffolding)
**Subtype:** Age moderation after controlling for cognitive tests
**Full ID:** 7.2.1

---

## Research Question

**Primary Question:**
Does age explain variance in REMEMVR performance beyond what cognitive tests predict? If not, VR may compensate for age-related decline.

**Scope:**
This RQ examines age effects on overall episodic memory performance (theta_all) after controlling for cognitive tests (RAVLT, BVMT, RPM). N=100 participants. Tests hierarchical regression to determine whether age predicts REMEMVR beyond cognitive ability.

**Theoretical Framing:**
VR scaffolding hypothesis - contextual richness in VR compensates for age-related encoding deficits. If true, age effects should be fully mediated by cognitive ability (which VR bypasses through environmental support). Connects to Ch5's age-invariant VR forgetting finding (AgeTime p=.96).

---

## Theoretical Background

**Relevant Theories:**
- **VR Scaffolding Theory**: Contextual richness in virtual environments provides environmental support that compensates for age-related cognitive decline
- **Cognitive Reserve Theory**: Individual differences in cognitive ability buffer against age-related performance declines
- **Mediation Framework**: Age effects on memory performance may be fully explained by underlying cognitive abilities measured by standardized tests

**Key Citations:**
Theories predict full mediation if VR scaffolding is effective

**Theoretical Predictions:**
VR scaffolding should compensate for age-related encoding deficits, leading to full mediation of age effects by cognitive tests. Age should predict REMEMVR in bivariate analysis but become non-significant when controlling for cognitive tests.

**Literature Gaps:**
Limited research on VR's potential to compensate for age-related episodic memory decline through environmental scaffolding

---

## Hypothesis

**Primary Hypothesis:**
Age should NOT predict REMEMVR after controlling for cognitive tests, consistent with Ch5's age-invariant VR forgetting finding (AgeTime p=.96).

**Secondary Hypotheses:**
Complete or near-complete mediation expected - cognitive tests will fully explain age-related variance in REMEMVR performance.

**Theoretical Rationale:**
VR scaffolding hypothesis predicts that contextual richness compensates for age-related encoding deficits. If true, age effects should be fully mediated by cognitive ability since VR bypasses age-sensitive processes through environmental support.

**Expected Effect Pattern:**
- Bivariate: r(Age, Theta) = small negative correlation (r < -0.15)
- After control: Age beta becomes non-significant (p > 0.05)
- Substantial attenuation of age beta from Model 1 to Model 2

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
Uses omnibus theta_all scores from Ch5 5.1.1 that aggregate across all episodic memory domains to assess overall VR scaffolding effects

**Exclusion Rationale:**
None - all domains included in omnibus analysis

---

## Analysis Approach

**Analysis Type:**
Multiple regression with hierarchical entry and cross-validation

**High-Level Workflow:**

**Step 1:** Extract and prepare data
- Load theta_all scores from Ch5 5.1.1 results
- Extract cognitive tests from dfnonvr.csv (RAVLT_T, BVMT_T, RPM_T)
- Extract age as continuous variable
- Check data quality and missingness

**Step 2:** Bivariate correlations
- Compute r(Age, Theta) - expect small negative correlation
- Compute r(Age, RAVLT), r(Age, BVMT), r(Age, RPM) - expect negative from literature
- Create correlation matrix for all variables

**Step 3:** Hierarchical regression
- Model 1: `Theta ~ Age` (bivariate age effect)
- Model 2: `Theta ~ Age + RAVLT_T + BVMT_T + RPM_T` (controlled age effect)
- Test whether Age remains significant in Model 2
- Report R and F-test for model improvement

**Step 4:** Test individual predictors
- Extract standardized beta coefficients with 95% CIs
- Compute semi-partial correlations (sr) for unique variance
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Primary: Bonferroni ( = 0.00179/4 = 0.000448)
- Secondary: FDR for comparison

**Step 5:** Mediation analysis (conceptual)
- Path a: Age  Cognitive Tests (expect significant)
- Path b: Cognitive Tests  REMEMVR (from prior analyses)
- Path c': Age  REMEMVR controlling for tests (expect NULL)
- Compare beta_Age in Model 1 vs Model 2

**Step 6:** Effect sizes and importance
- Cohen's f = R/(1-R)
- Compare standardized betas between models
- Bootstrap CIs (1000 iterations)

**Step 7:** Model diagnostics
- Multicollinearity: VIF < 5
- Residual normality: Shapiro-Wilk test, Q-Q plot
- Homoscedasticity: Breusch-Pagan test
- Influential points: Cook's D < 4/N

**Step 8:** Cross-validation
- Method: 5-fold CV
- Metrics: Test R, RMSE, MAE
- Check for overfitting

**Step 9:** Power analysis
- Post-hoc power for observed effects
- Sensitivity: smallest detectable effect at 80% power

**Expected Outputs:**
- data/step01_cognitive_tests.csv (extracted test scores)
- data/step02_theta_means.csv (mean theta per participant)  
- data/step03_analysis_input.csv (merged analysis dataset)
- data/step04_bivariate_correlations.csv (correlation matrix)
- data/step05_hierarchical_models.csv (Model 1 and 2 results)
- data/step06_regression_results.csv (coefficients, CIs, dual p-values)
- data/step07_model_diagnostics.csv (VIF, residuals, Cook's D)
- data/step08_effect_sizes.csv (R, f, sr, with 95% CIs)
- data/step09_cross_validation.csv (k-fold CV results)
- data/step10_power_analysis.csv (post-hoc and sensitivity)
- results/age_mediation_summary.md (text summary for thesis)
- plots/diagnostic_plots.png (residuals, Q-Q, homoscedasticity)
- plots/age_mediation_visualization.png (visualization of mediation)

**Success Criteria:**
- Age significant (or trending) in bivariate (r < -0.15)
- Age NOT significant after controlling for tests (p > 0.05) 
- Beta_Age drops substantially from Model 1 to Model 2
- Model explains significant variance (p < 0.00179)
- VIF < 5 for all predictors (no multicollinearity)
- Residuals normally distributed (Shapiro-Wilk p > 0.05)
- Homoscedasticity confirmed (Breusch-Pagan p > 0.05)
- No influential outliers (Cook's D < 4/N)
- Cross-validation R within 10% of training R
- Power > 0.80 for medium effect (f = 0.15)

---

## Data Source

**Data Type:**
DERIVED (from Ch5 5.1.1 outputs + master.xlsx cognitive tests)

### DERIVED Data Sources:

**Source RQ:**
Ch5 5.1.1 (Functional Form Comparison - provides omnibus theta_all scores)

**File Paths:**
- results/ch5/5.1.1/data/step03_theta_scores.csv (IRT ability estimates)
- data/cache/master.xlsx (cognitive test scores and demographics)

**Dependencies:**
Ch5 5.1.1 must complete Steps 1-3 (IRT calibration and theta estimation) before this RQ can run

### Cognitive Test Variables (master.xlsx):
- RAVLT: RAVLT_T (total learning score)
- BVMT: BVMT_T (total recall score)  
- RPM: RPM_T (Raven's Progressive Matrices total score)
- Age: continuous variable in years

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions)
- [x] Complete cognitive test data required

**Items:**
- N/A (uses aggregated theta_all scores from Ch5 5.1.1)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4) - inherited from Ch5 5.1.1

---