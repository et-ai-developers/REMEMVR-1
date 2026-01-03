# RQ 7.1.1: Do cognitive tests predict overall REMEMVR ability?

**Chapter:** 7
**Type:** Predictive Validity (Core)
**Subtype:** Do cognitive tests predict overall REMEMVR ability?
**Full ID:** 7.1.1

---

## Research Question

**Primary Question:**
Do established neuropsychological tests (RAVLT, BVMT, NART, RPM) predict overall episodic memory ability as measured by REMEMVR theta scores?

**Scope:**
This RQ examines the predictive relationship between four standardized cognitive tests and mean episodic memory ability (theta scores) across 100 participants. Cognitive tests are converted to T-scores (M=50, SD=10). Analysis uses mean theta scores across four test sessions per participant. Statistical threshold adjusted for Chapter 7 multiple comparisons (alpha = 0.00179).

**Theoretical Framing:**
Core convergent validity question for REMEMVR. If traditional tests validly measure episodic memory, they should predict ecological performance. However, ecological validity gap predicts imperfect prediction due to contextual differences between laboratory and VR environments.

---

## Theoretical Background

**Relevant Theories:**
- **Predictive Validity Theory** (Cronbach & Meehl, 1955): Valid measures of the same construct should correlate meaningfully. Neuropsychological tests and REMEMVR both claim to measure episodic memory, so moderate correlation expected.
- **Ecological Validity Gap** (Chaytor & Schmitter-Edgecombe, 2003): Laboratory tests may fail to capture real-world cognitive demands due to simplified, artificial contexts. VR provides more ecologically valid assessment.

**Key Citations:**
To be added by rq_scholar

**Theoretical Predictions:**
Predictive validity theory expects moderate correlations (r = 0.5-0.7) if tests measure the same construct. Ecological validity gap theory predicts lower correlations due to contextual differences. Recent meta-analyses (2024) show VR-traditional test correlations typically range r=0.4-0.6 (R²=0.16-0.36), suggesting our predicted R²=0.35 represents an upper bound of realistic expectations. RAVLT and BVMT (episodic memory tests) should predict better than NART and RPM (intelligence tests).

**Practice Effects Consideration:**
Cognitive tests administered once (Session 1) avoid practice effects that could confound convergent validity estimates. Recent literature shows significant practice effects in RAVLT and BVMT-R with repeated administration, making single-session design methodologically advantageous for clean validity assessment.

**Literature Gaps:**
Limited research on VR-based episodic memory assessment validity. Gap in understanding how traditional neuropsychological batteries relate to immersive, contextually rich memory tasks.

---

## Hypothesis

**Primary Hypothesis:**
Cognitive tests should predict REMEMVR with moderate effect (R² = 0.30-0.45), demonstrating convergent validity. RAVLT and BVMT (episodic memory tests) should show stronger prediction than NART and RPM (intelligence tests).

**Secondary Hypotheses:**
1. RAVLT_beta > RPM_beta (episodic memory tests predict better than fluid intelligence)
2. Substantial residual variance (>50%) indicating unique REMEMVR variance not captured by traditional tests
3. NART may show weaker prediction due to language validity concerns

**Theoretical Rationale:**
If tests measure the same underlying episodic memory construct, moderate prediction expected. However, VR context provides richer encoding cues, spatial navigation demands, and ecological validity that traditional tests lack, predicting substantial unexplained variance.

**Expected Effect Pattern:**
Overall model: R² = 0.25-0.45 (acknowledging ecological validity gap uncertainty), F(4,95) = 7.9-21.4, p < 0.001. Individual predictors: RAVLT_beta = 0.25-0.40 (strongest), BVMT_beta = 0.20-0.30, RPM_beta = 0.10-0.25, NART_beta = 0.05-0.20 (weakest, noting ceiling effects). At least one episodic test significant after Bonferroni correction (alpha = 0.0125 within-RQ, 0.00179 chapter-level).

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: All object identity items included in omnibus theta

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location, legacy)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Disambiguation: All spatial location items included in omnibus theta

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: All temporal order items included in omnibus theta

**Inclusion Rationale:**
Uses omnibus "All" factor from Ch5 RQ 5.1.1, which combines all WWW domains and all paradigms (Free/Cued/Recognition) into single episodic memory ability estimate. This provides most general measure of REMEMVR performance for convergent validity testing.

**Exclusion Rationale (if applicable):**
No domain-specific exclusions. Analysis deliberately uses comprehensive episodic memory measure to test overall convergent validity with traditional neuropsychological batteries.

---

## Analysis Approach

**Power Analysis:**
- Sample size: N=100 with k predictors
- Post-hoc power for medium effects (f²=0.15): Approximately 80%
- Minimum detectable effect: f²=0.10 with current sample
- Limitation acknowledged: Underpowered for small effects (f²<0.10)


**Analysis Type:**
Multiple Linear Regression with standardized predictors (T-scores)

**High-Level Workflow:**

