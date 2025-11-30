# Results Summary: RQ 5.2 - Differential Consolidation Across Memory Domains

**Research Question:** Do memory domains (What/Where/When) show different rates of forgetting during the early consolidation window (Day 0->1) versus later decay (Day 1->6)?

**Analysis Completed:** 2025-11-23

**Analyst:** rq_results agent (v4.0) with master claude orchestration

---

## 1. Statistical Findings

### Sample Characteristics

- **Total N:** 100 participants (UIDs)
- **Total Observations:** 1200 (100 participants x 4 test sessions x 3 domains)
- **Missing Data:** None detected (all expected rows present)
- **Segment Distribution:**
  - Early segment (Tests 1-2): 600 observations (50%)
  - Late segment (Tests 3-4): 600 observations (50%)

### Piecewise LMM Model Results

**Model Specification:**
- Formula: `theta ~ Days_within * Segment * domain`
- Random Effects: Random intercepts and slopes by UID
- Estimation: Maximum Likelihood (REML=False)
- Convergence: **Successful**

**Model Fit Statistics:**
- Log-likelihood: -1580.02
- AIC: 3192.05
- BIC: 3273.49
- Number of groups: 100
- Observations per group: 12

**Fixed Effects (12 terms):**

| Effect | Coef. | SE | z | p-value | 95% CI |
|--------|-------|-----|---|---------|--------|
| Intercept | 0.701 | 0.095 | 7.40 | <0.001 | [0.515, 0.887] |
| Segment[Late] | -0.917 | 0.131 | -7.00 | <0.001 | [-1.173, -0.660] |
| Domain[When] | -0.456 | 0.117 | -3.89 | <0.001 | [-0.686, -0.226] |
| Domain[Where] | -0.022 | 0.117 | -0.19 | 0.848 | [-0.252, 0.207] |
| Segment[Late]:Domain[When] | 0.585 | 0.184 | 3.18 | 0.001 | [0.225, 0.946] |
| Segment[Late]:Domain[Where] | 0.193 | 0.184 | 1.05 | 0.294 | [-0.167, 0.553] |
| Days_within | -0.507 | 0.095 | -5.34 | <0.001 | [-0.693, -0.321] |
| Days_within:Segment[Late] | 0.476 | 0.101 | 4.70 | <0.001 | [0.277, 0.675] |
| Days_within:Domain[When] | 0.299 | 0.133 | 2.26 | 0.024 | [0.039, 0.559] |
| Days_within:Domain[Where] | 0.052 | 0.133 | 0.39 | 0.697 | [-0.208, 0.311] |
| Days_within:Segment[Late]:Domain[When] | -0.281 | 0.142 | -1.98 | 0.048 | [-0.559, -0.003] |
| Days_within:Segment[Late]:Domain[Where] | -0.127 | 0.142 | -0.90 | 0.370 | [-0.406, 0.151] |

**Random Effects Variance Components:**
- Participant intercepts: 0.204 (SD = 0.452)
- Participant slopes: 0.011 (SD = 0.106)
- Intercept-slope covariance: -0.009

### Segment-Domain Slopes (Theta Units per Day)

| Segment | Domain | Slope | SE | 95% CI |
|---------|--------|-------|-----|--------|
| Early | What | -0.507 | 0.095 | [-0.693, -0.321] |
| Early | Where | -0.456 | 0.095 | [-0.642, -0.269] |
| Early | When | -0.208 | 0.095 | [-0.395, -0.022] |
| Late | What | -0.031 | 0.038 | [-0.106, 0.044] |
| Late | Where | -0.107 | 0.038 | [-0.182, -0.032] |
| Late | When | -0.013 | 0.038 | [-0.088, 0.062] |

**Key Pattern:** All Early segment slopes are substantially steeper (more negative) than Late segment slopes, indicating rapid initial forgetting followed by slower decay.

### Planned Contrasts (Decision D068: Dual P-Values)

| Contrast | Beta | SE | z | p (uncorr.) | p (Bonf.) | Sig? |
|----------|------|-----|---|-------------|-----------|------|
| Where-What (Early) | 0.052 | 0.134 | 0.38 | 0.701 | 1.000 | No |
| When-What (Early) | 0.299 | 0.134 | 2.22 | 0.026 | 0.157 | No* |
| Where-What (Late) | -0.076 | 0.054 | -1.40 | 0.162 | 0.972 | No |
| When-What (Late) | 0.018 | 0.054 | 0.33 | 0.740 | 1.000 | No |
| Where Slope Change - What Slope Change | -0.127 | 0.145 | -0.88 | 0.380 | 1.000 | No |
| When Slope Change - What Slope Change | -0.281 | 0.145 | -1.94 | 0.053 | 0.315 | No |

