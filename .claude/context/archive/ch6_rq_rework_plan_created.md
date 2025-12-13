# Chapter 6 RQ Rework Plan Creation

**Last Updated:** 2025-12-13 (context-manager archival)

---

## rq_rework.md Creation (2025-12-13 13:45)

**Created:** `results/ch6/rq_rework.md` (~350 lines)

**Archived from:** state.md Session (2025-12-13 13:45)
**Original Date:** 2025-12-13 13:45
**Reason:** Plan fully implemented in Sessions 14:30 and 20:50, rework complete

---

### Rework Plan Structure

**Part 1:** Model Averaging Methodology (Burnham & Anderson 2002)
- Akaike weights renormalization
- Model-averaged predictions
- Unconditional variance (equation 4.9)
- ΔAIC < 7 threshold

**Part 2:** P1-CRITICAL - RQ 6.8.1 (4.2% weight) + cascade (6.8.2-6.8.4)
- Best model weight = 4.2% (EXTREME uncertainty)
- 20 models with ΔAIC < 2
- Source/Destination confidence interaction

**Part 3:** P2-HIGH - RQ 6.1.1 (21.7% weight) + cascade (6.1.2-6.1.5)
- Best model weight = 21.7% (high uncertainty)
- Overall confidence trajectory
- Critical for 824× ICC ratio (RQ 6.1.4)

**Part 4:** P3-P5 MODERATE - RQs 6.3.1, 6.4.1, 6.5.1 + cascades
- 6.3.1: Domain (What/Where/When) - 55.6% best weight
- 6.4.1: Paradigm (IFR/ICR/IRE) - 50% best weight (tied)
- 6.5.1: Schema (Common/Unique) - 65.3% best weight

**Part 5:** P6-FIX - RQ 6.7.3 (use Ch5 MA residuals)
- Requires Ch5 5.1.1 model averaging first
- NULL finding (r=0.02) almost certainly robust

**Part 6:** Implementation Order (Phase 1-4)
1. Phase 1: Create tools/model_averaging.py
2. Phase 2: 6.8.1, 6.1.1 (CRITICAL + HIGH)
3. Phase 3: 6.3.1, 6.4.1, 6.5.1 (MODERATE)
4. Phase 4: 6.7.3 fix + validation + docs

**Part 7:** Validation Checklist
- ROOT RQ model averaging
- RQ 6.7.3 fix
- Derivative RQs (decision to NOT re-run)
- Documentation updates

**Part 8:** Risk Assessment
- 824× ICC ratio finding validation
- NULL interaction findings robustness
- Timeline estimate (2-3 days)

**Part 9:** Documentation Updates
- summary.md files for ROOT RQs
- docs/lmm_methodology.md enhancement
- rq_status.tsv updates

---

### Implementation Phases Detail

**Phase 1 (Day 1):** Infrastructure
- Create `tools/model_averaging.py` with reusable functions
- `identify_competitive_models()` - ΔAIC < 7 filtering
- `compute_unconditional_variance()` - B&A 2002 eq 4.9
- `compute_model_averaged_random_effects()` - ICC support
- `_get_primary_time_term()` - Random slope mapping
- `run_model_averaging_pipeline()` - Automation

**Phase 2 (Day 1-2):** CRITICAL + HIGH Priority
- 6.8.1: 66 models, 4.2% best weight (EXTREME)
- 6.1.1: 65 models, 21.7% best weight (HIGH)
- Update cascades (6.8.2-6.8.4, 6.1.2-6.1.5) if needed

**Phase 3 (Day 2-3):** MODERATE Priority
- 6.3.1: 65 models, 55.6% best weight
- 6.4.1: 66 models, 50% best weight (tied)
- 6.5.1: 66 models, 65.3% best weight
- Update cascades if needed

**Phase 4 (Day 3):** Fixes + Validation
- Ch5 5.1.1 model-averaged residuals
- 6.7.3 correlation using MA residuals
- Documentation updates
- Validation checklist completion

---

### Total Impact

**RQs Affected:** 22 (71% of Chapter 6)
- 5 ROOT RQs (kitchen sink)
- 1 ROOT RQ fix (6.7.3)
- 16 derivative RQs (cascade potential)

**Estimated Timeline:** 2-3 days
**Priority:** HIGH (thesis-level impact)

---

### Implementation Results (Sessions 14:30 and 20:50)

**Phase 1: Infrastructure** ✅ COMPLETE
- tools/model_averaging.py enhanced (779 lines)
- All 5 functions implemented and tested

**Phase 2: CRITICAL + HIGH** ✅ COMPLETE (Session 14:30)
- 6.8.1: 51 competitive models, Eff_N=43.4 (EXTREME)
- 6.1.1: 48 competitive models, Eff_N=31.1 (EXTREME)
- Cascades: NOT re-run (MA outputs available for sensitivity)

**Phase 3: MODERATE** ✅ COMPLETE (Session 14:30)
- 6.3.1: 4 competitive models, Eff_N=2.4 (LOW)
- 6.4.1: 2 competitive models, Eff_N=2.0 (LOW)
- 6.5.1: 2 competitive models, Eff_N=1.8 (LOW)

**Phase 4: Fixes + Validation** ✅ COMPLETE (Session 20:50)
- Ch5 5.1.1 MA residuals: 51 models, Eff_N=40.09
- 6.7.3 fix: NULL finding ROBUST (r=-0.05 vs r=0.02)
- Documentation: 5 summary.md files + lmm_methodology.md created
- Validation checklist: ALL items complete

**Actual Timeline:** 2 sessions (~70 minutes total)

---

**Status:** ✅ COMPLETE - All phases implemented, validation complete, Chapter 6 model averaging rework 100% complete

**Related Topics:**
- ch6_kitchen_sink_audit_complete_model_averaging_gap (Session 2025-12-13 13:45)
- ch6_model_averaging_methodology_burnham_anderson (Session 2025-12-13 13:45)
- ch6_critical_rework_priorities (Session 2025-12-13 13:45)
- ch6_model_averaging_implementation_complete_5_root_rqs (Session 2025-12-13 14:30)
- ch6_rework_all_items_complete (Session 2025-12-13 20:50)

---
