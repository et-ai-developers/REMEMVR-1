# Random Slopes Testing Taxonomy 4.4 Validation

**Topic:** Validation of improvement_taxonomy.md Section 4.4 MANDATORY requirement for random slopes testing
**Created:** 2025-12-31
**Status:** Active - Core methodological contribution

---

## Random Slopes Testing - Taxonomy Section 4.4 (2025-12-31 Afternoon)

**Context:** Multiple RQs in Tier 1 batch required random slopes testing per improvement_taxonomy.md Section 4.4

**Requirement:** "Cannot claim homogeneous effects without testing for heterogeneity"

**Archived from:** state.md (Session 2025-12-31 Afternoon)
**Original Date:** 2025-12-31
**Reason:** Session now 3+ sessions old, methodology validation archived

---

### Taxonomy Section 4.4 Summary

**Core Principle:**
- Before claiming "age effects are uniform" or "trajectories are homogeneous"
- MUST test intercepts-only vs intercepts+slopes models
- Compare via AIC (ΔAIC > 2.0 favors slopes)
- Document result regardless of outcome

**Three Possible Outcomes:**

**Option A: Random slopes improve fit (ΔAIC > 2)**
- Use slopes model
- Report individual differences exist
- Interpret variance components

**Option B: Convergence failure**
- Document failure systematically
- Use intercepts-only by necessity
- Explain data limitation (not assumption)

**Option C: Random slopes worsen fit (ΔAIC < -2)**
- Use intercepts-only model
- Justified by parsimony (simpler is better)
- Report homogeneity as empirical finding

---

### Validation Across Tier 1 Batch

**RQ 5.3.3 (Consolidation):**
- **Outcome:** Option A (ΔAIC = +143.55)
- Slopes MASSIVELY improve fit
- Individual differences in consolidation rate are REAL
- Created step02b_random_slopes_comparison.py

**RQ 5.1.4 (ICC):**
- **Outcome:** Option C (ΔAIC = -4.69)
- Slopes WORSEN fit across all 10 models
- Forgetting variance is overfitting noise
- Created step07_random_slopes_comparison.py
- Validates 2025-12-03 LR test (p=0.69)

**RQ 5.1.2 (Two-phase forgetting):**
- **Outcome:** Option B (convergence failure)
- N=100 insufficient for slopes
- Documented limitation
- Fallback to intercepts-only justified

---

### Methodological Contributions

**1. Demonstrates CRITICAL importance of testing:**
- SAME methodology applied to RQ 5.3.3 and 5.1.4
- OPPOSITE conclusions (148 AIC point difference)
- Cannot assume slopes are/aren't needed - MUST test

**2. Validates three-option framework:**
- All three outcomes occurred in Tier 1 batch
- Framework handles all cases systematically
- No ad-hoc decisions needed

**3. Thesis-level rigor:**
- Transparent documentation of all outcomes
- No hidden assumptions about homogeneity
- Empirical evidence for parsimony choices

---

### Code Standardization

**File Naming Convention:**
- `stepXX_random_slopes_comparison.py` (where XX is step number)

**Standard Method:**
- Use compare_lmm_models_kitchen_sink
- Set re_formula='~1' for intercepts-only
- Compare AIC vs existing with-slopes model
- Decision rule: ΔAIC > 2.0 favors slopes

**Standard Output:**
- CSV with AIC comparison
- validation.md section documenting result
- Log file with convergence diagnostics

---

### Cross-RQ Patterns

**When slopes improve fit:**
- Consolidation hypotheses (RQ 5.3.3)
- Paradigm effects (multiple RQs)
- Individual differences research questions

**When slopes fail/worsen:**
- ICC estimation with binary data (RQ 5.1.4)
- Small sample trajectory studies (RQ 5.1.2)
- Uniform age effects (multiple RQs)

**Design factors predicting outcome:**
- Data type: Ordinal > Binary (824× difference Ch6 vs Ch5)
- Sample size: N=100 marginal for slopes
- Timepoints: 4 timepoints minimal for slope estimation
- Effect size: Weak effects → slopes don't help

---

### Integration with GLMM Validation

**Separate but complementary:**
- Random slopes testing: Tests TRAJECTORY heterogeneity
- GLMM validation: Tests BASELINE hypotheses at item level
- Both MANDATORY for complete rigor
- Different research questions, different methods

**Example (RQ 5.2.3, from late evening session):**
- Random slopes testing: Convergence failure (ΔAIC=-792.49)
- GLMM validation: Age × Domain interaction NULL→NULL (robust)
- Both contribute to complete picture

---

**Related Topics:**
- `ch5_tier1_batch_certification_complete` - Application context
- `rq_5_1_4_critical_random_slopes_finding` - Option C example
- `consolidation_piecewise_random_slopes_massive_improvement` - Option A example
- improvement_taxonomy.md Section 4.4 (primary documentation)

---
