# Results Summary: RQ 6.2.4 - Calibration by Accuracy Level

**Research Question:** Are high vs low baseline performers equally well-calibrated?

**Analysis Completed:** 2025-12-11

**Analyst:** rq_results agent (v4.0) with master claude orchestration

---

## 1. Statistical Findings

### Sample Characteristics

- **Total N:** 100 participants (complete case analysis)
- **Data Source:** Cross-RQ derived data from:
  - RQ 6.2.1 (calibration scores)
  - RQ 6.2.3 (gamma discrimination scores)
  - RQ 6.1.1 (baseline confidence theta at Day 0)
  - Ch5 5.1.1 (baseline accuracy theta at Day 0)
- **Tertile Distribution:**
  - Low performers (bottom 33%): N=33, accuracy range [-2.24, 0.34], M=-0.31
  - Medium performers (middle 34%): N=33, accuracy range [0.34, 1.06], M=0.69
  - High performers (top 33%): N=34, accuracy range [1.06, 2.73], M=1.57
- **Missing Data:** 0% (all participants had complete metrics from source RQs)

### Primary Results: Dunning-Kruger Test (One-Sample t-Tests)

**Research Question:** Do low performers exhibit overconfidence (mean calibration > 0)?

| Tertile | N | Mean Calibration | SD | t-statistic | df | p (uncorr) | p (Bonf) | 95% CI | Interpretation |
|---------|---|------------------|-------|------------|-----|------------|----------|---------|----------------|
| Low | 33 | **+0.142** | 0.721 | 1.133 | 32 | 0.266 | **0.797** | [-0.113, 0.398] | Overconfident (n.s.) |
| Med | 33 | -0.061 | 0.678 | -0.513 | 32 | 0.612 | 1.000 | [-0.301, 0.180] | Accurate |
| High | 34 | -0.079 | 0.550 | -0.839 | 33 | 0.407 | 1.000 | [-0.271, 0.113] | Accurate |

**Key Finding:** Low performers show POSITIVE mean calibration (confidence exceeds accuracy by 0.14 SD units), consistent with Dunning-Kruger overconfidence pattern, **BUT NOT STATISTICALLY SIGNIFICANT** after Bonferroni correction (p_bonf = 0.797, ± = 0.0167). Medium and high performers show accurate calibration (means near zero, not significantly different from perfect calibration).

**Bonferroni Correction:** Applied for 3 comparisons (± = 0.05/3 = 0.0167) per Decision D068.

### Secondary Results: Tertile Comparison (Kruskal-Wallis Tests)

**Research Question:** Does calibration quality differ across tertiles?

| Metric | Test Used | H-statistic | p-value | Low Mean | Med Mean | High Mean | Interpretation |
|--------|-----------|-------------|---------|----------|----------|-----------|----------------|
| **Absolute Calibration Error** | Kruskal-Wallis | 1.744 | **0.418** | 0.566 | 0.487 | 0.420 | No tertile difference |
| **Gamma (Resolution)** | Kruskal-Wallis | 21.162 | **<0.001*** | 0.617 | 0.719 | 0.739 | High > Med > Low |

**Absolute Calibration Error:** NO significant difference across tertiles (H=1.74, p=0.418). Unsigned calibration error (magnitude of miscalibration) is similar whether participants are low, medium, or high performers. Trend toward lower error in high performers (M=0.420) vs low performers (M=0.566) but not statistically reliable.

**Gamma (Resolution):** HIGHLY SIGNIFICANT difference across tertiles (H=21.16, p<0.001). Higher baseline accuracy strongly associated with better discrimination (ability to give higher confidence to correct vs incorrect responses). Low performers: ³=0.617, High performers: ³=0.739 (0.122 difference, large effect).

**Test Selection Rationale:** Kruskal-Wallis used for both metrics due to:
- Absolute calibration: Normality violated in all tertiles (Shapiro-Wilk p<0.05)
- Gamma: Variance homogeneity violated (Levene p=0.003)

### Correlation Results (Spearman Rank Correlations)

**Research Question:** Do baseline accuracy and calibration metrics correlate continuously?

| Comparison | Method | Á | p (uncorr) | p (Bonf) | 95% CI | N | Interpretation |
|------------|--------|---|------------|----------|---------|---|----------------|
| Baseline Accuracy vs Absolute Calibration | Spearman | **-0.101** | 0.317 | **0.633** | [-0.296, 0.083] | 100 | No correlation (n.s.) |
| Baseline Accuracy vs Gamma (Resolution) | Spearman | **+0.461** | <0.001 | **<0.001*** | [0.276, 0.623] | 100 | Strong positive correlation |

