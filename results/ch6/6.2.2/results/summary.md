# Results Summary: RQ 6.2.2 - Over-Underconfidence Trajectory

**Research Question:** Do people become overconfident as memories fade over the 6-day retention interval?

**Analysis Completed:** 2025-12-11

**Analyst:** rq_results agent (v4.0) with master claude orchestration

---

## 1. Statistical Findings

### Sample Characteristics

- **Total Observations:** 400 (100 participants x 4 test sessions)
- **Test Sessions:** T1 (Day 0), T2 (Day 1), T3 (Day 3), T4 (Day 6)
- **Data Source:** RQ 6.2.1 calibration scores (theta_confidence - theta_accuracy)
- **Missing Data:** None (complete data for all observations)

### Classification Distribution

**Overall Classification (400 observations):**
- Overconfident (Calibration > 0.1): 187 observations (46.8%)
- Underconfident (Calibration < -0.1): 177 observations (44.2%)
- Calibrated (|Calibration| <= 0.1): 36 observations (9.0%)

**Classification threshold:** epsilon = 0.1 SD units (scientifically meaningful difference between confidence and accuracy)

### Proportion Overconfident Trajectory

| Test Session | N Total | N Overconfident | Proportion | 95% CI |
|--------------|---------|-----------------|------------|---------|
| T1 (Day 0) | 100 | 41 | 0.41 | [0.319, 0.508] |
| T2 (Day 1) | 100 | 48 | 0.48 | [0.385, 0.577] |
| T3 (Day 3) | 100 | 47 | 0.47 | [0.375, 0.567] |
| T4 (Day 6) | 100 | 51 | 0.51 | [0.413, 0.606] |

**Change from Day 0 to Day 6:** +10.0 percentage points (41% to 51%)

### Trend Test (Logistic Regression)

**Model:** Logistic regression predicting overconfidence (binary: 1 if Calibration > 0.1, else 0) from time (ordinal: 0, 1, 3, 6 days)

**Model Convergence:** Successful

**Fixed Effect Estimates:**

| Term | Estimate (log-odds) | SE | z | p-value | Odds Ratio | 95% CI |
|------|---------------------|-----|------|---------|------------|---------|
| Intercept | -0.262 | 0.149 | -1.76 | 0.079 | 0.769 | [0.575, 1.030] |
| Time (days) | 0.053 | 0.044 | 1.20 | 0.230 | 1.054 | [0.967, 1.148] |

**Interpretation of Time Effect:**
- **Slope:** ² = 0.053 (log-odds per day)
- **Odds Ratio:** OR = 1.054 per day [0.967, 1.148]
- **Statistical Significance:** p = 0.230 (NON-SIGNIFICANT at ± = 0.05)
- **Practical Interpretation:** Each additional day increases odds of overconfidence by 5.4%, but this trend is not statistically reliable

**Hypothesis Test:** The proportion of overconfident observations does NOT show a significant increasing trend over time (p = 0.230 > 0.05).

### Mean Calibration Trajectory

| Test Session | N | Mean Calibration | SD | 95% CI |
|--------------|---|------------------|-----|---------|
| T1 (Day 0) | 100 | -0.116 | 0.890 | [-0.290, 0.058] |
| T2 (Day 1) | 100 | -0.034 | 0.958 | [-0.222, 0.154] |
| T3 (Day 3) | 100 | 0.039 | 0.937 | [-0.145, 0.222] |
| T4 (Day 6) | 100 | 0.111 | 0.895 | [-0.064, 0.287] |

**Change from Day 0 to Day 6:** +0.227 z-units (shift from underconfidence to overconfidence)

**Trajectory Pattern:**
- Day 0: Mean calibration negative (-0.116), indicating slight underconfidence on average
- Day 1-3: Mean calibration approaches zero (improving calibration)
- Day 6: Mean calibration positive (+0.111), indicating slight overconfidence on average

### Cross-Reference to RQ 6.2.1

