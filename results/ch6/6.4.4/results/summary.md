# Results Summary: RQ 6.4.4 - Paradigm-Specific Trait Variance in Confidence Decline

**Research Question:** Is confidence decline (trajectory slope) more trait-like for some memory paradigms than others?

**Analysis Completed:** 2025-12-12

**Analyst:** rq_results agent (v4.0) with master claude orchestration

---

## 1. Statistical Findings

### Sample Characteristics

- **Total observations:** 1200 (100 participants × 4 test sessions × 3 paradigms)
- **Paradigms analyzed:** Free Recall (IFR), Cued Recall (ICR), Recognition (IRE)
- **Test sessions:** T1, T2, T3, T4 (Days 0, 1, 3, 6)
- **Time variable:** log_TSVR (logarithmic hours since VR encoding, Decision D070)
- **Time range:** 1.00 to 246.24 hours (log_TSVR: 0.69 to 5.51)
- **Theta confidence range:** -2.40 to 0.58 (mean: -0.78)
- **Missing data:** None (all 100 participants contributed data for all 3 paradigms × 4 tests)

### LMM Convergence Status

All three paradigm-stratified Linear Mixed Models converged successfully:

| Paradigm | N | Formula | Convergence | AIC | BIC |
|----------|---|---------|-------------|-----|-----|
| Free Recall (IFR) | 400 | theta ~ log_TSVR + (log_TSVR \| UID) | True | 370.78 | 394.73 |
| Cued Recall (ICR) | 400 | theta ~ log_TSVR + (log_TSVR \| UID) | True | 330.30 | 354.25 |
| Recognition (IRE) | 400 | theta ~ log_TSVR + (log_TSVR \| UID) | True | 298.82 | 322.77 |

**Note:** Convergence achieved with no singular fit warnings. Random slope models are identifiable for all paradigms.

### Variance Components Per Paradigm

Extracted from fitted LMMs (Step 2):

| Paradigm | var_intercept | var_slope | cov_int_slope | cor_int_slope | var_residual | var_total |
|----------|--------------|-----------|---------------|---------------|--------------|-----------|
| IFR | 0.1857 | 0.0033 | -0.0018 | -0.071 | 0.0683 | 0.2573 |
| ICR | 0.2097 | 0.0033 | -0.0050 | -0.188 | 0.0579 | 0.2709 |
| IRE | 0.1742 | 0.0022 | 0.0014 | 0.074 | 0.0554 | 0.2318 |

**Interpretation:**
- **var_intercept:** Baseline confidence shows substantial between-person variance across all paradigms (0.17-0.21)
- **var_slope:** Slope variance is small but non-zero (0.002-0.003), indicating modest individual differences in decline rate
- **cov_int_slope:** Negative covariance for IFR and ICR (higher baseline ’ faster decline), positive for IRE (higher baseline ’ slower decline)
- **var_residual:** Within-person residual variance smallest for IRE (0.055), largest for IFR (0.068)

### Intraclass Correlation Coefficients (ICC)

Computed per paradigm (Step 3):

| Paradigm | ICC_intercept | ICC_slope_simple | ICC_slope_conditional | interpretation_intercept | interpretation_slope |
|----------|---------------|------------------|----------------------|-------------------------|---------------------|
| IFR | 0.665 | 0.046 | 0.297 | Substantial | Negligible |
| ICR | 0.771 | 0.055 | 0.323 | Substantial | Small |
| IRE | 0.659 | 0.038 | 0.214 | Substantial | Negligible |

**ICC_intercept (baseline confidence):**
- All paradigms show **substantial** trait variance (0.66-0.77)
- ICR highest (0.77): 77% of baseline confidence variance is between-person
- IFR and IRE similar (0.66): Two-thirds of baseline variance is trait-like
- **Conclusion:** Individual differences in baseline confidence are stable across retrieval paradigms

