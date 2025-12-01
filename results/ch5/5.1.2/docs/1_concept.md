# RQ 5.1.2: Evidence for Two-Phase Forgetting (Rapid then Slow)

**Chapter:** 5
**RQ Number:** 1.2
**Full ID:** 5.1.2

---

## Research Question

**Primary Question:**
Do data support a two-phase model with rapid initial decline (Day 0-1) followed by slower decay (Day 1-6)?

**Scope:**
This RQ examines forgetting rate changes across the 6-day retention interval using IRT-derived theta scores from RQ 5.1.1. Tests whether forgetting exhibits two distinct phases: rapid pre-consolidation (0-48 hours TSVR) and slower post-consolidation (48-240 hours TSVR). Analysis uses three convergent tests: (1) quadratic term significance, (2) piecewise vs continuous model comparison via AIC, (3) early vs late slope ratio.

**Theoretical Framing:**
Consolidation theory predicts rapid forgetting during pre-consolidation (before memory stabilization) followed by slower forgetting after consolidation. If episodic memories undergo consolidation primarily during first 24 hours (one night's sleep), forgetting trajectory should show inflection point around Day 1, with steeper initial slope transitioning to shallower slope post-consolidation.

---

## Theoretical Background

**Relevant Theories:**
- **Consolidation Theory** (Dudai, 2004; Hardt et al., 2013): Newly encoded memories undergo time-dependent stabilization process. During consolidation, memories are vulnerable and forgetting is rapid. After consolidation, memories stabilize and forgetting decelerates. Hippocampal-dependent episodic memories consolidate over ~24 hours (one sleep cycle).
- **Multiple Trace Theory** (Nadel & Moscovitch, 1997): Predicts episodic memories require hippocampus indefinitely, but consolidation still affects retrieval efficiency. Initial encoding creates fragile trace; consolidation strengthens trace over days.

**Key Citations:**
- Dudai (2004): Consolidation theory framework for memory stabilization processes
- Hardt et al. (2013): Review of consolidation mechanisms and time course
- Ebbinghaus (1885/1964): Classic forgetting curve shows rapid initial decline with deceleration over time
- Wixted & Ebbesen (1991): Two-component model of forgetting (fast + slow components)

**Theoretical Predictions:**
Consolidation theory predicts two-phase forgetting: (1) Rapid pre-consolidation phase (Day 0-1, before sleep-dependent stabilization) with steep forgetting slope, (2) Slower post-consolidation phase (Day 1-6, after stabilization) with shallow forgetting slope. Inflection point should occur around Day 1 (after one night's sleep). Early/Late slope ratio should be < 0.5 if two-phase pattern is robust.

**Literature Gaps:**
Most forgetting studies use continuous models (exponential, power) that assume constant forgetting rate or smooth deceleration. Few studies explicitly test piecewise models to detect consolidation-related inflection points. VR-based episodic memory with precise time-since-encoding (TSVR) allows fine-grained test of two-phase hypothesis at theoretically meaningful inflection point (24-hour consolidation window).

---

## Hypothesis

**Primary Hypothesis:**
Forgetting exhibits two distinct phases: rapid initial decline (Day 0-1, pre-consolidation) followed by slower decay (Day 1-6, post-consolidation). Evidence will come from convergence of three tests: (1) significant quadratic term (positive curvature = deceleration), (2) piecewise model fits better than continuous model (ΔAIC < -2), (3) Late/Early slope ratio < 0.5.

**Secondary Hypotheses:**
1. Quadratic term will be positive and significant (p < 0.003333 Bonferroni-corrected), indicating concave-up curvature (deceleration over time)
2. Piecewise model will have lower AIC than best continuous model from RQ 5.1.1 (ΔAIC < -2)
3. Visual inspection will show clear inflection point at Day 1 (24-hour mark, one night's sleep)

**Theoretical Rationale:**
Consolidation theory predicts memory traces undergo time-dependent stabilization during first ~24 hours post-encoding. During this vulnerable period, forgetting is rapid. After consolidation, traces are stabilized and forgetting decelerates. Sleep plays critical role in consolidation, so inflection point should occur after first night's sleep (~Day 1). VR-based episodic memories are hippocampal-dependent and thus subject to consolidation dynamics.

**Expected Effect Pattern:**
Quadratic model: Theta ~ Time + Time² + (Time | UID) will show significant positive Time² coefficient (p < 0.003333). Piecewise model: Theta ~ Days_within × Segment + (Days_within | UID) will have AIC at least 2 points lower than best continuous model. Early segment slope (0-48 hours) will be ~4x steeper than Late segment slope (48-240 hours), yielding ratio ~0.25. Segment × Time interaction will be significant (p < 0.003333).

---

## Memory Domains

**Note:** This RQ uses aggregate theta scores from RQ 5.1.1. Domain information inherited from RQ 5.1.1 analysis.

**Domains Examined (from RQ 5.1.1):**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object identity / naming

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location, legacy)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Disambiguation: All Where tags included (inherited from RQ 5.7)

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order / sequence

**Inclusion Rationale:**
This RQ uses theta scores from RQ 5.1.1, which examined all three WWW domains. Analysis collapses across domains to test whether forgetting trajectory shows two-phase pattern regardless of domain. Domain-specific two-phase patterns could be examined in future RQ, but this RQ focuses on general two-phase evidence.

**Exclusion Rationale:**
None - inherits all domains from RQ 5.1.1.

---

## Analysis Approach

**Analysis Type:**
LMM (Linear Mixed Models) for trajectory modeling with three convergent tests: (1) Quadratic term significance, (2) Piecewise vs continuous model comparison via AIC, (3) Early vs late slope extraction and ratio computation

**High-Level Workflow:**

**Step 0:** Get Data - Load theta scores and best-fitting continuous model from results/ch5/5.1.1/, load TSVR mapping

**Step 1:** Data Preparation - Create time transformations (TSVR, TSVR², log(TSVR+1)), create piecewise time structure (Early: 0-48 hours, Late: 48-240 hours) with Days_within variable for each segment

**Step 2:** Test 1 - Quadratic Term Significance - Fit Theta ~ Time + Time² + (Time | UID), **model selection strategy:** attempt full random slopes model (Time | UID) first, if convergence fails (checked via validate_lmm_convergence), simplify to: (1) uncorrelated random slopes (Time || UID) (removes intercept-slope correlation parameter), (2) if still fails, random intercepts only (1 | UID), with N=100, quadratic random slopes may not converge (Bates et al., 2015 recommend N>=200 for complex random structures), extract Time² coefficient and p-value, apply Bonferroni correction (α = 0.0033), significant positive coefficient = evidence for deceleration (two-phase)

**Step 3:** Test 2 - Piecewise vs Continuous Model Comparison - Fit Theta ~ Days_within × Segment + (Days_within | UID), **model selection strategy:** same fallback as Step 2 - attempt random slopes, simplify if convergence fails, compare AIC to best continuous model from RQ 5.7, ΔAIC < -2 favors piecewise (two-phase), ΔAIC > +2 favors continuous (single-phase), |ΔAIC| < 2 = equivalent

**Step 3.5:** Validate LMM Assumptions - After fitting quadratic and piecewise models, perform comprehensive assumption checks: (1) Residual normality via Q-Q plots + Shapiro-Wilk test (p>0.05 threshold), (2) Homoscedasticity via residual vs fitted plot (visual inspection for funnel patterns), (3) Random effects normality via Q-Q plots of random intercepts/slopes, (4) Independence via ACF plots (Lag-1 ACF < 0.1 threshold - repeated measures data), (5) Linearity within segments via partial residual plots, use validate_lmm_assumptions_comprehensive tool for automated checks, **remedial actions:** if residual normality violated, use robust standard errors; if homoscedasticity violated, model variance structure; if autocorrelation detected, add AR(1) correlation structure; document all assumption test results in validation report

**Step 4:** Test 3 - Extract Early vs Late Forgetting Rates - Extract slope for Early segment (0-48 hours), extract slope for Late segment (48-240 hours), compute Late/Early ratio (expect < 0.5 if two-phase robust), test Segment × Time interaction significance

**Step 5:** Visualization - Plot observed means with error bars, overlay continuous model predictions from RQ 5.7, overlay piecewise model predictions, highlight inflection point at Day 1

**Data Preprocessing (Per Solution Section 1.4):**
- **No IRT preprocessing:** Uses pre-computed theta scores from RQ 5.7
- **Time Variable:** TSVR_hours (actual hours since encoding), same as RQ 5.7
- **Piecewise Structure:** Early segment = [0, 48) hours TSVR (Day 0-1, excluding 48h), Late segment = [48, 240] hours TSVR (Day 1-6, including 48h)
- **Days_within:** Time variable recentered within each segment (0 = segment start)

**Special Methods:**
- **Triangulation via Three Convergent Tests:** Quadratic term, AIC comparison, slope ratio - convergence strengthens inference
- **Bonferroni Correction:** α = 0.05/15 = 0.003333 corrects for family of 15 research questions in Chapter 5 (per thesis-wide multiple testing control strategy), applies to quadratic term and Segment × Time interaction as primary hypothesis tests for this RQ, conservative approach controls experiment-wise error rate across all Chapter 5 analyses, follows Bender & Lange (2001) guidelines for pre-planned multiple comparisons in related research questions
- **AIC Decision Rule:** ΔAIC < -2 (piecewise superior), ΔAIC > +2 (continuous superior), |ΔAIC| < 2 (equivalent)
- **Theoretical Inflection Point:** 48 hours TSVR chosen based on consolidation theory (one night's sleep + ~24 hour consolidation window)
- **Model Comparison to RQ 5.7:** Uses best-fitting continuous model from RQ 5.7 as baseline (avoids re-fitting multiple continuous models)
- **Convergence Fallback Strategy:** Quadratic random slopes (Time | UID) may not converge with N=100 participants, fallback hierarchy: (1) attempt maximal model (Time | UID), (2) if fails, simplify to uncorrelated slopes (Time || UID), (3) if still fails, random intercepts only (1 | UID), document convergence decisions in results, same strategy applies to piecewise model with Days_within random slopes
- **Convergence Failure Impact on Triangulation:** If convergence failures occur requiring fallback to random intercepts only (1 | UID), triangulation evidence will apply to population-average trajectory, not individual-level patterns. In this scenario, we can only claim two-phase pattern describes average forgetting across participants, not that all individuals exhibit two-phase forgetting. Convergence status will be reported transparently in validation report. If random slopes converge for one model but not the other, this asymmetry will be discussed as methodological limitation. Interpretation will acknowledge that N=100 may be insufficient to detect individual variability in forgetting trajectories for complex models (per Bates et al. 2015 recommendation N>=200 for random slopes).
- **Comprehensive LMM Assumption Validation:** After fitting quadratic and piecewise models, validate assumptions via validate_lmm_assumptions_comprehensive tool (performs 6 assumption checks: normality, homoscedasticity, autocorrelation, etc.), comprehensive validation critical with N=100 and complex random structures where assumption violations can substantially affect Type I error rates (Schielzeth et al., 2020), report all assumption test results with remedial actions if violations detected

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.1.1 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 5.1.1 (Which functional form best describes forgetting trajectories?)

**File Paths:**
- `results/ch5/5.1.1/data/step02_theta_long.csv` - Theta scores from RQ 5.1.1 IRT analysis
  - Columns: UID, test, domain, theta
- `results/ch5/5.1.1/data/step00_tsvr_mapping.csv` - Time Since VR mapping
  - Columns: UID, test, TSVR (hours since encoding)
- `results/ch5/5.1.1/data/step03_best_model.pkl` - Pickled best-fitting continuous model from RQ 5.1.1 (for comparison)

**Dependencies:**
RQ 5.1.1 must complete all steps (IRT calibration, purification, theta extraction, LMM trajectory modeling with 5 candidate models, best model selection) before this RQ can run. Specifically requires:
- Step 2 output (theta scores)
- Step 0 output (TSVR mapping)
- Step 3 output (best continuous model for AIC comparison)

**Usage:**
This RQ uses aggregate theta scores (collapsed across domains) from RQ 5.1.1 as outcome variable. Tests whether forgetting trajectory shows two-phase pattern (rapid then slow) using quadratic term, piecewise model, and slope ratio. Best continuous model from RQ 5.1.1 serves as baseline for piecewise model comparison.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants from RQ 5.1.1 (inherited inclusion criteria - all 100 participants)

**Items:**
- N/A (theta scores already aggregated per participant × test, collapsed across items)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4 - inherited from RQ 5.1.1)
- Note: TSVR values vary by participant (actual hours since encoding), not nominal days

**Domains:**
- Note: Analysis collapses across What/Where/When domains (uses aggregate theta, not domain-specific)
- Inherited domain inclusion from RQ 5.1.1 (all three WWW domains)

---
