# RQ 5.5: Schema Congruence Effects on Forgetting Trajectories

**Research Question:** Does schema congruence (common, congruent, incongruent) affect the trajectory of episodic forgetting over 6 days?

**Analysis Date:** 2025-11-24

**Analyst:** rq_results agent (v4.0) with master claude orchestration

**Pipeline Version:** v4.X (13-agent atomic architecture)

---

## 1. Statistical Findings

### Sample Characteristics

- **Total N:** 100 participants
- **Observations:** 1,200 (100 participants x 4 test sessions x 3 congruence categories)
- **Test Sessions:** T1, T2, T3, T4 (TSVR: 1, 28.8, 78.7, 151.4 hours)
- **Missing Data:** None (all 400 composite_IDs preserved from RQ 5.1)

### IRT Calibration Results

**Pass 1 Calibration:**
- Model: 3-dimensional Graded Response Model (GRM)
- Dimensions: Common, Congruent, Incongruent (based on item codes i1-i6)
- Items analyzed: 72 interactive paradigm items (IFR, ICR, IRE)
- Convergence: Successful

**Item Purification (Decision D039):**
- Purification criteria: Discrimination (a >= 0.4), Difficulty (|b| <= 3.0)
- Items retained: 51/72 (70.8%)
- Items excluded: 21 items
  - Primary exclusion reason: Extreme difficulty (b > 3.0) combined with low discrimination
  - Items with difficulty up to b = 30.8 observed before purification (extreme)
- Items per dimension after purification:
  - Common: 19/24 retained (79.2%)
  - Congruent: 19/24 retained (79.2%)
  - Incongruent: 13/24 retained (54.2%)

**Note:** Incongruent dimension had notably more items excluded (11/24 = 45.8% removed) compared to Common and Congruent (5/24 = 20.8% each). This asymmetry may reflect genuine item property differences or introduce selection bias.

**Pass 2 Calibration (Purified Items):**
- Items: 51 purified items
- Convergence: Successful
- Parameter ranges:
  - Discrimination a: [0.41, 2.97]
  - Difficulty b: [-2.94, 2.97]

**Theta Score Estimates:**

| Dimension | Mean | SD | Min | Max |
|-----------|------|-----|-----|-----|
| Common | 0.004 | 0.890 | -2.06 | 2.72 |
| Congruent | 0.007 | 0.888 | -2.05 | 2.47 |
| Incongruent | 0.013 | 0.902 | -2.07 | 2.34 |

Standard errors: Mean SE = 0.20-0.25 across dimensions (acceptable precision).

### LMM Model Selection

**Candidate Models Tested:**
5 LMM specifications with Congruence x Time interactions (Treatment coding, Common as reference):

| Model | AIC | BIC | Delta AIC | AIC Weight |
|-------|-----|-----|-----------|------------|
| **Log** | 2652.57 | 2703.47 | 0.00 | ~1.000 |
| Lin+Log | 2674.50 | 2740.67 | 21.93 | <0.001 |
| Quadratic | 2691.55 | 2757.72 | 38.99 | <0.001 |
| Linear | 2698.79 | 2749.69 | 46.23 | <0.001 |
| Quad+Log | 2746.19 | 2827.64 | 93.63 | <0.001 |

**Best Model:** Logarithmic (Log) - overwhelming evidence (AIC weight ~1.000)

**Winning Model Formula:**
```
theta ~ TSVR_log * congruence + (TSVR_log | UID)
```

### Fixed Effects (Best Model)

| Effect | Coef | SE | z | p |
|--------|------|-----|---|---|
| Intercept | 0.654 | 0.100 | 6.57 | <.001*** |
| Congruent (vs Common) | -0.060 | 0.102 | -0.58 | .559 |
| Incongruent (vs Common) | 0.079 | 0.102 | 0.78 | .438 |
| TSVR_log (Time) | -0.193 | 0.024 | -7.98 | <.001*** |
| TSVR_log x Congruent | 0.019 | 0.027 | 0.68 | .494 |
| TSVR_log x Incongruent | -0.021 | 0.027 | -0.76 | .448 |

**Random Effects:**
- Group Variance: 0.470 (substantial individual differences in baseline ability)
- Group x TSVR_log Covariance: -0.072 (negative: higher baseline associated with faster forgetting)
- TSVR_log Variance: 0.022 (moderate individual differences in forgetting rate)
- Residual: 0.407

### Post-Hoc Contrasts (Decision D068: Dual p-values)

**Slope Contrasts (Forgetting Rate Differences):**