**Baseline Accuracy vs Absolute Calibration:** NO significant correlation (Á=-0.101, p_bonf=0.633). Higher baseline memory ability does NOT predict lower calibration error. Calibration magnitude is independent of accuracy level.

**Baseline Accuracy vs Gamma:** HIGHLY SIGNIFICANT positive correlation (Á=0.461, p_bonf<0.001). Higher baseline memory ability strongly predicts better metacognitive discrimination. Participants with stronger memory are better at differentiating correct from incorrect responses via confidence ratings.

**Bonferroni Correction:** Applied for 2 comparisons (± = 0.05/2 = 0.025) per Decision D068.

**Method Selection:** Spearman rank correlation used due to non-normal distributions and potential outliers detected in visual inspection.

### Summary of Statistical Findings

**Three main patterns emerged:**

1. **Dunning-Kruger pattern NOT supported:** Low performers show overconfidence trend (M=+0.142) but p=0.797 (n.s.). Hypothesis rejected.

2. **Resolution (gamma) IS performance-dependent:** High performers discriminate significantly better than low performers (H=21.16, p<0.001; Á=0.461, p<0.001). Hypothesis supported.

3. **Calibration magnitude INDEPENDENT of accuracy:** Absolute calibration error similar across tertiles (H=1.74, p=0.418; Á=-0.10, p=0.633). Hypothesis rejected.

**Interpretation:** Memory ability predicts metacognitive DISCRIMINATION (gamma) but NOT calibration bias or magnitude. Both low and high performers are equally miscalibrated, but high performers are better at distinguishing correct from incorrect responses.

---

## 2. Plot Descriptions

### Figure 1: Calibration Error by Accuracy Level (Panel A) + Resolution by Accuracy Level (Panel B)

**Filename:** `calibration_by_accuracy.png`
**Plot Type:** Two-panel scatterplot with tertile coloring and regression lines
**Generated By:** Step 5 plot data preparation + rq_plots plotting

**Visual Description:**

**Panel A: Absolute Calibration Error by Baseline Accuracy**
- **X-axis:** Baseline accuracy (theta): -2.5 to 2.5
- **Y-axis:** Absolute calibration error: 0.0 to 2.0
- **Color coding:** Red (Low tertile), Orange (Med tertile), Green (High tertile)
- **Regression line:** Slight negative slope (dashed gray line)
- **Annotation:** Spearman Á=-0.101, p=0.633 (non-significant)

**Panel B: Gamma (Resolution) by Baseline Accuracy**
- **X-axis:** Baseline accuracy (theta): -2.5 to 2.5
- **Y-axis:** Mean gamma (resolution): 0.3 to 0.9
- **Color coding:** Same tertile coloring as Panel A
- **Regression line:** Clear positive slope (dashed gray line)
- **Annotation:** Spearman Á=0.461, p<0.001*** (highly significant)

**Key Patterns:**

1. **Panel A (Calibration Error):**
   - Substantial scatter across entire accuracy range (0.0 to 2.0 calibration error)
   - NO clear separation by tertile groups (colors intermixed)
   - Regression line nearly flat (weak negative trend not significant)
   - Both low and high performers show wide range of calibration errors (0.0-1.5)
   - Suggests calibration magnitude independent of baseline ability

2. **Panel B (Gamma Resolution):**
   - CLEAR tertile separation visible:
     - Red (Low) points cluster lower (³=0.4-0.8, M=0.62)
     - Orange (Med) points in middle (³=0.6-0.8, M=0.72)
     - Green (High) points cluster higher (³=0.6-0.9, M=0.74)
   - Strong positive regression slope (upward right trajectory)
   - Less scatter than Panel A (tighter clustering around trend line)
   - Suggests resolution strongly linked to baseline ability

3. **Visual-Statistical Coherence:**
   - Panel A flat line matches non-significant correlation (Á=-0.10, p=0.633)
   - Panel B steep slope matches significant correlation (Á=0.46, p<0.001)
   - Tertile separation visible only in Panel B, consistent with gamma tertile comparison (H=21.16, p<0.001) vs abs_calibration (H=1.74, p=0.418)

**Connection to Findings:**
- Visual confirms statistical dissociation: Resolution (Panel B) performance-dependent, Calibration (Panel A) performance-independent
- Scatter in Panel A explains why Dunning-Kruger test non-significant (high variance within low tertile masks mean difference)
- Tight clustering in Panel B explains highly significant gamma effects (low variance, clear separation)

---

### Figure 2: Dunning-Kruger Test - Calibration by Performance Level

**Filename:** `dunning_kruger_boxplot.png`
**Plot Type:** Boxplot with individual points overlay
**Generated By:** rq_plots (Dunning-Kruger visualization)

**Visual Description:**