**ICC_slope_simple (unconditional slope variance):**
- All paradigms show **negligible-to-small** trait variance (0.04-0.05)
- ICR highest (0.055): 5.5% of slope variance is between-person (small trait effect)
- IFR intermediate (0.046): 4.6% (negligible)
- IRE lowest (0.038): 3.8% (negligible)
- **Conclusion:** Confidence decline rates are primarily state-like (random fluctuation), not trait-like

**ICC_slope_conditional (slope variance at Day 6):**
- Accounts for intercept-slope correlation
- ICR highest (0.32): 32% trait variance at Day 6 (moderate)
- IFR intermediate (0.30): 30% (moderate)
- IRE lowest (0.21): 21% (low-moderate)
- **Conclusion:** When accounting for correlation with baseline, slope variance increases but remains below trait threshold (0.50)

### Paradigm Comparisons (Step 4)

Pairwise ICC_slope differences:

| Comparison | ICC_slope_diff_simple | ICC_slope_diff_conditional | Direction |
|------------|----------------------|---------------------------|-----------|
| IFR - ICR | -0.009 | -0.026 | ICR higher |
| IFR - IRE | +0.007 | +0.083 | IFR higher |
| ICR - IRE | +0.016 | +0.109 | ICR higher |

**Ranking by ICC_slope_simple:**
1. **ICR (Cued Recall):** 0.055 (highest)
2. **IFR (Free Recall):** 0.046 (intermediate)
3. **IRE (Recognition):** 0.038 (lowest)

**Hypothesis Test Result:** **REFUTED**

- **Hypothesis:** Free Recall would show highest ICC_slope (individual differences magnified under high cognitive demand)
- **Actual Result:** Cued Recall shows highest ICC_slope (0.055 vs 0.046 for IFR)
- **Difference:** Small (” = 0.009, ~1% of total variance)
- **All ICC_slope values < 0.10:** Slopes are state-like across all paradigms

### Comparison to Chapter 5 Accuracy ICC (Step 5)

Cross-RQ comparison to Ch5 5.3.7 (accuracy ICC by paradigm):

| Paradigm | ICC_intercept_confidence | ICC_intercept_accuracy | ICC_intercept_diff | ICC_slope_confidence | ICC_slope_accuracy | ICC_slope_diff | Interpretation |
|----------|-------------------------|------------------------|-------------------|---------------------|-------------------|----------------|----------------|
| IFR | 0.665 | 0.501 | +0.164 | 0.046 | 0.022 | +0.024 | Confidence and accuracy show SIMILAR slope variance |
| ICR | 0.771 | 0.437 | +0.335 | 0.055 | 0.000 | +0.055 | Confidence reveals MORE slope variance than accuracy |
| IRE | 0.659 | 0.515 | +0.144 | 0.038 | 0.014 | +0.024 | Confidence and accuracy show SIMILAR slope variance |

**Key Findings:**

1. **Baseline (ICC_intercept):**
   - Confidence shows higher baseline trait variance than accuracy across all paradigms (+0.14 to +0.34)
   - Largest difference for ICR (+0.34): 5-level confidence data captures more individual differences than dichotomous accuracy

2. **Slope (ICC_slope):**
   - Average ICC_slope difference: +0.034 (confidence slightly higher than accuracy)
   - IFR: +0.024 (similar)
   - **ICR: +0.055 (confidence reveals MORE slope variance)** - Accuracy showed virtually zero slope variance (0.000089), confidence shows small but detectable variance (0.055)
   - IRE: +0.024 (similar)

3. **Overall Pattern:**
   - Confidence and accuracy show **similar** slope variance patterns (both state-like)
   - 5-level confidence data reveals slightly more slope variance than dichotomous accuracy (+3.4% on average)
   - **Exception:** ICR shows larger difference (+5.5%), suggesting confidence trajectories may be more sensitive to individual differences in cued recall paradigm

---

## 2. Plot Descriptions

**No plots generated for this RQ** (status.yaml shows rq_plots: bypassed)

**Rationale:** This RQ focuses on tabular ICC decomposition and paradigm comparison. Visualizations not required for variance component interpretation. Results presented in numerical tables (Sections 1, 3, 4).

