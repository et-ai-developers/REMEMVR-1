# Paradigms Section Complete (RQ 5.3.6-5.3.9) - Cross-Cutting Findings Replicated

**Topic:** paradigms_5.3.6_5.3.9_complete_cross_cutting_replication
**Created:** 2025-12-04 20:00
**Last Updated:** 2025-12-04 20:00

---

## Complete Paradigms Section (RQ 5.3.6-5.3.9) Execution (2025-12-04 03:00)

**Task:** Complete Paradigms Section (RQ 5.3.6-5.3.9) - Final 4 RQs of Paradigms Analysis

**Context:** User requested execution of remaining paradigms RQs following execution_plan.md. This session completed all 4 remaining RQs in the Paradigms section (5.3.6, 5.3.7, 5.3.8, 5.3.9), bringing Chapter 5 to 94% completion (29/31 RQs).

**Archived from:** state.md Session (2025-12-04 03:00)
**Original Date:** 2025-12-04 03:00
**Reason:** All 4 paradigm RQs completed and validated, cross-cutting findings replicated across all 3 factor structures

### Major Accomplishments

## RQ 5.3.6: Purified CTT Effects for Paradigms ✅ COMPLETE

#### Executed 9 Analysis Steps (step00-step08)

| Step | Name | Key Result |
|------|------|------------|
| 00 | Load dependencies | RQ 5.3.1 complete, 45/72 items retained |
| 01 | Map items | IFR 50%, ICR 79%, IRE 58% retention |
| 02-03 | Compute CTT | Full and Purified CTT scores |
| 04 | Reliability | IFR α improved +0.142, ICR unchanged, IRE decreased -0.044 |
| 05 | Correlation analysis | **ALL 3 paradigms significant** (Δr=+0.023 to +0.098) |
| 06 | Z-standardize | 9 columns validated |
| 07 | Fit parallel LMMs | 9 models converged, **PARADOX: Purified CTT WORSE AIC** |
| 08 | Prepare plot data | 6 correlation + 3 AIC rows |

**KEY FINDING: Purification-Trajectory Paradox Confirmed (3rd Replication)**
- Correlation improvement: IFR Δr=+0.098 (p<0.001), ICR Δr=+0.023 (p=0.034), IRE Δr=+0.050 (p=0.001)
- BUT AIC worse: IFR ΔAIC=-33.4, ICR ΔAIC=-5.3, IRE ΔAIC=-6.8 (negative = Full better)
- **Now confirmed across 3 factor structures:** Domains (5.2.5), Congruence (5.4.5), Paradigms (5.3.6)

---

## RQ 5.3.7: Variance Decomposition for Paradigms ✅ COMPLETE

#### Executed 7 Analysis Steps (step00-step06)

| Step | Name | Key Result |
|------|------|------------|
| 00 | Load theta | 1200 rows from RQ 5.3.1 |
| 01 | Load metadata | Log model best fit confirmed |
| 02 | Fit LMMs | 3 paradigm-stratified models |
| 03 | Compute ICC | 9 estimates (3 types × 3 paradigms) |
| 04 | Extract random effects | 300 rows for RQ 5.3.8 |
| 05 | Test correlations | D068 dual p-values |
| 06 | Compare ICC | Barplot data prepared |

**KEY FINDING: ICC_slope ≈ 0 for ALL Paradigms (Design Limitation Confirmed)**

| Paradigm | ICC_intercept | ICC_slope |
|----------|---------------|-----------|
| Free Recall | 0.501 (Substantial) | 0.022 (Low) |
| Cued Recall | 0.437 (Substantial) | 0.000 (Low) |
| Recognition | 0.515 (Substantial) | 0.015 (Low) |

**Interpretation:**
- Forgetting rates NOT trait-like (ICC_slope near zero)
- Replicates pattern from Domains (5.2.6) and Congruence (5.4.6)
- Design limitation: 4 timepoints insufficient to estimate slope variance reliably

---

## RQ 5.3.8: Clustering for Paradigms ✅ COMPLETE

#### Executed 8 Analysis Steps (step00-step07)

| Step | Name | Key Result |
|------|------|------------|
| 00 | Load random effects | 100 × 6 features from RQ 5.3.7 |
| 01 | Standardize | Z-scores validated |
| 02 | K selection | K=3 by BIC (parsimony rule from K=4) |
| 03 | Fit K-means | 3 clusters: 33, 31, 36 (balanced) |
| 04 | Validate quality | Silhouette=0.367, DB=0.981, Dunn=0.064 |
| 05 | Bootstrap stability | Jaccard=0.714 (marginal) |
| 06 | Characterize | No paradigm-selective profiles |
| 07 | Plot data | Scatter matrix prepared |

