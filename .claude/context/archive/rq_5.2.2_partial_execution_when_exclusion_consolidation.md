# RQ 5.2.2 Execution - When Domain Exclusion & Consolidation

**Topic:** Complete execution history of RQ 5.2.2 (Domain-Specific Consolidation Effects with When Domain Exclusion)

**Created:** 2025-12-02 23:15

---

## Session (2025-12-02 23:15) - Partial Execution (Steps 00-02)

**Archived from:** state.md
**Original Date:** 2025-12-02 23:15
**Reason:** 3+ sessions old, partial RQ execution archived for historical record

**Task:** RQ 5.2.2 Partial Execution - Domain-Specific Consolidation Effects with When Domain Exclusion

**Context:** User requested step-by-step execution of RQ 5.2.2 with When domain exclusion due to floor effect discovered in RQ 5.2.1 (6-9% probability, 77% item exclusion). Session paused after Step 02 for /save.

**Major Accomplishments:**

**1. Document Updates for When Domain Exclusion**

Updated `1_concept.md` and `2_plan.md` to reflect When domain exclusion:
- Research question changed from 3 domains (What/Where/When) to 2 domains (What/Where)
- Expected row counts reduced: 1200 → 800 rows
- Planned contrasts reduced: 6 → 3 (Bonferroni α = 0.0167)
- Validation criteria updated throughout

**2. Steps 00-02 Completed Successfully**

| Step | Name | Output | Status |
|------|------|--------|--------|
| 00 | Prepare piecewise input | 800 rows (filtered from 1200) | ✅ |
| 01 | Fit piecewise LMM | 8 fixed effects, converged | ✅ |
| 02 | Extract slopes | 4 segment-domain slopes | ✅ |

**3. Key Bug Fixes During Execution**

**Step 00 - Data source correction:**
- Original code referenced RQ 5.1.1 data (overall theta, no domains)
- Fixed: Changed to RQ 5.2.1 data (domain-specific theta scores)
- Fixed: Test numbering is 1,2,3,4 (sequential) not 0,1,3,6 (nominal days)
- Updated SEGMENT_MAPPING: Early=[1,2], Late=[3,4]

**Step 00 - When domain filter:**
- Added explicit filter: `df = df[df["domain"].isin(["what", "where"])]`
- Logged row reduction: 1200 → 800 rows (400 When rows removed)

**Step 02 - Slope computation update:**
- Removed When domain slope calculations (was computing 6 slopes, now 4)
- Updated validation: expected_domains = {"what", "where"} instead of {"what", "where", "when"}

**4. Statistical Results Summary (Partial)**

**Model Fit (Step 01):**
- 3-way Days_within × Segment × domain interaction LMM
- 800 observations, 100 groups (UIDs)
- Log-Likelihood: -756.82, AIC: 1537.63

**Key Fixed Effects:**
- Days_within: **-0.4564 (p<.001)** - significant forgetting slope in Early-What
- Days_within×Segment[T.Late]: **+0.3854 (p<.001)** - slope flattens significantly in Late
- Days_within×domain[T.where]: 0.0233 (p=.775) - no domain difference
- 3-way interaction: -0.0371 (p=.671) - **no differential consolidation by domain**

**Segment-Domain Slopes (Step 02):**
| Segment | Domain | Slope | SE | 95% CI |
|---------|--------|-------|-----|--------|
| Early | What | -0.456 | 0.059 | [-0.57, -0.34] |
| Early | Where | -0.433 | 0.059 | [-0.55, -0.32] |
| Late | What | -0.071 | 0.025 | [-0.12, -0.02] |
| Late | Where | -0.085 | 0.025 | [-0.13, -0.04] |

**Preliminary Interpretation:**
- **Strong consolidation effect:** Early slopes (~-0.45) are ~6× steeper than Late slopes (~-0.08)
- **No domain-specific consolidation:** What ≈ Where in both segments
- **Hypothesis NOT supported:** Spatial memory (Where) does not show greater consolidation benefit than object identity (What)

**5. Files Created/Modified**

**Document Updates (2):**
- `results/ch5/5.2.2/docs/1_concept.md` - When excluded, hypothesis updated
- `results/ch5/5.2.2/docs/2_plan.md` - Row counts, contrasts, validation updated

**Code Files Modified (3):**
- `results/ch5/5.2.2/code/step00_prepare_piecewise_input.py` - RQ 5.2.1 source, When filter, test numbering
- `results/ch5/5.2.2/code/step01_fit_piecewise_lmm.py` - Docstring updated for 2 domains
- `results/ch5/5.2.2/code/step02_extract_slopes.py` - 4 slopes instead of 6, validation updated

**Data Files Created (3):**
- `data/step00_piecewise_lmm_input.csv` (800 rows, 8 cols)
- `data/step01_piecewise_lmm_model.pkl` (fitted model)
- `results/step01_piecewise_lmm_summary.txt` (model output)

**Results Files Created (2):**
- `results/step02_fixed_effects.csv` (11 terms including RE variance)
- `results/step02_segment_domain_slopes.csv` (4 rows: 2 segments × 2 domains)

**6. Remaining Steps (3)**

| Step | Name | Status |
|------|------|--------|
| 03 | Compute contrasts | Pending (needs code update for 3 contrasts) |
| 04 | Compute consolidation benefit | Pending (needs code update for 2 domains) |
| 05 | Prepare plot data | Pending (needs code update for 8 rows) |

**Session Metrics:**