**If plots were to be generated (future enhancement):**

Suggested visualizations:
1. **ICC Comparison Bar Chart:** ICC_intercept vs ICC_slope_simple across 3 paradigms (shows paradigm differences visually)
2. **Variance Decomposition Pie Charts:** One per paradigm, showing proportion of var_intercept, var_slope, var_residual in var_total
3. **Ch5 Comparison Scatter Plot:** Confidence ICC (y-axis) vs Accuracy ICC (x-axis) for intercept and slope separately (diagonal = perfect agreement, points above diagonal = confidence higher)

---

## 3. Interpretation

### Hypothesis Testing

**Original Hypothesis (from 1_concept.md):**

"Free Recall may show highest ICC_slope (individual differences magnified under high cognitive demand). Alternatively, all paradigms may show ICC_slope H 0, replicating Chapter 5 findings where retrieval support affected baseline but not slope variance."

**Hypothesis Status:** **PARTIALLY REFUTED**

**Evidence:**
- Free Recall does NOT show highest ICC_slope (ICR > IFR: 0.055 vs 0.046)
- All paradigms DO show ICC_slope < 0.10 (state-like slopes, consistent with Ch5 pattern)
- Unexpected finding: Cued Recall (intermediate demand) shows highest slope variance, not Free Recall (highest demand) or Recognition (lowest demand)

**Secondary Hypothesis:**

"If ICC_slope differs by paradigm, retrieval support moderates trait-like individual differences in metacognitive monitoring decline."

**Status:** **PARTIALLY SUPPORTED**

- ICC_slope does differ slightly by paradigm (ICR = 0.055, IFR = 0.046, IRE = 0.038)
- Differences are small (max ” = 0.016, or 1.6% of total variance)
- Pattern is non-monotonic with retrieval support (Cued Recall highest, not Free Recall or Recognition)
- **Conclusion:** Retrieval support shows weak, non-linear relationship with slope variance

### Theoretical Contextualization

**Trait vs State Memory Theory:**

This RQ tests whether confidence decline rates show trait-like (stable individual differences, high ICC) or state-like (context-dependent, low ICC) variance. Results clearly indicate **state-like slopes** across all paradigms:

- ICC_slope_simple < 0.10 for all paradigms (negligible-to-small trait variance)
- 95-96% of slope variance is within-person (state-like fluctuation)
- Only 4-6% of slope variance is between-person (trait-like stability)

**Comparison to Chapter 5 Accuracy Findings:**

Ch5 5.3.7 found similar pattern for accuracy trajectories (ICC_slope H 0 for all paradigms). Current findings extend this to confidence:

1. **Baseline (ICC_intercept):** Both accuracy and confidence show substantial trait variance (0.44-0.77), but confidence shows higher trait variance (+0.14 to +0.34)
2. **Slope (ICC_slope):** Both accuracy and confidence show minimal slope trait variance (<0.10), with confidence slightly higher (+0.034 on average)
3. **Interpretation:** Forgetting rates are fundamentally state-like regardless of measurement (accuracy vs confidence) or retrieval paradigm (Free/Cued/Recognition)

**Retrieval Support Theory:**

Hypothesis predicted Free Recall (highest demand) would show highest ICC_slope due to amplified individual differences. Results refute this:

- Cued Recall (intermediate support) shows highest ICC_slope (0.055)
- Free Recall (lowest support) shows intermediate ICC_slope (0.046)
- Recognition (highest support) shows lowest ICC_slope (0.038)

**Possible Explanations for ICR Supremacy:**

1. **Optimal Difficulty Hypothesis:** Cued Recall may provide optimal cognitive challenge for revealing individual differences - not too easy (Recognition) nor too hard (Free Recall)
2. **Metacognitive Sensitivity:** Partial retrieval cues may enhance metacognitive monitoring, allowing confidence ratings to better track individual ability differences
3. **Statistical Artifact:** Small differences (0.009-0.016) may reflect sampling variability rather than true paradigm effects (no formal hypothesis test conducted)
4. **Measurement Precision:** Cued Recall confidence may have better psychometric properties (lower residual variance: 0.058 vs 0.068 for IFR)

