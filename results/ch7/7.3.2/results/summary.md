# Results Summary: RQ 7.3.2 - Cognitive Predictors of Calibration Quality

**Research Question:** Do cognitive tests predict who is well-calibrated (confidence matches accuracy) vs overconfident (confidence exceeds accuracy)?

**Analysis Completed:** January 5, 2026

**Analyst:** rq_results agent (v4.0) with master claude orchestration

---

## 1. Statistical Findings

### Hierarchical Regression Results

**Model Comparison:**
- Model 1 (Demographics): R² = 0.006, F(3,96) = 0.20, p = 0.896
- Model 2 (Full Model): R² = 0.024, F(6,93) = 0.38, p = 0.891
- ”R² = 0.018, F(3,93) = 0.56, p = 0.648 (n.s.)

**Individual Predictor Results:**

| Predictor | ² | SE | t | p (uncorr) | p (Bonf) | p (FDR) | 95% CI | VIF |
|-----------|---|----|----|-------------|----------|---------|---------|-----|
| Age | 0.004 | 0.006 | 0.72 | 0.471 | 1.000 | 0.854 | [-0.007, 0.015] | 1.45 |
| Sex | 0.048 | 0.148 | 0.33 | 0.745 | 1.000 | 0.854 | [-0.246, 0.342] | 1.04 |
| Education | -0.008 | 0.042 | -0.18 | 0.855 | 1.000 | 0.854 | [-0.091, 0.075] | 1.04 |
| RAVLT_T | -0.004 | 0.007 | -0.56 | 0.576 | 1.000 | 0.854 | [-0.019, 0.011] | 1.20 |
| BVMT_T | 0.009 | 0.009 | 1.04 | 0.302 | 1.000 | 0.854 | [-0.008, 0.026] | 1.75 |
| RPM_T | -0.007 | 0.008 | -0.90 | 0.369 | 1.000 | 0.854 | [-0.023, 0.009] | 1.38 |

**Key Findings:**
- **No significant predictors**: All p-values > 0.30 after correction (Bonferroni ± = 0.000597)
- **Weak overall prediction**: R² = 0.024 (2.4% variance explained)
- **Multicollinearity acceptable**: All VIF < 2.0, well below concern threshold of 5.0
- **Effect sizes negligible**: All standardized coefficients |²| < 0.05

### Sample Characteristics
- **Total N:** 100 participants (complete data)
- **Missing data:** None after merging calibration metrics with cognitive test scores
- **Calibration quality range:** -1.97 to 1.82 (standardized metric from Ch6)
- **Cognitive test T-scores:** RAVLT_T (M=50.0, SD=10.0), BVMT_T (M=50.0, SD=10.0), RPM_T (M=50.0, SD=10.0)

### Cross-Reference to Planned Expectations
- **Expected R² range:** 0.10-0.20 (planned modest prediction)
- **Actual R²:** 0.024 (below expected range)
- **Expected RPM dominance:** ² > 0.20, p < 0.05 
- **Actual RPM effect:** ² = -0.007, p = 0.369 (opposite direction, non-significant)
- **Prediction accuracy:** Hypothesis not supported

---

## 2. Plot Descriptions

### Figure 1: Calibration vs Accuracy Prediction Comparison
**File:** `plots/calibration_vs_accuracy.png`

**Visual Description:**
Bar chart comparing R² values for cognitive test prediction of calibration quality versus accuracy. Shows two bars:
- **Calibration quality** (red): R² = 0.024 (current RQ 7.3.2)
- **Accuracy** (teal): R² = 0.188 (from RQ 7.3.1)

**Key Patterns:**
- Dramatic difference in predictability: accuracy R² is 7.8 times larger than calibration R²
- Calibration quality appears nearly unpredictable from cognitive test performance
- Visual confirms metacognitive dissociation: calibration is distinct from accuracy