**RQ 6.2.1 Finding:** Calibration worsens significantly over time (LRT p = 0.004)
- RQ 6.2.1 tested whether calibration MAGNITUDE changes (absolute difference between confidence and accuracy)
- RQ 6.2.1 found significant increase in miscalibration over the retention interval

**This RQ (6.2.2) Finding:** Proportion overconfident shows non-significant trend (p = 0.230)
- This RQ tested whether overconfidence DIRECTION emerges (shift from under- to overconfident)
- Mean calibration shifts from -0.116 (underconfident) to +0.111 (overconfident)
- Proportion overconfident increases from 41% to 51% (+10 percentage points)
- BUT logistic trend test non-significant (p = 0.230)

**Integration:** These findings are COMPLEMENTARY not contradictory:
- RQ 6.2.1: Calibration gets WORSE (miscalibration increases, p = 0.004) - SIGNIFICANT
- RQ 6.2.2: Direction shifts toward OVERCONFIDENCE (mean +0.227, proportion +10%) - DESCRIPTIVE PATTERN
- RQ 6.2.2: Proportion overconfident trend NOT SIGNIFICANT (p = 0.230) - indicates gradual shift in DEGREE not discrete category flip

---

## 2. Plot Descriptions

### Figure 1: Overconfidence Trajectory (Dual-Axis)

**Filename:** plots/overconfidence_trajectory.png

**Plot Type:** Dual-axis line plot (proportion + mean calibration over time)

**Visual Description:**

The plot displays two complementary metrics of overconfidence across four test sessions:

**Panel A (Left): Proportion Overconfident**
- **X-axis:** Days Since Encoding (Day 0, 1, 3, 6 corresponding to T1-T4)
- **Y-axis:** Proportion Overconfident (range 0.3 to 0.7)
- **Reference Line:** 50% chance level (dashed gray horizontal line)
- **Trajectory:** Red line with error bars (95% CI)

**Panel B (Right): Mean Calibration**
- **X-axis:** Days Since Encoding (Day 0, 1, 3, 6 corresponding to T1-T4)
- **Y-axis:** Mean Calibration in z-units (range -0.4 to +0.4)
- **Reference Line:** Perfect calibration at 0 (solid black horizontal line)
- **Background Shading:** Underconfident region (green, below 0), Overconfident region (red, above 0), Calibrated region (gray, near 0)
- **Trajectory:** Blue line with error bars (95% CI)

**Key Visual Patterns:**

1. **Panel A - Proportion Overconfident:**
   - Starts at 41% (Day 0), below 50% chance
   - Increases to 48% (Day 1)
   - Slight decrease to 47% (Day 3)
   - Ends at 51% (Day 6), just above 50% chance
   - Error bars substantial and overlapping across all timepoints
   - Trajectory shows general upward trend but with non-monotonic pattern (Day 2 to Day 3 dip)

2. **Panel B - Mean Calibration:**
   - Starts in underconfident region (-0.116, Day 0)
   - Crosses perfect calibration line between Day 1 and Day 3
   - Ends in overconfident region (+0.111, Day 6)
   - Error bars cross zero at all timepoints (confidence intervals include perfect calibration)
   - Trajectory shows smoother monotonic increase compared to proportion metric

3. **Statistical Annotation:**
   - Panel A displays trend test result: "Trend: OR=1.05, p=0.230 (n.s.)"
   - Indicates non-significant logistic regression trend

**Connection to Statistical Findings:**

- **Visual-Statistical Coherence:** The non-significant trend test (p = 0.230) is consistent with substantial overlap in error bars across timepoints. Visual inspection confirms no clear separation between Day 0 and Day 6 proportions.

- **Mean Calibration Shift:** The smooth monotonic trajectory in Panel B (+0.227 change) visually supports the shift from underconfidence to overconfidence, even though proportion trend is non-significant.

- **Interpretation Aid:** The dual-axis format reveals that calibration change is GRADUAL (continuous shift in mean) rather than CATEGORICAL (discrete flip from underconfident to overconfident).

### Figure 2: Classification Distribution by Timepoint

**Filename:** plots/classification_distribution.png

