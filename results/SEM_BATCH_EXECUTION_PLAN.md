# SEM Calibration Batch Execution Plan
**Date:** 2025-12-28
**Status:** Phase 2 & 3 Prototypes COMPLETE - Ready for full batch

**Context:** Phases 2 & 3 validated SEM approach - all RQs weaken (artifact removal), but ROBUST effects SURVIVE (p<0.05) while SPURIOUS effects DISAPPEAR (p>0.05).

---

## Phase 2 & 3 Results (COMPLETED) ✅

| RQ | Type | PRE-SEM | POST-SEM | Status | Classification |
|----|------|---------|----------|--------|----------------|
| **6.2.2** | Proportion overconf | p=0.230 (ns) | p=0.807 (ns) | ✅ DONE | **NULL** (artifact disappeared) |
| **6.2.1** | Magnitude worsens | p=0.004 ⭐⭐ | p=0.013 ⭐ | ✅ DONE | **ROBUST** (effect survived) |

**Key Pattern:**
- **BOTH weakened** (78-80% artifact components)
- **6.2.1 survived** (still p<0.05 → ROBUST)
- **6.2.2 disappeared** (p>0.05 → SPURIOUS)

---

## Remaining RQs Requiring SEM (Estimated: 13-18 RQs)

### Tier 1: CRITICAL (r_diff < 0.20) - 2 RQs

| RQ | Description | r_diff | Current Status | Priority |
|----|-------------|--------|----------------|----------|
| **6.3.2** | Domain × Time calibration | 0.085 | BLOCKED | **URGENT** |
| **6.6.2** | Baseline conf → HCE | Unknown | BLOCKED | **URGENT** |

**Expected:**
- Both have catastrophic reliability
- 6.3.2 has major finding (crossover interaction χ²=59.60, p<0.0001)
- High risk: findings may be artifacts

---

### Tier 2: HIGH (r_diff 0.20-0.60) - 3 RQs

| RQ | Description | r_diff | Current Status | Priority |
|----|-------------|--------|----------------|----------|
| **6.8.2** | Conf variability × Time | 0.379 | PLATINUM (caveat) | HIGH |
| **6.5.2** | Paradigm × Session calib | 0.536 | PLATINUM (caveat) | HIGH |
| **6.4.2** | Paradigm calibration | 0.66 | PLATINUM (caveat) | MODERATE |

**Expected:**
- Poor to marginal reliability
- May or may not survive SEM
- Survival depends on real effect strength

---

### Tier 3: MODERATE (r_diff > 0.60 or unknown) - 8-13 RQs (estimated)

**6.2.X Series (Calibration Trilogy):**
- 6.2.3: Resolution discrimination
- 6.2.4: (if exists, check dependency)
- 6.2.5: (if exists, check dependency)

**6.3.X Series (Domain Calibration):**
- 6.3.3: (if exists)
- 6.3.4: (if exists)

**6.4.X Series (Paradigm Calibration):**
- 6.4.3: (if exists)
- 6.4.4: (if exists)

**6.5.X Series (Paradigm × Session):**
- 6.5.3: (if exists)

**6.6.X Series (High-Confidence Errors):**
- 6.6.3: (if exists)

**6.7.X Series (Accuracy Variability - may use calibration):**
- 6.7.3: (confirmed reference to 6.2.1 calibration)

**6.8.X Series (Confidence Variability):**
- 6.8.3: (if exists)
- 6.8.4: (if exists)

**Expected:**
- Marginal reliability (0.60-0.70)
- Moderate survival rate
- ~50% ROBUST, ~50% NULL

---

## Execution Strategy

### Phase 4: Systematic Batch (40-60h estimated)

**Workflow for EACH RQ:**

**Step 1: Check Dependency (5 min)**
- Does this RQ use calibration from 6.2.1?
- Or does it compute its own difference score?

**Step 2: Apply SEM Calibration (30 min)**
- If uses 6.2.1: Already have SEM scores
- If computes own: Create RQ-specific SEM script (like step02_compute_calibration_SEM.py)

**Step 3: Re-run Analysis (60 min)**
- Modify analysis script to use SEM calibration
- Run full analysis pipeline
- Generate all output files

**Step 4: Compare & Classify (30 min)**
- PRE-SEM vs POST-SEM p-values
- Coefficient changes
- Classify as ROBUST/NULL/MARGINAL

**Step 5: Document (30 min)**
- Create comparison report (like PHASE2_SEM_PROTOTYPE_COMPARISON.md)
- Update summary.md with SEM findings
- Note survival status

**Total per RQ:** ~2.5-3 hours
**Total for 13-18 RQs:** 32-54 hours

---

## Classification Framework

After SEM, classify each RQ:

