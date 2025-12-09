# Chapter 5 RQ Status Tracker - User Guide

**File:** `rq_status.tsv`
**Last Updated:** 2025-12-09
**Purpose:** Comprehensive roadmap for taking Ch5 RQs from current state to PhD thesis gold-standard

---

## What This Document Is

This TSV file is your **actionable roadmap** for completing Chapter 5. It tells you:
1. **What's done** vs what needs work
2. **Why** each RQ isn't thesis-ready (specific gaps)
3. **What to do** next (concrete action)
4. **How long** it will take (effort estimate)
5. **Which order** to do them (priority + dependencies)

## Column Definitions

| Column | Meaning | Example Values |
|--------|---------|----------------|
| **RQ** | RQ identifier | 5.1.1, 5.2.3, 5.4.7 |
| **Type** | Category + ROOT/derivative | General/ROOT, Paradigms/Consolidation |
| **Status** | Current completion level | GOLD, COMPLETE, DEPRIORITIZED |
| **Model_Form** | Which model/approach used | PowerLaw α=0.410, Recip+Log, Log HYBRID |
| **Gaps** | What prevents thesis-ready | ROOT_Cascade_CRITICAL, Plots_Outdated, - |
| **Next_Action** | Single most important step | RERUN with Recip+Log, Regenerate plots, None |
| **Effort** | Time estimate | 30min, 2hr, 1day, 0 (done) |
| **Priority** | Urgency level | CRITICAL, HIGH, MODERATE, LOW, DONE |
| **Blocks** | Which RQs depend on this | 5.4.2,5.4.3,5.4.4 (this RQ blocks these) |
| **Dependencies** | Which RQs this depends on | 5.4.1 (this RQ needs 5.4.1 first) |
| **Validation** | Has validation.md? Status? | PASS, PARTIAL, PASS (obsolete) |
| **Notes** | Key findings + context | Brief summary of results + issues |

---

## Status Values Explained

- **GOLD**: Extended model selection + averaging complete, plots current, interpretation updated, validation passed. **Thesis-ready with ZERO compromises.**
- **COMPLETE**: Analysis done and validated, but may need updates (model propagation, plots, interpretation).
- **DEPRIORITIZED**: Not executed, answered by another RQ or expected NULL.

---

## Priority Levels & What They Mean

### DONE (17 RQs)
**No action needed.** These are thesis-ready as-is.
- All Type 5.3 (Paradigms): 9/9 RQs DONE
- Type 5.5 (Source-Dest): 5/7 RQs DONE (2 optional verification)
- Type 5.2 (Domains): 1/8 ROOT DONE
- Type 5.4 (Congruence): 2/8 GOLD (5.4.6 variance + 5.4.7 clustering complete)

### HIGH (7 RQs) - **DO THESE FIRST**
**Critical cascade from ROOT model changes.** Must rerun before thesis defense.
- **Type 5.4 Congruence (4 RQs):** 5.4.2-5.4.5 need Recip+Log model update (~8 hours total, 5.4.6-5.4.7 COMPLETE)
- **Type 5.1 General (2 RQs):** 5.1.3 (practice decomposition), 5.1.4 (model comparison)
- **Type 5.2 Domains (1 RQ):** 5.2.7 (clustering rerun after 5.2.6)

### MODERATE-HIGH (2 RQs)
**Important for downstream analyses.**
- **5.1.4:** Model comparison (blocks 5.1.5)
- **5.2.6:** Variance decomposition rerun (blocks 5.2.7)

### MODERATE (3 RQs)
**Robustness checks or minor fixes.**
- **5.1.2:** Add AR(1) autocorrelation structure
- **5.1.5:** Clarify slope direction interpretation
- **5.2.2:** Regenerate plots (exclude When domain)

### LOW-MODERATE (3 RQs)
**Verify robustness (likely already OK).**
- **5.2.3, 5.2.4, 5.2.5:** Check if Log vs Recip+Log affects NULL findings (likely robust)

### LOW (2 RQs)
**Optional verification.**
- **5.5.2, 5.5.3:** Verify NULL findings with 13-model averaged predictions

