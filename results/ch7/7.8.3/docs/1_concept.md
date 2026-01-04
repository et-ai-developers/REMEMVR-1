# RQ 7.8.3: Parsimonious Predictive Model with Cross-Validation

**Chapter:** 7
**Type:** 8 (Integration)
**Subtype:** Parsimonious Prediction
**Full ID:** 7.8.3

---

## Research Question

**Primary Question:**
What is the most parsimonious model to predict REMEMVR episodic memory performance, and how well does it generalize to unseen data?

**Scope:**
This RQ compares 4 nested regression models with varying complexity: (1) Minimal: Age + RAVLT, (2) Core: Age + RAVLT + BVMT, (3) Extended: + RPM + Education, (4) Full: all predictors. Uses 5-fold cross-validation to assess generalization. N=100 participants, comparing training R vs cross-validation R to quantify overfitting.

**Theoretical Framing:**
Model parsimony balances predictive power with generalizability. Overfitting occurs when complex models perform well on training data but poorly on new data. This RQ identifies the optimal complexity for REMEMVR prediction while ensuring practical utility for future applications.

---

## Theoretical Background

**Relevant Theories:**
- **Bias-Variance Tradeoff:** Increasing model complexity reduces bias but increases variance, potentially harming generalization
- **Episodic Memory Convergent Validity:** REMEMVR should correlate moderately (not perfectly) with established episodic tests
- **Cognitive Reserve Theory:** Core predictors (age, episodic tests) should account for substantial REMEMVR variance

**Key Citations:**

**Theoretical Predictions:**
Age and episodic memory tests should form the core predictive model, with diminishing returns from additional predictors

**Literature Gaps:**
Limited research on optimal predictor sets for VR-based episodic memory assessment

---

## Hypothesis

**Primary Hypothesis:**
Age + RAVLT + BVMT should achieve cross-validation R H 0.30-0.35 with minimal overfitting (shrinkage < 0.10). Adding more predictors may not improve cross-validated R.

**Secondary Hypotheses:**
- Minimal model (Age + RAVLT) should achieve CV-R H 0.20-0.25
- Full model should show substantial overfitting (shrinkage > 0.15)
- Core 3-predictor model should be optimal balance

**Theoretical Rationale:**
Age and established episodic tests capture core variance in REMEMVR. Additional predictors likely contribute noise rather than signal, degrading generalization.

**Expected Effect Pattern:**
Best cross-validation R with fewest predictors. Acceptable shrinkage (< 0.10) from training to CV performance. Core model should outperform minimal and full models in CV-R.

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
Uses omnibus theta_all scores from Ch5 5.1.1 that aggregate across all episodic memory domains for maximum generalizability

**Exclusion Rationale:**
Not examining domain-specific predictions to focus on overall REMEMVR performance

---

## Analysis Approach

**Analysis Type:**
Nested multiple regression with 5-fold cross-validation and model comparison

**High-Level Workflow:**

**Step 1:** Extract and prepare data
- Load theta_all scores from Ch5 5.1.1 results
- Extract cognitive tests from dfnonvr.csv
- Compute derived scores and standardize to T-scores
- Check data quality and missingness

**Step 2:** Fit nested regression models
- Model 1 (Minimal): Age + RAVLT_Total
- Model 2 (Core): Age + RAVLT_Total + BVMT_Total
- Model 3 (Extended): + RPM_Score + Education
- Model 4 (Full): + NART_Score + DASS_Total + Sleep + Sex

**Step 3:** Cross-validation
- 5-fold stratified CV (maintain age distribution)
- Compute training R and CV-R for each model
- Calculate shrinkage = Training R - CV-R
- Report mean  SE across folds

**Step 4:** Model selection
- Identify model with best CV-R given complexity
- Apply parsimony criterion: prefer simpler if CV-R within 0.02
- Test significance of R improvements between nested models

**Step 5:** Effect sizes and diagnostics
- Standardized betas with 95% CIs for optimal model
- Semi-partial correlations (sr) for unique variance
- VIF < 5 for multicollinearity check
- Report BOTH uncorrected AND corrected p-values (Decision D068)

**Step 6:** Sensitivity analyses
- Bootstrap CIs (1000 iterations) for CV-R estimates
- Leave-one-out CV for comparison with 5-fold
- Exclude outliers and rerun analysis

**Expected Outputs:**
- data/step01_cognitive_tests.csv (extracted test scores)
- data/step02_theta_all_scores.csv (mean theta per participant)
- data/step03_analysis_input.csv (merged analysis dataset)
- data/step04_nested_models.csv (4 model specifications)
- data/step05_cv_results.csv (training vs CV R by model)
- data/step06_optimal_model.csv (coefficients, CIs, dual p-values)
- data/step07_model_diagnostics.csv (VIF, residuals, Cook's D)
- data/step08_sensitivity_analysis.csv (bootstrap CIs, LOO-CV)
- results/parsimony_analysis.md (text summary for thesis)
- plots/cv_performance.png (training vs CV R by model)
- plots/shrinkage_comparison.png (overfitting visualization)

**Success Criteria:**
- [ ] Fit 4 nested models successfully
- [ ] Complete 5-fold CV for all models
- [ ] Core model achieves CV-R > 0.25
- [ ] Core model shrinkage < 0.10
- [ ] Full model shows greater shrinkage than core
- [ ] VIF < 5 for all predictors in optimal model
- [ ] Residuals normally distributed (Shapiro-Wilk p > 0.05)
- [ ] No influential outliers (Cook's D < 4/N)
- [ ] Bootstrap CIs stable across iterations

---

## Data Source

**Data Type:**
DERIVED (from Ch5 5.1.1 outputs + master.xlsx cognitive tests)

### DERIVED Data Sources:

**Source RQ:**
Ch5 5.1.1 (Functional Form Comparison - provides theta_all scores)

**File Paths:**
- results/ch5/5.1.1/data/step03_theta_scores.csv
- data/cache/master.xlsx (cognitive test scores, demographics, DASS)

**Dependencies:**
Ch5 5.1.1 must complete Steps 1-3 (IRT calibration) before this RQ can run

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants with complete cognitive test data
- [ ] Exclude: Participants with missing RAVLT or BVMT scores (if any)

**Variables:**
- [x] DV: theta_all (mean across all 4 tests)
- [x] Core IVs: Age, RAVLT_Total, BVMT_Total
- [x] Extended IVs: RPM_Score, Education
- [x] Additional IVs: NART_Score, DASS_Total, Sleep, Sex

**Tests:**
- [x] All 4 tests aggregated into theta_all mean score

---