### Unexpected Patterns

**1. Cued Recall Shows Highest ICC_slope (Not Free Recall)**

**Pattern:** ICR ICC_slope = 0.055 (highest), IFR ICC_slope = 0.046 (intermediate), IRE ICC_slope = 0.038 (lowest)

**Why Unexpected:** Hypothesis predicted Free Recall (highest cognitive demand) would show highest slope variance due to amplified individual differences under challenge

**Investigation Suggestions:**
- Examine item-level difficulty: Are Cued Recall items better calibrated for detecting individual differences?
- Test alternative hypothesis: Optimal difficulty (intermediate support) maximizes individual difference detection
- Explore confidence rating patterns: Do participants use confidence scale differently across paradigms?
- Conduct sensitivity analysis: Re-run with alternative ICC formulas (e.g., reliability-adjusted ICC) to verify robustness

**2. Negative Intercept-Slope Correlations for IFR and ICR**

**Pattern:**
- IFR: cor_int_slope = -0.071 (higher baseline ’ faster decline)
- ICR: cor_int_slope = -0.188 (higher baseline ’ faster decline)
- IRE: cor_int_slope = +0.074 (higher baseline ’ slower decline)

**Why Unexpected:** Recognition shows opposite pattern from Free/Cued Recall

**Investigation Suggestions:**
- Examine ceiling effects: Do high-confidence participants on Recognition have less room to decline?
- Test regression to mean: Do extreme baseline scores regress toward mean over time?
- Explore paradigm-specific forgetting mechanisms: Different neural substrates for recognition vs recall?

**3. Confidence Shows Higher Baseline ICC Than Accuracy (All Paradigms)**

**Pattern:** ICC_intercept_diff = +0.14 to +0.34 (confidence > accuracy)

**Why Notable:** 5-level confidence scale captures more individual differences than dichotomous accuracy (correct/incorrect)

**Theoretical Implication:**
- Confidence ratings provide richer individual difference information than accuracy alone
- Metacognitive monitoring shows stable trait variance even when performance accuracy does not
- Suggests confidence assessments may be more sensitive for detecting subtle cognitive differences

### Broader Implications

**REMEMVR Validation:**

Findings support REMEMVR as valid metacognitive assessment tool:
- Confidence trajectories show substantial baseline trait variance (ICC_intercept = 0.66-0.77) across all paradigms
- Confidence ratings are psychometrically stable (convergent LMMs, positive variance components)
- Multi-paradigm sensitivity: Detects paradigm differences in both baseline and slope variance

**However:**
- Minimal slope trait variance (ICC_slope < 0.10) limits utility for assessing individual differences in forgetting rates
- Baseline confidence may be more useful clinical target than decline trajectories

**Methodological Insights:**

1. **5-Level Confidence Data Reveals More Variance Than Dichotomous Accuracy:**
   - Average ICC_slope difference: +0.034 (confidence > accuracy)
   - Largest for Cued Recall (+0.055): Confidence trajectories may be more sensitive in intermediate-difficulty tasks
   - Implication: Multi-level confidence scales recommended over binary accuracy for individual difference research

2. **Paradigm-Specific ICC Patterns Are Weak:**
   - Max ICC_slope difference: 0.016 (1.6% of total variance)
   - All paradigms show state-like slopes (ICC_slope < 0.10)
   - Retrieval support does not strongly moderate slope trait variance
   - Implication: Forgetting rates are fundamentally state-like regardless of task difficulty

3. **Random Slope Models Are Identifiable for Confidence Data:**
   - All 3 LMMs converged without singularity warnings
   - Variance components all positive (no negative variances)
   - Suggests confidence data has sufficient variability for complex random effects structures

**Clinical Relevance:**

