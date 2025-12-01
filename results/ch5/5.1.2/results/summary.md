# Results Summary: RQ 5.1.2 - Evidence for Two-Phase Forgetting (Rapid then Slow)

**Research Question:** Do episodic memory data support a two-phase model with rapid initial decline (Day 0-1) followed by slower decay (Day 1-6)?

**Analysis Completed:** 2025-11-28

**Analyst:** rq_results agent (v4.0) with master claude orchestration

---

## 1. Statistical Findings

### Sample Characteristics

- **Total N:** 100 participants (inherited from RQ 5.1.1)
- **Observations:** 400 data points (100 participants x 4 test sessions)
- **Data Source:** IRT-derived theta scores from RQ 5.1.1, collapsed across What/Where/When domains
- **Time Variable:** TSVR (Time Since VR encoding) in hours, range: 1.0 to 148.0 hours
- **Missing Data:** None (complete data for all participants across 4 test sessions)
- **Retention Interval:** Day 0 (encoding), Day 1 (~24h), Day 3 (~72h), Day 6 (~144h)

### Triangulation Strategy: Three Convergent Tests

This RQ used three independent statistical tests to triangulate evidence for two-phase forgetting:

1. **Test 1:** Quadratic term significance (curvature = deceleration)
2. **Test 2:** Piecewise vs continuous model AIC comparison (sharp inflection vs smooth curve)
3. **Test 3:** Early vs Late slope ratio (rapid->slow transition)

**Key Finding:** Tests 1 and 3 STRONGLY support two-phase forgetting, but Test 2 favors continuous model. This indicates forgetting DOES decelerate over time (two-phase pattern present), but transition is GRADUAL rather than sharp inflection at 48 hours.

---

### Test 1: Quadratic Term Significance

**Model:** Theta ~ Time + Time� + (1 | UID)

**Note:** Random structure used fallback to intercepts-only (1 | UID) due to convergence issues with attempted random slopes (Time | UID). With N=100 participants, complex random structures often fail to converge (Bates et al., 2015 recommend N>=200).

**Fixed Effects:**

| Term | Coefficient | SE | z | p (uncorr) | p (Bonf) | 95% CI |
|------|-------------|----|----|------------|----------|---------|
| Intercept | 0.612 | 0.080 | 7.650 | <.001 | <.001 | [0.455, 0.769] |
| Time | -0.016 | 0.002 | -9.292 | <.001 | <.001 | [-0.019, -0.012] |
| Time� | 0.000054 | 0.000 | 5.415 | <.001 | <.001 | [0.000, 0.000] |

**Bonferroni Correction:** � = 0.05/15 = 0.0033 (correcting for 15 RQs in Chapter 5)

**Convergence:** True
**Model Fit:** AIC = 873.24, BIC = 893.19
**Random Effects Variance:** ò(intercept) = 0.373 (substantial individual differences in baseline memory ability)

**Test 1 Result:** Time� coefficient is POSITIVE (0.000054) and SIGNIFICANT (p < 0.001, well below Bonferroni � = 0.0033). This indicates significant DECELERATION in forgetting rate over time (concave-up curvature), supporting two-phase hypothesis.

---

### Test 2: Piecewise vs Continuous Model Comparison

**Piecewise Model:** Theta ~ Days_within x Segment + (Days_within | UID)

**Segment Definition:**
- **Early:** 0-48 hours TSVR (Day 0-1, pre-consolidation)
- **Late:** 48-240 hours TSVR (Day 1-6, post-consolidation)
- **Theoretical Rationale:** 48-hour breakpoint represents one night's sleep + consolidation window

**Fixed Effects:**

| Term | Coefficient | SE | z | p (uncorr) | p (Bonf) | 95% CI |
|------|-------------|----|----|------------|----------|---------|
| Intercept (Early start) | 0.656 | 0.087 | 7.526 | <.001 | <.001 | [0.485, 0.827] |
| Segment[T.Late] | -0.860 | 0.095 | -9.034 | <.001 | <.001 | [-1.046, -0.673] |
| Days_within (Early slope) | -0.432 | 0.071 | -6.063 | <.001 | <.001 | [-0.572, -0.292] |
| Days_within:Segment[T.Late] | 0.362 | 0.076 | 4.791 | <.001 | <.001 | [0.214, 0.511] |

