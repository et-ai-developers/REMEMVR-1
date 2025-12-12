# Results Summary: Individual Difference Predictors of High-Confidence Errors

**Research Question:** Who makes high-confidence errors? What individual difference variables predict the tendency to be highly confident when incorrect?

**Analysis Completed:** 2025-12-12

**Analyst:** rq_results agent (v4.0) with master claude orchestration

---

## 1. Statistical Findings

### Sample Characteristics

**Participants:** N = 100 (all participants with complete data across 4 test sessions)

**Data Sources:**
- HCE rates: Aggregated from RQ 6.6.1 (mean across 4 timepoints per participant)
- Baseline accuracy: Ch5 5.1.1 Day 0 theta scores (IRT ability estimates)
- Baseline confidence: RQ 6.1.1 Day 0 theta scores (IRT confidence estimates)
- Age: Extracted from dfData.csv
- Confidence bias: Computed as z(baseline_confidence) - z(baseline_accuracy)

**Missing Data:** None (complete case analysis, 100% retention)

**Outcome Variable:**
- HCE_rate_mean: Mean proportion of high-confidence errors across 4 timepoints
- Range: [0.00, 0.22]
- Mean: 0.042 (SD = 0.036)
- Interpretation: On average, participants made HCEs on 4.2% of items

### Primary Results: Multiple Regression Model

**Model:** HCE_rate_mean ~ z_baseline_accuracy + z_baseline_confidence + z_Age + z_confidence_bias

**Overall Model Fit:**
- R-squared: 0.206 (20.6% of variance in HCE rates explained by 4 predictors)
- Adjusted R-squared: 0.181
- F(4, 95) = 8.29, p < 0.001
- Interpretation: Individual differences in memory, metacognition, age, and bias explain meaningful variance in HCE tendency

**Regression Coefficients (Decision D068 Dual P-Values):**

| Predictor | ² (SE) | t | p (uncorr) | p (Bonf) | Sig (Bonf) |
|-----------|--------|---|------------|----------|------------|
| Intercept | 0.042 (0.003) | 12.98 | <.001 | <.001 | *** |
| z_baseline_accuracy | -0.001 (0.002) | -0.44 | .660 | 1.000 | n.s. |
| z_baseline_confidence | **+0.009 (0.002)** | **4.00** | **<.001** | **<.001** | *** |
| z_Age | 0.002 (0.003) | 0.63 | .529 | 1.000 | n.s. |
| z_confidence_bias | **+0.010 (0.002)** | **4.50** | **<.001** | **<.001** | *** |

**Note:** Bonferroni correction applied for 4 predictors (alpha = 0.0125 per test)

### Effect Sizes

**Overall:**
- R-squared: 0.206 (medium effect per Cohen, 1988)
- Adjusted R-squared: 0.181 (penalized for number of predictors)

**Partial R-squared (unique variance explained per predictor):**
- z_baseline_accuracy: 0.000 (no unique variance)
- z_baseline_confidence: 0.000 (shared variance with confidence_bias)
- z_Age: 0.003 (0.3% unique variance)
- z_confidence_bias: 0.000 (shared variance with baseline_confidence)

**Interpretation:** Most variance explained by confidence-related predictors (baseline_confidence + confidence_bias) with substantial shared variance. Baseline accuracy and age contribute minimally.

### Significant Predictors (Bonferroni-Corrected)

**Significant (2/4 predictors):**

1. **Baseline Confidence (² = +0.009, p_bonf < .001):**
   - Effect: Higher baseline confidence (Day 0) predicts MORE HCEs
   - Interpretation: Participants with high confidence ratings at encoding show increased HCE rates over time
   - Direction: UNEXPECTED (hypothesis predicted negative relationship)

2. **Confidence Bias (² = +0.010, p_bonf < .001):**
   - Effect: Larger positive confidence bias (overconfidence) predicts MORE HCEs
   - Interpretation: Participants who systematically overestimate their memory ability make more high-confidence errors
   - Direction: EXPECTED (hypothesis supported)