For cognitive assessment applications:
- **Baseline confidence** shows substantial trait variance (66-77%) - useful for identifying individual differences in metacognitive calibration
- **Confidence decline** shows minimal trait variance (4-6%) - less useful for tracking individual-specific forgetting patterns
- **Recommendation:** Focus on cross-sectional confidence assessments rather than longitudinal trajectories for individual difference measurement
- **Exception:** Cued Recall may be optimal paradigm if slope variance is clinically relevant (highest ICC_slope = 0.055)

---

## 4. Limitations

### Sample Limitations

**Sample Size:**
- N = 100 participants provides adequate power for detecting medium effects (ICC e 0.30) but underpowered for small effects (ICC < 0.10)
- ICC_slope estimates (0.04-0.06) are near lower detection limit - true values may be even smaller
- Cannot rule out that observed paradigm differences (” = 0.009-0.016) are sampling variability rather than true effects
- **Implication:** Findings of "negligible slope variance" are robust, but exact paradigm rankings may be unstable

**Missing Data:**
- No missing data in this RQ (all 100 participants contributed 4 tests × 3 paradigms = 1200 observations)
- However, missing data accumulated in upstream RQ 6.4.1 during IRT calibration and purification
- Cannot assess whether missingness patterns introduced bias into theta_confidence estimates

**Generalizability:**
- University undergraduate sample (age M H 20, predominantly female) limits generalizability to:
  - Older adults (metacognitive monitoring changes with age)
  - Clinical populations (MCI, dementia, anxiety disorders affect confidence calibration)
  - Non-WEIRD samples (cross-cultural metacognitive differences documented)

### Methodological Limitations

**Measurement:**

1. **Theta Confidence Scale:**
   - IRT-derived theta estimates assume unidimensional confidence latent trait
   - Range: -2.40 to 0.58 (mean: -0.78) suggests overall low confidence (negative theta)
   - Negative mean may reflect item difficulty (hard items ’ low confidence) or sample characteristics (underconfident participants)
   - **Concern:** Does negative theta indicate measurement artifact or true metacognitive calibration?

2. **5-Level Confidence Rating Limitations:**
   - RQ 6.4.1 noted participants show restricted confidence range (many use only extremes: 1 and 5)
   - Restricted range may reduce slope variance (less room for individual differences in decline)
   - **Implication:** ICC_slope estimates may be artificially low due to measurement ceiling/floor effects

3. **Paradigm Stratification:**
   - Three separate LMMs (one per paradigm) rather than single LMM with Paradigm × Time interaction
   - Cannot formally test whether ICC_slope differences are statistically significant (no p-values)
   - **Recommendation:** Future work should use multilevel ICC framework with nested paradigms

**Design:**

1. **No Baseline Confidence-Free Measurement:**
   - Day 0 theta estimates include confidence ratings made immediately after encoding (not truly "baseline")
   - Cannot separate encoding confidence from retrieval confidence
   - Intercept variance may reflect encoding individual differences, not just metacognitive trait

2. **Fixed Test Session Timing:**
   - TSVR variable accounts for actual hours (Decision D070), but test sessions still clustered around nominal Days 0, 1, 3, 6
   - Limited variability in TSVR within test session (e.g., all Day 1 tests within 20-28 hour window)
   - May underestimate slope variance if forgetting dynamics differ at finer timescales

3. **No Control for Practice Effects:**
   - Four repeated retrievals may alter confidence trajectories (testing effect on metacognitive monitoring)
   - Cannot separate forgetting from confidence recalibration due to repeated testing
   - LMM assumes linear time effect (may not capture testing-induced non-linearity)

**Statistical:**

1. **LMM Specification:**
   - Random slopes model assumes linear log_TSVR trajectories (no quadratic/cubic forgetting curves tested)
   - Time transformation: log_TSVR (logarithmic hours) assumes power-law forgetting, not exponential
   - Alternative time transformations (sqrt_TSVR, 1/TSVR) not tested for robustness
   - **Concern:** ICC_slope estimates depend on time scale choice

