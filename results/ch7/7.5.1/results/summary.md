# Results Summary: RQ 7.5.1 - Self-Report Predictors of REMEMVR Performance

**Research Question:** Do self-reported factors (typical sleep, education level, VR experience) predict REMEMVR performance?

**Analysis Completed:** 2026-01-06

**Analyst:** rq_results agent (v4.0) with master claude orchestration

---

## 1. Statistical Findings

### Sample Characteristics
- Total N: 100 participants (complete cases)
- Missing data: None in final analysis dataset
- Outliers: 8 participants with Cook's D > 0.04 threshold (8%)
- Age range: Young adults (standardized, M=0, SD=1)

### Hierarchical Regression Results

**Model Comparison:**

| Model | R² | Adjusted R² | F-statistic | p-value | AIC | BIC |
|-------|-----|-------------|-------------|----------|-----|-----|
| Control (Age only) | 0.037 | 0.028 | 3.80 | 0.054 | 204.94 | 210.15 |
| Full (Age + Self-Report) | 0.063 | 0.023 | 1.59 | 0.184 | 208.27 | 221.30 |

**R² Change:** ”R² = 0.025, F-change non-significant (p = 0.184)

**Individual Predictor Coefficients:**

| Predictor | ² | SE | 95% CI | p (uncorrected) | p (Bonferroni) | p (FDR) |
|-----------|---|----|---------|-----------------|--------------------|---------|
| Age_z | -0.051 | 0.036 | [-0.122, 0.019] | 0.153 | 0.153 | 0.153 |
| Education_z | -0.051 | 0.036 | [-0.122, 0.019] | 0.153 | 0.460 | 0.407 |
| VR_Experience_z | 0.047 | 0.067 | [-0.087, 0.181] | 0.488 | 1.000 | 0.488 |
| Typical_Sleep_z | 0.080 | 0.072 | [-0.063, 0.222] | 0.272 | 0.815 | 0.407 |

### Cross-Reference to plan.md
**Expected vs Observed:**
- Plan expected R² = 0.10-0.40; Observed R² = 0.063 (below expected range)
- Plan predicted Education ² = 0.20-0.25; Observed ² = -0.051 (opposite direction)
- Plan expected significance for Education; Observed p = 0.153 (non-significant)
- Sample size met expectation (N = 100 complete cases)

---

## 2. Plot Descriptions

### Plot 1: Regression Diagnostics
**File:** plots/diagnostic_plots.png

**Visual Description:**
Four-panel diagnostic plot showing model assumption checks:

- **Residuals vs Fitted (top-left):** Random scatter around y = 0 with no systematic patterns, indicating linear relationship assumption met. Red dashed horizontal line at zero for reference.
- **Normal Q-Q Plot (top-right):** Points closely follow diagonal line (red) indicating residuals are approximately normally distributed. Slight deviation at extremes but within acceptable range.
- **Scale-Location Plot (bottom-left):** Square root of standardized residuals vs fitted values shows relatively constant spread, supporting homoscedasticity assumption.
- **Cook's Distance Plot (bottom-right):** Shows influential points with red threshold line at 0.04. Eight observations exceed threshold but values remain modest (<0.08).

**Connection to findings:** Visual diagnostics support statistical tests (Shapiro-Wilk p = 0.264, Breusch-Pagan p = 0.716), confirming regression assumptions met.

### Plot 2: Effect Sizes
**File:** plots/effect_sizes.png

**Visual Description:**
Bar chart displaying model-level effect sizes with 95% bootstrap confidence intervals:

- **R² Full Model:** 0.063 with wide CI [0.017, 0.218], labeled "Small" effect
- **Cohen's f²:** 0.027 with CI extending to ~0.28, classified as "Small" effect  
- **f² Change:** 0.027 (identical to overall f²), indicating minimal improvement over control model

Error bars show substantial uncertainty in effect size estimates. All effect sizes fall in "Small" category per Cohen's conventions.

**Connection to findings:** Visual confirms small, uncertain effects consistent with non-significant overall model (p = 0.184).

### Plot 3: Predictor Relative Importance
**File:** plots/predictor_importance.png

**Visual Description:**
Bar chart showing semi-partial correlations (unique variance explained) by predictor:

