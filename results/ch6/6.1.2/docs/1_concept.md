# RQ 6.1.2: Two-Phase Pattern in Confidence Decline

**Chapter:** 6
**Type:** Confidence
**Subtype:** Two-Phase Pattern
**Full ID:** 6.1.2

---

## Research Question

**Primary Question:**
Does confidence decline show the same two-phase pattern (rapid early, slow late) as accuracy?

**Scope:**
This RQ examines confidence trajectories across a 6-day retention interval using IRT-derived theta scores from graded response model (5-category ordinal confidence data). Analyzes N=100 participants x 4 test sessions = 400 observations. Tests for two-phase pattern with 48-hour breakpoint separating Early (0-48h) and Late (48-144h) segments.

**Theoretical Framing:**
If sleep-dependent consolidation affects metacognitive monitoring similarly to memory traces, confidence should exhibit the same two-phase pattern found for accuracy in Chapter 5: rapid decline Day 0->1, slower decay Day 1->6. Tests whether metacognition parallels memory dynamics.

---

## Theoretical Background

**Relevant Theories:**
- **Sleep-Dependent Consolidation Theory:** Consolidation processes during sleep stabilize memory traces, leading to differentiated forgetting patterns across early (pre-consolidation) and late (post-consolidation) retention intervals.
- **Metacognitive Monitoring Theory:** Confidence judgments reflect underlying memory strength. If consolidation affects memory traces, metacognitive monitoring should track these changes, showing parallel two-phase patterns.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
Sleep-dependent consolidation should affect metacognitive monitoring similarly to memory traces. Confidence decline should show rapid early decay (Day 0->1, pre-consolidation instability) followed by slower late decay (Day 1->6, post-consolidation stabilization).

**Literature Gaps:**
[To be identified by rq_scholar]

---

## Hypothesis

**Primary Hypothesis:**
Confidence exhibits two-phase pattern paralleling accuracy: rapid decline Day 0->1, slower decay Day 1->6.

**Evidence Criteria (2/3 tests required):**
1. Significant quadratic term (p < 0.01 Bonferroni correction)
2. Piecewise model AIC < continuous model by > 2
3. Late/Early slope ratio < 0.5

**Theoretical Rationale:**
Sleep-dependent consolidation creates differential forgetting dynamics. If Chapter 5 accuracy showed two-phase pattern, and confidence tracks memory strength, confidence should replicate this pattern. Metacognitive monitoring should be sensitive to consolidation-driven changes in memory stability.

**Expected Effect Pattern:**
- **Early segment (0-48h):** Steep negative slope (rapid confidence decline)
- **Late segment (48-144h):** Shallow negative slope (slow confidence decline)
- **Breakpoint:** 48 hours (nominal Day 1, post-sleep consolidation)
- **Success:** 2 out of 3 statistical tests support two-phase pattern, OR all 3 NULL (replicating accuracy pattern from Ch5 5.1.2)

---

## Memory Domains

**Domains Examined:**

- [x] **Omnibus "All" Factor**
  - Description: Single factor combining all confidence items (TC_*)
  - Rationale: Parallel to Ch5 5.1.2 which examined omnibus accuracy factor
  - Note: 5-category ordinal confidence data (0, 0.25, 0.5, 0.75, 1.0)

**Inclusion Rationale:**
RQ 6.1.2 uses omnibus "All" factor to directly parallel Ch5 5.1.2 accuracy analysis. This allows clean comparison of whether two-phase pattern replicates across accuracy vs confidence measures. Domain-specific analyses deferred to Type 6.3 (Domain Confidence).

**Exclusion Rationale:**
Domain-specific factors (What/Where/When), paradigm-specific factors (IFR/ICR/IRE), and congruence factors (Common/Congruent/Incongruent) excluded from this RQ. These are examined in separate Type 6.3, 6.4, and 6.5 RQs respectively.

---

## Analysis Approach

**Analysis Type:**
Linear Mixed Models (LMM) with piecewise time segments + quadratic models for two-phase pattern testing

**High-Level Workflow:**

**Step 0:** Load theta_confidence scores from RQ 6.1.1 (IRT-derived confidence ability estimates from 5-category GRM)

**Step 1:** Create piecewise time variables with 48-hour breakpoint (Early: 0-48h, Late: 48-144h)

**Step 2:** Test 1 - Quadratic model: Fit LMM with Time + Time^2, test quadratic term significance (Bonferroni alpha=0.01)

**Step 3:** Test 2 - Piecewise vs continuous comparison: Fit piecewise model (separate slopes for Early/Late segments), compare AIC to continuous linear model, require delta AIC > 2

**Step 4:** Test 3 - Slope ratio: Compute Early segment slope and Late segment slope, compute Late/Early ratio, require ratio < 0.5 for two-phase evidence

**Step 5:** Compare pattern to Ch5 5.1.2 accuracy two-phase analysis (document if confidence replicates accuracy pattern or diverges)

**Expected Outputs:**
- results/step02_quadratic_model_summary.txt (quadratic term test, p-value)
- results/step03_piecewise_comparison.csv (AIC values for piecewise vs continuous models)
- results/step04_slope_ratio.csv (Early slope, Late slope, ratio)
- results/step05_ch5_comparison.csv (comparison to Ch5 5.1.2 findings)
- plots/step06_twophase_theta_data.csv (plot source data showing two-phase pattern)

**Success Criteria:**
- All models converge successfully
- 2 out of 3 tests support two-phase pattern (quadratic significant, piecewise preferred, slope ratio < 0.5), OR all 3 tests NULL (replicating Ch5 5.1.2 accuracy pattern)
- Comparison to Ch5 5.1.2 documented (does confidence parallel accuracy?)
- Plot data complete and ready for visualization

---

## Data Source

**Data Type:**
DERIVED (from RQ 6.1.1 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 6.1.1 (Confidence Model Selection)

**File Paths:**
- results/ch6/6.1.1/data/step03_theta_confidence.csv (IRT-derived confidence ability estimates, 400 rows)
- results/ch6/6.1.1/data/step00_tsvr_mapping.csv (time mapping: UID x TEST x TSVR hours)

**Dependencies:**
RQ 6.1.1 must complete Steps 1-3 (IRT Pass 1 GRM calibration, item purification, IRT Pass 2 re-calibration) before this RQ can run. Requires theta_confidence scores from 5-category graded response model.

**Comparison Dependency:**
Ch5 5.1.2 results required for pattern comparison (does confidence two-phase pattern replicate accuracy two-phase pattern?)

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants from RQ 6.1.1 (N=100, inherited inclusion criteria)

**Items:**
- N/A (theta scores already aggregated across items)
- Note: RQ 6.1.1 item purification already applied (items with |b| > 3.0 OR a < 0.4 excluded)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4; nominal Days 0, 1, 3, 6)
- Time variable: TSVR (actual hours since encoding), not nominal days

**Segments:**
- Early segment: 0-48 hours (Day 0 to Day 1)
- Late segment: 48-144 hours (Day 1 to Day 6)
- Breakpoint: 48 hours (paralleling Ch5 5.1.2)

---