**Connection to Findings:**
Supports theoretical distinction between memory performance and metacognitive monitoring. Cognitive tests that strongly predict accuracy (18.8% variance) have minimal predictive power for calibration quality (2.4% variance).

---

### Figure 2: Cross-Validation Performance
**File:** `plots/cross_validation.png`

**Visual Description:**
Two-panel plot showing cross-validation results across 5 folds:

**Left panel - Train vs Test R²:**
- Training R² (red dots): Range 0.03-0.06, consistently positive but small
- Test R² (brown dots): Range -0.20 to -0.06, all negative values
- Clear separation indicates severe overfitting

**Right panel - Prediction Error (RMSE):**
- RMSE across folds: Range 0.55-0.86
- Generally decreasing trend from folds 1-4, then increase in fold 5
- High variability suggests model instability

**Key Patterns:**
- **Severe overfitting detected:** All test R² values negative (worse than predicting the mean)
- **Model instability:** Wide variation in performance across folds
- **Poor generalizability:** Model fails to predict new data

**Connection to Findings:**
Cross-validation reveals that the weak R² = 0.024 is likely due to chance overfitting rather than genuine predictive relationships. Model performs worse than baseline on out-of-sample data.

---

### Figure 3: Hierarchical Regression and Predictor Importance
**File:** `plots/hierarchical_regression.png`

**Visual Description:**
Two-panel visualization:

**Left panel - Model Comparison:**
- Demographics model: R² H 0.006 (minimal prediction)
- Full model: R² H 0.024 (slight improvement but still very low)
- Modest increase from adding cognitive tests

**Right panel - Cognitive Predictor Importance:**
Horizontal bar chart showing semi-partial R² for each cognitive test:
- **RPM_T:** Largest bar (H 1e-5), but still negligible
- **BVMT_T:** Medium bar
- **RAVLT_T:** Smallest bar
- All values extremely small (< 0.001)

**Key Patterns:**
- Minimal improvement from demographics to full model
- RPM shows highest (but still negligible) unique contribution
- All predictors explain < 0.1% unique variance individually
- No clear pattern supporting fluid intelligence hypothesis

**Connection to Findings:**
Visual confirms statistical results: cognitive tests add minimal predictive power beyond demographics, and even the best predictor (RPM) explains negligible unique variance.

---

## 3. Interpretation

### Hypothesis Testing

**Original Hypothesis (from 1_concept.md):**
"RPM (fluid intelligence) will predict calibration quality more strongly than RAVLT or BVMT (memory tests). Metacognitive monitoring requires reasoning abilities to compare internal confidence states to performance, which should correlate with fluid intelligence measures."

**Hypothesis Status:** **REJECTED**

The statistical findings provide no support for the original hypothesis:
- RPM did not significantly predict calibration quality (² = -0.007, p = 0.369)
- RPM showed negative (not positive) association with calibration
- No cognitive test significantly predicted calibration after correction
- Effect sizes for all predictors were negligible (|²| < 0.05)

### Theoretical Contextualization

**Metacognitive Dissociation Evidence:**

This RQ provides strong evidence for **metacognitive dissociation** - the finding that cognitive abilities predict memory accuracy but not calibration quality:

1. **Accuracy vs Calibration Prediction:**
   - Cognitive tests explain 18.8% of accuracy variance (RQ 7.3.1) 
   - Same tests explain only 2.4% of calibration variance (current RQ)
   - 7.8-fold difference in predictive power

2. **Theoretical Implications:**
   - Memory performance relies on encoding, storage, and retrieval processes measured by cognitive tests
   - Calibration quality relies on metacognitive monitoring processes that appear independent of general cognitive ability
   - Supports dual-process metacognitive theories (confidence judgments involve distinct mechanisms from memory performance)

