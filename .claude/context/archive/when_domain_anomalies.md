# When Domain Anomalies

**Topic:** Floor effects and item attrition in When (temporal) domain across RQ analyses
**Created:** 2025-11-24 12:30 (context-manager curation)

---

## When Domain Floor Effects in RQ 5.1 (2025-11-23 04:00)

**Context:** During rq_results agent testing on RQ 5.1, two anomalies were flagged related to When domain

**Anomalies Flagged:**

1. **When Domain Floor Effect**
   - Probability 6-9% throughout (near 0% floor)
   - Cannot interpret When domain forgetting trajectory meaningfully
   - Requires investigation before acceptance

2. **When Domain Item Attrition**
   - 20/26 items (77%) excluded for low discrimination
   - Only 6 items retained, limiting reliability
   - Item content review recommended

**Scientific Plausibility Assessment:**
- What domain: PLAUSIBLE (88%->72%, valid forgetting trajectory)
- Where domain: PLAUSIBLE (61%->38%, valid forgetting trajectory)
- When domain: IMPLAUSIBLE (floor effects invalidate interpretation)

**Key Findings from summary.md:**

**IRT Results:**
- Pass 1: 105 items analyzed
- Purification: 70/105 retained (66.7%)
- Domain coverage: What=19, Where=45, When=6 items

**LMM Results:**
- When vs What: beta=-0.415, p<.001 (significant)
- But this is confounded by floor effect

**Interpretation Note:**
Dual-scale reporting (theta + probability) revealed floor effect that would have been invisible on theta scale alone. This validates the dual-scale trajectory plot approach.

**Archived from:** state.md
**Original Date:** 2025-11-23 04:00
**Reason:** Anomaly documentation relevant to When domain investigation

---

## When Domain in RQ 5.2 Consolidation Analysis (2025-11-24 10:00)

**Context:** Piecewise LMM analysis (Days 0-1 vs Days 1-6) showed unexpected When domain behavior

**Early Segment Slopes (consolidation window Day 0-1):**
- What: -0.507/day (steepest decline)
- Where: -0.456/day
- When: -0.208/day (flattest - least forgetting)

**Late Segment Slopes (decay phase Day 1-6):**
- What: -0.031/day (nearly flat)
- Where: -0.107/day (continued decline)
- When: -0.013/day (nearly flat)

**Consolidation Benefit Ranking (unexpected):**
1. When (best) - least early forgetting
2. Where
3. What (worst) - most early forgetting

**Interpretation Challenge:**
When domain appears to show "least forgetting" but this may be artifact of floor effect - cannot decline further when already near floor.

**Archived from:** state.md
**Original Date:** 2025-11-24 10:00
**Reason:** Anomaly documentation relevant to When domain investigation

---

## When Domain NOT Anomalous in RQ 5.3 Paradigm Analysis (2025-11-24 12:30)

**Context:** RQ 5.3 analyzed by paradigm (IFR/ICR/IRE) rather than by domain (What/Where/When)

**Observation:** No floor effects or anomalies flagged in RQ 5.3

**Implication:** Floor effects appear to be domain-specific (When domain) rather than paradigm-specific. The paradigm analysis (Free Recall / Cued Recall / Recognition) does not suffer from the same floor effects.

**This suggests:** The When domain items themselves may have poor psychometric properties, rather than there being a systematic issue with the analytical approach.

**Archived from:** state.md
**Original Date:** 2025-11-24 12:30
**Reason:** Documentation of When anomaly scope (domain-specific, not paradigm-specific)

---
