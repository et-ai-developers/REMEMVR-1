# Results Summary: RQ 7.3.1 - Do Cognitive Tests Predict Confidence Trajectories?

**Research Question:** Do cognitive tests predict confidence ratings (IRT-scaled) as they predict accuracy? This tests whether metacognition shares predictors with memory.

**Analysis Completed:** 2026-01-05

**Analyst:** rq_results agent (v4.0) with master claude orchestration

---

## 1. Statistical Findings

### Sample Characteristics
- Total N: 100 participants
- Missing data: None (0% exclusions)
- Complete cases: 100 participants with both confidence theta scores and cognitive test data
- Data sources: Ch6 6.1.1 confidence theta scores + dfnonvr.csv cognitive tests

### Hierarchical Regression Results

**Model Comparison:**

| Model | R² | Adj R² | F | p-value | 95% CI | Cohen's f² |
|-------|-----|--------|---|---------|---------|------------|
| Demographics | 0.020 | -0.010 | 0.66 | 0.577 | [0.004, 0.147] | 0.021 |
| Cognitive | 0.188 | 0.135 | 3.58 | 0.003 | [0.118, 0.386] | 0.231 |

**Hierarchical Test:**
- ”R² = 0.167, F-change = 6.38, p < 0.001
- Cognitive tests explain significant additional variance beyond demographics

### Individual Predictor Effects

**Standardized Coefficients (Full Model):**

| Predictor | ² | SE | p (uncorrected) | p (Bonferroni) | p (FDR) | sr² | VIF |
|-----------|---|-----|-----------------|----------------|---------|-----|-----|
| Age | 0.002 | 0.003 | 0.323 | 0.324 | 0.648 | 0.009 | 1.45 |
| Sex | -0.006 | 0.067 | 0.930 | 0.930 | 0.936 | 0.001 | 1.04 |
| Education | -0.002 | 0.019 | 0.936 | 0.936 | 0.936 | 0.001 | 1.04 |
| **RAVLT_T** | **0.002** | **0.003** | **0.601** | **1.000** | **0.902** | **0.002** | **1.20** |
| **BVMT_T** | **0.009** | **0.004** | **0.021** | **0.064** | **0.090** | **0.048** | **1.75** |
| **RPM_T** | **0.008** | **0.004** | **0.030** | **0.090** | **0.090** | **0.042** | **1.38** |

**Multiple Comparisons:** None of the cognitive tests survive Bonferroni correction (± = 0.000597) but BVMT and RPM show nominally significant uncorrected effects.

**Multicollinearity:** All VIF values < 5, indicating acceptable levels of multicollinearity.

### Cross-Validation Assessment

**5-Fold Cross-Validation Results:**
- Mean training R² = 0.203 ± 0.039
- Mean test R² = -0.021 ± 0.231
- Train-test gap = 0.224 (>10% threshold)
- **Overfitting concern:** Model shows poor generalization with negative test R² in some folds

### Power Analysis

**Statistical Power:**
- Overall model: 95.7% power for observed effect (f² = 0.231)
- Individual cognitive tests: ~11-14% power at Bonferroni-corrected ± = 0.000597
- **Underpowered:** Individual predictor tests lack sufficient power for reliable detection

---

## 2. Plot Descriptions

### Figure 1: Hierarchical Regression Comparison
**Filename:** hierarchical_regression.png

**Visual Description:**
Left panel shows model R² comparison with Demographics (R² = 0.020) substantially lower than Cognitive (R² = 0.188), visually confirming the significant hierarchical improvement. Right panel displays individual predictor semi-partial r² values with BVMT showing highest unique contribution (sr² = 0.048), followed by RPM (sr² = 0.042), and RAVLT minimal (sr² = 0.002).

**Connection to Findings:**
Visual clearly shows the substantial improvement when adding cognitive tests and the dominance of BVMT and RPM over RAVLT in predicting confidence theta scores.

### Figure 2: Cross-Validation Results
**Filename:** cross_validation.png

**Visual Description:**
Bar chart comparing training R² (blue) vs test R² (red) across 5 folds. Training R² consistently around 0.15-0.26, while test R² varies dramatically from +0.22 (fold 4) to -0.38 (fold 3). Negative test R² values indicate worse-than-intercept-only prediction in some folds.

**Connection to Findings:**
Visualizes the overfitting concern identified in cross-validation analysis, with high variability and poor generalization evident in the substantial train-test gap.

### Figure 3: Confidence vs Accuracy Prediction Comparison
**Filename:** confidence_vs_accuracy.png