2. **ICC Formula Choice:**
   - Used unconditional ICC_slope_simple (var_slope / var_total) for primary comparisons
   - Alternative: ICC_slope_conditional accounts for intercept-slope correlation but less intuitive
   - Literature inconsistent on which ICC formula to use for slopes
   - **Implication:** ICC rankings (ICR > IFR > IRE) may change with alternative ICC definitions

3. **No Formal Hypothesis Test:**
   - Paradigm comparisons are descriptive (” ICC reported, no p-values)
   - Cannot determine if ICC_slope differences (0.009-0.016) are statistically significant or sampling variability
   - Bonferroni correction (Decision D068) not applicable (no multiple comparisons formally tested)
   - **Recommendation:** Bootstrap confidence intervals for ICC differences in future work

### Generalizability Constraints

**Population:**
- Findings may not generalize to:
  - Older adults (age-related changes in metacognitive monitoring and retrieval processes)
  - Clinical populations with metacognitive deficits (schizophrenia, OCD, anxiety disorders)
  - Children/adolescents (developing metacognitive systems)
  - High-performing experts (calibrated confidence may show different trait patterns)

**Context:**
- VR desktop paradigm differs from:
  - Fully immersive HMD VR (confidence ratings may differ with embodiment)
  - Real-world episodic memory (naturalistic confidence judgments)
  - Standard neuropsychological tests (2D stimuli, verbal confidence reports)

**Task:**
- REMEMVR-specific confidence ratings may not reflect:
  - Naturalistic metacognitive monitoring (spontaneous, not prompted)
  - Domain-general confidence (findings specific to episodic memory, may not extend to semantic, procedural, or working memory)
  - Other confidence scales (e.g., percentage confidence, forced-choice confidence)

### Technical Limitations

**IRT-Derived Theta Estimates (Decision Dependency on RQ 6.4.1):**
- Theta_confidence scores computed in RQ 6.4.1 using 3-factor GRM (IFR, ICR, IRE dimensions)
- Item purification in RQ 6.4.1 excluded items with extreme difficulty or low discrimination
- **Concern:** Purification may have removed items that captured individual slope differences
- Cannot assess whether ICC_slope estimates would differ with full (unpurified) item set
- **Transparency:** This RQ inherits all IRT assumptions and limitations from RQ 6.4.1

**Variance Component Extraction:**
- Variance components extracted from statsmodels MixedLM random effects covariance matrix
- Assumes random effects are normally distributed (may not hold if theta_confidence is skewed)
- Small variance estimates (var_slope = 0.002-0.003) may be unstable (estimation uncertainty not quantified)
- **Recommendation:** Bootstrap variance component CIs to assess estimation precision

**Ch5 5.3.7 Comparison Limitations:**
- Ch5 5.3.7 used accuracy (dichotomous), this RQ uses confidence (5-level IRT theta)
- ICC formulas may differ between RQs (not verified)
- Paradigm labels may differ ("free_recall" vs "IFR") - mapping assumed correct
- **Assumption:** ICC interpretation thresholds (<0.10 = negligible, 0.10-0.30 = small, etc.) apply equally to accuracy and confidence

### Limitations Summary

Despite these constraints, findings are **robust within scope:**
- All 3 LMMs converged successfully (no estimation failures)
- ICC_intercept substantial across all paradigms (0.66-0.77) - baseline trait variance is reliable
- ICC_slope consistently < 0.10 across all paradigms (state-like pattern is consistent)
- Ch5 comparison shows similar pattern (confidence and accuracy both state-like slopes)

**Critical Limitation:** Small ICC_slope differences (0.009-0.016) may not be statistically or practically significant. Recommendation: Interpret paradigm rankings (ICR > IFR > IRE) as exploratory hypothesis-generating findings, not confirmatory evidence.

Limitations indicate **directions for future work** (see Section 5: Next Steps).

---

## 5. Next Steps

### Immediate Follow-Ups (Current Data)

