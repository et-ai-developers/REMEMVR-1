# RQ 6.3.4 Measurement Artifact at Domain Level

## Measurement Artifact Confirmation (2025-12-11 22:45)

**Context:** RQ 6.3.4 extends RQ 6.1.4's measurement artifact finding (824× ratio for general confidence) to domain-stratified analysis, revealing 54-73× more trait variance with 5-level ordinal confidence vs binary accuracy.

**Archived from:** state.md Session (2025-12-11 22:45)
**Original Date:** 2025-12-11 22:45
**Reason:** Session 22:45 archived (now 3+ sessions old from Session 23:15)

---

### Confidence (5-level) vs Accuracy (binary) ICC_slope by Domain

**Primary Finding:** 5-level ordinal confidence reveals **~60× more trait variance** than binary accuracy across domains.

| Domain | Confidence ICC | Accuracy ICC | Fold-Change |
|--------|---------------|--------------|-------------|
| What | 0.590 | 0.008 | **73×** |
| Where | 0.590 | 0.011 | **54×** |
| When | 0.00001 | N/A | - |

**Key Insights:**

1. **Extends RQ 6.1.4 Finding:**
   - RQ 6.1.4 (general confidence): 824× ratio
   - RQ 6.3.4 (domain-specific): 54-73× ratio per domain
   - Both analyses confirm ordinal measurement reveals hidden trait variance

2. **When Domain Universality:**
   - When domain shows near-zero ICC_slope for BOTH measures
   - Universal decline regardless of measurement precision
   - Not a measurement artifact - genuinely no individual differences

3. **What/Where Consistency:**
   - Both show ~60× improvement with ordinal measurement
   - Confirms individual differences exist but require fine-grained measurement
   - Binary accuracy too coarse to detect trait variance

**Theoretical Implications:**

- **Measurement Resolution Matters:** Ordinal scales (5-level confidence) capture individual differences invisible to binary scales (correct/incorrect)
- **Domain-Specific Measurement Precision:** What/Where domains benefit from ordinal measurement, When domain does not
- **Clinical Assessment Design:** REMEMVR should prioritize ordinal confidence scales over binary accuracy for individual difference assessment

**Statistical Evidence:**
- Comparison data: `results/ch6/6.3.4/data/step06_ch5_comparison.csv`
- Visualization: `results/ch6/6.3.4/plots/confidence_vs_accuracy_icc.png`

**Related Findings:**
- RQ 6.1.4: General confidence shows 824× ratio (archived in `rq_6.1.4_icc_decomposition_major_finding_824x_ratio.md`)
- RQ 6.3.4: Domain-specific analysis shows 54-73× ratios (this finding)
- Ch5 5.2.6: Domain-specific accuracy ICC baseline for comparison

---

**Status:** ✅ **MEASUREMENT ARTIFACT CONFIRMED AT DOMAIN LEVEL**

5-level ordinal confidence reveals 54-73× more trait variance than binary accuracy for What/Where domains. Extends RQ 6.1.4 general finding to domain-stratified analysis. When domain shows universal decline (ICC≈0) for both measures, confirming genuine lack of individual differences rather than measurement limitation.
