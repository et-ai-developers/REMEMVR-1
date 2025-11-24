# Results Summary: RQ 5.4 - Linear Trend in Forgetting Rate Across Paradigms

**Research Question:** Does forgetting rate decrease monotonically from Free Recall -> Cued Recall -> Recognition, consistent with an ordered retrieval support gradient?

**Analysis Completed:** 2025-11-24

**Analyst:** rq_results agent (v4.0) with master claude orchestration

---

## 1. Statistical Findings

### Sample Characteristics

- **Total N:** 100 participants (inherited from RQ 5.3)
- **Total Observations:** 1,200 (100 participants x 4 tests x 3 paradigms)
- **Missing Data:** None (complete cases from RQ 5.3)
- **Model Source:** Log model from RQ 5.3 (best AIC = 2346.60)

### Dependency Verification

This secondary analysis used outputs from RQ 5.3:
- LMM fitted model (step05_lmm_fitted_model.pkl) - Log model with paradigm x time interactions
- LMM input data (step04_lmm_input.csv) - 1,200 observations with theta scores by paradigm
- All dependency files loaded successfully with model convergence confirmed

### Paradigm-Specific Forgetting Slopes

Forgetting rates (slopes) from the Log model evaluated at Day 3 midpoint:

| Paradigm | Slope | Interpretation |
|----------|-------|----------------|
| Free Recall | -0.470 | Slowest forgetting (least negative) |
| Cued Recall | -0.520 | Intermediate forgetting |
| Recognition | -0.597 | Fastest forgetting (most negative) |

**Note:** More negative slope = faster forgetting (theta decreases more rapidly over time).

### Marginal Means at Day 3

| Paradigm | Marginal Mean | SE | 95% CI |
|----------|---------------|-----|--------|
| Free Recall | 0.013 | 0.065 | [-0.115, 0.141] |
| Cued Recall | -0.019 | 0.065 | [-0.148, 0.109] |
| Recognition | 0.083 | 0.065 | [-0.045, 0.211] |

### Primary Result: Linear Trend Contrast

| Statistic | Value |
|-----------|-------|
| Contrast Estimate (b) | -0.127 |
| Standard Error | 0.052 |
| z-value | -2.47 |
| p-value (uncorrected) | 0.013 |
| p-value (Bonferroni, n=15) | 0.200 |
| 95% CI | [-0.228, -0.026] |
| Significant (uncorrected) | Yes (p < 0.05) |
| Significant (Bonferroni) | No (p > 0.05) |

**Contrast Weights:** Free Recall = -1, Cued Recall = 0, Recognition = +1

**Decision D068 Compliance:** Both uncorrected and Bonferroni-corrected p-values reported as required.

---

## 2. Plot Descriptions

### Figure 1: Paradigm Forgetting Rates Bar Plot

**Filename:** `plots/paradigm_forgetting_rates.png`

**Plot Type:** Bar plot with error bars and linear trend line overlay

**Visual Description:**

The plot displays marginal mean theta values at Day 3 for three retrieval paradigms ordered by retrieval support (Free Recall -> Cued Recall -> Recognition):

- **X-axis:** Retrieval Paradigm (ordered: Free Recall, Cued Recall, Recognition)
- **Y-axis:** Marginal Mean Theta (Day 3) ranging from approximately -0.2 to 0.3
- **Bars:** Color-coded by paradigm (red = Free Recall, blue = Cued Recall, green = Recognition)
- **Error bars:** 95% confidence intervals (substantial overlap visible across all three paradigms)
- **Dashed line:** Linear trend overlay (descending from left to right)
- **Subtitle annotation:** "Linear trend: b = -0.127, z = -2.47, p = 0.01"

**Key Visual Patterns:**

1. **Bar heights:** Recognition shows highest marginal mean (0.083), Free Recall intermediate (0.013), Cued Recall lowest (-0.019)
2. **Trend line direction:** Descending from Free Recall to Recognition (negative slope)
3. **Error bar overlap:** Substantial overlap among all three paradigms - consistent with non-significant Bonferroni-corrected result
4. **Non-monotonic pattern:** Cued Recall is LOWER than Free Recall, breaking expected monotonic ordering

**Connection to Findings:**

- The descending trend line visually confirms the negative linear contrast estimate (b = -0.127)
- Overlapping confidence intervals align with Bonferroni-corrected p = 0.20 (not significant)
- The pattern shows Recognition with highest memory at Day 3 but FASTEST forgetting rate

---

## 3. Interpretation

### Hypothesis Testing

**Original Hypothesis (from 1_concept.md):**
"Forgetting rate (slope magnitude) follows ordered trend: Free > Cued > Recognition. More negative slope = faster forgetting. Paradigms should lie on a monotonic continuum."