---

## Critical Findings & Patterns

### 🔴 ROOT Model Changes (Cascade Impact)

**Three ROOT RQs underwent extended model selection, revealing:**

1. **5.1.1 (General/ROOT):**
   - Basic: Log 48% → Extended: PowerLaw α=0.410 (16 models averaged)
   - **ΔAIC = 3.10** vs Log (moderate impact)
   - **Derivatives affected:** 5.1.2-5.1.5 (minor updates needed)

2. **5.2.1 (Domains/ROOT):**
   - Basic: Log 62% → Extended: Recip+Log (10 models averaged)
   - **Two-process forgetting** (rapid 1/(t+1) + slow log(t+1))
   - **Derivatives affected:** 5.2.6-5.2.7 need rerun (random slopes + clustering)

3. **5.3.1 (Paradigms/ROOT):**
   - Basic: Log 99.98% → Extended: PowerLaw α=0.140 (14 models averaged)
   - **ΔAIC = 0.07** vs Log (NEGLIGIBLE)
   - **Derivatives affected:** NONE (Log still valid)

4. **5.4.1 (Congruence/ROOT):**
   - Basic: Log 99.98% → Extended: Recip+Log 73.7% (15 models, EXTREME uncertainty)
   - **ΔAIC = 7.50** vs Log (HIGH impact)
   - **Derivatives affected:** 5.4.2-5.4.7 **ALL NEED RERUN** (6 RQs, ~12 hours)

5. **5.5.1 (Source-Dest/ROOT):**
   - Basic: Log 63.5% → Extended: Quadratic 6.7% (13 models, EXTREME uncertainty)
   - **ΔAIC = 0.34** vs Log (TIED)
   - **HYBRID approach:** Log for tests, 13-model averaging for plots
   - **Derivatives affected:** 5.5.2-5.5.3 optional verification only

### 🎯 Key Insights

**Model Completeness Crisis Resolved:**
- Basic 5-model comparisons systematically **overconfident** (factor of 4-16,000×)
- Extended 66-model comparisons reveal true uncertainty
- Model averaging now **mandatory** for all trajectory RQs (weight < 30% threshold)

**Paradigm Shifts:**
- **5.1.1:** Ebbinghaus logarithmic → Wixted power-law forgetting
- **5.2.1 & 5.4.1:** Two-process forgetting (rapid reciprocal + slow logarithmic)

**Cross-Cutting Replications (Robust Findings):**
1. **Purification-Trajectory Paradox:** 4 replications (5.2.5, 5.3.6, 5.4.5, 5.5.5)
2. **ICC_slope ≈ 0:** 3 replications (5.2.6, 5.3.7, 5.4.6) - design limitation
3. **Weak Clustering:** 4 instances (5.2.7, 5.3.8, 5.4.7, 5.5.7 EXCEPTION)
4. **Item Difficulty Invariance:** 5.3.9 cross-classified GLMM (answers 5.1.6, 5.2.8, 5.4.8)

**Major Novel Discoveries:**
- **5.5.6:** OPPOSITE intercept-slope correlations (Source r=+0.989, Dest r=-0.903, both p<10⁻³⁷)
- **5.5.7:** EXCEPTIONAL clustering (Silhouette=0.417, ONLY Ch5 RQ ≥0.40 threshold)

---

## How to Use This Roadmap

### Step 1: Prioritize by Category

**Immediate (HIGH priority, 9 RQs, ~20 hours):**
```
Type 5.4: 5.4.2 → 5.4.3 → 5.4.4 → 5.4.5 → 5.4.6 → 5.4.7 (sequential on 5.4.6)
Type 5.1: 5.1.3 (practice decomposition) + 5.1.4 (model comparison)
Type 5.2: 5.2.7 (after 5.2.6 rerun)
```

**Secondary (MODERATE, 3 RQs, ~4 days):**
```
5.1.2 (AR1 autocorrelation)
5.1.5 (slope direction)
5.2.2 (plot regeneration)
5.2.6 (Recip+Log rerun) → feeds 5.2.7
```