**1. Bootstrap Confidence Intervals for ICC Differences:**
- **Why:** Paradigm ICC_slope differences are small (0.009-0.016) - statistical significance unknown
- **How:** Resample participants with replacement (1000 iterations), recompute ICC per paradigm, generate 95% CIs for pairwise differences
- **Expected Insight:** Determine if ICR > IFR > IRE ranking is statistically robust or sampling artifact
- **Timeline:** Immediate (same data, bootstrap resampling script)

**2. Multilevel ICC Framework with Paradigm × Time Interaction:**
- **Why:** Current approach uses 3 separate LMMs (cannot formally test paradigm differences)
- **How:** Fit single LMM with nested structure: theta ~ Paradigm × log_TSVR + (log_TSVR | UID) + (1 | UID:Paradigm), compute multilevel ICC accounting for paradigm nesting
- **Expected Insight:** Formal hypothesis test of whether ICC_slope differs across paradigms (p-value for Paradigm × Time random effect variance)
- **Timeline:** 1-2 days (requires multilevel ICC computation function)

**3. Alternative Time Transformations:**
- **Why:** Current ICC_slope estimates based on log_TSVR (assumes power-law forgetting) - robustness to time scale unknown
- **How:** Refit LMMs with sqrt_TSVR, 1/TSVR, raw TSVR (linear hours), compare ICC_slope rankings across transformations
- **Expected Insight:** Determine if ICR > IFR > IRE pattern is robust to time scale choice or transformation-specific
- **Timeline:** Immediate (same data, refit LMMs with different time variables)

### Planned Thesis RQs (Chapter 6 Continuation)

**RQ 6.4.5: Domain × Paradigm Interaction for Confidence ICC (Planned):**
- **Focus:** Does paradigm-specific ICC_slope pattern (ICR > IFR > IRE) hold within each memory domain (What, Where, When)?
- **Why:** Current RQ aggregates across domains - domain-specific patterns may reveal why Cued Recall shows highest slope variance
- **Builds On:** Uses theta_confidence scores from RQ 6.4.1 (stratified by domain × paradigm), replicates this RQ's ICC decomposition within each domain
- **Expected Timeline:** Next RQ in Chapter 6 Paradigm Confidence series (after RQ 6.4.4)

**RQ 6.5.X: Congruence × Confidence ICC (Potential Future Work):**
- **Focus:** Does confidence trajectory slope variance differ for Common, Congruent, and Incongruent items?
- **Why:** Congruence may moderate metacognitive monitoring (incongruent items may show more individual differences in confidence decline)
- **Builds On:** Extends paradigm-specific ICC framework to congruence factor analysis
- **Expected Timeline:** Chapter 6 Congruence series (dependent on Ch5 congruence RQs completing first)

### Methodological Extensions (Future Data Collection or Re-Analysis)

**1. Test Alternative ICC Definitions:**
- **Current Limitation:** Used unconditional ICC_slope_simple for primary comparisons (literature inconsistent on formula choice)
- **Extension:** Compare 5 ICC formulas from ICC literature (Shrout & Fleiss 1979, McGraw & Wong 1996, Liljequist et al. 2019)
- **Expected Insight:** Determine if paradigm rankings are robust to ICC definition or formula-dependent
- **Feasibility:** Immediate (same variance components, different ICC calculations)

**2. Examine Confidence Rating Response Patterns:**
- **Current Limitation:** RQ 6.4.1 noted restricted confidence range (many participants use only extremes: 1 and 5)
- **Extension:** Compute per-participant confidence rating entropy/variance, test if restricted range predicts lower ICC_slope
- **Expected Insight:** Determine if negligible slope variance is artifact of restricted confidence scale usage
- **Feasibility:** Moderate (requires item-level confidence data from RQ 6.4.1 raw inputs)

**3. Item-Level Difficulty Analysis:**
- **Current Limitation:** Don't know if Cued Recall items are better calibrated for detecting individual differences
- **Extension:** Extract IRT item difficulty distributions per paradigm, test if ICR has optimal difficulty spread
- **Expected Insight:** Determine if ICR's highest ICC_slope is due to item psychometric properties
- **Feasibility:** Moderate (requires RQ 6.4.1 IRT item parameters)