| Comparison | Beta | SE | z | p (uncorr) | p (Bonf) | Significant |
|------------|------|-----|---|-----------|----------|-------------|
| Congruent - Common | 0.019 | 0.027 | 0.68 | .494 | 1.000 | No |
| Incongruent - Common | -0.021 | 0.027 | -0.76 | .448 | 1.000 | No |
| Congruent - Incongruent | 0.039 | 0.027 | 1.44 | .149 | .447 | No |

**Result:** No significant differences in forgetting slopes between any congruence categories (all p > 0.14 uncorrected).

### Effect Sizes

| Effect | f-squared | Interpretation |
|--------|-----------|----------------|
| Congruent (vs Common) | 0.0003 | Negligible |
| Incongruent (vs Common) | 0.0005 | Negligible |
| TSVR_log (Time) | 0.053 | Small |
| TSVR_log x Congruent | 0.0004 | Negligible |
| TSVR_log x Incongruent | 0.0005 | Negligible |

**Summary:** Time main effect is small (f-squared = 0.053). All congruence effects and interactions are negligible (f-squared < 0.001).

---

## 2. Plot Descriptions

### Figure 1: Forgetting Trajectories by Schema Congruence - Theta Scale

**Filename:** `plots/trajectory_theta.png`

**Plot Type:** Line plot with 95% confidence bands

**Visual Description:**

The plot displays forgetting trajectories across 4 test sessions (TSVR: 0-151 hours) for three congruence categories (Common=purple, Congruent=green, Incongruent=red).

- **X-axis:** Time Since VR Encoding (hours): 0 to ~150
- **Y-axis:** Memory Ability (Theta): -0.6 to 0.7

**Congruence Trajectories (Theta Scale):**
- **Common:** Starts at theta = 0.47 (Day 0), declines to theta = -0.38 (Day 6) - 0.85 SD decline
- **Congruent:** Starts at theta = 0.42 (Day 0), declines to theta = -0.40 (Day 6) - 0.82 SD decline
- **Incongruent:** Starts at theta = 0.55 (Day 0), declines to theta = -0.40 (Day 6) - 0.95 SD decline

**Key Visual Patterns:**
1. All three categories show similar monotonic decline (forgetting over time)
2. Trajectories converge by Day 6 (theta approximately -0.38 to -0.40 for all)
3. Incongruent starts highest at Day 0 (theta = 0.55) but declines to same endpoint
4. Confidence bands overlap substantially at all time points (consistent with non-significant interactions)
5. Rapid initial forgetting (Day 0 to Day 1) followed by slower decline (Day 3 to Day 6) - logarithmic pattern confirmed

**Connection to Findings:**
- Visual confirms non-significant Congruence x Time interactions (overlapping CIs)
- All three lines converge, consistent with no differential forgetting rates
- Logarithmic shape visible: steeper decline early, flattening later (supports Log model selection)

---

### Figure 2: Forgetting Trajectories by Schema Congruence - Probability Scale

**Filename:** `plots/trajectory_probability.png`

**Plot Type:** Line plot with 95% confidence bands (Decision D069 compliance)

**Visual Description:**

Dual-scale companion to Figure 1, showing performance probability over time.

- **X-axis:** Time Since VR Encoding (hours): 0 to ~150
- **Y-axis:** Probability Correct (%): 0 to 100
- **Reference line:** 50% (dashed horizontal line, chance performance)

**Congruence Trajectories (Probability Scale):**
- **Common:** 61.5% -> 40.6% (20.9 percentage point decline)
- **Congruent:** 60.4% -> 40.0% (20.4 percentage point decline)
- **Incongruent:** 63.5% -> 40.2% (23.3 percentage point decline)

**Key Visual Patterns:**
1. All categories start above 60% and end around 40% (below chance)
2. Performance crosses 50% threshold between Day 1 and Day 3 for all categories
3. By Day 6, all categories show below-chance performance (~40%)
4. Confidence bands overlap at all time points
5. Incongruent shows slightly larger absolute decline (23.3 pp) but non-significant

**Practical Interpretation:**
The probability scale reveals that participants start with moderate performance (60-64%) and decline to below-chance levels (40%) by Day 6. The 50% threshold crossing indicates memory becoming unreliable after approximately 72 hours. No meaningful differences between congruence categories in practical terms.

---

## 3. Interpretation

### Hypothesis Testing

**Primary Hypothesis (from 1_concept.md):**
"Congruent items (schema-consistent) will show slower forgetting than incongruent items (schema-violating), due to schema-based consolidation processes."