**Hypothesis Status:** **NOT SUPPORTED - OPPOSITE DIRECTION FOUND**

The linear trend contrast is significant at uncorrected alpha (p = 0.013) but NOT significant after Bonferroni correction (p = 0.20). More critically, the direction of the effect is OPPOSITE to theoretical prediction:

- **Predicted:** Forgetting rate decreases with more retrieval support (positive trend)
- **Observed:** Forgetting rate INCREASES with more retrieval support (negative trend, b = -0.127)

### Unexpected Patterns

**ANOMALY 1: Reversed Effect Direction (FLAGGED FOR INVESTIGATION)**

- **Type:** Wrong direction
- **Description:** The retrieval support gradient hypothesis predicted that paradigms with more retrieval support (Recognition > Cued > Free) would show SLOWER forgetting. Instead, Recognition shows the FASTEST forgetting (slope = -0.597) while Free Recall shows the SLOWEST forgetting (slope = -0.470).
- **Investigation Suggestions:**
  1. Examine ceiling effects in Recognition paradigm - if recognition performance starts near ceiling at Day 0, there is more room to decline
  2. Check RQ 5.3 trajectory plots for paradigm-specific ceiling effects
  3. Consider encoding-retrieval specificity - Free Recall at encoding may create more durable traces
  4. Investigate testing effect - repeated retrieval may benefit Free Recall more than Recognition
  5. Review item difficulty - Recognition items may be harder to retain despite easier retrieval cues

**ANOMALY 2: Non-Monotonic Pattern in Marginal Means**

- **Type:** Unexpected pattern
- **Description:** Marginal means at Day 3 show non-monotonic ordering: Recognition (0.083) > Free Recall (0.013) > Cued Recall (-0.019). Cued Recall is BELOW Free Recall, contradicting simple retrieval support gradient.
- **Investigation Suggestions:**
  1. This may reflect floor effects in Cued Recall combined with ceiling effects in Recognition
  2. Check participant-level heterogeneity in paradigm performance
  3. Examine whether specific item types drive Cued Recall disadvantage

### Theoretical Contextualization

**Retrieval Support Gradient Theory Challenge:**

The traditional retrieval support gradient (Tulving & Thomson, 1973) predicts better retention with more retrieval cues. However, forgetting RATE is not equivalent to retention level. Our findings suggest:

1. **Retrieval mode effect:** Free Recall may engage deeper retrieval processing that strengthens memory traces (testing effect literature: Roediger & Karpicke, 2006)
2. **Encoding specificity:** Free Recall during test 1 may create retrieval-strengthened traces absent in Recognition
3. **Ceiling compression:** Recognition starts higher but has compressed range for decline detection

**Literature Connections (from rq_scholar validation):**

- Rosenthal & Rosnow (1985): Linear trend methodology appropriate for ordered factors
- Maxwell & Delaney (2004): Polynomial contrasts provide focused test of ordering hypothesis
- rq_scholar noted (9.4/10): "Theory excellent (encoding-retrieval specificity, polynomial contrasts). Suggest acknowledging ceiling effects in recognition paradigm."

The scholar validation explicitly warned about ceiling effects - this appears prescient given the observed pattern.

### Statistical Significance vs. Practical Significance

The uncorrected p-value (0.013) suggests evidence for a linear trend, but:
- Bonferroni correction eliminates significance (p = 0.20)
- Effect size is modest (b = -0.127 on theta scale)
- Direction contradicts theory, suggesting the finding may reflect methodological artifacts rather than genuine cognitive mechanism

### Broader Implications

**For REMEMVR Assessment:**
- Different paradigms show different forgetting dynamics
- Cannot assume retrieval support uniformly benefits retention over time
- May need to consider paradigm-specific interpretive frameworks

**Methodological Insights:**
- Testing linear trends is more powerful than pairwise comparisons (1 df vs 2+ df)
- However, directional prediction failure suggests theoretical model needs revision
- Ceiling/floor effects should be examined before interpreting slope differences

---

## 4. Limitations

### Sample Limitations

- **Inherited from RQ 5.3:** N = 100 university undergraduates
- **Demographic restriction:** Young adult sample (M age ~20) limits generalizability
- **No subsample analyses:** Individual difference moderators not examined

### Methodological Limitations

**Design:**
1. **Ceiling effects in Recognition:** rq_scholar explicitly warned about this. Recognition may start near ceiling, artificially increasing slope magnitude.
2. **Floor effects in Cued Recall:** Observed Cued Recall marginal mean (-0.019) near zero suggests floor compression.
3. **Testing effects confound:** Repeated retrieval may differentially benefit paradigms.