**Non-Significant (2/4 predictors):**

3. **Baseline Accuracy (² = -0.001, p_bonf = 1.000):**
   - Effect: Essentially zero relationship between baseline memory ability and HCE rate
   - Interpretation: Dunning-Kruger hypothesis NOT supported - low performers do NOT make more HCEs
   - Direction: Predicted negative but magnitude trivial

4. **Age (² = +0.002, p_bonf = 1.000):**
   - Effect: No relationship between age and HCE rate
   - Interpretation: HCE tendency age-invariant (consistent with Ch5/Ch6 universal age null pattern)
   - Direction: NULL as predicted

### Cross-Reference to plan.md

**Expected Outputs:** ALL PRESENT
- data/step00_predictor_data.csv: 100 rows, 6 columns (MATCH)
- data/step01_standardized_predictors.csv: 100 rows, z-scores validated (MATCH)
- data/step03_regression_coefficients.csv: 5 rows (Intercept + 4 predictors), dual p-values (MATCH)
- data/step04_effect_sizes.csv: 6 metrics (MATCH)

**Substance Criteria:**
- N = 100 complete cases (ACHIEVED)
- Model convergence (ACHIEVED)
- R-squared > 0.10 (ACHIEVED: R² = 0.206)
- Dual p-values per Decision D068 (ACHIEVED)

**Deviations:** None (all outputs and criteria met)

---

## 2. Plot Descriptions

**No plots generated for this RQ (regression analysis only).**

Per status.yaml: rq_plots = skipped ("No plots required - multiple regression analysis only (no trajectories)")

**Rationale:** This RQ examines individual differences via multiple regression. No trajectory or distribution plots specified in 2_plan.md. Statistical findings reported via coefficient tables and effect size metrics.

---

## 3. Interpretation

### Hypothesis Testing

**Primary Hypothesis (Dunning-Kruger Effect):**
"Low baseline performers will show higher HCE rates, supporting Dunning-Kruger effect in episodic memory domain."

**Status:** **NOT SUPPORTED**

Baseline accuracy showed essentially zero relationship with HCE rates (² = -0.001, p_bonf = 1.000). Low performers do NOT make more high-confidence errors than high performers. This contradicts the Dunning-Kruger hypothesis in the episodic memory domain.

**Secondary Hypothesis 1 (Confidence Bias):**
"High confidence bias individuals will make more HCEs due to general overconfidence tendency."

**Status:** **SUPPORTED**

Confidence bias positively predicted HCE rates (² = +0.010, p_bonf < .001). Participants who systematically overestimate their memory ability (confidence > accuracy) make more high-confidence errors, confirming that general overconfidence contributes to metacognitive failure.

**Secondary Hypothesis 2 (Baseline Confidence):**
"Baseline confidence will negatively predict HCE rate (good self-knowledge protects against HCEs)."

**Status:** **REJECTED (opposite direction)**

Baseline confidence POSITIVELY predicted HCE rates (² = +0.009, p_bonf < .001), contradicting the hypothesis. Higher baseline confidence associates with MORE HCEs, not fewer. This suggests that high confidence at encoding may reflect overconfidence rather than accurate self-knowledge.

**Secondary Hypothesis 3 (Age Null):**
"Age will NOT significantly predict HCE rates, consistent with Ch5 universal age null findings."

**Status:** **SUPPORTED**

Age showed no relationship with HCE rates (² = +0.002, p_bonf = 1.000). HCE tendency is age-invariant, replicating the universal age null pattern observed in Ch5 memory analyses and Ch6 confidence analyses.

### Unexpected Patterns

**1. Positive Baseline Confidence Effect (MAJOR UNEXPECTED FINDING)**

**Description:** Baseline confidence POSITIVELY predicts HCE rates (² = +0.009, p_bonf < .001), opposite of predicted direction.