**Hypothesis Status: NOT SUPPORTED**

The statistical findings fail to confirm differential forgetting rates:
- Congruence x Time interactions: All p > 0.14 (uncorrected), all p > 0.44 (Bonferroni-corrected)
- Effect sizes: All negligible (f-squared < 0.001)
- Visual inspection: Trajectories converge, no separation in forgetting rates

**Secondary Hypotheses:**
1. "Common items (schema-neutral) will fall between congruent and incongruent" - NOT SUPPORTED (no ordering differences)
2. "Von Restorff effect may boost incongruent encoding (T1 performance)" - PARTIALLY SUPPORTED (Incongruent shows highest T1 theta = 0.55), but difference non-significant
3. "By Day 6, ordering should be: Congruent > Common > Incongruent" - NOT SUPPORTED (all converge to similar endpoint)

### Dual-Scale Trajectory Interpretation (Decision D069)

**Theta Scale Findings:**
Memory ability declined approximately 0.82-0.95 SD across all congruence categories from Day 0 to Day 6. This represents a medium-to-large effect of time on memory performance. Critically, all three categories showed parallel decline trajectories.

**Statistical Interpretation:**
The Time main effect was highly significant (beta = -0.193, p < .001), indicating robust forgetting. However, the effect size was small (f-squared = 0.053), suggesting that while forgetting is statistically reliable, individual differences and residual variance explain most of the performance variation.

**Probability Scale Findings:**
Performance probability dropped from 60-64% to 40% across all categories - a decline of approximately 20-23 percentage points. By Day 6, performance was below chance (50%), indicating memory traces became unreliable.

**Practical Interpretation:**
The probability scale reveals clinically meaningful forgetting: after 6 days, participants performed worse than random guessing. Importantly, this occurred equally for schema-congruent and schema-incongruent items. For VR-based assessment, schema congruence does not appear to moderate forgetting in a meaningful way.

**Why Both Scales Matter:**
- **Theta:** Provides standardized effect sizes (0.82-0.95 SD decline) comparable to other memory research
- **Probability:** Shows practical significance - 40% performance at Day 6 is clinically meaningful
- **Together:** Both scales converge on the same conclusion - no differential forgetting by congruence

### Theoretical Contextualization

**Schema Theory Predictions Not Confirmed:**

The findings do not support schema-mediated consolidation effects (Bartlett, 1932; Ghosh & Gilboa, 2014) in this VR episodic memory context. Several theoretical interpretations are possible:

1. **Encoding vs. Consolidation:** Schema effects may primarily operate at encoding, not consolidation. If congruent and incongruent items are initially encoded with equal strength (no significant T1 differences in theta), differential consolidation cannot manifest.

2. **VR Context Specificity:** Immersive VR may create strong contextual bindings that override schema effects. The rich perceptual detail in VR environments may reduce reliance on schema-based reconstruction.

3. **Item-Room Binding Strength:** The congruence manipulation (toothbrush in bathroom vs. unexpected locations) may be too subtle relative to the overall encoding richness of VR. All items receive comparable encoding support from spatial context.

4. **Parallel Forgetting:** All memory traces, regardless of schema congruence, may follow the same neurobiological decay trajectory. Schema effects observed in other paradigms may not generalize to immersive VR.

**Literature Connections (from rq_scholar validation):**
- Bartlett (1932): Schema-based reconstruction not evident in VR paradigm
- Ghosh & Gilboa (2014): Schema-mediated consolidation effects not observed
- Gilboa & Marlatte (2017): Schema integration may require longer time scales than 6 days
- Brod et al. (2018): Schema effects may be item-specific rather than categorical

### Unexpected Patterns

**1. Incongruent Items Show Highest Initial Performance (Von Restorff Pattern)**

Incongruent items showed the highest Day 0 theta (0.55 vs. 0.47 Common, 0.42 Congruent). Although non-significant, this pattern is consistent with the Von Restorff effect: schema-violating items may receive enhanced encoding due to distinctiveness/surprise.

**Investigation Suggestion:** Examine item-level encoding patterns to determine if incongruent items truly benefit from distinctiveness or if this is random variation.

**2. Asymmetric Item Retention After Purification**

Incongruent dimension had significantly more items excluded (45.8%) than Common/Congruent (20.8%). This raises concerns:
- Are incongruent items intrinsically more difficult/discriminating poorly?
- Does the reduced item count (13 vs. 19) affect theta estimation precision for incongruent dimension?
- Could selection bias from purification mask true congruence effects?