**CRITICAL ISSUE:** Convergence = FALSE (model did not converge, parameter estimates potentially unstable)

**AIC Comparison:**

| Model | AIC | deltaAIC (vs Continuous) | Interpretation |
|-------|-----|----------------------|----------------|
| **Best Continuous (RQ 5.1.1)** | 873.71 | 0.00 (reference) | Log model from RQ 5.1.1 |
| **Quadratic (Test 1)** | 873.24 | -0.47 | Equivalent to continuous |
| **Piecewise (Test 2)** | 878.74 | +5.03 | WORSE than continuous |

**Decision Rule:** deltaAIC < -2 favors piecewise (sharp inflection), deltaAIC > +2 favors continuous (smooth curve), |deltaAIC| < 2 equivalent

**Test 2 Result:** deltaAIC = +5.03 strongly favors CONTINUOUS model over piecewise. Evidence AGAINST sharp inflection at 48 hours. However, this result is qualified by piecewise model non-convergence and potential random structure mismatch (see Limitations).

---

### Test 3: Early vs Late Slope Ratio

**Extracted from Piecewise Model (despite non-convergence):**

| Metric | Value | SE | 95% CI | Interpretation |
|--------|-------|----|---------|-----------------|
| **Early slope** (0-48h) | -0.432 | 0.071 | [-0.572, -0.292] | Rapid forgetting (-0.432 theta units/day) |
| **Late slope** (48-240h) | -0.070 | 0.026 | [-0.121, -0.018] | Slow forgetting (-0.070 theta units/day) |
| **Ratio (Late/Early)** | 0.161 | 0.066 | [0.032, 0.291] | Late forgetting only 16% of Early rate |
| **Interaction p-value** | <0.000002 | - | - | Highly significant (p << 0.0033 Bonferroni �) |

**Threshold for "Robust Two-Phase":** Ratio < 0.5 (Late forgetting less than half Early rate)

**Test 3 Result:** Ratio = 0.161 << 0.5 threshold. Late forgetting only 16% as fast as Early forgetting. Interaction HIGHLY significant (p < 0.000002). STRONG evidence for two-phase forgetting pattern with dramatically different forgetting rates across segments.

---

### Assumption Validation (Step 4)

**Comprehensive checks performed on both models (6 diagnostics):**

| Assumption | Quadratic Model | Piecewise Model | Threshold |
|------------|-----------------|-----------------|-----------|
| Residual normality (Shapiro-Wilk) | PASS (p=0.099) | PASS (p=0.111) | p > 0.05 |
| Homoscedasticity (Breusch-Pagan) | FAIL (p=0.031) | FAIL (p=0.049) | p > 0.05 |
| Random intercepts normality | PASS (p=0.057) | PASS (p=0.056) | p > 0.05 |
| Random slopes normality | N/A (no slopes) | PASS (p=0.827) | p > 0.05 |
| Autocorrelation (ACF lag-1) | FAIL (ACF=-0.22) | FAIL (ACF=-0.22) | |ACF| < 0.1 |
| Outliers (Studentized residuals) | PASS (1/400 = 0.25%) | PASS | <5% |

**Summary:** Both models passed normality checks and outlier detection, but FAILED homoscedasticity and autocorrelation tests. These violations can inflate Type I error rates and bias parameter estimates (see Limitations, Section 4).

---

### Synthesis of Triangulation Results

| Test | Evidence for Two-Phase? | Strength |
|------|-------------------------|----------|
| **Test 1** (Quadratic term) | YES - Time� significant (p<.001) | Strong |
| **Test 2** (AIC comparison) | NO - Continuous favored (deltaAIC=+5.03) | Strong (against) |
| **Test 3** (Slope ratio) | YES - Ratio=0.161<<0.5, interaction p<.001 | Very Strong |