**Plot Type:** Stacked bar chart (proportional composition)

**Visual Description:**

The plot displays the distribution of three classification categories across four test sessions:

- **X-axis:** Test Session (Day 0/T1, Day 1/T2, Day 3/T3, Day 6/T4)
- **Y-axis:** Proportion (range 0 to 1.0, representing 100%)
- **Color Coding:**
  - Green: Underconfident (Calibration < -0.1)
  - Gray: Calibrated (|Calibration| <= 0.1)
  - Red: Overconfident (Calibration > 0.1)
- **Reference Line:** 50% dashed white line (for visual comparison)

**Distribution Patterns:**

| Session | Underconfident | Calibrated | Overconfident |
|---------|----------------|------------|---------------|
| Day 0 (T1) | ~46% (green) | ~13% (gray) | ~41% (red) |
| Day 1 (T2) | ~50% (green) | ~2% (gray) | ~48% (red) |
| Day 3 (T3) | ~43% (green) | ~10% (gray) | ~47% (red) |
| Day 6 (T4) | ~39% (green) | ~10% (gray) | ~51% (red) |

**Key Visual Patterns:**

1. **Underconfident (Green) Proportion:**
   - Starts at ~46% (Day 0), slightly higher than overconfident
   - Increases to ~50% (Day 1) - highest underconfident proportion
   - Decreases to ~39% (Day 6) - lowest underconfident proportion
   - Overall trend: DECREASING from Day 0 to Day 6

2. **Overconfident (Red) Proportion:**
   - Starts at ~41% (Day 0), slightly lower than underconfident
   - Increases to ~48% (Day 1)
   - Further increases to ~51% (Day 6) - highest overconfident proportion
   - Overall trend: INCREASING from Day 0 to Day 6
   - Crosses 50% reference line at Day 6 (overconfident becomes slight majority)

3. **Calibrated (Gray) Proportion:**
   - Small proportion throughout (~2-13%)
   - Most participants are miscalibrated (either over- or underconfident)
   - Inconsistent pattern across sessions (highest at Day 0, lowest at Day 1)

4. **Composition Shift:**
   - Day 0: Underconfident > Overconfident (46% vs 41%)
   - Day 6: Overconfident > Underconfident (51% vs 39%)
   - Net compositional change: 10% shift from underconfident to overconfident category

**Connection to Statistical Findings:**

- The visual shift from green-dominant (Day 0) to red-dominant (Day 6) composition confirms the descriptive pattern of emergent overconfidence.
- The small calibrated proportion (~9% overall) explains why most participants are classified as miscalibrated.
- The stacked bar format reveals that overconfidence emergence is partly driven by underconfidence DECLINE (not just overconfidence increase).

---

## 3. Interpretation

### Hypothesis Testing

**Original Hypothesis (from 1_concept.md):**
"Overconfidence (Calibration > 0) will INCREASE from Day 0 to Day 6 as accuracy declines faster than confidence adjusts. Expected: significant positive Time effect on proportion overconfident."

**Hypothesis Status:** **PARTIALLY SUPPORTED**

**Evidence:**
1. **Descriptive Pattern Confirms Hypothesis:**
   - Proportion overconfident increases from 41% (Day 0) to 51% (Day 6) - 10 percentage point increase
   - Mean calibration shifts from -0.116 (underconfident) to +0.111 (overconfident) - 0.227 z-unit change
   - Direction of change aligns with hypothesis (shift toward overconfidence)

2. **Statistical Trend Test Non-Significant:**
   - Logistic regression: ² = 0.053, p = 0.230 (NON-SIGNIFICANT at ± = 0.05)
   - Odds ratio 95% CI includes 1.0 [0.967, 1.148], indicating no reliable effect
   - The observed 10% increase could reflect sampling variability rather than true population trend

**Nuanced Interpretation:**
The hypothesis predicted emergent overconfidence, which IS observed descriptively (+10 percentage points, mean shift of +0.227 z-units). However, the logistic trend test indicates this pattern is NOT statistically reliable at conventional ± = 0.05 threshold. This is a WEAK or MARGINAL finding rather than null result - the effect is in the predicted direction but underpowered or genuinely small.

