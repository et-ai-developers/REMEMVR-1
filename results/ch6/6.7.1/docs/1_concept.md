# RQ 6.7.1: Initial Confidence Predicting Forgetting Rates

**Chapter:** 6
**Type:** Predictive
**Subtype:** Day 0 Confidence
**Full ID:** 6.7.1

---

## Research Question

**Primary Question:**
Does high initial retrieval confidence at Day 0 predict slower forgetting trajectories across a 6-day retention interval?

**Scope:**
This RQ examines the relationship between initial metacognitive retrieval confidence (theta_confidence at T1/Day 0, measured AFTER retrieval during the Day 0 test) and subsequent forgetting rates (random slopes from accuracy trajectories). Sample: N=100 participants with both Day 0 confidence estimates and individual forgetting slopes.

**IMPORTANT TERMINOLOGY NOTE:** Confidence is measured during the Day 0 TEST (T1), after participants attempt retrieval - NOT during initial VR encoding. These are retrospective metacognitive judgments about retrieval success (Koriat & Ma'ayan, 2005), not encoding-time predictions. The term "Day 0 retrieval confidence" is used throughout to reflect this distinction.

**Theoretical Framing:**
If metacognitive judgments after retrieval reflect underlying memory trace strength, then memories retrieved with high confidence should show slower decay. Alternatively, if confidence judgments are imperfect or dissociated from encoding strength, initial confidence may not predict forgetting trajectories. This RQ tests whether Day 0 metacognitive state has predictive validity for subsequent memory dynamics.

---

## Theoretical Background

**Relevant Theories:**
- **Encoding Strength Theory**: Well-encoded items should generate both high confidence judgments and durable memory traces, creating positive correlation between Day 0 confidence and slower forgetting.
- **Metacognitive Monitoring Models**: If confidence judgments accurately reflect memory strength, high confidence should predict better retention. If metacognitive access is imperfect, confidence may dissociate from objective memory quality.
- **Levels of Processing**: Items encoded with elaborative processing should generate high confidence (due to fluent retrieval at encoding) and slower forgetting (due to rich trace formation).

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
High Day 0 confidence predicting slower forgetting would support the view that metacognitive judgments at encoding tap into encoding quality. Null result would suggest confidence is dissociated from factors controlling consolidation, possibly reflecting only retrieval fluency at T1 rather than trace durability.

**Literature Gaps:**
[To be identified by rq_scholar]

---

## Hypothesis

**Primary Hypothesis:**
High Day 0 confidence may predict slower forgetting slope (well-encoded items have both high confidence and slower decay). Positive correlation expected between Day0_confidence and forgetting_slope (more positive/less negative slopes for high confidence individuals).

**Secondary Hypotheses:**
Alternatively, confidence may NOT predict forgetting if metacognitive judgments are imperfect and only reflect momentary retrieval fluency at T1 rather than encoding quality or consolidation trajectory.

**Theoretical Rationale:**
If confidence at encoding reflects genuine encoding strength (not just retrieval fluency), then high initial confidence should correlate with durable traces that resist decay. This assumes metacognitive monitoring has access to encoding quality information, not just retrieval ease.

**Expected Effect Pattern:**
Positive correlation between Day0_confidence and forgetting_slope. Tertile analysis (High/Med/Low initial confidence groups) should show high confidence group with slower (less negative) forgetting slopes. Direction of effect will clarify whether confidence has predictive validity for consolidation.

---

## Memory Domains

**Domains Examined:**

- [x] **Omnibus "All" Factor**
  - Description: Single aggregate confidence score combining all VR items
  - Parallels Ch5 5.1.X General analyses

**Inclusion Rationale:**
Uses omnibus confidence factor from RQ 6.1.1 to match the omnibus accuracy factor from Ch5 5.1.4. General forgetting slopes (not domain-specific) to test broad relationship between initial metacognitive state and memory dynamics.

**Exclusion Rationale:**
Domain-specific analyses not needed for this predictive RQ. Focus is on overall confidence-forgetting relationship, not domain differences.

---

## Analysis Approach

**Analysis Type:**
Correlation and regression analysis testing predictive relationship between Day 0 retrieval confidence and individual forgetting slopes

**High-Level Workflow:**

**Step 0:** Load Day 0 retrieval confidence from RQ 6.1.1 (theta_confidence at T1)
**Step 1:** Load forgetting slopes from Ch5 5.1.4 (random slopes from accuracy LMM)
**Step 2:** Validate assumptions before correlation analysis:
- **Normality test:** Shapiro-Wilk on both variables (Day0_confidence, forgetting_slope)
- If p < 0.05 (non-normality detected): Use Spearman rank correlation as primary analysis, report Pearson as supplementary
- If p >= 0.05 (normality acceptable): Use Pearson as primary, report Spearman as robustness check
- Document: Shapiro-Wilk W statistics, p-values, decision rationale
**Step 3:** Compute correlation: Day0_confidence vs slope with dual p-values (parametric test + bootstrap 95% CI with 10000 resamples). **Note:** Decision D068 dual p-values (Wald + LRT) apply to LMM/regression contexts, not simple correlation; use parametric + bootstrap for correlation
**Step 4:** Fit simple linear regression: forgetting_slope ~ Day0_confidence to quantify predictive relationship
- Report: β coefficient, SE, t-statistic, p-value, R²
- Check assumptions: Q-Q plot of residuals, residuals vs fitted, Cook's D for outliers
**Step 5:** Test if high confidence predicts slower forgetting (directional hypothesis)
**Step 6:** Tertile analysis - create High/Med/Low confidence tertiles, compare mean forgetting slopes across groups (one-way ANOVA + Tukey HSD)
**Step 7:** Prepare plot data showing relationship between initial confidence and forgetting trajectories

**Expected Outputs:**
- data/step01_predictive_data.csv (100 rows: UID, Day0_confidence, forgetting_slope)
- results/step02_normality_tests.csv (Shapiro-Wilk results for both variables)
- results/step03_correlation.csv (r, p_parametric, bootstrap_CI_95, Spearman_rho if applicable)
- results/step04_regression.csv (β, SE, t, p, R², residual diagnostics)
- results/step05_tertile_slopes.csv (3 rows: tertile means for confidence and slopes, ANOVA F, p)
- plots/step06_confidence_predicts_forgetting.csv (plot data showing relationship with regression line)

**Success Criteria:**
- Day 0 retrieval confidence extracted successfully from RQ 6.1.1 (100 values)
- Forgetting slopes extracted successfully from Ch5 5.1.4 (100 values)
- Normality assessed via Shapiro-Wilk with documented decision
- Correlation computed with appropriate method (Pearson or Spearman based on normality) + bootstrap 95% CI
- Regression analysis complete with assumption diagnostics (Q-Q, residuals, Cook's D)
- Tertile analysis complete with valid group sizes (each tertile >= 30 participants)
- Direction of effect documented (positive/negative/null)
- Plot data complete with no missing values

---

## Data Source

**Data Type:**
DERIVED (from RQ 6.1.1 and Ch5 5.1.4 outputs)

### DERIVED Data Source:

**Source RQs:**
- **RQ 6.1.1** (Confidence Functional Form): Provides Day 0 confidence estimates
- **Ch5 5.1.4** (Accuracy ICC Decomposition): Provides individual forgetting slopes

**File Paths:**
- results/ch6/6.1.1/data/step03_theta_confidence.csv (confidence theta scores, filter to T1/Day 0)
- results/ch5/5.1.4/data/step04_random_effects.csv (individual random slopes for accuracy forgetting)

**Dependencies:**
- RQ 6.1.1 must complete Step 3 (IRT calibration for confidence)
- Ch5 RQ 5.1.4 must complete Step 4 (random effects extraction from accuracy LMM)

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (inherited from both source RQs)
- No exclusions - all participants with both Day 0 confidence and forgetting slope estimates

**Items:**
- N/A (theta scores and slopes already aggregated to person-level)

**Tests:**
- Day 0 confidence: T1 only (baseline measurement)
- Forgetting slopes: Derived from all 4 tests (T1-T4) in Ch5 5.1.4

---

## Interpretation Guidelines

**Section 5: How to Interpret Results**

### 5.1 Direction of Effect

**Positive correlation (r > 0):** High Day 0 confidence predicts SLOWER forgetting (less negative slopes). Supports encoding strength hypothesis - confident memories are durable memories.

**Negative correlation (r < 0):** High Day 0 confidence predicts FASTER forgetting. Would suggest metacognitive overconfidence at encoding - being confident doesn't mean well-encoded.

**Null correlation (|r| < 0.10):** Day 0 confidence dissociated from forgetting trajectory. Metacognitive judgments at encoding do not tap into factors controlling consolidation.

### 5.2 Effect Size Benchmarks

| Effect Size | r Value | Interpretation |
|-------------|---------|----------------|
| Strong | |r| > 0.50 | Confidence is a powerful predictor of forgetting |
| Moderate | 0.30 ≤ |r| ≤ 0.50 | Confidence has meaningful predictive validity |
| Weak | 0.10 ≤ |r| < 0.30 | Small but potentially meaningful relationship |
| Negligible | |r| < 0.10 | No practical predictive value |

### 5.3 Confidence Interval Interpretation

- If 95% CI excludes 0: Statistically significant relationship
- If 95% CI includes 0: Cannot reject null hypothesis of no relationship
- Width of CI: Narrower = more precise estimate (N=100 provides reasonable precision)

### 5.4 Tertile Analysis Interpretation

**Expected pattern if hypothesis supported:**
- High confidence tertile: Mean slope closest to 0 (slowest forgetting)
- Medium confidence tertile: Intermediate slope
- Low confidence tertile: Most negative slope (fastest forgetting)

**Monotonic pattern (High > Med > Low):** Strong support for encoding strength hypothesis
**Non-monotonic pattern:** May suggest non-linear relationship or confounds

### 5.5 Theoretical Implications

**If positive relationship found:**
- Validates metacognitive accuracy: Confidence at encoding reflects encoding quality
- Practical application: Day 0 confidence could identify at-risk memories for intervention
- Mechanism: Encoding strength drives both confident retrieval AND durable traces

**If null relationship found:**
- Dissociation between metacognition and consolidation processes
- Confidence may reflect retrieval fluency at T1, not encoding quality
- Separate neural systems for "feeling of knowing" vs trace consolidation

### 5.6 Assumption Validation

**Linearity:** Check scatterplot for curvilinear patterns; if present, consider polynomial terms
**Homoscedasticity:** Residuals should show constant variance across predicted values
**Normality:** For N=100, Central Limit Theorem provides robustness to mild non-normality
**Outliers:** Cook's D > 4/N suggests influential observations; report sensitivity analysis

### 5.7 Comparison to Ch5 Context

This predictive analysis extends Ch5 findings:
- Ch5 5.1.4 documented ICC_slope ≈ 0.077 (low but detectable individual differences in forgetting)
- If Day 0 confidence predicts these individual differences, it identifies a metacognitive source of variance
- Compare effect size here to Ch5 5.1.4 ICC_slope magnitude

---
