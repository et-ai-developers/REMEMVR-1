# RQ 5.2.5 When Exclusion Complete - Contamination Fix & Re-execution

This archive contains the complete history of RQ 5.2.5 re-execution after discovering When domain contamination.

---

## RQ 5.2.5 Complete Re-execution - When Domain Exclusion Fix (2025-12-03 20:45)

**Task:** RQ 5.2.5 Complete Re-execution - When Domain Exclusion Fix

**Context:** User identified that RQ 5.2.5 was contaminated with When domain data (26 items in step01_item_mapping.csv). When domain should have been excluded per RQ 5.2.1 floor effect discovery (77% item attrition, 6-9% floor). Complete re-execution required.

**Archived from:** state.md
**Original Date:** 2025-12-03 20:45
**Reason:** 3+ sessions old, complete RQ execution archived for historical record

### Major Accomplishments

**1. Updated Documentation for When Exclusion**

Modified `1_concept.md` and `2_plan.md` to document When domain exclusion:
- Exclusion rationale: Floor effect in RQ 5.2.1 (77% item attrition)
- Only What/Where domains analyzed (When items with -O- tag excluded)
- Expected item counts updated (79 What/Where items vs original 105)

**2. Fixed All 9 Code Steps (step00-step08)**

| Step | Changes | Result |
|------|---------|--------|
| step00_load_data.py | Filter purified_items to factor!='when', drop theta_when column | 69→64 items, no theta_when |
| step01_map_items.py | classify_domain returns None for -O- tags, skip those | 26 When items excluded, 79 What/Where remain |
| step02_compute_full_ctt.py | domains=['what','where'] only | No CTT_full_when column |
| step03_compute_purified_ctt.py | domains=['what','where'] only | No CTT_purified_when column |
| step04_assess_reliability.py | domains=['what','where'] only | 2 rows output (not 3) |
| step05_correlation_analysis.py | Bonferroni k=2 (not 3), domains=['what','where'] | 2 rows output |
| step06_standardize_outcomes.py | Long format 800 rows (400×2 not 400×3) | Correct reshape |
| step07_fit_parallel_lmms.py | Docstring update, 800 rows input | All 3 LMMs converged |
| step08_prepare_plot_data.py | required_domains=['what','where'] | 4 rows correlation data |

**3. Key Results After Fix**

**Reliability (Step 4):**
- What: α_full=0.712, α_purified=0.702 (slight reduction, acceptable)
- Where: α_full=0.821, α_purified=0.829 (slight improvement)

**Correlation Analysis (Step 5):**

| Domain | r(Full CTT, IRT) | r(Purified CTT, IRT) | Δr | Steiger z | p (Bonferroni k=2) |
|--------|------------------|----------------------|----|-----------|---------------------|
| What | 0.879 | 0.906 | +0.027 | 10.06 | <0.001 |
| Where | 0.940 | 0.955 | +0.015 | 14.22 | <0.001 |

**LMM Model Comparison (Step 7):**

| Measurement | AIC | delta_AIC | Interpretation |
|-------------|-----|-----------|----------------|
| IRT theta | 1655.06 | 0.00 | Best fit (reference) |
| Full CTT | 1780.06 | +125.00 | Substantial support for IRT |
| Purified CTT | 1812.26 | +157.21 | Substantial support for IRT |

**4. Validation Pipeline Completed**

Ran rq_inspect agent - all 4 validation layers PASS:
- Existence: All 17 output files present
- Structure: Correct columns, no theta_when/CTT_when
- Substance: Row counts correct (800 long format, 400 wide format)
- Logs: All steps show SUCCESS, no When domain data

**5. Updated status.yaml**

Updated context_dump fields for rq_concept, rq_inspect, rq_results to reflect When exclusion.

### Key Findings

**1. Purification Improves Correlation (Hypothesis SUPPORTED):**
Both What and Where domains show significantly higher Purified CTT-IRT correlation than Full CTT-IRT (Δr = 0.015-0.027, p < 0.001). IRT item purification removes measurement noise.

**2. IRT Superior for Trajectory Modeling (Expected):**
IRT theta shows substantially better model fit (AIC 1655) than either CTT approach (1780-1812). Delta_AIC > 100 indicates strong evidence for IRT superiority.

**3. Paradox Pattern Persists:**
Similar to RQ 5.12, Purified CTT shows WORSE model fit than Full CTT despite higher correlation with IRT. "Good" items are too homogeneous for trajectory modeling—item count matters.

### Files Modified

**Documentation (2 files):**
- `results/ch5/5.2.5/docs/1_concept.md` - When exclusion rationale
- `results/ch5/5.2.5/docs/2_plan.md` - When exclusion header

**Code (9 files):**
- `results/ch5/5.2.5/code/step00_load_data.py` - Filter When items/columns
- `results/ch5/5.2.5/code/step01_map_items.py` - Exclude When domain classification
- `results/ch5/5.2.5/code/step02_compute_full_ctt.py` - What/Where only
- `results/ch5/5.2.5/code/step03_compute_purified_ctt.py` - What/Where only
- `results/ch5/5.2.5/code/step04_assess_reliability.py` - What/Where only
- `results/ch5/5.2.5/code/step05_correlation_analysis.py` - What/Where only, Bonferroni k=2
- `results/ch5/5.2.5/code/step06_standardize_outcomes.py` - What/Where only
- `results/ch5/5.2.5/code/step07_fit_parallel_lmms.py` - Docstring update
- `results/ch5/5.2.5/code/step08_prepare_plot_data.py` - What/Where validation

**Status (1 file):**
- `results/ch5/5.2.5/status.yaml` - Updated context_dumps for 3 agents

### Session Metrics

**Tokens:**
- Session start: ~8k (after /refresh)
- Session end: ~60k (at /save)
- Delta: ~52k consumed

**Code steps fixed:** 9
**Code steps run successfully:** 9
**Bugs encountered:** 0 (clean execution after fixes)
**Validation status:** PASS (all 4 layers)

### Active Topics Referenced

- rq_5.2.5_when_exclusion_complete (Session 2025-12-03 20:45: contaminated_with_when_26_items, fixed_all_9_code_steps, 79_what_where_items_analyzed, correlation_improvement_significant what_delta_0.027_where_delta_0.015, irt_best_aic_1655_vs_ctt_1780, purified_ctt_worse_than_full_ctt_paradox_persists)

- ctt_irt_convergence_validated (Session 2025-12-03 20:45: purified_ctt_higher_r_with_irt, steiger_z_significant_both_domains, bonferroni_k_2_what_where_only, reliability_maintained_alpha_0.70_to_0.83)

### Relevant Archived Topics (from context-finder)

- rq_5_12_complete_execution_steps_0_8_paradox_discovered.md (2025-11-30: Same CTT-IRT convergence analysis, paradox pattern)
- when_domain_anomalies.md (2025-11-23: Floor effect discovery)
- phase1_critical_path_complete.md (2025-11-26: Steiger's z-test tool creation)

### End of Session (2025-12-03 20:45)

**Status:** ✅ **RQ 5.2.5 COMPLETE - WHEN DOMAIN EXCLUDED**

Fixed contaminated RQ 5.2.5 by excluding When domain from all 9 analysis steps. Both What and Where domains show significant purification improvement (Δr = 0.015-0.027, p < 0.001). IRT theta clearly superior for trajectory modeling (AIC 1655 vs CTT 1780-1812). Paradox pattern confirmed: Purified CTT has higher correlation but worse model fit than Full CTT.

**Chapter 5 Progress:** 17/31 RQs complete (55%). RQ 5.2.5 now validated and ready for thesis.

---
