# Schema Baseline-Trajectory Framework Finalized

**Purpose:** Complete documentation of "Baseline Effects, Trajectory Nulls" framework, cross-chapter validation (Ch5 + Ch6), and theoretical interpretation of schema congruence effects in immersive VR.

**Related Topics:**
- ch6_100_pct_certification_complete.md
- gee_validation_protocol_binary_outcomes.md
- rq_5_4_1_glmm_narrative_integration_complete.md (2025-12-31 morning)

---

## RQ 6.5.1 CONDITIONAL → FULL PLATINUM Upgrade (2025-12-30)

**Blocker Status:** CONDITIONAL PLATINUM (2025-12-27)
- GLMM NULL→SIGNIFICANT finding (p=.660→.003)
- Required narrative decision: Accept GLMM findings or flag as artifact

**User Decision:** Option A - Accept GLMM findings, adopt "Baseline Effects, Trajectory Nulls" framework

**Archived from:** state.md Session (2025-12-30 Continuation)
**Original Date:** 2025-12-30
**Reason:** Framework finalized, cross-chapter validation complete, RQ 6.5.1 upgraded to FULL PLATINUM

---

### Complete Schema Pattern (All 4 RQs Validated)

| RQ | Measure | IRT→LMM | GLMM/GEE | Interpretation |
|----|---------|---------|----------|----------------|
| **5.4.1** (Ch5) | Accuracy baseline | p=.548 (null) | **p=.011** (sig) | Baseline effect |
| **6.5.1** (Ch6) | Confidence baseline | p=.660 (null) | **p=.003** (sig) | Baseline effect |
| **6.5.2** (Ch6) | Calibration baseline | p=.487 (null) | Pending | - |
| **6.5.3** (Ch6) | HCE rate | p=.130 (null) | **p=.169** (null) ✅ | TRUE NULL |

---

### Framework Definition: "Baseline Effects, Trajectory Nulls"

**Pattern Summary:**
1. ✅ Schema affects BASELINE (Congruent > Common > Incongruent) for accuracy + confidence
2. ✅ Schema does NOT affect TRAJECTORY (Schema × Time interactions NULL)
3. ✅ Schema does NOT affect METACOGNITIVE DISSOCIATION (HCE rates equivalent)

**Theoretical Interpretation:**
> "Schema congruence affects **encoding strength** (baseline performance and confidence) but NOT **forgetting dynamics** (decline rates) or **metacognitive dissociation** (high-confidence errors). Immersive VR encoding creates schema effects at ACQUISITION, not RETENTION."

**Key Insight:**
- IRT→LMM aggregation LOSES item-level signal (24× compression: 24 items → 1 ability score)
- GLMM preserves item-level variance → detects baseline differences
- IRT→LMM and GLMM are COMPLEMENTARY, not contradictory

---

### Cross-Chapter Convergence

**Ch5 (Accuracy):**
- IRT→LMM: p=.548 (NULL)
- GLMM: p=.011 (SIGNIFICANT)
- Effect size: Congruent items +4.6% higher accuracy at T1

**Ch6 (Confidence):**
- IRT→LMM: p=.660 (NULL)
- GLMM: p=.003 (SIGNIFICANT)
- Effect size: Congruent items +2.5% higher confidence at T1

**Convergent Pattern:**
- Both accuracy AND confidence show baseline schema effects
- Both show NULL trajectory effects (Schema × Time)
- Effect sizes modest but consistent (2.5-4.6 percentage points)

**Why This Matters:**
- Multi-method convergence (IRT, LMM, GLMM across Ch5 + Ch6)
- Schema effects on ENCODING not RETENTION
- Validates immersive VR as encoding-focused paradigm (6-day window)

---

### RQ 6.5.1 Upgrade Details

**Files Created:**
1. PLATINUM_UPGRADE_2025-12-30.md (comprehensive upgrade document)
2. status.yaml updated (CERTIFIED_FULL, upgrade decision documented)
3. validation.md updated (PLATINUM upgrade addendum)

**Time:** ~20 min

**Upgrade Criteria Met:**
1. ✅ All PLATINUM criteria satisfied (6/6)
2. ✅ GLMM findings integrated (not artifact)
3. ✅ Cross-chapter convergence documented (Ch5 + Ch6)
4. ✅ Framework finalized ("Baseline Effects, Trajectory Nulls")
5. ✅ Theoretical interpretation revised (acquisition not retention)
6. ✅ Publication-ready documentation (upgrade document + validation addendum)

---

### Methodological Lessons

**1. IRT Aggregation vs GLMM:**
- IRT ability scores: Average across 24 items → loses item-level variance
- GLMM: Analyzes 24 items × 4 tests × 100 participants = 9,600 observations
- Information preservation: GLMM > IRT→LMM (no aggregation loss)

**2. When IRT→LMM NULL but GLMM SIGNIFICANT:**
- Check if effect is BASELINE (T1 differences) not TRAJECTORY (Time × Group)
- If baseline: GLMM may detect signal lost in IRT aggregation
- If trajectory: Re-examine LMM specification (interaction terms, random slopes)

**3. Framework Evolution:**
- **Original hypothesis:** "Quadruple NULL" (no schema effects anywhere)
- **Revised framework:** "Baseline Effects, Trajectory Nulls" (schema affects encoding not retention)
- Evolution driven by GLMM validation revealing hidden baseline patterns

---

### Implications for Ch7

**Expected Pattern:**
- Ch7 RQs with schema predictors should test:
  1. Baseline effects (GLMM, expect SIGNIFICANT if Ch5/Ch6 pattern holds)
  2. Trajectory effects (IRT→LMM, expect NULL based on Ch5/Ch6)
  3. Metacognitive dissociation (GLMM on HCE, expect NULL based on RQ 6.5.3)

**Hypothesis:**
- Schema congruence is ENCODING manipulation (affects T1 baseline)
- NOT retention manipulation (does not affect forgetting rate)
- Immersive VR encoding is STRONG enough to create lasting baseline effects
- But NOT strong enough to alter forgetting/consolidation dynamics

---

### Files Referenced

**Ch6:**
- results/ch6/6.5.1/PLATINUM_UPGRADE_2025-12-30.md
- results/ch6/6.5.1/status.yaml
- results/ch6/6.5.1/validation.md
- results/ch6/6.5.3/PLATINUM_FINALIZATION_REPORT.md (GEE validation)

**Ch5:**
- results/ch5/5.4.1/summary.md (GLMM narrative integration, 2025-12-31)
- results/ch5/5.4.1/validation.md (GLMM validation section added)

**Documentation:**
- docs/glmm_candidates.md (framework documented, RQ 6.5.1 + 6.5.3 entries updated)

---

**End of Entry**