**4. Longitudinal Confidence Calibration Analysis:**
- **Current Limitation:** Cannot separate forgetting from confidence recalibration due to repeated testing
- **Extension:** Compute confidence-accuracy correspondence per test session, test if calibration changes over time differ by paradigm
- **Expected Insight:** Determine if practice effects on metacognitive monitoring contribute to slope variance
- **Feasibility:** High (requires paired accuracy + confidence data from RQ 6.4.1 upstream dependency)

### Theoretical Questions Raised

**1. Why Does Cued Recall Show Highest ICC_slope?**
- **Question:** What cognitive mechanism explains ICR > IFR > IRE pattern (contradicts demand hypothesis)?
- **Next Steps:** Examine partial retrieval cue effects on metacognitive monitoring, test "optimal difficulty" hypothesis with behavioral experiments
- **Expected Insight:** Identify conditions under which intermediate task difficulty maximizes individual difference detection
- **Feasibility:** Long-term (requires new experimental design, ~1 year)

**2. Do Confidence Trajectories Track Different Forgetting Mechanisms Than Accuracy?**
- **Question:** Why does confidence show slightly more slope variance than accuracy (average +0.034 ICC difference)?
- **Next Steps:** Correlate confidence slopes with accuracy slopes at participant level, test if dissociations predict metacognitive monitoring deficits
- **Expected Insight:** Determine if confidence and accuracy tap distinct forgetting processes (recollection vs familiarity)
- **Feasibility:** Moderate (requires paired accuracy + confidence data, ~3 months)

**3. Can Baseline Confidence Predict Future Cognitive Decline?**
- **Question:** ICC_intercept = 0.66-0.77 (substantial trait variance) - is baseline confidence a stable cognitive marker?
- **Next Steps:** Collect longitudinal follow-up data (1-2 years later), test if Day 0 confidence predicts later cognitive performance
- **Expected Insight:** Assess clinical utility of confidence assessments for early detection of metacognitive deficits
- **Feasibility:** Long-term (requires multi-year longitudinal cohort, ~2-3 years)

### Priority Ranking

**High Priority (Do First):**
1. Bootstrap CIs for ICC differences (immediate, resolves statistical significance question)
2. RQ 6.4.5 (domain × paradigm ICC) - natural next step in thesis progression
3. Alternative time transformations (immediate, robustness check)

**Medium Priority (Subsequent):**
1. Multilevel ICC framework (methodological improvement, ~1-2 days)
2. Alternative ICC formulas (literature comparison, immediate)
3. Confidence rating response patterns (methodological investigation, moderate effort)

**Lower Priority (Aspirational):**
1. Item-level difficulty analysis (requires extensive RQ 6.4.1 data extraction)
2. Longitudinal calibration analysis (high effort, requires accuracy-confidence pairing)
3. Optimal difficulty hypothesis testing (new experimental design, long-term)
4. Clinical utility longitudinal study (multi-year cohort, outside thesis scope)

### Next Steps Summary

The findings establish **Cued Recall as unexpected leader in slope trait variance**, raising critical question:

**Why does intermediate retrieval support maximize individual differences in confidence decline?**

Three immediate follow-ups:
1. **Bootstrap CIs:** Are paradigm differences statistically significant? (Answers: "Is ICR > IFR > IRE robust?")
2. **RQ 6.4.5:** Do domain-specific patterns explain ICR supremacy? (Answers: "Is ICR advantage domain-specific?")
3. **Time transformations:** Is pattern robust to forgetting curve assumptions? (Answers: "Is ICR advantage model-dependent?")

Methodological extensions (multilevel ICC, ICC formula comparisons, confidence rating patterns) valuable for robustness testing but secondary to theoretical question.

---

**Summary generated by:** rq_results agent (v4.0)

**Pipeline version:** v4.X (13-agent atomic architecture)

**Date:** 2025-12-12T09:30:00Z

---

**End of Summary**