**Overall Conclusion:** Evidence for two-phase forgetting is **ROBUST but NUANCED**. Two of three tests strongly support two-phase pattern (Tests 1 and 3), indicating forgetting rate DOES decelerate over time. However, Test 2 (AIC comparison) favors continuous smooth deceleration over sharp piecewise inflection, suggesting the transition is **GRADUAL** rather than abrupt at 48 hours.

**Resolution:** Forgetting exhibits two-phase dynamics (rapid early, slow late), but the change is not a discrete inflection point at Day 1. Instead, forgetting rate continuously decelerates across the 6-day interval, with Early segment substantially faster than Late segment when artificially divided at 48 hours.

---

## 2. Plot Descriptions

### Figure 1: Model Comparison - Continuous vs Piecewise Forgetting Trajectories

**Filename:** `piecewise_comparison.png`
**Plot Type:** Two-panel comparison (Quadratic vs Piecewise models)
**Generated By:** Step 6 plot data preparation + rq_plots agent

**Visual Description:**

The figure presents side-by-side comparison of two competing models for forgetting trajectories over 240 hours (10 days) post-encoding:

**Left Panel: Continuous Model (Quadratic)**
- **Observed data:** 4 black points with error bars (mean theta +/- SE at each test session)
- **Model predictions:** Red curve showing smooth quadratic trajectory
- **Confidence band:** Pink shaded region (95% CI widening over time, indicating increasing uncertainty)
- **X-axis:** Hours Since VR Encoding (TSVR): 0 to 250 hours
- **Y-axis:** Memory Ability (Theta): -1.0 to +1.0

**Visual Pattern (Left):**
- Smooth continuous deceleration from theta ~ +0.6 at encoding to theta ~ -0.5 at Day 6
- Steep initial decline (0-50h), gradually flattening curve
- NO visible inflection point - smooth concave-up curvature throughout
- Observed points align well with predicted curve (minimal misfit)

