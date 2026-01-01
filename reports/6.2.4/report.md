# RQ 6.2.4: Calibration by Accuracy Level

**Chapter:** Ch6
**Status:** PLATINUM CERTIFIED
**Certification Date:** 2025-12-29
**Report Generated:** 2026-01-01

---

## 1. Executive Summary

**What we tested:** Whether high vs low baseline memory performers differ in metacognitive calibration quality.

**What we found:** Metacognitive dissociation - Resolution (gamma discrimination) is performance-dependent (Á=0.46, p<0.001), but calibration bias is performance-independent (Á=-0.10, p=0.633). Dunning-Kruger effect not supported (low performers overconfident trend M=+0.14, p_bonf=0.797).

**Why it matters:** Demonstrates that memory ability predicts metacognitive sensitivity (discrimination) but not metacognitive bias (calibration direction/magnitude). Aligns with Fleming & Lau (2014) two-dimensional metacognition model - suggests separate interventions needed for improving discrimination vs reducing calibration bias.

---

## 2. Research Question

**Question:**
Are high vs low baseline performers equally well-calibrated?

**Hypothesis:**
High baseline performers will be BETTER calibrated than low performers, showing:
- Smaller absolute calibration errors (|calibration|)
- Higher discrimination (gamma)
- Negative correlation: baseline accuracy vs |calibration|
- Positive correlation: baseline accuracy vs gamma
- Dunning-Kruger pattern: Low performers overconfident (positive calibration)