**Note:** Bonferroni correction: alpha = 0.05/6 = 0.0083. *When-What (Early) is significant uncorrected (p=0.026) but not after Bonferroni correction (p=0.157).

### Consolidation Benefit Indices

| Domain | Early Slope | Late Slope | Benefit (Early-Late) | 95% CI | Rank |
|--------|-------------|------------|---------------------|--------|------|
| When | -0.208 | -0.013 | -0.195 | [-0.396, 0.006] | 1 (Best) |
| Where | -0.456 | -0.107 | -0.349 | [-0.550, -0.148] | 2 |
| What | -0.507 | -0.031 | -0.476 | [-0.677, -0.275] | 3 (Worst) |

**Interpretation:** Negative consolidation benefit = more forgetting in Early vs Late segment. When domain shows LEAST early forgetting (benefit closest to zero), What domain shows MOST early forgetting (most negative benefit).

### Effect Sizes (Cohen's f-squared)

| Effect | f-squared | Interpretation |
|--------|-----------|----------------|
| Segment[Late] | 0.041 | Small |
| Days_within | 0.024 | Small |
| Days_within:Segment[Late] | 0.018 | Negligible |
| Domain effects | <0.013 | Negligible |
| 3-way interactions | <0.004 | Negligible |

**Summary:** Main effects of segment and time are small but meaningful. Domain-specific effects and interactions are negligible to small.

---

## 2. Plot Descriptions

### Figure 1: Piecewise Forgetting Trajectory - Theta Scale

**Filename:** `plots/piecewise_trajectory_theta.png`
**Plot Type:** Line plot with piecewise fitted trajectories and observed data points

**Visual Description:**

The plot displays forgetting trajectories over time (TSVR hours, 0-150) for three memory domains with both observed means (points) and model-fitted lines.

- **X-axis:** Hours Since VR Encoding (TSVR): 0 to ~150 hours
- **Y-axis:** Memory Ability (Theta): -0.5 to 0.7

**Domain Trajectories:**

1. **What (red):** Starts highest at T1 (theta ~0.69), shows steep decline in Early segment (0-25 hours), then slower decline in Late segment. Ends at theta ~-0.35 by T4.

2. **Where (blue):** Starts at theta ~0.67, shows steep Early decline similar to What, but crosses over What in the Late segment. Ends LOWEST at theta ~-0.48 by T4.

3. **When (green):** Starts LOWEST at theta ~0.20, shows shallowest Early decline, nearly flat in Late segment. Ends at theta ~-0.10 by T4.

**Key Visual Patterns:**

1. All domains show characteristic piecewise forgetting: steep decline 0-25 hours (consolidation window), then flatter slope afterward.
2. The domain trajectories CROSS: What and Where start similar and high, When starts low. By T4, What and Where are lowest, When is highest.
3. When domain shows most stability (shallowest overall decline).
4. Where domain shows continued decline in Late segment (visible downward slope), unlike What and When which flatten.

**Annotation:** "Early: Day 0-1 (consolidation) | Late: Day 1-6 (decay)"

### Figure 2: Piecewise Forgetting Trajectory - Probability Scale

**Filename:** `plots/piecewise_trajectory_probability.png`
**Plot Type:** Line plot with probability-transformed trajectories (Decision D069 compliance)

**Visual Description:**

- **X-axis:** Hours Since VR Encoding (TSVR): 0 to ~150 hours
- **Y-axis:** Probability Correct (%): 0 to 100%

**Domain Trajectories (Probability Scale):**

1. **What (red):** Starts at ~65%, declines to ~42% by T4. 23 percentage point decline.
2. **Where (blue):** Starts at ~65%, declines to ~40% by T4. 25 percentage point decline.
3. **When (green):** Starts at ~55%, declines to ~47% by T4. 8 percentage point decline.

**Practical Interpretation:**
- What and Where show substantial declines (23-25 percentage points over 6 days)
- When shows minimal decline (8 percentage points), remaining relatively stable
- By Day 6, all domains converge toward 40-47% probability correct (approaching chance level for difficult items)

**Annotation:** "Decision D069: Dual-scale for interpretability"

**Connection to Findings:**

Both plots confirm the statistical finding that When domain shows shallowest forgetting slope (especially in Early segment). The theta-scale plot is more sensitive to trajectory differences, while the probability-scale plot shows practical performance implications.

---

## 3. Interpretation

### Hypothesis Testing

**Original Hypothesis (from 1_concept.md):**
"Sleep-dependent consolidation (Day 0->1, including one night's sleep) may benefit spatial memory (Where) more than semantic (What), based on hippocampal replay theories."

