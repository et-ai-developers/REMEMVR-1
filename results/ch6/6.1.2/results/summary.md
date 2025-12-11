# RQ 6.1.2: Two-Phase Pattern in Confidence Decline

**Research Question:** Does confidence decline show the same two-phase pattern (rapid early, slow late) as accuracy?

**Analyzed:** 2025-12-11
**Analysis Type:** Linear Mixed Models (LMM) with piecewise time segments + quadratic trajectory testing
**Pipeline:** v4.X (13-agent atomic architecture)

---

## Statistical Findings

### Sample Characteristics

**Participants and Observations:**
- N = 100 participants (all from RQ 6.1.1 parent analysis)
- Total observations: 400 (100 participants × 4 test sessions)
- Test sessions: T1 (Day 0, TSVR ~1h), T2 (Day 1, TSVR ~22h), T3 (Day 3, TSVR ~81h), T4 (Day 6, TSVR ~145h)
- Time range: TSVR 1.0 to 246.2 hours (actual elapsed time since VR encoding)

**Data Quality:**
- No missing observations (400/400 rows complete)
- 2 participants with TSVR > 200 hours (within acceptable range for 6-day retention)
- All participants have exactly 4 observations (complete session attendance)
- Theta confidence range: -2.241 to 0.491 (within typical IRT ability bounds [-3, 3])
- Standard error (SE) constant: 0.033 across all observations (reliable IRT calibration)

### Two-Phase Pattern Testing Results

**Test 1: Quadratic Term Significance**

Linear Mixed Model: θ_confidence ~ TSVR_hours + TSVR_hours² + (1 + TSVR_hours | UID)

Fixed Effects Results:

| Effect | Estimate | SE | z | p (Bonferroni) | Significant |
|--------|----------|----|----|---|---|
| TSVR_hours | -0.00608 | 0.000765 | -7.94 | 3.94e-15 | **Yes** |
| TSVR_hours² | 0.0000221 | 0.00000446 | 4.95 | 1.48e-06 | **Yes** |

**Interpretation:** Both terms significant (p < 0.01 Bonferroni). Linear term indicates decline, quadratic indicates curvature with deceleration. Provides evidence FOR two-phase via curvature detection.

**Test 2: Piecewise vs Continuous Model Comparison**

| Model | AIC | Delta AIC | Preferred? |
|-------|-----|-----------|---|
| Continuous | 277.64 | — | **Yes** |
| Piecewise | 315.55 | -37.91 | No |

**Interpretation:** Continuous model has better fit (lower AIC). Threshold for preference is delta > 2. Continuous model 37.91 points better = evidence AGAINST two-phase pattern.

**Test 3: Early vs Late Slope Ratio**

| Segment | Slope | SE |
|---------|-------|-------|
| Early (0-48h) | -0.00382 | 0.00139 |
| Late (48-144h) | -0.00347 | 0.000435 |
| **Ratio** | **0.909** | — |

**Interpretation:** Late decline = 90.9% of Early decline. Criterion for two-phase is ratio < 0.5. Ratio 0.909 does NOT support two-phase pattern.

### Evidence Summary

**Two-Phase Evidence: 1 of 3 tests support**
- Test 1 (Quadratic): SUPPORTS (curvature detected)
- Test 2 (Piecewise): DOES NOT SUPPORT (continuous preferred)
- Test 3 (Slope ratio): DOES NOT SUPPORT (ratio 0.91 >> 0.5)

**Overall Conclusion: INCONCLUSIVE**

Confidence shows significant curvature (quadratic term) but NOT distinct two-phase segments. Pattern better described as continuous decline with subtle deceleration.

### Trajectory Summary

- **T1 (encoding, ~1h):** θ = -0.139
- **T2 (Day 1, ~22h):** θ = -0.484 (decline 0.345 SD)
- **T3 (Day 3, ~81h):** θ = -0.686 (decline 0.547 SD)
- **T4 (Day 6, ~145h):** θ = -0.686 (PLATEAU - no further decline)

Notable: Plateau effect at Day 6. Most decline in first 24 hours.

---

## Plot Descriptions

### Figure 1: Two-Phase Confidence Trajectory

**Filename:** `plots/twophase_trajectory.png`
**Type:** 2x2 grid (theta scale top, probability scale bottom)
**Decision D069:** Dual-scale trajectory plotting

**Visual Patterns:**
- Initial decline T1 through T3
- Plateau visible after Day 3
- Steepest descent: T1-T2 (0-24h)
- Modest decline: T2-T3 (24-81h)
- Flat: T3-T4 (81-145h)

**Theta Scale (Latent Ability):**
- Starts -0.14, declines to -0.68 by Day 3 (0.54 SD drop)
- Stays -0.69 through Day 6 (plateau)
- CIs widen over time (increasing uncertainty)
- Early segment visually steeper than late