**Verification (LOW, 5 RQs, ~3.5 hours):**
```
5.2.3, 5.2.4, 5.2.5 (check Recip+Log robustness)
5.5.2, 5.5.3 (check 13-model robustness)
```

### Step 2: Handle Dependencies

**Critical paths:**
1. **5.4.1 (DONE) → 5.4.2-5.4.7** (6 derivatives blocked until rerun)
2. **5.2.6 (needs rerun) → 5.2.7** (clustering depends on variance random effects)
3. **5.1.4 (model comparison) → 5.1.5** (clustering interpretation)

### Step 3: Estimate Timeline

**Conservative (doing everything):**
- HIGH priority: ~20 hours (3 days)
- MODERATE: ~4 days (2 days if parallel)
- LOW verification: ~3.5 hours (optional)
- **Total: 5-7 days full-time work**

**Aggressive (HIGH only + critical MODERATE):**
- Type 5.4 cascade: ~12 hours (can parallelize 5.4.2-5.4.5, then 5.4.6→5.4.7)
- 5.1.3, 5.1.4, 5.2.6, 5.2.7: ~7 hours
- **Total: ~19 hours = 2.5 days**

### Step 4: Quality Gates

**Before marking RQ as GOLD:**
- [ ] Extended model comparison run (if trajectory RQ)
- [ ] Model averaging applied (if best weight < 30%)
- [ ] Plots regenerated with model-averaged predictions
- [ ] Interpretation updated (theory section matches model)
- [ ] Validation.md exists and PASS
- [ ] All derivative RQs updated if ROOT changed

---

## FAQ

**Q: Why are some RQs marked COMPLETE but need rerun?**
A: They were completed BEFORE extended model selection on ROOT RQs. Original analyses valid, but need updating to match new ROOT model (e.g., Log → Recip+Log).

**Q: What does "ROOT_Cascade_CRITICAL" mean?**
A: The ROOT RQ (e.g., 5.4.1) changed models after derivatives were done. Derivatives now use obsolete model and MUST be rerun.

**Q: Why are Type 5.3 RQs all DONE but Type 5.4 need reruns?**
A: **5.3.1 extended testing:** ΔAIC=0.07 (Log vs PowerLaw TIED) → derivatives still valid.
**5.4.1 extended testing:** ΔAIC=7.50 (Recip+Log DOMINATES) → derivatives invalid.

**Q: What's the difference between COMPLETE and GOLD?**
A: **COMPLETE** = Analysis done, may need updates. **GOLD** = Extended comparison + averaging + current plots + updated interpretation. ZERO compromises.

**Q: Can I skip LOW priority items?**
A: Yes, but document as limitations. NULL findings (5.2.3-5.2.5, 5.5.2-5.5.3) likely robust, but verification adds confidence.

**Q: How do I know if verification is needed?**
A: Check "Gaps" column for "Optional_Verification". If NULL finding with high power (p>>0.05, power=1.00), verification optional.

---

## Next Steps After Completion

1. **Update `results/ch5/story.md`** with extended model findings
2. **Create thesis Methods section** documenting model averaging protocol
3. **Write thesis Results sections** for each RQ with updated interpretations
4. **Archive this status file** with final completion date
5. **Generate Chapter 5 synthesis document** (cross-RQ patterns + novel discoveries)

---

## Contact & Documentation

**Questions?** See:
- `docs/lmm_methodology.md` - LMM specifications
- `docs/results/models.md` - Extended model comparison protocol
- `.claude/CLAUDE.md` - Analysis pipeline overview
- `results/ch5/5.X.X/results/summary.md` - Individual RQ results

**Status tracking:**
- This file (`rq_status.tsv`) - Current state
- `results/ch5/rq_status_UPDATED.tsv` - Extended model findings (MERGED into this file)
- Archive files in `.claude/context/archive/` - Historical decisions

---

**Last Updated:** 2025-12-09 by Claude Code (context-finder synthesis)
**Next Update:** After completing HIGH priority cascade (Type 5.4 reruns)