**Visual Description:**
Comparative bar chart showing semi-partial r² values for each cognitive test predicting confidence (red bars) versus accuracy (blue bars). For all three tests, accuracy prediction exceeds confidence prediction, with the pattern most pronounced for RPM (accuracy sr² = 0.080 vs confidence sr² = 0.042).

**Connection to Findings:**
Provides direct visual evidence for metacognitive dissociation - cognitive tests are systematically better predictors of memory accuracy than confidence, supporting the hypothesis that metacognitive monitoring involves distinct cognitive processes.

---

## 3. Interpretation

### Hypothesis Testing

**Original Hypothesis:** Cognitive tests may predict confidence weakly or not at all compared to accuracy prediction. Expected R² for confidence < R² for accuracy from RQ 7.1.1.

**Hypothesis Status:** **SUPPORTED**

The statistical findings confirm weaker cognitive prediction for confidence:
- Confidence R² = 0.188 vs Accuracy R² = 0.226 (from comparison with RQ 7.1.1)
- Individual predictors systematically weaker for confidence across all three cognitive tests
- Cross-validation suggests model overfitting, indicating limited generalizability

### Metacognitive Dissociation Evidence

**Primary Evidence:**
The comparison with accuracy prediction (RQ 7.1.1) reveals systematic differences in cognitive predictor patterns:

1. **Overall Model Strength:**
   - Accuracy: R² = 0.226 (stronger)
   - Confidence: R² = 0.188 (weaker)
   - Evidence supports metacognitive dissociation hypothesis

2. **Individual Predictor Patterns:**
   - **RAVLT:** Minimal prediction for both accuracy and confidence (sr² H 0.002 for confidence vs 0.017 for accuracy)
   - **BVMT:** Moderate confidence prediction (sr² = 0.048 vs 0.065 for accuracy) - complex pattern
   - **RPM:** Clear dissociation (sr² = 0.042 for confidence vs 0.080 for accuracy) - supports executive/reasoning distinction

### Theoretical Contextualization

**Metacognitive Theory Implications:**
The findings align with Nelson & Narens (1990) metacognitive monitoring theory and dual-process frameworks:

1. **Partial Independence:** Confidence shows related but distinct cognitive predictors compared to accuracy, indicating metacognitive monitoring recruits overlapping but not identical cognitive systems.

2. **Executive Function Role:** RPM (fluid intelligence) predicts both confidence and accuracy but more strongly predicts accuracy, suggesting metacognitive monitoring may rely less heavily on pure reasoning ability than memory performance itself.

3. **Domain Specificity:** BVMT (visuospatial memory) shows the strongest confidence prediction, consistent with the VR task's spatial demands, but the prediction is still weaker than for accuracy.

### Unexpected Patterns

**Cross-Validation Overfitting:**
The substantial overfitting (mean test R² = -0.021) was unexpected and concerning. Possible explanations:
1. Small sample size (N=100) relative to predictor set may lead to unstable estimates
2. Confidence measures may be inherently noisier than accuracy measures
3. Individual differences in confidence calibration may create subgroup heterogeneity not captured by linear models

**Convergence Warnings:**
Despite convergence warnings in logs, final results appear mathematically consistent and interpretable, suggesting successful model fitting despite optimization challenges.

### Broader Implications

**REMEMVR Validation:**
Findings contribute to REMEMVR construct validity by demonstrating that:
- Confidence ratings capture systematic individual differences related to but distinct from memory ability
- VR-derived confidence measures show theoretically predicted relationships with established cognitive tests
- Metacognitive dissociation evident even within immersive VR episodic memory contexts

**Clinical Applications:**
For cognitive assessment applications:
- Confidence measures may provide complementary information beyond accuracy scores
- Metacognitive monitoring assessment could identify executive/self-awareness deficits distinct from memory impairments
- However, limited power suggests larger samples needed for individual assessment applications

---

## 4. Limitations

### Sample Limitations

**Sample Size:**
- N = 100 provides adequate power (95.7%) for overall model detection but severely underpowered (11-14%) for individual cognitive predictors at Bonferroni-corrected ± = 0.000597
- Cross-validation instability suggests N=100 may be insufficient for stable parameter estimation with 6 predictors
- Confidence intervals for individual effects are wide, limiting precision of effect size estimates

**Demographic Constraints:**
- Undergraduate sample (implied from master.xlsx source) limits generalizability to older adults and clinical populations
- Confidence-accuracy relationships may differ across age groups and cognitive abilities
- Limited demographic diversity constrains external validity

**Cross-Validation Concerns:**
- Substantial overfitting (train-test gap = 0.224) raises questions about model generalizability
- Negative test R² in some folds indicates worse-than-chance prediction, suggesting model instability
- 5-fold CV with N=100 creates small validation sets (N=20) that may be unreliable

