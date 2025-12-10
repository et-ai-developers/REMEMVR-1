# Chapter 5 RQ Status Tracker - User Guide

**File:** `rq_status.tsv`
**Last Updated:** 2025-12-10 (RQ 5.5.3 → GOLD, FINAL ROOT verification complete, 22/40 GOLD = 55.0%)
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

### DONE (27 RQs) - ✅ **22/40 GOLD (55.0% - OVER HALFWAY) 🎉**
**No action needed.** These are thesis-ready as-is.
- All Type 5.3 (Paradigms): 9/9 RQs DONE
- **Type 5.5 (Source-Dest): 7/7 GOLD ✅** (ALL COMPLETE - 100% gold standard)
- **Type 5.1 (General): 5/6 GOLD** (5.1.1 ROOT, 5.1.2 two-phase + practice, 5.1.3 age + practice, 5.1.4 variance, 5.1.5 clustering)
- **Type 5.2 (Domains): 7/8 GOLD** (5.2.1 ROOT, 5.2.2 consolidation, 5.2.3 age + ROOT verification, 5.2.4 IRT-CTT + ROOT verification, 5.2.5 PurifiedCTT + ROOT verification, 5.2.6 variance, 5.2.7 clustering)
- **Type 5.4 (Congruence): 6/6 GOLD ✅** (5.4.1 ROOT, 5.4.2 consolidation, 5.4.3 age, 5.4.4 IRT-CTT, 5.4.5 PurifiedCTT, 5.4.6 variance, 5.4.7 clustering ALL COMPLETE)

### HIGH (0 RQs) - ✅ **ALL COMPLETE**
**No high-priority items remaining.** Type 5.1 General fully complete with practice decomposition methodology.

### MODERATE-HIGH (2 RQs)
**Important for downstream analyses.**
- **5.1.4:** Model comparison (blocks 5.1.5)
- **5.2.6:** Variance decomposition rerun (blocks 5.2.7)

### MODERATE (0 RQs)
**Robustness checks or minor fixes.**
- None remaining (5.1.2 elevated to HIGH)

### LOW-MODERATE (0 RQs) - ✅ **ALL COMPLETE**
**No low-moderate priority items remaining.**

### LOW (0 RQs) - ✅ **ALL COMPLETE**
**No low-priority items remaining.** All optional ROOT verifications complete.

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
- **5.1.2:** Two-phase deceleration reinterpreted → Practice saturation (5.7x) explains more than consolidation

**NEW: Practice Decomposition Methodology (2025-12-09):**
- **RQ 5.1.2:** Dual-phase model separates T1→T2 (practice+forgetting) from T2→T4 (forgetting only)
- **Finding:** Practice PARTIALLY masks forgetting (5.7x difference, p<0.000002)
- **RQ 5.1.3:** Age-invariance test reveals practice effects equal across ages (p=0.41)
- **Impact:** Resolves wrong-direction artifacts, strengthens VR Scaffolding Hypothesis
- **Generalizability:** Method applicable to ALL repeated-measures memory designs

**CRITICAL METHODOLOGICAL DISCOVERY (RQ 5.4.2, 2025-12-09):**
- **Random effects structure matters MORE than functional form**
- Piecewise (AIC=2581.55, random slopes) vs Continuous (AIC=2593.41, random intercepts)
- ΔAIC = +11.86 is driven by random effects complexity, NOT functional form superiority
- **Lesson:** Always match random effects structure when comparing models (apples-to-apples)
- **Pattern recognized:** Kitchen sink uses ~1 for stability, piecewise uses ~time for theory-testing
- **Consequence:** Cannot conclude discrete phases exist without matched-effects comparison

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

**Q: Why did RQ 5.4.2 use kitchen sink instead of just updating to Recip+Log?**
A: Sensitivity analysis showed continuous models fit MUCH better than piecewise (ΔAIC = -91). Rather than blindly updating functional form, we tested 66 models to let data determine best approach. Result: EXTREME uncertainty (15 competitive models, 6% best weight) requires model averaging. Also discovered that random effects structure matters MORE than functional form (piecewise better with random slopes, continuous tested with random intercepts for stability).

**Q: Why did RQ 5.4.3, 5.4.4, and 5.4.5 update to Recip+Log but not kitchen sink?**
A: These RQs test relationships/convergence, not trajectory shape. Findings expected robust across functional forms:
- **5.4.3 (Age):** NULL 3-way interactions confirmed with both Log and Recip+Log (0/4 significant)
- **5.4.4 (IRT-CTT):** Convergence IMPROVED with Recip+Log (kappa: 0.667 → 1.00 perfect agreement). **Kitchen sink sensitivity analysis (2025-12-09)** confirmed robustness: Both IRT and CTT show extreme model uncertainty (6% best weights across 66 models), yet convergence persists (r>0.87).
- **5.4.5 (PurifiedCTT):** Purification-trajectory paradox **ROBUST** across functional forms. Recip+Log STRENGTHENED paradox for Common (+1.8) and Congruent (+3.0), REVERSED Incongruent from Purified-better (-2.0) to TIED (+0.4). Straightforward ROOT update sufficient for all three.

**Q: Why are Type 5.3 RQs all DONE but Type 5.4 needed reruns?**
A: **5.3.1 extended testing:** ΔAIC=0.07 (Log vs PowerLaw TIED) → derivatives still valid.
**5.4.1 extended testing:** ΔAIC=7.50 (Recip+Log DOMINATES) → all 6 derivatives updated (NOW COMPLETE ✅).

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

**Last Updated:** 2025-12-10 by Claude Code (🎉🎉 MILESTONE: 22/40 GOLD = 55.0% - RQ 5.5.3 → GOLD, FINAL ROOT verification complete, Type 5.5 = 7/7 GOLD)
**Next Update:** After initiating work on remaining DEPRIORITIZED RQs (if thesis requires them)