**Statistical:**
1. **N = 3 paradigms for trend:** Linear trend tested on only 3 points - sensitive to any single paradigm deviation.
2. **Within-LMM contrast:** Preserves full information but assumes Log model is correct specification.
3. **Multiple comparison burden:** Bonferroni correction for n=15 tests across thesis may be overly conservative.

### Technical Limitations

**Secondary Analysis Constraints:**
- Depends entirely on RQ 5.3 model quality
- Cannot re-examine model specification choices
- Inherits any RQ 5.3 limitations (see RQ 5.3 summary.md)

**Slope Interpretation:**
- Slopes evaluated at Day 3 midpoint (log(3) = 1.099)
- Different evaluation points might yield different patterns
- Log model slopes are instantaneous rates, not average slopes

**Decision Dependencies:**
- D070 (TSVR): Analysis uses log-transformed time (inherited from RQ 5.3)
- D068 (dual p-values): Bonferroni correction applied with n=15 tests

### Generalizability Constraints

- Findings specific to REMEMVR VR paradigm
- Three paradigms may not generalize to other retrieval task variants
- University sample limits extension to clinical populations

### Plausibility Concerns

**Technical Limitations flagged:**
- Direction of effect OPPOSITE to theoretical prediction (see Anomaly 1)
- Non-monotonic pattern in marginal means (see Anomaly 2)
- Results from automated pipeline require human expert review before publication

---

## 5. Next Steps

### Immediate Follow-Ups

**1. Ceiling Effect Analysis (HIGH PRIORITY):**
- Examine Day 0 performance distributions by paradigm
- If Recognition starts > 90%, ceiling compression explains faster apparent forgetting
- Can use RQ 5.3 theta_scores data

**2. Individual Differences in Paradigm Effects:**
- Extract participant-specific paradigm slopes from RQ 5.3 random effects
- Identify whether pattern holds uniformly or driven by subgroups

**3. Alternative Evaluation Points:**
- Re-compute marginal means at Day 1, Day 6 (not just Day 3)
- Test if pattern reverses at different time points

### Planned Future RQs

**Chapter 5 Continuation:**
- RQ 5.4 completes the paradigm analysis sequence (5.3 trajectories -> 5.4 linear trend)
- Results inform interpretation but do not block subsequent RQs

**Related Analyses:**
- Chapter 6 may examine domain x paradigm interactions
- Testing effect analyses could use multi-session data

### Methodological Extensions

**1. Quadratic Trend Test:**
- Add quadratic contrast weights [+1, -2, +1]
- May detect U-shaped pattern (Cued Recall lowest)

**2. Bayesian Reanalysis:**
- Compute Bayes Factor for linear trend
- Better quantify evidence for/against hypothesis

**3. Ceiling Effect Adjustment:**
- Consider beta regression for bounded outcomes
- May correct for range restriction artifacts

### Theoretical Questions

**1. Testing Effect Magnitude:**
- How much does repeated retrieval during test sessions drive Free Recall advantage?
- Would spaced vs. massed testing alter paradigm ordering?

**2. Encoding-Retrieval Interaction:**
- Do encoding processes differ by anticipated retrieval type?
- VR encoding may favor self-generated retrieval (Free Recall)

**3. Retrieval Support Reconceptualization:**
- Is retrieval support gradient about accuracy or retention?
- May need to distinguish level vs. rate measures

### Priority Ranking

**High Priority:**
1. Ceiling effect analysis (explains anomaly)
2. Alternative evaluation point analysis

**Medium Priority:**
1. Individual difference clustering
2. Quadratic trend test

**Lower Priority:**
1. Bayesian reanalysis
2. Beta regression modeling

---

## Summary Statement

RQ 5.4 tested whether forgetting rates follow a linear trend consistent with retrieval support gradient theory (Free > Cued > Recognition). The linear trend contrast was significant at uncorrected alpha (b = -0.127, z = -2.47, p = 0.01) but NOT significant after Bonferroni correction (p = 0.20). **Critically, the observed direction was OPPOSITE to prediction:** Recognition showed fastest forgetting despite providing most retrieval support. This counter-intuitive finding likely reflects ceiling effects in Recognition performance, as explicitly warned by rq_scholar during validation. The hypothesis is not supported, and alternative explanations (ceiling compression, testing effects) should be investigated before drawing theoretical conclusions.

---

**Summary generated by:** rq_results agent (v4.0)

**Pipeline version:** v4.X (13-agent atomic architecture)

**Date:** 2025-11-24

**Anomaly Count:** 2 (1 wrong direction, 1 unexpected pattern)

**Plausibility Assessment:** Results technically valid but theoretically unexpected - ceiling effect investigation recommended before interpretation.