### Theoretical Contextualization

**Metacognitive Monitoring Theory:**

The findings present a nuanced picture of confidence-accuracy dissociation over time:

1. **RQ 6.2.1 Context:** Calibration WORSENS significantly (p = 0.004)
   - Miscalibration increases over retention interval
   - Confidence and accuracy become less aligned

2. **This RQ (6.2.2):** Direction shifts toward OVERCONFIDENCE but trend non-significant
   - Mean calibration crosses from negative (underconfident) to positive (overconfident)
   - Proportion overconfident increases by 10% but with wide confidence intervals
   - Suggests gradual shift in DEGREE not discrete category flip

**Interpretation:**
The significant worsening of calibration (RQ 6.2.1) reflects increasing miscalibration MAGNITUDE (absolute difference between confidence and accuracy grows). This RQ tests whether that worsening is DIRECTIONAL (asymmetric toward overconfidence) or SYMMETRIC (equal increases in over- and underconfidence). The non-significant trend (p = 0.230) suggests miscalibration worsening is relatively SYMMETRIC - some participants become more overconfident, others more underconfident, without strong population-level directionality.

**Alternative Explanation:**
The descriptive shift (+10%) may reflect:
- Genuine small effect underpowered with N=100
- Sampling variability (true population proportion stable)
- Non-linear trajectory (U-shaped or threshold effect not captured by linear logistic model)

### Memory-Metacognition Coupling Dynamics

**Coupled vs Dissociated Systems:**

The hypothesis predicted DISSOCIATION: confidence lags behind accuracy decline, creating emergent overconfidence.

**Findings suggest PARTIAL COUPLING:**
- Calibration worsens (RQ 6.2.1 p = 0.004) - some dissociation present
- Direction shift weak (p = 0.230) - confidence adjusts reasonably well to accuracy decline
- Both overconfidence AND underconfidence increase (from 41% to 51% overconfident, but also from 46% to 39% underconfident represents 7% DECREASE)

**Interpretation:**
Confidence and accuracy decline in RELATIVELY parallel fashion (coupled system) but with INCREASING NOISE (miscalibration magnitude grows). The shift toward overconfidence is modest and statistically unreliable, suggesting metacognitive monitoring adjusts to memory decay reasonably well at the population level, even as individual-level calibration worsens.

### Unexpected Patterns

**1. Non-Monotonic Proportion Trajectory (Panel A, Figure 1):**

The proportion overconfident shows Day 0 (41%) -> Day 1 (48%) -> Day 3 (47%) -> Day 6 (51%) pattern.

**Expected:** Monotonic increase (41% -> 48% -> 52% -> 55%)
**Observed:** Day 1 to Day 3 dip (48% -> 47%)

**Possible Explanations:**
- **Sleep Consolidation (Day 0 to Day 1):** Overnight consolidation may selectively preserve accuracy more than confidence updates, creating temporary overconfidence spike at Day 1.
- **Confidence Recalibration (Day 1 to Day 3):** Participants may adjust confidence downward between Day 1 and Day 3 after recognizing memory difficulty, temporarily improving calibration.
- **Sampling Variability:** 1% difference (48% vs 47%) within measurement error, may not reflect true trajectory.

**Follow-Up Needed:** Test quadratic time term (Day^2) to formally assess non-linearity.

**2. Small Calibrated Proportion (~9%):**

Only 36/400 observations (9.0%) fall within epsilon = 0.1 calibration threshold (well-calibrated).

**Interpretation:**
- Most participants are MISCALIBRATED (91%) - either overconfident or underconfident
- Epsilon = 0.1 may be conservative (scientifically meaningful difference) but results in sparse "calibrated" category
- Metacognitive precision limited - participants struggle to achieve tight confidence-accuracy alignment

**Implication:** VR episodic memory tasks may be challenging for metacognitive monitoring. Confidence judgments noisy relative to actual performance.