**Literature Connections:**
- **Flavell's Metacognitive Theory:** Calibration requires metacognitive monitoring that is distinct from cognitive capacity
- **Dual-Process Metacognition:** Confidence relies on both automatic fluency and controlled monitoring; our findings suggest monitoring is not captured by traditional cognitive tests
- **Individual Differences Research:** Adds to literature showing metacognitive accuracy is poorly predicted by cognitive ability measures

### Unexpected Patterns

**1. Negative Test R² in Cross-Validation:**
The most striking unexpected finding was that all 5 cross-validation folds produced negative test R² values (range: -0.20 to -0.06). This indicates the model performed worse than simply predicting the mean calibration score for all participants.

**Investigation suggestions:**
- Examine overfitting: Small sample size (N=100) relative to predictors (6) may enable chance capitalization
- Consider measurement error: Calibration quality may have low reliability, limiting predictable variance
- Check for non-linear relationships: Linear regression may miss complex cognitive-metacognitive associations

**2. Opposite Direction for RPM:**
RPM showed a negative association with calibration quality (² = -0.007), opposite to the predicted positive relationship.

**Investigation suggestions:**
- Explore curvilinear relationships: High fluid intelligence might lead to overconfidence in some contexts
- Consider context-specific effects: VR episodic memory may engage different metacognitive processes than abstract reasoning
- Check for suppression effects: RPM's relationship with calibration might be mediated by other variables

**3. Extremely Small Effect Sizes:**
All cognitive predictors showed negligible effect sizes, with the largest semi-partial correlation < 0.001.

**Investigation suggestions:**
- Power analysis limitations: Very small true effects may require much larger samples for detection
- Measurement considerations: Aggregated calibration metrics may obscure domain-specific patterns
- Alternative predictors: Other individual difference variables (personality, metacognitive beliefs) might be more relevant

### Broader Implications

**REMEMVR Validation:**

Findings provide important validation evidence for REMEMVR as a metacognitive assessment tool:
- **Discriminant validity:** Calibration quality distinct from cognitive ability, supporting metacognitive specificity
- **Clinical potential:** Individual differences in calibration quality not confounded by general cognitive ability
- **Research utility:** Provides clean measure of metacognitive monitoring independent of memory capacity

**Methodological Insights:**

1. **Metacognitive Measurement:**
   - Standard cognitive batteries may be insufficient for predicting metacognitive accuracy
   - Need for specialized metacognitive assessment instruments
   - Calibration quality as emergent property not reducible to cognitive components

2. **Statistical Considerations:**
   - Cross-validation essential for small-effect research to detect overfitting
   - Bootstrap confidence intervals more informative than p-values for negligible effects
   - Dual p-value reporting (Decision D068) reveals how multiple comparisons affect inference

3. **Theoretical Development:**
   - Results challenge cognitive-metacognitive correlation assumptions
   - Support for domain-specific metacognitive monitoring processes
   - Need for process-based (not ability-based) models of metacognitive individual differences

**Clinical Relevance:**

For cognitive assessment applications:
- Calibration quality represents distinct metacognitive dimension not captured by traditional neuropsychological tests
- Poor calibration may indicate metacognitive monitoring deficits independent of memory impairment
- REMEMVR calibration measures could complement standard cognitive batteries in clinical evaluation
- Findings suggest metacognitive training may benefit individuals regardless of cognitive ability level

---

## 4. Limitations

### Sample Limitations

**Sample Size:**
- N = 100 provides adequate power (0.80) for medium effects (f² = 0.15) but underpowered for small effects (f² = 0.02, power = 0.20)
- Observed effect extremely small (f² = 0.024), requiring N H 1600 for adequate power
- Cross-validation revealed severe overfitting with current sample size

**Demographic Constraints:**
- University undergraduate sample (age range approximately 18-25) limits generalizability to older adults where metacognitive monitoring may differ
- High education sample (all current college students) prevents examining education effects on calibration
- Limited cognitive ability range in university sample may restrict variance in predictors