### PLATINUM-ROBUST ✅
**Criteria:** p<0.05 POST-SEM
**Interpretation:** Real effect confirmed (survives artifact removal)
**Documentation:** "Effect robust to SEM validation (p=X.XX)"
**Examples:** RQ 6.2.1 (p=0.013 POST-SEM)

### PLATINUM-NULL ⭐
**Criteria:** p>0.05 POST-SEM
**Interpretation:** True null confirmed (artifact removed)
**Documentation:** "No significant effect after controlling measurement error (p=X.XX)"
**Examples:** RQ 6.2.2 (p=0.807 POST-SEM)

### PLATINUM-MARGINAL ⚠️
**Criteria:** 0.05 < p < 0.10 POST-SEM
**Interpretation:** Uncertain, report both versions
**Documentation:** "Weak evidence POST-SEM (p=X.XX), interpret cautiously"
**Examples:** (TBD)

---

## Batch Execution Order

**Priority 1: Tier 1 RQs (2 RQs, ~6h)**
1. RQ 6.3.2 (domain × time crossover - major finding at risk)
2. RQ 6.6.2 (baseline conf → HCE - theoretical importance)

**Priority 2: Tier 2 RQs (3 RQs, ~9h)**
3. RQ 6.8.2 (confidence variability)
4. RQ 6.5.2 (paradigm × session)
5. RQ 6.4.2 (paradigm calibration)

**Priority 3: Tier 3 RQs (8-13 RQs, ~24-39h)**
- Start with 6.2.X series (calibration trilogy derivatives)
- Then 6.3.X, 6.4.X series
- Finally 6.7.X, 6.8.X if they use calibration

**Total estimate:** 39-54 hours for full batch

---

## Success Metrics

### Quantitative
- [ ] All Tier 1 RQs classified (ROBUST/NULL/MARGINAL)
- [ ] All Tier 2 RQs classified
- [ ] ≥80% of Tier 3 RQs classified
- [ ] Survival rate documented (~40-60% expected)

### Qualitative
- [ ] Major findings validated (6.3.2 crossover, 6.6.2 metacognitive deterioration)
- [ ] NULL findings confirmed (stronger evidence)
- [ ] Conservative effect size estimates (defensible)
- [ ] Publication-ready methodology (SEM validation complete)

### Documentation
- [ ] Individual comparison reports for Tier 1-2 RQs
- [ ] Batch summary report (ROBUST vs NULL pattern)
- [ ] Updated summary.md files with SEM findings
- [ ] Thesis implications document

---

## Risk Mitigation

### Risk 1: Major Findings Disappear
**Concern:** 6.3.2 crossover (χ²=59.60, p<0.0001) may be artifact
**Mitigation:** If disappears, it's scientifically correct (was measurement error)
**Backup:** Have alternative theoretical interpretations ready

### Risk 2: Too Many NULLs
**Concern:** >60% survival failure = underpowered study
**Mitigation:** NULL findings are equally valuable (confirmed via gold-standard SEM)
**Defense:** "We didn't cherry-pick - we tested everything rigorously"

### Risk 3: Time Overrun
**Concern:** 40-60h estimate may be conservative
**Mitigation:** Can pause after Tier 1-2 (critical RQs) if needed
**Checkpoint:** Review after 5 RQs (~15h), assess pace

---

## Next Steps (IMMEDIATE)

**Option A: Start Tier 1 Batch (Recommended)**
1. RQ 6.3.2 (domain × time, r_diff=0.085, crossover at risk)
2. RQ 6.6.2 (baseline conf, metacognitive deterioration)
3. **Time:** ~6 hours total
4. **Result:** Validate pattern on highest-risk RQs

**Option B: Complete Inventory First**
1. Search all 6.X.X RQ directories
2. Identify which ones actually use calibration
3. Refine Tier 3 list (currently estimated)
4. **Time:** ~30 min
5. **Result:** Exact scope known before starting

**Option C: Strategic Selection**
1. Pick 3-5 theoretically critical RQs only
2. Leave rest for "future work"
3. **Time:** ~9-15 hours
4. **Result:** Core thesis validated, scope reduced

---

## My Recommendation: Option B → A

**Reasoning:**
1. **Inventory first** (30 min) - Know exact scope before committing
2. **Then Tier 1 batch** (6h) - Validate highest-risk findings
3. **Checkpoint decision** - Continue to Tier 2-3 or pause

**Benefits:**
- No wasted effort on non-calibration RQs
- Clear understanding of total time commitment
- Can adjust strategy based on Tier 1 results

**Next action:** Run systematic inventory of all Ch6 RQs to identify which ones actually compute/use calibration scores.

---

**End of Batch Execution Plan**

**Status:** Ready to proceed with systematic inventory → Tier 1 execution