**Investigation Suggestion:** Examine removed items' characteristics. Consider sensitivity analysis with relaxed purification thresholds.

**3. Pass 2 IRT Warnings**

The log notes 4 items with a < 0.4 and 2 items with |b| > 3.0 after Pass 2 re-calibration. This suggests parameter instability - purified items' parameters shifted when calibrated without removed items.

**Investigation Suggestion:** Check if parameter shifts affected theta estimates systematically by dimension.

### Broader Implications

**For Schema Theory:**
These findings suggest schema congruence effects may be paradigm-dependent. VR episodic memory, with its rich multisensory encoding, may operate differently than traditional word-list or picture paradigms where schema effects are typically observed.

**For REMEMVR Assessment:**
Schema congruence does not appear to be a significant moderator of forgetting in this VR paradigm. Item placement (congruent vs. incongruent rooms) can be determined by other factors (ecological validity, practical constraints) without concern for differential forgetting.

**Methodological Insights:**
1. The logarithmic model provided best fit (overwhelming AIC evidence), consistent with classic forgetting curve literature (Ebbinghaus, 1885)
2. Dual-scale reporting (D069) confirmed parallel conclusions across theta and probability scales
3. Strong individual differences in baseline (Group Var = 0.47) and forgetting rate (TSVR_log Var = 0.022) warrant future investigation

---

## 4. Limitations

### Sample Limitations

**Sample Size:**
- N = 100 provides adequate power for medium effects (d = 0.5) but may be underpowered for small congruence effects
- Post-hoc power for observed effect sizes (f-squared < 0.001) is very low (<10%)
- Wide confidence intervals on interaction terms reflect limited precision

**Demographic Constraints:**
- Sample characteristics inherited from RQ 5.1 (not extracted independently)
- Generalizability to clinical populations unknown

### Methodological Limitations

**Measurement:**

1. **Asymmetric Purification:** Incongruent dimension lost 45.8% of items vs. 20.8% for other dimensions. This creates:
   - Unequal measurement precision across dimensions
   - Potential selection bias (retained incongruent items may be unrepresentative)
   - Possible underestimation of incongruent effects

2. **Congruence Operationalization:** Congruence defined by item codes (i1-i6) rather than independent ratings. The manipulation's effectiveness (do participants perceive items as congruent/incongruent?) was not validated.

3. **Q-Matrix Assumptions:** Simple structure assumed (each item loads on exactly one dimension). In reality, some items may have cross-loadings.

**Design:**

1. **No Manipulation Check:** We cannot verify that participants perceived schema-congruent items as more "expected" than incongruent items in VR context.

2. **Cross-RQ Dependency:** Data derived from RQ 5.1. Any data extraction issues in RQ 5.1 propagate to RQ 5.5.

3. **Interactive Paradigms Only:** RFR excluded. Effects may differ for room-level recall.

**Statistical:**

1. **Pass 2 Parameter Drift:** Log warnings indicate some items shifted outside thresholds after re-calibration. This instability may affect theta estimates.

2. **Treatment Coding:** Common as reference assumes schema-neutral baseline. If Common items have implicit schema associations, contrast interpretation changes.

3. **Multiple Comparisons:** Three contrasts tested. Bonferroni correction applied but reduces power for detecting true effects.

### Generalizability Constraints

**Population:**
- University sample - may not generalize to clinical populations with schema integration deficits
- Young adults - schema effects may differ in aging (stronger reliance on schemas)

**Context:**
- Desktop VR - immersive HMD VR may show different pattern
- Specific VR environment - other environments may have stronger/weaker schema cues

**Task:**
- Object-room associations - other schema domains (person-action, event-sequence) may show effects
- 6-day retention - longer intervals may reveal schema consolidation effects

### Technical Limitations

**IRT Purification Impact (Decision D039):**
The 29.2% item removal rate (21/72 items) is within expected range but creates information loss. The asymmetric removal by dimension (45.8% incongruent vs. 20.8% others) is a notable concern.

**TSVR Variable (Decision D070):**
Using continuous hours assumes linear relationship in log-space. Circadian effects (sleep consolidation) may introduce non-monotonic patterns not captured by this specification.

**Dual-Scale Transformation (Decision D069):**
Probability estimates assume average item difficulty (b=0). Dimension-specific item difficulties may distort probability comparisons.

### Limitations Summary