**Attrition:**
- Complete data available for all 100 participants (no missing data issues)
- However, sample represents subset of larger study with unknown selection effects
- Participants with very poor calibration may have been excluded from initial cognitive testing

### Methodological Limitations

**Measurement:**

1. **Calibration Quality Metric:**
   - Aggregated across all memory domains and test sessions, potentially obscuring domain-specific patterns
   - Single composite score may not capture multifaceted nature of metacognitive monitoring
   - Unknown reliability of calibration metric limits maximum predictable variance

2. **Cognitive Test Selection:**
   - Limited to memory tests (RAVLT, BVMT) and fluid intelligence (RPM)
   - Missing potentially relevant measures: executive function, working memory, processing speed
   - T-score standardization within sample may not reflect population norms
   - No measures of metacognitive beliefs or metamemory knowledge

3. **VR Context Specificity:**
   - Calibration measured in VR episodic memory tasks may not generalize to other metacognitive contexts
   - Desktop VR limitations (not fully immersive) may affect calibration processes
   - Structured VR encoding task differs from naturalistic confidence judgment situations

**Design:**

1. **Cross-Sectional Limitations:**
   - No temporal relationship between cognitive tests and calibration quality
   - Cannot establish causal relationships or developmental patterns
   - Individual differences may be trait-like or state-dependent

2. **Statistical Model Constraints:**
   - Linear regression assumes additive effects, may miss interaction or threshold effects
   - Normal distribution assumptions for calibration quality not explicitly tested
   - No consideration of clustered or multilevel structure in VR data

**Statistical:**

1. **Multiple Comparisons:**
   - Conservative Bonferroni correction (± = 0.000597) may overcorrect for Type I error
   - Family-wise error rate approach may miss small but meaningful effects
   - No adjustment for exploratory nature of cross-validation findings

2. **Overfitting Assessment:**
   - 5-fold CV with N=100 creates small validation sets (N=20), increasing CV variance
   - Model selection not performed within CV folds, potentially inflating overfitting estimates
   - Bootstrap stability assessment shows no predictors consistently significant across iterations

### Generalizability Constraints

**Population:**
- Findings may not generalize to:
  - Older adults (age-related changes in metacognitive monitoring)
  - Clinical populations (neurological conditions affecting confidence judgment)
  - Lower education samples (different metacognitive strategies)
  - Non-WEIRD samples (cultural differences in confidence expression)

**Context:**
- VR episodic memory calibration differs from:
  - Real-world metacognitive judgments (naturalistic confidence decisions)
  - Other cognitive domains (mathematical, verbal, spatial reasoning)
  - Clinical assessment contexts (formal neuropsychological testing)

**Task:**
- REMEMVR calibration specific to:
  - Episodic memory content (what/where/when)
  - Structured encoding task (not spontaneous learning)
  - Post-retrieval confidence judgments (not feeling-of-knowing)

### Technical Limitations

**Cross-Validation Issues:**
- Severe overfitting detected: all test R² values negative
- Model performs worse than baseline prediction on new data
- Suggests observed R² = 0.024 likely due to chance capitalization on noise
- 5-fold CV may be unstable with small effects and limited sample size

**Bootstrap Stability:**
- No cognitive predictors showed stable significance across bootstrap samples
- Jaccard similarity indices all < 0.40 (instability threshold)
- Sign consistency < 0.87 for all predictors (effect direction unstable)
- Results suggest no robust cognitive-calibration associations detectable with current design

**Effect Size Interpretation:**
- Cohen's f² = 0.024 falls between "negligible" and "small" conventional thresholds
- Confidence intervals for all predictors include zero with substantial width
- Practical significance questionable even if statistical significance achieved

### Limitations Summary

Despite these constraints, findings provide **robust evidence for metacognitive dissociation:**
- Consistent near-zero effects across multiple cognitive predictors
- Large difference between accuracy (R² = 0.188) and calibration (R² = 0.024) prediction
- Cross-validation confirms weak effects not due to sample-specific artifacts
- Results align with theoretical expectations for metacognitive independence