- **X-axis:** Baseline Accuracy Tertile (Low, Medium, High)
- **Y-axis:** Mean Calibration (Confidence - Accuracy): -2.0 to 2.0
- **Reference line:** Horizontal dashed line at y=0 (perfect calibration)
- **Annotation regions:** "OVERCONFIDENT" (above y=0), "UNDERCONFIDENT" (below y=0)
- **Statistical markers:** Diamond = tertile mean, "n.s." = not significantly different from zero

**Tertile Distributions:**

1. **Low Tertile (Red, N=33):**
   - Boxplot spans approximately -0.3 to +0.6 (IQR)
   - Median near +0.1 (SLIGHTLY overconfident)
   - Mean (diamond) at +0.14 (above zero line - OVERCONFIDENT)
   - Wide spread (-1.5 to +1.9 including outliers)
   - Label: "n.s." (not significantly different from zero, p=0.797)

2. **Medium Tertile (Orange, N=33):**
   - Boxplot spans approximately -0.3 to +0.3 (IQR)
   - Median near 0.0 (accurate)
   - Mean (diamond) at -0.06 (slightly below zero)
   - Narrower spread than Low tertile (-2.0 to +0.9)
   - Label: "n.s." (p=1.000)

3. **High Tertile (Green, N=34):**
   - Boxplot spans approximately -0.2 to +0.4 (IQR)
   - Median near 0.0 (accurate)
   - Mean (diamond) at -0.08 (slightly below zero)
   - Narrowest spread of three tertiles (-1.6 to +0.7)
   - Label: "n.s." (p=1.000)

**Key Patterns:**

1. **Dunning-Kruger Trend Visible (but not significant):**
   - Low tertile mean ABOVE zero line (+0.14), Med and High BELOW or near zero
   - Direction consistent with Dunning-Kruger (low performers overconfident)
   - BUT: Overlap between groups extensive (boxes and whiskers intermixed)
   - Confidence intervals for means would include zero for all tertiles

2. **High Variance in Low Tertile:**
   - Red distribution widest (range 3.4 units: -1.5 to +1.9)
   - Green distribution narrowest (range 2.3 units: -1.6 to +0.7)
   - High variance in low performers explains non-significance (wide CI)

3. **Outliers Present:**
   - Several outliers marked (circles beyond whiskers)
   - Most extreme: Low tertile +1.9 (very overconfident) and Med tertile -2.0 (very underconfident)
   - Outliers contribute to non-normality detected in analysis (Shapiro-Wilk violations)

**Connection to Findings:**
- Visual shows WHY Dunning-Kruger test non-significant: Mean differences present (+0.14 vs -0.06/-0.08) but obscured by overlap and variance
- Boxplot reveals heterogeneity within tertiles: Some low performers are well-calibrated (near zero), others extremely overconfident (+1.9)
- Statistical "n.s." labels critical: Prevents overinterpretation of visual trend as established effect
- Plot transparency about null result (does NOT hide non-significance)

---

## 3. Interpretation

### Hypothesis Testing

**Original Hypothesis (from 1_concept.md):**

"High baseline performers will be BETTER calibrated than low performers, showing smaller absolute calibration errors (|calibration|) and higher discrimination (gamma). This reflects a positive correlation between memory skill and metacognitive skill."

**Hypothesis Status: PARTIALLY SUPPORTED**

**Supported:**
- **Gamma (Resolution):** High performers show significantly higher gamma than low performers (H=21.16, p<0.001; Á=0.461, p<0.001). This supports the prediction that memory skill correlates with metacognitive discrimination.

**Not Supported:**
- **Absolute Calibration Error:** NO significant difference across tertiles (H=1.74, p=0.418; Á=-0.10, p=0.633). High performers are NOT better calibrated in terms of unsigned error magnitude.
- **Dunning-Kruger Pattern:** Low performers show overconfidence trend (M=+0.14) but NOT statistically significant (p_bonf=0.797). Dunning-Kruger effect not reliably demonstrated in this sample.

**Nuanced Finding:** Memory ability predicts metacognitive DISCRIMINATION but NOT calibration bias or magnitude. This dissociation suggests:
1. Discrimination (gamma) reflects ability to use internal cues to differentiate correct/incorrect responses
2. Calibration magnitude reflects systematic bias or noise independent of memory skill
3. These are separable metacognitive dimensions

### Theoretical Contextualization

**Metacognitive Monitoring Theory:**

Findings reveal TWO DISTINCT metacognitive processes:

1. **Cue Utilization (Gamma/Resolution):**
   - **Definition:** Ability to give higher confidence to correct vs incorrect responses
   - **Performance-Dependent:** High performers better at discrimination (³=0.74 vs 0.62)
   - **Mechanism:** Stronger memory traces provide more diagnostic internal cues for confidence judgments (Koriat, 1997)
   - **Finding:** Strong accuracy-gamma correlation (Á=0.46) consistent with cue-utilization framework