**Hypothesis Status: NOT SUPPORTED**

The results do NOT support the hypothesis. Contrary to predictions:

1. **Where domain did NOT show the least early forgetting.** Where showed intermediate consolidation benefit (rank 2), not the best.

2. **When domain showed the LEAST early forgetting** (rank 1, smallest consolidation benefit magnitude), which was NOT predicted.

3. **No planned contrasts were significant after Bonferroni correction** (alpha = 0.0083). The 3-way interactions were not significant.

4. **When-What (Early) contrast** was marginally significant uncorrected (p=0.026) but not after correction (p=0.157).

### Dual-Scale Trajectory Interpretation (Decision D069)

**Theta Scale Findings:**

Memory ability declined across all domains, with Early segment slopes 3-20x steeper than Late segment slopes:
- What: Early slope = -0.51 SD/day, Late slope = -0.03 SD/day (17x steeper Early)
- Where: Early slope = -0.46 SD/day, Late slope = -0.11 SD/day (4x steeper Early)
- When: Early slope = -0.21 SD/day, Late slope = -0.01 SD/day (21x steeper Early)

**Statistical Interpretation:**

The two-phase forgetting pattern (steep then flat) is consistent with standard memory consolidation theory. However, domain differences in consolidation were minimal (all effect sizes negligible). The pattern suggests general consolidation rather than domain-specific consolidation.

**Probability Scale Findings:**

- What: 65% -> 42% (23 percentage point decline, T1 to T4)
- Where: 65% -> 40% (25 percentage point decline, T1 to T4)
- When: 55% -> 47% (8 percentage point decline, T1 to T4)

**Practical Interpretation:**

When domain shows remarkable stability (only 8 percentage point decline over 6 days), while What and Where show substantial declines approaching chance performance. This suggests temporal memory may be more resistant to forgetting than spatial or object memory in this VR paradigm - contrary to hippocampal replay predictions.

**Why Both Scales Matter:**
- **Theta:** Provides psychometrically rigorous comparison of slopes (-0.51 vs -0.21 SD/day is a meaningful difference)
- **Probability:** Shows practical impact - When domain remains at ~47% (above chance) while What and Where approach ~40-42% (near chance)

### Theoretical Contextualization

**Sleep Consolidation Theory (Rasch & Born, 2013):**

The finding that ALL domains show two-phase forgetting (steep Early, flat Late) is consistent with general consolidation theory. The first 24 hours post-encoding involve active consolidation processes that stabilize memories.

However, the domain-specific predictions based on hippocampal replay theory were NOT confirmed. Spatial memory (Where) did not show preferential consolidation benefit.

**Alternative Interpretation - When Domain Specificity:**

The unexpected stability of When (temporal) memory may reflect:

1. **Floor effect in initial encoding:** When domain started with lowest theta (0.20 vs 0.67-0.69), leaving less room for decline.

2. **Different encoding mechanism:** Temporal order may be encoded more semantically (gist-based) rather than episodically, making it less susceptible to consolidation-related changes.

3. **Measurement artifact:** When domain may have items with different psychometric properties (though RQ 5.1 purification should have controlled for this).

### Unexpected Patterns

**Anomaly 1: When Domain Most Consolidated (Not Where)**

- **Type:** Wrong direction (relative to hypothesis)
- **Description:** Hypothesis predicted Where > When for consolidation benefit. Results show When > Where > What.
- **Investigation suggestion:** Examine When domain item characteristics. Are When items semantically simpler? Check RQ 5.1 item parameters for domain-specific difficulty patterns.

**Anomaly 2: Where Shows Continued Late Decay**

- **Type:** Unexpected pattern
- **Description:** Where domain shows the steepest Late segment slope (-0.107/day), while What and When are nearly flat (-0.031 and -0.013/day). This suggests spatial memory continues forgetting after consolidation window, contrary to preservation hypothesis.
- **Investigation suggestion:** Examine whether Where domain has measurement floor effects or whether this reflects genuine spatial memory vulnerability over time.

**Note:** These unexpected patterns are flagged for investigation. Results from automated pipeline require manual verification before final acceptance.

### Broader Implications

**REMEMVR Validation:**

The piecewise LMM successfully detected the expected two-phase forgetting pattern, demonstrating REMEMVR's sensitivity to consolidation dynamics. However, domain-specific consolidation effects were smaller than anticipated.

**Methodological Insights:**

1. **Piecewise modeling effective:** The segmented approach (Early/Late) captures forgetting dynamics better than linear models, with clear slope differences between phases.

2. **Effect sizes small:** Domain-specific consolidation differences have negligible effect sizes (f-squared < 0.005), suggesting limited practical importance even if statistically significant.

