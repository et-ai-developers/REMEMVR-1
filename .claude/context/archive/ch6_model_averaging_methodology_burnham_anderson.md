# Chapter 6 Model Averaging Methodology - Burnham & Anderson (2002)

**Last Updated:** 2025-12-13 (context-manager archival)

---

## Model Averaging Methodology Background (2025-12-13 13:45)

**Archived from:** state.md Session (2025-12-13 13:45)
**Original Date:** 2025-12-13 13:45
**Reason:** Methodology implemented in Sessions 14:30 and 20:50, comprehensive documentation created in docs/lmm_methodology.md

---

### Burnham & Anderson (2002) Framework

**Core Principle:** When model uncertainty exists (no single model dominates), use model averaging to incorporate evidence from ALL competitive models rather than selecting single "best" model.

**Key Components:**

1. **Akaike Weights**
   - Normalize AIC differences into probabilities
   - Represent strength of evidence for each model
   - Sum to 1.0 across all models

2. **Model-Averaged Predictions**
   - Weighted average of predictions from competitive models
   - Each model contributes proportional to its Akaike weight
   - Provides robust predictions accounting for model uncertainty

3. **Unconditional Variance (Equation 4.9)**
   - Standard model variance + model selection variance
   - Accounts for uncertainty about which model is "correct"
   - Critical for proper confidence intervals

4. **ΔAIC < 7 Threshold**
   - Burnham & Anderson recommend including models with ΔAIC < 4-7
   - We use ΔAIC < 7 (conservative, includes more models)
   - Models with ΔAIC ≥ 7 have <3% weight (negligible contribution)

---

### Implementation in REMEMVR Project

**Implemented via:** `tools/model_averaging.py` (779 lines, Session 14:30)

**Key Functions:**

1. `identify_competitive_models()`
   - Filters models with ΔAIC < 7
   - Renormalizes Akaike weights to sum to 1.0
   - Computes Effective N (1 / Σ(weight²))

2. `compute_unconditional_variance()`
   - Implements B&A 2002 equation 4.9
   - Adds model selection uncertainty to standard errors
   - Used for confidence intervals on predictions

3. `compute_model_averaged_random_effects()`
   - Averages random intercepts across competitive models
   - Averages random slopes across competitive models
   - Essential for ICC decomposition (RQ 6.1.4)

4. `_get_primary_time_term()`
   - Maps 65+ model names to primary time predictor
   - Enables random slope extraction for each model
   - Handles all functional forms (linear, log, power law, etc.)

5. `run_model_averaging_pipeline()`
   - Complete automation from kitchen sink results to MA outputs
   - Standardized step05b_*.csv output format
   - Used across all 5 ROOT RQs

---

### Effective N Classification

**Effective N = 1 / Σ(weight²)**

| Effective N | Uncertainty Level | Interpretation |
|-------------|------------------|----------------|
| 1.0 - 2.0 | LOW | Single model dominates (>70% weight) |
| 2.1 - 5.0 | MODERATE | 2-5 models competitive |
| 5.1 - 20.0 | HIGH | Many models competitive |
| > 20.0 | EXTREME | No single model dominates |

**Chapter 6 Results:**

| RQ | Competitive Models | Effective N | Level |
|----|-------------------|-------------|-------|
| 6.8.1 | 51 | 43.4 | EXTREME |
| 6.1.1 | 48 | 31.1 | EXTREME |
| 6.3.1 | 4 | 2.4 | LOW |
| 6.4.1 | 2 | 2.0 | LOW |
| 6.5.1 | 2 | 1.8 | LOW |

**Chapter 5 Results:**

| RQ | Competitive Models | Effective N | Level |
|----|-------------------|-------------|-------|
| 5.1.1 | 51 | 40.09 | EXTREME |

---

### Application to Kitchen Sink Results

**Before Model Averaging:**
- 65-66 models tested per ROOT RQ
- Akaike weights computed
- Single "best" model selected
- 78-96% of model evidence IGNORED

**After Model Averaging:**
- ΔAIC < 7 threshold applied
- 2-51 competitive models identified
- Model-averaged predictions computed
- ALL model evidence incorporated
- Unconditional variance accounts for model uncertainty

---

### Thesis Implications

1. **Robustness:** NULL findings validated across multiple competitive models (not dependent on single model choice)

2. **Uncertainty Quantification:** Effective N reveals when model choice matters (6.8.1, 6.1.1) vs when it doesn't (6.3.1, 6.4.1, 6.5.1)

3. **ICC Decomposition:** 824× ratio (RQ 6.1.4) now has model-averaged foundation from 48 competitive models

4. **Scientific Rigor:** Follows Burnham & Anderson best practices for multimodel inference

---

**Status:** ✅ COMPLETE - Methodology implemented across all ROOT RQs, comprehensive documentation created

**Documentation:** Full methodology documented in `docs/lmm_methodology.md` (created Session 20:50)

**Related Topics:**
- ch6_kitchen_sink_audit_complete_model_averaging_gap (Session 2025-12-13 13:45)
- ch6_rq_rework_plan_created (Session 2025-12-13 13:45)
- ch6_model_averaging_implementation_complete_5_root_rqs (Session 2025-12-13 14:30)
- burnham_anderson_2002_implementation (Session 2025-12-13 14:30)
- docs_lmm_methodology_created (Session 2025-12-13 20:50)

---