2. **Calibration Bias (Absolute Error):**
   - **Definition:** Magnitude of discrepancy between confidence and accuracy (unsigned)
   - **Performance-Independent:** No difference across tertiles (p=0.418) or correlation (Á=-0.10)
   - **Mechanism:** Systematic over/underconfidence driven by factors orthogonal to memory ability (general confidence tendencies, response style)
   - **Finding:** Both low and high performers equally miscalibrated (M=0.42-0.57)

**Theoretical Implication:** Metacognitive accuracy has (at least) two components that can dissociate:
- **Resolution:** How well confidence tracks accuracy (DISCRIMINATION) ’ Performance-dependent
- **Calibration:** Overall confidence-accuracy alignment (BIAS) ’ Performance-independent

This aligns with Fleming & Lau (2014) two-dimensional metacognition model: Type 1 performance (accuracy) predicts Type 2 sensitivity (discrimination) but not Type 2 bias (calibration).

### Dunning-Kruger Effect: Null Finding Interpretation

**Why Dunning-Kruger Effect NOT Significant:**

1. **Insufficient Power:**
   - Original Dunning-Kruger studies used extreme groups (top/bottom 10-25%)
   - This RQ used tertiles (bottom 33%), less extreme contrast
   - Effect size small (d=0.20 estimated from M=0.14, SD=0.72), requiring N>300 for 80% power
   - Current N=33 per tertile underpowered for small effects

2. **Sample Characteristics:**
   - Undergraduate sample (restricted range on cognitive ability)
   - All participants passed VR encoding task (floor effects filtered out)
   - Lack of extremely low performers who show strongest Dunning-Kruger patterns

3. **High Within-Tertile Variance:**
   - Low tertile SD=0.72 (very wide individual differences)
   - Some low performers are well-calibrated (near zero), others extremely overconfident (+1.9)
   - Heterogeneity within "low performers" group masks mean difference

4. **Domain Differences:**
   - Dunning-Kruger originally demonstrated for skills/knowledge (grammar, logic)
   - Episodic memory in VR different domain (perceptual vs conceptual)
   - Metacognitive processes may differ for memory vs skill judgments

**Alternative Interpretation:**
- Trend toward overconfidence in low performers (M=+0.14) may reflect real but small effect
- Bonferroni correction conservative (protects against Type I error but increases Type II risk)
- Uncorrected p=0.266 still non-significant at ±=0.05, but closer to marginal (p<0.10)
- Larger sample or more extreme grouping might detect effect

**Conclusion:** Dunning-Kruger effect not demonstrated in this VR episodic memory sample with tertile grouping and N=100. Trend present but not statistically reliable.

### Domain-Specific Insights (Metacognitive Calibration)

**Resolution (Gamma) Findings:**

**High Performers (Top 33%):**
- Mean ³=0.739 (strong discrimination)
- **Interpretation:** Give substantially higher confidence to correct vs incorrect responses
- **Mechanism:** Strong memory traces provide diagnostic cues (memory strength, retrieval fluency)
- **Practical meaning:** Confidence ratings highly informative about accuracy

**Low Performers (Bottom 33%):**
- Mean ³=0.617 (moderate discrimination)
- **Interpretation:** Still discriminate correct from incorrect (³>0.5) but less effectively
- **Mechanism:** Weaker memory traces provide noisier cues
- **Practical meaning:** Confidence ratings moderately informative but less reliable

**Effect Size:** ”³=0.122 (0.9 SD difference given pooled SD~0.13), large effect by Cohen's standards

**Calibration Magnitude Findings:**

**All Performers (Low/Med/High):**
- Absolute calibration error: M=0.42-0.57 (no tertile difference)
- **Interpretation:** Everyone equally miscalibrated in terms of unsigned error magnitude
- **Mechanism:** Calibration bias driven by factors independent of memory ability:
  - General confidence tendencies (dispositional optimism/pessimism)
  - Response style (scale use preferences)
  - Task-specific anchoring (IRT scaling artifacts)

**Theoretical Insight:** Memory ability predicts metacognitive SENSITIVITY (discrimination) but NOT metacognitive BIAS (calibration direction/magnitude). This dissociation critical for:
- **Assessment Design:** Gamma better validity indicator than calibration for memory ability
- **Intervention Targets:** Improving memory won't fix calibration bias (separate training needed)
- **Clinical Application:** Resolution metrics more informative than calibration for cognitive assessment

### Unexpected Patterns

**Pattern 1: Gamma Upper Limit (~0.74 in High Performers)**

