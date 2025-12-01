# RQ 5.4.2: Congruent Items and Early Consolidation

**Chapter:** 5
**RQ Number:** 5.4.2
**Full ID:** 5.4.2

---

## Research Question

**Primary Question:**
Is the schema congruence effect on forgetting driven by differential consolidation (Day 0→1) or later decay (Day 1→6)?

**Scope:**
This RQ examines whether schema-congruent items benefit more from early consolidation (the critical sleep-dependent consolidation window occurring between Day 0 and Day 1) compared to incongruent items. The analysis uses piecewise regression to model two distinct temporal phases: Early segment (Days 0-1, consolidation-dominated) and Late segment (Days 1-6, decay-dominated). The investigation focuses on whether the congruence effect observed in RQ 5.5 is primarily a consolidation phenomenon or a general forgetting rate difference.

**Theoretical Framing:**
Sleep-dependent consolidation theory predicts that schema-consistent memories preferentially benefit from hippocampal-neocortical dialogue during sleep. If this prediction holds, congruent items should show less forgetting specifically during the Early segment (which includes one night's sleep), while the congruence effect may diminish during the Late segment (where multiple nights dilute per-night effects). This RQ tests a mechanistic prediction about when schema effects emerge in the forgetting trajectory.

---

## Theoretical Background

**Relevant Theories:**
- **Sleep Consolidation Theory** (Stickgold & Walker, 2013; Rasch & Born, 2013; Stickgold, 2005): Schema-consistent memories preferentially benefit from hippocampal-neocortical dialogue during sleep. Sleep-dependent consolidation is particularly important for integrating new memories with existing knowledge structures.
- **Schema Theory** (Bartlett, 1932; Ghosh & Gilboa, 2014): Pre-existing knowledge structures (schemas) facilitate encoding, consolidation, and retrieval of congruent information. Congruent items are more efficiently integrated into long-term memory.
- **Systems Consolidation** (McClelland et al., 1995): Initially hippocampus-dependent memories gradually become distributed in neocortex over time. Schema-congruent items may consolidate faster due to existing neocortical representations.

**Key Citations:**
- Stickgold & Walker (2013): Sleep consolidation benefits schema-consistent memories
- Rasch & Born (2013): Hippocampal-neocortical dialogue during sleep
- Stickgold (2005): Sleep-dependent memory consolidation mechanisms
- Bartlett (1932): Schema theory foundations
- Ghosh & Gilboa (2014): Schema effects on memory consolidation
- McClelland et al. (1995): Complementary learning systems theory

**Theoretical Predictions:**
Sleep consolidation theory predicts a 3-way interaction: Congruent items should show less decline during the Early segment (consolidation window with one night's sleep) compared to Incongruent items. This differential benefit should be less pronounced during the Late segment (Days 1-6), where consolidation is complete and decay dominates. The Early segment captures the critical window where schema-based consolidation mechanisms are most active.

**Literature Gaps:**
Most schema studies examine encoding or single-delay retrieval. Few studies test whether schema effects emerge specifically during early consolidation (0-24h with sleep) versus later decay. This RQ uses piecewise regression to isolate consolidation-specific effects, testing a mechanistic prediction about when schema benefits occur rather than just whether they occur overall.

---

## Hypothesis

**Primary Hypothesis:**
Congruent items will show less forgetting during the consolidation window (Day 0-1) compared to incongruent items, as schema-based memory benefits from sleep-dependent consolidation. The congruence effect may be less pronounced during later decay (Day 1-6).

**Secondary Hypotheses:**
1. Early segment slopes (Days 0-1) will be steeper than Late segment slopes (Days 1-6) for all congruence types, reflecting two-phase forgetting (rapid consolidation phase, slower decay phase)
2. The 3-way interaction (Days_within × Segment × Congruence) will be significant, indicating that the congruence effect is stronger in the Early segment than the Late segment
3. In the Late segment, congruence effects will diminish as all memory types enter the decay-dominated phase

**Theoretical Rationale:**
Sleep consolidation theory predicts schema-congruent memories benefit from hippocampal-neocortical dialogue during sleep. The Early segment (Day 0-1) includes one night's sleep - the critical window for consolidation. If schema effects are consolidation-driven, they should emerge most strongly here. The Late segment (Day 1-6) includes multiple nights, diluting per-night effects, and represents decay-dominated forgetting where consolidation is largely complete. Piecewise regression isolates these distinct processes.

**Expected Effect Pattern:**
Significant 3-way interaction: Days_within × Segment[Late] × Congruence[Congruent]. This interaction tests whether the congruence effect (Congruent vs Incongruent slope difference) differs between Early and Late segments. Expected pattern: Congruent slope less negative than Incongruent in Early segment, with this difference reduced in Late segment. Alpha = 0.0033 with Bonferroni correction (also report uncorrected).

---

## Memory Domains

**Domains Examined:**

- [ ] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object identity / naming

- [ ] **Where** (Spatial Location)
  - [ ] `-L-` tags (general location, legacy)
  - [ ] `-U-` tags (pick-up location)
  - [ ] `-D-` tags (put-down location)
  - Disambiguation: N/A - domains not examined in this RQ

- [ ] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order / sequence

**Inclusion Rationale:**
This RQ does NOT examine memory domains (What/Where/When). Instead, it examines items categorized by schema congruence (Congruent, Common, Incongruent). The analysis focuses on how schema consistency affects consolidation and decay processes, not domain-specific forgetting. Memory domains are orthogonal to this RQ's focus.

**Exclusion Rationale:**
Memory domains (What/Where/When) are excluded because this RQ tests a different theoretical question: whether schema congruence effects are consolidation-driven. Domain-specific effects are addressed in RQ 5.1-5.2. Here, items are aggregated across domains and analyzed by congruence category.

---

## Analysis Approach

**Analysis Type:**
IRT (Item Response Theory) for ability estimation + Piecewise LMM (Linear Mixed Models) with 3-way interaction for consolidation vs decay modeling

**High-Level Workflow:**

**Step 0:** Get Data - Use theta scores from RQ 5.5 ("Items by Congruence" analysis)

**Step 1:** Data Preparation
- Reshape theta scores to long format (Congruence as factor variable: Common/Congruent/Incongruent)
- Create piecewise time structure with two segments:
  - Early segment: Days 0-1 (consolidation window, includes one night's sleep)
  - Late segment: Days 1-6 (decay-dominated phase)
  - CRITICAL: Assign Day 1 to Early only (no overlap between segments)
- Create "Days_within" variable (centered at 0 for each segment start)
- Verify no overlap in segment assignments

**Step 2:** Piecewise LMM with 3-Way Interaction
- Formula: Theta ~ Days_within × Segment × Congruence
- Treatment coding: Common as reference congruence, Early as reference segment
- Random effects: Intercepts and slopes by UID (participant)
- Fit with REML=False (for model comparison)
- Save model pickle

**Step 3:** Extract Segment-Specific Slopes
- Extract early segment slopes (Common/Congruent/Incongruent)
- Extract late segment slopes (Common/Congruent/Incongruent)
- Create summary table with slopes, SEs, and 95% CIs

**Step 4:** Test Key Hypothesis - Congruent Consolidation Benefit
- Hypothesis: Congruent items show less decline in Early segment than Incongruent
- Extract 3-way interaction term: Days_within × Segment[Late] × Congruence[Congruent]
- Test significance with and without Bonferroni correction (α = 0.0033)

**Step 5:** Visualization
- Generate two-panel piecewise trajectory plot (Early | Late)
- Three lines per panel (Common/Congruent/Incongruent)
- Show observed means and model predictions
- Highlight Early-Late slope differences and congruence effects

**Data Preprocessing (Per Solution Section 1.4):**
- **Accuracy Scores:** Dichotomize before IRT (1 = 1, <1 = 0) - inherited from RQ 5.5
- **Confidence Ratings:** Use raw 1-5 Likert (no bias correction) - inherited from RQ 5.5
- **IRT Model:** GRM (Graded Response Model) - inherited from RQ 5.5
- **Theta Scores:** Use pre-computed theta estimates from RQ 5.5, no re-calibration needed

**Special Methods:**
- **Piecewise Regression:** Models different processes (consolidation vs decay) operating in different time windows. Critical design choice: Day 1 assigned to Early segment only (no overlap) because one night's sleep defines the consolidation window.
- **3-Way Interaction:** Tests if consolidation benefit (Early segment) differs by congruence type. This interaction isolates the mechanistic prediction of sleep consolidation theory.
- **Segment Definition:** Early (Days 0-1) includes one night's sleep (critical consolidation window). Late (Days 1-6) includes multiple nights, diluting per-night effects.
- **Treatment Coding:** Common congruence as reference (baseline), Early segment as reference. Allows direct interpretation of interaction term.

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.5 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 5.5 (Schema Congruence Effects on Forgetting)

**File Paths:**
- `results/ch5/rq5/data/step03_theta_scores.csv` (IRT ability estimates by congruence)
- Expected columns: UID, Test, Congruence (Common/Congruent/Incongruent), theta

**Dependencies:**
RQ 5.5 must complete Steps 1-3 (IRT calibration on "Items by Congruence" factor structure, purification, theta extraction) before this RQ can run. RQ 5.6 uses the same theta estimates but applies a different temporal modeling strategy (piecewise regression instead of continuous time).

**Usage:**
This RQ uses theta scores from RQ 5.5 as outcome variable for piecewise LMM. No re-calibration needed - same IRT model, different LMM structure (consolidation vs decay phases).

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants from RQ 5.5 (inherited inclusion criteria)
- Expected N = 100 participants × 4 tests = 400 observations

**Items:**
- N/A (theta scores already aggregated by congruence category, not individual items)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4)
- Note: Tests are assigned to segments (T1-T2 = Early, T3-T4 = Late) but all four tests are included

**Additional Variables:**
- Segment (Early: Tests 1-2, Late: Tests 3-4)
- Days_within_segment (time variable centered at 0 for each segment start)
- Congruence (Common/Congruent/Incongruent) - inherited from RQ 5.5

---

## Validation Procedures

**Validation Type:**
LMM Assumption Validation + Convergence Diagnostics + Sensitivity Analyses

**Rationale:**
Piecewise LMM with 3-way interaction requires rigorous assumption validation to ensure valid statistical inference. With N=100 participants at the lower bound for random slopes (Newsom recommends 100-200 groups), convergence diagnostics are critical. Assumption violations can inflate Type I error rates, producing false positives. This section specifies comprehensive validation procedures following Pinheiro & Bates (2000) and Schielzeth et al. (2020) guidelines.

---

### 7.1 LMM Assumption Validation

**Six Core Diagnostic Checks:**

1. **Residual Normality**
   - Visual: Q-Q plot of standardized residuals
   - Quantitative: Shapiro-Wilk test (p > 0.05 acceptable)
   - Threshold: Moderate departures acceptable (LMM robust to normality violations with N=100)
   - Remedial action if violated: Check for outliers, consider robust standard errors

2. **Residual Homoscedasticity**
   - Visual: Residuals vs fitted values plot (should show random scatter, no funnel pattern)
   - Quantitative: Levene's test or Breusch-Pagan test (p > 0.05 acceptable)
   - Threshold: Variance ratio across groups < 3:1 acceptable
   - Remedial action if violated: Log-transform outcome (theta), add variance structure to model

3. **Random Effects Normality**
   - Visual: Q-Q plots for random intercepts and random slopes
   - Quantitative: Shapiro-Wilk test on BLUPs (Best Linear Unbiased Predictors)
   - Threshold: p > 0.01 (more lenient than residuals)
   - Remedial action if violated: Check for outlier participants, consider simplifying random effects

4. **Autocorrelation**
   - Visual: ACF (autocorrelation function) plot of residuals within participants
   - Quantitative: Durbin-Watson statistic (1.5-2.5 acceptable range)
   - Threshold: First-order autocorrelation |r| < 0.3 acceptable
   - Remedial action if violated: Add AR(1) correlation structure to model

5. **Outlier Detection**
   - Identify observations with |standardized residual| > 3
   - Identify participants with random effects > 3 SD from mean
   - Cook's distance for influential observations (D > 4/n threshold)
   - Remedial action: Report outliers, run sensitivity analysis with/without outliers

6. **Multicollinearity**
   - Compute VIF (Variance Inflation Factor) for fixed effects
   - Threshold: VIF < 5 acceptable, VIF < 10 tolerable
   - Remedial action if violated: Unlikely with orthogonal time variable, but center predictors if needed

---

### 7.2 Convergence Diagnostics

**Random Slopes Model Selection Strategy:**

The piecewise LMM includes random intercepts and random slopes by UID (participant). With N=100 participants, this is at the lower boundary for random slopes models (Newsom: 100-200 groups recommended). Convergence failures are plausible.

**Model Selection Protocol:**

1. **Attempt maximal random slopes first** (Days_within × Segment random slopes)
2. **Check singular fit warnings** from statsmodels
3. **If convergence fails:**
   - Simplify to random intercepts only (remove random slopes)
   - Check convergence again
4. **If both converge:**
   - Compare via Likelihood Ratio Test (LRT)
   - Use AIC/BIC as secondary criteria
5. **Document final model and justification** in results

**Convergence Criteria:**

- No singular fit warnings (indicates variance-covariance matrix issues)
- All variance components > 0 (negative variances indicate model misspecification)
- Gradient norm < 0.01 (indicates successful optimization)
- Hessian matrix positive definite (indicates valid curvature at MLE)

**Remedial Actions if Convergence Fails:**

- Simplify random effects structure (intercepts only)
- Check for collinearity in fixed effects
- Increase maximum iterations (default 100 → 200)
- Try different optimization algorithms (if available in statsmodels)

---

### 7.3 Bonferroni Test Family Definition

**Test Family for Bonferroni Correction:**

The concept document states α = 0.0033 but does not explicitly define the test family. To ensure appropriate Type I error control, we specify:

**Primary Test Family (15 tests total):**

1. 3-way interaction: Days_within × Segment[Late] × Congruence[Congruent]
2. 3-way interaction: Days_within × Segment[Late] × Congruence[Incongruent]
3. 2-way interaction: Days_within × Congruence[Congruent] (Early segment)
4. 2-way interaction: Days_within × Congruence[Incongruent] (Early segment)
5. 2-way interaction: Days_within × Segment[Late] (Common congruence)
6. 2-way interaction: Segment[Late] × Congruence[Congruent] (across time)
7. 2-way interaction: Segment[Late] × Congruence[Incongruent] (across time)
8. Main effect: Days_within (Early segment, Common congruence)
9. Main effect: Segment[Late] (Common congruence, Day 0)
10. Main effect: Congruence[Congruent] (Early segment, Day 0)
11. Main effect: Congruence[Incongruent] (Early segment, Day 0)
12. Post-hoc contrast: Congruent vs Incongruent (Early segment slopes)
13. Post-hoc contrast: Congruent vs Incongruent (Late segment slopes)
14. Post-hoc contrast: Early vs Late (Congruent slopes)
15. Post-hoc contrast: Early vs Late (Incongruent slopes)

**Bonferroni Correction:** α = 0.05 / 15 = 0.0033 (FWER control)

**Rationale:** Pre-specified test family defined a priori to control Family-Wise Error Rate (FWER) per Bonferroni principles. All 15 tests are theoretically motivated by the piecewise LMM 3-way interaction design.

**Reporting:** Per Decision D068, report both uncorrected (α = 0.05) and Bonferroni-corrected (α = 0.0033) p-values in all results tables.

---

### 7.4 Sensitivity Analyses

**Three Sensitivity Analyses to Assess Robustness:**

1. **Piecewise vs Continuous Time Models**
   - Compare piecewise LMM (Early/Late segments) to continuous time models (Linear, Logarithmic, Lin+Log)
   - Rationale: Piecewise model assumes discrete regime change at Day 1; continuous models assume smooth trajectory
   - Evaluation: If continuous models fit better (lower AIC), piecewise assumption may be unjustified
   - Expected outcome: Piecewise should fit better if consolidation vs decay are distinct processes

2. **Knot Placement Sensitivity**
   - Test alternative knot placements: Day 0.5, Day 1.0, Day 1.5
   - Rationale: Day 1 knot is theoretically motivated (one night's sleep) but arbitrary
   - Evaluation: If results highly sensitive to knot placement, conclusions fragile
   - Expected outcome: Day 1 knot should yield best fit based on sleep consolidation theory

3. **Derived Data Weighting**
   - Weight observations by inverse variance of theta estimates (IRT standard errors)
   - Rationale: Theta scores have heterogeneous precision (varies by participant ability and item parameters)
   - Evaluation: If results change substantially, conclusions may be driven by imprecise theta estimates
   - Expected outcome: Weighting should strengthen effects (downweight noisy estimates)

**Reporting:** Document all sensitivity analyses in results. If primary conclusions robust across all three analyses, confidence in findings increases. If sensitive, interpret results cautiously.

---
