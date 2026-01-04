# RQ 7.3.1: Do cognitive tests predict confidence trajectories?

**Chapter:** 7
**Type:** Metacognition Predictors  
**Subtype:** Confidence Prediction
**Full ID:** 7.3.1

---

## Research Question

**Primary Question:**
Do cognitive tests predict confidence ratings (IRT-scaled) as they predict accuracy? This tests whether metacognition shares predictors with memory.

**Scope:**
This RQ examines predictive relationships between cognitive tests (RAVLT-T, BVMT-T, RPM-T) and IRT-derived confidence theta scores from Chapter 6. Cross-sectional analysis using multiple regression with N=100 participants. Compares prediction pattern for confidence versus accuracy (from RQ 7.1.1).

**Theoretical Framing:**
Tests whether metacognitive monitoring (confidence) has similar or different cognitive predictors compared to memory performance. Critical for understanding if confidence is simply a reflection of memory ability or involves distinct cognitive processes.

---

## Theoretical Background

**Relevant Theories:**
- **Metacognitive Theory** (Nelson & Narens, 1990): Metacognitive monitoring may rely on executive processes (self-awareness, error detection) rather than memory encoding capacity
- **Dual-Process Theory**: Confidence judgments may recruit different cognitive systems than memory retrieval itself
- **Executive Function Theory**: Metacognitive accuracy may depend on reasoning and self-monitoring abilities rather than memory capacity

**Key Citations:**
Chapter 6 established confidence-accuracy dissociation (824 ICC ratio) suggesting partial independence of confidence from accuracy

**Theoretical Predictions:**
Tests designed for memory capacity (RAVLT, BVMT) may not predict metacognitive monitoring. Fluid intelligence tests (RPM) may show stronger prediction if confidence relies on executive/reasoning processes.

**Literature Gaps:**
Limited research on cognitive predictors of metacognitive monitoring in episodic memory contexts, particularly using IRT-scaled confidence measures.

---

## Hypothesis

**Primary Hypothesis:**
Cognitive tests may predict confidence weakly or not at all compared to accuracy prediction. Expected R for confidence < R for accuracy from RQ 7.1.1.

**Secondary Hypotheses:**
RPM (fluid intelligence) may predict confidence more strongly than RAVLT/BVMT if metacognitive monitoring relies on executive/reasoning processes rather than memory capacity.

**Theoretical Rationale:**
Chapter 6 established confidence-accuracy dissociation - if confidence is partially independent from accuracy, it should have different cognitive predictors. Metacognitive monitoring may recruit executive control rather than memory encoding systems.

**Expected Effect Pattern:**
Overall model R for confidence prediction < 0.35 (lower than accuracy prediction). RPM may show strongest individual prediction for confidence, while RAVLT/BVMT may be non-significant after correction.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Included in overall confidence theta scores from Ch6

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location)
  - [x] `-U-` tags (pick-up location) 
  - [x] `-D-` tags (put-down location)
  - Description: Included in overall confidence theta scores from Ch6

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Included in overall confidence theta scores from Ch6

**Inclusion Rationale:**
Uses omnibus confidence theta scores from Ch6 6.1.1 that aggregate across all episodic memory domains. Parallels accuracy analysis approach from RQ 7.1.1 for direct comparison.

**Exclusion Rationale:**
No domain-specific exclusions - uses comprehensive confidence scores to match accuracy prediction approach.

---

## Analysis Approach

**Analysis Type:**
Multiple regression with hierarchical entry and cross-validation

**High-Level Workflow:**

**Step 1:** Extract and prepare data
- Load confidence theta scores from Ch6 6.1.1 results  
- Extract cognitive tests from dfnonvr.csv
- Compute derived scores and standardize to T-scores
- Check data quality and missingness

**Step 2:** Hierarchical regression
- Model 1: Demographics only (Age, Sex, Education)
- Model 2: + Cognitive tests (RAVLT_T, BVMT_T, RPM_T)
- Report R and F-test for model improvement

**Step 3:** Test individual predictors  
- Extract standardized betas with 95% CIs
- Compute semi-partial correlations (sr) for unique variance
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Primary: Bonferroni ( = 0.00179/3 = 0.000597)
- Secondary: FDR for comparison

**Step 4:** Effect sizes and importance
- Cohen's f = R/(1-R)
- Dominance analysis or relative weights
- Bootstrap CIs (1000 iterations)

**Step 5:** Model diagnostics
- Multicollinearity: VIF < 5 for all predictors
- Residual normality: Shapiro-Wilk test, Q-Q plot
- Homoscedasticity: Breusch-Pagan test
- Influential points: Cook's D < 4/N threshold

**Step 6:** Cross-validation
- Method: 5-fold CV
- Metrics: Test R, RMSE, MAE  
- Check for overfitting if test R << training R

**Step 7:** Power analysis
- Post-hoc power for observed effect sizes
- Sensitivity: smallest detectable effect at 80% power

**Step 8:** Compare with accuracy prediction
- Load results from RQ 7.1.1
- Compare R values, predictor patterns
- Test which predictors differ between accuracy and confidence

**Expected Outputs:**
- data/step01_confidence_theta.csv (extracted confidence scores)
- data/step02_cognitive_tests.csv (extracted test scores) 
- data/step03_analysis_input.csv (merged analysis dataset)
- data/step04_hierarchical_regression.csv (model comparison results)
- data/step05_regression_results.csv (coefficients, CIs, dual p-values)
- data/step06_model_diagnostics.csv (VIF, residuals, Cook's D)
- data/step07_effect_sizes.csv (R, f, sr, with 95% CIs)
- data/step08_cross_validation.csv (k-fold CV results)
- data/step09_power_analysis.csv (post-hoc and sensitivity)
- data/step10_accuracy_comparison.csv (comparison with RQ 7.1.1)
- results/confidence_prediction_summary.md (text summary for thesis)
- plots/diagnostic_plots.png (residuals, Q-Q, homoscedasticity)
- plots/predictor_comparison.png (confidence vs accuracy predictors)

**Success Criteria:**
- R_confidence documented (may be < 0.25, lower than accuracy)
- Report which tests predict confidence vs accuracy differently  
- VIF < 5 for all predictors (no multicollinearity)
- Residuals normally distributed (Shapiro-Wilk p > 0.05)
- Homoscedasticity confirmed (Breusch-Pagan p > 0.05)  
- No influential outliers (Cook's D < 4/N)
- Cross-validation R within 15% of training R (allowing for smaller effects)
- Connects to Ch6 confidence-accuracy dissociation findings
- Power analysis documents detectability of medium effects

---

## Data Source

**Data Type:**
DERIVED (from Ch6 6.1.1 outputs + master.xlsx cognitive tests)

### DERIVED Data Sources:

**Source RQ:**
Ch6 6.1.1 (provides confidence theta scores)

**File Paths:**
- results/ch6/6.1.1/data/step03_confidence_theta_scores.csv
- data/cache/master.xlsx (cognitive test scores)

**Dependencies:**
Ch6 6.1.1 must complete before this RQ can run

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants from Ch6 6.1.1
- [ ] Exclude: None planned (inherit Ch6 inclusion criteria)

**Items:**
- N/A (confidence theta scores already aggregated across items)

**Tests:**
- [x] All 4 tests (confidence ratings aggregated across all test sessions)

**Cognitive Tests:**
- [x] RAVLT Total T-score (verbal episodic memory)
- [x] BVMT Total T-score (visuospatial episodic memory)  
- [x] RPM T-score (fluid intelligence/reasoning)
- [ ] NART excluded for this specific RQ (focus on 3 core tests)

---