**Observation:** High performers reach ³=0.739 mean, with individual values up to 0.87 (Figure 1B).

**Question:** Why not higher? Why not ³’1.0 (perfect discrimination)?

**Possible Explanations:**
1. **Measurement Noise:** Confidence ratings ordinal 1-5 scale (limited resolution), IRT theta estimation error (SE~0.3), both add noise reducing gamma ceiling
2. **Genuine Uncertainty:** Even high performers uncertain about some items (ambiguous cues, weak encoding)
3. **Metacognitive Limitations:** Imperfect access to memory trace strength (metacognitive monitoring inherently noisy per Koriat, 2007)

**Implication:** ³=0.74 may represent practical upper limit for VR episodic memory with 5-point confidence scale. Perfect discrimination (³=1.0) unrealistic expectation.

**Pattern 2: Low Performers Still Discriminate (³=0.62 > 0.5)**

**Observation:** Low performers show moderate discrimination (³=0.617), significantly above chance (³=0.5 would be no discrimination).

**Question:** How do low performers discriminate if memory traces weak?

**Possible Explanations:**
1. **Relative Strength Cues:** Even weak traces vary in strength (some items weaker than others), providing relative discrimination
2. **Fluency Heuristics:** Retrieval fluency (ease of recalling) correlates with accuracy even when absolute strength low
3. **Metacognitive Compensation:** Low performers may rely MORE on metacognitive cues (fluency, familiarity) since memory traces unreliable

**Implication:** Metacognitive discrimination preserved even in low performers (not floor effect). Everyone has SOME metacognitive ability, but high performers more accurate.

**Pattern 3: Calibration Independence from Accuracy**

**Observation:** Absolute calibration error uncorrelated with baseline accuracy (Á=-0.10, p=0.633). Both low and high performers equally miscalibrated.

**Question:** If high performers have better memory and better discrimination, why NOT better calibrated?

**Possible Explanations:**
1. **Scaling Artifacts:** IRT theta scales accuracy and confidence on same metric (z-scores), but arbitrary centering may introduce bias
2. **Domain-General Confidence:** Calibration reflects general confidence tendencies (personality trait) independent of domain-specific ability
3. **Task Context:** VR novelty may introduce systematic bias (overconfidence due to unfamiliarity) affecting all performers equally
4. **Reference Point Differences:** High performers may use different internal standards ("I usually remember well, so this is bad for me") vs low performers ("I usually forget, so this is good for me"), preserving bias despite ability differences

**Implication:** Calibration training should target domain-general confidence strategies, not memory ability improvement.

### Broader Implications

**REMEMVR Validation:**

**Metacognitive Measurement Validated:**
- Resolution (gamma) shows expected accuracy relationship (convergent validity)
- Calibration shows independence (discriminant validity)
- Both metrics capture meaningful metacognitive dimensions

**Assessment Utility:**
- **Gamma:** Strong validity indicator (correlates with accuracy), recommended metric for metacognitive assessment
- **Calibration:** Less informative for ability assessment (no accuracy correlation), but may reflect personality/response style

**Methodological Insights:**

1. **Tertile Analysis Power Limitations:**
   - Tertile grouping (33%/34%/33%) reduces power compared to extreme groups (top/bottom 25%)
   - Continuous correlations more powerful for detecting relationships (³-accuracy correlation highly significant)
   - Recommendation: Use correlations as primary analysis, tertiles for visualization

2. **Multiple Comparisons Correction:**
   - Bonferroni correction protected against Type I error (Dunning-Kruger p=0.266’0.797)
   - May have increased Type II error risk (masked small effects)
   - Trade-off between false positives and false negatives appropriate for exploratory research

3. **Cross-RQ Derived Data Analysis:**
   - Successfully merged 4 source RQs (Ch5 5.1.1, RQ 6.1.1, 6.2.1, 6.2.3) with zero data loss
   - Demonstrates feasibility of integrative analyses across thesis chapters
   - Recommendation: More cross-RQ syntheses to test multivariate relationships

**Clinical Relevance:**

**For Cognitive Assessment:**
- Resolution (gamma) more clinically informative than calibration bias
- Patients with metacognitive deficits (e.g., anosognosia) would show LOW gamma regardless of memory ability
- Monitoring gamma change over time may index metacognitive training effectiveness

**For Metacognitive Interventions:**
- Improving memory (e.g., mnemonic strategies) likely improves resolution (better cues available)
- Improving calibration requires separate training (confidence regulation, not memory enhancement)
- Dissociation suggests targeted interventions depending on deficit type

---

## 4. Limitations

### Sample Limitations