3. **Bonferroni correction matters:** Without correction, When-What (Early) appears significant (p=0.026). With correction, no effects survive (p=0.157). This highlights the importance of multiple comparison correction.

---

## 4. Limitations

### Sample Limitations

**Sample Size:**
- N=100 provides adequate power for medium effects but may be underpowered for the small effects observed here (f-squared < 0.02)
- Power analysis for detecting small effects (f-squared = 0.02) at alpha=0.0083 suggests ~200+ participants needed

**Demographic Constraints:**
- Sample characteristics inherited from RQ 5.1 (university sample, predominantly young adults)
- Limited generalizability to older adults or clinical populations with altered consolidation

### Methodological Limitations

**Piecewise Structure:**
- Segment boundary fixed at ~24 hours based on theory, but optimal boundary not empirically determined
- Alternative segment definitions (e.g., Day 0-2 vs Day 2-6) not tested

**Design:**
- No sleep measurement: Cannot confirm actual sleep quality/duration during consolidation window
- Practice effects: Repeated testing may confound consolidation effects
- No control condition for non-sleep-related forgetting

**Statistical:**
- Simple piecewise structure assumes linear forgetting within segments (no exponential/logarithmic curves tested)
- Random slopes assume linear individual differences (no random quadratic terms)
- Effect sizes computed as f-squared (Cohen's d equivalents not computed for contrasts)

### Technical Limitations

**Log Warnings (Documented in Execution):**
- Initial code versions encountered errors (test value mapping, attribute access) that were fixed during execution
- Final runs passed all validation checks

**IRT Transformation Assumptions (Decision D069):**
- Probability scale uses mean item discrimination (a=0.9385) and fixed difficulty (b=0)
- Domain-specific item parameters not used for transformation (simplification may affect precision)

**TSVR Variable (Decision D070):**
- Days_within computed from actual TSVR hours, not nominal days
- Some variation in actual test timing (e.g., Late segment Days_within ranges 0-7.7 days, slightly beyond expected 0-5 days)

### Generalizability Constraints

**Population:**
- Young adult university sample limits generalizability to:
  - Older adults (who may show different consolidation patterns)
  - Clinical populations (e.g., sleep disorders, cognitive impairment)

**Context:**
- VR paradigm-specific findings may not generalize to real-world episodic memory
- Desktop VR (not fully immersive HMD) may affect encoding depth

**Note:** This analysis used automated pipeline (13 agents, v4.X architecture). Results validated for technical correctness (rq_inspect) and scientific plausibility (rq_results), but require human expert review before publication.

---

## 5. Next Steps

### Immediate Follow-Ups

**1. Investigate When Domain Floor Effect:**
- **Why:** When domain started with lowest theta, possibly limiting decline magnitude
- **How:** Examine RQ 5.1 theta score distributions by domain at T1
- **Timeline:** Immediate (data available)

**2. Test Alternative Segment Boundaries:**
- **Why:** 24-hour boundary is theory-driven but not empirically validated
- **How:** Re-run piecewise LMM with Day 0-2/Day 2-6 segmentation
- **Timeline:** 1-2 days (requires code modification)

**3. Examine Item-Level Patterns by Domain:**
- **Why:** Domain differences may be driven by specific items, not domain-level processes
- **How:** Cross-reference with RQ 5.1 item parameters, identify problematic items per domain
- **Timeline:** 1 day (data available)

### Planned Future RQs

**RQ 5.3 (Planned):**
- Focus on confidence-accuracy relationships across retention intervals
- May provide insight into metacognitive awareness of consolidation

**RQ 5.4+ (Planned):**
- Individual difference moderators (age, sleep quality proxies)
- May explain heterogeneity in consolidation benefit

### Methodological Extensions

**1. Nonlinear Piecewise Models:**
- Test exponential/power forgetting functions within segments
- May better capture consolidation dynamics

**2. Sleep Quality Covariates:**
- If sleep quality data available, include as moderator
- Would strengthen consolidation interpretation

**3. Alternative Effect Size Metrics:**
- Compute Cohen's d for specific contrasts
- More interpretable for comparing to literature

### Theoretical Questions Raised

**1. Why is Temporal Memory Most Stable?**
- Contradicts hippocampal replay predictions
- May reflect encoding mechanism differences (semantic vs episodic)
- Requires targeted investigation of When domain encoding

**2. Why Does Spatial Memory Continue Declining?**
- Where domain shows steepest Late slope
- May indicate spatial memory vulnerability rather than consolidation protection
- Requires comparison with non-VR spatial memory paradigms

---

**Summary generated by:** rq_results agent (v4.0)
**Pipeline version:** v4.X (13-agent atomic architecture)
**Date:** 2025-11-23
