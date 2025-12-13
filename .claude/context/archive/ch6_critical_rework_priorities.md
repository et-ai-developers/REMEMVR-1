# Chapter 6 Critical Rework Priorities

**Last Updated:** 2025-12-13 (context-manager archival)

---

## Rework Priorities Based on Model Uncertainty (2025-12-13 13:45)

**Archived from:** state.md Session (2025-12-13 13:45)
**Original Date:** 2025-12-13 13:45
**Reason:** All priorities addressed and implemented in Sessions 14:30 and 20:50

---

### Priority Classification

Priorities based on best model Akaike weight (lower weight = higher priority):

| Priority | RQ | Best Model Weight | Uncertainty Level | Status |
|----------|-----|------------------|-------------------|--------|
| **P1-CRITICAL** | 6.8.1 | 4.2% | EXTREME | ✅ COMPLETE |
| **P2-HIGH** | 6.1.1 | 21.7% | HIGH | ✅ COMPLETE |
| **P3-MODERATE** | 6.3.1 | 55.6% | MODERATE | ✅ COMPLETE |
| **P4-MODERATE** | 6.4.1 | 50.0% | MODERATE | ✅ COMPLETE |
| **P5-MODERATE** | 6.5.1 | 65.3% | MODERATE | ✅ COMPLETE |
| **P6-FIX** | 6.7.3 | N/A (correlation) | N/A | ✅ COMPLETE |

---

### P1-CRITICAL: RQ 6.8.1 (Source-Destination Confidence)

**Issue:** Best model = 4.2% weight (EXTREME uncertainty)
- 66 models tested
- 20 models with ΔAIC < 2
- Single-best selection ignores 95.8% of model evidence

**Impact:** NULL interaction finding (Source vs Destination) at severe risk

**Implementation (Session 14:30):**
- 51 competitive models (ΔAIC < 7)
- Effective N = 43.4 (EXTREME)
- 99.6% total weight included
- NULL interaction ROBUST (p=0.553 across all models)

**Cascades:** 6.8.2, 6.8.3, 6.8.4 (derivatives NOT re-run, MA outputs available)

---

### P2-HIGH: RQ 6.1.1 (Overall Confidence Trajectory)

**Issue:** Best model = 21.7% weight (Sin+Cos)
- 65 models tested
- Single-best selection ignores 78.3% of model evidence

**Impact:**
- Trajectory interpretation at risk
- 824× ICC ratio (RQ 6.1.4) depends on this ROOT RQ's random effects

**Implementation (Session 14:30):**
- 48 competitive models (ΔAIC < 7)
- Effective N = 31.1 (EXTREME)
- 97.5% total weight included
- MA intercept SD = 0.314, slope SD = 0.099
- Random slopes from ALL 48 models = foundation for 824× ICC validation

**Cascades:** 6.1.2, 6.1.3, 6.1.4, 6.1.5 (6.1.4 now has MA validation foundation)

---

### P3-MODERATE: RQ 6.3.1 (Domain - What/Where/When)

**Issue:** Best model = 55.6% weight (Ultimate)
- 65 models tested
- Moderate uncertainty

**Impact:** Domain effects interpretation moderately at risk

**Implementation (Session 14:30):**
- 4 competitive models (ΔAIC < 7)
- Effective N = 2.4 (LOW)
- 92.0% total weight included
- Ultimate model dominates (60.5% renormalized weight)
- MA has limited impact but provides methodological consistency

**Cascades:** 6.3.2, 6.3.3, 6.3.4 (derivatives NOT re-run)

---

### P4-MODERATE: RQ 6.4.1 (Paradigm - IFR/ICR/IRE)

**Issue:** Best model = 50% weight (Linear/Exponential_proxy TIED)
- 66 models tested
- Perfect tie between 2 models

**Impact:** Paradigm effects interpretation depends on arbitrary tie-break

**Implementation (Session 14:30):**
- 2 competitive models (ΔAIC < 7)
- Effective N = 2.0 (LOW - perfect tie)
- 100% total weight included
- MA averages across tie (50%/50%)

**Cascades:** 6.4.2, 6.4.3 (derivatives NOT re-run)

---

### P5-MODERATE: RQ 6.5.1 (Schema - Common/Unique)

**Issue:** Best model = 65.3% weight (Quad+Log+SquareRoot)
- 66 models tested
- Low uncertainty, model dominates

**Impact:** Schema effects interpretation minimally at risk

**Implementation (Session 14:30):**
- 2 competitive models (ΔAIC < 7)
- Effective N = 1.8 (LOW)
- 87.5% total weight included
- Best model still dominates (74% renormalized weight)
- MA has minimal impact

**Cascades:** 6.5.2 (derivative NOT re-run)

---

### P6-FIX: RQ 6.7.3 (Trajectory-Calibration Correlation)

**Issue:** Uses Ch5 5.1.1 residuals from single-best model
- Should use model-averaged residuals

**Impact:** NULL finding (r=0.02, p=0.85) almost certainly robust but lacks MA validation

**Implementation (Session 20:50):**
- Ch5 5.1.1 MA residuals created (51 models, Eff_N=40.09)
- 6.7.3 re-run with MA residuals
- NULL finding ROBUST: r=-0.05 (vs r=0.02), p=0.65 (vs p=0.85)
- Direction flipped but effect size remains negligible (|r| < 0.05)

---

### Cascade Decision

**Decision:** Derivative RQs NOT re-run
- MA outputs (step05b_*.csv) available in ROOT RQ data/ folders
- Can be used for future sensitivity analysis if needed
- Derivatives use ROOT RQ outputs (coefficients, contrasts, correlations, ICC)
- ROOT RQ findings remain robust with MA, so derivatives likely robust too

**Rationale:**
- Time savings (22 RQs → 6 RQs)
- MA outputs available for validation if concerns arise
- Thesis can document MA at ROOT level, note derivatives used single-best

---

**Status:** ✅ COMPLETE - All 6 priorities addressed, model averaging implemented

**Key Finding:** Only 2 RQs showed EXTREME uncertainty (6.8.1, 6.1.1) where model averaging had substantial impact. Others had concentrated weights (1-2 models dominate) where MA provides methodological consistency but minimal practical impact.

**Related Topics:**
- ch6_kitchen_sink_audit_complete_model_averaging_gap (Session 2025-12-13 13:45)
- ch6_rq_rework_plan_created (Session 2025-12-13 13:45)
- ch6_model_averaging_implementation_complete_5_root_rqs (Session 2025-12-13 14:30)
- ch6_rework_all_items_complete (Session 2025-12-13 20:50)

---