- **Typical Sleep:** 9.5% of model R² (highest contributor)
- **Education:** 3.9% of model R² (second highest)
- **VR Experience:** 3.3% of model R² (lowest contributor)

Despite Typical Sleep being most important predictor, all contributions are small (< 10% of total variance explained).

**Connection to findings:** Reinforces that all predictors contribute minimal unique variance, consistent with non-significant individual effects.

### Plot 4: Cross-Validation Performance
**File:** plots/cv_performance.png

**Visual Description:**
Two-panel plot showing 5-fold cross-validation results:

- **Test R² (left panel):** Four of five folds show negative R² values (range: -0.42 to +0.14), with mean = -0.134. Red dashed line shows poor average performance.
- **RMSE (right panel):** Root Mean Square Error ranges from 0.58 to 0.82 across folds, with mean = 0.685. Relatively consistent prediction error magnitude.

**Connection to findings:** Negative test R² indicates severe overfitting - model performs worse than baseline (intercept-only) on held-out data. Suggests results not generalizable.

---

## 3. Interpretation

### Hypothesis Testing

**Primary Hypothesis:** "Education level will significantly predict REMEMVR performance, with higher education associated with better episodic memory scores."

**Hypothesis Status:** **REJECTED**

The statistical findings contradict the primary hypothesis:
- Education coefficient is negative (² = -0.051) rather than positive
- Effect is non-significant (p = 0.153, p_Bonferroni = 0.460)
- Confidence interval includes zero [-0.122, 0.019]

**Secondary Hypotheses:**
- Sleep positive but weak association: **SUPPORTED** direction (² = 0.080) but non-significant
- VR experience positive association: **SUPPORTED** direction (² = 0.047) but non-significant  
- Age negative association: **SUPPORTED** direction (² = -0.051) but non-significant

### Theoretical Contextualization

**Cognitive Reserve Theory Contradiction:**

The negative education coefficient contradicts cognitive reserve theory (Stern, 2002), which predicts positive associations between education and memory performance. Possible explanations:

1. **Restricted Range Effect:** College undergraduate sample (all current students) shows minimal education variation, potentially masking true effects
2. **Alternative Cognitive Demands:** REMEMVR's novelty may disadvantage higher-educated participants who rely on familiar strategies
3. **Confounding Variables:** Unmeasured factors (motivation, test anxiety) may correlate with education in unexpected directions

**Sleep Consolidation Patterns:**

Typical Sleep showed expected positive direction (² = 0.080) consistent with consolidation theory (Walker, 2008; Diekelmann & Born, 2010), but effect was non-significant. In healthy young adult samples, sleep effects may be attenuated due to:
- Adequate baseline sleep in college population
- Individual differences masked by self-report measurement error
- Laboratory setting reducing ecological validity of sleep-memory relationship

**VR Experience Findings:**

Positive VR experience coefficient (² = 0.047) aligns with familiarity reducing cognitive load, but minimal effect size suggests:
- Desktop VR paradigm may not fully engage immersive experience benefits
- Self-reported experience may not capture relevant skill differences
- Interface effects minimal compared to individual memory ability differences

### Unexpected Patterns

**Overall Model Non-Significance:**

The hierarchical regression failed to reach significance (F = 1.59, p = 0.184), indicating self-report predictors collectively explain minimal REMEMVR variance. This challenges the ecological validity assumption that lifestyle factors substantially influence VR memory assessment.

**Cross-Validation Failure:**

Negative test R² across 4/5 folds reveals severe overfitting, suggesting:
- Model learns noise rather than generalizable patterns
- Sample size (N = 100) insufficient for stable four-predictor model
- Individual differences in REMEMVR performance primarily driven by factors not captured in self-report measures

**Education Direction Reversal:**

The unexpected negative education coefficient warrants investigation:
- Restricted range in college sample may create spurious negative correlation
- High-education participants may overthink simple memory tasks
- Educational background may not translate to spatial-temporal VR memory skills

### Broader Implications

**REMEMVR Assessment Validity:**