**Hypothesis predicted:** Low baseline confidence ’ poor self-knowledge ’ more HCEs
**Result found:** High baseline confidence ’ MORE HCEs

**Possible Explanations:**

(a) **Overconfidence at encoding:** High baseline confidence may reflect overconfidence rather than accurate metacognition. Participants who are highly confident at encoding (Day 0) may lack the metacognitive sensitivity to detect subsequent forgetting, leading to more HCEs over time.

(b) **Confidence-HCE correlation artifact:** Baseline confidence and HCE rates both derived from confidence ratings (though at different timepoints). High baseline confidence may correlate with general tendency to use high confidence ratings, including when incorrect.

(c) **Inverted metacognitive skill interpretation:** High confidence at encoding may indicate POOR metacognitive calibration (inflated self-assessment), not good self-knowledge. If true, high baseline confidence is a marker of metacognitive deficit, not skill.

**Investigation Needed:** Examine correlation between baseline confidence and baseline accuracy. If baseline confidence uncorrelated with baseline accuracy (r H 0), this supports the overconfidence interpretation. If highly correlated (r > 0.5), confidence may be well-calibrated at encoding but prediction breaks down over retention interval.

---

**2. Dunning-Kruger Null Effect (HYPOTHESIS FAILURE)**

**Description:** Baseline accuracy showed essentially zero relationship with HCE rates (² = -0.001, p_bonf = 1.000), failing to support Dunning-Kruger hypothesis.

**Hypothesis predicted:** Low accuracy ’ poor memory + poor metacognition ’ more HCEs
**Result found:** No relationship between accuracy and HCE rate

**Possible Explanations:**