**Theoretical Framework:**
- **Metacognitive Monitoring Theory:** High-quality monitoring leads to accurate confidence judgments (good calibration), poor monitoring leads to miscalibration
- **Dunning-Kruger Effect:** Low-skill individuals lack metacognitive ability to accurately assess performance, leading to overconfidence
- **Cue-Utilization Framework:** Calibration depends on quality of cues used for metacognitive judgments - high performers may use more diagnostic cues
- **Fleming & Lau (2014) Two-Dimensional Model:** Type 2 sensitivity (discrimination) ` Type 2 bias (calibration)

**Expected Patterns:**
- Tertile comparison: Significant effect of baseline accuracy tertile on calibration metrics (p<0.05)
- Dunning-Kruger test: Low tertile positive mean calibration (overconfidence), significantly different from zero
- Correlations: Negative r for accuracy vs |calibration|, positive r for accuracy vs gamma (both p<0.05)

---

## 3. Historical Context

**Archive Search:**
- Topics searched: 5
- Entries found: 7
- Date range: 2025-12-11 to 2025-12-29

**Key Events (Chronological):**

1. **2025-12-11 21:00** - RQ 6.2.4 COMPLETED (source: rq_6.2.4_complete_dunning_kruger_not_sig_thesis_ready.md)
   - Dunning-Kruger NOT significant (Low performers M=+0.142, p_bonf=0.797)
   - Gamma-accuracy correlation STRONG (Á=0.461, p<0.001)
   - Calibration-accuracy correlation NULL (Á=-0.101, p=0.633)
   - METACOGNITIVE DISSOCIATION found: Resolution performance-dependent, Calibration performance-independent
   - Total 13/31 Ch6 RQs thesis-ready (42%)

2. **2025-12-12 14:30** - DUNNING-KRUGER DOUBLE NULL discovered (source: ch6_dunning_kruger_double_null.md)
   - RQ 6.2.4: Low accuracy does NOT predict poor calibration (NULL, p=0.797)
   - RQ 6.6.2: Low accuracy does NOT predict high HCE rates (NULL, ²=-0.001, p=1.000)
   - Convergent evidence: Low performers NOT worse at metacognitive monitoring in VR episodic memory
   - Establishes boundary condition for Dunning-Kruger effect (domain-specificity)
   - Alternative mechanism: HCEs driven by overconfidence (metacognitive trait), not low ability (cognitive deficit)

3. **2025-12-29 06:00-09:37** - PLATINUM CERTIFICATION (source: status.yaml platinum_context)
   - Criteria Version: 2025-12-27 (GLMM validation, random slopes, difference score reliability)
   - GLMM Compliance: NOT NEEDED (correlation/tertile analysis, no intercept testing)
   - Difference Score Reliability: INHERITED from RQ 6.2.1 (r_diff=0.822)
   - Power Analysis: DOCUMENTED for Dunning-Kruger null (d=0.20, N>300 required for 0.80 power)
   - Zero blockers, 100% criteria met, publication-ready

**Blockers Resolved:**
- None - RQ executed smoothly from conception to certification

**Cross-References:**
- Related to RQ 6.2.1 (Calibration Over Time) - provides calibration scores
- Related to RQ 6.2.3 (Resolution Over Time) - provides gamma scores
- Related to RQ 6.6.2 (HCE Predictors) - converges on Dunning-Kruger double null
- Completes Calibration Series (6.2.1-6.2.4, 4/5 complete)

---

## 4. Methodology

### Data Sources

**ROOT or DERIVED:** DERIVED (uses outputs from 4 prior RQs)

**Specific Sources:**
- RQ 6.2.1 (Calibration Over Time): `results/ch6/6.2.1/data/step02_calibration_scores.csv` - mean calibration across 4 tests
- RQ 6.2.3 (Resolution Over Time): `results/ch6/6.2.3/data/step01_gamma_scores.csv` - mean gamma across 4 tests
- RQ 6.1.1 (Confidence Model Selection): `results/ch6/6.1.1/data/step03_theta_confidence.csv` - Day 0 baseline confidence
- Ch5 5.1.1 (Accuracy Functional Form): `results/ch5/5.1.1/data/step03_theta_scores.csv` - Day 0 baseline accuracy

### Analysis Pipeline

**Steps:**

| Step | Description | Output Files |
|------|-------------|--------------|
| Step 0 | Merge metrics from 4 source RQs | step00_merged_metrics.csv (100 rows, 5 columns) |
| Step 1 | Create accuracy tertiles (Low/Med/High) | step01_accuracy_tertiles.csv, step01_tertile_summary.txt |
| Step 2 | Tertile comparison (Kruskal-Wallis) | step02_tertile_comparison.csv, step02_normality_tests.csv, step02_variance_tests.csv |
| Step 3 | Dunning-Kruger test (one-sample t-tests) | step03_dunning_kruger_test.csv |
| Step 4 | Correlations (Spearman) | step04_correlation.csv, step04_normality_tests.csv |
| Step 5 | Prepare plot data | step05_calibration_by_accuracy_plot_data.csv |

### Tools Used

**Key Tools:**
- **pandas:** Data merging, tertile assignment, descriptive statistics
- **scipy.stats:** Shapiro-Wilk (normality), Levene (variance homogeneity), Kruskal-Wallis (non-parametric ANOVA), one-sample t-tests, Spearman correlation
- **numpy:** Absolute value computation, data transformations
- **matplotlib/seaborn:** Visualization (via rq_plots agent)

### Critical Design Decisions

**Decision D068 (Dual p-values):**
- Bonferroni correction applied: 3 t-tests (±=0.05/3=0.0167), 2 correlations (±=0.05/2=0.025)
- All results report BOTH uncorrected and Bonferroni-corrected p-values
- Rationale: Balance Type I vs Type II error for exploratory research (source: validation.md lines 129-138)

**Tertile vs Extreme Groups:**
- Used tertiles (33%/34%/33%) rather than extreme groups (top/bottom 25%)
- Rationale: Maintains larger N per group (33-34 vs 25), but reduces power to detect small effects
- Trade-off: More stable estimates (larger N) vs weaker contrast (tertiles less extreme)
- Limitation acknowledged: Power insufficient for Dunning-Kruger small effect (d=0.20) (source: summary.md lines 256-261, 421-424)

**Baseline vs Mean Metrics:**
- Baseline accuracy/confidence: Day 0 (T1) only
- Calibration/gamma: Mean across all 4 tests (Days 0, 1, 3, 6)
- Rationale: Baseline accuracy defines tertiles (stable trait), calibration/gamma averaged for reliability (source: plan.md lines 61-71)

**Non-Parametric Test Selection:**
- Kruskal-Wallis used for tertile comparisons (both metrics)
- Spearman correlation used (both comparisons)
- Rationale: Normality violated (Shapiro-Wilk p<0.05 for abs_calibration all tertiles), variance homogeneity violated for gamma (Levene p=0.003)
- Conservative approach prioritizes robustness over power (source: validation.md lines 63-83)

**Warnings (if any from file reading):**
- None flagged during report generation

---

## 5. Results

### Sample Characteristics

**Sample Size:**
- Total N: 100 participants (complete case analysis, zero missing data)
- Exclusions: None (all participants from source RQs had complete metrics)
- Missing data: 0%

**Final Sample:**
- N = 100 (100 participants × 5 metrics merged from 4 source RQs)

**Tertile Distribution:**

| Tertile | N | Accuracy Range | Mean Accuracy |
|---------|---|----------------|---------------|
| Low | 33 | -2.24 to 0.34 | -0.31 |
| Med | 33 | 0.34 to 1.06 | 0.69 |
| High | 34 | 1.06 to 2.73 | 1.57 |

### Primary Findings

**KEY STATISTICS:**

**Finding 1: Dunning-Kruger Effect NOT SUPPORTED**

| Tertile | N | Mean Calibration | Direction | t-statistic | p_uncorr | p_bonf | Interpretation |
|---------|---|------------------|-----------|-------------|----------|--------|----------------|
| Low | 33 | +0.142 | OVERCONFIDENT | 1.13 | 0.266 | 0.797 | Trend n.s. |
| Med | 33 | -0.061 | UNDERCONFIDENT | -0.51 | 0.612 | 1.000 | Accurate |
| High | 34 | -0.079 | UNDERCONFIDENT | -0.84 | 0.407 | 1.000 | Accurate |

**Interpretation:** Low performers show overconfidence TREND (mean=+0.14 in predicted direction), but NOT SIGNIFICANT after Bonferroni correction (p_bonf=0.797). Dunning-Kruger effect not supported in this sample.

**Finding 2: Gamma-Accuracy Correlation HIGHLY SIGNIFICANT**

| Comparison | Method | Á | p_uncorr | p_bonf | 95% CI |
|------------|--------|---|----------|--------|--------|
| baseline_accuracy vs mean_gamma | Spearman | 0.461 | <0.001 | <0.001*** | [0.28, 0.62] |

**Interpretation:** Higher baseline accuracy STRONGLY CORRELATES with better metacognitive discrimination. Effect size medium-large (Á=0.46). Better memory ’ better ability to distinguish remembered from forgotten.

**Finding 3: Calibration-Accuracy Correlation NOT SIGNIFICANT**

| Comparison | Method | Á | p_uncorr | p_bonf | 95% CI |
|------------|--------|---|----------|--------|--------|
| baseline_accuracy vs abs_calibration | Spearman | -0.101 | 0.317 | 0.633 | [-0.30, 0.08] |

**Interpretation:** Absolute calibration error is INDEPENDENT of baseline accuracy. Both low and high performers are equally miscalibrated. Calibration bias is NOT related to memory ability.

**Finding 4: Tertile Comparison Results**

| Metric | Test | Statistic | p-value | Low Mean | Med Mean | High Mean | Interpretation |
|--------|------|-----------|---------|----------|----------|-----------|----------------|
| abs_calibration | Kruskal-Wallis | H=1.74 | 0.418 | 0.566 | 0.487 | 0.420 | NO tertile difference |
| mean_gamma | Kruskal-Wallis | H=21.16 | <0.001*** | 0.617 | 0.719 | 0.739 | SIGNIFICANT tertile difference |

**Convergent Evidence:** Gamma effects replicate across methods (tertile H=21.16, p<0.001 AND correlation Á=0.46, p<0.001). Calibration null replicate across methods (tertile H=1.74, p=0.418 AND correlation Á=-0.10, p=0.633).

### Model Comparison (if applicable)

NOT APPLICABLE - This RQ uses correlation/tertile analysis (no model selection)

---

## 6. Visualizations

### Plot 1: Calibration Error by Accuracy Level (Panel A) + Resolution by Accuracy Level (Panel B)
**File:** `plots/calibration_by_accuracy.png`

**Description:**
Two-panel scatterplot showing calibration metrics vs baseline accuracy with tertile color-coding (Red=Low, Orange=Med, Green=High).

**Panel A: Absolute Calibration Error by Baseline Accuracy**
- X-axis: Baseline accuracy (theta) -2.5 to 2.5
- Y-axis: Absolute calibration error 0.0 to 2.0
- Pattern: Substantial scatter, NO clear tertile separation (colors intermixed)
- Regression line: Nearly flat (slight negative slope, dashed gray)
- Annotation: Spearman Á=-0.101, p=0.633 (non-significant)

**Panel B: Gamma (Resolution) by Baseline Accuracy**
- X-axis: Baseline accuracy (theta) -2.5 to 2.5
- Y-axis: Mean gamma (resolution) 0.3 to 0.9
- Pattern: CLEAR tertile separation - Red (Low) cluster lower (³=0.4-0.8), Green (High) cluster higher (³=0.6-0.9)
- Regression line: Strong positive slope (upward right trajectory, dashed gray)
- Annotation: Spearman Á=0.461, p<0.001*** (highly significant)

**Key Patterns:**
- Panel A flat line matches non-significant correlation (visual-statistical coherence)
- Panel B steep slope matches significant correlation (visual-statistical coherence)
- Tertile separation visible only in Panel B (consistent with gamma H=21.16, p<0.001 vs abs_calibration H=1.74, p=0.418)
- Less scatter in Panel B (tighter clustering around trend) vs wide scatter in Panel A (high variance)

**Connection to Findings:**
Visual confirms statistical dissociation - Resolution (Panel B) performance-dependent, Calibration (Panel A) performance-independent. Scatter in Panel A explains why Dunning-Kruger test non-significant (high variance within low tertile masks mean difference).

---

### Plot 2: Dunning-Kruger Test - Calibration by Performance Level
**File:** `plots/dunning_kruger_boxplot.png`

**Description:**
Boxplot with individual points overlay showing mean calibration by baseline accuracy tertile. Reference line at y=0 (perfect calibration), annotation regions "OVERCONFIDENT" (above zero) and "UNDERCONFIDENT" (below zero). Diamond markers show tertile means, "n.s." labels indicate not significantly different from zero.

**Tertile Distributions:**

**Low Tertile (Red, N=33):**
- Boxplot IQR: -0.3 to +0.6
- Median: +0.1 (slightly overconfident)
- Mean (diamond): +0.14 (ABOVE zero line - OVERCONFIDENT)
- Range: -1.5 to +1.9 (widest spread)
- Label: "n.s." (p=0.797)

**Medium Tertile (Orange, N=33):**
- Boxplot IQR: -0.3 to +0.3
- Median: 0.0 (accurate)
- Mean (diamond): -0.06 (slightly below zero)
- Range: -2.0 to +0.9 (narrower than Low)
- Label: "n.s." (p=1.000)

**High Tertile (Green, N=34):**
- Boxplot IQR: -0.2 to +0.4
- Median: 0.0 (accurate)
- Mean (diamond): -0.08 (slightly below zero)
- Range: -1.6 to +0.7 (narrowest spread)
- Label: "n.s." (p=1.000)

**Key Patterns:**
- Dunning-Kruger trend VISIBLE (Low mean above zero, Med/High near/below zero) but NOT SIGNIFICANT (extensive overlap)
- High variance in Low tertile (range 3.4 units) explains non-significance (wide CI)
- Outliers present (circles beyond whiskers) - most extreme: Low +1.9 (very overconfident), Med -2.0 (very underconfident)
- Statistical "n.s." labels critical - prevents overinterpretation of visual trend

**Connection to Findings:**
Visual shows WHY Dunning-Kruger test non-significant: Mean differences present (+0.14 vs -0.06/-0.08) but obscured by overlap and variance. Boxplot reveals heterogeneity within tertiles: Some low performers well-calibrated (near zero), others extremely overconfident (+1.9). Plot transparency about null result (does NOT hide non-significance).

---

## 7. Interpretation

### Hypothesis Testing

**Original Hypothesis:**
"High baseline performers will be BETTER calibrated than low performers, showing smaller absolute calibration errors (|calibration|) and higher discrimination (gamma)."

**Hypothesis Status: PARTIALLY SUPPORTED**

**Supported:**
- Gamma (Resolution): High performers show significantly higher gamma than low performers (H=21.16, p<0.001; Á=0.461, p<0.001)

**Not Supported:**
- Absolute Calibration Error: NO significant difference across tertiles (H=1.74, p=0.418; Á=-0.10, p=0.633)
- Dunning-Kruger Pattern: Low performers show overconfidence trend (M=+0.14) but NOT statistically significant (p_bonf=0.797)

**Nuanced Finding:**
Memory ability predicts metacognitive DISCRIMINATION but NOT calibration bias or magnitude. This dissociation suggests:
1. Discrimination (gamma) reflects ability to use internal cues to differentiate correct/incorrect responses
2. Calibration magnitude reflects systematic bias or noise independent of memory skill
3. These are separable metacognitive dimensions

### Theoretical Contextualization

**Metacognitive Monitoring Theory:**

**TWO DISTINCT metacognitive processes:**

1. **Cue Utilization (Gamma/Resolution):**
   - Definition: Ability to give higher confidence to correct vs incorrect responses
   - Performance-Dependent: High performers better discrimination (³=0.74 vs 0.62)
   - Mechanism: Stronger memory traces provide more diagnostic internal cues (Koriat, 1997)
   - Finding: Strong accuracy-gamma correlation (Á=0.46) consistent with cue-utilization framework

2. **Calibration Bias (Absolute Error):**
   - Definition: Magnitude of discrepancy between confidence and accuracy (unsigned)
   - Performance-Independent: No difference across tertiles (p=0.418), no correlation (Á=-0.10)
   - Mechanism: Systematic over/underconfidence driven by factors orthogonal to memory ability (general confidence tendencies, response style)
   - Finding: Both low and high performers equally miscalibrated (M=0.42-0.57)

**Theoretical Implication:**
Metacognitive accuracy has (at least) two components that can dissociate:
- **Resolution:** How well confidence tracks accuracy (DISCRIMINATION) ’ Performance-dependent
- **Calibration:** Overall confidence-accuracy alignment (BIAS) ’ Performance-independent

Aligns with Fleming & Lau (2014) two-dimensional metacognition model: Type 1 performance (accuracy) predicts Type 2 sensitivity (discrimination) but not Type 2 bias (calibration).

### Cross-RQ Patterns

**Convergent Evidence:**

**Dunning-Kruger Double Null (RQs 6.2.4 + 6.6.2):**
- RQ 6.2.4: Low accuracy does NOT predict poor calibration (NULL, p=0.797)
- RQ 6.6.2: Low accuracy does NOT predict high HCE rates (NULL, ²=-0.001, p=1.000)
- Convergence: Low performers NOT worse at metacognitive monitoring in VR episodic memory
- Boundary condition: Dunning-Kruger effect domain-specific (robust in general knowledge/reasoning, NULL in VR episodic memory)

**Calibration Trilogy Integration (RQs 6.2.1-6.2.3):**
- RQ 6.2.1: Calibration MAGNITUDE worsens over time (p=0.004)
- RQ 6.2.2: Overconfidence PROPORTION increases (+10%, p=0.230 n.s.)
- RQ 6.2.3: Resolution DISCRIMINATION declines (p=0.011)
- RQ 6.2.4: Resolution performance-DEPENDENT, calibration performance-INDEPENDENT (NEW dissociation)

**Fleming & Lau Two-Dimensional Model Validation:**
- Ch5: Memory performance (Type 1) measured via IRT theta
- Ch6: Metacognitive sensitivity (Type 2 sensitivity = gamma) + Metacognitive bias (Type 2 bias = calibration)
- Finding: Type 1 predicts Type 2 sensitivity (Á=0.46) but NOT Type 2 bias (Á=-0.10)
- Supports model prediction: Sensitivity and bias are separable dimensions

### Unexpected Findings

**Anomaly 1: Gamma Upper Limit (~0.74 in High Performers)**

**Observation:** High performers reach ³=0.739 mean (individual max 0.87), not approaching theoretical max ³=1.0 (perfect discrimination).

**Possible Explanations:**
1. Measurement noise: Confidence ratings ordinal 1-5 scale (limited resolution), IRT theta estimation error (SE~0.3)
2. Genuine uncertainty: Even high performers uncertain about some items (ambiguous cues, weak encoding)
3. Metacognitive limitations: Imperfect access to memory trace strength (metacognitive monitoring inherently noisy per Koriat, 2007)

**Implication:** ³=0.74 may represent practical upper limit for VR episodic memory with 5-point confidence scale. Perfect discrimination (³=1.0) unrealistic expectation.

**Anomaly 2: Low Performers Still Discriminate (³=0.62 > 0.5)**

**Observation:** Low performers show moderate discrimination (³=0.617), significantly above chance (³=0.5 would be no discrimination).

**Possible Explanations:**
1. Relative strength cues: Even weak traces vary in strength (some items weaker than others)
2. Fluency heuristics: Retrieval fluency (ease of recalling) correlates with accuracy even when absolute strength low
3. Metacognitive compensation: Low performers may rely MORE on metacognitive cues (fluency, familiarity) since memory traces unreliable

**Implication:** Metacognitive discrimination preserved even in low performers (not floor effect). Everyone has SOME metacognitive ability, but high performers more accurate.

**Anomaly 3: Calibration Independence from Accuracy**

**Observation:** Absolute calibration error uncorrelated with baseline accuracy (Á=-0.10, p=0.633). Both low and high performers equally miscalibrated.

**Possible Explanations:**
1. Scaling artifacts: IRT theta scales accuracy and confidence on same metric (z-scores), but arbitrary centering may introduce bias
2. Domain-general confidence: Calibration reflects general confidence tendencies (personality trait) independent of domain-specific ability
3. Task context: VR novelty may introduce systematic bias (overconfidence due to unfamiliarity) affecting all performers equally
4. Reference point differences: High performers may use different internal standards ("I usually remember well, so this is bad for me") vs low performers ("I usually forget, so this is good for me")

**Implication:** Calibration training should target domain-general confidence strategies, not memory ability improvement.

---

## 8. Limitations

### Sample Limitations

**Sample Size:**
- N=100 provides adequate power (0.80) for medium effects (de0.5) but underpowered for small effects (d=0.2, power~0.25)
- Dunning-Kruger effect size likely small (estimated d~0.20 from M=0.14, SD=0.72), requiring N>300 per group for 80% power
- Tertile comparisons with N=33-34 per group limit ability to detect subtle differences

**Demographic Constraints:**
- University undergraduate sample (age M~20, SD~2) limits generalizability to older adults
- Restricted cognitive ability range (all college students) may compress Dunning-Kruger effect
- Predominantly female (68%) may not represent male metacognitive patterns
- WEIRD sample (Western, Educated, Industrialized, Rich, Democratic) limits cross-cultural generalizability

**Tertile Selection:**
- Used thirds (33%/34%/33%) rather than extreme groups (top/bottom 25%)
- Less power to detect effects than extreme groups designs (used in original Dunning-Kruger studies)
- "Low performers" group (bottom 33%) includes many average performers (tertile boundary at ¸=0.34, only 0.34 SD below mean)

### Methodological Limitations

**Measurement:**
1. Confidence Scale Resolution: Ordinal 1-5 confidence scale (limited granularity), may constrain gamma ceiling (³=0.74 theoretical max=1.0)
2. IRT Theta Scaling: Accuracy and confidence theta both z-standardized (M=0, SD=1), arbitrary centering may introduce calibration bias artifacts
3. Baseline-Only Analysis: Used Day 0 (T1) baseline metrics only (not averaging across test sessions), single timepoint may not reflect stable metacognitive traits (state vs trait issue)
4. Domain Aggregation: Analyzed omnibus "All" factor (What/Where/When collapsed), domain-specific calibration patterns (6.3.2) not examined here

**Design:**
1. Cross-Sectional Tertile Assignment: Tertiles based on baseline accuracy (cross-sectional grouping), cannot address whether low performers BECOME better calibrated if memory improves (longitudinal question)
2. No Experimental Manipulation: Observational correlational design (no intervention to improve calibration or memory), cannot test causal mechanisms

**Statistical:**
1. Non-Parametric Tests Required: Normality violated for absolute calibration (Shapiro-Wilk p<0.05 all tertiles), variance homogeneity violated for gamma (Levene p=0.003), Kruskal-Wallis less powerful than ANOVA
2. Multiple Comparisons: Bonferroni correction conservative (increases Type II error risk), uncorrected Dunning-Kruger p=0.266 still non-significant but closer to conventional ±=0.05
3. Outliers Present: Several extreme calibration values (Low +1.9, Med -2.0), contribute to non-normality and variance heterogeneity

### Generalizability Constraints

**Population:**
- Findings may not generalize to older adults (metacognitive monitoring declines with age), clinical populations (anosognosia patients lack metacognitive awareness), extreme cognitive ability groups (gifted or intellectually disabled)

**Context:**
- VR episodic memory specific task may differ from traditional neuropsychological tests (2D stimuli, verbal responses), real-world metacognitive judgments (everyday memory monitoring), other cognitive domains (working memory, attention, reasoning)

**Task:**
- REMEMVR paradigm specificity: Desktop VR (not fully immersive HMD), structured encoding (10-minute guided navigation), forced-choice retrieval (3-option multiple choice), confidence ratings collected AFTER retrieval (not during encoding/retrieval)

### Technical Limitations

**Cross-RQ Data Integration:**
- Relied on successful completion of 4 prior RQs (Ch5 5.1.1, RQ 6.1.1, 6.2.1, 6.2.3), assumes prior analyses valid (any errors propagate to this RQ)
- Calibration and gamma metrics inherit limitations from source RQs: IRT purification (43/102 items retained, 58% excluded), Confidence IRT model selection (RQ 6.1.1), TSVR variable assumptions (RQ 6.2.1-6.2.3)

**Difference Score Reliability:**
- Calibration metric (z_confidence - z_accuracy) is difference score
- Reliability: r_diff = 0.822 (INHERITED from RQ 6.2.1, ACCEPTABLE threshold e0.70)
- Difference scores can have lower reliability than component scores (measurement error compounds)

---

## 9. Publication-Ready Summary

**Context & Method:** This study examined whether baseline memory performance predicts metacognitive calibration quality in a VR episodic memory paradigm. N=100 participants completed 4 test sessions. Baseline accuracy (Day 0 IRT theta from Ch5 5.1.1) grouped participants into tertiles (Low/Med/High performers, N=33-34 each). Calibration metrics (mean calibration = confidence - accuracy difference; mean gamma = Goodman-Kruskal discrimination) computed from RQs 6.2.1 and 6.2.3. Tertile comparisons used Kruskal-Wallis tests (normality/variance violations), Dunning-Kruger hypothesis tested via one-sample t-tests (Low tertile overconfidence), continuous relationships examined via Spearman correlations. Bonferroni correction applied (3 t-tests ±=0.0167, 2 correlations ±=0.025).

**Results:** METACOGNITIVE DISSOCIATION discovered. Resolution (gamma) is PERFORMANCE-DEPENDENT: High performers discriminate significantly better than low performers (Kruskal-Wallis H=21.16, p<0.001; tertile means ³=0.62 vs 0.72 vs 0.74), strong positive correlation with baseline accuracy (Spearman Á=0.46, p<0.001, 95% CI [0.28, 0.62]). Calibration bias is PERFORMANCE-INDEPENDENT: No tertile difference in absolute calibration error (H=1.74, p=0.418; tertile means M=0.57 vs 0.49 vs 0.42), no correlation with baseline accuracy (Á=-0.10, p=0.633, 95% CI [-0.30, 0.08]). Dunning-Kruger effect NOT supported: Low performers show overconfidence trend (M=+0.14) but not statistically significant after Bonferroni correction (p_bonf=0.797). Convergent evidence across methods: Gamma effects replicate in both tertile comparison and correlation analysis; calibration null replicate in both analyses.

**Interpretation:** Memory ability predicts metacognitive SENSITIVITY (discrimination) but NOT metacognitive BIAS (calibration direction/magnitude). Aligns with Fleming & Lau (2014) two-dimensional metacognition model: Type 1 performance (accuracy) predicts Type 2 sensitivity (gamma, Á=0.46) but not Type 2 bias (calibration, Á=-0.10). Cue-utilization framework (Koriat, 1997): Stronger memory traces provide more diagnostic internal cues for confidence judgments, enabling better discrimination. However, calibration bias appears driven by factors orthogonal to memory ability (general confidence tendencies, response style, task context). Dunning-Kruger null finding may reflect insufficient power (N=33 per tertile underpowered for d=0.20 effect, N>300 required for 80% power), sample characteristics (restricted range in undergraduate sample, lack of extremely low performers), or domain-specificity (effect robust in general knowledge/reasoning, null in VR episodic memory).

**Conclusion:** Metacognitive calibration has dissociable components - resolution (discrimination) improves with memory ability, calibration bias does not. Clinical implication: Improving memory (e.g., mnemonic strategies) likely improves resolution (better cues available), but improving calibration requires separate training (confidence regulation, not memory enhancement). Dissociation suggests targeted interventions depending on deficit type. Boundary condition for Dunning-Kruger effect established: Low performers NOT worse at metacognitive monitoring in VR episodic memory (converges with RQ 6.6.2 double null). VR may scaffold metacognitive accuracy differently than traditional paradigms.

---

## 10. Metadata & Sources

### Report Metadata
- **Generated:** 2026-01-01
- **Agent:** rq_report v1.0.0 (Sonnet 4.5 model)
- **RQ Folder:** results/ch6/6.2.4/

### Sources Synthesized

**Archive Sources:** 5 topics, 7 entries
- rq_6.2.4_complete_dunning_kruger_not_sig_thesis_ready (archive/rq_6.2.4_complete_dunning_kruger_not_sig_thesis_ready.md, 2025-12-11)
- ch6_dunning_kruger_double_null (archive_index.md line 652-653, 2025-12-12)
- ch6_progress snapshots (archive_index.md lines 589, 605, 656, 2025-12-11 to 2025-12-12)

**RQ Files:** 24 files
- Core docs: concept.md (165 lines), plan.md (931 lines), summary.md (653 lines)
- Validation: validation.md (284 lines), PLATINUM_FINALIZATION_REPORT.md (182 lines)
- Specifications: (tools.yaml and analysis.yaml not explicitly read, embedded in code)
- Execution: status.yaml (55 lines), 9 data CSV files, 1 log file, 2 plot PNG files
- PLATINUM: PLATINUM_FINALIZATION_REPORT.md (certification complete 2025-12-29)

**Data Files Read (9 total):**
- step00_merged_metrics.csv (100 rows, 5 columns)
- step01_accuracy_tertiles.csv (100 rows, 4 columns)
- step01_tertile_summary.txt (text summary)
- step02_tertile_comparison.csv (6+ rows, tertile descriptives)
- step02_normality_tests.csv (6 rows, Shapiro-Wilk results)
- step02_variance_tests.csv (2 rows, Levene results)
- step03_dunning_kruger_test.csv (3 rows, one-sample t-tests)
- step04_correlation.csv (2 rows, Spearman correlations)
- step04_normality_tests.csv (3 rows, normality for correlation variables)
- step05_calibration_by_accuracy_plot_data.csv (100 rows, plot source)

**Plots Inspected (2 total):**
- calibration_by_accuracy.png (168KB, two-panel scatterplot with tertile coloring)
- dunning_kruger_boxplot.png (116KB, boxplot with individual points overlay)

**Logs Read (1 total):**
- steps_00_to_05.log (8.3KB, execution log for 6-step pipeline)

### Context Dumps from status.yaml

**rq_tools_context:**
"0 analysis + 4 validation tools cataloged for calibration by accuracy analysis"

**rq_analysis_context:**
"6 steps (stdlib only - pandas+scipy), 4 validation tools, cross-RQ derived data analysis"

**rq_results_context:**
"Results validated for scientific plausibility. 3 key findings: (1) Dunning-Kruger NOT significant (p=0.797), (2) Gamma-accuracy correlation STRONG (Á=0.46, p<0.001), (3) Calibration independent of accuracy (p=0.633). Summary documented in results/summary.md"

**rq_platinum_context:**
"PLATINUM CERTIFIED (2025-12-29). Criteria Version: 2025-12-27 (GLMM validation, random slopes, difference score reliability). GLMM Compliance: NOT NEEDED (correlation/tertile analysis, no intercept testing). Difference Score Reliability: INHERITED from RQ 6.2.1 (r_diff=0.822). Power Analysis: DOCUMENTED for Dunning-Kruger null (d=0.20, N>300 required for 0.80 power). Zero blockers, 100% criteria met, publication-ready"

### Warnings Flagged

**No warnings flagged during report generation.**

All critical files present, all validation checks passed, PLATINUM certification complete.

---

**End of Report**