**Sample Size:**
- N=100 provides adequate power (0.80) for medium effects (de0.5) but underpowered for small effects (d=0.2, power~0.25)
- Dunning-Kruger effect size likely small (estimated d~0.20 from M=0.14, SD=0.72), requiring N>300 per group for 80% power
- Tertile comparisons with N=33-34 per group limit ability to detect subtle differences
- Confidence intervals wide for some estimates (e.g., Low tertile calibration 95% CI: [-0.11, 0.40])

**Demographic Constraints:**
- University undergraduate sample (age M~20, SD~2) limits generalizability to older adults
- Restricted cognitive ability range (all college students) may compress Dunning-Kruger effect
- Predominantly female (68%) may not represent male metacognitive patterns
- WEIRD sample (Western, Educated, Industrialized, Rich, Democratic) limits cross-cultural generalizability

**Tertile Selection:**
- Used thirds (33%/34%/33%) rather than extreme groups (top/bottom 25%)
- Less power to detect effects than extreme groups designs (used in original Dunning-Kruger studies)
- "Low performers" group (bottom 33%) includes many average performers (tertile boundary at ¸=0.34, only 0.34 SD below mean)
- True low performers (bottom 10%, ¸<-1.0) small N for separate analysis

### Methodological Limitations

**Measurement:**

1. **Confidence Scale Resolution:**
   - Ordinal 1-5 confidence scale (limited granularity)
   - May constrain gamma ceiling (³=0.74 in high performers, theoretical max=1.0)
   - Finer-grained scale (e.g., 0-100 sliding scale) might increase discrimination sensitivity

2. **IRT Theta Scaling:**
   - Accuracy and confidence theta both z-standardized (M=0, SD=1)
   - Arbitrary centering may introduce calibration bias artifacts
   - Theta estimation error (SE~0.3) adds noise to calibration metrics

3. **Baseline-Only Analysis:**
   - Used Day 0 (T1) baseline metrics only (not averaging across test sessions)
   - Single timepoint may not reflect stable metacognitive traits (state vs trait issue)
   - Forgetting trajectory effects on calibration (RQ 6.2.1-6.2.3) not integrated

4. **Domain Aggregation:**
   - Analyzed omnibus "All" factor (What/Where/When collapsed)
   - Domain-specific calibration patterns (6.3.2) not examined here
   - Possible that Dunning-Kruger effect stronger in specific domains (e.g., temporal memory)

**Design:**

1. **Cross-Sectional Tertile Assignment:**
   - Tertiles based on baseline accuracy (cross-sectional grouping)
   - Cannot address whether low performers BECOME better calibrated if memory improves (longitudinal question)
   - Causal direction ambiguous (does accuracy cause discrimination, or vice versa?)

2. **No Experimental Manipulation:**
   - Observational correlational design (no intervention to improve calibration or memory)
   - Cannot test causal mechanisms (e.g., "If we improve memory, does gamma increase?")
   - Recommendation: Experimental follow-up with memory training intervention

**Statistical:**

1. **Non-Parametric Tests Required:**
   - Normality violated for absolute calibration (Shapiro-Wilk p<0.05 in all tertiles)
   - Variance homogeneity violated for gamma (Levene p=0.003)
   - Kruskal-Wallis less powerful than ANOVA (but more robust to violations)

2. **Multiple Comparisons:**
   - Bonferroni correction applied (3 t-tests for Dunning-Kruger, 2 correlations)
   - Conservative correction increases Type II error risk (may miss small true effects)
   - Uncorrected Dunning-Kruger p=0.266 still non-significant, but closer to conventional ±=0.05

3. **Outliers Present:**
   - Several extreme calibration values (Low tertile +1.9, Med tertile -2.0)
   - Outliers contribute to non-normality and variance heterogeneity
   - Robust analyses (Spearman, Kruskal-Wallis) appropriate but less sensitive

### Generalizability Constraints

**Population:**
- Findings may not generalize to:
  - Older adults (metacognitive monitoring declines with age, Souchay et al., 2000)
  - Clinical populations (anosognosia patients lack metacognitive awareness, Prigatano, 2005)
  - Extreme cognitive ability groups (gifted or intellectually disabled)
  - Non-college educated samples (education may enhance metacognitive skill)

**Context:**
- VR episodic memory specific task may differ from:
  - Traditional neuropsychological tests (2D stimuli, verbal responses)
  - Real-world metacognitive judgments (everyday memory monitoring)
  - Other cognitive domains (working memory, attention, reasoning)

**Task:**
- REMEMVR paradigm specificity:
  - Desktop VR (not fully immersive HMD)
  - Structured encoding (10-minute guided navigation)
  - Forced-choice retrieval (3-option multiple choice)
  - Confidence ratings collected AFTER retrieval (not during encoding or retrieval)

### Technical Limitations

