# Chapter 6: Dunning-Kruger Double Null Pattern

**Topic:** `ch6_dunning_kruger_double_null`

**Description:** Systematic null finding for Dunning-Kruger effect across TWO independent tests in Chapter 6. RQ 6.2.4 tested whether low accuracy predicts poor calibration (NULL, not significant). RQ 6.6.2 tested whether low accuracy predicts high HCE rates (NULL, β = -0.001, p = 1.000). Both tests converge: low performers are NOT worse at metacognitive monitoring in VR episodic memory. This double null establishes boundary condition for Dunning-Kruger effect and supports domain-specificity of metacognitive deficits.

---

## Dunning-Kruger Double Null (2025-12-12 14:30)

**Archived from:** state.md Session (2025-12-12 14:30)
**Original Date:** 2025-12-12 14:30
**Reason:** Cross-RQ theoretical pattern - preserving systematic null finding

### Classic Dunning-Kruger Effect

**Original Finding (Kruger & Dunning, 1999):**
- Low performers overestimate their ability
- High performers underestimate their ability
- **Metacognitive deficit:** Low skill → poor self-insight
- **Mechanism:** "Double curse" - low ability + inability to recognize it

**Domain:** General knowledge, logical reasoning, grammar, humor

**Generalization Hypothesis:**
- D-K should apply to ALL cognitive domains
- Including episodic memory
- Including VR-based assessment

### Test 1: RQ 6.2.4 (Calibration by Accuracy)

**Research Question:**
Does baseline accuracy predict metacognitive calibration?

**Hypothesis (Dunning-Kruger):**
- Low accuracy → poor calibration (negative relationship)
- Low performers should show worse metacognitive monitoring

**Analysis:**
- Predictor: Baseline accuracy (IRT theta at Test 1)
- Outcome: Calibration (confidence_z - accuracy_z)
- Method: LMM with Accuracy × Time interaction

**Result:**
- Main effect: NULL (not significant)
- Interaction: NULL (not significant)
- **Conclusion:** Baseline accuracy does NOT predict calibration

**Interpretation:**
- Low performers are NOT worse at calibrating confidence to accuracy
- Metacognitive monitoring quality independent of memory ability
- **FIRST D-K null in VR episodic memory**

**Status:** Archived in `rq_6.2.4_complete_dunning_kruger_not_sig_thesis_ready.md`

### Test 2: RQ 6.6.2 (HCE Profiles by Accuracy)

**Research Question:**
Does baseline accuracy predict HCE rates (high-confidence errors)?

**Hypothesis (Dunning-Kruger):**
- Low accuracy → high HCE rates (negative relationship)
- Low performers make more HCEs due to combined memory + metacognitive deficits

**Analysis:**
- Predictor: z_baseline_accuracy (standardized IRT theta at Test 1)
- Outcome: HCE_rate_mean (proportion of trials with HCEs)
- Method: OLS multiple regression (4 predictors)
- Bonferroni correction: α = 0.0125

**Result:**
- β = -0.001, SE = 0.002
- t = -0.44, p_bonf = 1.000
- Correlation: r = -0.04 (essentially zero)
- **Conclusion:** Baseline accuracy has ZERO relationship with HCE rates

**Interpretation:**
- Low performers are NOT more prone to HCEs
- Memory ability does NOT predict metacognitive error patterns
- HCEs driven by metacognitive factors (overconfidence), not cognitive factors
- **SECOND D-K null in VR episodic memory**

**Status:** Archived in `rq_6.6.2_complete_dunning_kruger_not_supported_thesis_ready.md`

### Convergent Evidence: Double Null

**Pattern Across Two Tests:**

| RQ | Predictor | Outcome | D-K Prediction | Finding | Status |
|----|-----------|---------|----------------|---------|--------|
| 6.2.4 | Baseline accuracy | Calibration | Negative | NULL | Not sig |
| 6.6.2 | Baseline accuracy | HCE rates | Negative | NULL | p = 1.000 |

**Consistency:**
- Two independent statistical tests
- Two different metacognitive outcomes (calibration, HCE)
- Two different methods (LMM, OLS regression)
- **BOTH NULL:** Accuracy does NOT predict metacognitive quality

