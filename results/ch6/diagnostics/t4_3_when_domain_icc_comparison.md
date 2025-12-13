# T4.3: Ch5 When Domain ICC Comparison for RQ 6.3.4

**Date:** 2025-12-14
**Task:** Verify When domain ICC available from Ch5 5.2.6; if missing, document why

---

## Summary

**Finding:** Ch5 5.2.6 does NOT include "When" domain analysis. Only "What" and "Where" domains are present.

**Reason:** The REMEMVR paradigm measures three domains:
- **What** (Object identity): Measured via recognition/identification questions
- **Where** (Spatial location): Measured via location/placement questions
- **When** (Temporal order): Measured via sequence/order questions

Ch5 5.2.6 focuses on accuracy ICC for What/Where domains only. The "When" domain accuracy analysis may not have been included because:
1. Temporal order judgments have different psychometric properties
2. "When" accuracy has floor effects (harder to remember sequence than items/locations)
3. Ch5 scope focused on the primary What/Where comparison

---

## Data Comparison

### Ch5 5.2.6 (Accuracy ICC - What/Where Only)

| Domain | ICC_slope | Interpretation |
|--------|-----------|----------------|
| What   | 0.52      | Substantial    |
| Where  | 0.53      | Substantial    |
| When   | N/A       | Not analyzed   |

### Ch6 6.3.4 (Confidence ICC - All Three Domains)

| Domain | ICC_slope (converged) | Stability |
|--------|----------------------|-----------|
| What   | ~0.00                | UNSTABLE  |
| Where  | ~0.00                | UNSTABLE  |
| When   | ~0.00                | STABLE    |

---

## Implications

1. **Cannot make direct When comparison:** Ch5 has no When domain ICC to compare with Ch6 6.3.4
2. **What/Where comparison possible:**
   - Ch5 (Accuracy): ICC ~0.52 (substantial individual differences in forgetting rate)
   - Ch6 (Confidence): ICC ~0.00 (when properly converged) - no individual differences in confidence decline rate
3. **Accuracy-Confidence dissociation for What/Where:**
   - Accuracy: Substantial ICC (people differ in how fast they forget)
   - Confidence: Near-zero ICC (people decline in confidence similarly)
   - This supports the "metacognitive artifact" hypothesis from Ch6

---

## Recommendation

**For Thesis:**
- Report Ch6 6.3.4 When domain ICC as exploratory finding
- Acknowledge Ch5 When domain ICC unavailable for comparison
- Focus accuracy-confidence comparison on What/Where domains where both Ch5 and Ch6 data exist
- Note that converged Ch6 What/Where ICC estimates (~0.00) contrast with Ch5's substantial ICC (~0.52)

---

## Files Referenced

- `results/ch5/5.2.6/data/step06_domain_icc_comparison.csv` (Ch5 accuracy ICC)
- `results/ch6/diagnostics/lmm_convergence_sensitivity.csv` (Ch6 confidence ICC + convergence status)