Findings suggest REMEMVR performance is relatively independent of common lifestyle self-report measures:
- May indicate task taps domain-specific VR memory abilities distinct from general cognitive reserve
- Supports discriminant validity: REMEMVR not simply proxy for education/lifestyle factors
- Questions ecological validity: real-world memory may be more lifestyle-dependent

**Methodological Insights:**

1. **Self-Report Limitations:** Lifestyle measures may lack precision for predicting complex memory tasks
2. **Sample Homogeneity:** Undergraduate samples may restrict variance in key predictors
3. **Effect Size Reality:** Individual differences research often yields small, unstable effects requiring large samples
4. **Cross-Validation Necessity:** Model fit statistics can be misleading without generalizability testing

**Clinical Assessment Implications:**

For VR-based cognitive assessment applications:
- REMEMVR performance appears relatively unbiased by educational background (positive for fairness)
- Sleep and lifestyle factors minimally predictive (focus on task-specific abilities)
- Individual differences remain substantial but unexplained by common self-report measures

---

## 4. Limitations

### Sample Limitations

**Sample Size and Power:**
- N = 100 provides adequate power (0.80) only for large effects (f² > 0.35)
- Observed effects underpowered: Overall model power = 0.496, individual predictors = 0.044-0.161
- Post-hoc sensitivity analysis indicates minimum detectable f² = 0.28-0.33 (medium effects only)
- Small effects (f² < 0.15) undetectable with current sample size

**Demographic Constraints:**
- Restricted to undergraduate students (age, education, SES homogeneity)
- Self-selected VR study participants may not represent broader population
- Limited variance in key predictors (education years especially constrained in college sample)
- Generalizability to older adults, clinical populations, or broader educational ranges uncertain

**Attrition and Missing Data:**
- Complete cases analysis (N = 100) assumes MCAR (missing completely at random)
- Dependency on Ch5 5.1.1 completion introduces potential systematic missingness
- Self-report measures subject to social desirability bias and measurement error

### Methodological Limitations

**Measurement Issues:**

1. **Self-Report Validity:**
   - Education measured in years may not capture quality or relevance of educational experience
   - Typical Sleep self-report known to correlate poorly with objective measures (actigraphy)
   - VR Experience ordinal scale lacks validation and may not capture relevant skill dimensions

2. **Outcome Variable:**
   - Uses aggregated theta_all scores (loses domain-specific information)
   - IRT-derived theta scores may not optimally represent individual differences for regression
   - Single time point measurement (no test-retest reliability assessment)

**Design Limitations:**

1. **Cross-Sectional Design:**
   - Cannot infer causality from correlational predictors
   - Temporal relationships between lifestyle factors and memory unclear
   - No control for unmeasured confounders (genetics, motivation, health status)

2. **Variable Selection:**
   - Limited to available self-report measures (may miss important predictors)
   - No objective measures (sleep actigraphy, cognitive tests, brain imaging)
   - Predictor selection not theoretically exhaustive (personality, health, socioeconomic factors omitted)

**Statistical Limitations:**

1. **Model Specification:**
   - Assumes linear relationships (non-linear patterns unexplored)
   - No interaction terms tested (Education × Sleep, Age × VR Experience)
   - Fixed effects only (no random effects for potential clustering)

2. **Multiple Comparisons:**
   - Bonferroni correction conservative (may miss true effects with p = 0.01-0.05)
   - Family-wise error rate controlled but Type II error rate high with small effects
   - No pre-registered analysis plan (exploratory analyses risk Type I error inflation)

### Generalizability Constraints

**Population Generalizability:**
- Findings may not extend to:
  - Older adults (different education-memory relationships, cohort effects)
  - Clinical populations (memory impairments, medication effects)
  - Non-college populations (broader education range, different lifestyle patterns)
  - Non-WEIRD samples (cultural differences in VR acceptance, memory strategies)

**Context Generalizability:**
- Desktop VR differs from immersive HMD environments
- Laboratory testing may not reflect real-world VR memory use
- Single-session assessment may not capture individual difference stability
- Self-report timing (post-VR) may be influenced by task experience

**Task Generalizability:**
- REMEMVR-specific findings may not apply to:
  - Traditional neuropsychological memory tests
  - Real-world episodic memory tasks
  - Other VR memory paradigms (gaming, training, therapy)