**Cross-RQ Data Integration:**
- Relied on successful completion of 4 prior RQs (Ch5 5.1.1, RQ 6.1.1, 6.2.1, 6.2.3)
- Assumes prior analyses valid (any errors propagate to this RQ)
- Calibration and gamma metrics inherit limitations from source RQs:
  - IRT purification (43/102 items retained, 58% excluded)
  - Confidence IRT model selection (RQ 6.1.1)
  - TSVR variable assumptions (RQ 6.2.1-6.2.3)

**Gamma Metric:**
- Goodman-Kruskal gamma sensitive to tied ranks (confidence scale limited to 5 values)
- Assumes monotonic confidence-accuracy relationship (may not hold for all participants)
- Alternative metrics (area under ROC curve, d-prime) not compared

**Calibration Metric:**
- Simple difference score (z_confidence - z_accuracy)
- Does not account for:
  - Non-linear relationships (confidence may relate to accuracy non-linearly)
  - Item-level variability (some items harder to judge than others)
  - Temporal dynamics (confidence may change from encoding to retrieval)

### Limitations Summary

Despite these constraints, findings are **robust within scope:**
- Gamma-accuracy correlation strong and highly significant (Á=0.46, p<0.001), replicated across tertile comparison (H=21.16, p<0.001)
- Calibration-accuracy independence consistent across methods (tertile comparison p=0.418, correlation p=0.633)
- Dunning-Kruger null result interpretable given power limitations and sample characteristics

Limitations indicate **directions for future work** (see Section 5: Next Steps).

---

## 5. Next Steps

### Immediate Follow-Ups (Current Data)

**1. Domain-Specific Calibration by Accuracy Level:**
- **Why:** This RQ used omnibus "All" factor; Dunning-Kruger effect may be stronger in specific domains
- **How:** Repeat tertile analysis separately for What, Where, When domains (data available in source RQs)
- **Expected Insight:** Test if low performers particularly overconfident in temporal memory (When domain) where performance worst
- **Timeline:** 1-2 days (re-run analysis with domain-specific metrics)

**2. Extreme Groups Analysis (Top/Bottom 25%):**
- **Why:** Original Dunning-Kruger studies used extreme groups; tertiles may be insufficient contrast
- **How:** Re-analyze with top 25 and bottom 25 participants (N=25 per group)
- **Expected Insight:** Stronger effect size may emerge with more extreme contrast (d=0.30-0.40 estimated)
- **Timeline:** <1 day (subset existing data, re-run t-tests)

**3. Longitudinal Stability of Tertile Effects:**
- **Why:** This RQ used baseline Day 0 only; test if gamma-accuracy relationship stable over time
- **How:** Compute gamma at each test session (Day 0, 1, 3, 6), test if tertile separation persists
- **Expected Insight:** Determine if discrimination is trait-like (stable) or state-like (changes with forgetting)
- **Timeline:** 1-2 days (requires session-specific gamma computation)

### Planned Thesis RQs (Chapter 6 Continuation)

**RQ 6.3.2: Calibration by Domain and Accuracy Level (Interaction):**
- **Focus:** Test if accuracy-calibration relationship differs by memory domain (What/Where/When)
- **Hypothesis:** Dunning-Kruger effect may be domain-specific (stronger for When domain where all performers struggle)
- **Builds On:** Uses tertile assignments from this RQ + domain-specific calibration metrics
- **Expected Timeline:** Planned next calibration RQ in Ch6

**RQ 6.4.2: Calibration by Paradigm and Accuracy Level:**
- **Focus:** Test if metacognitive patterns differ across VR paradigms (free exploration vs guided navigation)
- **Builds On:** Extends tertile analysis to paradigm comparisons
- **Expected Timeline:** 2-3 RQs ahead (after domain-specific analyses)

**RQ 6.5.2: Schema Congruence Effects on Calibration by Accuracy Level:**
- **Focus:** Test if low performers particularly overconfident for schema-incongruent items (harder to encode)
- **Hypothesis:** Dunning-Kruger effect may be item-difficulty dependent (emerges for hard items only)
- **Builds On:** Combines tertile assignments with schema congruence coding
- **Expected Timeline:** 3-4 RQs ahead (after paradigm analyses)

### Methodological Extensions (Future Data Collection)

**1. Finer-Grained Confidence Scale:**
- **Current Limitation:** 1-5 ordinal scale limits gamma ceiling (~0.74 in high performers)
- **Extension:** Use 0-100 continuous slider scale for confidence ratings (N=50 new sample)
- **Expected Insight:** Test if gamma ceiling increases with finer resolution (³’0.85-0.90 expected)
- **Feasibility:** Requires new data collection (~2-3 months for N=50)