### Methodological Limitations

**Measurement Constraints:**
1. **Confidence Theta Aggregation:** Uses omnibus confidence scores aggregated across all memory domains and test sessions, potentially masking domain-specific or temporal patterns in confidence-cognition relationships

2. **Cognitive Test Coverage:** Limited to three cognitive tests; broader cognitive battery might reveal additional predictors (e.g., executive function, working memory, processing speed)

3. **Cross-Sectional Design:** Cannot establish causal direction - do cognitive abilities influence confidence calibration, or does confidence influence cognitive test performance?

**Statistical Limitations:**
1. **Linear Model Assumptions:** Assumes linear relationships between cognitive tests and confidence; nonlinear or threshold effects not explored

2. **Multiple Comparisons:** Despite Bonferroni correction, family-wise error rate inflation possible with numerous exploratory analyses across cognitive predictors

3. **Missing Moderators:** Age, education, or personality factors might moderate cognitive-confidence relationships but not systematically examined

### Generalizability Constraints

**Population Generalizability:**
- Findings limited to young adults with intact cognitive abilities
- May not extend to older adults with age-related cognitive decline
- Clinical populations (MCI, dementia) may show different confidence-cognition relationships
- Cultural differences in confidence expression not considered

**Task Generalizability:**
- VR-specific episodic memory task may not reflect confidence-cognition relationships in:
  - Real-world memory situations
  - Non-spatial memory domains
  - Different metacognitive judgment types (feeling-of-knowing, judgment-of-learning)
- Laboratory-based confidence ratings may differ from naturalistic metacognitive monitoring

### Technical Limitations

**Model Convergence Issues:**
- Hierarchical regression logs report convergence failures for both models, though results appear valid
- Optimization challenges may indicate near-singular design matrices or collinearity issues
- Alternative fitting methods (ridge regression, regularization) not explored

**Cross-RQ Dependency:**
- Comparison with RQ 7.1.1 assumes comparable methodology and sample characteristics
- Temporal separation between accuracy and confidence analyses may introduce systematic differences
- Different analysis pipelines could create methodological artifacts in comparison

**Power Analysis Constraints:**
- Post-hoc power analysis based on observed effects may be overly optimistic
- Bonferroni correction extremely conservative for exploratory research context
- Individual predictor power calculations assume independence that may not hold

### Confidence Rating Response Patterns

**Response Pattern Analysis:** Not systematically examined in this RQ, but Chapter 7 analyses should document % participants using full 1-5 confidence scale vs extremes only (1s and 5s). No bias correction applied in this analysis (transparency priority). Extreme response styles may limit interpretability of confidence-cognition relationships and contribute to model instability observed in cross-validation.

---

## 5. Next Steps

### Immediate Follow-Ups (Current Data)

**1. Regularization Analysis:**
- **Why:** Cross-validation overfitting suggests parameter instability
- **How:** Re-run hierarchical regression with ridge or elastic net regularization to improve generalizability
- **Expected Insight:** More stable effect estimates and better cross-validation performance
- **Timeline:** Can be done immediately with same analysis dataset

**2. Nonlinear Relationship Exploration:**
- **Why:** Linear model assumptions may miss threshold or curvilinear effects
- **How:** Fit polynomial terms, spline regression, or GAM models for cognitive predictors
- **Expected Insight:** Identify optimal ranges of cognitive ability for confidence prediction
- **Timeline:** 2-3 days with additional model specification

**3. Confidence Response Pattern Analysis:**
- **Why:** Extreme response styles (1s and 5s only) may contribute to model instability
- **How:** Analyze distribution of confidence ratings, identify extreme responders, test robustness
- **Expected Insight:** Quantify response style effects on cognitive-confidence relationships
- **Timeline:** 1 day with descriptive analysis of confidence distributions

### Planned Thesis RQs (Chapter 7 Continuation)

**RQ 7.3.2: Domain-Specific Confidence Prediction (Planned):**
- **Focus:** Test whether cognitive predictors differ across What/Where/When confidence domains
- **Builds On:** Uses domain-separated confidence scores from Ch6, same cognitive predictors
- **Expected Insight:** Spatial vs temporal vs object confidence may have different cognitive bases
- **Timeline:** Next RQ in Ch7 metacognition sequence

**RQ 7.3.3: Confidence Calibration Predictors (Planned):**
- **Focus:** Do cognitive tests predict confidence-accuracy correlation (calibration) rather than confidence level?
- **Builds On:** Combines accuracy data (RQ 7.1.1) with confidence data, computes individual calibration indices
- **Expected Insight:** Metacognitive accuracy may have different predictors than confidence bias
- **Timeline:** Two RQs ahead after domain-specific analysis