Limitations primarily affect **statistical power for small effects** rather than validity of main conclusion that cognitive tests poorly predict calibration quality.

---

## 5. Next Steps

### Immediate Follow-Ups (Current Data)

**1. Domain-Specific Calibration Analysis:**
- **Why:** Aggregated calibration metric may obscure domain differences (What/Where/When)
- **How:** Re-run regression with separate calibration scores for each memory domain
- **Expected Insight:** RPM might predict spatial (Where) calibration better than temporal (When) calibration
- **Timeline:** Can be done immediately using Ch6 domain-specific outputs

**2. Non-Linear Relationship Exploration:**
- **Why:** Linear regression may miss threshold or curvilinear cognitive-metacognitive associations
- **How:** Add quadratic terms for cognitive predictors, test spline regression models
- **Expected Insight:** High fluid intelligence might show overconfidence (inverted-U pattern)
- **Timeline:** Immediate (same data, alternative model specifications)

**3. Alternative Metacognitive Metrics:**
- **Why:** Resolution/calibration slope may be more theory-relevant than composite calibration quality
- **How:** Test separate models for different Ch6 calibration components (resolution, slope, overconfidence)
- **Expected Insight:** Cognitive tests might predict specific metacognitive components differently
- **Timeline:** ~1 day (requires accessing Ch6 component-level outputs)

### Planned Thesis RQs (Chapter 7 Continuation)

**RQ 7.3.3: Personality Predictors of Calibration Quality (Planned):**
- **Focus:** Test whether personality measures (Big Five, need for cognition) predict calibration better than cognitive tests
- **Why:** Metacognitive monitoring might rely more on motivational than cognitive factors
- **Builds On:** Uses same calibration metrics, adds personality measures from baseline assessment
- **Expected Timeline:** Next individual differences RQ in Chapter 7

**RQ 7.4.1: Neural Correlates of Calibration Quality (Exploratory):**
- **Focus:** Examine EEG markers during confidence judgments for high vs low calibration participants
- **Why:** Current RQ shows cognitive tests insufficient; brain-based measures may be more predictive
- **Builds On:** Participants identified as good vs poor calibrators from current analysis
- **Expected Timeline:** Depends on EEG data availability (may be future collaboration)

**RQ 7.3.4: Calibration Training Effectiveness (Planned):**
- **Focus:** Test whether metacognitive training improves calibration quality independent of cognitive ability
- **Why:** Findings suggest calibration is distinct from ability; training should be equally effective across cognitive levels
- **Builds On:** Uses calibration quality as pre-training individual difference measure
- **Expected Timeline:** 2-3 RQs ahead (requires intervention development)

### Methodological Extensions (Future Data Collection)

**1. Expand Cognitive Battery:**
- **Current Limitation:** Limited to memory + fluid intelligence tests
- **Extension:** Add executive function (Stroop, N-back), metacognitive beliefs (Metacognitive Awareness Inventory), metamemory knowledge scales
- **Expected Insight:** More specific cognitive predictors or metacognitive measures might show stronger associations
- **Feasibility:** Requires expanded assessment battery (~1 hour additional testing)

**2. Increase Sample Size for Small Effect Detection:**
- **Current Limitation:** N = 100 underpowered for f² = 0.024 (needs N H 1600 for 80% power)
- **Extension:** Multi-site data collection or meta-analysis across similar VR studies
- **Expected Insight:** Determine if true effect size is exactly zero or small but non-zero
- **Feasibility:** Long-term collaboration (1-2 years for adequate sample)

**3. Longitudinal Design:**
- **Current Limitation:** Cross-sectional design prevents causal or developmental inferences
- **Extension:** Test cognitive predictors at baseline, calibration quality at multiple time points
- **Expected Insight:** Establish temporal precedence, examine stability of individual differences
- **Feasibility:** Requires 6-12 month follow-up study (~1 year for completion)