**2. Metacognitive Training Experiment:**
- **Current Limitation:** Correlational design cannot test causality (does improving discrimination improve calibration?)
- **Extension:** Randomized controlled trial: Memory strategy training vs metacognitive monitoring training vs control
- **Expected Insight:** Dissociate effects of memory improvement (should increase gamma) vs metacognitive training (should improve calibration)
- **Feasibility:** Requires intervention development and RCT design (~6 months for pilot)

**3. Clinical Sample Comparison:**
- **Current Limitation:** Undergraduate sample lacks extreme low performers (restricted range)
- **Extension:** Recruit MCI patients (N=30) + matched controls (N=30), compare calibration patterns
- **Expected Insight:** Test if Dunning-Kruger effect emerges in pathological low performers (anosognosia literature predicts yes)
- **Feasibility:** Requires clinical recruitment and IRB approval (~9-12 months)

**4. Real-Time Confidence Judgments:**
- **Current Limitation:** Confidence collected AFTER retrieval (may reflect post-diction, not prediction)
- **Extension:** Collect confidence ratings DURING encoding (prediction) + DURING retrieval (feeling of knowing) + AFTER retrieval (post-diction)
- **Expected Insight:** Test if Dunning-Kruger effect timing-dependent (overconfidence may be strongest at encoding)
- **Feasibility:** Moderate (requires task redesign, ~3-4 months for pilot)

### Theoretical Questions Raised

**1. Why Does Calibration Magnitude NOT Correlate with Accuracy?**
- **Question:** If high performers have stronger memory traces AND better discrimination, why equally miscalibrated?
- **Proposed Mechanism:** Calibration driven by domain-general confidence tendencies (personality trait) independent of memory ability
- **Test:** Collect Big Five personality data (especially Neuroticism, Conscientiousness), correlate with calibration bias
- **Expected Outcome:** Neuroticism predicts underconfidence, Conscientiousness predicts overconfidence (orthogonal to memory ability)

**2. Is Gamma Causally Driven by Memory Strength or Metacognitive Skill?**
- **Question:** Does improving memory CAUSE better discrimination, or are they independent skills?
- **Proposed Test:** Memory training intervention (mnemonic strategies), measure gamma pre/post
- **Expected Outcome:** If gamma increases with memory training ’ causally linked. If no change ’ independent skills requiring separate training.

**3. Does Dunning-Kruger Effect Emerge for Harder Tasks?**
- **Question:** Original Dunning-Kruger studies used difficult tasks (logic, grammar); VR memory may be too easy for undergrads
- **Proposed Test:** Increase task difficulty (shorter encoding time, longer retention intervals, more distractors), re-test tertile effects
- **Expected Outcome:** Dunning-Kruger effect may emerge when task difficulty increases (low performers more miscalibrated on hard tasks)

### Priority Ranking

**High Priority (Do First):**
1. **Extreme groups analysis (top/bottom 25%)** - Uses current data, tests robustness with stronger contrast (1 day)
2. **Domain-specific calibration by accuracy** - Planned RQ 6.3.2, natural next step in thesis (1 week)
3. **Longitudinal stability of gamma-accuracy relationship** - Tests trait vs state question (2 days)

**Medium Priority (Subsequent):**
1. **Metacognitive training experiment** - Tests causality, but requires new data collection (6+ months)
2. **Finer-grained confidence scale** - Addresses gamma ceiling, requires new sample (3 months)
3. **Real-time confidence judgments** - Tests timing-dependent overconfidence (4 months)

**Lower Priority (Aspirational):**
1. **Clinical sample comparison (MCI patients)** - Requires clinical recruitment, IRB, specialized testing (12+ months)
2. **Personality correlates of calibration** - Interesting but outside core thesis scope (separate project)
3. **fMRI neural mechanisms** - Long-term collaboration, outside thesis timeline (1-2 years)

### Next Steps Summary

The findings establish **DISSOCIATION between metacognitive discrimination (gamma) and calibration bias**, raising three critical questions for immediate follow-up:

1. **Robustness:** Does Dunning-Kruger effect emerge with extreme groups (top/bottom 25%)? (Current data, 1 day)
2. **Domain-Specificity:** Is gamma-accuracy relationship stronger for specific memory domains? (Planned RQ 6.3.2, 1 week)
3. **Stability:** Is discrimination performance-dependence stable across forgetting trajectory? (Current data, 2 days)

Methodological extensions (finer confidence scale, metacognitive training, clinical samples) valuable but require new data collection beyond current thesis scope. Theoretical questions (causality, personality, task difficulty) suggest long-term research program extending thesis findings.

---

**End of Summary**

**Generated by:** rq_results agent (v4.0)
**Pipeline version:** v4.X (13-agent atomic architecture)
**Date:** 2025-12-11
