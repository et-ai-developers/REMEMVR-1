# CTT-IRT Convergence Validation - Purification Benefits & Paradox Pattern

This archive contains the history of CTT-IRT convergence validation findings across multiple RQs, documenting the purification benefit hypothesis and the paradox pattern where purified CTT shows higher correlation but worse model fit.

---

## RQ 5.2.5 CTT-IRT Convergence Validation (2025-12-03 20:45)

**Context:** RQ 5.2.5 re-executed with When domain excluded (floor effect). Validation of purification benefit hypothesis using Steiger's z-test for dependent correlations.

**Archived from:** state.md
**Original Date:** 2025-12-03 20:45
**Reason:** Complete CTT-IRT convergence analysis archived for cross-RQ pattern tracking

### Key Findings

**Purification Improves Correlation (Hypothesis SUPPORTED):**

Both What and Where domains show significantly higher Purified CTT-IRT correlation than Full CTT-IRT:

| Domain | r(Full CTT, IRT) | r(Purified CTT, IRT) | Δr | Steiger z | p (Bonferroni k=2) | Status |
|--------|------------------|----------------------|----|-----------|---------------------|--------|
| What | 0.879 | 0.906 | +0.027 | 10.06 | <0.001 | ✅ SIGNIFICANT |
| Where | 0.940 | 0.955 | +0.015 | 14.22 | <0.001 | ✅ SIGNIFICANT |

**Interpretation:** IRT item purification successfully removes measurement noise, improving convergence between CTT and IRT theta scales.

**Reliability After Purification:**
- What: α_full=0.712 → α_purified=0.702 (slight reduction, acceptable)
- Where: α_full=0.821 → α_purified=0.829 (slight improvement)

Both domains maintain adequate reliability (α > 0.70) after purification.

**Bonferroni Correction:**
- k=2 domains (What/Where only, When excluded)
- Critical p-value: 0.05/2 = 0.025
- Both domains: p < 0.001 (far below threshold)

### IRT Superior for Trajectory Modeling

**LMM Model Comparison (Step 7):**

| Measurement | AIC | delta_AIC | Burnham-Anderson Interpretation |
|-------------|-----|-----------|--------------------------------|
| IRT theta | 1655.06 | 0.00 (reference) | Best fit |
| Full CTT | 1780.06 | +125.00 | **Substantial support for IRT** |
| Purified CTT | 1812.26 | +157.21 | **Substantial support for IRT** |

Delta_AIC > 100 indicates extremely strong evidence for IRT superiority in trajectory modeling.

### Paradox Pattern Confirmed

**Paradox:** Purified CTT shows HIGHER correlation with IRT theta (better convergence) but WORSE model fit for trajectories than Full CTT.

**Evidence:**
- Purified CTT vs Full CTT correlation: +0.015 to +0.027 improvement (p<0.001)
- Purified CTT vs Full CTT model fit: AIC 1812 vs 1780 (Purified WORSE by 32 AIC points)

**Explanation (from RQ 5.12 investigation):**
1. **Purification removes "bad" items** → Remaining items more homogeneous
2. **More homogeneous items** → Less variance in CTT scores
3. **Less variance** → Poorer discrimination of individual trajectories
4. **Item count matters** → Full CTT has more items, more information for trajectories
5. **BUT purified items better reflect theta** → Higher correlation

**Implication:**
- For **cross-sectional** convergence: Purified CTT preferred (higher r with theta)
- For **longitudinal** trajectories: Full CTT or IRT theta preferred (more variance/information)

### Cross-Reference to Related Findings

**Similar Pattern in RQ 5.12:**
- Archive: `rq_5_12_complete_execution_steps_0_8_paradox_discovered.md` (2025-11-30)
- Same paradox observed: Purification improves r but worsens AIC
- Decision: Report both Full and Purified CTT, explain trade-off transparently

**When Domain Floor Effect:**
- Archive: `when_domain_anomalies.md` (2025-11-23)
- 77% item attrition, 6-9% floor performance
- Excluded from all domain-based RQs (5.2.2, 5.2.3, 5.2.5, 5.2.6, 5.2.7)

**Steiger's Z-Test Tool:**
- Archive: `phase1_critical_path_complete.md` (2025-11-26)
- Tool created for dependent correlation comparison
- Used in RQ 5.12 and 5.2.5 for purification benefit validation

### Methodological Notes

**Decision D068:** Dual p-values reported
- Both raw p-value and Bonferroni-corrected p-value reported
- Conservative threshold: Bonferroni
- Transparency: Raw p-value for reader judgment

**Statistical Power:**
- N=400 participants × timepoints provides excellent power
- Steiger z > 10 indicates very strong effect
- Effect size (Δr = 0.015-0.027) small but meaningful at scale

**Generalizability:**
- Pattern consistent across What and Where domains
- Pattern consistent across RQ 5.12 (schema) and 5.2.5 (domain)
- Suggests systematic purification benefit across all IRT-based analyses

### Files Referenced

**RQ 5.2.5 Outputs:**
- `results/ch5/5.2.5/data/step05_correlation_comparison.csv` - Steiger z-test results
- `results/ch5/5.2.5/data/step04_reliability_estimates.csv` - Alpha values
- `results/ch5/5.2.5/data/step07_model_comparison.csv` - AIC comparison

**Related RQs:**
- RQ 5.12: First discovery of paradox pattern
- RQ 5.2.2: When excluded, consolidation analysis
- RQ 5.2.3: When excluded, Age×Domain interaction

### Status

**RQ 5.2.5:** ✅ COMPLETE - WHEN DOMAIN EXCLUDED

**Findings:** Purification improves CTT-IRT convergence significantly (Δr = 0.015-0.027, p < 0.001). IRT theta superior for trajectory modeling (AIC 1655 vs CTT 1780-1812). Paradox pattern confirmed: good items trade correlation for variance.

**Thesis Impact:** Methodological contribution - demonstrates purification benefit but warns against over-purification for longitudinal studies. Supports dual-reporting strategy (Full CTT for trajectories, Purified CTT for convergence validation).

---
