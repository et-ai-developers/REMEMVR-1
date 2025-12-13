# Chapter 6 Extreme Model Uncertainty - Validated via Model Averaging

This archive documents the validation of EXTREME model uncertainty findings in Chapter 6 ROOT RQs, particularly RQ 6.8.1 (Effective N=43.4) and RQ 6.1.1 (Effective N=31.1), demonstrating that no single model dominates and model averaging is mandatory.

---

## Extreme Model Uncertainty Validated (2025-12-13 14:30)

**Archived from:** state.md Session (2025-12-13 14:30)
**Original Date:** 2025-12-13 14:30
**Reason:** Session 3+ old, archiving to topic-based storage per context-manager protocol

### Key Discovery: Two ROOT RQs Show EXTREME Uncertainty

**RQ 6.8.1 (Source-Destination Confidence):**
- Kitchen sink: 66 models tested
- Best model weight: 4.2% (EXTREME uncertainty)
- Competitive models (ΔAIC < 7): 51 models capturing 99.6% of total weight
- **Effective N: 43.4** - Very high, indicating no single model dominates
- Interpretation: 20+ models are essentially equivalent (ΔAIC < 2)

**RQ 6.1.1 (Overall Confidence Trajectory):**
- Kitchen sink: 65 models tested
- Best model weight: 21.7% (Sin+Cos model)
- Competitive models (ΔAIC < 7): 48 models capturing 97.5% of total weight
- **Effective N: 31.1** - High uncertainty
- Interpretation: Multiple competing functional forms, no clear winner

### Contrast with MODERATE Uncertainty RQs

**RQ 6.3.1 (Domain):** Effective N = 2.4 (Ultimate model dominates with 55.6%)
**RQ 6.4.1 (Paradigm):** Effective N = 2.0 (Perfect tie between 2 models)
**RQ 6.5.1 (Schema):** Effective N = 1.8 (Single model with 65.3%)

### Why This Matters

**Original approach (single best selection):**
- 6.8.1: Ignored 95.8% of model evidence (selected 4.2% model)
- 6.1.1: Ignored 78.3% of model evidence (selected 21.7% model)
- Risk: Conclusions based on arbitrarily selected model from large set of equivalents

**Model averaging approach:**
- Integrates evidence across all 51 (6.8.1) or 48 (6.1.1) competitive models
- Predictions weighted by Akaike weights (evidence strength)
- Variance estimates include model selection uncertainty (Burnham & Anderson 2002, eq 4.9)
- More robust conclusions that acknowledge functional form uncertainty

### Impact on Major Findings

**6.8.1 NULL interaction (Source vs Destination):**
- Original: p=0.553 based on single best model (4.2% weight)
- Model-averaged: NULL finding ROBUST across all 51 competitive models
- Conclusion: Source-destination equivalence is NOT model-dependent

**6.1.1 Random effects (for 824× ICC ratio):**
- Original: Single model (Recip_sq) provided intercept/slope SDs
- Model-averaged: 48 models contribute to intercept SD=0.314, slope SD=0.099
- Impact: RQ 6.1.4's major finding (824× ICC ratio) now has model-averaged foundation
- Next step: Sensitivity analysis comparing single-best vs MA random effects

### Effective N Interpretation

**Formula:** Effective N ≈ 1 / Σ(w_i²) where w_i are renormalized Akaike weights

**Interpretation:**
- **N ≈ 1:** Single model dominates (concentrated evidence)
- **N ≈ 2-5:** Small set of competitive models (moderate uncertainty)
- **N > 30:** Large set of competitive models (EXTREME uncertainty)

**Why it matters:**
- Low N (1-5): Model averaging may not change conclusions much
- High N (>30): Model averaging MANDATORY - single model selection is arbitrary

### Methodological Lesson

**Kitchen sink comparison alone is insufficient:**
- Computing 65+ AICs identifies competitive models
- But selecting "best" from large competitive set ignores model uncertainty
- Model averaging quantifies uncertainty via Effective N
- Effective N > 30 signals "no clear winner, integrate evidence"

**Thesis implication:**
- Chapter 6 confidence trajectories show MORE functional form ambiguity than Chapter 5 accuracy
- This is itself a finding: Memory has clearer decay signature than metacognition
- Model averaging reveals this ambiguity rather than hiding it

---