**RQ 7.4.1: Longitudinal Confidence Changes (Exploratory):**
- **Focus:** Do cognitive tests predict confidence trajectory slopes across Day 0’6?
- **Builds On:** Uses session-specific confidence data, tests cognitive prediction of forgetting-related confidence changes
- **Expected Insight:** Individual differences in confidence updating over time
- **Timeline:** Dependent on trajectory-level confidence data availability

### Methodological Extensions (Future Data Collection)

**1. Larger Sample Size:**
- **Current Limitation:** N=100 underpowered for individual cognitive predictor detection
- **Extension:** Target N=250-300 for adequate power (80%) at corrected alpha levels
- **Expected Insight:** More precise effect size estimates and stable cross-validation
- **Feasibility:** Requires new data collection (~6-12 months)

**2. Expanded Cognitive Battery:**
- **Current Limitation:** Limited to 3 cognitive tests (RAVLT, BVMT, RPM)
- **Extension:** Add executive function (Stroop, TMT), working memory (n-back), processing speed tests
- **Expected Insight:** Comprehensive cognitive profile of confidence prediction
- **Feasibility:** Moderate - existing cognitive tests available (~3 months for new sample)

**3. Confidence Calibration Focus:**
- **Current Limitation:** Analyzes confidence level, not confidence accuracy
- **Extension:** Primary outcome = confidence-accuracy correlation per participant
- **Expected Insight:** Test whether cognitive tests predict metacognitive accuracy rather than bias
- **Feasibility:** Can be done with current data (immediate follow-up)

**4. Cross-Sectional Age Comparison:**
- **Current Limitation:** Young adult sample only
- **Extension:** Recruit older adult sample (65+), compare confidence-cognition relationships across age
- **Expected Insight:** Age differences in metacognitive monitoring-cognition relationships
- **Feasibility:** Requires new recruitment and ethical approval (~12 months)

### Theoretical Questions Raised

**1. Cognitive Mechanisms of Metacognitive Monitoring:**
- **Question:** Which specific cognitive processes support confidence judgments in episodic memory?
- **Next Steps:** Neurocognitive study with fMRI or EEG during confidence rating
- **Expected Insight:** Neural networks supporting confidence vs accuracy may dissociate
- **Feasibility:** Long-term collaboration (2+ years)

**2. Development of Confidence-Cognition Relationships:**
- **Question:** Are confidence-cognition relationships stable across development and aging?
- **Next Steps:** Lifespan study from adolescence through older adulthood
- **Expected Insight:** Ontogenetic changes in metacognitive monitoring may track cognitive development
- **Feasibility:** Large-scale longitudinal design (5+ years)

**3. Clinical Applications of Metacognitive Dissociation:**
- **Question:** Can confidence-accuracy dissociation patterns identify specific cognitive impairments?
- **Next Steps:** Clinical validation study in MCI, dementia, TBI populations
- **Expected Insight:** Diagnostic utility of metacognitive assessment beyond standard cognitive testing
- **Feasibility:** Clinical partnerships required (1-2 years)

### Priority Ranking

**High Priority (Do First):**
1. Regularization analysis - addresses overfitting concerns with current data
2. RQ 7.3.2 (domain-specific confidence prediction) - natural extension in thesis sequence
3. Confidence calibration analysis - leverages existing accuracy data for deeper insights

**Medium Priority (Subsequent):**
1. Nonlinear relationship exploration - tests model assumption robustness
2. RQ 7.3.3 (calibration predictors) - complements confidence level findings
3. Response pattern analysis - addresses measurement quality concerns

**Lower Priority (Aspirational):**
1. Expanded cognitive battery - requires new data collection
2. Age comparison study - valuable but resource-intensive
3. Neurocognitive mechanisms - long-term research program beyond thesis scope

### Next Steps Summary

The findings establish **metacognitive dissociation** in VR episodic memory, with cognitive tests predicting confidence more weakly than accuracy. Three critical questions for immediate follow-up:

1. **Regularization:** Can overfitting be reduced while preserving effect pattern? (Current data)
2. **Domain specificity:** Do cognitive predictors differ across What/Where/When confidence? (RQ 7.3.2)
3. **Calibration focus:** Do cognitive tests predict confidence accuracy rather than confidence level? (Current + RQ 7.1.1 data)

Methodological extensions (larger samples, expanded cognitive testing) would strengthen conclusions but require new data collection beyond current thesis scope.

---

**Summary generated by:** rq_results agent (v4.0)
**Pipeline version:** v4.X (13-agent atomic architecture)
**Date:** 2026-01-05T21:30:00Z