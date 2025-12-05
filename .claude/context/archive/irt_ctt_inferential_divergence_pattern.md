# IRT-CTT Inferential Divergence Pattern

**Topic:** Documentation of measurement convergence vs inferential divergence pattern across IRT-CTT analyses

**Archive Created:** 2025-12-05 14:45 (context-manager curation)

---

## [Inferential Divergence Pattern Discovery] (2025-12-05 14:30)

**Archived from:** state.md Session (2025-12-05 14:30)
**Original Date:** 2025-12-05 14:30
**Reason:** Pattern documented, archived for reference

### Key Finding

**Pattern:** High correlations (measurement convergence) but different significance patterns (inferential divergence)

**RQ 5.5.4 Evidence:**
- **Measurement Convergence:** r=0.944 (source), r=0.871 (destination) - EXCEPTIONAL/STRONG
- **Inferential Divergence:** Cohen's κ=0.000, significance agreement only 50%

### Mechanism

**CTT Bounded Scale [0,1] Compresses Variance:**
- IRT theta: unbounded scale (-∞ to +∞), full variance preserved
- CTT proportion-correct: bounded [0,1], variance compression near boundaries
- Result: Attenuated effect sizes in CTT, reduced statistical power

**Evidence:**
- Sign agreement: 100% (4/4 terms) - both methods detect same direction
- Significance agreement: 50% (2/4 terms) - IRT detects weaker effects
- Kappa: 0.000 - no better than chance for significance agreement

### Interpretation

**This is NOT a measurement problem:**
- High correlations (r > 0.87) validate same underlying constructs measured
- Perfect directional agreement confirms same empirical patterns detected

**This IS a sensitivity difference:**
- IRT more sensitive for detecting location-specific effects
- CTT less sensitive due to bounded scale compression
- Both methods valid, IRT superior for subtle effect detection

### Cross-RQ Pattern

**RQ 5.5.4 (Source-Destination):**
- κ=0.000, agreement=50%
- Kappa threshold (>0.60) NOT MET
- BUT high correlations support convergent validity

**Historical Context:**
- RQ 5.3.5 (Paradigms): κ=0.667, agreement=83.3% - SUBSTANTIAL
- RQ 5.4.4 (Congruence): κ=0.667, agreement=83.3% - SUBSTANTIAL
- Pattern varies by factor structure and effect magnitude

### Methodological Implications

**For Thesis:**
1. **Report both metrics:** Static convergence (correlations) + Dynamic convergence (kappa)
2. **Interpret divergence:** Bounded CTT compresses variance, attenuates effects
3. **IRT advantages:** More sensitive for location-specific effects in source-destination memory
4. **NOT artifact:** High correlations validate same constructs measured

**Threshold Interpretation:**
- κ > 0.60: Substantial agreement (RQ 5.3.5, 5.4.4)
- κ = 0.00: Divergence interpretable when r > 0.70 (RQ 5.5.4)
- Low kappa + high r = sensitivity difference, not measurement failure

### Files Referenced

**Analysis Outputs:**
- results/ch5/5.5.4/data/step02_correlations.csv (r values)
- results/ch5/5.5.4/data/step05_fixed_effects_comparison.csv (kappa)
- results/ch5/5.5.4/results/summary.md (comprehensive interpretation)

**Cross-References:**
- Archive: rq_5.3.5_complete_execution_irt_ctt_convergence.md (κ=0.667 paradigm example)
- Archive: rq_5.4.4_complete_execution_irt_ctt_convergence.md (κ=0.667 congruence example)
- Archive: ctt_irt_convergence_validated.md (2025-12-03 20:45: purification paradox)

---