**KEY FINDING: Weak Clustering - No Memory Phenotypes (3rd Replication)**

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Silhouette | 0.367 | ≥ 0.40 | ❌ FAIL |
| Davies-Bouldin | 0.981 | < 1.50 | ✅ PASS |
| Jaccard | 0.714 | ≥ 0.75 | ❌ MARGINAL |

**Interpretation:**
- No paradigm-selective memory phenotypes (hypothesis NOT supported)
- Same pattern as Domains (5.2.7) and Congruence (5.4.7)
- Clustering driven by intercepts only (slopes ≈ 0)
- Memory is a continuous dimension, not discrete phenotypes

---

## RQ 5.3.9: Item LMM for Paradigms ✅ COMPLETE

#### Executed 5 Analysis Steps (step00-step04)

| Step | Name | Key Result |
|------|------|------------|
| 00 | Extract responses | 18,000 item-level observations |
| 01 | Create composite ID | 400 unique UIDs × tests |
| 02 | Center and merge | Difficulty_c mean=0, TSVR merged |
| 03 | Fit LMM | 3-way interaction tested |
| 04 | Extract interaction | Plot data prepared |

**KEY FINDING: 3-Way Interaction NOT Significant (Paradigm-Invariant)**

| Term | β | p_bonferroni | Significant? |
|------|---|--------------|--------------|
| Time:Difficulty_c:paradigmIFR | 0.00026 | 1.0 | ❌ No |
| Time:Difficulty_c:paradigmIRE | 0.00006 | 1.0 | ❌ No |

**Interpretation:**
- Item difficulty effects are PARADIGM-INVARIANT
- Harder items show lower accuracy, but relationship doesn't differ over time across paradigms
- Same pattern as Domains (5.2.8 - would show same if not BLOCKED)

---

### Session Metrics

**Chapter 5 Progress:**
- Before session: 25/31 RQs complete (81%)
- After session: **29/31 RQs complete (94%)**
- Paradigms section: **9/9 COMPLETE** (100%)
- Only 2 remaining: 5.1.6, 5.2.8 (both BLOCKED by GLMM tools)

**Cross-Cutting Findings Now Replicated Across ALL 3 Factor Structures:**

| Finding | Domains | Paradigms | Congruence |
|---------|---------|-----------|------------|
| Purification Paradox | 5.2.5 ✅ | **5.3.6** ✅ | 5.4.5 ✅ |
| ICC_slope ≈ 0 | 5.2.6 ✅ | **5.3.7** ✅ | 5.4.6 ✅ |
| Weak Clustering | 5.2.7 ✅ | **5.3.8** ✅ | 5.4.7 ✅ |
| Item Difficulty Invariant | 5.2.8 BLOCKED | **5.3.9** ✅ | 5.4.8 BLOCKED |

**Files Modified:**
- results/ch5/5.3.6/code/step*.py (9 scripts)
- results/ch5/5.3.6/data/* (16 files)
- results/ch5/5.3.6/plots/* (2 PNG + script)
- results/ch5/5.3.6/status.yaml
- results/ch5/5.3.7/code/step*.py (7 scripts)
- results/ch5/5.3.7/data/* (18 files)
- results/ch5/5.3.7/plots/* (1 PNG + script)
- results/ch5/5.3.7/status.yaml
- results/ch5/5.3.8/code/step*.py (8 scripts)
- results/ch5/5.3.8/data/* (13 files)
- results/ch5/5.3.8/plots/* (2 PNG + script)
- results/ch5/5.3.8/status.yaml
- results/ch5/5.3.9/code/step*.py (5 scripts)
- results/ch5/5.3.9/data/* (9 files)
- results/ch5/5.3.9/plots/* (1 PNG + script)
- results/ch5/5.3.9/status.yaml

### Cross-References

**Related Archive Topics:**
- ctt_irt_convergence_validated.md (2025-12-03 20:45: Purification paradox original discovery)
- icc_slope_deep_investigation_complete.md (2025-12-03 14:30: ICC_slope=0 as design limitation)
- rq_5.2.7_complete_domain_clustering.md (2025-12-03 22:50: Weak clustering methodology)
- rq53_paradigm_analysis.md (2025-11-24: Prior paradigms RQs 5.3.1-5.3.5)

---

**End of Archive Entry**