**Step 1:** Extract and prepare cognitive test data from master.xlsx using established tag patterns
**Step 2:** Compute derived scores (RAVLT_Total = sum T1-T5) and standardize all tests to T-scores (M=50, SD=10)
**Step 3:** Load mean theta scores from Ch5 5.1.1 (average across 4 test sessions per participant)
**Step 4:** Check regression assumptions with remedial actions:
- Normality (Shapiro-Wilk p > 0.05, Q-Q plots)
- Homoscedasticity (Breusch-Pagan p > 0.05, residual plots)
- Linearity (partial regression plots for each predictor, RESET test if needed)
- Multicollinearity (VIF < 5, acknowledging context-dependent thresholds per Kalnins & Hill 2025)
- Outliers (Cook's D < 4/n, leverage values, DFBETAs)
- Independence (participant-level data ensures no repeated measures)

Remedial actions if violated:
- Normality: Report robust standard errors (HC3) and bootstrap 95% CIs (1000 replications), note as limitation
- Homoscedasticity: Use White's heteroscedasticity-consistent standard errors (HC3)
- Linearity: If systematic patterns detected, consider polynomial terms or transformations
- Multicollinearity: If VIF > 5, report predictor correlations, consider ridge regression (alpha=0.1) or PCA
- Outliers: If Cook's D > 4/n, report results with and without influential points
- Multiple solutions: If multiple violations, prioritize bootstrap inference (robust to multiple assumption violations)
**Step 5:** Fit multiple regression model: Theta_Mean ~ RAVLT_T + BVMT_T + NART_T + RPM_T
Note: Implementation requires tools.analysis_regression module with:
- Multiple linear regression (statsmodels.OLS or sklearn.LinearRegression)
- Assumption checking functions (Shapiro-Wilk, Breusch-Pagan, VIF calculation)
- Effect size computation (R², adjusted R², semi-partial correlations)
**Step 6:** Test individual predictors with Bonferroni correction
- Within-RQ family: 4 predictors, alpha = 0.05/4 = 0.0125 per predictor
- Report BOTH uncorrected AND Bonferroni-corrected p-values (Decision D068)
- Include 95% CIs for all beta coefficients using bootstrap (1000 replications)
**Step 7:** Compute predictor importance via standardized betas and semi-partial correlations (sr²)
- Dominance analysis or relative importance weights to rank predictors
- Test hypothesis: RAVLT_beta > RPM_beta (episodic > fluid intelligence)
- Report unique variance explained by each predictor (sr²)
**Step 8:** Sensitivity analysis and cross-validation:
- Repeat excluding NART due to language validity concerns AND known ceiling effects that restrict range
- Compare R² with and without NART (expect minimal change if NART contribution weak)
- Implement 5-fold cross-validation (seed=42) to assess model stability and overfitting risk
- Report train-test generalization gap (should be < 0.10)
- Report both R² and adjusted R² to account for small sample (N=100) relative to predictors (k=4)
- Consider Holm-Bonferroni as less conservative alternative to standard Bonferroni (preserves FWER with correlated tests)

**CRITICAL for Ch7 and multiple comparisons:**
- Report BOTH uncorrected AND Bonferroni-corrected p-values (Decision D068)
- Include model diagnostics step (VIF, residuals, homoscedasticity)
- Include effect sizes with 95% CIs (R², sr², ²)
- Multiple comparison adjustment: Chapter-level alpha = 0.05/28 RQs = 0.00179

**Expected Outputs:**
- data/step01_cognitive_tests.csv (extracted test scores with T-score conversions)
- data/step02_theta_mean.csv (mean theta per participant from Ch5 5.1.1)
- data/step03_merged_analysis.csv (cognitive tests merged with theta scores)
- data/step04_regression_diagnostics.csv (assumption checks, VIF values)
- data/step05_regression_results.csv (model summary, coefficients, p-values)
- data/step06_predictor_importance.csv (standardized betas, sr² values)
- data/step07_sensitivity_analysis.csv (model without NART)
- results/regression_summary.md (formatted results for thesis)

**Success Criteria:**
- Model explains significant variance (p < 0.00179)
- R² between 0.25 and 0.50 (convergent but not redundant)
- At least one episodic test (RAVLT or BVMT) significant after Bonferroni correction
- Residual > 50% (substantial unique REMEMVR variance)
- All VIF values < 5.0
- Model diagnostics pass (normality, homoscedasticity)

---



**Note on Tool Availability:**
All required analysis tools are fully implemented in tools.analysis_regression module with 100% test coverage (8/8 functions, 29+ tests passing). The tools include hierarchical regression, cross-validation, assumption checking, and bootstrap confidence intervals.

## Data Source

**Data Type:**
DERIVED (from Ch5 5.1.1 outputs + master.xlsx)

### DERIVED Data Source:

**Source RQ:**
Ch5 5.1.1 (Functional Form Comparison) for REMEMVR theta scores

**File Paths:**
- results/ch5/5.1.1/data/step03_theta_scores.csv (IRT theta estimates across 4 test sessions)
- master.xlsx (cognitive test raw scores)

**Dependencies:**
Ch5 5.1.1 must complete Steps 1-3 (IRT calibration with omnibus "All" factor) before this RQ can run. Cognitive test data extracted independently from master.xlsx using established tag patterns.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants from Ch5 5.1.1 (inherited inclusion criteria)
- [ ] Exclude: Participants with missing cognitive test data (report final n)

**Items:**
- [x] All items from omnibus "All" factor (theta scores already aggregated)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4) - mean theta computed across sessions per participant

**Cognitive Tests:**
- [x] RAVLT_Total (sum of T1-T5 trials)
- [x] BVMT_TotR (Brief Visuospatial Memory Test - Revised total recall)
- [x] NART (National Adult Reading Test - with language validity caveat)
- [x] RPM (Raven's Progressive Matrices)

---