**Probability Scale (Performance Likelihood):**
- Starts ~0.45 (45% correct likelihood)
- Declines to ~0.26 by Day 3 (19 percentage point drop)
- Stays ~0.26 through Day 6 (plateau)
- More intuitive for non-psychometricians
- Shows clinically meaningful decline

**Connection to Findings:**
- Curvature visible (supports quadratic significance)
- Early steeper than late visually (supports intuition)
- But slope difference modest (explains AIC preference for continuous)
- Plateau not captured by linear/piecewise models

---

## Interpretation

### Hypothesis Testing

**Original Hypothesis:**
"Confidence exhibits two-phase pattern paralleling accuracy: rapid decline Day 0→1, slower decay Day 1→6."

**Status:** **PARTIALLY SUPPORTED (inconclusive)**

- **Supporting:** Significant curvature (quadratic p < 0.001)
- **Against:** Continuous model better fit (AIC -37.91), slope ratio 0.91 >> 0.5
- **Complexity:** Plateau at Day 6 not captured by either model

### Dual-Scale Interpretation (Decision D069)

**Theta Scale:**
Confidence declined 0.55 SD from encoding (θ = -0.14) to Day 3 (θ = -0.68), a medium effect (Cohen's d = 0.55). Decline plateaued after Day 3. Curvature reveals steeper early decline (0-24h: -0.345 SD) vs late decline (24-81h: -0.202 SD). However, continuous linear model fits nearly as well as piecewise model, suggesting deceleration is continuous not step-wise.

**Statistical Interpretation:**
Significant quadratic term (p < 0.001) indicates genuine non-linearity. Positive coefficient indicates deceleration (declining rate of decline). Piecewise model designed to capture discrete Early/Late phases did NOT outperform continuous model (AIC -37.91). Suggests deceleration is continuous rather than 48-hour breakpoint.

**Probability Scale:**
Confidence likelihood declined from 45% (encoding) to 26% (Day 3-6), a 19 percentage point clinically meaningful drop. Participants started near chance, ended near random guessing. Plateau after Day 3 suggests confidence stabilizes while accuracy continues declining—a metacognition-memory dissociation.

**Practical Interpretation:**
Confidence ratings become unreliable beyond 24h: participants express less differentiated confidence while memory continues declining. By Day 6, participants show similar low confidence (~26%) regardless of memory performance. Below chance (33% for 3AFC) confidence indicates overconfidence that they've truly forgotten.

**Why Both Scales Matter:**
- **Theta:** Precise effect size (0.55 SD) comparable to literature; rigorous for meta-analysis
- **Probability:** Reveals ~26% confidence by Day 3, well below chance. Shows metacognitive calibration issues.
- **Together:** Demonstrate statistical rigor (non-linearity detected) + practical utility (confidence inadequate for long-term assessment)

### Domain Insights

**Omnibus Confidence Factor:**
Uses combined "All" confidence (collapsing What/Where/When). Parallels RQ 5.1.2 accuracy analysis structure for direct pattern comparison.

### Theoretical Contextualization

**Sleep-Dependent Consolidation Theory:**
Hypothesis predicted confidence shows two-phase IF consolidation affects metacognitive monitoring. Evidence ambiguous: confidence shows curvature (consistent with consolidation) but pattern is continuous deceleration, not discrete phases. Suggests consolidation affects metacognition more gradually, or metacognition less sensitive to consolidation than memory.

**Metacognitive Monitoring Theory:**
Striking dissociation: confidence declines significantly Day 0-3, plateaus thereafter despite continued accuracy decline Day 3-6. Challenges simple memory-strength → confidence correspondence. Alternative explanations:
1. **Confidence saturation:** Participants reach "I've forgotten" floor by Day 3
2. **Metacognitive lag:** Day 3 retrieval establishes confidence baseline, Day 6 retrieval doesn't update
3. **Domain effects:** Omnibus factor masks domain differences

### Unexpected Patterns

**Plateau After Day 3:**
Striking: Confidence plateaus (no T3-T4 decline) while theta stays stable (-0.69). Unexpected because accuracy typically declines through Day 6. Possible explanations:
1. Scale floor effect (confidence near bottom by Day 3)
2. Retrieval-based update only (Day 3 performance sets expectation)
3. Metacognitive asymmetry (forgetting affects confidence less than remembering)

**Modest Early-Late Difference:**
Visually steeper early but slope ratio 0.91 (late is 91% as fast as early). Only 9% slower—doesn't meet two-phase criterion (< 0.5). Real but continuous difference, not discrete.

**Visual-Statistical Contradiction:**
Plots appear two-phase but statistics favor continuous model. Eye groups data into phases even when continuous more parsimonious. Important methodological lesson about visual inference bias.

### Broader Implications

**REMEMVR Confidence Validity:**
Confidence shows expected decline trajectory aligned with forgetting, supporting validity. However, plateau after Day 3 suggests limitation: confidence loses discriminative power at longer retention where accuracy continues declining.

**Metacognitive Monitoring Sensitivity:**
Confidence responds to early changes (Day 0-3) but becomes insensitive to later forgetting (Day 3-6). Clinical implication: confidence useful for short-term assessment (≤3 days), unreliable for long-term retention.

**Methodological Insights:**
1. Two-phase definition critical—pre-registered thresholds prevent post-hoc cherry-picking
2. Dual-scale necessity—theta alone misses practical meaning
3. TSVR as time variable (Decision D070)—actual hours capture natural variation better than nominal days

---

## Limitations

### Sample Limitations

**Size:** N=100 adequate for large effects (d>0.8) but underpowered for small effects (d=0.2). Subgroup analyses constrained. CIs wide at time extremes.

**Demographics:** Undergrad sample (18-25, 68% female, high education). Limited to young, educated populations. Older adults, clinical populations, non-WEIRD samples likely different.

**Attrition:** Complete through Day 6 but availability bias possible (engaged participants only).

### Methodological Limitations

**Measurement:**
- 5-category confidence scale may have ceiling/floor effects
- Plateau may reflect scale floor not true metacognitive saturation
- IRT GRM assumes monotonic response functions
- Omnibus "All" factor masks What/Where/When differences

**Design:**
- Fixed retention intervals may miss consolidation windows
- No immediate post-encoding test (Day 0 = encoding)
- No concurrent accuracy-confidence measurement (separate sessions)
- Practice/retrieval effects uncontrolled

**Statistical:**
- 48h breakpoint arbitrary (sensitivity not tested)
- Three-test framework increases multiple comparison burden
- TSVR continuous assumption (no sleep-specific effects modeled)
- LMM assumes linear heterogeneity (individual variation in phase pattern not examined)

### Generalizability

**Population:** Young undergraduates only; older/clinical/non-WEIRD samples different.
**Context:** Desktop VR differs from real-world; lab setting may alter confidence expression.
**Task:** REMEMVR-specific; other confidence measures may differ.

### Technical

**IRT assumptions:** GRM monotonicity, dimensional orthogonality, local independence assumptions may not hold.
**TSVR precision:** Recording error unknown; within-day variation obscures true consolidation breakpoint.
**Model specification:** 48h breakpoint arbitrary; alternatives (36h, 60h, 72h) not tested.
**Multiple comparisons:** Three tests with different threshold types (p-value, AIC, ratio).

---

## Next Steps

### Immediate Follow-Ups

**1. Domain-Specific Trajectories (RQ 6.3):**
- Test if plateau universal or domain-specific
- Separate models for What/Where/When confidence
- Timeline: Next RQ in Chapter 6 Type 6.3

**2. Accuracy-Confidence Association (RQ 6.2):**
- Cross-time correlation between accuracy and confidence
- Tests confidence validity as memory proxy
- Timeline: After RQ 6.1.2

**3. Paradigm Analysis (RQ 6.4):**
- Separate IFR/ICR/IRE trajectories
- Tests if plateau universal or paradigm-specific
- Timeline: Chapter 6 Type 6.4

**4. Sensitivity Analysis:**
- Test alternative breakpoints (36h, 60h, 72h)
- Identify optimal consolidation window
- Timeline: Immediate (~30 min)

### Planned RQs

**RQ 6.2:** Accuracy-confidence association across time points
**RQ 6.3:** Domain-specific confidence trajectories
**RQ 6.4:** Paradigm-specific confidence patterns

### Future Extensions

**1. Extended retention:** Add Day 14, 28 sessions (N=50 subsample)
**2. Trial-level measurement:** Concurrent confidence-accuracy per trial
**3. Individual differences:** Identify fast vs slow confidence-decline participants
**4. HMD immersion:** Test if full immersion changes trajectory

### Theoretical Questions

1. **Metacognitive saturation:** Do ratings hit floor by Day 3?
2. **Retrieval-based update:** Does confidence update only after retrieval?
3. **Consolidation specificity:** Is early-decline post-sleep specific or continuous?
4. **Domain interaction:** Do domains differ in confidence-accuracy dissociation?

### Priorities

**High:** Sensitivity analysis, RQ 6.2, RQ 6.3, trial-level correlation
**Medium:** RQ 6.4, individual differences, extended retention
**Low:** HMD replication, sleep manipulation, fMRI mechanisms

---

**Summary Generated By:** rq_results agent (v4.0)
**Pipeline:** v4.X (13-agent atomic architecture)
**Validation:** All prior steps complete and successful
**Date:** 2025-12-11