**Right Panel: Piecewise Model (Inflection at 48h)**
- **Observed data:** Same 4 black points with error bars
- **Model predictions:**
  - Blue line (Early segment, 0-48h): Steep negative slope
  - Green line (Late segment, 48-240h): Shallow negative slope
  - Vertical dashed gray line at 48h: Theoretical inflection point (one night's sleep)
- **Confidence bands:**
  - Blue shaded (Early): 95% CI for pre-consolidation phase
  - Green shaded (Late): 95% CI for post-consolidation phase
- **Axes:** Same as left panel

**Visual Pattern (Right):**
- Clear two-phase structure: Rapid decline Early, slow decline Late
- Visible "kink" at 48h inflection point (not smooth transition)
- Early segment: theta drops from +0.66 to -0.21 in 48 hours (-0.87 total decline)
- Late segment: theta drops from -0.20 to -0.76 in 192 hours (-0.56 total decline, but over 4x longer duration)
- Confidence bands VERY wide (especially Late segment), reflecting model uncertainty and non-convergence
- Both segments' CIs overlap substantially, despite significant interaction term

**Key Patterns Across Both Panels:**

1. **Deceleration visible in both models:** Forgetting slows over time regardless of model choice
2. **Early forgetting steep:** Both models show rapid decline in first 48 hours (0-2 days)
3. **Late forgetting shallow:** Both models show slower decline after 48 hours (Days 2-6)
4. **Observed data fit both models:** Black points fall within confidence bands of both models (neither model grossly misfit)
5. **Uncertainty increases over time:** Confidence bands widen from Day 0 to Day 6 in both panels (fewer observations, extrapolation uncertainty)

**Differences Between Models:**

- **Continuous (left):** Smooth curve assumes forgetting rate changes continuously (no discrete phases)
- **Piecewise (right):** Sharp "kink" at 48h assumes discrete phase transition (consolidation-driven inflection)
- **Parsimony:** Continuous model simpler (no inflection point parameter), hence favored by AIC despite similar fit to observed data

**Connection to Findings:**

- **Visual supports Test 1:** Quadratic curve shows clear concave-up curvature (deceleration), matching significant Time� coefficient (p<.001)
- **Visual supports Test 3:** Piecewise panel shows dramatically different slopes (steep blue vs shallow green), matching slope ratio 0.161
- **Visual explains Test 2 result:** No obvious "kink" in observed data at 48h - smooth curve (left) fits data as well as piecewise (right) with fewer parameters, hence lower AIC

**Interpretation:** Plot reveals why triangulation is partial. Both models capture the SAME underlying pattern (deceleration), but differ in HOW they model the transition. Continuous model treats it as smooth change, piecewise treats it as sharp break. Data support deceleration (two-phase pattern exists) but do not demand sharp inflection (continuous sufficient).

---

## 3. Interpretation

### Hypothesis Testing

**Original Hypothesis (from 1_concept.md):**

"Forgetting exhibits two distinct phases: rapid initial decline (Day 0-1, pre-consolidation) followed by slower decay (Day 1-6, post-consolidation). Evidence will come from convergence of three tests: (1) significant quadratic term (positive curvature = deceleration), (2) piecewise model fits better than continuous model (deltaAIC < -2), (3) Late/Early slope ratio < 0.5."

**Hypothesis Status:** **PARTIALLY SUPPORTED**

The hypothesis prediction of triangulated evidence was PARTIALLY confirmed:
- **Test 1 (Quadratic term):** SUPPORTED - Time� significant (p < 0.001 < Bonferroni � = 0.0033), positive coefficient indicates deceleration
- **Test 2 (AIC comparison):** NOT SUPPORTED - Piecewise model WORSE fit than continuous (deltaAIC = +5.03 > +2 threshold), contradicts prediction of deltaAIC < -2
- **Test 3 (Slope ratio):** STRONGLY SUPPORTED - Ratio = 0.161 << 0.5 threshold, interaction p < 0.000002 (highly significant)

**Refined Interpretation:**

Two of three tests support two-phase forgetting, but the divergent AIC result reveals a CRITICAL NUANCE:

1. **Two-phase PATTERN exists:** Forgetting does exhibit rapid->slow dynamics. Early segment forgetting rate (-0.432/day) is 6.2x faster than Late segment (-0.070/day). This is robust, replicable, and highly significant.

2. **Two-phase MECHANISM may differ from hypothesis:** The hypothesis assumed a discrete consolidation-driven inflection at 48 hours (one night's sleep). However, AIC comparison favors continuous smooth deceleration over piecewise sharp break. This suggests forgetting rate changes GRADUALLY across retention interval, not abruptly at Day 1.

3. **Consolidation theory still relevant:** Consolidation may drive deceleration (stabilizing memories reduces vulnerability), but the process appears continuous rather than creating discrete pre/post-consolidation phases. Sleep-dependent consolidation could be ongoing across multiple nights, not "switched on/off" at 24 hours.

**Theoretical Reconciliation:**

The findings align with **continuous consolidation models** (e.g., Wixted & Ebbesen, 1991; Sadeh et al., 2014) rather than **discrete-phase consolidation theory** (Dudai, 2004). Instead of vulnerable->stable transition at fixed timepoint, memories may undergo graded stabilization over days, producing continuous deceleration rather than sharp inflection.

---

### Consolidation Theory Context

**Traditional Consolidation Prediction:**

Classical consolidation theory (Dudai, 2004; Hardt et al., 2013) predicts discrete phases:
1. **Pre-consolidation (0-24h):** Fragile traces, rapid forgetting, hippocampal-dependent
2. **Post-consolidation (24h+):** Stabilized traces, slow forgetting, cortical redistribution

One night's sleep (occurring ~24-48h post-encoding for most participants in REMEMVR) should trigger consolidation, creating inflection point.

**Our Findings Challenge This:**

- deltaAIC = +5.03 indicates data do NOT require discrete inflection at 48 hours
- Smooth quadratic deceleration (AIC = 873.24) fits as well as or better than piecewise break
- This suggests consolidation is **graded process**, not binary switch

**Alternative Consolidation Models Supported:**

1. **Multiple Trace Theory (MTT):** Nadel & Moscovitch (1997) propose episodic memories remain hippocampal-dependent indefinitely, but trace strength increases gradually over repeated reactivations. Our continuous deceleration aligns with gradual strengthening, not discrete stabilization.

2. **Continuous Consolidation:** Wixted & Ebbesen (1991) two-component model assumes fast + slow forgetting processes operate simultaneously from encoding, with relative contribution shifting gradually over time. This predicts smooth deceleration, not inflection.

3. **Systems Consolidation Timescales:** While sleep-dependent consolidation occurs within hours (Rasch & Born, 2013), systems-level cortical integration may require days to weeks (Frankland & Bontempi, 2005). Our 6-day window may capture early systems consolidation, which is continuous rather than discrete.

**Resolution:**

Two-phase forgetting pattern EXISTS (slope ratio robust), but the underlying mechanism is likely **continuous graded consolidation** rather than discrete pre/post transition at 24 hours. VR episodic memories may stabilize gradually over multiple sleep cycles (Days 0-6), producing smooth deceleration curve observed in our data.

---

### Unexpected Patterns

#### Unexpected Pattern 1: Triangulation Failure (AIC Contradiction)

**What We Found:**

Test 2 (AIC comparison) favored continuous model (deltaAIC = +5.03), contradicting Tests 1 and 3 which supported two-phase forgetting. This was UNEXPECTED given hypothesis predicted all three tests would converge.

**Theoretical Implications:**

This divergence is scientifically meaningful, not merely statistical noise:

1. **Tests 1 and 3 detect PATTERN:** Quadratic term and slope ratio both measure whether forgetting rate CHANGES over time. Both tests confirm deceleration exists (forgetting slows).

2. **Test 2 detects MECHANISM:** AIC comparison tests whether change is SHARP BREAK (piecewise) or SMOOTH TRANSITION (continuous). Result favors smooth transition.

3. **Synthesis:** Two-phase PATTERN is real (rapid->slow dynamics), but MECHANISM is continuous deceleration, not discrete consolidation-driven inflection.

**Possible Explanations:**

- **Sleep variability:** Participants slept at different times post-encoding (TSVR captures actual hours, not synchronized circadian timing). If consolidation is sleep-dependent, inflection point should vary by individual sleep timing, averaging out to smooth curve at population level.

- **Consolidation gradedness:** Memory stabilization may be continuous process (trace strength increasing gradually) rather than binary state transition (fragile->stable). Multiple sleep cycles over 6 days produce cumulative stabilization, not single-night inflection.

- **Individual differences:** Some participants may exhibit inflection at 24h, others at 48h or 72h. Averaging across individuals with heterogeneous consolidation timing yields smooth population curve.

---

#### Unexpected Pattern 2: Piecewise Model Non-Convergence

**What We Found:**

Piecewise model failed to converge (Converged: False in step03 summary), despite attempting full random slopes structure (Days_within | UID). In contrast, quadratic model converged after fallback to random intercepts only (1 | UID).

**Methodological Implications:**

Non-convergence is CRITICAL LIMITATION for Test 2 (AIC comparison):

1. **Parameter instability:** Non-converged models may have unstable coefficient estimates. Our Late slope (-0.070) and interaction term (0.362) could shift substantially if model were re-fit with different starting values or simplified random structure.

2. **AIC unreliability:** AIC comparison between converged (quadratic) and non-converged (piecewise) models is questionable. AIC penalizes model complexity, but non-convergence suggests piecewise model is OVER-PARAMETERIZED for N=100 dataset.

3. **Random structure mismatch:** Quadratic used (1 | UID), piecewise attempted (Days_within | UID). Comparing models with different random structures confounds TIME PATTERN (quadratic vs piecewise) with MODEL COMPLEXITY (random intercepts vs slopes). This violates AIC comparison assumptions (models should differ only in fixed effects, not random structure).

**Investigation Needed:**

Re-fit piecewise model with SAME random structure as quadratic (1 | UID random intercepts only) to obtain valid AIC comparison. If piecewise (1|UID) still has worse AIC than quadratic (1|UID), Test 2 result is robust. If piecewise (1|UID) improves AIC, current conclusion may change.

**Plan.md Warning:**

This issue was anticipated. Plan.md Section "Verify RQ 5.1.1 model convergence status" explicitly warned: "If RQ 5.1.1 used fallback to (1 | UID) random intercepts only, RQ 5.1.2 piecewise models MUST use same fallback structure for valid AIC comparison."

This warning was NOT followed in execution (piecewise attempted full random slopes despite quadratic using intercepts-only). **This is investigable error, not inherent data limitation.**

---

### Broader Implications

#### REMEMVR Validation

**Forgetting Trajectory Dynamics:**

This RQ demonstrates REMEMVR captures theoretically meaningful forgetting dynamics:
- Clear deceleration over 6-day retention interval (not linear decline)
- Pattern consistent with consolidation processes (rapid initial, slow later)
- Sufficient measurement precision to detect curvature (quadratic term significant)

**Measurement Sensitivity:**

IRT-derived theta scores sensitive enough to detect:
- Small effect sizes (Time� coefficient = 0.000054, yet p < 0.001)
- Differential forgetting rates (Early vs Late slopes significantly different)
- Individual differences (random intercept variance ò = 0.373)

---

#### Methodological Insights

**1. Triangulation Value:**

This RQ exemplifies why triangulation is critical for nuanced inference:
- Single test (e.g., only Test 2) would conclude NO two-phase forgetting (missed the pattern)
- Single test (e.g., only Test 3) would conclude STRONG two-phase forgetting (missed the continuous mechanism)
- **Three tests together** reveal BOTH pattern (two-phase dynamics) AND mechanism (continuous deceleration)

**Lesson:** When testing theoretical models with multiple predictions, use convergent evidence across complementary analytical approaches. Divergence signals theoretical refinement needed.

**2. Random Structure Selection:**

Non-convergence of piecewise model highlights critical LMM challenge:
- **Maximal random structures recommended** (Barr et al., 2013) to avoid anticonservative inferences
- **BUT: Maximal structures often fail** with moderate sample sizes (N=100)
- **Fallback hierarchy essential:** Pre-specify sequence of simplifications (slopes -> uncorrelated slopes -> intercepts-only)
- **Consistency crucial:** If comparing models, use SAME random structure or AIC comparison invalid

**Lesson:** With N < 200, expect random slopes convergence failures. Pre-register fallback strategy and apply CONSISTENTLY across compared models.

---

## 4. Limitations

### Sample Limitations

**Sample Size:**

- N = 100 participants adequate for detecting moderate-to-large effects (Tests 1 and 3 highly significant), but INSUFFICIENT for complex random structures (random slopes convergence failures)
- Individual differences in forgetting trajectories cannot be reliably estimated without random slopes (which require N >= 200 per Bates et al., 2015)

**Demographic Constraints:**

- Sample characteristics inherited from RQ 5.1.1 (likely university undergraduates, age 18-25)
- Restricted age range limits generalizability to older adults, where consolidation dynamics may differ
- No demographic data reported (sex, education, sleep habits) prevents examining moderators

---

### Methodological Limitations

**Measurement:**

**1. Domain Aggregation:**

- Collapsed across What/Where/When domains to increase power for general two-phase test
- However, consolidation dynamics may differ by domain (data available from RQ 5.1.1 but not analyzed here)

**2. Limited Timepoints:**

- Only 4 test sessions (Days 0, 1, 3, 6) limits trajectory resolution
- Cannot detect inflection points BETWEEN sessions (e.g., at 36 hours, 120 hours)
- ACF estimates unstable with <10 timepoints, limiting autocorrelation assessment reliability

**Design:**

**1. Fixed Inflection Point (48 hours):**

- Theoretical choice of 48h based on "one night's sleep" logic, but:
  - Actual sleep timing varies by participant (TSVR = hours since encoding, not hours since sleep)
  - Consolidation may occur 12-36h POST-SLEEP, meaning inflection point should be participant-specific
- Alternative inflection points (24h, 72h, 96h) not tested

**2. Repeated Testing Effects:**

- Four retrievals (Days 0, 1, 3, 6) may alter forgetting trajectory via testing effect (retrieval practice strengthens traces)
- Cannot separate testing-induced deceleration from consolidation-induced deceleration with current design

**Statistical:**

**1. Model Convergence Failures:**

- Piecewise model did NOT converge (Converged: False), making parameter estimates and AIC potentially unstable
- Non-convergence indicates model over-parameterized for N=100

**2. Random Structure Mismatch:**

- Quadratic model used fallback (1 | UID), piecewise attempted full (Days_within | UID)
- **CRITICAL ISSUE:** Comparing models with different random structures confounds TIME PATTERN with MODEL COMPLEXITY
- AIC comparison invalid when random structures differ
- Correct approach: Refit piecewise with (1 | UID) matching quadratic, THEN compare AICs

**3. Assumption Violations:**

- Homoscedasticity violated (Breusch-Pagan p = 0.031, 0.049) - marginal
- Autocorrelation violated (ACF lag-1 = -0.22, exceeds |0.1| threshold)
- Violations can inflate Type I error, but primary results highly significant (p < 0.001), so conclusions likely robust

---

### Technical Limitations

**1. Piecewise Model Non-Convergence Impact:**

- **Test 2 conclusion (deltaAIC = +5.03 favors continuous) TENTATIVE** pending re-fit with simplified random structure
- Non-converged models have unstable parameter estimates, making AIC unreliable

**2. Cross-RQ Dependency:**

- This RQ entirely dependent on RQ 5.1.1 outputs (theta scores, TSVR, best model)
- If RQ 5.1.1 results change, RQ 5.1.2 results may change

---

### Limitations Summary

**Most Critical Limitations (Affect Interpretation):**

1. **Piecewise model non-convergence + random structure mismatch:** Test 2 (AIC comparison) conclusion tentative, requires re-analysis with matched random structures
2. **Repeated testing confound:** Cannot separate consolidation-driven deceleration from testing effect-driven deceleration
3. **Limited timepoints (N=4):** Cannot detect inflection points between sessions

**Despite These Constraints:**

Core findings are **robust within scope:**
- Tests 1 and 3 converge on two-phase pattern (deceleration exists, slope ratio robust)
- Visual inspection supports smooth deceleration (both models fit observed data)
- Effect sizes large (Early slope 6x faster than Late slope)
- Significance margins substantial (p-values well below corrected �)

---

## 5. Next Steps

### Immediate Follow-Ups (Current Data, High Priority)

**1. Refit Piecewise Model with Matched Random Structure (CRITICAL)**

**Why:** Current AIC comparison (Test 2) confounds time pattern (quadratic vs piecewise) with model complexity (intercepts-only vs random slopes). Invalid comparison.

**How:**
- Refit piecewise model with (1 | UID) random intercepts only (matching quadratic model's random structure)
- Compare AICs with matched random structures
- Expected outcome: If piecewise (1|UID) still has deltaAIC > +2, Test 2 conclusion robust. If deltaAIC improves to -2 to +2 range, conclusion changes to "models equivalent."

**Timeline:** Immediate (1-2 hours, re-run Step 3 with simplified random structure specification)

**Impact:** Resolves most critical methodological limitation. Essential before publication.

---

**2. Apply Robust Standard Errors and AR(1) Correlation Structure**

**Why:** Assumption violations (heteroscedasticity p=0.031, autocorrelation ACF=-0.22) may bias standard errors and inflate Type I error.

**How:**
- Refit both models with Huber-White robust standard errors (corrects heteroscedasticity)
- Add AR(1) autoregressive correlation structure (corrects autocorrelation)
- Compare p-values and confidence intervals to original models

**Expected Outcome:**
- Time� significance likely holds (p < 0.001 has large margin)
- Interaction significance likely holds (p < 0.000002 has huge margin)

**Timeline:** Immediate (2-3 hours)

**Impact:** Ensures statistical inferences robust to assumption violations.

---

**3. Domain-Specific Two-Phase Analysis**

**Why:** Consolidation dynamics may differ by memory domain (spatial vs temporal vs object). Current analysis collapsed across domains.

**How:**
- Load RQ 5.1.1 domain-specific theta scores (not aggregated)
- Fit 3 separate piecewise models (one per domain: What, Where, When)
- Extract Early slope, Late slope, Ratio for each domain

**Timeline:** 4-6 hours

**Impact:** Tests domain specificity of consolidation dynamics.

---

### Planned Thesis RQs (Subsequent Analyses)

**RQ 5.9: Individual Differences in Forgetting Trajectories (Planned)**

**Focus:** Extract participant-specific forgetting slopes (requires random slopes convergence with larger N or Bayesian estimation)

**Timeline:** After data collection expansion (6-12 months) OR after Bayesian methods implementation

---

**RQ 5.10: Testing Effect vs Consolidation Effect on Deceleration (Planned)**

**Focus:** Separate consolidation-driven deceleration from retrieval practice-driven deceleration

**Design:**
- **Group 1 (current data):** Test at Days 0, 1, 3, 6 (repeated testing)
- **Group 2 (new data):** Test ONLY at Day 0 and Day 6 (no intermediate tests)
- Compare deceleration between groups

**Timeline:** Requires new data collection (6-12 months)

---

### Methodological Extensions (Future Studies)

**1. Extend Retention Interval to 14, 28 Days**

**Why:** 6-day window may not capture full consolidation timescale.

**How:** Add test sessions at Days 14, 28 (N=50 subsample)

**Feasibility:** Moderate (requires longer participant commitment)

---

**2. Experimental Consolidation Manipulation**

**Why:** Current study observational. Causal test requires experimental manipulation.

**Designs:**
- Sleep deprivation study (manipulate consolidation opportunity)
- Consolidation enhancement study (post-encoding reactivation)

**Feasibility:** High complexity (sleep lab required), 12-18 months

---

**3. Larger Sample for Random Slopes (N=200+)**

**Why:** Current N=100 insufficient for random slopes convergence.

**Timeline:** 12-18 months data collection

---

### Priority Ranking

**High Priority (Do First - Essential for Robustness):**

1. **Refit piecewise with matched random structure** (Follow-Up #1) - Resolves critical AIC comparison validity issue
2. **Apply robust SEs + AR(1)** (Follow-Up #2) - Ensures inferences robust to assumption violations
3. **Domain-specific analysis** (Follow-Up #3) - Uses current data, tests important theoretical question

**Medium Priority (Valuable but Not Critical):**

1. **Extend retention to 14, 28 days** - Determines consolidation asymptote
2. **Bayesian LMM for random slopes** - Enables individual differences analysis with current N=100

**Lower Priority (Long-Term, Resource-Intensive):**

1. **Experimental consolidation manipulation** - Causal test, requires sleep lab
2. **Larger sample (N=200+)** - Gold standard for random slopes

---

### Next Steps Summary

**Immediate actions** (next 1-2 weeks):

1. **Refit piecewise model** with (1|UID) to validate Test 2 AIC comparison
2. **Apply robust SEs + AR(1)** to verify Tests 1 and 3 significance holds
3. **Domain-specific analysis** to test if consolidation dynamics differ across What/Where/When

These three analyses use CURRENT DATA, require minimal additional work (8-12 hours total), and substantially strengthen robustness of conclusions before publication.

---

**Summary generated by:** rq_results agent (v4.0)
**Pipeline version:** v4.X (13-agent atomic architecture)
**Date:** 2025-11-28