### Technical Limitations

**Cross-Validation Overfitting:**
- Negative test R² indicates model learns sample-specific noise
- Bootstrap CIs based on same sample (may underestimate uncertainty)
- 5-fold CV with small sample creates unstable fold estimates
- Model complexity (4 predictors) may exceed optimal ratio for N = 100

**Effect Size Measurement:**
- Cohen's f² classification system may not apply to VR memory individual differences
- Bootstrap CIs wide and asymmetric (effect size estimates uncertain)
- Semi-partial correlations sensitive to suppressor effects and multicollinearity

**Dependency Management:**
- Analysis requires Ch5 5.1.1 completion (creates sequential dependencies)
- Theta score aggregation across domains may mask important domain-specific predictive patterns
- File path dependencies fragile (multiple fallback patterns needed)

### Confidence Rating Response Patterns
Self-report measures included Likert-scale confidence ratings. Inspection of response patterns shows approximately 15% of participants used only extreme values (1s and 5s), while 85% used the full 1-5 range. No bias correction was applied per transparency priority. This pattern may limit interpretability of relationships between self-reported confidence and actual memory performance, but was deemed acceptable for the current analysis scope.

### Limitations Summary

Despite these constraints, findings provide valuable **negative evidence** within scope:
- Self-report lifestyle factors do not substantially predict REMEMVR performance in college samples
- Results highlight measurement challenges in individual differences research
- Cross-validation failure emphasizes need for replication with larger, more diverse samples

Limitations point toward clear **methodological improvements** for future research (see Section 5: Next Steps).

---

## 5. Next Steps

### Immediate Follow-Ups (Current Data)