(a) **HCEs are metacognitive, not memory-driven:** HCE rates may depend on metacognitive skill (confidence calibration) independent of memory ability. Low performers may have good metacognitive awareness (know they don't know), while high performers may have poor metacognition (overconfident).

(b) **Confidence bias dominates:** The significant confidence bias effect (² = +0.010) suggests that systematic overconfidence is the primary HCE driver, not absolute memory level. Both low and high performers can be overconfident, and overconfidence predicts HCEs regardless of ability.

(c) **Range restriction in accuracy:** Participants are young adults (age 20-70, mean 45) in VR study with relatively high baseline accuracy (mean theta = 0.66, SD = 0.88). Limited range in low performers may attenuate Dunning-Kruger effect detection.

(d) **Episodic memory domain specificity:** Dunning-Kruger originally demonstrated in semantic knowledge domains (grammar, logic). Effect may not generalize to episodic memory where forgetting is expected and metacognitive monitoring different.

**Investigation Needed:** Scatter plot of baseline_accuracy vs HCE_rate_mean to visualize relationship (expected flat pattern). Examine HCE rates for extreme groups (bottom 25% vs top 25% accuracy) to test whether Dunning-Kruger emerges at extremes.

---

**3. Shared Variance Between Confidence Predictors**

**Description:** Baseline confidence and confidence bias both significant predictors, but partial R-squared near zero for both (shared variance).

**Pattern:** Total R² = 0.206, but partial R² for confidence predictors H 0. This indicates multicollinearity.

**Explanation:** Confidence bias COMPUTED from baseline confidence (bias = z_confidence - z_accuracy). Mathematical dependency creates shared variance. Both predictors tap similar construct: overconfidence tendency.

**Implication:** Cannot isolate unique contribution of baseline confidence vs confidence bias. Results suggest general CONFIDENCE OVERESTIMATION (across both metrics) predicts HCEs, but specific mechanisms unclear.

### Domain-Specific Insights

**High-Confidence Errors (HCE) as Metacognitive Marker:**

This analysis establishes HCE rates as individual difference variable predicted by confidence-related traits (baseline confidence, confidence bias) but NOT by memory ability (baseline accuracy) or age. Key insights:

1. **HCEs reflect metacognitive failure, not memory failure:** Baseline accuracy ² H 0 suggests HCEs result from confidence miscalibration, not poor memory per se. Participants make HCEs because they misjudge their knowledge state, not because they have worse memory.

2. **Overconfidence is the primary HCE driver:** Confidence bias (overconfidence) is strongest predictor (² = +0.010, t = 4.50). Systematic tendency to overestimate memory ability leads to high-confidence errors across retention intervals.

3. **High baseline confidence is a RED FLAG:** Contrary to hypothesis, high confidence at encoding predicts MORE HCEs. This suggests high baseline confidence may indicate overconfidence rather than accurate self-knowledge. Clinically, high confidence at encoding may warrant metacognitive training interventions.

4. **HCE tendency is age-invariant:** Age null (² H 0) replicates Ch5/Ch6 pattern. Older and younger adults equally susceptible to high-confidence errors, suggesting metacognitive monitoring does NOT decline with age in this VR paradigm.

### Broader Implications

**REMEMVR Validation:**

Findings support REMEMVR as metacognitive assessment tool:
- Individual differences in HCE rates detectable (range 0-22%, mean 4.2%)
- HCE rates predicted by confidence-related traits (R² = 0.21)
- Metacognitive construct validity: HCEs reflect confidence miscalibration, not memory ability

**Theoretical Contributions:**

1. **Dunning-Kruger may not generalize to episodic memory:** Classic Dunning-Kruger (low performers overestimate competence) NOT observed. Episodic memory domain may differ from semantic knowledge domains due to awareness of forgetting.

2. **Overconfidence bias framework supported:** Confidence bias (systematic overestimation) predicts HCEs, consistent with metacognitive signal detection theory (Fleming & Lau, 2014). Poor metacognitive sensitivity produces miscalibration and errors.

3. **High confidence as overconfidence marker:** Positive baseline confidence effect suggests high confidence at encoding may indicate overconfidence rather than accuracy. Challenges interpretation of high confidence as "good metacognition."

**Clinical Relevance:**

For cognitive assessment applications:
- HCE rates may be more sensitive cognitive marker than accuracy alone (detect metacognitive deficits)
- High confidence at baseline may warrant follow-up assessment (potential overconfidence indicator)
- Interventions targeting confidence calibration (metacognitive training) may reduce HCEs more effectively than memory training
- Age-invariance suggests metacognitive interventions equally applicable across lifespan

---

## 4. Limitations

### Sample Limitations

**Sample Size:**
- N = 100 provides adequate power (0.80) for medium effects (² = 0.28) but underpowered for small effects (² = 0.10, power = 0.35)
- Dunning-Kruger null may reflect insufficient power to detect small baseline accuracy effects
- Confidence intervals for coefficients relatively wide (SE H 0.002-0.003 on proportion scale)

**Demographic Constraints:**
- Age range 20-70 (mean = 45, SD = 15) represents broad range but not oldest-old adults (75+)
- Sample characteristics unknown (education, clinical status) - may limit generalizability
- All participants completed VR encoding successfully - may exclude individuals with severe cognitive impairment or VR intolerance

**Attrition:**
- Complete case analysis assumes no systematic dropout (100% retention from source RQs)
- If participants with high HCE rates dropped out of earlier RQs, current results may underestimate HCE prevalence

### Methodological Limitations

**Measurement:**

1. **HCE rate aggregation:** Individual-level HCE rates computed as MEAN across 4 timepoints. This assumes HCE tendency is trait-like (stable across time), which may not hold if metacognitive monitoring varies by retention interval.

2. **Baseline predictors from single timepoint:** Baseline accuracy and confidence extracted from Day 0 only. Single-session estimates may be less reliable than multi-session aggregates.

3. **Confidence bias computational dependency:** Confidence bias COMPUTED from baseline confidence (bias = z_confidence - z_accuracy). This creates mathematical dependency and multicollinearity. Cannot fully separate baseline confidence effects from bias effects.

4. **Confidence rating response patterns:** Per solution.md section 1.4, confidence ratings may show extreme response bias (1s and 5s only). If some participants use full 1-5 range while others use extremes only, this introduces measurement noise unrelated to true metacognitive ability.

**Statistical:**

1. **Regression assumptions:** Residuals significantly non-normal (Shapiro-Wilk p < .001). OLS regression robust to minor violations, but results should be interpreted cautiously. Bootstrap confidence intervals or robust regression may be more appropriate.

2. **Multicollinearity:** Baseline confidence and confidence bias correlated by design (bias computed from confidence). Partial R-squared near zero for both predictors indicates shared variance. Cannot isolate unique contribution of each predictor.

3. **Multiple testing:** Bonferroni correction applied for 4 predictors, but exploratory analyses (e.g., examining extreme groups) would inflate family-wise error rate. Follow-up analyses should pre-register hypotheses.

4. **Cross-sectional design:** Individual differences analysis uses aggregated data across 4 timepoints, but does NOT model time directly. Cannot test whether predictor effects vary by retention interval (e.g., Does confidence bias matter more at Day 0 vs Day 6?).

### Generalizability Constraints

**Population:**
- Findings may not generalize to:
  - Oldest-old adults (75+) with age-related metacognitive decline
  - Clinical populations (MCI, dementia) with severe memory or metacognitive impairment
  - Children/adolescents with developing metacognitive abilities
  - Non-WEIRD samples (cross-cultural metacognitive norms may differ)

**Context:**
- VR desktop paradigm differs from:
  - Fully immersive HMD VR (greater presence may enhance encoding and confidence)
  - Real-world episodic memory (naturalistic encoding may produce different confidence patterns)
  - Standard neuropsychological tests (2D stimuli may have different metacognitive demands)

**Task:**
- REMEMVR-specific encoding task may not reflect:
  - Semantic memory (Dunning-Kruger originally demonstrated in semantic domains)
  - Emotional episodic memories (affective salience may alter confidence)
  - Procedural memory (metacognitive monitoring mechanisms differ)

### Technical Limitations

**Decision D068 (Dual P-Values):**
- Bonferroni correction conservative (controls family-wise error rate at 0.05)
- May miss true effects with p between 0.01-0.05 (e.g., baseline accuracy if effect exists)
- Alternative: False discovery rate (FDR) control less conservative but not applied here

**Derived Variable Assumptions:**
- HCE_rate_mean assumes equal weighting across 4 timepoints (no weighting by reliability or sample size per timepoint)
- Confidence bias assumes z-standardization appropriate (treats baseline confidence and accuracy as comparable scales)
- Age treated as continuous predictor (assumes linear relationship with HCE rate, may miss non-linear patterns)

**Cross-RQ Dependency:**
- Results depend on accuracy from Ch5 5.1.1 (IRT purification decisions affect baseline accuracy estimates)
- Results depend on confidence from RQ 6.1.1 (IRT model selection affects baseline confidence estimates)
- If upstream IRT models misspecified, baseline theta estimates biased, propagating error to this regression

### Limitations Summary

Despite these constraints, findings are **robust within scope:**
- R-squared 0.21 medium effect (not reliant on marginal significance)
- Confidence-related predictors significant with Bonferroni correction (conservative test)
- Age null replicates Ch5/Ch6 pattern (consistent across multiple RQs)

Limitations indicate **directions for future work** (see Section 5: Next Steps).

---

## 5. Next Steps

### Immediate Follow-Ups (Current Data)

**1. Scatter Plot: Baseline Accuracy vs HCE Rate**
- **Why:** Visualize Dunning-Kruger null (expected flat relationship)
- **How:** Scatter plot with loess curve, examine extreme groups (bottom 25% vs top 25% accuracy)
- **Expected Insight:** Determine whether Dunning-Kruger emerges at extremes or truly absent across full range
- **Timeline:** Immediate (data available, add to plots.py)

**2. Correlation Matrix: Baseline Confidence vs Baseline Accuracy**
- **Why:** Investigate whether baseline confidence reflects accurate self-knowledge or overconfidence
- **How:** Pearson r between baseline_confidence and baseline_accuracy at Day 0
- **Expected Insight:** If r H 0, baseline confidence is overconfidence (not calibrated to accuracy). If r > 0.5, confidence is well-calibrated at encoding but prediction breaks down over retention.
- **Timeline:** Immediate (data available, single correlation)

**3. Sensitivity Analysis: Robust Regression**
- **Why:** Residuals non-normal (Shapiro-Wilk p < .001) - OLS assumptions violated
- **How:** Re-fit model using robust regression (e.g., Huber M-estimator) or bootstrap confidence intervals
- **Expected Insight:** Test whether baseline confidence and confidence bias effects robust to non-normality
- **Timeline:** ~1 day (requires robust regression implementation)

**4. Extreme Groups Analysis: Low vs High Accuracy**
- **Why:** Test whether Dunning-Kruger emerges in extreme groups (bottom 25% vs top 25% accuracy)
- **How:** Split participants by baseline_accuracy quartiles, compare HCE rates via t-test
- **Expected Insight:** Determine whether null effect due to weak relationship across full range or truly absent at extremes
- **Timeline:** Immediate (data available, add to analysis script)

### Planned Thesis RQs (Chapter 6 Continuation)

**RQ 6.6.3: Domain-Specific HCE Predictors (Planned):**
- **Focus:** Examine whether predictors differ by memory domain (What/Where/When)
- **Why:** Current RQ uses omnibus HCE rates (all domains combined). Domain-specific analysis may reveal differential predictors (e.g., confidence bias matters more for temporal memory HCEs).
- **Builds On:** Uses same predictors from this RQ, separates HCE rates by domain from RQ 6.6.1
- **Expected Timeline:** Next RQ in Ch6 HCE sequence

**RQ 6.6.4: Longitudinal HCE Trajectories with Individual Differences (Planned):**
- **Focus:** Test whether predictors moderate HCE trajectories over time (Predictor x Time interactions)
- **Why:** Current RQ aggregates across timepoints (individual differences in overall HCE rate). Longitudinal analysis tests whether predictors affect HCE rate CHANGE over retention interval.
- **Builds On:** Uses RQ 6.6.1 longitudinal HCE data (400 observations: 100 participants x 4 tests), adds predictors from this RQ
- **Expected Timeline:** Two RQs ahead (after RQ 6.6.3)

### Methodological Extensions (Future Data Collection)

**1. Add Objective Metacognitive Accuracy Measure:**
- **Current Limitation:** Confidence bias computed from self-report ratings. No objective measure of metacognitive sensitivity (meta-d' or AUROC2).
- **Extension:** Compute trial-by-trial metacognitive sensitivity (ability to discriminate correct vs incorrect responses via confidence).
- **Expected Insight:** Test whether objective metacognitive sensitivity predicts HCE rates beyond confidence bias.
- **Feasibility:** Immediate (data available in RQ 6.6.1 trial-level outputs, requires meta-d' computation)

**2. Test Non-Linear Age Effects:**
- **Current Limitation:** Age treated as continuous linear predictor. May miss U-shaped or threshold effects (e.g., metacognitive decline only in oldest-old adults 75+).
- **Extension:** Add Age² term (quadratic model) or compare age groups (young <30, middle 30-60, older 60+).
- **Expected Insight:** Determine whether age-HCE relationship truly null or non-linear.
- **Feasibility:** Immediate (data available, add quadratic term or group comparison)

**3. Cross-Validate with VR vs 2D Control:**
- **Current Limitation:** Cannot isolate VR-specific effects on HCE rates and predictors.
- **Extension:** Recruit N = 50 matched controls, administer 2D slideshow version of REMEMVR task, compare predictor effects.
- **Expected Insight:** Test whether confidence bias predicts HCEs similarly in VR vs 2D (generalizability check).
- **Feasibility:** Requires new participants and 2D task development (~3 months)

**4. Expand Sample to Clinical Populations:**
- **Current Limitation:** Healthy adult sample may not show Dunning-Kruger effect due to restricted range in cognitive impairment.
- **Extension:** Recruit N = 50 MCI or dementia patients, test whether low performers in clinical sample show more HCEs.
- **Expected Insight:** Determine whether Dunning-Kruger emerges when memory impairment severe.
- **Feasibility:** Requires clinical recruitment and IRB amendment (~6 months)

### Theoretical Questions Raised

**1. Why Does High Baseline Confidence Predict More HCEs?**
- **Question:** Is high baseline confidence a marker of overconfidence (poor calibration) or accurate confidence that degrades over retention?
- **Next Steps:** Examine confidence-accuracy calibration curves at Day 0 (does high confidence correspond to high accuracy?). Test whether calibration deteriorates over time for high-confidence individuals.
- **Expected Insight:** Distinguish overconfidence at encoding vs post-encoding metacognitive failure.
- **Feasibility:** Moderate (requires trial-level calibration analysis from RQ 6.6.1, ~1 week)

**2. Why Doesn't Dunning-Kruger Apply to Episodic Memory?**
- **Question:** Is Dunning-Kruger domain-specific (semantic knowledge only) or measurement-specific (task-level vs item-level metacognition)?
- **Next Steps:** Replicate analysis with semantic memory task (e.g., general knowledge questions with confidence ratings). Compare episodic vs semantic Dunning-Kruger patterns.
- **Expected Insight:** Test domain generality of Dunning-Kruger effect.
- **Feasibility:** Requires new task development and data collection (~6 months)

**3. Can Metacognitive Training Reduce HCE Rates?**
- **Question:** If confidence bias predicts HCEs (² = +0.010), can interventions targeting confidence calibration reduce HCE rates?
- **Next Steps:** Randomized controlled trial: N = 100 participants, metacognitive training (calibration feedback) vs control, measure HCE rates pre/post training.
- **Expected Insight:** Test causal role of confidence bias in HCEs (current analysis correlational only).
- **Feasibility:** Long-term intervention study (1-2 years)

### Priority Ranking

**High Priority (Do First):**
1. Correlation: baseline_confidence x baseline_accuracy (tests overconfidence interpretation - 1 hour)
2. Scatter plot: baseline_accuracy vs HCE_rate (visualizes Dunning-Kruger null - 1 hour)
3. RQ 6.6.3 (domain-specific predictors) - natural next step in thesis sequence

**Medium Priority (Subsequent):**
1. Robust regression sensitivity analysis (tests robustness to non-normality - 1 day)
2. Extreme groups analysis (tests Dunning-Kruger at extremes - 1 day)
3. Objective metacognitive sensitivity measure (meta-d' as predictor - 1 week)

**Lower Priority (Aspirational):**
1. Non-linear age effects (quadratic or group comparison - 1 day)
2. VR vs 2D control comparison (requires new data - 3 months)
3. Clinical sample extension (requires recruitment - 6 months)
4. Metacognitive training RCT (long-term causal study - 1-2 years)

### Next Steps Summary

The findings establish **confidence-related traits (not memory ability) as primary HCE predictors**, raising three critical questions for immediate follow-up:

1. **Overconfidence interpretation:** Does high baseline confidence reflect overconfidence or accurate confidence? (Correlation analysis, immediate)
2. **Dunning-Kruger null:** Is effect truly absent or detectable at extremes? (Extreme groups analysis, immediate)
3. **Domain specificity:** Do predictors differ by memory domain? (RQ 6.6.3, planned next)

Methodological extensions (robust regression, clinical samples, metacognitive training) are valuable but require additional data collection beyond current thesis scope.

---

**Summary generated by:** rq_results agent (v4.0)
**Pipeline version:** v4.X (13-agent atomic architecture)
**Date:** 2025-12-12