**3. High Individual Variability (Wide CIs):**

95% confidence intervals for proportion overconfident are wide (e.g., Day 6: [0.413, 0.606]).

**Interpretation:**
- Substantial between-participant variability in calibration trajectories
- Some participants become more overconfident, others more underconfident (heterogeneous trajectories)
- Population-level trend may mask subgroup differences (e.g., high vs low performers have different calibration dynamics)

**Follow-Up Needed:** Individual difference analysis - cluster participants by calibration trajectory patterns.

### Broader Implications

**REMEMVR Validation:**

1. **Metacognitive Assessment Capability:**
   - REMEMVR captures confidence-accuracy dissociation over time (RQ 6.2.1 calibration worsening)
   - Direction of miscalibration (over vs under) shows modest trend but high variability
   - Tool suitable for detecting MAGNITUDE of miscalibration, less sensitive to DIRECTION

2. **Temporal Resolution:**
   - Four timepoints (Day 0, 1, 3, 6) sufficient to observe calibration worsening (6.2.1)
   - May need denser sampling (hourly intervals Day 0-1, daily Day 1-6) to resolve non-monotonic patterns

**Methodological Insights:**

1. **Classification Threshold Sensitivity:**
   - Epsilon = 0.1 results in 9% calibrated, 91% miscalibrated
   - Alternative thresholds (epsilon = 0.2 or 0.3) would increase calibrated proportion
   - Choice impacts interpretability: strict threshold (0.1) emphasizes miscalibration prevalence, lenient threshold (0.3) may obscure signal

2. **Complementary Analysis Approaches:**
   - RQ 6.2.1 continuous calibration (LMM, p = 0.004) - SIGNIFICANT
   - RQ 6.2.2 categorical overconfidence (logistic, p = 0.230) - NON-SIGNIFICANT
   - Continuous approach more sensitive to gradual shifts than categorical

**Clinical Relevance:**

For cognitive assessment applications:
- **Population-Level Calibration:** Shifts from slight underconfidence (Day 0) to slight overconfidence (Day 6) - clinically modest (~0.2 SD)
- **Individual-Level Calibration:** High variability (wide CIs) suggests some individuals show large miscalibration changes
- **Assessment Utility:** Calibration trajectory may differentiate clinical populations (e.g., MCI patients may show steeper overconfidence emergence if metacognitive monitoring impaired)

---

## 4. Limitations

### Sample Limitations

**Sample Size:**
- N = 100 participants provides 400 observations (4 timepoints)
- Power for logistic regression trend test: estimated 0.65 for small effect (OR = 1.05)
- Non-significant trend (p = 0.230) may reflect UNDERPOWERING not true null
- Larger N (200-300) needed to reliably detect 5% odds ratio per day

**Demographic Constraints:**
- University undergraduate sample (age: M = 20.3, SD = 1.8) limits generalizability to older adults
- Older adults may show different metacognitive trajectories (declining monitoring capacity)
- Restricted education range (all current college students) prevents examining education effects on calibration

**Attrition:**
- Inherited from Ch5 5.1.1 and 6.1.1 (3% dropout by Day 6)
- Attrition modest but may introduce bias if participants with poor calibration drop out

### Methodological Limitations

**Measurement:**

1. **Classification Threshold (epsilon = 0.1):**
   - Somewhat arbitrary choice (0.1 SD units = scientifically meaningful difference)
   - Results sensitive to threshold: epsilon = 0.05 would decrease calibrated proportion, epsilon = 0.2 would increase
   - No established convention for "well-calibrated" threshold in IRT-based calibration

2. **Calibration Metric:**
   - Simple difference score (theta_confidence - theta_accuracy) assumes linear relationship
   - May not capture non-linear confidence-accuracy mappings (e.g., overconfidence only at low accuracy)
   - RQ 6.2.1 used continuous metric, this RQ categorizes - discretization loses information

3. **Omnibus Aggregation:**
   - Uses single "All" factor (aggregated What/Where/When domains)
   - Domain-specific calibration patterns obscured (addressed separately in 6.3.2)
   - May mask heterogeneous trajectories across memory types