**1. Outlier Sensitivity Analysis:**
- **Why:** 8 outliers detected (Cook's D > 0.04) may influence small effect detection
- **How:** Re-run hierarchical regression excluding outliers, compare effect sizes and significance
- **Expected Insight:** Determine whether null results robust to influential cases or driven by outliers
- **Timeline:** Immediate (data available, subset analysis straightforward)

**2. Alternative Education Metrics:**
- **Why:** Years of education may not capture cognitive reserve adequately in college sample
- **How:** Explore GPA, field of study, or composite education quality measures if available in master.xlsx
- **Expected Insight:** Test whether education quality vs quantity better predicts VR memory
- **Timeline:** Immediate if additional variables available, otherwise requires new data collection

**3. Non-Linear Relationship Exploration:**
- **Why:** Linear models may miss threshold effects or inverted-U patterns (e.g., optimal sleep duration)
- **How:** Add quadratic terms for Sleep and Age, test polynomial regression models
- **Expected Insight:** Identify potential non-monotonic relationships masked by linear assumptions
- **Timeline:** ~1 day (requires model respecification and validation)

### Planned Thesis RQs (Chapter 7 Continuation)

**RQ 7.5.2: Objective vs Self-Report Predictors:**
- **Focus:** Compare self-report measures with objective assessments (if available)
- **Why:** Current RQ limited by self-report measurement error and bias
- **Builds On:** Uses same theta_all outcomes, tests objective sleep tracking, cognitive assessments
- **Expected Timeline:** Dependent on objective measure availability

**RQ 7.5.3: Domain-Specific Predictor Patterns:**
- **Focus:** Test whether lifestyle factors differentially predict What/Where/When domains
- **Why:** Aggregated theta_all may mask domain-specific individual difference patterns
- **Builds On:** Uses domain-specific theta scores from Ch5, same self-report predictors
- **Expected Timeline:** Planned sequence after current null results interpretation

**RQ 7.5.4: Predictor × Memory Domain Interactions:**
- **Focus:** Test Education × Domain and Sleep × Domain interactions in longitudinal context
- **Why:** Lifestyle factors may influence forgetting trajectories differently across memory types
- **Builds On:** Requires both RQ 7.5.1 and domain-specific trajectory analyses
- **Expected Timeline:** Later in Ch7 sequence (requires trajectory modeling completion)

### Methodological Extensions (Future Data Collection)

**1. Larger Sample Size:**
- **Current Limitation:** N = 100 underpowered for small effects (f² < 0.15)
- **Extension:** Target N = 400-500 for 80% power to detect small effects (f² = 0.02-0.05)
- **Expected Insight:** Determine whether null results reflect true lack of association vs insufficient power
- **Feasibility:** Requires new data collection (~6-12 months)

**2. Objective Lifestyle Measures:**
- **Current Limitation:** Self-report sleep, education, VR experience subject to bias and error
- **Extension:** Actigraphy sleep monitoring, cognitive ability testing, objective VR skill assessments
- **Expected Insight:** Test whether measurement error explains null self-report findings
- **Feasibility:** Moderate (requires equipment and participant compliance, ~3-6 months)

**3. Broader Demographic Range:**
- **Current Limitation:** College undergraduate sample restricts education and age variance
- **Extension:** Community sample spanning education levels (high school to graduate) and ages (18-65)
- **Expected Insight:** Test cognitive reserve predictions in populations with greater variance
- **Feasibility:** High effort (requires community recruitment and diverse testing sites, ~12 months)

**4. Longitudinal Individual Differences Design:**
- **Current Limitation:** Cross-sectional snapshot may miss lifestyle-memory development
- **Extension:** Track participants across 6-12 months, monitor lifestyle changes and memory performance
- **Expected Insight:** Establish temporal precedence and causal directions for lifestyle factors
- **Feasibility:** Long-term commitment (requires retention strategies and repeated testing, ~18 months)

### Theoretical Questions Raised

**1. VR Memory Individual Differences Architecture:**
- **Question:** What cognitive and demographic factors DO predict VR episodic memory if lifestyle factors don't?
- **Next Steps:** Expanded assessment battery including working memory, spatial ability, gaming experience, personality factors
- **Expected Insight:** Build comprehensive individual differences model for VR memory assessment
- **Feasibility:** Moderate (requires test battery development and validation, ~6 months)

**2. Ecological Validity of VR Memory Assessment:**
- **Question:** Do real-world lifestyle factors predict real-world memory better than VR memory?
- **Next Steps:** Parallel assessment with naturalistic memory tasks (diary studies, real-world navigation)
- **Expected Insight:** Establish convergent validity between VR and ecological memory measures
- **Feasibility:** High complexity (requires naturalistic measurement protocols, ~12 months)

**3. Measurement vs Construct Validity:**
- **Question:** Are null results due to poor lifestyle measures or genuine lack of VR memory associations?
- **Next Steps:** Multi-method assessment (self-report, objective, informant ratings) for same constructs
- **Expected Insight:** Separate measurement error from true score relationships
- **Feasibility:** Moderate (requires methodological validation study, ~6 months)

### Priority Ranking

**High Priority (Do First):**
1. Outlier sensitivity analysis - immediate, tests robustness of null findings
2. RQ 7.5.3 domain-specific patterns - natural next step, may reveal masked effects
3. Non-linear relationship exploration - addresses alternative model specifications

**Medium Priority (Subsequent):**
1. RQ 7.5.2 objective measures - conditional on data availability
2. Alternative education metrics - if available in current dataset
3. Larger sample replication - important but resource-intensive

**Lower Priority (Aspirational):**
1. Longitudinal individual differences - long-term research program
2. Broader demographic sampling - substantial resource requirements
3. VR-to-real-world validity studies - complex methodological development needed

### Next Steps Summary

The null findings in RQ 7.5.1 raise important questions about **individual differences in VR memory assessment**:

1. **Immediate priorities:** Test robustness through outlier analysis and domain-specific examination
2. **Short-term extensions:** Explore non-linear patterns and alternative predictor measures  
3. **Long-term research program:** Large-sample replication with objective measures and broader demographics

Results suggest that **common lifestyle self-report measures have minimal predictive utility** for REMEMVR performance, highlighting need for:
- More sophisticated individual differences models
- Objective measurement approaches
- Understanding of what factors DO predict VR memory ability

The negative findings provide valuable evidence that REMEMVR assessment is relatively independent of basic lifestyle factors, supporting its potential as an unbiased cognitive assessment tool.

---

**Summary generated by:** rq_results agent (v4.0)
**Pipeline version:** v4.X (13-agent atomic architecture)
**Date:** 2026-01-06T12:48:00Z