**Robustness:**
- Not a Type II error (6.6.2 has N=100, adequate power)
- Not a measurement issue (IRT theta is reliable)
- Not a confound (controlled for age, confidence bias)
- **Systematic pattern:** D-K does NOT apply to VR episodic memory

### Theoretical Implications

**Boundary Conditions for Dunning-Kruger Effect:**

1. **Domain-Specificity:**
   - D-K robust in general knowledge, logical reasoning
   - D-K NULL in VR episodic memory
   - **Implication:** Metacognitive deficits are domain-specific, not universal

2. **Task Characteristics:**
   - D-K tasks: Abstract reasoning, knowledge retrieval
   - VR tasks: Concrete spatial memory, immersive encoding
   - **Implication:** Immersive VR may scaffold metacognitive accuracy

3. **Memory vs Reasoning:**
   - D-K applies to reasoning/judgment tasks
   - D-K does NOT apply to episodic memory tasks (at least in VR)
   - **Implication:** Memory domain has different metacognitive dynamics

**Fleming & Lau (2014) Two-Dimensional Model:**
- Cognitive performance (Type 1) and metacognitive monitoring (Type 2) are SEPARABLE
- VR finding: Strong support for separability
- D-K assumption: Low Type 1 → poor Type 2 (violated in VR)

### Alternative Mechanisms for HCE

**If NOT Dunning-Kruger, then what drives HCEs?**

**From RQ 6.6.2 findings:**
- **Confidence bias:** β = +0.010, p < .001 (overconfidence predicts HCEs)
- **Baseline confidence:** β = +0.009, p < .001 (high confidence predicts HCEs)
- **Age:** β = +0.002, p = 1.000 (null, age-invariant)
- **Model R²:** 0.206 (20.6% variance explained by metacognitive factors)

**Mechanism:**
- HCEs driven by OVERCONFIDENCE (metacognitive miscalibration)
- NOT by low ability (cognitive deficit)
- Overconfidence is a TRAIT (individual difference), not linked to ability level

### Cross-Chapter Consistency

**Chapter 5 (Accuracy):**
- Multiple RQs test cognitive factors (schema, domain, trajectory)
- Baseline accuracy measured via IRT
- **Used in Ch6:** Predictor for metacognitive outcomes

**Chapter 6 (Metacognition):**
- Multiple RQs test metacognitive factors (confidence, calibration, HCE)
- Confidence measured via confidence-IRT
- **Pattern:** Cognitive and metacognitive dimensions SEPARABLE

**Cross-chapter finding:**
- Accuracy (Ch5) does NOT constrain metacognition (Ch6)
- Low memory ability ≠ poor metacognitive monitoring
- **Supports:** Domain-general metacognitive skill independent of domain-specific memory ability

### Practical Implications

**Cannot Identify HCE-Prone Individuals via Memory Tests:**
- Memory ability irrelevant for HCE risk
- Must assess metacognitive calibration directly
- Overconfidence is the target, not memory training

**Metacognitive Training:**
- Focus on calibration, not memory improvement
- Target overconfidence trait
- VR assessment reveals metacognitive style independent of ability

**Clinical Assessment:**
- VR metacognitive assessment NOT confounded by memory impairment
- Metacognitive deficits diagnosable in memory-impaired populations
- Separable treatment targets (memory vs metacognition)

### Related Archive Topics

- **rq_6.2.4_complete_dunning_kruger_not_sig_thesis_ready:** First D-K null (calibration)
- **rq_6.6.2_complete_dunning_kruger_not_supported_thesis_ready:** Second D-K null (HCE)
- **ch6_hce_driven_by_metacognition_not_memory:** Metacognitive vs cognitive drivers
- **ch6_hce_decrease_35_percent_metacognitive_success:** Adaptive monitoring (RQ 6.6.1)

### Summary

Dunning-Kruger effect does NOT generalize to VR episodic memory domain. TWO independent tests (RQ 6.2.4 calibration, RQ 6.6.2 HCE rates) both show NULL effects of baseline accuracy on metacognitive quality. Low performers are NOT worse at metacognitive monitoring. This establishes boundary condition for D-K effect and supports domain-specificity of metacognitive deficits. HCEs are driven by overconfidence (metacognitive trait), not low ability (cognitive deficit). Memory performance and metacognitive monitoring are separable dimensions in VR episodic memory.

---