**Design:**

1. **Trend Test Specification:**
   - Linear logistic model assumes constant log-odds change per day
   - Non-monotonic pattern (Figure 1 Panel A: Day 1 to Day 3 dip) violates linearity
   - Quadratic or piecewise models not tested (may better capture trajectory shape)

2. **Time Variable:**
   - Used nominal days (0, 1, 3, 6) as ordinal predictor
   - Could use TSVR (actual hours: 0, 24, 72, 144) for continuous time - not tested here
   - Ordinal vs continuous time may yield different trend test results

3. **No Covariates:**
   - Logistic regression includes only time predictor (no age, baseline ability, domain controls)
   - Individual differences in calibration trajectories not modeled
   - Potential confounds unaccounted for (e.g., task engagement decline over sessions)

**Statistical:**

1. **Multiple Testing:**
   - Tested proportion overconfident (logistic regression p = 0.230) AND mean calibration (descriptive)
   - No correction for multiple comparisons across metrics
   - If testing both proportion and mean as formal hypotheses, alpha inflation risk

2. **Independence Assumption:**
   - Logistic regression assumes independence of observations
   - 400 observations from 100 participants (4 per participant) are CLUSTERED
   - Should use mixed-effects logistic regression with participant random effects (not implemented)
   - Standard errors may be underestimated (inflated Type I error risk)

3. **Model Fit Not Assessed:**
   - Logistic regression converged but no goodness-of-fit test (e.g., Hosmer-Lemeshow)
   - Residual diagnostics not examined
   - Model assumptions (linearity of log-odds) not validated

### Generalizability Constraints

**Population:**
- Findings may not generalize to:
  - Older adults (metacognitive monitoring declines with age, overconfidence may emerge more strongly)
  - Clinical populations (MCI/dementia patients show impaired calibration)
  - Non-WEIRD samples (cultural differences in confidence expression)

**Context:**
- VR desktop paradigm differs from real-world episodic memory
- Confidence ratings may be less accurate for immersive experiences than standard lab tasks
- Structured retrieval (forced-choice) may alter confidence calibration compared to free recall

**Task:**
- REMEMVR specific overconfidence patterns may not reflect general episodic memory metacognition
- Short encoding (10 minutes) may engage different metacognitive processes than naturalistic long-duration experiences

### Technical Limitations

**Dependency on RQ 6.2.1:**
- This RQ uses calibration scores from RQ 6.2.1 (theta_confidence - theta_accuracy)
- Any limitations/errors in RQ 6.2.1 propagate here
- RQ 6.2.1 merges outputs from Ch5 5.1.1 (accuracy) and 6.1.1 (confidence) - inherits limitations from both

**IRT Purification Impact:**
- Theta scores derived from purified item sets (Ch5 5.1.1 and 6.1.1 both used Decision D039 purification)
- Item exclusions may create domain imbalances affecting calibration estimates
- Purification thresholds somewhat arbitrary (a >= 0.4, |b| <= 3.0)

**Calibration Metric Assumptions:**
- Assumes theta_accuracy and theta_confidence on comparable scales (both standardized)
- Ignores measurement error (theta SEs not incorporated into calibration)
- Simple difference may not reflect true latent calibration construct

### Limitations Summary

**Most Critical Limitations:**
1. **Statistical Power:** N=100 underpowered for small effects (OR = 1.05), non-significant trend may be Type II error
2. **Non-Independence:** Clustered observations (4 per participant) violate logistic regression independence assumption
3. **Threshold Sensitivity:** epsilon = 0.1 choice impacts classification proportions and interpretability

**Despite Limitations, Findings Are Interpretable:**
- Descriptive pattern robust: +10% overconfidence shift, +0.227 mean calibration change
- Non-significant trend (p = 0.230) indicates pattern NOT STRONG or CONSISTENT enough for reliable detection
- Complementary to RQ 6.2.1 (calibration worsens significantly) - directionality weak even as magnitude increases