**Tokens:**
- Session start: ~6k (after /refresh)
- Session end: ~45k (at /save)
- Delta: ~39k consumed

**Bug Fixes:** 4 issues fixed during execution
1. Data source correction (5.1.1 → 5.2.1)
2. Test numbering (0,1,3,6 → 1,2,3,4)
3. When domain filter addition
4. Slope computation reduction (6 → 4)

**Key Insights:**

**When Domain Exclusion:**
- Floor effect discovered in RQ 5.2.1: 6-9% probability throughout study
- 20/26 When items (77%) excluded for low discrimination
- Cannot meaningfully interpret When domain forgetting
- Consistent approach: All subsequent domain RQs exclude When

**Consolidation Effect Pattern:**
- Strong segment effect (Early vs Late) confirms consolidation hypothesis
- ~6× slope reduction after Day 1 (consolidation window)
- However, no domain-specific consolidation benefit
- What and Where consolidate equally

**End of Session (2025-12-02 23:15)**

**Status:** 🔄 **RQ 5.2.2 IN PROGRESS** - Completed Steps 00-02 (data prep, LMM fit, slope extraction) with When domain exclusion. 4 bugs fixed (data source, test numbering, When filter, slope reduction). **PRELIMINARY FINDING:** Strong consolidation effect (~6× slope reduction) but no domain-specific benefit - What ≈ Where. Steps 03-05 remaining (contrasts, consolidation benefit, plot data). Session paused for /save at ~45k tokens.

---

## Session (2025-12-03 00:15) - Complete Execution + RQ 5.2.3 Documentation Updates

**Archived from:** state.md
**Original Date:** 2025-12-03 00:15
**Reason:** 3+ sessions old, RQ 5.2.2 complete + RQ 5.2.3 docs updated

**Task:** RQ 5.2.2 Complete Execution + RQ 5.2.3 Documentation Updates for When Domain Exclusion

**Context:** User requested continuation of RQ 5.2.2 (Steps 03-05) then preparation of RQ 5.2.3 for When domain exclusion.

**Major Accomplishments:**

**1. RQ 5.2.2 Complete - All 6 Steps Executed**

Completed remaining Steps 03-05 with When domain exclusion:

| Step | Name | Output | Status |
|------|------|--------|--------|
| 00 | Prepare piecewise input | 800 rows (When excluded) | ✅ |
| 01 | Fit piecewise LMM | 8 fixed effects, converged | ✅ |
| 02 | Extract slopes | 4 segment-domain slopes | ✅ |
| 03 | Compute contrasts | 3 contrasts (reduced from 6) | ✅ |
| 04 | Consolidation benefit | 2 domain benefits | ✅ |
| 05 | Prepare plot data | 8 rows (2 domains × 4 tests) | ✅ |

**Key Finding: NO Domain-Specific Consolidation Effects**

All 3 contrasts between What and Where domains non-significant:
- Early segment: What vs Where slope difference p = 0.698
- Late segment: What vs Where slope difference p > 0.68
- Consolidation benefit: What vs Where benefit difference p > 0.68

**Consolidation Benefit Results:**

| Domain | Early Slope | Late Slope | Benefit (Early-Late) | Benefit % |
|--------|-------------|------------|---------------------|-----------|
| What | -0.456 | -0.071 | 0.385 | 84.4% |
| Where | -0.433 | -0.085 | 0.348 | 80.4% |

Both domains show strong consolidation (~6× slope reduction) but benefits are statistically equivalent.

**2. RQ 5.2.3 Documentation Updated for When Domain Exclusion**

Updated 3 files to reflect When domain exclusion pattern:
- `results/ch5/5.2.3/docs/1_concept.md` - Research question scope changed
- `results/ch5/5.2.3/docs/2_plan.md` - Row counts, validation criteria updated
- `results/ch5/5.2.3/code/step00_get_data_from_rq51.py` - When filter added

**Hypothesis Status:**
- **NOT SUPPORTED:** Spatial memory (Where) does NOT show greater consolidation benefit than object identity (What)
- Both domains consolidate equally after Day 1
- VR episodic memory may not follow traditional consolidation patterns seen in non-VR spatial tasks

**Files Modified (RQ 5.2.2):**
- 3 code files (steps 03-05)
- 6 data files created
- 3 results files created
- Full validation pipeline executed (rq_inspect, rq_plots, rq_results)

**Files Modified (RQ 5.2.3):**
- 1 concept file
- 1 plan file
- 1 step00 code file

**Session Metrics:**
- Tokens consumed: ~40k
- Steps completed: 3 (RQ 5.2.2) + 3 files updated (RQ 5.2.3)
- Bugs fixed: 0 (all APIs correct from previous session)

**Key Insights:**

**Domain Consolidation Pattern:**
- When domain cannot be analyzed (floor effect 6-9% probability, 77% attrition)
- What and Where domains show equivalent consolidation (~80-84% slope reduction)
- No evidence for domain-specific consolidation mechanisms in VR episodic memory

**Methodological Consistency:**
- All downstream domain RQs (5.2.X) must exclude When domain
- Pattern documented across RQ suite for transparency
- Statistical approach (3 contrasts, Bonferroni α = 0.0167) maintains rigor

**End of Session (2025-12-03 00:15)**

**Status:** ✅ **RQ 5.2.2 COMPLETE** - All 6 steps executed, NULL FINDING documented (no domain-specific consolidation), full validation pipeline passed. ✅ **RQ 5.2.3 DOCUMENTATION UPDATED** - When domain exclusion pattern applied, ready for future execution.

---
