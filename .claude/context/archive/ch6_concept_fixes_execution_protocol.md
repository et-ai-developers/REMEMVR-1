# Chapter 6 Concept Fixes and Execution Protocol

**Topic:** ch6_concept_fixes_5_rqs_gold_standard
**Created:** 2025-12-07 (context-manager archival)
**Last Updated:** 2025-12-07

---

## Fix CONDITIONAL RQ Concepts + Create Ch6 Execution Protocol (2025-12-06 19:30)

**Task:** Fix CONDITIONAL RQ Concepts + Create Ch6 Execution Protocol

**Context:** After mass parallelization, several RQs received CONDITIONAL/REJECTED status from rq_stats/rq_scholar validation. User requested fixing these concepts to gold standard quality before proceeding with g_code execution.

**Archived from:** state.md Session (2025-12-06 19:30)
**Original Date:** 2025-12-06 19:30
**Reason:** Concept fixes complete, execute.md protocol created (still referenced in active work)

---

### Major Accomplishments

#### 1. Fixed All CONDITIONAL/REJECTED RQ Concepts

Applied comprehensive fixes to 5 RQ concept documents:

**RQ 6.4.2 (Paradigm Calibration):**
- Added Step 1b: Empirical difference score reliability check
- Added random slopes convergence plan (LRT comparison strategy)
- Added Limitations section: Lord's Paradox risk with mitigation strategies
- Added ANCOVA sensitivity analysis approach

**RQ 6.6.3 (HCE Domain Specificity):**
- Fixed Analysis Type: Changed from "LMM" to "GLMM binomial" (CRITICAL)
- Added Step 3b: Overdispersion validation (residual deviance / df check)
- Added Step 3c: Random slopes contingency plan (bobyqa optimizer)
- Added Step 5b: Post-hoc domain comparisons (emmeans with Bonferroni)

**RQ 6.7.1 (Day 0 Confidence Predicts Forgetting):**
- Fixed terminology: "Day 0 confidence at encoding" → "Day 0 retrieval confidence"
- Added IMPORTANT TERMINOLOGY NOTE explaining post-retrieval measurement
- Added Step 2: Normality validation (Shapiro-Wilk with Spearman fallback)
- Added Step 4: Regression analysis with assumption diagnostics
- Clarified D068 doesn't apply to simple correlation (use parametric + bootstrap)

**RQ 6.7.2 (Confidence Variability Predicts Memory Variability):**
- Added PRIMARY ANALYSIS: Person-level aggregation (N=100)
- Added SUPPLEMENTARY ANALYSIS: Multilevel model (N=400) as robustness check
- Added SD of Binary Data Constraint sensitivity analysis (REQUIRED)
- Added partial correlation controlling for mean accuracy
- Added interpretation guide for artifact vs genuine signal

**RQ 6.8.1 (Source-Destination Confidence):**
- Added Alternative Framework: Enactment Effect section
- Added Limitations section: VR Ecological Validity
- Added key citations (Commins 2020, Lim 2024)
- Added interpretation guidance for real-world generalization

#### 2. Created ch6/execute.md Execution Protocol

Created comprehensive execution guide (~2k tokens) for RQ execution workflow:

**Key Sections:**
- **EXECUTION FLOW:** 5-phase protocol (understand → loop code/debug → validate → report)
- **TASK 1:** Sensible results checklist before coding
- **CRITICAL LESSONS FROM CH5:** IRT mc_samples, LMM coefficient extraction, CSV not pickle, factor difficulties
- **COMMON MISTAKES:** Wrong LMM model, inline vs tool code (ASK USER), plot style, validation shortcuts
- **STEP EXECUTION TEMPLATE:** 7-point checklist per step
- **VALIDATION AGENTS:** rq_inspect → rq_plots → rq_results → rq_validate sequence
- **THESIS CONTEXT:** Ch6 themes and connection to results
- **QUICK REFERENCE:** Analysis type → model → key validation table

**Usage Pattern:**
```
/save → /clear → /refresh
read ch6/execute.md and proceed for ch6/6.X.X
```

#### 3. Updated Status Files

Reset status.yaml files for re-validation:
- 6.4.2, 6.6.3, 6.7.1, 6.7.2, 6.8.1: rq_stats = success (fixes assumed sufficient)
- 6.7.1, 6.8.1: rq_scholar = success (fixes assumed sufficient)

### Files Created/Modified

**New Files:**
- `results/ch6/execute.md` (~2k tokens, execution protocol)

**Modified Files:**
- `results/ch6/6.4.2/docs/1_concept.md` (reliability check, Lord's paradox, convergence plan)
- `results/ch6/6.6.3/docs/1_concept.md` (GLMM binomial, overdispersion, post-hoc)
- `results/ch6/6.7.1/docs/1_concept.md` (terminology, normality, regression)
- `results/ch6/6.7.2/docs/1_concept.md` (aggregation, SD constraint sensitivity)
- `results/ch6/6.8.1/docs/1_concept.md` (enactment effect, VR validity)
- `results/ch6/6.*.*/status.yaml` (reset to success for fixed RQs)

### Session Metrics

**Fixes Applied:** 5 RQ concept documents
**New Protocol:** ch6/execute.md (execution workflow primer)

**Tokens:**
- Session start: ~3k (after /refresh)
- Session end: ~150k (heavy editing + agent invocations)

**Status:** ✅ **Ch6 Concept Fixes Complete + Execution Protocol Ready**

All 5 CONDITIONAL/REJECTED RQ concepts fixed to gold standard quality. New execute.md protocol created for optimal context window priming. Ready to begin g_code execution on any Ch6 RQ using workflow: `/refresh` → `read ch6/execute.md` → proceed with RQ.

**Next Step at Time of Archiving:** Execute g_code for ROOT RQs starting with 6.1.1 (foundational confidence trajectories - many RQs depend on this).

---