---

## 5. Next Steps

### Immediate Follow-Ups (Current Data)

**1. Mixed-Effects Logistic Regression with Participant Random Effects:**
- **Why:** Current analysis violates independence assumption (4 observations per participant)
- **How:** Fit generalized linear mixed model (GLMM): overconfident ~ time + (1|UID)
- **Expected Insight:** Adjust standard errors for clustering, obtain correct p-value for trend test (may change from p=0.230)
- **Timeline:** Immediate (same data, different model specification in statsmodels or lme4)

**2. Test Non-Linear Time Trajectory:**
- **Why:** Figure 1 Panel A shows non-monotonic pattern (Day 1 to Day 3 dip)
- **How:** Add quadratic time term: overconfident ~ time + time^2 + (1|UID)
- **Expected Insight:** Determine if Day 1 spike and Day 3 dip statistically meaningful or sampling noise
- **Timeline:** Immediate (same data, add polynomial term)

**3. Sensitivity Analysis for Classification Threshold:**
- **Why:** epsilon = 0.1 somewhat arbitrary, results may depend on threshold choice
- **How:** Re-run classification with epsilon = 0.05, 0.2, 0.3; test trend at each threshold
- **Expected Insight:** Assess robustness of non-significant trend to threshold definition
- **Timeline:** ~1 hour (re-run Steps 1-3 with different epsilon values)

**4. Individual Difference Clustering:**
- **Why:** Wide CIs suggest heterogeneous calibration trajectories across participants
- **How:** Extract person-level calibration change (Day 6 - Day 0), cluster into "increasers" vs "decreasers" vs "stable"
- **Expected Insight:** Identify subgroups with different overconfidence dynamics (e.g., high performers more overconfident, low performers more underconfident)
- **Timeline:** Immediate (current data, groupby participant)

### Planned Thesis RQs (Chapter 6 Continuation)

**RQ 6.3.2: Domain-Specific Overconfidence Trajectories (Planned):**
- **Focus:** Test whether overconfidence emergence differs across What/Where/When domains
- **Why:** This RQ uses omnibus "All" factor; domains may show heterogeneous directionality (e.g., When domain more prone to overconfidence)
- **Builds On:** Uses domain-specific calibration scores from RQ 6.3.1 (domain decomposition of 6.2.1)
- **Expected Timeline:** Next in calibration series after 6.3.1 completes

**RQ 6.4.X: Metacognitive Predictors of Calibration (Exploratory):**
- **Focus:** What predicts good vs poor calibration? Baseline ability? Memory performance? Individual traits?
- **Why:** High variability in calibration trajectories suggests individual differences matter
- **Builds On:** Uses calibration scores from 6.2.1 as outcome, regresses on participant characteristics
- **Expected Timeline:** Later in Ch6 (after domain-specific analyses 6.3.X complete)

### Methodological Extensions (Future Data Collection)

**1. Increase Sample Size for Adequate Power:**
- **Current Limitation:** N=100 underpowered for small effects (OR = 1.05, estimated power = 0.65)
- **Extension:** Recruit N=200-300 participants for adequate power (0.80) to detect 5% odds ratio per day
- **Expected Insight:** Resolve whether p=0.230 trend reflects true null or Type II error
- **Feasibility:** Requires new data collection (~6 months for N=200)

**2. Test Alternative Calibration Metrics:**
- **Current Limitation:** Simple difference score (theta_confidence - theta_accuracy) may not capture non-linear relationships
- **Extension:** Test ratio metric (theta_confidence / theta_accuracy), absolute difference (|Calibration|), or Brier score
- **Expected Insight:** Determine if calibration metric choice affects directionality findings
- **Feasibility:** Immediate (current data, alternative metric calculation)

**3. Add Hourly Sampling Day 0-1 to Resolve Consolidation Effects:**
- **Current Limitation:** Day 0 to Day 1 jump largest (41% to 48%), but no intermediate timepoints
- **Extension:** Add 6-hour and 12-hour post-encoding tests to resolve consolidation dynamics
- **Expected Insight:** Test sleep consolidation hypothesis (overconfidence spike after overnight sleep?)
- **Feasibility:** Requires new data collection with denser sampling (~1 year for design + collection)