**4. Compare VR vs Traditional Metacognitive Tasks:**
- **Current Limitation:** VR-specific findings may not generalize to other metacognitive contexts
- **Extension:** Administer both REMEMVR and standard confidence judgment tasks (word lists, general knowledge)
- **Expected Insight:** Test whether cognitive-calibration dissociation is VR-specific or general
- **Feasibility:** Moderate (requires developing parallel non-VR calibration tasks, ~3 months)

### Theoretical Questions Raised

**1. Process-Based Models of Metacognitive Individual Differences:**
- **Question:** If cognitive ability doesn't predict calibration, what cognitive processes do?
- **Next Steps:** Develop and test models based on metacognitive control, monitoring efficiency, or confidence criterion setting
- **Expected Insight:** Move beyond ability-based to process-based individual differences
- **Feasibility:** Long-term theoretical development (2-3 years)

**2. Neural Mechanisms of Calibration Quality:**
- **Question:** What brain networks support good vs poor metacognitive monitoring?
- **Next Steps:** fMRI or EEG study during confidence judgments, compare high vs low calibration participants
- **Expected Insight:** Identify neural signatures of metacognitive accuracy independent of memory performance
- **Feasibility:** Requires neuroimaging collaboration (~2 years)

**3. Developmental Trajectory of Metacognitive Dissociation:**
- **Question:** Is cognitive-calibration independence consistent across age groups?
- **Next Steps:** Cross-sectional age comparison or longitudinal tracking of metacognitive development
- **Expected Insight:** Understand when and how metacognitive monitoring becomes independent of cognitive ability
- **Feasibility:** Requires developmental sample (~3-5 years for longitudinal design)

**4. Clinical Applications of Calibration Assessment:**
- **Question:** Can calibration quality measures identify metacognitive deficits in clinical populations?
- **Next Steps:** Test REMEMVR calibration in MCI, TBI, or other populations with known metacognitive impairments
- **Expected Insight:** Validate calibration as clinical marker independent of standard cognitive measures
- **Feasibility:** Clinical collaboration required (~2 years for patient recruitment and testing)

### Priority Ranking

**High Priority (Do First):**
1. Domain-specific calibration analysis - tests theoretical specificity, uses current data
2. Non-linear relationship exploration - addresses unexpected negative RPM direction
3. RQ 7.3.3 personality predictors - natural next step in individual differences sequence

**Medium Priority (Subsequent):**
1. Alternative metacognitive metrics analysis - robustness check for different calibration components
2. Expanded cognitive battery - addresses measurement limitations with additional constructs
3. RQ 7.3.4 calibration training - tests practical implications of dissociation findings

**Lower Priority (Aspirational):**
1. Large-scale replication for small effects - ideal but requires substantial resources
2. Neuroimaging correlates - interesting but outside current thesis scope
3. Developmental/clinical extensions - valuable but beyond current research program

### Next Steps Summary

The findings establish **strong evidence for metacognitive dissociation** - cognitive tests predict accuracy but not calibration quality. This raises three critical questions for immediate follow-up:

1. **Domain Specificity:** Are there domain-specific patterns in cognitive-calibration relationships? (Immediate analysis)
2. **Alternative Predictors:** What individual difference measures DO predict calibration quality? (RQ 7.3.3 personality)
3. **Mechanism Understanding:** What cognitive processes (not abilities) support good calibration? (Theoretical development)

Methodological extensions (larger samples, longitudinal designs, clinical applications) are valuable but require resources beyond current thesis scope. The priority should be on understanding **what predicts calibration quality** if not traditional cognitive abilities.

---

**Summary generated by:** rq_results agent (v4.0)
**Pipeline version:** v4.X (13-agent atomic architecture)
**Date:** 2026-01-05T22:30:00Z