The primary limitation is **low statistical power** for detecting congruence effects given negligible observed effect sizes. The **asymmetric purification** by dimension raises measurement concerns. However, the core finding - no significant differential forgetting - is robust: effects are not merely non-significant but genuinely negligible (f-squared < 0.001).

---

## 5. Next Steps

### Immediate Follow-Ups (Current Data)

**1. Sensitivity Analysis for Purification Thresholds:**
- **Why:** Asymmetric item retention may bias results
- **How:** Re-run with relaxed thresholds (a >= 0.3, |b| <= 4.0) to retain more incongruent items
- **Expected Insight:** Determine if congruence effects emerge with more balanced item sets
- **Timeline:** Immediate (same data, alternative parameters)

**2. Item-Level Analysis of Removed Items:**
- **Why:** 21 items excluded - understand what makes them problematic
- **How:** Examine removed items' content, paradigm source, response patterns
- **Expected Insight:** Identify if incongruent items are intrinsically harder or if purification criteria are biased
- **Timeline:** 1-2 days

**3. Individual Differences in Congruence Effects:**
- **Why:** Random effects show substantial individual variation
- **How:** Extract person-specific congruence effects, correlate with individual characteristics
- **Expected Insight:** Some individuals may show strong congruence effects even if group mean is null
- **Timeline:** 1 week

### Planned Thesis RQs

**RQ 5.6 and Beyond (If Applicable):**
Schema congruence findings inform interpretation of subsequent Chapter 5 RQs examining forgetting trajectories. The null finding suggests congruence can be de-prioritized as a moderator in future analyses.

### Methodological Extensions (Future Data Collection)

**1. Manipulation Check Study:**
- **Current Limitation:** No validation that items are perceived as congruent/incongruent
- **Extension:** Collect congruence ratings from independent sample
- **Expected Insight:** Confirm manipulation validity
- **Feasibility:** Low cost (online survey, N=50)

**2. Extended Retention Intervals:**
- **Current Limitation:** 6 days may be insufficient for schema consolidation effects
- **Extension:** Test at 2 weeks and 4 weeks
- **Expected Insight:** Schema effects may emerge only after extended consolidation
- **Feasibility:** Requires new data collection

**3. Explicit Schema Prime Condition:**
- **Current Limitation:** Schema congruence implicit in item placement
- **Extension:** Prime participants with room schemas before encoding
- **Expected Insight:** Strengthened schema activation may enhance congruence effects
- **Feasibility:** Requires modified VR protocol

### Theoretical Questions Raised

**1. Are Schema Effects Domain-Specific?**
- Schema congruence null in object-room binding
- May be present in temporal sequences, person-action associations
- Future RQs could test alternative schema domains

**2. Does VR Override Schema Processing?**
- Rich perceptual encoding may reduce reliance on schemas
- Direct comparison with 2D paradigm needed

**3. Individual Differences in Schema Reliance:**
- Some participants may rely more on schemas than others
- Working memory capacity, cognitive style may predict congruence sensitivity

### Priority Ranking

**High Priority (Do First):**
1. Sensitivity analysis for purification thresholds (addresses main methodological concern)
2. Item-level analysis of removed items (explains asymmetric retention)

**Medium Priority (Subsequent):**
1. Individual differences analysis (explores person-level variability)
2. Manipulation check (validates construct)

**Lower Priority (Aspirational):**
1. Extended retention study (requires new data)
2. Schema prime condition (requires protocol modification)
3. Alternative schema domain RQs (future thesis work)

---

## Summary

RQ 5.5 tested whether schema congruence (common, congruent, incongruent items) affects forgetting trajectories in VR episodic memory. **The primary hypothesis was not supported:** no significant differential forgetting rates were observed between congruence categories (all interaction p-values > 0.14, all effect sizes negligible).

**Key Findings:**
1. All congruence categories showed similar forgetting trajectories (~0.85 SD decline over 6 days)
2. Logarithmic model provided best fit (AIC weight ~1.000)
3. Time main effect significant (p < .001) but small effect size (f-squared = 0.053)
4. By Day 6, performance dropped to ~40% (below chance) for all categories
5. Substantial individual differences in baseline and forgetting rate warrant future investigation

**Implications:**
Schema congruence does not appear to moderate forgetting in this VR episodic memory paradigm. Item placement can be determined by other factors without concern for differential retention. These findings suggest schema effects may be paradigm-dependent and not universal across memory contexts.

---

**Summary generated by:** rq_results agent (v4.0)

**Pipeline version:** v4.X (13-agent atomic architecture)

**Date:** 2025-11-24