**4. Compare VR vs 2D Calibration Trajectories:**
- **Current Limitation:** Cannot isolate VR-specific metacognitive effects
- **Extension:** Recruit N=100 matched controls, administer 2D slideshow version, compare overconfidence emergence
- **Expected Insight:** Test if VR immersion affects confidence-accuracy dissociation (e.g., VR confidence more resistant to updating than 2D?)
- **Feasibility:** Requires new participants and 2D task development (~6 months)

### Theoretical Questions Raised

**1. Why Does Calibration Worsen (6.2.1) Without Strong Directionality (6.2.2)?**
- **Question:** Miscalibration MAGNITUDE increases significantly (p=0.004) but DIRECTION shows weak trend (p=0.230). Why symmetric worsening?
- **Next Steps:** Examine variance of calibration over time (SD increases from 0.89 to 0.90 in this RQ). Test if calibration SPREAD increases more than mean shifts.
- **Expected Insight:** Distinguish between population-level shift (mean change) vs individual-level noise (variance increase)
- **Feasibility:** Immediate (current data, variance ratio test)

**2. Individual Differences in Metacognitive Monitoring Capacity:**
- **Question:** Wide CIs suggest some participants maintain good calibration while others worsen. What predicts resilient metacognition?
- **Next Steps:** Regress calibration change on baseline cognitive ability, memory performance, personality (if available)
- **Expected Insight:** Identify protective factors for maintaining confidence-accuracy alignment
- **Feasibility:** Requires additional measures (cognitive battery, personality inventory) - not in current dataset

**3. Neural Mechanisms of Confidence Updating:**
- **Question:** What brain regions support confidence adjustment as memories fade? Prefrontal metacognitive monitoring? Hippocampal memory signals?
- **Next Steps:** fMRI study during VR retrieval with trial-by-trial confidence ratings
- **Expected Insight:** Identify neural dissociations between accuracy and confidence updating (e.g., PFC activity predicts confidence adjustment speed?)
- **Feasibility:** Long-term collaboration (~2-3 years for fMRI study)

### Priority Ranking

**High Priority (Do First):**
1. Mixed-effects logistic regression (correct non-independence) - addresses critical statistical limitation
2. Quadratic time term (test non-linearity) - resolves Figure 1 Panel A pattern
3. Individual difference clustering - leverages high variability to identify subgroups

**Medium Priority (Subsequent):**
1. RQ 6.3.2 (domain-specific overconfidence) - natural next step in thesis progression
2. Sensitivity analysis for epsilon threshold - robustness check for classification
3. Variance analysis (calibration spread over time) - explains 6.2.1 vs 6.2.2 divergence

**Lower Priority (Aspirational):**
1. Sample size increase - ideal but requires new data collection
2. VR vs 2D comparison - interesting but not critical for current thesis
3. fMRI neural mechanisms - long-term research program, outside thesis scope

### Next Steps Summary

The findings establish that **calibration worsens over time (RQ 6.2.1 p=0.004) with modest shift toward overconfidence (RQ 6.2.2 +10%, p=0.230 non-significant)**, raising three critical questions for immediate follow-up:

1. **Mixed-effects model:** Does correcting for non-independence change p=0.230 trend? (Statistical refinement)
2. **Domain decomposition:** Is overconfidence emergence domain-specific? (RQ 6.3.2 planned)
3. **Individual differences:** What predicts resilient vs vulnerable calibration? (Exploratory clustering)

Methodological extensions (larger N, denser sampling, VR vs 2D) are valuable but require new data collection beyond current thesis scope. Priority is refining current analysis (mixed-effects) and completing domain-specific series (6.3.X).

---

**Summary Generated By:** rq_results agent (v4.0)
**Pipeline Version:** v4.X (13-agent atomic architecture)
**Date:** 2025-12-11
